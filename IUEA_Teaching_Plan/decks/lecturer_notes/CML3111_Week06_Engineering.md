# CML3111 Week06 Engineering

Lecturer companion to the revised PowerPoint. Slide numbers match this edition. Explain the worked examples directly; revision checks are for individual study.

## Slide 1 — Cleaning data and explaining changes

PURPOSE
Cleaning data and explaining changes

CONNECT
Previous slide: the preceding week.

EXPLAIN
Communications, Electrical, Mechatronics and Robotics Engineering

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
Previous slide: Cleaning data and explaining changes.

EXPLAIN
Recognise missing values and repeated records.

Make a working copy and record each cleaning action.

LECTURER CUE
Ask learners to explain this goal in ordinary language. The first successful attempt matters more than covering optional extensions. Defer: MCAR/MAR/MNAR names, five chart families and six unaided defect hunts are reference. Teach missingness causes in everyday language first.

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
Week 5 selected and summarised columns. Before trusting those summaries, inspect missing values, repeated observations and measurement units.

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
A repeated record or a missing measurement can change a summary. We keep the original records, apply the stated cleaning rules and explain each change before plotting.

LECTURER CUE
A team records device temperature to investigate cooling. Use a communications cabinet, an electrical enclosure or a robot controller as the physical example. No specialist hardware knowledge is assumed.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Raw data and Missing value.

REFERENCES


## Slide 5 — Raw data and Missing value

PURPOSE
Raw data and Missing value

CONNECT
Previous slide: Why this week’s tools are needed.

EXPLAIN
Raw data: The original supplied records. Keep these unchanged so another person can check your decisions.

Missing value: A value that was not recorded, represented here by None in Python records. Missing does not automatically mean zero.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Record and equipment ID and Median and imputation.

REFERENCES


## Slide 6 — Record and equipment ID and Median and imputation

PURPOSE
Record and equipment ID and Median and imputation

CONNECT
Previous slide: Raw data and Missing value.

EXPLAIN
Record and equipment ID: A record ID identifies an observation. An equipment ID identifies the source and may repeat legitimately. Remove repeated observations only under the stated rule.

Median and imputation: The median is the middle sorted value, or the mean of the two middle values. Imputation fills a missing value using an explicit rule and introduces uncertainty.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
An unusual value needs a reason.

REFERENCES


## Slide 7 — An unusual value needs a reason

PURPOSE
An unusual value needs a reason

CONNECT
Previous slide: Record and equipment ID and Median and imputation.

EXPLAIN
A missing reading has no recorded value.

Zero is a recorded value and may be physically meaningful.

A large or negative value needs instrument and unit context.

Preserve the raw data and record every cleaning decision.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Find the median by sorting the readings.

REFERENCES


## Slide 8 — Find the median by sorting the readings

PURPOSE
Find the median by sorting the readings

CONNECT
Previous slide: An unusual value needs a reason.

EXPLAIN
The median is a middle value after ordering the numbers from smallest to largest. In [2, 4, 30], the middle item is 4.

With an even number of readings, average the two middle values. [20, 22, 24, 80] has middle values 22 and 24, so the median is 23.

None is missing information in our list, not a number to sort. Collect only recorded values before calculating this median.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Mean, median and unusual readings.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 9 — Mean, median and unusual readings

PURPOSE
Mean, median and unusual readings

CONNECT
Previous slide: Find the median by sorting the readings.

EXPLAIN
Readings | Mean | Median

2, 4, 6 | 4 | 4

2, 4, 30 | 12 | 4

The mean uses every value. The median is the middle sorted value. A large value needs context.

LECTURER CUE
The mean uses every value. The median is the middle sorted value. A large value needs context.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Testing for None and importing one tool.

REFERENCES


## Slide 10 — Testing for None and importing one tool

PURPOSE
Testing for None and importing one tool

CONNECT
Previous slide: Mean, median and unusual readings.

EXPLAIN
value is None asks whether value is the special None object. value is not None is the opposite question. Use these tests for Python None.

This differs from ==, which compares values. Do not use is to compare ordinary numeric measurements.

from statistics import median loads just the median function. statistics is a standard Python module; median is the callable tool used below.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Filling a gap adds an estimate.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 11 — Filling a gap adds an estimate

PURPOSE
Filling a gap adds an estimate

