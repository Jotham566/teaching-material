# DA09 Instructor guide: Sort, group, mean and median

Private. Keep this file out of the student folder.

**Objective.** By the end: you can total a column by group, sort the result, and say when the median describes a column better than the mean.

**Question of the day.** Which item earns the most, and what is a typical sale in a small practice shop?

Prerequisite: DA08 Select, filter and calculate a revenue column.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

Where it overruns: The move to the 1513-row table is the first time students cannot check every row by eye. Say so aloud and check totals instead.

## Block A. Group, total and sort

groupby gathers the rows with the same item. A calculation such as sum then works inside each group. sort_values puts the answer in order.

Ask for the prediction first: Predict which item sold the most units and which earned the most money.

```python
import pandas as pd
shop = pd.read_csv("camp_shop.csv")
shop["revenue_ugx"] = shop["units"] * shop["unit_price_ugx"]
units_by_item = shop.groupby("item")["units"].sum()
revenue_by_item = shop.groupby("item")["revenue_ugx"].sum().sort_values(ascending=False)
print(units_by_item)
print(revenue_by_item)
```

Correct result: Pen sold the most units, 103. Book earned the most money, 297000 shillings, then Juice 150000 and Pen 103000. The three revenues add to 550000. The item that sells the most units is not the item that earns the most.

Investigate, with answers:

- Why does Pen sell the most units and earn the least money? Answer: A Pen costs 1000 shillings and a Book costs 3000, so each Pen sale brings in less.
- How do you check the grouped totals? Answer: Add them up and compare with the overall total of 550000.

Modify: Group the revenue by date and find the date with the most revenue. Answer: 2026-12-20 with 47000.

```python
by_date = shop.groupby("date")["revenue_ugx"].sum()
best_date = by_date.idxmax()
```

## Block B. Mean, median and a proportion

Now meet the bigger Sunrise Shops table: 1513 sales from three shops. The mean can be pulled up by a few huge sales. The median is not. A proportion needs its whole named: 36 large orders out of 1513 sales.

Ask for the prediction first: Predict whether the mean sale value is above or below the median.

```python
sunrise = pd.read_csv("sunrise_sales.csv")
sunrise["line_value"] = sunrise["units"] * sunrise["unit_price_ugx"]
mean_value = sunrise["line_value"].mean()
median_value = sunrise["line_value"].median()
bulk = (sunrise["units"] >= 10).sum()
share = bulk / len(sunrise)
print(round(mean_value), median_value)
print(bulk, len(sunrise), round(share * 100, 1))
```

Correct result: The mean sale value is about 4214 shillings and the median is 2400. A few bulk purchases pull the mean up. 36 of the 1513 sales have 10 units or more, which is 2.4 percent. The 1513 is the denominator.

Investigate, with answers:

- Which number is a better answer to "what does a typical sale bring in"? Answer: The median, 2400, because a few bulk sales inflate the mean.
- Why must you say that the whole is 1513 sales? Answer: A percentage with no stated whole cannot be compared with another percentage.

Modify: Find the proportion of sales with 5 units or more. Answer: About 8.7 percent, 132 of 1513.

```python
n5 = (sunrise["units"] >= 5).sum()
share5 = n5 / len(sunrise)
```

## Make: reference

```python
import pandas as pd
sunrise = pd.read_csv("sunrise_sales.csv")
sunrise["line_value"] = sunrise["units"] * sunrise["unit_price_ugx"]
by_branch = sunrise.groupby("branch_id")["line_value"].sum().sort_values(ascending=False)
print(by_branch)
assert by_branch.sum() == sunrise["line_value"].sum()
# Branch 1: 2997000. Branch 2: 1985400. Branch 3: 1393500. Total 6375900.
```

Evidence to collect: DA09.ipynb with three sorted totals that add to 6375900 and a passing assert.

## Misconceptions to listen for

- The item that sells the most units earns the most money.
- The mean is always the best summary.
- A percentage is meaningful without its whole.

## Questions to ask, with expected answers

- When would you quote the median and not the mean? Expected: When a few very large values pull the mean away from what most sales look like.
- What check follows every group total? Expected: Add the groups and compare with the overall total.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
