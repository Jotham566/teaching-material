"""Figure kinds for Session 3 (Measuring a model). Numbers come from demo_runs/s03/results.json (a real recorded run of demo_runs/s03/s03_measure.py).

Kinds (use as dict(kind='t03_<name>')): dots, baselines, confusion, net, f1, hist, thresholds, roc, cost, memorise, cases, blank
"""
import json
import math
from pathlib import Path

import numpy as np

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD, fig
import slidekit as K

_R = json.loads((Path(__file__).resolve().parent.parent / 'demo_runs' / 's03' / 'results.json').read_text())
TT = _R['threshold_table']
N_TEST, N_LATE = _R['n_test'], _R['late_test']
N_OK = N_TEST - N_LATE


def _pct(x, d=0):
    return f'{100 * x:.{d}f}%'


def _row(t):
    return next(r for r in TT if abs(r['threshold'] - t) < 1e-9)


# ------------------------------------------------------------------ 1. always say "on time"
@fig('x_t03_dots')
def dots(w, h, **_):
    s = Scene(w, h)
    n, cols = 100, 10
    gx, gy, d = 0.35, 0.45, 0.34
    late = {3, 17, 26, 38, 44, 59, 71, 83, 96}   # 9 of every 100, spread out (the real rate is 83 of 900, 9.2 percent)
    for i in range(n):
        r, c = divmod(i, cols)
        x = gx + c * d + d / 2
        y = h - 0.55 - r * d - d / 2
        s.circle(x, y, 0.115, fill=RED if i in late else HAIR, edge=RED if i in late else GREY, lw=1.2)
    s.text(gx + cols * d / 2, 0.25, 'Red = late. Real run: 83 late of 900', size=14, color=MUTE)
    x0 = gx + cols * d + 0.55
    cw = w - x0 - 0.1
    s.box(x0, h - 2.2, cw, 1.6, '', fill=PAPER, edge=INK, lw=2)
    s.text(x0 + cw / 2, h - 0.95, 'Say "on time" for all', size=18, weight='bold')
    s.text(x0 + cw / 2, h - 1.65, _pct(_R['always_no']['accuracy'], 1) + ' right', size=30, weight='bold')
    s.box(x0, h - 4.05, cw, 1.6, '', fill=GOLD, edge=INK, lw=2)
    s.text(x0 + cw / 2, h - 2.85, 'Late invoices caught', size=18, weight='bold')
    s.text(x0 + cw / 2, h - 3.5, '0 of 83', size=30, weight='bold')
    return s


# ------------------------------------------------------------------ 2. baselines
def _baseline_chart(w, h, ents):
    s = Scene(w, h)
    cols = [('Accuracy', INK), ('Precision', GOLD), ('Recall', RED)]
    x_lab, x0, x1 = 0.1, 2.15, w - 0.65
    gh = (h - 0.95) / len(ents)
    for gi, (name, acc, pr, rc) in enumerate(ents):
        top = h - 0.15 - gi * gh
        s.text(x_lab, top - gh / 2, name, size=16, weight='bold', ha='left')
        for bi, (val, (cn, cc)) in enumerate(zip((acc, pr, rc), cols)):
            bh = 0.27
            y = top - 0.18 - (bi + 1) * (bh + 0.1) + 0.1
            if val is None:
                s.text(x0 + 0.05, y + bh / 2, 'none flagged, so no precision', size=14, color=MUTE, ha='left')
                continue
            s.rect(x0, y, max(0.03, val * (x1 - x0)), bh, fill=cc, edge=INK, lw=1.2)
            s.text(x0 + val * (x1 - x0) + 0.08, y + bh / 2, _pct(val, 1 if cn == 'Accuracy' and abs(val * 100 - round(val * 100)) > 1e-9 else 0), size=14, weight='bold', ha='left')
    ly = 0.3
    xx = x0
    for cn, cc in cols:
        s.rect(xx, ly - 0.1, 0.25, 0.2, fill=cc, edge=INK, lw=1)
        s.text(xx + 0.33, ly, cn, size=14, ha='left')
        xx += 1.75
    s.line(x0, 0.62, x0, h - 0.1, color=INK, lw=1.4)
    return s


@fig('x_t03_baselines')
def baselines(w, h, **_):
    rr = _row(0.2)
    return _baseline_chart(w, h, [('Majority-class\nbaseline', _R['always_no']['accuracy'], None, 0.0),
                                  ('Rule: paid late\nlast year', _R['rule']['accuracy'], _R['rule']['precision'], _R['rule']['recall']),
                                  ('Model, flag at\n0.20 or more', rr['accuracy'], rr['precision'], rr['recall'])])


@fig('x_t03_alarm_base')
def alarm_base(w, h, **_):
    return _baseline_chart(w, h, [('Alarm that\nnever rings\n(majority class)', 0.98, None, 0.0), ('Our alarm\n(16 of 20 fires)', 0.962, 0.32, 0.80)])


# ------------------------------------------------------------------ 3. confusion table with real counts
def _matrix(w, h, vals, rows, cols, descs, hl='tp', size=17):
    """2 x 2 confusion matrix. vals = (TP, FP, FN, TN); rows = (top, bottom) labels; cols = (left, right) labels."""
    s = Scene(w, h)
    lw_, top = 1.9, 0.8
    cw = (w - lw_ - 0.1) / 2
    ch = (h - top - 0.1) / 2
    x0 = lw_
    s.text(x0 + cw / 2, h - 0.4, cols[0], size=size, weight='bold')
    s.text(x0 + cw * 1.5, h - 0.4, cols[1], size=size, weight='bold')
    s.text(lw_ / 2, 0.1 + ch * 1.5, rows[0], size=size, weight='bold')
    s.text(lw_ / 2, 0.1 + ch * 0.5, rows[1], size=size, weight='bold')
    gold = {'tp': {'tp'}, 'precision': {'tp', 'fp'}, 'recall': {'tp', 'fn'}}[hl]
    cells = [(0, 1, vals[0], 'True positive (TP)', 'tp'), (1, 1, vals[1], 'False positive (FP)', 'fp'), (0, 0, vals[2], 'False negative (FN)', 'fn'), (1, 0, vals[3], 'True negative (TN)', 'tn')]
    for (cx, cy, n, nm, key), d in zip(cells, descs):
        x = x0 + cx * cw + 0.05
        y = 0.1 + cy * ch + 0.05
        s.box(x, y, cw - 0.1, ch - 0.1, '', fill=GOLD if key in gold else PAPER, edge=INK, lw=2.0, r=0.06)
        s.text(x + (cw - 0.1) / 2, y + (ch - 0.1) * 0.72, f'{n:,}', size=34, weight='bold', color=RED if key == 'fn' else INK)
        s.text(x + (cw - 0.1) / 2, y + (ch - 0.1) * 0.37, nm, size=size - 1, weight='bold', color=INK)
        s.text(x + (cw - 0.1) / 2, y + (ch - 0.1) * 0.16, d, size=14, color=BODY)
    return s


