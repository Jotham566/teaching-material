# DA17 Instructor guide: Merging two tables and the fan-out trap

Private. Keep this file out of the student folder.

**Objective.** By the end: you can merge two tables on a key, check the row count before and after, and spot a duplicated key that inflates a total.

**Question of the day.** Which product category earns the most, and can we trust the merge that tells us?

Prerequisite: DA16 Cleaning the raw export.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

Where it overruns: The Block B surprise is the lesson. Let students find the extra 115 rows themselves before you explain.

## Block A. A merge you can trust

sales.csv holds the product_id of each sale. products.csv says which category each product belongs to. Merge them on product_id. The row count must not change, because each sale matches exactly one product.

Ask for the prediction first: Predict the row count after the merge and which category earns the most.

```python
import pandas as pd
sales = pd.read_csv("sunrise_sales.csv")
products = pd.read_csv("sunrise_products.csv")
sales["line_value"] = sales["units"] * sales["unit_price_ugx"]
print(products["product_id"].is_unique)
merged = sales.merge(products[["product_id", "category"]], on="product_id", how="left")
print(len(sales), len(merged))
by_category = merged.groupby("category")["line_value"].sum().sort_values(ascending=False)
print(by_category)
print(by_category.sum())
```

Correct result: The key is unique (True). Both tables have 1513 rows. The categories rank Household 2082700, Drinks 1863200, Stationery 1686500 and Snacks 743500, and they add to 6375900. The count and the total both match the true values, so the merge is safe.

Investigate, with answers:

- Why check that product_id is unique before merging? Answer: If a product appeared twice, every sale of it would be copied twice.
- How do you know the merge did not lose or add rows? Answer: The row count is 1513 before and after, and the category totals add to the overall total.

Modify: Show the category with the lowest revenue. Answer: Snacks with 743500.

```python
worst = by_category.idxmin()
```

## Block B. The fan-out trap

sunrise_products_practice.csv is a copy of the products table with one product listed twice. Merge with it and watch the totals. No error appears.

Ask for the prediction first: Predict what happens to the row count and the total revenue.

```python
practice = pd.read_csv("sunrise_products_practice.csv")
print(practice["product_id"].is_unique)
bad = sales.merge(practice[["product_id", "category"]], on="product_id", how="left")
print(len(bad), bad["line_value"].sum())
print(bad["line_value"].sum() - sales["line_value"].sum())
print(practice[practice.duplicated("product_id", keep=False)])
```

Correct result: The key is not unique (False). The merged table has 1628 rows, which is 115 too many, and the total is 7079900, which is 704000 too high. The duplicate is Juice with product_id 6. Python raised no error. Only the check of the row count and total finds it.

Investigate, with answers:

- Why did Python not warn us? Answer: A merge with a repeated key is legal. It simply copies the matching rows.
- What two numbers give the problem away? Answer: The row count rose from 1513 to 1628, and the total rose from 6375900 to 7079900.

Modify: Ask the merge to check the key by adding validate="many_to_one". Read the result. Answer: pandas stops with a MergeError.

```python
try:
    sales.merge(practice[["product_id", "category"]], on="product_id", validate="many_to_one")
    outcome = "no error"
except Exception as error:
    outcome = type(error).__name__
```

## Make: reference

```python
import pandas as pd
sales = pd.read_csv("sunrise_sales.csv")
branches = pd.read_csv("sunrise_branches.csv")
sales["line_value"] = sales["units"] * sales["unit_price_ugx"]
named = sales.merge(branches[["branch_id", "branch_name"]], on="branch_id", how="left", validate="many_to_one")
assert len(named) == len(sales)
by_name = named.groupby("branch_name")["line_value"].sum()
print(by_name)
# Central Market 2997000, Campus Gate 1985400, Roadside 1393500. They match session 9.
```

Evidence to collect: DA17.ipynb with the unchanged row count, three branch totals and the reconciliation sentence.

## Misconceptions to listen for

- A merge that runs without an error is correct.
- A merge never changes the row count.
- Any shared column can be a key.

## Questions to ask, with expected answers

- What two numbers tell you a merge went wrong? Expected: The row count and the grand total.
- What does validate="many_to_one" check? Expected: That the key is unique in the second table, so each row of the first matches one row.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
