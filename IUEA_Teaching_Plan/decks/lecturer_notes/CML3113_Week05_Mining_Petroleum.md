# CML3113 Week05 Mining Petroleum

Lecturer companion. The same explanations are embedded in the PowerPoint speaker notes. Open Presenter View, or expand the Notes pane when preparing.

## Slide 1 — Using pandas to answer table questions

Using pandas to answer table questions
CML3113, Week 5, slide 1

Explanation to give
pandas performs table operations that build on the lists, records and loops already taught. Explain the row, column and unit before using an operation.

Worked illustration / lecturer answer
A filter retains matching rows. groupby gathers matching labels. For A:2, A:3, B:4, the totals are A:5 and B:4.

Misconception to address
Use this as an orientation to the lesson. Terms and syntax will be unpacked on their own slides; students do not need to know them in advance.

On this slide
Mining and Petroleum Engineering

Continue to
Today’s learning

## Slide 2 — Today’s learning

Today’s learning
CML3113, Week 5, slide 2

Explanation to give
pandas performs table operations that build on the lists, records and loops already taught. Explain the row, column and unit before using an operation.

Worked illustration / lecturer answer
A filter retains matching rows. groupby gathers matching labels. For A:2, A:3, B:4, the totals are A:5 and B:4.

Misconception to address
At the end, check the specific outcome shown here using a small previously demonstrated example. A completed file without an explanation is not evidence of understanding.

On this slide
Read a labelled table and select rows.

Calculate column summaries and grouped totals.

Continue to
Connection to the previous lesson

## Slide 3 — Connection to the previous lesson

Connection to the previous lesson
CML3113, Week 5, slide 3

Explanation to give
pandas performs table operations that build on the lists, records and loops already taught. Explain the row, column and unit before using an operation.

Worked illustration / lecturer answer
A filter retains matching rows. groupby gathers matching labels. For A:2, A:3, B:4, the totals are A:5 and B:4.

Misconception to address
Connect this to the previous result named on this slide. Demonstrate the first step again if necessary; there is no requirement for partner work before the explanation.

On this slide
Week 4 used lists, dictionaries, loops and CSV rows. pandas keeps these same records in a labelled table and provides operations that work across its columns.

Continue to
Why this week’s tools are needed

## Slide 4 — Why this week’s tools are needed

Why this week’s tools are needed
CML3113, Week 5, slide 4

Explanation to give
pandas performs table operations that build on the lists, records and loops already taught. Explain the row, column and unit before using an operation.

Worked illustration / lecturer answer
A filter retains matching rows. groupby gathers matching labels. For A:2, A:3, B:4, the totals are A:5 and B:4.

Misconception to address
Connect this to the previous result named on this slide. Demonstrate the first step again if necessary; there is no requirement for partner work before the explanation.

On this slide
The supplied campus_energy.csv records campus electricity use. We practise pandas on four invented rows first, then inspect the supplied file and its units.

Continue to
Rows columns and units

## Slide 5 — Rows columns and units

Rows columns and units
CML3113, Week 5, slide 5

Explanation to give
A DataFrame is a labelled table. Each row describes one observation and each column holds one field across observations. pandas is the library; pd is the short name we choose when importing it.

Worked illustration / lecturer answer
A building label and its kWh belong on the same row. If building A has two rows, that is two observations of A, not necessarily two different buildings. pd.DataFrame(...) constructs the table from supplied data.

Misconception to address
Row count and distinct-building count answer different questions. kW measures power while kWh measures energy accumulated over time.

On this slide
A row describes one observation. A column describes one field.

A DataFrame is pandas’ labelled table.

A Series is one labelled column.

kWh measures energy. kW measures power.

A data type (dtype) describes the kind of values in a column, such as whole numbers, decimals or text.

Continue to
A table keeps related observations together

## Slide 6 — A table keeps related observations together

A table keeps related observations together
CML3113, Week 5, slide 6

Explanation to give
A DataFrame is a labelled table. Each row describes one observation and each column holds one field across observations. pandas is the library; pd is the short name we choose when importing it.

Worked illustration / lecturer answer
A building label and its kWh belong on the same row. If building A has two rows, that is two observations of A, not necessarily two different buildings. pd.DataFrame(...) constructs the table from supplied data.

