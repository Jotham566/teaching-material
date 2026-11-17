"""Facts for Session 12 (Inference: is the difference real?). Every number is computed with numpy and pandas only, because SciPy and statsmodels are not installed in the authoring sandbox.
The t-distribution p-value is computed by numerical integration of the t density (math.lgamma and numpy); the normal p-value with math.erfc.
The notebook compares the SciPy and statsmodels results with these numbers. Slides show only these numbers.
"""
import math
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

BUILD = Path(__file__).resolve().parents[1]
DATA = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'data'
SEED = 42


def n(x):
    return f'{int(round(x)):,}'


def t_pvalue(t, df):
    """Two-sided p-value of Student's t distribution by numerical integration of the density (trapezoid rule, 600,001 points)."""
    c = math.exp(math.lgamma((df + 1) / 2) - math.lgamma(df / 2)) / math.sqrt(df * math.pi)
    x = np.linspace(abs(t), abs(t) + 120, 600001)
    y = c * (1 + x ** 2 / df) ** (-(df + 1) / 2)
    return float(2 * np.trapezoid(y, x))


def z_pvalue(z):
    return math.erfc(abs(z) / math.sqrt(2))


def welch(a, b):
    """Welch t statistic, standard error, degrees of freedom and two-sided p-value for the difference of two means a - b."""
    va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    se = math.sqrt(va + vb)
    t = (a.mean() - b.mean()) / se
    df = (va + vb) ** 2 / (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1))
    return t, se, df, t_pvalue(t, df)


def hist(values, lo, hi, bins):
    c, e = np.histogram(values, bins=bins, range=(lo, hi))
    return [float(x) for x in e], [int(x) for x in c]


