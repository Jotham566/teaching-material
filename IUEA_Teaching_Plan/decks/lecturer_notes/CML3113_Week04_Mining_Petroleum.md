# CML3113 Week04 Mining Petroleum

Lecturer companion to the revised PowerPoint. Slide numbers match this edition. Explain the worked examples directly; revision checks are for individual study.

## Slide 1 — Lists loops and reading a table

PURPOSE
Lists loops and reading a table

CONNECT
Build on the preceding week. Explain why this example is needed before running it.

EXPLAIN
Mining and Petroleum Engineering

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Today’s learning.

## Slide 2 — Today’s learning

PURPOSE
Today’s learning

CONNECT
Build on Lists loops and reading a table. Explain why this example is needed before running it.

EXPLAIN
Read lists and dictionary fields.

Trace a loop, read CSV rows and calculate summaries.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Connection to the previous lesson.

## Slide 3 — Connection to the previous lesson

PURPOSE
Connection to the previous lesson

CONNECT
Build on Today’s learning. Explain why this example is needed before running it.

EXPLAIN
Week 3 introduced values, function inputs and results, conditions and list positions. Now we repeat a calculation across records, then organise those records by keys.

LECTURER DETAIL
TEACHING PURPOSE
Recall and a first attempt

CONNECT
Build on the preceding slide: Today’s learning.

LECTURER CUE

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

NEXT
The engineering context. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Why this week’s tools are needed.

## Slide 4 — Why this week’s tools are needed

PURPOSE
Why this week’s tools are needed

CONNECT
Build on Connection to the previous lesson. Explain why this example is needed before running it.

EXPLAIN
Sensor readings arrive as records in a CSV file. We first learn the Python collections and loops needed to read those records and summarise them.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
List and index.

## Slide 5 — List and index

PURPOSE
List and index

CONNECT
Build on Why this week’s tools are needed. Explain why this example is needed before running it.

EXPLAIN
List and index: A list holds values in order: [2, 4, 6]. Square brackets select a position. readings[0] selects the first item, 2.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A list position starts at zero.

## Slide 6 — A list position starts at zero

PURPOSE
A list position starts at zero

CONNECT
Build on List and index. Explain why this example is needed before running it.

EXPLAIN
In [2, 4, 6], position 0 holds 2.

Position 1 holds 4. Position 2 holds 6.

There is no position 3 in this three-item list.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Read list operations.

## Slide 7 — Read list operations

PURPOSE
Read list operations

CONNECT
Build on A list position starts at zero. Explain why this example is needed before running it.

EXPLAIN
append and len: readings.append(8) adds 8 to the end of the list. len(readings) counts its items. The dot selects an operation belonging to that object; parentheses call it.
Slice: readings[1:3] selects positions 1 and 2. The stop position 3 is excluded. A slice produces a new list; it does not remove items from the original.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A list stores items in order.

## Slide 8 — A list stores items in order

PURPOSE
A list stores items in order

CONNECT
Build on Read list operations. Explain why this example is needed before running it.

EXPLAIN
[] builds a list. Positions start at zero. The slice stops before position 3.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Loop and iteration.

## Slide 9 — Loop and iteration

PURPOSE
Loop and iteration

CONNECT
Build on A list stores items in order. Explain why this example is needed before running it.

EXPLAIN
Loop and iteration: A for loop runs its indented body once per item. Each pass is one iteration.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Accumulator.

## Slide 10 — Accumulator

PURPOSE
Accumulator

CONNECT
Build on Loop and iteration. Explain why this example is needed before running it.

EXPLAIN
Accumulator: A running total. Set it to zero before the loop, add inside the loop, and read the final total afterward.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A loop repeats an indented block.

## Slide 11 — A loop repeats an indented block

PURPOSE
A loop repeats an indented block

CONNECT
Build on Accumulator. Explain why this example is needed before running it.

EXPLAIN
for reading in readings: takes one item at a time.

The colon starts the block. Four spaces show which lines repeat.

A running total must start at zero before the loop.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A mean uses a total and a count.

## Slide 12 — A mean uses a total and a count

PURPOSE
A mean uses a total and a count

