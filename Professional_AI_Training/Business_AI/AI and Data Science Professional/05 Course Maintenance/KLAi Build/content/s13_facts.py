"""Numbers for Session 13 (regression), computed from branch_weeks.csv with numpy only. statsmodels is not installed here, so every coefficient is solved by
numpy least squares (np.linalg.lstsq) and checked against the normal equations. The notebook compares the statsmodels and scikit-learn results with these values."""
import math
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

BUILD = Path(__file__).resolve().parents[1]
DATA = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'data'


def t_crit(df, level=0.95):
    """Two-sided critical value of Student's t, by integrating the density (scipy is not installed here)."""
    c = math.exp(math.lgamma((df + 1) / 2) - math.lgamma(df / 2)) / math.sqrt(df * math.pi)
    xs = np.linspace(0, 12, 120001)
    pdf = c * (1 + xs ** 2 / df) ** (-(df + 1) / 2)
    cdf = np.concatenate([[0], np.cumsum((pdf[1:] + pdf[:-1]) / 2 * np.diff(xs))])
    return float(np.interp(level / 2, cdf, xs))


def ols(X, y):
    """Coefficients, residuals, and the standard errors of a least squares fit. X already holds the column of ones."""
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    b2 = np.linalg.solve(X.T @ X, X.T @ y)          # the normal equations give the same answer
    assert np.allclose(b, b2, rtol=1e-6, atol=1e-8)
    e = y - X @ b
    n, k = X.shape
    sse = float((e ** 2).sum())
    sst = float(((y - y.mean()) ** 2).sum())
    s2 = sse / (n - k)
    se = np.sqrt(s2 * np.diag(np.linalg.inv(X.T @ X)))
    r2 = 1 - sse / sst
    return dict(b=b, e=e, fit=X @ b, se=se, sse=sse, sst=sst, r2=r2, adj=1 - (1 - r2) * (n - 1) / (n - k), s=math.sqrt(s2), rmse=math.sqrt(sse / n), n=n, k=k)


