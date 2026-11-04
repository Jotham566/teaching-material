"""Figure kinds for Sessions 19 and 20 (forecasting, neural networks), author letter j. Registered as x_dsj_<kind>; used as visual=dict(kind='dsj_<kind>', ...).

  dsj_decomp      a time series pulled apart into observed, trend, season and noise panels (real numbers passed in)
  dsj_columns     vertical columns with value labels (labels, values, hl)
  dsj_lines       a line chart with a legend, an optional cut line (the train and test cut) and optional dots
  dsj_timesplit   60 months as squares: a random split next to a split at a cut date
  dsj_scatter2    two scatter panels side by side with their correlation
  dsj_pipeline    a scikit-learn Pipeline as one box holding its steps, fit on train and predict on test
  dsj_horizon     a month line with today marked and forecast horizons of 1, 3 and 12 months
  dsj_neuron      one artificial neuron: inputs, weights, weighted sum plus bias, activation, output (numbers passed in)
  dsj_activations sigmoid and ReLU curves side by side
  dsj_mlp         a feedforward network (multilayer perceptron) with layer names and counts
  dsj_descent     gradient descent on one weight: the loss curve with the real steps marked
  dsj_epoch       one epoch as a row of batches
  dsj_playground  a labelled sketch of the TensorFlow Playground screen
  dsj_transfer    a pretrained network: frozen early layers, a new last layer trained on your own data
All text is 14 pt or larger and every figure is audited for overlaps by figkit.
"""
import math

import numpy as np
from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, PALE, fig
import slidekit as K


def tw(t, size, kind='regular'):
    return K.width_in(str(t), size, kind)


def wrapped(s, x, y, w, text, size, weight='normal', color=INK, ha='left', va='center'):
    lines = K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', w)
    s.text(x, y, '\n'.join(lines), size=size, weight=weight, color=color, ha=ha, va=va)
    return len(lines) * size * 1.15 / 72


def nice(v):
    """A tick label with thousands separators."""
    return f'{v:,.0f}'


def axes(s, x0, y0, x1, y1):
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)


# ------------------------------------------------------------------ decomposition
@fig('x_dsj_decomp')
def dsj_decomp(w, h, observed=(), trend=(), season=(), noise=(), year_ticks=(), unit='cases', **_):
    s = Scene(w, h)
    panels = [('Observed', observed, INK), ('Trend', trend, RED), ('Season', season, INK), ('Noise', noise, MUTE)]
    left, right = 1.55, 0.2
    n = len(observed)
    ph = (h - 0.55) / 4
    for k, (name, vals, col) in enumerate(panels):
        ytop = h - 0.05 - k * ph
        ybot = ytop - ph + 0.12
        vals = np.asarray(vals, float)
        lo, hi = vals.min(), vals.max()
        if name in ('Season', 'Noise'):
            m = max(abs(lo), abs(hi)); lo, hi = -m, m
        pad = (hi - lo) * 0.12 or 1
        lo -= pad; hi += pad
        px = lambda i: left + i / (n - 1) * (w - left - right)
        py = lambda v: ybot + (v - lo) / (hi - lo) * (ytop - 0.12 - ybot)
        s.line(left, ybot, w - right, ybot, color=HAIR, lw=1.2)
        if name in ('Season', 'Noise'):
            s.line(left, py(0), w - right, py(0), color=HAIR, lw=1.0, dash=True)
        s.ax.plot([px(i) for i in range(n)], [py(v) for v in vals], color=col, lw=2.6, zorder=4)
        s.text(0.1, (ytop + ybot) / 2 + 0.1, name, size=16, weight='bold', ha='left', color=col if col != MUTE else BODY)
    for i, lab in year_ticks:
        x = left + i / (n - 1) * (w - left - right)
        s.text(x, 0.2, lab, size=14, color=BODY)
        s.line(x, 0.42, x, 0.5, color=INK, lw=1.4)
    return s