@fig('x_t03_confusion')
def confusion(w, h, t=0.2, size=17, **_):
    r = _row(t)
    return _matrix(w, h, (r['tp'], r['fp'], r['fn'], r['tn']), ('Model said\n"late"', 'Model said\n"on time"'), ('Really late', 'Really on time'),
                   ('caught', 'false alarm', 'missed', 'rightly cleared'), hl='tp', size=size)


@fig('x_t03_alarm')
def alarm(w, h, hl='tp', size=17, **_):
    return _matrix(w, h, (16, 34, 4, 946), ('Alarm\nrang', 'Alarm\nsilent'), ('Real fire', 'No fire'),
                   ('rang, fire', 'rang, no fire', 'silent, fire', 'silent, no fire'), hl=hl, size=size)


@fig('x_t03_alarm_thr')
def alarm_thr(w, h, **_):
    s = Scene(w, h)
    x0, x1, y0, y1 = 0.5, w - 0.3, 0.95, h - 0.9
    px = lambda v: x0 + v / 10 * (x1 - x0)
    xs = np.linspace(0, 10, 200)
    def curve(m, sd):
        return np.exp(-0.5 * ((xs - m) / sd) ** 2)
    for m, sd, col, ec in ((3.0, 1.1, HAIR, GREY), (6.6, 1.2, RED, RED)):
        ys = y0 + curve(m, sd) * (y1 - y0 - 0.3)
        s.ax.fill_between([px(v) for v in xs], y0, ys, color=col, alpha=0.75 if col == RED else 1.0, ec=ec, lw=1.5, zorder=2)
    s.line(x0, y0, x1, y0, lw=2)
    s.text((x0 + x1) / 2, 0.3, 'smoke level the alarm senses (a score from 0 to 10)', size=14, color=MUTE)
    s.text(px(1.6), y0 + 1.2, 'No fire:\ncooking, toast', size=15, weight='bold')
    s.text(px(8.6), y0 + 1.2, 'Real\nfire', size=15, weight='bold')
    for v, lab in ((7.4, 'High\nthreshold'), (5.0, 'Our\nsetting'), (3.6, 'Low\nthreshold')):
        s.line(px(v), y0, px(v), y1 + 0.05, color=INK, lw=2.4, dash=True, z=5)
        s.text(px(v), y1 + 0.45, lab, size=14, weight='bold')
    return s


# ------------------------------------------------------------------ 4. high and low threshold (an illustration)
def _field():
    rng = np.random.default_rng(11)
    red = [(2.6 + rng.normal(0, 0.55), 2.05 + rng.normal(0, 0.55)) for _ in range(8)]
    grey = []
    while len(grey) < 30:
        p = (rng.uniform(0.2, 5.0), rng.uniform(0.2, 3.7))
        if all(math.dist(p, q) > 0.38 for q in red + grey):
            grey.append(p)
    return red, grey


@fig('x_t03_net')
def net(w, h, **_):
    s = Scene(w, h)
    red, grey = _field()
    cx, cy = 2.6, 2.05
    pw = (w - 0.3) / 2
    for k, (rad, title) in enumerate(((0.78, 'High threshold: flag fewer'), (1.55, 'Low threshold: flag more'))):
        ox, oy = k * (pw + 0.3), 0.55
        s.rect(ox, oy, pw, h - 1.15, fill=PAPER, edge=INK, lw=1.6)
        sc = (pw - 0.3) / 5.2
        mx = lambda p: (ox + 0.15 + p[0] * sc, oy + 0.1 + p[1] * (h - 1.35) / 3.9)
        flagged_red = sum(1 for p in red if math.dist(p, (cx, cy)) <= rad)
        flagged_grey = sum(1 for p in grey if math.dist(p, (cx, cy)) <= rad)
        for p in grey:
            x, y = mx(p)
            s.circle(x, y, 0.09, fill=HAIR, edge=GREY, lw=1)
        for p in red:
            x, y = mx(p)
            s.circle(x, y, 0.1, fill=RED, edge=RED, lw=1)
        x, y = mx((cx, cy))
        s.ax.add_patch(__import__('matplotlib.patches', fromlist=['Ellipse']).Ellipse((x, y), 2 * rad * sc, 2 * rad * (h - 1.35) / 3.9, fc='none', ec=INK, lw=2.6, ls='--', zorder=5))
        s.text(ox + pw / 2, h - 0.25, title, size=18, weight='bold')
        f = flagged_red + flagged_grey
        s.text(ox + pw / 2, 0.27, f'Precision {flagged_red} of {f}.  Recall {flagged_red} of 8.', size=15, weight='bold')
    return s


# ------------------------------------------------------------------ 5. F1
@fig('x_t03_f1')
def f1(w, h, **_):
    s = Scene(w, h)
    cases = [('Our alarm: precision 32%, recall 80%', 0.32, 0.80), ('Precision 90%, recall 10%', 0.90, 0.10), ('Precision 50%, recall 50%', 0.50, 0.50)]
    x0, x1 = 0.2, w - 0.7
    gh = (h - 0.6) / 3
    for gi, (lab, p, r) in enumerate(cases):
        top = h - 0.1 - gi * gh
        avg = (p + r) / 2
        f = 2 * p * r / (p + r)
        s.text(x0, top - 0.25, lab, size=16, weight='bold', ha='left')
        for bi, (nm, v, col) in enumerate((('Average', avg, HAIR), ('F1', f, GOLD))):
            y = top - 0.62 - bi * 0.5
            s.rect(x0 + 0.0, y - 0.18, max(0.03, v * (x1 - x0 - 1.3)), 0.36, fill=col, edge=INK, lw=1.3)
            s.text(x0 + v * (x1 - x0 - 1.3) + 0.1, y, f'{nm} {_pct(v)}', size=15, weight='bold', ha='left')
    s.text(x0, 0.2, 'F1 = 2PR ÷ (P + R) = 2 ÷ (1/P + 1/R).  P: precision.  R: recall.  The harmonic mean.', size=15, color=BODY, ha='left')
    return s


