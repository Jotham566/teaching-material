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


# ------------------------------------------------------------------ 4. a neuron as a weighted checklist
@fig('x_t01_checklist')
def x_t01_checklist(w, h, inputs=(1, 1, 0), title='Payment A', threshold=4, **_):
    names = ['Amount over UGX 1,200,000', 'New payee', 'Outside office hours']
    wts = [3, 2, 1]
    s = Scene(w, h)
    s.text(0.1, h - 0.3, f'{title}: a risk checklist', size=18, weight='bold', ha='left')
    s.text(w - 1.7, h - 0.75, 'yes (1) or no (0) x weight', size=15, color=MUTE, ha='right')
    s.text(w - 0.15, h - 0.75, 'points', size=15, color=MUTE, ha='right')
    top = h - 0.95
    rh = 0.7
    pts = []
    for i, (nm, wt, v) in enumerate(zip(names, wts, inputs)):
        y = top - (i + 1) * rh
        s.box(0.1, y + 0.07, 0.55, 0.55, '', fill=GOLD if v else PAPER, lw=2, r=0.04)
        if v:
            s.line(0.2, y + 0.35, 0.33, y + 0.21, lw=3.4, z=5)
            s.line(0.33, y + 0.21, 0.56, y + 0.51, lw=3.4, z=5)
        s.text(0.85, y + 0.35, nm, size=18, ha='left', weight='bold' if v else 'normal', color=INK if v else MUTE)
        s.text(w - 1.7, y + 0.35, f'{v} x {wt}', size=18, ha='right', color=BODY)
        s.text(w - 0.15, y + 0.35, f'= {v * wt}', size=20, ha='right', weight='bold')
        s.line(0.1, y, w - 0.1, y, color=HAIR, lw=1)
        pts.append(v * wt)
    tot = sum(pts)
    y = top - 3 * rh - 0.3
    s.text(0.1, y + 0.1, f'Total score: {" + ".join(str(p) for p in pts)} = {tot}', size=21, weight='bold', ha='left')
    flag = tot >= threshold
    s.box(0.1, y - 1.0, w - 0.2, 0.7, f'{tot} is {"at least" if flag else "below"} {threshold}: ' + ('send to a person to check' if flag else 'let it through'),
          size=19, fill=GOLD if flag else PAPER, lw=2, weight='bold')
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
    s.text(xs[0], gy + 8 * c + 0.45, '64 numbers in', size=17, weight='bold')
    # hidden: 16 neurons (two columns of 8 drawn as 8 + 8)
    hy = [0.95 + k * 0.33 for k in range(8)]
    hx = [xs[1] - 0.3, xs[1] + 0.3]
    for xx in hx:
        for yy in hy:
            s.circle(xx, yy + 0.45, 0.13, fill=PAPER, edge=INK, lw=1.6, z=4)
    s.text(xs[1], 0.95 + 8 * 0.33 + 0.55, '16 neurons', size=17, weight='bold')
    # output: 10 circles
    oy = [0.55 + k * 0.33 for k in range(10)]
    for k, yy in enumerate(oy):
        s.circle(xs[2], yy + 0.18, 0.14, fill=GOLD if k == 3 else PAPER, edge=INK, lw=1.6, z=4)
        s.text(xs[2] + 0.45, yy + 0.18, str(k), size=15, ha='left', weight='bold' if k == 3 else 'normal')
    s.text(xs[2] + 0.3, 0.55 + 10 * 0.33 + 0.4, '10 scores out', size=17, weight='bold')
    # a few connecting lines
    for yy in (gy + 0.3, gy + 1.0, gy + 1.7):
        for ty in (hy[1] + 0.45, hy[4] + 0.45, hy[7] + 0.45):
            s.line(gx + 8 * c, yy, hx[0] - 0.13, ty, color=HAIR, lw=0.9, z=1)
    for ty in (hy[1] + 0.45, hy[4] + 0.45, hy[7] + 0.45):
        for k in (1, 3, 6):
            s.line(hx[1] + 0.13, ty, xs[2] - 0.14, oy[k] + 0.18, color=HAIR, lw=0.9, z=1)
    s.text(3.9, 0.22, 'every neuron has its own checklist of 64 weights', size=15, color=BODY)
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
    s.text(hx + 8 * bw, 3.95, '16 neurons: how much each fired', size=15, weight='bold')
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


# ------------------------------------------------------------------ 8. training: accuracy rises with passes
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
    s.text((ax0 + ax1) / 2 + 0.2, 0.2, 'passes over the training images', size=15, color=BODY)
    s.text(0.25, (ay0 + ay1) / 2, 'right on unseen images', size=15, color=BODY, rot=90)
    cmap = LinearSegmentedColormap.from_list('kl', [RED, '#FFFFFF', INK])
    k = 11
    for j, (key, lab) in enumerate((('w1_pass1', 'one neuron, 1 pass'), ('w1_final', 'same, 200 passes'))):
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
