"""Repaired Machine Learning illustrations for sessions 1 to 12 and labs F01 and F02 (review round 3).

Shared foundation figures keep their c_ names for the Data Analysis decks, so the Machine Learning decks use ml_r3_ copies.
Session 7 to 12 figures replace the ml_ figures of the same name (this module is imported after figs_ml).
Text is 16 pt or larger everywhere. Numbers come from camp_2026/data or from numpy.
"""
import math

import numpy as np
import pandas as pd
from matplotlib.patches import Arc, Polygon

from brand import INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD
from figkit import Scene, fig, FONT
from figs_common import scatter_axes, fit_line, Code, label_under, axes_xy, fit_mono, vstr, run_lines, MONO_EM, shop as shop_c, draw_house
from figs_ml import axes_in, data_table, shop_raw, shop as shop_rev, homes, fares


# ====================================================================== word icons (1.3 x 1.3 in)
def _fork(s, n, hi):
    s.circle(0.2, 0.65, 0.09, fill=INK, edge=INK)
    ys = {1: [0.65], 2: [1.0, 0.3], 3: [1.05, 0.65, 0.25]}[n]
    for k, y in enumerate(ys):
        s.line(0.28, 0.65, 0.85, y, color=INK, lw=2.4)
        s.box(0.85, y - 0.12, 0.35, 0.24, '', fill=GOLD if k == hi else PAPER, lw=1.8, r=0.02)


@fig('ml_r3_wicon')
def ml_r3_wicon(w, h, kind='parens', **_):
    s = Scene(w, h)
    cx, cy = w / 2, h / 2
    if kind == 'parens':
        s.text(cx, cy + 0.02, '( )', size=48, weight='bold', mono=True)
        s.box(0.4, 0.15, 0.5, 0.14, '', fill=GOLD, lw=1.6, r=0.02)
    elif kind == 'indent':
        for k, (x0, ww, f) in enumerate([(0.12, 0.8, INK), (0.4, 0.7, GOLD), (0.4, 0.55, GOLD), (0.12, 0.65, INK)]):
            s.box(x0, 1.05 - k * 0.3, ww, 0.15, '', fill=f, edge=INK, lw=1.4, r=0.02)
        s.arrow(0.1, 0.45, 0.36, 0.45, color=RED, lw=2.2, head=12)
    elif kind == 'comment':
        s.text(0.38, cy + 0.12, '#', size=52, weight='bold', mono=True, color=RED)
        for k in range(2):
            s.line(0.62, cy + 0.3 - k * 0.3, 1.2, cy + 0.3 - k * 0.3, color=GREY, lw=3)
        s.line(0.2, 0.2, 1.15, 0.2, color=HAIR, lw=2)
    elif kind == 'convert':
        s.box(0.06, 0.45, 0.42, 0.4, '"7"', size=14, mono=True, fill=GOLD, lw=1.8, r=0.03)
        s.arrow(0.52, 0.65, 0.77, 0.65, color=RED, lw=2.4, head=13)
        s.box(0.82, 0.45, 0.42, 0.4, '7', size=20, mono=True, weight='bold', lw=1.8, r=0.03)
    elif kind == 'error':
        s.poly([(cx, 1.15), (0.1, 0.18), (1.2, 0.18)], fill=PAPER, edge=RED, lw=3)
        s.text(cx, 0.5, '!', size=40, weight='bold', color=RED)
    elif kind == 'trace':
        s.box(0.12, 0.15, 1.06, 1.0, '', fill=PAPER, edge=RED, lw=2.4, r=0.05)
        for k, y in enumerate([1.0, 0.8, 0.6]):
            s.line(0.25, y, 0.25 + 0.7 - k * 0.15, y, color=GREY, lw=3, z=4)
        s.line(0.25, 0.35, 0.9, 0.35, color=RED, lw=4, z=4)
    elif kind == 'integer':
        s.box(0.1, 0.35, 1.1, 0.6, '3', size=26, mono=True, weight='bold', fill=PAPER, lw=2.2, r=0.05)
    elif kind == 'float':
        s.box(0.1, 0.35, 1.1, 0.6, '2.5', size=24, mono=True, weight='bold', fill=PAPER, lw=2.2, r=0.05)
    elif kind == 'compare':
        s.text(cx, cy + 0.1, 'a < b', size=26, weight='bold', mono=True)
        s.text(cx, 0.28, '?', size=30, weight='bold', color=RED)
    elif kind == 'bool':
        s.box(0.15, 0.7, 1.0, 0.4, 'True', size=16, weight='bold', fill=GOLD, lw=1.8, r=0.04)
        s.box(0.15, 0.2, 1.0, 0.4, 'False', size=16, weight='bold', fill=PAPER, lw=1.8, r=0.04)
    elif kind == 'if':
        _fork(s, 2, 0)
        s.text(0.28, 1.15, 'if', size=16, weight='bold', mono=True, ha='center')
    elif kind == 'else':
        _fork(s, 2, 1)
        s.text(0.3, 1.15, 'else', size=16, weight='bold', mono=True, ha='center')
    elif kind == 'elif':
        _fork(s, 3, 1)
    elif kind == 'index':
        s.cells(0.12, 0.55, ['a', 'b', 'c'], w=0.35, h=0.4, size=16, labels=[0, 1, 2], label_size=16, hl=[1], label_color=RED)
    elif kind == 'list':
        s.cells(0.2, 0.45, ['', '', ''], w=0.3, h=0.4, size=16)
        s.line(0.12, 0.35, 0.12, 0.95, color=INK, lw=3)
        s.line(0.12, 0.35, 0.2, 0.35, color=INK, lw=3)
        s.line(0.12, 0.95, 0.2, 0.95, color=INK, lw=3)
        s.line(1.18, 0.35, 1.18, 0.95, color=INK, lw=3)
        s.line(1.18, 0.35, 1.1, 0.35, color=INK, lw=3)
        s.line(1.18, 0.95, 1.1, 0.95, color=INK, lw=3)
    elif kind == 'dict':
        for k in range(2):
            y = 0.72 - k * 0.5
            s.box(0.08, y, 0.5, 0.38, 'key', size=14, weight='bold', fill=GOLD, lw=1.8, r=0.03)
            s.box(0.62, y, 0.6, 0.38, 'value', size=14, fill=PAPER, lw=1.8, r=0.03)
    elif kind == 'item':
        s.cells(0.1, 0.35, ['', '', '', ''], w=0.28, h=0.35, hl=[2])
        s.arrow(0.1 + 2.5 * 0.28, 1.15, 0.1 + 2.5 * 0.28, 0.76, color=RED, lw=2.4, head=13)
    elif kind == 'func':
        s.arrow(0.03, cy, 0.33, cy, color=INK, lw=2.4, head=12)
        s.box(0.35, 0.25, 0.6, 0.8, 'f', size=30, weight='bold', fill=INK, color=PAPER, lw=2, r=0.05)
        s.arrow(0.97, cy, 1.27, cy, color=INK, lw=2.4, head=12)
    elif kind == 'return':
        s.box(0.06, 0.3, 0.6, 0.7, '', fill=PAPER, lw=2.2, r=0.05)
        s.arrow(0.7, cy, 0.9, cy, color=RED, lw=2.6, head=13)
        s.box(0.93, 0.45, 0.32, 0.4, '8', size=18, mono=True, weight='bold', fill=GOLD, lw=1.8, r=0.03)
    elif kind == 'assert':
        s.text(cx, 0.9, '==', size=34, weight='bold', mono=True)
        s.box(0.2, 0.2, 0.9, 0.42, 'pass', size=16, weight='bold', fill=GOLD, lw=1.8, r=0.04)
    elif kind == 'slot':
        s.box(0.1, 0.15, 1.1, 1.0, '', fill=INK, edge=INK, lw=1.6, r=0.06)
        s.box(0.2, 0.45, 0.9, 0.4, 'price', size=15, mono=True, fill=PAPER, lw=1.8, r=0.03, dash=True)
    elif kind == 'arg':
        s.box(0.28, 1.0, 0.74, 0.28, '2000', size=14, mono=True, weight='bold', fill=GOLD, lw=1.8, r=0.03)
        s.arrow(cx, 0.98, cx, 0.6, color=RED, lw=2.4, head=13)
        s.box(0.2, 0.15, 0.9, 0.4, '', fill=PAPER, lw=1.8, r=0.03, dash=True)
    elif kind == 'topdown':
        for k in range(3):
            s.line(0.5, 1.0 - k * 0.32, 1.15 - k * 0.12, 1.0 - k * 0.32, color=INK, lw=3.4)
        s.arrow(0.2, 1.15, 0.2, 0.2, color=RED, lw=2.6, head=14)
    elif kind == 'update':
        s.box(0.06, 0.45, 0.4, 0.4, '3', size=18, mono=True, lw=1.8, r=0.03, color=GREY)
        s.line(0.04, 0.4, 0.48, 0.9, color=RED, lw=3)
        s.arrow(0.5, 0.65, 0.75, 0.65, color=INK, lw=2.2, head=12)
        s.box(0.8, 0.45, 0.42, 0.4, '4', size=18, mono=True, weight='bold', fill=GOLD, lw=1.8, r=0.03)
    elif kind == 'vector':
        s.cells(0.15, 0.5, ['40', '2'], w=0.5, h=0.42, size=16, mono=True, labels=['area', 'rooms'], label_size=14, hl=[0])
    elif kind == 'array':
        for r in range(2):
            for c in range(3):
                s.box(0.1 + c * 0.37, 0.3 + (1 - r) * 0.45, 0.35, 0.42, str(r * 3 + c + 1), size=16, mono=True, fill=GOLD if r == 0 else PAPER, lw=1.8, r=0.02)
    elif kind == 'elementwise':
        for c in range(3):
            x = 0.1 + c * 0.4
            s.box(x, 0.95, 0.34, 0.3, str(c + 1), size=14, mono=True, lw=1.6, r=0.02)
            s.arrow(x + 0.17, 0.92, x + 0.17, 0.58, color=RED, lw=2, head=10)
            s.box(x, 0.25, 0.34, 0.3, str(2 * (c + 1)), size=14, mono=True, fill=GOLD, lw=1.6, r=0.02)
    elif kind == 'unit':
        s.text(cx, 0.85, 'm²', size=40, weight='bold')
        s.line(0.15, 0.4, 1.15, 0.4, color=INK, lw=2.4)
        for k in range(6):
            s.line(0.15 + k * 0.2, 0.4, 0.15 + k * 0.2, 0.28, color=INK, lw=2)
    elif kind == 'value':
        s.box(0.1, 0.35, 1.1, 0.6, '2000', size=22, mono=True, weight='bold', fill=GOLD, lw=2.2, r=0.05)
    elif kind == 'type':
        for k, t in enumerate(['int', 'float', 'str']):
            s.box(0.15, 0.88 - k * 0.38, 1.0, 0.32, t, size=14, weight='bold', mono=True, fill=GOLD if k == 0 else PAPER, lw=1.6, r=0.03)
    elif kind == 'funnel':
        s.poly([(0.12, 1.1), (1.18, 1.1), (0.75, 0.55), (0.75, 0.15), (0.55, 0.25), (0.55, 0.55)], fill=GOLD, edge=INK, lw=2.2)
    elif kind == 'sum':
        s.text(cx, cy, 'Σ', size=64, weight='bold')
    elif kind == 'percentile':
        s.box(0.1, 0.3, 1.1, 0.4, '', fill=PAPER, lw=2, r=0.02)
        s.box(0.1, 0.3, 0.825, 0.4, '', fill=GOLD, lw=2, r=0.02)
        s.text(cx, 0.95, '75%', size=22, weight='bold')
    elif kind == 'missing':
        for r in range(2):
            for c in range(2):
                miss = r == 1 and c == 1
                s.box(0.18 + c * 0.5, 0.2 + (1 - r) * 0.5, 0.46, 0.46, '?' if miss else '', size=22, weight='bold', color=RED, fill=PAPER, lw=1.8, r=0.01, dash=miss, edge=RED if miss else INK)
    elif kind == 'noindex':
        for k in range(3):
            s.text(0.4, 1.0 - k * 0.3, str(k), size=18, mono=True, color=GREY)
        s.line(0.15, 0.2, 0.65, 1.15, color=RED, lw=3.2)
        s.box(0.7, 0.2, 0.5, 0.95, '', fill=GOLD, lw=1.8, r=0.02)
    elif kind == 'axis':
        s.line(0.3, 0.2, 0.3, 1.1, color=INK, lw=2.4)
        s.line(0.3, 0.2, 1.2, 0.2, color=INK, lw=2.4)
        s.text(0.14, 0.7, 'UGX', size=14, rot=90, weight='bold', color=RED)
        for k in range(3):
            s.box(0.5 + k * 0.23, 0.2, 0.17, 0.25 + k * 0.2, '', fill=PAPER, lw=1.6, r=0.01)
    elif kind == 'title':
        s.line(0.2, 1.1, 1.1, 1.1, color=INK, lw=5)
        s.line(0.2, 0.2, 1.1, 0.2, color=INK, lw=2)
        for k in range(3):
            s.box(0.3 + k * 0.28, 0.2, 0.2, 0.2 + k * 0.18, '', fill=PAPER, lw=1.6, r=0.01)
    elif kind == 'input':
        s.arrow(0.03, cy, 0.5, cy, color=RED, lw=2.8, head=14)
        s.box(0.55, 0.25, 0.65, 0.8, '', fill=PAPER, lw=2.4, r=0.05)
    elif kind == 'limit':
        s.arrow(0.05, cy, 0.85, cy, color=INK, lw=2.6, head=14)
        s.line(1.0, 0.2, 1.0, 1.1, color=RED, lw=6)
    elif kind == 'repeat':
        r = 0.4
        s.ax.add_patch(Arc((cx, cy), 2 * r, 2 * r, theta1=40, theta2=330, color=INK, lw=3.2, zorder=4))
        th = math.radians(330)
        px, py = cx + r * math.cos(th), cy + r * math.sin(th)
        tx, ty = -math.sin(th), math.cos(th)
        nx, ny = math.cos(th), math.sin(th)
        s.ax.add_patch(Polygon([(px + tx * 0.16, py + ty * 0.16), (px + nx * 0.1, py + ny * 0.1), (px - nx * 0.1, py - ny * 0.1)], closed=True, fc=INK, ec=INK, zorder=5))
    else:
        raise ValueError(kind)
    return s


