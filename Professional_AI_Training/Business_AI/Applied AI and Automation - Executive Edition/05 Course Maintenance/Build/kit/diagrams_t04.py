"""Figure kinds for Session 4 (Words as numbers). Numbers come from demo_runs/s04/results.json (a real recorded run of demo_runs/s04/s04_run.py).

Kinds (use as dict(kind='t04_<name>')): bow, tfidf, plane, numbers, euclid, manhattan, dot, cosine, compare4, search (skin='contracts'|'finance'|'hr'), agree, map, blank, cheat
"""
import json
import math
from pathlib import Path

import numpy as np
from matplotlib.patches import Arc, Polygon

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD, fig
import slidekit as K

_R = json.loads((Path(__file__).resolve().parent.parent / 'demo_runs' / 's04' / 'results.json').read_text())


class _Plane:
    """A drawing area in inches with unit grid: to(x, y) maps a vector (x, y) to scene inches."""
    def __init__(self, s, ox, oy, sc, xmax, ymax, grid=True, ticks=True, size=14, labels=('', '')):
        self.s, self.ox, self.oy, self.sc = s, ox, oy, sc
        if grid:
            for i in range(xmax + 1):
                s.line(ox + i * sc, oy, ox + i * sc, oy + ymax * sc, color=HAIR, lw=0.9, z=0)
            for j in range(ymax + 1):
                s.line(ox, oy + j * sc, ox + xmax * sc, oy + j * sc, color=HAIR, lw=0.9, z=0)
        s.line(ox, oy, ox + xmax * sc + 0.15, oy, lw=2.0, z=1)
        s.line(ox, oy, ox, oy + ymax * sc + 0.15, lw=2.0, z=1)
        if ticks:
            for i in range(0, xmax + 1, 2 if xmax > 6 else 1):
                s.text(ox + i * sc, oy - 0.2, str(i), size=size, color=MUTE)
            for j in range(0, ymax + 1, 2 if ymax > 6 else 1):
                s.text(ox - 0.2, oy + j * sc, str(j), size=size, color=MUTE)
        if labels[0]:
            s.text(ox + xmax * sc / 2, oy - 0.52, labels[0], size=size, color=MUTE)
        if labels[1]:
            s.text(ox - 0.58, oy + ymax * sc / 2, labels[1], size=size, color=MUTE, rot=90)

    def to(self, x, y):
        return self.ox + x * self.sc, self.oy + y * self.sc

    def arrow(self, x, y, color=INK, lw=3.0, x0=0, y0=0, label=None, dx=0.12, dy=0.12, ha='left', size=16, head=18, dash=False):
        a, b = self.to(x0, y0)
        c, d = self.to(x, y)
        self.s.arrow(a, b, c, d, color=color, lw=lw, head=head, dash=dash)
        if label:
            self.s.text(c + dx, d + dy, label, size=size, weight='bold', color=color if color != GOLD else INK, ha=ha)

    def dot(self, x, y, color=INK, r=0.07):
        c, d = self.to(x, y)
        self.s.circle(c, d, r, fill=color, edge=INK, lw=1.2, z=5)


def _card(s, x, y, w, h, head, big, sub=None, fill=PAPER, hsize=16, bsize=26):
    s.box(x, y, w, h, '', fill=fill, edge=INK, lw=1.8)
    s.text(x + w / 2, y + h - 0.28, head, size=hsize, weight='bold')
    s.text(x + w / 2, y + h / 2 - 0.05, big, size=bsize, weight='bold')
    if sub:
        s.text(x + w / 2, y + 0.26, sub, size=14, color=BODY)


# ------------------------------------------------------------------ 1. bag of words
@fig('x_t04_bow')
def bow(w, h, **_):
    s = Scene(w, h)
    B = _R['bow']
    show = ['maize', 'flour', 'send', 'invoice', 'rice', 'late', 'the']
    idx = [B['vocab'].index(v) for v in show]
    y = h - 0.15
    for i, t in zip(B['ids'], B['texts']):
        s.text(0.05, y - 0.18, f'{i}', size=15, weight='bold', ha='left')
        s.text(0.45, y - 0.18, t, size=15, ha='left')
        y -= 0.37
    top = y - 0.2
    cw = [0.55] + [0.97] * len(show)
    sc = (w - 0.1) / sum(cw)
    cw = [c * sc for c in cw]
    rows = [[''] + show] + [[i] + [str(B['counts'][r][j]) for j in idx] for r, i in enumerate(B['ids'])]
    hl = {(r + 1, c + 1): GOLD for r in range(4) for c in range(len(show)) if B['counts'][r][idx[c]] > 0}
    s.table(0.05, top, cw, (top - 0.1) / 5, rows, size=16, hl_cells=hl)
    return s


