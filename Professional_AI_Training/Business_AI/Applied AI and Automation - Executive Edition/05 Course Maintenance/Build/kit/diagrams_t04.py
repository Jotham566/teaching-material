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
    """The recorded run used scikit-learn TfidfVectorizer defaults: idf = ln((1 + N) / (1 + df)) + 1, weight = tf x idf, then each message vector divided by its length."""
    s = Scene(w, h)
    M = {m['word']: m for m in _R['m06_words']}
    words = ['jerrycan', 'invoice', 'oil', 'send', 'please', 'the']
    N = 40
    idf = lambda df: math.log((1 + N) / (1 + df)) + 1
    length = math.sqrt(sum((m['count'] * idf(m['in_messages'])) ** 2 for m in _R['m06_words']))
    rows = [['Term in\nmessage M06', 'tf', 'df', 'Simplified:\ntf × N ÷ df', 'idf (scikit-learn)\nln(41 ÷ (1 + df)) + 1', f'Real weight: tf × idf ÷ {length:.2f}']]
    for wd in words:
        m = M[wd]
        v = m['count'] * idf(m['in_messages']) / length
        assert abs(v - m['real']) < 0.0006, (wd, v, m['real'])
        rows.append([wd, str(m['count']), str(m['in_messages']), f"{m['count']} × 40 ÷ {m['in_messages']} = {m['simple']:g}", f"{idf(m['in_messages']):.2f}",
                     f"{m['count']} × {idf(m['in_messages']):.2f} ÷ {length:.2f} = {m['real']:.3f}"])
    cw = [1.55, 0.7, 0.7, 2.5, 2.6, 3.4]
    sc = (w - 0.1) / sum(cw)
    cw = [c * sc for c in cw]
    rh = (h - 1.25) / 7
    s.table(0.05, h - 0.05, cw, rh, rows, size=14, hl_cells={(r, 3): GOLD for r in (1, 2)}, align=['left', 'center', 'center', 'center', 'center', 'center'])
    s.text(0.1, 0.9, 'TF-IDF(t, d) = tf(t, d) × idf(t), idf(t) = ln[(1 + N) ÷ (1 + df(t))] + 1, then divide by the length of the message vector.', size=14, weight='bold', ha='left')
    s.text(0.1, 0.55, 't: a term. d: a message. N = 40 messages. df(t): messages containing t. ln: natural logarithm. This is scikit-learn\'s default, used in the run.', size=14, color=BODY, ha='left')
    s.text(0.1, 0.2, 'Textbook form: tf × log(N ÷ df). The simplified column drops the log. Rare term (small df): high weight.', size=14, color=BODY, ha='left')
    return s


# ------------------------------------------------------------------ 3. words as arrows in a plane
@fig('x_t04_plane')
def plane(w, h, **_):
    s = Scene(w, h)
    P = _Plane(s, 1.0, 0.95, 0.56, 7, 6, labels=('dimension 1: about money', 'dimension 2: trucks'))
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



