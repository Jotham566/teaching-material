"""DA figures, part B: sessions 10 to 12 (cleaning, charts, checkpoint one)."""
import numpy as np
import pandas as pd

from figs_da_util import (SUN, file_shape, Scene, fig, Chart, chart, shop, sales, products, daily, raw, money, fmt_axis_money, INK, BODY, MUTE, GREY, HAIR,
                          PAPER, RED, GOLD, BRANCH)
import figkit


# ------------------------------------------------------------------ session 10
def _counts():
    r = raw()
    dup = int(r.duplicated().sum())
    dd = r.drop_duplicates()
    blank = int((dd['units'] == '').sum())
    slash = int(dd['sale_date'].str.contains('/').sum())
    return len(r), dup, len(dd), blank, slash


@fig('da_hero_cleaning')
def da_hero_cleaning(w, h, **_):
    s = Scene(w, h)
    n, dup, kept, blank, slash = _counts()
    y = h / 2 + 0.2
    bw, bh = 3.2, 2.5
    xs = [0.3, 4.35, 8.4]
    titles = ['The raw file', 'A copy to work on', 'The cleaned table']
    sub = [f'{n:,} rows', f'{n:,} rows, then {dup} repeats removed', f'{kept:,} rows']
    for i, x in enumerate(xs):
        s.box(x, y - bh / 2, bw, bh, '', fill=PAPER, lw=2.0 if i != 0 else 2.8, edge=INK if i != 1 else INK, r=0.06)
        s.text(x + bw / 2, y + 0.75, titles[i], size=22, weight='bold')
    s.icon('folder', xs[0] + bw / 2, y + 0.0, 0.9)
    s.icon('notebook', xs[1] + bw / 2, y + 0.0, 0.9)
    s.icon('check', xs[2] + bw / 2, y + 0.0, 0.8)
    s.text(xs[0] + bw / 2, y - 0.7, sub[0], size=19, color=BODY)
    s.text(xs[1] + bw / 2, y - 0.7, f'{n:,} rows', size=19, color=BODY)
    s.text(xs[1] + bw / 2, y - 1.02, f'{dup} repeats removed', size=17, color=MUTE)
    s.text(xs[2] + bw / 2, y - 0.7, sub[2], size=19, color=BODY)
    for a in (xs[0] + bw, xs[1] + bw):
        s.arrow(a + 0.1, y, a + 0.75, y, color=RED, lw=2.6)
    s.text(xs[0] + bw + 0.43, y + 0.4, 'copy', size=17, color=RED, weight='bold')
    s.text(xs[1] + bw + 0.43, y + 0.4, 'clean', size=17, color=RED, weight='bold')
    s.text(xs[0] + bw / 2, y - 1.55, 'never changed', size=18, color=RED, weight='bold')
    s.text(w / 2, 0.35, 'Every change is made on the copy and written in a log.', size=20, color=BODY)
    return s


@fig('da_raw_copy')
def da_raw_copy(w, h, **_):
    s = Scene(w, h)
    n, dup, kept, blank, slash = _counts()
    s.box(0.2, h - 1.35, 3.3, 1.0, 'sunrise_sales_raw.csv', size=15, fill=PAPER, lw=2.8, mono=True)
    s.text(1.85, h - 1.65, 'the file on disk: untouched', size=17, color=RED, weight='bold')
    s.arrow(3.6, h - 0.85, 4.2, h - 0.85, color=INK, lw=2.4)
    s.box(4.3, h - 1.35, 3.2, 1.0, f'raw_sales\n{n:,} rows', size=19, fill=PAPER, lw=1.6, mono=True)
    s.arrow(5.9, h - 1.45, 5.9, h - 2.55, color=RED, lw=2.4)
    s.text(5.75, h - 2.0, '.drop_duplicates()', size=16, color=RED, weight='bold', ha='right', mono=True)
    s.box(4.3, h - 3.65, 3.2, 1.0, f'deduped\n{kept:,} rows', size=19, fill=GOLD, lw=1.8, mono=True, weight='bold')
    s.text(5.9, h - 3.95, 'the copy we work on', size=17, color=BODY)
    s.text(0.2, h - 2.8, 'Rule: the raw file is the evidence.', size=19, weight='bold', ha='left')
    s.text(0.2, h - 3.3, 'We never save over it.', size=19, ha='left')
    s.text(0.2, h - 3.8, 'Changes go on the copy.', size=19, ha='left')
    return s


