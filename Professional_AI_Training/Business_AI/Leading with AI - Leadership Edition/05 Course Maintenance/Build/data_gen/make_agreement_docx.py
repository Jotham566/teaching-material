#!/usr/bin/env python3
"""Build supplier_agreement_busoga_oils.docx from the .txt source (python-docx).

The .txt file is the single source of the wording. Run after editing it:
    python3 make_agreement_docx.py
"""
import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

HERE = Path(__file__).resolve().parent
EDITION = HERE.parents[2]
CASE = EDITION / "03 Learner Materials" / "Practice Files" / "01 Case Company"
SRC = CASE / "supplier_agreement_busoga_oils.txt"
OUT = CASE / "supplier_agreement_busoga_oils.docx"
RED = RGBColor(0xAE, 0x25, 0x25)


def set_font(run, size=None, bold=None, color=None, italic=None):
    run.font.name = "Lato"
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.append(rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), "Lato")
    if size:
        run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color


def para(doc, txt, size=11, bold=False, italic=False, color=None, align=None, before=0, after=4, keep=False):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before, pf.space_after, pf.line_spacing = Pt(before), Pt(after), 1.08
    pf.keep_with_next = keep
    if align:
        p.alignment = align
    r = p.add_run(txt)
    set_font(r, size, bold, color, italic)
    return p


def add_page_field(p):
    for kind, text in (("begin", None), (None, " PAGE "), ("end", None)):
        r = p.add_run()
        set_font(r, 8)
        if kind:
            c = OxmlElement("w:fldChar")
            c.set(qn("w:fldCharType"), kind)
            r._element.append(c)
        else:
            t = OxmlElement("w:instrText")
            t.set(qn("xml:space"), "preserve")
            t.text = text
            r._element.append(t)


def main():
    lines = [l.rstrip() for l in SRC.read_text(encoding="utf-8").splitlines()]
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(2.2)
    sec.top_margin, sec.bottom_margin = Cm(1.8), Cm(1.6)
    st = doc.styles["Normal"]
    st.font.name = "Lato"
    st.font.size = Pt(11)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Lato")

    hp = sec.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_font(hp.add_run("FICTIONAL TEACHING DOCUMENT"), 8, True, RED)
    fp = sec.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_font(fp.add_run("Nile Valley Foods Ltd and Busoga Oils Ltd (fictional). Page "), 8)
    add_page_field(fp)

    i = 0
    while i < len(lines):
        l = lines[i]
        i += 1
        if not l:
            continue
        if l == "FICTIONAL TEACHING DOCUMENT":
            para(doc, l, 11, True, color=RED, after=0)
        elif l.startswith("Not a real contract"):
            para(doc, l, 8.5, italic=True, after=8)
        elif l.startswith("SUPPLY AGREEMENT"):
            para(doc, l, 15, True, after=2, before=2)
        elif l.startswith("Made on"):
            para(doc, l, 11, after=6)
        elif re.match(r"^\d{1,2}\. \S", l) and len(l) < 70:
            para(doc, l, 11.5, True, before=7, after=2, keep=True)
        elif l.startswith(("Signed", "Schedule 1")):
            para(doc, l, 11, after=2, before=2 if l.startswith("Signed for Nile") else 0)
        else:
            para(doc, l, 11, after=4)
    doc.core_properties.author = "KLAi Professional Learning"
    doc.core_properties.title = "Supply Agreement (FICTIONAL TEACHING DOCUMENT)"
    doc.save(OUT)
    print("wrote", OUT.name)


if __name__ == "__main__":
    main()
