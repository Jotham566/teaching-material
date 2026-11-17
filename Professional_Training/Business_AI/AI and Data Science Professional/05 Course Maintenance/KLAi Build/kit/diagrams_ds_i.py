"""Figure kinds for Sessions 17 and 18 (forests, boosting and overfitting; finding structure without labels), author letter i. Registered as x_<kind>, used as visual=dict(kind='<kind>', ...).

  ds_i_fitpanels   three small panels of one scatter (training and test points) with the fitted curve of a different flexibility in each, and the two errors
  ds_i_curves      lines against a ladder of settings (degree, depth, number of trees, k): training versus test, a marked best setting, zone labels, end-of-line labels
  ds_i_bootstrap   bagging: the training rows, three bootstrap samples (repeats in gold), one tree each, and the averaged prediction
  ds_i_boost       gradient boosting by hand: points, the prediction after each tree and the residuals
  ds_i_grid        a grid search: the cross-validated score of each combination, the best in gold, and the five fold scores of the best
  ds_i_hbars       horizontal bars (signed coefficients, or importances with a spread)
  ds_i_models      model comparison: cross-validated score with its spread, and the test score, per model
  ds_i_rfm         the orders of one customer turned into recency, frequency and monetary value
  ds_i_hist2       two histograms side by side (before and after a log transform)
  ds_i_moves       the four moves of k-means on ten real customers, panel by panel
  ds_i_segments    all customers on two axes, coloured by segment
  ds_i_pca         customers on the first two principal components, and the explained variance of each component
  ds_i_centroids   one small bar chart per segment: how far each segment sits from the average, in standard deviations
  ds_i_isodemo     random cuts isolate an odd customer in a few steps and a typical customer in many
All text is 14 pt or larger and every figure is audited for overlaps by figkit.
"""
import numpy as np
from matplotlib.patches import Rectangle

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, PALE, fig
import slidekit as K


def tw(t, size, kind='regular'):
    return K.width_in(str(t), size, kind)


def wrap_text(s, x, y, w, text, size, weight='normal', color=INK, ha='left', va='center', italic=False):
    lines = K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', w)
    s.text(x, y, '\n'.join(lines), size=size, weight=weight, color=color, ha=ha, va=va, italic=italic)
    return len(lines) * size * 1.15 / 72


def _clip(s, artist, x0, y0, x1, y1):
    r = Rectangle((x0, y0), x1 - x0, y1 - y0, transform=s.ax.transData, fc='none', ec='none')
    s.ax.add_patch(r)
    artist.set_clip_path(r)


def _spread(items, gap):
    """items: list of [y, key]; push apart so that neighbours are at least gap apart (keeps order). Returns dict key -> y."""
    it = sorted(items, key=lambda a: a[0])
    ys = [a[0] for a in it]
    for i in range(1, len(ys)):
        if ys[i] - ys[i - 1] < gap:
            ys[i] = ys[i - 1] + gap
    return {a[1]: y for a, y in zip(it, ys)}


STYLE = {'ink': dict(color=INK, lw=3.4), 'red': dict(color=RED, lw=3.4), 'gold': dict(color=GOLD, lw=4.0), 'mute': dict(color=MUTE, lw=2.6)}