@fig('da_missing_dup')
def da_missing_dup(w, h, **_):
    s = Scene(w, h)
    rows = [['id', 'price'], ['1', '1000'], ['2', ''], ['2', ''], ['3', '3000']]
    cw = [1.0, 1.5]
    x0, y_top, rh = 0.35, h - 0.55, 0.42
    s.text(x0, h - 0.25, 'raw', size=20, weight='bold', ha='left', mono=True)
    s.table(x0, y_top, cw, rh, rows, size=18, hl_cells={(2, 1): GOLD, (3, 1): GOLD})
    s.rect(x0, y_top - 4 * rh, sum(cw), rh * 2, fill='none', edge=RED, lw=3, z=5)
    s.text(x0 + sum(cw) + 0.25, y_top - 2.2 * rh, 'the same row twice:\na duplicate', size=18, color=RED, weight='bold', ha='left')
    s.text(x0 + sum(cw) + 0.25, y_top - 4.0 * rh - 0.1, 'gold cells have no\nprice: missing', size=18, ha='left')
    s.arrow(x0 + 0.5, y_top - 5 * rh - 0.08, x0 + 0.5, y_top - 5 * rh - 0.5, color=RED, lw=2.4)
    s.text(x0 + 0.75, y_top - 5 * rh - 0.29, 'drop_duplicates()', size=16, color=RED, weight='bold', mono=True, ha='left')
    rows2 = [['id', 'price'], ['1', '1000'], ['2', ''], ['3', '3000']]
    s.table(x0, y_top - 5 * rh - 0.6, cw, 0.34, rows2, size=16, hl_cells={(2, 1): GOLD})
    s.text(x0 + sum(cw) + 0.25, y_top - 5 * rh - 1.25, '3 rows stay. One price\nis still missing.', size=18, ha='left')
    return s


@fig('da_raw_counts')
def da_raw_counts(w, h, **_):
    s = Scene(w, h)
    n, dup, kept, blank, slash = _counts()
    y = h - 1.7
    boxes = [(0.2, 2.6, f'{n:,}', 'rows in the raw file', PAPER), (3.7, 2.6, f'−{dup}', 'exact repeats', PAPER), (7.2, 2.6, f'{kept:,}', 'rows left: the clean file count', GOLD)]
    for x, bw, big, small, fill in boxes:
        s.box(x, y, bw, 1.1, big, size=34, fill=fill, weight='bold', r=0.05, lw=2.0)
        s.text(x + bw / 2, y - 0.38, small, size=17, color=BODY)
    s.text(3.2, y + 0.55, '→', size=30, weight='bold', color=RED)
    s.text(6.7, y + 0.55, '=', size=30, weight='bold', color=RED)
    s.line(0.2, 1.8, w - 0.2, 1.8, color=HAIR, lw=1.2)
    s.text(0.2, 1.4, 'More problems still sit in those rows', size=19, weight='bold', ha='left')
    bw3 = (w - 0.4 - 0.5) / 3
    for k, tx in enumerate([f'{blank} blank units', f'{slash} dates with slashes', '12 units in words']):
        s.box(0.2 + k * (bw3 + 0.25), 0.2, bw3, 0.85, tx, size=20, fill=PAPER, edge=RED, lw=2.4, color=INK)
    return s


