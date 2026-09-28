# CML3113 Week02 Mining Petroleum

Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.

## Slide 1 — Running and saving your first notebook

TEACHING PURPOSE
Running and saving your first notebook

LECTURER CUE
Use PowerPoint Presenter View for these notes. Teach one example, pause for every learner to predict, then work an analogous example together. The practice notebook is a learning aid, not an extra graded upload.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Today’s learning. Move on after a learner can explain the current example or required action.

## Slide 2 — Today’s learning

TEACHING PURPOSE
Today’s learning

CONNECT
Build on the preceding slide: Running and saving your first notebook.

LECTURER CUE
Ask learners to explain this goal in ordinary language. The first successful attempt matters more than covering optional extensions. Defer: Terminal commands, staging, branching, merging, GitHub Desktop installation and f-string formatting are reference topics. Do not make them prerequisites for A2.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Week 2 includes your Week 1 catch-up. Move on after a learner can explain the current example or required action.

## Slide 3 — Week 2 includes your Week 1 catch-up

TEACHING PURPOSE
Week 2 includes your Week 1 catch-up

CONNECT
Build on the preceding slide: Today’s learning.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Recall and a first attempt. Move on after a learner can explain the current example or required action.

## Slide 4 — Recall and a first attempt

TEACHING PURPOSE
Recall and a first attempt

CONNECT
Build on the preceding slide: Week 2 includes your Week 1 catch-up.

LECTURER CUE
Allow two minutes for everyone to try. Ask pairs to compare. If many cannot begin, show the first step and repeat with changed values. Checkpoint for today: Ask everyone to point to the output, rerun one cell, and find the saved .ipynb on their own computer. If they cannot, repeat these actions before GitHub.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

NEXT
The engineering context. Move on after a learner can explain the current example or required action.

## Slide 5 — The engineering context

TEACHING PURPOSE
The engineering context

CONNECT
Build on the preceding slide: Recall and a first attempt.

LECTURER CUE
A pump team records temperature to investigate operation. Mining students can relate this to a dewatering pump; petroleum students to a transfer pump. These are teaching examples, not operating limits.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
Measurements become observations. Move on after a learner can explain the current example or required action.

## Slide 6 — Measurements become observations

TEACHING PURPOSE
Measurements become observations

CONNECT
Build on the preceding slide: The engineering context.

LECTURER CUE
Ask students to describe what they see before introducing terminology. Generated conceptual teaching illustration.  Source: figs/experiential/ASSET_SOURCES.md.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
Words we will use. Move on after a learner can explain the current example or required action.

## Slide 7 — Words we will use

TEACHING PURPOSE
Words we will use

CONNECT
Build on the preceding slide: Measurements become observations.

EXPLAIN IN ORDINARY WORDS
A CSV is a text table. The header supplies column names. With csv.DictReader, values start as text, even if they look like numbers. A path tells Python where the file is.

CHECK AND EXPECTED ANSWER
Can "2.5" from csv.DictReader be added as a number without conversion? No; convert valid numeric text first.

IF LEARNERS ARE STUCK
Show the file in the runtime folder and compare its exact filename, case and column headers. Upload data again after a fresh Colab runtime.

POINT TO THE DEFINITION
File: A saved item with a name. Its extension tells us the kind: .ipynb is a notebook, .csv a table, .py a Python script and .md a text document.
Folder: A container that helps you keep related files together. Extracting a ZIP restores the files inside it.

NEXT
The files in your ZIP. Move on after a learner can explain the current example or required action.

## Slide 8 — The files in your ZIP

TEACHING PURPOSE
The files in your ZIP

CONNECT
Build on the preceding slide: Words we will use.

EXPLAIN IN ORDINARY WORDS
A module supplies Python tools; import asks Python to load it. A version identifies a software release. A path identifies a file. A state error happens when stored values differ from what we expected.

CHECK AND EXPECTED ANSWER
Notebook 04 starts at 12, adds 5 to get 17, then resets to 12. Why does it print 12? The final assignment overwrites 17.

