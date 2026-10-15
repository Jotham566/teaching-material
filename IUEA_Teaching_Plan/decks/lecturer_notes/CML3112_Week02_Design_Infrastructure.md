# CML3112 Week02 Design Infrastructure

Lecturer companion. The same explanations are embedded in the PowerPoint speaker notes. Open Presenter View, or expand the Notes pane when preparing.

## Slide 1 — Where the work

Where the work
CML3112, Week 2, slide 1

Explanation to give
Today the learner creates, runs, saves and submits a notebook. Separate those actions so a successful run is not mistaken for a saved or submitted file.

Worked illustration / lecturer answer
The runtime remembers readings = 12. One update adding 5 gives 17; repeating only that update gives 22. A fresh run starts at 12 again.

Misconception to address
Use this as an orientation to the lesson. Terms and syntax will be unpacked on their own slides; students do not need to know them in advance.

Continue to
By the end of today you can…

## Slide 2 — By the end of today you can…

By the end of today you can…
CML3112, Week 2, slide 2

Explanation to give
Today the learner creates, runs, saves and submits a notebook. Separate those actions so a successful run is not mistaken for a saved or submitted file.

Worked illustration / lecturer answer
The runtime remembers readings = 12. One update adding 5 gives 17; repeating only that update gives 22. A fresh run starts at 12 again.

Misconception to address
Use the outcomes listed on this slide to check understanding through the small examples, rather than asking only whether everybody understands.

Continue to
How today runs

## Slide 3 — How today runs

How today runs
CML3112, Week 2, slide 3

Explanation to give
Orient students to this particular lesson: explain what they will see demonstrated, which file they will use and what they must retain for revision. Keep the transition short enough to preserve explanation time.

Worked illustration / lecturer answer
Open the next worked example on the projector and name its input and intended result. Demonstrate it yourself before asking students to interpret a result. Use remaining summary and glossary pages for independent revision.

Misconception to address
The historical slide's timed group activity is not a requirement to stop for partner work. Use a lecturer-led walkthrough in the current limited class time.

Continue to
Previous lesson and today’s topics

## Slide 4 — Previous lesson and today’s topics

Previous lesson and today’s topics
CML3112, Week 2, slide 4

Explanation to give
Today the learner creates, runs, saves and submits a notebook. Separate those actions so a successful run is not mistaken for a saved or submitted file.

Worked illustration / lecturer answer
The runtime remembers readings = 12. One update adding 5 gives 17; repeating only that update gives 22. A fresh run starts at 12 again.

Misconception to address
Use the outcomes listed on this slide to check understanding through the small examples, rather than asking only whether everybody understands.

Continue to
Two minutes: what stuck from Week 1?

## Slide 5 — Two minutes: what stuck from Week 1?

Two minutes: what stuck from Week 1?
CML3112, Week 2, slide 5

Explanation to give
Recall features as information known beforehand and target as the answer to predict. Days until servicing is a quantity, so regression. A fixed verified formula may make ML unnecessary. Use the following answer slide to explain why, without requiring partner discussion.

Worked illustration / lecturer answer
Point to the particular code cell or answer on this slide while explaining the reasoning.

Misconception to address
The current assignment guide and live form take precedence over historical logistics printed in this deck.

Continue to
How did you do?

## Slide 6 — How did you do?

How did you do?
CML3112, Week 2, slide 6

Explanation to give
For each answer on this slide, identify the deciding feature of the question: timing of the input, kind of target, run order or operation requested.

Worked illustration / lecturer answer
The input columns, and the value?
The columns you were given are the FEATURES. The value you predicted is the TARGET. One row with both is one EXAMPLE.
Days until servicing?
Regression — the answer is a number with a unit. If it were 'service due or not' it would be classification.
One of the four limits?
Missing data, weak patterns, a better physical model or changed operating conditions.

Misconception to address
If a student gives a different engineering example, check its reasoning and timing rather than requiring identical wording to the printed example.

Continue to
Four questions, four tools

## Slide 7 — Four questions, four tools

