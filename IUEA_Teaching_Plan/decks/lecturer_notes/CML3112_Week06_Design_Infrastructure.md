# CML3112 Week06 Design Infrastructure

Lecturer companion. The same explanations are embedded in the PowerPoint speaker notes. Open Presenter View, or expand the Notes pane when preparing.

## Slide 1 — Cleaning data and explaining changes

Cleaning data and explaining changes
CML3112, Week 6, slide 1

Explanation to give
Inspect quality before interpreting a chart. Preserve raw records and justify each removal or estimated value.

Worked illustration / lecturer answer
A blank is not a measured zero. With observed values 20 and 24, median filling would insert an estimate of 22, which must be recorded as estimated.

Misconception to address
Use this as an orientation to the lesson. Terms and syntax will be unpacked on their own slides; students do not need to know them in advance.

On this slide
Civil Engineering and Architecture

Continue to
Today’s learning

## Slide 2 — Today’s learning

Today’s learning
CML3112, Week 6, slide 2

Explanation to give
Inspect quality before interpreting a chart. Preserve raw records and justify each removal or estimated value.

Worked illustration / lecturer answer
A blank is not a measured zero. With observed values 20 and 24, median filling would insert an estimate of 22, which must be recorded as estimated.

Misconception to address
At the end, check the specific outcome shown here using a small previously demonstrated example. A completed file without an explanation is not evidence of understanding.

On this slide
Recognise missing values and repeated records.

Make a working copy and record each cleaning action.

Continue to
Connection to the previous lesson

## Slide 3 — Connection to the previous lesson

Connection to the previous lesson
CML3112, Week 6, slide 3

Explanation to give
Inspect quality before interpreting a chart. Preserve raw records and justify each removal or estimated value.

Worked illustration / lecturer answer
A blank is not a measured zero. With observed values 20 and 24, median filling would insert an estimate of 22, which must be recorded as estimated.

Misconception to address
Connect this to the previous result named on this slide. Demonstrate the first step again if necessary; there is no requirement for partner work before the explanation.

On this slide
Week 5 selected and summarised columns. Before trusting those summaries, inspect missing values, repeated observations and measurement units.

Continue to
Why this week’s tools are needed

## Slide 4 — Why this week’s tools are needed

Why this week’s tools are needed
CML3112, Week 6, slide 4

Explanation to give
Inspect quality before interpreting a chart. Preserve raw records and justify each removal or estimated value.

Worked illustration / lecturer answer
A blank is not a measured zero. With observed values 20 and 24, median filling would insert an estimate of 22, which must be recorded as estimated.

Misconception to address
Connect this to the previous result named on this slide. Demonstrate the first step again if necessary; there is no requirement for partner work before the explanation.

On this slide
A repeated record or a missing measurement can change a summary. We keep the original records, apply the stated cleaning rules and explain each change before plotting.

Continue to
Raw data and Missing value

## Slide 5 — Raw data and Missing value

Raw data and Missing value
CML3112, Week 6, slide 5

Explanation to give
Raw data is the original record of what was received. Work on a copy and record changes. Missing means unrecorded; zero may be a valid reading. An unusual value is a reason to investigate, not automatic permission to delete.

Worked illustration / lecturer answer
A temperature sensor can genuinely report zero degrees. A blank temperature conveys no reading. Treating both as zero would change the mean and disguise missingness.

Misconception to address
A negative value can be physically valid in some units and impossible in others. Use the stated measurement and instrument context.

On this slide
Raw data: The original supplied records. Keep these unchanged so another person can check your decisions.
Missing value: A value that was not recorded, represented here by None in Python records. Missing does not automatically mean zero.

Continue to
Record and equipment ID and Median and imputation

## Slide 6 — Record and equipment ID and Median and imputation

Record and equipment ID and Median and imputation
CML3112, Week 6, slide 6

Explanation to give
Sort the observed numbers to find the median. For an odd count use the middle number; for an even count average the two middle numbers. Imputation inserts an estimate for a missing value and should be recorded as an estimate.

Worked illustration / lecturer answer
For 2, 4 and 90, the median is 4 while the mean is 32. For 2, 4, 6 and 8, the median is (4 + 6) / 2 = 5.

Misconception to address
Do not put a missing marker into the arithmetic. A median can be less affected by an extreme reading but does not reconstruct the lost truth.

On this slide
Record and equipment ID: A record ID identifies an observation. An equipment ID identifies the source and may repeat legitimately. Remove repeated observations only under the stated rule.
Median and imputation: The median is the middle sorted value, or the mean of the two middle values. Imputation fills a missing value using an explicit rule and introduces uncertainty.

Continue to
An unusual value needs a reason

## Slide 7 — An unusual value needs a reason

An unusual value needs a reason
CML3112, Week 6, slide 7

Explanation to give
Raw data is the original record of what was received. Work on a copy and record changes. Missing means unrecorded; zero may be a valid reading. An unusual value is a reason to investigate, not automatic permission to delete.

Worked illustration / lecturer answer
A temperature sensor can genuinely report zero degrees. A blank temperature conveys no reading. Treating both as zero would change the mean and disguise missingness.

Misconception to address
A negative value can be physically valid in some units and impossible in others. Use the stated measurement and instrument context.

On this slide
A missing reading has no recorded value.

Zero is a recorded value and may be physically meaningful.

A large or negative value needs instrument and unit context.

Preserve the raw data and record every cleaning decision.

Continue to
Find the median by sorting the readings

## Slide 8 — Find the median by sorting the readings

Find the median by sorting the readings
CML3112, Week 6, slide 8

Explanation to give
Sort the observed numbers to find the median. For an odd count use the middle number; for an even count average the two middle numbers. Imputation inserts an estimate for a missing value and should be recorded as an estimate.

Worked illustration / lecturer answer
For 2, 4 and 90, the median is 4 while the mean is 32. For 2, 4, 6 and 8, the median is (4 + 6) / 2 = 5.

