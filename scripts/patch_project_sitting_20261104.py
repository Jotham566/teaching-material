"""Patch the wording about the Engineering ML project for the lecturer decision of 4 November 2026:

  * the project is INDIVIDUAL, TIMED (one supervised 3-hour sitting in the Week 12 class slot, in Google Colab, entered and submitted like Practical Test 1)
    and fully AUTO-GRADED (Part A coded notebook /30, Part B structured decision memo form /15). No demo, no clinic, no take-home, no upload form;
  * proposed sitting slots (always 'proposed, lecturer to confirm'): CML3112 Tue 1 Dec 11:00-14:00, CML3113 Fri 4 Dec 08:00-11:00, CML3111 Fri 4 Dec 11:00-14:00;
  * an unmarked rehearsal is released after Class 4 (CML3112 Tue 24 Nov, CML3113 and CML3111 Fri 27 Nov).

Files patched: Block_Assessment_Arrangement_2026-11-03.md, data/assessment_blocks_20261103.json, the three student_guides/<cohort>/ML_PROJECT.md,
the three syllabus .docx, the master teaching plan .docx and .xlsx (PDFs are regenerated where one sits next to the docx).
Safety rules (as in patch_docx_20261103.py): every original is copied once into a _backup_2026-11-04 folder next to it before it is written; every replacement
asserts its match count and nothing is written if one is wrong; a file that already carries the marker is reported 'already patched' and left alone.
Usage: python3 scripts/patch_project_sitting_20261104.py [--dry-run] [--learn]    (--learn prints the match counts instead of asserting them)
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import docx
import openpyxl

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "IUEA_Teaching_Plan"
DRY = "--dry-run" in sys.argv
LEARN = "--learn" in sys.argv
MARK = "PROJECT_SITTING_20261104"
BACKUP = "_backup_2026-11-04"
PROPOSED = "proposed, lecturer to confirm"
SIT = {
    "CML3112": dict(day="Tuesday 1 December", long="Tuesday 1 December 2026", start="11:00", end="14:00", rehearsal="Tuesday 24 November", short="Tue 1 Dec"),
    "CML3113": dict(day="Friday 4 December", long="Friday 4 December 2026", start="08:00", end="11:00", rehearsal="Friday 27 November", short="Fri 4 Dec"),
    "CML3111": dict(day="Friday 4 December", long="Friday 4 December 2026", start="11:00", end="14:00", rehearsal="Friday 27 November", short="Fri 4 Dec"),
}
SYLLABUS = {"IUEA_ML_Syllabus_CohortA_Design_and_Infrastructure.docx": "CML3112", "IUEA_ML_Syllabus_CohortB_Mining_and_Petroleum.docx": "CML3113",
            "IUEA_ML_Syllabus_CohortC_Engineering.docx": "CML3111"}
ALL_SLOTS = "CML3112 Tue 1 Dec 11:00 to 14:00, CML3113 Fri 4 Dec 08:00 to 11:00, CML3111 Fri 4 Dec 11:00 to 14:00"
TIMED = "one supervised 3-hour sitting in Google Colab, entered and submitted like Practical Test 1 (portal start, personal deadline, countdown, Submit test cell, then the Google Form)"
PART_A = "Part A, the coded project notebook (30 marks, hidden checks on data you have not seen)"
PART_B = "Part B, a structured decision memo form inside the notebook (15 marks: your recommended model, your validation and test numbers, three limits and a next step chosen from lists, and two short written answers)"
FLAG_SENTENCE = "The lecturer gets a short spot-check list of flagged cases (identity mismatch, copied code, identical written answers, an edited supplied cell, a test set opened twice); a flag never lowers a mark by itself."

report = []   # (file, rule id, count)


def backup(path):
    path = Path(path)
    dest_dir = path.parent / BACKUP
    dest_dir.mkdir(exist_ok=True)
    dest = dest_dir / path.name
    if not dest.exists():
        shutil.copy2(path, dest)
    return dest


# ------------------------------------------------------------------------------------------------ text rules
def syllabus_rules(code):
    s = SIT[code]
    when = f"{s['long']}, {s['start']} to {s['end']} Kampala time; {PROPOSED}"
    return [
        ("calendar", f"Week 12 is a project clinic ({s['day']} for your cohort), with supervised work and questions and no demo, which is where the semester ends. The Engineering ML project is released after Class 4 and is due Friday 11 December 2026, 23:59 Kampala (proposed, lecturer to confirm).",
         f"Week 12 is the project sitting ({when}), a supervised 3-hour individual sitting that is timed and marked automatically, which is where the semester ends. An unmarked rehearsal of the project is released after Class 4 ({s['rehearsal']} 2026; {PROPOSED})."),
        ("individual", "Forty-five per cent of the mark is individual: the quizzes, the assignments and Practical Test 1. The Engineering ML project (45 per cent) is a take-home graded like Practical Test 1; whether it is done individually or in teams is to be confirmed by the lecturer.",
         "Ninety per cent of the mark is individual: the quizzes, the assignments, Practical Test 1 and the Engineering ML project (45 per cent), which is one supervised 3-hour timed sitting in Week 12 and is marked automatically like Practical Test 1."),
        ("marked", "is auto-graded and also marked against a rubric, in the way Practical Test 1 is marked. Part B, a one-page decision memo (15 marks), is marked against a rubric. The criterion-level rubrics and the split of Part A between automatic checks and rubric marks are to be confirmed by the lecturer and will be published before the project is released.",
         "is auto-graded by hidden checks on data you have not seen, in the way Practical Test 1 is marked. Part B, a structured decision memo form inside the notebook (15 marks), is also marked automatically: the model you recommend, your validation and test numbers, three limits and a next step chosen from lists, and two short answers checked by keyword and length rules. No person marks your notebook by hand. The mark scheme is published before the rehearsal."),
        ("rubric_publication", "The project rubrics are to be confirmed by the lecturer and will be published before the project is released.", "The project mark scheme (the Part A checks and the Part B form rules) is published before the rehearsal is released."),
        ("teams", "Whether the Engineering ML project is done in teams or individually is to be confirmed by the lecturer.", "The Engineering ML project is individual."),
        ("nodemo", "There is no demo, no live defence and no reflection mark. If the project is done in teams, how each member's contribution is recorded is to be confirmed by the lecturer. Whatever is set, an individual mark stays separate from shared project marks.",
         "There is no demo, no live defence and no reflection mark. The Engineering ML project is individual, so each student's project mark is their own and stays separate from shared team marks."),
        ("ai", "In Practical Test 1, AI assistance is prohibited. Test 1 is a take-home practical followed by an understanding check, in which you may",
         "In Practical Test 1 and in the Engineering ML project sitting, AI assistance is prohibited. Each is a timed Colab practical followed by an understanding check, in which you may"),
        ("demo_visible", "the questions at the Week 12 demo make the difference visible", "the understanding check makes the difference visible"),
        ("section7", "You submit the project as a take-home, graded like Practical Test 1. It covers only what was taught in Weeks 1 to 11. It is released after Class 4 and is due Friday 11 December 2026, 23:59 Kampala (proposed, lecturer to confirm). Week 12 is a project clinic: supervised work and questions, and no demo. The project has two parts: Part A, the coded project notebook (30 marks, auto-graded plus a rubric, like Practical Test 1), and Part B, a one-page decision memo (15 marks, rubric).",
         f"You sit the project alone, as {TIMED}, in Week 12 ({when}). It is marked automatically and covers only what was taught in Weeks 1 to 11. An unmarked rehearsal version, with a practice dataset and no solved walk-through, is released after Class 4 ({s['rehearsal']} 2026; {PROPOSED}). Each student receives one of three data variants, allocated at random. The project has two parts: {PART_A}, and {PART_B}. {FLAG_SENTENCE}"),
        ("open_test", "open the sealed test group once", "open the test set once"),
        ("alone", "Whether you work alone or in a team, and whether you may choose your own problem, is to be confirmed by the lecturer.", "You work alone, and the problem is the one in the notebook for your cohort."),
        ("table_mode", "Take-home submission; individual or team: to be confirmed by the lecturer", "Individual, timed 3-hour sitting in Week 12, auto-graded"),
        ("table_parts", "Part A, the coded project notebook (30 marks, auto-graded plus a rubric, like Practical Test 1), and Part B, a one-page decision memo (15 marks, rubric). It covers only what was taught in Weeks 1 to 11. Rubrics and the split of Part A between automatic checks and rubric marks are to be confirmed by the lecturer.",
         "Part A, the coded project notebook (30 marks, hidden checks on unseen data), and Part B, a structured decision memo form inside the notebook (15 marks, automatic). It covers only what was taught in Weeks 1 to 11. Everything is marked automatically."),
        ("table_when", "Brief in Class 4 (Week 11 content); released after Class 4; due Fri 11 Dec 2026 23:59 (proposed, lecturer to confirm)",
         f"Brief in Class 4 (Week 11 content); rehearsal released after Class 4; sitting in Week 12 ({s['short']} {s['start']} to {s['end']}; {PROPOSED})"),
        ("ai_declaration", "AI-use declaration in the project", "No AI in the project sitting (the Practical Test 1 rule)"),
        ("version", "3 November 2026 to remove the demo and make the project a submission", "3 November 2026 to remove the demo and 4 November 2026 to make the project an individual, timed, auto-graded sitting"),
        ("header", "(Week 12 project clinic)", "(Week 12 project sitting)"),
        ("class4", "Class 4 · Features, choosing a model and the project brief", "Class 4 · Features, choosing a model and the project brief; rehearsal released after the class"),
        ("week12_row", "Project clinic (supervised work and questions; no demo)", "Project sitting (3 hours, individual, timed, auto-graded)"),
        ("week12_head", "The clinic", "The sitting", "whole"),
        ("week12_text", "Supervised work on the Engineering ML project, and questions. Block 2 pack (A9, A10, A11) closes", "The Engineering ML project sitting: 3 hours, individual, timed, auto-graded, in Google Colab. Block 2 pack (A9, A10, A11) closes"),
        ("week12_due", "The project is due Fri 11 Dec 2026 23:59 (proposed, lecturer to confirm).", f"The sitting is {s['short']} {s['start']} to {s['end']} ({PROPOSED})."),
    ]


MASTER_RULES = [
    ("m_arch", "which end with the Week 12 project clinic", "which end with the Week 12 project sitting"),
    ("m_end", "ending at the Week 12 project clinic (Tuesday 1 December for CML3112, Friday 4 December for CML3113 and CML3111)",
     f"ending at the Week 12 project sitting (CML3112 Tuesday 1 December 11:00 to 14:00, CML3113 Friday 4 December 08:00 to 11:00, CML3111 Friday 4 December 11:00 to 14:00; {PROPOSED})"),
    ("m_demo_removed", "the Engineering ML project is submitted instead, due Friday 11 December 2026, 23:59 Kampala (proposed, lecturer to confirm).",
     f"the Engineering ML project is an individual, timed, auto-graded 3-hour sitting in Week 12 instead ({PROPOSED})."),
    ("m_block4", "Block 4 · Week 12 · Project clinic", "Block 4 · Week 12 · Project sitting"),
    ("m_week12", "is a project clinic. There is no demo and nobody presents. Students work on the Engineering ML project with supervision and ask questions. The project is a take-home that they submit, graded like Practical Test 1. It covers only Weeks 1 to 11, is released after Class 4 and is due Friday 11 December 2026, 23:59 Kampala (proposed, lecturer to confirm). It has two parts: Part A, the coded project notebook (30 marks, auto-graded plus a rubric, like Practical Test 1), and Part B, a one-page decision memo (15 marks, rubric).",
     f"is the project sitting: {TIMED}, in the class slot ({ALL_SLOTS}; {PROPOSED}). It is individual, timed and auto-graded, with no demo and no presentation, and covers only Weeks 1 to 11. An unmarked rehearsal (practice notebook and practice dataset, no solved walk-through) is released after Class 4. Each student receives one of three data variants. It has two parts: {PART_A}, and {PART_B}. {FLAG_SENTENCE}"),
    ("m_week12_tail", "the sealed test group opened once, and the memo. The rubrics, the split inside Part A, whether students work alone or in teams, the clinic room and helpers, and any reproducibility check are to be confirmed by the lecturer.",
     "the test set opened once, and the memo form. The room, invigilation, power and network arrangements for the sitting, and the form windows, are to be confirmed by the lecturer."),
    ("m_take_home", "a take-home that students submit", "a timed, auto-graded sitting that each student takes alone"),
    ("m_individual", "Forty-five per cent of the mark is individual on the component modes in the table above (the quizzes, the assignments and Practical Test 1). The Data Analysis Project (10 per cent) is a team mark. The Engineering ML project (45 per cent) is a take-home graded like Practical Test 1, and whether it is done individually or in teams is to be confirmed by the lecturer.",
     "Ninety per cent of the mark is individual on the component modes in the table above (the quizzes, the assignments, Practical Test 1 and the Engineering ML project). The Data Analysis Project (10 per cent) is a team mark. The Engineering ML project (45 per cent) is an individual, timed, auto-graded 3-hour sitting in Week 12."),
    ("m_individual2", "a project that is submitted and partly auto-graded", "an individual, fully auto-graded project sitting"),
    ("m_fourth", "which rests on the forty-five per cent individual mark (the quizzes, the assignments and Practical Test 1), the contribution log with repository evidence, and the way individual work on the project is recorded (to be confirmed by the lecturer).",
     "which rests on the ninety per cent individual mark (the quizzes, the assignments, Practical Test 1 and the Engineering ML project, which is sat alone), and the contribution log with repository evidence for the Data Analysis Project."),
    ("m_crowd", "The Week 12 project clinic brings a whole cohort, up to about a hundred students in Cohort A, into one session of supervised work and questions, so its room, helpers and running arrangements are to be confirmed by the lecturer.",
     "The Week 12 project sitting puts a whole cohort, up to about a hundred students in Cohort A, into one supervised 3-hour Colab sitting, so its room, invigilators, power and network arrangements are to be confirmed by the lecturer."),
    ("m_class4", "project released (due Fri 11 Dec 2026 23:59 (proposed, lecturer to confirm))", f"rehearsal version released (project sitting in Week 12; {PROPOSED})"),
    ("m_class4b", "the project is released after Class 4 and due Friday 11 December 2026, 23:59 Kampala (proposed, lecturer to confirm)", f"an unmarked rehearsal is released after Class 4 and the project is sat in Week 12 ({PROPOSED})"),
    ("m_released_after", "Released after this class; due Friday 11 December 2026, 23:59 Kampala (proposed, lecturer to confirm). Week 12 is a project clinic.", f"Rehearsal released after this class; the project sitting is in Week 12 (3 hours, individual, timed, auto-graded; {PROPOSED})."),
    ("m_introduced", "released after it; it is due Friday 11 December 2026, 23:59 Kampala (proposed, lecturer to confirm).", f"a rehearsal version is released after it, and the project is sat in Week 12 ({PROPOSED})."),
    ("m_table_mode", "Take-home submission, graded like Practical Test 1 (Part A /30, Part B /15); individual or team: to be confirmed by the lecturer", "Individual, timed 3-hour sitting, auto-graded (Part A /30, Part B /15)"),
    ("m_table_when", "Brief in Class 4 (Week 11 content); released after Class 4; due Fri 11 Dec 2026 23:59 (proposed, lecturer to confirm)", f"Brief in Class 4 (Week 11 content); rehearsal released after Class 4; sitting in the Week 12 class slot ({ALL_SLOTS}; {PROPOSED})"),
    ("m_week12_row", "Week 12: project clinic (supervised work and questions; no demo).", "Week 12: project sitting (3 hours, individual, timed, auto-graded; no demo)."),
    ("m_week12_due", "The Engineering ML project is due Fri 11 Dec 2026 23:59 (proposed, lecturer to confirm).", f"The project sitting is in this class slot ({PROPOSED})."),
    ("m_week12_due2", "The Engineering ML Project is due Friday 11 December 2026, 23:59 Kampala (proposed, lecturer to confirm). Clinic arrangements: to be confirmed by the lecturer.",
     f"The Engineering ML Project sitting is in this class slot ({PROPOSED}). Sitting arrangements: to be confirmed by the lecturer."),
    ("m_clinic_whole", "Clinic", "Sitting", "whole"),
    ("m_brief", "The project is released after Class 4 and is due Friday 11 December 2026, 23:59 Kampala (proposed, lecturer to confirm). The rubrics, the split inside Part A and team or individual work are to be confirmed by the lecturer.",
     f"An unmarked rehearsal is released after Class 4 and the project is sat in Week 12 ({PROPOSED}). Part A and Part B are both marked automatically, and the project is individual."),
    ("m_arrange", "Week 12 project clinic arrangements: room, helpers and supervision", "Week 12 project sitting arrangements: room, invigilators, power and network"),
    ("m_row_a", "Project brief given; project released (due Fri 11 Dec 2026 23:59 (proposed, lecturer to confirm))", f"Project brief given; rehearsal version released (project sitting in Week 12; {PROPOSED})"),
    ("m_row_b", "Project clinic (no demo)", "Project sitting (individual, timed, auto-graded; no demo)"),
    ("m_row_c", "No demo. The Engineering ML project is due Fri 11 Dec 2026 23:59 (proposed, lecturer to confirm)", f"No demo. The Engineering ML project is a 3-hour individual sitting in this class slot ({PROPOSED})"),
    ("m_ai_declaration", "AI-use declaration in the project", "No AI in the project sitting (the Practical Test 1 rule)"),
    ("m_version_note", "3 November 2026 to remove the demo and make the project a submission", "3 November 2026 to remove the demo and 4 November 2026 to make the project an individual, timed, auto-graded sitting"),
    ("m_week12_calendar", "Week 12 is the project clinic (no demo).", "Week 12 is the project sitting (3 hours, individual, timed, auto-graded; no demo)."),
    ("m_week12_calendar2", "Week 12 is the project clinic", "Week 12 is the project sitting"),
    ("m_week12_cal3", "Project Clinic", "Project Sitting"),
    ("m_readme", "teaching, assessment and clinic weeks marked", "teaching, assessment and project sitting weeks marked"),
    ("m_clinic_week", "Clinic week: 1 (Week 12).", "Project sitting week: 1 (Week 12)."),
    ("m_green", "green = project clinic week", "green = project sitting week"),
    ("m_projectclinic", "Project clinic (supervised work and questions; no demo)", "Project sitting (3 hours, individual, timed, auto-graded)"),
    ("m_xl_h16", "Week 12: project clinic (supervised work and questions; no demo). ", "Week 12: project sitting (3 hours, individual, timed, auto-graded; no demo). "),
    ("m_xl_i16", "The clinic: supervised work on the project, and questions. No demo. Room and helpers: to be confirmed by the lecturer.", "The sitting: 3 hours, individual, timed, auto-graded, in Google Colab. No demo. Room and invigilators: to be confirmed by the lecturer."),
    ("m_xl_rubrics16", "Project clinic. The Engineering ML Project is due Friday 11 December 2026, 23:59 Kampala (proposed, lecturer to confirm).", f"Project sitting. The Engineering ML Project is sat in this class slot ({PROPOSED})."),
    ("m_xl_m16", "Rubrics: to be confirmed by the lecturer.", "Both parts are marked automatically; the lecturer reviews a short spot-check list."),
    ("m_xl_n16", "Clinic arrangements (room, helpers): to be confirmed by the lecturer.", "Sitting arrangements (room, invigilators, power, network): to be confirmed by the lecturer."),
    ("m_xl_t15", "Week 12 project demo arrangements (format, order, marks, mark scheme): to be confirmed by the lecturer.", "Week 12 project sitting arrangements (room, network, rehearsal notebook shared, form windows): to be confirmed by the lecturer."),
    ("m_xl_a2", "45% of the mark is individual on the component modes below (quizzes, assignments and Practical Test 1); the Engineering ML project is a take-home graded like Practical Test 1 and whether it is individual or in teams is to be confirmed by the lecturer;",
     "90% of the mark is individual on the component modes below (quizzes, assignments, Practical Test 1 and the Engineering ML project, an individual timed 3-hour sitting that is auto-graded);"),
    ("m_xl_c10", "Individual or team: to be confirmed by the lecturer", "Individual, timed Colab sitting, 3h, auto-graded", "whole"),
    ("m_xl_b25", "Due Fri 11 Dec 2026 23:59 (proposed, lecturer to confirm)", f"Week 12 class slot ({PROPOSED})", "whole"),
    ("m_xl_e10", "Take-home submission covering Weeks 1 to 11 only. Part A: coded project notebook, 30 marks, auto-graded plus rubric, like Practical Test 1. Part B: one-page decision memo, 15 marks, rubric. Rubrics and the split inside Part A: to be confirmed by the lecturer. No demo.",
     "Individual timed sitting (3 hours, Google Colab, entered and submitted like Practical Test 1) covering Weeks 1 to 11 only. Part A: coded project notebook, 30 marks, hidden checks on unseen data. Part B: structured decision memo form inside the notebook, 15 marks, checked automatically. Unmarked rehearsal released after Class 4; three data variants. No demo."),
    ("m_xl_f10", "Project rubric (see Rubrics sheet)", "Automatic: hidden checks (Part A) and form rules (Part B); see Rubrics sheet", "whole"),
    ("m_xl_a12", "Of which individual (quizzes, assignments, Practical Test 1)", "Of which individual (quizzes, assignments, Practical Test 1, Engineering ML project)", "whole"),
    ("m_xl_f12", "Quizzes, assignments and Practical Test 1 are individually assessed. The Engineering ML project (45%) is counted in neither line: individual or team is to be confirmed by the lecturer.",
     "Quizzes, assignments, Practical Test 1 and the Engineering ML project (45%) are individually assessed."),
    ("m_xl_a32", "Why 45% individual", "Why 90% individual", "whole"),
    ("m_xl_b30", "End-to-end capability is now shown in the Block 2 assignment, the quizzes and the Engineering ML project, a take-home that students submit.",
     "End-to-end capability is now shown in the Block 2 assignment, the quizzes and the Engineering ML project, a timed, auto-graded sitting that each student takes alone."),
    ("m_xl_b32", "Individual quizzes, an individual test and individually marked assignments provide individual evidence alongside shared project marks. The project is a take-home graded like Practical Test 1; individual or team is to be confirmed by the lecturer.",
     "Individual quizzes, an individual test, individually marked assignments and an individual, auto-graded Engineering ML sitting provide individual evidence alongside the shared Data Analysis Project mark."),
    ("m_xl_a4", "criterion marks to be confirmed by the lecturer", "all marks automatic (Part A hidden checks, Part B form rules)"),
    ("m_xl_f9", "Take-home project, Part A auto-graded plus rubric, Part B rubric. Marking time: to be confirmed by the lecturer (teams or individuals).",
     "Individual timed sitting, Part A and Part B both auto-graded. Marking time is the grading run plus a short spot-check list review (the lecturer confirms the time)."),
    ("m_xl_sv_b16", "Short project demo (Week 12; proposal, not final)", "Project sitting (Week 12, 3 hours, individual, timed, auto-graded; proposal, not final)", "whole"),
    ("m_xl_sv_c16", "Demo format, running order and mark scheme: to be confirmed by the lecturer.", "Sitting arrangements and form windows: to be confirmed by the lecturer.", "whole"),
    ("m_xl_sv_f16", "SHARED: demo format.", "SHARED: sitting format."),
    ("m_xl_r21", "Week 12 is a project clinic, which gives one more session of supervised project work.", "Week 12 is the project sitting, a fixed 3-hour slot that is not available as spare teaching time."),
    ("m_xl_a30", "an individual test and", "an individual test and"),
]
MASTER_RULES = [r for r in MASTER_RULES if r[1] != r[2]]


def run_rules(text, rules, counts):
    for rule in rules:
        rid, old, new = rule[0], rule[1], rule[2]
        mode = rule[3] if len(rule) > 3 else "sub"
        if mode == "whole":
            if text.strip() == old:
                text = new
                counts[rid] = counts.get(rid, 0) + 1
        else:
            n = text.count(old)
            if n:
                text = text.replace(old, new)
                counts[rid] = counts.get(rid, 0) + n
    return text


# ------------------------------------------------------------------------------------------------ docx
def para_set(p, text):
    if p.runs:
        p.runs[0].text = text
        for r in p.runs[1:]:
            r.text = ""
    else:
        p.add_run(text)


def all_paragraphs(d):
    seen = set()
    out = []

    def walk(container):
        for p in container.paragraphs:
            if p._p not in seen:
                seen.add(p._p)
                out.append(p)
        for t in container.tables:
            for row in t.rows:
                for c in row.cells:
                    walk(c)
    walk(d)
    for s in d.sections:
        for part in (s.header, s.footer):
            walk(part)
    return out


def patch_docx(path, rules, expect):
    path = Path(path)
    d = docx.Document(path)
    if MARK in (d.core_properties.keywords or ""):
        print(f"already patched: {path.name}")
        return
    counts = {}
    for p in all_paragraphs(d):
        text = p.text
        if not text.strip():
            continue
        new = run_rules(text, rules, counts)
        if new != text:
            # a paragraph with several runs keeps the first run's formatting
            para_set(p, new)
    finish(path.name, counts, expect, rules)
    if not DRY and not LEARN:
        backup(path)
        d.core_properties.keywords = ((d.core_properties.keywords or "") + " " + MARK).strip()
        d.save(path)
        print(f"patched {path.name}")


def finish(name, counts, expect, rules):
    for rid, n in sorted(counts.items()):
        print(f"  {name}: {rid} x{n}")
        report.append((name, rid, n))
    if LEARN:
        return
    exp = expect or {}
    assert counts == exp, f"{name}: match counts differ.\n expected {exp}\n found    {counts}"


def patch_xlsx(path, rules, expect):
    path = Path(path)
    wb = openpyxl.load_workbook(path)
    if MARK in (wb.properties.keywords or ""):
        print(f"already patched: {path.name}")
        return
    counts = {}
    for ws in wb:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and not c.value.startswith("="):
                    new = run_rules(c.value, rules, counts)
                    if new != c.value:
                        c.value = new
    ws = wb["Assessment"]
    assert ws["D12"].value == "=D6+D7+D9", ws["D12"].value
    ws["D12"].value = "=D6+D7+D9+D10"
    finish(path.name, counts, expect, rules)
    if not DRY and not LEARN:
        backup(path)
        wb.properties.keywords = ((wb.properties.keywords or "") + " " + MARK).strip()
        wb.save(path)
        print(f"patched {path.name}")


# ------------------------------------------------------------------------------------------------ markdown and json
def replace_once(text, old, new, label):
    assert text.count(old) == 1, f"{label}: expected 1 match, found {text.count(old)}: {old[:70]!r}"
    return text.replace(old, new)


def patch_arrangement():
    path = BASE / "Block_Assessment_Arrangement_2026-11-03.md"
    t = path.read_text()
    if MARK in t:
        print(f"already patched: {path.name}")
        return
    t = replace_once(t, "- The Engineering ML project stays. Students submit it as a take-home, graded like Practical Test 1. It covers only what was taught this semester (Weeks 1 to 11).",
                     "- The Engineering ML project stays. Update of 4 November 2026: it is INDIVIDUAL, TIMED and fully AUTO-GRADED. Each student sits it once, alone, in one supervised 3-hour sitting in Google Colab, entered and submitted like Practical Test 1. It covers only what was taught this semester (Weeks 1 to 11).", "intro")
    t = replace_once(t, "- Week 12 is a project clinic: supervised work and questions. Nobody presents. The class dates are the same as before (CML3112 Tue 1 Dec, CML3113 and CML3111 Fri 4 Dec).",
                     f"- Week 12 is the project sitting (3 hours, individual, timed, auto-graded) in the class slot: CML3112 Tue 1 Dec 11:00 to 14:00, CML3113 Fri 4 Dec 08:00 to 11:00, CML3111 Fri 4 Dec 11:00 to 14:00 ({PROPOSED}). Nobody presents and there is no clinic. An unmarked rehearsal (practice notebook and practice dataset, same structure, no solved walk-through) is released right after Class 4.", "week12")
    t = replace_once(t, "| A | Coded project notebook | 30 | Auto-graded checks plus a rubric, as for Practical Test 1 |", "| A | Coded project notebook | 30 | Auto-graded: hidden checks on unseen data, plus automatic checks of the process (test set opened once, no data leakage, seed, charts) |", "partA")
    t = replace_once(t, "| B | One-page decision memo | 15 | Rubric |", "| B | Structured decision memo (a form of fields inside the notebook) | 15 | Auto-graded: model chosen, validation and test numbers compared with the notebook, three limits and a next step from lists, two short written answers by keyword and length rules |", "partB")
    t = replace_once(t, "| | Proposed (lecturer to confirm) |\n|---|---|\n| Released | After Class 4: CML3112 Tue 24 Nov, CML3113 and CML3111 Fri 27 Nov |\n| Due | Friday 11 December 2026, 23:59 Kampala, all cohorts |\n| Form window | None is open. `opens_at` and `closes_at` stay empty in `data/assessments.json` until you set them |",
                     "| | Proposed (lecturer to confirm) |\n|---|---|\n| Rehearsal (unmarked) | Released after Class 4: CML3112 Tue 24 Nov, CML3113 and CML3111 Fri 27 Nov |\n| Sitting (3 hours) | CML3112 Tue 1 Dec 11:00 to 14:00; CML3113 Fri 4 Dec 08:00 to 11:00; CML3111 Fri 4 Dec 11:00 to 14:00 (Kampala time) |\n| Time limit | The Practical Test 1 mechanism: personal deadline = the earlier of 3 hours after Start and the class closing time (Test windows row with `duration_minutes` 180) |\n| Form window | None is open. Key `CML311x\\|ML_PROJECT` in the Colab test collector; `opens_at` and `closes_at` stay empty until you set them |", "dates")
    t = replace_once(t, "Still to be confirmed by the lecturer: individual or team work, how the project is handed in (one notebook with the memo inside, or a notebook plus a separate memo file), the split of Part A between automatic checks and rubric marks, and the rubrics. The draft project in `second_half/Project/` proposes 24 automatic marks and 6 rubric marks for Part A and builds the memo inside the notebook.",
                     "Decided on 4 November 2026: individual work; one timed, supervised sitting; one notebook with the memo form inside it, handed in with the Test 1 Submit test cell and Google Form; Part A (30) and Part B (15) both fully automatic, with no rubric and no manual marking. A short spot-check list of flagged cases (identity mismatch, copied code, identical written answers, an edited supplied cell, a test set opened twice) is for the lecturer to look at; a flag never reduces a mark by itself. Each student receives one of three data variants (A, B, C) allocated at random by the portal. Still to be confirmed by the lecturer: the sitting dates and times, the room, the form windows and the portal deployment. The draft project in `second_half/Project/` implements this decision.", "tbc")
    t = t.replace("# Assessment update: no demo, the project is submitted", "# Assessment update: no demo, the project is an individual timed auto-graded sitting", 1)
    t += f"\n<!-- {MARK} -->\n"
    print("  arrangement md: 7 replacements and 1 heading")
    if not DRY and not LEARN:
        backup(path)
        path.write_text(t)
        print(f"patched {path.name}")


def patch_json():
    path = ROOT / "data" / "assessment_blocks_20261103.json"
    raw = path.read_text()
    d = json.loads(raw)
    p = d["engineering_ml_project"]
    if p.get("sitting"):
        print(f"already patched: {path.name}")
        return
    assert p["parts"][0]["id"] == "ML_PROJECT_A" and p["parts"][0]["marks"] == 30 and p["parts"][1]["id"] == "ML_PROJECT_B" and p["parts"][1]["marks"] == 15
    new = {}
    for k, v in p.items():
        new[k] = v
    new["what"] = "INDIVIDUAL, TIMED and fully AUTO-GRADED project. One supervised 3-hour sitting in Google Colab in the Week 12 class slot, entered and submitted like Practical Test 1. One submission with two parts. (Update of 4 November 2026.)"
    new["parts"][0]["title"] = "Coded project notebook"
    new["parts"][0]["marking"] = "Fully automatic: hidden checks on unseen data (24 marks) and automatic process checks (6 marks: test set opened once after the choice, no data leakage, reproducible with the seed, readable charts)."
    new["parts"][1]["title"] = "Structured decision memo (a form of fields inside the notebook)"
    new["parts"][1]["marking"] = "Fully automatic: recommended model and decision threshold, validation and test numbers compared with the notebook, three limits and a next step chosen from lists, two short written answers checked by keyword and length rules."
    new["submission_formats"] = ["ipynb"]
    new["hand_in"] = "One notebook with the memo form inside it, handed in like Practical Test 1: the Submit test cell, then the Google Form, before the personal deadline."
    new["submission_note"] = ("Uses the Colab test collector key ML_PROJECT (CML3111|ML_PROJECT, CML3112|ML_PROJECT, CML3113|ML_PROJECT) with a Test windows row of duration_minutes=180, not the assignment form. "
                              "opens_at and closes_at stay null until the lecturer sets them.")
    new["team_or_individual"] = "individual"
    new["rubric_and_marks_detail"] = "No rubric and no manual marking. Part A is 30 automatic marks, Part B is 15 automatic marks. The lecturer reviews a short spot-check list; a flag never lowers a mark by itself."
    # The take-home due date no longer exists. The key stays because data/assessments.json, grader/continuous_assessment.py and tests/test_continuous_assessment.py
    # still read and compare it (proposed_closes_at); its status now says so. The sitting window replaces it once the lecturer sets the Test windows row.
    new["due"] = {"all_cohorts": p["due"]["all_cohorts"], "text": "SUPERSEDED on 4 November 2026: there is no take-home due date. Placeholder kept only because the registry and tests still read it; the Week 12 sitting window replaces it.",
                  "status": "superseded placeholder (proposed, lecturer to confirm the sitting window)"}
    new["released"] = {"rule": "Unmarked rehearsal released right after Class 4 (Week 11 content): practice notebook and practice dataset, same structure, no solved walk-through",
                       "dates": p["released"]["dates"], "status": PROPOSED}
    new["sitting"] = {"duration_minutes": 180, "mode": "supervised, individual, timed, auto-graded, Google Colab; personal deadline = the earlier of 3 hours after Start and the class closing time",
                      "slots": {"CML3112": {"date": "2026-12-01", "start": "11:00", "end": "14:00"}, "CML3113": {"date": "2026-12-04", "start": "08:00", "end": "11:00"},
                                "CML3111": {"date": "2026-12-04", "start": "11:00", "end": "14:00"}},
                      "timezone": "Africa/Kampala", "data_variants": ["A", "B", "C"], "status": PROPOSED}
    d["engineering_ml_project"] = new

    def sub(container, key, old, repl):
        value = container[key]
        assert value.count(old) == 1, f"json {key}: expected 1 match of {old[:60]!r}, found {value.count(old)}"
        container[key] = value.replace(old, repl)
    sub(d, "decision", "students SUBMIT it: it is a take-home, graded like Practical Test 1,", "students sit it alone: it is an individual, timed (one supervised 3-hour sitting), fully auto-graded project like Practical Test 1,")
    sub(d, "decision", "Week 12 is a project clinic (supervised work and questions, no demo).", "Week 12 is the project sitting (3 hours, individual, timed, auto-graded; no demo, no clinic). An unmarked rehearsal is released right after Class 4.")
    d["calendar"]["semester_ends"] = "Week 12 (project sitting). The sitting slots are proposed, lecturer to confirm."
    w = d["calendar"]["week_12_project_clinic"]       # the key name is kept: readers use it
    w["what"] = "Project sitting: 3 hours, individual, timed, auto-graded, in Google Colab, in the class slot. No demo, no presentation, no clinic."
    w["marks"] = "Part A 30 and Part B 15, both automatic (see engineering_ml_project)"
    w["sitting_slots"] = {"CML3112": "2026-12-01 11:00-14:00", "CML3113": "2026-12-04 08:00-11:00", "CML3111": "2026-12-04 11:00-14:00"}
    w["dates_status"] = "Same Week 12 class dates as before. Slots and times: proposed, lecturer to confirm."
    changed = d["changed"]
    for i, old, repl in ((1, "It is a take-home submission, not a demo. Part A coded notebook 30 (auto-graded plus rubric), Part B one-page decision memo 15 (rubric).", "It is an individual, timed, auto-graded sitting, not a demo. Part A coded notebook 30 (automatic), Part B structured decision memo form 15 (automatic)."),
                         (2, "Week 12 is a project clinic (supervised work and questions, no demo).", "Week 12 is the project sitting (3 hours, individual, timed, auto-graded; no demo, no clinic)."),
                         (3, "Project released after Class 4; proposed due date Friday 11 December 2026 23:59 Kampala for all cohorts (proposed, lecturer to confirm).", "Unmarked rehearsal released after Class 4; the sitting is in the Week 12 class slot (proposed, lecturer to confirm).")):
        assert changed[i].count(old) == 1, (i, changed[i])
        changed[i] = changed[i].replace(old, repl)
    oi = d["open_items"]
    assert oi[0].startswith("Whether the project is done individually or in teams") and oi[1].startswith("Release date (after Class 4) and due date")
    oi[0] = "Resolved on 4 November 2026: individual, timed, fully auto-graded. Still open: confirm the sitting dates, times and room, and the portal and collector deployment."
    oi[1] = "Rehearsal release dates (after Class 4) and the Week 12 sitting slots: proposed, lecturer to confirm. No form window is opened until the lecturer sets one (Test windows row, duration_minutes 180)."
    notes = d.get("lecturer_to_decide") or d.get("open_decisions")
    text = json.dumps(d, indent=2, ensure_ascii=False) + "\n"
    # list entries that still mention the old due date: report them, do not guess
    left = [ln.strip() for ln in text.splitlines() if re.search(r"11 December|clinic|take-home", ln, re.I)]
    for ln in left:
        print("  json still says:", ln[:200])
    print("  json: engineering_ml_project rewritten (due removed, sitting added)")
    if not DRY and not LEARN:
        backup(path)
        path.write_text(text)
        print(f"patched {path.name}")


GUIDE = """# {code} ML_PROJECT — Engineering ML project (one timed sitting)

