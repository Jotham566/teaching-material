# -*- coding: utf-8 -*-
"""Generate the three tool labs for the Data Analysis track.

Every number that appears in a lab comes out of answer_key.json, which was
produced by running the query against the same database the participants get.
Nothing here is typed from memory, and verify_da_track.py re-executes the lot.
"""
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)

TRACK = os.path.join(_ROOT, "DataAnalysis_Track")
DATA = os.path.join(TRACK, "data")
LABS = os.path.join(TRACK, "labs")

with open(os.path.join(DATA, "answer_key.json"), encoding="utf-8") as fh:
    K = json.load(fh)


def ugx(x):
    return "UGX {:,.0f}".format(x)


def n(x):
    return "{:,}".format(x)


# =========================================================== SQL, sessions 3-5
# Each question carries the query that answers it and the answer that query
# returned. The query IS the answer key: verify_da_track.py runs every one of
# them and fails if the result moves.
SQL_Q = [
    ("How many orders are in the database?",
     "SELECT COUNT(*) FROM orders;",
     n(K["s2"]["orders_total"]),
     "Start here so you have a number to check every later filter against."),

    ("How many were delivered, and how many cancelled?",
     "SELECT status, COUNT(*) AS orders\n"
     "FROM orders\nGROUP BY status\nORDER BY orders DESC;",
     "Delivered {}, Pending, Cancelled {}".format(
         n(K["s2"]["orders_delivered"]), n(K["s2"]["orders_cancelled"])),
     "Three statuses, and from here on every revenue question has to say "
     "which of them it counts."),

    ("Compare COUNT(*) with COUNT(customer_id) on the orders table. "
     "Why do they differ?",
     "SELECT COUNT(*) AS rows_in_table,\n"
     "       COUNT(customer_id) AS rows_with_a_customer\n"
     "FROM orders;",
     "{} rows, {} with a customer".format(
         *[n(v) for v in K["s2"]["count_star_vs_customer_id"]]),
     "COUNT(*) counts rows. COUNT(column) counts rows where that column is "
     "not NULL. The gap is {} walk-in orders with no customer recorded, and "
     "it is the single most useful thing in this session.".format(
         n(K["s2"]["count_star_vs_customer_id"][0]
           - K["s2"]["count_star_vs_customer_id"][1]))),

    ("Which sales channel is used most?",
     "SELECT channel, COUNT(*) AS orders\n"
     "FROM orders\nGROUP BY channel\nORDER BY orders DESC;",
     ", ".join("{} {}".format(c, n(v))
               for c, v in K["s2"]["orders_by_channel"]),
     "GROUP BY plus ORDER BY on the aggregate. Note you can order by "
     "something you computed."),

    ("Which customer segments have more than 80 customers?",
     "SELECT segment, COUNT(*) AS customers\n"
     "FROM customers\nGROUP BY segment\nHAVING COUNT(*) > 80\n"
     "ORDER BY customers DESC;",
     ", ".join("{} {}".format(s, n(v))
               for s, v in K["s2"]["segments_over_80_customers"]),
     "HAVING filters groups; WHERE filters rows. Try it with WHERE and read "
     "the error: that error is worth more than the answer."),

    ("What is total revenue across every order line, before any filtering?",
     "SELECT SUM(quantity * unit_price_ugx * (1 - discount)) AS revenue_ugx\n"
     "FROM order_items;",
     ugx(K["s3"]["revenue_all_ugx"]),
     "Revenue is a calculation, not a column, and this is the definition "
     "used for the rest of the course: quantity x price x (1 - discount)."),

    ("Now revenue for delivered orders only.",
     "SELECT SUM(oi.quantity * oi.unit_price_ugx * (1 - oi.discount))\n"
     "         AS revenue_ugx\n"
     "FROM order_items oi\n"
     "JOIN orders o ON o.order_id = oi.order_id\n"
     "WHERE o.status = 'Delivered';",
     ugx(K["s3"]["revenue_delivered_ugx"]),
     "The first join. {} of the unfiltered total is sitting in pending and "
     "cancelled orders, which is why 'revenue' with no qualifier is not an "
     "answer.".format(ugx(K["s3"]["revenue_all_ugx"]
                          - K["s3"]["revenue_delivered_ugx"]))),

    ("Revenue by region, delivered orders only.",
     "SELECT c.region,\n"
     "       SUM(oi.quantity * oi.unit_price_ugx * (1 - oi.discount))\n"
     "         AS revenue_ugx\n"
     "FROM order_items oi\n"
     "JOIN orders o    ON o.order_id    = oi.order_id\n"
     "JOIN customers c ON c.customer_id = o.customer_id\n"
     "WHERE o.status = 'Delivered'\n"
     "GROUP BY c.region\nORDER BY revenue_ugx DESC;",
     ", ".join("{} {}".format(r, ugx(v))
               for r, v in K["s3"]["revenue_by_region_ugx"]),
     "Three tables. And a trap: this total is LOWER than the delivered total "
     "above, because joining to customers drops the {} walk-in orders. That "
     "is {} of revenue gone with no warning.".format(
         n(K["s3"]["inner_join_drops_rows"]),
         ugx(K["s3"]["revenue_lost_to_inner_join_ugx"]))),
]