Misconception to address
Row count and distinct-building count answer different questions. kW measures power while kWh measures energy accumulated over time.

On this slide
Our four rows record building A twice and building B twice.

Each row contains the building label and an energy reading.

kWh is energy. kW is power. The units describe different quantities.

Continue to
Our small energy table

## Slide 7 — Our small energy table

Our small energy table
CML3113, Week 5, slide 7

Explanation to give
A DataFrame is a labelled table. Each row describes one observation and each column holds one field across observations. pandas is the library; pd is the short name we choose when importing it.

Worked illustration / lecturer answer
A building label and its kWh belong on the same row. If building A has two rows, that is two observations of A, not necessarily two different buildings. pd.DataFrame(...) constructs the table from supplied data.

Misconception to address
Row count and distinct-building count answer different questions. kW measures power while kWh measures energy accumulated over time.

On this slide
building | kwh
A | 2
A | 4
B | 5
B | 7
The four observations total 18 kWh.

Continue to
Library and pandas and DataFrame

## Slide 8 — Library and pandas and DataFrame

Library and pandas and DataFrame
CML3113, Week 5, slide 8

Explanation to give
A DataFrame is a labelled table. Each row describes one observation and each column holds one field across observations. pandas is the library; pd is the short name we choose when importing it.

Worked illustration / lecturer answer
A building label and its kWh belong on the same row. If building A has two rows, that is two observations of A, not necessarily two different buildings. pd.DataFrame(...) constructs the table from supplied data.

Misconception to address
Row count and distinct-building count answer different questions. kW measures power while kWh measures energy accumulated over time.

On this slide
Library and pandas: A library is reusable code. pandas provides tools for data tables. import pandas as pd makes pd a short name for that library.
DataFrame: A table with named columns and indexed rows. df is just the variable name we choose for this table.

Continue to
A labelled table in Python

## Slide 9 — A labelled table in Python

A labelled table in Python
CML3113, Week 5, slide 9

Explanation to give
A DataFrame is a labelled table. Each row describes one observation and each column holds one field across observations. pandas is the library; pd is the short name we choose when importing it.

Worked illustration / lecturer answer
A building label and its kWh belong on the same row. If building A has two rows, that is two observations of A, not necessarily two different buildings. pd.DataFrame(...) constructs the table from supplied data.

Misconception to address
Row count and distinct-building count answer different questions. kW measures power while kWh measures energy accumulated over time.

On this slide
The illustration uses machinery records. The same row, column and index structure applies to our building-energy table.

Continue to
Series and Method and attribute

## Slide 10 — Series and Method and attribute

Series and Method and attribute
CML3113, Week 5, slide 10

Explanation to give
Selecting df["kwh"] gives one column as a Series, retaining its row labels. Calling .mean() then summarises that column. An attribute such as shape reports information without parentheses.

Worked illustration / lecturer answer
For kWh values 2, 4 and 9, the mean is 15 / 3 = 5. df.shape reports row and column counts; df.head() displays an initial sample of rows.

Misconception to address
df["kwh"] and df[["kwh"]] have different shapes: a Series versus a one-column DataFrame. Brackets select; parentheses call an operation.

On this slide
Series: One labelled column. df["kwh"] selects the column named kwh.
Method and attribute: A method performs an operation, as in df.head(). An attribute provides a stored property, as in df.shape. Parentheses call an operation.

Continue to
Reading pandas syntax

## Slide 11 — Reading pandas syntax

Reading pandas syntax
CML3113, Week 5, slide 11

Explanation to give
Selecting df["kwh"] gives one column as a Series, retaining its row labels. Calling .mean() then summarises that column. An attribute such as shape reports information without parentheses.

Worked illustration / lecturer answer
For kWh values 2, 4 and 9, the mean is 15 / 3 = 5. df.shape reports row and column counts; df.head() displays an initial sample of rows.

Misconception to address
df["kwh"] and df[["kwh"]] have different shapes: a Series versus a one-column DataFrame. Brackets select; parentheses call an operation.

On this slide
import pandas as pd loads the library and gives it a short name.

pd.read_csv("file.csv") calls a function. The quoted text is the file path.

df["kwh"] selects a column. df["kwh"].mean() calls a method on that column.