def wi(kind):
    return ('ml_r3_wicon', {'kind': kind})


# ====================================================================== session 1
@fig('ml_r3_print')
def ml_r3_print(w, h):
    s = Scene(w, h)
    c1 = Code(s, 0.2, h - 0.2, ['print("Hello, data")'], size=22)
    label_under(s, c1, 0, 0, 5, 'print', size=18, sub='the instruction')
    label_under(s, c1, 0, 5, 20, 'what to show', size=18, sub='inside the brackets')
    ox = c1.x0 + c1.w + 0.25
    s.arrow(ox, c1.y(0), ox + 0.5, c1.y(0), color=RED, lw=2.6)
    s.box(ox + 0.6, c1.y(0) - 0.32, 1.9, 0.64, 'Hello, data', size=19, mono=True, fill=PAPER, lw=1.8)
    c2 = Code(s, 0.2, h * 0.43, ['print(3 + 2)'], size=22)
    label_under(s, c2, 0, 6, 11, '3 + 2', size=18, sub='no quotation marks, so Python adds')
    s.arrow(ox, c2.y(0), ox + 0.5, c2.y(0), color=RED, lw=2.6)
    s.box(ox + 0.6, c2.y(0) - 0.32, 0.9, 0.64, '5', size=24, mono=True, fill=PAPER, lw=1.8)
    return s