CONNECT
Build on A loop repeats an indented block. Explain why this example is needed before running it.

EXPLAIN
Start the total at 0. Add 2, then 4, then 6.

The final total is 12. The count is 3.

12 / 3 gives the mean 4. An empty list needs a separate rule.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A loop changes the running total.

## Slide 13 — A loop changes the running total

PURPOSE
A loop changes the running total

CONNECT
Build on A mean uses a total and a count. Explain why this example is needed before running it.

EXPLAIN
This illustration uses six separate readings. Next we trace the smaller list [2, 4, 6] using the same running-total rule.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Tracing the loop.

## Slide 14 — Tracing the loop

PURPOSE
Tracing the loop

CONNECT
Build on A loop changes the running total. Explain why this example is needed before running it.

EXPLAIN
There are three readings.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Worked example.

## Slide 15 — Lists loops and records in Python

PURPOSE
Lists loops and records in Python

CONNECT
Build on Tracing the loop. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Expected output.

## Slide 16 — Lists loops and records results

PURPOSE
Lists loops and records results

CONNECT
Build on Lists loops and records in Python. Explain why this example is needed before running it.

EXPLAIN
4.0

LECTURER DETAIL
TEACHING PURPOSE
Expected output

CONNECT
Build on the preceding slide: Worked example.

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

NEXT
Dictionary. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Built-in summaries of a list.

## Slide 17 — Built-in summaries of a list

PURPOSE
Built-in summaries of a list

CONNECT
Build on Lists loops and records results. Explain why this example is needed before running it.

EXPLAIN
Output: 12, 3, 2, 6. sum totals; len counts; min and max select the smallest and largest.

LECTURER DETAIL
Output: 12, 3, 2, 6. sum totals; len counts; min and max select the smallest and largest.

readings = [2, 4, 6]
print(sum(readings))
print(len(readings))
print(min(readings))
print(max(readings))

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A dictionary is a record with named fields.

## Slide 18 — A dictionary is a record with named fields

PURPOSE
A dictionary is a record with named fields

CONNECT
Build on Built-in summaries of a list. Explain why this example is needed before running it.

EXPLAIN
record = {"unit": "A", "reading": 4} stores two key–value pairs. Keys name fields; values hold the information.

Braces enclose the dictionary. A colon separates each key from its value and a comma separates pairs. Each key is unique.

record["reading"] returns 4. Unlike a list position, "reading" names the field we want.

LECTURER DETAIL


TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Reading and updating a dictionary.

## Slide 19 — Reading and updating a dictionary

PURPOSE
Reading and updating a dictionary

CONNECT
Build on A dictionary is a record with named fields. Explain why this example is needed before running it.

EXPLAIN
Output: 4, then 6, then 0. get uses the fallback only when that key is absent.

LECTURER DETAIL
Output: 4, then 6, then 0. get uses the fallback only when that key is absent.

record = {"unit": "A", "reading": 4}
print(record["reading"])
record["reading"] = 6
print(record["reading"])
print(record.get("missing", 0))

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Tuples and unpacking.

## Slide 20 — Tuples and unpacking

PURPOSE
Tuples and unpacking

CONNECT
Build on Reading and updating a dictionary. Explain why this example is needed before running it.

EXPLAIN
A tuple stores items in order. point = (2, 3) stores two coordinates; point[0] is 2. You cannot reassign point[0].

x, y = point gives the first item to x and the second to y. This is unpacking; the number of names must match the number of items.

A tuple prevents replacing its positions. It does not freeze the contents of a mutable object stored inside it.

LECTURER DETAIL


TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Unpacking a pair.

## Slide 21 — Unpacking a pair

PURPOSE
Unpacking a pair

CONNECT
Build on Tuples and unpacking. Explain why this example is needed before running it.

EXPLAIN
Output: 2, then 3.

LECTURER DETAIL
Output: 2, then 3.

point = (2, 3)
x, y = point
print(x)
print(y)

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A set remembers distinct items.

## Slide 22 — A set remembers distinct items

PURPOSE
A set remembers distinct items

CONNECT
Build on Unpacking a pair. Explain why this example is needed before running it.

