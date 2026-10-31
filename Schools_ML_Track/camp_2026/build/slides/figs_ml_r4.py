"""Repairs for Machine Learning sessions 13 to 24, labs F03 and F04 and the extension ML25.

Imported after figs_ml, so a figure registered here under an existing name replaces the older one.
Part 1 wraps every figure those decks use so its text is drawn at 16 pt or more where the layout allows.
Part 2 holds the redrawn figures.
"""
import numpy as np
import pandas as pd

import figkit
from figkit import Scene, LayoutError, fig, fig_registry
from brand import CAMP, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD
import figs_ml  # noqa: F401  (registers the originals first)

DATA = CAMP / 'data'
_ORIG = dict(fig_registry())


def _with_floor(orig, name):
    """Run an original figure with every text raised to at least 16 pt (15, then 14 if 16 does not fit)."""
    def fn(w, h, **p):
        saved_text, saved_axes = Scene.text, figs_ml.axes_in
        for floor in (16, 15, 14):
            def text(self, x, y, s, size=18, *a, __fl=floor, **k):
                return saved_text(self, x, y, s, max(size, __fl), *a, **k)

            def axes_in(s, x, y, w_, h_, __fl=floor, **kw):
                ax = saved_axes(s, x, y, w_, h_, **kw)
                ax.tick_params(labelsize=__fl)
                return ax
            Scene.text, figs_ml.axes_in = text, axes_in
            try:
                sc = orig(w, h, **p)
                if hasattr(sc, 'audit'):
                    sc.audit(name)
                return sc
            except LayoutError:
                continue
            finally:
                Scene.text, figs_ml.axes_in = saved_text, saved_axes
        return orig(w, h, **p)
    return fn


def _used_names():
    import concepts_ml_2
    names = set()
    for v in concepts_ml_2.CONCEPTS.values():
        names.add(v['question']['fig'])
        for f in v.get('word_icons', {}).values():
            if not isinstance(f, str):
                names.add(f[0])
        for s in v['slides']:
            for f in ([s['fig']] if 'fig' in s else s['figs']):
                names.add(f if isinstance(f, str) else f[0])
    return names


def _apply_bumps(skip):
    for name in _used_names():
        if name in skip or name == 'ml_icon' or name not in _ORIG or not name.startswith('ml_'):
            continue
        figkit._REG[name] = _with_floor(_ORIG[name], name)



_OVERRIDE = set()


def redraw(name):
    """Register a figure; a name that already exists replaces the older drawing and is not size-bumped."""
    def deco(fn):
        _OVERRIDE.add(name)
        figkit._REG[name] = fn
        return fn
    return deco


import math  # noqa: E402
from matplotlib.patches import Wedge, Circle  # noqa: E402

BAND = '#BDBDBD'


