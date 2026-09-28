# CML3112 Week05 Design Infrastructure

Lecturer companion to the revised PowerPoint. Slide numbers match this edition. Explain the worked examples directly; revision checks are for individual study.

## Slide 1 — Using pandas to answer table questions

PURPOSE
Using pandas to answer table questions

CONNECT
Build on the preceding week. Explain why this example is needed before running it.

EXPLAIN
Civil Engineering and Architecture

LECTURER DETAIL
TEACHING PURPOSE
Using pandas to answer table questions

LECTURER CUE
Use PowerPoint Presenter View for these notes. Teach one example, pause for every learner to predict, then work an analogous example together. The practice notebook is a learning aid, not an extra graded upload.

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

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
Build on Using pandas to answer table questions. Explain why this example is needed before running it.

EXPLAIN
Read a labelled table and select rows.

Calculate column summaries and grouped totals.

LECTURER DETAIL
TEACHING PURPOSE
Today’s learning

CONNECT
Build on the preceding slide: Using pandas to answer table questions.

LECTURER CUE
Ask learners to explain this goal in ordinary language. The first successful attempt matters more than covering optional extensions. Defer: NumPy broadcasting, broad Kaggle searches and twelve-plus-ten independent questions are optional extension. No change of editor is needed.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

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
Week 4 used lists, dictionaries, loops and CSV rows. pandas keeps these same records in a labelled table and provides operations that work across its columns.

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
The supplied campus_energy.csv records campus electricity use. We practise pandas on four invented rows first, then inspect the supplied file and its units.

LECTURER DETAIL
TEACHING PURPOSE
The engineering context

CONNECT
Build on the preceding slide: Recall and a first attempt.

LECTURER CUE
A building team records indoor temperature to investigate comfort. Civil students can discuss construction and inspection; architecture students can discuss shading and ventilation. Explain the quantities before using them.

EXPLAIN IN ORDINARY WORDS
A calculated column stores a result for each row at refresh. A measure is evaluated under the filters of the current visual. SUMX evaluates an expression for each row before adding it.

CHECK AND EXPECTED ANSWER
Should revenue respond to a selected region? Yes; test the measure with that filter and reconcile it to known data.

IF LEARNERS ARE STUCK
Work one order line by hand, then two lines. Name the numerator and denominator populations before an average-order-value measure.

NEXT
Rows columns and units. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Rows columns and units.

## Slide 5 — Rows columns and units

PURPOSE
Rows columns and units

CONNECT
Build on Why this week’s tools are needed. Explain why this example is needed before running it.

EXPLAIN
A row describes one observation. A column describes one field.

A DataFrame is pandas’ labelled table.

A Series is one labelled column.

kWh measures energy. kW measures power.

A data type (dtype) describes the kind of values in a column, such as whole numbers, decimals or text.

LECTURER DETAIL
TEACHING PURPOSE
Rows columns and units

CONNECT
Build on the preceding slide: The engineering context.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

TYPE NUANCE
An object dtype alone does not prove that a column contains bad numeric values; it can hold Python objects, including numbers. Inspect values and conversion results. Missing values may display as NaN, None, NaT or pandas NA depending on dtype.

NEXT
A table keeps related observations together. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A table keeps related observations together.

## Slide 6 — A table keeps related observations together

PURPOSE
A table keeps related observations together

CONNECT
Build on Rows columns and units. Explain why this example is needed before running it.

EXPLAIN
Our four rows record building A twice and building B twice.

Each row contains the building label and an energy reading.

kWh is energy. kW is power. The units describe different quantities.

LECTURER DETAIL
TEACHING PURPOSE
A table keeps related observations together

CONNECT
Build on the preceding slide: Rows columns and units.

LECTURER CUE
Draw a four-row table before running the example. Describe a reading of kWh as energy, and kW as power; the units are different.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
Our small energy table. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Our small energy table.

## Slide 7 — Our small energy table

PURPOSE
Our small energy table

CONNECT
Build on A table keeps related observations together. Explain why this example is needed before running it.

EXPLAIN
The four observations total 18 kWh.

LECTURER DETAIL
TEACHING PURPOSE
Our small energy table

CONNECT
Build on the preceding slide: A table keeps related observations together.