# ------------------------------------------------------------------ lines against a ladder of settings
@fig('x_ds_i_curves')
def ds_i_curves(w, h, xs=(), series=(), xlabel='', ylabel='', ymin=0.0, ymax=1.0, ticks=(), fmt='{:.2f}', mark=None, mark_label='', zones=(), hline=None, size=16, right=1.9, notes=(), **_):
    s = Scene(w, h)
    zone_h = 0.62 if zones else 0.0
    x0, x1, y0, y1 = 1.35, w - right, 0.62 + zone_h + 0.3, h - 0.55
    px = lambda i: x0 + 0.3 + i * (x1 - x0 - 0.6) / max(len(xs) - 1, 1)
    py = lambda v: y0 + (v - ymin) / (ymax - ymin) * (y1 - y0)
    if mark is not None:
        bw = (px(1) - px(0)) * 0.8
        s.rect(px(mark) - bw / 2, y0, bw, y1 - y0, fill=GOLD, edge=GOLD, lw=0, z=0)
        s.text(px(mark), y1 + 0.27, mark_label, size=size, weight='bold')
    for t in ticks:
        s.line(x0, py(t), x1, py(t), color=HAIR, lw=0.9, z=0.5)
        s.text(x0 - 0.12, py(t), fmt.format(t), size=14, color=GREY, ha='right')
    if hline is not None:
        v, lab = hline
        s.line(x0, py(v), x1, py(v), color=MUTE, lw=2.0, dash=True, z=1)
        s.text(x0 + 0.1, py(v) + 0.2, lab, size=14, color=MUTE, ha='left')
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    for i, lab in enumerate(xs):
        s.text(px(i), y0 - 0.22, str(lab), size=14, color=GREY)
    s.text((x0 + x1) / 2, 0.2 if not zones else 0.2, xlabel, size=size, color=MUTE) if not zones else s.text((x0 + x1) / 2, y0 - 0.5, xlabel, size=size, color=MUTE)
    s.text(0.3, (y0 + y1) / 2, ylabel, size=size, color=MUTE, rot=90)
    ends = []
    for k, sr in enumerate(series):
        st = STYLE[sr.get('kind', 'ink')]
        pts = [(px(i), py(v)) for i, v in enumerate(sr['ys']) if v is not None]
        ln, = s.ax.plot([p[0] for p in pts], [p[1] for p in pts], color=st['color'], lw=st['lw'], zorder=4, solid_capstyle='round')
        _clip(s, ln, x0, y0, x1 + 0.3, y1)
        for p in pts:
            s.circle(p[0], p[1], 0.07, fill=st['color'], edge=st['color'], lw=1, z=5)
        ends.append([pts[-1][1], k])
    place = _spread(ends, 0.32)
    for k, sr in enumerate(series):
        st = STYLE[sr.get('kind', 'ink')]
        pts = [(px(i), py(v)) for i, v in enumerate(sr['ys']) if v is not None]
        s.text(pts[-1][0] + 0.2, place[k], sr['label'], size=size, weight='bold', color=st['color'] if sr.get('kind') != 'gold' else INK, ha='left')
    for (i, v, text, dx, dy) in notes:
        s.text(px(i) + dx, py(v) + dy, text, size=14, color=BODY, ha='left')
    if zones:
        yz = 0.55
        for (a, b, lab, col) in zones:
            s.line(px(a) - 0.2, yz + 0.3, px(b) + 0.2, yz + 0.3, color=col, lw=3.2)
            s.text((px(a) + px(b)) / 2, yz, lab, size=size, weight='bold', color=col)
    return s


# ------------------------------------------------------------------ three fitted curves on one scatter
@fig('x_ds_i_fitpanels')
def ds_i_fitpanels(w, h, panels=(), train=(), test=(), xlabel='', ylabel='', xr=(0, 1), yr=(0, 1), yticks=(), size=16, **_):
    s = Scene(w, h)
    n = len(panels)
    gap = 0.25
    left = 1.0
    pw = (w - left - 0.05 - gap * (n - 1)) / n
    top = h - 1.15
    bot = 1.55
    for k, p in enumerate(panels):
        x0 = left + k * (pw + gap)
        x1 = x0 + pw
        px = lambda v: x0 + 0.05 + (v - xr[0]) / (xr[1] - xr[0]) * (pw - 0.1)
        py = lambda v: bot + (v - yr[0]) / (yr[1] - yr[0]) * (top - bot)
        s.text(x0 + pw / 2, h - 0.25, p['title'], size=size + 1, weight='bold', color=p.get('color', INK))
        s.text(x0 + pw / 2, h - 0.62, p['sub'], size=15, color=BODY)
        s.rect(x0, bot, pw, top - bot, fill=PAPER, edge=INK, lw=1.4, z=0.5)
        for t in yticks:
            s.line(x0, py(t), x1, py(t), color=HAIR, lw=0.8, z=0.6)
            if k == 0:
                s.text(x0 - 0.1, py(t), str(t), size=14, color=GREY, ha='right')
        xs, ys = p['curve']
        ln, = s.ax.plot([px(v) for v in xs], [py(v) for v in ys], color=RED, lw=3.4, zorder=4)
        _clip(s, ln, x0, bot, x1, top)
        for (a, b) in train:
            s.circle(px(a), py(b), 0.075, fill=INK, edge=INK, lw=1, z=5)
        for (a, b) in test:
            s.circle(px(a), py(b), 0.075, fill=PAPER, edge=INK, lw=1.4, z=3)
        if p.get('off'):
            s.text(x0 + pw / 2, top - 0.3, p['off'], size=14, color=RED, weight='bold')
        for v in (xr[0], xr[1]):
            pass
        s.text(x0 + 0.05, bot - 0.22, f'{xr[0]:,.0f}', size=14, color=GREY, ha='left')
        s.text(x1 - 0.05, bot - 0.22, f'{xr[1]:,.0f}', size=14, color=GREY, ha='right')
    s.text(left + (w - left) / 2, bot - 0.52, xlabel, size=size, color=MUTE)
    s.text(0.3, (top + bot) / 2, ylabel, size=size, color=MUTE, rot=90)
    ly = 0.28
    s.circle(left + 0.15, ly, 0.075, fill=INK, edge=INK, z=5)
    s.text(left + 0.3, ly, 'training week', size=15, ha='left')
    s.circle(left + 2.15, ly, 0.075, fill=PAPER, edge=INK, lw=1.4, z=5)
    s.text(left + 2.3, ly, 'test week (held back)', size=15, ha='left')
    s.line(left + 4.9, ly, left + 5.3, ly, color=RED, lw=3.4)
    s.text(left + 5.4, ly, 'fitted curve', size=15, ha='left')
    return s