Misconception to address
Do not put a missing marker into the arithmetic. A median can be less affected by an extreme reading but does not reconstruct the lost truth.

On this slide
The median is a middle value after ordering the numbers from smallest to largest. In [2, 4, 30], the middle item is 4.

With an even number of readings, average the two middle values. [20, 22, 24, 80] has middle values 22 and 24, so the median is 23.

None is missing information in our list, not a number to sort. Collect only recorded values before calculating this median.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Mean, median and unusual readings

## Slide 9 — Mean, median and unusual readings

Mean, median and unusual readings
CML3112, Week 6, slide 9

Explanation to give
Sort the observed numbers to find the median. For an odd count use the middle number; for an even count average the two middle numbers. Imputation inserts an estimate for a missing value and should be recorded as an estimate.

Worked illustration / lecturer answer
For 2, 4 and 90, the median is 4 while the mean is 32. For 2, 4, 6 and 8, the median is (4 + 6) / 2 = 5.

Misconception to address
Do not put a missing marker into the arithmetic. A median can be less affected by an extreme reading but does not reconstruct the lost truth.

On this slide
Readings | Mean | Median
2, 4, 6 | 4 | 4
2, 4, 30 | 12 | 4
The mean uses every value. The median is the middle sorted value. A large value needs context.

Continue to
Testing for None and importing one tool

## Slide 10 — Testing for None and importing one tool

Testing for None and importing one tool
CML3112, Week 6, slide 10

Explanation to give
Read “is None” as a check for Python's designated missing-result value in these records. It is different from asking whether the number equals zero or whether a string is empty.

Worked illustration / lecturer answer
For values [0, None, 4], testing value is not None retains 0 and 4. Testing merely if value would discard the valid zero too.

Misconception to address
A CSV blank is initially "", not None. The loader must convert it deliberately if the later function expects None.

On this slide
value is None asks whether value is the special None object. value is not None is the opposite question. Use these tests for Python None.

This differs from ==, which compares values. Do not use is to compare ordinary numeric measurements.

from statistics import median loads just the median function. statistics is a standard Python module; median is the callable tool used below.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Filling a gap adds an estimate

## Slide 11 — Filling a gap adds an estimate

Filling a gap adds an estimate
CML3112, Week 6, slide 11

Explanation to give
Sort the observed numbers to find the median. For an odd count use the middle number; for an even count average the two middle numbers. Imputation inserts an estimate for a missing value and should be recorded as an estimate.

Worked illustration / lecturer answer
For 2, 4 and 90, the median is 4 while the mean is 32. For 2, 4, 6 and 8, the median is (4 + 6) / 2 = 5.

Misconception to address
Do not put a missing marker into the arithmetic. A median can be less affected by an extreme reading but does not reconstruct the lost truth.

On this slide
The valid readings, sorted, are 20, 22, 24 and 80.

The two middle values are 22 and 24. Their mean is 23.

Using 23 for a blank is a declared cleaning rule. It does not recover the lost measurement.

In Python, value is None tests for a missing marker. is not None tests that it is not that marker.

Continue to
Cleaning decisions and charts in Python (1/2)

## Slide 12 — Cleaning decisions and charts in Python (1/2)

Cleaning decisions and charts in Python (1/2)
CML3112, Week 6, slide 12

Explanation to give
Explain why cleaning precedes the chart. A repeated observation can count twice; a missing value should not silently become a measured zero. Every change needs an explicit rule and a retained original.

Worked illustration / lecturer answer
Compare the raw record count with the cleaned count, then show which fields were estimated. A chart caption should say whether it uses observed values, filled values or both.

Misconception to address
Do not choose a cleaning rule merely because it makes the chart smoother. The rule must follow the task and the measurement context.

Read the displayed code line by line
from statistics import median
Bring the named tool from this library into the current Python session.

raw = [20, None, 22, 24, 80]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

known = []
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

for value in raw:
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

if value is not None:
Evaluate this yes/no condition. Execute its indented body only on the matching path.

known.append(value)
Evaluate the argument and add it as one new item at the end of this list.

fill = median(known)
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

cleaned = []
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Cleaning decisions and charts in Python (2/2)

## Slide 13 — Cleaning decisions and charts in Python (2/2)

Cleaning decisions and charts in Python (2/2)
CML3112, Week 6, slide 13

Explanation to give
Explain why cleaning precedes the chart. A repeated observation can count twice; a missing value should not silently become a measured zero. Every change needs an explicit rule and a retained original.

Worked illustration / lecturer answer
Compare the raw record count with the cleaned count, then show which fields were estimated. A chart caption should say whether it uses observed values, filled values or both.

Misconception to address
Do not choose a cleaning rule merely because it makes the chart smoother. The rule must follow the task and the measurement context.

Read the displayed code line by line
for value in raw:
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

if value is None:
Evaluate this yes/no condition. Execute its indented body only on the matching path.

cleaned.append(fill)
Evaluate the argument and add it as one new item at the end of this list.

else:
Use this remaining path when the matching earlier condition did not succeed.

cleaned.append(value)
Evaluate the argument and add it as one new item at the end of this list.

print(fill)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(raw)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(cleaned)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Continue the SAME cell; keep indentation. Run after all parts are entered.

Continue to
Cleaning decisions and charts results

## Slide 14 — Cleaning decisions and charts results

Cleaning decisions and charts results
CML3112, Week 6, slide 14

Explanation to give
Explain why cleaning precedes the chart. A repeated observation can count twice; a missing value should not silently become a measured zero. Every change needs an explicit rule and a retained original.

Worked illustration / lecturer answer
Compare the raw record count with the cleaned count, then show which fields were estimated. A chart caption should say whether it uses observed values, filled values or both.

Misconception to address
Do not choose a cleaning rule merely because it makes the chart smoother. The rule must follow the task and the measurement context.

