#!/usr/bin/env python3
"""batch_grade.py - the lecturer's weekly command. Supersedes autograde.py.

Python standard library only. No Docker, no pip, no server, no network.

Grade a folder of notebooks against every test, visible and hidden:

    python3 batch_grade.py --assignment W05 --notebooks submissions/W05 \
        --data-dir data --out results/W05

Verify the tokens exported from the Google Form:

    python3 batch_grade.py --assignment W05 --tokens forms_W05.csv \
        --out results/W05

Do both, and audit a random 20 percent of the notebooks against what their
tokens claimed:

    python3 batch_grade.py --assignment W05 --notebooks submissions/W05 \
        --tokens forms_W05.csv --sample 20 --out results/W05

Outputs, all under --out:
    results.csv          one row per student, every question, plus flags
    feedback/<sid>.txt   the file to hand back to the student
    summary.txt          the same summary that is printed

Each notebook runs in its own subprocess from a clean interpreter, with a
per-cell timeout and a whole-notebook timeout, so one student's infinite loop
cannot stall the run. The per-cell timeout uses SIGALRM and is therefore
Unix-only; on Windows only the whole-notebook timeout applies. Run this on
Linux or macOS.

Student id comes from the notebook file name. Anything matching a student
number is taken from the start of the name, so all of these work:
    S24001.ipynb   S24001_W05.ipynb   W05_S24001 (2).ipynb
"""

import argparse
import csv
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import iuea_grader as ig                                            # noqa: E402

SID_RE = re.compile(r"(S\s?\d{4,8})", re.I)
RUNNER_NAME = "_run_one_notebook.py"


# --------------------------------------------------------------------------- #
# the subprocess runner, written out next to this file at run time
# --------------------------------------------------------------------------- #

