"""Figure kinds for sessions 16, 17 and 18 (author F). Registered like kit/diagrams_ml.py; use as visual=dict(kind='f_coin_curve', ...).

Session 16 (maximum likelihood, MAP, bias-variance)
  f_coin_curve   k, n, mode ('lik' | 'loglik' | 'both'), marks, best      the likelihood (or log-likelihood) of k heads in n flips against p
  f_underflow    (none)                                                   log10 of a product of fair-coin probabilities against the number of flips
  f_gauss_noise  (none)                                                   a line with Gaussian noise drawn as bell curves
  f_gauss_scan   xs, ys, best, data                                       log-likelihood against mu, with the data strip
  f_ce_curve     marks                                                    the loss -ln(p) against the probability given to the true answer
  f_panels_bars  labels, panels [{title, values, hl, note}]               small bar charts side by side (likelihood, prior, posterior)
  f_penalty      lam                                                      squared error, penalty and their sum against one weight
  f_bv_sim       (none)                                                   three polynomial fits repeated over 300 training sets
  f_bv_stack     degrees, bias2, variance, noise                          stacked bars of expected error
  f_tokens       tokens, probs, base, rows                                a sentence with the model's probability and surprise for every token
Session 17 and 18 kinds are added below.
"""
import importlib.util
import math
from pathlib import Path

import numpy as np

import slidekit as K
from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, PALE, fig

LABS = Path(__file__).resolve().parents[1] / 'content' / 'labs'
_NS = {}


def lab_ns(num):
    """Variables of the solution notebook of session `num` (cached)."""
    if num not in _NS:
        spec = importlib.util.spec_from_file_location(f's{num:02d}_nb_fig', LABS / f's{num:02d}_nb.py')
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        _NS[num] = m.namespace()
    return _NS[num]


def _lin(lo, hi, a, b):
    return lambda v: a + (v - lo) / (hi - lo) * (b - a)


def _axes(s, x0, x1, y0, y1, xlabel='', ylabel='', size=16, xl_y=None, yl_x=None):
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    if xlabel:
        s.text((x0 + x1) / 2, xl_y if xl_y is not None else y0 - 0.62, xlabel, size=size, color=MUTE)
    if ylabel:
        s.text(yl_x if yl_x is not None else x0 - 0.78, (y0 + y1) / 2, ylabel, size=size, color=MUTE, rot=90)


def _xticks(s, px, vals, labels, y0, size=14):
    for v, lab in zip(vals, labels):
        s.line(px(v), y0, px(v), y0 - 0.08, color=INK, lw=1.4)
        s.text(px(v), y0 - 0.27, lab, size=size, color=GREY)


def _yticks(s, py, vals, labels, x0, size=14):
    for v, lab in zip(vals, labels):
        s.line(x0, py(v), x0 - 0.08, py(v), color=INK, lw=1.4)
        s.text(x0 - 0.14, py(v), lab, size=size, color=GREY, ha='right')


# ------------------------------------------------------------------ session 16
def _coin_panel(s, ox, oy, pw, ph, k, n, mode, marks, best, size):
    x0, x1, y0, y1 = ox + 1.45, ox + pw - 0.3, oy + 0.95, oy + ph - 0.45
    ps = np.linspace(0.02, 0.98, 120)
    if mode == 'lik':
        f = lambda p: p ** k * (1 - p) ** (n - k)
        lo, hi = 0.0, f(k / n) * 1.3
        ylab, ytv = 'likelihood L(p)', [0, f(k / n)]
        ytl = ['0', f'{f(k / n):.4f}']
        fmt = lambda v: f'{v:.5f}'.rstrip('0')
    else:
        f = lambda p: k * math.log(p) + (n - k) * math.log(1 - p)
        lo, hi = -22.0, f(k / n) + 3.0
        ylab, ytv = 'log-likelihood ln L(p)', [f(k / n), -10, -15]
        ytl = [f'{f(k / n):.2f}', '-10', '-15']
        fmt = lambda v: f'{v:.2f}'
    px = _lin(0, 1, x0, x1)
    py = _lin(lo, hi, y0, y1)
    _axes(s, x0, x1, y0, y1, 'p, the chance of heads', ylab, size, xl_y=oy + 0.22, yl_x=ox + 0.3)
    _xticks(s, px, [0, 0.5, 1], ['0', '0.5', '1'], y0)
    _yticks(s, py, ytv, ytl, x0)
    ps = [p for p in ps if f(p) >= lo]
    s.ax.plot([px(p) for p in ps], [py(f(p)) for p in ps], color=INK, lw=3.2, zorder=3)
    for p in marks:
        hit = abs(p - best) < 1e-9
        s.line(px(p), y0, px(p), py(f(p)), color=RED if hit else GREY, lw=2.0 if hit else 1.4, dash=not hit, z=2)
        s.circle(px(p), py(f(p)), 0.11 if hit else 0.085, fill=GOLD if hit else PAPER, edge=INK, lw=1.8, z=5)
        if not hit:
            s.text(px(p) + 0.17, py(f(p)) + 0.2, f'p = {p:g}', size=14, color=BODY, ha='left')
    if best is not None:
        s.text(px(best) + 0.2, py(f(best)) + 0.12, (f'maximum at\np = {best:g}' if pw > 6.5 else f'p = {best:g}'), size=size - 1, color=RED, weight='bold', ha='left')
    return fmt