# ------------------------------------------------------------------ columns
@fig('x_dsj_columns')
def dsj_columns(w, h, labels=(), values=(), hl=(), ylabel='', fmt='{:,.0f}', size=14, valsize=14, **_):
    s = Scene(w, h)
    n = len(values)
    x0, y0 = 0.15, 0.55
    top = h - 0.55
    mx = max(values)
    slot = (w - x0 - 0.1) / n
    bw = slot * 0.7
    for i, v in enumerate(values):
        bh = (v / mx) * (top - y0)
        x = x0 + i * slot + (slot - bw) / 2
        s.rect(x, y0, bw, bh, fill=GOLD if i in hl else INK, edge=INK, lw=1.4, z=2)
        s.text(x + bw / 2, y0 + bh + 0.2, fmt.format(v), size=valsize, color=INK, weight='bold' if i in hl else 'normal')
        s.text(x + bw / 2, 0.3, labels[i], size=size, color=BODY)
    s.line(x0, y0, w - 0.1, y0, color=INK, lw=2)
    return s


# ------------------------------------------------------------------ lines
@fig('x_dsj_lines')
def dsj_lines(w, h, series=(), ticks=(), cut=None, cut_label='', ylabel='', xlabel='', ymin=None, ymax=None, legend='top', yticks=(), size=15, shade=None, yfmt='{:,.0f}', **_):
    """series: [{name, values (None = gap), color 'ink'|'red'|'gold'|'grey', dash, dots}]; ticks: [(index, label)]; cut: x index of a dashed vertical line; shade: (i0, i1) pale band."""
    s = Scene(w, h)
    colors = {'ink': INK, 'red': RED, 'gold': GOLD, 'grey': GREY, 'mute': MUTE}
    nmax = max(len(sr['values']) for sr in series)
    allv = [v for sr in series for v in sr['values'] if v is not None]
    lo = min(allv) if ymin is None else ymin
    hi = max(allv) if ymax is None else ymax
    lead = 0.0
    if legend == 'top':
        lead = 0.5
    x0, x1 = 1.25 if ylabel or yticks else 0.4, w - 0.3
    y0, y1 = 0.75 if (ticks or xlabel) else 0.3, h - 0.2 - lead
    if xlabel:
        y0 += 0.3
    px = lambda i: x0 + i / (nmax - 1) * (x1 - x0)
    py = lambda v: y0 + (v - lo) / (hi - lo) * (y1 - y0)
    axes(s, x0, y0, x1, y1)
    if shade:
        s.rect(px(shade[0]), y0, px(shade[1]) - px(shade[0]), y1 - y0, fill=PALE, edge=PALE, lw=0, z=0)
    for v in yticks:
        s.text(x0 - 0.12, py(v), yfmt.format(v), size=14, color=BODY, ha='right')
        s.line(x0, py(v), x1, py(v), color=HAIR, lw=0.9, z=0)
    for i, lab in ticks:
        s.text(px(i), y0 - 0.25, lab, size=14, color=BODY)
        s.line(px(i), y0, px(i), y0 - 0.08, color=INK, lw=1.4)
    if xlabel:
        s.text((x0 + x1) / 2, 0.2, xlabel, size=size, color=MUTE)
    if ylabel:
        s.text(0.3, (y0 + y1) / 2, ylabel, size=size, color=MUTE, rot=90)
    if cut is not None:
        s.line(px(cut), y0, px(cut), y1, color=INK, lw=1.8, dash=True, z=2)
        if cut_label:
            s.text(px(cut) - 0.1, y1 - 0.02, cut_label.split('|')[0], size=14, color=BODY, ha='right', va='top')
            if '|' in cut_label:
                s.text(px(cut) + 0.1, y1 - 0.02, cut_label.split('|')[1], size=14, color=BODY, ha='left', va='top')
    for sr in series:
        col = colors.get(sr.get('color', 'ink'), INK)
        pts = [(i, v) for i, v in enumerate(sr['values']) if v is not None]
        s.ax.plot([px(i) for i, _ in pts], [py(v) for _, v in pts], color=col, lw=sr.get('lw', 3.0), ls='--' if sr.get('dash') else '-', zorder=4)
        if sr.get('dots'):
            for i, v in pts:
                s.circle(px(i), py(v), 0.065, fill=col, edge=INK, lw=1.0, z=5)
    if legend == 'top':
        x = x0
        for sr in series:
            col = colors.get(sr.get('color', 'ink'), INK)
            s.line(x, h - 0.3, x + 0.55, h - 0.3, color=col, lw=3.4, dash=bool(sr.get('dash')), z=4)
            s.text(x + 0.65, h - 0.3, sr['name'], size=size, ha='left')
            x += 0.65 + tw(sr['name'], size) + 0.5
    return s


