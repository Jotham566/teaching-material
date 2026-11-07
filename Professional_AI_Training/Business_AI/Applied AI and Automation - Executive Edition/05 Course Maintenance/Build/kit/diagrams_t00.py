"""Figure kinds for Session 0: t00_roc, t00_descent, t00_weighted (house price weighted sum), t00_network (forward and backward pass), t00_confusion (spam filter)."""
import numpy as np

import matplotlib.pyplot as plt

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, fig

plt.rcParams.update({'mathtext.fontset': 'custom', 'mathtext.rm': 'Lato', 'mathtext.it': 'Lato:italic', 'mathtext.bf': 'Lato:bold',
                     'mathtext.default': 'it'})


def _panel(s, x, y, w, h, lines, gap=0.0):
    """A formula panel. lines: (text, size, color, weight) from the top down; the y step comes from the size."""
    s.box(x, y, w, h, '', fill=PAPER, edge=INK, lw=1.8, r=0.08)
    cy = y + h - 0.12
    for ln in lines:
        txt, size, col, wt = (list(ln) + [None, None, None])[:4] if not isinstance(ln, str) else (ln, 14, None, None)
        size = size or 14
        step = size / 72 * 1.5 + gap
        cy -= step / 2
        s.text(x + 0.14, cy, txt, size=size, ha='left', color=col or INK, weight=wt or 'normal')
        cy -= step / 2
    return s


@fig('x_t00_roc')
def x_t00_roc(w, h, size=14, **_):
    """ROC curve (illustrative, AUC 0.86) with the TPR and FPR formulas and the spam-filter numbers beside it."""
    s = Scene(w, h)
    pw = 3.15                      # formula panel width
    x0, x1, y0, y1 = 0.85, w - pw - 0.25, 0.75, h - 0.3
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    s.text((x0 + x1) / 2, 0.3, 'false positive rate', size=15, color=MUTE)
    s.text(0.3, (y0 + y1) / 2, 'true positive rate (recall)', size=15, color=MUTE, rot=90)
    px = lambda u: x0 + u * (x1 - x0)
    py = lambda v: y0 + v * (y1 - y0)
    us = np.linspace(0, 1, 80)
    curve = lambda u: u ** 0.163          # area under this curve is 1 / 1.163 = 0.86
    s.ax.fill_between([px(u) for u in us], [py(0)] * len(us), [py(curve(u)) for u in us], color=GOLD, alpha=0.45, zorder=1)
    s.ax.plot([px(0), px(1)], [py(0), py(1)], color=MUTE, lw=2, ls='--', zorder=2)
    s.ax.plot([px(u) for u in us], [py(curve(u)) for u in us], color=INK, lw=3.4, zorder=3)
    s.circle(px(0.1), py(curve(0.1)), 0.1, fill=RED, edge=INK, lw=1.6, z=5)
    s.text(px(0.1) + 0.2, py(curve(0.1)) - 0.3, 'one threshold', size=size, ha='left', color=RED, weight='bold')
    s.text(px(0.74), py(0.12), 'Dashed: coin flip,\narea 0.5', size=size, color=MUTE)
    s.text(px(0.64), py(0.36), 'Gold area =\nAUC', size=15, ha='center', weight='bold')
    _panel(s, w - pw, 0.25, pw, h - 0.5, [
        ('Rates at one threshold', 15, INK, 'bold'),
        (r'$\mathrm{TPR}=\frac{TP}{TP+FN}$', 18, INK, None),
        ('TPR = recall: spam caught', 14, BODY, None),
        (r'$\mathrm{FPR}=\frac{FP}{FP+TN}$', 18, INK, None),
        ('FPR: good emails flagged', 14, BODY, None),
        ('Spam filter example:', 14, INK, 'bold'),
        (r'$\mathrm{TPR}=30/50=0.60$', 15, INK, None),
        (r'$\mathrm{FPR}=10/950\approx0.011$', 15, INK, None),
        ('AUC = area under the curve', 14, BODY, None)], gap=0.04)
    return s