IF LEARNERS ARE STUCK
01: the named module is deliberately unavailable; remove the unused import instead of trying to install a made-up package. 02: the exercise asserts Python 2 but the course uses Python 3; inspect sys.version_info and correct that deliberate mismatch. 03: upload the issued CSV and replace the nonexistent folder path with its real filename. 04: remove the unwanted reset, restart and run all for 17; repeat only the increment to see 22, then 27.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
A script and a notebook. Move on after a learner can explain the current example or required action.

## Slide 9 — A script and a notebook

TEACHING PURPOSE
A script and a notebook

CONNECT
Build on the preceding slide: The files in your ZIP.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Open the main notebook together. Move on after a learner can explain the current example or required action.

## Slide 10 — Open the main notebook together

TEACHING PURPOSE
Open the main notebook together

CONNECT
Build on the preceding slide: A script and a notebook.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Words we will use. Move on after a learner can explain the current example or required action.

## Slide 11 — Words we will use

TEACHING PURPOSE
Words we will use

CONNECT
Build on the preceding slide: Open the main notebook together.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

POINT TO THE DEFINITION
Python and code: Python is the language. Code is the instructions written in that language. Running asks the computer to carry them out.
Cell and output: A cell is one notebook block. A code cell runs instructions; a text cell explains them. Output is the result shown below a code cell.

NEXT
A notebook has two kinds of cell. Move on after a learner can explain the current example or required action.

## Slide 12 — A notebook has two kinds of cell

TEACHING PURPOSE
A notebook has two kinds of cell

CONNECT
Build on the preceding slide: Words we will use.

LECTURER CUE
Open the extracted proof_of_life.ipynb in Colab. Show the code cell, text cell, run button and output with the pointer before asking students to click.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Cells share one Python session. Move on after a learner can explain the current example or required action.

## Slide 13 — Cells share one Python session

TEACHING PURPOSE
Cells share one Python session

CONNECT
Build on the preceding slide: A notebook has two kinds of cell.

LECTURER CUE
Point to the code, saved output and shared memory. The pictured filename is illustrative. Open proof_of_life.ipynb for today’s work.
Source: existing course illustration figs/notebook_anatomy.png. These are illustrative examples, not this cohort’s assessed results.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Start with numbers and values. Move on after a learner can explain the current example or required action.

## Slide 14 — Start with numbers and values

TEACHING PURPOSE
Start with numbers and values

CONNECT
Build on the preceding slide: Cells share one Python session.

EXPLAIN IN ORDINARY WORDS
A value is a piece of information. A variable is a name referring to a value. In length_m = 5, Python evaluates the right side and binds that result to the name on the left.

CHECK AND EXPECTED ANSWER
After x=3 then x=5, what does print(x) display? 5. The earlier value is not added automatically.

IF LEARNERS ARE STUCK
Write the name on a card and the current value beside it. Distinguish number 3 from quoted text "3".

POINT TO THE DEFINITION
Number: A number expresses how much or how many: 3 items or 2.5 metres. Whole numbers count; decimal numbers can describe a part of a unit.
Value and unit: A value is one piece of information. The number 2.5 is a value. A measurement also needs a unit, such as metres. Python does not attach that unit automatically.

NEXT
Give a value a name. Move on after a learner can explain the current example or required action.

## Slide 15 — Give a value a name

TEACHING PURPOSE
Give a value a name

CONNECT
Build on the preceding slide: Start with numbers and values.

EXPLAIN IN ORDINARY WORDS
A value is a piece of information. A variable is a name referring to a value. In length_m = 5, Python evaluates the right side and binds that result to the name on the left.

CHECK AND EXPECTED ANSWER
After x=3 then x=5, what does print(x) display? 5. The earlier value is not added automatically.

IF LEARNERS ARE STUCK
Write the name on a card and the current value beside it. Distinguish number 3 from quoted text "3".