Four questions, four tools
CML3112, Week 2, slide 7

Explanation to give
Give each tool one job: Python expresses instructions, a notebook combines code and explanations, Colab runs the notebook in a browser, and Git/GitHub records and hosts project versions.

Worked illustration / lecturer answer
A saved .ipynb can move between notebook environments. Moving the document does not necessarily move the running session or its uploaded CSV.

Misconception to address
Do not imply students must master all tools at once or that no other tool can ever be needed. Demonstrate the browser workflow used for this assessment.

Continue to
The four questions

## Slide 8 — The four questions

The four questions
CML3112, Week 2, slide 8

Explanation to give
Give each tool one job: Python expresses instructions, a notebook combines code and explanations, Colab runs the notebook in a browser, and Git/GitHub records and hosts project versions.

Worked illustration / lecturer answer
A saved .ipynb can move between notebook environments. Moving the document does not necessarily move the running session or its uploaded CSV.

Misconception to address
Do not imply students must master all tools at once or that no other tool can ever be needed. Demonstrate the browser workflow used for this assessment.

Continue to
Google Colab

## Slide 9 — Google Colab

Google Colab
CML3112, Week 2, slide 9

Explanation to give
Demonstrate the file-opening path slowly: sign in, open Colab, choose the notebook upload option and select the extracted .ipynb file. Connecting starts a remote Python runtime.

Worked illustration / lecturer answer
Open proof_of_life.ipynb, identify a code cell and run it with Shift+Enter. Show the result underneath. Upload its CSV separately through the runtime Files panel before reading it.

Misconception to address
Saving the notebook to Drive and uploading data to a temporary runtime are separate actions. If the runtime is replaced, the data file may need uploading again.

Continue to
Your first notebook

## Slide 10 — Your first notebook

Your first notebook
CML3112, Week 2, slide 10

Explanation to give
Demonstrate the file-opening path slowly: sign in, open Colab, choose the notebook upload option and select the extracted .ipynb file. Connecting starts a remote Python runtime.

Worked illustration / lecturer answer
Open proof_of_life.ipynb, identify a code cell and run it with Shift+Enter. Show the result underneath. Upload its CSV separately through the runtime Files panel before reading it.

Misconception to address
Saving the notebook to Drive and uploading data to a temporary runtime are separate actions. If the runtime is replaced, the data file may need uploading again.

Continue to
Three cells

## Slide 11 — Three cells

Three cells
CML3112, Week 2, slide 11

Explanation to give
Read the three cells separately. Cell 1 prints the cohort greeting and 4. Cell 2 assigns readings = 12 and the f-string inserts 12 into the text. Repeating only cell 3 gives 17,22,27. Repeating cells 2 and 3 resets to 12 and ends at 17. Braces inside an f-string request the current value; they are not printed literally.

Worked illustration / lecturer answer
Point to the particular code cell or answer on this slide while explaining the reasoning.

Misconception to address
The current assignment guide and live form take precedence over historical logistics printed in this deck.

Continue to
The three things that go wrong in the first ten minutes

## Slide 12 — The three things that go wrong in the first ten minutes

The three things that go wrong in the first ten minutes
CML3112, Week 2, slide 12

Explanation to give
Teach a diagnosis sequence: read the final error line, locate the indicated instruction, compare the expected input with what actually exists, and fix the first cause. Explain the error type rather than treating all red output alike.

Worked illustration / lecturer answer
NameError often means a misspelled or not-yet-created name. FileNotFoundError means the named path was not found. TypeError can result from adding text and a number. A wrong answer can occur with no exception at all.

Misconception to address
The highlighted line is where Python noticed a problem, not always its original cause. Do not install an unrelated package when the exercise deliberately names a nonexistent module.

Continue to
Markdown cell

## Slide 13 — Markdown cell

Markdown cell
CML3112, Week 2, slide 13

Explanation to give
Explain the notebook as a document containing executable instructions and readable explanations. The code cell holds Python; the text cell explains the reasoning. Output sits below the code that produced it.

