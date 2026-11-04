"""Figure kinds for Sessions 13 to 15 (probability, distributions and sampling, Bayes). Author E. Every name starts with e_.

Used as visual=dict(kind='e_pmf', ...) and so on (registered as x_e_pmf):
  e_grid       cells (rows of text), hl [[r, c]], row_label, col_label       the 36 outcomes of two dice
  e_pmf        labels, values, hl, mean_at, mean_label, value_texts, ...    a probability mass function as bars
  e_pdf        curve (uniform or normal), shade [{a, b, label}], ...        a density curve with shaded area
  e_cov        points, mx, my, labels                                       scatter with the mean lines and signs of the products
  e_corr       panels [{kind, caption}]                                     small scatter plots with their correlation
  e_softmax    words, panels [{title, probs, keep, sub}], logits            next-word probabilities as bars
  e_natfreq    root, mid, leaves                                            a tree of natural frequencies
  e_table2     row_labels, col_labels, counts, hl                           a 2 by 2 table of counts with totals
  e_lln        series [{ns, vals}], target                                  running means settling down
  e_hist       panels [{title, x, h, mu, sigma}]                            histograms in a row (central limit theorem)
  e_slices     words, probs, u                                              a bar cut into slices, and a random number landing in one
  e_gauss2d    points, mean, cov, labels                                    a two-dimensional Gaussian cloud with ellipses
"""
import math

import numpy as np
from matplotlib.patches import Ellipse

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, PALE, fig
import slidekit as K


def _lines_h(n, size):
    return n * size * 1.18 / 72


# ------------------------------------------------------------------ e_grid
@fig('x_e_grid')
def x_e_grid(w, h, cells=(), hl=(), row_label='Die 2', col_label='Die 1', size=18, head_fill=PALE, **_):
    s = Scene(w, h)
    nr, nc = len(cells), len(cells[0])
    left, top = 1.5, h - 0.7
    cw = min((w - left - 0.1) / nc, 1.0)
    ch = min((top - 0.1) / nr, 0.68)
    hs = {(a, b) for a, b in hl}
    s.text(left + nc * cw / 2, h - 0.25, col_label + ' (columns)', size=size, weight='bold', color=MUTE)
    s.text(0.1, top - nr * ch / 2, row_label + '\n(rows)', size=size, weight='bold', color=MUTE, ha='left')
    for c in range(nc):
        s.text(left + c * cw + cw / 2, top + 0.2, str(c + 1), size=size, weight='bold')
    for r in range(nr):
        s.text(left - 0.3, top - r * ch - ch / 2, str(r + 1), size=size, weight='bold')
        for c in range(nc):
            on = (r, c) in hs
            s.rect(left + c * cw, top - (r + 1) * ch, cw, ch, fill=GOLD if on else PAPER, edge=INK, lw=1.2)
            s.text(left + c * cw + cw / 2, top - r * ch - ch / 2, str(cells[r][c]), size=size, weight='bold' if on else 'normal', color=INK if on else BODY, z=5)
    return s


# ------------------------------------------------------------------ e_pmf
@fig('x_e_pmf')
def x_e_pmf(w, h, labels=(), values=(), hl=(), mean_at=None, mean_label='', value_texts=None, xlabel='', ylabel='probability', ymax=None, size=16,
            total_text='', value_size=14, **_):
    s = Scene(w, h)
    n = len(values)
    x0, x1 = 1.0, w - 0.2
    base = 1.05 if xlabel else 0.7
    if mean_at is not None:
        base += 0.2
    top = h - (0.6 if (total_text or mean_label) else 0.25)
    ym = ymax or max(values) * 1.18
    slot = (x1 - x0) / n
    bw = slot * 0.7
    py = lambda v: base + v / ym * (top - base)
    s.line(x0, base, x1, base, color=INK, lw=2)
    s.line(x0, base, x0, top, color=INK, lw=2)
    s.text(0.3, (base + top) / 2, ylabel, size=size, color=MUTE, rot=90)
    for i, v in enumerate(values):
        cx = x0 + (i + 0.5) * slot
        on = i in hl
        s.rect(cx - bw / 2, base, bw, py(v) - base, fill=GOLD if on else PAPER, edge=INK, lw=2, z=3)
        t = value_texts[i] if value_texts else f'{v:.3f}'.rstrip('0').rstrip('.')
        s.text(cx, py(v) + 0.17, t, size=value_size, weight='bold' if on else 'normal', color=INK)
        s.text(cx, base - (0.5 if mean_at is not None else 0.25), str(labels[i]), size=size)
    if xlabel:
        s.text((x0 + x1) / 2, 0.25, xlabel, size=size, color=MUTE)
    if mean_at is not None:
        mx = x0 + (mean_at + 0.5) * slot
        s.poly([(mx, base - 0.02), (mx - 0.14, base - 0.2), (mx + 0.14, base - 0.2)], fill=RED, edge=RED, lw=1, z=5)
        s.line(mx, base, mx, h - 0.45 if mean_label else top - 0.05, color=RED, lw=2, dash=True, z=4)
        if mean_label:
            s.text(mx + 0.12, h - 0.25, mean_label, size=size, color=RED, weight='bold', ha='left')
    if total_text:
        s.text(x1, h - 0.22, total_text, size=size, color=MUTE, ha='right', weight='bold')
    return s


