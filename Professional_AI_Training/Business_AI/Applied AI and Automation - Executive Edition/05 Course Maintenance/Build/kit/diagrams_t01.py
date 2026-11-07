"""Figures for Session 1, Seeing: pixels, features and neurons.  Names: x_t01_*  (content kind 't01_*').

Every picture is drawn from the recorded run in demo_runs/s01/ (digits_run.py, rgb_image.py): the numbers are the real ones.
Data are read from demo_runs/s01/results_s01.npz and results_s01.json; scikit-learn's bundled digits are loaded for the feature scatter.
"""
import json
from pathlib import Path

import numpy as np
from matplotlib.colors import LinearSegmentedColormap

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD, fig

RUN = Path(__file__).resolve().parent.parent / 'demo_runs' / 's01'
_R = {}


def _res():
    if not _R:
        z = np.load(RUN / 'results_s01.npz')
        _R.update({k: z[k] for k in z.files})
        _R['json'] = json.load(open(RUN / 'results_s01.json'))
    return _R


def _frame(s):
    s.ax.set_xlim(0, s.w)
    s.ax.set_ylim(0, s.h)
    s.ax.set_aspect('equal')


def _gray(s, arr, x, y, size, frame=True, vmax=16.0):
    """Draw an 8x8 grey image (0 white .. 16 black) with its lower-left corner at (x, y), `size` inches wide."""
    s.ax.imshow(arr, cmap='gray_r', vmin=0, vmax=vmax, extent=(x, x + size, y, y + size), interpolation='nearest', zorder=2)
    if frame:
        s.rect(x, y, size, size, fill='none', edge=INK, lw=1.6, z=3)
    _frame(s)


def _rgb(s, arr, x, y, size):
    s.ax.imshow(arr.astype(np.uint8), extent=(x, x + size, y, y + size), interpolation='nearest', zorder=2)
    s.rect(x, y, size, size, fill='none', edge=INK, lw=1.6, z=3)
    _frame(s)


# ------------------------------------------------------------------ 1. an image is a grid of numbers
@fig('x_t01_pixels')
def x_t01_pixels(w, h, **_):
    r = _res()
    img = r['images'][int(r['img_i'])]
    s = Scene(w, h)
    c = 0.5
    gx, gy = 0.1, 0.3
    for i in range(8):
        for j in range(8):
            v = int(img[i, j])
            shade = 1 - 0.9 * v / 16.0
            col = (shade, shade, shade)
            s.rect(gx + j * c, gy + (7 - i) * c, c, c, fill=col, edge=HAIR, lw=0.8, z=2)
            s.text(gx + j * c + c / 2, gy + (7 - i) * c + c / 2, str(v), size=15, color=PAPER if v >= 8 else INK, weight='bold' if v >= 8 else 'normal', z=5)
    s.rect(gx, gy, 8 * c, 8 * c, fill='none', edge=INK, lw=2, z=4)
    s.text(gx + 4 * c, gy + 8 * c + 0.28, 'What the computer gets: 64 numbers', size=17, weight='bold')
    _gray(s, img, 5.2, 1.9, 2.2)
    s.text(6.3, 1.9 + 2.2 + 0.3, 'What you see', size=17, weight='bold')
    s.text(6.3, 1.4, '0 is white, 16 is black ink', size=15, color=BODY)
    s.text(6.3, 0.95, 'This is a handwritten 3', size=15, color=BODY)
    s.arrow(4.35, 3.0, 5.0, 3.0, lw=2.2)
    return s


# ------------------------------------------------------------------ 2. colour = three numbers
@fig('x_t01_rgb')
def x_t01_rgb(w, h, **_):
    img = np.load(RUN / 'rgb_image.npy')
    s = Scene(w, h)
    isz = 3.4
    ix, iy = 0.1, 0.55
    _rgb(s, img, ix, iy, isz)
    cell = isz / 8
    picks = [((0, 0), 'A'), ((2, 3), 'B'), ((7, 6), 'C')]
    for k, ((rr, cc), nm) in enumerate(picks):
        px, py = ix + cc * cell, iy + (7 - rr) * cell
        s.rect(px, py, cell, cell, fill='none', edge=RED, lw=3, z=5)
        s.text(px + cell / 2, py + cell / 2, nm, size=15, weight='bold', color=PAPER if k != 1 else INK, z=7)
    s.text(ix + isz / 2, iy + isz + 0.3, 'A tiny photo: 8 by 8 pixels', size=17, weight='bold')
    s.text(ix + isz / 2, 0.25, '8 x 8 x 3 = 192 numbers', size=17, color=BODY)
    rows = [('A', 'sky'), ('B', 'sun'), ('C', 'hill')]
    ys = [3.7, 2.55, 1.4]
    for (rr, cc), nm in [p for p in picks]:
        pass
    for k, ((rr, cc), nm) in enumerate(picks):
        col = tuple(int(v) for v in img[rr, cc])
        y = ys[k]
        s.text(4.35, y + 0.1, nm, size=17, weight='bold', color=RED)
        s.rect(4.65, y - 0.28, 0.75, 0.75, fill=tuple(v / 255 for v in col), edge=INK, lw=1.6, z=3)
        s.text(5.55, y + 0.1, f'({col[0]}, {col[1]}, {col[2]})', size=19, weight='bold', ha='left')
        s.text(5.55, y - 0.25, f'{rows[k][1]}: red, green, blue', size=15, color=BODY, ha='left')
    s.text(4.35, 4.5, 'Three numbers per pixel', size=16, color=BODY, ha='left')
    return s