# ======================================================================================== word icons (1.3 x 1.3 in)
@redraw('ml_r4_icon')
def ml_r4_icon(w, h, kind='tr_table', **_):
    s = Scene(w, h)
    cx, cy = w / 2, h / 2
    L = 2.2
    if kind in ('tr_table', 'te_table'):
        dash = kind == 'te_table'
        for r in range(4):
            for c in range(3):
                x, y = 0.15 + c * 0.35, 1.05 - r * 0.25 - 0.22
                last = c == 2
                if dash and last:
                    s.rect(x, y, 0.32, 0.22, fill=PAPER, edge=RED, lw=1.6)
                else:
                    s.rect(x, y, 0.32, 0.22, fill=GOLD if last else PAPER, lw=1.5)
        if dash:
            s.text(0.15 + 2 * 0.35 + 0.16, 0.66, '?', size=18, weight='bold', color=RED, z=7)
    elif kind == 'leak':
        s.poly([(0.2, 1.15), (1.1, 1.15), (0.95, 0.4), (0.35, 0.4)], fill=PAPER, lw=2.2)
        s.rect(0.37, 0.8, 0.56, 0.3, fill=GOLD, lw=0, edge=GOLD)
        s.circle(0.65, 0.4, 0.05, fill=PAPER, edge=PAPER, lw=0, z=5)
        for yy, rr in [(0.27, 0.07), (0.1, 0.06)]:
            s.circle(0.65, yy, rr, fill=RED, edge=RED, lw=1.2)
    elif kind == 'rise':
        s.line(0.2, 0.2, 1.1, 0.2, lw=2.4)
        s.line(1.1, 0.2, 1.1, 0.95, color=RED, lw=3)
        s.line(0.2, 0.2, 1.1, 0.95, lw=2.4)
        s.arrow(0.25, 0.08, 1.05, 0.08, color=INK, lw=1.8, head=11)
        s.arrow(1.22, 0.25, 1.22, 0.9, color=RED, lw=1.8, head=11)
    elif kind == 'intercept':
        s.arrow(0.4, 0.15, 0.4, 1.2, lw=2, head=12)
        s.arrow(0.25, 0.3, 1.25, 0.3, lw=2, head=12)
        s.line(0.15, 0.55, 1.15, 1.1, lw=2.6)
        s.circle(0.4, 0.5 + 0.0 + 0.0 + 0.1, 0.1, fill=GOLD, lw=2, z=5)
        s.line(0.15, 0.55, 1.15, 1.1, lw=2.6, z=2)
    elif kind == 'fit_arrow':
        for (dx, dy) in [(0.18, 0.35), (0.3, 0.7), (0.42, 0.5), (0.22, 0.95)]:
            s.circle(dx, dy, 0.06, fill=PAPER, lw=1.8)
        s.arrow(0.55, 0.65, 0.78, 0.65, lw=2, head=12)
        s.line(0.85, 0.3, 1.2, 1.0, color=RED, lw=3)
    elif kind == 'predict':
        s.arrow(0.2, 0.15, 0.2, 1.2, lw=2, head=12)
        s.arrow(0.1, 0.25, 1.25, 0.25, lw=2, head=12)
        s.line(0.2, 0.3, 1.2, 1.1, lw=2.6)
        s.line(0.75, 0.25, 0.75, 0.7, color=RED, lw=2, dash=True)
        s.line(0.75, 0.7, 0.2, 0.7, color=RED, lw=2, dash=True)
        s.circle(0.75, 0.7, 0.07, fill=GOLD, lw=2, z=5)
        s.circle(0.75, 0.25, 0.06, fill=RED, edge=RED, z=5)
    elif kind == 'gap':
        s.line(0.1, 0.35, 1.2, 0.95, lw=2.6)
        s.circle(0.65, 0.95, 0.09, fill=GOLD, lw=2, z=5)
        s.line(0.65, 0.65, 0.65, 0.86, color=RED, lw=3.2, z=4)
        s.circle(0.3, 0.3, 0.08, fill=GOLD, lw=2, z=5)
        s.line(0.3, 0.38, 0.3, 0.5, color=RED, lw=3.2, z=4)
    elif kind == 'held_out':
        for i in range(6):
            held = i >= 4
            s.rect(0.1 + i * 0.19, 0.55, 0.16, 0.3, fill=GOLD if held else PAPER, lw=1.6)
        s.box(0.06, 0.48, 0.8, 0.44, '', fill='none', edge=INK, lw=1.4, r=0.03, z=4)
        s.arrow(1.0, 0.45, 1.0, 0.18, color=RED, lw=2, head=12)
    elif kind == 'pie_small':
        s.ax.add_patch(Circle((cx, cy), 0.45, fc=PAPER, ec=INK, lw=2, zorder=2))
        s.ax.add_patch(Wedge((cx, cy), 0.45, 90, 90 + 90, fc=GOLD, ec=INK, lw=2, zorder=3))
    elif kind == 'mae':
        for i, v in enumerate([0.25, 0.7, 0.45, 0.9]):
            s.rect(0.15 + i * 0.28, 0.2, 0.2, v * 0.85, fill=PAPER, lw=1.6)
        s.line(0.08, 0.2 + 0.575 * 0.85, 1.2, 0.2 + 0.575 * 0.85, color=RED, lw=2.4, dash=True, z=5)
    elif kind == 'classes':
        for k, (x0, y0, f) in enumerate([(0.3, 0.9, PAPER), (0.9, 0.9, GOLD), (0.6, 0.3, BAND)]):
            for dx, dy in [(0, 0), (0.16, 0.08), (-0.08, -0.14), (0.1, -0.15)]:
                s.circle(x0 + dx, y0 + dy, 0.075, fill=f, lw=1.8)
    elif kind == 'ratio':
        for i in range(10):
            s.rect(0.12 + (i % 5) * 0.21, 0.72 - (i // 5) * 0.28, 0.18, 0.24, fill=GOLD if i != 9 else PAPER, lw=1.6)
        s.text(cx, 0.25, '9 of 10', size=16, weight='bold', va='center')
    elif kind == 'majority':
        for i, v in enumerate([0.9, 0.4, 0.4]):
            s.rect(0.15 + i * 0.37, 0.2, 0.3, v, fill=GOLD if i == 0 else PAPER, lw=1.8)
    elif kind == 'depth':
        for (x, y) in [(0.65, 1.1), (0.35, 0.7), (0.95, 0.7), (0.2, 0.3), (0.5, 0.3)]:
            s.circle(x, y, 0.08, fill=PAPER, lw=2, z=4)
        for (a, b) in [((0.65, 1.1), (0.35, 0.7)), ((0.65, 1.1), (0.95, 0.7)), ((0.35, 0.7), (0.2, 0.3)), ((0.35, 0.7), (0.5, 0.3))]:
            s.line(a[0], a[1], b[0], b[1], lw=2)
        s.arrow(1.18, 1.1, 1.18, 0.25, color=RED, lw=2, head=12)
    elif kind == 'wiggle':
        xs = np.linspace(0.1, 1.2, 60)
        s.ax.plot(xs, 0.65 + 0.35 * np.sin(xs * 11) * np.exp(-0.5 * (xs - 0.6) ** 2 * 2), color=RED, lw=2.6, zorder=3)
        for xv in (0.2, 0.42, 0.65, 0.88, 1.1):
            yv = 0.65 + 0.35 * np.sin(xv * 11) * np.exp(-0.5 * (xv - 0.6) ** 2 * 2)
            s.circle(xv, yv, 0.06, fill=GOLD, lw=1.8, z=5)
    elif kind == 'pair_marks':
        for i in range(4):
            x = 0.2 + i * 0.3
            s.circle(x, 0.95, 0.08, fill=GOLD, lw=1.8)
            s.circle(x, 0.3 + (0.12 if i % 2 else 0), 0.08, fill=PAPER, lw=1.8)
    elif kind == 'three_way':
        s.rect(0.08, 0.5, 0.65, 0.35, fill=PAPER, lw=2)
        s.rect(0.73, 0.5, 0.22, 0.35, fill=GOLD, lw=2)
        s.rect(0.95, 0.5, 0.22, 0.35, fill=BAND, lw=2)
    elif kind == 'strata':
        for i in range(3):
            for j, f in enumerate([PAPER, GOLD, BAND]):
                s.rect(0.15 + i * 0.37, 0.2 + j * 0.3, 0.3, 0.3, fill=f, lw=1.6)
    elif kind == 'bars_pick':
        for i, (v, f) in enumerate([(0.9, PAPER), (0.55, GOLD), (0.8, PAPER)]):
            s.rect(0.15 + i * 0.37, 0.2, 0.3, v, fill=f, lw=1.8)
    elif kind == 'bounds':
        s.box(0.15, 0.25, 0.8, 0.8, '', fill='none', edge=INK, lw=2, r=0.04, dash=True)
        s.circle(0.4, 0.55, 0.07, fill=GOLD, lw=1.8)
        s.circle(0.65, 0.8, 0.07, fill=GOLD, lw=1.8)
        s.circle(1.15, 0.55, 0.09, fill=RED, edge=RED)
    elif kind == 'balance':
        s.line(0.65, 0.2, 0.65, 0.95, lw=2.4)
        s.line(0.15, 0.95, 1.15, 0.95, lw=2.6)
        s.line(0.35, 0.2, 0.95, 0.2, lw=2.4)
        for x in (0.15, 1.15):
            s.line(x, 0.95, x - 0.08, 0.6, lw=1.6)
            s.line(x, 0.95, x + 0.08, 0.6, lw=1.6)
            s.line(x - 0.12, 0.6, x + 0.12, 0.6, lw=2.4)
    elif kind == 'restart':
        s.ax.add_patch(Wedge((cx, cy), 0.45, 40, 330, width=0.1, fc=INK, ec=INK, zorder=3))
        s.poly([(cx + 0.39 - 0.17, cy - 0.2), (cx + 0.39 + 0.17, cy - 0.2), (cx + 0.39, cy + 0.12)], fill=RED, edge=RED, lw=1, z=5)
    elif kind == 'people':
        for x, f in [(0.3, PAPER), (0.65, GOLD), (1.0, PAPER)]:
            s.circle(x, 0.85, 0.11, fill=f, lw=2)
            s.ax.add_patch(Wedge((x, 0.35), 0.2, 0, 180, fc=f, ec=INK, lw=2, zorder=3))
    elif kind == 'solo':
        s.circle(cx, 0.85, 0.2, fill=GOLD, lw=2.2)
        s.ax.add_patch(Wedge((cx, 0.15), 0.4, 0, 180, fc=GOLD, ec=INK, lw=2.2, zorder=3))
    elif kind == 'stairs':
        for i in range(3):
            s.rect(0.15 + i * 0.35, 0.2, 0.35, 0.2 + i * 0.25, fill=GOLD if i == 2 else PAPER, lw=2)
        s.arrow(0.2, 0.75, 1.0, 1.15, color=RED, lw=2.2, head=13)
    elif kind == 'bubble':
        s.box(0.15, 0.4, 1.0, 0.65, '', fill=PAPER, lw=2.2, r=0.12)
        s.poly([(0.35, 0.42), (0.3, 0.15), (0.6, 0.42)], fill=PAPER, edge=INK, lw=2.2, z=3)
        s.line(0.36, 0.43, 0.59, 0.43, color=PAPER, lw=3.5, z=5)
        for i in range(3):
            s.line(0.3, 0.88 - i * 0.14, 0.95 - (0.2 if i == 2 else 0), 0.88 - i * 0.14, color=GREY, lw=1.8, z=4)
    elif kind == 'dev':
        s.line(0.1, 0.65, 1.2, 0.65, color=RED, lw=2.4)
        for x, y in [(0.3, 1.0), (0.6, 0.25), (0.95, 0.95)]:
            s.circle(x, y, 0.07, fill=GOLD, lw=1.8, z=5)
            s.line(x, y, x, 0.65, lw=1.8, dash=True)
    elif kind == 'sd_band':
        s.rect(0.08, 0.38, 1.12, 0.55, fill='#EDEDED', edge=GREY, lw=1.2, z=1)
        s.line(0.08, 0.655, 1.2, 0.655, color=RED, lw=2.2, z=3)
        for x, y in [(0.2, 0.5), (0.4, 0.85), (0.6, 0.45), (0.8, 0.9), (1.0, 0.6), (0.3, 1.1), (0.9, 0.2)]:
            s.circle(x, y, 0.06, fill=PAPER, lw=1.6, z=4)
    elif kind == 'frac_bar':
        s.rect(0.1, 0.5, 1.1, 0.3, fill=PAPER, lw=2)
        s.rect(0.1, 0.5, 0.37, 0.3, fill=GOLD, lw=2)
        for i in range(10):
            s.line(0.1 + i * 0.11, 0.5, 0.1 + i * 0.11, 0.38, lw=1.2)
    elif kind == 'slider':
        s.line(0.1, 0.65, 1.2, 0.65, lw=2.4)
        s.circle(0.8, 0.65, 0.17, fill=GOLD, lw=2.2, z=5)
        s.line(0.1, 0.4, 1.2, 0.4, lw=2.4)
        s.circle(0.35, 0.4, 0.17, fill=PAPER, lw=2.2, z=5)
        s.line(0.1, 0.9, 1.2, 0.9, lw=2.4)
        s.circle(0.55, 0.9, 0.17, fill=PAPER, lw=2.2, z=5)
    elif kind == 'wsum':
        for y, t in [(0.95, 'a'), (0.65, 'b'), (0.35, 'c')]:
            s.rect(0.1, y - 0.1, 0.2, 0.2, fill=PAPER, lw=1.6)
            s.line(0.3, y, 0.75, 0.65, color=GREY, lw=1.4)
        s.circle(0.95, 0.65, 0.2, fill=GOLD, lw=2.2, z=5)
        s.line(0.87, 0.65, 1.03, 0.65, lw=2.2, z=6)
        s.line(0.95, 0.57, 0.95, 0.73, lw=2.2, z=6)
    elif kind == 'checklist':
        for i in range(3):
            y = 0.95 - i * 0.33
            s.rect(0.15, y - 0.1, 0.2, 0.2, fill=GOLD if i < 2 else PAPER, lw=1.8)
            s.line(0.5, y, 1.15, y, color=GREY, lw=2.4)
    elif kind == 'code':
        s.rect(0.1, 0.3, 1.1, 0.8, fill=INK, edge=INK, lw=1)
        for i, (x2, f) in enumerate([(0.65, GOLD), (0.95, PAPER), (0.5, PAPER)]):
            s.line(0.22, 0.95 - i * 0.2, 0.22 + x2 * 0.8, 0.95 - i * 0.2, color=f, lw=2.6, z=5)
        s.rect(0.5, 0.12, 0.3, 0.1, fill=INK, edge=INK, lw=1)
    elif kind == 'screen':
        s.rect(0.1, 0.35, 1.1, 0.75, fill=PAPER, lw=2.2)
        for i, v in enumerate([0.25, 0.45, 0.35]):
            s.rect(0.3 + i * 0.28, 0.45, 0.2, v, fill=GOLD if i == 1 else PAPER, lw=1.6)
        s.line(0.65, 0.35, 0.65, 0.18, lw=2.2)
        s.line(0.4, 0.18, 0.9, 0.18, lw=2.6)
    elif kind == 'cert':
        s.rect(0.15, 0.3, 1.0, 0.75, fill=PAPER, lw=2.2)
        for i in range(2):
            s.line(0.3, 0.9 - i * 0.18, 0.95, 0.9 - i * 0.18, color=GREY, lw=2)
        s.circle(0.65, 0.42, 0.16, fill=GOLD, lw=2, z=5)
        s.line(0.58, 0.42, 0.63, 0.37, lw=2.2, z=6)
        s.line(0.63, 0.37, 0.73, 0.5, lw=2.2, z=6)
    elif kind == 'folder2':
        s.poly([(0.1, 0.3), (0.1, 1.0), (0.5, 1.0), (0.6, 0.9), (1.2, 0.9), (1.2, 0.3)], fill=GOLD, lw=2.2)
        s.line(0.1, 0.78, 1.2, 0.78, lw=2)
    elif kind == 'disclose':
        s.rect(0.2, 0.15, 0.8, 1.0, fill=PAPER, lw=2.2)
        for i in range(3):
            s.line(0.35, 0.95 - i * 0.18, 0.85, 0.95 - i * 0.18, color=GREY, lw=2)
        s.circle(0.85, 0.3, 0.22, fill=GOLD, lw=2.2, z=5)
        s.text(0.85, 0.3, 'AI', size=16, weight='bold', z=7)
    elif kind == 'tag_label':
        s.poly([(0.15, 0.65), (0.5, 1.05), (1.15, 1.05), (1.15, 0.25), (0.5, 0.25)], fill=GOLD, lw=2.2)
        s.circle(0.4, 0.65, 0.07, fill=PAPER, lw=1.8, z=5)
    elif kind == 'snow':
        for ang in (0, 60, 120):
            a = math.radians(ang)
            s.line(cx - 0.5 * math.cos(a), cy - 0.5 * math.sin(a), cx + 0.5 * math.cos(a), cy + 0.5 * math.sin(a), lw=2.8, z=3)
            for sgn in (-1, 1):
                ex, ey = cx + sgn * 0.5 * math.cos(a), cy + sgn * 0.5 * math.sin(a)
                for da in (30, -30):
                    b = a + math.pi * (1 if sgn < 0 else 0) + math.radians(150 if da > 0 else -150) * 1.0
                    s.line(ex, ey, ex + 0.16 * math.cos(b + math.pi), ey + 0.16 * math.sin(b + math.pi), lw=2, z=3) if False else None
        s.circle(cx, cy, 0.12, fill=GOLD, lw=2, z=5)
    return s


# ======================================================================================== sessions 13 to 15
from figs_ml import axes_in, hand_and_fit, homes, homes_split, split_idx, ols, predict, mae, money, bars_compare  # noqa: E402


@redraw('ml_features_target')
def ml_features_target(w, h, **_):
    s = Scene(w, h)
    d = homes().head(4)[['area_m2', 'rooms', 'rent_ugx']]
    rh = 0.52
    cws = [1.9, 1.5, 2.1]
    tx, ty = 0.5, h - 0.85
    rows = [list(d.columns)] + [[f'{v:,}' if c == 'rent_ugx' else str(v) for c, v in zip(d.columns, r)] for r in d.astype(object).values.tolist()]
    s.table(tx, ty, cws, rh, rows, size=20, hl_cells={(0, 0): GOLD, (0, 1): GOLD, (0, 2): '#EDEDED'})
    s.brace(tx, tx + cws[0] + cws[1], ty + 0.18, depth=0.18)
    s.text(tx + (cws[0] + cws[1]) / 2, ty + 0.55, 'features: the inputs', size=22, weight='bold')
    s.brace(tx + cws[0] + cws[1] + 0.05, tx + sum(cws), ty + 0.18, depth=0.18)
    s.text(tx + cws[0] + cws[1] + cws[2] / 2, ty + 0.55, 'target: the answer', size=22, weight='bold', color=RED)
    mx = tx + sum(cws) + 0.55
    my = ty - 5 * rh / 2
    s.arrow(mx, my, mx + 0.5, my, lw=2.6, head=18)
    s.box(mx + 0.6, my - 0.85, 1.7, 1.7, 'model', size=26, weight='bold', r=0.08, fill='#111111', edge='#111111', color=PAPER)
    s.arrow(mx + 2.4, my, mx + 2.9, my, lw=2.6, head=18)
    s.text(mx + 3.0, my, 'a guess\nof the rent', size=24, weight='bold', ha='left')
    s.text(w / 2, 0.5, 'The model sees the features. The target stays hidden when it guesses.', size=20, color=BODY)
    return s


@redraw('ml_leakage_timeline')
def ml_leakage_timeline(w, h, **_):
    s = Scene(w, h)
    y = 2.35
    s.arrow(0.25, y, w - 0.2, y, lw=3, head=22)
    s.text(0.3, y - 0.4, 'time', size=18, color=MUTE, ha='left')
    spec = [(0.3, 2.35, PAPER, INK, 'before', 'area, rooms', INK),
            (2.9, 2.2, GOLD, INK, 'the answer', 'selling price', INK),
            (5.3, 2.2, PAPER, RED, 'after', 'final payment', RED)]
    for x, bw, fill, edge, head, sub, col in spec:
        s.box(x, y + 0.55, bw, 1.55, '', fill=fill, edge=edge, lw=2.4 if edge == RED else 2, r=0.05)
        s.text(x + bw / 2, y + 1.7, head, size=24, weight='bold', color=col)
        s.text(x + bw / 2, y + 1.1, sub, size=19, color=col)
        s.line(x + bw / 2, y + 0.55, x + bw / 2, y + 0.1, color=GREY, lw=1.6)
    s.icon('check', 0.3 + 2.35 / 2, y, 0.5)
    s.circle(2.9 + 1.1, y, 0.12, fill=INK)
    s.icon('cross', 5.3 + 1.1, y, 0.5)
    s.text(w / 2, 1.1, 'A feature must exist before the answer does.', size=21, weight='bold')
    s.text(w / 2, 0.45, 'Information from after it is leakage.', size=21, color=RED, weight='bold')
    return s


@redraw('ml_practice_vs_exam')
def ml_practice_vs_exam(w, h, **_):
    s = Scene(w, h)
    rows_tr = [['area', 'rent']] + [['49', '290k'], ['141', '587k'], ['123', '552k']]
    rows_te = [['area', 'rent']] + [['63', '?'], ['88', '?'], ['72', '?']]
    s.text(1.5, h - 0.35, 'training data', size=24, weight='bold')
    s.text(5.5, h - 0.35, 'test data', size=24, weight='bold')
    s.table(0.4, h - 0.8, [1.0, 1.2], 0.5, rows_tr, size=20, hl_cols=(1,), hl_cells={(0, 0): '#EDEDED', (0, 1): '#EDEDED'})
    s.table(4.4, h - 0.8, [1.0, 1.2], 0.5, rows_te, size=20, hl_cells={(0, 0): '#EDEDED', (0, 1): '#EDEDED'})
    s.text(1.5, h - 3.1, 'the model learns from these', size=17)
    s.text(5.5, h - 3.1, 'kept aside as the exam', size=17)
    s.box(0.4, 0.8, 5.2, 0.55, '', fill=PAPER, lw=2, r=0.03)
    s.rect(0.4 + 3.95, 0.8, 1.25, 0.55, fill=GOLD, lw=2)
    s.text(0.4 + 3.95 / 2, 1.075, 'practice questions', size=18)
    s.text(0.4 + 3.95 + 0.625, 1.075, 'exam', size=18, weight='bold')
    s.text(0.4, 0.35, 'The exam questions are never used for practice.', size=17, color=MUTE, ha='left')
    return s


# ---------------------------------------------------------------------------------------- session 14
def _rent_axes(ax, ylim=(0, 700000)):
    ax.set_yticks([200000, 400000, 600000])
    ax.set_yticklabels(['200k', '400k', '600k'])
    ax.set_ylim(*ylim)


@redraw('ml_three_lines')
def ml_three_lines(w, h, **_):
    x, y, hand, beta, fit = hand_and_fit()
    mb = np.full_like(y, y.mean())
    s = Scene(w, h)
    cw = 3.85
    for k, (name, pred, line_fn, col) in enumerate([('plain mean guess', mb, lambda xs: np.full_like(xs, y.mean()), GREY),
                                                     ('my guess line', hand, lambda xs: 100000 + 3000 * xs, RED),
                                                     ('the fitted line', fit, lambda xs: beta[0] + beta[1] * xs, INK)]):
        x0 = 0.1 + k * (cw + 0.12)
        ax = axes_in(s, x0 + 0.95, 1.55, cw - 1.1, h - 2.55)
        xs = np.array([x.min() - 5, x.max() + 5])
        ax.plot(xs, line_fn(xs), color=col, lw=3, ls='--' if col == RED else '-')
        for xi, yi, pi in zip(x, y, pred):
            ax.plot([xi, xi], [yi, pi], color=INK, lw=2.4, zorder=3)
        ax.scatter(x, y, s=95, facecolor=GOLD, edgecolor=INK, linewidth=1.6, zorder=4)
        ax.set_xticks([])
        _rent_axes(ax)
        ax.set_ylabel('rent (UGX)', fontsize=16)
        ax.set_xlabel('area', fontsize=16)
        s.text(x0 + cw / 2 + 0.3, h - 0.4, name, size=20, weight='bold')
        s.text(x0 + cw / 2 + 0.3, 0.95, money(mae(y, pred)), size=30, weight='bold', mono=True)
        s.text(x0 + cw / 2 + 0.3, 0.45, 'average miss (UGX)', size=16, color=MUTE)
    return s


@redraw('ml_extrapolation')
def ml_extrapolation(w, h, **_):
    s = Scene(w, h)
    ax = axes_in(s, 0.6, 1.0, 4.4, h - 2.0)
    Xv = np.array([10, 20, 30, 40])
    ax.plot([0, 70], [0, 700], color=INK, lw=3)
    ax.scatter(Xv, Xv * 10, s=120, facecolor=PAPER, edgecolor=INK, linewidth=2, zorder=3)
    ax.scatter([35], [350], s=240, facecolor=GOLD, edgecolor=INK, linewidth=2.2, zorder=4)
    ax.axvspan(10, 40, color='#F1F1F1', zorder=0)
    ax.text(25, 570, 'examples\nlive here', fontsize=18, ha='center', fontweight='bold', family=figkit.FONT)
    ax.text(35, 250, '35: fine', fontsize=18, ha='center', va='top', fontweight='bold', family=figkit.FONT)
    ax.set_xlim(0, 70)
    ax.set_ylim(0, 760)
    ax.set_xticks([10, 20, 30, 40])
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.set_xlabel('input X', fontsize=16)
    s.arrow(5.1, 2.9, 5.7, 2.9, color=RED, lw=2.6, head=20)
    s.text(6.7, 2.9, '1000?', size=34, weight='bold', color=RED)
    s.text(6.5, 1.75, 'far off the page:\nno example\nis near', size=19, color=RED, weight='bold')
    s.text(w / 2, h - 0.35, 'a line is trustworthy near its examples', size=21, weight='bold')
    return s


# ---------------------------------------------------------------------------------------- session 15
@redraw('ml_seed_dice')
def ml_seed_dice(w, h, **_):
    d = homes()
    Xc = d[['area_m2', 'rooms']].values.astype(float)
    y = d['rent_ugx'].values.astype(float)
    res = []
    for seed in range(1, 11):
        tr, te = split_idx(len(d), 0.25, seed)
        res.append(mae(y[te], predict(ols(Xc[tr], y[tr]), Xc[te])))
    s = Scene(w, h)
    ax = axes_in(s, 1.5, 1.95, w - 1.9, h - 2.95)
    xs = list(range(1, 11))
    best = int(np.argmin(res))
    ax.scatter(xs, res, s=240, facecolor=[GOLD if i == 6 else PAPER for i in range(10)], edgecolor=INK, linewidth=2.2, zorder=3)
    ax.scatter([xs[best]], [res[best]], s=360, facecolor='none', edgecolor=RED, linewidth=3.2, zorder=4)
    ax.axhline(np.mean(res), color=GREY, lw=2, ls='--')
    ax.set_xticks(xs)
    ax.set_xlabel('random_state (the seed of the shuffle)', fontsize=17)
    ax.set_ylabel('average miss (UGX)', fontsize=17)
    lo, hi = min(res), max(res)
    ax.set_ylim(lo - (hi - lo) * 0.6, hi + (hi - lo) * 0.6)
    s.text(w / 2, h - 0.35, 'the same model, ten different shuffles', size=21, weight='bold')
    s.text(0.4, 0.95, f'Our seed 7 (gold dot): {money(res[6])}.', size=18, ha='left', color=RED, weight='bold')
    s.text(0.4, 0.45, f'Luckiest seed {xs[best]} (ringed): {money(res[best])}.  Typical: {money(np.mean(res))}.', size=18, ha='left', color=RED, weight='bold')
    return s


def _test_panel(w, h, which):
    d, tr, te, y, pred, base, beta = homes_split()
    s = Scene(w, h)
    x = d['area_m2'].values[te]
    ax = axes_in(s, 1.55, 2.2, w - 1.85, h - 3.15)
    p = base if which == 'base' else pred
    order = np.argsort(x)
    ax.axhline(base[0], color=RED, lw=2.6 if which == 'base' else 1.8, ls='-' if which == 'base' else '--', zorder=1)
    if which == 'model':
        ax.plot(x[order], p[order], color=INK, lw=3, zorder=2)
    for xi, yi, pi in zip(x, y[te], p):
        ax.plot([xi, xi], [yi, pi], color=INK, lw=1.8, zorder=2)
    ax.scatter(x, y[te], s=70, facecolor=GOLD, edgecolor=INK, linewidth=1.4, zorder=4)
    ax.set_ylim(0, 800000)
    ax.set_yticks([200000, 400000, 600000])
    ax.set_yticklabels(['200k', '400k', '600k'])
    ax.set_xlabel('area (square metres)', fontsize=16)
    ax.set_ylabel('rent (UGX)', fontsize=16)
    ax.text(0.98, 0.04, 'red line: the plain guess', transform=ax.transAxes, fontsize=16, color=RED, ha='right', va='bottom', fontweight='bold', family=figkit.FONT)
    ttl = 'plain guess: the training mean' if which == 'base' else 'the fitted model'
    s.text(w / 2, h - 0.4, ttl, size=21, weight='bold')
    s.text(w / 2, 0.95, money(mae(y[te], p)), size=30, weight='bold', mono=True)
    s.text(w / 2, 0.4, 'average miss on 30 unseen homes (UGX)', size=17, color=MUTE)
    return s


@redraw('ml_mae_test_baseline')
def ml_mae_test_baseline(w, h, **_):
    return _test_panel(w, h, 'base')


@redraw('ml_mae_test_model')
def ml_mae_test_model(w, h, **_):
    return _test_panel(w, h, 'model')




@redraw('ml_fit_predict_flow')
def ml_fit_predict_flow(w, h, **_):
    s = Scene(w, h)
    Xv = [10, 20, 30, 40]
    yv = [100, 200, 300, 400]
    top = h - 0.45
    s.table(0.2, top, [0.9], 0.55, [['X']] + [[str(v)] for v in Xv], size=21)
    s.table(1.2, top, [0.9], 0.55, [['y']] + [[str(v)] for v in yv], size=21)
    s.text(1.15, top - 5 * 0.55 - 0.45, 'examples: inputs\nand answers', size=17, color=BODY)
    s.arrow(2.25, top - 1.4, 2.8, top - 1.4, lw=2.4, head=16)
    s.box(2.85, top - 2.0, 1.2, 1.2, 'fit', size=26, mono=True, weight='bold', fill='#111111', edge='#111111', color=PAPER, r=0.07)
    s.arrow(4.1, top - 1.4, 4.55, top - 1.4, lw=2.4, head=16)
    ax = axes_in(s, 4.65, top - 2.8, 2.8, 2.5)
    ax.plot([0, 50], [0, 500], color=RED, lw=3)
    ax.scatter(Xv, yv, s=80, facecolor=PAPER, edgecolor=INK, linewidth=1.8, zorder=3)
    ax.scatter([35], [350], s=170, facecolor=GOLD, edgecolor=INK, linewidth=2, zorder=4)
    ax.set_xticks([])
    ax.set_yticks([])
    s.text(6.05, top - 0.0, 'the learned line', size=19, weight='bold')
    s.text(6.05, 1.2, 'predict([[35]])\ngives 350', size=19, mono=True, weight='bold')
    s.text(w / 2, 0.6, 'fit learns the line. predict reads a new answer from it.', size=18, color=BODY)
    return s
# ======================================================================================== sessions 16 to 18
from figs_ml import PETAL, _overfit_data, poly_gap_data, lock_icon, three_way, fares  # noqa: E402

IRIS_NOTE = 'Counts checked against the iris file that ships with scikit-learn.'


@redraw('ml_petal_ranges')
def ml_petal_ranges(w, h, **_):
    s = Scene(w, h)
    x0, x1 = 3.6, w - 0.7
    sc = (x1 - x0) / 7.0
    X = lambda v: x0 + v * sc
    ys = {'setosa': h - 1.2, 'versicolor': h - 1.95, 'virginica': h - 2.7}
    fills = {'setosa': PAPER, 'versicolor': GOLD, 'virginica': BAND}
    for sp, (lo, hi) in PETAL.items():
        s.rect(X(lo), ys[sp] - 0.27, (hi - lo) * sc, 0.54, fill=fills[sp], lw=2)
        s.text(3.4, ys[sp] + 0.13, sp, size=22, weight='bold', ha='right')
        s.text(3.4, ys[sp] - 0.22, f'{lo:.1f} to {hi:.1f} cm', size=17, color=MUTE, ha='right')
    s.line(x0, 0.75, x1, 0.75, lw=2)
    for v in range(0, 8):
        s.line(X(v), 0.75, X(v), 0.63, lw=1.6)
        s.text(X(v), 0.38, str(v), size=18)
    s.text(x1 + 0.1, 0.38, 'cm', size=17, color=MUTE, ha='left')
    for t in (2.5, 4.8):
        s.line(X(t), 1.7, X(t), h - 0.85, color=RED, lw=3, dash=True, z=5)
        s.text(X(t), h - 0.5, f'rule: {t}', size=20, weight='bold', color=RED)
    s.brace(X(4.5), X(5.1), 1.55, depth=-0.0) if False else None
    s.text(X(4.8), 1.2, 'versicolor and virginica overlap from 4.5 to 5.1 cm', size=18, color=RED, ha='center', weight='bold')
    return s


@redraw('ml_tree_diagram')
def ml_tree_diagram(w, h, **_):
    s = Scene(w, h)

    def node(cx, cy, text, wd, ht=0.8, fill=PAPER):
        s.box(cx - wd / 2, cy - ht / 2, wd, ht, text, size=20, fill=fill, lw=2, r=0.07, weight='bold')
    node(4.0, h - 0.55, 'petal length <= 2.45 ?', 3.6)
    node(6.6, h - 2.1, 'petal width <= 1.75 ?', 3.6)
    ly = 1.25
    node(1.6, ly, 'setosa', 2.2, 0.8)
    node(5.2, ly, 'versicolor', 2.4, 0.8, GOLD)
    node(8.5, ly, 'virginica', 2.2, 0.8, BAND)
    s.arrow(3.0, h - 0.95, 1.7, ly + 0.45, lw=2.2, head=15)
    s.text(1.85, h - 1.9, 'yes', size=21, weight='bold', color=RED)
    s.arrow(5.0, h - 0.95, 6.0, h - 1.7, lw=2.2, head=15)
    s.text(6.3, h - 1.25, 'no', size=21, weight='bold', color=RED)
    s.arrow(5.7, h - 2.5, 5.2, ly + 0.45, lw=2.2, head=15)
    s.text(4.65, h - 2.75, 'yes', size=21, weight='bold', color=RED)
    s.arrow(7.5, h - 2.5, 8.4, ly + 0.45, lw=2.2, head=15)
    s.text(8.95, h - 2.6, 'no', size=21, weight='bold', color=RED)
    s.text(1.6, 0.6, '50 flowers', size=17, color=BODY)
    s.text(5.2, 0.6, '49 right, 5 wrong', size=17, color=BODY)
    s.text(8.5, 0.6, '45 right, 1 wrong', size=17, color=BODY)
    s.text(9.95, h - 1.2, 'Each box asks\na question.\nEach arrow is\nyes or no.', size=19, ha='left', va='center')
    s.text(w - 0.2, 0.15, 'All 150 flowers. Your tree may differ slightly.', size=16, color=MUTE, ha='right', va='bottom')
    return s


def _plus(name, extra):
    base = _with_floor(_ORIG[name], name)

    def fn(w, h, **p):
        s = base(w, h, **p)
        extra(s, w, h)
        return s
    _OVERRIDE.add(name)
    figkit._REG[name] = fn


_plus('ml_zones_hand', lambda s, w, h: s.text(w / 2, 4.1, 'Wrong on 7 of 150 flowers: accuracy 0.953', size=18, weight='bold', color=RED))


@redraw('ml_overfit_curve')
def ml_overfit_curve(w, h, **_):
    xtr, ytr, xte, yte, poly, line = _overfit_data()
    s = Scene(w, h)
    ax = axes_in(s, 1.4, 0.95, 6.5, h - 1.45)
    xs = np.linspace(xtr.min(), xtr.max(), 300)
    yy = poly(xs)
    yy = np.where((yy > -3000) & (yy < 30000), yy, np.nan)
    ax.scatter(xte[::3], yte[::3], s=70, facecolor='#EDEDED', edgecolor=GREY, linewidth=1.4, zorder=2)
    ax.plot(xs, yy, color=RED, lw=3.4, zorder=3)
    ax.plot(xs, line(xs), color=INK, lw=3.2, zorder=3)
    ax.scatter(xtr, ytr, s=190, facecolor=GOLD, edgecolor=INK, linewidth=2, zorder=5)
    ax.set_ylim(-3000, 30000)
    ax.set_xlabel('distance (km)', fontsize=18)
    ax.set_ylabel('fare (UGX)', fontsize=18)
    ax.set_yticks([0, 10000, 20000, 30000])
    ax.set_yticklabels(['0', '10k', '20k', '30k'])
    X = 8.35
    s.circle(X + 0.1, h - 0.7, 0.13, fill=GOLD, lw=2)
    s.text(X + 0.4, h - 0.7, '8 training trips', size=19, ha='left')
    s.circle(X + 0.1, h - 1.2, 0.09, fill='#EDEDED', edge=GREY, lw=1.6)
    s.text(X + 0.4, h - 1.2, 'new trips', size=19, ha='left')
    s.line(X - 0.05, h - 1.95, X + 0.3, h - 1.95, color=RED, lw=3.4)
    s.text(X + 0.4, h - 1.95, 'curve through every\ntraining trip', size=18, ha='left', color=RED, weight='bold')
    s.text(X, h - 2.9, f'training miss  {mae(ytr, poly(xtr)):,.0f}\nnew trips miss {mae(yte, poly(xte)):,.0f}', size=17, ha='left', color=RED, mono=True)
    s.line(X - 0.05, h - 3.85, X + 0.3, h - 3.85, color=INK, lw=3.4)
    s.text(X + 0.4, h - 3.85, 'a plain line', size=19, ha='left', weight='bold')
    s.text(X, h - 4.35, f'new trips miss {mae(yte, line(xte)):,.0f}', size=17, ha='left', mono=True)
    return s


@redraw('ml_confusion_3x3')
def ml_confusion_3x3(w, h, **_):
    s = Scene(w, h)
    cw, ch = 1.2, 0.85
    x0, y0 = 2.45, h - 1.5
    names = ['setosa', 'versicolor', 'virginica']
    s.text(x0 + 1.5 * cw, h - 0.35, 'predicted', size=21, weight='bold')
    for k, nm in enumerate(names):
        s.text(x0 + k * cw + cw / 2, h - 1.0, nm, size=16)
        s.text(x0 - 0.12, y0 - k * ch - ch / 2, nm, size=17, ha='right')
    s.text(0.3, y0 - 1.5 * ch, 'actual', size=21, weight='bold', rot=90)
    for r in range(3):
        for k in range(3):
            s.box(x0 + k * cw, y0 - (r + 1) * ch, cw, ch, 'right' if r == k else 'mix-up', size=17, fill=GOLD if r == k else PAPER, lw=2, r=0.03, weight='bold' if r == k else 'normal', color=INK if r == k else MUTE)
        s.text(x0 + 3 * cw + 0.15, y0 - r * ch - ch / 2, '= 10', size=18, ha='left', color=BODY)
    s.text(x0 + 1.5 * cw, y0 - 3 * ch - 0.4, 'each row adds to 10: ten flowers of each species', size=17, color=BODY)
    return s


@redraw('ml_two_cuts')
def ml_two_cuts(w, h, **_):
    s = Scene(w, h)
    W = w - 1.0

    def bar(y, parts):
        x = 0.5
        for name, n, f in parts:
            bw = W * n / 150
            s.rect(x, y, bw, 0.6, fill=f, lw=2)
            s.text(x + bw / 2, y + 0.3, f'{name} {n}' if bw > 1.9 else str(n), size=18, weight='bold')
            x += bw
    y1, y2, y3 = h - 1.15, h - 2.75, 0.4
    s.text(0.5, y1 + 0.85, 'start: 150 flowers', size=19, weight='bold', ha='left')
    bar(y1, [('all', 150, PAPER)])
    ax_ = w - 0.9
    s.arrow(ax_, y1 - 0.05, ax_, y2 + 0.65, color=RED, lw=2.4, head=16)
    s.text(ax_ - 0.2, (y1 + y2 + 0.65) / 2, 'first cut: 30 flowers (20%)\nare locked away for the final test', size=18, ha='right', color=RED, weight='bold')
    s.text(0.5, y2 + 0.85, 'two parts', size=19, weight='bold', ha='left')
    bar(y2, [('development', 120, BAND), ('final test', 30, GOLD)])
    s.arrow(ax_, y2 - 0.05, ax_, y3 + 0.65, color=RED, lw=2.4, head=16)
    s.text(ax_ - 0.2, (y2 + y3 + 0.65) / 2 + 0.05, 'second cut: 30 of the 120 (25%)\nbecome the validation part', size=18, ha='right', color=RED, weight='bold')
    bar(y3, [('train', 90, PAPER), ('validation', 30, BAND), ('final test', 30, GOLD)])
    return s


@redraw('ml_checkpoint_two_list')
def ml_checkpoint_two_list(w, h, **_):
    s = Scene(w, h)
    items = ['the three split sizes', 'the baseline score', 'two validation scores', 'the chosen depth', 'the final test accuracy', 'the confusion matrix', 'two limitations']
    for i, t in enumerate(items):
        col, row = i // 4, i % 4
        x = 0.5 + col * 6.1
        y = h - 0.85 - row * 0.95
        s.icon('check', x + 0.3, y, 0.62)
        s.text(x + 0.85, y, t, size=24, ha='left')
    s.text(w / 2 + 3.0, 1.0, 'all from one\nrestarted notebook', size=22, weight='bold', ha='center', color=RED)
    s.text(w / 2 - 3.0, 0.45, 'Seven pieces of evidence.', size=20, color=BODY, ha='left')
    return s


@redraw('ml_complexity_gap')
def ml_complexity_gap(w, h, **_):
    res = poly_gap_data()
    s = Scene(w, h)
    ax = axes_in(s, 1.5, 1.25, w - 1.9, h - 2.6)
    xs = np.arange(len(res))
    tr = [r[1] for r in res]
    te = [r[2] for r in res]
    top = min(max(te), 3 * max(tr[0], te[0]))
    ax.bar(xs - 0.2, tr, 0.38, color=GOLD, edgecolor=INK, linewidth=2)
    ax.bar(xs + 0.2, np.minimum(te, top), 0.38, color=PAPER, edgecolor=INK, linewidth=2)
    for i, v in enumerate(te):
        if v > top:
            ax.text(xs[i] + 0.2, top * 1.05, f'{v:,.0f}', ha='center', va='bottom', fontsize=16, fontweight='bold', color=RED, family=figkit.FONT)
    ax.set_xticks(xs)
    ax.set_xticklabels(['line', 'bend 1', 'bend 3', 'bend 7', 'bend 10'], fontsize=17)
    ax.set_ylim(0, top * 1.3)
    ticks = [0, 2500, 5000, 7500]
    ticks = [t for t in ticks if t <= top * 1.05]
    ax.set_yticks(ticks)
    ax.set_yticklabels([f'{t:,}' for t in ticks])
    ax.set_ylabel('average miss (UGX)', fontsize=17)
    s.rect(1.75, h - 1.05, 0.3, 0.3, fill=GOLD, lw=2)
    s.text(2.2, h - 0.9, 'training trips', size=18, ha='left')
    s.rect(4.35, h - 1.05, 0.3, 0.3, fill=PAPER, lw=2)
    s.text(4.8, h - 0.9, 'new trips', size=18, ha='left')
    s.text(w / 2, h - 0.35, 'the more it bends, the better it remembers', size=20, weight='bold')
    s.text(w / 2, 0.3, 'The same idea as a tree with too many questions.', size=18, color=BODY)
    return s
# ======================================================================================== sessions 19 to 22
from figs_ml import fares_models  # noqa: E402


def tick_box(s, x, y, size=0.4, done=True):
    s.rect(x - size / 2, y - size / 2, size, size, fill=GOLD if done else PAPER, lw=2)
    if done:
        s.line(x - size * 0.25, y, x - size * 0.05, y - size * 0.22, lw=2.6, z=5)
        s.line(x - size * 0.05, y - size * 0.22, x + size * 0.27, y + size * 0.25, lw=2.6, z=5)


def num_dot(s, x, y, n, r=0.26):
    s.circle(x, y, r, fill=GOLD, lw=2)
    s.text(x, y, str(n), size=18, weight='bold', z=7)


@redraw('ml_checkpoint_two_list')
def ml_checkpoint_two_list(w, h, **_):
    s = Scene(w, h)
    items = ['the three split sizes', 'the baseline score', 'two validation scores', 'the chosen depth', 'the final test accuracy', 'the confusion matrix', 'two limitations']
    pitch = (h - 0.4) / len(items)
    for i, t in enumerate(items):
        y = h - 0.2 - pitch * (i + 0.5)
        tick_box(s, 0.6, y, 0.4)
        s.text(1.2, y, t, size=23, ha='left')
    s.box(7.4, h / 2 - 1.0, 4.2, 2.0, 'all seven come from\none notebook, restarted\nand run from the top', size=21, weight='bold', r=0.06, edge=RED, color=RED)
    return s


@redraw('ml_three_datasets')
def ml_three_datasets(w, h, **_):
    s = Scene(w, h)
    cards = [('homes', 'synthetic_homes.csv', f'{len(homes())} homes', ['area_m2', 'rooms'], 'rent_ugx', 'a number'),
             ('fares', 'synthetic_fares.csv', f'{len(fares())} boda-boda trips', ['distance_km', 'rush_hour', 'raining'], 'fare_ugx', 'a number'),
             ('flowers', 'iris', '150 flowers', ['sepal_length', 'sepal_width', 'petal_length', 'petal_width'], 'species', 'a category')]
    cw = (w - 0.4 - 0.5) / 3
    for i, (nm, f, n, cols, tgt, kind) in enumerate(cards):
        x = 0.2 + i * (cw + 0.25)
        s.box(x, 0.2, cw, h - 0.4, '', fill=PAPER, lw=2, r=0.06)
        s.text(x + 0.2, h - 0.6, f, size=18, weight='bold', ha='left', mono=True)
        s.text(x + 0.25, h - 1.1, n, size=21, ha='left', color=BODY)
        s.text(x + 0.25, h - 1.7, 'inputs', size=19, ha='left', color=MUTE, weight='bold')
        for k, c in enumerate(cols):
            s.text(x + 0.25, h - 2.15 - k * 0.4, c, size=19, ha='left', mono=True)
        if nm == 'fares':
            s.text(x + 0.25, h - 2.15 - 3 * 0.4 + 0.05, 'left out: tip_ugx', size=18, ha='left', mono=True, color=RED, weight='bold')
        s.text(x + 0.25, 1.0, 'target', size=19, ha='left', color=MUTE, weight='bold')
        s.text(x + 0.25, 0.55, tgt, size=21, ha='left', mono=True, weight='bold', color=RED)
        s.text(x + cw - 0.2, 0.55, kind, size=19, ha='right', color=BODY)
    return s


@redraw('ml_trip_timeline')
def ml_trip_timeline(w, h, **_):
    s = Scene(w, h)
    y = 1.35
    s.arrow(0.2, y, w - 0.2, y, lw=3, head=22)
    bw = 2.3
    xs = [0.2 + bw / 2, w / 2, w - 0.2 - bw / 2]
    stations = [(xs[0], 'booking', 'distance_km\nrush_hour\nraining', 'known: inputs', GOLD, INK),
                (xs[1], 'ride ends', 'fare_ugx\nthe target', 'the answer', PAPER, INK),
                (xs[2], 'afterwards', 'tip_ugx', 'too late to use', PAPER, RED)]
    for x, t, sub, note, f, col in stations:
        s.circle(x, y, 0.13, fill=INK, z=5)
        s.box(x - bw / 2, y + 0.45, bw, 2.55, '', fill=f, lw=2.2, r=0.06, edge=col)
        s.text(x, y + 2.7, t, size=22, weight='bold', color=col)
        s.text(x, y + 1.7, sub, size=17, mono=True, color=col)
        s.text(x, y - 0.55, note, size=19, weight='bold', color=col)
    return s


@redraw('ml_plan_sizes')
def ml_plan_sizes(w, h, **_):
    s = Scene(w, h)
    cw = (w - 0.2 - 0.3) / 2
    for i, (ttl, q, ok, foot) in enumerate([('fits two weeks', 'Can distance and\nrush hour predict\na boda-boda fare?', True, 'data exists, and a\nnumber answers it'),
                                            ('too big', 'Can a computer\npredict everything\nabout Kampala?', False, 'no data, no number')]):
        x = 0.1 + i * (cw + 0.3)
        col = INK if ok else RED
        s.box(x, 0.3, cw, h - 0.6, '', fill=PAPER, lw=2.4, r=0.06, edge=col)
        s.text(x + cw / 2, h - 0.85, ttl, size=24, weight='bold', color=col)
        s.line(x + 0.3, h - 1.35, x + cw - 0.3, h - 1.35, color=HAIR, lw=1.4)
        s.text(x + cw / 2, h / 2 + 0.05, q, size=22)
        s.text(x + cw / 2, 0.95, foot, size=18, color=col if not ok else BODY)
    return s


@redraw('ml_plan_storyboard')
def ml_plan_storyboard(w, h, **_):
    s = Scene(w, h)
    rows = [('Question', 'Can distance, rush hour and rain predict a boda-boda fare?'), ('Dataset', 'synthetic_fares.csv, 150 invented trips'), ('Target', 'fare_ugx'),
            ('Inputs', 'distance_km, rush_hour, raining. Not tip_ugx.'), ('Baseline', 'the mean fare of the training trips'), ('Evaluation', 'mean absolute error in UGX, final test used once'), ('Limits', 'invented data, so no claim about real fares')]
    s.box(0.2, 0.1, w - 0.4, h - 0.2, '', fill=PAPER, lw=2, r=0.04)
    pitch = (h - 0.4) / len(rows)
    for i, (a, b) in enumerate(rows):
        y = h - 0.2 - pitch * (i + 0.5)
        s.text(0.55, y, a, size=22, weight='bold', ha='left', color=RED if a == 'Limits' else INK)
        s.text(2.8, y, b, size=22, ha='left')
        if i < len(rows) - 1:
            s.line(0.45, y - pitch / 2, w - 0.45, y - pitch / 2, color=HAIR, lw=1.2)
    return s


@redraw('ml_fare_baseline_gaps')
def ml_fare_baseline_gaps(w, h, **_):
    m = fares_models()
    d, tr, va, y = m['d'], m['tr'], m['va'], m['y']
    mean = y[tr].mean()
    s = Scene(w, h)
    ax = axes_in(s, 1.4, 0.95, 6.8, h - 1.65)
    xv = d['distance_km'].values[va]
    yv = y[va]
    ax.axhline(mean, color=RED, lw=3.4, zorder=2)
    for xi, yi in zip(xv, yv):
        ax.plot([xi, xi], [yi, mean], color=INK, lw=1.8, zorder=2)
    ax.scatter(xv, yv, s=90, facecolor=GOLD, edgecolor=INK, linewidth=1.6, zorder=4)
    ax.set_xlabel('distance (km)', fontsize=17)
    ax.set_ylabel('fare (UGX)', fontsize=17)
    ax.set_yticks([0, 10000, 20000])
    ax.set_yticklabels(['0', '10k', '20k'])
    s.text(4.8, h - 0.3, '30 validation trips and the plain guess', size=20, weight='bold')
    X = 8.6
    s.line(X, h - 1.1, X + 0.55, h - 1.1, color=RED, lw=3.6)
    s.text(X + 0.7, h - 1.1, 'the guess:', size=19, ha='left', weight='bold', color=RED)
    s.text(X, h - 1.65, f'always {money(mean)} UGX', size=21, ha='left', weight='bold', color=RED)
    s.line(X, h - 2.35, X + 0.55, h - 2.35, color=INK, lw=3)
    s.text(X + 0.7, h - 2.35, 'the average miss:', size=19, ha='left', weight='bold')
    s.box(X, h - 3.7, 2.9, 1.0, f'{money(m["base_val"])} UGX', size=30, fill=GOLD, weight='bold', r=0.05, mono=True)
    s.text(X, h - 4.15, 'the average black bar', size=17, ha='left', color=BODY)
    return s


@redraw('ml_scatter_read')
def ml_scatter_read(w, h, **_):
    d = fares()
    row = d.iloc[2]
    s = Scene(w, h)
    ax = axes_in(s, 1.5, 1.0, w - 1.9, h - 1.7)
    ax.scatter(d['distance_km'], d['fare_ugx'], s=40, facecolor=PAPER, edgecolor=INK, linewidth=1.3, zorder=2)
    ax.scatter([row['distance_km']], [row['fare_ugx']], s=300, facecolor=GOLD, edgecolor=INK, linewidth=2.4, zorder=4)
    ax.plot([row['distance_km']] * 2, [0, row['fare_ugx']], color=RED, lw=2.4, ls='--', zorder=3)
    ax.plot([0, row['distance_km']], [row['fare_ugx']] * 2, color=RED, lw=2.4, ls='--', zorder=3)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 26000)
    ax.set_xlabel('distance (km)', fontsize=18)
    ax.set_ylabel('fare (UGX)', fontsize=18)
    ax.set_yticks([0, 10000, 20000])
    ax.set_yticklabels(['0', '10k', '20k'])
    ax.text(0.5, 25500, f'the gold dot: {row["distance_km"]} km, {int(row["fare_ugx"]):,} UGX', fontsize=17, fontweight='bold', va='top', family=figkit.FONT)
    s.text(w / 2, h - 0.35, 'each dot is one trip', size=21, weight='bold')
    return s


@redraw('ml_bar_to_beat')
def ml_bar_to_beat(w, h, **_):
    m = fares_models()
    s = Scene(w, h)
    x0, top = 3.0, h - 0.9
    vmax = m['base_val']
    L = w - x0 - 0.6
    s.text(0.3, top, 'plain guess', size=24, weight='bold', ha='left')
    s.rect(x0, top - 0.4, L, 0.8, fill=GOLD, lw=2.4)
    s.text(x0 + L - 0.25, top, f'{money(vmax)}', size=28, weight='bold', mono=True, ha='right')
    y2 = top - 1.7
    s.text(0.3, y2, 'your model', size=24, weight='bold', ha='left')
    s.box(x0, y2 - 0.4, L * 0.55, 0.8, '?', size=28, weight='bold', dash=True, lw=2.2, r=0.02, edge=RED, color=RED)
    s.line(x0 + L, top - 0.45, x0 + L, y2 - 0.45, color=RED, lw=2.6, dash=True)
    s.line(x0 + L * 0.55, y2 - 0.45, x0 + L, y2 - 0.45, color=RED, lw=2.6, dash=True)
    s.text(x0, y2 - 0.85, 'must end shorter than the bar above', size=20, ha='left', color=RED, weight='bold')
    s.text(x0, 0.4, 'average miss on the 30 validation trips, in UGX', size=18, color=MUTE, ha='left')
    return s


# ---------------------------------------------------------------------------------------- session 21
@redraw('ml_same_split')
def ml_same_split(w, h, **_):
    s = Scene(w, h)
    cands = ['plain guess', 'distance only', 'distance, rush, rain']
    for i, c in enumerate(cands):
        y = h - 1.0 - i * 1.1
        s.box(0.2, y - 0.37, 2.9, 0.74, c, size=18, weight='bold', r=0.05)
        s.arrow(3.15, y, 4.0, h / 2 + 0.1, lw=1.8, head=12)
    s.box(4.05, h / 2 - 0.95, 1.85, 2.1, '', fill=BAND, lw=2.2, r=0.05)
    s.text(4.975, h / 2 + 0.6, 'the same', size=19, weight='bold')
    s.text(4.975, h / 2 + 0.1, '30 validation', size=18)
    s.text(4.975, h / 2 - 0.3, 'trips', size=18)
    s.arrow(5.95, h / 2 + 0.1, 6.35, h / 2 + 0.1, lw=2.2, head=14)
    s.text(7.05, h / 2 + 0.1, 'one\nerror\nmeasure', size=19, weight='bold')
    s.text(w / 2, 0.45, 'Same trips, same measure: the scores compare fairly.', size=18, color=BODY)
    return s


@redraw('ml_assistant_loop')
def ml_assistant_loop(w, h, **_):
    s = Scene(w, h)
    bw, bh = 2.2, 1.05
    ty, by = h - 1.0, 1.7
    boxes = [('ask', 0.3, ty), ('predict what\nthe hint does', 2.75, ty), ('run it', 5.2, ty), ('test it\nwith asserts', 5.2, by), ('keep or reject\nand log it', 2.75, by)]
    for t, x, y in boxes:
        s.box(x, y - bh / 2, bw, bh, t, size=19, weight='bold', r=0.06, fill=GOLD if 'test' in t else PAPER)
    s.arrow(0.3 + bw + 0.03, ty, 2.72, ty, lw=2.2, head=14)
    s.arrow(2.75 + bw + 0.03, ty, 5.17, ty, lw=2.2, head=14)
    s.arrow(5.2 + bw / 2, ty - bh / 2 - 0.03, 5.2 + bw / 2, by + bh / 2 + 0.03, lw=2.2, head=14)
    s.arrow(5.17, by, 2.75 + bw + 0.03, by, lw=2.2, head=14)
    s.text(1.4, by, 'A plausible answer\nis not a checked\nanswer.', size=20, weight='bold', color=RED)
    s.text(w / 2, 0.45, 'Treat every suggestion as a hint to test.', size=18, color=BODY)
    return s


@redraw('ml_total_bug')
def ml_total_bug(w, h, side='plus', **_):
    s = Scene(w, h)
    op, res, ok, note = ('+', '2003', False, 'plus adds the numbers') if side == 'plus' else ('*', '6000', True, 'times gives the price of 3')
    s.code(0.1, h - 0.15, ['def total(price, quantity):', f'    return price {op} quantity', '', 'total(2000, 3)'], size=17, line_h=0.4, pad=0.18, w=w - 0.2)
    s.text(1.2, 1.3, res, size=40, weight='bold', mono=True, color=INK if ok else RED)
    s.text(w - 1.5, 1.3, 'right' if ok else 'wrong', size=24, weight='bold', color=INK if ok else RED)
    s.text(w / 2, 0.4, note, size=19, color=BODY)
    return s


@redraw('ml_decision_card')
def ml_decision_card(w, h, **_):
    m = fares_models()
    s = Scene(w, h)
    s.box(0.25, 0.25, w - 0.5, h - 0.5, '', fill=PAPER, lw=2.4, r=0.05)
    s.text(0.7, h - 0.8, 'Decision', size=26, weight='bold', ha='left')
    s.text(0.7, h - 1.85, 'I keep distance, rush hour and\nrain as inputs.', size=22, ha='left')
    s.text(0.7, h - 3.0, f'Validation error {money(m["val"]["three"])} UGX,\nagainst {money(m["base_val"])} for the plain guess.', size=22, ha='left')
    s.text(0.7, h - 4.15, 'I leave out tip_ugx: it is known\nonly after the trip.', size=22, ha='left', color=RED, weight='bold')
    return s


# ---------------------------------------------------------------------------------------- session 22
@redraw('ml_val_vs_test')
def ml_val_vs_test(w, h, **_):
    m = fares_models()
    s = Scene(w, h)
    ax = axes_in(s, 0.9, 0.95, w - 1.3, h - 2.4)
    x = np.arange(2)
    base = [m['base_val'], m['base_test']]
    mod = [m['val']['three'], m['test_three']]
    b1 = ax.bar(x - 0.2, base, 0.36, color=PAPER, edgecolor=INK, linewidth=2)
    b2 = ax.bar(x + 0.2, mod, 0.36, color=GOLD, edgecolor=INK, linewidth=2)
    for bars, vals in ((b1, base), (b2, mod)):
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 60, f'{v:,.0f}', ha='center', va='bottom', fontsize=17, fontweight='bold', family=figkit.FONT)
    ax.set_xticks(x)
    ax.set_xticklabels(['validation trips', 'final test trips'], fontsize=18)
    ax.set_ylim(0, 6200)
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    s.rect(0.9, h - 1.2, 0.3, 0.3, fill=PAPER, lw=2)
    s.text(1.35, h - 1.05, 'plain guess', size=19, ha='left')
    s.rect(3.6, h - 1.2, 0.3, 0.3, fill=GOLD, lw=2)
    s.text(4.05, h - 1.05, 'model', size=19, ha='left')
    s.text(w / 2, h - 0.4, 'average miss (UGX)', size=21, weight='bold')
    s.text(w / 2, 0.3, 'The lead is smaller on the test, and that is normal.', size=17, color=BODY)
    return s


