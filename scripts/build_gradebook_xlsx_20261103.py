"""Build IUEA_Teaching_Plan/IUEA_ML_Gradebook_Semester1.xlsx: an Excel version of the gradebook.gs logic, with formulas.

Policy of 10 November 2026 (data/assessment_policy_20261110.json): assignments A1 to A5 20 (each /20, all five count equally), quizzes Q1 to Q5 20
(each /5, all five count equally), Practical Test 1 20 (/100 scaled to 20), Engineering ML project 40 (Part A /30 + Part B /15 = 45 raw, scaled to 40).
A missing item scores 0. Not counted: Q6 onward and the block quizzes, A6 onward and the block assignments, the Data Analysis project, Practical Test 2,
the demo; best-3-of-5 and the Week 6 waiver are retired.
Sheets: Read me, Settings (weights and maxima), Grades (empty, formulas ready for about 250 students across the three cohorts, one sheet with a
cohort column), Checks (six worked examples with hand-computed expected results and a PASS/FAIL formula for each).
The live gradebook is the Google Sheet driven by grader/gradebook.gs. This workbook is an offline working copy and a calculator that follows the
same rules. While either project part is blank the project is PENDING: the sheet shows
'Semester 1 provisional: x of 60 marks, y percent' and 'PENDING' for Final % and Band. Once both parts hold a number it shows the full total out of 100.
Style: plain, black header band, hairline borders (KLAi). Usage: python3 scripts/build_gradebook_xlsx_20261103.py [output.xlsx]"""
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "IUEA_Teaching_Plan" / "IUEA_ML_Gradebook_Semester1.xlsx"
FIRST_ROW, LAST_ROW = 6, 255          # Grades: 250 student rows

FONT = "Arial"
BLACK = PatternFill("solid", fgColor="000000")
HAIR = Side(style="hair", color="7F7F7F")
BORDER = Border(left=HAIR, right=HAIR, top=HAIR, bottom=HAIR)
H_FONT = Font(name=FONT, size=10, bold=True, color="FFFFFF")
B_FONT = Font(name=FONT, size=10)
T_FONT = Font(name=FONT, size=14, bold=True)
N_FONT = Font(name=FONT, size=9, italic=True, color="404040")
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)

# column plan (1-based letters) -------------------------------------------------------------------------------------------------------
INPUT_COLUMNS = [
    ("student_id", "A", 16), ("name", "B", 22), ("email", "C", 26), ("cohort", "D", 10),
    ("Q1", "E", 6), ("Q2", "F", 6), ("Q3", "G", 6), ("Q4", "H", 6), ("Q5", "I", 6),
    ("W01", "J", 6), ("W02", "K", 6), ("W03", "L", 6), ("W04", "M", 6), ("W05", "N", 6),
    ("Practical Test 1", "O", 12), ("ML Project Part A", "P", 12), ("ML Project Part B", "Q", 12),
]
SUBLABEL = {"Q1": "out of 5", "Q2": "out of 5", "Q3": "out of 5", "Q4": "out of 5", "Q5": "out of 5",
            "W01": "A1 /20", "W02": "A2 /20", "W03": "A3 /20", "W04": "A4 /20", "W05": "A5 /20",
            "Practical Test 1": "out of 100", "ML Project Part A": "out of 30", "ML Project Part B": "out of 15"}
CALC_COLUMNS = [
    ("Quizzes earned (of 25)", "R", 10), ("Quizzes (of 20)", "S", 10), ("Assignments earned (of 100)", "T", 11), ("Assignments (of 20)", "U", 11),
    ("Test 1 (of 20)", "V", 10), ("Provisional marks (of 60)", "W", 12), ("Provisional percent", "X", 11),
    ("Project", "Y", 16), ("Project (of 40)", "Z", 10), ("Semester 1 provisional", "AA", 52), ("Final %", "AB", 10), ("Band", "AC", 22), ("Missing", "AD", 60)]
S = "Settings!"


