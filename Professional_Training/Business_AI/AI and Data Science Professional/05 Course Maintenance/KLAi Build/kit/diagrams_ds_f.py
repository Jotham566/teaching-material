"""Figure kinds for Sessions 11 and 12 (Exploring and visualising with Python; Inference), author letter f.
Registered as x_<kind> and used as visual=dict(kind='<kind>', ...).

  f_anatomy   the matplotlib Figure and Axes drawn on a real chart, with numbered parts and the code that makes each part
  f_panels    one to four chart panels in a grid. Each panel has a type:
                 sns   a real seaborn chart drawn from the Lakeside CSV files (recipe name: see RECIPES)
                 hist  a histogram from precomputed bin edges and counts, with vertical lines and shaded tails
                 bar   bars with optional error bars, highlight colours and value labels
                 line  one or more lines
                 interval  horizontal confidence intervals with a reference line
                 scatter   points with an optional fitted guide
  f_alarm     a 10 by 10 grid of tests; the false alarms are red
All text is 14 pt or larger. The sns recipes read the data files themselves, so the picture is exactly what the same seaborn call draws.
"""
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, PALE, fig
import slidekit as K

BUILD = Path(__file__).resolve().parents[1]
DATA = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'data'
LIGHT = '#D9D9D9'


@lru_cache(maxsize=None)
def _orders():
    o = pd.read_csv(DATA / 'orders.csv', parse_dates=['order_date'])
    ln = pd.read_csv(DATA / 'order_lines.csv')
    return o.merge(ln.groupby('order_id').size().rename('basket_size'), on='order_id')


@lru_cache(maxsize=None)
def _returns_by_branch():
    o = _orders()
    ln = pd.read_csv(DATA / 'order_lines.csv').merge(o[['order_id', 'branch_id']], on='order_id')
    rt = pd.read_csv(DATA / 'returns.csv').merge(o[['order_id', 'branch_id']], on='order_id')
    d = pd.DataFrame({'returns': rt.groupby('branch_id').size(), 'lines': ln.groupby('branch_id').size()})
    d['per_100'] = d.returns / d.lines * 100
    return d


def _kfmt(x, pos=None):
    if x >= 1e6:
        return f'{x / 1e6:g}M'
    return f'{x / 1000:g}k' if x else '0'


def _label(ax, p):
    if p.get('title'):
        ax.set_title(p['title'], fontsize=16, fontweight='bold', loc='left', pad=8)
    ax.set_xlabel(p.get('xlabel', ''), fontsize=15)
    ax.set_ylabel(p.get('ylabel', ''), fontsize=15)
    ax.tick_params(labelsize=14)
    if p.get('xk'):
        ax.xaxis.set_major_formatter(FuncFormatter(_kfmt))
    if p.get('yk'):
        ax.yaxis.set_major_formatter(FuncFormatter(_kfmt))
    if p.get('xlim'):
        ax.set_xlim(*p['xlim'])
    if p.get('ylim'):
        ax.set_ylim(*p['ylim'])


def _legend(ax, p, loc='upper right'):
    h, lab = ax.get_legend_handles_labels()
    if h:
        ax.legend(fontsize=14, loc=p.get('legend', loc), frameon=False, handlelength=1.6, borderaxespad=0.2)


# ------------------------------------------------------------------ seaborn recipes on the real files
def _r_hist_value(ax, p):
    import seaborn as sns
    o = _orders()
    sns.histplot(data=o, x='order_value_ugx', binwidth=10000, binrange=(0, 200000), color=GREY, edgecolor=PAPER, ax=ax)
    ax.axvline(o.order_value_ugx.median(), color=GOLD, lw=3, label=f'median {o.order_value_ugx.median():,.0f}')
    ax.axvline(o.order_value_ugx.mean(), color=RED, lw=3, ls='--', label=f'mean {o.order_value_ugx.mean():,.0f}')
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:,.0f}'))


def _r_hist_basket(ax, p):
    import seaborn as sns
    sns.histplot(data=_orders(), x='basket_size', discrete=True, shrink=0.85, color=GREY, edgecolor=PAPER, ax=ax)
    ax.set_xlim(0, 15)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:,.0f}'))


def _r_box_pay(ax, p):
    import seaborn as sns
    sns.boxplot(data=_orders(), x='payment_method', y='order_value_ugx', showfliers=False, color=PALE, linecolor=INK, linewidth=2, width=0.55, ax=ax)
    ax.yaxis.set_major_formatter(FuncFormatter(_kfmt))