LECTURER CUE
The four observations total 18 kWh. Their mean is 4.5 kWh. Building totals are A: 6 and B: 12.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
Words we will use. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Library and pandas and DataFrame.

## Slide 8 — Library and pandas and DataFrame

PURPOSE
Library and pandas and DataFrame

CONNECT
Build on Our small energy table. Explain why this example is needed before running it.

EXPLAIN
Library and pandas: A library is reusable code. pandas provides tools for data tables. import pandas as pd makes pd a short name for that library.
DataFrame: A table with named columns and indexed rows. df is just the variable name we choose for this table.

LECTURER DETAIL
TEACHING PURPOSE
Words we will use

CONNECT
Build on the preceding slide: Our small energy table.

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

POINT TO THE DEFINITION
Library and pandas: A library is reusable code. pandas provides tools for data tables. import pandas as pd makes pd a short name for that library.
DataFrame: A table with named columns and indexed rows. df is just the variable name we choose for this table.

NEXT
A DataFrame is a labelled table. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A labelled table in Python.

## Slide 9 — A labelled table in Python

PURPOSE
A labelled table in Python

CONNECT
Build on Library and pandas and DataFrame. Explain why this example is needed before running it.

EXPLAIN
The illustration uses machinery records. The same row, column and index structure applies to our building-energy table.

LECTURER DETAIL
TEACHING PURPOSE
A labelled table in Python

CONNECT
Build on the preceding slide: A DataFrame is a labelled table.

LECTURER CUE
Point to one row, column, index and dtype. This maintenance table is illustrative. Work with the issued cohort table next.
Source: existing course illustration figs/dataframe_anatomy.png. These are illustrative examples, not this cohort’s assessed results.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
Words we will use. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Series and Method and attribute.

## Slide 10 — Series and Method and attribute

PURPOSE
Series and Method and attribute

CONNECT
Build on A labelled table in Python. Explain why this example is needed before running it.

EXPLAIN
Series: One labelled column. df["kwh"] selects the column named kwh.
Method and attribute: A method performs an operation, as in df.head(). An attribute provides a stored property, as in df.shape. Parentheses call an operation.

LECTURER DETAIL
TEACHING PURPOSE
Words we will use

CONNECT
Build on the preceding slide: A labelled table in Python.

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

POINT TO THE DEFINITION
Series: One labelled column. df["kwh"] selects the column named kwh.
Method and attribute: A method performs an operation, as in df.head(). An attribute provides a stored property, as in df.shape. Parentheses call an operation.

NEXT
Reading pandas syntax. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Reading pandas syntax.

## Slide 11 — Reading pandas syntax

PURPOSE
Reading pandas syntax

CONNECT
Build on Series and Method and attribute. Explain why this example is needed before running it.

EXPLAIN
import pandas as pd loads the library and gives it a short name.

pd.read_csv("file.csv") calls a function. The quoted text is the file path.

df["kwh"] selects a column. df["kwh"].mean() calls a method on that column.

LECTURER DETAIL
TEACHING PURPOSE
Reading pandas syntax

CONNECT
Build on the preceding slide: Words we will use.

LECTURER CUE
Replace file.csv with the actual issued filename. Explain library, alias, function and method before running the worked example.

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

NEXT
Build the table before asking questions. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Build the table before asking questions.

## Slide 12 — Build the table before asking questions

PURPOSE
Build the table before asking questions

CONNECT
Build on Reading pandas syntax. Explain why this example is needed before running it.

EXPLAIN
Each dictionary key becomes a column name. Equal-length lists supply its rows.

LECTURER DETAIL
TEACHING PURPOSE
Build the table before asking questions

CONNECT
Build on the preceding slide: Reading pandas syntax.

LECTURER CUE
Each dictionary key becomes a column name. Equal-length lists supply its rows.

Complete practice code:
import pandas as pd
df = pd.DataFrame({"building": ["A", "A", "B", "B"],
                   "kwh": [2, 4, 5, 7]})
print(df)

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

WALK THROUGH THIS CODE
import loads a library. from selects a tool from it.
print displays a value below the cell.
Square brackets create a list or select an item.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Select a column and calculate its mean. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Select a column and calculate its mean.

## Slide 13 — Select a column and calculate its mean

PURPOSE
Select a column and calculate its mean

CONNECT
Build on Build the table before asking questions. Explain why this example is needed before running it.

