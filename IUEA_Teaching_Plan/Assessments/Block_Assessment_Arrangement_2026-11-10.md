# Assessment update: the Semester 1 grading policy of 10 November 2026

Written 10 November 2026. Source of truth: `data/assessment_policy_20261110.json`; the plain note is `Grading_Policy_2026-11-10.md`. It supersedes the weights, the best-of rules, the Week 6 waiver rule and the block rule of `Block_Assessment_Arrangement_2026-11-03.md` (and the 2 November and 30 October notes). The blocks, deadlines, quiz sittings, the Week 12 project sitting and the project design (individual, timed, auto-graded) are unchanged.

## What changed from the 3 November arrangement

| | 3 November | 10 November |
|---|---|---|
| Assignments | 15 (A1 to A5 best 3 of 5, plus Block 1 and Block 2, out of 160) | **20**: A1 to A5, each /20, all five count equally |
| Quizzes | 15 (Q1 to Q5 best 3 of 5, plus two block quizzes, out of 35) | **20**: Q1 to Q5, each /5, all five count equally |
| Data Analysis project | 10 | **does not count** |
| Practical Test 1 | 15 | **20** (marked /100, scaled to 20) |
| Engineering ML project | 45 (Part A /30 + Part B /15) | **40** (the same 45 raw marks, scaled to 40) |
| Total | 100 | 100 |
| Provisional result before the project is marked | out of 55 | out of **60** (assignments 20 + quizzes 20 + Practical Test 1 20) |

Coursework (assignments + quizzes) is now 40 of the 100. A missing or not-yet-marked item scores zero. The best-3-of-5 rule, the Week 6 waiver and the rule that the blocks always count are retired. The project counts only when both parts are marked and is never counted as zero while pending.

## Why items no longer count

Only the five weekly assignments and five weekly quizzes of Weeks 1 to 5 are counted, because they are the work every student did under the same conditions. These items are not counted:

- Q6 onward and the Week 8 to 11 block quizzes (Q7 to Q10 in the gradebook; Q8 to Q11 on the receipts), A6 onward and the Week 8 to 11 block assignments (A7 to A11).
- The Data Analysis project, Practical Test 2 and the demonstration.

The Week 8 to 11 items are still set, sat, collected and given feedback, and their receipts are kept in the ledger. They now work as practice for the project sitting. They add nothing to the final mark.

## What to tell the students

From 10 November your Semester 1 mark out of 100 is your five assignments A1 to A5 (20 marks, all five count equally), your five quizzes Q1 to Q5 (20 marks, all five count equally), Practical Test 1 (20 marks) and the Engineering ML project sitting in Week 12 (40 marks). There is no best-of rule and no Week 6 waiver any more, and a missing item scores zero. The Data Analysis project, and the Week 8 to 11 block assignments (A7 to A11) and block quizzes (Q7 to Q10), no longer count toward your final mark. Please still do the Week 8 to 11 work: it is collected, you get feedback on it, and it is the best preparation for the project sitting. Until the project is marked your result is shown as provisional, out of 60, with the project marked PENDING.

## Files updated

Everything below was changed by `scripts/apply_policy_20261110.py` (idempotent; `--dry` shows the list) unless a regeneration is named.