# ------------------------------------------------------------------ e_pdf
def _curve(kind, x, mu=0.0, sigma=1.0, a=0.0, b=1.0):
    if kind == 'uniform':
        return np.where((x >= a) & (x <= b), 1.0 / (b - a), 0.0)
    return np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * math.sqrt(2 * math.pi))


@fig('x_e_pdf')
def x_e_pdf(w, h, curve='normal', lo=-4, hi=4, mu=0.0, sigma=1.0, a=0.0, b=1.0, shade=(), xticks=(), xlabel='', ylabel='density', notes=(), size=16,
            ymax=None, ytick_texts=(), **_):
    s = Scene(w, h)
    x0, x1 = 1.0, w - 0.3
    base, top = 0.95, h - 0.3
    xs = np.linspace(lo, hi, 600)
    ys = _curve(curve, xs, mu, sigma, a, b)
    ym = ymax or float(ys.max()) * 1.25
    px = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    py = lambda v: base + v / ym * (top - base)
    for sh in shade:
        m = (xs >= sh['a']) & (xs <= sh['b'])
        xx = np.concatenate([[sh['a']], xs[m], [sh['b']]])
        yy = np.concatenate([[_curve(curve, np.array(sh['a']), mu, sigma, a, b)], ys[m], [_curve(curve, np.array(sh['b']), mu, sigma, a, b)]])
        s.ax.fill_between([px(v) for v in xx], base, [py(v) for v in yy], color=sh.get('fill', GOLD), alpha=sh.get('alpha', 1.0), lw=0, zorder=2)
    s.ax.plot([px(v) for v in xs], [py(v) for v in ys], color=INK, lw=3, zorder=4)
    s.line(x0, base, x1, base, color=INK, lw=2, z=5)
    s.line(x0, base, x0, top, color=INK, lw=2, z=5)
    s.text(0.3, (base + top) / 2, ylabel, size=size, color=MUTE, rot=90)
    for v in xticks:
        s.line(px(v), base, px(v), base - 0.08, color=INK, lw=1.6)
        s.text(px(v), base - 0.3, f'{v:g}', size=max(14, size - 1))
    if xlabel:
        s.text((x0 + x1) / 2, 0.2, xlabel, size=size, color=MUTE)
    for i, t in enumerate(ytick_texts):
        yv, txt = t
        s.line(x0 - 0.08, py(yv), x0, py(yv), color=INK, lw=1.6)
        s.text(x0 - 0.12, py(yv), txt, size=14, ha='right')
    for nt in notes:
        s.text(px(nt['x']), py(nt['y']), nt['text'], size=nt.get('size', size), color=nt.get('color', INK), weight=nt.get('weight', 'bold'), ha=nt.get('ha', 'center'))
        if nt.get('to'):
            tx, ty = nt['to']
            s.arrow(px(nt['x']), py(nt['y']) - 0.15, px(tx), py(ty), color=nt.get('color', INK), lw=1.8, head=13)
    return s


