"""Make the view-only student copy of the marks workbook: no emails, a short Read me written for students.

  python3 IUEA_Teaching_Plan/grader/make_student_copy.py [--src ~/Desktop/IUEA_Semester1_Final_Marks.xlsx] [--out ~/Desktop/IUEA_Semester1_Marks_Student_Copy.xlsx] [--date "10 November 2026"]

The source is the staff workbook written by refresh_final_marks.sh (already recalculated). Values only, so the copy has no formulas.
"""
import argparse
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

COHORTS = ['CML3111', 'CML3112', 'CML3113']
READ_ME = [
    ('IUEA Semester 1 marks so far', None),
    ('Updated', '{date}'),
    (None, None),
    ('Please check now', None),
    ('1', 'Find your row (Ctrl+F, or Cmd+F on Mac) with your registration number. Check that it is exactly right.'),
    ('2', 'Check your marks: Assignment, Quiz, Test Practical, and Final Mark.'),
    ('3', 'Open the "Why these marks" tab for the reason behind each mark.'),
    ('4', 'If anything is wrong, send me your registration number, the item, and what is wrong. Attach your submission receipt or a screenshot if you have one.'),
    (None, None),
    ('How to read it', None),
    ('Tabs', 'Use the tab for your course: CML3111, CML3112 or CML3113.'),
    ('Assignment /20', 'Assignments 1 to 5, each out of 20. All five count equally.'),
    ('Quiz /20', 'Quizzes 1 to 5, each out of 5. All five count equally.'),
    ('Test Practical /20', 'Practical Test 1 (out of 100) scaled to 20.'),
    ('Project /40', 'Empty for now. It is added after the Week 12 sittings.'),
    ('Final Mark', 'Assignment + Quiz + Test Practical (+ Project once marked). For now it is out of 60, not 100.'),
    ('Whole marks', 'Every mark is rounded to a whole number; half a mark rounds up.'),
    ('A 0', 'It means I did not receive that item, or could not mark it. "Why these marks" says which.'),
    ('Name not captured', 'I have no name for this registration number. Tell me yours.'),
]


def build(src, out, date):
    s = load_workbook(src, data_only=True)
    wb = Workbook()
    wb.remove(wb.active)
    thin = Side(style='thin', color='BFBFBF')
    box = Border(left=thin, right=thin, top=thin, bottom=thin)
    black = PatternFill('solid', fgColor='000000')
    pale = PatternFill('solid', fgColor='FFF7D6')

    rm = wb.create_sheet('Read me')
    rm.column_dimensions['A'].width = 22
    rm.column_dimensions['B'].width = 100
    rm.sheet_view.showGridLines = False
    for i, (a, b) in enumerate(READ_ME, 1):
        rm.cell(row=i, column=1, value=a)
        rm.cell(row=i, column=2, value=(b or '').replace('{date}', date) or None)
        rm.cell(row=i, column=2).alignment = Alignment(wrap_text=True, vertical='top')
        rm.cell(row=i, column=1).alignment = Alignment(vertical='top')
        if b is None and a:
            rm.cell(row=i, column=1).font = Font(bold=True, size=14 if i == 1 else 12)
        elif a:
            rm.cell(row=i, column=1).font = Font(bold=True)

    hdr = ['Reg Number', 'Name', 'Program', 'Assignment /20', 'Quiz /20', 'Test Practical /20', 'Project /40', 'Final Mark']
    widths = [18, 34, 11, 15, 11, 18, 12, 12]
    for cohort in COHORTS:
        ws_src = s[cohort]
        ws = wb.create_sheet(cohort)
        ws['A1'] = f'{cohort} marks so far'
        ws['A1'].font = Font(bold=True, size=14)
        ws['A2'] = 'Final Mark is out of 60 until the project is added (out of 100). See "Read me".'
        ws['A2'].font = Font(italic=True, color='595959')
        for j, (h, wd) in enumerate(zip(hdr, widths), 1):
            c = ws.cell(row=4, column=j, value=h)
            c.font = Font(bold=True, color='FFFFFF')
            c.fill = black
            c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            c.border = box
            ws.column_dimensions[get_column_letter(j)].width = wd
        ws.row_dimensions[4].height = 32
        n = 0
        for r in range(5, ws_src.max_row + 1):
            if not ws_src.cell(r, 1).value:
                continue
            n += 1
            # source columns: 1 reg, 2 name, 3 email (dropped), 4 program, 5..9 marks
            vals = [ws_src.cell(r, c).value for c in (1, 2, 4, 5, 6, 7, 8, 9)]
            for j, v in enumerate(vals, 1):
                c = ws.cell(row=4 + n, column=j, value=v)
                c.border = box
                if j >= 4:
                    c.alignment = Alignment(horizontal='center')
                    c.number_format = '0'
            ws.cell(row=4 + n, column=7).fill = pale
            ws.cell(row=4 + n, column=8).font = Font(bold=True)
        ws.freeze_panes = 'A5'
        ws.auto_filter.ref = f'A4:H{4 + n}'
        ws.sheet_view.showGridLines = False
        ws.page_setup.orientation = 'landscape'
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.print_title_rows = '4:4'

    w_src = s['Why these marks']
    ws = wb.create_sheet('Why these marks')
    ws['A1'] = 'Why these marks'
    ws['A1'].font = Font(bold=True, size=14)
    for j, (h, wd) in enumerate(zip(['Cohort', 'Reg Number', 'Name', 'Why these marks'], [11, 18, 30, 120]), 1):
        c = ws.cell(row=4, column=j, value=h)
        c.font = Font(bold=True, color='FFFFFF')
        c.fill = black
        c.alignment = Alignment(horizontal='center', vertical='center')
        c.border = box
        ws.column_dimensions[get_column_letter(j)].width = wd
    n = 0
    for r in range(5, w_src.max_row + 1):
        if not w_src.cell(r, 2).value:
            continue
        n += 1
        for j in range(1, 5):
            c = ws.cell(row=4 + n, column=j, value=w_src.cell(r, j).value)
            c.border = box
            c.alignment = Alignment(wrap_text=True, vertical='top')
        txt = str(w_src.cell(r, 4).value or '')
        ws.row_dimensions[4 + n].height = max(30, 15 * (txt.count('\n') + 1 + len(txt) // 120))
    ws.freeze_panes = 'A5'
    ws.auto_filter.ref = f'A4:D{4 + n}'
    ws.sheet_view.showGridLines = False
    wb.save(out)
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--src', default=str(Path.home() / 'Desktop' / 'IUEA_Semester1_Final_Marks.xlsx'))
    ap.add_argument('--out', default=str(Path.home() / 'Desktop' / 'IUEA_Semester1_Marks_Student_Copy.xlsx'))
    ap.add_argument('--date', default='10 November 2026')
    a = ap.parse_args()
    n = build(a.src, a.out, a.date)
    print(f'{n} students; written to {a.out}')


if __name__ == '__main__':
    main()
