# -*- coding: utf-8 -*-
"""Verify the Data Analysis track. Run this after ANY edit to the content,
the generator or the labs.

The rule this enforces: no number reaches a handout without having been
produced by running something. So this script

  1. extracts every ```sql block from the labs and EXECUTES it against the
     real database, failing on any error,
  2. re-derives each asserted answer independently and compares it to the
     answer key,
  3. runs the pandas cleaning pipeline from the Python lab end to end and
     checks it lands on the target revenue,
  4. checks the schedule arithmetic, the assessment weights and the tool
     hours,
  5. checks house style, because the standing instruction is no "X, not Y"
     antithesis.

A check that cannot fail is not a check, so each section prints what it
actually compared.
"""
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)

import da_content as C                                   # noqa: E402

TRACK = os.path.join(_ROOT, "DataAnalysis_Track")
DATA = os.path.join(TRACK, "data")
LABS = os.path.join(TRACK, "labs")
DB = os.path.join(DATA, "riverside.db")

FAIL = []
CHECKS = 0


def ok(msg):
    global CHECKS
    CHECKS += 1
    print("  pass  " + msg)


def bad(msg):
    FAIL.append(msg)
    print("  FAIL  " + msg)


def section(t):
    print("\n" + t)


# ---------------------------------------------------------------- 1. schedule
section("1. Schedule and weights")
if sum(m for m, _, _ in C.BLOCK) == C.HOURS_PER_SESSION * 60:
    ok("the three-hour block sums to %d minutes"
       % (C.HOURS_PER_SESSION * 60))
else:
    bad("block does not sum to three hours")

if C.WEEKS * C.SESSIONS_PER_WEEK * C.HOURS_PER_SESSION == C.TOTAL_HOURS == 45:
    ok("5 weeks x 3 sessions x 3 hours = %d hours" % C.TOTAL_HOURS)
else:
    bad("total hours do not reconcile")

if len(C.SESSIONS) == 15 and [s["n"] for s in C.SESSIONS] == list(range(1, 16)):
    ok("fifteen sessions, numbered 1 to 15 with no gaps")
else:
    bad("session numbering is wrong")

wk = {}
for s in C.SESSIONS:
    wk.setdefault(s["week"], []).append(s["n"])
if all(len(v) == 3 for v in wk.values()) and len(wk) == 5:
    ok("three sessions in each of five weeks")
else:
    bad("weeks are not three sessions each: %r" % wk)

tot = sum(w for _, w, _, _ in C.ASSESSMENT)
if tot == 100:
    ok("assessment weights sum to 100")
else:
    bad("assessment weights sum to %d" % tot)

if sum(C.TOOL_HOURS.values()) == C.TOTAL_HOURS:
    ok("tool hours sum to the track total (%s)"
       % ", ".join("%s %dh" % kv for kv in C.TOOL_HOURS.items()))
else:
    bad("tool hours do not sum to the total")

# Python-heavy was a requirement, not a preference. Statistics, charts and
# the investigation are all taught IN Python, so the family total is what
# has to clear the bar.
if C.PYTHON_HOURS >= 2 * max(C.TOOL_HOURS["SQL"], C.TOOL_HOURS["Power BI"]):
    ok("the Python family gets %dh of %dh, at least twice either other tool"
       % (C.PYTHON_HOURS, C.TOTAL_HOURS))
else:
    bad("the track is not Python-heavy: %dh against SQL %dh"
        % (C.PYTHON_HOURS, C.TOOL_HOURS["SQL"]))

# The foundations were the whole point of the replan. Two sessions with no
# code is a decision that can be quietly undone by an edit, so assert it.
_found = [s for s in C.SESSIONS if s["tool"] == "Foundations"]
if len(_found) == 2 and [s["n"] for s in _found] == [1, 2]:
    ok("sessions 1 and 2 are foundations, before any tool")
else:
    bad("the two foundation sessions are not first: %r"
        % [s["n"] for s in _found])

# every session has to be teachable: outcomes, both blocks, a lab, homework
for s in C.SESSIONS:
    miss = [f for f in ("title", "b1", "b2", "lab", "home", "trap", "roadmap")
            if not str(s.get(f, "")).strip()]
    if miss:
        bad("session %d is missing %s" % (s["n"], miss))
if not FAIL:
    ok("all twelve sessions have outcomes, two blocks, a lab, homework, "
       "a trap and a roadmap mapping")