Continue to
Read the table constructor in stages

## Slide 12 — Read the table constructor in stages

Read the table constructor in stages
CML3113, Week 5, slide 12

Explanation to give
A DataFrame is a labelled table. Each row describes one observation and each column holds one field across observations. pandas is the library; pd is the short name we choose when importing it.

Worked illustration / lecturer answer
A building label and its kWh belong on the same row. If building A has two rows, that is two observations of A, not necessarily two different buildings. pd.DataFrame(...) constructs the table from supplied data.

Misconception to address
Row count and distinct-building count answer different questions. kW measures power while kWh measures energy accumulated over time.

On this slide
import pandas as pd loads pandas and gives it the shorter name pd. This is an alias; you could use another name consistently.

Inside pd.DataFrame(...), the dictionary keys become column names. Each list supplies that column’s values in row order.

All these column lists have the same length. At position 0, building is "A" and kwh is 2; together they form the first row.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Build the table before asking questions

## Slide 13 — Build the table before asking questions

Build the table before asking questions
CML3113, Week 5, slide 13

Explanation to give
A DataFrame is a labelled table. Each row describes one observation and each column holds one field across observations. pandas is the library; pd is the short name we choose when importing it.

Worked illustration / lecturer answer
A building label and its kWh belong on the same row. If building A has two rows, that is two observations of A, not necessarily two different buildings. pd.DataFrame(...) constructs the table from supplied data.

Misconception to address
Row count and distinct-building count answer different questions. kW measures power while kWh measures energy accumulated over time.

Read the displayed code line by line
import pandas as pd
Load this library. An alias after as is the shorter name used below.

df = pd.DataFrame({"building": ["A", "A", "B", "B"],
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

"kwh": [2, 4, 5, 7]})
This line continues the surrounding expression or block; read it together with the preceding line rather than running it alone.

print(df)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Each dictionary key becomes a column name. Equal-length lists supply its rows.

Continue to
Select first then summarise

## Slide 14 — Select first then summarise

Select first then summarise
CML3113, Week 5, slide 14

Explanation to give
Selecting df["kwh"] gives one column as a Series, retaining its row labels. Calling .mean() then summarises that column. An attribute such as shape reports information without parentheses.

Worked illustration / lecturer answer
For kWh values 2, 4 and 9, the mean is 15 / 3 = 5. df.shape reports row and column counts; df.head() displays an initial sample of rows.

Misconception to address
df["kwh"] and df[["kwh"]] have different shapes: a Series versus a one-column DataFrame. Brackets select; parentheses call an operation.

On this slide
df["kwh"] selects the energy column as a Series, which is a labelled sequence of values. Its entries are 2, 4, 5 and 7.

Store it as energy = df["kwh"]. energy.mean() adds those four values and divides by four: 18 / 4 = 4.5.

df["kwh"].mean() combines those same two steps. A dot chooses a method; parentheses call it.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Select a column and calculate its mean

## Slide 15 — Select a column and calculate its mean

Select a column and calculate its mean
CML3113, Week 5, slide 15

Explanation to give
Selecting df["kwh"] gives one column as a Series, retaining its row labels. Calling .mean() then summarises that column. An attribute such as shape reports information without parentheses.

Worked illustration / lecturer answer
For kWh values 2, 4 and 9, the mean is 15 / 3 = 5. df.shape reports row and column counts; df.head() displays an initial sample of rows.

Misconception to address
df["kwh"] and df[["kwh"]] have different shapes: a Series versus a one-column DataFrame. Brackets select; parentheses call an operation.

Read the displayed code line by line
print(df["kwh"])
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(df["kwh"].mean())
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
The four numbers are 2, 4, 5 and 7. Their mean is 18 / 4 = 4.5 kWh.

Continue to
Mask and filter

## Slide 16 — Mask and filter

Mask and filter
CML3113, Week 5, slide 16

Explanation to give
A comparison against a column creates one True/False result per row. That Boolean mask selects rows. Explain the mask first and only then put it inside df[...].

Worked illustration / lecturer answer
With kWh [2, 5, 8], the mask kwh > 5 is [False, False, True]. Applying it keeps only the row with 8. Using >= 5 would keep two rows.