@fig('x_t00_loop')
def x_t00_loop(w, h, **_):
    """The training loop with its formulas and the house-price numbers (2 per m2, 10 per bedroom, bias 30, actual 300)."""
    s = Scene(w, h)
    bw, bh = 3.55, 1.35
    xl, xr = 0.1, w - bw - 0.1
    yt, yb = h - 0.05 - bh, 1.5
    boxes = [(xl, yt, '1  Predict', [r'$\hat{y}=w_1x_1+w_2x_2+b$', r'$=2\times100+10\times3+30=260$'], False),
             (xr, yt, '2  Measure the loss', [r'$L=(y-\hat{y})^2$', r'$=(300-260)^2=1{,}600$'], False),
             (xr, yb, '3  Update the parameters', [r'$w\leftarrow w-\eta\,\partial L/\partial w$', r'$\eta$ = learning rate'], True),
             (xl, yb, '4  Repeat: one epoch', ['One pass over all houses,', 'then back to step 1'], False)]
    for x, y, head, ls, hl in boxes:
        s.box(x, y, bw, bh, '', fill=GOLD if hl else PAPER, edge=INK, lw=2.0, r=0.08)
        s.text(x + bw / 2, y + bh - 0.27, head, size=16, weight='bold')
        s.text(x + bw / 2, y + 0.7, ls[0], size=17 if '$' in ls[0] else 15)
        s.text(x + bw / 2, y + 0.3, ls[1], size=15 if '$' in ls[1] else 14, color=BODY)
    ym_t, ym_b = yt + bh / 2, yb + bh / 2
    s.arrow(xl + bw + 0.05, ym_t, xr - 0.05, ym_t, lw=2.4, head=18)
    s.arrow(xr + bw / 2, yt - 0.04, xr + bw / 2, yb + bh + 0.04, lw=2.4, head=18)
    s.arrow(xr - 0.05, ym_b, xl + bw + 0.05, ym_b, lw=2.4, head=18)
    s.arrow(xl + bw / 2, yb + bh + 0.04, xl + bw / 2, yt - 0.04, lw=2.4, head=18)
    s.text(w / 2, 1.08, r'$y$ actual price (300)   $\hat{y}$ prediction   $w$ weight   $b$ bias   $L$ loss', size=13, color=BODY)
    s.text(w / 2, 0.62, r'$\mathrm{MSE}=\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2$', size=17, color=INK)
    s.text(w / 2, 0.14, r'MSE: the average over $n$ houses of the squared error; $\sum$ means add up', size=13, color=BODY)
    return s


@fig('x_t00_descent')
def x_t00_descent(w, h, size=14, **_):
    """Gradient descent on one weight, with the update rule and the house-price numbers beside the curve."""
    s = Scene(w, h)
    pw = 3.4
    x0, x1, y0, y1 = 0.7, w - pw - 0.2, 0.7, h - 0.4
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    s.text((x0 + x1) / 2, 0.3, 'one weight w (a parameter)', size=15, color=MUTE)
    s.text(0.3, (y0 + y1) / 2, 'loss L', size=15, color=MUTE, rot=90)
    xs = np.linspace(0, 1, 120)
    curve = lambda u: 0.12 + 0.88 * (2 * u - 1) ** 2
    px = lambda u: x0 + 0.2 + u * (x1 - x0 - 0.4)
    py = lambda v: y0 + 0.15 + v * (y1 - y0 - 0.3)
    s.ax.plot([px(u) for u in xs], [py(curve(u)) for u in xs], color=INK, lw=3, zorder=3)
    steps = [0.05, 0.2, 0.33, 0.42, 0.47, 0.5]
    for i, u in enumerate(steps):
        s.circle(px(u), py(curve(u)), 0.12 if i not in (0, len(steps) - 1) else 0.16, fill=GOLD if i in (0, len(steps) - 1) else PAPER, edge=INK, lw=2, z=5)
        if i:
            s.arrow(px(steps[i - 1]) + 0.1, py(curve(steps[i - 1])) - 0.05, px(u) - 0.1, py(curve(u)) + 0.05, color=RED, lw=2, head=14, z=4)
    s.text(px(0.05) + 0.25, py(curve(0.05)) + 0.2, 'Start: high loss', size=size, ha='left', weight='bold')
    s.text(px(0.5), py(0.6), 'Each step:\nupdate w', size=size, color=RED, weight='bold')
    s.text(px(0.5), py(0.3), 'Minimum', size=size, weight='bold')
    _panel(s, w - pw, 0.25, pw, h - 0.5, [
        ('One update step', 15, INK, 'bold'),
        (r'$w\leftarrow w-\eta\,\frac{\partial L}{\partial w}$', 19, INK, None),
        (r'$w$ weight, $\eta$ learning rate,', 13, BODY, None),
        (r'$\partial L/\partial w$ gradient (slope of loss)', 13, BODY, None),
        ('House weight for floor area:', 14, INK, 'bold'),
        (r'$\partial L/\partial w_1=-2x_1(y-\hat{y})$', 14, INK, None),
        (r'$=-2\times100\times40=-8{,}000$', 14, INK, None),
        (r'$\eta=0.00001$ (small, as the slope is large)', 13, BODY, None),
        (r'$w_1=2-0.00001\times(-8{,}000)=2.08$', 14, RED, 'bold'),
        (r'New $\hat{y}=268$; loss $=32^2=1{,}024$', 14, INK, None)], gap=0.03)
    return s


