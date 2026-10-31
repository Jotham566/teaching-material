# DA12 Instructor guide: Checkpoint one: load, summarise, chart and explain

Private. Keep this file out of the student folder.

**Objective.** By the end: you can read a table, check it, summarise it, chart it and explain two findings and one limit, from a restarted notebook.

**Question of the day.** What do the Sunrise Shops sales tell us about the three shops?

Prerequisite: DA11 Charts that say what the numbers say.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 15 | recall, then read the brief together |
| 80 | learners work and the instructor visits each of the five |
| 15 | break away from screens |
| 40 | learners finish, restart and run all |
| 20 | individual check, save and submit |
| 10 | review |

Where it overruns: Do not teach new syntax. Repair with the error cards from sessions 7 to 11.

## Make: reference

```python
import pandas as pd
import matplotlib.pyplot as plt
sales = pd.read_csv("sunrise_sales.csv")
sales["line_value"] = sales["units"] * sales["unit_price_ugx"]
rows = len(sales)
total = sales["line_value"].sum()
missing = int(sales.isna().sum().sum())
duplicates = int(sales.duplicated().sum())
names = {1: "Central Market", 2: "Campus Gate", 3: "Roadside"}
sales["branch"] = sales["branch_id"].map(names)
by_branch = sales.groupby("branch")["line_value"].sum().sort_values(ascending=False)
assert by_branch.sum() == total
plt.bar(by_branch.index, by_branch.values)
plt.ylabel("Revenue (UGX)")
plt.ylim(bottom=0)
plt.show()
# 1513 rows, 6375900 in revenue, no missing values, no duplicates. Central Market earns the most.
```

Evidence to collect: DA12.ipynb that reruns from a restarted kernel, with the rows, total, checks, sorted branch totals, one labelled chart, two findings and one limitation. Marks follow ASSESSMENT_AND_SHOWCASE.md.

## Misconceptions to listen for

- A notebook that works now will work after a restart.
- More charts show more skill.
- A finding needs no number.

## Questions to ask, with expected answers

- Where does each number in your findings come from? Expected: A named output cell. If it has no cell, it does not go in the finding.
- What can this data not tell us? Expected: Anything about real shops. It is invented, and it has no costs, so no profit.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