@fig('ml_r3_pipeline')
def ml_r3_pipeline(w, h):
    s = Scene(w, h)
    cw = (w - 0.4) / 3
    stages = [('120 homes we know', False), ('the computer learns a line', True), ('a guess for a new home', None)]
    for i, (cap, line) in enumerate(stages):
        x = 0.2 + i * cw
        if i < 2:
            scatter_axes(s, x + 1.0, 0.95, cw - 1.5, h - 2.05, line=line, mark=None, size=14, ylab=False, xlab=False)
            s.text(x + 1.0 + (cw - 1.5) / 2, 0.38, 'area to rent', size=16, color=MUTE)
        else:
            cx = x + cw / 2
            draw_house(s, cx, h - 1.55, 1.4)
            s.text(cx, h - 2.5, '50 m²', size=22, mono=True, weight='bold')
            s.arrow(cx, h - 2.75, cx, h - 3.1, color=RED, lw=2.4, head=16)
            d, m, b = fit_line()
            s.box(cx - 1.15, h - 3.85, 2.3, 0.8, f'{round(m * 50 + b):,}', size=22, weight='bold', mono=True, fill=GOLD, lw=2.2, r=0.06)
            s.text(cx, h - 4.2, 'UGX a month', size=16, color=MUTE)
        s.text(x + cw / 2, h - 0.3, cap, size=20, weight='bold')
        if i < 2:
            s.arrow(x + cw - 0.4, h * 0.5, x + cw + 0.15, h * 0.5, color=RED, lw=2.6, head=18)
    return s


# ====================================================================== session 2 and lab F01
@fig('ml_r3_trace')
def ml_r3_trace(w, h, code=('price = 2500.5', 'quantity = 2', 'total = price * quantity', 'print(total)', 'quantity = 4', 'print(total)', 'total = price * quantity', 'print(total)'),
                names=('price', 'quantity', 'total')):
    steps = run_lines(code)
    s = Scene(w, h)
    size = 16
    nrow = len(code) + 1
    rh = min(0.5, (h - 0.2) / nrow)
    cwid = [max(len(c) for c in code) * size * MONO_EM / 72 + 0.25] + [1.05] * len(names) + [1.05]
    sc = (w - 0.2) / sum(cwid)
    if sc < 1:
        cwid = [c * sc for c in cwid]
    rows = [['code line'] + list(names) + ['printed']]
    prev, hl = {}, {}
    for r, (ln, vals, pr) in enumerate(steps, start=1):
        row = [ln]
        for c, nm in enumerate(names, start=1):
            v = vals.get(nm)
            row.append('' if v is None else vstr(v))
            if v is not None and prev.get(nm) != v:
                hl[(r, c)] = GOLD
        row.append(pr or '')
        rows.append(row)
        prev = vals
    s.table(0.1, h - 0.1, cwid, rh, rows, size=size, mono_cols=(0, len(names) + 1), hl_cells=hl, align=['left'] + ['center'] * (len(names) + 1))
    return s


@fig('ml_r3_stale')
def ml_r3_stale(w, h):
    s = Scene(w, h)
    st = run_lines(['price = 2500.5', 'quantity = 2', 'total = price * quantity', 'quantity = 4', 'total = price * quantity'])
    snaps = [('first calculation', st[2][1]), ('after quantity = 4', st[3][1]), ('calculated again', st[4][1])]
    colw = (w - 0.3) / 3
    for i, (cap, v) in enumerate(snaps):
        x = 0.15 + i * colw
        s.text(x + colw / 2, h - 0.4, cap, size=18, weight='bold')
        for k, nm in enumerate(['price', 'quantity', 'total']):
            yy = h - 1.95 - k * 1.1
            fill = GOLD if (i == 1 and nm == 'quantity') or (i == 2 and nm == 'total') else PAPER
            s.box(x + 0.2, yy, colw - 0.4, 0.95, '', fill=fill, lw=1.8, r=0.04)
            s.text(x + 0.35, yy + 0.8, nm, size=16, mono=True, ha='left', va='top')
            s.text(x + colw / 2 + 0.15, yy + 0.38, vstr(v[nm]), size=26, weight='bold', mono=True)
        if i == 1:
            s.text(x + colw / 2, 0.3, 'total is still the old answer', size=17, color=RED, weight='bold')
    return s


# ====================================================================== session 3
@fig('ml_r3_error')
def ml_r3_error(w, h, error='NameError', message="name 'price' is not defined", code='print(price)', line=1, hint='the name was never created in this session'):
    s = Scene(w, h)
    bx, bw = 0.15, w * 0.745
    inner = bw - 0.5
    s.box(bx, 0.7, bw, h - 0.9, '', fill=PAPER, edge=RED, lw=2.4, r=0.05)
    s.text(bx + 0.25, h - 0.55, 'Traceback (most recent call last)', size=fit_mono('Traceback (most recent call last)', inner, 17), mono=True, color=MUTE, ha='left')
    s.text(bx + 0.25, h - 1.3, f'Cell In[1], line {line}', size=18, mono=True, color=BODY, ha='left')
    s.text(bx + 0.25, h - 2.0, f'----> {line}  {code}', size=18, mono=True, ha='left')
    s.line(bx + 0.2, h - 2.5, bx + bw - 0.2, h - 2.5, color=HAIR, lw=1.2)
    last = f'{error}: {message}'
    es = fit_mono(last, inner, 18, pad=0.05)
    ey = h - 3.15
    s.text(bx + 0.25, ey, error, size=es, mono=True, weight='bold', color=RED, ha='left')
    s.text(bx + 0.25 + len(error) * es * MONO_EM / 72, ey, f': {message}', size=es, mono=True, ha='left')
    ax0 = bx + bw + 0.5
    s.arrow(ax0, ey, bx + bw + 0.03, ey, color=RED, lw=2.4, head=17)
    s.text(ax0 + 0.1, ey, 'read this\nline first', size=18, weight='bold', ha='left')
    s.arrow(ax0, h - 1.3, bx + bw + 0.03, h - 1.3, color=RED, lw=2.4, head=17)
    s.text(ax0 + 0.1, h - 1.3, 'then the\nline number', size=16, ha='left', color=BODY)
    s.text(bx + 0.25, 0.38, hint, size=17, color=MUTE, ha='left')
    return s


@fig('ml_r3_comment')
def ml_r3_comment(w, h):
    s = Scene(w, h)
    code = ['# The price came in as text', 'text_price = "12.5"', 'price = float(text_price)', 'total = price * 4', 'print(total)']
    cb = Code(s, 0.15, h - 0.25, code, size=18, lead=1.8)
    right = cb.x0 + cb.w
    s.arrow(right + 0.55, cb.y(0), right + 0.05, cb.y(0), color=RED, lw=2.2, head=15)
    s.text(right + 0.65, cb.y(0) + 0.14, 'comment', size=20, weight='bold', ha='left')
    s.text(right + 0.65, cb.y(0) - 0.2, 'a note for people', size=16, color=MUTE, ha='left')
    s.text(0.15, cb.bottom - 0.45, 'Python skips everything after the #', size=19, ha='left', color=BODY)
    s.box(0.15, 0.3, 1.9, 0.75, '50.0', size=26, weight='bold', mono=True, fill=GOLD, lw=2.0, r=0.05)
    s.text(2.25, 0.68, 'is what the cell prints', size=18, ha='left', color=BODY)
    return s


# ====================================================================== session 4
@fig('ml_r3_edge')
def ml_r3_edge(w, h, threshold=5000, values=(4999, 5000, 5001), op='>=', yes='Buy', no='Save', var='budget'):
    s = Scene(w, h)
    ly = h * 0.55
    s.line(0.4, ly, w - 0.4, ly, color=INK, lw=2.4)
    xs = [w * (0.2 + 0.3 * i) for i in range(len(values))]
    cmp = {'>=': lambda a, b: a >= b, '>': lambda a, b: a > b, '<=': lambda a, b: a <= b, '<': lambda a, b: a < b}[op]
    mid = xs[1]
    s.line(mid, ly - 0.35, mid, ly + 0.35, color=RED, lw=2.8, z=3)
    s.text(mid, ly + 1.4, f'edge: {threshold}', size=20, weight='bold', color=RED)
    for x, v in zip(xs, values):
        ok = cmp(v, threshold)
        s.circle(x, ly, 0.22, fill=GOLD if v == threshold else PAPER, edge=INK, lw=2.4, z=4)
        s.text(x, ly - 0.55, str(v), size=22, weight='bold', mono=True)
        s.text(x, ly - 0.98, f'{var} {op} {threshold}', size=16, mono=True, color=MUTE)
        s.box(x - 0.6, ly - 2.0, 1.2, 0.6, str(ok), size=22, weight='bold', mono=True, fill=GOLD if ok else PAPER, lw=1.8, r=0.05)
        s.text(x, ly + 0.8, yes if ok else no, size=22, weight='bold')
    s.text(w / 2, 0.3, f'{op} includes the edge value itself', size=19, color=BODY)
    return s


