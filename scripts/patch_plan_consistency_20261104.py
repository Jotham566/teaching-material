"""Consistency pass of 4 November 2026 over the Semester 1 plan documents, after the decision that the Week 12 Engineering ML
project is an individual, timed, fully auto-graded 3-hour sitting (Part A 30 + Part B 15 = 45 percent, no rubric, no demo, no clinic,
no team, no take-home).  It removes the wording the earlier patches (apply_policy_20261103.py, patch_docx_20261103.py,
patch_project_sitting_20261104.py) left behind.

Files patched (all in IUEA_Teaching_Plan/):
  * IUEA_ML_Semester1_Master_Teaching_Plan.docx   (project marking paragraph, build-list row, item numbering)
  * IUEA_ML_Semester1_Master_Teaching_Plan.xlsx   (Read Me, Assessment, Rubrics, Tools Rollout, Risk Register, Master Plan, Cohort A/B/C)
  * the three syllabi .docx                       (quiz sentence, test-1 mode, project rubric table, demo/team wording)
  * IUEA_ML_Gradebook_Semester1.xlsx              (three strings: one-page memo, individual-or-team and 11 December due date)
The Weekly Quiz Operations Guide was audited and needed no change.

Method.  Word files: run-level edits with python-docx (formatting kept).  Excel files: the cell text is replaced directly in the sheet XML
inside the zip (these workbooks keep every string inline), so styles, widths, merges, hyperlinks, validations and cached values are
untouched.  Every replacement asserts its match count; nothing is written if one is wrong.  A file whose replacements are all
already applied is reported 'already patched'.  Before a file is written it is copied to a sibling _backup_2026-11-04 folder; if a file of
the same name is already there, the copy is saved as <name>.pre_audit (and never overwrites an existing backup).

Usage: python3 scripts/patch_plan_consistency_20261104.py [--dry-run]
"""
import re
import shutil
import sys
import zipfile
from pathlib import Path

import docx
from docx.text.paragraph import Paragraph

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "IUEA_Teaching_Plan"
DRY = "--dry-run" in sys.argv
BACKUP = "_backup_2026-11-04"


def backup(path):
    path = Path(path)
    d = path.parent / BACKUP
    d.mkdir(exist_ok=True)
    dest = d / path.name
    if dest.exists():
        dest = d / (path.name + ".pre_audit")
    if not dest.exists():
        shutil.copy2(path, dest)
    return dest


# ------------------------------------------------------------------------------------------------ Word
def all_paragraphs(d):
    body = d.element.body
    for p in body.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"):
        yield Paragraph(p, d)
    for s in d.sections:
        for part in (s.header, s.footer, s.first_page_header, s.first_page_footer, s.even_page_header, s.even_page_footer):
            for p in part._element.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"):
                yield Paragraph(p, d)


def replace_in_paragraph(par, old, new):
    """Replace one occurrence inside a paragraph, keeping the first affected run's formatting."""
    runs = par.runs
    text = "".join(r.text for r in runs)
    i = text.find(old)
    if i < 0:
        return False
    j = i + len(old)
    pos = 0
    first = True
    for r in runs:
        a, b = pos, pos + len(r.text)
        pos = b
        if b <= i or a >= j:
            continue
        s = max(i, a) - a
        e = min(j, b) - a
        if first:
            r.text = r.text[:s] + new + r.text[e:]
            first = False
        else:
            r.text = r.text[:s] + r.text[e:]
    return True


def patch_docx(path, rules, report):
    path = Path(path)
    d = docx.Document(str(path))
    todo = False
    for old, new, count in rules:
        n_old = sum(p.text.count(old) for p in all_paragraphs(d))
        n_new = sum(p.text.count(new) for p in all_paragraphs(d))
        if n_old == 0 and n_new >= count:
            report.append((path.name, old[:50], "already"))
            continue
        assert n_old == count, f"{path.name}: expected {count} match(es) for {old[:60]!r}, found {n_old}"
        done = 0
        for p in list(all_paragraphs(d)):
            while old in p.text:
                assert replace_in_paragraph(p, old, new)
                done += 1
        assert done == count, (path.name, old[:60], done)
        report.append((path.name, old[:50], done))
        todo = True
    if todo and not DRY:
        backup(path)
        d.save(str(path))
    return todo


# ------------------------------------------------------------------------------------------------ Excel (sheet XML)
def esc(s):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return "".join(c if ord(c) < 128 else f"&#{ord(c)};" for c in s)