# ------------------------------------------------------------------ 3. features: two measurements separate 0 from 1
@fig('x_t01_features')
def x_t01_features(w, h, **_):
    from sklearn.datasets import load_digits
    d = load_digits()
    m = d.target < 2
    ink = d.data.sum(1)[m]
    cen = d.images[:, 2:6, 3:5].reshape(len(d.target), -1).sum(1)[m]
    y = d.target[m]
    s = Scene(w, h)
    ax0, ax1, ay0, ay1 = 0.9, w - 0.2, 0.95, h - 0.75
    s.line(ax0, ay0, ax1, ay0, lw=2)
    s.line(ax0, ay0, ax0, ay1, lw=2)
    xlo, xhi = ink.min() - 10, ink.max() + 10
    px = lambda v: ax0 + 0.1 + (v - xlo) / (xhi - xlo) * (ax1 - ax0 - 0.2)
    py = lambda v: ay0 + 0.1 + v / (cen.max() * 1.05) * (ay1 - ay0 - 0.2)
    for dig, col, mk in ((0, INK, 'o'), (1, GOLD, 's')):
        sel = y == dig
        s.ax.scatter([px(v) for v in ink[sel]], [py(v) for v in cen[sel]], s=36, c=col, edgecolors=INK, linewidths=0.8, marker=mk, zorder=4)
    t = 51.76
    s.line(ax0, py(t), ax1, py(t), color=RED, lw=2.6, dash=True, z=6)
    right = int(((cen > t) == (y == 1)).sum())
    s.text((ax0 + ax1) / 2, h - 0.3, f'One rule: above the red line, say 1. Right for {right} of {len(y)}', size=16, color=RED, weight='bold')
    s.text((ax0 + ax1) / 2, 0.45, 'Feature 1: how much ink in total (less to more)', size=16, color=BODY)
    s.text(0.3, (ay0 + ay1) / 2, 'Feature 2: ink in the centre strip', size=16, color=BODY, rot=90)
    s.box(ax0 + 0.2, 1.2, 0.28, 0.28, '', fill=INK, r=0.02)
    s.text(ax0 + 0.6, 1.34, '0', size=16, ha='left', weight='bold')
    s.box(ax0 + 0.2, 1.65, 0.28, 0.28, '', fill=GOLD, r=0.02)
    s.text(ax0 + 0.6, 1.79, '1', size=16, ha='left', weight='bold')
    return s


# ------------------------------------------------------------------ 4. a weighted sum with a bias: the price of a house
@fig('x_t01_weighted')
def x_t01_weighted(w, h, area=80, beds=3, title='House A', **_):
    w_area, w_bed, bias = 2, 10, 30
    s = Scene(w, h)
    s.text(0.1, h - 0.3, f'{title}: price from floor area and bedrooms', size=18, weight='bold', ha='left')
    s.text(w - 1.9, h - 0.75, 'input x weight', size=15, color=MUTE, ha='right')
    s.text(w - 0.15, h - 0.75, 'UGX million', size=15, color=MUTE, ha='right')
    top = h - 0.95
    rh = 0.6
    rows = [(f'Floor area: {area} m\u00b2', f'{area} x {w_area}', area * w_area),
            (f'Bedrooms: {beds}', f'{beds} x {w_bed}', beds * w_bed),
            ('Base price (the bias)', 'added once', bias)]
    for i, (nm, calc, val) in enumerate(rows):
        y = top - (i + 1) * rh
        s.text(0.15, y + 0.35, nm, size=18, ha='left', weight='bold' if i < 2 else 'normal', color=INK if i < 2 else BODY)
        s.text(w - 1.9, y + 0.35, calc, size=18, ha='right', color=BODY)
        s.text(w - 0.15, y + 0.35, ('+ ' if i == 2 else '= ') + str(val), size=20, ha='right', weight='bold')
        s.line(0.1, y, w - 0.1, y, color=HAIR, lw=1)
    tot = area * w_area + beds * w_bed + bias
    y = top - 3 * rh - 0.3
    s.text(0.1, y + 0.1, f'{area * w_area} + {beds * w_bed} + {bias} = {tot}', size=21, weight='bold', ha='left')
    s.box(0.1, y - 1.0, w - 0.2, 0.7, f'Price: UGX {tot} million', size=19, fill=GOLD, lw=2, weight='bold')
    s.text(w / 2, y - 1.4, 'weighted sum + bias:  z = w1x1 + w2x2 + b  (also z = Σ wx + b)', size=15, color=BODY)
    return s


