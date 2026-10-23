# CML3111 Test 1 — Take-home practical
**Individual work · 100 marks · 3 hours from Start test**

1. Run **Check details and countdown**. **Double-check your full name, Student ID/ Registration Number, and email.** Use the same Google email in Colab and the submission form. If any detail is wrong, contact your lecturer before continuing; do not create another identity.
2. Run **Prepare CSV and libraries**, then write your own pandas CSV-reading code in Task 1.
3. Complete Tasks 1–8 in order. Keep `raw_data` unchanged; Task 3 produces `cleaned_data`. Save regularly.
4. Run **Submit your test**, click the button, open its form, **check your name, Student ID/ Registration Number, and email again**, then press **Submit**. Wait for confirmation.

The timer includes setup, interruptions and submission. It ends at your personal deadline or the class cutoff, whichever comes first. Resume with the same entry link, email and registration number; the timer does not restart.

No AI-generated answers or collaboration. If you change a support cell, use **Edit → Undo**. If submission fails, contact your lecturer before the deadline.

## Coding tasks and time plan
10 minutes setup · 135 coding · 15 checking · 20 submitting.

Use pandas, matplotlib and ordinary Python. Work from top to bottom in the answer cells. Replace `None` with your calculation; it means “not completed yet”. Follow the comments, run each cell and check its output. You may add code cells, but keep the requested result names. Only Task 7 requires a function.

Cells labelled **Do not edit this cell** are supplied setup or submission tools: run them, but do not change or delete them. In answer cells, keep lines marked **Do not edit** unchanged.


## Task 1: Read and inspect the raw data — 20 marks

Read `engineering_data.csv` with pandas using `file_path`; name the DataFrame `raw_data`. Keep it unchanged throughout the test.
Complete the named answers below:
- `first_rows`: first 5 rows using `.head()`; `last_rows`: last 5 using `.tail()` (1 mark each).
- `data_shape`: `.shape`; `row_count`: `len(raw_data)` (1 mark each).
- `target_dtype`: the `target` column's `.dtype` (2). A column has `.dtype`; a whole DataFrame has `.dtypes`.
- Run `raw_data.info()` to display column types and non-missing counts (2). It prints a summary; do not assign its result.
- `numeric_summary`: `.describe()` for numeric columns (2).
- `missing_counts`: missing count for each column, using `.isna()` or `.isnull()` followed by `.sum()` (2).
- `duplicate_count`: number of repeated `record_id` values AFTER the first occurrence (2).
- `invalid_records`: rows where `target` is missing OR `load_pct` is below 0 OR above 100 (4). This is inspection only: do not remove these rows yet.
Reading the correct CSV into `raw_data` earns 2 marks. Display your answers to check them.

## Task 2: Visualisation before cleaning — 10 marks

Using `raw_data`, create a scatter chart of `load_pct` (horizontal) against `target` (vertical). Do not clean or fill values first.
Use `figure, axes = plt.subplots()`, then either `axes.scatter(...)` or `raw_data.plot.scatter(x=..., y=..., ax=axes)`.
Add a title, horizontal label including %, and vertical label including the target unit shown above. Keep `before_figure = figure`: it saves this chart for marking.
Marks: correct points 4; title 2; horizontal label 2; vertical label and unit 2.

## Task 3: Clean the data — 20 marks

Start with a copy of `raw_data`; call it `cleaned_data`. Apply these rules in order:
1. Keep the first row for each `record_id`.
2. Remove rows with missing `target` or `load_pct` outside 0–100. Keep 0 and 100.
3. Find the median `ambient_c` in the retained rows. Fill only missing temperatures with this median.
Keep the same five columns and row order. Do not alter known values or equipment labels. Display the cleaned table and check for missing values, duplicates and invalid loads again.
Marks: 4 for each correctly cleaned column. Index numbers do not matter.

## Task 4: Visualisation after cleaning — 10 marks

Repeat Task 2 using `cleaned_data`. Use a new figure with the same two columns and units, and a title such as “After cleaning”. Keep `after_figure = figure`: it saves this chart for marking.
Marks: correct cleaned points 4; title 2; horizontal label 2; vertical label and unit 2. No written comparison is required.

## Task 5: Calculate statistics — 15 marks

Using `cleaned_data`, calculate `target_mean`, `target_sum`, `target_median`, `target_count` and `target_std` from `target`.
Also calculate and display `equipment_modes`: all most frequent `equipment_id` values using `.mode()`. Each of these six answers earns 2.5 marks.
Use pandas' `.std()` with its default sample standard deviation. Do not round answers. Mode means most frequent; `.mode()` returns every tied mode. These are descriptive calculations, not safety conclusions.

## Task 6: Group and aggregate — 10 marks

Group `cleaned_data` by `equipment_id`. Use `groupby` and `agg` to calculate the mean and count of `target` for each equipment. Store the DataFrame as `equipment_summary` and display it.
Its index must contain equipment IDs and its two columns must be named `mean` and `count`. Keep full precision. Group order does not affect marks (5 marks per column).

## Task 7: Reuse your statistics in one function — 5 marks

Turn three calculations from Task 5 into a reusable function. The supplied inputs are a DataFrame (`table`) and a column name (`column_name`).
Return a dictionary with keys `mean`, `sum`, `median`, calculated from `table[column_name]`. Replace the three `None` values. Use the inputs rather than a fixed column or the global `cleaned_data`.
Then call your function for `cleaned_data` and `"target"`, and again for `"load_pct"`. Display both results. The grader tests the function with other numeric values (5 marks).

## Task 8: Conditions and a loop — 10 marks

Use a `for` loop over `cleaned_data["load_pct"]`. Inside it, use `if`, `elif`, `else` to count loads in these categories:
- `low`: below 40;
- `medium`: 40 to 75 inclusive;
- `high`: above 75.
Update the supplied `load_band_counts` dictionary and display it after the loop. Do not type the final counts by hand. For loads `[20, 40, 75, 90]`, the counts would be `{"low": 1, "medium": 2, "high": 1}`.
These are test categories, not safety limits. Correct counts: 6 marks; a loop: 2; conditions inside that loop: 2. No second function is required.