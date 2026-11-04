# Verification record, 2 November 2026

> **Update of 3 November 2026.** The checks below were run before the demo was removed. The new checks are listed in `Grading_Update_By_Hand_2026-11-03.md` and the verification section of `Block_Assessment_Arrangement_2026-11-03.md`.
>
> **4 November follow-up:** The stale `test_assessment_pipeline.cjs` expectation for waived Week 6 was corrected to keep the assessment blocked. The full Node regression suite now passes; the failure list below is a historical record of the 2 November run.

Everything here was run offline in the Linux workspace (Python 3.10, Node 22). No Google service, Colab or network was used. "Live" means the real Google Forms and Sheets, which were not touched.

## Checks that pass

| # | Check | Result |
|---|---|---|
| 1 | `python3 scripts/verify_quiz_arithmetic.py` (arithmetic of every code block, question mix per week, house style, cohort hygiene, answer positions, snippets, wrong-answer wording, and a new section 8 for the swap and the retirement) | 166 passes, 0 failures, exit 0. The mix, antithesis and em dash failures noted in an earlier session did not appear: the script already passed before my changes (run first, before editing) and passes now. |
| 2 | Section 8 of that script, executed: the two moved questions re-implemented and run (limit check with inclusive MAE, empty-table IndexError and its guard); Q10 still has 5 questions with the mix 2 interpretation, 1 diagnosis, 1 traceback, 1 judgement; exactly two Q10 questions come from the Q11 bank and have the kinds of the two they replaced; archive holds 5 Q11 and 5 Q12 questions; weeks 12 and 13 flagged retired; every cohort's payload carries the RETIRED notice and block wording; no live intro says "best ten of twelve" or "nine of eleven"; both generated .gs files are pure ASCII | all pass |
| 3 | `node grader/gradebook.gs --test` (rewritten unit tests: weights 15/15/10/15/30/15, no Test 2, blocks 40/60 and 10/10, totals 35 and 160, retired Q11 and Q12 columns ignored, progress lines) | 102 passed, 0 failed |
| 4 | `tests/test_continuous_assessment.py` (updated: new policy file, 35 and 160, retired weeks, registry deadlines equal the policy file, template has no Test 2 column, half-up rounding) | 24 tests OK |
| 5 | `tests/test_coursework_agreement_20261102.cjs`: 300 seeded random students scored by gradebook.gs and by continuous_assessment.py; earned, available and weighted must match | 300 of 300 agree. This found a real difference: Python rounded halves to even (8.625 became 8.62) and the gradebook rounds halves up (8.63). `continuous_assessment.py` now has `round2` that matches. |
| 6 | `tests/test_block_sittings_20261102.cjs`: the regenerated `create_quiz_forms.gs` and `block_quiz_sittings_20261102.gs` loaded together against in-memory fake Forms. Plan equals the policy file; old Week 11 forms are detected and a Block 2 sitting refuses to open anything; `replaceWeek11Questions()` replaces Week 11 only, keeps form ids and links, skips a form with responses; `refreshBlockQuizIntros()` skips open and responded forms; `open_Block1_*` and `open_Block2_*` open exactly two forms for 24 hours and set pending closes; `close_Block*` closes them; `retireQ11AndQ12Forms()` closes six forms and `openQuizFor` then refuses weeks 12 and 13; a retired flag on a block form stops a sitting; all three .gs files are pure ASCII | 8 of 8 sections pass |
| 7 | `tests/test_block_windows_20261102.cjs`: `applyBlockWindows()` sets 15 windows with the policy closing times and the existing opening times, never touches A6 or TEST2, is idempotent; `showBlockWindows()` reports 15 OK | pass |
| 8 | `tests/test_assessment_waivers.cjs` (was failing before my changes because it still expected "best 9" and "best 7"; updated for best 3 and no Test 2) | pass |
| 9 | Existing quiz tests that load `create_quiz_forms.gs`: `test_quiz_window.cjs`, `test_quiz_import.cjs`, `test_quiz_feedback_update.cjs` | pass |
| 10 | Syntax check (`node --check`) of `create_quiz_forms.gs`, `gradebook.gs`, `block_quiz_sittings_20261102.gs`, `apply_block_windows_20261102.gs` | pass |
| 11 | Every generated .gs file contains only ASCII bytes (checked in code before writing, and again by the tests) | pass |
| 12 | Idempotence: `apply_block_policy_20261102.py`, `build_block_packages_20261102.py`, `patch_block_docs_20261102.py`, `build_quiz_forms_gs.py` and `patch_block_docx_20261102.py` run a second time | no file changed (md5 of every text, json, gs, py, ipynb, csv and docx file before and after); the docx script prints "already patched" |
| 13 | Backups: every one of the 122 modified tracked files has a copy in a sibling `_backup_2026-11-02` folder | all 122 exist and equal git HEAD (the CSV template differs only in line endings that git normalises) |
| 14 | Rebuilt Week 8 to 12 assignment notebooks (15) | only cell 1 (the workflow cell) differs from the backup; metadata and every graded cell are unchanged |
| 15 | Rebuilt student ZIPs (15) | each opens, and holds the same file names as the original |
| 16 | The three syllabi, master plan docx, Quiz Operations Guide docx and master plan xlsx | reload with python-docx and openpyxl; LibreOffice converted all six to PDF (done by the helper agent; temporary PDFs deleted); xlsx formulas recalculated: weights total 100, individual 60, team 40; five rubric totals 100 |
| 17 | Scan of the final text of the five Word files for "Practical Test 2", "Week 13/14/15", "18 December", "45 contact", "best ten", "nine of eleven", "45/50/180 marks", "65 per cent" | every remaining hit is a sentence saying Test 2 or the Week 13 to 15 sessions no longer exist, or the Operations Guide telling you to close the Week 12 and 13 forms |
| 18 | Full test folder, run file by file by exit code, before and after | 62 pass after. The baseline was rebuilt from git HEAD with the unchanged folders linked in: no test passes there and fails now. The 4 new tests and the fixed waivers test pass now. |

