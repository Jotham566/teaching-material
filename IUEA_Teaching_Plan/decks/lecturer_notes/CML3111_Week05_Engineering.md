# CML3111 Week 5

## Slide 1: Using pandas to answer table questions

Using pandas to answer table questions
CML3111, Week 5, slide 1

Explanation to give
pandas performs table operations that build on the lists, records and loops already taught. Explain the row, column and unit before using an operation.

Worked illustration / lecturer answer
A filter retains matching rows. groupby gathers matching labels. For A:2, A:3, B:4, the totals are A:5 and B:4.

Misconception to address
Use this as an orientation to the lesson. Terms and syntax will be unpacked on their own slides; students do not need to know them in advance.

On this slide
Communications, Electrical, Mechatronics and Robotics Engineering

Continue to
Today’s learning

## Slide 2: Today’s learning

Today’s learning
CML3111, Week 5, slide 2

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

## Slide 3: DataFrame and column names

Explain each field before indexing. This file provides the observations for every calculation in the lesson.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 4: The supplied file

Uploading a notebook does not upload its data. Check the exact filename and column headings. Each cohort has its own data, so numerical results can differ.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 5: Operations for the next example

Import and short names
import pandas as pd loads pandas and gives it the short name pd. pd.read_csv refers to a function in that library.

Reading a CSV
pd.read_csv("filename.csv") reads the named file into a DataFrame: a table with labelled columns and row labels. The file must exist in the working folder.

Counting dimensions
table.shape gives (number of rows, number of columns). shape is a property, so it has no parentheses.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 6: Operations for the next example

Column data types
table.dtypes reports each column’s stored type. int64 means integers, float64 means decimal numbers, and object often contains text. Numeric blanks commonly appear as NaN.

A preview of rows
table.head() returns the first five rows. It leaves the table unchanged. A preview is not the entire dataset.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 7: Loading the supplied observations

Code walkthrough
Line 1: import pandas as pd
Load pandas. An import makes these names available; it does not run the analysis.

Line 2: raw = pd.read_csv("campus_energy.csv")
Read the supplied file into raw. Its rows remain the untouched source for this lesson.

Line 3: print(raw.head())
Display raw.head(). The first five observations and their column headings. Read one whole row aloud before discussing a column.

Line 4: print(raw.shape)
Display raw.shape. The pair is row count followed by column count.

Line 5: print(raw.dtypes)
Display raw.dtypes. Read each heading beside its stored type. float64 can include missing numerical entries.

Reading the result
The preview establishes the file schema. The row/column pair describes the full file, while head shows only five rows. Explain that NaN means a missing entry, not a measured zero.

Output from the supplied CSV (this cohort):
  meter_id     building        block    month   kwh  cost_ugx
0    M-001  Kabojja Lab  Engineering  2026-01  4820   3374000
1    M-001  Kabojja Lab  Engineering  2026-02  5310   3717000
2    M-001  Kabojja Lab  Engineering  2026-03  6140   4298000
3    M-002   Workshop A  Engineering  2026-01  7420   5194000
4    M-002   Workshop A  Engineering  2026-02  7980   5586000
(24, 6)
meter_id    object
building    object
block       object
month       object
kwh          int64
cost_ugx     int64
dtype: object


Further explanation
read_csv creates a DataFrame. head shows the first five rows. shape gives row and column counts. dtypes describes each column. raw remains unchanged throughout the lesson.

Complete worked example:
import pandas as pd
raw = pd.read_csv("campus_energy.csv")
print(raw.head())
print(raw.shape)
print(raw.dtypes)

Result from the supplied example
meter_id     building        block    month   kwh  cost_ugx
0    M-001  Kabojja Lab  Engineering  2026-01  4820   3374000
1    M-001  Kabojja Lab  Engineering  2026-02  5310   3717000
2    M-001  Kabojja Lab  Engineering  2026-03  6140   4298000
3    M-002   Workshop A  Engineering  2026-01  7420   5194000
4    M-002   Workshop A  Engineering  2026-02  7980   5586000
(24, 6)
meter_id    object
building    object
block       object
month       object
kwh          int64
cost_ugx     int64
dtype: object