EXPLAIN
A set is useful when the question is “Have we seen this ID?” It keeps one instance of each distinct item.

seen = set() creates an empty set. seen.add("A") adds an item. "A" in seen asks whether it is present.

Do not use a set when position or repeated readings matter. Sets cannot be indexed. {} creates an empty dictionary, not an empty set.

LECTURER DETAIL


TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Set membership and repeated IDs.

## Slide 23 — Set membership and repeated IDs

PURPOSE
Set membership and repeated IDs

CONNECT
Build on A set remembers distinct items. Explain why this example is needed before running it.

EXPLAIN
Output: 1, True, False. Adding the same ID twice keeps one distinct ID.

LECTURER DETAIL
Output: 1, True, False. Adding the same ID twice keeps one distinct ID.

seen = set()
seen.add("A")
seen.add("A")
print(len(seen))
print("A" in seen)
print("B" in seen)

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
How the four collections differ.

## Slide 24 — How the four collections differ

PURPOSE
How the four collections differ

CONNECT
Build on Set membership and repeated IDs. Explain why this example is needed before running it.

EXPLAIN
Choose by the question: ordered readings, named fields, fixed positions, or distinct IDs.

LECTURER DETAIL
Choose by the question: ordered readings, named fields, fixed positions, or distinct IDs.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Dictionary items and two loop names.

## Slide 25 — Dictionary items and two loop names

PURPOSE
Dictionary items and two loop names

CONNECT
Build on How the four collections differ. Explain why this example is needed before running it.

EXPLAIN
record.items() provides each key with its value as a pair. The loop unpacks each pair into the names key and value.

for key, value in record.items(): repeats the indented body for each field. Use .items() when both the label and its value are needed.

LECTURER DETAIL


TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Looping through named fields.

## Slide 26 — Looping through named fields

PURPOSE
Looping through named fields

CONNECT
Build on Dictionary items and two loop names. Explain why this example is needed before running it.

EXPLAIN
Output: unit A, then reading 6. The dictionary preserves insertion order.

LECTURER DETAIL
Output: unit A, then reading 6. The dictionary preserves insertion order.

record = {"unit": "A", "reading": 6}
for key, value in record.items():
    print(key, value)

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A position and a key find different things.

## Slide 27 — A position and a key find different things

PURPOSE
A position and a key find different things

CONNECT
Build on Looping through named fields. Explain why this example is needed before running it.

EXPLAIN
Both examples return 4. Explain how each lookup finds it.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
CSV and header.

## Slide 28 — CSV and header

PURPOSE
CSV and header

CONNECT
Build on A position and a key find different things. Explain why this example is needed before running it.

EXPLAIN
CSV and header: CSV means comma-separated values. One line usually represents one record; a header names the columns. CSV numbers arrive as text and may need float conversion.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
One record at a time.

## Slide 29 — One record at a time

PURPOSE
One record at a time

CONNECT
Build on CSV and header. Explain why this example is needed before running it.

EXPLAIN
A CSV is a text table with a header row.

DictReader uses that header for dictionary keys.

CSV cells begin as text, even when they look numeric.

float("2.5") converts text into the number 2.5.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A CSV file has a header and text values.

## Slide 30 — A CSV file has a header and text values

PURPOSE
A CSV file has a header and text values

CONNECT
Build on One record at a time. Explain why this example is needed before running it.

EXPLAIN
An empty field is empty text. Check the task’s rule before converting it.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A CSV row becomes a dictionary.

## Slide 31 — A CSV row becomes a dictionary

PURPOSE
A CSV row becomes a dictionary

CONNECT
Build on A CSV file has a header and text values. Explain why this example is needed before running it.

EXPLAIN
The header gives field names, such as unit and reading.

csv.DictReader returns one dictionary for each data row.

The value "2.5" starts as text. float("2.5") makes the number 2.5.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
with and import.

## Slide 32 — with and import

PURPOSE
with and import

CONNECT
Build on A CSV row becomes a dictionary. Explain why this example is needed before running it.

EXPLAIN
with and import: import makes library tools available. with open(...) opens a file for a block and closes it afterward. A filename must match an existing file in the working folder.