for s in C.SESSIONS:
    if not 2 <= len(s["outcomes"]) <= 4:
        bad("session %d has %d outcomes" % (s["n"], len(s["outcomes"])))

# ------------------------------------------------- 1b. vocabulary and figures
section("1b. Vocabulary, glossary and figures")
_no_vocab = [s["n"] for s in C.SESSIONS if not s.get("vocab")]
if _no_vocab:
    bad("sessions with no vocabulary list: %r" % _no_vocab)
else:
    ok("all fifteen sessions define their new words before using them "
       "(%d terms in total)" % len(C.GLOSSARY))

_sizes = [len(s["vocab"]) for s in C.SESSIONS]
if max(_sizes) <= 10:
    ok("no session introduces more than %d new terms (a beginner cannot "
       "hold more)" % max(_sizes))
else:
    bad("a session introduces %d new terms, which is too many for one "
        "evening" % max(_sizes))

# The glossary builder raises on a duplicate definition, so reaching here
# proves no term is defined twice. Worth stating, because the failure mode
# is two sessions quietly disagreeing about what a word means.
ok("no term is defined twice across the fifteen sessions")

_with_excel = sum(1 for _, _, x, _ in C.GLOSSARY if x)
if _with_excel >= len(C.GLOSSARY) // 3:
    ok("%d of %d terms carry a spreadsheet equivalent, which is what makes "
       "this teachable to this room" % (_with_excel, len(C.GLOSSARY)))
else:
    bad("only %d terms have a spreadsheet equivalent" % _with_excel)

FIGS = os.path.join(TRACK, "figs")
_built = set(f[:-4] for f in os.listdir(FIGS) if f.endswith(".png"))
_used = {f for s in C.SESSIONS for f in s.get("figs", [])}
if _used - _built:
    bad("sessions reference figures that were never built: %r"
        % sorted(_used - _built))
else:
    ok("every figure referenced by a session exists (%d of them)"
       % len(_used))
if _built - _used:
    bad("figures built but referenced by no session: %r"
        % sorted(_built - _used))
else:
    ok("no orphan figures")
for f in sorted(_built):
    if os.path.getsize(os.path.join(FIGS, f + ".png")) < 10000:
        bad("%s.png is under 10 KB, so it is probably blank" % f)

# ---------------------------------------------------------------- 2. datasets
section("2. Datasets")
for d in C.DATASETS:
    for f in ("name", "url", "licence", "shape", "account", "use"):
        if not str(d.get(f, "")).strip():
            bad("dataset %s has no %s" % (d.get("key"), f))
ok("%d datasets, each with a licence, a shape and an account note"
   % len(C.DATASETS))

# The whole point of the dataset work was commercial safety. Enforce it.
banned = [d["name"] for d in C.DATASETS
          if "NC" in d["licence"] or "NonCommercial" in d["licence"]]
if banned:
    bad("NonCommercial dataset in the live list: %r" % banned)
else:
    ok("no NonCommercial or internal-use dataset in the live list")

if len(C.CUT) >= 3:
    ok("%d pieces of cut material recorded with reasons, so they do not "
       "creep back" % len(C.CUT))
else:
    bad("what was cut is not recorded")

if len(C.REJECTED) >= 5:
    ok("%d rejected datasets recorded with reasons, so they do not get "
       "re-proposed" % len(C.REJECTED))
else:
    bad("rejected datasets not recorded")

# ---------------------------------------------------------------- 3. the data
section("3. The generated dataset")
if not os.path.exists(DB):
    bad("riverside.db is missing. Run data/build_teaching_data.py")
    print("\n%d checks, %d failures" % (CHECKS, len(FAIL)))
    sys.exit(1)

with open(os.path.join(DATA, "answer_key.json"), encoding="utf-8") as fh:
    K = json.load(fh)
# Opened from a local copy. On a mounted or synced folder, sqlite3 raises
# "attempt to write a readonly database" even for a SELECT, because it still
# wants to touch the journal. Copying first makes the verifier work in the
# same places the generator does.
_tmp = os.path.join(tempfile.gettempdir(), "verify_riverside_%d.db"
                    % os.getpid())
shutil.copyfile(DB, _tmp)
con = sqlite3.connect(_tmp)

for t, expected in K["row_counts"].items():
    got = con.execute("SELECT COUNT(*) FROM %s" % t).fetchone()[0]
    if got != expected:
        bad("%s has %d rows, key says %d" % (t, got, expected))
