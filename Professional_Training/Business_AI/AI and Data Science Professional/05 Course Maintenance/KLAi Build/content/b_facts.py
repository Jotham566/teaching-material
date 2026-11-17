"""Shared real-data facts for Sessions 1, 3 and 4 (author b). Everything is computed with pandas and numpy from the course data files.
Not a session file: the lint and the deck builder only load content/sNN.py."""
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

BUILD = Path(__file__).resolve().parents[1]
DATA = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'data'
TABS = ['orders', 'order_lines', 'products', 'branches', 'customers', 'branch_weeks']


def n(x):
    """Integer with thousands separators: 2,000."""
    return f'{int(round(x)):,}'


def pct(x, d=1):
    return f'{x * 100:.{d}f}'


def s(x):
    return '' if pd.isna(x) else str(x)


@lru_cache(maxsize=None)
def base():
    xl = pd.ExcelFile(DATA / 'lakeside_for_sheets.xlsx')
    T = {t: xl.parse(t) for t in TABS}
    o, l, p, b, c, w = (T[t] for t in TABS)
    full = pd.read_csv(DATA / 'orders.csv')
    v = o.order_value_ugx
    q1, q3 = float(v.quantile(0.25)), float(v.quantile(0.75))
    B = dict(T=T, full=full, tabs=xl.sheet_names)
    B['n_orders'] = len(o)
    B['sum'] = int(v.sum())
    B['mean'] = float(v.mean())
    B['median'] = float(v.median())
    B['mode'] = int(v.mode().iloc[0])
    B['mode_count'] = int((v == B['mode']).sum())
    B['min'], B['max'] = int(v.min()), int(v.max())
    B['sd'] = float(v.std())                 # sample standard deviation, Sheets =STDEV
    B['sd_pop'] = float(v.std(ddof=0))       # Sheets =STDEV.P
    B['var'] = B['sd'] ** 2
    B['q1'], B['q3'] = q1, q3
    B['iqr'] = q3 - q1
    B['fence_hi'] = q3 + 1.5 * (q3 - q1)
    B['n_out'] = int((v > B['fence_hi']).sum())
    B['n_out_pct'] = B['n_out'] / len(o)
    B['whisker_hi'] = float(v[v <= B['fence_hi']].max())
    B['whisker_lo'] = float(v.min())
    B['skew'] = float(v.skew())
    B['full_n'] = len(full)
    B['full_mean'] = float(full.order_value_ugx.mean())
    B['full_median'] = float(full.order_value_ugx.median())
    B['full_skew'] = float(full.order_value_ugx.skew())
    B['full_ratio'] = B['full_mean'] / B['full_median']
    B['ratio'] = B['mean'] / B['median']
    v2 = v.drop(v.idxmax())
    B['mean_wo_max'] = float(v2.mean())
    B['mean_shift'] = B['mean'] - B['mean_wo_max']
    B['median_wo_max'] = float(v2.median())
    B['sd_wo_max'] = float(v2.std())
    B['n_le_10k'] = int((v <= 10000).sum())
    B['n_le_50k'] = int((v <= 50000).sum())
    B['n_gt_100k'] = int((v > 100000).sum())
    B['share_gt_100k'] = B['n_gt_100k'] / len(o)
    B['full_share_gt_100k'] = float((full.order_value_ugx > 100000).mean())
    B['max_order_id'] = str(o.loc[v.idxmax(), 'order_id'])
    B['max_order_branch'] = str(o.loc[v.idxmax(), 'branch_id'])
    # payment method
    pm = o.payment_method.value_counts()
    B['pay'] = {k: int(x) for k, x in pm.items()}
    B['pay_mode'] = str(pm.index[0])
    B['mm_share'] = float(pm['Mobile money'] / len(o))
    # branches
    g = o.groupby('branch_id').order_value_ugx.agg(['count', 'sum', 'mean', 'median'])
    B['by_branch'] = g
    B['branch_names'] = b.set_index('branch_id').branch_name.to_dict()
    # months
    o2 = o.assign(month=o.order_date.str[:7])
    m = o2.groupby('month').order_value_ugx.agg(['count', 'sum'])
    B['months'] = m
    # walk-in against loyalty
    wi = o.customer_id.isna()
    B['loyal_n'], B['walk_n'] = int((~wi).sum()), int(wi.sum())
    B['loyal_mean'], B['walk_mean'] = float(v[~wi].mean()), float(v[wi].mean())
    B['loyal_median'], B['walk_median'] = float(v[~wi].median()), float(v[wi].median())
    fv = full.order_value_ugx
    fwi = full.customer_id.isna()
    B['full_loyal_mean'], B['full_walk_mean'] = float(fv[~fwi].mean()), float(fv[fwi].mean())
    B['customers_total'] = len(c)
    B['customers_with_order'] = int(o.customer_id.nunique())
    # order lines
    B['n_lines'] = len(l)
    return B