# ------------------------------------------------------------------ bagging
@fig('x_ds_i_bootstrap')
def ds_i_bootstrap(w, h, ids=(), samples=(), **_):
    s = Scene(w, h)
    cw, ch = 0.42, 0.4
    xs0 = 2.75
    s.text(0.1, h - 0.35, 'Training rows', size=16, weight='bold', ha='left')
    for i, v in enumerate(ids):
        s.box(xs0 + i * cw, h - 0.55, cw, ch, str(v), size=15, fill=PAPER, edge=INK, lw=1.4, r=0.02)
    ytop = h - 1.15
    rowh = (ytop - 0.15) / len(samples)
    ax_ = xs0 + len(ids) * cw + 0.3
    tx = ax_ + 0.6
    pw_, px_ = 2.05, w - 2.15
    for k, smp in enumerate(samples):
        yc = ytop - (k + 0.5) * rowh
        s.text(0.1, yc + 0.2, f'Bootstrap sample {k + 1}', size=16, weight='bold', ha='left')
        out = [v for v in ids if v not in smp]
        s.text(0.1, yc - 0.17, 'left out: ' + (', '.join(map(str, out)) if out else 'none'), size=14, color=MUTE, ha='left')
        for i, v in enumerate(smp):
            rep = smp.count(v) > 1
            s.box(xs0 + i * cw, yc - ch / 2, cw, ch, str(v), size=15, fill=GOLD if rep else PAPER, edge=INK, lw=1.4, r=0.02)
        s.arrow(ax_ - 0.15, yc, tx - 0.05, yc, color=INK, lw=2.0, head=14)
        s.box(tx, yc - 0.3, 1.25, 0.6, f'Tree {k + 1}', size=17, fill=INK, edge=INK, color=PAPER, weight='bold', r=0.06)
        s.arrow(tx + 1.3, yc, px_ - 0.05, h / 2 - 0.3 + (0 if True else 0) + (k - 1) * 0.28, color=INK, lw=2.0, head=14)
    s.box(px_, h / 2 - 1.05, pw_, 1.55, '', fill=GOLD, edge=INK, lw=1.8, r=0.06)
    s.text(px_ + pw_ / 2, h / 2 + 0.15, 'Average of\nthe trees', size=17, weight='bold')
    s.text(px_ + pw_ / 2, h / 2 - 0.6, 'one prediction', size=15)
    return s


# ------------------------------------------------------------------ boosting by hand
@fig('x_ds_i_boost')
def ds_i_boost(w, h, x=(), y=(), panels=(), xlabel='', ylabel='', yr=(0, 60), size=16, **_):
    s = Scene(w, h)
    n = len(panels)
    gap = 0.25
    left = 1.0
    pw = (w - left - 0.05 - gap * (n - 1)) / n
    top, bot = h - 1.1, 0.95
    xr = (min(x) - 60, max(x) + 60)
    for k, p in enumerate(panels):
        x0 = left + k * (pw + gap)
        px = lambda v: x0 + 0.05 + (v - xr[0]) / (xr[1] - xr[0]) * (pw - 0.1)
        py = lambda v: bot + (v - yr[0]) / (yr[1] - yr[0]) * (top - bot)
        s.text(x0 + pw / 2, h - 0.25, p['title'], size=size + 1, weight='bold')
        s.text(x0 + pw / 2, h - 0.65, p['sub'], size=15, color=BODY)
        s.rect(x0, bot, pw, top - bot, fill=PAPER, edge=INK, lw=1.4, z=0.5)
        for t in (20, 40, 60):
            s.line(x0, py(t), x0 + pw, py(t), color=HAIR, lw=0.8, z=0.6)
            if k == 0:
                s.text(x0 - 0.1, py(t), str(t), size=14, color=GREY, ha='right')
        # prediction as flat runs
        pred = p['pred']
        i = 0
        while i < len(pred):
            j = i
            while j + 1 < len(pred) and abs(pred[j + 1] - pred[i]) < 1e-9:
                j += 1
            a = px(x[i]) - (0.0 if i == 0 else (px(x[i]) - px(x[i - 1])) / 2) - (0.25 if i == 0 else 0)
            b = px(x[j]) + (0.0 if j == len(pred) - 1 else (px(x[j + 1]) - px(x[j])) / 2) + (0.25 if j == len(pred) - 1 else 0)
            s.line(a, py(pred[i]), b, py(pred[i]), color=RED, lw=3.4, z=4)
            i = j + 1
        for a, b, pr in zip(x, y, pred):
            s.line(px(a), py(b), px(a), py(pr), color=RED, lw=1.8, dash=True, z=3)
            s.circle(px(a), py(b), 0.085, fill=INK, edge=INK, lw=1, z=5)
        s.text(x0 + 0.05, bot - 0.22, f'{xr[0]:,.0f}', size=14, color=GREY, ha='left')
        s.text(x0 + pw - 0.05, bot - 0.22, f'{xr[1]:,.0f}', size=14, color=GREY, ha='right')
    s.text(left + (w - left) / 2, 0.28, xlabel, size=size, color=MUTE)
    s.text(0.3, (top + bot) / 2, ylabel, size=size, color=MUTE, rot=90)
    return s