# ------------------------------------------------------------------ 3b. a network produces the vector (simplified)
@fig('x_t04_network')
def network(w, h, **_):
    s = Scene(w, h)
    V = _R['sample_vectors']['first8']['query']
    cy = h / 2 + 0.25
    # left: the text
    s.box(0.1, cy - 0.85, 2.7, 1.7, 'What happens if\nheavy rain floods\nthe road...', size=16, fill=PAPER, lw=2)
    s.text(1.45, cy + 1.2, 'Text goes in', size=17, weight='bold')
    # middle: a small network, drawn like Session 1
    cols = [4.0, 5.2, 6.4]
    ys = [[cy + 0.9 - k * 0.45 for k in range(5)], [cy + 0.9 - k * 0.45 for k in range(5)], [cy + 0.9 - k * 0.45 for k in range(5)]]
    for a in range(2):
        for ya in ys[a]:
            for yb in ys[a + 1]:
                s.line(cols[a], ya, cols[a + 1], yb, color=HAIR, lw=0.9, z=1)
    for c, col in zip(cols, ys):
        for yy in col:
            s.circle(c, yy, 0.14, fill=PAPER, edge=INK, lw=1.6, z=4)
    s.arrow(2.85, cy, 3.75, cy, lw=2.4)
    s.arrow(6.6, cy, 7.5, cy, lw=2.4)
    s.text(5.2, cy + 1.45, 'A network like Session 1\'s', size=17, weight='bold')
    s.text(5.2, cy - 1.3, 'drawn small: the real one is much bigger', size=14, color=MUTE)
    # right: the 384 numbers
    s.text(9.5, cy + 1.45, '384 numbers out', size=17, weight='bold')
    for j, v in enumerate(V[:6]):
        s.box(8.55, cy + 0.95 - j * 0.38, 1.9, 0.34, f'{v:+.2f}'.replace('-', '\u2212'), size=14, fill=GOLD, lw=1.3, r=0.04)
    s.text(9.5, cy - 1.3, '... and 378 more', size=14, color=MUTE)
    # bottom: how it was trained
    s.box(0.1, 0.02, w - 0.2, 0.42, 'Trained on over a billion pairs of related sentences, so that similar meanings land close. Simplified.', size=14, fill=PALE, lw=1.2)
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
    s.text(w - 1.2, h - 0.35, 'cosine\nsimilarity', size=15, color=MUTE)
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
    s.text(5.0 + (w - 5.15) / 2, 3.75, 'Euclidean distance', size=18, weight='bold')
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
    s.text(5.0 + (w - 5.15) / 2, 3.75, 'Manhattan distance', size=18, weight='bold')
    s.text(5.0 + (w - 5.15) / 2, 3.15, '3 across + 4 up', size=17)
    s.text(5.0 + (w - 5.15) / 2, 2.7, '= 7', size=30, weight='bold')
    s.text(5.0 + (w - 5.15) / 2, 1.6, 'Grey: the Euclidean\ndistance, 5', size=15, color=MUTE)
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
    rows = [['Measure', 'Ana to Ben\n(long arrow)', 'Ana to Chloe\n(short arrow)', 'Closer\nto Ana'],
            ['Euclidean distance', '5', '1.4', 'Chloe'], ['Manhattan distance', '7', '2', 'Chloe'], ['Dot product', '50', '24', 'Ben'], ['Cosine similarity', '1.00', '0.96', 'Ben']]
    cw = [2.5, 1.55, 1.75, 1.2]
    sc = (w - 0.1) / sum(cw)
    cw = [c * sc for c in cw]
    rh = (h - 0.9) / 5
    hl = {(1, 3): GOLD, (2, 3): GOLD, (3, 3): RED, (4, 3): RED}
    s.table(0.05, h - 0.05, cw, rh * 1.3 if False else rh, rows, size=17, hl_cells={(1, 3): GOLD, (2, 3): GOLD, (3, 3): GOLD, (4, 3): GOLD}, align=['left', 'center', 'center', 'center'])
    s.text(0.1, 0.62, 'Euclidean and Manhattan distance: smaller is closer.', size=15, color=BODY, ha='left')
    s.text(0.1, 0.25, 'Dot product and cosine similarity: bigger is closer.', size=15, color=BODY, ha='left')
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
    for j, t in enumerate(['A plain description', 'Semantic: 1st', '2nd', '3rd', 'Keyword: 1st']):
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
            ['Euclidean distance (smaller wins)', f"{a['euclid']:.2f}", f"{b['euclid']:.2f}"],
            ['Manhattan distance (smaller wins)', f"{a['manhattan']:.1f}", f"{b['manhattan']:.1f}"],
            ['Dot product (bigger wins)', f"{a['dot']:.2f}", f"{b['dot']:.2f}"],
            ['Cosine similarity (bigger wins)', f"{a['cosine']:.3f}", f"{b['cosine']:.3f}"]]
    cw = [3.9, 1.65, 1.65]
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
    rows = [['Measure', 'A to B', 'A to C', 'B to C'], ['Euclidean\ndistance', '?', '?', '?'], ['Manhattan\ndistance', '?', '?', '?'], ['Dot product', '?', '?', '?'], ['Cosine\nsimilarity', '?', '?', '?']]
    cw = [1.75, 1.0, 1.0, 1.0]
    sc = (w - 0.1) / sum(cw)
    cw = [c * sc for c in cw]
    s.table(0.05, h - 0.95, cw, (h - 1.0) / 5.1, rows, size=14, align=['left', 'center', 'center', 'center'])
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
    cols = [('Euclidean distance', 'straight line', 'euclid', 'Smaller is closer.', 'Sees length and direction.'),
            ('Manhattan distance', 'city blocks', 'manhattan', 'Smaller is closer.', 'Adds up every difference.'),
            ('Dot product', 'sum of products', 'dot', 'Bigger is closer.', 'Rewards long arrows.'),
            ('Cosine similarity', 'angle', 'cosine', 'Bigger is closer.', 'Ignores length.')]
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


