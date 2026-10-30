# CML3112 Week 7

Each slide shows its text, then the spoken script the lecturer reads aloud.

## Slide 1: Preparing for Practical Test 1

Civil Engineering and Architecture

Practical revision before Test 1
Test time: confirm with the lecturer

**Spoken script**

Welcome to Week 7. This week we prepare for Practical Test 1. It is practical revision for civil engineering and architecture.

We learn no new syntax. We rehearse what we already know on a practice file, step by step, so that the test feels familiar.

Take your time with each example. The practice is ungraded.

For the test time, please check the slide and confirm it with the lecturer.

## Slide 2: Your revision files

01

Use this slide deck and CML3112_Test1_practice.csv. Save both on your laptop.

02

Work through the examples in order in a new Colab notebook. Try each practice question before reading its answer.

03

Practice is ungraded. Keep your notebook for revision. No form submission is needed.

**Spoken script**

This week we prepare for Practical Test 1. Nothing new appears. We practise what we already know on a small practice file.

You need two things on your laptop: this slide deck and the practice CSV named on the slide. Save both.

Then open a new notebook in Colab and work through the examples in order. Before you read the answer to a practice question, try it yourself first. That is how the practice helps.

The practice is ungraded. Keep your notebook, because it is your own revision copy. There is no form to submit this week.

## Slide 3: Practice and test-day files

01

BEFORE THE TEST: use CML3112_Test1_practice.csv with the worked examples in this section.

02

ON TEST DAY: the entry page provides a different notebook and engineering_data.csv.

03

The test downloads unlock only during the scheduled test window.

**Spoken script**

We use two different sets of files, and it helps to keep them apart in your mind.

Before the test, we use the practice CSV with the worked examples in this section. It is small, so we can check every answer by hand.

On test day, the entry page gives you a different notebook and a different file called engineering underscore data dot csv. The same ideas apply, but the data is new.

The test downloads only unlock during the scheduled test window. So you will see them when the test begins, and the practice file is what we use until then.

## Slide 4: A new practice notebook in Colab

01

Open colab.research.google.com and sign in. Choose New notebook. Rename it Test revision.

02

Click Connect. Add a code cell with + Code. Run a cell with its triangle button.

03

Run cells from top to bottom. Save with File, then Save.

**Spoken script**

We start by making a fresh notebook. Open colab dot research dot google dot com and sign in. Choose New notebook, and rename it Test revision.

Next, click Connect. This starts the computer in the cloud that runs your code. To add a code cell, click plus Code. To run a cell, press the triangle button beside it.

Run the cells from top to bottom. A later cell uses names made by an earlier cell, so skipping one can cause an error.

When you finish, save with File, then Save. A tidy, saved notebook makes revision easy later.

## Slide 5: Uploading your practice CSV

01

In Colab, click the folder icon on the left. Click Upload and choose CML3112_Test1_practice.csv.

02

Wait until the filename appears in the Files panel. Keep its name unchanged.

03

If the session resets, upload the file again before running your cells.

**Spoken script**

The practice file must be inside Colab before we can read it. On the left of Colab, click the folder icon. Click Upload, and choose the practice CSV.

Wait until the file name appears in the Files panel. Keep the name exactly as it is. Python is picky about spelling, so a changed name stops the file from being found.

One more thing to remember. Colab keeps uploaded files only for the current session. If the session resets, the file disappears, and you upload it again before running your cells.

If you ever see an error saying the file was not found, check these three things: the upload, the spelling, and whether the session reset.

## Slide 6: What each column means

01

reading identifies one measurement. machine identifies the equipment that produced it.

02

load is the equipment load in percent. target is power demand, measured in kW.

03

ambient is the surrounding air temperature in °C. A blank cell means the value is missing.

**Spoken script**

Let us learn what the columns mean in the practice file. We will use these names in every example.

The column reading identifies one measurement. The column machine identifies the equipment that produced it.

The column load is the equipment load, in percent. The column target is power demand, measured in kilowatts. Target is just the column name. The thing it holds is what we calculate and predict.

The column ambient is the temperature of the surrounding air, in degrees Celsius.

A blank cell means the value is missing. When pandas reads the file, a blank number shows as NaN.

Each row holds one measurement and the conditions around it.

## Slide 7: Reading a CSV with pandas

01

import pandas as pd loads pandas and gives it the short name pd.

02

pd.read_csv(filename) reads the uploaded table. The filename is text, so it needs quotation marks.

03

A name stores the resulting DataFrame. print(table) displays it, and len(table) counts its rows.

**Spoken script**

Reading a CSV takes three small steps, and we have used all of them before.

First, import pandas as pd. This loads the pandas library and gives it the short name pd, so we type less afterwards.

Second, pd dot read underscore csv, with the file name in brackets, reads the uploaded table. The file name is text, so it goes inside quotation marks.

Third, we store the result under a name of our choice. That result is a DataFrame, which is a table with named columns. Then print of the table shows it, and len of the table counts its rows.

CSV means comma separated values. It is a plain text table where commas separate the columns.

## Slide 8: Loading the supplied practice file

source keeps the original file contents.

Blank numeric cells appear as NaN.

Expected: seven rows.

```python
import pandas as pd
filename = "CML3112_Test1_practice.csv"
source = pd.read_csv(filename)
print(source)
print(len(source))
```

**Spoken script**

Now we load the practice file. First line: import pandas as pd. Second line: filename equals the practice file name inside quotation marks. Third line: source equals pd dot read underscore csv of filename. We call the table source because it keeps the original contents of the file.

The fourth line prints the table, and the fifth prints its length.

When we run this, we see seven rows. Some cells show NaN. NaN is how pandas displays a blank number, meaning the value is missing.

Look at the table for a moment. Reading 1 appears twice. Reading 5 has no target. Reading 6 has a load of 120. These are the problems we clean in the next slides. Nothing needs to be memorised here. We only need to see that the file is loaded and has seven rows.

## Slide 9: The practice cleaning rules

01

Keep the first row for each reading identifier. Remove rows whose target is missing.

02

Keep load values from 0 to 100, including both limits.

03

After those removals, replace missing ambient values with the retained ambient median.

**Spoken script**

The practice file comes with clear cleaning rules. Cleaning means fixing a table before we calculate from it.

Rule one. If a reading identifier appears more than once, keep the first row for it. Also remove any row whose target is missing.

Rule two. Keep only loads from 0 to 100, and both 0 and 100 are allowed. Load is a percentage, so a value like 120 is impossible.

Rule three. After those removals, fill each missing ambient value with the median of the ambient values that remain.

The order matters, because the median must come from the rows we kept. On test day, the test gives you its own rules. You read them carefully and follow them in the same careful way.

## Slide 10: Removing duplicates and missing targets

01

drop_duplicates("reading") keeps the first occurrence of each reading identifier.

02

dropna(subset=["target"]) removes a row when its target is missing.

03

.copy() creates a separate table. We keep source unchanged for comparison.

**Spoken script**

Two pandas functions do the first two cleaning steps.

The first is drop underscore duplicates with the word reading in quotation marks. It looks at the reading column, and when an identifier repeats, it keeps the first row and removes the later ones.