POINT TO THE DEFINITION
Variable: A variable is a name referring to a value. In readings = 12, readings is the name and 12 is its initial number.
Assignment: Read = as “assign”, not “is equal to”. Python calculates the right side first, then gives that value to the name on the left. A later assignment replaces its previous value.

NEXT
Four symbols in our first program. Move on after a learner can explain the current example or required action.

## Slide 16 — Four symbols in our first program

TEACHING PURPOSE
Four symbols in our first program

CONNECT
Build on the preceding slide: Give a value a name.

LECTURER CUE
Read each symbol aloud: = stores a value under a name; + adds; print(...) displays its input; parentheses hold the input to print. A # starts a comment for a person.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

NEXT
The session remembers earlier values. Move on after a learner can explain the current example or required action.

## Slide 17 — The session remembers earlier values

TEACHING PURPOSE
The session remembers earlier values

CONNECT
Build on the preceding slide: Four symbols in our first program.

LECTURER CUE
Run the following cells separately. After the first cell, readings refers to 12. The second reads the current value, adds 5, then stores the answer under the same name.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Worked example. Move on after a learner can explain the current example or required action.

## Slide 18 — Worked example

TEACHING PURPOSE
Worked example

CONNECT
Build on the preceding slide: The session remembers earlier values.

LECTURER CUE
Open the extracted proof_of_life.ipynb in Colab. Show the code cell, text cell, run button and output with the pointer before asking students to click. Read each symbol aloud: = stores a value under a name; + adds; print(...) displays its input; parentheses hold the input to print. A # starts a comment for a person. Run the following cells separately. After the first cell, readings refers to 12. The second reads the current value, adds 5, then stores the answer under the same name.

Complete practice code:
readings = 12
# Run the next two lines in a SECOND cell.
readings = readings + 5
print(readings)

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

WALK THROUGH THIS CODE
print displays a value below the cell.
= assigns the value on the right to the name on the left.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Expected output. Move on after a learner can explain the current example or required action.

## Slide 19 — Expected output

TEACHING PURPOSE
Expected output

CONNECT
Build on the preceding slide: Worked example.

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Runtime. Move on after a learner can explain the current example or required action.

## Slide 20 — Runtime

TEACHING PURPOSE
Runtime

CONNECT
Build on the preceding slide: Expected output.

EXPLAIN IN ORDINARY WORDS
A value is a piece of information. A variable is a name referring to a value. In length_m = 5, Python evaluates the right side and binds that result to the name on the left.

CHECK AND EXPECTED ANSWER
After x=3 then x=5, what does print(x) display? 5. The earlier value is not added automatically.

IF LEARNERS ARE STUCK
Write the name on a card and the current value beside it. Distinguish number 3 from quoted text "3".

POINT TO THE DEFINITION
Runtime: The running Python session and its current memory. Restarting clears variables. Downloading the notebook saves the document, not the whole running computer.

NEXT
Execution order changes the result. Move on after a learner can explain the current example or required action.

## Slide 21 — Execution order changes the result

TEACHING PURPOSE
Execution order changes the result

CONNECT
Build on the preceding slide: Runtime.

LECTURER CUE
Trace 12 + 5 = 17, then 22, then 27. Restarting clears memory. Running the setup cell restores 12.
Source: existing course illustration figs/execution_trap.png. These are illustrative examples, not this cohort’s assessed results.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
You are the notebook’s memory. Move on after a learner can explain the current example or required action.

## Slide 22 — You are the notebook’s memory

TEACHING PURPOSE
You are the notebook’s memory

CONNECT
Build on the preceding slide: Execution order changes the result.

LECTURER CUE
Do this before revealing the discussion slide. One learner moves or writes the items, the other checks. Swap roles. Every student explains one step. Expected: 22. Re-running the setup first would replace the value with 12 again.
Wait for an individual prediction before inviting pair discussion. Give a first-step hint if needed.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
What the activity shows. Move on after a learner can explain the current example or required action.

## Slide 23 — What the activity shows

TEACHING PURPOSE
What the activity shows

