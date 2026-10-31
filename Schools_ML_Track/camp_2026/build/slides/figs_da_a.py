"""DA figures, part A: sessions 7 to 9 (tables, select/filter/new column, group/sort/mean/median)."""
import numpy as np
import pandas as pd

from figs_da_util import (file_shape, Scene, fig, Chart, chart, shop, sales, products, daily, money, strip, fmt_axis_money, INK, BODY, MUTE, GREY, HAIR,
                          PAPER, RED, GOLD, BRANCH)
import figkit


# ------------------------------------------------------------------ session 7
@fig('da_tables_hero')
def da_tables_hero(w, h, **_):
    s = Scene(w, h)
    sh, su, pr = shop(), sales(), products()
    cards = [('camp_shop.csv', file_shape('camp_shop.csv'), 'a practice shop', 'notebook'),
             ('sunrise_products.csv', file_shape('products.csv'), 'the price board', 'tag'),
             ('sunrise_sales.csv', file_shape('sales.csv'), 'three shops, 60 days', 'receipt')]
    cw = w / 3
    for i, (name, shp, what, icon) in enumerate(cards):
        cx = cw * i + cw / 2
        s.icon(icon, cx, h - 0.75, 0.95)
        s.text(cx, h - 1.55, name, size=21, weight='bold')
        s.text(cx, h - 1.95, what, size=17, color=MUTE)
        rows, cols = shp
        gw, gh = 0.5 * cols / 1.0 * 0.62, 1.2
        x0 = cx - gw / 2
        ccw = gw / cols
        for c in range(cols):
            for r in range(4):
                s.rect(x0 + c * ccw, h - 2.35 - gh * (r + 1) / 4, ccw, gh / 4, fill=PAPER, edge=INK, lw=1.3)
        s.text(cx, h - 2.35 - gh - 0.18, '. . .', size=20, color=MUTE)
        s.text(cx, 0.68, f'{rows:,} rows', size=24, weight='bold')
        s.text(cx, 0.28, f'{cols} columns', size=20, color=BODY)
    return s


@fig('da_table_anatomy')
def da_table_anatomy(w, h, **_):
    s = Scene(w, h)
    sh = shop().head(5)
    cols = ['sale_id', 'date', 'item', 'units', 'unit_price_ugx']
    rows = [cols] + [[str(v) for v in r] for r in sh[cols].values.tolist()]
    cw = [1.0, 1.4, 0.9, 0.85, 1.85]
    x0, y_top = 0.2, h - 1.05
    rh = 0.46
    s.table(x0, y_top, cw, rh, rows, size=16, hl_cols=(3,))
    s.rect(x0, y_top - 4 * rh, sum(cw), rh, fill='none', edge=RED, lw=3, z=5)
    s.text(x0 + 0.95, h - 0.4, 'header: the name of each column', size=18, ha='left', weight='bold')
    s.arrow(x0 + 1.7, h - 0.62, x0 + 1.7, y_top + 0.02, color=RED, lw=2)
    s.text(x0 + sum(cw) / 2, 0.35, 'column: one kind of fact, here the units sold', size=18, ha='center')
    s.arrow(x0 + sum(cw[:3]) + cw[3] / 2, 0.62, x0 + sum(cw[:3]) + cw[3] / 2, y_top - 6 * rh + 0.06, color=INK, lw=2)
    s.text(x0 + sum(cw) + 0.1, y_top - 3.5 * rh, 'row:\none sale', size=18, ha='left', color=RED, weight='bold')
    s.text(w - 0.15, h - 0.4, 'shape (60, 5)', size=19, color=MUTE, weight='bold', ha='right')
    return s


