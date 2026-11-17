"""Repairs for the Python for Data Analysis figures of sessions 1 to 12 (imported after figs_da, so these names win).

Also holds the purpose-made 1.3 x 1.3 inch word icons (r1_icon_*) so that no pictogram is reused inside one deck.
"""
import numpy as np
import pandas as pd

from figs_da_util import (Scene, fig, Chart, chart, shop, sales, daily, raw, money, fmt_axis_money, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD)
from figs_da_b import _counts
import figkit


# ============================================================ figures
@fig('da_totals_check')
def da_totals_check(w, h, **_):
    s = Scene(w, h)
    su = sales()
    g = su.groupby('branch')['line_value'].sum()
    names = ['Central Market', 'Campus Gate', 'Roadside']
    full = int(g.sum())
    lost = int(su[su['branch'] == 'Central Market']['line_value'].iloc[0])
    bw = 2.3
    xs = [0.3, 3.3, 6.3]
    tx = 9.2
    tw = 2.0

    def row(y, vals, ok, first_red=False):
        for k, (x, v) in enumerate(zip(xs, vals)):
            red = first_red and k == 0
            s.box(x, y - 0.32, bw, 0.64, money(v), size=20, r=0.05, edge=RED if red else INK, lw=2.6 if red else 1.6, weight='bold')
        s.text(xs[1] - 0.35, y, '+', size=28, weight='bold')
        s.text(xs[2] - 0.35, y, '+', size=28, weight='bold')
        s.text(xs[2] + bw + 0.4, y, '=', size=28, weight='bold')
        s.box(tx, y - 0.32, tw, 0.64, money(sum(vals)), size=20, r=0.05, fill=GOLD if ok else PAPER, edge=INK if ok else RED, lw=2.0, weight='bold')
        s.icon('check' if ok else 'cross', tx + tw + 0.5, y, 0.6)

    s.text(0.3, h - 0.35, 'Every sale is still there', size=21, weight='bold', ha='left')
    for x, nm in zip(xs, names):
        s.text(x + bw / 2, h - 0.9, nm, size=18, color=BODY)
    s.text(tx + tw / 2, h - 0.9, 'the pieces added', size=18, color=BODY)
    row(h - 1.5, [int(g[n]) for n in names], True)
    s.text(0.3, h - 2.1, f'{money(full)} is the grand total, so the pieces match', size=18, ha='left', color=BODY)
    s.line(0.3, h - 2.45, w - 0.3, h - 2.45, color=HAIR, lw=1.2)
    s.text(0.3, h - 2.85, 'One sale was lost on the way', size=21, weight='bold', ha='left', color=RED)
    vals = [int(g['Central Market']) - lost, int(g['Campus Gate']), int(g['Roadside'])]
    row(h - 3.5, vals, False, True)
    s.text(0.3, h - 4.1, f'{money(sum(vals))} does not match {money(full)}', size=18, ha='left', color=RED, weight='bold')
    return s


@fig('da_cleaning_log')
def da_cleaning_log(w, h, **_):
    s = Scene(w, h)
    n, dup, kept, blank, slash = _counts()
    rows = [['problem', 'rows'], ['duplicate rows', str(dup)], ['blank units', str(blank)], ['dates with slashes', str(slash)]]
    s.text(0.3, h - 0.3, 'cleaning_log.csv', size=19, weight='bold', ha='left', mono=True)
    s.table(0.3, h - 0.6, [3.1, 1.2], 0.45, rows, size=19, align=['left', 'center'])
    s.text(0.3, h - 2.7, 'One line for each problem, with its row count.', size=18, color=BODY, ha='left')
    s.text(0.3, h - 3.1, 'to_csv(..., index=False)', size=18, mono=True, weight='bold', ha='left')
    data = [['rows'], [str(dup)], [str(blank)], [str(slash)]]
    s.text(0.3, h - 3.5, 'without index=False', size=16, color=RED, ha='left')
    s.table(0.3, h - 3.65, [0.6, 1.3], 0.28, [['', 'rows']] + [[str(i), r[0]] for i, r in enumerate(data[1:])], size=14,
            hl_cells={(0, 0): '#EEEEEE', **{(i, 0): '#F2C9C9' for i in (1, 2, 3)}})
    s.text(3.4, h - 3.5, 'with index=False', size=16, ha='left')
    s.table(3.4, h - 3.65, [1.3], 0.28, data, size=14, hl_cells={(i, 0): GOLD for i in (1, 2, 3)})
    s.text(5.0, h - 4.2, 'no extra\nrow-number\ncolumn', size=15, ha='left', color=BODY)
    return s