Misconception to address
A mask is not the filtered table. Also check the column contains numbers, since text comparisons follow different rules.

On this slide
Mask and filter: A comparison produces True/False for each row. df[mask] keeps the True rows.

Continue to
A comparison creates a Boolean mask

## Slide 17 — A comparison creates a Boolean mask

A comparison creates a Boolean mask
CML3113, Week 5, slide 17

Explanation to give
A comparison against a column creates one True/False result per row. That Boolean mask selects rows. Explain the mask first and only then put it inside df[...].

Worked illustration / lecturer answer
With kWh [2, 5, 8], the mask kwh > 5 is [False, False, True]. Applying it keeps only the row with 8. Using >= 5 would keep two rows.

Misconception to address
A mask is not the filtered table. Also check the column contains numbers, since text comparisons follow different rules.

On this slide
The illustration filters torque readings. Our next example applies the same True/False selection to kWh values.

Continue to
Keep rows where the comparison is true

## Slide 18 — Keep rows where the comparison is true

Keep rows where the comparison is true
CML3113, Week 5, slide 18

Explanation to give
A comparison against a column creates one True/False result per row. That Boolean mask selects rows. Explain the mask first and only then put it inside df[...].

Worked illustration / lecturer answer
With kWh [2, 5, 8], the mask kwh > 5 is [False, False, True]. Applying it keeps only the row with 8. Using >= 5 would keep two rows.

Misconception to address
A mask is not the filtered table. Also check the column contains numbers, since text comparisons follow different rules.

Read the displayed code line by line
mask = df["kwh"] > 4
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(mask)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(df[mask])
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
The mask is False, False, True, True. The selected rows contain 5 and 7 kWh.

Continue to
groupby and aggregation

## Slide 19 — groupby and aggregation

groupby and aggregation
CML3113, Week 5, slide 19

Explanation to give
Split rows into groups with the same label, select the quantity to summarise, then apply the aggregation. Read a chained expression as several small operations on the previous result.

Worked illustration / lecturer answer
For A values 2 and 3, and B value 4, grouped totals are A:5 and B:4. totals.max() returns 5, while totals.idxmax() returns the label A.

Misconception to address
nunique counts distinct labels, not records. idxmax returns an index label; it is the appropriate result only when the question asks which group is largest.

On this slide
groupby and aggregation: groupby collects rows with the same label. An aggregation such as sum or mean returns a summary for each group.

Continue to
Trace a group total before using groupby

## Slide 20 — Trace a group total before using groupby

Trace a group total before using groupby
CML3113, Week 5, slide 20

Explanation to give
Split rows into groups with the same label, select the quantity to summarise, then apply the aggregation. Read a chained expression as several small operations on the previous result.

Worked illustration / lecturer answer
For A values 2 and 3, and B value 4, grouped totals are A:5 and B:4. totals.max() returns 5, while totals.idxmax() returns the label A.

Misconception to address
nunique counts distinct labels, not records. idxmax returns an index label; it is the appropriate result only when the question asks which group is largest.

On this slide
Group | Values assigned to it | Total
A | 2 and 4 | 6
B | 5 and 7 | 12
groupby separates rows by the building label. sum adds the kWh values inside each group.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Read each step of a pandas chain

## Slide 21 — Read each step of a pandas chain

Read each step of a pandas chain
CML3113, Week 5, slide 21

Explanation to give
Split rows into groups with the same label, select the quantity to summarise, then apply the aggregation. Read a chained expression as several small operations on the previous result.

Worked illustration / lecturer answer
For A values 2 and 3, and B value 4, grouped totals are A:5 and B:4. totals.max() returns 5, while totals.idxmax() returns the label A.

Misconception to address
nunique counts distinct labels, not records. idxmax returns an index label; it is the appropriate result only when the question asks which group is largest.

On this slide
groups = df.groupby("building") describes groups of rows with matching building labels.

energy_groups = groups["kwh"] selects the energy values within those groups. totals = energy_groups.sum() calculates one total per group.

df.groupby("building")["kwh"].sum() is the same sequence written on one line. Read it from left to right.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Calculate one total for each building

## Slide 22 — Calculate one total for each building

Calculate one total for each building
CML3113, Week 5, slide 22

