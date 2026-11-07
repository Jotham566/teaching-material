"""Figures for Session 2, Learning from examples: types of machine learning, decision trees, nearest neighbours.  Names: x_t02_*  (content kind 't02_*').

Every number comes from the recorded run in demo_runs/s02/ (learn_run.py, results_s02.json).  The expense claims are FICTIONAL (make_expenses.py, seed 2026);
the 40 customer messages are the Nile Valley Foods practice file (labels from the answer key).
"""
import csv
import json
import math
from pathlib import Path

from matplotlib.patches import Ellipse, Circle

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD, fig
import slidekit as K

RUN = Path(__file__).resolve().parent.parent / 'demo_runs' / 's02'
_C = {}


def _res():
    if not _C:
        _C.update(json.load(open(RUN / 'results_s02.json')))
    return _C


def _short(t, n):
    t = t.strip()
    if len(t) <= n:
        return t
    cut = t[:n].rsplit(' ', 1)[0].rstrip(',.;: ')
    return cut + ' ...'


# ------------------------------------------------------------------ labelled examples: a category and a number
@fig('x_t02_labelled')
def x_t02_labelled(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.28, 'Classification: the label is a category', size=17, weight='bold', ha='left')
    rh = 0.58
    top = h - 0.5
    msgs = [('You have won UGX 5,000,000. Send a fee to claim it.', 'spam'),
            ('You have received UGX 20,000 from Grace.', 'not spam'),
            ('The meeting is moved to 3 pm.', 'not spam')]
    for i, (m, lab) in enumerate(msgs):
        y = top - (i + 1) * rh
        s.box(0.05, y + 0.05, w - 2.1, rh - 0.1, '', fill=PAPER, lw=1.5, r=0.05)
        s.text(0.18, y + rh / 2, m, size=15, ha='left')
        s.arrow(w - 2.0, y + rh / 2, w - 1.8, y + rh / 2, lw=2, head=12)
        s.box(w - 1.7, y + 0.07, 1.6, rh - 0.14, lab, size=16, fill=GOLD if lab == 'spam' else PAPER, lw=1.8, weight='bold', r=0.06)
    y0 = top - 3 * rh - 0.4
    s.line(0.05, y0 + 0.18, w - 0.05, y0 + 0.18, color=HAIR, lw=1.2)
    s.text(0.1, y0 - 0.1, 'Regression: the label is a number', size=17, weight='bold', ha='left')
    hs = [('80 m\u00b2, 3 bedrooms', 'UGX 220 million'), ('50 m\u00b2, 2 bedrooms', 'UGX 150 million'), ('120 m\u00b2, 4 bedrooms', 'UGX 310 million')]
    for i, (m, lab) in enumerate(hs):
        y = y0 - 0.3 - (i + 1) * rh
        s.box(0.05, y + 0.05, w - 2.1, rh - 0.1, '', fill=PAPER, lw=1.5, r=0.05)
        s.text(0.18, y + rh / 2, m, size=15, ha='left')
        s.arrow(w - 2.0, y + rh / 2, w - 1.8, y + rh / 2, lw=2, head=12)
        s.box(w - 1.7, y + 0.07, 1.6, rh - 0.14, lab, size=14, fill=GOLD, lw=1.8, weight='bold', r=0.06)
    s.text(w - 1.0, h - 0.28, 'label', size=15, color=RED, weight='bold')
    return s