def hist(values, lo, hi, step):
    """Bin counts for values clipped into [lo, hi): returns edges, counts, and how many values lie at or above hi."""
    edges = list(np.arange(lo, hi + step / 2, step))
    cnt, _ = np.histogram(np.asarray(values, dtype=float), bins=edges)
    return [float(e) for e in edges], [int(c) for c in cnt], int((np.asarray(values) >= hi).sum())


@lru_cache(maxsize=None)
def sim():
    """The Monte Carlo simulation of Session 4, from the 2,000 workbook orders (the population). Seeded, so every build gives the same numbers."""
    B = base()
    v = B['T']['orders'].order_value_ugx.to_numpy(float)
    mu, sig = float(v.mean()), float(v.std(ddof=0))
    rng = np.random.default_rng(2026)
    S = dict(mu=mu, sigma=sig)
    idx = rng.integers(0, len(v), (200, 30))     # 200 samples of 30 orders, with replacement, exactly the lab recipe
    m30 = v[idx].mean(axis=1)
    m5 = v[idx[:, :5]].mean(axis=1)             # the first 5 orders of the same samples
    S['m30'], S['m5'] = m30, m5
    above = int(np.argmax(m30 > mu))
    S['first_samples'] = [(i + 1, float(m30[i]), float(m30[i] - mu)) for i in (0, 1, above)]
    m200 = v[rng.integers(0, len(v), (200, 200))].mean(axis=1)   # 200 samples of 200 orders (drawn after the others, so they do not change)
    S['m200'] = m200
    S['sd200'] = float(m200.std(ddof=1))
    S['sd30'], S['sd5'] = float(m30.std(ddof=1)), float(m5.std(ddof=1))
    S['mean30'], S['min30'], S['max30'] = float(m30.mean()), float(m30.min()), float(m30.max())
    S['below_full'] = int((m30 < B['full_mean']).sum())
    S['below_mu'] = int((m30 < mu).sum())
    S['picked'] = sorted(int(k) for k in rng.choice(24 * 7, 30, replace=False))
    # theory
    S['se5'], S['se30'] = sig / np.sqrt(5), sig / np.sqrt(30)
    S['se100'], S['se200'] = sig / np.sqrt(100), sig / np.sqrt(200)
    # many draws, to describe the true sampling distributions
    big = np.random.default_rng(7)
    S['big'] = {}
    for k in (5, 30, 200):
        mm = v[big.integers(0, len(v), (20000, k))].mean(axis=1)
        S['big'][k] = dict(mean=float(mm.mean()), sd=float(mm.std(ddof=1)), skew=float(pd.Series(mm).skew()), below=float((mm < mu).mean()), means=mm)
    # ranges a learner may see, from 5,000 repeats of the whole lab (middle 98 percent)
    lab = np.random.default_rng(99)
    rows = []
    for _ in range(5000):
        ix = lab.integers(0, len(v), (200, 30))
        a = v[ix].mean(axis=1)
        b5 = v[ix[:, :5]].mean(axis=1)
        rows.append((a.mean(), a.std(ddof=1), a.min(), a.max(), (a < B['full_mean']).sum(), b5.std(ddof=1), (a < mu).sum()))
    R = np.array(rows)
    S['rng'] = {k: (float(np.percentile(R[:, i], 1)), float(np.percentile(R[:, i], 99))) for i, k in enumerate(['avg', 'sd', 'min', 'max', 'below_full', 'sd5', 'below_mu'])}
    S['rng_ratio'] = (float(np.percentile(R[:, 5] / R[:, 1], 1)), float(np.percentile(R[:, 5] / R[:, 1], 99)))
    # running share of orders above 100,000
    big_flag = (v > 100000).astype(float)[np.random.default_rng(11).permutation(len(v))]   # orders counted in a random order
    run = np.cumsum(big_flag) / np.arange(1, len(v) + 1)
    S['running'] = [(int(k), float(run[k - 1])) for k in list(range(20, 201, 5)) + list(range(210, 2001, 10))]
    return S