CONNECT
Build on the preceding slide: You are the notebook’s memory.

LECTURER CUE
Ask which step produced this answer. Return to the concrete action if a learner cannot explain it. This is practice feedback, never a quiz key.

NEXT
Your turn. Move on after a learner can explain the current example or required action.

## Slide 24 — Your turn

TEACHING PURPOSE
Your turn

CONNECT
Build on the preceding slide: What the activity shows.

LECTURER CUE
Give silent thinking time, then let pairs discuss. Rotate who types. This is practice, not a graded quiz. Expected response: 22. Running the entire example from the top resets readings to 12, so a complete run ends at 17 every time.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

DISCUSSION KEY FOR THIS SLIDE
DISCUSS THE REASONING
Practice discussion
22. Running the entire example from the top resets readings to 12, so a complete run ends at 17 every time.
Which step produced this result? What changes if one input changes?
CML3113   Week 2   25
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
Practice discussion. Move on after a learner can explain the current example or required action.

## Slide 25 — Practice discussion

TEACHING PURPOSE
Practice discussion

CONNECT
Build on the preceding slide: Your turn.

LECTURER CUE
Ask how the result was obtained. Reteach the smallest missing step instead of giving a longer lecture.

NEXT
Save a copy you can find again. Move on after a learner can explain the current example or required action.

## Slide 26 — Save a copy you can find again

TEACHING PURPOSE
Save a copy you can find again

CONNECT
Build on the preceding slide: Practice discussion.

EXPLAIN IN ORDINARY WORDS
A CSV is a text table. The header supplies column names. With csv.DictReader, values start as text, even if they look like numbers. A path tells Python where the file is.

CHECK AND EXPECTED ANSWER
Can "2.5" from csv.DictReader be added as a number without conversion? No; convert valid numeric text first.

IF LEARNERS ARE STUCK
Show the file in the runtime folder and compare its exact filename, case and column headers. Upload data again after a fresh Colab runtime.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
The words in the repair exercises. Move on after a learner can explain the current example or required action.

## Slide 27 — The words in the repair exercises

TEACHING PURPOSE
The words in the repair exercises

CONNECT
Build on the preceding slide: Save a copy you can find again.

EXPLAIN IN ORDINARY WORDS
A module supplies Python tools; import asks Python to load it. A version identifies a software release. A path identifies a file. A state error happens when stored values differ from what we expected.

CHECK AND EXPECTED ANSWER
Notebook 04 starts at 12, adds 5 to get 17, then resets to 12. Why does it print 12? The final assignment overwrites 17.

IF LEARNERS ARE STUCK
01: the named module is deliberately unavailable; remove the unused import instead of trying to install a made-up package. 02: the exercise asserts Python 2 but the course uses Python 3; inspect sys.version_info and correct that deliberate mismatch. 03: upload the issued CSV and replace the nonexistent folder path with its real filename. 04: remove the unwanted reset, restart and run all for 17; repeat only the increment to see 22, then 27.

POINT TO THE DEFINITION
Module and version: A module is a collection of Python tools. import asks for it. A version identifies a software release; different releases can behave differently.
Path and working folder: A path tells Python where a file is. A bare filename is looked up in the current working folder. The runtime Files panel shows uploaded files.

NEXT
Your cohort data. Move on after a learner can explain the current example or required action.

## Slide 28 — Your cohort data

TEACHING PURPOSE
Your cohort data

CONNECT
Build on the preceding slide: The words in the repair exercises.

EXPLAIN IN ORDINARY WORDS
A CSV is a text table. The header supplies column names. With csv.DictReader, values start as text, even if they look like numbers. A path tells Python where the file is.

CHECK AND EXPECTED ANSWER
Can "2.5" from csv.DictReader be added as a number without conversion? No; convert valid numeric text first.

IF LEARNERS ARE STUCK
Show the file in the runtime folder and compare its exact filename, case and column headers. Upload data again after a fresh Colab runtime.

NEXT
The four repair exercises. Move on after a learner can explain the current example or required action.