# ------------------------------------------------------------------ four ways of learning
@fig('x_t02_four_ways')
def x_t02_four_ways(w, h, **_):
    s = Scene(w, h)
    gap = 0.15
    pw = (w - 0.1 - 3 * gap) / 4
    titles = ['Supervised', 'Unsupervised', 'Reinforcement', 'Self-supervised']
    caps = ['Learns from examples with the right answer attached', 'Finds groups when nobody gives answers',
            'Learns by trial and reward', 'Hides a part of its own data and predicts it']
    for i in range(4):
        x = 0.05 + i * (pw + gap)
        cx = x + pw / 2
        s.box(x, 0.05, pw, h - 0.1, '', fill=PAPER, lw=1.8, r=0.08)
        s.text(cx, h - 0.4, titles[i], size=19, weight='bold')
        s.line(x + 0.15, h - 0.75, x + pw - 0.15, h - 0.75, lw=1.4)
        lines = K.wrap(caps[i], 16, 'regular', pw - 0.4)
        s.text(cx, 0.25 + len(lines) * 0.13 + 0.1, '\n'.join(lines), size=16, color=BODY)
        base = 1.55
        if i == 0:
            pts = [(-0.7, 0.9, 'g'), (-0.35, 0.55, 'g'), (-0.8, 0.45, 'g'), (0.35, 0.95, 'b'), (0.7, 0.55, 'b'), (0.45, 0.35, 'b')]
            for dx, dy, k in pts:
                if k == 'g':
                    s.rect(cx + dx - 0.1, base + dy - 0.1, 0.2, 0.2, fill=GOLD, edge=INK, lw=1.4, z=4)
                else:
                    s.circle(cx + dx, base + dy, 0.11, fill=INK, edge=INK, lw=1, z=4)
            s.circle(cx, base + 0.15, 0.2, fill=PAPER, edge=RED, lw=2.6, z=5)
            s.text(cx, base + 0.14, '?', size=18, weight='bold', color=RED, z=7)
        elif i == 1:
            import random
            rnd = random.Random(4)
            for (gx, gy) in ((-0.6, 0.95), (0.55, 0.9), (0.0, 0.3)):
                for _k in range(5):
                    s.circle(cx + gx + rnd.uniform(-0.28, 0.28), base + gy + rnd.uniform(-0.2, 0.2), 0.07, fill=GREY, edge=INK, lw=1, z=4)
                s.ax.add_patch(Ellipse((cx + gx, base + gy), 0.9, 0.62, fc='none', ec=RED, lw=2, ls='--', zorder=5))
        elif i == 2:
            s.box(cx - 1.1, base + 0.7, 0.9, 0.5, 'Try', size=16, fill=PAPER, lw=1.6)
            s.box(cx + 0.2, base + 0.7, 0.9, 0.5, 'Score', size=16, fill=GOLD, lw=1.6)
            s.arrow(cx - 0.2, base + 0.95, cx + 0.2, base + 0.95, lw=2)
            s.arrow(cx + 0.65, base + 0.7, cx + 0.65, base + 0.38, lw=2)
            s.arrow(cx + 0.65, base + 0.38, cx - 0.65, base + 0.38, lw=2)
            s.arrow(cx - 0.65, base + 0.38, cx - 0.65, base + 0.7, lw=2)
            s.text(cx, base + 0.15, 'adjust and try again', size=16, color=RED, weight='bold')
        else:
            s.text(cx, base + 1.15, 'Thank you for the', size=16)
            s.box(cx - 0.45, base + 0.5, 0.9, 0.45, '?', size=20, fill=GOLD, lw=1.6, weight='bold')
            s.text(cx, base + 0.25, 'delivery today', size=16)
    return s


# ------------------------------------------------------------------ the drawn decision tree (real data)
@fig('x_t02_tree')
def x_t02_tree(w, h, **_):
    tree = _res()['tree']
    s = Scene(w, h)
    leaves = []

    def collect(n):
        if 'leaf' in n:
            leaves.append(n)
        else:
            collect(n['left'])
            collect(n['right'])
    collect(tree)
    nl = len(leaves)
    slot = (w - 0.1) / nl
    cnt = [0]

    def place(n, depth):
        n['depth'] = depth
        if 'leaf' in n:
            n['x'] = 0.05 + slot * (cnt[0] + 0.5)
            cnt[0] += 1
        else:
            place(n['left'], depth + 1)
            place(n['right'], depth + 1)
            n['x'] = (n['left']['x'] + n['right']['x']) / 2
    place(tree, 0)
    ys = [h - 0.5 - d * 1.08 for d in range(4)]
    bw, bh = 1.72, 0.74

    def question(n):
        f, t = n['feature'], n['thr']
        if f.startswith('receipt'):
            return 'Receipt\nattached?'
        if f.startswith('amount'):
            return f'Amount over\nUGX {int(round(t)) * 1000:,}?'
        return f'Filed over\n{int(t)} days late?'

    def draw(n):
        y = ys[n['depth']]
        if 'leaf' in n:
            q = n['leaf'] == 'queried'
            c = n['counts'][n['leaf']]
            s.box(n['x'] - 0.78, y - bh / 2, 1.56, bh, f"{'Queried' if q else 'Paid'}\n{c} of {n['n']}", size=16, fill=GOLD if q else PAPER, lw=2.2, weight='bold', r=0.08)
            return
        s.box(n['x'] - bw / 2, y - bh / 2, bw, bh, question(n), size=16, fill=PAPER, lw=1.8, r=0.08)
        for side, ch in (('no', n['left']), ('yes', n['right'])):
            cy = ys[ch['depth']]
            s.line(n['x'], y - bh / 2, ch['x'], cy + bh / 2, lw=1.8, z=1)
            mx, my = (n['x'] + ch['x']) / 2, (y - bh / 2 + cy + bh / 2) / 2
            off = 0.32 if side == 'yes' else -0.32
            s.text(mx + off, my + 0.03, side, size=15, weight='bold', color=RED, z=8)
            draw(ch)
    draw(tree)
    return s