@lru_cache(maxsize=None)
def facts():
    t = pd.read_csv(DATA / 'offer_test.csv')
    o = t[t.group == 'offer'].next_month_spend_ugx.values.astype(float)
    c = t[t.group == 'control'].next_month_spend_ugx.values.astype(float)
    allv = t.next_month_spend_ugx.values.astype(float)
    F = dict(test=t, offer=o, control=c, all=allv)
    F['n_o'], F['n_c'], F['n'] = len(o), len(c), len(t)
    F['mean_o'], F['mean_c'], F['mean_all'] = float(o.mean()), float(c.mean()), float(allv.mean())
    F['sd_o'], F['sd_c'], F['sd_all'] = float(o.std(ddof=1)), float(c.std(ddof=1)), float(allv.std(ddof=1))
    F['lift'] = F['mean_o'] - F['mean_c']
    F['lift_pct'] = F['lift'] / F['mean_c'] * 100
    F['med_o'], F['med_c'] = float(np.median(o)), float(np.median(c))
    # standard error of each mean and of the lift, and the formula confidence interval
    F['se_o'], F['se_c'] = F['sd_o'] / math.sqrt(len(o)), F['sd_c'] / math.sqrt(len(c))
    F['se_lift'] = math.sqrt(F['se_o'] ** 2 + F['se_c'] ** 2)
    F['ci_lift'] = (F['lift'] - 1.96 * F['se_lift'], F['lift'] + 1.96 * F['se_lift'])
    F['ci_o'] = (F['mean_o'] - 1.96 * F['se_o'], F['mean_o'] + 1.96 * F['se_o'])
    F['ci_c'] = (F['mean_c'] - 1.96 * F['se_c'], F['mean_c'] + 1.96 * F['se_c'])
    # Welch t test
    F['t'], F['se_welch'], F['df'], F['p_t'] = welch(o, c)
    F['p_normal'] = z_pvalue(F['t'])
    # effect size: Cohen's d with the pooled standard deviation
    sp = math.sqrt(((len(o) - 1) * o.var(ddof=1) + (len(c) - 1) * c.var(ddof=1)) / (len(o) + len(c) - 2))
    F['sp'], F['d'] = float(sp), F['lift'] / sp
    # sampling variability: treat all 2,500 customers as the population; draw with replacement
    rng = np.random.default_rng(SEED)
    F['pop_mean'], F['pop_sd'] = F['mean_all'], float(allv.std(ddof=0))
    F['sampling'] = {}
    for m in (25, 100, 400, 1600):
        means = rng.choice(allv, size=(1000, m)).mean(axis=1)
        F['sampling'][m] = dict(means=means, sim_se=float(means.std(ddof=0)), formula_se=F['pop_sd'] / math.sqrt(m))
    F['means100'] = F['sampling'][100]['means']
    # what 95 percent means: 1,000 samples of 100, each with its own interval; the first 30 are drawn
    rng = np.random.default_rng(SEED + 1)
    iv = []
    for _ in range(1000):
        s = rng.choice(allv, 100)
        se = s.std(ddof=1) / 10
        iv.append((float(s.mean()), float(s.mean() - 1.96 * se), float(s.mean() + 1.96 * se)))
    miss = [not (lo <= F['pop_mean'] <= hi) for _, lo, hi in iv]
    F['cover'], F['cover_miss'] = iv[:30], miss[:30]
    F['cover_hits'] = 30 - sum(miss[:30])
    F['cover_rate'] = (1000 - sum(miss)) / 1000 * 100
    # bootstrap of the lift
    rng = np.random.default_rng(SEED)
    boot = np.array([rng.choice(o, len(o)).mean() - rng.choice(c, len(c)).mean() for _ in range(5000)])
    F['boot'] = boot
    F['boot_se'] = float(boot.std(ddof=1))
    F['boot_ci'] = tuple(float(x) for x in np.percentile(boot, [2.5, 97.5]))
    # permutation test of the difference in means
    rng = np.random.default_rng(SEED)
    is_off = (t.group == 'offer').values
    perm = np.empty(5000)
    for i in range(5000):
        s = rng.permutation(is_off)
        perm[i] = allv[s].mean() - allv[~s].mean()
    F['perm'] = perm
    F['perm_hits'] = int((np.abs(perm) >= abs(F['lift'])).sum())
    F['p_perm'] = F['perm_hits'] / 5000
    F['perm_sd'] = float(perm.std(ddof=1))
    # two proportions
    bo = t[t.group == 'offer'].returned_within_30d.values
    bc = t[t.group == 'control'].returned_within_30d.values
    F['x_o'], F['x_c'] = int(bo.sum()), int(bc.sum())
    F['p1'], F['p2'] = F['x_o'] / len(bo), F['x_c'] / len(bc)
    F['p_pool'] = (F['x_o'] + F['x_c']) / (len(bo) + len(bc))
    F['gap'] = F['p1'] - F['p2']
    F['se_pool'] = math.sqrt(F['p_pool'] * (1 - F['p_pool']) * (1 / len(bo) + 1 / len(bc)))
    F['z'] = F['gap'] / F['se_pool']
    F['p_z'] = z_pvalue(F['z'])
    se_u = math.sqrt(F['p1'] * (1 - F['p1']) / len(bo) + F['p2'] * (1 - F['p2']) / len(bc))
    F['se_unpooled'] = se_u
    F['ci_gap'] = (F['gap'] - 1.96 * se_u, F['gap'] + 1.96 * se_u)
    # A/A tests: split the control group at random into two halves; the true difference is zero
    rng = np.random.default_rng(SEED)
    alarms, ps = [], []
    for i in range(100):
        idx = rng.permutation(len(c))
        a, b = c[idx[:627]], c[idx[627:]]
        _, _, _, p = welch(a, b)
        ps.append(p)
        if p < 0.05:
            alarms.append(i)
    F['aa_alarms'], F['aa_ps'] = alarms, ps
    # multiple comparisons
    F['family'] = {m: 1 - 0.95 ** m for m in (1, 5, 10, 20, 40)}
    # optional stopping: A/A experiments, 10 looks, the z test at each look
    rng = np.random.default_rng(SEED)
    runs, per_arm, looks = 2000, 1000, 10
    x = rng.choice(c, size=(runs, 2, per_arm))
    step = per_arm // looks
    z_at = []
    for k in range(1, looks + 1):
        m = k * step
        a, b = x[:, 0, :m], x[:, 1, :m]
        se = np.sqrt(a.var(axis=1, ddof=1) / m + b.var(axis=1, ddof=1) / m)
        z_at.append((a.mean(axis=1) - b.mean(axis=1)) / se)
    z_at = np.array(z_at)
    F['peek_final'] = float((np.abs(z_at[-1]) > 1.96).mean() * 100)
    F['peek_any'] = float((np.abs(z_at) > 1.96).any(axis=0).mean() * 100)
    F['peek_runs'], F['peek_looks'] = runs, looks
    # histogram data for figures
    F['h_means100'] = hist(F['means100'], 52000, 76000, 24)
    F['h_boot'] = hist(boot, -1000, 11000, 24)
    F['h_perm'] = hist(perm, -6000, 6000, 24)
    F['h_spend_o'] = hist(o, 0, 250000, 25)
    F['h_spend_c'] = hist(c, 0, 250000, 25)
    return F


def run_snippet(code, ns=None):
    """Execute slide code with the data folder as the working directory; returns (namespace, printed output and the value of a final bare expression)."""
    import ast
    import contextlib
    import io
    import os
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
                    print(repr(val))
            else:
                exec(compile(tree, '<s>', 'exec'), ns)
    finally:
        os.chdir(old)
    return ns, buf.getvalue().rstrip('\n')