EXPLAIN
The four numbers are 2, 4, 5 and 7. Their mean is 18 / 4 = 4.5 kWh.

LECTURER DETAIL
TEACHING PURPOSE
Select a column and calculate its mean

CONNECT
Build on the preceding slide: Build the table before asking questions.

LECTURER CUE
The four numbers are 2, 4, 5 and 7. Their mean is 18 / 4 = 4.5 kWh.

Complete practice code:
print(df["kwh"])
print(df["kwh"].mean())

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

WALK THROUGH THIS CODE
print displays a value below the cell.
Square brackets create a list or select an item.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Mask and filter. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Mask and filter.

## Slide 14 — Mask and filter

PURPOSE
Mask and filter

CONNECT
Build on Select a column and calculate its mean. Explain why this example is needed before running it.

EXPLAIN
Mask and filter: A comparison produces True/False for each row. df[mask] keeps the True rows.

LECTURER DETAIL
TEACHING PURPOSE
Mask and filter

CONNECT
Build on the preceding slide: Select a column and calculate its mean.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

POINT TO THE DEFINITION
Mask and filter: A comparison produces True/False for each row. df[mask] keeps the True rows.

NEXT
A comparison creates a Boolean mask. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A comparison creates a Boolean mask.

## Slide 15 — A comparison creates a Boolean mask

PURPOSE
A comparison creates a Boolean mask

CONNECT
Build on Mask and filter. Explain why this example is needed before running it.

EXPLAIN
The illustration filters torque readings. Our next example applies the same True/False selection to kWh values.

LECTURER DETAIL
TEACHING PURPOSE
A comparison creates a Boolean mask

CONNECT
Build on the preceding slide: Mask and filter.

LECTURER CUE
Read > as greater than, then trace one row through the mask. Selection does not delete the source rows. 40 is a practice threshold, not a safety standard.
Source: existing course illustration figs/boolean_mask.png. These are illustrative examples, not this cohort’s assessed results.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

NEXT
Keep rows where the comparison is true. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Keep rows where the comparison is true.

## Slide 16 — Keep rows where the comparison is true

PURPOSE
Keep rows where the comparison is true

CONNECT
Build on A comparison creates a Boolean mask. Explain why this example is needed before running it.

EXPLAIN
The mask is False, False, True, True. The selected rows contain 5 and 7 kWh.

LECTURER DETAIL
TEACHING PURPOSE
Keep rows where the comparison is true

CONNECT
Build on the preceding slide: A comparison creates a Boolean mask.

LECTURER CUE
The mask is False, False, True, True. The selected rows contain 5 and 7 kWh.

Complete practice code:
mask = df["kwh"] > 4
print(mask)
print(df[mask])

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

WALK THROUGH THIS CODE
print displays a value below the cell.
Square brackets create a list or select an item.
= assigns the value on the right to the name on the left.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
groupby and aggregation. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
groupby and aggregation.

## Slide 17 — groupby and aggregation

PURPOSE
groupby and aggregation

CONNECT
Build on Keep rows where the comparison is true. Explain why this example is needed before running it.

EXPLAIN
groupby and aggregation: groupby collects rows with the same label. An aggregation such as sum or mean returns a summary for each group.

LECTURER DETAIL
TEACHING PURPOSE
groupby and aggregation

CONNECT
Build on the preceding slide: Keep rows where the comparison is true.

EXPLAIN IN ORDINARY WORDS
Grouping puts rows sharing a key into buckets, then computes a result for each bucket. WHERE filters rows before SQL grouping; HAVING filters grouped results.

CHECK AND EXPECTED ANSWER
Which condition keeps only groups with more than five rows? HAVING COUNT(*) > 5.

IF LEARNERS ARE STUCK
Draw two buckets and count by hand. Name the intended output grain before writing the aggregation.

POINT TO THE DEFINITION
groupby and aggregation: groupby collects rows with the same label. An aggregation such as sum or mean returns a summary for each group.

NEXT
Selection and grouping answer different questions. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Calculate one total for each building.

## Slide 18 — Calculate one total for each building

PURPOSE
Calculate one total for each building

CONNECT
Build on groupby and aggregation. Explain why this example is needed before running it.

EXPLAIN
Expected: A totals 6 kWh; B totals 12 kWh.

