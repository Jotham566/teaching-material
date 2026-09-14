# -*- coding: utf-8 -*-
"""Build the IUEA Semester 1 Master Teaching Plan workbook."""
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
from plan_content import (CALENDAR, COHORT_META, SHARED, COHORTS, ASSESSMENT,
                          ALT_MODEL, RUBRICS, TOOLS, DATASETS, RISKS, B,
                          QUIZZES, TECH_STACK, MARKING_LOAD,
                          MARKING_TOTAL_BEFORE, MARKING_TOTAL_AFTER, AUTHORING_ONE_OFF)

OUT = _ROOT + "/IUEA_Teaching_Plan/IUEA_ML_Semester1_Master_Teaching_Plan.xlsx"

FONT = "Arial"
NAVY = "1F3864"
MID = "2E5C8A"
LIGHT = "D9E2F3"
BAND = "F2F5FB"
AMBER = "FFF2CC"
RED = "FCE4E4"
GREEN = "E2EFDA"

thin = Side(style="thin", color="B4C6E7")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

H_FILL = PatternFill("solid", fgColor=NAVY)
H_FONT = Font(name=FONT, size=10, bold=True, color="FFFFFF")
T_FONT = Font(name=FONT, size=18, bold=True, color=NAVY)
S_FONT = Font(name=FONT, size=11, italic=True, color=MID)
SEC_FONT = Font(name=FONT, size=12, bold=True, color="FFFFFF")
SEC_FILL = PatternFill("solid", fgColor=MID)
BODY = Font(name=FONT, size=9)
BODY_B = Font(name=FONT, size=9, bold=True)
TOP = Alignment(vertical="top", wrap_text=True)
TOPC = Alignment(vertical="top", horizontal="center", wrap_text=True)

wb = Workbook()


def title_block(ws, title, subtitle, span):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=span)
    c = ws.cell(1, 1, title); c.font = T_FONT
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=span)
    c = ws.cell(2, 1, subtitle); c.font = S_FONT
    ws.row_dimensions[1].height = 26
    ws.row_dimensions[2].height = 18


def header_row(ws, row, headers, widths, height=32):
    for i, h in enumerate(headers, start=1):
        c = ws.cell(row, i, h)
        c.font = H_FONT; c.fill = H_FILL
        c.alignment = Alignment(vertical="center", horizontal="center", wrap_text=True)
        c.border = BORDER
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[row].height = height


def write_row(ws, row, values, fill=None, bold_first=False, heights=None):
    for i, v in enumerate(values, start=1):
        c = ws.cell(row, i, v)
        c.font = BODY_B if (bold_first and i == 1) else BODY
        c.alignment = TOPC if i == 1 else TOP
        c.border = BORDER
        if fill:
            c.fill = PatternFill("solid", fgColor=fill)
    if heights:
        ws.row_dimensions[row].height = heights


# ==========================================================================
# 1. READ ME
# ==========================================================================
ws = wb.active
ws.title = "Read Me"
ws.sheet_properties.tabColor = NAVY
title_block(ws, "IUEA Year 3 Engineering — Machine Learning Programme",
            "Semester 1 Master Teaching Plan · 7 September – 18 December 2026 · 15 study weeks · 3 contact hours per cohort per week",
            6)
ws.column_dimensions["A"].width = 26
for col in "BCDEF":
    ws.column_dimensions[col].width = 22

r = 4


def sec(text):
    global r
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
    c = ws.cell(r, 1, text); c.font = SEC_FONT; c.fill = SEC_FILL
    c.alignment = Alignment(vertical="center", wrap_text=True)
    ws.row_dimensions[r].height = 20
    r += 1


def para(label, text, h=None):
    global r
    c = ws.cell(r, 1, label); c.font = BODY_B; c.alignment = TOP
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=6)
    c2 = ws.cell(r, 2, text); c2.font = BODY; c2.alignment = TOP
    ws.row_dimensions[r].height = h or 30
    r += 1


sec("WHAT THIS WORKBOOK IS")
para("Purpose", "The lecturer-ready master plan for Semester 1. It fixes the calendar, the week-by-week "
                "architecture, the shared core and the cohort-specific overlay, the assessment design and the "
                "rubrics. It is the layer that must be agreed BEFORE lesson plans, slide decks, notebooks and "
                "labs are produced.", 44)
para("Design rule", "Approximately 70% of each session is a shared machine learning core, taught identically to all "
                    "three cohorts, and approximately 30% is a discipline-specific overlay of examples, datasets and "
                    "projects. Prepare once, re-skin three times. The 'Shared vs Divergent' sheet tells you exactly "
                    "which is which, week by week.", 44)
para("Pedagogical rule", "The problem creates the need for the concept. No week opens with a definition. Every tool is "
                         "introduced by the problem it solves. Students are left to struggle productively in at least "
                         "one segment of every session.", 36)
para("Not yet built", "Lesson plans, slide decks, Jupyter notebooks, the course-authored teaching datasets, the test "
                      "variants and the Semester 2 plan. The 'Dataset Register' marks every course-authored artefact "
                      "as TO BE BUILT with the week it is needed.", 36)