# ------------------------------------------------------------------ e_cov
@fig('x_e_cov')
def x_e_cov(w, h, points=(), mx=0.0, my=0.0, xlabel='', ylabel='', size=16, labels=True, **_):
    s = Scene(w, h)
    x0, x1, y0, y1 = 1.15, w - 0.3, 0.95, h - 0.3
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    lox, hix = min(xs) - 0.8, max(xs) + 0.8
    loy, hiy = min(ys) - 0.8, max(ys) + 0.8
    px = lambda v: x0 + (v - lox) / (hix - lox) * (x1 - x0)
    py = lambda v: y0 + (v - loy) / (hiy - loy) * (y1 - y0)
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    s.text((x0 + x1) / 2, 0.28, xlabel, size=size, color=MUTE)
    s.text(0.3, (y0 + y1) / 2, ylabel, size=size, color=MUTE, rot=90)
    s.ax.fill_between([px(mx), x1], py(my), y1, color=GOLD, alpha=0.22, lw=0, zorder=1)
    s.ax.fill_between([x0, px(mx)], y0, py(my), color=GOLD, alpha=0.22, lw=0, zorder=1)
    s.line(px(mx), y0, px(mx), y1, color=RED, lw=2.2, dash=True, z=3)
    s.line(x0, py(my), x1, py(my), color=RED, lw=2.2, dash=True, z=3)
    s.text(px(mx) + 0.1, y0 + 0.2, f'mean x = {mx:g}', size=size, color=RED, weight='bold', ha='left')
    s.text(x1 - 0.1, py(my) + 0.22, f'mean y = {my:g}', size=size, color=RED, weight='bold', ha='right')
    for (x, y) in points:
        pos = (x - mx) * (y - my)
        s.circle(px(x), py(y), 0.11, fill=INK if pos > 0 else (PAPER if pos < 0 else GREY), edge=INK, lw=2, z=5)
    if labels:
        for sx, sy, sg in ((0.5, 0.65, '+'), (-0.5, -0.65, '+'), (-0.5, 0.65, '-'), (0.5, -0.65, '-')):
            s.text(px(mx + sx), py(my + sy), sg, size=30, weight='bold', color=MUTE)
    return s


# ------------------------------------------------------------------ e_corr
def corr_data(kind, n=40, seed=5):
    rng = np.random.default_rng(seed)
    x = rng.uniform(-1, 1, n) if kind == 'curve' else rng.normal(0, 1, n)
    e = rng.normal(0, 1, n)
    if kind == 'pos':
        y = 0.95 * x + 0.35 * e
    elif kind == 'neg':
        y = -0.95 * x + 0.35 * e
    elif kind == 'none':
        y = e
    else:
        y = x ** 2 + 0.03 * e
    return x, y


@fig('x_e_corr')
def x_e_corr(w, h, panels=(), size=16, **_):
    s = Scene(w, h)
    n = len(panels)
    gap = 0.3
    pw = (w - gap * (n - 1)) / n
    ph = h - 1.15
    for i, p in enumerate(panels):
        x, y = corr_data(p['kind'])
        r = float(np.corrcoef(x, y)[0, 1])
        ox = i * (pw + gap)
        s.rect(ox + 0.05, 1.1, pw - 0.1, ph - 0.05, fill=PAPER, edge=INK, lw=1.6)
        lx, hx, ly, hy = x.min() - 0.15, x.max() + 0.15, y.min() - 0.15, y.max() + 0.15
        for xi, yi in zip(x, y):
            s.circle(ox + 0.25 + (xi - lx) / (hx - lx) * (pw - 0.5), 1.3 + (yi - ly) / (hy - ly) * (ph - 0.45), 0.055, fill=INK, edge=INK, lw=0.5, z=4)
        s.text(ox + pw / 2, h - 0.27 if False else 0.78, f'r = {r:+.2f}', size=size + 2, weight='bold', color=RED)
        s.text(ox + pw / 2, 0.3, p.get('caption', ''), size=size, color=BODY)
    return s