Worked illustration / lecturer answer
In one code cell, print(2 + 2) displays 4 below it. In a text cell, write “I added two counts.” Running that text cell formats the explanation rather than calculating a result.

Misconception to address
A cell's location is document order, while its execution counter reflects when it last ran. Saved output may come from an earlier version of the code.

Continue to
Thirty seconds: check you are with me

## Slide 14 — Thirty seconds: check you are with me

Thirty seconds: check you are with me
CML3112, Week 2, slide 14

Explanation to give
Enter creates a new line; Shift+Enter executes. hello appears below its code cell. Values 17 and 27 can both result from the shown update if it has run different numbers of times. The difference exposes shared runtime state, not different arithmetic.

Worked illustration / lecturer answer
Point to the particular code cell or answer on this slide while explaining the reasoning.

Misconception to address
The current assignment guide and live form take precedence over historical logistics printed in this deck.

Continue to
How did you do?

## Slide 15 — How did you do?

How did you do?
CML3112, Week 2, slide 15

Explanation to give
For each answer on this slide, identify the deciding feature of the question: timing of the input, kind of target, run order or operation requested.

Worked illustration / lecturer answer
Enter did nothing?
Enter adds a new line inside a cell. Shift + Enter runs the cell.
Where does 'hello' appear?
The output appears directly below the cell that produced it.
27 versus 17 — who is wrong?
Neither. They have run the cell a different number of times. That is not a difference of opinion, it is a property of how notebooks work — and it is the subject of the execution-order block.

Misconception to address
If a student gives a different engineering example, check its reasoning and timing rather than requiring identical wording to the printed example.

Continue to
Notebook cells and execution

## Slide 16 — Notebook cells and execution

Notebook cells and execution
CML3112, Week 2, slide 16

Explanation to give
This divider introduces The anatomy of a notebook. Explain the notebook as a document containing executable instructions and readable explanations. The code cell holds Python; the text cell explains the reasoning. Output sits below the code that produced it.

Worked illustration / lecturer answer
In one code cell, print(2 + 2) displays 4 below it. In a text cell, write “I added two counts.” Running that text cell formats the explanation rather than calculating a result.

Misconception to address
Keep this transition brief. The detailed demonstration follows; do not add another activity before students have seen it.

Continue to
The anatomy of a notebook

## Slide 17 — The anatomy of a notebook

The anatomy of a notebook
CML3112, Week 2, slide 17

Explanation to give
Explain the notebook as a document containing executable instructions and readable explanations. The code cell holds Python; the text cell explains the reasoning. Output sits below the code that produced it.

Worked illustration / lecturer answer
In one code cell, print(2 + 2) displays 4 below it. In a text cell, write “I added two counts.” Running that text cell formats the explanation rather than calculating a result.

Misconception to address
A cell's location is document order, while its execution counter reflects when it last ran. Saved output may come from an earlier version of the code.

Continue to
Cell, kernel, and the execution counter

## Slide 18 — Cell, kernel, and the execution counter

Cell, kernel, and the execution counter
CML3112, Week 2, slide 18

Explanation to give
Explain the notebook as a document containing executable instructions and readable explanations. The code cell holds Python; the text cell explains the reasoning. Output sits below the code that produced it.

Worked illustration / lecturer answer
In one code cell, print(2 + 2) displays 4 below it. In a text cell, write “I added two counts.” Running that text cell formats the explanation rather than calculating a result.

Misconception to address
A cell's location is document order, while its execution counter reflects when it last ran. Saved output may come from an earlier version of the code.

Continue to
The trap, and the habit that saves you

## Slide 19 — The trap, and the habit that saves you

The trap, and the habit that saves you
CML3112, Week 2, slide 19

Explanation to give
Describe the runtime as a temporary shared workspace containing names and their current values. All code cells use that same workspace. Running a cell updates it; merely editing a cell does not.

Worked illustration / lecturer answer
Run readings = 12 once. Running readings = readings + 5 gives 17, then 22, then 27 on successive executions. Restart and run from the top resets to 12 and ends at 17.