## Slide 8: Selecting and summarising a column

The mean describes readings in this supplied file, not a general expected monthly use.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 9: Operations for the next example

Reading chained operations
Read a chain from left to right. In table["target"].mean(), select the target Series first, then calculate its mean. Each step uses the previous step’s result.

Rounded display
series.round(3) returns values rounded to three decimal places. Python round(number, 3) rounds one number. Keep unrounded calculations for returned assessment answers.

Selecting columns
table["column"] returns one labelled column, a Series. table[["a", "b"]] returns a DataFrame containing those named columns in that order.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 10: Operations for the next example

Mean of recorded values
series.mean() adds known values and divides by their count. pandas skips missing values by default. The result has the same unit as the original column.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 11: Energy values and their mean

Code walkthrough
Line 1: print(raw["kwh"].head())
Display raw['kwh'].head(). Read these values alongside their source column labels. The display does not change the calculation or source data.

Line 2: print(round(float(raw["kwh"].mean()), 3))
Display round(float(raw['kwh'].mean()), 3). Read these values alongside their source column labels. The display does not change the calculation or source data.

Reading the result
The displayed mean covers the entire kwh column, not just the five previewed readings. Its unit is kWh per recorded meter-month.

Output from the supplied CSV (this cohort):
0    4820
1    5310
2    6140
3    7420
4    7980
Name: kwh, dtype: int64
5666.042


Further explanation
head shows the first five readings. The mean uses the entire column.

Complete worked example:
print(raw["kwh"].head())
print(round(float(raw["kwh"].mean()), 3))

Result from the supplied example
0    4820
1    5310
2    6140
3    7420
4    7980
Name: kwh, dtype: int64
5666.042

## Slide 12: Ask a question about each energy reading

This is a practice question, not an engineering safety limit. Separate calculating the answers from selecting the rows. True and False are Boolean values, not the strings "True" and "False".

## Slide 13: Operations for the next example

Selecting rows with a mask
A column comparison produces one True or False per row. table[mask] keeps the True rows. & combines masks: both conditions must hold. Parenthesise each comparison.

Adding values and counting True
series.sum() adds its values. For a Boolean mask, True counts as 1 and False as 0. table.isna().sum() therefore counts missing cells separately for each column.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 14: Inspect the answers before selecting rows

Match the row labels in the two outputs. The comparison answers the question for every row and leaves raw unchanged.

Result from the supplied example
0    4820
1    5310
2    6140
3    7420
4    7980
Name: kwh, dtype: int64
0    False
1     True
2     True
3     True
4     True
Name: kwh, dtype: bool

## Slide 15: Use the True answers to select rows

Quoted names inside brackets select a named column; a True/False Series inside brackets selects rows. The question and the table must refer to matching row labels.

## Slide 16: Keep and count the high-energy readings

This result table contains the selected rows. We only inspect it here; the original raw table remains unchanged. The count should equal the number of retained rows. The supplied threshold is strictly greater than 5000, so exactly 5000 is excluded.

Result from the supplied example
meter_id     building        block    month   kwh  cost_ugx
1    M-001  Kabojja Lab  Engineering  2026-02  5310   3717000
2    M-001  Kabojja Lab  Engineering  2026-03  6140   4298000
3    M-002   Workshop A  Engineering  2026-01  7420   5194000
4    M-002   Workshop A  Engineering  2026-02  7980   5586000
5    M-002   Workshop A  Engineering  2026-03  8115   5680500
14

## Slide 17: Groups and labels

The maximum is a building label, not a row number. Group totals cover the months present in the CSV.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 18: Operations for the next example

Counting distinct labels
series.nunique() counts different recorded values, ignoring missing values by default. It counts categories rather than rows.

Label of the largest value
series.idxmax() returns the label attached to the largest value. It does not return that value. If several entries tie, it returns the first such label.

Grouping rows
table.groupby("label")["value"] groups the value column by matching labels. Apply mean() or sum() to calculate one result per group. Missing group labels are excluded by default.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 19: Building totals from campus_energy.csv