# ------------------------------------------------------------------ e_softmax
@fig('x_e_softmax')
def x_e_softmax(w, h, words=(), panels=(), logits=None, size=17, label_w=1.35, arrow=True, **_):
    s = Scene(w, h)
    n = len(words)
    top = h - 1.1
    bottom = 0.85
    row = (top - bottom) / n
    x = 0.1
    for i, wd in enumerate(words):
        s.text(label_w, top - (i + 0.5) * row, wd, size=size, weight='bold', ha='right')
    x = label_w + 0.2
    if logits is not None:
        s.text(x + 0.45, h - 0.55, 'logit z', size=size, weight='bold', color=MUTE)
        for i, z in enumerate(logits):
            s.text(x + 0.45, top - (i + 0.5) * row, f'{z:g}', size=size)
        x += 1.15
        if arrow:
            s.text(x + 0.05, h - 0.55, 'softmax →', size=size, weight='bold', color=RED, ha='left')
            x += 1.55
        else:
            x += 0.3
    k = len(panels)
    gap = 0.3
    pw = (w - x - gap * (k - 1) - 0.1) / k
    vmax = max(max(p['probs']) for p in panels)
    for j, p in enumerate(panels):
        px0 = x + j * (pw + gap)
        s.text(px0 + pw / 2, h - 0.55, p['title'], size=size, weight='bold')
        s.line(px0, bottom, px0, top, color=INK, lw=1.8)
        bar_w = pw - 0.95
        for i, v in enumerate(p['probs']):
            keep = True if p.get('keep') is None else bool(p['keep'][i])
            yc = top - (i + 0.5) * row
            bw = max(0.03, bar_w * v / (vmax * 1.0))
            if keep:
                s.rect(px0, yc - row * 0.3, bw, row * 0.6, fill=GOLD if p.get('gold') else INK, edge=INK, lw=1.6, z=3)
            else:
                s.rect(px0, yc - row * 0.3, bw, row * 0.6, fill=PAPER, edge=GREY, lw=1.6, z=3)
            s.text(px0 + bw + 0.1, yc, f'{v:.3f}', size=max(14, size - 2), ha='left', color=INK if keep else GREY, weight='bold' if keep else 'normal')
        if p.get('sub'):
            s.text(px0 + pw / 2, 0.38, p['sub'], size=max(14, size - 1), color=MUTE)
    return s


# ------------------------------------------------------------------ e_natfreq
@fig('x_e_natfreq')
def x_e_natfreq(w, h, root='', mid=(), leaves=(), edges=(), size=17, **_):
    s = Scene(w, h)
    nmid = len(mid)
    nleaf = sum(len(l) for l in leaves)
    slot = (w - 0.2) / nleaf
    bw = slot - 0.2
    lh = 1.0
    ys = [h - 0.5, h / 2 + 0.05, 0.75]
    centers = []
    k = 0
    leaf_c = []
    for lv in leaves:
        cs = []
        for _ in lv:
            cs.append(0.1 + (k + 0.5) * slot)
            k += 1
        leaf_c.append(cs)
    mid_c = [sum(c) / len(c) for c in leaf_c]
    root_c = sum(mid_c) / len(mid_c)
    rw = min(3.6, max(K.width_in(root, size, 'bold') + 0.4, 2.4))
    s.box(root_c - rw / 2, ys[0] - 0.4, rw, 0.8, root, size=size, weight='bold', fill=PAPER, edge=INK, lw=2)
    for i, m in enumerate(mid):
        mw = min(max(K.width_in(m['text'], size, 'bold') + 0.4, 1.9), 4.4)
        s.box(mid_c[i] - mw / 2, ys[1] - 0.4, mw, 0.8, m['text'], size=size, weight='bold', fill=GOLD if m.get('hl') else PAPER, edge=INK, lw=2)
        s.line(root_c + (-0.3 if mid_c[i] < root_c else 0.3), ys[0] - 0.4, mid_c[i], ys[1] + 0.4, color=INK, lw=1.8)
        if edges:
            s.text((root_c + mid_c[i]) / 2 + (-0.65 if mid_c[i] < root_c else 0.65), (ys[0] + ys[1]) / 2 + 0.03, edges[0][i], size=max(14, size - 2), color=RED, weight='bold')
        for j, lf in enumerate(leaves[i]):
            cx = leaf_c[i][j]
            lines = K.wrap(lf['text'], size - 1, 'bold' if lf.get('hl') else 'regular', bw - 0.2)
            hh = max(0.8, len(lines) * (size - 1) * 1.2 / 72 + 0.3)
            s.box(cx - bw / 2, ys[2] - hh / 2, bw, hh, '\n'.join(lines), size=size - 1, weight='bold' if lf.get('hl') else 'normal', fill=GOLD if lf.get('hl') else PAPER, edge=INK, lw=1.8)
            s.line(mid_c[i] + (-0.2 if cx < mid_c[i] else 0.2), ys[1] - 0.4, cx, ys[2] + hh / 2, color=INK, lw=1.6)
            if edges:
                s.text((mid_c[i] + cx) / 2 + (-0.55 if cx < mid_c[i] else 0.55), (ys[1] + ys[2]) / 2 + 0.05, edges[1][i][j], size=max(14, size - 2), color=RED, weight='bold')
    return s


