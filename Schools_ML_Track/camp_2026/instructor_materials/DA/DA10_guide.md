# DA10 Instructor guide: Cleaning without hiding evidence

Private. Keep this file out of the student folder.

**Objective.** By the end: you can find missing values and duplicates, remove the duplicates on a copy, and save a cleaning log that says what you did.

**Question of the day.** What is wrong with the raw Sunrise sales file, and how many rows does each problem touch?

**Where this is used.** Exports from tills often hold duplicates, blanks and typing slips. Good analysts keep a log of every fix so the owner can trust the result. How many problems can you find before you fix a single one?

Prerequisite: DA09 Sort, group, mean and median.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

## Block A. Missing values and duplicates in a small table

Keep the raw table unchanged and work on a copy. isna marks missing cells True. Adding the True values counts them. drop_duplicates removes rows that repeat another row exactly.

Ask for the prediction first: Predict how many missing prices there are and how many rows stay after the duplicate is removed.

```python
import pandas as pd
raw = pd.DataFrame({"id": [1, 2, 2, 3], "price": [1000, None, None, 3000]})
clean = raw.drop_duplicates().copy()
print(raw["price"].isna().sum())
print(len(clean))
print(clean["price"].mean())
```

Correct result: The raw table has 2 missing prices. After the duplicate row is removed, 3 rows stay and one price is still missing. The mean of the two known prices is 2000. The missing price is unknown and is not free.

Investigate, with answers:

- Why would replacing the missing price with 0 change the meaning? Answer: Zero says the item was free. The truth is that nobody recorded the price.
- Could two identical rows be real separate sales? Answer: Yes, if two customers bought the same thing. Here the repeated id shows it is a copy.

Modify: Count how many rows in clean still have a missing price. Answer: One.

```python
still_missing = clean["price"].isna().sum()
```

## Block B. The raw Sunrise file

sunrise_sales_raw.csv is the Sunrise sales as an untidy export. Count the problems. to_csv saves a table to a file. index=False stops pandas adding an extra column of row numbers.

Ask for the prediction first: Predict how many duplicate rows the file holds. The clean version has 1513 sales.

```python
raw_sales = pd.read_csv("sunrise_sales_raw.csv")
print(raw_sales.shape)
print(raw_sales.duplicated().sum())
deduped = raw_sales.drop_duplicates()
print(deduped.shape)
print(deduped["units"].isna().sum())
log = pd.DataFrame({"problem": ["duplicate rows", "blank units"], "rows": [raw_sales.duplicated().sum(), deduped["units"].isna().sum()]})
log.to_csv("cleaning_log.csv", index=False)
print(pd.read_csv("cleaning_log.csv"))
```

Correct result: The raw file has 1538 rows. 25 are exact duplicates, so removing them leaves 1513, the same as the clean file. 40 rows have blank units. The log table is saved and read back with two lines: 25 duplicate rows and 40 blank-unit rows.

Investigate, with answers:

- Why does the cleaned row count of 1513 match the clean file? Answer: The 25 extra rows were exact copies. Removing them restores the original count.
- Why not fill the 40 blank units with the mean? Answer: It would invent sales that nobody recorded. We decide in session 16 how to report them.

Modify: Count the rows whose date is written with slashes, and add them to the log. Answer: 60 rows.

```python
slashes = deduped["sale_date"].str.contains("/").sum()
```

## Make: reference

```python
import pandas as pd
log = pd.DataFrame({"step": ["raw rows", "duplicate removed", "missing price remaining"], "count": [4, 1, 1]})
log.to_csv("my_log.csv", index=False)
print(pd.read_csv("my_log.csv"))
# Zero would say the item was free. The price is unknown.
```

Build log entry to look for: DA10.ipynb and my_log.csv with the three counts and the sentence about zero.

## Misconceptions to listen for

- A missing value is the same as zero.
- Every repeated row is an error.
- Cleaning means making the numbers look nice.

## Questions to ask, with expected answers

- What goes in a cleaning log? Expected: The problem, how many rows it touched, and what you did.
- Why work on a copy? Expected: The raw file is the evidence. Overwriting it destroys the evidence.

## Online version

For a hybrid group. The live class is 90 minutes on video with screen sharing. The learner finishes the build in their own time, about an hour. The full rules are in handbook/HYBRID_DELIVERY.md.

### Live clock, 90 minutes

| Minutes | Activity |
|---|---|
| 5 | Recall: three questions on paper, then say the answers aloud |
| 35 | Block A, Missing values and duplicates in a small table: predict, run, investigate. The Modify step moves to the build task. |
| 5 | Break away from the screen |
| 35 | Block B, The raw Sunrise file: predict, run, investigate. The Modify step moves to the build task. |
| 10 | Close: say the exit sentence aloud, then the build task is set |

### After-class build task, about an hour

1. Modify, Block A (Missing values and duplicates in a small table): Count how many rows in clean still have a missing price.
2. Modify, Block B (The raw Sunrise file): Count the rows whose date is written with slashes, and add them to the log.
3. Make: Write a cleaning log for the four-row table in Block A: four raw rows, one duplicate removed, one price still missing. Save it as a CSV with to_csv. Write one sentence on why replacing the missing price with zero would change what the data says.

When you finish, write two sentences: what you changed and how you checked it. Add a build log entry. Send a photo of your work or the notebook by the route the organiser sets, before the next class.

### Next class

In the next class recall, ask: What goes in a cleaning log? Expected: The problem, how many rows it touched, and what you did.

## Build log and feedback

Look at what each of the five learners saved and note one strength and one next step for each. Share them kindly and privately. Nothing is scored or ranked. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and show-and-tells need your judgement.
