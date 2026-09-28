# CML3112 Week02 Design Infrastructure

Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.

## Slide 1 — Where the work

TEACHING PURPOSE
Where the work

LECTURER CUE
Today you stop reading about this and start doing it. By the end of the session you will have run your own code, seen its output, and put it somewhere a marker can find it.
You need three things: a browser, a Google account and a GitHub account. You do not need to install anything at all — that is deliberate.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
By the end of today you can…. Move on after a learner can explain the current example or required action.

## Slide 2 — By the end of today you can…

TEACHING PURPOSE
By the end of today you can…

CONNECT
Build on the preceding slide: Where the work.

LECTURER CUE
Seven objectives, and the fourth is the one that will save you the most time all semester.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
How today runs. Move on after a learner can explain the current example or required action.

## Slide 3 — How today runs

TEACHING PURPOSE
How today runs

CONNECT
Build on the preceding slide: By the end of today you can….

LECTURER CUE
The same eleven-segment shape as Week 1, with more keyboard time than any session so far. The break falls at the midpoint, straight after the execution-trap segment.

NEXT
Where we got to, and where we are going. Move on after a learner can explain the current example or required action.

## Slide 4 — Where we got to, and where we are going

TEACHING PURPOSE
Where we got to, and where we are going

CONNECT
Build on the preceding slide: How today runs.

LECTURER CUE
Ten minutes of recall before any new material. A2 is due at the start of Week 3, and by the end of today most of it is already built.

NEXT
Two minutes: what stuck from Week 1?. Move on after a learner can explain the current example or required action.

## Slide 5 — Two minutes: what stuck from Week 1?

TEACHING PURPOSE
Two minutes: what stuck from Week 1?

CONNECT
Build on the preceding slide: Where we got to, and where we are going.

LECTURER CUE
These three answers are the vocabulary the rest of the semester assumes. If you cannot answer them, the Week 1 deck's glossary slide has all of it in one place.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

DISCUSSION KEY FOR THIS SLIDE
ANSWERS
How did you do?
A
The input columns, and the value?
The columns you were given are the FEATURES. The value you predicted is the TARGET. One row with both is one EXAMPLE.
B
Days until servicing?
Regression — the answer is a number with a unit. If it were 'service due or not' it would be classification.
C
One of the four limits?
No data · no signal · physics is simply better · the future stopped resembling the past. Any one of those.
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
How did you do?. Move on after a learner can explain the current example or required action.

## Slide 6 — How did you do?

TEACHING PURPOSE
How did you do?

CONNECT
Build on the preceding slide: Two minutes: what stuck from Week 1?.

LECTURER CUE
Features, target, example: those three words are the vocabulary every later week assumes. If the first question was hard, the Week 1 deck's data-table figure and glossary slide have all of it in one place, and half an hour on them this evening is worth more than anything else you could revise.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

NEXT
Four questions, four tools. Move on after a learner can explain the current example or required action.

## Slide 7 — Four questions, four tools

TEACHING PURPOSE
Four questions, four tools

CONNECT
Build on the preceding slide: How did you do?.

LECTURER CUE
Each of today's four tools answers a different question, and the question is the part to remember. Meeting ten libraries in three weeks and retaining none is the standard way an introductory data course fails; knowing which question each tool answers is what stops it happening to you.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
The four questions. Move on after a learner can explain the current example or required action.

## Slide 8 — The four questions

TEACHING PURPOSE
The four questions

CONNECT
Build on the preceding slide: Four questions, four tools.

LECTURER CUE
Read it as four questions rather than four products. The question is the durable part — the tool that answers it will change during your career, and the question will not.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
Google Colab. Move on after a learner can explain the current example or required action.

## Slide 9 — Google Colab

TEACHING PURPOSE
Google Colab

CONNECT
Build on the preceding slide: The four questions.

