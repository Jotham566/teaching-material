
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