# ------------------------------------------------------------------ 6. where the invoices score
@fig('x_t03_hist')
def hist(w, h, **_):
    s = Scene(w, h)
    H = _R['hist']
    late = np.array(H['late']) / sum(H['late'])
    ok = np.array(H['on_time']) / sum(H['on_time'])
    x0, x1, y0, y1 = 0.95, w - 0.2, 0.95, h - 0.5
    xmax = 0.8
    px = lambda v: x0 + v / xmax * (x1 - x0)
    ymax = 0.5
    py = lambda v: y0 + v / ymax * (y1 - y0)
    for i in range(16):
        a, b = H['bins'][i], H['bins'][i + 1]
        bw = (px(b) - px(a))
        s.rect(px(a) + 0.01, y0, bw * 0.46, py(ok[i]) - y0, fill=HAIR, edge=GREY, lw=0.8, z=2)
        s.rect(px(a) + 0.01 + bw * 0.48, y0, bw * 0.46, py(late[i]) - y0, fill=RED, edge=RED, lw=0.8, z=2)
    s.line(x0, y0, x1, y0, lw=2)
    s.line(x0, y0, x0, y1, lw=2)
    for v in (0, 0.2, 0.4, 0.6, 0.8):
        s.text(px(v), y0 - 0.25, f'{v:.1f}', size=14)
    s.text((x0 + x1) / 2 + 0.3, 0.22, 'score the model gives an invoice (0 = safe, 1 = surely late)', size=14, color=MUTE)
    s.text(0.28, (y0 + y1) / 2, 'share of its group', size=14, color=MUTE, rot=90)
    for v, lab, yy in ((0.5, 'flag at 0.50', y1 - 0.05), (0.2, 'flag at 0.20', y1 - 0.62), (0.05, '0.05', y1 - 1.2)):
        s.line(px(v), y0, px(v), yy - 0.18, color=INK, lw=2, dash=True, z=4)
        s.text(px(v) + 0.08, yy, lab, size=14, weight='bold', ha='left')
    lx = px(0.53)
    s.rect(lx, y1 - 1.95, 0.25, 0.2, fill=HAIR, edge=GREY, lw=1)
    s.text(lx + 0.35, y1 - 1.85, 'paid on time (817)', size=14, ha='left')
    s.rect(lx, y1 - 2.4, 0.25, 0.2, fill=RED, edge=RED, lw=1)
    s.text(lx + 0.35, y1 - 2.3, 'paid late (83)', size=14, ha='left')
    return s


# ------------------------------------------------------------------ 7. the threshold table (recorded run)
@fig('x_t03_thresholds')
def thresholds(w, h, size=15, **_):
    s = Scene(w, h)
    heads = ['Threshold', 'Flagged', 'True\npositives', 'False\npositives', 'False\nnegatives', 'Precision', 'Recall', 'F1', 'Accuracy']
    rows = [heads, ['no flags\n(baseline)', '0', '0', '0', f'{N_LATE}', 'none', '0%', '0%', _pct(_R['always_no']['accuracy'], 1)]]
    for r in TT:
        rows.append([f"{r['threshold']:.2f}", f"{r['flagged']}", f"{r['tp']}", f"{r['fp']}", f"{r['fn']}", _pct(r['precision']), _pct(r['recall']), _pct(r['f1']), _pct(r['accuracy'], 1)])
    cw = [1.55, 1.1, 1.3, 1.3, 1.35, 1.35, 1.2, 0.95, 1.4]
    sc = (w - 0.1) / sum(cw)
    cw = [c * sc for c in cw]
    rh = (h - 0.1) / len(rows)
    s.table(0.05, h - 0.05, cw, rh, rows, size=size, hl_rows=(4,), hl_fill=GOLD, align=['left'] + ['center'] * 8, dim_rows=(1,))
    return s


# ------------------------------------------------------------------ 9. ROC with the thresholds marked
@fig('x_t03_roc')
def roc(w, h, size=15, **_):
    s = Scene(w, h)
    x0, x1, y0, y1 = 1.0, w - 0.3, 0.85, h - 0.3
    px = lambda v: x0 + v * (x1 - x0)
    py = lambda v: y0 + v * (y1 - y0)
    pts = _R['roc_full']
    xs = [px(a) for a, b in pts]
    ys = [py(b) for a, b in pts]
    s.ax.fill_between(xs, [py(0)] * len(xs), ys, color=GOLD, alpha=0.45, zorder=1)
    s.line(x0, y0, x1, y0, lw=2)
    s.line(x0, y0, x0, y1, lw=2)
    s.ax.plot([px(0), px(1)], [py(0), py(1)], color=MUTE, lw=2, ls='--', zorder=2)
    s.ax.plot(xs, ys, color=INK, lw=3.2, zorder=3)
    s.text((x0 + x1) / 2, 0.28, 'false positive rate (of the invoices paid on time)', size=size, color=MUTE)
    s.text(0.3, (y0 + y1) / 2, 'true positive rate = recall (of the late invoices)', size=size, color=MUTE, rot=90)
    offs = {0.5: (0.02, -0.42), 0.3: (0.17, -0.12), 0.2: (0.17, -0.12), 0.15: (0.17, -0.12), 0.1: (0.17, -0.12), 0.05: (0.17, -0.12)}
    for r in TT:
        fx = r['fp'] / (r['fp'] + r['tn'])
        cx_, cy_ = px(fx), py(r['recall'])
        s.circle(cx_, cy_, 0.09, fill=RED, edge=INK, lw=1.4, z=5)
        dx, dy = offs[r['threshold']]
        s.text(cx_ + dx, cy_ + dy, f"{r['threshold']:.2f}", size=14, weight='bold', ha='left' if dx > 0 else 'right', z=6)
    s.text(px(0.43), py(0.66), f"Gold area\nis the AUC\n{_R['auc_logistic']:.2f}", size=size, weight='bold')
    s.text(px(0.84), py(0.50), 'Dashed line:\ncoin flip, 0.50', size=size, color=MUTE)
    r2 = _row(0.2)
    s.text(px(0.98), py(0.31), f"TPR = TP ÷ (TP + FN) = {r2['tp']} ÷ {r2['tp'] + r2['fn']} = {_pct(r2['recall'])}", size=14, weight='bold', ha='right')
    s.text(px(0.98), py(0.215), f"FPR = FP ÷ (FP + TN) = {r2['fp']} ÷ {r2['fp'] + r2['tn']} = {_pct(r2['fp'] / (r2['fp'] + r2['tn']))}", size=14, weight='bold', ha='right')
    return s