<!-- BLOCK_ASSESSMENT_20261103 -->
<!-- {mark} -->
**What it is:** the Engineering ML project is an INDIVIDUAL, TIMED, AUTO-GRADED sitting of 3 hours in Google Colab. It is worth 45 percent of the course. There is no demo, no upload form and no take-home. It covers only what was taught in Weeks 1 to 11.

- **Part A: coded notebook, 30 marks.** Functions you write are run on data you cannot see (24 marks). Six more marks check how you worked: the test set (group E6) is opened **once** and only **after** you have chosen your model and decision threshold; you **fit preprocessing on the training set only** (no data leakage); you keep `random_state=17` so the result is reproducible; and your two charts have a title, named axes and the unit.
- **Part B: decision memo, 15 marks.** The memo is a form of fields inside the notebook (`MEMO`): the model you recommend, your validation and test numbers, three limits and a next step chosen from lists, and two short written answers. It is marked automatically. Nothing is marked by hand.

**Your sitting (proposed, lecturer to confirm):** {day}, {start} to {end} Kampala time, in your usual class slot. Your own 3 hours start when you press Start on the entry page; the class closing time is the last cutoff.

**Rehearsal (unmarked):** a practice notebook and a practice dataset, with the same structure, are released right after Class 4 ({rehearsal}; proposed, lecturer to confirm). Nothing is submitted or marked. A fully solved walk-through is not given: do the rehearsal yourself, with a 3-hour timer if you can.