def formulas(r):
    """The calculated cells of one student row. All of them are blank while the student_id cell is blank."""
    g = lambda body: f'=IF($A{r}="","",{body})'
    marked = f'$Y{r}="Project: marked"'
    qlist = "".join(f'IF(ISNUMBER(${c}{r}),"","Q{i}, ")' + ("&" if i < 5 else "") for i, c in enumerate("EFGHI", 1))
    alist = "".join(f'IF(ISNUMBER(${c}{r}),"","A{i}, ")' + ("&" if i < 5 else "") for i, c in enumerate("JKLMN", 1))
    missing = (f'IF(ISNUMBER($O{r}),"","Practical Test 1; ")'
               f'&IF(COUNT($E{r}:$I{r})<5,"quizzes: "&LEFT({qlist},LEN({qlist})-2)&"; ","")'
               f'&IF(COUNT($J{r}:$N{r})<5,"assignments: "&LEFT({alist},LEN({alist})-2)&"; ","")')
    return {
        "R": g(f"SUM($E{r}:$I{r})"),
        "S": g(f"ROUND($R{r}*{S}$B$3/{S}$B$13,2)"),
        "T": g(f"SUM($J{r}:$N{r})"),
        "U": g(f"ROUND($T{r}*{S}$B$4/{S}$B$14,2)"),
        "V": g(f"IF(ISNUMBER($O{r}),ROUND($O{r}*{S}$B$5/100,2),0)"),
        "W": g(f"ROUND($S{r}+$U{r}+$V{r},2)"),
        "X": g(f"ROUND($W{r}/{S}$B$20*100,2)"),
        "Y": g(f'IF(AND(ISNUMBER($P{r}),ISNUMBER($Q{r})),"Project: marked","Project: PENDING")'),
        "Z": g(f"IF({marked},ROUND(($P{r}+$Q{r})*{S}$B$6/{S}$B$18,2),0)"),
        "AA": g(f'IF({marked},"","Semester 1 provisional: "&TEXT($W{r},"0.00")&" of "&{S}$B$20&" marks, "&TEXT($X{r},"0.00")&" percent")'),
        "AB": g(f'IF({marked},ROUND($S{r}+$U{r}+$V{r}+$Z{r},2),"PENDING")'),
        "AC": g(f'IF({marked},IF({S}$B$22,LOOKUP($AB{r},{S}$A$25:$A$30,{S}$B$25:$B$30),"Awaiting Faculty bands"),"PENDING")'),
        "AD": g(missing),
    }


def style_header(ws, row, headers, widths=None):
    for col, text in headers:
        c = ws[f"{col}{row}"]
        c.value = text
        c.fill, c.font, c.border, c.alignment = BLACK, H_FONT, BORDER, CENTER


def grid(ws, first, last, c1, c2):
    for r in range(first, last + 1):
        for ci in range(c1, c2 + 1):
            cell = ws.cell(r, ci)
            cell.border = BORDER
            if cell.font == Font():
                cell.font = B_FONT


def add_validations(ws, first, last):
    spec = [("E", "I", 5), ("J", "N", 20), ("O", "O", 100), ("P", "P", 30), ("Q", "Q", 15)]
    for a, b, top in spec:
        dv = DataValidation(type="decimal", operator="between", formula1="0", formula2=str(top), allow_blank=True, showErrorMessage=True,
                            errorTitle="Mark out of range", error=f"Enter a number from 0 to {top}, or leave the cell empty if there is no mark yet.")
        ws.add_data_validation(dv)
        dv.add(f"{a}{first}:{b}{last}")
    dv = DataValidation(type="list", formula1='"CML3111,CML3112,CML3113"', allow_blank=True, showErrorMessage=True, error="Use CML3111, CML3112 or CML3113.")
    ws.add_data_validation(dv)
    dv.add(f"D{first}:D{last}")


def sheet_header(ws, title, note):
    ws["A1"].value = title
    ws["A1"].font = T_FONT
    ws["A2"].value = note
    ws["A2"].font = N_FONT
    ws.sheet_view.showGridLines = False


