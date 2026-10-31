# DA18 Instructor guide: Checkpoint two: clean, merge and reconcile

Private. Keep this file out of the student folder.

**Objective.** By the end: you can clean a raw export, merge it with a lookup table, and report a total together with its named difference from the true total.

**Question of the day.** Which category earns the most in the cleaned data, and by how much do our totals fall short of the truth?

Prerequisite: DA17 Merging two tables and the fan-out trap.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 15 | recall, then read the brief together |
| 80 | learners work and the instructor visits each of the five |
| 15 | break away from screens |
| 40 | learners finish, restart and run all |
| 20 | individual check, save and submit |
| 10 | review |

Where it overruns: Use the error cards from sessions 10, 16 and 17 for repair. Introduce no new syntax.

## Make: reference

```python
import pandas as pd
raw = pd.read_csv("sunrise_sales_raw.csv")
products = pd.read_csv("sunrise_products.csv")
lookup = {n.title(): n for n in products["name"]}
words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
work = raw.drop_duplicates().copy()
work["sale_date"] = pd.to_datetime(work["sale_date"], format="%Y-%m-%d", errors="coerce").fillna(pd.to_datetime(work["sale_date"], format="%d/%m/%Y", errors="coerce"))
work["product"] = work["product"].str.strip().str.title().map(lookup)
work["units"] = pd.to_numeric(work["units"].replace(words), errors="coerce")
excluded = work[work["units"].isna()]
clean = work.dropna(subset=["units"]).copy()
clean["units"] = clean["units"].astype(int)
clean["line_value"] = clean["units"] * clean["unit_price_ugx"]
clean = clean.merge(products.rename(columns={"name": "product"})[["product", "category"]], on="product", how="left", validate="many_to_one")
assert len(clean) == 1473
by_category = clean.groupby("category")["line_value"].sum().sort_values(ascending=False)
true_sales = pd.read_csv("sunrise_sales.csv")
true_total = int((true_sales["units"] * true_sales["unit_price_ugx"]).sum())
residual = true_total - int(clean["line_value"].sum())
assert by_category.sum() == clean["line_value"].sum()
print(by_category)
print(residual)
# Household earns the most. The residual 125400 is the value of the 40 excluded rows.
```

Evidence to collect: DA18.ipynb that reruns from a restarted kernel, with rows kept and excluded, the unique-key check, category totals, the named residual and two limitations. Marks follow ASSESSMENT_AND_SHOWCASE.md.

## Misconceptions to listen for

- A passing merge means correct totals.
- The residual means the pipeline is wrong.
- More steps mean a better checkpoint.

## Questions to ask, with expected answers

- How do you prove the merge did not change the data? Expected: The row count and the grand total are the same before and after.
- What is the residual here? Expected: 125400 shillings, the value of the 40 sales with blank units.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
