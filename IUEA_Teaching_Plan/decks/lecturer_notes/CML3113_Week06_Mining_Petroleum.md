# CML3113 Week 6

## Slide 1: Cleaning data and explaining changes

Cleaning data and explaining changes
Explanation to give
Inspect quality before interpreting a chart. Preserve raw records and justify each removal or estimated value.

Worked illustration / lecturer answer
A blank is not a measured zero. With observed values 20 and 24, median filling would insert an estimate of 22, which must be recorded as estimated.

Misconception to address
Use this as an orientation to the lesson. Terms and syntax will be unpacked on their own slides; students do not need to know them in advance.

On this slide
Mining and Petroleum Engineering

## Slide 2: Today: clean, check and explain

The aim is to understand each cleaning decision. Learners save their practice in Drive. A6 and Quiz 6 do not contribute to coursework marks; earlier submissions remain preserved. This waiver does not cancel other assessments.

## Slide 3: The supplied file

Uploading a notebook does not upload its data. Check the exact filename and column headings. Each cohort has its own data, so numerical results can differ.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 4: Operations for the next example

Import and short names
import pandas as pd loads pandas and gives it the short name pd. pd.read_csv refers to a function in that library.

Reading a CSV
pd.read_csv("filename.csv") reads the named file into a DataFrame: a table with labelled columns and row labels. The file must exist in the working folder.

Counting dimensions
table.shape gives (number of rows, number of columns). shape is a property, so it has no parentheses.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 5: Operations for the next example

Column data types
table.dtypes reports each column’s stored type. int64 means integers, float64 means decimal numbers, and object often contains text. Numeric blanks commonly appear as NaN.

A preview of rows
table.head() returns the first five rows. It leaves the table unchanged. A preview is not the entire dataset.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 6: Two names for two tables

Names are labels chosen by us, not special Python words. raw_data lets us check what was originally recorded; cleaned_data will hold the result of each cleaning step. Do not call every table data because we need to distinguish them.

## Slide 7: Loading the supplied observations

raw_data: the original table read from the CSV.

cleaned_data: a separate working table that we will change.

Step-by-step explanation

import pandas as pd
Load the named tools. Importing a model class does not train a model.

raw_data = pd.read_csv('engineering_data.csv')
raw_data stores original CSV table; keep it unchanged so the analysis can be checked.

print(raw_data.head())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(raw_data.shape)
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(raw_data.dtypes)
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
record_id equipment_id  load_pct  ambient_c  target
0          1           E1     59.15      31.71  14.001
1          2           E2     77.46      29.97  15.147
2          3           E3     69.60      19.87  13.005
3          4           E4     75.98      22.29     NaN
4          5           E5     57.62      23.40  12.554
(91, 5)
record_id         int64
equipment_id     object
load_pct        float64
ambient_c       float64
target          float64
dtype: object

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 8: EDA: understand the original observations

An ID is a label, not a measurement to average. The CSV is synthetic teaching data. Its patterns do not establish real engineering operating limits. Week 5 introduced EDA; here we repeat it as the first stage of a complete workflow.

## Slide 9: Check types and recorded values

count excludes missing cells. Quartiles split sorted values into four parts: 50% is the median, 25% and 75% bound the middle half. Standard deviation describes spread. Inspect measurements, not record IDs. A minimum below zero in load_pct flags a value to investigate.

## Slide 10: Inspect structure and numerical ranges

table.info() prints column types and non-missing counts. Call it directly; do not wrap it in print.

table[numeric_columns].describe() summarises selected numeric measurements: count, mean, standard deviation, minimum, quartiles and maximum.

Step-by-step explanation

raw_data.info()
Evaluate the displayed statement using the values produced by the preceding statements.

numeric_columns = ['load_pct', 'ambient_c', 'target']
numeric_columns stores the result of the displayed expression.

print(raw_data[numeric_columns].describe())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 91 entries, 0 to 90
Data columns (total 5 columns):
 #   Column        Non-Null Count  Dtype  
---  ------        --------------  -----  
 0   record_id     91 non-null     int64  
 1   equipment_id  91 non-null     object 
 2   load_pct      91 non-null     float64
 3   ambient_c     90 non-null     float64
 4   target        90 non-null     float64
dtypes: float64(3), int64(1), object(1)
memory usage: 3.7+ KB
        load_pct  ambient_c     target
