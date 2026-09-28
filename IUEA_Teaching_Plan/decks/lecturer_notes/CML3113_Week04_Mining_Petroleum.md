# CML3113 Week04 Mining Petroleum

Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.

## Slide 1 — Lists loops and reading a table

TEACHING PURPOSE
Lists loops and reading a table

LECTURER CUE
Use PowerPoint Presenter View for these notes. Teach one example, pause for every learner to predict, then work an analogous example together. The practice notebook is a learning aid, not an extra graded upload.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

NEXT
Today’s learning. Move on after a learner can explain the current example or required action.

## Slide 2 — Today’s learning

TEACHING PURPOSE
Today’s learning

CONNECT
Build on the preceding slide: Lists loops and reading a table.

LECTURER CUE
Ask learners to explain this goal in ordinary language. The first successful attempt matters more than covering optional extensions. Defer: Nested comprehensions, arbitrary exception handling, a blank-page investigation and data-source hunting are later practice. Never use except: pass to silently erase evidence.

EXPLAIN IN ORDINARY WORDS
A CSV is a text table. The header supplies column names. With csv.DictReader, values start as text, even if they look like numbers. A path tells Python where the file is.

CHECK AND EXPECTED ANSWER
Can "2.5" from csv.DictReader be added as a number without conversion? No; convert valid numeric text first.

IF LEARNERS ARE STUCK
Show the file in the runtime folder and compare its exact filename, case and column headers. Upload data again after a fresh Colab runtime.

NEXT
Recall and a first attempt. Move on after a learner can explain the current example or required action.

## Slide 3 — Recall and a first attempt

TEACHING PURPOSE
Recall and a first attempt

CONNECT
Build on the preceding slide: Today’s learning.

LECTURER CUE
Allow two minutes for everyone to try. Ask pairs to compare. If many cannot begin, show the first step and repeat with changed values. Checkpoint for today: Students trace the running total without executing and identify the numeric field in the real CSV. Revisit a three-item list if either step fails.

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
A pump team records temperature to investigate operation. Mining students can relate this to a dewatering pump; petroleum students to a transfer pump. These are teaching examples, not operating limits.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
List and index. Move on after a learner can explain the current example or required action.

## Slide 5 — List and index

TEACHING PURPOSE
List and index

CONNECT
Build on the preceding slide: The engineering context.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

POINT TO THE DEFINITION
List and index: A list holds values in order: [2, 4, 6]. Square brackets select a position. readings[0] selects the first item, 2.

NEXT
A list position starts at zero. Move on after a learner can explain the current example or required action.

## Slide 6 — A list position starts at zero

TEACHING PURPOSE
A list position starts at zero

CONNECT
Build on the preceding slide: List and index.

LECTURER CUE
Draw three boxes labelled 0, 1 and 2 holding 2, 4 and 6. Read the first item aloud, then trace the loop by hand.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

NEXT
Read list operations. Move on after a learner can explain the current example or required action.

## Slide 7 — Read list operations

TEACHING PURPOSE
Read list operations

CONNECT
Build on the preceding slide: A list position starts at zero.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

POINT TO THE DEFINITION
append and len: readings.append(8) adds 8 to the end of the list. len(readings) counts its items. The dot selects an operation belonging to that object; parentheses call it.
Slice: readings[1:3] selects positions 1 and 2. The stop position 3 is excluded. A slice produces a new list; it does not remove items from the original.

NEXT
A list stores items in order. Move on after a learner can explain the current example or required action.

## Slide 8 — A list stores items in order

TEACHING PURPOSE
A list stores items in order

CONNECT
Build on the preceding slide: Read list operations.

LECTURER CUE
Read each symbol before running. Ask everyone to predict. Expected output: 2 then 4 then [4, 6]. readings[4] would raise IndexError.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

WALK THROUGH THIS CODE
print displays a value below the cell.
append adds one item to the end of a list.
Square brackets create a list or select an item.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Loop and iteration. Move on after a learner can explain the current example or required action.

## Slide 9 — Loop and iteration

TEACHING PURPOSE
Loop and iteration

CONNECT
Build on the preceding slide: A list stores items in order.

EXPLAIN IN ORDINARY WORDS
A loop repeats its indented instructions for each item. A running total must be initialised before the loop and updated inside it.

CHECK AND EXPECTED ANSWER
For values 2,4,6 and total initially 0, what are the successive totals? 2,6,12.

IF LEARNERS ARE STUCK
Use a trace table with current item and total. Resetting total inside the loop loses earlier additions.

POINT TO THE DEFINITION
Loop and iteration: A for loop runs its indented body once per item. Each pass is one iteration.

NEXT
Accumulator. Move on after a learner can explain the current example or required action.

## Slide 10 — Accumulator

TEACHING PURPOSE
Accumulator

CONNECT
Build on the preceding slide: Loop and iteration.

EXPLAIN IN ORDINARY WORDS
A loop repeats its indented instructions for each item. A running total must be initialised before the loop and updated inside it.

CHECK AND EXPECTED ANSWER
For values 2,4,6 and total initially 0, what are the successive totals? 2,6,12.

IF LEARNERS ARE STUCK
Use a trace table with current item and total. Resetting total inside the loop loses earlier additions.

POINT TO THE DEFINITION
Accumulator: A running total. Set it to zero before the loop, add inside the loop, and read the final total afterward.

NEXT
A loop repeats an indented block. Move on after a learner can explain the current example or required action.