def sheet_files(z):
    wb = z.read("xl/workbook.xml").decode("utf8")
    rels = z.read("xl/_rels/workbook.xml.rels").decode("utf8")
    rid2target = {}
    for m in re.finditer(r"<Relationship [^>]*>", rels):
        t = re.search(r'Target="([^"]+)"', m.group(0)).group(1)
        i = re.search(r'Id="([^"]+)"', m.group(0)).group(1)
        rid2target[i] = t.lstrip("/") if t.startswith("/") else "xl/" + t
    out = {}
    for m in re.finditer(r'<sheet [^>]*name="([^"]+)"[^>]*r:id="([^"]+)"', wb):
        out[m.group(1).replace("&amp;", "&")] = rid2target[m.group(2)]
    return out


def patch_xlsx(path, rules, report):
    """rules: (sheet name, old text, new text, expected count in that sheet)"""
    path = Path(path)
    with zipfile.ZipFile(path) as z:
        files = sheet_files(z)
        data = {n: z.read(n) for n in z.namelist()}
        infos = {i.filename: i for i in z.infolist()}
        order = [i.filename for i in z.infolist()]
    changed = False
    for sheet, old, new, count in rules:
        fn = files[sheet]
        xml = data[fn].decode("utf8")
        eo, en = esc(old), esc(new)
        n_old, n_new = xml.count(eo), xml.count(en)
        if n_old == 0 and n_new >= count:
            report.append((path.name, f"{sheet}: {old[:40]}", "already"))
            continue
        assert n_old == count, f"{path.name}[{sheet}]: expected {count} for {old[:60]!r}, found {n_old}"
        data[fn] = xml.replace(eo, en).encode("utf8")
        report.append((path.name, f"{sheet}: {old[:40]}", n_old))
        changed = True
    if changed and not DRY:
        backup(path)
        tmp = path.with_suffix(".tmp_audit")
        with zipfile.ZipFile(tmp, "w") as zo:
            for n in order:
                zi = zipfile.ZipInfo(n, infos[n].date_time)
                zi.compress_type = infos[n].compress_type
                zi.external_attr = infos[n].external_attr
                zo.writestr(zi, data[n])
        tmp.replace(path)
    return changed


# ------------------------------------------------------------------------------------------------ the rules
MARKING_OLD = ("The project is marked out of 45: Part A, the coded notebook, 30 marks (auto-graded checks plus a rubric), and Part B, the one-page decision memo, "
               "15 marks (rubric). The criterion-level rubrics are to be confirmed by the lecturer and will be published before the project is released.")
MARKING_NEW = ("The project is marked out of 45, all of it automatically: Part A, the coded notebook, 30 marks (hidden checks on unseen data and process checks), and "
               "Part B, the structured decision memo form inside the notebook, 15 marks (form rules). The mark scheme is published before the rehearsal is released.")

PLAN_DOCX = [
    (MARKING_OLD, MARKING_NEW, 1),
    ("Project brief, Part A notebook and checks, Part B memo template, and the rubrics", "Project brief, Part A notebook and checks, Part B memo form, and the mark scheme", 1),
]

SYL_RULES = [
    ("Practical Test 1 in Week 7 and the Week 12 project clinic have no quiz", "Practical Test 1 in Week 7 and the Week 12 project sitting have no quiz", 1),
    ("we should talk before the project demo rather than after it", "we should talk before the project sitting rather than after it", 1),
    ("that nobody in the team can explain", "that nobody can explain", 1),
    ("Take-home Colab practical, 3 hours from the start.", "Timed Colab practical, 3 hours from the start.", 1),
    ("Auto-graded checks on your code plus rubric marks, as for Practical Test 1. Covers Weeks 1 to 11 only. The split between checks and rubric marks is to be confirmed by the lecturer.",
     "Marked automatically, as for Practical Test 1: 24 marks of hidden checks on data you have not seen and 6 marks of process checks (the test set opened once, no data leakage, the same result with the seed, readable charts). Covers Weeks 1 to 11 only. No rubric and no marking by hand.", 1),
    ("Part B: one-page decision memo", "Part B: structured decision memo form", 1),
    ("Rubric: a clear recommendation, the evidence for it, and its limits and risks, written for a non-specialist engineer. The marks for each criterion are to be confirmed by the lecturer.",
     "Marked automatically by form rules: the model you recommend, your validation and test numbers compared with your notebook, three limits and a next step chosen from lists, and two short written answers checked by keyword and length rules.", 1),
]
SYLLABI = ["IUEA_ML_Syllabus_CohortA_Design_and_Infrastructure.docx", "IUEA_ML_Syllabus_CohortB_Mining_and_Petroleum.docx", "IUEA_ML_Syllabus_CohortC_Engineering.docx"]