Misconception to address
If the initialisation and update are in one cell, running the whole cell repeatedly gives 17 each time. Put them in separate cells when demonstrating repeated updates.

Continue to
The same cell, run three times

## Slide 20 — The same cell, run three times

The same cell, run three times
CML3112, Week 2, slide 20

Explanation to give
Describe the runtime as a temporary shared workspace containing names and their current values. All code cells use that same workspace. Running a cell updates it; merely editing a cell does not.

Worked illustration / lecturer answer
Run readings = 12 once. Running readings = readings + 5 gives 17, then 22, then 27 on successive executions. Restart and run from the top resets to 12 and ends at 17.

Misconception to address
If the initialisation and update are in one cell, running the whole cell repeatedly gives 17 each time. Put them in separate cells when demonstrating repeated updates.

Continue to
Can you answer these?

## Slide 21 — Can you answer these?

Can you answer these?
CML3112, Week 2, slide 21

Explanation to give
Counters [4],[1],[5],[2] show nonsequential execution, but do not alone prove an incorrect answer. Restart and run in the written order to check. Failure after a restart may reveal a stale variable, missing input file or missing setup; diagnose the actual first exception.

Worked illustration / lecturer answer
Point to the particular code cell or answer on this slide while explaining the reasoning.

Misconception to address
The current assignment guide and live form take precedence over historical logistics printed in this deck.

Continue to
How did you do?

## Slide 22 — How did you do?

How did you do?
CML3112, Week 2, slide 22

Explanation to give
For each answer on this slide, identify the deciding feature of the question: timing of the input, kind of target, run order or operation requested.

Worked illustration / lecturer answer
Counters [4], [1], [5], [2]?
They were run out of order, so the kernel's memory does not match what the notebook looks like. Do not trust the final answer until you have restarted and run all.
It fails after restarting?
Cell 6 may need a value from an earlier cell, a deleted cell or a cell run out of order. Restart and run all cells to locate the first failure.
Why restart rather than re-run one cell?
Because re-running one cell keeps everything else the kernel is holding, including things that no longer exist anywhere in your code. Only a restart proves the notebook can produce its results from nothing but itself — which is what reproducibility means.

Misconception to address
If a student gives a different engineering example, check its reasoning and timing rather than requiring identical wording to the printed example.

Continue to
Diagnosing a notebook from its counters

## Slide 23 — Diagnosing a notebook from its counters

Diagnosing a notebook from its counters
CML3112, Week 2, slide 23

Explanation to give
Counters [2],[7],[3] reveal execution order, not a complete history. A blank counter usually means a cell has not executed in the current session or its execution information was cleared. It does not establish that every later result is wrong. Restart, load the required data and run all to test the dependency chain.

Worked illustration / lecturer answer
Point to the particular code cell or answer on this slide while explaining the reasoning.

Misconception to address
The current assignment guide and live form take precedence over historical logistics printed in this deck.

Continue to
Break

## Slide 24 — Break

Break
CML3112, Week 2, slide 24

Explanation to give
Announce the actual return time based on the clock now, rather than leaving “ten minutes” ambiguous.

Worked illustration / lecturer answer
Save the current notebook before the break. On return, continue at the next topic named in the deck.

Misconception to address
No new assessment or group task is assigned by this divider.

Continue to
What version control gives you

## Slide 25 — What version control gives you

What version control gives you
CML3112, Week 2, slide 25

Explanation to give
Distinguish saving the working file, recording a version and submitting an assignment. Git records chosen changes in commits; GitHub hosts a repository. A commit message should describe the change.

Worked illustration / lecturer answer
For today's browser route, download the notebook from Colab, create a private GitHub repository, upload the notebook and CSV, commit them, then edit and commit your own README. The A2 form receives the notebook and README plus the repository URL.

Misconception to address
git commands belong in a terminal, not a Python cell. The web interface handles the remote commit directly. A repository upload does not replace the assignment form.

