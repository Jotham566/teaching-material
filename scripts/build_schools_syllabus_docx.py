# -*- coding: utf-8 -*-
"""The S.5 / S.6 Machine Learning Track syllabus, for students and parents.

ONE TYPE SCALE, DECLARED HERE, REFERENCED EVERYWHERE
----------------------------------------------------
T below is the only place a point size appears. Sizing each element where it
was written is what produced fourteen near-duplicate sizes with a 7.5pt floor
on an earlier document; every value here is a multiple of 0.5, the floor is
9pt because parents will print this, and there are four steps in the reading
range. verify_schools_track.py audits the BUILT file and fails if the
histogram grows a stray.

WRITTEN FOR TWO READERS AT ONCE
-------------------------------
A sixteen-year-old deciding whether to give up part of the holiday, and a
parent deciding whether to pay for it. So: no undefined jargon, every week
says what exists at the end of it, and the limits are stated in the document
rather than discovered in week three.
"""
import os
import sys

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH as AL
from docx.oxml.ns import qn
from docx.shared import Inches
from docxkit import *                # noqa
import schools_content as C          # noqa: E402

TRACK_DIR = _os.path.join(_ROOT, "Schools_ML_Track", "archive", "original_ml_syllabus")
FIGS = _os.path.join(TRACK_DIR, "figs")
OUT = _os.path.join(TRACK_DIR, "ML_Track_S5_S6_Syllabus.docx")

# ------------------------------------------------------------ the type scale
# Nine roles. Nothing outside this dict sets a size.
T = dict(
    display=24.0,     # the title on the cover
    subtitle=13.0,    # the line under it
    h1=15.0,          # section headings
    h2=11.5,          # week headings
    lead=11.0,        # the opening paragraph of a section
    body=10.5,        # everything a parent reads at length
    small=9.5,        # table text, captions
    label=9.0,        # kickers and figure captions. The floor.
)
assert all(abs(v * 2 - round(v * 2)) < 1e-9 for v in T.values()), \
    "every size must be a multiple of 0.5: Word stores half-points"
assert min(T.values()) >= 9.0, "9pt floor: this document gets printed"
_reading = [v for v in T.values() if 9.5 <= v <= 11.5]
assert len(set(_reading)) <= 4, "at most four steps in the reading range"


def fig(d, name, caption):
    """A figure at the width schools_content declares for it.

    The width is not a parameter here on purpose. The figure generator sizes
    its own type against the same number and refuses to draw anything that
    would land under 8pt on paper, so a width chosen at the point of use
    would break that guarantee silently.
    """
    p = d.add_paragraph()
    p.alignment = AL.CENTER
    p.paragraph_format.space_after = Pt(4)
    p.add_run().add_picture(_os.path.join(FIGS, name + ".png"),
                            width=Inches(C.FIG_PLACEMENT[name]))
    para(d, caption, size=T["label"], italic=True, colour=MID,
         align=AL.CENTER, after=12)


def tidy_page_breaks(doc):
    """docxkit's callout() and table() end with a spacer paragraph, which
    strands an empty page before an explicit break."""
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


# ------------------------------------------------------------ the sections
# In order, and numbered from this list rather than by hand. Two sections
# were inserted in the middle of this document after it was first written,
# which left one cross-reference pointing at the wrong section and another
# pointing at a section that had moved. A number typed into prose is a
# number that goes stale silently, so refer to a section with snum().
SECTIONS = [
    "The roadmap",
    "Week by week",
    "A session, hour by hour",
    "The data you will actually work on",
    "Project ideas, so you can picture yours",
    "Marks, and what the certificate means",
    "What to bring",
    "The software, every piece of it by name",
    "Questions parents ask",
    "What this track does not do",
    "Practical details",
]


def snum(title):
    """The number a section ended up with. Raises if the title is wrong,
    because a silently wrong cross-reference is the thing this replaces."""
    return SECTIONS.index(title) + 1


def sref(title):
    return "section %d" % snum(title)


def h1_page(d, title):
    h = h1(d, "%d  ·  %s" % (snum(title), title))
    h.paragraph_format.page_break_before = True
    return h


d = new_doc(margin_cm=1.9)
header_footer(d, "%s for %s  ·  %s" % (C.TRACK, C.FOR_WHOM, C.SUBTITLE),
              size=T["label"])
first_page_different(d)

