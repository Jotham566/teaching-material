# DA18 Instructor guide: Does your total match the true total? Clean, merge and reconcile

Private. Keep this file out of the student folder.

**Objective.** By the end: you can clean a raw export, merge it with a lookup table, and report a total together with its named difference from the true total.

**Question of the day.** Which category earns the most in the cleaned data, and by how much do our totals fall short of the truth?

**Where this is used.** Accountants and auditors compare two totals and explain the gap. Banks and tax teams do this every month. Can you explain why your total is a little short of the true one?

Prerequisite: DA17 Merging two tables and the fan-out trap.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 15 | recall, then read the brief together |
| 80 | learners work and the instructor visits each of the five |
| 15 | break away from screens |
| 40 | learners finish, restart and run all |
| 20 | a quiet one-to-one chat, then save and share |
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

Build log entry to look for: DA18.ipynb that reruns from a restarted kernel, with rows kept and excluded, the unique-key check, category totals, the named residual and two limitations. It goes in the build log, and the instructor gives one strength and one next step in a private chat.

## Misconceptions to listen for

- A passing merge means correct totals.
- The residual means the pipeline is wrong.
- More steps mean a better result.

## Questions to ask, with expected answers

- How do you prove the merge did not change the data? Expected: The row count and the grand total are the same before and after.
- What is the residual here? Expected: 125400 shillings, the value of the 40 sales with blank units.

## Online version

For a hybrid group. The live class is 90 minutes on video with screen sharing. The learner finishes the build in their own time, about an hour. The full rules are in handbook/HYBRID_DELIVERY.md.

### Live clock, 90 minutes

| Minutes | Activity |
|---|---|
| 5 | Recall: three questions on paper, then say the answers aloud |
| 35 | Read the brief together on the shared screen, then the first build step. Each learner shares their screen in turn. |
| 5 | Break away from the screen |
| 35 | Learners keep building. The instructor visits each learner by screen share, about seven minutes each. |
| 10 | Close: say the exit sentence aloud, then the rest of the build task is set |

### After-class build task, about an hour

1. Make: In DA18.ipynb start from sunrise_sales_raw.csv. 1) Clean it with a function and report the rows kept, rows excluded and the cleaning steps. 2) Merge the clean table with the products table on product_id. Check that the key is unique and that the row count is unchanged. 3) Total the revenue by category. 4) Compare the cleaned total with the true total in sunrise_sales.csv. Name the residual and its cause. 5) Write two limitations. Run from a restarted kernel, save DA18.ipynb with a short explanation of your checks, and share them by the route in START_HERE.md.

When you finish, write two sentences: what you changed and how you checked it. Add a build log entry. Send a photo of your work or the notebook by the route the organiser sets, before the next class.

### Next class

In the next class recall, ask: How do you prove the merge did not change the data? Expected: The row count and the grand total are the same before and after.

This is a work session. Keep the live part for the brief and for individual check-ins. The learner builds in the live time and after class.

## Build log and feedback

Look at what each of the five learners saved and note one strength and one next step for each. Share them kindly and privately. Nothing is scored or ranked. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and show-and-tells need your judgement.