LECTURER DETAIL
TEACHING PURPOSE
Calculate one total for each building

CONNECT
Build on the preceding slide: A chained expression is several small steps.

LECTURER CUE
Expected: A totals 6 kWh; B totals 12 kWh.

Complete practice code:
print(df.groupby("building")["kwh"].sum())

EXPLAIN IN ORDINARY WORDS
Grouping puts rows sharing a key into buckets, then computes a result for each bucket. WHERE filters rows before SQL grouping; HAVING filters grouped results.

CHECK AND EXPECTED ANSWER
Which condition keeps only groups with more than five rows? HAVING COUNT(*) > 5.

IF LEARNERS ARE STUCK
Draw two buckets and count by hand. Name the intended output grain before writing the aggregation.

WALK THROUGH THIS CODE
print displays a value below the cell.
Square brackets create a list or select an item.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Expected output. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Expected output.

## Slide 19 — pandas tables and summaries results

PURPOSE
pandas tables and summaries results

CONNECT
Build on Calculate one total for each building. Explain why this example is needed before running it.

EXPLAIN
Mean 4.5. The filter keeps B rows with 5 and 7. Group totals: A = 6, B = 12 kWh.

LECTURER DETAIL
TEACHING PURPOSE
Expected output

CONNECT
Build on the preceding slide: Calculate one total for each building.

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

NEXT
Unique labels and the largest group. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Reading a chain one operation at a time.

## Slide 20 — Reading a chain one operation at a time

PURPOSE
Reading a chain one operation at a time

CONNECT
Build on pandas tables and summaries results. Explain why this example is needed before running it.

EXPLAIN
df.groupby("building") groups rows by their building labels. ["kwh"] selects the energy values within each group. .sum() totals them.

Store this result in totals. totals.idxmax() returns the label with the largest total. These are consecutive operations on the result of the previous step.

LECTURER DETAIL


TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Unique labels and the largest group.

## Slide 21 — Unique labels and the largest group

PURPOSE
Unique labels and the largest group

CONNECT
Build on Reading a chain one operation at a time. Explain why this example is needed before running it.

EXPLAIN
nunique counts distinct labels, not rows. idxmax returns the label of the largest total.

Here there is no tie.

LECTURER DETAIL
TEACHING PURPOSE
Unique labels and the largest group

CONNECT
Build on the preceding slide: Expected output.

LECTURER CUE
nunique counts distinct labels, not rows. idxmax returns the label of the largest total. Here there is no tie.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

NEXT
Unique labels and the largest group in Python. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Unique labels and the largest group in Python.

## Slide 22 — Unique labels and the largest group in Python

PURPOSE
Unique labels and the largest group in Python

CONNECT
Build on Unique labels and the largest group. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
TEACHING PURPOSE
Unique labels and the largest group in Python

CONNECT
Build on the preceding slide: Unique labels and the largest group.

LECTURER CUE
nunique counts distinct labels, not rows. idxmax returns the label of the largest total. Here there is no tie.

Complete practice code:
print(df["building"].nunique())
totals = df.groupby("building")["kwh"].sum()
print(totals.idxmax())

EXPLAIN IN ORDINARY WORDS
Grouping puts rows sharing a key into buckets, then computes a result for each bucket. WHERE filters rows before SQL grouping; HAVING filters grouped results.

CHECK AND EXPECTED ANSWER
Which condition keeps only groups with more than five rows? HAVING COUNT(*) > 5.

IF LEARNERS ARE STUCK
Draw two buckets and count by hand. Name the intended output grain before writing the aggregation.

WALK THROUGH THIS CODE
print displays a value below the cell.
Square brackets create a list or select an item.
= assigns the value on the right to the name on the left.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Create a column from two existing columns. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Create a column from two existing columns.

## Slide 23 — Create a column from two existing columns

PURPOSE
Create a column from two existing columns

CONNECT
Build on Unique labels and the largest group in Python. Explain why this example is needed before running it.

EXPLAIN
A new column can store a calculation for every row. Division pairs the values in matching rows.

For this invented table all energy values are positive. UGX is Uganda shillings. Cost divided by energy has units UGX/kWh.

LECTURER DETAIL
TEACHING PURPOSE
Create a column from two existing columns