Continue to
Tracking changes with Git

## Slide 26 — Tracking changes with Git

Tracking changes with Git
CML3112, Week 2, slide 26

Explanation to give
Distinguish saving the working file, recording a version and submitting an assignment. Git records chosen changes in commits; GitHub hosts a repository. A commit message should describe the change.

Worked illustration / lecturer answer
For today's browser route, download the notebook from Colab, create a private GitHub repository, upload the notebook and CSV, commit them, then edit and commit your own README. The A2 form receives the notebook and README plus the repository URL.

Misconception to address
git commands belong in a terminal, not a Python cell. The web interface handles the remote commit directly. A repository upload does not replace the assignment form.

Continue to
The four places your work can be

## Slide 27 — The four places your work can be

The four places your work can be
CML3112, Week 2, slide 27

Explanation to give
Distinguish saving the working file, recording a version and submitting an assignment. Git records chosen changes in commits; GitHub hosts a repository. A commit message should describe the change.

Worked illustration / lecturer answer
For today's browser route, download the notebook from Colab, create a private GitHub repository, upload the notebook and CSV, commit them, then edit and commit your own README. The A2 form receives the notebook and README plus the repository URL.

Misconception to address
git commands belong in a terminal, not a Python cell. The web interface handles the remote commit directly. A repository upload does not replace the assignment form.

Continue to
Repository, commit, and push

## Slide 28 — Repository, commit, and push

Repository, commit, and push
CML3112, Week 2, slide 28

Explanation to give
Distinguish saving the working file, recording a version and submitting an assignment. Git records chosen changes in commits; GitHub hosts a repository. A commit message should describe the change.

Worked illustration / lecturer answer
For today's browser route, download the notebook from Colab, create a private GitHub repository, upload the notebook and CSV, commit them, then edit and commit your own README. The A2 form receives the notebook and README plus the repository URL.

Misconception to address
git commands belong in a terminal, not a Python cell. The web interface handles the remote commit directly. A repository upload does not replace the assignment form.

Continue to
Doing it: repository, commit, push

## Slide 29 — Doing it: repository, commit, push

Doing it: repository, commit, push
CML3112, Week 2, slide 29

Explanation to give
Distinguish saving the working file, recording a version and submitting an assignment. Git records chosen changes in commits; GitHub hosts a repository. A commit message should describe the change.

Worked illustration / lecturer answer
For today's browser route, download the notebook from Colab, create a private GitHub repository, upload the notebook and CSV, commit them, then edit and commit your own README. The A2 form receives the notebook and README plus the repository URL.

Misconception to address
git commands belong in a terminal, not a Python cell. The web interface handles the remote commit directly. A repository upload does not replace the assignment form.

Continue to
From Colab to GitHub

## Slide 30 — From Colab to GitHub

From Colab to GitHub
CML3112, Week 2, slide 30

Explanation to give
Distinguish saving the working file, recording a version and submitting an assignment. Git records chosen changes in commits; GitHub hosts a repository. A commit message should describe the change.

Worked illustration / lecturer answer
For today's browser route, download the notebook from Colab, create a private GitHub repository, upload the notebook and CSV, commit them, then edit and commit your own README. The A2 form receives the notebook and README plus the repository URL.

Misconception to address
git commands belong in a terminal, not a Python cell. The web interface handles the remote commit directly. A repository upload does not replace the assignment form.

Continue to
Assignment A2 — Proof of Life

## Slide 31 — Assignment A2 — Proof of Life

Assignment A2 — Proof of Life
CML3112, Week 2, slide 31

Explanation to give
A2 requires the completed main notebook and the student’s own README.md, with a repository URL in the form. Keep the CSV in the runtime/repository. The current guide is authoritative about the required execution-order explanation; repair exercises are practice. Read the live form cutoff rather than the old “start of Week 3” label.

Worked illustration / lecturer answer
Point to the particular code cell or answer on this slide while explaining the reasoning.

Misconception to address
The current assignment guide and live form take precedence over historical logistics printed in this deck.

