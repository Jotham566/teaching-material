# CML3113 Week13 Mining Petroleum

Lecturer companion to the revised PowerPoint. Slide numbers match this edition. Explain the worked examples directly; revision checks are for individual study.

## Slide 1 — Making the project understandable and runnable

PURPOSE
Making the project understandable and runnable

CONNECT
Previous slide: the preceding week.

EXPLAIN
Mining and Petroleum Engineering

LECTURER CUE
Use PowerPoint Presenter View for these notes. Teach one example, pause for every learner to predict, then work an analogous example together. The practice notebook is a learning aid, not an extra graded upload.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Today’s learning.

REFERENCES


## Slide 2 — Today’s learning

PURPOSE
Today’s learning

CONNECT
Previous slide: Making the project understandable and runnable.

EXPLAIN
Run the project from a fresh session.

Repair unclear run instructions using a fresh run.

LECTURER CUE
Ask learners to explain this goal in ordinary language. The first successful attempt matters more than covering optional extensions. Defer: Package refactoring, complex repository layout and extra tooling are optional. Keep a working simple notebook.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Connection to the previous lesson.

REFERENCES


## Slide 3 — Connection to the previous lesson

PURPOSE
Connection to the previous lesson

CONNECT
Previous slide: Today’s learning.

EXPLAIN
The models and charts already exist. The remaining task is to make the evidence understandable and runnable from the supplied files.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Why this week’s tools are needed.

REFERENCES


## Slide 4 — Why this week’s tools are needed

PURPOSE
Why this week’s tools are needed

CONNECT
Previous slide: Connection to the previous lesson.

EXPLAIN
A project is ready for handover when its files and written instructions reproduce its results in a fresh session. Today we check that evidence ourselves.

LECTURER CUE
A pump team records temperature to investigate operation. Mining students can relate this to a dewatering pump; petroleum students to a transfer pump. These are teaching examples, not operating limits.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Reproducibility and Dependency.

REFERENCES


## Slide 5 — Reproducibility and Dependency

PURPOSE
Reproducibility and Dependency

CONNECT
Previous slide: Why this week’s tools are needed.

EXPLAIN
Reproducibility: Another person can use the stated data, environment and steps to check the result. Terminology varies; state the operational test.

Dependency: A package your code needs. Record versions actually used, rather than guessing them.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Relative path and README.

REFERENCES


## Slide 6 — Relative path and README

PURPOSE
Relative path and README

CONNECT
Previous slide: Reproducibility and Dependency.

EXPLAIN
Relative path: A location interpreted from the current working folder. It is not always relative to the notebook file itself.

README: The project’s instructions: question, files, data source, environment, run order, results and limitations.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A useful README.

REFERENCES


## Slide 7 — A useful README

PURPOSE
A useful README

CONNECT
Previous slide: Relative path and README.

EXPLAIN
State the engineering question and target unit.

List the supplied data and required software versions.

Give the order for running the notebook from a fresh session.

State limitations and each member’s contribution.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Someone else needs to reproduce the result.

REFERENCES


## Slide 8 — Someone else needs to reproduce the result

PURPOSE
Someone else needs to reproduce the result

CONNECT
Previous slide: A useful README.

EXPLAIN
Which instructions would a new user need?

LECTURER CUE
Ask students to describe what they see before introducing terminology. Generated conceptual teaching illustration.  Source: figs/experiential/ASSET_SOURCES.md.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A reproducible notebook starts fresh.

REFERENCES


## Slide 9 — A reproducible notebook starts fresh

PURPOSE
A reproducible notebook starts fresh

CONNECT
Previous slide: Someone else needs to reproduce the result.

EXPLAIN
The saved outputs must agree with a fresh run in the stated order.

LECTURER CUE
Demonstrate restarting, uploading the issued data, and running all. The same result also depends on data, package versions and any random seeds.
Source: existing course illustration figs/execution_trap.png. These are illustrative examples, not this cohort’s assessed results.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Saved outputs can hide missing steps.

