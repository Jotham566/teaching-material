"""Figures for Class 1. Imported by content/c1.py (diagrams.py auto-imports only classes 2 to 4).

  bars_c1      items [{label, value, fill}], unit, caption   filled bars with value labels and a caption (gold = best)
  tree_c1      node                                          the decision tree with the yes / no labels beside the lines, not on them
  descent_c1   labels                                        gradient descent picture whose y axis says 'loss (MSE)'
  sheet_c1     headers, rows, rowlabels, hl                  a table sketch whose left numbers are the real row numbers of the file
"""
import numpy as np

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, fig
import slidekit as K
import diagrams_ml as _dm

SHADE = '#B9B9B9'


def _wrap(s, x, y, w, text, size, weight='normal', color=INK, ha='center', va='center'):
    lines = K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', w)
    s.text(x, y, '\n'.join(lines), size=size, weight=weight, color=color, ha=ha, va=va)


@fig('x_bars_c1')
def x_bars_c1(w, h, items=(), unit='', size=18, caption='', **_):
    s = Scene(w, h)
    n = len(items)
    lab_w = 3.4
    foot = 0.75
    mv = max(i['value'] for i in items)
    row = (h - foot - 0.1) / n
    bx0 = lab_w + 0.2
    bar_w = w - bx0 - 1.9
    for i, it in enumerate(items):
        yc = h - 0.1 - (i + 0.5) * row
        _wrap(s, lab_w, yc, lab_w - 0.1, it['label'], size, ha='right')
        bw = max(0.04, bar_w * it['value'] / mv)
        s.rect(bx0, yc - row * 0.28, bw, row * 0.56, fill=GOLD if it.get('hl') else SHADE, edge=INK, lw=2)
        s.text(bx0 + bw + 0.15, yc, f"{it['value']:g}{unit}", size=size, weight='bold', ha='left')
    s.line(bx0, foot - 0.05, bx0, h - 0.1, color=INK, lw=2)
    _wrap(s, bx0, 0.35, w - bx0 - 0.1, caption, 16, color=MUTE, ha='left')
    return s


@fig('x_tree_c1')
def x_tree_c1(w, h, node=None, size=16, **_):
    s = Scene(w, h)
    d = _dm._depth(node)
    nl = _dm._leaves(node)
    slot = (w - 0.2) / nl
    ylev = lambda k: h - 0.55 - k * ((h - 1.1) / max(d, 1))

    def draw(n, k, left):
        wd = _dm._leaves(n) * slot
        cx = 0.1 + left + wd / 2
        if 'v' in n:
            bw = min(slot - 0.12, 1.5)
            s.box(cx - bw / 2, ylev(k) - 0.33, bw, 0.66, n['v'], size=size, fill=GOLD, edge=INK, lw=1.8, weight='bold')
            return cx
        lc = draw(n['yes'], k + 1, left)
        rc = draw(n['no'], k + 1, left + _dm._leaves(n['yes']) * slot)
        qw = min(max(K.width_in(n['q'], size, 'bold') + 0.35, 1.6), wd - 0.1 if wd > 1.8 else 3.0)
        s.box(cx - qw / 2, ylev(k) - 0.33, qw, 0.66, n['q'], size=size, fill=PAPER, edge=INK, lw=2.0, weight='bold')
        for c, lab in ((lc, 'yes'), (rc, 'no')):
            side = -1 if c < cx else 1
            x_top, y_top, y_bot = cx + side * 0.25, ylev(k) - 0.33, ylev(k + 1) + 0.33
            s.line(x_top, y_top, c, y_bot, color=INK, lw=1.8)
            xm, ym = (x_top + c) / 2, (y_top + y_bot) / 2
            s.text(xm + side * 0.38, ym + 0.02, lab, size=size, color=RED, weight='bold')
        return cx
    draw(node, 0, 0)
    return s


