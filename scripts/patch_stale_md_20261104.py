#!/usr/bin/env python3
"""Patch stale statements in markdown/text files after the 3-4 November 2026
assessment decision (see IUEA_Teaching_Plan/Block_Assessment_Arrangement_2026-11-03.md
and IUEA_Teaching_Plan/second_half/Plan_Weeks_8-12.pdf).

Current truth: the semester ends at Week 12 (12 study weeks, 36 contact hours).
Weeks 8 to 11 are four classes in second_half/. Week 12 is the individual,
timed, auto-graded Engineering ML project sitting (45 percent). There is no
Practical Test 2, no demo, no Weeks 13 to 15, no clinic.

Scope: live md/txt files of the teaching plan (lecturer notes, checklists,
READMEs, test operations, the old assessment banks for TEST2 and ML_PROJECT).
Historical records only receive a one-line header.

Idempotent: each edit is skipped when its new text is already present, and each
changed file is first copied to a sibling _backup_2026-11-04 folder (as
<name>.pre_audit if that name already exists there; never overwritten).
Every replacement asserts its expected match count.

Run from anywhere:  python3 scripts/patch_stale_md_20261104.py
"""
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TP = os.path.join(ROOT, "IUEA_Teaching_Plan")
CHANGED = []


def backup(path):
    d = os.path.join(os.path.dirname(path), "_backup_2026-11-04")
    os.makedirs(d, exist_ok=True)
    dst = os.path.join(d, os.path.basename(path))
    if os.path.exists(dst):
        dst += ".pre_audit"
    if os.path.exists(dst):
        return
    shutil.copy2(path, dst)


class Doc:
    def __init__(self, rel, base=TP):
        self.path = os.path.join(base, rel)
        with open(self.path, encoding="utf-8") as f:
            self.orig = f.read()
        self.text = self.orig

    def sub(self, old, new, count=1):
        """Literal replacement with an asserted count; skipped if already done."""
        if new and new in self.text:
            return
        if old not in self.text:
            assert new in self.text, "neither old nor new text found in %s: %r" % (self.path, old[:70])
            return
        n = self.text.count(old)
        assert n == count, "%s: expected %d match(es), found %d for %r" % (self.path, count, n, old[:70])
        self.text = self.text.replace(old, new)

    def rx(self, pattern, new, count=1, flags=re.M, done=None):
        """Regex replacement with an asserted count; `done` is a literal that
        proves the edit was already applied."""
        if done is not None and done in self.text:
            return
        found = re.findall(pattern, self.text, flags)
        assert len(found) == count, "%s: expected %d match(es), found %d for %r" % (
            self.path, count, len(found), pattern[:70])
        self.text = re.sub(pattern, lambda m: new, self.text, flags=flags)

    def header(self, line, after_title=False):
        if line in self.text:
            return
        if after_title and self.text.startswith("#"):
            first, _, rest = self.text.partition("\n")
            self.text = first + "\n\n" + line + "\n" + rest
        else:
            self.text = line + "\n\n" + self.text

    def append(self, block, marker):
        if marker in self.text:
            return
        if not self.text.endswith("\n"):
            self.text += "\n"
        self.text += "\n" + block

    def save(self):
        if self.text != self.orig:
            backup(self.path)
            with open(self.path, "w", encoding="utf-8") as f:
                f.write(self.text)
            CHANGED.append(os.path.relpath(self.path, ROOT))


SUPERSEDED = ("> Superseded by Block_Assessment_Arrangement_2026-11-03.md and second_half/Plan_Weeks_8-12.pdf: "
              "the semester ends at Week 12, Weeks 8 to 11 are four classes in second_half/, the project is an "
              "individual timed sitting in Week 12, and there is no Practical Test 2, demo or Weeks 13 to 15. "
              "Kept as a record.")

# ---------------------------------------------------------------- Teaching_Progress.md
d = Doc("Teaching_Progress.md")
d.sub("# IUEA teaching progress — 29 September 2026\n",
      "# IUEA teaching progress\n\n"
      "> Current status: the last section of this file, **Status 4 November 2026**. Everything between here and there is history.\n\n"
      "## History: status of 29 September 2026\n")
