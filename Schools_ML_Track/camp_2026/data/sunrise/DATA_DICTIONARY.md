# Sunrise Shops data

Sunrise Shops is a fictional chain of three shops. Everything here is generated (seed 20261031) and says nothing about real shops, prices or demand. It contains no learner records. Every number quoted in a lesson comes from `answer_key.json`.

Dates run for 60 days, 2026-09-01 to 2026-10-30. Money is in UGX. Revenue is always `units * unit_price_ugx`. Costs exist only in `products`, so profit uses the current cost list.

## sunrise.sqlite (clean)

| Table | Rows | Columns |
|---|---:|---|
| branches | 3 | branch_id, branch_name, area_type (market, school, roadside) |
| products | 15 | product_id, name, category (Stationery, Drinks, Snacks, Household), cost_ugx, price_ugx |
| sales | 1,513 | sale_id, sale_date, branch_id, product_id, units, unit_price_ugx |
| daily_branch | 180 | day, branch_id, customers_counted, rain_mm |
| products_practice | 16 | product_id, name, category. Juice (id 6) appears twice on purpose, for the fan-out lesson. |

`sales.unit_price_ugx` is the price charged on the day. Sugar 1kg rose from 4,500 to 5,000 UGX on day 31, so a sale keeps its own price.

The same tables are provided as CSV files for pandas (`products_practice.csv` included), and the Python-only camp track uses the CSVs. The SQLite file is kept for the professional course.

## daily_summary.csv (for exploration)

One row per branch per day (180 rows): `day, branch, customers_counted, rain_mm, sale_lines, revenue_ugx`. Built for the exploratory-analysis sessions. Customers counted and revenue are related but not tightly (correlation 0.62). Rain is in the data as a variable to examine and has almost no effect, which is an honest finding in its own right.

## sales_raw.csv (messy)

The same sales exported badly: columns `sale_id, sale_date, branch, product, units, unit_price_ugx`, with branch and product as text. Five defects are planted (counts in `answer_key.json`): exact duplicate rows, two date formats in one column, blank units, product names in inconsistent case and spacing, and units written as words.

Cleaning policy used by the key: drop exact duplicates, parse both date formats, normalise names with `strip().title()`, convert words to numbers, and exclude rows with blank units and report them. The cleaned revenue is therefore lower than the database revenue by exactly the value of the excluded rows, and a correct pipeline reports that difference instead of claiming the totals match.

## Rebuild and check

```
python3 generators/build_sunrise_data.py     # writes this folder (run from camp_2026/data)
python3 generators/verify_sunrise_data.py    # 32 independent checks, must all pass
```