@fig('da_chart_anatomy')
def da_chart_anatomy(w, h, **_):
    figkit.use_style()
    import matplotlib.pyplot as plt
    f = plt.figure(figsize=(w, h))
    ax = f.add_axes([0.5, 0.29, 0.47, 0.55])
    d = shop().groupby('item')['revenue_ugx'].sum().reindex(['Book', 'Juice', 'Pen'])
    ax.bar(d.index, d.values, color=[GOLD, PAPER, PAPER], edgecolor=INK, linewidth=2)
    ax.set_ylim(0, d.max() * 1.1)
    ax.set_ylabel('Revenue (UGX)', fontsize=15)
    ax.set_title('Revenue by item', loc='left', fontsize=17)
    ax.tick_params(labelsize=14)
    fmt_axis_money(ax)
    kw = dict(fontsize=16, color=RED, fontweight='bold', va='center', ha='left', textcoords='figure fraction', annotation_clip=False,
              arrowprops=dict(arrowstyle='-|>', color=RED, lw=1.8, shrinkA=3, shrinkB=2))
    kw2 = dict(kw, arrowprops=dict(kw['arrowprops'], relpos=(1.0, 0.5)))
    ax.annotate('title: says what\nis shown', xy=(0.0, 1.05), xycoords='axes fraction', xytext=(0.02, 0.9), **kw2)
    ax.annotate('axis label: the quantity\nand its unit', xy=(-0.41, 0.5), xycoords='axes fraction', xytext=(0.02, 0.58), **kw2)
    ax.annotate('the axis starts at zero', xy=(0.0, 0.0), xycoords='axes fraction', xytext=(0.02, 0.33), **kw2)
    f.text(0.735, 0.115, 'one bar for each category', fontsize=16, color=RED, fontweight='bold', va='center', ha='center')
    f.text(0.5, 0.035, 'Source: camp_shop.csv', fontsize=14, color=INK, va='center', ha='left')
    f.text(0.02, 0.07, 'source note: where\nthe data came from', fontsize=16, color=RED, fontweight='bold', va='center', ha='left')
    f.add_artist(plt.matplotlib.patches.FancyArrowPatch((0.30, 0.05), (0.485, 0.036), transform=f.transFigure, arrowstyle='-|>', mutation_scale=16,
                                                        color=RED, lw=1.8, shrinkA=0, shrinkB=0))
    return Chart(f)


@fig('da_scatter_cr')
def da_scatter_cr(w, h, **_):
    f, ax = chart(w, h)
    d = daily()
    ax.scatter(d['customers_counted'], d['revenue_ugx'], s=38, color=INK, alpha=0.75)
    ax.set_xlabel('Customers counted in a day')
    ax.set_ylabel('Revenue that day (UGX)')
    fmt_axis_money(ax)
    pt = d[(d['customers_counted'].between(95, 105)) & (d['revenue_ugx'] > 70000)].iloc[0]
    ax.annotate('one dot = one shop on one day', xy=(pt['customers_counted'], pt['revenue_ugx']), xytext=(15, 122000), fontsize=16, fontweight='bold', color=RED,
                arrowprops=dict(arrowstyle='-|>', color=RED, lw=2))
    ax.text(0.98, 0.07, f'{len(d)} dots: more customers\nusually bring more money', transform=ax.transAxes, fontsize=16, fontweight='bold', va='bottom', ha='right',
            bbox=dict(boxstyle='round,pad=0.35', fc='white', ec=INK, lw=1.2), zorder=10)
    return Chart(f)


