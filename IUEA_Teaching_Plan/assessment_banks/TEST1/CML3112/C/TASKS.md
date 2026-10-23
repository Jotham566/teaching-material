# CML3112 TEST1 — Take-home practical test

Individual work • 100 marks • Up to three hours from **Start test**.

**Check your personal deadline on the official test entry page. Start only when ready to work.**
The timer includes setup, internet interruptions and submission. It cannot be paused or restarted by refreshing, changing devices or reopening Colab. Your deadline is the earlier of three hours after starting or the class closing time. Colab may still allow editing afterwards, but late work is not accepted for grading.

## 1. Open your own working copy
On the entry page, enter your full name, Google account email and Student Registration Number. Use that same Google account throughout. Click **Open my test in Colab**, and work in that private editable notebook. You do not need to make a copy. Click **Connect** if shown. To resume, use the entry link with the same email and Student Registration Number; it opens the same saved notebook without restarting the timer.

## 2. Load the data
Check the identity cell near the top. Tell your lecturer immediately if the details are wrong; do not change the supplied course, test or allocation settings. Run the identity cell using the triangle beside it. Then run **Load the supplied CSV and Python libraries**. In the issued notebook this creates `engineering_data.csv` automatically; no separate CSV upload is needed. Wait for the preview and row count. After a runtime reset, rerun these setup cells before your work. If using a backup notebook without an embedded CSV setup cell, upload your assigned `engineering_data.csv` through Colab's folder icon first.

## 3. Complete the questions
Work from top to bottom. Read each question, write your code in its code cell and run it. Keep supplied function names and required output formats unchanged. Use pandas as instructed. Complete the eight coding tasks using pandas, matplotlib and ordinary Python. There are no interpretation choices or written report. Save regularly using **File → Save**.

## 4. Submit — allow at least 20 minutes
1. Run your completed cells, check the results and save. Submit your completed work even if some questions are unfinished.
2. Run the final **Submit your test** cell. Choose the same Google account when asked to authorize access. This access lets the helper save a notebook snapshot and share it privately with your lecturer.
3. Click **Submit test** and wait for the generated form link. If the browser does not open it automatically, click the displayed link.
4. Open the form. Check the email shown; use **Switch account** if it is wrong. Check your full name and Student Registration Number. Leave the prefilled allocation code, snapshot ID and hash unchanged. Tick the email confirmation box, then press **Submit** before your personal deadline.
5. Wait for the form confirmation. Keep the saved snapshot unchanged in Drive until marks are released.

**The notebook button alone does not complete submission: you must submit the form too.** Do not separately upload a CSV, PDF, ZIP or screenshots. A form confirmation acknowledges receipt; it does not make a late submission valid. Marks are calculated after the test. If you replace your submission, submit a complete new snapshot and its form before the same deadline.

## If something fails
Record the error and contact your lecturer immediately, before the deadline. Do not create a second identity or use another student's files. If Colab disconnects, reconnect and rerun setup; your saved notebook remains in Drive, but runtime variables may need to be recreated. The timer continues.

No AI-generated solutions, collaboration, messaging or copied answers.

## Coding tasks and time plan
Setup: 10 minutes. Tasks 1–8: about 135 minutes. Check and save: 15 minutes. Submit: 20 minutes. Total: 180 minutes. These are planning estimates; your personal deadline is authoritative.

Use only pandas, matplotlib and ordinary Python. No modelling, scikit-learn, SQL, written report or multiple-choice answers. All 100 marks come from coding.

Each question has a supplied function header and a separate supplied run cell. Write your answer inside the function, indented by four spaces. The input argument contains rows from the CSV; the first supplied line converts these to a DataFrame. Do not change function names or returned dictionary keys. `return` sends your answer to the caller; `print` only displays it. The run cell calls the function with your dataset.

The grader also calls each function independently on other values with the same columns and cleaning rules. Use its input argument, not a global table or typed-in final answer. An unfinished cleaning function may prevent later demonstration cells running, but later functions can still earn marks independently. Submit partial work before the deadline.


## Task 1: EDA before cleaning — 10 marks

Use the original data, including its errors. Calculate and return:
- `preview`: the first five rows as a DataFrame (2 marks).
- `rows`: number of rows; `columns`: number of columns (2 marks each).
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