# ------------------------------------------------------------------ time split
@fig('x_dsj_timesplit')
def dsj_timesplit(w, h, n=60, cut=48, test_idx=(), year_ticks=(), left_title='', right_title='', note_left='', note_right='', **_):
    """Two strips of n month squares. Top: test months scattered at random (test_idx). Bottom: train before the cut date, test after it."""
    s = Scene(w, h)
    lab_w = 0.1
    cw = (w - 0.3) / n
    sq = cw * 0.86

    def strip(y, is_test):
        for i in range(n):
            t = is_test(i)
            s.rect(0.15 + i * cw + (cw - sq) / 2, y, sq, sq * 1.5, fill=GOLD if t else INK, edge=INK, lw=0.8, z=2)

    tests = set(test_idx)
    sh = sq * 1.5
    s.text(0.15, h - 0.3, left_title, size=17, weight='bold', ha='left')
    y1 = h - 0.95
    strip(y1, lambda i: i in tests)
    s.text(0.15, y1 - 0.3, note_left, size=15, color=BODY, ha='left')
    t2 = y1 - 0.95
    s.text(0.15, t2, right_title, size=17, weight='bold', ha='left')
    y2 = t2 - 0.65
    strip(y2, lambda i: i >= cut)
    s.line(0.15 + cut * cw, y2 - 0.1, 0.15 + cut * cw, y2 + sh + 0.1, color=RED, lw=3.0, z=6)
    for i, lab in year_ticks:
        s.text(0.15 + (i + 0.5) * cw, y2 - 0.3, lab, size=14, color=BODY)
    s.text(0.15, y2 - 0.7, note_right, size=15, color=BODY, ha='left')
    # key
    kx = w - 3.75
    s.rect(kx, h - 0.45, 0.28, 0.28, fill=INK, edge=INK, lw=1)
    s.text(kx + 0.38, h - 0.31, 'training month', size=15, ha='left')
    s.rect(kx + 2.1, h - 0.45, 0.28, 0.28, fill=GOLD, edge=INK, lw=1)
    s.text(kx + 2.48, h - 0.31, 'test month', size=15, ha='left')
    return s


