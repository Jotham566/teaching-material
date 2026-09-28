# CML3111 Week06 Engineering

Lecturer companion to the revised PowerPoint. Slide numbers match this edition. Explain the worked examples directly; revision checks are for individual study.

## Slide 1 — Cleaning data and explaining changes

PURPOSE
Cleaning data and explaining changes

CONNECT
Build on the preceding week. Explain why this example is needed before running it.

EXPLAIN
Communications, Electrical, Mechatronics and Robotics Engineering

LECTURER DETAIL
TEACHING PURPOSE
Cleaning data and explaining changes

LECTURER CUE
Use PowerPoint Presenter View for these notes. Teach one example, pause for every learner to predict, then work an analogous example together. The practice notebook is a learning aid, not an extra graded upload.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

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
Build on Cleaning data and explaining changes. Explain why this example is needed before running it.

EXPLAIN
Recognise missing values and repeated records.

Make a working copy and record each cleaning action.

LECTURER DETAIL
TEACHING PURPOSE
Today’s learning

CONNECT
Build on the preceding slide: Cleaning data and explaining changes.

LECTURER CUE
Ask learners to explain this goal in ordinary language. The first successful attempt matters more than covering optional extensions. Defer: MCAR/MAR/MNAR names, five chart families and six unaided defect hunts are reference. Teach missingness causes in everyday language first.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

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
Week 5 selected and summarised columns. Before trusting those summaries, inspect missing values, repeated observations and measurement units.

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
A repeated record or a missing measurement can change a summary. We keep the original records, apply the stated cleaning rules and explain each change before plotting.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Raw data and Missing value.

## Slide 5 — Raw data and Missing value

PURPOSE
Raw data and Missing value

CONNECT
Build on Why this week’s tools are needed. Explain why this example is needed before running it.

EXPLAIN
Raw data: The original supplied records. Keep these unchanged so another person can check your decisions.
Missing value: A value that was not recorded, represented here by None in Python records. Missing does not automatically mean zero.

LECTURER DETAIL
TEACHING PURPOSE
Words we will use

CONNECT
Build on the preceding slide: The engineering context.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

POINT TO THE DEFINITION
Raw data: The original supplied records. Keep these unchanged so another person can check your decisions.
Missing value: A value that was not recorded, represented here by None in Python records. Missing does not automatically mean zero.

NEXT
Words we will use. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Record and equipment ID and Median and imputation.

## Slide 6 — Record and equipment ID and Median and imputation

PURPOSE
Record and equipment ID and Median and imputation

CONNECT
Build on Raw data and Missing value. Explain why this example is needed before running it.

EXPLAIN
Record and equipment ID: A record ID identifies an observation. An equipment ID identifies the source and may repeat legitimately. Remove repeated observations only under the stated rule.
Median and imputation: The median is the middle sorted value, or the mean of the two middle values. Imputation fills a missing value using an explicit rule and introduces uncertainty.

LECTURER DETAIL
TEACHING PURPOSE
Words we will use

CONNECT
Build on the preceding slide: Words we will use.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

POINT TO THE DEFINITION
Record and equipment ID: A record ID identifies an observation. An equipment ID identifies the source and may repeat legitimately. Remove repeated observations only under the stated rule.
Median and imputation: The median is the middle sorted value, or the mean of the two middle values. Imputation fills a missing value using an explicit rule and introduces uncertainty.

NEXT
An unusual value needs a reason. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
An unusual value needs a reason.

## Slide 7 — An unusual value needs a reason

PURPOSE
An unusual value needs a reason

CONNECT
Build on Record and equipment ID and Median and imputation. Explain why this example is needed before running it.

EXPLAIN
A missing reading has no recorded value.

Zero is a recorded value and may be physically meaningful.

A large or negative value needs instrument and unit context.

Preserve the raw data and record every cleaning decision.

LECTURER DETAIL
TEACHING PURPOSE
An unusual value needs a reason

CONNECT
Build on the preceding slide: Words we will use.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
Mean, median and unusual readings. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Mean, median and unusual readings.

## Slide 8 — Mean, median and unusual readings

PURPOSE
Mean, median and unusual readings

CONNECT
Build on An unusual value needs a reason. Explain why this example is needed before running it.

EXPLAIN
The mean uses every value. The median is the middle sorted value. A large value needs context.

LECTURER DETAIL
TEACHING PURPOSE
Mean, median and unusual readings

CONNECT
Build on the preceding slide: An unusual value needs a reason.

LECTURER CUE
The mean uses every value. The median is the middle sorted value. A large value needs context.

EXPLAIN IN ORDINARY WORDS
Mean is total divided by count. Median is the middle of sorted values. A percentile locates a position in that ordered distribution; interpolation conventions can differ. Match the summary to the question.

CHECK AND EXPECTED ANSWER
For [2,3,4,5,100], median=4 and mean=22.8. The large value pulls the mean up.

IF LEARNERS ARE STUCK
Sort five values by hand. A skewed distribution does not make the mean wrong if the question concerns totals or expected cost.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
Filling a gap adds an estimate. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Filling a gap adds an estimate.

## Slide 9 — Filling a gap adds an estimate

PURPOSE
Filling a gap adds an estimate

CONNECT
Build on Mean, median and unusual readings. Explain why this example is needed before running it.

EXPLAIN
The valid readings, sorted, are 20, 22, 24 and 80.

The two middle values are 22 and 24. Their mean is 23.

Using 23 for a blank is a declared cleaning rule. It does not recover the lost measurement.

In Python, value is None tests for a missing marker. is not None tests that it is not that marker.

LECTURER DETAIL
TEACHING PURPOSE
Filling a gap adds an estimate

CONNECT
Build on the preceding slide: Mean, median and unusual readings.

