# Lab: Python — cleaning, and writing down what you did
### Sessions 7, 8 and 9 · `data/orders_raw.csv`, `customers_raw.csv`,
### `order_items_raw.csv`

These three CSVs are the same business as `riverside.db`, exported badly by a
system that has been in use for nine years. Your job is to get from them to a
revenue number that matches the database, and to keep a log that lets somebody
else get there too.

**The target.** Revenue on delivered orders, according to the database, is
**UGX 8,751,705,520**. You are not told how to reach it.

**But a correct answer off these CSVs lands on UGX 8,751,672,145**, which is
UGX 33,375 lower. That gap is not a mistake you can fix. The imported
category was recorded in dollars **to the cent**, so converting it back at
3,780 cannot recover the exact shilling price on 2,016 delivered
lines. Rounding to the cent throws away a fraction of a shilling each time,
and it does not come back.

Landing within a few thousand shillings of the database is therefore the pass
mark, and **writing the residual down with its cause is part of it**. An
analyst who reports a reconciliation as exact when it is not has told you
they did not look. One who says "0.0004% low, from cent-rounding on the
dollar-priced lines" has told you they did.

Work in a notebook. Keep the cells in order and use Restart and Run All
before you submit, because a notebook that only works in the order you
happened to click is not a result.

---

## Part 1 — profile before you touch anything

```python
import pandas as pd

items = pd.read_csv("data/order_items_raw.csv")
orders = pd.read_csv("data/orders_raw.csv")
customers = pd.read_csv("data/customers_raw.csv")

for name, df in [("items", items), ("orders", orders),
                 ("customers", customers)]:
    print(name, df.shape)
    print(df.dtypes)
    print(df.isna().sum())
    print("-" * 40)
```

`order_items_raw.csv` has **20,775** rows. The database has
**20,234**. That difference is the whole lab, and it is made of three
separate problems, not one.

Write down the three numbers before you go on: rows in, rows you expect,
difference.

---

## Part 2 — the seven defects

Find each one before you read its fix. The counts are given so you know when
you have found all of it, but the count is the *answer*, not the method.

### 1. Duplicate rows — 40 of them
An export that ran twice. Exact duplicates across every column.
```python
items.duplicated().sum()
items = items.drop_duplicates()
```
Decide, and write down, whether an exact duplicate is always an error. On an
order line it is: the same product twice on one order would be one line with
quantity 2.

### 2. Negative quantities — 501 rows
Not corrupt. This system records a return as a negative line on the original
order, which is a convention, not a defect — until you sum quantity and get
a number that means neither sales nor net.
```python
items[items["quantity"] < 0].shape
returns = items[items["quantity"] < 0].copy()
sales = items[items["quantity"] > 0].copy()
```
Split them. Your revenue target is sales; returns are a separate figure the
manager also wants.

### 3. Prices in the wrong currency — 2,523 rows
One category was priced by a team that works in dollars. Nothing in the file
says so. Find it by asking what a price *should* look like:
```python
prod = pd.read_csv("data/products.csv")
j = sales.merge(prod[["product_id", "category", "unit_price_ugx"]],
                on="product_id", how="left", validate="many_to_one")
j.groupby("category")["unit_price"].describe()[["min", "max"]]
```
One category's prices are three orders of magnitude below the others. The
recorded rate is **3,780 UGX to the dollar**. Convert, and say in the log
that you did, because if the rate is wrong every number downstream is wrong
by the same factor.

### 4. Discounts above 1.0 — 203 rows
Someone typed 15 meaning 15 per cent, into a column where 0.15 means the
same thing. A discount of 15.0 makes revenue negative, which is the tell.
```python
sales[sales["discount"] > 1]["discount"].unique()
```

### 5. Two date formats in one column — 1,055 rows
`order_date` arrives as both `2025-03-14` and `14/03/2025`.
```python
orders["order_date"] = pd.to_datetime(orders["order_date"],
                                      format="mixed", dayfirst=True)
```
Then check the range. If you get dates in 1970 or 2087, the parse guessed.

### 6. Customer names, 117 of them messy
Upper case, lower case, and leading and trailing spaces. Harmless until you
group by name and get three groups for one customer.
```python
customers["customer_name"] = (customers["customer_name"]
                              .str.strip().str.title())
```

### 7. Missing customer ids — 172 orders
Walk-in trade. These are real orders with real revenue and no customer.
**This is a decision, not a fix.** Dropping them loses
UGX 390,632,335 of revenue. Keeping them means every per-customer analysis has
a gap you must state. Either is defensible; silence is not.

### And one more, which nothing will tell you about
Two customer ids, **1007** and **1999**, are the same business:
*Gumisiriza Enterprises*. Same name, same city, two ids, both with orders against them.
Per-customer totals are wrong until you decide what to do. Find it with:
```python
customers.groupby(["customer_name", "city"]).size().sort_values().tail()
```

---

## Part 3 — the cleaning log

A table, in the notebook, filled in as you go. Not written afterwards.

| Step | Rows before | Rows after | What changed | Why |
|---|---|---|---|---|
| Loaded raw items | — | 20,775 | — | — |
| Dropped exact duplicates | 20,775 | | 40 rows | export ran twice |
| Split out returns | | | 501 rows moved | negative quantity is a return |
| ... | | | | |

The log is marked as heavily as the answer. A number nobody can reproduce is
not a result, and in six months the person who cannot reproduce it is you.

---

## Part 4 — reconcile, which is the actual skill

Reproduce your SQL answers in pandas and compare them.

```python
rev = (sales["quantity"] * sales["unit_price"]
       * (1 - sales["discount"])).sum()
print(f"{rev:,.0f}")
```

Then by region, delivered only, and set it against the SQL result:

| Region | Revenue, delivered, customers only |
|---|---|
| Eastern | UGX 2,514,623,935 |
| Northern | UGX 2,107,303,745 |
| Central | UGX 2,022,616,760 |
| Western | UGX 1,810,419,785 |

Every difference is a finding. Chase each one until you can name it, then
stop: the cent-rounding residual above is named, so it is finished. "Close
enough" with no number beside it is how a wrong figure reaches a board
paper.

---

## Homework

Same routine on a real file: **Online Retail II**, CC BY 4.0, at
<https://archive.ics.uci.edu/dataset/502/online+retail+ii> —
1,067,371 rows x 8 columns, .xlsx, Dec 2009 to Dec 2011, no account needed.

It has its own versions of most of the defects above, plus two this dataset
does not have: negative quantities that are cancellations rather than
returns, and a customer id column with a third of its values missing. Profile
it, clean it, log it, and write three sentences saying what the file is a
record of.
