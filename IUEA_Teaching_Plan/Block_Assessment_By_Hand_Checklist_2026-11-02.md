# What you still do by hand (2 November 2026)

> **Update of 3 November 2026.** Parts A and B below are unchanged. Part C (gradebook) is replaced by `Grading_Update_By_Hand_2026-11-03.md`, and the project and demo items in part D no longer apply (there is no demo).

Nothing live has been changed. I had no network, so every Google Form, Sheet and Apps Script project is exactly as you left it. The steps below are in the order to do them. Under each step is what the log shows when it works. If a line says something else, stop and send me the log.

Each project below has its own Apps Script editor. Run a function by choosing it in the function box and pressing Run, then open View > Logs (or Execution log).

**Do not run `rebuildAllForms()`.** It deletes all 36 forms and changes every link.

## A. Quiz project (the one that holds `create_quiz_forms.gs`)

Do A1 to A7 this week. They only need to be done before Tuesday 10 November, except A5 and A6 which must be done before Tuesday 24 November.

| # | Do this | It works when |
|---|---|---|
| A1 | Copy the current `create_quiz_forms.gs` somewhere safe (a copy is also in `grader/_backup_2026-11-02/`). Open the new `grader/create_quiz_forms.gs`, select all, copy. In the editor open `create_quiz_forms.gs`, select all, paste over it, Save. | Save finishes without a red error banner. The file is about 455 KB (the old one was 462 KB). |
| A2 | In the editor add a new script file named `block_quiz_sittings_20261102` and paste `grader/block_quiz_sittings_20261102.gs` into it. If the project still has `block_quiz_sittings_20261030`, **delete that file**. Two files with the same function names would silently let one win. | The project has exactly one file that defines `open_Block1_CML3112`. |
| A3 | Run `retireQ11AndQ12Forms()`. | Six lines `RETIRED CML31xx\|12 (...), 0 responses kept` and `CML31xx\|13 ...`, then `retireQ11AndQ12Forms: 6 forms closed and retired, 0 not found (expected 6 closed, 0 not found).` If a line says `N responses kept` with N above 0, tell me. The responses stay, the form just closes. |
| A4 | Run `closeStatus()`. | `quizzes pending a close: 0` and `Nothing is open.` (Nothing retired is waiting to close.) |
| A5 | Run `replaceWeek11Questions()`. This puts the new Q10 questions on the three existing Week 11 forms. Links, QR codes and response sheets stay the same. | Three lines `replaced the questions on CML31xx · Weekly Quiz 10 — Features and choosing a model`, then `done: 3 forms replaced, 0 skipped. Links and QR codes are unchanged.` If it prints `SKIPPED CML31xx week 11: it already has N responses`, that form was left alone. Tell me, do not rebuild. |
| A6 | Run `refreshBlockQuizIntros()`. It puts the block wording ("sat together in the last 20 minutes of Class 2 or 4", out of 35, 15 percent) into the Week 8, 9, 10 and 11 form descriptions. | Twelve lines `description updated: CML31xx week N`, then `refreshBlockQuizIntros: 12 updated, 0 skipped (expected 12 updated).` A form with responses or one that is open is skipped with a line saying so. |
| A7 | Run `checkBlockQuizForms()`. Read only. | Twelve lines starting `OK` (for example `OK      CML3112 B1 Q7 (week 8)`) and `checkBlockQuizForms: 12 OK, 0 with problems (expected 12 OK).` Lines starting `warning` (for example a title difference) do not stop a sitting. |
| A8 | Check one Week 11 form by eye: open its link as a student would. Run `audit_W11_CML3112` (then `audit_W11_CML3113`, `audit_W11_CML3111`). | The form's first question is "Which candidate meets both constraints?" and the third is "What check prevents this error?". The audit shows `TOTAL POINTS ON THIS FORM: 5` and `DIAGNOSIS: the marking side of this form is correct`. |

### Sitting days

| When | Run | It works when |
|---|---|---|
| Class 2, last 20 minutes. CML3112 Tue 10 Nov 13:40. CML3113 Fri 13 Nov 10:40. CML3111 Fri 13 Nov 13:40. | `open_Block1_CML3112`, `open_Block1_CML3113` or `open_Block1_CML3111` | The usual `OPEN:` and `link:` lines for the Week 8 form and again for the Week 9 form, then `OPENED CML3112 Block 1: Q7 and Q8 (weeks 8 and 9). Each closes itself after 24 hours.` Show both QR codes or share both links. If it is not the planned day it adds `NOTE: today is ... but ... is planned for ...` and opens anyway. |
| Right after opening | `closeStatus()` | `quizzes pending a close: 2` with two lines `closes ... (24 hours from now)`. |
| Class 4, last 20 minutes. CML3112 Tue 24 Nov 13:40. CML3113 Fri 27 Nov 10:40. CML3111 Fri 27 Nov 13:40. | `open_Block2_CML3112`, `open_Block2_CML3113` or `open_Block2_CML3111` | Same, ending `OPENED CML3112 Block 2: Q9 and Q10 (weeks 10 and 11).` If the Week 11 form still has the old questions it prints `NOT OPENED. ... run replaceWeek11Questions() ... Nothing was opened.` Fix that and run it again. |
| Next day | `closeStatus()` | `Nothing is open.` |
| Emergency, to close early | `close_Block1_CML31xx` or `close_Block2_CML31xx` | `CLOSED CML31xx Block 1 (Q7 and Q8).` |
| Emergency, if the check blocks you on the day | `open_W8_CML31xx` and `open_W9_CML31xx` (Block 1) or `open_W10_CML31xx` and `open_W11_CML31xx` (Block 2) | These open one form each and skip all checks. Opening week 12 or 13 now throws `... is retired and is not sat this semester.` |

