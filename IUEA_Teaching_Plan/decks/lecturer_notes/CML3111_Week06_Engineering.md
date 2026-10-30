# CML3111 Week 6

Each slide shows its text, then the spoken script the lecturer reads aloud.

## Slide 1: Cleaning data and explaining changes

Communications, Electrical, Mechatronics and Robotics Engineering

Friday 16 October 2026
Friday 11:00–14:00, Room 115

**Spoken script**

Welcome to week six for CML3111, which serves Communications, Electrical, Mechatronics and Robotics Engineering.

This week we work with data that has problems in it. Real records often have blanks, repeated rows and values that cannot be right. We learn to find these problems, fix them with clear rules, and then explain every change we made.

By the end of the session we will have a clean table, a few summaries and three charts, and we will be able to say why each step was taken.

## Slide 2: Today: inspect, clean, check and plot

First inspect the original CSV. Then apply the cleaning rules, check the result, and explain the cleaned charts.

This walkthrough supports the existing Week 6 assignment and quiz. Their requirements are unchanged.

**Spoken script**

Today we follow one path from start to finish. First we inspect the original file, which means we look at it carefully before changing anything. Then we apply cleaning rules, which are short sentences that say which rows to remove and which blanks to fill. After that we check the result to confirm the rules did what we expected. Finally we draw charts and explain what they show.

This walkthrough supports the assignment and the quiz that already exist for week six. Their requirements have not changed. Everything we do today is practice for them.

## Slide 3: The supplied file

Extract this week’s student ZIP. Upload engineering_data.csv into Colab using the Files panel, or keep it beside the notebook locally.

The examples below read this file. Run the cells in slide order. Keep the original CSV unchanged.

**Spoken script**

Every example today reads one file called engineering underscore data dot csv. A CSV file is a plain text table where each line is a row and commas separate the columns.

Extract this week's student ZIP file first. A ZIP file is a folder packed into one file, so we unpack it to get at what is inside. Then upload engineering underscore data dot csv into Colab using the Files panel. If you work on your own computer, keep the file in the same folder as your notebook.

Uploading a notebook does not upload its data, so check that the file name is spelled exactly right. Run the cells in the same order as the slides, and keep the original file unchanged. Each cohort has its own data, so your numbers can differ from a classmate in another programme.

## Slide 4: Operations for the next example

01

Import and short names: import pandas as pd loads pandas and gives it the short name pd. pd.read_csv refers to a function in that library.

02

Reading a CSV: pd.read_csv("filename.csv") reads the named file into a DataFrame: a table with labelled columns and row labels. The file must exist in the working folder.

03

Counting dimensions: table.shape gives (number of rows, number of columns). shape is a property, so it has no parentheses.

**Spoken script**

Three small tools come first.

The first line is import pandas as pd. Pandas is a library, which means a collection of ready-made tools written by other people. Import loads it, and as pd gives it the short name pd so we type less. When we later write pd dot read underscore csv, we are using the read underscore csv tool from that library.

The second tool reads a file. We write pd dot read underscore csv and put the file name in quotes inside the brackets. It returns a DataFrame, which is a table with named columns and a label for each row. The file must be in the working folder, the place where the notebook is running.

The third tool counts the table. Writing table dot shape gives two numbers, the number of rows and then the number of columns. Shape has no brackets after it, because it is a stored fact about the table and nothing needs to be calculated.

## Slide 5: Operations for the next example

Column data types: table.dtypes reports each column’s stored type. int64 means integers, float64 means decimal numbers, and object often contains text. Numeric blanks commonly appear as NaN.

A preview of rows: table.head() returns the first five rows. It leaves the table unchanged. A preview is not the entire dataset.

**Spoken script**

Two more tools help us look at a table.

The first is table dot dtypes. A dtype is the kind of value a column stores. The value int sixty-four means whole numbers. The value float sixty-four means numbers with a decimal part. The value object usually means text. Blank cells in a numeric column usually show up as NaN, which stands for not a number and simply means the value is missing.

The second is table dot head with empty brackets. It shows the first five rows. Showing rows does not change the table in any way. But five rows is only a small preview, so it does not tell us what the whole file contains.

We use dtypes to check that each column holds the kind of value we expect, and head to see what a few real rows look like.

## Slide 6: Two names for two tables

raw_data: the original table read from the CSV.

cleaned_data: a separate working table that we will change.

**Spoken script**

We will keep two tables with two different names.

The first is raw underscore data. This is the original table exactly as it came from the CSV file. We never change it. If anyone asks what was originally recorded, raw underscore data gives the answer.

The second is cleaned underscore data. This is a separate working table, and it is the one we change step by step.

These names are labels that we chose ourselves. Python gives them no special meaning. We use two names because we need to tell the two tables apart. If we called both of them data, we could lose track of which one still holds the original records and could no longer show what we changed.

## Slide 7: Loading the supplied observations

Import pandas using its conventional alias pd.

Run this example on the supplied engineering_data.csv.

```python
import pandas as pd
raw_data = pd.read_csv("engineering_data.csv")
print(raw_data.head())
print(raw_data.shape)
print(raw_data.dtypes)
```

**Spoken script**

We load the file and take a first look. The code has four lines after the import.

The first line is import pandas as pd, which brings in the pandas library under the short name pd.

The second line is raw underscore data equals pd dot read underscore csv, with the file name in brackets. It reads the CSV file and stores the table under the name raw underscore data.

The third line prints raw underscore data dot head, which displays the first five rows. The fourth prints raw underscore data dot shape, which shows the number of rows and then the number of columns. The fifth prints raw underscore data dot dtypes, which shows the kind of value in each column.

We read the output in that order. The preview shows the columns record underscore id, equipment underscore id, load underscore pct, ambient underscore c and target. The shape tells us how big the table is, and the dtypes tell us which columns are numbers and which are text. Run this on your own copy of the file.

## Slide 8: EDA: understand the original observations

EDA means exploratory data analysis: inspect what the columns mean, their types, missing values, ranges and patterns before choosing cleaning actions.

record_id identifies an observation; equipment_id identifies its source. load_pct is %, ambient_c is °C, and target is motor temperature (°C).

**Spoken script**

EDA stands for exploratory data analysis. That is a formal name for looking carefully at data before we decide what to do with it. We check what each column means, what type it holds, where values are missing, what range the numbers cover and whether any patterns appear.

In this file, record underscore id identifies one observation. Think of it as a ticket number for a single reading. Equipment underscore id tells us which machine the reading came from, so the same equipment can appear many times. Load underscore pct is the load in percent. Ambient underscore c is the surrounding temperature in degrees Celsius. The column called target is motor temperature, also in degrees Celsius.