CONNECT
Previous slide: Testing for None and importing one tool.

EXPLAIN
The valid readings, sorted, are 20, 22, 24 and 80.

The two middle values are 22 and 24. Their mean is 23.

Using 23 for a blank is a declared cleaning rule. It does not recover the lost measurement.

In Python, value is None tests for a missing marker. is not None tests that it is not that marker.

LECTURER CUE
Use the example below to sort four valid readings. The median is (22 + 24) / 2 = 23. Filling a blank with 23 is a stated teaching rule, not a recovered measurement.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Worked example (1/2).

REFERENCES


## Slide 12 — Cleaning decisions and charts in Python (1/2)

PURPOSE
Cleaning decisions and charts in Python (1/2)

CONNECT
Previous slide: Filling a gap adds an estimate.

EXPLAIN
Read the code in this order:
from statistics import median
raw = [20, None, 22, 24, 80]
known = []
for value in raw:
    if value is not None:
        known.append(value)
fill = median(known)
cleaned = []

import loads a library. from selects a tool from it.

for takes the next item. The indented block repeats.

if tests a condition. The chosen indented block runs.

Read top to bottom. Run the complete example in the matching practice notebook.

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

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Worked example (2/2).

REFERENCES


## Slide 13 — Cleaning decisions and charts in Python (2/2)

PURPOSE
Cleaning decisions and charts in Python (2/2)

CONNECT
Previous slide: Cleaning decisions and charts in Python (1/2).

EXPLAIN
Read the code in this order:
for value in raw:
    if value is None:
        cleaned.append(fill)
    else:
        cleaned.append(value)
print(fill)
print(raw)
print(cleaned)

for takes the next item. The indented block repeats.

if tests a condition. The chosen indented block runs.

print displays a value below the cell.

Continue the SAME cell; keep indentation. Run after all parts are entered.

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

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Expected output.

REFERENCES


## Slide 14 — Cleaning decisions and charts results

PURPOSE
Cleaning decisions and charts results

CONNECT
Previous slide: Cleaning decisions and charts in Python (2/2).

EXPLAIN
23.0
[20, None, 22, 24, 80]
[20, 23.0, 22, 24, 80]

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Copy a record and remember an ID.

REFERENCES


## Slide 15 — Copy a record and remember an ID

PURPOSE
Copy a record and remember an ID

CONNECT
Previous slide: Cleaning decisions and charts results.

EXPLAIN
dict(row): For our flat records, dict(row) makes a separate dictionary with the same fields. Changing a number in the copy leaves the original record unchanged.

set, in, add and continue: set() starts an empty collection of unique items. in checks membership; add remembers an item. continue skips the rest of the current loop pass.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A working copy preserves the original.

REFERENCES


## Slide 16 — A working copy preserves the original

PURPOSE
A working copy preserves the original

CONNECT
Previous slide: Copy a record and remember an ID.

EXPLAIN
In this separate four-record example, remove one repeated C record and fill B with (20 + 24) / 2 = 22.

LECTURER CUE
Ask students to describe what they see before introducing terminology. Generated conceptual teaching illustration. The working-copy rule is a toy activity, not the exact assessed cleaning policy. Source: figs/experiential/ASSET_SOURCES.md.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Copies and duplicate checks.

REFERENCES


## Slide 17 — Copies and duplicate checks

PURPOSE
Copies and duplicate checks

CONNECT
Previous slide: A working copy preserves the original.

EXPLAIN
Read the code in this order:
row = {"id": "A", "reading": 4}
copy = dict(row)
copy["reading"] = 5
seen = set()
seen.add(row["id"])
print(row["reading"])
print("A" in seen)

print displays a value below the cell.

Square brackets create a list or select an item.

Braces hold dictionary key: value pairs here.

dict(row) makes a shallow copy. A set keeps unique IDs.

LECTURER CUE
Read each symbol before running. Ask everyone to predict. Expected output: 4 then True. The example has only scalar fields. A shallow copy does not independently copy nested lists.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Trace the duplicate-record decision.

REFERENCES


## Slide 18 — Trace the duplicate-record decision

PURPOSE
Trace the duplicate-record decision

CONNECT
Previous slide: Copies and duplicate checks.

EXPLAIN
Record ID | Already in seen? | Action

