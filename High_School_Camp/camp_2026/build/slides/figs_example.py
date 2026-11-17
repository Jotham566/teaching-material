"""Exemplars of the figure style. Read these before writing figures; copy the habits, not the content.

Habits: canvas = placement size in inches (type sizes are real points); hairline black outlines; white fill; gold marks the
thing to look at, red marks a warning or a connection; real numbers computed from the data files; at least 16 pt type; a
short label beside each part so the picture explains itself; generous white space; pictograms only where they carry the
analogy (a shop, a bottle of juice), never as decoration.
"""
import pandas as pd

from brand import CAMP, INK, MUTE, RED, GOLD, PAPER
from figkit import Scene, fig

DATA = CAMP / 'data'


@fig('ex_groupby_piles')
def ex_groupby_piles(w, h, **_):
    """Rows of a table sorted into piles by item, then one total per pile."""
    shop = pd.read_csv(DATA / 'camp_shop.csv')
    shop['rev'] = shop['units'] * shop['unit_price_ugx']
    tot = shop.groupby('item')['rev'].sum()
    s = Scene(w, h)
    items = ['Book', 'Pen', 'Juice']
    icons = {'Book': 'book', 'Pen': 'pen', 'Juice': 'bottle'}
    s.text(w * 0.5, h - 0.3, '60 sales, one pile for each item', size=20, weight='bold')
    for i, it in enumerate(items):
        cx = w * (0.2 + 0.3 * i)
        s.icon(icons[it], cx, h - 1.2, 0.95)
        s.text(cx, h - 1.95, it, size=22, weight='bold')
        for k in range(4):
            s.box(cx - 0.6 + (k % 2) * 0.62, h - 2.75 - (k // 2) * 0.44, 0.56, 0.38, '', fill=PAPER, lw=1.4, r=0.03)
        s.text(cx, h - 3.5, f'{(shop.item == it).sum()} sales', size=17, color=MUTE)
        s.arrow(cx, h - 3.7, cx, h - 4.0, color=RED)
        s.box(cx - 1.0, h - 4.75, 2.0, 0.65, f'{tot[it]:,}', size=24, fill=GOLD, weight='bold', r=0.05)
    return s
