<!-- SUPERSEDED_20261110 -->
> **Superseded on 10 November 2026 by `Grading_Policy_2026-11-10.md`.** The weights, the best-3-of-5 rule, the Week 6 waiver, the block rule and the provisional total out of 55 recorded below are history. From 10 November only A1 to A5 and Q1 to Q5 count: the final mark is assignments 20 + quizzes 20 + Practical Test 1 20 + Engineering ML project 40, and provisional results are out of 60. The body below is left unchanged as a record.

# Block assessment arrangement for the four-class second half

> **Superseded in part on 3 November 2026 by `Block_Assessment_Arrangement_2026-11-03.md`.** The blocks, deadlines, quiz sittings and the 35 and 160 totals below still stand. There is no Week 12 demo, the weights table and the project paragraph below no longer apply, and the Engineering ML project is now submitted (Part A /30, Part B /15, weight 45). The source of truth is `data/assessment_blocks_20261103.json`.

Written 2 November 2026. Supersedes `Block_Assessment_Arrangement_2026-10-30.md`. Source of truth: `data/assessment_blocks_20261102.json`. The steps you still do by hand, in order, are in `Block_Assessment_By_Hand_Checklist_2026-11-02.md`. The checks that were run are in `Block_Assessment_Verification_2026-11-02.md`.

## The decision (approved 2 November 2026)

The semester ends at Week 12. Practical Test 2 is dropped. Teaching is four classes, and Week 12 is a short project demo. Weeks 1 to 5 stay weekly (best 3 of 5, Week 6 waived). The forms, graders and graded functions are unchanged. Only deadlines, quiz sittings and the way marks are added up change.

| | CML3112 (Tue) | CML3113 (Fri 08:00) and CML3111 (Fri 11:00) |
|---|---|---|
| Class 1, Week 8 content | Tue 3 Nov | Fri 6 Nov |
| Class 2, Week 9 content | Tue 10 Nov | Fri 13 Nov |
| Class 3, Week 10 content | Tue 17 Nov | Fri 20 Nov |
| Class 4, Week 11 content | Tue 24 Nov | Fri 27 Nov |
| Week 12 short project demo | Tue 1 Dec | Fri 4 Dec |

| | Block 1 (Classes 1 and 2) | Block 2 (Classes 3 and 4) |
|---|---|---|
| Assignment parts | A7 Regression and baseline (20) + A8 Classification and cost (20) = 40 | A9 Validation and trust (20, Class 3) + A10 Features and ablation (20) + A11 Model recommendation (20), both Class 4 = 60 |
| Quiz forms | Q7 (Week 8 form) + Q8 (Week 9 form), 5 marks each = 10 | Q9 (Week 10 form) + Q10 (Week 11 form), 5 marks each = 10 |
| Quiz sitting | last 20 minutes of Class 2: CML3112 Tue 10 Nov, Fridays 13 Nov | last 20 minutes of Class 4: CML3112 Tue 24 Nov, Fridays 27 Nov |
| Each form stays open | 24 hours | 24 hours |
| Assignment closes, CML3112 | Tue 17 Nov 2026, 11:00 | Tue 1 Dec 2026, 11:00 |
| Assignment closes, CML3113 | Fri 20 Nov 2026, 08:00 | Fri 4 Dec 2026, 08:00 |
| Assignment closes, CML3111 | Fri 20 Nov 2026, 11:00 | Fri 4 Dec 2026, 11:00 |

Q11 (Week 12 form) and Q12 (Week 13 form) are retired and never sat. Block 1 deadlines are the same as in the 30 October note. Block 2 deadlines move earlier because the semester ends at Week 12.

## Grading

Quizzes are out of 3 x 5 + 10 + 10 = **35** marks. Assignments are out of 3 x 20 + 40 + 60 = **160** marks. Both counts assume Week 6 is waived, so the best 3 of the 5 weekly items count. A block is never dropped. A part that is not submitted scores zero. Each component is worth 15 percent of the course: marks earned divided by the total, times 15.

| Component | Old weight | New weight |
|---|---:|---:|
| Quizzes | 10 | 15 |
| Assignments | 10 | 15 |
| Data analysis project | 10 | 10 |
| Practical Test 1 | 15 | 15 |
| Practical Test 2 | 20 | dropped |
| Engineering ML project | 25 | 30 |
| Demonstration | 10 | 15 |
| Total | 100 | 100 |

The weights still need checking against IUEA regulations.

## Q10 changed

Class 4 now teaches model comparison as well as features. Two questions in Q10 (the Week 11 form) were swapped for two questions of the same kind from the retired Q11 bank:

| Position | Kind | Was | Now |
|---|---|---|---|
| 1 | interpretation | Which values are produced? (feature arithmetic) | Which candidate meets both constraints? |
| 3 | traceback | What does this error suggest? (KeyError on a feature) | What check prevents this error? (empty candidate table) |

The mix is unchanged: two interpretation, one diagnosis, one traceback, one judgement. The form title is now "Weekly Quiz 10 - Features and choosing a model". The five replaced and retired question lists are kept in `scripts/pandas_quiz_revision.py` (`RETIRED_ARCHIVE`).

## Week 12 project demo

Proposal, not final. Each team presents for about five minutes on demo day, with questions from the class. The marks, mark scheme, project milestones, due date, individual defence and prizes are **to be confirmed by the lecturer**. In `data/assessments.json` the TEST2 rows are retired and the DEMO and ML_PROJECT rows have no open or close time, so no form can open until you set one.

## What changed in the files

- Data: `data/assessment_blocks_20261102.json` (new), `data/assessments.json` (block deadlines, TEST2 retired, project and demo dates blank), `data/submission_links.json` (closing times).
- Apps Script: `grader/create_quiz_forms.gs` (regenerated; adds `replaceWeek11Questions()` and refuses to open weeks 12 and 13), `grader/block_quiz_sittings_20261102.gs` (new), `grader/apply_block_windows_20261102.gs` (new), `grader/gradebook.gs`. The two `_20261030.gs` files are now empty stubs so that their function names cannot clash.
- Python: `grader/continuous_assessment.py` (blocks, weights, half-up rounding to match the gradebook), `scripts/` (bank, generator, verifier, policy scripts).
- Documents: the three syllabi, the master teaching plan (docx and xlsx), the Weekly Quiz Operations Guide, `Assignment_Submission_Links.md`, `Assignment_Instructions_Index.md`, `grader/README.md`.
- Students: `student_guides/<cohort>/B1.md`, `B2.md`, `W08.md` to `W12.md`, a retired notice on `TEST2.md`, and the old 15 and 18 December deadlines removed from `DEMO.md` and `ML_PROJECT.md`. The Week 8 to 12 student ZIPs were rebuilt with the new START_HERE text.
- Every changed file has an untouched copy in a sibling `_backup_2026-11-02` folder.

## Not changed

The old Week 8 to 15 decks in `decks/` and their ZIPs, the Practical Test 2 notebooks, graders and portal files (kept, unused), the live Google Forms and Sheets (no network here), the Lecturer Teaching Guide W1-W15 and the other Word documents not listed above, and the notebooks' graded cells.
