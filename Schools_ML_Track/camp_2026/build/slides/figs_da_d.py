"""DA figures, part D: sessions 16 to 18 (cleaning the raw export, merging, checkpoint two)."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from figs_da_util import (SUN, Scene, fig, Chart, chart, sales, products, daily, raw, practice, money, fmt_axis_money, clean_pipeline, INK, BODY, MUTE,
                          GREY, HAIR, PAPER, RED, GOLD)
from figs_da_b import _flow
import figkit


def _messy_samples():
    """One real raw row for each kind of defect, with the matching cleaned row (by sale_id)."""
    r = raw()
    clean, excluded, _ = clean_pipeline()
    official = set(products()['name'])
    slash = r[r['sale_date'].str.contains('/')].iloc[0]
    name = r[~r['product'].isin(official) & ~r['product'].duplicated(keep=False).eq(False)].iloc[0] if False else None
    messy_names = r[~r['product'].isin(official)]
    name = messy_names[messy_names['product'].map(lambda v: v.strip().islower() or v.strip().isupper())].iloc[0]
    word = r[r['units'].isin(['one', 'two', 'three', 'four', 'five'])].iloc[0]
    blank = r[r['units'] == ''].iloc[0]
    return slash, name, word, blank, clean


# ------------------------------------------------------------------ session 16
@fig('da_hero_clean_export')
def da_hero_clean_export(w, h, **_):
    s = Scene(w, h)
    slash, name, word, blank, clean = _messy_samples()
    cols = ['sale_id', 'sale_date', 'product', 'units']
    cw = [0.85, 1.45, 1.85, 0.85]
    left = [cols]
    for r in (slash, name, word, blank):
        left.append([str(r['sale_id']), r['sale_date'], "'" + r['product'] + "'", r['units'] if r['units'] != '' else '(blank)'])
    s.text(0.1, h - 0.4, 'the raw export', size=20, weight='bold', ha='left')
    hl = {(1, 1): GOLD, (2, 2): GOLD, (3, 3): GOLD, (4, 3): GOLD}
    s.table(0.1, h - 0.7, cw, 0.62, left, size=16, hl_cells=hl, align=['center', 'center', 'left', 'center'])
    s.arrow(5.25, h - 2.2, 6.2, h - 2.2, color=RED, lw=3)
    s.text(5.72, h - 1.75, 'pipeline', size=19, weight='bold', color=RED)
    rights = [cols]
    for r in (slash, name, word, blank):
        c = clean[clean['sale_id'].astype(str) == str(r['sale_id'])]
        if len(c):
            c = c.iloc[0]
            rights.append([str(c['sale_id']), str(c['sale_date'].date()), str(c['product']), str(int(c['units']))])
        else:
            rights.append([str(r['sale_id']), 'left out', '', ''])
    s.text(6.35, h - 0.4, 'the clean table', size=20, weight='bold', ha='left')
    s.table(6.35, h - 0.7, [0.85, 1.45, 1.85, 0.85], 0.62, rights, size=16, align=['center', 'center', 'left', 'center'], hl_cells={(1, 1): GOLD, (2, 2): GOLD, (3, 3): GOLD, (4, 1): '#F2C9C9'})
    s.text(0.1, 0.55, 'gold: a value the pipeline fixes.  Red: a row that cannot be repaired, so it is left out and counted.', size=17, ha='left', color=BODY)
    return s


@fig('da_date_formats')
def da_date_formats(w, h, **_):
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
    s.table(0.2, h - 0.35, [1.75, 1.75, 1.75, 1.75], 0.78, data, size=17, hl_cells=hl, header_weight='bold')
    s.text(0.2, h - 3.7, 'NaT means: this format does not fit, no date made.', size=18, ha='left', color=BODY)
    s.text(0.2, h - 4.2, 'iso.fillna(slash) keeps whichever format fitted.', size=18, ha='left', mono=True, weight='bold')
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
    s.table(0.15, h - 0.4, [2.35, 2.75, 2.35], 0.66, rows, size=17, align=['left', 'left', 'left'], hl_cells={(i, 2): GOLD for i in range(1, 5)})
    s.text(0.15, 0.7, 'One product, many spellings. The lookup gives each one the single', size=18, ha='left', color=BODY)
    s.text(0.15, 0.3, 'official name, so groups and totals count it once.', size=18, ha='left', color=BODY)
    return s


@fig('da_units_fix')
def da_units_fix(w, h, **_):
    s = Scene(w, h)
    r = raw()
    words_n = int(r.drop_duplicates()['units'].isin(['one', 'two', 'three', 'four', 'five']).sum())
    blank_n = int((r.drop_duplicates()['units'] == '').sum())
    w1 = r[r['units'].isin(['one', 'two', 'three', 'four', 'five'])].iloc[0]
    n1 = r[~r['units'].isin(['one', 'two', 'three', 'four', 'five', ''])].iloc[0]
    b1 = r[r['units'] == ''].iloc[0]
    rows = [['in the file', 'after\nto_numeric', 'what happens'],
            [repr(w1['units']).strip("'"), str(int({'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}[w1['units']])), 'a word becomes a number'],
            [n1['units'], str(int(n1['units'])), 'text that is a number stays'],
            ['(blank)', 'NaN', 'cannot be repaired: left out']]
    hl = {(1, 1): GOLD, (2, 1): GOLD, (3, 1): '#F2C9C9', (3, 2): '#F2C9C9'}
    s.table(0.15, h - 0.4, [1.8, 2.5, 3.1], 0.75, rows, size=17, hl_cells=hl, align=['center', 'center', 'left'])
    s.text(0.15, 0.95, f'{words_n} rows have a word. {blank_n} rows are blank.', size=20, weight='bold', ha='left')
    s.text(0.15, 0.45, 'A blank is not zero and not the mean. Nobody knows the units.', size=18, ha='left', color=BODY)
    return s


@fig('da_pipeline')
def da_pipeline(w, h, **_):
    s = Scene(w, h)
    clean, excluded, steps = clean_pipeline()
    labels = ['the raw\nfile', 'drop\nrepeats', 'parse\ndates', 'fix\nnames', 'words to\nnumbers', 'leave out\nblanks']
    n = len(steps)
    gap = 0.3
    bw = (w - 0.2 - gap * (n - 1)) / n
    prev = None
    for i, ((lab, cnt), name) in enumerate(zip(steps, labels)):
        x = 0.1 + i * (bw + gap)
        changed = prev is not None and cnt != prev
        s.box(x, h - 3.0, bw, 1.8, '', fill=GOLD if i == n - 1 else PAPER, lw=1.8, r=0.05)
        s.text(x + bw / 2, h - 1.65, name, size=17, weight='bold')
        s.text(x + bw / 2, h - 2.5, f'{cnt:,}', size=24, weight='bold')
        if changed:
            s.text(x + bw / 2, h - 3.45, f'{cnt - prev:+,} rows'.replace('-', '−'), size=19, weight='bold', color=RED)
        else:
            s.text(x + bw / 2, h - 3.45, 'same rows' if i else '', size=16, color=MUTE)
        if i < n - 1:
            s.arrow(x + bw + 0.03, h - 2.1, x + bw + gap - 0.03, h - 2.1, color=RED, lw=2.2, head=13)
        prev = cnt
    s.text(0.1, h - 0.4, 'The same steps, in the same order, every time', size=22, weight='bold', ha='left')
    s.text(0.1, 0.5, f'{len(excluded)} rows left out for blank units, counted and reported.', size=19, ha='left', color=BODY)
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
    s.rect(x0, h - 1.6, true_total * sc, 0.7, fill=GREY, edge=INK, lw=1.8)
    s.text(x0 + true_total * sc / 2, h - 1.25, money(true_total), size=22, weight='bold', color=PAPER)
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
    s.box(0.2, h - 1.8, 1.7, 1.0, f'raw\n{steps[0][1]:,} rows', size=17, lw=1.8, r=0.05, mono=True)
    s.arrow(1.95, h - 1.3, 2.5, h - 1.3, color=RED, lw=2.4)
    s.box(2.55, 1.3, 3.4, h - 1.4, '', fill=INK, edge=INK, r=0.08)
    lines = ['def clean_sales(raw):', '  drop repeats', '  parse both date formats', '  fix the names', '  words to numbers', '  split off the blanks', '  return clean, excluded']
    for i, l in enumerate(lines):
        s.text(2.7, h - 0.35 - i * 0.5, l, size=14, mono=True, color=PAPER, ha='left', weight='bold' if i in (0, 6) else 'normal')
    s.arrow(6.0, h - 1.0, 6.5, h - 1.0, color=RED, lw=2.4)
    s.box(6.55, h - 1.5, 1.05, 0.9, f'clean\n{len(clean):,}', size=14, fill=GOLD, lw=1.8, r=0.05, mono=True)
    s.arrow(6.0, h - 3.0, 6.5, h - 3.0, color=RED, lw=2.4)
    s.box(6.55, h - 3.5, 1.05, 0.9, f'excluded\n{len(excluded)}', size=13, fill=PAPER, lw=1.8, r=0.05, mono=True, edge=RED)
    s.text(0.2, 0.9, f'assert len(clean) == {len(clean):,}', size=16, mono=True, ha='left', weight='bold')
    s.text(0.2, 0.4, 'a check that stops the notebook when the steps change a count', size=16, ha='left', color=BODY)
    return s


# ------------------------------------------------------------------ session 17
@fig('da_hero_merge')
def da_hero_merge(w, h, **_):
    s = Scene(w, h)
    su = sales().head(5)
    pr = products()
    s.text(0.2, h - 0.4, 'sales', size=22, weight='bold', ha='left')
    srows = [['sale_id', 'product_id', 'line_value']] + [[str(r.sale_id), str(r.product_id), money(r.line_value)] for r in su.itertuples()]
    s.table(0.2, h - 0.7, [1.2, 1.6, 1.7], 0.46, srows, size=17)
    ids = list(dict.fromkeys(su['product_id']))
    prow = [['product_id', 'category']] + [[str(i), pr.loc[pr['product_id'] == i, 'category'].iloc[0]] for i in ids]
    s.text(8.0, h - 0.4, 'products', size=22, weight='bold', ha='left')
    s.table(8.0, h - 0.7, [1.6, 2.2], 0.46, prow, size=17)
    sx = 0.2 + 1.2 + 0.8
    sw = 1.6
    for k, r in enumerate(su.itertuples()):
        y1 = h - 0.7 - (k + 1.5) * 0.46
        j = ids.index(r.product_id)
        y2 = h - 0.7 - (j + 1.5) * 0.46
        s.line(0.2 + 4.5, y1, 8.0, y2, color=RED, lw=2.0, z=3)
    s.text(w / 2 - 0.2, 0.85, 'The key: product_id is in both tables.', size=21, weight='bold')
    s.text(w / 2 - 0.2, 0.35, 'A merge follows each red line and copies the category onto the sale.', size=19, color=BODY)
    return s


@fig('da_merge_result')
def da_merge_result(w, h, **_):
    s = Scene(w, h)
    su = sales()
    pr = products()
    m = su.merge(pr[['product_id', 'category']], on='product_id', how='left')
    d = m.head(5)
    rows = [['sale_id', 'product_id', 'line_value', 'category']] + [[str(r.sale_id), str(r.product_id), money(r.line_value), r.category] for r in d.itertuples()]
    s.table(0.15, h - 0.3, [0.95, 1.25, 1.4, 1.5], 0.5, rows, size=16, hl_cols=(3,))
    s.text(0.15, 1.1, f'rows before the merge: {len(su):,}', size=19, ha='left', weight='bold')
    s.text(0.15, 0.55, f'rows after the merge:  {len(m):,}', size=19, ha='left', weight='bold')
    s.icon('check', 5.0, 0.8, 0.7)
    s.text(5.5, 0.8, 'nothing lost,\nnothing copied', size=17, ha='left', color=BODY)
    return s


@fig('da_unique_key')
def da_unique_key(w, h, **_):
    s = Scene(w, h)
    pr = products().iloc[3:9]
    pp = practice()
    pp = pp[pp['product_id'].between(4, 9) | pp.index.isin([15])].copy()
    s.text(0.3, h - 0.35, 'products: each id once', size=19, weight='bold', ha='left')
    s.table(0.3, h - 0.6, [1.1, 1.6], 0.46, [['product_id', 'name']] + [[str(r.product_id), r.name] for r in pr.itertuples()], size=15, align=['center', 'left'])
    s.text(0.3, 0.85, 'is_unique  →  True', size=22, weight='bold', ha='left', mono=True)
    s.line(3.85, 0.4, 3.85, h - 0.3, color=HAIR, lw=1.2)
    s.text(4.1, h - 0.35, 'practice copy: Juice twice', size=19, weight='bold', color=RED, ha='left')
    sub = practice()
    sub = sub[sub['product_id'].between(5, 8)].reset_index(drop=True)
    rows = [['product_id', 'name']] + [[str(r.product_id), r.name] for r in sub.itertuples()]
    hl = {(i + 1, c): '#F2C9C9' for i, r in enumerate(sub.itertuples()) if r.product_id == 6 for c in (0, 1)}
    s.table(4.1, h - 0.6, [1.1, 1.7], 0.46, rows, size=15, hl_cells=hl, align=['center', 'left'])
    s.text(4.1, 0.85, 'is_unique  →  False', size=22, weight='bold', ha='left', mono=True, color=RED)
    s.text(w / 2, 0.3, 'A key must be unique in the table it looks up.', size=18, color=BODY)
    return s


@fig('da_fan_out')
def da_fan_out(w, h, **_):
    s = Scene(w, h)
    su = sales()
    pr = practice()
    sale = su[su['product_id'] == 6].iloc[0]
    n0, n1 = len(su), len(su.merge(pr[['product_id', 'category']], on='product_id', how='left'))
    t0 = int(su['line_value'].sum())
    t1 = int(su.merge(pr[['product_id', 'category']], on='product_id', how='left')['line_value'].sum())
    s.text(0.2, h - 0.35, 'one sale', size=18, weight='bold', ha='left')
    s.table(0.2, h - 0.5, [0.8, 0.9], 0.46, [['sale', 'id'], [str(sale['sale_id']), '6']], size=16)
    s.arrow(2.05, h - 0.95, 2.7, h - 0.95, color=RED, lw=2.4)
    s.text(2.8, h - 0.35, 'two Juice rows', size=18, weight='bold', ha='left')
    s.table(2.8, h - 0.5, [0.8, 1.5], 0.46, [['id', 'category'], ['6', 'Drinks'], ['6', 'Drinks']], size=16, hl_cells={(1, 0): '#F2C9C9', (2, 0): '#F2C9C9', (1, 1): '#F2C9C9', (2, 1): '#F2C9C9'})
    s.arrow(5.15, h - 1.15, 5.8, h - 1.15, color=RED, lw=2.4)
    s.text(5.9, h - 0.35, 'sale, copied', size=18, weight='bold', ha='left')
    s.table(5.9, h - 0.5, [0.65, 0.6], 0.46, [['sale', 'id'], [str(sale['sale_id']), '6'], [str(sale['sale_id']), '6']], size=15, hl_cells={(1, 0): '#F2C9C9', (2, 0): '#F2C9C9'})
    s.line(0.2, h - 2.2, w - 0.2, h - 2.2, color=HAIR, lw=1.2)
    s.text(0.3, h - 2.7, 'rows', size=20, weight='bold', ha='left')
    s.box(1.4, h - 3.0, 1.7, 0.6, f'{n0:,}', size=22, r=0.05)
    s.arrow(3.2, h - 2.7, 3.9, h - 2.7, color=RED, lw=2.4)
    s.box(4.0, h - 3.0, 1.7, 0.6, f'{n1:,}', size=22, r=0.05, edge=RED, lw=2.4, color=RED, weight='bold')
    s.text(5.85, h - 2.7, f'+{n1 - n0}', size=20, weight='bold', color=RED, ha='left')
    s.text(0.3, h - 3.65, 'revenue', size=20, weight='bold', ha='left')
    s.box(1.4, h - 3.95, 1.9, 0.6, money(t0), size=20, r=0.05)
    s.arrow(3.4, h - 3.65, 4.0, h - 3.65, color=RED, lw=2.4)
    s.box(4.1, h - 3.95, 1.9, 0.6, money(t1), size=20, r=0.05, edge=RED, lw=2.4, color=RED, weight='bold')
    s.text(6.15, h - 3.65, f'+{money(t1 - t0)}', size=18, weight='bold', color=RED, ha='left')
    s.text(0.3, 0.35, 'No error appeared. Only the row count and the total show it.', size=17, color=BODY, ha='left')
    return s


@fig('da_validate_stop')
def da_validate_stop(w, h, **_):
    s = Scene(w, h)
    s.code(0.3, h - 0.3, ['sales.merge(practice[["product_id", "category"]],', '            on="product_id",', '            validate="many_to_one")'], size=14, line_h=0.34, w=7.0)
    s.arrow(w / 2, h - 1.7, w / 2, h - 2.45, color=RED, lw=2.6)
    s.box(0.3, h - 4.3, w - 0.6, 1.7, '', fill=PAPER, edge=RED, lw=3, r=0.06)
    s.text(0.5, h - 2.95, 'MergeError', size=24, weight='bold', color=RED, ha='left', mono=True)
    s.text(0.5, h - 3.5, 'Merge keys are not unique in right dataset;\nnot a many-to-one merge', size=16, mono=True, ha='left')
    s.text(w / 2, 0.45, 'validate turns a silent wrong total into a loud stop.', size=19, weight='bold')
    return s


@fig('da_category_totals')
def da_category_totals(w, h, **_):
    f, ax = chart(w, h)
    m = sales().merge(products()[['product_id', 'category']], on='product_id', how='left')
    d = m.groupby('category')['line_value'].sum().sort_values()
    colors = [GOLD if v == d.max() else PAPER for v in d.values]
    ax.barh(d.index, d.values, color=colors, edgecolor=INK, linewidth=1.8, height=0.6)
    for i, v in enumerate(d.values):
        ax.text(v + d.max() * 0.015, i, f'{int(v):,}', va='center', fontsize=18, fontweight='bold')
    ax.set_xlim(0, d.max() * 1.3)
    ax.set_xlabel('Revenue (UGX)')
    fmt_axis_money(ax, 'x')
    ax.set_title(f'Four categories add to {int(d.sum()):,}', loc='left', fontsize=18)
    return Chart(f)


@fig('da_rowcount_check')
def da_rowcount_check(w, h, **_):
    s = Scene(w, h)
    su = sales()
    pr = products()
    m = su.merge(pr[['product_id', 'category']], on='product_id', how='left', validate='many_to_one')
    items = [('is the key unique?', 'True'), ('rows before the merge', f'{len(su):,}'), ('rows after the merge', f'{len(m):,}'),
             ('category totals add to', money(m['line_value'].sum()))]
    for i, (lab, val) in enumerate(items):
        y = h - 0.7 - i * 0.95
        s.text(0.3, y, lab, size=21, ha='left')
        s.box(4.2, y - 0.32, 2.4, 0.64, val, size=21, weight='bold', fill=GOLD if i in (1, 2) else PAPER, r=0.05)
        s.icon('check', 7.1, y, 0.6)
    s.text(w / 2, 0.22, 'Four numbers that prove a merge changed nothing it should not.', size=17, color=BODY)
    return s


# ------------------------------------------------------------------ session 18
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
    steps_ = [('Clean', f'{len(clean):,}', 'rows kept'), ('Merge', f'{len(m):,}', 'rows, same count'), ('Total', money(by.sum()), 'by category'), ('Compare', money(true_total), 'the true total'),
              ('Name it', money(true_total - got), 'the residual')]
    _flow(s, w, h - 2.75, steps_, bh=1.8, size=20)
    s.text(0.1, h - 0.4, 'Checkpoint two: clean, merge, total, compare, name the gap', size=22, weight='bold', ha='left')
    s.text(0.1, 1.15, f'Finding: {by.index[0]} earns the most, {money(by.iloc[0])} in the cleaned data.', size=20, ha='left')
    s.text(0.1, 0.55, f'Limit: {len(excluded)} sales with blank units cannot be recovered, so the totals fall short by {money(true_total - got)}.', size=20, ha='left', color=BODY)
    return s


@fig('da_cp2_checks')
def da_cp2_checks(w, h, **_):
    s = Scene(w, h)
    clean, excluded, steps, m, by, true_total = _cp2_numbers()
    got = int(clean['line_value'].sum())
    items = [f'rows kept {len(clean):,}, left out {len(excluded)}', 'product_id is unique before the merge', f'row count after the merge: {len(m):,}, unchanged',
             f'category totals add to {money(by.sum())}', f'residual named: {money(true_total - got)}']
    for i, t in enumerate(items):
        y = h - 0.6 - i * 0.88
        s.icon('check', 0.55, y, 0.62)
        s.text(1.05, y, t, size=20, ha='left')
    s.text(0.3, 0.3, 'A checkpoint is the checks that you can show.', size=18, color=BODY, ha='left')
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
    for i, c in enumerate(cats):
        ax.text(i, truth[c] * 1.03, f'−{int(truth[c] - by[c]):,}', ha='center', fontsize=16, fontweight='bold', color=RED)
    ax.set_ylim(0, truth.max() * 1.18)
    ax.set_ylabel('Revenue (UGX)')
    fmt_axis_money(ax)
    ax.legend(fontsize=15, loc='upper right')
    return Chart(f)