# ------------------------------------------------------------------ 2. tf-idf on message M06
@fig('x_t04_tfidf')
def tfidf(w, h, **_):
    s = Scene(w, h)
    M = {m['word']: m for m in _R['m06_words']}
    words = ['jerrycan', 'invoice', 'oil', 'send', 'please', 'the']
    rows = [['Word in M06', 'Count', 'In how many\nof 40 messages', 'Count × 40 ÷ that', 'Real TF-IDF']]
    for wd in words:
        m = M[wd]
        rows.append([wd, str(m['count']), str(m['in_messages']), f"{m['count']} × 40 ÷ {m['in_messages']} = {m['simple']:g}", f"{m['real']:.3f}"])
    cw = [1.5, 0.85, 1.5, 2.45, 1.4]
    sc = (w - 0.1) / sum(cw)
    cw = [c * sc for c in cw]
    rh = (h - 0.1) / 7.3
    s.table(0.05, h - 0.05, cw, rh, [rows[0]] + rows[1:], size=15, hl_cols=(), hl_cells={(r, 3): GOLD for r in (1, 2)}, align=['left', 'center', 'center', 'left', 'center'])
    return s


# ------------------------------------------------------------------ 3. words as arrows in a plane
@fig('x_t04_plane')
def plane(w, h, **_):
    s = Scene(w, h)
    P = _Plane(s, 1.0, 0.95, 0.56, 7, 6, labels=('how much the word is about money', 'about trucks'))
    items = [('invoice', 4, 1, INK, 0.12, -0.28), ('receipt', 3, 1.5, INK, -0.1, 0.35), ('lorry', 1, 4, RED, 0.14, 0.05), ('truck', 1.5, 3.3, RED, 0.12, -0.3)]
    for nm, x, y, c, dx, dy in items:
        P.arrow(x, y, color=c, label=None)
    s.text(P.to(4, 1)[0] + 0.2, P.to(4, 1)[1] - 0.3, 'invoice (4, 1)', size=15, weight='bold', ha='left')
    s.text(P.to(3, 1.5)[0] - 0.05, P.to(3, 1.5)[1] + 0.38, 'receipt (3, 1.5)', size=15, weight='bold', ha='center')
    s.text(P.to(1, 4)[0] + 0.15, P.to(1, 4)[1] + 0.1, 'lorry (1, 4)', size=15, weight='bold', color=RED, ha='left')
    s.text(P.to(1.5, 3.3)[0] + 0.2, P.to(1.5, 3.3)[1] - 0.3, 'truck (1.5, 3.3)', size=15, weight='bold', color=RED, ha='left')
    s.box(5.15, 2.9, w - 5.3, 1.35, 'Money words\npoint to the right', size=16, fill=PAPER, lw=1.8)
    s.box(5.15, 1.2, w - 5.3, 1.35, 'Truck words\npoint upwards', size=16, fill=PAPER, lw=1.8, edge=RED)
    return s