# ===================================================================== cover
spacer(d, 16)
para(d, "HOLIDAY PROGRAMME FOR %s STUDENTS" % C.FOR_WHOM.upper(),
     size=T["label"], bold=True, colour=MID, align=AL.CENTER, after=10)
para(d, C.TRACK, size=T["display"], bold=True, colour=NAVY, align=AL.CENTER,
     after=4)
para(d, C.SUBTITLE, size=T["subtitle"], colour=MID, align=AL.CENTER,
     after=14)

callout(d, "What your child will be able to do on the last day",
        "Open a data file they have never seen, clean it, find something true "
        "in it, teach a computer to make a prediction from it, check honestly "
        "whether the prediction is any good, and stand up for five minutes "
        "and explain the whole thing to a room.\n\n"
        "They will have built that themselves, on their own laptop, from a "
        "starting point of never having written a line of code. It takes "
        "seventy-two hours and it is genuinely within reach of an S.5 "
        "student.\n\n"
        "The work is published to a portfolio they keep, and the certificate "
        "carries a mark earned from that work rather than from attendance.",
        MID_H, LIGHT_H,
        label_size=T["small"], text_size=T["body"])

spacer(d, 8)
fig(d, "timeline_schools",
    "The eight weeks, and what exists on their laptop at the end of each one.")

# ===================================================================== part 1
h1_page(d, "The roadmap")
para(d, "Fifteen stages, in the order a person actually learns them. The "
        "colour of each card says which fortnight of the track covers it. It "
        "is the first thing in this syllabus because a student deserves to "
        "see the whole route before they start, including where it stops.",
     size=T["lead"])

fig(d, "roadmap_schools",
    "Fifteen stages. The colour says which fortnight covers it. Stage 2 is "
    "the mathematics they already have from A-level. Stage 15 is what comes "
    "after this track, and it is grey because this track does not teach it.")

para(d, "Two of the fifteen cards are not taught here, and both are "
        "deliberate.", size=T["body"], bold=True, after=4)
para(d, "Stage 2, the mathematics, is marked as something they already have. "
        "The mean, the median, spread, correlation, the line of best fit, "
        "probability and gradients are all on the A-level syllabus. This is "
        "the most encouraging fact in the whole document: a student who is "
        "doing Subsidiary or Principal Mathematics is already holding half of "
        "what machine learning is built on, and has never been shown that it "
        "is the same thing.", size=T["body"])
para(d, "Stage 15 is what comes next. Image recognition, language models and "
        "reinforcement learning all need the foundations this track builds. "
        "%s says where to learn them."
     % sref("What this track does not do").capitalize(),
     size=T["body"])

# ===================================================================== part 2
# h1 rather than h1_page: the two roadmap notes above leave most of a page
# free, and forcing a break here wasted it.
h1(d, "%d  ·  %s" % (snum("Week by week"), "Week by week"))
para(d, "Twenty-four sessions of three hours. Each week below says what is "
        "taught, which A-level mathematics it leans on, and what exists at "
        "the end of the week. That last column is the one to read if you are "
        "short of time.", size=T["lead"])

for w in C.WEEKS_PLAN:
    h2(d, "Week %d  ·  %s" % (w["n"], w["title"]))
    para(d, "Roadmap stage%s %s" % (
        "s" if len(w["stages"]) > 1 else "",
        ", ".join(str(n) for n in w["stages"])),
        size=T["label"], bold=True, colour=MID, after=6)

    table(d, ["#", "Session", "What happens"],
          [[str(i + 1), t, b] for i, (t, b) in enumerate(w["sessions"])],
          [4, 30, 66], font=T["small"], hdr_font=T["small"])
    spacer(d, 4)
    table(d, ["", ""],
          [["The maths behind it", w["maths"]],
           ["What you have at the end", w["build"]],
           ["Before the next session", w["home"]]],
          [24, 76], font=T["small"], hide_header=True)
    spacer(d, 10)

# ===================================================================== part 3
h1_page(d, "A session, hour by hour")
para(d, "Every session has the same shape, so nobody has to wonder what is "
        "coming. These are teenagers on holiday, so no teaching block runs "
        "longer than twenty-five minutes and more than half of the time is "
        "spent at the keyboard rather than listening.", size=T["lead"])

table(d, ["Minutes", "What", "Why it is built this way"],
      [[str(m), what, why] for m, what, why in C.BLOCK],
      [10, 24, 66], font=T["small"], hdr_font=T["small"])

