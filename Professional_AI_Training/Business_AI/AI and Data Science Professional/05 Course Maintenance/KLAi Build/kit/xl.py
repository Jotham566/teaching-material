"""Spreadsheet lab workbooks that work in Excel AND Google Sheets (only plain functions: SUM, SUMPRODUCT, MMULT, MINVERSE, MDETERM, TRANSPOSE, SQRT, EXP, LN, LOG, INDEX, IF, AND, ABS, AVERAGE, STDEV.P, COUNT ...; no dynamic arrays, no LET, no LAMBDA).

    x = XL('Session 2: Vectors', 'Dot product, length and cosine similarity', solution=False)
    ws = x.sheet('Work')
    x.text(ws, 'A1', 'My vectors', bold=True)
    x.input(ws, 'B3', answer='=SUMPRODUCT(B1:D1,B2:D2)')      # a gold cell the learner fills; the model answer is written only in solution mode
    x.check('Dot product is 32', "=Work!B3", 32)            # one automatic check: value of the learner's cell compared with the expected number
    x.save(path)

Every workbook has the sheets: 'Start here' (what to do, written by x.start(...)), your own sheets, and 'Check' (built by x.save): one row per check showing OK or NOT YET, and a summary cell that says
'All N checks pass' or 'N of M checks pass'. Matrix formulas (MMULT, MINVERSE, TRANSPOSE) are written as array formulas over a fixed range with x.array(ws, 'B5:C6', '=MMULT(...)').
Verification: kit/check_workbooks.py builds the solution version, recalculates it with LibreOffice and requires 'All N checks pass', and builds the learner version and requires that it does NOT pass.
"""
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.formula import ArrayFormula

BLACK, GOLD, RED, GREY = '111111', 'E0BE36', 'AE2525', '666666'
FONT = 'Calibri'   # Lato is not installed on most laptops; Calibri exists in Excel and falls back well in Google Sheets
HAIR = Side(style='thin', color='BFBFBF')
BOX = Border(left=HAIR, right=HAIR, top=HAIR, bottom=HAIR)


