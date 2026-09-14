# -*- coding: utf-8 -*-
"""Lecturer Teaching Guide — the stage directions stripped out of the decks.

The decks are shared with students, so they carry only student-facing
explanation. Everything that tells the lecturer what to do lives here.
"""
import sys, json, glob, os, re
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
from docx.enum.text import WD_ALIGN_PARAGRAPH as AL
from docxkit import *      # noqa
from docxkit import _border

OUT = _ROOT + "/IUEA_Teaching_Plan/IUEA_ML_Lecturer_Teaching_Guide_W1-W15.docx"

# Collect every extracted lecturer note, keep one copy per week (the three
# cohorts share the same guidance except where a note is explicitly branched).
rows = []
for f in sorted(glob.glob(_ROOT + "/data/lecturer_notes_*.json")):
    rows += json.load(open(f, encoding="utf-8"))

by_week = {}
for r in rows:
    m = re.search(r"Week (\d+)", r["deck"])
    code = r["deck"].split()[0]
    if not m:
        continue
    wk = int(m.group(1))
    key = (wk, r["slide"])
    by_week.setdefault(wk, {})
    if key not in by_week[wk]:
        by_week[wk][key] = {"slide": r["slide"], "title": r["title"],
                            "texts": {}, "order": r["slide"]}
    by_week[wk][key]["texts"][code] = r["text"]

WEEK_TITLE = {
 1: ("AI, machine learning and the engineering problem", "Tue 8 / Fri 11 September 2026"),
 2: ("Colab, notebooks and version control", "Tue 15 / Fri 18 September 2026"),
 3: ("Python as an engineering calculator", "Tue 22 / Fri 25 September 2026"),
 4: ("Collections, loops and files", "Tue 29 September / Fri 2 October 2026"),
 5: ("pandas, and finding data you can trust", "Tue 6 October · Friday cohorts do not meet"),
 6: ("Dirty data, and seeing it", "Tue 13 / Fri 16 October 2026"),
 7: ("Practical Test 1 — Data Investigation", "Tue 20 / Fri 23 October 2026"),
 8: ("Learning from data: the first model", "Tue 27 / Fri 30 October 2026"),
 9: ("Classification: predicting a category", "Tue 3 / Fri 6 November 2026"),
 10: ("Can I trust this model?", "Tue 10 / Fri 13 November 2026"),
 11: ("Features: where engineering knowledge enters", "Tue 17 / Fri 20 November 2026"),
 12: ("Model comparison and engineering judgement", "Tue 24 / Fri 27 November 2026"),
 13: ("Project studio: reproducibility and peer review", "Tue 1 / Fri 4 December 2026"),
 14: ("Practical Test 2 — End-to-End Engineering ML", "Tue 8 / Fri 11 December 2026"),
 15: ("Engineering ML Demo Day, viva and reflection", "Tue 15 / Fri 18 December 2026"),
}

d = new_doc(margin_cm=2.2)
header_footer(d, "IUEA Faculty of Engineering · Lecturer Teaching Guide · Weeks 1–15 · NOT FOR STUDENTS")
first_page_different(d)

spacer(d, 44)
para(d, "INTERNATIONAL UNIVERSITY OF EAST AFRICA · FACULTY OF ENGINEERING",
     size=10.5, bold=True, colour=MID, align=AL.CENTER, after=18)
para(d, "Lecturer Teaching Guide", size=27, bold=True, colour=NAVY, align=AL.CENTER, after=4)
para(d, "Weeks 1–15 · CML3111 · CML3112 · CML3113", size=14, colour=MID, align=AL.CENTER, after=18)
p = para(d, "NOT FOR CIRCULATION TO STUDENTS", size=12, bold=True, align=AL.CENTER,
         after=8, before=8)
_border(p, "top", "C00000", 12)
_border(p, "bottom", "C00000", 12)
spacer(d, 16)
para(d, "Semester 1, 2026/27 · companion to the slide decks", size=11, align=AL.CENTER, after=30)

