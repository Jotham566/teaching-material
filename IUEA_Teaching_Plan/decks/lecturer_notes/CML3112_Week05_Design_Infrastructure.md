# CML3112 Week05 Design Infrastructure

Lecturer companion to the revised PowerPoint. Slide numbers match this edition. Explain the worked examples directly; revision checks are for individual study.

## Slide 1 — Using pandas to answer table questions

PURPOSE
Using pandas to answer table questions

CONNECT
Previous slide: the preceding week.

EXPLAIN
Civil Engineering and Architecture

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
Previous slide: Using pandas to answer table questions.

EXPLAIN
Read a labelled table and select rows.

Calculate column summaries and grouped totals.

LECTURER CUE
Ask learners to explain this goal in ordinary language. The first successful attempt matters more than covering optional extensions. Defer: NumPy broadcasting, broad Kaggle searches and twelve-plus-ten independent questions are optional extension. No change of editor is needed.

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
Week 4 used lists, dictionaries, loops and CSV rows. pandas keeps these same records in a labelled table and provides operations that work across its columns.

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
The supplied campus_energy.csv records campus electricity use. We practise pandas on four invented rows first, then inspect the supplied file and its units.

LECTURER CUE
A building team records indoor temperature to investigate comfort. Civil students can discuss construction and inspection; architecture students can discuss shading and ventilation. Explain the quantities before using them.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Rows columns and units.

REFERENCES


## Slide 5 — Rows columns and units

PURPOSE
Rows columns and units

CONNECT
Previous slide: Why this week’s tools are needed.

EXPLAIN
A row describes one observation. A column describes one field.

A DataFrame is pandas’ labelled table.

A Series is one labelled column.

kWh measures energy. kW measures power.

A data type (dtype) describes the kind of values in a column, such as whole numbers, decimals or text.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A table keeps related observations together.

REFERENCES


## Slide 6 — A table keeps related observations together

PURPOSE
A table keeps related observations together

CONNECT
Previous slide: Rows columns and units.

EXPLAIN
Our four rows record building A twice and building B twice.

Each row contains the building label and an energy reading.

kWh is energy. kW is power. The units describe different quantities.

LECTURER CUE
Draw a four-row table before running the example. Describe a reading of kWh as energy, and kW as power; the units are different.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Our small energy table.

REFERENCES


## Slide 7 — Our small energy table

PURPOSE
Our small energy table

CONNECT
Previous slide: A table keeps related observations together.

EXPLAIN
building | kwh

A | 2

A | 4

B | 5

B | 7

The four observations total 18 kWh.

LECTURER CUE
The four observations total 18 kWh. Their mean is 4.5 kWh. Building totals are A: 6 and B: 12.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Library and pandas and DataFrame.

REFERENCES


## Slide 8 — Library and pandas and DataFrame

PURPOSE
Library and pandas and DataFrame

CONNECT
Previous slide: Our small energy table.

EXPLAIN
Library and pandas: A library is reusable code. pandas provides tools for data tables. import pandas as pd makes pd a short name for that library.

DataFrame: A table with named columns and indexed rows. df is just the variable name we choose for this table.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A labelled table in Python.

REFERENCES


## Slide 9 — A labelled table in Python

PURPOSE
A labelled table in Python

CONNECT
Previous slide: Library and pandas and DataFrame.

EXPLAIN
The illustration uses machinery records. The same row, column and index structure applies to our building-energy table.

LECTURER CUE
Point to one row, column, index and dtype. This maintenance table is illustrative. Work with the issued cohort table next.
Source: existing course illustration figs/dataframe_anatomy.png. These are illustrative examples, not this cohort’s assessed results.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Series and Method and attribute.

REFERENCES
Source: existing course illustration figs/dataframe_anatomy.png. These are illustrative examples, not this cohort’s assessed results.

## Slide 10 — Series and Method and attribute

PURPOSE
Series and Method and attribute

CONNECT
Previous slide: A labelled table in Python.

EXPLAIN
Series: One labelled column. df["kwh"] selects the column named kwh.

Method and attribute: A method performs an operation, as in df.head(). An attribute provides a stored property, as in df.shape. Parentheses call an operation.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Reading pandas syntax.

REFERENCES


## Slide 11 — Reading pandas syntax

PURPOSE
Reading pandas syntax

CONNECT
Previous slide: Series and Method and attribute.