def _r_scatter_hue(ax, p):
    import seaborn as sns
    smp = _orders().sample(2000, random_state=1)
    sns.scatterplot(data=smp, x='basket_size', y='order_value_ugx', hue='payment_method', palette=[INK, RED, GOLD], alpha=0.65, s=34, edgecolor='none', ax=ax)
    ax.set_ylim(0, 300000)
    ax.set_xticks([0, 5, 10, 15, 20])
    ax.yaxis.set_major_formatter(FuncFormatter(_kfmt))
    ax.legend(fontsize=14, loc='upper left', frameon=False, title=None, handletextpad=0.2, borderaxespad=0.1)


def _r_bar_branch(ax, p):
    import seaborn as sns
    sns.barplot(data=_orders().sort_values('branch_id'), x='branch_id', y='order_value_ugx', color=GREY, edgecolor=INK, errorbar=('ci', 95), seed=1, err_kws={'color': INK, 'linewidth': 2.2}, capsize=0.25, ax=ax)
    ax.set_ylim(0, 60000)
    ax.yaxis.set_major_formatter(FuncFormatter(_kfmt))


def _r_count_branch(ax, p):
    d = _returns_by_branch()
    cols = [RED if v == d.returns.max() else GREY for v in d.returns]
    ax.bar(d.index, d.returns, color=cols, edgecolor=INK, lw=1.0)
    for i, v in enumerate(d.returns):
        ax.text(i, v + 6, str(v), ha='center', va='bottom', fontsize=14)
    ax.set_ylim(0, d.returns.max() * 1.15)


def _r_rate_branch(ax, p):
    d = _returns_by_branch()
    cols = [RED if v == d.per_100.max() else GREY for v in d.per_100]
    ax.bar(d.index, d.per_100, color=cols, edgecolor=INK, lw=1.0)
    for i, v in enumerate(d.per_100):
        ax.text(i, v + 0.04, f'{v:.2f}', ha='center', va='bottom', fontsize=14)
    ax.set_ylim(0, d.per_100.max() * 1.15)


def _monthly():
    o = _orders()
    m = o.assign(year=o.order_date.dt.year.astype(str), month=o.order_date.dt.month).groupby(['year', 'month']).agg(revenue_m=('order_value_ugx', lambda s: s.sum() / 1e6), orders=('order_id', 'size')).reset_index()
    return m


def _r_line_season(ax, p):
    import seaborn as sns
    sns.lineplot(data=_monthly(), x='month', y='revenue_m', hue='year', palette=[INK, RED], marker='o', markersize=8, ax=ax)
    ax.set_xticks(range(1, 13))
    ax.set_ylim(0, 100)
    ax.legend(fontsize=14, loc='upper left', frameon=False, title=None)


def _r_line_orders(ax, p):
    import seaborn as sns
    sns.lineplot(data=_monthly(), x='month', y='orders', hue='year', palette=[INK, RED], marker='o', markersize=8, ax=ax)
    ax.set_xticks(range(1, 13))
    ax.set_ylim(0, 2000)
    ax.legend(fontsize=14, loc='upper left', frameon=False, title=None)


def _r_line_monthly_dated(ax, p):
    o = _orders()
    mo = o.groupby(o.order_date.dt.to_period('M')).order_value_ugx.sum() / 1e6
    ax.plot(mo.index.astype(str), mo.values, marker='o', color=INK)
    ax.set_xticks(range(0, len(mo), 3))
    ax.set_xticklabels([str(x) for x in mo.index[::3]], rotation=0, fontsize=12)
    ax.set_ylim(0, 100)


RECIPES = {'hist_value': _r_hist_value, 'hist_basket': _r_hist_basket, 'box_pay': _r_box_pay, 'scatter_hue': _r_scatter_hue, 'bar_branch': _r_bar_branch,
           'count_branch': _r_count_branch, 'rate_branch': _r_rate_branch, 'line_season': _r_line_season, 'line_orders': _r_line_orders, 'line_monthly': _r_line_monthly_dated}


