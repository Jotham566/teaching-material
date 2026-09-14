# -*- coding: utf-8 -*-
"""Week 1 pre-flight checklist.

Everything in the programme that has never been executed against real
hardware, plus the checks that make the first session survivable. Written to
be printed and ticked, so it stays short and every line is an action.
"""
import sys

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
from docx.enum.text import WD_ALIGN_PARAGRAPH as AL
from docxkit import *      # noqa
from docxkit import _border

OUT = (_ROOT + "/IUEA_Teaching_Plan/"
       "IUEA_ML_Week1_PreFlight_Checklist.docx")

d = new_doc(margin_cm=2.0)
header_footer(d, "IUEA Faculty of Engineering · CML3111 / CML3112 / CML3113 · "
                 "Week 1 pre-flight")
first_page_different(d)

spacer(d, 26)
para(d, "INTERNATIONAL UNIVERSITY OF EAST AFRICA · FACULTY OF ENGINEERING",
     size=10, bold=True, colour=MID, align=AL.CENTER, after=14)
para(d, "Week 1 Pre-Flight Checklist", size=25, bold=True, colour=NAVY,
     align=AL.CENTER, after=4)
para(d, "Semester 1, 2026/27 · print this and tick it", size=12, colour=MID,
     align=AL.CENTER, after=16)

callout(d, "The hardware is the part that has not been checked",
        "The teaching material for all fifteen weeks is written and checked. What is not "
        "checked is the hardware. Four things in this programme have never been executed "
        "against a real machine or a real room, because they could not be tested from a "
        "sandbox. Each takes about ten minutes and each one can stop a session in front of "
        "a hundred students. They are listed first, before anything else, because no amount "
        "of slide preparation compensates for a room that cannot get online.",
        "C00000", RED_H)

h1(d, "1 · The four untested things")
para(d, "Do these before Tuesday. Write the result in the right-hand column so the next "
        "person to read this knows whether it was checked or assumed.")

table(d, ["#", "What to test", "How", "Pass looks like", "Result"],
      [["1", "Room 106 wifi under load",
        "Get 25–30 students or 25 browser tabs on Colab at once in Room 106 and run a "
        "cell that imports pandas and reads a CSV. Ask ICT for the access-point count "
        "and per-AP client cap in writing.",
        "Every session executes a cell within 30 s. ICT confirms the AP can hold ~100 "
        "clients.", ""],
       ["2", "Colab file upload",
        "In a real Colab notebook run files.upload() and upload a small CSV from the "
        "machine you will teach from.",
        "The file appears and pandas reads it. If it fails, the fallback is mounting "
        "Drive, and the Week 2 deck needs one slide changed.", ""],
       ["3", "The Windows offline installer",
        "Run install_offline_windows.bat on a Windows laptop that has never had Python "
        "installed. This has never been executed — there was no cmd.exe in the build "
        "environment.",
        "Python, the packages and VS Code install without a network. Any student it "
        "fails for is routed to Colab.", ""],
       ["4", "Apps Script HMAC signing",
        "In the gradebook Apps Script, sign a known string with "
        "computeHmacSha256Signature and compare the result against the token "
        "iuea_grader.py produces for the same string.",
        "The two match byte for byte. If they differ, submission tokens cannot be "
        "verified and batch_grade.py --sample becomes the only check.", ""]],
      [4, 20, 34, 34, 8], font=8.2)

spacer(d, 8)
callout(d, "If number 1 fails",
        "This is the one with no software workaround. The Week 2 session onwards assumes "
        "roughly a hundred simultaneous Colab sessions in Room 106. If the room cannot "
        "carry it, the options are to split CML3112 into two half-cohorts for hands-on "
        "weeks, to move that cohort to a room with better coverage, or to fall back to the "
        "offline bundle for that cohort only. All three cost real time to arrange, which is "
        "why this is tested in Week 1 rather than discovered in Week 2.",
        "C55A11", AMBER_H)

page_break(d)