@fig('x_f_coin_curve')
def f_coin_curve(w, h, k=7, n=10, mode='lik', marks=(0.5, 0.7, 0.9), best=0.7, size=16, **_):
    s = Scene(w, h)
    if mode == 'both':
        _coin_panel(s, 0, 0, w / 2, h, k, n, 'lik', [best], best, size)
        _coin_panel(s, w / 2, 0, w / 2, h, k, n, 'loglik', [best], best, size)
    else:
        _coin_panel(s, 0, 0, w, h, k, n, mode, marks, best, size)
    return s


@fig('x_f_underflow')
def f_underflow(w, h, size=16, **_):
    s = Scene(w, h)
    x0, x1, y0, y1 = 1.35, w - 0.3, 0.95, h - 0.45
    px = _lin(0, 1200, x0, x1)
    py = _lin(-450, 0, y0, y1)
    _axes(s, x0, x1, y0, y1, 'number of coin flips', 'log10 of the likelihood', size, xl_y=0.22, yl_x=0.3)
    _xticks(s, px, [0, 400, 800, 1200], ['0', '400', '800', '1200'], y0)
    _yticks(s, py, [0, -100, -200, -300], ['0', '-100', '-200', '-300'], x0)
    s.ax.plot([px(0), px(1200)], [py(0), py(-0.30103 * 1200)], color=INK, lw=3.2, zorder=3)
    s.ax.plot([x0, x1], [py(-324), py(-324)], color=RED, lw=2.4, ls='--', zorder=3)
    s.text(x0 + 0.2, py(-324) - 0.3, 'below this line a computer stores 0', size=size - 1, color=RED, weight='bold', ha='left')
    for n_, lab, dy in ((10, '10 flips', 0.4), (100, '100 flips', 0.4), (1100, '1,100 flips', 0.35)):
        v = -0.30103 * n_
        s.circle(px(n_), py(v), 0.1, fill=GOLD, edge=INK, lw=1.8, z=5)
    s.text(px(10) + 0.2, py(-3) + 0.35, '10 flips: 0.001', size=size - 2, ha='left')
    s.text(px(100) + 0.25, py(-30) + 0.15, '100 flips: 0.0000...(30 zeros)', size=size - 2, ha='left')
    s.text(px(1100), py(-331) - 0.5, '1,100 flips', size=size - 2, ha='center', weight='bold')
    return s