**Data variants:** each student receives one of three data variants (A, B, C), allocated at random by the entry page, as in Practical Test 1. Your numbers will differ from your neighbour's.

**Rules (the same as Practical Test 1):** individual work. You may use your lecture slides, lab notebooks, revision guide, cheatsheet and your own notes. **No AI or outside help:** do not use Gemini, ChatGPT, Copilot or any other AI tool, and do not get answers from another person. You may be asked to explain your code afterwards. A short list of unusual cases (for example identical written answers or copied code) is checked by the lecturer; a flag alone never lowers a mark.

## On the day

1. Open the entry link or scan the QR code your lecturer shows. Enter your full name, your Google account email and your Student Registration Number, then press **Start**. **Your 3 hours start now** and the timer cannot be paused.
2. Click **Open my test in Colab** and use the same Google account. Open your private notebook (`ML_PROJECT`).
3. Run the countdown cell (check your name, registration number and email), then the supplied setup cell. It creates your CSV; no upload is needed.
4. Work from top to bottom. Replace each TODO. Keep function names and variable names exactly as printed. Use the self-check cells.
5. Fill the `MEMO` form (Task 9). Use the lists in the notebook for limits and next step.
6. Choose **Runtime, then Restart session and run all**. Fix any error. Choose **File, then Save**.
7. Allow **at least 20 minutes** to submit. Run the **Submit your test** cell, choose the same Google account, click **Submit test**, open the form link, check your details and press **Submit** before your personal deadline. Wait for the confirmation.

