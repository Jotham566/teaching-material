# CML3113 Week06 Mining Petroleum

Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.

## Slide 1 — Cleaning data and explaining changes

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

## Slide 2 — Today’s learning

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

## Slide 3 — Recall and a first attempt

TEACHING PURPOSE
Recall and a first attempt

CONNECT
Build on the preceding slide: Today’s learning.

LECTURER CUE
Allow two minutes for everyone to try. Ask pairs to compare. If many cannot begin, show the first step and repeat with changed values. Checkpoint for today: Students distinguish repeated equipment from duplicate records and explain why an outlier is not automatically deleted.

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
Words we will use. Move on after a learner can explain the current example or required action.

## Slide 5 — Words we will use

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

## Slide 6 — Words we will use

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

## Slide 7 — An unusual value needs a reason

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

## Slide 8 — Mean, median and unusual readings

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

## Slide 9 — Filling a gap adds an estimate

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

## Slide 10 — Worked example (1/2)

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

## Slide 11 — Worked example (2/2)

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

## Slide 12 — Expected output

TEACHING PURPOSE
Expected output

CONNECT
Build on the preceding slide: Worked example (2/2).

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

NEXT
Copy a record and remember an ID. Move on after a learner can explain the current example or required action.

## Slide 13 — Copy a record and remember an ID

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

## Slide 14 — A working copy preserves the original

TEACHING PURPOSE
A working copy preserves the original

CONNECT
Build on the preceding slide: Copy a record and remember an ID.

LECTURER CUE
Ask students to describe what they see before introducing terminology. Generated conceptual teaching illustration. The working-copy rule is a toy activity, not the exact assessed cleaning policy. Source: figs/experiential/ASSET_SOURCES.md.

NEXT
Copies and duplicate checks. Move on after a learner can explain the current example or required action.

## Slide 15 — Copies and duplicate checks

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

## Slide 16 — Copying records and recognising repeats

TEACHING PURPOSE
Copying records and recognising repeats

CONNECT
Build on the preceding slide: Copies and duplicate checks.

LECTURER CUE
set() creates a collection of already-seen identifiers. in checks membership. continue skips the rest of that iteration. dict(row) copies a record so later edits do not change the original. Different record IDs from the same equipment remain legitimate observations.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

NEXT
Following a cleaning loop. Move on after a learner can explain the current example or required action.

## Slide 17 — Following a cleaning loop

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

## Slide 18 — Copying records and recognising repeats in Python (1/2)

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

## Slide 19 — Copying records and recognising repeats in Python (2/2)

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

## Slide 20 — Summaries returned as a dictionary

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

## Slide 21 — Summaries returned as a dictionary in Python

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

## Slide 22 — Reading a blank field

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

## Slide 23 — Reading a blank field in Python

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

## Slide 24 — Audit

TEACHING PURPOSE
Audit

CONNECT
Build on the preceding slide: Reading a blank field in Python.

POINT TO THE DEFINITION
Audit: A count and explanation of what changed, why it changed and how many records remain.

NEXT
Every cleaning change needs a record. Move on after a learner can explain the current example or required action.

## Slide 25 — Every cleaning change needs a record

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

## Slide 26 — You are the cleaning audit

TEACHING PURPOSE
You are the cleaning audit

CONNECT
Build on the preceding slide: Every cleaning change needs a record.

LECTURER CUE
Do this before revealing the discussion slide. One learner moves or writes the items, the other checks. Swap roles. Every student explains one step. Expected: The working records are A:20, B:22, C:24. One duplicate was removed and one blank was filled. 22 is an estimate, not a recovered measurement.
Wait for an individual prediction before inviting pair discussion. Give a first-step hint if needed.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

NEXT
What the activity shows. Move on after a learner can explain the current example or required action.

## Slide 27 — What the activity shows

TEACHING PURPOSE
What the activity shows

CONNECT
Build on the preceding slide: You are the cleaning audit.