@fig('x_f_gauss_noise')
def f_gauss_noise(w, h, size=16, **_):
    s = Scene(w, h)
    x0, x1, y0, y1 = 1.1, w - 0.3, 0.95, h - 0.3
    px = _lin(0.3, 5.9, x0, x1)
    py = _lin(0, 12, y0, y1)
    _axes(s, x0, x1, y0, y1, 'x, the input', 'y, the target', size, xl_y=0.22, yl_x=0.3)
    xs = np.array([1, 2, 3, 4, 5.])
    ys = np.array([3.1, 4.0, 7.2, 8.2, 11.0])
    f = lambda x: 0.5 + 2 * x
    for cx in (2, 4):
        t = np.linspace(-1.8, 1.8, 60)
        pdf = np.exp(-t ** 2 / (2 * 0.6 ** 2))
        xs_b = [px(cx + 0.55 * v) for v in pdf]
        ys_b = [py(f(cx) + tv) for tv in t]
        s.ax.fill_betweenx(ys_b, [px(cx)] * len(t), xs_b, color=GOLD, alpha=0.55, zorder=2, lw=0)
        s.ax.plot(xs_b, ys_b, color=INK, lw=1.8, zorder=3)
    s.ax.plot([px(0.4), px(5.7)], [py(f(0.4)), py(f(5.7))], color=RED, lw=3.4, zorder=4)
    for x, y in zip(xs, ys):
        s.line(px(x), py(y), px(x), py(f(x)), color=BODY, lw=1.6, dash=True, z=3)
        s.circle(px(x), py(y), 0.1, fill=INK, edge=INK, lw=1, z=6)
    s.text(px(0.55), py(f(5.7)) - 0.55, 'the model: y-hat = 0.5 + 2x', size=size, color=RED, weight='bold', ha='left')
    s.text(px(4.35), py(3.2), 'Gaussian noise:\nmost points sit\nnear the line', size=size - 1, color=INK, ha='left')
    s.text(px(0.45), py(1.0), 'dashed = residual, y - y-hat', size=size - 2, color=BODY, ha='left')
    return s


@fig('x_f_gauss_scan')
def f_gauss_scan(w, h, xs=(), ys=(), best=None, data=(), size=16, **_):
    s = Scene(w, h)
    x0, x1, y0, y1 = 1.45, w - 0.3, 0.95, h - 1.1
    lo, hi = min(xs) - 0.1, max(xs) + 0.1
    px = _lin(lo, hi, x0, x1)
    ylo, yhi = min(ys) - 1.2, max(ys) + 1.2
    py = _lin(ylo, yhi, y0, y1)
    _axes(s, x0, x1, y0, y1, 'mu, the mean we try (mm)', 'log-likelihood', size, xl_y=0.22, yl_x=0.3)
    _xticks(s, px, [9, 10, 11], ['9', '10', '11'], y0)
    _yticks(s, py, [round(max(ys), 2), -12, -16], [f'{max(ys):.2f}', '-12', '-16'], x0)
    s.ax.plot([px(v) for v in xs], [py(v) for v in ys], color=INK, lw=3, zorder=3)
    for v, y in zip(xs, ys):
        hit = best is not None and abs(v - best) < 1e-9
        s.circle(px(v), py(y), 0.11 if hit else 0.07, fill=GOLD if hit else PAPER, edge=INK, lw=1.6, z=5)
    s.line(px(best), y0, px(best), py(max(ys)), color=RED, lw=2.2, dash=True, z=2)
    s.text(px(best), py(max(ys)) + 0.4, f'best mu = {best:g}', size=size, color=RED, weight='bold')
    ty = h - 0.3
    s.line(x0, ty, x1, ty, color=HAIR, lw=1.4)
    for d in data:
        s.circle(px(d), ty, 0.09, fill=INK, edge=INK, lw=1, z=5)
    s.text(x0, ty - 0.33, 'the 8 measurements', size=size - 2, color=BODY, ha='left')
    return s


@fig('x_f_ce_curve')
def f_ce_curve(w, h, marks=(0.9, 0.5, 0.1), size=16, **_):
    s = Scene(w, h)
    x0, x1, y0, y1 = 1.45, w - 0.3, 0.95, h - 0.4
    px = _lin(0, 1, x0, x1)
    py = _lin(0, 3.6, y0, y1)
    _axes(s, x0, x1, y0, y1, 'probability the model gave to the true answer', 'loss = -ln(p)', size, xl_y=0.22, yl_x=0.3)
    _xticks(s, px, [0, 0.5, 1], ['0', '0.5', '1'], y0)
    _yticks(s, py, [0, 1, 2, 3], ['0', '1', '2', '3'], x0)
    ps = np.linspace(0.027, 1, 120)
    s.ax.plot([px(p) for p in ps], [py(-math.log(p)) for p in ps], color=INK, lw=3.2, zorder=3)
    for p in marks:
        v = -math.log(p)
        s.circle(px(p), py(v), 0.1, fill=GOLD if p == min(marks) else PAPER, edge=INK, lw=1.8, z=5)
        s.text(px(p) + (0.05 if p > 0.7 else 0.2), py(v) + 1.0 if p > 0.7 else py(v) + 0.15, f'p = {p:g}: loss {v:.2f}', size=size - 2, ha='right' if p > 0.7 else 'left', color=RED if p == min(marks) else INK, weight='bold' if p == min(marks) else 'normal')
    return s