LECTURER CUE
The reason this course uses Colab is bandwidth and time. A hundred students installing Python, an editor and five libraries over one campus connection does not work; it has to be attempted to be believed.
The honest limitation: Colab needs an internet connection. That is why the two practical tests in Weeks 7 and 14 are sat offline on lab machines instead, and why the Setup Guide still exists for anyone who wants a local installation.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Your first notebook. Move on after a learner can explain the current example or required action.

## Slide 10 — Your first notebook

TEACHING PURPOSE
Your first notebook

CONNECT
Build on the preceding slide: Google Colab.

LECTURER CUE
Thirty minutes with your hands on the keyboard. Open a browser now — this segment does not work as something you watch.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Three cells. Move on after a learner can explain the current example or required action.

## Slide 11 — Three cells

TEACHING PURPOSE
Three cells

CONNECT
Build on the preceding slide: Your first notebook.

LECTURER CUE
Three cells, and each teaches one thing. Cell 1: code runs and produces output underneath it. Cell 2: a name can hold a value, and that value survives into the next cell. Cell 3: running the same cell twice is not the same as running it once.
The f in front of a string is what lets you put a variable inside the text — anything in {curly braces} is replaced by that variable's value.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
The three things that go wrong in the first ten minutes. Move on after a learner can explain the current example or required action.

## Slide 12 — The three things that go wrong in the first ten minutes

TEACHING PURPOSE
The three things that go wrong in the first ten minutes

CONNECT
Build on the preceding slide: Three cells.

LECTURER CUE
Every item on this slide came from a real beginner making that mistake in a real first session. Shift-and-Enter alone accounts for a large share of the first ten minutes. Keep the slide in view while you work rather than reading it once, because it answers most of what goes wrong before you have to ask anybody.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Markdown cell. Move on after a learner can explain the current example or required action.

## Slide 13 — Markdown cell

TEACHING PURPOSE
Markdown cell

CONNECT
Build on the preceding slide: The three things that go wrong in the first ten minutes.

LECTURER CUE
This is what makes a notebook better than a script for data work: the reasoning lives beside the calculation instead of in a separate report nobody updates.
In Colab, press the + Text button instead of + Code. A # at the start of a line makes it a heading; ** around words makes them bold.
From Week 5 your submitted notebooks are marked partly on whether a reader can follow them, so this is not optional polish.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Thirty seconds: check you are with me. Move on after a learner can explain the current example or required action.

## Slide 14 — Thirty seconds: check you are with me

TEACHING PURPOSE
Thirty seconds: check you are with me

CONNECT
Build on the preceding slide: Markdown cell.

LECTURER CUE
Three quick questions to confirm you are still with the session. Question C is the interesting one: two people running identical code and getting different numbers is a real property of notebooks, and the execution-order block explains why.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

DISCUSSION KEY FOR THIS SLIDE
ANSWERS
How did you do?
A
Enter did nothing?
Enter adds a new line inside the cell. Shift and Enter together runs it. This catches almost everybody once.
B
Where does 'hello' appear?
Directly underneath that cell, in the output area. Not in a separate window — a notebook keeps the code and its output together, which is the whole point of it.
C
27 versus 17 — who is wrong?
Neither. They have run the cell a different number of times. That is not a difference of opinion, it is a property of how notebooks work — and it is the subject of the execution-order block.
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
How did you do?. Move on after a learner can explain the current example or required action.

## Slide 15 — How did you do?

TEACHING PURPOSE
How did you do?

CONNECT
Build on the preceding slide: Thirty seconds: check you are with me.

LECTURER CUE
Answer C sets up the next segment. Two notebooks holding identical code can hold different values, because the kernel remembers how many times each cell has been run and the screen does not show you that history. Neither person is wrong; the notebook is simply not telling you everything it knows.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
What a notebook actually is. Move on after a learner can explain the current example or required action.

## Slide 16 — What a notebook actually is

TEACHING PURPOSE
What a notebook actually is

CONNECT
Build on the preceding slide: How did you do?.

LECTURER CUE
Twenty minutes away from the keyboard, and the only concept block in the session. The execution-order block depends on it, because the execution trap only makes sense once you know what the kernel is holding on your behalf.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
The anatomy of a notebook. Move on after a learner can explain the current example or required action.

