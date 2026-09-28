# CML3111 Week13 Engineering

Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.

## Slide 1 — Making the project understandable and runnable

TEACHING PURPOSE
Making the project understandable and runnable

LECTURER CUE
Use PowerPoint Presenter View for these notes. Teach one example, pause for every learner to predict, then work an analogous example together. The practice notebook is a learning aid, not an extra graded upload.

NEXT
Today’s learning. Move on after a learner can explain the current example or required action.

## Slide 2 — Today’s learning

TEACHING PURPOSE
Today’s learning

CONNECT
Build on the preceding slide: Making the project understandable and runnable.

LECTURER CUE
Ask learners to explain this goal in ordinary language. The first successful attempt matters more than covering optional extensions. Defer: Package refactoring, complex repository layout and extra tooling are optional. Keep a working simple notebook.

EXPLAIN IN ORDINARY WORDS
A repository is the project folder and recorded history. A commit records a chosen change; uploading or pushing shares it. A README tells someone else how to run the work.

CHECK AND EXPECTED ANSWER
Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.

IF LEARNERS ARE STUCK
Ask a partner to follow only the README. It should identify the data, files, run order and expected result. Keep secrets out of the repository.

NEXT
Recall and a first attempt. Move on after a learner can explain the current example or required action.

## Slide 3 — Recall and a first attempt

TEACHING PURPOSE
Recall and a first attempt

CONNECT
Build on the preceding slide: Today’s learning.

LECTURER CUE
Allow two minutes for everyone to try. Ask pairs to compare. If many cannot begin, show the first step and repeat with changed values. Checkpoint for today: A partner can locate the input data and follow the run order without hints.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

NEXT
The engineering context. Move on after a learner can explain the current example or required action.

## Slide 4 — The engineering context

TEACHING PURPOSE
The engineering context

CONNECT
Build on the preceding slide: Recall and a first attempt.

LECTURER CUE
A team records device temperature to investigate cooling. Use a communications cabinet, an electrical enclosure or a robot controller as the physical example. No specialist hardware knowledge is assumed.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

NEXT
Words we will use. Move on after a learner can explain the current example or required action.

## Slide 5 — Words we will use

TEACHING PURPOSE
Words we will use

CONNECT
Build on the preceding slide: The engineering context.

EXPLAIN IN ORDINARY WORDS
A repository is the project folder and recorded history. A commit records a chosen change; uploading or pushing shares it. A README tells someone else how to run the work.

CHECK AND EXPECTED ANSWER
Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.

IF LEARNERS ARE STUCK
Ask a partner to follow only the README. It should identify the data, files, run order and expected result. Keep secrets out of the repository.

POINT TO THE DEFINITION
Reproducibility: Another person can use the stated data, environment and steps to check the result. Terminology varies; state the operational test.
Dependency: A package your code needs. Record versions actually used, rather than guessing them.

NEXT
Words we will use. Move on after a learner can explain the current example or required action.

## Slide 6 — Words we will use

TEACHING PURPOSE
Words we will use

CONNECT
Build on the preceding slide: Words we will use.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

POINT TO THE DEFINITION
Relative path: A location interpreted from the current working folder. It is not always relative to the notebook file itself.
README: The project’s instructions: question, files, data source, environment, run order, results and limitations.

NEXT
A useful README. Move on after a learner can explain the current example or required action.

## Slide 7 — A useful README

TEACHING PURPOSE
A useful README

CONNECT
Build on the preceding slide: Words we will use.

EXPLAIN IN ORDINARY WORDS
A repository is the project folder and recorded history. A commit records a chosen change; uploading or pushing shares it. A README tells someone else how to run the work.

CHECK AND EXPECTED ANSWER
Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.

IF LEARNERS ARE STUCK
Ask a partner to follow only the README. It should identify the data, files, run order and expected result. Keep secrets out of the repository.

NEXT
Someone else needs to reproduce the result. Move on after a learner can explain the current example or required action.

## Slide 8 — Someone else needs to reproduce the result

TEACHING PURPOSE
Someone else needs to reproduce the result

CONNECT
Build on the preceding slide: A useful README.

LECTURER CUE
Ask students to describe what they see before introducing terminology. Generated conceptual teaching illustration.  Source: figs/experiential/ASSET_SOURCES.md.

NEXT
A reproducible notebook starts fresh. Move on after a learner can explain the current example or required action.