@fig('x_f_panels_bars')
def f_panels_bars(w, h, labels=(), panels=(), size=16, ymax=None, **_):
    """Small bar charts side by side. A panel may carry its own labels, signed values and value labels (show: True)."""
    s = Scene(w, h)
    n = len(panels)
    pw = (w - 0.1) / n
    for i, pn in enumerate(panels):
        ox = 0.05 + i * pw
        x0, x1 = ox + 0.2, ox + pw - 0.25
        top_y = h - 1.05
        s.text((x0 + x1) / 2, h - 0.35, pn['title'], size=size + 1, weight='bold')
        if pn.get('note'):
            s.text((x0 + x1) / 2, h - 0.72, pn['note'], size=size - 2, color=MUTE)
        vals = pn['values']
        labs = pn.get('labels', labels)
        m = len(vals)
        bw = (x1 - x0) / m
        vmax, vmin = (ymax if ymax else max(max(vals), 0.0) * 1.08), min(min(vals), 0.0) * 1.08
        show = pn.get('show', False)
        room = 0.4 if show else 0.0
        low = 0.75 + (0.4 if vmin < 0 and show else 0.0)
        y_lo, y_hi = low, top_y - room
        py = _lin(vmin, vmax, y_lo, y_hi)
        base = py(0.0)
        for j, v in enumerate(vals):
            hit = pn.get('hl') == j
            ytop, ybot = (py(v), base) if v >= 0 else (base, py(v))
            s.rect(x0 + j * bw + 0.04, ybot, bw - 0.08, max(ytop - ybot, 0.012), fill=GOLD if hit else PALE, edge=INK, lw=1.4, z=3)
            s.text(x0 + j * bw + bw / 2, 0.45, labs[j], size=14, color=GREY)
            if show:
                fmt = pn.get('fmt', '{:.3f}')
                s.text(x0 + j * bw + bw / 2, (ytop + 0.24) if v >= 0 else (ybot - 0.24), fmt.format(v), size=size - 2, color=RED if hit else INK, weight='bold' if hit else 'normal')
        s.line(x0, base, x1, base, color=INK, lw=2)
        if pn.get('hl') is not None and pn.get('best_label'):
            j = pn['hl']
            v = vals[j]
            s.text(x0 + j * bw + bw / 2, py(v) + 0.3, pn['best_label'], size=size - 2, color=RED, weight='bold')
    return s


@fig('x_f_bits_bars')
def f_bits_bars(w, h, items=(), size=16, **_):
    """items: [{label, p, bits}] drawn as horizontal bars, one per event."""
    s = Scene(w, h)
    lab_w = 3.6
    x0, x1 = lab_w + 0.1, w - 0.3
    top = max(i['bits'] for i in items) * 1.3
    px = _lin(0, top, x0, x1)
    n = len(items)
    rh = (h - 0.9) / n
    for k, it in enumerate(items):
        yc = h - 0.3 - (k + 0.5) * rh
        s.text(0.05, yc + 0.2, it['label'], size=size, weight='bold', ha='left')
        s.text(0.05, yc - 0.2, it['p'], size=size - 1, color=MUTE, ha='left')
        s.rect(x0, yc - 0.28, px(it['bits']) - x0, 0.56, fill=GOLD if it.get('hl') else PALE, edge=INK, lw=1.6, z=3)
        s.text(px(it['bits']) + 0.15, yc, f"{it['bits']:g} " + ('bit' if it['bits'] == 1 else 'bits'), size=size, weight='bold', ha='left')
    s.line(x0, 0.45, x0, h - 0.3, color=INK, lw=2)
    s.text((x0 + x1) / 2, 0.2, 'surprise = -log2(p), in bits', size=size - 1, color=MUTE)
    return s


