"""Figure kinds for Sessions 15 and 16 (classification and judging a model), author letter h. Each is registered as x_<kind> and used as visual=dict(kind='<kind>', ...).
Every figure is drawn from numbers the session file computed from the real loans data; nothing here invents data.

  dsh_target        a real excerpt of the loans table with the target column in gold and braces for features and target
  dsh_sigmoid       the S-shaped sigmoid curve against a straight line, with one real loan marked
  dsh_onehot        text category values and the indicator (one-hot) columns that replace them
  dsh_tree          a decision tree drawn from the fitted tree: question, number of loans, default rate; leaves in gold when the default rate is high
  dsh_hist          predicted probabilities of two groups as bars, with the decision threshold as a dashed line
  dsh_confusion     the confusion matrix (Actual down the side, Predicted across the top) with an optional gold focus
  dsh_groupbars     small groups of vertical bars with values on top (accuracy against recall for several models)
  dsh_curve         one or more real curves (ROC, precision-recall, metrics against threshold, cost against threshold) with marks and a baseline
  dsh_leak_timeline a timeline that shows which columns exist when the model must decide and which appear only afterwards
  dsh_folds         stratified k-fold rounds with the number of loans and defaults in each fold and a score per round
  dsh_weights       class_weight='balanced': rows per class against the weight each row gets
All text is 14 pt or larger and every figure is audited for overlaps by figkit.
"""
import numpy as np
from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, PALE, fig
import slidekit as K


def tw(t, size, kind='regular'):
    return K.width_in(str(t), size, kind)


def _wrap(s, x, y, w, text, size, weight='normal', color=INK, ha='center', va='center'):
    lines = K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', w)
    s.text(x, y, '\n'.join(lines), size=size, weight=weight, color=color, ha=ha, va=va)
    return len(lines) * size * 1.15 / 72


def _axes(s, x0, x1, y0, y1, xlabel, ylabel, size=16, xticks=(), yticks=(), px=None, py=None, fmt=lambda v: f'{v:g}'):
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    s.text((x0 + x1) / 2, 0.26, xlabel, size=size, color=MUTE)
    s.text(0.27, (y0 + y1) / 2, ylabel, size=size, color=MUTE, rot=90)
    for v in xticks:
        s.line(px(v), y0, px(v), y0 - 0.07, color=INK, lw=1.4)
        s.text(px(v), y0 - 0.27, fmt(v), size=14, color=GREY)
    for v in yticks:
        s.text(x0 - 0.12, py(v), fmt(v), size=14, color=GREY, ha='right')
        s.line(x0, py(v), x1, py(v), color=HAIR, lw=1.0, z=0)


# ------------------------------------------------------------------ an excerpt with the target column
@fig('x_dsh_target')
def dsh_target(w, h, headers=(), rows=(), target=-1, positive='default = 1: the loan defaulted (positive class)', negative='default = 0: the loan was repaid (negative class)', size=15, **_):
    s = Scene(w, h)
    n = len(headers)
    target = target % n
    colw = [max([tw(headers[c], size, 'bold')] + [tw(r[c], size) for r in rows]) + 0.3 for c in range(n)]
    tot = sum(colw)
    if tot > w - 0.2:
        colw = [c * (w - 0.2) / tot for c in colw]
    rh = 0.46
    x0 = 0.1
    ytop = h - 0.2
    cells = {(0, c): PALE for c in range(n)}
    for r in range(len(rows) + 1):
        cells[(r, target)] = GOLD
    s.table(x0, ytop, colw, rh, [list(headers)] + [list(r) for r in rows], header=True, size=size, align=['left'] * n, hl_cells=cells)
    ybot = ytop - (len(rows) + 1) * rh
    xs = [x0 + sum(colw[:c]) for c in range(n + 1)]
    fx1 = xs[target] - 0.05
    s.brace(x0 + 0.05, fx1, ybot - 0.15, depth=0.18, up=True)
    s.text(x0 + 0.05, ybot - 0.62, 'features: the inputs,\nknown when the loan is approved', size=17, weight='bold', ha='left')
    s.brace(xs[target] + 0.05, xs[target + 1] - 0.05, ybot - 0.15, depth=0.18, up=True)
    s.text(xs[target + 1] - 0.05, ybot - 0.62, 'target (label):\nthe answer', size=17, weight='bold', color=RED, ha='right')
    s.text(x0, 0.95, positive, size=16, ha='left', weight='bold')
    s.text(x0, 0.45, negative, size=16, ha='left', color=BODY)
    return s