# ------------------------------------------------------------------ 5. layers: 64 pixels, 16 neurons, 10 scores
@fig('x_t01_layers')
def x_t01_layers(w, h, **_):
    r = _res()
    s = Scene(w, h)
    xs = [1.1, 3.9, 6.6]
    # input: a small 8x8 grid of squares
    c = 0.26
    gx, gy = xs[0] - 4 * c, 1.35
    img = r['images'][int(r['img_i'])]
    _gray(s, img, gx, gy, 8 * c)
    s.text(xs[0], gy + 8 * c + 0.45, 'Input layer: 64', size=17, weight='bold')
    # hidden: 16 neurons (two columns of 8 drawn as 8 + 8)
    hy = [0.95 + k * 0.33 for k in range(8)]
    hx = [xs[1] - 0.3, xs[1] + 0.3]
    for xx in hx:
        for yy in hy:
            s.circle(xx, yy + 0.45, 0.13, fill=PAPER, edge=INK, lw=1.6, z=4)
    s.text(xs[1], 0.95 + 8 * 0.33 + 0.55, 'Hidden layer: 16', size=17, weight='bold')
    # output: 10 circles
    oy = [0.55 + k * 0.33 for k in range(10)]
    for k, yy in enumerate(oy):
        s.circle(xs[2], yy + 0.18, 0.14, fill=GOLD if k == 3 else PAPER, edge=INK, lw=1.6, z=4)
        s.text(xs[2] + 0.45, yy + 0.18, str(k), size=15, ha='left', weight='bold' if k == 3 else 'normal')
    s.text(xs[2] - 0.1, 0.55 + 10 * 0.33 + 0.4, 'Output layer: 10', size=17, weight='bold')
    # a few connecting lines
    for yy in (gy + 0.3, gy + 1.0, gy + 1.7):
        for ty in (hy[1] + 0.45, hy[4] + 0.45, hy[7] + 0.45):
            s.line(gx + 8 * c, yy, hx[0] - 0.13, ty, color=HAIR, lw=0.9, z=1)
    for ty in (hy[1] + 0.45, hy[4] + 0.45, hy[7] + 0.45):
        for k in (1, 3, 6):
            s.line(hx[1] + 0.13, ty, xs[2] - 0.14, oy[k] + 0.18, color=HAIR, lw=0.9, z=1)
    s.text(3.9, 0.22, 'every hidden neuron has 64 weights and one bias', size=15, color=BODY)
    return s


# ------------------------------------------------------------------ 6. what the first layer looks for
@fig('x_t01_weights')
def x_t01_weights(w, h, **_):
    r = _res()
    w1 = r['w1_final']   # 64 x 16
    fav = r['json']['fav']          # (digit, how many of its 30 strongest images)
    order = [13, 8, 10, 16, 1, 4, 3, 9]
    cmap = LinearSegmentedColormap.from_list('kl', [RED, '#FFFFFF', INK])
    s = Scene(w, h)
    tile, gx, gy = 1.15, 0.15, 0.95
    x0, y0 = 0.1, 0.9
    for n, k1 in enumerate(order):
        k = k1 - 1
        row, col = divmod(n, 4)
        x = x0 + col * (tile + gx)
        y = y0 + (1 - row) * (tile + gy)
        t = w1[:, k].reshape(8, 8)
        m = np.abs(t).max()
        s.ax.imshow(t, cmap=cmap, vmin=-m, vmax=m, extent=(x, x + tile, y, y + tile), interpolation='nearest', zorder=2)
        s.rect(x, y, tile, tile, fill='none', edge=INK, lw=1.4, z=3)
        dg, c = fav[k]
        s.text(x + tile / 2, y - 0.3, f'fires for {dg}s', size=15, weight='bold')
        s.text(x + tile / 2, y - 0.62, f'{c} of 30', size=14, color=BODY)
    _frame(s)
    lx = 5.5
    s.text(lx, 4.45, '8 of the 16 neurons', size=15, weight='bold', ha='left')
    s.rect(lx, 3.5, 0.35, 0.35, fill=INK, edge=INK, lw=1)
    s.text(lx + 0.5, 3.67, 'ink adds', size=16, ha='left')
    s.rect(lx, 2.9, 0.35, 0.35, fill=RED, edge=RED, lw=1)
    s.text(lx + 0.5, 3.07, 'ink subtracts', size=16, ha='left')
    s.rect(lx, 2.3, 0.35, 0.35, fill=PAPER, edge=INK, lw=1)
    s.text(lx + 0.5, 2.47, 'ignored', size=16, ha='left')
    return s