@fig('x_f_ce_kl')
def f_ce_kl(w, h, rows=(), entropy=0.0, size=16, **_):
    """rows: [{label, ce}] ; each bar is the entropy (pale) plus the KL divergence (red) = the cross-entropy."""
    s = Scene(w, h)
    lab_w = 3.5
    x0, x1 = lab_w + 0.1, w - 0.2
    top = max(r['ce'] for r in rows) * 1.28
    px = _lin(0, top, x0, x1)
    n = len(rows)
    rh = (h - 1.2) / n
    for k, r in enumerate(rows):
        yc = h - 0.3 - (k + 0.5) * rh
        s.text(0.05, yc, r['label'], size=size, weight='bold', ha='left')
        s.rect(x0, yc - 0.3, px(entropy) - x0, 0.6, fill=PALE, edge=INK, lw=1.6, z=3)
        kl = r['ce'] - entropy
        if kl > 1e-9:
            s.rect(px(entropy), yc - 0.3, max(px(r['ce']) - px(entropy), 0.02), 0.6, fill=RED, edge=INK, lw=1.6, z=3)
        s.text(px(r['ce']) + 0.15, yc + 0.0, f"{r['ce']:.3f}", size=size, weight='bold', ha='left')
        if kl > 1e-9:
            s.text(px(r['ce']) + 0.15, yc - 0.45, f'KL = {kl:.3f}', size=size - 2, color=RED, ha='left')
    s.line(x0, 0.75, x0, h - 0.3, color=INK, lw=2)
    s.rect(x0, 0.2, 0.28, 0.28, fill=PALE, edge=INK, lw=1.4)
    s.text(x0 + 0.4, 0.34, f'entropy {entropy:.2f} (cannot be removed)', size=size - 2, ha='left')
    s.rect(x0 + 4.7, 0.2, 0.28, 0.28, fill=RED, edge=INK, lw=1.4)
    s.text(x0 + 5.1, 0.34, 'KL divergence (the model\'s excess)', size=size - 2, ha='left')
    return s


@fig('x_f_penalty')
def f_penalty(w, h, lam=5, size=16, **_):
    s = Scene(w, h)
    x0, x1, y0, y1 = 1.3, w - 0.3, 0.95, h - 0.4
    px = _lin(0, 3, x0, x1)
    py = _lin(0, 60, y0, y1)
    _axes(s, x0, x1, y0, y1, 'w, the weight', 'loss', size, xl_y=0.22, yl_x=0.3)
    _xticks(s, px, [0, 1, 2, 3], ['0', '1', '2', '3'], y0)
    ws = np.linspace(0, 3, 100)
    sse = lambda v: 58.06 - 57 * v + 14 * v ** 2
    pen = lambda v: lam * v ** 2
    tot = lambda v: sse(v) + pen(v)
    for fn, col, lw_, ls in ((sse, INK, 3.0, '-'), (pen, GREY, 2.6, '--'), (tot, RED, 3.4, '-')):
        pts = [(px(v), py(fn(v))) for v in ws if fn(v) <= 60]
        s.ax.plot([a for a, b in pts], [b for a, b in pts], color=col, lw=lw_, ls=ls, zorder=3)
    w_mle, w_map = 28.5 / 14, 28.5 / (14 + lam)
    for v, c in ((w_mle, INK), (w_map, RED)):
        s.line(px(v), y0, px(v), py(tot(v)) if c == RED else py(sse(v)), color=c, lw=1.8, dash=True)
        s.circle(px(v), py(tot(v)) if c == RED else py(sse(v)), 0.1, fill=GOLD, edge=INK, lw=1.8, z=5)
    for j, (lab, col, ls) in enumerate((('squared error: lowest at w = %.2f' % w_mle, INK, '-'), ('penalty $%g\\,w^2$' % lam, GREY, '--'), ('sum: lowest at w = %.2f' % w_map, RED, '-'))):
        yy = py(57) - j * 0.42
        s.ax.plot([px(0.95), px(1.2)], [yy, yy], color=col, lw=3, ls=ls, zorder=5)
        s.text(px(1.27), yy, lab, size=size - 1, ha='left', color=col if col != GREY else BODY)
    return s


