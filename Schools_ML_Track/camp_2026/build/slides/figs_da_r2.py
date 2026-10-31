"""DA figures, repair pass R2 (sessions 13 to 24).

Imported after figs_da, so every figure registered here replaces the figure of the same name in figs_da_c, _d, _e and _f.
Also holds the small purpose-made word icons (1.3 x 1.3 inches) used by concepts_da_2.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Wedge

from figs_da_util import (SUN, Scene, fig, Chart, chart, sales, products, daily, raw, practice, money, fmt_axis_money, clean_pipeline,
                          INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD)
import figkit

# one colour per shop, the same in every figure
SHOP = {'Central Market': dict(fc=INK, ec=INK), 'Campus Gate': dict(fc=RED, ec=RED), 'Roadside': dict(fc=GOLD, ec=INK)}
SHOPS = ['Central Market', 'Campus Gate', 'Roadside']


def _axes(w, h):
    figkit.use_style()
    f, ax = plt.subplots(figsize=(w, h))
    return f, ax


# ================================================================== session 13
@fig('da_hero_numpy')
def da_hero_numpy(w, h, **_):
    f, ax = _axes(w, h)
    c = daily()['customers_counted'].to_numpy()
    rng = np.random.RandomState(7)
    ax.scatter(c, rng.uniform(0.05, 0.95, len(c)), s=46, color=INK, alpha=0.75, zorder=3)
    m, med = c.mean(), float(np.median(c))
    ax.axvline(m, color=RED, lw=3.4, zorder=2)
    ax.axvline(med, color=INK, lw=3, ls='--', zorder=2)
    ax.text(m + 4, 1.22, f'mean {m:.1f}', ha='left', va='center', fontsize=20, fontweight='bold', color=RED)
    ax.text(med - 4, 1.22, f'median {med:g}', ha='right', va='center', fontsize=20, fontweight='bold', color=INK)
    ax.set_title('daily["customers_counted"].to_numpy()   gives 180 numbers, one dot each', loc='left', fontsize=18, pad=14)
    ax.set_ylim(-0.05, 1.4)
    ax.set_xlim(0, 365)
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.set_xlabel('Customers counted in a day (the lowest day is {}, the highest is {})'.format(int(c.min()), int(c.max())))
    return Chart(f)


@fig('da_two_routes')
def da_two_routes(w, h, **_):
    s = Scene(w, h)
    d = daily()
    c = d['customers_counted'].to_numpy()
    rows = [('mean', 'daily["customers_counted"].mean()', 'np.mean(customers)', f'{np.mean(c):.1f}'),
            ('median', 'daily["customers_counted"].median()', 'np.median(customers)', f'{np.median(c):g}')]
    for i, (lab, a, b, v) in enumerate(rows):
        yb = h - 0.3 - i * 2.2
        s.text(0.3, yb, 'pandas', size=16, color=MUTE, ha='left')
        s.box(0.3, yb - 0.82, 5.3, 0.6, a, size=16, fill=INK, edge=INK, color=PAPER, mono=True, r=0.05)
        s.text(0.3, yb - 1.05, 'NumPy', size=16, color=MUTE, ha='left')
        s.box(0.3, yb - 1.87, 5.3, 0.6, b, size=16, fill=INK, edge=INK, color=PAPER, mono=True, r=0.05)
        s.arrow(5.65, yb - 0.52, 6.3, yb - 0.95, color=RED, lw=2)
        s.arrow(5.65, yb - 1.57, 6.3, yb - 1.15, color=RED, lw=2)
        s.box(6.35, yb - 1.35, 1.25, 0.6, v, size=22, fill=GOLD, weight='bold', r=0.05)
    s.text(w / 2, 0.25, 'Two routes, one answer: a check that one mistake cannot fool.', size=16, color=BODY)
    return s


@fig('da_std_dev')
def da_std_dev(w, h, **_):
    f, ax = _axes(w, h)
    c = daily()['customers_counted'].to_numpy()
    m, sd = c.mean(), c.std()
    rng = np.random.RandomState(5)
    ax.scatter(c, rng.uniform(0, 1, len(c)), s=24, color=INK, alpha=0.75, zorder=3)
    ax.axvline(m, color=RED, lw=3)
    ax.axvspan(m - sd, m + sd, color='#EDEDED', zorder=1)
    ax.text(m, 1.14, f'mean {m:.1f}', ha='center', fontsize=17, fontweight='bold', color=RED, bbox=dict(fc=PAPER, ec='none', pad=2), zorder=6)
    ax.annotate('', xy=(m + sd, -0.3), xytext=(m, -0.3), arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=2.2))
    ax.text(m + sd / 2 + 0.35 * sd, -0.55, f'typical distance {sd:.1f}', ha='center', va='top', fontsize=17, fontweight='bold', bbox=dict(fc=PAPER, ec='none', pad=2), zorder=7)
    ax.set_ylim(-1.0, 1.4)
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.set_xlabel('Customers counted in a day\ngrey band: one standard deviation each side of the mean')
    return Chart(f)


@fig('da_outlier_fence')
def da_outlier_fence(w, h, **_):
    f, ax = _axes(w, h)
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
    ax.text(29800, top * 0.38, f'largest sale:\n{int(v.max()):,}', ha='right', fontsize=17, fontweight='bold', color=INK)
    ax.text(1500, top * 0.93, 'ordinary sales', fontsize=17, fontweight='bold', ha='left')
    ax.set_xlim(0, 30000)
    ax.set_xlabel(f'Value of one sale (UGX). Fence = Q3 + 1.5 × (Q3 − Q1) = {q3:,.0f} + 1.5 × {q3 - q1:,.0f}')
    ax.set_ylabel('Number of sales')
    fmt_axis_money(ax, 'x')
    return Chart(f)


# ================================================================== session 14
@fig('da_hist_bins')
def da_hist_bins(w, h, bins=30, **_):
    f, ax = _axes(w, h)
    v = sales()['line_value']
    ax.hist(v, bins=np.linspace(0, v.max(), bins + 1), color=GREY, edgecolor=PAPER)
    ax.set_xlim(0, 20000)
    ax.set_title(f'bins={bins}: ' + ('wide bars, a rough shape' if bins < 40 else 'narrow bars, more detail'), loc='left', fontsize=17)
    ax.set_xlabel(f'Value of one sale (UGX)\nthe tail runs on to {int(v.max()):,}, off the right edge')
    ax.set_ylabel('Number of sales')
    fmt_axis_money(ax, 'x')
    return Chart(f)


@fig('da_boxplot_anatomy')
def da_boxplot_anatomy(w, h, **_):
    figkit.use_style()
    f = plt.figure(figsize=(w, h))
    ax = f.add_axes([0.1, 0.1, 0.25, 0.84])
    d = daily()
    v = d[d['branch'] == 'Campus Gate']['customers_counted']
    ax.boxplot([v], widths=0.5, patch_artist=True, medianprops=dict(color=RED, lw=3.2), boxprops=dict(facecolor=GOLD, lw=2), whiskerprops=dict(lw=2),
               capprops=dict(lw=2), flierprops=dict(marker='o', markersize=7, markerfacecolor=INK))
    ax.set_xticks([])
    ax.set_ylabel('Customers per day, Campus Gate', fontsize=16)
    q1, med, q3 = np.percentile(v, [25, 50, 75])
    iqr = q3 - q1
    hi = v[v <= q3 + 1.5 * iqr].max()
    lo = v[v >= q1 - 1.5 * iqr].min()
    kw = dict(fontsize=18, color=INK, fontweight='bold', va='center', ha='left', textcoords='figure fraction', annotation_clip=False,
              arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.8, shrinkA=3, shrinkB=2))
    ax.annotate(f'top whisker: {hi:g}', xy=(1.0, hi), xycoords='data', xytext=(0.45, 0.88), **kw)
    ax.annotate(f'75% mark: {q3:g}', xy=(1.25, q3), xycoords='data', xytext=(0.45, 0.70), **kw)
    kw2 = dict(kw)
    kw2['color'] = RED
    kw2['arrowprops'] = dict(arrowstyle='-|>', color=RED, lw=1.8, shrinkA=3, shrinkB=2)
    ax.annotate(f'median: {med:g}', xy=(1.25, med), xycoords='data', xytext=(0.45, 0.52), **kw2)
    ax.annotate(f'25% mark: {q1:g}', xy=(1.25, q1), xycoords='data', xytext=(0.45, 0.34), **kw)
    ax.annotate(f'bottom whisker: {lo:g}', xy=(1.0, lo), xycoords='data', xytext=(0.45, 0.16), **kw)
    return Chart(f)


@fig('da_box_branches')
def da_box_branches(w, h, **_):
    f, ax = _axes(w, h)
    su = sales()
    data = [su[su['branch'] == b]['line_value'] for b in SHOPS]
    ax.boxplot(data, labels=SHOPS, widths=0.5, patch_artist=True, medianprops=dict(color=RED, lw=3.4), boxprops=dict(facecolor=PAPER, lw=2),
               whiskerprops=dict(lw=2), capprops=dict(lw=2), flierprops=dict(marker='o', markersize=5, markerfacecolor=GREY, markeredgecolor=GREY))
    ax.set_ylim(0, 12000)
    for i, dd in enumerate(data, start=1):
        ax.text(i + 0.28, dd.median(), f'median {int(dd.median()):,}', fontsize=16, fontweight='bold', color=RED, va='center')
    ax.set_xlabel(f'A few dots run above 12,000, up to {int(su["line_value"].max()):,}')
    ax.set_ylabel('Value of one sale (UGX)')
    fmt_axis_money(ax)
    return Chart(f)


@fig('da_median_branches')
def da_median_branches(w, h, **_):
    f, ax = _axes(w, h)
    d = daily()
    names = ['Roadside', 'Campus Gate', 'Central Market']
    data = [d[d['branch'] == b]['customers_counted'] for b in names]
    ax.boxplot(data, labels=names, vert=False, widths=0.5, patch_artist=True, medianprops=dict(color=RED, lw=3.2), boxprops=dict(facecolor=PAPER, lw=1.8),
               whiskerprops=dict(lw=1.8), capprops=dict(lw=1.8), flierprops=dict(marker='o', markersize=5, markerfacecolor=GREY, markeredgecolor=GREY))
    for i, dd in enumerate(data, start=1):
        ax.text(dd.median(), i + 0.38, f'median {dd.median():g}', fontsize=17, fontweight='bold', color=RED, ha='center')
    ax.set_xlabel('Customers counted in a day')
    ax.set_ylim(0.4, 3.9)
    return Chart(f)


# ================================================================== session 15
@fig('da_scatter_hue')
def da_scatter_hue(w, h, **_):
    f, ax = _axes(w, h)
    d = daily()
    for b in SHOPS:
        dd = d[d['branch'] == b]
        ax.scatter(dd['customers_counted'], dd['revenue_ugx'], s=60, color=SHOP[b]['fc'], edgecolor=SHOP[b]['ec'], linewidth=1.5, label=b, zorder=3)
    ax.legend(fontsize=16, loc='upper left')
    ax.set_xlabel('Customers counted in a day')
    ax.set_ylabel('Revenue that day (UGX)')
    fmt_axis_money(ax)
    r = d['customers_counted'].corr(d['revenue_ugx'])
    ax.text(0.97, 0.06, f'r = {r:.3f}', transform=ax.transAxes, ha='right', fontsize=20, fontweight='bold')
    return Chart(f)


@fig('da_corr_examples')
def da_corr_examples(w, h, **_):
    figkit.use_style()
    f, axs = plt.subplots(1, 4, figsize=(w, h))
    d = daily()
    x = np.linspace(0, 1, 40)
    panels = [(x, x, 'r = 1', 'made-up rise'), (d['customers_counted'], d['revenue_ugx'], f'r = {d["customers_counted"].corr(d["revenue_ugx"]):.2f}', 'customers, revenue'),
              (d['rain_mm'], d['customers_counted'], f'r = {d["rain_mm"].corr(d["customers_counted"]):.2f}', 'rain, customers'), (x, 1 - x, 'r = −1', 'made-up fall')]
    for ax, (a, b, t, sub) in zip(axs, panels):
        ax.scatter(a, b, s=14, color=INK, alpha=0.8)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(t, fontsize=20, fontweight='bold', color=RED if 'rain' in sub else INK)
        ax.set_xlabel(sub, fontsize=16)
    f.tight_layout()
    return Chart(f)


@fig('da_heatmap')
def da_heatmap(w, h, **_):
    f, ax = _axes(w, h)
    d = daily()
    cols = ['customers_counted', 'rain_mm', 'sale_lines', 'revenue_ugx']
    labels = ['customers', 'rain', 'sale lines', 'revenue']
    c = d[cols].corr().values
    cmap = LinearSegmentedColormap.from_list('klai', [RED, PAPER, INK])
    ax.imshow(c, cmap=cmap, vmin=-1, vmax=1)
    ax.set_xticks(range(4))
    ax.set_yticks(range(4))
    ax.set_xticklabels(labels, fontsize=17)
    ax.set_yticklabels(labels, fontsize=17)
    for i in range(4):
        for j in range(4):
            ax.text(j, i, f'{c[i, j]:.2f}', ha='center', va='center', fontsize=20, fontweight='bold', color=PAPER if c[i, j] > 0.5 else INK)
    for sp in ax.spines.values():
        sp.set_visible(True)
    ax.tick_params(length=0)
    return Chart(f)


@fig('da_rain_corr_bars')
def da_rain_corr_bars(w, h, **_):
    f, ax = _axes(w, h)
    d = daily()
    vals = [d[d['branch'] == b]['rain_mm'].corr(d[d['branch'] == b]['customers_counted']) for b in SHOPS]
    y = np.arange(3)[::-1]
    for yy, v, b in zip(y, vals, SHOPS):
        ax.barh(yy, v, color=SHOP[b]['fc'], edgecolor=SHOP[b]['ec'] if b != 'Campus Gate' else INK, linewidth=1.8, height=0.5)
    ax.axvline(0, color=INK, lw=2)
    ax.set_xlim(-1, 1)
    ax.set_yticks(y)
    ax.set_yticklabels(SHOPS, fontsize=17)
    for yy, v in zip(y, vals):
        ax.text(v + (0.04 if v >= 0 else -0.04), yy, f'{v:.3f}', va='center', ha='left' if v >= 0 else 'right', fontsize=18, fontweight='bold')
    ax.set_xlabel('Correlation of rain with customers (the full scale is −1 to 1)')
    return Chart(f)


def _umbrella(s, x, y, size):
    """An open umbrella centred on (x, y), about `size` inches wide."""
    r = size / 2
    s.ax.add_patch(Wedge((x, y - 0.1 * size), r, 0, 180, fc=RED, ec=INK, lw=2, zorder=3))
    s.line(x, y - 0.1 * size, x, y - 0.62 * size, color=INK, lw=2.6, z=4)
    s.line(x, y - 0.62 * size, x - 0.12 * size, y - 0.62 * size, color=INK, lw=2.6, z=4)


@fig('da_cause_umbrella')
def da_cause_umbrella(w, h, **_):
    s = Scene(w, h)
    s.icon('rain', w / 2, h - 0.8, 1.2)
    s.text(w / 2 + 1.15, h - 0.8, 'rain', size=24, weight='bold', ha='left')
    s.arrow(w / 2 - 0.7, h - 1.35, 2.9, h - 2.0, color=RED, lw=2.6)
    s.arrow(w / 2 + 0.7, h - 1.35, w - 3.0, h - 2.0, color=RED, lw=2.6)
    _umbrella(s, 2.5, h - 2.3, 1.2)
    s.text(2.5, 0.75, 'umbrellas open', size=20, weight='bold')
    s.box(w - 4.6, h - 3.0, 3.4, 0.9, 'roads get wet', size=22, weight='bold', fill=GOLD, r=0.05)
    s.text(5.0, h - 2.55, 'both follow the rain,', size=18, color=RED, weight='bold')
    s.text(5.0, h - 3.0, 'so they move together', size=18, color=RED, weight='bold')
    s.text(w / 2, 0.3, 'Umbrellas do not wet the roads. The third thing, rain, drives both.', size=19, color=BODY)
    return s


# ================================================================== session 16
@fig('da_date_formats')
def da_date_formats(w, h, **_):
    import pandas as pd
    s = Scene(w, h)
    r = raw()
    rows = [r.iloc[0], r[r['sale_date'].str.contains('/')].iloc[0], r[r['sale_date'].str.contains('/')].iloc[5]]
    head = ['raw text', 'try\n%Y-%m-%d', 'try\n%d/%m/%Y', 'kept']
    data = [head]
    for rr in rows:
        t = rr['sale_date']
        a = pd.to_datetime(t, format='%Y-%m-%d', errors='coerce')
        b = pd.to_datetime(t, format='%d/%m/%Y', errors='coerce')
        keep = a if not pd.isna(a) else b
        data.append([t, str(a.date()) if not pd.isna(a) else 'NaT', str(b.date()) if not pd.isna(b) else 'NaT', str(keep.date())])
    hl = {}
    for i in (1, 2, 3):
        for c in (1, 2):
            hl[(i, c)] = GOLD if data[i][c] != 'NaT' else '#EDEDED'
        hl[(i, 3)] = GOLD
    s.table(0.2, h - 0.25, [1.9, 1.9, 1.9, 1.9], 0.68, data, size=17, hl_cells=hl, header_weight='bold')
    s.text(0.2, 1.0, 'NaT means: this format does not fit, no date made.', size=18, ha='left', color=BODY)
    s.text(0.2, 0.45, 'iso.fillna(slash) keeps whichever format fitted.', size=18, ha='left', mono=True, weight='bold')
    return s


@fig('da_name_normalise')
def da_name_normalise(w, h, **_):
    s = Scene(w, h)
    r = raw()
    official = set(products()['name'])
    lookup = {n.title(): n for n in products()['name']}
    uniq = [v for v in dict.fromkeys(r['product']) if v not in official]
    low = [v for v in uniq if v.strip().islower()][:1]
    up = [v for v in uniq if v.strip().isupper()][:1]
    sp = [v for v in uniq if v not in low + up and v.strip() == v.strip().title()][:2]
    messy = low + up + sp
    rows = [['in the raw file', '.str.strip().str.title()', 'lookup name']]
    for v in messy:
        t = v.strip().title()
        rows.append([repr(v), t, lookup[t]])
    s.table(0.15, h - 0.25, [3.0, 3.6, 2.8], 0.56, rows, size=17, align=['left', 'left', 'left'], hl_cells={(i, 2): GOLD for i in range(1, 5)})
    s.text(0.15, 0.95, 'One product, many spellings. The lookup gives each one the', size=18, ha='left', color=BODY)
    s.text(0.15, 0.45, 'single official name, so groups and totals count it once.', size=18, ha='left', color=BODY)
    return s


@fig('da_units_fix')
def da_units_fix(w, h, **_):
    s = Scene(w, h)
    r = raw()
    words_n = int(r.drop_duplicates()['units'].isin(['one', 'two', 'three', 'four', 'five']).sum())
    blank_n = int((r.drop_duplicates()['units'] == '').sum())
    w1 = r[r['units'].isin(['one', 'two', 'three', 'four', 'five'])].iloc[0]
    n1 = r[~r['units'].isin(['one', 'two', 'three', 'four', 'five', ''])].iloc[0]
    rows = [['in the file', 'after\nto_numeric', 'what happens'],
            [repr(w1['units']).strip("'"), str(int({'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}[w1['units']])), 'a word becomes a number'],
            [n1['units'], str(int(n1['units'])), 'text that is a number stays'],
            ['(blank)', 'NaN', 'cannot be repaired: left out']]
    hl = {(1, 1): GOLD, (2, 1): GOLD, (3, 1): '#F2C9C9', (3, 2): '#F2C9C9'}
    s.table(0.15, h - 0.25, [2.2, 2.7, 3.9], 0.64, rows, size=18, hl_cells=hl, align=['center', 'center', 'left'])
    s.text(0.15, 1.0, f'{words_n} rows have a word. {blank_n} rows are blank.', size=20, weight='bold', ha='left')
    s.text(0.15, 0.45, 'A blank is not zero and not the mean. Nobody knows the units.', size=18, ha='left', color=BODY)
    return s


@fig('da_residual_bar')
def da_residual_bar(w, h, **_):
    s = Scene(w, h)
    clean, excluded, _ = clean_pipeline()
    true_total = int(sales()['line_value'].sum())
    got = int(clean['line_value'].sum())
    gap = true_total - got
    x0, x1 = 2.7, w - 0.4
    sc = (x1 - x0) / true_total
    s.text(0.3, h - 1.25, 'true total', size=21, weight='bold', ha='left')
    s.rect(x0, h - 1.6, true_total * sc, 0.7, fill=PAPER, edge=INK, lw=2.0)
    s.text(x0 + true_total * sc / 2, h - 1.25, money(true_total), size=22, weight='bold', color=INK)
    s.text(0.3, h - 2.65, 'cleaned total', size=21, weight='bold', ha='left')
    s.rect(x0, h - 3.0, got * sc, 0.7, fill=GOLD, edge=INK, lw=1.8)
    s.rect(x0 + got * sc, h - 3.0, gap * sc, 0.7, fill=RED, edge=RED, lw=1.8)
    s.text(x0 + got * sc / 2, h - 2.65, money(got), size=22, weight='bold')
    s.arrow(x0 + got * sc + gap * sc / 2, h - 3.6, x0 + got * sc + gap * sc / 2, h - 3.07, color=RED, lw=2.6)
    s.text(x1, h - 3.95, f'residual {money(gap)}: the value of the {len(excluded)} sales with blank units', size=19, weight='bold', color=RED, ha='right')
    s.text(0.3, h - 0.4, 'Scaled to the same length, the gap is small and it has a name', size=20, weight='bold', ha='left')
    return s


@fig('da_function_wrap')
def da_function_wrap(w, h, **_):
    s = Scene(w, h)
    clean, excluded, steps = clean_pipeline()
    s.box(0.1, h - 2.15, 1.2, 1.2, f'raw\n{steps[0][1]:,}', size=16, lw=1.8, r=0.05, mono=True)
    s.arrow(1.33, h - 1.55, 1.78, h - 1.55, color=RED, lw=2.4)
    s.box(1.82, 1.25, 3.95, h - 1.35, '', fill=INK, edge=INK, r=0.08)
    lines = ['def clean_sales(raw):', '  drop repeats', '  parse both date formats', '  fix the names', '  words to numbers', '  split off the blanks', '  return clean, excluded']
    for i, l in enumerate(lines):
        s.text(1.98, h - 0.45 - i * 0.48, l, size=16, mono=True, color=PAPER, ha='left', weight='bold' if i in (0, 6) else 'normal')
    s.arrow(5.8, h - 1.3, 6.15, h - 1.3, color=RED, lw=2.4)
    s.box(6.2, h - 1.95, 1.4, 1.2, f'clean\n{len(clean):,}', size=16, fill=GOLD, lw=1.8, r=0.05, mono=True)
    s.arrow(5.8, h - 3.2, 6.15, h - 3.2, color=RED, lw=2.4)
    s.box(6.2, h - 3.85, 1.4, 1.2, f'excluded\n{len(excluded)}', size=16, fill=PAPER, lw=1.8, r=0.05, mono=True, edge=RED)
    s.text(0.1, 0.85, f'assert len(clean) == {len(clean)}', size=17, mono=True, ha='left', weight='bold')
    s.text(0.1, 0.35, 'stops the notebook when the steps change a count', size=16, ha='left', color=BODY)
    return s


# ================================================================== session 17
@fig('da_unique_key')
def da_unique_key(w, h, **_):
    s = Scene(w, h)
    pr = products().iloc[3:9]
    s.text(0.2, h - 0.35, 'products: each id once', size=19, weight='bold', ha='left')
    s.table(0.2, h - 0.6, [1.4, 1.9], 0.48, [['product_id', 'name']] + [[str(r.product_id), r.name] for r in pr.itertuples()], size=16, align=['center', 'left'])
    s.text(0.2, 0.7, 'is_unique  →  True', size=20, weight='bold', ha='left', mono=True)
    s.line(3.8, 0.4, 3.8, h - 0.3, color=HAIR, lw=1.2)
    s.text(4.0, h - 0.35, 'practice copy: Juice twice', size=19, weight='bold', color=RED, ha='left')
    sub = practice()
    sub = sub[sub['product_id'].between(5, 8)].reset_index(drop=True)
    rows = [['product_id', 'name']] + [[str(r.product_id), r.name] for r in sub.itertuples()]
    hl = {(i + 1, c): '#F2C9C9' for i, r in enumerate(sub.itertuples()) if r.product_id == 6 for c in (0, 1)}
    s.table(4.0, h - 0.6, [1.4, 1.9], 0.48, rows, size=16, hl_cells=hl, align=['center', 'left'])
    s.text(4.0, 0.7, 'is_unique  →  False', size=20, weight='bold', ha='left', mono=True, color=RED)
    s.text(w / 2, 0.2, 'A key must be unique in the table it looks up.', size=16, color=BODY)
    return s


@fig('da_merge_result')
def da_merge_result(w, h, **_):
    s = Scene(w, h)
    su = sales()
    pr = products()
    m = su.merge(pr[['product_id', 'category']], on='product_id', how='left')
    d = m.head(5)
    rows = [['sale_id', 'product_id', 'line_value', 'category']] + [[str(r.sale_id), str(r.product_id), money(r.line_value), r.category] for r in d.itertuples()]
    s.table(0.15, h - 0.35, [1.2, 1.6, 1.7, 1.8], 0.55, rows, size=17, hl_cols=(3,))
    s.text(7.4, h - 0.95, 'rows before the merge', size=20, ha='left', weight='bold')
    s.box(10.5, h - 1.3, 1.2, 0.6, f'{len(su):,}', size=22, weight='bold', r=0.05)
    s.text(7.4, h - 1.95, 'rows after the merge', size=20, ha='left', weight='bold')
    s.box(10.5, h - 2.3, 1.2, 0.6, f'{len(m):,}', size=22, weight='bold', fill=GOLD, r=0.05)
    s.icon('check', 7.7, 1.15, 0.75)
    s.text(8.3, 1.15, 'nothing lost, nothing copied', size=20, ha='left', weight='bold')
    return s


@fig('da_fan_out')
def da_fan_out(w, h, **_):
    s = Scene(w, h)
    su = sales()
    pr = practice()
    sale = su[su['product_id'] == 6].iloc[0]
    mm = su.merge(pr[['product_id', 'category']], on='product_id', how='left')
    n0, n1 = len(su), len(mm)
    t0, t1 = int(su['line_value'].sum()), int(mm['line_value'].sum())
    pink = '#F2C9C9'
    top = h - 0.65
    rh = 0.5
    s.text(0.3, h - 0.3, 'one sale', size=19, weight='bold', ha='left')
    s.table(0.3, top, [1.2, 0.9], rh, [['sale', 'id'], [str(sale['sale_id']), '6']], size=18)
    s.arrow(2.6, top - 0.75, 3.7, top - 0.75, color=RED, lw=2.8)
    s.text(4.0, h - 0.3, 'two Juice rows', size=19, weight='bold', ha='left')
    s.table(4.0, top, [0.9, 1.8], rh, [['id', 'category'], ['6', 'Drinks'], ['6', 'Drinks']], size=18, hl_cells={(1, 0): pink, (2, 0): pink, (1, 1): pink, (2, 1): pink})
    s.arrow(7.0, top - 0.75, 8.1, top - 0.75, color=RED, lw=2.8)
    s.text(8.4, h - 0.3, 'sale, copied', size=19, weight='bold', ha='left')
    s.table(8.4, top, [1.2, 0.9], rh, [['sale', 'id'], [str(sale['sale_id']), '6'], [str(sale['sale_id']), '6']], size=18, hl_cells={(1, 0): pink, (2, 0): pink})
    s.line(0.3, 2.15, w - 0.3, 2.15, color=HAIR, lw=1.2)
    s.text(0.3, 1.7, 'rows', size=21, weight='bold', ha='left')
    s.box(2.3, 1.4, 2.0, 0.6, f'{n0:,}', size=22, r=0.05)
    s.arrow(4.45, 1.7, 5.4, 1.7, color=RED, lw=2.8)
    s.box(5.55, 1.4, 2.0, 0.6, f'{n1:,}', size=22, r=0.05, edge=RED, lw=2.4, color=RED, weight='bold')
    s.text(7.75, 1.7, f'+{n1 - n0}', size=22, weight='bold', color=RED, ha='left')
    s.text(0.3, 0.95, 'revenue', size=21, weight='bold', ha='left')
    s.box(2.3, 0.65, 2.0, 0.6, money(t0), size=21, r=0.05)
    s.arrow(4.45, 0.95, 5.4, 0.95, color=RED, lw=2.8)
    s.box(5.55, 0.65, 2.0, 0.6, money(t1), size=21, r=0.05, edge=RED, lw=2.4, color=RED, weight='bold')
    s.text(7.75, 0.95, f'+{money(t1 - t0)}', size=21, weight='bold', color=RED, ha='left')
    s.text(0.3, 0.25, 'No error appeared. Only the counts show it.', size=17, color=BODY, ha='left')
    return s


@fig('da_validate_stop')
def da_validate_stop(w, h, **_):
    s = Scene(w, h)
    s.code(0.2, h - 0.2, ['sales.merge(practice[["product_id", "category"]],', '            on="product_id",', '            validate="many_to_one")'], size=16, line_h=0.4, w=7.3)
    s.arrow(w / 2, h - 1.75, w / 2, h - 2.3, color=RED, lw=2.6)
    s.box(0.2, 0.85, w - 0.4, 1.7, '', fill=PAPER, edge=RED, lw=3, r=0.06)
    s.text(0.45, 2.2, 'MergeError', size=24, weight='bold', color=RED, ha='left', mono=True)
    s.text(0.45, 1.45, 'Merge keys are not unique in right dataset;\nnot a many-to-one merge', size=16, mono=True, ha='left')
    s.text(w / 2, 0.38, 'validate turns a silent wrong total into a loud stop.', size=17, weight='bold')
    return s


@fig('da_rowcount_check')
def da_rowcount_check(w, h, **_):
    s = Scene(w, h)
    su = sales()
    pr = products()
    m = su.merge(pr[['product_id', 'category']], on='product_id', how='left', validate='many_to_one')
    cw, ch, y0 = 4.4, 3.6, 0.4
    for x, title, sub in [(0.3, 'before the merge', 'sales'), (w - 0.3 - cw, 'after the merge', 'sales with category')]:
        s.box(x, y0, cw, ch, '', fill=PAPER, lw=2.0, r=0.05)
        s.text(x + cw / 2, y0 + ch - 0.4, title, size=21, weight='bold')
        s.text(x + cw / 2, y0 + ch - 0.85, sub, size=17, color=BODY)
        s.text(x + cw / 2, y0 + 2.05, f'{len(su if x < 1 else m):,} rows', size=32, weight='bold')
        s.text(x + cw / 2, y0 + 1.25, f'UGX {money((su if x < 1 else m)["line_value"].sum())}', size=26, weight='bold')
        s.text(x + cw / 2, y0 + 0.55, 'revenue' if x < 1 else 'category totals add to this', size=17, color=BODY)
    s.text(w / 2, h - 0.85, 'merge', size=22, weight='bold')
    s.arrow(w / 2 - 1.3, h - 1.3, w / 2 + 1.3, h - 1.3, color=RED, lw=3, head=20)
    s.text(w / 2, h - 1.85, 'validate=\n"many_to_one"', size=16, mono=True)
    s.icon('check', w / 2, 1.55, 0.9)
    s.text(w / 2, 0.75, 'nothing changed', size=19, weight='bold')
    return s


# ================================================================== session 18
def _cp2_numbers():
    clean, excluded, steps = clean_pipeline()
    m = clean.merge(products().rename(columns={'name': 'product'})[['product', 'category']], on='product', how='left', validate='many_to_one')
    by = m.groupby('category')['line_value'].sum().sort_values(ascending=False)
    true_total = int(sales()['line_value'].sum())
    return clean, excluded, steps, m, by, true_total


@fig('da_hero_cp2')
def da_hero_cp2(w, h, **_):
    s = Scene(w, h)
    clean, excluded, steps, m, by, true_total = _cp2_numbers()
    got = int(clean['line_value'].sum())
    gap = true_total - got
    raw_n, dedup_n = steps[0][1], steps[1][1]
    s.text(0.1, h - 0.4, 'Checkpoint two: load, clean, merge, total, reconcile', size=22, weight='bold', ha='left')
    names = [('Load', f'{raw_n:,} raw rows'), ('Clean', f'{len(clean):,} rows kept'), ('Merge', f'{len(m):,} rows,\nsame count'), ('Total', f'UGX {money(by.sum())}'),
             ('Reconcile', f'true {money(true_total)}\ngap {money(gap)}')]
    n = len(names)
    x0, gap_x = 1.15, (w - 2.3) / (n - 1)
    y = h - 1.95
    s.line(x0, y, x0 + gap_x * (n - 1), y, color=INK, lw=3.2, z=1)
    for i, (a, b) in enumerate(names):
        x = x0 + i * gap_x
        s.circle(x, y, 0.42, fill=GOLD if i == n - 1 else INK, edge=INK, lw=2, z=3)
        s.text(x, y, str(i + 1), size=22, weight='bold', color=INK if i == n - 1 else PAPER, z=7)
        s.text(x, y - 0.7, a, size=21, weight='bold')
        s.text(x, y - 1.05, b, size=17, color=BODY, va='top')
    s.text(x0 + gap_x, y + 0.95, f'−{raw_n - dedup_n} repeats', size=17, weight='bold', color=RED)
    s.text(x0 + gap_x, y + 0.65, f'−{len(excluded)} blanks', size=17, weight='bold', color=RED)
    s.text(0.1, 0.85, f'Finding: {by.index[0]} earns the most, {money(by.iloc[0])} in the cleaned data.', size=19, ha='left')
    s.text(0.1, 0.35, f'Limit: {len(excluded)} sales with blank units cannot be recovered, so totals fall short by {money(gap)}.', size=19, ha='left', color=BODY)
    return s


@fig('da_cp2_checks')
def da_cp2_checks(w, h, **_):
    s = Scene(w, h)
    clean, excluded, steps, m, by, true_total = _cp2_numbers()
    got = int(clean['line_value'].sum())
    items = [f'rows kept {len(clean):,}, left out {len(excluded)}', 'product_id is unique before the merge', f'row count after the merge: {len(m):,}, unchanged',
             f'category totals add to {money(by.sum())}', f'residual named: {money(true_total - got)}']
    for i, t in enumerate(items):
        y = h - 0.55 - i * 0.82
        s.icon('check', 0.5, y, 0.58)
        s.text(1.0, y, t, size=18, ha='left')
    s.text(0.2, 0.3, 'A checkpoint is a set of checks you can show.', size=17, color=BODY, ha='left')
    return s


@fig('da_category_clean_vs_true')
def da_category_clean_vs_true(w, h, **_):
    f, ax = chart(w, h)
    clean, excluded, steps, m, by, true_total = _cp2_numbers()
    truth = sales().merge(products()[['product_id', 'category']], on='product_id', how='left').groupby('category')['line_value'].sum()
    cats = list(by.index)
    x = np.arange(len(cats))
    ax.bar(x - 0.2, [truth[c] for c in cats], 0.4, color=PAPER, edgecolor=INK, linewidth=1.8, label='true total')
    ax.bar(x + 0.2, [by[c] for c in cats], 0.4, color=GOLD, edgecolor=INK, linewidth=1.8, label='cleaned total')
    ax.set_xticks(x)
    ax.set_xticklabels(cats)
    top = truth.max() * 1.42
    for i, c in enumerate(cats):
        ax.text(i, max(truth[c], by[c]) + top * 0.03, f'short by\n{int(truth[c] - by[c]):,}', ha='center', va='bottom', fontsize=16, fontweight='bold', color=RED)
    ax.set_ylim(0, top)
    ax.set_ylabel('Revenue (UGX)')
    fmt_axis_money(ax)
    ax.legend(fontsize=16, loc='upper right', ncol=2)
    return Chart(f)


# ================================================================== session 19
@fig('da_hero_plan')
def da_hero_plan(w, h, **_):
    s = Scene(w, h)
    cards = [('Which category\nearns the most\nat each branch?', 'sales, products,\nbranches', True, 'one merge'),
             ('Which branch earns\nthe most per\ncustomer counted?', 'sales and the\ndaily summary', True, 'one division'),
             ('Did the Sugar price\nrise change its\nunits sold?', 'units and\nunit_price_ugx', True, 'two averages'),
             ('Why do people like\nCampus Gate?', 'no column\nholds opinions', False, 'cannot be answered')]
    n = len(cards)
    cw = (w - 0.4 - (n - 1) * 0.25) / n
    for i, (q, need, ok, note) in enumerate(cards):
        x = 0.2 + i * (cw + 0.25)
        s.box(x, 0.2, cw, h - 0.4, '', fill=PAPER, lw=2.0, r=0.06, edge=INK if ok else RED)
        s.text(x + cw / 2, h - 1.0, q, size=18, weight='bold', va='center')
        s.text(x + cw / 2, 2.5, 'needs', size=16, color=MUTE)
        s.text(x + cw / 2, 1.95, need, size=16)
        s.icon('check' if ok else 'cross', x + cw / 2, 1.1, 0.6)
        s.text(x + cw / 2, 0.55, note, size=16, color=BODY if ok else RED, weight='bold')
    return s


@fig('da_question_ladder')
def da_question_ladder(w, h, **_):
    s = Scene(w, h)
    su = sales()
    sg = su[su['product_id'] == 14].groupby('unit_price_ugx')['units'].mean()
    lo, hi = sg[4500], sg[5000]
    steps = [('topic', 'the Sugar price rise'), ('question', 'Did the rise change units sold?'), ('columns', 'product_id, units, unit_price_ugx'),
             ('method', 'average units per sale at each price'), ('chart', f'{lo:.2f} before, {hi:.2f} after')]
    for i, (a, b) in enumerate(steps):
        y = h - 0.5 - i * 0.84
        s.box(0.2, y - 0.3, 1.7, 0.6, a, size=18, weight='bold', fill=GOLD if i == 1 else PAPER, r=0.05)
        s.text(2.1, y, b, size=20, ha='left')
        if i < len(steps) - 1:
            s.arrow(1.05, y - 0.32, 1.05, y - 0.52, color=RED, lw=2.2, head=12)
    return s


@fig('da_ai_log_card')
def da_ai_log_card(w, h, **_):
    s = Scene(w, h)
    rows = [['log entry', 'what you write'], ['date and tool', 'or: teacher demonstration'], ['your first attempt', 'saved before any help'], ['the question you asked', 'and the reply'],
            ['accepted or rejected', 'and why'], ['the test you ran', 'and its result']]
    s.text(0.15, h - 0.3, 'AI_USE_LOG.md', size=19, weight='bold', ha='left', mono=True)
    s.table(0.15, h - 0.6, [3.1, 3.9], 0.52, rows, size=17, align=['left', 'left'], mono_cols=())
    s.text(0.15, 0.9, 'No help used? Write: No AI assistance used.', size=19, weight='bold', ha='left')
    s.text(0.15, 0.4, 'The log shows that you checked. It is not a reward.', size=18, ha='left', color=BODY)
    return s


@fig('da_licence_check')
def da_licence_check(w, h, **_):
    s = Scene(w, h)
    steps = [('Read the licence', 'at the source, on the owner\'s page', 'magnifier'), ('Instructor approves', 'and checks there are no personal details', 'person'),
             ('Say where it came from', 'a source note in the plan and the report', 'notebook')]
    for i, (a, b, ic) in enumerate(steps):
        y = h - 1.0 - i * 1.55
        s.icon(ic, 0.8, y, 0.9)
        s.text(1.7, y + 0.2, a, size=22, weight='bold', ha='left')
        s.text(1.7, y - 0.28, b, size=17, color=BODY, ha='left')
        if i < 2:
            s.arrow(0.8, y - 0.5, 0.8, y - 1.0, color=RED, lw=2.2, head=12)
    return s


# ================================================================== session 20
@fig('da_second_route')
def da_second_route(w, h, **_):
    s = Scene(w, h)
    su = sales()
    by = su.groupby('branch')['line_value'].sum()
    total = int(su['line_value'].sum())
    s.text(0.3, h - 0.35, 'Route one: add the three branch totals', size=20, weight='bold', ha='left')
    xs = [0.3, 2.5, 4.7]
    for i, (b_, v) in enumerate(by.items()):
        s.box(xs[i], h - 1.35, 2.0, 0.62, money(v), size=20, r=0.05)
        s.text(xs[i] + 1.0, h - 1.7, b_, size=16, color=MUTE)
    s.text(7.0, h - 1.04, '= ' + money(sum(by.values)), size=22, weight='bold', ha='left')
    s.line(0.3, 2.35, w - 0.3, 2.35, color=HAIR, lw=1.2)
    s.text(0.3, 2.0, 'Route two: add every sale at once', size=20, weight='bold', ha='left')
    s.code(0.3, 1.7, ['sales["line_value"].sum()'], size=16, line_h=0.4, w=4.0)
    s.text(4.6, 1.35, '= ' + money(total), size=22, weight='bold', ha='left')
    s.icon('check', 0.7, 0.4, 0.55)
    s.text(1.2, 0.4, 'the two routes agree', size=20, weight='bold', ha='left')
    return s


@fig('da_partner_rerun')
def da_partner_rerun(w, h, **_):
    s = Scene(w, h)
    s.icon('person', 0.8, h - 1.0, 0.8)
    s.text(0.8, h - 1.75, 'you', size=19, weight='bold')
    s.icon('person', w - 0.8, h - 1.0, 0.8)
    s.text(w - 0.8, h - 1.75, 'partner', size=19, weight='bold')
    s.arrow(1.6, h - 1.0, w - 1.7, h - 1.0, color=INK, lw=2.4)
    s.text(w / 2, h - 0.5, 'notebook and data file', size=17)
    s.box(w / 2 - 1.7, h - 3.0, 3.4, 0.75, 'restart, run all', size=20, weight='bold', r=0.05)
    s.arrow(w - 1.0, h - 2.05, w / 2 + 1.7, h - 2.6, color=RED, lw=2.2)
    s.box(0.2, 0.2, 3.1, 1.2, 'same numbers', size=20, weight='bold', fill=GOLD, r=0.05)
    s.box(w - 3.9, 0.2, 3.7, 1.35, 'a different number:\nfix the first cell\nthat differs', size=17, weight='bold', edge=RED, lw=2.4, r=0.05)
    s.arrow(w / 2 - 0.8, h - 3.05, 1.8, 1.45, color=INK, lw=2)
    s.arrow(w / 2 + 0.8, h - 3.05, w - 2.0, 1.6, color=RED, lw=2)
    return s


@fig('da_cleaning_log_card')
def da_cleaning_log_card(w, h, **_):
    import pandas as pd
    s = Scene(w, h)
    su = pd.read_csv(SUN / 'sales.csv')
    miss = int(su.isna().sum().sum())
    dups = int(su.duplicated().sum())
    rows = [['check on sales.csv', 'count', 'what we did'], ['missing values', str(miss), 'none found: no change'], ['duplicate rows', str(dups), 'none found: no change'],
            ['rows in the file', f'{len(su):,}', 'kept as the file came']]
    s.text(0.15, h - 0.3, 'cleaning_log.md', size=19, weight='bold', ha='left', mono=True)
    s.table(0.15, h - 0.6, [3.2, 1.3, 3.8], 0.58, rows, size=18, align=['left', 'center', 'left'])
    s.text(0.15, 1.1, '"No change needed" is a finding.', size=20, weight='bold', ha='left')
    s.text(0.15, 0.55, 'The raw export in session 16 was different: 1,538 rows, 25 repeats and 40 blank units.', size=18, ha='left', color=BODY)
    return s


# ================================================================== session 21
@fig('da_report_anatomy')
def da_report_anatomy(w, h, **_):
    s = Scene(w, h)
    by = sales().groupby('branch')['line_value'].sum().sort_values(ascending=False)
    px, pw = 0.2, 3.4
    s.box(px, 0.15, pw, h - 0.3, '', fill=PAPER, lw=2.0, r=0.02)
    s.text(px + 0.2, h - 0.5, 'Revenue by branch', size=17, weight='bold', ha='left')
    for i, v in enumerate(by.values):
        s.rect(px + 0.35 + i * 1.0, 1.85, 0.8, 1.7 * v / by.max(), fill=GOLD if i == 0 else PAPER, edge=INK, lw=1.6)
    s.line(px + 0.3, 1.85, px + pw - 0.3, 1.85, color=INK, lw=1.8)
    for y, k in ((1.5, 0), (1.25, 0), (0.9, 1), (0.45, 2)):
        s.line(px + 0.3, y, px + pw - 0.3 - 0.5 * (k == 2), y, color=HAIR if k < 2 else GREY, lw=3.4, z=3)
    labels = [('title says what\nis shown', h - 0.5, h - 0.5), ('one chart, axes\nlabelled with units', h - 1.9, h - 1.9), ('findings, each next\nto its evidence', 1.5, 1.4),
              ('limitation in\nplain words', 0.9, 0.9), ('data source note', 0.45, 0.45)]
    for t, y, ay in labels:
        s.text(px + pw + 0.85, y, t, size=16, weight='bold', ha='left', color=RED)
        s.arrow(px + pw + 0.8, y, px + pw - 0.15, ay, color=RED, lw=2, head=12)
    return s


@fig('da_savefig_flow')
def da_savefig_flow(w, h, **_):
    s = Scene(w, h)
    s.text(0.2, h - 0.35, 'Right order', size=20, weight='bold', ha='left')
    s.code(0.2, h - 0.65, ['plt.bar(by.index, by.values)', 'plt.savefig("revenue.png", bbox_inches="tight")', 'plt.show()'], size=16, line_h=0.4, w=6.9)
    s.icon('check', 7.3, h - 1.3, 0.55)
    s.line(0.2, h - 2.25, w - 0.2, h - 2.25, color=HAIR, lw=1.2)
    s.text(0.2, h - 2.6, 'Wrong order: a blank picture', size=20, weight='bold', ha='left', color=RED)
    s.code(0.2, h - 2.9, ['plt.bar(by.index, by.values)', 'plt.show()', 'plt.savefig("revenue.png", bbox_inches="tight")'], size=16, line_h=0.4, w=6.9, hl_lines=(2,))
    s.icon('cross', 7.3, h - 3.55, 0.55)
    s.text(0.2, 0.22, 'show clears the figure, so save first. tight keeps the labels in.', size=16, ha='left', color=BODY)
    return s


@fig('da_ai_critique_loop')
def da_ai_critique_loop(w, h, **_):
    s = Scene(w, h)
    nodes = [('Your own attempt first', 'notebook'), ('Ask for a hint, not an answer', 'magnifier'), ('Predict, run, test it', 'calculator'), ('Keep or reject, and say why', 'check')]
    for i, (lab, ic) in enumerate(nodes):
        y = h - 0.65 - i * 1.0
        s.icon(ic, 0.8, y, 0.6)
        s.text(1.5, y, lab, size=20, ha='left', weight='bold')
        if i < 3:
            s.arrow(0.8, y - 0.36, 0.8, y - 0.64, color=RED, lw=2.4)
    s.text(0.2, 0.55, 'Write each turn in AI_USE_LOG.md.', size=17, color=BODY, ha='left')
    s.text(0.2, 0.2, 'You explain every line you keep.', size=17, color=BODY, ha='left')
    return s


# ================================================================== session 22
@fig('da_hero_handover')
def da_hero_handover(w, h, **_):
    s = Scene(w, h)
    s.icon('folder', 1.9, h - 2.0, 2.8)
    s.text(1.9, 1.05, 'my project folder', size=22, weight='bold')
    files = [('project.ipynb', 'the code, rerun clean'), ('cleaning_log.md', 'every row removed'), ('data_dictionary.md', 'every column used'),
             ('report.pdf', 'the one page report'), ('AI_USE_LOG.md', 'every use of AI')]
    top = h - 0.7
    ys = [top - i * 0.72 for i in range(len(files))]
    s.line(4.35, ys[0], 4.35, ys[-1], color=INK, lw=2.4, z=2)
    s.arrow(3.35, h - 2.2, 4.3, h - 2.2, color=RED, lw=3, head=18)
    for (nm, what), y in zip(files, ys):
        s.line(4.35, y, 4.75, y, color=INK, lw=2.4, z=2)
        s.text(4.9, y, nm, size=19, weight='bold', mono=True, ha='left')
        s.text(8.7, y, what, size=19, ha='left', color=BODY)
    s.text(w / 2 + 1.5, 0.45, 'Each file opens, reruns and agrees with the others.', size=20, color=BODY)
    return s


@fig('da_report_page')
def da_report_page(w, h, **_):
    s = Scene(w, h)
    su = sales()
    by = su.groupby('branch')['line_value'].sum().sort_values(ascending=False)
    total = int(su['line_value'].sum())
    s.box(0.2, 0.1, w - 0.4, h - 0.2, '', fill=PAPER, lw=2.0, r=0.02)
    rows = [('question', 'Which shop earns the most?'), ('data', 'Sunrise Shops sales, invented, 60 days, 1,513 rows'), ('method', 'total each shop, check against the grand total'),
            ('finding', f'{by.index[0]} earns {money(by.iloc[0])} of {money(total)}'), ('finding', f'{by.index[-1]} earns the least, {money(by.iloc[-1])}'),
            ('recommend', 'compare revenue per customer counted before any decision'), ('limit', 'no costs, so no profit; data is invented')]
    for i, (a, b) in enumerate(rows):
        y = h - 0.5 - i * 0.55
        s.text(0.45, y, a, size=17, weight='bold', ha='left', color=RED if a == 'limit' else INK)
        s.text(2.2, y, b, size=17, ha='left')
    return s


# ================================================================== session 23
@fig('da_talk_storyboard')
def da_talk_storyboard(w, h, **_):
    s = Scene(w, h)
    by = sales().groupby('branch')['line_value'].sum().sort_values(ascending=False)
    frames = [('My question', 'Which shop\nearns the most?'), ('My data', '1,513 sales,\n3 shops,\n60 days,\ninvented'), ('What I did', 'cleaned,\nmerged,\nadded up,\nchecked'),
              ('What I found', f'{by.index[0]}\n{money(by.iloc[0])}'), ('What it\ncannot show', 'costs, so\nno profit')]
    n = 5
    fw = (w - 0.4 - 4 * 0.2) / n
    for i, (a, b) in enumerate(frames):
        x = 0.2 + i * (fw + 0.2)
        s.box(x, 0.25, fw, h - 0.5, '', fill=PAPER, lw=1.8, r=0.04)
        s.text(x + fw / 2, h - 0.85, a, size=19, weight='bold')
        if i == 3:
            for k, v in enumerate(by.values):
                s.rect(x + 0.32 + k * 0.62, 1.3, 0.5, 1.2 * v / by.max(), fill=GOLD if k == 0 else PAPER, edge=INK, lw=1.4)
            s.text(x + fw / 2, 0.8, b, size=17, weight='bold')
        else:
            s.text(x + fw / 2, h / 2 - 0.35, b, size=18, va='center')
    return s


@fig('da_talk_timeline')
def da_talk_timeline(w, h, **_):
    s = Scene(w, h)
    parts = [('question', 0.5), ('data', 0.5), ('what I did', 1.0), ('finding', 2.0), ('limit and next step', 1.0), ('questions', 3.0)]
    total = sum(m for _, m in parts)
    x0, sc = 0.2, (w - 0.4) / total
    t = 0
    for i, (lab, m) in enumerate(parts):
        bw = m * sc
        last = i == len(parts) - 1
        s.box(x0 + t * sc, h - 2.2, bw, 1.0, '', fill=GOLD if i == 3 else (PAPER if last else INK), edge=INK if (last or i == 3) else PAPER, lw=1.8, r=0.02)
        ly = h - 2.2 - 0.4 - (i % 2) * 0.5
        if i % 2 or bw < 1.5:
            s.line(x0 + t * sc + bw / 2, h - 2.2, x0 + t * sc + bw / 2, ly + 0.17, color=INK, lw=1.2)
        s.text(x0 + t * sc + bw / 2, ly, lab, size=17, color=INK)
        t += m
    s.text(x0, h - 0.5, 'The five minutes', size=22, weight='bold', ha='left')
    s.text(x0 + 2.5 * sc, h - 0.95, '5 minutes of talking', size=18, color=BODY)
    s.text(x0 + 6.5 * sc, h - 0.95, '3 minutes of questions', size=18, color=BODY)
    s.icon('clock', w / 2 - 2.6, 0.75, 0.9)
    s.text(w / 2 - 1.9, 0.75, 'a timer in the corner of the room', size=20, ha='left', weight='bold')
    return s


@fig('da_three_questions')
def da_three_questions(w, h, **_):
    s = Scene(w, h)
    rows = [('"Where did this number come from?"', 'the output cell\nin your notebook'), ('"What did you clean?"', 'your\ncleaning log'), ('"What can this data not tell us?"', 'the limitation\nyou wrote')]
    for i, (q, a) in enumerate(rows):
        y = h - 0.8 - i * 1.3
        s.icon('person', 0.7, y, 0.75)
        s.box(1.5, y - 0.45, 5.2, 0.9, q, size=19, r=0.05)
        s.arrow(6.8, y, 7.6, y, color=RED, lw=2.6)
        s.box(7.7, y - 0.45, 3.8, 0.9, a, size=18, fill=GOLD, r=0.05, weight='bold')
    return s


@fig('da_backup_plan')
def da_backup_plan(w, h, **_):
    s = Scene(w, h)
    s.box(0.4, h - 2.0, 4.2, 1.7, 'live notebook', size=26, weight='bold', r=0.05)
    s.arrow(4.7, h - 1.15, 7.2, h - 1.15, color=RED, lw=3, head=20)
    s.text(5.95, h - 0.65, 'if the laptop fails', size=19, color=RED, weight='bold')
    s.box(7.3, h - 2.0, 4.2, 1.7, 'PDF and\nscreenshots', size=26, weight='bold', fill=GOLD, r=0.05)
    s.line(0.4, 1.75, w - 0.4, 1.75, color=HAIR, lw=1.2)
    s.text(0.4, 1.2, '1   Explain the workflow aloud while the pictures stay on screen.', size=20, ha='left')
    s.text(0.4, 0.55, '2   Arrange a short live rerun afterwards if evidence is missing.', size=20, ha='left')
    return s


# ================================================================== session 24
@fig('da_hero_showcase')
def da_hero_showcase(w, h, **_):
    s = Scene(w, h)
    parts = [('setup and backups', 30), ('welcome', 10), ('presentations and questions', 40), ('break', 10), ('feedback and certificates', 20), ('reflection and next steps', 70)]
    total = sum(m for _, m in parts)
    x0, x1 = 4.4, w - 0.3
    sc = (x1 - x0) / total
    s.text(0.3, h - 0.4, 'The showcase session, in minutes', size=22, weight='bold', ha='left')
    t = 0
    for i, (lab, m) in enumerate(parts):
        y = h - 1.1 - i * 0.52
        s.text(0.3, y, lab, size=19, ha='left', weight='bold' if i == 2 else 'normal')
        fill = GOLD if i == 2 else (PAPER if i in (1, 3, 4) else INK)
        col = INK if fill != INK else PAPER
        s.box(x0 + t * sc, y - 0.2, m * sc, 0.4, str(m), size=18, fill=fill, edge=INK, lw=1.6, r=0.02, color=col, weight='bold')
        t += m
    s.text(0.3, 0.3, 'Parents and guardians join for welcome, presentations and certificates.', size=19, ha='left', color=BODY)
    return s


@fig('da_next_goal')
def da_next_goal(w, h, **_):
    s = Scene(w, h)
    s.box(0.3, 0.3, w - 0.6, h - 0.6, '', fill=PAPER, lw=2.0, r=0.04)
    fields = [('my next goal', 4.15, 2), ('my first step', 2.65, 2), ('by when', 1.15, 1)]
    for lab, y, n in fields:
        s.text(0.7, y, lab, size=22, weight='bold', ha='left')
        for k in range(n):
            s.line(0.7, y - 0.5 - k * 0.45, w - 0.7, y - 0.5 - k * 0.45, color=INK, lw=1.4, z=3)
    s.icon('pen', w - 1.1, h - 0.85, 0.9)
    return s


# ================================================================== word icons (1.3 x 1.3 inches each)
def _frame(s, size=1.0):
    return s.w / 2, s.h / 2


@fig('da_icon_corr')
def da_icon_corr(w, h, **_):
    s = Scene(w, h)
    s.line(0.2, 0.2, 0.2, 1.15, color=INK, lw=2.2, z=2)
    s.line(0.2, 0.2, 1.15, 0.2, color=INK, lw=2.2, z=2)
    rng = np.random.RandomState(4)
    for i in range(12):
        t = i / 11
        x = 0.38 + 0.7 * t
        y = 0.38 + 0.62 * t + rng.uniform(-0.1, 0.1)
        s.circle(x, y, 0.065, fill=INK, edge=INK, lw=1)
    return s


@fig('da_icon_strength')
def da_icon_strength(w, h, **_):
    s = Scene(w, h)
    s.line(0.15, 0.65, 1.15, 0.65, color=INK, lw=3, z=2)
    for k in (0.15, 0.65, 1.15):
        s.line(k, 0.5, k, 0.8, color=INK, lw=2.4, z=2)
    s.circle(1.0, 0.65, 0.17, fill=RED, edge=RED, lw=1.5, z=4)
    return s


@fig('da_icon_heat')
def da_icon_heat(w, h, **_):
    s = Scene(w, h)
    shades = [[RED, '#F5F5F5', '#BDBDBD'], ['#F5F5F5', INK, '#8C8C8C'], ['#BDBDBD', '#8C8C8C', INK]]
    for r in range(3):
        for c in range(3):
            s.rect(0.2 + c * 0.3, 0.2 + (2 - r) * 0.3, 0.3, 0.3, fill=shades[r][c], edge=INK, lw=1.4)
    return s


@fig('da_icon_hue')
def da_icon_hue(w, h, **_):
    s = Scene(w, h)
    for x, y, fc, ec in [(0.45, 0.85, INK, INK), (0.9, 0.7, RED, RED), (0.65, 0.4, GOLD, INK), (0.35, 0.4, INK, INK), (0.95, 0.35, GOLD, INK), (0.65, 0.95, RED, RED)]:
        s.circle(x, y, 0.13, fill=fc, edge=ec, lw=1.6)
    return s


def _bars(s, heights, fills=None):
    n = len(heights)
    bw = 0.9 / n
    for i, hh in enumerate(heights):
        s.rect(0.2 + i * bw, 0.2, bw, hh, fill=(fills or {}).get(i, PAPER), edge=INK, lw=1.4)
    s.line(0.15, 0.2, 1.15, 0.2, color=INK, lw=2.2, z=3)


@fig('da_icon_hist')
def da_icon_hist(w, h, mode='bell', **_):
    s = Scene(w, h)
    if mode == 'bell':
        _bars(s, [0.15, 0.35, 0.7, 0.95, 0.65, 0.3, 0.12])
    else:
        _bars(s, [0.95, 0.7, 0.42, 0.25, 0.15, 0.1, 0.06], fills={5: GOLD, 6: GOLD})
    return s


@fig('da_icon_box')
def da_icon_box(w, h, **_):
    s = Scene(w, h)
    s.line(0.65, 0.15, 0.65, 1.15, color=INK, lw=2.2, z=2)
    s.line(0.45, 0.15, 0.85, 0.15, color=INK, lw=2.2, z=2)
    s.line(0.45, 1.15, 0.85, 1.15, color=INK, lw=2.2, z=2)
    s.rect(0.38, 0.4, 0.54, 0.5, fill=GOLD, edge=INK, lw=2, z=3)
    s.line(0.38, 0.62, 0.92, 0.62, color=RED, lw=3.4, z=4)
    return s


@fig('da_icon_boxes')
def da_icon_boxes(w, h, **_):
    s = Scene(w, h)
    for x, lo, hi, med in [(0.3, 0.25, 0.8, 0.5), (0.65, 0.2, 0.65, 0.4), (1.0, 0.3, 0.95, 0.6)]:
        s.line(x, 0.15, x, 1.15, color=INK, lw=1.8, z=2)
        s.rect(x - 0.12, lo + 0.1, 0.24, hi - lo, fill=PAPER, edge=INK, lw=1.6, z=3)
        s.line(x - 0.12, med + 0.1, x + 0.12, med + 0.1, color=RED, lw=2.8, z=4)
    return s


@fig('da_icon_elementwise')
def da_icon_elementwise(w, h, **_):
    s = Scene(w, h)
    for i in range(3):
        x = 0.2 + i * 0.32
        s.rect(x, 0.9, 0.3, 0.25, fill=PAPER, edge=INK, lw=1.6)
        s.arrow(x + 0.15, 0.86, x + 0.15, 0.46, color=RED, lw=2.2, head=11)
        s.rect(x, 0.2, 0.3, 0.25, fill=GOLD, edge=INK, lw=1.6)
    return s


@fig('da_icon_percentile')
def da_icon_percentile(w, h, **_):
    s = Scene(w, h)
    hs = [0.15, 0.25, 0.38, 0.52, 0.68, 0.85, 1.0]
    bw = 0.13
    for i, hh in enumerate(hs):
        s.rect(0.17 + i * bw, 0.15, bw, hh * 0.9, fill=GOLD if i == 3 else PAPER, edge=INK, lw=1.4)
    s.line(0.17 + 3.5 * bw, 0.1, 0.17 + 3.5 * bw, 1.2, color=RED, lw=2.6, z=4, dash=True)
    return s


@fig('da_icon_sd')
def da_icon_sd(w, h, **_):
    s = Scene(w, h)
    s.line(0.1, 0.35, 1.2, 0.35, color=INK, lw=2.2, z=2)
    s.line(0.65, 0.2, 0.65, 1.2, color=RED, lw=3, z=2)
    for x, y in [(0.3, 0.55), (0.45, 0.85), (0.55, 0.65), (0.8, 0.75), (0.95, 0.55), (0.72, 1.0), (0.2, 0.95), (1.05, 0.9)]:
        s.circle(x, y, 0.06, fill=INK, edge=INK, lw=1)
    s.arrow(0.65, 0.2, 1.05, 0.2, color=INK, lw=2, head=11)
    return s


@fig('da_icon_pipeline')
def da_icon_pipeline(w, h, **_):
    s = Scene(w, h)
    for i in range(3):
        x = 0.1 + i * 0.42
        s.rect(x, 0.45, 0.3, 0.4, fill=GOLD if i == 2 else PAPER, edge=INK, lw=1.8)
        if i < 2:
            s.arrow(x + 0.31, 0.65, x + 0.42, 0.65, color=RED, lw=2, head=9)
    return s


@fig('da_icon_residual')
def da_icon_residual(w, h, **_):
    s = Scene(w, h)
    s.rect(0.1, 0.6, 1.1, 0.3, fill=PAPER, edge=INK, lw=1.8)
    s.rect(0.1, 0.25, 0.92, 0.3, fill=GOLD, edge=INK, lw=1.8)
    s.rect(1.02, 0.25, 0.18, 0.3, fill=RED, edge=RED, lw=1.8)
    return s


def _card(s, x, y, w_, h_, fill=PAPER, lines=2):
    s.rect(x, y, w_, h_, fill=fill, edge=INK, lw=1.8, z=3)
    for k in range(lines):
        s.line(x + 0.07, y + h_ - 0.14 - k * 0.14, x + w_ - 0.07, y + h_ - 0.14 - k * 0.14, color=INK, lw=1.4, z=4)


@fig('da_icon_mergekey')
def da_icon_mergekey(w, h, **_):
    s = Scene(w, h)
    _card(s, 0.1, 0.5, 0.45, 0.55)
    _card(s, 0.75, 0.5, 0.45, 0.55)
    s.line(0.55, 0.62, 0.75, 0.62, color=RED, lw=3.4, z=5)
    return s


@fig('da_icon_merge')
def da_icon_merge(w, h, mode='merge', **_):
    s = Scene(w, h)
    _card(s, 0.1, 0.8, 0.4, 0.35)
    _card(s, 0.1, 0.25, 0.4, 0.35, fill=PAPER if mode == 'merge' else '#EDEDED')
    s.arrow(0.55, 0.95, 0.75, 0.75, color=RED, lw=2, head=10)
    s.arrow(0.55, 0.45, 0.75, 0.65, color=RED, lw=2, head=10)
    _card(s, 0.8, 0.45, 0.4, 0.5, fill=GOLD)
    return s


@fig('da_icon_fanout')
def da_icon_fanout(w, h, **_):
    s = Scene(w, h)
    _card(s, 0.1, 0.5, 0.4, 0.4)
    s.arrow(0.52, 0.72, 0.78, 1.0, color=RED, lw=2, head=10)
    s.arrow(0.52, 0.68, 0.78, 0.4, color=RED, lw=2, head=10)
    _card(s, 0.8, 0.9, 0.4, 0.25, fill=GOLD)
    _card(s, 0.8, 0.2, 0.4, 0.25, fill=GOLD)
    return s


@fig('da_icon_scope')
def da_icon_scope(w, h, **_):
    s = Scene(w, h)
    s.box(0.2, 0.3, 0.7, 0.7, '', fill=PAPER, lw=2, r=0.05, dash=True)
    for x, y in [(0.4, 0.5), (0.65, 0.8), (0.7, 0.45), (0.45, 0.75)]:
        s.circle(x, y, 0.06, fill=GOLD, edge=INK, lw=1.4, z=4)
    for x, y in [(1.1, 0.4), (1.05, 1.1), (0.15, 1.1)]:
        s.circle(x, y, 0.06, fill=GREY, edge=GREY, lw=1.4, z=4)
    return s


@fig('da_icon_licence')
def da_icon_licence(w, h, **_):
    s = Scene(w, h)
    s.rect(0.15, 0.3, 1.0, 0.7, fill=PAPER, edge=INK, lw=2)
    for k in range(3):
        s.line(0.3, 0.88 - k * 0.14, 0.8, 0.88 - k * 0.14, color=INK, lw=1.6, z=4)
    s.circle(0.9, 0.45, 0.14, fill=GOLD, edge=INK, lw=1.8, z=4)
    return s


@fig('da_icon_caption')
def da_icon_caption(w, h, **_):
    s = Scene(w, h)
    s.rect(0.2, 0.55, 0.9, 0.55, fill=PAPER, edge=INK, lw=2)
    for x, hh in [(0.35, 0.18), (0.55, 0.3), (0.75, 0.22)]:
        s.rect(x, 0.62, 0.14, hh, fill=GOLD, edge=INK, lw=1.2, z=4)
    s.line(0.3, 0.35, 1.0, 0.35, color=INK, lw=2.6, z=3)
    s.line(0.3, 0.2, 0.75, 0.2, color=INK, lw=2.6, z=3)
    return s


@fig('da_icon_cause')
def da_icon_cause(w, h, **_):
    s = Scene(w, h)
    s.box(0.1, 0.45, 0.4, 0.4, '', fill=GOLD, lw=1.8, r=0.04)
    s.arrow(0.52, 0.65, 0.78, 0.65, color=RED, lw=3, head=14)
    s.box(0.8, 0.45, 0.4, 0.4, '', fill=PAPER, lw=1.8, r=0.04)
    return s