# ------------------------------------------------------------------ grid search
@fig('x_ds_i_grid')
def ds_i_grid(w, h, row_title='', col_title='', rows=(), cols=(), values=(), best=(0, 0), folds=(), fold_mean=0.0, fold_sd=0.0, size=16, **_):
    s = Scene(w, h)
    cw, ch = 1.2, 0.7
    x0 = 1.75
    ytop = h - 1.45
    s.text(x0 + len(cols) * cw / 2, h - 0.3, col_title, size=size, weight='bold')
    for j, c in enumerate(cols):
        s.box(x0 + j * cw, ytop, cw, 0.5, str(c), size=16, fill=INK, edge=INK, color=PAPER, weight='bold', r=0.02)
    s.text(0.1, ytop - 0.2, row_title, size=size, weight='bold', ha='left') if False else None
    for i, r in enumerate(rows):
        yb = ytop - (i + 1) * ch
        s.box(0.1, yb, x0 - 0.1, ch, str(r), size=16, fill=INK, edge=INK, color=PAPER, weight='bold', r=0.02)
        for j in range(len(cols)):
            isb = (i, j) == tuple(best)
            s.box(x0 + j * cw, yb, cw, ch, f'{values[i][j]:.3f}', size=17, fill=GOLD if isb else PAPER, edge=INK, lw=2.4 if isb else 1.2, r=0.02, weight='bold' if isb else 'normal')
    s.text(0.1, h - 0.3, row_title, size=size, weight='bold', ha='left')
    s.text(0.1, 0.35, 'Each cell: mean AUC over 5 folds', size=15, color=MUTE, ha='left')
    # folds of the best
    fx = x0 + len(cols) * cw + 0.7
    fw = w - fx - 0.1
    s.text(fx + fw / 2, h - 0.3, 'The five folds of the best cell', size=size, weight='bold')
    lo, hi = 0.6, 0.85
    base, top = 0.95, h - 1.0
    bw = fw / (len(folds) * 1.5)
    for t in (0.6, 0.7, 0.8):
        yy = base + (t - lo) / (hi - lo) * (top - base)
        s.line(fx, yy, fx + fw, yy, color=HAIR, lw=0.9, z=0.5)
        s.text(fx - 0.08, yy, f'{t:.1f}', size=14, color=GREY, ha='right')
    for k, v in enumerate(folds):
        bx = fx + 0.15 + k * bw * 1.5
        s.rect(bx, base, bw, (v - lo) / (hi - lo) * (top - base), fill=GOLD, edge=INK, lw=1.4, z=2)
        s.text(bx + bw / 2, base - 0.22, f'{k + 1}', size=14, color=GREY)
    s.text(fx + fw / 2, base - 0.55, f'mean {fold_mean:.3f}, sd {fold_sd:.3f}', size=15, weight='bold')
    return s


# ------------------------------------------------------------------ horizontal bars
@fig('x_ds_i_hbars')
def ds_i_hbars(w, h, items=(), signed=False, fmt='{:+.2f}', xlabel='', pos_note='', neg_note='', size=16, vmax=None, label_w=3.2, **_):
    s = Scene(w, h)
    n = len(items)
    left = label_w
    right = w - 1.2
    top = h - 0.55
    bot = 0.95
    rh = (top - bot) / n
    vals = [it[1] for it in items]
    errs = [it[2] if len(it) > 2 and it[2] is not None else 0 for it in items]
    vm = vmax or max(abs(v) + e for v, e in zip(vals, errs))
    if signed:
        zero = (left + right) / 2
        sc = (right - left) / 2 / vm
    else:
        zero = left
        sc = (right - left) / vm
    s.line(zero, bot - 0.05, zero, top + 0.05, color=INK, lw=2)
    for i, it in enumerate(items):
        label, v = it[0], it[1]
        yc = top - (i + 0.5) * rh
        col = (RED if v > 0 else INK) if signed else INK
        bh = rh * 0.62
        s.rect(min(zero, zero + v * sc), yc - bh / 2, abs(v) * sc, bh, fill=col, edge=col, lw=1, z=2)
        if errs[i]:
            s.line(zero + (v - errs[i]) * sc, yc, zero + (v + errs[i]) * sc, yc, color=GOLD, lw=3.0, z=4)
        s.text(left - 0.15, yc, label, size=size, ha='right')
        tx = zero + v * sc + (0.12 if v >= 0 else -0.12) + (errs[i] * sc if v >= 0 else -errs[i] * sc)
        s.text(tx, yc, fmt.format(v), size=15, ha='left' if v >= 0 else 'right', weight='bold')
    s.text((left + right) / 2, 0.4, xlabel, size=size, color=MUTE)
    if signed:
        s.text(zero + 0.15, h - 0.25, pos_note, size=15, color=RED, weight='bold', ha='left')
        s.text(zero - 0.15, h - 0.25, neg_note, size=15, color=INK, weight='bold', ha='right')
    return s