## Slide 11 — A loop repeats an indented block

TEACHING PURPOSE
A loop repeats an indented block

CONNECT
Build on the preceding slide: Accumulator.

LECTURER CUE
Trace the native loop table that follows. Predict total after each item. An empty list needs a guard before dividing by its length.

EXPLAIN IN ORDINARY WORDS
A loop repeats its indented instructions for each item. A running total must be initialised before the loop and updated inside it.

CHECK AND EXPECTED ANSWER
For values 2,4,6 and total initially 0, what are the successive totals? 2,6,12.

IF LEARNERS ARE STUCK
Use a trace table with current item and total. Resetting total inside the loop loses earlier additions.

NEXT
A mean uses a total and a count. Move on after a learner can explain the current example or required action.

## Slide 12 — A mean uses a total and a count

TEACHING PURPOSE
A mean uses a total and a count

CONNECT
Build on the preceding slide: A loop repeats an indented block.

LECTURER CUE
Make a table with columns reading and total: (2,2), (4,6), (6,12). len(readings) counts three items. 12 / 3 is 4.

EXPLAIN IN ORDINARY WORDS
A combined mean is the combined total divided by the combined count. Averaging group means equally gives each group equal influence regardless of size.

CHECK AND EXPECTED ANSWER
Group A: one value 10; group B: three values 2. Overall mean is 16/4=4, not (10+2)/2=6.

IF LEARNERS ARE STUCK
Recover each group total as mean times count, add totals, then divide by all observations.

NEXT
A loop changes the running total. Move on after a learner can explain the current example or required action.

## Slide 13 — A loop changes the running total

TEACHING PURPOSE
A loop changes the running total

CONNECT
Build on the preceding slide: A mean uses a total and a count.

LECTURER CUE
The displayed mean is rounded to two decimals. Keep full precision in calculations. This larger illustration follows the same rule as our smaller 2, 4, 6 example.
Source: existing course illustration figs/accumulator_trace.png. These are illustrative examples, not this cohort’s assessed results.

EXPLAIN IN ORDINARY WORDS
A loop repeats its indented instructions for each item. A running total must be initialised before the loop and updated inside it.

CHECK AND EXPECTED ANSWER
For values 2,4,6 and total initially 0, what are the successive totals? 2,6,12.

IF LEARNERS ARE STUCK
Use a trace table with current item and total. Resetting total inside the loop loses earlier additions.

NEXT
Tracing the loop. Move on after a learner can explain the current example or required action.

## Slide 14 — Tracing the loop

TEACHING PURPOSE
Tracing the loop

CONNECT
Build on the preceding slide: A loop changes the running total.

LECTURER CUE
There are three readings. The mean is 12 / 3 = 4. Reset total before repeating the calculation.

EXPLAIN IN ORDINARY WORDS
A loop repeats its indented instructions for each item. A running total must be initialised before the loop and updated inside it.

CHECK AND EXPECTED ANSWER
For values 2,4,6 and total initially 0, what are the successive totals? 2,6,12.

IF LEARNERS ARE STUCK
Use a trace table with current item and total. Resetting total inside the loop loses earlier additions.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
Worked example. Move on after a learner can explain the current example or required action.

## Slide 15 — Worked example

TEACHING PURPOSE
Worked example

CONNECT
Build on the preceding slide: Tracing the loop.

LECTURER CUE
Draw three boxes labelled 0, 1 and 2 holding 2, 4 and 6. Read the first item aloud, then trace the loop by hand. Make a table with columns reading and total: (2,2), (4,6), (6,12). len(readings) counts three items. 12 / 3 is 4. Before a real CSV, show a two-line text extract and name its header. Open the issued CSV together. Explain csv.DictReader as one dictionary per row. Convert only the numeric column and state what should happen to an invalid value.

Complete practice code:
readings = [2, 4, 6]
total = 0
for reading in readings:
    total = total + reading
mean = total / len(readings)
print(mean)

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

WALK THROUGH THIS CODE
for takes the next item. The indented block repeats.
print displays a value below the cell.
Square brackets create a list or select an item.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Expected output. Move on after a learner can explain the current example or required action.

## Slide 16 — Expected output

TEACHING PURPOSE
Expected output

CONNECT
Build on the preceding slide: Worked example.

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

NEXT
Dictionary. Move on after a learner can explain the current example or required action.

## Slide 17 — Dictionary

TEACHING PURPOSE
Dictionary

CONNECT
Build on the preceding slide: Expected output.

EXPLAIN IN ORDINARY WORDS
A dictionary pairs a key with a value. For {"unit":"A", "reading":4}, record["reading"] looks up the key and gives 4. The key is not a list position.

CHECK AND EXPECTED ANSWER
What happens if the key is spelled "Reading" instead? It is a different key; direct lookup can raise KeyError.

IF LEARNERS ARE STUCK
Point to each key and its value. Read the colon as associates-with, then do one exact lookup.

POINT TO THE DEFINITION
Dictionary: A collection of named values such as {"temperature_c": 25}. Access the value with row["temperature_c"].

NEXT
Read dictionary operations. Move on after a learner can explain the current example or required action.

## Slide 18 — Read dictionary operations

TEACHING PURPOSE
Read dictionary operations

CONNECT
Build on the preceding slide: Dictionary.

EXPLAIN IN ORDINARY WORDS
A dictionary pairs a key with a value. For {"unit":"A", "reading":4}, record["reading"] looks up the key and gives 4. The key is not a list position.