**Do not submit** a ZIP, CSV, PDF or a separate memo. The notebook button alone is not a submission: you must submit the form. Late forms are not graded.

Preparation only until the lecturer opens the sitting. This guide does not open any form.
"""


def patch_guides():
    for code in SIT:
        path = BASE / "student_guides" / code / "ML_PROJECT.md"
        t = path.read_text()
        if MARK in t:
            print(f"already patched: {path.parent.name}/{path.name}")
            continue
        assert t.count("## 4. Hand in") == 1 and "Submission link:" in t and t.startswith(f"# {code} ML_PROJECT"), path
        s = SIT[code]
        new = GUIDE.format(code=code, mark=MARK, day=s["long"], start=s["start"], end=s["end"], rehearsal=s["rehearsal"] + " 2026")
        print(f"  {code} guide: whole file rewritten (the old upload-form hand-in removed)")
        if not DRY and not LEARN:
            backup(path)
            path.write_text(new)
            print(f"patched {path.parent.name}/{path.name}")


# ------------------------------------------------------------------------------------------------ main
EXPECT_SYLLABUS = None    # filled by --learn, see below
EXPECT_MASTER_DOCX = None
EXPECT_MASTER_XLSX = None
EXPECT = json.loads((Path(__file__).with_name("patch_project_sitting_20261104_counts.json")).read_text()) if Path(__file__).with_name("patch_project_sitting_20261104_counts.json").exists() else {}


def main():
    patch_arrangement()
    patch_json()
    patch_guides()
    for name, code in SYLLABUS.items():
        patch_docx(BASE / name, syllabus_rules(code), EXPECT.get(name))
    patch_docx(BASE / "IUEA_ML_Semester1_Master_Teaching_Plan.docx", MASTER_RULES, EXPECT.get("IUEA_ML_Semester1_Master_Teaching_Plan.docx"))
    patch_xlsx(BASE / "IUEA_ML_Semester1_Master_Teaching_Plan.xlsx", MASTER_RULES, EXPECT.get("IUEA_ML_Semester1_Master_Teaching_Plan.xlsx"))
    if LEARN:
        out = {}
        for name, rid, n in report:
            out.setdefault(name, {})[rid] = n
        Path(__file__).with_name("patch_project_sitting_20261104_counts.json").write_text(json.dumps(out, indent=1) + "\n")
        print("counts written")
    if not DRY and not LEARN:
        # prove the documents open, and refresh a PDF that already sits next to a docx
        with tempfile.TemporaryDirectory() as tmp:
            for name in list(SYLLABUS) + ["IUEA_ML_Semester1_Master_Teaching_Plan.docx", "IUEA_ML_Semester1_Master_Teaching_Plan.xlsx"]:
                r = subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, str(BASE / name)], capture_output=True, timeout=240)
                ok = (Path(tmp) / (Path(name).stem + ".pdf")).exists()
                print(f"  opens in LibreOffice: {name}: {ok}")
                pdf = BASE / (Path(name).stem + ".pdf")
                if ok and pdf.exists():
                    backup(pdf)
                    shutil.copy2(Path(tmp) / pdf.name, pdf)
                    print(f"  refreshed {pdf.name}")


if __name__ == "__main__":
    main()