# ------------------------------------------------------------------ 4. the first numbers of a real embedding
@fig('x_t04_numbers')
def numbers(w, h, **_):
    s = Scene(w, h)
    V = _R['sample_vectors']
    rows = [('Plain question', 'What happens if heavy rain floods the road...', V['first8']['query'], None),
            ('Clause: Force majeure', 'events beyond its reasonable control, including flood...', V['first8']['K1'], V['cos_q_K1']),
            ('Clause: Governing law', 'governed by the laws of Uganda...', V['first8']['K8'], V['cos_q_K8'])]
    rh = 1.05
    x0 = 3.3
    cw = (w - x0 - 2.45) / 9
    s.text(x0, h - 0.2, 'the first 8 of 384 numbers', size=15, color=MUTE, ha='left')
    s.text(w - 1.2, h - 0.35, 'similarity to\nthe question', size=15, color=MUTE)
    for i, (nm, sub, vec, cs) in enumerate(rows):
        y = h - 0.55 - (i + 1) * rh
        s.text(0.05, y + rh * 0.62, nm, size=17, weight='bold', ha='left')
        s.text(0.05, y + rh * 0.22, sub[:36] + ('...' if len(sub) > 36 else ''), size=14, color=BODY, ha='left') if False else None
        for j, v in enumerate(vec):
            s.box(x0 + j * cw, y + 0.2, cw - 0.05, 0.62, f'{v:+.2f}'.replace('-', '−'), size=15, fill=GOLD if (cs and cs > 0.3) else PAPER, lw=1.3, r=0.04)
        s.text(x0 + 8 * cw + 0.2, y + 0.51, '...', size=20, weight='bold')
        s.text(w - 1.2, y + 0.51, '' if cs is None else f'{cs:.2f}', size=24, weight='bold')
    return s


# ------------------------------------------------------------------ 5. Euclidean
@fig('x_t04_euclid')
def euclid(w, h, **_):
    s = Scene(w, h)
    P = _Plane(s, 0.7, 0.75, 0.43, 7, 9, labels=('', ''))
    a, b = P.to(3, 4), P.to(6, 8)
    P.arrow(3, 4, color=INK, label='a (3, 4)', dx=-0.2, dy=0.25, ha='right')
    P.arrow(6, 8, color=GREY, label='b (6, 8)', dx=-0.12, dy=0.2, ha='right')
    s.line(a[0], a[1], b[0], a[1], color=MUTE, lw=2, dash=True, z=2)
    s.line(b[0], a[1], b[0], b[1], color=MUTE, lw=2, dash=True, z=2)
    s.arrow(a[0], a[1], b[0], b[1], color=RED, lw=3.4, head=16, z=6)
    s.text((a[0] + b[0]) / 2, a[1] - 0.22, '3 across', size=15, color=BODY)
    s.text(b[0] + 0.1, (a[1] + b[1]) / 2, '4 up', size=15, color=BODY, ha='left')
    s.text(5.3, 3.9, 'Straight line from a to b', size=17, weight='bold', ha='left') if False else None
    s.box(5.0, 2.4, w - 5.15, 1.9, '', fill=GOLD, edge=INK, lw=2)
    s.text(5.0 + (w - 5.15) / 2, 3.75, 'Straight line', size=18, weight='bold')
    s.text(5.0 + (w - 5.15) / 2, 3.15, '3 across, 4 up', size=17)
    s.text(5.0 + (w - 5.15) / 2, 2.7, '= 5', size=30, weight='bold')
    return s


# ------------------------------------------------------------------ 6. Manhattan
@fig('x_t04_manhattan')
def manhattan(w, h, **_):
    s = Scene(w, h)
    P = _Plane(s, 0.7, 0.75, 0.43, 7, 9, labels=('', ''))
    a, b = P.to(3, 4), P.to(6, 8)
    pts = [(3, 4), (3, 5), (4, 5), (4, 6), (5, 6), (5, 7), (6, 7), (6, 8)]   # stairs of city blocks: 3 across and 4 up
    s.arrow(a[0], a[1], b[0], b[1], color=HAIR, lw=2.6, head=12, z=2)
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        p, q = P.to(x1, y1), P.to(x2, y2)
        s.line(p[0], p[1], q[0], q[1], color=RED, lw=4.2, z=5)
    P.dot(3, 4, INK)
    P.dot(6, 8, INK)
    s.text(a[0] - 0.15, a[1] - 0.25, 'a', size=17, weight='bold', ha='right')
    s.text(b[0] - 0.15, b[1] + 0.2, 'b', size=17, weight='bold', ha='right')
    s.box(5.0, 2.4, w - 5.15, 1.9, '', fill=GOLD, edge=INK, lw=2)
    s.text(5.0 + (w - 5.15) / 2, 3.75, 'City blocks', size=18, weight='bold')
    s.text(5.0 + (w - 5.15) / 2, 3.15, '3 across + 4 up', size=17)
    s.text(5.0 + (w - 5.15) / 2, 2.7, '= 7', size=30, weight='bold')
    s.text(5.0 + (w - 5.15) / 2, 1.6, 'Grey line: the straight\nline, 5', size=15, color=MUTE)
    return s