Explanation to give
Distinguish a group total from a group mean and from the number of observations. Work one named group's arithmetic by hand before reading the pandas result.

Worked illustration / lecturer answer
If A has readings 2 and 3, its sum is 5 and its mean is 2.5. The label A remains attached to the summary, so another reader knows which building it describes.

Misconception to address
A taller total can reflect more observations rather than greater typical use. Choose the aggregation that matches the question.

Read the displayed code line by line
print(df.groupby("building")["kwh"].sum())
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Expected: A totals 6 kWh; B totals 12 kWh.

Continue to
pandas tables and summaries results

## Slide 23 — pandas tables and summaries results

pandas tables and summaries results
CML3113, Week 5, slide 23

Explanation to give
Distinguish a group total from a group mean and from the number of observations. Work one named group's arithmetic by hand before reading the pandas result.

Worked illustration / lecturer answer
If A has readings 2 and 3, its sum is 5 and its mean is 2.5. The label A remains attached to the summary, so another reader knows which building it describes.

Misconception to address
A taller total can reflect more observations rather than greater typical use. Choose the aggregation that matches the question.

On this slide
Mean 4.5. The filter keeps B rows with 5 and 7. Group totals: A = 6, B = 12 kWh.

Continue to
Unique labels and the largest group

## Slide 24 — Unique labels and the largest group

Unique labels and the largest group
CML3113, Week 5, slide 24

Explanation to give
Split rows into groups with the same label, select the quantity to summarise, then apply the aggregation. Read a chained expression as several small operations on the previous result.

Worked illustration / lecturer answer
For A values 2 and 3, and B value 4, grouped totals are A:5 and B:4. totals.max() returns 5, while totals.idxmax() returns the label A.

Misconception to address
nunique counts distinct labels, not records. idxmax returns an index label; it is the appropriate result only when the question asks which group is largest.

On this slide
nunique counts distinct labels, not rows. idxmax returns the label of the largest total.

Here there is no tie.

Continue to
Unique labels and the largest group in Python

## Slide 25 — Unique labels and the largest group in Python

Unique labels and the largest group in Python
CML3113, Week 5, slide 25

Explanation to give
Split rows into groups with the same label, select the quantity to summarise, then apply the aggregation. Read a chained expression as several small operations on the previous result.

Worked illustration / lecturer answer
For A values 2 and 3, and B value 4, grouped totals are A:5 and B:4. totals.max() returns 5, while totals.idxmax() returns the label A.

Misconception to address
nunique counts distinct labels, not records. idxmax returns an index label; it is the appropriate result only when the question asks which group is largest.

Read the displayed code line by line
print(df["building"].nunique())
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

totals = df.groupby("building")["kwh"].sum()
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(totals.idxmax())
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Create a column from two existing columns

## Slide 26 — Create a column from two existing columns

Create a column from two existing columns
CML3113, Week 5, slide 26

Explanation to give
A derived column combines existing columns row by row. Track units through the division. Cost divided by energy gives a rate in currency per kWh.

Worked illustration / lecturer answer
A fictional bill of 6,000 UGX for 10 kWh gives 600 UGX/kWh. Create that rate before filtering if later work needs the column in the filtered table.

Misconception to address
The average of individual rates is generally different from total cost divided by total energy. Use the operation the question actually specifies and check zero-energy cases.

On this slide
A new column can store a calculation for every row. Division pairs the values in matching rows.

For this invented table all energy values are positive. UGX is Uganda shillings. Cost divided by energy has units UGX/kWh.

Continue to
An energy rate is cost divided by energy

## Slide 27 — An energy rate is cost divided by energy

An energy rate is cost divided by energy
CML3113, Week 5, slide 27

Explanation to give
A derived column combines existing columns row by row. Track units through the division. Cost divided by energy gives a rate in currency per kWh.

Worked illustration / lecturer answer
A fictional bill of 6,000 UGX for 10 kWh gives 600 UGX/kWh. Create that rate before filtering if later work needs the column in the filtered table.

Misconception to address
The average of individual rates is generally different from total cost divided by total energy. Use the operation the question actually specifies and check zero-energy cases.

Read the displayed code line by line
df["cost_ugx"] = [1000, 2400, 3500, 5600]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