@fig('da_cleaning_log')
def da_cleaning_log(w, h, **_):
    s = Scene(w, h)
    n, dup, kept, blank, slash = _counts()
    rows = [['problem', 'rows'], ['duplicate rows', str(dup)], ['blank units', str(blank)], ['dates with slashes', str(slash)]]
    s.text(0.3, h - 0.3, 'cleaning_log.csv', size=19, weight='bold', ha='left', mono=True)
    s.table(0.3, h - 0.6, [3.1, 1.2], 0.5, rows, size=19, align=['left', 'center'])
    s.text(0.3, h - 2.9, 'Each problem, how many rows, what we did.', size=18, color=BODY, ha='left')
    s.text(0.3, h - 3.35, 'to_csv(..., index=False)', size=18, mono=True, weight='bold', ha='left')
    s.text(0.3, h - 3.75, 'without index=False', size=15, color=RED, ha='left')
    s.table(0.3, h - 3.9, [0.6, 1.3], 0.28, [['', 'rows'], ['0', '25'], ['1', '40']], size=14, hl_cells={(0, 0): '#EEEEEE', (1, 0): '#F2C9C9', (2, 0): '#F2C9C9'})
    s.text(3.4, h - 3.75, 'with index=False', size=15, ha='left')
    s.table(3.4, h - 3.9, [1.3], 0.28, [['rows'], ['25'], ['40']], size=14, hl_cells={(1, 0): GOLD, (2, 0): GOLD})
    s.text(5.0, h - 4.3, 'no extra\nrow-number\ncolumn', size=15, ha='left', color=BODY)
    return s


@fig('da_zero_vs_missing')
def da_zero_vs_missing(w, h, **_):
    s = Scene(w, h)
    s.text(w / 4, h - 0.4, 'Left blank', size=22, weight='bold')
    s.text(3 * w / 4, h - 0.4, 'Filled with 0', size=22, weight='bold', color=RED)
    for k, (cx, third, col) in enumerate([(w / 4, '', INK), (3 * w / 4, '0', RED)]):
        rows = [['item', 'price'], ['A', '1000'], ['B', third], ['C', '3000']]
        s.table(cx - 1.1, h - 0.75, [0.8, 1.4], 0.5, rows, size=20, hl_cells={(2, 1): GOLD} if k == 0 else {(2, 1): '#F2C9C9'})
        if k == 0:
            s.text(cx, h - 3.0, 'B is unknown', size=19, weight='bold')
            s.text(cx, h - 3.55, 'mean of the known prices: 2000', size=18, color=BODY)
        else:
            s.text(cx, h - 3.0, 'B is now free', size=19, weight='bold', color=RED)
            s.text(cx, h - 3.55, f'mean becomes {int(round((1000 + 0 + 3000) / 3)):,}', size=18, color=RED)
    s.text(w / 2, 0.35, 'A made-up zero changes what the data says.', size=20, weight='bold')
    s.line(w / 2, 0.75, w / 2, h - 0.2, color=HAIR, lw=1.2)
    return s


# ------------------------------------------------------------------ session 11
@fig('da_hero_chart_choice')
def da_hero_chart_choice(w, h, **_):
    s = Scene(w, h)
    sh = shop()
    su = sales()
    dl = daily()
    cw = w / 4 - 0.2
    kinds = [('Which is\nbigger?', 'bar chart'), ('How does it\nchange?', 'line chart'), ('How are values\nspread out?', 'histogram'), ('Do two things\ngo together?', 'scatter plot')]
    for i, (q, name) in enumerate(kinds):
        x = 0.1 + i * (cw + 0.2)
        s.box(x, 0.2, cw, h - 0.4, '', fill=PAPER, lw=1.8, r=0.06)
        s.text(x + cw / 2, h - 0.8, q, size=19, weight='bold')
        s.text(x + cw / 2, 0.75, name, size=22, weight='bold', color=RED)
        px, py, pw, ph = x + 0.3, 1.25, cw - 0.6, 2.05
        s.line(px, py, px + pw, py, color=INK, lw=1.6)
        s.line(px, py, px, py + ph, color=INK, lw=1.6)
        if i == 0:
            d = sh.groupby('item')['revenue_ugx'].sum().reindex(['Book', 'Pen', 'Juice'])
            for k, v in enumerate(d.values):
                s.rect(px + 0.12 + k * pw / 3, py, pw / 3 - 0.2, ph * 0.95 * v / d.max(), fill=GOLD if v == d.max() else PAPER, edge=INK, lw=1.6)
        elif i == 1:
            d = sh.groupby('date')['revenue_ugx'].sum().values
            xs = px + np.linspace(0.05, pw - 0.05, len(d))
            ys = py + 0.1 + (ph - 0.25) * d / d.max()
            s.ax.plot(xs, ys, color=INK, lw=2.4, zorder=4)
        elif i == 2:
            v = su['line_value']
            counts, _e = np.histogram(v, bins=np.arange(0, 12001, 1000))
            for k, c in enumerate(counts):
                s.rect(px + 0.05 + k * (pw - 0.1) / len(counts), py, (pw - 0.1) / len(counts), ph * 0.95 * c / counts.max(), fill=GREY, edge=PAPER, lw=0.8)
        else:
            d = dl.iloc[::2]
            xs = px + 0.1 + (pw - 0.2) * (d['customers_counted'] / d['customers_counted'].max())
            ys = py + 0.1 + (ph - 0.2) * (d['revenue_ugx'] / d['revenue_ugx'].max())
            s.ax.scatter(xs, ys, s=16, color=INK, zorder=4)
    return s


