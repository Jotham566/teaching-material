# ML10 Instructor guide: Cleaning without hiding evidence

Private. Keep this file out of the student folder.

**Objective.** By the end: you can count missing values and duplicates, remove an exact duplicate on a copy, and save a cleaning log.

**Question of the day.** What is wrong with this table, and what did I change?

Prerequisite: ML09 Mean, median, range and proportions.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

## Block A. Count the problems

A tiny table has two sets of trouble. Count them before you change anything.

Ask for the prediction first: Predict how many missing prices and how many duplicate rows the raw table has.

```python
import pandas as pd
raw = pd.DataFrame({"id": [1, 2, 2, 3], "price": [1000, None, None, 3000]})
missing = raw["price"].isna().sum()
dupes = raw.duplicated().sum()
clean = raw.drop_duplicates().copy()
print(missing, dupes, len(clean))
print(clean["price"].mean())
```

Correct result: The cell prints 2, 1 and 3, then 2000.0. isna marks each blank as True and sum counts them. duplicated marks the repeated row and drop_duplicates removes it. copy makes a separate table, so raw stays unchanged. The mean of 2000.0 uses the two prices that exist and ignores the missing one.

Investigate, with answers:

- Why do we work on a copy? Answer: The raw table is the evidence. If a change is wrong we can start again from it.
- Why not replace the missing price with 0? Answer: Zero means a free item. A missing price is unknown, and zero would pull the mean down.

Modify: Print how many prices are still missing in clean. Answer: One price is still missing.

```python
still_missing = clean["price"].isna().sum()
```

## Block B. Save a cleaning log

Write down what you found as a small table and save it as a file.

Ask for the prediction first: Predict how many rows and columns the saved log has after you read it back.

```python
log = pd.DataFrame({"step": ["raw rows", "duplicate removed", "price still missing"], "count": [4, 1, 1]})
log.to_csv("cleaning_log.csv", index=False)
log_back = pd.read_csv("cleaning_log.csv")
print(log_back)
print(log_back.shape)
```

Correct result: The log has 3 rows and 2 columns. to_csv writes the table into cleaning_log.csv. index=False stops pandas adding a column of row numbers. Reading the file back proves that it saved. The log lists the raw row count and each change, so a reader can repeat the cleaning.

Investigate, with answers:

- What would the log look like with index=False left out? Answer: The file would carry an extra unnamed column of row numbers.
- Who is the cleaning log for? Answer: Anyone who needs to check or repeat your work, including you next week.

Modify: Add the step final rows with a count of 3 and save again. Answer: The log has 4 rows.

```python
log = pd.DataFrame({"step": ["raw rows", "duplicate removed", "price still missing", "final rows"], "count": [4, 1, 1, 3]})
log.to_csv("cleaning_log.csv", index=False)
log_back = pd.read_csv("cleaning_log.csv")
```

## Make: reference

```python
import pandas as pd
my_log = pd.DataFrame({"step": ["raw rows", "duplicate removed", "price missing"], "count": [4, 1, 1]})
my_log.to_csv("my_log.csv", index=False)
back = pd.read_csv("my_log.csv")
print(back)
# Zero would say the item was free. A missing price means the price is unknown.
```

Evidence to collect: ML10.ipynb with the counts 2 missing, 1 duplicate, the saved log, and the explanation about zero.

## Misconceptions to listen for

- Missing values should be filled with 0.
- Two equal rows are always a mistake.
- Cleaning means changing the original file.

## Questions to ask, with expected answers

- Why can two equal rows be genuine? Expected: Two customers can buy the same item at the same price on the same day.
- What is the first thing to do with a messy file? Expected: Keep the raw copy, then count the problems.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
