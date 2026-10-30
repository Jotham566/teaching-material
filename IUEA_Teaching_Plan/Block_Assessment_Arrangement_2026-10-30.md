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

Weekly work in Weeks 1 to 6 keeps the best 4 of 6 (best 3 of 5 for CML3112 and CML3113, where Week 6 is not assigned). Blocks are never dropped, because each one carries three classes of teaching. A part that is not submitted scores zero.

Quizzes are out of 50 marks (45 when Week 6 is not assigned). Assignments are out of 180 marks (160). The percentage is marks earned divided by that total, times 10. Course weights are unchanged: quizzes 10, assignments 10, Data Analysis Project 10, Practical Test 1 15, Practical Test 2 20, Engineering ML Project 25, Demonstration 10.

## What changed in the files

Decks for Weeks 1, 8 to 13 (assessment slides, exit slides, spoken notes), student guides (Weeks 8 to 12 plus new `B1.md` and `B2.md` per cohort), the assignment banks and the Week 8 to 12 student ZIPs (deadline line and a block note), `Assignment_Instructions_Index.md`, `Assignment_Submission_Links.md`, `data/assessments.json` (new closing times), the three syllabi, the master teaching plan (docx and the Assessment sheet), the Quiz Operations Guide and the grader README.

## What you still do by hand

1. In the Apps Script submission project, run `applyBlockWindows()` from `grader/apply_block_windows_20261030.gs` once. It moves the A7 to A11 form windows.
2. In the quiz project, run `open_Block1_CML31xx` in the last 20 minutes of the Week 10 class and `open_Block2_CML31xx` in the Week 13 class, from `grader/block_quiz_sittings_20261030.gs`.
3. Install the updated gradebook rule if you grade from `continuous_assessment.py`. That script was left unchanged on purpose and still counts the old weekly rule, so aggregate by hand or edit its constants before final marks.
4. The Q12 quiz bank was written for the old Week 13. It does not ask about regularisation or nearest neighbours. Write a new bank, regenerate the form with `build_quiz_forms_gs.py`, rebuild the live form, and update `data/quiz_links.json`.
5. Tell students once, in class, that the weekly quiz and assignment stop after Week 6 and what the block deadlines are.