CONNECT
Build on the preceding slide: Unique labels and the largest group in Python.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

NEXT
An energy rate is cost divided by energy. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
An energy rate is cost divided by energy.

## Slide 24 — An energy rate is cost divided by energy

PURPOSE
An energy rate is cost divided by energy

CONNECT
Build on Create a column from two existing columns. Explain why this example is needed before running it.

EXPLAIN
Expected rates: 500, 600, 700 and 800 UGX/kWh. Keep units in column names.

LECTURER DETAIL
TEACHING PURPOSE
An energy rate is cost divided by energy

CONNECT
Build on the preceding slide: Create a column from two existing columns.

LECTURER CUE
Expected rates: 500, 600, 700 and 800 UGX/kWh. Keep units in column names.

Complete practice code:
df["cost_ugx"] = [1000, 2400, 3500, 5600]
df["rate_ugx_per_kwh"] = df["cost_ugx"] / df["kwh"]
print(df["rate_ugx_per_kwh"])

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

WALK THROUGH THIS CODE
print displays a value below the cell.
Square brackets create a list or select an item.
= assigns the value on the right to the name on the left.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Load the assignment table before analysing it. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Load the assignment table before analysing it.

## Slide 25 — Load the assignment table before analysing it

PURPOSE
Load the assignment table before analysing it

CONNECT
Build on An energy rate is cost divided by energy. Explain why this example is needed before running it.

EXPLAIN
Upload campus_energy.csv to the current runtime first. read_csv reads it into a new DataFrame.

head() displays the first five rows; shape gives row and column counts; dtypes shows column data types.

We call this issued_table to keep it separate from the invented four-row df used above.

LECTURER DETAIL
TEACHING PURPOSE
Load the assignment table before analysing it

CONNECT
Build on the preceding slide: An energy rate is cost divided by energy.

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

TYPE NUANCE
An object dtype alone does not prove that a column contains bad numeric values; it can hold Python objects, including numbers. Inspect values and conversion results. Missing values may display as NaN, None, NaT or pandas NA depending on dtype.

NEXT
Inspect the supplied energy file. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Inspect the supplied energy file.

## Slide 26 — Inspect the supplied energy file

PURPOSE
Inspect the supplied energy file

CONNECT
Build on Load the assignment table before analysing it. Explain why this example is needed before running it.

EXPLAIN
Check column names, data types and units before attempting the six issued tasks.

LECTURER DETAIL
TEACHING PURPOSE
Inspect the supplied energy file

CONNECT
Build on the preceding slide: Load the assignment table before analysing it.

LECTURER CUE
Check column names, data types and units before attempting the six issued tasks.

Complete practice code:
issued_table = pd.read_csv("campus_energy.csv")
print(issued_table.head())
print(issued_table.shape)
print(issued_table.dtypes)

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

WALK THROUGH THIS CODE
print displays a value below the cell.
= assigns the value on the right to the name on the left.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

TYPE NUANCE
An object dtype alone does not prove that a column contains bad numeric values; it can hold Python objects, including numbers. Inspect values and conversion results. Missing values may display as NaN, None, NaT or pandas NA depending on dtype.

NEXT
You are groupby. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Revision example and answer.

## Slide 27 — Revision example and answer

PURPOSE
Revision example and answer

CONNECT
Build on Inspect the supplied energy file. Explain why this example is needed before running it.

EXPLAIN
Example: Use > 5 instead. Predict the surviving rows. Which building has the largest total?

Answer: Only the row with 7 survives. Building B has the larger total, 12 kWh.

LECTURER DETAIL
TEACHING PURPOSE
Your turn

CONNECT
Build on the preceding slide: What the activity shows.

LECTURER CUE
Give silent thinking time, then let pairs discuss. Rotate who types. This is practice, not a graded quiz. Expected response: Only the row with 7 survives. Building B has the larger total, 12 kWh.

DISCUSSION KEY FOR THIS SLIDE
DISCUSS THE REASONING
Practice discussion
Only the row with 7 survives. Building B has the larger total, 12 kWh.
Which step produced this result? What changes if one input changes?
CML3112   Week 5   32
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
Practice discussion. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Preparing for the assignment.

## Slide 28 — Preparing for the assignment

PURPOSE
Preparing for the assignment