@lru_cache(maxsize=None)
def facts():
    bw = pd.read_csv(DATA / 'branch_weeks.csv')
    F = dict(bw=bw)
    n = len(bw)
    y = bw.orders.values.astype(float)
    ff, pr, rn = bw.footfall.values.astype(float), bw.promo_on.values.astype(float), bw.rainfall_mm.values.astype(float)
    one = np.ones(n)
    F.update(n=n, branches=int(bw.branch_id.nunique()), weeks=int(bw.week_start.nunique()), first=str(bw.week_start.min()), last=str(bw.week_start.max()),
             promo_n=int(pr.sum()), promo_pct=float(pr.mean() * 100), ff_min=int(ff.min()), ff_max=int(ff.max()), ff_mean=float(ff.mean()), orders_mean=float(y.mean()), orders_min=int(y.min()), orders_max=int(y.max()),
             rain_mean=float(rn.mean()), rain_max=float(rn.max()))
    F['r'] = float(np.corrcoef(ff, y)[0, 1])
    m1 = ols(np.column_stack([one, ff]), y)
    F['m1'] = m1
    # a rival line through the mean point with a smaller slope, to show the sum of squared residuals is larger
    alt_slope = 0.015
    alt_int = float(y.mean() - alt_slope * ff.mean())
    alt_e = y - (alt_int + alt_slope * ff)
    F.update(alt_slope=alt_slope, alt_int=alt_int, alt_sse=float((alt_e ** 2).sum()))
    X3 = np.column_stack([one, ff, pr, rn])
    m3 = ols(X3, y)
    F['X3'], F['m3'] = X3, m3
    tc = t_crit(m3['n'] - m3['k'])
    F['tcrit'] = tc
    F['ci'] = [(float(b - tc * s), float(b + tc * s)) for b, s in zip(m3['b'], m3['se'])]
    F['y'] = y
    # one worked record for the residual formula
    i0 = 0
    F['rec0'] = dict(branch=str(bw.branch_id[0]), week=str(bw.week_start[0]), ff=int(ff[0]), orders=int(y[0]), fit=float(m1['fit'][0]), res=float(m1['e'][0]))
    # branch indicator model: B01 is the reference level
    levels = sorted(bw.branch_id.unique())
    D = np.column_stack([(bw.branch_id.values == l).astype(float) for l in levels])
    F['levels'] = levels
    F['D'] = D
    mb = ols(np.column_stack([X3, D[:, 1:]]), y)
    F['mb'] = mb
    full = np.column_stack([one, D])
    F['trap_cols'] = int(full.shape[1])
    F['trap_rank'] = int(np.linalg.matrix_rank(full))
    # residual spread by thirds of the fitted values
    q = pd.qcut(m3['fit'], 3, labels=False)
    F['res_sd_thirds'] = [float(pd.Series(m3['e'])[q == k].std()) for k in range(3)]
    F['fit_thirds'] = [(float(m3['fit'][q == k].min()), float(m3['fit'][q == k].max())) for k in range(3)]
    # other models
    rain_only = ols(np.column_stack([one, rn]), y)
    F['rain_only_b'] = float(rain_only['b'][1])
    promo_only = ols(np.column_stack([one, pr]), y)
    F['promo_only_b'] = float(promo_only['b'][1])
    F['corr_ff_rain'] = float(np.corrcoef(ff, rn)[0, 1])
    F['promo_ff_mean'] = (float(ff[pr == 0].mean()), float(ff[pr == 1].mean()))
    # sales as the target
    sales = bw.sales_ugx.values.astype(float)
    ms = ols(X3, sales)
    F['sales_r2'] = ms['r2']
    F['sales_max'], F['sales_median'] = int(sales.max()), float(np.median(sales))
    # a time-based split: first 78 weeks to fit, last 26 weeks to test
    wk = sorted(bw.week_start.unique())
    cut = wk[78]
    tr = (bw.week_start < cut).values
    mt = ols(X3[tr], y[tr])
    pt = X3[~tr] @ mt['b']
    et = y[~tr] - pt
    base = np.full((~tr).sum(), y[tr].mean())
    F.update(cut=str(cut), n_tr=int(tr.sum()), n_te=int((~tr).sum()), te_rmse=float(np.sqrt((et ** 2).mean())), te_base_rmse=float(np.sqrt(((y[~tr] - base) ** 2).mean())),
             te_r2=float(1 - (et ** 2).sum() / ((y[~tr] - y[~tr].mean()) ** 2).sum()), tr_rmse=mt['rmse'], te_b=mt['b'], te_last=str(wk[-1]), tr_last=str(wk[77]))
    F['tr_mean'] = float(y[tr].mean())
    F['te_mae'] = float(np.abs(et).mean())
    # a worked prediction
    wk_row = np.array([1, 2000, 1, 20.0])
    F['pred'] = float(wk_row @ m3['b'])
    F['pred_noprom'] = float(np.array([1, 2000, 0, 20.0]) @ m3['b'])
    # points for the pictures (deterministic samples)
    rng = np.random.RandomState(13)
    F['idx25'] = np.sort(np.concatenate([[0], rng.choice(np.arange(1, n), 24, replace=False)]))
    # rows for the indicator pictures: one real record from each of four branches
    pick = [bw[bw.branch_id == b].iloc[2] for b in ('B01', 'B03', 'B02', 'B06', 'B01')]
    F['pick'] = pick
    return F


if __name__ == '__main__':
    F = facts()
    for k, v in F.items():
        if k not in ('bw', 'X3', 'D', 'y', 'm1', 'm3', 'mb', 'pick'):
            print(k, v)
    for nm in ('m1', 'm3', 'mb'):
        m = F[nm]
        print(nm, np.round(m['b'], 5), 'r2', round(m['r2'], 4), 'adj', round(m['adj'], 4), 'rmse', round(m['rmse'], 3), 's', round(m['s'], 3), 'sse', round(m['sse'], 1), 'sst', round(m['sst'], 1))
    print('se', np.round(F['m3']['se'], 5))