# ------------------------------------------------------------------ e_table2
@fig('x_e_table2')
def x_e_table2(w, h, row_labels=(), col_labels=(), counts=(), hl=(), hl_total=(), corner='', size=18, totals=True, **_):
    s = Scene(w, h)
    nr, nc = len(counts), len(counts[0])
    lw_ = 2.3
    cw = (w - lw_ - 0.1) / (nc + (1 if totals else 0))
    rh = min(0.9, (h - 0.1) / (nr + 1 + (1 if totals else 0)))
    top = h - 0.05
    hs = {tuple(x) for x in hl}
    ht = {tuple(x) if isinstance(x, (list, tuple)) else x for x in hl_total}
    colt = [sum(counts[r][c] for r in range(nr)) for c in range(nc)]
    rowt = [sum(counts[r]) for r in range(nr)]
    grand = sum(rowt)
    heads = list(col_labels) + (['Total'] if totals else [])
    for c, t in enumerate(heads):
        s.rect(lw_ + c * cw, top - rh, cw, rh, fill=PALE, edge=INK, lw=1.2)
        s.text(lw_ + c * cw + cw / 2, top - rh / 2, '\n'.join(K.wrap(t, size - 1, 'bold', cw - 0.15)), size=size - 1, weight='bold')
    if corner:
        s.text(0.1, top - rh / 2, corner, size=size - 1, color=MUTE, ha='left')
    rows = list(range(nr)) + ([None] if totals else [])
    for ri, r in enumerate(rows):
        y = top - (ri + 2) * rh
        lab = row_labels[r] if r is not None else 'Total'
        s.rect(0.05, y, lw_ - 0.05, rh, fill=PALE, edge=INK, lw=1.2)
        s.text(0.15, y + rh / 2, '\n'.join(K.wrap(lab, size - 1, 'bold', lw_ - 0.3)), size=size - 1, weight='bold', ha='left')
        for c in range(nc + (1 if totals else 0)):
            if r is None:
                v = colt[c] if c < nc else grand
                on = ('tot', 'col', c) in ht
            else:
                v = counts[r][c] if c < nc else rowt[r]
                on = ((r, c) in hs) if c < nc else (('tot', 'row', r) in ht)
            s.rect(lw_ + c * cw, y, cw, rh, fill=GOLD if on else PAPER, edge=INK, lw=1.2)
            s.text(lw_ + c * cw + cw / 2, y + rh / 2, f'{v:,}', size=size, weight='bold' if (on or r is None or c == nc) else 'normal', z=5)
    return s


# ------------------------------------------------------------------ e_lln
@fig('x_e_lln')
def x_e_lln(w, h, series=(), target=3.5, ylo=1.0, yhi=6.0, nmax=10000, size=16, target_label='true mean 3.5', **_):
    s = Scene(w, h)
    x0, x1, y0, y1 = 1.1, w - 0.3, 0.95, h - 0.25
    lx = lambda n: x0 + math.log10(n) / math.log10(nmax) * (x1 - x0)
    py = lambda v: y0 + (v - ylo) / (yhi - ylo) * (y1 - y0)
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    t = 1
    while t <= nmax:
        s.line(lx(t), y0, lx(t), y0 - 0.08, color=INK, lw=1.6)
        s.text(lx(t), y0 - 0.3, f'{t:,}', size=14)
        t *= 10
    s.text((x0 + x1) / 2, 0.2, 'number of rolls so far (log scale)', size=size, color=MUTE)
    s.text(0.3, (y0 + y1) / 2, 'average so far', size=size, color=MUTE, rot=90)
    for v in range(int(math.ceil(ylo)), int(yhi) + 1):
        s.text(x0 - 0.12, py(v), str(v), size=14, ha='right')
    s.ax.plot([x0, x1], [py(target)] * 2, color=RED, lw=2.4, ls='--', zorder=3)
    s.text(x1 - 0.05, py(target) + 0.25, target_label, size=size, color=RED, weight='bold', ha='right')
    for k, ser in enumerate(series):
        s.ax.plot([lx(n) for n in ser['ns']], [py(v) for v in ser['vals']], color=GOLD if k else INK, lw=3, zorder=5 - k, solid_joinstyle='round')
    return s


