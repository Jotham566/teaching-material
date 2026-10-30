# CML3112 Week 5

Each slide shows its text, then the spoken script the lecturer reads aloud.

## Slide 1: Using pandas to answer table questions

Civil Engineering and Architecture

Tuesday 06 October 2026
Tuesday 11:00–14:00, Room 106

**Spoken script**

Welcome to Week 5 for CML3112, the civil engineering and architecture group. Today we use a tool called pandas to answer questions about a table of data.

Pandas is a toolbox of ready-made code for Python. In earlier weeks we worked with lists, dictionaries and loops. Pandas does similar work on a whole table at once, in a few short lines.

By the end of the session we can ask a table questions, such as which rows pass a test and what the total is for each group. The slide shows the day, time and room for your class.

## Slide 2: Today’s learning

Read a labelled table and select rows.

Calculate column summaries and grouped totals.

You can explain which observations a filter keeps and what a grouped total means.

**Spoken script**

This slide shows where we are heading today. We will do two things.

First, we read a labelled table and select rows. A labelled table is a table where every column has a name at the top, like a sheet in Excel. Selecting rows means picking out only the records we want.

Second, we calculate column summaries and grouped totals. A column summary is one number that describes a whole column, such as an average. A grouped total is a total worked out separately for each group, such as the total energy for each building.

By the end of the session, you should be able to explain two things in your own words. You can say which rows a filter keeps, and you can say what a grouped total means.

## Slide 3: DataFrame and column names

A DataFrame is a table with named columns. campus_energy.csv contains meter_id, building, block, month, kwh and cost_ugx.

One row records a meter reading for a month. kwh measures energy and cost_ugx gives the cost in Uganda shillings.

**Spoken script**

A DataFrame is the pandas word for a table. Think of one sheet in Excel. Every column has a name, and every row is one record.

Last time we read a CSV file with the csv module and received lists of values. A DataFrame holds the same information, and it also remembers the column names for us.

Our file today is called campus underscore energy dot csv. It has six columns. meter underscore id is the name of an electricity meter. building is the building where that meter sits. block is the larger group the building belongs to. month is the month of the reading. kwh is the energy used, in kilowatt hours. cost underscore ugx is the cost in Uganda shillings.

One row records one meter's reading for one month.

## Slide 4: The supplied file

Extract this week’s student ZIP. Upload campus_energy.csv into Colab using the Files panel, or keep it beside the notebook locally.

The examples below read this file. Run the cells in slide order. Keep the original CSV unchanged.

**Spoken script**

Before we write any code, the data file must be in the right place.

Extract this week's student ZIP file. A ZIP file is one packed folder that holds several files. Inside is campus underscore energy dot csv.

If you work in Colab, open the Files panel and upload that CSV there. Uploading a notebook does not upload its data, so check that the CSV appears in the list of files. If you work on your own computer, keep the CSV in the same folder as your notebook.

The examples that follow all read this file. Run the cells in the same order as the slides. Keep the original CSV unchanged, so we can always go back to the original readings.

## Slide 5: Operations for the next example

01

Import and short names: import pandas as pd loads pandas and gives it the short name pd. pd.read_csv refers to a function in that library.

02

Reading a CSV: pd.read_csv("filename.csv") reads the named file into a DataFrame: a table with labelled columns and row labels. The file must exist in the working folder.

03

Counting dimensions: table.shape gives (number of rows, number of columns). shape is a property, so it has no parentheses.

**Spoken script**

Three small tools before our first example.

The first is import pandas as pd. To import means to bring a library into our notebook. A library is a collection of ready-made code written by other people. The words as pd give pandas a short nickname, so we can type pd instead of pandas every time.

The second is pd dot read underscore csv, with the file name in brackets and quotation marks. It reads the file and gives us back a DataFrame. In an earlier week we did this with the csv module and received lists. Now we receive a table with named columns and a label for every row. The file must be in the working folder, which is the folder our notebook runs in.

The third is dot shape. It gives two numbers, the number of rows first and then the number of columns. Shape has no brackets, because it is a stored fact about the table and needs no calculation.

## Slide 6: Operations for the next example

Column data types: table.dtypes reports each column’s stored type. int64 means integers, float64 means decimal numbers, and object often contains text. Numeric blanks commonly appear as NaN.