# ------------------------------------------------------------------ model comparison
@fig('x_ds_i_models')
def ds_i_models(w, h, rows=(), lo=0.68, hi=0.80, band=None, size=16, **_):
    s = Scene(w, h)
    n = len(rows)
    left, right = 3.4, w - 0.4
    top, bot = h - 0.95, 1.05
    rh = (top - bot) / n
    px = lambda v: left + (v - lo) / (hi - lo) * (right - left)
    if band:
        s.rect(px(band[0]), bot - 0.1, px(band[1]) - px(band[0]), top - bot + 0.2, fill=PALE, edge=PALE, lw=0, z=0)
        s.text((px(band[0]) + px(band[1])) / 2, top + 0.45, band[2], size=15, color=MUTE, weight='bold')
    for t in np.arange(lo, hi + 1e-9, 0.02):
        s.line(px(t), bot - 0.1, px(t), top + 0.1, color=HAIR, lw=0.8, z=0.5)
        s.text(px(t), bot - 0.35, f'{t:.2f}', size=14, color=GREY)
    s.line(left, bot - 0.1, right, bot - 0.1, color=INK, lw=2)
    for i, r in enumerate(rows):
        yc = top - (i + 0.5) * rh
        s.text(left - 0.2, yc + 0.17, r['label'], size=size, weight='bold', ha='right')
        s.text(left - 0.2, yc - 0.17, r['note'], size=14, color=MUTE, ha='right')
        s.line(px(r['cv'] - r['sd']), yc + 0.12, px(r['cv'] + r['sd']), yc + 0.12, color=INK, lw=3.0, z=3)
        s.circle(px(r['cv']), yc + 0.12, 0.1, fill=INK, edge=INK, z=5)
        s.circle(px(r['test']), yc - 0.12, 0.1, fill=GOLD, edge=INK, lw=1.6, z=5)
    s.circle(0.3, 0.28, 0.09, fill=INK, edge=INK)
    s.text(0.5, 0.28, 'cross-validated AUC, ± 1 standard deviation', size=15, ha='left')
    s.circle(0.3, h - 0.2, 0.09, fill=GOLD, edge=INK, lw=1.6)
    s.text(0.5, h - 0.2, 'test AUC', size=15, ha='left')
    return s


# ------------------------------------------------------------------ RFM from one customer's orders
@fig('x_ds_i_rfm')
def ds_i_rfm(w, h, customer='', orders=(), total=0, last_date='', end_date='', r=0, f=0, m=0, size=16, **_):
    s = Scene(w, h)
    rh = 0.42
    cw = [1.9, 2.1]
    x0, ytop = 0.1, h - 0.85
    s.text(x0, h - 0.3, f'Orders of customer {customer}', size=16, weight='bold', ha='left')
    rows = [['order_date', 'order_value_ugx']] + [[a, f'{b:,}'] for a, b in orders]
    hl = {(len(rows) - 1, 0): GOLD}
    s.table(x0, ytop, cw, rh, rows, header=True, size=15, align=['left', 'right'], hl_cells={**{(0, c): PALE for c in (0, 1)}, **hl})
    yb = ytop - len(rows) * rh
    s.text(x0, yb - 0.3, f'(the last {len(orders)} of {total} orders)', size=14, color=MUTE, ha='left')
    cx = x0 + sum(cw) + 0.9
    cwid = w - cx - 0.05
    ch = (h - 0.6) / 3
    cards = [('R', 'Recency', f'{r} days', f'from the last order ({last_date}) to the last date in the file ({end_date})'),
             ('F', 'Frequency', f'{f} orders', f'how many orders the customer made'),
             ('M', 'Monetary value', f'{m:,} UGX', 'the total spent over all orders')]
    for k, (letter, head, big, small) in enumerate(cards):
        yt = h - 0.05 - k * (ch + 0.0)
        s.box(cx, yt - ch + 0.1, cwid, ch - 0.15, '', fill=PAPER, edge=INK, lw=1.8, r=0.06)
        s.box(cx + 0.12, yt - ch + 0.25, 0.6, 0.6, letter, size=22, fill=GOLD, edge=INK, lw=1.6, weight='bold', r=0.05)
        s.text(cx + 0.9, yt - 0.28, head, size=16, weight='bold', ha='left')
        s.text(cx + 0.9 + tw(head, 16, 'bold') + 0.25, yt - 0.28, big, size=20, weight='bold', ha='left', color=RED)
        wrap_text(s, cx + 0.9, yt - 0.68, cwid - 1.05, small, 14, color=BODY, va='center')
        s.arrow(x0 + sum(cw) + 0.1, ytop - (len(rows) - 1) * rh - rh / 2 + (k - 1) * 0.0, cx - 0.05, yt - ch / 2 + 0.03, color=MUTE, lw=1.6, head=12)
    return s