@fig('ml_r3_flow')
def ml_r3_flow(w, h, conds=(('budget >= 5000', 'Buy'),), else_text='Save', code=('if budget >= 5000:', '    print("Buy")', 'else:', '    print("Save")'), size=16):
    s = Scene(w, h)
    n = len(conds)
    top = h - 0.15
    if code and n == 1:
        cb = Code(s, 0.15, h - 0.15, list(code), size=size)
        top = cb.bottom - 0.3
    fx = 0.2
    qw = max(len(c[0]) + 2 for c in conds) * size * MONO_EM / 72 + 0.4
    ow = w - fx - qw - 1.3
    qh = 0.72
    avail = top - 0.1 - (n + 1) * qh
    gap = max(0.42, min(0.7, avail / n))
    ytop = top - 0.1
    for i, (cond, out) in enumerate(conds):
        yb = ytop - i * (qh + gap) - qh
        s.box(fx, yb, qw, qh, cond + ' ?', size=size, weight='bold', mono=True, fill=PAPER, lw=2.2, r=0.06)
        s.arrow(fx + qw, yb + qh / 2, fx + qw + 1.0, yb + qh / 2, color=INK, lw=1.8, head=13)
        s.text(fx + qw + 0.5, yb + qh / 2 + 0.22, 'True', size=16, color=BODY)
        s.box(fx + qw + 1.05, yb + 0.04, ow, qh - 0.08, out, size=size, weight='bold', mono=True, fill=GOLD, lw=1.8, r=0.05)
        s.arrow(fx + qw / 2, yb, fx + qw / 2, yb - gap, color=INK, lw=1.8, head=13)
        s.text(fx + qw / 2 + 0.12, yb - gap / 2, 'False', size=16, color=BODY, ha='left')
    ye = ytop - n * (qh + gap)
    s.box(fx, ye - qh, qw + 1.05 + ow, qh, else_text, size=size, weight='bold', mono=True, fill=GOLD, lw=1.8, r=0.05)
    return s


@fig('ml_r3_zones')
def ml_r3_zones(w, h, flowers=((1.4, 'setosa'), (1.4, 'setosa'), (4.7, 'versicolor'), (4.5, 'versicolor'), (4.9, 'versicolor'), (6.0, 'virginica'), (5.1, 'virginica'), (5.9, 'virginica')),
                cuts=(2.5, 4.8), names=('setosa', 'versicolor', 'virginica'), verdict=False):
    s = Scene(w, h)
    x0, x1 = 0.7, w - 0.5
    px = lambda v: x0 + v / 7.0 * (x1 - x0)
    ly = h * 0.36
    s.line(x0, ly, x1, ly, color=INK, lw=2.4)
    for t in range(0, 8):
        s.line(px(t), ly, px(t), ly - 0.1, color=INK, lw=1.6)
        s.text(px(t), ly - 0.36, str(t), size=17, color=BODY)
    s.text((x0 + x1) / 2, ly - 0.8, 'petal length (cm)', size=19)
    bounds = [0.0, cuts[0], cuts[1], 7.0]
    guess = lambda v: names[0] if v < cuts[0] else (names[1] if v < cuts[1] else names[2])
    for i, nm in enumerate(names):
        a, b = px(bounds[i]), px(bounds[i + 1])
        s.box(a + 0.03, ly + 0.05, b - a - 0.06, 0.5, nm, size=19, weight='bold', fill=PAPER, lw=1.6, r=0.03)
    for c in cuts:
        s.line(px(c), ly - 0.05, px(c), ly + 2.3, color=RED, lw=2.4, dash=True)
        s.text(px(c), ly + 2.58, str(c), size=19, weight='bold', color=RED)
    fills = {names[0]: PAPER, names[1]: GREY, names[2]: INK}
    levels, right = [], 0
    for v, sp in sorted(flowers):
        lvl = next((i for i, lx_ in enumerate(levels) if px(v) - lx_ > 0.42), None)
        if lvl is None:
            levels.append(px(v))
            lvl = len(levels) - 1
        else:
            levels[lvl] = px(v)
        cy = ly + 0.95 + lvl * 0.42
        ok = guess(v) == sp
        right += ok
        s.circle(px(v), cy, 0.16, fill=fills[sp], edge=INK if ok else RED, lw=2.0 if ok else 3.4, z=4)
        if verdict and not ok:
            s.text(px(v) + 0.35, cy, 'wrong', size=17, color=RED, weight='bold', z=6, ha='left')
    for i, nm in enumerate(names):
        lx = 0.7 + i * 3.7
        s.circle(lx, 0.28, 0.14, fill=fills[nm], edge=INK, lw=1.8)
        s.text(lx + 0.25, 0.28, f'true species: {nm}', size=17, ha='left', color=BODY)
    if verdict:
        s.text(w - 0.4, h - 0.4, f'{right} of {len(flowers)} right', size=30, weight='bold', ha='right')
    return s


# ====================================================================== session 5
@fig('ml_r3_loop_trace')
def ml_r3_loop_trace(w, h, values=(1000, 2000, 3000), var='price'):
    s = Scene(w, h)
    cum = list(np.cumsum(values))
    rows = [['pass', var, 'before', 'after']]
    prev = 0
    for i, (v, c) in enumerate(zip(values, cum), start=1):
        rows.append([str(i), str(v), str(prev), str(int(c))])
        prev = int(c)
    cw = [0.8, 0.95, 1.05, 1.05]
    rh = 0.55
    s.text(0.1 + sum(cw) / 2, h - 0.25, 'pass by pass', size=18, weight='bold')
    s.table(0.1, h - 0.55, cw, rh, rows, size=17, mono_cols=(1, 2, 3), hl_cells={(i, 3): GOLD for i in range(1, len(rows))})
    bx0 = 0.1 + sum(cw) + 1.2
    bw = w - bx0 - 0.2
    top = int(max(cum))
    px, py = axes_xy(s, bx0, 0.85, bw, h - 1.9, (0, len(values)), (0, top * 1.1), xticks=[], yticks=[0, top], size=16)
    for i, c in enumerate(cum):
        bwid = bw / len(values) * 0.6
        s.box(px(i + 0.5) - bwid / 2, 0.85, bwid, py(c) - 0.85, '', fill=GOLD if i == len(values) - 1 else PAPER, lw=1.6, r=0.01)
        s.text(px(i + 0.5), 0.55, f'pass {i + 1}', size=16, color=BODY)
    s.text(bx0 + bw / 2 - 0.3, h - 0.45, 'total after each pass', size=17, weight='bold')
    return s


@fig('ml_r3_reset_pair')
def ml_r3_reset_pair(w, h, inside=False, values=(1000, 2000, 3000)):
    s = Scene(w, h)
    code = ['for price in prices:', '    total = 0', '    total = total + price'] if inside else ['total = 0', 'for price in prices:', '    total = total + price']
    cb = Code(s, 0.1, h - 0.15, code, size=16)
    totals, t = [], 0
    for u in values:
        if inside:
            t = 0
        t += u
        totals.append(t)
    s.text(0.15, cb.bottom - 0.4, 'total after each pass', size=17, ha='left', color=BODY)
    n = len(values)
    bw = (w - 0.3) / n
    for i, v in enumerate(totals):
        s.box(0.15 + i * bw + 0.05, cb.bottom - 1.45, bw - 0.1, 0.7, str(v), size=22, weight='bold', mono=True, fill=GOLD if i == n - 1 else PAPER, lw=1.8, r=0.04)
    s.text(w / 2, cb.bottom - 1.95, f'final total: {totals[-1]}', size=24, weight='bold', color=RED if inside else INK)
    return s