# ------------------------------------------------------------------ sigmoid
@fig('x_dsh_sigmoid')
def dsh_sigmoid(w, h, mark=None, size=16, **_):
    s = Scene(w, h)
    x0, x1, y0, y1 = 1.05, w - 0.3, 0.8, h - 0.25
    zlo, zhi, plo, phi = -6.0, 6.0, -0.32, 1.32
    px = lambda z: x0 + (z - zlo) / (zhi - zlo) * (x1 - x0)
    py = lambda p: y0 + (p - plo) / (phi - plo) * (y1 - y0)
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    s.text((x0 + x1) / 2, 0.26, 'score z (log-odds), built from the features', size=size, color=MUTE)
    s.text(0.27, (y0 + y1) / 2, 'predicted probability p', size=size, color=MUTE, rot=90)
    for p in (0.0, 0.5, 1.0):
        s.text(x0 - 0.12, py(p), f'{p:g}', size=14, color=GREY, ha='right')
    for z in (-4, 0, 4):
        s.text(px(z), y0 - 0.25, f'{z}', size=14, color=GREY)
    for p in (0.0, 1.0):
        s.line(x0, py(p), x1, py(p), color=HAIR, lw=1.4, z=1)
    s.ax.plot([x0, x1], [py(0.5), py(0.5)], color=MUTE, lw=2, ls='--', zorder=2)
    zs = np.linspace(zlo, zhi, 200)
    s.ax.plot([px(z) for z in zs], [py(0.5 + 0.105 * z) for z in zs], color=RED, lw=2.4, ls=(0, (4, 3)), zorder=3)
    s.ax.plot([px(z) for z in zs], [py(1 / (1 + np.exp(-z))) for z in zs], color=INK, lw=3.8, zorder=4)
    s.text(px(-5.9), py(1.17), 'A straight line goes below 0\nand above 1: not a probability', size=size, color=RED, weight='bold', ha='left')
    s.text(x1 - 0.05, py(0.1), 'The sigmoid (logistic) function\nstays between 0 and 1', size=size, weight='bold', ha='right')
    s.text(px(-5.9), py(0.58), 'p = 0.5', size=size, color=MUTE, weight='bold', ha='left')
    if mark:
        z, p, label = mark
        s.circle(px(z), py(p), 0.13, fill=GOLD, edge=INK, lw=2, z=6)
        s.text(px(z) + 0.25, py(p) + 0.35, label, size=size, ha='left', weight='bold')
    return s


# ------------------------------------------------------------------ one-hot encoding
@fig('x_dsh_onehot')
def dsh_onehot(w, h, headers=(), rows=(), new_headers=(), new_rows=(), hl=(), size=17, **_):
    """Left: one text variable. Right: one 0/1 column per category. hl: list of (row, col) cells holding the 1 for each record, shown in gold."""
    s = Scene(w, h)
    rh = 0.6
    lw_ = [max([tw(headers[0], size, 'bold')] + [tw(r[0], size) for r in rows]) + 0.3]
    nw = [max(tw(new_headers[c], size, 'bold'), max(tw(r[c], size) for r in new_rows)) + 0.3 for c in range(len(new_headers))]
    gap = 1.0
    scale = min(1.0, (w - 0.2 - gap) / (lw_[0] + sum(nw)))
    lw_ = [c * scale for c in lw_]
    nw = [c * scale for c in nw]
    ytop = h - 0.75
    s.text(0.1, h - 0.3, 'Before: text', size=17, weight='bold', ha='left')
    s.table(0.1, ytop, lw_, rh, [list(headers)] + [list(r) for r in rows], size=size, align=['left'], hl_cells={(0, 0): PALE})
    x2 = 0.1 + lw_[0] + gap
    s.arrow(0.1 + lw_[0] + 0.12, ytop - rh * (len(rows) + 1) / 2, x2 - 0.12, ytop - rh * (len(rows) + 1) / 2, lw=3, head=20)
    s.text(x2, h - 0.3, 'After: one 0 or 1 column per category', size=17, weight='bold', ha='left')
    cells = {(0, c): PALE for c in range(len(new_headers))}
    for r, c in hl:
        cells[(r + 1, c)] = GOLD
    s.table(x2, ytop, nw, rh, [list(new_headers)] + [list(r) for r in new_rows], size=size, align=['center'] * len(nw), hl_cells=cells)
    return s