CHECK AND EXPECTED ANSWER
What happens if the key is spelled "Reading" instead? It is a different key; direct lookup can raise KeyError.

IF LEARNERS ARE STUCK
Point to each key and its value. Read the colon as associates-with, then do one exact lookup.

POINT TO THE DEFINITION
Key and lookup: A key is the name used to find a value. record["reading"] looks up that key. record.get("missing", 0) returns 0 if the key is absent.
items and paired names: record.items() supplies key/value pairs. for key, value in ... puts each pair into two names, then runs the indented block once for that pair.

NEXT
Dictionary lookups and list slices. Move on after a learner can explain the current example or required action.

## Slide 19 — Dictionary lookups and list slices

TEACHING PURPOSE
Dictionary lookups and list slices

CONNECT
Build on the preceding slide: Read dictionary operations.

LECTURER CUE
Read one row at a time and use a changed value. This is a syntax reference for the worked examples.

EXPLAIN IN ORDINARY WORDS
A dictionary pairs a key with a value. For {"unit":"A", "reading":4}, record["reading"] looks up the key and gives 4. The key is not a list position.

CHECK AND EXPECTED ANSWER
What happens if the key is spelled "Reading" instead? It is a different key; direct lookup can raise KeyError.

IF LEARNERS ARE STUCK
Point to each key and its value. Read the colon as associates-with, then do one exact lookup.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
A position and a key find different things. Move on after a learner can explain the current example or required action.

## Slide 20 — A position and a key find different things

TEACHING PURPOSE
A position and a key find different things

CONNECT
Build on the preceding slide: Dictionary lookups and list slices.

LECTURER CUE
Ask students to describe what they see before introducing terminology. Generated conceptual teaching illustration.  Source: figs/experiential/ASSET_SOURCES.md.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

NEXT
A dictionary gives each value a key. Move on after a learner can explain the current example or required action.

## Slide 21 — A dictionary gives each value a key

TEACHING PURPOSE
A dictionary gives each value a key

CONNECT
Build on the preceding slide: A position and a key find different things.

LECTURER CUE
Read each symbol before running. Ask everyone to predict. Expected output: 4, then 0, then unit A and reading 6. Dictionaries preserve insertion order, but access by key is the important distinction. An unknown key with [] raises KeyError.

EXPLAIN IN ORDINARY WORDS
A dictionary pairs a key with a value. For {"unit":"A", "reading":4}, record["reading"] looks up the key and gives 4. The key is not a list position.

CHECK AND EXPECTED ANSWER
What happens if the key is spelled "Reading" instead? It is a different key; direct lookup can raise KeyError.

IF LEARNERS ARE STUCK
Point to each key and its value. Read the colon as associates-with, then do one exact lookup.

WALK THROUGH THIS CODE
for takes the next item. The indented block repeats.
print displays a value below the cell.
Square brackets create a list or select an item.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Three ways to collect values. Move on after a learner can explain the current example or required action.

## Slide 22 — Three ways to collect values

TEACHING PURPOSE
Three ways to collect values

CONNECT
Build on the preceding slide: A dictionary gives each value a key.

LECTURER CUE
A dictionary uses key: value pairs, such as {"reading": 4}.

EXPLAIN IN ORDINARY WORDS
A dictionary pairs a key with a value. For {"unit":"A", "reading":4}, record["reading"] looks up the key and gives 4. The key is not a list position.

CHECK AND EXPECTED ANSWER
What happens if the key is spelled "Reading" instead? It is a different key; direct lookup can raise KeyError.

IF LEARNERS ARE STUCK
Point to each key and its value. Read the colon as associates-with, then do one exact lookup.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
CSV and header. Move on after a learner can explain the current example or required action.

## Slide 23 — CSV and header

TEACHING PURPOSE
CSV and header

CONNECT
Build on the preceding slide: Three ways to collect values.

EXPLAIN IN ORDINARY WORDS
A CSV is a text table. The header supplies column names. With csv.DictReader, values start as text, even if they look like numbers. A path tells Python where the file is.

CHECK AND EXPECTED ANSWER
Can "2.5" from csv.DictReader be added as a number without conversion? No; convert valid numeric text first.

IF LEARNERS ARE STUCK
Show the file in the runtime folder and compare its exact filename, case and column headers. Upload data again after a fresh Colab runtime.

POINT TO THE DEFINITION
CSV and header: CSV means comma-separated values. One line usually represents one record; a header names the columns. CSV numbers arrive as text and may need float conversion.

NEXT
One record at a time. Move on after a learner can explain the current example or required action.

## Slide 24 — One record at a time

TEACHING PURPOSE
One record at a time

CONNECT
Build on the preceding slide: CSV and header.

EXPLAIN IN ORDINARY WORDS
A CSV is a text table. The header supplies column names. With csv.DictReader, values start as text, even if they look like numbers. A path tells Python where the file is.

CHECK AND EXPECTED ANSWER
Can "2.5" from csv.DictReader be added as a number without conversion? No; convert valid numeric text first.

IF LEARNERS ARE STUCK
Show the file in the runtime folder and compare its exact filename, case and column headers. Upload data again after a fresh Colab runtime.

NEXT
A CSV file has a header and text values. Move on after a learner can explain the current example or required action.

## Slide 25 — A CSV file has a header and text values

TEACHING PURPOSE
A CSV file has a header and text values

CONNECT
Build on the preceding slide: One record at a time.

LECTURER CUE
Read one row at a time and use a changed value. This is a syntax reference for the worked examples.