# ------------------------------------------------------------------ 7. dot product
@fig('x_t04_dot')
def dot(w, h, **_):
    s = Scene(w, h)
    P = _Plane(s, 0.7, 0.75, 0.43, 7, 9, labels=('', ''))
    P.arrow(3, 4, color=INK, label='a', dx=-0.2, dy=0.15, ha='right')
    P.arrow(6, 8, color=GREY, label='b', dx=-0.12, dy=0.2, ha='right')
    P.arrow(4, 3, color=RED, label='c', dx=0.1, dy=-0.2, ha='left')
    x0 = 4.35
    cw = w - x0 - 0.1
    for k, (head, who, r1, r2, tot, fill) in enumerate((('a with b', 'b', '3 × 6 = 18', '4 × 8 = 32', '50', GOLD), ('a with c', 'c', '3 × 4 = 12', '4 × 3 = 12', '24', PAPER))):
        y = h - 2.3 - k * 2.35
        s.box(x0, y, cw, 2.1, '', fill=fill, edge=INK, lw=2)
        s.text(x0 + cw / 2, y + 1.78, head, size=18, weight='bold')
        s.text(x0 + cw / 2, y + 1.32, r1 + '   (across)', size=16)
        s.text(x0 + cw / 2, y + 0.92, r2 + '   (up)', size=16)
        s.text(x0 + cw / 2, y + 0.36, 'add: ' + tot, size=24, weight='bold')
    return s


# ------------------------------------------------------------------ 8. cosine
@fig('x_t04_cosine')
def cosine(w, h, **_):
    s = Scene(w, h)
    P = _Plane(s, 0.7, 0.75, 0.43, 7, 9, labels=('', ''))
    P.arrow(6, 8, color=GREY, lw=5, head=16)
    P.arrow(3, 4, color=INK, label='a  and  b point the same way', dx=-0.6, dy=-0.3, ha='left', size=14) if False else P.arrow(3, 4, color=INK)
    P.arrow(4, 3, color=RED)
    o = P.to(0, 0)
    s.text(P.to(6, 8)[0] - 0.1, P.to(6, 8)[1] + 0.2, 'b', size=17, weight='bold', ha='right')
    s.text(P.to(3, 4)[0] - 0.2, P.to(3, 4)[1] + 0.1, 'a', size=17, weight='bold', ha='right')
    s.text(P.to(4, 3)[0] + 0.12, P.to(4, 3)[1] - 0.15, 'c', size=17, weight='bold', color=RED, ha='left')
    s.ax.add_patch(Arc(o, 4.2, 4.2, theta1=36.87, theta2=53.13, color=RED, lw=3.4, zorder=6))
    s.text(o[0] + 2.6 * math.cos(math.radians(45)), o[1] + 2.6 * math.sin(math.radians(45)), '16°', size=16, weight='bold', color=RED)
    x0 = 4.85
    cw = w - x0 - 0.1
    s.box(x0, 3.05, cw, 1.55, '', fill=GOLD, edge=INK, lw=2)
    s.text(x0 + cw / 2, 4.3, 'a and b: no angle', size=17, weight='bold')
    s.text(x0 + cw / 2, 3.65, 'cosine 1.00', size=24, weight='bold')
    s.box(x0, 1.2, cw, 1.6, '', fill=PAPER, edge=INK, lw=2)
    s.text(x0 + cw / 2, 2.5, 'a and c: 16°', size=17, weight='bold')
    s.text(x0 + cw / 2, 1.85, 'cosine 0.96', size=24, weight='bold')
    s.text(x0 + cw / 2, 1.42, '24 ÷ (5 × 5)', size=15, color=BODY)
    return s