This step comes first because the cleaning rules we write later depend on knowing what each column should look like.

## Slide 9: Check types and recorded values

table.info() prints column types and non-missing counts. Call it directly; do not wrap it in print.

table[numeric_columns].describe() summarises selected numeric measurements: count, mean, standard deviation, minimum, quartiles and maximum.

**Spoken script**

Two tools give us a fuller picture of a table.

The first is table dot info with empty brackets. It prints each column's type and how many values in that column are present. We call it directly. We do not wrap it in print, because it already prints its report by itself.

The second is table, then square brackets containing a list of numeric column names, then dot describe. This summarises only the columns we named. For each one it reports the count of recorded values, the mean, the standard deviation, the minimum, the quartiles and the maximum.

The mean is the average. The standard deviation tells us how spread out the values are. Quartiles split the sorted values into four equal parts. The fifty percent line is the median, the middle value.

We describe the measurements only. An identifier such as record underscore id is a label, so averaging it would mean nothing. A minimum below zero in a percentage column is a flag telling us to investigate.

## Slide 10: Inspect structure and numerical ranges

Compare count with the original row count. Read min and max before deciding whether a value violates the stated rule.

Run after the preceding example using the supplied CSV.

```python
raw_data.info()
numeric_columns = ["load_pct", "ambient_c", "target"]
print(raw_data[numeric_columns].describe())
```

**Spoken script**

We run info and describe on the original table.

The first line is raw underscore data dot info with empty brackets. It lists every column with its type and the number of values present.

The second line creates a list called numeric underscore columns. The list holds three column names in quotes, load underscore pct, ambient underscore c and target. Those are the measurements.

The third line prints raw underscore data, then square brackets holding that list, then dot describe. That gives count, mean, standard deviation, minimum, quartiles and maximum for those three columns.

The first thing to check is the count. Compare it with the total number of rows. If a column has fewer values than there are rows, some cells are blank. Then read the minimum and maximum of each column. We decide whether a value breaks a rule only after we have seen the real range. Run this after the previous example, using your own copy of the file.

## Slide 11: Check which equipment is represented

value_counts() counts rows for each label. dropna=False also shows missing labels.

Counts can reveal missing groups or unequal coverage. Repeated equipment IDs are expected; repeated record IDs need separate inspection.

**Spoken script**

We now ask which equipment appears in the data and how often.

The tool is value underscore counts with empty brackets. It looks at one column and counts how many rows carry each label. If we add dropna equals False inside the brackets, it also counts blank labels, so a missing label shows up as its own line instead of silently disappearing.

Counts like these can reveal problems. One piece of equipment might be missing entirely, or some might have far fewer observations than others.

We should expect equipment labels to repeat. One machine gives many readings, so the same label appears on many rows. A repeated record underscore id is different. Each record underscore id is meant to name exactly one observation, so a repeat there needs a closer look, and we handle that next.

## Slide 12: Count observations per equipment

These are observation counts, not counts of distinct machines. The later duplicate row is still present in this raw-data summary.

Run after the preceding example using the supplied CSV.

```python
equipment_counts = raw_data["equipment_id"].value_counts(
    dropna=False)
print(equipment_counts)
```

**Spoken script**

We count the rows for each piece of equipment.

The first line takes the equipment underscore id column of raw underscore data and calls value underscore counts on it, with dropna equals False. The result is stored under the name equipment underscore counts. The second line prints it.

The output is a list. Each line shows an equipment label and the number of rows carrying that label. Read it to see which equipment is present and whether the counts are roughly balanced.

These are counts of observations. They do not tell us how many distinct machines exist. One machine can contribute many rows. This summary also still contains the later repeated row, because we have not removed anything yet. Run this on your own copy of the file.

## Slide 13: Preview the raw distribution

A histogram groups numeric values into intervals and counts observations in each interval. bins=10 requests ten intervals.

plt.subplots() gives a figure and its axes. ax selects where the chart is drawn. Missing numeric values are omitted from the plot.

**Spoken script**

Before cleaning, we draw one chart of the target column. It is called a histogram.

A histogram groups numeric values into intervals and counts how many observations fall into each interval. The word bins means those intervals. Writing bins equals ten asks for ten of them. The height of each bar is a count of observations.

To draw a chart we call plt dot subplots with empty brackets. It gives us two things. The first is a figure, which is the whole image. The second is the axes, which is the area inside the image where the chart is drawn. We pass the axes to the plot using ax equals, which tells pandas where to draw.

Missing values cannot be placed on the chart, so the histogram leaves them out. We read the horizontal direction as the target measurement and the vertical direction as how many observations fall there. An extreme value is a reason to investigate. It is no reason to delete the row straight away.

## Slide 14: Plot the target before cleaning

The chart includes all recorded targets, including observations that may later be removed. Compare with the cleaned distribution at the end; do not infer causation from shape.

Run after the preceding example using the supplied CSV.

```python
import matplotlib.pyplot as plt
raw_figure, raw_axes = plt.subplots()
raw_data["target"].plot.hist(bins=10, ax=raw_axes)
raw_axes.set_xlabel("motor temperature (°C)")
raw_axes.set_ylabel("Observation count")
raw_axes.set_title("Before cleaning")
plt.show()
```

**Spoken script**

We draw the target histogram on the original, uncleaned table.

The first line imports matplotlib dot pyplot as plt. Matplotlib is the plotting library, and plt is its short name.

The second line calls plt dot subplots and stores the two results as raw underscore figure and raw underscore axes. The figure is the whole image and the axes is the drawing area.

The third line takes the target column of raw underscore data and calls plot dot hist with bins equals ten and ax equals raw underscore axes. That draws a histogram with ten intervals inside our drawing area.

The next three lines set the horizontal label to motor temperature in degrees Celsius, the vertical label to observation count, and the title to before cleaning. The last line, plt dot show, displays the chart.

This chart includes every recorded target, even rows we may remove later. At the end we compare it with the cleaned version. We describe the shape we see. We should not claim it shows a cause.

## Slide 15: Inspect a relationship before cleaning

A scatter plot places one observation at its load and target coordinates. x and y name the two columns; ax selects the plotting area.

Look for gaps, unusual points and possible trends. A visible association does not show that load caused the target to change.

**Spoken script**

Next we look at how two columns relate, using a scatter plot.

A scatter plot draws one dot for each row. The dot sits at the position given by two numbers from that row. Here the horizontal position is the load and the vertical position is the target.