LECTURER CUE
Use the example below to sort four valid readings. The median is (22 + 24) / 2 = 23. Filling a blank with 23 is a stated teaching rule, not a recovered measurement.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
Worked example (1/2). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Worked example (1/2).

## Slide 10 — Cleaning decisions and charts in Python (1/2)

PURPOSE
Cleaning decisions and charts in Python (1/2)

CONNECT
Build on Filling a gap adds an estimate. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
TEACHING PURPOSE
Worked example (1/2)

CONNECT
Build on the preceding slide: Filling a gap adds an estimate.

LECTURER CUE
Use the example below to sort four valid readings. The median is (22 + 24) / 2 = 23. Filling a blank with 23 is a stated teaching rule, not a recovered measurement. Model a defect register: observation, evidence, decision, affected count, limitation. Work one repeated record and one missing value together. Draw a scatter plot from four pairs on the board. A pattern can motivate investigation without proving that one variable causes the other.

Complete practice code:
from statistics import median
raw = [20, None, 22, 24, 80]
known = []
for value in raw:
    if value is not None:
        known.append(value)
fill = median(known)
cleaned = []
for value in raw:
    if value is None:
        cleaned.append(fill)
    else:
        cleaned.append(value)
print(fill)
print(raw)
print(cleaned)

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

WALK THROUGH THIS CODE
import loads a library. from selects a tool from it.
for takes the next item. The indented block repeats.
if tests a condition. The chosen indented block runs.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Worked example (2/2). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Worked example (2/2).

## Slide 11 — Cleaning decisions and charts in Python (2/2)

PURPOSE
Cleaning decisions and charts in Python (2/2)

CONNECT
Build on Cleaning decisions and charts in Python (1/2). Explain why this example is needed before running it.

EXPLAIN
Continue the SAME cell; keep indentation. Run after all parts are entered.

LECTURER DETAIL
TEACHING PURPOSE
Worked example (2/2)

CONNECT
Build on the preceding slide: Worked example (1/2).

LECTURER CUE
Use the example below to sort four valid readings. The median is (22 + 24) / 2 = 23. Filling a blank with 23 is a stated teaching rule, not a recovered measurement. Model a defect register: observation, evidence, decision, affected count, limitation. Work one repeated record and one missing value together. Draw a scatter plot from four pairs on the board. A pattern can motivate investigation without proving that one variable causes the other.

Complete practice code:
from statistics import median
raw = [20, None, 22, 24, 80]
known = []
for value in raw:
    if value is not None:
        known.append(value)
fill = median(known)
cleaned = []
for value in raw:
    if value is None:
        cleaned.append(fill)
    else:
        cleaned.append(value)
print(fill)
print(raw)
print(cleaned)

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

WALK THROUGH THIS CODE
for takes the next item. The indented block repeats.
if tests a condition. The chosen indented block runs.
print displays a value below the cell.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Expected output. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Expected output.

## Slide 12 — Cleaning decisions and charts results

PURPOSE
Cleaning decisions and charts results

CONNECT
Build on Cleaning decisions and charts in Python (2/2). Explain why this example is needed before running it.

EXPLAIN
23.0
[20, None, 22, 24, 80]
[20, 23.0, 22, 24, 80]

LECTURER DETAIL
TEACHING PURPOSE
Expected output

CONNECT
Build on the preceding slide: Worked example (2/2).

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

NEXT
Copy a record and remember an ID. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Copy a record and remember an ID.

## Slide 13 — Copy a record and remember an ID

PURPOSE
Copy a record and remember an ID

CONNECT
Build on Cleaning decisions and charts results. Explain why this example is needed before running it.

EXPLAIN
dict(row): For our flat records, dict(row) makes a separate dictionary with the same fields. Changing a number in the copy leaves the original record unchanged.
set, in, add and continue: set() starts an empty collection of unique items. in checks membership; add remembers an item. continue skips the rest of the current loop pass.

LECTURER DETAIL
TEACHING PURPOSE
Copy a record and remember an ID

CONNECT
Build on the preceding slide: Expected output.

EXPLAIN IN ORDINARY WORDS
A dictionary pairs a key with a value. For {"unit":"A", "reading":4}, record["reading"] looks up the key and gives 4. The key is not a list position.

CHECK AND EXPECTED ANSWER
What happens if the key is spelled "Reading" instead? It is a different key; direct lookup can raise KeyError.

IF LEARNERS ARE STUCK
Point to each key and its value. Read the colon as associates-with, then do one exact lookup.

POINT TO THE DEFINITION
dict(row): For our flat records, dict(row) makes a separate dictionary with the same fields. Changing a number in the copy leaves the original record unchanged.
set, in, add and continue: set() starts an empty collection of unique items. in checks membership; add remembers an item. continue skips the rest of the current loop pass.

NEXT
A working copy preserves the original. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A working copy preserves the original.

## Slide 14 — A working copy preserves the original

PURPOSE
A working copy preserves the original

CONNECT
Build on Copy a record and remember an ID. Explain why this example is needed before running it.

EXPLAIN
In this separate four-record example, remove one repeated C record and fill B with (20 + 24) / 2 = 22.

LECTURER DETAIL
TEACHING PURPOSE
A working copy preserves the original

CONNECT
Build on the preceding slide: Copy a record and remember an ID.

LECTURER CUE
Ask students to describe what they see before introducing terminology. Generated conceptual teaching illustration. The working-copy rule is a toy activity, not the exact assessed cleaning policy. Source: figs/experiential/ASSET_SOURCES.md.

NEXT
Copies and duplicate checks. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Copies and duplicate checks.

## Slide 15 — Copies and duplicate checks

PURPOSE
Copies and duplicate checks

CONNECT
Build on A working copy preserves the original. Explain why this example is needed before running it.

EXPLAIN
dict(row) makes a shallow copy. A set keeps unique IDs.

