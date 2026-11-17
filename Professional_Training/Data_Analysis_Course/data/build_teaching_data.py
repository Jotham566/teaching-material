#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Riverside Distributors teaching dataset.

Standard library only: sqlite3, csv, json, random, datetime. It runs on any
Python 3.8+ with nothing installed, which matters because participants run it
on locked-down work laptops.

WHY THIS IS GENERATED RATHER THAN A REAL FILE
---------------------------------------------
The obvious core datasets for a course like this are either licensed for
internal use only (Tableau's Superstore) or NonCommercial (Olist), and a
course that might be paid for cannot ship either. Generating it also buys
three things a real file cannot:

  1. The defects are DELIBERATE and documented, so each one teaches a named
     skill instead of whatever mess the file happened to contain.
  2. Every lab answer is computed here, from the same data, and written to
     answer_key.json. No number in any handout was estimated.
  3. It is properly normalised, so the SQL joins are real joins.

The real, verified, CC BY 4.0 datasets come in from week 2 onward. This one is
the spine, not the whole diet.

SEEDED DEFECTS (the answer key lists the exact counts)
------------------------------------------------------
  1. Exact duplicate rows in order_items_raw.csv
  2. Customer names with inconsistent case and trailing spaces
  3. Missing customer_id on walk-in orders
  4. Returns entered as negative quantities in the raw extract
  5. Two date formats in one column of orders_raw.csv
  6. One product category priced in USD while everything else is UGX
  7. Discounts recorded above 1.0
  8. One customer duplicated under two ids

The SQLite database is the CLEAN version, so SQL sessions are about SQL. The
_raw.csv files carry the defects, so the pandas cleaning session is about
cleaning. Both describe the same business, and reconciling them is session 6.

Usage:  python3 build_teaching_data.py [--out DIR] [--seed N]
"""
import argparse
import csv
import json
import os
import random
import shutil
import sqlite3
import tempfile
from datetime import date, timedelta

# --------------------------------------------------------------- parameters
SEED = 20260913
N_CUSTOMERS = 400
N_PRODUCTS = 120
N_REPS = 12
N_ORDERS = 6000
START = date(2024, 1, 1)
END = date(2025, 12, 31)

REGIONS = ["Central", "Eastern", "Northern", "Western"]
CITIES = {
    "Central": ["Kampala", "Entebbe", "Mukono", "Wakiso", "Masaka"],
    "Eastern": ["Jinja", "Mbale", "Soroti", "Tororo", "Iganga"],
    "Northern": ["Gulu", "Lira", "Arua", "Kitgum", "Moroto"],
    "Western": ["Mbarara", "Fort Portal", "Hoima", "Kasese", "Kabale"],
}
SEGMENTS = ["Supermarket", "Wholesaler", "Kiosk", "Hotel", "Institution"]
CHANNELS = ["Field visit", "Phone", "WhatsApp", "Walk-in", "Online"]
STATUSES = ["Delivered", "Delivered", "Delivered", "Delivered", "Delivered",
            "Delivered", "Delivered", "Delivered", "Pending", "Cancelled"]
CATEGORIES = [
    # (name, low price UGX, high price UGX, margin)
    ("Cooking oil", 9000, 42000, 0.14),
    ("Maize flour", 4500, 26000, 0.11),
    ("Rice", 7000, 38000, 0.13),
    ("Sugar", 5500, 31000, 0.10),
    ("Soap and detergent", 3000, 19000, 0.22),
    ("Bottled water", 1200, 14000, 0.18),
    ("Tea and coffee", 6000, 48000, 0.26),
    ("Imported appliances", 85000, 950000, 0.31),   # priced in USD in the raw
]
RETURN_REASONS = ["Damaged in transit", "Wrong item delivered",
                  "Short shipment", "Expired stock", "Customer changed order"]

FIRST = ["Aisha", "Brian", "Catherine", "David", "Esther", "Fred", "Grace",
         "Henry", "Irene", "Joseph", "Kevin", "Lydia", "Moses", "Nancy",
         "Oscar", "Patricia", "Robert", "Sarah", "Timothy", "Violet",
         "Wilson", "Yasmin", "Zachary", "Betty", "Charles", "Diana",
         "Emmanuel", "Florence", "Geoffrey", "Hellen"]
LAST = ["Abebe", "Businge", "Chelimo", "Dhikusooka", "Ekwaru", "Furaha",
        "Gumisiriza", "Hakizimana", "Isabirye", "Jjuuko", "Kagaba",
        "Lubega", "Mugisha", "Nabirye", "Okello", "Piloya", "Rukundo",
        "Ssemwanga", "Tumwine", "Wanyama", "Zziwa", "Achieng", "Byaruhanga",
        "Kyomuhendo", "Namutebi", "Opio", "Ssekandi", "Twinomugisha"]
BIZ_SUFFIX = ["Traders", "Enterprises", "General Merchandise", "Supermarket",
              "Stores", "Distributors", "Wholesalers", "Trading Co",
              "Cash & Carry", "Retail Ltd"]

USD_UGX = 3780.0          # the rate the appliance prices are recorded in


def tidy(name):
    return " ".join(name.split())


def build(out_dir, seed):
    rng = random.Random(seed)
    os.makedirs(out_dir, exist_ok=True)

    # ------------------------------------------------------------ reps
    reps = []
    for i in range(N_REPS):
        reps.append({
            "rep_id": 100 + i,
            "rep_name": f"{rng.choice(FIRST)} {rng.choice(LAST)}",
            "region": REGIONS[i % len(REGIONS)],
            "hire_date": (START - timedelta(days=rng.randint(120, 2200))
                          ).isoformat(),
        })

    # ------------------------------------------------------------ customers
    customers = []
    for i in range(N_CUSTOMERS):
        region = rng.choice(REGIONS)
        seg = rng.choice(SEGMENTS)
        base = f"{rng.choice(LAST)} {rng.choice(BIZ_SUFFIX)}"
        customers.append({
            "customer_id": 1000 + i,
            "customer_name": base,
            "segment": seg,
            "region": region,
            "city": rng.choice(CITIES[region]),
            "signup_date": (START - timedelta(days=rng.randint(0, 1500))
                            ).isoformat(),
            "credit_limit_ugx": rng.choice([0, 0, 500000, 1000000, 2000000,
                                            5000000, 10000000]),
        })

    # DEFECT 8: one customer exists twice under two ids. Same name, same city,
    # different id, and both are used by orders. Entity resolution, gently.
    twin_src = customers[7]
    twin = dict(twin_src)
    twin["customer_id"] = 1999
    twin["signup_date"] = (date.fromisoformat(twin_src["signup_date"])
                           + timedelta(days=11)).isoformat()
    customers.append(twin)
    duplicate_pair = (twin_src["customer_id"], twin["customer_id"],
                      twin_src["customer_name"])

    # ------------------------------------------------------------ products
    products = []
    for i in range(N_PRODUCTS):
        cat, lo, hi, margin = CATEGORIES[i % len(CATEGORIES)]
        price = rng.randrange(lo, hi, 100)
        products.append({
            "product_id": 5000 + i,
            "product_name": f"{cat} item {i + 1:03d}",
            "category": cat,
            "pack_size": rng.choice(["1 x 1", "6 x 1", "12 x 1", "24 x 1",
                                     "1 x 5kg", "1 x 20L"]),
            "unit_cost_ugx": round(price * (1 - margin), 2),
            "unit_price_ugx": float(price),
        })

    # ------------------------------------------------------------ orders
    days = (END - START).days
    orders, items, returns = [], [], []
    line_seq = 0
    for oid in range(1, N_ORDERS + 1):
        # Business seasonality: December and a smaller Easter-ish bump, and
        # a weekday bias, so the time-series session has something real to
        # find rather than noise.
        while True:
            d = START + timedelta(days=rng.randint(0, days))
            w = 1.0
            if d.month == 12:
                w = 1.9
            elif d.month in (4, 8):
                w = 1.25
            elif d.month in (1, 2):
                w = 0.8
            if d.weekday() >= 5:
                w *= 0.35
            if rng.random() < w / 1.9:
                break
        cust = rng.choice(customers)
        rep = next(r for r in reps if r["region"] == cust["region"]) \
            if rng.random() < 0.82 else rng.choice(reps)
        channel = rng.choice(CHANNELS)
        orders.append({
            "order_id": 90000 + oid,
            "customer_id": cust["customer_id"],
            "rep_id": rep["rep_id"],
            "order_date": d.isoformat(),
            "channel": channel,
            "status": rng.choice(STATUSES),
        })
        for _ in range(rng.choices([1, 2, 3, 4, 5, 6, 7, 8],
                                   weights=[18, 22, 20, 14, 10, 7, 5, 4])[0]):
            line_seq += 1
            p = rng.choice(products)
            qty = rng.choices([1, 2, 3, 4, 6, 12, 24, 48],
                              weights=[26, 20, 14, 12, 10, 9, 6, 3])[0]
            disc = rng.choices([0.0, 0.0, 0.0, 0.05, 0.10, 0.15],
                               weights=[52, 12, 8, 14, 9, 5])[0]
            items.append({
                "order_id": 90000 + oid,
                "line_no": line_seq,
                "product_id": p["product_id"],
                "quantity": qty,
                "unit_price_ugx": p["unit_price_ugx"],
                "discount": disc,
            })

    # ------------------------------------------------------------ returns
    for it in items:
        o = next(o for o in orders if o["order_id"] == it["order_id"])
        if o["status"] != "Delivered":
            continue
        if rng.random() < 0.031:
            rq = it["quantity"] if rng.random() < 0.45 else max(
                1, it["quantity"] // 2)
            returns.append({
                "order_id": it["order_id"],
                "line_no": it["line_no"],
                "return_date": (date.fromisoformat(o["order_date"])
                                + timedelta(days=rng.randint(1, 30))
                                ).isoformat(),
                "reason": rng.choice(RETURN_REASONS),
                "quantity_returned": rq,
            })

    # ------------------------------------------------------------ fx
    fx, rate = [], USD_UGX
    d = START
    while d <= END:
        rate += rng.uniform(-6, 6.5)
        fx.append({"rate_date": d.isoformat(), "usd_ugx": round(rate, 2)})
        d += timedelta(days=1)

    return dict(reps=reps, customers=customers, products=products,
                orders=orders, items=items, returns=returns, fx=fx,
                duplicate_pair=duplicate_pair, rng=rng)


# --------------------------------------------------------------- the clean DB
SCHEMA = """
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS returns;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS reps;
DROP TABLE IF EXISTS fx_rates;

CREATE TABLE reps (
    rep_id     INTEGER PRIMARY KEY,
    rep_name   TEXT NOT NULL,
    region     TEXT NOT NULL,
    hire_date  TEXT NOT NULL
);
CREATE TABLE customers (
    customer_id      INTEGER PRIMARY KEY,
    customer_name    TEXT NOT NULL,
    segment          TEXT NOT NULL,
    region           TEXT NOT NULL,
    city             TEXT NOT NULL,
    signup_date      TEXT NOT NULL,
    credit_limit_ugx INTEGER NOT NULL
);
CREATE TABLE products (
    product_id     INTEGER PRIMARY KEY,
    product_name   TEXT NOT NULL,
    category       TEXT NOT NULL,
    pack_size      TEXT NOT NULL,
    unit_cost_ugx  REAL NOT NULL,
    unit_price_ugx REAL NOT NULL
);
CREATE TABLE orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER,                      -- NULL for walk-in trade
    rep_id      INTEGER NOT NULL REFERENCES reps(rep_id),
    order_date  TEXT NOT NULL,
    channel     TEXT NOT NULL,
    status      TEXT NOT NULL
);
CREATE TABLE order_items (
    order_id       INTEGER NOT NULL REFERENCES orders(order_id),
    line_no        INTEGER PRIMARY KEY,
    product_id     INTEGER NOT NULL REFERENCES products(product_id),
    quantity       INTEGER NOT NULL,
    unit_price_ugx REAL NOT NULL,
    discount       REAL NOT NULL
);
CREATE TABLE returns (
    order_id          INTEGER NOT NULL,
    line_no           INTEGER NOT NULL,
    return_date       TEXT NOT NULL,
    reason            TEXT NOT NULL,
    quantity_returned INTEGER NOT NULL
);
CREATE TABLE fx_rates (
    rate_date TEXT PRIMARY KEY,
    usd_ugx   REAL NOT NULL
);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_cust ON orders(customer_id);
CREATE INDEX idx_items_order ON order_items(order_id);
"""


def write_db(path, D, walkins):
    if os.path.exists(path):
        os.remove(path)
    con = sqlite3.connect(path)
    con.executescript(SCHEMA)
    con.executemany("INSERT INTO reps VALUES (?,?,?,?)",
                    [(r["rep_id"], r["rep_name"], r["region"], r["hire_date"])
                     for r in D["reps"]])
    con.executemany("INSERT INTO customers VALUES (?,?,?,?,?,?,?)",
                    [(c["customer_id"], c["customer_name"], c["segment"],
                      c["region"], c["city"], c["signup_date"],
                      c["credit_limit_ugx"]) for c in D["customers"]])
    con.executemany("INSERT INTO products VALUES (?,?,?,?,?,?)",
                    [(p["product_id"], p["product_name"], p["category"],
                      p["pack_size"], p["unit_cost_ugx"], p["unit_price_ugx"])
                     for p in D["products"]])
    con.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?)",
                    [(o["order_id"],
                      None if o["order_id"] in walkins else o["customer_id"],
                      o["rep_id"], o["order_date"], o["channel"], o["status"])
                     for o in D["orders"]])
    con.executemany("INSERT INTO order_items VALUES (?,?,?,?,?,?)",
                    [(i["order_id"], i["line_no"], i["product_id"],
                      i["quantity"], i["unit_price_ugx"], i["discount"])
                     for i in D["items"]])
    con.executemany("INSERT INTO returns VALUES (?,?,?,?,?)",
                    [(r["order_id"], r["line_no"], r["return_date"],
                      r["reason"], r["quantity_returned"])
                     for r in D["returns"]])
    con.executemany("INSERT INTO fx_rates VALUES (?,?)",
                    [(f["rate_date"], f["usd_ugx"]) for f in D["fx"]])
    con.commit()
    return con


# --------------------------------------------------------------- the raw CSVs
def write_csv(path, rows, fields):
    # newline="\n", not newline="": the csv module writes \r\n by default on
    # every platform, and the repository normalises CSV to LF, so the default
    # makes nine files show as modified after every regeneration.
    with open(path, "w", newline="\n", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def write_raw(out_dir, D, walkins, rng):
    """The same business, exported badly. This is what week 2 cleans."""
    defects = {}

    # --- orders_raw.csv : DEFECT 5, two date formats in one column
    rows, alt = [], 0
    for o in D["orders"]:
        d = date.fromisoformat(o["order_date"])
        if rng.random() < 0.18:
            ds = d.strftime("%d/%m/%Y")
            alt += 1
        else:
            ds = d.isoformat()
        rows.append({
            "order_id": o["order_id"],
            "customer_id": ("" if o["order_id"] in walkins
                            else o["customer_id"]),
            "rep_id": o["rep_id"],
            "order_date": ds,
            "channel": o["channel"],
            "status": o["status"],
        })
    defects["dates_in_dd_mm_yyyy"] = alt
    defects["orders_missing_customer_id"] = len(walkins)
    write_csv(os.path.join(out_dir, "orders_raw.csv"), rows,
              ["order_id", "customer_id", "rep_id", "order_date", "channel",
               "status"])

    # --- customers_raw.csv : DEFECT 2, case and whitespace
    rows, messy = [], 0
    for c in D["customers"]:
        nm = c["customer_name"]
        r = rng.random()
        if r < 0.12:
            nm = nm.upper(); messy += 1
        elif r < 0.22:
            nm = nm.lower(); messy += 1
        elif r < 0.34:
            nm = "  " + nm + "   "; messy += 1
        rows.append({"customer_id": c["customer_id"], "customer_name": nm,
                     "segment": c["segment"], "region": c["region"],
                     "city": c["city"], "signup_date": c["signup_date"],
                     "credit_limit_ugx": c["credit_limit_ugx"]})
    defects["customer_names_messy"] = messy
    write_csv(os.path.join(out_dir, "customers_raw.csv"), rows,
              ["customer_id", "customer_name", "segment", "region", "city",
               "signup_date", "credit_limit_ugx"])

    # --- order_items_raw.csv : DEFECTS 1, 4, 6, 7
    cat_of = {p["product_id"]: p["category"] for p in D["products"]}
    rows = []
    usd_rows = bad_disc = 0
    for it in D["items"]:
        price = it["unit_price_ugx"]
        # DEFECT 6: the imported category was entered in USD by a different
        # team. Nothing in the file says so, which is the whole lesson.
        if cat_of[it["product_id"]] == "Imported appliances":
            price = round(price / USD_UGX, 2)
            usd_rows += 1
        disc = it["discount"]
        # DEFECT 7: a few discounts recorded as percentages, so 15 not 0.15
        if disc > 0 and rng.random() < 0.035:
            disc = disc * 100
            bad_disc += 1
        rows.append({"order_id": it["order_id"], "line_no": it["line_no"],
                     "product_id": it["product_id"], "quantity": it["quantity"],
                     "unit_price": price, "discount": disc})
    defects["lines_priced_in_usd"] = usd_rows
    defects["discounts_over_one"] = bad_disc

    # DEFECT 4: returns appended as negative-quantity lines rather than kept
    # in their own table, which is how a lot of real systems do it
    neg = 0
    for r in D["returns"]:
        src = next(i for i in D["items"] if i["line_no"] == r["line_no"])
        price = src["unit_price_ugx"]
        if cat_of[src["product_id"]] == "Imported appliances":
            price = round(price / USD_UGX, 2)
        rows.append({"order_id": r["order_id"], "line_no": src["line_no"],
                     "product_id": src["product_id"],
                     "quantity": -r["quantity_returned"],
                     "unit_price": price, "discount": src["discount"]})
        neg += 1
    defects["negative_quantity_lines"] = neg

    # DEFECT 1: exact duplicate rows, from an export run twice
    dups = rng.sample(rows, 40)
    rows.extend([dict(r) for r in dups])
    defects["duplicate_rows"] = 40
    rng.shuffle(rows)
    write_csv(os.path.join(out_dir, "order_items_raw.csv"), rows,
              ["order_id", "line_no", "product_id", "quantity", "unit_price",
               "discount"])
    return defects, len(rows)


# --------------------------------------------------------------- answer key
def answer_key(con, D, defects, raw_rows, duplicate_pair):
    """Every number a handout quotes is computed here, by running the query.

    If a lab answer is not in this dict, the lab must not assert it.
    """
    q = lambda sql: con.execute(sql).fetchall()          # noqa: E731
    one = lambda sql: con.execute(sql).fetchone()[0]     # noqa: E731

    REV = ("SUM(oi.quantity * oi.unit_price_ugx * (1 - oi.discount))")
    key = {}
    key["generated_with_seed"] = SEED
    key["row_counts"] = {t: one(f"SELECT COUNT(*) FROM {t}") for t in
                         ("reps", "customers", "products", "orders",
                          "order_items", "returns", "fx_rates")}
    key["raw_order_items_rows"] = raw_rows
    key["seeded_defects"] = defects
    key["duplicate_customer"] = {"kept_id": duplicate_pair[0],
                                 "duplicate_id": duplicate_pair[1],
                                 "name": duplicate_pair[2]}

    # --- session 2
    key["s2"] = {}
    key["s2"]["orders_total"] = one("SELECT COUNT(*) FROM orders")
    key["s2"]["orders_delivered"] = one(
        "SELECT COUNT(*) FROM orders WHERE status = 'Delivered'")
    key["s2"]["orders_cancelled"] = one(
        "SELECT COUNT(*) FROM orders WHERE status = 'Cancelled'")
    key["s2"]["count_star_vs_customer_id"] = [
        one("SELECT COUNT(*) FROM orders"),
        one("SELECT COUNT(customer_id) FROM orders")]
    key["s2"]["orders_by_channel"] = [list(r) for r in q(
        "SELECT channel, COUNT(*) c FROM orders GROUP BY channel "
        "ORDER BY c DESC")]
    key["s2"]["products_per_category"] = [list(r) for r in q(
        "SELECT category, COUNT(*) FROM products GROUP BY category "
        "ORDER BY category")]
    key["s2"]["segments_over_80_customers"] = [list(r) for r in q(
        "SELECT segment, COUNT(*) n FROM customers GROUP BY segment "
        "HAVING n > 80 ORDER BY n DESC")]

    # --- session 3
    key["s3"] = {}
    key["s3"]["revenue_all_ugx"] = round(one(
        f"SELECT {REV} FROM order_items oi"), 2)
    key["s3"]["revenue_delivered_ugx"] = round(one(
        f"SELECT {REV} FROM order_items oi "
        "JOIN orders o ON o.order_id = oi.order_id "
        "WHERE o.status = 'Delivered'"), 2)
    key["s3"]["inner_join_drops_rows"] = one(
        "SELECT COUNT(*) FROM orders WHERE customer_id IS NULL")
    key["s3"]["revenue_lost_to_inner_join_ugx"] = round(one(
        f"SELECT {REV} FROM order_items oi "
        "JOIN orders o ON o.order_id = oi.order_id "
        "WHERE o.customer_id IS NULL"), 2)
    key["s3"]["revenue_by_region_ugx"] = [[r[0], round(r[1], 2)] for r in q(
        f"SELECT c.region, {REV} rev FROM order_items oi "
        "JOIN orders o ON o.order_id = oi.order_id "
        "JOIN customers c ON c.customer_id = o.customer_id "
        "WHERE o.status = 'Delivered' GROUP BY c.region ORDER BY rev DESC")]
    key["s3"]["top_rep_2025"] = [[r[0], round(r[1], 2)] for r in q(
        f"SELECT r.rep_name, {REV} rev FROM order_items oi "
        "JOIN orders o ON o.order_id = oi.order_id "
        "JOIN reps r ON r.rep_id = o.rep_id "
        "WHERE o.status = 'Delivered' AND o.order_date >= '2025-01-01' "
        "GROUP BY r.rep_name ORDER BY rev DESC LIMIT 3")]
    # The raw CSVs record the imported category in USD to the cent, so
    # converting back at 3,780 cannot recover the shilling price exactly. The
    # residual is tiny and it is REAL: a participant who cleans the CSVs
    # correctly lands here, not on the database total. Both numbers are in the
    # key so the lab can state the expected gap instead of sending people to
    # chase a rounding error for an hour.
    cat = {r[0]: r[1] for r in con.execute(
        "SELECT product_id, category FROM products")}
    status = {r[0]: r[1] for r in con.execute(
        "SELECT order_id, status FROM orders")}
    rt = 0.0
    usd_lines = 0
    for oid, pid, qty, price, disc in con.execute(
            "SELECT order_id, product_id, quantity, unit_price_ugx, discount "
            "FROM order_items"):
        if status[oid] != "Delivered":
            continue
        if cat[pid] == "Imported appliances":
            price = round(price / USD_UGX, 2) * USD_UGX
            usd_lines += 1
        rt += qty * price * (1 - disc)
    key["s3"]["revenue_delivered_from_raw_ugx"] = round(rt, 2)
    key["s3"]["usd_rounding_residual_ugx"] = round(
        key["s3"]["revenue_delivered_ugx"] - rt, 2)
    key["s3"]["usd_lines_delivered"] = usd_lines

    key["s3"]["returns_value_ugx"] = round(one(
        "SELECT SUM(rt.quantity_returned * oi.unit_price_ugx "
        "           * (1 - oi.discount)) "
        "FROM returns rt JOIN order_items oi ON oi.line_no = rt.line_no"), 2)

    # --- session 7, the statistics that need a real distribution
    vals = [r[0] for r in q(
        f"SELECT {REV} v FROM order_items oi GROUP BY oi.order_id")]
    vals.sort()
    n = len(vals)
    pct = lambda p: round(vals[min(n - 1, int(p / 100.0 * n))], 2)  # noqa: E731
    key["s7"] = {
        "orders_with_value": n,
        "order_value_mean_ugx": round(sum(vals) / n, 2),
        "order_value_median_ugx": pct(50),
        "order_value_p10_ugx": pct(10),
        "order_value_p90_ugx": pct(90),
        "order_value_max_ugx": round(vals[-1], 2),
        "mean_over_median": round((sum(vals) / n) / pct(50), 3),
    }
    key["s7"]["revenue_by_month_ugx"] = [[r[0], round(r[1], 2)] for r in q(
        f"SELECT substr(o.order_date, 1, 7) m, {REV} rev "
        "FROM order_items oi JOIN orders o ON o.order_id = oi.order_id "
        "WHERE o.status = 'Delivered' GROUP BY m ORDER BY m")]
    key["s7"]["return_rate_by_region"] = [[r[0], round(r[1], 4)] for r in q(
        "SELECT c.region, "
        "  1.0 * SUM(CASE WHEN rt.line_no IS NOT NULL THEN 1 ELSE 0 END) "
        "      / COUNT(*) AS rate "
        "FROM order_items oi "
        "JOIN orders o ON o.order_id = oi.order_id "
        "JOIN customers c ON c.customer_id = o.customer_id "
        "LEFT JOIN returns rt ON rt.line_no = oi.line_no "
        "GROUP BY c.region ORDER BY rate DESC")]
    key["s7"]["returns_count_by_region"] = [list(r) for r in q(
        "SELECT c.region, COUNT(*) n FROM returns rt "
        "JOIN order_items oi ON oi.line_no = rt.line_no "
        "JOIN orders o ON o.order_id = oi.order_id "
        "JOIN customers c ON c.customer_id = o.customer_id "
        "GROUP BY c.region ORDER BY n DESC")]
    return key


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--seed", type=int, default=SEED)
    a = ap.parse_args()

    D = build(a.out, a.seed)
    rng = D["rng"]

    # DEFECT 3: walk-in trade has no customer on the order. 3% of orders.
    walkins = set(o["order_id"] for o in D["orders"] if rng.random() < 0.03)

    # the twin customer has to actually be used, or nobody can find it
    twin_kept, twin_dup, _ = D["duplicate_pair"]
    for o in rng.sample(D["orders"], 14):
        o["customer_id"] = twin_dup

    # SQLite is built on local disk and then copied into place. On a network
    # share, a synced folder or a mounted drive, sqlite3 can fail mid-script
    # with "disk I/O error" because it cannot take the locks it wants. Several
    # participants will have OneDrive or a mapped drive, so this is the normal
    # case rather than an edge case.
    db = os.path.join(a.out, "riverside.db")
    tmp = os.path.join(tempfile.gettempdir(),
                       "riverside_build_%d.db" % os.getpid())
    con = write_db(tmp, D, walkins)
    defects, raw_rows = write_raw(a.out, D, walkins, rng)
    key = answer_key(con, D, defects, raw_rows, D["duplicate_pair"])

    with open(os.path.join(a.out, "answer_key.json"), "w",
              encoding="utf-8") as fh:
        json.dump(key, fh, indent=2, sort_keys=True, ensure_ascii=True)

    # a clean CSV set as well, for the Power BI sessions
    write_csv(os.path.join(a.out, "customers.csv"), D["customers"],
              list(D["customers"][0].keys()))
    write_csv(os.path.join(a.out, "products.csv"), D["products"],
              list(D["products"][0].keys()))
    write_csv(os.path.join(a.out, "reps.csv"), D["reps"],
              list(D["reps"][0].keys()))
    write_csv(os.path.join(a.out, "orders.csv"),
              [{**o, "customer_id": ("" if o["order_id"] in walkins
                                     else o["customer_id"])}
               for o in D["orders"]], list(D["orders"][0].keys()))
    write_csv(os.path.join(a.out, "order_items.csv"), D["items"],
              list(D["items"][0].keys()))
    write_csv(os.path.join(a.out, "returns.csv"), D["returns"],
              list(D["returns"][0].keys()))
    con.close()
    shutil.copyfile(tmp, db)
    os.remove(tmp)

    print(f"built {db}")
    for t, c in key["row_counts"].items():
        print(f"  {t:<12} {c:>7,}")
    print(f"  raw item rows {raw_rows:,} "
          f"(clean {key['row_counts']['order_items']:,} + "
          f"{defects['negative_quantity_lines']} returns + 40 duplicates)")
    print("\nseeded defects:")
    for k, v in sorted(defects.items()):
        print(f"  {k:<28} {v}")
    print(f"\nrevenue, delivered orders: UGX "
          f"{key['s3']['revenue_delivered_ugx']:,.0f}")
    print(f"mean order value UGX {key['s7']['order_value_mean_ugx']:,.0f} "
          f"vs median UGX {key['s7']['order_value_median_ugx']:,.0f} "
          f"(ratio {key['s7']['mean_over_median']})")


if __name__ == "__main__":
    main()