@fig('da_df_from_dict')
def da_df_from_dict(w, h, **_):
    s = Scene(w, h)
    s.code(0.3, h - 0.25, ['sales = pd.DataFrame({', '  "item": ["Book", "Pen", "Book"],', '  "units": [2, 5, 3]})'], size=15, line_h=0.34, w=5.9)
    tx, ty, rh = 1.9, h - 2.45, 0.5
    s.table(tx, ty, [1.4, 1.4], rh, [['item', 'units'], ['Book', '2'], ['Pen', '5'], ['Book', '3']], size=20)
    s.arrow(1.8, h - 1.62, tx + 0.7, ty + 0.03, color=RED, lw=2, rad=0.0)
    s.arrow(3.3, h - 1.62, tx + 2.1, ty + 0.03, color=RED, lw=2, rad=0.0)
    s.text(tx + 3.1, ty - 2 * rh, 'each key is a\ncolumn header,\neach list fills\nthe column', size=17, ha='left', color=BODY)
    s.text(tx + 1.4, ty - 4 * rh - 0.28, 'shape (3, 2)', size=19, weight='bold', color=MUTE)
    return s


@fig('da_csv_to_df')
def da_csv_to_df(w, h, **_):
    s = Scene(w, h)
    sh = shop()
    lines = ['sale_id,date,item,units,unit_price_ugx'] + [','.join(str(v) for v in r) for r in sh.head(3)[['sale_id', 'date', 'item', 'units', 'unit_price_ugx']].values.tolist()]
    cwid, chh = 5.6, 1.55
    top = h - 0.25
    s.box(0.3, top - chh, cwid, chh, '', fill=PAPER, lw=1.6, r=0.05)
    s.text(0.45, top - 0.12, 'camp_shop.csv: plain text, commas between the boxes', size=15, ha='left', color=MUTE, va='top')
    for i, l in enumerate(lines):
        s.text(0.5, top - 0.52 - i * 0.27, l, size=16, mono=True, ha='left')
    s.arrow(w / 2 - 0.9, top - chh - 0.1, w / 2 - 0.9, top - chh - 0.62, color=RED, lw=2.4)
    s.text(w / 2 - 0.65, top - chh - 0.36, 'pd.read_csv("camp_shop.csv")', size=17, weight='bold', color=RED, ha='left')
    rows = [['sale_id', 'date', 'item', 'units', 'unit_price_ugx']] + [[str(v) for v in r] for r in sh.head(3)[['sale_id', 'date', 'item', 'units', 'unit_price_ugx']].values.tolist()]
    s.table(0.3, top - chh - 0.72, [0.95, 1.4, 0.85, 0.8, 1.85], 0.44, rows, size=16)
    s.text(0.3, 0.3, 'a DataFrame: the same facts, now in rows and named columns', size=17, ha='left', color=BODY)
    return s


@fig('da_shape_rule')
def da_shape_rule(w, h, **_):
    s = Scene(w, h)
    gx, gy, gw, gh = 0.9, 0.9, 3.0, 2.7
    for c in range(5):
        for r in range(12):
            s.rect(gx + c * gw / 5, gy + r * gh / 12, gw / 5, gh / 12, fill=PAPER, edge=INK, lw=0.9)
    s.brace(gx, gx + gw, gy + gh + 0.12, depth=0.14, up=True, color=RED, lw=2.4)
    s.text(gx + gw / 2, gy + gh + 0.55, f'columns: {file_shape("camp_shop.csv")[1]}', size=20, color=RED, weight='bold')
    s.line(gx - 0.12, gy, gx - 0.12, gy + gh, color=INK, lw=2.4)
    s.line(gx - 0.12, gy, gx - 0.02, gy, color=INK, lw=2.4)
    s.line(gx - 0.12, gy + gh, gx - 0.02, gy + gh, color=INK, lw=2.4)
    s.text(gx - 0.3, gy + gh / 2, f'rows: {file_shape("camp_shop.csv")[0]}', size=20, weight='bold', rot=90)
    s.text(gx + gw / 2, 0.45, 'camp_shop.csv', size=18, color=MUTE)
    sh, su, pr = shop(), sales(), products()
    sunrise_shape = file_shape('sales.csv')
    x = 5.1
    s.text(x, h - 0.45, 'shape = (rows, columns)', size=24, weight='bold', ha='left')
    items = [('shop.shape', file_shape('camp_shop.csv'), 'practice sales'), ('products.shape', pr.shape, 'price board'), ('sunrise.shape', sunrise_shape, 'shop sales')]
    for i, (code, shp, what) in enumerate(items):
        y = h - 1.3 - i * 0.85
        s.box(x, y - 0.32, 2.5, 0.64, code, size=18, fill=INK, edge=INK, color=PAPER, mono=True, r=0.06)
        s.arrow(x + 2.6, y, x + 3.2, y, color=INK, lw=2)
        s.text(x + 3.3, y, f'({shp[0]:,}, {shp[1]})', size=24, weight='bold', ha='left')
        s.text(x + 5.0, y, what, size=18, color=MUTE, ha='left')
    s.text(x, 0.5, 'The first number counts the rows.\nThe second number counts the columns.', size=19, ha='left', color=BODY)
    return s


