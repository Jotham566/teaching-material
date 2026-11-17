"""Figures for Class 2 (classification), drawn from the real reference numbers. Auto-imported by diagrams.py.

  confusion_c2  tp, fp, fn, tn, focus   a confusion matrix in the scikit-learn orientation (Actual down the side, Predicted across the top)
  imbalance     actual [0/1 ...]        the validation rows, and what the majority-class baseline (always says "no") gets right
  sigmoid       mark (score, prob)      the S-shaped curve that turns a score into a probability, with a straight line for contrast
  threshold     probs, actual, ths, rows  the validation probabilities on a 0 to 1 strip with the threshold lines
  roc_real      points, auc, marks      the real ROC steps (false positive rate against true positive rate)
  spread        values, mu, sd, mark    training values on a number line with the mean, one standard deviation each side, and the z-score scale
  logloss       marks                   log loss of one row against its probability, for an actual positive and an actual negative
  gd_curve      steps, marks            the mean training log loss falling over gradient-descent steps, with the weights written beside it
"""
import numpy as np

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, fig
import slidekit as K


# ------------------------------------------------------------------ confusion matrix with cohort words
@fig('x_confusion_c2')
def x_confusion_c2(w, h, tp=0, fp=0, fn=0, tn=0, focus=None, size=18, col_pos='Predicted\npositive', col_neg='Predicted\nnegative', row_pos='Actual\npositive', row_neg='Actual\nnegative',
                   subs=('predicted yes, was yes', 'predicted yes, was no', 'predicted no, was yes', 'predicted no, was no'), **_):
    """Standard scikit-learn orientation: rows are the Actual class (negative first), columns are the Predicted class (negative first).
    focus: None (gold on TP), 'precision' (gold on the Predicted positive column), 'recall' (gold on the Actual positive row)."""
    s = Scene(w, h)
    lw_, top = 1.6, 1.0
    cw = (w - lw_ - 0.1) / 2
    ch = (h - top - 0.1) / 2
    x0 = lw_
    s.text(x0 + cw / 2, h - 0.5, col_neg, size=size, weight='bold')
    s.text(x0 + cw * 1.5, h - 0.5, col_pos, size=size, weight='bold')
    s.text(lw_ / 2, 0.1 + ch * 1.5, row_neg, size=size, weight='bold')
    s.text(lw_ / 2, 0.1 + ch * 0.5, row_pos, size=size, weight='bold')
    # (column, row from the bottom, count, name, plain words): top row is Actual negative
    cells = [(0, 1, tn, 'True negative (TN)', subs[3]), (1, 1, fp, 'False positive (FP)', subs[1]),
             (0, 0, fn, 'False negative (FN)', subs[2]), (1, 0, tp, 'True positive (TP)', subs[0])]
    for cx, cy, n, nm, sub in cells:
        gold = (focus == 'precision' and cx == 1) or (focus == 'recall' and cy == 0) or (focus is None and nm.startswith('True positive'))
        x = x0 + cx * cw + 0.05
        y = 0.1 + cy * ch + 0.05
        s.box(x, y, cw - 0.1, ch - 0.1, '', fill=GOLD if gold else PAPER, edge=INK, lw=2.0, r=0.06)
        s.text(x + (cw - 0.1) / 2, y + (ch - 0.1) * 0.7, f'{n:,}', size=36, weight='bold')
        s.text(x + (cw - 0.1) / 2, y + (ch - 0.1) * 0.27, nm + '\n' + sub, size=size - 4, color=BODY)
    return s


