#!/usr/bin/env python3
"""batch_grade.py - the lecturer's weekly command. Supersedes autograde.py.

Requires Docker and pandas. Student code runs without network access; trusted checks run outside its container.

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

Student Registration Number is recovered from the safe notebook filename:
    99_TEST_000_DEMO-X_W02.ipynb -> 99/TEST/000/DEMO-X
Legacy S-number filenames remain readable for existing internal fixtures.
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

from registration import registration_from_filename, normalize

import iuea_grader as ig                                            # noqa: E402

SID_RE = re.compile(r"(S\s?\d{4,8})", re.I)
RUNNER_NAME = "_run_one_notebook.py"


# --------------------------------------------------------------------------- #
# the subprocess runner, written out next to this file at run time
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #

def student_id_from_name(path):
    """Student id from the file name, or "" if the name does not contain one."""
    base = os.path.basename(path)
    registration = registration_from_filename(base)
    if registration:
        return registration
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
        from isolated_grading import evaluate
        # Docker runs as an unprivileged user; expose only copied practice files.
        os.chmod(work, 0o755)
        for root, dirs, files in os.walk(work):
            for d in dirs:
                os.chmod(os.path.join(root, d), 0o755)
            for f in files:
                os.chmod(os.path.join(root, f), 0o644)
        record.update(evaluate(work, spec_path, hidden_path, assignment, cohort,
                               per_cell, total_timeout))
        record["notebook"] = nb_path
        declared = normalize(record.get("declared_sid") or "")
        # The file name wins when it carries a student number, because the
        # notebook's STUDENT_ID is whatever the student typed. When the file
        # name has no student number in it - which is what a Google Forms
        # upload looks like - the notebook is all there is.
        if name_sid:
            record["student_id"] = name_sid
            if declared and declared != name_sid:
                record["id_source"] = "filename, notebook disagrees (%s)" % declared
                record["status"] = "IDENTITY_MISMATCH"
        elif declared:
            record["student_id"] = declared
            record["id_source"] = "notebook STUDENT_ID"
        else:
            record["student_id"] = sid
            record["id_source"] = "file name, no id found anywhere"
    except TimeoutError:
        record["status"] = "TIMEOUT"
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
                    help="authoritative cohort; a conflicting notebook declaration is rejected")
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
        print("REFUSING TO GRADE: missing checks: %s" % ", ".join(no_check))
        print("         The hidden spec is probably missing. Looked for "
              "spec_%s_hidden.py." % assignment)
        return 2
    if args.notebooks:
        from isolated_grading import preflight
        try:
            preflight()
        except Exception as exc:
            print("PREFLIGHT FAILED:", exc)
            return 2
    title = getattr(spec, "TITLE", assignment)
    all_q = [qid for qid, _ in ig.resolve_questions(spec, args.cohort)]
    vis_q = [qid for qid, q in ig.resolve_questions(spec, args.cohort)
             if q.get("visible", True)]

    os.makedirs(args.out, exist_ok=True)
    runner_path = os.path.join(HERE, RUNNER_NAME)

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
        groups = {}
        for nb in all_nbs:
            sid = student_id_from_name(nb)
            if not sid:
                print("Submission filename needs a roster student registration number:", nb)
                return 2
            groups.setdefault(sid, []).append(nb)
        duplicates = {sid: paths for sid, paths in groups.items() if len(paths) > 1}
        if duplicates:
            print("Duplicate submissions: select the latest on-time upload using the submission manifest before grading.")
            print(json.dumps(duplicates, indent=2))
            return 2
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

    if unverified or discrepancies or any(r["status"] not in ("OK", "ERRORS") for r in records):
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\ninterrupted")
        sys.exit(130)