# ------------------------------------------------------------------ generic panels (precomputed numbers)
def _p_hist(ax, p):
    e, c = np.asarray(p['edges'], float), np.asarray(p['counts'], float)
    ctr = (e[:-1] + e[1:]) / 2
    cols = [p.get('color', GREY)] * len(c)
    if p.get('counts2') is not None:
        c2 = np.asarray(p['counts2'], float)
        ax.bar(e[:-1], c, width=np.diff(e), align='edge', color=INK, alpha=0.5, edgecolor=PAPER, lw=0.5, label=p.get('label1'))
        ax.bar(e[:-1], c2, width=np.diff(e), align='edge', color=GOLD, alpha=0.65, edgecolor=PAPER, lw=0.5, label=p.get('label2'))
        c = np.zeros_like(c)
    if p.get('red_abs') is not None:
        cols = [RED if abs(x) >= p['red_abs'] else p.get('color', GREY) for x in ctr]
    ax.bar(e[:-1], c, width=np.diff(e), align='edge', color=cols, edgecolor=PAPER, lw=0.5)
    for x, lab, col, ls in p.get('vlines', []):
        ax.axvline(x, color=col, lw=3, ls=ls, label=lab)
    if p.get('ymax'):
        ax.set_ylim(0, p['ymax'])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:,.0f}'))
    _label(ax, p)
    _legend(ax, p)


def _p_bar(ax, p):
    labs, vals = p['labels'], np.asarray(p['values'], float)
    n = len(labs)
    cols = [p.get('hl_color', RED) if i in p.get('hl', []) else p.get('color', GREY) for i in range(n)]
    if p.get('horizontal'):
        ax.barh(range(n), vals, color=cols, edgecolor=INK, lw=1.0)
        ax.set_yticks(range(n))
        ax.set_yticklabels(labs, fontsize=14)
        ax.invert_yaxis()
        for i, v in enumerate(vals):
            ax.text(v + p.get('pad', 0), i, p['fmt'].format(v), va='center', ha='left', fontsize=14)
    else:
        ax.bar(range(n), vals, color=cols, edgecolor=INK, lw=1.0, width=p.get('width', 0.7))
        ax.set_xticks(range(n))
        ax.set_xticklabels(labs, fontsize=14)
        if p.get('fmt'):
            for i, v in enumerate(vals):
                ax.text(i, v + p.get('pad', 0), p['fmt'].format(v), ha='center', va='bottom', fontsize=14)
    if p.get('err'):
        lo, hi = np.asarray(p['err'][0], float), np.asarray(p['err'][1], float)
        ax.errorbar(range(n), vals, yerr=[vals - lo, hi - vals], fmt='none', ecolor=INK, elinewidth=2.4, capsize=6, capthick=2.4)
    for y, lab, col, ls in p.get('hlines', []):
        ax.axhline(y, color=col, lw=2.6, ls=ls, label=lab)
    _label(ax, p)
    _legend(ax, p)


def _p_line(ax, p):
    for sdef in p['series']:
        ax.plot(sdef['x'], sdef['y'], color=sdef.get('color', INK), marker=sdef.get('marker', 'o'), markersize=sdef.get('ms', 8), lw=2.6, label=sdef.get('label'))
    for x, y, txt, dx, dy in p.get('notes', []):
        ax.annotate(txt, (x, y), xytext=(x + dx, y + dy), fontsize=14, color=INK, arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.6))
    if p.get('xticks'):
        ax.set_xticks(p['xticks'])
    for y, lab, col, ls in p.get('hlines', []):
        ax.axhline(y, color=col, lw=2.2, ls=ls, label=lab)
    _label(ax, p)
    _legend(ax, p)


def _p_interval(ax, p):
    labs = p['labels']
    est, lo, hi = (np.asarray(p[k], float) for k in ('est', 'low', 'high'))
    n = len(labs)
    cols = [RED if m else INK for m in p.get('miss', [False] * n)]
    for i in range(n):
        ax.hlines(i, lo[i], hi[i], color=cols[i], lw=p.get('lw', 3.2))
        ax.plot(est[i], i, 'o', color=cols[i], ms=p.get('ms', 8))
        if p.get('annot'):
            ax.text(hi[i] + p.get('pad', 0), i, p['annot'][i], va='center', ha='left', fontsize=14, color=cols[i])
    if p.get('ref') is not None:
        ax.axvline(p['ref'][0], color=p['ref'][2] if len(p['ref']) > 2 else GOLD, lw=3, ls='--', label=p['ref'][1])
    ax.set_yticks(range(n))
    ax.set_yticklabels(labs if p.get('show_labels', True) else [''] * n, fontsize=14)
    ax.set_ylim(n - 0.5, -0.5)
    _label(ax, p)
    _legend(ax, p, 'lower right')


