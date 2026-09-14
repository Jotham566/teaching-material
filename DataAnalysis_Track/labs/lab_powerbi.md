# Lab: Power BI — a model, three measures, one dashboard
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
which reads UGX 1,459,000 instead of UGX 1,809,000 — 19% low, with no error and nothing
on the card to tell you. An average whose top and bottom disagree about which
rows they cover is the most common wrong number in business reporting.

**Check against numbers you already trust.** These came out of SQL in session
5 and out of pandas in session 9:

| Measure | Expected |
|---|---|
| `Revenue UGX`, no filter | UGX 10,758,894,480 |
| `Delivered Revenue UGX` | UGX 8,751,705,520 |
| `Avg Order Value UGX`, delivered | about UGX 1,809,000 |
| the same measure without `CALCULATE` | UGX 1,459,000 — wrong, and silent |

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