# ====================================================================== session 6
@fig('ml_r3_machine')
def ml_r3_machine(w, h, name='revenue', params=('units', 'price'), args=(3, 2000), body='units * price', result=None, show_code=True,
                  code=('def revenue(units, price):', '    return units * price')):
    s = Scene(w, h)
    if result is None:
        result = vstr(eval(body, dict(zip(params, args))))
    cy0 = 1.9 if show_code else 0.5
    top = h - 0.55
    mh = top - cy0
    mx, mw = w * 0.36, w * 0.33
    s.box(mx, cy0, mw, mh, '', fill=PAPER, lw=2.6, r=0.1)
    s.text(mx + mw / 2, cy0 + mh * 0.68, name, size=22 if w < 9 else 28, weight='bold', mono=True)
    bt = f'return {body}' if len(body) < 8 else (f'return\n{body}' if len(body) < 22 else body)
    s.text(mx + mw / 2, cy0 + mh * 0.3, bt, size=fit_mono(max(bt.split('\n'), key=len), mw, 16 if w < 9 else 19, pad=0.1), mono=True, color=BODY)
    n = len(params)
    s.text(0.2 + w * 0.07, h - 0.3, 'arguments in', size=17, color=MUTE)
    for i, (pn, av) in enumerate(zip(params, args)):
        yy = cy0 + mh * (0.72 - 0.44 * i / max(1, n - 1)) if n > 1 else cy0 + mh * 0.5
        s.box(0.2, yy - 0.3, w * 0.14, 0.6, vstr(av) if not isinstance(av, str) else av, size=20, weight='bold', mono=True, fill=GOLD, lw=1.8, r=0.05)
        s.arrow(0.25 + w * 0.14, yy, mx - 0.02, yy, color=INK, lw=2.0, head=14)
        s.text((0.25 + w * 0.14 + mx) / 2, yy + 0.3, pn, size=16, mono=True, color=RED, weight='bold')
    rw = w * 0.17
    s.arrow(mx + mw + 0.02, cy0 + mh / 2, w - 0.2 - rw, cy0 + mh / 2, color=INK, lw=2.0, head=14)
    s.box(w - 0.2 - rw, cy0 + mh / 2 - 0.4, rw, 0.8, result, size=fit_mono(result, rw, 24, pad=0.15), weight='bold', mono=True, fill=PAPER, lw=2.0, r=0.05)
    s.text(w - 0.2 - rw / 2, cy0 + mh / 2 + 0.7, 'answer back', size=17, color=MUTE)
    if show_code:
        Code(s, 0.15, 1.45, list(code), size=16)
    return s


# ====================================================================== lab F01 and F02
@fig('ml_r3_predict_paper')
def ml_r3_predict_paper(w, h, code=('units = 3', 'price = 1000', 'total = units * price', 'print(total)', 'print(total / units)', 'print("1000")', 'units = 4', 'print(total)', 'total = units * price', 'print(total)')):
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec('\n'.join(code), {})
    n = len(buf.getvalue().strip().split('\n'))
    s = Scene(w, h)
    cb = Code(s, 0.1, h - 0.15, list(code), size=16, lead=1.45)
    px0 = cb.x0 + cb.w + 0.4
    pw = w - px0 - 0.1
    s.box(px0, 0.35, pw, h - 0.65, '', fill=PAPER, lw=2.2, r=0.04)
    s.text(px0 + pw / 2, h - 0.65, 'my prediction on paper', size=20, weight='bold')
    rh = (h - 1.6) / n
    for i in range(n):
        yy = h - 1.2 - (i + 0.5) * rh
        s.line(px0 + 0.25, yy - rh / 2 + 0.05, px0 + pw - 0.25, yy - rh / 2 + 0.05, color=HAIR, lw=1.2)
        s.text(px0 + 0.4, yy, f'{i + 1}', size=17, color=MUTE, ha='left')
    s.icon('pen', px0 + pw - 0.55, 0.9, 0.9)
    return s


@fig('ml_r3_three_pens')
def ml_r3_three_pens(w, h, n=3, price=1000):
    s = Scene(w, h)
    step = (w - 3.0) / n
    for i in range(n):
        x = 0.9 + i * step
        s.icon('pen', x, h - 1.55, 1.5)
        s.box(x - 0.55, h - 2.85, 1.1, 0.6, f'{price:,}', size=19, weight='bold', mono=True, fill=GOLD, lw=1.8, r=0.05)
        if i < n - 1:
            s.text(x + step / 2, h - 2.55, '+', size=30, weight='bold')
    s.text(w - 1.75, h - 2.55, '=', size=34, weight='bold')
    s.box(w - 1.4, h - 2.95, 1.3, 0.8, f'{n * price:,}', size=22, weight='bold', mono=True, fill=GOLD, lw=2.2, r=0.05)
    s.text(w / 2, h - 0.3, f'{n} pens at UGX {price:,} each', size=22, weight='bold')
    s.text(w / 2, 1.0, f'{n} * {price} = {n * price}', size=30, mono=True, weight='bold')
    return s


@fig('ml_r3_units')
def ml_r3_units(w, h):
    s = Scene(w, h)
    y = h / 2 - 0.5
    s.box(0.2, y, 2.0, 1.0, '40 m²', size=28, weight='bold', fill=PAPER, lw=2.2, r=0.05)
    s.text(2.5, y + 0.5, '+', size=36, weight='bold')
    s.box(2.8, y, 2.0, 1.0, '2 rooms', size=28, weight='bold', fill=PAPER, lw=2.2, r=0.05)
    s.text(5.1, y + 0.5, '=', size=36, weight='bold')
    s.box(5.4, y, 1.8, 1.0, '42 ?', size=28, weight='bold', fill=PAPER, lw=2.2, r=0.05, edge=RED, color=RED)
    s.text(w / 2, y - 0.8, 'square metres and rooms do not mix', size=20, color=RED, weight='bold')
    return s


# ====================================================================== session 7
@fig('ml_csv_to_table')
def ml_csv_to_table(w, h, **_):
    s = Scene(w, h)
    raw = shop_raw().head(3)[['sale_id', 'date', 'item', 'units', 'unit_price_ugx']]
    lines = ['sale_id,date,item,units,unit_price_ugx'] + [','.join(str(v) for v in r) for r in raw.astype(object).values.tolist()]
    top = h - 0.1
    cwid, ch = s.code(0.2, top, lines, size=16, line_h=0.3, pad=0.15, w=5.6)
    ytab_top = top - ch - 0.7
    s.arrow(2.9, top - ch - 0.05, 2.9, ytab_top + 0.05, color=RED, lw=2.4, head=18)
    s.text(3.2, top - ch - 0.42, 'pd.read_csv("camp_shop.csv")', size=17, mono=True, ha='left')
    data_table(s, 0.2, ytab_top, raw, [0.95, 1.45, 0.9, 0.9, 1.95], row_h=0.38, size=16, hl_rows=(0,), hl_fill='#EDEDED')
    s.text(0.2, ytab_top - 4 * 0.38 - 0.28, '... 57 more rows', size=17, color=MUTE, ha='left')
    ax = 7.6
    s.text(ax, top - 0.3, 'The first line of the file\nholds the headers.', size=19, ha='left')
    s.arrow(ax - 0.1, top - 0.3, 5.95, top - 0.3, color=INK, lw=1.8, head=14)
    s.text(ax, top - 1.5, 'Every other line is one row:\none sale.', size=19, ha='left')
    s.arrow(ax - 0.1, top - 1.45, 5.95, top - 0.3 - 0.32 * 2, color=INK, lw=1.8, head=14)
    s.box(ax, 0.55, 4.0, 0.8, '60 rows by 5 columns', size=24, fill=GOLD, weight='bold', r=0.05)
    s.text(ax + 2.0, 0.28, 'shape (60, 5)', size=17, mono=True, color=MUTE)
    return s


