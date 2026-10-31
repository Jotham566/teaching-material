# DA07 Instructor guide: A table in Python: DataFrame, columns and reading a CSV

Private. Keep this file out of the student folder.

**Objective.** By the end: you can build a small table, read a CSV file into one, and say how many rows and columns it has and what each column holds.

**Question of the day.** What is in each table we have been given?

Prerequisite: DA06 Functions and checks that fail loudly.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

Where it overruns: Six words and two blocks. If Block B runs long, shorten the products table and keep the shop table.

## Block A. Build a tiny table

pandas is a library for tables. import pandas as pd loads it and gives it the short name pd. A dot after a name reaches something that belongs to it: sales.shape asks the table for its size. A shape of (3, 2) means three rows and two columns.

Ask for the prediction first: Predict the shape of the table before you run the cell.

```python
import pandas as pd
sales = pd.DataFrame({"item": ["Book", "Pen", "Book"], "units": [2, 5, 3]})
print(sales)
print(sales.shape)
print(list(sales.columns))
```

Correct result: The cell prints a table of three rows and two columns, then (3, 2), then ['item', 'units']. The first column holds the item sold and the second holds the units.

Investigate, with answers:

- Which number in (3, 2) counts rows? Answer: The first one. The shape is rows first and then columns.
- Where do the column headers come from? Answer: From the keys of the dictionary we gave pandas.

Modify: Add a third column called price_ugx with the values 3000, 1000 and 3000, then print the shape. Answer: The shape becomes (3, 3).

```python
sales["price_ugx"] = [3000, 1000, 3000]
```

## Block B. Read a CSV file

pd.read_csv reads a CSV file and returns a DataFrame. The path is where the file is. Here the file sits beside the notebook, so its name is enough. dtypes lists the type of each column.

Ask for the prediction first: Predict how many rows and columns camp_shop.csv has, and which columns hold text.

```python
shop = pd.read_csv("camp_shop.csv")
print(shop.shape)
print(shop.dtypes)
products = pd.read_csv("sunrise_products.csv")
print(products.shape)
print(products.head(3))
```

Correct result: The shop table has shape (60, 5). date and item hold text. The other three columns are whole numbers. The Sunrise products table has shape (15, 5): fifteen products, each with an id, a name, a category and two prices.

Investigate, with answers:

- Which columns would you use to work out revenue? Answer: units and unit_price_ugx. Revenue is units times unit price.
- Why is date a text column here? Answer: pandas reads it as text until we ask it to treat it as a date, which is a later session.

Modify: Show the last three rows of the shop table with tail(3). Answer: Sales 58, 59 and 60.

```python
last3 = shop.tail(3)
```

## Make: reference

```python
import pandas as pd
sunrise = pd.read_csv("sunrise_sales.csv")
print(sunrise.shape)
print(list(sunrise.columns))
# 1513 rows and 6 columns. sale_date holds the date and unit_price_ugx the price of one unit.
```

Evidence to collect: DA07.ipynb with shape (1513, 6), the six column names and two sentences naming the date and price columns.

## Misconceptions to listen for

- A CSV file is an Excel file.
- Reading a file changes the file.
- The shape lists columns first.

## Questions to ask, with expected answers

- What is the difference between a row and a column? Expected: A row is one record. A column is one kind of information about every record.
- What does read_csv give back? Expected: A DataFrame.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