# ------------------------------------------------------------------ an everyday decision tree: carry an umbrella?
@fig('x_t02_umbrella')
def x_t02_umbrella(w, h, **_):
    s = Scene(w, h)
    bw, bh = 2.0, 0.8
    lw_ = 1.9
    ys = [h - 0.75, h - 2.15, h - 3.5]

    def q(x, y, text):
        s.box(x - bw / 2, y - bh / 2, bw, bh, text, size=16, fill=PAPER, lw=1.8, r=0.08)

    def leaf(x, y, head, sub, gold):
        s.box(x - lw_ / 2, y - bh / 2, lw_, bh, head + '\n' + sub, size=15, fill=GOLD if gold else PAPER, lw=2.2, weight='bold', r=0.08)

    def edge(x1, y1, x2, y2, lab, dx):
        s.line(x1, y1 - bh / 2, x2, y2 + bh / 2, lw=1.8, z=1)
        s.text((x1 + x2) / 2 + dx, (y1 + y2) / 2 + 0.02, lab, size=15, weight='bold', color=RED, z=8)
    xl, xa, xb = 1.2, 4.4, 6.5
    xq = (xa + xb) / 2
    xr = (xl + xq) / 2
    q(xr, ys[0], 'Is the sky\ncloudy?')
    leaf(xl, ys[1], 'No umbrella', '0 of 5 days rained', False)
    edge(xr, ys[0], xl, ys[1], 'no', -0.3)
    q(xq, ys[1], 'Forecast over\n50% rain?')
    edge(xr, ys[0], xq, ys[1], 'yes', 0.3)
    leaf(xa, ys[2], 'No umbrella', '0 of 2 days rained', False)
    edge(xq, ys[1], xa, ys[2], 'no', -0.3)
    leaf(xb, ys[2], 'Carry it', '4 of 5 days rained', True)
    edge(xq, ys[1], xb, ys[2], 'yes', 0.3)
    s.text(0.15, 1.45, 'Each question is a split.', size=15, ha='left', color=BODY)
    s.text(0.15, 1.15, 'Each answer box is a leaf.', size=15, ha='left', color=BODY)
    s.text(0.15, 0.85, 'Longest path: 2 questions,', size=15, ha='left', color=BODY)
    s.text(0.15, 0.55, 'so the depth is 2.', size=15, ha='left', color=BODY)
    s.text(w - 0.1, 0.25, '12 past days, invented for illustration', size=14, ha='right', color=MUTE)
    return s


