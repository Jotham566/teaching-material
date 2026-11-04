# Assessment update: no demo, the project is an individual timed auto-graded sitting

Written 3 November 2026. Source of truth: `data/assessment_blocks_20261103.json`. It supersedes `data/assessment_blocks_20261102.json` and the weights, project and demo parts of `Block_Assessment_Arrangement_2026-11-02.md`. The blocks, deadlines and quiz sittings of 2 November are unchanged and still stand. The steps you run by hand are in `Grading_Update_By_Hand_2026-11-03.md`.

## The decision (lecturer, 3 November 2026)

- There is no demo. Practical Test 2 stays removed.
- The Engineering ML project stays. Update of 4 November 2026: it is INDIVIDUAL, TIMED and fully AUTO-GRADED. Each student sits it once, alone, in one supervised 3-hour sitting in Google Colab, entered and submitted like Practical Test 1. It covers only what was taught this semester (Weeks 1 to 11).
- Semester 1 results can be published before the project is marked, with the project shown as PENDING.
- Week 12 is the project sitting (3 hours, individual, timed, auto-graded) in the class slot: CML3112 Tue 1 Dec 11:00 to 14:00, CML3113 Fri 4 Dec 08:00 to 11:00, CML3111 Fri 4 Dec 11:00 to 14:00 (proposed, lecturer to confirm). Nobody presents and there is no clinic. An unmarked rehearsal (practice notebook and practice dataset, same structure, no solved walk-through) is released right after Class 4.
- Quizzes (weekly Q1 to Q5 best 3 of 5 plus the two block quizzes, out of 35) and assignments (A1 to A5 best 3 of 5 plus the two blocks, out of 160) are unchanged.

## Weights (sum 100)

| Component | 2 Nov | 3 Nov |
|---|---:|---:|
| Quizzes | 15 | 15 |
| Assignments | 15 | 15 |
| Data analysis project | 10 | 10 |
| Practical Test 1 | 15 | 15 |
| Engineering ML project | 30 | 45 |
| Demonstration | 15 | removed |
| Total | 100 | 100 |

The weights still need checking against IUEA regulations.

## The Engineering ML project

| Part | What | Marks | Marked by |
|---|---|---:|---|
| A | Coded project notebook | 30 | Auto-graded: hidden checks on unseen data, plus automatic checks of the process (test set opened once, no data leakage, seed, charts) |
| B | Structured decision memo (a form of fields inside the notebook) | 15 | Auto-graded: model chosen, validation and test numbers compared with the notebook, three limits and a next step from lists, two short written answers by keyword and length rules |
| Total | | 45 | |

| | Proposed (lecturer to confirm) |
|---|---|
| Rehearsal (unmarked) | Released after Class 4: CML3112 Tue 24 Nov, CML3113 and CML3111 Fri 27 Nov |
| Sitting (3 hours) | CML3112 Tue 1 Dec 11:00 to 14:00; CML3113 Fri 4 Dec 08:00 to 11:00; CML3111 Fri 4 Dec 11:00 to 14:00 (Kampala time) |
| Time limit | The Practical Test 1 mechanism: personal deadline = the earlier of 3 hours after Start and the class closing time (Test windows row with `duration_minutes` 180) |
| Form window | None is open. Key `CML311x\|ML_PROJECT` in the Colab test collector; `opens_at` and `closes_at` stay empty until you set them |

Decided on 4 November 2026: individual work; one timed, supervised sitting; one notebook with the memo form inside it, handed in with the Test 1 Submit test cell and Google Form; Part A (30) and Part B (15) both fully automatic, with no rubric and no manual marking. A short spot-check list of flagged cases (identity mismatch, copied code, identical written answers, an edited supplied cell, a test set opened twice) is for the lecturer to look at; a flag never reduces a mark by itself. Each student receives one of three data variants (A, B, C) allocated at random by the portal. Still to be confirmed by the lecturer: the sitting dates and times, the room, the form windows and the portal deployment. The draft project in `second_half/Project/` implements this decision.

## How results show before the project is marked

The gradebook has two project columns, `ML Project Part A` and `ML Project Part B`. A blank cell means not marked yet. A typed 0 is a mark of zero.

