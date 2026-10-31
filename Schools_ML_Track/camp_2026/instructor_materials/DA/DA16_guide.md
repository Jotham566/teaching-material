# DA16 Instructor guide: Cleaning the raw export

Private. Keep this file out of the student folder.

**Objective.** By the end: you can turn a messy export into a clean table with a pipeline that reruns, and explain why its total is lower than the true total.

**Question of the day.** If we clean the raw export carefully, does it give back the true revenue?

Prerequisite: DA15 Exploring relationships: scatter plots, correlation and cause.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

Where it overruns: Two blocks of dense code. Run each line in its own cell the first time, and print after each.

## Block A. Dates and names

The raw export has two date formats in one column: 2026-09-01 and 01/09/2026. Parse each format on its own, and keep the date that worked. Names appear as juice, JUICE and " Juice ". Strip the spaces, fix the case and look each name up in the products table.

Ask for the prediction first: Predict how many dates cannot be parsed after both formats have been tried.

```python
import pandas as pd
raw = pd.read_csv("sunrise_sales_raw.csv")
work = raw.drop_duplicates().copy()
iso = pd.to_datetime(work["sale_date"], format="%Y-%m-%d", errors="coerce")
slash = pd.to_datetime(work["sale_date"], format="%d/%m/%Y", errors="coerce")
work["sale_date"] = iso.fillna(slash)
print(work["sale_date"].isna().sum())
print(work["sale_date"].min().date(), work["sale_date"].max().date())
products = pd.read_csv("sunrise_products.csv")
lookup = {n.title(): n for n in products["name"]}
work["product"] = work["product"].str.strip().str.title().map(lookup)
print(work["product"].isna().sum(), work["product"].nunique())
```

Correct result: The cell prints 0 dates that cannot be parsed, then the range 2026-09-01 to 2026-10-30. The names step prints 0 names left unmatched and 15 different products. Every date and product name is now one consistent form.

Investigate, with answers:

- Why parse the two formats separately and join the results? Answer: Python cannot tell whether 03/09/2026 is 3 September or 9 March. We know the second format is day first, so we say so.
- What does errors="coerce" do? Answer: It turns a date that does not fit the format into a missing value instead of stopping with an error.

Modify: Count how many rows used the slash format. Answer: 60.

```python
n_slash = int(raw.drop_duplicates()["sale_date"].str.contains("/").sum())
```

## Block B. Units, blanks and the residual

Some units are written as words, such as two. A lookup turns them into numbers. Blank units cannot be repaired, so we exclude those rows and count them. Then we compare with the true total. The two totals will differ, and the difference has a name.

Ask for the prediction first: Predict whether the cleaned revenue will be above, equal to or below the true revenue of 6375900.

```python
words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
work["units"] = pd.to_numeric(work["units"].replace(words), errors="coerce")
excluded = work[work["units"].isna()]
clean = work.dropna(subset=["units"]).copy()
clean["units"] = clean["units"].astype(int)
clean["line_value"] = clean["units"] * clean["unit_price_ugx"]
print(len(excluded), len(clean))
print(clean["line_value"].sum())
true_sales = pd.read_csv("sunrise_sales.csv")
true_total = (true_sales["units"] * true_sales["unit_price_ugx"]).sum()
residual = true_total - clean["line_value"].sum()
print(residual)
```

Correct result: 40 rows are excluded and 1473 rows are clean. The cleaned revenue is 6250500, which is 125400 below the true 6375900. The residual of 125400 is the value of the 40 excluded sales. It is not a mistake in the pipeline. It is the cost of rows that cannot be recovered.

Investigate, with answers:

- Why is the cleaned total below the true total? Answer: The 40 blank-unit sales are missing from the clean table, and their value is what is left over.
- Would it be honest to report that the two totals match? Answer: No. They differ by 125400, and the report says so and says why.

Modify: Prove that the residual equals the value of the 40 excluded sales, using the true sales table. Answer: Both are 125400.

```python
excluded_value = (true_sales[true_sales["sale_id"].isin(excluded["sale_id"])]["units"] * true_sales[true_sales["sale_id"].isin(excluded["sale_id"])]["unit_price_ugx"]).sum()
```

## Make: reference

```python
import pandas as pd
products = pd.read_csv("sunrise_products.csv")
lookup = {n.title(): n for n in products["name"]}
words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}

def clean_sales(raw):
    work = raw.drop_duplicates().copy()
    iso = pd.to_datetime(work["sale_date"], format="%Y-%m-%d", errors="coerce")
    slash = pd.to_datetime(work["sale_date"], format="%d/%m/%Y", errors="coerce")
    work["sale_date"] = iso.fillna(slash)
    work["product"] = work["product"].str.strip().str.title().map(lookup)
    work["units"] = pd.to_numeric(work["units"].replace(words), errors="coerce")
    excluded = work[work["units"].isna()]
    clean = work.dropna(subset=["units"]).copy()
    clean["units"] = clean["units"].astype(int)
    clean["line_value"] = clean["units"] * clean["unit_price_ugx"]
    return clean, excluded

clean, excluded = clean_sales(pd.read_csv("sunrise_sales_raw.csv"))
assert len(clean) == 1473
assert clean["line_value"].sum() == 6250500
print(len(excluded))
# The residual is 125400, the value of the 40 sales with blank units.
```

Evidence to collect: DA16.ipynb with the function, two passing asserts, and a sentence naming the residual of 125400 and its cause.

## Misconceptions to listen for

- A clean file must match the true total exactly.
- Blank units can be replaced by the mean.
- Cleaning order does not matter.

## Questions to ask, with expected answers

- Why do the cleaned and true totals differ? Expected: The 40 blank-unit sales cannot be recovered, and their value is the residual.
- Why put the steps in a function? Expected: It reruns the same steps every time and can be tested with assert.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
