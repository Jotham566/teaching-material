# IUEA teaching progress

> Current status: the last section of this file, **Status 4 November 2026** (project arrangement updated 13 November 2026). Everything between here and there is history.

## History: status of 29 September 2026

| Cohort | Confirmed coverage | Next lesson |
|---|---|---|
| CML3112 | All Week 3 content completed on 29 September | Week 4, from its opening recap; teach loops and file reading before expecting A4 completion. |
| CML3113 | Week 3 not yet taught | Week 3 from slide 1. |
| CML3111 | Week 3 not yet taught | Week 3 from slide 1. |

Form availability does not mean the topic has already been taught. CML3112 A4 is open by the lecturer's request, but the Week 4 lesson is still next. The opening operation did not confirm Week 4 teaching.

## Explain an assignment in one minute

1. Show the exact assignment notebook filename (or required document for a report task).
2. State the outcome: “You will produce these named outputs.” Point to the marks beside each task.
3. State the upload count and formats. For A3 and A4, it is **one completed assignment notebook**.
4. Show the cohort's student form and its current Kampala deadline.
5. Ask students to locate the first task. Setup help is optional reference; practice notebooks are not submissions.

Share the refreshed student ZIP for the cohort and week. Students already working in an older copy should keep their answers and use the new instructions as a reference; they do not need to restart or resubmit solely because the wording changed. Assessed outputs, marks and deadlines are unchanged by this clarity revision.

## Current CML3112 availability

See [the 29 September student links](CML3112_Sept29_Student_Links.md). That separate, earlier reopening superseded the original A3 deadline. This instruction revision makes no further availability change.

## Approved A3 extension for Friday cohorts

The lecturer approved a one-week extension on 29 September because Week 3 has not yet been taught:

- CML3113 A3: **9 October 2026 at 08:00 Kampala**.
- CML3111 A3: **9 October 2026 at 11:00 Kampala**.

These replace the previous 2 October deadlines. Existing work remains valid. No quiz or other assignment deadline changes accompany this extension.

## Student packages: no grading scripts

Updated Week 3 and Week 5 notebooks need no grader imports or self-check files. Share the current ZIPs in `student_packages`. The lecturer’s automatic grader still evaluates every task, including hidden checks, after upload. Existing submissions remain valid; do not ask students to redo their work. Students using an old notebook may keep it with its original helpers, or copy their answers into the updated notebook.

## Status 4 November 2026 (project arrangement updated 13 November 2026)

This is the current position. The older sections above are history.

- Weeks 1 to 7 are done. Week 7 was Practical Test 1. Week 6 was practical revision (A6 and Quiz 6 not assigned; they do not count).
- Week 8 theory: CML3113 and CML3111 had it on Friday 30 October, without the lab. CML3112 starts Week 8 on Tuesday 3 November.
- The semester ends at Week 12 (12 study weeks, 36 contact hours). Weeks 8 to 11 are taught as four classes, concepts first and then the lab. Slides, lab notebooks, lecturer guides, student packages, student slide PDFs and the project are in `second_half/`.

| Class | Content | CML3112 (Tue) | CML3113 and CML3111 (Fri) |
|---|---|---|---|
| 1 First model | Week 8 | Tue 3 Nov | Fri 6 Nov (concepts recap, then the lab) |
| 2 Classification | Week 9 | Tue 10 Nov | Fri 13 Nov |
| 3 Trust | Week 10 | Tue 17 Nov | Fri 20 Nov |
| 4 Choosing | Week 11 | Tue 24 Nov | Fri 27 Nov |

- Week 12 is the Engineering ML project: individual, timed, auto-graded, sat online in Google Colab from anywhere (own laptop, own Google account, internet). There is no room and no in-person invigilation. Same entry page, countdown and Submit test flow as Practical Test 1. Part A coded notebook 30 plus Part B decision memo 15 (a form inside the notebook) = 45 raw, scaled to 40 percent of the course. It covers Weeks 1 to 10 only (the first half plus Classes 1 to 3). The Week 11 tasks (feature ablation, writing the model-choice rule) are cut; the model-choice rule is a supplied cell the student calls.
- Project data (13 November 2026): real data, the same file for every student in all three cohorts, with no variants. It is the UCI Steel Industry Energy Consumption dataset (DAEWOO Steel, 2018, 35,040 readings of 15 minutes, CC BY 4.0), built into the notebook. Question 1 predicts Usage_kWh; Question 2 warns on readings of 60 kWh or more. Split by month: train January to August, validate September to October, test November to December. Students may add their own cells; work is marked wherever it is, as long as the required function names exist when the notebook runs from the top. The rehearsal uses the same file with a different target (lagging reactive power, kVarh).
- One window for all three cohorts (confirmed 13 November 2026): opens Monday 23 November 2026, 00:00 Kampala time, closes Wednesday 25 November 2026, 23:59. Each student has 3 hours from pressing Start test, capped at the window's close, so start by Wednesday 25 November, 20:59 to get the full 3 hours. The lecturer answers wording and technical questions on the class channel from 08:00 to 20:00 each day of the window (hours: lecturer to confirm). A student whose attempt fails for a technical reason reports it at once on the class channel with a screenshot; the lecturer can authorise one fresh attempt, still capped at the window's close. Marks are final by Wednesday 2 December 2026.
- An unmarked rehearsal on practice data is released right after Class 3: CML3112 Tue 17 Nov; CML3113 and CML3111 Fri 20 Nov.
- Gone: Practical Test 2, the demo and viva, Weeks 13 to 15, the project clinic, team ML projects, the old take-home project, the December due dates, and the Q11 and Q12 quizzes. The data analysis project no longer counts toward the final mark (it is still set as practice).
- Weights (policy of 10 November 2026, `Grading_Policy_2026-11-10.md`): assignments 20 (A1 to A5, all five count equally), quizzes 20 (Q1 to Q5, all five count equally), Practical Test 1 20, Engineering ML project 40. Not counted: Q6 onward and the Week 8 to 11 block quizzes (Q7 to Q10), A6 onward and the Week 8 to 11 block assignments (A7 to A11), the Data Analysis project, Practical Test 2 and the demo. Block 1 is A7 + A8 and Q7 + Q8 (quiz sat in the last 20 minutes of Class 2); Block 2 is A9 + A10 + A11 and Q9 + Q10 (last 20 minutes of Class 4). They are still set and collected as practice, with feedback. The best-3-of-5 rule, the Week 6 waiver and the block rule are retired. Results are provisional out of 60 until the project is marked.
- Details: `Grading_Policy_2026-11-10.md` (the current weights), `second_half/Plan_Weeks_8-12.pdf`, `Block_Assessment_Arrangement_2026-11-10.md`, `Block_Assessment_Arrangement_2026-11-03.md`, `second_half/Project/README.md` and `Grading_Update_By_Hand_2026-11-03.md`.
