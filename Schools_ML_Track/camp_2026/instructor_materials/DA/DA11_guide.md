# DA11 Instructor guide: Charts that say what the numbers say

Private. Keep this file out of the student folder.

**Objective.** By the end: you can draw a bar chart, a line chart, a histogram and a scatter plot with labelled axes, and state one finding and one limit for each.

**Question of the day.** Which chart shows this comparison most clearly?

Prerequisite: DA10 Cleaning without hiding evidence.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

Where it overruns: plt.show() blocks nothing in a notebook, but charts can overlap. Close each figure before the next.

## Block A. Bar and line charts

plt.bar draws one bar for each category. A bar chart starts its value axis at zero, because the length of a bar stands for the amount. plt.plot joins points in order, which suits dates.

Ask for the prediction first: Predict which of the three bars will be tallest.

```python
import pandas as pd
import matplotlib.pyplot as plt
shop = pd.read_csv("camp_shop.csv")
shop["revenue_ugx"] = shop["units"] * shop["unit_price_ugx"]
by_item = shop.groupby("item")["revenue_ugx"].sum()
plt.bar(by_item.index, by_item.values)
plt.ylabel("Revenue (UGX)")
plt.title("Revenue by item, practice shop")
plt.ylim(bottom=0)
plt.show()
by_date = shop.groupby("date")["revenue_ugx"].sum()
plt.plot(by_date.index, by_date.values)
plt.ylabel("Revenue (UGX)")
plt.xticks(rotation=90)
plt.show()
```

Correct result: The first chart has three bars. Book is tallest at 297000, then Juice and Pen. The second chart is a line of 20 daily revenues, with the highest point on 2026-12-20. Every axis says what it measures and the bar chart starts at zero.

Investigate, with answers:

- Why does the bar chart start at zero? Answer: The length of the bar stands for the amount. A cut-off axis makes small differences look huge.
- Why use a line for dates and bars for items? Answer: Dates have an order, so a line shows change. Items have no order, so separate bars are fairer.

Modify: Draw the bar chart of units by item and add its label. Answer: Pen is tallest with 103 units.

```python
units_by_item = shop.groupby("item")["units"].sum()
plt.bar(units_by_item.index, units_by_item.values)
plt.ylabel("Units sold")
plt.close("all")
```

## Block B. Histogram and scatter plot

A histogram shows how the values are spread. A scatter plot puts two numbers on the two axes. These two charts use the Sunrise Shops tables.

Ask for the prediction first: Predict the shape of the histogram of sale values: balanced, or bunched at the low end with a long tail?

```python
sunrise = pd.read_csv("sunrise_sales.csv")
sunrise["line_value"] = sunrise["units"] * sunrise["unit_price_ugx"]
plt.hist(sunrise["line_value"], bins=30)
plt.xlabel("Value of one sale (UGX)")
plt.ylabel("Number of sales")
plt.show()
daily = pd.read_csv("sunrise_daily_summary.csv")
plt.scatter(daily["customers_counted"], daily["revenue_ugx"])
plt.xlabel("Customers counted in a day")
plt.ylabel("Revenue that day (UGX)")
plt.show()
```

Correct result: The histogram is bunched at the low end with a long tail to the right, because most sales are small and a few are very large. The scatter plot has 180 dots, one for each shop and day. More customers usually mean more revenue, but the dots are scattered, so the link is not exact.

Investigate, with answers:

- What does the long tail in the histogram tell us? Answer: A few sales are far larger than the rest. That is why the mean is above the median.
- Does the scatter plot show that customers cause revenue? Answer: It shows that they go together. It does not prove cause. That needs more evidence.

Modify: Change bins=30 to bins=10 and describe what the histogram loses. Answer: It hides detail in the long tail.

```python
counts, edges = plt.hist(sunrise["line_value"], bins=10)[:2]
plt.close("all")
```

## Make: reference

```python
import pandas as pd
import matplotlib.pyplot as plt
sunrise = pd.read_csv("sunrise_sales.csv")
sunrise["line_value"] = sunrise["units"] * sunrise["unit_price_ugx"]
names = {1: "Central Market", 2: "Campus Gate", 3: "Roadside"}
sunrise["branch"] = sunrise["branch_id"].map(names)
by_branch = sunrise.groupby("branch")["line_value"].sum()
plt.bar(by_branch.index, by_branch.values)
plt.ylabel("Revenue (UGX)")
plt.ylim(bottom=0)
plt.show()
# Central Market earns the most, 2997000. The data is invented, so it says nothing about real shops.
```

Evidence to collect: DA11.ipynb with a labelled bar chart of three branches, one finding and one limitation.

## Misconceptions to listen for

- A line chart suits any categories.
- A cut-off axis makes the chart clearer.
- Two things that move together cause each other.

## Questions to ask, with expected answers

- Which chart suits the revenue of each branch, and why? Expected: A bar chart, because the branches are separate categories.
- What must every chart carry? Expected: Labelled axes with units, and a title that says what is shown.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