@redraw('ml_handover_checklist')
def ml_handover_checklist(w, h, **_):
    s = Scene(w, h)
    items = ['the data file sits beside the notebook', 'Restart and Run All works from the top', 'the data origin is stated, and it is invented', 'validation and final test are reported apart', 'limits are written next to the result']
    pitch = (h - 0.4) / len(items)
    for i, t in enumerate(items):
        y = h - 0.2 - pitch * (i + 0.5)
        num_dot(s, 0.7, y, i + 1)
        s.text(1.3, y, t, size=24, ha='left')
    return s


@redraw('ml_one_page_report')
def ml_one_page_report(w, h, **_):
    s = Scene(w, h)
    s.box(0.4, 0.2, 5.0, h - 0.4, '', fill=PAPER, lw=2.4, r=0.03)
    heads = ['Question', 'Data and method', 'Result, with the baseline', 'Limit', 'Next step']
    pitch = (h - 0.6) / len(heads)
    for i, name in enumerate(heads):
        y = h - 0.5 - i * pitch
        s.text(0.75, y, name, size=19, weight='bold', ha='left')
        for k in range(2):
            s.line(0.75, y - 0.3 - k * 0.2, 5.05, y - 0.3 - k * 0.2, color=HAIR, lw=1.8, z=4)
    s.line(5.75, 0.3, 5.75, h - 0.3, lw=2.2)
    s.line(5.6, 0.3, 5.75, 0.3, lw=2.2)
    s.line(5.6, h - 0.3, 5.75, h - 0.3, lw=2.2)
    s.text(6.0, h / 2, 'one page,\nfive parts', size=24, weight='bold', ha='left')
    return s