## Slide 17 — The anatomy of a notebook

TEACHING PURPOSE
The anatomy of a notebook

CONNECT
Build on the preceding slide: What a notebook actually is.

LECTURER CUE
The kernel is the part worth understanding properly. It is a single Python session sitting behind the whole notebook, so a variable made in cell 2 is available in cell 7 because both cells are talking to that one session. The cells themselves have no connection to each other.
This is also why a notebook can lie to you. The kernel remembers everything you have run in the order you ran it, and that order need not match the order the cells appear on screen.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Cell, kernel, and the execution counter. Move on after a learner can explain the current example or required action.

## Slide 18 — Cell, kernel, and the execution counter

TEACHING PURPOSE
Cell, kernel, and the execution counter

CONNECT
Build on the preceding slide: The anatomy of a notebook.

LECTURER CUE
Watch the execution counter. It is the single most useful diagnostic in a notebook and almost no beginner looks at it.
A notebook where the counters run 1, 2, 3, 4 top to bottom is a notebook you can trust. Anything else needs checking.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
The trap, and the habit that saves you. Move on after a learner can explain the current example or required action.

## Slide 19 — The trap, and the habit that saves you

TEACHING PURPOSE
The trap, and the habit that saves you

CONNECT
Build on the preceding slide: Cell, kernel, and the execution counter.

LECTURER CUE
Twenty minutes on the most common way a notebook produces a confident wrong answer, and on the one menu item that prevents it. If you take a single habit out of Week 2, take this one.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
The same cell, run three times. Move on after a learner can explain the current example or required action.

## Slide 20 — The same cell, run three times

TEACHING PURPOSE
The same cell, run three times

CONNECT
Build on the preceding slide: The trap, and the habit that saves you.

LECTURER CUE
This is why `readings = readings + 5` behaves the way it does: the right-hand side is worked out first, using whatever is currently in readings, and the result is then put back into readings. Run it three times and you have added fifteen.
The habit: **Restart and Run All** before you believe any answer. It clears the kernel and runs every cell from the top in order, which is exactly what your marker's machine will do.
From Week 5 your submitted work is graded by a program that does precisely this from a clean start. If your notebook only works in the order you happened to click, it does not work.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Can you answer these?. Move on after a learner can explain the current example or required action.

## Slide 21 — Can you answer these?

TEACHING PURPOSE
Can you answer these?

CONNECT
Build on the preceding slide: The same cell, run three times.

LECTURER CUE
Question B is the one to take slowly. It is the realisation that 'it worked' can be an illusion produced by execution order, and that restarting is what turns the claim into evidence.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

DISCUSSION KEY FOR THIS SLIDE
ANSWERS
How did you do?
A
Counters [4], [1], [5], [2]?
They were run out of order, so the kernel's memory does not match what the notebook looks like. Do not trust the final answer until you have restarted and run all.
B
It fails after restarting?
Cell 6 was depending on something created by a cell that has since been changed or deleted — or on a cell further down that you happened to run earlier. It never actually worked from a clean start; the kernel was just still holding the leftovers.
C
Why restart rather than re-run one cell?
Because re-running one cell keeps everything else the kernel is holding, including things that no longer exist anywhere in your code. Only a restart proves the notebook can produce its results from nothing but itself — which is what reproducibility means.
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
How did you do?. Move on after a learner can explain the current example or required action.

## Slide 22 — How did you do?

TEACHING PURPOSE
How did you do?

CONNECT
Build on the preceding slide: Can you answer these?.

LECTURER CUE
Answer B describes the most common way submitted work loses marks: the notebook ran for you and then failed for the marker. Every automated grader and every colleague runs code from a clean start, which is the whole reason the restart habit is asked for here.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Diagnosing a notebook from its counters. Move on after a learner can explain the current example or required action.

## Slide 23 — Diagnosing a notebook from its counters