A preview of rows: table.head() returns the first five rows. It leaves the table unchanged. A preview is not the entire dataset.

**Spoken script**

Two more tools.

A data type is the kind of value a column holds. Writing table dot dtypes lists every column with its type. int64 means whole numbers. float64 means numbers that can have a decimal part. object usually means text.

Sometimes a number column has an empty cell. Pandas shows an empty number as capital N, small a, capital N, which means missing. A missing value is an empty slot in the table, and it is different from a zero reading.

The second tool is table dot head, with brackets. It shows the first five rows. A real table may have thousands of rows, so head gives us a quick look. It leaves the table unchanged. Five rows are only a small part of the dataset, so we should avoid drawing conclusions about the whole file from them.

## Slide 7: Loading the supplied observations

read_csv creates a DataFrame.

Run this cell on the supplied CSV. Read the output below the cell.

```python
import pandas as pd
raw = pd.read_csv("campus_energy.csv")
print(raw.head())
print(raw.shape)
print(raw.dtypes)
```

**Spoken script**

We now run our first pandas code on the supplied file.

Line one is import pandas as pd. It brings pandas into the notebook under the short name pd.

Line two reads the file. pd dot read underscore csv opens campus underscore energy dot csv, and the equals sign stores the resulting DataFrame in a variable called raw. We chose that name because this table holds the raw, original readings.

Line three prints raw dot head, which shows the first five rows with their column names. Read one whole row from left to right first. It tells us the meter, the building, the block, the month, the energy and the cost.

Line four prints raw dot shape. The first number is how many rows the whole file has, and the second is how many columns.

Line five prints raw dot dtypes. Read each column name beside its type. Run the cell and read the output below it.

## Slide 8: Selecting and summarising a column

raw["kwh"] selects the energy column as a Series. mean() averages its known values.

Square brackets select a named column. Parentheses call a method such as mean().

**Spoken script**

Now we look at one column on its own.

We write raw, then square brackets, then the column name in quotation marks. So raw square bracket kwh selects the energy column. The result is called a Series, which is a single column of values with a label for each row.

Then we add dot mean, with brackets. The mean is the average. Pandas adds up the known values in the column and divides by how many there are.

Two kinds of brackets appear here, and they do different jobs. Square brackets select a named column. Round brackets call a method. A method is an action attached to the thing before the dot, and mean is such an action.

The mean describes the readings in this file only. It is an average over the meter months that we have.

## Slide 9: Operations for the next example

01

Reading chained operations: Read a chain from left to right. In table["target"].mean(), select the target Series first, then calculate its mean. Each step uses the previous step’s result.

02

Rounded display: series.round(3) returns values rounded to three decimal places. Python round(number, 3) rounds one number. Keep unrounded calculations for returned assessment answers.

03

Selecting columns: table["column"] returns one labelled column, a Series. table[["a", "b"]] returns a DataFrame containing those named columns in that order.

**Spoken script**

Three ideas that help us read the next examples.

First, a chain. Read a chain from left to right. In table square bracket target square bracket dot mean, we first select the target column, and then we calculate its mean. Each step works on the result of the step before it.

Second, rounding. series dot round with the number three gives the values rounded to three decimal places. Python's own round function, with a number and a three, rounds one single number. When you return answers for assessment, keep the unrounded calculation.

Third, selecting columns. A single name in square brackets gives one column, a Series. A list of names inside square brackets gives a smaller DataFrame with those columns, in the order we wrote them. That means two pairs of square brackets, one pair for the list and one pair for the selection.

## Slide 10: Operations for the next example

Mean of recorded values: series.mean() adds known values and divides by their count. pandas skips missing values by default. The result has the same unit as the original column.

**Spoken script**

One more tool, the mean of the recorded values.

The mean is the ordinary average. Pandas adds up the known values and divides by how many there are. For example, the values two, four and six add to twelve, and twelve divided by three gives four.

If a cell is missing, pandas skips it by default. It leaves that cell out of both the adding and the counting.

The result has the same unit as the original column. If the column is in kilowatt hours, the mean is also in kilowatt hours. For our file, that is the average energy of one meter in one month.

## Slide 11: Energy values and their mean

