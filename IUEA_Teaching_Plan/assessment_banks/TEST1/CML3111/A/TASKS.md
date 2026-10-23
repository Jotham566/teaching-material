# CML3111 Test 1 — Take-home practical
**Individual work · 100 marks · 3 hours from Start test**

1. Run **Check details and countdown**, then **Prepare CSV and libraries**.
2. In Task 1, write the pandas code to read the file into `raw_data`.
3. Complete Tasks 1–8 in order. Task 3 produces `cleaned_data`. Save regularly.
4. Run **Submit your test**, click the button, then open its form and press **Submit**. Wait for confirmation.

The timer includes setup, interruptions and submission. It stops at your personal deadline or the class cutoff, whichever comes first. To resume, use the same entry link, email and registration number; your timer does not restart.

No AI-generated answers or collaboration. If a support cell is changed or deleted, use **Edit → Undo**. If submission fails, contact your lecturer before the deadline.

## Coding tasks and time plan
10 minutes setup · 135 coding · 15 checking · 20 submitting.

Use pandas, matplotlib and ordinary Python. Write only in the answer cells. Run the cells labelled “Run only”; do not edit them.

Keep function names and return keys unchanged. The supplied first line turns input records into a DataFrame. Calculate from that input; the grader checks other values too. Later functions can earn marks even if cleaning is unfinished.


## Task 1: EDA before cleaning — 10 marks

First read `engineering_data.csv` with pandas, using `file_path`, and store the table in `raw_data` (2 marks). The file is in the current folder, so its name is the relative file path.

Then use the original data, including its errors. Calculate and return:
- `preview`: the first five rows as a DataFrame (2 marks).
- `rows` and `columns`: the two dimensions (2 marks together).
- `missing`: missing-value count for each column as a Series (2 marks).
- `duplicates`: repeated record IDs after the first occurrence (2 marks).
The return dictionary is supplied. Replace each `None` with your calculation. Do not clean this table. The supplied run cell also calls `info()` to show data types and recorded counts, and `describe()` to show numeric summaries; these inspection commands carry no extra marks.

## Task 2: Visualisation before cleaning — 10 marks

Create one scatter chart from the original table: `load_pct` on the horizontal axis and `target` on the vertical axis. Keep repeated observations and invalid loads in this BEFORE chart. Matplotlib does not draw pairs with a missing coordinate; do not fill or clean the data for this chart.
Return the supplied `figure`. Plot the correct points (4 marks), add the supplied `chart_title` (2), label the horizontal axis with load and percent (2), and label the vertical axis with target and the supplied `target_unit` (2). Colour and styling are your choice.

## Task 3: Clean the data — 20 marks

Work on a copy. Apply these rules IN ORDER:
1. Keep the first occurrence of each `record_id`.
2. Exclude rows with a missing `target` or `load_pct` outside 0–100 inclusive. Keep valid boundary values 0 and 100.
3. Calculate the median `ambient_c` from the retained rows, ignoring missing values. Fill only missing ambient temperatures with this median.
Return the cleaned DataFrame with the same five columns and original row order. Do not change equipment labels or known measurements. Index numbers do not matter. Do not remove rows merely because they have a high target.
The grader gives 4 marks for each correctly retained column (record IDs, equipment IDs, loads, temperatures and targets).

## Task 4: Visualisation after cleaning — 10 marks

The input now contains CLEANED observations. Make the same load/target scatter chart so it can be compared with the BEFORE chart. Use the supplied title and target unit. Return a Figure, not an image filename or text.
Correct cleaned points: 4 marks; title: 2; horizontal axis with percent: 2; vertical axis with target units: 2. You may reuse or call your Task 2 function. No written comparison is required.

## Task 5: Calculate statistics — 15 marks

Use CLEANED data. Return the following six entries in the supplied dictionary (2.5 marks each):
- `mean`, `sum`, `median`, `count`, `std`: calculated from the `target` column.
- `mode`: ALL most frequent equipment IDs, as a list in alphabetical order, calculated from `equipment_id`.
Use pandas' sample standard deviation (`.std()`, default `ddof=1`). Do not round returned answers. The sum is a descriptive calculation across observations, not a total-energy measure or a safety conclusion.
**Reference provided for this test:** mean is the average; sum adds values; median is the middle value; count counts recorded values; standard deviation measures spread. `values.std()` returns sample standard deviation. Mode means most frequent: `labels.mode().tolist()` returns ALL tied modes as a list. For labels `A, A, B, B, C`, it returns `["A", "B"]`. You do not need to derive a statistical formula.

## Task 6: Group and aggregate — 15 marks

Group CLEANED observations by `equipment_id`. Use `groupby` and `agg` to calculate the `mean`, `sum` and `count` of `target` for each equipment ID (5 marks per column).
Return a DataFrame whose index contains equipment IDs and whose columns are named `mean`, `sum`, `count`. Equipment order does not affect marks. Keep full numerical precision.
Reference: `table.groupby("group_column")["numeric_column"].agg(["mean", "sum", "count"])` applies several calculations to each group. Replace the placeholder column names with the required columns.

## Task 7: A function with conditions — 10 marks

Write a reusable function using `if`, `elif`, `else` and `return`. Its input is one valid numeric load percentage from the same dataset. Return exactly:
- `"low"` if load is below 40;
- `"medium"` if load is from 40 through 75 inclusive;
- `"high"` if load is above 75.
These are test categories, not engineering safety limits. Check both boundary values: 40 and 75 must return `"medium"`. Return the label rather than only printing it. The supplied run cell uses a load from your cleaned CSV.

## Task 8: A loop using the same data — 10 marks

Use a `for` loop to visit every load in the supplied list. Call `classify_load` for each load and increment the matching counter in the supplied dictionary. Return the dictionary after the loop. An empty list must return all three counts as zero.
The run cell gets this list from the CLEANED CSV. For `[20, 40, 75, 90]`, the result is `{"low": 1, "medium": 2, "high": 1}`. Do not type the final dataset counts by hand. If Task 7 is unfinished, you may put the same conditions inside this loop for partial credit.