TEACHING PURPOSE
Diagnosing a notebook from its counters

CONNECT
Build on the preceding slide: How did you do?.

LECTURER CUE
This is the diagnostic routine to use for the rest of your degree. Counters out of order, or a blank counter, mean the notebook and the kernel disagree, and the kernel is what actually ran.
Step 4 is the question that matters. A result you cannot reproduce from a clean start is indistinguishable from a coincidence, which is why reproducibility gets treated as an engineering requirement in this course.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Break. Move on after a learner can explain the current example or required action.

## Slide 24 — Break

TEACHING PURPOSE
Break

CONNECT
Build on the preceding slide: Diagnosing a notebook from its counters.

LECTURER CUE
Ten minutes. Git comes after the break and it needs you awake.

NEXT
What version control gives you. Move on after a learner can explain the current example or required action.

## Slide 25 — What version control gives you

TEACHING PURPOSE
What version control gives you

CONNECT
Build on the preceding slide: Break.

LECTURER CUE
Twenty-five minutes on what Git records that a copied folder does not. The commands come later; this segment is about the problem they solve, because Git treated as ceremony never gets used voluntarily.

EXPLAIN IN ORDINARY WORDS
A repository is the project folder and recorded history. A commit records a chosen change; uploading or pushing shares it. A README tells someone else how to run the work.

CHECK AND EXPECTED ANSWER
Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.

IF LEARNERS ARE STUCK
Ask a partner to follow only the README. It should identify the data, files, run order and expected result. Keep secrets out of the repository.

NEXT
The problem Git actually solves. Move on after a learner can explain the current example or required action.

## Slide 26 — The problem Git actually solves

TEACHING PURPOSE
The problem Git actually solves

CONNECT
Build on the preceding slide: What version control gives you.

LECTURER CUE
The 'final_v3_REAL_final' folder is a problem everybody recognises, and Git is the tool built for it. The assessment consequence is the part to take seriously: your commit history is the evidence of which part of a team project you did, and sixty-five per cent of your mark is individual.

EXPLAIN IN ORDINARY WORDS
A repository is the project folder and recorded history. A commit records a chosen change; uploading or pushing shares it. A README tells someone else how to run the work.

CHECK AND EXPECTED ANSWER
Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.

IF LEARNERS ARE STUCK
Ask a partner to follow only the README. It should identify the data, files, run order and expected result. Keep secrets out of the repository.

NEXT
The four places your work can be. Move on after a learner can explain the current example or required action.

## Slide 27 — The four places your work can be

TEACHING PURPOSE
The four places your work can be

CONNECT
Build on the preceding slide: The problem Git actually solves.

LECTURER CUE
Most Git confusion comes from not knowing which of these four places a file is in. The diagram is worth photographing.
The staging area feels like a pointless extra step until the first time you want to commit two of the five files you changed. That is what it is for.

EXPLAIN IN ORDINARY WORDS
A repository is the project folder and recorded history. A commit records a chosen change; uploading or pushing shares it. A README tells someone else how to run the work.

CHECK AND EXPECTED ANSWER
Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.

IF LEARNERS ARE STUCK
Ask a partner to follow only the README. It should identify the data, files, run order and expected result. Keep secrets out of the repository.

NEXT
Repository, commit, and push. Move on after a learner can explain the current example or required action.

## Slide 28 — Repository, commit, and push

TEACHING PURPOSE
Repository, commit, and push

CONNECT
Build on the preceding slide: The four places your work can be.

LECTURER CUE
Commit messages matter more than beginners expect. 'update', 'fix' and 'stuff' are worthless in November. A message should say what changed and, where it is not obvious, why.

EXPLAIN IN ORDINARY WORDS
A repository is the project folder and recorded history. A commit records a chosen change; uploading or pushing shares it. A README tells someone else how to run the work.

CHECK AND EXPECTED ANSWER
Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.

IF LEARNERS ARE STUCK
Ask a partner to follow only the README. It should identify the data, files, run order and expected result. Keep secrets out of the repository.