STATUS = """## Status 4 November 2026

This is the current position. The older sections above are history.

- Weeks 1 to 7 are done. Week 7 was Practical Test 1. Week 6 was waived.
- Week 8 theory: CML3113 and CML3111 had it on Friday 30 October, without the lab. CML3112 starts Week 8 on Tuesday 3 November.
- The semester ends at Week 12 (12 study weeks, 36 contact hours). Weeks 8 to 11 are taught as four classes, concepts first and then the lab. Slides, lab notebooks, lecturer guides, student packages, student slide PDFs and the project are in `second_half/`.

| Class | Content | CML3112 (Tue) | CML3113 and CML3111 (Fri) |
|---|---|---|---|
| 1 First model | Week 8 | Tue 3 Nov | Fri 6 Nov (concepts recap, then the lab) |
| 2 Classification | Week 9 | Tue 10 Nov | Fri 13 Nov |
| 3 Trust | Week 10 | Tue 17 Nov | Fri 20 Nov |
| 4 Choosing | Week 11 | Tue 24 Nov | Fri 27 Nov |

- Week 12 is the Engineering ML project: individual, timed, auto-graded, one supervised 3-hour sitting in Google Colab in the class slot, with the same entry and Submit test flow as Practical Test 1. Part A coded notebook 30 plus Part B decision memo 15 (a form inside the notebook) = 45 percent. It covers Weeks 1 to 11 only.
- Proposed sittings (lecturer to confirm): CML3112 Tue 1 Dec 11:00 to 14:00; CML3113 Fri 4 Dec 08:00 to 11:00; CML3111 Fri 4 Dec 11:00 to 14:00. An unmarked rehearsal is released right after Class 4 (Tue 24 Nov, Fri 27 Nov).
- Gone: Practical Test 2, the demo and viva, Weeks 13 to 15, the project clinic, team ML projects, the old take-home project, the December due dates, and the Q11 and Q12 quizzes. The data analysis project (10 percent) is still a team project.
- Weights: quizzes 15, assignments 15, data analysis project 10, Practical Test 1 15, ML project 45. Block 1 is A7 + A8 and Q7 + Q8 (quiz sat in the last 20 minutes of Class 2). Block 2 is A9 + A10 + A11 and Q9 + Q10 (last 20 minutes of Class 4). Weeks 1 to 5 stay weekly, best 3 of 5. Results are provisional out of 55 until the project is marked.
- Details: `second_half/Plan_Weeks_8-12.pdf`, `Block_Assessment_Arrangement_2026-11-03.md`, `second_half/Project/README.md` and `Grading_Update_By_Hand_2026-11-03.md`.
"""
d.append(STATUS, "## Status 4 November 2026")
d.save()