# ------------------------------------------------------------------ what makes a good question: the umbrella days
@fig('x_t02_split_umbrella')
def x_t02_split_umbrella(w, h, **_):
    s = Scene(w, h)
    bars = [('All 12 past days', 12, 4, 3.65), ('Sky cloudy: 7 days', 7, 4, 1.75), ('Sky clear: 5 days', 5, 0, 0.45)]
    bx, bw_, bh = 0.1, w - 0.2, 0.6
    for lab, n, q, y in bars:
        s.text(bx, y + bh + 0.28, f'{lab}: {q / n * 100:.0f}% rained', size=18, weight='bold', ha='left')
        gi = 1 - (q / n) ** 2 - (1 - q / n) ** 2
        s.text(bx + bw_, y + bh + 0.28, f'Gini G = {gi:.2f}', size=17, weight='bold', ha='right', color=RED)
        qw = bw_ * q / n
        if q:
            s.rect(bx, y, qw, bh, fill=GOLD, edge=INK, lw=1.8, z=3)
            s.text(bx + qw / 2, y + bh / 2, f'{q} rained', size=17, weight='bold', z=6)
        s.rect(bx + qw, y, bw_ - qw, bh, fill=PAPER, edge=INK, lw=1.8, z=3)
        s.text(bx + qw + (bw_ - qw) / 2, y + bh / 2, f'{n - q} dry', size=17, color=BODY, z=6)
    s.arrow(w / 2, 3.45, w / 2, 2.95, lw=2.4)
    s.text(w / 2 + 0.2, 3.2, 'ask: is the sky cloudy?', size=17, weight='bold', color=RED, ha='left')
    return s


# ------------------------------------------------------------------ what makes a good question
@fig('x_t02_split')
def x_t02_split(w, h, **_):
    d = _res()['split_receipt']
    s = Scene(w, h)
    bars = [('All 240 claims', d['all_n'], d['all_q'], 3.65), ('Receipt attached: 163 claims', d['with_n'], d['with_q'], 1.75), ('No receipt: 77 claims', d['without_n'], d['without_q'], 0.45)]
    bx, bw_, bh = 0.1, w - 0.2, 0.6
    for lab, n, q, y in bars:
        s.text(bx, y + bh + 0.28, f'{lab}: {q / n * 100:.0f}% queried', size=18, weight='bold', ha='left')
        qw = bw_ * q / n
        s.rect(bx, y, qw, bh, fill=GOLD, edge=INK, lw=1.8, z=3)
        s.rect(bx + qw, y, bw_ - qw, bh, fill=PAPER, edge=INK, lw=1.8, z=3)
        s.text(bx + qw / 2, y + bh / 2, f'{q}', size=17, weight='bold', z=6)
        s.text(bx + qw + (bw_ - qw) / 2, y + bh / 2, f'{n - q} paid', size=17, color=BODY, z=6)
    s.arrow(w / 2, 3.45, w / 2, 2.95, lw=2.4)
    s.text(w / 2 + 0.2, 3.2, 'ask: was a receipt attached?', size=17, weight='bold', color=RED, ha='left')
    return s


# ------------------------------------------------------------------ nearest neighbours on real (fictional) claims
@fig('x_t02_knn')
def x_t02_knn(w, h, **_):
    d = _res()['knn_demo']
    pts = d['points']
    s = Scene(w, h)
    ax0, ax1, ay0, ay1 = 1.1, w - 0.15, 0.95, h - 0.65
    s.line(ax0, ay0, ax1, ay0, lw=2)
    s.line(ax0, ay0, ax0, ay1, lw=2)
    lo, hi = 3.65, 6.45
    px = lambda a: ax0 + (math.log10(a) - lo) / (hi - lo) * (ax1 - ax0 - 0.1)
    py = lambda dd: ay0 + dd / 90.0 * (ay1 - ay0 - 0.1)
    for a, lab in ((10000, '10,000'), (100000, '100,000'), (1000000, '1,000,000')):
        s.line(px(a), ay0, px(a), ay0 - 0.08, lw=1.6)
        s.text(px(a), ay0 - 0.3, lab, size=14)
    for dd in (0, 30, 60, 90):
        s.line(ax0 - 0.08, py(dd), ax0, py(dd), lw=1.6)
        s.text(ax0 - 0.15, py(dd), str(dd), size=14, ha='right')
    for a, dd, o in pts:
        if o == 'queried':
            s.rect(px(a) - 0.07, py(dd) - 0.07, 0.14, 0.14, fill=GOLD, edge=INK, lw=1.0, z=3)
        else:
            s.circle(px(a), py(dd), 0.07, fill=PAPER, edge=INK, lw=1.2, z=3)
    qa, qd = d['query']
    for i in d['nn_idx']:
        a, dd, o = pts[i]
        s.circle(px(a), py(dd), 0.2, fill='none', edge=RED, lw=2.8, z=6)
        s.line(px(qa), py(qd), px(a), py(dd), color=RED, lw=1.4, dash=True, z=2)
    s.ax.scatter([px(qa)], [py(qd)], s=420, marker='*', c=RED, edgecolors=INK, linewidths=1.2, zorder=8)
    s.text((ax0 + ax1) / 2 + 0.2, 0.25, 'Amount claimed, UGX (log scale)', size=16, color=BODY)
    s.text(0.3, (ay0 + ay1) / 2, 'Days to file', size=16, color=BODY, rot=90)
    ly = h - 0.3
    s.circle(ax0 + 0.1, ly, 0.08, fill=PAPER, edge=INK, lw=1.2)
    s.text(ax0 + 0.28, ly, 'paid', size=15, ha='left')
    s.rect(ax0 + 1.0, ly - 0.08, 0.16, 0.16, fill=GOLD, edge=INK, lw=1.0)
    s.text(ax0 + 1.28, ly, 'queried', size=15, ha='left')
    s.ax.scatter([ax0 + 2.55], [ly], s=170, marker='*', c=RED, edgecolors=INK, linewidths=1, zorder=8)
    s.text(ax0 + 2.78, ly, 'new claim', size=15, ha='left')
    s.circle(ax0 + 4.15, ly, 0.13, fill='none', edge=RED, lw=2.4)
    s.text(ax0 + 4.4, ly, '5 nearest', size=15, ha='left')
    return s