| State | What the sheet shows |
|---|---|
| Either project column blank | `Semester 1 provisional: x of 55 marks, y percent` (quizzes, assignments, data analysis project and Test 1; weights 15 + 15 + 10 + 15 = 55) and `Project: PENDING`. `Final %` and `Band` stay blank. An unmarked project is never counted as zero |
| Both columns hold a number | The full total out of 100. The provisional line is cleared |

A student with a missing quiz or assignment part still scores zero for it. A blank data analysis project or Practical Test 1 also scores zero and is listed under Missing. Only the project can be pending. The best-of rules and the block rules are exactly as before.

## Which file is the live gradebook

| File | What it is |
|---|---|
| The Google Sheet (tab `Grades`) driven by `grader/gradebook.gs` | **The live gradebook.** It holds the marks and the totals. This is the only place marks are entered and results are published from |
| `grader/gradebook.gs` | The script that is pasted into that sheet. It is code, with no student data |
| `grader/Grades_template.csv` | A template: the header row for creating a `Grades` sheet. No students. Updated today with the project columns |
| `IUEA_Teaching_Plan/IUEA_ML_Gradebook_Semester1.xlsx` | New today. An Excel copy of the same rules with formulas (Settings, Grades, Checks). Empty. A working copy and a calculator; it does not feed the Google Sheet |
| `IUEA_Teaching_Plan/IUEA_ML_Semester1_Master_Teaching_Plan.xlsx` | The teaching plan workbook. Its `Assessment` and `Rubrics` sheets describe the weights and are not a gradebook. Updated today |
| `IUEA_Teaching_Plan/assessment_operations/private/IUEA_Continuous_Assessment.xlsx` (and the copies under `private/reviews/` and `before_one_command/`) | A private cumulative marks workbook built from the CA ledger by `scripts/build_continuous_assessment.mjs`, last built 21 October 2026. It still uses the OLD weights and rules. Not updated, because the builder only runs on your Mac. Do not use its totals |
| `assessment_operations/private/*_quiz_source.xlsx`, `assignment_source.xlsx` | Raw exports of quiz and assignment responses. Inputs |
| `test_operations/grading_output/**/Test_Marks.xlsx` | Practical Test 1 marking output and rehearsals. Inputs |
| `assessment_operations/private/ledger.json` | The CA ledger. A machine file, not a workbook. `continuous_assessment.py --from-ledger` turns it into a totals CSV |
| `DataAnalysis_Track/*` and `grader/da_gradebook.py` | The separate Data Analysis track. Not part of this course |
| `grade-submissions` | A command script, not a workbook. `review/` holds dated review notes and no gradebook |

## What changed in the files

- Data: `data/assessment_blocks_20261103.json` (new), `data/assessments.json` (DEMO retired; ML_PROJECT has two parts, maximum 45, proposed dates, still no window).
- Apps Script: `grader/gradebook.gs` (weights, project columns, provisional mode, `prepareGradesColumns()`, project imports), `grader/retire_demo_forms_20261103.gs` (new).
- Python: `grader/continuous_assessment.py` (weights, `semester_totals()`, project part scores, `--totals-out`, `--from-ledger`), `grader/Grades_template.csv`.
- Documents: the three syllabi, the master plan (Word and Excel: Read Me, Calendar, the weekly sheets, Assessment, Rubrics, Marking Load, Risk Register), the Weekly Quiz Operations Guide, `Assignment_Submission_Links.md`, `Assignment_Instructions_Index.md`, `grader/README.md`, the student guides `B1.md`, `B2.md`, `DEMO.md` (retired) and `ML_PROJECT.md` in all three cohorts, and a header note on the three 2 November notes.
- Scripts: `scripts/apply_policy_20261103.py`, `patch_docx_20261103.py`, `patch_gradebook_20261103.py`, `patch_continuous_assessment_20261103.py`, `patch_tests_20261103.py`, `build_policy_20261103.py`, `build_gradebook_xlsx_20261103.py`, `verify_gradebook_xlsx_20261103.py`. `assessment_registry.py`, `build_quizops_docx.py` and `build_block_packages_20261102.py` were brought in step. `apply_block_policy_20261102.py` and `patch_block_docs_20261102.py` now stop with "SUPERSEDED" because running them would undo today's changes.
- Tests: `test_continuous_assessment.py`, `test_assessment_waivers.cjs`, `test_coursework_agreement_20261102.cjs`, `test_block_sittings_20261102.cjs` and `test_block_windows_20261102.cjs` were updated. `test_gradebook_sheet_20261103.cjs` and `test_retire_demo_20261103.cjs` are new. `test_continuous_assessment.py` also checks that the 2 November and 3 November policy files agree on every block, date and rule.
- Every changed file has an untouched copy in a sibling `_backup_2026-11-03` folder. Nothing was deleted.