# ------------------------------------------------------------------ before and after a transform
@fig('x_ds_i_hist2')
def ds_i_hist2(w, h, panels=(), size=16, **_):
    s = Scene(w, h)
    n = len(panels)
    gap = 0.5
    left = 0.85
    pw = (w - left - 0.1 - gap * (n - 1)) / n
    top, bot = h - 1.05, 0.95
    for k, p in enumerate(panels):
        x0 = left + k * (pw + gap)
        cnt = np.array(p['counts'], float)
        mx = cnt.max()
        bw = pw / len(cnt)
        s.text(x0 + pw / 2, h - 0.25, p['title'], size=size + 1, weight='bold')
        s.text(x0 + pw / 2, h - 0.65, p['sub'], size=15, color=RED, weight='bold')
        for i, c in enumerate(cnt):
            hh = c / mx * (top - bot)
            s.rect(x0 + i * bw, bot, bw, hh, fill=GOLD if p.get('gold') else INK, edge=PAPER, lw=0.8, z=2)
        s.line(x0, bot, x0 + pw, bot, color=INK, lw=2)
        s.line(x0, bot, x0, top, color=INK, lw=2)
        for (frac, lab) in p['xticks']:
            s.text(x0 + frac * pw, bot - 0.22, lab, size=14, color=GREY)
        s.text(x0 + pw / 2, bot - 0.55, p['xlabel'], size=15, color=MUTE)
        if k == 0:
            s.text(0.3, (top + bot) / 2, 'number of customers', size=15, color=MUTE, rot=90)
    return s


# ------------------------------------------------------------------ the four moves of k-means
@fig('x_ds_i_moves')
def ds_i_moves(w, h, points=(), steps=(), titles=(), xlabel='', ylabel='', size=16, **_):
    s = Scene(w, h)
    n = len(steps)
    gap = 0.2
    left = 0.35
    pw = (w - left - 0.05 - gap * (n - 1)) / n
    top, bot = h - 1.2, 0.85
    P = np.array(points)
    xr = (P[:, 0].min() - 0.35, P[:, 0].max() + 0.35)
    yr = (P[:, 1].min() - 0.35, P[:, 1].max() + 0.35)
    for k, st in enumerate(steps):
        x0 = left + k * (pw + gap)
        px = lambda v: x0 + 0.05 + (v - xr[0]) / (xr[1] - xr[0]) * (pw - 0.1)
        py = lambda v: bot + (v - yr[0]) / (yr[1] - yr[0]) * (top - bot)
        s.text(x0 + pw / 2, h - 0.25, titles[k][0], size=size, weight='bold')
        s.text(x0 + pw / 2, h - 0.62, titles[k][1], size=14, color=BODY)
        s.rect(x0, bot, pw, top - bot, fill=PAPER, edge=INK, lw=1.4, z=0.5)
        C = st['centres']
        for i, (a, b) in enumerate(P):
            j = st['labels'][i]
            s.line(px(a), py(b), px(C[j][0]), py(C[j][1]), color=HAIR, lw=1.2, z=1)
        for i, (a, b) in enumerate(P):
            j = st['labels'][i]
            s.circle(px(a), py(b), 0.1, fill=INK if j == 0 else PAPER, edge=INK, lw=1.8, z=4)
        for j, c in enumerate(C):
            s.box(px(c[0]) - 0.14, py(c[1]) - 0.14, 0.28, 0.28, '', fill=GOLD, edge=RED, lw=2.6, r=0.02, z=6)
        if k > 0 and titles[k][2]:
            prevC = steps[k - 1]['centres']
            for j in range(2):
                s.arrow(px(prevC[j][0]), py(prevC[j][1]), px(C[j][0]), py(C[j][1]), color=RED, lw=2.0, head=12, z=5)
        s.text(x0 + pw / 2, bot - 0.27, f'inertia {st["inertia"]:.2f}', size=15, weight='bold')
    s.text(left + (w - left) / 2, 0.2, xlabel, size=15, color=MUTE)
    return s


