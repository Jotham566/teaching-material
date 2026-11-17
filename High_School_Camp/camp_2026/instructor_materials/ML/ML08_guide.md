# ML08 Instructor guide: Select, filter and calculate new columns

Private. Keep this file out of the student folder.

**Objective.** By the end: you can pick a column, keep rows that meet a condition, add a revenue column and total it by item.

**Question of the day.** Which item earned the most money in the practice shop?

**Where this is used.** A shopkeeper asks which item earned the most this week. Answering needs a filter and a new column: units times price. What would you ask of the sales of your own shop?

Prerequisite: ML07 Tables and reading a CSV file.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

## Block A. Select and filter

Read the practice shop and keep the large sales.

Ask for the prediction first: Predict how many of the 60 sales have 5 units or more.

```python
import pandas as pd
shop = pd.read_csv("camp_shop.csv")
units = shop["units"]
big = shop[shop["units"] >= 5]
print(len(big))
print(units.sum())
```

Correct result: The cell prints 30 and 277. shop["units"] selects one column. The comparison inside the outer brackets gives True or False for every row, and only the True rows stay. That filter keeps 30 sales. All 60 sales together sold 277 units.

Investigate, with answers:

- Is the filter deleting the other 30 rows? Answer: No. The big table is a new, smaller table. shop still has all 60 rows.
- Why can the sum of units not tell us the money earned? Answer: The three items have different prices, so units and money are different quantities.

Modify: Filter the Juice sales with 5 units or more and count them. Answer: Seven sales.

```python
juice_big = shop[(shop["item"] == "Juice") & (shop["units"] >= 5)]
n_juice_big = len(juice_big)
```

## Block B. A revenue column and totals by item

Multiply units by price on every row, then add the money for each item.

Ask for the prediction first: Predict which item earns the most money. Is it the one with the most units?

```python
shop["revenue_ugx"] = shop["units"] * shop["unit_price_ugx"]
total_revenue = shop["revenue_ugx"].sum()
by_item = shop.groupby("item")["revenue_ugx"].sum()
print(total_revenue)
print(by_item)
```

Correct result: The total is 550000 shillings. Book earns 297000, Juice 150000 and Pen 103000. Pen sold the most units, 103, but Book earns the most money because each Book costs 3000. Assigning to a new column name creates the column, and the groupby line adds the revenue of each item separately.

Investigate, with answers:

- Pen sold the most units. Why is it last for revenue? Answer: A pen costs only UGX 1000, so its units bring in little money.
- Do the three item totals add up to the overall total? Answer: Yes: 297000 + 150000 + 103000 is 550000. If they did not, something would be wrong.

Modify: Group the units column by item instead and print the totals. Answer: Book 99, Juice 75, Pen 103.

```python
units_by_item = shop.groupby("item")["units"].sum()
```

## Make: reference

```python
import pandas as pd
shop = pd.read_csv("camp_shop.csv")
over3 = shop[shop["units"] >= 3]
total_units = over3["units"].sum()
mean_units = over3["units"].mean()
print(len(over3), total_units, mean_units)
# 42 rows, 247 units in all, about 5.88 units per sale. The total is for all the rows together and the mean is for one row.
```

Build log entry to look for: ML08.ipynb with 42 rows, total 247, mean about 5.88, and a sentence on the difference.

## Misconceptions to listen for

- Filtering removes rows from the file.
- The item with the most units earns the most money.
- A mean is the same as a total.

## Questions to ask, with expected answers

- Why do we check that the grouped totals add to the overall total? Expected: It catches rows lost or counted twice.
- Can this table tell us profit? Expected: No. It has no costs.

## Online version

For a hybrid group. The live class is 90 minutes on video with screen sharing. The learner finishes the build in their own time, about an hour. The full rules are in handbook/HYBRID_DELIVERY.md.

### Live clock, 90 minutes

| Minutes | Activity |
|---|---|
| 5 | Recall: three questions on paper, then say the answers aloud |
| 35 | Block A, Select and filter: predict, run, investigate. The Modify step moves to the build task. |
| 5 | Break away from the screen |
| 35 | Block B, A revenue column and totals by item: predict, run, investigate. The Modify step moves to the build task. |
| 10 | Close: say the exit sentence aloud, then the build task is set |

### After-class build task, about an hour

1. Modify, Block A (Select and filter): Filter the Juice sales with 5 units or more and count them.
2. Modify, Block B (A revenue column and totals by item): Group the units column by item instead and print the totals.
3. Make: Keep the rows with units of at least 3. Calculate the total units and the mean units per row. Say why these two numbers are different quantities.

When you finish, write two sentences: what you changed and how you checked it. Add a build log entry. Send a photo of your work or the notebook by the route the organiser sets, before the next class.

### Next class

In the next class recall, ask: Why do we check that the grouped totals add to the overall total? Expected: It catches rows lost or counted twice.

## Build log and feedback

Look at what each of the five learners saved and note one strength and one next step for each. Share them kindly and privately. Nothing is scored or ranked. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and show-and-tells need your judgement.