h1(d, "2 · Week 1 materials")
para(d, "All of these are built and validated. This section is a presence check, not a "
        "build instruction.")

table(d, ["Item", "Where", "Check"],
      [["Week 1 deck, your cohort",
        "decks/CML3112_Week01_Design_Infrastructure.pptx · "
        "CML3113_Week01_Mining_Petroleum.pptx · CML3111_Week01_Engineering.pptx",
        "54 slides, starting with the title and your profile. Opens in PowerPoint with figures visible and speaker notes present."],
       ["Lecturer teaching guide",
        "IUEA_ML_Lecturer_Teaching_Guide_W1-W15.docx",
        "Week 1 section read once before the session. NOT to be circulated — it holds "
        "the answer keys."],
       ["Student setup guide",
        "IUEA_ML_Student_Setup_Guide.docx",
        "Printed or shared. Tells students NOT to install Python beforehand."],
       ["Syllabus, your cohort",
        "IUEA_ML_Syllabus_CohortA/B/C_*.docx",
        "Published to students in Week 1, including the assessment weights."],
       ["Pre-work video",
        "IBM Technology, AI / ML / Deep Learning / Generative AI Explained",
        "youtube.com/watch?v=qYNweeDHiyU · under 10 minutes · link tested from your "
        "own machine on the day."]],
      [18, 34, 48], font=8.4)

spacer(d, 6)
h2(d, "The three things Week 1 actually has to achieve")
para(d, "Everything else on the slides is in service of these. If the session runs short, "
        "protect them in this order.")
table(d, ["Priority", "Outcome", "How you know it happened"],
      [["1", "Every student has done machine learning once, on paper, before any "
             "software appears.",
        "The hand-prediction exercise is complete and the error arrow has been drawn. "
        "Students can say what a feature and a target are without prompting."],
       ["2", "Every student knows they already hold the hardest prerequisite.",
        "The roadmap segment has been delivered and the point about Years 1–2 "
        "mathematics has been said out loud. This is the single highest-value sentence "
        "in the session for a cohort that assumes ML belongs to computer scientists."],
       ["3", "Nobody leaves without knowing how they are assessed and that both tests "
             "are offline.",
        "The assessment slide has been shown and the offline-test rule stated. It "
        "changes how students treat coursework from Week 2."]],
      [8, 44, 48], font=8.4)

spacer(d, 8)
h2(d, "Standing operational facts for Semester 1")
para(d, "Friday is a six-hour back-to-back day, 08:00 to 14:00, with a room change and no "
        "gap between CML3113 in Room 105 and CML3111 in Room 115. Prepare both Friday "
        "sessions as one preparation, since they share roughly seventy per cent of their "
        "content, and put the most demanding activity in the 08:00 slot. If a session has "
        "to shrink, shrink the 11:00 one.")
para(d, "Friday 9 October 2026 is Independence Day and falls in Week 5, the pandas "
        "session. CML3112 meets normally on Tuesday 6 October, so teach Week 5 to that "
        "cohort and record it. The recording and the notebook go to CML3113 and CML3111 by "
        "Wednesday 7 October, with a 45-minute online clinic that week and a 30-minute "
        "consolidation opening Week 6. Arrange the recording before 6 October, because "
        "there is no second chance at it.")

spacer(d, 8)
callout(d, "One thing to fix in the first week, not later",
        "Ask ICT in writing for the Room 106 access-point count and client capacity, and "
        "recruit six to eight floor helpers per cohort from among the students who get set "
        "up fastest. Both take a few minutes in Week 1 and both stop being possible once "
        "the hands-on weeks start.", "2E5C8A", LIGHT_H)

spacer(d, 12)
para(d, "Week 1 pre-flight checklist · generated 8 September 2026 · "
        "regenerate from build_preflight_docx.py after any change to the plan.",
     size=8.5, italic=True, colour=GREY, align=AL.CENTER)

d.save(OUT)
print("saved", OUT)