# ------------------------------------------------------------------ all customers coloured by segment
SEG_STYLE = [dict(fc=INK, ec=INK), dict(fc=RED, ec=RED), dict(fc=GOLD, ec=INK), dict(fc=PAPER, ec=GREY)]


def _scatter_seg(s, X, Y, seg, px, py, size_pt=7):
    for k in range(4):
        idx = [i for i, g in enumerate(seg) if g == k]
        st = SEG_STYLE[k]
        s.ax.scatter([px(X[i]) for i in idx], [py(Y[i]) for i in idx], s=size_pt, c=st['fc'], edgecolors=st['ec'], linewidths=0.6, zorder=4, alpha=0.9)


@fig('x_ds_i_segments')
def ds_i_segments(w, h, x=(), y=(), seg=(), names=(), xticks=(), yticks=(), xlabel='', ylabel='', size=16, right=2.9, **_):
    s = Scene(w, h)
    x0, x1, y0, y1 = 1.55, w - right, 0.95, h - 0.15
    xr = (min(x) - 0.05, max(x) + 0.05)
    yr = (min(y) - 0.05, max(y) + 0.05)
    px = lambda v: x0 + (v - xr[0]) / (xr[1] - xr[0]) * (x1 - x0)
    py = lambda v: y0 + (v - yr[0]) / (yr[1] - yr[0]) * (y1 - y0)
    s.rect(x0, y0, x1 - x0, y1 - y0, fill=PAPER, edge=INK, lw=1.6, z=0.5)
    for v, lab in xticks:
        s.line(px(v), y0, px(v), y1, color=HAIR, lw=0.8, z=0.6)
        s.text(px(v), y0 - 0.22, lab, size=14, color=GREY)
    for v, lab in yticks:
        s.line(x0, py(v), x1, py(v), color=HAIR, lw=0.8, z=0.6)
        s.text(x0 - 0.1, py(v), lab, size=14, color=GREY, ha='right')
    _scatter_seg(s, x, y, seg, px, py)
    s.text((x0 + x1) / 2, 0.2, xlabel, size=size, color=MUTE)
    s.text(0.3, (y0 + y1) / 2, ylabel, size=size, color=MUTE, rot=90)
    ly = y1 - 0.3
    for k, nm in enumerate(names):
        st = SEG_STYLE[k]
        s.ax.scatter([x1 + 0.35], [ly], s=90, c=st['fc'], edgecolors=st['ec'], linewidths=1.4, zorder=6)
        wrap_text(s, x1 + 0.6, ly, right - 0.75, nm, 15, 'bold', va='center')
        ly -= 0.78
    return s


# ------------------------------------------------------------------ PCA
@fig('x_ds_i_pca')
def ds_i_pca(w, h, scores=(), seg=(), ratio=(), size=16, **_):
    s = Scene(w, h)
    sc = np.array(scores)
    x0, x1, y0, y1 = 1.0, w * 0.62, 0.95, h - 0.55
    xr = (sc[:, 0].min() - 0.2, sc[:, 0].max() + 0.2)
    yr = (sc[:, 1].min() - 0.2, sc[:, 1].max() + 0.2)
    px = lambda v: x0 + (v - xr[0]) / (xr[1] - xr[0]) * (x1 - x0)
    py = lambda v: y0 + (v - yr[0]) / (yr[1] - yr[0]) * (y1 - y0)
    s.rect(x0, y0, x1 - x0, y1 - y0, fill=PAPER, edge=INK, lw=1.6, z=0.5)
    s.line(px(0), y0, px(0), y1, color=HAIR, lw=0.9, z=0.6)
    s.line(x0, py(0), x1, py(0), color=HAIR, lw=0.9, z=0.6)
    _scatter_seg(s, sc[:, 0], sc[:, 1], seg, px, py)
    s.text((x0 + x1) / 2, 0.5, f'PC1 ({ratio[0] * 100:.0f}% of the variance)', size=15, color=MUTE)
    s.text(0.3, (y0 + y1) / 2, f'PC2 ({ratio[1] * 100:.0f}%)', size=15, color=MUTE, rot=90)
    s.text((x0 + x1) / 2, h - 0.25, 'Each dot is one customer', size=16, weight='bold')
    # explained variance bars
    bx0 = x1 + 0.9
    bw = (w - bx0 - 0.1) / 3
    base, top = 1.2, h - 1.0
    s.text(bx0 + 1.5 * bw, h - 0.25, 'Explained variance', size=16, weight='bold')
    cum = 0
    for k, r in enumerate(ratio):
        bxx = bx0 + k * bw
        hh = r / 0.7 * (top - base)
        s.rect(bxx + 0.08, base, bw - 0.16, hh, fill=GOLD if k < 2 else HAIR, edge=INK, lw=1.4, z=2)
        s.text(bxx + bw / 2, base + hh + 0.22, f'{r * 100:.0f}%', size=16, weight='bold')
        s.text(bxx + bw / 2, base - 0.25, f'PC{k + 1}', size=15, color=GREY)
        cum += r
    s.text(bx0 + 1.5 * bw, 0.3, f'PC1 and PC2 together: {sum(ratio[:2]) * 100:.0f}%', size=15, color=MUTE)
    return s