1, first record | No | Remember 1; keep a copy

1, repeated record | Yes | continue; skip this copy

2, next record | No | Remember 2; keep a copy

This example removes repeated record IDs, not every observation from repeated equipment.

Read the rows in order. This example removes repeated record IDs, not every observation from repeated equipment.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Following a cleaning loop.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 19 — Following a cleaning loop

PURPOSE
Following a cleaning loop

CONNECT
Previous slide: Trace the duplicate-record decision.

EXPLAIN
Expression | Meaning

seen = set() | Start an empty collection of IDs

record_id in seen | Has this ID already been recorded?

continue | Skip the remaining lines for this item

value is None | Check for Python’s no-value marker

An empty string "" and None are different values. Parse CSV fields according to the issued rule.

LECTURER CUE
Read one row at a time and use a changed value. This is a syntax reference for the worked examples.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Copying records and recognising repeats in Python (1/2).

REFERENCES


## Slide 20 — Copying records and recognising repeats in Python (1/2)

PURPOSE
Copying records and recognising repeats in Python (1/2)

CONNECT
Previous slide: Following a cleaning loop.

EXPLAIN
Read the code in this order:
raw_records = [{"id": 1, "equipment": "A", "value": 10},
               {"id": 1, "equipment": "A", "value": 10},
               {"id": 2, "equipment": "A", "value": 12}]
seen = set()
kept = []

Square brackets create a list or select an item.

Braces hold dictionary key: value pairs here.

= assigns the value on the right to the name on the left.

Read top to bottom. Run the complete example in the matching practice notebook.

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

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Copying records and recognising repeats in Python (2/2).

REFERENCES


## Slide 21 — Copying records and recognising repeats in Python (2/2)

PURPOSE
Copying records and recognising repeats in Python (2/2)

CONNECT
Previous slide: Copying records and recognising repeats in Python (1/2).

EXPLAIN
Read the code in this order:
for row in raw_records:
    if row["id"] in seen:
        continue
    seen.add(row["id"])
    kept.append(dict(row))
print(len(raw_records), len(kept))

for takes the next item. The indented block repeats.

if tests a condition. The chosen indented block runs.

print displays a value below the cell.

Continue the SAME cell; keep indentation. Run after all parts are entered.

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

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Summaries returned as a dictionary.

REFERENCES


## Slide 22 — Summaries returned as a dictionary

PURPOSE
Summaries returned as a dictionary

CONNECT
Previous slide: Copying records and recognising repeats in Python (2/2).

EXPLAIN
This example expects a nonempty list.

It calculates a count and mean, then returns a dictionary with named outputs.

Use the exact keys specified by the issued task when adapting this pattern.

LECTURER CUE
This example expects a nonempty list. It calculates a count and mean, then returns a dictionary with named outputs. Use the exact keys specified by the issued task when adapting this pattern.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Summaries returned as a dictionary in Python.

REFERENCES


## Slide 23 — Summaries returned as a dictionary in Python

PURPOSE
Summaries returned as a dictionary in Python

CONNECT
Previous slide: Summaries returned as a dictionary.

EXPLAIN
Read the code in this order:
def describe(values):
    count = len(values)
    mean = sum(values) / count
    return {"count": count, "mean": mean}

print(describe([10, 12]))

def names the function. Inputs go inside parentheses.

return sends the result back to the caller.

print displays a value below the cell.

Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER CUE
This example expects a nonempty list. It calculates a count and mean, then returns a dictionary with named outputs. Use the exact keys specified by the issued task when adapting this pattern.

Complete practice code:
def describe(values):
    count = len(values)
    mean = sum(values) / count
    return {"count": count, "mean": mean}

print(describe([10, 12]))

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Reading a blank field.

REFERENCES


## Slide 24 — Reading a blank field

PURPOSE
Reading a blank field

CONNECT
Previous slide: Summaries returned as a dictionary in Python.

EXPLAIN
CSV values start as text.

The if/else below stores None for a blank.

Otherwise float converts the text into a number.

LECTURER CUE
CSV values start as text. The if/else below stores None for a blank. Otherwise float converts the text into a number.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Reading a blank field in Python.

REFERENCES


## Slide 25 — Reading a blank field in Python

PURPOSE
Reading a blank field in Python

CONNECT
Previous slide: Reading a blank field.

