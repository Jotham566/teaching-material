"""Figure kinds for Sessions 1 to 3 of Mathematics for AI and ML (author A). Registered as x_ma_*, used as visual=dict(kind='ma_...').

Session 1 (functions and logarithms)
  ma_sigma     values, name        a row of boxes with indices, the sigma expression above and the expanded sum below
  ma_function  rule, pairs         a function drawn as a machine: inputs go in, outputs come out
  ma_graph     curves, points, xlim, ylim, xticks, yticks, xlabel, ylabel, mirror
  ma_chain     words, probs        a sentence as a chain of probabilities, then the product and the sum of logarithms
  ma_scale     (none)              why the product underflows: exponents on a line
  ma_nextword  words, probs, loss  five possible next words as bars, with minus ln p beside each
Session 2 (vectors)
  ma_rowvec    headers, rows, row  one row of a table becomes a vector
  ma_vec2d     arrows, dots, segments, arc, arcs, xlim, ylim
  ma_trig      deg                 trigonometry refresher: an arrow of length 1, its cosine, and angles in degrees and radians
  ma_dot       u, v                the dot product as matching products added up
  ma_rank      items, best         horizontal bars of a score, best one in gold
Session 3 (matrices)
  ma_matgrid   values, hl          a matrix with row and column indices and its shape
  ma_transform panels, shape       a shape and its image under a matrix, with the images of the two axis arrows
  ma_matvec    A, x, row, names    matrix times vector, one row at a time
  ma_matmul    A, B, row, col, names  matrix times matrix, one entry at a time
  ma_shapes    (none)              shapes that match and shapes that do not
  ma_transpose A                   a matrix and its transpose
  ma_layer     x, y, hl, wrow      one layer y = W x + b; the weights into output hl are dark and labelled
  ma_params    (none)              the toy network 3, 4, 2 with the count of its numbers
  ma_logbars   items               bars on a logarithmic scale, from 26 numbers to billions
"""
import math

import numpy as np
from matplotlib.patches import Polygon, Arc

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD, fig
import slidekit as K


def _fmt(v):
    if isinstance(v, str):
        return v
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v))).replace('-', '−')
    return f'{v:g}'.replace('-', '−')


def draw_matrix(s, x, ytop, M, cw=0.7, ch=0.55, size=20, hl_rows=(), hl_cols=(), hl_cells=(), fills=None, color=INK, bracket=True, bold=False):
    """Draw a matrix (list of rows) with its top-left corner at (x, ytop). Highlighted rows, columns and cells get a gold fill. Returns (width, height)."""
    m, n = len(M), len(M[0])
    pad = 0.12
    for i in range(m):
        for j in range(n):
            bx, by = x + pad + j * cw, ytop - (i + 1) * ch
            hl = i in hl_rows or j in hl_cols or (i, j) in hl_cells
            fill = (fills or {}).get((i, j), GOLD if hl else None)
            if fill:
                s.rect(bx + 0.02, by + 0.02, cw - 0.04, ch - 0.04, fill=fill, edge=fill, lw=0, z=1)
            s.text(bx + cw / 2, by + ch / 2, _fmt(M[i][j]), size=size, color=color, weight='bold' if bold else 'normal')
    w, h = n * cw + 2 * pad, m * ch
    if bracket:
        for xx, d in ((x, 1), (x + w, -1)):
            s.line(xx, ytop, xx, ytop - h, lw=2.2)
            s.line(xx, ytop, xx + d * 0.1, ytop, lw=2.2)
            s.line(xx, ytop - h, xx + d * 0.1, ytop - h, lw=2.2)
    return w, h


# ------------------------------------------------------------------ Session 1
@fig('x_ma_sigma')
def x_ma_sigma(w, h, values=(3, 5, 2, 8), name='x', size=22, **_):
    s = Scene(w, h)
    n = len(values)
    s.text(w / 2, h - 0.95, rf'$\sum_{{i=1}}^{{{n}}} {name}_i$', size=34)
    s.text(w / 2, h - 2.0, f'Add up the {name}-values from i = 1 to i = {n}', size=17, color=MUTE)
    bw = 1.05
    gap = 0.2
    tot = n * bw + (n - 1) * gap
    x0 = (w - tot) / 2
    y = 1.35
    for i, v in enumerate(values):
        x = x0 + i * (bw + gap)
        s.box(x, y, bw, 0.8, _fmt(v), size=size + 2, fill=PAPER, edge=INK, lw=2, r=0.04)
        s.text(x + bw / 2, y + 1.1, rf'${name}_{i + 1}$', size=20, color=RED)
        s.text(x + bw / 2, y - 0.3, f'i = {i + 1}', size=15, color=GREY)
    total = sum(values)
    s.text(w / 2, 0.45, ' + '.join(_fmt(v) for v in values) + f' = {_fmt(total)}', size=26, weight='bold')
    return s