# ------------------------------------------------------------------ the bridge: picture, claim, text (all numbers)
@fig('x_t04_bridge')
def bridge(w, h, **_):
    s = Scene(w, h)
    cw_ = (w - 0.1 - 2 * 0.5) / 3
    cards = [('Session 1', 'A picture', '192 numbers', 'for an 8 by 8 colour picture', PAPER),
             ('Session 2', 'A house', '2 numbers', 'floor area, km to town; nearest = smallest distance', PAPER),
             ('Today', 'A text', 'many numbers', 'counts, weights, then an embedding; then measure distance', GOLD)]
    for i, (a, b, c, d, f) in enumerate(cards):
        x = 0.05 + i * (cw_ + 0.5)
        s.box(x, 0.3, cw_, h - 0.6, '', fill=f, edge=INK, lw=2, r=0.08)
        s.text(x + cw_ / 2, h - 0.8, a, size=16, color=MUTE, weight='bold')
        s.text(x + cw_ / 2, h - 1.4, b, size=22, weight='bold')
        s.text(x + cw_ / 2, h / 2 - 0.1, c, size=22, weight='bold', color=RED)
        ln = K.wrap(d, 15, 'regular', cw_ - 0.4)
        s.text(x + cw_ / 2, 1.2, '\n'.join(ln), size=15, color=BODY)
        if i < 2:
            s.arrow(x + cw_ + 0.05, h / 2, x + cw_ + 0.45, h / 2, lw=2.4)
    return s


# ------------------------------------------------------------------ the grid calculation of Session 2, again
@fig('x_t04_met')
def met(w, h, **_):
    s = Scene(w, h)
    P = _Plane(s, 0.7, 0.75, 0.43, 7, 9, labels=('', ''))
    a, b = P.to(3, 4), P.to(6, 8)
    s.line(a[0], a[1], b[0], a[1], color=MUTE, lw=2, dash=True, z=2)
    s.line(b[0], a[1], b[0], b[1], color=MUTE, lw=2, dash=True, z=2)
    s.arrow(a[0], a[1], b[0], b[1], color=RED, lw=3.4, head=16, z=6)
    P.dot(3, 4, INK)
    P.dot(6, 8, INK)
    s.text(a[0] - 0.15, a[1] - 0.25, 'N  (3, 4)', size=15, weight='bold', ha='right')
    s.text(b[0] - 0.15, b[1] + 0.2, 'P  (6, 8)', size=15, weight='bold', ha='right')
    s.text((a[0] + b[0]) / 2, a[1] - 0.22, '3 across', size=15, color=BODY)
    s.text(b[0] + 0.1, (a[1] + b[1]) / 2, '4 up', size=15, color=BODY, ha='left')
    x0 = 5.0
    cw = w - x0 - 0.1
    s.box(x0, 3.35, cw, 1.15, 'Session 2: houses N and P\n3 across, 4 up, so 5', size=16, fill=PAPER, lw=1.8)
    s.arrow(x0 + cw / 2, 3.3, x0 + cw / 2, 2.85, lw=2.2)
    s.box(x0, 1.45, cw, 1.35, 'Today: arrow tips a and b\nsame numbers, same 5', size=16, fill=GOLD, lw=2, weight='bold')
    s.text(x0 + cw / 2, 0.9, 'Only the list gets longer', size=15, color=BODY)
    return s