EXPLAIN
Read the code in this order:
text_values = ["20", "", "24"]
parsed = []
for text in text_values:
    if text == "":
        parsed.append(None)
    else:
        parsed.append(float(text))
print(parsed)

for takes the next item. The indented block repeats.

if tests a condition. The chosen indented block runs.

float converts numeric text into a decimal number.

Read top to bottom. Run the complete example in the matching practice notebook.

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

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Audit.

REFERENCES


## Slide 26 — Audit

PURPOSE
Audit

CONNECT
Previous slide: Reading a blank field in Python.

EXPLAIN
Audit: A count and explanation of what changed, why it changed and how many records remain.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Every cleaning change needs a record.

REFERENCES


## Slide 27 — Every cleaning change needs a record

PURPOSE
Every cleaning change needs a record

CONNECT
Previous slide: Audit.

EXPLAIN
A duplicate record ID suggests a repeated observation.

Two different observations from the same equipment can both be valid.

Record the evidence, action, number of affected rows and limitation.

LECTURER CUE
Model a defect register: observation, evidence, decision, affected count, limitation. Work one repeated record and one missing value together.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Chart axes.

REFERENCES


## Slide 28 — Chart axes

PURPOSE
Chart axes

CONNECT
Previous slide: Every cleaning change needs a record.

EXPLAIN
Chart axes: A chart maps values to positions. Read the horizontal variable, vertical variable and their units before interpreting a pattern.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A scatter plot pairs two measurements.

REFERENCES


## Slide 29 — A scatter plot pairs two measurements

PURPOSE
A scatter plot pairs two measurements

CONNECT
Previous slide: Chart axes.

EXPLAIN
The horizontal axis gives the input value.

The vertical axis gives the corresponding reading.

One point represents one observation. A pattern alone does not prove causation.

LECTURER CUE
Draw a scatter plot from four pairs on the board. A pattern can motivate investigation without proving that one variable causes the other.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Choose a chart after naming the question.

REFERENCES


## Slide 30 — Choose a chart after naming the question

PURPOSE
Choose a chart after naming the question

CONNECT
Previous slide: A scatter plot pairs two measurements.

EXPLAIN
Scatter and bar: A scatter plot places one point for each paired measurement. A bar chart compares values across named groups. Label both axes and their units.

Histogram and bins: A histogram counts observations in numerical intervals called bins. The horizontal axis is the measurement; the vertical axis is a count. Bin edges affect its appearance.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Choosing a chart for the question.

REFERENCES


## Slide 31 — Choosing a chart for the question

PURPOSE
Choosing a chart for the question

CONNECT
Previous slide: Choose a chart after naming the question.

EXPLAIN
This week uses histograms, scatter plots and bar charts. The other chart types are reference examples.

LECTURER CUE
Name the question answered by each chart. Correlation does not establish causation. A bar chart usually needs a zero baseline.
Source: existing course illustration figs/chart_chooser.png. These are illustrative examples, not this cohort’s assessed results.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A chart with labelled axes.

REFERENCES
Source: existing course illustration figs/chart_chooser.png. These are illustrative examples, not this cohort’s assessed results.

## Slide 32 — A chart with labelled axes

PURPOSE
A chart with labelled axes

CONNECT
Previous slide: Choosing a chart for the question.

EXPLAIN
matplotlib is a plotting library. plt is the short name we give its pyplot module.

fig, ax = plt.subplots() returns two objects: fig is the whole figure; ax is its plotting area. scatter places the paired measurements as points.

ax.set_xlabel(...) labels the horizontal axis. set_ylabel labels the vertical axis. Keep fig when the task asks you to return a Figure object.

LECTURER CUE
matplotlib draws charts. subplots creates a Figure, the whole page, and Axes, the plotting area. scatter pairs each input with its corresponding reading. The horizontal axis is the input and the vertical axis is the reading. A pattern alone does not prove causation. In the test, return Figure objects as the brief specifies.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A chart with labelled axes in Python.

REFERENCES


## Slide 33 — A chart with labelled axes in Python

PURPOSE
A chart with labelled axes in Python

CONNECT
Previous slide: A chart with labelled axes.