# ------------------------------------------------------------------ 9. the four measures disagree on the toy vectors
@fig('x_t04_compare4')
def compare4(w, h, **_):
    s = Scene(w, h)
    rows = [['Measure', 'a to b\n(long arrow)', 'a to c\n(short arrow)', 'Closer to a'],
            ['Straight line', '5', '1.4', 'c'], ['City blocks', '7', '2', 'c'], ['Agreement score', '50', '24', 'b'], ['Cosine of the angle', '1.00', '0.96', 'b']]
    cw = [2.6, 1.7, 1.7, 1.55]
    sc = (w - 0.1) / sum(cw)
    cw = [c * sc for c in cw]
    rh = (h - 0.9) / 5
    hl = {(1, 3): GOLD, (2, 3): GOLD, (3, 3): RED, (4, 3): RED}
    s.table(0.05, h - 0.05, cw, rh * 1.3 if False else rh, rows, size=17, hl_cells={(1, 3): GOLD, (2, 3): GOLD, (3, 3): GOLD, (4, 3): GOLD}, align=['left', 'center', 'center', 'center'])
    s.text(0.1, 0.62, 'Straight line and city blocks: smaller is closer.', size=15, color=BODY, ha='left')
    s.text(0.1, 0.25, 'Agreement score and cosine: bigger is closer.', size=15, color=BODY, ha='left')
    return s


# ------------------------------------------------------------------ 10. semantic search results (one skin)
@fig('x_t04_search')
def search(w, h, skin='contracts', **_):
    s = Scene(w, h)
    S = _R['skins'][skin]
    Q = S['queries']
    cw = [3.9, 2.0, 2.0, 2.0, 2.0]
    sc = (w - 0.1) / sum(cw)
    cw = [c * sc for c in cw]
    xs = [0.05]
    for c in cw:
        xs.append(xs[-1] + c)
    top = h - 0.05
    hh = 0.42
    for j, t in enumerate(['A plain description', 'Meaning search: 1st', '2nd', '3rd', 'Word search: 1st']):
        s.text(xs[j] + 0.1 if j == 0 else (xs[j] + xs[j + 1]) / 2, top - hh / 2, t, size=15, weight='bold', ha='left' if j == 0 else 'center')
    s.line(0.05, top - hh, w - 0.05, top - hh, lw=2)
    rh = (h - hh - 0.1) / len(Q)
    for i, q in enumerate(Q):
        y1 = top - hh - i * rh
        yc = y1 - rh / 2
        lines = K.wrap(q['query'], 15, 'regular', cw[0] - 0.25)
        s.text(xs[0] + 0.1, yc, '\n'.join(lines), size=15, ha='left')
        for j, t3 in enumerate(q['top3']):
            right = t3['id'] == q['want']
            if right:
                s.rect(xs[j + 1] + 0.05, y1 - rh + 0.06, cw[j + 1] - 0.1, rh - 0.12, fill=GOLD, edge=INK, lw=1.2, z=1)
            nm = '\n'.join(K.wrap(t3['head'], 14, 'bold' if right else 'regular', cw[j + 1] - 0.3))
            s.text((xs[j + 1] + xs[j + 2]) / 2, yc + 0.1, nm, size=14, weight='bold' if right else 'normal')
            s.text((xs[j + 1] + xs[j + 2]) / 2, y1 - rh + 0.2, f"{t3['cosine']:.2f}", size=14, color=BODY)
        kw = q['keyword_top']
        if not kw:
            s.text((xs[4] + xs[5]) / 2, yc, 'no word in common', size=14, color=RED, weight='bold')
        else:
            right = q['keyword_hit_at1']
            if right:
                s.rect(xs[4] + 0.05, y1 - rh + 0.06, cw[4] - 0.1, rh - 0.12, fill=GOLD, edge=INK, lw=1.2, z=1)
            nm = '\n'.join(K.wrap(kw[0]['head'], 14, 'bold' if right else 'regular', cw[4] - 0.3))
            s.text((xs[4] + xs[5]) / 2, yc, nm, size=14, weight='bold' if right else 'normal')
        s.line(0.05, y1 - rh, w - 0.05, y1 - rh, color=HAIR, lw=0.9)
    return s