head shows the first five readings.

Run this cell on the supplied CSV. Read the output below the cell.

```python
print(raw["kwh"].head())
print(round(float(raw["kwh"].mean()), 3))
```

**Spoken script**

This cell looks at the energy column and calculates its average.

Line one is print of raw square bracket kwh dot head. We select the kwh column, take its first five values with head, and print them. Each value appears beside its row label on the left. This is only a preview.

Line two is print of round of float of raw kwh dot mean, with three. We read it from the inside outwards. The mean calculates the average of the whole kwh column. Float turns the answer into an ordinary decimal number. Round with a three cuts it to three decimal places. Print shows it.

The average covers the entire column, and the head shows only five rows. Its unit is kilowatt hours for one meter in one month. Run the cell and read the output below it.

## Slide 12: Ask a question about each energy reading

raw["kwh"] selects the energy column. Comparing it with 5000 returns one True or False per row.

True means the reading is greater than 5,000 kWh; False means it is not. Equality does not pass this strict threshold.

**Spoken script**

We can ask a yes or no question about every row at once.

We select the energy column with raw square bracket kwh, and then compare it with five thousand using the greater than sign. Pandas checks every row and returns one answer per row. The answer is either True or False.

True means that the reading is greater than five thousand kilowatt hours. False means it is not. The sign is strictly greater than, so a reading of exactly five thousand gives False.

True and False are special values in Python called Boolean values. They are two values with no quotation marks around them. The threshold of five thousand is only a practice question for learning. It is no engineering safety limit.

At this stage we only collect the answers. Choosing the rows comes next.

## Slide 13: Operations for the next example

Selecting rows with a mask: A column comparison produces one True or False per row. table[mask] keeps the True rows. & combines masks: both conditions must hold. Parenthesise each comparison.

Adding values and counting True: series.sum() adds its values. For a Boolean mask, True counts as 1 and False as 0. table.isna().sum() therefore counts missing cells separately for each column.

**Spoken script**

Two ideas for working with rows.

First, a mask. When we compare a column with a number, we get one True or False for each row. We call that list of answers a mask. Putting the mask inside square brackets after the table keeps the rows where the answer is True and drops the rest.

To combine two questions, we use the and sign, the ampersand. Both conditions must hold for a row to stay. Put round brackets around each comparison, so that pandas reads them separately.

Second, adding and counting. series dot sum adds the values in the series. In a mask, True counts as one and False counts as zero. So summing a mask counts how many rows answered True.

The same idea counts missing cells. table dot isna marks each missing cell as True, and then dot sum counts them separately for each column.

## Slide 14: Inspect the answers before selecting rows

Run using this week’s supplied CSV.

```python
energy_is_high = raw["kwh"] > 5000
print(raw["kwh"].head())
print(energy_is_high.head())
```

**Spoken script**

We now store the question and look at its answers beside the data.

Line one reads energy underscore is underscore high equals raw square bracket kwh, greater than five thousand. The name on the left is a variable that stores the column of True and False answers.

Line two prints the first five energy readings. Line three prints the first five answers.

Place the two outputs side by side and match the row labels. Each answer belongs to the reading with the same row label. A reading above five thousand has True beside it. A reading at or below five thousand has False.

The comparison answers the question for every row and leaves the raw table unchanged. Run the cell with this week's supplied CSV and check each answer against its reading.

## Slide 15: Use the True answers to select rows

raw[energy_is_high] returns the rows whose answer is True. This selection is often called a Boolean mask.

.sum() counts True answers because True counts as 1 and False as 0.

**Spoken script**

Now we use the answers to choose rows.

We write raw, then square brackets, and inside them the variable energy underscore is underscore high. Pandas returns only the rows whose answer is True. We call this selection a Boolean mask.

There are two uses of square brackets to separate. A quoted name inside the brackets selects a column. A column of True and False answers inside the brackets selects rows. The answers and the table must refer to the same row labels.

We can also count the answers. dot sum adds them up, because True counts as one and False counts as zero. The total is the number of rows that passed the test.

## Slide 16: Keep and count the high-energy readings

Run using this week’s supplied CSV.

```python
high_energy_readings = raw[energy_is_high]
print(high_energy_readings.head())
print(int(energy_is_high.sum()))
```