Code walkthrough
Line 1: totals = raw.groupby("building")["kwh"].sum()
Group all source rows by building and add each group’s recorded energy.

Line 2: print(totals)
Display totals. Read these values alongside their source column labels. The display does not change the calculation or source data.

Line 3: print(raw["building"].nunique())
Display raw['building'].nunique(). Read these values alongside their source column labels. The display does not change the calculation or source data.

Line 4: print(totals.idxmax())
Display totals.idxmax(). Read these values alongside their source column labels. The display does not change the calculation or source data.

Reading the result
The labelled totals add energy over the recorded months. The distinct-label count is the number of buildings, and the final name identifies the largest total.

Output from the supplied CSV (this cohort):
building
Admin Tower        7385
Hostel Block C    29530
Hostel Block D    26745
Kabojja Lab       16270
Lecture Hall 2     5685
Library            9650
Server Room       17205
Workshop A        23515
Name: kwh, dtype: int64
8
Hostel Block C


Further explanation
Trace one building back to its source rows. pandas performs the grouping and addition.

Complete worked example:
totals = raw.groupby("building")["kwh"].sum()
print(totals)
print(raw["building"].nunique())
print(totals.idxmax())

Result from the supplied example
building
Admin Tower        7385
Hostel Block C    29530
Hostel Block D    26745
Kabojja Lab       16270
Lecture Hall 2     5685
Library            9650
Server Room       17205
Workshop A        23515
Name: kwh, dtype: int64
8
Hostel Block C

## Slide 20: A calculated energy rate

A zero denominator cannot define a unit rate. Filtering here is for this rate demonstration, not an instruction to delete the original observation.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 21: Operations for the next example

Adding or replacing a column
table["name"] = values assigns that column. An array follows row order. A Series aligns by row label, so keep labels paired with the intended observations.

Column arithmetic
Arithmetic on columns calculates one result per row. Series align by row label. Divide only where the denominator is valid and keep actual and predicted observations paired.

A separate working table
table.copy() creates a working copy. Assigning columns on this copy preserves the source table, so you can compare before and after.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 22: Rates from recorded cost and energy

Code walkthrough
Line 1: priced = raw[raw["kwh"] > 0].copy()
Select positive energy readings and copy them before calculating a unit rate.

Line 2: priced["rate_ugx_per_kwh"] = priced["cost_ugx"] / priced["kwh"]
Divide each recorded cost by its paired positive energy reading. The new column has units UGX/kWh.

Line 3: print(priced[["building", "kwh", "cost_ugx", "rate_ugx_per_kwh"]].head())
Display priced[['building', 'kwh', 'cost_ugx', 'rate_ugx_per_kwh']].head(). Read these values alongside their source column labels. The display does not change the calculation or source data.

Reading the result
For any displayed row, divide cost_ugx by kwh to reproduce the rate. Compare rates only where energy is positive.

Output from the supplied CSV (this cohort):
      building   kwh  cost_ugx  rate_ugx_per_kwh
0  Kabojja Lab  4820   3374000             700.0
1  Kabojja Lab  5310   3717000             700.0
2  Kabojja Lab  6140   4298000             700.0
3   Workshop A  7420   5194000             700.0
4   Workshop A  7980   5586000             700.0


Further explanation
The two columns come from the same source row. Double brackets select a list of columns in the requested display order.

Complete worked example:
priced = raw[raw["kwh"] > 0].copy()
priced["rate_ugx_per_kwh"] = priced["cost_ugx"] / priced["kwh"]
print(priced[["building", "kwh", "cost_ugx", "rate_ugx_per_kwh"]].head())

Result from the supplied example
building   kwh  cost_ugx  rate_ugx_per_kwh
0  Kabojja Lab  4820   3374000             700.0
1  Kabojja Lab  5310   3717000             700.0
2  Kabojja Lab  6140   4298000             700.0
3   Workshop A  7420   5194000             700.0
4   Workshop A  7980   5586000             700.0

## Slide 23: Your issued assignment