The second is dropna with subset equals a list holding target. Dropna means drop the missing. With subset, it only checks the target column. So a row disappears when its target is blank. A blank ambient value does not remove a row. We fill that later.

The last piece is dot copy. It makes a separate table to work on, so source stays unchanged and we can compare before and after.

## Slide 11: The first two cleaning steps

Remove one repeated reading.

Remove one missing target.

Expected row counts: 6, then 5.

```python
raw = source.drop_duplicates("reading")
print(len(raw))
raw = raw.dropna(subset=["target"]).copy()
print(len(raw))
```

**Spoken script**

Let us run the first two cleaning steps. Line one: raw equals source dot drop underscore duplicates of reading. This removes the repeated reading 1. Line two prints the length.

Line three: raw equals raw dot dropna with subset equal to a list of target, then dot copy. This removes reading 5, which has no target. Line four prints the length again.

We expect six, and then five. Seven rows became six after the repeat was removed. Six became five after the missing target was removed.

Notice that source still has seven rows. We built raw as a new working table. The original is safe if we want to look at it again.

## Slide 12: Selecting a valid load range

01

between(0, 100) returns True for loads from 0 to 100. Other values receive False.

02

.loc[mask] keeps rows marked True. A mask is a row-by-row list of yes/no decisions.

03

The practice row with load 120 must be removed.

**Spoken script**

Next we keep only loads in the valid range. We do this with a mask.

A mask is a row by row list of yes or no decisions. Each row gets True if it passes the check, and False if it fails.

The check is between with 0 and 100 in brackets. It gives True for loads from 0 to 100, including both limits. Every other value gets False.

Then dot loc with the mask in square brackets keeps the rows marked True and drops the rest.

In the practice file, the row with load 120 fails the check, so it must be removed. After filtering, the row labels on the left may have gaps. That is normal, and those labels are just positions.

## Slide 13: Keeping the valid loads

["load"] selects one column.

tolist displays its values as a list.

Expected retained targets: [10.0, 20.0, 30.0, 40.0].

```python
mask = raw["load"].between(0, 100)
raw = raw.loc[mask].copy()
print(raw["target"].tolist())
```

**Spoken script**

Here is the load filter in code. Line one: mask equals raw, square brackets with load in quotation marks, dot between of zero and one hundred. The square brackets with a name select one column, and between checks every value in it.

Line two: raw equals raw dot loc of mask, then dot copy. This keeps only the rows marked True and gives us a clean working table.

Line three prints raw, then target, then dot tolist. Tolist shows the values as a plain Python list.

We expect the list ten, twenty, thirty and forty, written as ten point zero and so on. That means four rows remain. All later means and charts use these four rows.

## Slide 14: The median and missing ambient values

01

The median is the middle value after sorting the known values. Here: 20, 30, 40. Median: 30 °C.

02

.median() ignores missing values. .fillna(value) replaces only missing entries.

03

Calculate this median after removing the unwanted rows.

**Spoken script**

The median is the middle value after we sort the known values. In the practice file, the known ambient values that remain are 20, 30 and 40. The middle one is 30. So the median is 30 degrees Celsius.

Two details help us here. The dot median function ignores missing values, so blanks do not disturb the answer. And dot fillna with a value replaces only the missing entries, and leaves known values as they are.

The timing is important. We calculate the median after removing the unwanted rows. The rejected rows had high ambient values, and using them would change the answer. Reading 2 has no ambient value, so it will receive 30.

## Slide 15: Filling the missing ambient value

The median uses retained rows only.

Expected: 30.0 and [20.0, 30.0, 30.0, 40.0].

```python
median = raw["ambient"].median()
raw["ambient"] = raw["ambient"].fillna(median)
print(median)
print(raw["ambient"].tolist())
```

**Spoken script**

Now we fill the missing ambient value. Line one: median equals raw, ambient in square brackets, dot median. Python works out the middle of the known ambient values in the four kept rows.

Line two: raw, ambient in square brackets, equals raw ambient dot fillna of median. We put the filled column back into the table, so the table changes. Without this assignment, the table would stay the same.

Lines three and four print the median and the ambient list.

We expect thirty point zero, then the list twenty, thirty, thirty and forty. Reading 2 now holds 30. The median used only the retained rows, and source still holds all seven original rows.

## Slide 16: Selecting, averaging and grouping

01

raw["target"] selects one column, called a Series.

02

.mean() adds the known values and divides by their count.

03

.groupby("machine") collects rows with the same machine label before calculating a result for each machine.

**Spoken script**

Three small ideas get us to averages by group.

First, raw with target in square brackets selects one column. A single column is called a Series. It is a list of values with labels.

Second, dot mean adds the known values and divides by how many there are. For our four targets, ten plus twenty plus thirty plus forty is a hundred, and a hundred divided by four is twenty five.

Third, dot groupby with machine in quotation marks collects the rows with the same machine label. Then it calculates a result for each machine separately. M1 has ten and twenty, so its mean is fifteen. M2 has thirty and forty, so its mean is thirty five.

## Slide 17: Overall mean and machine means

Select target, then calculate.

Expected: overall 25.0; M1 15.0; M2 35.0. All are in kW.

```python
overall = raw["target"].mean()
groups = raw.groupby("machine")["target"].mean()
print(overall)
print(groups)
```

**Spoken script**

Here are the overall mean and the machine means. Line one: overall equals raw, target in square brackets, dot mean. We select the target column, then calculate its average. Line two: groups equals raw dot groupby of machine, target in square brackets, dot mean. This sorts the rows by machine, selects target, and averages inside each group. Lines three and four print the two results.

Our four targets are ten, twenty, thirty and forty. The overall mean is twenty five point zero. The machine means come out as M1 fifteen point zero and M2 thirty five point zero.

All three answers are in kilowatts. The printed Series for the groups also shows a line saying Name target, dtype float64. That line only describes the Series, and the numbers above it are the answers. The calculation does not change raw.

## Slide 18: Practice: calculate a changed mean

01

Using the four retained targets, imagine the last value changes from 40 to 60.

02

Calculate the overall mean and both machine means on paper.

03

Keep the CSV and notebook unchanged for the next example.

**Spoken script**

Now a short exercise on paper. We take our four retained targets: ten, twenty, thirty and forty. Imagine the last value changes from forty to sixty.

Calculate the overall mean first. Then calculate the mean for each machine. Remember that M1 holds the first two readings and M2 holds the last two.

Use a pencil and work it by hand. Test questions often ask for a calculation you can check this way.

This is only a thought experiment. We do not change the CSV or the notebook, because the next examples need the original values. When you have your answers, move to the next slide to check them.

## Slide 19: Practice answer

01

Overall: (10 + 20 + 30 + 60) / 4 = 30 kW.

02

M1: 15 kW. M2: (30 + 60) / 2 = 45 kW.

03

The four retained rows still end with target 40.

**Spoken script**

Here is the answer to the practice question.

For the overall mean, we add ten, twenty, thirty and sixty. That makes one hundred and twenty. Divide by four, and we get thirty kilowatts.

