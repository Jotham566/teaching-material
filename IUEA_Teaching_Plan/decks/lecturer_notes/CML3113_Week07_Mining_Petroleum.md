# CML3113 Week 7

## Slide 1: Preparing for Practical Test 1

A6 and Quiz 6 are waived for this cohort. This is ungraded practical revision. No assignment upload or quiz response is required. Previous submissions remain on record but do not count towards coursework marks.
A6 and Quiz 6 are waived for this cohort. This is ungraded practical revision. No assignment upload or quiz response is required. Previous submissions remain on record but do not count towards coursework marks.
Send this deck and CML3113_Test1_practice.csv together several days before Test 1. The CSV contains synthetic practice readings. All worked data examples use this file. Practice is ungraded. The later test-day section uses different files from the timed portal.

## Slide 2: Your revision files

Share the CSV as a separate attachment beside the PPTX. Students do not need an assessment packet or grader. The practice CSV is intentionally small so they can check every calculation by hand.

## Slide 3: Practice and test-day files

The clearly named practice file avoids confusing it with engineering_data.csv. Portal timing applies to test downloads, not the practice attachment. The repository remains public by the lecturer’s decision, so portal timing is not a claim that public repository files are private.

## Slide 4: A new practice notebook in Colab

A notebook holds code cells and output. Later cells use names created by earlier cells. Confirm the name and saved status. Students do not need a test notebook for this revision.

## Slide 5: Uploading your practice CSV

The Files panel uploads to the temporary session, not into the notebook itself. A FileNotFoundError usually means the file was not uploaded, its filename differs, or the session reset. Do not upload the PPTX into Colab. Avoid a duplicate download name ending in (1).

## Slide 6: What each column means

These are synthetic teaching values, not measurements from an operating site. A row contains one measurement and its associated input conditions. target is a column name, not a unit. M1 and M2 are invented equipment identifiers. read_csv displays missing numeric values as NaN.

## Slide 7: Reading a CSV with pandas

A DataFrame is a table with named columns. The equals sign assigns a result to a name. CSV means comma-separated values. Python is case-sensitive, including the filename.

## Slide 8: Loading the supplied practice file

Line 1 imports pandas. Line 2 stores the exact filename. Line 3 reads it into source. The last two lines show the table and its row count. No test data is involved.

Result from the supplied example
reading machine  load  target  ambient
0        1      M1    20    10.0     20.0
1        2      M1    40    20.0      NaN
2        3      M2    60    30.0     30.0
3        4      M2    80    40.0     40.0
4        1      M1    20    10.0     20.0
5        5      M2    50     NaN     90.0
6        6      M2   120    90.0    100.0
7

## Slide 9: The practice cleaning rules

The file has seven rows: readings 1, 2, 3, 4, a repeated 1, reading 5 with no target, and reading 6 with load 120. The four retained readings have targets 10, 20, 30 and 40. These practice rules are explicit; students must read the actual test rules on test day.

## Slide 10: Removing duplicates and missing targets

The list ["target"] identifies the column to inspect for missing values. Do not remove a row just because ambient is missing: its replacement comes later. The duplicate reading 1 repeats the first row.

## Slide 11: The first two cleaning steps

First, seven rows become six after dropping the repeated reading 1. Then six become five after removing reading 5. source still has seven rows. raw is a new working table.

Result from the supplied example
6
5

## Slide 12: Selecting a valid load range

Both limits are included by default. A missing load would also fail this check. The row labels can have gaps after filtering; they are not the reading identifiers.

## Slide 13: Keeping the valid loads

Line 1 checks load for each remaining row. Line 2 retains the True rows, leaving four records. Line 3 displays their targets. All later summaries and charts use these four records.

Result from the supplied example
[10.0, 20.0, 30.0, 40.0]

## Slide 14: The median and missing ambient values

The original rejected rows include high ambient values. Using them would change the replacement. The retained reading 2 has no ambient value, so it receives 30. Assign the filled Series back to the ambient column.

## Slide 15: Filling the missing ambient value

The median is 30. Reading 2 receives 30. The final ambient values in row order are 20, 30, 30, 40. source remains available with all seven original rows.

Result from the supplied example
30.0
[20.0, 30.0, 30.0, 40.0]

## Slide 16: Selecting, averaging and grouping

Explain the whole-table mean by hand first: (10 + 20 + 30 + 40) / 4 = 25. For M1, (10 + 20) / 2 = 15. For M2, (30 + 40) / 2 = 35. A group mean is a separate calculation for each label.

## Slide 17: Overall mean and machine means

Line 1 averages all four targets. Line 2 groups rows by machine, selects target and averages within each group. Lines 3 and 4 display the results. The calculation does not change raw.

