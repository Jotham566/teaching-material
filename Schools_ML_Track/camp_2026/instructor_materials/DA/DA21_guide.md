# DA21 Instructor guide: Build and test the chart report

Private. Keep this file out of the student folder.

**Objective.** By the end: you can build a chart report that a stranger reads in 30 seconds, and you can critique a coding assistant's hint with a test.

**Question of the day.** Does my report answer my questions without a verbal tour?

Prerequisite: DA20 Build a reliable analysis.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

Where it overruns: The 20-minute critique lab sits inside the Make block. Start it only for learners who passed the individual readiness check.

## Make: reference

```python
import pandas as pd
import matplotlib.pyplot as plt
sales = pd.read_csv("sunrise_sales.csv")
sales["line_value"] = sales["units"] * sales["unit_price_ugx"]
by_branch = sales.groupby("branch_id")["line_value"].sum()
plt.bar(by_branch.index.astype(str), by_branch.values)
plt.ylabel("Revenue (UGX)")
plt.title("Revenue by branch, Sunrise Shops (invented data)")
plt.ylim(bottom=0)
plt.savefig("revenue.png", bbox_inches="tight")
plt.show()
with open("revenue.png", "rb") as f:
    header = f.read(4)
# savefig writes the image and bbox_inches="tight" keeps the labels in.
```

Evidence to collect: A chart report whose headline numbers match the notebook, a peer note on where they hesitated, and AI_USE_LOG.md with the tested critique.

## Misconceptions to listen for

- More charts make a stronger report.
- A plausible AI answer is a correct one.
- The report is allowed to need a spoken explanation.

## Questions to ask, with expected answers

- Where did your peer hesitate, and what did you change? Expected: A real hesitation and a concrete change to a heading or label.
- How did you test the assistant's advice? Expected: Predict, run, compare with the known answer, and keep the failing case.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