EXPLAIN
Read the code in this order:
import matplotlib.pyplot as plt
inputs = [1, 2, 3, 4]
readings = [12, 14, 13, 18]
fig, ax = plt.subplots()
ax.scatter(inputs, readings)
ax.set_xlabel("Input (teaching units)")
ax.set_ylabel("Reading (teaching units)")
ax.set_title("Four invented observations")
plt.show()

import loads a library. from selects a tool from it.

Square brackets create a list or select an item.

= assigns the value on the right to the name on the left.

Read top to bottom. Run the complete example in the matching practice notebook.

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

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A bar chart and a histogram count different things.

REFERENCES


## Slide 34 — A bar chart and a histogram count different things

PURPOSE
A bar chart and a histogram count different things

CONNECT
Previous slide: A chart with labelled axes in Python.

EXPLAIN
A bar chart has named groups. bar(["A", "B"], [13, 16]) makes one bar for each supplied group value.

A histogram divides a numeric range into intervals called bins. hist(readings, bins=2) counts readings in two intervals.

With [12, 14, 13, 18], the intervals run from 12 to 15 and 15 to 18. Counts are 3 and 1; the final interval includes the last endpoint.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Comparing groups and a distribution.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 35 — Comparing groups and a distribution

PURPOSE
Comparing groups and a distribution

CONNECT
Previous slide: A bar chart and a histogram count different things.

EXPLAIN
bar compares one value for each named group. hist counts observations in value intervals called bins.

Read the bar labels and both axes.

This practice uses two bins; follow the exact bin rule in the test brief.

Save and keep the Figure objects when a task asks for them.

LECTURER CUE
bar compares one value for each named group. hist counts observations in value intervals called bins. Read the bar labels and both axes. This practice uses two bins; follow the exact bin rule in the test brief. Save and keep the Figure objects when a task asks for them.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Comparing groups and a distribution in Python (1/2).

REFERENCES


## Slide 36 — Comparing groups and a distribution in Python (1/2)

PURPOSE
Comparing groups and a distribution in Python (1/2)

CONNECT
Previous slide: Comparing groups and a distribution.

EXPLAIN
Read the code in this order:
bar_fig, bar_ax = plt.subplots()
bar_ax.bar(["A", "B"], [13, 16])
bar_ax.set_xlabel("Group")
bar_ax.set_ylabel("Mean reading (teaching units)")
bar_ax.set_title("Two invented group means")
hist_fig, hist_ax = plt.subplots()
hist_ax.hist(readings, bins=2)
hist_ax.set_xlabel("Reading (teaching units)")
hist_ax.set_ylabel("Count of observations")

Square brackets create a list or select an item.

= assigns the value on the right to the name on the left.

Read top to bottom. Run the complete example in the matching practice notebook.

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

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Comparing groups and a distribution in Python (2/2).

REFERENCES


## Slide 37 — Comparing groups and a distribution in Python (2/2)

PURPOSE
Comparing groups and a distribution in Python (2/2)

CONNECT
Previous slide: Comparing groups and a distribution in Python (1/2).

EXPLAIN
Read the code in this order:
hist_ax.set_title("Distribution of four observations")
plt.show()

Read the inputs and identify the operation.

Predict the result before running this cell.

Continue the SAME cell; keep indentation. Run after all parts are entered.

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

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Revision example and answer.

REFERENCES


## Slide 38 — Revision example and answer

PURPOSE
Revision example and answer

CONNECT
Previous slide: Comparing groups and a distribution in Python (2/2).

EXPLAIN
Example: Explain why 80 was retained. Replace 24 with 26, predict the new fill value, and check that cleaning still leaves raw unchanged.

Answer: An unusual value alone does not prove an error. The task did not authorize deleting 80. With 26 replacing 24, the middle known values are 22 and 26, so the new fill is 24. The raw list still contains None.

LECTURER CUE
Give silent thinking time, then let pairs discuss. Rotate who types. This is practice, not a graded quiz. Expected response: An unusual value alone does not prove an error. The task did not authorize deleting 80. With 26 replacing 24, the middle known values are 22 and 26, so the new fill is 24. The raw list still contains None.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Read a list comprehension after the full loop.

REFERENCES


## Slide 39 — Read a list comprehension after the full loop

PURPOSE
Read a list comprehension after the full loop

CONNECT
Previous slide: Revision example and answer.

EXPLAIN
A list comprehension builds a new list using an expression for each visited item. [value * 2 for value in readings] doubles each reading.