ok("every table's row count matches the answer key")

# referential integrity, which the labs' joins depend on
orphan_items = con.execute(
    "SELECT COUNT(*) FROM order_items oi "
    "LEFT JOIN orders o ON o.order_id = oi.order_id "
    "WHERE o.order_id IS NULL").fetchone()[0]
orphan_ret = con.execute(
    "SELECT COUNT(*) FROM returns rt "
    "LEFT JOIN order_items oi ON oi.line_no = rt.line_no "
    "WHERE oi.line_no IS NULL").fetchone()[0]
bad_cust = con.execute(
    "SELECT COUNT(*) FROM orders o "
    "LEFT JOIN customers c ON c.customer_id = o.customer_id "
    "WHERE o.customer_id IS NOT NULL AND c.customer_id IS NULL").fetchone()[0]
if orphan_items or orphan_ret or bad_cust:
    bad("orphan rows: items %d, returns %d, orders with unknown customer %d"
        % (orphan_items, orphan_ret, bad_cust))
else:
    ok("no orphan rows: every item, return and customer id resolves")

# the walk-in NULLs are deliberate and the lab's best trap depends on them
nulls = con.execute(
    "SELECT COUNT(*) FROM orders WHERE customer_id IS NULL").fetchone()[0]
if nulls == K["s3"]["inner_join_drops_rows"] > 0:
    ok("%d walk-in orders carry a NULL customer, which is what makes the "
       "INNER JOIN trap real" % nulls)
else:
    bad("walk-in NULL count is %d, key says %d"
        % (nulls, K["s3"]["inner_join_drops_rows"]))

# the skew the statistics session needs has to actually be there
if K["s7"]["mean_over_median"] > 2.0:
    ok("order value is genuinely skewed: mean is %.2fx the median, so the "
       "session 7 lesson is in the data rather than asserted"
       % K["s7"]["mean_over_median"])
else:
    bad("order value is not skewed enough for the statistics session")

# and so does the rate-versus-count reversal
rate_top = K["s7"]["return_rate_by_region"][0][0]
count_top = K["s7"]["returns_count_by_region"][0][0]
if rate_top != count_top:
    ok("rate and count disagree as intended: most returns in %s, highest "
       "return RATE in %s" % (count_top, rate_top))
else:
    bad("the same region leads on both count and rate, so the session 7 "
        "example does not work")

# seasonality, which the time-series block promises
months = dict(K["s7"]["revenue_by_month_ugx"])
dec = [v for m, v in months.items() if m.endswith("-12")]
feb = [v for m, v in months.items() if m.endswith("-02")]
if dec and feb and min(dec) > 1.4 * max(feb):
    ok("December beats February by at least 1.4x in both years, so the "
       "seasonality block has something to find")
else:
    bad("no clear seasonality in the generated data")

# ------------------------------------------------------- 4. execute every SQL
section("4. Every SQL block in the labs, executed")
sql_txt = open(os.path.join(LABS, "lab_sql.md"), encoding="utf-8").read()
blocks = re.findall(r"```sql\n(.*?)```", sql_txt, re.S)
ran = 0
for b in blocks:
    stmt = b.strip()
    if not stmt:
        continue
    try:
        con.execute(stmt).fetchall()
        ran += 1
    except Exception as e:                                # noqa: BLE001
        bad("SQL block failed: %s ... -> %s" % (stmt[:70].replace("\n", " "),
                                                e))
if ran and not any("SQL block failed" in f for f in FAIL):
    ok("%d SQL blocks from lab_sql.md executed without error" % ran)
if ran < 9:
    bad("only %d SQL blocks found; the lab should have at least 9" % ran)

# ------------------------------------- 5. re-derive the answers independently
section("5. Answers re-derived a different way")
# The key computed revenue with SUM() in SQL. Re-derive it in Python from the
# raw rows, so a mistake in the SQL expression cannot agree with itself.
rows = con.execute(
    "SELECT oi.quantity, oi.unit_price_ugx, oi.discount, o.status, "
    "       o.customer_id "
    "FROM order_items oi JOIN orders o ON o.order_id = oi.order_id"
).fetchall()
rev_all = sum(q * p * (1 - d) for q, p, d, _, _ in rows)
rev_del = sum(q * p * (1 - d) for q, p, d, st, _ in rows if st == "Delivered")
rev_null = sum(q * p * (1 - d) for q, p, d, _, c in rows if c is None)