@fig('da_dtypes')
def da_dtypes(w, h, **_):
    s = Scene(w, h)
    sh = shop().head(4)
    cols = ['sale_id', 'date', 'item', 'units', 'unit_price_ugx']
    cw = [1.1, 1.45, 0.95, 0.95, 1.95]
    x0, y_top, rh = 0.55, h - 0.5, 0.52
    rows = [cols] + [[str(v) for v in r] for r in sh[cols].values.tolist()]
    s.table(x0, y_top, cw, rh, rows, size=16)
    kinds = ['whole number', 'text', 'text', 'whole number', 'whole number']
    x = x0
    tag_y = 0.95
    for i, k in enumerate(kinds):
        fill = GOLD if k == 'text' else INK
        col = INK if k == 'text' else PAPER
        s.box(x + 0.04, tag_y, cw[i] - 0.08, 0.7, k.replace(' ', '\n'), size=16, fill=fill, edge=INK, color=col, weight='bold', r=0.05)
        s.arrow(x + cw[i] / 2, tag_y + 0.72, x + cw[i] / 2, y_top - 5 * rh - 0.03, color=INK, lw=1.6, head=12)
        x += cw[i]
    s.text(w / 2, 0.4, 'print(shop.dtypes) tells you what kind of thing each column holds', size=18, color=BODY)
    return s


@fig('da_icon_grid')
def da_icon_grid(w, h, mode='row', **_):
    s = Scene(w, h)
    n = 4
    cell = 0.26
    x0, y0 = (w - n * cell) / 2, (h - n * cell) / 2
    for r in range(n):
        for c in range(n):
            hit = (mode == 'row' and r == 1) or (mode == 'col' and c == 2)
            s.rect(x0 + c * cell, y0 + (n - 1 - r) * cell, cell, cell, fill=GOLD if hit else PAPER, edge=INK, lw=1.4)
    return s


# ------------------------------------------------------------------ session 8
@fig('da_hero_takings')
def da_hero_takings(w, h, **_):
    s = Scene(w, h)
    sh = shop()
    tot = sh.groupby('item')['revenue_ugx'].sum()
    items = [('Book', 'book'), ('Pen', 'pen'), ('Juice', 'bottle')]
    xs = [1.6, 4.3, 7.0]
    for (it, ic), x in zip(items, xs):
        s.icon(ic, x, h - 1.35, 1.2)
        s.text(x, h - 2.3, it, size=22, weight='bold')
        s.box(x - 1.0, h - 3.55, 2.0, 0.75, money(tot[it]), size=24, fill=GOLD, weight='bold', r=0.05)
    for x in (2.95, 5.65):
        s.text(x, h - 3.17, '+', size=34, weight='bold')
    s.text(8.3, h - 3.17, '=', size=34, weight='bold')
    s.icon('coin', 10.15, h - 2.2, 2.0, text='UGX')
    s.text(10.15, h - 3.55, money(tot.sum()), size=30, weight='bold')
    s.text(w / 2, 0.35, 'Revenue: the money the sales brought in, before paying for stock', size=19, color=BODY)
    return s


