# CML3113 Week 13

## Slide 1: Making the project understandable and runnable

Making the project understandable and runnable
Explanation to give
The handover should reproduce the result using the files and instructions alone. Saved output is insufficient evidence.

Worked illustration / lecturer answer
Restart, load the stated data and follow the README literally. A mismatch between a documented filename and the actual file is a handover defect to fix.

Misconception to address
Use this as an orientation to the lesson. Terms and syntax will be unpacked on their own slides; students do not need to know them in advance.

On this slide
Mining and Petroleum Engineering

## Slide 2: Today’s learning

Today’s learning
Explanation to give
The handover should reproduce the result using the files and instructions alone. Saved output is insufficient evidence.

Worked illustration / lecturer answer
Restart, load the stated data and follow the README literally. A mismatch between a documented filename and the actual file is a handover defect to fix.

Misconception to address
At the end, check the specific outcome shown here using a small previously demonstrated example. A completed file without an explanation is not evidence of understanding.

On this slide
Run the project from a fresh session.

Repair unclear run instructions using a fresh run.

## Slide 3: Connection to the previous lesson

Connection to the previous lesson
Explanation to give
The handover should reproduce the result using the files and instructions alone. Saved output is insufficient evidence.

Worked illustration / lecturer answer
Restart, load the stated data and follow the README literally. A mismatch between a documented filename and the actual file is a handover defect to fix.

Misconception to address
Connect this to the previous result named on this slide. Demonstrate the first step again if necessary; there is no requirement for partner work before the explanation.

On this slide
The models and charts already exist. The remaining task is to make the evidence understandable and runnable from the supplied files.

## Slide 4: The continuing pandas workflow

This is revision, not a new test requirement. Lists can name columns or hold returned predictions, but students do not need to rebuild table operations with manual CSV loops. Existing function signatures, marks and allowed-resource rules stay unchanged.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 5: Relative data paths and saved outputs

Explain data/raw as folders inside the project. A path starting with a private machine username will fail elsewhere. Keep raw data separate and never overwrite it with cleaned data.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 6: Why this week’s tools are needed

Why this week’s tools are needed
Explanation to give
The handover should reproduce the result using the files and instructions alone. Saved output is insufficient evidence.

Worked illustration / lecturer answer
Restart, load the stated data and follow the README literally. A mismatch between a documented filename and the actual file is a handover defect to fix.

Misconception to address
Connect this to the previous result named on this slide. Demonstrate the first step again if necessary; there is no requirement for partner work before the explanation.

On this slide
A project is ready for handover when its files and written instructions reproduce its results in a fresh session. Check each claim against the results in your notebook.

## Slide 7: Reproducibility and Dependency

Reproducibility and Dependency
Explanation to give
A reproducible handover gives another person enough files and instructions to obtain the reported result from a fresh environment. Saved outputs can survive even when the code no longer produces them.

Worked illustration / lecturer answer
Restart, load the documented data and run from the first cell. If a later cell relies on a deleted variable, the clean run reveals the missing step. Record the required Python libraries and versions.

Misconception to address
Restarting the runtime clears variables; it does not necessarily restore deleted data files. Re-upload or locate the documented inputs before the fresh run.

On this slide
Reproducibility: Another person can use the stated data, environment and steps to check the result. Terminology varies; state the operational test_data.
Dependency: A package your code needs. Record versions actually used, rather than guessing them.

## Slide 8: Relative path and README

Relative path and README
Explanation to give
A path identifies where a file is found. A relative path starts from the current working directory. Explain each folder component and the final practice_filename.

Worked illustration / lecturer answer
data/readings.csv means the readings.csv file inside a data folder under the current working directory. A path from your own Downloads folder will usually fail on another person's machine.

Misconception to address
The working directory is not automatically the notebook's own folder in every tool. Check it and organise the project rather than hard-coding a personal absolute path.

