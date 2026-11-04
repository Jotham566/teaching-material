"""Build IUEA_Teaching_Plan/IUEA_ML_Gradebook_Semester1.xlsx: an Excel version of the gradebook.gs logic, with formulas.

Sheets: Read me, Settings (weights and maxima), Grades (empty, formulas ready for about 250 students across the three cohorts, one sheet with a
cohort column), Checks (six worked examples with hand-computed expected results and a PASS/FAIL formula for each).
The live gradebook is the Google Sheet driven by grader/gradebook.gs. This workbook is an offline working copy and a calculator that follows the
same rules: weekly best 3 of 5, Block 1 and Block 2 always counted, quizzes out of 35 and assignments out of 160, 15 percent each; data analysis project 10;
Practical Test 1 15; Engineering ML project 45 = Part A /30 + Part B /15. While either project part is blank the project is PENDING: the sheet shows
'Semester 1 provisional: x of 55 marks, y percent' and 'PENDING' for Final % and Band. Once both parts hold a number it shows the full total out of 100.
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
    ("Q7", "J", 6), ("Q8", "K", 6), ("Q9", "L", 6), ("Q10", "M", 6),
    ("W01", "N", 6), ("W02", "O", 6), ("W03", "P", 6), ("W04", "Q", 6), ("W05", "R", 6),
    ("W08", "S", 6), ("W09", "T", 6), ("W10", "U", 6), ("W11", "V", 6), ("W12", "W", 6),
    ("Data Analysis Project", "X", 12), ("Practical Test 1", "Y", 12), ("ML Project Part A", "Z", 12), ("ML Project Part B", "AA", 12),
]
SUBLABEL = {"Q1": "weekly", "Q2": "weekly", "Q3": "weekly", "Q4": "weekly", "Q5": "weekly", "Q7": "Block 1", "Q8": "Block 1", "Q9": "Block 2", "Q10": "Block 2",
            "W01": "A1", "W02": "A2", "W03": "A3", "W04": "A4", "W05": "A5", "W08": "A7 Block 1", "W09": "A8 Block 1", "W10": "A9 Block 2", "W11": "A10 Block 2", "W12": "A11 Block 2",
            "Data Analysis Project": "out of 100", "Practical Test 1": "out of 100", "ML Project Part A": "out of 30", "ML Project Part B": "out of 15"}
CALC_COLUMNS = [
    ("Quizzes earned", "AB", 10), ("Quizzes (of 15)", "AC", 10), ("Assignments earned", "AD", 11), ("Assignments (of 15)", "AE", 11),
    ("Data analysis (of 10)", "AF", 11), ("Test 1 (of 15)", "AG", 10), ("Provisional marks (of 55)", "AH", 12), ("Provisional percent", "AI", 11),
    ("Project", "AJ", 16), ("Project (of 45)", "AK", 10), ("Semester 1 provisional", "AL", 52), ("Final %", "AM", 10), ("Band", "AN", 22), ("Missing", "AO", 60)]
S = "Settings!"


def formulas(r):
    """The calculated cells of one student row. All of them are blank while the student_id cell is blank."""
    g = lambda body: f'=IF($A{r}="","",{body})'
    weekly_q = ",".join(f"IFERROR(LARGE($E{r}:$I{r},{k}),0)" for k in (1, 2, 3))
    weekly_a = ",".join(f"IFERROR(LARGE($N{r}:$R{r},{k}),0)" for k in (1, 2, 3))
    marked = f'$AJ{r}="Project: marked"'
    missing = (f'IF(ISNUMBER($X{r}),"","Data Analysis Project; ")&IF(ISNUMBER($Y{r}),"","Practical Test 1; ")'
               f'&IF(COUNT($E{r}:$I{r})<3,"weekly quizzes: "&COUNT($E{r}:$I{r})&" of 3 that count; ","")'
               f'&IF(COUNT($N{r}:$R{r})<3,"weekly assignments: "&COUNT($N{r}:$R{r})&" of 3 that count; ","")'
               f'&IF(COUNT($J{r}:$K{r})=0,"Block 1 quiz; ","")&IF(COUNT($L{r}:$M{r})=0,"Block 2 quiz; ","")'
               f'&IF(COUNT($S{r}:$T{r})=0,"Block 1 assignment; ","")&IF(COUNT($U{r}:$W{r})=0,"Block 2 assignment; ","")')
    return {
        "AB": g(f"SUM({weekly_q})+SUM($J{r}:$M{r})"),
        "AC": g(f"ROUND($AB{r}/{S}$B$17*{S}$B$3,2)"),
        "AD": g(f"SUM({weekly_a})+SUM($S{r}:$W{r})"),
        "AE": g(f"ROUND($AD{r}/{S}$B$18*{S}$B$4,2)"),
        "AF": g(f"IF(ISNUMBER($X{r}),ROUND($X{r}/100*{S}$B$5,2),0)"),
        "AG": g(f"IF(ISNUMBER($Y{r}),ROUND($Y{r}/100*{S}$B$6,2),0)"),
        "AH": g(f"ROUND($AC{r}+$AE{r}+$AF{r}+$AG{r},2)"),
        "AI": g(f"ROUND($AH{r}/{S}$B$24*100,2)"),
        "AJ": g(f'IF(AND(ISNUMBER($Z{r}),ISNUMBER($AA{r})),"Project: marked","Project: PENDING")'),
        "AK": g(f"IF({marked},ROUND(($Z{r}+$AA{r})/{S}$B$22*{S}$B$7,2),0)"),
        "AL": g(f'IF({marked},"","Semester 1 provisional: "&TEXT($AH{r},"0.00")&" of "&{S}$B$24&" marks, "&TEXT($AI{r},"0.00")&" percent")'),
        "AM": g(f'IF({marked},ROUND($AC{r}+$AE{r}+$AF{r}+$AG{r}+$AK{r},2),"PENDING")'),
        "AN": g(f'IF({marked},IF({S}$B$26,LOOKUP($AM{r},{S}$A$29:$A$34,{S}$B$29:$B$34),"Awaiting Faculty bands"),"PENDING")'),
        "AO": g(missing),
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
    spec = [("E", "I", 5), ("J", "M", 5), ("N", "W", 20), ("X", "Y", 100), ("Z", "Z", 30), ("AA", "AA", 15)]
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
    grid(ws, first, last, 1, 41)
    for r in range(first, last + 1):
        for col in ("AL", "AO"):
            ws[f"{col}{r}"].alignment = Alignment(wrap_text=False, vertical="top")
    ws.freeze_panes = f"E{first}"
    add_validations(ws, first, last)


def build_settings(wb):
    ws = wb.create_sheet("Settings")
    sheet_header(ws, "Settings", "Weights and maxima. Change a weight here and every sheet follows. Decision of the lecturer, 3 November 2026; weights still to be checked against IUEA regulations.")
    ws.column_dimensions["A"].width = 52
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 80
    style_header(ws, 2 + 0, [])
    rows = [
        (3, "Quizzes (percent of the course)", 15, ""),
        (4, "Assignments (percent of the course)", 15, ""),
        (5, "Data analysis project (percent)", 10, "marked out of 100"),
        (6, "Practical Test 1 (percent)", 15, "marked out of 100"),
        (7, "Engineering ML project (percent)", 45, "Part A coded notebook /30 plus Part B decision memo /15. There is no demo."),
        (8, "Total of the weights", "=SUM(B3:B7)", "must be 100"),
        (9, "Weights check", '=IF(B8=100,"OK","WEIGHTS DO NOT SUM TO 100")', ""),
        (10, "Weekly items that count (Weeks 1 to 5)", 3, "Best 3 of 5; Week 6 is waived. The formulas on the Grades sheet use LARGE(...,1), (...,2) and (...,3): to change this number, change the formulas too."),
        (11, "Marks per quiz form", 5, ""),
        (12, "Marks per assignment part", 20, ""),
        (13, "Block 1 quiz (Q7 + Q8)", "=2*B11", "always counts"),
        (14, "Block 2 quiz (Q9 + Q10)", "=2*B11", "always counts"),
        (15, "Block 1 assignment (A7 + A8)", "=2*B12", "always counts"),
        (16, "Block 2 assignment (A9 + A10 + A11)", "=3*B12", "always counts"),
        (17, "Quizzes are out of", "=B10*B11+B13+B14", "3 x 5 + 10 + 10 = 35"),
        (18, "Assignments are out of", "=B10*B12+B15+B16", "3 x 20 + 40 + 60 = 160"),
        (20, "Project Part A maximum", 30, "coded project notebook"),
        (21, "Project Part B maximum", 15, "one-page decision memo"),
        (22, "Project is out of", "=B20+B21", "must equal the project weight"),
        (23, "Project check", '=IF(B22=B7,"OK","PROJECT PARTS DO NOT MATCH THE WEIGHT")', ""),
        (24, "Provisional is out of (marked components)", "=B3+B4+B5+B6", "quizzes + assignments + data analysis project + Practical Test 1 = 55"),
        (26, "Grade bands verified against IUEA regulations? (TRUE or FALSE)", False, "FALSE until the Faculty bands are entered below. While FALSE the Band column says 'Awaiting Faculty bands'."),
    ]
    for r, label, value, note in rows:
        ws[f"A{r}"].value, ws[f"B{r}"].value, ws[f"C{r}"].value = label, value, note
        ws[f"C{r}"].alignment = WRAP
    ws["A28"].value, ws["B28"].value = "Band floor (percent)", "Band"
    style_header(ws, 28, [("A", "Band floor (percent)"), ("B", "Band")])
    for i, (floor, band) in enumerate([(0, "F"), (45, "D"), (50, "C"), (60, "B"), (70, "B+"), (80, "A")]):
        ws[f"A{29 + i}"].value, ws[f"B{29 + i}"].value = floor, band
    ws["C29"].value = "PLACEHOLDER bands copied from gradebook.gs. Replace with the IUEA regulations before you show a letter grade to anybody. Keep the floors in ascending order."
    ws["C29"].alignment = WRAP
    grid(ws, 3, 24, 1, 3)
    grid(ws, 26, 26, 1, 3)
    grid(ws, 29, 34, 1, 2)
    for r in (3, 4, 5, 6, 7, 10, 11, 12, 20, 21, 26):
        ws[f"B{r}"].font = Font(name=FONT, size=10, bold=True)
    for r in range(3, 35):
        ws.row_dimensions[r].height = 28 if r in (10, 26, 29) else 16
    return ws


def build_readme(wb):
    ws = wb.active
    ws.title = "Read me"
    sheet_header(ws, "IUEA ML Semester 1 gradebook (Excel)", "CML3111, CML3112 and CML3113. Written 3 November 2026.")
    ws.column_dimensions["A"].width = 120
    lines = [
        "What this is",
        "An Excel calculator that follows the same rules as grader/gradebook.gs. The live gradebook is the Google Sheet driven by gradebook.gs. Use this workbook as a working copy, a check, or a fallback. Marks entered here do not reach the Google Sheet by themselves.",
        "",
        "How to use it",
        "1. Open the Grades sheet. Type one student per row: student_id, name, email, cohort, then the marks. Leave a cell empty when there is no mark yet. Type 0 only for a real zero.",
        "2. Quiz columns Q1 to Q5 are the weekly quizzes (the best 3 of 5 count). Q7 and Q8 are Block 1, Q9 and Q10 are Block 2. W01 to W05 are the weekly assignments A1 to A5. W08 and W09 are A7 and A8 (Block 1). W10, W11 and W12 are A9, A10 and A11 (Block 2). Q6 and W06 do not exist here: Week 6 is waived.",
        "3. The columns to the right are calculated. Do not type in them.",
        "",
        "Weights (sum 100)",
        "Quizzes 15, assignments 15, data analysis project 10, Practical Test 1 15, Engineering ML project 45 (Part A coded notebook out of 30, Part B one-page decision memo out of 15). There is no demo and no Practical Test 2.",
        "",
        "Provisional results and PENDING",
        "While either project column (ML Project Part A, ML Project Part B) is empty, the project is PENDING. The sheet shows 'Semester 1 provisional: x of 55 marks, y percent', calculated over the quizzes, assignments, data analysis project and Practical Test 1. Final % and Band show PENDING. An unmarked project is never counted as zero.",
        "When both columns hold a number, the sheet shows the full total out of 100. Type 0 and 0 for a student who submitted no project, once marking is finished.",
        "A missing quiz or assignment part still scores zero. An empty data analysis project or Practical Test 1 also scores zero and is listed under Missing.",
        "",
        "Checks sheet",
        "Six worked examples with the answers worked out by hand. The last column says PASS or FAIL for each. If one says FAIL, a formula has been changed.",
        "",
        "Not decided yet",
        "Grade bands are placeholders (Settings sheet) until the IUEA rules are entered. Whether the project is individual or in teams, its release date and its due date (proposed Friday 11 December 2026, 23:59 Kampala) are for the lecturer to confirm.",
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
    full = {c: 5 for c in "EFGHIJKLM"}
    full.update({c: 20 for c in "NOPQRSTUVW"})
    ex = []
    ex.append(("CHECK-1 no project", {**full, "X": 100, "Y": 100}, 55.00, "PENDING"))
    mid = dict(zip("EFGHI", [4, 5, 3, 5, 4]))
    mid.update(dict(zip("NOPQR", [16, 18, 14, 20, 12])))
    ex.append(("CHECK-2 only Part A", {**mid, "X": 72, "Y": 65, "Z": 27}, 28.01, "PENDING"))
    ex.append(("CHECK-3 full total", {**full, "X": 80, "Y": 60, "Z": 24, "AA": 9}, 47.00, 80.00))
    ex.append(("CHECK-4 no submissions", {}, 0.00, "PENDING"))
    ex.append(("CHECK-5 project zero", {**full, "X": 100, "Y": 100, "Z": 0, "AA": 0}, 55.00, 55.00))
    ex.append(("CHECK-6 best-of rules", {**dict(zip("EFGHI", [0, 5, 5, 5, 2])), "J": 5, "K": 5, "L": 5, "M": 0,
                                         **dict(zip("NOPQR", [20, 0, 0, 20, 20])), "S": 20, "T": 20, "U": 20, "V": 0, "W": 20}, 25.99, "PENDING"))
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
    for col, label, w in (("AQ", "Expected provisional marks (hand)", 14), ("AR", "Expected final (hand)", 14), ("AS", "Check", 10)):
        ws.column_dimensions[col].width = w
        ws[f"{col}5"].value, ws[f"{col}5"].fill, ws[f"{col}5"].font, ws[f"{col}5"].alignment, ws[f"{col}5"].border = label, BLACK, H_FONT, CENTER, BORDER
        ws[f"{col}4"].value, ws[f"{col}4"].font, ws[f"{col}4"].alignment, ws[f"{col}4"].border = "by hand" if col != "AS" else "formula", N_FONT, CENTER, BORDER
    for r, (prov, final) in expected.items():
        ws[f"AQ{r}"].value = prov
        ws[f"AR{r}"].value = final
        ws[f"AS{r}"].value = (f'=IF(AND(ROUND($AH{r}-$AQ{r},2)=0,IF(ISNUMBER($AR{r}),AND(ISNUMBER($AM{r}),ROUND($AM{r}-$AR{r},2)=0),$AM{r}=$AR{r})),"PASS","FAIL")')
        for col in ("AQ", "AR", "AS"):
            ws[f"{col}{r}"].border = BORDER
            ws[f"{col}{r}"].font = B_FONT
    ws["A13"].value = "All checks"
    ws["A13"].font = Font(name=FONT, size=10, bold=True)
    ws["B13"].value = f'=IF(COUNTIF(AS{FIRST_ROW}:AS{FIRST_ROW + 5},"PASS")=6,"ALL 6 PASS","CHECK FAILED")'
    ws["B13"].font = Font(name=FONT, size=10, bold=True)
    notes = [
        "By hand. CHECK-1: quizzes 15, assignments 15, data analysis 10, Test 1 15 = 55 of 55, 100 percent; project blank so PENDING.",
        "CHECK-2: weekly quizzes best 3 of [4,5,3,5,4] = 14 of 35 = 6.00; weekly assignments best 3 of [16,18,14,20,12] = 54 of 160 = 5.06; data analysis 7.20; Test 1 9.75; sum 28.01. Part A alone does not end PENDING.",
        "CHECK-3: 15 + 15 + 8.00 + 9.00 + (24 + 9) = 80.00 out of 100. CHECK-4: nothing handed in, 0.00 of 55, PENDING. CHECK-5: project typed as 0 and 0, so marked: final 55.00.",
        "CHECK-6: weekly quizzes best 3 of [0,5,5,5,2] = 15, Block 1 quiz 10, Block 2 quiz 5 = 30 of 35 = 12.86; assignments weekly [20,0,0,20,20] = 60, Block 1 40, Block 2 40 = 140 of 160 = 13.13; data analysis and Test 1 empty = 0; provisional 25.99.",
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