# ------------------------------------------------------------------ 10. cost of each threshold
@fig('x_t03_cost')
def cost(w, h, **_):
    s = Scene(w, h)
    rows = [('Never flag', _R['cost_never_flag_ugx'])] + [(f"Flag at {r['threshold']:.2f}", r['cost_ugx']) for r in TT]
    best = min(rows, key=lambda x: x[1])[1]
    x0, x1 = 1.95, w - 1.15
    mx = max(v for _, v in rows)
    bh = (h - 1.75) / len(rows)
    for i, (lab, v) in enumerate(rows):
        y = h - 0.1 - (i + 1) * bh
        s.text(0.1, y + bh / 2, lab, size=15, ha='left', weight='bold' if v == best else 'normal')
        s.rect(x0, y + 0.06, v / mx * (x1 - x0), bh - 0.12, fill=GOLD if v == best else (HAIR if i == 0 else PAPER), edge=INK, lw=1.4)
        s.text(x0 + v / mx * (x1 - x0) + 0.08, y + bh / 2, f'{v / 1e6:.1f}', size=15, weight='bold', ha='left')
    s.text(0.1, 1.13, 'Cost = (TP + FP) × chase cost + FN × miss cost.  Every flag is chased, right or wrong.', size=14, weight='bold', ha='left')
    s.text(0.1, 0.72, 'Total cost over the 900 test invoices, in UGX million.', size=14, color=BODY, ha='left')
    s.text(0.1, 0.3, 'ASSUMED for the lesson: UGX 20,000 per flag, UGX 300,000 per miss.', size=15, color=RED, weight='bold', ha='left')
    return s


# ------------------------------------------------------------------ 11. memorising
@fig('x_t03_memorise')
def memorise(w, h, **_):
    s = Scene(w, h)
    D = _R['depth_curve']
    x0, x1, y0, y1 = 1.1, w - 0.4, 0.95, h - 0.35
    lo, hi = 0.82, 1.0
    px = lambda i: x0 + 0.25 + i / (len(D) - 1) * (x1 - x0 - 0.5)
    py = lambda v: y0 + (v - lo) / (hi - lo) * (y1 - y0)
    s.line(x0, y0, x1, y0, lw=2)
    s.line(x0, y0, x0, y1, lw=2)
    for v in (0.85, 0.90, 0.95, 1.0):
        s.line(x0 - 0.06, py(v), x0, py(v), lw=1.4)
        s.text(x0 - 0.1, py(v), f'{int(round(v * 100))}%', size=14, ha='right')
    for i, d in enumerate(D):
        s.text(px(i), y0 - 0.25, str(d['depth']), size=14)
    s.text((x0 + x1) / 2, 0.25, 'how many yes/no questions deep the tree may go', size=14, color=MUTE)
    s.line(x0, py(_R['always_no']['accuracy']), x1, py(_R['always_no']['accuracy']), color=MUTE, lw=1.8, dash=True, z=2)
    s.text(x1 - 0.1, py(_R['always_no']['accuracy']) + 0.2, 'majority-class baseline: 90.8%', size=14, color=MUTE, ha='right')
    s.ax.plot([px(i) for i in range(len(D))], [py(d['train_acc']) for d in D], color=INK, lw=3.2, marker='o', ms=8, zorder=4)
    s.ax.plot([px(i) for i in range(len(D))], [py(d['test_acc']) for d in D], color=RED, lw=3.2, marker='o', ms=8, zorder=4)
    s.text(px(7) - 0.1, py(1.0) + 0.2, 'training set: 100%', size=15, weight='bold', ha='right')
    s.text(px(7) - 0.1, py(D[-1]['test_acc']) - 0.3, f"test set: {D[-1]['test_acc'] * 100:.1f}%", size=15, weight='bold', color=RED, ha='right')
    return s


# ------------------------------------------------------------------ 13. the twenty cases
@fig('x_t03_cases')
def cases(w, h, size=14, **_):
    s = Scene(w, h)
    C = _R['cases20']
    heads = ['Case', 'Invoice', 'Amount UGX', 'Score', 'Really late?']
    cw = [0.75, 1.3, 1.45, 0.9, 1.4]
    half = (w - 0.3) / 2
    sc = half / sum(cw)
    cw = [c * sc for c in cw]
    rh = (h - 0.1) / 11
    for b in range(2):
        rows = [heads]
        hl = {}
        for k, c in enumerate(C[b * 10:(b + 1) * 10], 1):
            rows.append([str(c['case']), c['invoice'], f"{c['amount_ugx']:,}", f"{c['score']:.2f}", 'late' if c['really_late'] else 'on time'])
            if c['really_late']:
                hl[(k, 4)] = GOLD
        s.table(b * (half + 0.3), h - 0.05, cw, rh, rows, size=size, hl_cells=hl, align=['center', 'center', 'right', 'center', 'center'])
    return s


# ------------------------------------------------------------------ 14. the blank table for the exercise
@fig('x_t03_blank')
def blank(w, h, size=16, **_):
    s = Scene(w, h)
    lw_, top = 1.7, 0.75
    cw = (w - lw_ - 0.05) / 2
    ch = (h - top - 1.05) / 2
    s.text(lw_ + cw / 2, h - 0.38, 'Really late', size=size, weight='bold')
    s.text(lw_ + cw * 1.5, h - 0.38, 'Really on time', size=size, weight='bold')
    s.text(lw_ / 2, 1.05 + ch * 1.5, 'Score 0.20\nor more\n(positive)', size=size, weight='bold')
    s.text(lw_ / 2, 1.05 + ch * 0.5, 'Score under\n0.20\n(negative)', size=size, weight='bold')
    for cx in range(2):
        for cy in range(2):
            s.box(lw_ + cx * cw + 0.04, 1.05 + cy * ch + 0.04, cw - 0.08, ch - 0.08, '', edge=INK, lw=2, fill=GOLD if (cx, cy) == (0, 1) else PAPER)
    s.text(lw_ + cw / 2, 1.05 + ch * 1.5, 'true positive\n(TP)', size=size, color=MUTE)
    s.text(lw_ + cw * 1.5, 1.05 + ch * 1.5, 'false positive\n(FP)', size=size, color=MUTE)
    s.text(lw_ + cw / 2, 1.05 + ch * 0.5, 'false negative\n(FN)', size=size, color=MUTE)
    s.text(lw_ + cw * 1.5, 1.05 + ch * 0.5, 'true negative\n(TN)', size=size, color=MUTE)
    s.text(0.1, 0.68, 'Precision = TP ÷ (TP + FP)', size=size, weight='bold', ha='left')
    s.text(0.1, 0.25, 'Recall = TP ÷ (TP + FN)', size=size, weight='bold', ha='left')
    return s