# ------------------------------------------------------------------ 7. one image through the network
@fig('x_t01_forward')
def x_t01_forward(w, h, **_):
    r = _res()
    img = r['images'][int(r['img_i'])]
    hid, proba = r['hidden'], r['proba']
    s = Scene(w, h)
    base = 0.85
    _gray(s, img, 0.1, 1.6, 1.5)
    s.text(0.85, 3.35, 'the 3', size=16, weight='bold')
    s.arrow(1.75, 2.35, 2.2, 2.35, lw=2.2)
    # hidden bars
    hm = hid.max()
    bw = 0.17
    hx = 2.3
    s.text(hx + 8 * bw, 3.95, 'hidden layer: 16 neurons, how much each fired', size=15, weight='bold')
    for k, v in enumerate(hid):
        hgt = 2.4 * v / hm
        s.rect(hx + k * bw, base, bw - 0.03, max(hgt, 0.02), fill=GOLD if v > 2.4 else INK, edge=INK, lw=0.8, z=3)
    s.line(hx - 0.03, base, hx + 16 * bw, base, lw=1.5)
    s.text(hx + 8 * bw, base - 0.3, 'neuron 1 ... 16', size=15, color=BODY)
    s.arrow(hx + 16 * bw + 0.12, 2.35, 5.4, 2.35, lw=2.2)
    ox = 5.5
    ow = 0.205
    s.text(ox + 5 * ow, 3.95, '10 scores', size=15, weight='bold')
    for k, v in enumerate(proba):
        hgt = 2.4 * v
        s.rect(ox + k * ow, base, ow - 0.03, max(hgt, 0.02), fill=GOLD if k == int(proba.argmax()) else PAPER, edge=INK, lw=1.2, z=3)
        s.text(ox + k * ow + ow / 2 - 0.015, base - 0.3, str(k), size=15, weight='bold' if k == int(proba.argmax()) else 'normal')
    s.line(ox - 0.03, base, ox + 10 * ow, base, lw=1.5)
    s.text(ox + 3 * ow + ow / 2, base + 2.4 * proba[3] + 0.28, f'{proba[3] * 100:.0f}%', size=17, weight='bold', ha='center')
    s.text(ox + 5 * ow, 0.2, 'digit', size=15, color=BODY)
    return s


# ------------------------------------------------------------------ 8. training: accuracy rises with epochs
@fig('x_t01_learning')
def x_t01_learning(w, h, **_):
    r = _res()
    curve = r['json']['curve']
    s = Scene(w, h)
    ax0, ax1, ay0, ay1 = 1.05, 5.3, 0.95, h - 0.7
    s.line(ax0, ay0, ax1, ay0, lw=2)
    s.line(ax0, ay0, ax0, ay1, lw=2)
    n = len(curve)
    px = lambda i: ax0 + 0.3 + i * (ax1 - ax0 - 0.5) / (n - 1)
    py = lambda v: ay0 + v * (ay1 - ay0 - 0.15)
    for v in (0, 0.5, 1.0):
        s.line(ax0, py(v), ax1, py(v), color=HAIR, lw=0.8, z=0)
        s.text(ax0 - 0.1, py(v), f'{int(v * 100)}%', size=15, ha='right')
    s.ax.plot([px(i) for i in range(n)], [py(a) for _, a in curve], color=INK, lw=3, zorder=3)
    for i, (e, a) in enumerate(curve):
        s.circle(px(i), py(a), 0.09, fill=GOLD if i in (0, n - 1) else PAPER, edge=INK, lw=1.6, z=5)
        if e not in (2, 3):
            s.text(px(i), ay0 - 0.3, str(e), size=15)
    s.text(px(0) + 0.15, py(curve[0][1]) + 0.4, f'{curve[0][1] * 100:.0f}%', size=16, weight='bold', ha='left')
    s.text(px(n - 1) - 0.1, py(curve[-1][1]) + 0.4, f'{curve[-1][1] * 100:.0f}%', size=16, weight='bold', ha='right')
    s.text((ax0 + ax1) / 2 + 0.2, 0.2, 'epochs (full passes over the training images)', size=15, color=BODY)
    s.text(0.25, (ay0 + ay1) / 2, 'right on unseen images', size=15, color=BODY, rot=90)
    cmap = LinearSegmentedColormap.from_list('kl', [RED, '#FFFFFF', INK])
    k = 11
    for j, (key, lab) in enumerate((('w1_pass1', 'one neuron, 1 epoch'), ('w1_final', 'same, 200 epochs'))):
        t = r[key][:, k].reshape(8, 8)
        m = np.abs(t).max()
        y = 2.65 - j * 1.9
        s.ax.imshow(t, cmap=cmap, vmin=-m, vmax=m, extent=(5.95, 7.45, y, y + 1.5), interpolation='nearest', zorder=2)
        s.rect(5.95, y, 1.5, 1.5, fill='none', edge=INK, lw=1.4, z=3)
        s.text(6.7, y + 1.75 if j == 0 else y + 1.75, lab, size=14, weight='bold')
    _frame(s)
    return s