@fig('da_chart_anatomy')
def da_chart_anatomy(w, h, **_):
    figkit.use_style()
    import matplotlib.pyplot as plt
    f = plt.figure(figsize=(w, h))
    ax = f.add_axes([0.5, 0.22, 0.47, 0.6])
    d = shop().groupby('item')['revenue_ugx'].sum().reindex(['Book', 'Juice', 'Pen'])
    ax.bar(d.index, d.values, color=[GOLD, PAPER, PAPER], edgecolor=INK, linewidth=2)
    ax.set_ylim(0, d.max() * 1.1)
    ax.set_ylabel('Revenue (UGX)', fontsize=15)
    ax.set_title('Revenue by item', loc='left', fontsize=17)
    ax.tick_params(labelsize=14)
    fmt_axis_money(ax)
    kw = dict(fontsize=16, color=RED, fontweight='bold', va='center', ha='left', textcoords='figure fraction', annotation_clip=False,
              arrowprops=dict(arrowstyle='-|>', color=RED, lw=1.8, shrinkA=3, shrinkB=2))
    ax.annotate('title: says what\nis shown', xy=(0.0, 1.05), xycoords='axes fraction', xytext=(0.02, 0.9), **kw)
    ax.annotate('axis label: the quantity\nand its unit', xy=(-0.27, 0.5), xycoords='axes fraction', xytext=(0.02, 0.55), **kw)
    ax.annotate('the axis starts at zero', xy=(0.0, 0.0), xycoords='axes fraction', xytext=(0.02, 0.27), **kw)
    ax.annotate('one bar for each category', xy=(1.0, d['Juice'] * 0.2), xycoords='data', xytext=(0.5, 0.07), **kw)
    return Chart(f)


@fig('da_axis_honesty')
def da_axis_honesty(w, h, kind='zero', **_):
    f, ax = chart(w, h)
    d = shop().groupby('item')['revenue_ugx'].sum().reindex(['Book', 'Juice', 'Pen'])
    ax.bar(d.index, d.values, color=[GOLD, PAPER, PAPER], edgecolor=INK, linewidth=2)
    if kind == 'cut':
        ax.set_ylim(90000, 300000)
        ax.set_title('Axis starts at 90,000: misleading', loc='left', color=RED, fontsize=17)
        ax.text(2, 105000, f'Pen looks about\n1/{int(round((d["Book"] - 90000) / (d["Pen"] - 90000)))} of Book', ha='center', fontsize=15, color=RED, fontweight='bold')
    else:
        ax.set_ylim(0, 320000)
        ax.set_title('Axis starts at 0: fair', loc='left', fontsize=17)
        ax.text(2, d['Pen'] + 12000, 'Pen is about\n1/3 of Book', ha='center', fontsize=15, fontweight='bold')
    fmt_axis_money(ax)
    ax.set_ylabel('Revenue (UGX)')
    return Chart(f)