LECTURER DETAIL
TEACHING PURPOSE
Copies and duplicate checks

CONNECT
Build on the preceding slide: A working copy preserves the original.

LECTURER CUE
Read each symbol before running. Ask everyone to predict. Expected output: 4 then True. The example has only scalar fields. A shallow copy does not independently copy nested lists.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

WALK THROUGH THIS CODE
print displays a value below the cell.
Square brackets create a list or select an item.
Braces hold dictionary key: value pairs here.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Copying records and recognising repeats. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Following a cleaning loop.

## Slide 16 — Following a cleaning loop

PURPOSE
Following a cleaning loop

CONNECT
Build on Copies and duplicate checks. Explain why this example is needed before running it.

EXPLAIN
An empty string "" and None are different values. Parse CSV fields according to the issued rule.

LECTURER DETAIL
TEACHING PURPOSE
Following a cleaning loop

CONNECT
Build on the preceding slide: Copying records and recognising repeats.

LECTURER CUE
Read one row at a time and use a changed value. This is a syntax reference for the worked examples.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
Copying records and recognising repeats in Python (1/2). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Copying records and recognising repeats in Python (1/2).

## Slide 17 — Copying records and recognising repeats in Python (1/2)

PURPOSE
Copying records and recognising repeats in Python (1/2)

CONNECT
Build on Following a cleaning loop. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
TEACHING PURPOSE
Copying records and recognising repeats in Python (1/2)

CONNECT
Build on the preceding slide: Following a cleaning loop.

LECTURER CUE
set() creates a collection of already-seen identifiers. in checks membership. continue skips the rest of that iteration. dict(row) copies a record so later edits do not change the original. Different record IDs from the same equipment remain legitimate observations.

Complete practice code:
raw_records = [{"id": 1, "equipment": "A", "value": 10},
               {"id": 1, "equipment": "A", "value": 10},
               {"id": 2, "equipment": "A", "value": 12}]
seen = set()
kept = []
for row in raw_records:
    if row["id"] in seen:
        continue
    seen.add(row["id"])
    kept.append(dict(row))
print(len(raw_records), len(kept))

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

WALK THROUGH THIS CODE
Square brackets create a list or select an item.
Braces hold dictionary key: value pairs here.
= assigns the value on the right to the name on the left.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Copying records and recognising repeats in Python (2/2). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Copying records and recognising repeats in Python (2/2).

## Slide 18 — Copying records and recognising repeats in Python (2/2)

PURPOSE
Copying records and recognising repeats in Python (2/2)

CONNECT
Build on Copying records and recognising repeats in Python (1/2). Explain why this example is needed before running it.

EXPLAIN
Continue the SAME cell; keep indentation. Run after all parts are entered.

LECTURER DETAIL
TEACHING PURPOSE
Copying records and recognising repeats in Python (2/2)

CONNECT
Build on the preceding slide: Copying records and recognising repeats in Python (1/2).

LECTURER CUE
set() creates a collection of already-seen identifiers. in checks membership. continue skips the rest of that iteration. dict(row) copies a record so later edits do not change the original. Different record IDs from the same equipment remain legitimate observations.

Complete practice code:
raw_records = [{"id": 1, "equipment": "A", "value": 10},
               {"id": 1, "equipment": "A", "value": 10},
               {"id": 2, "equipment": "A", "value": 12}]
seen = set()
kept = []
for row in raw_records:
    if row["id"] in seen:
        continue
    seen.add(row["id"])
    kept.append(dict(row))
print(len(raw_records), len(kept))

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

WALK THROUGH THIS CODE
for takes the next item. The indented block repeats.
if tests a condition. The chosen indented block runs.
print displays a value below the cell.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Summaries returned as a dictionary. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Summaries returned as a dictionary.

## Slide 19 — Summaries returned as a dictionary

PURPOSE
Summaries returned as a dictionary

CONNECT
Build on Copying records and recognising repeats in Python (2/2). Explain why this example is needed before running it.

EXPLAIN
This example expects a nonempty list.

It calculates a count and mean, then returns a dictionary with named outputs.

Use the exact keys specified by the issued task when adapting this pattern.

LECTURER DETAIL
TEACHING PURPOSE
Summaries returned as a dictionary

CONNECT
Build on the preceding slide: Copying records and recognising repeats in Python (2/2).

LECTURER CUE
This example expects a nonempty list. It calculates a count and mean, then returns a dictionary with named outputs. Use the exact keys specified by the issued task when adapting this pattern.

EXPLAIN IN ORDINARY WORDS
A dictionary pairs a key with a value. For {"unit":"A", "reading":4}, record["reading"] looks up the key and gives 4. The key is not a list position.

CHECK AND EXPECTED ANSWER
What happens if the key is spelled "Reading" instead? It is a different key; direct lookup can raise KeyError.

IF LEARNERS ARE STUCK
Point to each key and its value. Read the colon as associates-with, then do one exact lookup.

NEXT
Summaries returned as a dictionary in Python. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Summaries returned as a dictionary in Python.

## Slide 20 — Summaries returned as a dictionary in Python

PURPOSE
Summaries returned as a dictionary in Python

CONNECT
Build on Summaries returned as a dictionary. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
TEACHING PURPOSE
Summaries returned as a dictionary in Python

CONNECT
Build on the preceding slide: Summaries returned as a dictionary.

LECTURER CUE
This example expects a nonempty list. It calculates a count and mean, then returns a dictionary with named outputs. Use the exact keys specified by the issued task when adapting this pattern.

Complete practice code:
def describe(values):
    count = len(values)
    mean = sum(values) / count
    return {"count": count, "mean": mean}

print(describe([10, 12]))

