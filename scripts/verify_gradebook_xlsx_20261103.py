"""Verify IUEA_Teaching_Plan/IUEA_ML_Gradebook_Semester1.xlsx.

1. Structure (openpyxl, formulas as text): sheets, Settings values, formulas present in every calculated cell, no typed values in calculated cells,
   data validations on the mark columns.
2. Recomputation: 80 seeded random students (some with no project, some with only Part A, some complete, some with nothing) are written into a COPY of
   the Grades sheet, LibreOffice recalculates it, and every calculated cell is compared with two independent Python calculations:
   (a) plain arithmetic written here, (b) grader/continuous_assessment.py semester_totals().
3. The Checks sheet: six worked examples with hand-computed answers all say PASS, and the hand values equal the Python values.
Needs LibreOffice (soffice) for step 2 and 3. Usage: python3 scripts/verify_gradebook_xlsx_20261103.py [path-to-xlsx]"""
import random
import shutil
import subprocess
import sys
import tempfile
from math import floor
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "IUEA_Teaching_Plan" / "grader"))
sys.path.insert(0, str(ROOT / "scripts"))
from continuous_assessment import semester_totals  # noqa: E402
import build_gradebook_xlsx_20261103 as B  # noqa: E402

PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "IUEA_Teaching_Plan" / "IUEA_ML_Gradebook_Semester1.xlsx"
FAILS = []
PASSES = 0


def check(name, cond, detail=""):
    global PASSES
    if cond:
        PASSES += 1
    else:
        FAILS.append(f"{name} {detail}")
        print("  FAIL", name, detail)


def round2(x):
    return floor(x * 100 + 0.5) / 100