# ------------------------------------------------------------------ 9. recorded predictions
@fig('x_t01_gallery')
def x_t01_gallery(w, h, **_):
    r = _res()
    xte, yte, pred = r['xte'], r['yte'], r['pred']
    wrong = [i for i in range(len(yte)) if pred[i] != yte[i]]
    right = list(range(8))
    idx = right + wrong[:4]
    s = Scene(w, h)
    cols = 6
    cw = (w - 0.1) / cols
    rh = h / 2
    isz = 1.2
    for n, i in enumerate(idx):
        row, col = divmod(n, cols)
        cx = 0.05 + col * cw + cw / 2
        top = h - row * rh
        ok = pred[i] == yte[i]
        _gray(s, xte[i].reshape(8, 8), cx - isz / 2, top - 0.1 - isz, isz, frame=False)
        s.rect(cx - isz / 2, top - 0.1 - isz, isz, isz, fill='none', edge=INK if ok else RED, lw=2 if ok else 4, z=4)
        s.text(cx, top - 0.1 - isz - 0.3, f'true {yte[i]}, said {pred[i]}', size=16, weight='normal' if ok else 'bold', color=INK if ok else RED)
    _frame(s)
    return s


# ------------------------------------------------------------------ 10. fragility: shift the picture
@fig('x_t01_shift')
def x_t01_shift(w, h, **_):
    r = _res()
    img = r['images'][int(r['img_i'])]
    acc = r['json']['shift']
    s = Scene(w, h)
    sz = 1.8
    for k in range(3):
        a = np.zeros_like(img)
        a[:, k:] = img[:, :8 - k]
        x = 0.35 + k * 2.5
        _gray(s, a, x, 1.9, sz)
        s.text(x + sz / 2, 4.3, ['original', 'moved 1 pixel', 'moved 2 pixels'][k], size=16, weight='bold')
        s.text(x + sz / 2, 1.3, f'{acc[str(k)] * 100:.0f}% right', size=22, weight='bold', color=INK if k == 0 else RED)
        if k < 2:
            s.arrow(x + sz + 0.15, 2.8, x + 2.5 - 0.15, 2.8, lw=2)
    s.text(w / 2, 0.5, 'Accuracy on all 450 unseen test images, shifted the same way', size=15, color=BODY)
    return s


# ------------------------------------------------------------------ 11. hand-made versus learned features
@fig('x_t01_handlearned')
def x_t01_handlearned(w, h, **_):
    r = _res()
    s = Scene(w, h)
    img = r['images'][int(r['img_i'])]
    rows = [(h * 0.74, 'A person chooses what to measure', 'person', 'total ink and\nink in the centre', 'one line on\nthe centre ink', 'Easy to explain', GOLD),
            (h * 0.26, 'The network finds what to measure', 'robot', '16 neurons, with\nweights from training', '10 scores,\nthe biggest wins', 'Hard to explain', PAPER)]
    for y, head, ic, mid, out, note, fill in rows:
        s.text(0.1, y + 0.78, head, size=17, weight='bold', ha='left')
        _gray(s, img, 0.1, y - 0.45, 0.9)
        s.arrow(1.15, y, 1.75, y)
        s.box(1.85, y - 0.5, 2.5, 1.0, mid, size=15, fill=fill)
        s.arrow(4.45, y, 5.05, y)
        s.box(5.15, y - 0.5, 2.1, 1.0, out, size=15)
        s.text(6.2, y - 0.8, note, size=15, color=BODY)
    s.line(0.1, h / 2, w - 0.1, h / 2, color=HAIR, lw=1.2)
    _frame(s)
    return s


# ================================================================== peek inside a neuron (concept-flow additions, 6 November 2026)
_P = {}


def _peek():
    if not _P:
        z = np.load(RUN / 'neuron_peek.npz')
        _P.update({k: z[k] for k in z.files})
    return _P


