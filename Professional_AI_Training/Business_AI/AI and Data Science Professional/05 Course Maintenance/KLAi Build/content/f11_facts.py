"""Facts for Session 11 (Exploring and visualising with Python), computed with pandas and numpy from the real Lakeside Mart CSV files.
Used by content/s11.py and content/labs/s11_nb.py. Nothing here is typed from memory. `run_snippet` runs the code that is shown on a slide and returns its real output.
"""
import contextlib
import io
import os
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

BUILD = Path(__file__).resolve().parents[1]
DATA = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'data'
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def n(x):
    return f'{int(round(x)):,}'


def run_snippet(code, ns=None):
    """Execute slide code in the data folder with the Agg backend and return (namespace, printed output, value of a final bare expression as text)."""
    import ast
    import matplotlib
    matplotlib.use('Agg')
    ns = ns if ns is not None else {'__name__': '__main__'}
    old = os.getcwd()
    os.chdir(DATA)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            tree = ast.parse(code)
            if tree.body and isinstance(tree.body[-1], ast.Expr):
                last = ast.Expression(tree.body[-1].value)
                exec(compile(ast.Module(tree.body[:-1], type_ignores=[]), '<s>', 'exec'), ns)
                val = eval(compile(last, '<s>', 'eval'), ns)
                if val is not None:
                    print(val.to_string() if hasattr(val, 'to_string') else repr(val))
            else:
                exec(compile(tree, '<s>', 'exec'), ns)
    finally:
        os.chdir(old)
    return ns, buf.getvalue().rstrip('\n')


@lru_cache(maxsize=None)
def facts():
    o = pd.read_csv(DATA / 'orders.csv', parse_dates=['order_date'])
    ln = pd.read_csv(DATA / 'order_lines.csv')
    rt = pd.read_csv(DATA / 'returns.csv')
    br = pd.read_csv(DATA / 'branches.csv')
    F = dict(rows=len(o), cols=o.shape[1], lines_rows=len(ln), returns_rows=len(rt), orders_start=str(o.order_date.min().date()), orders_end=str(o.order_date.max().date()))
    F['missing_cust'] = int(o.customer_id.isna().sum())
    v = o.order_value_ugx
    F['desc'] = {k: float(x) for k, x in v.describe().round(0).items()}
    F['mean'], F['median'], F['std'] = float(v.mean()), float(v.median()), float(v.std())
    F['q1'], F['q3'] = float(v.quantile(.25)), float(v.quantile(.75))
    F['skew'] = float(v.skew())
    F['mean_over_median'] = F['mean'] / F['median']
    F['above200k'] = int((v > 200000).sum())
    F['above200k_pct'] = F['above200k'] / len(o) * 100
    fence = F['q3'] + 1.5 * (F['q3'] - F['q1'])
    F['fence'] = float(fence)
    F['outliers_iqr'] = int((v > fence).sum())
    F['outliers_iqr_pct'] = F['outliers_iqr'] / len(o) * 100
    # basket size
    bs = ln.groupby('order_id').size().rename('basket_size')
    ob = o.merge(bs, on='order_id')
    F['basket_median'], F['basket_mean'], F['basket_max'] = float(ob.basket_size.median()), float(ob.basket_size.mean()), int(ob.basket_size.max())
    F['basket_one_pct'] = float((ob.basket_size == 1).mean() * 100)
    F['corr'] = float(ob.basket_size.corr(ob.order_value_ugx))
    smp = ob.sample(2000, random_state=1)
    F['sample_above300k'] = int((smp.order_value_ugx > 300000).sum())
    F['ob_shape'] = ob.shape
    # payment method
    F['pay_median'] = {k: float(x) for k, x in ob.groupby('payment_method').order_value_ugx.median().items()}
    F['pay_n'] = {k: int(x) for k, x in ob.groupby('payment_method').size().items()}
    F['pay_q1'] = {k: float(x) for k, x in ob.groupby('payment_method').order_value_ugx.quantile(.25).items()}
    F['pay_q3'] = {k: float(x) for k, x in ob.groupby('payment_method').order_value_ugx.quantile(.75).items()}
    # branch means with a normal 95 percent interval
    g = ob.groupby('branch_id').order_value_ugx
    mean_b, sd_b, n_b = g.mean(), g.std(), g.size()
    se_b = sd_b / np.sqrt(n_b)
    F['branch_mean'] = {k: float(x) for k, x in mean_b.items()}
    F['branch_lo'] = {k: float(mean_b[k] - 1.96 * se_b[k]) for k in mean_b.index}
    F['branch_hi'] = {k: float(mean_b[k] + 1.96 * se_b[k]) for k in mean_b.index}
    F['branch_max'], F['branch_min'] = str(mean_b.idxmax()), str(mean_b.idxmin())
    F['branch_overlap'] = bool(F['branch_lo'][F['branch_max']] < F['branch_hi'][F['branch_min']])
    names = br.set_index('branch_id').branch_name
    F['names'] = {k: str(x) for k, x in names.items()}
    # returns: count and rate
    lb = ln.merge(o[['order_id', 'branch_id']], on='order_id')
    rb = rt.merge(o[['order_id', 'branch_id']], on='order_id')
    d = pd.DataFrame({'returns': rb.groupby('branch_id').size(), 'lines': lb.groupby('branch_id').size()})
    d['per_100'] = d.returns / d.lines * 100
    d['rank_count'] = d.returns.rank(ascending=False, method='min').astype(int)
    d['rank_rate'] = d.per_100.rank(ascending=False, method='min').astype(int)
    F['rb'] = d
    F['rate_all'] = len(rt) / len(ln) * 100
    F['top_count'], F['top_rate'] = str(d.returns.idxmax()), str(d.per_100.idxmax())
    F['low_rate'] = str(d.per_100.idxmin())
    # seasonality
    m = o.assign(year=o.order_date.dt.year, month=o.order_date.dt.month).groupby(['year', 'month']).agg(revenue=('order_value_ugx', 'sum'), orders=('order_id', 'size')).reset_index()
    m['rev_m'] = m.revenue / 1e6
    F['monthly'] = m
    nd = m[m.month != 12]
    F['rev_other_mean'] = float(nd.rev_m.mean())
    F['dec_rev'] = {int(y): float(m[(m.year == y) & (m.month == 12)].rev_m.iloc[0]) for y in (2024, 2025)}
    F['dec_ratio'] = {y: F['dec_rev'][y] / F['rev_other_mean'] for y in (2024, 2025)}
    F['orders_other_mean'] = float(nd.orders.mean())
    F['dec_orders'] = {int(y): int(m[(m.year == y) & (m.month == 12)].orders.iloc[0]) for y in (2024, 2025)}
    F['dec_orders_ratio'] = {y: F['dec_orders'][y] / F['orders_other_mean'] for y in (2024, 2025)}
    F['aov_other'] = float(nd.revenue.sum() / nd.orders.sum())
    F['aov_dec'] = {int(y): float(m[(m.year == y) & (m.month == 12)].revenue.iloc[0] / m[(m.year == y) & (m.month == 12)].orders.iloc[0]) for y in (2024, 2025)}
    mm = m.assign(ym=m.year * 100 + m.month)
    F['peak'] = int(mm.loc[mm.rev_m.idxmax(), 'ym'])
    F['peak_month'] = int(mm.loc[mm.rev_m.idxmax(), 'month'])
    F['cust_missing_pct'] = F['missing_cust'] / len(o) * 100
    F['ob'] = ob
    return F