**Spoken script**

This cell keeps the high readings and counts them.

Line one reads high underscore energy underscore readings equals raw, square brackets, energy underscore is underscore high. It builds a new table that contains only the rows with True, and stores it under that name. The original raw table stays unchanged.

Line two prints the first five rows of the new table. Each row shows the same columns as before, and the row labels on the left show which original rows were kept. Some labels are missing, because those rows were dropped.

Line three prints int of energy underscore is underscore high dot sum. The sum counts the True answers, and int shows the result as a whole number.

That count should equal the number of rows kept. A reading of exactly five thousand is left out, because the test is strictly greater than. Run the cell and read the output.

## Slide 17: Groups and labels

groupby("building") gathers rows with the same building label. Selecting kwh and calling sum adds their energy.

nunique counts distinct building labels. idxmax returns the label whose total is largest.

**Spoken script**

Now we answer a bigger question, which is how much energy each building used in total.

The tool is groupby. Writing groupby with building in quotation marks gathers together all rows that have the same building label. Think of sorting a pile of meter readings into one heap for each building. We then select the kwh column and call sum, and pandas adds up the energy inside each heap.

Two more tools help us read the result. nunique counts how many different labels there are. Used on the building column, it tells us how many distinct buildings the file contains.

idxmax gives the label that has the largest total. The answer is a building name. It is a label and carries no row number.

The totals cover the months that appear in the CSV.

## Slide 18: Operations for the next example

01

Counting distinct labels: series.nunique() counts different recorded values, ignoring missing values by default. It counts categories rather than rows.

02

Label of the largest value: series.idxmax() returns the label attached to the largest value. It does not return that value. If several entries tie, it returns the first such label.

03

Grouping rows: table.groupby("label")["value"] groups the value column by matching labels. Apply mean() or sum() to calculate one result per group. Missing group labels are excluded by default.

**Spoken script**

Three tools for groups.

First, series dot nunique. It counts the different values in a column. If a column holds Library, Library and Server Room, nunique gives two. It counts categories, and it skips missing values by default.

Second, series dot idxmax. A series has values and labels. idxmax finds the largest value and gives back the label attached to it. It returns the label itself, and the largest value stays hidden. If two entries tie for the largest, it returns the first label.

Third, grouping rows. table dot groupby with a label column in quotation marks, then square brackets with the value column. That gathers the value column into one group for each label. After that we call mean or sum, and pandas gives one answer per group. Rows with a missing group label are left out by default.

## Slide 19: Building totals from campus_energy.csv

Trace one building back to its source rows.

Run this cell on the supplied CSV. Read the output below the cell.

```python
totals = raw.groupby("building")["kwh"].sum()
print(totals)
print(raw["building"].nunique())
print(totals.idxmax())
```

**Spoken script**

This cell finds the energy total for each building.

Line one is totals equals raw dot groupby, building, then square brackets with kwh, then dot sum. Pandas gathers the rows of each building, takes the kwh values in each gathered group, and adds them. The result is stored in totals. It is a Series with one total for each building, and the building names serve as its labels.

Line two prints totals. Each line shows a building name and its total energy in kilowatt hours.

Line three prints raw building dot nunique. That is the number of different buildings in the file.

Line four prints totals dot idxmax. It gives the name of the building with the largest total.

To check the result, pick one building and find its rows in the source table. Add its kwh values by hand and compare with the total. Run the cell and read the output below it.

## Slide 20: A calculated energy rate

Cost divided by energy gives UGX per kWh. First check that the denominator is positive.

copy preserves raw. Assigning table["new_name"] adds a calculated column.

**Spoken script**

We can also calculate a new quantity from two columns.

Cost divided by energy gives the price of one kilowatt hour, in shillings. We call it UGX per kWh. Before dividing, we check that the energy is greater than zero, because dividing by zero has no meaning.

To keep our original table safe, we use dot copy. It makes a separate working table, so changes to the copy leave raw untouched.

Then we add the new column. We write the copy's name, square brackets, and a new column name in quotation marks, followed by an equals sign and the calculation. Pandas creates that column and fills it with one result for every row.

The filter here is for this rate demonstration. It is no instruction to delete the original observation.

## Slide 21: Operations for the next example

01