@fig('x_f_bv_sim')
def f_bv_sim(w, h, size=16, **_):
    ns = lab_ns(16)
    s = Scene(w, h)
    pw = (w - 0.1) / 3
    xx = np.linspace(0, 1, 100)
    for i, d in enumerate(ns['degrees']):
        ox = 0.05 + i * pw
        x0, x1, y0, y1 = ox + 0.2, ox + pw - 0.2, 1.05, h - 0.75
        px = _lin(0, 1, x0, x1)
        py = _lin(-2, 2, y0, y1)
        s.rect(x0, y0, x1 - x0, y1 - y0, fill=PAPER, edge=INK, lw=1.4)
        s.text((x0 + x1) / 2, h - 0.4, ['A straight line (degree 1)', 'A cubic (degree 3)', 'Degree 9'][i], size=size + 1, weight='bold')
        for r in range(30):
            s.ax.plot([px(v) for v in ns['x_test']], [py(float(np.clip(v, -2, 2))) for v in ns['preds'][d][r]], color=GREY, alpha=0.45, lw=1.1, zorder=2)
        s.ax.plot([px(v) for v in xx], [py(v) for v in ns['true_f'](xx)], color=RED, lw=3.2, zorder=4)
        s.ax.plot([px(v) for v in ns['x_test']], [py(float(v)) for v in ns['preds'][d].mean(axis=0)], color=INK, lw=3.0, ls='--', zorder=5)
        s.text((x0 + x1) / 2, 0.68, f'bias squared {ns["bias2"][d]:.3f}', size=size - 1, color=INK)
        s.text((x0 + x1) / 2, 0.3, f'variance {ns["variance"][d]:.3f}', size=size - 1, color=RED, weight='bold')
    return s


@fig('x_f_bv_stack')
def f_bv_stack(w, h, degrees=(), bias2=(), variance=(), noise=0.09, size=16, **_):
    s = Scene(w, h)
    x0, x1, y0, y1 = 1.1, w - 3.3, 0.9, h - 0.5
    top = 1.0
    py = _lin(0, top, y0, y1)
    n = len(degrees)
    bw = (x1 - x0) / n
    _axes(s, x0, x1, y0, y1, '', 'expected error', size, yl_x=0.3)
    _yticks(s, py, [0, 0.5, 1.0], ['0', '0.5', '1.0'], x0)
    for i, d in enumerate(degrees):
        bx = x0 + i * bw + bw * 0.2
        ww = bw * 0.6
        acc = 0.0
        for v, col in ((bias2[i], RED), (variance[i], GOLD), (noise, PALE)):
            s.rect(bx, py(acc), ww, max(py(acc + v) - py(acc), 0.01), fill=col, edge=INK, lw=1.4, z=3)
            acc += v
        s.text(bx + ww / 2, py(acc) + 0.28, f'{acc:.3f}', size=size, weight='bold')
        s.text(bx + ww / 2, y0 - 0.3, f'degree {d}', size=size)
    lx = x1 + 0.35
    for j, (lab, col) in enumerate((('bias squared', RED), ('variance', GOLD), ('noise (fixed)', PALE))):
        yy = y1 - 0.5 - j * 0.75
        s.rect(lx, yy - 0.16, 0.32, 0.32, fill=col, edge=INK, lw=1.4)
        s.text(lx + 0.45, yy, lab, size=size - 1, ha='left')
    return s


@fig('x_f_tokens')
def f_tokens(w, h, tokens=(), probs=(), base='e', total_label='', size=16, **_):
    s = Scene(w, h)
    n = len(tokens)
    lab_w = 2.7
    tot_w = 1.9
    cw = (w - lab_w - tot_w - 0.1) / n
    unit = 'ln' if base == 'e' else 'log2'
    f = (lambda p: -math.log(p)) if base == 'e' else (lambda p: -math.log2(p))
    ys = [h - 0.7, h - 1.75, h - 2.65]
    s.text(0.05, ys[0], 'the next word', size=size, color=MUTE, ha='left')
    s.text(0.05, ys[1], 'probability the\nmodel gave it', size=size, color=MUTE, ha='left')
    s.text(0.05, ys[2], f'-{unit}(p)', size=size, color=MUTE, ha='left')
    for i, (t, p) in enumerate(zip(tokens, probs)):
        cx = lab_w + i * cw
        s.box(cx + 0.06, ys[0] - 0.32, cw - 0.12, 0.64, t, size=size + 2, fill=PAPER, edge=INK, lw=1.8, weight='bold')
        s.text(cx + cw / 2, ys[1], f'{p:g}', size=size + 2)
        s.text(cx + cw / 2, ys[2], f'{f(p):.2f}', size=size + 2, color=RED, weight='bold')
        if i < n - 1:
            pass
    tx = lab_w + n * cw
    s.text(tx + tot_w / 2, ys[0], 'total', size=size, color=MUTE)
    tot = sum(f(p) for p in probs)
    s.box(tx + 0.1, ys[2] - 0.36, tot_w - 0.2, 0.72, f'{tot:.2f}', size=size + 4, fill=GOLD, edge=INK, lw=2, weight='bold')
    if total_label:
        s.text(w / 2, 0.45, total_label, size=size, color=BODY)
    return s


