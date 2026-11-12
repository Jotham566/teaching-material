"""Helpers for the build guides and rehearsal checklists (Word). Builds on docx_kit.

Inline markup in any text: **bold** and `code`. Lines inside a table cell are split on a newline."""
import re
from docx_kit import *

TOK = re.compile(r'(\*\*.+?\*\*|`.+?`)')
MONO = 'Courier New'


def mono(run):
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    for a in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rf.set(qn(a), MONO)


def rich(p, text, size=10, color=BLACK, bold=False, italic=False):
    for part in TOK.split(text):
        if not part:
            continue
        if part.startswith('**'):
            add_run(p, part[2:-2], size, True, italic, color)
        elif part.startswith('`'):
            r = add_run(p, part[1:-1], size - 0.5, bold, False, color); mono(r)
        else:
            add_run(p, part, size, bold, italic, color)


def setup_styles(doc):
    for name, size, before, after in (('Heading 1', 15, 14, 4), ('Heading 2', 12, 10, 3)):
        st = doc.styles[name]
        st.font.name = FONT; st.font.size = Pt(size); st.font.bold = True; st.font.italic = False
        st.font.color.rgb = rgb(BLACK)
        rf = st.element.rPr.rFonts
        for a in list(rf.attrib):
            if 'Theme' in a or 'theme' in a:
                del rf.attrib[a]
        for a in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
            rf.set(qn(a), FONT)
        st.paragraph_format.space_before = Pt(before); st.paragraph_format.space_after = Pt(after)
        st.paragraph_format.keep_with_next = True


def H1(doc, text):
    p = doc.add_paragraph(style='Heading 1')
    p.add_run(text)
    return p


def H2(doc, text):
    p = doc.add_paragraph(style='Heading 2')
    p.add_run(text)
    return p


def P(doc, text, size=10, after=4, italic=False, color=BLACK, before=0, keep=False):
    p = doc.add_paragraph(); fmt(p, before, after, keep=keep)
    rich(p, text, size, color, italic=italic)
    return p


def NUM(doc, items, size=10, start=1):
    """Numbered steps with a hanging indent. Numbers are typed so that every list restarts at 1."""
    for i, t in enumerate(items, start):
        p = doc.add_paragraph(); fmt(p, 0, 3)
        pf = p.paragraph_format
        pf.left_indent = Cm(0.8); pf.first_line_indent = Cm(-0.8)
        pf.tab_stops.add_tab_stop(Cm(0.8))
        add_run(p, f'{i}.\t', size, True)
        rich(p, t, size)


def BUL(doc, items, size=10):
    for t in items:
        p = doc.add_paragraph(); fmt(p, 0, 2)
        pf = p.paragraph_format
        pf.left_indent = Cm(0.8); pf.first_line_indent = Cm(-0.5)
        pf.tab_stops.add_tab_stop(Cm(0.8))
        add_run(p, '-\t', size, True)
        rich(p, t, size)


def _cell_rich(cell, spec, size, bold=False, color=BLACK):
    cell.paragraphs[0].text = ''
    first = True
    for line in str(spec).split('\n'):
        p = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        fmt(p, 0, 2)
        rich(p, line, size, color, bold=bold)


def TABLE(doc, header, rows, widths, size=9.5, label_cols=(0,)):
    n = len(rows) + (1 if header else 0)
    t = doc.add_table(rows=n, cols=len(widths))
    fix_table(t, widths); cell_margins(t)
    r0 = 0
    if header:
        for c, h in zip(t.rows[0].cells, header):
            shade(c, BLACK); cell_borders(c, BLACK)
            _cell_rich(c, h, 9, True, WHITE)
        trPr = t.rows[0]._tr.get_or_add_trPr(); trPr.append(OxmlElement('w:tblHeader'))
        r0 = 1
    for i, row in enumerate(rows):
        tr = t.rows[r0 + i]; cant_split(tr)
        for j, (c, spec) in enumerate(zip(tr.cells, row)):
            cell_borders(c)
            _cell_rich(c, spec, size, bold=(j in label_cols))
    spacer(doc, 5)
    return t


def GOLD_BOX(doc, title, lines, size=9.5):
    t = doc.add_table(rows=1, cols=1)
    fix_table(t, [CONTENT_CM]); cell_margins(t, 90, 90, 150, 150)
    c = t.rows[0].cells[0]; shade(c, GOLD); cell_borders(c, GOLD)
    p = c.paragraphs[0]; fmt(p, 0, 2); add_run(p, title, size, True)
    for line in lines:
        p = c.add_paragraph(); fmt(p, 0, 2); rich(p, line, size)
    spacer(doc, 5)


def BOX(doc, title, lines, size=9.5):
    t = doc.add_table(rows=1, cols=1)
    fix_table(t, [CONTENT_CM]); cell_margins(t, 90, 90, 150, 150)
    c = t.rows[0].cells[0]; cell_borders(c, '808080')
    p = c.paragraphs[0]; fmt(p, 0, 2); add_run(p, title, size, True)
    for line in lines:
        p = c.add_paragraph(); fmt(p, 0, 2); rich(p, line, size)
    spacer(doc, 5)


def CODE(doc, text, size=9):
    t = doc.add_table(rows=1, cols=1)
    fix_table(t, [CONTENT_CM]); cell_margins(t, 80, 80, 150, 150)
    c = t.rows[0].cells[0]; cell_borders(c, '808080')
    first = True
    for line in text.split('\n'):
        p = c.paragraphs[0] if first else c.add_paragraph()
        first = False
        fmt(p, 0, 0); r = add_run(p, line if line else ' ', size); mono(r)
    spacer(doc, 5)


def new_guide(name, sub_title, subject):
    d = new_doc(name, subject)
    setup_styles(d)
    title(d, name, sub_title)
    return d