In the code, x equals and y equals name the two columns we want. As before, ax equals tells pandas which drawing area to use.

When we read a scatter plot, we look for gaps, unusual dots far from the others, and any general direction in which the dots seem to drift. If higher loads tend to sit with higher targets, we can say the two move together in this file.

That is an association, which means a pattern of moving together. It does not show that load caused the target to change. Other factors might be involved, and a chart alone cannot tell us.

## Slide 16: Plot raw load against the target

A point at load -5 is visible because these are uncleaned rows. Missing target values cannot be plotted. Later compare the cleaned scatter plot after applying the stated rules.

Run after the preceding example using the supplied CSV.

```python
raw_scatter_figure, raw_scatter_axes = plt.subplots()
raw_data.plot.scatter(x="load_pct", y="target", ax=raw_scatter_axes)
raw_scatter_axes.set_xlabel("Load (%)")
raw_scatter_axes.set_ylabel("motor temperature (°C)")
raw_scatter_axes.set_title("Before cleaning")
plt.show()
```

**Spoken script**

We draw the scatter plot with the original rows.

The first line creates a new figure and drawing area, named raw underscore scatter underscore figure and raw underscore scatter underscore axes.

The second line calls plot dot scatter on raw underscore data, with x equals the load underscore pct column and y equals the target column, drawing into our axes.

The next three lines label the horizontal direction load in percent, label the vertical direction motor temperature in degrees Celsius, and give the title before cleaning. Then plt dot show displays the chart.

Look for the point at a load of minus five. It appears because we have not cleaned anything. A load of minus five percent cannot be a real reading. Rows with a missing target cannot appear at all, because a dot needs both numbers. After we apply our rules, we draw the same chart again and compare. Run this after the previous example.

## Slide 17: A missing value is not zero

01

NaN means a value is missing. A measured zero is still a recorded value.

02

isna() asks “is this cell missing?” It returns True for yes and False for no.

03

.sum() counts True answers: True counts as 1 and False as 0.

**Spoken script**

Three ideas help us handle blanks.

First, NaN means a value is missing. It stands for not a number. A measured zero is a real recorded value, and a blank is a cell where nothing was recorded. If a sensor was off and logged nothing, we cannot say the energy used was zero.

Second, the tool isna with empty brackets asks a question of every cell, namely is this cell missing. The answer is True for yes and False for no.

Third, dot sum counts the True answers. It treats True as one and False as zero, so adding them up gives the number of missing cells. For a whole table, isna gives an answer for each cell, and sum then counts them down each column.

So isna followed by sum gives us the number of blanks in every column in one step.

## Slide 18: Count missing cells in each column

Use the supplied engineering_data.csv. Run cells in order.

```python
print(raw_data.isna().sum())
```

**Spoken script**

We count the blanks in each column of the original table.

There is a single line. It writes print, then raw underscore data dot isna with empty brackets, then dot sum with empty brackets.

We read it from the inside out. Isna turns the table into a grid of True and False answers, with True wherever a cell is missing. Sum then adds those answers down each column, so we get one number per column.

The output lists each column name followed by its count of missing cells. A zero means that column has no blanks. A larger number tells us how many cells we must decide about. That decides which columns need a rule later.

Use your own copy of the file, and run the cells in order.

## Slide 19: Find a repeated observation

record_id identifies one observation. equipment_id identifies the equipment and may repeat.

duplicated("record_id") marks later copies True. The first occurrence is False.

**Spoken script**

Now we look for repeated observations.

The column record underscore id is meant to identify one observation. Equipment underscore id names the equipment and is allowed to repeat. So we search for repeats in record underscore id.

The tool is duplicated, and we put the column name in quotes inside the brackets. It goes down the column and marks each later copy of an ID as True. The first time an ID appears, it is marked False.

For example, take the IDs one, two, one. The answers are False, False, True. The second one is marked because it is a later copy.

Our rule keeps the first occurrence, so the later copy is the one we remove. The supplied file has one later copy of record ID one. Repeated equipment labels are normal and are not a problem.

## Slide 20: Count repeated record IDs

Read each input before running.

Use the supplied engineering_data.csv. Run cells in order.

```python
is_repeated_record = raw_data.duplicated("record_id")
print(is_repeated_record)
print(is_repeated_record.sum())
```

**Spoken script**

We now find and count the repeated record IDs.

The first line is is underscore repeated underscore record equals raw underscore data dot duplicated, with record underscore id in quotes. It stores a column of True and False answers, one for each row.

The second line prints that column. We see an answer for every row, and we look for any True.

The third line prints is underscore repeated underscore record dot sum. Because True counts as one, the sum is the number of later copies.

The printed total tells us how many rows would be removed if we dropped repeats. Read each input before running, and use your own copy of the file. Run the cells in order.

## Slide 21: Remove the later copy; keep the original

drop_duplicates("record_id") keeps the first occurrence of each record ID.

.copy() makes an independent working table. len(table) counts its rows.

**Spoken script**

Finding a repeat and removing it are two different actions. Duplicated answers a question. Drop underscore duplicates takes action.

We write drop underscore duplicates with record underscore id in quotes inside the brackets. It returns a table without the later copies. It keeps the first occurrence of each record ID.

We add dot copy with empty brackets after it. Copy makes an independent working table, so changes we make later cannot affect any other table.

We also want to count rows. The function len, which is short for length, gives the number of rows in a table.

This step builds our working table from the raw one. The original raw underscore data stays untouched, so it still has all of its rows.

## Slide 22: Create the working table

Read each input before running.

Use the supplied engineering_data.csv. Run cells in order.

```python
cleaned_data = raw_data.drop_duplicates("record_id").copy()
print(len(raw_data))
print(len(cleaned_data))
```

**Spoken script**

We create the working table.

The first line is cleaned underscore data equals raw underscore data dot drop underscore duplicates, with record underscore id in quotes, followed by dot copy. Reading it left to right, we take the raw table, drop any later repeat of a record ID, and copy the result into a new table named cleaned underscore data.

The second line prints len of raw underscore data, the number of rows in the original. The third prints len of cleaned underscore data, the number of rows in the working table.

We compare the two numbers. The working table should have fewer rows by exactly the number of later copies we found earlier. The raw table has not changed, which is why we kept two names. Read each input before running, and use your own copy of the file.

## Slide 23: Question 1: is the target recorded?

cleaned_data["target"] selects the target column.

.notna() asks whether each value is present. It returns True for a recorded value and False for a missing value.

**Spoken script**