# ------------------------------------------------------------------ decision tree drawn from a fitted tree
def _tdepth(n):
    return 0 if 'leaf' in n else 1 + max(_tdepth(n['yes']), _tdepth(n['no']))


def _tleaves(n):
    return 1 if 'leaf' in n else _tleaves(n['yes']) + _tleaves(n['no'])


@fig('x_dsh_tree')
def dsh_tree(w, h, node=None, size=15, **_):
    """node: {'q': 'burden <= 1.11', 'n': 5998, 'rate': 0.129, 'yes': node, 'no': node} or a leaf {'leaf': True, 'n':..., 'rate':...}.
    Each box shows the question (or the leaf probability), the number of loans that reach it and their default rate. yes = the answer to the question is yes."""
    s = Scene(w, h)
    d = _tdepth(node)
    nl = _tleaves(node)
    slot = (w - 0.2) / nl
    bh = 0.98
    top = h - 0.1 - bh
    ystep = (top - 0.15) / max(d, 1)
    ylev = lambda k: top - k * ystep   # bottom edge of a box at depth k

    def draw(nd, k, left):
        wd = _tleaves(nd) * slot
        cx = 0.1 + left + wd / 2
        bw = min(slot - 0.14, 2.5)
        yb = ylev(k)
        leaf = 'leaf' in nd
        rate = nd['rate']
        if leaf:
            s.box(cx - bw / 2, yb, bw, bh, '', fill=GOLD if rate >= 0.25 else PAPER, edge=INK, lw=2.2, r=0.06)
            s.text(cx, yb + bh * 0.76, f'p = {rate:.2f}', size=size + 3, weight='bold')
            s.text(cx, yb + bh * 0.30, f'{nd["n"]:,} loans\n{rate * 100:.1f}% defaulted', size=size - 1, color=BODY)
            return cx
        lc = draw(nd['yes'], k + 1, left)
        rc = draw(nd['no'], k + 1, left + _tleaves(nd['yes']) * slot)
        qw = min(max(tw(nd['q'], size, 'bold') + 0.3, 2.0), 3.4)
        s.box(cx - qw / 2, yb, qw, bh, '', fill=PAPER, edge=INK, lw=2.0, r=0.06)
        s.text(cx, yb + bh * 0.72, nd['q'], size=size, weight='bold')
        s.text(cx, yb + bh * 0.28, f'{nd["n"]:,} loans\n{rate * 100:.1f}% defaulted', size=size - 1, color=BODY)
        for c, lab in ((lc, 'yes'), (rc, 'no')):
            x_from = cx + (-0.35 if c < cx else 0.35)
            s.line(x_from, yb, c, ylev(k + 1) + bh, color=INK, lw=1.8)
            s.text((x_from + c) / 2 + (-0.25 if c < cx else 0.25), (yb + ylev(k + 1) + bh) / 2, lab, size=size, color=RED, weight='bold')
        return cx
    draw(node, 0, 0)
    return s