class XL:
    def __init__(self, title, subtitle, solution=False):
        self.wb = Workbook()
        self.title, self.subtitle, self.solution = title, subtitle, solution
        self.wb.remove(self.wb.active)
        self.checks = []
        self.start_ws = self.wb.create_sheet('Start here')
        self._start_row = 1

    # ---------------------------------------------------------------- sheets and text
    def sheet(self, name, widths=None):
        ws = self.wb.create_sheet(name)
        ws.sheet_view.showGridLines = False
        for col, w in (widths or {}).items():
            ws.column_dimensions[col].width = w
        return ws

    def text(self, ws, cell, value, bold=False, color=BLACK, size=11, wrap=False, fill=None, italic=False, align=None, border=False):
        c = ws[cell]
        c.value = value
        c.font = Font(name=FONT, bold=bold, color=color, size=size, italic=italic)
        c.alignment = Alignment(wrap_text=wrap, vertical='top', horizontal=align)
        if fill:
            c.fill = PatternFill('solid', fgColor=fill)
        if border:
            c.border = BOX
        return c

    def band(self, ws, row, text, cols=8):
        for i in range(1, cols + 1):
            c = ws.cell(row=row, column=i)
            c.fill = PatternFill('solid', fgColor=BLACK)
        c = ws.cell(row=row, column=1, value=text)
        c.font = Font(name=FONT, bold=True, color='FFFFFF', size=13)
        ws.row_dimensions[row].height = 24

    def table(self, ws, top_left, headers, rows, widths=None):
        """A small data table: header row in bold with a gold underline, values below, hairline borders. Returns the cell range of the body."""
        from openpyxl.utils import coordinate_to_tuple, get_column_letter
        r0, c0 = coordinate_to_tuple(top_left)
        for j, h in enumerate(headers):
            c = ws.cell(row=r0, column=c0 + j, value=h)
            c.font = Font(name=FONT, bold=True, color=BLACK)
            c.border = Border(bottom=Side(style='medium', color=GOLD), left=HAIR, right=HAIR, top=HAIR)
        for i, row in enumerate(rows, 1):
            for j, v in enumerate(row):
                c = ws.cell(row=r0 + i, column=c0 + j, value=v)
                c.font = Font(name=FONT, color=BLACK)
                c.border = BOX
        for j, w in enumerate(widths or []):
            ws.column_dimensions[get_column_letter(c0 + j)].width = w
        return f'{get_column_letter(c0)}{r0 + 1}:{get_column_letter(c0 + len(headers) - 1)}{r0 + len(rows)}'

    # ---------------------------------------------------------------- inputs and formulas
    def input(self, ws, cell, answer=None, label=None):
        """A gold cell the learner fills. In the solution workbook the model answer (a value or a formula) is written in it."""
        c = ws[cell]
        c.fill = PatternFill('solid', fgColor=GOLD)
        c.border = Border(left=Side(style='medium', color=BLACK), right=Side(style='medium', color=BLACK), top=Side(style='medium', color=BLACK), bottom=Side(style='medium', color=BLACK))
        c.font = Font(name=FONT, bold=True, color=BLACK)
        if self.solution and answer is not None:
            c.value = answer
        return c

    def formula(self, ws, cell, f, bold=False):
        c = ws[cell]
        c.value = f
        c.font = Font(name=FONT, bold=bold, color=BLACK)
        c.border = BOX
        return c

    def array(self, ws, rng, f, gold=False):
        """An array formula over a fixed range, for MMULT, MINVERSE, TRANSPOSE. Excel and Google Sheets both accept it. In a learner workbook with gold=True the range is left empty."""
        if gold and not self.solution:
            for row in ws[rng]:
                for c in row:
                    c.fill = PatternFill('solid', fgColor=GOLD)
                    c.border = BOX
            return
        first = rng.split(':')[0]
        ws[first] = ArrayFormula(rng, f)
        for row in ws[rng]:
            for c in row:
                c.border = BOX
                c.font = Font(name=FONT, color=BLACK)
                if gold:
                    c.fill = PatternFill('solid', fgColor=GOLD)

    # ---------------------------------------------------------------- start sheet and checks
    def start(self, what, steps, tool_note='Works in Excel and in Google Sheets. In Google Sheets choose File, Import, Upload, then Replace spreadsheet.'):
        ws = self.start_ws
        ws.sheet_view.showGridLines = False
        ws.column_dimensions['A'].width = 110
        self.band(ws, 1, self.title, cols=1)
        self.text(ws, 'A2', self.subtitle, color=GREY)
        self.text(ws, 'A4', 'What you do', bold=True)
        self.text(ws, 'A5', what, wrap=True)
        ws.row_dimensions[5].height = 15 * (1 + len(what) // 105)
        r = 7
        self.text(ws, f'A{r}', 'Steps', bold=True)
        for i, s in enumerate(steps, 1):
            r += 1
            self.text(ws, f'A{r}', f'{i}.  {s}', wrap=True)
            ws.row_dimensions[r].height = 15 * (1 + len(s) // 100)
        r += 2
        self.text(ws, f'A{r}', 'Gold cells are yours to fill. Everything else is given. The sheet called Check tells you which answers are right.', bold=True, wrap=True)
        ws.row_dimensions[r].height = 30
        self.text(ws, f'A{r + 2}', tool_note, color=GREY, italic=True, wrap=True)
        ws.row_dimensions[r + 2].height = 30

    def check(self, label, ref_formula, expected, tol=0.01):
        """Add an automatic check. ref_formula is a formula string for the learner's cell, for example '=Work!B3'. expected is the number it must equal within tol, or a text it must equal."""
        self.checks.append((label, ref_formula, expected, tol))

    def _build_check(self):
        ws = self.wb.create_sheet('Check')
        ws.sheet_view.showGridLines = False
        for col, w in zip('ABCDE', (58, 18, 18, 12, 4)):
            ws.column_dimensions[col].width = w
        self.band(ws, 1, 'Check your answers', cols=4)
        for j, h in enumerate(['What is checked', 'Your value', 'Expected', 'Result']):
            self.text(ws, f'{"ABCD"[j]}3', h, bold=True, border=True)
        n = len(self.checks)
        for i, (label, ref, expected, tol) in enumerate(self.checks):
            r = 4 + i
            self.text(ws, f'A{r}', label, border=True, wrap=True)
            ws[f'B{r}'] = ref
            ws[f'B{r}'].border = BOX
            ws[f'C{r}'] = expected
            ws[f'C{r}'].border = BOX
            if isinstance(expected, (int, float)):
                f = f'=IF(ISNUMBER(B{r}),IF(ABS(B{r}-C{r})<={tol},"OK","NOT YET"),"NOT YET")'
            else:
                f = f'=IF(B{r}=C{r},"OK","NOT YET")'
            ws[f'D{r}'] = f
            ws[f'D{r}'].border = BOX
            ws[f'D{r}'].font = Font(name=FONT, bold=True)
        r = 4 + n + 1
        self.text(ws, f'A{r}', 'Summary', bold=True)
        ws[f'B{r}'] = f'=IF(COUNTIF(D4:D{3 + n},"OK")={n},"All {n} checks pass",COUNTIF(D4:D{3 + n},"OK")&" of {n} checks pass")'
        ws[f'B{r}'].font = Font(name=FONT, bold=True, color=RED)
        self.summary_cell = f'B{r}'
        self.n_checks = n

    def save(self, path):
        self._build_check()
        self.wb.properties.title = self.title
        self.wb.properties.creator = 'KLAi Professional Learning'
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.wb.save(str(path))
        return path