Our first cleaning question is whether each row has a recorded target. The target is motor temperature in degrees Celsius. If it is missing, we cannot use that row as an observed outcome.

We write cleaned underscore data, then target in quotes inside square brackets. That selects the target column.

Then we add dot notna with empty brackets. Notna asks whether each value is present. It is the opposite of isna. It returns True for a recorded value and False for a missing one. A recorded target of zero counts as present, because zero is a real value.

The next example only creates the answers. It does not delete any rows yet. Deleting is a separate step.

## Slide 24: Look at the values, then their answers

Read each input before running.

Use the supplied engineering_data.csv. Run cells in order.

```python
target_is_recorded = cleaned_data["target"].notna()
print(cleaned_data["target"].head())
print(target_is_recorded.head())
```

**Spoken script**

We look at the target values and then at the answers about them.

The first line is target underscore is underscore recorded equals cleaned underscore data, target in quotes in square brackets, dot notna. This stores one True or False answer for each row.

The second line prints the first five target values, using dot head. The third prints the first five answers.

We read the two outputs side by side. Wherever a target value shows NaN, the answer beside it is False. Wherever there is a number, the answer is True. This check shows us that the answers match what we see in the data.

Read each input before running, and use your own copy of the file.

## Slide 25: Use the answers to select rows

cleaned_data[target_is_recorded] keeps rows whose answer is True. Rows answering False are left out of the returned table.

This True/False selection is called a Boolean mask. The variable name does not need to end in _mask.

**Spoken script**

Now we use the True and False answers to choose rows.

We write cleaned underscore data, then square brackets containing target underscore is underscore recorded. This keeps the rows whose answer is True. Rows whose answer is False are left out of the table that comes back.

A column of True and False answers used like this is called a Boolean mask. Boolean is the word for a value that can only be True or False. Think of a mask with holes. The rows lying under True holes show through and the rest are covered up. The variable name does not need to end in underscore mask.

Notice there are two uses of square brackets. When we put a quoted column name inside them, we select a column. When we put a column of True and False answers inside them, we select rows. We make the answers from the same table we select from, so the row labels line up. Creating the answers and using them are two separate steps.

## Slide 26: Try one condition on its own

Read each input before running.

Use the supplied engineering_data.csv. Run cells in order.

```python
rows_with_target = cleaned_data[target_is_recorded].copy()
print(len(cleaned_data))
print(len(rows_with_target))
```

**Spoken script**

We try the target condition by itself.

The first line is rows underscore with underscore target equals cleaned underscore data, then target underscore is underscore recorded in square brackets, then dot copy. That keeps only the rows with a recorded target and stores them as a new table.

The second line prints the number of rows in cleaned underscore data before the selection. The third prints the number of rows in rows underscore with underscore target.

The second number should be smaller by the count of missing targets. That confirms the mask removed exactly the rows we meant it to remove.

We have not changed cleaned underscore data itself here. We made a separate table so we could see the effect of one rule alone. Read each input before running, and use your own copy of the file.

## Slide 27: Question 2: is the load valid?

load_pct is a percentage. For this exercise the valid range is 0 through 100, including both endpoints.

.between(0, 100) answers True inside that range and False outside it.

**Spoken script**

Our second question is whether the load is valid. Load underscore pct is a percentage, and for this exercise the valid range is zero through one hundred, including both endpoints. So zero passes and one hundred passes. Minus five fails, and so would one hundred and one.

The tool is between, and we give it the two endpoints inside the brackets, zero and one hundred. Between returns True for every value inside that range, endpoints included, and False for every value outside.

The supplied file contains a load of minus five for record ID nine. That is impossible for a percentage load. Under our stated rule we reject that observation. We do not quietly change the reading to something that looks plausible, because we have no way of knowing what the true value was.

## Slide 28: Inspect the load answers

Read each input before running.

Use the supplied engineering_data.csv. Run cells in order.

```python
load_is_valid = cleaned_data["load_pct"].between(0, 100)
print(cleaned_data["load_pct"].head(10))
print(load_is_valid.head(10))
```

**Spoken script**

We create the load answers and look at them next to the values.

The first line is load underscore is underscore valid equals cleaned underscore data, load underscore pct in square brackets, dot between with zero and one hundred. It stores a True or False answer for each row.

The second line prints the first ten load values, using head with ten inside the brackets. The third prints the first ten answers.

We read the two lists together. Every load inside the range zero to one hundred has True beside it. Any load outside it has False beside it. In the output the minus five is easy to spot, with a False next to it.

This lets us confirm that the rule works on real rows before we use it to remove anything. Read each input before running, and use your own copy of the file.

## Slide 29: Keep a row only when both answers are True

01

& means “and” for two True/False columns.

02

True & True → True. Any pair containing False → False.

03

Our rule: a recorded target AND a valid load.

**Spoken script**

We want rows that pass both checks, so we need a way to combine two columns of True and False answers.

The symbol is the ampersand, which reads as and. Placed between two True and False columns, it gives True only when both answers are True. True and True gives True. Any pair containing a False gives False.

For pandas columns we must use this symbol. The plain Python word and does not work on whole columns.

Our rule for keeping a row is that it has a recorded target and a valid load. We have already stored each condition under its own name, which keeps the line short and easy to read. If you write the comparisons directly instead, put each one in brackets.

## Slide 30: Which observations will we keep?

A row stays only when both checks pass. These records come from the supplied CSV.

**Spoken script**

Here we test the rule on three records taken from the supplied file.

A row stays only when both checks pass.

Record one has a recorded target and a load of fifty-nine point one five percent. Both checks pass, so it stays.

Record four has a valid load of seventy-five point nine eight percent, but its target is blank. The target check fails, so the row goes.

Record nine has a recorded target, but its load is minus five percent. The load check fails, so the row goes too.

These are three chosen examples, and the full table has many more rows. The rule is the same for all of them. A row needs both conditions to be True before it is kept.

## Slide 31: Combine the answers, then keep those rows

Read each input before running.

Use the supplied engineering_data.csv. Run cells in order.

```python
rows_to_keep = target_is_recorded & load_is_valid
print(rows_to_keep.sum())
cleaned_data = cleaned_data[rows_to_keep].copy()
print(len(cleaned_data))
```

**Spoken script**

We combine the two answers and keep the matching rows.

The first line is rows underscore to underscore keep equals target underscore is underscore recorded, an ampersand, then load underscore is underscore valid. The result is True only for rows that pass both checks.

The second line prints rows underscore to underscore keep dot sum. Since True counts as one, this is the number of rows we are about to keep.

