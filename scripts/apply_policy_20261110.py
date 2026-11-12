#!/usr/bin/env python3
"""Bring every living document, guide and builder into line with the grading policy of 10 November 2026.

Source of truth: data/assessment_policy_20261110.json and IUEA_Teaching_Plan/Grading_Policy_2026-11-10.md.
  Final mark /100 = assignments 20 (A1 to A5, each /20, all five equal) + quizzes 20 (Q1 to Q5, each /5, all five equal)
                    + Practical Test 1 20 + Engineering ML project 40 (Part A 30 + Part B 15 = 45 raw, scaled to 40).
  Not counted (still set and collected as practice): Q6 onward and the Week 8 to 11 block quizzes (Q7 to Q10), A6 onward and
  the Week 8 to 11 block assignments (A7 to A11), the Data Analysis project, Practical Test 2, the demo.
  Retired: best-3-of-5, the Week 6 waiver, the block rule. Provisional results are out of 60 until the project is marked.

Idempotent: every replacement is skipped when the new text is already present. Dated history notes only get a banner.
Not touched on purpose (another session owns them): grader/gradebook.gs, grader/Grades_template.csv, grader/README.md,
grader/continuous_assessment.py, grader/grade_test_batch.py, grader/test_collection_issues.py, grader/final_marks_export.py,
test_operations/TEST_CHECKLIST.md, tests/test_test_batch.py, scripts/assessment_registry.py and the gradebook xlsx builders.
Usage: python3 scripts/apply_policy_20261110.py [--dry]   (use .iuea-grader-env for the docx/xlsx parts)
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]; BASE = ROOT / "IUEA_Teaching_Plan"; SCR = ROOT / "scripts"
DRY = "--dry" in sys.argv
COHORTS = ("CML3111", "CML3112", "CML3113")
CHANGED = []; MISSING = []


# ------------------------------------------------------------------------------------------------ helpers
def note_changed(p):
    p = str(Path(p).relative_to(ROOT));
    if p not in CHANGED: CHANGED.append(p)


def edit_text(path, pairs, regex=False, required=True):
    """pairs = [(old, new)]. A pair is skipped when `new` is already there; reported when `old` is missing and required."""
    path = Path(path)
    if not path.exists(): MISSING.append(f"{path}: file missing"); return False
    t0 = t = path.read_text(encoding="utf-8")
    for old, new in pairs:
        if regex:
            t2, n = re.subn(old, new, t, flags=re.S)
            if n == 0 and required and not re.search(new if isinstance(new, str) and not re.search(r"\\[0-9g]", new) else "$^", t): MISSING.append(f"{path.relative_to(ROOT)}: no match for /{old[:60]}/")
            t = t2
        else:
            if new in t and old in new: continue          # already applied (new text contains old)
            if old in t: t = t.replace(old, new)
            elif new not in t and required: MISSING.append(f"{path.relative_to(ROOT)}: missing {old[:70]!r}")
    if t != t0:
        if not DRY: path.write_text(t, encoding="utf-8")
        note_changed(path); return True
    return False


def line_replace(path, startswith, newline, required=True):
    """Replace the whole line that starts with `startswith` (md/txt)."""
    path = Path(path); t0 = path.read_text(encoding="utf-8"); out = []; hit = False
    for ln in t0.split("\n"):
        if ln.startswith(startswith): out.append(newline); hit = True
        else: out.append(ln)
    if not hit and newline not in t0 and required: MISSING.append(f"{path.relative_to(ROOT)}: no line starting {startswith[:60]!r}")
    t = "\n".join(out)
    if t != t0:
        if not DRY: path.write_text(t, encoding="utf-8")
        note_changed(path); return True
    return False


BANNER_MARK = "SUPERSEDED_20261110"
BANNER = ("<!-- SUPERSEDED_20261110 -->\n> **Superseded on 10 November 2026 by `Grading_Policy_2026-11-10.md`.** The weights, the best-3-of-5 rule, "
          "the Week 6 waiver, the block rule and the provisional total out of 55 recorded below are history. From 10 November only A1 to A5 and Q1 to Q5 count: "
          "the final mark is assignments 20 + quizzes 20 + Practical Test 1 20 + Engineering ML project 40, and provisional results are out of 60. "
          "The body below is left unchanged as a record.\n\n")


def add_banner(path):
    path = Path(path); t = path.read_text(encoding="utf-8")
    if BANNER_MARK in t: return
    if not DRY: path.write_text(BANNER + t, encoding="utf-8")
    note_changed(path)


PRACTICE_STU = ("**Does this count?** No. From 10 November 2026 the Week 8 to 11 block assignments (A7 to A11) and block quizzes (Q7 to Q10) are practice "
                "and do not count toward your final mark (only A1 to A5 and Q1 to Q5 count). Still do the work: it is collected, you get feedback, and it prepares you "
                "for the project sitting.")
COUNT_STU = ("Your Semester 1 mark out of 100 is: assignments 20 (A1 to A5, each marked out of 20, all five count equally) + quizzes 20 (Q1 to Q5, each marked out of 5, "
             "all five count equally) + Practical Test 1 20 + Engineering ML project 40 (Part A 30 + Part B 15 = 45 marks, scaled to 40). "
             "There is no best-3-of-5 rule and no Week 6 waiver any more: a missing item scores zero. The Data Analysis project, Practical Test 2 and the demo do not count. "
             "The Week 8 to 11 block assignments and quizzes (A7 to A11, Q7 to Q10) and A6 and Q6 are practice and do not count toward the final mark.")
PROV_STU = ("Your Semester 1 result can be published before the project is marked. It then shows as provisional, out of 60 marks (assignments 20 + quizzes 20 + Practical Test 1 20), "
            "with the project marked PENDING. The full total out of 100 appears when the project is marked.")


# ------------------------------------------------------------------------------------------------ 1. dated history notes: banner only
def history_banners():
    for n in ("Block_Assessment_Arrangement_2026-10-30.md", "Block_Assessment_Arrangement_2026-11-02.md", "Block_Assessment_Arrangement_2026-11-03.md",
              "Block_Assessment_By_Hand_Checklist_2026-11-02.md", "Block_Assessment_Verification_2026-11-02.md", "Grading_Update_By_Hand_2026-11-03.md",
              "Stale_Documents_Audit_2026-11-04.md", "Practical_Revision_Week6_Waiver.md", "Week8_Onwards_Deck_Review_2026-10-29.md",
              "Weeks8-12_Rebuild_Log_and_Industry_Coverage_2026-10-30.md"):
        add_banner(BASE / n)


# ------------------------------------------------------------------------------------------------ 2. living markdown
def living_markdown():
    tp = BASE / "Teaching_Progress.md"
    edit_text(tp, [
        ("(a form inside the notebook) = 45 percent. It covers Weeks 1 to 11 only.", "(a form inside the notebook) = 45 raw, scaled to 40 percent of the course. It covers Weeks 1 to 11 only."),
        ("The data analysis project (10 percent) is still a team project.", "The data analysis project no longer counts toward the final mark (it is still set as practice)."),
    ])
    line_replace(tp, "- Weights: quizzes 15",
                 "- Weights (policy of 10 November 2026, `Grading_Policy_2026-11-10.md`): assignments 20 (A1 to A5, all five count equally), quizzes 20 (Q1 to Q5, all five count equally), "
                 "Practical Test 1 20, Engineering ML project 40. Not counted: Q6 onward and the Week 8 to 11 block quizzes (Q7 to Q10), A6 onward and the Week 8 to 11 block assignments "
                 "(A7 to A11), the Data Analysis project, Practical Test 2 and the demo. Block 1 is A7 + A8 and Q7 + Q8 (quiz sat in the last 20 minutes of Class 2); Block 2 is A9 + A10 + A11 "
                 "and Q9 + Q10 (last 20 minutes of Class 4). They are still set and collected as practice, with feedback. The best-3-of-5 rule, the Week 6 waiver and the block rule are retired. "
                 "Results are provisional out of 60 until the project is marked.")
    edit_text(tp, [("- Details: `second_half/Plan_Weeks_8-12.pdf`, `Block_Assessment_Arrangement_2026-11-03.md`",
                    "- Details: `Grading_Policy_2026-11-10.md` (the current weights), `second_half/Plan_Weeks_8-12.pdf`, `Block_Assessment_Arrangement_2026-11-10.md`, `Block_Assessment_Arrangement_2026-11-03.md`")], required=False)

    edit_text(tp, [("Week 7 was Practical Test 1. Week 6 was waived.", "Week 7 was Practical Test 1. Week 6 was practical revision (A6 and Quiz 6 not assigned; they do not count).")], required=False)
    edit_text(BASE / "assessment_operations/README.md", [("A6 and Quiz 6 are waived for all three programmes; their original marks remain recorded but excluded from totals.",
              "A6 and Quiz 6 are not assigned for any programme and do not count; their original marks remain recorded but are excluded from totals. From 10 November 2026 only A1 to A5 and Q1 to Q5 count (Grading_Policy_2026-11-10.md).")], required=False)

    bc = BASE / "Before_Each_Class_Checklist.md"
    edit_text(bc, [
        ("## Current exception: all three programmes — A6 and Quiz 6 waived", "## Current exception: all three programmes — A6 and Quiz 6 not assigned (they do not count)"),
        ("remain on record but are excluded from coursework totals.", "remain on record but do not count toward the final mark (only A1 to A5 and Q1 to Q5 count; see [Grading_Policy_2026-11-10.md](Grading_Policy_2026-11-10.md))."),
        ("The Block 1 quiz (Q7 + Q8, 10 marks) is sat in the last 20 minutes of this class.", "The Block 1 quiz (Q7 + Q8, 10 marks) is sat in the last 20 minutes of this class. It is practice and does not count toward the final mark."),
        ("Block 1 assignments (A7, A8) close on the date in the arrangement note.", "Block 1 practice assignments (A7, A8; they do not count toward the final mark) close on the date in the arrangement note."),
        ("The Block 2 quiz (Q9 + Q10, 10 marks) is sat in the last 20 minutes.", "The Block 2 quiz (Q9 + Q10, 10 marks) is sat in the last 20 minutes (practice; it does not count toward the final mark)."),
    ], required=False)

    sl = BASE / "Assignment_Submission_Links.md"
    edit_text(sl, [("A7 and A8 form Block 1 and close together; A9, A10 and A11 form Block 2 and close together.",
                    "A7 and A8 form Block 1 and close together; A9, A10 and A11 form Block 2 and close together. **Update of 10 November 2026:** only A1 to A5 count toward the final mark; "
                    "A6 onward, including the Week 8 to 11 block assignments (A7 to A11), are practice that is still collected and given feedback but adds nothing to the final mark "
                    "(see `Grading_Policy_2026-11-10.md`).")])
    edit_text(sl, [("ML_PROJECT: Engineering ML project (individual, timed 3-hour sitting; Part A /30, Part B /15)",
                    "ML_PROJECT: Engineering ML project (individual, timed 3-hour sitting; Part A /30, Part B /15, scaled to 40 percent of the course)")], required=False)

    gr = BASE / "assessment_operations/reference/GRADING.md"
    t = gr.read_text(encoding="utf-8")
    new = ("> Policy since 10 November 2026 (`data/assessment_policy_20261110.json`, plain note `Grading_Policy_2026-11-10.md`): final mark /100 = assignments 20 + quizzes 20 + Practical Test 1 20 + "
           "Engineering ML project 40. The live gradebook is the Google Sheet driven by `grader/gradebook.gs`. The private workbook described below was last built on 21 October and still uses "
           "the OLD weights and rules: do not use its totals for Semester 1 results.\n\n"
           "- Assignments: A1 to A5, each marked out of 20, all five count equally. Assignment mark /20 = (A1 + A2 + A3 + A4 + A5) / 5.\n"
           "- Quizzes: Q1 to Q5, each marked out of 5, all five count equally. Quiz mark /20 = (Q1 + Q2 + Q3 + Q4 + Q5) x 4 / 5.\n"
           "- Practical Test 1: marked out of 100, scaled to 20. Engineering ML project: Part A /30 + Part B /15 = 45, scaled to 40; counted only when both parts are marked.\n"
           "- Not counted: Q6 onward and the Week 8 to 11 block quizzes, A6 onward and the Week 8 to 11 block assignments, the Data Analysis project, Practical Test 2 and the demo. "
           "Their receipts are still collected and kept; they add nothing to the final mark. The best-3-of-5 rule, the Week 6 waiver and the block rule are retired.\n"
           "- Until the project is marked the result is provisional out of 60 (assignments 20 + quizzes 20 + Practical Test 1 20). An unmarked project is never counted as zero.\n")
    edit_text(gr, [("- A blank is pending or not yet submitted, **not a zero**. A numeric zero is a completed mark.",
                    "- In the private workbook a blank is pending or not yet submitted, **not a zero**, and a numeric zero is a completed mark. In the Semester 1 final mark (policy of 10 November 2026) a missing or not-yet-marked assignment, quiz or Practical Test 1 scores 0; only the project can be PENDING.")], required=False)
    if "Policy since 10 November 2026" not in t:
        a = t.index("> Policy since 3 and 4 November 2026"); b = t.index("- A blank is pending")
        if not DRY: gr.write_text(t[:a] + new + t[b:], encoding="utf-8")
        note_changed(gr)

    # second_half
    edit_text(BASE / "second_half/README.md", [("The Engineering ML project (45 percent of the course)", "The Engineering ML project (40 percent of the course)")])
    pr = BASE / "second_half/Project/README.md"
    edit_text(pr, [("It counts 45 percent of the course:", "It counts 40 percent of the course (Part A 30 + Part B 15 = 45 marks, scaled to 40):")])
    edit_text(BASE / "second_half/Build/AUTHORING_GUIDE.md", [("and counts 45 percent of the course)", "and counts 40 percent of the course; the Week 8 to 11 assignments and quizzes are practice that does not count)")], required=False)


# ------------------------------------------------------------------------------------------------ 3. student guides and assignment banks
def student_guides():
    for c in COHORTS:
        g = BASE / "student_guides" / c
        for n in ("B1.md", "B2.md"):
            p = g / n
            line_replace(p, "Weeks 1 to 5 stay weekly, and Week 6 is waived.", COUNT_STU)
            edit_text(p, [
                ("A part you do not submit scores zero, so submit every part.", "A part you do not submit gets no feedback, so submit every part."),
                ("It is worth 45 percent of the course: Part A, the coded project notebook (30 marks), and Part B, a structured decision memo inside the notebook (15 marks).",
                 "It is worth 40 percent of the course: Part A, the coded project notebook (30 marks), and Part B, a structured decision memo inside the notebook (15 marks); the 45 marks are scaled to 40."),
            ], required=False)
            line_replace(p, "Your Semester 1 result can be published before the project is marked.", PROV_STU)
            edit_text(p, [("## Assignment\n", "## Assignment\n\nThese are practice assignments: they do not count toward your final mark (see How it counts below), but they are collected and you get feedback.\n")], required=False)
        da = g / "DA_PROJECT.md"
        edit_text(da, [(r"(\*\*Deadline:\*\*[^\n]*\n)", r"\1**Does this count?** No. From 10 November 2026 the Data Analysis project does not count toward your final mark (see Grading_Policy_2026-11-10.md). It is still collected and you get feedback.\n")], regex=True, required=False) if "Does this count" not in da.read_text(encoding="utf-8") else None
        p = g / "ML_PROJECT.md"
        edit_text(p, [("It is worth 45 percent of the course.", "It is worth 40 percent of the course (Part A 30 + Part B 15 = 45 marks, scaled to 40).")])
        for n in ("W08", "W09", "W10", "W11", "W12"):
            practice_line_md(g / f"{n}.md")
        w6 = g / "W06.md"
        if w6.exists():
            line_replace(w6, "Coursework: best 9 of 11", W6_NEW, required=False)
    for c in COHORTS:
        for w in ("W08", "W09", "W10", "W11", "W12"):
            d = BASE / "assessment_banks" / w / c / "A"
            practice_line_md(d / "ASSIGNMENT_INSTRUCTIONS.md"); practice_line_txt(d / "ASSIGNMENT_INSTRUCTIONS.txt"); practice_line_nb(d / f"{w}_student.ipynb")
        d = BASE / "assessment_banks/W06" / c / "A"
        for n in ("ASSIGNMENT_INSTRUCTIONS.md", "ASSIGNMENT_INSTRUCTIONS.txt", "TASKS.md"):
            if (d / n).exists(): line_replace(d / n, "Coursework: best 9 of 11", W6_NEW, required=False)
        nb = d / "W06_student.ipynb"
        if nb.exists():
            edit_text(nb, [("Coursework: best 9 of 11 assigned quizzes (10%); best 7 of 10 assigned weekly assignments (10%). A6 and Quiz 6 are excluded, including any previously recorded marks. Other assessments keep their weights.",
                            W6_NEW)], required=False)
        ml = BASE / "assessment_banks/ML_PROJECT" / c / "A"
        for n in ("ASSIGNMENT_INSTRUCTIONS.md", "ASSIGNMENT_INSTRUCTIONS.txt", "TASKS.md"):
            edit_text(ml / n, [("worth 45: Part A coded notebook 30 and Part B decision memo 15", "worth 40 (Part A coded notebook 30 and Part B decision memo 15, 45 marks scaled to 40)")], required=False)


W6_NEW = ("Coursework: A6 and Quiz 6 are not assigned and do not count toward the final mark, including any previously recorded marks. "
          "Only A1 to A5 and Q1 to Q5 count (20 percent each). See Grading_Policy_2026-11-10.md.")


def practice_line_md(p):
    p = Path(p)
    if not p.exists(): return
    edit_text(p, [
        (re.compile(r"(\*\*Block quiz:\*\*[^\n]*\n)").pattern, r"\1\n" + PRACTICE_STU + "\n"),
    ], regex=True, required=False) if PRACTICE_STU not in p.read_text(encoding="utf-8") else None
    edit_text(p, [("- A part that is not submitted scores zero. Submit each part as you finish it.", "- A part that is not submitted gets no feedback. Submit each part as you finish it.")], required=False)


def practice_line_txt(p):
    p = Path(p)
    if not p.exists(): return
    txt = p.read_text(encoding="utf-8")
    if PRACTICE_STU.replace("**", "") in txt or PRACTICE_STU in txt: pass
    else:
        t = re.sub(r"(\*{0,2}Block quiz:\*{0,2}[^\n]*\n)", lambda m: m.group(1) + "\n" + PRACTICE_STU.replace("**", "") + "\n", txt, count=1)
        if t != txt:
            if not DRY: p.write_text(t, encoding="utf-8")
            note_changed(p)
    edit_text(p, [("- A part that is not submitted scores zero. Submit each part as you finish it.", "- A part that is not submitted gets no feedback. Submit each part as you finish it.")], required=False)


def practice_line_nb(p):
    p = Path(p)
    if not p.exists(): return
    txt = p.read_text(encoding="utf-8")
    if "Does this count?" not in txt:
        pat = re.compile(r'^(\s*)"(\*\*Block quiz:\*\*[^"\n]*)\\n",\n', re.M)
        def sub(m):
            ind = m.group(1)
            return m.group(0) + f'{ind}"\\n",\n{ind}"{PRACTICE_STU}\\n",\n'
        t = pat.sub(sub, txt, count=1)
        if t != txt:
            if not DRY: p.write_text(t, encoding="utf-8")
            note_changed(p)
        else: MISSING.append(f"{p.relative_to(ROOT)}: no Block quiz line")
    edit_text(p, [('A part that is not submitted scores zero. Submit each part as you finish it.', 'A part that is not submitted gets no feedback. Submit each part as you finish it.')], required=False)


# ------------------------------------------------------------------------------------------------ 4. project text (45 percent -> 40)
PROJECT_RULES = [
    ("Part A 30 marks + Part B 15 marks = 45 percent of the course", "Part A 30 marks + Part B 15 marks = 45 marks, scaled to 40 percent of the course"),
    ("Part A 30 + Part B 15 = 45 percent of the course", "Part A 30 + Part B 15 = 45 marks, scaled to 40 percent of the course"),
    ("Together 45 percent of the course", "Together 45 marks, scaled to 40 percent of the course"),
    ("(out of 45, which is 45 percent of the course)", "(out of 45, scaled to 40 percent of the course)"),
    ("Part A 30 marks and Part B 15 marks (45 percent of the course)", "Part A 30 marks and Part B 15 marks (45 marks, scaled to 40 percent of the course)"),
    ("worth 45 percent (Part A 30, Part B 15)", "worth 40 percent (Part A 30, Part B 15, scaled from 45)"),
    ("45 percent of the course", "40 percent of the course"),
    ("worth 45 percent.", "worth 40 percent."),
]


def project_text():
    files = []
    sh = BASE / "second_half"
    skip = ("_backup_", "/Slides/", "/Student Packages/")
    for ext in ("*.py", "*.json", "*.ipynb", "*.gs", "*.md", "*.txt"):
        for f in sh.rglob(ext):
            s = str(f)
            if any(k in s for k in skip) or "__pycache__" in s: continue
            files.append(f)
    files += [BASE / "grader/submission_forms.gs", ROOT / "data/iuea_assignment_form_briefs.json", BASE / "test_portal/Packets.gs"]
    for f in files:
        if not f.exists(): continue
        t = f.read_text(encoding="utf-8", errors="ignore")
        if "45 percent" not in t: continue
        edit_text(f, PROJECT_RULES, required=False)


# ------------------------------------------------------------------------------------------------ 5. builders and scripts (source text)
def builders():
    # quiz forms (generated create_quiz_forms.gs is rebuilt from this)
    q = SCR / "build_quiz_forms_gs.py"
    edit_text(q, [
        ('"two block quizzes are Q7 and Q8 (Block 1) and Q9 and Q10 (Block 2). Do not submit this form.")',
         '"block quizzes Q7 to Q10 are practice and do not count toward the final mark. Do not submit this form.")'),
        ('+ f"\\n• Five questions, one mark each. The two Block {block} quizzes together are out of 10 marks and a block always counts. "\n              "All quizzes together are out of 35 marks and count for 15% of the course."',
         '+ f"\\n• Five questions, one mark each. The two Block {block} quizzes together are out of 10 marks. "\n              "These block quizzes are practice: they do not count toward your final mark (only Q1 to Q5 do), but do them anyway. The feedback shows you what to fix before the project sitting."'),
        ("'Five questions, one mark each. All quizzes together are out of 35 marks and count for 15% of the course.'",
         "'Five questions, one mark each. Quizzes Q1 to Q5 are each out of 5, all five count equally, and together they are worth 20% of the course.'"),
        ("'Quiz 6 is not assigned. Of the Week 1 to 5 quizzes your best three count, and there are no resits.'",
         "'All five of the Week 1 to 5 quizzes count. There is no best-of rule and there are no resits.'"),
        ("if wk==6:intro='NOT ASSIGNED: Quiz 6 is waived for practical revision. No submission or mark is required.'",
         "if wk==6:intro='NOT ASSIGNED: Quiz 6 is not set (practical revision) and does not count toward the final mark. No submission or mark is required.'"),
        ("# Week 6 waived; two block sittings from Week 8; quizzes out of 35 marks and 15% of the course.",
         "# Week 6 waived; two block sittings from Week 8. Superseded 10 November 2026: only Q1 to Q5 count (each /5, 20% of the course); the block quizzes are practice."),
        ("# Policy of 2 November 2026 (data/assessment_blocks_20261102.json): Weeks 1 to 5 weekly, best 3 of 5,",
         "# Policy of 10 November 2026 (data/assessment_policy_20261110.json): Q1 to Q5 all count (20%); Q6 onward and the block quizzes are practice. Earlier: Weeks 1 to 5 weekly, best 3 of 5,"),
    ], required=False)
    edit_text(SCR / "verify_quiz_arithmetic.py", [
        ('ok(f"{_code}: Weeks 1 to 5 intros state best three and 15%",\n       all(("best three" in _by[w]["intro"] and "15%" in _by[w]["intro"]) for w in (1, 2, 3, 4, 5)))',
         'ok(f"{_code}: Weeks 1 to 5 intros say all five count and 20%",\n       all(("all five count" in _by[w]["intro"] and "20%" in _by[w]["intro"]) for w in (1, 2, 3, 4, 5)))'),
    ], required=False)
    edit_text(SCR / "build_quiz_timer.py", [("'Five questions. One attempt. Your best ten of ' +\n        'twelve quizzes count.'", "'Five questions. One attempt. ' +\n        'Read each question once.'")], required=False)
    edit_text(BASE / "quiz_timer.html", [("'Five questions. One attempt. Your best ten of ' +\n        'twelve quizzes count.'", "'Five questions. One attempt. ' +\n        'Read each question once.'")], required=False)
    edit_text(SCR / "pptxkit.py", [("Twelve this semester, best ten count. No resits.", "Q1 to Q5 all count. No resits.")], required=False)
    # quiz operations guide source
    qo = SCR / "build_quizops_docx.py"
    edit_text(qo, QUIZOPS_RULES, required=False)
    # project tools
    for f in ("second_half/Project/tools/build_project_docs.py", "second_half/Project/tools/build_project_notebooks.py",
              "second_half/Project/tools/build_deploy_bundle.py", "second_half/Project/grader_spec/grade_project.py"):
        edit_text(BASE / f, PROJECT_RULES, required=False)


QUIZOPS_RULES = [
    ("From 2 November 2026 nine weeks are sat (Weeks 1 to 5 and the four block forms Q7 to Q10); Week 6 is waived and Q11 and Q12 are retired.",
     "Nine weeks are sat (Weeks 1 to 5 and the four block forms Q7 to Q10); Week 6 is not assigned and Q11 and Q12 are retired. From 10 November 2026 only Q1 to Q5 count toward the final mark; the block quizzes are practice."),
    ("counts the best 3 of Q1–Q5 and the two blocks (Q7 + Q8 and Q9 + Q10), and ignores Q6 (waived), Q11 and Q12 (retired)",
     "counts all five of Q1–Q5 (each out of 5) and ignores Q6, the block quizzes Q7 to Q10 (practice, collected and kept), Q11 and Q12 (retired)"),
    ("Q11 and Q12 are retired and are never sat. Each form is worth 5 marks, so a block quiz is out of 10. The forms, answer keys and gradebook columns are unchanged.",
     "Q11 and Q12 are retired and are never sat. Each form is worth 5 marks, so a block quiz is out of 10. From 10 November 2026 the block quizzes are practice: they are sat, marked and kept, with feedback, but add nothing to the final mark. The forms, answer keys and gradebook columns are unchanged."),
    ("Gradebook: Weeks 1 to 5 keep the best 3 of 5, because Week 6 is waived for all three cohorts. The two blocks are never dropped. Quizzes are out of 35 marks (3 x 5 + 10 + 10) and assignments out of 160 marks (3 x 20 + 40 + 60); each component is worth 15% of the course. From 3 November 2026 there is no demo: the Engineering ML project (45%) is Part A /30 plus Part B /15, entered in two columns. Until both columns hold a mark the sheet shows 'Semester 1 provisional: x of 55 marks, y percent' and 'Project: PENDING', and leaves Final % and Band blank.",
     "Gradebook (policy of 10 November 2026): all five of Q1 to Q5 count equally (25 raw, scaled to 20) and all five of A1 to A5 count equally (100 raw, scaled to 20); there is no best-of rule and no Week 6 waiver. Practical Test 1 is 20 and the Engineering ML project is 40 (Part A /30 plus Part B /15, 45 raw scaled to 40, entered in two columns). Q6 onward and the block quizzes, and A6 onward and the block assignments, do not count. Until both project columns hold a mark the sheet shows 'Semester 1 provisional: x of 60 marks, y percent' and 'Project: PENDING', and leaves Final % and Band blank."),
]


# ------------------------------------------------------------------------------------------------ 6. builders that cannot be regenerated safely (text only)
def stale_builders():
    """build_syllabi.py, build_master_docx.py, plan_content.py and build_xlsx.py are still the pre-30-October 15-week builders (their line 1 already
    says so). Their generated files were changed afterwards by the patch_* scripts, so regenerating would undo that work, and half-editing the
    weights in them would leave an incoherent source. They only get a note; the live documents are patched in place below."""
    add = (" Update of 10 November 2026: the grading policy changed again (Grading_Policy_2026-11-10.md); the live documents were patched IN PLACE by "
           "scripts/apply_policy_20261110.py and this generator still carries the older weights and rules on purpose.")
    for n in ("build_syllabi.py", "build_master_docx.py", "plan_content.py", "build_xlsx.py"):
        p = SCR / n; lines = p.read_text(encoding="utf-8").split("\n")
        if lines and lines[0].startswith("# NOTE (4 November 2026)") and "10 November 2026" not in lines[0]:
            lines[0] += add
            if not DRY: p.write_text("\n".join(lines), encoding="utf-8")
            note_changed(p)


# ------------------------------------------------------------------------------------------------ 7. data
def data_files():
    p = ROOT / "data/assessments.json"
    rows = json.loads(p.read_text(encoding="utf-8")); n = 0
    for r in rows:
        if r.get("id") in ("W08", "W09", "W10", "W11", "W12") and r.get("block") and "Practice" not in (r.get("delivery_note") or ""):
            r["delivery_note"] = (r.get("delivery_note") or "").rstrip() + " Practice: from 10 November 2026 this does not count toward the final mark (still collected, with feedback)."
            n += 1
    if n:
        if not DRY: p.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        note_changed(p)


# ------------------------------------------------------------------------------------------------ 8. docx / xlsx
def para_text_replace(par, old, new):
    """Replace inside one paragraph; keep run formatting when `old` sits inside a single run, else merge runs into the first."""
    if old in new and new in par.text: return False       # already applied
    for r in par.runs:
        if old in r.text:
            r.text = r.text.replace(old, new); return True
    full = par.text
    if old in full and par.runs:
        newfull = full.replace(old, new)
        par.runs[0].text = newfull
        for r in par.runs[1:]: r.text = ""
        return True
    return False


def iter_pars(doc):
    for p in doc.paragraphs: yield p
    for t in doc.tables:
        for row in t.rows:
            seen = set()
            for c in row.cells:
                if id(c._tc) in seen: continue
                seen.add(id(c._tc))
                for p in c.paragraphs: yield p
    for s in doc.sections:
        for part in (s.header, s.footer):
            for p in part.paragraphs: yield p


def docx_edit(path, pairs, required=True):
    from docx import Document
    path = Path(path)
    if not path.exists(): MISSING.append(f"{path}: missing"); return
    d = Document(str(path)); changed = False
    for old, new in pairs:
        n = 0
        for p in iter_pars(d):
            if old in p.text and para_text_replace(p, old, new): n += 1
        if n: changed = True
        elif required and not any(new in p.text for p in iter_pars(d)): MISSING.append(f"{path.name}: missing {old[:70]!r}")
    if changed:
        if not DRY: d.save(str(path))
        note_changed(path)


SYL_RULES = [
    ("It is also continuous: fifty-five per cent of your mark (the quizzes, the assignments, the Data Analysis Project and Practical Test 1) is earned, and can be published, before the project is marked",
     "It is also continuous: sixty per cent of your mark (the assignments A1 to A5, the quizzes Q1 to Q5 and Practical Test 1) is earned, and can be published, before the project is marked"),
    ("Ninety per cent of the mark is individual: the quizzes, the assignments, Practical Test 1 and the Engineering ML project (45 per cent), which is one supervised 3-hour timed sitting",
     "All of the mark is individual: the assignments, the quizzes, Practical Test 1 and the Engineering ML project (40 per cent), which is one supervised 3-hour timed sitting"),
    ("Nine quizzes are sat in all (Week 6 is waived, and Q11 and Q12 no longer exist).",
     "Nine quizzes are sat in all (Week 6 is not assigned, and Q11 and Q12 no longer exist), but only Q1 to Q5 count toward your final mark: the block quizzes Q7 to Q10 are practice."),
    ("Second, there are no resits. Of the five weekly quizzes in Weeks 1 to 5 only your best three count, so two of them can go badly for any reason at all, and that is what covers illness, travel and a bad day; the two block quizzes always count.",
     "Second, there are no resits. All five weekly quizzes in Weeks 1 to 5 count equally (each is worth 4 of the 20 quiz marks), so every one of them matters; the block quizzes are practice, so a bad day in Week 9 or 11 costs you nothing but the feedback."),
    ("The quizzes are out of 35 marks and are worth 15 per cent of the course, and they exist to tell you, and me, whether you have kept up. Fifteen per cent of your mark sits in Practical Test 1, which is unaided.",
     "The quizzes are worth 20 per cent of the course (Q1 to Q5, each marked out of 5), and they exist to tell you, and me, whether you have kept up. Twenty per cent of your mark sits in Practical Test 1, which is unaided."),
    ("which is why the best three of the five weekly assignments count and the two blocks always count.",
     "which is why all five of A1 to A5 count. The two block packs are practice that does not count, but do them: they are the rehearsal for the project sitting."),
    ("The project is marked out of 45. Part A", "The project is marked out of 45, scaled to 40 percent of the course. Part A"),
    ("Five weekly assignments in Weeks 1 to 5 and then two block packs is a manageable load", "Five weekly assignments in Weeks 1 to 5 and then two practice block packs is a manageable load"),
    ("Quiz 6 (waived)", "Quiz 6 (not assigned; does not count)"),
    ("A6 · Cleaning notebook and data quality statement (waived)", "A6 · Cleaning notebook and data quality statement (not assigned; does not count)"),
]


def syllabi():
    for f in ("IUEA_ML_Syllabus_CohortA_Design_and_Infrastructure.docx", "IUEA_ML_Syllabus_CohortB_Mining_and_Petroleum.docx", "IUEA_ML_Syllabus_CohortC_Engineering.docx"):
        p = BASE / f
        rules = list(SYL_RULES)
        docx_edit(p, rules, required=False)
        syl_table(p)


def syl_table(path):
    from docx import Document
    d = Document(str(path)); t = None; before = [x.text for x in iter_pars(d)]
    for tb in d.tables:
        if tb.rows and tb.rows[0].cells[0].text.strip() == "Component" and "Weight" in tb.rows[0].cells[3].text: t = tb; break
    if t is None: MISSING.append(f"{path.name}: weight table missing"); return
    def setc(cell, text):
        ps = cell.paragraphs
        if ps and ps[0].runs:
            ps[0].runs[0].text = text
            for r in ps[0].runs[1:]: r.text = ""
        elif ps: ps[0].add_run(text)
    ch = False
    for row in t.rows[1:]:
        k = row.cells[0].text.strip()
        if k.startswith("Quizzes"):
            setc(row.cells[0], "Quizzes: weekly in Weeks 1–5 (Q1 to Q5 count)")
            setc(row.cells[1], "Weeks 1–5 weekly. Block 1 (Q7, Q8) in the last 20 minutes of Class 2 and Block 2 (Q9, Q10) in the last 20 minutes of Class 4 are practice")
            setc(row.cells[3], "20%")
            setc(row.cells[4], "Five multiple-choice questions on your phone per form, auto-marked with immediate feedback. Weeks 1 to 5 are weekly five-minute quizzes (Q1 to Q5): each is out of 5, all five count equally, and together they are worth 20%. From Week 8 the two forms of a block are sat together (Block 1: Q7 and Q8; Block 2: Q9 and Q10), each form open for 24 hours; they are practice and do not count toward the final mark, but feedback is given. Week 6 is not assigned and Q11 and Q12 are retired. There is no best-of rule.")
            ch = True
        elif k.startswith("Practical challenges"):
            setc(row.cells[0], "Practical challenges and assignments")
            setc(row.cells[1], "Weekly in Weeks 1–5 (A1 to A5 count). Block 1 pack (A7, A8) closes 17 November 11:00 and Block 2 pack (A9, A10, A11) closes 1 December 11:00 (Kampala time); both are practice")
            setc(row.cells[3], "20%")
            setc(row.cells[4], "All five of A1 to A5 count equally (each marked out of 20, 100 raw, scaled to 20). The Block 1 and Block 2 packs (A7 to A11) are practice: they use the same assignment forms, are collected and given feedback, but do not count toward the final mark. Upload the required notebook and report through the assignment form. Visible checks provide practice feedback; final marks use the submitted files.")
            ch = True
        elif k.startswith("Data Analysis Project"):
            setc(row.cells[0], "Data Analysis Project (practice)")
            setc(row.cells[3], "0%")
            setc(row.cells[4], "Does not count toward the final mark from 10 November 2026. Cleaned dataset, question-driven analysis, four or more charts, one page of findings. An individual contribution log is required.")
            ch = True
        elif k.startswith("Practical Test 1"):
            setc(row.cells[3], "20%"); ch = True
        elif k.startswith("Engineering ML Project"):
            setc(row.cells[3], "40%")
            c4 = row.cells[4].text
            c4 = c4.replace("Part A, the coded project notebook (30 marks, hidden checks on unseen data), and Part B, a structured decision memo form inside the notebook (15 marks, automatic).",
                            "Part A, the coded project notebook (30 marks, hidden checks on unseen data), and Part B, a structured decision memo form inside the notebook (15 marks, automatic); the 45 marks are scaled to 40.")
            c4 = c4.replace("it is shown as provisional, out of 55 marks, with the project PENDING.", "it is shown as provisional, out of 60 marks, with the project PENDING.")
            setc(row.cells[4], c4); ch = True
    if ch and [x.text for x in iter_pars(d)] != before:
        if not DRY: d.save(str(path))
        note_changed(path)


MASTER_RULES = [
    ("fifty-five per cent of the mark is now genuinely continuous, accumulated across five weekly assignments, five weekly quizzes, two block packs, two block quiz sittings, a team project and a practical test, rather than concentrated in one or two events.",
     "sixty per cent of the mark is now genuinely continuous, accumulated across five weekly assignments, five weekly quizzes and a practical test, rather than concentrated in one or two events. The two block packs and two block quiz sittings are still set as practice but do not count."),
    ("Ninety per cent of the mark is individual on the component modes in the table above (the quizzes, the assignments, Practical Test 1 and the Engineering ML project). The Data Analysis Project (10 per cent) is a team mark. The Engineering ML project (45 per cent) is an individual",
     "All of the mark is individual on the component modes in the table above (the assignments, the quizzes, Practical Test 1 and the Engineering ML project). The Data Analysis Project no longer counts toward the final mark. The Engineering ML project (40 per cent) is an individual"),
    ("The end-to-end work of Weeks 8 to 11 is now assessed in the Block 1 and Block 2 assignments and quizzes and in the Engineering ML project",
     "The end-to-end work of Weeks 8 to 11 is practised in the Block 1 and Block 2 assignments and quizzes (practice, collected with feedback, not counted) and assessed in the Engineering ML project"),
    ("the best three of the five count; Week 6 is waived for all three cohorts.", "all five count (Q1 to Q5, 20 per cent of the course); Week 6 is not assigned."),
    ("And there are no resits: only the best three of the five weekly quizzes count, so a student who misses two sessions, or a cohort that loses one to a network failure, is not penalised at all.",
     "And there are no resits: all five weekly quizzes count equally, so a cohort that loses one to a network failure is given the 24-hour asynchronous window."),
    ("each quiz mark is a small part of the 35-mark quiz total", "each quiz mark is a small part of the 25-mark quiz total (scaled to 20)"),
    ("Fifteen per cent of the mark sits in Practical Test 1", "Twenty per cent of the mark sits in Practical Test 1"),
    ("The project is marked out of 45, all of it automatically:", "The project is marked out of 45, scaled to 40, all of it automatically:"),
    ("Until both project columns are marked it shows a provisional Semester 1 result out of 55 marks with the project PENDING", "Until both project columns are marked it shows a provisional Semester 1 result out of 60 marks with the project PENDING"),
    ("which rests on the ninety per cent individual mark (the quizzes, the assignments, Practical Test 1 and the Engineering ML project, which is sat alone), and the contribution log with repository evidence for the Data Analysis Project.",
     "which rests on a fully individual mark (the assignments, the quizzes, Practical Test 1 and the Engineering ML project, which is sat alone), and the contribution log with repository evidence for the Data Analysis Project, which is set as practice and no longer counts."),
    ("Week 7 was Practical Test 1 and Week 6 was waived.", "Week 7 was Practical Test 1 and Week 6 was not assigned."),
    ("Assessment. Weeks 1 to 5 stay weekly (best 3 of 5). Block 1 is A7 (Regression and baseline) plus A8 (Classification and cost) with Q7 and Q8, sat together in the last 20 minutes of Class 2. Block 2 is A9, A10 and A11 with Q9 and Q10, sat in the last 20 minutes of Class 4. Weights: quizzes 15, assignments 15, Data Analysis Project 10 (still a team project, teams of 4 to 5 formed in Week 1), Practical Test 1 15, Engineering ML project 45. Semester 1 results can be published provisionally out of 55 with the project pending. Detail: Block_Assessment_Arrangement_2026-11-03.md.",
     "Assessment. From 10 November 2026 the final mark is assignments 20 (A1 to A5, all five count) + quizzes 20 (Q1 to Q5, all five count) + Practical Test 1 20 + Engineering ML project 40. Block 1 is A7 (Regression and baseline) plus A8 (Classification and cost) with Q7 and Q8, sat together in the last 20 minutes of Class 2. Block 2 is A9, A10 and A11 with Q9 and Q10, sat in the last 20 minutes of Class 4. The blocks are practice: still done and given feedback, but not counted. The Data Analysis Project (teams of 4 to 5 formed in Week 1) is also practice and no longer counts. Semester 1 results can be published provisionally out of 60 with the project pending. Detail: Grading_Policy_2026-11-10.md."),
    ("Assessment. Block 1 sitting: A7 and A8, and the Q7 and Q8 quizzes, are sat together in the last 20 minutes of this class.",
     "Assessment. Block 1 sitting (practice, does not count toward the final mark): A7 and A8, and the Q7 and Q8 quizzes, are sat together in the last 20 minutes of this class."),
    ("Assessment. Proposed Block 1 assignment deadlines (A7 and A8):", "Assessment. Proposed Block 1 (practice) assignment deadlines (A7 and A8):"),
    ("Assessment. Block 2 sitting: A9, A10 and A11, and the Q9 and Q10 quizzes, in the last 20 minutes.", "Assessment. Block 2 sitting (practice, does not count toward the final mark): A9, A10 and A11, and the Q9 and Q10 quizzes, in the last 20 minutes."),
    ("and neither block can be dropped. Q11 and Q12 are retired. The quiz total is 35 marks (3 x 5 + 10 + 10), worth 15% of the course. Assignments follow the same rule: the best 3 of the five weekly assignments, Block 1 (A7 + A8 = 40 marks) and Block 2 (A9 + A10 + A11 = 60 marks), a total of 160 marks, worth 15%. Full details: Block_Assessment_Arrangement_2026-11-02.md.",
     "and both blocks are practice: they are sat and given feedback but do not count toward the final mark. Q11 and Q12 are retired. The counted quizzes Q1 to Q5 total 25 marks, scaled to 20 (20% of the course). Assignments follow the same rule: all five of A1 to A5 count (100 marks, scaled to 20, worth 20%), while Block 1 (A7 + A8 = 40 marks) and Block 2 (A9 + A10 + A11 = 60 marks) are practice. Full details: Grading_Policy_2026-11-10.md."),
    ("gives a fifty-five / forty-five split without altering", "gives a sixty / forty split without altering"),
    ("counts 45 percent of the course", "counts 40 percent of the course"),
    ("Block 1 quiz (Q7, Q8) in the last 20 minutes.", "Block 1 quiz (Q7, Q8; practice) in the last 20 minutes."),
    ("Block 2 quiz (Q9, Q10) in the last 20 minutes.", "Block 2 quiz (Q9, Q10; practice) in the last 20 minutes."),
    ("Block 1 assignment (A7, A8) closes:", "Block 1 assignment (A7, A8; practice) closes:"),
    ("Block 2 assignment (A9, A10, A11) closes:", "Block 2 assignment (A9, A10, A11; practice) closes:"),
]


def master_docx():
    p = BASE / "IUEA_ML_Semester1_Master_Teaching_Plan.docx"
    docx_edit(p, MASTER_RULES, required=False)
    from docx import Document
    d = Document(str(p)); ch = False; before = [x.text for x in iter_pars(d)]
    def setc(cell, text):
        ps = cell.paragraphs
        if ps and ps[0].runs:
            ps[0].runs[0].text = text
            for r in ps[0].runs[1:]: r.text = ""
        elif ps: ps[0].add_run(text)
    for t in d.tables:
        for row in t.rows:
            seen = []; cells = []
            for c in row.cells:
                if c._tc in seen: continue
                seen.append(c._tc); cells.append(c)
            k = cells[0].text.strip()
            if k.startswith("Quizzes (weekly in Weeks 1–5") and len(cells) >= 4:
                setc(cells[0], "Quizzes (Q1 to Q5, weekly in Weeks 1–5)"); setc(cells[1], "W1–W5 weekly. Block quizzes (Q7 to Q10) are practice and do not count"); setc(cells[3], "20%"); ch = True
            elif k.startswith("Practical challenges and assignments (weekly") and len(cells) >= 4:
                setc(cells[0], "Practical challenges and assignments (A1 to A5, weekly in Weeks 1–5)"); setc(cells[1], "Weeks 1–5. The Block 1 and Block 2 packs (A7 to A11) are practice and do not count"); setc(cells[3], "20%"); ch = True
            elif k.startswith("Data Analysis Project") and len(cells) >= 4 and cells[-1].text.strip() == "10%":
                setc(cells[0], "Data Analysis Project (practice, does not count)"); setc(cells[-1], "0%"); ch = True
            elif k.startswith("Practical Test 1") and len(cells) >= 4 and cells[-1].text.strip() == "15%":
                setc(cells[-1], "20%"); ch = True
            elif k.startswith("Engineering ML Project") and len(cells) >= 4 and cells[-1].text.strip() == "45%":
                setc(cells[-1], "40%"); ch = True
            elif k.startswith("Individual share of the total mark"):
                setc(cells[-1], "100%"); ch = True
            elif k.startswith("Team share of the total mark"):
                setc(cells[-1], "0% (the Data Analysis Project no longer counts)"); ch = True
            elif k.startswith("Continuous assessment (55%)"):
                setc(cells[0], "Continuous assessment (60%)"); setc(cells[1], "Quizzes 20% · Practical challenges and assignments 20% · Practical Test 1 20% (the Data Analysis Project and the Week 8 to 11 block work do not count)"); setc(cells[-1], "60%"); ch = True
            elif k.startswith("Final assessment (45%)"):
                setc(cells[0], "Final assessment (40%)"); setc(cells[1], "Engineering ML Project 40% (Part A 30 + Part B 15 = 45, scaled to 40)"); setc(cells[-1], "40%"); ch = True
    if ch and [x.text for x in iter_pars(d)] != before:
        if not DRY: d.save(str(p))
        note_changed(p)


def other_docx():
    docx_edit(BASE / "IUEA_ML_Weekly_Quiz_Operations_Guide.docx", QUIZOPS_RULES, required=False)
    docx_edit(BASE / "IUEA_ML_Lecturer_Teaching_Guide_W1-W15.docx", [
        ("Week 7 was Practical Test 1 and Week 6 was waived.", "Week 7 was Practical Test 1 and Week 6 was not assigned."),
        ("Assessment. Weeks 1 to 5 stay weekly (best 3 of 5). Block 1 is A7 (Regression and baseline) plus A8 (Classification and cost) with Q7 and Q8, sat together in the last 20 minutes of Class 2. Block 2 is A9, A10 and A11 with Q9 and Q10, sat in the last 20 minutes of Class 4. Weights: quizzes 15, assignments 15, Data Analysis Project 10 (still a team project, teams of 4 to 5 formed in Week 1), Practical Test 1 15, Engineering ML project 45. Semester 1 results can be published provisionally out of 55 with the project pending. Detail: Block_Assessment_Arrangement_2026-11-03.md.",
         "Assessment. From 10 November 2026 the final mark is assignments 20 (A1 to A5, all five count) + quizzes 20 (Q1 to Q5, all five count) + Practical Test 1 20 + Engineering ML project 40. Block 1 is A7 (Regression and baseline) plus A8 (Classification and cost) with Q7 and Q8, sat together in the last 20 minutes of Class 2. Block 2 is A9, A10 and A11 with Q9 and Q10, sat in the last 20 minutes of Class 4. The blocks are practice: still done and given feedback, but not counted. The Data Analysis Project (teams of 4 to 5 formed in Week 1) is also practice and no longer counts. Semester 1 results can be published provisionally out of 60 with the project pending. Detail: Grading_Policy_2026-11-10.md."),
        ("Assessment. Block 1 sitting: A7 and A8, and the Q7 and Q8 quizzes,", "Assessment. Block 1 sitting (practice, does not count toward the final mark): A7 and A8, and the Q7 and Q8 quizzes,"),
        ("Assessment. Block 2 sitting: A9, A10 and A11, and the Q9 and Q10 quizzes,", "Assessment. Block 2 sitting (practice, does not count toward the final mark): A9, A10 and A11, and the Q9 and Q10 quizzes,"),
        ("counts 45 percent of the course", "counts 40 percent of the course (Part A 30 + Part B 15 = 45 marks, scaled to 40)"),
    ], required=False)


XLSX_REGEX = [
    (r"Worth 1 of the 35 quiz marks \(quizzes are 15% of the course\); the best 3 of the five weekly quizzes count, Week 6 is waived, no resits\.",
     "Out of 5 marks. Q1 to Q5 all count equally and together are 20% of the course; no resits."),
    (r"contributes to Practical Challenges & Assignments \(15%; best 3 of the five weekly assignments count\)", "contributes to Practical Challenges & Assignments (20%; all five of A1 to A5 count equally)"),
    (r"A2 is one of the five weekly assignments in Weeks 1 to 5, of which the best three count \(Week 6 is waived\), and the assignments are 15% of the course\. The Week 2 quiz is one of the five weekly quizzes, of which the best three count, and the quizzes are 15% of the course\.",
     "A2 is one of the five weekly assignments A1 to A5, all of which count equally (20% of the course). The Week 2 quiz is one of the five quizzes Q1 to Q5, all of which count equally (20% of the course)."),
    (r"The Data Analysis Project is 10% in its own right\.", "The Data Analysis Project no longer counts toward the final mark (it is practice)."),
    (r"A6 is waived for all three cohorts and does not count towards the assignments \(15%\)\.", "A6 is not assigned for any cohort and does not count (only A1 to A5 count, 20%)."),
    (r"PRACTICAL TEST 1 = 15% of the Semester 1 mark\.", "PRACTICAL TEST 1 = 20% of the Semester 1 mark."),
    (r"DATA ANALYSIS PROJECT DUE \(10%\)\.", "DATA ANALYSIS PROJECT DUE (practice, does not count)."),
    (r"A(\d+) is part (A|B|C) of Block (\d) \(((?:A\d+ \+ )+A\d+) = (\d+) marks; the assignments are 15% of the course\)", r"A\1 is part \2 of Block \3 (\4 = \5 marks; practice, does not count toward the final mark)"),
    (r"A10 and A11 are parts B and C of Block 2 \(A9 \+ A10 \+ A11 = 60 marks; the assignments are 15% of the course\)", "A10 and A11 are parts B and C of Block 2 (A9 + A10 + A11 = 60 marks; practice, does not count toward the final mark)"),
    (r"Data Analysis Project is submitted and marked \(10%\)\.", "Data Analysis Project is submitted and marked (practice, does not count)."),
    (r"The Engineering ML Project \(45%\) is introduced", "The Engineering ML Project (40%) is introduced"),
    (r"ENGINEERING ML PROJECT brief given in this class \(45%\)", "ENGINEERING ML PROJECT brief given in this class (40%)"),
    (r"Engineering ML Project \(45%\)", "Engineering ML Project (40%)"),
    (r"Engineering ML project \(45%\)", "Engineering ML project (40%)"),
    (r"Block 1 quiz \(Q7, Q8\) in the last 20 minutes\.", "Block 1 quiz (Q7, Q8; practice) in the last 20 minutes."),
    (r"Block 2 quiz \(Q9, Q10\) in the last 20 minutes\.", "Block 2 quiz (Q9, Q10; practice) in the last 20 minutes."),
    (r"Block 1 assignment \(A7, A8\) closes", "Block 1 assignment (A7, A8; practice) closes"),
    (r"Block 2 assignment \(A9, A10, A11\) closes", "Block 2 assignment (A9, A10, A11; practice) closes"),
    (r"Contact hours per cohort: 36 \(12 sessions of 3 hours; Week 6 is waived for the quiz and assignment\)", "Contact hours per cohort: 36 (12 sessions of 3 hours; Week 6 has no quiz or assignment)"),
    (r"the alternative mapping on that same sheet records a 55/45 split under the new weights", "the alternative mapping on that same sheet records a 60/40 split under the new weights"),
    (r"\(the project rubric sums to its 45 marks\)", "(the project rubric sums to its 45 marks, scaled to 40)"),
    (r"the Engineering ML project parts sum to its 45 marks\.", "the Engineering ML project parts sum to its 45 marks, scaled to 40."),
    (r"calculate weights, apply best-of rules and flag missing work\. Until both project columns are marked it shows a provisional Semester 1 result out of 55 marks",
     "calculate weights (all five of A1 to A5 and Q1 to Q5 count) and flag missing work. Until both project columns are marked it shows a provisional Semester 1 result out of 60 marks"),
    (r"Best 3 of the five weekly quizzes and the 24-hour block window provide some flexibility", "The 24-hour block window provides some flexibility (all five of Q1 to Q5 count, so there is no best-of cushion)"),
    (r"Practical Test 1 - Data Investigation \(15%\)", "Practical Test 1 - Data Investigation (20%)"),
    (r"Data Analysis Project \(10%\)", "Data Analysis Project (practice, does not count)"),
    (r"Quizzes \(15%\) - how the five questions", "Quizzes (20%) - how the five questions"),
]


def master_xlsx():
    import openpyxl
    p = BASE / "IUEA_ML_Semester1_Master_Teaching_Plan.xlsx"
    wb = openpyxl.load_workbook(str(p)); n = 0
    for ws in wb:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and not c.value.startswith("="):
                    v = c.value
                    for pat, rep in XLSX_REGEX: v = re.sub(pat, rep, v)
                    if v != c.value: c.value = v; n += 1
    ws = wb["Assessment"]
    def S(a, v):
        nonlocal n
        if ws[a].value != v: ws[a].value = v; n += 1
    S("A2", "Entirely practical, continuous and project-based. No traditional written examination. All of the mark is individual on the component modes below (assignments, quizzes, Practical Test 1 and the Engineering ML project, an individual timed 3-hour sitting that is auto-graded); automatic grading coverage is validated assessment by assessment. Policy of 10 November 2026: see Grading_Policy_2026-11-10.md.")
    S("A6", "QUIZZES (Q1 to Q5, weekly in Weeks 1-5)")
    S("B6", "W1-W5 weekly. Block quizzes Q7 to Q10 (last 20 minutes of Class 2 and Class 4) are practice and do not count")
    S("D6", 0.2)
    S("E6", "Five diagnostic questions per form, one mark each. Q1 to Q5 are each out of 5 and all five count equally (25 raw, scaled to 20), worth 20%. Weeks 1-5: a five-minute QR-code quiz in the last five minutes. The block quizzes are practice: sat, marked and given feedback, but not counted. Instant score and teaching feedback. No resits. A network failure is covered by the 24-hour window.")
    S("A7", "Practical challenges & assignments (A1 to A5, weekly in Weeks 1-5)")
    S("B7", "Weeks 1-5 weekly (A1 to A5). A6 onward and the Block 1 (A7, A8) and Block 2 (A9, A10, A11) packs are practice and do not count")
    S("D7", 0.2)
    S("E7", "Weekly notebooks, scripts and one-pagers pushed to the repository. Students self-check against visible tests before submitting; the lecturer batch-grades against hidden tests. All five of A1 to A5 count equally (each out of 20, 100 raw, scaled to 20), worth 20%. The block packs are practice: collected and given feedback, but not counted.")
    S("A8", "Data Analysis Project (practice, does not count)")
    S("D8", 0)
    S("F8", "Does not count toward the final mark from 10 November 2026. Data Analysis Project rubric (see Rubrics sheet) is kept for the practice feedback.")
    S("D9", 0.2)
    S("D10", 0.4)
    if "scaled to 40" not in (ws["E10"].value or ""):
        S("E10", (ws["E10"].value or "").replace("Part B: structured decision memo form inside the notebook, 15 marks, checked automatically.", "Part B: structured decision memo form inside the notebook, 15 marks, checked automatically. The 45 marks are scaled to 40."))
    S("F12", "Quizzes, assignments, Practical Test 1 and the Engineering ML project (40%) are individually assessed.")
    S("A13", "Of which team (Data Analysis Project, no longer counted)")
    S("F13", "The Data Analysis Project is a team piece of practice work and carries no weight.")
    S("A19", "CONTINUOUS ASSESSMENT (60%)")
    S("B20", "W1-W5 weekly (Q1 to Q5)"); S("D20", 0.2); S("E20", "All five count equally; 25 raw, scaled to 20. Block quizzes are practice")
    S("B21", "Weeks 1-5 (A1 to A5)"); S("D21", 0.2); S("E21", "All five count equally; 100 raw, scaled to 20. Block packs are practice")
    S("A22", "Data Analysis Project (practice)"); S("D22", 0); S("E22", "Does not count")
    S("D23", 0.2)
    S("A24", "FINAL ASSESSMENT (40%)")
    S("D25", 0.4)
    S("A32", "Why 100% individual")
    S("B32", "With teams of 4–5 and up to 22 teams in Cohort A, a team-heavy mark scheme would let a weak student pass on a strong teammate's work. From 10 November 2026 every counted component is individual: the assignments, the quizzes, Practical Test 1 and the auto-graded Engineering ML sitting. The Data Analysis Project is still done in teams as practice and carries no weight.")
    S("B33", "Five auto-graded quizzes and five graded assignments (A1 to A5) mean 40% of the mark comes from these recurring components, with Practical Test 1 bringing continuous assessment to 60%. Quiz feedback is immediate; local assignment grading runs after collection, and the lecturer gets a weekly engagement signal across ~195 students that is otherwise invisible until the first test. See the 'Assessment Tech Stack' and 'Marking Load' sheets for how this is affordable for one person. From Week 8 the quizzes and assignments are set in two practice blocks that are collected with feedback but do not count.")
    if n:
        if not DRY: wb.save(str(p))
        note_changed(p)


def submission_forms_gs():
    """Re-embed the ML_PROJECT student guide as the form brief (the only brief that is a verbatim copy of its guide). Same logic as build_submission_forms.py
    but touches only the briefs, so it does not re-embed the registry (which another session is changing)."""
    p = BASE / "grader/submission_forms.gs"; s = p.read_text(encoding="utf-8")
    a = s.index("var ASSESSMENTS = ") + len("var ASSESSMENTS = "); b = s.index("\n", a)
    line = s[a:b]; assert line.endswith(";"), "unexpected ASSESSMENTS line"
    rows = json.loads(line[:-1]); n = 0
    for r in rows:
        if r.get("track") != "IUEA" or r.get("id") not in ("ML_PROJECT", "DA_PROJECT"): continue
        g = BASE / "student_guides" / r["cohort"] / (r["id"] + ".md")
        if g.exists() and r.get("brief") != g.read_text(encoding="utf-8"):
            r["brief"] = g.read_text(encoding="utf-8"); n += 1
    if n:
        new = s[:a] + json.dumps(rows, ensure_ascii=True, separators=(",", ":")) + ";" + s[b:]
        assert all(ord(ch) < 128 for ch in new[a:b + 1 + len(new) - len(s)]), "non-ASCII in generated line"
        if not DRY: p.write_text(new, encoding="utf-8")
        note_changed(p)


SH_RULES = [
    ("Block 1 is Classes 1 and 2. Its assignment has two parts: A7 (regression) and A8 (classification).",
     "Block 1 is Classes 1 and 2. Its assignment has two parts: A7 (regression) and A8 (classification). It is practice: it does not count toward your final mark, but it is collected and you get feedback."),
    ("Block 1 is Class 1 and Class 2.", "Block 1 is Class 1 and Class 2. It is practice: it does not count toward your final mark."),
    ("A10 (features) and A11 (model recommendation), both from Class 4.", "A10 (features) and A11 (model recommendation), both from Class 4. Block 2 is practice: it does not count toward your final mark, but it is collected and you get feedback."),
    ("The Block 2 quiz opens in the last 20 minutes of this class and stays open for 24 hours.", "The Block 2 quiz opens in the last 20 minutes of this class and stays open for 24 hours. It is practice and does not count toward your final mark."),
    ("A word on how this counts.", "A word on how this counts. The block work is practice: it does not count toward your final mark (only A1 to A5 and Q1 to Q5 do), but it is collected and you get feedback."),
]
SH_PPTX_RULES = PROJECT_RULES + SH_RULES


def second_half_sources():
    sh = BASE / "second_half/Build"
    for f in list((sh / "content").glob("c[1-4].py")) + list((sh / "_specs").glob("*.json")):
        edit_text(f, SH_RULES, required=False)


def pptx_patch(path, rules):
    from pptx import Presentation
    path = Path(path); prs = Presentation(str(path)); changed = False
    def paras(shapes):
        for sh in shapes:
            if sh.shape_type == 6 and hasattr(sh, "shapes"):
                yield from paras(sh.shapes)
            if getattr(sh, "has_text_frame", False) and sh.has_text_frame:
                yield from sh.text_frame.paragraphs
            if getattr(sh, "has_table", False) and sh.has_table:
                for r in sh.table.rows:
                    for c in r.cells: yield from c.text_frame.paragraphs
    def fix(par):
        nonlocal changed
        for old, new in rules:
            if old in par.text:
                if not para_text_replace(par, old, new): continue
                changed = True
    for s in prs.slides:
        for par in paras(s.shapes): fix(par)
        if s.has_notes_slide:
            for par in s.notes_slide.notes_text_frame.paragraphs: fix(par)
    if changed:
        if not DRY: prs.save(str(path))
        note_changed(path)


def second_half_decks():
    for f in sorted((BASE / "second_half/Slides").rglob("*.pptx")):
        if f.name.startswith("~$"): continue
        pptx_patch(f, SH_PPTX_RULES)


def rewrite_zip(zpath, replacements):
    """Replace named members of a zip with new bytes, keeping order, compression and timestamps of the others."""
    import zipfile, io
    zpath = Path(zpath)
    if not zpath.exists(): MISSING.append(f"{zpath.name}: missing"); return
    with zipfile.ZipFile(zpath) as z:
        items = [(i, z.read(i.filename)) for i in z.infolist()]
    names = {i.filename for i, _ in items}
    changed = False; buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as out:
        for info, data in items:
            new = replacements.get(info.filename)
            if new is not None and new != data: data = new; changed = True
            zi = zipfile.ZipInfo(info.filename, info.date_time); zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = info.external_attr; zi.create_system = info.create_system
            out.writestr(zi, data)
    for n in replacements:
        if n not in names: MISSING.append(f"{zpath.name}: no member {n}")
    if changed:
        if not DRY: zpath.write_bytes(buf.getvalue())
        note_changed(zpath)


def student_package_zips():
    """student_packages/<cohort>_W0x_student.zip are what students download: START_HERE.md is the student guide and W0x_student.ipynb is the bank notebook."""
    for c in COHORTS:
        for w in ("W08", "W09", "W10", "W11", "W12"):
            rewrite_zip(BASE / "student_packages" / f"{c}_{w}_student.zip", {
                "START_HERE.md": (BASE / "student_guides" / c / f"{w}.md").read_bytes(),
                f"{w}_student.ipynb": (BASE / "assessment_banks" / w / c / "A" / f"{w}_student.ipynb").read_bytes()})
        if c != "CML3111":
            rewrite_zip(BASE / "student_packages" / f"{c}_W06_student.zip", {"00_START_HERE.txt": (BASE / "student_guides" / c / "W06.md").read_bytes()})


def working_copy():
    d = BASE / "student_packages/CML3113_W08_student"
    for src, name in ((BASE / "student_guides/CML3113/W08.md", "START_HERE.md"), (BASE / "assessment_banks/W08/CML3113/A/W08_student.ipynb", "W08_student.ipynb")):
        f = d / name
        if f.exists() and f.read_bytes() != src.read_bytes():
            if not DRY: f.write_bytes(src.read_bytes())
            note_changed(f)

# ------------------------------------------------------------------------------------------------ main
def main():
    history_banners(); living_markdown(); student_guides(); project_text(); builders(); stale_builders(); data_files(); submission_forms_gs(); second_half_sources(); student_package_zips(); working_copy()
    try:
        import docx, openpyxl  # noqa
        syllabi(); master_docx(); other_docx(); master_xlsx(); second_half_decks()
    except ImportError:
        MISSING.append("python-docx/openpyxl not available: docx and xlsx parts skipped (use .iuea-grader-env)")
    print(("DRY RUN: " if DRY else "") + f"{len(CHANGED)} files changed")
    for c in CHANGED: print("  changed", c)
    for m in MISSING: print("  NOTE", m)


if __name__ == "__main__":
    main()
