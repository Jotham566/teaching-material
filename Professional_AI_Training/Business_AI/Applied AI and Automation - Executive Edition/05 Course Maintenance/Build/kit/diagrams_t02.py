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


# ------------------------------------------------------------------ labelled examples
@fig('x_t02_labelled')
def x_t02_labelled(w, h, **_):
    rows = list(csv.DictReader(open(RUN / 'customer_messages.csv')))
    key = {r['id']: r['true_category'] for r in csv.DictReader(open(RUN / 'customer_messages_key.csv'))}
    by = {r['id']: r['text'] for r in rows}
    pick = [('M01', 62), ('M02', 62), ('M03', 62), ('M09', 62)]
    s = Scene(w, h)
    s.text(0.1, h - 0.3, 'The example (what it sees)', size=17, weight='bold', ha='left')
    s.text(w - 1.0, h - 0.3, 'The label', size=17, weight='bold', ha='center', color=RED)
    top = h - 0.6
    rh = 0.95
    for i, (mid, n) in enumerate(pick):
        y = top - (i + 1) * rh
        s.box(0.05, y + 0.08, w - 2.2, rh - 0.16, '', fill=PAPER, lw=1.6, r=0.06)
        lines = K.wrap(mid + ': ' + _short(by[mid], n), 16, 'regular', w - 2.6)
        s.text(0.2, y + rh / 2, '\n'.join(lines[:2]), size=16, ha='left')
        s.arrow(w - 2.1, y + rh / 2, w - 1.85, y + rh / 2, lw=2)
        cat = key[mid]
        s.box(w - 1.75, y + 0.17, 1.65, rh - 0.34, cat, size=17, fill=GOLD, lw=1.8, weight='bold', r=0.08)
    s.text(w / 2, 0.25, 'Real NVF messages, shortened. The label comes from the answer key.', size=15, color=BODY)
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
    s.text(0.1, h - 0.3, '40 messages in 5 groups of 8', size=18, weight='bold', ha='left')
    bw, bh = 0.78, 0.5
    x0 = 1.35
    for r in range(5):
        y = h - 1.15 - r * 0.62
        s.text(0.1, y + bh / 2, f'Round {r + 1}', size=16, weight='bold', ha='left')
        for c in range(5):
            test = c == r
            s.box(x0 + c * (bw + 0.06), y, bw, bh, '8', size=16, fill=GOLD if test else PAPER, lw=1.6, r=0.04, weight='bold' if test else 'normal')
    s.box(x0, 0.6, 0.5, 0.3, '', fill=GOLD, lw=1.4, r=0.03)
    s.text(x0 + 0.65, 0.75, 'test: keep hidden', size=15, ha='left')
    s.box(x0 + 2.55, 0.6, 0.5, 0.3, '', fill=PAPER, lw=1.4, r=0.03)
    s.text(x0 + 3.2, 0.75, 'train: learn from these', size=15, ha='left')
    s.text(w / 2, 0.2, 'Average the five scores. Then reshuffle and repeat.', size=16, color=BODY)
    return s


# ------------------------------------------------------------------ honest accuracy on 40 messages
@fig('x_t02_cv')
def x_t02_cv(w, h, **_):
    r = _res()['cv_messages']
    order = [('always the commonest', 'Always say the commonest category', GREY), ('keyword rule (no training)', 'Keyword rule (no training)', PAPER),
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
    s.text(w / 2, h - 0.3, 'Nearest neighbours, 5 neighbours, 240 fictional claims', size=16, weight='bold')
    return s