The third line is cleaned underscore data equals cleaned underscore data, then rows underscore to underscore keep in square brackets, then dot copy. That replaces the working table with only the kept rows.

The fourth line prints the number of rows now in the working table. It matches the count we printed a moment ago, and that agreement confirms the selection worked. Read each input before running, and use your own copy of the file.

## Slide 32: Fill only missing ambient temperatures

ambient_c is temperature in °C. .median() finds the middle of the recorded values in the retained rows.

.fillna(value) replaces only missing entries. Assign the result back to the ambient_c column.

**Spoken script**

One blank remains to handle, in the ambient temperature column. Ambient underscore c is the surrounding temperature in degrees Celsius.

We fill it with the median. The median is the middle of the recorded values after sorting them from smallest to largest. If there is an even number of values, it is the average of the two middle ones. Pandas skips missing values when it works out the median.

We compute the median after removing the invalid rows. That way, rows we threw away have no influence on the number we fill in.

The tool fillna with a value in the brackets replaces only the missing entries and leaves every recorded value alone. We assign the result back to the ambient underscore c column.

We fill only ambient temperature. We do not invent missing targets. The filled numbers are estimates, so we must say so when we report our work.

## Slide 33: Fill missing ambient temperatures

Calculate the median using the retained rows only.

Run this example on the supplied engineering_data.csv.

```python
median_ambient_c = cleaned_data["ambient_c"].median()
cleaned_data["ambient_c"] = (
    cleaned_data["ambient_c"].fillna(median_ambient_c))
print(round(float(median_ambient_c), 3))
print(cleaned_data.isna().sum())
```

**Spoken script**

We fill the blank ambient temperatures with the median.

The first line takes the ambient underscore c column of cleaned underscore data and calls dot median. The result is stored as median underscore ambient underscore c. We compute it on the retained rows only.

The second statement replaces the column. On the right side we take the same column and call fillna with the median in brackets. Any blank gets the median, and every recorded value stays as it was. The result is assigned back into the ambient underscore c column.

The third line prints the median, converted with float and rounded to three decimal places so it reads cleanly. The fourth prints the missing count for every column.

The final output should show zero in every column. That means no blank cells remain. The filled values are estimates, so we record that they were estimated. Run this on your own copy of the file.

## Slide 34: Validate the result before interpreting charts

Count original and retained rows. Check duplicate record IDs, missing values and valid loads again.

.all() answers True only when every row passes the condition. A check confirms what the data contain; a table named cleaned_data is not automatically correct.

**Spoken script**

Before we trust the charts, we check the cleaned table. A table called cleaned underscore data is not automatically correct. The name is only a label, so we need evidence.

We count the original rows and the retained rows. We check again for repeated record IDs. We check again for missing values. And we check again that every load is valid.

For the last check we use the tool all with empty brackets. It answers True only when every row passes the condition. If even one row fails, it answers False.

A check like this confirms what the data actually contain.

## Slide 35: Check the cleaned table

Expect 91 original rows, 88 retained rows, zero duplicate IDs, zero remaining missing cells, and True for the load check. Missing temperatures are estimates; the unchanged raw table retains the original gaps.

Run after the preceding example using the supplied CSV.

```python
print("Rows before:", len(raw_data))
print("Rows after:", len(cleaned_data))
print("Duplicate IDs:", cleaned_data.duplicated("record_id").sum())
print(cleaned_data.isna().sum())
print("Loads valid:", cleaned_data["load_pct"].between(0, 100).all())
```

**Spoken script**

We run five checks on the cleaned table.

The first two lines print the number of rows before cleaning, from raw underscore data, and the number of rows after cleaning, from cleaned underscore data.

The third line counts repeated record IDs in the cleaned table, using duplicated and then sum. The fourth prints the missing count for each column. The fifth checks the load column with between zero and one hundred, followed by all, and prints True or False.

We expect ninety-one original rows and eighty-eight retained rows. We expect zero duplicate IDs and zero missing cells. And we expect True for the load check.

The filled temperatures are estimates. The raw table is unchanged, so it still holds the original gaps, and anyone can compare the two. Run this after the previous example, using your own copy of the file.

## Slide 36: Summaries and grouped results

mean, min and max summarise a numeric column. groupby collects rows with the same equipment label before calculating.

Use the cleaned table for summaries and charts.

**Spoken script**

Now we summarise the cleaned data.

Three tools describe one numeric column. Mean gives the average. Min gives the lowest value. Max gives the highest.

We also want results for each piece of equipment. The tool is groupby. It collects all the rows that share the same equipment label into a bundle, and then calculates on each bundle separately. So instead of one average for the whole file, we get one average per equipment label.

A group average describes the observations in this file. It does not prove that the equipment itself caused a difference.

We use the cleaned table for summaries and charts. If we used the raw table, repeated rows and impossible loads would distort every number.

## Slide 37: Operations for the next example

01

Mean of recorded values: series.mean() adds known values and divides by their count. pandas skips missing values by default. The result has the same unit as the original column.

02

Several summaries at once: series.agg(["mean", "min", "max"]) applies those three named calculations and returns a labelled Series of results. min and max give the lowest and highest recorded values.

03

Grouping rows: table.groupby("label")["value"] groups the value column by matching labels. Apply mean() or sum() to calculate one result per group. Missing group labels are excluded by default.

**Spoken script**

Three tools prepare our summaries.

First, series dot mean. A Series is one column of a table. Mean adds up the known values and divides by how many there are. Pandas skips missing values by default. The answer has the same unit as the original column.

Second, series dot agg with a list of three names in quotes, mean, min and max. Agg is short for aggregate, which means combining many values into one summary. This applies the three calculations and returns a labelled Series with one result for each name.

Third, table dot groupby with a label column in brackets, followed by the value column in square brackets. This groups the value column by matching labels. We then call mean or sum to get one result per group. Rows with a missing group label are left out by default.

Together these let us summarise a whole column and each equipment group.

## Slide 38: Summaries of the cleaned CSV

Store three summary values for the target in target_summary.

Run this example on the supplied engineering_data.csv.

```python
target_summary = cleaned_data["target"].agg(["mean", "min", "max"])
mean_target_by_equipment = (
    cleaned_data.groupby("equipment_id")["target"].mean())
print(target_summary)
print(mean_target_by_equipment.round(3))
```

**Spoken script**

We calculate summaries on the cleaned table.

The first line takes the target column of cleaned underscore data and calls agg with mean, min and max. The result is a small labelled set of three numbers, stored as target underscore summary.