# ------------------------------------------------------------------ 11. agree and disagree on real vectors
@fig('x_t04_agree')
def agree(w, h, **_):
    s = Scene(w, h)
    pr = _R['pair_examples'][1]['raw']
    a, b = pr['F5'], pr['F10']
    rows = [['Query: "Make sure our books\nmatch what the bank says."', 'Bank\nreconciliation', 'Bad debt\nwrite-off'],
            ['Length of the arrow', f"{a['length']:.2f}", f"{b['length']:.2f}"],
            ['Straight line (smaller wins)', f"{a['euclid']:.2f}", f"{b['euclid']:.2f}"],
            ['City blocks (smaller wins)', f"{a['manhattan']:.1f}", f"{b['manhattan']:.1f}"],
            ['Agreement score (bigger wins)', f"{a['dot']:.2f}", f"{b['dot']:.2f}"],
            ['Cosine (bigger wins)', f"{a['cosine']:.3f}", f"{b['cosine']:.3f}"]]
    cw = [3.7, 1.75, 1.75]
    sc = (w - 0.1) / sum(cw)
    cw = [c * sc for c in cw]
    rh = (h - 1.3) / 6.3
    hl = {(2, 1): GOLD, (3, 1): GOLD, (4, 2): GOLD, (5, 2): GOLD}
    s.table(0.05, h - 0.05, cw, rh, rows, size=15, hl_cells=hl, align=['left', 'center', 'center'])
    Rs = _R['summary']
    s.text(0.1, 1.0, 'Gold marks the closer answer for each measure.', size=14, color=BODY, ha='left')
    s.text(0.1, 0.62, f"Length-1 vectors: all four pick the same top answer in {Rs['all_four_agree_top1']} of {Rs['n_queries']} searches.", size=14, color=BODY, ha='left')
    s.text(0.1, 0.25, f"Lengths left alone, as in this table: all four agree in {Rs['raw_all_four_agree_top1']} of {Rs['n_queries']}.", size=14, color=BODY, ha='left')
    return s


# ------------------------------------------------------------------ 12. a 2D map of the 384-number vectors
@fig('x_t04_map')
def mapfig(w, h, **_):
    s = Scene(w, h)
    pts = _R['pca']['points']
    xs = [p['x'] for p in pts]
    ys = [p['y'] for p in pts]
    x0, x1, y0, y1 = 0.35, w - 0.3, 0.85, h - 0.65
    px = lambda v: x0 + (v - min(xs)) / (max(xs) - min(xs)) * (x1 - x0 - 0.2) + 0.1
    py = lambda v: y0 + (v - min(ys)) / (max(ys) - min(ys)) * (y1 - y0 - 0.2) + 0.1
    s.rect(x0, y0, x1 - x0, y1 - y0, fill=PAPER, edge=HAIR, lw=1.2, z=0)
    col = {'contracts': INK, 'finance': GOLD, 'hr': RED}
    byid = {p['id']: p for p in pts}
    for sk, d in _R['skins'].items():
        for q in d['queries']:
            qp, ap = byid[q['qid']], byid[q['want']]
            s.line(px(qp['x']), py(qp['y']), px(ap['x']), py(ap['y']), color=GREY, lw=1.3, dash=True, z=1)
    for p in pts:
        if p['kind'] == 'passage':
            s.circle(px(p['x']), py(p['y']), 0.11, fill=col[p['skin']], edge=INK, lw=1.3, z=4)
        else:
            s.ax.scatter([px(p['x'])], [py(p['y'])], marker='*', s=260, c=PAPER, edgecolors=INK, linewidths=1.6, zorder=6)
    lx = 0.4
    for sk, t in (('contracts', 'Contract clauses'), ('finance', 'Finance terms'), ('hr', 'HR policy')):
        s.circle(lx + 0.1, h - 0.3, 0.11, fill=col[sk], edge=INK, lw=1.3, z=4)
        s.text(lx + 0.3, h - 0.3, t, size=16, weight='bold', ha='left')
        lx += 0.5 + 0.115 * len(t) * 1.15
    ex = _R['pca']['explained']
    s.text(0.4, 0.55, 'Dots: passages. Stars: plain descriptions. Dashed: to the right answer.', size=14, color=BODY, ha='left')
    s.text(0.4, 0.2, f"The map keeps only {100 * _R['pca']['total']:.0f}% of the information in the 384 numbers.", size=14, color=BODY, ha='left')
    return s