callout(d, "Why this document exists separately",
        "The slide decks are given to students after each session, so their speaker notes carry only "
        "explanation a student can use. Everything that tells you what to do — what to print, when to "
        "circulate, what to say aloud, what to deliberately get wrong, and the answers to every planted "
        "exercise — was moved here.\n\n"
        "That matters for more than tone. Eight activities depend on students NOT knowing the answer: the "
        "Break and Fix notebooks in Week 2, the Wrong Answer Hunt in Week 3, Investigation Lab 1 in Week 4, "
        "the Outlier Argument in Week 6, the 97 Per Cent Trap in Week 9, the Too Good To Be True leakage "
        "notebooks in Week 10, the unlabelled model comparison in Week 12, and the Week 15 viva bank. "
        "Their answer keys are in this document and nowhere else. Distributing this file to a class group "
        "would invalidate all eight.",
        "C00000", RED_H)
page_break(d)

h1(d, "Contents")
toc(d)
page_break(d)

h1(d, "How to use this guide")
para(d, "Each week below lists its slides in order. For every slide that needs anything from you, the guide "
        "gives the instruction. Slides with no entry need nothing beyond what is on them.")
para(d, "Where the three cohorts need different handling — the Week 5 Independence Day holiday is the main "
        "case — the entry is labelled by course code. Everything else applies to all three.")
para(d, "The decks are generated from scripts, so if you change a slide, change it in the generator rather "
        "than in PowerPoint. Otherwise your edit is lost the next time the deck is rebuilt.")

table(d, ["Course code", "Cohort", "Day, time and room"],
      [["CML3112", "Architecture + Civil Engineering (~100)", "Tuesday 11:00–14:00 · Room 106"],
       ["CML3113", "Mining + Petroleum Engineering (~40–50)", "Friday 08:00–11:00 · Room 105"],
       ["CML3111", "Electrical, Mechatronics & Robotics, Communications (~50)",
        "Friday 11:00–14:00 · Room 115"]],
      [16, 46, 38], bold_first=True)
spacer(d, 10)
callout(d, "The two standing operational facts",
        "Friday is a six-hour back-to-back day, 08:00 to 14:00, with a room change and no gap. Prepare both "
        "Friday sessions as one preparation — they share roughly 70% of content — and put the most demanding "
        "activity in the 08:00 slot.\n\n"
        "Friday 9 October is Independence Day, so CML3113 and CML3111 lose Week 5. Teach it to CML3112 on "
        "Tuesday 6 October and record that session; the recording plus the notebook goes to the Friday "
        "cohorts by Wednesday 7 October, with a 45-minute online clinic that week and a 30-minute "
        "consolidation opening Week 6.", "C55A11", AMBER_H)

for wk in sorted(by_week):
    page_break(d)
    title, when = WEEK_TITLE[wk]
    h1(d, f"Week {wk} — {title}")
    para(d, when, size=11, italic=True, colour=GREY, after=12)

    entries = sorted(by_week[wk].values(), key=lambda r: r["order"])
    n = 0
    for e in entries:
        texts = e["texts"]
        uniq = {}
        for code, t in texts.items():
            uniq.setdefault(t, []).append(code)
        n += 1
        label = f"Slide {e['slide']}"
        if e["title"]:
            label += f" · {e['title']}"
        h3(d, label)
        if len(uniq) == 1:
            para(d, list(uniq)[0], size=10.5, space=1.18, after=8)
        else:
            for t, codes in uniq.items():
                para(d, " / ".join(sorted(codes)) + ":", size=10, bold=True, colour=MID, after=2)
                para(d, t, size=10.5, space=1.18, after=8)
    para(d, f"{n} slides in Week {wk} need something from you.", size=9.5, italic=True,
         colour=GREY, before=8)

spacer(d, 14)
para(d, "Lecturer Teaching Guide version 1.0 · generated from the deck sources · "
        "regenerate after any change to the decks.", size=9, italic=True, colour=GREY,
     align=AL.CENTER)

d.save(OUT)
print("saved", OUT)
print(f"weeks: {sorted(by_week)}; entries: {sum(len(v) for v in by_week.values())}")