# ------------------------------------------------------------------ nearest neighbours on words: precedent
@fig('x_t02_precedent')
def x_t02_precedent(w, h, idx=0, **_):
    p = _res()['precedents'][idx]
    q = p['query']
    s = Scene(w, h)
    qh = 0.95
    qy = h - 0.05 - qh
    s.box(0.05, qy, w - 0.1, qh, '', fill=GOLD, lw=2, r=0.08)
    lines = K.wrap(q['id'] + ': ' + _short(q['text'], 95), 16, 'regular', w - 1.9)
    s.text(0.25, qy + qh / 2, '\n'.join(lines[:2]), size=16, ha='left', weight='bold')
    s.text(w - 0.2, qy + qh / 2, 'new message', size=15, ha='right', color=INK)
    s.text(0.1, qy - 0.3, 'Its three most similar past messages', size=17, weight='bold', ha='left')
    rh = 0.78
    top = qy - 0.5
    for i, nb in enumerate(p['neighbours']):
        y = top - (i + 1) * rh
        s.box(0.05, y + 0.05, w - 0.1, rh - 0.1, '', fill=PAPER, lw=1.5, r=0.06)
        s.text(0.55, y + rh / 2, f"{nb['sim']:.2f}", size=17, weight='bold')
        ln = K.wrap(nb['id'] + ': ' + _short(nb['text'], 70), 15, 'regular', w - 3.4)
        s.text(1.0, y + rh / 2, '\n'.join(ln[:2]), size=15, ha='left')
        s.box(w - 1.65, y + 0.17, 1.5, rh - 0.34, nb['cat'], size=15, fill=INK, edge=INK, color=PAPER, weight='bold', r=0.06)
    cats = [nb['cat'] for nb in p['neighbours']]
    best = max(set(cats), key=cats.count)
    n = cats.count(best)
    verdict = f'Vote: {n} of 3 say {best}' if n >= 2 else 'Vote: three different answers, no clear winner'
    s.box(0.05, 0.08, w - 0.1, 0.62, verdict, size=18, fill=PAPER, edge=RED, lw=2.4, weight='bold', r=0.08, color=INK if n >= 2 else RED)
    s.text(0.55, top + 0.05, '', size=15)
    return s