EXPLAIN
import pandas as pd loads the library and gives it a short name.

pd.read_csv("file.csv") calls a function. The quoted text is the file path.

df["kwh"] selects a column. df["kwh"].mean() calls a method on that column.

LECTURER CUE
Replace file.csv with the actual issued filename. Explain library, alias, function and method before running the worked example.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Read the table constructor in stages.

REFERENCES


## Slide 12 — Read the table constructor in stages

PURPOSE
Read the table constructor in stages

CONNECT
Previous slide: Reading pandas syntax.

EXPLAIN
import pandas as pd loads pandas and gives it the shorter name pd. This is an alias; you could use another name consistently.

Inside pd.DataFrame(...), the dictionary keys become column names. Each list supplies that column’s values in row order.

All these column lists have the same length. At position 0, building is "A" and kwh is 2; together they form the first row.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Build the table before asking questions.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 13 — Build the table before asking questions

PURPOSE
Build the table before asking questions

CONNECT
Previous slide: Read the table constructor in stages.

EXPLAIN
Read the code in this order:
import pandas as pd
df = pd.DataFrame({"building": ["A", "A", "B", "B"],
                   "kwh": [2, 4, 5, 7]})
print(df)

import loads a library. from selects a tool from it.

print displays a value below the cell.

Square brackets create a list or select an item.

Each dictionary key becomes a column name. Equal-length lists supply its rows.

LECTURER CUE
Each dictionary key becomes a column name. Equal-length lists supply its rows.

Complete practice code:
import pandas as pd
df = pd.DataFrame({"building": ["A", "A", "B", "B"],
                   "kwh": [2, 4, 5, 7]})
print(df)

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Select first then summarise.

REFERENCES


## Slide 14 — Select first then summarise

PURPOSE
Select first then summarise

CONNECT
Previous slide: Build the table before asking questions.

EXPLAIN
df["kwh"] selects the energy column as a Series, which is a labelled sequence of values. Its entries are 2, 4, 5 and 7.

Store it as energy = df["kwh"]. energy.mean() adds those four values and divides by four: 18 / 4 = 4.5.

df["kwh"].mean() combines those same two steps. A dot chooses a method; parentheses call it.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Select a column and calculate its mean.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 15 — Select a column and calculate its mean

PURPOSE
Select a column and calculate its mean

CONNECT
Previous slide: Select first then summarise.

EXPLAIN
Read the code in this order:
print(df["kwh"])
print(df["kwh"].mean())

print displays a value below the cell.

Square brackets create a list or select an item.

The four numbers are 2, 4, 5 and 7. Their mean is 18 / 4 = 4.5 kWh.

LECTURER CUE
The four numbers are 2, 4, 5 and 7. Their mean is 18 / 4 = 4.5 kWh.

Complete practice code:
print(df["kwh"])
print(df["kwh"].mean())

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Mask and filter.

REFERENCES


## Slide 16 — Mask and filter

PURPOSE
Mask and filter

CONNECT
Previous slide: Select a column and calculate its mean.

EXPLAIN
Mask and filter: A comparison produces True/False for each row. df[mask] keeps the True rows.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A comparison creates a Boolean mask.

REFERENCES


## Slide 17 — A comparison creates a Boolean mask

PURPOSE
A comparison creates a Boolean mask

CONNECT
Previous slide: Mask and filter.

EXPLAIN
The illustration filters torque readings. Our next example applies the same True/False selection to kWh values.

LECTURER CUE
Read > as greater than, then trace one row through the mask. Selection does not delete the source rows. 40 is a practice threshold, not a safety standard.
Source: existing course illustration figs/boolean_mask.png. These are illustrative examples, not this cohort’s assessed results.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Keep rows where the comparison is true.

REFERENCES
Source: existing course illustration figs/boolean_mask.png. These are illustrative examples, not this cohort’s assessed results.

## Slide 18 — Keep rows where the comparison is true

PURPOSE
Keep rows where the comparison is true

CONNECT
Previous slide: A comparison creates a Boolean mask.

EXPLAIN
Read the code in this order:
mask = df["kwh"] > 4
print(mask)
print(df[mask])

print displays a value below the cell.

Square brackets create a list or select an item.

= assigns the value on the right to the name on the left.

The mask is False, False, True, True. The selected rows contain 5 and 7 kWh.

LECTURER CUE
The mask is False, False, True, True. The selected rows contain 5 and 7 kWh.