@fig('x_t00_weighted')
def x_t00_weighted(w, h, **_):
    """House price as a weighted sum. 2 x 100 + 10 x 3 + 30 = 260 (UGX millions); actual price 300; error 40. Formulas in a panel."""
    s = Scene(w, h)
    pw = 3.3
    ox, oy = 3.7, 2.75
    s.text(0.65, 4.5, 'inputs x', size=15, weight='bold')
    s.text(2.1, 4.5, 'weights w', size=15, weight='bold', color=RED)
    s.text(ox, 4.5, 'prediction z', size=15, weight='bold')
    for y, v, nm, wt in [(3.5, '100', 'floor area (m²)', '2'), (1.95, '3', 'bedrooms', '10')]:
        s.circle(0.65, y, 0.4, fill=PAPER, edge=INK, lw=2, z=3)
        s.text(0.65, y, v, size=20, weight='bold')
        s.text(0.65, y - 0.68, nm, size=13, color=BODY)
        s.line(1.05, y, ox - 0.55, oy, color=BODY, lw=1.8, z=1)
        mx = 2.1
        my = y + (oy - y) * (mx - 1.05) / (ox - 0.55 - 1.05)
        s.circle(mx, my, 0.34, fill=GOLD, edge=INK, lw=2.2, z=4)
        s.text(mx, my, wt, size=16, weight='bold', z=7)
    s.circle(ox, oy, 0.55, fill=PAPER, edge=INK, lw=2.4, z=3)
    s.text(ox, oy, '260', size=22, weight='bold')
    s.box(2.45, 0.55, 1.5, 0.6, 'bias b = 30', size=15, weight='bold', fill=GOLD, edge=INK)
    s.line(3.2, 1.15, ox - 0.1, oy - 0.55, color=BODY, lw=1.8, z=1)
    s.text(ox, 0.2, 'UGX millions', size=13, color=MUTE)
    _panel(s, w - pw, 0.25, pw, h - 0.5, [
        ('The weighted sum', 15, INK, 'bold'),
        (r'$z=w_1x_1+w_2x_2+b$', 17, INK, None),
        (r'$z=\mathbf{w}\cdot\mathbf{x}+b$ (vector form)', 13, BODY, None),
        (r'$z=2\times100+10\times3+30=260$', 14, INK, None),
        ('Then an activation f gives a = f(z):', 13, BODY, None),
        (r'ReLU: $f(z)=\max(0,z)$', 14, INK, None),
        (r'Sigmoid: $\sigma(z)=\frac{1}{1+e^{-z}}$', 16, INK, None),
        ('x input, w weight, b bias, z sum', 13, BODY, None),
        ('actual 300, error = 300 − 260 = 40', 14, RED, 'bold')], gap=0.03)
    return s