# ------------------------------------------------------------------ 4b. a neuron, opened up on an everyday decision: carry an umbrella?
@fig('x_t01_neuron_toy')
def x_t01_neuron_toy(w, h, **_):
    s = Scene(w, h)
    names = [('Chance of rain: 70', 'x 0.1', '= 7.0'), ('Minutes outside: 30', 'x 0.05', '= 1.5')]
    ys = [2.75, 1.55]
    heads = [(1.4, 'inputs'), (3.55, 'weight'), (4.75, 'product'), (6.5, 'weighted sum'), (8.3, 'plus bias'), (10.0, 'activation'), (11.2, 'output')]
    for x, t in heads:
        s.text(x, 3.8, t, size=15, color=MUTE, weight='bold')
    for (nm, wt, pr), y in zip(names, ys):
        s.box(0.1, y - 0.3, 2.65, 0.6, nm, size=15, fill=GOLD, weight='bold')
        s.arrow(2.85, y, 3.1, y, lw=2)
        s.box(3.15, y - 0.28, 0.95, 0.56, wt, size=16, weight='bold')
        s.arrow(4.2, y, 4.4, y, lw=2)
        s.text(4.8, y, pr, size=19, weight='bold')
        s.line(5.2, y, 5.5, 2.15, color=BODY, lw=1.6, z=1)
    s.box(5.5, 1.5, 1.9, 1.3, 'w1x1 + w2x2\n7.0 + 1.5\n= 8.5', size=15, weight='bold')
    s.arrow(7.5, 2.15, 7.75, 2.15, lw=2.2)
    s.box(7.8, 1.5, 1.45, 1.3, 'bias b = -6\n8.5 - 6\n= 2.5', size=15, weight='bold')
    s.arrow(9.35, 2.15, 9.6, 2.15, lw=2.2)
    s.box(9.45, 1.5, 1.15, 1.3, 'Step:\nabove 0\nis 1', size=15, weight='bold')
    s.arrow(10.65, 2.15, 10.85, 2.15, lw=2.2)
    s.circle(11.25, 2.15, 0.34, fill=GOLD, edge=INK, lw=2.2, z=3)
    s.text(11.25, 2.15, '1', size=24, weight='bold', z=6)
    s.text(11.25, 1.5, 'carry it', size=14, weight='bold')
    s.text(w / 2, 1.02, 'z = w1x1 + w2x2 + b = 7.0 + 1.5 − 6 = 2.5        a = f(z) = step(2.5) = 1', size=17, weight='bold')
    s.text(w / 2, 0.62, 'A second day: 20% chance, 30 minutes: 2.0 + 1.5 - 6 = -2.5, below 0, so the output is 0: leave it at home.', size=14, color=BODY)
    s.text(w / 2, 0.22, 'Simplified: real neurons have many inputs. A step is the simplest activation function; ReLU and sigmoid come next.', size=14, color=MUTE)
    return s


# ------------------------------------------------------------------ 4c. a real neuron of the trained digit network, opened up
@fig('x_t01_neuron_real')
def x_t01_neuron_real(w, h, **_):
    p = _peek()
    raw, x, W, b, total, out = p['raw'], p['x'], p['W'], p['b'], p['total'], p['out']
    s = Scene(w, h)
    top0 = [int(i) for i in p['top0']]
    sz = 2.3
    ix, iy = 0.1, 1.15
    _gray(s, raw.reshape(8, 8), ix, iy, sz)
    cell = sz / 8
    for lab, i in zip('ABC', top0):
        r, c = divmod(i, 8)
        px, py = ix + c * cell, iy + (7 - r) * cell
        s.rect(px, py, cell, cell, fill='none', edge=RED, lw=3, z=5)
        s.text(px + cell / 2, py + cell / 2, lab, size=14, weight='bold', color=PAPER, z=7)
    s.text(ix + sz / 2, iy + sz + 0.3, 'The 3: 64 inputs', size=16, weight='bold')
    s.text(ix + sz / 2, iy - 0.3, 'Neuron 1 looks at all 64', size=14, color=BODY)
    # the products, rounded so that the column adds up exactly
    k = 0
    prod = x * W[:, k]
    pr = [round(float(prod[i]), 2) for i in top0]
    tot_sum = round(float(prod.sum()), 2)
    rest = round(tot_sum - sum(pr), 2)
    rows = [['pixel', 'input', 'x  weight', '=  product']]
    for lab, i, q in zip('ABC', top0, pr):
        rows.append([lab, f'{x[i]:.2f}', f'x  {W[i, k]:.2f}', f'=  {q:.2f}'])
    rows.append(['61 more', '...', '...', f'=  {rest:.2f}'])
    s.table(2.95, 3.95, [0.95, 0.95, 1.35, 1.35], 0.5, rows, size=16, hl_rows=(), hl_cols=(3,), hl_fill=PAPER, align=['center'] * 4)
    s.text(2.95 + 2.3, 1.15, 'Simplified: the 3 biggest of 64 products are shown and\nthe other 61 are added in one lump. Input = ink / 16.', size=14, color=MUTE)
    # right: the chain
    bx, bw = 8.0, 3.8
    s.box(bx, 3.0, bw, 0.7, f'Weighted sum Σ wx of 64 inputs: {tot_sum:.2f}', size=15, weight='bold')
    s.arrow(bx + bw / 2, 3.0, bx + bw / 2, 2.78, lw=2)
    s.box(bx, 2.1, bw, 0.7, f'Add bias b = {b[k]:.2f}: z = {total[k]:.2f}', size=15, weight='bold')
    s.arrow(bx + bw / 2, 2.1, bx + bw / 2, 1.88, lw=2)
    s.box(bx, 1.2, bw, 0.7, f'a = ReLU(z) = max(0, z) = {out[k]:.2f}', size=15, weight='bold', fill=GOLD)
    s.text(bx + bw / 2, 3.95, 'Neuron 1, step by step', size=16, weight='bold')
    s.text(bx + bw / 2, 0.6, f'Neuron 2, same 3: z = {float(x @ W[:, 1]):.3f} + {b[1]:.3f} = {total[1]:.3f}.\nBelow 0, so a = max(0, z) = {out[1]:.0f}.', size=14, color=RED, weight='bold')
    return s