On this slide
23.0
[20, None, 22, 24, 80]
[20, 23.0, 22, 24, 80]

Continue to
Copy a record and remember an ID

## Slide 15 — Copy a record and remember an ID

Copy a record and remember an ID
CML3112, Week 6, slide 15

Explanation to give
A record ID identifies a particular observation. Equipment ID identifies the source and may repeat legitimately. Keep a set of observation IDs already retained and copy records before altering fields.

Worked illustration / lecturer answer
For record IDs A, B, B, retain the first A and first B under a first-occurrence rule. Two different records from the same meter remain different observations.

Misconception to address
Do not deduplicate by equipment ID unless instructed. row.copy() protects top-level scalar fields but is only a shallow copy if nested mutable objects exist.

On this slide
dict(row): For our flat records, dict(row) makes a separate dictionary with the same fields. Changing a number in the copy leaves the original record unchanged.
set, in, add and continue: set() starts an empty collection of unique items. in checks membership; add remembers an item. continue skips the rest of the current loop pass.

Continue to
A working copy preserves the original

## Slide 16 — A working copy preserves the original

A working copy preserves the original
CML3112, Week 6, slide 16

Explanation to give
A record ID identifies a particular observation. Equipment ID identifies the source and may repeat legitimately. Keep a set of observation IDs already retained and copy records before altering fields.

Worked illustration / lecturer answer
For record IDs A, B, B, retain the first A and first B under a first-occurrence rule. Two different records from the same meter remain different observations.

Misconception to address
Do not deduplicate by equipment ID unless instructed. row.copy() protects top-level scalar fields but is only a shallow copy if nested mutable objects exist.

On this slide
In this separate four-record example, remove one repeated C record and fill B with (20 + 24) / 2 = 22.

Continue to
Copies and duplicate checks

## Slide 17 — Copies and duplicate checks

Copies and duplicate checks
CML3112, Week 6, slide 17

Explanation to give
A record ID identifies a particular observation. Equipment ID identifies the source and may repeat legitimately. Keep a set of observation IDs already retained and copy records before altering fields.

Worked illustration / lecturer answer
For record IDs A, B, B, retain the first A and first B under a first-occurrence rule. Two different records from the same meter remain different observations.

Misconception to address
Do not deduplicate by equipment ID unless instructed. row.copy() protects top-level scalar fields but is only a shallow copy if nested mutable objects exist.

Read the displayed code line by line
row = {"id": "A", "reading": 4}
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

copy = dict(row)
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

copy["reading"] = 5
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

seen = set()
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

seen.add(row["id"])
Remember this item in the set. Adding the same item again does not create a duplicate.

print(row["reading"])
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print("A" in seen)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
dict(row) makes a shallow copy. A set keeps unique IDs.

Continue to
Trace the duplicate-record decision

## Slide 18 — Trace the duplicate-record decision

Trace the duplicate-record decision
CML3112, Week 6, slide 18

Explanation to give
A record ID identifies a particular observation. Equipment ID identifies the source and may repeat legitimately. Keep a set of observation IDs already retained and copy records before altering fields.

Worked illustration / lecturer answer
For record IDs A, B, B, retain the first A and first B under a first-occurrence rule. Two different records from the same meter remain different observations.

Misconception to address
Do not deduplicate by equipment ID unless instructed. row.copy() protects top-level scalar fields but is only a shallow copy if nested mutable objects exist.

On this slide
Record ID | Already in seen? | Action
1, first record | No | Remember 1; keep a copy
1, repeated record | Yes | continue; skip this copy
2, next record | No | Remember 2; keep a copy
This example removes repeated record IDs, not every observation from repeated equipment.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Following a cleaning loop

## Slide 19 — Following a cleaning loop

Following a cleaning loop
CML3112, Week 6, slide 19

Explanation to give
A record ID identifies a particular observation. Equipment ID identifies the source and may repeat legitimately. Keep a set of observation IDs already retained and copy records before altering fields.

Worked illustration / lecturer answer
For record IDs A, B, B, retain the first A and first B under a first-occurrence rule. Two different records from the same meter remain different observations.

Misconception to address
Do not deduplicate by equipment ID unless instructed. row.copy() protects top-level scalar fields but is only a shallow copy if nested mutable objects exist.

On this slide
Expression | Meaning
seen = set() | Start an empty collection of IDs
record_id in seen | Has this ID already been recorded?
continue | Skip the remaining lines for this item
value is None | Check for Python’s no-value marker
An empty string "" and None are different values. Parse CSV fields according to the issued rule.

Continue to
Copying records and recognising repeats in Python (1/2)

## Slide 20 — Copying records and recognising repeats in Python (1/2)

Copying records and recognising repeats in Python (1/2)
CML3112, Week 6, slide 20

Explanation to give
A record ID identifies a particular observation. Equipment ID identifies the source and may repeat legitimately. Keep a set of observation IDs already retained and copy records before altering fields.

Worked illustration / lecturer answer
For record IDs A, B, B, retain the first A and first B under a first-occurrence rule. Two different records from the same meter remain different observations.

Misconception to address
Do not deduplicate by equipment ID unless instructed. row.copy() protects top-level scalar fields but is only a shallow copy if nested mutable objects exist.

Read the displayed code line by line
raw_records = [{"id": 1, "equipment": "A", "value": 10},
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

{"id": 1, "equipment": "A", "value": 10},
This line continues the surrounding expression or block; read it together with the preceding line rather than running it alone.

{"id": 2, "equipment": "A", "value": 12}]
This line continues the surrounding expression or block; read it together with the preceding line rather than running it alone.

seen = set()
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

kept = []
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Copying records and recognising repeats in Python (2/2)

## Slide 21 — Copying records and recognising repeats in Python (2/2)

Copying records and recognising repeats in Python (2/2)
CML3112, Week 6, slide 21