Result from the supplied example
25.0
machine
M1    15.0
M2    35.0
Name: target, dtype: float64

## Slide 18: Practice: calculate a changed mean

The task is a hand calculation, avoiding hidden changes to the data used by subsequent examples. M1 contains 10 and 20. M2 would contain 30 and 60.

## Slide 19: Practice answer

Only M2 contains the changed reading. This is a hypothetical calculation. The subsequent chart still uses the four original retained targets.

## Slide 20: Charts and numerical findings

A scatter point combines values from the same row. Four points are enough to rehearse the commands, but too few to justify a general engineering conclusion. Revise the other chart types from earlier lessons as well. The test specifies which charts it requires.

## Slide 21: A labelled practice chart

Read the coordinates of the first and last points. Target increases as load increases in this invented example. Do not claim this proves that load caused the increase. Reuse the original raw table, not dirty or clean.

Result from the supplied example
Values are stored for the next step; this cell does not print a result.

## Slide 22: Histograms and group-mean bars

A histogram groups numeric values into intervals, whereas a bar chart groups by categories. Use the same cleaned four-row table. The following histogram has two bins: 0 to below 25, and 25 to 50 including the final edge.

## Slide 23: A target histogram

Targets 10 and 20 fall in the first bin. Targets 30 and 40 fall in the second. There are four readings in total. show displays and finishes the chart in Colab.

Result from the supplied example
Values are stored for the next step; this cell does not print a result.

## Slide 24: Bar labels and heights

Recall the earlier groupby calculation. A Series has an index and values. Here the index is the machine name rather than a numeric row label.

## Slide 25: Machine-mean bars

M1 averages readings 1 and 2, giving 15. M2 averages readings 3 and 4, giving 35. These synthetic means describe this small sample and do not establish causation.

Result from the supplied example
Values are stored for the next step; this cell does not print a result.

## Slide 26: Functions and returned answers

The automated grader calls functions with other records. A pasted fixed answer can match a displayed example and still fail for another input. print displays a value but does not replace return. The following practice function is unrelated to the assessed function names.

## Slide 27: A practice function

The argument values receives a column from the practice CSV. pd.Series represents it as one labelled column. mean calculates its average. float converts the result to a Python decimal number. return sends it back to the caller. The first call averages targets 10, 20, 30, 40. The second averages loads 20, 40, 60, 80. print displays each returned result.

Result from the supplied example
25.0
50.0

## Slide 28: Practice columns and test columns

The practice CSV stays unchanged. Read each pair aloud. A record identifier labels an observation; it is not a timestamp. The test notebook explains its column names before the tasks. The next examples use practice names only.

## Slide 29: Tables and lists of records

Use the retained raw table from the earlier practice cleaning. Each dictionary has reading, machine, load, target and ambient keys. The list preserves row order. These retained rows have no missing values. The supplied test helper also handles missing values when converting the original input.

## Slide 30: The retained rows as records

First, convert the four cleaned rows into a list. The first dictionary describes M1 at load 20 with target 10 and ambient 20. The integer row labels of the DataFrame are not a column in these dictionaries. Rebuilding a DataFrame gives the same four measurements.

Result from the supplied example
{'reading': 1, 'machine': 'M1', 'load': 20, 'target': 10.0, 'ambient': 20.0}
4

## Slide 31: Missing values during conversion

Explain these as steps inside a provided helper. astype(object) changes the storage type, not the measured quantities. Missing numeric CSV cells are normally NaN; the function interface uses None. The next practice helper mirrors this supplied convenience.

## Slide 32: A helper for the original CSV

The helper accepts any table. It uses that argument instead of a global variable. The return statement gives a list back to the caller. original_records still contains the duplicate, the missing target and the invalid load.

Result from the supplied example
7

## Slide 33: A cleaning function follows the same steps

This combines already practised operations. Students should explain the input, each row removal, the replacement median and the return type. No marks depend on memorising the four practice target values.

## Slide 34: The complete practice cleaning function

Trace seven input rows to six after removing the repeated reading, five after dropping the missing target, and four after checking load. The retained known ambient values are 20, 30 and 40. Their median is 30. Returning through as_records preserves the column names and row order.

Result from the supplied example
Values are stored for the next step; this cell does not print a result.

## Slide 35: Calling the cleaning function

The function call returns a new list assigned to cleaned_records. The second retained record originally had missing ambient. The two successive bracket operations first choose a record, then its ambient field.

Result from the supplied example
7
4
30.0

## Slide 36: Summary values inside a dictionary

