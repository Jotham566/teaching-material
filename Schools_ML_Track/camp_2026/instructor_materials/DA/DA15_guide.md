# DA15 Instructor guide: Exploring relationships: scatter plots, correlation and cause

Private. Keep this file out of the student folder.

**Objective.** By the end: you can draw a scatter plot coloured by group, read a correlation number, and say why a correlation does not prove one thing causes another.

**Question of the day.** Do busier days bring in more money, and does rain keep customers away?

**Where this is used.** Taxi parks, shops and farms all ask whether rain changes demand. Two things moving together do not prove that one causes the other. Do rainy days keep customers away, or is something else going on?

Prerequisite: DA14 Exploring distributions with seaborn.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

## Block A. A scatter plot and one correlation

sns.scatterplot puts one column on each axis. hue= colours the dots by group. .corr() calculates the correlation between two columns.

Ask for the prediction first: Predict whether the correlation between customers and revenue is close to 0, close to 1 or close to -1.

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
daily = pd.read_csv("sunrise_daily_summary.csv")
sns.scatterplot(data=daily, x="customers_counted", y="revenue_ugx", hue="branch")
plt.show()
r = daily["customers_counted"].corr(daily["revenue_ugx"])
print(round(r, 3))
```

Correct result: The dots rise from left to right, so more customers usually mean more revenue. The correlation is 0.623: positive and moderately strong. The dots are scattered, so a customer count does not fix the revenue.

Investigate, with answers:

- What would a correlation of 1 look like on the chart? Answer: All the dots would lie exactly on one rising line.
- Why do the colours help? Answer: They show that the three shops sit in different parts of the chart. Central Market is at the busy end.

Modify: Find the correlation between customers and the number of sale lines (sale_lines). Answer: 0.744, stronger.

```python
r_lines = daily["customers_counted"].corr(daily["sale_lines"])
```

## Block B. A heatmap of every pair, and the rain question

A heatmap of .corr() shows every pair at once. annot=True writes the numbers in the squares. Rain is in the data as rain_mm. Does it matter?

Ask for the prediction first: Predict whether rain_mm is strongly related to customers.

```python
cols = ["customers_counted", "rain_mm", "sale_lines", "revenue_ugx"]
table = daily[cols].corr()
sns.heatmap(table, annot=True, vmin=-1, vmax=1)
plt.show()
print(round(table.loc["rain_mm", "customers_counted"], 3))
print(round(table.loc["sale_lines", "revenue_ugx"], 3))
```

Correct result: Rain and customers have a correlation of -0.013, which is essentially zero. Sale lines and revenue have 0.565. In this data the weather barely matters. A weak correlation is a finding too.

Investigate, with answers:

- What does -0.013 tell us about rain? Answer: Almost nothing links them in this data. Wet days and dry days look alike.
- Could a strong correlation still be a coincidence? Answer: Yes. Two things can move together without one causing the other, so we look for a reason as well.

Modify: Find the correlation of rain_mm with revenue_ugx. Answer: -0.054, also close to zero.

```python
r_rain = table.loc["rain_mm", "revenue_ugx"]
```

## Make: reference

```python
import pandas as pd
daily = pd.read_csv("sunrise_daily_summary.csv")
result = {}
for name in ["Central Market", "Campus Gate", "Roadside"]:
    part = daily[daily["branch"] == name]
    result[name] = round(part["rain_mm"].corr(part["customers_counted"]), 3)
print(result)
# All three are weak. The largest is Roadside at -0.159. Even that does not prove that rain causes fewer customers.
```

Build log entry to look for: DA15.ipynb with three correlations and a sentence on why correlation is not cause.

## Misconceptions to listen for

- A strong correlation proves cause.
- A correlation near zero means the chart is wrong.
- Correlation of -0.5 means no relationship.

## Questions to ask, with expected answers

- What would you check before saying rain keeps customers away? Expected: A reason and more evidence: the correlation is weak, and other things change from day to day.
- What does a negative correlation mean? Expected: One goes up as the other goes down.

## Online version

For a hybrid group. The live class is 90 minutes on video with screen sharing. The learner finishes the build in their own time, about an hour. The full rules are in handbook/HYBRID_DELIVERY.md.

### Live clock, 90 minutes

| Minutes | Activity |
|---|---|
| 5 | Recall: three questions on paper, then say the answers aloud |
| 35 | Block A, A scatter plot and one correlation: predict, run, investigate. The Modify step moves to the build task. |
| 5 | Break away from the screen |
| 35 | Block B, A heatmap of every pair, and the rain question: predict, run, investigate. The Modify step moves to the build task. |
| 10 | Close: say the exit sentence aloud, then the build task is set |

### After-class build task, about an hour

1. Modify, Block A (A scatter plot and one correlation): Find the correlation between customers and the number of sale lines (sale_lines).
2. Modify, Block B (A heatmap of every pair, and the rain question): Find the correlation of rain_mm with revenue_ugx.
3. Make: Check the rain question for each shop separately. For each branch find the correlation between rain_mm and customers_counted. Say whether rain matters at any shop and why a correlation could not prove that it does.

When you finish, write two sentences: what you changed and how you checked it. Add a build log entry. Send a photo of your work or the notebook by the route the organiser sets, before the next class.

### Next class

In the next class recall, ask: What would you check before saying rain keeps customers away? Expected: A reason and more evidence: the correlation is weak, and other things change from day to day.

## Build log and feedback

Look at what each of the five learners saved and note one strength and one next step for each. Share them kindly and privately. Nothing is scored or ranked. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and show-and-tells need your judgement.