## Slide 9 — A reproducible notebook starts fresh

TEACHING PURPOSE
A reproducible notebook starts fresh

CONNECT
Build on the preceding slide: Someone else needs to reproduce the result.

LECTURER CUE
Demonstrate restarting, uploading the issued data, and running all. The same result also depends on data, package versions and any random seeds.
Source: existing course illustration figs/execution_trap.png. These are illustrative examples, not this cohort’s assessed results.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Saved outputs can hide missing steps. Move on after a learner can explain the current example or required action.

## Slide 10 — Saved outputs can hide missing steps

TEACHING PURPOSE
Saved outputs can hide missing steps

CONNECT
Build on the preceding slide: A reproducible notebook starts fresh.

LECTURER CUE
Demonstrate a clean run from a fresh session with the actual files. If a variable exists only from an earlier manual cell run, fix the run order.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
A path names where a file is found. Move on after a learner can explain the current example or required action.

## Slide 11 — A path names where a file is found

TEACHING PURPOSE
A path names where a file is found

CONNECT
Build on the preceding slide: Saved outputs can hide missing steps.

LECTURER CUE
Explain every dependency and test a relative path. Include data-access instructions if the data cannot be redistributed.

EXPLAIN IN ORDINARY WORDS
A CSV is a text table. The header supplies column names. With csv.DictReader, values start as text, even if they look like numbers. A path tells Python where the file is.

CHECK AND EXPECTED ANSWER
Can "2.5" from csv.DictReader be added as a number without conversion? No; convert valid numeric text first.

IF LEARNERS ARE STUCK
Show the file in the runtime folder and compare its exact filename, case and column headers. Upload data again after a fresh Colab runtime.

NEXT
Read the path example. Move on after a learner can explain the current example or required action.

## Slide 12 — Read the path example

TEACHING PURPOSE
Read the path example

CONNECT
Build on the preceding slide: A path names where a file is found.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

POINT TO THE DEFINITION
Path and cwd: Path is a tool imported from Python’s pathlib module. Path.cwd() returns the folder where Python is currently running.
name: The .name property gives the last folder component as text. It depends on your runtime. A different folder name is expected on another computer.

NEXT
Worked example. Move on after a learner can explain the current example or required action.

## Slide 13 — Worked example

TEACHING PURPOSE
Worked example

CONNECT
Build on the preceding slide: Read the path example.

LECTURER CUE
Demonstrate a clean run from a fresh session with the actual files. If a variable exists only from an earlier manual cell run, fix the run order. Explain every dependency and test a relative path. Include data-access instructions if the data cannot be redistributed. Model actionable feedback: “Step 2 names data.csv, but the supplied file is readings.csv; please make them match.”

Complete practice code:
from pathlib import Path
print(Path.cwd().name)
# The name depends on the folder where Python is running.

WALK THROUGH THIS CODE
import loads a library. from selects a tool from it.
print displays a value below the cell.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Expected output. Move on after a learner can explain the current example or required action.

## Slide 14 — Expected output

TEACHING PURPOSE
Expected output

CONNECT
Build on the preceding slide: Worked example.

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

NEXT
Tell another person what the project needs. Move on after a learner can explain the current example or required action.

## Slide 15 — Tell another person what the project needs

TEACHING PURPOSE
Tell another person what the project needs

CONNECT
Build on the preceding slide: Expected output.

EXPLAIN IN ORDINARY WORDS
Training fits rules. Validation helps choose among rules. The final test estimates performance after choices are fixed. Information that would be unavailable at the real prediction time must stay out of the inputs.

CHECK AND EXPECTED ANSWER
May two readings of the same machine appear on both sides when evaluating new machines? No; split by machine. For forecasting, train on the past and evaluate later time.

IF LEARNERS ARE STUCK
Use three envelopes. Keep the final-test envelope closed while selecting features or settings.

POINT TO THE DEFINITION
requirements.txt and versions: This text file lists required Python packages and their versions. Record the versions used in the working environment; test them with the supplied run instructions.
Data source, permission and seed: Name the data source and any licence or permission for reuse. Record random seeds used in modelling. A seed supports repeatability; it does not repair data leakage.

NEXT
Words we will use. Move on after a learner can explain the current example or required action.

## Slide 16 — Words we will use

TEACHING PURPOSE
Words we will use