# ------------------------------------------------------------------ 4d. why the activation exists
@fig('x_t01_activation')
def x_t01_activation(w, h, **_):
    p = _peek()
    s = Scene(w, h)
    s.text(2.85, 3.95, 'Without an activation function', size=17, weight='bold')
    y = 2.75
    xs = [0.45, 2.95, 5.35]
    for xx, v in zip(xs, (5, 10, 30)):
        s.circle(xx, y, 0.32, fill=PAPER, edge=INK, lw=2, z=3)
        s.text(xx, y, str(v), size=19, weight='bold')
    for xx, t in ((1.7, 'Layer 1\nx 2'), (4.15, 'Layer 2\nx 3')):
        s.box(xx - 0.55, y - 0.4, 1.1, 0.8, t, size=15, weight='bold')
    for a, b_ in ((0.8, 1.1), (2.3, 2.58), (3.3, 3.58), (4.78, 5.0)):
        s.arrow(a, y, b_, y, lw=2, head=13)
    s.text(2.85, 1.85, 'Two layers, one after the other', size=15, color=BODY)
    s.box(1.0, 0.85, 3.7, 0.7, 'Same as ONE layer: x 6.   5 x 6 = 30', size=16, fill=GOLD, weight='bold')
    s.text(2.85, 0.4, 'Stacking gives nothing new.', size=15, color=RED, weight='bold')
    s.line(6.0, 0.3, 6.0, 3.9, color=HAIR, lw=1.4)
    # ReLU graph
    gx0, gx1, gy0, gy1 = 7.0, 11.6, 0.95, 3.5
    xlo, xhi, ylo, yhi = -2.0, 5.0, -0.0, 5.0
    px = lambda v: gx0 + (v - xlo) / (xhi - xlo) * (gx1 - gx0)
    py = lambda v: gy0 + (v - ylo) / (yhi - ylo) * (gy1 - gy0)
    s.text(9.3, 3.95, 'With ReLU: a bend', size=17, weight='bold')
    s.line(gx0, gy0, gx1, gy0, lw=2)
    s.line(px(0), gy0, px(0), gy1 + 0.1, lw=2)
    s.text(9.3, 0.4, 'total before the activation function', size=14, color=MUTE)
    s.text(6.65, 2.2, 'output', size=14, color=MUTE, rot=90)
    s.line(px(xlo), py(0), px(0), py(0), color=INK, lw=4, z=3)
    s.line(px(0), py(0), px(5), py(5), color=INK, lw=4, z=3)
    t1, o1 = float(p['total'][0]), float(p['out'][0])
    t2, o2 = float(p['total'][1]), float(p['out'][1])
    s.circle(px(t1), py(o1), 0.13, fill=GOLD, edge=INK, lw=2, z=6)
    s.text(px(t1) - 0.15, py(o1) + 0.28, f'neuron 1: {t1:.2f} stays {o1:.2f}', size=14, weight='bold', ha='right')
    s.circle(px(t2), py(o2), 0.13, fill=RED, edge=INK, lw=2, z=6)
    s.text(px(t2) - 0.55, py(o2) + 0.6, f'neuron 2: {t2:.2f}\nbecomes 0', size=14, weight='bold', color=RED, ha='center')
    return s


# ------------------------------------------------------------------ 4e. from neuron to layer: a table of weights
@fig('x_t01_layer_table')
def x_t01_layer_table(w, h, **_):
    p = _peek()
    x, W, b, out = p['x'], p['W'], p['b'], p['out']
    cols_px = [int(i) for i in p['top0']]       # pixels A, B, C
    s = Scene(w, h)
    f = lambda v: f'{v:.2f}'
    rows = [['', 'weight on A', 'weight on B', 'weight on C', '61 more', 'bias', 'output'],
            ['The 3: input'] + [f(x[i]) for i in cols_px] + ['...', '', '']]
    for k in (0, 1, 2):
        rows.append([f'Neuron {k + 1}'] + [f(W[i, k]) for i in cols_px] + ['...', f(b[k]), f(out[k])])
    rows.append(['...', '', '', '', '', '', ''])
    rows.append(['Neuron 16'] + [f(W[i, 15]) for i in cols_px] + ['...', f(b[15]), f(out[15])])
    cw = [1.55, 1.3, 1.3, 1.3, 1.1, 0.9, 1.0]
    s.table(0.1, 4.2, cw, 0.5, rows, size=15, hl_rows=(2,), hl_cols=(), hl_fill=GOLD, dim_rows=(5,), align=['center'] * 7)
    tx = 9.0
    s.text(tx, 3.85, '16 rows = 16 neurons', size=17, weight='bold', ha='left')
    s.text(tx, 3.3, 'Each row: 64 weights\nand one bias.', size=15, ha='left', color=BODY)
    s.text(tx, 2.7, 'a = f(Wx + b)', size=22, ha='left', weight='bold')
    s.text(tx, 1.95, 'W: 16 rows x 64 columns\nx: the 64 inputs\nb: 16 biases, f: ReLU,\na: the 16 outputs', size=14, ha='left', color=BODY)
    s.text(tx, 1.0, '64 x 16 = 1,024 weights\n+ 16 biases', size=15, ha='left', color=BODY)
    s.text(tx, 0.4, 'Gold row: neuron 1 from the\nlast slide, output 4.58.', size=14, ha='left', color=MUTE)
    return s