Its first part says what to store; its for part says which items supply value. [2, 4, 6] becomes [4, 8, 12].

This compact spelling is optional. Use the expanded loop already taught when that is easier to explain.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A compact loop is optional.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 40 — A compact loop is optional

PURPOSE
A compact loop is optional

CONNECT
Previous slide: Read a list comprehension after the full loop.

EXPLAIN
Read the code in this order:
readings = [2, 4, 6]
doubled = []
for value in readings:
    doubled.append(value * 2)
print(doubled)
# Same operation in compact form:
print([value * 2 for value in readings])

for takes the next item. The indented block repeats.

print displays a value below the cell.

append adds one item to the end of a list.

A list comprehension makes the same list. Learn the ordinary loop first.

LECTURER CUE
Read each symbol before running. Ask everyone to predict. Expected output: [4, 8, 12] twice

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Preparing for the assignment.

REFERENCES


## Slide 41 — Preparing for the assignment

PURPOSE
Preparing for the assignment

CONNECT
Previous slide: A compact loop is optional.

EXPLAIN
W06 uses a list of record dictionaries.

Show one record and one field lookup before the function interfaces.

Parse CSV blank numeric cells as None. dict(row) copies a record. append adds an item to a list.

The task brief specifies the cleaning order and returned outputs.

LECTURER CUE
W06 uses a list of record dictionaries. Show one record and one field lookup before the function interfaces. Parse CSV blank numeric cells as None. Model copying with dict(row) and list.append. Walk through the published cleaning order before students write clean_records, summarize_records and audit_cleaning. Teach set membership for duplicate IDs and grouped accumulation. Explain that written evidence belongs in My written evidence, not in code comments.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Preparing for the assignment continued.

REFERENCES


## Slide 42 — Preparing for the assignment continued

PURPOSE
Preparing for the assignment continued

CONNECT
Previous slide: Preparing for the assignment.

EXPLAIN
A set records IDs already seen.

Group summaries collect readings with the same equipment ID.

Explain that written evidence belongs in My written evidence, not in code comments.

LECTURER CUE
W06 uses a list of record dictionaries. Show one record and one field lookup before the function interfaces. Parse CSV blank numeric cells as None. Model copying with dict(row) and list.append. Walk through the published cleaning order before students write clean_records, summarize_records and audit_cleaning. Teach set membership for duplicate IDs and grouped accumulation. Explain that written evidence belongs in My written evidence, not in code comments.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Cleaning choices and charts.

REFERENCES


## Slide 43 — Cleaning choices and charts

PURPOSE
Cleaning choices and charts

CONNECT
Previous slide: Preparing for the assignment continued.

EXPLAIN
Filling blanks with zero changes the mean and may be unjustified.

Dropping every row with any blank can remove valid observations.

A failed numeric conversion identifies a problematic value to inspect rather than hide.

A histogram describes one distribution; a scatter plot shows paired values; a grouped chart compares groups.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Cleaning choices and charts continued.

REFERENCES


## Slide 44 — Cleaning choices and charts continued

PURPOSE
Cleaning choices and charts continued

CONNECT
Previous slide: Cleaning choices and charts.

EXPLAIN
Read both axes and units.

A plausible extreme needs investigation before deletion.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Your issued task.

REFERENCES


## Slide 45 — Your issued task

PURPOSE
Your issued task

CONNECT
Previous slide: Cleaning choices and charts continued.

EXPLAIN
Investigate motor winding temperature.

Target units: deg C.

These are synthetic teaching records, not measurements suitable for deployment.

Each record is one operating observation; equipment_id repeats across observations.

LECTURER CUE
Investigate motor winding temperature. Target units: deg C. These are synthetic teaching records, not measurements suitable for deployment. Each record is one operating observation; equipment_id repeats across observations.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
clean_records(records).

REFERENCES


## Slide 46 — clean_records(records)

PURPOSE
clean_records(records)

CONNECT
Previous slide: Your issued task.

EXPLAIN
Return copied records in original order: remove repeated record_id after its first occurrence, drop rows with missing target or load_pct outside 0–100 inclusive, then fill missing ambient_c with the median of retained non-missing ambient_c values.

Preserve raw input.