Your issued assignment
CML3111, Week 5, slide 34

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

## Slide 24: q1: 3 marks

Required interface: q1: 3 marks

Load campus_energy.csv into a DataFrame called df.

Keep these exact output keys and the function name. You may use descriptive local variable names, such as true_positive_count, but the returned dictionary must use the published key, such as tp. The grader checks keys and values; changing a key changes the interface.

## Slide 25: q2: 3 marks

Required interface: q2: 3 marks

Set n_meters to the number of distinct meters in the file.

Keep these exact output keys and the function name. You may use descriptive local variable names, such as true_positive_count, but the returned dictionary must use the published key, such as tp. The grader checks keys and values; changing a key changes the interface.

## Slide 26: q3: 4 marks

Required interface: q3: 4 marks

Add a column cost_per_kwh to df, equal to cost_ugx / kwh.

Keep these exact output keys and the function name. You may use descriptive local variable names, such as true_positive_count, but the returned dictionary must use the published key, such as tp. The grader checks keys and values; changing a key changes the interface.

## Slide 27: q4: 4 marks

Required interface: q4: 4 marks

Set high_use to the rows of df where kwh is greater than 5000.

Do this after q3 so the derived column comes along.

Keep these exact output keys and the function name. You may use descriptive local variable names, such as true_positive_count, but the returned dictionary must use the published key, such as tp. The grader checks keys and values; changing a key changes the interface.

## Slide 28: q5: 3 marks

Required interface: q5: 3 marks

Set mean_cost_per_kwh to the mean of the cost_per_kwh column.

Keep these exact output keys and the function name. You may use descriptive local variable names, such as true_positive_count, but the returned dictionary must use the published key, such as tp. The grader checks keys and values; changing a key changes the interface.

## Slide 29: q6: 3 marks

Required interface: q6: 3 marks

Set peak_building to the name of the building with the highest total kwh.

Keep these exact output keys and the function name. You may use descriptive local variable names, such as true_positive_count, but the returned dictionary must use the published key, such as tp. The grader checks keys and values; changing a key changes the interface.

## Slide 30: Pandas investigation submission

Pandas investigation submission
CML3111, Week 5, slide 41

Explanation to give
This slide hands over CML3111 W05. Show the exact form title before uploading. The required packet is one completed .ipynb notebook.

Worked illustration / lecturer answer
The recorded cutoff for this form is 2026-10-16T11:00:00+03:00. Check the live form for later changes. A replacement must contain the complete required file set, not just the changed file.

Misconception to address
Students enter their own Student Registration Number as required freeform text. They wait for filenames to appear, press Submit and keep the confirmation. A file saved in Drive or GitHub is not itself a form submission.

On this slide
Opens: 07 Oct 2026, 11:00 Kampala

Deadline: 16 Oct 2026, 11:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

Continue to
Project preparation

## Slide 31: Project preparation

Project preparation
CML3111, Week 5, slide 42

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

Published deadline: 30 Oct 2026, 11:00 Kampala

Continue to
Week 5 quiz

## Slide 32: Week 5 quiz

Week 5 quiz
CML3111, Week 5, slide 43

Explanation to give
This is the CML3111 Week 5 quiz. The student link opens the response form; it does not activate its window. In Quiz Controls use open_W5_CML3111 when ready and read the logged closing time.

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

## Slide 33: Week 5 support

Week 5 support
CML3111, Week 5, slide 44

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

## Slide 34: Revision and submission checklist

Revision and submission checklist
CML3111, Week 5, slide 45

Explanation to give
pandas performs table operations that build on the lists, records and loops already taught. Explain the row, column and unit before using an operation.

Worked illustration / lecturer answer
A filter retains matching rows. groupby gathers matching labels. For A:2, A:3, B:4, the totals are A:5 and B:4.

Misconception to address
Close by identifying the actual saved file and its correct submission route. Read the live deadline. For current weekly notebook tasks, students upload their own work, not the practice notebook, ZIP or grading files.

On this slide
You can explain which observations a filter keeps and what a grouped total means.

Save your work and check the required submission files.