# ------------------------------------------------------------------ the imbalance picture
@fig('x_imbalance')
def x_imbalance(w, h, actual=(), word='yes', size=17, **_):
    s = Scene(w, h)
    n = len(actual)
    side = min(0.46, (w - 0.2) / n - 0.05)
    step = (w - 0.2 - side) / (n - 1)
    n_yes = int(sum(actual))
    n_no = n - n_yes
    right = n_no

    def row(y, items, label, label_color=INK):
        s.text(0.1, y + side + 0.3, label, size=18, weight='bold', ha='left', color=label_color)
        for i, v in enumerate(items):
            x = 0.1 + i * step
            s.box(x, y, side, side, '', fill=GOLD if v == 1 else PAPER, edge=INK, lw=1.8, r=0.04)
            s.text(x + side / 2, y + side / 2, 'yes' if v == 1 else 'no', size=14, weight='bold' if v == 1 else 'normal', color=INK)
    row(h - 1.55, list(actual), f'Actual classes: {n_no} no, {n_yes} yes')
    wrong = [1 if v == 1 else 0 for v in actual]
    s.text(0.1, h - 2.8 + side + 0.3, 'Majority-class baseline: always says "no"', size=18, weight='bold', ha='left')
    for i, v in enumerate(actual):
        x = 0.1 + i * step
        s.box(x, h - 2.8, side, side, '', fill=RED if v == 1 else PAPER, edge=INK, lw=1.8, r=0.04)
        s.text(x + side / 2, h - 2.8 + side / 2, 'no', size=14, weight='bold', color=PAPER if v == 1 else INK)
    s.text(0.1, 1.55, f'Right on {right} of {n} rows. Accuracy {right / n:.2f}.', size=22, weight='bold', ha='left')
    s.text(0.1, 0.85, f'Red: the {n_yes} actual positives this baseline never finds.', size=18, ha='left', color=RED, weight='bold')
    s.text(0.1, 0.3, 'A high accuracy that finds no positive is useless.', size=18, ha='left', color=BODY)
    return s


# ------------------------------------------------------------------ sigmoid
@fig('x_sigmoid')
def x_sigmoid(w, h, mark=None, size=16, **_):
    s = Scene(w, h)
    x0, x1, y0, y1 = 1.05, w - 0.3, 0.75, h - 0.25
    zlo, zhi, plo, phi = -6.0, 6.0, -0.32, 1.32
    px = lambda z: x0 + (z - zlo) / (zhi - zlo) * (x1 - x0)
    py = lambda p: y0 + (p - plo) / (phi - plo) * (y1 - y0)
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    s.text((x0 + x1) / 2, 0.28, 'score s (a number built from the features)', size=size, color=MUTE)
    s.text(0.3, (y0 + y1) / 2, 'predicted probability (positive class)', size=size, color=MUTE, rot=90)
    for p in (0.0, 0.5, 1.0):
        s.text(x0 - 0.12, py(p), f'{p:g}', size=14, color=GREY, ha='right')
    for z in (-4, 0, 4):
        s.text(px(z), y0 - 0.22, f'{z}', size=14, color=GREY)
    for p in (0.0, 1.0):
        s.line(x0, py(p), x1, py(p), color=HAIR, lw=1.4, z=1)
    s.ax.plot([x0, x1], [py(0.5), py(0.5)], color=MUTE, lw=2, ls='--', zorder=2)
    zs = np.linspace(zlo, zhi, 200)
    s.ax.plot([px(z) for z in zs], [py(0.5 + 0.105 * z) for z in zs], color=RED, lw=2.4, ls=(0, (4, 3)), zorder=3)
    s.ax.plot([px(z) for z in zs], [py(1 / (1 + np.exp(-z))) for z in zs], color=INK, lw=3.8, zorder=4)
    s.text(px(-5.9), py(1.18), 'A linear function goes\nbelow 0 and above 1', size=size, color=RED, weight='bold', ha='left')
    s.text(px(1.4), py(0.0), 'The sigmoid (logistic)\nfunction stays\nbetween 0 and 1', size=size, weight='bold', ha='left')
    s.text(px(-3.0), py(0.5) + 0.22, 'decision threshold 0.5', size=size, color=MUTE, weight='bold', ha='center')
    s.text(px(-3.4), py(0.4), 'below: negative (no)', size=size, color=BODY, ha='center')
    s.text(px(3.4), py(0.6), 'above: positive (yes)', size=size, color=BODY, ha='center')
    if mark:
        z, p = mark
        s.circle(px(z), py(p), 0.13, fill=GOLD, edge=INK, lw=2, z=6)
        where = 'below 0.5' if p < 0.5 else 'above 0.5'
        s.text(px(z) + 0.25, py(p) - 0.45, f'row 3: s = {z:.2f}\np = {p:.2f} ({where})', size=size, ha='left', weight='bold')
    return s