## Checks run offline

| Check | Before | After |
|---|---|---|
| `node grader/gradebook.gs --test` | 102 passed | 160 passed, 0 failed |
| `tests/test_continuous_assessment.py` | 24 tests OK | 38 tests OK |
| `tests/test_coursework_agreement_20261102.cjs` (gradebook.gs and the Python module on 300 seeded students) | 300 agree | 300 agree, now including provisional (108 students) and full totals (192 students) |
| `tests/test_gradebook_sheet_20261103.cjs` (prepare columns, provisional, Part A only, full total, bad marks, imports) | new | pass |
| `tests/test_retire_demo_20261103.cjs` | new | pass |
| `scripts/verify_gradebook_xlsx_20261103.py` (Excel recalculated in LibreOffice for 80 random students against two Python calculations, and the six worked examples) | new | 357 checks passed, 0 failed |
| `scripts/verify_quiz_arithmetic.py` | all checks passed | all checks passed |
| Whole `tests/` folder, run file by file, plus the two self tests | 67 pass, 24 fail | 69 pass, 24 fail |

The 24 failures are the same 24 files before and after: `test_beginner_sequence`, `test_ca_bundle`, `test_ca_refresh`, `test_cleaning_audit`, `test_colab_exams`, `test_csv_examples`, `test_da_contracts`, `test_dashboard_numbers`, `test_exam_unit_aliases`, `test_explicit_foundations`, `test_isolated_grading`, `test_iuea_foundations`, `test_later_assessments`, `test_later_teaching_consistency`, `test_pandas_continuity`, `test_presentation_guidance`, `test_programme_reconciliation`, `test_registration_authority`, `test_revision_grader_alignment`, `test_revision_slides`, `test_sector_findings`, `test_slide_specific_notes`, `test_test1_coding` and `test_assessment_pipeline.cjs`. They were failing before today and none of them is about the weights or the demo. One test, `test_course_content.py`, failed for a short while mid-session because of a quote mark in `build_quizops_docx.py`; it is fixed and passes.

The three syllabi, the master plan, the Quiz Operations Guide and the master plan workbook all open and convert in LibreOffice; the workbook's weights total 100, the individual share is 45 and the team share 10, and the project rubric totals 45.

## Not changed, and not verified

- Nothing live (Google Sheets, Forms, Apps Script) was touched or run.
- `second_half/` (decks, lecturer guides, the plan PDF and the student ZIPs) still say "short project and demo in Week 12", for example the Class 4 slides. They belong to another session's work. The old Week 1 to 15 decks and the Lecturer Teaching Guide W1-W15 also still describe the old calendar.
- `grader/rubrics/ML_PROJECT.json`, `grader/rubrics/DEMO.json` and `grader/specs/spec_ML_PROJECT.py` describe the older 100-mark project and the demo. The new project grader is being built in `second_half/Project/`. I did not touch either.
- `Before_Each_Class_Checklist.md` and `Teaching_Progress.md` still describe the old calendar.
- The private marks workbook (see the table above).

<!-- PROJECT_SITTING_20261104 -->


<!-- AUDIT_20261104 -->
## Status after the stale-statement audit of 4 November 2026

- The "Not changed, and not verified" list above is out of date in two places. `Before_Each_Class_Checklist.md` and `Teaching_Progress.md` now describe the four-class calendar (updated 4 November), and `second_half/` (Plan_Weeks_8-12.pdf, the Class 4 deck wording, the lecturer guides) now states the individual timed sitting. `grader/rubrics/ML_PROJECT.json`, `rubrics/DEMO.json` and `specs/spec_ML_PROJECT.py` are listed as superseded in `grader/SUPERSEDED_README.md`.
- The sentence "Update of 4 November 2026" in the project section is the current rule. Ignore "take-home" and the 11 December due date wherever they remain in this note (the `due` placeholder in the JSON is superseded).
- The audit table is in `Stale_Documents_Audit_2026-11-04.md`.