# ------------------------------------------------------------------ distribution of predicted probabilities for two groups
@fig('x_dsh_hist')
def dsh_hist(w, h, edges=(), a=(), b=(), a_label='', b_label='', threshold=None, size=16, **_):
    """a and b: share (0 to 1) of group A and group B in each bin; edges: bin edges. Bars are drawn side by side in each bin."""
    s = Scene(w, h)
    x0, x1, y0, y1 = 1.2, w - 0.3, 0.9, h - 0.35
    top = max(max(a), max(b)) * 1.12
    px = lambda v: x0 + (v - edges[0]) / (edges[-1] - edges[0]) * (x1 - x0)
    py = lambda v: y0 + v / top * (y1 - y0)
    yt = [t for t in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7) if t <= top]
    _axes(s, x0, x1, y0, y1, 'predicted probability of default', 'share of the loans in the group', size, xticks=[e for e in edges[::2]], yticks=yt, px=px, py=py)
    for i in range(len(a)):
        xl, xr = px(edges[i]), px(edges[i + 1])
        bw = (xr - xl) * 0.42
        s.rect(xl + (xr - xl) * 0.06, y0, bw, py(a[i]) - y0, fill=PAPER, edge=INK, lw=1.6, z=3)
        s.rect(xl + (xr - xl) * 0.06 + bw, y0, bw, py(b[i]) - y0, fill=GOLD, edge=INK, lw=1.6, z=3)
    if threshold is not None:
        s.line(px(threshold), y0, px(threshold), y1, color=RED, lw=2.6, dash=True, z=5)
        s.text(px(threshold) + 0.1, y1 - 0.02, f'threshold {threshold:g}', size=size, color=RED, weight='bold', ha='left')
    lx = x1 - 4.6
    s.rect(lx, y1 - 1.0, 0.3, 0.26, fill=PAPER, edge=INK, lw=1.6)
    s.text(lx + 0.42, y1 - 0.87, a_label, size=15, ha='left')
    s.rect(lx, y1 - 1.4, 0.3, 0.26, fill=GOLD, edge=INK, lw=1.6)
    s.text(lx + 0.42, y1 - 1.27, b_label, size=15, ha='left')
    return s


# ------------------------------------------------------------------ confusion matrix
@fig('x_dsh_confusion')
def dsh_confusion(w, h, tp=0, fp=0, fn=0, tn=0, focus=None, size=18, neg='repaid', pos='defaulted', **_):
    """scikit-learn orientation: rows are the Actual class (negative first), columns the Predicted class (negative first).
    focus: None (TP gold), 'precision' (gold on the predicted-positive column), 'recall' (gold on the actual-positive row), 'accuracy' (gold on TP and TN), 'none' (no gold)."""
    s = Scene(w, h)
    lw_, top = 1.9, 1.05
    cw = (w - lw_ - 0.1) / 2
    ch = (h - top - 0.1) / 2
    x0 = lw_
    s.text(x0 + cw / 2, h - 0.52, f'Predicted\nnegative ({neg})', size=size - 2, weight='bold')
    s.text(x0 + cw * 1.5, h - 0.52, f'Predicted\npositive ({pos})', size=size - 2, weight='bold')
    s.text(lw_ / 2, 0.1 + ch * 1.5, f'Actual\nnegative\n({neg})', size=size - 2, weight='bold')
    s.text(lw_ / 2, 0.1 + ch * 0.5, f'Actual\npositive\n({pos})', size=size - 2, weight='bold')
    cells = [(0, 1, tn, 'TN', 'true negative'), (1, 1, fp, 'FP', 'false positive'), (0, 0, fn, 'FN', 'false negative'), (1, 0, tp, 'TP', 'true positive')]
    for cx, cy, n, code, nm in cells:
        gold = ((focus is None and code == 'TP') or (focus == 'precision' and cx == 1) or (focus == 'recall' and cy == 0) or (focus == 'accuracy' and code in ('TP', 'TN')))
        x = x0 + cx * cw + 0.05
        y = 0.1 + cy * ch + 0.05
        s.box(x, y, cw - 0.1, ch - 0.1, '', fill=GOLD if gold else PAPER, edge=INK, lw=2.0, r=0.06)
        s.text(x + (cw - 0.1) / 2, y + (ch - 0.1) * 0.68, f'{n:,}', size=36, weight='bold')
        s.text(x + (cw - 0.1) / 2, y + (ch - 0.1) * 0.25, f'{code}: {nm}', size=size - 3, color=BODY)
    return s