For machine M1, nothing changed, so its mean stays fifteen kilowatts. For M2, we average thirty and sixty. That gives forty five kilowatts.

Only M2 holds the changed reading, which is why only its mean moved. The overall mean moved too, since it includes that reading.

This was a hypothetical calculation. The four retained rows in our notebook still end with a target of forty, so the charts that follow use the original values.

## Slide 20: Charts and numerical findings

01

A scatter plot shows pairs of values, such as load and target.

02

Label each axis with its quantity and unit. Give the chart a descriptive title.

03

For a finding, state the value, unit and what it describes. A pattern alone does not prove a cause.

**Spoken script**

This slide covers charts and findings.

A scatter plot shows pairs of values. Each point is one row, placed by its load across and its target upward.

Every chart needs labels. Label each axis with what it measures and its unit, and give the chart a descriptive title. A reader should understand the chart without asking you.

A finding is a sentence that reports a result. State the value, the unit and what it describes. For example, the mean target for machine M2 was thirty five, with its unit.

Be careful with causes. A pattern in a small table shows what happened in those rows. It does not prove why. So we write what we see and avoid claiming the cause.

## Slide 21: A labelled practice chart

scatter places one point per row.

xlabel and ylabel name the axes.

show displays the chart.

Expected points: (20, 10), (40, 20), (60, 30), (80, 40).

```python
import matplotlib.pyplot as plt
plt.scatter(raw["load"], raw["target"])
plt.xlabel("Load (%)")
plt.ylabel("Target (kW)")
plt.title("Four practice readings")
plt.show()
```

**Spoken script**

Here is a fully labelled chart. First we import matplotlib dot pyplot as plt. Then plt dot scatter takes the load column for the horizontal axis and the target column for the vertical axis. Scatter places one point per row.

Next, plt dot xlabel names the horizontal axis, Load, with its unit, percent. Plt dot ylabel names the vertical axis, Target, with its unit, kilowatts. Plt dot title gives the chart a name, Four practice readings. Last, plt dot show displays it.

We expect four points: at load 20, target 10; at 40 and 20; at 60 and 30; and at 80 and 40. They rise together from left to right.

This cell prints no numbers, because it draws a picture. We always include the units in the axis labels, so never leave them out.

## Slide 22: Histograms and group-mean bars

01

A histogram counts readings within numeric ranges. plt.hist(values, bins=...) defines those ranges.

02

A bar chart compares named groups. plt.bar(labels, heights) places one bar per label.

03

The histogram shows the target distribution. The bars show one mean per machine.

**Spoken script**

We have two more chart types to revisit.

A histogram counts readings within numeric ranges. We call plt dot hist with the values and bins equals something. The bins define the ranges. Each bar shows how many readings fall in one range.

A bar chart compares named groups. We call plt dot bar with the labels first and the heights second. We get one bar for each label.

Here is how we use them. The histogram shows the distribution of the target, meaning how the values spread out. The bars show one mean per machine.

Both charts use the same cleaned four row table from before.

## Slide 23: A target histogram

bins gives the interval boundaries.

The y-axis counts records.

Expected: two readings in each of the two bins.

```python
plt.hist(raw["target"], bins=[0, 25, 50])
plt.xlabel("Target (kW)")
plt.ylabel("Number of readings")
plt.title("Practice target distribution")
plt.show()
```

**Spoken script**

Now a histogram of the target. We call plt dot hist of raw target, with bins equal to a list: zero, twenty five and fifty. The bins are the boundaries of the ranges. So we get two ranges: from zero up to twenty five, and from twenty five to fifty.

Plt dot xlabel names the horizontal axis, Target, in kilowatts. Plt dot ylabel says Number of readings, since the vertical axis counts records. Plt dot title names the chart, and plt dot show draws it.

Targets ten and twenty fall into the first range. Targets thirty and forty fall into the second. So we expect two readings in each bar, which is four readings in total.

The cell prints no numbers. It only draws the chart.

## Slide 24: Bar labels and heights

01

groups contains the mean for each machine. Its index holds the machine labels.

02

groups.index gives M1 and M2. groups.values gives 15 and 35.

03

Pass labels first and heights second to plt.bar.

**Spoken script**

Before we draw the bars, we need to know what is inside groups. It is the result of the machine mean from earlier. It is a Series, and a Series has two parts.

The first part is the index, which holds the labels. Here the labels are the machine names, so groups dot index gives M1 and M2.

The second part is the values. Groups dot values gives fifteen and thirty five, the two means.

For plt dot bar we pass the labels first and the heights second. The first label M1 matches the first height, fifteen. So our two inputs are already ready, and no extra work is needed.

## Slide 25: Machine-mean bars

Each bar represents a group mean.

Use the same unit as target.

Expected bar heights: M1 = 15, M2 = 35.

```python
plt.bar(groups.index, groups.values)
plt.xlabel("Machine")
plt.ylabel("Mean target (kW)")
plt.title("Mean target by machine")
plt.show()
```

**Spoken script**

Here are the machine mean bars. Line one: plt dot bar of groups dot index, comma, groups dot values. The index supplies the labels M1 and M2, and the values supply the heights. We get one bar for each machine.

Plt dot xlabel says Machine. Plt dot ylabel says Mean target, with the unit in brackets, kilowatts. We use the same unit as the target, since a mean has the same unit as the values it averages. Plt dot title says Mean target by machine, and plt dot show draws the chart.

We expect two bars. M1 has height fifteen, and M2 has height thirty five. M1 averages readings 1 and 2. M2 averages readings 3 and 4.

These means describe this small sample. They do not show a cause.

## Slide 26: Functions and returned answers

01

A function is a named calculation. def starts its definition. Indented lines belong to it.

02

An argument supplies the input. return sends the result back to the caller.

03

In the test, keep every supplied function name and calculate from its input.

**Spoken script**

A function is a named calculation. We write it once and use it many times.

The word def starts the definition. The lines indented below it belong to the function. An argument is the input we give it, written in brackets after the name. The word return sends the answer back to the code that called the function.

A common mix up involves print. Print only shows a value on the screen. It does not hand the value back. For answers, we use return.

On test day, keep every function name exactly as supplied, and calculate from the input. A function that only holds a copied answer works for one example and fails when the grader tries other records. The practice function on the next slide is just for practice and uses its own name.

## Slide 27: A practice function

values receives the supplied column.

float returns a Python decimal number.

Expected: mean target 25.0; mean load 50.0%.

```python
def average_reading(values):
    readings = pd.Series(values)
    return float(readings.mean())

print(average_reading(raw["target"]))
print(average_reading(raw["load"]))
```

**Spoken script**

Here is a small practice function. The line def average underscore reading, with values in brackets, names the function and its input. Values will receive a column.

The next line makes readings equal to pd dot Series of values. This turns the input into one labelled column.

The third line returns float of readings dot mean. Mean finds the average, and float turns the result into a plain Python decimal number. Return sends it back.

After the function, we call it twice, and print each result. The first call uses the target column. The second uses the load column.

We expect twenty five point zero for the target, and fifty point zero for the load. We got two answers from one function, because the input changed.

