"""DA figures, part C: sessions 13 to 15 (NumPy, distributions, relationships)."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from figs_da_util import (Scene, fig, Chart, chart, sales, daily, money, fmt_axis_money, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, BRANCH)
import figkit


def _axes(w, h, n=1, ncols=None, **kw):
    figkit.use_style()
    ncols = ncols or n
    nrows = int(np.ceil(n / ncols))
    f, axs = plt.subplots(nrows, ncols, figsize=(w, h), **kw)
    return f, np.atleast_1d(axs).ravel()


# ------------------------------------------------------------------ session 13
@fig('da_hero_numpy')
def da_hero_numpy(w, h, **_):
    s = Scene(w, h)
    c = daily()['customers_counted'].to_numpy()
    s.text(0.3, h - 0.4, f'customers = daily["customers_counted"].to_numpy()', size=17, mono=True, ha='left')
    x = 0.3
    first = c[:9]
    for i, v in enumerate(first):
        s.box(x + i * 0.95, h - 1.65, 0.9, 0.75, str(v), size=22, fill=PAPER, lw=1.8, r=0.03)
    s.text(x + 9 * 0.95 + 0.45, h - 1.28, '… 180 numbers', size=22, weight='bold', ha='left')
    s.arrow(w / 2, h - 1.85, w / 2, h - 2.55, color=RED, lw=2.4)
    res = [('mean', f'{np.mean(c):.1f}'), ('median', f'{np.median(c):g}'), ('spread (max − min)', f'{int(c.max() - c.min())}'), ('25% and 75% marks', f'{np.percentile(c, 25):g}  {np.percentile(c, 75):g}')]
    bw = (w - 0.6 - 3 * 0.25) / 4
    for i, (lab, val) in enumerate(res):
        bx = 0.3 + i * (bw + 0.25)
        s.box(bx, 0.35, bw, 1.65, '', fill=PAPER, lw=1.8, r=0.05)
        s.text(bx + bw / 2, 1.5, val, size=28 if i < 3 else 24, weight='bold')
        s.text(bx + bw / 2, 0.85, lab, size=17, color=BODY)
    s.text(w - 0.3, h - 2.2, 'one array, many answers', size=18, color=MUTE, ha='right')
    return s


@fig('da_array_strip')
def da_array_strip(w, h, **_):
    s = Scene(w, h)
    c = daily()['customers_counted'].to_numpy()[:7]
    bw = 0.95
    x0 = 0.45
    s.text(0.3, h - 0.45, 'customers', size=20, mono=True, weight='bold', ha='left')
    for i, v in enumerate(c):
        s.box(x0 + i * 1.0, h - 1.5, bw, 0.8, str(v), size=22, lw=1.8, r=0.03)
    for i in range(len(c)):
        s.arrow(x0 + i * 1.0 + bw / 2, h - 1.55, x0 + i * 1.0 + bw / 2, h - 2.35, color=RED, lw=2, head=13)
    s.text(0.05, h - 2.0, '+50', size=20, weight='bold', color=RED, ha='left')
    s.text(0.3, h - 2.95, 'busier = customers + 50', size=20, mono=True, weight='bold', ha='left')
    for i, v in enumerate(c):
        s.box(x0 + i * 1.0, h - 3.95, bw, 0.8, str(v + 50), size=22, fill=GOLD, lw=1.8, r=0.03)
    s.text(w / 2, 0.35, 'One instruction changes every number in the array at once.', size=19, color=BODY)
    return s


@fig('da_two_routes')
def da_two_routes(w, h, **_):
    s = Scene(w, h)
    d = daily()
    c = d['customers_counted'].to_numpy()
    rows = [('mean', 'daily["customers_counted"].mean()', 'np.mean(customers)', f'{np.mean(c):.1f}'),
            ('median', 'daily["customers_counted"].median()', 'np.median(customers)', f'{np.median(c):g}')]
    for i, (lab, a, b, v) in enumerate(rows):
        yb = h - 0.35 - i * 2.2
        s.text(0.45, yb, 'pandas', size=16, color=MUTE, ha='left')
        s.box(0.45, yb - 0.75, 4.9, 0.6, a, size=14, fill=INK, edge=INK, color=PAPER, mono=True, r=0.05)
        s.text(0.45, yb - 0.98, 'NumPy', size=16, color=MUTE, ha='left')
        s.box(0.45, yb - 1.73, 4.9, 0.6, b, size=14, fill=INK, edge=INK, color=PAPER, mono=True, r=0.05)
        s.arrow(5.45, yb - 0.45, 6.2, yb - 0.85, color=RED, lw=2)
        s.arrow(5.45, yb - 1.43, 6.2, yb - 1.05, color=RED, lw=2)
        s.box(6.25, yb - 1.25, 1.35, 0.6, v, size=22, fill=GOLD, weight='bold', r=0.05)
    s.text(w / 2, 0.25, 'Two routes, one answer: a check that one mistake cannot fool.', size=16.5, color=BODY)
    return s


@fig('da_percentiles_line')
def da_percentiles_line(w, h, **_):
    f, axs = _axes(w, h)
    ax = axs[0]
    c = np.sort(daily()['customers_counted'].to_numpy())
    rng = np.random.RandomState(3)
    ax.scatter(c, rng.uniform(0, 1, len(c)), s=26, color=INK, alpha=0.8, zorder=3)
    q1, med, q3 = np.percentile(c, [25, 50, 75])
    for q, lab, col in [(q1, f'25% mark\n{q1:g}', GREY), (med, f'middle\n{med:g}', RED), (q3, f'75% mark\n{q3:g}', GREY)]:
        ax.axvline(q, color=col if col != GREY else INK, lw=2.8, ls='-' if col == RED else '--', zorder=2)
        ax.text(q, 1.12, lab, ha='center', va='bottom', fontsize=16, fontweight='bold', color=col if col == RED else INK, bbox=dict(fc=PAPER, ec='none', pad=2), zorder=6)
    n = len(c)
    ax.text((c.min() + q1) / 2, -0.28, f'{n // 4} days', ha='center', fontsize=15, color=MUTE)
    ax.text((q1 + med) / 2, -0.28, f'{n // 4} days', ha='center', fontsize=15, color=MUTE)
    ax.text((med + q3) / 2, -0.28, f'{n // 4} days', ha='center', fontsize=15, color=MUTE)
    ax.text((q3 + c.max()) / 2, -0.28, f'{n // 4 + n % 4} days', ha='center', fontsize=15, color=MUTE)
    ax.set_ylim(-0.4, 1.75)
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.set_xlabel('Customers counted in a day (each dot is one shop-day, 180 in all)')
    return Chart(f)


@fig('da_outlier_fence')
def da_outlier_fence(w, h, **_):
    f, axs = _axes(w, h)
    ax = axs[0]
    v = sales()['line_value'].to_numpy()
    q1, q3 = np.percentile(v, [25, 75])
    fence = q3 + 1.5 * (q3 - q1)
    ax.hist(v[v <= fence], bins=np.arange(0, 30001, 750), color=GREY, edgecolor=PAPER)
    ax.set_ylim(0, 400)
    ax.hist(v[(v > fence) & (v <= 30000)], bins=np.arange(0, 30001, 750), color=GOLD, edgecolor=INK, linewidth=0.6)
    ax.axvline(fence, color=RED, lw=3)
    top = ax.get_ylim()[1]
    ax.text(fence + 400, top * 0.9, f'fence {fence:,.0f}', color=RED, fontsize=18, fontweight='bold', va='top')
    big = int((v > fence).sum())
    ax.text(fence + 400, top * 0.72, f'{big} sales above\nthe fence', fontsize=17, fontweight='bold', va='top')
    ax.text(29800, top * 0.38, f'largest sale:\n{int(v.max()):,}', ha='right', fontsize=16, color=MUTE)
    ax.text(1500, top * 0.93, 'ordinary sales', fontsize=17, fontweight='bold', ha='left')
    ax.set_xlim(0, 30000)
    ax.set_xlabel(f'Value of one sale (UGX). Fence = Q3 + 1.5 × (Q3 − Q1) = {q3:,.0f} + 1.5 × {q3 - q1:,.0f}')
    ax.set_ylabel('Number of sales')
    fmt_axis_money(ax, 'x')
    return Chart(f)


@fig('da_std_dev')
def da_std_dev(w, h, **_):
    f, axs = _axes(w, h)
    ax = axs[0]
    c = daily()['customers_counted'].to_numpy()
    m, sd = c.mean(), c.std()
    rng = np.random.RandomState(5)
    ax.scatter(c, rng.uniform(0, 1, len(c)), s=24, color=INK, alpha=0.75, zorder=3)
    ax.axvline(m, color=RED, lw=3)
    ax.axvspan(m - sd, m + sd, color='#EDEDED', zorder=1)
    ax.text(m, 1.12, f'mean {m:.1f}', ha='center', fontsize=17, fontweight='bold', color=RED, bbox=dict(fc=PAPER, ec='none', pad=2), zorder=6)
    ax.annotate('', xy=(m + sd, -0.2), xytext=(m, -0.2), arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=2.2))
    ax.text(m + sd / 2, -0.38, f'typical distance\n{sd:.1f}', ha='center', va='top', fontsize=16, fontweight='bold')
    ax.set_ylim(-0.75, 1.4)
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.set_xlabel('Customers counted in a day (grey band: one standard deviation each side)')
    return Chart(f)


# ------------------------------------------------------------------ session 14
@fig('da_hero_dist')
def da_hero_dist(w, h, **_):
    f, axs = _axes(w, h, 2, ncols=2, gridspec_kw={'width_ratios': [1.1, 1]})
    su = sales()
    ax = axs[0]
    v = su['line_value']
    ax.hist(v, bins=30, color=GREY, edgecolor=PAPER)
    ax.set_title('One column: how the values spread', loc='left', fontsize=17)
    ax.set_xlabel('Value of one sale (UGX)')
    ax.set_ylabel('Number of sales')
    fmt_axis_money(ax, 'x')
    ax2 = axs[1]
    data = [su[su['branch'] == b]['line_value'] for b in ['Central Market', 'Campus Gate', 'Roadside']]
    bp = ax2.boxplot(data, labels=['Central\nMarket', 'Campus\nGate', 'Roadside'], widths=0.55, patch_artist=True, showfliers=False,
                     medianprops=dict(color=RED, lw=3), boxprops=dict(facecolor=PAPER, lw=1.8), whiskerprops=dict(lw=1.8), capprops=dict(lw=1.8))
    ax2.set_ylim(0, 10000)
    ax2.set_title('Groups side by side', loc='left', fontsize=17)
    ax2.set_ylabel('Value of one sale (UGX)')
    fmt_axis_money(ax2)
    f.tight_layout()
    return Chart(f)


@fig('da_hist_bins')
def da_hist_bins(w, h, bins=30, **_):
    f, axs = _axes(w, h)
    ax = axs[0]
    v = sales()['line_value']
    ax.hist(v, bins=np.linspace(0, v.max(), bins + 1), color=GREY, edgecolor=PAPER)
    ax.set_xlim(0, 20000)
    ax.text(0.98, 0.5, f'the tail runs on to\n{int(v.max()):,} (not shown)', transform=ax.transAxes, ha='right', fontsize=15, color=MUTE)
    ax.set_title(f'bins={bins}: ' + ('wide bars, a rough shape' if bins < 40 else 'narrow bars, more detail'), loc='left', fontsize=17)
    ax.set_xlabel('Value of one sale (UGX)')
    ax.set_ylabel('Number of sales')
    fmt_axis_money(ax, 'x')
    return Chart(f)


@fig('da_skew_pair')
def da_skew_pair(w, h, kind='balanced', **_):
    f, axs = _axes(w, h)
    ax = axs[0]
    if kind == 'balanced':
        d = daily()
        v = d[d['branch'] == 'Central Market']['customers_counted']
        ax.hist(v, bins=14, color=GREY, edgecolor=PAPER)
        ax.set_title('Central Market customers per day', loc='left', fontsize=16)
        ax.set_xlabel('Customers counted')
        ax.text(0.97, 0.9, f'skew {v.skew():.1f}', transform=ax.transAxes, ha='right', fontsize=18, fontweight='bold')
    else:
        v = sales()['line_value']
        ax.hist(v, bins=30, color=GREY, edgecolor=PAPER)
        ax.set_title('Value of one sale', loc='left', fontsize=16, color=RED)
        ax.set_xlabel('UGX')
        fmt_axis_money(ax, 'x')
        ax.text(0.97, 0.9, f'skew {v.skew():.1f}', transform=ax.transAxes, ha='right', fontsize=18, fontweight='bold', color=RED)
    ax.set_ylabel('Number of days' if kind == 'balanced' else 'Number of sales')
    return Chart(f)


@fig('da_boxplot_anatomy')
def da_boxplot_anatomy(w, h, **_):
    figkit.use_style()
    f = plt.figure(figsize=(w, h))
    ax = f.add_axes([0.1, 0.12, 0.3, 0.8])
    d = daily()
    v = d[d['branch'] == 'Campus Gate']['customers_counted']
    ax.boxplot([v], widths=0.5, patch_artist=True, medianprops=dict(color=RED, lw=3.2), boxprops=dict(facecolor=GOLD, lw=2), whiskerprops=dict(lw=2),
               capprops=dict(lw=2), flierprops=dict(marker='o', markersize=7, markerfacecolor=INK))
    ax.set_xticks([])
    ax.set_ylabel('Customers per day, Campus Gate', fontsize=15)
    q1, med, q3 = np.percentile(v, [25, 50, 75])
    iqr = q3 - q1
    hi = v[v <= q3 + 1.5 * iqr].max()
    lo = v[v >= q1 - 1.5 * iqr].min()
    kw = dict(fontsize=16, color=INK, fontweight='bold', va='center', ha='left', textcoords='figure fraction', annotation_clip=False,
              arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.8, shrinkA=3, shrinkB=2))
    ax.annotate(f'whisker: the highest\nordinary day, {hi:g}', xy=(1.0, hi), xycoords='data', xytext=(0.5, 0.86), **kw)
    ax.annotate(f'top of the box: the 75% mark, {q3:g}', xy=(1.25, q3), xycoords='data', xytext=(0.5, 0.68), **kw)
    kw2 = dict(kw)
    kw2['color'] = RED
    kw2['arrowprops'] = dict(arrowstyle='-|>', color=RED, lw=1.8, shrinkA=3, shrinkB=2)
    ax.annotate(f'line: the median, {med:g}', xy=(1.25, med), xycoords='data', xytext=(0.5, 0.5), **kw2)
    ax.annotate(f'bottom of the box: the 25% mark, {q1:g}', xy=(1.25, q1), xycoords='data', xytext=(0.5, 0.32), **kw)
    ax.annotate(f'whisker: the lowest ordinary day, {lo:g}', xy=(1.0, lo), xycoords='data', xytext=(0.5, 0.14), **kw)
    f.text(0.5, 0.05, 'The box holds the middle half of the days.', fontsize=16, color=BODY)
    return Chart(f)


@fig('da_box_branches')
def da_box_branches(w, h, **_):
    f, axs = _axes(w, h)
    ax = axs[0]
    su = sales()
    names = ['Central Market', 'Campus Gate', 'Roadside']
    data = [su[su['branch'] == b]['line_value'] for b in names]
    ax.boxplot(data, labels=names, widths=0.55, patch_artist=True, medianprops=dict(color=RED, lw=3.2), boxprops=dict(facecolor=PAPER, lw=1.8),
               whiskerprops=dict(lw=1.8), capprops=dict(lw=1.8), flierprops=dict(marker='o', markersize=4, markerfacecolor=GREY, markeredgecolor=GREY))
    ax.set_ylim(0, 22000)
    for i, dd in enumerate(data, start=1):
        ax.text(i + 0.33, dd.median(), f'median\n{int(dd.median()):,}', fontsize=15, fontweight='bold', color=RED, va='center')
    ax.text(0.98, 0.97, f'dots above 22,000 run on to {int(su["line_value"].max()):,}', transform=ax.transAxes, ha='right', va='top', fontsize=14, color=MUTE)
    ax.set_ylabel('Value of one sale (UGX)')
    fmt_axis_money(ax)
    return Chart(f)


@fig('da_median_branches')
def da_median_branches(w, h, **_):
    f, axs = _axes(w, h)
    ax = axs[0]
    d = daily()
    names = ['Roadside', 'Campus Gate', 'Central Market']
    data = [d[d['branch'] == b]['customers_counted'] for b in names]
    ax.boxplot(data, labels=names, vert=False, widths=0.55, patch_artist=True, medianprops=dict(color=RED, lw=3.2), boxprops=dict(facecolor=PAPER, lw=1.8),
               whiskerprops=dict(lw=1.8), capprops=dict(lw=1.8), flierprops=dict(marker='o', markersize=5, markerfacecolor=GREY, markeredgecolor=GREY))
    for i, dd in enumerate(data, start=1):
        ax.text(dd.median(), i + 0.38, f'median {dd.median():g}', fontsize=16, fontweight='bold', color=RED, ha='center')
    ax.set_xlabel('Customers counted in a day')
    ax.set_ylim(0.4, 3.9)
    return Chart(f)


# ------------------------------------------------------------------ session 15
@fig('da_hero_relation')
def da_hero_relation(w, h, **_):
    f, axs = _axes(w, h, 2, ncols=2)
    d = daily()
    ax = axs[0]
    ax.scatter(d['customers_counted'], d['revenue_ugx'], s=22, color=INK, alpha=0.7)
    r1 = d['customers_counted'].corr(d['revenue_ugx'])
    ax.set_title(f'Customers and revenue: r = {r1:.2f}', loc='left', fontsize=17)
    ax.set_xlabel('Customers counted')
    ax.set_ylabel('Revenue (UGX)')
    fmt_axis_money(ax)
    ax = axs[1]
    ax.scatter(d['rain_mm'], d['customers_counted'], s=22, color=INK, alpha=0.7)
    r2 = d['rain_mm'].corr(d['customers_counted'])
    ax.set_title(f'Rain and customers: r = {r2:.2f}', loc='left', fontsize=17, color=RED)
    ax.set_xlabel('Rain (mm)')
    ax.set_ylabel('Customers counted')
    f.tight_layout()
    return Chart(f)


@fig('da_scatter_hue')
def da_scatter_hue(w, h, **_):
    f, axs = _axes(w, h)
    ax = axs[0]
    d = daily()
    for b, col, edge in [('Central Market', INK, INK), ('Campus Gate', GOLD, INK), ('Roadside', PAPER, RED)]:
        dd = d[d['branch'] == b]
        ax.scatter(dd['customers_counted'], dd['revenue_ugx'], s=60, color=col, edgecolor=edge, linewidth=1.5, label=b, zorder=3)
    ax.legend(fontsize=16, loc='upper left')
    ax.set_xlabel('Customers counted in a day')
    ax.set_ylabel('Revenue that day (UGX)')
    fmt_axis_money(ax)
    r = d['customers_counted'].corr(d['revenue_ugx'])
    ax.text(0.97, 0.06, f'r = {r:.3f}', transform=ax.transAxes, ha='right', fontsize=20, fontweight='bold')
    return Chart(f)


@fig('da_corr_examples')
def da_corr_examples(w, h, **_):
    f, axs = _axes(w, h, 4, ncols=4)
    d = daily()
    rng = np.random.RandomState(2)
    x = np.linspace(0, 1, 40)
    panels = [(x, x, 'r = 1', 'a made-up straight line'), (d['customers_counted'], d['revenue_ugx'], f'r = {d["customers_counted"].corr(d["revenue_ugx"]):.2f}', 'customers, revenue'),
              (d['rain_mm'], d['customers_counted'], f'r = {d["rain_mm"].corr(d["customers_counted"]):.2f}', 'rain, customers'), (x, 1 - x, 'r = −1', 'a made-up falling line')]
    for ax, (a, b, t, sub) in zip(axs, panels):
        ax.scatter(a, b, s=14, color=INK, alpha=0.8)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(t, fontsize=20, fontweight='bold', color=RED if 'rain' in sub else INK)
        ax.set_xlabel(sub, fontsize=14)
    f.tight_layout()
    return Chart(f)


@fig('da_heatmap')
def da_heatmap(w, h, **_):
    f, axs = _axes(w, h)
    ax = axs[0]
    d = daily()
    cols = ['customers_counted', 'rain_mm', 'sale_lines', 'revenue_ugx']
    labels = ['customers', 'rain', 'sale lines', 'revenue']
    c = d[cols].corr().values
    cmap = LinearSegmentedColormap.from_list('klai', [RED, PAPER, INK])
    ax.imshow(c, cmap=cmap, vmin=-1, vmax=1)
    ax.set_xticks(range(4))
    ax.set_yticks(range(4))
    ax.set_xticklabels(labels, fontsize=15)
    ax.set_yticklabels(labels, fontsize=15)
    for i in range(4):
        for j in range(4):
            ax.text(j, i, f'{c[i, j]:.2f}', ha='center', va='center', fontsize=19, fontweight='bold', color=PAPER if abs(c[i, j]) > 0.5 else INK)
    for sp in ax.spines.values():
        sp.set_visible(True)
    ax.tick_params(length=0)
    return Chart(f)


@fig('da_rain_corr_bars')
def da_rain_corr_bars(w, h, **_):
    f, axs = _axes(w, h)
    ax = axs[0]
    d = daily()
    names = ['Central Market', 'Campus Gate', 'Roadside']
    vals = [d[d['branch'] == b]['rain_mm'].corr(d[d['branch'] == b]['customers_counted']) for b in names]
    y = np.arange(3)[::-1]
    ax.barh(y, vals, color=[GOLD, GOLD, GOLD], edgecolor=INK, linewidth=1.8, height=0.5)
    ax.axvline(0, color=INK, lw=2)
    ax.set_xlim(-1, 1)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=17)
    for yy, v in zip(y, vals):
        ax.text(v + (0.04 if v >= 0 else -0.04), yy, f'{v:.3f}', va='center', ha='left' if v >= 0 else 'right', fontsize=18, fontweight='bold')
    ax.set_xlabel('Correlation of rain with customers (the full scale is −1 to 1)')
    return Chart(f)


@fig('da_cause_umbrella')
def da_cause_umbrella(w, h, **_):
    s = Scene(w, h)
    s.icon('rain', w / 2, h - 0.8, 1.2)
    s.text(w / 2, h - 1.6, 'rain', size=22, weight='bold')
    s.arrow(w / 2 - 0.5, h - 1.85, 1.9, h - 2.55, color=RED, lw=2.4)
    s.arrow(w / 2 + 0.5, h - 1.85, w - 1.9, h - 2.55, color=RED, lw=2.4)
    s.icon('person', 1.9, h - 3.0, 0.9)
    s.text(1.9, h - 3.85, 'people open\numbrellas', size=19, weight='bold')
    s.box(w - 3.0, h - 3.45, 2.2, 0.8, 'wet roads', size=22, weight='bold', fill=GOLD, r=0.05)
    s.text(w / 2, h - 3.0, 'they move together', size=18, color=RED, weight='bold')
    s.text(w / 2, 0.3, 'Umbrellas do not make roads wet. A third thing, rain, drives both.', size=17, color=BODY)
    return s