The second statement is groupby on the equipment underscore id column, then the target column, then mean. It gives one average target for each piece of equipment, stored as mean underscore target underscore by underscore equipment.

The third line prints target underscore summary. The fourth prints the grouped means rounded to three decimal places.

The first printout shows the lowest, average and highest target across all cleaned rows. The second shows how the average differs between equipment. We keep the same unit as the target column. Remember that these averages describe this file only. Run this on your own copy of the file.

## Slide 39: Choosing a chart for the question

This week uses histograms, scatter plots and bar charts. The other chart types are reference examples.

**Spoken script**

Before we draw more charts, we choose the right chart for the question.

This week we use three. A bar chart compares named groups, such as the average target for each equipment group. A histogram counts how many individual readings fall in each numeric interval, which shows how the readings are spread. A scatter plot places each row by two numbers, such as target against load.

For each chart, we should be able to say what one mark means. One bar in a histogram is a count of readings in an interval. One dot in a scatter plot is one row. One bar in a bar chart is the summary for one group.

The slide says other chart types are reference examples only. Remember that changing the interval width in a histogram can change its shape, so we state our choice and also inspect the data.

## Slide 40: Charts and units

A scatter plot compares two numerical columns. A histogram counts observations in value intervals. A bar chart compares group summaries.

plt.subplots creates a Figure and plotting Axes. Use ax= to choose where pandas draws, then label each axis.

**Spoken script**

We match each chart to its job and label it with units.

A scatter plot compares two numeric columns. A histogram counts observations in value intervals. A bar chart compares summaries for groups.

To draw any of them, we call plt dot subplots. It creates a figure, which is the whole image, and axes, which is the area where the chart is drawn. We then pass ax equals the axes to pandas, so pandas knows where to draw.

Finally we label each axis, using set underscore xlabel for the horizontal one and set underscore ylabel for the vertical one. A label should say what is measured and its unit. A chart without labels forces the reader to guess.

We use ten bins for histograms, as the project requires.

## Slide 41: Operations for the next example

plt.subplots() returns two objects: a figure (the whole image) and axes (the plotting area). Store them as scatter_figure and scatter_axes.

The ax= argument tells pandas where to draw: ax=scatter_axes uses that plotting area. Keep the library keyword ax unchanged.

**Spoken script**

Two ideas come before we draw the scatter plot.

First, plt dot subplots with empty brackets returns two objects. One is a figure, the whole image. The other is axes, the plotting area inside the image. We store them under two names of our choice, scatter underscore figure and scatter underscore axes. Although the second name is plural, one axes object holds one plot here.

Second, the argument ax equals tells pandas where to draw. In ax equals scatter underscore axes, the word ax on the left is a name defined by pandas, so we keep it exactly as written. The name on the right is our own variable that points to the plotting area.

Each new call to plt dot subplots creates a separate image and plotting area. We call it again each time we want a new chart.

## Slide 42: Load and motor temperature demand

Import plotting tools using the conventional alias plt.

Run this example on the supplied engineering_data.csv.

```python
import matplotlib.pyplot as plt
scatter_figure, scatter_axes = plt.subplots()
cleaned_data.plot.scatter(
    x="load_pct", y="target", ax=scatter_axes)
scatter_axes.set_xlabel("Load (%)")
scatter_axes.set_ylabel("Motor temperature (°C)")
plt.show()
```

**Spoken script**

We draw the scatter plot using the cleaned table.

The first line imports matplotlib dot pyplot as plt, the plotting library with its short name.

The second line calls plt dot subplots and stores the results as scatter underscore figure and scatter underscore axes.

The third statement calls plot dot scatter on cleaned underscore data, with x equals load underscore pct and y equals target, drawing into scatter underscore axes. It places one dot for each row. Rows with a missing coordinate cannot form a dot.

The next two lines set the horizontal label to load in percent and the vertical label to motor temperature in degrees Celsius. Plt dot show displays the chart.

Compare it with the earlier chart made before cleaning. The impossible load is gone. We describe any trend we see in the dots, and we do not claim that load caused the temperature. Run this on your own copy of the file.

## Slide 43: Operations for the next example

A bar for each labelled value: series.plot.bar(ax=ax) draws a bar for each Series label. When the Series contains group means, bar heights represent those means.

Histogram intervals: series.plot.hist(bins=10, ax=ax) groups known values into ten value intervals and counts observations in each. Bar heights are counts, not the original measurement values.

**Spoken script**

Two chart tools are next.

The first is series dot plot dot bar, with ax equals our drawing area. It draws one bar for each label in the Series. When the Series holds group means, each bar's height is that group's mean.

The second is series dot plot dot hist, with bins equals ten and ax equals our drawing area. A histogram groups the known values into ten intervals and counts how many observations land in each one. The height of each bar is a count of observations. It is no measurement value from the original column.

So a bar chart shows one summary number per label. A histogram shows how many readings fall in each numeric interval. Keeping that difference clear helps us read each chart correctly.

## Slide 44: Mean motor temperature for each equipment group

Create a new image and plotting area dedicated to this bar chart.

Run this example on the supplied engineering_data.csv.

```python
bar_figure, bar_axes = plt.subplots()
mean_target_by_equipment.plot.bar(ax=bar_axes)
bar_axes.set_xlabel("Equipment ID")
bar_axes.set_ylabel("Mean motor temperature (°C)")
plt.show()
```

**Spoken script**

We draw a bar chart of the group means.

The first line creates a new figure and drawing area, named bar underscore figure and bar underscore axes. Each chart gets its own image and its own plotting area.

The second line takes mean underscore target underscore by underscore equipment, the grouped averages we computed earlier, and calls plot dot bar into bar underscore axes. We get one bar for each equipment label, and the bar height is that equipment's average motor temperature.

The next two lines label the horizontal direction equipment ID and the vertical direction mean motor temperature in degrees Celsius. Plt dot show displays the chart.

We read it by comparing bar heights between equipment labels. A taller bar means a higher average in this file. It does not prove the equipment is the cause. Run this after the previous examples, using your own copy of the file.

## Slide 45: Distribution of motor temperature readings

Create a separate histogram image and plotting area.

Run this example on the supplied engineering_data.csv.

```python
histogram_figure, histogram_axes = plt.subplots()
cleaned_data["target"].plot.hist(
    bins=10, ax=histogram_axes)
histogram_axes.set_xlabel("Motor temperature (°C)")
histogram_axes.set_ylabel("Observation count")
plt.show()
```

**Spoken script**

We draw a histogram of the cleaned motor temperatures.

The first line creates a separate figure and plotting area, named histogram underscore figure and histogram underscore axes.

