# Block assessment arrangement from Week 8

Source of truth: `data/assessment_blocks_20261030.json`. This note explains it in plain language and lists what you still have to do by hand.

## The decision

From Week 8 there is no weekly quiz and no weekly assignment. There is one assignment pack and one quiz sitting after every three classes. Weeks 1 to 6 stay weekly. The forms, the graders and the graded functions are unchanged. Only the deadlines, the quiz sittings and the way marks are added up change.

| | Block 1 (Weeks 8 to 10) | Block 2 (Weeks 11 to 13) |
|---|---|---|
| Content | regression, baseline and errors; classification and cost; validation and leakage | features and ablation; choosing a model; regularisation, nearest neighbours, reproducibility |
| Assignment parts | A7 + A8 + A9, 20 marks each, 60 in all | A10 + A11, 20 marks each, 40 in all (Week 13 has no graded notebook) |
| Quiz | Q7 + Q8 + Q9, 5 marks each, 15 in all | Q10 + Q11 + Q12, 5 marks each, 15 in all |
| Quiz sitting | last 20 minutes of the Week 10 class, three forms opened together, 24 hours each | last 20 minutes of the Week 13 class, same way |
| Assignment closes, CML3111 | 20 Nov 2026, 11:00 | 10 Dec 2026, 23:59 |
| Assignment closes, CML3112 | 17 Nov 2026, 11:00 | 7 Dec 2026, 23:59 |
| Assignment closes, CML3113 | 20 Nov 2026, 08:00 | 10 Dec 2026, 23:59 |

## Grading

Weekly work stays in Weeks 1 to 5 and the best 3 of 5 count. Week 6 is waived for all three cohorts (see `Practical_Revision_Week6_Waiver.md`). Blocks are never dropped, because each one carries three classes of teaching. A part that is not submitted scores zero.

Quizzes are out of 45 marks and assignments out of 160. The percentage is marks earned divided by that total, times 10. Course weights are unchanged: quizzes 10, assignments 10, Data Analysis Project 10, Practical Test 1 15, Practical Test 2 20, Engineering ML Project 25, Demonstration 10.

## What changed in the files

Decks for Weeks 1, 8 to 13 (assessment slides, exit slides, spoken notes), student guides (Weeks 8 to 12 plus new `B1.md` and `B2.md` per cohort), the assignment banks and the Week 8 to 12 student ZIPs (deadline line and a block note), `Assignment_Instructions_Index.md`, `Assignment_Submission_Links.md`, `data/assessments.json` (new closing times), the three syllabi, the master teaching plan (docx and the Assessment sheet), the Quiz Operations Guide and the grader README.

## What you still do by hand

1. In the Apps Script submission project, run `applyBlockWindows()` from `grader/apply_block_windows_20261030.gs` once. It moves the A7 to A11 form windows.
2. In the quiz project, run `open_Block1_CML31xx` in the last 20 minutes of the Week 10 class and `open_Block2_CML31xx` in the Week 13 class, from `grader/block_quiz_sittings_20261030.gs`.
3. `grader/continuous_assessment.py` now has `coursework_totals()`, which applies this rule to the ledger. `gradebook.gs` already applies it.
4. The Week 13 quiz (Q12) bank has been rewritten for regularisation, nearest neighbours and reproducibility. See section below for how to rebuild the live form.
5. Tell students once, in class, that the weekly quiz and assignment stop after Week 6 and what the block deadlines are.

## Rebuilding the live Week 13 quiz form (Q12)

The new Q12 bank is in `scripts/quiz_bank_weeks.py` (`BANKS[13]`). Its two tables are the Week 13 deck's own numbers, and `scripts/verify_quiz_arithmetic.py` re-checks them. The 36-form script was regenerated, and only Week 13 changed.

1. Open the quiz Apps Script project and paste the new `grader/create_quiz_forms.gs` over the old file.
2. Run `replaceWeek13Questions()` once. It replaces the five questions on the three existing Week 13 forms and sets the new title and description. Links, QR codes and response sheets stay the same. A form that already has responses is skipped.
3. Run `auditForm(13, "CML3111")` and the same for CML3112 and CML3113 (through a small wrapper, as the Quiz Operations Guide describes), and open one form yourself.
4. Do not run `rebuildAllForms()` for this. It deletes all 36 forms and changes every link.