## Slide 28: Practice columns and test columns

01

Practice reading corresponds to test record_id. Practice machine corresponds to test equipment_id.

02

Practice load corresponds to test load_pct. Practice ambient corresponds to test ambient_c. target has the same name.

03

The calculations are the same. Use the column names in the file you are working with.

**Spoken script**

The practice file and the test file use different column names for the same ideas. Let us read the pairs aloud.

Practice reading matches test record underscore id. Practice machine matches test equipment underscore id. Practice load matches test load underscore pct. Practice ambient matches test ambient underscore c. The column called target has the same name in both.

An identifier such as record id labels one observation. It tells us which row is which.

The good news is that the calculations are identical. Only the names change. Always use the column names in the file you are working with. The test notebook explains its columns before the tasks, and the next examples use the practice names.

## Slide 29: Tables and lists of records

01

A DataFrame is a labelled table. A list of dictionaries stores the same rows as separate Python records.

02

table.to_dict("records") returns one dictionary per row. pd.DataFrame(records) turns those records back into a table.

03

The test supplies a conversion helper. You may use it when returning cleaned records.

**Spoken script**

Sometimes the test wants cleaned data returned as a list of records. We should understand what that means.

A DataFrame is a labelled table. A record is one row written as a Python dictionary, which is a set of named entries like load and target. A list of dictionaries holds all rows this way.

Table dot to underscore dict with the word records in quotation marks gives one dictionary per row. And pd dot DataFrame of the records turns them back into a table.

The test supplies a conversion helper, and you may use it when returning cleaned records. You do not need to write that part from scratch.

## Slide 30: The retained rows as records

[0] selects the first record.

The table has the same columns and values.

Expected: first record has reading 1 and target 10. Row count: 4.

```python
practice_records = raw.to_dict("records")
print(practice_records[0])
restored = pd.DataFrame(practice_records)
print(len(restored))
```

**Spoken script**

Let us convert the four retained rows. Line one: practice underscore records equals raw dot to underscore dict of records. This gives a list with one dictionary per row.

Line two prints practice underscore records, square bracket zero. The zero selects the first record in the list.

We see reading 1, machine M1, load 20, target 10 and ambient 20. The labels on the left side of the table do not appear in the dictionaries.

Line three: restored equals pd dot DataFrame of practice underscore records. Line four prints its length, and we expect four. The rebuilt table has the same columns and the same values as raw, so we lose nothing when we convert.

## Slide 31: Missing values during conversion

01

The test helper uses astype(object) so cells can hold Python None.

02

notna() marks known values. where(mask, None) keeps those values and replaces missing cells with None.

03

The helper finishes with to_dict("records"). It is supplied so you do not have to invent a missing-value converter.

**Spoken script**

When a test passes records into a function, missing values arrive as None, which is Python's word for nothing there. The test helper converts the table for us, and it does this in three steps. We do not write it ourselves. It helps to know what happens.

First, astype with object lets cells hold Python None. It changes how values are stored. The measurements stay the same.

Second, notna marks the known values with True. Then where with the mask and None keeps the known values and puts None in the missing cells.

Third, the helper finishes with to underscore dict of records. Pandas normally shows missing numbers as NaN, and the function interface uses None. Because the helper is supplied, we do not have to invent a missing value converter.

## Slide 32: A helper for the original CSV

source is the original uploaded CSV.

Expected: 7 original records, including the rows to remove.

```python
def as_records(table):
    objects = table.astype(object)
    return objects.where(table.notna(), None).to_dict("records")

original_records = as_records(source)
print(len(original_records))
```

**Spoken script**

We now write our own copy of that helper, named as underscore records. It takes one input called table.

Line two: objects equals table dot astype of object. Line three returns objects dot where of table dot notna, comma None, then dot to underscore dict of records. This keeps the known cells, replaces missing cells with None, and builds the list.

Because it works on whatever table we give it, it uses its argument and needs no global variable.

Then we call as underscore records on source, store the result as original underscore records, and print its length.

We expect seven. The list still includes the duplicate, the missing target and the invalid load, because we have not cleaned anything yet.

## Slide 33: A cleaning function follows the same steps

01

def names the function and its input. Every indented line belongs to that function.

02

Build a table from the input, apply the earlier cleaning rules, and return records using the helper.

03

Calling the function with different records must calculate a new result.

**Spoken script**

A cleaning function is built from steps we already know. The first line, def, names the function and its input. Every indented line belongs to it.

Inside, we build a table from the input records. We apply the cleaning rules in the same order as before: remove repeats, remove missing targets, keep valid loads, fill the missing ambient with the median. Then we return the records using the helper.

The key idea is that the function calculates from whatever input it receives. If we call it with different records, it must give a new result.

When you read a cleaning function, ask four things. What is the input? Which rows are removed? What replaces the missing values? What type is returned? You do not need to memorise any practice values.

## Slide 34: The complete practice cleaning function

The input is records, not a global CSV table.

Returns a new list of cleaned records. It does not print the answer.

```python
def revision_clean(records):
    table = pd.DataFrame(records)
    table = table.drop_duplicates("reading")
    table = table.dropna(subset=["target"])
    table = table.loc[table["load"].between(0, 100)].copy()
    middle = table["ambient"].median()
    table["ambient"] = table["ambient"].fillna(middle)
    return as_records(table)
```

**Spoken script**

Here is the full practice cleaning function. We read it line by line.

The def line names it revision underscore clean and takes records. The next line builds a table with pd dot DataFrame of records.

Then comes drop underscore duplicates on reading. After that, dropna on the target. After that, we keep loads from zero to one hundred with loc and between, and add dot copy.

Next, middle equals the median of ambient in this cleaned table, and fillna puts middle into the gaps.

The last line returns as underscore records of the table. It sends back a new list of cleaned records, and it does not print the answer.

The input is the list of records the caller supplies, so the function works on any records we give it. Seven input rows become six, then five, then four.

## Slide 35: Calling the cleaning function

The original list remains available.

Expected: 7 original rows, 4 cleaned rows, replacement ambient 30.0.

```python
cleaned_records = revision_clean(original_records)
print(len(original_records))
print(len(cleaned_records))
print(cleaned_records[1]["ambient"])
```

**Spoken script**

We now call the cleaning function on the original records.

The first line passes original underscore records into revision underscore clean. The function returns a new list, and we store it under the name cleaned underscore records. The original list is not touched, so we can still look at it afterwards.

The next two lines print the length of each list. The original list has seven records. The cleaned list has four, because one repeat, one missing target and one load of one hundred and twenty were removed.

The last line looks at one value. The square brackets work in two steps. The first pair, with the number one, picks the second record, because Python counts from zero. The second pair, with the word ambient in quotation marks, picks that record's ambient value. That record had a blank ambient cell. It now shows thirty point zero, the median we filled in.

## Slide 36: Summary values inside a dictionary

01

len(table) counts rows. target.min() and target.max() find the smallest and largest values.

02

A return dictionary gives each result a name: count, mean, minimum, maximum and group_means.

03