@fig('da_revenue_card')
def da_revenue_card(w, h, **_):
    s = Scene(w, h)
    sh = shop()
    s.text(0.2, h - 0.45, 'units × price = revenue, row by row', size=19, weight='bold', ha='left')
    for i, r in enumerate(sh.head(3).itertuples()):
        yy = h - 1.25 - i * 0.7
        s.box(0.2, yy - 0.28, 3.3, 0.56, f'{r.units} × {r.unit_price_ugx:,} = {r.revenue_ugx:,}', size=19, mono=True, fill=PAPER, lw=1.6, r=0.04)
    s.text(0.2, h - 3.45, f'. . . and {len(sh) - 3} more rows', size=19, color=BODY, ha='left')
    s.arrow(3.85, h / 2 - 0.2, 5.0, h / 2 - 0.2, color=RED, lw=2.6, head=18)
    s.text(4.42, h / 2 + 0.15, 'sum', size=20, weight='bold', color=RED, mono=True)
    s.icon('coin', 6.3, h / 2 + 0.55, 1.5, text='UGX')
    s.text(6.3, h / 2 - 0.5, money(sh['revenue_ugx'].sum()), size=30, weight='bold')
    s.text(6.3, h / 2 - 1.0, 'revenue', size=20, color=BODY)
    return s


@fig('da_profit_unknown')
def da_profit_unknown(w, h, **_):
    s = Scene(w, h)
    rev = money(shop()['revenue_ugx'].sum())
    s.box(0.3, h - 1.5, w - 0.6, 0.85, f'revenue  {rev}', size=26, weight='bold', fill=GOLD, lw=2.0, r=0.05)
    s.box(0.3, h - 2.75, w - 0.6, 0.85, 'cost of the stock: not in the table', size=22, color=RED, weight='bold', fill=PAPER, edge=RED, lw=2.6, r=0.05)
    s.line(0.3, h - 3.1, w - 0.3, h - 3.1, color=INK, lw=2.0)
    s.text(0.3, h - 3.65, 'profit = revenue − cost = ?', size=26, weight='bold', ha='left')
    s.text(0.3, 0.45, 'We can report revenue and stop there.', size=19, color=BODY, ha='left')
    return s


@fig('r1_assert_demo')
def r1_assert_demo(w, h, **_):
    from figs_common import Code
    s = Scene(w, h)
    cb = Code(s, 0.2, h - 0.3, ['assert revenue(3, 2000) == 6000', 'assert revenue(0, 2000) == 0', 'assert revenue(5, 1000) == 5000'], size=19, lead=1.9)
    s.text(0.2, cb.bottom - 0.4, 'three checks, each with an answer we already know', size=18, color=BODY, ha='left')
    x0 = cb.x0 + cb.w + 0.5
    cw = (w - x0 - 0.2 - 0.3) / 2
    for i, (head, out, edge, fill, col) in enumerate([('every check passes', 'prints nothing', INK, GOLD, INK),
                                                       ('one check fails', 'AssertionError', RED, PAPER, RED)]):
        x = x0 + i * (cw + 0.3)
        s.text(x + cw / 2, h - 0.55, head, size=20, weight='bold', color=col)
        s.box(x, h - 2.35, cw, 1.4, out, size=20, mono=True, weight='bold', fill=fill, edge=edge, lw=2.4, r=0.05, color=col)
    s.text(x0 + cw / 2, h - 2.85, 'silence means pass', size=18, color=BODY)
    s.text(x0 + cw * 1.5 + 0.3, h - 2.85, 'the program stops', size=18, color=RED)
    return s


