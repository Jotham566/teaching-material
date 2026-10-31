"""Shared helpers for the Python for Data Analysis figures (data loading, chart wrapper, drawing helpers)."""
from functools import lru_cache

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import figkit
from figkit import Scene, fig, LayoutError  # noqa: F401
from brand import CAMP, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD

DATA = CAMP / 'data'
SUN = DATA / 'sunrise'
BRANCH = {1: 'Central Market', 2: 'Campus Gate', 3: 'Roadside'}

# standard placement sizes (inches)
Q = (11.9, 4.75)
C = (7.7, 4.95)
W = (11.9, 4.45)
P = (5.85, 3.75)
ICON = (1.3, 1.3)


@lru_cache(maxsize=None)
def shop():
    d = pd.read_csv(DATA / 'camp_shop.csv')
    d['revenue_ugx'] = d['units'] * d['unit_price_ugx']
    return d


@lru_cache(maxsize=None)
def sales():
    d = pd.read_csv(SUN / 'sales.csv')
    d['line_value'] = d['units'] * d['unit_price_ugx']
    d['branch'] = d['branch_id'].map(BRANCH)
    return d


@lru_cache(maxsize=None)
def products():
    return pd.read_csv(SUN / 'products.csv')


@lru_cache(maxsize=None)
def daily():
    return pd.read_csv(SUN / 'daily_summary.csv')


@lru_cache(maxsize=None)
def raw():
    return pd.read_csv(SUN / 'sales_raw.csv', dtype=str, keep_default_na=False)


@lru_cache(maxsize=None)
def practice():
    return pd.read_csv(SUN / 'products_practice.csv')


def file_shape(name):
    """(rows, columns) of a CSV exactly as read_csv returns it."""
    if name == 'camp_shop.csv':
        return pd.read_csv(DATA / name).shape
    return pd.read_csv(SUN / name).shape


def money(v):
    return f'{int(v):,}'


class Chart:
    """Wraps a matplotlib figure so the figure registry can save it like a Scene."""

    def __init__(self, f):
        self.f = f

    def save(self, path, name=''):
        return figkit.save_chart(self.f, path)


def chart(w, h):
    figkit.use_style()
    f, ax = plt.subplots(figsize=(w, h))
    return f, ax


def fmt_axis_money(ax, axis='y'):
    import matplotlib.ticker as mt
    f = mt.FuncFormatter(lambda v, p: f'{int(v):,}')
    (ax.yaxis if axis == 'y' else ax.xaxis).set_major_formatter(f)


def strip(s, x, y, values, w=0.8, h=0.62, size=18, hl=(), hl_fill=GOLD, fmt=str, labels=None, label_size=14, edge=INK):
    """A horizontal strip of boxes with values (an array drawn as number boxes). Returns the right edge."""
    s.cells(x, y, [fmt(v) for v in values], w=w, h=h, size=size, hl=hl, hl_fill=hl_fill, labels=labels, label_size=label_size, edge=edge, lw=1.6)
    return x + len(values) * w


def table_from(s, x, y_top, df_rows, col_w, row_h=0.46, size=16, **kw):
    """df_rows: list of lists (first row is the header)."""
    return s.table(x, y_top, col_w, row_h, df_rows, size=size, **kw)


def clean_pipeline():
    """The session 16 cleaning pipeline: returns (clean, excluded, steps) where steps are (label, rows) after each step."""
    r = pd.read_csv(SUN / 'sales_raw.csv')
    steps = [('raw file', len(r))]
    work = r.drop_duplicates().copy()
    steps.append(('drop repeats', len(work)))
    iso = pd.to_datetime(work['sale_date'], format='%Y-%m-%d', errors='coerce')
    slash = pd.to_datetime(work['sale_date'], format='%d/%m/%Y', errors='coerce')
    work['sale_date'] = iso.fillna(slash)
    steps.append(('parse dates', len(work)))
    lookup = {n.title(): n for n in products()['name']}
    work['product'] = work['product'].str.strip().str.title().map(lookup)
    steps.append(('fix names', len(work)))
    words = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}
    work['units'] = pd.to_numeric(work['units'].replace(words), errors='coerce')
    steps.append(('words to numbers', len(work)))
    excluded = work[work['units'].isna()]
    clean = work.dropna(subset=['units']).copy()
    clean['units'] = clean['units'].astype(int)
    clean['line_value'] = clean['units'] * clean['unit_price_ugx']
    steps.append(('leave out blanks', len(clean)))
    return clean, excluded, steps