# ------------------------------------------------------------------ two scatter panels
@fig('x_dsj_scatter2')
def dsj_scatter2(w, h, panels=(), size=15, **_):
    """panels: [{title, points [(x, y)], xlabel, r_label}]; both panels share the y range."""
    s = Scene(w, h)
    n = len(panels)
    pw = (w - 0.2) / n
    ys = [p[1] for pn in panels for p in pn['points']]
    ylo, yhi = min(ys), max(ys)
    for k, pn in enumerate(panels):
        ox = 0.1 + k * pw
        x0, x1, y0, y1 = ox + 0.95, ox + pw - 0.2, 0.85, h - 0.95
        xs = [p[0] for p in pn['points']]
        xlo, xhi = min(xs), max(xs)
        px = lambda v: x0 + (v - xlo) / (xhi - xlo) * (x1 - x0)
        py = lambda v: y0 + (v - ylo) / (yhi - ylo) * (y1 - y0)
        axes(s, x0, y0, x1, y1)
        s.text(ox + pw / 2, h - 0.3, pn['title'], size=17, weight='bold')
        s.text(ox + pw / 2, h - 0.68, pn['r_label'], size=16, weight='bold', color=RED)
        s.text((x0 + x1) / 2, 0.3, pn['xlabel'], size=size, color=MUTE)
        if k == 0:
            s.text(ox + 0.2, (y0 + y1) / 2, 'malaria cases in the month', size=size, color=MUTE, rot=90)
        for v in (xlo, xhi):
            s.text(px(v), y0 - 0.2, f'{v:.0f}', size=14, color=GREY)
        for (a, b) in pn['points']:
            s.circle(px(a), py(b), 0.045, fill=INK, edge=INK, lw=0.4, z=4)
        if pn.get('line'):
            b0, b1 = pn['line']
            s.ax.plot([px(xlo), px(xhi)], [py(b0 + b1 * xlo), py(b0 + b1 * xhi)], color=RED, lw=3.2, zorder=5)
    for v in (ylo, yhi):
        s.text(0.1 + 0.88, 0.85 + (v - ylo) / (yhi - ylo) * (h - 0.95 - 0.85), f'{v:,.0f}', size=14, color=GREY, ha='right')
    return s


# ------------------------------------------------------------------ pipeline
@fig('x_dsj_pipeline')
def dsj_pipeline(w, h, steps=(), in_label='Variables X', out_label='Predictions', fit_text='', predict_text='', **_):
    """steps: [{name, text}] drawn inside one outer box labelled Pipeline."""
    s = Scene(w, h)
    n = len(steps)
    oy0, oy1 = 1.6, h - 0.1
    ox0, ox1 = 1.95, w - 1.95
    s.box(ox0, oy0, ox1 - ox0, oy1 - oy0, '', fill=PALE, edge=INK, lw=2.6, r=0.1)
    s.text(ox0 + 0.2, oy1 - 0.32, 'Pipeline', size=19, weight='bold', ha='left')
    gap = 0.45
    bw = (ox1 - ox0 - 0.4 - gap * (n - 1)) / n
    by0, by1 = oy0 + 0.25, oy1 - 0.75
    for i, st in enumerate(steps):
        x = ox0 + 0.2 + i * (bw + gap)
        s.box(x, by0, bw, by1 - by0, '', fill=GOLD if i == n - 1 else PAPER, edge=INK, lw=2.0, r=0.07, z=3)
        s.text(x + bw / 2, by1 - 0.28, st['name'], size=16, weight='bold', z=4)
        wrapped(s, x + bw / 2, by1 - 0.62, bw - 0.25, st['text'], 15, ha='center', va='top')
        if i < n - 1:
            s.arrow(x + bw + 0.04, (by0 + by1) / 2, x + bw + gap - 0.04, (by0 + by1) / 2, lw=2.4, head=16)
    ym = (by0 + by1) / 2
    s.box(0.1, ym - 0.45, 1.5, 0.9, in_label, size=16, weight='bold', r=0.06)
    s.arrow(1.65, ym, ox0 - 0.05, ym, lw=2.4, head=16)
    s.arrow(ox1 + 0.05, ym, w - 1.65, ym, lw=2.4, head=16)
    s.box(w - 1.6, ym - 0.45, 1.5, 0.9, out_label, size=16, weight='bold', r=0.06)
    wrapped(s, 0.1, 0.95, w / 2 - 0.3, fit_text, 16, ha='left')
    wrapped(s, w / 2 + 0.1, 0.95, w / 2 - 0.3, predict_text, 16, ha='left')
    return s