# ---------------------------------------------------------------- Before_Each_Class_Checklist.md
d = Doc("Before_Each_Class_Checklist.md")
NEWPOS = """## Current teaching position: 4 November 2026

Weeks 1 to 7 are done. The semester ends at Week 12. Weeks 8 to 11 are four classes (Class 1 to Class 4) taught from `second_half/`: CML3112 on Tue 3, 10, 17 and 24 Nov; CML3113 and CML3111 on Fri 6, 13, 20 and 27 Nov (they had the Week 8 theory on Fri 30 Oct without the lab, so their Class 1 is a recap and the lab). Week 12 is the individual timed project sitting (proposed: CML3112 Tue 1 Dec 11:00 to 14:00; CML3113 Fri 4 Dec 08:00 to 11:00; CML3111 Fri 4 Dec 11:00 to 14:00; lecturer to confirm). There is no Practical Test 2, no demo and no Weeks 13 to 15. See [teaching progress](Teaching_Progress.md) and [Block_Assessment_Arrangement_2026-11-03.md](Block_Assessment_Arrangement_2026-11-03.md). The week table at the end of this file is updated; the 29 September position below is history.

"""
d.sub("## Current teaching position — 29 September\n", NEWPOS + "## Teaching position on 29 September (history)\n")
rows = {
    8: "| 8 (Class 1) | CML3112 Tue 3 Nov (starts Week 8); CML3113 and CML3111 Fri 6 Nov (they had the Week 8 theory on Fri 30 Oct without the lab: recap, then the lab). Teach from `second_half/`. Check the regression/baseline package (A7) and written interpretation. Do not open Q7 today: Q7 and Q8 are sat together in the Block 1 quiz in Class 2. Treat the separate data-analysis project as held until its full assessment is validated. |",
    9: "| 9 (Class 2) | CML3112 Tue 10 Nov; Fridays 13 Nov. Check the classification/cost package (A8) and class meanings. The Block 1 quiz (Q7 + Q8, 10 marks) is sat in the last 20 minutes of this class. |",
    10: "| 10 (Class 3) | CML3112 Tue 17 Nov; Fridays 20 Nov. Check the validation/leakage package (A9) and split protocol. No quiz today. Block 1 assignments (A7, A8) close on the date in the arrangement note. |",
    11: "| 11 (Class 4) | CML3112 Tue 24 Nov; Fridays 27 Nov. Check the features/ablation and model recommendation packages (A10, A11), the decision memo and written evidence. The Block 2 quiz (Q9 + Q10, 10 marks) is sat in the last 20 minutes. After class, release the unmarked project rehearsal. |",
    12: "| 12 | Engineering ML project sitting: 3 hours, individual, timed, auto-graded, in Colab, with the Practical Test 1 entry and Submit test flow. Proposed (lecturer to confirm): CML3112 Tue 1 Dec 11:00 to 14:00; CML3113 Fri 4 Dec 08:00 to 11:00; CML3111 Fri 4 Dec 11:00 to 14:00. Prepare from `second_half/Project/` (marking guide, `deploy/DEPLOYMENT_STEPS.md`). No weekly quiz and no weekly assignment. |",
}
for n, row in rows.items():
    d.rx(r"^\| %d \| (Check|Plan).*$" % n, row, done=row)
d.rx(r"^\| 13 \| Prepare the project studio.*$", "| 13 to 15 | Superseded: there are no Weeks 13 to 15, no Practical Test 2, no demo and no project clinic. The semester ends at Week 12. |",
     done="| 13 to 15 | Superseded")
d.rx(r"^\| 14 \| Practical Test 2:.*\n", "", done="| 13 to 15 | Superseded") if "| 14 | Practical Test 2:" in d.text else None
d.rx(r"^\| 15 \| Confirm project/demo release.*\n", "", done="| 13 to 15 | Superseded") if "| 15 | Confirm project/demo" in d.text else None
d.save()

# ---------------------------------------------------------------- Beginner_Lecturer_Guide.md
d = Doc("Beginner_Lecturer_Guide.md")
d.header("> **Current (4 November 2026):** the semester ends at Week 12. Weeks 8 to 11 are four classes taught from `second_half/`; Week 12 is the individual timed project sitting. There is no Practical Test 2, demo or Weeks 13 to 15. See [teaching progress](Teaching_Progress.md).")
d.sub("For Weeks 7 and 14, complete rehearsal before the timed test.",
      "For Week 7 (Practical Test 1) and the Week 12 project sitting, complete the rehearsal before the timed test.")
d.sub("Weeks 7 and 14 use their existing examination timetable; their opening preparation slides are for use before the test, not replacement exam content. Week 15 uses the published demo timetable. Week 13 prioritises studio work and the final weekly quiz.",
      "Week 7 uses its examination timetable; its opening preparation slides are for use before the test, not replacement exam content. Week 12 is the project sitting (3 hours, individual, timed; proposed times in Teaching_Progress.md). There are no Weeks 13 to 15, no Practical Test 2 and no demo.")
d.sub("## Weeks 6 to 15 pandas continuation", "## Weeks 6 to 12 pandas continuation")
d.rx(r"### Week 12\n\nFilter candidate tables.*?(?=\nThe assignment loader is supplied)",
     "### Week 12\n\nThe project sitting: 3 hours, individual, timed, auto-graded, covering Weeks 1 to 11. Filtering candidate tables by both constraints and the published tie-breaks (the old Week 12 topic) is now taught in Class 4.\n\n"
     "### Weeks 13 to 15\n\nSuperseded on 4 November 2026: these weeks are no longer taught.\n",
     flags=re.S, done="### Weeks 13 to 15")