Continue to
What makes a README worth reading

## Slide 32 — What makes a README worth reading

What makes a README worth reading
CML3112, Week 2, slide 32

Explanation to give
Treat the README as instructions for someone opening the project for the first time. Name the files, setup requirements, entry notebook and exact order needed to reproduce the result.

Worked illustration / lecturer answer
Replace “run the analysis” with “Open analysis.ipynb, place readings.csv in data/, restart the runtime and run all cells.” A useful repair comment names the failed step and the corrected filename.

Misconception to address
A repository URL proves a location exists, not that the work runs or was submitted. Contribution claims should point to specific work, not only a count of commits.

Continue to
Break and Fix

## Slide 33 — Break and Fix

Break and Fix
CML3112, Week 2, slide 33

Explanation to give
Teach a diagnosis sequence: read the final error line, locate the indicated instruction, compare the expected input with what actually exists, and fix the first cause. Explain the error type rather than treating all red output alike.

Worked illustration / lecturer answer
NameError often means a misspelled or not-yet-created name. FileNotFoundError means the named path was not found. TypeError can result from adding text and a number. A wrong answer can occur with no exception at all.

Misconception to address
The highlighted line is where Python noticed a problem, not always its original cause. Do not install an unrelated package when the exercise deliberately names a nonexistent module.

Continue to
Before you leave the room

## Slide 34 — Before you leave the room

Before you leave the room
CML3112, Week 2, slide 34

Explanation to give
There are separate submission actions: activate the Week 2 quiz for a 24-hour window, and use the A2 form for the completed notebook plus README. Five minutes is expected quiz effort, not a five-minute opening. Where catching up, A1 and Quiz 1 have separate links.

Worked illustration / lecturer answer
Point to the particular code cell or answer on this slide while explaining the reasoning.

Misconception to address
The current assignment guide and live form take precedence over historical logistics printed in this deck.

Continue to
Revision material

## Slide 35 — Revision material

Revision material
CML3112, Week 2, slide 35

Explanation to give
Orient students to this particular lesson: explain what they will see demonstrated, which file they will use and what they must retain for revision. Keep the transition short enough to preserve explanation time.

Worked illustration / lecturer answer
Open the next worked example on the projector and name its input and intended result. Demonstrate it yourself before asking students to interpret a result. Use remaining summary and glossary pages for independent revision.

Misconception to address
The historical slide's timed group activity is not a requirement to stop for partner work. Use a lecturer-led walkthrough in the current limited class time.

Continue to
What you should take away

## Slide 36 — What you should take away

What you should take away
CML3112, Week 2, slide 36

Explanation to give
Today the learner creates, runs, saves and submits a notebook. Separate those actions so a successful run is not mistaken for a saved or submitted file.

Worked illustration / lecturer answer
The runtime remembers readings = 12. One update adding 5 gives 17; repeating only that update gives 22. A fresh run starts at 12 again.

Misconception to address
Use the outcomes listed on this slide to check understanding through the small examples, rather than asking only whether everybody understands.

Continue to
Self-test — write something for each before you look

## Slide 37 — Self-test — write something for each before you look

Self-test — write something for each before you look
CML3112, Week 2, slide 37

Explanation to give
A: restart and run with required data available, then diagnose the first error. B: counters record actual execution sequence. C: git add naming two files stages those two, not all five. D: GitHub records project history; the current course collects graded files through the assignment form. E: Tests 1 and 2 use the prepared offline environment with invigilated collection.

Worked illustration / lecturer answer
Point to the particular code cell or answer on this slide while explaining the reasoning.

Misconception to address
The current assignment guide and live form take precedence over historical logistics printed in this deck.

Continue to
How did you do?

## Slide 38 — How did you do?

How did you do?
CML3112, Week 2, slide 38

Explanation to give
Clarify the old GitHub wording: repositories preserve work and contribution history, but the current grader receives uploaded assessment files. Students still need the appropriate submission form. A notebook that fails after restarting may lack variables, files or setup; do not assert stale memory is the only possible cause.