# ------------------------------------------------------------------ 12. old versus new invoices (demo slide, 7.3 x 3.9)
@fig('x_t03_versus')
def versus(w, h, left=None, right=None, middle='', **_):
    s = Scene(w, h)
    pw = (w - 2.2) / 2
    for i, side in enumerate((left, right)):
        x = 0.05 + i * (pw + 2.1)
        s.box(x, 0.05, pw, h - 0.1, '', fill=GOLD if i else PAPER, edge=INK, lw=2.0, r=0.08)
        s.text(x + pw / 2, h - 0.5, side['head'], size=20, weight='bold')
        s.text(x + pw / 2, h / 2 + 0.1, side['big'], size=54, weight='bold')
        s.text(x + pw / 2, 0.7, side['unit'], size=16, color=BODY)
    s.arrow(0.05 + pw + 0.15, h / 2 + 0.1, 0.05 + pw + 1.95, h / 2 + 0.1, lw=3, head=22)
    s.text(0.05 + pw + 1.05, h / 2 - 0.35, middle, size=17, weight='bold', color=RED)
    return s


# ------------------------------------------------------------------ the five formulas, with the smoke alarm numbers
@fig('x_t03_formulas')
def formulas(w, h, size=15, **_):
    TP, FP, FN, TN = 16, 34, 4, 946
    P, R = TP / (TP + FP), TP / (TP + FN)
    acc, fpr, f1v = (TP + TN) / (TP + TN + FP + FN), FP / (FP + TN), 2 * P * R / (P + R)
    assert (round(100 * acc, 1), round(100 * P), round(100 * R), round(100 * f1v)) == (96.2, 32, 80, 46) and abs(fpr - 0.0347) < 0.0005
    s = Scene(w, h)
    rows = [['Measure', 'Formula', 'Alarm numbers', 'The question it answers'],
            ['Accuracy', '(TP + TN) ÷ (TP + TN + FP + FN)', '(16 + 946) ÷ 1,000 = 96.2%', 'How often is it right?'],
            ['Precision', 'TP ÷ (TP + FP)', '16 ÷ (16 + 34) = 32%', 'When it rings, is it a fire?'],
            ['Recall (TPR)', 'TP ÷ (TP + FN)', '16 ÷ (16 + 4) = 80%', 'Of the fires, how many caught?'],
            ['False positive rate', 'FP ÷ (FP + TN)', '34 ÷ (34 + 946) = 3.5%', 'Of the quiet events, how many rang?'],
            ['F1 score', '2 × P × R ÷ (P + R)', '2 × 0.32 × 0.80 ÷ 1.12 = 46%', 'Precision and recall in one']]
    cw = [2.0, 3.3, 3.2, 3.8]
    sc = (w - 0.1) / sum(cw)
    cw = [c * sc for c in cw]
    rh = (h - 0.85) / 6
    s.table(0.05, h - 0.05, cw, rh, rows, size=size, hl_cells={(r, 1): GOLD for r in range(1, 6)}, align=['left', 'left', 'left', 'left'])
    s.text(0.1, 0.4, 'TP, FP, FN, TN: the four counts in the confusion matrix. P: precision. R: recall.', size=15, color=BODY, ha='left')
    return s


# ================================================================== 11 November 2026 rework: figures that build each measure step by step
ALARM = dict(tp=16, fp=34, fn=4, tn=946)          # invented smoke alarm year: 1,000 events, 20 real fires
_KEYS = (('tp', 0, 1), ('fp', 1, 1), ('fn', 0, 0), ('tn', 1, 0))   # (key, column, row) with row 1 at the top
_NAMES = dict(tp='True positive (TP)', fp='False positive (FP)', fn='False negative (FN)', tn='True negative (TN)')
_STORY = dict(tp='rang, and there\nwas a fire', fp='rang, but there\nwas no fire', fn='silent, but there\nwas a fire', tn='silent, and there\nwas no fire')


def _mini(s, x, y, w, h, vals, num=(), den=(), named=True, size=15, big=28, heads=('Real fire', 'No fire'), rows=('Alarm\nrang', 'Alarm\nsilent'),
          lw_=1.25, top=0.55, sub=None):
    """A 2 x 2 confusion matrix drawn inside (x, y, w, h). num: cells in gold; den: cells outlined thick; others dimmed when den is given."""
    cw = (w - lw_) / 2
    ch = (h - top) / 2
    s.text(x + lw_ + cw / 2, y + h - top / 2, heads[0], size=size, weight='bold')
    s.text(x + lw_ + cw * 1.5, y + h - top / 2, heads[1], size=size, weight='bold')
    s.text(x + lw_ / 2, y + ch * 1.5, rows[0], size=size, weight='bold')
    s.text(x + lw_ / 2, y + ch * 0.5, rows[1], size=size, weight='bold')
    for key, cx, cy in _KEYS:
        bx, by = x + lw_ + cx * cw + 0.04, y + cy * ch + 0.04
        dim = bool(den) and key not in den and key not in num
        s.box(bx, by, cw - 0.08, ch - 0.08, '', fill=GOLD if key in num else PAPER, edge=HAIR if dim else INK,
              lw=1.4 if dim else (3.4 if key in den or key in num else 2.0), r=0.05)
        col = GREY if dim else (RED if key == 'fn' and not num else INK)
        if named:
            s.text(bx + (cw - 0.08) / 2, by + (ch - 0.08) * 0.64, f'{vals[key]:,}', size=big, weight='bold', color=col)
            lab = (sub or {}).get(key, key.upper())
            s.text(bx + (cw - 0.08) / 2, by + (ch - 0.08) * 0.24, lab, size=size, weight='bold', color=GREY if dim else INK)
        else:
            s.text(bx + (cw - 0.08) / 2, by + (ch - 0.08) * 0.68, f'{vals[key]:,}', size=big, weight='bold', color=col)
            s.text(bx + (cw - 0.08) / 2, by + (ch - 0.08) * 0.28, _STORY[key], size=size, color=BODY)