d.save()

# ---------------------------------------------------------------- Curriculum_Benchmark_and_Teaching_Map.md
d = Doc("Curriculum_Benchmark_and_Teaching_Map.md")
d.sub("The Week 3–15 PowerPoints supersede", "The Week 3–7 PowerPoints (and, from 4 November 2026, the Weeks 8 to 11 class decks in `second_half/`) supersede")
d.rx(r"^\| 12 \| Fair comparisons and constraints \|.*$",
     "| 11 (Class 4; the old Week 12 topic) | Fair comparisons and constraints | Apply every requirement before selecting a candidate |",
     done="| 11 (Class 4; the old Week 12 topic)")
d.rx(r"^\| 13 \| Fresh run, paths, environment.*\n^\| 14 \| Previously taught evaluation.*\n^\| 15 \| Question, evidence.*$",
     "| 12 | Everything from Weeks 1 to 11, applied under time (Weeks 13 to 15 no longer exist) | Sit the 3-hour individual project; a rehearsal is released after Class 4 |",
     done="| 12 | Everything from Weeks 1 to 11, applied under time")
d.sub("Weeks 7 and 14 contain rehearsal activities to complete before the test period.",
      "Week 7 contains rehearsal activities to complete before the test; the Week 12 project has its own unmarked rehearsal after Class 4.")
d.rx(r"^\| 12 \| Cross out ineligible candidates.*$", "| 11 (Class 4) | Cross out ineligible candidates before ranking | Inclusive constraints and tie-breaks |",
     done="| 11 (Class 4) | Cross out")
d.rx(r"^\| 13 \| Exchange run instructions.*\n", "", done="| 11 (Class 4) | Cross out") if "| 13 | Exchange run" in d.text else None
d.rx(r"^\| 15 \| Explain one finding.*\n?", "", done="| 11 (Class 4) | Cross out") if "| 15 | Explain one finding" in d.text else None
d.save()

# ---------------------------------------------------------------- Teaching_Prerequisite_Map.md
d = Doc("Teaching_Prerequisite_Map.md")
d.rx(r"^\| 12 \| Eligibility, tuple comparison.*$",
     "| 11 (Class 4; the old Week 12 topic) | Eligibility, tuple comparison, sorting keys and empty results | Ranked candidates, the meaning of passing a function, then the full selection example |",
     done="| 11 (Class 4; the old Week 12 topic)")
d.rx(r"^\| 13 \| Fresh session, working folder.*\n^\| 14–15 \| Previously taught modelling.*$",
     "| 12 | Project sitting: no new syntax, everything from Weeks 1 to 11 (Weeks 13 to 15 no longer exist) | Rehearsal released after Class 4; use the published brief |",
     done="| 12 | Project sitting: no new syntax")
d.save()

# ---------------------------------------------------------------- video_library.md
d = Doc("video_library.md")
d.sub("## Weeks 5-15 map", "## Weeks 5-12 map")
d.sub("(the core of Weeks 5-15)", "(the core of Weeks 5-12)")
d.save()

# ---------------------------------------------------------------- historical notes
d = Doc("Practical_Revision_Week6_Waiver.md")
d.header("> Note of 4 November 2026: Practical Test 2, the final project demo and Weeks 13 to 15 no longer exist (see Block_Assessment_Arrangement_2026-11-03.md). Everything else below is the 21 October record.", after_title=True)
d.save()
for rel in ("Week8_Benchmark_and_Change_Log_2026-10-30.md",
            "Week8_Onwards_Deck_Review_2026-10-29.md",
            "Weeks8-12_Rebuild_Log_and_Industry_Coverage_2026-10-30.md"):
    d = Doc(rel)
    extra = ""
    if rel.startswith("Week8_Benchmark"):
        extra = " The line that CML3112 taught Week 8 on 27 October is not current: CML3112 starts Week 8 on Tue 3 Nov 2026."
    d.header(SUPERSEDED + extra, after_title=True)
    d.save()

