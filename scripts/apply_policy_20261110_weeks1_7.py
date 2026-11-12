#!/usr/bin/env python3
"""SECOND SECTION of the 10 November 2026 grading-policy pass: the DELIVERED Weeks 1 to 7 teaching material.

Companion to scripts/apply_policy_20261110.py (living documents). Source of truth: data/assessment_policy_20261110.json,
plain note IUEA_Teaching_Plan/Grading_Policy_2026-11-10.md.
  Final mark /100 = assignments 20 (A1 to A5, all five equal, 4 each) + quizzes 20 (Q1 to Q5, all five equal, 4 each)
                    + Practical Test 1 20 + Engineering ML project 40 (individual timed Colab sitting, Week 12).
  Not counted: Q6 onward, A6 onward (incl. Week 8 to 11 blocks), Data Analysis project, Practical Test 2, demo.
  Retired: best-3-of-5, best ten of twelve, the Week 6 waiver, the block rule, the 65 percent individual share.

What it patches (idempotent: a replacement already applied is skipped):
  1. IUEA_Teaching_Plan/decks/CML311x_Week0[1-7]_*.pptx : slide text (incl. tables/groups) and speaker notes, runs edited in place;
     the weights chart picture on Week 1 slide 8 is replaced by figs/assessment_20261110.png (made by scripts/make_figures.py).
  2. IUEA_Teaching_Plan/decks/lecturer_notes/*Week0[1-7]*.md  (text dumps of the decks).
  3. Week 6 student files (assessment_banks/W06, guided_practice/*/W06) that said "waived".
  4. The sources that regenerate the decks, so a rebuild does not undo the patch: data/*.json and scripts/build_*.py text.
     NB the Week 1 slide 9 text was created by scripts/patch_blocks_20261030.py (a later layer than build_week1.py); this
     script is the newest layer and must be run after those patches when decks are rebuilt.
Not touched on purpose: dated history notes, _backup_*, archive, second_half, the lecturer's other session's files.
Usage: source .iuea-grader-env/bin/activate; python scripts/apply_policy_20261110_weeks1_7.py [--dry]
"""
import re, sys, glob
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]; BASE = ROOT / "IUEA_Teaching_Plan"
DRY = "--dry" in sys.argv
CHANGED = {}; NOT_FOUND = []

COUNT_A = "Weeks 1 to 5: a quiz and an assignment each week. All five of each count, worth 4 of 20 marks each. Week 6 is practice."