# ======================================================================================== sessions 23 to 25 and labs F03, F04
@redraw('ml_parent_five_slides')
def ml_parent_five_slides(w, h, **_):
    s = Scene(w, h)
    cards = [('1', 'Question', 'distance, rush\nhour and rain:\na fare?'), ('2', 'Data', '150 invented\ntrips'), ('3', 'Test', 'a plain guess,\nthen the model'),
             ('4', 'Result', 'the error in UGX\nbeside the\nbaseline'), ('5', 'Limit', 'what it\ncannot tell')]
    cw, gap = 2.12, 0.3
    x0 = (w - (5 * cw + 4 * gap)) / 2
    for i, (n, t, sub) in enumerate(cards):
        x = x0 + i * (cw + gap)
        s.box(x, 0.95, cw, 3.1, '', fill=GOLD if t == 'Result' else PAPER, lw=2.2, r=0.04, edge=RED if t == 'Limit' else INK)
        s.text(x + cw / 2, 3.6, t, size=24, weight='bold', color=RED if t == 'Limit' else INK)
        s.text(x + cw / 2, 2.35, sub, size=18)
        s.text(x + 0.25, 1.3, n, size=18, weight='bold', color=MUTE, ha='left')
        if i < 4:
            s.arrow(x + cw + 0.03, 2.5, x + cw + gap - 0.03, 2.5, lw=2, head=12)
    s.text(w / 2, 0.45, 'five slides, five minutes, no jargon', size=20, weight='bold')
    return s