spacer(d, 8)
callout(d, "Every session ends with something that runs",
        "A student never leaves with a half-finished screen. The last forty "
        "five minutes of each session exists so that there is a file on their "
        "laptop that does something, however small, before they go home.\n\n"
        "The twenty minutes after that is show and tell: two or three "
        "students put their own screen on the projector. It is the part they "
        "come back for.",
        "1F6F8B", "DDEAF0",
        label_size=T["small"], text_size=T["body"])

# ===================================================================== part 4
h1_page(d, "The data you will actually work on")
para(d, "A course like this is only as concrete as its data, so here is all "
        "of it. Nothing in the list below needs the room's internet to be "
        "working, which is deliberate.", size=T["lead"])

table(d, ["Where it comes from", "What it is"],
      [[a, b] for a, b in C.DATA], [24, 76],
      font=T["small"], hdr_font=T["small"])

spacer(d, 8)
callout(d, "The class survey stays in the class",
        "The dataset the students spend the most time on is the one they "
        "make in the first session, because a table with your own sleep and "
        "your own journey to school in it is the one you argue with. It "
        "carries no names, it is not published to anybody's portfolio, and it "
        "is deleted at the end of the track.\n\n"
        "Everything students do publish is built on public data, or on data "
        "they collected themselves.",
        "1F6F8B", "DDEAF0",
        label_size=T["small"], text_size=T["body"])

# ===================================================================== part 5
h1_page(d, "Project ideas, so you can picture yours")
para(d, "Students choose their own project in Week 7 and present it in Week "
        "8. These are examples to start an argument with rather than a menu, "
        "and the best projects every time are the ones a student brought "
        "themselves. Each one names where the data would come from, because "
        "an idea with no dataset behind it is a wish.", size=T["lead"])

table(d, ["The question", "Where the data comes from"],
      [[q, src] for q, src in C.PROJECTS], [46, 54],
      font=T["small"], hdr_font=T["small"])

spacer(d, 8)
para(d, "What a project has to satisfy", size=T["h2"], bold=True, colour=NAVY,
     after=4)
# A table rather than numbered paragraphs: docxkit's para() has no hanging
# indent, so a wrapped rule ran back to the left margin under its own
# number. Every other list in this document is a table anyway.
table(d, ["", ""],
      [[str(i), rule] for i, rule in enumerate(C.PROJECT_RULES, 1)],
      [4, 96], font=T["small"], hide_header=True)

# ===================================================================== part 6
h1_page(d, "Marks, and what the certificate means")
para(d, "A certificate with real marks was asked for, so the marks come from "
        "work rather than from turning up. Attendance is expected and is not "
        "a grade.", size=T["lead"])

fig(d, "marks_schools",
    "Where the hundred marks come from, and when each piece is due.")

table(d, ["What", "Weight", "When", "How it is marked"],
      [[a, "%d%%" % w, when, how] for a, w, when, how in C.ASSESSMENT],
      [24, 9, 10, 57], font=T["small"], hdr_font=T["small"])

# The bands table split across two pages once, leaving one of them with a
# repeated header row and three lines on it, so this heading forces a break
# and the table, the notes and the callout all travel with it. That page was
# then too empty to justify itself, which is what the mark notes below fix:
# they are the questions a student asks the moment marks are mentioned and
# they belong on this page anyway.
_cert = para(d, "What the certificate says", size=T["h2"], bold=True,
             colour=NAVY, after=4)
_cert.paragraph_format.page_break_before = True
table(d, ["Band", "Mark", "What it claims the student can do"],
      [[name, ("%d%% and above" % cut) if cut else "below 50%", says]
       for name, cut, says in C.BANDS],
      [22, 16, 62], font=T["small"], hdr_font=T["small"])

spacer(d, 6)
para(d, "Late work, missed checkpoints, and second attempts", size=T["h2"],
     bold=True, colour=NAVY, after=4)
table(d, ["", ""], [[a, b] for a, b in C.MARK_NOTES], [22, 78],
      font=T["small"], hide_header=True)

spacer(d, 6)
callout(d, "A student below 50 still receives a certificate, and it does not "
           "overstate",
        "It states that they attended and took part, and it does not claim a "
        "skill that is not there. We would rather a certificate from this "
        "track meant something to the person reading it, including to an "
        "admissions officer who has seen a hundred of them.",
        "C55A11", AMBER_H,
        label_size=T["small"], text_size=T["body"])

