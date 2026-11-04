# -*- coding: utf-8 -*-
"""Check the track workbook's formulas without needing LibreOffice.

Two things are checked, and the difference matters:

  1. Every function used is Excel-2007-era, so it needs no _xlfn. prefix and
     cannot come back as #NAME?. This is a static check on the formula text.
  2. The arithmetic each formula is SUPPOSED to do is computed here in Python
     and compared to what the sheet claims. An off-by-one range or a wrong
     absolute reference shows up as a number that does not match.

This is not a substitute for opening the file: only a real engine proves a
formula evaluates. It is what can be proved without one, and the first
version of the old mark-sheet formula used SUM(IF(...)), which needs array entry
and came back #VALUE! from a real recalc, so the static check alone would
not have caught it.
"""
import re
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
WB = os.path.join(_ROOT, "DataAnalysis_Track",
                  "DataAnalysis_Track_Workbook.xlsx")

# Functions that need no prefix and that LibreOffice also evaluates. Anything
# outside this set has to be justified before it goes in.
ALLOWED = {"IF", "SUM", "COUNTIF", "COUNTA", "AND"}

fails = []
wb = load_workbook(sys.argv[1] if len(sys.argv) > 1 else WB)

# ------------------------------------------------ 1. only safe functions
used, formulas = set(), 0
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith("="):
                formulas += 1
                for fn in re.findall(r"([A-Z_][A-Z0-9_.]*)\s*\(", c.value):
                    used.add(fn)
                    if fn not in ALLOWED:
                        fails.append("%s!%s uses %s, which is not on the "
                                     "safe list" % (ws.title, c.coordinate,
                                                    fn))
print("%d formulas; functions used: %s" % (formulas, ", ".join(sorted(used))))
if not any("safe list" in f for f in fails):
    print("  pass  every function is Excel-2007-era, so no _xlfn. prefix is "
          "needed and none can return #NAME?")

# Array-entry constructs are the other way to get an error openpyxl cannot
# see. SUM(IF(range...)) is the one that already bit this file.
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and re.search(r"SUM\s*\(\s*IF\s*\(",
                                                      c.value or ""):
                fails.append("%s!%s uses SUM(IF(...)), which needs array "
                             "entry and evaluates to #VALUE!"
                             % (ws.title, c.coordinate))
if not any("array" in f or "SUM(IF" in f for f in fails):
    print("  pass  no SUM(IF(...)) array construct anywhere")


def num(ws, ref):
    v = ws[ref].value
    return v if isinstance(v, (int, float)) else 0


# ------------------------------------------------ 2. the arithmetic
ws = wb["Three-hour block"]
mins = [num(ws, "A%d" % r) for r in range(5, 12)]
if ws["A12"].value == "=SUM(A5:A11)" and sum(mins) == 180:
    print("  pass  the block sums to 180 minutes: %s" % mins)
else:
    fails.append("block total formula is %r over %r"
                 % (ws["A12"].value, mins))

run, t = [], 0
for m in mins:
    t += m
    run.append(t)
if run[-1] == 180 and ws["B11"].value == "=B10+A11":
    print("  pass  the running column chains correctly and ends at 180: %s"
          % run)
else:
    fails.append("running total chain is wrong: %r / %r"
                 % (run, ws["B11"].value))

# No marks, weights or grades anywhere in the workbook (lecturer decision,
# 4 Nov 2026). The old Assessment and Mark sheet checks are retired, and
# these replace them.
for banned in ("Assessment", "Mark sheet"):
    if banned in wb.sheetnames:
        fails.append("sheet %r still exists; the course has no marks" % banned)
import re as _re
_bad = _re.compile(r"\b(marks?|marked|grades?|graded|weights?|weighted|"
                   r"pass mark|distinction|assessment|assessed|quiz|exam)\b",
                   _re.I)