CONNECT
Build on Revision example and answer. Explain why this example is needed before running it.

EXPLAIN
A5 uses the supplied fictional campus_energy.csv, not a live Kaggle download.

The six tasks use read_csv, nunique, division of columns, a > filter, mean and grouped totals. idxmax returns the label of the largest value.

A mean of individual rates gives each observation equal weight.

Total cost divided by total energy weights by energy.

LECTURER DETAIL
TEACHING PURPOSE
Preparing for the assignment

CONNECT
Build on the preceding slide: Practice discussion.

LECTURER CUE
A5 uses the supplied fictional campus_energy.csv, not a live Kaggle download. Teach read_csv, nunique, division of columns, > filtering, mean and groupby(...).sum().idxmax() before the six public tasks. idxmax returns the label of the largest value. Explain how a rate differs from a total and how a mean of rates differs from a total-cost/total-energy ratio.

EXPLAIN IN ORDINARY WORDS
A CSV is a text table. The header supplies column names. With csv.DictReader, values start as text, even if they look like numbers. A path tells Python where the file is.

CHECK AND EXPECTED ANSWER
Can "2.5" from csv.DictReader be added as a number without conversion? No; convert valid numeric text first.

IF LEARNERS ARE STUCK
Show the file in the runtime folder and compare its exact filename, case and column headers. Upload data again after a fresh Colab runtime.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Data types and filters. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Data types and filters.

## Slide 29 — Data types and filters

PURPOSE
Data types and filters

CONNECT
Build on Preparing for the assignment. Explain why this example is needed before running it.

EXPLAIN
A Boolean mask is a list-like column of True/False values. len(mask) counts all rows; mask.sum() counts True entries.

Strings sort as text, so "9" can rank above "100".

Inspect numeric types before taking maxima.

KeyError often means the column name does not match; check spelling, case and spaces. shape is (rows, columns).

LECTURER DETAIL
TEACHING PURPOSE
Data types and filters

CONNECT
Build on the preceding slide: Preparing for the assignment.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

NEXT
Data types and filters continued. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Data types and filters continued.

## Slide 30 — Data types and filters continued

PURPOSE
Data types and filters continued

CONNECT
Build on Data types and filters. Explain why this example is needed before running it.

EXPLAIN
Read provenance and units before trusting a dataset.

LECTURER DETAIL
TEACHING PURPOSE
Data types and filters continued

CONNECT
Build on the preceding slide: Data types and filters.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
Your issued assignment. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Your issued assignment.

## Slide 31 — Your issued assignment

PURPOSE
Your issued assignment

CONNECT
Build on Data types and filters continued. Explain why this example is needed before running it.

EXPLAIN
Open W05_student.ipynb.

Read every task and its input units before coding.

Keep the required function names and returned outputs.

Run the supplied visible checks, then restart and run all.

LECTURER DETAIL
TEACHING PURPOSE
Your issued assignment

CONNECT
Build on the preceding slide: Data types and filters continued.

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

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
q1: 3 marks. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
q1: 3 marks.

## Slide 32 — q1: 3 marks

PURPOSE
q1: 3 marks

CONNECT
Build on Your issued assignment. Explain why this example is needed before running it.

EXPLAIN
Load campus_energy.csv into a DataFrame called df.

LECTURER DETAIL
TEACHING PURPOSE
q1: 3 marks

CONNECT
Build on the preceding slide: Your issued assignment.

LECTURER CUE
Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

NEXT
q2: 3 marks. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
q2: 3 marks.

## Slide 33 — q2: 3 marks

PURPOSE
q2: 3 marks

CONNECT
Build on q1: 3 marks. Explain why this example is needed before running it.

EXPLAIN
Set n_meters to the number of distinct meters in the file.

LECTURER DETAIL
TEACHING PURPOSE
q2: 3 marks

CONNECT
Build on the preceding slide: q1: 3 marks.

LECTURER CUE
Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

NEXT
q3: 4 marks. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
q3: 4 marks.

## Slide 34 — q3: 4 marks

PURPOSE
q3: 4 marks

CONNECT
Build on q2: 3 marks. Explain why this example is needed before running it.

EXPLAIN
Add a column cost_per_kwh to df, equal to cost_ugx / kwh.

LECTURER DETAIL
TEACHING PURPOSE
q3: 4 marks