On this slide
Relative path: A location interpreted from the current working folder. It is not always relative to the notebook file itself.
README: The project’s instructions: question, files, data source, environment, run order, results and limitations.

## Slide 9: A useful README

A useful README
Explanation to give
Treat the README as instructions for someone opening the project for the first time. Name the files, setup requirements, entry notebook and exact order needed to reproduce the result.

Worked illustration / lecturer answer
Replace “run the analysis” with “Open analysis.ipynb, place readings.csv in data/, restart the runtime and run all cells.” A useful repair comment names the failed step and the corrected practice_filename.

Misconception to address
A repository URL proves a location exists, not that the work runs or was submitted. Contribution claims should point to specific work, not only a count of commits.

On this slide
State the engineering question and target unit.

List the supplied data and required software versions.

Give the order for running the notebook from a fresh session.

State limitations and each member’s contribution.

## Slide 10: Someone else needs to reproduce the result

Someone else needs to reproduce the result
Explanation to give
Describe a handover as a reproducibility test carried out with only the delivered files and written directions. The person checking it should not need your memory of previous actions.

Worked illustration / lecturer answer
Close the runtime, start fresh and follow the README literally. If it names data.csv while the folder contains readings.csv, repair the instructions and repeat the check.

Misconception to address
A screenshot of a successful old output is not proof that today's package works from a clean prediction_start_time.

On this slide
Which instructions would a new user need?

## Slide 11: A reproducible notebook starts fresh

A reproducible notebook starts fresh
Explanation to give
A reproducible handover gives another person enough files and instructions to obtain the reported result from a fresh environment. Saved outputs can survive even when the code no longer produces them.

Worked illustration / lecturer answer
Restart, load the documented data and run from the first cell. If a later cell relies on a deleted variable, the clean run reveals the missing step. Record the required Python libraries and versions.

Misconception to address
Restarting the runtime clears variables; it does not necessarily restore deleted data files. Re-upload or locate the documented inputs before the fresh run.

On this slide
The saved outputs must agree with a fresh run in the stated order.

## Slide 12: Saved outputs can hide missing steps

Saved outputs can hide missing steps
Explanation to give
A reproducible handover gives another person enough files and instructions to obtain the reported result from a fresh environment. Saved outputs can survive even when the code no longer produces them.

Worked illustration / lecturer answer
Restart, load the documented data and run from the first cell. If a later cell relies on a deleted variable, the clean run reveals the missing step. Record the required Python libraries and versions.

Misconception to address
Restarting the runtime clears variables; it does not necessarily restore deleted data files. Re-upload or locate the documented inputs before the fresh run.

On this slide
A notebook can display an old answer after its inputs have changed.

A fresh session begins without the old variables.

Restarting and running all tests whether the stated order creates the result.

## Slide 13: A path names where a file is found

A path names where a file is found
Explanation to give
A path identifies where a file is found. A relative path starts from the current working directory. Explain each folder component and the final practice_filename.

Worked illustration / lecturer answer
data/readings.csv means the readings.csv file inside a data folder under the current working directory. A path from your own Downloads folder will usually fail on another person's machine.

Misconception to address
The working directory is not automatically the notebook's own folder in every tool. Check it and organise the project rather than hard-coding a personal absolute path.

On this slide
A relative path is interpreted from the current working folder.

Package versions describe the software used to run the code.

The README must give both run instructions and data-access instructions.

## Slide 14: Read the path example

Read the path example
Explanation to give
A path identifies where a file is found. A relative path starts from the current working directory. Explain each folder component and the final practice_filename.

Worked illustration / lecturer answer
data/readings.csv means the readings.csv file inside a data folder under the current working directory. A path from your own Downloads folder will usually fail on another person's machine.

Misconception to address
The working directory is not automatically the notebook's own folder in every tool. Check it and organise the project rather than hard-coding a personal absolute path.

On this slide
Path and cwd: Path is a tool imported from Python’s pathlib module. Path.cwd() returns the folder where Python is currently running.
name: The .name property gives the last folder component as text. It depends on your runtime. A different folder name is expected on another computer.