@fig('x_t03_stories')
def stories(w, h, **_):
    """The four outcomes told as stories, no names yet."""
    s = Scene(w, h)
    _mini(s, 0.05, 0.05, w - 0.1, h - 0.1, ALARM, named=False, size=16, big=34, top=0.6, lw_=1.45)
    return s


@fig('x_t03_named')
def named(w, h, **_):
    """The same table, now with the four standard names."""
    s = Scene(w, h)
    _mini(s, 0.05, 0.05, w - 0.1, h - 0.1, ALARM, named=True, size=16, big=34, top=0.6, lw_=1.45,
          sub={k: v for k, v in _NAMES.items()})
    return s


_STEPS = {
    'accuracy': (('tp', 'tn'), ('tp', 'fp', 'fn', 'tn'),
                 ['Right answers:', '16 + 946 = 962', 'All events:', '1,000', '962 ÷ 1,000 = 0.962', '= 96.2%'],
                 'Accuracy =\n(TP + TN) ÷\n(TP + TN + FP + FN)'),
    'precision': (('tp',), ('tp', 'fp'),
                  ['Times it rang:', '16 + 34 = 50', 'A real fire in:', '16 of them', '16 ÷ 50 = 0.32', '= 32%'],
                  'Precision =\nTP ÷ (TP + FP)'),
    'recall': (('tp',), ('tp', 'fn'),
               ['Real fires:', '16 + 4 = 20', 'It rang for:', '16 of them', '16 ÷ 20 = 0.80', '= 80%'],
               'Recall =\nTP ÷ (TP + FN)'),
    'fpr': (('fp',), ('fp', 'tn'),
            ['Events with no fire:', '34 + 946 = 980', 'It rang anyway:', '34 of them', '34 ÷ 980 = 0.035', '= 3.5%'],
            'False positive rate =\nFP ÷ (FP + TN)'),
}


@fig('x_t03_measure')
def measure(w, h, which='precision', **_):
    """Matrix with the cells a measure uses, then the worked numbers, then the formula."""
    s = Scene(w, h)
    num, den, lines, formula = _STEPS[which]
    T = ALARM
    if which == 'accuracy':
        assert round(100 * (T['tp'] + T['tn']) / 1000, 1) == 96.2
    mw = 4.35
    _mini(s, 0.02, 0.05, mw, h - 0.1, T, num=num, den=den, size=15, big=26, top=0.5, lw_=1.05)
    x0 = mw + 0.25
    y = h - 0.25
    for i, ln in enumerate(lines):
        bold = i % 2 == 1
        s.text(x0, y, ln, size=17 if bold else 15, weight='bold' if bold else 'normal', color=INK if bold else BODY, ha='left')
        y -= 0.42 if not bold else 0.5
    fh = 0.42 * (formula.count('\n') + 1) + 0.2
    s.box(x0 - 0.08, 0.08, w - x0 + 0.03, fh, '', fill=GOLD, edge=INK, lw=2.0, r=0.06)
    s.text(x0 + (w - x0 - 0.05) / 2 - 0.04, 0.08 + fh / 2, formula, size=16, weight='bold')
    return s


@fig('x_t03_alarm_base2')
def alarm_base2(w, h, **_):
    """Our alarm against an alarm that never rings: accuracy worked for both."""
    s = Scene(w, h)
    pw = (w - 0.3) / 2
    never = dict(tp=0, fp=0, fn=20, tn=980)
    for k, (title, vals, l1, l2) in enumerate((('Our alarm', ALARM, '(16 + 946) ÷ 1,000 = 96.2%', 'fires caught: 16 of 20'),
                                              ('An alarm that never rings', never, '(0 + 980) ÷ 1,000 = 98%', 'fires caught: 0 of 20'))):
        x = k * (pw + 0.3)
        s.text(x + pw / 2, h - 0.22, title, size=17, weight='bold')
        _mini(s, x, 1.25, pw, h - 1.6, vals, num=('tp', 'tn'), size=14, big=22, top=0.5, lw_=0.95)
        s.text(x + pw / 2, 0.85, 'Accuracy ' + l1, size=15, weight='bold')
        s.text(x + pw / 2, 0.35, l2, size=16, weight='bold', color=RED if k else INK)
    return s


@fig('x_t03_avg')
def avg(w, h, **_):
    """Two alarms, their precision, recall and plain average."""
    s = Scene(w, h)
    cases = [('Our alarm (TP 16, FP 34, FN 4)', 0.32, 0.80, '4 fires missed'), ('Cautious alarm (TP 2, FP 0, FN 18)', 1.00, 0.10, '18 fires missed')]
    x0, x1 = 1.75, w - 1.0
    gh = (h - 0.1) / 2
    for gi, (lab, p, r, miss) in enumerate(cases):
        top = h - 0.05 - gi * gh
        s.text(0.05, top - 0.25, lab, size=16, weight='bold', ha='left')
        a = (p + r) / 2
        for bi, (nm, v, col) in enumerate((('Precision', p, PAPER), ('Recall', r, PAPER), ('Average', a, HAIR))):
            y = top - 0.75 - bi * 0.45
            s.text(x0 - 0.12, y, nm, size=15, ha='right', weight='bold' if nm == 'Average' else 'normal')
            s.rect(x0, y - 0.16, max(0.03, v * (x1 - x0)), 0.32, fill=col, edge=INK, lw=1.3)
            s.text(x0 + v * (x1 - x0) + 0.1, y, _pct(v), size=15, weight='bold', ha='left')
        s.text(x0, top - 2.05, f'({_pct(p)[:-1]} + {_pct(r)[:-1]}) ÷ 2 = {_pct(a)}, yet {miss}', size=15, color=RED if gi else BODY, weight='bold', ha='left')
    return s