# ---------------------------------------------------------------- decks index files
d = Doc("decks/README.md")
d.header("> **4 November 2026:** the semester ends at Week 12. The Week 8 to 11 decks in this folder are replaced by the four class decks in `../second_half/Slides/`, and Week 12 is the individual project sitting. Weeks 13, 14 and 15 are superseded and not used. Weeks 1 to 7 are unchanged. See `../Teaching_Progress.md`.", after_title=True)
if "Week 14 rehearsal reuses Week 12 data." in d.text:
    d.sub("Week 14 rehearsal reuses Week 12 data.", "the Week 14 rehearsal is no longer used.")
d.text = d.text.replace("; The Week 14 rehearsal is", "; the Week 14 rehearsal is")  # repairs an earlier run
for n in (13, 14, 15):
    d.rx(r"^\| %d \| \[Week" % n, "| %d (superseded: not used, see ../second_half/) | [Week" % n, done="| %d (superseded" % n)
for n, c in ((8, 1), (9, 2), (10, 3), (11, 4)):
    d.rx(r"^\| %d \| \[Week" % n, "| %d (replaced by ../second_half/ Class %d) | [Week" % (n, c), done="| %d (replaced" % n)
d.rx(r"^\| 12 \| \[Week", "| 12 (superseded: Week 12 is the project sitting) | [Week", done="| 12 (superseded")
d.save()

d = Doc("decks/LECTURER_NOTES_INDEX.md")
d.header("> **4 November 2026:** Weeks 8 to 11 are now taught from `../second_half/` (four classes, with lecturer guides there). Weeks 13, 14 and 15 are superseded and not used. Week 12 is the individual project sitting.", after_title=True)
d.sub("CML3112: Week 4. CML3111 and CML3113: Week 3, from slide 1.",
      "Weeks 1 to 7 are done. CML3112 starts Week 8 (Class 1) on Tue 3 Nov; CML3113 and CML3111 on Fri 6 Nov. See `../Teaching_Progress.md` (status of 4 November 2026).")
for cohort in ("CML3111_Week%02d_Engineering", "CML3112_Week%02d_Design_Infrastructure", "CML3113_Week%02d_Mining_Petroleum"):
    for n in (13, 14, 15):
        name = cohort % n
        old = "· [Readable notes](./lecturer_notes/%s.md)" % name
        new = old + " · superseded: not used, see ../second_half/"
        d.sub(old, new)
d.save()

d = Doc("../README.md", base=TP)
d.sub("**Teaching materials:** use the updated PowerPoints",
      "**Weeks 8 to 12 (4 November 2026):** the semester ends at Week 12. Weeks 8 to 11 are four classes in [IUEA_Teaching_Plan/second_half/](IUEA_Teaching_Plan/second_half/) (slides, lab notebooks, lecturer guides, student packages, the plan PDF). Week 12 is the individual, timed, auto-graded ML project. There is no Practical Test 2, demo or Weeks 13 to 15. See [teaching progress](IUEA_Teaching_Plan/Teaching_Progress.md).\n\n**Teaching materials:** use the updated PowerPoints")
d.sub("15 weeks, 3 cohorts, 45 contact hours each", "12 study weeks, 3 cohorts, 36 contact hours each")
d.sub("45 (15 weeks x 3 cohorts), 1,569 slides", "21 in `decks/` (Weeks 1 to 7) and 12 class decks in `second_half/Slides/` (Weeks 8 to 11)")
d.sub("decks/                       45 .pptx, one per week per cohort",
      "decks/                       45 .pptx, one per week per cohort (Weeks 8 to 15 superseded by second_half/)")
d.save()

# ---------------------------------------------------------------- test operations
d = Doc("test_operations/TEST_CHECKLIST.md")
d.sub("For Test 1 (Week 7) and Test 2 (Week 14) in CML3111, CML3112 and CML3113.",
      "For Test 1 (Week 7) in CML3111, CML3112 and CML3113. Practical Test 2 was removed on 2 November 2026. The Week 12 project sitting uses the same entry and Submit flow; its steps are in `../second_half/Project/Lecturer_Marking_Guide.pdf` and `../second_half/Project/deploy/DEPLOYMENT_STEPS.md`.")