@redraw('ml_claim_evidence')
def ml_claim_evidence(w, h, **_):
    m = fares_models()
    s = Scene(w, h)
    s.box(0.2, h - 1.9, w - 0.4, 1.6, 'Claim: the model guesses fares\nbetter than a plain guess.', size=22, weight='bold', fill=GOLD, lw=2.2, r=0.05)
    s.arrow(w / 2, h - 1.95, w / 2, h - 2.6, lw=2.2, head=14)
    bw = (w - 0.4 - 0.3) / 2
    for i, (ttl, txt) in enumerate([('evidence one', f'the plain guess\nmisses by\n{money(m["base_test"])} UGX'), ('evidence two', f'the model\nmisses by\n{money(m["test_three"])} UGX')]):
        x = 0.2 + i * (bw + 0.3)
        s.box(x, 0.4, bw, 2.1, '', lw=2.2, r=0.05)
        s.text(x + bw / 2, 2.15, ttl, size=19, weight='bold', color=MUTE)
        s.text(x + bw / 2, 1.2, txt, size=23)
    return s


@redraw('ml_audience_cards')
def ml_audience_cards(w, h, **_):
    s = Scene(w, h)
    rows = [('a parent hears', 'It guesses the fare from the distance.\nIt was tested on trips it never saw.', GOLD),
            ('a classmate hears', 'Linear regression with three inputs,\ncompared with a mean baseline.', PAPER)]
    ch = 2.15
    for i, (who, say, f) in enumerate(rows):
        y = h - 0.2 - ch - i * (ch + 0.2)
        s.box(0.2, y, w - 0.4, ch, '', fill=f, lw=2.2, r=0.05)
        s.text(0.5, y + ch - 0.45, who, size=21, weight='bold', ha='left')
        s.text(0.5, y + 0.8, say, size=22, ha='left')
    return s