count  91.000000  90.000000  90.000000
mean   56.027692  26.467444  12.115478
std    23.026181   4.641630   2.874421
min    -5.000000  18.350000   6.625000
25%    35.430000  22.562500   9.637000
50%    59.150000  26.045000  12.432000
75%    76.330000  30.772500  14.122500
max    93.150000  34.970000  17.295000

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 11: Check which equipment is represented

value_counts() counts rows for each label. dropna=False also shows missing labels.

Counts can reveal missing groups or unequal coverage. Repeated equipment IDs are expected; repeated record IDs need separate inspection.

## Slide 12: Count observations per equipment

value_counts() counts rows for each label. dropna=False also shows missing labels.

Counts can reveal missing groups or unequal coverage. Repeated equipment IDs are expected; repeated record IDs need separate inspection.

Step-by-step explanation

equipment_counts = raw_data['equipment_id'].value_counts(dropna=False)
equipment_counts stores the result of the displayed expression.

print(equipment_counts)
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
equipment_id
E1    16
E2    15
E3    15
E4    15
E5    15
E6    15
Name: count, dtype: int64

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 13: Preview the raw distribution

Read the horizontal axis as the target measurement and the vertical axis as observation count. This is an uncleaned preview. An extreme value is a reason to investigate, not automatic permission to delete it.

## Slide 14: Plot the target before cleaning

A histogram groups numeric values into intervals and counts observations in each interval. bins=10 requests ten intervals.

plt.subplots() gives a figure and its axes. ax selects where the chart is drawn. Missing numeric values are omitted from the plot.

Step-by-step explanation

import matplotlib.pyplot as plt
Load the named tools. Importing a model class does not train a model.

raw_figure, raw_axes = plt.subplots()
raw_figure stores the result of the displayed expression. raw_axes stores the result of the displayed expression.

raw_data['target'].plot.hist(bins=10, ax=raw_axes)
series.plot.hist(bins=10, ax=ax) groups known values into ten value intervals and counts observations in each. Bar heights are counts, not the original measurement values.

raw_axes.set_xlabel('crusher energy (kWh/t)')
Evaluate the displayed statement using the values produced by the preceding statements.

raw_axes.set_ylabel('Observation count')
Evaluate the displayed statement using the values produced by the preceding statements.

raw_axes.set_title('Before cleaning')
Evaluate the displayed statement using the values produced by the preceding statements.

plt.show()
Evaluate the displayed statement using the values produced by the preceding statements.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 15: Inspect a relationship before cleaning

A scatter plot places one observation at its load and target coordinates. x and y name the two columns; ax selects the plotting area.

Look for gaps, unusual points and possible trends. A visible association does not show that load caused the target to change.

## Slide 16: Plot raw load against the target

A scatter plot places one observation at its load and target coordinates. x and y name the two columns; ax selects the plotting area.

Look for gaps, unusual points and possible trends. A visible association does not show that load caused the target to change.

Step-by-step explanation

raw_scatter_figure, raw_scatter_axes = plt.subplots()
raw_scatter_figure stores the result of the displayed expression. raw_scatter_axes stores the result of the displayed expression.

raw_data.plot.scatter(x='load_pct', y='target', ax=raw_scatter_axes)
table.plot.scatter(x="load_pct", y="target", ax=ax) plots one point per row using those two columns. ax selects the plotting area. Rows with missing plot coordinates cannot form complete points.

raw_scatter_axes.set_xlabel('Load (%)')
Evaluate the displayed statement using the values produced by the preceding statements.

raw_scatter_axes.set_ylabel('crusher energy (kWh/t)')
Evaluate the displayed statement using the values produced by the preceding statements.

raw_scatter_axes.set_title('Before cleaning')
Evaluate the displayed statement using the values produced by the preceding statements.

plt.show()
Evaluate the displayed statement using the values produced by the preceding statements.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 17: A missing value is not zero

Read True as yes and False as no. For a whole table isna gives an answer for each cell. sum counts the True answers down each column: True counts as 1 and False as 0. A missing crusher-energy measurement is not evidence that energy consumption was zero.

## Slide 18: Count missing cells in each column

NaN means a value is missing. A measured zero is still a recorded value.

isna() asks “is this cell missing?” It returns True for yes and False for no.

.sum() counts True answers: True counts as 1 and False as 0.

Step-by-step explanation

print(raw_data.isna().sum())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
record_id       0
equipment_id    0
load_pct        0
ambient_c       1
target          1
dtype: int64

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 19: Find a repeated observation