# ------------------------------------------------------------------ 13. blank table for the hands-on exercise
@fig('x_t04_blank')
def blank(w, h, size=15, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.28, 'A = (3, 4)    B = (3, 1)    C = (6, 0)', size=17, weight='bold', ha='left')
    s.text(0.1, h - 0.68, 'lengths: A 5, B 3.16, C 6', size=15, color=BODY, ha='left')
    rows = [['Pair', 'Straight\nline', 'City\nblocks', 'Agree-\nment', 'Cosine'], ['A to B', '?', '?', '?', '?'], ['A to C', '?', '?', '?', '?'], ['B to C', '?', '?', '?', '?']]
    cw = [1.15, 1.05, 1.05, 1.05, 1.1]
    sc = (w - 0.1) / sum(cw)
    cw = [c * sc for c in cw]
    s.table(0.05, h - 0.95, cw, (h - 1.0) / 4.1, rows, size=size)
    return s


# ------------------------------------------------------------------ 14. the distance cheat sheet (one panel per measure)
def _mini(s, kind, x, y, w, h):
    """A small drawing in the box (x, y, w, h)."""
    ax_, ay_ = x + 0.25, y + 0.2
    bx_, by_ = x + w - 0.3, y + h - 0.2
    s.line(ax_, ay_, x + w - 0.1, ay_, color=HAIR, lw=1.2)
    s.line(ax_, ay_, ax_, y + h - 0.05, color=HAIR, lw=1.2)
    if kind == 'euclid':
        s.arrow(ax_, ay_, bx_, by_, color=GREY, lw=2, head=11)
        s.arrow(ax_ + 0.5, ay_ + 0.3, bx_, by_, color=RED, lw=3.2, head=13, z=6)
        s.circle(ax_ + 0.5, ay_ + 0.3, 0.06, fill=INK)
    elif kind == 'manhattan':
        pts = [(ax_ + 0.5, ay_ + 0.3), (ax_ + 0.5, ay_ + 0.7), (ax_ + 1.0, ay_ + 0.7), (ax_ + 1.0, by_ - 0.2), (bx_, by_ - 0.2), (bx_, by_)]
        for p, q in zip(pts, pts[1:]):
            s.line(p[0], p[1], q[0], q[1], color=RED, lw=3.2, z=6)
        s.circle(*pts[0], 0.06, fill=INK)
    elif kind == 'dot':
        s.arrow(ax_, ay_, ax_ + 0.9, ay_ + 1.0, color=INK, lw=2.6, head=12)
        s.arrow(ax_, ay_, bx_, by_ - 0.1, color=GREY, lw=3.6, head=12)
        s.text(x + w / 2 + 0.3, y + h * 0.25, 'long arrows score higher', size=14, color=RED, weight='bold') if False else None
    else:
        s.arrow(ax_, ay_, ax_ + 1.0, ay_ + 1.15, color=INK, lw=2.6, head=12)
        s.arrow(ax_, ay_, ax_ + 1.45, ay_ + 0.85, color=RED, lw=2.6, head=12)
        s.ax.add_patch(Arc((ax_, ay_), 1.3, 1.3, theta1=40.2, theta2=49.0, color=RED, lw=3, zorder=6))


@fig('x_t04_cheat')
def cheat(w, h, **_):
    s = Scene(w, h)
    cols = [('Euclidean', 'straight line', 'euclid', 'Smaller is closer.', 'Sees length and direction.'),
            ('Manhattan', 'city blocks', 'manhattan', 'Smaller is closer.', 'Adds up every difference.'),
            ('Dot product', 'agreement score', 'dot', 'Bigger is closer.', 'Rewards long arrows.'),
            ('Cosine', 'angle', 'cosine', 'Bigger is closer.', 'Ignores length.')]
    pw = (w - 0.4) / 4
    for i, (nm, nick, kind, rule, note) in enumerate(cols):
        x = 0.05 + i * (pw + 0.1)
        s.box(x, 0.05, pw, h - 0.1, '', fill=PAPER, edge=INK, lw=1.8)
        _mini(s, kind, x + 0.05, h - 1.95, pw - 0.1, 1.7)
        s.text(x + pw / 2, h - 2.25, nm, size=19, weight='bold')
        s.text(x + pw / 2, h - 2.65, nick, size=16, color=RED, weight='bold')
        s.text(x + pw / 2, h - 3.15, rule, size=15)
        s.text(x + pw / 2, h - 3.55, note, size=14, color=BODY)
    return s