# ------------------------------------------------------------------ cross-validation: take turns being the test set
@fig('x_t02_folds')
def x_t02_folds(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.3, '40 messages in 5 folds of 8 (k = 5)', size=18, weight='bold', ha='left')
    bw, bh = 0.78, 0.5
    x0 = 1.35
    for r in range(5):
        y = h - 1.15 - r * 0.62
        s.text(0.1, y + bh / 2, f'Round {r + 1}', size=16, weight='bold', ha='left')
        for c in range(5):
            test = c == r
            s.box(x0 + c * (bw + 0.06), y, bw, bh, '8', size=16, fill=GOLD if test else PAPER, lw=1.6, r=0.04, weight='bold' if test else 'normal')
    s.box(x0, 0.6, 0.5, 0.3, '', fill=GOLD, lw=1.4, r=0.03)
    s.text(x0 + 0.65, 0.75, 'test fold: held out', size=15, ha='left')
    s.box(x0 + 2.55, 0.6, 0.5, 0.3, '', fill=PAPER, lw=1.4, r=0.03)
    s.text(x0 + 3.2, 0.75, 'training folds: learn from these', size=15, ha='left')
    s.text(w / 2, 0.2, 'Score = (s1 + s2 + s3 + s4 + s5) / 5, the mean of the k scores. Then reshuffle.', size=16, color=BODY)
    return s


# ------------------------------------------------------------------ honest accuracy on 40 messages
@fig('x_t02_cv')
def x_t02_cv(w, h, **_):
    r = _res()['cv_messages']
    order = [('always the commonest', 'Majority-class baseline', GREY), ('keyword rule (no training)', 'Keyword rule (no training)', PAPER),
             ('decision tree on words', 'Decision tree on words', GOLD), ('nearest neighbours k=1 (TF-IDF)', 'Nearest neighbours, k = 1', GOLD),
             ('nearest neighbours k=3 (TF-IDF)', 'Nearest neighbours, k = 3', GOLD), ('nearest neighbours k=5 (TF-IDF)', 'Nearest neighbours, k = 5', GOLD)]
    s = Scene(w, h)
    x0, x1 = 4.5, w - 0.9
    px = lambda v: x0 + v * (x1 - x0)
    top = h - 0.6
    rh = 0.5
    for t in (0, 0.25, 0.5, 0.75, 1.0):
        s.line(px(t), 0.62, px(t), top, color=HAIR, lw=1, z=0)
        s.text(px(t), 0.35, f'{int(t * 100)}%', size=14)
    s.text(w - 0.1, h - 0.22, 'bar: average of 100 tests   line: worst to best test', size=14, color=BODY, ha='right')
    for i, (k, lab, fill) in enumerate(order):
        v = r[k]
        yc = top - (i + 0.5) * rh
        s.text(0.1, yc, lab, size=16, ha='left')
        s.rect(x0, yc - 0.17, px(v['mean']) - x0, 0.34, fill=fill, edge=INK, lw=1.6, z=3)
        if v['sd'] > 0:
            s.line(px(v['lo']), yc, px(v['hi']), yc, color=RED, lw=2.4, z=5)
            s.line(px(v['lo']), yc - 0.12, px(v['lo']), yc + 0.12, color=RED, lw=2.4, z=5)
            s.line(px(v['hi']), yc - 0.12, px(v['hi']), yc + 0.12, color=RED, lw=2.4, z=5)
        s.text(x1 + 0.1, yc, f"{v['mean'] * 100:.0f}%", size=16, weight='bold', ha='left')
    return s


# ------------------------------------------------------------------ the scale of the measurements matters
@fig('x_t02_scaling')
def x_t02_scaling(w, h, **_):
    d = _res()['scaling']
    s = Scene(w, h)
    base, top = 1.5, h - 0.7
    for i, (lab, v, fill) in enumerate((('Raw numbers', d['raw'], PAPER), ('Same scale first', d['scaled'], GOLD))):
        x = 0.9 + i * 3.3
        hh = (top - base) * v
        s.rect(x, base, 2.0, hh, fill=fill, edge=INK, lw=2, z=3)
        s.text(x + 1.0, base + hh + 0.3, f'{v * 100:.0f}%', size=26, weight='bold')
        s.text(x + 1.0, base - 0.3, lab, size=18, weight='bold')
    s.line(0.7, base, w - 0.2, base, lw=2)
    s.text(w / 2, 0.6, 'amount runs to 2,500 (UGX thousands), days to 90', size=16, color=BODY)
    s.text(w / 2, 0.15, 'min-max scaling: x\u2032 = (x \u2212 min) / (max \u2212 min)', size=16, weight='bold')
    s.text(w / 2, h - 0.3, 'Nearest neighbours, 5 neighbours, 240 fictional claims', size=16, weight='bold')
    return s