REFERENCES
Source: existing course illustration figs/execution_trap.png. These are illustrative examples, not this cohort’s assessed results.

## Slide 10 — Saved outputs can hide missing steps

PURPOSE
Saved outputs can hide missing steps

CONNECT
Previous slide: A reproducible notebook starts fresh.

EXPLAIN
A notebook can display an old answer after its inputs have changed.

A fresh session begins without the old variables.

Restarting and running all tests whether the stated order creates the result.

LECTURER CUE
Demonstrate a clean run from a fresh session with the actual files. If a variable exists only from an earlier manual cell run, fix the run order.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A path names where a file is found.

REFERENCES


## Slide 11 — A path names where a file is found

PURPOSE
A path names where a file is found

CONNECT
Previous slide: Saved outputs can hide missing steps.

EXPLAIN
A relative path is interpreted from the current working folder.

Package versions describe the software used to run the code.

The README must give both run instructions and data-access instructions.

LECTURER CUE
Explain every dependency and test a relative path. Include data-access instructions if the data cannot be redistributed.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Read the path example.

REFERENCES


## Slide 12 — Read the path example

PURPOSE
Read the path example

CONNECT
Previous slide: A path names where a file is found.

EXPLAIN
Path and cwd: Path is a tool imported from Python’s pathlib module. Path.cwd() returns the folder where Python is currently running.

name: The .name property gives the last folder component as text. It depends on your runtime. A different folder name is expected on another computer.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Worked example.

REFERENCES


## Slide 13 — Project handover in Python

PURPOSE
Project handover in Python

CONNECT
Previous slide: Read the path example.

EXPLAIN
Read the code in this order:
from pathlib import Path
print(Path.cwd().name)
# The name depends on the folder where Python is running.

import loads a library. from selects a tool from it.

print displays a value below the cell.

Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER CUE
Demonstrate a clean run from a fresh session with the actual files. If a variable exists only from an earlier manual cell run, fix the run order. Explain every dependency and test a relative path. Include data-access instructions if the data cannot be redistributed. Model actionable feedback: “Step 2 names data.csv, but the supplied file is readings.csv; please make them match.”

Complete practice code:
from pathlib import Path
print(Path.cwd().name)
# The name depends on the folder where Python is running.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Expected output.

REFERENCES


## Slide 14 — Project handover results

PURPOSE
Project handover results

CONNECT
Previous slide: Project handover in Python.

EXPLAIN
Your current working folder name; it is environment-dependent.

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Tell another person what the project needs.

REFERENCES


## Slide 15 — Tell another person what the project needs

PURPOSE
Tell another person what the project needs

CONNECT
Previous slide: Project handover results.

EXPLAIN
requirements.txt and versions: This text file lists required Python packages and their versions. Record the versions used in the working environment; test them with the supplied run instructions.

Data source, permission and seed: Name the data source and any licence or permission for reuse. Record random seeds used in modelling. A seed supports repeatability; it does not repair data leakage.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Run checks and contribution evidence.

REFERENCES


## Slide 16 — Run checks and contribution evidence

PURPOSE
Run checks and contribution evidence

CONNECT
Previous slide: Tell another person what the project needs.

EXPLAIN
Independent run check: Restart the session and follow your written instructions without relying on earlier variables. Record the first failure and its repair.

Contribution evidence: A record of each person’s work, tied to files, commits or explanations. It does not require making a private repository public.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Useful feedback identifies an exact repair.

REFERENCES


## Slide 17 — Useful feedback identifies an exact repair

PURPOSE
Useful feedback identifies an exact repair

CONNECT
Previous slide: Run checks and contribution evidence.

EXPLAIN
Vague feedback: "It does not work."

Useful feedback: "Step 2 names data.csv, but the supplied file is readings.csv."

The repair is to make the instructions and actual filename agree.

LECTURER CUE
Model actionable feedback: “Step 2 names data.csv, but the supplied file is readings.csv; please make them match.”

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Revision example and answer.

REFERENCES


## Slide 18 — Revision example and answer

PURPOSE
Revision example and answer