EXPLAIN IN ORDINARY WORDS
A dictionary pairs a key with a value. For {"unit":"A", "reading":4}, record["reading"] looks up the key and gives 4. The key is not a list position.

CHECK AND EXPECTED ANSWER
What happens if the key is spelled "Reading" instead? It is a different key; direct lookup can raise KeyError.

IF LEARNERS ARE STUCK
Point to each key and its value. Read the colon as associates-with, then do one exact lookup.

WALK THROUGH THIS CODE
def names the function. Inputs go inside parentheses.
return sends the result back to the caller.
print displays a value below the cell.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Reading a blank field. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Reading a blank field.

## Slide 21 — Reading a blank field

PURPOSE
Reading a blank field

CONNECT
Build on Summaries returned as a dictionary in Python. Explain why this example is needed before running it.

EXPLAIN
CSV values start as text.

The if/else below stores None for a blank.

Otherwise float converts the text into a number.

LECTURER DETAIL
TEACHING PURPOSE
Reading a blank field

CONNECT
Build on the preceding slide: Summaries returned as a dictionary in Python.

LECTURER CUE
CSV values start as text. The if/else below stores None for a blank. Otherwise float converts the text into a number.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
Reading a blank field in Python. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Reading a blank field in Python.

## Slide 22 — Reading a blank field in Python

PURPOSE
Reading a blank field in Python

CONNECT
Build on Reading a blank field. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
TEACHING PURPOSE
Reading a blank field in Python

CONNECT
Build on the preceding slide: Reading a blank field.

LECTURER CUE
CSV values start as text. The if/else below stores None for a blank. Otherwise float converts the text into a number.

Complete practice code:
text_values = ["20", "", "24"]
parsed = []
for text in text_values:
    if text == "":
        parsed.append(None)
    else:
        parsed.append(float(text))
print(parsed)

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
Audit. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Audit.

## Slide 23 — Audit

PURPOSE
Audit

CONNECT
Build on Reading a blank field in Python. Explain why this example is needed before running it.

EXPLAIN
Audit: A count and explanation of what changed, why it changed and how many records remain.

LECTURER DETAIL
TEACHING PURPOSE
Audit

CONNECT
Build on the preceding slide: Reading a blank field in Python.

POINT TO THE DEFINITION
Audit: A count and explanation of what changed, why it changed and how many records remain.

NEXT
Every cleaning change needs a record. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Every cleaning change needs a record.

## Slide 24 — Every cleaning change needs a record

PURPOSE
Every cleaning change needs a record

CONNECT
Build on Audit. Explain why this example is needed before running it.

EXPLAIN
A duplicate record ID suggests a repeated observation.

Two different observations from the same equipment can both be valid.

Record the evidence, action, number of affected rows and limitation.

LECTURER DETAIL
TEACHING PURPOSE
Every cleaning change needs a record

CONNECT
Build on the preceding slide: Audit.

LECTURER CUE
Model a defect register: observation, evidence, decision, affected count, limitation. Work one repeated record and one missing value together.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

NEXT
You are the cleaning audit. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Chart axes.

## Slide 25 — Chart axes

PURPOSE
Chart axes

CONNECT
Build on Every cleaning change needs a record. Explain why this example is needed before running it.

EXPLAIN
Chart axes: A chart maps values to positions. Read the horizontal variable, vertical variable and their units before interpreting a pattern.

LECTURER DETAIL
TEACHING PURPOSE
Chart axes

CONNECT
Build on the preceding slide: What the activity shows.

EXPLAIN IN ORDINARY WORDS
Begin with the question and intended comparison. Identify what an axis, bar, point or colour represents, including its unit. A chart summarises data and may hide variation.

CHECK AND EXPECTED ANSWER
For a bar chart comparing amounts, why normally start the value axis at zero? Bar length encodes magnitude; truncation can exaggerate differences.

IF LEARNERS ARE STUCK
Read one mark aloud as a sentence. Check the population, period, filters and units before stating the finding.

POINT TO THE DEFINITION
Chart axes: A chart maps values to positions. Read the horizontal variable, vertical variable and their units before interpreting a pattern.

NEXT
A scatter plot pairs two measurements. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A scatter plot pairs two measurements.

## Slide 26 — A scatter plot pairs two measurements

PURPOSE
A scatter plot pairs two measurements

CONNECT
Build on Chart axes. Explain why this example is needed before running it.

EXPLAIN
The horizontal axis gives the input value.

The vertical axis gives the corresponding reading.

One point represents one observation. A pattern alone does not prove causation.

LECTURER DETAIL
TEACHING PURPOSE
A scatter plot pairs two measurements

CONNECT
Build on the preceding slide: Chart axes.

LECTURER CUE
Draw a scatter plot from four pairs on the board. A pattern can motivate investigation without proving that one variable causes the other.

EXPLAIN IN ORDINARY WORDS
Begin with the question and intended comparison. Identify what an axis, bar, point or colour represents, including its unit. A chart summarises data and may hide variation.

CHECK AND EXPECTED ANSWER
For a bar chart comparing amounts, why normally start the value axis at zero? Bar length encodes magnitude; truncation can exaggerate differences.

IF LEARNERS ARE STUCK
Read one mark aloud as a sentence. Check the population, period, filters and units before stating the finding.

NEXT
Choose a chart after naming the question. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Choose a chart after naming the question.

## Slide 27 — Choose a chart after naming the question

PURPOSE
Choose a chart after naming the question

CONNECT
Build on A scatter plot pairs two measurements. Explain why this example is needed before running it.

EXPLAIN
Scatter and bar: A scatter plot places one point for each paired measurement. A bar chart compares values across named groups. Label both axes and their units.
Histogram and bins: A histogram counts observations in numerical intervals called bins. The horizontal axis is the measurement; the vertical axis is a count. Bin edges affect its appearance.