# ------------------------------------------------------------------ threshold strip
@fig('x_threshold')
def x_threshold(w, h, probs=(), actual=(), ths=(), rows=(), size=16, **_):
    s = Scene(w, h)
    x0, x1 = 0.6, w - 0.5
    ax_y = 2.55
    px = lambda p: x0 + p * (x1 - x0)
    s.line(x0, ax_y, x1, ax_y, color=INK, lw=2)
    for p in (0, 0.25, 0.5, 0.75, 1):
        s.line(px(p), ax_y, px(p), ax_y - 0.08, color=INK, lw=1.4)
        s.text(px(p), ax_y - 0.28, f'{p:g}', size=14, color=GREY)
    s.text((x0 + x1) / 2, ax_y - 0.62, 'predicted probability of the positive class (yes)', size=size, color=MUTE)
    order = np.argsort(probs, kind='stable')
    binw = 0.045
    stacks = {}
    pos = {}
    for i in order:
        b = int(probs[i] / binw)
        k = stacks.get(b, 0)
        stacks[b] = k + 1
        pos[i] = (b, k)
    tall = max(stacks.values())
    r = min(0.12, (h - ax_y - 1.0) / (2 * tall + 1) / 1.0)
    r = max(r, 0.06)
    for i in range(len(probs)):
        b, k = pos[i]
        cx = px(min(1.0, (b + 0.5) * binw)) if stacks[b] > 1 else px(probs[i])
        cy = ax_y + 0.05 + r + k * (2 * r + 0.02)
        s.circle(cx, cy, r, fill=GOLD if actual[i] == 1 else PAPER, edge=INK, lw=1.6, z=5)
        near = [t_ for t_ in ths if abs(probs[i] - t_) < 0.012]
        if near:
            s.text(cx, cy + 0.38, f'p = {probs[i]:.3f}', size=14, weight='bold', color=INK, z=7, bbox=dict(fc='white', ec='none', pad=1.5))
    for th in ths:
        s.line(px(th), ax_y, px(th), h - 0.8, color=RED if abs(th - 0.5) < 1e-9 else MUTE, lw=2.4, dash=True, z=3)
        s.text(px(th), h - 0.5, f'{th:g}', size=18, weight='bold', color=RED if abs(th - 0.5) < 1e-9 else INK)
    ly = ax_y - 0.95
    s.circle(0.75, ly, 0.11, fill=GOLD, edge=INK, lw=1.6)
    s.text(0.95, ly, 'actual positive', size=14, ha='left')
    s.circle(2.55, ly, 0.11, fill=PAPER, edge=INK, lw=1.6)
    s.text(2.75, ly, 'actual negative', size=14, ha='left')
    s.text(4.35, ly, 'Dashed: threshold, positive at or above', size=14, ha='left', color=BODY)
    for i, t in enumerate(rows):
        s.text(0.2, ly - 0.4 - i * 0.36, t, size=16, ha='left', weight='bold' if i == 1 else 'normal')
    return s


# ------------------------------------------------------------------ real ROC
@fig('x_roc_real')
def x_roc_real(w, h, points=(), auc=None, marks=(), size=16, **_):
    s = Scene(w, h)
    x0, x1, y0, y1 = 1.1, w - 0.35, 0.85, h - 0.3
    px = lambda u: x0 + u * (x1 - x0)
    py = lambda v: y0 + v * (y1 - y0)
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    s.text((x0 + x1) / 2, 0.28, 'false positive rate, FPR (share of actual negatives flagged positive)', size=size, color=MUTE)
    s.text(0.3, (y0 + y1) / 2, 'true positive rate, TPR = recall', size=size, color=MUTE, rot=90)
    for v in (0, 0.5, 1):
        s.text(x0 - 0.3, py(v), f'{v:g}', size=14, color=GREY, ha='right')
        s.text(px(v), y0 - 0.34, f'{v:g}', size=14, color=GREY)
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    s.ax.fill_between([px(u) for u in xs], [py(0)] * len(xs), [py(v) for v in ys], step=None, color=GOLD, alpha=0.4, zorder=1)
    s.ax.plot([px(0), px(1)], [py(0), py(1)], color=MUTE, lw=2, ls='--', zorder=2)
    s.ax.plot([px(u) for u in xs], [py(v) for v in ys], color=INK, lw=3.4, zorder=3, drawstyle='default')
    for u, v in zip(xs, ys):
        s.circle(px(u), py(v), 0.06, fill=INK, edge=INK, lw=1, z=4)
    for m in marks:
        s.circle(px(m['x']), py(m['y']), 0.13, fill=RED, edge=INK, lw=1.6, z=6)
        s.text(px(m['x']) + m.get('dx', 0.25), py(m['y']) + m.get('dy', 0.0), m['label'], size=size, ha='left', weight='bold', color=RED)
    s.text(px(0.76), py(0.36), 'Dashed line:\nrandom guessing,\nAUC 0.5', size=size, color=MUTE)
    if auc is not None:
        s.text(px(0.7), py(0.1), f'Gold area = AUC {auc:.2f}', size=size + 2, weight='bold')
    return s