@fig('x_ma_function')
def x_ma_function(w, h, rule='f(x) = 2x + 1', pairs=((0, 1), (1, 3), (2, 5), (3, 7)), size=20, **_):
    s = Scene(w, h)
    mx, mw = w / 2 - 1.5, 3.0
    s.box(mx, h / 2 - 0.9, mw, 1.8, '', fill=INK, edge=INK, r=0.1)
    s.text(w / 2, h / 2 + 0.45, 'function', size=17, color=GOLD, weight='bold')
    s.text(w / 2, h / 2 - 0.2, rule, size=24, color=PAPER, weight='bold')
    n = len(pairs)
    ys = np.linspace(h - 0.8, 0.6, n)
    for (a, b), y in zip(pairs, ys):
        s.text(0.75, y, f'x = {_fmt(a)}', size=size, ha='center')
        s.arrow(1.45, y, mx - 0.1, h / 2 + (y - h / 2) * 0.25, lw=2, head=14, color=GREY)
        s.arrow(mx + mw + 0.1, h / 2 + (y - h / 2) * 0.25, w - 1.95, y, lw=2, head=14, color=GREY)
        s.text(w - 0.95, y, f'f(x) = {_fmt(b)}', size=size, ha='center', weight='bold')
    s.text(0.75, h - 0.2, 'input', size=16, color=RED, weight='bold')
    s.text(w - 0.95, h - 0.2, 'output', size=16, color=RED, weight='bold')
    return s


_SAFE = {'np': np, 'exp': np.exp, 'log': np.log}


