# -*- coding: utf-8 -*-
"""Numbers for the Data Analysis slides, straight out of the answer key.

Every figure that appears on a slide comes through here, so a slide cannot
quote a number the dataset does not produce. Regenerate the data and the
decks change with it.
"""
import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
KEY = os.path.join(_ROOT, "DataAnalysis_Track", "data", "answer_key.json")

with open(KEY, encoding="utf-8") as fh:
    K = json.load(fh)


def n(x):
    return "{:,}".format(x)


def ugx(x):
    return "UGX {:,.0f}".format(x)


def bn(x):
    """Billions, for a headline where the full figure is unreadable."""
    return "UGX {:.2f}bn".format(x / 1e9)


def m(x):
    """Millions, switching to billions above a thousand million.

    "UGX 1204m" appeared on a slide and read as a typo. Anything over a
    thousand million is clearer as billions.
    """
    if abs(x) >= 1e9:
        return bn(x)
    return "UGX {:,.0f}m".format(x / 1e6)


# the handful of figures the slides actually use, named so a typo in a key
# path fails at import rather than printing something odd on a slide
ROWS = K["row_counts"]
ORDERS = ROWS["orders"]
ITEMS = ROWS["order_items"]
CUSTOMERS = ROWS["customers"]
PRODUCTS = ROWS["products"]
REPS = ROWS["reps"]
RETURNS = ROWS["returns"]
RAW_ITEM_ROWS = K["raw_order_items_rows"]

DELIVERED = K["s2"]["orders_delivered"]
CANCELLED = K["s2"]["orders_cancelled"]
COUNT_STAR, COUNT_COL = K["s2"]["count_star_vs_customer_id"]
WALKINS = COUNT_STAR - COUNT_COL

REV_ALL = K["s3"]["revenue_all_ugx"]
REV_DELIVERED = K["s3"]["revenue_delivered_ugx"]
REV_FROM_RAW = K["s3"]["revenue_delivered_from_raw_ugx"]
REV_WALKIN = K["s3"]["revenue_lost_to_inner_join_ugx"]
RESIDUAL = K["s3"]["usd_rounding_residual_ugx"]
USD_LINES_DELIVERED = K["s3"]["usd_lines_delivered"]
RETURNS_VALUE = K["s3"]["returns_value_ugx"]
REV_BY_REGION = K["s3"]["revenue_by_region_ugx"]
TOP_REPS = K["s3"]["top_rep_2025"]

MEAN_ORDER = K["s7"]["order_value_mean_ugx"]
MEDIAN_ORDER = K["s7"]["order_value_median_ugx"]
P10_ORDER = K["s7"]["order_value_p10_ugx"]
P90_ORDER = K["s7"]["order_value_p90_ugx"]
MAX_ORDER = K["s7"]["order_value_max_ugx"]
SKEW = K["s7"]["mean_over_median"]
BY_MONTH = K["s7"]["revenue_by_month_ugx"]
RETURN_RATE = K["s7"]["return_rate_by_region"]
RETURN_COUNT = K["s7"]["returns_count_by_region"]

DEFECTS = K["seeded_defects"]
DUP_ROWS = DEFECTS["duplicate_rows"]
NEG_LINES = DEFECTS["negative_quantity_lines"]
USD_LINES = DEFECTS["lines_priced_in_usd"]
BAD_DISCOUNTS = DEFECTS["discounts_over_one"]
ALT_DATES = DEFECTS["dates_in_dd_mm_yyyy"]
MESSY_NAMES = DEFECTS["customer_names_messy"]
MISSING_CUST = DEFECTS["orders_missing_customer_id"]
DUP_CUST = K["duplicate_customer"]

# derived, and derived HERE rather than typed on a slide
AOV_DELIVERED = REV_DELIVERED / DELIVERED
# What the Power BI measure gives if the denominator is not filtered
# to delivered as well: delivered revenue over ALL orders. 19% low,
# silent, and now taught as the mistake rather than shipped as one.
AOV_UNFILTERED = REV_DELIVERED / ORDERS
CANCELLED_GAP = REV_ALL - REV_DELIVERED
DEC_2025 = dict(BY_MONTH)["2025-12"]
FEB_2024 = dict(BY_MONTH)["2024-02"]
DEC_OVER_FEB = DEC_2025 / FEB_2024
RETURN_RATE_TOP = RETURN_RATE[0]           # highest rate
RETURN_COUNT_TOP = RETURN_COUNT[0]         # most returns

# ---------------------------------------------------------------- slide text
# The placeholders every week module may use. They live here, in one place,
# because sessions moved between modules when the track was replanned from
# twelve sessions to fifteen and each module's private copy went stale. A
# week module now adds only the names peculiar to it.
FMT_BASE = dict(
    orders=n(ORDERS), items=n(ITEMS), customers=n(CUSTOMERS),
    products=n(PRODUCTS), reps=n(REPS), returns=n(RETURNS),
    raw=n(RAW_ITEM_ROWS), delivered=n(DELIVERED), cancelled=n(CANCELLED),
    count_star=n(COUNT_STAR), count_col=n(COUNT_COL), walkins=n(WALKINS),
    joined=n(COUNT_COL),
    rev_all=ugx(REV_ALL), rev_delivered=ugx(REV_DELIVERED),
    rev_from_raw=ugx(REV_FROM_RAW), walkin_rev=ugx(REV_WALKIN),
    cancelled_gap=ugx(CANCELLED_GAP), returns_value=ugx(RETURNS_VALUE),
    residual=ugx(RESIDUAL), usd_delivered=n(USD_LINES_DELIVERED),
    aov=ugx(round(AOV_DELIVERED, -3)),
    aov_wrong=ugx(round(REV_DELIVERED / ORDERS, -3)),
    top_reps=", ".join("{} at {}".format(r, m(v)) for r, v in TOP_REPS),
    dup_rows=n(DUP_ROWS), neg_lines=n(NEG_LINES), usd_lines=n(USD_LINES),
    bad_discounts=n(BAD_DISCOUNTS), alt_dates=n(ALT_DATES),
    messy_names=n(MESSY_NAMES), missing_cust=n(MISSING_CUST),
    skew="{:.1f}".format(SKEW),
    mean_order=ugx(MEAN_ORDER), median_order=ugx(MEDIAN_ORDER),
    mean_order_raw="{:,.0f}".format(MEAN_ORDER),
    median_order_raw="{:,.0f}".format(MEDIAN_ORDER),
    p10_order=ugx(P10_ORDER), p90_order=ugx(P90_ORDER),
    max_order=ugx(MAX_ORDER),
    dec_over_feb="{:.1f}".format(DEC_OVER_FEB),
    count_top_region=RETURN_COUNT_TOP[0], count_top_n=n(RETURN_COUNT_TOP[1]),
    rate_top_region=RETURN_RATE_TOP[0],
    rate_top_pct="{:.2f}%".format(100 * RETURN_RATE_TOP[1]),
    rate_bottom_region=RETURN_RATE[-1][0],
    rate_bottom_pct="{:.2f}%".format(100 * RETURN_RATE[-1][1]),
    rate_top_pct_east="{:.2f}%".format(
        100 * dict(RETURN_RATE)[RETURN_COUNT_TOP[0]]),
    region_top=REV_BY_REGION[0][0], region_top_bn=bn(REV_BY_REGION[0][1]),
    region_low=REV_BY_REGION[-1][0], region_low_bn=bn(REV_BY_REGION[-1][1]),
)