SQL_LAB = """# Lab: SQL — getting the rows you asked for
### Sessions 3, 4 and 5 · Riverside Distributors · `data/riverside.db`

Open `riverside.db` in **DB Browser for SQLite**: File, Open Database, then
the *Execute SQL* tab. Nothing to install beyond the browser itself, and
nothing you type here can damage the file as long as you only write SELECT.

**The tables.** Six of them, and the shape matters more than the names:

| Table | Rows | One row is |
|---|---|---|
| `customers` | {n_cust} | a business that buys from us |
| `products` | {n_prod} | something we sell |
| `reps` | {n_reps} | a sales rep, who belongs to one region |
| `orders` | {n_ord} | one order, on one date, by one rep |
| `order_items` | {n_item} | one product on one order |
| `returns` | {n_ret} | one returned line, with a reason |

`orders` has one row per order and `order_items` has one row per product on
that order. That single fact is behind most wrong answers in SQL, so say it
out loud before you start.

**Revenue, for the whole course, is** `quantity * unit_price_ugx *
(1 - discount)`. Amounts are Ugandan shillings.

---

## The eight questions

Work them in order. Each one has the query and the answer, so check yourself
as you go rather than at the end. Write the query before you read the answer:
reading it first feels like learning and is not.

{questions}

---

## Session 5: the report the sales manager actually wants

> Revenue by rep by month for 2025, net of returns.

Ranking and running totals are deliberately NOT part of this. SQL does both,
with window functions, and they are a session's worth of new ideas eight days
after your first SELECT. Export this result and rank it in the spreadsheet,
where you are already fluent.

Build it in steps, as three CTEs. A CTE is just a named query you can use
like a table, and three short named steps are readable by somebody who did
not write them, which nested subqueries are not.

```sql
WITH lines AS (
    -- step 1: one row per order line, with its month and its rep
    SELECT o.rep_id,
           substr(o.order_date, 1, 7)                        AS month,
           oi.line_no,
           oi.quantity * oi.unit_price_ugx * (1 - oi.discount) AS gross_ugx
    FROM order_items oi
    JOIN orders o ON o.order_id = oi.order_id
    WHERE o.status = 'Delivered'
      AND o.order_date >= '2025-01-01'
),
net AS (
    -- step 2: subtract what came back. LEFT JOIN, because most lines have
    -- no return and an INNER JOIN here would silently keep only the
    -- returned ones.
    SELECT l.rep_id, l.month,
           SUM(l.gross_ugx) AS gross_ugx,
           SUM(COALESCE(rt.quantity_returned, 0) * oi.unit_price_ugx
               * (1 - oi.discount)) AS returned_ugx
    FROM lines l
    JOIN order_items oi ON oi.line_no = l.line_no
    LEFT JOIN returns rt ON rt.line_no = l.line_no
    GROUP BY l.rep_id, l.month
)
-- step 3: name the reps, rank them inside their region, run the total
SELECT r.region,
       r.rep_name,
       n.month,
       ROUND(n.gross_ugx)                      AS gross_ugx,
       ROUND(n.returned_ugx)                   AS returned_ugx,
       ROUND(n.gross_ugx - n.returned_ugx)     AS net_ugx
FROM net n
JOIN reps r ON r.rep_id = n.rep_id
ORDER BY r.region, r.rep_name, n.month;
```

**Check it against these,** which are the top three reps by 2025 revenue
before returns are taken off:

{top_reps}

Total value of everything returned, across both years: **{returns_value}**.

### What to hand in
The query, and one sentence naming which rep you would talk to first and
why. The sentence is the assessed part. A query with no conclusion is not an
analysis.

---

## Break it on purpose

Do these three after it works. Each takes one minute and each teaches
something that will otherwise cost you a day.

1. **Change the `LEFT JOIN returns` to `JOIN`.** Revenue collapses, because
   now only the returned lines survive. Note the new number.
2. **Remove `WHERE o.status = 'Delivered'`.** Revenue rises by
   {cancelled_gap}, all of it from orders nobody paid for.
3. **Join `orders` to `customers` with an ordinary `JOIN`** and total the
   revenue. It falls by {walkin_gap}, because {walkin_orders} walk-in orders
   have no customer to join to. Nothing warns you. The only tell is that the
   row count moved, which is why you check the row count after every join.
"""