The second statement takes the target column of cleaned underscore data and calls plot dot hist with bins equals ten and ax equals histogram underscore axes. This groups the cleaned temperatures into ten intervals and counts the observations in each.

The next two lines label the horizontal direction motor temperature in degrees Celsius and the vertical direction observation count. Plt dot show displays the chart.

Now compare this with the histogram we drew before cleaning. Several things may have changed, such as the number of observations. We describe the differences we can see. We do not explain them with causes that our data cannot support. Run this on your own copy of the file.

## Slide 46: Optional extension: check numeric text

The main cleaning and charting walkthrough is complete. Continue here only if time permits.

Sometimes a numeric column contains text that cannot be converted to a number. The following check distinguishes that problem from an existing blank.

**Spoken script**

The main walkthrough for cleaning and charting is complete. Continue with this extension only if time permits. It is optional.

Sometimes a column that should hold numbers contains text that cannot be turned into a number, such as a word typed by mistake. That is a different problem from a blank cell, and we want to tell the two apart.

The next slides show a check for this. Our supplied file has no such text, so we expect the count of failed conversions to be zero. We reuse raw underscore data, the original table, so we inspect the entries exactly as they were recorded.

## Slide 47: Operations for the next example

Converting numeric text: pd.to_numeric(column, errors="coerce") converts numeric values or text. Unparseable text becomes missing. Compare original and converted values so existing gaps are not counted as conversion failures.

**Spoken script**

We meet one tool for converting text to numbers. It is pd dot to underscore numeric, and we give it a column and errors equals coerce.

To convert means to change the stored type of each value. Numbers stay as numbers, and text that looks like a number becomes a number. The word coerce means to force. With coerce, any text that cannot be read as a number becomes a missing value.

That creates a small trap. A cell that was already blank also shows up as missing after conversion. So after converting, we compare the original column with the converted one. A conversion failure is a cell that held something in the original and became missing in the converted version. A blank that was already there is not counted as a failure.

## Slide 48: Check numeric conversion of ambient temperature

Start conversion of the original ambient column into numbers.

Run this example on the supplied engineering_data.csv.

```python
ambient_numbers = pd.to_numeric(
    raw_data["ambient_c"], errors="coerce")
value_was_recorded = raw_data["ambient_c"].notna()
conversion_failed = value_was_recorded & ambient_numbers.isna()
print(int(conversion_failed.sum()))
print(raw_data[conversion_failed].head())
```

**Spoken script**

We check whether any ambient temperature entries fail to convert.

The first statement calls pd dot to underscore numeric on the original ambient underscore c column, with errors equals coerce, and stores the result as ambient underscore numbers. Unreadable text would now be missing.

The second line asks which original cells were recorded, using notna, and stores the answers as value underscore was underscore recorded.

The third line combines two answers with the ampersand symbol. A conversion failed when the original value was recorded and the converted value is missing. The result is conversion underscore failed.

The fourth line prints the number of failures, using sum and converting it with int. The fifth prints the first rows that failed.

On our file we expect zero, and an empty table. That tells us the column holds no unreadable text. Run this on your own copy of the file.

## Slide 49: Optional extension: put steps in a function

A function gives a reusable calculation a name. Its body runs when the function is called.

The next example calculates mean load for each equipment group; it is practice, not an A6 requirement.

**Spoken script**

This extension is optional practice. It is not required for assignment six.

A function gives a reusable calculation a name. When we write a function, its body does nothing until we call it by name. Once defined, we can call it many times on different inputs.

A function has parameters, which are the inputs it expects. It sends back a result with the word return, and that result is passed back to whoever called the function.

The next example calculates the mean load for each equipment group. Its input is a list of records, where each record is a dictionary describing one row. Inside, the function turns those records into a table, groups it, and returns the means.

You can come back to this after the cleaning steps feel comfortable.

## Slide 50: Operations for the next example

Returning a dictionary: series.to_dict() maps Series labels to values. table.to_dict("records") instead returns a list of row dictionaries. Choose the form specified in the example.

A table from Python values: pd.DataFrame(records) builds a table from row dictionaries. With a dictionary of column lists, keys become column names and each list supplies that column’s values.

**Spoken script**

Two tools help us move between tables and plain Python values.

The first is to underscore dict. Called on a Series, it makes a dictionary that maps each label to its value. Called on a table with the word records in quotes, it makes a list of row dictionaries, one dictionary for each row, with column names as keys. We choose whichever form the example asks for.

The second is pd dot DataFrame with a collection in the brackets. It builds a table from Python values. Given a list of row dictionaries, it makes one row from each dictionary. Given a dictionary of column lists, the keys become the column names, and each list supplies the values for that column.

So to underscore dict turns a table into plain Python data, and DataFrame turns plain Python data back into a table.

## Slide 51: A function called with the supplied records

equipment_records is the list of row dictionaries supplied to this function.

Run this example on the supplied engineering_data.csv.

```python
def mean_load_by_equipment(equipment_records):
    equipment_data = pd.DataFrame(equipment_records)
    mean_load_by_group = (
        equipment_data.groupby("equipment_id")["load_pct"].mean())
    return mean_load_by_group.to_dict()
raw_records = raw_data.to_dict("records")
print(mean_load_by_equipment(raw_records))
```

**Spoken script**

We define a function and call it.

The line starting with def defines the function. Its name is mean underscore load underscore by underscore equipment, and it takes one input, equipment underscore records. That is the list of row dictionaries given to the function.

Inside, the first line builds a table with pd dot DataFrame from those records. The second line groups the table by equipment underscore id, picks the load underscore pct column and takes the mean. The third line returns that result, converted with to underscore dict so it becomes a dictionary.

After the function, the next line converts raw underscore data into a list of row dictionaries with to underscore dict and the word records. We call that list raw underscore records.

The last line prints what the function returns when we give it raw underscore records. The output is a dictionary with one average load for each equipment label. Run this on your own copy of the file.

## Slide 52: Your issued task

01

Investigate motor winding temperature.

02

Target units: deg C.

03

These are synthetic teaching records, not measurements suitable for deployment.

04

Each record is one operating observation; equipment_id repeats across observations.

**Spoken script**

This slide describes the task issued to your group. We are investigating motor winding temperature, and the target is measured in degrees Celsius.

Each record is one operating observation, which means one operating observation. The same piece of equipment appears on many rows, so equipment underscore id repeats.

The records are synthetic teaching data. Someone made them up for learning. They do not describe real equipment, and they are not good enough to use for deciding how a real machine should be run.