Complete practice code:
mask = df["kwh"] > 4
print(mask)
print(df[mask])

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
groupby and aggregation.

REFERENCES


## Slide 19 — groupby and aggregation

PURPOSE
groupby and aggregation

CONNECT
Previous slide: Keep rows where the comparison is true.

EXPLAIN
groupby and aggregation: groupby collects rows with the same label. An aggregation such as sum or mean returns a summary for each group.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Trace a group total before using groupby.

REFERENCES


## Slide 20 — Trace a group total before using groupby

PURPOSE
Trace a group total before using groupby

CONNECT
Previous slide: groupby and aggregation.

EXPLAIN
Group | Values assigned to it | Total

A | 2 and 4 | 6

B | 5 and 7 | 12

groupby separates rows by the building label. sum adds the kWh values inside each group.

Read the rows in order. groupby separates rows by the building label. sum adds the kWh values inside each group.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Read each step of a pandas chain.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 21 — Read each step of a pandas chain

PURPOSE
Read each step of a pandas chain

CONNECT
Previous slide: Trace a group total before using groupby.

EXPLAIN
groups = df.groupby("building") describes groups of rows with matching building labels.

energy_groups = groups["kwh"] selects the energy values within those groups. totals = energy_groups.sum() calculates one total per group.

df.groupby("building")["kwh"].sum() is the same sequence written on one line. Read it from left to right.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Calculate one total for each building.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 22 — Calculate one total for each building

PURPOSE
Calculate one total for each building

CONNECT
Previous slide: Read each step of a pandas chain.

EXPLAIN
Read the code in this order:
print(df.groupby("building")["kwh"].sum())

print displays a value below the cell.

Square brackets create a list or select an item.

Expected: A totals 6 kWh; B totals 12 kWh.

LECTURER CUE
Expected: A totals 6 kWh; B totals 12 kWh.

Complete practice code:
print(df.groupby("building")["kwh"].sum())

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Expected output.

REFERENCES


## Slide 23 — pandas tables and summaries results

PURPOSE
pandas tables and summaries results

CONNECT
Previous slide: Calculate one total for each building.

EXPLAIN
Mean 4.5. The filter keeps B rows with 5 and 7. Group totals: A = 6, B = 12 kWh.

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Unique labels and the largest group.

REFERENCES


## Slide 24 — Unique labels and the largest group

PURPOSE
Unique labels and the largest group

CONNECT
Previous slide: pandas tables and summaries results.

EXPLAIN
nunique counts distinct labels, not rows. idxmax returns the label of the largest total.

Here there is no tie.

LECTURER CUE
nunique counts distinct labels, not rows. idxmax returns the label of the largest total. Here there is no tie.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Unique labels and the largest group in Python.

REFERENCES


## Slide 25 — Unique labels and the largest group in Python

PURPOSE
Unique labels and the largest group in Python

CONNECT
Previous slide: Unique labels and the largest group.

EXPLAIN
Read the code in this order:
print(df["building"].nunique())
totals = df.groupby("building")["kwh"].sum()
print(totals.idxmax())

print displays a value below the cell.

Square brackets create a list or select an item.

= assigns the value on the right to the name on the left.

Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER CUE
nunique counts distinct labels, not rows. idxmax returns the label of the largest total. Here there is no tie.

Complete practice code:
print(df["building"].nunique())
totals = df.groupby("building")["kwh"].sum()
print(totals.idxmax())

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Create a column from two existing columns.

REFERENCES


## Slide 26 — Create a column from two existing columns

PURPOSE
Create a column from two existing columns

CONNECT
Previous slide: Unique labels and the largest group in Python.

EXPLAIN
A new column can store a calculation for every row. Division pairs the values in matching rows.

For this invented table all energy values are positive. UGX is Uganda shillings. Cost divided by energy has units UGX/kWh.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
An energy rate is cost divided by energy.

REFERENCES


## Slide 27 — An energy rate is cost divided by energy

PURPOSE
An energy rate is cost divided by energy

CONNECT
Previous slide: Create a column from two existing columns.

EXPLAIN
Read the code in this order:
df["cost_ugx"] = [1000, 2400, 3500, 5600]
df["rate_ugx_per_kwh"] = df["cost_ugx"] / df["kwh"]
print(df["rate_ugx_per_kwh"])

print displays a value below the cell.

Square brackets create a list or select an item.

