# CML3112 Week05 Design Infrastructure

Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.

## Slide 1 — Using pandas to answer table questions

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

## Slide 2 — Today’s learning

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

## Slide 3 — Recall and a first attempt

TEACHING PURPOSE
Recall and a first attempt

CONNECT
Build on the preceding slide: Today’s learning.

LECTURER CUE
Allow two minutes for everyone to try. Ask pairs to compare. If many cannot begin, show the first step and repeat with changed values. Checkpoint for today: Each student predicts a filter and explains what one group total means before running it.

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
A building team records indoor temperature to investigate comfort. Civil students can discuss construction and inspection; architecture students can discuss shading and ventilation. Explain the quantities before using them.

EXPLAIN IN ORDINARY WORDS
A calculated column stores a result for each row at refresh. A measure is evaluated under the filters of the current visual. SUMX evaluates an expression for each row before adding it.

CHECK AND EXPECTED ANSWER
Should revenue respond to a selected region? Yes; test the measure with that filter and reconcile it to known data.

IF LEARNERS ARE STUCK
Work one order line by hand, then two lines. Name the numerator and denominator populations before an average-order-value measure.

NEXT
Rows columns and units. Move on after a learner can explain the current example or required action.

## Slide 5 — Rows columns and units

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

## Slide 6 — A table keeps related observations together

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

## Slide 7 — Our small energy table

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

## Slide 8 — Words we will use

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

## Slide 9 — A DataFrame is a labelled table

TEACHING PURPOSE
A DataFrame is a labelled table

CONNECT
Build on the preceding slide: Words we will use.

LECTURER CUE
Explain dictionary braces, column labels in quotes and lists of values before constructing the DataFrame. In class, read the issued campus_energy.csv with pd.read_csv after this tiny example.

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

NEXT
A labelled table in Python. Move on after a learner can explain the current example or required action.

## Slide 10 — A labelled table in Python

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

## Slide 11 — Words we will use

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

## Slide 12 — Reading pandas syntax

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

## Slide 13 — Build the table before asking questions

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

## Slide 14 — Select a column and calculate its mean

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

## Slide 15 — Mask and filter

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

## Slide 16 — A comparison creates a Boolean mask

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

## Slide 17 — Keep rows where the comparison is true

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

## Slide 18 — groupby and aggregation

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

## Slide 19 — Selection and grouping answer different questions

TEACHING PURPOSE
Selection and grouping answer different questions

CONNECT
Build on the preceding slide: groupby and aggregation.

LECTURER CUE
Run the column selection, comparison and filtered table in separate cells. Then group rows by building and add energy within each group.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
A chained expression is several small steps. Move on after a learner can explain the current example or required action.

## Slide 20 — A chained expression is several small steps

TEACHING PURPOSE
A chained expression is several small steps

CONNECT
Build on the preceding slide: Selection and grouping answer different questions.

LECTURER CUE
Read one row at a time and use a changed value. This is a syntax reference for the worked examples.

EXPLAIN IN ORDINARY WORDS
Grouping puts rows sharing a key into buckets, then computes a result for each bucket. WHERE filters rows before SQL grouping; HAVING filters grouped results.

CHECK AND EXPECTED ANSWER
Which condition keeps only groups with more than five rows? HAVING COUNT(*) > 5.

IF LEARNERS ARE STUCK
Draw two buckets and count by hand. Name the intended output grain before writing the aggregation.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
Calculate one total for each building. Move on after a learner can explain the current example or required action.

## Slide 21 — Calculate one total for each building

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

## Slide 22 — Expected output

TEACHING PURPOSE
Expected output

CONNECT
Build on the preceding slide: Calculate one total for each building.

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

NEXT
Unique labels and the largest group. Move on after a learner can explain the current example or required action.

## Slide 23 — Unique labels and the largest group

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

## Slide 24 — Unique labels and the largest group in Python

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

## Slide 25 — Create a column from two existing columns

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

## Slide 26 — An energy rate is cost divided by energy

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

## Slide 27 — Load the assignment table before analysing it

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

## Slide 28 — Inspect the supplied energy file

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

## Slide 29 — You are groupby

TEACHING PURPOSE
You are groupby

CONNECT
Build on the preceding slide: Inspect the supplied energy file.

LECTURER CUE
Do this before revealing the discussion slide. One learner moves or writes the items, the other checks. Swap roles. Every student explains one step. Expected: A totals 6 kWh. B totals 12 kWh. B is largest and there are 2 distinct buildings.
Wait for an individual prediction before inviting pair discussion. Give a first-step hint if needed.

EXPLAIN IN ORDINARY WORDS
Grouping puts rows sharing a key into buckets, then computes a result for each bucket. WHERE filters rows before SQL grouping; HAVING filters grouped results.

CHECK AND EXPECTED ANSWER
Which condition keeps only groups with more than five rows? HAVING COUNT(*) > 5.

IF LEARNERS ARE STUCK
Draw two buckets and count by hand. Name the intended output grain before writing the aggregation.

NEXT
What the activity shows. Move on after a learner can explain the current example or required action.

## Slide 30 — What the activity shows

TEACHING PURPOSE
What the activity shows

CONNECT
Build on the preceding slide: You are groupby.

LECTURER CUE
Ask which step produced this answer. Return to the concrete action if a learner cannot explain it. This is practice feedback, never a quiz key.

NEXT
Your turn. Move on after a learner can explain the current example or required action.

## Slide 31 — Your turn

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

## Slide 32 — Practice discussion

TEACHING PURPOSE
Practice discussion

CONNECT
Build on the preceding slide: Your turn.

LECTURER CUE
Ask how the result was obtained. Reteach the smallest missing step instead of giving a longer lecture.

NEXT
Preparing for the assignment. Move on after a learner can explain the current example or required action.

## Slide 33 — Preparing for the assignment

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

## Slide 34 — Data types and filters

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

## Slide 35 — Data types and filters continued

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

## Slide 36 — Your issued assignment

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

## Slide 37 — q1: 3 marks

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

## Slide 38 — q2: 3 marks

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

## Slide 39 — q3: 4 marks

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

## Slide 40 — q4: 4 marks

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

## Slide 41 — q5: 3 marks

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

## Slide 42 — q6: 3 marks

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

## Slide 43 — Pandas investigation submission

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

## Slide 44 — Project preparation

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

## Slide 45 — Week 5 quiz

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

## Slide 46 — Before you leave

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