For IDs 1, 2, 1 the answers are False, False, True. We mark the last occurrence because our stated rule keeps the first. The supplied CSV has one later copy of record ID 1. Repeated equipment labels are normal.

## Slide 20: Count repeated record IDs

record_id identifies one observation. equipment_id identifies the equipment and may repeat.

duplicated("record_id") marks later copies True. The first occurrence is False.

Step-by-step explanation

is_repeated_record = raw_data.duplicated('record_id')
is_repeated_record stores the result of the displayed expression.

print(is_repeated_record)
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(is_repeated_record.sum())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
0     False
1     False
2     False
3     False
4     False
      ...  
86    False
87    False
88    False
89    False
90     True
Length: 91, dtype: bool
1

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 21: Remove the later copy; keep the original

Finding and removing are different actions: duplicated answers a question; drop_duplicates returns a table without later copies. Read the next chain left to right. The original raw_data table stays at 91 rows.

## Slide 22: Create the working table

drop_duplicates("record_id") keeps the first occurrence of each record ID.

.copy() makes an independent working table. len(table) counts its rows.

Step-by-step explanation

cleaned_data = raw_data.drop_duplicates('record_id').copy()
cleaned_data stores the result of the displayed expression.

print(len(raw_data))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(len(cleaned_data))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
91
90

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 23: Question 1: is the target recorded?

Target is crusher energy in kWh/t. We cannot use a missing target as an observed outcome. notna means NOT missing, the opposite of isna. A recorded target of zero would count as present. The next example only creates answers; it does not delete rows.

## Slide 24: Look at the values, then their answers

cleaned_data["target"] selects the target column.

.notna() asks whether each value is present. It returns True for a recorded value and False for a missing value.

Step-by-step explanation

target_is_recorded = cleaned_data['target'].notna()
target_is_recorded stores the result of the displayed expression.

print(cleaned_data['target'].head())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(target_is_recorded.head())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
0    14.001
1    15.147
2    13.005
3       NaN
4    12.554
Name: target, dtype: float64
0     True
1     True
2     True
3    False
4     True
Name: target, dtype: bool

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 25: Use the answers to select rows

Distinguish brackets with a quoted column name from brackets with a True/False Series. The first selects a column; the second selects rows. Use answers produced from this same working table so row labels align. Creating the answers and using them to select rows are separate steps.

## Slide 26: Try one condition on its own

cleaned_data[target_is_recorded] keeps rows whose answer is True. Rows answering False are left out of the returned table.

This True/False selection is called a Boolean mask. The variable name does not need to end in _mask.

Step-by-step explanation

rows_with_target = cleaned_data[target_is_recorded].copy()
rows_with_target stores the result of the displayed expression.

print(len(cleaned_data))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(len(rows_with_target))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
90
89

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 27: Question 2: is the load valid?

Read the endpoints as included: 0 and 100 pass; -5 and 101 fail. The supplied file contains load -5 for record ID 9. We reject that observation under this stated cleaning rule rather than silently changing its reading.

## Slide 28: Inspect the load answers

load_pct is a percentage. For this exercise the valid range is 0 through 100, including both endpoints.

.between(0, 100) answers True inside that range and False outside it.

Step-by-step explanation

load_is_valid = cleaned_data['load_pct'].between(0, 100)
load_is_valid stores the result of the displayed expression.

print(cleaned_data['load_pct'].head(10))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(load_is_valid.head(10))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
0    59.15
1    77.46
2    69.60
3    75.98
4    57.62
5    50.12
6    24.66
7    72.92
8    -5.00
9    67.91
Name: load_pct, dtype: float64
0     True
1     True
2     True
3     True
4     True
5     True
6     True
7     True
8    False
9     True
Name: load_pct, dtype: bool

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 29: Keep a row only when both answers are True

Python and is not the operator for combining pandas Series; use &. Both answer columns here come from the same cleaned_data table. Named conditions avoid nesting several expressions on one line. If writing comparisons directly, place each comparison in parentheses.

## Slide 30: Which observations will we keep?

These three record IDs are from the supplied CSV. Record 1 has target 14.001 and load 59.15, so both checks pass. Record 4 has no target, although load 75.98 is valid. Record 9 has target 13.908, but load -5 fails. A row needs BOTH conditions. This is a selected illustration, not the entire 90-row table.

## Slide 31: Combine the answers, then keep those rows



Step-by-step explanation