COHORTS = ["Cohort A", "Cohort B", "Cohort C"]
PLAN_X = [
    ("Read Me", "Twelve risks with owners and mitigations.", "Eighteen risks with owners and mitigations.", 1),
    ("Read Me", "All four rubrics, with criterion weights that sum to 100 by formula.",
     "All four rubrics, with criterion weights that sum to 100 by formula (the project rubric sums to its 45 marks).", 1),
    ("Rubrics", "Criterion weights sum to 100 by formula.", "Criterion weights sum to 100 by formula; the Engineering ML project parts sum to its 45 marks.", 1),
    ("Rubrics", "Part B: one-page decision memo", "Part B: structured decision memo form", 1),
    ("Rubrics", "Auto-graded checks on your code plus rubric marks, as for Practical Test 1. Covers Weeks 1 to 11 only. The split between automatic checks and rubric marks is to be confirmed by the lecturer.",
     "Fully automatic, as for Practical Test 1: 24 marks of hidden checks on unseen data and 6 marks of process checks (test set opened once after the choice, no data leakage, same result with the seed, readable charts). Covers Weeks 1 to 11 only.", 1),
    ("Rubrics", "Rubric: a clear recommendation, the evidence for it, and its limits and risks, written for a non-specialist engineer. The marks for each criterion are to be confirmed by the lecturer.",
     "Form rules, all automatic: the recommended model and threshold, validation and test numbers compared with the notebook, three limits and a next step chosen from lists, and two short written answers checked by keyword and length rules.", 1),
    ("Rubrics", "To be confirmed by the lecturer", "No rubric and no marking by hand; the lecturer reads a spot-check list, and a flag never lowers a mark by itself.", 2),
    ("Assessment", "Take-home Colab practical, 3 hours from the start.", "Timed Colab practical, 3 hours from the start.", 1),
    ("Tools Rollout", "permitted with a log in the W12 challenge and in projects. Prohibited in both tests.",
     "permitted with a log in coursework and in the Data Analysis Project. Prohibited in Practical Test 1 and in the Engineering ML project sitting.", 1),
    ("Risk Register", "Practical Test 1 prohibits AI; it is a take-home test with an understanding check.",
     "Practical Test 1 and the Engineering ML project sitting prohibit AI; each is a timed Colab practical, with an understanding check.", 1),
]
# the Week 12 row and the Week 8 to 11 wording, on the shared sheet and the three cohort sheets
WEEK12_OBJ_OLD = ("• Present a team result in about five minutes and answer questions from the class.\n"
                  "• Show the steps of Classes 1 to 4 on the cohort data: clean, split, baseline, two or more models, a fair comparison, the sealed test group opened once.\n"
                  "• Hand in a one-page decision memo.\nObjectives, marks and mark scheme: to be confirmed by the lecturer.")
WEEK12_OBJ_NEW = ("• Sit the Engineering ML project alone, in one supervised 3-hour timed sitting in Google Colab, entered and submitted like Practical Test 1.\n"
                  "• Show the steps of Classes 1 to 4 on the cohort data: clean, split, baseline, two or more models, a fair comparison, the test set opened once.\n"
                  "• Complete the structured decision memo form inside the notebook.\nMarks: Part A 30 and Part B 15, both automatic.")
WEEK12_STRUCT_OLD = ("• Running order, room and time per team: to be confirmed by the lecturer.\n"
                     "• Each team presents for about five minutes, with questions from the class (Plan_Weeks_8-12.pdf).\n")
WEEK12_STRUCT_NEW = ("• Sitting (all proposed, lecturer to confirm): CML3112 Tue 1 Dec 11:00 to 14:00; CML3113 Fri 4 Dec 08:00 to 11:00; CML3111 Fri 4 Dec 11:00 to 14:00. Room and invigilators: to be confirmed by the lecturer.\n"
                     "• Personal deadline = the earlier of 3 hours after Start and the class closing time, as in Practical Test 1. Nobody presents.\n")
