"""Figure kinds for Session 4 (Words as numbers). Numbers come from demo_runs/s04/results.json (a real recorded run of demo_runs/s04/s04_run.py).

Kinds (use as dict(kind='t04_<name>')): list, arrow, recall, dot, dotread, length, angle, cosine, scale, compare4, bowhand, bowcos, df, log, tfidf_text, tfidf,
noshare, plane, network, numbers, search (skin='contracts'|'finance'|'hr'), agree, blank, cheat. Rebuilt 11 November 2026 (explain before use).
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
            s.box(x0 + j * cw, y + 0.2, cw - 0.05, 0.62, ('0.00' if abs(v) < 0.005 else f'{v:+.2f}'.replace('-', '−')), size=15, fill=GOLD if (cs and cs > 0.3) else PAPER, lw=1.3, r=0.04)
        s.text(x0 + 8 * cw + 0.2, y + 0.51, '...', size=20, weight='bold')
        s.text(w - 1.2, y + 0.51, '' if cs is None else f'{cs:.2f}', size=24, weight='bold')
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


# ================================================================== 11 November 2026: explain-before-use figures
# Toy vectors (invented, worked by hand): Ana (3, 4), Ben (6, 8), Chloe (4, 3), ratings out of 10.
ANA, BEN, CHLOE = (3, 4), (6, 8), (4, 3)
SUB = '₁₂'


def _col(s, x, y, lines, w):
    """Draw lines top-down from y. Each line: (text, size, weight, color, gap_after). Wraps to width w."""
    for t, size, wt, col, gap in lines:
        ln = K.wrap(t, size, 'bold' if wt == 'bold' else 'regular', w)
        s.text(x, y, '\n'.join(ln), size=size, weight=wt, color=col, ha='left', va='top')
        y -= len(ln) * size * 1.2 / 72 + gap
    return y


def _films(s, ox=0.75, oy=0.7, sc=0.38, xmax=7, ymax=9, arrows=True, who=('Ana', 'Ben', 'Chloe'), size=14):
    P = _Plane(s, ox, oy, sc, xmax, ymax, labels=('Film 1 rating', 'Film 2 rating'), size=size)
    pos = {'Ana': (ANA, INK), 'Ben': (BEN, GREY), 'Chloe': (CHLOE, RED)}
    for nm in sorted(who, key=lambda n: n != 'Ben'):
        (x, y), c = pos[nm]
        if arrows:
            P.arrow(x, y, color=c, lw=4.5 if nm == 'Ben' else 3.0)
        else:
            P.dot(x, y, c, r=0.08)
    off = {'Ana': (-0.12, 0.22, 'right'), 'Ben': (-0.12, 0.1, 'right'), 'Chloe': (0.14, -0.2, 'left')}
    for nm in who:
        (x, y), c = pos[nm]
        dx, dy, ha = off[nm]
        tx, ty = P.to(x, y)
        s.text(tx + dx, ty + dy, nm, size=15, weight='bold', color=RED if nm == 'Chloe' else INK, ha=ha)
    return P


# ------------------------------------------------------------------ a vector is a list of numbers in a fixed order
@fig('x_t04_list')
def vlist(w, h, **_):
    s = Scene(w, h)
    x0, cw, ch = 1.45, 1.25, 0.85
    s.text(x0 + cw / 2, 4.5, 'Film 1', size=16, weight='bold', color=MUTE)
    s.text(x0 + cw * 1.5, 4.5, 'Film 2', size=16, weight='bold', color=MUTE)
    for k, (nm, v, hl) in enumerate((('Ana', ANA, True), ('Chloe', CHLOE, False))):
        y = 3.3 - k * 1.2
        s.text(0.1, y + ch / 2, nm, size=20, weight='bold', ha='left', color=RED if k else INK)
        s.cells(x0, y, list(v), w=cw, h=ch, size=28, hl=(0, 1) if hl else ())
        s.text(x0 + 2 * cw + 0.3, y + ch / 2, f'=  ({v[0]}, {v[1]})', size=26, weight='bold', ha='left')
    s.text(x0 + 2 * cw + 0.3, 1.65, 'same numbers, other order:\na different vector', size=15, color=RED, ha='left', va='top')
    _col(s, 0.1, 1.05, [('Position 1 is always Film 1, position 2 always Film 2.', 16, 'normal', BODY, 0.12),
                        ('Each position is a dimension: 2 numbers, 2 dimensions.', 16, 'bold', INK, 0)], w - 0.2)
    return s


# ------------------------------------------------------------------ a vector drawn as an arrow from 0
@fig('x_t04_arrow')
def varrow(w, h, **_):
    s = Scene(w, h)
    P = _films(s, ox=0.75, oy=0.75, sc=0.4, xmax=7, ymax=9)
    a0, a1, a2 = P.to(0, 0), P.to(3, 0), P.to(3, 4)
    s.line(a0[0], a0[1] + 0.03, a1[0], a1[1] + 0.03, color=GOLD, lw=5, z=3)
    s.line(a1[0], a1[1], a2[0], a2[1], color=GOLD, lw=5, z=3)
    s.text(a1[0] + 0.12, a1[1] + 0.25, '3 across, then 4 up', size=14, color=BODY, ha='left')
    x0 = 4.3
    _col(s, x0, h - 0.1, [('Ana (3, 4): go 3 across, then 4 up. Draw the arrow from 0 to that point.', 15, 'normal', INK, 0.25),
                          ('Direction = the mix', 17, 'bold', INK, 0.05),
                          ('Ben (6, 8) is Ana\'s numbers times 2: the same direction.', 15, 'normal', BODY, 0.25),
                          ('Length = how strong', 17, 'bold', INK, 0.05),
                          ('Ben\'s arrow is twice as long as Ana\'s.', 15, 'normal', BODY, 0.25),
                          ('Chloe (4, 3) leans the other way.', 15, 'normal', RED, 0)], w - x0 - 0.1)
    return s


# ------------------------------------------------------------------ Session 2's two distances on the film vectors
@fig('x_t04_recall')
def recall2(w, h, **_):
    s = Scene(w, h)
    P = _films(s, arrows=False)
    a, b, c = P.to(*ANA), P.to(*BEN), P.to(*CHLOE)
    for q in (b, c):
        s.line(a[0], a[1], q[0], a[1], color=GOLD, lw=3.2, z=2)
        s.line(q[0], a[1], q[0], q[1], color=GOLD, lw=3.2, z=2)
        s.line(a[0], a[1], q[0], q[1], color=RED, lw=3.2, z=3)
    x0 = 3.95
    rows = [['', 'Ana (3, 4) to Ben (6, 8)', 'Ana (3, 4) to Chloe (4, 3)'],
            ['Gap on each film', '3 and 4', '1 and 1'],
            ['Euclidean (red line):\n√(gap₁² + gap₂²)', '√(9 + 16) = √25 = 5', '√(1 + 1) = √2 = 1.41'],
            ['Manhattan (gold path):\ngap₁ + gap₂', '3 + 4 = 7', '1 + 1 = 2']]
    cw = [3.05, 2.4, 2.45]
    s.table(x0, h - 0.05, cw, 0.8, rows, size=15, align=['left', 'center', 'center'], hl_cells={(2, 2): GOLD, (3, 2): GOLD})
    _col(s, x0, h - 3.35, [('gap₁ is the gap on Film 1, counted as a positive number. Both distances: smaller is closer, so Chloe is closer to Ana.', 15, 'normal', BODY, 0)], sum(cw))
    return s


# ------------------------------------------------------------------ dot product: worked first, then the formula
@fig('x_t04_dot')
def dotw(w, h, **_):
    s = Scene(w, h)
    _films(s)
    x0 = 3.95
    pw = w - x0 - 0.1
    s.text(x0, h - 0.25, 'Step 1: multiply the matching ratings.  Step 2: add.', size=17, weight='bold', ha='left')
    s.box(x0, 2.45, pw, 1.15, '', fill=PAPER, edge=INK, lw=2)
    s.text(x0 + 0.15, 3.25, 'Ana with Ben:', size=17, weight='bold', ha='left')
    s.text(x0 + 2.25, 3.25, '3 × 6 = 18,   4 × 8 = 32,   18 + 32 = 50', size=17, weight='bold', ha='left')
    s.text(x0 + 0.15, 2.8, 'Ana with Chloe:', size=17, weight='bold', ha='left')
    s.text(x0 + 2.25, 2.8, '3 × 4 = 12,   4 × 3 = 12,   12 + 12 = 24', size=17, weight='bold', ha='left')
    s.text(x0, 2.05, 'The formula:   a · b = a₁b₁ + a₂b₂', size=21, weight='bold', ha='left')
    _col(s, x0, 1.65, [('a = (a₁, a₂) is Ana, b = (b₁, b₂) is Ben. a₁b₁ means a₁ × b₁.', 14, 'normal', BODY, 0.06),
                       ('Longer lists: a · b = Σ aᵢbᵢ. Σ means add up, one term for each position i.', 14, 'normal', BODY, 0.06),
                       ('Session 1\'s weighted sum (inputs times weights, added) is a dot product.', 14, 'normal', BODY, 0)], pw)
    return s


# ------------------------------------------------------------------ how to read a dot product: three cases
@fig('x_t04_dotread')
def dotread(w, h, **_):
    s = Scene(w, h)
    pw = (w - 0.2) / 3
    cases = [('Same mix', [(BEN, GREY), (ANA, INK)], ['Ana with Ben', '3 × 6 + 4 × 8'], '= 50, big'),
             ('Nothing shared', [((5, 0), INK), ((0, 5), RED)], ['(5, 0) with (0, 5)', '5 × 0 + 0 × 5'], '= 0'),
             ('Long arrows win', [(BEN, GREY), (ANA, INK)], ['Ana with Ana: 25', 'Ana with Ben: 50'], 'Ben beats Ana')]
    for i, (head, arrows, calc, res) in enumerate(cases):
        x = 0.05 + i * (pw + 0.05)
        s.box(x, 0.05, pw, h - 0.1, '', fill=PAPER, edge=HAIR, lw=1.4)
        s.text(x + pw / 2, h - 0.35, head, size=18, weight='bold')
        P = _Plane(s, x + 0.45, 1.85, 0.2, 9, 9, ticks=False)
        for (vx, vy), c in arrows:
            P.arrow(vx, vy, color=c, lw=4.5 if c == GREY else 2.8, head=14)
        s.text(x + pw / 2, 1.42, calc[0], size=15)
        s.text(x + pw / 2, 1.02, calc[1], size=15)
        s.text(x + pw / 2, 0.5, res, size=19, weight='bold', color=RED if i == 2 else INK)
    return s


# ------------------------------------------------------------------ length of an arrow (Pythagoras)
@fig('x_t04_length')
def length(w, h, **_):
    s = Scene(w, h)
    P = _Plane(s, 0.75, 0.7, 0.38, 7, 9, labels=('Film 1 rating', 'Film 2 rating'))
    o, r, t = P.to(0, 0), P.to(3, 0), P.to(3, 4)
    s.poly([o, r, t], fill=PALE, edge=PALE, lw=0.5, z=1)
    s.line(o[0], o[1] + 0.02, r[0], r[1] + 0.02, color=GOLD, lw=5, z=3)
    s.line(r[0], r[1], t[0], t[1], color=GOLD, lw=5, z=3)
    P.arrow(3, 4, color=INK, lw=3.4)
    s.text((o[0] + r[0]) / 2, o[1] + 0.22, '3', size=16, weight='bold')
    s.text(r[0] + 0.15, (r[1] + t[1]) / 2, '4', size=16, weight='bold', ha='left')
    s.text((o[0] + t[0]) / 2 - 0.2, (o[1] + t[1]) / 2 + 0.2, '5', size=18, weight='bold', color=RED, ha='right')
    s.text(t[0] - 0.12, t[1] + 0.22, 'Ana', size=15, weight='bold', ha='right')
    x0 = 3.95
    pw = w - x0 - 0.1
    s.text(x0, h - 0.25, 'Square each number, add, then take the square root.', size=17, weight='bold', ha='left')
    s.box(x0, 2.05, pw, 1.6, '', fill=PAPER, edge=INK, lw=2)
    for k, (nm, line) in enumerate((('Ana (3, 4):', '3² + 4² = 9 + 16 = 25,    √25 = 5'), ('Ben (6, 8):', '6² + 8² = 36 + 64 = 100,    √100 = 10'),
                                    ('Chloe (4, 3):', '4² + 3² = 16 + 9 = 25,    √25 = 5'))):
        s.text(x0 + 0.15, 3.3 - k * 0.45, nm, size=17, weight='bold', ha='left')
        s.text(x0 + 1.85, 3.3 - k * 0.45, line, size=17, weight='bold', ha='left')
    s.text(x0, 1.65, 'The formula:   ‖a‖ = √(a₁² + a₂²)', size=21, weight='bold', ha='left')
    _col(s, x0, 1.25, [('‖a‖ is read "the length of a". a₁² (a₁ squared) means a₁ × a₁.', 14, 'normal', BODY, 0.06),
                       ('√ is the square root: √25 = 5 because 5 × 5 = 25.', 14, 'normal', BODY, 0.06),
                       ('It is the Euclidean distance from 0 to the tip. Longer lists: ‖a‖ = √Σ aᵢ².', 14, 'normal', BODY, 0)], pw)
    return s


# ------------------------------------------------------------------ what an angle and its cosine mean
@fig('x_t04_angle')
def angle(w, h, **_):
    s = Scene(w, h)
    pw = (w - 0.3) / 4
    cases = [('0°', 53.13, 53.13, 'Same direction', 'cos = 1'), ('16°', 53.13, 36.87, 'Ana and Chloe', 'cos = 0.96'),
             ('90°', 90, 0, 'Right angle:\nnothing shared', 'cos = 0'), ('180°', 180, 0, 'Opposite\ndirections', 'cos = −1')]
    for i, (head, t1, t2, cap, cs) in enumerate(cases):
        x = 0.05 + i * (pw + 0.066)
        s.box(x, 0.05, pw, h - 0.1, '', fill=PAPER, edge=HAIR, lw=1.4)
        s.text(x + pw / 2, h - 0.35, head, size=22, weight='bold')
        ox = x + pw / 2 if t1 == 180 else (x + 0.75 if t1 == 90 else x + 0.7)
        oy = 1.75
        L = 1.45
        for t, c, lw, f in ((t1, GREY if i == 0 else INK, 5.5 if i == 0 else 3, 1.0), (t2, RED if i else INK, 3, 0.55 if i == 0 else 1.0)):
            s.arrow(ox, oy, ox + f * L * math.cos(math.radians(t)), oy + f * L * math.sin(math.radians(t)), color=c, lw=lw, head=15)
        if t1 != t2:
            s.ax.add_patch(Arc((ox, oy), 1.1, 1.1, theta1=min(t1, t2), theta2=max(t1, t2), color=RED, lw=3, zorder=6))
        s.circle(ox, oy, 0.05, fill=INK, edge=INK)
        s.text(x + pw / 2, 0.95, cap, size=15, color=BODY)
        s.text(x + pw / 2, 0.35, cs, size=20, weight='bold', color=RED)
    return s


# ------------------------------------------------------------------ cosine similarity: worked first, then the formula
@fig('x_t04_cosine')
def cosw(w, h, **_):
    s = Scene(w, h)
    P = _films(s)
    o = P.to(0, 0)
    s.ax.add_patch(Arc(o, 2.6, 2.6, theta1=36.87, theta2=53.13, color=RED, lw=3.4, zorder=6))
    s.text(o[0] + 1.6 * math.cos(math.radians(45)), o[1] + 1.6 * math.sin(math.radians(45)), '16°', size=15, weight='bold', color=RED)
    x0 = 3.95
    pw = w - x0 - 0.1
    s.text(x0, h - 0.25, 'Divide the dot product by the two lengths multiplied.', size=17, weight='bold', ha='left')
    s.box(x0, 2.45, pw, 1.15, '', fill=PAPER, edge=INK, lw=2)
    s.text(x0 + 0.15, 3.25, 'Ana with Ben:', size=17, weight='bold', ha='left')
    s.text(x0 + 2.25, 3.25, '50 ÷ (5 × 10) = 50 ÷ 50 = 1.00', size=17, weight='bold', ha='left')
    s.text(x0 + 0.15, 2.8, 'Ana with Chloe:', size=17, weight='bold', ha='left')
    s.text(x0 + 2.25, 2.8, '24 ÷ (5 × 5) = 24 ÷ 25 = 0.96, so 16°', size=17, weight='bold', ha='left')
    s.text(x0, 2.05, 'The formula:   cos(θ) = (a · b) ÷ (‖a‖ × ‖b‖)', size=21, weight='bold', ha='left')
    _col(s, x0, 1.65, [('θ (theta) is the angle between the arrows. a · b is the dot product, ‖a‖ and ‖b‖ the lengths.', 14, 'normal', BODY, 0.06),
                       ('Bigger is closer: 1 same direction, 0 right angle, −1 opposite.', 14, 'normal', BODY, 0.06),
                       ('Some tools report cosine distance, which is 1 − cos(θ): smaller is closer.', 14, 'normal', BODY, 0)], pw)
    return s


# ------------------------------------------------------------------ cosine ignores length
@fig('x_t04_scale')
def scale(w, h, **_):
    s = Scene(w, h)
    P = _films(s, ox=0.7, oy=0.7, sc=0.36, xmax=7, ymax=9, who=('Ana', 'Ben'))
    x0 = 3.55
    rows = [['', 'Ana with Ana', 'Ana with Ben'], ['Dot product', '25', '50'], ['Lengths', '5 × 5 = 25', '5 × 10 = 50'], ['Cosine', '25 ÷ 25 = 1', '50 ÷ 50 = 1']]
    cw = [1.3, 1.4, 1.4]
    s.table(x0, h - 0.1, cw, 0.68, rows, size=15, align=['left', 'center', 'center'], hl_cells={(3, 1): GOLD, (3, 2): GOLD})
    _col(s, x0, h - 3.0, [('Ben doubles every rating. The dot product doubles, the lengths double, and the two cancel.', 15, 'normal', BODY, 0)], sum(cw))
    return s


# ------------------------------------------------------------------ the four measures compared, with the working
@fig('x_t04_compare4')
def compare4(w, h, **_):
    s = Scene(w, h)
    rows = [['Measure', 'Ana to Ben', 'Ana to Chloe', 'Closer is', 'Picks'],
            ['Euclidean distance', '√(3² + 4²) = 5', '√(1² + 1²) = 1.41', 'smaller', 'Chloe'],
            ['Manhattan distance', '3 + 4 = 7', '1 + 1 = 2', 'smaller', 'Chloe'],
            ['Dot product', '18 + 32 = 50', '12 + 12 = 24', 'bigger', 'Ben'],
            ['Cosine similarity', '50 ÷ (5 × 10) = 1.00', '24 ÷ (5 × 5) = 0.96', 'bigger', 'Ben']]
    cw = [2.75, 3.0, 3.0, 1.45, 1.55]
    s.table(0.05, h - 0.05, cw, 0.62, rows, size=17, align=['left', 'center', 'center', 'center', 'center'],
            hl_cells={(r, 4): GOLD for r in range(1, 5)})
    s.text(0.1, 0.75, 'Distances see both length and direction. The dot product rewards long arrows.', size=15, color=BODY, ha='left')
    s.text(0.1, 0.35, 'Cosine similarity sees direction only.', size=15, color=BODY, ha='left')
    return s


# ------------------------------------------------------------------ bag of words built on three tiny messages
TINY = [('S1', 'send the invoice'), ('S2', 'the invoice is late'), ('S3', 'the rice is late')]
VOCAB = ['send', 'the', 'invoice', 'is', 'late', 'rice']


def _counts(t):
    ws = t.split()
    return [ws.count(v) for v in VOCAB]


@fig('x_t04_bowhand')
def bowhand(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.25, 'Three tiny messages', size=17, weight='bold', ha='left')
    for k, (i, t) in enumerate(TINY):
        s.text(0.1, h - 0.85 - k * 0.55, i, size=17, weight='bold', ha='left')
        s.text(0.65, h - 0.85 - k * 0.55, f'"{t}"', size=17, ha='left')
    s.arrow(3.35, 2.75, 3.95, 2.75, lw=2.4)
    x0 = 4.15
    s.text(x0, h - 0.25, 'Step 1: list every word once.  Step 2: count it in each message.', size=17, weight='bold', ha='left')
    rows = [[''] + VOCAB] + [[i] + [str(c) for c in _counts(t)] for i, t in TINY]
    cw = [0.75] + [1.12] * 6
    hl = {(r + 1, c + 1): GOLD for r, (_, t) in enumerate(TINY) for c, v in enumerate(_counts(t)) if v}
    s.table(x0, h - 0.6, cw, 0.5, rows, size=17, hl_cells=hl)
    _col(s, 0.1, 1.35, [('6 words in the list, so each message is a vector of 6 numbers: S2 = (0, 1, 1, 1, 1, 0). This list of words is the vocabulary.', 15, 'normal', INK, 0.08),
                        ('The order of the words is lost: "dog bites man" and "man bites dog" get the same counts.', 15, 'normal', BODY, 0)], w - 0.2)
    return s


@fig('x_t04_bowcos')
def bowcos(w, h, **_):
    s = Scene(w, h)
    import numpy as np_
    V = {i: np_.array(_counts(t)) for i, t in TINY}
    pw = (w - 0.15) / 2
    for k, (other, shared) in enumerate((('S1', 'the, invoice'), ('S3', 'the, is, late'))):
        a, b = V['S2'], V[other]
        dt = int(a @ b)
        la, lb = float(np_.linalg.norm(a)), float(np_.linalg.norm(b))
        cs = dt / (la * lb)
        x = 0.05 + k * (pw + 0.05)
        s.box(x, 0.95, pw, h - 1.0, '', fill=GOLD if k else PAPER, edge=INK, lw=1.8)
        s.text(x + pw / 2, h - 0.35, f'S2 with {other}', size=19, weight='bold')
        s.text(x + pw / 2, h - 0.8, f'"{TINY[1][1]}"', size=14, color=BODY)
        s.text(x + pw / 2, h - 1.15, f'"{dict(TINY)[other]}"', size=14, color=BODY)
        lb_s = '√3 = 1.73' if other == 'S1' else '√4 = 2'
        lines = [f'Shared: {shared}', f'Dot product: {dt}', f'Lengths: 2 and {lb_s}', f'Cosine: {dt} ÷ (2 × {lb:.2f}) = {cs:.2f}' if other == 'S1' else f'Cosine: {dt} ÷ (2 × 2) = {cs:.2f}']
        assert abs(la - 2) < 1e-9
        for j, ln in enumerate(lines):
            s.text(x + 0.15, h - 1.7 - j * 0.5, ln, size=15 if j < 3 else 16, weight='bold' if j == 3 else 'normal', ha='left')
    s.text(w / 2, 0.55, 'Two of the three shared words, the and is, say nothing about the topic.', size=15, color=RED, weight='bold')
    s.text(w / 2, 0.18, 'Lengths: √ of the sum of the squared counts, as for Ana.', size=14, color=BODY)
    return s


# ------------------------------------------------------------------ tf and df on message M06 and the 40 messages
_M06 = {m['word']: m for m in _R['m06_words']}
SIX = ['the', 'please', 'send', 'oil', 'invoice', 'jerrycan']


@fig('x_t04_df')
def dfig(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.22, 'Six words from message M06, out of 40 messages', size=17, weight='bold', ha='left')
    x0, xmax = 1.45, 5.35
    sc = (xmax - x0) / 40
    s.text(x0, h - 0.68, 'df: messages that contain the word', size=14, color=MUTE, ha='left')
    s.text(w - 0.55, h - 0.68, 'tf in M06', size=14, color=MUTE)
    for k, wd in enumerate(SIX):
        m = _M06[wd]
        y = h - 1.25 - k * 0.5
        s.text(0.1, y, wd, size=16, weight='bold', ha='left')
        s.rect(x0, y - 0.16, 40 * sc, 0.32, fill=PALE, edge=HAIR, lw=0.8, z=1)
        s.rect(x0, y - 0.16, m['in_messages'] * sc, 0.32, fill=RED if m['in_messages'] <= 4 else GREY, edge=INK, lw=1, z=2)
        s.text(x0 + m['in_messages'] * sc + 0.1, y, f"{m['in_messages']} of 40", size=14, weight='bold', ha='left')
        s.text(w - 0.55, y, str(m['count']), size=16, weight='bold')
    s.text(0.1, 0.55, 'Common word, big df: a weak clue to what M06 is about.', size=15, color=BODY, ha='left')
    s.text(0.1, 0.18, 'Rare word, small df: a strong clue.', size=15, color=RED, weight='bold', ha='left')
    return s


# ------------------------------------------------------------------ inverse document frequency and the log
def _ln2(x):
    return f'{math.log(x):.2f}'


@fig('x_t04_log')
def logfig(w, h, **_):
    s = Scene(w, h)
    rows = [['Word', 'df', 'N ÷ df', 'ln(N ÷ df)']]
    for wd in SIX[::-1]:
        d = _M06[wd]['in_messages']
        r = 40 / d
        rows.append([wd, str(d), f'40 ÷ {d} = {r:.1f}'.replace('.0 ', ' ') if r != int(r) else f'40 ÷ {d} = {int(r)}', _ln2(r)])
    cw = [1.5, 0.75, 2.2, 1.75]
    s.table(0.05, h - 0.05, cw, 0.58, rows, size=16, align=['left', 'center', 'center', 'center'], hl_cells={(1, 3): GOLD})
    x0 = 6.6
    _col(s, x0, h - 0.1, [('N = 40 messages. N ÷ df runs from 1.8 to 40, so one rare word would outweigh the rest.', 15, 'normal', INK, 0.18),
                          ('The log grows slowly: 40 becomes 3.69 and 1.8 becomes 0.60. The order stays the same.', 15, 'normal', INK, 0.18),
                          ('ln x: how many times you multiply by e (about 2.718) to reach x.', 15, 'bold', INK, 0.1),
                          ('ln 1 = 0,  ln 2.718 = 1,  ln 10 = 2.30,  ln 100 = 4.61', 15, 'bold', RED, 0.18),
                          ('A word in every message: ln(40 ÷ 40) = ln 1 = 0.', 15, 'normal', BODY, 0)], w - x0 - 0.1)
    return s


# ------------------------------------------------------------------ TF-IDF worked on M06, textbook form
@fig('x_t04_tfidf_text')
def tfidf_text(w, h, **_):
    s = Scene(w, h)
    rows = [['Word in M06', 'tf', 'df', 'idf = ln(40 ÷ df)', 'tf × idf']]
    for wd in SIX[::-1]:
        m = _M06[wd]
        idf = round(math.log(40 / m['in_messages']), 2)
        rows.append([wd, str(m['count']), str(m['in_messages']), f'{idf:.2f}', f"{m['count']} × {idf:.2f} = {m['count'] * idf:.2f}"])
    cw = [1.75, 0.7, 0.7, 2.2, 2.35]
    s.table(0.05, h - 0.05, cw, 0.45, rows, size=16, align=['left', 'center', 'center', 'center', 'center'], hl_cells={(2, 4): GOLD, (1, 4): PALE})
    x0 = 8.15
    _col(s, x0, h - 0.1, [('invoice wins: it is repeated (tf 2) and rare (df 4).', 16, 'bold', INK, 0.15),
                          ('jerrycan is rarer but appears once. the is everywhere, so it weighs least.', 15, 'normal', BODY, 0)], w - x0 - 0.1)
    s.text(0.1, 0.62, 'The formula:   TF-IDF(t, d) = tf(t, d) × ln(N ÷ df(t))', size=20, weight='bold', ha='left')
    s.text(0.1, 0.2, 't: a word (term). d: a message (document). tf: count of t in d. df: messages containing t. N = 40. Numbers rounded to 2 decimals.', size=14, color=BODY, ha='left')
    return s


# ------------------------------------------------------------------ TF-IDF as recorded: scikit-learn smoothed form, then length 1
@fig('x_t04_tfidf')
def tfidf(w, h, **_):
    """The recorded run used scikit-learn TfidfVectorizer defaults: idf = ln((1 + N) / (1 + df)) + 1, weight = tf x idf, then each message vector divided by its length."""
    s = Scene(w, h)
    N = 40
    idf = lambda df: math.log((1 + N) / (1 + df)) + 1
    length = math.sqrt(sum((m['count'] * idf(m['in_messages'])) ** 2 for m in _R['m06_words']))
    rows = [['Word in M06', 'tf', 'df', 'idf = ln(41 ÷ (1 + df)) + 1', 'tf × idf', f'÷ {length:.2f}, recorded']]
    for wd in SIX[::-1]:
        m = _M06[wd]
        i3 = round(idf(m['in_messages']), 3)
        p3 = round(m['count'] * i3, 3)
        v = p3 / round(length, 2)
        assert f'{v:.3f}' == f"{m['real']:.3f}", (wd, v, m['real'])
        rows.append([wd, str(m['count']), str(m['in_messages']), f'{i3:.3f}', f"{m['count']} × {i3:.3f} = {p3:.3f}", f"{m['real']:.3f}"])
    cw = [1.75, 0.65, 0.65, 3.2, 2.65, 2.0]
    s.table(0.05, h - 0.05, cw, 0.42, rows, size=15, align=['left', 'center', 'center', 'center', 'center', 'center'], hl_cells={(2, 5): GOLD})
    _col(s, 0.1, 1.1, [('The +1s act as if one extra message held every word: no division by 0, and a word in every message keeps a little weight.', 14, 'normal', BODY, 0.05),
                       (f'{length:.2f} is the length of M06\'s vector of 27 weights, √(sum of the squares), as for Ana\'s arrow. Dividing by it makes the length 1.', 14, 'normal', BODY, 0)], w - 0.2)
    return s


# ------------------------------------------------------------------ counts see no link between a question and its clause
@fig('x_t04_noshare')
def noshare(w, h, **_):
    s = Scene(w, h)
    S = _R['skins']['contracts']
    q = S['queries'][0]
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location('s04_corpus', Path(__file__).resolve().parent.parent / 'demo_runs' / 's04' / 's04_corpus.py')
    _m = _iu.module_from_spec(_sp)
    _sp.loader.exec_module(_m)
    _SK = _m.SKINS
    k1 = [t for i, _, t in _SK['contracts']['passages'] if i == 'K1'][0]
    for k, (head, txt, edge) in enumerate((('Plain question', q['query'], INK), ('Clause: Force majeure', k1, RED))):
        y = h - 0.1 - (k + 1) * 1.65
        s.box(0.05, y, w - 0.1, 1.5, '', fill=PAPER, edge=edge, lw=1.8)
        s.text(0.2, y + 1.22, head, size=17, weight='bold', ha='left', color=edge)
        s.text(0.2, y + 0.92, '\n'.join(K.wrap(txt, 15, 'regular', w - 0.5)), size=15, ha='left', va='top')
    s.text(0.1, 1.05, 'Words in common: none. Dot product of the counts: 0, so cosine 0.', size=16, weight='bold', ha='left')
    s.text(0.1, 0.6, 'Yet both are about a flood that stops a delivery.', size=16, color=RED, weight='bold', ha='left')
    s.text(0.1, 0.2, 'Recorded run: the keyword search found no shared word for this question.', size=14, color=BODY, ha='left')
    return s


# ------------------------------------------------------------------ an embedding toy: words as arrows in a plane, with cosine
@fig('x_t04_plane')
def plane(w, h, **_):
    s = Scene(w, h)
    P = _Plane(s, 1.0, 0.95, 0.56, 7, 6, labels=('dimension 1: about money', 'dimension 2: trucks'))
    for x, y, c in ((4, 1, INK), (3, 1.5, INK), (1, 4, RED)):
        P.arrow(x, y, color=c)
    s.text(P.to(4, 1)[0] + 0.15, P.to(4, 1)[1] - 0.3, 'invoice (4, 1)', size=15, weight='bold', ha='left')
    s.text(P.to(3, 1.5)[0] - 0.05, P.to(3, 1.5)[1] + 0.38, 'receipt (3, 1.5)', size=15, weight='bold', ha='center')
    s.text(P.to(1, 4)[0] + 0.15, P.to(1, 4)[1] + 0.1, 'lorry (1, 4)', size=15, weight='bold', color=RED, ha='left')
    x0 = 5.1
    s.box(x0, 2.75, w - x0 - 0.05, 1.75, '', fill=GOLD, lw=1.8)
    s.text(x0 + (w - x0) / 2, 4.15, 'invoice, receipt', size=16, weight='bold')
    s.text(x0 + (w - x0) / 2, 3.6, '13.5 ÷ (4.12 × 3.35)', size=15)
    s.text(x0 + (w - x0) / 2, 3.1, 'cosine 0.98', size=19, weight='bold')
    s.box(x0, 0.75, w - x0 - 0.05, 1.75, '', fill=PAPER, lw=1.8, edge=RED)
    s.text(x0 + (w - x0) / 2, 2.15, 'invoice, lorry', size=16, weight='bold', color=RED)
    s.text(x0 + (w - x0) / 2, 1.6, '8 ÷ (4.12 × 4.12)', size=15)
    s.text(x0 + (w - x0) / 2, 1.1, 'cosine 0.47', size=19, weight='bold')
    return s


# ------------------------------------------------------------------ a network produces the vector (simplified)
@fig('x_t04_network')
def network(w, h, **_):
    s = Scene(w, h)
    V = _R['sample_vectors']['first8']['query']
    cy = h / 2 + 0.25
    s.box(0.1, cy - 0.85, 2.7, 1.7, 'What happens if\nheavy rain floods\nthe road...', size=16, fill=PAPER, lw=2)
    s.text(1.45, cy + 1.2, 'Text goes in', size=17, weight='bold')
    cols = [4.0, 5.2, 6.4]
    ys = [cy + 0.9 - k * 0.45 for k in range(5)]
    for a in range(2):
        for ya in ys:
            for yb in ys:
                s.line(cols[a], ya, cols[a + 1], yb, color=HAIR, lw=0.9, z=1)
    for c in cols:
        for yy in ys:
            s.circle(c, yy, 0.14, fill=PAPER, edge=INK, lw=1.6, z=4)
    s.arrow(2.85, cy, 3.75, cy, lw=2.4)
    s.arrow(6.6, cy, 7.5, cy, lw=2.4)
    s.text(5.2, cy + 1.45, 'A network like Session 1\'s', size=17, weight='bold')
    s.text(5.2, cy - 1.3, 'drawn small: the real one is much bigger', size=14, color=MUTE)
    s.text(9.5, cy + 1.45, '384 numbers out', size=17, weight='bold')
    for j, v in enumerate(V[:6]):
        s.box(8.55, cy + 0.95 - j * 0.38, 1.9, 0.34, ('0.00' if abs(v) < 0.005 else f'{v:+.2f}'.replace('-', '−')), size=14, fill=PAPER, lw=1.3, r=0.04)
    s.text(9.5, cy - 1.3, '... and 378 more', size=14, color=MUTE)
    s.box(0.1, 0.02, w - 0.2, 0.42, 'Fine-tuned on more than a billion pairs of related sentences, so that similar meanings land close (model card).', size=14, fill=PALE, lw=1.2)
    return s