r += 1
sec("THE CONFIRMED TIMETABLE")
para("Status", "CONFIRMED by the lecturer, September 2026. Every date, room and time in this workbook now "
               "follows from this table. There is nothing left to fill in.", 26)

hdr = ["Course code", "Day & time", "Room", "Cohort & programmes", "Approx. size", "Course title"]
header_row(ws, r, hdr, [16, 24, 12, 38, 18, 42])
r += 1
for _code, _key in (("CML3112", "A"), ("CML3113", "B"), ("CML3111", "C")):
    _m = COHORT_META[_key]
    write_row(ws, r, [_code, f"{_m['day']} {_m['time']}", _m["room"],
                      f"{_m['name']} \u2014 {_m['programmes']}", _m["size"], _m["title"]],
              fill=GREEN, bold_first=True, heights=30)
    r += 1

r += 1
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
c = ws.cell(r, 1, "THREE CONSEQUENCES OF THIS TIMETABLE, each of which changes how the semester runs.  "
                  "(1) Friday is a SIX-HOUR back-to-back day, 08:00\u201314:00, with a room change and no gap \u2014 "
                  "see Risk R16.  "
                  "(2) The Week 5 Independence Day holiday now falls only on the two FRIDAY cohorts. CML3112 "
                  "teaches Week 5 normally on Tue 06 Oct, so record that session and issue it to the Friday "
                  "cohorts \u2014 see Risk R1.  "
                  "(3) The largest cohort (~100) is in Room 106, and because the course runs in Google Colab, "
                  "that room's WIFI capacity is now the biggest single delivery risk \u2014 see Risk R17.")
c.font = BODY_B; c.alignment = TOP; c.fill = PatternFill("solid", fgColor=AMBER)
ws.row_dimensions[r].height = 62
r += 2

sec("THE THREE COHORTS")
header_row(ws, r, ["Cohort", "Programmes", "Approx. size", "Course title", "Course code", "Anchor domain"],
           [26, 30, 24, 42, 24, 34])
r += 1
for k in ("A", "B", "C"):
    m = COHORT_META[k]
    write_row(ws, r, [m["name"], m["programmes"], m["size"], m["title"], m["code"], m["domain"]],
              fill=BAND if k == "B" else None, bold_first=True, heights=32)
    r += 1

r += 1
sec("ACTION 2 — ESCALATE THESE THREE ITEMS TO THE FACULTY IN WEEK 1")
for label, txt in [
    ("Test capacity", "Cohort A (~100) almost certainly cannot sit the Week 7 and Week 14 practical tests in one lab "
                      "sitting. A written capacity request, or approval for two sittings, is needed by Week 5. See Risk R2."),
    ("Week 5 holiday", "Friday 9 October 2026 is Uganda Independence Day and falls in Week 5. Both Friday cohorts lose "
                       "the most important pandas session of the semester. Either a make-up slot is approved or the "
                       "asynchronous mitigation is published by 7 October. Decide in Week 2. See Risk R1."),
    ("Marking support", "Fully human marking of this design is about 246 hours a semester, roughly 16 hours a week. "
                        "The auto-grading stack takes it to about 120 hours, roughly 8 hours a week. Still worth "
                        "quantifying in a Week 1 request. See the 'Marking Load' sheet and Risk R8."),
    ("Assessment records", "There is no institutional LMS, so quiz responses and the gradebook will sit in a "
                           "personal Google account. Get a written Faculty position on ownership and data "
                           "protection, and export everything to the course share as CSV at the end of every "
                           "block. See Risk R15."),
    ("Assessment policy", "The weightings on the 'Assessment' sheet are a proposal. If IUEA mandates a coursework / "
                          "final split, the alternative 40/60 mapping on that same sheet satisfies it without changing "
                          "any teaching. Confirm which model applies before Week 5, because Test 1 falls in Week 7."),
]:
    para(label, txt, 40)

r += 1
sec("HOW TO NAVIGATE THIS WORKBOOK")
for label, txt in [
    ("Calendar", "All 15 weeks with real dates for both the Tuesday and the Friday slots, teaching weeks and "
                 "assessment weeks marked, and the public holiday flagged."),
    ("Master Plan (Shared Core)", "The 70% core. One row per week. This is what you prepare once."),
    ("Cohort A / B / C", "The full 20-column plan per cohort, with the discipline overlay merged in. These are the "
                         "sheets to print or hand to the department."),
    ("Shared vs Divergent", "Week by week: what is identical across cohorts and what must be re-skinned. Use this to "
                            "plan your own preparation time."),
    ("Assessment", "Component weights, dates, individual versus team, machine-marked share, and the alternative "
                   "40/60 continuous-assessment model."),
    ("Assessment Tech Stack", "The five free layers that make continuous assessment possible for one lecturer, "
                              "with each tool's verified limits. Working code is in the assessment-tools folder."),
    ("Marking Load", "The before-and-after arithmetic: ~246 hours fully human against ~120 with the stack."),
    ("Rubrics", "All six rubrics, with criterion weights that sum to 100 by formula."),
    ("Tools Rollout", "Every tool, the week it appears, and the problem it solves. The AI-assistant ladder is the last row."),
    ("Dataset Register", "Every dataset with host, licence, size, task, weeks used and verification status."),
    ("Risk Register", "Twelve risks with owners and mitigations. R1, R2 and R3 need action in the first fortnight."),
]:
    para(label, txt, 26)

