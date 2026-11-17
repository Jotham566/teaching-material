# DA12 Instructor guide: Show your first chart and explain what it says

Private. Keep this file out of the student folder.

**Objective.** By the end: you can read a table, check it, summarise it, chart it and explain two findings and one limit, from a restarted notebook.

**Question of the day.** What do the Sunrise Shops sales tell us about the three shops?

**Where this is used.** Every analyst sends someone a first report: a table, one chart and a few honest sentences. Today you make yours. Who would you most like to send it to?

Prerequisite: DA11 Charts that say what the numbers say.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 15 | recall, then read the brief together |
| 80 | learners work and the instructor visits each of the five |
| 15 | break away from screens |
| 40 | learners finish, restart and run all |
| 20 | a quiet one-to-one chat, then save and share |
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

Build log entry to look for: DA12.ipynb that reruns from a restarted kernel, with the rows, total, checks, sorted branch totals, one labelled chart, two findings and one limitation. It goes in the build log, and the instructor gives one strength and one next step in a private chat.

## Misconceptions to listen for

- A notebook that works now will work after a restart.
- More charts show more skill.
- A finding needs no number.

## Questions to ask, with expected answers

- Where does each number in your findings come from? Expected: A named output cell. If it has no cell, it does not go in the finding.
- What can this data not tell us? Expected: Anything about real shops. It is invented, and it has no costs, so no profit.

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

1. Make: In DA12.ipynb use sunrise_sales.csv. 1) Report the number of rows and the total revenue. 2) Check for missing values and duplicates and report the counts. 3) Total the revenue by branch with names from a dictionary and sort the result. 4) Draw one labelled chart. 5) Write two findings and one limitation in text cells. 6) Look at the topic on your progress map and write one project question that this table, or another supplied table, could help answer. Restart the kernel, run all cells from the top, save DA12.ipynb with a short report.pdf or report.docx, and share them by the route in START_HERE.md.

When you finish, write two sentences: what you changed and how you checked it. Add a build log entry. Send a photo of your work or the notebook by the route the organiser sets, before the next class.

### Next class

In the next class recall, ask: Where does each number in your findings come from? Expected: A named output cell. If it has no cell, it does not go in the finding.

This is a work session. Keep the live part for the brief and for individual check-ins. The learner builds in the live time and after class.

## Build log and feedback

Look at what each of the five learners saved and note one strength and one next step for each. Share them kindly and privately. Nothing is scored or ranked. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and show-and-tells need your judgement.