# ---------------------------------------------------------------- the replacement rules (old, new), sentence level
PAIRS = [
    # --- Week 1 slide 8: weights
    ("Individual work accounts for 65% of the mark.", "All of the mark is individual work."),
    ("Individual work accounts for sixty five per cent of the mark. That means most of your result depends on what you can do yourself.",
     "All of the mark is individual work. That means your result depends on what you can do yourself."),
    ("Individual work accounts for sixty-five per cent of the mark.", "All of the mark is individual work."),
    # --- Week 1 slide 9: how quizzes and assignments count
    ("Weeks 1 to 5: a quiz and an assignment each week, and the best 3 of the 5 count. Week 6 is waived.", COUNT_A),
    ("Block 1 is Weeks 8 to 10 and Block 2 is Weeks 11 to 13. Each block has one assignment pack and one quiz.",
     "Block 1 is Weeks 8 and 9 and Block 2 is Weeks 10 and 11. Each block has an assignment pack and a quiz."),
    ("A block counts in full and cannot be dropped. Together the two blocks carry about 60 percent of the quiz and assignment marks.",
     "Block work is practice: it is marked and you get feedback, but it does not count toward the final mark."),
    ("In Weeks 1 to 6 you have a short quiz and an assignment each week, and your best four of the six count, so two weak weeks do not hurt you.",
     "In Weeks 1 to 5 you have a short quiz and an assignment each week, and all five quizzes and all five assignments count. "
     "The assignments carry twenty marks and the quizzes carry twenty marks, so each one is worth four. Week 6 is practice and does not count."),
    ("From Week 8 we assess every three classes. Block 1 covers Weeks 8 to 10 and Block 2 covers Weeks 11 to 13. Each block has one assignment pack and one quiz, and each is handed in or sat after the third class of the block.",
     "From Week 8 we assess in two blocks of two classes. Block 1 covers Weeks 8 and 9 and Block 2 covers Weeks 10 and 11. Each block has an assignment pack and a quiz, handed in or sat at the end of the block."),
    ("A block counts in full and cannot be dropped, because it holds three weeks of learning. Together the two blocks carry about sixty percent of the quiz and assignment marks. The two practical tests, the projects and the demonstration are unchanged.",
     "Block work is practice: it is marked and you get feedback, but it does not count toward the final mark. Only Assignments 1 to 5 and Quizzes 1 to 5 count. "
     "Practical Test 1 is worth twenty marks, and the Engineering ML Project, an individual timed sitting in Week 12, is worth forty."),
    # --- Week 1 slide 5: semester arc
    ("Weeks 7 and 14 are practical tests: you are given data you have never seen and asked what you make of it. The project runs from Week 9 to the last session.",
     "Week 7 is Practical Test 1: you are given data you have never seen and asked what you make of it. The project is an individual timed sitting in Week 12."),
    ("Weeks 7 and 14 are practical tests. In a practical test you are given a data set you have never seen before",
     "Week 7 is Practical Test 1. In the test you are given a data set you have never seen before"),
    ("The project runs from Week 9 to the last session. You will work on it in a team, and I will explain how teams work later today.",
     "The Engineering ML project is an individual timed sitting in Week 12, and you prepare for it in class. Later today I will explain how project teams work."),
    # --- Week 1 slide 45: teams and projects
    ("You will do two projects together: a data analysis project due Week 8, and the Engineering ML Project from Week 9 to Week 15.",
     "A team data analysis project due Week 8 (practice, not counted), then the Engineering ML Project: an individual timed sitting in Week 12, worth 40 marks."),
    ("Sixty-five per cent of the mark is individual. Your team keeps a contribution log", "All of the mark is individual. Your team keeps a contribution log"),
    ("In Week 15, each student submits an individual written defence and reflection according to the published brief.",
     "The Engineering ML Project is an individual timed sitting in Week 12, according to the published brief."),
    ("You do two projects together. The first is a data analysis project, and the second is the Engineering ML Project, which runs from Week 9 to Week 15. The slide gives the due week for the first one.",
     "You do a team data analysis project, which is practice and does not count toward the final mark. The Engineering ML Project is different: it is an individual timed sitting in Week 12 and carries forty marks. The slide gives the due week for the data analysis project."),
    ("Sixty five per cent of the mark is individual. Your team keeps", "All of the mark is individual. Your team keeps"),
    ("In Week 15, each student submits an individual written defence and reflection, following the published brief.",
     "The Engineering ML Project itself is an individual timed sitting in Week 12, following the published brief."),
    # --- Week 1 slide 10: weekly deliverables
    ("Eleven small pieces spread over twelve weeks is manageable; nine of them attempted in December is not.",
     "Five assignments and five quizzes in Weeks 1 to 5 all count; none can be dropped."),
    ("Eleven small pieces spread over twelve weeks is manageable.",
     "Five assignments and five quizzes in the first five weeks all count, so none can be dropped, and a missed one scores zero."),
    ("Weekly in Weeks 1 to 6. Every three classes from Week 8.", "Weekly in Weeks 1 to 5. Every two classes from Week 8."),
    # --- Week 1 quiz slide
    ("One mark each; the quiz is out of 5. Tap View score", "One mark each. Tap View score"),
    ("One per cent each. Tap View score and read the feedback.", "One mark each. Tap View score and read the feedback."),
    ("Quiz category: 10%. Best ten of twelve count.", "Quizzes: Q1 to Q5 all count, 4 of the 20 quiz marks each."),
    ("Quiz category: 10%. Best nine of eleven count; Quiz 6 is waived.", "Quizzes: Q1 to Q5 all count, 4 of the 20 quiz marks each."),
    ("The quiz category is ten per cent, and your best ten of twelve count.", "Quizzes 1 to 5 all count, and each is worth four of the twenty quiz marks."),
    ("The quiz category is ten per cent, and your best nine of eleven count because Quiz 6 is waived.", "Quizzes 1 to 5 all count, and each is worth four of the twenty quiz marks."),
    # --- Week 6 (A6 / Quiz 6 are practice, not waived)
    ("This walkthrough supports the existing Week 6 assignment and quiz. Their requirements are unchanged.",
     "This walkthrough is practice for Week 6. A6 and Quiz 6 do not count toward the final mark."),
    ("This walkthrough supports the assignment and the quiz that already exist for week six. Their requirements have not changed.",
     "This walkthrough is practice for week six. Assignment six and quiz six do not count toward the final mark."),
    ("The waiver covers only this assignment and quiz and does not cancel other assessments.",
     "This applies only to this assignment and quiz: Assignments 1 to 5 and Quizzes 1 to 5 all count."),
    ("Assignment six and quiz six are waived for CML3112.", "Assignment six and quiz six are not assigned for CML3112, and they do not count toward the final mark."),
    ("Assignment six and quiz six are waived, so no upload is required.", "Assignment six and quiz six are not assigned and do not count, so no upload is required."),
    ("A6 and Quiz 6 are waived for this cohort. This is ungraded practical revision. No assignment upload or quiz response is required. Previous submissions remain on record but do not count towards coursework marks.",
     "A6 and Quiz 6 are not assigned for this cohort and do not count toward the final mark (only A1 to A5 and Q1 to Q5 count). This is ungraded practical revision. No assignment upload or quiz response is required."),
    ("A6 and Quiz 6 are waived. This is ungraded practice. No submission is required.", "A6 and Quiz 6 are not assigned and do not count toward the final mark. This is ungraded practice. No submission is required."),
    ("A6 and Quiz 6 are waived. No submission is required.", "A6 and Quiz 6 are not assigned. No submission is required."),
    ("A6 and Quiz 6 are waived. No upload is required.", "A6 and Quiz 6 are not assigned. No upload is required."),
    ("A6 and Quiz 6 are waived", "A6 and Quiz 6 are not assigned and do not count"),
]
# regex pairs for cohort-specific variants: (pattern, replacement)
REGEX = [
    (r"A6 and Quiz 6 are not assigned and do not count for (CML311\d)\.", r"A6 and Quiz 6 are not assigned for \1 and do not count toward the final mark."),
    (r"A6 and Quiz 6 are not assigned and do not count for (CML311\d)\b", r"A6 and Quiz 6 are not assigned for \1 and do not count toward the final mark"),
]
# Week 7 notes: Practical Test 1 weight (appended once)
W7_OLD = "The test is marked out of one hundred, and the marks are shared across five parts."
W7_NEW = "The test is marked out of one hundred, and the marks are shared across five parts. The test counts for twenty of the hundred marks of the course."