Adding or replacing a column: table["name"] = values assigns that column. An array follows row order. A Series aligns by row label, so keep labels paired with the intended observations.

02

Column arithmetic: Arithmetic on columns calculates one result per row. Series align by row label. Divide only where the denominator is valid and keep actual and predicted observations paired.

03

A separate working table: table.copy() creates a working copy. Assigning columns on this copy preserves the source table, so you can compare before and after.

**Spoken script**

Three tools for building new columns.

First, adding a column. We write table, square brackets, a new name in quotation marks, then an equals sign and the values. If the values are a plain list or array, pandas places them in row order. If they come as a Series, pandas matches them by row label. So we should keep the labels paired with the right observations.

Second, column arithmetic. When we divide one column by another, pandas does the sum row by row and gives one result per row. We divide only where the bottom number is valid. We also keep the actual values and the predicted values paired, row for row.

Third, table dot copy. It creates a separate working table. We add columns to the copy and the source table stays as it was, so we can compare before and after.

## Slide 22: Rates from recorded cost and energy

The two columns come from the same source row.

Run this cell on the supplied CSV. Read the output below the cell.

```python
priced = raw[raw["kwh"] > 0].copy()
priced["rate_ugx_per_kwh"] = priced["cost_ugx"] / priced["kwh"]
print(priced[["building", "kwh", "cost_ugx", "rate_ugx_per_kwh"]].head())
```

**Spoken script**

This cell builds the rate column, one line at a time.

Line one is priced equals raw, square brackets, raw kwh greater than zero, then dot copy. Inside the brackets the comparison keeps only the rows with positive energy. Dot copy then makes a separate working table, stored under the name priced.

Line two adds the new column, rate underscore ugx underscore per underscore kwh. Each value is cost underscore ugx divided by kwh, calculated within the same row. The unit is shillings per kilowatt hour.

Line three prints the first five rows of four columns. The double square brackets contain a list of column names, and pandas shows them in the order we wrote them.

The two columns come from the same source row. For any row you see, divide cost by kwh with a calculator and check that you get the printed rate. Run the cell and read the output.

## Slide 23: Your issued assignment

01

Open W05_student.ipynb.

02

Read every task and its input units before coding.

03

Keep the required function names and returned outputs.

04

Restart and run all cells, then save the completed notebook.

**Spoken script**

This is the assignment for the week. Open the notebook called W zero five underscore student dot i p y n b.

Read every task and its input units before you start coding. The units tell you what each number measures, such as kilowatt hours or shillings, and that helps you choose the right calculation.

Keep the required function names and returned outputs exactly as given. The checking depends on those names.

When you finish, restart the notebook and run all cells from the top. This confirms that the notebook works from start to finish. Then save the completed notebook. The next slides show the six tasks.

## Slide 24: q1: 3 marks

Load campus_energy.csv into a DataFrame called df.

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

Question one is worth three marks, and it is the first step of the notebook.

Load the file campus underscore energy dot csv into a DataFrame called df. The tool is pd dot read underscore csv with the file name, as in our worked example. The name df must be exactly this, because later questions use it.

Keep the exact names and outputs. Check the types, units and the issued brief before you move on.

## Slide 25: q2: 3 marks

Set n_meters to the number of distinct meters in the file.

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

Question two is worth three marks.

Set a variable called n underscore meters to the number of distinct meters in the file. Distinct means different. A meter appears in several rows, one for each month, so counting rows would give a bigger number. We want each meter counted once.

We used nunique earlier to count different buildings. The same tool counts different meters on the meter underscore id column.

Keep the exact names and outputs. Check the types, units and the issued brief.

## Slide 26: q3: 4 marks

Add a column cost_per_kwh to df, equal to cost_ugx / kwh.

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

Question three is worth four marks.

Add a new column called cost underscore per underscore kwh to df. Each value equals cost underscore ugx divided by kwh, calculated in the same row.

The new column answers how many shillings one kilowatt hour cost for that meter in that month. We built a column like this in the rate example, by writing df, square brackets with the new name in quotation marks, an equals sign, and then the division.

Keep the exact names and outputs. Check the types, units and the issued brief. Later questions use this column, so build it carefully.

## Slide 27: q4: 4 marks