A grouped Series.to_dict() converts its equipment labels and means into another dictionary.

**Spoken script**

Next we build a summary of the cleaned data. We want five named answers.

The first is the count. The len function counts the rows in the table. The first is count, the second is mean, the third and fourth are the smallest and largest targets, and the fifth is group_means. Target dot min gives the smallest value in the target column, and target dot max gives the largest.

The mean is the average, and we met it earlier. The fifth answer is group underscore means, one average for each machine.

We return all five inside a dictionary. A dictionary is a collection where every answer has a name. So we can ask for count, or mean, or minimum, and get that exact answer back.

For group means, we take the grouped averages and call to underscore dict on them. This turns the machine labels and their averages into another small dictionary inside the big one.

With our four practice targets, the count is four, the mean is twenty-five, the minimum is ten and the maximum is forty. Machine M1 averages fifteen and machine M2 averages thirty-five.

## Slide 37: A summary function

Braces enclose key–value pairs.

Returns named numerical values and a dictionary of machine means.

```python
def revision_summary(records):
    table = pd.DataFrame(records)
    values = table["target"]
    groups = table.groupby("machine")["target"].mean()
    return {"count": len(table),
            "mean": float(values.mean()),
            "minimum": float(values.min()),
            "maximum": float(values.max()),
            "group_means": groups.to_dict()}
```

**Spoken script**

Here is the function that does all of that.

It is called revision underscore summary, and it takes the cleaned records as its input. The first line turns the records into a table. The second line picks out the target column and calls it values. The third line groups the rows by machine and averages the target within each group.

Then comes the return statement, which holds a dictionary. Curly brackets, called braces, open and close it. Inside, each entry is a name in quotation marks, a colon, and then its value. Commas separate the entries.

Count uses len of the table. Mean, minimum and maximum each use values, and we wrap them in float, which gives us a plain Python decimal number. The last entry, group underscore means, takes the grouped averages and converts them to a dictionary.

The function does not print anything. It sends the whole dictionary back to whoever called it. The dictionary is spread over several lines, but it is still one dictionary.

## Slide 38: Reading the returned summary

Use a key to retrieve a named answer.

Expected: 4 and 25.0; 10.0 and 40.0; M1: 15.0, M2: 35.0.

```python
summary = revision_summary(cleaned_records)
print(summary["count"], summary["mean"])
print(summary["minimum"], summary["maximum"])
print(summary["group_means"])
```

**Spoken script**

We call the summary function on the cleaned records and keep the result under the name summary.

To read one answer, we write the dictionary name and then the key in square brackets, with the key in quotation marks. So summary with the word count gives the count, and summary with the word mean gives the mean.

The first print line shows four and twenty-five point zero. The second shows the minimum, ten point zero, and the maximum, forty point zero. The third prints the group means. It shows machine M1 at fifteen point zero and machine M2 at thirty-five point zero.

These prints are for us. They help us check our own work. On test day the grader does not read what we print. It receives the dictionary that the function returns. The grader reads the dictionary that the function returns, so we use return.

## Slide 39: A Figure is an object you can return

01

plt.subplots() creates a Figure and its plotting Axes. fig holds the whole chart; ax holds the drawing area.

02

ax.scatter, ax.bar and ax.hist draw on those Axes. set_xlabel, set_ylabel and set_title add labels.

03

return fig gives the chart to the caller. plt.show() only displays it.

**Spoken script**

Some test tasks ask for a chart, so we need to know how a function can give a chart back.

The call plt dot subplots creates two things at once. The first is the Figure, which is the whole picture, like a blank sheet of paper. The second is the Axes, which is the drawing area on that sheet, where the points and bars go. We call them fig and ax.

We draw on the Axes. Ax dot scatter makes a scatter plot, ax dot bar makes bars, and ax dot hist makes a histogram. Set underscore xlabel, set underscore ylabel and set underscore title add the labels and the title.

Finally, return fig hands the finished chart to the caller. Plt dot show only displays the chart on the screen. It does not hand anything back.

So in the test we return the Figure itself. We do not return a file name, a screenshot or a description of the chart.

## Slide 40: A function returning a scatter Figure

fig and ax receive the two created objects.

The returned Figure contains four points from the practice CSV.

```python
def revision_scatter(table):
    fig, ax = plt.subplots()
    ax.scatter(table["load"], table["target"])
    ax.set_xlabel("Load (%)")
    ax.set_ylabel("Target (kW)")
    ax.set_title("Practice load and target")
    return fig
```

**Spoken script**

This function draws one scatter plot and returns it.

The input is a table of cleaned rows. The first line creates the Figure and the Axes and stores them as fig and ax. The second line draws the scatter. It takes the load column for the horizontal position and the target column for the vertical position, so each row becomes one point.

The next three lines add words. The x label says Load, with the percent sign in brackets. The y label says Target, with kilowatts in brackets, so anyone reading the chart knows the unit. The title says Practice load and target.

The last line returns fig. We return the Figure, which holds the whole chart.

With our practice file, the returned Figure holds four points. The function reads only the table it is given, and it does not change that table.

## Slide 41: Alphabetical order for group means

01

groupby("machine")["target"].mean() calculates one mean per machine.

02

sort_index() orders that Series by its labels. M1 comes before M2.

03

Use the same ordered Series for both the bar labels and heights.

**Spoken script**

This slide is about getting bars in a sensible and fixed order.

We start with the same grouped average as before. The group by call collects the rows for each machine, and the mean gives one average per machine. The result is a Series, which is one column of values with a label on each value. The labels here are the machine names.

Sort underscore index puts those labels in alphabetical order. M1 comes before M2. If there were more machines, they would also line up alphabetically.

The key point is to use this one ordered Series for both parts of the bar chart. The labels come from its index and the heights come from its values, so each bar keeps the right height.

If we sorted only the heights, a number could end up under the wrong machine. By sorting the Series itself, each label and its average move together.

## Slide 42: A function returning ordered bars

sort_index sorts the group labels.

Expected bar order and height: M1 = 15, then M2 = 35.

```python
def revision_bars(table):
    means = table.groupby("machine")["target"].mean()
    means = means.sort_index()
    fig, ax = plt.subplots()
    ax.bar(means.index, means.values)
    ax.set_xlabel("Machine")
    ax.set_ylabel("Mean target (kW)")
    ax.set_title("Practice machine means")
    return fig
```

**Spoken script**

This function returns a bar chart with one bar for each machine.

The first line groups the table by machine and averages the target. The second line puts those averages in alphabetical order of machine name. The third line creates the Figure and Axes.

Then ax dot bar draws the bars. The first thing we pass in is the labels, which are the machine names. The second is the heights, which are the averages. Because both come from the same ordered Series, every label sits above its own bar.

The labels follow. The x label says Machine. The y label says Mean target, with kilowatts in brackets. The title says Practice machine means. The function ends with return fig.

With our practice data, we expect two bars. M1 comes first with a height of fifteen, and M2 comes second with a height of thirty-five.

## Slide 43: Ten histogram bins

01

The earlier two-bin example explained counting. The test asks for ten equal-width bins.

02