@fig('x_ma_graph')
def x_ma_graph(w, h, curves=(), points=(), xlim=(0, 5), ylim=(0, 10), xticks=None, yticks=None, xlabel='x', ylabel='y', mirror=False, size=16, labels=(), segs=(), **_):
    """curves: [{'fn': '2*x+1', 'label': 'f(x) = 2x + 1', 'color': 'red', 'lx': 3.0, 'ly': 5, 'ha': 'left'}]. points: [{'x', 'y', 'label', 'dx', 'dy', 'ha'}]. labels: [(x, y, text, color)] free text."""
    s = Scene(w, h)
    x0, x1, y0, y1 = 1.15, w - 0.35, 0.85, h - 0.3
    px = lambda v: x0 + (v - xlim[0]) / (xlim[1] - xlim[0]) * (x1 - x0)
    py = lambda v: y0 + (v - ylim[0]) / (ylim[1] - ylim[0]) * (y1 - y0)
    xticks = xticks if xticks is not None else list(range(int(xlim[0]), int(xlim[1]) + 1))
    yticks = yticks if yticks is not None else list(range(int(ylim[0]), int(ylim[1]) + 1, max(1, int((ylim[1] - ylim[0]) // 5))))
    for t in xticks:
        s.line(px(t), y0, px(t), y1, color=PALE, lw=1.0, z=0)
        s.text(px(t), y0 - 0.25, _fmt(t), size=14, color=GREY)
    for t in yticks:
        s.line(x0, py(t), x1, py(t), color=PALE, lw=1.0, z=0)
        s.text(x0 - 0.12, py(t), _fmt(t), size=14, color=GREY, ha='right')
    if ylim[0] < 0 < ylim[1]:
        s.line(x0, py(0), x1, py(0), color=MUTE, lw=1.6, z=1)
    if xlim[0] < 0 < xlim[1]:
        s.line(px(0), y0, px(0), y1, color=MUTE, lw=1.6, z=1)
    s.line(x0, y0, x1, y0, lw=2.2, z=2)
    s.line(x0, y0, x0, y1, lw=2.2, z=2)
    s.text((x0 + x1) / 2, 0.22, xlabel, size=size, color=MUTE)
    s.text(0.3, (y0 + y1) / 2, ylabel, size=size, color=MUTE, rot=90)
    if mirror:
        lo, hi = max(xlim[0], ylim[0]), min(xlim[1], ylim[1])
        s.ax.plot([px(lo), px(hi)], [py(lo), py(hi)], color=GREY, lw=2, ls='--', zorder=2)
    for sg in segs:
        s.ax.plot([px(sg[0]), px(sg[2])], [py(sg[1]), py(sg[3])], color=sg[4] if len(sg) > 4 else GREY, lw=1.8, ls='--', zorder=3)
    for c in curves:
        xs = np.linspace(c.get('x0', xlim[0]), c.get('x1', xlim[1]), 400)
        with np.errstate(all='ignore'):
            ys = eval(c['fn'], {'__builtins__': {}}, dict(_SAFE, x=xs))
        ok = np.isfinite(ys) & (ys >= ylim[0] - 1e-9) & (ys <= ylim[1] + 1e-9)
        xs, ys = xs[ok], ys[ok]
        col = {'red': RED, 'ink': INK, 'gold': GOLD, 'grey': MUTE}.get(c.get('color', 'ink'), INK)
        s.ax.plot([px(a) for a in xs], [py(b) for b in ys], color=col, lw=3.6, zorder=4)
        if c.get('label'):
            s.text(px(c['lx']), py(c['ly']), c['label'], size=size + 1, color=col if col != GOLD else INK, weight='bold', ha=c.get('ha', 'left'))
    for p in points:
        s.circle(px(p['x']), py(p['y']), 0.09, fill=GOLD, edge=INK, lw=1.6, z=6)
        if p.get('label'):
            s.text(px(p['x']) + p.get('dx', 0.18), py(p['y']) + p.get('dy', 0.2), p['label'], size=size, ha=p.get('ha', 'left'), color=INK, z=7)
    for (lx, ly, txt, col) in labels:
        s.text(px(lx), py(ly), txt, size=size + 1, color={'red': RED, 'ink': INK, 'grey': MUTE}.get(col, INK), weight='bold', ha='left')
    return s


@fig('x_ma_chain')
def x_ma_chain(w, h, words=(), probs=(), size=20, sentence_note='A short sentence, one word at a time (illustrative: made-up probabilities)', **_):
    """Each word with its probability given the words before it; then the product, and the sum of natural logarithms."""
    s = Scene(w, h)
    n = len(words)
    bw = (w - 0.3 - 0.45 * (n - 1)) / n
    y = h - 1.55
    for i, (wd, p) in enumerate(zip(words, probs)):
        x = 0.15 + i * (bw + 0.45)
        s.box(x, y, bw, 0.7, wd, size=size, weight='bold', fill=PAPER, edge=INK, lw=2)
        s.text(x + bw / 2, y - 0.3, f'p = {p:g}', size=17, color=RED, weight='bold')
        s.text(x + bw / 2, y - 0.78, f'ln p = {np.log(p):.3f}'.replace('-', '−'), size=16, color=BODY)
        if i < n - 1:
            s.text(x + bw + 0.225, y + 0.35, '×', size=24, color=INK, weight='bold')
    s.text(w / 2, h - 0.4, sentence_note, size=17, color=MUTE)
    prod = float(np.prod(probs))
    sl = float(np.sum(np.log(probs)))
    if n > 4:
        s.text(w / 2, 0.95, 'Multiply the probabilities: ' + ' × '.join(f'{p:g}' for p in probs) + f' = {prod:.6f}', size=19, weight='bold')
        s.text(w / 2, 0.4, f'Add the {n} ln p values: {sl:.4f}'.replace('-', '−'), size=21, weight='bold', color=RED)
    else:
        s.text(w / 2, 0.95, 'Multiply the probabilities: ' + ' × '.join(f'{p:g}' for p in probs) + f' = {prod:.3f}', size=21, weight='bold')
        s.text(w / 2, 0.4, 'Add the logarithms: ' + ' + '.join(f'({np.log(p):.3f})' for p in probs).replace('-', '−') + f' = {sl:.3f}'.replace('-', '−'), size=21, weight='bold', color=RED)
    return s


@fig('x_ma_scale')
def x_ma_scale(w, h, size=18, **_):
    s = Scene(w, h)
    xa, xb = 0.8, w - 0.9
    ex = lambda e: xa + (e / -720.0) * (xb - xa)
    yl = h - 1.35
    s.arrow(xa, yl, xb + 0.5, yl, lw=2.4, head=16)
    for e in (0, -100, -200, -300, -400, -500, -600, -700):
        s.line(ex(e), yl - 0.1, ex(e), yl + 0.1, lw=1.8)
        s.text(ex(e), yl + 0.35, f'$10^{{{e}}}$', size=15, color=GREY)
    s.text(w / 2, h - 0.35, 'Powers of ten, from 1 down to a very small number', size=17, color=MUTE)
    s.rect(xa, yl - 0.4, ex(-308) - xa, 0.28, fill=GOLD, edge=INK, lw=1.4)
    s.text(xa + 0.1, yl - 0.85, 'Gold: the numbers a computer can store, down to about $10^{-308}$', size=17, ha='left', weight='bold')
    s.circle(ex(-699), yl, 0.12, fill=RED, edge=INK, lw=1.6, z=6)
    s.text(xb + 0.35, yl - 1.55, '1000 words at probability 0.2 each:\nthe product is about $10^{-699}$.\nThe computer shows 0.', size=17, color=RED, weight='bold', ha='right')
    s.arrow(ex(-699), yl - 1.05, ex(-699), yl - 0.2, color=RED, lw=1.8, head=12)
    s.text(w / 2, 0.45, 'The sum of the logarithms is 1000 × ln 0.2 = −1609.4. That is an ordinary number.', size=19, weight='bold')
    return s


@fig('x_ma_nextword')
def x_ma_nextword(w, h, words=(), probs=(), loss=True, highlight=None, prompt='', size=19, **_):
    s = Scene(w, h)
    n = len(words)
    top = h - 0.95
    if prompt:
        s.text(0.2, h - 0.4, prompt, size=19, ha='left', weight='bold')
    s.text(2.3, top - 0.02, 'probability p', size=15, color=MUTE, ha='left')
    if loss:
        s.text(w - 0.1, top - 0.02, '−ln p', size=16, color=RED, ha='right', weight='bold')
    rh = (top - 0.35) / n
    bx0, bmax = 2.3, w - 2.3 - (1.75 if loss else 0.9)
    for i, (wd, p) in enumerate(zip(words, probs)):
        yc = top - 0.4 - (i + 0.5) * rh + 0.1
        s.text(0.2, yc, wd, size=size, ha='left', weight='bold' if i == highlight else 'normal')
        bw = max(0.05, bmax * p / max(probs))
        s.rect(bx0, yc - rh * 0.3, bw, rh * 0.6, fill=GOLD if i == highlight else PALE, edge=INK, lw=1.4)
        s.text(bx0 + bw + 0.1, yc, f'{p:.2f}', size=size, ha='left')
        if loss:
            s.text(w - 0.1, yc, f'{-np.log(p):.3f}', size=size, ha='right', color=RED, weight='bold' if i == highlight else 'normal')
    return s


# ------------------------------------------------------------------ Session 2
@fig('x_ma_rowvec')
def x_ma_rowvec(w, h, headers=(), rows=(), row=0, vec_label='', size=19, **_):
    s = Scene(w, h)
    n = len(headers)
    cw = [3.3] + [0.95] * (n - 1)
    ch = 0.52
    ytop = h - 0.35
    xx = 0.1
    for j, hd in enumerate(headers):
        s.text(xx + (0.1 if j == 0 else cw[j] / 2), ytop, hd, size=16, weight='bold', color=MUTE, ha='left' if j == 0 else 'center')
        xx += cw[j]
    for i, r in enumerate(rows):
        yy = ytop - 0.3 - (i + 1) * ch
        xx = 0.1
        for j, v in enumerate(r):
            s.rect(xx, yy, cw[j], ch, fill=GOLD if i == row else PAPER, edge=INK, lw=1.4)
            s.text(xx + (0.1 if j == 0 else cw[j] / 2), yy + ch / 2, str(v), size=size - 3 if j == 0 else size, ha='left' if j == 0 else 'center')
            xx += cw[j]
    ybot = ytop - 0.3 - len(rows) * ch
    vals = rows[row][1:]
    s.text(0.2, ybot - 0.6, 'The gold row, written as a vector:', size=19, weight='bold', ha='left')
    x0 = 3.8
    s.text(x0 - 0.2, ybot - 1.45, vec_label + ' =', size=22, ha='right', weight='bold')
    draw_matrix(s, x0, ybot - 1.15, [list(vals)], cw=1.0, ch=0.6, size=22)
    return s


@fig('x_ma_vec2d')
def x_ma_vec2d(w, h, arrows=(), dots=(), segments=(), arc=None, arcs=(), xlim=(0, 8), ylim=(0, 8), size=18, grid=True, **_):
    """arrows: [{'v': (3, 4), 'o': (0, 0), 'label': 'a', 'color': 'ink'|'red'|'grey', 'dash': False, 'dx': .., 'dy': .., 'ha': ..}]."""
    s = Scene(w, h)
    ax0, ax1, ay0, ay1 = 0.75, w - 0.3, 0.6, h - 0.3
    unit = min((ax1 - ax0) / (xlim[1] - xlim[0]), (ay1 - ay0) / (ylim[1] - ylim[0]))
    ox = ax0
    oy = ay0
    px = lambda v: ox + (v - xlim[0]) * unit
    py = lambda v: oy + (v - ylim[0]) * unit
    cmap = {'red': RED, 'grey': MUTE, 'ink': INK}
    if grid:
        for t in range(int(xlim[0]), int(xlim[1]) + 1):
            s.line(px(t), py(ylim[0]), px(t), py(ylim[1]), color=PALE, lw=1.0, z=0)
            s.text(px(t), py(ylim[0]) - 0.22, _fmt(t), size=14, color=GREY)
        for t in range(int(ylim[0]), int(ylim[1]) + 1):
            s.line(px(xlim[0]), py(t), px(xlim[1]), py(t), color=PALE, lw=1.0, z=0)
            s.text(px(xlim[0]) - 0.15, py(t), _fmt(t), size=14, color=GREY, ha='right')
    s.line(px(xlim[0]), py(ylim[0]), px(xlim[1]), py(ylim[0]), lw=2, z=1)
    s.line(px(xlim[0]), py(ylim[0]), px(xlim[0]), py(ylim[1]), lw=2, z=1)
    for sg in segments:
        a, b = sg['a'], sg['b']
        col = cmap.get(sg.get('color', 'grey'))
        s.ax.plot([px(a[0]), px(b[0])], [py(a[1]), py(b[1])], color=col, lw=2.2, ls='--', zorder=3)
        if sg.get('label'):
            s.text(px((a[0] + b[0]) / 2) + sg.get('dx', 0.0), py((a[1] + b[1]) / 2) + sg.get('dy', 0.0), sg['label'], size=size, color=col, weight='bold', ha=sg.get('ha', 'center'))
    for a in arrows:
        o = a.get('o', (0, 0))
        v = a['v']
        col = cmap.get(a.get('color', 'ink'))
        s.arrow(px(o[0]), py(o[1]), px(o[0] + v[0]), py(o[1] + v[1]), color=col, lw=3.0 if not a.get('dash') else 2.2, head=18, dash=a.get('dash', False), z=5)
        if a.get('label'):
            s.text(px(o[0] + v[0]) + a.get('dx', 0.12), py(o[1] + v[1]) + a.get('dy', 0.18), a['label'], size=size + 1, color=col, weight='bold', ha=a.get('ha', 'left'), z=8)
    for d in dots:
        s.circle(px(d['p'][0]), py(d['p'][1]), 0.1, fill=d.get('fill', GOLD), edge=INK, lw=1.6, z=6)
        if d.get('label'):
            s.text(px(d['p'][0]) + d.get('dx', 0.15), py(d['p'][1]) + d.get('dy', 0.2), d['label'], size=size, ha=d.get('ha', 'left'), weight='bold', z=8)
    for ac in ([arc] if arc else []) + list(arcs):
        a1, a2 = math.degrees(math.atan2(ac['b'][1], ac['b'][0])), math.degrees(math.atan2(ac['a'][1], ac['a'][0]))
        lo, hi = min(a1, a2), max(a1, a2)
        r = ac.get('r', 1.0) * unit
        col = cmap.get(ac.get('color', 'red'), RED)
        s.ax.add_patch(Arc((px(0), py(0)), 2 * r, 2 * r, theta1=lo, theta2=hi, color=col, lw=2.4, zorder=6))
        if ac.get('label'):
            mid = math.radians(ac.get('at', (lo + hi) / 2))
            s.text(px(0) + (r + ac.get('lr', 0.45)) * math.cos(mid), py(0) + (r + ac.get('lr', 0.45)) * math.sin(mid), ac['label'], size=ac.get('size', size), color=col, weight='bold')
    return s


@fig('x_ma_trig')
def x_ma_trig(w, h, deg=60, size=17, **_):
    """Trigonometry refresher: an arrow of length 1 at angle theta; cos theta is how far it reaches along the horizontal. A small table of angles in degrees and radians beside it."""
    s = Scene(w, h)
    tw = [0.8, 1.25, 0.9]
    R_ = min(2.4, h - 1.7, (w - sum(tw) - 0.75) / 2.15)
    cx, cy = 0.3 + R_ * 1.08, 0.95
    th = np.linspace(0, math.pi, 200)
    s.ax.plot(cx + R_ * np.cos(th), cy + R_ * np.sin(th), color=HAIR, lw=1.6, zorder=1)
    s.line(cx - R_ - 0.15, cy, cx + R_ + 0.2, cy, lw=2, z=1)
    for v in (-1, 0, 1):
        s.line(cx + v * R_, cy - 0.07, cx + v * R_, cy + 0.07, lw=2, z=1)
        s.text(cx + v * R_, cy - 0.3, _fmt(v), size=15, color=GREY)
    a = math.radians(deg)
    tx, ty = cx + R_ * math.cos(a), cy + R_ * math.sin(a)
    s.line(tx, ty, tx, cy, color=MUTE, lw=1.8, dash=True, z=2)
    s.line(cx, cy, tx, cy, color=RED, lw=5, z=3)
    s.arrow(cx, cy, tx, ty, lw=3.0, head=18, z=5)
    s.text(cx + (tx - cx) / 2 - 0.3, cy + (ty - cy) / 2 + 0.12, 'length 1', size=15, color=INK, ha='right', rot=0)
    s.ax.add_patch(Arc((cx, cy), 0.9, 0.9, theta1=0, theta2=deg, color=GOLD, lw=3, zorder=6))
    s.text(cx + 0.68 * math.cos(a / 2) + 0.05, cy + 0.68 * math.sin(a / 2), 'θ', size=19, color=INK, weight='bold', ha='left')
    s.text(cx + (tx - cx) / 2, cy - 0.62, f'cos {deg}° = {math.cos(a):.1f}', size=size, color=RED, weight='bold')
    s.text(0.1, h - 0.3, f'An arrow of length 1 at angle θ = {deg}°', size=15, color=MUTE, ha='left')
    rows = [['angle', 'radians', 'cosine'], ['0°', '0', '1'], [f'{deg}°', f'{math.radians(deg):.3f}', f'{math.cos(a):.1f}'], ['90°', '1.571', '0'], ['180°', '3.142 (π)', '−1']]
    x0 = w - sum(tw) - 0.05
    s.table(x0, h - 0.55, tw, 0.5, rows, size=15, hl_rows=(2,))
    return s


@fig('x_ma_dot')
def x_ma_dot(w, h, u=(1, 2, 2), v=(2, 0, 1), size=22, **_):
    s = Scene(w, h)
    n = len(u)
    bw, gap = 1.0, 0.3
    tot = n * bw + (n - 1) * gap
    x0 = (w - tot) / 2 + 0.9
    yu, yv, yp = h - 0.9, h - 1.65, h - 2.9
    s.text(x0 - 0.35, yu + 0.3, 'u', size=24, ha='right', weight='bold')
    s.text(x0 - 0.35, yv + 0.3, 'v', size=24, ha='right', weight='bold')
    for i in range(n):
        x = x0 + i * (bw + gap)
        s.box(x, yu, bw, 0.6, _fmt(u[i]), size=size, fill=PAPER, lw=2, r=0.03)
        s.box(x, yv, bw, 0.6, _fmt(v[i]), size=size, fill=PAPER, lw=2, r=0.03)
        s.arrow(x + bw / 2, yv - 0.05, x + bw / 2, yp + 0.72, lw=2, head=14, color=GREY)
        s.box(x, yp, bw, 0.6, _fmt(u[i] * v[i]), size=size, fill=GOLD, lw=2, r=0.03, weight='bold')
        s.text(x + bw / 2, yp - 0.3, f'{_fmt(u[i])} × {_fmt(v[i])}', size=15, color=MUTE)
    s.text(x0 - 0.35, yp + 0.3, 'products', size=15, color=MUTE, ha='right')
    tot_v = sum(a * b for a, b in zip(u, v))
    s.text(w / 2, 0.5, ' + '.join(_fmt(a * b) for a, b in zip(u, v)) + f' = {_fmt(tot_v)}', size=28, weight='bold', color=RED)
    s.text(w / 2, 1.05, 'Add the products: this is the dot product of u and v', size=17, color=MUTE)
    return s


@fig('x_ma_rank')
def x_ma_rank(w, h, items=(), best=0, vmax=1.0, fmt='{:.3f}', size=18, header='', lab_w=4.3, **_):
    s = Scene(w, h)
    n = len(items)
    top = h - (0.5 if header else 0.05)
    if header:
        s.text(0.1, h - 0.25, header, size=16, color=MUTE, ha='left')
    rh = (top - 0.05) / n
    bmax = w - lab_w - 1.1
    for i, (lab, val) in enumerate(items):
        yc = top - (i + 0.5) * rh
        s.text(0.1, yc, lab, size=size, ha='left', weight='bold' if i == best else 'normal')
        bw = max(0.04, bmax * abs(val) / vmax)
        s.rect(lab_w, yc - rh * 0.3, bw, rh * 0.6, fill=GOLD if i == best else PALE, edge=INK, lw=1.4)
        s.text(lab_w + bw + 0.1, yc, fmt.format(val), size=size, ha='left', weight='bold' if i == best else 'normal')
    return s


# ------------------------------------------------------------------ Session 3
@fig('x_ma_matgrid')
def x_ma_matgrid(w, h, values=(), hl=None, row_labels=None, size=20, shape_text='', cw=0.95, ch=0.5, **_):
    s = Scene(w, h)
    m, n = len(values), len(values[0])
    width = n * cw + 0.24
    x0 = (w - width) / 2 + 0.5
    ytop = h - 1.0
    for j in range(n):
        s.text(x0 + 0.12 + (j + 0.5) * cw, ytop + 0.3, f'column {j + 1}', size=15, color=MUTE)
    for i in range(m):
        s.text(x0 - 0.2, ytop - (i + 0.5) * ch, (row_labels[i] if row_labels else f'row {i + 1}'), size=15, color=MUTE, ha='right')
    draw_matrix(s, x0, ytop, values, cw=cw, ch=ch, size=size, hl_cells=[tuple(hl)] if hl else ())
    s.text(w / 2, h - 0.35, shape_text, size=19, weight='bold')
    return s


@fig('x_ma_transform')
def x_ma_transform(w, h, panels=(), shape=((0, 0), (2, 0), (2, 1), (1, 1), (1, 3), (0, 3)), axes_arrows=False, size=17, **_):
    """panels: [{'title': 'Scale', 'M': [[2,0],[0,1]], 'M_text': 'x doubles'}]. The original shape is dashed grey, the image is gold."""
    s = Scene(w, h)
    P = np.array(shape, float)
    n = len(panels)
    gap = 0.25
    pw = (w - gap * (n - 1)) / n
    mats = [np.array(p['M'], float) for p in panels]
    pts = [P] + [P @ M.T for M in mats]
    if axes_arrows:
        pts += [M.T for M in mats]
    allp = np.vstack(pts)
    lo = np.minimum(allp.min(0) - 0.4, -0.3)
    hi = np.maximum(allp.max(0) + 0.4, 0.3)
    span = max(hi[0] - lo[0], hi[1] - lo[1])
    has_note = any(p.get('note') for p in panels)
    top_h = 1.5 if has_note else 1.0
    side = min(pw - 0.1, h - top_h - 0.1)
    unit = side / span
    c0 = ((hi[0] + lo[0]) / 2, (hi[1] + lo[1]) / 2)
    for k, (p, M) in enumerate(zip(panels, mats)):
        ox = k * (pw + gap) + (pw - side) / 2
        oy = 0.1
        px = lambda v, ox=ox: ox + side / 2 + (v - c0[0]) * unit
        py = lambda v, oy=oy: oy + side / 2 + (v - c0[1]) * unit
        s.rect(ox, oy, side, side, fill=PAPER, edge=HAIR, lw=1.2, z=0)
        for t in range(int(math.floor(lo[0])), int(math.ceil(hi[0])) + 1):
            if lo[0] <= t <= hi[0]:
                s.line(px(t), oy, px(t), oy + side, color=PALE if t else MUTE, lw=1.0 if t else 1.6, z=0)
        for t in range(int(math.floor(lo[1])), int(math.ceil(hi[1])) + 1):
            if lo[1] <= t <= hi[1]:
                s.line(ox, py(t), ox + side, py(t), color=PALE if t else MUTE, lw=1.0 if t else 1.6, z=0)
        s.ax.add_patch(Polygon([(px(a), py(b)) for a, b in P], closed=True, fc='none', ec=MUTE, lw=2, ls='--', zorder=3))
        Q = P @ M.T
        s.ax.add_patch(Polygon([(px(a), py(b)) for a, b in Q], closed=True, fc=GOLD, ec=INK, lw=2.4, zorder=4, alpha=0.9))
        if axes_arrows:
            for col, e in ((RED, (1, 0)), (INK, (0, 1))):
                v = M @ np.array(e, float)
                s.arrow(px(0), py(0), px(v[0]), py(v[1]), color=col, lw=3.4, head=18, z=8)
        dy0 = 0.5 if has_note else 0.0
        s.text(ox + side / 2, oy + side + 0.72 + dy0, p['title'], size=size + 2, weight='bold')
        if p.get('M_text'):
            s.text(ox + side / 2, oy + side + 0.3 + dy0, p['M_text'], size=size - 1, color=BODY)
        if p.get('note'):
            s.text(ox + side / 2, oy + side + 0.3, p['note'], size=size - 1, color=BODY)
    return s


@fig('x_ma_matvec')
def x_ma_matvec(w, h, A=(), x=(), row=0, work='', size=20, names=('A', 'x', 'y = A x'), caption=None, **_):
    s = Scene(w, h)
    A = [list(r) for r in A]
    m, n = len(A), len(A[0])
    xv = [[v] for v in x]
    y = [[sum(A[i][j] * x[j] for j in range(n))] for i in range(m)]
    cw, ch = 0.75, 0.55
    ytop = h - 1.0
    xA = 0.4
    wa, ha_ = draw_matrix(s, xA, ytop, A, cw=cw, ch=ch, size=size, hl_rows=(row,))
    s.text(xA + wa + 0.3, ytop - ha_ / 2, '×', size=26)
    xx = xA + wa + 0.6
    off = (m - n) * ch / 2
    wx, hx = draw_matrix(s, xx, ytop - off, xv, cw=cw, ch=ch, size=size, hl_rows=tuple(range(n)))
    s.text(xx + wx + 0.3, ytop - ha_ / 2, '=', size=26)
    xy = xx + wx + 0.6
    wy, hy = draw_matrix(s, xy, ytop, y, cw=cw, ch=ch, size=size, hl_cells=[(row, 0)])
    s.text(xA + wa / 2, ytop + 0.3, names[0], size=20, color=RED, weight='bold')
    s.text(xx + wx / 2, ytop - off + 0.3, names[1], size=20, color=RED, weight='bold')
    s.text(xy + wy / 2, ytop + 0.3, names[2], size=20, color=RED, weight='bold')
    s.text(w / 2, 0.45, work, size=19, weight='bold')
    s.text(w / 2, 0.98, caption or f'The gold row of {names[0]}, times {names[1]}, gives the gold entry of the answer', size=16, color=MUTE)
    return s


@fig('x_ma_matmul')
def x_ma_matmul(w, h, A=(), B=(), row=0, col=1, work='', size=20, names=('A', 'B', 'C = A B'), caption=None, **_):
    s = Scene(w, h)
    A = np.array(A, float)
    B = np.array(B, float)
    C = A @ B
    ncols = A.shape[1] + B.shape[1] + C.shape[1]
    cw, ch = min(0.75, (w - 0.8 - 1.2 - 0.72) / ncols), min(0.55, (h - 2.5) / A.shape[0])
    if cw < 0.65 or ch < 0.5:
        size = 18
    ytop = h - 1.0
    xA = 0.4
    wa, ha_ = draw_matrix(s, xA, ytop, A.tolist(), cw=cw, ch=ch, size=size, hl_rows=(row,))
    s.text(xA + wa + 0.3, ytop - ha_ / 2, '×', size=26)
    xB = xA + wa + 0.6
    wb, hb = draw_matrix(s, xB, ytop, B.tolist(), cw=cw, ch=ch, size=size, hl_cols=(col,))
    s.text(xB + wb + 0.3, ytop - ha_ / 2, '=', size=26)
    xC = xB + wb + 0.6
    wc, hc = draw_matrix(s, xC, ytop, C.tolist(), cw=cw, ch=ch, size=size, hl_cells=[(row, col)])
    s.text(xA + wa / 2, ytop + 0.3, names[0], size=20, color=RED, weight='bold')
    s.text(xB + wb / 2, ytop + 0.3, names[1], size=20, color=RED, weight='bold')
    s.text(xC + wc / 2, ytop + 0.3, names[2], size=20, color=RED, weight='bold')
    s.text(w / 2, 0.45, work, size=19, weight='bold')
    s.text(w / 2, 0.98, caption or 'Gold row of A, gold column of B: together they give the gold entry of C', size=16, color=MUTE)
    return s


def _dims_box(s, x, ytop, rows, cols, unit, fill=PAPER, size=18):
    bw, bh = cols * unit, rows * unit
    s.rect(x, ytop - bh, bw, bh, fill=fill, edge=INK, lw=2.2)
    s.text(x + bw / 2, ytop - bh / 2, f'{rows} × {cols}', size=size, weight='bold')
    return bw, bh


@fig('x_ma_shapes')
def x_ma_shapes(w, h, size=19, **_):
    s = Scene(w, h)
    u = 0.45
    for k, (a, b, c, d, ok) in enumerate([(2, 3, 3, 4, True), (2, 3, 2, 3, False)]):
        ytop = h - 0.35 - k * 2.3
        s.text(0.1, ytop, 'Shapes match: the two inner numbers agree (3 and 3)' if ok else 'Shapes do not match: the inner numbers differ (3 and 2)', size=17, ha='left', weight='bold', color=INK if ok else RED)
        ytop -= 0.3
        x = 0.4
        bw1, bh1 = _dims_box(s, x, ytop, a, b, u)
        s.text(x + bw1 + 0.25, ytop - 0.55, '×', size=24)
        x2 = x + bw1 + 0.5
        bw2, bh2 = _dims_box(s, x2, ytop, c, d, u)
        s.text(x2 + bw2 + 0.25, ytop - 0.55, '=', size=24)
        x3 = x2 + bw2 + 0.5
        yy = ytop - max(a, c) * u - 0.3
        if ok:
            bw3, bh3 = _dims_box(s, x3, ytop, a, d, u, fill=GOLD)
            s.text(x3 + bw3 / 2, yy, f'C is {a} × {d}', size=15, color=MUTE)
        else:
            s.box(x3, ytop - 1.1, 2.2, 1.1, 'no answer', size=18, fill=PAPER, edge=RED, lw=2.2, color=RED, weight='bold', dash=True)
        s.text(x + bw1 / 2, yy, f'A is {a} × {b}', size=15, color=MUTE)
        s.text(x2 + bw2 / 2, yy, f'B is {c} × {d}', size=15, color=MUTE)
    return s


@fig('x_ma_transpose')
def x_ma_transpose(w, h, A=((1, 2, 3), (4, 5, 6)), size=22, **_):
    s = Scene(w, h)
    A = [list(r) for r in A]
    T = [list(r) for r in zip(*A)]
    cw, ch = 0.75, 0.6
    ytop = h - 1.3
    x0 = 0.4
    wa, ha_ = draw_matrix(s, x0, ytop, A, cw=cw, ch=ch, size=size, hl_rows=(0,))
    s.text(x0 + wa / 2, ytop + 0.45, f'A is {len(A)} × {len(A[0])}', size=18, color=RED, weight='bold')
    s.arrow(x0 + wa + 0.3, ytop - ha_ / 2, x0 + wa + 1.5, ytop - ha_ / 2, lw=2.6, head=18)
    s.text(x0 + wa + 0.9, ytop - ha_ / 2 + 0.5, 'transpose', size=15, color=MUTE)
    x1 = x0 + wa + 1.8
    wt, ht = draw_matrix(s, x1, ytop + (len(T) - len(A)) * ch / 2 * 0, T, cw=cw, ch=ch, size=size, hl_cols=(0,))
    s.text(x1 + wt / 2, ytop + 0.45, rf'$A^T$ is {len(T)} × {len(T[0])}', size=18, color=RED, weight='bold')
    s.text(w / 2, 0.45, 'Rows become columns. Entry (i, j) of A is entry (j, i) of the transpose.', size=17, weight='bold')
    return s


@fig('x_ma_layer')
def x_ma_layer(w, h, x=(), y=(), size=18, hl=0, wrow=None, **_):
    """One layer y = W x + b. The lines into output hl are drawn dark; with wrow (row hl of W) each is labelled with its weight, and a zero weight is dashed."""
    s = Scene(w, h)
    nin, nout = len(x), len(y)
    xl, xr = 1.4, w - 1.5
    yin = np.linspace(h - 1.15, 1.2, nin)
    yout = np.linspace(h - 0.95, 0.95, nout)
    for i, yi in enumerate(yin):
        for j, yj in enumerate(yout):
            on = j == hl
            zero = on and wrow is not None and wrow[i] == 0
            s.line(xl + 0.28, yi, xr - 0.28, yj, color=(MUTE if zero else INK) if on else HAIR, lw=2.6 if on else 1.0, dash=zero, z=2 if on else 1)
            if on and wrow is not None:
                t_ = 0.3
                lx, ly = xl + 0.28 + t_ * (xr - xl - 0.56), yi + t_ * (yj - yi)
                s.box(lx - 0.42, ly - 0.17, 0.84, 0.34, f'w = {_fmt(wrow[i])}', size=15, fill=PAPER, edge=RED, lw=1.2, color=RED, weight='bold', z=6)
    for i, yi in enumerate(yin):
        s.circle(xl, yi, 0.28, fill=PAPER, edge=INK, lw=2, z=3)
        s.text(xl, yi, _fmt(x[i]), size=17, weight='bold', z=5)
        s.text(xl - 0.5, yi, rf'$x_{i + 1}$', size=18, ha='right')
    for j, yj in enumerate(yout):
        s.circle(xr, yj, 0.28, fill=GOLD if j == hl else PAPER, edge=INK, lw=2, z=3)
        s.text(xr, yj, _fmt(y[j]), size=17, weight='bold', z=5)
        s.text(xr + 0.5, yj, rf'$y_{j + 1}$', size=18, ha='left')
    s.text(w / 2, h - 0.25, f'Each line is one weight. Dark: the weights into y{chr(0x2080 + hl + 1)}', size=16, color=MUTE)
    s.text(xl, 0.3, 'inputs x', size=16, color=MUTE)
    s.text(xr, 0.3, 'outputs y', size=16, color=MUTE)
    return s


@fig('x_ma_params')
def x_ma_params(w, h, size=17, **_):
    s = Scene(w, h)
    layers = [('Inputs: 3', 3), ('Hidden layer: 4', 4), ('Outputs: 2', 2)]
    xs = [1.0, w / 2, w - 1.0]
    ypos = lambda n: [3.0 + (i - (n - 1) / 2) * 0.65 * -1 for i in range(n)]
    for k in range(2):
        for ya in ypos(layers[k][1]):
            for yb in ypos(layers[k + 1][1]):
                s.line(xs[k] + 0.2, ya, xs[k + 1] - 0.2, yb, color=HAIR, lw=1.0, z=1)
    for (lab, n), x in zip(layers, xs):
        for yv in ypos(n):
            s.circle(x, yv, 0.2, fill=PAPER, edge=INK, lw=2, z=3)
        s.text(x, h - 0.3, lab, size=17, weight='bold')
    s.box((xs[0] + xs[1]) / 2 - 1.2, 0.8, 2.4, 0.5, 'W1: 4 × 3 = 12', size=16, fill=GOLD, edge=INK, weight='bold')
    s.box((xs[1] + xs[2]) / 2 - 1.2, 0.8, 2.4, 0.5, 'W2: 2 × 4 = 8', size=16, fill=GOLD, edge=INK, weight='bold')
    s.text(xs[1], 1.5, 'biases b1: 4 numbers', size=16, color=RED, weight='bold')
    s.text(xs[2] - 0.2, 1.5, 'biases b2: 2 numbers', size=16, color=RED, weight='bold', ha='center')
    s.text(w / 2, 0.35, 'Parameters:  12 + 4 + 8 + 2 = 26', size=24, weight='bold')
    return s


@fig('x_ma_logbars')
def x_ma_logbars(w, h, items=(), size=18, gold_last=2, **_):
    """items: [(label, value, value_text)]. The bar length is log10 of the value, so each tick is a hundred times bigger than the last."""
    s = Scene(w, h)
    n = len(items)
    lab_w = 0.3
    top = h - 0.7
    rh = (top - 0.7) / n
    top_exp = 11.0
    bmax = w - lab_w - 1.9
    for e in range(0, 12, 2):
        xe = lab_w + bmax * e / top_exp
        s.line(xe, 0.62, xe, top - 0.02, color=PALE, lw=1.2, z=0)
        s.text(xe, 0.35, f'$10^{{{e}}}$', size=16, color=GREY)
    s.text(0.1, h - 0.25, 'Each tick to the right is a hundred times bigger', size=15, color=MUTE, ha='left')
    for i, (lab, val, vt) in enumerate(items):
        yc = top - (i + 0.5) * rh
        s.text(0.1, yc + rh * 0.3, lab, size=16, ha='left')
        bw = bmax * math.log10(val) / top_exp
        s.rect(lab_w, yc - rh * 0.4, bw, rh * 0.42, fill=GOLD if i >= n - gold_last else PALE, edge=INK, lw=1.4, z=2)
        s.text(lab_w + bw + 0.1, yc - rh * 0.19, vt, size=size, ha='left', weight='bold', z=6)
    return s