## Failures that were already there and are not mine

The historical 2 November run reported these 27 existing test files failing both before and after the assessment changes: test_automatic_identity_refresh.py test_beginner_sequence.py test_cleaning_audit.py test_colab_exams.py test_csv_examples.py test_da_contracts.py test_da_sql_grade.py test_dashboard_numbers.py test_document_renderer.py test_exam_unit_aliases.py test_explicit_foundations.py test_identity_text.py test_isolated_grading.py test_iuea_foundations.py test_later_assessments.py test_later_teaching_consistency.py test_pandas_continuity.py test_presentation_guidance.py test_programme_reconciliation.py test_registration_authority.py test_revision_grader_alignment.py test_revision_slides.py test_sector_findings.py test_separator_reconciliation.py test_slide_specific_notes.py test_test1_coding.py test_assessment_pipeline.cjs

At the time, `test_assessment_pipeline.cjs` failed at line 75 because it expected `submissionAssessmentReleased_('CML3112|W06', ...)` to be true, although waived Week 6 correctly remains blocked. Its assertion was updated on 4 November; the other failures listed above were outside that run's assessment changes.

## Found and fixed on the way

- The 30 October syllabus patch gave the CML3112 syllabus the CML3111 deadlines (20 Nov, 10 Dec) and the CML3113 syllabus the CML3112 deadlines (17 Nov, 7 Dec). The new patch reads the course code from each document.
- The form descriptions of Weeks 1 to 5 still said "best ten of twelve" and "best nine of eleven". The generator now says best 3 of 5, 35 marks and 15 percent. The live descriptions of Weeks 1 to 5 are not pushed (those forms have responses).
- `importMarkedResults` in `gradebook.gs` no longer accepts the "Practical Test 2" column as an import target, so marks cannot be written into a column that is no longer counted.
- The four `*_20261030.py` policy scripts would now overwrite the new arrangement if someone ran them. Each exits with "SUPERSEDED" instead. The two `*_20261030.gs` files are empty stubs for the same reason.

## What I could not verify

- Any live behaviour. The helper functions were run against fake Forms written to match the calls the existing code already makes (`getItems`, `deleteItem`, `addMultipleChoiceItem`, `setCustomClosedFormMessage`, `setAcceptingResponses`). A real form may behave differently, for example in how long `replaceWeek11Questions()` takes.
- Whether the live Week 8 to 11 forms already carry the questions in the bank. `checkBlockQuizForms()` tests exactly that and only blocks a sitting for Week 11.
- Whether anybody has responses on the Week 11 forms (`replaceWeek11Questions()` skips those).
- Whether an earlier `applyBlockWindows()` was ever run. The new one handles both cases.
- Word and Excel rendering in Word itself (checked in LibreOffice only), and the master plan workbook's Class 1 to 4 session detail, which still describes the old design (a row-level note points to the plan and the lecturer guides).
- The new decks, labs and guides in `second_half/` were not touched, so their assessment slides were not compared with this arrangement. Their text on Block 1, Block 2 and the Week 12 demo should be read once.
- The Lecturer Teaching Guide W1-W15, the old Week 8 to 15 decks and ZIPs, `Teaching_Progress.md`, `Before_Each_Class_Checklist.md` and the other Word documents still describe the old calendar. They were outside the list you gave.
