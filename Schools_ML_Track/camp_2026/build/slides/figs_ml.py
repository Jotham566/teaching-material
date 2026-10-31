"""Machine Learning illustrations for sessions 7 to 24, labs F03 and F04 and the extension ML25.

Every figure is a function fn(w, h, **params) -> Scene registered with @fig('ml_...'). Numbers come from the CSV files in
camp_2026/data or from numpy computed here. scikit-learn is not imported: regression uses numpy.linalg.lstsq and splits use
numpy.random.RandomState(r).permutation, which is the shuffle train_test_split performs for an integer random_state.
"""
import math

import numpy as np
import pandas as pd

from brand import CAMP, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD
from figkit import Scene, fig, use_style, save_chart, plt, FONT

DATA = CAMP / 'data'
SPECIES = ['setosa', 'versicolor', 'virginica']


# ------------------------------------------------------------------ data helpers
_cache = {}


def shop():
    if 'shop' not in _cache:
        d = pd.read_csv(DATA / 'camp_shop.csv')
        d['revenue_ugx'] = d['units'] * d['unit_price_ugx']
        _cache['shop'] = d
    return _cache['shop']


def shop_raw():
    if 'shop_raw' not in _cache:
        _cache['shop_raw'] = pd.read_csv(DATA / 'camp_shop.csv')
    return _cache['shop_raw']


def homes():
    if 'homes' not in _cache:
        _cache['homes'] = pd.read_csv(DATA / 'synthetic_homes.csv')
    return _cache['homes']


def fares():
    if 'fares' not in _cache:
        _cache['fares'] = pd.read_csv(DATA / 'synthetic_fares.csv')
    return _cache['fares']


def split_idx(n, test_size, seed=7):
    """Indices (train, test) exactly as sklearn's train_test_split(test_size, random_state=seed) picks them."""
    n_test = int(math.ceil(test_size * n))
    n_train = int(math.floor((1 - test_size) * n))
    perm = np.random.RandomState(seed).permutation(n)
    return perm[n_test:n_test + n_train], perm[:n_test]


def three_way(n, seed=7):
    """150 rows -> (train 90, val 30, test 30) the way the lesson code splits them."""
    dev, test = split_idx(n, 0.2, seed)
    t2, v2 = split_idx(len(dev), 0.25, seed)
    return dev[t2], dev[v2], test


def ols(X, y):
    A = np.column_stack([np.ones(len(X)), X])
    beta = np.linalg.lstsq(A, y, rcond=None)[0]
    return beta


def predict(beta, X):
    return beta[0] + np.asarray(X).reshape(len(X), -1) @ beta[1:]


def mae(a, b):
    return float(np.mean(np.abs(np.asarray(a) - np.asarray(b))))


def money(v):
    return f'{v:,.0f}'


# ------------------------------------------------------------------ drawing helpers
def axes_in(s, x, y, w, h, **kw):
    """A matplotlib axes placed at (x, y, w, h) inches (bottom left origin) on a Scene, styled for slides."""
    ax = s.f.add_axes([x / s.w, y / s.h, w / s.w, h / s.h], **kw)
    ax.set_facecolor(PAPER)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    for sp in ('left', 'bottom'):
        ax.spines[sp].set_color(INK)
        ax.spines[sp].set_linewidth(1.4)
    ax.tick_params(labelsize=14, colors=INK, width=1.2)
    return ax


def data_table(s, x, ytop, df, col_w, row_h=0.42, size=16, hl_cells=None, hl_rows=(), hl_cols=(), hl_fill=GOLD, mono_cols=(), align=None, dim_rows=()):
    rows = [list(df.columns)] + [[('' if (isinstance(v, float) and np.isnan(v)) else (f'{v:,}' if isinstance(v, (int, np.integer)) and abs(v) >= 10000 else str(v))) for v in r] for r in df.astype(object).values.tolist()]
    return s.table(x, ytop, col_w, row_h, rows, size=size, hl_cells=hl_cells, hl_rows=hl_rows, hl_cols=hl_cols, hl_fill=hl_fill, mono_cols=mono_cols, align=align, dim_rows=dim_rows)


def label(s, x, y, text, size=18, color=INK, weight='normal', ha='center'):
    return s.text(x, y, text, size=size, color=color, weight=weight, ha=ha)


def flow_arrow(s, x1, y, x2, text='', size=16, color=INK, dy=0.3):
    s.arrow(x1, y, x2, y, color=color, lw=2.4, head=18)
    if text:
        s.text((x1 + x2) / 2, y + dy, text, size=size, color=color, mono=True)