NEXT
Doing it: repository, commit, push. Move on after a learner can explain the current example or required action.

## Slide 29 — Doing it: repository, commit, push

TEACHING PURPOSE
Doing it: repository, commit, push

CONNECT
Build on the preceding slide: Repository, commit, and push.

LECTURER CUE
Twenty-five minutes with the whole room in step. You leave this segment with a live GitHub URL, and submit that URL together with the notebook and README.md for A2.

EXPLAIN IN ORDINARY WORDS
A repository is the project folder and recorded history. A commit records a chosen change; uploading or pushing shares it. A README tells someone else how to run the work.

CHECK AND EXPECTED ANSWER
Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.

IF LEARNERS ARE STUCK
Ask a partner to follow only the README. It should identify the data, files, run order and expected result. Keep secrets out of the repository.

NEXT
From Colab to GitHub. Move on after a learner can explain the current example or required action.

## Slide 30 — From Colab to GitHub

TEACHING PURPOSE
From Colab to GitHub

CONNECT
Build on the preceding slide: Doing it: repository, commit, push.

LECTURER CUE
Use the browser route in STUDENT_HOW_TO.md: download the completed notebook from Colab; create a private GitHub repository with a README; choose Add file, Upload files; add the notebook and supplied CSV; commit the changes. Edit and commit your own README. The displayed Git commands are optional reference for a local terminal, not instructions to type into a Python cell.

EXPLAIN IN ORDINARY WORDS
A repository is the project folder and recorded history. A commit records a chosen change; uploading or pushing shares it. A README tells someone else how to run the work.

CHECK AND EXPECTED ANSWER
Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.

IF LEARNERS ARE STUCK
Ask a partner to follow only the README. It should identify the data, files, run order and expected result. Keep secrets out of the repository.

NEXT
Assignment A2 — Proof of Life. Move on after a learner can explain the current example or required action.

## Slide 31 — Assignment A2 — Proof of Life

TEACHING PURPOSE
Assignment A2 — Proof of Life

CONNECT
Build on the preceding slide: From Colab to GitHub.

LECTURER CUE
A2 is marked out of 20: identity 2, proof_sum 4, fresh-run readings 4, correct CSV records 4, execution-order explanation 3, README 3. Keep My explanation: in the notebook text cell. Submit exactly the completed renamed notebook and your own README.md together, plus the repository URL in its form field. The CSV stays in the runtime and repository. Use the current cohort form deadline; do not promise an automatic redo or extra attempt. A1, Quiz 1, A2 and Quiz 2 are separate tasks.

EXPLAIN IN ORDINARY WORDS
A CSV is a text table. The header supplies column names. With csv.DictReader, values start as text, even if they look like numbers. A path tells Python where the file is.

CHECK AND EXPECTED ANSWER
Can "2.5" from csv.DictReader be added as a number without conversion? No; convert valid numeric text first.

IF LEARNERS ARE STUCK
Show the file in the runtime folder and compare its exact filename, case and column headers. Upload data again after a fresh Colab runtime.

NEXT
What makes a README worth reading. Move on after a learner can explain the current example or required action.

## Slide 32 — What makes a README worth reading

TEACHING PURPOSE
What makes a README worth reading

CONNECT
Build on the preceding slide: Assignment A2 — Proof of Life.

LECTURER CUE
The README is required now. Include the programme, exact file list, instructions to open the notebook, upload the CSV, restart and run from the top, then save/download. Demonstrate editing README.md on GitHub and downloading the raw file. Ask a partner to follow the instructions literally. Do not submit the instruction README supplied in the ZIP.

EXPLAIN IN ORDINARY WORDS
A repository is the project folder and recorded history. A commit records a chosen change; uploading or pushing shares it. A README tells someone else how to run the work.

CHECK AND EXPECTED ANSWER
Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.

IF LEARNERS ARE STUCK
Ask a partner to follow only the README. It should identify the data, files, run order and expected result. Keep secrets out of the repository.