Keep the target name and its unit in mind, because your written evidence must state them.

## Slide 53: clean_records(records)

Return copied records in original order: remove repeated record_id after its first occurrence, drop rows with missing target or load_pct outside 0–100 inclusive, then fill missing ambient_c with the median of retained non-missing ambient_c values.

Preserve raw input.

No other changes.

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

The first required function is clean underscore records, and it takes one input called records.

It returns copies of the records in the original order. It makes three changes.

First, it removes any repeated record underscore id after its first occurrence. Second, it drops every row whose target is missing, and every row whose load underscore pct is outside the range zero to one hundred, including both endpoints. Third, it fills any missing ambient underscore c with the median of the ambient values that were recorded in the rows that remain.

It makes no other changes. It must preserve the raw input, so we work on copies and leave the original records alone.

Keep the exact function name and the exact outputs. Check types, units and your issued brief before you submit.

## Slide 54: summarize_records(clean_records)

Return count, mean, minimum, maximum of target and group_means by equipment_id.

Retain full precision.

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

The second required function is summarize underscore records, and it takes cleaned records as its input.

It returns a summary with four values for the target column. These are the count, the mean, the minimum and the maximum. It also returns group underscore means, which gives the mean target for each equipment underscore id.

The slide says to retain full precision. That means we do not round any of the numbers. We return them exactly as calculated.

Keep the exact names and outputs given on the slide. Check types, units and your issued brief before you submit.

## Slide 55: audit_cleaning(raw_records, cleaned_records)

Return raw_count and cleaned_count; duplicate_ids is the number of cleaned records beyond the first occurrence of each record_id; missing_targets counts None targets; invalid_loads counts cleaned load_pct outside 0–100 inclusive.

Report the actual supplied data, which may still contain defects.

Do not change either input.

All five values are integer counts.

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

The third required function is audit underscore cleaning, and it takes two inputs, raw underscore records and cleaned underscore records. An audit is a check that reports what is true about the data.

It returns five values. Raw underscore count and cleaned underscore count are the number of records in each input. Duplicate underscore ids is the number of cleaned records that come after the first occurrence of their record underscore id. Missing underscore targets is the count of records whose target is None. Invalid underscore loads is the count of cleaned records whose load underscore pct lies outside zero to one hundred, including both endpoints.

It reports the actual supplied data, which may still contain defects, so we do not fix anything inside the audit. It must not change either input. All five values are integer counts, meaning whole numbers.

Keep the exact names and outputs. Check types, units and your issued brief.

## Slide 56: Written evidence

01

Use the cell headed “My written evidence”.

02

Explain the supplied scenario in your own words.

03

State target units, reasons and limitations.

04

Submit one complete notebook containing code and written evidence.

**Spoken script**

Alongside the code, we submit written evidence. Use the notebook cell headed My written evidence.

In it, explain the supplied scenario in your own words. Then state the target units, give your reasons for each cleaning choice, and describe the limitations, which are the things your analysis cannot tell us.

A good explanation links a decision to a named result. For example, we might say we removed a row because its load was outside the valid range, and then give the effect on the row count.

Submit one complete notebook containing both the code and the written evidence.

## Slide 57: Cleaning and quality submission

01

Opens: 16 Oct 2026, 11:00 Kampala

02

Deadline: 23 Oct 2026, 11:00 Kampala

03

Use your full Student Registration Number in the form.

04

Keep the submitted files and confirmation.

Open W06 assignment form

https://docs.google.com/forms/d/e/1FAIpQLSfcvyIDBXQG0fnr8EYsAHCsFatx8MDwAjzct3kPMz2JgAPxZQ/viewform

**Spoken script**

This slide covers submission of the week six assignment. Check the slide for the dates and times when the form opens and closes.

Enter your full Student Registration Number in the form. The required file is one completed notebook.

Keep the files you submitted and the confirmation you receive. Saving a file in Drive or on GitHub does not count as a submission. Only the form submission does.

The form link is on the slide. Use the button there to open the week six assignment form.

## Slide 58: Project preparation

01

Use the published data analysis project brief.

02

Build the evidence gradually in your project notebook.

03

Keep raw data, labelled charts, run instructions and individual contributions.

04

Published deadline: 30 Oct 2026, 11:00 Kampala

**Spoken script**

We also prepare for the data analysis project. Use the published project brief, which sets out what the project needs.

Build your evidence gradually in the project notebook, as you go along, so nothing is left to the last day.

Keep four things. Keep the raw data. Keep labelled charts, which means charts with named axes and units. Keep instructions for running the work. And keep a record of each person's individual contribution, saying exactly which part each member produced.

The slide shows the published deadline, so check it there.

## Slide 59: Week 6 quiz

01

Answer individually after the lecturer activates the quiz.

02

Available for 24 hours from activation.

03

Use your Student Registration Number and registered account.

04

Check the announced quiz closing time.

Open this week’s quiz

https://forms.gle/BwRZGzPvSzTwDqaH6

**Spoken script**

The week six quiz is answered individually. It opens when the lecturer activates it, and then it stays open for twenty-four hours.

Use your Student Registration Number and your registered account. Check the announced closing time so you know when the quiz ends.

The link on the slide opens the response form. The twenty-four hours run from the moment the lecturer activates the quiz.

## Slide 60: Revision and submission checklist

Explain each cleaning or modelling decision using your pandas table and its outputs.

Keep raw data unchanged. Restart and run all cells before submitting the required assignment notebook.

Point to your evidence. Save your work.

**Spoken script**

Before you finish, make sure you can explain each cleaning or modelling decision, using your pandas table and its outputs as evidence.

Keep the raw data unchanged. Before submitting the required assignment notebook, restart the notebook and run all the cells from the top. This confirms that the notebook works from start to finish.

Point to your evidence. When you justify a change, show its effect and say which values are estimates. Then save your work.

## Slide 61: Optional revision video

01

For revision after class.

02

StatQuest with Josh Starmer
Boxplots are Awesome!!!

03

Opening up to 04:00, optional preview-selected excerpt

04

Listening question: What does the box show, and does a point outside it prove an error?

Open explainer video

https://www.youtube.com/watch?v=fHLhBnmwUM0

**Spoken script**

This video is optional and is for revision after class. It comes from StatQuest with Josh Starmer and is titled Boxplots are Awesome. The suggested part is the opening, up to four minutes.

Before watching, think about this question. What does the box show, and does a point outside it prove an error?

A boxplot is a chart that summarises where the middle of the data sits and how spread out it is. The link is on the slide if you want to watch it.