## Slide 15: Tell another person what the project needs

Tell another person what the project needs
Explanation to give
Treat the README as instructions for someone opening the project for the first time. Name the files, setup requirements, entry notebook and exact order needed to reproduce the result.

Worked illustration / lecturer answer
Replace “run the analysis” with “Open analysis.ipynb, place readings.csv in data/, restart the runtime and run all cells.” A useful repair comment names the failed step and the corrected practice_filename.

Misconception to address
A repository URL proves a location exists, not that the work runs or was submitted. Contribution claims should point to specific work, not only a count of commits.

On this slide
requirements.txt and versions: This text file lists required Python packages and their versions. Record the versions used in the working environment; test them with the supplied run instructions.
Data source, permission and seed: Name the data source and any licence or permission for reuse. Record random seeds used in modelling. A seed supports repeatability; it does not repair data leakage.

## Slide 16: Run checks and contribution evidence

Run checks and contribution evidence
Explanation to give
Treat the README as instructions for someone opening the project for the first time. Name the files, setup requirements, entry notebook and exact order needed to reproduce the result.

Worked illustration / lecturer answer
Replace “run the analysis” with “Open analysis.ipynb, place readings.csv in data/, restart the runtime and run all cells.” A useful repair comment names the failed step and the corrected practice_filename.

Misconception to address
A repository URL proves a location exists, not that the work runs or was submitted. Contribution claims should point to specific work, not only a count of commits.

On this slide
Independent run check: Restart the session and follow your written instructions without relying on earlier variables. Record the first failure and its repair.
Contribution evidence: A record of each person’s work, tied to files, commits or explanations. It does not require making a private repository public.

## Slide 17: Useful feedback identifies an exact repair

Useful feedback identifies an exact repair
Explanation to give
Treat the README as instructions for someone opening the project for the first time. Name the files, setup requirements, entry notebook and exact order needed to reproduce the result.

Worked illustration / lecturer answer
Replace “run the analysis” with “Open analysis.ipynb, place readings.csv in data/, restart the runtime and run all cells.” A useful repair comment names the failed step and the corrected practice_filename.

Misconception to address
A repository URL proves a location exists, not that the work runs or was submitted. Contribution claims should point to specific work, not only a count of commits.

On this slide
Vague feedback: "It does not work."

Useful feedback: "Step 2 names data.csv, but the supplied file is readings.csv."

The repair is to make the instructions and actual filename agree.

## Slide 18: Revision example and answer

Revision example and answer
Explanation to give
Use the displayed example as a short individual revision question, then explain the reasoning behind its answer.

Worked illustration / lecturer answer
Check: restart the notebook runtime and follow your README exactly, without using remembered variables.

If Step 2 names data.csv but the file is readings.csv, correct the filename in the instructions. Run again from the beginning and record the successful result.

Misconception to address
Trace the operation that changes the value rather than accepting a memorised output. For notebook-state examples, specify which cell is repeated and whether the initialisation ran again.

## Slide 19: Preparing for the assignment

Preparing for the assignment
Explanation to give
Week 13 adds no new weekly assignment notebook. Use the time to make the existing project reproducible and prepare for the offline test_data.

Worked illustration / lecturer answer
Open the project README, restart and follow its steps. Then rehearse locating and reopening the complete test notebook on the prepared offline computer.

Misconception to address
Quiz 13 is a separate activity when activated. Do not invent an A13 upload or require students to submit an extra weekly report.

On this slide
No new weekly assignment.

Continue the official project deliverables and Week 13 quiz.

Rehearse Colab Test 2 saving and submission and the published function interfaces before Week 14.

Do not add an extra upload.

## Slide 20: A reproducible handover

A reproducible handover
Explanation to give
A reproducible handover gives another person enough files and instructions to obtain the reported result from a fresh environment. Saved outputs can survive even when the code no longer produces them.