@fig('da_hist_tail')
def da_hist_tail(w, h, **_):
    f, ax = chart(w, h)
    v = sales()['line_value']
    ax.hist(v, bins=30, color=GOLD, edgecolor=INK, linewidth=0.8)
    ax.set_xlabel('Value of one sale (UGX)')
    ax.set_ylabel('Number of sales')
    fmt_axis_money(ax, 'x')
    top = ax.get_ylim()[1]
    ax.annotate('most sales are small', xy=(3000, top * 0.85), xytext=(30000, top * 0.85), fontsize=17, fontweight='bold', va='center',
                arrowprops=dict(arrowstyle='-|>', color=INK, lw=2))
    big = int((v > 20000).sum())
    ax.annotate(f'{big} sales above 20,000:\nthe long tail', xy=(50000, top * 0.03), xytext=(52000, top * 0.4), fontsize=17, fontweight='bold', color=RED,
                arrowprops=dict(arrowstyle='-|>', color=RED, lw=2))
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
    ax.text(0.98, 0.06, f'{len(d)} dots: more customers\nusually bring more money', transform=ax.transAxes, fontsize=16, fontweight='bold', va='bottom', ha='right')
    return Chart(f)


@fig('da_line_dates')
def da_line_dates(w, h, **_):
    f, ax = chart(w, h)
    d = shop().groupby('date')['revenue_ugx'].sum()
    ax.plot(range(len(d)), d.values, color=INK, lw=3, marker='o', ms=5)
    best = int(d.values.argmax())
    ax.scatter([best], [d.values[best]], s=140, color=GOLD, edgecolor=INK, zorder=5)
    ax.annotate(f'highest: {d.index[best]}\n{int(d.values[best]):,}', xy=(best, d.values[best]), xytext=(best - 9, d.values[best] * 0.98), fontsize=16, fontweight='bold',
                arrowprops=dict(arrowstyle='-|>', color=INK, lw=2))
    ax.set_xticks(range(0, len(d), 4))
    ax.set_xticklabels([d.index[i][5:] for i in range(0, len(d), 4)])
    ax.set_xlabel('Date (month-day)')
    ax.set_ylabel('Revenue (UGX)')
    ax.set_ylim(0, d.max() * 1.15)
    fmt_axis_money(ax)
    return Chart(f)


# ------------------------------------------------------------------ session 12
def _flow(s, w, y, steps, bh=1.25, size=19):
    n = len(steps)
    gap = 0.38
    bw = (w - 0.2 - gap * (n - 1)) / n
    for i, (head, num, small) in enumerate(steps):
        x = 0.1 + i * (bw + gap)
        s.box(x, y, bw, bh, '', fill=PAPER, lw=1.8, r=0.05)
        s.text(x + bw / 2, y + bh - 0.3, head, size=size, weight='bold')
        s.text(x + bw / 2, y + bh / 2 - 0.08, num, size=size + 5, weight='bold')
        s.text(x + bw / 2, y + 0.25, small, size=15, color=MUTE)
        if i < n - 1:
            s.arrow(x + bw + 0.03, y + bh / 2, x + bw + gap - 0.03, y + bh / 2, color=RED, lw=2.4, head=14)
    return bw


@fig('da_cp1_flow')
def da_cp1_flow(w, h, **_):
    s = Scene(w, h)
    su = sales()
    rows, cols = file_shape('sales.csv')
    clean = pd.read_csv(SUN / 'sales.csv')
    miss = int(clean.isna().sum().sum())
    dups = int(clean.duplicated().sum())
    total = int(su['line_value'].sum())
    by = su.groupby('branch')['line_value'].sum().sort_values(ascending=False)
    steps = [('Load', f'{rows:,}', f'rows, {cols} columns'), ('Check', f'{miss} + {dups}', 'missing, duplicates'), ('Summarise', money(total), 'UGX revenue'),
             ('Chart', '3', 'branches compared'), ('Explain', '2 + 1', 'findings, limit')]
    _flow(s, w, h - 2.75, steps, bh=1.8, size=20)
    s.text(0.1, h - 0.4, 'Checkpoint one: five steps, a real number at each step', size=22, weight='bold', ha='left')
    s.text(0.1, 1.15, f'First finding: {by.index[0]} earns the most, {money(by.iloc[0])} of the {money(total)}.', size=20, ha='left')
    s.text(0.1, 0.55, 'Limit: the data is invented and has no costs, so it says nothing about real shops or profit.', size=20, ha='left', color=BODY)
    return s