# ------------------------------------------------------------------ grouped bars
@fig('x_dsh_groupbars')
def dsh_groupbars(w, h, groups=(), legend=(), size=17, ymax=1.0, **_):
    """groups: [{'label': ..., 'values': [v1, v2], 'texts': ['0.89', '0.17']}]; legend: names of the bars (gold = second)."""
    s = Scene(w, h)
    x0, x1, y0, y1 = 0.9, w - 0.2, 1.05, h - 0.6
    py = lambda v: y0 + v / ymax * (y1 - y0)
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    for v in (0, 0.5, 1.0):
        s.text(x0 - 0.12, py(v), f'{v:g}', size=14, color=GREY, ha='right')
        s.line(x0, py(v), x1, py(v), color=HAIR, lw=1.0, z=0)
    n = len(groups)
    gw = (x1 - x0) / n
    bw = min(0.85, gw * 0.32)
    for i, g in enumerate(groups):
        cx = x0 + gw * (i + 0.5)
        for j, (v, t) in enumerate(zip(g['values'], g['texts'])):
            bx = cx - bw - 0.04 + j * (bw + 0.08)
            s.rect(bx, y0, bw, max(py(v) - y0, 0.02), fill=GOLD if j else PAPER, edge=INK, lw=2.0, z=3)
            s.text(bx + bw / 2, py(v) + 0.2, t, size=size, weight='bold')
        _wrap(s, cx, y0 - 0.4, gw - 0.2, g['label'], size - 1, 'bold')
    lx = x0 + 0.2
    for j, name in enumerate(legend):
        s.rect(lx, h - 0.4, 0.3, 0.26, fill=GOLD if j else PAPER, edge=INK, lw=1.8)
        s.text(lx + 0.42, h - 0.27, name, size=16, ha='left')
        lx += 0.42 + tw(name, 16) + 0.45
    return s


# ------------------------------------------------------------------ curves
@fig('x_dsh_curve')
def dsh_curve(w, h, curves=(), xlabel='', ylabel='', baseline=None, baseline_label='', baseline_at=None, marks=(), area=None, area_label='', xlim=(0, 1), ylim=(0, 1), xticks=None,
              yticks=None, unit='', size=16, **_):
    """curves: [{'points': [(x, y)...], 'label': 'text', 'color': 'ink'|'red'|'mute', 'lx': x of the label, 'ly': y of the label, 'dash': bool}].
    baseline: 'diag' (a dashed diagonal) or a number (a dashed horizontal line); baseline_at: (x, y) of its label. marks: [{'x', 'y', 'label', 'dx', 'dy'}].
    area: index of the curve whose area is shaded gold; area_label is written at (xlim 66 per cent, ylim 14 per cent)."""
    s = Scene(w, h)
    x0, x1, y0, y1 = 1.25, w - 0.35, 0.85, h - 0.3
    px = lambda v: x0 + (v - xlim[0]) / (xlim[1] - xlim[0]) * (x1 - x0)
    py = lambda v: y0 + (v - ylim[0]) / (ylim[1] - ylim[0]) * (y1 - y0)
    xt = xticks or [xlim[0], (xlim[0] + xlim[1]) / 2, xlim[1]]
    yt = yticks or [ylim[0], (ylim[0] + ylim[1]) / 2, ylim[1]]
    _axes(s, x0, x1, y0, y1, xlabel, ylabel, size, xt, yt, px, py, fmt=lambda v: f'{v:g}{unit}')
    if area is not None:
        pts = curves[area]['points']
        s.ax.fill_between([px(p[0]) for p in pts], [py(ylim[0])] * len(pts), [py(p[1]) for p in pts], color=GOLD, alpha=0.4, zorder=1)
        if area_label:
            s.text(px(xlim[0] + 0.7 * (xlim[1] - xlim[0])), py(ylim[0] + 0.14 * (ylim[1] - ylim[0])), area_label, size=size + 1, weight='bold')
    if baseline == 'diag':
        s.ax.plot([px(0), px(1)], [py(0), py(1)], color=MUTE, lw=2, ls='--', zorder=2)
    elif baseline is not None:
        s.ax.plot([x0, x1], [py(baseline), py(baseline)], color=MUTE, lw=2, ls='--', zorder=2)
    if baseline_label and baseline_at:
        s.text(px(baseline_at[0]), py(baseline_at[1]), baseline_label, size=size, color=MUTE, weight='bold')
    cols = {'ink': INK, 'red': RED, 'mute': MUTE, 'gold': GOLD}
    for c in curves:
        pts = c['points']
        s.ax.plot([px(p[0]) for p in pts], [py(p[1]) for p in pts], color=cols[c.get('color', 'ink')], lw=3.4, zorder=4, ls='--' if c.get('dash') else '-')
        if c.get('label'):
            s.text(px(c['lx']), py(c['ly']), c['label'], size=size, weight='bold', color=cols[c.get('color', 'ink')] if c.get('color') != 'gold' else INK, ha=c.get('ha', 'left'))
    for m in marks:
        s.circle(px(m['x']), py(m['y']), 0.12, fill=m.get('fill', RED), edge=INK, lw=1.6, z=6)
        if m.get('label'):
            s.text(px(m['x']) + m.get('dx', 0.2), py(m['y']) + m.get('dy', -0.25), m['label'], size=size, ha=m.get('ha', 'left'), weight='bold', color=INK)
    return s