LECTURER DETAIL
TEACHING PURPOSE
Choose a chart after naming the question

CONNECT
Build on the preceding slide: A scatter plot pairs two measurements.

EXPLAIN IN ORDINARY WORDS
Begin with the question and intended comparison. Identify what an axis, bar, point or colour represents, including its unit. A chart summarises data and may hide variation.

CHECK AND EXPECTED ANSWER
For a bar chart comparing amounts, why normally start the value axis at zero? Bar length encodes magnitude; truncation can exaggerate differences.

IF LEARNERS ARE STUCK
Read one mark aloud as a sentence. Check the population, period, filters and units before stating the finding.

POINT TO THE DEFINITION
Scatter and bar: A scatter plot places one point for each paired measurement. A bar chart compares values across named groups. Label both axes and their units.
Histogram and bins: A histogram counts observations in numerical intervals called bins. The horizontal axis is the measurement; the vertical axis is a count. Bin edges affect its appearance.

NEXT
Choosing a chart for the question. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Choosing a chart for the question.

## Slide 28 — Choosing a chart for the question

PURPOSE
Choosing a chart for the question

CONNECT
Build on Choose a chart after naming the question. Explain why this example is needed before running it.

EXPLAIN
This week uses histograms, scatter plots and bar charts. The other chart types are reference examples.

LECTURER DETAIL
TEACHING PURPOSE
Choosing a chart for the question

CONNECT
Build on the preceding slide: Choose a chart after naming the question.

LECTURER CUE
Name the question answered by each chart. Correlation does not establish causation. A bar chart usually needs a zero baseline.
Source: existing course illustration figs/chart_chooser.png. These are illustrative examples, not this cohort’s assessed results.

EXPLAIN IN ORDINARY WORDS
Begin with the question and intended comparison. Identify what an axis, bar, point or colour represents, including its unit. A chart summarises data and may hide variation.

CHECK AND EXPECTED ANSWER
For a bar chart comparing amounts, why normally start the value axis at zero? Bar length encodes magnitude; truncation can exaggerate differences.

IF LEARNERS ARE STUCK
Read one mark aloud as a sentence. Check the population, period, filters and units before stating the finding.

NEXT
A chart with labelled axes. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A chart with labelled axes.

## Slide 29 — A chart with labelled axes

PURPOSE
A chart with labelled axes

CONNECT
Build on Choosing a chart for the question. Explain why this example is needed before running it.

EXPLAIN
matplotlib is a plotting library. plt is the short name we give its pyplot module.

fig, ax = plt.subplots() returns two objects: fig is the whole figure; ax is its plotting area. scatter places the paired measurements as points.

ax.set_xlabel(...) labels the horizontal axis. set_ylabel labels the vertical axis. Keep fig when the task asks you to return a Figure object.

LECTURER DETAIL
TEACHING PURPOSE
A chart with labelled axes

CONNECT
Build on the preceding slide: Choosing a chart for the question.

LECTURER CUE
matplotlib draws charts. subplots creates a Figure, the whole page, and Axes, the plotting area. scatter pairs each input with its corresponding reading. The horizontal axis is the input and the vertical axis is the reading. A pattern alone does not prove causation. In the test, return Figure objects as the brief specifies.

EXPLAIN IN ORDINARY WORDS
Begin with the question and intended comparison. Identify what an axis, bar, point or colour represents, including its unit. A chart summarises data and may hide variation.

CHECK AND EXPECTED ANSWER
For a bar chart comparing amounts, why normally start the value axis at zero? Bar length encodes magnitude; truncation can exaggerate differences.

IF LEARNERS ARE STUCK
Read one mark aloud as a sentence. Check the population, period, filters and units before stating the finding.

NEXT
A chart with labelled axes in Python. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A chart with labelled axes in Python.

## Slide 30 — A chart with labelled axes in Python

PURPOSE
A chart with labelled axes in Python

CONNECT
Build on A chart with labelled axes. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
TEACHING PURPOSE
A chart with labelled axes in Python

CONNECT
Build on the preceding slide: A chart with labelled axes.

LECTURER CUE
matplotlib draws charts. subplots creates a Figure, the whole page, and Axes, the plotting area. scatter pairs each input with its corresponding reading. The horizontal axis is the input and the vertical axis is the reading. A pattern alone does not prove causation. In the test, return Figure objects as the brief specifies.

Complete practice code:
import matplotlib.pyplot as plt
inputs = [1, 2, 3, 4]
readings = [12, 14, 13, 18]
fig, ax = plt.subplots()
ax.scatter(inputs, readings)
ax.set_xlabel("Input (teaching units)")
ax.set_ylabel("Reading (teaching units)")
ax.set_title("Four invented observations")
plt.show()

EXPLAIN IN ORDINARY WORDS
Begin with the question and intended comparison. Identify what an axis, bar, point or colour represents, including its unit. A chart summarises data and may hide variation.

CHECK AND EXPECTED ANSWER
For a bar chart comparing amounts, why normally start the value axis at zero? Bar length encodes magnitude; truncation can exaggerate differences.

IF LEARNERS ARE STUCK
Read one mark aloud as a sentence. Check the population, period, filters and units before stating the finding.

WALK THROUGH THIS CODE
import loads a library. from selects a tool from it.
Square brackets create a list or select an item.
= assigns the value on the right to the name on the left.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Comparing groups and a distribution. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Comparing groups and a distribution.

## Slide 31 — Comparing groups and a distribution

PURPOSE
Comparing groups and a distribution

CONNECT
Build on A chart with labelled axes in Python. Explain why this example is needed before running it.

EXPLAIN
bar compares one value for each named group. hist counts observations in value intervals called bins.

Read the bar labels and both axes.

This practice uses two bins; follow the exact bin rule in the test brief.

Save and keep the Figure objects when a task asks for them.