@redraw('ml_demo_backup')
def ml_demo_backup(w, h, **_):
    s = Scene(w, h)
    s.box(0.2, h - 2.1, 2.7, 1.8, 'live demo', size=24, weight='bold', r=0.05)
    s.arrow(2.95, h - 1.2, 4.0, h - 1.2, color=RED, lw=2.6, head=18)
    s.text(3.5, h - 0.75, 'fails', size=20, weight='bold', color=RED)
    s.box(4.05, h - 2.1, 3.45, 1.8, 'backup: a screenshot\nof the saved output', size=20, weight='bold', r=0.05, fill=GOLD)
    s.box(0.2, 0.3, w - 0.4, 1.9, 'Did an AI assistant help you?\nSay so on the last slide.', size=24, weight='bold', r=0.05, edge=RED, color=RED, lw=2.6)
    return s


@redraw('ml_showcase_run')
def ml_showcase_run(w, h, **_):
    s = Scene(w, h)
    steps = [('present', 'your five\nslides'), ('explain', 'what the\nnumber means'), ('answer', 'questions\nfrom the room'), ('change', 'one small thing,\nunaided')]
    cw, gap = 2.6, 0.45
    x0 = (w - (4 * cw + 3 * gap)) / 2
    for i, (t, sub) in enumerate(steps):
        x = x0 + i * (cw + gap)
        s.box(x, 1.2, cw, 2.9, '', fill=GOLD if t == 'change' else PAPER, lw=2.2, r=0.05)
        s.text(x + cw / 2, 3.35, t, size=28, weight='bold')
        s.text(x + cw / 2, 2.2, sub, size=20)
        s.text(x + 0.25, 1.55, str(i + 1), size=19, weight='bold', color=MUTE, ha='left')
        if i < 3:
            s.arrow(x + cw + 0.05, 2.65, x + cw + gap - 0.05, 2.65, lw=2.2, head=14)
    s.text(w / 2, 0.5, 'Your work, your voice, nothing to lean on but what you know.', size=19, color=BODY)
    return s