Explanation to give
A record ID identifies a particular observation. Equipment ID identifies the source and may repeat legitimately. Keep a set of observation IDs already retained and copy records before altering fields.

Worked illustration / lecturer answer
For record IDs A, B, B, retain the first A and first B under a first-occurrence rule. Two different records from the same meter remain different observations.

Misconception to address
Do not deduplicate by equipment ID unless instructed. row.copy() protects top-level scalar fields but is only a shallow copy if nested mutable objects exist.

Read the displayed code line by line
for row in raw_records:
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

if row["id"] in seen:
Evaluate this yes/no condition. Execute its indented body only on the matching path.

continue
Skip the rest of this iteration and proceed to the next item.

seen.add(row["id"])
Remember this item in the set. Adding the same item again does not create a duplicate.

kept.append(dict(row))
Evaluate the argument and add it as one new item at the end of this list.

print(len(raw_records), len(kept))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Continue the SAME cell; keep indentation. Run after all parts are entered.

Continue to
Summaries returned as a dictionary

## Slide 22 — Summaries returned as a dictionary

Summaries returned as a dictionary
CML3112, Week 6, slide 22

Explanation to give
A dictionary labels fields with keys. A list organises records by position. Explain each lookup in a nested expression separately rather than saying it all at once.

Worked illustration / lecturer answer
records[0]["reading"] first selects the first record, then finds its reading field. In {"unit": "A", "reading": 4}, the key reading retrieves 4 regardless of its visual position.

Misconception to address
Using a missing key with square brackets raises KeyError. get("missing", 0) uses 0 only if the key is absent, not when its existing value is None.

On this slide
This example expects a nonempty list.

It calculates a count and mean, then returns a dictionary with named outputs.

Use the exact keys specified by the issued task when adapting this pattern.

Continue to
Summaries returned as a dictionary in Python

## Slide 23 — Summaries returned as a dictionary in Python

Summaries returned as a dictionary in Python
CML3112, Week 6, slide 23

Explanation to give
A dictionary labels fields with keys. A list organises records by position. Explain each lookup in a nested expression separately rather than saying it all at once.

Worked illustration / lecturer answer
records[0]["reading"] first selects the first record, then finds its reading field. In {"unit": "A", "reading": 4}, the key reading retrieves 4 regardless of its visual position.

Misconception to address
Using a missing key with square brackets raises KeyError. get("missing", 0) uses 0 only if the key is absent, not when its existing value is None.

Read the displayed code line by line
def describe(values):
Store these instructions under this function name. Names in parentheses are its inputs; the body waits until a call.

count = len(values)
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

mean = sum(values) / count
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

return {"count": count, "mean": mean}
Evaluate this result and send it to the caller, ending this function call.

print(describe([10, 12]))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Reading a blank field

## Slide 24 — Reading a blank field

Reading a blank field
CML3112, Week 6, slide 24

Explanation to give
Inspect a field before converting it. A blank string represents no recorded number here. Converting that blank with float raises ValueError, so handle the missing case explicitly.

Worked illustration / lecturer answer
For text values ["2", "", "4"], skip the blank and convert the other two to 2.0 and 4.0. Their mean is 3.0 using count 2, not count 3.

Misconception to address
Do not convert blank to zero merely to silence an error. Zero is a measurement. Catch only the expected conversion failure so unrelated coding errors remain visible.

On this slide
CSV values start as text.

The if/else below stores None for a blank.

Otherwise float converts the text into a number.

Continue to
Reading a blank field in Python

## Slide 25 — Reading a blank field in Python

Reading a blank field in Python
CML3112, Week 6, slide 25

Explanation to give
Inspect a field before converting it. A blank string represents no recorded number here. Converting that blank with float raises ValueError, so handle the missing case explicitly.

Worked illustration / lecturer answer
For text values ["2", "", "4"], skip the blank and convert the other two to 2.0 and 4.0. Their mean is 3.0 using count 2, not count 3.

Misconception to address
Do not convert blank to zero merely to silence an error. Zero is a measurement. Catch only the expected conversion failure so unrelated coding errors remain visible.

Read the displayed code line by line
text_values = ["20", "", "24"]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

parsed = []
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

for text in text_values:
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

if text == "":
Evaluate this yes/no condition. Execute its indented body only on the matching path.

parsed.append(None)
Evaluate the argument and add it as one new item at the end of this list.

else:
Use this remaining path when the matching earlier condition did not succeed.

parsed.append(float(text))
Evaluate the argument and add it as one new item at the end of this list.

print(parsed)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Audit

## Slide 26 — Audit

Audit
CML3112, Week 6, slide 26

Explanation to give
An audit describes the difference between the received data and the retained data. State what was counted and why a record was removed or a field filled. Return named counts so another reader can verify the accounting.

Worked illustration / lecturer answer
If 5 raw records become 4 after one duplicate removal, raw_count is 5 and cleaned_count is 4. A filled field changes a value but does not by itself remove a record.

Misconception to address
Several defect counts can overlap on the same record. Do not add them as if they were mutually exclusive removals unless your counting rule guarantees that.

On this slide
Audit: A count and explanation of what changed, why it changed and how many records remain.

Continue to
Every cleaning change needs a record

## Slide 27 — Every cleaning change needs a record

Every cleaning change needs a record
CML3112, Week 6, slide 27

Explanation to give
An audit describes the difference between the received data and the retained data. State what was counted and why a record was removed or a field filled. Return named counts so another reader can verify the accounting.

Worked illustration / lecturer answer
If 5 raw records become 4 after one duplicate removal, raw_count is 5 and cleaned_count is 4. A filled field changes a value but does not by itself remove a record.

Misconception to address
Several defect counts can overlap on the same record. Do not add them as if they were mutually exclusive removals unless your counting rule guarantees that.

On this slide
A duplicate record ID suggests a repeated observation.

Two different observations from the same equipment can both be valid.

