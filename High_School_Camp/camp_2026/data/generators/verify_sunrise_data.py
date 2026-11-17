#!/usr/bin/env python3
"""Independent check of the Sunrise Shops dataset against answer_key.json.

Re-derives every key number a second way (pandas on the CSVs, SQL on the
database), runs a student-style cleaning pipeline on sales_raw.csv, detects each
seeded defect from the file itself, and confirms the generator is reproducible.
Run:  python3 verify_sunrise_data.py
"""
import filecmp, json, os, shutil, sqlite3, subprocess, sys, tempfile
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(os.path.dirname(HERE), "sunrise")
key = json.load(open(os.path.join(D, "answer_key.json")))
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


sales = pd.read_csv(os.path.join(D, "sales.csv"))
prod = pd.read_csv(os.path.join(D, "products.csv"))
br = pd.read_csv(os.path.join(D, "branches.csv"))
day = pd.read_csv(os.path.join(D, "daily_branch.csv"))
sales["rev"] = sales["units"] * sales["unit_price_ugx"]

# --- clean data, second derivation
check("sales rows", len(sales) == key["sales_rows"], len(sales))
check("total revenue", int(sales.rev.sum()) == key["total_revenue_ugx"], int(sales.rev.sum()))
m = sales.merge(prod, on="product_id").merge(br, on="branch_id")
check("revenue by branch", m.groupby("branch_name").rev.sum().to_dict() == key["revenue_by_branch"])
check("revenue by category", m.groupby("category").rev.sum().to_dict() == key["revenue_by_category"])
cust = day.merge(br, on="branch_id").groupby("branch_name").customers_counted.sum()
check("customers counted", cust.to_dict() == key["customers_counted_by_branch"])
rpc = (m.groupby("branch_name").rev.sum() / cust).round(2).to_dict()
check("revenue per customer", rpc == key["revenue_per_customer_by_branch"], rpc)
check("mean/median", round(sales.rev.mean(), 2) == key["line_value_mean_ugx"] and sales.rev.median() == key["line_value_median_ugx"])
check("property 1: mean well above median", sales.rev.mean() / sales.rev.median() >= 1.3)
top_rev = max(rpc, key=lambda b: key["revenue_by_branch"][b])
top_rate = max(rpc, key=rpc.get)
check("property 2: most revenue != best rate", top_rev != top_rate, f"{top_rev} vs {top_rate}")
profit = int(((sales.unit_price_ugx - sales.merge(prod, on="product_id").cost_ugx) * sales.units).sum())
check("profit", profit == key["total_profit_ugx"], profit)

# --- database agrees with the CSVs
tmp = tempfile.mkdtemp()
shutil.copy(os.path.join(D, "sunrise.sqlite"), tmp)
con = sqlite3.connect(os.path.join(tmp, "sunrise.sqlite"))
check("db revenue = csv revenue", con.execute("SELECT SUM(units*unit_price_ugx) FROM sales").fetchone()[0] == key["total_revenue_ugx"])
n_dup, rev_dup = con.execute("SELECT COUNT(*), SUM(s.units*s.unit_price_ugx) FROM sales s JOIN products_practice p ON s.product_id=p.product_id").fetchone()
check("property 3: fan-out inflates rows and revenue", n_dup == key["fan_out"]["joined_rows"] > len(sales) and rev_dup > key["total_revenue_ugx"], f"{n_dup} rows, +{rev_dup - key['total_revenue_ugx']} UGX")
check("no orphan keys", con.execute("SELECT COUNT(*) FROM sales s LEFT JOIN products p USING(product_id) WHERE p.product_id IS NULL").fetchone()[0] == 0)
check("NULL-free clean tables", con.execute("SELECT COUNT(*) FROM sales WHERE units IS NULL OR sale_date IS NULL").fetchone()[0] == 0)
check("weekday effect present", key["weekday_effect"]["central_market_saturday_lines_per_day"] > key["weekday_effect"]["central_market_monday_to_thursday_lines_per_day"])
con.close()