The projected clock (`quiz_timer.html`) is still five minutes. For two quizzes in 20 minutes run it twice, or tell the room it has about ten minutes each.

When you import the marks, use the existing `configureQuizImports` and `importQuizScores` steps for weeks 8, 9, 10 and 11 only. Leave weeks 12 and 13 out. The gradebook ignores the Q11 and Q12 columns even if they hold marks.

## B. Submission project (the one that holds `submission_forms.gs`)

| # | Do this | It works when |
|---|---|---|
| B1 | Add a new file `apply_block_windows_20261102` and paste `grader/apply_block_windows_20261102.gs`. If the project has `apply_block_windows_20261030`, delete it. | Save without errors. |
| B2 | Run `applyBlockWindows()`. Do it before Tuesday 17 November. It moves the A9, A10 and A11 closing times and leaves every opening time as it is. A7 and A8 already close on the dates you want. | Lines `set CML31xx\|W10 opens ... closes ...` for the changed forms (nine on a normal run) and `already set ...` for the others, then `applyBlockWindows: 9 set, 6 already correct, 0 left (15 in all). Now run showBlockWindows() ...`. If it says `Stopped before the six-minute limit`, run it again, it skips what is done. |
| B3 | Run `showBlockWindows()`. Read only. | Fifteen lines starting `OK` and `showBlockWindows: 15 OK, 0 need attention (expected 15 OK).` A line starting `DIFFERS` shows the expected closing time. |

## C. Gradebook sheet

| # | Do this | It works when |
|---|---|---|
| C1 | Paste `grader/gradebook.gs` over the script bound to the Grades sheet. | Save without errors. |
| C2 | Run `recomputeAll()`. Everybody's Final % changes because the weights changed. | A toast `Recomputed N rows.` The Q11, Q12 and Practical Test 2 columns can stay in the sheet, they are ignored. Check one student against the Check below. |
| C3 | Check one row by hand: a student with full marks in every quiz and assignment column that counts (Q1 to Q5, Q7 to Q10, W01 to W05, W08 to W12) should show 15 from quizzes and 15 from assignments. | `showProgress` on that row reports `Block 1 quiz: 2 of 2 forms sat, 10 of 10 marks` and `Block 2 assignment: 3 of 3 parts submitted, 60 of 60 marks`. |

## D. Things only you can decide or do

1. **Weights.** 15 / 15 / 10 / 15 / 30 / 15 are in every document. They still need checking against IUEA regulations.
2. **Project and demo.** The Week 12 demo mark scheme, whether it is marked per team or per student, the project milestones and the due date are all written as "to be confirmed by the lecturer". The DEMO and ML_PROJECT submission forms have no open or close time, so they stay closed until you set one with `setSubmissionWindow(key, openAt, closeAt)` in the submission project.
3. **Opening times of A9 to A11.** I left them as they were. A9 opens on the Class 2 date (CML3112 Tue 10 Nov) and A10 on the Class 3 date, a week before the class that teaches them. Say if you want them moved to the class date.
4. **Contact hours.** The syllabi now say 12 study weeks and 36 contact hours (12 x 3), which I worked out. Confirm that is the number IUEA wants.
5. **Tell the students once, in Class 2 and again in Class 3:** no Test 2, two quiz sittings (Class 2 and Class 4), Block 1 closes Tue 17 Nov or Fri 20 Nov, Block 2 closes Tue 1 Dec or Fri 4 Dec, and the Week 12 demo.
6. **Student ZIPs.** The Week 8 to 12 ZIPs in `student_packages/` were rebuilt with the new START_HERE wording. Only resend them if students need the new wording. The live form shows the deadline that counts.
7. **Still open from the plan:** open each class notebook once in real Colab and run all cells (I could only run them against a NumPy stand-in for scikit-learn), and tell the Friday cohorts that Class 1 is a recap plus a long lab.


<!-- AUDIT_20261104 -->
> **Update of 4 November 2026.** Items D1 and D5 above are stale. The weights are now 15 / 15 / 10 / 15 / 45 (no demo, no Practical Test 2). The Engineering ML project is an individual, timed, auto-graded 3-hour Colab sitting in the Week 12 class slot, and there is no Week 12 demo. Tell the students that in Class 2 and Class 3 (wording in `Grading_Update_By_Hand_2026-11-03.md`, section 4). In D2, the DEMO and ML_PROJECT upload forms are not used; the project window is set in the collector (`second_half/Project/deploy/DEPLOYMENT_STEPS.md`).