# ------------------------------------------------------------------ shared grid: houses by floor area and distance to the town centre
def _house_grid(s, ox=1.0, oy=0.85, sc=0.42, xm=8, ym=8):
    """Squared paper. Across: floor area, 4 squares = 40 m2 at the left edge, 1 square = 10 m2. Up: km to the town centre, 1 square = 1 km."""
    for i in range(xm + 1):
        s.line(ox + i * sc, oy, ox + i * sc, oy + ym * sc, color=HAIR, lw=0.9, z=0)
    for j in range(ym + 1):
        s.line(ox, oy + j * sc, ox + xm * sc, oy + j * sc, color=HAIR, lw=0.9, z=0)
    s.line(ox, oy, ox + xm * sc + 0.12, oy, lw=2, z=1)
    s.line(ox, oy, ox, oy + ym * sc + 0.12, lw=2, z=1)
    for i in range(0, xm + 1, 2):
        s.text(ox + i * sc, oy - 0.2, str(40 + 10 * i), size=14, color=BODY)
    for j in range(0, ym + 1, 2):
        s.text(ox - 0.14, oy + j * sc, str(j), size=14, color=BODY, ha='right')
    s.text(ox + xm * sc / 2, 0.17, 'Floor area, m\u00b2 (1 square = 10 m\u00b2)', size=14, color=BODY)
    s.text(0.2, oy + ym * sc / 2, 'Km to town centre', size=14, color=BODY, rot=90)
    return lambda area, km: (ox + (area / 10.0 - 4) * sc, oy + km * sc)


# ------------------------------------------------------------------ distance on squared paper (houses)
@fig('x_t02_grid')
def x_t02_grid(w, h, **_):
    s = Scene(w, h)
    to = _house_grid(s)
    n = to(80, 3)
    p = to(110, 7)
    s.line(n[0], n[1], p[0], n[1], color=MUTE, lw=2, dash=True, z=2)
    s.line(p[0], n[1], p[0], p[1], color=MUTE, lw=2, dash=True, z=2)
    s.arrow(n[0], n[1], p[0], p[1], color=RED, lw=3.2, head=14, z=6)
    s.text((n[0] + p[0]) / 2, n[1] - 0.22, '3 across', size=14, color=BODY)
    s.text(p[0] + 0.1, (n[1] + p[1]) / 2, '4 up', size=14, color=BODY, ha='left')
    for (a_, k_, lab) in ((110, 7, 'P'), (90, 4, 'Q'), (60, 4, 'R')):
        c = to(a_, k_)
        s.circle(c[0], c[1], 0.1, fill=PAPER, edge=INK, lw=1.6, z=5)
        s.text(c[0] + 0.22, c[1] + 0.18, lab, size=15, weight='bold')
    s.ax.scatter([n[0]], [n[1]], s=330, marker='*', c=RED, edgecolors=INK, linewidths=1.1, zorder=8)
    s.text(n[0] - 0.12, n[1] - 0.3, 'N', size=15, weight='bold', ha='right')
    x0 = 5.0
    cw = w - x0 - 0.1
    s.text(x0 + cw / 2, h - 0.3, 'Euclidean distance from N', size=16, weight='bold')
    rows = [('N to P', '3\u00b2 + 4\u00b2 = 25, root 5', '5', PAPER), ('N to Q', '1\u00b2 + 1\u00b2 = 2, root 1.4', '1.4', GOLD), ('N to R', '2\u00b2 + 1\u00b2 = 5, root 2.2', '2.2', PAPER)]
    for k, (a, b, c, f) in enumerate(rows):
        y = h - 1.65 - k * 1.05
        s.box(x0, y, cw, 0.95, '', fill=f, edge=INK, lw=1.8)
        s.text(x0 + 0.12, y + 0.7, a, size=16, weight='bold', ha='left')
        s.text(x0 + 0.12, y + 0.27, b, size=14, ha='left')
        s.text(x0 + cw - 0.1, y + 0.62, c, size=24, weight='bold', ha='right')
    s.text(x0 + cw / 2, 0.45, 'Smallest = nearest: Q', size=16, weight='bold', color=RED)
    return s