CONNECT
Build on the preceding slide: q2: 3 marks.

LECTURER CUE
Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

NEXT
q4: 4 marks. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
q4: 4 marks.

## Slide 35 — q4: 4 marks

PURPOSE
q4: 4 marks

CONNECT
Build on q3: 4 marks. Explain why this example is needed before running it.

EXPLAIN
Set high_use to the rows of df where kwh is greater than 5000.

Do this after q3 so the derived column comes along.

LECTURER DETAIL
TEACHING PURPOSE
q4: 4 marks

CONNECT
Build on the preceding slide: q3: 4 marks.

LECTURER CUE
Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

NEXT
q5: 3 marks. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
q5: 3 marks.

## Slide 36 — q5: 3 marks

PURPOSE
q5: 3 marks

CONNECT
Build on q4: 4 marks. Explain why this example is needed before running it.

EXPLAIN
Set mean_cost_per_kwh to the mean of the cost_per_kwh column.

LECTURER DETAIL
TEACHING PURPOSE
q5: 3 marks

CONNECT
Build on the preceding slide: q4: 4 marks.

LECTURER CUE
Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

NEXT
q6: 3 marks. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
q6: 3 marks.

## Slide 37 — q6: 3 marks

PURPOSE
q6: 3 marks

CONNECT
Build on q5: 3 marks. Explain why this example is needed before running it.

EXPLAIN
Set peak_building to the name of the building with the highest total kwh.

LECTURER DETAIL
TEACHING PURPOSE
q6: 3 marks

CONNECT
Build on the preceding slide: q5: 3 marks.

LECTURER CUE
Read the specific public requirement shown on this slide. Explain the input, output and evidence before independent work; do not work the assessed answer for the class.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

NEXT
Pandas investigation submission. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Pandas investigation submission.

## Slide 38 — Pandas investigation submission

PURPOSE
Pandas investigation submission

CONNECT
Build on q6: 3 marks. Explain why this example is needed before running it.

EXPLAIN
Opens: 06 Oct 2026, 11:00 Kampala

Deadline: 13 Oct 2026, 11:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

LECTURER DETAIL
TEACHING PURPOSE
Pandas investigation submission

CONNECT
Build on the preceding slide: q6: 3 marks.

LECTURER CUE
The form link is cohort-specific. Recheck the live form and release status before class. These scheduled assignment dates are separate from the quiz activation window. The issued brief defines the required files, even if the form accepts additional formats. Source: data/submission_links.json

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Project preparation. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Project preparation.

## Slide 39 — Project preparation

PURPOSE
Project preparation

CONNECT
Build on Pandas investigation submission. Explain why this example is needed before running it.

EXPLAIN
Use the published data analysis project brief.

Build the evidence gradually in your project notebook.

Keep raw data, labelled charts, run instructions and individual contributions.

Published deadline: 27 Oct 2026, 11:00 Kampala

LECTURER DETAIL
TEACHING PURPOSE
Project preparation

CONNECT
Build on the preceding slide: Pandas investigation submission.

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
Week 5 quiz. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Week 5 quiz.

## Slide 40 — Week 5 quiz

PURPOSE
Week 5 quiz

CONNECT
Build on Project preparation. Explain why this example is needed before running it.

EXPLAIN
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

The lecturer will confirm the exact closing time.

LECTURER DETAIL
TEACHING PURPOSE
Week 5 quiz

CONNECT
Build on the preceding slide: Project preparation.

LECTURER CUE
Activate the matching open_W5_CML3112 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

QUIZ OPERATION
Opening the student link does not activate the quiz. In Quiz Controls run the matching open_W<week>_<cohort> function once when ready. Announce the logged closing time: 24 hours after activation. Five minutes describes expected answering time, not the availability window. Quiz 1 and Quiz 2 require separate activation when collecting catch-up work.

NEXT
Before you leave. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Before you leave.

## Slide 41 — Revision and submission checklist

PURPOSE
Revision and submission checklist

CONNECT
Build on Week 5 quiz. Explain why this example is needed before running it.

EXPLAIN
You can explain which observations a filter keeps and what a grouped total means.

Save your work and check the required submission files.

LECTURER DETAIL
TEACHING PURPOSE
Before you leave

CONNECT
Build on the preceding slide: Week 5 quiz.

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