EXPLAIN IN ORDINARY WORDS
A CSV is a text table. The header supplies column names. With csv.DictReader, values start as text, even if they look like numbers. A path tells Python where the file is.

CHECK AND EXPECTED ANSWER
Can "2.5" from csv.DictReader be added as a number without conversion? No; convert valid numeric text first.

IF LEARNERS ARE STUCK
Show the file in the runtime folder and compare its exact filename, case and column headers. Upload data again after a fresh Colab runtime.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
A CSV row becomes a dictionary. Move on after a learner can explain the current example or required action.

## Slide 26 — A CSV row becomes a dictionary

TEACHING PURPOSE
A CSV row becomes a dictionary

CONNECT
Build on the preceding slide: A CSV file has a header and text values.

LECTURER CUE
Before a real CSV, show a two-line text extract and name its header. Open the issued CSV together. Explain csv.DictReader as one dictionary per row. Convert only the numeric column and state what should happen to an invalid value.

EXPLAIN IN ORDINARY WORDS
A CSV is a text table. The header supplies column names. With csv.DictReader, values start as text, even if they look like numbers. A path tells Python where the file is.

CHECK AND EXPECTED ANSWER
Can "2.5" from csv.DictReader be added as a number without conversion? No; convert valid numeric text first.

IF LEARNERS ARE STUCK
Show the file in the runtime folder and compare its exact filename, case and column headers. Upload data again after a fresh Colab runtime.

NEXT
with and import. Move on after a learner can explain the current example or required action.

## Slide 27 — with and import

TEACHING PURPOSE
with and import

CONNECT
Build on the preceding slide: A CSV row becomes a dictionary.

POINT TO THE DEFINITION
with and import: import makes library tools available. with open(...) opens a file for a block and closes it afterward. A filename must match an existing file in the working folder.

NEXT
Your cohort data. Move on after a learner can explain the current example or required action.

## Slide 28 — Your cohort data

TEACHING PURPOSE
Your cohort data

CONNECT
Build on the preceding slide: with and import.

EXPLAIN IN ORDINARY WORDS
A probability-like score and a class decision are different outputs. A threshold turns a score into an action. Lowering a warning threshold usually raises both detections and false alarms.

CHECK AND EXPECTED ANSWER
At a rule of score >= 0.5, what happens at 0.5? It is positive. With > 0.5 it would not be.

IF LEARNERS ARE STUCK
Mark three scores below, at and above the boundary. Do not promise the score is well calibrated without checking.

NEXT
Read the supplied CSV in four steps. Move on after a learner can explain the current example or required action.

## Slide 29 — Read the supplied CSV in four steps

TEACHING PURPOSE
Read the supplied CSV in four steps

CONNECT
Build on the preceding slide: Your cohort data.

EXPLAIN IN ORDINARY WORDS
A CSV is a text table. The header supplies column names. With csv.DictReader, values start as text, even if they look like numbers. A path tells Python where the file is.

CHECK AND EXPECTED ANSWER
Can "2.5" from csv.DictReader be added as a number without conversion? No; convert valid numeric text first.

IF LEARNERS ARE STUCK
Show the file in the runtime folder and compare its exact filename, case and column headers. Upload data again after a fresh Colab runtime.

NEXT
Open a real CSV and inspect its first row. Move on after a learner can explain the current example or required action.

## Slide 30 — Open a real CSV and inspect its first row

TEACHING PURPOSE
Open a real CSV and inspect its first row

CONNECT
Build on the preceding slide: Read the supplied CSV in four steps.

LECTURER CUE
Read the actual keys and text values. Check the uploaded filename if Python reports FileNotFoundError.

Complete practice code:
import csv
with open("drill_shift_log.csv", newline="") as source:
    rows = list(csv.DictReader(source))
print(rows[0])
print(len(rows))

EXPLAIN IN ORDINARY WORDS
A CSV is a text table. The header supplies column names. With csv.DictReader, values start as text, even if they look like numbers. A path tells Python where the file is.

CHECK AND EXPECTED ANSWER
Can "2.5" from csv.DictReader be added as a number without conversion? No; convert valid numeric text first.

IF LEARNERS ARE STUCK
Show the file in the runtime folder and compare its exact filename, case and column headers. Upload data again after a fresh Colab runtime.

WALK THROUGH THIS CODE
import loads a library. from selects a tool from it.
print displays a value below the cell.
Square brackets create a list or select an item.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
A record and a growing list. Move on after a learner can explain the current example or required action.

## Slide 31 — A record and a growing list

TEACHING PURPOSE
A record and a growing list

CONNECT
Build on the preceding slide: Open a real CSV and inspect its first row.

LECTURER CUE
Braces pair a key with its value. append adds one value to the end of a list. The same pattern works after reading a CSV row.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

NEXT
A record and a growing list in Python. Move on after a learner can explain the current example or required action.

## Slide 32 — A record and a growing list in Python

TEACHING PURPOSE
A record and a growing list in Python

CONNECT
Build on the preceding slide: A record and a growing list.

LECTURER CUE
Braces pair a key with its value. append adds one value to the end of a list. The same pattern works after reading a CSV row.

Complete practice code:
records = [{"sensor": "A", "reading": "2.5"},
           {"sensor": "B", "reading": "3.5"}]
values = []
for row in records:
    values.append(float(row["reading"]))
print(values)

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