r += 1
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
c = ws.cell(r, 1, "Dataset verification note: datasets marked VERIFIED were confirmed to exist and to be openly "
                  "licensed on 1 September 2026. Those marked VERIFY BEFORE USE are named from the lecturer's "
                  "knowledge of the repositories but were not confirmed. Re-check every link in the week before "
                  "you use it, and stage every dataset on the local share rather than fetching it live in class.")
c.font = Font(name=FONT, size=9, italic=True, color="9C4500"); c.alignment = TOP
c.fill = PatternFill("solid", fgColor=AMBER)
ws.row_dimensions[r].height = 46
ws.freeze_panes = "A4"

# ==========================================================================
# 2. CALENDAR
# ==========================================================================
ws = wb.create_sheet("Calendar")
ws.sheet_properties.tabColor = MID
title_block(ws, "Semester 1 Calendar", "15 study weeks from Monday 7 September 2026. Each cohort meets once per week for 3 hours.", 7)
hdr = ["Week", "Block / Phase", "Week commencing", "CML3112 · Tue 11:00–14:00 · Rm 106",
       "CML3113 · Fri 08:00–11:00 · Rm 105", "CML3111 · Fri 11:00–14:00 · Rm 115",
       "Week type", "Notes and actions"]
header_row(ws, 4, hdr, [7, 30, 18, 24, 24, 24, 17, 58])
r = 5
for wk, wc, tue, fri, kind, note in CALENDAR:
    phase = SHARED[wk]["phase"]
    fill = None
    if kind.startswith("ASSESSMENT"):
        fill = RED
    elif "Demo" in kind:
        fill = GREEN
    elif note:
        fill = AMBER
    write_row(ws, r, [wk, phase, wc, tue, fri, fri, kind, note], fill=fill, bold_first=True,
              heights=44 if note else 26)
    r += 1

r += 1
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
c = ws.cell(r, 1, "Teaching weeks: 13.  Assessment weeks: 2 (Weeks 7 and 14).  Contact hours per cohort: 45. "
                  "Total lecturer contact: 9 hours per week — 3 on Tuesday and SIX BACK-TO-BACK ON FRIDAY, "
                  "08:00 to 14:00 with a room change and no gap. See Risk R16.")
c.font = BODY_B; c.alignment = TOP
r += 1
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
c = ws.cell(r, 1, "Colour key:  red = assessment week ·  amber = action required ·  green = demo day.")
c.font = Font(name=FONT, size=9, italic=True); c.alignment = TOP
ws.freeze_panes = "A5"

# ==========================================================================
# 3. MASTER PLAN — SHARED CORE
# ==========================================================================
CORE_HDR = ["Week", "Block / Phase", "Topic", "Learning objectives (by the end of the session, students can…)",
            "3-hour session structure", "Concepts introduced", "Tools introduced",
            "Practical / lab", "Interactive challenge", "Assignment", "Weekly quiz (QR, auto-graded)",
            "Project milestone", "Assessment relevance", "Lecturer preparation", "Required resources"]
CORE_W = [7, 30, 34, 62, 78, 56, 50, 56, 56, 44, 54, 40, 46, 66, 52]


def cp_text(wk):
    if wk not in QUIZZES:
        return "—"
    title, desc = QUIZZES[wk]
    return title + "\n" + desc


def structure_with_cp(wk, structure):
    """Append the standing quiz instruction to a teaching week's running order.

    Every teaching session ends with the five-minute weekly quiz, so this is
    the same note in all twelve weeks. Weeks 7 and 14 are the practical tests
    and Week 15 is Demo Day, and none of those carry a quiz.
    """
    if wk not in QUIZZES:
        return structure
    return (structure + "\n" + B + "LAST FIVE MINUTES — " + QUIZZES[wk][0] +
            ". Open the Form, project the QR, give it exactly five minutes, close it, and show the "
            "cohort's score distribution before they leave. Worth 1%, best 10 of 12 count, no resits. "
            "If the network is down, convert it to a 48-hour link and say so out loud.")


ws = wb.create_sheet("Master Plan (Shared Core)")
ws.sheet_properties.tabColor = "70AD47"
title_block(ws, "Master Plan — the shared 70% machine learning core",
            "Taught identically to all three cohorts. Prepare once. The discipline overlay lives on the three cohort sheets.", 14)
header_row(ws, 4, CORE_HDR, CORE_W, 40)
r = 5
for wk in range(1, 16):
    d = SHARED[wk]
    fill = RED if d["phase"].startswith("ASSESSMENT") else (BAND if wk % 2 == 0 else None)
    write_row(ws, r, [wk, d["phase"], d["topic"], d["los"], structure_with_cp(wk, d["structure"]),
                      d["concepts"], d["tools"], d["practical"], d["challenge"], d["assignment"],
                      cp_text(wk), d["milestone"], d["assessrel"], d["prep"], d["resources"]],
              fill=fill, bold_first=True, heights=200)
    r += 1
