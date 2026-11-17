# DA21 Instructor guide: Build and check the chart report

Private. Keep this file out of the student folder.

**Objective.** By the end: you can build a chart report that a stranger reads in 30 seconds, and you can critique a coding assistant's hint with a test.

**Question of the day.** Does my report answer my questions without a verbal tour?

**Where this is used.** A report that needs its author in the room has not done its job. Clear titles, labels and units let a farmer, a manager or a parent read it alone. Could your report speak for itself?

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

Build log entry to look for: A chart report whose headline numbers match the notebook, a peer note on where they hesitated, and AI_USE_LOG.md with the tested critique.

## Misconceptions to listen for

- More charts make a stronger report.
- A plausible AI answer is a correct one.
- The report is allowed to need a spoken explanation.

## Questions to ask, with expected answers

- Where did your peer hesitate, and what did you change? Expected: A real hesitation and a concrete change to a heading or label.
- How did you test the assistant's advice? Expected: Predict, run, compare with the known answer, and keep the failing case.

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

1. Make: Build the chart report. Use few charts, readable labels with units, the covered dates and a visible data source note. Write two findings and one limitation next to their evidence. Give a peer 30 seconds to find the largest category and its total, and record where they hesitate. To put a chart in your report, call plt.savefig("revenue.png", bbox_inches="tight") before plt.show(), then insert the PNG with Insert and Pictures. When the instructor confirms you are ready, spend 20 minutes with AI_CODING_ASSISTANTS_LAB.md: critique a hint on the practice function, run a test and log it in AI_USE_LOG.md.

When you finish, write two sentences: what you changed and how you checked it. Add a build log entry. Send a photo of your work or the notebook by the route the organiser sets, before the next class.

### Next class

In the next class recall, ask: Where did your peer hesitate, and what did you change? Expected: A real hesitation and a concrete change to a heading or label.

This is a work session. Keep the live part for the brief and for individual check-ins. The learner builds in the live time and after class.

## Build log and feedback

Look at what each of the five learners saved and note one strength and one next step for each. Share them kindly and privately. Nothing is scored or ranked. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and show-and-tells need your judgement.