# ------------------------------------------------------------------ leakage timeline
@fig('x_dsh_leak_timeline')
def dsh_leak_timeline(w, h, events=(), decision=1, known='Known when the lender must decide', after='Recorded only afterwards', size=16, **_):
    """events: [{'when': 'title', 'what': 'variables recorded here'}]; events up to and including index `decision` are known at decision time."""
    s = Scene(w, h)
    n = len(events)
    seg = (w - 0.4) / n
    y = h * 0.5
    s.line(0.2, y, w - 0.2, y, color=INK, lw=3)
    for i, ev in enumerate(events):
        x = 0.2 + seg * (i + 0.5)
        late = i > decision
        s.circle(x, y, 0.15, fill=RED if late else GOLD, edge=INK, lw=2.4, z=4)
        _wrap(s, x, y + 0.7, seg - 0.25, ev['when'], size + 1, 'bold')
        _wrap(s, x, y - 0.75, seg - 0.25, ev['what'], size - 1, color=BODY)
    xcut = 0.2 + seg * (decision + 1)
    s.line(xcut, y - 1.45, xcut, y + 1.3, color=RED, lw=2.6, dash=True, z=5)
    s.brace(0.25, xcut - 0.1, h - 0.55, depth=0.16, up=False)
    s.text((0.25 + xcut - 0.1) / 2, h - 0.2, known, size=size + 1, weight='bold')
    s.brace(xcut + 0.1, w - 0.25, h - 0.55, depth=0.16, up=False)
    s.text((xcut + w - 0.25) / 2, h - 0.2, after, size=size + 1, weight='bold', color=RED)
    s.text(xcut, 0.25, 'The model must predict here', size=size, weight='bold', color=RED)
    return s