CONNECT
Build on the preceding slide: Tell another person what the project needs.

EXPLAIN IN ORDINARY WORDS
A repository is the project folder and recorded history. A commit records a chosen change; uploading or pushing shares it. A README tells someone else how to run the work.

CHECK AND EXPECTED ANSWER
Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.

IF LEARNERS ARE STUCK
Ask a partner to follow only the README. It should identify the data, files, run order and expected result. Keep secrets out of the repository.

POINT TO THE DEFINITION
Peer review: Someone else tests the instructions and reports a specific observation and suggested improvement.
Contribution evidence: A record of each person’s work, tied to files, commits or explanations. It does not require making a private repository public.

NEXT
Useful feedback identifies an exact repair. Move on after a learner can explain the current example or required action.

## Slide 17 — Useful feedback identifies an exact repair

TEACHING PURPOSE
Useful feedback identifies an exact repair

CONNECT
Build on the preceding slide: Words we will use.

LECTURER CUE
Model actionable feedback: “Step 2 names data.csv, but the supplied file is readings.csv; please make them match.”

EXPLAIN IN ORDINARY WORDS
A CSV is a text table. The header supplies column names. With csv.DictReader, values start as text, even if they look like numbers. A path tells Python where the file is.

CHECK AND EXPECTED ANSWER
Can "2.5" from csv.DictReader be added as a number without conversion? No; convert valid numeric text first.

IF LEARNERS ARE STUCK
Show the file in the runtime folder and compare its exact filename, case and column headers. Upload data again after a fresh Colab runtime.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
You are a new project user. Move on after a learner can explain the current example or required action.

## Slide 18 — You are a new project user

TEACHING PURPOSE
You are a new project user

CONNECT
Build on the preceding slide: Useful feedback identifies an exact repair.

LECTURER CUE
Do this before revealing the discussion slide. One learner moves or writes the items, the other checks. Swap roles. Every student explains one step. Expected: Success means the instructions produce the stated result. Record the observed issue rather than simply writing "works".
Wait for an individual prediction before inviting pair discussion. Give a first-step hint if needed.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
What the activity shows. Move on after a learner can explain the current example or required action.

## Slide 19 — What the activity shows

TEACHING PURPOSE
What the activity shows

CONNECT
Build on the preceding slide: You are a new project user.

LECTURER CUE
Ask which step produced this answer. Return to the concrete action if a learner cannot explain it. This is practice feedback, never a quiz key.

NEXT
Your turn. Move on after a learner can explain the current example or required action.

## Slide 20 — Your turn

TEACHING PURPOSE
Your turn

CONNECT
Build on the preceding slide: What the activity shows.

LECTURER CUE
Give silent thinking time, then let pairs discuss. Rotate who types. This is practice, not a graded quiz. Expected response: Revise that step and repeat. A claim that the notebook runs is supported by a fresh run, not by saved outputs alone.

EXPLAIN IN ORDINARY WORDS
A repository is the project folder and recorded history. A commit records a chosen change; uploading or pushing shares it. A README tells someone else how to run the work.

CHECK AND EXPECTED ANSWER
Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.

IF LEARNERS ARE STUCK
Ask a partner to follow only the README. It should identify the data, files, run order and expected result. Keep secrets out of the repository.

DISCUSSION KEY FOR THIS SLIDE
DISCUSS THE REASONING
Practice discussion
Revise that step and repeat. A claim that the notebook runs is supported by a fresh run, not by saved outputs alone.
Which step produced this result? What changes if one input changes?
CML3111   Week 13   21
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
Practice discussion. Move on after a learner can explain the current example or required action.

## Slide 21 — Practice discussion

TEACHING PURPOSE
Practice discussion

CONNECT
Build on the preceding slide: Your turn.

LECTURER CUE
Ask how the result was obtained. Reteach the smallest missing step instead of giving a longer lecture.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Short explainer and discussion. Move on after a learner can explain the current example or required action.

## Slide 22 — Short explainer and discussion

TEACHING PURPOSE
Short explainer and discussion

CONNECT
Build on the preceding slide: Practice discussion.

LECTURER CUE
Title, channel, 19:53 runtime and chapter boundaries checked on the video page on 15 September 2026. Desktop installation is optional. The originally shared t=167 link starts at installation.
After viewing: Explain the difference between saving a file and recording a commit. Then make one browser-based commit.
Preview before class and stop after the selected short excerpt. If playback fails, teach the worked example. Video is optional. Source: https://www.youtube.com/watch?v=v5gnvDUWqFM

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