@redraw('ml_portfolio_next')
def ml_portfolio_next(w, h, **_):
    s = Scene(w, h)
    bw = 3.3
    s.box(0.1, 0.25, bw, h - 0.5, '', lw=2.2, r=0.05)
    s.text(0.1 + bw / 2, h - 0.75, 'your portfolio', size=22, weight='bold')
    for i, t in enumerate(['the handover\nnotebook', 'the data file', 'the one-page\nreport', 'the AI use log']):
        y = h - 1.6 - i * 0.88
        num_dot(s, 0.5, y, i + 1, r=0.22)
        s.text(0.9, y, t, size=19, ha='left')
    s.arrow(0.1 + bw + 0.1, h / 2, 0.1 + bw + 0.55, h / 2, lw=2.6, head=18)
    x2 = 0.1 + bw + 0.65
    s.box(x2, 0.25, w - x2 - 0.1, h - 0.5, '', lw=2.2, r=0.05, fill=GOLD)
    s.text(x2 + (w - x2 - 0.1) / 2, h - 0.75, 'one next step', size=22, weight='bold')
    for i, t in enumerate(['a new\nquestion', 'real data, with\npermission', 'a bigger model,\ntested fairly']):
        y = h - 1.9 - i * 1.15
        s.text(x2 + 0.25, y, t, size=19, ha='left')
    return s


@redraw('ml_unaided_change')
def ml_unaided_change(w, h, **_):
    s = Scene(w, h)
    s.code(0.15, h - 0.4, ['model = LinearRegression()', 'model.fit(X_train, y_train)', 'print(mae)'], size=19, line_h=0.46, pad=0.2, w=5.05, hl_lines=(1,))
    s.arrow(5.3, h - 1.1, 5.75, h - 1.1, lw=2.4, head=16)
    s.box(5.8, h - 2.0, 1.75, 1.8, 'change\none thing', size=20, weight='bold', r=0.05, fill=GOLD)
    s.text(w / 2, 2.2, 'Predict the result, run it,\nand explain the difference.', size=21, weight='bold')
    s.text(w / 2, 1.0, 'If it breaks, read the last line\nof the message first.', size=19, color=BODY)
    return s


# ---------------------------------------------------------------------------------------- F03
def _strip2(s, x0, L, y, vals, vmax=8, mean=4, size=18):
    s.line(x0, y, x0 + L, y, lw=2)
    for t in range(vmax + 1):
        s.line(x0 + t * L / vmax, y - 0.08, x0 + t * L / vmax, y + 0.08, lw=1.6)
        s.text(x0 + t * L / vmax, y - 0.38, str(t), size=size, color=BODY)
    seen = {}
    for v in vals:
        k = seen.get(v, 0)
        seen[v] = k + 1
        s.circle(x0 + v * L / vmax, y + 0.32 + k * 0.36, 0.16, fill=GOLD, lw=2, z=4)
    s.line(x0 + mean * L / vmax, y - 0.05, x0 + mean * L / vmax, y + 1.55, color=RED, lw=3, dash=True, z=3)