Here the targets are 10, 20, 30, 40. Count is 4, mean 25, minimum 10 and maximum 40. group_means maps M1 to 15 and M2 to 35. Unlike to_dict("records") on a DataFrame, to_dict() on a Series produces one mapping.

## Slide 37: A summary function

Each quoted key names one output. Colons connect keys to values. Commas separate entries. float converts a pandas numerical result into a Python decimal number. A multiline dictionary may continue until its closing brace. Keep full numerical precision.

Result from the supplied example
Values are stored for the next step; this cell does not print a result.

## Slide 38: Reading the returned summary

First call the function with the retained records. Then retrieve results from its returned dictionary. Printed results help you check your work, but the grader receives the returned dictionary itself.

Result from the supplied example
4 25.0
10.0 40.0
{'M1': 15.0, 'M2': 35.0}

## Slide 39: A Figure is an object you can return

Displaying a chart is different from returning a chart. The test asks for actual Figure objects in a list, in scatter, bar, histogram order. Students should not return filenames, screenshots or dictionaries describing charts.

## Slide 40: A function returning a scatter Figure

The input table contains cleaned rows. The scatter combines load and target from each row. All chart labels belong to ax. The return statement returns fig, not ax. This function does not modify the input.

Result from the supplied example
Values are stored for the next step; this cell does not print a result.

## Slide 41: Alphabetical order for group means

The index of the grouped Series is its machine labels. Sorting by index sorts those labels, not the mean values. Sorting heights independently would attach the wrong value to a machine.

## Slide 42: A function returning ordered bars

Compute the means first, then put their labels in alphabetical order. Pass labels and corresponding means to bar. Return the Figure object. With more groups, the same function still calculates all group means.

Result from the supplied example
Values are stored for the next step; this cell does not print a result.

## Slide 43: Ten histogram bins

Ten bins means ten intervals, not ten readings. The first bin starts at 10 and the last ends at 40. The rightmost edge is included. There are only four readings, so many bins are empty. Do not reuse the earlier fixed boundaries [0, 25, 50] for the test.

## Slide 44: A function returning a ten-bin histogram

A histogram Figure contains rectangular bars, including bars with zero height. The heights sum to the number of records. The unit belongs on the target axis; the other axis counts observations.

Result from the supplied example
Values are stored for the next step; this cell does not print a result.

## Slide 45: Returning the three Figures in order

The square brackets form a list of the three returned objects. A helper must be defined before this function is called. The actual test requires a build_charts function; helpers are allowed. The chart list is the returned answer, while show displays it for inspection.

Result from the supplied example
Values are stored for the next step; this cell does not print a result.

## Slide 46: The gap between group means

Emphasise the difference between a group mean and an individual record. Use group means for group_gap. Its unit is the target unit. The observed gap does not establish why the equipment differs.

## Slide 47: Calculating the group gap

The means Series contains 15 and 35. Taking their maximum and minimum produces a gap of 20. This is an observed difference in these synthetic data, not a recommendation to replace equipment.

Result from the supplied example
20.0

## Slide 48: A finding contains a value and a unit

A nested dictionary is a dictionary containing another dictionary. Keys value and unit are literal names required by the test. Correct unit spellings such as °C, deg C and degrees C are equivalent. A quantity measured in kWh/t cannot be labelled kW.

## Slide 49: A helper for a value with its unit

The first argument is the number. The second is its unit string. The helper constructs the inner dictionary. The next function uses it to give every finding an explicit unit.

Result from the supplied example
25.0 kWh/t

## Slide 50: Returning the five practice findings

Reuse the summary calculation to avoid inconsistent values. pd.Series turns the group_means dictionary into a Series whose index is the machine labels. Calculate the gap on that Series. The returned outer dictionary has five exact keys. Each entry is an inner dictionary returned by with_unit.

Result from the supplied example
Values are stored for the next step; this cell does not print a result.

## Slide 51: Checking the returned findings

count returns {value: 4, unit: observations}. mean returns {value: 25.0, unit: the cohort target unit}. group_gap returns value 20 with that same target unit. To get just the gap number, use findings["group_gap"]["value"].

Result from the supplied example
{'value': 4, 'unit': 'observations'}
{'value': 25.0, 'unit': 'kWh/t'}
{'value': 20.0, 'unit': 'kWh/t'}

## Slide 52: Practice: another input to your functions

[:2] is a slice taking positions 0 and 1. Demonstrate calls revision_clean(original_records[:2]), then pass that result to each later function. There is no assessment submission for this practice.

## Slide 53: Practice answer

[:2] is a slice taking positions 0 and 1. Demonstrate calls revision_clean(original_records[:2]), then pass that result to each later function. There is no assessment submission for this practice.