WALK THROUGH THIS CODE
for takes the next item. The indented block repeats.
float converts numeric text into a decimal number.
print displays a value below the cell.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Skip a blank before converting text. Move on after a learner can explain the current example or required action.

## Slide 33 — Skip a blank before converting text

TEACHING PURPOSE
Skip a blank before converting text

CONNECT
Build on the preceding slide: A record and a growing list in Python.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
Collect only the recorded numbers. Move on after a learner can explain the current example or required action.

## Slide 34 — Collect only the recorded numbers

TEACHING PURPOSE
Collect only the recorded numbers

CONNECT
Build on the preceding slide: Skip a blank before converting text.

LECTURER CUE
Expected: 2 [2.5, 3.5]. A blank is missing, not a recorded zero.

Complete practice code:
text_values = ["2.5", "", "3.5"]
values = []
for text in text_values:
    if text != "":
        values.append(float(text))
print(len(values), values)

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

WALK THROUGH THIS CODE
for takes the next item. The indented block repeats.
if tests a condition. The chosen indented block runs.
float converts numeric text into a decimal number.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Summaries for separate groups. Move on after a learner can explain the current example or required action.

## Slide 35 — Summaries for separate groups

TEACHING PURPOSE
Summaries for separate groups

CONNECT
Build on the preceding slide: Collect only the recorded numbers.

LECTURER CUE
A dictionary can hold one running total for each group. An absent key needs an initial zero. Then add the reading to that group. To calculate group means, keep a matching count and divide each group total by its own count.

EXPLAIN IN ORDINARY WORDS
A combined mean is the combined total divided by the combined count. Averaging group means equally gives each group equal influence regardless of size.

CHECK AND EXPECTED ANSWER
Group A: one value 10; group B: three values 2. Overall mean is 16/4=4, not (10+2)/2=6.

IF LEARNERS ARE STUCK
Recover each group total as mean times count, add totals, then divide by all observations.

NEXT
Summaries for separate groups in Python (1/2). Move on after a learner can explain the current example or required action.

## Slide 36 — Summaries for separate groups in Python (1/2)

TEACHING PURPOSE
Summaries for separate groups in Python (1/2)

CONNECT
Build on the preceding slide: Summaries for separate groups.

LECTURER CUE
A dictionary can hold one running total for each group. An absent key needs an initial zero. Then add the reading to that group. To calculate group means, keep a matching count and divide each group total by its own count.

Complete practice code:
records = [{"group": "A", "reading": 2},
           {"group": "A", "reading": 4},
           {"group": "B", "reading": 9}]
totals = {}
for row in records:
    group = row["group"]
    if group not in totals:
        totals[group] = 0
    totals[group] = totals[group] + row["reading"]
print(totals)

WALK THROUGH THIS CODE
for takes the next item. The indented block repeats.
if tests a condition. The chosen indented block runs.
Square brackets create a list or select an item.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Summaries for separate groups in Python (2/2). Move on after a learner can explain the current example or required action.

## Slide 37 — Summaries for separate groups in Python (2/2)

TEACHING PURPOSE
Summaries for separate groups in Python (2/2)

CONNECT
Build on the preceding slide: Summaries for separate groups in Python (1/2).

LECTURER CUE
A dictionary can hold one running total for each group. An absent key needs an initial zero. Then add the reading to that group. To calculate group means, keep a matching count and divide each group total by its own count.

Complete practice code:
records = [{"group": "A", "reading": 2},
           {"group": "A", "reading": 4},
           {"group": "B", "reading": 9}]
totals = {}
for row in records:
    group = row["group"]
    if group not in totals:
        totals[group] = 0
    totals[group] = totals[group] + row["reading"]
print(totals)

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

WALK THROUGH THIS CODE
print displays a value below the cell.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
A group mean needs its own count. Move on after a learner can explain the current example or required action.

## Slide 38 — A group mean needs its own count

TEACHING PURPOSE
A group mean needs its own count

CONNECT
Build on the preceding slide: Summaries for separate groups in Python (2/2).

EXPLAIN IN ORDINARY WORDS
A combined mean is the combined total divided by the combined count. Averaging group means equally gives each group equal influence regardless of size.

CHECK AND EXPECTED ANSWER
Group A: one value 10; group B: three values 2. Overall mean is 16/4=4, not (10+2)/2=6.

IF LEARNERS ARE STUCK
Recover each group total as mean times count, add totals, then divide by all observations.

NEXT
From group totals to group means. Move on after a learner can explain the current example or required action.

## Slide 39 — From group totals to group means

TEACHING PURPOSE
From group totals to group means

CONNECT
Build on the preceding slide: A group mean needs its own count.

LECTURER CUE
Expected: A has mean 3.0 and B has mean 9.0. Each group uses its own denominator.

Complete practice code:
counts = {}
for row in records:
    group = row["group"]
    counts[group] = counts.get(group, 0) + 1
means = {}
for group, total in totals.items():
    means[group] = total / counts[group]
print(means)

EXPLAIN IN ORDINARY WORDS
A combined mean is the combined total divided by the combined count. Averaging group means equally gives each group equal influence regardless of size.

CHECK AND EXPECTED ANSWER
Group A: one value 10; group B: three values 2. Overall mean is 16/4=4, not (10+2)/2=6.

IF LEARNERS ARE STUCK
Recover each group total as mean times count, add totals, then divide by all observations.

WALK THROUGH THIS CODE
for takes the next item. The indented block repeats.
print displays a value below the cell.
Square brackets create a list or select an item.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
When numeric text cannot be converted. Move on after a learner can explain the current example or required action.

