# -*- coding: utf-8 -*-
"""The glossary handout: every word the track uses, in plain language.

Printed once, in session 1, and kept. Built from the sessions' own vocabulary
lists rather than maintained separately, so a term cannot be taught without
reaching this page and this page cannot drift from what was taught.

The third column is the point: these are people who have been fluent in a
spreadsheet for years and have never been told that a field is a column.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH as AL
from docx.oxml.ns import qn
from docxkit import *              # noqa
import da_content as C             # noqa: E402

OUT = os.path.join(_ROOT, "DataAnalysis_Track",
                   "DataAnalysis_Glossary.docx")


def tidy_page_breaks(doc):
    removed, changed = 0, True
    while changed:
        changed = False
        body = list(doc.element.body)
        for i, el in enumerate(body):
            if el.tag != qn("w:p") or i == 0:
                continue
            pPr = el.find(qn("w:pPr"))
            if pPr is None or pPr.find(qn("w:pageBreakBefore")) is None:
                continue
            prev = body[i - 1]
            if prev.tag == qn("w:p") and \
                    "".join(prev.itertext()).strip() == "":
                prev.getparent().remove(prev)
                removed += 1
                changed = True
                break
    return removed


d = new_doc(margin_cm=1.8)
header_footer(d, "Data Analysis track · glossary · keep this")
first_page_different(d)

spacer(d, 18)
para(d, "DATA ANALYSIS WITH PYTHON, SQL AND POWER BI", size=10, bold=True,
     colour=MID, align=AL.CENTER, after=12)
para(d, "Every word this course uses", size=22, bold=True, colour=NAVY,
     align=AL.CENTER, after=4)
para(d, "{} terms · in plain language · with the spreadsheet equivalent"
     .format(len(C.GLOSSARY)), size=12, colour=MID, align=AL.CENTER,
     after=16)

callout(d, "How to use this",
        "Printed once, in session 1, and kept on the desk for five weeks. "
        "Nothing in this course is explained with a word that is not on this "
        "page.\n\n"
        "The third column matters most. You have been fluent in a "
        "spreadsheet for years, and most of what follows is a second name "
        "for something you already do: a field is a column, a record is a "
        "row, a join is a VLOOKUP, GROUP BY is a pivot table. Where there "
        "is no spreadsheet equivalent, the column says so, and those are "
        "the genuinely new ideas. There are fewer than you expect.\n\n"
        "The session column says where each word is introduced, so you can "
        "go back to the deck it was taught in.",
        MID_H, LIGHT_H)

spacer(d, 10)
rows = [[t, dfn, (xl or "no direct equivalent"), "S{}".format(n)]
        for t, dfn, xl, n in C.GLOSSARY]
table(d, ["Term", "What it means", "In a spreadsheet", "Taught"],
      rows, [16, 50, 26, 8], font=8.6, hdr_font=8.6)

# ------------------------------------------------------------ by session
h = h1(d, "The same words, session by session")
h.paragraph_format.page_break_before = True
para(d, "Use this to prepare, or to catch up after a session you missed. "
        "Each session introduces between four and ten new terms, and they "
        "are read out at the start of it.")

for ss in C.SESSIONS:
    v = ss.get("vocab", [])
    if not v:
        continue
    h3(d, "Session {} · {} · {} new terms".format(
        ss["n"], ss["title"], len(v)))
    table(d, ["", ""],
          [[t, dfn + ("" if not xl else "   [spreadsheet: " + xl + "]")]
           for t, dfn, xl in v], [18, 82], font=8.4, hide_header=True)
    spacer(d, 8)

_gone = tidy_page_breaks(d)
d.save(OUT)
print("saved " + OUT)
print("  {} terms across {} sessions, {} stranded paragraphs removed"
      .format(len(C.GLOSSARY),
              sum(1 for s in C.SESSIONS if s.get("vocab")), _gone))
no_excel = [t for t, _, x, _ in C.GLOSSARY if not x]
print("  {} terms have no spreadsheet equivalent, which is the genuinely "
      "new material:".format(len(no_excel)))
print("    " + ", ".join(no_excel))