NEXT
Break and Fix. Move on after a learner can explain the current example or required action.

## Slide 33 — Break and Fix

TEACHING PURPOSE
Break and Fix

CONNECT
Build on the preceding slide: What makes a README worth reading.

LECTURER CUE
Guide repairs 01–04 in class, one at a time. 01: identify the deliberately unavailable module and remove the unused import; do not install the made-up package. 02: compare the required and actual Python versions. 03: locate the CSV and correct its path. 04: trace 12, then 17, then the unwanted reset to 12. Remove the reset; restart and Run all for 17. Ask learners to state the cause before showing a repair. These notebooks and hello_engineering.py are practice only; return to proof_of_life.ipynb for the assessed work.

EXPLAIN IN ORDINARY WORDS
A module supplies Python tools; import asks Python to load it. A version identifies a software release. A path identifies a file. A state error happens when stored values differ from what we expected.

CHECK AND EXPECTED ANSWER
Notebook 04 starts at 12, adds 5 to get 17, then resets to 12. Why does it print 12? The final assignment overwrites 17.

IF LEARNERS ARE STUCK
01: the named module is deliberately unavailable; remove the unused import instead of trying to install a made-up package. 02: the exercise asserts Python 2 but the course uses Python 3; inspect sys.version_info and correct that deliberate mismatch. 03: upload the issued CSV and replace the nonexistent folder path with its real filename. 04: remove the unwanted reset, restart and run all for 17; repeat only the increment to see 22, then 27.

NEXT
Before you leave the room. Move on after a learner can explain the current example or required action.

## Slide 34 — Before you leave the room

TEACHING PURPOSE
Before you leave the room

CONNECT
Build on the preceding slide: Break and Fix.

LECTURER CUE
Answer the setup question honestly. 'I could not get that far' is worth more to me than a guess, and it is not the question that carries the mark.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Revision material. Move on after a learner can explain the current example or required action.

## Slide 35 — Revision material

TEACHING PURPOSE
Revision material

CONNECT
Build on the preceding slide: Before you leave the room.

LECTURER CUE
Everything past this slide is revision material: a summary, a self-test with worked answers, an eighteen-term glossary and a one-page command reference. It is written to be studied from during the week.

NEXT
What you should take away. Move on after a learner can explain the current example or required action.

## Slide 36 — What you should take away

TEACHING PURPOSE
What you should take away

CONNECT
Build on the preceding slide: Revision material.

LECTURER CUE
Seven statements covering the whole session. The fourth and the seventh are the two that carry into every later week: Restart and Run All as the only honest test, and the broken notebook that never announces itself.

EXPLAIN IN ORDINARY WORDS
A value is a piece of information. A variable is a name referring to a value. In length_m = 5, Python evaluates the right side and binds that result to the name on the left.

CHECK AND EXPECTED ANSWER
After x=3 then x=5, what does print(x) display? 5. The earlier value is not added automatically.

IF LEARNERS ARE STUCK
Write the name on a card and the current value beside it. Distinguish number 3 from quoted text "3".

NEXT
Self-test — write something for each before you look. Move on after a learner can explain the current example or required action.

## Slide 37 — Self-test — write something for each before you look

TEACHING PURPOSE
Self-test — write something for each before you look

CONNECT
Build on the preceding slide: What you should take away.

LECTURER CUE
Question E is worth thinking about properly. It is the trade-off at the centre of how this course is set up.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

DISCUSSION KEY FOR THIS SLIDE
ANSWERS
How did you do?
A
'It worked yesterday'?
Restart and Run All. Almost always the kernel was holding something from a cell that has since changed or been deleted, so it never really worked from a clean start.
B
What the counter tells you?
The order in which cells were actually executed. Position on the page is only a layout — the counter is what the kernel actually did, and the two can disagree.
C
Recording two of five files?
git add, naming just those two files rather than using a dot. They move into the staging area, and only staged files go into the next commit.
D
Why GitHub rather than email?
Because it records who did what and when, which is how a team mark becomes an individual one; because the grading tools collect work from repositories automatically; and because it is what every engineering employer expects you to have used.
E
Colab needs internet — so how are the tests run?
Offline, on laboratory machines with a local Python installation and no network. That is deliberate: it makes the no-AI-assistance rule actually enforceable rather than a request, and it certifies what you can do unaided. It is also why the Student Setup Guide still exists.
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
How did you do?. Move on after a learner can explain the current example or required action.