LECTURER CUE
Ask which step produced this answer. Return to the concrete action if a learner cannot explain it. This is practice feedback, never a quiz key.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
Chart axes. Move on after a learner can explain the current example or required action.

## Slide 28 — Chart axes

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

## Slide 29 — A scatter plot pairs two measurements

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

## Slide 30 — Choose a chart after naming the question

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

## Slide 31 — Choosing a chart for the question

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

## Slide 32 — A chart with labelled axes

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

## Slide 33 — A chart with labelled axes in Python

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

## Slide 34 — Comparing groups and a distribution

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

## Slide 35 — Comparing groups and a distribution in Python (1/2)

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

## Slide 36 — Comparing groups and a distribution in Python (2/2)

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

## Slide 37 — Your turn

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
CML3113   Week 6   38
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
Practice discussion. Move on after a learner can explain the current example or required action.

## Slide 38 — Practice discussion

TEACHING PURPOSE
Practice discussion

CONNECT
Build on the preceding slide: Your turn.

LECTURER CUE
Ask how the result was obtained. Reteach the smallest missing step instead of giving a longer lecture.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

NEXT
A compact loop is optional. Move on after a learner can explain the current example or required action.

## Slide 39 — A compact loop is optional

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

## Slide 40 — Short explainer and discussion

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

## Slide 41 — After the video

TEACHING PURPOSE
After the video

CONNECT
Build on the preceding slide: Short explainer and discussion.

DELIVER THIS SLIDE
Read the stated purpose, then point to the named example or action on the slide. Ask learners to describe what they will do before moving on. For a break slide, announce the return time; for a section divider, name the next concrete task.

NEXT
Preparing for the assignment. Move on after a learner can explain the current example or required action.

## Slide 42 — Preparing for the assignment

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

## Slide 43 — Preparing for the assignment continued

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

## Slide 44 — Cleaning choices and charts

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

## Slide 45 — Cleaning choices and charts continued

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

## Slide 46 — Your issued task

TEACHING PURPOSE
Your issued task

CONNECT
Build on the preceding slide: Cleaning choices and charts continued.

LECTURER CUE
Investigate crusher energy demand. Target units: kWh/t. These are synthetic teaching records, not measurements suitable for deployment. Each record is one operating observation; equipment_id repeats across observations.

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

## Slide 47 — clean_records(records)

TEACHING PURPOSE
clean_records(records)

CONNECT
Build on the preceding slide: Your issued task.

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W06/CML3113/A/TASKS.md

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
summarize_records(clean_records). Move on after a learner can explain the current example or required action.

## Slide 48 — summarize_records(clean_records)

TEACHING PURPOSE
summarize_records(clean_records)

CONNECT
Build on the preceding slide: clean_records(records).

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W06/CML3113/A/TASKS.md

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

NEXT
audit_cleaning(raw_records, cleaned_records). Move on after a learner can explain the current example or required action.

## Slide 49 — audit_cleaning(raw_records, cleaned_records)

TEACHING PURPOSE
audit_cleaning(raw_records, cleaned_records)

CONNECT
Build on the preceding slide: summarize_records(clean_records).

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W06/CML3113/A/TASKS.md

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

NEXT
Written evidence. Move on after a learner can explain the current example or required action.

## Slide 50 — Written evidence

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

## Slide 51 — Cleaning and quality submission

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

## Slide 52 — Project preparation

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

## Slide 53 — Week 6 quiz

TEACHING PURPOSE
Week 6 quiz

CONNECT
Build on the preceding slide: Project preparation.

LECTURER CUE
Activate the matching open_W6_CML3113 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

QUIZ OPERATION
Opening the student link does not activate the quiz. In Quiz Controls run the matching open_W<week>_<cohort> function once when ready. Announce the logged closing time: 24 hours after activation. Five minutes describes expected answering time, not the availability window. Quiz 1 and Quiz 2 require separate activation when collecting catch-up work.

NEXT
Before you leave. Move on after a learner can explain the current example or required action.

## Slide 54 — Before you leave

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