# ------------------------------------------------------------------ session 18
def _blend(t):
    """White to gold, t in 0..1."""
    a, b = (255, 255, 255), (0xE0, 0xBE, 0x36)
    return '#%02X%02X%02X' % tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


@fig('x_f_attention')
def f_attention(w, h, tokens=(), weights=(), outputs=(), note='', size=16, **_):
    """Attention weights as a grid: row = the token that asks (query), column = the token it reads from (key). Darker gold = larger weight. Right: the output row."""
    s = Scene(w, h)
    n = len(tokens)
    cw, ch = 1.45, 0.78
    gx = 3.3
    gy_top = h - 1.35
    s.text(gx + n * cw / 2, h - 0.3, 'columns = key tokens (being read)', size=size, color=MUTE)
    s.text(0.05, h - 0.3, 'rows = query tokens (asking)', size=size, color=MUTE, ha='left')
    for j, t in enumerate(tokens):
        s.text(gx + j * cw + cw / 2, h - 0.8, t, size=size, weight='bold')
    for i, t in enumerate(tokens):
        y = gy_top - (i + 1) * ch
        s.text(gx - 0.2, y + ch / 2, t, size=size, weight='bold', ha='right')
        for j in range(n):
            v = weights[i][j]
            s.rect(gx + j * cw, y, cw, ch, fill=_blend(min(1.0, v / 0.7)), edge=INK, lw=1.4, z=2)
            s.text(gx + j * cw + cw / 2, y + ch / 2, f'{v:.3f}', size=size + 1, weight='bold' if v == max(weights[i]) else 'normal')
        ox = gx + n * cw + 0.55
        s.arrow(gx + n * cw + 0.08, y + ch / 2, ox - 0.1, y + ch / 2, lw=2.0, head=14)
        s.text(ox, y + ch / 2, '(' + ', '.join(f'{v:.2f}' for v in outputs[i]) + ')', size=size, ha='left')
    s.text(gx + n * cw + 0.55, h - 0.8, 'output = weights × V', size=size, weight='bold', ha='left')
    s.text(w / 2, 0.38, note, size=size, color=BODY)
    return s


@fig('x_f_network')
def f_network(w, h, layers=(('Inputs', 2), ('Hidden (tanh)', 4), ('Output', 1)), size=16, **_):
    """Same picture as the shared network figure, with the backward arrow labelled by the industry term (error signal) instead of 'blame'."""
    s = Scene(w, h)
    n = len(layers)
    xs = [0.9 + i * (w - 1.8) / (n - 1) for i in range(n)]
    pos = []
    for (nm, k), x in zip(layers, xs):
        pos.append([(x, 0.95 + (h - 2.55) * (j + 0.5) / k) for j in range(k)])
        s.text(x, h - 0.35, nm, size=size, weight='bold')
    for a, b in zip(pos, pos[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b:
                s.line(x1, y1, x2, y2, color=HAIR, lw=1.2, z=1)
    for col in pos:
        for (x, y) in col:
            s.circle(x, y, 0.2, fill=PAPER, edge=INK, lw=2, z=4)
    s.circle(pos[-1][0][0], pos[-1][0][1], 0.26, fill=GOLD, edge=INK, lw=2.4, z=5)
    s.arrow(xs[0] + 0.3, 0.38, xs[-1] - 0.3, 0.38, color=INK, lw=2.4, head=16)
    s.text((xs[0] + xs[-1]) / 2, 0.1, 'forward: the guess', size=size, color=INK)
    s.arrow(xs[-1] - 0.3, h - 1.2, xs[0] + 0.3, h - 1.2, color=RED, lw=2.4, head=16)
    s.text((xs[0] + xs[-1]) / 2, h - 0.85, 'backward: pass the error signal back, then adjust each weight', size=size, color=RED, weight='bold')
    return s