= assigns the value on the right to the name on the left.

Expected rates: 500, 600, 700 and 800 UGX/kWh. Keep units in column names.

LECTURER CUE
Expected rates: 500, 600, 700 and 800 UGX/kWh. Keep units in column names.

Complete practice code:
df["cost_ugx"] = [1000, 2400, 3500, 5600]
df["rate_ugx_per_kwh"] = df["cost_ugx"] / df["kwh"]
print(df["rate_ugx_per_kwh"])

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Load the assignment table before analysing it.

REFERENCES


## Slide 28 — Load the assignment table before analysing it

PURPOSE
Load the assignment table before analysing it

CONNECT
Previous slide: An energy rate is cost divided by energy.

EXPLAIN
Upload campus_energy.csv to the current runtime first. read_csv reads it into a new DataFrame.

head() displays the first five rows; shape gives row and column counts; dtypes shows column data types.

We call this issued_table to keep it separate from the invented four-row df used above.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Inspect the supplied energy file.

REFERENCES


## Slide 29 — Inspect the supplied energy file

PURPOSE
Inspect the supplied energy file

CONNECT
Previous slide: Load the assignment table before analysing it.

EXPLAIN
Read the code in this order:
issued_table = pd.read_csv("campus_energy.csv")
print(issued_table.head())
print(issued_table.shape)
print(issued_table.dtypes)

print displays a value below the cell.

= assigns the value on the right to the name on the left.

Check column names, data types and units before attempting the six issued tasks.

LECTURER CUE
Check column names, data types and units before attempting the six issued tasks.

Complete practice code:
issued_table = pd.read_csv("campus_energy.csv")
print(issued_table.head())
print(issued_table.shape)
print(issued_table.dtypes)

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Revision example and answer.

REFERENCES


## Slide 30 — Revision example and answer

PURPOSE
Revision example and answer

CONNECT
Previous slide: Inspect the supplied energy file.

EXPLAIN
Example: Use > 5 instead. Predict the surviving rows. Which building has the largest total?

Answer: Only the row with 7 survives. Building B has the larger total, 12 kWh.

LECTURER CUE
Give silent thinking time, then let pairs discuss. Rotate who types. This is practice, not a graded quiz. Expected response: Only the row with 7 survives. Building B has the larger total, 12 kWh.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Preparing for the assignment.

REFERENCES


## Slide 31 — Preparing for the assignment

PURPOSE
Preparing for the assignment

CONNECT
Previous slide: Revision example and answer.

EXPLAIN
A5 uses the supplied fictional campus_energy.csv, not a live Kaggle download.

The six tasks use read_csv, nunique, division of columns, a > filter, mean and grouped totals. idxmax returns the label of the largest value.

A mean of individual rates gives each observation equal weight.

Total cost divided by total energy weights by energy.

LECTURER CUE
A5 uses the supplied fictional campus_energy.csv, not a live Kaggle download. Teach read_csv, nunique, division of columns, > filtering, mean and groupby(...).sum().idxmax() before the six public tasks. idxmax returns the label of the largest value. Explain how a rate differs from a total and how a mean of rates differs from a total-cost/total-energy ratio.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Data types and filters.

REFERENCES


## Slide 32 — Data types and filters

PURPOSE
Data types and filters

CONNECT
Previous slide: Preparing for the assignment.

EXPLAIN
A Boolean mask is a list-like column of True/False values. len(mask) counts all rows; mask.sum() counts True entries.

Strings sort as text, so "9" can rank above "100".

Inspect numeric types before taking maxima.

KeyError often means the column name does not match; check spelling, case and spaces. shape is (rows, columns).

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Data types and filters continued.

REFERENCES


## Slide 33 — Data types and filters continued

PURPOSE
Data types and filters continued

CONNECT
Previous slide: Data types and filters.

EXPLAIN
Read provenance and units before trusting a dataset.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Your issued assignment.

REFERENCES


## Slide 34 — Your issued assignment

PURPOSE
Your issued assignment

CONNECT
Previous slide: Data types and filters continued.

EXPLAIN
Open W05_student.ipynb.

Read every task and its input units before coding.

Keep the required function names and returned outputs.

Run the supplied visible checks, then restart and run all.