ws.freeze_panes = "C5"
ws.auto_filter.ref = f"A4:O{r-1}"

# ==========================================================================
# 4–6. COHORT SHEETS
# ==========================================================================
COH_HDR = ["Week", "Block / Phase", "Week commencing", "Session date · time · room", "Cohort",
           "Course code", "Course title", "Topic",
           "Learning objectives (by the end of the session, students can…)",
           "3-hour session structure", "Concepts introduced", "Tools introduced", "Practical / lab",
           "Dataset(s)", "Interactive challenge", "Assignment (due next session)",
           "Weekly quiz (QR, auto-graded)", "Project milestone",
           "Assessment relevance", "Lecturer preparation", "Required resources", "Shared vs cohort-specific"]
COH_W = [7, 28, 18, 27, 9, 12, 40, 34, 62, 78, 56, 50, 60, 60, 56, 44, 54, 40, 46, 70, 52, 46]

TAB = {"A": "C00000", "B": "BF8F00", "C": "2E75B6"}
for k in ("A", "B", "C"):
    m = COHORT_META[k]
    ws = wb.create_sheet(f"Cohort {k}")
    ws.sheet_properties.tabColor = TAB[k]
    title_block(ws, f"Cohort {k} — {m['title']}",
                f"{m['programmes']} · {m['size']} · one 3-hour session per week · 45 contact hours · "
                f"{m['slot']}", 20)
    header_row(ws, 4, COH_HDR, COH_W, 44)
    r = 5
    for wk in range(1, 16):
        d = SHARED[wk]
        ov = COHORTS[k].get(wk, {})
        _, wc, tue, fri, kind, note = CALENDAR[wk - 1]

        practical = d["practical"]
        if ov.get("practical_add"):
            practical = practical + "\n\nCOHORT " + k + " FRAMING: " + ov["practical_add"]
        prep = d["prep"]
        if ov.get("prep_add"):
            prep = prep + "\n" + B + "COHORT " + k + ": " + ov["prep_add"]
        dataset = ov.get("dataset", "Uses the cohort anchor dataset carried forward from Week 5 — see the Dataset Register.")
        if wk == 2:
            dataset = "None. A single small CSV is opened only to prove the environment works."
        if wk == 3:
            dataset = ov.get("dataset", "No dataset — formula-driven.")
        if wk == 13:
            dataset = "The team's own project dataset."

        fill = RED if d["phase"].startswith("ASSESSMENT") else (BAND if wk % 2 == 0 else None)
        if note and not d["phase"].startswith("ASSESSMENT"):
            fill = AMBER
        write_row(ws, r, [wk, d["phase"], wc,
                          (tue if m["day"] == "Tuesday" else fri) + f"\n{m['time']} · {m['room']}",
                          f"Cohort {k}",
                          m["code"], m["title"], d["topic"], d["los"],
                          structure_with_cp(wk, d["structure"]), d["concepts"], d["tools"], practical, dataset,
                          d["challenge"], d["assignment"], cp_text(wk), d["milestone"], d["assessrel"], prep,
                          d["resources"],
                          ov.get("divergence", "Largely shared — check the Shared vs Divergent sheet.")],
                  fill=fill, bold_first=True, heights=220)
        r += 1
    ws.freeze_panes = "H5"
    ws.auto_filter.ref = f"A4:V{r-1}"

# ==========================================================================
# 7. SHARED VS DIVERGENT
# ==========================================================================
ws = wb.create_sheet("Shared vs Divergent")
ws.sheet_properties.tabColor = "7030A0"
title_block(ws, "Shared core versus cohort-specific overlay",
            "Where one preparation serves three cohorts, and where three separate preparations are genuinely needed.", 6)
header_row(ws, 4, ["Week", "Topic", "Shared across all three cohorts (prepare once)",
                   "Must be re-skinned per cohort (prepare three times)",
                   "Approx. re-skin effort", "Cohort A / B / C divergence"],
           [7, 34, 62, 62, 20, 74])
