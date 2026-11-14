"""Supplied pieces of the marked notebook for the collection design of 14 November 2026 (no Submit step).

  backup_code()  appended to the supplied setup cell. Inside Colab only, it starts a background thread that, at once and then every
                 5 minutes, sends the notebook ON SCREEN (google.colab _message 'get_ipynb') and the address of the open file
                 (output.eval_js('location.href')) to the collector through the gateway, with the allocation code the entry page put in
                 the identity cell. The data block of the setup cell is left out of each backup (the grader puts it back). If the server
                 says the open file is not the issued one, a warning appears at the top of the setup cell's output. Anywhere else (the
                 grader, the Check my notebook process) it does nothing.
  check_cell()   "Check my notebook": optional self-help. Runs the student's code cells again from the top in a FRESH Python process
                 (the grader's time limits), lists every cell that fails, confirms the required functions and the MEMO form, and runs the
                 public self-checks. It never shows a hidden result or a mark.
  attempt_cell() the last cell: information only (how saving and collection work). The entry page adds the allocation lines to it.

The required names come from project_contracts.NAMES and the memo fields from the MEMO form in project_content, so a change to
the task list needs only a rebuild. There is no token and no deadline logic in the notebook: the server keeps the deadline.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "grader_spec"))
ROOT = HERE.parents[3]

CHECK_MARKER = '# IUEA-CHECK-CELL'
SUBMIT_MARKER = '# IUEA-SUBMIT-CELL'
CHECK_TITLE = '#@title Check my notebook - Do not edit this cell'
CELL_TIMEOUT, TOTAL_TIMEOUT = 30, 300          # the same limits as grade_project.py (--cell-timeout 30, --notebook-timeout 300)


def public_url():
    """The Cloudflare entry host (data/test_portal_config.json), the same host as the entry links."""
    config = json.loads((ROOT / 'data/test_portal_config.json').read_text())
    return config['public_url'].rstrip('/')


def required_functions():
    import project_contracts as K
    return list(dict.fromkeys(K.NAMES.values()))


def memo_fields():
    import project_content as PC
    return re.findall(r'^\s+"(\w+)":', PC.MEMO_STARTER, re.M)


# Cells the check never runs: the timer, the submit cell, this cell and the self-checks (they run at the end, on purpose).
SKIP_MARKERS = ['#@title Check details and countdown', 'Submit your test', 'Submit your project', CHECK_MARKER, SUBMIT_MARKER, '# IUEA-ATTEMPT-CELL',
                '# This cell is a SELF-CHECK', '# MEMO SELF-CHECK']
SELF_CHECK_MARKERS = ['# This cell is a SELF-CHECK', '# MEMO SELF-CHECK']

RUNNER = r'''
import builtins, contextlib, io, json, signal, sys, traceback, warnings
warnings.filterwarnings("ignore")
nb = json.load(open(sys.argv[1]))
skip, selfchecks, needed, memo_fields, cell_limit = json.loads(sys.argv[2])
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
try:
    from IPython.display import display as _display
except Exception:
    def _display(*a, **k):
        for x in a:
            print(x)
builtins.display = _display
class Slow(Exception):
    pass
def alarm(*_):
    raise Slow("took more than %d seconds" % cell_limit)
signal.signal(signal.SIGALRM, alarm)
ns = {"__name__": "__main__"}
report = {"cells": 0, "failed": [], "selfchecks": []}
number = 0
for cell in nb.get("cells", []):
    if cell.get("cell_type") != "code":
        continue
    number += 1
    src = cell.get("source", "")
    src = "".join(src) if isinstance(src, list) else str(src)
    tags = cell.get("metadata", {}).get("tags", [])
    if any(m in src for m in skip) or "autograde-skip" in tags:
        if any(m in src for m in selfchecks):
            report["selfchecks"].append(src)
        continue
    src = "\n".join("# notebook command left out" if l.lstrip().startswith(("%", "!")) else l for l in src.splitlines())
    if not src.strip():
        continue
    report["cells"] += 1
    signal.alarm(cell_limit)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src, "<code cell %d>" % number, "exec"), ns)
    except BaseException as error:
        line = ""
        for frame in traceback.extract_tb(error.__traceback__):
            if frame.filename == "<code cell %d>" % number:
                line = " (line %d)" % frame.lineno
        report["failed"].append({"cell": number, "first_line": src.strip().splitlines()[0][:80], "error": type(error).__name__ + line + ": " + str(error)[:200]})
    finally:
        signal.alarm(0)
        plt.close("all")
report["missing_functions"] = [n for n in needed if not callable(ns.get(n))]
memo = ns.get("MEMO")
report["memo_found"] = isinstance(memo, dict)
report["memo_missing_fields"] = [f for f in memo_fields if not isinstance(memo, dict) or f not in memo]
outputs = []
for src in report.pop("selfchecks"):
    buffer = io.StringIO()
    signal.alarm(cell_limit * 2)
    try:
        with contextlib.redirect_stdout(buffer):
            exec(compile(src, "<self-check>", "exec"), ns)
    except BaseException as error:
        buffer.write("The self-check stopped: " + type(error).__name__ + "\n")
    finally:
        signal.alarm(0)
    outputs.append(buffer.getvalue())
report["selfcheck_output"] = outputs
print("IUEA-REPORT " + json.dumps(report))
'''


def check_cell():
    names, fields = required_functions(), memo_fields()
    args = json.dumps([SKIP_MARKERS, SELF_CHECK_MARKERS, names, fields, CELL_TIMEOUT])
    return f'''{CHECK_TITLE}
{CHECK_MARKER}  (supplied: do not edit. It is not marked and it never shows a mark.)
# Run it before you submit. Click "Check my notebook". It runs a copy of your code cells again from the top, in a fresh Python, the way the
# marking computer does, and tells you which cell fails, whether every required function and the MEMO form are there, and what the
# self-checks say. Your notebook itself is not changed. It takes one to three minutes.
import json as _ck_json, os as _ck_os, subprocess as _ck_sp, sys as _ck_sys, tempfile as _ck_tmp
import ipywidgets as _ck_w
from IPython.display import display as _ck_display, clear_output as _ck_clear
_CK_RUNNER = {RUNNER!r}
_CK_ARGS = {args!r}

def _ck_notebook():
    from google.colab import _message
    return _message.blocking_request("get_ipynb", timeout_sec=60)["ipynb"]

def _ck_run(_):
    _ck_button.disabled = True
    with _ck_out:
        _ck_clear()
        try:
            notebook = _ck_notebook()
        except Exception:
            print("Could not read the notebook on your screen. Wait a moment and click the button again.")
            _ck_button.disabled = False
            return
        print("Running your code cells from the top in a fresh Python. Please wait (one to three minutes)...")
        folder = _ck_tmp.mkdtemp(prefix="check_")
        with open(_ck_os.path.join(folder, "notebook.json"), "w") as f:
            _ck_json.dump(notebook, f)
        with open(_ck_os.path.join(folder, "runner.py"), "w") as f:
            f.write(_CK_RUNNER)
        try:
            done = _ck_sp.run([_ck_sys.executable, "runner.py", "notebook.json", _CK_ARGS], cwd=folder, capture_output=True, text=True,
                              timeout={TOTAL_TIMEOUT}, env=dict(_ck_os.environ, MPLBACKEND="Agg"))
            line = [l for l in done.stdout.splitlines() if l.startswith("IUEA-REPORT ")]
            report = _ck_json.loads(line[-1][len("IUEA-REPORT "):]) if line else None
        except _ck_sp.TimeoutExpired:
            report = None
            print("Your notebook took more than {TOTAL_TIMEOUT // 60} minutes to run from the top. The marking computer stops at the same limit.")
            print("Look for a loop that runs too long, or a cell that waits for input.")
        _ck_clear()
        if report is None:
            print("The check could not finish. Choose Runtime, Restart session and run all, and look for the first error.")
        else:
            print("Code cells run:", report["cells"])
            if report["failed"]:
                print("These cells stop with an error when the notebook runs from the top. Fix the FIRST one first:")
                for f in report["failed"]:
                    print("  code cell", f["cell"], "starting", repr(f["first_line"]), "->", f["error"])
            else:
                print("Every code cell runs from the top without an error.")
            print("Required functions missing:", ", ".join(report["missing_functions"]) if report["missing_functions"] else "none. All are there.")
            if not report["memo_found"]:
                print("The MEMO form was not found. Run the MEMO cell and keep its name MEMO.")
            elif report["memo_missing_fields"]:
                print("MEMO fields missing:", ", ".join(report["memo_missing_fields"]))
            else:
                print("The MEMO form is there with every field.")
            for text in report["selfcheck_output"]:
                print()
                print(text.strip())
            print()
            print("This check uses only the public self-checks. The marks come from other rows that you cannot see.")
        _ck_button.disabled = False

_ck_button = _ck_w.Button(description="Check my notebook", button_style="info", icon="search")
_ck_out = _ck_w.Output()
_ck_button.on_click(_ck_run)
_ck_display(_ck_button, _ck_out)
'''


PACKED_MARKER = '__IUEA_PACKED_DATA__'
ATTEMPT_MARKER = '# IUEA-ATTEMPT-CELL'
BACKUP_MINUTES = 5


def backup_code(url=None):
    base = (url or public_url()).rstrip('/')
    return f'''
# Automatic backup (supplied). Inside Colab, a copy of the notebook on your screen goes to your lecturer every {BACKUP_MINUTES} minutes.
# You do not need to do anything. Your work is collected automatically at your deadline.
def _iuea_backup_start(address={base + "/api/backup"!r}, minutes={BACKUP_MINUTES}):
    import json, threading, time, urllib.request
    try:
        from IPython import get_ipython
        shell = get_ipython()
        if shell is None or "google.colab" not in type(shell).__module__:
            return                                   # not in Colab (the marking computer, Check my notebook): no backup
        from google.colab import _message, output
        from IPython.display import display, HTML
    except Exception:
        return
    attempt = str(globals().get("_IUEA_ALLOCATION", ""))
    if not attempt:
        print("Backup is off: run the first cell (your details and the countdown) first, then this cell again.")
        return
    old = globals().get("_iuea_backup_thread")
    if old is not None and old.is_alive():
        return
    note = display(HTML(""), display_id=True)
    packed = _PACKED.strip()
    def send():
        notebook = _message.blocking_request("get_ipynb", timeout_sec=60)["ipynb"]
        for cell in notebook.get("cells", []):
            text = "".join(cell.get("source", "")) if isinstance(cell.get("source"), list) else str(cell.get("source", ""))
            if "# IUEA-SETUP-CELL" in text:
                cell["source"] = text.replace(packed, "__IUEA_" + "PACKED_DATA__")
        href = str(output.eval_js("location.href"))[:500]
        body = json.dumps({{"attempt": attempt, "href": href, "notebook": json.dumps(notebook)}}).encode("utf-8")
        request = urllib.request.Request(address, data=body, headers={{"Content-Type": "application/json"}}, method="POST")
        with urllib.request.urlopen(request, timeout=60) as reply:
            return json.loads(reply.read().decode("utf-8"))
    def loop():
        while True:
            try:
                answer = send() or {{}}
                result = answer.get("result") or {{}}
                if result.get("other_file"):
                    note.update(HTML('<div style="border:3px solid #b3261e;background:#fff0ee;padding:10px;font-size:16px;color:#7a1712">'
                                     '<b>You are working in a different file from your issued notebook.</b> Your work here is still backed up. '
                                     'Go back to the entry page and click Resume, or keep working here and tell your lecturer on the class channel.</div>'))
                elif answer.get("ok"):
                    note.update(HTML('<div style="color:#526577;font-size:13px">Automatic backup sent at ' + time.strftime("%H:%M") + '. Your notebook also saves itself; press Ctrl+S now and then.</div>'))
                elif result.get("closed") or "deadline" in str(answer.get("error", "")):
                    note.update(HTML('<div style="color:#526577;font-size:13px">Your time has ended. Your work was collected at your deadline.</div>'))
                    return
            except Exception:
                pass
            time.sleep(minutes * 60)
    thread = threading.Thread(target=loop, name="iuea-backup", daemon=True)
    thread.start()
    globals()["_iuea_backup_thread"] = thread
_iuea_backup_start()
'''


def attempt_cell():
    return f'''#@title How your work is collected - Do not edit this cell
{ATTEMPT_MARKER}  (supplied: information only, nothing to run)
# There is no Submit button. Your notebook saves itself to your Google Drive while you work; press Ctrl+S now and then.
# At your deadline your lecturer's server stops your editing and collects your work: the last version saved before the deadline,
# or the newest automatic backup if that is newer. If you finish early, press "I have finished" on the entry page.
print("Nothing to submit here. Your work is collected automatically at your deadline.")
'''


if __name__ == '__main__':
    compile(check_cell(), 'check', 'exec')
    compile(backup_code('https://example.test'), 'backup', 'exec')
    compile(attempt_cell(), 'attempt', 'exec')
    print('the cells compile;', len(required_functions()), 'functions,', len(memo_fields()), 'memo fields')
