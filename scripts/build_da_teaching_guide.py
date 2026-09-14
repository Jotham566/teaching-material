# -*- coding: utf-8 -*-
"""The Data Analysis lecturer guide: the stage directions, session by session.

pptxkit.notes() splits each note on the TO TEACH marker. Everything before it
goes into the deck's own speaker notes, where a participant can read it in the
shared file; everything after it is lecturer-only and is collected here, so
the decks can be handed out after each session without publishing the answers
or the timing notes.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH as AL
from docx.oxml.ns import qn
from docxkit import *              # noqa
import da_content as DC            # noqa: E402
import build_da_decks as B         # noqa: E402

OUT = os.path.join(_ROOT, "DataAnalysis_Track",
                   "DataAnalysis_Lecturer_Guide.docx")


def h1_page(doc, text):
    h = h1(doc, text)
    h.paragraph_format.page_break_before = True
    return h


def tidy_page_breaks(doc):
    """Same fix as the plan builder: docxkit's callout and table end with a
    spacer paragraph, which strands an empty page before a page break."""
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


# building the decks is what populates LECTURER
for ss in DC.SESSIONS:
    B.build_session(ss)

by_deck = {}
for note in B.LECTURER:
    by_deck.setdefault(note["deck"], []).append(note)

d = new_doc(margin_cm=2.0)
header_footer(d, "Data Analysis track · lecturer guide · not for "
                 "distribution to participants")
first_page_different(d)

spacer(d, 26)
para(d, "LECTURER ONLY", size=10, bold=True, colour=MID, align=AL.CENTER,
     after=14)
para(d, "Data Analysis Track: Stage Directions", size=22, bold=True,
     colour=NAVY, align=AL.CENTER, after=4)
para(d, "Twelve sessions · what to do, in order, on each slide", size=12,
     colour=MID, align=AL.CENTER, after=18)

callout(d, "What this is, and what the decks already say",
        "Each slide in each deck carries speaker notes a participant can "
        "read, because the decks are handed out after every session. The "
        "instructions below are the part that is NOT in the decks: timing, "
        "what to ask the room, which answer to dwell on, and what to do when "
        "somebody is stuck.\n\n"
        "So: the deck is the script and this is the direction. Print this or "
        "keep it on a second screen; do not project it.\n\n"
        "Generated from the decks themselves, so it cannot fall out of step "
        "with them. Re-run build_da_teaching_guide.py after any content "
        "edit.",
        MID_H, LIGHT_H)

spacer(d, 8)
table(d, ["Session", "Slides with direction"],
      [["{}. {}".format(ss["n"], ss["title"]),
        str(len(by_deck.get("S{:02d} {}".format(ss["n"], ss["title"]), [])))]
       for ss in DC.SESSIONS], [70, 30], font=9, hdr_font=9)

for ss in DC.SESSIONS:
    key = "S{:02d} {}".format(ss["n"], ss["title"])
    notes = by_deck.get(key, [])
    h1_page(d, "Session {} · {}".format(ss["n"], ss["title"]))
    para(d, "Week {} · {} · {} hours · roadmap.sh: {}".format(
        ss["week"], ss["tool"], DC.HOURS_PER_SESSION, ss["roadmap"]),
        size=9, bold=True, colour=MID, after=8)

    callout(d, "The mistake this session exists to prevent", ss["trap"],
            "C55A11", AMBER_H)
    spacer(d, 6)

    para(d, "Timing", size=10.5, bold=True, colour=NAVY, after=4)
    table(d, ["Minutes", "What", "Why"],
          [[str(mn), what, why] for mn, what, why in DC.BLOCK],
          [12, 30, 58], font=8.4, hdr_font=8.4)
    spacer(d, 8)

    para(d, "Slide by slide", size=10.5, bold=True, colour=NAVY, after=4)
    if notes:
        table(d, ["Slide", "What the slide says", "What YOU do"],
              [[str(nt["slide"]), nt["title"] or "—", nt["text"]]
               for nt in notes], [8, 30, 62], font=8.4, hdr_font=8.4)
    else:
        para(d, "No lecturer-only direction on this deck.", size=9,
             italic=True, colour=MUTED)

    spacer(d, 8)
    para(d, "Homework set tonight", size=10.5, bold=True, colour=NAVY,
         after=4)
    para(d, ss["home"], size=9.5)
    if ss.get("check"):
        spacer(d, 4)
        para(d, "Assessed here: " + ss["check"], size=9.5, bold=True,
             colour=MID)
    if ss.get("note"):
        spacer(d, 4)
        para(d, "Note: " + ss["note"], size=9.5, italic=True, colour=MID)

_gone = tidy_page_breaks(d)
d.save(OUT)
print("saved " + OUT)
print("  {} sessions, {} lecturer-only directions, {} stranded paragraphs "
      "removed".format(len(DC.SESSIONS), len(B.LECTURER), _gone))