VIDEO ROUTINE
Preview the exact link and stated excerpt before class. State the viewing question first, pause after the example, and ask a learner to explain it. If access fails, use the adjacent worked example and discussion rather than spend class time troubleshooting streaming.

NEXT
After the video. Move on after a learner can explain the current example or required action.

## Slide 23 — After the video

TEACHING PURPOSE
After the video

CONNECT
Build on the preceding slide: Short explainer and discussion.

EXPLAIN IN ORDINARY WORDS
A repository is the project folder and recorded history. A commit records a chosen change; uploading or pushing shares it. A README tells someone else how to run the work.

CHECK AND EXPECTED ANSWER
Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.

IF LEARNERS ARE STUCK
Ask a partner to follow only the README. It should identify the data, files, run order and expected result. Keep secrets out of the repository.

NEXT
Preparing for the assignment. Move on after a learner can explain the current example or required action.

## Slide 24 — Preparing for the assignment

TEACHING PURPOSE
Preparing for the assignment

CONNECT
Build on the preceding slide: After the video.

LECTURER CUE
No new weekly assignment. Continue the official project deliverables and Week 13 quiz. Rehearse offline TEST2 saving and the published function interfaces before Week 14. Do not add an extra upload.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
A reproducible handover. Move on after a learner can explain the current example or required action.

## Slide 25 — A reproducible handover

TEACHING PURPOSE
A reproducible handover

CONNECT
Build on the preceding slide: Preparing for the assignment.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
A repository is the project folder and recorded history. A commit records a chosen change; uploading or pushing shares it. A README tells someone else how to run the work.

CHECK AND EXPECTED ANSWER
Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.

IF LEARNERS ARE STUCK
Ask a partner to follow only the README. It should identify the data, files, run order and expected result. Keep secrets out of the repository.

NEXT
A reproducible handover continued. Move on after a learner can explain the current example or required action.

## Slide 26 — A reproducible handover continued

TEACHING PURPOSE
A reproducible handover continued

CONNECT
Build on the preceding slide: A reproducible handover.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
A repository is the project folder and recorded history. A commit records a chosen change; uploading or pushing shares it. A README tells someone else how to run the work.

CHECK AND EXPECTED ANSWER
Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.

IF LEARNERS ARE STUCK
Ask a partner to follow only the README. It should identify the data, files, run order and expected result. Keep secrets out of the repository.

NEXT
Project preparation. Move on after a learner can explain the current example or required action.

## Slide 27 — Project preparation

TEACHING PURPOSE
Project preparation

CONNECT
Build on the preceding slide: A reproducible handover continued.

LECTURER CUE
Explain the released brief now. Confirm its grading-release checks before assigning it. Avoid treating weekly practice as a substitute for the project evidence. The project brief remains authoritative.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Week 13 quiz. Move on after a learner can explain the current example or required action.

## Slide 28 — Week 13 quiz

TEACHING PURPOSE
Week 13 quiz

CONNECT
Build on the preceding slide: Project preparation.

LECTURER CUE
Activate the matching open_W13_CML3111 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

QUIZ OPERATION
Opening the student link does not activate the quiz. In Quiz Controls run the matching open_W<week>_<cohort> function once when ready. Announce the logged closing time: 24 hours after activation. Five minutes describes expected answering time, not the availability window. Quiz 1 and Quiz 2 require separate activation when collecting catch-up work.

NEXT
Before you leave. Move on after a learner can explain the current example or required action.

## Slide 29 — Before you leave

TEACHING PURPOSE
Before you leave

CONNECT
Build on the preceding slide: Week 13 quiz.

LECTURER CUE
Ask every learner for an individual response. Record one misconception to revisit at the start of the next class. If a deadline changed, announce the exact Kampala date and update the source registry before rebuilding slides.

EXPLAIN IN ORDINARY WORDS
A repository is the project folder and recorded history. A commit records a chosen change; uploading or pushing shares it. A README tells someone else how to run the work.

CHECK AND EXPECTED ANSWER
Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.

IF LEARNERS ARE STUCK
Ask a partner to follow only the README. It should identify the data, files, run order and expected result. Keep secrets out of the repository.