DIVERGE = {
 1: ("Course contract, the rules-vs-learning argument, the Problem Hunt design, the gallery walk, team formation, A1 brief.",
     "The 12-row printed dataset extract, the two framing questions, the Problem Hunt prompt cards.", "Low — 1 hour each"),
 2: ("Everything. The tool map, the install clinic, terminal, notebook, Git, Kaggle, Break and Fix.",
     "Nothing beyond the one-line README prompt naming their programme.", "None"),
 3: ("All Python concepts, the function-library task design, the Wrong Answer Hunt format, the debugger demo.",
     "The six engineering formulas and the unit traps planted in the Wrong Answer Hunt.", "Medium — 2–3 hours each"),
 4: ("All collections, loops, file I/O and exception content. The Reading Report task. The Investigation Lab format and question bank.",
     "The ~300-row Investigation Lab file, its planted finding and its red herrings.", "High — 3–4 hours each"),
 5: ("All NumPy and pandas content. The loops-vs-pandas comparison. The Kaggle and UCI sourcing segment. The Ten Questions format.",
     "The anchor dataset, the twelve interrogation questions, and the dataset subsetting work (heavy for Cohort B).", "High — 4 hours each"),
 6: ("All cleaning and visualisation content. The Data Clinic design. The Outlier Argument format. Chart grammar.",
     "The damaged dataset with its six planted defects, and the five outlier cases.", "High — 4 hours each"),
 7: ("Format, duration, rules, offline bundle, rubric, invigilation plan, auto-check script, moderation plan.",
     "Three matched unseen dataset variants per cohort, with model answers and mark schemes. Nine variants in total.", "Very high — 6–8 hours each"),
 8: ("All regression, metric and baseline content. The fifteen-line demonstration structure. The leaderboard.",
     "The dataset, the target, the physical error unit, and the 'is it good enough' question.", "Low — 1–2 hours each"),
 9: ("All classification content. The cost-asymmetry framing. The 97% Trap design. The drawn decision tree.",
     "The dataset, the class definitions or banding decision, and the four cost categories.", "Medium — 2–3 hours each"),
 10: ("All validation, cross-validation and leakage content. The depth sweep. The Too Good To Be True format. PM1 review.",
      "The three planted leakage causes, dressed in the cohort's own terms.", "Medium — 2–3 hours each"),
 11: ("All encoding, scaling, ColumnTransformer, Pipeline, selection and ablation content. The Domain Advantage design.",
      "The feature set, the one demonstration feature that must beat the raw columns, and the standards reference sheet.", "Medium — 3 hours each"),
 12: ("The comparison protocol, the five selection criteria, the GridSearchCV demonstration, the defence round, the question bank.",
      "The challenge dataset and the fictional client brief with its real constraint.", "Medium — 2–3 hours each"),
 13: ("EVERYTHING. Repository structure, README standards, requirements.txt, restart-and-run-all, peer review, the clinic rotation.",
      "Nothing. This week is genuinely identical across all three cohorts.", "None"),
 14: ("Format, duration, rules, offline bundle, rubric, invigilation, auto-check script, moderation.",
      "Three matched unseen dataset variants per cohort. Nine variants in total.", "Very high — 6–8 hours each"),
 15: ("Demo fair format, viva bank structure, peer assessment form, recognition categories, reflection prompt, the Week 1 promise comparison.",
      "The project titles that emerge, and which external assessor to invite.", "Low — under 1 hour each"),
}
r = 5
for wk in range(1, 16):
    sh, dv_, eff = DIVERGE[wk]
    parts = []
    for k in ("A", "B", "C"):
        ov = COHORTS[k].get(wk, {})
        parts.append(f"[{k}] " + ov.get("divergence", "Largely shared."))
    fill = RED if SHARED[wk]["phase"].startswith("ASSESSMENT") else (BAND if wk % 2 == 0 else None)
    write_row(ws, r, [wk, SHARED[wk]["topic"], sh, dv_, eff, "\n".join(parts)],
              fill=fill, bold_first=True, heights=96)
    r += 1
r += 1
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
c = ws.cell(r, 1, "Reading of this sheet: the two assessment weeks and Weeks 4–7 carry almost all of the "
                  "triplicated preparation, because that is where the datasets must be authored. Weeks 2 and 13 "
                  "require no divergent preparation at all. Eighteen unseen test dataset variants are needed in "
                  "total — nine for each test, being three matched variants per cohort. Build the nine for Test 1 "
                  "during Weeks 2–5, and the nine for Test 2 during Weeks 8–12. Do not leave either set to the "
                  "fortnight before the test, when there will be no capacity.")
c.font = BODY_B; c.alignment = TOP; c.fill = PatternFill("solid", fgColor=LIGHT)
ws.row_dimensions[r].height = 46
ws.freeze_panes = "C5"

# ==========================================================================
# 8. ASSESSMENT
# ==========================================================================
ws = wb.create_sheet("Assessment")
ws.sheet_properties.tabColor = "C55A11"
title_block(ws, "Semester 1 assessment design",
            "Entirely practical, continuous and project-based. No traditional written examination. "
            "65% of the mark is individual; 35% is machine-marked.", 6)
r = 4
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
c = ws.cell(r, 1, "MODEL 1 — RECOMMENDED"); c.font = SEC_FONT; c.fill = SEC_FILL
ws.row_dimensions[r].height = 20
r += 1
header_row(ws, r, ["Component", "When", "Individual / team", "Weight", "Deliverable", "Marked against"],
           [42, 30, 34, 10, 54, 44])
r += 1
first = r
for comp, when, mode, wt, deliv, marked in ASSESSMENT:
    write_row(ws, r, [comp, when, mode, wt, deliv, marked], bold_first=True, heights=42)
    ws.cell(r, 4).number_format = "0%"
    ws.cell(r, 4).alignment = TOPC
    r += 1