@fig('ml_three_files')
def ml_three_files(w, h, **_):
    s = Scene(w, h)
    tbls = [(shop_rev()[['sale_id', 'item', 'units']].head(3), [0.95, 0.9, 0.85], 'one row = one sale', '60 rows, 5 columns (3 shown)'),
            (homes().head(3), [0.9, 1.05, 0.85, 1.25], 'one row = one home', '120 rows, 4 columns'),
            (fares()[['trip_id', 'distance_km', 'raining', 'fare_ugx']].head(3), [0.85, 1.45, 1.0, 1.1], 'one row = one trip', '150 rows, 6 columns (4 shown)')]
    x = 0.15
    for df, cws, cap, sub in tbls:
        tw = sum(cws)
        data_table(s, x, h - 0.4, df, cws, row_h=0.45, size=16, hl_rows=(0,), hl_fill='#EDEDED')
        s.text(x + tw / 2, h - 0.4 - 4 * 0.45 - 0.45, cap, size=20, weight='bold')
        s.text(x + tw / 2, h - 0.4 - 4 * 0.45 - 0.95, sub, size=16, color=MUTE)
        x += tw + 0.25
    return s


@fig('ml_shape_grid')
def ml_shape_grid(w, h, **_):
    s = Scene(w, h)
    rows = [['item', 'units'], ['Book', '2'], ['Pen', '5'], ['Book', '3']]
    tx, ty, rh = 0.4, h - 0.5, 0.55
    cw = [1.35, 1.15]
    s.table(tx, ty, cw, rh, rows, size=20, hl_rows=(0,), hl_fill='#EDEDED')
    xr = tx + sum(cw) + 0.2
    s.line(xr, ty - rh, xr, ty - 4 * rh, color=RED, lw=3)
    s.text(xr + 0.15, ty - 2.5 * rh, '3 rows', size=20, weight='bold', color=RED, ha='left')
    s.line(tx, ty + 0.12, tx + sum(cw), ty + 0.12, color=INK, lw=3) if False else None
    s.brace(tx, tx + sum(cw), ty - 4 * rh - 0.15, depth=-0.14, color=INK, lw=2.4, up=True)
    s.text(tx + sum(cw) / 2, ty - 4 * rh - 0.55, '2 columns', size=20, weight='bold')
    s.box(tx, ty - 4 * rh - 1.5, sum(cw), 0.6, 'shape (3, 2)', size=22, mono=True, weight='bold', fill=GOLD, lw=2, r=0.05)
    s.text(tx + sum(cw) / 2, ty - 4 * rh - 1.9, 'rows first, then columns', size=17, color=MUTE) if False else None
    ox = 4.7
    s.text(ox, h - 0.55, 'The three files this term', size=18, weight='bold', ha='left')
    sets = [('camp_shop', shop_raw()), ('synthetic_homes', homes()), ('synthetic_fares', fares())]
    for k, (name, d) in enumerate(sets):
        y = h - 1.4 - k * 1.0
        s.text(ox, y + 0.15, name, size=17, mono=True, ha='left')
        s.box(ox, y - 0.5, 2.3, 0.5, f'{d.shape}', size=20, mono=True, weight='bold', fill=PAPER, lw=1.8, r=0.04)
    return s


# ====================================================================== session 8
@fig('ml_select_col')
def ml_select_col(w, h, **_):
    s = Scene(w, h)
    d = shop_raw().head(5)[['sale_id', 'item', 'units']]
    data_table(s, 0.6, h - 0.2, d, [1.5, 1.7, 1.5], row_h=0.55, size=22, hl_cols=(2,))
    yb = h - 0.2 - 6 * 0.55
    s.text(w / 2, yb - 0.55, 'shop["units"]', size=22, mono=True, weight='bold')
    s.text(w / 2, yb - 1.05, 'reads one column', size=18, color=MUTE)
    return s


@fig('ml_filter_rows')
def ml_filter_rows(w, h, **_):
    s = Scene(w, h)
    d = shop_raw().head(5)[['item', 'units']].copy()
    d['units >= 5'] = d['units'] >= 5
    keep = [i + 1 for i, v in enumerate(d['units >= 5']) if v]
    rows = [list(d.columns)] + [[r[0], str(r[1]), str(r[2])] for r in d.astype(object).values.tolist()]
    s.table(0.4, h - 0.2, [1.4, 1.3, 2.6], 0.55, rows, size=20, hl_rows=tuple(keep))
    yb = h - 0.2 - 6 * 0.55
    s.text(w / 2, yb - 0.55, 'shop[shop["units"] >= 5]', size=20, mono=True, weight='bold')
    s.text(w / 2, yb - 1.05, 'keeps the True rows', size=18, color=MUTE)
    return s


@fig('ml_mask_steps')
def ml_mask_steps(w, h, **_):
    s = Scene(w, h)
    vals = shop_raw().head(6)['units'].tolist()
    mask = [v >= 5 for v in vals]
    y0, rh = h - 0.85, 0.55
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
            s.box(5.6, y0 - k * rh - rh + 0.04, 1.5, rh - 0.08, f'{v} units', size=19, fill=GOLD, r=0.03)
            s.arrow(3.95, y0 - i * rh - rh / 2 + 0.04, 5.55, y0 - k * rh - rh / 2 + 0.04, color=RED, lw=1.8, head=13)
            k += 1
    s.text(0.4, 0.45, 'True keeps the row. False drops it.', size=18, ha='left', color=BODY)
    return s


@fig('ml_new_column')
def ml_new_column(w, h, **_):
    s = Scene(w, h)
    d = shop_rev().head(5)[['item', 'units', 'unit_price_ugx', 'revenue_ugx']]
    n_all = len(shop_rev())
    cw = [1.2, 1.0, 1.9, 1.8]
    rh = 0.52
    data_table(s, 0.2, h - 0.2, d, cw, row_h=rh, size=18, hl_cols=(3,))
    yb = h - 0.2 - 6 * rh
    s.text(0.2, yb - 0.25, f'... {n_all - 5} more rows', size=17, color=MUTE, ha='left')
    s.text(0.2, yb - 0.75, 'revenue = units x unit_price_ugx, one row at a time', size=17, ha='left')
    sub5, tot = int(d.revenue_ugx.sum()), int(shop_rev().revenue_ugx.sum())
    s.box(0.2, 0.2, 3.5, 0.55, f'these 5 rows: {sub5:,}', size=18, weight='bold', fill=PAPER, lw=1.8, r=0.05)
    s.box(3.9, 0.2, 3.6, 0.55, f'all {n_all} rows: {tot:,}', size=18, weight='bold', fill=GOLD, lw=1.8, r=0.05)
    return s


@fig('ml_units_vs_money')
def ml_units_vs_money(w, h, **_):
    d = shop_rev().groupby('item').agg(units=('units', 'sum'), rev=('revenue_ugx', 'sum'))
    order = ['Book', 'Pen', 'Juice']
    s = Scene(w, h)
    for k, (col, ttl) in enumerate([('units', 'Units sold'), ('rev', 'Money earned (UGX)')]):
        ax = axes_in(s, 0.9 + k * 6.1, 0.6, 4.7, h - 1.7)
        vals = [d.loc[i, col] for i in order]
        top = int(np.argmax(vals))
        bars = ax.bar(order, vals, color=[GOLD if i == top else PAPER for i in range(3)], edgecolor=INK, linewidth=2, width=0.6)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + max(vals) * 0.03, f'{v:,.0f}', ha='center', va='bottom', fontsize=18, fontweight='bold', family=FONT)
        ax.set_ylim(0, max(vals) * 1.22)
        ax.set_yticks([])
        ax.spines['left'].set_visible(False)
        ax.tick_params(axis='x', labelsize=18)
        s.text(0.9 + k * 6.1 + 2.35, h - 0.45, ttl, size=22, weight='bold')
    return s


