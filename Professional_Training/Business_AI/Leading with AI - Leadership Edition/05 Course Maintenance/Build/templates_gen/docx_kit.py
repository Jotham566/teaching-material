"""python-docx helpers: KLAi header band, footer, tables, example text."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ROW_HEIGHT_RULE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from common import *

CONTENT_CM = 17.4


def rgb(h):
    return RGBColor.from_string(h)


def set_font(run, size=None, bold=None, italic=None, color=None):
    run.font.name = FONT
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts'); rpr.insert(0, rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rf.set(qn(a), FONT)
    if size: run.font.size = Pt(size)
    if bold is not None: run.font.bold = bold
    if italic is not None: run.font.italic = italic
    if color: run.font.color.rgb = rgb(color)


def add_run(p, text, size=10, bold=False, italic=False, color=BLACK):
    r = p.add_run(text)
    set_font(r, size, bold, italic, color)
    return r


def fmt(p, before=0, after=4, line=1.1, align=None, keep=False):
    pf = p.paragraph_format
    pf.space_before = Pt(before); pf.space_after = Pt(after); pf.line_spacing = line
    if align: p.alignment = align
    if keep: pf.keep_with_next = True
    return p


def para(doc, text='', size=10, bold=False, italic=False, color=BLACK, before=0, after=4, align=None, keep=False):
    p = doc.add_paragraph()
    fmt(p, before, after, align=align, keep=keep)
    if text:
        add_run(p, text, size, bold, italic, color)
    return p


def example(p, text, size=10):
    return add_run(p, text, size, False, True, GREY)


def shade(cell, fill):
    tcPr = cell._element.get_or_add_tcPr()
    for old in tcPr.findall(qn('w:shd')):
        tcPr.remove(old)
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), fill)
    tcPr.append(shd)


def cell_borders(cell, color=HAIR, sz=4, sides=('top', 'left', 'bottom', 'right')):
    tcPr = cell._element.get_or_add_tcPr()
    b = tcPr.find(qn('w:tcBorders'))
    if b is None:
        b = OxmlElement('w:tcBorders'); tcPr.append(b)
    for s in ('top', 'left', 'bottom', 'right'):
        e = OxmlElement('w:' + s)
        if s in sides:
            e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), str(sz)); e.set(qn('w:color'), color); e.set(qn('w:space'), '0')
        else:
            e.set(qn('w:val'), 'nil')
        b.append(e)


def cell_margins(table, top=50, bottom=50, left=90, right=90):
    tblPr = table._element.tblPr
    m = OxmlElement('w:tblCellMar')
    for k, v in (('top', top), ('left', left), ('bottom', bottom), ('right', right)):
        e = OxmlElement('w:' + k); e.set(qn('w:w'), str(v)); e.set(qn('w:type'), 'dxa'); m.append(e)
    tblPr.append(m)


def fix_table(table, widths_cm, indent_cm=0):
    table.autofit = False
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    tblPr = table._element.tblPr
    lay = OxmlElement('w:tblLayout'); lay.set(qn('w:type'), 'fixed'); tblPr.append(lay)
    tw = tblPr.find(qn('w:tblW'))
    if tw is None:
        tw = OxmlElement('w:tblW'); tblPr.append(tw)
    tw.set(qn('w:type'), 'dxa'); tw.set(qn('w:w'), str(int(sum(widths_cm) * 567)))
    grid = table._element.find(qn('w:tblGrid'))
    for gc, w in zip(grid.findall(qn('w:gridCol')), widths_cm):
        gc.set(qn('w:w'), str(int(w * 567)))
    for row in table.rows:
        for c, w in zip(row.cells, widths_cm):
            c.width = Cm(w)


def cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    e = OxmlElement('w:cantSplit'); trPr.append(e)


def fill_cell(cell, spec, size=10, bold=False, color=BLACK):
    """spec: text; lines starting with '~' are grey italic examples; '\n' splits paragraphs."""
    cell.paragraphs[0].text = ''
    first = True
    for line in str(spec).split('\n'):
        p = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        fmt(p, 0, 2)
        if line.startswith('~'):
            add_run(p, line[1:], size, False, True, GREY)
        else:
            add_run(p, line, size, bold, False, color)


def grid(doc, rows, widths, header=None, label_cols=(0,), size=10, min_h=None, hdr_size=9):
    """A hairline grid. header: list of column titles in a black band. rows: list of lists of specs."""
    n = len(rows) + (1 if header else 0)
    t = doc.add_table(rows=n, cols=len(widths))
    fix_table(t, widths); cell_margins(t)
    r0 = 0
    if header:
        for c, h in zip(t.rows[0].cells, header):
            shade(c, BLACK); cell_borders(c, BLACK)
            fill_cell(c, h, hdr_size, True, WHITE)
        r0 = 1
        # repeat header row
        trPr = t.rows[0]._tr.get_or_add_trPr(); th = OxmlElement('w:tblHeader'); trPr.append(th)
    for i, row in enumerate(rows):
        tr = t.rows[r0 + i]; cant_split(tr)
        h = min_h[i] if isinstance(min_h, (list, tuple)) else min_h
        if h:
            tr.height = Cm(h); tr.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
        for j, (c, spec) in enumerate(zip(tr.cells, row)):
            cell_borders(c)
            fill_cell(c, spec, size, bold=(j in label_cols))
    return t


def box(doc, title, lines, size=9.5):
    """Instruction box: one hairline cell, no fill."""
    t = doc.add_table(rows=1, cols=1)
    fix_table(t, [CONTENT_CM]); cell_margins(t, 80, 80, 140, 140)
    c = t.rows[0].cells[0]; cell_borders(c, '808080')
    c.paragraphs[0].text = ''
    p = c.paragraphs[0]; fmt(p, 0, 2)
    add_run(p, title, size, True)
    for line in lines:
        p = c.add_paragraph(); fmt(p, 0, 1)
        if line.startswith('~'):
            add_run(p, line[1:], size, False, True, GREY)
        else:
            add_run(p, line, size)
    spacer(doc, 4)
    return t


def spacer(doc, pts=6):
    p = doc.add_paragraph(); fmt(p, 0, 0)
    p.paragraph_format.line_spacing = Pt(pts)
    r = p.add_run(''); r.font.size = Pt(1)
    return p


def title(doc, text, sub=None):
    para(doc, text, 22, True, after=2, keep=True)
    if sub:
        para(doc, sub, 10.5, color='404040', after=8)


def h2(doc, text, before=8, after=3):
    return para(doc, text, 12, True, before=before, after=after, keep=True)


def signoff(doc, labels, widths=None, height=1.3):
    widths = widths or [CONTENT_CM / len(labels)] * len(labels)
    t = doc.add_table(rows=1, cols=len(labels)); fix_table(t, widths); cell_margins(t)
    tr = t.rows[0]; tr.height = Cm(height); tr.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST; cant_split(tr)
    for c, lab in zip(tr.cells, labels):
        cell_borders(c)
        fill_cell(c, lab, 8.5, False, '404040')
    return t


def page_break(doc):
    p = doc.add_paragraph(); fmt(p, 0, 0)
    p.add_run().add_break(WD_BREAK.PAGE)
    p.paragraph_format.line_spacing = Pt(1)


def _field(p, instr, size=8):
    for kind, txt in (('begin', None), (None, instr), ('end', None)):
        r = p.add_run(); set_font(r, size, color='595959')
        if kind:
            fc = OxmlElement('w:fldChar'); fc.set(qn('w:fldCharType'), kind); r._element.append(fc)
        else:
            it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = instr; r._element.append(it)


def p_border(p, side='bottom', color=GOLD, sz=8, space=1):
    pPr = p._p.get_or_add_pPr()
    b = OxmlElement('w:pBdr'); e = OxmlElement('w:' + side)
    e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), str(sz)); e.set(qn('w:space'), str(space)); e.set(qn('w:color'), color)
    b.append(e); pPr.append(b)


def new_doc(template_name, subject=''):
    doc = Document()
    st = doc.styles['Normal']
    st.font.name = FONT; st.font.size = Pt(10)
    st.element.rPr.rFonts.set(qn('w:eastAsia'), FONT)
    st.element.rPr.rFonts.set(qn('w:cs'), FONT)
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(1.8)
    sec.top_margin = Cm(2.7); sec.bottom_margin = Cm(1.8)
    sec.header_distance = Cm(0.9); sec.footer_distance = Cm(0.7)
    # header band
    hd = sec.header
    first = hd.paragraphs[0]
    t = hd.add_table(1, 2, Cm(CONTENT_CM))
    fix_table(t, [7.0, CONTENT_CM - 7.0]); cell_margins(t, 90, 90, 160, 160)
    c0, c1 = t.rows[0].cells
    for c in (c0, c1):
        shade(c, BLACK); cell_borders(c, BLACK)
    p = c0.paragraphs[0]; fmt(p, 0, 0)
    p.add_run().add_picture(str(LOGO), height=Cm(0.85))
    p = c1.paragraphs[0]; fmt(p, 0, 0, align=WD_ALIGN_PARAGRAPH.RIGHT)
    add_run(p, 'Leading with AI  |  Leadership Edition', 8.5, False, False, WHITE)
    c1.vertical_alignment = 1
    c0.vertical_alignment = 1
    first._element.getparent().remove(first._element)
    after = hd.add_paragraph(); fmt(after, 0, 0); p_border(after, 'bottom', GOLD, 8, 0)
    after.paragraph_format.line_spacing = Pt(2)
    # footer
    ft = sec.footer
    fp = ft.paragraphs[0]; fmt(fp, 0, 0)
    p_border(fp, 'top', 'A6A6A6', 4, 4)
    pPr = fp._p.get_or_add_pPr()
    tabs = OxmlElement('w:tabs'); tab = OxmlElement('w:tab')
    tab.set(qn('w:val'), 'right'); tab.set(qn('w:pos'), str(int(CONTENT_CM * 567))); tabs.append(tab); pPr.append(tabs)
    add_run(fp, FOOT + template_name, 8, False, False, '595959')
    add_run(fp, '\tPage ', 8, False, False, '595959')
    _field(fp, 'PAGE')
    for sn in ('Header', 'Footer'):
        try:
            ppr = doc.styles[sn].element.pPr
            if ppr is not None:
                for tb in ppr.findall(qn('w:tabs')):
                    ppr.remove(tb)
        except KeyError:
            pass
    cp = doc.core_properties
    cp.title = template_name; cp.author = 'KLAi Professional Learning'; cp.subject = subject or 'Leading with AI, Leadership Edition'
    cp.keywords = 'KLAi, template'
    return doc


def save(doc, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(path))
    print('wrote', path.name)