# ------------------------------------------------------------------ segment centres in standard deviations
@fig('x_ds_i_centroids')
def ds_i_centroids(w, h, names=(), vals=(), vars=('Recency', 'Frequency', 'Spend'), size=16, **_):
    s = Scene(w, h)
    n = len(names)
    gap = 0.2
    left = 0.1
    pw = (w - left - 0.05 - gap * (n - 1)) / n
    top, bot = h - 1.0, 0.7
    rh = (top - bot) / len(vars)
    vm = 2.6
    for k in range(n):
        x0 = left + k * (pw + gap)
        zero = x0 + pw / 2
        sc = (pw / 2 - 0.1) / vm
        wrap_text(s, x0 + pw / 2, h - 0.45, pw, names[k], 15, 'bold', ha='center')
        s.rect(x0, bot - 0.1, pw, top - bot + 0.2, fill=PAPER, edge=INK, lw=1.2, z=0.5)
        s.line(zero, bot - 0.1, zero, top + 0.1, color=INK, lw=1.6, z=1)
        for j, v in enumerate(vals[k]):
            yc = top - (j + 0.5) * rh
            col = RED if v > 0 else INK
            s.rect(min(zero, zero + v * sc), yc - 0.24, abs(v) * sc, 0.26, fill=col, edge=col, lw=1, z=2)
            s.text(x0 + 0.1, yc + 0.22, vars[j], size=14, color=BODY, ha='left')
            s.text(zero + v * sc + (0.08 if v >= 0 else -0.08), yc - 0.11, f'{v:+.1f}', size=14, weight='bold', ha='left' if v >= 0 else 'right')
    s.text((w) / 2, 0.22, 'Distance of the segment average from the average customer, in standard deviations (0 = average)', size=15, color=MUTE)
    return s


# ------------------------------------------------------------------ isolation by random cuts
@fig('x_ds_i_isodemo')
def ds_i_isodemo(w, h, points=(), panels=(), size=16, **_):
    s = Scene(w, h)
    n = len(panels)
    gap = 0.3
    left = 0.1
    pw = (w - left - 0.05 - gap * (n - 1)) / n
    top, bot = h - 1.3, 0.45
    P = np.array(points)
    xr = (P[:, 0].min() - 0.15, P[:, 0].max() + 0.15)
    yr = (P[:, 1].min() - 0.15, P[:, 1].max() + 0.15)
    for k, pn in enumerate(panels):
        x0 = left + k * (pw + gap)
        px = lambda v: x0 + (v - xr[0]) / (xr[1] - xr[0]) * pw
        py = lambda v: bot + (v - yr[0]) / (yr[1] - yr[0]) * (top - bot)
        s.text(x0 + pw / 2, h - 0.28, pn['title'], size=size + 1, weight='bold')
        s.text(x0 + pw / 2, h - 0.72, pn['sub'], size=15, color=BODY)
        s.text(x0 + pw / 2, h - 1.07, pn['sub2'], size=15, color=RED, weight='bold')
        s.rect(x0, bot, pw, top - bot, fill=PAPER, edge=INK, lw=1.4, z=0.5)
        for i, c in enumerate(pn['cuts']):
            lo, hi = c['lo'], c['hi']
            if c['axis'] == 0:
                xx = px(c['at']); s.line(xx, py(max(lo[1], yr[0])), xx, py(min(hi[1], yr[1])), color=RED, lw=2.2, z=3)
                s.text(xx + 0.1, py(min(hi[1], yr[1])) - 0.17, str(i + 1), size=14, weight='bold', color=RED, ha='left') if len(pn['cuts']) <= 4 else None
            else:
                yy = py(c['at']); s.line(px(max(lo[0], xr[0])), yy, px(min(hi[0], xr[1])), yy, color=RED, lw=2.2, z=3)
                s.text(px(max(lo[0], xr[0])) + 0.1, yy + 0.17, str(i + 1), size=14, weight='bold', color=RED, ha='left') if len(pn['cuts']) <= 4 else None
        for i, (a, b) in enumerate(P):
            if i in (pn['target'],):
                continue
            s.circle(px(a), py(b), 0.06, fill=INK, edge=INK, lw=1, z=4)
        a, b = P[pn['target']]
        s.circle(px(a), py(b), 0.16, fill=GOLD, edge=RED, lw=2.6, z=6)
    return s
