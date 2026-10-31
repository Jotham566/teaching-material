# ML12 Instructor guide: Checkpoint one and a project question

Private. Keep this file out of the student folder.

**Objective.** By the end: you can load a table, check it, total it, chart it, write two findings and a limitation, and ask one prediction question a table could answer.

**Question of the day.** Can I take a table from a file to a labelled chart and a careful finding on my own?

Prerequisite: ML11 Charts that show what the numbers say.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | recall |
| 20 | brief and worked skeleton |
| 15 | break |
| 100 | checkpoint work |
| 20 | project question |
| 15 | save and exit check |

Where it overruns: Most time goes on the independent checkpoint. Keep the skeleton short and let students use their own wording.

## Block A. The checkpoint skeleton

Run the skeleton, then repeat each step in your own notebook, ML12.ipynb, with your own wording.

Ask for the prediction first: Predict the row count, the total revenue and the best-selling item by revenue.

```python
import pandas as pd
import matplotlib.pyplot as plt
shop = pd.read_csv("camp_shop.csv")
missing = shop.isna().sum().sum()
shop["revenue_ugx"] = shop["units"] * shop["unit_price_ugx"]
by_item = shop.groupby("item")["revenue_ugx"].sum()
print(shop.shape[0], missing, by_item.sum())
assert by_item.sum() == shop["revenue_ugx"].sum()
plt.bar(by_item.index, by_item.values)
plt.ylabel("Revenue (UGX)")
plt.title("Revenue by item, practice shop")
plt.show()
```

Correct result: The skeleton prints 60 rows, 0 missing cells and a total revenue of 550000. The assert passes silently because the item totals add up to the overall total. The chart shows Book as the tallest bar. Your checkpoint needs the same steps with your own two findings, one limitation, a missing-value check and a clean rerun from a restarted kernel.

Investigate, with answers:

- What does the passing assert prove? Answer: That the grouped totals and the overall total agree.
- Why record that there were no missing values? Answer: A check that finds nothing is still evidence that you looked.

Modify: Add a finding with a number and one limitation as text cells under the chart. Answer: For example: Book earns UGX 297000, about 54% of revenue. The data is invented and has no costs.

```python
book_share = by_item['Book'] / by_item.sum()
```

## Block B. Write your project question

In the last 20 minutes choose a table and write three sentences: the question, the dataset and the target. Model building starts next week.

Ask for the prediction first: Before you look at the datasets again, write the question you would most like a model to answer.

Correct result: Your three sentences name a question a table can answer, one supplied dataset (synthetic_homes.csv, synthetic_fares.csv or the iris flowers), and the target to predict. Inputs must be known before the target is. Good: predict monthly rent from area and rooms. Weak: explain why rents are high.

Investigate, with answers:

- Which column is the target in synthetic_fares.csv? Answer: fare_ugx, the price of the trip.
- Why does a prediction question need inputs known beforehand? Answer: A model cannot use information that only exists after the answer.

Modify: Rewrite a question that asks why into one that asks for a prediction. Answer: Why are rents high becomes: can area and rooms predict monthly rent?

## Make: reference

```python
import pandas as pd
import matplotlib.pyplot as plt
shop = pd.read_csv("camp_shop.csv")
missing = shop.isna().sum().sum()
shop["revenue_ugx"] = shop["units"] * shop["unit_price_ugx"]
by_item = shop.groupby("item")["revenue_ugx"].sum()
total_units = shop["units"].sum()
print(len(shop), missing, total_units, by_item.to_dict())
```

Evidence to collect: ML12.ipynb: totals, one labelled chart, two findings, one limitation, a missing-value check, a restarted-kernel run, and a three-sentence project question.

## Misconceptions to listen for

- The checkpoint needs a new technique.
- A prediction question can be any question.
- No missing values means no check is needed.

## Questions to ask, with expected answers

- What do you do first if the totals disagree? Expected: Compare row counts at each step to find where rows changed.
- What makes a project question suitable? Expected: A table can answer it, a target exists, and its inputs are known beforehand.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