# leftovers that must not survive in the delivered decks (used by the check)
STALE = re.compile(r"best (3|three|four|ten|nine)\b|best (ten|nine) of|are waived|is waived|Week 6 is waived|65%|[Ss]ixty[- ]five per cent|cannot be dropped|"
                   r"Quiz category: 10|Weeks 7 and 14|Week 15, each|two projects together|from Week 9 to Week 15|waiver covers", re.I)


def note(path):
    p = str(Path(path).relative_to(ROOT)); CHANGED[p] = CHANGED.get(p, 0) + 1


def apply_text(t):
    """Apply every rule to a string; return the new string."""
    for old, new in PAIRS:
        if old in t:
            t = t.replace(old, new)
    for pat, rep in REGEX:
        t = re.sub(pat, rep, t)
    if W7_OLD in t and W7_NEW not in t:
        t = t.replace(W7_OLD, W7_NEW)
    return t


# ------------------------------------------------------------------------------------------------ plain text files
def patch_textfile(path):
    path = Path(path)
    try: t0 = path.read_text(encoding="utf-8")
    except Exception: return
    t = apply_text(t0)
    if t != t0:
        if not DRY: path.write_text(t, encoding="utf-8")
        note(path)


# ------------------------------------------------------------------------------------------------ pptx
def paragraphs(shapes):
    for s in shapes:
        if s.shape_type == 6:
            yield from paragraphs(s.shapes)
        if s.has_text_frame:
            yield from s.text_frame.paragraphs
        if getattr(s, "has_table", False) and s.has_table:
            for r in s.table.rows:
                for c in r.cells:
                    yield from c.text_frame.paragraphs


def fix_paragraph(p):
    old = "".join(r.text for r in p.runs)
    if not old: return False
    new = apply_text(old)
    if new == old: return False
    # prefer an in-run edit so formatting is kept; otherwise put the whole paragraph into the first run
    for r in p.runs:
        rt = apply_text(r.text)
        if rt != r.text:
            r.text = rt
    if "".join(r.text for r in p.runs) != new:
        p.runs[0].text = new
        for r in p.runs[1:]: r.text = ""
    return True


OLD_CHART_SHA1 = "eb83aac352784a7f5605d6406881f6fb22d2b660"