@redraw('ml_same_mean_spread')
def ml_same_mean_spread(w, h, **_):
    s = Scene(w, h)
    x0, L = 1.4, w - 3.0
    ya, yb = h - 1.45, 1.05
    _strip2(s, x0, L, ya, [2, 2, 6, 6])
    _strip2(s, x0, L, yb, [4, 4, 4, 4])
    s.text(0.3, ya + 0.6, 'A', size=26, weight='bold', ha='left')
    s.text(0.3, yb + 0.6, 'B', size=26, weight='bold', ha='left')
    xm = x0 + 4.35 * L / 8
    s.text(xm, ya + 1.0, 'mean 4, spread 2', size=21, weight='bold', ha='left')
    s.text(xm, yb + 1.0, 'mean 4, spread 0', size=21, weight='bold', ha='left')
    s.text(w / 2, 0.2, 'Same mean, different groups: the red line is the mean', size=19, color=RED, weight='bold')
    return s


@redraw('ml_prob_vs_fraction')
def ml_prob_vs_fraction(w, h, **_):
    throws = np.random.RandomState(5).randint(1, 7, 10)
    k = int((throws > 4).sum())
    s = Scene(w, h)
    s.text(1.5, h - 0.45, 'a fair die', size=21, weight='bold')
    for i in range(6):
        s.box(0.25 + (i % 3) * 0.6, h - 1.25 - (i // 3) * 0.6, 0.52, 0.52, str(i + 1), size=18, weight='bold', fill=GOLD if i + 1 > 4 else PAPER, lw=1.8, r=0.04)
    s.text(1.05, h - 2.85, '2 faces of 6\nare above 4:\nprobability 2/6', size=17)
    s.text(5.5, h - 0.45, 'ten throws', size=21, weight='bold')
    for i, v in enumerate(throws):
        s.box(3.85 + (i % 5) * 0.66, h - 1.25 - (i // 5) * 0.66, 0.58, 0.58, str(v), size=18, weight='bold', fill=GOLD if v > 4 else PAPER, lw=1.8, r=0.04)
    s.text(5.5, h - 2.85, f'{k} of 10 are above 4:\nobserved fraction {k}/10', size=17)
    s.text(w / 2, 0.75, 'The fraction you saw is not the probability.', size=19, weight='bold', color=BODY)
    s.text(w / 2, 0.3, 'It does not promise what the next throw gives.', size=18, color=BODY)
    return s


# ---------------------------------------------------------------------------------------- F04
@redraw('ml_matrix_grid')
def ml_matrix_grid(w, h, **_):
    s = Scene(w, h)
    x0, y0, c = 1.6, h - 1.35, 1.15
    s.text(x0 + c / 2, y0 + 0.4, 'area_m2', size=18, mono=True)
    s.text(x0 + 1.5 * c, y0 + 0.4, 'rooms', size=18, mono=True)
    vals = [[40, 2], [60, 3]]
    for r in range(2):
        s.text(x0 - 0.15, y0 - r * c - c / 2, f'home {r}', size=18, ha='right', color=MUTE)
        for k in range(2):
            s.box(x0 + k * c, y0 - (r + 1) * c, c, c, str(vals[r][k]), size=28, weight='bold', fill=GOLD if (r, k) == (0, 1) else PAPER, lw=2, r=0.03)
    s.brace(x0, x0 + 2 * c, y0 - 2 * c - 0.12, depth=-0.12)
    s.text(x0 + c, y0 - 2 * c - 0.55, 'shape (2, 2)', size=20, weight='bold')
    s.text(x0 + c, y0 - 2 * c - 0.95, 'rows by columns', size=18, color=BODY)
    s.text(x0 + 2 * c + 0.25, y0 - c, 'homes[0, 1] is 2:\nrow 0, column 1', size=19, ha='left', color=RED, weight='bold')
    s.arrow(x0 + 2 * c + 0.2, y0 - 0.6, x0 + 2 * c - 0.25, y0 - 0.6, color=RED, lw=2.2, head=14) if False else None
    return s


@redraw('ml_slope_step')
def ml_slope_step(w, h, **_):
    s = Scene(w, h)
    for i, (a, v) in enumerate([(40, '260,000'), (41, '263,000')]):
        x = 0.4 + i * 3.9
        s.box(x, 1.5, 2.6, 2.5, '', fill=PAPER, lw=2.2, r=0.05)
        s.text(x + 1.3, 3.5, f'{a} m2', size=24, weight='bold')
        s.text(x + 1.3, 2.8, '2 rooms', size=19, color=BODY)
        s.text(x + 1.3, 2.0, v, size=26, weight='bold', mono=True)
    s.arrow(3.1, 2.75, 4.2, 2.75, color=RED, lw=2.4, head=16)
    s.text(3.65, 3.15, '+1 m2', size=18, weight='bold', color=RED)
    s.text(w / 2, 4.5, 'rent rises by 3,000', size=22, weight='bold', color=RED)
    s.text(w / 2, 0.85, 'The slope is the change in rent', size=19, color=BODY)
    s.text(w / 2, 0.4, 'for one more square metre, rooms held fixed.', size=19, color=BODY)
    return s


@redraw('ml_matrix_rows')
def ml_matrix_rows(w, h, **_):
    s = Scene(w, h)
    rows = [['home', 'area_m2', 'rooms', 'rent'], ['0', '40', '2', '260,000'], ['1', '60', '3', '340,000'], ['2', '50', '2', '290,000']]
    s.table(0.3, h - 0.4, [1.2, 1.7, 1.4, 2.1], 0.75, rows, size=20, hl_rows=(3,), mono_cols=(1, 2, 3))
    s.text(w / 2, 1.2, 'the new row [50, 2] gives shape (3, 2)', size=21, weight='bold')
    s.text(w / 2, 0.6, 'The weights stay the same, so the rule does not change.', size=18, color=BODY)
    return s


@redraw('ml_weighted_sum')
def ml_weighted_sum(w, h, **_):
    s = Scene(w, h)
    tiles = [('100000', 'intercept:\nthe starting amount'), ('3000 x 40', 'weight for area\ntimes the area'), ('20000 x 2', 'weight for rooms\ntimes the rooms'), ('260000', 'the predicted\nrent, UGX')]
    tw = 2.4
    gap = (w - 0.4 - 4 * tw) / 3
    for i, (a, b) in enumerate(tiles):
        x = 0.2 + i * (tw + gap)
        s.box(x, h / 2 - 0.05, tw, 1.15, a, size=23, weight='bold', mono=True, fill=GOLD if i == 3 else PAPER, lw=2.2, r=0.05)
        s.text(x + tw / 2, h / 2 - 0.8, b, size=18, color=BODY)
        if i < 3:
            s.text(x + tw + gap / 2, h / 2 + 0.5, '=' if i == 2 else '+', size=32, weight='bold')
    s.text(w / 2, h - 0.5, 'A weighted sum: multiply each input by its weight, then add', size=21, weight='bold')
    s.text(w / 2, 0.45, 'invented numbers for teaching, not real Kampala rents', size=17, color=RED)
    return s


# ---------------------------------------------------------------------------------------- ML25
@redraw('ml_neuron_net')
def ml_neuron_net(w, h, **_):
    s = Scene(w, h)
    layers = [(4, 'four\nmeasurements'), (8, 'eight hidden\nunits'), (3, 'three\nspecies')]
    xs = [1.9, w / 2, w - 1.9]
    pos = []
    for (n, _), x in zip(layers, xs):
        gap = min(0.5, (h - 2.1) / max(n - 1, 1))
        pos.append([(x, h / 2 + 0.55 + (n - 1) * gap / 2 - i * gap) for i in range(n)])
    for a, b in zip(pos[:-1], pos[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b:
                s.line(x1, y1, x2, y2, color=HAIR, lw=0.9, z=1)
    for lay, col in zip(pos, [PAPER, GOLD, PAPER]):
        for (x, y) in lay:
            s.circle(x, y, 0.17, fill=col, lw=1.8, z=3)
    for (n, t), x in zip(layers, xs):
        s.text(x, 0.6, t, size=21, weight='bold')
    return s


@redraw('ml_scale_inputs')
def ml_scale_inputs(w, h, **_):
    s = Scene(w, h)
    names = ['sepal length', 'sepal width', 'petal length', 'petal width']
    raw = [(4.3, 7.9), (2.0, 4.4), (1.0, 6.9), (0.1, 2.5)]
    z = [(-1.87, 2.49), (-2.43, 3.09), (-1.57, 1.79), (-1.45, 1.71)]   # (x - mean) / std over the 150 iris flowers
    lx = 2.65
    s.text(0.2, h - 0.35, 'before scaling: cm', size=20, weight='bold', ha='left')
    X1 = lambda v: lx + 0.2 + v * 0.6
    for i, (n, (a, b)) in enumerate(zip(names, raw)):
        y = h - 0.95 - i * 0.42
        s.text(lx, y, n, size=17, ha='right')
        s.rect(X1(a), y - 0.14, (b - a) * 0.6, 0.28, fill=GOLD, lw=1.6)
    s.text(0.2, 2.2, 'after scaling: centred on 0', size=20, weight='bold', ha='left')
    X2 = lambda v: lx + 2.3 + v * 0.8
    for i, (n, (a, b)) in enumerate(zip(names, z)):
        y = 1.65 - i * 0.38
        s.text(lx, y, n, size=17, ha='right')
        s.rect(X2(a), y - 0.13, (b - a) * 0.8, 0.26, fill=GOLD, lw=1.6)
    s.line(X2(0), 0.0, X2(0), 1.95, color=RED, lw=2.2, dash=True, z=5)
    s.text(X2(0) + 0.15, 0.2, '0', size=17, weight='bold', color=RED, ha='left')
    return s


@redraw('ml_model_trio')
def ml_model_trio(w, h, **_):
    s = Scene(w, h)
    names = ['majority baseline', 'tree, depth 3', 'small network']
    for i, n in enumerate(names):
        y = h - 1.1 - i * 1.15
        s.box(0.2, y - 0.4, 2.9, 0.8, n, size=19, weight='bold', r=0.05, fill=GOLD if i == 2 else PAPER)
        s.arrow(3.15, y, 3.95, h / 2 + 0.3 + (1 - i) * 0.3, lw=1.8, head=12)
    s.box(4.0, h / 2 - 0.55, 1.85, 1.9, '', fill=BAND, lw=2.2, r=0.05)
    s.text(4.925, h / 2 + 0.7, 'the same', size=19, weight='bold')
    s.text(4.925, h / 2 + 0.05, 'validation\nflowers', size=19)
    s.arrow(5.9, h / 2 + 0.4, 6.3, h / 2 + 0.4, lw=2.2, head=14)
    s.text(6.35, h / 2 + 0.4, 'accuracy', size=19, weight='bold', ha='left')
    s.text(w / 2, 0.9, 'Bigger is not automatically better.', size=20, weight='bold')
    s.text(w / 2, 0.4, 'Compare on the same flowers.', size=18, color=BODY)
    return s

_apply_bumps(_OVERRIDE)