## Slide 54: What a filled value can and cannot tell us

Ask which ambient reading was actually missing: reading 2. Filling it with 30 does not prove that the true temperature was 30. Keeping source lets us distinguish recorded and estimated values.

## Slide 55: An identifier is not a clock

Reading 4 is not evidence of hour 4. An ID can be assigned during collection or import without representing time. Likewise, M2 having a higher sample mean does not prove it is faulty. Do not infer causes or safety decisions from this teaching dataset.

## Slide 56: Test 1 revision checklist

Practice outputs: four rows, overall target mean 25, machine means 15 and 35, ambient median 30. The test supplies its own function names, return formats and rules. Do not hard-code these practice values.

## Slide 57: Recording interpretation answers

DECISIONS is a Python dictionary in the notebook. Its keys identify questions and its string values hold selected option letters. Use the labels printed in that question. A choice label is unrelated to file allocation. No student should select a paper version or edit the internal allocation cell.

## Slide 58: A dictionary entry for a practice question

This is a syntax demonstration, not an assessed answer. Explain the braces, quoted key, colon and quoted value. In the actual test, edit the existing question keys instead of replacing them with practice. Students must choose their own option by reading the question.

Result from the supplied example
B

## Slide 59: Test-day instructions

Pause at this boundary when reviewing in advance. The remaining slides are procedural instructions, not additional practice tasks. No practice file should be submitted to the test form.

## Slide 60: Your test files on test day

The page assigns files automatically. Students do not choose a version. Re-entering the same registration number and Google email retrieves the same allocation. The page can be opened in advance, but downloads are available only during the authorised test window. A phone scan is useful for opening the page, but students must download and use both files on their laptop. Students never choose a test version.

## Slide 61: Opening the notebook and CSV

A notebook upload does not include its data. Show the folder icon, then Upload. Wait until engineering_data.csv appears. Do not upload a ZIP. The portal prefills the identity cell; students check it and run it before later cells. The final submission cell contains an internal allocation code and is collapsed for clarity. Keep it unchanged.

## Slide 62: One notebook contains all answers

A function is a named block of code. The grader calls that function with different records, so it must calculate from its argument. DECISIONS is a dictionary pairing each question identifier with one option letter. Use a non-assessed demonstration such as {"practice": "B"}. No separate report or prose answer section is required.

## Slide 63: How the 100 marks are allocated

Explain that all marks come from the published checks. Correct code on unseen inputs earns coding marks. Each of the six interpretation choices earns 5 marks. Test 1 contributes 15 points and Test 2 contributes 20 points to the semester total. For example, 80/100 in Test 1 contributes 12 semester points. Partial marks are available for independently checked outputs; charts and cleaning each have a complete contract.

## Slide 64: Order of work

Test 1: duplicate removal keeps the first occurrence. Exclude a missing target or invalid load. Only then calculate the retained ambient median. Test 2: row filters are supplied, but missing ambient values remain. A pipeline learns the median from the training partition and reuses it for validation. Fitting a median on all rows leaks evaluation information. Do not reveal assessed option answers during the test.

## Slide 65: The three-hour session

Announce the actual start and close time displayed by the form. These periods total 180 minutes. Code execution is allowed during checking. Report internet or runtime problems immediately. Record incidents with the affected learner and time. Do not silently treat a failed upload as a submitted test.

## Slide 66: Before submitting

A fresh session has no variables from earlier runs. This exposes cells that depend on stale values or an incorrect order. The supplied CSV example cell calls the implemented functions. The final submission cell creates a button. Clicking it prepares a separate snapshot of the current notebook in Drive; later edits to the working notebook do not change that snapshot. Students must open the generated form link and press Submit. The button alone is not a completed submission.

## Slide 67: Submission and confirmation

Demonstrate the final button using a rehearsal notebook. The button privately shares a saved snapshot with the lecturer and fills the form fields. Tick the form’s email confirmation box before pressing Submit. Do not type snapshot IDs manually. The form records the verified Google email; it must be the same account that owns the snapshot. A new attempt requires clicking the notebook button again and submitting its new form link. The latest on-time attempt is considered; technical or identity errors remain pending. Earlier attempts are retained.

## Slide 68: How grading works

Grades are calculated in a batch on the lecturer’s Mac after the test. The Mac can be off during submission. Google Forms and Drive collect the snapshots. Before admitting students, rehearse the entry page, two downloads, notebook button and form confirmation. After the test, export the batch and run Grade_Tests.command with Docker running. A receipt is not a grade. A genuine zero is distinct from pending or infrastructure failure. The attendee register is built from submissions; without an enrolled roster it cannot identify absentees.