RUNNER_SOURCE = r'''
"""Executed as a subprocess, one per notebook. Prints one JSON object.

Approach carried over from autograde.py: read the .ipynb as plain JSON, strip
IPython magics so they do not raise SyntaxError, execute the code cells
top-to-bottom in one shared namespace, then run the spec's checks against that
namespace. A cell that raises is recorded and the run continues, because a
student whose cell 3 fails may still have cells 4-10 correct.
"""
import io, json, os, signal, sys, traceback

nb_path, spec_path, hidden_path, assignment, cohort, out_path, per_cell = \
    sys.argv[1:8]
per_cell = int(per_cell)
hidden_path = hidden_path or None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iuea_grader as ig

R = {"status": "OK", "cell_errors": [], "cells_total": 0, "cells_ok": 0,
     "questions": {}, "fingerprint": "", "stdout_tail": ""}


def die(status, msg):
    R["status"] = status
    R["cell_errors"].append({"cell": -1, "etype": status, "emsg": msg})
    json.dump(R, open(out_path, "w"))
    sys.exit(0)


try:
    nb = json.load(open(nb_path, "r", encoding="utf-8"))
except Exception as exc:
    die("BAD_NOTEBOOK", "could not parse .ipynb as JSON: %r" % (exc,))
cells = nb.get("cells")
if not isinstance(cells, list):
    die("BAD_NOTEBOOK", "no 'cells' list in notebook")


def clean_source(src):
    """Comment out IPython magics and help syntax so a cell still compiles."""
    if isinstance(src, list):
        src = "".join(src)
    out = []
    for line in src.split("\n"):
        s = line.lstrip()
        if s.startswith(("%", "!", "?")) or (
                s.endswith("?") and not s.endswith("??") and s[:-1]
                and s[:-1].replace(".", "").replace("_", "").isalnum()):
            out.append("# [batch_grade: notebook magic removed] " + line)
        else:
            out.append(line)
    return "\n".join(out)


code_cells = []
for i, c in enumerate(cells):
    if c.get("cell_type") != "code":
        continue
    if "autograde-skip" in ((c.get("metadata") or {}).get("tags") or []):
        continue
    body = clean_source(c.get("source", ""))
    if body.strip():
        code_cells.append((i, body))
R["cells_total"] = len(code_cells)

ns = {"__name__": "__main__", "__file__": os.path.abspath(nb_path)}
PREAMBLE = ("try:\n"
            "    import matplotlib\n"
            "    matplotlib.use('Agg')\n"
            "    import matplotlib.pyplot as _plt\n"
            "    _plt.show = lambda *a, **k: None\n"
            "except Exception:\n"
            "    pass\n")
try:
    exec(compile(PREAMBLE, "<preamble>", "exec"), ns)
except Exception:
    pass

HAVE_ALARM = hasattr(signal, "SIGALRM")


class CellTimeout(Exception):
    pass


if HAVE_ALARM:
    signal.signal(signal.SIGALRM,
                  lambda s, f: (_ for _ in ()).throw(
                      CellTimeout("cell exceeded %ds" % per_cell)))


def offending_line(exc, tag, body):
    """The actual source line that blew up, dug out of the traceback."""
    lines, lineno, tb = body.split("\n"), None, exc.__traceback__
    while tb is not None:
        if tb.tb_frame.f_code.co_filename == tag:
            lineno = tb.tb_lineno
        tb = tb.tb_next
    if lineno is None and isinstance(exc, SyntaxError) and exc.lineno:
        lineno = exc.lineno
    if lineno and 1 <= lineno <= len(lines):
        return lineno, lines[lineno - 1].strip()[:200]
    return lineno, ""


captured, real_stdout = io.StringIO(), sys.stdout
for code_no, (idx, body) in enumerate(code_cells, 1):
    tag = "<cell %d>" % (idx + 1)
    sys.stdout = captured
    if HAVE_ALARM:
        signal.alarm(per_cell)
    try:
        exec(compile(body, tag, "exec"), ns)
        R["cells_ok"] += 1
    except CellTimeout as exc:
        R["cell_errors"].append({"cell": idx + 1, "code_cell": code_no,
                                 "etype": "CellTimeout", "emsg": str(exc),
                                 "src": body.strip().split("\n")[0][:200]})
    except SystemExit:
        R["cells_ok"] += 1
    except BaseException as exc:
        lineno, src = offending_line(exc, tag, body)
        R["cell_errors"].append({
            "cell": idx + 1, "code_cell": code_no,
            "etype": type(exc).__name__, "emsg": str(exc)[:400],
            "line": lineno, "src": src,
            "tb": "\n".join(traceback.format_exc().strip().split("\n")[-3:])})
    finally:
        if HAVE_ALARM:
            signal.alarm(0)
        sys.stdout = real_stdout
if R["cell_errors"] and R["status"] == "OK":
    R["status"] = "ERRORS"
R["stdout_tail"] = captured.getvalue()[-2000:]

# ---- run every check, visible and hidden ---------------------------------- #
try:
    spec = ig.load_spec(assignment, spec_path, include_hidden=True,
                        hidden_path=hidden_path)
except Exception as exc:
    die("BAD_SPEC", "could not load test spec: %r" % (exc,))

# The cohort in the notebook wins, because that is what the student was set.
# Google Forms renames an uploaded file to "<original> - <Responder Name>",
# so the file name is not a reliable student id. Record what the notebook
# itself says, and let batch_grade.py reconcile the two.
R["declared_sid"] = (str(ns.get("STUDENT_ID")).strip().upper()
                     if isinstance(ns.get("STUDENT_ID"), str) else "")
nb_cohort = ns.get("COHORT") if isinstance(ns.get("COHORT"), str) else ""
use_cohort = nb_cohort or cohort or getattr(spec, "DEFAULT_COHORT", "")
R["cohort"] = use_cohort
questions = ig.resolve_questions(spec, use_cohort)
for qid, q in questions:
    res = ig.run_check(qid, q, ns)
    R["questions"][qid] = {"ok": res.ok, "awarded": res.awarded,
                           "marks": res.marks, "msg": res.message,
                           "visible": bool(q.get("visible", True)),
                           "err": res.error}
try:
    R["fingerprint"] = ig.answer_fingerprint(questions, ns)
except Exception as exc:
    R["fingerprint"] = ""
    R["cell_errors"].append({"cell": -1, "etype": "FINGERPRINT",
                             "emsg": str(exc)[:200]})

json.dump(R, open(out_path, "w"))
'''


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #

def student_id_from_name(path):
    """Student id from the file name, or "" if the name does not contain one."""
    base = os.path.basename(path)
    m = SID_RE.search(base)
    if m:
        return m.group(1).replace(" ", "").upper()
    return ""


def fallback_id_from_name(path):
    base = os.path.splitext(os.path.basename(path))[0]
    return base.strip().upper()[:24] or "UNKNOWN"


def find_notebooks(folder):
    out = []
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d not in (".ipynb_checkpoints",
                                                "__pycache__")]
        for f in sorted(files):
            if f.endswith(".ipynb") and not f.startswith("."):
                out.append(os.path.join(root, f))
    return out


def grade_one(nb_path, spec_path, hidden_path, assignment, cohort, data_dir,
              per_cell, total_timeout, runner_path):
    """Grade one notebook in a subprocess and a scratch directory."""
    name_sid = student_id_from_name(nb_path)
    sid = name_sid or fallback_id_from_name(nb_path)
    work = tempfile.mkdtemp(prefix="bg_%s_" % re.sub(r"\W", "", sid)[:16])
    record = {"student_id": sid, "notebook": nb_path, "status": "OK",
              "questions": {}, "fingerprint": "", "cell_errors": [],
              "cells_total": 0, "cells_ok": 0, "cohort": cohort,
              "seconds": 0.0, "stdout_tail": "", "declared_sid": "",
              "id_source": "filename" if name_sid else "filename (no S-number)"}
    t0 = time.time()
    try:
        # Data files are copied in so a notebook that says
        # pd.read_csv("campus_energy.csv") works without editing.
        if data_dir and os.path.isdir(data_dir):
            for f in os.listdir(data_dir):
                src = os.path.join(data_dir, f)
                if os.path.isfile(src):
                    shutil.copy2(src, os.path.join(work, f))
                    sub = os.path.join(work, "data")
                    os.makedirs(sub, exist_ok=True)
                    shutil.copy2(src, os.path.join(sub, f))
        # The submitted notebook contains its own setup cell, which looks for
        # iuea_grader.py, the spec and the data next to itself. If it cannot
        # find them it stops early and every later cell fails on a name that
        # was never defined. So the sandbox is made to look like the student's
        # own folder: grader, spec and data all present.
        shutil.copy2(os.path.join(HERE, "iuea_grader.py"),
                     os.path.join(work, "iuea_grader.py"))
        spec_sub = os.path.join(work, "specs")
        os.makedirs(spec_sub, exist_ok=True)
        shutil.copy2(spec_path, os.path.join(spec_sub,
                                             os.path.basename(spec_path)))
        nb_local = os.path.join(work, "submission.ipynb")
        shutil.copy2(nb_path, nb_local)
        out_json = os.path.join(work, "result.json")
        cmd = [sys.executable, runner_path, nb_local, spec_path,
               hidden_path or "", assignment, cohort or "", out_json,
               str(per_cell)]
        env = dict(os.environ)
        env["IUEA_SPEC_DIR"] = spec_sub
        env["MPLBACKEND"] = "Agg"
        try:
            subprocess.run(cmd, cwd=work, timeout=total_timeout,
                           env=env,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.PIPE)
        except subprocess.TimeoutExpired:
            record["status"] = "TIMEOUT"
            record["seconds"] = round(time.time() - t0, 2)
            return record
        if not os.path.isfile(out_json):
            record["status"] = "RUNNER_DIED"
            record["seconds"] = round(time.time() - t0, 2)
            return record
        with open(out_json) as fh:
            record.update(json.load(fh))
        record["notebook"] = nb_path
        declared = record.get("declared_sid") or ""
        # The file name wins when it carries a student number, because the
        # notebook's STUDENT_ID is whatever the student typed. When the file
        # name has no student number in it - which is what a Google Forms
        # upload looks like - the notebook is all there is.
        if name_sid:
            record["student_id"] = name_sid
            if declared and declared != name_sid:
                record["id_source"] = "filename, notebook disagrees (%s)" % declared
        elif declared:
            record["student_id"] = declared
            record["id_source"] = "notebook STUDENT_ID"
        else:
            record["student_id"] = sid
            record["id_source"] = "file name, no id found anywhere"
    except Exception as exc:                           # noqa: BLE001
        record["status"] = "HARNESS_ERROR"
        record["cell_errors"] = [{"cell": -1, "etype": type(exc).__name__,
                                  "emsg": str(exc)[:300]}]
    finally:
        shutil.rmtree(work, ignore_errors=True)
    record["seconds"] = round(time.time() - t0, 2)
    return record