## Slide 29 — The four repair exercises

TEACHING PURPOSE
The four repair exercises

CONNECT
Build on the preceding slide: Your cohort data.

EXPLAIN IN ORDINARY WORDS
A module supplies Python tools; import asks Python to load it. A version identifies a software release. A path identifies a file. A state error happens when stored values differ from what we expected.

CHECK AND EXPECTED ANSWER
Notebook 04 starts at 12, adds 5 to get 17, then resets to 12. Why does it print 12? The final assignment overwrites 17.

IF LEARNERS ARE STUCK
01: the named module is deliberately unavailable; remove the unused import instead of trying to install a made-up package. 02: the exercise asserts Python 2 but the course uses Python 3; inspect sys.version_info and correct that deliberate mismatch. 03: upload the issued CSV and replace the nonexistent folder path with its real filename. 04: remove the unwanted reset, restart and run all for 17; repeat only the increment to see 22, then 27.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Repository and commit. Move on after a learner can explain the current example or required action.

## Slide 30 — Repository and commit

TEACHING PURPOSE
Repository and commit

CONNECT
Build on the preceding slide: The four repair exercises.

EXPLAIN IN ORDINARY WORDS
A repository is the project folder and recorded history. A commit records a chosen change; uploading or pushing shares it. A README tells someone else how to run the work.

CHECK AND EXPECTED ANSWER
Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.

IF LEARNERS ARE STUCK
Ask a partner to follow only the README. It should identify the data, files, run order and expected result. Keep secrets out of the repository.

POINT TO THE DEFINITION
Repository and commit: A repository stores a project and its recorded changes. A commit records a change with a message. Git tracks history; GitHub hosts repositories online.

NEXT
Record a change in your repository. Move on after a learner can explain the current example or required action.

## Slide 31 — Record a change in your repository

TEACHING PURPOSE
Record a change in your repository

CONNECT
Build on the preceding slide: Repository and commit.

EXPLAIN IN ORDINARY WORDS
A repository is the project folder and recorded history. A commit records a chosen change; uploading or pushing shares it. A README tells someone else how to run the work.

CHECK AND EXPECTED ANSWER
Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.

IF LEARNERS ARE STUCK
Ask a partner to follow only the README. It should identify the data, files, run order and expected result. Keep secrets out of the repository.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Short explainer and discussion. Move on after a learner can explain the current example or required action.

## Slide 32 — Short explainer and discussion

TEACHING PURPOSE
Short explainer and discussion

CONNECT
Build on the preceding slide: Record a change in your repository.

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

## Slide 33 — After the video

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

## Slide 34 — Preparing for the assignment

TEACHING PURPOSE
Preparing for the assignment

CONNECT
Build on the preceding slide: After the video.

LECTURER CUE
Use proof_of_life.ipynb for A2. Upload the cohort CSV into the runtime Files area and show the filename before reading it. Model repair 01, guide 02–03 and trace 04. Submit the completed main notebook and your own README.md together, plus the repository URL. Repairs 01–04 and hello_engineering.py are practice, not extra submissions.

EXPLAIN IN ORDINARY WORDS
A CSV is a text table. The header supplies column names. With csv.DictReader, values start as text, even if they look like numbers. A path tells Python where the file is.

CHECK AND EXPECTED ANSWER
Can "2.5" from csv.DictReader be added as a number without conversion? No; convert valid numeric text first.

IF LEARNERS ARE STUCK
Show the file in the runtime folder and compare its exact filename, case and column headers. Upload data again after a fresh Colab runtime.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Preparing for the assignment continued. Move on after a learner can explain the current example or required action.

## Slide 35 — Preparing for the assignment continued

TEACHING PURPOSE
Preparing for the assignment continued

CONNECT
Build on the preceding slide: Preparing for the assignment.

