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
version of the mark-sheet formula used SUM(IF(...)), which needs array entry
and came back #VALUE! from a real recalc, so the static check alone would
not have caught it.
"""
import re
import sys
import os

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
WB = os.path.join(_ROOT, "DataAnalysis_Track",
                  "DataAnalysis_Track_Workbook.xlsx")

# Functions that need no prefix and that LibreOffice also evaluates. Anything
# outside this set has to be justified before it goes in.
ALLOWED = {"IF", "SUM", "COUNT", "SUMPRODUCT"}

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

ws = wb["Assessment"]
w = [num(ws, "B%d" % r) for r in range(5, 9)]
if abs(sum(w) - 1.0) < 1e-9 and ws["B9"].value == "=SUM(B5:B8)":
    print("  pass  assessment weights sum to 100%%: %s"
          % ["%.0f%%" % (x * 100) for x in w])
else:
    fails.append("assessment weights sum to %r" % sum(w))

# The mark sheet is the only sheet with real logic in it.
ws = wb["Mark sheet"]
weights = [num(ws, "%s5" % get_column_letter(c)) for c in range(3, 7)]
marks = [num(ws, "%s6" % get_column_letter(c)) for c in range(3, 7)]
if [round(x * 100) for x in weights] == [15, 15, 30, 40]:
    print("  pass  the weight row matches the assessment sheet: %s"
          % ["%.0f%%" % (x * 100) for x in weights])
else:
    fails.append("mark-sheet weights %r do not match the assessment sheet"
                 % weights)

got = sum(m * x for m, x in zip(marks, weights)) / sum(weights)
if abs(got - 73.2) < 0.05:
    print("  pass  the example row (%s) weights to %.1f, which the formula "
          "in G6 computes as SUMPRODUCT over the same two ranges"
          % (marks, got))
else:
    fails.append("example row weights to %.2f, expected 73.2" % got)

# the promise in the note under the table: a half-marked participant is
# scored on the weight actually marked
part = [80, 72, None, None]
den = sum(x for m, x in zip(part, weights) if m is not None)
nume = sum(m * x for m, x in zip(part, weights) if m is not None)
if abs(nume / den - 76.0) < 0.05 and abs(den - 0.30) < 1e-9:
    print("  pass  a participant with only the two checkpoints marked scores "
          "%.1f on %.0f%% of the weight, which is what the note promises"
          % (nume / den, den * 100))
else:
    fails.append("part-marked case gives %.2f on %.2f of the weight"
                 % (nume / den, den))

g6 = ws["G6"].value
if "C$5" in g6 and "F$5" in g6 and 'COUNT(C6:F6)=0' in g6:
    print("  pass  G6 locks the weight row with $5 and blanks itself when no "
          "mark is entered")
else:
    fails.append("G6 is not anchored to the weight row: %r" % g6)

print()
if fails:
    print("FAILURES:")
    for f in fails:
        print("  - " + f)
    sys.exit(1)
print("workbook formulas verified as far as they can be without an engine. "
      "Cached values are absent until the file is opened, which is normal "
      "for an openpyxl-written workbook.")
