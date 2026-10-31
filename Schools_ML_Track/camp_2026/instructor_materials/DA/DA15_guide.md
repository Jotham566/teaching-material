# DA15 Instructor guide: Exploring relationships: scatter plots, correlation and cause

Private. Keep this file out of the student folder.

**Objective.** By the end: you can draw a scatter plot coloured by group, read a correlation number, and say why a correlation does not prove one thing causes another.

**Question of the day.** Do busier days bring in more money, and does rain keep customers away?

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

Evidence to collect: DA15.ipynb with three correlations and a sentence on why correlation is not cause.

## Misconceptions to listen for

- A strong correlation proves cause.
- A correlation near zero means the chart is wrong.
- Correlation of -0.5 means no relationship.

## Questions to ask, with expected answers

- What would you check before saying rain keeps customers away? Expected: A reason and more evidence: the correlation is weak, and other things change from day to day.
- What does a negative correlation mean? Expected: One goes up as the other goes down.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