def _p_scatter(ax, p):
    ax.scatter(p['x'], p['y'], s=p.get('s', 30), color=p.get('color', INK), alpha=p.get('alpha', 0.6), edgecolor='none')
    _label(ax, p)


def _p_sns(ax, p):
    RECIPES[p['recipe']](ax, p)
    _label(ax, p)


PANELS = {'sns': _p_sns, 'hist': _p_hist, 'bar': _p_bar, 'line': _p_line, 'interval': _p_interval, 'scatter': _p_scatter}


@fig('x_f_panels')
def f_panels(w, h, panels=(), ncols=None, wspace=0.3, hspace=0.55, left=0.1, right=0.98, bottom=0.17, top=0.88, **_):
    s = Scene(w, h)
    n = len(panels)
    ncols = ncols or n
    nrows = -(-n // ncols)
    gs = s.f.add_gridspec(nrows, ncols, left=left, right=right, bottom=bottom, top=top, wspace=wspace, hspace=hspace)
    for i, p in enumerate(panels):
        ax = s.f.add_subplot(gs[i // ncols, i % ncols])
        ax.set_facecolor(PAPER)
        PANELS[p['type']](ax, p)
    return s


# ------------------------------------------------------------------ the matplotlib Figure and Axes, labelled
@fig('x_f_anatomy')
def f_anatomy(w, h, months=(), values=(), parts=(), **_):
    s = Scene(w, h)
    from matplotlib.patches import FancyBboxPatch
    bg = s.f.add_axes([0, 0, 1, 1])
    bg.axis('off')
    bg.set_xlim(0, w)
    bg.set_ylim(0, h)
    bg.add_patch(FancyBboxPatch((0.05, 0.05), 6.75, h - 0.1, boxstyle='round,pad=0,rounding_size=0.1', fc=PALE, ec=INK, lw=2.4))
    bg.set_zorder(0)
    s.ax.set_zorder(5)
    # real chart inside the page
    ax = s.f.add_axes([1.35 / w, 0.95 / h, 5.0 / w, 2.35 / h])
    ax.set_facecolor(PAPER)
    ax.set_zorder(1)
    ax.plot(range(len(values)), values, marker='o', color=INK, lw=2.6, ms=7)
    ax.set_xticks(range(0, len(months), 3))
    ax.set_xticklabels([months[i] for i in range(0, len(months), 3)], fontsize=14)
    ax.set_title('Monthly revenue, 2024', fontsize=16, fontweight='bold', pad=8)
    ax.set_ylabel('UGX millions', fontsize=15)
    ax.set_xlabel('Month', fontsize=15)
    ax.tick_params(labelsize=14)
    ax.set_ylim(0, 100)
    # numbered markers
    marks = [(0.35, h - 0.35), (1.8, 3.05), (2.4, 3.6), (0.45, 3.05), (4.6, 0.53), (0.95, 0.78), (5.55, 3.05)]
    for k, (x, y) in enumerate(marks[:len(parts)]):
        s.circle(x, y, 0.17, fill=GOLD, edge=INK, lw=1.6, z=8)
        s.text(x, y, str(k + 1), size=14, weight='bold', z=9)
    # legend of the parts
    x0, rowh = 7.1, (h - 0.1) / max(1, len(parts))
    for k, (term, code) in enumerate(parts):
        yc = h - 0.05 - (k + 0.5) * rowh
        s.circle(x0 + 0.17, yc, 0.17, fill=GOLD, edge=INK, lw=1.6, z=8)
        s.text(x0 + 0.17, yc, str(k + 1), size=14, weight='bold', z=9)
        s.text(x0 + 0.5, yc + 0.13, term, size=15, weight='bold', ha='left')
        s.text(x0 + 0.5, yc - 0.15, code, size=14, mono=True, ha='left', color=BODY)
    return s


# ------------------------------------------------------------------ a grid of tests with false alarms in red
@fig('x_f_alarm')
def f_alarm(w, h, alarms=(), label_a='', label_b='', n=100, **_):
    s = Scene(w, h)
    side = min(h - 0.9, w - 0.2) / 10
    x0 = (w - side * 10) / 2
    ytop = h - 0.15
    al = set(alarms)
    for i in range(n):
        r, c = divmod(i, 10)
        s.box(x0 + c * side + 0.03, ytop - (r + 1) * side + 0.03, side - 0.06, side - 0.06, '', fill=RED if i in al else PAPER, edge=INK, lw=1.2, r=0.02)
    s.text(w / 2, 0.3, label_a, size=16, weight='bold')
    return s