Record the evidence, action, number of affected rows and limitation.

Continue to
Chart axes

## Slide 28 — Chart axes

Chart axes
CML3112, Week 6, slide 28

Explanation to give
Explain a scatter point as a pair of measurements from one observation. The horizontal coordinate comes from the x variable, the vertical coordinate from y. Name units before describing a pattern.

Worked illustration / lecturer answer
A point at (20, 8) on a temperature-versus-load plot means that observation had 20 degrees and load 8 in the labelled unit. It does not show the eighth observation at time 20.

Misconception to address
Association in a plot does not establish causation. fig is the complete Figure; ax is its plotting area. Return the Figure when the assignment requires it.

On this slide
Chart axes: A chart maps values to positions. Read the horizontal variable, vertical variable and their units before interpreting a pattern.

Continue to
A scatter plot pairs two measurements

## Slide 29 — A scatter plot pairs two measurements

A scatter plot pairs two measurements
CML3112, Week 6, slide 29

Explanation to give
Explain a scatter point as a pair of measurements from one observation. The horizontal coordinate comes from the x variable, the vertical coordinate from y. Name units before describing a pattern.

Worked illustration / lecturer answer
A point at (20, 8) on a temperature-versus-load plot means that observation had 20 degrees and load 8 in the labelled unit. It does not show the eighth observation at time 20.

Misconception to address
Association in a plot does not establish causation. fig is the complete Figure; ax is its plotting area. Return the Figure when the assignment requires it.

On this slide
The horizontal axis gives the input value.

The vertical axis gives the corresponding reading.

One point represents one observation. A pattern alone does not prove causation.

Continue to
Choose a chart after naming the question

## Slide 30 — Choose a chart after naming the question

Choose a chart after naming the question
CML3112, Week 6, slide 30

Explanation to give
Choose the chart from the question. A bar chart compares named categories; a histogram counts numerical observations in intervals; a scatter plot compares paired numbers. Explain what one mark means.

Worked illustration / lecturer answer
Use bars for mean energy by building, a histogram for the distribution of individual energy readings, and scatter for energy against temperature. A histogram bar's height counts observations in a bin.

Misconception to address
Histogram bins are numerical intervals, not separate named buildings. Changing bin widths can change the visible pattern, so state the choice and inspect the data too.

On this slide
Scatter and bar: A scatter plot places one point for each paired measurement. A bar chart compares values across named groups. Label both axes and their units.
Histogram and bins: A histogram counts observations in numerical intervals called bins. The horizontal axis is the measurement; the vertical axis is a count. Bin edges affect its appearance.

Continue to
Choosing a chart for the question

## Slide 31 — Choosing a chart for the question

Choosing a chart for the question
CML3112, Week 6, slide 31

Explanation to give
Choose the chart from the question. A bar chart compares named categories; a histogram counts numerical observations in intervals; a scatter plot compares paired numbers. Explain what one mark means.

Worked illustration / lecturer answer
Use bars for mean energy by building, a histogram for the distribution of individual energy readings, and scatter for energy against temperature. A histogram bar's height counts observations in a bin.

Misconception to address
Histogram bins are numerical intervals, not separate named buildings. Changing bin widths can change the visible pattern, so state the choice and inspect the data too.

On this slide
This week uses histograms, scatter plots and bar charts. The other chart types are reference examples.

Continue to
A chart with labelled axes

## Slide 32 — A chart with labelled axes

A chart with labelled axes
CML3112, Week 6, slide 32

Explanation to give
Explain a scatter point as a pair of measurements from one observation. The horizontal coordinate comes from the x variable, the vertical coordinate from y. Name units before describing a pattern.

Worked illustration / lecturer answer
A point at (20, 8) on a temperature-versus-load plot means that observation had 20 degrees and load 8 in the labelled unit. It does not show the eighth observation at time 20.

Misconception to address
Association in a plot does not establish causation. fig is the complete Figure; ax is its plotting area. Return the Figure when the assignment requires it.

On this slide
matplotlib is a plotting library. plt is the short name we give its pyplot module.

fig, ax = plt.subplots() returns two objects: fig is the whole figure; ax is its plotting area. scatter places the paired measurements as points.

ax.set_xlabel(...) labels the horizontal axis. set_ylabel labels the vertical axis. Keep fig when the task asks you to return a Figure object.

Continue to
A chart with labelled axes in Python

## Slide 33 — A chart with labelled axes in Python

A chart with labelled axes in Python
CML3112, Week 6, slide 33

Explanation to give
Explain a scatter point as a pair of measurements from one observation. The horizontal coordinate comes from the x variable, the vertical coordinate from y. Name units before describing a pattern.

Worked illustration / lecturer answer
A point at (20, 8) on a temperature-versus-load plot means that observation had 20 degrees and load 8 in the labelled unit. It does not show the eighth observation at time 20.

Misconception to address
Association in a plot does not establish causation. fig is the complete Figure; ax is its plotting area. Return the Figure when the assignment requires it.

Read the displayed code line by line
import matplotlib.pyplot as plt
Load this library. An alias after as is the shorter name used below.

inputs = [1, 2, 3, 4]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

readings = [12, 14, 13, 18]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

fig, ax = plt.subplots()
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

ax.scatter(inputs, readings)
Plot one point for each aligned x/y pair.

ax.set_xlabel("Input (teaching units)")
Label the horizontal axis with the named quantity and unit.

ax.set_ylabel("Reading (teaching units)")
Label the vertical axis with the named quantity and unit.

ax.set_title("Four invented observations")
This line continues the surrounding expression or block; read it together with the preceding line rather than running it alone.

plt.show()
This line continues the surrounding expression or block; read it together with the preceding line rather than running it alone.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
A bar chart and a histogram count different things

## Slide 34 — A bar chart and a histogram count different things

A bar chart and a histogram count different things
CML3112, Week 6, slide 34