@fig('da_select_column')
def da_select_column(w, h, **_):
    s = Scene(w, h)
    sh = shop().head(5)
    cols = ['item', 'units', 'unit_price_ugx']
    cw = [1.0, 0.95, 1.9]
    rows = [cols] + [[str(v) for v in r] for r in sh[cols].values.tolist()]
    x0, y_top, rh = 0.25, h - 0.95, 0.46
    s.text(x0, h - 0.45, 'shop', size=20, weight='bold', ha='left', mono=True)
    s.table(x0, y_top, cw, rh, rows, size=16, hl_cols=(1,))
    s.box(0.25, 0.3, 3.7, 0.62, 'shop["units"]', size=20, fill=INK, edge=INK, color=PAPER, mono=True, r=0.06)
    s.arrow(1.9, 0.95, x0 + cw[0] + cw[1] / 2, y_top - 6 * rh - 0.03, color=RED, lw=2, rad=0.0)
    s.arrow(x0 + sum(cw) + 0.25, y_top - 3 * rh, 5.8, y_top - 3 * rh, color=INK, lw=2.4)
    s.table(5.9, y_top, [1.5], rh, [['units']] + [[str(v)] for v in sh['units']], size=18, hl_cells={(r, 0): GOLD for r in range(1, 6)})
    s.text(6.65, y_top - 6 * rh - 0.3, 'one column', size=17, color=MUTE)
    return s


@fig('da_filter_mask')
def da_filter_mask(w, h, **_):
    s = Scene(w, h)
    sh = shop().head(8)
    mask = sh['units'] >= 5
    rows = [['item', 'units', 'units >= 5']] + [[r.item, str(r.units), str(bool(m))] for r, m in zip(sh.itertuples(), mask)]
    x0, y_top, rh = 0.2, h - 0.35, 0.42
    hl = {}
    for i, m in enumerate(mask, start=1):
        if m:
            for c in range(3):
                hl[(i, c)] = GOLD
    s.table(x0, y_top, [1.0, 0.95, 1.65], rh, rows, size=16, hl_cells=hl)
    kept = sh[mask]
    s.arrow(x0 + 3.75, y_top - 4.5 * rh, 4.9, y_top - 4.5 * rh, color=RED, lw=2.4)
    s.text(4.3, y_top - 4.5 * rh + 0.35, 'keep\nTrue', size=17, color=RED, weight='bold')
    s.table(5.0, y_top, [1.0, 0.95], rh, [['item', 'units']] + [[r.item, str(r.units)] for r in kept.itertuples()], size=16, hl_cells={(i, c): GOLD for i in range(1, len(kept) + 1) for c in range(2)})
    s.text(5.5, y_top - (len(kept) + 1) * rh - 0.35, f'{len(kept)} of these 8 rows stay', size=17, color=MUTE)
    s.text(x0, 0.3, 'The mask is a True or False for every row. Only True rows stay.', size=17, ha='left', color=BODY)
    return s


@fig('da_new_column')
def da_new_column(w, h, **_):
    s = Scene(w, h)
    sh = shop().head(5)
    cw = [1.0, 0.8, 0.4, 1.7, 0.4, 1.75]
    hdr = ['item', 'units', '', 'unit_price_ugx', '', 'revenue_ugx']
    rows = [hdr]
    for r in sh.itertuples():
        rows.append([r.item, str(r.units), '×', str(r.unit_price_ugx), '=', money(r.revenue_ugx)])
    x0, y_top, rh = 0.15, h - 0.3, 0.46
    hl = {(i, 5): GOLD for i in range(0, 6)}
    s.table(x0, y_top, cw, rh, rows, size=16, hl_cells=hl)
    total = shop()['revenue_ugx'].sum()
    s.text(x0, y_top - 6 * rh - 0.38, 'shop["revenue_ugx"] =', size=16, mono=True, ha='left')
    s.text(x0 + 0.4, y_top - 6 * rh - 0.7, 'shop["units"] * shop["unit_price_ugx"]', size=16, mono=True, ha='left')
    s.box(0.15, 0.2, 4.2, 0.6, f'all 60 rows add to {money(total)}', size=19, fill=GOLD, weight='bold', r=0.05)
    return s


@fig('da_revenue_card')
def da_revenue_card(w, h, **_):
    s = Scene(w, h)
    s.icon('coin', w / 2, h - 1.4, 1.9, text='UGX')
    s.text(w / 2, h - 2.55, money(shop()['revenue_ugx'].sum()), size=34, weight='bold')
    s.text(w / 2, h - 3.1, 'revenue: money taken in', size=20, color=BODY)
    return s