# ====================================================================== session 9
@fig('ml_units_dotplot')
def ml_units_dotplot(w, h, **_):
    u = shop_raw()['units'].values
    mean, med = float(u.mean()), float(np.median(u))
    s = Scene(w, h)
    ax = axes_in(s, 0.9, 1.0, w - 1.8, h - 1.7)
    counts = {v: int((u == v).sum()) for v in range(1, 9)}
    for v, c in counts.items():
        ax.scatter([v] * c, range(1, c + 1), s=215, facecolor=PAPER, edgecolor=INK, linewidth=2.0, zorder=3)
    ax.axvline(mean, color=RED, lw=3, zorder=2)
    ax.axvline(med, color=INK, lw=3, zorder=2, ls='--')
    ax.set_xlim(0.4, 8.6)
    ax.set_ylim(0.3, max(counts.values()) + 1.9)
    ax.set_xticks(range(1, 9))
    ax.tick_params(axis='x', labelsize=20)
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.set_xlabel('units in one sale', fontsize=19)
    top = max(counts.values()) + 0.55
    ax.text(mean + 0.08, top, f'mean {mean:.2f}', color=RED, fontsize=22, fontweight='bold', ha='left', va='bottom')
    ax.text(med - 0.08, top, f'median {med:.1f}', color=INK, fontsize=22, fontweight='bold', ha='right', va='bottom')
    s.text(w / 2, h - 0.3, 'each circle is one of the 60 sales', size=19, color=MUTE)
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
            s.text(x0 + i * (bw + gap) + bw / 2, 1.0 + hh + 0.24, f'{m:g}' if shared else str(v), size=20, weight='bold')
        s.line(x0 - 0.1, 1.0, x0 + 4 * (bw + gap), 1.0, lw=2)
    s.arrow(3.2, 2.3, 4.75, 2.3, color=RED, lw=2.6, head=18)
    s.text(3.97, 2.95, 'share the\ntotal equally', size=17, color=RED, weight='bold')
    s.text(1.7, 0.5, f'total {sum(vals)}', size=19)
    s.text(6.3, 0.5, f'{sum(vals)} / {len(vals)} = {m:g} each', size=19)
    s.text(w / 2, h - 0.3, 'mean of 10, 12, 14 and 16', size=22, weight='bold')
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
        ax.text(pos + 1.0, 0.35, f'{name}: {val:g}', fontsize=17, color=RED, fontweight='bold', va='bottom', ha='left')
    ax.set_xlim(0, 62)
    ax.set_ylim(0, 8.8)
    ax.set_xlabel('the 60 sales in order, smallest first', fontsize=17)
    ax.set_ylabel('units', fontsize=17)
    ax.tick_params(labelsize=16)
    s.text(w / 2, h - 0.3, 'range: 1 to 8, which is 7', size=20, weight='bold')
    return s


@fig('ml_outlier_lines')
def ml_outlier_lines(w, h, **_):
    a = [10, 12, 14, 16]
    b = a + [100]
    s = Scene(w, h)
    for k, (vals, y, ttl) in enumerate([(a, h - 1.2, 'four values'), (b, h - 3.15, 'add one very large value')]):
        ax = axes_in(s, 1.0, y - 0.35, w - 1.6, 0.95)
        ax.set_xlim(0, 110)
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.spines['left'].set_visible(False)
        ax.scatter(vals[:4], [0.3, 0.62, 0.3, 0.62], s=300, facecolor=PAPER, edgecolor=INK, linewidth=2, zorder=4)
        if k == 1:
            ax.scatter(vals[4:], [0.45], s=300, facecolor=RED, edgecolor=RED, linewidth=2, zorder=4)
        ax.axvline(np.mean(vals), color=RED, lw=3, ymax=0.95, zorder=2)
        ax.axvline(np.median(vals), color=INK, lw=3, ls='--', ymax=0.95, zorder=3)
        ax.tick_params(axis='x', labelsize=16)
        s.text(0.4, y + 0.9, ttl, size=20, weight='bold', ha='left')
        s.text(w - 0.4, y + 0.9, f'mean {np.mean(vals):g}   median {np.median(vals):g}', size=21, weight='bold', ha='right')
    s.text(w - 0.4, 0.2, 'red line: mean   dashed line: median', size=17, color=BODY, ha='right')
    return s


# ====================================================================== session 10
def _raw_rows():
    return [['id', 'price'], ['1', '1000'], ['2', ''], ['2', ''], ['3', '3000']]


@fig('ml_copy_raw')
def ml_copy_raw(w, h, **_):
    s = Scene(w, h)
    rows = _raw_rows()
    s.table(0.3, h - 0.75, [0.8, 1.0], 0.5, rows, size=19)
    s.text(1.2, h - 0.35, 'raw', size=22, weight='bold')
    s.text(1.2, 1.35, 'never changed', size=17, color=MUTE)
    s.arrow(2.35, h - 2.0, 4.2, h - 2.0, color=RED, lw=2.6, head=18)
    s.text(3.3, h - 1.5, 'drop_duplicates()\n.copy()', size=16, mono=True)
    clean = rows[:3] + [rows[4]]
    s.table(4.7, h - 0.75, [0.8, 1.0], 0.5, clean, size=19)
    s.text(5.6, h - 0.35, 'clean', size=22, weight='bold')
    s.text(5.6, 1.35, '3 rows, one price\nstill missing', size=17, color=MUTE)
    s.box(4.35, 0.2, 2.5, 0.5, 'edit this copy only', size=17, fill=GOLD, weight='bold', r=0.05)
    return s


@fig('ml_cleaning_log')
def ml_cleaning_log(w, h, **_):
    s = Scene(w, h)
    rows = [['step', 'rows'], ['raw rows', '4'], ['duplicate removed', '1'], ['rows left', '3']]
    s.table(0.3, h - 0.5, [3.3, 1.2], 0.6, rows, size=21, hl_rows=(0,), hl_fill='#EDEDED', align=['left', 'center'])
    s.text(0.3, h - 0.25, 'the log', size=20, weight='bold', ha='left')
    s.arrow(2.0, h - 0.5 - 4 * 0.6 - 0.1, 2.0, 1.35, color=RED, lw=2.4, head=16)
    s.text(2.25, 1.8, 'read it back', size=17, ha='left', color=BODY)
    s.box(0.3, 0.3, 3.4, 0.7, 'shape (3, 2)', size=24, mono=True, weight='bold', fill=GOLD, lw=2, r=0.05)
    s.text(3.9, 0.65, '3 rows, 2 columns', size=18, ha='left')
    return s


@fig('ml_save_roundtrip')
def ml_save_roundtrip(w, h, **_):
    s = Scene(w, h)
    pairs = [('index=False', ['step,count', 'raw rows,4', 'duplicate removed,1'], INK, 'the file holds only your columns'),
             ('default', [',step,count', '0,raw rows,4', '1,duplicate removed,1'], RED, 'an extra column of row numbers')]
    cw = (w - 0.7) / 2
    for k, (ttl, lines, col, note) in enumerate(pairs):
        x = 0.2 + k * (cw + 0.3)
        s.text(x, h - 0.35, f'to_csv(..., {ttl})' if k == 0 else 'to_csv(...) with no setting', size=19, mono=True, weight='bold', ha='left', color=col)
        s.code(x, h - 0.7, lines, size=18, line_h=0.42, pad=0.18, w=cw)
        s.text(x, 1.2, note, size=19, ha='left', weight='bold' if k else 'normal', color=col)
    s.text(0.2, 0.55, 'Read the saved file back and check the shape.', size=18, ha='left', color=BODY)
    return s


# ====================================================================== session 11
@fig('ml_pick_chart')
def ml_pick_chart(w, h, **_):
    d = shop_rev()
    s = Scene(w, h)
    cw, gap = 2.65, 0.43
    qs = ['Which item\nearns the most?', 'How are the\nunits spread?', 'Do the items differ\nin spread?', 'How did revenue\nchange by day?']
    tn = ['bar chart', 'histogram', 'box plot', 'line chart']
    for k in range(4):
        x = 0.25 + k * (cw + gap)
        ax = axes_in(s, x + 0.15, 1.15, cw - 0.3, 1.4)
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
        s.text(x + cw / 2, h - 0.5, qs[k], size=18, weight='bold')
        s.arrow(x + cw / 2, h - 1.05, x + cw / 2, 2.75, color=RED, lw=2, head=14)
        s.text(x + cw / 2, 0.55, tn[k], size=22, weight='bold')
    return s