# ------------------------------------------------------------------ everyday: three friends rate two films (vectors)
@fig('x_t04_tastes')
def tastes(w, h, **_):
    s = Scene(w, h)
    P = _Plane(s, 0.95, 0.85, 0.42, 7, 9, labels=('Film 1 rating (comedy)', 'Film 2 rating (action)'), size=14)
    P.arrow(3, 4, color=INK)
    P.arrow(6, 8, color=GREY)
    P.arrow(4, 3, color=RED)
    s.text(P.to(3, 4)[0] - 0.12, P.to(3, 4)[1] + 0.2, 'Ana', size=16, weight='bold', ha='right')
    s.text(P.to(6, 8)[0] - 0.12, P.to(6, 8)[1] + 0.05, 'Ben', size=16, weight='bold', ha='right')
    s.text(P.to(4, 3)[0] + 0.12, P.to(4, 3)[1] - 0.2, 'Chloe', size=16, weight='bold', color=RED, ha='left')
    x0 = 4.55
    cw = [1.15, 1.0, 1.0]
    rows = [['Ratings\nout of 10', 'Film 1', 'Film 2'], ['Ana', '3', '4'], ['Ben', '6', '8'], ['Chloe', '4', '3']]
    s.table(x0, h - 0.55, cw, 0.62, rows, size=16, align=['left', 'center', 'center'], hl_cells={(1, 1): GOLD, (1, 2): GOLD})
    s.text(x0, 0.95, 'Ana is the vector (3, 4):\na list of two numbers,\none dimension per film.', size=15, color=BODY, ha='left')
    return s


# ------------------------------------------------------------------ the four measures, wide: plane on the left, formula and worked numbers on the right
_MEASURES = {
    'euclid': dict(name='Euclidean distance', sub='The straight-line distance. Smaller means closer.',
                   formula='d(a, b) = \u221a[ (a\u2081 \u2212 b\u2081)\u00b2 + (a\u2082 \u2212 b\u2082)\u00b2 ]',
                   sym=['a\u2081, a\u2082: Ana\'s ratings of Film 1 and Film 2. b\u2081, b\u2082: Ben\'s.', 'a\u2081 \u2212 b\u2081 is the gap on Film 1. Square each gap, add, take the root.', 'n films: d(a, b) = \u221a\u03a3 (a\u1d62 \u2212 b\u1d62)\u00b2. Industry name: L2 distance.'],
                   worked=['Ana (3, 4) and Ben (6, 8):', '\u221a[ (3 \u2212 6)\u00b2 + (4 \u2212 8)\u00b2 ] = \u221a(9 + 16) = \u221a25 = 5']),
    'manhattan': dict(name='Manhattan distance', sub='Also called city-block distance: add the gaps, as if walking a street grid. Smaller means closer.',
                      formula='d(a, b) = |a\u2081 \u2212 b\u2081| + |a\u2082 \u2212 b\u2082|',
                      sym=['| | means the size of the gap, ignoring its sign.', 'Same a\u2081, a\u2082, b\u2081, b\u2082 as before. No squares, no root.', 'n films: d(a, b) = \u03a3 |a\u1d62 \u2212 b\u1d62|. Industry name: L1 distance.'],
                      worked=['Ana (3, 4) and Ben (6, 8):', '|3 \u2212 6| + |4 \u2212 8| = 3 + 4 = 7']),
    'dot': dict(name='Dot product', sub='Multiply matching ratings, then add. Bigger means closer.',
                formula='a \u00b7 b = a\u2081b\u2081 + a\u2082b\u2082',
                sym=['a\u2081b\u2081 means a\u2081 \u00d7 b\u2081: the two Film 1 ratings multiplied.', 'Big ratings give big scores, so long arrows score high.', 'n films: a \u00b7 b = \u03a3 a\u1d62b\u1d62 (\u03a3: add up over every film i). Also the inner product.'],
                worked=['Ana with Ben: 3 \u00d7 6 + 4 \u00d7 8 = 18 + 32 = 50', 'Ana with Chloe: 3 \u00d7 4 + 4 \u00d7 3 = 12 + 12 = 24']),
    'cosine': dict(name='Cosine similarity', sub='The dot product divided by both lengths, so only the angle counts. 1 means the same direction.',
                   formula='cos(\u03b8) = (a \u00b7 b) \u00f7 (\u2016a\u2016 \u00d7 \u2016b\u2016)',
                   sym=['\u03b8 (theta) is the angle between the two arrows.', '\u2016a\u2016 is the length of a: \u221a(a\u2081\u00b2 + a\u2082\u00b2). Ana: \u221a(9 + 16) = 5. Ben 10. Chloe 5.', 'n films: \u2016a\u2016 = \u221a\u03a3 a\u1d62\u00b2. Cosine distance = 1 \u2212 cos(\u03b8).'],
                   worked=['Ana with Ben: 50 \u00f7 (5 \u00d7 10) = 1.00, same direction', 'Ana with Chloe: 24 \u00f7 (5 \u00d7 5) = 0.96, angle 16\u00b0'])}