Worked illustration / lecturer answer
Point to the particular code cell or answer on this slide while explaining the reasoning.

Misconception to address
The current assignment guide and live form take precedence over historical logistics printed in this deck.

Continue to
Every word we used today (1 of 3)

## Slide 39 — Every word we used today (1 of 3)

Every word we used today (1 of 3)
CML3112, Week 2, slide 39

Explanation to give
Demonstrate the file-opening path slowly: sign in, open Colab, choose the notebook upload option and select the extracted .ipynb file. Connecting starts a remote Python runtime.

Worked illustration / lecturer answer
Open proof_of_life.ipynb, identify a code cell and run it with Shift+Enter. Show the result underneath. Upload its CSV separately through the runtime Files panel before reading it.

Misconception to address
Use this page for revision. Connect each word to the concrete example just taught; do not introduce all the definitions as new material in one block.

Continue to
Every word we used today (2 of 3)

## Slide 40 — Every word we used today (2 of 3)

Every word we used today (2 of 3)
CML3112, Week 2, slide 40

Explanation to give
Explain assignment as evaluating the right side and attaching the name on the left to that result. The name can later refer to a different value. Read the equals sign as “assign”, rather than as a mathematical claim that lasts forever.

Worked illustration / lecturer answer
length_m = 4 makes length_m refer to 4. length_m = 6 replaces that association. Printing length_m now displays 6; the name does not remember a history of both values.

Misconception to address
Use this page for revision. Connect each word to the concrete example just taught; do not introduce all the definitions as new material in one block.

Continue to
Every word we used today (3 of 3)

## Slide 41 — Every word we used today (3 of 3)

Every word we used today (3 of 3)
CML3112, Week 2, slide 41

Explanation to give
Treat the README as instructions for someone opening the project for the first time. Name the files, setup requirements, entry notebook and exact order needed to reproduce the result.

Worked illustration / lecturer answer
Replace “run the analysis” with “Open analysis.ipynb, place readings.csv in data/, restart the runtime and run all cells.” A useful repair comment names the failed step and the corrected filename.

Misconception to address
Use this page for revision. Connect each word to the concrete example just taught; do not introduce all the definitions as new material in one block.

Continue to
One-page reference — the commands and the habits

## Slide 42 — One-page reference — the commands and the habits

One-page reference — the commands and the habits
CML3112, Week 2, slide 42

Explanation to give
Use this as a reference, not a command drill. Today’s browser GitHub route does not require the terminal commands. Before submission, load the correct data, restart, run all and save. For an error, read its type and the indicated operation, then describe what was expected and what happened.

Worked illustration / lecturer answer
Point to the particular code cell or answer on this slide while explaining the reasoning.

Misconception to address
The current assignment guide and live form take precedence over historical logistics printed in this deck.

Continue to
Five questions,

## Slide 43 — Five questions,

Five questions,
CML3112, Week 2, slide 43

Explanation to give
This is the CML3112 Week 2 quiz. The student link opens the response form; it does not activate its window. In Quiz Controls use open_W2_CML3112 when ready and read the logged closing time.

Worked illustration / lecturer answer
Explain the distinction between the expected answering time and availability: five minutes of questions can still be available for 24 hours after activation. Enter the learner’s own Student Registration Number and use the registered Google account.

Misconception to address
Read the exact live cutoff before announcing it. Do not promise a new attempt to somebody who already submitted. Quiz catch-up and assignment uploads are separate forms.

Continue to
Error messages provide clues

## Slide 44 — Error messages provide clues

Error messages provide clues
CML3112, Week 2, slide 44

Explanation to give
Close with a precise correction: some wrong results produce no exception, so reading errors is only part of checking work. Verify run order, the input file, units and whether the result is plausible. Next week explains the Python values and operators used in the first notebook.

Worked illustration / lecturer answer
Point to the particular code cell or answer on this slide while explaining the reasoning.

Misconception to address
The current assignment guide and live form take precedence over historical logistics printed in this deck.