LECTURER DETAIL
TEACHING PURPOSE
Comparing groups and a distribution

CONNECT
Build on the preceding slide: A chart with labelled axes in Python.

LECTURER CUE
bar compares one value for each named group. hist counts observations in value intervals called bins. Read the bar labels and both axes. This practice uses two bins; follow the exact bin rule in the test brief. Save and keep the Figure objects when a task asks for them.

EXPLAIN IN ORDINARY WORDS
Mean is total divided by count. Median is the middle of sorted values. A percentile locates a position in that ordered distribution; interpolation conventions can differ. Match the summary to the question.

CHECK AND EXPECTED ANSWER
For [2,3,4,5,100], median=4 and mean=22.8. The large value pulls the mean up.

IF LEARNERS ARE STUCK
Sort five values by hand. A skewed distribution does not make the mean wrong if the question concerns totals or expected cost.

NEXT
Comparing groups and a distribution in Python (1/2). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Comparing groups and a distribution in Python (1/2).

## Slide 32 — Comparing groups and a distribution in Python (1/2)

PURPOSE
Comparing groups and a distribution in Python (1/2)

CONNECT
Build on Comparing groups and a distribution. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
TEACHING PURPOSE
Comparing groups and a distribution in Python (1/2)

CONNECT
Build on the preceding slide: Comparing groups and a distribution.

LECTURER CUE
bar compares one value for each named group. hist counts observations in value intervals called bins. Read the bar labels and both axes. This practice uses two bins; follow the exact bin rule in the test brief. Save and keep the Figure objects when a task asks for them.

Complete practice code:
bar_fig, bar_ax = plt.subplots()
bar_ax.bar(["A", "B"], [13, 16])
bar_ax.set_xlabel("Group")
bar_ax.set_ylabel("Mean reading (teaching units)")
bar_ax.set_title("Two invented group means")
hist_fig, hist_ax = plt.subplots()
hist_ax.hist(readings, bins=2)
hist_ax.set_xlabel("Reading (teaching units)")
hist_ax.set_ylabel("Count of observations")
hist_ax.set_title("Distribution of four observations")
plt.show()

EXPLAIN IN ORDINARY WORDS
Mean is total divided by count. Median is the middle of sorted values. A percentile locates a position in that ordered distribution; interpolation conventions can differ. Match the summary to the question.

CHECK AND EXPECTED ANSWER
For [2,3,4,5,100], median=4 and mean=22.8. The large value pulls the mean up.

IF LEARNERS ARE STUCK
Sort five values by hand. A skewed distribution does not make the mean wrong if the question concerns totals or expected cost.

WALK THROUGH THIS CODE
Square brackets create a list or select an item.
= assigns the value on the right to the name on the left.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Comparing groups and a distribution in Python (2/2). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Comparing groups and a distribution in Python (2/2).

## Slide 33 — Comparing groups and a distribution in Python (2/2)

PURPOSE
Comparing groups and a distribution in Python (2/2)

CONNECT
Build on Comparing groups and a distribution in Python (1/2). Explain why this example is needed before running it.

EXPLAIN
Continue the SAME cell; keep indentation. Run after all parts are entered.

LECTURER DETAIL
TEACHING PURPOSE
Comparing groups and a distribution in Python (2/2)

CONNECT
Build on the preceding slide: Comparing groups and a distribution in Python (1/2).

LECTURER CUE
bar compares one value for each named group. hist counts observations in value intervals called bins. Read the bar labels and both axes. This practice uses two bins; follow the exact bin rule in the test brief. Save and keep the Figure objects when a task asks for them.

Complete practice code:
bar_fig, bar_ax = plt.subplots()
bar_ax.bar(["A", "B"], [13, 16])
bar_ax.set_xlabel("Group")
bar_ax.set_ylabel("Mean reading (teaching units)")
bar_ax.set_title("Two invented group means")
hist_fig, hist_ax = plt.subplots()
hist_ax.hist(readings, bins=2)
hist_ax.set_xlabel("Reading (teaching units)")
hist_ax.set_ylabel("Count of observations")
hist_ax.set_title("Distribution of four observations")
plt.show()

EXPLAIN IN ORDINARY WORDS
Mean is total divided by count. Median is the middle of sorted values. A percentile locates a position in that ordered distribution; interpolation conventions can differ. Match the summary to the question.

CHECK AND EXPECTED ANSWER
For [2,3,4,5,100], median=4 and mean=22.8. The large value pulls the mean up.

IF LEARNERS ARE STUCK
Sort five values by hand. A skewed distribution does not make the mean wrong if the question concerns totals or expected cost.

WALK THROUGH THIS CODE
Read the inputs and identify the operation.
Predict the result before running this cell.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Your turn. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Revision example and answer.

## Slide 34 — Revision example and answer

PURPOSE
Revision example and answer

CONNECT
Build on Comparing groups and a distribution in Python (2/2). Explain why this example is needed before running it.

EXPLAIN
Example: Explain why 80 was retained. Replace 24 with 26, predict the new fill value, and check that cleaning still leaves raw unchanged.

Answer: An unusual value alone does not prove an error. The task did not authorize deleting 80. With 26 replacing 24, the middle known values are 22 and 26, so the new fill is 24. The raw list still contains None.

LECTURER DETAIL
TEACHING PURPOSE
Your turn

CONNECT
Build on the preceding slide: Comparing groups and a distribution in Python (2/2).

LECTURER CUE
Give silent thinking time, then let pairs discuss. Rotate who types. This is practice, not a graded quiz. Expected response: An unusual value alone does not prove an error. The task did not authorize deleting 80. With 26 replacing 24, the middle known values are 22 and 26, so the new fill is 24. The raw list still contains None.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