No other changes.

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W06/CML3111/A/TASKS.md

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
summarize_records(clean_records).

REFERENCES


## Slide 47 — summarize_records(clean_records)

PURPOSE
summarize_records(clean_records)

CONNECT
Previous slide: clean_records(records).

EXPLAIN
Return count, mean, minimum, maximum of target and group_means by equipment_id.

Retain full precision.

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W06/CML3111/A/TASKS.md

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
audit_cleaning(raw_records, cleaned_records).

REFERENCES


## Slide 48 — audit_cleaning(raw_records, cleaned_records)

PURPOSE
audit_cleaning(raw_records, cleaned_records)

CONNECT
Previous slide: summarize_records(clean_records).

EXPLAIN
Return raw_count and cleaned_count; duplicate_ids is the number of cleaned records beyond the first occurrence of each record_id; missing_targets counts None targets; invalid_loads counts cleaned load_pct outside 0–100 inclusive.

Report the actual supplied data, which may still contain defects.

Do not change either input.

All five values are integer counts.

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W06/CML3111/A/TASKS.md

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Written evidence.

REFERENCES


## Slide 49 — Written evidence

PURPOSE
Written evidence

CONNECT
Previous slide: audit_cleaning(raw_records, cleaned_records).

EXPLAIN
Use the cell headed “My written evidence”.

Explain the supplied scenario in your own words.

State target units, reasons and limitations.

Submit one complete notebook containing code and written evidence.

LECTURER CUE
Published criterion weights and exact requirements remain in TASKS.md. Broader project exercises are formative and do not add weekly marks. Local automated reasoning assessment remains subject to its release checks.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Cleaning and quality submission.

REFERENCES


## Slide 50 — Cleaning and quality submission

PURPOSE
Cleaning and quality submission

CONNECT
Previous slide: Written evidence.

EXPLAIN
Opens: 16 Oct 2026, 11:00 Kampala

Deadline: 23 Oct 2026, 11:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

LECTURER CUE
The form link is cohort-specific. Recheck the live form and release status before class. These scheduled assignment dates are separate from the quiz activation window. The issued brief defines the required files, even if the form accepts additional formats. Source: data/submission_links.json

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Project preparation.

REFERENCES


## Slide 51 — Project preparation

PURPOSE
Project preparation

CONNECT
Previous slide: Cleaning and quality submission.

EXPLAIN
Use the published data analysis project brief.

Build the evidence gradually in your project notebook.

Keep raw data, labelled charts, run instructions and individual contributions.

Published deadline: 30 Oct 2026, 11:00 Kampala

LECTURER CUE
Explain the released brief now. Confirm its grading-release checks before assigning it. Avoid treating weekly practice as a substitute for the project evidence. The project brief remains authoritative.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Week 6 quiz.

REFERENCES


## Slide 52 — Week 6 quiz

PURPOSE
Week 6 quiz

CONNECT
Previous slide: Project preparation.

EXPLAIN
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

The lecturer will confirm the exact closing time.

LECTURER CUE
Activate the matching open_W6_CML3111 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Before you leave.

REFERENCES


## Slide 53 — Revision and submission checklist

PURPOSE
Revision and submission checklist

CONNECT
Previous slide: Week 6 quiz.

EXPLAIN
You can justify a change, show its effect and identify an estimated value.

Save your work and check the required submission files.

LECTURER CUE
Ask every learner for an individual response. Record one misconception to revisit at the start of the next class. If a deadline changed, announce the exact Kampala date and update the source registry before rebuilding slides.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Optional revision video.

REFERENCES


## Slide 54 — Optional revision video

PURPOSE
Optional revision video

CONNECT
Previous slide: Revision and submission checklist.

EXPLAIN
For revision after class.

StatQuest with Josh Starmer
Boxplots are Awesome!!!

Opening up to 04:00, optional preview-selected excerpt

Listening question: What does the box show, and does a point outside it prove an error?

LECTURER CUE
Linked by the official StatQuest video index. Full audiovisual preview and excerpt timing still required; do not make viewing compulsory.
After viewing: Explain why an unusual temperature needs investigation before deletion.
Preview before class and stop after the selected short excerpt. If playback fails, teach the worked example. Video is optional. Source: https://www.youtube.com/watch?v=fHLhBnmwUM0

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
independent revision and the issued task.

REFERENCES