## Slide 40 — When numeric text cannot be converted

TEACHING PURPOSE
When numeric text cannot be converted

CONNECT
Build on the preceding slide: From group totals to group means.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Catch one expected conversion failure. Move on after a learner can explain the current example or required action.

## Slide 41 — Catch one expected conversion failure

TEACHING PURPOSE
Catch one expected conversion failure

CONNECT
Build on the preceding slide: When numeric text cannot be converted.

LECTURER CUE
Expected: None. The assignment specifies which invalid records to skip; do not invent a replacement number.

Complete practice code:
text = "bad"
try:
    reading = float(text)
except ValueError:
    reading = None
print(reading)

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

WALK THROUGH THIS CODE
float converts numeric text into a decimal number.
print displays a value below the cell.
= assigns the value on the right to the name on the left.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
You are the loop. Move on after a learner can explain the current example or required action.

## Slide 42 — You are the loop

TEACHING PURPOSE
You are the loop

CONNECT
Build on the preceding slide: Catch one expected conversion failure.

LECTURER CUE
Do this before revealing the discussion slide. One learner moves or writes the items, the other checks. Swap roles. Every student explains one step. Expected: The new total is 20 and count is 4, so the mean is 5. Resetting the total inside the loop loses earlier additions.
Wait for an individual prediction before inviting pair discussion. Give a first-step hint if needed.

EXPLAIN IN ORDINARY WORDS
A loop repeats its indented instructions for each item. A running total must be initialised before the loop and updated inside it.

CHECK AND EXPECTED ANSWER
For values 2,4,6 and total initially 0, what are the successive totals? 2,6,12.

IF LEARNERS ARE STUCK
Use a trace table with current item and total. Resetting total inside the loop loses earlier additions.

NEXT
What the activity shows. Move on after a learner can explain the current example or required action.

## Slide 43 — What the activity shows

TEACHING PURPOSE
What the activity shows

CONNECT
Build on the preceding slide: You are the loop.

LECTURER CUE
Ask which step produced this answer. Return to the concrete action if a learner cannot explain it. This is practice feedback, never a quiz key.

EXPLAIN IN ORDINARY WORDS
A loop repeats its indented instructions for each item. A running total must be initialised before the loop and updated inside it.

CHECK AND EXPECTED ANSWER
For values 2,4,6 and total initially 0, what are the successive totals? 2,6,12.

IF LEARNERS ARE STUCK
Use a trace table with current item and total. Resetting total inside the loop loses earlier additions.

NEXT
Your turn. Move on after a learner can explain the current example or required action.

## Slide 44 — Your turn

TEACHING PURPOSE
Your turn

CONNECT
Build on the preceding slide: What the activity shows.

LECTURER CUE
Give silent thinking time, then let pairs discuss. Rotate who types. This is practice, not a graded quiz. Expected response: Total 20, count 4, mean 5.0. Resetting inside the loop discards previous additions and leaves only the last value in total.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

DISCUSSION KEY FOR THIS SLIDE
DISCUSS THE REASONING
Practice discussion
Total 20, count 4, mean 5.0. Resetting inside the loop discards previous additions and leaves only the last value in total.
Which step produced this result? What changes if one input changes?
CML3113   Week 4   45
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
Practice discussion. Move on after a learner can explain the current example or required action.

## Slide 45 — Practice discussion

TEACHING PURPOSE
Practice discussion

CONNECT
Build on the preceding slide: Your turn.

LECTURER CUE
Ask how the result was obtained. Reteach the smallest missing step instead of giving a longer lecture.

EXPLAIN IN ORDINARY WORDS
A loop repeats its indented instructions for each item. A running total must be initialised before the loop and updated inside it.

CHECK AND EXPECTED ANSWER
For values 2,4,6 and total initially 0, what are the successive totals? 2,6,12.

IF LEARNERS ARE STUCK
Use a trace table with current item and total. Resetting total inside the loop loses earlier additions.

NEXT
Preparing for the assignment. Move on after a learner can explain the current example or required action.

## Slide 46 — Preparing for the assignment

TEACHING PURPOSE
Preparing for the assignment

CONNECT
Build on the preceding slide: Practice discussion.

LECTURER CUE
Open the issued W04 notebook and its cohort CSV. Compute the requested valid_count, mean_reading, above_limit and group_means using the exact names in the notebook. First identify the correct field and its unit. Keep the CSV beside the notebook locally or upload it into the Colab runtime. The written interpretation is practice.

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

## Slide 47 — Preparing for the assignment continued

TEACHING PURPOSE
Preparing for the assignment continued

CONNECT
Build on the preceding slide: Preparing for the assignment.

LECTURER CUE
Open the issued W04 notebook and its cohort CSV. Compute the requested valid_count, mean_reading, above_limit and group_means using the exact names in the notebook. First identify the correct field and its unit. Keep the CSV beside the notebook locally or upload it into the Colab runtime. The written interpretation is practice.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Counting every record honestly. Move on after a learner can explain the current example or required action.

## Slide 48 — Counting every record honestly

TEACHING PURPOSE
Counting every record honestly

CONNECT
Build on the preceding slide: Preparing for the assignment continued.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
A CSV is a text table. The header supplies column names. With csv.DictReader, values start as text, even if they look like numbers. A path tells Python where the file is.

CHECK AND EXPECTED ANSWER
Can "2.5" from csv.DictReader be added as a number without conversion? No; convert valid numeric text first.