def build_grades(ws, rows=None, first=FIRST_ROW, last=LAST_ROW):
    headers = INPUT_COLUMNS + CALC_COLUMNS
    for name, col, width in headers:
        ws.column_dimensions[col].width = width
    style_header(ws, 5, [(c, n) for n, c, w in headers])
    for name, col, w in INPUT_COLUMNS:
        sub = SUBLABEL.get(name)
        if sub:
            c = ws[f"{col}4"]
            c.value, c.font, c.alignment, c.border = sub, N_FONT, CENTER, BORDER
    for name, col, w in CALC_COLUMNS:
        c = ws[f"{col}4"]
        c.value, c.font, c.alignment, c.border = "calculated", N_FONT, CENTER, BORDER
    ws.row_dimensions[5].height = 42
    for r in range(first, last + 1):
        for col, f in formulas(r).items():
            ws[f"{col}{r}"].value = f
    for r, values in (rows or {}).items():
        for col, v in values.items():
            ws[f"{col}{r}"].value = v
    grid(ws, first, last, 1, 30)
    for r in range(first, last + 1):
        for col in ("AA", "AD"):
            ws[f"{col}{r}"].alignment = Alignment(wrap_text=False, vertical="top")
    ws.freeze_panes = f"E{first}"
    add_validations(ws, first, last)


def build_settings(wb):
    ws = wb.create_sheet("Settings")
    sheet_header(ws, "Settings", "Weights and maxima. Change a weight here and every sheet follows. Decision of the lecturer, 10 November 2026; weights still to be checked against IUEA regulations.")
    ws.column_dimensions["A"].width = 52
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 80
    style_header(ws, 2 + 0, [])
    rows = [
        (3, "Quizzes Q1 to Q5 (percent of the course)", 20, "each quiz is worth 4; all five count equally"),
        (4, "Assignments A1 to A5 (percent of the course)", 20, "each assignment is worth 4; all five count equally"),
        (5, "Practical Test 1 (percent)", 20, "marked out of 100, scaled to 20"),
        (6, "Engineering ML project (percent)", 40, "Part A coded notebook /30 plus Part B decision memo /15 = 45 raw, scaled to 40. There is no demo."),
        (7, "Total of the weights", "=SUM(B3:B6)", "must be 100"),
        (8, "Weights check", '=IF(B7=100,"OK","WEIGHTS DO NOT SUM TO 100")', ""),
        (10, "Marks per quiz form", 5, ""),
        (11, "Marks per assignment", 20, ""),
        (12, "Quizzes and assignments that count (each)", 5, "All five count. A missing item scores 0. There is no best-of rule and no Week 6 waiver. The Grades sheet has exactly five columns of each."),
        (13, "Quizzes are out of", "=B12*B10", "5 x 5 = 25"),
        (14, "Assignments are out of", "=B12*B11", "5 x 20 = 100"),
        (16, "Project Part A maximum", 30, "coded project notebook"),
        (17, "Project Part B maximum", 15, "one-page decision memo"),
        (18, "Project is out of (raw)", "=B16+B17", "45, scaled to the project weight"),
        (19, "Project check", '=IF(B6=40,"OK","PROJECT WEIGHT IS NOT 40")', ""),
        (20, "Provisional is out of (marked components)", "=B3+B4+B5", "assignments + quizzes + Practical Test 1 = 60"),
        (22, "Grade bands verified against IUEA regulations? (TRUE or FALSE)", False, "FALSE until the Faculty bands are entered below. While FALSE the Band column says 'Awaiting Faculty bands'."),
    ]
    for r, label, value, note in rows:
        ws[f"A{r}"].value, ws[f"B{r}"].value, ws[f"C{r}"].value = label, value, note
        ws[f"C{r}"].alignment = WRAP
    style_header(ws, 24, [("A", "Band floor (percent)"), ("B", "Band")])
    for i, (floor, band) in enumerate([(0, "F"), (45, "D"), (50, "C"), (60, "B"), (70, "B+"), (80, "A")]):
        ws[f"A{25 + i}"].value, ws[f"B{25 + i}"].value = floor, band
    ws["C25"].value = "PLACEHOLDER bands copied from gradebook.gs. Replace with the IUEA regulations before you show a letter grade to anybody. Keep the floors in ascending order."
    ws["C25"].alignment = WRAP
    grid(ws, 3, 20, 1, 3)
    grid(ws, 22, 22, 1, 3)
    grid(ws, 25, 30, 1, 2)
    for r in (3, 4, 5, 6, 10, 11, 12, 16, 17, 22):
        ws[f"B{r}"].font = Font(name=FONT, size=10, bold=True)
    for r in range(3, 31):
        ws.row_dimensions[r].height = 28 if r in (6, 12, 22, 25) else 16
    return ws