ax.hist(values, bins=10) divides the range from the minimum to the maximum into ten equal intervals.

03

For practice targets 10 to 40, each bin is 3 units wide. Empty bins still count as bins.

**Spoken script**

A histogram sorts readings into ranges and counts how many fall in each range. Those ranges are called bins.

Earlier we chose the bin edges ourselves, and we used two bins. In the test, the task asks for ten bins of equal width. We write ax dot hist, then the values, then bins equals ten. Matplotlib then takes the span from the smallest value to the largest and cuts it into ten equal intervals.

Notice that ten bins means ten intervals.

For our practice targets, the smallest is ten and the largest is forty. The span is thirty, and thirty divided by ten gives three. So each bin is three units wide.

We only have four readings, so most bins will be empty. That is fine. An empty bin is still a bin, and it is drawn with zero height. We do not reuse the old edges of zero, twenty-five and fifty for the test.

## Slide 44: A function returning a ten-bin histogram

bins=10 lets matplotlib calculate the edges.

Expected: 10 bars with total count 4, spanning targets 10 to 40.

```python
def revision_histogram(table):
    fig, ax = plt.subplots()
    ax.hist(table["target"], bins=10)
    ax.set_xlabel("Target (kW)")
    ax.set_ylabel("Number of observations")
    ax.set_title("Practice target distribution")
    return fig
```

**Spoken script**

This function returns the histogram Figure.

The first line makes the Figure and the Axes. The second line calls ax dot hist on the target column, with bins equals ten. We do not list the edges. We let matplotlib calculate them from the data.

Then come the labels. The x label says Target, with kilowatts in brackets, because the horizontal axis shows target values. The y label says Number of observations, because the vertical axis counts readings. The title says Practice target distribution. The function ends with return fig.

For our practice data, we expect ten bars. Most of them have zero height. The heights add up to four, because there are four readings. The bars spread across targets from ten to forty.

If your Figure shows ten bars and the heights add up to the number of rows, the function is doing its job.

## Slide 45: Returning the three Figures in order

Each helper returns one real Figure.

The list holds scatter, bar and histogram Figures in that order.

```python
def revision_charts(records):
    table = pd.DataFrame(records)
    return [revision_scatter(table),
            revision_bars(table),
            revision_histogram(table)]

figures = revision_charts(cleaned_records)
plt.show()
```

**Spoken script**

Now we combine the three chart functions into one.

Revision underscore charts takes the cleaned records. Its first line turns the records into a table. Then it returns a list, written with square brackets. The list holds three things, each made by a helper function we wrote already. The first is the scatter Figure. The second is the bar Figure. The third is the histogram Figure. The order matters: scatter, then bars, then histogram.

Each helper returns a real Figure object, so the list holds three real Figures.

After the function, we call it on the cleaned records and store the list under the name figures. Then plt dot show lets us look at the charts on screen.

A helper function must be defined before we call the function that uses it. In the real test, we keep the function name that the notebook gives us, and helpers are allowed.

## Slide 46: The gap between group means

01

The group gap is the largest group mean minus the smallest group mean.

02

Our machine means are 15 and 35. The gap is 35 − 15 = 20.

03

This differs from the individual target range: 40 − 10 = 30.

**Spoken script**

A group gap tells us how far apart two groups are on average.

We find the average for each machine. Then we take the largest group average and subtract the smallest one. The answer is the group gap.

In our practice data, the machine averages are fifteen and thirty-five. The gap is thirty-five minus fifteen, which is twenty.

We should not mix this up with the range of the individual readings. The smallest single target is ten, the largest is forty, and forty minus ten gives thirty. That number describes the spread of single readings. The group gap describes the distance between two averages. They answer different questions, so they give different numbers.

The gap has the same unit as the target. It tells us what we see in this sample. It does not tell us why the machines differ.

## Slide 47: Calculating the group gap

max and min operate on group means here.

Expected: group gap 20.0 kW.

```python
table = pd.DataFrame(cleaned_records)
means = table.groupby("machine")["target"].mean()
gap = float(means.max() - means.min())
print(gap)
```

**Spoken script**

Here is the group gap in code.

The first line builds a table from the cleaned records. The second line groups by machine and takes the average target, which gives one number for each machine. The third line takes the largest of those averages, subtracts the smallest, and wraps the answer in float to get a plain decimal number. We call it gap. The last line prints it.

The important detail is that max and min work on the machine averages here. That is why the answer is thirty-five minus fifteen, which is twenty.

We expect twenty point zero. The unit is kilowatts, the same unit as the target.

This is an observed difference in our small practice sample. It does not tell us why one machine has a higher average.

## Slide 48: A finding contains a value and a unit

01

A finding is a small dictionary, for example {"value": 25.0, "unit": "kW"}.

02

The outer dictionary names the finding. The inner dictionary stores its number and unit.

03

Use observations for count. Use the target unit for mean, minimum, maximum and group_gap.

**Spoken script**

A numerical finding needs two parts. It needs the number, and it needs the unit that goes with it.

We store a finding as a small dictionary with two keys. The first key is value, and it holds the number. The second key is unit, and it holds the unit as text. For example, value twenty-five point zero and unit kilowatts.

The test asks for five findings, and each has a name. So we use a dictionary inside a dictionary. The outer dictionary holds the name of the finding. Each name points to an inner dictionary with the value and the unit.

There is a rule for the units. For the count, we use the word observations. For the mean, the minimum, the maximum and the group gap, we use the unit of the target column, which is kilowatts for us.

Matching the unit to the quantity matters. A number in the wrong unit is a wrong finding.

## Slide 49: A helper for a value with its unit

The function returns one inner dictionary.

Expected: 25.0 kW.

```python
def with_unit(value, unit):
    return {"value": value, "unit": unit}

example = with_unit(25.0, "kW")
print(example["value"], example["unit"])
```

**Spoken script**

This small helper makes one finding for us, so we do not type the same dictionary five times.

The function is called with underscore unit, and it takes two inputs. The first is the value. The second is the unit. Its only line returns a dictionary with two entries. The key value holds the number we passed in, and the key unit holds the text we passed in.

Below the function, we try it. We call with underscore unit with twenty-five point zero and the unit kilowatts, and we store the result under the name example. Then we print the value and the unit by asking example for each key.

The output is twenty-five point zero followed by kilowatts.

This helper returns one inner dictionary. In the next function, we use it for every finding, so each answer carries its unit.

## Slide 50: Returning the five practice findings

The count has a different unit.

Returns five findings, each containing value and unit.

```python
def revision_findings(records):
    result = revision_summary(records)
    means = pd.Series(result["group_means"])
    gap = float(means.max() - means.min())
    unit = "kW"
    return {"count": with_unit(result["count"], "observations"),
            "mean": with_unit(result["mean"], unit),
            "minimum": with_unit(result["minimum"], unit),
            "maximum": with_unit(result["maximum"], unit),
            "group_gap": with_unit(gap, unit)}
```

**Spoken script**

This function returns all five findings at once.