- Dated notes (banner only, bodies unchanged): the three `Block_Assessment_Arrangement_*` notes, `Block_Assessment_By_Hand_Checklist_2026-11-02.md`, `Block_Assessment_Verification_2026-11-02.md`, `Grading_Update_By_Hand_2026-11-03.md`, `Stale_Documents_Audit_2026-11-04.md`, `Practical_Revision_Week6_Waiver.md`, `Week8_Onwards_Deck_Review_2026-10-29.md`, `Weeks8-12_Rebuild_Log_and_Industry_Coverage_2026-10-30.md`.
- Living notes: `Teaching_Progress.md`, `Before_Each_Class_Checklist.md`, `Assignment_Submission_Links.md`, `assessment_operations/README.md`, `assessment_operations/reference/GRADING.md`, `second_half/README.md`, `second_half/Project/README.md`, `second_half/Build/AUTHORING_GUIDE.md`.
- Student guides (all three cohorts): `B1.md`, `B2.md`, `ML_PROJECT.md`, `DA_PROJECT.md`, `W08.md` to `W12.md`, and `W06.md` for CML3112 and CML3113.
- Assignment banks: `assessment_banks/W08` to `W12` (`ASSIGNMENT_INSTRUCTIONS.md`, `.txt` and the `W0x_student.ipynb` opening cell, task content untouched), `assessment_banks/W06` (CML3112, CML3113) and `assessment_banks/ML_PROJECT`.
- Documents patched in place: the three syllabi, `IUEA_ML_Semester1_Master_Teaching_Plan.docx` and `.xlsx`, `IUEA_ML_Weekly_Quiz_Operations_Guide.docx`, `IUEA_ML_Lecturer_Teaching_Guide_W1-W15.docx`.
- Regenerated from source: `grader/create_quiz_forms.gs` (by `scripts/build_quiz_forms_gs.py`), `second_half/Plan_Weeks_8-12.docx` and `.pdf` (`make_plan.py`), `second_half/Project/Student_Brief_*.docx` and `.pdf` and `Lecturer_Marking_Guide.docx` and `.pdf` (`tools/build_project_docs.py`), `second_half/Lecturer Guides/*` (`make_guides.py`; only Class 4 changed).
- Patched text in generated files: `grader/submission_forms.gs` (project and Data Analysis briefs), `data/assessments.json` (delivery note on W08 to W12), the nine `ML_PROJECT_student.ipynb` and nine solution notebooks, `second_half/Project/deploy/Portal.gs` and `PacketsMLProject.gs`, the `second_half/Build` sources (`content/c1.py` to `c4.py`, `_specs/*.json`, `kit/make_plan.py`), and the twelve `second_half/Slides` decks (slide text and speaker notes).
- Builders and checks: `scripts/build_quiz_forms_gs.py`, `build_quizops_docx.py`, `build_quiz_timer.py`, `pptxkit.py`, `verify_quiz_arithmetic.py`, `quiz_timer.html`, and the project tools under `second_half/Project/tools/` and `grader_spec/grade_project.py`. `build_syllabi.py`, `build_master_docx.py`, `plan_content.py` and `build_xlsx.py` only have their header note extended (see below).

## Not regenerated, and why

- `build_syllabi.py`, `build_master_docx.py`, `plan_content.py`, `build_xlsx.py`: still the 15-week builders of September. Their files were changed afterwards by the `patch_*` scripts, so running them would undo that work. The documents above were patched in place instead.
- `scripts/build_continuous_assessment.mjs` and the private `IUEA_Continuous_Assessment.xlsx`: need the lecturer's Mac artifact runtime. The private workbook still uses the old weights; do not use its totals.
- `second_half/Student Slides PDF/*` (the deck PDFs) and `second_half/Student Packages/*.zip`: the deck builder needs the pptx skill scripts, which are not available here. The decks were patched directly; the PDFs still show the 3 November wording on the Block and project slides.
- Weeks 1 to 7 decks, the old Weeks 8 to 15 decks, `decks/lecturer_notes/*`, `guided_practice/*` and `student_packages/*`: delivered or superseded material (see `Stale_Documents_Audit_2026-11-04.md`). They still say "best 3 of 5", "10 percent" or "Block 1 is Weeks 8 to 10" in places.
- `grader/oct15_pandas_quiz_revision.gs`: a one-off October script that carries the original quiz intro ("best ten of twelve"). The live forms are replaced from `create_quiz_forms.gs`.
- Live Google Forms, Sheets and Apps Script projects: nothing on Google was touched. Re-running `create_quiz_forms.gs` or re-pasting `submission_forms.gs` is a by-hand step.
- Owned by another session and not touched: `grader/gradebook.gs`, `grader/Grades_template.csv`, `grader/README.md`, `grader/continuous_assessment.py`, `grader/final_marks_export.py`, `grader/grade_test_batch.py`, `grader/test_collection_issues.py`, `test_operations/TEST_CHECKLIST.md`, `scripts/assessment_registry.py` and the gradebook xlsx builders.

## Correction of 10 November 2026: there is no live Google gradebook

Earlier notes (for example `Block_Assessment_Arrangement_2026-11-03.md` and `Grading_Update_By_Hand_2026-11-03.md`) call "the Google Sheet with a tab called `Grades`, driven by `grader/gradebook.gs`" the live gradebook. It does not exist. On 10 November 2026 I checked everything under wirmbeesubs@gmail.com: Apps Script (All Projects: six projects, none a gradebook), Google Drive (the only gradebook-named file is "Synthetic QA gradebook — no student marks" of 15 September, with no script) and Google Sheets. `gradebook.gs` was never deployed.

How marks actually flow: the Google projects only COLLECT work (assignment and quiz forms, the test entry portal, the practical test and grading ZIP export menus). The Mac mini grades the exported ZIPs into the private ledger and `IUEA_Continuous_Assessment.xlsx`. The final marks workbook is built from that ledger by `grader/final_marks_export.py`. `grader/gradebook.gs` and `IUEA_ML_Gradebook_Semester1.xlsx` follow the same policy and agree with the Python grader, but they are optional tools, not the live record.