def read_token_csv(path):
    """Pull tokens out of a Google Forms CSV export.

    Forms puts a header row on it, with column names taken from the question
    text. Any cell that looks like a token is accepted, so the column can be
    called anything and the sheet can be reordered.
    """
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        sample = fh.read(8192)
        fh.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except Exception:                              # noqa: BLE001
            dialect = csv.excel
        for r in csv.reader(fh, dialect):
            rows.append(r)
    if not rows:
        return []
    out = []
    for i, r in enumerate(rows):
        tok = ""
        for cell in r:
            c = (cell or "").strip()
            if c.upper().startswith(ig.TOKEN_PREFIX + "-"):
                tok = c
                break
        if not tok:
            if i == 0:
                continue                               # header row
            # A row with no token at all is still worth reporting.
            joined = " | ".join((c or "").strip() for c in r)[:80]
            if joined.strip(" |"):
                out.append({"row": i + 1, "token": "", "raw": joined})
            continue
        out.append({"row": i + 1, "token": tok,
                    "raw": " | ".join((c or "").strip() for c in r)[:120]})
    return out


# --------------------------------------------------------------------------- #
# feedback file
# --------------------------------------------------------------------------- #

def write_feedback(folder, rec, assignment, title, token_info):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "%s.txt" % re.sub(r"\W", "_",
                                                  rec["student_id"]))
    L = []
    rule = "-" * 68
    L.append(rule)
    L.append("%s  %s" % (assignment, title))
    L.append("Student: %s" % rec["student_id"])
    if rec.get("cohort"):
        L.append("Cohort:  %s" % rec["cohort"])
    L.append(rule)
    qs = rec.get("questions") or {}
    got = sum(q.get("awarded", 0) for q in qs.values())
    avail = sum(q.get("marks", 0) for q in qs.values())
    if rec["status"] == "TIMEOUT":
        L.append("")
        L.append("Your notebook did not finish running inside the time limit,")
        L.append("so it could not be graded automatically. Usually this is a")
        L.append("loop that never ends. Come and see me.")
    elif rec["status"] in ("BAD_NOTEBOOK", "RUNNER_DIED", "HARNESS_ERROR"):
        L.append("")
        L.append("Your file could not be opened as a notebook, so it could")
        L.append("not be graded. Check you uploaded the .ipynb and not a")
        L.append("screenshot, a PDF, or a zip. Come and see me.")
    for qid in sorted(qs):
        q = qs[qid]
        mark = "PASS" if q.get("ok") else "FAIL"
        if 0 < q.get("awarded", 0) < q.get("marks", 0):
            mark = "PART"
        L.append("")
        L.append("[%s] %-4s %s / %s marks%s" % (
            mark, qid, ig._fmt_marks(q.get("awarded", 0)),
            ig._fmt_marks(q.get("marks", 0)),
            "" if q.get("visible") else "   (graded after submission)"))
        if not q.get("ok") and q.get("msg"):
            for line in ig._wrap(q["msg"], 64):
                L.append("       %s" % line)
    L.append("")
    L.append(rule)
    L.append("TOTAL  %s / %s" % (ig._fmt_marks(got), ig._fmt_marks(avail)))
    L.append(rule)
    errs = rec.get("cell_errors") or []
    if errs:
        L.append("")
        L.append("Cells that raised an error when I ran your notebook from a")
        L.append("clean start. Marks above are what survived. Run")
        L.append("Runtime > Restart and run all before you submit, every time:")
        for e in errs[:8]:
            L.append("  cell %s: %s: %s" % (e.get("cell"), e.get("etype"),
                                            (e.get("emsg") or "")[:150]))
            if e.get("src"):
                L.append("      %s" % e["src"][:80])
    if token_info is not None:
        L.append("")
        L.append(rule)
        L.append("Submission code")
        if not token_info.get("present"):
            L.append("  No code was found for you in the Form responses.")
        elif not token_info.get("verified"):
            L.append("  Your code did not verify: %s"
                     % token_info.get("reason", ""))
            L.append("  Most often this is a partial paste. Re-run the submit")
            L.append("  cell and paste the whole line.")
        else:
            L.append("  Verified. Submitted %s." % token_info.get("time_utc"))
            if token_info.get("mismatch"):
                L.append("  NOTE: the code claims %s visible marks and your"
                         % ig._fmt_marks(token_info.get("claimed", 0)))
                L.append("  notebook scores %s on the same questions. I mark"
                         % ig._fmt_marks(token_info.get("actual", 0)))
                L.append("  the notebook. Come and see me if that surprises you.")
    L.append("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
    return path


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #

def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Grade a week's notebooks and verify the Form tokens.")
    ap.add_argument("--assignment", "-a", required=True,
                    help="assignment id, e.g. W05")
    ap.add_argument("--spec", default=None,
                    help="path to spec_<A>.py (default: search for it)")
    ap.add_argument("--hidden-spec", default=None,
                    help="path to spec_<A>_hidden.py (default: search "
                         "specs/hidden/ for it)")
    ap.add_argument("--notebooks", "-n", default=None,
                    help="folder of submitted .ipynb files")
    ap.add_argument("--tokens", "-t", default=None,
                    help="CSV exported from the Google Form")
    ap.add_argument("--data-dir", default=None,
                    help="folder of data files to place beside each notebook")
    ap.add_argument("--out", "-o", default="results",
                    help="output folder (default: results)")
    ap.add_argument("--cohort", default="",
                    help="cohort for per-cohort specs; the notebook's own "
                         "COHORT variable overrides this")
    ap.add_argument("--sample", type=float, default=None, metavar="N",
                    help="grade only a random N%% of the notebooks and compare "
                         "them against the token-claimed scores")
    ap.add_argument("--seed", type=int, default=None,
                    help="random seed, so a sample can be reproduced")
    ap.add_argument("--cell-timeout", type=int, default=20,
                    help="seconds per cell (Unix only, default 20)")
    ap.add_argument("--notebook-timeout", type=int, default=120,
                    help="seconds per notebook (default 120)")
    ap.add_argument("--jobs", "-j", type=int, default=0,
                    help="parallel notebooks (default: cpu count, max 8)")
    args = ap.parse_args(argv)

    assignment = args.assignment.strip().upper()
    if not args.notebooks and not args.tokens:
        print("Nothing to do: give --notebooks, --tokens, or both.")
        return 2

    spec_path = ig.find_spec_file(assignment, args.spec)
    if spec_path is None:
        print("Cannot find spec_%s.py. Pass --spec explicitly." % assignment)
        return 2
    hidden_path = ig.find_hidden_spec_file(assignment, args.hidden_spec)
    try:
        spec = ig.load_spec(assignment, spec_path, include_hidden=True,
                            hidden_path=hidden_path)
    except Exception as exc:                           # noqa: BLE001
        print("spec_%s.py will not import: %s" % (assignment, exc))
        return 2
    no_check = [qid for qid, q in ig.resolve_questions(spec, args.cohort)
                if not callable(q.get("check"))]
    if no_check:
        print("WARNING: %s have no check function. They will score zero for "
              "everybody." % ", ".join(no_check))
        print("         The hidden spec is probably missing. Looked for "
              "spec_%s_hidden.py." % assignment)
    title = getattr(spec, "TITLE", assignment)
    all_q = [qid for qid, _ in ig.resolve_questions(spec, args.cohort)]
    vis_q = [qid for qid, q in ig.resolve_questions(spec, args.cohort)
             if q.get("visible", True)]

    os.makedirs(args.out, exist_ok=True)
    runner_path = os.path.join(HERE, RUNNER_NAME)
    with open(runner_path, "w", encoding="utf-8") as fh:
        fh.write(RUNNER_SOURCE)

    # ---- tokens ---------------------------------------------------------- #
    tokens = {}
    token_rows, dup_tokens, unverified = [], [], []
    if args.tokens:
        token_rows = read_token_csv(args.tokens)
        for row in token_rows:
            if not row["token"]:
                unverified.append((row["row"], "", "no code in this row"))
                continue
            info = ig.verify_token(row["token"])
            if not info["ok"]:
                unverified.append((row["row"], row["token"][:40],
                                   info["reason"]))
                continue
            if info["assignment"] != assignment:
                unverified.append((row["row"], info["student_id"],
                                   "code is for %s, not %s"
                                   % (info["assignment"], assignment)))
                continue
            sid = info["student_id"]
            prev = tokens.get(sid)
            if prev:
                dup_tokens.append(sid)
                # keep the latest, which is the resubmission
                if info["timestamp"] < prev["timestamp"]:
                    continue
            info["row"] = row["row"]
            tokens[sid] = info

    # ---- notebooks ------------------------------------------------------- #
    nbs, sampled, all_nbs = [], False, []
    if args.notebooks:
        all_nbs = find_notebooks(args.notebooks)
        nbs = list(all_nbs)
        if args.sample is not None:
            pct = max(0.0, min(100.0, args.sample))
            k = max(1, int(round(len(all_nbs) * pct / 100.0))) if all_nbs else 0
            rng = random.Random(args.seed)
            nbs = rng.sample(all_nbs, min(k, len(all_nbs)))
            sampled = True

    t0 = time.time()
    records = []
    if nbs:
        jobs = args.jobs or min(8, (os.cpu_count() or 2))
        print("Grading %d notebook%s against %d tests (%d visible, %d hidden)"
              % (len(nbs), "" if len(nbs) == 1 else "s", len(all_q),
                 len(vis_q), len(all_q) - len(vis_q)))
        print("  spec:   %s" % spec_path)
        print("  hidden: %s" % (hidden_path or "NONE FOUND"))
        print("  jobs:   %d" % jobs)
        if sampled:
            print("  SAMPLE: %.0f%% of %d submissions, seed %s"
                  % (args.sample, len(all_nbs), args.seed))
        with ThreadPoolExecutor(max_workers=jobs) as pool:
            futs = {pool.submit(grade_one, nb, spec_path, hidden_path,
                                assignment, args.cohort, args.data_dir,
                                args.cell_timeout, args.notebook_timeout,
                                runner_path): nb
                    for nb in nbs}
            done = 0
            for fut in as_completed(futs):
                records.append(fut.result())
                done += 1
                if done % 25 == 0 or done == len(nbs):
                    sys.stdout.write("\r  graded %d/%d" % (done, len(nbs)))
                    sys.stdout.flush()
        print("")
    elapsed = time.time() - t0
    records.sort(key=lambda r: r["student_id"])

    # ---- compare notebooks with tokens ----------------------------------- #
    discrepancies = []
    fp_mismatch = []
    by_sid = {r["student_id"]: r for r in records}
    for sid, rec in by_sid.items():
        info = tokens.get(sid)
        if not info:
            continue
        actual = sum(rec["questions"].get(q, {}).get("awarded", 0.0)
                     for q in info["scores"])
        claimed = info["claimed_total"]
        if abs(actual - claimed) > 1e-6:
            discrepancies.append({
                "student_id": sid, "claimed": claimed, "actual": actual,
                "delta": round(claimed - actual, 4),
                "per_q": {q: (info["scores"][q],
                              rec["questions"].get(q, {}).get("awarded", 0.0))
                          for q in info["scores"]},
            })
        if info["fingerprint"] and rec.get("fingerprint") and \
                info["fingerprint"] != rec["fingerprint"]:
            fp_mismatch.append(sid)

    # ---- results.csv ----------------------------------------------------- #
    csv_path = os.path.join(args.out, "results.csv")
    fields = (["student_id", "id_source", "cohort", "status", "notebook"]
              + ["%s_marks" % q for q in all_q]
              + ["notebook_total", "max_total", "visible_total",
                 "token_present", "token_verified", "token_reason",
                 "token_claimed_visible", "token_time_utc",
                 "answer_hash_match", "score_discrepancy",
                 "cells_total", "cells_ok", "n_cell_errors", "seconds"])
    seen_sids = set()
    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for rec in records:
            sid = rec["student_id"]
            seen_sids.add(sid)
            qs = rec.get("questions") or {}
            info = tokens.get(sid)
            row = {"student_id": sid,
                   "id_source": rec.get("id_source", ""),
                   "cohort": rec.get("cohort", ""),
                   "status": rec["status"], "notebook": rec["notebook"],
                   "cells_total": rec.get("cells_total", 0),
                   "cells_ok": rec.get("cells_ok", 0),
                   "n_cell_errors": len(rec.get("cell_errors") or []),
                   "seconds": rec.get("seconds", 0)}
            for q in all_q:
                row["%s_marks" % q] = ig._fmt_marks(qs.get(q, {})
                                                    .get("awarded", 0))
            row["notebook_total"] = ig._fmt_marks(
                sum(q.get("awarded", 0) for q in qs.values()))
            row["max_total"] = ig._fmt_marks(
                sum(q.get("marks", 0) for q in qs.values()))
            row["visible_total"] = ig._fmt_marks(
                sum(qs.get(q, {}).get("awarded", 0) for q in vis_q))
            row["token_present"] = "yes" if info else "no"
            row["token_verified"] = "yes" if info else ""
            row["token_reason"] = "" if info else ""
            row["token_claimed_visible"] = (
                ig._fmt_marks(info["claimed_total"]) if info else "")
            row["token_time_utc"] = info["time_utc"] if info else ""
            if info and info["fingerprint"] and rec.get("fingerprint"):
                row["answer_hash_match"] = (
                    "yes" if info["fingerprint"] == rec["fingerprint"] else "NO")
            else:
                row["answer_hash_match"] = ""
            d = [x for x in discrepancies if x["student_id"] == sid]
            row["score_discrepancy"] = ig._fmt_marks(d[0]["delta"]) if d else ""
            w.writerow(row)
        # tokens with no notebook: still record them
        for sid, info in sorted(tokens.items()):
            if sid in seen_sids:
                continue
            row = {f: "" for f in fields}
            row.update({"student_id": sid, "cohort": info.get("cohort", ""),
                        "status": "NO_NOTEBOOK" if args.notebooks else "TOKEN_ONLY",
                        "token_present": "yes", "token_verified": "yes",
                        "token_claimed_visible":
                            ig._fmt_marks(info["claimed_total"]),
                        "token_time_utc": info["time_utc"]})
            for q in all_q:
                row["%s_marks" % q] = ""
            w.writerow(row)

    # ---- feedback files -------------------------------------------------- #
    fb_dir = os.path.join(args.out, "feedback")
    for rec in records:
        info = tokens.get(rec["student_id"])
        d = [x for x in discrepancies if x["student_id"] == rec["student_id"]]
        ti = None
        if args.tokens:
            ti = {"present": bool(info), "verified": bool(info),
                  "reason": "", "time_utc": info["time_utc"] if info else "",
                  "mismatch": bool(d),
                  "claimed": info["claimed_total"] if info else 0,
                  "actual": (sum(rec["questions"].get(q, {}).get("awarded", 0)
                                 for q in info["scores"]) if info else 0)}
            if not info:
                for r, who, why in unverified:
                    if who and who.upper() == rec["student_id"]:
                        ti.update({"present": True, "verified": False,
                                   "reason": why})
        write_feedback(fb_dir, rec, assignment, title, ti)

    # ---- summary --------------------------------------------------------- #
    S = []

    def say(line=""):
        S.append(line)
        print(line)

    n = len(records)
    status_counts = {}
    for r in records:
        status_counts[r["status"]] = status_counts.get(r["status"], 0) + 1
    say("")
    say("=" * 68)
    say("  %s  %s" % (assignment, title))
    say("=" * 68)
    if args.notebooks:
        say("  notebooks found        %d" % len(all_nbs))
        say("  notebooks graded       %d%s"
            % (n, "  (sample)" if sampled else ""))
        say("  clean, no cell errors  %d" % status_counts.get("OK", 0))
        say("  ran with cell errors   %d" % status_counts.get("ERRORS", 0))
        say("  timed out              %d" % status_counts.get("TIMEOUT", 0))
        say("  unreadable file        %d" % (status_counts.get("BAD_NOTEBOOK", 0)
                                             + status_counts.get("RUNNER_DIED", 0)
                                             + status_counts.get("HARNESS_ERROR", 0)))
        if n:
            tot = [sum(q.get("awarded", 0) for q in r["questions"].values())
                   for r in records]
            mx = max((sum(q.get("marks", 0) for q in r["questions"].values())
                      for r in records), default=0)
            say("  mean mark              %.1f / %s"
                % (sum(tot) / float(n), ig._fmt_marks(mx)))
            say("  wall clock             %.1fs  (%.2fs per notebook)"
                % (elapsed, elapsed / n))
    if args.notebooks:
        odd = [r["student_id"] for r in records
               if "disagree" in r.get("id_source", "")
               or "no id found" in r.get("id_source", "")]
        if odd:
            say("  student id in doubt    %d  %s"
                % (len(odd), ", ".join(odd[:8])))
    if args.tokens:
        say("  form rows read         %d" % len(token_rows))
        say("  tokens verified        %d" % len(tokens))
        say("  tokens UNVERIFIED      %d" % len(unverified))
        if dup_tokens:
            say("  students with >1 code  %d  (latest kept)"
                % len(set(dup_tokens)))
        for row, who, why in unverified[:15]:
            say("      row %-4s %-10s %s" % (row, who or "-", why))
        if len(unverified) > 15:
            say("      ... and %d more, see results.csv"
                % (len(unverified) - 15))
    if args.notebooks and args.tokens:
        no_nb = sorted(set(tokens) - seen_sids)
        no_tok = sorted(seen_sids - set(tokens))
        if sampled:
            say("  codes not in this sample %d  (not graded, not a problem)"
                % len(no_nb))
        else:
            say("  code but no notebook   %d%s"
                % (len(no_nb), ("  " + ", ".join(no_nb[:8])) if no_nb else ""))
        say("  notebook but no code   %d%s"
            % (len(no_tok), ("  " + ", ".join(no_tok[:8])) if no_tok else ""))
        say("  answer-hash mismatch   %d%s"
            % (len(fp_mismatch),
               ("  " + ", ".join(fp_mismatch[:8])) if fp_mismatch else ""))
        say("")
        if discrepancies:
            say("  SCORE DISCREPANCIES   %d of %d compared"
                % (len(discrepancies), len([r for r in records
                                            if r["student_id"] in tokens])))
            say("  " + "-" * 66)
            for d in sorted(discrepancies, key=lambda x: -abs(x["delta"])):
                say("  %-10s code claims %-5s notebook scores %-5s  delta %+g"
                    % (d["student_id"], ig._fmt_marks(d["claimed"]),
                       ig._fmt_marks(d["actual"]), d["delta"]))
                for q, (c, a) in sorted(d["per_q"].items()):
                    if abs(c - a) > 1e-6:
                        say("               %s: code %s, notebook %s"
                            % (q, ig._fmt_marks(c), ig._fmt_marks(a)))
            say("  " + "-" * 66)
            say("  The notebook mark is the mark. A positive delta means the")
            say("  code claimed more than the notebook earns.")
        else:
            say("  score discrepancies    0  (every compared code matches its"
                " notebook)")
    say("=" * 68)
    say("  results:  %s" % csv_path)
    if records:
        say("  feedback: %s/  (%d files)" % (fb_dir, len(records)))
    say("=" * 68)
    with open(os.path.join(args.out, "summary.txt"), "w",
              encoding="utf-8") as fh:
        fh.write("\n".join(S) + "\n")

    if unverified or discrepancies:
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\ninterrupted")
        sys.exit(130)
