# DA08 Instructor guide: Select, filter and calculate a revenue column

Private. Keep this file out of the student folder.

**Objective.** By the end: you can pick a column, keep the rows that meet a condition, and add a revenue column.

**Question of the day.** How much money did the practice shop take in, and where did it come from?

**Where this is used.** A shop owner asks which sales were big and how much money they brought in. Picking out rows and adding a new column is how analysts answer that on their own data. Which rows of a shop table would you pick out first?

Prerequisite: DA07 A table in Python: DataFrame, columns and reading a CSV.

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

Read the practice shop. Square brackets with a column name select one column. A comparison inside square brackets keeps only the rows where it is True.

Ask for the prediction first: Predict how many of the 60 sales have 5 units or more.

```python
import pandas as pd
shop = pd.read_csv("camp_shop.csv")
units = shop["units"]
big = shop[shop["units"] >= 5]
print(len(big))
print(units.sum())
```

Correct result: The cell prints 30 and then 277. shop["units"] selects one column. The comparison gives True or False for every row, and only the True rows stay. All 60 sales together sold 277 units.

Investigate, with answers:

- Is the filter deleting the other 30 rows? Answer: No. big is a new, smaller table. shop still has all 60 rows.
- Why can the sum of units not tell us the money earned? Answer: The three items have different prices, so units and money are different quantities.

Modify: Filter the Juice sales with 5 units or more and count them. Answer: Seven sales.

```python
juice_big = shop[(shop["item"] == "Juice") & (shop["units"] >= 5)]
n_juice_big = len(juice_big)
```

## Block B. A new revenue column

Assigning to a new column name creates the column. Multiplying two columns multiplies their matching rows. This is how units times price becomes revenue.

Ask for the prediction first: Predict the total revenue, using the item prices 3000, 1000 and 2000.

```python
shop["revenue_ugx"] = shop["units"] * shop["unit_price_ugx"]
print(shop.head(3))
print(shop["revenue_ugx"].sum())
```

Correct result: The first three revenues are 3000, 2000 and 8000. The total revenue is 550000 shillings. This is money taken in. There is no cost column, so profit cannot be worked out.

Investigate, with answers:

- Why is revenue not profit? Answer: Profit is revenue minus the cost of the goods. The table has no cost.
- Does the new column change camp_shop.csv? Answer: No. It exists only in the notebook until you save it.

Modify: Find the revenue of the Book sales only. Answer: 297000.

```python
book_revenue = shop[shop["item"] == "Book"]["revenue_ugx"].sum()
```

## Make: reference

```python
import pandas as pd
shop = pd.read_csv("camp_shop.csv")
shop["revenue_ugx"] = shop["units"] * shop["unit_price_ugx"]
pens = shop[(shop["item"] == "Pen") & (shop["units"] >= 4)]
print(len(pens), pens["revenue_ugx"].sum())
# 14 sales and 90000 shillings. The count is how many sales. The revenue is how much money.
```

Build log entry to look for: DA08.ipynb with 14 sales, 90000 shillings and a sentence on the difference.

## Misconceptions to listen for

- Filtering removes rows from the file.
- The item with the most units earns the most money.
- A new column is saved in the CSV automatically.

## Questions to ask, with expected answers

- Why do we use & and not the word and inside the brackets of a filter? Expected: pandas combines two columns of True and False values row by row, and & does that.
- Why should the total of the parts equal the whole? Expected: It is the first check that a calculation did not lose or double rows.

## Online version

For a hybrid group. The live class is 90 minutes on video with screen sharing. The learner finishes the build in their own time, about an hour. The full rules are in handbook/HYBRID_DELIVERY.md.

### Live clock, 90 minutes

| Minutes | Activity |
|---|---|
| 5 | Recall: three questions on paper, then say the answers aloud |
| 35 | Block A, Select and filter: predict, run, investigate. The Modify step moves to the build task. |
| 5 | Break away from the screen |
| 35 | Block B, A new revenue column: predict, run, investigate. The Modify step moves to the build task. |
| 10 | Close: say the exit sentence aloud, then the build task is set |

### After-class build task, about an hour

1. Modify, Block A (Select and filter): Filter the Juice sales with 5 units or more and count them.
2. Modify, Block B (A new revenue column): Find the revenue of the Book sales only.
3. Make: Keep the Pen sales that have 4 units or more. Count them and add up the revenue they bring in. Say why the count and the revenue are different quantities.

When you finish, write two sentences: what you changed and how you checked it. Add a build log entry. Send a photo of your work or the notebook by the route the organiser sets, before the next class.

### Next class

In the next class recall, ask: Why do we use & and not the word and inside the brackets of a filter? Expected: pandas combines two columns of True and False values row by row, and & does that.

## Build log and feedback

Look at what each of the five learners saved and note one strength and one next step for each. Share them kindly and privately. Nothing is scored or ranked. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and show-and-tells need your judgement.