## Slide 38 — How did you do?

TEACHING PURPOSE
How did you do?

CONNECT
Build on the preceding slide: Self-test — write something for each before you look.

LECTURER CUE
Answer E is the trade-off at the centre of how this course is set up. Colab removes every installation problem and needs a connection to work; the offline lab machines make the no-AI rule in the two tests enforceable rather than a request. Both compromises are deliberate, and they are why the Student Setup Guide still exists for anyone who wants a local installation.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Every word we used today (1 of 3). Move on after a learner can explain the current example or required action.

## Slide 39 — Every word we used today (1 of 3)

TEACHING PURPOSE
Every word we used today (1 of 3)

CONNECT
Build on the preceding slide: How did you do?.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Every word we used today (2 of 3). Move on after a learner can explain the current example or required action.

## Slide 40 — Every word we used today (2 of 3)

TEACHING PURPOSE
Every word we used today (2 of 3)

CONNECT
Build on the preceding slide: Every word we used today (1 of 3).

EXPLAIN IN ORDINARY WORDS
A value is a piece of information. A variable is a name referring to a value. In length_m = 5, Python evaluates the right side and binds that result to the name on the left.

CHECK AND EXPECTED ANSWER
After x=3 then x=5, what does print(x) display? 5. The earlier value is not added automatically.

IF LEARNERS ARE STUCK
Write the name on a card and the current value beside it. Distinguish number 3 from quoted text "3".

NEXT
Every word we used today (3 of 3). Move on after a learner can explain the current example or required action.

## Slide 41 — Every word we used today (3 of 3)

TEACHING PURPOSE
Every word we used today (3 of 3)

CONNECT
Build on the preceding slide: Every word we used today (2 of 3).

LECTURER CUE
Eighteen terms, and all of them are used every week from now on. If you can define them all by Week 4 you are in good shape — several appear in the weekly quizzes.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

NEXT
One-page reference — the commands and the habits. Move on after a learner can explain the current example or required action.

## Slide 42 — One-page reference — the commands and the habits

TEACHING PURPOSE
One-page reference — the commands and the habits

CONNECT
Build on the preceding slide: Every word we used today (3 of 3).

LECTURER CUE
Photograph this slide. It answers most of what comes up in Weeks 3 to 6, and the four Git commands on it are the same four you will still be using on the project in Week 13.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Five questions,. Move on after a learner can explain the current example or required action.

## Slide 43 — Five questions,

TEACHING PURPOSE
Five questions,

CONNECT
Build on the preceding slide: One-page reference — the commands and the habits.

LECTURER CUE
The last five minutes of every teaching session. Five questions, one per cent, and you see your score as you submit.
Nothing on it can be answered without reading what it shows you, so there is nothing to revise for it beyond having done the session. Twelve run across the semester and the best ten count.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

QUIZ OPERATION
Opening the student link does not activate the quiz. In Quiz Controls run the matching open_W<week>_<cohort> function once when ready. Announce the logged closing time: 24 hours after activation. Five minutes describes expected answering time, not the availability window. Quiz 1 and Quiz 2 require separate activation when collecting catch-up work.

NEXT
Every error today told you. Move on after a learner can explain the current example or required action.

## Slide 44 — Every error today told you

TEACHING PURPOSE
Every error today told you

CONNECT
Build on the preceding slide: Five questions,.

LECTURER CUE
Everything you saw go wrong today has gone wrong for every engineer in this building, and it will keep happening for the rest of your career. What changes is how long it takes you to read the message and carry on. Next week is Python as an engineering calculator, built on formulas from your own programme.