# ------------------------------------------------------------------ illustrative smooth ROC
@fig('x_roc_smooth')
def x_roc_smooth(w, h, size=16, **_):
    """An invented smooth ROC curve, to show what many thresholds look like."""
    s = Scene(w, h)
    x0, x1, y0, y1 = 1.1, w - 0.35, 0.85, h - 0.3
    px = lambda u: x0 + u * (x1 - x0)
    py = lambda v: y0 + v * (y1 - y0)
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    s.text((x0 + x1) / 2, 0.28, 'false positive rate, FPR (share of actual negatives flagged positive)', size=size, color=MUTE)
    s.text(0.3, (y0 + y1) / 2, 'true positive rate, TPR = recall', size=size, color=MUTE, rot=90)
    for v in (0, 0.5, 1):
        s.text(x0 - 0.3, py(v), f'{v:g}', size=14, color=GREY, ha='right')
        s.text(px(v), y0 - 0.34, f'{v:g}', size=14, color=GREY)
    xs = np.linspace(0, 1, 200)
    ys = 1 - (1 - xs) ** 4
    s.ax.fill_between([px(u) for u in xs], [py(0)] * len(xs), [py(v) for v in ys], color=GOLD, alpha=0.4, zorder=1)
    s.ax.plot([px(0), px(1)], [py(0), py(1)], color=MUTE, lw=2, ls='--', zorder=2)
    s.ax.plot([px(u) for u in xs], [py(v) for v in ys], color=INK, lw=3.4, zorder=3)
    s.text(px(0.78), py(0.42), 'Dashed line:\nrandom guessing', size=size, color=MUTE)
    s.text(px(0.66), py(0.2), 'Gold area = AUC', size=size + 2, weight='bold')
    s.text(px(0.66), py(0.08), 'Illustrative curve', size=size, color=RED, weight='bold')
    return s


# ------------------------------------------------------------------ standard deviation on a number line
@fig('x_spread')
def x_spread(w, h, values=(), mu=0.0, sd=1.0, mark=None, name='load_pct', unit='%', size=16, **_):
    """Each training value is a dot on the raw axis. The mean is a red line, one standard deviation each side is a gold band.
    Under it, the same axis is labelled in z-scores (standard deviations from the mean)."""
    s = Scene(w, h)
    v = np.asarray(values, float)
    lo, hi = min(v.min(), mu - 2.2 * sd), max(v.max(), mu + 2.2 * sd)
    x0, x1 = 0.45, w - 0.35
    px = lambda u: x0 + (u - lo) / (hi - lo) * (x1 - x0)
    ax_y = 2.0
    top = h - 1.15
    s.rect(px(mu - sd), ax_y, px(mu + sd) - px(mu - sd), top - ax_y, fill=GOLD, edge=GOLD, lw=0.5, z=1)
    order = np.argsort(v, kind='stable')
    binw = (hi - lo) / 30
    stacks = {}
    r = 0.07
    for i in order:
        b = int((v[i] - lo) / binw)
        k = stacks.get(b, 0)
        stacks[b] = k + 1
        hl = mark is not None and i == mark
        cx = px(v[i]) if hl else px(lo + (b + 0.5) * binw)
        cy = ax_y + 0.1 + r + k * (2 * r + 0.012)
        s.circle(cx, cy, r * (1.5 if hl else 1), fill=RED if hl else PAPER, edge=INK, lw=1.2, z=6 if hl else 5)
    s.line(x0, ax_y, x1, ax_y, color=INK, lw=2)
    s.line(px(mu), ax_y, px(mu), top, color=RED, lw=2.6, z=3)
    s.text(px(mu), top + 0.2, f'mean {mu:.2f}', size=size, weight='bold', color=RED)
    s.arrow(px(mu), top - 0.3, px(mu + sd), top - 0.3, color=INK, lw=2, head=12, z=4)
    s.text((px(mu) + px(mu + sd)) / 2 + 0.1, top - 0.08, f'1 SD = {sd:.2f}', size=14, weight='bold', ha='left')
    s.text(x0, h - 0.3, f'Each dot is one training row of {name}.', size=14, ha='left', color=BODY)
    s.text(x0, h - 0.62, 'Gold band: within one standard deviation (SD) of the mean.', size=14, ha='left', color=BODY)
    for k in (-2, -1, 0, 1, 2):
        u = mu + k * sd
        s.line(px(u), ax_y, px(u), ax_y - 0.1, color=INK, lw=1.4)
        s.text(px(u), ax_y - 0.28, f'{u:.1f}', size=14, color=GREY)
        s.text(px(u), ax_y - 1.05, f'{k:+d}' if k else '0', size=16, weight='bold')
    s.text((x0 + x1) / 2, ax_y - 0.6, f'raw value of {name} ({unit})', size=14, color=MUTE)
    s.line(x0, ax_y - 1.3, x1, ax_y - 1.3, color=INK, lw=1.4)
    s.text((x0 + x1) / 2, ax_y - 1.6, 'the same axis as z-scores: standard deviations from the mean', size=14, color=MUTE)
    return s