Worked illustration / lecturer answer
Restart, load the documented data and run from the first cell. If a later cell relies on a deleted variable, the clean run reveals the missing step. Record the required Python libraries and versions.

Misconception to address
Restarting the runtime clears variables; it does not necessarily restore deleted data files. Re-upload or locate the documented inputs before the fresh run.

On this slide
An absolute path from your own computer will usually fail elsewhere.

A relative path starts from the current working folder.

Record dependencies and actual versions, and fix randomness where appropriate; identical results across all machines are not guaranteed by a seed alone.

Captions should state a supported finding and its scope.

## Slide 21: A reproducible handover continued

A reproducible handover continued
Explanation to give
A reproducible handover gives another person enough files and instructions to obtain the reported result from a fresh environment. Saved outputs can survive even when the code no longer produces them.

Worked illustration / lecturer answer
Restart, load the documented data and run from the first cell. If a later cell relies on a deleted variable, the clean run reveals the missing step. Record the required Python libraries and versions.

Misconception to address
Restarting the runtime clears variables; it does not necessarily restore deleted data files. Re-upload or locate the documented inputs before the fresh run.

On this slide
Remove conflicting cell assignments and verify a fresh run before submission.

## Slide 22: Project preparation

Project preparation
Explanation to give
Make contribution evidence specific enough to check. A seed records the starting state of random choices; a contribution log records who produced and explained which work.

Worked illustration / lecturer answer
Name a file, function or chart and the decision behind it. Match that entry to meaningful repository history. Disclose AI assistance according to the assessment policy.

Misconception to address
Many commits do not necessarily mean substantial work, and a seed does not establish accuracy. Both are supporting evidence, not replacements for the analysis.

On this slide
Use the published machine learning project brief.

Build the evidence gradually in your project notebook.

Keep raw data, labelled charts, run instructions and individual contributions.

Published deadline: 18 Dec 2026, 08:00 Kampala

## Slide 23: Week 13 quiz

Week 13 quiz
Explanation to give
This is the CML3113 Week 1 quiz. The student link opens the response form; it does not activate its window. In Quiz Controls use open_W1_CML3113 when ready and read the logged closing time.

Worked illustration / lecturer answer
Explain the distinction between the expected answering time and availability: five minutes of questions can still be available for 24 hours after activation. Enter the learner’s own Student Registration Number and use the registered Google account.

Misconception to address
Read the exact live cutoff before announcing it. Do not promise a new attempt to somebody who already submitted. Quiz catch-up and assignment uploads are separate forms.

On this slide
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

Check the announced quiz closing time.

## Slide 24: Revision and submission checklist

Revision and submission checklist
Explanation to give
The handover should reproduce the result using the files and instructions alone. Saved output is insufficient evidence.

Worked illustration / lecturer answer
Restart, load the stated data and follow the README literally. A mismatch between a documented filename and the actual file is a handover defect to fix.

Misconception to address
Close by identifying the actual saved file and its correct submission route. Read the live deadline. For current weekly notebook tasks, students upload their own work, not the practice notebook, ZIP or grading files.

On this slide
Another learner can follow your README and reproduce the stated result.

Save your work and check the required submission files.

## Slide 25: Optional revision video

Optional revision video
Explanation to give
Give the viewing question before playing the excerpt: Why keep history, and what is a repository?

Worked illustration / lecturer answer
Use the adjacent worked example as the explanation if the video cannot load. Pause after the relevant example and connect its terms to the names and units already used in this lesson. Preview the displayed link and excerpt before class.

Misconception to address
The video is supporting revision, not a replacement for defining the symbols or a requirement to watch a full tutorial during limited class time.

On this slide
For revision after class.

CodeWithChris
GitHub Tutorial for Beginners (2025)

00:00–02:10, then 03:35–06:08 (4 min 43 sec total)

Listening question: Why keep history, and what is a repository?

Reference / existing resource
https://www.youtube.com/watch?v=v5gnvDUWqFM