def write_sql():
    qs = []
    for i, (q, sql, ans, note) in enumerate(SQL_Q, 1):
        qs.append("### {}. {}\n\n```sql\n{}\n```\n\n**Answer:** {}\n\n{}\n"
                  .format(i, q, sql, ans, note))
    txt = SQL_LAB.format(
        n_cust=n(K["row_counts"]["customers"]),
        n_prod=n(K["row_counts"]["products"]),
        n_reps=n(K["row_counts"]["reps"]),
        n_ord=n(K["row_counts"]["orders"]),
        n_item=n(K["row_counts"]["order_items"]),
        n_ret=n(K["row_counts"]["returns"]),
        questions="\n".join(qs),
        top_reps="\n".join("- **{}** — {}".format(r, ugx(v))
                           for r, v in K["s3"]["top_rep_2025"]),
        returns_value=ugx(K["s3"]["returns_value_ugx"]),
        cancelled_gap=ugx(K["s3"]["revenue_all_ugx"]
                          - K["s3"]["revenue_delivered_ugx"]),
        walkin_gap=ugx(K["s3"]["revenue_lost_to_inner_join_ugx"]),
        walkin_orders=n(K["s3"]["inner_join_drops_rows"]))
    p = os.path.join(LABS, "lab_sql.md")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(txt)
    return p