IF LEARNERS ARE STUCK
Show the file in the runtime folder and compare its exact filename, case and column headers. Upload data again after a fresh Colab runtime.

NEXT
Counting every record honestly continued. Move on after a learner can explain the current example or required action.

## Slide 49 — Counting every record honestly continued

TEACHING PURPOSE
Counting every record honestly continued

CONNECT
Build on the preceding slide: Counting every record honestly.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

NEXT
Your issued assignment. Move on after a learner can explain the current example or required action.

## Slide 50 — Your issued assignment

TEACHING PURPOSE
Your issued assignment

CONNECT
Build on the preceding slide: Counting every record honestly continued.

LECTURER CUE
# Week 4 reading report
Read README.md. Keep units in your explanation.

## valid_count (5 marks)
Store an integer count of rows whose rate_of_penetration field is nonblank. Skip blank readings before numeric conversion.

## mean_reading (5 marks)
Store the arithmetic mean of the nonblank rate_of_penetration values as a number. Add the valid readings and divide by their count. Keep full precision.

## above_limit (5 marks)
Store an integer count of valid rate_of_penetration readings strictly greater than 8.0. A reading equal to the threshold is not counted.

## group_means (5 marks)
Store a dictionary whose keys are the bit_type labels and whose values are the mean valid rate_of_penetration readings within each group. Divide each group total by its own valid count. Keep full precision.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
valid_count (5 marks). Move on after a learner can explain the current example or required action.

## Slide 51 — valid_count (5 marks)

TEACHING PURPOSE
valid_count (5 marks)

CONNECT
Build on the preceding slide: Your issued assignment.

LECTURER CUE
# Week 4 reading report
Read README.md. Keep units in your explanation.

## valid_count (5 marks)
Store an integer count of rows whose rate_of_penetration field is nonblank. Skip blank readings before numeric conversion.

## mean_reading (5 marks)
Store the arithmetic mean of the nonblank rate_of_penetration values as a number. Add the valid readings and divide by their count. Keep full precision.

## above_limit (5 marks)
Store an integer count of valid rate_of_penetration readings strictly greater than 8.0. A reading equal to the threshold is not counted.

## group_means (5 marks)
Store a dictionary whose keys are the bit_type labels and whose values are the mean valid rate_of_penetration readings within each group. Divide each group total by its own valid count. Keep full precision.

EXPLAIN IN ORDINARY WORDS
A count says how much work there is. A rate divides events by the relevant opportunities or population. Both numerator and denominator must describe the same period and group.

CHECK AND EXPECTED ANSWER
10 returns from 100 orders versus 20 from 1,000: rates are 10% and 2%. The second group has more returns but a lower rate.

IF LEARNERS ARE STUCK
Write numerator and denominator in words before putting numbers into the fraction.

NEXT
mean_reading (5 marks). Move on after a learner can explain the current example or required action.

## Slide 52 — mean_reading (5 marks)

TEACHING PURPOSE
mean_reading (5 marks)

CONNECT
Build on the preceding slide: valid_count (5 marks).

LECTURER CUE
# Week 4 reading report
Read README.md. Keep units in your explanation.

## valid_count (5 marks)
Store an integer count of rows whose rate_of_penetration field is nonblank. Skip blank readings before numeric conversion.

## mean_reading (5 marks)
Store the arithmetic mean of the nonblank rate_of_penetration values as a number. Add the valid readings and divide by their count. Keep full precision.

## above_limit (5 marks)
Store an integer count of valid rate_of_penetration readings strictly greater than 8.0. A reading equal to the threshold is not counted.

## group_means (5 marks)
Store a dictionary whose keys are the bit_type labels and whose values are the mean valid rate_of_penetration readings within each group. Divide each group total by its own valid count. Keep full precision.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

NEXT
above_limit (5 marks). Move on after a learner can explain the current example or required action.

## Slide 53 — above_limit (5 marks)

TEACHING PURPOSE
above_limit (5 marks)

CONNECT
Build on the preceding slide: mean_reading (5 marks).

LECTURER CUE
# Week 4 reading report
Read README.md. Keep units in your explanation.

## valid_count (5 marks)
Store an integer count of rows whose rate_of_penetration field is nonblank. Skip blank readings before numeric conversion.

## mean_reading (5 marks)
Store the arithmetic mean of the nonblank rate_of_penetration values as a number. Add the valid readings and divide by their count. Keep full precision.

## above_limit (5 marks)
Store an integer count of valid rate_of_penetration readings strictly greater than 8.0. A reading equal to the threshold is not counted.

## group_means (5 marks)
Store a dictionary whose keys are the bit_type labels and whose values are the mean valid rate_of_penetration readings within each group. Divide each group total by its own valid count. Keep full precision.

EXPLAIN IN ORDINARY WORDS
A probability-like score and a class decision are different outputs. A threshold turns a score into an action. Lowering a warning threshold usually raises both detections and false alarms.

CHECK AND EXPECTED ANSWER
At a rule of score >= 0.5, what happens at 0.5? It is positive. With > 0.5 it would not be.

IF LEARNERS ARE STUCK
Mark three scores below, at and above the boundary. Do not promise the score is well calibrated without checking.

NEXT
group_means (5 marks). Move on after a learner can explain the current example or required action.

## Slide 54 — group_means (5 marks)

TEACHING PURPOSE
group_means (5 marks)