rows_to_keep = target_is_recorded & load_is_valid
rows_to_keep stores the result of the displayed expression.

print(rows_to_keep.sum())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

cleaned_data = cleaned_data[rows_to_keep].copy()
cleaned_data stores the result of the displayed expression.

print(len(cleaned_data))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
88
88

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 32: Fill only missing ambient temperatures

Compute this after removing invalid observations, so discarded rows do not influence the replacement. For an even count, median averages the two central values. pandas skips missing values for median. We fill ambient temperature only; we do not invent missing targets. round(value, 3) changes the displayed precision, not our saved median. float converts the value to a Python decimal number for display.

## Slide 33: Fill missing ambient temperatures

ambient_c is temperature in °C. .median() finds the middle of the recorded values in the retained rows.

.fillna(value) replaces only missing entries. Assign the result back to the ambient_c column.

Step-by-step explanation

median_ambient_c = cleaned_data['ambient_c'].median()
median_ambient_c stores the result of the displayed expression.

cleaned_data['ambient_c'] = cleaned_data['ambient_c'].fillna(median_ambient_c)
cleaned_data stores the result of the displayed expression.

print(round(float(median_ambient_c), 3))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(cleaned_data.isna().sum())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
26.07
record_id       0
equipment_id    0
load_pct        0
ambient_c       0
target          0
dtype: int64

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 34: Validate the result before interpreting charts

Count original and retained rows. Check duplicate record IDs, missing values and valid loads again.

.all() answers True only when every row passes the condition. A check confirms what the data contain; a table named cleaned_data is not automatically correct.

## Slide 35: Check the cleaned table

Count original and retained rows. Check duplicate record IDs, missing values and valid loads again.

.all() answers True only when every row passes the condition. A check confirms what the data contain; a table named cleaned_data is not automatically correct.

Step-by-step explanation

print('Rows before:', len(raw_data))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print('Rows after:', len(cleaned_data))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print('Duplicate IDs:', cleaned_data.duplicated('record_id').sum())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(cleaned_data.isna().sum())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print('Loads valid:', cleaned_data['load_pct'].between(0, 100).all())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
Rows before: 91
Rows after: 88
Duplicate IDs: 0
record_id       0
equipment_id    0
load_pct        0
ambient_c       0
target          0
dtype: int64
Loads valid: True

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 36: Summaries and grouped results

A group mean describes observations in this file. It does not prove that equipment identity causes the difference.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 37: Operations for the next example

Mean of recorded values
series.mean() adds known values and divides by their count. pandas skips missing values by default. The result has the same unit as the original column.

Several summaries at once
series.agg(["mean", "min", "max"]) applies those three named calculations and returns a labelled Series of results. min and max give the lowest and highest recorded values.

Grouping rows
table.groupby("label")["value"] groups the value column by matching labels. Apply mean() or sum() to calculate one result per group. Missing group labels are excluded by default.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 38: Summaries of the cleaned CSV

Mean of recorded values: series.mean() adds known values and divides by their count. pandas skips missing values by default. The result has the same unit as the original column.

Several summaries at once: series.agg(["mean", "min", "max"]) applies those three named calculations and returns a labelled Series of results. min and max give the lowest and highest recorded values.

Grouping rows: table.groupby("label")["value"] groups the value column by matching labels. Apply mean() or sum() to calculate one result per group. Missing group labels are excluded by default.

Step-by-step explanation

target_summary = cleaned_data['target'].agg(['mean', 'min', 'max'])
target_summary stores the result of the displayed expression.

mean_target_by_equipment = cleaned_data.groupby('equipment_id')['target'].mean()
mean_target_by_equipment stores the result of the displayed expression.

print(target_summary)
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(mean_target_by_equipment.round(3))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
mean    12.073682
min      6.625000
max     17.295000
Name: target, dtype: float64
equipment_id
E1    12.251
E2    12.504
E3    12.131
E4    13.248
E5    10.651
E6    11.740
Name: target, dtype: float64

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 39: Choosing a chart for the question

Choosing a chart for the question
Explanation to give
Choose the chart from the question. A bar chart compares named categories; a histogram counts numerical observations in intervals; a scatter plot compares paired numbers. Explain what one mark means.

Worked illustration / lecturer answer
Use bars for mean energy by building, a histogram for the distribution of individual energy readings, and scatter for energy against temperature. A histogram bar's height counts observations in a bin.