@fig('da_notebook_layout')
def da_notebook_layout(w, h, **_):
    s = Scene(w, h)
    cells = [('text', '# Question: which shop earns the most?'), ('code', 'sales = pd.read_csv("sunrise_sales.csv")'), ('code', 'sales.isna().sum().sum()   # 0'),
             ('code', 'sales.groupby("branch")["line_value"].sum()'), ('code', 'plt.bar(by_branch.index, by_branch.values)'),
             ('text', 'Finding: Central Market earns the most. Limit: invented data.')]
    top = h - 0.25
    ch = 0.5
    s.text(0.2, top - 0.05, 'a notebook page, top to bottom', size=16, color=MUTE, ha='left', va='top')
    top -= 0.4
    for i, (kind, txt) in enumerate(cells):
        y = top - (i + 1) * (ch + 0.1) + 0.05
        if kind == 'code':
            s.box(1.15, y, w - 1.35, ch, '', fill=INK, edge=INK, r=0.04)
            s.text(1.3, y + ch / 2, txt, size=14, mono=True, ha='left', color=PAPER)
        else:
            s.box(1.15, y, w - 1.35, ch, '', fill=PAPER, edge=INK, lw=1.6, r=0.04)
            s.text(1.3, y + ch / 2, txt, size=16, ha='left')
        s.text(0.2, y + ch / 2, kind, size=16, color=RED if kind == 'code' else INK, weight='bold', ha='left')
    s.text(w / 2, 0.22, 'text cells explain, code cells calculate', size=17, color=BODY)
    return s


@fig('da_rerun_top')
def da_rerun_top(w, h, **_):
    s = Scene(w, h)
    xs = [0.25, 2.8, 5.35]
    labels = ['Restart the\nkernel', 'Run all cells\nfrom the top', 'Every number\nstill appears']
    for i, (x, lab) in enumerate(zip(xs, labels)):
        s.box(x, h - 2.1, 2.2, 1.2, lab, size=18, fill=PAPER, weight='bold', lw=2.0, r=0.05)
        if i < 2:
            s.arrow(x + 2.25, h - 1.5, x + 2.55, h - 1.5, color=RED, lw=2.4, head=14)
    s.line(0.25, h - 3.1, w - 0.25, h - 3.1, color=HAIR, lw=1.2)
    s.text(0.25, h - 3.5, 'If a cell fails, the notebook was relying on memory:', size=19, weight='bold', ha='left')
    s.text(0.25, h - 4.05, 'a value made in a cell that now runs later, or no longer exists.', size=18, color=BODY, ha='left')
    s.text(0.25, h - 4.5, 'Fix the first cell that fails, then run all again.', size=18, color=RED, weight='bold', ha='left')
    s.text(0.25, h - 0.45, 'The test of a notebook', size=22, weight='bold', ha='left')
    return s


@fig('da_finding_trace')
def da_finding_trace(w, h, **_):
    s = Scene(w, h)
    su = sales()
    by = su.groupby('branch')['line_value'].sum().sort_values(ascending=False)
    s.box(0.2, h - 1.65, w - 0.4, 1.1, '', fill=PAPER, lw=1.8, r=0.05)
    s.text(0.4, h - 0.95, 'Finding in the report', size=15, color=MUTE, ha='left')
    s.text(0.4, h - 1.35, f'{by.index[0]} earns the most: UGX {money(by.iloc[0])}.', size=21, weight='bold', ha='left')
    s.arrow(1.5, h - 1.7, 1.5, h - 2.55, color=RED, lw=2.6)
    s.text(1.7, h - 2.1, 'comes from this output', size=17, color=RED, weight='bold', ha='left')
    rows = [['branch', 'line_value']] + [[b, money(v)] for b, v in by.items()]
    s.table(0.2, h - 2.65, [2.5, 2.2], 0.5, rows, size=18, hl_cells={(1, 0): GOLD, (1, 1): GOLD})
    s.text(5.1, h - 3.4, 'No output,\nno finding.', size=20, weight='bold', ha='left', color=RED)
    return s