@fig('da_profit_unknown')
def da_profit_unknown(w, h, **_):
    s = Scene(w, h)
    s.text(w / 2, h - 0.8, f'{money(shop()["revenue_ugx"].sum())}', size=28, weight='bold')
    s.text(w / 2, h - 1.35, '− the cost of the stock', size=22)
    s.box(w / 2 - 1.3, h - 2.45, 2.6, 0.7, '?', size=34, fill=PAPER, edge=RED, color=RED, weight='bold', lw=2.4)
    s.text(w / 2, h - 3.0, '= profit', size=22, weight='bold')
    s.text(w / 2, 0.35, 'the table has no cost column', size=18, color=RED, weight='bold')
    return s


@fig('da_filter_copy')
def da_filter_copy(w, h, **_):
    s = Scene(w, h)
    sh = shop()
    mask = (sh['units'] >= 5).values
    gx = 0.7
    cs = 0.29
    s.text(gx + 3 * cs, h - 0.35, f'shop: all {len(sh)} rows', size=20, weight='bold')
    for i in range(len(sh)):
        c, r = i % 6, i // 6
        s.rect(gx + c * cs, h - 0.75 - (r + 1) * cs, cs, cs, fill=GOLD if mask[i] else PAPER, edge=INK, lw=1.0)
    s.arrow(gx + 6 * cs + 0.3, h - 2.1, 8.1, h - 2.1, color=RED, lw=2.6)
    s.text(5.1, h - 1.7, 'big = shop[shop["units"] >= 5]', size=17, mono=True, ha='center')
    kept = int(mask.sum())
    s.text(9.6, h - 0.35, f'big: {kept} rows', size=20, weight='bold')
    for k in range(kept):
        c, r = k % 6, k // 6
        s.rect(8.7 + c * cs, h - 0.75 - (r + 1) * cs, cs, cs, fill=GOLD, edge=INK, lw=1.0)
    s.text(gx + 3 * cs, 0.4, f'shop still has {len(sh)} rows', size=21, weight='bold')
    s.text(9.6, 0.4, 'a new, smaller table', size=19, color=BODY)
    return s


# ------------------------------------------------------------------ session 9
@fig('da_hero_piles')
def da_hero_piles(w, h, **_):
    s = Scene(w, h)
    sh = shop()
    units = sh.groupby('item')['units'].sum()
    rev = sh.groupby('item')['revenue_ugx'].sum()
    items = [('Book', 'book'), ('Pen', 'pen'), ('Juice', 'bottle')]
    s.text(1.0, h - 1.95, 'units sold', size=20, weight='bold', ha='left')
    s.text(1.0, h - 3.45, 'money taken (UGX)', size=20, weight='bold', ha='left')
    for i, (it, ic) in enumerate(items):
        x = 5.4 + i * 2.5
        s.icon(ic, x, h - 0.75, 0.95)
        s.text(x, h - 1.45, it, size=20, weight='bold')
        s.box(x - 0.95, h - 2.3, 1.9, 0.62, str(units[it]), size=24, fill=GOLD if units[it] == units.max() else PAPER, weight='bold', r=0.05)
        s.box(x - 0.95, h - 3.8, 1.9, 0.62, money(rev[it]), size=24, fill=GOLD if rev[it] == rev.max() else PAPER, weight='bold', r=0.05)
    s.text(w / 2, 0.45, 'The item that sells the most units is not the item that earns the most money.', size=20, color=BODY)
    return s