Explanation to give
Choose the chart from the question. A bar chart compares named categories; a histogram counts numerical observations in intervals; a scatter plot compares paired numbers. Explain what one mark means.

Worked illustration / lecturer answer
Use bars for mean energy by building, a histogram for the distribution of individual energy readings, and scatter for energy against temperature. A histogram bar's height counts observations in a bin.

Misconception to address
Histogram bins are numerical intervals, not separate named buildings. Changing bin widths can change the visible pattern, so state the choice and inspect the data too.

On this slide
A bar chart has named groups. bar(["A", "B"], [13, 16]) makes one bar for each supplied group value.

A histogram divides a numeric range into intervals called bins. hist(readings, bins=2) counts readings in two intervals.

With [12, 14, 13, 18], the intervals run from 12 to 15 and 15 to 18. Counts are 3 and 1; the final interval includes the last endpoint.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Comparing groups and a distribution

## Slide 35 — Comparing groups and a distribution

Comparing groups and a distribution
CML3112, Week 6, slide 35

Explanation to give
Choose the chart from the question. A bar chart compares named categories; a histogram counts numerical observations in intervals; a scatter plot compares paired numbers. Explain what one mark means.

Worked illustration / lecturer answer
Use bars for mean energy by building, a histogram for the distribution of individual energy readings, and scatter for energy against temperature. A histogram bar's height counts observations in a bin.

Misconception to address
Histogram bins are numerical intervals, not separate named buildings. Changing bin widths can change the visible pattern, so state the choice and inspect the data too.

On this slide
bar compares one value for each named group. hist counts observations in value intervals called bins.

Read the bar labels and both axes.

This practice uses two bins; follow the exact bin rule in the test brief.

Save and keep the Figure objects when a task asks for them.

Continue to
Comparing groups and a distribution in Python (1/2)

## Slide 36 — Comparing groups and a distribution in Python (1/2)

Comparing groups and a distribution in Python (1/2)
CML3112, Week 6, slide 36

Explanation to give
Choose the chart from the question. A bar chart compares named categories; a histogram counts numerical observations in intervals; a scatter plot compares paired numbers. Explain what one mark means.

Worked illustration / lecturer answer
Use bars for mean energy by building, a histogram for the distribution of individual energy readings, and scatter for energy against temperature. A histogram bar's height counts observations in a bin.

Misconception to address
Histogram bins are numerical intervals, not separate named buildings. Changing bin widths can change the visible pattern, so state the choice and inspect the data too.

Read the displayed code line by line
bar_fig, bar_ax = plt.subplots()
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

bar_ax.bar(["A", "B"], [13, 16])
Draw one bar for each named category with the supplied height.

bar_ax.set_xlabel("Group")
Label the horizontal axis with the named quantity and unit.

bar_ax.set_ylabel("Mean reading (teaching units)")
Label the vertical axis with the named quantity and unit.

bar_ax.set_title("Two invented group means")
This line continues the surrounding expression or block; read it together with the preceding line rather than running it alone.

hist_fig, hist_ax = plt.subplots()
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

hist_ax.hist(readings, bins=2)
Count numerical observations into intervals and display those counts.

hist_ax.set_xlabel("Reading (teaching units)")
Label the horizontal axis with the named quantity and unit.

hist_ax.set_ylabel("Count of observations")
Label the vertical axis with the named quantity and unit.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Comparing groups and a distribution in Python (2/2)

## Slide 37 — Comparing groups and a distribution in Python (2/2)

Comparing groups and a distribution in Python (2/2)
CML3112, Week 6, slide 37

Explanation to give
Choose the chart from the question. A bar chart compares named categories; a histogram counts numerical observations in intervals; a scatter plot compares paired numbers. Explain what one mark means.

Worked illustration / lecturer answer
Use bars for mean energy by building, a histogram for the distribution of individual energy readings, and scatter for energy against temperature. A histogram bar's height counts observations in a bin.

Misconception to address
Histogram bins are numerical intervals, not separate named buildings. Changing bin widths can change the visible pattern, so state the choice and inspect the data too.

Read the displayed code line by line
hist_ax.set_title("Distribution of four observations")
This line continues the surrounding expression or block; read it together with the preceding line rather than running it alone.

plt.show()
This line continues the surrounding expression or block; read it together with the preceding line rather than running it alone.

Result / continuity
Continue the SAME cell; keep indentation. Run after all parts are entered.

Continue to
Revision example and answer

## Slide 38 — Revision example and answer

Revision example and answer
CML3112, Week 6, slide 38

Explanation to give
Use the displayed example as a short individual revision question, then explain the reasoning behind its answer.

Worked illustration / lecturer answer
Example: Explain why 80 was retained. Replace 24 with 26, predict the new fill value, and check that cleaning still leaves raw unchanged.

Answer: An unusual value alone does not prove an error. The task did not authorize deleting 80. With 26 replacing 24, the middle known values are 22 and 26, so the new fill is 24. The raw list still contains None.

Misconception to address
Trace the operation that changes the value rather than accepting a memorised output. For notebook-state examples, specify which cell is repeated and whether the initialisation ran again.

Continue to
Read a list comprehension after the full loop

## Slide 39 — Read a list comprehension after the full loop

Read a list comprehension after the full loop
CML3112, Week 6, slide 39

Explanation to give
A comprehension is a compact way to construct a list. First show the equivalent full loop so the learner can identify the expression, the iteration and any condition.

Worked illustration / lecturer answer
squares = [x * x for x in [2, 3]] means initialise an empty list, take 2 then 3, and append each square. The result is [4, 9].

Misconception to address
This syntax is optional for these beginner tasks. A clear full loop is acceptable when it returns the required result.

On this slide
A list comprehension builds a new list using an expression for each visited item. [value * 2 for value in readings] doubles each reading.

Its first part says what to store; its for part says which items supply value. [2, 4, 6] becomes [4, 8, 12].