# ============================================================ word icons, drawn for a 1.3 x 1.3 canvas
@fig('r1_icon_venn')
def r1_icon_venn(w, h):
    s = Scene(w, h)
    s.circle(0.47, 0.65, 0.38, fill=PAPER, edge=INK, lw=2.2)
    s.circle(0.83, 0.65, 0.38, fill=PAPER, edge=INK, lw=2.2)
    s.poly([(0.65, 0.98), (0.85, 0.65), (0.65, 0.32), (0.45, 0.65)], fill=GOLD, edge=INK, lw=1.4, z=4)
    return s


@fig('r1_icon_index')
def r1_icon_index(w, h):
    s = Scene(w, h)
    s.arrow(w / 2, 1.2, w / 2, 0.86, color=RED, lw=2.6, head=14)
    s.box(0.4, 0.3, 0.5, 0.55, '0', size=22, weight='bold', mono=True, fill=GOLD, lw=2.2, r=0.04)
    return s


@fig('r1_icon_dict')
def r1_icon_dict(w, h):
    s = Scene(w, h)
    for i in range(3):
        y = 0.9 - i * 0.3
        s.box(0.15, y - 0.12, 0.45, 0.26, '', fill=PAPER, lw=1.8, r=0.02)
        s.box(0.7, y - 0.12, 0.45, 0.26, '', fill=GOLD if i == 1 else PAPER, lw=1.8, r=0.02)
    return s


@fig('r1_icon_running')
def r1_icon_running(w, h):
    s = Scene(w, h)
    for i in range(4):
        s.box(0.12 + i * 0.29, 0.2, 0.25, 0.25 + i * 0.22, '', fill=GOLD if i == 3 else PAPER, lw=1.8, r=0.01)
    return s


@fig('r1_icon_funnel')
def r1_icon_funnel(w, h):
    s = Scene(w, h)
    s.poly([(0.15, 1.05), (1.15, 1.05), (0.74, 0.55), (0.74, 0.15), (0.56, 0.15), (0.56, 0.55)], fill=PAPER, edge=INK, lw=2.2)
    s.circle(0.4, 0.8, 0.07, fill=INK, edge=INK, lw=1)
    s.circle(0.65, 0.88, 0.07, fill=GOLD, edge=INK, lw=1.4)
    s.circle(0.9, 0.8, 0.07, fill=INK, edge=INK, lw=1)
    return s


@fig('r1_icon_sort')
def r1_icon_sort(w, h):
    s = Scene(w, h)
    for i, v in enumerate(['3', '1', '2']):
        s.box(0.15 + i * 0.37, 0.8, 0.33, 0.33, v, size=14, weight='bold', mono=True, fill=PAPER, lw=1.6, r=0.02)
    s.arrow(w / 2, 0.76, w / 2, 0.5, color=RED, lw=2.4, head=12)
    for i, v in enumerate(['1', '2', '3']):
        s.box(0.15 + i * 0.37, 0.1, 0.33, 0.33, v, size=14, weight='bold', mono=True, fill=GOLD, lw=1.6, r=0.02)
    return s


@fig('r1_icon_median')
def r1_icon_median(w, h):
    s = Scene(w, h)
    for i in range(5):
        s.box(0.12 + i * 0.23, 0.2, 0.2, 0.3 + i * 0.12, '', fill=GOLD if i == 2 else PAPER, lw=1.6, r=0.01)
    s.line(0.12 + 2 * 0.23 + 0.1, 0.1, 0.12 + 2 * 0.23 + 0.1, 1.2, color=RED, lw=2.0, dash=True)
    return s


@fig('r1_icon_pie')
def r1_icon_pie(w, h):
    s = Scene(w, h)
    for r in range(2):
        for c in range(5):
            s.box(0.1 + c * 0.22, 0.45 + r * 0.26, 0.2, 0.24, '', fill=GOLD if (r == 0 and c < 3) else PAPER, lw=1.4, r=0.01)
    return s