df["rate_ugx_per_kwh"] = df["cost_ugx"] / df["kwh"]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(df["rate_ugx_per_kwh"])
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Expected rates: 500, 600, 700 and 800 UGX/kWh. Keep units in column names.

Continue to
Load the assignment table before analysing it

## Slide 28 — Load the assignment table before analysing it

Load the assignment table before analysing it
CML3113, Week 5, slide 28

Explanation to give
Explain the difference between loading a table and understanding it. read_csv opens the supplied file; inspection checks that the expected rows, fields and units arrived before any analysis.

Worked illustration / lecturer answer
Show df.head(), df.shape and df.dtypes as three views of the same table. The Week 5 campus_energy.csv is a fictional 24-row teaching file with repeated meter observations.

Misconception to address
A successful read does not prove the right file was loaded. Check the filename, the header and the number of records before calculating.

On this slide
Upload campus_energy.csv to the current runtime first. read_csv reads it into a new DataFrame.

head() displays the first five rows; shape gives row and column counts; dtypes shows column data types.

We call this issued_table to keep it separate from the invented four-row df used above.

Current notebook workflow
The latest student package contains no grader scripts or g.check cells. Restart and run the completed notebook, then submit it. Existing older submissions remain valid.

Continue to
Inspect the supplied energy file

## Slide 29 — Inspect the supplied energy file

Inspect the supplied energy file
CML3113, Week 5, slide 29

Explanation to give
Explain the difference between loading a table and understanding it. read_csv opens the supplied file; inspection checks that the expected rows, fields and units arrived before any analysis.

Worked illustration / lecturer answer
Show df.head(), df.shape and df.dtypes as three views of the same table. The Week 5 campus_energy.csv is a fictional 24-row teaching file with repeated meter observations.

Misconception to address
A successful read does not prove the right file was loaded. Check the filename, the header and the number of records before calculating.

Read the displayed code line by line
issued_table = pd.read_csv("campus_energy.csv")
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(issued_table.head())
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(issued_table.shape)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(issued_table.dtypes)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Check column names, data types and units before attempting the six issued tasks.

Continue to
Revision example and answer

## Slide 30 — Revision example and answer

Revision example and answer
CML3113, Week 5, slide 30

Explanation to give
Use the displayed example as a short individual revision question, then explain the reasoning behind its answer.

Worked illustration / lecturer answer
Example: Use > 5 instead. Predict the surviving rows. Which building has the largest total?

Answer: Only the row with 7 survives. Building B has the larger total, 12 kWh.

Misconception to address
Trace the operation that changes the value rather than accepting a memorised output. For notebook-state examples, specify which cell is repeated and whether the initialisation ran again.

Continue to
Preparing for the assignment

## Slide 31 — Preparing for the assignment

Preparing for the assignment
CML3113, Week 5, slide 31

Explanation to give
A5 uses the supplied campus_energy.csv and six named pandas outputs. Start with the loaded table, then create the rate column before taking the filtered subset.

Worked illustration / lecturer answer
Distinguish distinct meter count, a mean rate and the building with greatest total energy. These are three different questions about the same table.

Misconception to address
Return the exact requested values in one completed notebook. The learner does not upload data, ZIPs, helper scripts or a separate report for A5.

On this slide
A5 uses the supplied fictional campus_energy.csv, not a live Kaggle download.

The six tasks use read_csv, nunique, division of columns, a > filter, mean and grouped totals. idxmax returns the label of the largest value.

A mean of individual rates gives each observation equal weight.

Total cost divided by total energy weights by energy.

Current notebook workflow
The latest student package contains no grader scripts or g.check cells. Restart and run the completed notebook, then submit it. Existing older submissions remain valid.

Continue to
Data types and filters

## Slide 32 — Data types and filters

Data types and filters
CML3113, Week 5, slide 32

Explanation to give
A comparison against a column creates one True/False result per row. That Boolean mask selects rows. Explain the mask first and only then put it inside df[...].

Worked illustration / lecturer answer
With kWh [2, 5, 8], the mask kwh > 5 is [False, False, True]. Applying it keeps only the row with 8. Using >= 5 would keep two rows.

Misconception to address
A mask is not the filtered table. Also check the column contains numbers, since text comparisons follow different rules.