d.sub("Share the course’s Week 7 (Test 1) or Week 14 (Test 2) PDF slides", "Share the course’s Week 7 (Test 1) PDF slides")
d.sub("from the Week 7 or Week 14 deck. For timed Test 1, learners enter their details, start their timer and open their private notebook in Colab. For untimed Test 2, they download their notebook and CSV; do not distribute the A/B/C ZIPs to the class.",
      "from the Week 7 deck. For timed Test 1, learners enter their details, start their timer and open their private notebook in Colab. Do not distribute the A/B/C ZIPs to the class.")
d.sub(" Untimed Test 2 still uses a manual CSV upload.", "")
d.sub("for Test 1 and Test 2.\n", "for Test 1. (Test 2 no longer exists; the Week 12 project is marked with `second_half/Project/grader_spec/grade_project.py`.)\n")
d.sub("saved Test 1/Test 2 results", "saved Test 1 results")
d.sub(" (or Get my test files for Test 2)", "")
d.sub("Test 1 is marked out of 100 and contributes 15 semester points; Test 2 contributes 20.",
      "Test 1 is marked out of 100 and contributes 15 semester points. There is no Test 2.")
d.save()

d = Doc("test_operations/TEST_ENTRY_LINKS.md")
d.sub("| Course | Test 1 Week 7 | Test 2 Week 14 |", "| Course | Test 1 Week 7 | Test 2 (removed 2 Nov 2026: do not share) |")
d.header("> **4 November 2026:** Practical Test 2 no longer exists, so the Test 2 links below must not be shared. The Week 12 project entry links are in `../second_half/Project/deploy/`.", after_title=True)
d.save()

d = Doc("test_operations/TEST_FORM_LINKS.md")
d.header("> **4 November 2026:** the three TEST2 forms are retired (no Practical Test 2). Do not share them. They are kept here as a record.", after_title=True)
d.save()

d = Doc("test_operations/VERIFICATION.md")
d.header("> Dated verification record. The Test 2 items below refer to a test that was removed on 2 November 2026 (see Block_Assessment_Arrangement_2026-11-03.md).", after_title=True)
d.save()

d = Doc("test_portal/README.md")
d.header("> **4 November 2026:** Practical Test 2 and its Week 14 deck are not used. The Week 12 project sitting uses this portal with an `ML_PROJECT` key; see `../second_half/Project/deploy/DEPLOYMENT_STEPS.md`.", after_title=True)
d.save()

d = Doc("test_revision/README.md")
d.header("> **4 November 2026:** Practical Test 2 was removed, so the Test 2 revision materials below are not used and must not be shared. The Test 1 materials are unchanged. The Week 12 project has its own unmarked rehearsal in `../second_half/Project/Rehearsal/`.", after_title=True)
for c in ("CML3111", "CML3112", "CML3113"):
    d.sub("| %s | Week 14 / Test 2 |" % c, "| %s | Week 14 / Test 2 (not used) |" % c)
d.save()
for c in ("CML3111", "CML3112", "CML3113"):
    d = Doc("test_revision/%s/Test2/START_HERE.txt" % c)
    d.header("NOT USED: Practical Test 2 was removed on 2 November 2026. Kept for the record.")
    d.save()

# ---------------------------------------------------------------- assessment_operations
d = Doc("assessment_operations/CONTINUE_GRADING.md")
d.sub("| Test 1 / Test 2 notebooks |", "| Test 1 notebooks (there is no Test 2) |")
d.sub("**Test 1 and Test 2 are different:**", "**Test 1 is different (there is no Test 2; the Week 12 project is marked with `second_half/Project/grader_spec/grade_project.py`, see its marking guide):**")
d.save()

d = Doc("assessment_operations/reference/GRADING.md")
d.sub("## What the totals mean\n",
      "## What the totals mean\n\n> Policy since 3 and 4 November 2026 (`data/assessment_blocks_20261103.json`): quizzes 15, assignments 15, data analysis project 10, Practical Test 1 15, Engineering ML project 45 (individual timed sitting, Part A 30 + Part B 15). There is no Test 2 and no demo; the semester ends at Week 12; Weeks 1 to 5 are best 3 of 5 and the block rules apply from Week 8. The live gradebook is the Google Sheet driven by `grader/gradebook.gs`. The private workbook described below was last built on 21 October and still uses the older weights: do not use its totals for Semester 1 results.\n")