It takes the cleaned records. Its first line reuses the summary function we wrote, so the numbers stay consistent. Then we turn the group means dictionary into a Series, so that we can call max and min on it. The gap is the largest group mean minus the smallest, as before. We also store the unit text, kilowatts, in one name called unit.

The return statement builds the outer dictionary with five keys: count, mean, minimum, maximum and group underscore gap. Each key holds the result of with underscore unit.

The count is given the unit observations, because it counts rows. The other four use our target unit, kilowatts.

The function does not print. It returns a dictionary of five findings. Each finding has a value and a unit.

## Slide 51: Checking the returned findings

Two keys reach a nested value.

Expected values: count 4, mean 25.0, group gap 20.0.

```python
findings = revision_findings(cleaned_records)
print(findings["count"])
print(findings["mean"])
print(findings["group_gap"])
```

**Spoken script**

Now we check the findings with the practice records.

We call revision underscore findings on the cleaned records and store the result as findings. Then we print three of the entries.

The count prints as a small dictionary. Its value is four and its unit is the word observations. The mean prints with value twenty-five point zero and the target unit. The group gap prints with value twenty point zero and the same target unit.

To reach a number inside, we use two keys in a row. The first key picks the finding, and the second picks the value or the unit. So findings, then group underscore gap, then value, gives us just the number twenty point zero.

If your three printed results look like this, your function is working on the practice data.

## Slide 52: Practice: another input to your functions

01

Use original_records[:2] to select the first two original records. Clean this smaller input.

02

Call your summary, charts and findings functions on that result.

03

Predict the retained count, mean and group gap before running.

**Spoken script**

Here is a practice task. We test whether our functions really work on other input.

The expression original underscore records, then a colon and a two in square brackets, is called a slice. It takes the first two records from the list, at positions zero and one.

We clean this smaller input with revision underscore clean. Then we pass the cleaned result to the summary function, the charts function and the findings function.

Before we run anything, we predict three things. How many records are retained? What is the mean target? What is the group gap? Take a minute to work these out on paper or in your head. Look at the first two original rows in the practice file, and check each cleaning rule against them.

After that, run the cells and compare. If your prediction matches the output, you understand the functions. If not, find the step where your thinking and the code disagree.

## Slide 53: Practice answer

01

The two input records have unique IDs, known targets and valid loads. Both remain.

02

Mean target: 15. Only M1 remains, so group gap is 0. The missing ambient value becomes 20.

03

The functions calculate from the supplied argument, even when its length changes.

**Spoken script**

Here is the answer to that practice task.

The two records have different reading identifiers, so there are no repeats. Both have known targets, and both have loads between zero and one hundred. So both records stay.

The first record has a target of ten and the second has a target of twenty. The mean is fifteen. Both records belong to machine M1, so there is only one group. With one group, the largest and smallest group mean are the same number. The group gap is zero.

The second record had a blank ambient value. The only known ambient value is twenty, so the median is twenty, and that becomes the replacement.

This shows why a function must calculate from its input. The same code gave different answers for four records and for two records. A function with fixed answers pasted in would fail here.

## Slide 54: What a filled value can and cannot tell us

01

A median replacement is an estimate, not a recovered measurement. It can change summaries and patterns.

02

Keep the original data and state the replacement rule.

03

A pattern in synthetic practice data does not establish real equipment performance.

**Spoken script**

Filling a missing value is useful, but we must understand what it means.

When we replace a blank with the median, the new number is an estimate. It is a sensible guess made by a rule. In our practice file, reading two had no ambient value, and we put in thirty. We do not know that the true temperature was thirty.

Because the filled number is a guess, it can change our averages and patterns. So we keep the original data, and we state the rule we used. That way, anyone can tell which values were recorded and which were estimated.

One more point. Our practice data is synthetic, which means it was made up for teaching. A pattern in it does not tell us how real equipment performs. We use it to practise the method.

## Slide 55: An identifier is not a clock

01

reading and record_id identify observations. Their numbers do not tell us elapsed time.

02

A time trend needs an actual timestamp or a documented time sequence.

03

An equipment mean describes the observed sample. Investigate representative measured data before making operational decisions.

**Spoken script**

An identifier is a label. The columns reading and record underscore id give each row a name so we can tell rows apart.

A label is only a name. The number on a reading does not tell us when it was taken. Reading four does not mean hour four, and reading two does not mean it was taken before reading three in real time. The numbers may have been assigned when the data was collected or when it was imported.

If we want to study a trend over time, we need a real timestamp, or a time sequence that has been written down and documented.

The same care applies to averages. An equipment mean describes the readings we have. In our practice data, M2 has a higher mean than M1. That does not prove M2 is faulty. Before anyone makes a decision about real equipment, we would look at representative measured data. For this teaching dataset, we only practise reading the numbers correctly.

## Slide 56: Test 1 revision checklist

01

Read and clean the CSV, then return records without changing the input.

02

Return a summary dictionary, three Figure objects and five findings with units. Check the practice outputs.

03

Explain the limits of imputation, the difference between association and cause, and why an identifier is not time.

**Spoken script**

This slide is our checklist for revision. We can use it to check ourselves before the test.

First, can we read a CSV and clean it, and return the cleaned records without changing the input data?

Second, can we return a summary dictionary, a list of three Figure objects, and five findings that each carry a unit? We should run the practice versions and check that the outputs match what we expect.

Third, can we explain three ideas in our own words? The first is the limits of filling in missing values. The second is the difference between two things moving together and one causing the other. The third is why an identifier carries no time.

The practice results are four rows, an overall mean of twenty-five, machine means of fifteen and thirty-five, and an ambient median of thirty. The test has its own function names and return formats, so we should not paste these practice numbers into test answers. We should calculate them from the input.

## Slide 57: Recording interpretation answers

01

Read each question and its labelled answer options. Choose the option supported by the data or code.

02

In DECISIONS, keep the question identifier unchanged and replace its blank value with your chosen option letter.

03

These letters identify answer choices. The portal assigns your test files automatically.

**Spoken script**

Some test questions ask us to interpret data. For each one, the notebook shows a question and a list of answer options with letters.

We read the question and the options. Then we choose the option that the data or the code supports.

We record the choice in a dictionary called DECISIONS. Each entry has a question identifier as its key, and a blank value. We keep the identifier exactly as it is. We replace only the blank with our chosen option letter.

These letters are just labels for answer choices. They have nothing to do with which files you receive. The portal gives each student their test files automatically, so nobody picks a version.

So the job is simple. Read the question, choose the supported option, and type its letter into the matching entry in DECISIONS.

## Slide 58: A dictionary entry for a practice question

"practice" is a question identifier.

"B" is that question’s selected option.

Syntax example only: B represents a chosen option, not a test version.

```python
DECISIONS = {"practice": "B"}
print(DECISIONS["practice"])
```

**Spoken script**

Here is the DECISIONS dictionary in its simplest form.

The line starts with the name DECISIONS, then an equals sign, then braces. Inside the braces is one entry. The word practice in quotation marks is the key, which is the question identifier. After a colon comes the value, the capital letter B in quotation marks. That is the option chosen for that question.

The second line prints DECISIONS with the word practice in square brackets. Python looks up the key and shows its value, which is B.