# --- pandas routes for the Python-only track
pp = pd.read_csv(os.path.join(D, "products_practice.csv"))
fan = sales.merge(pp, on="product_id")
check("pandas fan-out matches key", len(fan) == key["fan_out"]["joined_rows"] and int(fan.rev.sum()) == key["fan_out"]["joined_revenue_ugx"], f"{len(fan)} rows")
check("merge on unique keys keeps row count", len(sales.merge(prod, on="product_id", validate="many_to_one")) == len(sales))
bd = sales.merge(day.rename(columns={"day": "sale_date"}), on=["sale_date", "branch_id"], how="right").groupby(["sale_date", "branch_id"]).agg(rev=("rev", "sum"), cust=("customers_counted", "first"), rain=("rain_mm", "first")).reset_index()
check("EDA: customers vs revenue correlation", round(bd.cust.corr(bd.rev), 3) == key["corr_customers_vs_revenue"] and 0.4 <= key["corr_customers_vs_revenue"] <= 0.9, round(bd.cust.corr(bd.rev), 3))

ds = pd.read_csv(os.path.join(D, "daily_summary.csv"))
check("daily_summary revenue = total revenue", int(ds.revenue_ugx.sum()) == key["total_revenue_ugx"] and len(ds) == 180)
check("daily_summary correlation matches key", round(ds.customers_counted.corr(ds.revenue_ugx), 3) == key["corr_customers_vs_revenue"])

# --- raw file: detect each defect from the file itself
raw = pd.read_csv(os.path.join(D, "sales_raw.csv"), dtype=str, keep_default_na=False)
check("raw file rows", len(raw) == key["raw_file_rows"], len(raw))
check("defect 1: duplicates", int(raw.duplicated().sum()) == key["raw_defects"]["duplicate_rows"])
check("defect 2: dd/mm/yyyy dates", int(raw.drop_duplicates().sale_date.str.contains("/").sum()) == key["raw_defects"]["mixed_date_format_rows"])
check("defect 3: blank units", int((raw.drop_duplicates().units == "").sum()) == key["raw_defects"]["blank_units_rows"])
words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
check("defect 5: word units", int(raw.drop_duplicates().units.isin(words).sum()) == key["raw_defects"]["units_as_words_rows"])
names = set(prod.name)
check("defect 4: messy names", int((~raw.drop_duplicates()["product"].isin(names)).sum()) == key["raw_defects"]["messy_name_rows"])

# --- a student-style pipeline lands on the key
c = raw.drop_duplicates().copy()
c["sale_date"] = pd.to_datetime(c.sale_date, format="mixed", dayfirst=True)
c["product"] = c["product"].str.strip().str.title()
fix = {n.title(): n for n in prod.name}
c["product"] = c["product"].map(fix)
c["units"] = c.units.replace(words)
blank = c[c.units == ""]
c = c[c.units != ""].copy()
c["units"] = c.units.astype(int)
c["unit_price_ugx"] = c.unit_price_ugx.astype(int)
check("pipeline: every name maps to a product", c["product"].notna().all())
check("pipeline: cleaned rows", len(c) == key["cleaned_rows"], len(c))
cleaned_rev = int((c.units * c.unit_price_ugx).sum())
check("pipeline: cleaned revenue", cleaned_rev == key["cleaned_revenue_ugx"], cleaned_rev)
check("residual vs database is named and exact", key["total_revenue_ugx"] - cleaned_rev == key["residual_vs_database_ugx"] == key["excluded_blank_units_value_ugx"], key["residual_vs_database_ugx"])
check("cleaned dates all in range", c.sale_date.min() >= pd.Timestamp("2026-09-01") and c.sale_date.max() <= pd.Timestamp("2026-10-30"))

# --- reproducibility
out = tempfile.mkdtemp()
subprocess.run([sys.executable, os.path.join(HERE, "build_sunrise_data.py"), "--out", out, "--seed", str(key["seed"])], check=True, capture_output=True)
same = all(filecmp.cmp(os.path.join(out, f), os.path.join(D, f), shallow=False) for f in
           ("sales.csv", "sales_raw.csv", "products.csv", "products_practice.csv", "daily_summary.csv", "branches.csv", "daily_branch.csv", "answer_key.json"))
check("regeneration is byte-identical (CSVs and key)", same)

print(f"\n{sum(results)}/{len(results)} checks passed")
sys.exit(0 if all(results) else 1)