@fig('x_t03_f1steps')
def f1steps(w, h, **_):
    """The harmonic mean worked for both alarms, then the formula."""
    s = Scene(w, h)
    P1, R1, P2, R2 = 0.32, 0.80, 1.0, 0.10
    h1, h2 = 1 / ((1 / P1 + 1 / R1) / 2), 1 / ((1 / P2 + 1 / R2) / 2)
    assert round(h1, 2) == 0.46 and round(h2, 2) == 0.18 and abs(h1 - 2 * P1 * R1 / (P1 + R1)) < 1e-12
    rows = [['Step', 'Our alarm', 'Cautious alarm'],
            ['Precision P and recall R', '0.32 and 0.80', '1.00 and 0.10'],
            ['1. One over each: 1 ÷ P, 1 ÷ R', '3.125 and 1.25', '1 and 10'],
            ['2. Average the two', '(3.125 + 1.25) ÷ 2 = 2.19', '(1 + 10) ÷ 2 = 5.5'],
            ['3. One over that average', '1 ÷ 2.19 = 0.46', '1 ÷ 5.5 = 0.18'],
            ['F1 score', '46%', '18%']]
    cw = [4.3, 3.6, 3.6]
    sc = (w - 0.1) / sum(cw)
    cw = [c * sc for c in cw]
    rh = (h - 1.05) / len(rows)
    s.table(0.05, h - 0.05, cw, rh, rows, size=16, hl_rows=(5,), align=['left', 'center', 'center'])
    s.text(0.1, 0.62, 'Same steps in one line:  F1 = 2 ÷ (1/P + 1/R) = 2 × P × R ÷ (P + R)', size=17, weight='bold', ha='left')
    s.text(0.1, 0.2, 'Check, our alarm:  2 × 0.32 × 0.80 ÷ (0.32 + 0.80) = 0.512 ÷ 1.12 = 0.46', size=16, color=BODY, ha='left')
    return s


ALARM_SET = [('High threshold', 12, 8, 8), ('Our setting', 16, 34, 4), ('Low threshold', 19, 181, 1)]


@fig('x_t03_alarm_table')
def alarm_table(w, h, **_):
    """The alarm at three thresholds: counts, precision and recall worked."""
    s = Scene(w, h)
    rows = [['Setting', 'Rang', 'Fires caught\n(TP)', 'False alarms\n(FP)', 'Fires missed\n(FN)', 'Precision\nTP ÷ (TP + FP)', 'Recall\nTP ÷ (TP + FN)']]
    for nm, tp, fp, fn in ALARM_SET:
        assert tp + fn == 20
        p, r = tp / (tp + fp), tp / (tp + fn)
        rows.append([nm, f'{tp + fp}', str(tp), str(fp), str(fn), f'{tp} ÷ {tp + fp} = {100 * p:.3g}%', f'{tp} ÷ 20 = {100 * r:.0f}%'])
    cw = [2.0, 0.95, 1.55, 1.6, 1.55, 2.25, 2.0]
    sc = (w - 1.0) / sum(cw)
    cw = [c * sc for c in cw]
    rh = (h - 0.1) / 4
    s.table(0.05, h - 0.05, cw, rh, rows, size=16, hl_rows=(2,), hl_fill=PALE, align=['left'] + ['center'] * 6)
    s.arrow(w - 0.55, h - 0.05 - rh * 1.3, w - 0.55, 0.25, lw=3, head=22)
    s.text(w - 0.3, (h - rh) / 2 + 0.05, 'lower the threshold', size=15, weight='bold', rot=90)
    return s


@fig('x_t03_roc_build')
def roc_build(w, h, **_):
    """The ROC curve built from five alarm settings: a table of points, then the points joined."""
    s = Scene(w, h)
    pts = [('Never rings', 0, 0, 20), ('High threshold', 12, 8, 8), ('Our setting', 16, 34, 4), ('Low threshold', 19, 181, 1), ('Always rings', 20, 980, 0)]
    rows = [['Setting', 'FPR = FP ÷ 980', 'TPR = TP ÷ 20']]
    P = []
    for nm, tp, fp, fn in pts:
        fpr, tpr = fp / 980, tp / 20
        P.append((nm, fpr, tpr))
        rows.append([nm, f'{fp} ÷ 980 = {100 * fpr:.2g}%' if 0 < fp < 980 else f'{fp} ÷ 980 = {100 * fpr:.0f}%', f'{tp} ÷ 20 = {100 * tpr:.0f}%'])
    tw = [2.0, 2.45, 1.85]
    s.table(0.05, h - 0.05, tw, (h - 0.1) / 6, rows, size=15, hl_rows=(3,), hl_fill=PALE, align=['left', 'center', 'center'])
    gx0 = sum(tw) + 1.05
    x0, x1, y0, y1 = gx0, w - 0.25, 0.8, h - 0.2
    px = lambda v: x0 + v * (x1 - x0)
    py = lambda v: y0 + v * (y1 - y0)
    s.line(x0, y0, x1, y0, lw=2)
    s.line(x0, y0, x0, y1, lw=2)
    for v in (0, 0.5, 1):
        s.text(px(v), y0 - 0.2, f'{int(v * 100)}%', size=14)
        s.text(x0 - 0.1, py(v), f'{int(v * 100)}%', size=14, ha='right')
    s.text((x0 + x1) / 2, 0.2, 'false positive rate (FPR)', size=15, color=MUTE)
    s.text(x0 - 0.75, (y0 + y1) / 2, 'true positive rate (TPR)', size=15, color=MUTE, rot=90)
    s.ax.plot([px(0), px(1)], [py(0), py(1)], color=MUTE, lw=2, ls='--', zorder=2)
    s.ax.plot([px(a) for _, a, b in P], [py(b) for _, a, b in P], color=INK, lw=3, zorder=3)
    for nm, a, b in P:
        s.circle(px(a), py(b), 0.08, fill=RED, edge=INK, lw=1.3, z=5)
    lab = {'High threshold': (0.22, 0.52), 'Our setting': (0.22, 0.72), 'Low threshold': (0.45, 0.85)}
    for nm, a, b in P:
        if nm in lab:
            tx, ty = lab[nm]
            s.line(px(a), py(b), px(tx) - 0.05, py(ty), color=GREY, lw=1.2, z=4)
            s.text(px(tx), py(ty), nm.split()[0], size=14, weight='bold', ha='left')
    s.text(px(0.62), py(0.3), 'coin flip', size=14, color=MUTE)
    return s