T12_OLD = "Engineering ML Project brief: given in Class 4. Dates, milestones and mark scheme: to be confirmed by the lecturer."
T12_NEW = "Engineering ML Project brief: given in Class 4. Rehearsal released after Class 4; sitting in Week 12 (proposed, lecturer to confirm); marking is automatic."
T13_OLD = "Prepare the approved project dataset list, with a route for teams proposing their own."
T13_NEW = "Prepare for the project: the rehearsal notebook and practice dataset are released after Class 4 (see second_half/Project/)."
T14_OLD = "\n• Prepare the contribution log template (who did what, with commit evidence)."
R14_OLD = "No graded project milestone in the plan. Project milestones, dates and mark scheme are to be confirmed by the lecturer."
R14_NEW = "No project milestone this week. The project is one individual sitting in Week 12 (proposed, lecturer to confirm)."
J15_OLD = "The project brief is given earlier in the class; dates, milestones and mark scheme are to be confirmed by the lecturer."
J15_NEW = "The project brief is given earlier in the class; the rehearsal is released after the class and the sitting is in Week 12 (proposed, lecturer to confirm)."
OWN_OLD = "a written 'conditions of use' statement for their own project model."
OWN_NEW = "a written 'conditions of use' statement for their own model."
DS_OLD = "The team's own project dataset, plus three course-authored"
DS_NEW = "The cohort dataset, plus three course-authored"

PLAN_X += [
    ("Master Plan (Shared Core)", WEEK12_OBJ_OLD, WEEK12_OBJ_NEW, 1),
    ("Master Plan (Shared Core)", WEEK12_STRUCT_OLD, WEEK12_STRUCT_NEW, 1),
    ("Master Plan (Shared Core)", T12_OLD, T12_NEW, 1),
    ("Master Plan (Shared Core)", T13_OLD, T13_NEW, 1),
    ("Master Plan (Shared Core)", T14_OLD, "", 1),
    ("Master Plan (Shared Core)", R14_OLD, R14_NEW, 1),
    ("Master Plan (Shared Core)", J15_OLD, J15_NEW, 1),
    ("Master Plan (Shared Core)", OWN_OLD, OWN_NEW, 1),
]
for c in COHORTS:
    PLAN_X += [
        (c, WEEK12_OBJ_OLD, WEEK12_OBJ_NEW, 1),
        (c, WEEK12_STRUCT_OLD, WEEK12_STRUCT_NEW, 1),
        (c, T12_OLD, T12_NEW, 1),
        (c, T13_OLD, T13_NEW, 1),
        (c, T14_OLD, "", 1),
        (c, R14_OLD, R14_NEW, 1),
        (c, J15_OLD, J15_NEW, 1),
        (c, OWN_OLD, OWN_NEW, 1),
        (c, DS_OLD, DS_NEW, 1),
    ]

GRADEBOOK_X = [
    ("Read me", "Part B one-page decision memo out of 15", "Part B structured decision memo form out of 15", 1),
    ("Read me", "Whether the project is individual or in teams, its release date and its due date (proposed Friday 11 December 2026, 23:59 Kampala) are for the lecturer to confirm.",
     "The project is an individual, timed, auto-graded 3-hour sitting in Week 12 (proposed: CML3112 Tue 1 Dec 11:00 to 14:00, CML3113 Fri 4 Dec 08:00 to 11:00, CML3111 Fri 4 Dec 11:00 to 14:00). The sitting dates, times and room are for the lecturer to confirm.", 1),
    ("Settings", "one-page decision memo", "structured decision memo form", 1),
]


def main():
    report = []
    # item numbering in the build list: rows 10 and 11 were removed earlier, so row 12 becomes 10
    p = BASE / "IUEA_ML_Semester1_Master_Teaching_Plan.docx"
    d = docx.Document(str(p))
    changed_docx = patch_docx(p, PLAN_DOCX, report)
    d = docx.Document(str(p))
    tbl = [t for t in d.tables if any(len(r.cells) > 1 and r.cells[1].text.startswith("Semester 2 master plan") for r in t.rows)]
    assert len(tbl) == 1
    ids = [r.cells[0].text for r in tbl[0].rows[1:] if r.cells[0].text.strip()]
    if ids[-1] == "12":
        assert ids[-2] == "9" and tbl[0].rows[-1].cells[1].text.startswith("Semester 2 master plan")
        if not DRY:
            backup(p)
            par = tbl[0].rows[-1].cells[0].paragraphs[0]
            assert replace_in_paragraph(par, "12", "10")
            d.save(str(p))
        report.append((p.name, "build-list item number 12 -> 10", 1))
    else:
        assert ids[-1] == "10", ids
        report.append((p.name, "build-list item number", "already"))
    for n in SYLLABI:
        patch_docx(BASE / n, SYL_RULES, report)
    patch_xlsx(BASE / "IUEA_ML_Semester1_Master_Teaching_Plan.xlsx", PLAN_X, report)
    patch_xlsx(BASE / "IUEA_ML_Gradebook_Semester1.xlsx", GRADEBOOK_X, report)
    for r in report:
        print(*r, sep=" | ")
    print("dry run, nothing written" if DRY else "done")


if __name__ == "__main__":
    main()