LECTURER DETAIL
TEACHING PURPOSE
with and import

CONNECT
Build on the preceding slide: A CSV row becomes a dictionary.

POINT TO THE DEFINITION
with and import: import makes library tools available. with open(...) opens a file for a block and closes it afterward. A filename must match an existing file in the working folder.

NEXT
Your cohort data. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Your cohort data.

## Slide 33 — Your cohort data

PURPOSE
Your cohort data

CONNECT
Build on with and import. Explain why this example is needed before running it.

EXPLAIN
drill_shift_log.csv

Summarise rate_of_penetration (m/hour); group by bit_type.

Read the issued task’s blank-value and threshold rules before calculating.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Read the supplied CSV in four steps.

## Slide 34 — Read the supplied CSV in four steps

PURPOSE
Read the supplied CSV in four steps

CONNECT
Build on Your cohort data. Explain why this example is needed before running it.

EXPLAIN
Place drill_shift_log.csv beside the notebook, or upload it in Colab’s Files panel.

import csv loads the CSV tools. newline="" lets the reader handle line endings. DictReader uses the header as dictionary keys.

list(...) collects the rows while the file is open. We inspect the first row and the count; the later assignment calculations are your work.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Open a real CSV and inspect its first row.

## Slide 35 — Open a real CSV and inspect its first row

PURPOSE
Open a real CSV and inspect its first row

CONNECT
Build on Read the supplied CSV in four steps. Explain why this example is needed before running it.

EXPLAIN
Read the actual keys and text values. Check the uploaded filename if Python reports FileNotFoundError.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A list of dictionaries.

## Slide 36 — A list of dictionaries

PURPOSE
A list of dictionaries

CONNECT
Build on Open a real CSV and inspect its first row. Explain why this example is needed before running it.

EXPLAIN
A record holds named fields for one observation. A list of records holds several observations in order.

records[0] selects the first dictionary. records[0]["reading"] then selects that dictionary’s reading field.

for row in records takes one dictionary at a time. row["reading"] retrieves that observation’s field; float converts numeric text when needed.

LECTURER DETAIL


TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A record and a growing list.

## Slide 37 — A record and a growing list

PURPOSE
A record and a growing list

CONNECT
Build on A list of dictionaries. Explain why this example is needed before running it.

EXPLAIN
Braces pair a key with its value. append adds one value to the end of a list.

The same pattern works after reading a CSV row.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A record and a growing list in Python.

## Slide 38 — A record and a growing list in Python

PURPOSE
A record and a growing list in Python

CONNECT
Build on A record and a growing list. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Skip a blank before converting text.

## Slide 39 — Skip a blank before converting text

PURPOSE
Skip a blank before converting text

CONNECT
Build on A record and a growing list in Python. Explain why this example is needed before running it.

EXPLAIN
An empty text field is "". The comparison != means “not equal to”. Only convert a value after the blank check passes.

In this example, values records valid numbers only. Its length is the valid count; the group summaries must use the same valid-record policy.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Collect only the recorded numbers.

## Slide 40 — Collect only the recorded numbers

PURPOSE
Collect only the recorded numbers

CONNECT
Build on Skip a blank before converting text. Explain why this example is needed before running it.

EXPLAIN
Expected: 2 [2.5, 3.5]. A blank is missing, not a recorded zero.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Summaries for separate groups.

## Slide 41 — Summaries for separate groups

PURPOSE
Summaries for separate groups

CONNECT
Build on Collect only the recorded numbers. Explain why this example is needed before running it.

EXPLAIN
A dictionary can hold one running total for each group.

An absent key needs an initial zero.

Then add the reading to that group.

To calculate group means, keep a matching count and divide each group total by its own count.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Summaries for separate groups in Python (1/2).

## Slide 42 — Summaries for separate groups in Python (1/2)

PURPOSE
Summaries for separate groups in Python (1/2)

CONNECT
Build on Summaries for separate groups. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Summaries for separate groups in Python (2/2).

## Slide 43 — Summaries for separate groups in Python (2/2)

PURPOSE
Summaries for separate groups in Python (2/2)