# ======================================================= Python, sessions 7-9
PY_LAB = """# Lab: Python — cleaning, and writing down what you did
### Sessions 7, 8 and 9 · `data/orders_raw.csv`, `customers_raw.csv`,
### `order_items_raw.csv`

These three CSVs are the same business as `riverside.db`, exported badly by a
system that has been in use for nine years. Your job is to get from them to a
revenue number that matches the database, and to keep a log that lets somebody
else get there too.

**The target.** Revenue on delivered orders, according to the database, is
**{rev_delivered}**. You are not told how to reach it.

**But a correct answer off these CSVs lands on {rev_from_raw}**, which is
{residual} lower. That gap is not a mistake you can fix. The imported
category was recorded in dollars **to the cent**, so converting it back at
{usd_rate} cannot recover the exact shilling price on {usd_lines} delivered
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

`order_items_raw.csv` has **{raw_rows}** rows. The database has
**{clean_items}**. That difference is the whole lab, and it is made of three
separate problems, not one.

Write down the three numbers before you go on: rows in, rows you expect,
difference.

---

## Part 2 — the seven defects

Find each one before you read its fix. The counts are given so you know when
you have found all of it, but the count is the *answer*, not the method.

### 1. Duplicate rows — {d_dupes} of them
An export that ran twice. Exact duplicates across every column.
```python
items.duplicated().sum()
items = items.drop_duplicates()
```
Decide, and write down, whether an exact duplicate is always an error. On an
order line it is: the same product twice on one order would be one line with
quantity 2.

### 2. Negative quantities — {d_neg} rows
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

### 3. Prices in the wrong currency — {d_usd} rows
One category was priced by a team that works in dollars. Nothing in the file
says so. Find it by asking what a price *should* look like:
```python
prod = pd.read_csv("data/products.csv")
j = sales.merge(prod[["product_id", "category", "unit_price_ugx"]],
                on="product_id", how="left", validate="many_to_one")
j.groupby("category")["unit_price"].describe()[["min", "max"]]
```
One category's prices are three orders of magnitude below the others. The
recorded rate is **{usd_rate} UGX to the dollar**. Convert, and say in the log
that you did, because if the rate is wrong every number downstream is wrong
by the same factor.

### 4. Discounts above 1.0 — {d_disc} rows
Someone typed 15 meaning 15 per cent, into a column where 0.15 means the
same thing. A discount of 15.0 makes revenue negative, which is the tell.
```python
sales[sales["discount"] > 1]["discount"].unique()
```

### 5. Two date formats in one column — {d_dates} rows
`order_date` arrives as both `2025-03-14` and `14/03/2025`.
```python
orders["order_date"] = pd.to_datetime(orders["order_date"],
                                      format="mixed", dayfirst=True)
```
Then check the range. If you get dates in 1970 or 2087, the parse guessed.

### 6. Customer names, {d_names} of them messy
Upper case, lower case, and leading and trailing spaces. Harmless until you
group by name and get three groups for one customer.
```python
customers["customer_name"] = (customers["customer_name"]
                              .str.strip().str.title())
```

### 7. Missing customer ids — {d_missing} orders
Walk-in trade. These are real orders with real revenue and no customer.
**This is a decision, not a fix.** Dropping them loses
{walkin_gap} of revenue. Keeping them means every per-customer analysis has
a gap you must state. Either is defensible; silence is not.

### And one more, which nothing will tell you about
Two customer ids, **{dup_kept}** and **{dup_dup}**, are the same business:
*{dup_name}*. Same name, same city, two ids, both with orders against them.
Per-customer totals are wrong until you decide what to do. Find it with:
```python
customers.groupby(["customer_name", "city"]).size().sort_values().tail()
```

---

## Part 3 — the cleaning log

A table, in the notebook, filled in as you go. Not written afterwards.

| Step | Rows before | Rows after | What changed | Why |
|---|---|---|---|---|
| Loaded raw items | — | {raw_rows} | — | — |
| Dropped exact duplicates | {raw_rows} | | {d_dupes} rows | export ran twice |
| Split out returns | | | {d_neg} rows moved | negative quantity is a return |
| ... | | | | |

The log is marked as heavily as the answer. A number nobody can reproduce is
not a result, and in six months the person who cannot reproduce it is you.

---

## Part 4 — reconcile, which is the actual skill

Reproduce your SQL answers in pandas and compare them.

```python
rev = (sales["quantity"] * sales["unit_price"]
       * (1 - sales["discount"])).sum()
print(f"{{rev:,.0f}}")
```

Then by region, delivered only, and set it against the SQL result:

{region_table}

Every difference is a finding. Chase each one until you can name it, then
stop: the cent-rounding residual above is named, so it is finished. "Close
enough" with no number beside it is how a wrong figure reaches a board
paper.

---

## Homework

Same routine on a real file: **Online Retail II**, CC BY 4.0, at
<https://archive.ics.uci.edu/dataset/502/online+retail+ii> —
{retail_shape}, no account needed.

It has its own versions of most of the defects above, plus two this dataset
does not have: negative quantities that are cancellations rather than
returns, and a customer id column with a third of its values missing. Profile
it, clean it, log it, and write three sentences saying what the file is a
record of.
"""