LECTURER CUE
Use proof_of_life.ipynb for A2. Upload the cohort CSV into the runtime Files area and show the filename before reading it. Model repair 01, guide 02–03 and trace 04. Submit the completed main notebook and your own README.md together, plus the repository URL. Repairs 01–04 and hello_engineering.py are practice, not extra submissions.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Execution order and saved changes. Move on after a learner can explain the current example or required action.

## Slide 36 — Execution order and saved changes

TEACHING PURPOSE
Execution order and saved changes

CONNECT
Build on the preceding slide: Preparing for the assignment continued.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Execution order and saved changes continued. Move on after a learner can explain the current example or required action.

## Slide 37 — Execution order and saved changes continued

TEACHING PURPOSE
Execution order and saved changes continued

CONNECT
Build on the preceding slide: Execution order and saved changes.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
A1 — what to write and submit. Move on after a learner can explain the current example or required action.

## Slide 38 — A1 — what to write and submit

TEACHING PURPOSE
A1 — what to write and submit

CONNECT
Build on the preceding slide: Execution order and saved changes continued.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Week 1 Assignment A1 catch-up upload. Move on after a learner can explain the current example or required action.

## Slide 39 — Week 1 Assignment A1 catch-up upload

TEACHING PURPOSE
Week 1 Assignment A1 catch-up upload

CONNECT
Build on the preceding slide: A1 — what to write and submit.

LECTURER CUE
Week 1 collection is permitted; existing marks remain protected and new written grading remains held until validated.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Week 1 Quiz 1 catch-up. Move on after a learner can explain the current example or required action.

## Slide 40 — Week 1 Quiz 1 catch-up

TEACHING PURPOSE
Week 1 Quiz 1 catch-up

CONNECT
Build on the preceding slide: Week 1 Assignment A1 catch-up upload.

LECTURER CUE
In Quiz Controls run open_W1_CML3113 when ready to give the full 24-hour window. Announce the exact logged deadline. Opening this link does not activate the quiz.

QUIZ OPERATION
Opening the student link does not activate the quiz. In Quiz Controls run the matching open_W<week>_<cohort> function once when ready. Announce the logged closing time: 24 hours after activation. Five minutes describes expected answering time, not the availability window. Quiz 1 and Quiz 2 require separate activation when collecting catch-up work.

NEXT
Week 2 assignment. Move on after a learner can explain the current example or required action.

## Slide 41 — Week 2 assignment

TEACHING PURPOSE
Week 2 assignment

CONNECT
Build on the preceding slide: Week 1 Quiz 1 catch-up.

LECTURER CUE
# A2 Proof of life
Full assessment requirements belong in the current public task guide; explain only the criterion or task shown on this slide.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Proof of life submission. Move on after a learner can explain the current example or required action.

## Slide 42 — Proof of life submission

TEACHING PURPOSE
Proof of life submission

CONNECT
Build on the preceding slide: Week 2 assignment.

LECTURER CUE
The form link is cohort-specific. Recheck the live form and release status before class. These scheduled assignment dates are separate from the quiz activation window. The issued brief defines the required files, even if the form accepts additional formats. Source: data/submission_links.json

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Week 2 quiz. Move on after a learner can explain the current example or required action.

## Slide 43 — Week 2 quiz

TEACHING PURPOSE
Week 2 quiz

CONNECT
Build on the preceding slide: Proof of life submission.

LECTURER CUE
Activate the matching open_W2_CML3113 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

QUIZ OPERATION
Opening the student link does not activate the quiz. In Quiz Controls run the matching open_W<week>_<cohort> function once when ready. Announce the logged closing time: 24 hours after activation. Five minutes describes expected answering time, not the availability window. Quiz 1 and Quiz 2 require separate activation when collecting catch-up work.

NEXT
Before you leave. Move on after a learner can explain the current example or required action.

## Slide 44 — Before you leave

TEACHING PURPOSE
Before you leave

CONNECT
Build on the preceding slide: Week 2 quiz.

LECTURER CUE
Ask every learner for an individual response. Record one misconception to revisit at the start of the next class. If a deadline changed, announce the exact Kampala date and update the source registry before rebuilding slides.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.
