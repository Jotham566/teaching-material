#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Sunrise Shops teaching dataset for Python & SQL for Data Analysis.

Standard library only (sqlite3, csv, json, random, datetime), so it runs on any
Python 3.8+ with nothing installed.

WHY IT IS GENERATED
-------------------
Every number on a lesson sheet comes from answer_key.json, which is written
here from the same data. Nothing is estimated. The data is SYNTHETIC: Sunrise
Shops is a fictional three-shop chain, and nothing here says anything about
real shops, prices or demand.

WHAT IT CONTAINS (all proposals from the restructuring plan, 31 Oct 2026)
-------------------------------------------------------------------------
Clean database  sunrise.sqlite
    branches(3)  products(15)  sales(~1,500)  daily_branch(180)
    products_practice  a copy of products in which one product appears twice,
                       so the fan-out join in session 14 can be seen.
Raw export      sales_raw.csv   the same sales, exported badly, five defects.
Clean CSVs      branches.csv products.csv sales.csv daily_branch.csv
Answer key      answer_key.json

THREE TEACHING PROPERTIES, ASSERTED (the build fails if one disappears)
-----------------------------------------------------------------------
 1. Mean line value is well above the median (a few bulk purchases), so the
    mean-versus-median lesson in session 7 is real.
 2. The branch with the most revenue is NOT the branch with the most revenue
    per counted customer, so the rate-versus-count lesson is real.
 3. The practice products table fans a join out: sales rows grow, and so does
    revenue, with no error raised.

FIVE SEEDED DEFECTS IN sales_raw.csv (counts are in the answer key)
-------------------------------------------------------------------
 1. exact duplicate rows            2. mixed date formats (ISO and dd/mm/yyyy)
 3. blank units                     4. product names in inconsistent case/spacing
 5. units written as words ("two")

CLEANING POLICY THE KEY ASSUMES
-------------------------------
Drop exact duplicates; parse both date formats; normalise names with
strip().title() and map to product_id; convert words to numbers; EXCLUDE rows
with blank units (they cannot be recovered) and count them. The cleaned
revenue is therefore LOWER than the database revenue by exactly the value of
the excluded rows. The key records that residual, and a correct pipeline must
report it instead of claiming the totals match.