Misconception to address
Histogram bins are numerical intervals, not separate named buildings. Changing bin widths can change the visible pattern, so state the choice and inspect the data too.

On this slide
This week uses histograms, scatter plots and bar charts. The other chart types are reference examples.

## Slide 40: Charts and units

The scatter uses the supplied load_pct and target. Equipment grouping is categorical. Use ten histogram bins as required by the project.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 41: Operations for the next example

Draw attention to the two sides of ax=scatter_axes. ax is a parameter name defined by pandas; scatter_axes is our descriptive Python variable. Despite the plural name, one Axes object holds one plot here. The conventional plt alias refers to matplotlib.pyplot. Each new plt.subplots() call creates a separate image and plotting area.

## Slide 42: Load and crusher energy demand

plt.subplots() returns two objects: a figure (the whole image) and axes (the plotting area). Store them as scatter_figure and scatter_axes.

The ax= argument tells pandas where to draw: ax=scatter_axes uses that plotting area. Keep the library keyword ax unchanged.

Step-by-step explanation

import matplotlib.pyplot as plt
Load the named tools. Importing a model class does not train a model.

scatter_figure, scatter_axes = plt.subplots()
scatter_figure stores the result of the displayed expression. scatter_axes stores the result of the displayed expression.

cleaned_data.plot.scatter(x='load_pct', y='target', ax=scatter_axes)
table.plot.scatter(x="load_pct", y="target", ax=ax) plots one point per row using those two columns. ax selects the plotting area. Rows with missing plot coordinates cannot form complete points.

scatter_axes.set_xlabel('Load (%)')
Evaluate the displayed statement using the values produced by the preceding statements.

scatter_axes.set_ylabel('Crusher energy (kWh/t)')
Evaluate the displayed statement using the values produced by the preceding statements.

plt.show()
Evaluate the displayed statement using the values produced by the preceding statements.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 43: Operations for the next example

A bar for each labelled value
series.plot.bar(ax=ax) draws a bar for each Series label. When the Series contains group means, bar heights represent those means.

Histogram intervals
series.plot.hist(bins=10, ax=ax) groups known values into ten value intervals and counts observations in each. Bar heights are counts, not the original measurement values.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 44: Mean crusher energy for each equipment group

A bar for each labelled value: series.plot.bar(ax=ax) draws a bar for each Series label. When the Series contains group means, bar heights represent those means.

Histogram intervals: series.plot.hist(bins=10, ax=ax) groups known values into ten value intervals and counts observations in each. Bar heights are counts, not the original measurement values.

Step-by-step explanation

bar_figure, bar_axes = plt.subplots()
bar_figure stores the result of the displayed expression. bar_axes stores the result of the displayed expression.

mean_target_by_equipment.plot.bar(ax=bar_axes)
series.plot.bar(ax=ax) draws a bar for each Series label. When the Series contains group means, bar heights represent those means.

bar_axes.set_xlabel('Equipment ID')
Evaluate the displayed statement using the values produced by the preceding statements.

bar_axes.set_ylabel('Mean crusher energy (kWh/t)')
Evaluate the displayed statement using the values produced by the preceding statements.

plt.show()
Evaluate the displayed statement using the values produced by the preceding statements.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 45: Distribution of crusher energy readings



Step-by-step explanation

histogram_figure, histogram_axes = plt.subplots()
histogram_figure stores the result of the displayed expression. histogram_axes stores the result of the displayed expression.

cleaned_data['target'].plot.hist(bins=10, ax=histogram_axes)
series.plot.hist(bins=10, ax=ax) groups known values into ten value intervals and counts observations in each. Bar heights are counts, not the original measurement values.

histogram_axes.set_xlabel('Crusher energy (kWh/t)')
Evaluate the displayed statement using the values produced by the preceding statements.

histogram_axes.set_ylabel('Observation count')
Evaluate the displayed statement using the values produced by the preceding statements.

plt.show()
Evaluate the displayed statement using the values produced by the preceding statements.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 46: Optional extension: check numeric text

This extension is ungraded and is not required to complete today’s core practice. The supplied CSV has no invalid numeric text; the expected conversion-failure count is zero. Reuse raw_data to inspect the original entries.

## Slide 47: Operations for the next example

Converting numeric text
pd.to_numeric(column, errors="coerce") converts numeric values or text. Unparseable text becomes missing. Compare original and converted values so existing gaps are not counted as conversion failures.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 48: Check numeric conversion of ambient temperature