CONNECT
Previous slide: Useful feedback identifies an exact repair.

EXPLAIN
Check: restart the notebook runtime and follow your README exactly, without using remembered variables.

If Step 2 names data.csv but the file is readings.csv, correct the filename in the instructions. Run again from the beginning and record the successful result.

LECTURER CUE
Give silent thinking time, then let pairs discuss. Rotate who types. This is practice, not a graded quiz. Expected response: Revise that step and repeat. A claim that the notebook runs is supported by a fresh run, not by saved outputs alone.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Preparing for the assignment.

REFERENCES


## Slide 19 — Preparing for the assignment

PURPOSE
Preparing for the assignment

CONNECT
Previous slide: Revision example and answer.

EXPLAIN
No new weekly assignment.

Continue the official project deliverables and Week 13 quiz.

Rehearse offline TEST2 saving and the published function interfaces before Week 14.

Do not add an extra upload.

LECTURER CUE
No new weekly assignment. Continue the official project deliverables and Week 13 quiz. Rehearse offline TEST2 saving and the published function interfaces before Week 14. Do not add an extra upload.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A reproducible handover.

REFERENCES


## Slide 20 — A reproducible handover

PURPOSE
A reproducible handover

CONNECT
Previous slide: Preparing for the assignment.

EXPLAIN
An absolute path from your own computer will usually fail elsewhere.

A relative path starts from the current working folder.

Record dependencies and actual versions, and fix randomness where appropriate; identical results across all machines are not guaranteed by a seed alone.

Captions should state a supported finding and its scope.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A reproducible handover continued.

REFERENCES


## Slide 21 — A reproducible handover continued

PURPOSE
A reproducible handover continued

CONNECT
Previous slide: A reproducible handover.

EXPLAIN
Remove conflicting cell assignments and verify a fresh run before submission.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Project preparation.

REFERENCES


## Slide 22 — Project preparation

PURPOSE
Project preparation

CONNECT
Previous slide: A reproducible handover continued.

EXPLAIN
Use the published machine learning project brief.

Build the evidence gradually in your project notebook.

Keep raw data, labelled charts, run instructions and individual contributions.

Published deadline: 18 Dec 2026, 08:00 Kampala

LECTURER CUE
Explain the released brief now. Confirm its grading-release checks before assigning it. Avoid treating weekly practice as a substitute for the project evidence. The project brief remains authoritative.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Week 13 quiz.

REFERENCES


## Slide 23 — Week 13 quiz

PURPOSE
Week 13 quiz

CONNECT
Previous slide: Project preparation.

EXPLAIN
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

The lecturer will confirm the exact closing time.

LECTURER CUE
Activate the matching open_W13_CML3113 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Before you leave.

REFERENCES


## Slide 24 — Revision and submission checklist

PURPOSE
Revision and submission checklist

CONNECT
Previous slide: Week 13 quiz.

EXPLAIN
Another learner can follow your README and reproduce the stated result.

Save your work and check the required submission files.

LECTURER CUE
Ask every learner for an individual response. Record one misconception to revisit at the start of the next class. If a deadline changed, announce the exact Kampala date and update the source registry before rebuilding slides.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Optional revision video.

REFERENCES


## Slide 25 — Optional revision video

PURPOSE
Optional revision video

CONNECT
Previous slide: Revision and submission checklist.

EXPLAIN
For revision after class.

CodeWithChris
GitHub Tutorial for Beginners (2025)

00:00–02:10, then 03:35–06:08 (4 min 43 sec total)

Listening question: Why keep history, and what is a repository?

LECTURER CUE
Title, channel, 19:53 runtime and chapter boundaries checked on the video page on 15 September 2026. Desktop installation is optional. The originally shared t=167 link starts at installation.
After viewing: Explain the difference between saving a file and recording a commit. Then make one browser-based commit.
Preview before class and stop after the selected short excerpt. If playback fails, teach the worked example. Video is optional. Source: https://www.youtube.com/watch?v=v5gnvDUWqFM

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
independent revision and the issued task.

REFERENCES