def _measure_fig(w, h, kind):
    s = Scene(w, h)
    M = _MEASURES[kind]
    P = _Plane(s, 0.95, 0.7, 0.42, 7, 8, labels=('Film 1 rating', 'Film 2 rating'), size=14)
    a, b, c = P.to(3, 4), P.to(6, 8), P.to(4, 3)
    if kind == 'euclid':
        P.arrow(3, 4, color=INK)
        P.arrow(6, 8, color=GREY)
        s.line(a[0], a[1], b[0], a[1], color=MUTE, lw=2, dash=True, z=2)
        s.line(b[0], a[1], b[0], b[1], color=MUTE, lw=2, dash=True, z=2)
        s.arrow(a[0], a[1], b[0], b[1], color=RED, lw=3.4, head=16, z=6)
        s.text((a[0] + b[0]) / 2, a[1] - 0.2, 'gap 3', size=14, color=BODY)
        s.text(b[0] + 0.1, (a[1] + b[1]) / 2, 'gap 4', size=14, color=BODY, ha='left')
    elif kind == 'manhattan':
        pts = [(3, 4), (3, 5), (4, 5), (4, 6), (5, 6), (5, 7), (6, 7), (6, 8)]
        s.arrow(a[0], a[1], b[0], b[1], color=HAIR, lw=2.6, head=12, z=2)
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            p, q = P.to(x1, y1), P.to(x2, y2)
            s.line(p[0], p[1], q[0], q[1], color=RED, lw=4.2, z=5)
        P.dot(3, 4, INK)
        P.dot(6, 8, INK)
    elif kind == 'dot':
        P.arrow(3, 4, color=INK)
        P.arrow(6, 8, color=GREY)
        P.arrow(4, 3, color=RED)
    else:
        P.arrow(6, 8, color=GREY, lw=5, head=16)
        P.arrow(3, 4, color=INK)
        P.arrow(4, 3, color=RED)
        o = P.to(0, 0)
        s.ax.add_patch(Arc(o, 3.6, 3.6, theta1=36.87, theta2=53.13, color=RED, lw=3.4, zorder=6))
        s.text(o[0] + 2.2 * math.cos(math.radians(45)), o[1] + 2.2 * math.sin(math.radians(45)), '16\u00b0', size=15, weight='bold', color=RED)
    s.text(a[0] - 0.12, a[1] + 0.2 if kind != 'euclid' else a[1] + 0.25, 'Ana', size=15, weight='bold', ha='right')
    s.text(b[0] - 0.12, b[1] + 0.05, 'Ben', size=15, weight='bold', ha='right')
    if kind in ('dot', 'cosine'):
        s.text(c[0] + 0.12, c[1] - 0.18, 'Chloe', size=15, weight='bold', color=RED, ha='left')
    x0 = 4.7
    pw = w - x0 - 0.1
    s.text(x0, h - 0.3, M['name'], size=22, weight='bold', ha='left')
    sub = K.wrap(M['sub'], 15, 'regular', pw - 0.1)
    s.text(x0, h - 0.72 - 0.12 * (len(sub) - 1), '\n'.join(sub), size=15, color=RED, weight='bold', ha='left')
    yf = h - 1.5
    s.text(x0, yf, M['formula'], size=21, weight='bold', ha='left')
    for i, line in enumerate(M['sym']):
        s.text(x0, yf - 0.5 - i * 0.34, line, size=14, color=BODY, ha='left')
    by = 0.15
    s.box(x0, by, pw, 1.15, '', fill=GOLD, edge=INK, lw=2)
    two = kind in ('dot', 'cosine')
    s.text(x0 + 0.15, by + 0.82, M['worked'][0], size=17 if two else 15, weight='bold', ha='left')
    s.text(x0 + 0.15, by + 0.38, M['worked'][1], size=17 if two else 18, weight='bold', ha='left')
    return s


for _k in ('euclid', 'manhattan', 'dot', 'cosine'):
    fig('x_t04_m_' + _k)(lambda w, h, _k=_k, **_: _measure_fig(w, h, _k))