This is only a demonstration of the syntax. The letter B here stands for a chosen option.

In the real test, the notebook already has the question keys. We edit those existing entries and fill in our own choices. We do not replace them with the word practice.

## Slide 59: Test-day instructions

01

The practice section ends here. Keep your revision notebook for study.

02

The following slides explain the timed test files, individual work and submission.

03

Use the portal-issued notebook and CSV for the actual test.

**Spoken script**

This slide marks the end of the practice section.

Everything before this point was revision. We should keep our revision notebook so that we can study from it.

The slides that follow explain the real test. They cover the timed test files, working individually, and how to submit.

For the actual test, we use the notebook and the CSV file that the portal gives us. We do not use the practice files.

So from here on we read the procedure, so that on the day we already know what to expect.

## Slide 60: Your test files on test day

01

Downloads unlock at the scheduled start time. Open the link or scan its QR code.

02

Enter your name, Google email and Student Registration Number.

03

Download your notebook and engineering_data.csv.

Open your test files

Direct URL (click or copy into your laptop browser):

https://iuea-test-entry.jothammartin-wambi.workers.dev/?test=CML3112%7CTEST1

**Spoken script**

This is how we get our test files on test day.

The downloads unlock at the scheduled start time. We open the link on the slide, or we scan the QR code with a phone.

The page asks for three details. We enter our name, our Google email and our Student Registration Number.

Then we download two files. One is our notebook. The other is engineering underscore data dot csv.

The page gives each student their files automatically. We do not choose anything. 

The direct web address is shown on the slide. We can click it, or copy it into the browser on our laptop.

## Slide 61: Opening the notebook and CSV

01

In Colab: File → Open notebook → Upload. Select the downloaded notebook.

02

Save a copy in Drive. Connect the session.

03

In Files on the left, upload engineering_data.csv.

**Spoken script**

Once we have both files, we open them in Colab.

First, in Colab we choose File, then Open notebook, then Upload. We select the notebook that we downloaded.

Second, we save a copy in Drive, and we connect the session.

Third, the notebook does not carry its data with it. So we look at the Files panel on the left, and we upload engineering underscore data dot csv there. We wait until the file name appears in the list.

Only then do we run the cells in order. If we follow these steps in order, we start the test with the notebook ready and the data in place.

## Slide 62: One notebook contains all answers

01

Code tasks have a prompt, function name and marks.

02

Six interpretation questions: record your chosen option letters in DECISIONS.

03

Submit one notebook snapshot using the final button.

**Spoken script**

Everything we submit lives in one notebook.

The notebook has two kinds of tasks. The first kind is code tasks. Each code task gives a prompt, the name of the function to write, and the marks it carries. We keep the function name exactly as given.

The second kind is interpretation. There are six interpretation questions. For these, we record our chosen option letters in the DECISIONS dictionary, as we practised.

When we have finished, we submit one notebook snapshot using the final button at the end of the notebook.

Our functions and our choices in DECISIONS are what we hand in.

## Slide 63: How the 100 marks are allocated

01

Cleaning 20. Summary statistics 15.

02

Three labelled charts 15. Five numerical findings 20.

03

Structured interpretation 30.

**Spoken script**

The test is marked out of one hundred, and the marks are shared across five parts.

Cleaning carries twenty marks. Summary statistics carries fifteen.

The three labelled charts carry fifteen marks. The five numerical findings carry twenty marks.

Structured interpretation carries thirty marks. That is the six interpretation questions we answer in DECISIONS.

Adding these up, twenty plus fifteen plus fifteen plus twenty plus thirty gives one hundred.

Knowing this helps us plan. Interpretation is the largest single part, so we should leave time to read those six questions carefully. Cleaning and findings each carry twenty marks, so they matter as well.

## Slide 64: Order of work

01

Load the raw CSV. Keep the original data.

02

Clean records before calculating summaries, charts and findings.

03

Answer the six interpretation questions.

**Spoken script**

Here is the order we should work in on test day.

First, we load the raw CSV, and we keep the original data as it is.

Second, we clean the records before we calculate anything else. Summaries, charts and findings all use the cleaned records, so cleaning has to come first.

Third, we answer the six interpretation questions.

This order follows the way the tasks depend on each other. If we calculate a mean before cleaning, the number would include rows that should have been removed.

So we start with the data, clean it, build the calculations on the cleaned records, and finish with interpretation. Keeping this order helps us avoid going back to repair earlier work.

## Slide 65: The three-hour session

01

First 15 minutes: setup and file checks.

02

Next 120 minutes: individual coding tasks.

03

Next 25 minutes: interpretation and checking.

04

Final 20 minutes: prepare the snapshot and submit the form.

**Spoken script**

The test lasts three hours, and the slide divides the time into four parts.

The first fifteen minutes are for setup and file checks. We open the notebook, upload the CSV, and make sure everything runs.

The next one hundred and twenty minutes are for the individual coding tasks. This is the longest part, and we work on our own.

The next twenty-five minutes are for interpretation and checking. We answer the interpretation questions and review our work.

The final twenty minutes are for preparing the snapshot and submitting the form.

Fifteen, one hundred and twenty, twenty-five and twenty add up to one hundred and eighty minutes, which is three hours.

## Slide 66: Before submitting

01

Restart the Colab session and run cells from the top.

02

Upload the same CSV again if the new session needs it.

03

Fix errors and run the final submission cell.

**Spoken script**

Before we submit, we do a final check that the whole notebook works from the start.

First, we restart the Colab session, and we run the cells from the top. A new session has no memory of earlier runs. So if a cell only worked because of an old value, this will show it.

Second, if the new session needs our CSV, we upload the same CSV again.

Third, we fix any errors that appear, and then we run the final submission cell.

It gives us confidence that the notebook we hand in runs in order from beginning to end.

We use that button on the next slide, so we are not finished until we complete that step too.

## Slide 67: Submission and confirmation

01

Click Submit test at the end of your notebook.

02

Open the generated form link using the same Google account. Check your details.

03

Press Submit before the deadline. Keep the confirmation.

**Spoken script**

Now we submit the test.

First, we click Submit test at the end of our notebook. This button prepares a snapshot of the notebook.

Second, we open the generated form link, using the same Google account that we used for the test. We check the details shown on the form.

Third, we press Submit on the form before the deadline. Then we keep the confirmation.

The deadline is shown on the form, so we check it there. The confirmation we keep is our record that we submitted.

## Slide 68: How grading works

01

The lecturer’s grader runs your submitted code on unseen data.

02

The private workbook records identity, submission time, status and marks.

03

A technical or identity problem remains pending until resolved.

**Spoken script**

Finally, here is how the test is graded.

The lecturer's grader runs the code that we submitted on unseen data. That means data that we have not seen. This is why our functions must calculate from their input and must not contain pasted answers.

The results go into a private workbook. It records each student's identity, the submission time, the status and the marks.

If there is a technical problem or an identity problem with a submission, it stays pending until it is resolved.

So the steps are clear. We write functions that work on any input, we submit through the form with the correct Google account, and the grader does the rest.