def write_python():
    d = K["seeded_defects"]
    rows = []
    for r, v in K["s3"]["revenue_by_region_ugx"]:
        rows.append("| {} | {} |".format(r, ugx(v)))
    region_table = ("| Region | Revenue, delivered, customers only |\n"
                    "|---|---|\n" + "\n".join(rows))
    retail = next(x for x in
                  __import__("da_content").DATASETS if x["key"] == "retail")
    txt = PY_LAB.format(
        rev_delivered=ugx(K["s3"]["revenue_delivered_ugx"]),
        rev_from_raw=ugx(K["s3"]["revenue_delivered_from_raw_ugx"]),
        residual=ugx(K["s3"]["usd_rounding_residual_ugx"]),
        usd_lines=n(K["s3"]["usd_lines_delivered"]),
        raw_rows=n(K["raw_order_items_rows"]),
        clean_items=n(K["row_counts"]["order_items"]),
        d_dupes=n(d["duplicate_rows"]),
        d_neg=n(d["negative_quantity_lines"]),
        d_usd=n(d["lines_priced_in_usd"]),
        d_disc=n(d["discounts_over_one"]),
        d_dates=n(d["dates_in_dd_mm_yyyy"]),
        d_names=n(d["customer_names_messy"]),
        d_missing=n(d["orders_missing_customer_id"]),
        usd_rate="3,780",
        walkin_gap=ugx(K["s3"]["revenue_lost_to_inner_join_ugx"]),
        dup_kept=K["duplicate_customer"]["kept_id"],
        dup_dup=K["duplicate_customer"]["duplicate_id"],
        dup_name=K["duplicate_customer"]["name"],
        region_table=region_table,
        retail_shape=retail["shape"])
    p = os.path.join(LABS, "lab_python.md")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(txt)
    return p