On this slide
A Boolean mask is a list-like column of True/False values. len(mask) counts all rows; mask.sum() counts True entries.

Strings sort as text, so "9" can rank above "100".

Inspect numeric types before taking maxima.

KeyError often means the column name does not match; check spelling, case and spaces. shape is (rows, columns).

Continue to
Data types and filters continued

## Slide 33 — Data types and filters continued

Data types and filters continued
CML3113, Week 5, slide 33

Explanation to give
A comparison against a column creates one True/False result per row. That Boolean mask selects rows. Explain the mask first and only then put it inside df[...].

Worked illustration / lecturer answer
With kWh [2, 5, 8], the mask kwh > 5 is [False, False, True]. Applying it keeps only the row with 8. Using >= 5 would keep two rows.

Misconception to address
A mask is not the filtered table. Also check the column contains numbers, since text comparisons follow different rules.

On this slide
Read provenance and units before trusting a dataset.

Continue to
Your issued assignment

## Slide 34 — Your issued assignment

Your issued assignment
CML3113, Week 5, slide 34

Explanation to give
A5 uses the supplied campus_energy.csv and six named pandas outputs. Start with the loaded table, then create the rate column before taking the filtered subset.

Worked illustration / lecturer answer
Distinguish distinct meter count, a mean rate and the building with greatest total energy. These are three different questions about the same table.

Misconception to address
Return the exact requested values in one completed notebook. The learner does not upload data, ZIPs, helper scripts or a separate report for A5.

On this slide
Open W05_student.ipynb.

Read every task and its input units before coding.

Keep the required function names and returned outputs.

Restart and run all cells, then save the completed notebook.

Current notebook workflow
The latest student package contains no grader scripts or g.check cells. Restart and run the completed notebook, then submit it. Existing older submissions remain valid.

Continue to
q1: 3 marks

## Slide 35 — q1: 3 marks

q1: 3 marks
CML3113, Week 5, slide 35

Explanation to give
Load the named CSV into df. Reading the file is different from constructing a new table with copied example values.

Worked illustration / lecturer answer
Inspect the header and 24-row file before analysis.

Misconception to address
The student submits the completed notebook only. Grading runs on the lecturer’s side; the current package needs no grading scripts.

On this slide
Load campus_energy.csv into a DataFrame called df.

Current notebook workflow
The latest student package contains no grader scripts or g.check cells. Restart and run the completed notebook, then submit it. Existing older submissions remain valid.

Continue to
q2: 3 marks

## Slide 36 — q2: 3 marks

q2: 3 marks
CML3113, Week 5, slide 36

Explanation to give
Count distinct meter_id values, not rows. A meter can contribute several monthly observations.

Worked illustration / lecturer answer
Two readings from M-001 count as one distinct meter.

Misconception to address
The student submits the completed notebook only. Grading runs on the lecturer’s side; the current package needs no grading scripts.

On this slide
Set n_meters to the number of distinct meters in the file.

Current notebook workflow
The latest student package contains no grader scripts or g.check cells. Restart and run the completed notebook, then submit it. Existing older submissions remain valid.

Continue to
q3: 4 marks

## Slide 37 — q3: 4 marks

q3: 4 marks
CML3113, Week 5, slide 37

Explanation to give
Create cost_per_kwh by dividing each row’s cost_ugx by its kwh.

Worked illustration / lecturer answer
For 6000 UGX and 10 kWh the rate is 600 UGX/kWh.

Misconception to address
The student submits the completed notebook only. Grading runs on the lecturer’s side; the current package needs no grading scripts.

On this slide
Add a column cost_per_kwh to df, equal to cost_ugx / kwh.

Current notebook workflow
The latest student package contains no grader scripts or g.check cells. Restart and run the completed notebook, then submit it. Existing older submissions remain valid.

Continue to
q4: 4 marks

## Slide 38 — q4: 4 marks

q4: 4 marks
CML3113, Week 5, slide 38

Explanation to give
Filter whole rows using the strict kwh > 5000 comparison, after creating the rate column.

Worked illustration / lecturer answer
A reading exactly 5000 does not pass this condition.

Misconception to address
The student submits the completed notebook only. Grading runs on the lecturer’s side; the current package needs no grading scripts.

On this slide
Set high_use to the rows of df where kwh is greater than 5000.