@fig('x_t00_network')
def x_t00_network(w, h, size=14, **_):
    """Forward and backward pass on a small network, with the chain rule and the house-price gradient written underneath."""
    s = Scene(w, h)
    ph = 1.55                       # formula panel height at the bottom
    layers = (('Input layer', 3), ('Hidden layer', 4), ('Hidden layer', 4), ('Output layer', 1))
    n = len(layers)
    xs = [0.9 + i * (w - 1.8) / (n - 1) for i in range(n)]
    top, bot = h - 1.15, ph + 0.75
    pos = []
    for (nm, k), x in zip(layers, xs):
        col = [(x, bot + (top - bot) * (j + 0.5) / k) for j in range(k)]
        pos.append(col)
        s.text(x, h - 0.2, nm, size=size, weight='bold')
    for a, b in zip(pos, pos[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b:
                s.line(x1, y1, x2, y2, color=HAIR, lw=1.2, z=1)
    for col in pos:
        for (x, y) in col:
            s.circle(x, y, 0.13, fill=PAPER, edge=INK, lw=2, z=4)
    s.circle(pos[-1][0][0], pos[-1][0][1], 0.2, fill=GOLD, edge=INK, lw=2.4, z=5)
    s.arrow(xs[0] + 0.3, ph + 0.55, xs[-1] - 0.3, ph + 0.55, color=INK, lw=2.4, head=16)
    s.text((xs[0] + xs[-1]) / 2, ph + 0.28, 'forward pass: prediction and loss', size=size, color=INK)
    s.arrow(xs[-1] - 0.3, h - 0.52, xs[0] + 0.3, h - 0.52, color=RED, lw=2.4, head=16)
    s.text((xs[0] + xs[-1]) / 2, h - 0.8, 'backward pass: gradient of the loss for each weight', size=size, color=RED, weight='bold')
    _panel(s, 0.1, 0.1, w - 0.2, ph, [
        (r'Chain rule:  $\frac{\partial L}{\partial w_1}=\frac{\partial L}{\partial\hat{y}}\cdot\frac{\partial\hat{y}}{\partial z}\cdot\frac{\partial z}{\partial w_1}$', 20, INK, None),
        (r'House:  $(-2(y-\hat{y}))\times(1)\times(x_1)=(-80)\times1\times100=-8{,}000$', 15, RED, 'bold'),
        (r'$L$ loss, $\hat{y}$ prediction, $z$ weighted sum, $w_1$ one weight, $\partial$ = "small change in"', 13, BODY, None),
        (r'Here $\hat{y}=z$ (no activation), so $\partial\hat{y}/\partial z=1$; $\partial z/\partial w_1=x_1=100$', 13, BODY, None)], gap=0.04)
    return s


@fig('x_t00_confusion')
def x_t00_confusion(w, h, tp=30, fp=10, fn=20, tn=940, size=18, **_):
    """Confusion matrix for a spam filter: rows are what the model said, columns what was true."""
    s = Scene(w, h)
    lw_, top = 2.0, 0.9
    cw = (w - lw_ - 0.1) / 2
    ch = (h - top - 0.1) / 2
    x0 = lw_
    s.text(x0 + cw / 2, h - 0.45, 'Really spam', size=size, weight='bold')
    s.text(x0 + cw * 1.5, h - 0.45, 'Really not spam', size=size, weight='bold')
    s.text(lw_ / 2, 0.1 + ch * 1.5, 'Model said\n"spam"', size=size, weight='bold')
    s.text(lw_ / 2, 0.1 + ch * 0.5, 'Model said\n"not spam"', size=size, weight='bold')
    cells = [(0, 1, tp, 'True positive (TP)', 'spam caught', GOLD), (1, 1, fp, 'False positive (FP)', 'good email flagged', PAPER),
             (0, 0, fn, 'False negative (FN)', 'spam missed', PAPER), (1, 0, tn, 'True negative (TN)', 'good email passed', PAPER)]
    for cx, cy, n, nm, sub, fill in cells:
        x = x0 + cx * cw + 0.05
        y = 0.1 + cy * ch + 0.05
        s.box(x, y, cw - 0.1, ch - 0.1, '', fill=fill, edge=INK, lw=2.0, r=0.06)
        s.text(x + (cw - 0.1) / 2, y + (ch - 0.1) * 0.66, f'{n:,}', size=36, weight='bold')
        s.text(x + (cw - 0.1) / 2, y + (ch - 0.1) * 0.26, nm + '\n' + sub, size=size - 4, color=BODY)
    return s