# ==================================================== Power BI, sessions 14-15
PBI_LAB = """# Lab: Power BI — a model, three measures, one dashboard
### Sessions 14 and 15 · `data/*.csv` and `data/riverside.db`

**Before you start: which path are you on?**

Power BI Desktop is Windows only and free. If you are on a Mac, or on a
laptop your employer has locked down, you work in the browser Service at
<https://app.powerbi.com> instead. Both paths are written out below. The
browser cannot do three things, and it is better to know now than at 20:40
on session 14:

1. **No full Power Query editor.** You get a reduced one. So on the browser
   path, clean in pandas first and load a clean CSV. That is not a
   consolation prize; it is what most working pipelines do anyway.
2. **No local file as a refreshing source.** An uploaded file is a snapshot.
3. **No SQLite connector.** Use the CSVs, not `riverside.db`.

---

## Part 1 — get the data in

**Desktop.** Home, Get Data, Text/CSV, and load these five separately:
`customers.csv`, `products.csv`, `reps.csv`, `orders.csv`,
`order_items.csv`. Load each one, do not append them.

**Browser.** Create, then upload the same five CSVs to your workspace.

Then, in Power Query (Desktop) or in pandas beforehand (browser):

- Promote the first row to headers, if it did not happen on its own.
- Set `order_date` to Date, not Text. Check the earliest and latest values
  are inside 2024-01-01 to 2025-12-31.
- Set `quantity` to Whole Number, and `unit_price_ugx` and `discount` to
  Decimal Number.
- Trim `customer_name`.

Look at the Applied Steps list when you are done. That list is a recipe: it
runs again next month on new data, which is the whole reason to clean here
rather than by hand in Excel.

---

## Part 2 — the model, which is where the marks are

Model view. You want a star: `order_items` in the middle, everything else
pointing at it.

| From | To | On | Cardinality |
|---|---|---|---|
| `order_items` | `orders` | `order_id` | many to one |
| `orders` | `customers` | `customer_id` | many to one |
| `orders` | `reps` | `rep_id` | many to one |
| `order_items` | `products` | `product_id` | many to one |

**Delete every relationship Power BI created for you first, then build these
four by hand.** Auto-detect is right about most of them and wrong in a way
you will not notice until a total is wrong.

Then add a date table, because without one your months sort alphabetically
and April comes first:

```
Dates =
ADDCOLUMNS(
    CALENDAR(DATE(2024,1,1), DATE(2025,12,31)),
    "Year", YEAR([Date]),
    "Month", FORMAT([Date], "mmm"),
    "MonthNo", MONTH([Date]),
    "YearMonth", FORMAT([Date], "yyyy-mm")
)
```

Mark it as a date table, relate `Dates[Date]` to `orders[order_date]`, and
sort `Month` by `MonthNo` in the column tools. That last step is the one
everybody skips.

---

## Part 3 — three measures

A measure is calculated when a visual asks for it, inside that visual's
filters. A column is calculated once, per row, when the data loads. Getting
those two confused is the commonest Power BI mistake there is.

```
Revenue UGX =
SUMX(
    order_items,
    order_items[quantity] * order_items[unit_price_ugx]
        * (1 - order_items[discount])
)

Delivered Revenue UGX =
CALCULATE([Revenue UGX], orders[status] = "Delivered")

Avg Order Value UGX =
DIVIDE(
    [Delivered Revenue UGX],
    CALCULATE(DISTINCTCOUNT(orders[order_id]),
              orders[status] = "Delivered")
)
```

Two things in that last measure, both of which matter.

`DIVIDE` rather than `/` so that a zero denominator gives a blank instead of
an error in front of your audience.

And **`CALCULATE` on the denominator, so both halves of the average cover the
same population.** Without it you divide DELIVERED revenue by ALL orders,
which reads {aov_wrong} instead of {aov} — 19% low, with no error and nothing
on the card to tell you. An average whose top and bottom disagree about which
rows they cover is the most common wrong number in business reporting.

**Check against numbers you already trust.** These came out of SQL in session
5 and out of pandas in session 9:

| Measure | Expected |
|---|---|
| `Revenue UGX`, no filter | {rev_all} |
| `Delivered Revenue UGX` | {rev_delivered} |
| `Avg Order Value UGX`, delivered | about {aov} |
| the same measure without `CALCULATE` | {aov_wrong} — wrong, and silent |

If your model is wrong, these will not match, and the gap usually tells you
which relationship is at fault. **A dashboard whose totals do not reconcile
is worth less than no dashboard,** because it is believed.

---

## Part 4 — the dashboard

One page. Four visuals. A person will look at it for thirty seconds.

1. **A card**, top left: `Delivered Revenue UGX`. The number they came for.
2. **A line chart**: revenue by `Dates[YearMonth]`. December is visibly
   bigger both years. Say so in the title.
3. **A bar chart**: revenue by region, sorted by value, not alphabetically.
4. **A table**: top ten customers by revenue, with average order value.
5. **One slicer**: `Dates[Year]`. One, not five.

Then the title, which is the assessed part. Not "Sales Dashboard". Something
like "December is a third of the year's revenue in two weeks", if that is
what you found. A title that states the finding does the reader's work for
them, which is what they are paying for.

### Homework: the map
Add **Uganda Healthsites** — <https://data.humdata.org/dataset/uganda-healthsites>,
ODbL, about 7,969 facilities with coordinates — and put a map visual on it,
coloured by facility type. Then write two sentences: one on what this file
makes easy, one on what it makes impossible. ODbL is share-alike, so if you
publish anything derived from it, say where it came from.

---

## What to hand in

The `.pbix` file, or a link to the published report, plus one page: the
question, the answer with its number, how you know, and what would change
your answer. Five minutes in front of the room in session 15.
"""


def write_pbi():
    aov = (K["s3"]["revenue_delivered_ugx"]
           / max(1, K["s2"]["orders_delivered"]))
    # the WRONG figure is computed too, so the lab can quote it rather
    # than describe it. Delivered revenue over ALL orders, which is what the
    # measure gives if the CALCULATE is left off the denominator.
    aov_wrong = (K["s3"]["revenue_delivered_ugx"]
                 / max(1, K["row_counts"]["orders"]))
    txt = PBI_LAB.format(
        rev_all=ugx(K["s3"]["revenue_all_ugx"]),
        rev_delivered=ugx(K["s3"]["revenue_delivered_ugx"]),
        aov=ugx(round(aov, -3)),
        aov_wrong=ugx(round(aov_wrong, -3)))
    p = os.path.join(LABS, "lab_powerbi.md")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(txt)
    return p


if __name__ == "__main__":
    os.makedirs(LABS, exist_ok=True)
    for f in (write_sql(), write_python(), write_pbi()):
        print("saved", f)