for label, got, want in (
        ("revenue, all lines", rev_all, K["s3"]["revenue_all_ugx"]),
        ("revenue, delivered", rev_del, K["s3"]["revenue_delivered_ugx"]),
        ("revenue on walk-in orders", rev_null,
         K["s3"]["revenue_lost_to_inner_join_ugx"])):
    if abs(got - want) < 1.0:
        ok("%s re-derived in Python: UGX %,.0f".replace(",.0f", ",.0f")
           % (label, got) if False else
           "%s re-derived in Python: UGX %s" % (label, format(got, ",.0f")))
    else:
        bad("%s: Python %s, key %s" % (label, got, want))

# the INNER JOIN really must lose revenue, or the lab's headline trap is a lie
inner = con.execute(
    "SELECT SUM(oi.quantity * oi.unit_price_ugx * (1 - oi.discount)) "
    "FROM order_items oi "
    "JOIN orders o ON o.order_id = oi.order_id "
    "JOIN customers c ON c.customer_id = o.customer_id").fetchone()[0]
if abs((rev_all - inner) - rev_null) < 1.0:
    ok("the INNER JOIN to customers loses exactly the walk-in revenue, "
       "UGX %s" % format(rev_null, ",.0f"))
else:
    bad("the walk-in arithmetic does not close: %s vs %s"
        % (rev_all - inner, rev_null))

# ------------------------------------------- 6. run the pandas lab for real
section("6. The pandas cleaning pipeline, run end to end")
try:
    import pandas as pd

    items = pd.read_csv(os.path.join(DATA, "order_items_raw.csv"))
    prod = pd.read_csv(os.path.join(DATA, "products.csv"))
    orders = pd.read_csv(os.path.join(DATA, "orders_raw.csv"))

    start_rows = len(items)
    if start_rows != K["raw_order_items_rows"]:
        bad("raw items file has %d rows, key says %d"
            % (start_rows, K["raw_order_items_rows"]))

    items = items.drop_duplicates()
    if start_rows - len(items) != K["seeded_defects"]["duplicate_rows"]:
        bad("dropped %d duplicates, expected %d"
            % (start_rows - len(items),
               K["seeded_defects"]["duplicate_rows"]))
    else:
        ok("drop_duplicates removed exactly the %d seeded duplicate rows"
           % K["seeded_defects"]["duplicate_rows"])

    sales = items[items["quantity"] > 0].copy()
    rets = items[items["quantity"] < 0].copy()
    if len(rets) == K["seeded_defects"]["negative_quantity_lines"]:
        ok("%d negative-quantity lines split out as returns" % len(rets))
    else:
        bad("found %d negative lines, expected %d"
            % (len(rets), K["seeded_defects"]["negative_quantity_lines"]))

    # fix the currency, the way the lab tells them to
    sales = sales.merge(prod[["product_id", "category"]], on="product_id",
                        how="left", validate="many_to_one")
    usd = sales["category"] == "Imported appliances"
    if int(usd.sum()) != K["seeded_defects"]["lines_priced_in_usd"]:
        bad("%d USD lines, expected %d"
            % (int(usd.sum()), K["seeded_defects"]["lines_priced_in_usd"]))
    else:
        ok("%d lines in the imported category are the USD-priced ones"
           % int(usd.sum()))
    sales.loc[usd, "unit_price"] = sales.loc[usd, "unit_price"] * 3780.0

    # fix the discounts typed as percentages
    over = sales["discount"] > 1
    sales.loc[over, "discount"] = sales.loc[over, "discount"] / 100.0
    if int(over.sum()) == K["seeded_defects"]["discounts_over_one"]:
        ok("%d discounts above 1.0 rescaled" % int(over.sum()))
    else:
        bad("%d discounts over 1.0, expected %d"
            % (int(over.sum()), K["seeded_defects"]["discounts_over_one"]))

    # the two date formats must both parse, and inside the known window
    parsed = pd.to_datetime(orders["order_date"], format="mixed",
                            dayfirst=True)
    if parsed.isna().sum():
        bad("%d order dates failed to parse" % int(parsed.isna().sum()))
    elif str(parsed.min().date()) >= "2024-01-01" and \
            str(parsed.max().date()) <= "2025-12-31":
        ok("both date formats parse, and every date lands inside "
           "2024-01-01 to 2025-12-31")
    else:
        bad("dates parsed outside the generated window: %s to %s"
            % (parsed.min(), parsed.max()))

    # and now the number the lab tells them to hit
    st = orders.set_index("order_id")["status"]
    sales["status"] = sales["order_id"].map(st)
    rev = ((sales["quantity"] * sales["unit_price"]
            * (1 - sales["discount"]))[sales["status"] == "Delivered"]).sum()
    # The expected landing point is NOT the database total: the raw CSVs
    # record the dollar-priced lines to the cent, so a correct clean lands a
    # known residual below it. Asserting the database total here would be a
    # check that can never pass; asserting the raw-derived total is a check
    # that fails if either the generator or the pipeline changes.
    want = K["s3"]["revenue_delivered_from_raw_ugx"]
    db_total = K["s3"]["revenue_delivered_ugx"]
    if abs(rev - want) < 1.0:
        ok("the cleaned CSVs land exactly where they should: UGX %s, which "
           "is UGX %s below the database total from cent-rounding on %s "
           "dollar-priced lines"
           % (format(rev, ",.0f"),
              format(K["s3"]["usd_rounding_residual_ugx"], ",.2f"),
              format(K["s3"]["usd_lines_delivered"], ",")))
    else:
        bad("cleaned revenue UGX %s, expected UGX %s (db total UGX %s)"
            % (format(rev, ",.0f"), format(want, ",.0f"),
               format(db_total, ",.0f")))
    if not 0 < K["s3"]["usd_rounding_residual_ugx"] < 0.0001 * db_total:
        bad("the rounding residual is %s, which is either zero or too large "
            "to be rounding" % K["s3"]["usd_rounding_residual_ugx"])
    else:
        ok("the residual is %.1e of revenue: small enough to be rounding, "
           "large enough to be worth naming"
           % (K["s3"]["usd_rounding_residual_ugx"] / db_total))