# ------------------------------------------------------------------ forecast horizon
@fig('x_dsj_horizon')
def dsj_horizon(w, h, past=12, future=12, horizons=((1, 'horizon 1 month'), (3, 'horizon 3 months'), (12, 'horizon 12 months')), past_label='months you know', **_):
    s = Scene(w, h)
    n = past + future
    cw = (w - 0.3) / n
    sq = cw * 0.82
    y = 1.0
    for i in range(n):
        x = 0.15 + i * cw + (cw - sq) / 2
        s.rect(x, y, sq, sq, fill=INK if i < past else PAPER, edge=INK, lw=1.2, z=2)
    xt = 0.15 + past * cw
    s.line(xt, y - 0.2, xt, y + sq + 0.25, color=RED, lw=3.2, z=6)
    s.text(xt, y - 0.45, 'today: the last month with data', size=16, weight='bold', color=RED)
    s.text(0.15 + past * cw / 2, y + sq + 0.35, past_label, size=16, color=BODY)
    top = y + sq + 0.55
    for k, (hz, lab) in enumerate(horizons):
        yy = top + 0.35 + k * 0.66
        s.line(xt, yy, xt + hz * cw, yy, color=INK, lw=3.0, z=5)
        s.line(xt + hz * cw, yy - 0.1, xt + hz * cw, yy + 0.1, color=INK, lw=3.0, z=5)
        s.line(xt, yy - 0.1, xt, yy + 0.1, color=INK, lw=3.0, z=5)
        s.text(xt + 0.05, yy + 0.27, lab, size=16, ha='left', weight='bold')
    return s


# ------------------------------------------------------------------ one neuron
@fig('x_dsj_neuron')
def dsj_neuron(w, h, inputs=(), bias=0.0, z=0.0, out=0.0, act='sigmoid', out_label='score', **_):
    """inputs: [{name, x, w}]. Draws inputs, weights, the weighted sum plus bias, the activation function and the output."""
    s = Scene(w, h)
    n = len(inputs)
    heads = [(1.45, '1 Inputs'), (4.1, '2 Weights'), (6.35, '3 Sum plus bias'), (8.75, '4 Activation'), (11.0, '5 Output')]
    for x, t in heads:
        s.text(x, h - 0.25, t, size=16, weight='bold', color=RED)
    top, bot = h - 0.95, 1.25
    ys = [top - (top - bot) * (i + 0.5) / n for i in range(n)]
    cx, cy = 6.35, (top + bot) / 2
    for (inp, y) in zip(inputs, ys):
        s.box(0.1, y - 0.33, 2.7, 0.66, f"{inp['name']} = {inp['x']:g}", size=15, r=0.05)
        s.arrow(2.85, y, cx - 0.55, cy + (y - cy) * 0.25, lw=2.0, head=14)
        s.text(3.7, y + (cy - y) * 0.0 + 0.0 + (0.27 if y >= cy else -0.27) * 1.0 + (cy - y) * 0.12, f"× {inp['w']:g}", size=15, weight='bold')
    s.circle(cx, cy, 0.55, fill=GOLD, edge=INK, lw=2.4, z=4)
    s.text(cx, cy, 'Σ', size=30, weight='bold', z=6)
    s.text(cx, cy - 0.95, f'bias b = {bias:g}', size=16, weight='bold')
    s.text(cx, cy + 0.9, f'z = {z:.2f}', size=16, weight='bold')
    s.arrow(cx + 0.58, cy, 7.75, cy, lw=2.4, head=16)
    s.box(7.8, cy - 0.45, 1.9, 0.9, act, size=18, weight='bold', r=0.06)
    s.arrow(9.75, cy, 10.2, cy, lw=2.4, head=16)
    s.box(10.25, cy - 0.45, 1.55, 0.9, f'{out:.3f}', size=20, weight='bold', fill=GOLD, r=0.06)
    s.text(11.0, cy - 0.85, out_label, size=15, color=BODY)
    return s