# ------------------------------------------------------------------ e_hist
@fig('x_e_hist')
def x_e_hist(w, h, panels=(), size=16, ymax=None, **_):
    s = Scene(w, h)
    n = len(panels)
    gap = 0.35
    pw = (w - gap * (n - 1) - 0.1) / n
    base, top = 0.8, h - 0.75
    for i, p in enumerate(panels):
        ox = 0.05 + i * (pw + gap)
        xs, hs = p['x'], p['h']
        lo, hi = p.get('lo', min(xs)), p.get('hi', max(xs))
        bwid = p['width']
        px = lambda v: ox + 0.1 + (v - lo) / (hi - lo) * (pw - 0.2)
        py = lambda v: base + v / (ymax or max(hs)) * (top - base - 0.1)
        s.text(ox + pw / 2, h - 0.3, p['title'], size=size, weight='bold')
        for xv, hv in zip(xs, hs):
            wpx = bwid / (hi - lo) * (pw - 0.2)
            s.rect(px(xv) - wpx / 2, base, wpx, py(hv) - base, fill=GOLD if p.get('gold') else PAPER, edge=INK, lw=0.6 if len(xs) > 30 else 1.2, z=3)
        s.line(ox, base, ox + pw, base, color=INK, lw=2, z=5)
        if p.get('mu') is not None and p.get('sigma'):
            gx = np.linspace(lo, hi, 200)
            gy = np.exp(-0.5 * ((gx - p['mu']) / p['sigma']) ** 2)
            sc = 1.0 / (p['sigma'] * math.sqrt(2 * math.pi))      # heights are densities, so the curve is the Gaussian pdf
            s.ax.plot([px(v) for v in gx], [py(sc * g) for g in gy], color=RED, lw=2.4, zorder=6)
        for v in p.get('ticks', (lo, hi)):
            s.text(px(v), base - 0.28, f'{v:g}', size=14)
    return s


# ------------------------------------------------------------------ e_slices
@fig('x_e_slices')
def x_e_slices(w, h, words=(), probs=(), u=None, size=17, **_):
    s = Scene(w, h)
    x0, x1 = 0.5, w - 0.5
    by, bh = h / 2 - 0.35, 0.8
    cum = np.cumsum(probs)
    fills = [INK, GOLD, PAPER, PALE, PAPER]
    xl = lambda v: x0 + v * (x1 - x0)
    prev = 0.0
    for i, (wd, p) in enumerate(zip(words, probs)):
        s.rect(xl(prev), by, xl(p + prev) - xl(prev), bh, fill=fills[i % 5], edge=INK, lw=2, z=3)
        mid = xl(prev + p / 2)
        wide = xl(p + prev) - xl(prev) > 1.4
        txt = f'{wd}\n{p:.3f}'
        if wide:
            s.text(mid, by + bh / 2, txt, size=size, weight='bold', color=PAPER if i == 0 else INK, z=6)
        else:
            lvl = 1 if i % 2 == 0 else 2
            ty = by + bh + 0.35 + (lvl - 1) * 0.72
            s.text(mid, ty, txt, size=size - 1, weight='bold')
            s.line(mid, ty - 0.33, mid, by + bh, color=GREY, lw=1.2)
        prev += p
    ticks = [0.0] + list(cum)
    for k, v in enumerate(ticks):
        if k + 1 < len(ticks) and ticks[k + 1] - v < 0.06:
            continue
        s.text(xl(v), by - 0.25, f'{v:.3f}'.rstrip('0').rstrip('.') if v != 0.0 else '0', size=14, color=MUTE)
    if u is not None:
        s.arrow(xl(u), by - 1.35, xl(u), by - 0.02, color=RED, lw=3, head=20)
        s.text(xl(u), by - 1.6, f'random number u = {u:g}', size=size, color=RED, weight='bold')
    return s