DISCUSSION KEY FOR THIS SLIDE
DISCUSS THE REASONING
Practice discussion
An unusual value alone does not prove an error. The task did not authorize deleting 80. With 26 replacing 24, the middle known values are 22 and 26, so the new fill is 24. The raw list still contains None.
Which step produced this result? What changes if one input changes?
CML3111   Week 6   38
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
Practice discussion. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A compact loop is optional.

## Slide 35 — A compact loop is optional

PURPOSE
A compact loop is optional

CONNECT
Build on Revision example and answer. Explain why this example is needed before running it.

EXPLAIN
A list comprehension makes the same list. Learn the ordinary loop first.

LECTURER DETAIL
TEACHING PURPOSE
A compact loop is optional

CONNECT
Build on the preceding slide: Practice discussion.

LECTURER CUE
Read each symbol before running. Ask everyone to predict. Expected output: [4, 8, 12] twice

EXPLAIN IN ORDINARY WORDS
A loop repeats its indented instructions for each item. A running total must be initialised before the loop and updated inside it.

CHECK AND EXPECTED ANSWER
For values 2,4,6 and total initially 0, what are the successive totals? 2,6,12.

IF LEARNERS ARE STUCK
Use a trace table with current item and total. Resetting total inside the loop loses earlier additions.

WALK THROUGH THIS CODE
for takes the next item. The indented block repeats.
print displays a value below the cell.
append adds one item to the end of a list.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Short explainer and discussion. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Preparing for the assignment.

## Slide 36 — Preparing for the assignment

PURPOSE
Preparing for the assignment

CONNECT
Build on A compact loop is optional. Explain why this example is needed before running it.

EXPLAIN
W06 uses a list of record dictionaries.

Show one record and one field lookup before the function interfaces.

Parse CSV blank numeric cells as None. dict(row) copies a record. append adds an item to a list.

The task brief specifies the cleaning order and returned outputs.

LECTURER DETAIL
TEACHING PURPOSE
Preparing for the assignment

CONNECT
Build on the preceding slide: After the video.

LECTURER CUE
W06 uses a list of record dictionaries. Show one record and one field lookup before the function interfaces. Parse CSV blank numeric cells as None. Model copying with dict(row) and list.append. Walk through the published cleaning order before students write clean_records, summarize_records and audit_cleaning. Teach set membership for duplicate IDs and grouped accumulation. Explain that written evidence belongs in My written evidence, not in code comments.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Preparing for the assignment continued. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Preparing for the assignment continued.

## Slide 37 — Preparing for the assignment continued

PURPOSE
Preparing for the assignment continued

CONNECT
Build on Preparing for the assignment. Explain why this example is needed before running it.

EXPLAIN
A set records IDs already seen.

Group summaries collect readings with the same equipment ID.

Explain that written evidence belongs in My written evidence, not in code comments.

LECTURER DETAIL
TEACHING PURPOSE
Preparing for the assignment continued

CONNECT
Build on the preceding slide: Preparing for the assignment.

LECTURER CUE
W06 uses a list of record dictionaries. Show one record and one field lookup before the function interfaces. Parse CSV blank numeric cells as None. Model copying with dict(row) and list.append. Walk through the published cleaning order before students write clean_records, summarize_records and audit_cleaning. Teach set membership for duplicate IDs and grouped accumulation. Explain that written evidence belongs in My written evidence, not in code comments.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Cleaning choices and charts. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Cleaning choices and charts.

## Slide 38 — Cleaning choices and charts

PURPOSE
Cleaning choices and charts

CONNECT
Build on Preparing for the assignment continued. Explain why this example is needed before running it.

EXPLAIN
Filling blanks with zero changes the mean and may be unjustified.

Dropping every row with any blank can remove valid observations.

A failed numeric conversion identifies a problematic value to inspect rather than hide.

A histogram describes one distribution; a scatter plot shows paired values; a grouped chart compares groups.

LECTURER DETAIL
TEACHING PURPOSE
Cleaning choices and charts

CONNECT
Build on the preceding slide: Preparing for the assignment continued.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

NEXT
Cleaning choices and charts continued. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Cleaning choices and charts continued.

## Slide 39 — Cleaning choices and charts continued

PURPOSE
Cleaning choices and charts continued

CONNECT
Build on Cleaning choices and charts. Explain why this example is needed before running it.

EXPLAIN
Read both axes and units.

A plausible extreme needs investigation before deletion.

LECTURER DETAIL
TEACHING PURPOSE
Cleaning choices and charts continued

CONNECT
Build on the preceding slide: Cleaning choices and charts.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

NEXT
Your issued task. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Your issued task.

## Slide 40 — Your issued task

PURPOSE
Your issued task

CONNECT
Build on Cleaning choices and charts continued. Explain why this example is needed before running it.

EXPLAIN
Investigate motor winding temperature.

Target units: deg C.

These are synthetic teaching records, not measurements suitable for deployment.

Each record is one operating observation; equipment_id repeats across observations.

LECTURER DETAIL
TEACHING PURPOSE
Your issued task

CONNECT
Build on the preceding slide: Cleaning choices and charts continued.

LECTURER CUE
Investigate motor winding temperature. Target units: deg C. These are synthetic teaching records, not measurements suitable for deployment. Each record is one operating observation; equipment_id repeats across observations.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
clean_records(records). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
clean_records(records).

## Slide 41 — clean_records(records)

PURPOSE
clean_records(records)

CONNECT
Build on Your issued task. Explain why this example is needed before running it.

EXPLAIN
Return copied records in original order: remove repeated record_id after its first occurrence, drop rows with missing target or load_pct outside 0–100 inclusive, then fill missing ambient_c with the median of retained non-missing ambient_c values.

Preserve raw input.

No other changes.

LECTURER DETAIL
TEACHING PURPOSE
clean_records(records)

