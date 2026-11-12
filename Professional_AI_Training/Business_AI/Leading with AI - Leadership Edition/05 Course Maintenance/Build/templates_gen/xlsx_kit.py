"""openpyxl helpers: KLAi band, instructions, headers, example rows, validation."""
import io
import math
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule, CellIsRule
from openpyxl.drawing.image import Image as XImage
from PIL import Image
from common import *

HAIRSIDE = Side(style='thin', color=HAIR)
BORDER = Border(left=HAIRSIDE, right=HAIRSIDE, top=HAIRSIDE, bottom=HAIRSIDE)
INPUTSIDE = Side(style='thin', color='404040')
INPUT_BORDER = Border(left=INPUTSIDE, right=INPUTSIDE, top=INPUTSIDE, bottom=INPUTSIDE)
BLACKFILL = PatternFill('solid', start_color=BLACK, end_color=BLACK)
GOLDFILL = PatternFill('solid', start_color=GOLD, end_color=GOLD)


def f(size=10, bold=False, italic=False, color=BLACK):
    return Font(name=FONT, size=size, bold=bold, italic=italic, color=color)


F_NORM = f()
F_EX = f(italic=True, color=GREY)
F_HEAD = f(9.5, True, False, WHITE)
WRAP = Alignment(wrap_text=True, vertical='top')
WRAPC = Alignment(wrap_text=True, vertical='top', horizontal='center')


def px(width_chars):
    return int(width_chars * 7 + 5)


def logo_image(height_px=40):
    im = Image.open(LOGO).convert('RGB')
    w = int(im.width * height_px / im.height)
    im2 = im.resize((w * 2, height_px * 2), Image.LANCZOS)
    buf = io.BytesIO(); im2.save(buf, 'PNG'); buf.seek(0)
    xi = XImage(buf); xi.width, xi.height = w, height_px
    return xi, w


def setup(ws, title, instructions, headers, widths, header_h=30, freeze=True):
    """Rows 1-3: black band with logo and title, instructions, column headers. Data starts at row 4."""
    n = len(headers)
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[L(i)].width = w
    ws.sheet_view.showGridLines = False
    ws.row_dimensions[1].height = 38
    for c in range(1, n + 1):
        cell = ws.cell(1, c); cell.fill = BLACKFILL
        cell.border = Border(bottom=Side(style='medium', color=GOLD))
    xi, lw = logo_image(34)
    xi.anchor = 'A1'
    ws.add_image(xi)
    # title column: first column whose left edge is beyond the logo
    acc, tc = 0, 1
    for i, w in enumerate(widths, 1):
        if acc >= lw + 14:
            tc = i; break
        acc += px(w)
        tc = i + 1
    tc = min(tc, n)
    if tc <= n:
        ws.cell(1, tc).value = title
        ws.cell(1, tc).font = f(13, True, False, WHITE)
        ws.cell(1, tc).alignment = Alignment(vertical='center', horizontal='left', indent=1)
    # instructions
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=n)
    c = ws.cell(2, 1); c.value = instructions; c.font = f(9.5); c.alignment = Alignment(wrap_text=True, vertical='center')
    total_chars = sum(widths) * 1.05
    lines = sum(max(1, math.ceil(len(part) / total_chars)) for part in instructions.split('\n'))
    ws.row_dimensions[2].height = max(30, 13.2 * lines + 8)
    # headers
    for i, h in enumerate(headers, 1):
        cell = ws.cell(3, i); cell.value = h; cell.font = F_HEAD; cell.fill = BLACKFILL
        cell.alignment = Alignment(wrap_text=True, vertical='center')
        cell.border = Border(left=Side(style='thin', color=BLACK), right=Side(style='thin', color=BLACK))
    ws.row_dimensions[3].height = header_h
    if freeze:
        ws.freeze_panes = 'A4'
    ws.page_setup.orientation = 'landscape'; ws.page_setup.paperSize = 9
    ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_title_rows = '1:3'
    ws.oddFooter.left.text = FOOT + ws.parent.properties.title if ws.parent.properties.title else FOOT
    ws.oddFooter.left.size = 8
    ws.oddFooter.right.text = 'Page &P of &N'; ws.oddFooter.right.size = 8


def style_row(ws, row, ncols, example=False, center_cols=(), fmts=None, input_cols=None):
    for c in range(1, ncols + 1):
        cell = ws.cell(row, c)
        cell.border = BORDER
        cell.font = F_EX if example else F_NORM
        cell.alignment = WRAPC if c in center_cols else WRAP
        if fmts and c in fmts:
            cell.number_format = fmts[c]


def fill_values(ws, row, values, start_col=1):
    for i, v in enumerate(values):
        if v is not None:
            ws.cell(row, start_col + i).value = v


def add_list(ws, rng, items, prompt=None):
    dv = DataValidation(type='list', formula1='"' + ','.join(items) + '"', allow_blank=True, showErrorMessage=True)
    dv.error = 'Choose a value from the list.'; dv.errorTitle = 'Not in the list'
    if prompt:
        dv.prompt = prompt; dv.showInputMessage = True
    ws.add_data_validation(dv); dv.add(rng)


def add_whole(ws, rng, lo, hi, msg=None):
    dv = DataValidation(type='whole', operator='between', formula1=str(lo), formula2=str(hi), allow_blank=True, showErrorMessage=True)
    dv.error = msg or f'Enter a whole number from {lo} to {hi}.'; dv.errorTitle = 'Out of range'
    ws.add_data_validation(dv); dv.add(rng)


def add_decimal(ws, rng, lo, hi=None):
    if hi is None:
        dv = DataValidation(type='decimal', operator='greaterThanOrEqual', formula1=str(lo), allow_blank=True, showErrorMessage=True)
    else:
        dv = DataValidation(type='decimal', operator='between', formula1=str(lo), formula2=str(hi), allow_blank=True, showErrorMessage=True)
    dv.error = 'Enter a number.'; dv.errorTitle = 'Number needed'
    ws.add_data_validation(dv); dv.add(rng)


def add_date(ws, rng):
    dv = DataValidation(type='date', operator='greaterThan', formula1='36526', allow_blank=True, showErrorMessage=True)
    dv.error = 'Enter a date, for example 15/12/2026.'; dv.errorTitle = 'Date needed'
    ws.add_data_validation(dv); dv.add(rng)


def cf_red(ws, rng, formula):
    ws.conditional_formatting.add(rng, FormulaRule(formula=[formula], font=Font(name=FONT, bold=True, color=RED, italic=False)))


def cf_gold(ws, rng, formula):
    ws.conditional_formatting.add(rng, FormulaRule(formula=[formula], fill=PatternFill('solid', start_color=GOLD, end_color=GOLD, bgColor=GOLD),
                                                     font=Font(name=FONT, bold=True, color=BLACK, italic=False)))


def note(ws, row, text, ncols, height=None, bold=False):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=ncols)
    c = ws.cell(row, 1); c.value = text; c.font = f(9, bold, False, '404040'); c.alignment = Alignment(wrap_text=True, vertical='top')
    if height:
        ws.row_dimensions[row].height = height


def new_wb(title):
    wb = Workbook()
    wb.properties.title = title
    wb.properties.creator = 'KLAi Professional Learning'
    wb.calculation.fullCalcOnLoad = True
    return wb


def save(wb, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(path)); print('wrote', path.name)