This compact spelling is optional. Use the expanded loop already taught when that is easier to explain.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
A compact loop is optional

## Slide 40 — A compact loop is optional

A compact loop is optional
CML3112, Week 6, slide 40

Explanation to give
A comprehension is a compact way to construct a list. First show the equivalent full loop so the learner can identify the expression, the iteration and any condition.

Worked illustration / lecturer answer
squares = [x * x for x in [2, 3]] means initialise an empty list, take 2 then 3, and append each square. The result is [4, 9].

Misconception to address
This syntax is optional for these beginner tasks. A clear full loop is acceptable when it returns the required result.

Read the displayed code line by line
readings = [2, 4, 6]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

doubled = []
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

for value in readings:
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

doubled.append(value * 2)
Evaluate the argument and add it as one new item at the end of this list.

print(doubled)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print([value * 2 for value in readings])
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
A list comprehension makes the same list. Learn the ordinary loop first.

Continue to
Preparing for the assignment

## Slide 41 — Preparing for the assignment

Preparing for the assignment
CML3112, Week 6, slide 41

Explanation to give
Describe the received table before changing it: its rows, columns, units and defects. Then explain each cleaning rule and preserve the original data.

Worked illustration / lecturer answer
A duplicate record ID and repeated equipment ID are different situations. Removing the former under a stated rule may be correct while removing the latter could discard legitimate observations.

Misconception to address
A correct output without a justification may not satisfy the reasoning criterion. Use the task’s exact rules rather than choosing whichever cleaning makes results look attractive.

On this slide
W06 uses a list of record dictionaries.

Show one record and one field lookup before the function interfaces.

Parse CSV blank numeric cells as None. dict(row) copies a record. append adds an item to a list.

The task brief specifies the cleaning order and returned outputs.

Continue to
Preparing for the assignment continued

## Slide 42 — Preparing for the assignment continued

Preparing for the assignment continued
CML3112, Week 6, slide 42

Explanation to give
Keep related equipment observations together so the validation really represents equipment the model has not seen.

Worked illustration / lecturer answer
The written question may supply a comparison scenario. Label those numbers as supplied scenario evidence; do not claim they came from a run of your own notebook.

Misconception to address
A supplied scenario and an observed experimental result have different provenance. Both can be interpreted, but should not be confused.

On this slide
A set records IDs already seen.

Group summaries collect readings with the same equipment ID.

Write your explanations in the My written evidence section.

Continue to
Cleaning choices and charts

## Slide 43 — Cleaning choices and charts

Cleaning choices and charts
CML3112, Week 6, slide 43

Explanation to give
Explain why cleaning precedes the chart. A repeated observation can count twice; a missing value should not silently become a measured zero. Every change needs an explicit rule and a retained original.

Worked illustration / lecturer answer
Compare the raw record count with the cleaned count, then show which fields were estimated. A chart caption should say whether it uses observed values, filled values or both.

Misconception to address
Do not choose a cleaning rule merely because it makes the chart smoother. The rule must follow the task and the measurement context.

On this slide
Filling blanks with zero changes the mean and may be unjustified.

Dropping every row with any blank can remove valid observations.

A failed numeric conversion identifies a problematic value to inspect rather than hide.

A histogram describes one distribution; a scatter plot shows paired values; a grouped chart compares groups.

Continue to
Cleaning choices and charts continued

## Slide 44 — Cleaning choices and charts continued

Cleaning choices and charts continued
CML3112, Week 6, slide 44

Explanation to give
Explain why cleaning precedes the chart. A repeated observation can count twice; a missing value should not silently become a measured zero. Every change needs an explicit rule and a retained original.

Worked illustration / lecturer answer
Compare the raw record count with the cleaned count, then show which fields were estimated. A chart caption should say whether it uses observed values, filled values or both.

Misconception to address
Do not choose a cleaning rule merely because it makes the chart smoother. The rule must follow the task and the measurement context.

On this slide
Read both axes and units.

A plausible extreme needs investigation before deletion.

Continue to
Your issued task

## Slide 45 — Your issued task

Your issued task
CML3112, Week 6, slide 45

Explanation to give
Name this cohort’s target and its unit exactly as displayed. Each row is one operating observation, while equipment_id can repeat across several observations.

Worked illustration / lecturer answer
Explain record_id as the identifier of an observation, load_pct as load expressed in percent and ambient_c as temperature in degrees Celsius. The target records the known answer in training data.

Misconception to address
These are synthetic examples for learning. They do not establish a calibrated physical relationship or justify operation of real equipment.

On this slide
Investigate building cooling load.

Target units: kW.

These are synthetic teaching records, not measurements suitable for deployment.

Each record is one operating observation; equipment_id repeats across observations.

Continue to
clean_records(records)

## Slide 46 — clean_records(records)

clean_records(records)
CML3112, Week 6, slide 46

Explanation to give
Follow the stated cleaning order and record-ID policy on copied records. Preserve the caller’s input and keep legitimate repeated equipment observations.

Worked illustration / lecturer answer
An estimated replacement belongs only in the specified field. A row dropped earlier must not influence a later training or cleaning statistic.

Misconception to address
Keep the exact output names and required types. Use the task text for the learner’s own assessed answer; the alternate example explains the method without replacing their work.

On this slide
Return copied records in original order: remove repeated record_id after its first occurrence, drop rows with missing target or load_pct outside 0–100 inclusive, then fill missing ambient_c with the median of retained non-missing ambient_c values.

Preserve raw input.

No other changes.

Continue to
summarize_records(clean_records)

## Slide 47 — summarize_records(clean_records)

summarize_records(clean_records)
CML3112, Week 6, slide 47

Explanation to give
Produce a dictionary from each group label to its own mean, using each group’s valid count.

Worked illustration / lecturer answer
Group A with readings 2 and 4 has mean 3. Group B with a single 9 has mean 9. Dividing both by the overall count would be wrong.