# ===================================================================== part 7
h1_page(d, "What to bring")
para(d, "Students bring their own laptops, which means a mixture of Windows "
        "and Mac of different ages. Everything below is planned around that.",
     size=T["lead"])

table(d, ["", ""], [[a, b] for a, b in C.KIT], [22, 78], font=T["small"],
      hide_header=True)

spacer(d, 6)
callout(d, "No laptop? Tell us before Week 1, not on the first morning",
        "A student without a laptop can still take the track: they pair with "
        "somebody for the session work and use a lab machine for the "
        "homework. That has to be arranged in advance, and a student who says "
        "nothing and arrives with no machine loses the first session.\n\n"
        "Everything also runs in a browser with nothing installed, which is "
        "the fallback for a laptop too old or too locked down for the "
        "install.",
        "C55A11", AMBER_H,
        label_size=T["small"], text_size=T["body"])

# ===================================================================== part 8
h1_page(d, "The software, every piece of it by name")
para(d, "All of it is free. None of it is a trial, none of it expires, and "
        "nothing here asks for a card. It is also the same stack a first-year "
        "university course and a working analyst use, so none of it is a toy "
        "version that has to be unlearned later.", size=T["lead"])

table(d, ["Tool", "What it is for"],
      [[a, b] for a, b in C.STACK], [20, 80],
      font=T["small"], hdr_font=T["small"])

spacer(d, 8)
callout(d, "One fixed version for the whole class",
        "Please do not install Python at home before Week 1, however keen a "
        "student is. The packages this track uses are compiled against a "
        "particular version of Python, so a laptop carrying a different one "
        "produces an error message nobody else in the room can reproduce, and "
        "there is no way to fix it while a session is running.\n\n"
        "We install the same version on every machine in Session 1, from a "
        "USB stick, and a student who arrives with nothing installed is the "
        "easiest person in the room to help.",
        "1F6F8B", "DDEAF0",
        label_size=T["small"], text_size=T["body"])

# ===================================================================== part 9
h1_page(d, "Questions parents ask")
for q, a in C.POLICIES:
    para(d, q, size=T["h2"], bold=True, colour=NAVY, after=3)
    para(d, a, size=T["body"], after=9)

# ===================================================================== part 7
h1_page(d, "What this track does not do")
para(d, "Written down because a family deciding how to spend a holiday and a "
        "fee deserves the edges as well as the promises.", size=T["lead"])
for t, why in C.LIMITS:
    para(d, t, size=T["h2"], bold=True, colour=NAVY, after=3)
    para(d, why, size=T["body"], after=9)

spacer(d, 6)
para(d, "Where to go after this track", size=T["h1"], bold=True, colour=NAVY,
     after=6)
table(d, ["", ""], [[a, b] for a, b in C.NEXT], [26, 74], font=T["small"],
      hide_header=True)

# ===================================================================== part 8
h1_page(d, "Practical details")
para(d, "The teaching content of this syllabus is settled. The arrangements "
        "below are for the school to confirm, and they are left blank rather "
        "than guessed, because a syllabus that goes home with a date in it "
        "that turns out to be wrong is worse than one with a gap.",
     size=T["lead"])

table(d, ["To confirm", "Details"],
      [[item, ""] for item in C.TO_CONFIRM], [34, 66],
      font=T["small"], hdr_font=T["small"])

spacer(d, 10)
callout(d, "One request of parents, and it is the one that matters most",
        "Ask your child to show you what they built, once a week. Not to "
        "check it, and you do not need to understand the code. Explaining it "
        "to somebody who does not already know is the single thing that turns "
        "a holiday course into a skill that stays, and ten minutes at the "
        "kitchen table does more for them than any extra session we could "
        "add.",
        MID_H, LIGHT_H,
        label_size=T["small"], text_size=T["body"])

_gone = tidy_page_breaks(d)
d.save(OUT)
print("saved " + OUT)
print("  %d weeks, %d sessions, %d hours, %d roadmap stages, %d stranded "
      "paragraphs removed"
      % (C.WEEKS, C.SESSIONS, C.TOTAL_HOURS, len(C.STAGES), _gone))
print("  type scale: " + ", ".join("%s %.1f" % kv for kv in sorted(
    T.items(), key=lambda kv: -kv[1])))