# ------------------------------------------------------------------ e_gauss2d
@fig('x_e_gauss2d')
def x_e_gauss2d(w, h, points=(), mean=(0, 0), cov=((1, 0), (0, 1)), xlabel='', ylabel='', size=16, axes_labels=True, xticks=(), yticks=(), mean_label='', **_):
    s = Scene(w, h)
    x0, x1, y0, y1 = 1.15, w - 0.3, 0.95, h - 0.3
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    lox, hix = min(xs) - 0.5, max(xs) + 0.5
    loy, hiy = min(ys) - 0.5, max(ys) + 0.5
    sc = min((x1 - x0) / (hix - lox), (y1 - y0) / (hiy - loy))
    cxm, cym = (x0 + x1) / 2, (y0 + y1) / 2
    mx_, my_ = (lox + hix) / 2, (loy + hiy) / 2
    px = lambda v: cxm + (v - mx_) * sc
    py = lambda v: cym + (v - my_) * sc
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    s.text((x0 + x1) / 2, 0.28, xlabel, size=size, color=MUTE)
    s.text(0.3, (y0 + y1) / 2, ylabel, size=size, color=MUTE, rot=90)
    c = np.array(cov, dtype=float)
    ev, evec = np.linalg.eigh(c)
    ang = math.degrees(math.atan2(evec[1, 1], evec[0, 1]))
    for k, (r, fillc) in enumerate(((2, GOLD), (1, GOLD))):
        e = Ellipse((px(mean[0]), py(mean[1])), 2 * r * math.sqrt(ev[1]) * sc, 2 * r * math.sqrt(ev[0]) * sc, angle=ang, fc=fillc, ec=INK, alpha=0.25 if k == 0 else 0.4, lw=2, zorder=1)
        s.ax.add_patch(e)
    for (x, y) in points:
        s.circle(px(x), py(y), 0.06, fill=INK, edge=INK, lw=0.5, z=4)
    for k in (1, 0):
        v = evec[:, k]
        L = 2 * math.sqrt(ev[k])
        s.arrow(px(mean[0]), py(mean[1]), px(mean[0] + v[0] * L), py(mean[1] + v[1] * L), color=RED, lw=3, head=18, z=6)
    s.circle(px(mean[0]), py(mean[1]), 0.09, fill=RED, edge=RED, z=7)
    for v in xticks:
        s.line(px(v), y0, px(v), y0 - 0.08, color=INK, lw=1.6)
        s.text(px(v), y0 - 0.3, f'{v:g}', size=14)
    for v in yticks:
        s.line(x0, py(v), x0 - 0.08, py(v), color=INK, lw=1.6)
        s.text(x0 - 0.12, py(v), f'{v:g}', size=14, ha='right')
    if mean_label:
        s.text(x0 + 0.15, y1 - 0.15, 'red dot = ' + mean_label, size=14, weight='bold', color=RED, ha='left', z=8)
    return s


# ------------------------------------------------------------------ e_ci
@fig('x_e_ci')
def x_e_ci(w, h, intervals=(), target=3.5, lo=2.5, hi=4.5, xlabel='', size=16, ticks=(), **_):
    s = Scene(w, h)
    x0, x1, y0, y1 = 0.9, w - 0.3, 0.95, h - 0.3
    px = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    n = len(intervals)
    ytop, ybot = y1 - 0.5, y0 + 0.2
    row = (ytop - ybot) / n
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    for v in ticks:
        s.line(px(v), y0, px(v), y0 - 0.08, color=INK, lw=1.6)
        s.text(px(v), y0 - 0.3, f'{v:g}', size=14)
    s.text((x0 + x1) / 2, 0.2, xlabel, size=size, color=MUTE)
    s.ax.plot([px(target)] * 2, [y0, y1 - 0.4], color=RED, lw=2.4, ls='--', zorder=2)
    s.text(px(target), y1 - 0.15, f'true mean {target:g}', size=size, color=RED, weight='bold')
    for i, (a, b, m) in enumerate(intervals):
        yc = ytop - (i + 0.5) * row
        miss = a > target or b < target
        col = RED if miss else INK
        s.line(px(a), yc, px(b), yc, color=col, lw=3.4, z=4)
        s.line(px(a), yc - 0.05, px(a), yc + 0.05, color=col, lw=2.6, z=4)
        s.line(px(b), yc - 0.05, px(b), yc + 0.05, color=col, lw=2.6, z=4)
        s.circle(px(m), yc, 0.045, fill=col, edge=col, lw=0.5, z=5)
    return s