CONNECT
Build on Summaries for separate groups in Python (1/2). Explain why this example is needed before running it.

EXPLAIN
Continue the SAME cell; keep indentation. Run after all parts are entered.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A group mean needs its own count.

## Slide 44 — A group mean needs its own count

PURPOSE
A group mean needs its own count

CONNECT
Build on Summaries for separate groups in Python (2/2). Explain why this example is needed before running it.

EXPLAIN
The preceding loop calculated a total for each group. Count records in those same groups, then divide each group total by its own count.

items() supplies the group name and its total together. We use small invented records, not the assignment’s answers.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
From group totals to group means.

## Slide 45 — From group totals to group means

PURPOSE
From group totals to group means

CONNECT
Build on A group mean needs its own count. Explain why this example is needed before running it.

EXPLAIN
Expected: A has mean 3.0 and B has mean 9.0. Each group uses its own denominator.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
When numeric text cannot be converted.

## Slide 46 — When numeric text cannot be converted

PURPOSE
When numeric text cannot be converted

CONNECT
Build on From group totals to group means. Explain why this example is needed before running it.

EXPLAIN
float("bad") raises ValueError: the text does not represent a number. An exception interrupts ordinary execution.

try contains the operation that might fail. except ValueError runs only for that named failure. Indentation shows the two blocks.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Catch one expected conversion failure.

## Slide 47 — Catch one expected conversion failure

PURPOSE
Catch one expected conversion failure

CONNECT
Build on When numeric text cannot be converted. Explain why this example is needed before running it.

EXPLAIN
Expected: None. The assignment specifies which invalid records to skip; do not invent a replacement number.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Revision example and answer.

## Slide 48 — Revision example and answer

PURPOSE
Revision example and answer

CONNECT
Build on Catch one expected conversion failure. Explain why this example is needed before running it.

EXPLAIN
Example: Add 8 to the list. Trace the new total and count before running. What happens if total = 0 is moved inside the loop?

Answer: Total 20, count 4, mean 5.0. Resetting inside the loop discards previous additions and leaves only the last value in total.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Preparing for the assignment.

## Slide 49 — Preparing for the assignment

PURPOSE
Preparing for the assignment

CONNECT
Build on Revision example and answer. Explain why this example is needed before running it.

EXPLAIN
Open the issued W04 notebook and its cohort CSV.

Compute the requested valid_count, mean_reading, above_limit and group_means using the exact names in the notebook.

First identify the correct field and its unit.

Keep the CSV beside the notebook locally or upload it into the Colab runtime.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Preparing for the assignment continued.

## Slide 50 — Preparing for the assignment continued

PURPOSE
Preparing for the assignment continued

CONNECT
Build on Preparing for the assignment. Explain why this example is needed before running it.

EXPLAIN
The written interpretation is practice.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Counting every record honestly.

## Slide 51 — Counting every record honestly

PURPOSE
Counting every record honestly

CONNECT
Build on Preparing for the assignment continued. Explain why this example is needed before running it.

EXPLAIN
DictReader already consumes the header; skipping its first yielded row skips real data.

A string such as "unknown" cannot be converted to float.

Catch the expected conversion error, count and record it, then continue under a stated policy.

Inspect whether skipped rows share a source before reporting a mean.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Counting every record honestly continued.

## Slide 52 — Counting every record honestly continued

PURPOSE
Counting every record honestly continued

CONNECT
Build on Counting every record honestly. Explain why this example is needed before running it.

EXPLAIN
A sample summary describes observed records, not every possible operating condition.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Your issued assignment.

## Slide 53 — Your issued assignment

PURPOSE
Your issued assignment

CONNECT
Build on Counting every record honestly continued. Explain why this example is needed before running it.

EXPLAIN
Open W04_student.ipynb.

Read every task and its input units before coding.

Keep the required function names and returned outputs.

Run the supplied visible checks, then restart and run all.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
valid_count (5 marks).

## Slide 54 — valid_count (5 marks)

PURPOSE
valid_count (5 marks)

CONNECT
Build on Your issued assignment. Explain why this example is needed before running it.

EXPLAIN
Store an integer count of rows whose rate_of_penetration field is nonblank.