# ------------------------------------------------------------------ log loss of one row
@fig('x_logloss')
def x_logloss(w, h, marks=(), size=16, **_):
    """Two curves: loss = -ln p for an actual positive (gold), and loss = -ln(1 - p) for an actual negative (black dashed). marks: dicts p, y, label."""
    s = Scene(w, h)
    x0, x1, y0, y1 = 1.0, w - 0.3, 0.8, h - 0.3
    lmax = 3.2
    px = lambda p: x0 + p * (x1 - x0)
    py = lambda l: y0 + min(l, lmax) / lmax * (y1 - y0)
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    s.text((x0 + x1) / 2, 0.28, 'predicted probability p of the positive class', size=size, color=MUTE)
    s.text(0.3, (y0 + y1) / 2, 'log loss of one row', size=size, color=MUTE, rot=90)
    for p in (0, 0.5, 1):
        s.text(px(p), y0 - 0.22, f'{p:g}', size=14, color=GREY)
    for l in (0, 1, 2, 3):
        s.text(x0 - 0.12, py(l), f'{l}', size=14, color=GREY, ha='right')
    ps = np.linspace(0.041, 0.999, 200)
    s.ax.plot([px(p) for p in ps], [py(-np.log(p)) for p in ps], color=GOLD, lw=4.2, zorder=4)
    s.ax.plot([px(1 - p) for p in ps], [py(-np.log(p)) for p in ps], color=INK, lw=3.0, ls=(0, (5, 3)), zorder=4)
    s.text(px(0.13), py(2.95), 'Gold: actual positive (y = 1)\nloss = -ln p', size=size, ha='left', weight='bold')
    s.text(px(0.73), py(1.75), 'Dashed: actual negative\n(y = 0): loss = -ln(1 - p)', size=size, ha='right', weight='bold')
    for m in marks:
        loss = -np.log(m['p']) if m['y'] == 1 else -np.log(1 - m['p'])
        s.circle(px(m['p']), py(loss), 0.13, fill=RED, edge=INK, lw=1.6, z=6)
        s.text(px(m['p']) + m.get('dx', 0.2), py(loss) + m.get('dy', 0.35), m['label'], size=size - 1, ha=m.get('ha', 'left'), weight='bold', color=RED)
    return s


# ------------------------------------------------------------------ gradient descent on the training log loss
@fig('x_gd_curve')
def x_gd_curve(w, h, steps=(), marks=(), size=16, **_):
    """steps: (step, mean training log loss) pairs; marks: dicts step, loss, label, dx, dy (label beside the point)."""
    s = Scene(w, h)
    x0, x1, y0, y1 = 1.0, w - 0.3, 0.8, h - 0.3
    smax = max(a for a, _ in steps)
    lmax = 0.75
    px = lambda k: x0 + k / smax * (x1 - x0)
    py = lambda l: y0 + l / lmax * (y1 - y0)
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    s.text((x0 + x1) / 2, 0.28, 'gradient-descent step (learning rate 0.5)', size=size, color=MUTE)
    s.text(0.3, (y0 + y1) / 2, 'training loss (mean log loss)', size=size, color=MUTE, rot=90)
    for k in (0, smax // 2, smax):
        s.text(px(k), y0 - 0.22, f'{k}', size=14, color=GREY)
    for l in (0, 0.25, 0.5, 0.75):
        s.text(x0 - 0.12, py(l), f'{l:g}', size=14, color=GREY, ha='right')
    s.ax.plot([px(a) for a, _ in steps], [py(b) for _, b in steps], color=INK, lw=3.6, zorder=4)
    for m in marks:
        s.circle(px(m['step']), py(m['loss']), 0.12, fill=GOLD, edge=INK, lw=1.6, z=6)
        s.text(px(m['step']) + m.get('dx', 0.2), py(m['loss']) + m.get('dy', 0.3), m['label'], size=size - 1, ha=m.get('ha', 'left'), weight='bold')
    return s