last = r - 1
write_row(ws, r, ["TOTAL", "", "", f"=SUM(D{first}:D{last})", "", ""], fill=LIGHT, bold_first=True, heights=18)
ws.cell(r, 4).number_format = "0%"; ws.cell(r, 4).font = BODY_B; ws.cell(r, 4).alignment = TOPC
r += 1
write_row(ws, r, ["Of which individual", "", "",
                  f"=D{first}+D{first+1}+D{first+3}+D{first+4}+D{first+6}", "",
                  "Weekly quizzes, weekly challenges, both practical tests, and the demo/viva/reflection are "
                  "individually assessed."],
          fill=GREEN, bold_first=True, heights=26)
ws.cell(r, 4).number_format = "0%"; ws.cell(r, 4).alignment = TOPC
r += 1
write_row(ws, r, ["Of which team", "", "", f"=D{first+2}+D{first+5}", "",
                  "Team marks are moderated by the individual viva and the contribution log."],
          fill=AMBER, bold_first=True, heights=26)
ws.cell(r, 4).number_format = "0%"; ws.cell(r, 4).alignment = TOPC
r += 1
write_row(ws, r, ["Of which machine-marked", "", "",
                  f"=D{first}+D{first+1}+D{first+3}*0.4+D{first+4}*0.45", "",
                  "Weekly quizzes and weekly challenges in full, plus 40% of Test 1 and 45% of Test 2. Held "
                  "deliberately below half of the course mark — see the Assessment Tech Stack sheet."],
          fill=LIGHT, bold_first=True, heights=30)
ws.cell(r, 4).number_format = "0%"; ws.cell(r, 4).alignment = TOPC
r += 3

ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
c = ws.cell(r, 1, "MODEL 2 — ALTERNATIVE, if IUEA mandates a coursework / final assessment split"); c.font = SEC_FONT; c.fill = SEC_FILL
ws.row_dimensions[r].height = 20
r += 1
header_row(ws, r, ["Component", "When", "Individual / team", "Weight", "Note", ""], [42, 30, 34, 10, 54, 44])
r += 1
alt_rows = []
for comp, when, mode, wt, note in ALT_MODEL:
    if wt == "":
        write_row(ws, r, [comp, "", "", "", "", ""], fill=LIGHT, bold_first=True, heights=18)
    else:
        write_row(ws, r, [comp, when, mode, wt, note, ""], heights=20)
        ws.cell(r, 4).number_format = "0%"; ws.cell(r, 4).alignment = TOPC
        alt_rows.append(r)
    r += 1
write_row(ws, r, ["TOTAL", "", "", "=" + "+".join(f"D{x}" for x in alt_rows), "", ""],
          fill=LIGHT, bold_first=True, heights=18)
ws.cell(r, 4).number_format = "0%"; ws.cell(r, 4).font = BODY_B; ws.cell(r, 4).alignment = TOPC
r += 3

ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
c = ws.cell(r, 1, "DESIGN NOTES"); c.font = SEC_FONT; c.fill = SEC_FILL
ws.row_dimensions[r].height = 20
r += 1
notes = [
 ("Why two tests, not one", "The original curriculum sketch carried a single practical test. With the assessment weeks "
  "fixed at Weeks 7 and 14, two tests are available and they should examine different things: Week 7 certifies data "
  "literacy (can you investigate a dataset?) and Week 14 certifies end-to-end capability (can you build and defend a "
  "model?). Splitting them also means a student who struggles in October is not sunk."),
 ("Why the tests run offline", "It makes the AI policy enforceable without surveillance. AI assistance is permitted and "
  "actively taught in coursework, where students explain and defend their work; it is excluded from the two tests, "
  "which certify unaided capability. Students are told the reasoning in Week 6, not on the day."),
 ("Why 65% individual", "With teams of 4–5 and up to 22 teams in Cohort A, a team-heavy mark scheme would let a weak "
  "student pass on a strong teammate's work. Twelve individual quizzes, two individual tests, individually "
  "marked weekly challenges, and an individual viva make the team mark safe to award."),
 ("Why continuous assessment", "Twelve auto-graded weekly quizzes plus eleven auto-graded weekly submissions mean "
  "40% of the mark accumulates steadily rather than landing in two large events. Students get feedback in minutes, "
  "and the lecturer gets a weekly engagement signal across ~195 students that is otherwise invisible until the "
  "first test. See the 'Assessment Tech Stack' and 'Marking Load' sheets for how this is affordable for one person."),
 ("Why nothing rewards accuracy alone", "Across all six rubrics, method, reasoning, validation and interpretation carry "
  "far more weight than the score achieved. A student whose model performs poorly but who diagnoses why, and says so, "
  "should out-score a student who copies a Kaggle notebook to a better number. The Week 15 recognition categories "
  "reinforce this: there is no prize for highest accuracy."),
 ("Late, absent and resit policy", "To be aligned with IUEA regulations before Week 5. As a minimum, agree in advance: "
  "the penalty for late coursework, the procedure for a student who misses a test week with cause, and whether a resit "
  "practical is available. Publish it in the syllabus, not by announcement."),
 ("Moderation", "Sample-moderate 10% of every component, and 100% of any script within 3 marks of a grade boundary. "
  "Publish every rubric before the work is set — students should never meet a rubric for the first time in an assessment."),
]
for label, txt in notes:
    c = ws.cell(r, 1, label); c.font = BODY_B; c.alignment = TOP
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=6)
    c2 = ws.cell(r, 2, txt); c2.font = BODY; c2.alignment = TOP
    ws.row_dimensions[r].height = 52
    r += 1