@fig('da_split_apply_combine')
def da_split_apply_combine(w, h, **_):
    s = Scene(w, h)
    sh = shop()
    n = sh.groupby('item').size()
    tot = sh.groupby('item')['revenue_ugx'].sum()
    s.text(1.0, h - 0.4, 'all rows', size=20, weight='bold')
    for i in range(12):
        c = i % 3
        s.box(0.2 + c * 0.62, h - 1.0 - (i // 3) * 0.5 - 0.44, 0.56, 0.44, ['B', 'P', 'J'][c], size=15, fill=PAPER, r=0.03, lw=1.3)
    s.arrow(2.35, h - 2.1, 3.0, h - 2.1, lw=2.4)
    s.text(2.65, h - 1.65, 'split', size=19, weight='bold', color=RED)
    ys = [h - 1.2, h - 2.5, h - 3.8]
    for it, y, lab in zip(['Book', 'Pen', 'Juice'], ys, ['B', 'P', 'J']):
        for k in range(4):
            s.box(3.1 + k * 0.5, y - 0.18, 0.44, 0.4, lab, size=14, r=0.03, lw=1.3)
        s.text(3.1 + 1.0, y - 0.55, f'{it}: {n[it]} sales', size=16, color=MUTE)
        s.arrow(5.3, y, 5.9, y, lw=2.2)
        s.box(6.0, y - 0.3, 1.55, 0.6, money(tot[it]), size=19, fill=GOLD, weight='bold', r=0.05)
    s.text(5.6, h - 0.45, 'add each pile', size=19, weight='bold', color=RED)
    s.text(w - 0.2, 0.35, f'combined: {money(tot.sum())}', size=19, weight='bold', ha='right')
    return s


@fig('da_units_bar')
def da_units_bar(w, h, which='units', **_):
    f, ax = chart(w, h)
    sh = shop()
    col = 'units' if which == 'units' else 'revenue_ugx'
    d = sh.groupby('item')[col].sum().reindex(['Book', 'Pen', 'Juice'])
    colors = [GOLD if v == d.max() else PAPER for v in d.values]
    bars = ax.bar(d.index, d.values, color=colors, edgecolor=INK, linewidth=1.8)
    for b, v in zip(bars, d.values):
        ax.text(b.get_x() + b.get_width() / 2, v, f'{int(v):,}', ha='center', va='bottom', fontsize=19, fontweight='bold')
    ax.set_ylim(0, d.max() * 1.18)
    ax.set_ylabel('Units sold' if which == 'units' else 'Revenue (UGX)')
    if which != 'units':
        fmt_axis_money(ax)
    ax.set_title('Pen sells the most units' if which == 'units' else 'Book earns the most money', loc='left')
    return Chart(f)


@fig('da_mean_pulled')
def da_mean_pulled(w, h, **_):
    s = Scene(w, h)
    su = sales()
    first = list(su['units'].head(9))
    big = int(su['units'].max())
    vals = first + [big]
    mean, med = float(np.mean(vals)), float(np.median(vals))
    x0, x1 = 0.7, w - 0.6
    ymid = h * 0.52
    mx = max(vals) + 2
    px = lambda v: x0 + (x1 - x0) * v / mx
    s.line(x0, ymid, x1, ymid, color=INK, lw=2)
    for t in range(0, mx + 1, 5):
        s.line(px(t), ymid - 0.08, px(t), ymid + 0.08, color=INK, lw=1.6)
        s.text(px(t), ymid - 0.35, str(t), size=16, color=MUTE)
    seen = {}
    for v in vals:
        k = seen.get(v, 0)
        seen[v] = k + 1
        s.circle(px(v), ymid + 0.32 + 0.32 * k, 0.14, fill=GOLD if v == big else INK, edge=INK, lw=1.4, z=4)
    s.text(px(big) - 0.1, ymid + 0.95, 'one bulk sale', size=17, ha='right', weight='bold')
    s.arrow(px(med), ymid - 1.35, px(med), ymid - 0.55, color=INK, lw=2.4)
    s.text(px(med), ymid - 1.7, f'median {med:g}', size=20, weight='bold')
    s.arrow(px(mean), ymid - 1.35, px(mean), ymid - 0.55, color=RED, lw=2.4)
    s.text(px(mean) + 0.1, ymid - 1.7, f'mean {mean:g}', size=20, weight='bold', color=RED, ha='left')
    s.text(w / 2, h - 0.4, 'Units in 10 real sales: nine ordinary ones and the largest', size=19, weight='bold')
    s.text(w / 2, 0.45, 'The bulk sale pulls the mean to the right.\nThe median stays with the ordinary sales.', size=17, color=BODY)
    return s


@fig('da_hist_mean_median')
def da_hist_mean_median(w, h, **_):
    f, ax = chart(w, h)
    v = sales()['line_value']
    ax.hist(v, bins=np.arange(0, 20001, 1000), color=GREY, edgecolor=PAPER)
    mean, med = v.mean(), v.median()
    ax.axvline(med, color=INK, lw=3)
    ax.axvline(mean, color=RED, lw=3)
    top = ax.get_ylim()[1]
    ax.annotate(f'median {int(med):,}', xy=(med, top * 0.8), xytext=(8000, top * 0.85), fontsize=18, fontweight='bold', va='center',
                arrowprops=dict(arrowstyle='-|>', color=INK, lw=2))
    ax.annotate(f'mean {int(round(mean)):,}', xy=(mean, top * 0.6), xytext=(8000, top * 0.62), fontsize=18, fontweight='bold', color=RED, va='center',
                arrowprops=dict(arrowstyle='-|>', color=RED, lw=2))
    ax.set_xlabel('Value of one sale (UGX)')
    ax.set_ylabel('Number of sales')
    ax.set_xlim(0, 20000)
    fmt_axis_money(ax, 'x')
    ax.text(19900, top * 0.3, f'the tail runs on\nto {int(v.max()):,}', ha='right', fontsize=16, color=INK)
    return Chart(f)


@fig('da_proportion_grid')
def da_proportion_grid(w, h, **_):
    s = Scene(w, h)
    su = sales()
    n = len(su)
    big = (su['units'] >= 10).values
    cols = 76
    cs = (w - 0.6) / cols
    top = h - 0.6
    for i in range(n):
        c, r = i % cols, i // cols
        if not big[i]:
            s.rect(0.3 + c * cs, top - (r + 1) * cs, cs * 0.8, cs * 0.8, fill=PAPER, edge=GREY, lw=0.5)
    for i in range(n):
        c, r = i % cols, i // cols
        if big[i]:
            s.rect(0.3 + c * cs - cs * 0.35, top - (r + 1) * cs - cs * 0.35, cs * 1.5, cs * 1.5, fill=GOLD, edge=INK, lw=1.2, z=4)
    s.text(0.3, h - 0.25, f'each small square is one of the {n:,} sales', size=17, ha='left', color=MUTE)
    k = int(big.sum())
    s.text(w / 2, 1.85, f'{k} of {n:,} sales have 10 units or more', size=24, weight='bold')
    s.text(w / 2, 1.2, f'{k} / {n:,} = {100 * k / n:.1f}%', size=28, weight='bold')
    s.text(w / 2, 0.5, f'the denominator is {n:,}: the whole we measure against', size=18, color=BODY)
    return s


@fig('da_totals_check')
def da_totals_check(w, h, **_):
    s = Scene(w, h)
    sh = shop()
    tot = sh.groupby('item')['revenue_ugx'].sum()
    full = sh['revenue_ugx'].sum()
    lost = sh['revenue_ugx'].iloc[0]
    xs = [0.6, 2.55, 4.5]
    bw = 1.5

    def row(y, vals, ok, color_first=INK):
        for k, (x, v) in enumerate(zip(xs, vals)):
            s.box(x, y - 0.3, bw, 0.6, money(v), size=18, r=0.05, edge=RED if (k == 0 and color_first == RED) else INK, lw=2.4 if (k == 0 and color_first == RED) else 1.6)
        s.text(2.33, y, '+', size=26, weight='bold')
        s.text(4.28, y, '+', size=26, weight='bold')
        s.text(6.3, y, '=', size=26, weight='bold')
        s.icon('check' if ok else 'cross', 7.0, y, 0.7)

    s.text(0.3, h - 0.45, 'Every row is still there', size=20, weight='bold', ha='left')
    row(h - 1.2, [tot['Book'], tot['Juice'], tot['Pen']], True)
    s.text(0.3, h - 1.85, f'{money(full)} is the overall total, so the piles match', size=17, ha='left', color=MUTE)
    s.line(0.3, h - 2.3, w - 0.3, h - 2.3, color=HAIR, lw=1.2)
    s.text(0.3, h - 2.75, 'One sale was lost on the way', size=20, weight='bold', ha='left', color=RED)
    book = tot['Book'] - lost
    row(h - 3.5, [book, tot['Juice'], tot['Pen']], False, RED)
    s.text(0.3, h - 4.2, f'{money(book + tot["Juice"] + tot["Pen"])} does not match {money(full)}', size=17, ha='left', color=RED)
    return s
