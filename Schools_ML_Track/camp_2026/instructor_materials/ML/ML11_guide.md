# ML11 Instructor guide: Charts that show what the numbers say

Private. Keep this file out of the student folder.

**Objective.** By the end: you can draw a labelled bar chart, a histogram and a box plot, and write one finding and one limitation.

**Question of the day.** How do I show which item earns most, and how sales vary, in a picture?

Prerequisite: ML10 Cleaning without hiding evidence.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

## Block A. A bar chart of revenue

Chart the revenue of each item from the practice shop. Label the axis with its unit.

Ask for the prediction first: Predict which bar will be tallest and roughly how tall.

```python
import matplotlib.pyplot as plt
import pandas as pd
shop = pd.read_csv("camp_shop.csv")
shop["revenue_ugx"] = shop["units"] * shop["unit_price_ugx"]
totals = shop.groupby("item")["revenue_ugx"].sum()
plt.bar(totals.index, totals.values)
plt.ylabel("Revenue (UGX)")
plt.title("Revenue by item in the practice shop")
plt.ylim(bottom=0)
plt.show()
```

Correct result: Three bars appear. Book is tallest at 297000, then Juice at 150000 and Pen at 103000. plt is the chart tool from matplotlib. ylabel and title add words, and ylim(bottom=0) starts the axis at zero so bar heights are fair. One finding is: Book earns the most, UGX 297000 of 550000. One limitation is: the data is invented and has no costs.

Investigate, with answers:

- Why must a bar chart start at zero? Answer: A bar's height should match its size. A cut-off axis exaggerates small differences.
- Does the chart tell us why Book earns most? Answer: No. It shows the totals only; the reason is a separate question.

Modify: Chart total units instead of revenue. Answer: Pen is now tallest, with 103 units.

```python
units_by_item = shop.groupby("item")["units"].sum()
plt.bar(units_by_item.index, units_by_item.values)
plt.ylabel("Units sold")
plt.show()
```

## Block B. A histogram and a box plot

seaborn draws statistical charts and builds on matplotlib. Draw how units vary and how they differ by item.

Ask for the prediction first: Predict which item has the lowest median units.

```python
import seaborn as sns
sns.histplot(data=shop, x="units", discrete=True)
plt.title("Units per sale")
plt.show()
sns.boxplot(data=shop, x="item", y="units")
plt.title("Units per sale for each item")
plt.show()
medians = shop.groupby("item")["units"].median()
```

Correct result: The histogram counts sales for each number of units and shows how they spread from 1 to 8. The box plot shows one box per item with a line at its median. Juice has the lowest median, 3.5 units, while Book has 5.0 and Pen 5.5. seaborn plots read straight from the table, which saves writing the grouping yourself.

Investigate, with answers:

- What does the line inside a box mean? Answer: The median of that item's units.
- Which chart shows how many sales had exactly 3 units? Answer: The histogram.

Modify: Change the histogram so it uses unit_price_ugx instead of units. Answer: Three tall bars appear, one at each price.

```python
sns.histplot(data=shop, x="unit_price_ugx")
plt.show()
```

## Make: reference

```python
import matplotlib.pyplot as plt
items = ["Book", "Pen", "Juice"]
heights = [6, 9, 4]
plt.bar(items, heights)
plt.ylabel("Units sold")
plt.title("Practice shop units sold")
plt.ylim(bottom=0)
plt.show()
# Finding: Pen sells 9 units, 3 more than Book. Limitation: the table is small and invented. Daily rainfall suits a line chart because the days are in order.
```

Evidence to collect: ML11.ipynb with a labelled bar chart, one finding with a number, one limitation, and the rainfall answer.

## Misconceptions to listen for

- A chart proves why something happened.
- The axis can start anywhere.
- A box plot shows every value.

## Questions to ask, with expected answers

- What is the first thing to look at on a chart? Expected: The title and the axis labels with their units.
- What can a bar chart never show you about cause? Expected: Anything. It shows totals and nothing about reasons.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