# ------------------------------------------------------------------ k-NN estimates a house price
@fig('x_t02_knn_house')
def x_t02_knn_house(w, h, **_):
    s = Scene(w, h)
    to = _house_grid(s)
    houses = [('A', 90, 4, 250), ('B', 60, 4, 190), ('C', 80, 1, 270), ('D', 110, 7, 330), ('E', 40, 2, 120), ('F', 100, 5, 300)]
    n = to(80, 3)
    dist = {}
    for lab, a_, k_, pr in houses:
        dist[lab] = math.hypot((a_ - 80) / 10.0, k_ - 3)
    near = sorted(dist, key=dist.get)[:3]
    for lab, a_, k_, pr in houses:
        c = to(a_, k_)
        if lab in near:
            s.circle(c[0], c[1], 0.2, fill='none', edge=RED, lw=2.8, z=6)
            s.line(n[0], n[1], c[0], c[1], color=RED, lw=1.4, dash=True, z=2)
        s.circle(c[0], c[1], 0.1, fill=GOLD if lab in near else PAPER, edge=INK, lw=1.6, z=5)
        s.text(c[0] + 0.24, c[1] + 0.2, lab, size=15, weight='bold')
    s.ax.scatter([n[0]], [n[1]], s=330, marker='*', c=RED, edgecolors=INK, linewidths=1.1, zorder=8)
    s.text(n[0] - 0.12, n[1] - 0.3, 'N', size=15, weight='bold', ha='right')
    x0 = 5.0
    cw = w - x0 - 0.1
    s.text(x0 + cw / 2, h - 0.3, 'Sold houses, nearest first', size=16, weight='bold')
    order = sorted(dist, key=dist.get)
    price = {lab: pr for lab, a_, k_, pr in houses}
    rows = [['House', 'Distance', 'Price']] + [[lab, f'{dist[lab]:.1f}', str(price[lab])] for lab in order]
    s.table(x0, h - 0.6, [0.8, 1.0, 0.9], 0.38, rows, size=15, hl_rows=(1, 2, 3), hl_fill=GOLD, align=['center'] * 3)
    avg = sum(price[l] for l in near) / 3.0
    s.text(x0 + cw / 2, 0.95, '(250 + 270 + 190) / 3', size=15, color=BODY)
    s.box(x0, 0.2, cw, 0.55, f'Estimate for N: {avg:.0f}', size=17, fill=PAPER, edge=RED, lw=2.4, weight='bold', r=0.08)
    return s


# ------------------------------------------------------------------ words first become counts (a taste of Session 4)
@fig('x_t02_counts')
def x_t02_counts(w, h, **_):
    s = Scene(w, h)
    words_ = ['pay', 'invoice', 'sugar', 'wet']
    msgs = [('M-a', 'Please can I pay my invoice', [1, 1, 0, 0]), ('M-b', 'Pay the invoice in two parts', [1, 1, 0, 0]),
            ('M-c', 'The delivered sugar is wet', [0, 0, 1, 1])]
    s.text(0.1, h - 0.3, 'Step 1: count a few words in each message (bag of words)', size=17, weight='bold', ha='left')
    x0 = 4.7
    cw = (w - x0 - 0.1) / 4
    for j, wd in enumerate(words_):
        s.text(x0 + j * cw + cw / 2, h - 0.85, wd, size=15, weight='bold')
    rh = 0.75
    for i, (mid, txt, cnt) in enumerate(msgs):
        y = h - 1.2 - (i + 1) * rh
        s.text(0.1, y + rh / 2, txt, size=15, ha='left')
        for j, v in enumerate(cnt):
            s.box(x0 + j * cw + 0.04, y + 0.12, cw - 0.08, rh - 0.24, str(v), size=18, fill=GOLD if v else PAPER, lw=1.5, r=0.04, weight='bold' if v else 'normal')
    s.text(w / 2, 1.2, 'Similar counts, so close. Different counts, so far apart.', size=16, color=BODY)
    s.box(0.05, 0.1, w - 0.1, 0.75, 'Session 4 builds this properly: TF-IDF weighting, then embeddings', size=17, fill=PAPER, edge=RED, lw=2.4, weight='bold', r=0.08)
    return s