# ------------------------------------------------------------------ stratified k-fold
@fig('x_dsh_folds')
def dsh_folds(w, h, k=5, subs=(), scores=(), summary='', unit='AUC', size=16, **_):
    """k rounds; in round r fold r is the validation fold (gold) and the other folds train the model (black). subs: one line of text per fold (loans and defaults)."""
    s = Scene(w, h)
    lab_w = 1.2
    score_w = 1.3 if scores else 0.0
    gap = 0.06
    bw = (w - 0.1 - lab_w - score_w - gap * (k - 1)) / k
    top = h - 0.65
    s.box(lab_w + 0.05, h - 0.5, 0.45, 0.32, '', fill=INK, edge=INK, r=0.04)
    s.text(lab_w + 0.6, h - 0.34, 'Training folds', size=size, ha='left')
    s.box(lab_w + 2.4, h - 0.5, 0.45, 0.32, '', fill=GOLD, edge=INK, r=0.04)
    s.text(lab_w + 2.95, h - 0.34, 'Validation fold', size=size, ha='left')
    if scores:
        s.text(w - 0.05 - score_w / 2, h - 0.34, unit, size=size, weight='bold', color=MUTE)
    foot = 0.8 if summary else 0.1
    rh = (top - 0.1 - foot) / k
    for r in range(k):
        yy = top - (r + 1) * rh + 0.04
        s.text(0.05, yy + (rh - 0.08) / 2, f'Round {r + 1}', size=size, weight='bold', ha='left')
        for c in range(k):
            x = 0.05 + lab_w + c * (bw + gap)
            held = c == r
            s.box(x, yy, bw, rh - 0.1, '', fill=GOLD if held else INK, edge=INK, lw=1.6, r=0.04)
            s.text(x + bw / 2, yy + (rh - 0.1) / 2, subs[c], size=size - 2, color=INK if held else PAPER)
        if scores:
            s.text(w - 0.05 - score_w / 2, yy + (rh - 0.1) / 2, scores[r], size=size + 2, weight='bold', color=RED)
    if summary:
        s.text(w / 2, 0.4, summary, size=size + 2, weight='bold', color=RED)
    return s


# ------------------------------------------------------------------ class weights
@fig('x_dsh_weights')
def dsh_weights(w, h, repaid=0, defaulted=0, w_repaid=0.0, w_default=0.0, size=17, **_):
    """Rows per class, the weight each row gets, and the weighted rows. Paired bars: white = repaid (negative class), gold = defaulted (positive class)."""
    s = Scene(w, h)
    lab_w = 3.3
    x0 = lab_w + 0.2
    maxw = w - x0 - 1.3
    mx = max(repaid, defaulted, repaid * w_repaid, defaulted * w_default)
    rows = [('Rows in the training set', repaid, defaulted, f'{repaid:,}', f'{defaulted:,}'),
            ('Weight of each row,\nclass_weight="balanced"', None, None, f'{w_repaid:.2f}', f'{w_default:.2f}'),
            ('Weighted rows:\nrows times weight', repaid * w_repaid, defaulted * w_default, f'{repaid * w_repaid:,.0f}', f'{defaulted * w_default:,.0f}')]
    rh = (h - 0.2) / 3
    for i, (lab, a, b, ta, tb) in enumerate(rows):
        yc = h - 0.1 - (i + 0.5) * rh
        s.text(0.1, yc, lab, size=size, weight='bold', ha='left')
        if a is None:
            s.rect(x0, yc + 0.05, 0.3, 0.3, fill=PAPER, edge=INK, lw=1.8)
            s.text(x0 + 0.45, yc + 0.2, f'repaid: {ta}', size=size + 3, weight='bold', ha='left')
            s.rect(x0, yc - 0.4, 0.3, 0.3, fill=GOLD, edge=INK, lw=1.8)
            s.text(x0 + 0.45, yc - 0.25, f'defaulted: {tb}', size=size + 3, weight='bold', ha='left', color=RED)
            continue
        bwa, bwb = maxw * a / mx, maxw * b / mx
        s.rect(x0, yc + 0.05, bwa, 0.36, fill=PAPER, edge=INK, lw=2)
        s.text(x0 + bwa + 0.12, yc + 0.23, ta, size=size, weight='bold', ha='left')
        s.rect(x0, yc - 0.41, bwb, 0.36, fill=GOLD, edge=INK, lw=2)
        s.text(x0 + bwb + 0.12, yc - 0.23, tb, size=size, weight='bold', ha='left')
    return s