@fig('x_t03_auc_pairs')
def auc_pairs(w, h, **_):
    """AUC as a share of pairs: 2 fires, 3 quiet events, 6 pairs, 5 ranked the right way."""
    s = Scene(w, h)
    fires, quiet = [8, 6], [7, 3, 2]
    ok = [(f, q, f > q) for f in fires for q in quiet]
    assert sum(o for *_, o in ok) == 5
    x0, x1, yl = 0.5, w - 0.4, h - 1.15
    px = lambda v: x0 + v / 10 * (x1 - x0)
    s.line(x0, yl, x1, yl, lw=2)
    for v in range(0, 11, 2):
        s.text(px(v), yl - 0.3, str(v), size=14)
    s.text((x0 + x1) / 2, h - 0.25, 'Smoke score of five events: red = real fire, grey = no fire', size=15, weight='bold')
    for v in fires:
        s.circle(px(v), yl + 0.3, 0.16, fill=RED, edge=INK, lw=1.4)
    for v in quiet:
        s.circle(px(v), yl + 0.3, 0.16, fill=HAIR, edge=INK, lw=1.4)
    cw, ch = (w - 0.2) / 3, 0.62
    for i, (f, q, good) in enumerate(ok):
        r, c = divmod(i, 3)
        bx, by = 0.1 + c * cw, yl - 1.25 - r * (ch + 0.12)
        s.box(bx + 0.04, by, cw - 0.08, ch, '', fill=GOLD if good else PAPER, edge=INK, lw=1.6, r=0.05)
        s.text(bx + cw / 2 - 0.25, by + ch / 2, f'fire {f} vs no fire {q}', size=15)
        s.icon('check' if good else 'cross', bx + cw - 0.4, by + ch / 2, 0.36)
    s.text(w / 2, 0.95, '5 of the 6 pairs put the fire higher:  AUC = 5 ÷ 6 = 0.83', size=17, weight='bold')
    s.text(w / 2, 0.35, 'AUC: the chance that a random fire scores above a random no-fire event', size=15, color=BODY)
    return s


@fig('x_t03_costcalc')
def costcalc(w, h, **_):
    """The cost of the 0.20 threshold built line by line."""
    s = Scene(w, h)
    r = _row(0.2)
    flags, fn = r['tp'] + r['fp'], r['fn']
    assert flags * 20000 + fn * 300000 == r['cost_ugx'] == 16440000
    lines = [('Flags chased = TP + FP', f"{r['tp']} + {r['fp']} = {flags}", PAPER),
             ('Chasing cost', f'{flags} × UGX 20,000 = UGX {flags * 20000:,}', PAPER),
             ('Late invoices missed = FN', f'{fn}', PAPER),
             ('Cost of the misses', f'{fn} × UGX 300,000 = UGX {fn * 300000:,}', PAPER),
             ('Total cost at 0.20', f"UGX {flags * 20000:,} + UGX {fn * 300000:,} = UGX {r['cost_ugx']:,}", GOLD)]
    bh = (h - 1.0) / len(lines)
    for i, (a, b, col) in enumerate(lines):
        y = h - 0.05 - (i + 1) * bh
        s.box(0.05, y + 0.05, w - 0.1, bh - 0.1, '', fill=col, edge=INK, lw=1.6, r=0.05)
        s.text(0.25, y + bh / 2, a, size=16, weight='bold', ha='left')
        s.text(w - 0.25, y + bh / 2, b, size=16, ha='right', weight='bold' if col == GOLD else 'normal')
    s.text(0.1, 0.45, 'Cost = (TP + FP) × chase cost + FN × miss cost', size=18, weight='bold', ha='left')
    return s


def _overfit_pts():
    # training cases: (x, y, late?) on two made-up features; two late cases sit among the on-time ones (noise)
    train = [(1.0, 1.2, 0), (1.6, 0.6, 0), (2.2, 1.5, 0), (0.7, 2.3, 0), (1.5, 2.6, 0), (2.8, 0.7, 0), (3.0, 1.9, 0), (0.9, 3.4, 0), (2.0, 2.8, 0), (3.6, 1.1, 0),
             (4.4, 3.3, 1), (3.8, 3.9, 1), (4.9, 2.6, 1), (4.0, 2.9, 1), (3.2, 4.3, 1), (5.0, 3.9, 1), (4.6, 4.5, 1), (2.6, 4.6, 1),
             (1.4, 1.8, 1), (2.9, 1.2, 1)]
    new = [(1.2, 1.5, 0), (2.7, 1.0, 0), (1.9, 0.9, 0), (3.1, 1.5, 0), (0.8, 2.8, 0), (4.3, 3.7, 1), (3.5, 3.5, 1), (4.8, 3.0, 1), (1.6, 3.2, 0), (2.5, 2.3, 1)]
    loops = [(1.4, 1.8, 0.5), (2.9, 1.2, 0.5)]
    return train, new, loops


def _line_says(p):
    return p[0] + p[1] > 5.3


def _wiggly_says(p, loops):
    return _line_says(p) or any(math.dist(p[:2], (a, b)) <= r for a, b, r in loops)


@fig('x_t03_overfit')
def overfit(w, h, **_):
    """Illustration: a model that memorises two odd training cases fits all of them and then errs on new cases."""
    s = Scene(w, h)
    train, new, loops = _overfit_pts()
    res = {}
    for nm, P in (('train', train), ('new', new)):
        res[nm] = (sum(_line_says(p) == bool(p[2]) for p in P), sum(_wiggly_says(p, loops) == bool(p[2]) for p in P), len(P))
    assert res == {'train': (18, 20, 20), 'new': (9, 6, 10)}, res
    pw = (w - 0.3) / 2
    for k, (P, title, nm) in enumerate(((train, 'Training cases: it learned these', 'train'), (new, 'New cases: never seen', 'new'))):
        ox, oy = k * (pw + 0.3), 0.8
        ph = h - 1.35
        sc = min((pw - 0.2) / 5.6, (ph - 0.1) / 5.0)
        mx = lambda p: (ox + 0.1 + p[0] * sc, oy + 0.05 + p[1] * sc)
        s.rect(ox, oy, pw, ph, fill=PAPER, edge=INK, lw=1.6)
        a, b = mx((0.6, 4.7)), mx((5.3, 0.0))
        s.line(a[0], a[1], b[0], b[1], color=INK, lw=2.4, z=3)
        for (cx, cy, r) in loops:
            c = mx((cx, cy))
            s.circle(c[0], c[1], r * sc, fill='none', edge=RED, lw=2.4, z=3)
        for p in P:
            x, y = mx(p)
            wrong = _wiggly_says(p, loops) != bool(p[2])
            s.circle(x, y, 0.09, fill=RED if p[2] else HAIR, edge=INK if wrong else (RED if p[2] else GREY), lw=2.6 if wrong else 1, z=4)
            if wrong:
                s.circle(x, y, 0.19, fill='none', edge=INK, lw=2, z=4)
        s.text(ox + pw / 2, h - 0.25, title, size=16, weight='bold')
        line_ok, wig_ok, n = res[nm]
        s.text(ox + pw / 2, 0.5, f'Memorising model: {wig_ok} of {n} right', size=15, weight='bold', color=RED)
        s.text(ox + pw / 2, 0.15, f'Straight line: {line_ok} of {n} right', size=15)
    return s
