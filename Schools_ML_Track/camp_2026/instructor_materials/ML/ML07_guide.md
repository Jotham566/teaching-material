# ML07 Instructor guide: Tables and reading a CSV file

Private. Keep this file out of the student folder.

**Objective.** By the end: you can read a CSV file into a pandas table and say how many rows and columns it has.

**Question of the day.** How many sales are in the practice shop file, and what does each one record?

Prerequisite: ML06 Functions and checks that fail loudly.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

Where it overruns: This session is the first with a library. Spend the first block on the tiny table and keep the file reading to the second block.

## Block A. Build a small table

pandas is a library for tables. Run the cell and look at the table it prints.

Ask for the prediction first: Predict how many rows and columns the table has.

```python
import pandas as pd
sales = pd.DataFrame({"item": ["Book", "Pen", "Book"], "units": [2, 5, 3]})
print(sales)
print(sales.shape)
```

Correct result: The table has 3 rows and 2 columns, so shape prints (3, 2). The headers are item and units. import pandas as pd loads the library and gives it the short name pd. A table made this way is a DataFrame. The dot after sales reaches a property that belongs to that table.

Investigate, with answers:

- What does the first number of shape count? Answer: Rows. The second number counts columns.
- Where do the headers come from? Answer: From the names in the curly brackets: item and units.

Modify: Add a fourth sale, Pen with 4 units, to both lists and run again. Answer: shape becomes (4, 2).

```python
sales = pd.DataFrame({"item": ["Book", "Pen", "Book", "Pen"], "units": [2, 5, 3, 4]})
```

## Block B. Read the practice shop file

camp_shop.csv sits beside your notebook. Read it into a table and look at the first rows.

Ask for the prediction first: Predict how many rows camp_shop.csv has and which headers it shows.

```python
import pandas as pd
shop = pd.read_csv("camp_shop.csv")
print(shop.head())
print(shop.shape)
print(list(shop.columns))
```

Correct result: The table has 60 rows and 5 columns, so shape prints (60, 5). The headers are sale_id, date, item, units and unit_price_ugx. read_csv reads the file into a DataFrame and head shows its first five rows. The unit of money is in the header: unit_price_ugx is in shillings.

Investigate, with answers:

- Why is the unit written in the header name unit_price_ugx? Answer: A number without a unit is easy to misread. The header says the price is in shillings.
- What do the 60 rows stand for? Answer: Sixty sales. Each row is one sale.

Modify: Show the first 10 rows by writing 10 inside the brackets of head. Answer: Ten rows print.

```python
first_ten = shop.head(10)
```

## Make: reference

```python
import pandas as pd
homes = pd.read_csv("synthetic_homes.csv")
print(homes.head())
print(homes.shape)
# 120 rows and 4 columns. Each row is one invented home. rent_ugx is monthly rent in shillings.
```

Evidence to collect: ML07.ipynb with the first rows, the shape (120, 4), and two sentences on a row and the unit.

## Misconceptions to listen for

- A DataFrame is only a picture that I cannot calculate with.
- The shape pair is the same as the first two rows.
- Every column has the same type.

## Questions to ask, with expected answers

- What does shape return for a table of 20 sales and 5 headers? Expected: (20, 5).
- Why keep the CSV beside the notebook? Expected: read_csv looks for the file starting from the notebook folder.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