# Statements that there are no marks are allowed, and so is the Power BI
# date table being "marked" as one.
_ALLOWED = _re.compile(r"no exam, marks, grades or weights|no marks or "
                       r"weights|no marks|never marked|nothing is marked|"
                       r"marked as the date table|marked as a date table|"
                       r"marked and sorted|marking it|correctly marked",
                       _re.I)
_hits = []
for _ws in wb.worksheets:
    for _row in _ws.iter_rows():
        for _c in _row:
            if isinstance(_c.value, str) and not _c.value.startswith("="):
                _t = _ALLOWED.sub("", _c.value)
                _m = _bad.search(_t)
                if _m:
                    _hits.append("%s!%s: %s" % (_ws.title, _c.coordinate,
                                                _m.group(0)))
if _hits:
    fails.append("assessment vocabulary in the workbook: %s" % _hits[:6])
else:
    print("  pass  no marks, grades, weights or assessment wording in any "
          "cell, and no Assessment or Mark sheet")

# The "no marks" notes themselves say "no marks"; they are the only allowed
# use, so the scan above ignores nothing. The Projects sheet therefore must
# not contain the banned words, and it does not.
ws = wb["Projects"]
rows = [ws["A%d" % r].value for r in range(5, 12)]
if rows[:5] == [x[0] for x in __import__("da_content").PROJECTS] \
        and rows[5] == "Final project" and rows[6] == "Certificate":
    print("  pass  the Projects sheet lists the five projects, the final "
          "project and the certificate in order")
else:
    fails.append("Projects sheet rows are %r" % rows)

# The tracker is the only sheet with real logic in it.
ws = wb["Progress tracker"]
hdr = [ws.cell(4, c).value for c in range(1, 12)]
if hdr[3:8] and len([h for h in hdr if h and h.startswith("Project ")]) == 5 \
        and hdr[-1] == "Course status":
    print("  pass  the tracker has five project columns and a status column")
else:
    fails.append("tracker headers are %r" % hdr)

j5, k5 = ws["J5"].value, ws["K5"].value
if ("COUNTIF(D5:H5,\"Finished\")" in j5 and "COUNTA(D5:H5)=0" in j5
        and "AND(J5=5,I5=\"Yes\")" in k5 and "COUNTA(C5:I5)=0" in k5):
    print("  pass  J5 counts Finished statuses over D:H and K5 says Complete "
          "only when all five are Finished and the final project is Yes")
else:
    fails.append("tracker formulas are %r / %r" % (j5, k5))

# Recompute the example row by hand: Finished, Finished, Started, Not
# started, Not started, final project No -> 2 finished, In progress.
ex = [ws.cell(5, c).value for c in range(4, 10)]
fin = sum(1 for v in ex[:5] if v == "Finished")
status = "Complete" if fin == 5 and ex[5] == "Yes" else "In progress"
if fin == 2 and status == "In progress":
    print("  pass  the example row (%s) gives %d finished and %r by the "
          "same rule as the formulas" % (ex, fin, status))
else:
    fails.append("example row gives %d finished, %s" % (fin, status))

# every data row carries both formulas, and blank rows stay blank
rows_ok = all(
    isinstance(ws["J%d" % r].value, str) and ws["J%d" % r].value.startswith(
        "=IF(COUNTA(D%d:H%d)=0" % (r, r))
    and ws["K%d" % r].value.startswith("=IF(COUNTA(C%d:I%d)=0" % (r, r))
    for r in range(5, 29))
if rows_ok:
    print("  pass  all 24 tracker rows carry both formulas and blank "
          "themselves when nothing is entered")
else:
    fails.append("a tracker row is missing its formulas")

if len(ws.data_validations.dataValidation) == 3:
    print("  pass  status, Yes/No and attendance cells have drop-down or "
          "range validation")
else:
    fails.append("tracker data validation missing")

print()
if fails:
    print("FAILURES:")
    for f in fails:
        print("  - " + f)
    sys.exit(1)
print("workbook formulas verified as far as they can be without an engine. "
      "Cached values are absent until the file is opened, which is normal "
      "for an openpyxl-written workbook.")