@fig('r1_icon_fraction')
def r1_icon_fraction(w, h):
    s = Scene(w, h)
    s.box(0.35, 0.8, 0.6, 0.3, '', fill=GOLD, lw=1.8, r=0.02)
    s.line(0.2, 0.65, 1.1, 0.65, color=INK, lw=3.0)
    s.box(0.2, 0.15, 0.9, 0.35, '', fill=PAPER, lw=1.8, r=0.02)
    return s


@fig('r1_icon_dup')
def r1_icon_dup(w, h):
    s = Scene(w, h)
    for k, (dx, dy) in enumerate([(0.0, 0.0), (0.18, -0.2)]):
        s.box(0.12 + dx, 0.55 + dy, 0.85, 0.5, '', fill=PAPER if k else GOLD, lw=2.0, r=0.03, z=2 + k)
        s.line(0.25 + dx, 0.88 + dy, 0.8 + dx, 0.88 + dy, color=INK, lw=2.2, z=5)
        s.line(0.25 + dx, 0.72 + dy, 0.6 + dx, 0.72 + dy, color=INK, lw=2.2, z=5)
    return s


@fig('r1_icon_blank')
def r1_icon_blank(w, h):
    s = Scene(w, h)
    for r in range(3):
        for c in range(3):
            blank = (r == 1 and c == 1)
            s.box(0.18 + c * 0.32, 0.18 + r * 0.32, 0.3, 0.3, '', fill=GOLD if blank else PAPER, lw=1.6, r=0.01)
    return s


@fig('r1_icon_bar')
def r1_icon_bar(w, h):
    s = Scene(w, h)
    s.line(0.12, 0.15, 1.2, 0.15, color=INK, lw=2.2)
    for i, v in enumerate([0.5, 0.95, 0.7]):
        s.box(0.2 + i * 0.34, 0.15, 0.28, v, '', fill=GOLD if i == 1 else PAPER, lw=1.8, r=0.01)
    return s


@fig('r1_icon_hist')
def r1_icon_hist(w, h):
    s = Scene(w, h)
    s.line(0.1, 0.15, 1.2, 0.15, color=INK, lw=2.2)
    for i, v in enumerate([0.9, 0.7, 0.45, 0.28, 0.15]):
        s.box(0.15 + i * 0.2, 0.15, 0.2, v, '', fill=GREY if i else GOLD, lw=1.4, r=0.0)
    return s


@fig('r1_icon_line')
def r1_icon_line(w, h):
    s = Scene(w, h)
    pts = [(0.15, 0.35), (0.4, 0.6), (0.65, 0.45), (0.9, 0.85), (1.15, 0.7)]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        s.line(x1, y1, x2, y2, color=INK, lw=3.0)
    for i, (x, y) in enumerate(pts):
        s.circle(x, y, 0.06, fill=GOLD if i == 3 else INK, edge=INK, lw=1.4, z=4)
    return s


@fig('r1_icon_scatter')
def r1_icon_scatter(w, h):
    s = Scene(w, h)
    for i, (x, y) in enumerate([(0.2, 0.25), (0.35, 0.4), (0.5, 0.35), (0.6, 0.62), (0.78, 0.55), (0.9, 0.85), (1.05, 0.95), (0.45, 0.55)]):
        s.circle(x, y, 0.065, fill=GOLD if i == 5 else INK, edge=INK, lw=1.2)
    return s


@fig('r1_icon_axes')
def r1_icon_axes(w, h):
    s = Scene(w, h)
    s.line(0.25, 0.15, 0.25, 1.15, color=INK, lw=2.6)
    s.line(0.25, 0.15, 1.2, 0.15, color=INK, lw=2.6)
    for i in range(1, 4):
        s.line(0.25, 0.15 + i * 0.28, 0.35, 0.15 + i * 0.28, color=INK, lw=2.0)
        s.line(0.25 + i * 0.28, 0.15, 0.25 + i * 0.28, 0.25, color=INK, lw=2.0)
    s.box(0.5, 0.5, 0.5, 0.2, '', fill=GOLD, lw=1.6, r=0.02)
    return s