d.save()

# ---------------------------------------------------------------- student package START_HERE
d = Doc("student_packages/CML3113_W08_student/START_HERE.md")
d.sub("**Block 1, part A of 3** (Weeks 8 to 10). Marked out of 20. All 3 parts of the block close together.",
      "**Block 1, part A of 2** (Weeks 8 and 9 content). Marked out of 20. Both parts of the block close together.")
d.sub("**Block quiz:** one sitting in the last 20 minutes of the Week 10 class, 3 short quizzes, 15 marks.",
      "**Block quiz:** one sitting in the last 20 minutes of Class 2 (Friday 13 November), 2 short quizzes, 10 marks.")
d.save()

# ---------------------------------------------------------------- assessment banks
SITTING = {"CML3112": "Tue 1 Dec 2026, 11:00 to 14:00", "CML3113": "Fri 4 Dec 2026, 08:00 to 11:00",
           "CML3111": "Fri 4 Dec 2026, 11:00 to 14:00"}
OLD_DEADLINE = {"CML3112": "15 December 2026, 11:00", "CML3113": "18 December 2026, 08:00", "CML3111": "18 December 2026, 11:00"}
for c in ("CML3111", "CML3112", "CML3113"):
    for fn in ("ASSIGNMENT_INSTRUCTIONS.md", "ASSIGNMENT_INSTRUCTIONS.txt", "TASKS.md"):
        d = Doc("assessment_banks/ML_PROJECT/%s/A/%s" % (c, fn))
        hdr = ("> **SUPERSEDED (4 November 2026).** The Engineering ML project is now an individual, timed, auto-graded 3-hour sitting in Week 12 "
               "(%s Kampala, proposed, lecturer to confirm), worth 45: Part A coded notebook 30 and Part B decision memo 15, entered and submitted "
               "like Practical Test 1. There is no report, no DOCX or PDF upload, no team and no demo. The current brief is "
               "`second_half/Project/Student_Brief_%s.pdf`. The take-home text below is the old bank and is not used." % (SITTING[c], c))
        d.header(hdr)
        if fn != "TASKS.md":
            d.rx(r"^\*\*Submit:\*\* TWO files together.*$",
                 "**Submit:** one completed notebook (.ipynb) with the decision memo form inside it, through the Submit test cell and form of the timed portal.",
                 done="through the Submit test cell and form of the timed portal")
            d.rx(r"^\*\*Deadline:\*\* %s Kampala\. The live form shows any later change\.$" % re.escape(OLD_DEADLINE[c]),
                 "**Sitting:** %s Kampala (proposed, lecturer to confirm). The old December deadline no longer applies." % SITTING[c],
                 done="**Sitting:**")
            d.rx(r"^3\. Use the \*\*Report checklist\*\*.*\n\n?Include the two-page engineering brief.*$",
                 "3. Part B is the decision memo form inside the notebook. There is no separate report.", flags=re.M,
                 done="Part B is the decision memo form inside the notebook")
            d.rx(r"## 4\. Hand in.*?\*\*Submission link:\*\* \S+\n",
                 "## 4. Hand in\n\nUse the Submit test cell in the notebook and the generated form, as in Practical Test 1, before your personal deadline. Keep the confirmation.\n",
                 flags=re.S, done="## 4. Hand in\n\nUse the Submit test cell")
        d.save()
    for v in "ABC":
        for fn in ("ASSIGNMENT_INSTRUCTIONS.md", "ASSIGNMENT_INSTRUCTIONS.txt", "TASKS.md", "STUDENT_HOW_TO.md"):
            d = Doc("assessment_banks/TEST2/%s/%s/%s" % (c, v, fn))
            d.header("> **Not used:** Practical Test 2 was removed on 2 November 2026. Kept for the record.")
            d.save()

print("changed %d file(s)" % len(CHANGED))
for p in CHANGED:
    print("  ", p)