@fig('x_descent_c1')
def x_descent_c1(w, h, labels=('Start: a big loss', 'Each step: update the parameter a little', 'Bottom: the smallest\nloss we can find'), size=17, **_):
    s = Scene(w, h)
    x0, x1, y0, y1 = 0.7, w - 0.4, 0.7, h - 0.5
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    s.text((x0 + x1) / 2, 0.3, 'a parameter the model can change (for example a slope)', size=16, color=MUTE)
    s.text(0.3, (y0 + y1) / 2, 'loss (MSE)', size=16, color=MUTE, rot=90)
    xs = np.linspace(0, 1, 120)
    curve = lambda u: 0.12 + 0.88 * (2 * u - 1) ** 2
    px = lambda u: x0 + 0.25 + u * (x1 - x0 - 0.5)
    py = lambda v: y0 + 0.15 + v * (y1 - y0 - 0.3)
    s.ax.plot([px(u) for u in xs], [py(curve(u)) for u in xs], color=INK, lw=3, zorder=3)
    steps = [0.05, 0.2, 0.33, 0.42, 0.47, 0.5]
    for i, u in enumerate(steps):
        s.circle(px(u), py(curve(u)), 0.13 if i not in (0, len(steps) - 1) else 0.17, fill=GOLD if i in (0, len(steps) - 1) else PAPER, edge=INK, lw=2, z=5)
        if i:
            s.arrow(px(steps[i - 1]) + 0.1, py(curve(steps[i - 1])) - 0.05, px(u) - 0.1, py(curve(u)) + 0.05, color=RED, lw=2, head=14, z=4)
    s.text(px(0.05) + 0.25, py(curve(0.05)) + 0.15, labels[0], size=size, ha='left', weight='bold')
    s.text(px(0.5), py(0.72), labels[1], size=size, color=RED, weight='bold')
    s.text(px(0.55), py(0.40), labels[2], size=size, ha='center', weight='bold')
    return s


@fig('x_sheet_c1')
def x_sheet_c1(w, h, headers=(), rows=(), rowlabels=(), hl=None, size=18, **_):
    """Like the sheet picture, but the numbers at the left are given (the real row numbers in the file), and the column letters are left out."""
    s = Scene(w, h)
    n = len(headers)
    lw_ = 0.95
    for sz in range(int(size), 13, -1):
        raw = [max([K.width_in(str(headers[c]), sz, 'bold')] + [K.width_in(str(r[c]), sz) for r in rows]) + 0.3 for c in range(n)]
        if sum(raw) + lw_ <= w:
            break
    cw = [min(x, 3.2) for x in raw]
    extra = (w - lw_ - 0.1 - sum(cw)) / n
    cw = [c + extra for c in cw] if extra > 0 else [c * (w - lw_ - 0.1) / sum(cw) for c in cw]
    lh = sz * 1.15 / 72
    wrapc = lambda t, wd, kind='regular': K.wrap(str(t), sz, kind, wd - 0.2)
    heights = [max(len(wrapc(headers[c], cw[c], 'bold')) for c in range(n)) * lh + 0.2]
    for r in rows:
        heights.append(max(len(wrapc(r[c], cw[c])) for c in range(n)) * lh + 0.18)
    total = sum(heights)
    top = h - 0.05
    x0 = lw_
    s.rect(x0, top - total, sum(cw), total, fill=PAPER, edge=INK, lw=1.8)
    y = top
    for ri, hh in enumerate(heights):
        cx = x0
        for c in range(n):
            txt = headers[c] if ri == 0 else rows[ri - 1][c]
            if hl and ri > 0 and hl[0] == ri - 1 and hl[1] == c:
                s.rect(cx + 0.02, y - hh + 0.02, cw[c] - 0.04, hh - 0.04, fill=GOLD, edge=GOLD, lw=0, z=2)
            s.text(cx + 0.1, y - hh / 2, '\n'.join(wrapc(txt, cw[c], 'bold' if ri == 0 else 'regular')), size=sz, weight='bold' if ri == 0 else 'normal', ha='left', color=INK if ri == 0 else BODY, z=5)
            cx += cw[c]
        s.line(x0, y - hh, x0 + sum(cw), y - hh, color=INK if ri == 0 else HAIR, lw=2.0 if ri == 0 else 1.0, z=4)
        if ri > 0:
            s.text(x0 - 0.1, y - hh / 2, str(rowlabels[ri - 1]), size=15, color=GREY, ha='right')
        y -= hh
    s.text(x0 - 0.1, top - heights[0] / 2, 'file row', size=14, color=GREY, ha='right')
    return s