Usage:  python3 build_sunrise_data.py [--out DIR] [--seed N]
"""
import argparse
import csv
import json
import os
import random
import shutil
import sqlite3
import statistics
import tempfile
from datetime import date, timedelta

SEED = 20261031
START = date(2026, 9, 1)
N_DAYS = 60

# id, name, category, cost_ugx, price_ugx
PRODUCTS = [
    (1, "Exercise Book", "Stationery", 2000, 3000),
    (2, "Pen", "Stationery", 600, 1000),
    (3, "Pencil", "Stationery", 300, 500),
    (4, "Ruler", "Stationery", 900, 1500),
    (5, "Geometry Set", "Stationery", 4200, 6000),
    (6, "Juice", "Drinks", 1300, 2000),
    (7, "Bottled Water", "Drinks", 600, 1000),
    (8, "Soda", "Drinks", 1000, 1500),
    (9, "Milk Packet", "Drinks", 900, 1200),
    (10, "Biscuits", "Snacks", 700, 1000),
    (11, "Chapati", "Snacks", 300, 500),
    (12, "Groundnuts", "Snacks", 500, 800),
    (13, "Soap Bar", "Household", 1800, 2500),
    (14, "Sugar 1kg", "Household", 3800, 4500),
    (15, "Candle", "Household", 400, 700),
]
SUGAR_NEW_PRICE = 5000  # price rise from day 30; sales rows keep the price charged
SUGAR_RISE_DAY = 30

# id, name, type, mean customers counted per weekday (Mon=0), conversion
BRANCHES = [
    (1, "Central Market", "market", [230, 230, 230, 230, 240, 310, 120], 0.043),
    (2, "Campus Gate", "school", [150, 150, 150, 150, 140, 40, 20], 0.080),
    (3, "Roadside", "roadside", [85, 85, 85, 85, 95, 110, 90], 0.072),
]
# product weights per branch (index = product_id - 1)
MIX = {
    1: [2, 3, 3, 1, 1, 4, 6, 5, 3, 4, 6, 4, 8, 9, 6],
    2: [9, 10, 8, 5, 3, 6, 5, 3, 2, 8, 9, 6, 1, 1, 1],
    3: [1, 2, 2, 1, 0.5, 8, 10, 9, 4, 6, 5, 5, 3, 3, 3],
}


def build(seed):
    rnd = random.Random(seed)
    days = [START + timedelta(days=i) for i in range(N_DAYS)]
    daily, sales = [], []
    sale_id = 0
    for d_idx, d in enumerate(days):
        rain = round(max(0.0, rnd.gauss(-3, 9)), 1) if rnd.random() < 0.45 else 0.0
        for b_id, _n, _t, per_wd, conv in BRANCHES:
            base = per_wd[d.weekday()]
            counted = int(round(base * (0.8 if rain > 8 else 1.0) * rnd.uniform(0.85, 1.15)))
            daily.append((d.isoformat(), b_id, counted, rain))
            lines = max(0, int(round(counted * conv * rnd.uniform(0.8, 1.2))))
            weights = MIX[b_id]
            for _ in range(lines):
                sale_id += 1
                pid = rnd.choices(range(1, 16), weights=weights)[0]
                if rnd.random() < 0.03:
                    units = rnd.randint(10, 40)  # bulk purchase
                else:
                    units = rnd.choices([1, 2, 3, 4, 5], weights=[40, 28, 16, 10, 6])[0]
                price = PRODUCTS[pid - 1][4]
                if pid == 14 and d_idx >= SUGAR_RISE_DAY:
                    price = SUGAR_NEW_PRICE
                sales.append((sale_id, d.isoformat(), b_id, pid, units, price))
    return days, daily, sales, rnd


def write_csv(path, header, rows):
    with open(path, "w", newline="\n", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def make_raw(sales, rnd):
    """Return (raw_rows, defect_counts, recoverable_excluded_value)."""
    pname = {p[0]: p[1] for p in PRODUCTS}
    bname = {b[0]: b[1] for b in BRANCHES}
    rows = []
    for s in sales:
        rows.append([s[0], s[1], bname[s[2]], pname[s[3]], s[4], s[5]])
    idx = list(range(len(rows)))
    rnd.shuffle(idx)
    pick = lambda n: [idx.pop() for _ in range(n)]
    blank_i = pick(40)                       # defect 3
    date_i = pick(60)                        # defect 2
    name_i = pick(80)                        # defect 4
    word_i = [i for i in idx if rows[i][4] <= 5][:12]   # defect 5
    for i in word_i:
        idx.remove(i)
    words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}
    excluded_value = 0
    for i in blank_i:
        excluded_value += rows[i][4] * rows[i][5]
        rows[i][4] = ""
    for i in date_i:
        y, m, d = rows[i][1].split("-")
        rows[i][1] = f"{d}/{m}/{y}"
    for i in name_i:
        v = rows[i][3]
        rows[i][3] = rnd.choice([v.lower(), v.upper(), " " + v, v + "  ", v.lower() + " "])
    for i in word_i:
        rows[i][4] = words[rows[i][4]]
    dup_src = rnd.sample(range(len(rows)), 25)   # defect 1
    for i in dup_src:
        rows.insert(rnd.randrange(len(rows) + 1), list(rows[i]))
    counts = {"duplicate_rows": 25, "mixed_date_format_rows": 60, "blank_units_rows": 40,
              "messy_name_rows": 80, "units_as_words_rows": 12}
    return rows, counts, excluded_value


def stats_from_db(con):
    q = lambda sql, *a: con.execute(sql, a).fetchall()
    key = {}
    key["sales_rows"] = q("SELECT COUNT(*) FROM sales")[0][0]
    key["total_revenue_ugx"] = q("SELECT SUM(units*unit_price_ugx) FROM sales")[0][0]
    key["total_units"] = q("SELECT SUM(units) FROM sales")[0][0]
    key["total_profit_ugx"] = q("SELECT SUM(s.units*(s.unit_price_ugx-p.cost_ugx)) FROM sales s JOIN products p USING(product_id)")[0][0]
    key["revenue_by_branch"] = {r[0]: r[1] for r in q("SELECT b.branch_name, SUM(s.units*s.unit_price_ugx) FROM sales s JOIN branches b USING(branch_id) GROUP BY b.branch_name ORDER BY 2 DESC")}
    key["revenue_by_category"] = {r[0]: r[1] for r in q("SELECT p.category, SUM(s.units*s.unit_price_ugx) FROM sales s JOIN products p USING(product_id) GROUP BY p.category ORDER BY 2 DESC")}
    key["units_by_product_top5"] = [[r[0], r[1]] for r in q("SELECT p.name, SUM(s.units) u FROM sales s JOIN products p USING(product_id) GROUP BY p.name ORDER BY u DESC, p.name LIMIT 5")]
    key["customers_counted_by_branch"] = {r[0]: r[1] for r in q("SELECT b.branch_name, SUM(d.customers_counted) FROM daily_branch d JOIN branches b USING(branch_id) GROUP BY b.branch_name")}
    key["revenue_per_customer_by_branch"] = {
        r[0]: round(r[1] / r[2], 2) for r in q(
            "SELECT b.branch_name, r.rev, c.cust FROM branches b "
            "JOIN (SELECT branch_id, SUM(units*unit_price_ugx) rev FROM sales GROUP BY branch_id) r USING(branch_id) "
            "JOIN (SELECT branch_id, SUM(customers_counted) cust FROM daily_branch GROUP BY branch_id) c USING(branch_id)")}
    vals = [r[0] for r in q("SELECT units*unit_price_ugx FROM sales")]
    key["line_value_mean_ugx"] = round(statistics.mean(vals), 2)
    key["line_value_median_ugx"] = statistics.median(vals)
    key["mean_over_median"] = round(statistics.mean(vals) / statistics.median(vals), 3)
    key["sales_rows_by_branch"] = {r[0]: r[1] for r in q("SELECT b.branch_name, COUNT(*) FROM sales s JOIN branches b USING(branch_id) GROUP BY b.branch_name")}
    return key


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sunrise"))
    ap.add_argument("--seed", type=int, default=SEED)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    days, daily, sales, rnd = build(a.seed)

    # ---- clean database, built in a temp dir (mounted folders break sqlite journals)
    tmp = tempfile.mkdtemp()
    dbp = os.path.join(tmp, "sunrise.sqlite")
    con = sqlite3.connect(dbp)
    con.executescript("""
    CREATE TABLE branches(branch_id INTEGER PRIMARY KEY, branch_name TEXT, area_type TEXT);
    CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT, category TEXT, cost_ugx INTEGER, price_ugx INTEGER);
    CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, sale_date TEXT, branch_id INTEGER REFERENCES branches(branch_id),
                       product_id INTEGER REFERENCES products(product_id), units INTEGER, unit_price_ugx INTEGER);
    CREATE TABLE daily_branch(day TEXT, branch_id INTEGER REFERENCES branches(branch_id), customers_counted INTEGER, rain_mm REAL,
                       PRIMARY KEY(day, branch_id));
    CREATE TABLE products_practice(product_id INTEGER, name TEXT, category TEXT);
    """)
    con.executemany("INSERT INTO branches VALUES(?,?,?)", [(b[0], b[1], b[2]) for b in BRANCHES])
    con.executemany("INSERT INTO products VALUES(?,?,?,?,?)", PRODUCTS)
    con.executemany("INSERT INTO sales VALUES(?,?,?,?,?,?)", sales)
    con.executemany("INSERT INTO daily_branch VALUES(?,?,?,?)", daily)
    pp = [(p[0], p[1], p[2]) for p in PRODUCTS]
    pp.append((6, "Juice", "Drinks"))  # the planted duplicate key
    con.executemany("INSERT INTO products_practice VALUES(?,?,?)", pp)
    con.commit()

    key = stats_from_db(con)

    # ---- property 3: fan-out
    fan_rows, fan_rev = con.execute(
        "SELECT COUNT(*), SUM(s.units*s.unit_price_ugx) FROM sales s JOIN products_practice p ON s.product_id=p.product_id").fetchone()
    key["fan_out"] = {"correct_rows": key["sales_rows"], "joined_rows": fan_rows,
                      "extra_rows": fan_rows - key["sales_rows"], "joined_revenue_ugx": fan_rev,
                      "overstatement_ugx": fan_rev - key["total_revenue_ugx"]}

    # ---- weekday effect (used by sessions 7/8/19)
    wk = {}
    for dow, label in ((5, "Saturday"),):
        r = con.execute("SELECT AVG(n) FROM (SELECT sale_date, COUNT(*) n FROM sales WHERE branch_id=1 AND strftime('%w',sale_date)=? GROUP BY sale_date)", (str(dow + 1 if dow < 6 else 0),)).fetchone()[0]
        wk["central_market_saturday_lines_per_day"] = round(r, 1)
    r = con.execute("SELECT AVG(n) FROM (SELECT sale_date, COUNT(*) n FROM sales WHERE branch_id=1 AND strftime('%w',sale_date) IN ('1','2','3','4') GROUP BY sale_date)").fetchone()[0]
    wk["central_market_monday_to_thursday_lines_per_day"] = round(r, 1)
    key["weekday_effect"] = wk

    # ---- daily table for EDA (sessions 13-15): customers, rain and revenue per branch-day
    drows = con.execute(
        "SELECT d.branch_id, d.customers_counted, d.rain_mm, COALESCE(SUM(s.units*s.unit_price_ugx),0) "
        "FROM daily_branch d LEFT JOIN sales s ON s.sale_date=d.day AND s.branch_id=d.branch_id GROUP BY d.day, d.branch_id").fetchall()

    def pearson(x, y):
        mx, my = sum(x) / len(x), sum(y) / len(y)
        sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
        return sxy / (sum((a - mx) ** 2 for a in x) ** 0.5 * sum((b - my) ** 2 for b in y) ** 0.5)
    key["corr_customers_vs_revenue"] = round(pearson([r[1] for r in drows], [r[3] for r in drows]), 3)
    # rain_mm is in the data as a variable to examine; the generator gives it almost no effect, and the key
    # records that so a lesson can ask "does rain matter here?" and get an honest, weak answer.
    key["corr_rain_vs_customers_by_branch"] = {
        b[1]: round(pearson([r[2] for r in drows if r[0] == b[0]], [r[1] for r in drows if r[0] == b[0]]), 3) for b in BRANCHES}

    # ---- raw export
    raw, counts, excluded_value = make_raw(sales, rnd)
    key["raw_defects"] = counts
    key["raw_file_rows"] = len(raw)
    key["cleaning_policy"] = ("drop exact duplicates; parse ISO and dd/mm/yyyy dates; strip().title() names mapped to product_id; "
                              "words to numbers; EXCLUDE rows with blank units and report them")
    key["cleaned_rows"] = key["sales_rows"] - counts["blank_units_rows"]
    key["excluded_blank_units_value_ugx"] = excluded_value
    key["cleaned_revenue_ugx"] = key["total_revenue_ugx"] - excluded_value
    key["residual_vs_database_ugx"] = excluded_value

    # ---- assert the three teaching properties
    assert key["mean_over_median"] >= 1.3, ("mean/median too flat", key["mean_over_median"])
    top_rev = max(key["revenue_by_branch"], key=key["revenue_by_branch"].get)
    top_rate = max(key["revenue_per_customer_by_branch"], key=key["revenue_per_customer_by_branch"].get)
    assert top_rev != top_rate, ("rate and count agree", top_rev, top_rate)
    assert key["fan_out"]["extra_rows"] > 0 and key["fan_out"]["overstatement_ugx"] > 0
    assert 0.4 <= key["corr_customers_vs_revenue"] <= 0.9, key["corr_customers_vs_revenue"]  # real but imperfect, never r=1
    assert 1200 <= key["sales_rows"] <= 1900, key["sales_rows"]
    key["properties"] = {"most_revenue_branch": top_rev, "best_revenue_per_customer_branch": top_rate}
    key["seed"] = a.seed
    key["synthetic"] = True

    # ---- write outputs
    con.close()
    con2 = sqlite3.connect(dbp)
    shutil.copy(dbp, os.path.join(a.out, "sunrise.sqlite"))
    write_csv(os.path.join(a.out, "branches.csv"), ["branch_id", "branch_name", "area_type"], [(b[0], b[1], b[2]) for b in BRANCHES])
    write_csv(os.path.join(a.out, "products.csv"), ["product_id", "name", "category", "cost_ugx", "price_ugx"], PRODUCTS)
    write_csv(os.path.join(a.out, "sales.csv"), ["sale_id", "sale_date", "branch_id", "product_id", "units", "unit_price_ugx"], sales)
    write_csv(os.path.join(a.out, "daily_branch.csv"), ["day", "branch_id", "customers_counted", "rain_mm"], daily)
    daily_rows = con2.execute(
        "SELECT d.day, b.branch_name, d.customers_counted, d.rain_mm, COUNT(s.sale_id), COALESCE(SUM(s.units*s.unit_price_ugx),0) "
        "FROM daily_branch d JOIN branches b USING(branch_id) LEFT JOIN sales s ON s.sale_date=d.day AND s.branch_id=d.branch_id "
        "GROUP BY d.day, d.branch_id ORDER BY d.day, d.branch_id").fetchall()
    write_csv(os.path.join(a.out, "daily_summary.csv"), ["day", "branch", "customers_counted", "rain_mm", "sale_lines", "revenue_ugx"], daily_rows)
    write_csv(os.path.join(a.out, "products_practice.csv"), ["product_id", "name", "category"], pp)
    write_csv(os.path.join(a.out, "sales_raw.csv"), ["sale_id", "sale_date", "branch", "product", "units", "unit_price_ugx"], raw)
    with open(os.path.join(a.out, "answer_key.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(key, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("wrote", a.out)
    print(json.dumps({k: key[k] for k in ("sales_rows", "total_revenue_ugx", "mean_over_median", "properties", "fan_out", "cleaned_rows", "cleaned_revenue_ugx", "residual_vs_database_ugx")}, indent=1))


if __name__ == "__main__":
    main()