Set high_use to the rows of df where kwh is greater than 5000.

Do this after q3 so the derived column comes along.

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

Question four is worth four marks.

Set a variable called high underscore use to the rows of df where kwh is greater than five thousand. We did this in the worked example. We write a comparison on the kwh column to get True and False answers, and then put those answers inside square brackets after df.

The slide asks us to do this after question three. The reason is that the new cost underscore per underscore kwh column then comes along with the selected rows. If we filtered first, the new column would be missing from high underscore use.

Keep the exact names and outputs. Check the types, units and the issued brief.

## Slide 28: q5: 3 marks

Set mean_cost_per_kwh to the mean of the cost_per_kwh column.

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

Question five is worth three marks.

Set a variable called mean underscore cost underscore per underscore kwh to the mean of the cost underscore per underscore kwh column. This is the column we created in question three, so question three must be done first.

The mean is the average. We select the column with df and square brackets, then add dot mean. Pandas adds up the known values and divides by how many there are. The answer has the same unit as the column, which is shillings per kilowatt hour.

Keep the exact names and outputs. Check the types, units and the issued brief.

## Slide 29: q6: 3 marks

Set peak_building to the name of the building with the highest total kwh.

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

Question six is worth three marks.

Set a variable called peak underscore building to the name of the building with the highest total kwh. Peak means the biggest.

This uses the building totals example. First group the rows by building and add up the kwh in each group. Then use idxmax on those totals. It returns the label with the largest total, which is a building name.

The answer must be the name of the building. The total energy value itself is a different thing.

Keep the exact names and outputs. Check the types, units and the issued brief.

## Slide 30: Pandas investigation submission

01

Opens: 06 Oct 2026, 11:00 Kampala

02

Deadline: 13 Oct 2026, 11:00 Kampala

03

Use your full Student Registration Number in the form.

04

Keep the submitted files and confirmation.

Open W05 assignment form

https://docs.google.com/forms/d/e/1FAIpQLSeP_Eykf3YDYN_6sbB5to0B3LX14fsujEVPhsp8UezRZXTNGw/viewform

**Spoken script**

This slide covers how you hand in your Pandas investigation. You submit through the W zero five assignment form for CML3112. The slide shows when the form opens and the deadline, so please check both there.

In the form, use your full Student Registration Number. The file you submit is your completed notebook.

After you submit, keep the submitted files and the confirmation. The confirmation is your proof that the work went in. Saving a file somewhere on your computer or in the cloud does not submit it. The form is the submission.

## Slide 31: Project preparation

01

Use the published data analysis project brief.

02

Build the evidence gradually in your project notebook.

03

Keep raw data, labelled charts, run instructions and individual contributions.

04

Published deadline: 27 Oct 2026, 11:00 Kampala

**Spoken script**

This slide is about preparing for the data analysis project. Use the published project brief. It lists what the project needs.

Build your evidence gradually in your project notebook. Work on it a little at a time during the weeks, and avoid leaving it to the last days.

Keep four things. Keep the raw data, which is the original file. Keep charts that carry labels. Keep the run instructions, which tell another person how to run your notebook. Keep a record of each person's individual contribution.

The slide shows the published deadline for CML3112, so please check it there.

## Slide 32: Week 5 quiz

01

Answer individually after the lecturer activates the quiz.

02

Available for 24 hours from activation.

03

Use your Student Registration Number and registered account.

04

Check the announced quiz closing time.

Open this week’s quiz

https://forms.gle/Ykncf1mmEbvghZgJ6

**Spoken script**

The Week 5 quiz is ready for CML3112. You answer it individually, after the lecturer activates it.

Once it is activated, it stays available for 24 hours. Check the announced closing time.

Use your Student Registration Number and your registered account. The link is on the slide.

## Slide 33: Revision and submission checklist

You can explain which observations a filter keeps and what a grouped total means.

Save your work and check the required submission files.

Point to your evidence. Save your work.

**Spoken script**

Before you leave, use this slide as your final check.

First, explain it. You can say which rows a filter keeps, and you can say what a grouped total means. If you can say these in your own words, you have met today's goal.

Second, save your work. Check which files the assignment requires, and make sure the completed notebook is saved and ready to submit.

Point to your evidence, and save your work.