# ------------------------------------------------------------------ activation functions
@fig('x_dsj_activations')
def dsj_activations(w, h, z_mark=None, **_):
    s = Scene(w, h)
    pw = (w - 0.4) / 2
    specs = [('Sigmoid', lambda z: 1 / (1 + np.exp(-z)), (-6, 6), (-0.05, 1.05), 'squashes any total into 0 to 1', [0, 0.5, 1]),
             ('ReLU', lambda z: np.maximum(z, 0), (-6, 6), (-0.5, 6.5), '0 for a negative total, the total itself otherwise', [0, 3, 6])]
    for k, (name, f, xr, yr, sub, yt) in enumerate(specs):
        ox = 0.2 + k * pw
        x0, x1, y0, y1 = ox + 0.75, ox + pw - 0.3, 1.15, h - 0.8
        px = lambda v: x0 + (v - xr[0]) / (xr[1] - xr[0]) * (x1 - x0)
        py = lambda v: y0 + (v - yr[0]) / (yr[1] - yr[0]) * (y1 - y0)
        s.text(ox + pw / 2, h - 0.3, name, size=19, weight='bold')
        s.line(x0, py(0), x1, py(0), color=INK, lw=1.8)
        s.line(px(0), y0, px(0), y1, color=HAIR, lw=1.4)
        zs = np.linspace(xr[0], xr[1], 120)
        s.ax.plot([px(v) for v in zs], [py(f(v)) for v in zs], color=INK, lw=3.4, zorder=4)
        for v in (-6, 0, 6):
            s.text(px(v), y0 - 0.2 + (0.0), f'{v}', size=14, color=BODY)
        for v in yt:
            s.text(x0 - 0.1, py(v), f'{v:g}', size=14, color=BODY, ha='right')
        s.text((x0 + x1) / 2, 0.55, 'the total z going in', size=15, color=MUTE)
        s.text(ox + pw / 2, h - 0.62, sub, size=15, color=BODY)
        if z_mark is not None:
            zm, label = z_mark
            s.circle(px(zm), py(f(zm)), 0.11, fill=GOLD, edge=INK, lw=2, z=6)
            outv = float(f(zm))
            s.text(x0 + 0.1, py(yr[1] - (yr[1] - yr[0]) * 0.17), f'gold dot:\nz = {zm:g} gives {outv:.3f}' if k == 0 else f'gold dot:\nz = {zm:g} gives {outv:.2f}', size=15, weight='bold', ha='left', color=RED)
    return s