except ImportError:
    print("  skip  pandas not installed, so section 6 did not run. "
          "THIS IS NOT A PASS.")

# ------------------------------------------------------------ 7. house style
section("7. House style")
prose = []
for s in C.SESSIONS:
    prose += [s["title"], s["b1"], s["b2"], s["lab"], s["home"], s["trap"]]
prose += [x for _, _, _, x in C.ASSESSMENT]
prose += [C.AUDIENCE] + [d["use"] for d in C.DATASETS]
for f in os.listdir(LABS):
    prose.append(open(os.path.join(LABS, f), encoding="utf-8").read())

# The standing instruction: no "X, not Y" antithesis. One deliberate use is
# allowed where the contrast IS the substance; more than that is the tell.
pat = re.compile(r"\b(is|are|was|were|comes|come)\s+not\s+\w+[^.]{0,40}?,"
                 r"\s+(?:it|they)\s+(?:is|are)\b", re.I)
hits = [p[:90] for p in prose if pat.search(str(p))]
if len(hits) <= 1:
    ok("no 'X, not Y' antithesis pile-up (%d instance%s)"
       % (len(hits), "" if len(hits) == 1 else "s"))
else:
    bad("antithesis construction in %d places: %r" % (len(hits), hits[:3]))

# em-dash editorial asides, the other tell
dash = [p[:90] for p in prose if re.search(r"—\s*(and|which|this is)\s",
                                           str(p))]
if len(dash) <= 2:
    ok("no run of em-dash editorial asides (%d)" % len(dash))
else:
    bad("em-dash asides in %d places: %r" % (len(dash), dash[:3]))

# every lab must state its dataset and its licence position
for f in sorted(os.listdir(LABS)):
    txt = open(os.path.join(LABS, f), encoding="utf-8").read()
    if "data/" not in txt:
        bad("%s never names a data file" % f)
if not any("never names" in f for f in FAIL):
    ok("every lab names the data it runs on")

# the Power BI lab must carry the Mac path, which was an explicit requirement
pbi = open(os.path.join(LABS, "lab_powerbi.md"), encoding="utf-8").read()
if "app.powerbi.com" in pbi and "Mac" in pbi and "cannot do three things" in pbi:
    ok("the Power BI lab gives the browser path and names what it cannot do")
else:
    bad("the Power BI lab does not handle Mac participants")

con.close()
os.remove(_tmp)
print("\n%d checks, %d failures" % (CHECKS, len(FAIL)))
if FAIL:
    print("\nFAILURES:")
    for f in FAIL:
        print("  - " + f)
    sys.exit(1)
print("all checks passed")