# ------------------------------------------------------------------ 4f. how one weight learns: the training loop on a single parameter
@fig('x_t01_one_weight')
def x_t01_one_weight(w, h, **_):
    s = Scene(w, h)
    bw, gap = 2.7, 0.26
    boxes = [('1  Prediction', 'input 2 x weight 0.5\n= prediction 1.0'),
             ('2  Loss', 'target 3, so error 2.0\nloss = 1/2 x 2.0\u00b2 = 2.0'),
             ('3  Gradient step', 'gradient = -4\nw = 0.5 − 0.1 x (−4)\n= 0.9'),
             ('4  Repeat', 'new prediction 1.8\nerror 1.2, loss 0.72')]
    for i, (hd, tx) in enumerate(boxes):
        x0 = 0.1 + i * (bw + gap)
        s.box(x0, 2.45, bw, 1.55, '', fill=GOLD if i == 2 else PAPER, lw=2)
        s.text(x0 + bw / 2, 3.7, hd, size=16, weight='bold')
        s.text(x0 + bw / 2, 3.0, tx, size=14, color=INK)
        if i < 3:
            s.arrow(x0 + bw + 0.02, 3.22, x0 + bw + gap - 0.02, 3.22, lw=2, head=12)
    rows = [['Round', '0', '1', '2', '3'],
            ['Weight', '0.5', '0.9', '1.14', '1.284'],
            ['Prediction', '1.0', '1.8', '2.28', '2.568'],
            ['Loss', '2.0', '0.72', '0.26', '0.09']]
    s.table(0.1, 2.2, [1.5, 1.2, 1.2, 1.2, 1.2], 0.45, rows, size=16, hl_rows=(3,), hl_fill=GOLD, align=['center'] * 5)
    s.text(8.35, 1.8, 'Gradient descent: repeated\nsmall steps against the\ngradient.', size=15, weight='bold', ha='left')
    s.text(8.35, 0.95, 'Backpropagation: finds the\ngradient for every weight.', size=15, ha='left', color=BODY)
    s.text(8.35, 0.3, '0.1 = learning rate η (step size)', size=14, ha='left', color=MUTE)
    return s


# ------------------------------------------------------------------ 4g. the formulas behind one learning step, with the slide's numbers
@fig('x_t01_formulas')
def x_t01_formulas(w, h, **_):
    s = Scene(w, h)
    rows = [['Step', 'Standard formula', 'With the numbers of the toy'],
            ['Prediction', 'ŷ = w × x', '0.5 × 2 = 1.0'],
            ['Loss: squared error', 'L = ½ (y − ŷ)²', '½ × (3 − 1)² = 2.0'],
            ['Gradient', '∂L/∂w = −x (y − ŷ)', '−2 × (3 − 1) = −4'],
            ['Update: gradient descent', 'w ← w − η ∂L/∂w', '0.5 − 0.1 × (−4) = 0.9'],
            ['Backpropagation: chain rule', '∂L/∂w = ∂L/∂ŷ · ∂ŷ/∂z · ∂z/∂w', '(−2) × 1 × 2 = −4'],
            ['Many examples: MSE', 'MSE = (1/n) Σ (yᵢ − ŷᵢ)²', 'sold 230, 150, 300: (100+0+100)/3 = 66.7']]
    s.table(0.1, 4.25, [2.8, 4.0, 4.7], 0.46, rows, size=15, hl_rows=(4,), hl_fill=GOLD, align=['left'] * 3)
    s.text(0.1, 0.5, 'z = wx + b is the weighted sum. Here b = 0 and there is no activation, so \u0177 = z.\nThe \u00bd makes the gradient tidy: L = (y \u2212 \u0177)\u00b2 gives \u22128 and \u03b7 = 0.05 gives the same steps.', size=14, ha='left', color=MUTE)
    return s