Converting numeric text: pd.to_numeric(column, errors="coerce") converts numeric values or text. Unparseable text becomes missing. Compare original and converted values so existing gaps are not counted as conversion failures.

Step-by-step explanation

ambient_numbers = pd.to_numeric(raw_data['ambient_c'], errors='coerce')
ambient_numbers stores the result of the displayed expression.

value_was_recorded = raw_data['ambient_c'].notna()
value_was_recorded stores the result of the displayed expression.

conversion_failed = value_was_recorded & ambient_numbers.isna()
conversion_failed stores the result of the displayed expression.

print(int(conversion_failed.sum()))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(raw_data[conversion_failed].head())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
0
Empty DataFrame
Columns: [record_id, equipment_id, load_pct, ambient_c, target]
Index: []

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 49: Optional extension: put steps in a function

Explain parameters as inputs and return as the result passed back to the caller. records is a list of row dictionaries. pd.DataFrame turns those rows into a labelled table. Learners can revisit this after understanding the cleaning workflow.

## Slide 50: Operations for the next example

Returning a dictionary
series.to_dict() maps Series labels to values. table.to_dict("records") instead returns a list of row dictionaries. Choose the form specified in the example.

A table from Python values
pd.DataFrame(records) builds a table from row dictionaries. With a dictionary of column lists, keys become column names and each list supplies that column’s values.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 51: A function called with the supplied records

Returning a dictionary: series.to_dict() maps Series labels to values. table.to_dict("records") instead returns a list of row dictionaries. Choose the form specified in the example.

A table from Python values: pd.DataFrame(records) builds a table from row dictionaries. With a dictionary of column lists, keys become column names and each list supplies that column’s values.

Step-by-step explanation

def mean_load_by_equipment(equipment_records):
    equipment_data = pd.DataFrame(equipment_records)
    mean_load_by_group = equipment_data.groupby('equipment_id')['load_pct'].mean()
    return mean_load_by_group.to_dict()
Define the function. Explain each input before the call. Its body runs only when called; return supplies the computed value.

raw_records = raw_data.to_dict('records')
raw_records stores the result of the displayed expression.

print(mean_load_by_equipment(raw_records))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
{'E1': 54.9475, 'E2': 61.326, 'E3': 53.46933333333333, 'E4': 66.854, 'E5': 48.10133333333333, 'E6': 51.54}

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 52: Ungraded cleaning practice

Open guided_practice.ipynb, then upload engineering_data.csv through Colab Files. Run the loading cell and confirm the expected column names. Learners follow this notebook during class; no separate A6 notebook is required.
A6 and Quiz 6 are waived for this cohort. This is ungraded practical revision. No assignment upload or quiz response is required. Previous submissions remain on record but do not count towards coursework marks.

## Slide 53: Explain your cleaning choices

Ask learners to identify one duplicated record ID and one missing value in the displayed data. Their explanation should name the column, state the chosen action and distinguish a measured value from an estimate. This is a short revision note, not a submitted report.
A6 and Quiz 6 are waived for this cohort. This is ungraded practical revision. No assignment upload or quiz response is required. Previous submissions remain on record but do not count towards coursework marks.

## Slide 54: Save your practice notebook

Use File > Save in Google Drive. Ask learners to check the notebook name in Drive and reopen it. A saved practice notebook is for their revision; the closed A6 form does not indicate unfinished work.
A6 and Quiz 6 are waived for this cohort. This is ungraded practical revision. No assignment upload or quiz response is required. Previous submissions remain on record but do not count towards coursework marks.

## Slide 55: Check your understanding

Expected answers: a missing value means no observation was recorded; zero is an actual numeric value. Keeping the raw CSV lets us repeat the analysis and check what was changed. If a learner confuses blank and zero, compare an unrecorded temperature with a measured 0 degrees C.
A6 and Quiz 6 are waived for this cohort. This is ungraded practical revision. No assignment upload or quiz response is required. Previous submissions remain on record but do not count towards coursework marks.

## Slide 56: Practical revision checklist

Restart the session and run from the first cell. If the CSV is missing, upload it again. Check that axes show the quantity and unit. Then switch to a NEW notebook and the cohort Test1_practice.csv for the Week 7 examples; do not mix its column names with the Week 6 file.
A6 and Quiz 6 are waived for this cohort. This is ungraded practical revision. No assignment upload or quiz response is required. Previous submissions remain on record but do not count towards coursework marks.