Do this after q3 so the derived column comes along.

Current notebook workflow
The latest student package contains no grader scripts or g.check cells. Restart and run the completed notebook, then submit it. Existing older submissions remain valid.

Continue to
q5: 3 marks

## Slide 39 — q5: 3 marks

q5: 3 marks
CML3113, Week 5, slide 39

Explanation to give
Find the mean of the created cost_per_kwh column, following the task’s stated table scope.

Worked illustration / lecturer answer
Mean of rates is not generally total cost divided by total energy.

Misconception to address
The student submits the completed notebook only. Grading runs on the lecturer’s side; the current package needs no grading scripts.

On this slide
Set mean_cost_per_kwh to the mean of the cost_per_kwh column.

Current notebook workflow
The latest student package contains no grader scripts or g.check cells. Restart and run the completed notebook, then submit it. Existing older submissions remain valid.

Continue to
q6: 3 marks

## Slide 40 — q6: 3 marks

q6: 3 marks
CML3113, Week 5, slide 40

Explanation to give
Sum kwh by building and return the label with the greatest total.

Worked illustration / lecturer answer
max gives a total; idxmax gives the label attached to that total.

Misconception to address
The student submits the completed notebook only. Grading runs on the lecturer’s side; the current package needs no grading scripts.

On this slide
Set peak_building to the name of the building with the highest total kwh.

Current notebook workflow
The latest student package contains no grader scripts or g.check cells. Restart and run the completed notebook, then submit it. Existing older submissions remain valid.

Continue to
Pandas investigation submission

## Slide 41 — Pandas investigation submission

Pandas investigation submission
CML3113, Week 5, slide 41

Explanation to give
This slide hands over CML3113 W05. Show the exact form title before uploading. The required packet is one completed .ipynb notebook.

Worked illustration / lecturer answer
The recorded cutoff for this form is 2026-10-16T08:00:00+03:00. Check the live form for later changes. A replacement must contain the complete required file set, not just the changed file.

Misconception to address
Students enter their own Student Registration Number as required freeform text. They wait for filenames to appear, press Submit and keep the confirmation. A file saved in Drive or GitHub is not itself a form submission.

On this slide
Opens: 07 Oct 2026, 08:00 Kampala

Deadline: 16 Oct 2026, 08:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

Continue to
Project preparation

## Slide 42 — Project preparation

Project preparation
CML3113, Week 5, slide 42

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

Published deadline: 30 Oct 2026, 08:00 Kampala

Continue to
Week 5 quiz

## Slide 43 — Week 5 quiz

Week 5 quiz
CML3113, Week 5, slide 43

Explanation to give
This is the CML3113 Week 5 quiz. The student link opens the response form; it does not activate its window. In Quiz Controls use open_W5_CML3113 when ready and read the logged closing time.

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
Week 5 support

## Slide 44 — Week 5 support

Week 5 support
CML3113, Week 5, slide 44

Explanation to give
This is a scheduling notice for the Friday cohorts. Confirm the faculty-approved replacement teaching arrangement before announcing details.

Worked illustration / lecturer answer
Provide a supported explanation of the pandas examples and an opportunity to ask questions. Begin the following session by revisiting column selection, masks and group summaries.

Misconception to address
A published upload deadline is separate from a replacement teaching session. Do not invent a session time or treat video-only homework as sufficient replacement support.

On this slide
Friday 9 October has no normal class.

The lecturer will announce a supported replacement session or recording with a clinic.

Week 6 starts with 30 minutes of consolidation.

Continue to
Revision and submission checklist

## Slide 45 — Revision and submission checklist

Revision and submission checklist
CML3113, Week 5, slide 45

Explanation to give
pandas performs table operations that build on the lists, records and loops already taught. Explain the row, column and unit before using an operation.

Worked illustration / lecturer answer
A filter retains matching rows. groupby gathers matching labels. For A:2, A:3, B:4, the totals are A:5 and B:4.

Misconception to address
Close by identifying the actual saved file and its correct submission route. Read the live deadline. For current weekly notebook tasks, students upload their own work, not the practice notebook, ZIP or grading files.

On this slide
You can explain which observations a filter keeps and what a grouped total means.

Save your work and check the required submission files.