Skip blank readings before numeric conversion.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
mean_reading (5 marks).

## Slide 55 — mean_reading (5 marks)

PURPOSE
mean_reading (5 marks)

CONNECT
Build on valid_count (5 marks). Explain why this example is needed before running it.

EXPLAIN
Store the arithmetic mean of the nonblank rate_of_penetration values as a number.

Add the valid readings and divide by their count.

Keep full precision.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
above_limit (5 marks).

## Slide 56 — above_limit (5 marks)

PURPOSE
above_limit (5 marks)

CONNECT
Build on mean_reading (5 marks). Explain why this example is needed before running it.

EXPLAIN
Store an integer count of valid rate_of_penetration readings strictly greater than 8.0.

A reading equal to the threshold is not counted.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
group_means (5 marks).

## Slide 57 — group_means (5 marks)

PURPOSE
group_means (5 marks)

CONNECT
Build on above_limit (5 marks). Explain why this example is needed before running it.

EXPLAIN
Store a dictionary whose keys are the bit_type labels and whose values are the mean valid rate_of_penetration readings within each group.

Divide each group total by its own valid count.

Keep full precision.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Week 4 rules.

## Slide 58 — Week 4 rules

PURPOSE
Week 4 rules

CONNECT
Build on group_means (5 marks). Explain why this example is needed before running it.

EXPLAIN
Fictional teaching data.

300 records.

Three blank rate_of_penetration values must be skipped in numerical summaries.

Threshold 8.0 is a teaching assumption.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Week 4 rules continued.

## Slide 59 — Week 4 rules continued

PURPOSE
Week 4 rules continued

CONNECT
Build on Week 4 rules. Explain why this example is needed before running it.

EXPLAIN
Compute valid_count, mean_reading, above_limit (strictly greater than 8.0) and group_means keyed by bit_type.

Use standard-library csv and collections.

Save a copy using your Student Registration Number with / replaced by _, followed by _W04.ipynb.

STUDENT_ID in the starter code means Student Registration Number.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Week 4 rules continued.

## Slide 60 — Week 4 rules continued

PURPOSE
Week 4 rules continued

CONNECT
Build on Week 4 rules continued. Explain why this example is needed before running it.

EXPLAIN
Four checks carry five marks each.

Explain the interesting pattern separately as formative practice.

For beginner step-by-step help, open ASSIGNMENT_INSTRUCTIONS.txt and STUDENT_HOW_TO.md in this folder.

The first names your required files and hand-in checklist; the second explains accounts, Colab, saving and uploads.

LECTURER DETAIL
TEACHING PURPOSE
Week 4 rules continued

CONNECT
Build on the preceding slide: Week 4 rules continued.

LECTURER CUE
Fictional teaching data. 300 records. Three blank rate_of_penetration values must be skipped in numerical summaries. Threshold 8.0 is a teaching assumption.

Compute valid_count, mean_reading, above_limit (strictly greater than 8.0) and group_means keyed by bit_type. Use standard-library csv and collections. Save a copy using your Student Registration Number with / replaced by _, followed by _W04.ipynb. STUDENT_ID in the starter code means Student Registration Number. Four checks carry five marks each. Explain the interesting pattern separately as formative practice.

NEXT
Reading report submission. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Reading report submission.

## Slide 61 — Reading report submission

PURPOSE
Reading report submission

CONNECT
Build on Week 4 rules continued. Explain why this example is needed before running it.

EXPLAIN
Opens: 02 Oct 2026, 08:00 Kampala

Deadline: 09 Oct 2026, 08:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Week 4 quiz.

## Slide 62 — Week 4 quiz

PURPOSE
Week 4 quiz

CONNECT
Build on Reading report submission. Explain why this example is needed before running it.

EXPLAIN
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

The lecturer will confirm the exact closing time.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Before you leave.

## Slide 63 — Revision and submission checklist

PURPOSE
Revision and submission checklist

CONNECT
Build on Week 4 quiz. Explain why this example is needed before running it.

EXPLAIN
You can show how the total and count change for each record.

Save your work and check the required submission files.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
independent revision and the issued task.