LECTURER CUE
# W05: pandas: load, filter, group
CML3112. Complete each named output. Save as STUDENT_ID_W05.ipynb.
## q1: 3 marks
Load campus_energy.csv into a DataFrame called df.
## q2: 3 marks
Set n_meters to the number of distinct meters in the file.
## q3: 4 marks
Add a column cost_per_kwh to df, equal to cost_ugx / kwh.
## q4: 4 marks
Set high_use to the rows of df where kwh is greater than 5000. Do this after q3 so the derived column comes along.
## q5: 3 marks
Set mean_cost_per_kwh to the mean of the cost_per_kwh column.
## q6: 3 marks
Set peak_building to the name of the building with the highest total kwh.
Restart and Run All, then save your named notebook. Practice check results are feedback; the submitted notebook is graded independently.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
q1: 3 marks.

REFERENCES


## Slide 35 — q1: 3 marks

PURPOSE
q1: 3 marks

CONNECT
Previous slide: Your issued assignment.

EXPLAIN
Load campus_energy.csv into a DataFrame called df.

LECTURER CUE
Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
q2: 3 marks.

REFERENCES


## Slide 36 — q2: 3 marks

PURPOSE
q2: 3 marks

CONNECT
Previous slide: q1: 3 marks.

EXPLAIN
Set n_meters to the number of distinct meters in the file.

LECTURER CUE
Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
q3: 4 marks.

REFERENCES


## Slide 37 — q3: 4 marks

PURPOSE
q3: 4 marks

CONNECT
Previous slide: q2: 3 marks.

EXPLAIN
Add a column cost_per_kwh to df, equal to cost_ugx / kwh.

LECTURER CUE
Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
q4: 4 marks.

REFERENCES


## Slide 38 — q4: 4 marks

PURPOSE
q4: 4 marks

CONNECT
Previous slide: q3: 4 marks.

EXPLAIN
Set high_use to the rows of df where kwh is greater than 5000.

Do this after q3 so the derived column comes along.

LECTURER CUE
Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
q5: 3 marks.

REFERENCES


## Slide 39 — q5: 3 marks

PURPOSE
q5: 3 marks

CONNECT
Previous slide: q4: 4 marks.

EXPLAIN
Set mean_cost_per_kwh to the mean of the cost_per_kwh column.

LECTURER CUE
Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
q6: 3 marks.

REFERENCES


## Slide 40 — q6: 3 marks

PURPOSE
q6: 3 marks

CONNECT
Previous slide: q5: 3 marks.

EXPLAIN
Set peak_building to the name of the building with the highest total kwh.

LECTURER CUE
Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Pandas investigation submission.

REFERENCES


## Slide 41 — Pandas investigation submission

PURPOSE
Pandas investigation submission

CONNECT
Previous slide: q6: 3 marks.

EXPLAIN
Opens: 06 Oct 2026, 11:00 Kampala

Deadline: 13 Oct 2026, 11:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

LECTURER CUE
The form link is cohort-specific. Recheck the live form and release status before class. These scheduled assignment dates are separate from the quiz activation window. The issued brief defines the required files, even if the form accepts additional formats. Source: data/submission_links.json

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Project preparation.

REFERENCES


## Slide 42 — Project preparation

PURPOSE
Project preparation

CONNECT
Previous slide: Pandas investigation submission.

EXPLAIN
Use the published data analysis project brief.

Build the evidence gradually in your project notebook.

Keep raw data, labelled charts, run instructions and individual contributions.

Published deadline: 27 Oct 2026, 11:00 Kampala

LECTURER CUE
Explain the released brief now. Confirm its grading-release checks before assigning it. Avoid treating weekly practice as a substitute for the project evidence. The project brief remains authoritative.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Week 5 quiz.

REFERENCES


## Slide 43 — Week 5 quiz

PURPOSE
Week 5 quiz

CONNECT
Previous slide: Project preparation.

EXPLAIN
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

The lecturer will confirm the exact closing time.

LECTURER CUE
Activate the matching open_W5_CML3112 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Before you leave.

REFERENCES


## Slide 44 — Revision and submission checklist

PURPOSE
Revision and submission checklist

CONNECT
Previous slide: Week 5 quiz.

EXPLAIN
You can explain which observations a filter keeps and what a grouped total means.

Save your work and check the required submission files.

LECTURER CUE
Ask every learner for an individual response. Record one misconception to revisit at the start of the next class. If a deadline changed, announce the exact Kampala date and update the source registry before rebuilding slides.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
independent revision and the issued task.

REFERENCES