def patch_pptx(path):
    from pptx import Presentation
    prs = Presentation(str(path)); n = 0
    new_img = (ROOT / "figs" / "assessment_20261110.png").read_bytes()
    for sl in prs.slides:
        for p in paragraphs(sl.shapes):
            n += fix_paragraph(p)
        if sl.has_notes_slide:
            for p in sl.notes_slide.notes_text_frame.paragraphs:
                n += fix_paragraph(p)
        for sh in sl.shapes:
            if sh.shape_type == 13 and sh.image.sha1 == OLD_CHART_SHA1:
                rid = sh._element.blipFill.blip.rEmbed
                part = sl.part.related_part(rid)
                part._blob = new_img; n += 1
    if n:
        if not DRY: prs.save(str(path))
        CHANGED[str(Path(path).relative_to(ROOT))] = n


def check_pptx():
    from pptx import Presentation
    left = []
    for f in sorted(glob.glob(str(BASE / "decks" / "CML311*_Week0[1-7]_*.pptx"))):
        prs = Presentation(f)
        for i, sl in enumerate(prs.slides, 1):
            texts = [p.text for p in paragraphs(sl.shapes)]
            if sl.has_notes_slide: texts += [p.text for p in sl.notes_slide.notes_text_frame.paragraphs]
            for t in texts:
                if STALE.search(t): left.append(f"{Path(f).name} slide {i}: {t[:90]}")
    return left


def patch_zip(path):
    """Student packages for Weeks 1 to 7 carry copies of the patched notebooks/instructions; rewrite changed members only."""
    import zipfile, shutil
    path = Path(path)
    with zipfile.ZipFile(path) as zin:
        infos = zin.infolist(); data = {}
        changed = False
        for i in infos:
            b = zin.read(i.filename)
            if i.filename.endswith((".ipynb", ".txt", ".md")):
                try:
                    s = b.decode("utf-8"); s2 = apply_text(s)
                    if s2 != s: b = s2.encode("utf-8"); changed = True
                except UnicodeDecodeError: pass
            data[i.filename] = b
    if not changed: return
    if not DRY:
        tmp = path.with_suffix(".zip.tmp")
        with zipfile.ZipFile(tmp, "w") as zout:
            for i in infos:
                zout.writestr(i, data[i.filename], compress_type=i.compress_type)
        shutil.move(str(tmp), str(path))
    note(path)


def main():
    # 1. decks (Weeks 1 to 7 of the three cohorts); skip lock files
    for f in sorted(glob.glob(str(BASE / "decks" / "CML311*_Week0[1-7]_*.pptx"))):
        patch_pptx(f)
    # 2. lecturer notes md
    for f in sorted(glob.glob(str(BASE / "decks" / "lecturer_notes" / "*Week0[1-7]*.md"))): patch_textfile(f)
    # 3. Week 6 student/lecturer files
    for pat in ("assessment_banks/W06/*/A/*", "guided_practice/*/W06/*"):
        for f in sorted(glob.glob(str(BASE / pat))):
            if Path(f).suffix in (".md", ".txt", ".ipynb"): patch_textfile(f)
    for f in sorted(glob.glob(str(BASE / "student_packages" / "CML311*_W0[1-7]_student.zip"))): patch_zip(f)
    # 4. sources that regenerate the decks
    for rel in ("data/spoken_notes_w1_7_13_15_20261030.json", "data/iuea_deck_content.json", "data/iuea_plain_language_edits.json",
                "data/slide_specific_lecturer_notes.json", "data/reviewed_presentation_notes.json", "data/lecturer_notes_build_w1115.json",
                "scripts/review_week1_material.py", "scripts/pptxkit.py", "scripts/weekly_submission_slide.py", "scripts/simplify_cml3113_week6.py",
                "scripts/stepwise_teaching_expansion.py"):
        if (ROOT / rel).exists(): patch_textfile(ROOT / rel)
    by = {}
    for p in CHANGED: by[Path(p).suffix] = by.get(Path(p).suffix, 0) + 1
    print(("DRY RUN: " if DRY else "") + f"files changed: {len(CHANGED)}  by type: {by}")
    for p in sorted(CHANGED): print("  ", p, CHANGED[p])
    if not DRY:
        left = check_pptx()
        print(f"stale marking phrases still in Weeks 1-7 decks: {len(left)}")
        for l in left: print("   LEFT:", l)


if __name__ == "__main__":
    main()