def recalc(src, outdir):
    subprocess.run(["soffice", "--headless", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(outdir), str(src)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
    return Path(outdir) / Path(src).name


# ---------------------------------------------------------------------------------------------------------------- 1. structure
wb = openpyxl.load_workbook(PATH)
check("sheets", wb.sheetnames == ["Read me", "Settings", "Grades", "Checks"], str(wb.sheetnames))
st = wb["Settings"]
want = {"B3": 15, "B4": 15, "B5": 10, "B6": 15, "B7": 45, "B10": 3, "B11": 5, "B12": 20, "B20": 30, "B21": 15, "B26": False}
for k, v in want.items():
    check(f"Settings {k}", st[k].value == v, f"{st[k].value!r} != {v!r}")
g = wb["Grades"]
calc_cols = [c for _, c, _ in B.CALC_COLUMNS]
bad = [f"{c}{r}" for r in range(B.FIRST_ROW, B.LAST_ROW + 1) for c in calc_cols if not (isinstance(g[f"{c}{r}"].value, str) and g[f"{c}{r}"].value.startswith("="))]
check("every calculated cell on Grades is a formula", not bad, str(bad[:5]))
check("no student data on the shipped Grades sheet", all(g.cell(r, ci).value is None for r in range(B.FIRST_ROW, B.LAST_ROW + 1) for ci in range(1, 28)))
check("black header band", g["A5"].fill.fgColor.rgb in ("FF000000", "00000000") and g["A5"].font.color.rgb in ("FFFFFFFF", "00FFFFFF"), f"{g['A5'].fill.fgColor.rgb} {g['A5'].font.color.rgb}")
check("hairline borders", g["E6"].border.left.style == "hair")
check("data validations on mark columns", len(g.data_validations.dataValidation) >= 7)
check("no Demo or Practical Test 2 column", not any("demo" in str(c.value).lower() or "test 2" in str(c.value).lower() for c in g[5]))
headers = [g[f"{c}5"].value for _, c, _ in B.INPUT_COLUMNS]
check("project part headers", "ML Project Part A" in headers and "ML Project Part B" in headers)

# ---------------------------------------------------------------------------------------------------------------- 2. recomputation
rnd = random.Random(20261103)
cols_q = list("EFGHI"); cols_b = list("JKLM"); cols_w = list("NOPQR"); cols_ab = list("STUVW")


def pick(top, blank=0.18):
    r = rnd.random()
    return None if r < blank else (0 if r < 0.3 else top if r < 0.55 else rnd.randint(0, top))


students = []
for i in range(80):
    mode = i % 5                      # 0 nothing, 1 no project, 2 only Part A, 3 only Part B, 4 complete
    s = {"A": f"S{i:03}", "B": f"Student {i}", "C": f"s{i}@example.com", "D": ["CML3111", "CML3112", "CML3113"][i % 3]}
    if mode != 0:
        for c in cols_q + cols_b:
            s[c] = pick(5)
        for c in cols_w + cols_ab:
            s[c] = pick(20)
        s["X"], s["Y"] = pick(100), pick(100)
    if mode == 2:
        s["Z"] = pick(30, 0.0)
    if mode == 3:
        s["AA"] = pick(15, 0.0)
    if mode == 4:
        s["Z"], s["AA"] = pick(30, 0.0), pick(15, 0.0)
    students.append(s)
tmp = Path(tempfile.mkdtemp())
try:
    copy = tmp / "gradebook.xlsx"
    shutil.copy(PATH, copy)
    w2 = openpyxl.load_workbook(copy)
    for i, s in enumerate(students):
        for col, v in s.items():
            if v is not None:
                w2["Grades"][f"{col}{B.FIRST_ROW + i}"].value = v
    w2.save(copy)
    out = recalc(copy, tmp / "out")
    v = openpyxl.load_workbook(out, data_only=True)
    vg, vc, vs = v["Grades"], v["Checks"], v["Settings"]
    check("Settings: weights total 100", vs["B8"].value == 100 and vs["B9"].value == "OK", f"{vs['B8'].value} {vs['B9'].value}")
    check("Settings: quizzes out of 35, assignments out of 160, provisional out of 55, project out of 45",
          (vs["B17"].value, vs["B18"].value, vs["B24"].value, vs["B22"].value) == (35, 160, 55, 45) and vs["B23"].value == "OK",
          str((vs["B17"].value, vs["B18"].value, vs["B24"].value, vs["B22"].value)))
    pending_n = marked_n = 0
    receipts = []
    for i, s in enumerate(students):
        r = B.FIRST_ROW + i
        # (a) plain arithmetic
        q_weekly = sorted([s[c] for c in cols_q if s.get(c) is not None], reverse=True)[:3]
        q = sum(q_weekly) + sum(s[c] for c in cols_b if s.get(c) is not None)
        a_weekly = sorted([s[c] for c in cols_w if s.get(c) is not None], reverse=True)[:3]
        a = sum(a_weekly) + sum(s[c] for c in cols_ab if s.get(c) is not None)
        qw, aw = round2(q / 35 * 15), round2(a / 160 * 15)
        daw = round2(s["X"] / 100 * 10) if s.get("X") is not None else 0
        t1w = round2(s["Y"] / 100 * 15) if s.get("Y") is not None else 0
        prov = round2(qw + aw + daw + t1w)
        pct = round2(prov / 55 * 100)
        marked = s.get("Z") is not None and s.get("AA") is not None
        pw = round2((s["Z"] + s["AA"]) / 45 * 45) if marked else 0
        final = round2(qw + aw + daw + t1w + pw) if marked else "PENDING"
        got = {c: vg[f"{c}{r}"].value for c in ("AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN", "AO")}
        ok = (got["AB"] == q and got["AD"] == a and abs(got["AC"] - qw) < 1e-9 and abs(got["AE"] - aw) < 1e-9 and abs(got["AF"] - daw) < 1e-9 and abs(got["AG"] - t1w) < 1e-9
              and abs(got["AH"] - prov) < 1e-9 and abs(got["AI"] - pct) < 1e-9 and abs(got["AK"] - pw) < 1e-9)
        check(f"row {s['A']} arithmetic", ok, str(got))
        if marked:
            marked_n += 1
            check(f"row {s['A']} marked", got["AJ"] == "Project: marked" and abs(got["AM"] - final) < 1e-9 and got["AL"] in (None, "") and got["AN"] == "Awaiting Faculty bands", str(got))
        else:
            pending_n += 1
            text = f"Semester 1 provisional: {prov:.2f} of 55 marks, {pct:.2f} percent"
            check(f"row {s['A']} pending", got["AJ"] == "Project: PENDING" and got["AM"] == "PENDING" and got["AN"] == "PENDING" and got["AL"] == text, str(got))
        check(f"row {s['A']} missing list matches the marks", ("Data Analysis Project" in (got["AO"] or "")) == (s.get("X") is None) and ("Practical Test 1" in (got["AO"] or "")) == (s.get("Y") is None))
        # (b) continuous_assessment.py
        qmap = dict(zip(cols_q + cols_b, ["Q1", "Q2", "Q3", "Q4", "Q5", "Q8", "Q9", "Q10", "Q11"]))
        wmap = dict(zip(cols_w + cols_ab, ["W01", "W02", "W03", "W04", "W05", "W08", "W09", "W10", "W11", "W12"]))
        for c, aid in {**qmap, **wmap}.items():
            if s.get(c) is not None:
                receipts.append(dict(cohort=s["D"], student_id=s["A"], assessment=aid, score=s[c], status="GRADED"))
        for c, aid in (("X", "DA_PROJECT"), ("Y", "TEST1")):
            if s.get(c) is not None:
                receipts.append(dict(cohort=s["D"], student_id=s["A"], assessment=aid, score=s[c], status="GRADED"))
        if s.get("Z") is not None or s.get("AA") is not None:
            full = marked
            receipts.append(dict(cohort=s["D"], student_id=s["A"], assessment="ML_PROJECT", score=(s["Z"] + s["AA"]) if full else None,
                                 status="GRADED" if full else "PART_MARKED", part_scores=dict(A=s.get("Z"), B=s.get("AA"))))
    tot = {(r["cohort"], r["student_id"]): r for r in semester_totals(receipts, [(s["D"], s["A"]) for s in students])}
    for i, s in enumerate(students):
        r = B.FIRST_ROW + i
        t = tot[(s["D"], s["A"])]
        check(f"row {s['A']} agrees with continuous_assessment.py",
              abs(vg[f"AH{r}"].value - t["provisional"]["marks"]) < 1e-9 and abs(vg[f"AI{r}"].value - t["provisional"]["percent"]) < 1e-9
              and ((t["final"] is None and vg[f"AM{r}"].value == "PENDING") or (t["final"] is not None and abs(vg[f"AM{r}"].value - t["final"]) < 1e-9)),
              f"{vg[f'AH{r}'].value} {t['provisional']} {vg[f'AM{r}'].value} {t['final']}")
    check("both modes exercised", pending_n > 20 and marked_n > 10, f"pending {pending_n}, marked {marked_n}")
    check("unused Grades rows stay blank", all(vg[f"AM{r}"].value in (None, "") for r in range(B.FIRST_ROW + 80, B.FIRST_ROW + 90)))

    # ------------------------------------------------------------------------------------------------------------ 3. Checks sheet
    results = [vc[f"AS{r}"].value for r in range(B.FIRST_ROW, B.FIRST_ROW + 6)]
    check("Checks sheet: six PASS", results == ["PASS"] * 6, str(results))
    check("Checks sheet: summary cell", vc["B13"].value == "ALL 6 PASS", str(vc["B13"].value))
    # hand values equal Python values
    for (sid, marks, prov, final), r in zip(B.examples(), range(B.FIRST_ROW, B.FIRST_ROW + 6)):
        rec = []
        qm = dict(zip("EFGHIJKLM", ["Q1", "Q2", "Q3", "Q4", "Q5", "Q8", "Q9", "Q10", "Q11"]))
        wm = dict(zip("NOPQRSTUVW", ["W01", "W02", "W03", "W04", "W05", "W08", "W09", "W10", "W11", "W12"]))
        for c, aid in {**qm, **wm}.items():
            if c in marks:
                rec.append(dict(cohort="CML3111", student_id=sid, assessment=aid, score=marks[c], status="GRADED"))
        for c, aid in (("X", "DA_PROJECT"), ("Y", "TEST1")):
            if c in marks:
                rec.append(dict(cohort="CML3111", student_id=sid, assessment=aid, score=marks[c], status="GRADED"))
        if "Z" in marks or "AA" in marks:
            full = "Z" in marks and "AA" in marks
            rec.append(dict(cohort="CML3111", student_id=sid, assessment="ML_PROJECT", score=(marks["Z"] + marks["AA"]) if full else None,
                            status="GRADED" if full else "PART_MARKED", part_scores=dict(A=marks.get("Z"), B=marks.get("AA"))))
        t = semester_totals(rec, [("CML3111", sid)])[0]
        check(f"example {sid}: hand provisional equals python", abs(t["provisional"]["marks"] - prov) < 1e-9, f"{t['provisional']['marks']} vs {prov}")
        check(f"example {sid}: hand final equals python", (final == "PENDING" and t["final"] is None) or (final != "PENDING" and abs(t["final"] - final) < 1e-9), f"{t['final']} vs {final}")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print(f"{PASSES} checks passed, {len(FAILS)} failed")
sys.exit(1 if FAILS else 0)