ws.freeze_panes = "A4"

# ==========================================================================
# 9. RUBRICS
# ==========================================================================
ws = wb.create_sheet("Rubrics")
ws.sheet_properties.tabColor = "A9D08E"
title_block(ws, "Assessment rubrics", "Published to students before the work is set. Criterion weights sum to 100 by formula.", 4)
r = 4
for name, crits in RUBRICS.items():
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    c = ws.cell(r, 1, name); c.font = SEC_FONT; c.fill = SEC_FILL
    ws.row_dimensions[r].height = 20
    r += 1
    header_row(ws, r, ["Criterion", "Marks", "What earns the marks", "Marker note"], [34, 9, 96, 40], 22)
    r += 1
    first = r
    for crit, mk, desc in crits:
        write_row(ws, r, [crit, mk, desc, ""], bold_first=True, heights=44)
        ws.cell(r, 2).alignment = TOPC
        r += 1
    last = r - 1
    write_row(ws, r, ["TOTAL", f"=SUM(B{first}:B{last})", "", ""], fill=LIGHT, bold_first=True, heights=18)
    ws.cell(r, 2).font = BODY_B; ws.cell(r, 2).alignment = TOPC
    r += 2
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
c = ws.cell(r, 1, "Standing marker rule across every rubric: a student is marked on what they can explain. If a "
                  "submission contains work the student cannot account for in the viva or in the written reasoning "
                  "section, the mark is reduced to the portion they can explain. This is stated in the syllabus and "
                  "applied consistently, and it is what makes a permissive AI policy workable.")
c.font = BODY_B; c.alignment = TOP; c.fill = PatternFill("solid", fgColor=AMBER)
ws.row_dimensions[r].height = 48
ws.freeze_panes = "A4"

# ==========================================================================
# 10. TOOLS ROLLOUT
# ==========================================================================
ws = wb.create_sheet("Tools Rollout")
ws.sheet_properties.tabColor = "4472C4"
title_block(ws, "Tool rollout — every tool introduced by the problem it solves",
            "No tool is named before the problem that needs it. This is what prevents tool fatigue.", 5)
header_row(ws, 4, ["Tool", "Week introduced", "What problem does this tool solve?", "First use in class",
                   "Notes and cautions"], [34, 14, 56, 40, 76])
r = 5
for tool, wk, prob, first_use, note in sorted(TOOLS, key=lambda x: (x[1], x[0])):
    write_row(ws, r, [tool, wk, prob, first_use, note], fill=BAND if r % 2 == 0 else None,
              bold_first=True, heights=34)
    ws.cell(r, 2).alignment = TOPC
    r += 1
r += 1
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
c = ws.cell(r, 1, "Deliberately NOT in Semester 1: deep learning, PyTorch, OpenCV, transfer learning, time-series "
                  "forecasting, RAG, agents, MLOps, FastAPI, cloud deployment. All are Semester 2. Students are told "
                  "this explicitly and told why: a beginner who meets ten tools learns none of them.")
c.font = BODY_B; c.alignment = TOP; c.fill = PatternFill("solid", fgColor=LIGHT)
ws.row_dimensions[r].height = 40
ws.freeze_panes = "A5"

# ==========================================================================
# 11. DATASET REGISTER
# ==========================================================================
ws = wb.create_sheet("Dataset Register")
ws.sheet_properties.tabColor = "BF8F00"
title_block(ws, "Dataset register",
            "Stage every dataset on the local share at the start of the semester. Never fetch live in class.", 8)
header_row(ws, 4, ["Dataset", "Cohort(s)", "Host / identifier", "Licence", "Size", "Task",
                   "Weeks used", "Status"], [46, 12, 44, 26, 42, 42, 16, 22])
r = 5
for row in DATASETS:
    st = row[7]
    fill = GREEN if st.startswith("VERIFIED") else (AMBER if st.startswith("VERIFY") else RED)
    write_row(ws, r, list(row), fill=fill, bold_first=True, heights=32)
    ws.cell(r, 2).alignment = TOPC
    ws.cell(r, 7).alignment = TOPC
    r += 1
r += 1
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
c = ws.cell(r, 1, "Status key:  green = existence and licence confirmed 1 Sep 2026 ·  amber = named from knowledge, "
                  "NOT confirmed, verify before use ·  red = course material that does not exist yet and must be "
                  "authored, with the week it is needed. The red rows are the real preparation workload of this "
                  "semester and should be scheduled now.")
c.font = BODY_B; c.alignment = TOP; c.fill = PatternFill("solid", fgColor=LIGHT)
ws.row_dimensions[r].height = 44
ws.freeze_panes = "A5"