@fig('ml_chart_anatomy')
def ml_chart_anatomy(w, h, **_):
    d = shop_rev().groupby('item')['revenue_ugx'].sum()
    s = Scene(w, h)
    ax = axes_in(s, 3.0, 0.8, 4.3, h - 2.1)
    ax.bar(d.index, d.values, color=[GOLD if v == d.max() else PAPER for v in d.values], edgecolor=INK, linewidth=2)
    ax.set_ylim(0, 330000)
    ax.set_yticks([0, 100000, 200000, 300000])
    ax.set_yticklabels(['0', '100k', '200k', '300k'])
    ax.tick_params(labelsize=16)
    ax.set_ylabel('Revenue (UGX)', fontsize=16)
    s.text(5.15, h - 0.4, 'Revenue by item', size=21, weight='bold')
    s.text(0.25, h - 0.4, 'title', size=19, color=RED, weight='bold', ha='left')
    s.arrow(0.95, h - 0.4, 3.8, h - 0.4, color=RED, lw=1.8, head=13)
    s.text(0.25, 3.0, 'axis label:\nwhat is measured\nand its unit', size=17, color=RED, weight='bold', ha='left')
    s.arrow(1.55, 2.55, 2.05, 2.55, color=RED, lw=1.8, head=13)
    s.text(0.25, 1.35, 'the axis\nstarts at zero', size=17, color=RED, weight='bold', ha='left')
    s.arrow(1.55, 1.1, 2.95, 0.85, color=RED, lw=1.8, head=13)
    return s


@fig('ml_hist_bins')
def ml_hist_bins(w, h, **_):
    u = shop_raw()['units'].values
    cnt = np.bincount(u, minlength=9)[1:]
    s = Scene(w, h)
    ax = axes_in(s, 0.9, 1.0, w - 1.3, h - 2.0)
    bars = ax.bar(range(1, 9), cnt, color=[GOLD if c == cnt.max() else PAPER for c in cnt], edgecolor=INK, linewidth=2, width=0.9)
    for b, c in zip(bars, cnt):
        ax.text(b.get_x() + b.get_width() / 2, c + 0.2, str(c), ha='center', fontsize=20, fontweight='bold', family=FONT)
    ax.set_ylim(0, cnt.max() + 2)
    ax.set_xticks(range(1, 9))
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='x', labelsize=20)
    ax.set_xlabel('units in one sale', fontsize=18)
    s.text(w / 2, h - 0.35, 'one bin for each number of units: how many of the 60 sales', size=18, weight='bold')
    return s


@fig('ml_boxplot_anatomy')
def ml_boxplot_anatomy(w, h, **_):
    u = shop_raw()[shop_raw().item == 'Pen']['units'].values
    q1, med, q3 = np.percentile(u, [25, 50, 75])
    lo, hi = u.min(), u.max()
    s = Scene(w, h)
    x0, x1 = 0.9, w - 0.9
    sc = (x1 - x0) / 9.0
    X = lambda v: x0 + v * sc
    yb, bh = 2.0, 1.0
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
        s.text(X(v), yy, name, size=18, weight='bold', color=RED if name.startswith('median') else INK)
        s.arrow(X(v), yy - 0.22, X(v), yb + bh + 0.04, color=GREY, lw=1.4, head=10)
    s.text(X((q1 + q3) / 2), yb - 0.2 + 0.0, '', size=16)
    s.text(X((q1 + q3) / 2), yb + bh / 2, '', size=16)
    s.text(w / 2, 0.3, 'the box holds the middle half of the sales', size=18, weight='bold')
    return s


@fig('ml_finding_card')
def ml_finding_card(w, h, **_):
    d = shop_rev().groupby('item')['revenue_ugx'].sum()
    s = Scene(w, h)
    ax = axes_in(s, 1.35, 0.7, 4.1, h - 1.7)
    ax.bar(d.index, d.values, color=[GOLD if v == d.max() else PAPER for v in d.values], edgecolor=INK, linewidth=2, width=0.6)
    ax.set_yticks([0, 100000, 200000, 300000])
    ax.set_yticklabels(['0', '100k', '200k', '300k'])
    ax.set_ylim(0, 330000)
    ax.set_ylabel('Revenue (UGX)', fontsize=16)
    ax.tick_params(labelsize=16)
    s.text(3.4, h - 0.35, 'Revenue by item, practice shop', size=19, weight='bold')
    x = 5.9
    s.box(x, h - 2.2, 5.8, 1.55, '', fill=PAPER, lw=2, r=0.05)
    s.text(x + 0.25, h - 0.95, 'Finding', size=22, weight='bold', ha='left')
    s.text(x + 0.25, h - 1.55, f'Book earns the most: UGX {int(d.max()):,}.', size=20, ha='left')
    s.box(x, 0.6, 5.8, 1.55, '', fill=PAPER, edge=RED, lw=2, r=0.05)
    s.text(x + 0.25, 1.65, 'Limitation', size=22, weight='bold', ha='left', color=RED)
    s.text(x + 0.25, 1.05, 'Practice data with no costs, so\nthis says nothing about profit.', size=19, ha='left')
    return s


# ====================================================================== session 12
@fig('ml_restart_run_all')
def ml_restart_run_all(w, h, **_):
    s = Scene(w, h)
    s.text(1.75, h - 0.4, 'hidden memory', size=21, weight='bold', color=RED)
    for i, n in enumerate([5, 2, 7, 3]):
        s.box(0.35, h - 1.3 - i * 0.68, 2.8, 0.55, f'In [{n}]: a cell', size=18, r=0.04, mono=True, edge=RED)
    s.text(1.75, 0.95, 'works today, because the\nnotebook remembers a\ncell you deleted', size=17, color=RED)
    s.arrow(3.35, 2.8, 4.45, 2.8, color=INK, lw=2.6, head=18)
    s.text(3.9, 3.5, 'Restart\nand run all', size=18, weight='bold')
    s.text(6.0, h - 0.4, 'top to bottom', size=21, weight='bold')
    for i in range(4):
        s.box(4.6, h - 1.3 - i * 0.68, 2.8, 0.55, f'In [{i + 1}]: a cell', size=18, r=0.04, mono=True, fill=GOLD)
    s.text(6.0, 0.95, 'works for everyone,\nevery time', size=17)
    return s


@fig('ml_question_target_input')
def ml_question_target_input(w, h, **_):
    s = Scene(w, h)
    s.text(1.35, h - 0.45, 'inputs', size=21, weight='bold')
    s.text(1.35, h - 0.85, 'known before', size=17, color=MUTE)
    for i, name in enumerate(['area_m2', 'rooms']):
        s.box(0.3, h - 2.0 - i * 1.0, 2.1, 0.75, name, size=19, mono=True, r=0.05)
        s.arrow(2.5, h - 1.62 - i * 1.0, 3.9, h - 2.3, color=INK, lw=2, head=14)
    s.box(3.95, h - 3.1, 1.5, 1.6, 'model', size=22, weight='bold', r=0.08, fill='#111111', edge='#111111', color=PAPER)
    s.arrow(5.55, h - 2.3, 6.1, h - 2.3, color=INK, lw=2.4, head=16)
    s.text(6.85, h - 0.45, 'target', size=21, weight='bold')
    s.text(6.85, h - 0.85, 'the answer', size=17, color=MUTE)
    s.box(6.15, h - 2.7, 1.45, 0.8, 'rent_ugx', size=17, mono=True, fill=GOLD, weight='bold', r=0.05)
    s.text(w / 2, 0.8, 'Can area and rooms predict monthly rent?', size=21, weight='bold')
    s.text(w / 2, 0.3, 'Every input must be known before the rent is.', size=17, color=BODY)
    return s


@fig('ml_data_dictionary')
def ml_data_dictionary(w, h, **_):
    s = Scene(w, h)
    rows = [['column', 'meaning', 'unit'], ['home_id', 'a number for each home', 'none'], ['area_m2', 'floor area', 'square metres'], ['rooms', 'number of rooms', 'count'], ['rent_ugx', 'monthly rent', 'UGX']]
    s.table(0.2, h - 0.2, [1.55, 3.0, 2.3], 0.65, rows, size=18, mono_cols=(0,), hl_rows=(0,), hl_fill='#EDEDED', align=['left', 'left', 'left'])
    s.text(0.2, 0.95, 'Written once, so a stranger can read the file.', size=18, ha='left', color=BODY)
    s.text(0.2, 0.4, 'home_id is a label. It is never an input.', size=18, ha='left', color=RED, weight='bold')
    return s