def build_readme(wb):
    ws = wb.active
    ws.title = "Read me"
    sheet_header(ws, "IUEA ML Semester 1 gradebook (Excel)", "CML3111, CML3112 and CML3113. Policy of 10 November 2026.")
    ws.column_dimensions["A"].width = 120
    lines = [
        "What this is",
        "An Excel calculator that follows the same rules as grader/gradebook.gs. The live gradebook is the Google Sheet driven by gradebook.gs. Use this workbook as a working copy, a check, or a fallback. Marks entered here do not reach the Google Sheet by themselves.",
        "",
        "How to use it",
        "1. Open the Grades sheet. Type one student per row: student_id, name, email, cohort, then the marks. Leave a cell empty when there is no mark yet. Type 0 only for a real zero.",
        "2. Quiz columns Q1 to Q5 are quizzes 1 to 5, each out of 5. W01 to W05 are assignments A1 to A5, each out of 20. All five of each count equally. Q6 onward, A6 onward, the block quizzes and assignments, the Data Analysis project, Practical Test 2 and the demo do not count and have no column here.",
        "3. The columns to the right are calculated. Do not type in them.",
        "",
        "Weights (sum 100)",
        "Assignments 20 (each of A1 to A5 is worth 4), quizzes 20 (each of Q1 to Q5 is worth 4), Practical Test 1 20 (out of 100, divided by 5), Engineering ML project 40 (Part A out of 30 plus Part B out of 15 = 45, scaled to 40). A missing item scores 0. There is no best-3-of-5 rule and no Week 6 waiver.",
        "",
        "Provisional results and PENDING",
        "While either project column (ML Project Part A, ML Project Part B) is empty, the project is PENDING. The sheet shows 'Semester 1 provisional: x of 60 marks, y percent', calculated over the assignments, quizzes and Practical Test 1. Final % and Band show PENDING. An unmarked project is never counted as zero.",
        "When both columns hold a number, the sheet shows the full total out of 100. Type 0 and 0 for a student who submitted no project, once marking is finished.",
        "Each part is rounded to two decimals (halves up) and the final is the rounded sum of the rounded parts.",
        "",
        "Checks sheet",
        "Six worked examples with the answers worked out by hand. The last column says PASS or FAIL for each. If one says FAIL, a formula has been changed.",
        "",
        "Not decided yet",
        "Grade bands are placeholders (Settings sheet) until the IUEA rules are entered. Whether the project is individual or in teams, its release date and its due date are for the lecturer to confirm.",
        "Student data is private. Keep this file with the other gradebook records. It holds no student data when it is first created.",
    ]
    for i, text in enumerate(lines, start=4):
        c = ws[f"A{i}"]
        c.value = text
        c.alignment = WRAP
        c.font = Font(name=FONT, size=10, bold=text in ("What this is", "How to use it", "Weights (sum 100)", "Provisional results and PENDING", "Checks sheet", "Not decided yet"))
        ws.row_dimensions[i].height = 15 if len(text) < 115 else 15 * (len(text) // 115 + 1)


# six worked examples: (student_id, marks by column letter, expected provisional marks, expected final or 'PENDING')
def examples():
    full = {c: 5 for c in "EFGHI"}
    full.update({c: 20 for c in "JKLMN"})
    ex = []
    ex.append(("CHECK-1 no project", {**full, "O": 100}, 60.00, "PENDING"))
    mid = dict(zip("EFGHI", [4, 5, 3, 5, 4]))
    mid.update(dict(zip("JKLMN", [16, 18, 14, 20, 12])))
    ex.append(("CHECK-2 only Part A", {**mid, "O": 65, "P": 27}, 45.80, "PENDING"))
    ex.append(("CHECK-3 full total", {**full, "O": 60, "P": 24, "Q": 9}, 52.00, 81.33))
    ex.append(("CHECK-4 no submissions", {}, 0.00, "PENDING"))
    ex.append(("CHECK-5 project zero", {**full, "O": 100, "P": 0, "Q": 0}, 60.00, 60.00))
    ex.append(("CHECK-6 missing scores zero", {**dict(zip("FGHI", [5, 5, 5, 2])), **dict(zip("JKLMN", [20, 0, 0, 20, 20]))}, 25.60, "PENDING"))
    return ex


def build_checks(wb):
    ws = wb.create_sheet("Checks")
    sheet_header(ws, "Checks", "Six worked examples. The expected answers were worked out by hand (see the notes on the Read me sheet). The last column recomputes the example and says PASS or FAIL.")
    rows = {}
    expected = {}
    for i, (sid, marks, prov, final) in enumerate(examples()):
        r = FIRST_ROW + i
        rows[r] = {"A": sid, "B": "worked example", "D": "CML3111", **marks}
        expected[r] = (prov, final)
    build_grades(ws, rows, FIRST_ROW, FIRST_ROW + 5)
    for col, label, w in (("AF", "Expected provisional marks (hand)", 14), ("AG", "Expected final (hand)", 14), ("AH", "Check", 10)):
        ws.column_dimensions[col].width = w
        ws[f"{col}5"].value, ws[f"{col}5"].fill, ws[f"{col}5"].font, ws[f"{col}5"].alignment, ws[f"{col}5"].border = label, BLACK, H_FONT, CENTER, BORDER
        ws[f"{col}4"].value, ws[f"{col}4"].font, ws[f"{col}4"].alignment, ws[f"{col}4"].border = "by hand" if col != "AH" else "formula", N_FONT, CENTER, BORDER
    for r, (prov, final) in expected.items():
        ws[f"AF{r}"].value = prov
        ws[f"AG{r}"].value = final
        ws[f"AH{r}"].value = (f'=IF(AND(ROUND($W{r}-$AF{r},2)=0,IF(ISNUMBER($AG{r}),AND(ISNUMBER($AB{r}),ROUND($AB{r}-$AG{r},2)=0),$AB{r}=$AG{r})),"PASS","FAIL")')
        for col in ("AF", "AG", "AH"):
            ws[f"{col}{r}"].border = BORDER
            ws[f"{col}{r}"].font = B_FONT
    ws["A13"].value = "All checks"
    ws["A13"].font = Font(name=FONT, size=10, bold=True)
    ws["B13"].value = f'=IF(COUNTIF(AH{FIRST_ROW}:AH{FIRST_ROW + 5},"PASS")=6,"ALL 6 PASS","CHECK FAILED")'
    ws["B13"].font = Font(name=FONT, size=10, bold=True)
    notes = [
        "By hand. CHECK-1: quizzes 20, assignments 20, Test 1 20 = 60 of 60, 100 percent; project blank so PENDING.",
        "CHECK-2: quizzes 4+5+3+5+4 = 21 of 25 = 16.80; assignments 16+18+14+20+12 = 80 of 100 = 16.00; Test 1 65 / 5 = 13.00; sum 45.80. Part A alone does not end PENDING.",
        "CHECK-3: 20 + 20 + 12.00 + (24 + 9) x 40 / 45 = 29.33, so provisional 52.00 and final 81.33. CHECK-4: nothing handed in, 0.00 of 60, PENDING. CHECK-5: project typed as 0 and 0, so marked: final 60.00.",
        "CHECK-6: quizzes [empty,5,5,5,2] = 17 of 25 = 13.60 (the empty one scores 0); assignments [20,0,0,20,20] = 60 of 100 = 12.00; Test 1 empty = 0; provisional 25.60.",
    ]
    for i, t in enumerate(notes):
        ws[f"A{15 + i}"].value = t
        ws[f"A{15 + i}"].font = N_FONT
    return ws


def build(out=OUT):
    wb = Workbook()
    build_readme(wb)
    build_settings(wb)
    gs = wb.create_sheet("Grades")
    sheet_header(gs, "Grades", "One row per student, all three cohorts. Type marks in the white columns on the left; the columns from 'Quizzes earned' onward are calculated. Empty means not marked yet.")
    build_grades(gs)
    build_checks(wb)
    wb.calculation.fullCalcOnLoad = True
    wb.properties.title = "IUEA ML Semester 1 gradebook"
    wb.properties.creator = "IUEA ML teaching"
    out = Path(out)
    wb.save(out)
    return out


if __name__ == "__main__":
    print("wrote", build())