Misconception to address
Keep the exact output names and required types. Use the task text for the learner’s own assessed answer; the alternate example explains the method without replacing their work.

On this slide
Return count, mean, minimum, maximum of target and group_means by equipment_id.

Retain full precision.

Continue to
audit_cleaning(raw_records, cleaned_records)

## Slide 48 — audit_cleaning(raw_records, cleaned_records)

audit_cleaning(raw_records, cleaned_records)
CML3112, Week 6, slide 48

Explanation to give
Inspect the two lists actually passed in. Report their counts and any specified defects still present after cleaning; do not assume the cleaned input is flawless.

Worked illustration / lecturer answer
If an independently supplied cleaned list still contains one repeated record ID, the audit must report that remaining defect rather than return zero by assumption.

Misconception to address
Keep the exact output names and required types. Use the task text for the learner’s own assessed answer; the alternate example explains the method without replacing their work.

On this slide
Return raw_count and cleaned_count; duplicate_ids is the number of cleaned records beyond the first occurrence of each record_id; missing_targets counts None targets; invalid_loads counts cleaned load_pct outside 0–100 inclusive.

Report the actual supplied data, which may still contain defects.

Do not change either input.

All five values are integer counts.

Continue to
Written evidence

## Slide 49 — Written evidence

Written evidence
CML3112, Week 6, slide 49

Explanation to give
Show the actual markdown answer cell headed My written evidence. This is where the learner explains the choices and the supplied scenario in their own words.

Worked illustration / lecturer answer
A useful explanation connects a decision to a named result and its limitation: for example, why a training-only median avoids using evaluation information. Describe supplied scenario figures as supplied, not as measurements the learner produced.

Misconception to address
Prompts and copied code comments do not substitute for the learner’s reasoning. Weekly work and tests use the notebook; projects also require their separate readable report.

On this slide
Use the cell headed “My written evidence”.

Explain the supplied scenario in your own words.

State target units, reasons and limitations.

Submit one complete notebook containing code and written evidence.

Continue to
Cleaning and quality submission

## Slide 50 — Cleaning and quality submission

Cleaning and quality submission
CML3112, Week 6, slide 50

Explanation to give
This slide hands over CML3112 W06. Show the exact form title before uploading. The required packet is one completed .ipynb notebook.

Worked illustration / lecturer answer
The recorded cutoff for this form is 2026-10-20T11:00:00+03:00. Check the live form for later changes. A replacement must contain the complete required file set, not just the changed file.

Misconception to address
Students enter their own Student Registration Number as required freeform text. They wait for filenames to appear, press Submit and keep the confirmation. A file saved in Drive or GitHub is not itself a form submission.

On this slide
Opens: 13 Oct 2026, 11:00 Kampala

Deadline: 20 Oct 2026, 11:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

Continue to
Project preparation

## Slide 51 — Project preparation

Project preparation
CML3112, Week 6, slide 51

Explanation to give
Make contribution evidence specific enough to check. A seed records the starting state of random choices; a contribution log records who produced and explained which work.

Worked illustration / lecturer answer
Name a file, function or chart and the decision behind it. Match that entry to meaningful repository history. Disclose AI assistance according to the assessment policy.

Misconception to address
Many commits do not necessarily mean substantial work, and a seed does not establish accuracy. Both are supporting evidence, not replacements for the analysis.

On this slide
Use the published data analysis project brief.

Build the evidence gradually in your project notebook.

Keep raw data, labelled charts, run instructions and individual contributions.

Published deadline: 27 Oct 2026, 11:00 Kampala

Continue to
Week 6 quiz

## Slide 52 — Week 6 quiz

Week 6 quiz
CML3112, Week 6, slide 52

Explanation to give
This is the CML3112 Week 6 quiz. The student link opens the response form; it does not activate its window. In Quiz Controls use open_W6_CML3112 when ready and read the logged closing time.

Worked illustration / lecturer answer
Explain the distinction between the expected answering time and availability: five minutes of questions can still be available for 24 hours after activation. Enter the learner’s own Student Registration Number and use the registered Google account.

Misconception to address
Read the exact live cutoff before announcing it. Do not promise a new attempt to somebody who already submitted. Quiz catch-up and assignment uploads are separate forms.

On this slide
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

Check the announced quiz closing time.

Continue to
Revision and submission checklist

## Slide 53 — Revision and submission checklist

Revision and submission checklist
CML3112, Week 6, slide 53

Explanation to give
Inspect quality before interpreting a chart. Preserve raw records and justify each removal or estimated value.

Worked illustration / lecturer answer
A blank is not a measured zero. With observed values 20 and 24, median filling would insert an estimate of 22, which must be recorded as estimated.

Misconception to address
Close by identifying the actual saved file and its correct submission route. Read the live deadline. For current weekly notebook tasks, students upload their own work, not the practice notebook, ZIP or grading files.

On this slide
You can justify a change, show its effect and identify an estimated value.

Save your work and check the required submission files.

Continue to
Optional revision video

## Slide 54 — Optional revision video

Optional revision video
CML3112, Week 6, slide 54

Explanation to give
Give the viewing question before playing the excerpt: What does the box show, and does a point outside it prove an error?

Worked illustration / lecturer answer
Use the adjacent worked example as the explanation if the video cannot load. Pause after the relevant example and connect its terms to the names and units already used in this lesson. Preview the displayed link and excerpt before class.

Misconception to address
The video is supporting revision, not a replacement for defining the symbols or a requirement to watch a full tutorial during limited class time.

On this slide
For revision after class.

StatQuest with Josh Starmer
Boxplots are Awesome!!!

Opening up to 04:00, optional preview-selected excerpt

Listening question: What does the box show, and does a point outside it prove an error?

Reference / existing resource
https://www.youtube.com/watch?v=fHLhBnmwUM0