CONNECT
Build on the preceding slide: above_limit (5 marks).

LECTURER CUE
# Week 4 reading report
Read README.md. Keep units in your explanation.

## valid_count (5 marks)
Store an integer count of rows whose rate_of_penetration field is nonblank. Skip blank readings before numeric conversion.

## mean_reading (5 marks)
Store the arithmetic mean of the nonblank rate_of_penetration values as a number. Add the valid readings and divide by their count. Keep full precision.

## above_limit (5 marks)
Store an integer count of valid rate_of_penetration readings strictly greater than 8.0. A reading equal to the threshold is not counted.

## group_means (5 marks)
Store a dictionary whose keys are the bit_type labels and whose values are the mean valid rate_of_penetration readings within each group. Divide each group total by its own valid count. Keep full precision.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

NEXT
Week 4 rules. Move on after a learner can explain the current example or required action.

## Slide 55 — Week 4 rules

TEACHING PURPOSE
Week 4 rules

CONNECT
Build on the preceding slide: group_means (5 marks).

LECTURER CUE
Fictional teaching data. 300 records. Three blank rate_of_penetration values must be skipped in numerical summaries. Threshold 8.0 is a teaching assumption.

Compute valid_count, mean_reading, above_limit (strictly greater than 8.0) and group_means keyed by bit_type. Use standard-library csv and collections. Save a copy using your Student Registration Number with / replaced by _, followed by _W04.ipynb. STUDENT_ID in the starter code means Student Registration Number. Four checks carry five marks each. Explain the interesting pattern separately as formative practice.

EXPLAIN IN ORDINARY WORDS
A probability-like score and a class decision are different outputs. A threshold turns a score into an action. Lowering a warning threshold usually raises both detections and false alarms.

CHECK AND EXPECTED ANSWER
At a rule of score >= 0.5, what happens at 0.5? It is positive. With > 0.5 it would not be.

IF LEARNERS ARE STUCK
Mark three scores below, at and above the boundary. Do not promise the score is well calibrated without checking.

NEXT
Week 4 rules continued. Move on after a learner can explain the current example or required action.

## Slide 56 — Week 4 rules continued

TEACHING PURPOSE
Week 4 rules continued

CONNECT
Build on the preceding slide: Week 4 rules.

LECTURER CUE
Fictional teaching data. 300 records. Three blank rate_of_penetration values must be skipped in numerical summaries. Threshold 8.0 is a teaching assumption.

Compute valid_count, mean_reading, above_limit (strictly greater than 8.0) and group_means keyed by bit_type. Use standard-library csv and collections. Save a copy using your Student Registration Number with / replaced by _, followed by _W04.ipynb. STUDENT_ID in the starter code means Student Registration Number. Four checks carry five marks each. Explain the interesting pattern separately as formative practice.

EXPLAIN IN ORDINARY WORDS
A CSV is a text table. The header supplies column names. With csv.DictReader, values start as text, even if they look like numbers. A path tells Python where the file is.

CHECK AND EXPECTED ANSWER
Can "2.5" from csv.DictReader be added as a number without conversion? No; convert valid numeric text first.

IF LEARNERS ARE STUCK
Show the file in the runtime folder and compare its exact filename, case and column headers. Upload data again after a fresh Colab runtime.

NEXT
Week 4 rules continued. Move on after a learner can explain the current example or required action.

## Slide 57 — Week 4 rules continued

TEACHING PURPOSE
Week 4 rules continued

CONNECT
Build on the preceding slide: Week 4 rules continued.

LECTURER CUE
Fictional teaching data. 300 records. Three blank rate_of_penetration values must be skipped in numerical summaries. Threshold 8.0 is a teaching assumption.

Compute valid_count, mean_reading, above_limit (strictly greater than 8.0) and group_means keyed by bit_type. Use standard-library csv and collections. Save a copy using your Student Registration Number with / replaced by _, followed by _W04.ipynb. STUDENT_ID in the starter code means Student Registration Number. Four checks carry five marks each. Explain the interesting pattern separately as formative practice.

NEXT
Reading report submission. Move on after a learner can explain the current example or required action.

## Slide 58 — Reading report submission

TEACHING PURPOSE
Reading report submission

CONNECT
Build on the preceding slide: Week 4 rules continued.

LECTURER CUE
The form link is cohort-specific. Recheck the live form and release status before class. These scheduled assignment dates are separate from the quiz activation window. The issued brief defines the required files, even if the form accepts additional formats. Source: data/submission_links.json

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Week 4 quiz. Move on after a learner can explain the current example or required action.

## Slide 59 — Week 4 quiz

TEACHING PURPOSE
Week 4 quiz

CONNECT
Build on the preceding slide: Reading report submission.

LECTURER CUE
Activate the matching open_W4_CML3113 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

QUIZ OPERATION
Opening the student link does not activate the quiz. In Quiz Controls run the matching open_W<week>_<cohort> function once when ready. Announce the logged closing time: 24 hours after activation. Five minutes describes expected answering time, not the availability window. Quiz 1 and Quiz 2 require separate activation when collecting catch-up work.

NEXT
Before you leave. Move on after a learner can explain the current example or required action.

## Slide 60 — Before you leave

TEACHING PURPOSE
Before you leave

CONNECT
Build on the preceding slide: Week 4 quiz.

LECTURER CUE
Ask every learner for an individual response. Record one misconception to revisit at the start of the next class. If a deadline changed, announce the exact Kampala date and update the source registry before rebuilding slides.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