CONNECT
Build on the preceding slide: Your issued task.

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W06/CML3111/A/TASKS.md

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
summarize_records(clean_records). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
summarize_records(clean_records).

## Slide 42 — summarize_records(clean_records)

PURPOSE
summarize_records(clean_records)

CONNECT
Build on clean_records(records). Explain why this example is needed before running it.

EXPLAIN
Return count, mean, minimum, maximum of target and group_means by equipment_id.

Retain full precision.

LECTURER DETAIL
TEACHING PURPOSE
summarize_records(clean_records)

CONNECT
Build on the preceding slide: clean_records(records).

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W06/CML3111/A/TASKS.md

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

NEXT
audit_cleaning(raw_records, cleaned_records). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
audit_cleaning(raw_records, cleaned_records).

## Slide 43 — audit_cleaning(raw_records, cleaned_records)

PURPOSE
audit_cleaning(raw_records, cleaned_records)

CONNECT
Build on summarize_records(clean_records). Explain why this example is needed before running it.

EXPLAIN
Return raw_count and cleaned_count; duplicate_ids is the number of cleaned records beyond the first occurrence of each record_id; missing_targets counts None targets; invalid_loads counts cleaned load_pct outside 0–100 inclusive.

Report the actual supplied data, which may still contain defects.

Do not change either input.

All five values are integer counts.

LECTURER DETAIL
TEACHING PURPOSE
audit_cleaning(raw_records, cleaned_records)

CONNECT
Build on the preceding slide: summarize_records(clean_records).

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W06/CML3111/A/TASKS.md

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

NEXT
Written evidence. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Written evidence.

## Slide 44 — Written evidence

PURPOSE
Written evidence

CONNECT
Build on audit_cleaning(raw_records, cleaned_records). Explain why this example is needed before running it.

EXPLAIN
Use the cell headed “My written evidence”.

Explain the supplied scenario in your own words.

State target units, reasons and limitations.

Submit one complete notebook containing code and written evidence.

LECTURER DETAIL
TEACHING PURPOSE
Written evidence

CONNECT
Build on the preceding slide: audit_cleaning(raw_records, cleaned_records).

LECTURER CUE
Published criterion weights and exact requirements remain in TASKS.md. Broader project exercises are formative and do not add weekly marks. Local automated reasoning assessment remains subject to its release checks.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Cleaning and quality submission. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Cleaning and quality submission.

## Slide 45 — Cleaning and quality submission

PURPOSE
Cleaning and quality submission

CONNECT
Build on Written evidence. Explain why this example is needed before running it.

EXPLAIN
Opens: 16 Oct 2026, 11:00 Kampala

Deadline: 23 Oct 2026, 11:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

LECTURER DETAIL
TEACHING PURPOSE
Cleaning and quality submission

CONNECT
Build on the preceding slide: Written evidence.

LECTURER CUE
The form link is cohort-specific. Recheck the live form and release status before class. These scheduled assignment dates are separate from the quiz activation window. The issued brief defines the required files, even if the form accepts additional formats. Source: data/submission_links.json

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Project preparation. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Project preparation.

## Slide 46 — Project preparation

PURPOSE
Project preparation

CONNECT
Build on Cleaning and quality submission. Explain why this example is needed before running it.

EXPLAIN
Use the published data analysis project brief.

Build the evidence gradually in your project notebook.

Keep raw data, labelled charts, run instructions and individual contributions.

Published deadline: 30 Oct 2026, 11:00 Kampala

LECTURER DETAIL
TEACHING PURPOSE
Project preparation

CONNECT
Build on the preceding slide: Cleaning and quality submission.

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
Week 6 quiz. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Week 6 quiz.

## Slide 47 — Week 6 quiz

PURPOSE
Week 6 quiz

CONNECT
Build on Project preparation. Explain why this example is needed before running it.

EXPLAIN
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

The lecturer will confirm the exact closing time.

LECTURER DETAIL
TEACHING PURPOSE
Week 6 quiz

CONNECT
Build on the preceding slide: Project preparation.

LECTURER CUE
Activate the matching open_W6_CML3111 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

QUIZ OPERATION
Opening the student link does not activate the quiz. In Quiz Controls run the matching open_W<week>_<cohort> function once when ready. Announce the logged closing time: 24 hours after activation. Five minutes describes expected answering time, not the availability window. Quiz 1 and Quiz 2 require separate activation when collecting catch-up work.

NEXT
Before you leave. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Before you leave.

## Slide 48 — Revision and submission checklist

PURPOSE
Revision and submission checklist

CONNECT
Build on Week 6 quiz. Explain why this example is needed before running it.

EXPLAIN
You can justify a change, show its effect and identify an estimated value.

Save your work and check the required submission files.

LECTURER DETAIL
TEACHING PURPOSE
Before you leave

CONNECT
Build on the preceding slide: Week 6 quiz.

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
Optional revision video.

## Slide 49 — Optional revision video

PURPOSE
Optional revision video

CONNECT
Build on Revision and submission checklist. Explain why this example is needed before running it.

EXPLAIN
For revision after class.

StatQuest with Josh Starmer
Boxplots are Awesome!!!

Opening up to 04:00, optional preview-selected excerpt

Listening question: What does the box show, and does a point outside it prove an error?

LECTURER DETAIL
TEACHING PURPOSE
Short explainer and discussion

CONNECT
Build on the preceding slide: A compact loop is optional.

LECTURER CUE
Linked by the official StatQuest video index. Full audiovisual preview and excerpt timing still required; do not make viewing compulsory.
After viewing: Explain why an unusual temperature needs investigation before deletion.
Preview before class and stop after the selected short excerpt. If playback fails, teach the worked example. Video is optional. Source: https://www.youtube.com/watch?v=fHLhBnmwUM0

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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
independent revision and the issued task.