# ==========================================================================
# 11b. ASSESSMENT TECH STACK
# ==========================================================================
ws = wb.create_sheet("Assessment Tech Stack")
ws.sheet_properties.tabColor = "00B050"
title_block(ws, "Assessment technology stack — five layers, all free",
            "Built and tested. The working code is in the assessment-tools folder alongside this workbook.", 6)
header_row(ws, 4, ["Layer", "Purpose", "Tool", "Cost", "What it removes", "Verified limits and cautions"],
           [26, 50, 44, 22, 56, 76])
r = 5
for row in TECH_STACK:
    fill = RED if row[0].startswith("What is NOT") else (BAND if r % 2 == 0 else None)
    write_row(ws, r, list(row), fill=fill, bold_first=True, heights=110)
    r += 1
r += 1
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
c = ws.cell(r, 1, "Design principle: auto-grading is used on the HIGH-VOLUME, LOW-STAKES work, and human marking is "
                  "concentrated on the reasoning. Machine-marked marks total 35% of the course (quizzes 10, "
                  "challenges 10, 40% of Test 1, 45% of Test 2), and that share is capped deliberately. The 25% "
                  "project, the 10% viva and the reasoning halves of both tests — 65% of the course — assess "
                  "engineering judgement, and no auto-grader can read them.")
c.font = BODY_B; c.alignment = TOP; c.fill = PatternFill("solid", fgColor=LIGHT)
ws.row_dimensions[r].height = 46
ws.freeze_panes = "B5"

# ==========================================================================
# 11c. MARKING LOAD
# ==========================================================================
ws = wb.create_sheet("Marking Load")
ws.sheet_properties.tabColor = "ED7D31"
title_block(ws, "Marking load — fully human versus the auto-graded stack",
            "Per semester, at ~195 students and 43 teams. This is the answer to 'can one lecturer assess 195 students?'", 6)
header_row(ws, 4, ["Item", "Volume", "Min. each", "Hours if all human", "Hours with the stack",
                   "How the saving is made"], [40, 30, 12, 18, 18, 76])
r = 5
first_ml = r
for item, vol, mins, before, after, how in MARKING_LOAD:
    fill = GREEN if after < before else (BAND if r % 2 == 0 else None)
    write_row(ws, r, [item, vol, mins, before, after, how], fill=fill, bold_first=True, heights=34)
    for col in (3, 4, 5):
        ws.cell(r, col).alignment = TOPC
    r += 1
last_ml = r - 1
write_row(ws, r, ["TOTAL (hours per semester)", "", "", f"=SUM(D{first_ml}:D{last_ml})",
                  f"=SUM(E{first_ml}:E{last_ml})", "Roughly 16 hours a week becomes roughly 8."],
          fill=LIGHT, bold_first=True, heights=20)
for col in (4, 5):
    ws.cell(r, col).font = BODY_B; ws.cell(r, col).alignment = TOPC
r += 1
write_row(ws, r, ["Hours saved per semester", "", "", "", f"=D{r-1}-E{r-1}",
                  "And the saving repeats every semester, while the authoring cost does not."],
          fill=GREEN, bold_first=True, heights=20)
ws.cell(r, 5).font = BODY_B; ws.cell(r, 5).alignment = TOPC
r += 2
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
c = ws.cell(r, 1, "ONE-OFF AUTHORING COST: " + AUTHORING_ONE_OFF)
c.font = BODY_B; c.alignment = TOP; c.fill = PatternFill("solid", fgColor=AMBER)
ws.row_dimensions[r].height = 32
r += 2
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
c = ws.cell(r, 1, "The honest reading of this sheet: the QR quizzes are NOT where the saving comes from — they "
                  "cost nothing to mark, but they were never the problem. The problem was ~2,145 weekly practical "
                  "submissions, and it is Layer B, the notebook auto-grader, that removes about 97 hours of it. "
                  "The quizzes do something different and also valuable: they give students instant feedback, "
                  "they give you a weekly engagement signal across ~195 students you cannot otherwise see, and they "
                  "let assessment weight move away from work that is expensive to mark. Both are worth having. "
                  "Only one of them fixes the workload.")
c.font = BODY; c.alignment = TOP
ws.row_dimensions[r].height = 62
ws.freeze_panes = "B5"

# ==========================================================================
# 12. RISK REGISTER
# ==========================================================================
ws = wb.create_sheet("Risk Register")
ws.sheet_properties.tabColor = "C00000"
title_block(ws, "Risk register", "Twelve delivery risks. R1, R2 and R3 require action in the first fortnight.", 6)
header_row(ws, 4, ["ID", "Risk", "Likelihood", "Impact", "Mitigation", "Owner"],
           [7, 62, 14, 12, 96, 26])
r = 5
for rid, risk, lik, imp, mit, own in RISKS:
    fill = RED if imp == "High" else (AMBER if imp == "Medium" else None)
    write_row(ws, r, [rid, risk, lik, imp, mit, own], fill=fill, bold_first=True, heights=72)
    ws.cell(r, 3).alignment = TOPC
    ws.cell(r, 4).alignment = TOPC
    r += 1
ws.freeze_panes = "B5"

wb.save(OUT)
print("saved", OUT)