def mini_row_marks(s, x, y, n, gold=(), size=0.22, gap=0.07, cols=None, edge=INK):
    """A block of small squares; gold marks the chosen ones."""
    cols = cols or n
    for i in range(n):
        cx = x + (i % cols) * (size + gap)
        cy = y - (i // cols) * (size + gap)
        s.rect(cx, cy, size, size, fill=GOLD if i in gold else PAPER, edge=edge, lw=1.1)


# ------------------------------------------------------------------ small icons (1.3 x 1.3 in) for the words slides
@fig('ml_icon')
def ml_icon(w, h, kind='grid_row', **_):
    s = Scene(w, h)
    cx, cy = w / 2, h / 2
    if kind in ('grid_row', 'grid_col', 'grid'):
        for r in range(4):
            for c in range(4):
                hl = (kind == 'grid_row' and r == 1) or (kind == 'grid_col' and c == 2)
                s.rect(0.15 + c * 0.25, h - 0.3 - r * 0.25, 0.22, 0.22, fill=GOLD if hl else PAPER, lw=1.5)
    elif kind == 'header':
        for r in range(3):
            for c in range(3):
                s.rect(0.2 + c * 0.3, h - 0.45 - r * 0.28, 0.27, 0.25, fill=INK if r == 0 else PAPER, lw=1.5)
    elif kind == 'shape':
        s.rect(0.25, 0.3, 0.8, 0.7, fill=PAPER, lw=2)
        s.text(cx, 0.65, '3 x 2', size=18, weight='bold')
    elif kind == 'csv':
        s.rect(0.25, 0.15, 0.8, 1.0, fill=PAPER, lw=2)
        for i in range(4):
            s.line(0.38, 1.0 - i * 0.2, 0.92, 1.0 - i * 0.2, color=GREY, lw=1.6)
        s.text(cx, 0.28, 'csv', size=18, weight='bold', mono=True)
    elif kind == 'level':
        for i, v in enumerate([0.5, 0.8, 1.0, 0.7]):
            s.rect(0.12 + i * 0.28, 0.2, 0.22, v * 0.8, fill=PAPER, lw=1.5)
        s.line(0.08, 0.2 + 0.75 * 0.8, 1.2, 0.2 + 0.75 * 0.8, color=RED, lw=2.4, z=4)
    elif kind == 'median':
        for i in range(5):
            s.circle(0.18 + i * 0.23, cy, 0.09, fill=GOLD if i == 2 else PAPER, lw=1.8)
        s.arrow(0.18 + 2 * 0.23, 0.2, 0.18 + 2 * 0.23, 0.45, color=INK, lw=2, head=12)
    elif kind == 'range':
        s.line(0.15, cy, 1.15, cy, lw=2.2)
        s.line(0.15, cy - 0.18, 0.15, cy + 0.18, lw=2.2)
        s.line(1.15, cy - 0.18, 1.15, cy + 0.18, lw=2.2)
        s.arrow(0.2, cy + 0.32, 1.1, cy + 0.32, color=RED, lw=2, head=12)
        s.arrow(1.1, cy + 0.32, 0.2, cy + 0.32, color=RED, lw=2, head=12)
    elif kind == 'pie':
        from matplotlib.patches import Wedge, Circle
        s.ax.add_patch(Circle((cx, cy), 0.45, fc=PAPER, ec=INK, lw=2, zorder=2))
        s.ax.add_patch(Wedge((cx, cy), 0.45, 90, 90 + 216, fc=GOLD, ec=INK, lw=2, zorder=3))
    elif kind == 'outlier':
        for i, x in enumerate([0.2, 0.32, 0.44, 0.56]):
            s.circle(x, cy, 0.07, fill=PAPER, lw=1.8)
        s.circle(1.12, cy, 0.09, fill=RED, edge=RED)
        s.line(0.1, cy - 0.25, 1.2, cy - 0.25, lw=1.6)
    elif kind == 'newcol':
        for r in range(4):
            for c in range(3):
                s.rect(0.15 + c * 0.28, h - 0.3 - r * 0.25, 0.25, 0.22, fill=GOLD if c == 2 else PAPER, lw=1.5)
    elif kind == 'copy':
        s.rect(0.2, 0.3, 0.6, 0.75, fill=PAPER, lw=2)
        s.rect(0.45, 0.15, 0.6, 0.75, fill=PAPER, lw=2, z=3)
    elif kind == 'lock':
        s.rect(cx - 0.35, 0.2, 0.7, 0.5, fill=GOLD, lw=2)
        from matplotlib.patches import Wedge
        s.ax.add_patch(Wedge((cx, 0.7), 0.26, 0, 180, width=0.07, fc=INK, ec=INK, zorder=3))
    elif kind == 'target':
        for r, f in [(0.5, PAPER), (0.34, PAPER), (0.18, GOLD)]:
            s.circle(cx, cy, r, fill=f, lw=2)
    elif kind == 'split':
        s.rect(0.1, cy - 0.2, 0.75, 0.4, fill=PAPER, lw=2)
        s.rect(0.85, cy - 0.2, 0.3, 0.4, fill=GOLD, lw=2)
    elif kind == 'flat':
        s.line(0.1, cy, 1.2, cy, color=INK, lw=2.6)
        for i, dy in enumerate([0.3, -0.25, 0.2, -0.35]):
            s.circle(0.25 + i * 0.28, cy + dy, 0.06, fill=PAPER, lw=1.8)
    elif kind == 'line':
        s.line(0.12, 0.25, 1.18, 1.05, color=INK, lw=2.6)
        for i, dy in enumerate([0.12, -0.1, 0.08, -0.06]):
            s.circle(0.25 + i * 0.27, 0.35 + i * 0.2 + dy, 0.06, fill=PAPER, lw=1.8)
    elif kind == 'tree':
        s.circle(cx, 1.0, 0.1, lw=2)
        s.circle(0.35, 0.5, 0.1, lw=2)
        s.circle(0.95, 0.5, 0.1, lw=2)
        s.line(cx, 0.92, 0.35, 0.6, lw=2)
        s.line(cx, 0.92, 0.95, 0.6, lw=2)
    elif kind == 'matrix':
        for r in range(2):
            for c in range(2):
                s.rect(0.3 + c * 0.35, 0.65 - r * 0.35, 0.32, 0.32, fill=GOLD if r == c else PAPER, lw=1.8)
    elif kind == 'die':
        s.box(0.25, 0.25, 0.8, 0.8, '', lw=2, r=0.1)
        for dx, dy in [(0.45, 0.45), (0.85, 0.85), (0.65, 0.65), (0.45, 0.85), (0.85, 0.45)]:
            s.circle(dx, dy, 0.05, fill=INK, edge=INK, z=4)
    elif kind == 'frozen':
        s.circle(cx, cy, 0.42, fill=PAPER, lw=2.2)
        s.line(cx, cy - 0.42, cx, cy + 0.42, lw=2)
        s.line(cx - 0.42, cy, cx + 0.42, cy, lw=2)
        s.line(cx - 0.3, cy - 0.3, cx + 0.3, cy + 0.3, lw=2)
        s.line(cx - 0.3, cy + 0.3, cx + 0.3, cy - 0.3, lw=2)
    elif kind == 'weight':
        s.poly([(0.3, 0.3), (1.0, 0.3), (0.85, 0.9), (0.45, 0.9)], fill=GOLD, lw=2)
        s.text(cx, 0.55, 'kg', size=18, weight='bold')
    elif kind == 'network':
        for x, ys in [(0.2, [0.4, 0.9]), (0.65, [0.3, 0.65, 1.0]), (1.1, [0.65])]:
            for yy in ys:
                s.circle(x, yy, 0.09, fill=PAPER, lw=1.8, z=3)
        for y1 in [0.4, 0.9]:
            for y2 in [0.3, 0.65, 1.0]:
                s.line(0.2, y1, 0.65, y2, color=GREY, lw=1.2)
        for y2 in [0.3, 0.65, 1.0]:
            s.line(0.65, y2, 1.1, 0.65, color=GREY, lw=1.2)
    elif kind == 'dots':
        for i, (dx, dy) in enumerate([(0.3, 0.4), (0.5, 0.65), (0.75, 0.6), (0.95, 0.95), (0.4, 0.8), (0.85, 0.35)]):
            s.circle(dx, dy, 0.07, fill=PAPER, lw=1.8)
    elif kind == 'scale':
        s.line(0.1, 0.5, 1.2, 0.5, lw=2.2)
        for i in range(6):
            s.line(0.1 + i * 0.22, 0.4, 0.1 + i * 0.22, 0.6, lw=1.8)
        s.circle(0.1 + 2 * 0.22, 0.5, 0.08, fill=GOLD, lw=1.6, z=4)
    elif kind == 'bars_hist':
        for i, v in enumerate([0.3, 0.6, 0.85, 0.5, 0.25]):
            s.rect(0.1 + i * 0.22, 0.2, 0.2, v, fill=PAPER, lw=1.6)
    elif kind == 'box':
        s.rect(0.35, 0.4, 0.5, 0.45, fill=PAPER, lw=2)
        s.line(0.35, 0.62, 0.85, 0.62, lw=2.6)
        s.line(cx, 0.85, cx, 1.1, lw=2)
        s.line(cx, 0.4, cx, 0.15, lw=2)
    elif kind == 'label':
        s.text(cx, cy + 0.3, 'Revenue', size=17, weight='bold')
        s.line(0.2, cy + 0.05, 1.1, cy + 0.05, lw=1.6)
        s.rect(0.3, 0.2, 0.2, 0.25, fill=PAPER, lw=1.6)
        s.rect(0.6, 0.2, 0.2, 0.45, fill=GOLD, lw=1.6)
    return s


# ================================================================== SESSION 7: tables and CSV files
def sheet(imgs, cols, path):
    from PIL import Image
    cw = max(i.width for i in imgs)
    ch = max(i.height for i in imgs)
    rows = (len(imgs) + cols - 1) // cols
    sh = Image.new('RGB', (cw * cols, ch * rows), '#999999')
    for k, im in enumerate(imgs):
        sh.paste(im, ((k % cols) * cw, (k // cols) * ch))
    sh.thumbnail((2400, 2600))
    sh.save(path)


@fig('ml_csv_to_table')
def ml_csv_to_table(w, h, **_):
    s = Scene(w, h)
    raw = shop().head(3)[['sale_id', 'date', 'item', 'units', 'unit_price_ugx']]
    lines = ['sale_id,date,item,units,unit_price_ugx'] + [','.join(str(v) for v in r) for r in raw.astype(object).values.tolist()]
    top = h - 0.1
    cwid, ch = s.code(0.2, top, lines, size=15, line_h=0.3, pad=0.15, w=5.4)
    ytab_top = top - ch - 0.85
    s.arrow(2.9, top - ch - 0.05, 2.9, ytab_top + 0.05, color=RED, lw=2.4, head=18)
    s.text(3.2, top - ch - 0.42, 'pd.read_csv("camp_shop.csv")', size=16, mono=True, ha='left')
    data_table(s, 0.2, ytab_top, raw, [0.95, 1.4, 0.9, 0.9, 1.95], row_h=0.4, size=16, hl_rows=(0,), hl_fill='#EDEDED')
    s.text(0.2, ytab_top - 4 * 0.4 - 0.25, '... 57 more rows', size=16, color=MUTE, ha='left')
    ax = 7.3
    s.text(ax, top - 0.3, 'The first line of the file\nholds the headers.', size=19, ha='left')
    s.arrow(ax - 0.1, top - 0.3, 5.75, top - 0.15 - 0.15, color=INK, lw=1.8, head=14)
    s.text(ax, top - 1.5, 'Every other line is one row:\none sale.', size=19, ha='left')
    s.arrow(ax - 0.1, top - 1.45, 5.75, top - 0.15 - 0.3 * 2.5, color=INK, lw=1.8, head=14)
    s.box(ax, 0.45, 4.3, 0.8, '60 rows by 5 columns', size=24, fill=GOLD, weight='bold', r=0.05)
    s.text(ax + 2.15, 0.2, 'shape (60, 5)', size=16, mono=True, color=MUTE, va='bottom')
    return s


@fig('ml_table_anatomy')
def ml_table_anatomy(w, h, **_):
    s = Scene(w, h)
    rows = [['item', 'units'], ['Book', '2'], ['Pen', '5'], ['Book', '3']]
    x0, ytop, rh = 0.4, h - 0.6, 0.8
    s.table(x0, ytop, [1.8, 1.6], rh, rows, size=24, hl_cells={(0, 0): '#EDEDED', (0, 1): '#EDEDED'})
    s.text(4.15, ytop - 0.4, 'headers name\nthe columns', size=18, ha='left')
    s.arrow(4.05, ytop - 0.4, x0 + 3.4 + 0.05, ytop - 0.4, color=INK, lw=1.8, head=14)
    s.text(4.15, ytop - 2.0, 'one row =\none record', size=18, ha='left')
    s.arrow(4.05, ytop - 2.0, x0 + 3.4 + 0.05, ytop - 2.0, color=INK, lw=1.8, head=14)
    s.box(x0 + 1.8 + 0.06, ytop - 4 * rh + 0.06, 1.48, 3 * rh - 0.12, '', fill='none', edge=RED, lw=3.2, r=0.04, z=5)
    s.text(4.15, ytop - 3.1, 'one column =\none kind of fact', size=18, ha='left', color=RED, weight='bold')
    s.arrow(4.05, ytop - 3.1, x0 + 3.4 - 0.5, ytop - 3.1, color=RED, lw=1.8, head=14)
    s.box(0.4, 0.2, 3.4, 0.6, 'shape (3, 2)', size=20, fill=GOLD, weight='bold', r=0.05, mono=True)
    s.text(4.15, 0.4, '3 rows, 2 columns', size=18, ha='left')
    return s


@fig('ml_code_to_table')
def ml_code_to_table(w, h, **_):
    s = Scene(w, h)
    lines = ['sales = pd.DataFrame({', '    "item": ["Book", "Pen", "Book"],', '    "units": [2, 5, 3]', '})']
    top = h - 0.15
    size, lh, pad = 16, 0.34, 0.2
    cwid, ch = s.code(0.3, top, lines, size=size, line_h=lh, pad=pad, w=5.2)
    cw = size * 0.602 / 72.0
    x0 = 0.3 + pad

    def tok(line, start, length, color):
        yc = top - pad - (line + 0.5) * lh
        s.box(x0 + start * cw - 0.03, yc - lh / 2 + 0.03, length * cw + 0.06, lh - 0.06, '', fill='none', edge=color, lw=2.4, r=0.03, z=6)
    tok(1, 4, 6, GOLD)      # "item"
    tok(1, 12, 23, GOLD)    # the list of items
    tok(2, 4, 7, RED)       # "units"
    tok(2, 13, 9, RED)      # [2, 5, 3]
    rows = [['item', 'units'], ['Book', '2'], ['Pen', '5'], ['Book', '3']]
    tx, rh = 0.8, 0.45
    ytab = top - ch - 0.65
    s.table(tx, ytab, [1.6, 1.4], rh, rows, size=20, hl_cells={(0, 0): GOLD, (1, 0): GOLD, (2, 0): GOLD, (3, 0): GOLD})
    s.box(tx + 1.6 + 0.04, ytab - 4 * rh + 0.04, 1.32, 4 * rh - 0.08, '', fill='none', edge=RED, lw=3.2, r=0.03, z=6)
    s.text(4.3, ytab - 0.55, 'a name becomes\na column header', size=17, ha='left', weight='bold')
    s.text(4.3, ytab - 1.4, 'a list fills its column\nfrom top to bottom', size=17, ha='left')
    s.text(4.3, ytab - 2.0 + 0.0, 'same colour, same column', size=16, ha='left', color=MUTE)
    return s


@fig('ml_shape_grid')
def ml_shape_grid(w, h, **_):
    s = Scene(w, h)
    sets = [('camp_shop', shop_raw(), 'a sale'), ('synthetic_homes', homes(), 'a home'), ('synthetic_fares', fares(), 'a trip')]
    x = 0.45
    base = 1.35
    for name, d, what in sets:
        r, c = d.shape
        bw, bh = c * 0.4, r * 0.02
        s.rect(x, base, bw, bh, fill=PAPER, edge=INK, lw=2)
        for k in range(1, c):
            s.line(x + k * bw / c, base, x + k * bw / c, base + bh, color=HAIR, lw=1.1, z=1)
        for k in range(1, 7):
            yy = base + k * bh / 7
            s.line(x, yy, x + bw, yy, color=HAIR, lw=1.1, z=1)
        s.text(x + bw / 2, base - 0.3, f'({r}, {c})', size=22, weight='bold', mono=True)
        s.text(x + bw / 2, base - 0.75, name, size=16, color=MUTE)
        s.text(x + bw / 2, base + bh + 0.25, f'one row =\n{what}', size=16)
        x += bw + 0.45
    return s


@fig('ml_three_files')
def ml_three_files(w, h, **_):
    s = Scene(w, h)
    tbls = [(shop()[['sale_id', 'item', 'units', 'unit_price_ugx']].head(3), [0.8, 0.65, 0.7, 1.5], 'one row = one sale', '5 columns, 4 shown'),
            (homes().head(3), [0.8, 0.9, 0.75, 1.0], 'one row = one home', '4 columns'),
            (fares()[['trip_id', 'distance_km', 'raining', 'fare_ugx']].head(3), [0.75, 1.35, 0.85, 1.0], 'one row = one trip', '6 columns, 4 shown')]
    x = 0.2
    for df, cws, cap, sub in tbls:
        tw = sum(cws)
        data_table(s, x, h - 0.5, df, cws, row_h=0.42, size=15, hl_rows=(0,), hl_fill='#EDEDED')
        s.text(x + tw / 2, h - 0.5 - 4 * 0.42 - 0.5, cap, size=20, weight='bold')
        s.text(x + tw / 2, h - 0.5 - 4 * 0.42 - 1.0, sub, size=16, color=MUTE)
        x += tw + 0.3
    return s


# ================================================================== SESSION 8: select, filter, new column
ITEM_ICON = {'Book': 'book', 'Pen': 'pen', 'Juice': 'bottle'}


@fig('ml_who_earns_most')
def ml_who_earns_most(w, h, **_):
    d = shop()
    g = d.groupby('item').agg(units=('units', 'sum'), price=('unit_price_ugx', 'first'))
    s = Scene(w, h)
    order = ['Book', 'Pen', 'Juice']
    for i, it in enumerate(order):
        cx = w * (0.17 + 0.33 * i)
        s.icon(ITEM_ICON[it], cx, h - 0.85, 0.95)
        s.text(cx, h - 1.55, it, size=24, weight='bold')
        s.tag(cx - 0.95, h - 2.2, f'{g.loc[it, "price"]:,} UGX each', size=17, fill=PAPER, color=INK, h=0.42, pad=0.12)
        s.text(cx, h - 2.8, f'{g.loc[it, "units"]} units sold', size=22, weight='bold')
        s.box(cx - 1.05, 0.45, 2.1, 0.85, 'money = ?', size=24, fill=PAPER, edge=RED, lw=2.4, color=RED, weight='bold', r=0.05)
        s.arrow(cx, h - 3.15, cx, 1.4, color=INK, lw=2, head=16)
    return s


@fig('ml_select_col')
def ml_select_col(w, h, **_):
    s = Scene(w, h)
    d = shop_raw().head(5)[['sale_id', 'item', 'units']]
    data_table(s, 0.6, h - 0.15, d, [1.4, 1.5, 1.4], row_h=0.4, size=18, hl_cols=(2,))
    s.text(w / 2, 0.75, 'shop["units"]', size=20, mono=True, weight='bold')
    s.text(w / 2, 0.3, 'reads one column', size=17, color=MUTE)
    return s


@fig('ml_filter_rows')
def ml_filter_rows(w, h, **_):
    s = Scene(w, h)
    d = shop_raw().head(5)[['item', 'units']].copy()
    d['units >= 5'] = d['units'] >= 5
    keep = [i + 1 for i, v in enumerate(d['units >= 5']) if v]
    rows = [list(d.columns)] + [[r[0], str(r[1]), str(r[2])] for r in d.astype(object).values.tolist()]
    s.table(0.3, h - 0.15, [1.3, 1.2, 2.5], 0.4, rows, size=18, hl_rows=tuple(keep))
    s.text(w / 2, 0.75, 'shop[shop["units"] >= 5]', size=19, mono=True, weight='bold')
    s.text(w / 2, 0.3, 'keeps the True rows', size=17, color=MUTE)
    return s


@fig('ml_mask_steps')
def ml_mask_steps(w, h, **_):
    s = Scene(w, h)
    d = shop_raw().head(6)
    vals = d['units'].tolist()
    mask = [v >= 5 for v in vals]
    y0, rh = h - 0.85, 0.52
    s.text(0.95, h - 0.4, 'units', size=19, weight='bold')
    s.text(3.2, h - 0.4, 'units >= 5', size=19, weight='bold', mono=True)
    s.text(6.3, h - 0.4, 'kept', size=19, weight='bold')
    for i, v in enumerate(vals):
        yy = y0 - i * rh
        s.box(0.4, yy - rh + 0.04, 1.1, rh - 0.08, str(v), size=20, r=0.03)
        s.box(2.5, yy - rh + 0.04, 1.4, rh - 0.08, str(mask[i]), size=19, fill=GOLD if mask[i] else PAPER, r=0.03, weight='bold' if mask[i] else 'normal')
    k = 0
    for i, v in enumerate(vals):
        if mask[i]:
            s.box(5.6, y0 - k * rh - rh + 0.04, 1.4, rh - 0.08, f'{v} units', size=19, fill=GOLD, r=0.03)
            s.arrow(3.95, y0 - i * rh - rh / 2 + 0.04, 5.55, y0 - k * rh - rh / 2 + 0.04, color=RED, lw=1.8, head=13)
            k += 1
    s.arrow(1.55, y0 - 3 * rh, 2.45, y0 - 3 * rh, color=INK, lw=2.2, head=16)
    s.text(0.4, 0.55, 'True keeps the row. False drops it from the new table.', size=17, ha='left', color=BODY)
    return s


@fig('ml_new_column')
def ml_new_column(w, h, **_):
    s = Scene(w, h)
    d = shop().head(5)[['item', 'units', 'unit_price_ugx', 'revenue_ugx']]
    cw = [1.25, 1.1, 1.9, 1.7]
    data_table(s, 0.2, h - 0.5, d, cw, row_h=0.55, size=18, hl_cols=(3,), hl_rows=())
    r = 3
    yc = h - 0.5 - 0.55 * (r + 0.5)
    s.box(0.2 + 1.25 + 0.04, yc - 0.27, 1.1 + 1.9 - 0.08, 0.54, '', fill='none', edge=RED, lw=3, r=0.03, z=6)
    s.text(0.2, 0.95, 'each revenue = units x unit_price_ugx, one row at a time', size=17, ha='left')
    s.box(0.2, 0.15, 3.4, 0.6, f'total revenue {int(shop().revenue_ugx.sum()):,}', size=18, fill=GOLD, weight='bold', r=0.05)
    s.text(3.8, 0.45, '= the sum of the whole new column', size=17, ha='left', color=BODY)
    return s


@fig('ml_units_vs_money')
def ml_units_vs_money(w, h, **_):
    d = shop().groupby('item').agg(units=('units', 'sum'), rev=('revenue_ugx', 'sum'))
    order = ['Book', 'Pen', 'Juice']
    s = Scene(w, h)
    for k, (col, ttl, fmt) in enumerate([('units', 'Units sold', '{:,.0f}'), ('rev', 'Money earned (UGX)', '{:,.0f}')]):
        ax = axes_in(s, 0.9 + k * 6.1, 0.6, 4.7, h - 1.7)
        vals = [d.loc[i, col] for i in order]
        top = int(np.argmax(vals))
        bars = ax.bar(order, vals, color=[GOLD if i == top else PAPER for i in range(3)], edgecolor=INK, linewidth=2, width=0.6)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + max(vals) * 0.03, fmt.format(v), ha='center', va='bottom', fontsize=17, fontweight='bold', family=FONT)
        ax.set_ylim(0, max(vals) * 1.22)
        ax.set_yticks([])
        ax.spines['left'].set_visible(False)
        ax.tick_params(axis='x', labelsize=18)
        s.text(0.9 + k * 6.1 + 2.35, h - 0.45, ttl, size=22, weight='bold')
    return s


@fig('ml_filter_copy')
def ml_filter_copy(w, h, **_):
    n = len(shop_raw())
    k = int((shop_raw().units >= 5).sum())
    s = Scene(w, h)
    s.rect(0.5, 1.2, 1.6, 3.0, fill=PAPER, lw=2.2)
    s.text(1.3, 2.7, f'{n}\nrows', size=26, weight='bold')
    s.text(1.3, 0.8, 'shop', size=19, mono=True)
    s.arrow(2.3, 2.7, 4.2, 2.7, color=RED, lw=2.6, head=18)
    s.text(3.25, 3.15, 'filter', size=19, weight='bold', color=RED)
    s.text(3.25, 2.3, 'units >= 5', size=16, mono=True)
    s.rect(4.4, 1.2 + 1.5, 1.6, 1.5, fill=GOLD, lw=2.2)
    s.text(5.2, 3.45, f'{k}\nrows', size=26, weight='bold')
    s.text(5.2, 0.8 + 1.5, 'big', size=19, mono=True)
    s.text(1.3, 4.55, 'still the same', size=17, color=MUTE)
    s.text(5.2, 4.55, 'a new, smaller table', size=17, color=MUTE)
    return s


# ================================================================== SESSION 9: mean, median, range, percentiles, proportions
@fig('ml_units_dotplot')
def ml_units_dotplot(w, h, **_):
    u = shop_raw()['units'].values
    mean, med = float(u.mean()), float(np.median(u))
    s = Scene(w, h)
    ax = axes_in(s, 0.9, 1.1, w - 1.8, h - 2.0)
    counts = {v: int((u == v).sum()) for v in range(1, 9)}
    for v, c in counts.items():
        ax.scatter([v] * c, range(1, c + 1), s=330, facecolor=PAPER, edgecolor=INK, linewidth=2.0, zorder=3)
    ax.axvline(mean, color=RED, lw=3, zorder=2)
    ax.axvline(med, color=INK, lw=3, zorder=2, ls='--')
    ax.set_xlim(0.4, 8.6)
    ax.set_ylim(0, max(counts.values()) + 2.4)
    ax.set_xticks(range(1, 9))
    ax.tick_params(axis='x', labelsize=20)
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.set_xlabel('units in one sale', fontsize=19)
    top = max(counts.values()) + 1.3
    ax.text(mean + 0.08, top, f'mean {mean:.2f}', color=RED, fontsize=22, fontweight='bold', ha='left', va='bottom')
    ax.text(med - 0.08, top, f'median {med:.1f}', color=INK, fontsize=22, fontweight='bold', ha='right', va='bottom')
    s.text(w / 2, h - 0.35, 'each circle is one of the 60 sales', size=19, color=MUTE)
    return s


@fig('ml_mean_level')
def ml_mean_level(w, h, **_):
    vals = [10, 12, 14, 16]
    m = float(np.mean(vals))
    s = Scene(w, h)
    bw, gap, sc = 0.5, 0.18, 0.17
    for k, (x0, shared) in enumerate([(0.35, False), (4.95, True)]):
        for i, v in enumerate(vals):
            hh = (m if shared else v) * sc
            s.rect(x0 + i * (bw + gap), 1.0, bw, hh, fill=GOLD if shared else PAPER, lw=2)
            s.text(x0 + i * (bw + gap) + bw / 2, 1.0 + hh + 0.22, f'{m:g}' if shared else str(v), size=20, weight='bold')
        s.line(x0 - 0.1, 1.0, x0 + 4 * (bw + gap), 1.0, lw=2)
    s.arrow(3.2, 2.3, 4.75, 2.3, color=RED, lw=2.6, head=18)
    s.text(3.97, 2.85, 'share the\ntotal equally', size=17, color=RED, weight='bold')
    s.text(1.7, 0.55, f'total {sum(vals)}', size=19)
    s.text(6.3, 0.55, f'{sum(vals)} / {len(vals)} = {m:g} each', size=19)
    s.text(w / 2, h - 0.3, 'mean', size=22, weight='bold')
    return s


@fig('ml_median_middle')
def ml_median_middle(w, h, **_):
    s = Scene(w, h)
    odd = sorted(shop_raw()['units'].head(9).tolist())
    even = [10, 12, 14, 16]
    s.text(0.4, h - 0.45, 'Nine sales in order', size=19, weight='bold', ha='left')
    s.cells(0.4, h - 1.55, odd, w=0.7, h=0.75, size=22, labels=None, hl=[4])
    s.text(0.4 + 4.5 * 0.7, h - 1.95, f'the middle one is {odd[4]}: the median', size=18, weight='bold')
    s.arrow(0.4 + 4.5 * 0.7, h - 1.78, 0.4 + 4.5 * 0.7, h - 1.58, color=RED, lw=2.4, head=14)
    s.text(0.4, 2.3, 'Four values in order', size=19, weight='bold', ha='left')
    s.cells(0.4, 1.0, even, w=0.9, h=0.8, size=22, hl=[1, 2])
    s.text(0.4 + 4 * 0.9 / 2, 0.55, '12 and 14 share the middle:\n(12 + 14) / 2 = 13', size=17)
    return s


@fig('ml_outlier_lines')
def ml_outlier_lines(w, h, **_):
    a = [10, 12, 14, 16]
    b = a + [100]
    s = Scene(w, h)
    for k, (vals, y, ttl) in enumerate([(a, h - 1.15, 'four values'), (b, h - 3.1, 'add one very large value')]):
        ax = axes_in(s, 1.0, y - 0.35, w - 1.6, 0.95)
        ax.set_xlim(0, 110)
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.spines['left'].set_visible(False)
        ax.scatter(vals, [0.45] * len(vals), s=380, facecolor=RED if (k == 1) else PAPER, edgecolor=INK, linewidth=2, zorder=3)
        if k == 1:
            ax.scatter(vals[:-1], [0.45] * (len(vals) - 1), s=380, facecolor=PAPER, edgecolor=INK, linewidth=2, zorder=4)
        ax.axvline(np.mean(vals), color=RED, lw=3, ymax=0.95)
        ax.axvline(np.median(vals), color=INK, lw=3, ls='--', ymax=0.95)
        ax.tick_params(axis='x', labelsize=16)
        s.text(0.4, y + 0.85, ttl, size=20, weight='bold', ha='left')
        s.text(w - 0.4, y + 0.85, f'mean {np.mean(vals):g}   median {np.median(vals):g}', size=21, weight='bold', ha='right')
    s.text(w / 2, 0.2, 'The mean moves from 13 to 30.4. The median moves from 13 to 14.', size=19, color=BODY)
    return s


@fig('ml_sorted_staircase')
def ml_sorted_staircase(w, h, **_):
    u = np.sort(shop_raw()['units'].values)
    s = Scene(w, h)
    ax = axes_in(s, 0.9, 1.0, w - 1.2, h - 1.6)
    ax.step(range(1, len(u) + 1), u, where='mid', color=INK, lw=2.6)
    q = np.percentile(u, [25, 50, 75])
    for pos, val, name in [(15, q[0], '25th'), (30, q[1], '50th'), (45, q[2], '75th')]:
        ax.vlines(pos + 0.5, 0, val, color=RED, lw=2.4, ls='--')
        ax.hlines(val, 0, pos + 0.5, color=RED, lw=2.4, ls='--')
        ax.text(pos + 1.2, 0.35, f'{name} percentile\n= {val:g}', fontsize=15, color=RED, fontweight='bold', va='bottom', ha='left')
    ax.set_xlim(0, 62)
    ax.set_ylim(0, 8.8)
    ax.set_xlabel('the 60 sales in order, smallest first', fontsize=17)
    ax.set_ylabel('units', fontsize=17)
    s.text(w / 2, h - 0.3, 'range: 1 to 8, which is 7', size=19, weight='bold')
    return s


@fig('ml_counters')
def ml_counters(w, h, n=20, k=12, cols=5, **_):
    s = Scene(w, h)
    rows = int(math.ceil(n / cols))
    r = min(0.3, (w - 1.0) / cols / 2.4, (h - 1.8) / rows / 2.4)
    gx = (w - cols * 2.4 * r) / 2
    for i in range(n):
        cx = gx + (i % cols) * 2.4 * r + r
        cy = h - 0.7 - (i // cols) * 2.4 * r
        s.circle(cx, cy, r, fill=GOLD if i < k else PAPER, lw=1.8)
    s.text(w / 2, 0.95, f'{k} out of {n}', size=24, weight='bold')
    s.text(w / 2, 0.4, f'{k} / {n} = {k / n:.2f} = {100 * k / n:g}%', size=21, mono=True)
    return s


# ================================================================== SESSION 10: cleaning
def raw_small():
    return pd.DataFrame({'id': [1, 2, 2, 3], 'price': [1000, None, None, 3000]})


@fig('ml_raw_problems')
def ml_raw_problems(w, h, **_):
    s = Scene(w, h)
    raw = raw_small()
    rows = [['id', 'price']] + [[str(int(r)), '' if np.isnan(p) else str(int(p))] for r, p in zip(raw['id'], raw['price'])]
    tx, ty, rh = 0.6, h - 0.5, 0.7
    s.table(tx, ty, [1.3, 1.9], rh, rows, size=24, hl_cells={(2, 1): PAPER, (3, 1): PAPER})
    for r in (2, 3):
        s.box(tx + 1.3 + 0.06, ty - (r + 1) * rh + 0.06, 1.9 - 0.12, rh - 0.12, '', fill='none', edge=RED, lw=3, r=0.05, z=6, dash=True)
    s.text(tx + 3.2 + 0.4, ty - 2.5 * rh - 0.0, '2 blank prices', size=22, color=RED, weight='bold', ha='left')
    s.brace(tx - 0.12, tx - 0.12, ty - 2 * rh, depth=0.0)
    s.box(tx - 0.12, ty - 4 * rh + 0.02, 3.5, 2 * rh - 0.04, '', fill='none', edge=INK, lw=2.4, r=0.05, z=5, dash=True)
    s.text(tx + 3.2 + 0.4, ty - 3.8 * rh, 'a repeated row', size=22, weight='bold', ha='left')
    # code to result cards on the right
    cx = 6.9
    cards = [('raw["price"].isna().sum()', '2', 'missing prices'), ('raw.duplicated().sum()', '1', 'repeated row'), ('len(raw.drop_duplicates())', '3', 'rows after cleaning')]
    for i, (code, val, what) in enumerate(cards):
        yy = h - 1.0 - i * 1.25
        s.box(cx, yy - 0.5, 3.5, 0.62, code, size=15, mono=True, fill='#111111', edge='#111111', color=PAPER, r=0.05)
        s.arrow(cx + 3.6, yy - 0.19, cx + 4.1, yy - 0.19, color=INK, lw=2, head=14)
        s.box(cx + 4.2, yy - 0.5, 0.6, 0.62, val, size=24, fill=GOLD, weight='bold', r=0.05)
        s.text(cx, yy - 0.78, what, size=17, color=MUTE, ha='left')
    return s


@fig('ml_zero_changes_mean')
def ml_zero_changes_mean(w, h, **_):
    s = Scene(w, h)
    known = [1000, 3000]
    ax = axes_in(s, 0.9, 1.2, w - 1.4, h - 2.5)
    vals = [np.mean(known), np.mean(known + [0])]
    bars = ax.bar(['leave it blank\n(mean of 1000, 3000)', 'fill with 0\n(mean of 1000, 0, 3000)'], vals, color=[GOLD, PAPER], edgecolor=[INK, RED], linewidth=[2, 3], width=0.55)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 60, f'{v:,.0f}', ha='center', va='bottom', fontsize=24, fontweight='bold', family=FONT)
    ax.set_ylim(0, 2600)
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='x', labelsize=17)
    s.text(w / 2, h - 0.4, 'average price (UGX)', size=21, weight='bold')
    s.text(w / 2, 0.3, '0 says the item was free. Nobody wrote the price down.', size=17, color=RED, weight='bold')
    return s


@fig('ml_copy_raw')
def ml_copy_raw(w, h, **_):
    s = Scene(w, h)
    raw = raw_small()
    rows = [['id', 'price']] + [[str(int(r)), '' if np.isnan(p) else str(int(p))] for r, p in zip(raw['id'], raw['price'])]
    s.table(0.3, h - 0.75, [0.8, 1.0], 0.5, rows, size=19)
    s.text(1.2, h - 0.35, 'raw', size=22, weight='bold')
    s.text(1.2, 0.95, 'never changed', size=17, color=MUTE)
    s.arrow(2.35, h - 2.0, 4.2, h - 2.0, color=RED, lw=2.6, head=18)
    s.text(3.3, h - 1.55, 'drop_duplicates()\n.copy()', size=15, mono=True)
    clean = rows[:3] + [rows[4]]
    s.table(4.7, h - 0.75, [0.8, 1.0], 0.5, clean, size=19, hl_rows=(), hl_cells={(2, 1): PAPER})
    s.text(5.6, h - 0.35, 'clean', size=22, weight='bold')
    s.text(5.6, 1.45, '3 rows, one price\nstill missing', size=17, color=MUTE)
    s.box(4.7, 0.3, 1.8, 0.55, 'work here', size=18, fill=GOLD, weight='bold', r=0.05)
    return s


@fig('ml_cleaning_log')
def ml_cleaning_log(w, h, **_):
    s = Scene(w, h)
    rows = [['step', 'count'], ['raw rows', '4'], ['duplicate removed', '1'], ['price still missing', '1']]
    s.table(0.4, h - 0.8, [3.3, 1.2], 0.6, rows, size=21, hl_rows=(0,), hl_fill='#EDEDED')
    s.text(w - 0.4, h - 1.3, 'a reader can\nrepeat each step', size=19, ha='right', weight='bold')
    s.text(0.4, 1.55, 'shape (3, 2)', size=19, mono=True, ha='left')
    s.text(0.4, 1.0, 'The log names every change and how many rows it touched.', size=17, ha='left', color=BODY)
    return s


@fig('ml_save_roundtrip')
def ml_save_roundtrip(w, h, **_):
    s = Scene(w, h)
    rows = [['step', 'count'], ['raw rows', '4'], ['duplicate removed', '1'], ['price still missing', '1']]
    s.table(0.2, h - 0.4, [2.0, 0.9], 0.38, rows, size=15, hl_rows=(0,), hl_fill='#EDEDED')
    s.arrow(3.3, h - 1.15, 4.7, h - 1.15, color=RED, lw=2.4, head=16)
    s.text(4.0, h - 0.7, 'to_csv', size=16, mono=True)
    s.code(4.9, h - 0.4, ['step,count', 'raw rows,4', 'duplicate removed,1', 'price still missing,1'], size=15, line_h=0.3, pad=0.14, w=2.9)
    s.arrow(7.95, h - 1.15, 9.0, h - 1.15, color=RED, lw=2.4, head=16)
    s.text(8.5, h - 0.7, 'read_csv', size=16, mono=True)
    s.table(9.1, h - 0.4, [1.6, 0.9], 0.38, [['step', 'count'], ['raw rows', '4'], ['...', '...']], size=15, hl_rows=(0,), hl_fill='#EDEDED')
    s.text(0.2, 1.95, 'index=False', size=19, mono=True, weight='bold', ha='left')
    s.code(0.2, 1.65, ['step,count', 'raw rows,4'], size=14, line_h=0.28, pad=0.12, w=2.5)
    s.text(3.1, 1.35, 'the file holds only your columns', size=16, ha='left')
    s.code(6.6, 1.65, [',step,count', '0,raw rows,4'], size=14, line_h=0.28, pad=0.12, w=2.5)
    s.text(6.6, 2.0 - 0.05 + 0.0, '', size=14)
    s.text(9.3, 1.35, 'without it: an extra\ncolumn of row numbers', size=16, ha='left', color=RED)
    s.text(6.6, 2.05, 'default', size=17, mono=True, weight='bold', ha='left', color=RED)
    return s


# ================================================================== SESSION 11: charts
@fig('ml_chart_trio')
def ml_chart_trio(w, h, **_):
    d = shop()
    s = Scene(w, h)
    tot = d.groupby('item')['revenue_ugx'].sum()
    cw, gap = 3.55, 0.3
    for k in range(3):
        x = 0.2 + k * (cw + gap)
        ax = axes_in(s, x + 0.25, 1.2, cw - 0.4, h - 2.5)
        if k == 0:
            ax.bar(tot.index, tot.values, color=[GOLD if v == tot.max() else PAPER for v in tot.values], edgecolor=INK, linewidth=2)
            ax.set_yticks([])
            ax.spines['left'].set_visible(False)
            cap, sub = 'Bar chart', 'compare amounts'
        elif k == 1:
            ax.hist(d['units'], bins=np.arange(0.5, 9.5, 1), color=PAPER, edgecolor=INK, linewidth=2)
            ax.set_yticks([])
            ax.spines['left'].set_visible(False)
            cap, sub = 'Histogram', 'see how values spread'
        else:
            data = [d[d['item'] == i]['units'] for i in ['Book', 'Juice', 'Pen']]
            bp = ax.boxplot(data, labels=['Book', 'Juice', 'Pen'], patch_artist=True, medianprops=dict(color=INK, linewidth=2.6), boxprops=dict(facecolor=PAPER, edgecolor=INK, linewidth=2), whiskerprops=dict(color=INK, linewidth=2), capprops=dict(color=INK, linewidth=2))
            ax.set_yticks([])
            ax.spines['left'].set_visible(False)
            cap, sub = 'Box plot', 'compare the spread'
        ax.tick_params(axis='x', labelsize=15)
        s.text(x + cw / 2, h - 0.45, cap, size=24, weight='bold')
        s.text(x + cw / 2, 0.55, sub, size=19, color=BODY)
    return s


@fig('ml_chart_anatomy')
def ml_chart_anatomy(w, h, **_):
    d = shop().groupby('item')['revenue_ugx'].sum()
    s = Scene(w, h)
    ax = axes_in(s, 3.0, 0.95, 4.3, h - 2.3)
    ax.bar(d.index, d.values, color=[GOLD if v == d.max() else PAPER for v in d.values], edgecolor=INK, linewidth=2)
    ax.set_ylim(0, 330000)
    ax.set_yticks([0, 100000, 200000, 300000])
    ax.set_yticklabels(['0', '100k', '200k', '300k'])
    ax.tick_params(labelsize=15)
    ax.set_ylabel('Revenue (UGX)', fontsize=16)
    s.text(5.15, h - 0.4, 'Revenue by item', size=21, weight='bold')
    s.text(0.25, h - 0.4, 'title', size=19, color=RED, weight='bold', ha='left')
    s.arrow(0.95, h - 0.4, 3.8, h - 0.4, color=RED, lw=1.8, head=13)
    s.text(0.25, 3.0, 'axis label:\nwhat is measured\nand its unit', size=17, color=RED, weight='bold', ha='left')
    s.arrow(1.4, 2.55, 2.05, 2.55, color=RED, lw=1.8, head=13)
    s.text(0.25, 1.35, 'the axis\nstarts at zero', size=17, color=RED, weight='bold', ha='left')
    s.arrow(1.9, 1.2, 3.0, 1.12, color=RED, lw=1.8, head=13)
    s.text(w / 2, 0.25, 'one bar for each item, heights from the data', size=15, color=MUTE)
    return s


@fig('ml_pick_chart')
def ml_pick_chart(w, h, **_):
    d = shop()
    s = Scene(w, h)
    cw, gap = 2.65, 0.43
    qs = ['Which item\nearns the most?', 'How are the\nunits spread?', 'Do the items differ\nin spread?', 'How did revenue\nchange by day?']
    tn = ['bar chart', 'histogram', 'box plot', 'line chart']
    for k in range(4):
        x = 0.25 + k * (cw + gap)
        ax = axes_in(s, x + 0.15, 1.5, cw - 0.3, 1.45)
        if k == 0:
            t = d.groupby('item')['revenue_ugx'].sum()
            ax.bar(range(3), t.values, color=[GOLD if v == t.max() else PAPER for v in t.values], edgecolor=INK, linewidth=2)
        elif k == 1:
            ax.hist(d['units'], bins=np.arange(0.5, 9.5, 1), color=PAPER, edgecolor=INK, linewidth=2)
        elif k == 2:
            ax.boxplot([d[d['item'] == i]['units'] for i in ['Book', 'Juice', 'Pen']], patch_artist=True, medianprops=dict(color=INK, linewidth=2.4), boxprops=dict(facecolor=PAPER, edgecolor=INK, linewidth=2), whiskerprops=dict(color=INK, linewidth=2), capprops=dict(color=INK, linewidth=2))
        else:
            t = d.groupby('date')['revenue_ugx'].sum()
            ax.plot(range(len(t)), t.values, color=INK, linewidth=2.6)
        ax.set_xticks([])
        ax.set_yticks([])
        s.text(x + cw / 2, h - 0.55, qs[k], size=18, weight='bold')
        s.arrow(x + cw / 2, h - 1.15, x + cw / 2, 3.1, color=RED, lw=2, head=14)
        s.text(x + cw / 2, 0.85, tn[k], size=22, weight='bold')
    return s


@fig('ml_boxplot_anatomy')
def ml_boxplot_anatomy(w, h, **_):
    u = shop_raw()[shop_raw().item == 'Pen']['units'].values
    q1, med, q3 = np.percentile(u, [25, 50, 75])
    lo, hi = u.min(), u.max()
    s = Scene(w, h)
    x0, x1 = 0.9, w - 0.9
    sc = (x1 - x0) / 9.0
    X = lambda v: x0 + (v - 0.0) * sc
    yb, bh = 2.15, 1.0
    s.line(x0, yb - 0.5, x1, yb - 0.5, lw=2)
    for v in range(0, 10):
        s.line(X(v), yb - 0.5, X(v), yb - 0.62, lw=1.6)
        s.text(X(v), yb - 0.9, str(v), size=17)
    s.text((x0 + x1) / 2, yb - 1.35, 'units in one sale (Pen sales)', size=17, color=MUTE)
    s.line(X(lo), yb + bh / 2, X(q1), yb + bh / 2, lw=3)
    s.line(X(q3), yb + bh / 2, X(hi), yb + bh / 2, lw=3)
    s.line(X(lo), yb + 0.2, X(lo), yb + bh - 0.2, lw=3)
    s.line(X(hi), yb + 0.2, X(hi), yb + bh - 0.2, lw=3)
    s.rect(X(q1), yb, X(q3) - X(q1), bh, fill=GOLD, lw=2.6)
    s.line(X(med), yb, X(med), yb + bh, lw=4.5, z=5)
    for v, name, up in [(lo, f'smallest {lo:g}', True), (q1, f'25% mark {q1:g}', False), (med, f'median {med:g}', True), (q3, f'75% mark {q3:g}', False), (hi, f'largest {hi:g}', True)]:
        yy = yb + bh + 0.55 if up else yb + bh + 1.25
        s.text(X(v), yy + 0.0, name, size=18, weight='bold', color=RED if name.startswith('median') else INK)
        s.arrow(X(v), yy - 0.22, X(v), yb + bh + 0.04 if up else yb + bh + 0.04, color=GREY, lw=1.4, head=10)
    s.text(X((q1 + q3) / 2), yb - 0.22, 'the box holds the middle half of the sales', size=16, weight='bold')
    return s


@fig('ml_hist_bins')
def ml_hist_bins(w, h, **_):
    u = shop_raw()['units'].values
    cnt = np.bincount(u, minlength=9)[1:]
    s = Scene(w, h)
    ax = axes_in(s, 0.9, 1.0, w - 1.3, h - 2.1)
    bars = ax.bar(range(1, 9), cnt, color=[GOLD if c == cnt.max() else PAPER for c in cnt], edgecolor=INK, linewidth=2, width=0.9)
    for b, c in zip(bars, cnt):
        ax.text(b.get_x() + b.get_width() / 2, c + 0.2, str(c), ha='center', fontsize=20, fontweight='bold', family=FONT)
    ax.set_ylim(0, cnt.max() + 2)
    ax.set_xticks(range(1, 9))
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='x', labelsize=20)
    ax.set_xlabel('units in one sale', fontsize=18)
    s.text(w / 2, h - 0.35, f'how many of the 60 sales had each number of units', size=19, weight='bold')
    return s


@fig('ml_finding_card')
def ml_finding_card(w, h, **_):
    d = shop().groupby('item')['revenue_ugx'].sum()
    s = Scene(w, h)
    ax = axes_in(s, 1.35, 0.7, 4.1, h - 1.7)
    ax.bar(d.index, d.values, color=[GOLD if v == d.max() else PAPER for v in d.values], edgecolor=INK, linewidth=2, width=0.6)
    ax.set_yticks([0, 100000, 200000, 300000])
    ax.set_yticklabels(['0', '100k', '200k', '300k'])
    ax.set_ylim(0, 330000)
    ax.set_ylabel('Revenue (UGX)', fontsize=16)
    ax.tick_params(labelsize=15)
    s.text(3.4, h - 0.35, 'Revenue by item, practice shop', size=19, weight='bold')
    x = 5.9
    s.box(x, h - 2.2, 5.8, 1.55, '', fill=PAPER, lw=2, r=0.05)
    s.text(x + 0.25, h - 0.95, 'Finding', size=22, weight='bold', ha='left')
    s.text(x + 0.25, h - 1.55, f'Book earns the most: UGX {int(d.max()):,}.', size=20, ha='left')
    s.box(x, 0.6, 5.8, 1.55, '', fill=PAPER, edge=RED, lw=2, r=0.05)
    s.text(x + 0.25, 1.65, 'Limitation', size=22, weight='bold', ha='left', color=RED)
    s.text(x + 0.25, 1.05, 'Practice data with no costs, so\nthis says nothing about profit.', size=19, ha='left')
    return s


# ================================================================== SESSION 12: checkpoint one and the project question
@fig('ml_checkpoint_flow')
def ml_checkpoint_flow(w, h, **_):
    s = Scene(w, h)
    steps = [('Read', 'folder', 'read_csv'), ('Check', 'magnifier', 'shape, isna'), ('Calculate', 'calculator', 'groupby'), ('Chart', 'bars', 'labelled'), ('Explain', 'notebook', 'findings'), ('Rerun', 'clock', 'run all')]
    n = len(steps)
    bw = 1.55
    gap = (w - 0.3 - n * bw) / (n - 1)
    for i, (name, icon, sub) in enumerate(steps):
        x = 0.15 + i * (bw + gap)
        s.box(x, 1.2, bw, 2.55, '', fill=PAPER, lw=1.8, r=0.06)
        s.icon(icon, x + bw / 2, 3.05, 0.9)
        s.text(x + bw / 2, 2.2, name, size=21, weight='bold')
        s.text(x + bw / 2, 1.65, sub, size=15, color=MUTE)
        if i < n - 1:
            s.arrow(x + bw + 0.04, 2.5, x + bw + gap - 0.04, 2.5, color=RED, lw=2.2, head=14)
    s.text(w / 2, 0.55, 'The same six steps, on your own, in one notebook', size=19, color=BODY)
    return s


@fig('ml_restart_run_all')
def ml_restart_run_all(w, h, **_):
    s = Scene(w, h)
    s.text(1.75, h - 0.4, 'hidden memory', size=21, weight='bold', color=RED)
    for i, n in enumerate([5, 2, 7, 3]):
        s.box(0.35, h - 1.3 - i * 0.68, 2.8, 0.55, f'In [{n}]: a cell', size=18, r=0.04, mono=True, edge=RED)
    s.text(1.75, 0.75, 'works today, because the\nnotebook remembers a cell\nyou no longer have', size=16, color=RED)
    s.arrow(3.35, 2.8, 4.45, 2.8, color=INK, lw=2.6, head=18)
    s.text(3.9, 3.4, 'Restart\nand run all', size=17, weight='bold')
    s.text(6.0, h - 0.4, 'top to bottom', size=21, weight='bold')
    for i in range(4):
        s.box(4.6, h - 1.3 - i * 0.68, 2.8, 0.55, f'In [{i + 1}]: a cell', size=18, r=0.04, mono=True, fill=GOLD)
    s.text(6.0, 0.95, 'works for everyone,\nevery time', size=16)
    return s


@fig('ml_question_target_input')
def ml_question_target_input(w, h, **_):
    s = Scene(w, h)
    s.text(1.35, h - 0.5, 'inputs', size=21, weight='bold')
    s.text(1.35, h - 0.9, 'known before', size=16, color=MUTE)
    for i, name in enumerate(['area_m2', 'rooms']):
        s.box(0.3, h - 2.0 - i * 1.0, 2.1, 0.75, name, size=19, mono=True, r=0.05)
        s.icon('check', 2.75, h - 1.62 - i * 1.0, 0.55)
        s.arrow(3.1, h - 1.62 - i * 1.0, 3.9, h - 2.3 - 0.5 * 0.0, color=INK, lw=2, head=14)
    s.box(3.95, h - 3.1, 1.5, 1.6, 'model', size=22, weight='bold', r=0.08, fill='#111111', edge='#111111', color=PAPER)
    s.arrow(5.55, h - 2.3, 6.1, h - 2.3, color=INK, lw=2.4, head=16)
    s.text(6.85, h - 0.5, 'target', size=21, weight='bold')
    s.text(6.85, h - 0.9, 'the answer', size=16, color=MUTE)
    s.box(6.15, h - 2.7, 1.45, 0.8, 'rent_ugx', size=17, mono=True, fill=GOLD, weight='bold', r=0.05)
    s.text(w / 2, 0.85, 'Can area and rooms predict monthly rent?', size=21, weight='bold')
    s.text(w / 2, 0.35, 'Every input must be known before the rent is.', size=17, color=BODY)
    return s


@fig('ml_three_sentences')
def ml_three_sentences(w, h, **_):
    s = Scene(w, h)
    rows = [('Question', 'Can area and rooms predict the monthly rent of a home?'),
            ('Dataset', 'synthetic_homes.csv: 120 invented homes.'),
            ('Target', 'rent_ugx, the number we want to predict.')]
    for i, (a, b) in enumerate(rows):
        y = h - 0.5 - i * 1.3
        s.text(0.4, y - 0.5, a, size=26, weight='bold', ha='left')
        s.text(3.2, y - 0.5, b, size=22, ha='left')
        s.line(0.4, y - 1.05, w - 0.4, y - 1.05, color=HAIR, lw=1.4)
    return s


@fig('ml_data_dictionary')
def ml_data_dictionary(w, h, **_):
    s = Scene(w, h)
    rows = [['column', 'meaning', 'unit'], ['home_id', 'a number for each home', 'none'], ['area_m2', 'floor area', 'square metres'], ['rooms', 'number of rooms', 'count'], ['rent_ugx', 'monthly rent', 'UGX']]
    s.table(0.2, h - 0.5, [1.55, 3.0, 2.3], 0.7, rows, size=18, mono_cols=(0,), hl_rows=(0,), hl_fill='#EDEDED', align=['left', 'left', 'left'])
    s.text(0.2, 0.75, 'Written once, so a stranger can read the file.', size=18, ha='left', color=BODY)
    s.text(0.2, 0.3, 'home_id is a label: it is never an input.', size=18, ha='left', color=RED, weight='bold')
    return s


# ================================================================== SESSION 13: features, targets, baseline, leakage
@fig('ml_features_target')
def ml_features_target(w, h, **_):
    s = Scene(w, h)
    d = homes().head(4)[['area_m2', 'rooms', 'rent_ugx']]
    tx, ty, rh = 0.4, h - 1.5, 0.5
    cws = [1.45, 1.05, 1.5]
    rows = [list(d.columns)] + [[f'{v:,}' if c == 'rent_ugx' else str(v) for c, v in zip(d.columns, r)] for r in d.astype(object).values.tolist()]
    s.table(tx, ty, cws, rh, rows, size=19, hl_cells={(0, 0): GOLD, (0, 1): GOLD, (0, 2): '#EDEDED'})
    s.brace(tx, tx + cws[0] + cws[1], ty + 0.2, depth=0.18)
    s.text(tx + (cws[0] + cws[1]) / 2, ty + 0.55, 'features: the inputs', size=20, weight='bold')
    s.brace(tx + cws[0] + cws[1] + 0.05, tx + sum(cws), ty + 0.2, depth=0.18)
    s.text(tx + sum(cws) - cws[2] / 2 + 0.2, ty + 0.8, 'target:\nthe answer', size=20, weight='bold', color=RED)
    mx = tx + sum(cws) + 0.5
    if w > 9:
        s.box(mx + 0.3, h - 3.4, 1.7, 1.7, 'model', size=24, weight='bold', r=0.08, fill='#111111', edge='#111111', color=PAPER)
        s.arrow(mx - 0.1, h - 2.55, mx + 0.25, h - 2.55, color=INK, lw=2.4, head=16)
        s.arrow(mx + 2.05, h - 2.55, mx + 2.7, h - 2.55, color=INK, lw=2.4, head=16)
        s.text(mx + 4.35, h - 2.55, 'a guess of\nthe rent', size=21, weight='bold', ha='center')
        s.text(w / 2, 0.45, 'The model sees the features. The target stays hidden when it guesses.', size=19, color=BODY)
    else:
        s.text(w / 2, 0.55, 'A model sees the features and\nguesses the target.', size=19, color=BODY)
    return s


@fig('ml_baseline_guess')
def ml_baseline_guess(w, h, **_):
    train = [2000, 4000, 6000]
    m = float(np.mean(train))
    new = 5000
    s = Scene(w, h)
    ax = axes_in(s, 1.4, 1.0, w - 1.9, h - 1.9)
    ax.scatter([1, 2, 3], train, s=330, facecolor=PAPER, edgecolor=INK, linewidth=2.2, zorder=3)
    ax.axhline(m, color=RED, lw=3, zorder=2)
    ax.scatter([4.6], [new], s=420, facecolor=GOLD, edgecolor=INK, linewidth=2.2, zorder=4)
    ax.plot([4.6, 4.6], [m, new], color=INK, lw=3, zorder=3)
    ax.text(4.85, (m + new) / 2 + 80, f'error {abs(new - m):,.0f}', fontsize=19, fontweight='bold', va='center', ha='left', family=FONT)
    ax.text(0.55, m + 220, f'baseline guess = mean = {m:,.0f}', fontsize=17, color=RED, fontweight='bold', va='bottom', family=FONT)
    ax.set_xlim(0.4, 6.7)
    ax.set_ylim(0, 7200)
    ax.set_xticks([2, 4.6])
    ax.set_xticklabels(['training prices', 'new item,\nreal price 5,000'], fontsize=16)
    ax.set_yticks([0, 2000, 4000, 6000])
    ax.set_yticklabels(['0', '2,000', '4,000', '6,000'], fontsize=15)
    s.text(w / 2, h - 0.35, 'always guess the training mean', size=20, weight='bold')
    return s


@fig('ml_practice_vs_exam')
def ml_practice_vs_exam(w, h, **_):
    s = Scene(w, h)
    s.icon('notebook', 1.7, h - 1.4, 1.4)
    s.text(1.7, h - 2.5, 'training data', size=24, weight='bold')
    s.text(1.7, h - 3.0, 'the model learns\nfrom these', size=18)
    s.icon('magnifier', 6.0, h - 1.4, 1.4)
    s.text(6.0, h - 2.5, 'test data', size=24, weight='bold')
    s.text(6.0, h - 3.0, 'kept aside to check\nwhat it learned', size=18)
    s.box(0.5, 0.35, 5.4, 0.55, '', fill=PAPER, lw=2, r=0.03)
    s.rect(0.5 + 4.05, 0.35, 1.35, 0.55, fill=GOLD, lw=2)
    s.text(0.5 + 4.05 / 2, 0.625, 'training: practice questions', size=15)
    s.text(0.5 + 4.05 + 0.675, 0.625, 'test', size=18, weight='bold')
    s.text(w / 2, 1.2, 'like practice questions and the exam', size=17, color=MUTE)
    return s


@fig('ml_open_model')
def ml_open_model(w, h, **_):
    d = homes()
    beta = ols(d[['area_m2']].values, d['rent_ugx'].values)
    s = Scene(w, h)
    ax = axes_in(s, 1.45, 0.95, w - 1.8, h - 2.0)
    ax.scatter(d['area_m2'], d['rent_ugx'], s=38, facecolor=PAPER, edgecolor=INK, linewidth=1.3, zorder=2)
    xs = np.array([d['area_m2'].min(), d['area_m2'].max()])
    ax.plot(xs, beta[0] + beta[1] * xs, color=RED, lw=3.4, zorder=3)
    ax.set_xlabel('area (square metres)', fontsize=17)
    ax.set_ylabel('rent (UGX)', fontsize=17)
    ax.set_yticks([200000, 400000, 600000])
    ax.set_yticklabels(['200k', '400k', '600k'])
    ax.tick_params(labelsize=15)
    s.box(1.5, h - 0.8, 5.2, 0.6, f'rent = {beta[0]:,.0f} + {beta[1]:,.0f} x area', size=20, fill=GOLD, weight='bold', r=0.05)
    return s


@fig('ml_leakage_timeline')
def ml_leakage_timeline(w, h, **_):
    s = Scene(w, h)
    y = h / 2 + 0.1
    s.arrow(0.3, y, w - 0.3, y, color=INK, lw=3, head=22)
    s.text(0.5, y + 0.35, 'time', size=16, color=MUTE, ha='left')
    xs = [1.5, 4.1, 6.5]
    s.box(0.4, y + 0.8, 2.3, 1.3, '', fill=PAPER, lw=2, r=0.05)
    s.text(1.55, y + 1.8, 'before', size=20, weight='bold')
    s.text(1.55, y + 1.3, 'area, rooms', size=17)
    s.icon('check', 1.55, y - 0.0, 0.5)
    for xc in (1.55, 4.1, 6.5):
        s.line(xc, y + 0.8, xc, y + 0.2, color=GREY, lw=1.6)
    s.box(3.0, y + 0.8, 2.2, 1.3, '', fill=GOLD, lw=2.2, r=0.05)
    s.text(4.1, y + 1.8, 'the answer', size=20, weight='bold')
    s.text(4.1, y + 1.3, 'selling price', size=17)
    s.circle(4.1, y, 0.12, fill=INK)
    s.box(5.5, y + 0.8, 2.0, 1.3, '', fill=PAPER, edge=RED, lw=2.6, r=0.05)
    s.text(6.5, y + 1.8, 'after', size=20, weight='bold', color=RED)
    s.text(6.5, y + 1.3, 'final payment', size=17, color=RED)
    s.icon('cross', 6.5, y, 0.5)
    s.text(w / 2, 1.0, 'A feature must exist before the answer does.', size=19, weight='bold')
    s.text(w / 2, 0.5, 'Information from after it is leakage.', size=19, color=RED, weight='bold')
    return s


# ================================================================== SESSION 14: a line
def hand_and_fit():
    d = homes().head(8)
    x = d['area_m2'].values.astype(float)
    y = d['rent_ugx'].values.astype(float)
    hand = 100000 + 3000 * x
    beta = ols(x.reshape(-1, 1), y)
    fit = beta[0] + beta[1] * x
    return x, y, hand, beta, fit


@fig('ml_eight_homes_lines')
def ml_eight_homes_lines(w, h, **_):
    x, y, hand, beta, fit = hand_and_fit()
    mh, mf, mb = mae(y, hand), mae(y, fit), mae(y, np.full_like(y, y.mean()))
    s = Scene(w, h)
    ax = axes_in(s, 1.4, 0.85, 6.0, h - 1.35)
    xs = np.array([x.min() - 5, x.max() + 5])
    ax.plot(xs, 100000 + 3000 * xs, color=RED, lw=3, ls='--')
    ax.plot(xs, beta[0] + beta[1] * xs, color=INK, lw=3.2)
    ax.axhline(y.mean(), color=GREY, lw=2.4)
    ax.scatter(x, y, s=190, facecolor=GOLD, edgecolor=INK, linewidth=2, zorder=4)
    ax.set_xlabel('area (square metres)', fontsize=17)
    ax.set_ylabel('rent (UGX)', fontsize=17)
    ax.set_yticks([200000, 400000, 600000])
    ax.set_yticklabels(['200k', '400k', '600k'])
    ax.tick_params(labelsize=15)
    s.text(4.4, h - 0.3, 'eight homes', size=20, weight='bold')
    X = 8.0
    rows = [(RED, '--', 'my guess line', mh), (INK, '-', 'the fitted line', mf), (GREY, '-', 'always the mean', mb)]
    for i, (c, ls, name, v) in enumerate(rows):
        yy = h - 1.0 - i * 1.15
        s.line(X, yy, X + 0.6, yy, color=c, lw=3.4, dash=(ls == '--'))
        s.text(X + 0.8, yy, name, size=19, weight='bold', ha='left')
        s.text(X + 0.8, yy - 0.42, f'misses by {money(v)}', size=18, ha='left', color=BODY)
    s.text(X, 0.3, 'on average, in UGX', size=16, ha='left', color=MUTE)
    return s


@fig('ml_line_anatomy')
def ml_line_anatomy(w, h, **_):
    s = Scene(w, h)
    ax = axes_in(s, 1.5, 0.95, w - 1.9, h - 1.8)
    xs = np.array([0, 60])
    ax.plot(xs, 100000 + 3000 * xs, color=INK, lw=3.4)
    ax.scatter([0], [100000], s=260, facecolor=GOLD, edgecolor=INK, linewidth=2.2, zorder=4)
    ax.plot([20, 30, 30], [160000, 160000, 190000], color=RED, lw=3)
    ax.text(25, 145000, 'run: 10 m2', fontsize=16, color=RED, ha='center', va='top', fontweight='bold', family=FONT)
    ax.text(31, 175000, 'rise: 30,000', fontsize=16, color=RED, ha='left', va='center', fontweight='bold', family=FONT)
    ax.text(3, 85000, 'start: 100,000 at area 0', fontsize=17, fontweight='bold', va='top', ha='left', family=FONT)
    ax.set_xlim(-2, 62)
    ax.set_ylim(0, 300000)
    ax.set_xlabel('area (square metres)', fontsize=17)
    ax.set_ylabel('rent (UGX)', fontsize=17)
    ax.set_yticks([100000, 200000, 300000])
    ax.set_yticklabels(['100k', '200k', '300k'])
    ax.tick_params(labelsize=15)
    s.text(w / 2, h - 0.35, 'rent = start + rise per m2 x area', size=20, weight='bold')
    return s


@fig('ml_guess_gaps')
def ml_guess_gaps(w, h, **_):
    x, y, hand, beta, fit = hand_and_fit()
    s = Scene(w, h)
    ax = axes_in(s, 1.45, 0.95, w - 1.8, h - 2.15)
    xs = np.array([x.min() - 5, x.max() + 5])
    ax.plot(xs, 100000 + 3000 * xs, color=RED, lw=3, ls='--', zorder=2)
    for xi, yi, hi in zip(x, y, hand):
        ax.plot([xi, xi], [yi, hi], color=INK, lw=3, zorder=3)
    ax.scatter(x, y, s=170, facecolor=GOLD, edgecolor=INK, linewidth=2, zorder=4)
    ax.set_xlabel('area (square metres)', fontsize=17)
    ax.set_ylabel('rent (UGX)', fontsize=17)
    ax.set_yticks([200000, 400000, 600000])
    ax.set_yticklabels(['200k', '400k', '600k'])
    ax.tick_params(labelsize=15)
    s.box(1.5, h - 0.85, 5.6, 0.62, f'average of the black bars = {money(mae(y, hand))} UGX', size=18, fill=GOLD, weight='bold', r=0.05)
    return s


@fig('ml_three_lines')
def ml_three_lines(w, h, **_):
    x, y, hand, beta, fit = hand_and_fit()
    mb = np.full_like(y, y.mean())
    s = Scene(w, h)
    cw = 3.8
    for k, (name, pred, line_fn, col) in enumerate([('plain mean guess', mb, lambda xs: np.full_like(xs, y.mean()), GREY),
                                                     ('my guess line', hand, lambda xs: 100000 + 3000 * xs, RED),
                                                     ('the fitted line', fit, lambda xs: beta[0] + beta[1] * xs, INK)]):
        x0 = 0.15 + k * (cw + 0.2)
        ax = axes_in(s, x0 + 0.1, 1.2, cw - 0.2, h - 2.4)
        xs = np.array([x.min() - 5, x.max() + 5])
        ax.plot(xs, line_fn(xs), color=col, lw=3, ls='--' if col == RED else '-')
        for xi, yi, pi in zip(x, y, pred):
            ax.plot([xi, xi], [yi, pi], color=INK, lw=2.4, zorder=3)
        ax.scatter(x, y, s=95, facecolor=GOLD, edgecolor=INK, linewidth=1.6, zorder=4)
        ax.set_xticks([])
        ax.set_yticks([])
        s.text(x0 + cw / 2, h - 0.4, name, size=19, weight='bold')
        s.text(x0 + cw / 2, 0.65, money(mae(y, pred)), size=28, weight='bold', mono=True)
        s.text(x0 + cw / 2, 0.25, 'average miss (UGX)', size=15, color=MUTE)
    return s


@fig('ml_fit_predict_flow')
def ml_fit_predict_flow(w, h, **_):
    s = Scene(w, h)
    Xv = [10, 20, 30, 40]
    yv = [100, 200, 300, 400]
    s.table(0.3, h - 0.5, [0.95], 0.5, [['X']] + [[str(v)] for v in Xv], size=19)
    s.table(1.4, h - 0.5, [0.95], 0.5, [['y']] + [[str(v)] for v in yv], size=19)
    s.text(1.35, 1.5, 'examples:\ninputs and answers', size=16, color=MUTE)
    s.arrow(2.5, h - 1.8, 3.2, h - 1.8, color=INK, lw=2.4, head=16)
    s.box(3.25, h - 2.35, 1.3, 1.1, 'fit', size=24, mono=True, weight='bold', fill='#111111', edge='#111111', color=PAPER, r=0.07)
    s.arrow(4.6, h - 1.8, 5.1, h - 1.8, color=INK, lw=2.4, head=16)
    ax = axes_in(s, 5.2, h - 3.1, 2.3, 2.3)
    ax.plot([0, 50], [0, 500], color=RED, lw=3)
    ax.scatter(Xv, yv, s=70, facecolor=PAPER, edgecolor=INK, linewidth=1.8, zorder=3)
    ax.scatter([35], [350], s=150, facecolor=GOLD, edgecolor=INK, linewidth=2, zorder=4)
    ax.set_xticks([])
    ax.set_yticks([])
    s.text(6.35, h - 0.6, 'the learned line', size=17, weight='bold')
    s.text(w - 0.3, h - 3.5, 'predict([[35]])  gives  350', size=18, mono=True, ha='right', weight='bold')
    s.text(w / 2, 0.4, 'fit learns the line. predict reads a new answer from it.', size=17, color=BODY)
    return s


@fig('ml_extrapolation')
def ml_extrapolation(w, h, **_):
    s = Scene(w, h)
    ax = axes_in(s, 0.5, 1.0, 4.9, h - 2.0)
    Xv = np.array([10, 20, 30, 40])
    ax.plot([0, 70], [0, 700], color=INK, lw=3)
    ax.scatter(Xv, Xv * 10, s=120, facecolor=PAPER, edgecolor=INK, linewidth=2, zorder=3)
    ax.scatter([35], [350], s=240, facecolor=GOLD, edgecolor=INK, linewidth=2.2, zorder=4)
    ax.axvspan(10, 40, color='#F1F1F1', zorder=0)
    ax.text(25, 560, 'examples\nlive here', fontsize=16, ha='center', fontweight='bold', family=FONT)
    ax.text(35, 250, '35: fine', fontsize=17, ha='center', va='top', fontweight='bold', family=FONT)
    ax.set_xlim(0, 70)
    ax.set_ylim(0, 760)
    ax.set_xticks([10, 20, 30, 40])
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    s.arrow(5.1, 2.9, 5.85, 2.9, color=RED, lw=2.4, head=18)
    s.text(6.7, 2.9, '1000?', size=34, weight='bold', color=RED)
    s.text(6.7, 2.05, 'far off the page:\nno example\nis near', size=17, color=RED, weight='bold')
    s.text(w / 2, h - 0.35, 'a line is trustworthy near its examples', size=19, weight='bold')
    return s


# ================================================================== SESSION 15: a complete regression experiment
def homes_split():
    d = homes()
    tr, te = split_idx(len(d), 0.25, 7)
    Xc = d[['area_m2', 'rooms']].values.astype(float)
    y = d['rent_ugx'].values.astype(float)
    beta = ols(Xc[tr], y[tr])
    pred = predict(beta, Xc[te])
    base = np.full(len(te), y[tr].mean())
    return d, tr, te, y, pred, base, beta


@fig('ml_split_homes')
def ml_split_homes(w, h, **_):
    d, tr, te, y, pred, base, beta = homes_split()
    s = Scene(w, h)
    cols, rows, t = 12, 10, 0.36
    x0, y0 = 0.4, h - 0.45
    test = set(te.tolist())
    for i in range(len(d)):
        cx = x0 + (i % cols) * t
        cy = y0 - (i // cols + 1) * t
        s.rect(cx, cy, t - 0.05, t - 0.05, fill=GOLD if i in test else PAPER, lw=1.2)
    s.text(x0 + cols * t / 2, 0.2, '120 homes, one square each', size=16, color=MUTE, va='bottom')
    X = 5.5
    s.box(X, h - 1.7, 0.45, 0.45, '', fill=PAPER, lw=2, r=0.03)
    s.text(X + 0.7, h - 1.28, f'{len(tr)} homes for training', size=24, weight='bold', ha='left')
    s.text(X + 0.7, h - 1.78, 'the line learns from these', size=18, ha='left', color=BODY)
    s.box(X, h - 3.2, 0.45, 0.45, '', fill=GOLD, lw=2, r=0.03)
    s.text(X + 0.7, h - 2.78, f'{len(te)} homes for testing', size=24, weight='bold', ha='left')
    s.text(X + 0.7, h - 3.28, 'it never sees these while it learns', size=18, ha='left', color=BODY)
    s.text(X, 0.85, 'The gold squares were picked by a shuffle,\nso they are spread across the whole list.', size=18, ha='left', color=BODY)
    return s


@fig('ml_shuffle_cut')
def ml_shuffle_cut(w, h, **_):
    d = homes()
    n = len(d)
    tr, te = split_idx(n, 0.25, 7)
    perm = np.random.RandomState(7).permutation(n)
    s = Scene(w, h)
    cw = (w - 0.6) / n
    x0 = 0.3
    def strip(y, golds, text):
        for i in range(n):
            s.rect(x0 + i * cw, y, cw, 0.5, fill=GOLD if i in golds else PAPER, edge=INK, lw=0.5)
        s.text(x0, y + 0.8, text, size=19, weight='bold', ha='left')
    strip(h - 1.2, set(), '1. the homes in file order, number 1 to 120')
    s.arrow(w / 2, h - 1.35, w / 2, h - 2.15, color=RED, lw=2.4, head=16)
    s.text(w / 2 + 0.2, h - 1.75, 'shuffle, with random_state=7', size=17, ha='left', color=RED, weight='bold')
    strip(h - 3.45, set(range(len(te))), '2. shuffled, then cut after 30')
    s.brace(x0, x0 + len(te) * cw, h - 3.55, depth=0.15, up=False)
    s.text(x0 + len(te) * cw / 2, h - 4.1, 'test\n30', size=17, weight='bold', ha='center')
    s.brace(x0 + len(te) * cw + 0.03, x0 + n * cw, h - 3.55, depth=0.15, up=False)
    s.text(x0 + len(te) * cw + (n - len(te)) * cw / 2, h - 4.1, 'train: the other 90', size=17, weight='bold')
    s.text(w - 0.3, 0.2, 'first three in the shuffle: homes ' + ', '.join(str(int(v) + 1) for v in perm[:3]), size=14, color=MUTE, ha='right', va='bottom')
    return s


@fig('ml_four_names')
def ml_four_names(w, h, **_):
    d, tr, te, y, pred, base, beta = homes_split()
    s = Scene(w, h)
    cw, ch = 2.45, 1.2
    x0 = 1.9
    top = h - 0.95
    s.text(x0 + cw / 2, h - 0.45, 'training', size=21, weight='bold')
    s.text(x0 + cw + 0.3 + cw / 2, h - 0.45, 'testing', size=21, weight='bold')
    s.text(0.95, top - ch / 2, 'inputs\n(features)', size=19, weight='bold')
    s.text(0.95, top - ch - 0.3 - ch / 2, 'answers\n(target)', size=19, weight='bold')
    cells = [(0, 0, 'X_train', f'({len(tr)}, 2)', False), (0, 1, 'X_test', f'({len(te)}, 2)', True), (1, 0, 'y_train', f'({len(tr)},)', False), (1, 1, 'y_test', f'({len(te)},)', True)]
    for r, c, name, shp, test in cells:
        x = x0 + c * (cw + 0.3)
        yb = top - ch - r * (ch + 0.3)
        s.box(x, yb, cw, ch, '', fill=GOLD if test else PAPER, lw=2, r=0.05)
        s.text(x + cw / 2, yb + ch / 2 + 0.2, name, size=22, weight='bold', mono=True)
        s.text(x + cw / 2, yb + ch / 2 - 0.27, f'shape {shp}', size=17, mono=True)
    s.text(w / 2, 0.4, 'Four names on the left of the equals sign\ncatch these four pieces, in this order.', size=16, color=MUTE)
    return s


def _gap_panel(s, x0, y0, wd, ht, x, y, pred, color, title, score):
    ax = axes_in(s, x0, y0, wd, ht)
    for xi, yi, pi in zip(x, y, pred):
        ax.plot([xi, xi], [yi, pi], color=INK, lw=1.8, zorder=2)
    ax.scatter(x, y, s=60, facecolor=GOLD, edgecolor=INK, linewidth=1.4, zorder=4)
    ax.scatter(x, pred, s=28, facecolor=color, edgecolor=color, zorder=3)
    ax.set_xticks([])
    ax.set_yticks([])
    return ax


@fig('ml_mae_test_baseline')
def ml_mae_test_baseline(w, h, **_):
    d, tr, te, y, pred, base, beta = homes_split()
    s = Scene(w, h)
    ax = _gap_panel(s, 0.3, 1.35, w - 0.6, h - 2.5, d['area_m2'].values[te], y[te], base, GREY, '', 0)
    ax.axhline(base[0], color=RED, lw=2.6, zorder=1)
    s.text(w / 2, h - 0.4, 'plain guess: the training mean', size=20, weight='bold')
    s.text(w / 2, 0.8, money(mae(y[te], base)), size=30, weight='bold', mono=True)
    s.text(w / 2, 0.35, 'average miss on 30 unseen homes (UGX)', size=16, color=MUTE)
    return s


@fig('ml_mae_test_model')
def ml_mae_test_model(w, h, **_):
    d, tr, te, y, pred, base, beta = homes_split()
    s = Scene(w, h)
    _gap_panel(s, 0.3, 1.35, w - 0.6, h - 2.5, d['area_m2'].values[te], y[te], pred, INK, '', 0)
    s.text(w / 2, h - 0.4, 'the fitted model', size=20, weight='bold')
    s.text(w / 2, 0.8, money(mae(y[te], pred)), size=30, weight='bold', mono=True)
    s.text(w / 2, 0.35, 'average miss on 30 unseen homes (UGX)', size=16, color=MUTE)
    return s


def bars_compare(s, items, x0, y0, wd, ht, unit_note='', vmax=None, label_size=20):
    """items: list of (label, value, kind) kind in '', 'gold', 'red'. Horizontal bars with the value at the end."""
    vmax = vmax or max(v for _, v, _ in items)
    n = len(items)
    bh = ht / n * 0.6
    for i, (lab, v, kind) in enumerate(items):
        y = y0 + ht - (i + 1) * ht / n + (ht / n - bh) / 2
        L = (v / vmax) * (wd - 2.6 - 1.7)
        s.rect(x0 + 2.6, y, max(L, 0.02), bh, fill=GOLD if kind == 'gold' else (PAPER if kind != 'red' else PAPER), edge=RED if kind == 'red' else INK, lw=3 if kind == 'red' else 2)
        s.text(x0 + 2.45, y + bh / 2, lab, size=label_size, ha='right', weight='bold' if kind == 'gold' else 'normal', color=RED if kind == 'red' else INK)
        s.text(x0 + 2.6 + L + 0.15, y + bh / 2, money(v), size=22, weight='bold', ha='left', color=RED if kind == 'red' else INK)
    if unit_note:
        s.text(x0 + 2.6, y0 - 0.3, unit_note, size=16, color=MUTE, ha='left')


@fig('ml_homes_score_bars')
def ml_homes_score_bars(w, h, **_):
    d, tr, te, y, pred, base, beta = homes_split()
    s = Scene(w, h)
    bars_compare(s, [('plain guess', mae(y[te], base), ''), ('fitted model', mae(y[te], pred), 'gold')], 0.3, 1.0, w - 0.6, h - 1.6, 'average miss on 30 unseen homes, in UGX; smaller is better')
    return s


@fig('ml_seed_dice')
def ml_seed_dice(w, h, **_):
    d = homes()
    Xc = d[['area_m2', 'rooms']].values.astype(float)
    y = d['rent_ugx'].values.astype(float)
    res = []
    for seed in range(1, 11):
        tr, te = split_idx(len(d), 0.25, seed)
        b = ols(Xc[tr], y[tr])
        res.append(mae(y[te], predict(b, Xc[te])))
    s = Scene(w, h)
    ax = axes_in(s, 1.4, 1.0, w - 1.8, h - 2.1)
    xs = list(range(1, 11))
    best = int(np.argmin(res))
    ax.scatter(xs, res, s=240, facecolor=[GOLD if i == 6 else PAPER for i in range(10)], edgecolor=INK, linewidth=2.2, zorder=3)
    ax.scatter([xs[best]], [res[best]], s=360, facecolor='none', edgecolor=RED, linewidth=3.2, zorder=4)
    ax.axhline(np.mean(res), color=GREY, lw=2, ls='--')
    ax.set_xticks(xs)
    ax.set_xlabel('random_state', fontsize=17)
    ax.set_ylabel('average miss (UGX)', fontsize=17)
    lo, hi = min(res), max(res)
    ax.set_ylim(lo - (hi - lo) * 0.6, hi + (hi - lo) * 0.6)
    ax.tick_params(labelsize=15)
    s.text(w / 2, h - 0.35, 'the same model, ten different shuffles', size=20, weight='bold')
    s.text(w - 0.3, 0.2, f'our seed 7: {money(res[6])}.  Lucky seed {xs[best]}: {money(res[best])}.  Typical: {money(np.mean(res))}.', size=15, color=RED, weight='bold', ha='right', va='bottom')
    return s


# ================================================================== SESSION 16: decision trees
PETAL = {'setosa': (1.0, 1.9), 'versicolor': (3.0, 5.1), 'virginica': (4.5, 6.9)}  # published iris ranges, petal length in cm


@fig('ml_petal_ranges')
def ml_petal_ranges(w, h, **_):
    s = Scene(w, h)
    x0, x1 = 2.6, w - 0.6
    sc = (x1 - x0) / 7.0
    X = lambda v: x0 + v * sc
    ys = {'setosa': h - 1.2, 'versicolor': h - 2.05, 'virginica': h - 2.9}
    fills = {'setosa': PAPER, 'versicolor': GOLD, 'virginica': '#BDBDBD'}
    for sp, (lo, hi) in PETAL.items():
        s.rect(X(lo), ys[sp] - 0.3, (hi - lo) * sc, 0.6, fill=fills[sp], lw=2)
        s.text(2.4, ys[sp], sp, size=22, weight='bold', ha='right')
        s.text(X(lo) - 0.1, ys[sp] - 0.5, f'{lo:g}', size=15, color=MUTE, ha='right')
        s.text(X(hi) + 0.1, ys[sp] - 0.5, f'{hi:g}', size=15, color=MUTE, ha='left')
    s.line(x0, 0.75, x1, 0.75, lw=2)
    for v in range(0, 8):
        s.line(X(v), 0.75, X(v), 0.63, lw=1.6)
        s.text(X(v), 0.4, str(v), size=17)
    s.text(x1 + 0.1, 0.4, 'cm', size=16, color=MUTE, ha='left')
    for t, name in [(2.5, 'rule: 2.5'), (4.8, 'rule: 4.8')]:
        s.line(X(t), 0.8, X(t), h - 0.75, color=RED, lw=3, dash=True, z=5)
        s.text(X(t), h - 0.4, name, size=19, weight='bold', color=RED)
    s.text(x1, h - 1.62, 'versicolor and virginica overlap from 4.5 to 5.1', size=16, color=RED, ha='right', weight='bold', bbox=dict(fc='white', ec='none', pad=2))
    return s


@fig('ml_tree_diagram')
def ml_tree_diagram(w, h, **_):
    s = Scene(w, h)

    def node(cx, cy, text, wd, ht=0.8, fill=PAPER):
        s.box(cx - wd / 2, cy - ht / 2, wd, ht, text, size=18, fill=fill, lw=2, r=0.07, weight='bold')
    node(2.9, h - 0.65, 'petal length <= 2.45 ?', 3.3)
    node(5.2, h - 2.35, 'petal width <= 1.75 ?', 3.3)
    node(1.1, 1.05, 'setosa', 1.9, 0.75)
    node(4.05, 1.05, 'versicolor', 2.1, 0.75, GOLD)
    node(6.5, 1.05, 'virginica', 1.9, 0.75, '#BDBDBD')
    s.arrow(2.3, h - 1.05, 1.2, 1.45, color=INK, lw=2.2, head=15)
    s.text(1.0, h - 2.2, 'yes', size=19, weight='bold', color=RED)
    s.arrow(3.7, h - 1.05, 4.7, h - 1.95, color=INK, lw=2.2, head=15)
    s.text(4.4, h - 1.35, 'no', size=19, weight='bold', color=RED)
    s.arrow(4.7, h - 2.75, 4.1, 1.45, color=INK, lw=2.2, head=15)
    s.text(3.95, h - 3.1, 'yes', size=19, weight='bold', color=RED)
    s.arrow(5.9, h - 2.75, 6.45, 1.45, color=INK, lw=2.2, head=15)
    s.text(6.45, h - 3.1, 'no', size=19, weight='bold', color=RED)
    s.text(1.1, 0.55, '50 flowers', size=15, color=MUTE)
    s.text(4.05, 0.55, '49 right, 5 wrong', size=15, color=MUTE)
    s.text(6.5, 0.55, '45 right, 1 wrong', size=15, color=MUTE)
    s.text(w / 2, 0.15, 'A classic tree for all 150 flowers. Yours may use slightly different numbers.', size=14, color=MUTE, va='bottom')
    return s


@fig('ml_zones_hand')
def ml_zones_hand(w, h, **_):
    s = Scene(w, h)
    x0, x1 = 0.4, w - 0.4
    sc = (x1 - x0) / 7.5
    X = lambda v: x0 + v * sc
    zones = [(0, 2.5, PAPER, 'setosa'), (2.5, 4.8, GOLD, 'versicolor'), (4.8, 7.5, '#BDBDBD', 'virginica')]
    for lo, hi, f, name in zones:
        s.rect(X(lo), 1.6, (hi - lo) * sc, 1.1, fill=f, lw=2)
        s.text(X((lo + hi) / 2), 2.15, name, size=18, weight='bold')
    for v in range(0, 8):
        s.line(X(v), 1.6, X(v), 1.45, lw=1.5)
        s.text(X(v), 1.2, str(v), size=15)
    s.text(w / 2, 0.7, 'petal length (cm)', size=16, color=MUTE)
    for t in (2.5, 4.8):
        s.line(X(t), 1.5, X(t), 3.0, color=RED, lw=3)
        s.text(X(t), 3.05, f'{t}', size=22, weight='bold', color=RED)
    s.text(w / 2, h - 0.3, 'my hand rule: two cuts', size=20, weight='bold')
    return s


@fig('ml_zones_tree')
def ml_zones_tree(w, h, **_):
    s = Scene(w, h)
    ax = axes_in(s, 1.0, 0.95, w - 1.3, h - 1.85)
    ax.set_xlim(0, 7.5)
    ax.set_ylim(0, 2.8)
    ax.axvspan(0, 2.45, color=PAPER, zorder=0)
    ax.add_patch(plt.Rectangle((2.45, 0), 5.05, 1.75, fc=GOLD, ec=INK, lw=2, zorder=1))
    ax.add_patch(plt.Rectangle((2.45, 1.75), 5.05, 1.05, fc='#BDBDBD', ec=INK, lw=2, zorder=1))
    ax.add_patch(plt.Rectangle((0, 0), 2.45, 2.8, fc=PAPER, ec=INK, lw=2, zorder=1))
    ax.text(1.2, 1.4, 'setosa', fontsize=16, fontweight='bold', ha='center', family=FONT)
    ax.text(4.9, 0.85, 'versicolor', fontsize=16, fontweight='bold', ha='center', family=FONT)
    ax.text(4.9, 2.3, 'virginica', fontsize=16, fontweight='bold', ha='center', family=FONT)
    ax.set_xlabel('petal length (cm)', fontsize=15)
    ax.set_ylabel('petal width (cm)', fontsize=15)
    ax.set_xticks([0, 2.45, 7])
    ax.set_xticklabels(['0', '2.45', '7'])
    ax.set_yticks([0, 1.75, 2.5])
    ax.set_yticklabels(['0', '1.75', '2.5'])
    ax.tick_params(labelsize=14)
    s.text(w / 2, h - 0.4, 'the tree: two cuts in two measurements', size=20, weight='bold')
    return s


@fig('ml_accuracy_tokens')
def ml_accuracy_tokens(w, h, **_):
    s = Scene(w, h)
    right = 9
    for i in range(10):
        cx = 0.7 + (i % 5) * 0.95
        cy = h - 0.9 - (i // 5) * 1.1
        s.icon('check' if i < right else 'cross', cx, cy, 0.9)
    s.text(5.6, h - 1.9, '9 right\n1 wrong', size=26, weight='bold', ha='left')
    s.box(0.4, 1.0, 6.6, 0.8, 'accuracy = right / all = 9 / 10', size=22, weight='bold', fill=GOLD, mono=True, r=0.05)
    s.text(0.4, 0.45, '= 0.9 = 90%   (a proportion times 100 is a percentage)', size=17, ha='left', color=BODY)
    return s


@fig('ml_majority_baseline')
def ml_majority_baseline(w, h, **_):
    s = Scene(w, h)
    for i, (sp, f) in enumerate([('setosa', GOLD), ('versicolor', PAPER), ('virginica', '#BDBDBD')]):
        x = 0.5 + i * 2.4
        for k in range(10):
            s.rect(x + (k % 5) * 0.34, h - 1.3 - (k // 5) * 0.34, 0.3, 0.3, fill=f, lw=1.3)
        s.text(x + 0.85, h - 2.25, sp, size=19, weight='bold')
        s.text(x + 0.85, h - 2.65, '50 flowers', size=16, color=MUTE)
    s.text(w / 2, h - 0.4, 'three species, equally common', size=19, weight='bold')
    s.box(0.5, 0.95, 6.7, 0.8, 'always guess "setosa": right 1 time in 3', size=20, weight='bold', r=0.05, edge=RED, color=RED)
    s.text(w / 2, 0.45, 'accuracy about 0.33. Any tree must beat this.', size=18, color=BODY)
    return s


@fig('ml_codes_names')
def ml_codes_names(w, h, **_):
    s = Scene(w, h)
    rows = [['code', 'species'], ['0', 'setosa'], ['1', 'versicolor'], ['2', 'virginica']]
    s.table(0.5, h - 0.6, [1.4, 2.6], 0.75, rows, size=24, hl_rows=(0,), hl_fill='#EDEDED')
    s.box(4.9, h - 3.0, 2.6, 1.5, '', fill=PAPER, edge=RED, lw=2.6, r=0.06)
    s.text(6.2, h - 1.85, '2 = 2 x 1 ?', size=26, weight='bold', color=RED, mono=True)
    s.line(5.15, h - 1.95, 7.25, h - 1.75, color=RED, lw=3.4)
    s.text(6.2, h - 2.6, 'No: a code is only\na name tag', size=18, weight='bold')
    s.text(w / 2, 0.55, 'The model returns a code. Use the names to read it.', size=18, color=BODY)
    return s


# ================================================================== SESSION 17: overfitting and fair comparison
def _overfit_data(n_train=8, seed=11, deg=7):
    d = fares()
    perm = np.random.RandomState(seed).permutation(len(d))
    tr = perm[:n_train]
    xtr, ytr = d['distance_km'].values[tr], d['fare_ugx'].values[tr].astype(float)
    order = np.argsort(xtr)
    xtr, ytr = xtr[order], ytr[order]
    rest = perm[n_train:]
    xte, yte = d['distance_km'].values[rest], d['fare_ugx'].values[rest].astype(float)
    keep = (xte > xtr.min()) & (xte < xtr.max())
    xte, yte = xte[keep], yte[keep]
    poly = np.polynomial.Polynomial.fit(xtr, ytr, deg)
    line = np.polynomial.Polynomial.fit(xtr, ytr, 1)
    return xtr, ytr, xte, yte, poly, line


@fig('ml_overfit_curve')
def ml_overfit_curve(w, h, **_):
    xtr, ytr, xte, yte, poly, line = _overfit_data()
    s = Scene(w, h)
    ax = axes_in(s, 1.3, 0.9, 6.6, h - 1.4)
    xs = np.linspace(xtr.min(), xtr.max(), 300)
    yy = poly(xs)
    yy = np.where((yy > -3000) & (yy < 30000), yy, np.nan)
    ax.plot(xs, yy, color=RED, lw=3.2, zorder=2)
    ax.plot(xs, line(xs), color=INK, lw=3, zorder=2)
    ax.scatter(xtr, ytr, s=170, facecolor=GOLD, edgecolor=INK, linewidth=2, zorder=4)
    ax.scatter(xte, yte, s=70, facecolor=PAPER, edgecolor=INK, linewidth=1.6, zorder=3)
    ax.set_ylim(-3000, 30000)
    ax.set_xlabel('distance (km)', fontsize=17)
    ax.set_ylabel('fare (UGX)', fontsize=17)
    ax.set_yticks([0, 10000, 20000, 30000])
    ax.set_yticklabels(['0', '10k', '20k', '30k'])
    ax.tick_params(labelsize=15)
    X = 8.3
    s.circle(X + 0.1, h - 0.8, 0.13, fill=GOLD, lw=2)
    s.text(X + 0.35, h - 0.8, '8 training trips', size=18, ha='left')
    s.circle(X + 0.1, h - 1.3, 0.09, fill=PAPER, lw=1.6)
    s.text(X + 0.35, h - 1.3, 'new trips', size=18, ha='left')
    s.line(X - 0.05, h - 2.0, X + 0.3, h - 2.0, color=RED, lw=3.4)
    s.text(X + 0.4, h - 2.0, 'curve through every\ntraining trip', size=17, ha='left', color=RED, weight='bold')
    s.text(X + 0.4, h - 2.75, f'training miss {mae(ytr, poly(xtr)):,.0f}\nnew trips miss {mae(yte, poly(xte)):,.0f}', size=16, ha='left', color=RED, mono=True)
    s.line(X - 0.05, h - 3.7, X + 0.3, h - 3.7, color=INK, lw=3.4)
    s.text(X + 0.4, h - 3.7, 'a plain line', size=17, ha='left', weight='bold')
    s.text(X + 0.4, h - 4.2, f'new trips miss {mae(yte, line(xte)):,.0f}', size=16, ha='left', mono=True)
    return s


@fig('ml_confusion_toy')
def ml_confusion_toy(w, h, **_):
    actual = [0, 0, 1, 1, 1]
    pred = [0, 1, 1, 0, 1]
    m = np.zeros((2, 2), int)
    for a, p in zip(actual, pred):
        m[a, p] += 1
    s = Scene(w, h)
    c = 1.3
    x0, y0 = 2.6, h - 1.75
    s.text(x0 + c, h - 0.4, 'predicted', size=21, weight='bold')
    s.text(x0 + c / 2, h - 1.15, 'no', size=19)
    s.text(x0 + 1.5 * c, h - 1.15, 'yes', size=19)
    s.text(0.75, y0 - c, 'actual', size=21, weight='bold')
    for r in range(2):
        s.text(x0 - 0.3, y0 - r * c - c / 2, ['no', 'yes'][r], size=19, ha='right')
        for k in range(2):
            s.box(x0 + k * c, y0 - (r + 1) * c, c, c, str(m[r, k]), size=38, fill=GOLD if r == k else PAPER, lw=2.4, r=0.03, weight='bold')
    s.text(x0 + c, y0 - 2 * c - 0.4, '3 right (the diagonal), 2 wrong', size=18, weight='bold')
    return s


@fig('ml_confusion_reading')
def ml_confusion_reading(w, h, **_):
    actual = [0, 0, 1, 1, 1]
    pred = [0, 1, 1, 0, 1]
    s = Scene(w, h)
    rows = [['', 'actual', 'predicted', '']] + [[str(i + 1), ['no', 'yes'][a], ['no', 'yes'][p], 'right' if a == p else 'wrong'] for i, (a, p) in enumerate(zip(actual, pred))]
    hl = {(i + 1, 3): GOLD for i, (a, p) in enumerate(zip(actual, pred)) if a == p}
    s.table(0.3, h - 0.5, [0.5, 1.2, 1.5, 1.2], 0.62, rows, size=19, hl_cells=hl, hl_rows=(0,), hl_fill='#EDEDED')
    s.text(5.1, h - 1.3, 'Each answer\nlands in one cell', size=19, weight='bold', ha='left')
    s.text(5.1, h - 2.4, 'row: what was true\ncolumn: what we said', size=17, ha='left')
    s.text(5.1, h - 3.4, 'Answer 2 was no,\nwe said yes: row no,\ncolumn yes.', size=16, ha='left', color=RED, weight='bold')
    return s


def poly_gap_data():
    d = fares()
    perm = np.random.RandomState(3).permutation(len(d))
    tr = perm[:12]
    xtr, ytr = d['distance_km'].values[tr], d['fare_ugx'].values[tr].astype(float)
    rest = perm[12:]
    xte, yte = d['distance_km'].values[rest], d['fare_ugx'].values[rest].astype(float)
    keep = (xte > xtr.min()) & (xte < xtr.max())
    xte, yte = xte[keep], yte[keep]
    out = []
    for deg in (1, 2, 4, 8, 11):
        p = np.polynomial.Polynomial.fit(xtr, ytr, deg)
        out.append((deg, mae(ytr, p(xtr)), mae(yte, p(xte))))
    return out


@fig('ml_complexity_gap')
def ml_complexity_gap(w, h, **_):
    res = poly_gap_data()
    s = Scene(w, h)
    ax = axes_in(s, 1.3, 1.15, w - 1.7, h - 2.2)
    xs = np.arange(len(res))
    tr = [r[1] for r in res]
    te = [r[2] for r in res]
    top = min(max(te), 3 * max(tr[0], te[0]))
    ax.bar(xs - 0.2, tr, 0.38, color=GOLD, edgecolor=INK, linewidth=2, label='training trips')
    ax.bar(xs + 0.2, np.minimum(te, top), 0.38, color=PAPER, edgecolor=INK, linewidth=2, label='new trips')
    for i, v in enumerate(te):
        if v > top:
            ax.text(xs[i] + 0.2, top, f'{v:,.0f}', ha='center', va='bottom', fontsize=14, fontweight='bold', color=RED, family=FONT)
    ax.set_xticks(xs)
    ax.set_xticklabels(['line', 'bend 1', 'bend 3', 'bend 7', 'bend 10'], fontsize=15)
    ax.set_ylim(0, top * 1.2)
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.legend(loc='upper left', fontsize=16)
    s.text(w / 2, h - 0.35, 'average miss (UGX): the more it bends, the better it remembers', size=17, weight='bold')
    s.text(w / 2, 0.4, 'The same idea as a tree with too many questions.', size=17, color=BODY)
    return s


@fig('ml_peek_test')
def ml_peek_test(w, h, **_):
    s = Scene(w, h)
    pts = [(2.0, h - 1.4, 'try a setting'), (5.7, h - 1.4, 'peek at the\nfinal test score'), (5.7, 1.5, 'change the setting\nto score higher'), (2.0, 1.5, 'repeat')]
    for x, y, t in pts:
        s.box(x - 1.3, y - 0.5, 2.6, 1.0, t, size=18, weight='bold', r=0.06, edge=RED if 'peek' in t else INK, color=RED if 'peek' in t else INK)
    s.arrow(3.4, h - 1.4, 4.3, h - 1.4, color=INK, lw=2.4, head=16)
    s.arrow(5.7, h - 1.95, 5.7, 2.05, color=INK, lw=2.4, head=16)
    s.arrow(4.3, 1.5, 3.4, 1.5, color=INK, lw=2.4, head=16)
    s.arrow(2.0, 2.05, 2.0, h - 1.95, color=INK, lw=2.4, head=16)
    s.icon('magnifier', 3.85, 3.4, 0.8)
    s.text(3.85, 2.55, 'the test turns\ninto practice', size=17, color=RED, weight='bold')
    return s


# ================================================================== SESSION 18: three-way split and the locked test
def lock_icon(s, x, y, size=0.6, color=INK):
    from matplotlib.patches import Wedge
    s.rect(x - 0.28 * size, y - 0.3 * size, 0.56 * size, 0.42 * size, fill=GOLD, lw=2.2)
    s.ax.add_patch(Wedge((x, y + 0.12 * size), 0.2 * size, 0, 180, width=0.06 * size, fc=INK, ec=INK, zorder=3))


@fig('ml_three_way_bar')
def ml_three_way_bar(w, h, unit='flowers', total=150, **_):
    s = Scene(w, h)
    parts = [('train', 90, PAPER, 'the model learns from these'), ('validation', 30, '#BDBDBD', 'choose the setting'), ('final test', 30, GOLD, 'locked until the end')]
    x0, wd = 0.4, w - 0.8
    xx = x0
    for name, n, f, note in parts:
        bw = wd * n / total
        s.rect(xx, h / 2 - 0.3, bw, 1.1, fill=f, lw=2.2)
        s.text(xx + bw / 2, h / 2 + 0.25, str(n), size=36, weight='bold')
        s.text(xx + bw / 2, h / 2 + 1.25, name, size=22, weight='bold')
        s.text(xx + bw / 2, h / 2 - 0.75, note, size=15, color=MUTE)
        xx += bw
    lock_icon(s, x0 + wd * 0.9 + 0.0, h / 2 - 1.5, 0.9)
    s.text(x0 + wd / 2, h - 0.35, f'{total} {unit} in all', size=20, weight='bold')
    return s


@fig('ml_three_way_bar_fares')
def ml_three_way_bar_fares(w, h, **_):
    return ml_three_way_bar(w, h, unit='trips', total=150)


@fig('ml_two_cuts')
def ml_two_cuts(w, h, **_):
    s = Scene(w, h)
    W = w - 1.0

    def bar(y, parts):
        x = 0.5
        for name, n, f in parts:
            bw = W * n / 150
            s.rect(x, y, bw, 0.62, fill=f, lw=2)
            s.text(x + bw / 2, y + 0.31, f'{name} {n}' if bw > 1.5 else str(n), size=17, weight='bold')
            x += bw
    y1, y2, y3 = h - 1.3, h - 2.75, 0.45
    s.text(0.5, y1 + 0.95, 'start: 150 flowers', size=18, weight='bold', ha='left')
    bar(y1, [('all', 150, PAPER)])
    s.arrow(1.6, y1 - 0.05, 1.6, y2 + 0.67, color=RED, lw=2.4, head=16)
    s.text(1.85, (y1 + y2 + 0.67) / 2, 'first cut: 30 flowers (20%)\nare locked away for the final test', size=16, ha='left', color=RED, weight='bold')
    s.text(0.5, y2 + 0.95, 'two parts', size=18, weight='bold', ha='left')
    bar(y2, [('development', 120, '#BDBDBD'), ('final test', 30, GOLD)])
    s.arrow(1.6, y2 - 0.05, 1.6, y3 + 0.67, color=RED, lw=2.4, head=16)
    s.text(1.85, (y2 + y3 + 0.67) / 2, 'second cut: 30 of the 120 (25%)\nbecome the validation part', size=16, ha='left', color=RED, weight='bold')
    bar(y3, [('train', 90, PAPER), ('validation', 30, '#BDBDBD'), ('final test', 30, GOLD)])
    return s


@fig('ml_stratify')
def ml_stratify(w, h, **_):
    s = Scene(w, h)
    cols = [PAPER, GOLD, '#BDBDBD']
    names = ['setosa', 'versicolor', 'virginica']
    for i, (nm, f) in enumerate(zip(names, cols)):
        s.rect(0.5 + i * 2.35, h - 0.85, 0.38, 0.38, fill=f, lw=1.8)
        s.text(1.0 + i * 2.35, h - 0.66, nm, size=17, ha='left')
    rows = [('train', 30), ('validation', 10), ('final test', 10)]
    unit = 0.085
    for r, (nm, k) in enumerate(rows):
        y = h - 2.0 - r * 1.15
        s.text(0.4, y + 0.3, nm, size=19, weight='bold', ha='left')
        x = 2.4
        for f in cols:
            bw = k * 0.055
            s.rect(x, y, bw, 0.6, fill=f, lw=2)
            s.text(x + bw / 2, y + 0.3, str(k), size=20, weight='bold')
            x += bw
    s.text(w / 2, 0.35, 'Every part holds each species in the same share.', size=18, weight='bold')
    return s


@fig('ml_choose_freeze_test')
def ml_choose_freeze_test(w, h, **_):
    s = Scene(w, h)
    cw = 2.5
    ys = h / 2
    s.box(0.2, ys + 0.2, 2.5, 0.65, 'baseline', size=19, weight='bold', r=0.05)
    s.box(0.2, ys - 0.7, 2.5, 0.65, 'tree, depth 1', size=19, weight='bold', r=0.05)
    s.box(0.2, ys - 1.6, 2.5, 0.65, 'tree, depth 3', size=19, weight='bold', r=0.05)
    s.text(1.45, ys + 1.2, 'score on validation', size=17, color=MUTE)
    for dy in (0.52, -0.38, -1.28):
        s.arrow(2.75, ys + dy, 3.5, ys - 0.35, color=INK, lw=1.8, head=12)
    s.box(3.55, ys - 0.85, 2.0, 1.0, 'pick the\nbest', size=19, weight='bold', r=0.05, fill=GOLD)
    s.arrow(5.6, ys - 0.35, 6.3, ys - 0.35, color=INK, lw=2.4, head=16)
    s.box(6.35, ys - 0.85, 1.9, 1.0, 'freeze it', size=19, weight='bold', r=0.05)
    lock_icon(s, 7.3, ys - 1.35, 0.5)
    s.arrow(8.3, ys - 0.35, 8.95, ys - 0.35, color=INK, lw=2.4, head=16)
    s.box(9.0, ys - 0.85, 1.6, 1.0, 'test\nonce', size=19, weight='bold', r=0.05, edge=RED, color=RED)
    s.arrow(10.65, ys - 0.35, 11.0, ys - 0.35, color=INK, lw=2.4, head=14)
    s.text(11.05, ys - 0.35, 'report', size=18, weight='bold', ha='left')
    s.text(w / 2, 0.45, 'The choice is made before the test is ever opened.', size=19, color=BODY)
    return s


@fig('ml_confusion_3x3')
def ml_confusion_3x3(w, h, **_):
    s = Scene(w, h)
    c = 0.95
    x0, y0 = 2.6, h - 1.45
    names = ['setosa', 'versicolor', 'virginica']
    s.text(x0 + 1.5 * c, h - 0.35, 'predicted', size=20, weight='bold')
    for k, nm in enumerate(names):
        s.text(x0 + k * c + c / 2, h - 0.95, nm, size=13)
        s.text(x0 - 0.15, y0 - k * c - c / 2, nm, size=14, ha='right')
    s.text(0.65, y0 - 1.5 * c, 'actual', size=20, weight='bold')
    for r in range(3):
        for k in range(3):
            s.box(x0 + k * c, y0 - (r + 1) * c, c, c, 'right' if r == k else 'mix-up', size=15, fill=GOLD if r == k else PAPER, lw=2, r=0.03, weight='bold' if r == k else 'normal', color=INK if r == k else MUTE)
        s.text(x0 + 3 * c + 0.1, y0 - r * c - c / 2, '= 10', size=16, ha='left', color=MUTE)
    s.text(x0 + 1.5 * c, y0 - 3 * c - 0.3, 'each row adds to 10: ten flowers of each species', size=14, color=BODY)
    return s


@fig('ml_checkpoint_two_list')
def ml_checkpoint_two_list(w, h, **_):
    s = Scene(w, h)
    items = ['the three split sizes', 'the baseline score', 'two validation scores', 'the chosen depth', 'the final test accuracy', 'the confusion matrix', 'two limitations']
    for i, t in enumerate(items):
        col, row = i // 4, i % 4
        x = 0.4 + col * 6.1
        y = h - 0.7 - row * 0.85
        s.icon('check', x + 0.3, y, 0.62)
        s.text(x + 0.8, y, t, size=23, ha='left')
    s.text(w / 2, 0.3, 'Seven pieces of evidence, all from one restarted notebook.', size=19, color=BODY)
    return s


# ================================================================== SESSIONS 19 to 22: the fares project
def fares_models():
    if 'fm' in _cache:
        return _cache['fm']
    d = fares()
    tr, va, te = three_way(len(d))
    y = d['fare_ugx'].values.astype(float)
    out = {'tr': tr, 'va': va, 'te': te, 'y': y, 'd': d, 'val': {}, 'beta': {}}
    sets = {'distance': ['distance_km'], 'three': ['distance_km', 'rush_hour', 'raining'], 'tip': ['distance_km', 'rush_hour', 'raining', 'tip_ugx']}
    out['base_val'] = mae(y[va], np.full(len(va), y[tr].mean()))
    out['base_test'] = mae(y[te], np.full(len(te), y[tr].mean()))
    for k, names in sets.items():
        X = d[names].values.astype(float)
        b = ols(X[tr], y[tr])
        out['beta'][k] = b
        out['val'][k] = mae(y[va], predict(b, X[va]))
        if k == 'three':
            out['test_three'] = mae(y[te], predict(b, X[te]))
    _cache['fm'] = out
    return out


@fig('ml_three_datasets')
def ml_three_datasets(w, h, **_):
    s = Scene(w, h)
    cards = [('synthetic_homes.csv', f'{len(homes())} homes', 'inputs: area_m2, rooms', 'target: rent_ugx', 'a number', 'shop'),
             ('synthetic_fares.csv', f'{len(fares())} boda-boda trips', 'inputs: distance_km,\nrush_hour, raining', 'target: fare_ugx', 'a number', 'bike'),
             ('iris flowers', '150 flowers', 'inputs: four measurements', 'target: species', 'a category', 'flower')]
    cw = (w - 0.4 - 0.8) / 3
    for i, (name, n, inp, tgt, kind, ic) in enumerate(cards):
        x = 0.2 + i * (cw + 0.4)
        cx = x + cw / 2
        s.box(x, 0.2, cw, h - 0.4, '', fill=PAPER, lw=2, r=0.06)
        if ic == 'flower':
            for k in range(5):
                a = k * 2 * math.pi / 5
                s.circle(cx + 0.24 * math.cos(a), h - 0.95 + 0.24 * math.sin(a), 0.17, fill=GOLD if k % 2 == 0 else PAPER, lw=2)
            s.circle(cx, h - 0.95, 0.12, fill=INK)
        else:
            s.icon(ic, cx, h - 0.95, 0.85)
        s.text(cx, h - 1.6, name, size=20, weight='bold')
        s.text(cx, h - 2.0, n, size=17, color=MUTE)
        s.text(cx, 1.45, inp, size=16)
        s.text(cx, 0.95, tgt, size=17, weight='bold', color=RED)
        s.text(cx, 0.5, f'the answer is {kind}', size=15, color=MUTE)
    return s


@fig('ml_fares_correlation')
def ml_fares_correlation(w, h, **_):
    d = fares()
    names = ['tip_ugx', 'distance_km', 'raining', 'rush_hour']
    r = {n: float(np.corrcoef(d[n], d['fare_ugx'])[0, 1]) for n in names}
    s = Scene(w, h)
    ax = axes_in(s, 2.3, 0.95, w - 2.7, h - 2.2)
    ys = np.arange(len(names))[::-1]
    for y_, n in zip(ys, names):
        ax.barh(y_, r[n], height=0.55, color=GOLD if n == 'distance_km' else PAPER, edgecolor=RED if n == 'tip_ugx' else INK, linewidth=3 if n == 'tip_ugx' else 2)
        ax.text(r[n] + (0.04 if r[n] >= 0 else -0.04), y_, f'{r[n]:.2f}', va='center', ha='left' if r[n] >= 0 else 'right', fontsize=19, fontweight='bold', family=FONT)
    ax.set_yticks(ys)
    ax.set_yticklabels(names, fontsize=16, family='DejaVu Sans Mono')
    ax.axvline(0, color=INK, lw=1.6)
    ax.set_xlim(-0.3, 1.2)
    ax.set_xticks([0, 0.5, 1.0])
    ax.tick_params(axis='x', labelsize=15)
    ax.set_xlabel('correlation with fare_ugx', fontsize=16)
    s.text(w / 2, h - 0.3, 'which column moves with the fare?', size=20, weight='bold')
    s.text(w / 2, h - 0.8, 'tip_ugx is highest, but it is known only after the trip', size=16, color=RED, weight='bold')
    return s


@fig('ml_trip_timeline')
def ml_trip_timeline(w, h, **_):
    s = Scene(w, h)
    y = h / 2 - 0.2
    s.arrow(0.2, y, w - 0.2, y, color=INK, lw=3, head=22)
    xs = [1.5, w / 2, w - 1.5]
    stations = [(xs[0], 'booking', 'distance_km\nrush_hour\nraining', 'check', GOLD, INK), (xs[1], 'ride ends', 'fare_ugx\nthe target', 'coin', PAPER, INK), (xs[2], 'afterwards', 'tip_ugx', 'cross', PAPER, RED)]
    for x, t, sub, ic, f, col in stations:
        s.circle(x, y, 0.13, fill=INK, z=5)
        s.box(x - 1.2, y + 0.45, 2.4, 1.95, '', fill=f, lw=2.2, r=0.06, edge=col)
        s.text(x, y + 2.05, t, size=19, weight='bold', color=col)
        s.text(x, y + 1.25, sub, size=16, mono=True, color=col)
        s.icon(ic, x, y - 0.75, 0.55)
    s.text(xs[0], y - 1.45, 'known: inputs', size=17, weight='bold')
    s.text(xs[1], y - 1.45, 'the answer', size=17, weight='bold')
    s.text(xs[2], y - 1.45, 'too late to use', size=17, weight='bold', color=RED)
    return s


@fig('ml_plan_storyboard')
def ml_plan_storyboard(w, h, **_):
    s = Scene(w, h)
    rows = [('Question', 'Can distance, rush hour and rain predict a boda-boda fare?'), ('Dataset', 'synthetic_fares.csv, 150 invented trips'), ('Target', 'fare_ugx'),
            ('Inputs', 'distance_km, rush_hour, raining. Not tip_ugx.'), ('Baseline', 'the mean fare of the training trips'), ('Evaluation', 'mean absolute error in UGX, final test used once'), ('Limits', 'invented data, so no claim about real fares')]
    s.box(0.2, 0.15, w - 0.4, h - 0.3, '', fill=PAPER, lw=2, r=0.04)
    pitch = (h - 0.6) / len(rows)
    for i, (a, b) in enumerate(rows):
        y = h - 0.3 - pitch * (i + 0.5)
        s.text(0.55, y, a, size=19, weight='bold', ha='left', color=RED if a == 'Limits' else INK)
        s.text(2.6, y, b, size=19, ha='left')
        if i < len(rows) - 1:
            s.line(0.45, y - pitch / 2, w - 0.45, y - pitch / 2, color=HAIR, lw=1.2)
    return s


@fig('ml_plan_sizes')
def ml_plan_sizes(w, h, **_):
    s = Scene(w, h)
    x0 = (w - 5.7) / 2
    for i, (ttl, q, ok) in enumerate([('fits two weeks', 'Can distance and rush hour\npredict a boda-boda fare?', True), ('too big', 'Can a computer predict\neverything about Kampala?', False)]):
        x = x0 + i * 2.95
        cx = x + 1.375
        s.box(x, 0.4, 2.75, h - 0.8, '', fill=PAPER, lw=2.2, r=0.06, edge=INK if ok else RED)
        s.icon('check' if ok else 'cross', cx, h - 1.1, 0.8)
        s.text(cx, h - 1.9, ttl, size=19, weight='bold', color=INK if ok else RED)
        s.text(cx, h / 2 - 0.3, q, size=15)
        s.text(cx, 0.9, 'a number answers it' if ok else 'no data, no number', size=14, color=MUTE)
    return s


@fig('ml_fare_baseline_gaps')
def ml_fare_baseline_gaps(w, h, **_):
    m = fares_models()
    d, tr, va, y = m['d'], m['tr'], m['va'], m['y']
    mean = y[tr].mean()
    s = Scene(w, h)
    ax = axes_in(s, 1.4, 0.9, 7.3, h - 1.6)
    xv = d['distance_km'].values[va]
    yv = y[va]
    ax.axhline(mean, color=RED, lw=3.2, zorder=2)
    for xi, yi in zip(xv, yv):
        ax.plot([xi, xi], [yi, mean], color=INK, lw=1.8, zorder=2)
    ax.scatter(xv, yv, s=90, facecolor=GOLD, edgecolor=INK, linewidth=1.6, zorder=4)
    ax.set_xlabel('distance (km)', fontsize=17)
    ax.set_ylabel('fare (UGX)', fontsize=17)
    ax.set_yticks([0, 10000, 20000])
    ax.set_yticklabels(['0', '10k', '20k'])
    ax.tick_params(labelsize=15)
    s.text(5.0, h - 0.3, '30 validation trips and the plain guess', size=19, weight='bold')
    X = 9.2
    s.line(X, h - 1.2, X + 0.6, h - 1.2, color=RED, lw=3.4)
    s.text(X + 0.75, h - 1.2, f'always {money(mean)}', size=18, ha='left', weight='bold', color=RED)
    s.text(X, h - 1.8, 'the training mean', size=17, ha='left', color=BODY)
    s.box(X, h - 3.15, 2.4, 0.95, money(m['base_val']), size=32, fill=GOLD, weight='bold', r=0.05, mono=True)
    s.text(X, h - 3.5, 'average miss, UGX', size=16, ha='left', color=MUTE)
    return s


@fig('ml_train_only_mean')
def ml_train_only_mean(w, h, **_):
    s = Scene(w, h)
    s.text(0.5, h - 0.5, 'right', size=22, weight='bold', ha='left')
    s.rect(0.5, h - 1.5, 3.2, 0.6, fill=PAPER, lw=2)
    s.text(2.1, h - 1.2, 'train 90', size=17, weight='bold')
    s.rect(3.7, h - 1.5, 1.0, 0.6, fill='#BDBDBD', lw=2)
    s.rect(4.7, h - 1.5, 1.0, 0.6, fill=GOLD, lw=2)
    s.arrow(2.1, h - 1.6, 2.1, h - 2.15, color=INK, lw=2.4, head=16)
    s.text(2.1, h - 2.45, 'mean of these 90', size=17, weight='bold')
    s.icon('check', 6.8, h - 1.2, 0.7)
    s.text(0.5, 1.95, 'wrong', size=22, weight='bold', ha='left', color=RED)
    s.rect(0.5, 0.95, 3.2, 0.6, fill=PAPER, edge=RED, lw=2)
    s.rect(3.7, 0.95, 1.0, 0.6, fill='#BDBDBD', edge=RED, lw=2)
    s.rect(4.7, 0.95, 1.0, 0.6, fill=GOLD, edge=RED, lw=2)
    s.text(3.1, 0.55, 'mean of all 150: it has peeked at the test trips', size=16, weight='bold', color=RED)
    s.icon('cross', 6.8, 1.25, 0.7)
    return s


@fig('ml_scatter_read')
def ml_scatter_read(w, h, **_):
    d = fares()
    row = d.iloc[2]
    s = Scene(w, h)
    ax = axes_in(s, 1.4, 1.0, w - 1.9, h - 1.7)
    ax.scatter(d['distance_km'], d['fare_ugx'], s=40, facecolor=PAPER, edgecolor=INK, linewidth=1.3, zorder=2)
    ax.scatter([row['distance_km']], [row['fare_ugx']], s=300, facecolor=GOLD, edgecolor=INK, linewidth=2.4, zorder=4)
    ax.plot([row['distance_km']] * 2, [0, row['fare_ugx']], color=RED, lw=2.4, ls='--', zorder=3)
    ax.plot([0, row['distance_km']], [row['fare_ugx']] * 2, color=RED, lw=2.4, ls='--', zorder=3)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 26000)
    ax.set_xlabel('distance (km): across', fontsize=17)
    ax.set_ylabel('fare (UGX): up', fontsize=17)
    ax.set_yticks([0, 10000, 20000])
    ax.set_yticklabels(['0', '10k', '20k'])
    ax.tick_params(labelsize=15)
    ax.text(0.5, 25500, f'the gold dot: {row["distance_km"]} km, {int(row["fare_ugx"]):,} UGX', fontsize=16, fontweight='bold', va='top', family=FONT)
    s.text(w / 2, h - 0.35, 'each dot is one trip', size=20, weight='bold')
    return s


@fig('ml_fare_scatter')
def ml_fare_scatter(w, h, **_):
    m = fares_models()
    d, tr, y = m['d'], m['tr'], m['y']
    x = d['distance_km'].values[tr]
    yy = y[tr]
    r = float(np.corrcoef(x, yy)[0, 1])
    s = Scene(w, h)
    ax = axes_in(s, 1.4, 1.0, w - 1.9, h - 1.7)
    ax.scatter(x, yy, s=70, facecolor=PAPER, edgecolor=INK, linewidth=1.6, zorder=3)
    b = ols(x.reshape(-1, 1), yy)
    xs = np.array([x.min(), x.max()])
    ax.plot(xs, b[0] + b[1] * xs, color=RED, lw=3, zorder=2)
    ax.set_xlabel('distance (km)', fontsize=17)
    ax.set_ylabel('fare (UGX)', fontsize=17)
    ax.set_yticks([0, 10000, 20000])
    ax.set_yticklabels(['0', '10k', '20k'])
    ax.tick_params(labelsize=15)
    s.text(w / 2, h - 0.35, f'90 training trips, correlation {r:.2f}', size=20, weight='bold')
    return s


@fig('ml_bar_to_beat')
def ml_bar_to_beat(w, h, **_):
    m = fares_models()
    s = Scene(w, h)
    bars_compare(s, [('plain guess', m['base_val'], 'gold')], 0.3, 1.4, w - 0.6, 2.0, 'validation miss in UGX')
    s.text(w / 2, h - 0.45, 'every model must score lower than this bar', size=20, weight='bold')
    return s


# ================================================================== SESSION 21: fair comparison
@fig('ml_fair_bars')
def ml_fair_bars(w, h, **_):
    m = fares_models()
    s = Scene(w, h)
    items = [('plain guess', m['base_val'], ''), ('distance only', m['val']['distance'], ''), ('distance, rush, rain', m['val']['three'], 'gold'), ('with the tip', m['val']['tip'], 'red')]
    ht = h - 1.2
    bars_compare(s, items, 0.3, 0.9, w - 0.6, ht, 'validation miss on 30 trips, in UGX; smaller is better')
    s.text(w - 0.4, 0.9 + ht / 8, 'not allowed: the tip is\nknown only after the trip', size=17, weight='bold', color=RED, ha='right')
    return s


@fig('ml_same_split')
def ml_same_split(w, h, **_):
    s = Scene(w, h)
    cands = ['plain guess', 'distance only', 'distance, rush, rain']
    for i, c in enumerate(cands):
        y = h - 1.1 - i * 1.1
        s.box(0.3, y - 0.35, 2.7, 0.7, c, size=17, weight='bold', r=0.05)
        s.arrow(3.05, y, 4.3, h / 2, color=INK, lw=1.8, head=12)
    s.box(4.35, h / 2 - 0.85, 1.75, 1.7, '', fill='#BDBDBD', lw=2.2, r=0.05)
    s.text(5.225, h / 2 + 0.4, 'the same', size=17, weight='bold')
    s.text(5.225, h / 2, '30 validation', size=16)
    s.text(5.225, h / 2 - 0.4, 'trips', size=16)
    s.arrow(6.15, h / 2, 6.7, h / 2, color=INK, lw=2.2, head=14)
    s.text(6.8, h / 2, 'one\nerror\nmeasure', size=15, weight='bold', ha='left')
    s.text(w / 2, 0.4, 'Same trips, same measure, so the scores compare fairly.', size=16, color=BODY)
    return s


@fig('ml_inputs_known')
def ml_inputs_known(w, h, **_):
    s = Scene(w, h)
    rows = [('distance_km', 'known at booking', True), ('rush_hour', 'known at booking', True), ('raining', 'known at booking', True), ('tip_ugx', 'known only afterwards', False)]
    for i, (n, why, ok) in enumerate(rows):
        y = h - 0.8 - i * 1.0
        s.icon('check' if ok else 'cross', 0.8, y, 0.75)
        s.text(1.6, y + 0.15, n, size=21, mono=True, ha='left', weight='bold', color=INK if ok else RED)
        s.text(1.6, y - 0.3, why, size=16, ha='left', color=MUTE if ok else RED)
    s.text(w / 2, 0.4, 'For each input ask: did we know it before the answer?', size=17, weight='bold')
    return s


@fig('ml_assistant_loop')
def ml_assistant_loop(w, h, **_):
    s = Scene(w, h)
    ty, by = h - 1.1, 1.3
    boxes = [('ask', 1.3, ty), ('predict what\nthe hint does', 4.0, ty), ('run it', 6.4, ty), ('test it\nwith asserts', 6.4, by), ('keep or reject,\nlog it', 3.7, by)]
    for t, x, y in boxes:
        s.box(x - 0.95, y - 0.5, 1.9, 1.0, t, size=16, weight='bold', r=0.06, fill=GOLD if 'test' in t else PAPER)
    s.arrow(2.3, ty, 3.0, ty, color=INK, lw=2.2, head=14)
    s.arrow(5.0, ty, 5.4, ty, color=INK, lw=2.2, head=14)
    s.arrow(6.4, ty - 0.55, 6.4, by + 0.55, color=INK, lw=2.2, head=14)
    s.arrow(5.4, by, 4.7, by, color=INK, lw=2.2, head=14)
    s.text(2.6, h / 2 + 0.05, 'A plausible answer\nis not a checked answer.', size=18, weight='bold', color=RED)
    return s


@fig('ml_total_bug')
def ml_total_bug(w, h, side='plus', **_):
    s = Scene(w, h)
    op, res, ok, note = ('+', '2003', False, 'plus adds the numbers') if side == 'plus' else ('*', '6000', True, 'times gives the price of 3')
    s.code(0.2, h - 0.25, ['def total(price, quantity):', f'    return price {op} quantity', '', 'total(2000, 3)'], size=14, line_h=0.3, pad=0.15, w=w - 0.4)
    s.text(1.7, 1.45, res, size=38, weight='bold', mono=True, color=INK if ok else RED)
    s.icon('check' if ok else 'cross', w - 1.0, 1.45, 0.65)
    s.text(w / 2, 0.55, note, size=17, color=BODY)
    return s


@fig('ml_decision_card')
def ml_decision_card(w, h, **_):
    m = fares_models()
    s = Scene(w, h)
    s.box(0.25, 0.25, w - 0.5, h - 0.5, '', fill=PAPER, lw=2.4, r=0.05)
    s.text(0.65, h - 0.8, 'Decision', size=24, weight='bold', ha='left')
    s.text(0.65, h - 1.8, 'I keep distance, rush hour and\nrain as inputs.', size=20, ha='left')
    s.text(0.65, h - 2.9, f'Validation error {money(m["val"]["three"])} UGX,\nagainst {money(m["base_val"])} for the plain guess.', size=20, ha='left')
    s.text(0.65, h - 4.0, 'I leave out tip_ugx: it is known\nonly after the trip.', size=20, ha='left', color=RED, weight='bold')
    return s


# ================================================================== SESSION 22: the final test
@fig('ml_final_test_bars')
def ml_final_test_bars(w, h, **_):
    m = fares_models()
    s = Scene(w, h)
    bars_compare(s, [('plain guess', m['base_test'], ''), ('frozen model', m['test_three'], 'gold')], 0.3, 1.0, w - 0.6, h - 1.6, 'average miss on the 30 locked trips, in UGX')
    return s


@fig('ml_open_once')
def ml_open_once(w, h, **_):
    s = Scene(w, h)
    s.box(0.4, 1.3, 2.5, 2.3, '', fill=GOLD, lw=2.4, r=0.06)
    lock_icon(s, 1.65, 2.75, 1.5)
    s.text(1.65, 1.7, '30 locked trips', size=17, weight='bold')
    s.arrow(3.0, 2.45, 4.1, 2.45, color=RED, lw=2.6, head=18)
    s.text(3.55, 2.9, 'open once', size=16, weight='bold', color=RED)
    s.box(4.2, 1.6, 3.0, 1.7, '', fill=PAPER, lw=2.2, r=0.06)
    s.text(5.7, 2.75, 'one number', size=22, weight='bold')
    s.text(5.7, 2.15, 'reported as it is', size=17)
    s.text(w / 2, 0.6, 'No second look, no tuning afterwards.', size=18, color=BODY)
    return s


@fig('ml_val_vs_test')
def ml_val_vs_test(w, h, **_):
    m = fares_models()
    s = Scene(w, h)
    ax = axes_in(s, 0.9, 1.0, w - 1.3, h - 2.2)
    x = np.arange(2)
    base = [m['base_val'], m['base_test']]
    mod = [m['val']['three'], m['test_three']]
    b1 = ax.bar(x - 0.2, base, 0.36, color=PAPER, edgecolor=INK, linewidth=2, label='plain guess')
    b2 = ax.bar(x + 0.2, mod, 0.36, color=GOLD, edgecolor=INK, linewidth=2, label='model')
    for bars, vals in ((b1, base), (b2, mod)):
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 60, f'{v:,.0f}', ha='center', va='bottom', fontsize=16, fontweight='bold', family=FONT)
    ax.set_xticks(x)
    ax.set_xticklabels(['validation trips', 'final test trips'], fontsize=16)
    ax.set_ylim(0, 6200)
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.legend(loc='upper right', fontsize=16, frameon=False)
    s.text(w / 2, h - 0.4, 'average miss (UGX)', size=20, weight='bold')
    s.text(w / 2, 0.3, 'The lead is smaller on the test, and that is normal.', size=16, color=BODY)
    return s


@fig('ml_handover_checklist')
def ml_handover_checklist(w, h, **_):
    s = Scene(w, h)
    items = [('folder', 'the data file sits beside the notebook'), ('clock', 'Restart and Run All works from the top'), ('notebook', 'the data origin is stated, and it is invented'), ('magnifier', 'validation and final test are reported apart'), ('check', 'limits are written next to the result')]
    pitch = (h - 0.4) / len(items)
    for i, (ic, t) in enumerate(items):
        y = h - 0.2 - pitch * (i + 0.5)
        s.icon(ic, 0.9, y, 0.6)
        s.text(1.7, y, t, size=22, ha='left')
    return s


@fig('ml_one_page_report')
def ml_one_page_report(w, h, **_):
    s = Scene(w, h)
    s.box(0.4, 0.2, 5.0, h - 0.4, '', fill=PAPER, lw=2.4, r=0.03)
    heads = ['Question', 'Data and method', 'Result, with the baseline', 'Limit', 'Next step']
    pitch = (h - 0.6) / len(heads)
    for i, name in enumerate(heads):
        y = h - 0.5 - i * pitch
        s.text(0.75, y, name, size=18, weight='bold', ha='left')
        for k in range(2):
            s.line(0.75, y - 0.3 - k * 0.2, 5.05, y - 0.3 - k * 0.2, color=HAIR, lw=1.8, z=4)
    s.text(w - 0.3, h / 2, 'one page,\nfive parts', size=19, weight='bold', ha='right')
    return s


# ================================================================== SESSIONS 23 and 24: showcase (guide mode)
@fig('ml_parent_five_slides')
def ml_parent_five_slides(w, h, **_):
    s = Scene(w, h)
    cards = [('1', 'Question', 'distance, rush hour\nand rain: a fare?'), ('2', 'Data', '150 invented trips'), ('3', 'Test', 'a plain guess,\nthen the model'),
             ('4', 'Result', 'the error in UGX,\nnext to the baseline'), ('5', 'Limit', 'what it cannot tell')]
    cw, gap = 2.05, 0.32
    x0 = (w - (5 * cw + 4 * gap)) / 2
    for i, (n, t, sub) in enumerate(cards):
        x = x0 + i * (cw + gap)
        s.box(x, h / 2 - 1.1, cw, 2.1, '', fill=GOLD if t == 'Result' else PAPER, lw=2.2, r=0.04, edge=RED if t == 'Limit' else INK)
        s.text(x + cw / 2, h / 2 + 0.6, t, size=21, weight='bold', color=RED if t == 'Limit' else INK)
        s.text(x + cw / 2, h / 2 - 0.2, sub, size=14)
        if i < 4:
            s.arrow(x + cw + 0.03, h / 2, x + cw + gap - 0.03, h / 2, lw=2, head=12)
    s.text(w / 2, h / 2 - 1.75, 'five slides, five minutes, no jargon', size=19, weight='bold')
    return s


@fig('ml_claim_evidence')
def ml_claim_evidence(w, h, **_):
    m = fares_models()
    s = Scene(w, h)
    s.box(0.3, h - 1.6, w - 0.6, 1.1, '', fill=GOLD, lw=2.2, r=0.05)
    s.text(w / 2, h - 0.8, 'Claim: the model guesses fares better than a plain guess.', size=18, weight='bold')
    s.arrow(w / 2, h - 1.65, w / 2, h - 2.25, lw=2.2, head=14)
    s.box(0.3, 0.9, 3.4, 1.9, '', lw=2.2, r=0.05)
    s.text(2.0, 2.35, 'evidence one', size=16, weight='bold')
    s.text(2.0, 1.55, f'plain guess misses by\n{money(m["base_test"])} UGX', size=17)
    s.box(4.0, 0.9, 3.4, 1.9, '', lw=2.2, r=0.05)
    s.text(5.7, 2.35, 'evidence two', size=16, weight='bold')
    s.text(5.7, 1.55, f'the model misses by\n{money(m["test_three"])} UGX', size=17)
    s.text(w / 2, 0.4, 'Say the claim, then show the numbers that support it.', size=16, color=BODY)
    return s


@fig('ml_audience_cards')
def ml_audience_cards(w, h, **_):
    s = Scene(w, h)
    rows = [('person', 'a parent', 'It guesses the fare from the distance.\nIt was tested on trips it never saw.'), ('laptop', 'a classmate', 'Linear regression with three inputs,\ncompared with a mean baseline.')]
    for i, (ic, who, say) in enumerate(rows):
        y = h - 1.5 - i * 1.85
        s.box(0.3, y - 0.7, w - 0.6, 1.6, '', lw=2.2, r=0.05)
        s.icon(ic, 1.1, y + 0.1, 0.9)
        s.text(1.9, y + 0.5, who, size=18, weight='bold', ha='left')
        s.text(1.9, y - 0.15, say, size=16, ha='left')
    s.text(w / 2, 0.3, 'The same finding, in the words your listener already has.', size=16, color=BODY)
    return s


@fig('ml_demo_backup')
def ml_demo_backup(w, h, **_):
    s = Scene(w, h)
    s.box(0.3, h - 2.1, 2.6, 1.6, 'live demo', size=19, weight='bold', r=0.05)
    s.arrow(3.0, h - 1.3, 4.2, h - 1.3, color=RED, lw=2.4, head=16)
    s.text(3.6, h - 0.95, 'fails', size=16, weight='bold', color=RED)
    s.box(4.3, h - 2.1, 3.1, 1.6, 'backup:\nscreenshot of\nthe saved output', size=17, weight='bold', r=0.05, fill=GOLD)
    s.icon('notebook', 1.2, 1.5, 0.9)
    s.text(2.0, 1.5, 'AI help used?\nSay so on the last slide.', size=17, ha='left', weight='bold')
    return s


@fig('ml_showcase_run')
def ml_showcase_run(w, h, **_):
    s = Scene(w, h)
    steps = [('present', 'your five slides'), ('explain', 'what the number means'), ('answer', 'questions from the room'), ('change', 'one small thing, unaided')]
    cw, gap = 2.45, 0.5
    x0 = (w - (4 * cw + 3 * gap)) / 2
    for i, (t, sub) in enumerate(steps):
        x = x0 + i * (cw + gap)
        s.box(x, h / 2 - 0.9, cw, 1.8, '', fill=GOLD if t == 'change' else PAPER, lw=2.2, r=0.05)
        s.text(x + cw / 2, h / 2 + 0.35, t, size=24, weight='bold')
        s.text(x + cw / 2, h / 2 - 0.3, sub, size=15)
        if i < 3:
            s.arrow(x + cw + 0.05, h / 2, x + cw + gap - 0.05, h / 2, lw=2.2, head=14)
    s.text(w / 2, h / 2 - 1.55, 'Your work, your voice, nothing to lean on but what you know.', size=18, color=BODY)
    return s


@fig('ml_portfolio_next')
def ml_portfolio_next(w, h, **_):
    s = Scene(w, h)
    s.text(1.9, h - 0.4, 'your portfolio', size=19, weight='bold')
    for i, (ic, t) in enumerate([('notebook', 'the handover notebook'), ('folder', 'the data file'), ('receipt', 'the one-page report'), ('pen', 'the AI use log')]):
        y = h - 1.2 - i * 0.95
        s.icon(ic, 0.7, y, 0.6)
        s.text(1.3, y, t, size=17, ha='left')
    s.arrow(3.5, h / 2, 4.2, h / 2, lw=2.4, head=16)
    s.text(4.4, h - 0.4, 'next step', size=19, weight='bold', ha='left')
    for i, t in enumerate(['a new question', 'real data, with permission', 'a bigger model, tested fairly']):
        s.text(4.4, h - 1.2 - i * 0.95, t, size=15, ha='left')
    return s


@fig('ml_unaided_change')
def ml_unaided_change(w, h, **_):
    s = Scene(w, h)
    s.code(0.3, h - 0.5, ['model = LinearRegression()', 'model.fit(X_train, y_train)', 'print(mae)'], size=15, line_h=0.34, pad=0.18, w=4.6, hl_lines=(1,))
    s.arrow(5.0, h - 1.05, 5.8, h - 1.05, lw=2.4, head=16)
    s.box(5.9, h - 1.9, 1.6, 1.7, 'change\none thing', size=17, weight='bold', r=0.05, fill=GOLD)
    s.text(w / 2, 1.9, 'Predict the result, run it, and explain the difference.', size=17, weight='bold')
    s.text(w / 2, 1.3, 'If it breaks, read the last line of the message first.', size=16, color=BODY)
    return s


# ================================================================== LAB F03: variation and probability
def _strip(s, x0, L, y, vals, vmax=8, mean=None, color=INK):
    s.line(x0, y, x0 + L, y, lw=2)
    for t in range(vmax + 1):
        s.line(x0 + t * L / vmax, y - 0.07, x0 + t * L / vmax, y + 0.07, lw=1.6)
        s.text(x0 + t * L / vmax, y - 0.3, str(t), size=14, color=MUTE)
    seen = {}
    for v in vals:
        k = seen.get(v, 0)
        seen[v] = k + 1
        s.circle(x0 + v * L / vmax, y + 0.3 + k * 0.4, 0.17, fill=GOLD, lw=2, z=4)
    if mean is not None:
        s.line(x0 + mean * L / vmax, y - 0.05, x0 + mean * L / vmax, y + 1.35, color=RED, lw=3, dash=True, z=3)


@fig('ml_same_mean_spread')
def ml_same_mean_spread(w, h, **_):
    s = Scene(w, h)
    x0, L = 1.6, w - 3.2
    _strip(s, x0, L, h - 2.0, [2, 2, 6, 6], mean=4)
    _strip(s, x0, L, 0.9, [4, 4, 4, 4], mean=4)
    s.text(0.25, h - 1.2, 'A', size=24, weight='bold', ha='left')
    s.text(0.25, 2.2, 'B', size=24, weight='bold', ha='left')
    s.text(x0 + 4.4 * L / 8, h - 1.0, 'mean 4, spread 2', size=19, weight='bold', ha='left')
    s.text(x0 + 4.4 * L / 8, 1.65, 'mean 4, spread 0', size=19, weight='bold', ha='left')
    s.text(x0 + L / 2, h - 0.3, 'Same mean, different groups: the red line is the mean', size=17, color=RED, weight='bold')
    return s


@fig('ml_deviation_arrows')
def ml_deviation_arrows(w, h, **_):
    s = Scene(w, h)
    x0, L, y = 0.9, w - 1.8, 1.7
    s.line(x0, y, x0 + L, y, lw=2)
    X = lambda v: x0 + v * L / 8
    for t in range(9):
        s.text(X(t), y - 0.35, str(t), size=14, color=MUTE)
    s.line(X(4), y - 0.05, X(4), y + 2.7, color=RED, lw=3, dash=True)
    s.text(X(4), y + 2.95, 'mean 4', size=17, weight='bold', color=RED)
    for k, v in enumerate([2, 2, 6, 6]):
        yy = y + 0.6 + (k % 2) * 0.9
        s.circle(X(v), yy, 0.18, fill=GOLD, lw=2, z=4)
        s.arrow(X(4) + (-0.05 if v < 4 else 0.05), yy, X(v) + (0.22 if v < 4 else -0.22), yy, lw=2, head=13)
        s.text(X(v) + (-0.6 if v < 4 else 0.6), yy + 0.0, '-2' if v < 4 else '+2', size=18, weight='bold')
    s.text(w / 2, 0.45, 'deviation = value minus mean, so it can be negative', size=17, color=BODY)
    return s


@fig('ml_prob_vs_fraction')
def ml_prob_vs_fraction(w, h, **_):
    throws = np.random.RandomState(5).randint(1, 7, 10)
    k = int((throws > 4).sum())
    s = Scene(w, h)
    s.text(1.9, h - 0.45, 'a fair die', size=19, weight='bold')
    for i in range(6):
        s.box(0.3 + (i % 3) * 0.6, h - 1.2 - (i // 3) * 0.6, 0.52, 0.52, str(i + 1), size=16, weight='bold', fill=GOLD if i + 1 > 4 else PAPER, lw=1.8, r=0.04)
    s.text(1.1, h - 2.75, '2 faces of 6\nare above 4:\nprobability 2/6', size=16)
    s.text(5.2, h - 0.45, 'ten throws', size=19, weight='bold')
    for i, v in enumerate(throws):
        s.box(3.6 + (i % 5) * 0.62, h - 1.2 - (i // 5) * 0.62, 0.54, 0.54, str(v), size=16, weight='bold', fill=GOLD if v > 4 else PAPER, lw=1.8, r=0.04)
    s.text(5.2, h - 2.75, f'{k} of 10 are above 4:\nobserved fraction {k}/10', size=16)
    s.text(w / 2, 0.5, 'The fraction you saw is not the probability, and it does not promise the next throw.', size=14, color=BODY)
    return s


@fig('ml_counters_fraction')
def ml_counters_fraction(w, h, **_):
    s = Scene(w, h)
    for i in range(5):
        s.circle(1.2 + i * 1.15, h - 1.6, 0.42, fill=GOLD if i < 3 else PAPER, edge=INK if i < 3 else RED, lw=2.4)
    s.text(1.2 + 1 * 1.15, h - 2.45, 'blue counters', size=16, color=MUTE)
    s.text(1.2 + 3.5 * 1.15, h - 2.45, 'red counters', size=16, color=MUTE)
    s.text(w / 2, 1.9, 'part divided by whole', size=18, weight='bold')
    s.text(w / 2, 1.1, '3 / 5  =  0.6  =  60%', size=34, weight='bold', mono=True)
    s.text(w / 2, h - 0.4, 'gold = blue in this picture', size=14, color=MUTE)
    return s


# ================================================================== LAB F04: matrices and weighted sums
@fig('ml_matrix_grid')
def ml_matrix_grid(w, h, **_):
    s = Scene(w, h)
    x0, y0, c = 1.9, h - 1.5, 1.2
    s.text(x0 + c / 2, y0 + 0.5, 'area_m2', size=17, mono=True)
    s.text(x0 + 1.5 * c, y0 + 0.5, 'rooms', size=17, mono=True)
    vals = [[40, 2], [60, 3]]
    for r in range(2):
        s.text(x0 - 0.2, y0 - r * c - c / 2, f'home {r}', size=17, ha='right', color=MUTE)
        for k in range(2):
            s.box(x0 + k * c, y0 - (r + 1) * c, c, c, str(vals[r][k]), size=26, weight='bold', fill=GOLD if (r, k) == (0, 1) else PAPER, lw=2, r=0.03)
    s.brace(x0, x0 + 2 * c, y0 - 2 * c - 0.15, depth=-0.12)
    s.text(x0 + c, y0 - 2 * c - 0.55, 'shape (2, 2): rows by columns', size=17, weight='bold')
    s.text(x0 + 2 * c + 0.3, y0 - 0.5 * c, 'homes[0, 1] is 2:\nrow 0, column 1', size=16, ha='left', color=RED, weight='bold')
    return s


@fig('ml_weighted_sum')
def ml_weighted_sum(w, h, **_):
    s = Scene(w, h)
    tiles = [('100000', 'intercept\nthe starting amount'), ('3000 x 40', 'weight for area\ntimes the area'), ('20000 x 2', 'weight for rooms\ntimes the rooms'), ('260000', 'the predicted\nrent, UGX')]
    tw = 2.3
    gap = (w - 0.6 - 4 * tw) / 3
    for i, (a, b) in enumerate(tiles):
        x = 0.3 + i * (tw + gap)
        s.box(x, h / 2 - 0.1, tw, 1.1, a, size=21 if i < 3 else 23, weight='bold', mono=True, fill=GOLD if i == 3 else PAPER, lw=2.2, r=0.05)
        s.text(x + tw / 2, h / 2 - 0.75, b, size=15, color=MUTE)
        if i < 3:
            s.text(x + tw + gap / 2, h / 2 + 0.45, '=' if i == 2 else '+', size=30, weight='bold')
    s.text(w / 2, h - 0.5, 'A weighted sum: multiply each input by its weight, then add', size=19, weight='bold')
    s.text(w / 2, 0.5, 'invented numbers for teaching, not real Kampala rents', size=15, color=RED)
    return s


@fig('ml_slope_step')
def ml_slope_step(w, h, **_):
    s = Scene(w, h)
    for i, (a, v) in enumerate([(40, '260,000'), (41, '263,000')]):
        x = 0.5 + i * 3.7
        s.box(x, 1.3, 2.4, 2.4, '', fill=PAPER, lw=2.2, r=0.05)
        s.text(x + 1.2, 3.2, f'{a} m2', size=22, weight='bold')
        s.text(x + 1.2, 2.5, '2 rooms', size=17, color=MUTE)
        s.text(x + 1.2, 1.75, v, size=24, weight='bold', mono=True)
    s.arrow(3.0, 2.5, 4.1, 2.5, color=RED, lw=2.4, head=16)
    s.text(3.55, 2.85, '+1 m2', size=16, weight='bold', color=RED)
    s.text(w / 2, 4.2, 'rent rises by 3,000', size=18, weight='bold', color=RED)
    s.text(w / 2, 0.6, 'The slope: change in rent for one more square metre, rooms held fixed.', size=14, color=BODY)
    return s


@fig('ml_matrix_rows')
def ml_matrix_rows(w, h, **_):
    s = Scene(w, h)
    rows = [['home', 'area_m2', 'rooms', 'rent'], ['0', '40', '2', '260,000'], ['1', '60', '3', '340,000'], ['2', '50', '2', '290,000']]
    s.table(0.4, h - 0.5, [1.2, 1.6, 1.4, 1.9], 0.75, rows, size=18, hl_rows=(3,), mono_cols=(1, 2, 3))
    s.text(w / 2, 0.75, 'the new row [50, 2] gives shape (3, 2)', size=18, weight='bold')
    s.text(w / 2, 0.3, 'weights stay the same, so the prediction rule does not change', size=14, color=BODY)
    return s


# ================================================================== EXTENSION ML25: a first neural network
@fig('ml_neuron_net')
def ml_neuron_net(w, h, **_):
    s = Scene(w, h)
    layers = [(4, 'four\nmeasurements'), (8, 'eight hidden\nunits'), (3, 'three\nspecies')]
    xs = [2.0, w / 2, w - 2.0]
    pos = []
    for (n, _), x in zip(layers, xs):
        gap = min(0.5, (h - 1.8) / max(n - 1, 1))
        pos.append([(x, h / 2 + 0.25 + (n - 1) * gap / 2 - i * gap) for i in range(n)])
    for a, b in zip(pos[:-1], pos[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b:
                s.line(x1, y1, x2, y2, color=HAIR, lw=0.9, z=1)
    for lay, col in zip(pos, [PAPER, GOLD, PAPER]):
        for (x, y) in lay:
            s.circle(x, y, 0.16, fill=col, lw=1.8, z=3)
    for (n, t), x in zip(layers, xs):
        s.text(x, 0.55, t, size=16, weight='bold')
    return s


@fig('ml_scale_inputs')
def ml_scale_inputs(w, h, **_):
    s = Scene(w, h)
    names = [('sepal length', 4.3, 7.9), ('sepal width', 2.0, 4.4), ('petal length', 1.0, 6.9), ('petal width', 0.1, 2.5)]
    x0, L = 2.6, w - 3.2
    s.text(x0, h - 0.4, 'before scaling: ranges in cm', size=17, weight='bold', ha='left')
    for i, (n, a, b) in enumerate(names):
        y = h - 0.95 - i * 0.45
        s.text(x0 - 0.15, y, n, size=14, ha='right')
        s.rect(x0 + a * L / 8, y - 0.15, (b - a) * L / 8, 0.3, fill=GOLD, lw=1.6)
    s.text(0.3, 2.15, 'after scaling: centred on 0, similar width', size=17, weight='bold', ha='left')
    for i, (n, a, b) in enumerate(names):
        y = 1.3 - i * 0.0
    for i in range(4):
        y = 1.65 - i * 0.3
        s.rect(x0 + L / 2 - 0.9, y - 0.1, 1.8, 0.2, fill=GOLD, lw=1.4)
    s.line(x0 + L / 2, 0.3, x0 + L / 2, 1.9, color=RED, lw=2, dash=True)
    return s


@fig('ml_model_trio')
def ml_model_trio(w, h, **_):
    s = Scene(w, h)
    names = ['majority baseline', 'tree, depth 3', 'small network']
    for i, n in enumerate(names):
        y = h - 1.3 - i * 1.15
        s.box(0.3, y - 0.4, 2.8, 0.8, n, size=17, weight='bold', r=0.05, fill=GOLD if i == 2 else PAPER)
        s.arrow(3.15, y, 4.2, h / 2 - 0.1 + (1 - i) * 0.3, lw=1.8, head=12)
    s.box(4.25, h / 2 - 0.9, 1.7, 1.6, '', fill='#BDBDBD', lw=2.2, r=0.05)
    s.text(5.1, h / 2 + 0.25, 'the same', size=16, weight='bold')
    s.text(5.1, h / 2 - 0.15, 'validation\nflowers', size=16)
    s.arrow(6.0, h / 2 - 0.1, 6.5, h / 2 - 0.1, lw=2.2, head=14)
    s.text(6.55, h / 2 - 0.1, 'accuracy', size=15, weight='bold', ha='left')
    s.text(w / 2, 0.45, 'Bigger is not automatically better. Compare on the same flowers.', size=15, color=BODY)
    return s