# ------------------------------------------------------------------ feedforward network
@fig('x_dsj_mlp')
def dsj_mlp(w, h, layers=(), note='', **_):
    """layers: [(name, count, sub)] drawn with every neuron; every neuron joins every neuron of the next layer."""
    s = Scene(w, h)
    n = len(layers)
    xs = [0.9 + i * (w - 1.8) / (n - 1) for i in range(n)]
    top, bot = h - 0.75, 1.35
    pos = []
    for (nm, cnt, sub), x in zip(layers, xs):
        col = []
        for j in range(cnt):
            y = (top + bot) / 2 if cnt == 1 else top - (top - bot) * j / (cnt - 1)
            col.append((x, y))
        pos.append(col)
        s.text(x, 0.82, nm, size=16, weight='bold')
        s.text(x, 0.4, sub, size=15, color=BODY)
    for a, b in zip(pos, pos[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b:
                s.line(x1, y1, x2, y2, color=HAIR, lw=0.8, z=1)
    for k, col in enumerate(pos):
        for (x, y) in col:
            last = k == n - 1
            s.circle(x, y, (0.08 if len(col) > 12 else 0.11) if not last else 0.2, fill=GOLD if last else PAPER, edge=INK, lw=1.8, z=4)
    if note:
        s.text(w / 2, h - 0.25, note, size=15, color=BODY)
    return s


# ------------------------------------------------------------------ gradient descent on one weight
@fig('x_dsj_descent')
def dsj_descent(w, h, weights=(), losses=(), target=3.0, start_label='', end_label='', **_):
    s = Scene(w, h)
    x0, x1, y0, y1 = 0.95, w - 0.3, 0.85, h - 0.3
    xr = (-0.5, 6.5)
    yr = (-1.5, max(losses) * 1.08)
    px = lambda v: x0 + (v - xr[0]) / (xr[1] - xr[0]) * (x1 - x0)
    py = lambda v: y0 + (v - yr[0]) / (yr[1] - yr[0]) * (y1 - y0)
    axes(s, x0, y0, x1, y1)
    s.text((x0 + x1) / 2, 0.3, 'the weight w', size=16, color=MUTE)
    s.text(0.3, (y0 + y1) / 2, 'loss', size=16, color=MUTE, rot=90)
    for v in (0, 3, 6):
        s.text(px(v), y0 - 0.2, f'{v}', size=14, color=BODY)
    ws = np.linspace(xr[0], xr[1], 150)
    s.ax.plot([px(v) for v in ws], [py((2 * v - 6) ** 2) for v in ws], color=INK, lw=3.2, zorder=3)
    for i in range(1, len(weights)):
        s.arrow(px(weights[i - 1]) + 0.05, py(losses[i - 1]) + 0.03, px(weights[i]) - 0.05, py(losses[i]) + 0.03, color=RED, lw=2.0, head=13, z=5)
    for i, (a, b) in enumerate(zip(weights, losses)):
        s.circle(px(a), py(b), 0.1, fill=GOLD if i in (0, len(weights) - 1) else PAPER, edge=INK, lw=1.8, z=6)
    s.text(px(weights[0]) + 0.3, py(losses[0]) + 0.15, start_label, size=15, ha='left', weight='bold')
    s.text(px(3.5), py(14), end_label, size=15, ha='left', weight='bold', color=RED)
    return s


# ------------------------------------------------------------------ one epoch
@fig('x_dsj_epoch')
def dsj_epoch(w, h, n_rows=0, batch=0, n_batches=0, **_):
    s = Scene(w, h)
    cw = (w - 0.3) / n_batches
    sq = cw * 0.8
    y = h - 1.7
    s.text(0.15, h - 0.35, f'Training set: {n_rows:,} records, cut into {n_batches} batches of up to {batch} records', size=17, weight='bold', ha='left')
    for i in range(n_batches):
        s.rect(0.15 + i * cw + (cw - sq) / 2, y, sq, 0.6, fill=GOLD if i == 0 else PAPER, edge=INK, lw=1.2, z=2)
    s.text(0.15 + cw / 2, y - 0.3, 'batch 1', size=15, ha='left')
    s.text(w - 0.15, y - 0.3, f'batch {n_batches}', size=15, ha='right')
    s.brace(0.15, w - 0.15, y - 0.65, depth=0.18, up=False)
    s.text(w / 2, y - 1.05, f'One epoch: the network has seen every training record once, in {n_batches} batches', size=17, weight='bold')
    s.text(w / 2, y - 1.5, f'After each batch the weights are adjusted once, so one epoch makes {n_batches} adjustments.', size=16, color=BODY)
    return s


# ------------------------------------------------------------------ TensorFlow Playground sketch
@fig('x_dsj_playground')
def dsj_playground(w, h, **_):
    s = Scene(w, h)
    heads = [('Epoch', 'counts passes'), ('Learning rate', 'step size'), ('Activation', 'ReLU, tanh, sigmoid'), ('Regularization', 'penalty'), ('Problem type', 'classification')]
    bw = (w - 0.2 - 0.15 * 4) / 5
    for i, (a, b) in enumerate(heads):
        x = 0.1 + i * (bw + 0.15)
        s.box(x, h - 1.0, bw, 0.85, '', fill=PALE, edge=INK, lw=1.6, r=0.06)
        s.text(x + bw / 2, h - 0.42, a, size=15, weight='bold')
        s.text(x + bw / 2, h - 0.74, b, size=14, color=BODY)
    cols = [('DATA', 'circle, XOR or spiral dots;\nnoise and train/test ratio'), ('FEATURES', 'x1 and x2, and\nmade-up ones'), ('HIDDEN LAYERS', 'add or remove layers and\nneurons with + and -'), ('OUTPUT', 'dots coloured by the\nnetwork; loss shown')]
    cw = (w - 0.2 - 0.3 * 3) / 4
    bh = h - 1.35
    cym = 0.15 + bh * 0.52
    for i, (a, b) in enumerate(cols):
        x = 0.1 + i * (cw + 0.3)
        s.box(x, 0.15, cw, bh, '', fill=PAPER, edge=INK, lw=2.0, r=0.07)
        s.text(x + cw / 2, 0.15 + bh - 0.3, a, size=17, weight='bold')
        s.text(x + cw / 2, 0.62, b, size=15, color=BODY)
        if i < 3:
            s.arrow(x + cw + 0.02, cym, x + cw + 0.28, cym, lw=2.2, head=14)
    x = 0.1
    s.circle(x + cw / 2, cym, 0.6, fill=PAPER, edge=INK, lw=2.4)
    s.circle(x + cw / 2, cym, 0.27, fill=GOLD, edge=INK, lw=2.0)
    x = 0.1 + (cw + 0.3)
    for k, t in enumerate(['x1', 'x2']):
        s.box(x + cw / 2 - 0.45, cym + 0.1 - k * 0.7, 0.9, 0.5, t, size=16, weight='bold', r=0.05)
    x = 0.1 + 2 * (cw + 0.3)
    for L, cnt in enumerate((4, 2)):
        for j in range(cnt):
            yy = cym if cnt == 1 else cym + 0.6 - j * (1.2 / (cnt - 1))
            s.circle(x + cw * (0.33 + 0.34 * L), yy, 0.15, fill=PAPER, edge=INK, lw=2.0)
    x = 0.1 + 3 * (cw + 0.3)
    s.rect(x + cw / 2 - 0.7, cym - 0.55, 1.4, 1.1, fill=PALE, edge=INK, lw=2.0)
    s.circle(x + cw / 2 - 0.3, cym + 0.2, 0.14, fill=GOLD, edge=INK, lw=1.6, z=4)
    s.circle(x + cw / 2 + 0.3, cym - 0.2, 0.14, fill=INK, edge=INK, lw=1.6, z=4)
    return s


# ------------------------------------------------------------------ transfer learning
@fig('x_dsj_transfer')
def dsj_transfer(w, h, **_):
    s = Scene(w, h)
    items = [('Early layers', 'edges, colours, simple textures', 'frozen: reused as they are', PAPER), ('Middle layers', 'shapes and parts of objects', 'frozen: reused as they are', PAPER), ('Last layer', 'your classes, for example ripe or unripe', 'new: trained on your own photos', GOLD)]
    n = 3
    gap = 0.6
    bw = (w - 0.2 - gap * (n - 1)) / n
    by0, by1 = 1.9, h - 0.15
    for i, (a, b, c, fill) in enumerate(items):
        x = 0.1 + i * (bw + gap)
        s.box(x, by0, bw, by1 - by0, '', fill=fill, edge=INK, lw=2.2, r=0.08)
        s.text(x + bw / 2, by1 - 0.4, a, size=19, weight='bold')
        wrapped(s, x + bw / 2, by1 - 0.8, bw - 0.4, b, 16, ha='center', va='top')
        wrapped(s, x + bw / 2, by0 + 0.4, bw - 0.4, c, 16, weight='bold', color=RED if i == 2 else INK, ha='center')
        if i < n - 1:
            s.arrow(x + bw + 0.05, (by0 + by1) / 2, x + bw + gap - 0.05, (by0 + by1) / 2, lw=2.4, head=16)
    s.brace(0.1, 0.1 + 2 * bw + gap, 1.45, depth=0.18, up=True)
    s.text((0.1 + 0.1 + 2 * bw + gap) / 2, 1.0, 'Trained by someone else on a large collection of images (pretrained)', size=16, weight='bold')
    x3 = 0.1 + 2 * (bw + gap)
    s.brace(x3, x3 + bw, 1.45, depth=0.18, up=True)
    s.text(x3 + bw / 2, 1.0, 'Trained by you', size=16, weight='bold', color=RED)
    return s
