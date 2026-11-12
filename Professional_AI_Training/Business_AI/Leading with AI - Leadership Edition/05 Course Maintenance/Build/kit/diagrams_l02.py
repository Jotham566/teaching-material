"""Figures for Leadership Edition Session 2, AI that predicts from your data.  Names: x_l02_*  (content kind 'l02_*').

No maths anywhere: pictures, counts and percentages only.  Numbers from the demonstration are read from the recorded run in
demo_runs/s02/ (results_s02.json; scikit-learn 1.9.1, 5 and 11 November 2026).  The expense claims are FICTIONAL.
Case figures come from research/*.md (IDs in the content file).  Loan, borrower and shop figures marked 'illustrative' are invented
to teach the idea and are labelled so on the slide.
"""
import json
from pathlib import Path

from matplotlib.patches import Ellipse

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD, fig
import slidekit as K

RUN = Path(__file__).resolve().parent.parent / 'demo_runs' / 's02'
_C = {}


def _res():
    if not _C:
        _C.update(json.load(open(RUN / 'results_s02.json')))
    return _C


def _kind(weight, italic=False):
    return 'italic' if italic else ('bold' if weight == 'bold' else 'regular')


def _lh(size):
    return size * 1.15 / 72.0


def _wrap(s, x, y, w, text, size, weight='normal', color=INK, ha='center', va='center', italic=False):
    """Wrapped text in a column of width w; returns its height in inches."""
    lines = K.wrap(text, size, _kind(weight, italic), w)
    s.text(x, y, '\n'.join(lines), size=size, weight=weight, color=color, ha=ha, va=va, italic=italic, parse_math=False)
    return len(lines) * _lh(size)


def _fit(text, w, hmax, smax=17, smin=14, weight='normal'):
    """Largest size in [smin, smax] at which text wrapped to width w fits height hmax."""
    for sz in range(smax, smin - 1, -1):
        if len(K.wrap(text, sz, _kind(weight), w)) * _lh(sz) <= hmax:
            return sz
    return smin


def _source(s, text, y=0.2, x=0.1):
    s.text(x, y, text, size=14, color=MUTE, ha='left')


# ------------------------------------------------------------------ recall bridge: Session 1 pictures, today records
@fig('x_l02_bridge')
def x_l02_bridge(w, h, **_):
    s = Scene(w, h)
    panels = [
        (0.1, 'Session 1: labelled pictures', 'plant', [('Leaf photo, brown spots', 'diseased'), ('Leaf photo, even green', 'healthy'), ('Leaf photo, yellow edges', 'diseased')],
         'Learns what a diseased leaf looks like'),
        (3.95, 'Today: labelled records', 'doc', [('5 years a client, always on time', 'repaid'), ('New client, 3 late payments', 'not repaid'), ('2 years a client, 1 late payment', 'repaid')],
         'Learns who is likely to repay'),
    ]
    pw = 3.65
    for x0, head, ic, rows, out in panels:
        s.text(x0 + 0.05, h - 0.3, head, size=18, weight='bold', ha='left')
        s.line(x0, h - 0.55, x0 + pw, h - 0.55, lw=1.6)
        for i, (txt, lab) in enumerate(rows):
            y = h - 1.05 - i * 0.68
            s.icon(ic, x0 + 0.28, y, 0.5)
            _wrap(s, x0 + 0.62, y, 1.65, txt, 14, ha='left', color=BODY)
            gold = lab in ('diseased', 'not repaid')
            s.box(x0 + 2.35, y - 0.2, 1.28, 0.4, lab, size=14, fill=GOLD if gold else PAPER, weight='bold', r=0.06)
        s.arrow(x0 + pw / 2, h - 2.75, x0 + pw / 2, h - 3.15, lw=2.2)
        s.icon('robot', x0 + 0.45, h - 3.62, 0.62)
        s.box(x0 + 0.85, h - 3.98, pw - 0.85, 0.72, '', fill=PAPER, lw=1.8, r=0.08)
        _wrap(s, x0 + 0.85 + (pw - 0.85) / 2, h - 3.62, pw - 1.05, out, 15, weight='bold')
    s.text(w / 2, 0.22, 'The same idea: learn from past examples whose answer is known', size=16, weight='bold', color=RED)
    return s


# ------------------------------------------------------------------ hook: Numida, Kampala (BNK-03)
@fig('x_l02_numida')
def x_l02_numida(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.28, 'Numida, Uganda: working-capital loans for small businesses', size=17, weight='bold', ha='left')
    bh = 0.8

    def lane(y, items):
        x = 0.1
        for i, (txt, wd, gold) in enumerate(items):
            s.box(x, y, wd, bh, '', fill=GOLD if gold else PAPER, lw=1.8, r=0.08)
            _wrap(s, x + wd / 2, y + bh / 2, wd - 0.2, txt, 15, weight='bold' if gold else 'normal')
            if i < len(items) - 1:
                s.arrow(x + wd + 0.04, y + bh / 2, x + wd + 0.36, y + bh / 2, lw=2.2, head=15)
            x += wd + 0.4
    lane(h - 1.45, [('Repeat client in good standing', 2.05, False), ('Scored by a model built from Numida’s own loan records', 2.75, False), ('Approved instantly', 1.9, True)])
    lane(h - 2.5, [('New client, or a larger loan', 2.05, False), ('A longer check', 2.75, False), ('Up to 24 hours', 1.9, False)])
    for i, (big, txt) in enumerate((('$20 million', 'lent to micro and small businesses by September 2022'),
                                    ('$250,000 to $2 million', 'lent each month, as monthly lending grew'))):
        x = 0.1 + i * 3.8
        s.box(x, 0.55, 3.6, 1.25, '', fill=PAPER, lw=1.6, r=0.08)
        s.text(x + 0.2, 1.47, big, size=22, weight='bold', ha='left', color=RED, parse_math=False)
        _wrap(s, x + 0.2, 0.92, 3.25, txt, 14, ha='left', color=BODY)
    _source(s, 'Source: TechCrunch, 28 Sep 2022. Company figures; no repayment rates published.')
    return s


# ------------------------------------------------------------------ the experienced loan officer and the model
@fig('x_l02_officer')
def x_l02_officer(w, h, **_):
    s = Scene(w, h)
    rows = [(h - 1.3, 'An experienced loan officer', 'person', 'A career of files', 'Remembers who repaid and who did not', '“Looks like a good risk”'),
            (h - 3.2, 'A prediction model', 'robot', 'Every record you hold', 'Finds the patterns that separated the two', '8 in 10 likely to repay')]
    for y, who, ic, src, how, out in rows:
        s.text(0.1, y + 0.85, who, size=17, weight='bold', ha='left')
        for k in range(3):
            s.icon('folder', 0.55 + k * 0.16, y + 0.05 - k * 0.12, 0.6)
        s.text(0.15, y - 0.62, src, size=14, ha='left', color=BODY)
        s.arrow(1.55, y, 2.15, y, lw=2.2, head=15)
        s.icon(ic, 2.6, y + 0.05, 0.8)
        _wrap(s, 3.1, y, 2.0, how, 15, ha='left', color=BODY)
        s.arrow(5.15, y, 5.6, y, lw=2.2, head=15)
        s.box(5.65, y - 0.42, 1.95, 0.84, '', fill=GOLD, lw=1.8, r=0.08)
        _wrap(s, 5.65 + 0.975, y, 1.75, out, 15, weight='bold')
    s.line(0.1, h - 2.18, w - 0.1, h - 2.18, color=HAIR, lw=1.2)
    s.text(w / 2, 0.45, 'Same habit: judge a new case by what happened to similar past cases', size=15, weight='bold', color=RED)
    s.text(w - 0.1, 0.1, 'The score is illustrative', size=14, color=MUTE, ha='right')
    return s


# ------------------------------------------------------------------ past records with a known outcome
@fig('x_l02_records')
def x_l02_records(w, h, **_):
    s = Scene(w, h)
    cols = [1.0, 1.35, 1.5, 1.75, 1.6]
    x0 = 0.25
    rows = [['Client', 'Years a\nclient', 'Late\npayments', 'Loan, UGX', 'Outcome'],
            ['A', '6', '0', '2,000,000', 'repaid'],
            ['B', '1', '3', '5,000,000', 'not repaid'],
            ['C', '3', '1', '1,500,000', 'repaid'],
            ['D', '4', '0', '3,000,000', 'repaid'],
            ['E', '1', '2', '800,000', 'not repaid'],
            ['New', '2', '1', '2,500,000', '?']]
    rh = 0.45
    top = h - 0.95
    hl = {(r, 4): GOLD for r in range(1, 6)}
    hl[(6, 4)] = PALE
    for c in range(5):
        hl[(6, c)] = hl.get((6, c), PALE)
    s.table(x0, top, cols, rh, rows, size=15, hl_cells=hl)
    s.text(x0 + 6 * 0 + 1.0 + 4.6 / 2 - 0.0, h - 0.55, 'What we knew when we lent: features', size=15, weight='bold')
    s.brace(x0 + 1.0, x0 + 1.0 + 4.6, h - 0.8, depth=-0.12)
    s.text(x0 + 5.6 + 0.8, h - 0.3, 'What happened:', size=15, weight='bold', color=RED)
    s.text(x0 + 5.6 + 0.8, h - 0.58, 'the label', size=15, weight='bold', color=RED)
    s.text(x0 + 7.2 - 0.8, top - 7 * rh - 0.3, 'Prediction fills in the ?', size=15, weight='bold', color=RED)
    s.text(0.1, 0.18, 'Illustrative records', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ learning: one question sorts 100 past borrowers
@fig('x_l02_sorting')
def x_l02_sorting(w, h, **_):
    s = Scene(w, h)
    s.box(w / 2 - 1.9, h - 0.85, 3.8, 0.7, 'Paid late in the past year?', size=17, weight='bold', lw=2, r=0.08)
    s.text(0.1, h - 0.3, '100 past borrowers', size=15, color=BODY, ha='left')
    sq, gap = 0.2, 0.06
    groups = [(1.75, 'yes', 6, 5, 12, '12 of 30 did not repay', 'about 4 in 10'), (5.45, 'no', 10, 7, 3, '3 of 70 did not repay', 'about 4 in 100')]
    gtop = h - 1.7
    for cx, lab, nc, nr, bad, cap, rate in groups:
        gw = nc * (sq + gap) - gap
        s.line(w / 2, h - 0.85, cx, gtop + 0.15, lw=1.8, z=1)
        s.text((w / 2 + cx) / 2 + (-0.35 if lab == 'yes' else 0.35), (h - 0.85 + gtop + 0.15) / 2 + 0.05, lab, size=16, weight='bold', color=RED)
        k = 0
        for r in range(nr):
            for c in range(nc):
                x = cx - gw / 2 + c * (sq + gap)
                y = gtop - (r + 1) * (sq + gap) + gap
                s.rect(x, y, sq, sq, fill=RED if k < bad else PAPER, edge=INK, lw=1.0)
                k += 1
        gb = gtop - nr * (sq + gap)
        s.text(cx, gb - 0.25, cap, size=15, weight='bold')
        s.text(cx, gb - 0.55, rate, size=15, color=BODY)
    s.rect(0.15, 0.13, 0.2, 0.2, fill=RED, edge=INK, lw=1.0)
    s.text(0.45, 0.23, 'did not repay', size=14, ha='left')
    s.text(w - 0.1, 0.23, 'Illustrative counts', size=14, color=MUTE, ha='right')
    return s


# ------------------------------------------------------------------ three kinds of prediction
@fig('x_l02_three_kinds')
def x_l02_three_kinds(w, h, **_):
    s = Scene(w, h)
    cw = (w - 0.2) / 3
    heads = [('A yes or no', 'Will this client repay?', 'classification'),
             ('A number', 'How many crates will this shop order next month?', 'forecast, or regression'),
             ('A ranking', 'Which customers do we call first?', 'ranking, or scoring')]
    for i, (hd, q, term) in enumerate(heads):
        x = 0.1 + i * cw
        cx = x + cw / 2
        if i:
            s.line(x, 0.3, x, h - 0.2, color=HAIR, lw=1.2)
        s.text(cx, h - 0.35, hd, size=19, weight='bold')
        py = h - 1.55
        if i == 0:
            s.icon('check', cx - 0.5, py, 1.1)
            s.icon('cross', cx + 0.5, py, 1.1)
        elif i == 1:
            vals = [0.5, 0.65, 0.55, 0.75]
            for k, v in enumerate(vals):
                s.rect(cx - 0.95 + k * 0.42, py - 0.55, 0.3, v * 1.2, fill=PAPER, edge=INK, lw=1.6)
            s.rect(cx - 0.95 + 4 * 0.42, py - 0.55, 0.3, 0.85 * 1.2, fill=GOLD, edge=INK, lw=1.6)
            s.text(cx - 0.95 + 4 * 0.42 + 0.15, py - 0.55 + 0.85 * 1.2 + 0.2, '?', size=18, weight='bold', color=RED)
            s.line(cx - 1.05, py - 0.55, cx + 1.05, py - 0.55, lw=1.8)
        else:
            for k in range(3):
                yy = py + 0.45 - k * 0.45
                s.text(cx - 0.6, yy, str(k + 1), size=17, weight='bold', color=RED if k == 0 else INK)
                s.icon('person', cx - 0.15, yy, 0.42)
                s.rect(cx + 0.15, yy - 0.08, 0.9 - k * 0.25, 0.16, fill=GOLD if k == 0 else PAPER, edge=INK, lw=1.2)
        _wrap(s, cx, h - 2.75, cw - 0.3, q, 16, color=BODY)
        s.text(cx, 1.05, 'Industry term', size=14, color=MUTE)
        _wrap(s, cx, 0.65, cw - 0.25, term, 16, weight='bold')
    return s


# ------------------------------------------------------------------ a score is a likelihood; someone sets the cut-off
@fig('x_l02_cutoff')
def x_l02_cutoff(w, h, **_):
    s = Scene(w, h)
    scores = [9, 9, 8, 8, 7, 6, 5, 4, 3, 2]
    step = (w - 0.4) / 10
    y = h - 1.65
    s.text(0.1, h - 0.3, 'Ten applicants, sorted by score: chance of repaying, out of 10', size=15, color=BODY, ha='left')
    for i, sc in enumerate(scores):
        x = 0.2 + step * (i + 0.5)
        s.text(x, y + 0.75, f'{sc} in 10', size=14, weight='bold')
        s.icon('person', x, y, 0.62, accent=GOLD if i < 6 else PAPER)
    cut = 0.2 + step * 6
    s.line(cut, y - 0.6, cut, y + 1.05, color=RED, lw=3, dash=True, z=6)
    s.text(cut, y - 0.85, 'the threshold', size=15, weight='bold', color=RED)
    s.arrow(cut - 0.15, y - 1.2, cut - 0.95, y - 1.2, color=RED, lw=2, head=13)
    s.arrow(cut + 0.15, y - 1.2, cut + 0.95, y - 1.2, color=RED, lw=2, head=13)
    s.brace(0.25, cut - 0.1, y - 1.55, depth=0.12)
    s.text((0.25 + cut - 0.1) / 2, y - 1.85, 'Approved automatically', size=16, weight='bold')
    s.brace(cut + 0.1, w - 0.25, y - 1.55, depth=0.12)
    s.text((cut + 0.1 + w - 0.25) / 2, y - 1.85, 'To a loan officer', size=16, weight='bold')
    s.text(w / 2, 0.55, 'The credit policy sets the line. Move it and the work and the risk move too.', size=15, color=BODY)
    s.text(w - 0.1, 0.18, 'Illustrative scores', size=14, color=MUTE, ha='right')
    return s


# ------------------------------------------------------------------ the data decides what it can learn
@fig('x_l02_data_decides')
def x_l02_data_decides(w, h, **_):
    s = Scene(w, h)
    tiles = [('calendar', 'History', 'Records kept long enough to cover good years and bad years'),
             ('tag', 'Labels', 'The outcome written down for each case: repaid or not, bought or not'),
             ('people', 'Enough cases', 'Many examples of each outcome, and of the rare one most of all'),
             ('clock', 'The future like the past', 'No big change since: a new product, a drought or a new law breaks the pattern')]
    tw, th = (w - 0.3) / 2, (h - 0.3) / 2
    for i, (ic, hd, tx) in enumerate(tiles):
        x = 0.1 + (i % 2) * (tw + 0.1)
        y = 0.1 + (1 - i // 2) * (th + 0.1)
        s.box(x, y, tw, th, '', fill=PAPER, lw=1.8, r=0.08)
        s.icon(ic, x + 0.55, y + th - 0.55, 0.8)
        _wrap(s, x + 1.05, y + th - 0.55, tw - 1.2, hd, 18, weight='bold', ha='left')
        _wrap(s, x + 0.25, y + (th - 1.0) / 2 + 0.05, tw - 0.45, tx, 15, ha='left', color=BODY)
    return s


# ------------------------------------------------------------------ fair testing: keep some records aside
@fig('x_l02_holdout')
def x_l02_holdout(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.3, '240 past claims from today’s demonstration, cut into 5 piles of 48', size=15, color=BODY, ha='left')
    bw, bh, gap = 1.3, 1.1, 0.12
    x0 = (w - (5 * bw + 4 * gap)) / 2
    y = h - 1.85
    for k in range(5):
        aside = k == 4
        s.box(x0 + k * (bw + gap), y, bw, bh, '', fill=GOLD if aside else PAPER, lw=2, r=0.06)
        s.icon('receipt', x0 + k * (bw + gap) + bw / 2, y + bh / 2 + 0.12, 0.55)
        s.text(x0 + k * (bw + gap) + bw / 2, y + 0.2, '48', size=16, weight='bold')
    s.brace(x0, x0 + 4 * bw + 3 * gap, y - 0.12, depth=0.12)
    s.text(x0 + (4 * bw + 3 * gap) / 2, y - 0.45, 'It learns from these 192', size=16, weight='bold')
    s.brace(x0 + 4 * (bw + gap), x0 + 5 * bw + 4 * gap, y - 0.12, depth=0.12)
    s.text(x0 + 4 * (bw + gap) + bw / 2, y - 0.45, 'Kept aside', size=16, weight='bold', color=RED)
    s.box(0.4, 0.75, w - 0.8, 1.05, '', fill=PAPER, lw=1.6, r=0.08)
    _wrap(s, w / 2, 1.43, w - 1.2, 'Then it is scored only on the 48 it never saw.', 16, weight='bold')
    _wrap(s, w / 2, 1.0, w - 1.2, 'Like judging a new loan officer on files they have never seen.', 15, color=BODY)
    s.text(w / 2, 0.3, 'The industry calls the kept-aside records the test set.', size=15, color=MUTE)
    return s


# ------------------------------------------------------------------ overfitting: the pattern, or the slips
@fig('x_l02_overfit')
def x_l02_overfit(w, h, **_):
    s = Scene(w, h)
    repaid = [(0.55, 0.15), (0.7, 0.3), (0.8, 0.12), (0.62, 0.4), (0.9, 0.35), (0.45, 0.22), (0.75, 0.55), (0.9, 0.62), (0.35, 0.1)]
    late = [(0.15, 0.7), (0.25, 0.88), (0.32, 0.6), (0.1, 0.45), (0.42, 0.82), (0.12, 0.22), (0.55, 0.9), (0.6, 0.75)]
    slip_r, slip_l = (0.2, 0.78), (0.8, 0.22)
    pw, ph = 3.1, 2.6
    for pi, (x0, title, cap) in enumerate(((0.45, 'Learns the pattern', 'A few slips stay on the wrong side'),
                                           (4.35, 'Learns the slips too', 'Perfect on past cases, worse on new ones'))):
        y0 = 1.2
        s.text(x0 + pw / 2, h - 0.3, title, size=18, weight='bold', color=RED if pi else INK)
        s.rect(x0, y0, pw, ph, fill=PAPER, edge=HAIR, lw=1.2, z=1)
        P = lambda u, v: (x0 + u * pw, y0 + v * ph)
        for u, v in repaid + [slip_r]:
            px, py = P(u, v)
            s.circle(px, py, 0.08, fill=PAPER, edge=INK, lw=1.5, z=4)
        for u, v in late + [slip_l]:
            px, py = P(u, v)
            s.rect(px - 0.08, py - 0.08, 0.16, 0.16, fill=GOLD, edge=INK, lw=1.3, z=4)
        a, b = P(0.03, 0.03), P(0.97, 0.97)
        s.line(a[0], a[1], b[0], b[1], color=RED, lw=2.6, z=3)
        if pi:
            for (u, v) in (slip_r, slip_l):
                cx, cy = P(u, v)
                s.ax.add_patch(Ellipse((cx, cy), 0.75, 0.5, fc='none', ec=RED, lw=2.6, zorder=3))
            nx, ny = P(0.88, 0.2)
            s.ax.plot([nx], [ny], marker='*', ms=20, color=RED, zorder=6)
        _wrap(s, x0 + pw / 2, 0.85, pw + 0.2, cap, 15, color=BODY)
        s.text(x0 + pw / 2, y0 - 0.12, '', size=14)
    s.circle(0.55, 0.3, 0.08, fill=PAPER, edge=INK, lw=1.5)
    s.text(0.72, 0.3, 'repaid', size=14, ha='left')
    s.rect(1.62, 0.22, 0.16, 0.16, fill=GOLD, edge=INK, lw=1.3)
    s.text(1.88, 0.3, 'did not repay', size=14, ha='left')
    s.ax.plot([3.65], [0.3], marker='*', ms=16, color=RED)
    s.text(3.82, 0.3, 'a new client, wrongly refused', size=14, ha='left')
    s.text(w - 0.1, 0.3, 'Illustration', size=14, color=MUTE, ha='right')
    return s


# ------------------------------------------------------------------ good at, bad at
@fig('x_l02_good_bad')
def x_l02_good_bad(w, h, **_):
    s = Scene(w, h)
    cols = [('Good at', 'check', ['Many similar decisions, made every day', 'Spotting patterns across thousands of records', 'Being fast and consistent', 'Showing whom to look at first']),
            ('Bad at', 'cross', ['Rare events with few past cases', 'A future unlike the past', 'Saying why, unless built to explain', 'Fairness, if past decisions were unfair'])]
    cw = (w - 0.3) / 2
    for i, (hd, ic, items) in enumerate(cols):
        x = 0.1 + i * (cw + 0.1)
        s.text(x + 0.1, h - 0.35, hd, size=20, weight='bold', ha='left', color=RED if i else INK)
        s.line(x, h - 0.65, x + cw, h - 0.65, lw=1.8)
        for k, it in enumerate(items):
            y = h - 1.25 - k * 0.98
            s.icon(ic, x + 0.35, y, 0.6)
            _wrap(s, x + 0.8, y, cw - 0.95, it, 16, ha='left', color=BODY)
    return s


# ------------------------------------------------------------------ industry tour: six industries
@fig('x_l02_six')
def x_l02_six(w, h, **_):
    s = Scene(w, h)
    tiles = [('calculator', 'Banking and microfinance', 'Who will repay a loan', 'Numida, Uganda'),
             ('phone', 'Telecom and mobile money', 'A credit score from mobile-money data', 'Airtel Money and GnuGrid CRB, Uganda'),
             ('plant', 'Agriculture and agribusiness', 'Which farmers get seed and fertiliser on credit', 'Apollo Agriculture, Kenya'),
             ('bottle', 'Manufacturing and FMCG', 'What each shop will order next', 'Coca-Cola suggested orders'),
             ('clinic', 'Healthcare and insurance', 'Which mothers’ messages are urgent', 'Jacaranda Health, Kenya'),
             ('people', 'Public sector', 'Which households are poorest, to send cash', 'Novissi, Togo')]
    gap = 0.12
    tw = (w - 0.2 - 2 * gap) / 3
    th = (h - 0.5 - gap) / 2
    for i, (ic, ind, use, ex) in enumerate(tiles):
        x = 0.1 + (i % 3) * (tw + gap)
        y = 0.45 + (1 - i // 3) * (th + gap)
        s.box(x, y, tw, th, '', fill=PAPER, lw=1.8, r=0.08)
        s.icon(ic, x + 0.5, y + th - 0.55, 0.75)
        tx = x + 1.0
        iw = tw - 1.15
        top = y + th - 0.15
        hh = _wrap(s, tx, top, iw, ind, 16, weight='bold', ha='left', va='top')
        top -= hh + 0.1
        uh = _wrap(s, tx, top, iw, use, 15, ha='left', va='top', color=BODY)
        top -= uh + 0.08
        _wrap(s, tx, top, iw, ex, 15, weight='bold', ha='left', va='top', color=RED)
    _source(s, 'Sources: TechCrunch 2022; TechAfrica News 2024; AI News 2026; Penn State 2023; J-PAL 2026. Company figures where stated.', y=0.16)
    return s


# ------------------------------------------------------------------ a case told as a story: problem, AI, result, catch
@fig('x_l02_case')
def x_l02_case(w, h, org='', icon='doc', problem='', ai='', big='', result='', catch='', source='', **_):
    s = Scene(w, h)
    s.icon(icon, 0.45, h - 0.35, 0.62)
    s.text(0.9, h - 0.35, org, size=19, weight='bold', ha='left')
    gap = 0.32
    cw = (w - 0.2 - 3 * gap) / 4
    y0, y1 = 0.55, h - 0.8
    heads = ['The problem', 'What the AI does', 'The result', 'The catch']
    texts = [problem, ai, result, catch]
    inner = cw - 0.3
    sizes = []
    for i, t in enumerate(texts):
        avail = (y1 - y0) - 0.65 - (0.62 if i == 2 else 0)
        sizes.append(_fit(t, inner, avail, 17, 14))
    sz = min(sizes)
    for i, (hd, t) in enumerate(zip(heads, texts)):
        x = 0.1 + i * (cw + gap)
        s.box(x, y0, cw, y1 - y0, '', fill=GOLD if i == 2 else PAPER, lw=2 if i != 3 else 2.2, edge=RED if i == 3 else INK, r=0.08)
        s.text(x + 0.15, y1 - 0.3, hd, size=17, weight='bold', ha='left', color=RED if i == 3 else INK)
        top = y1 - 0.62
        if i == 2:
            bs = _fit(big, inner, 0.55, 24, 16, 'bold')
            _wrap(s, x + 0.15, top, inner, big, bs, weight='bold', ha='left', va='top')
            top -= len(K.wrap(big, bs, 'bold', inner)) * _lh(bs) + 0.1
        _wrap(s, x + 0.15, top, inner, t, sz, ha='left', va='top', color=INK if i == 2 else BODY)
        if i < 3:
            s.arrow(x + cw + 0.03, (y0 + y1) / 2, x + cw + gap - 0.03, (y0 + y1) / 2, lw=2.2, head=14)
    _source(s, source, y=0.2)
    return s


# ------------------------------------------------------------------ demonstration: each rule as a likelihood (recorded)
@fig('x_l02_leaves')
def x_l02_leaves(w, h, **_):
    tree = _res()['tree']
    leaves = []

    def walk(n, path):
        if 'leaf' in n:
            leaves.append((path, n['counts']['queried'], n['n']))
            return
        f, t = n['feature'], n['thr']
        if f.startswith('receipt'):
            a, b = 'No receipt', 'Receipt'
        elif f.startswith('amount'):
            a, b = f'up to {int(t) * 1000:,}', f'over {int(t) * 1000:,}'
        else:
            a, b = f'filed within {int(t)} days', f'filed after {int(t)} days'
        walk(n['left'], path + [a])
        walk(n['right'], path + [b])
    walk(tree, [])
    leaves.sort(key=lambda r: (-r[1] / r[2], -r[2]))
    s = Scene(w, h)
    s.text(0.1, h - 0.3, 'Rule the model learned (amounts in UGX)', size=15, weight='bold', ha='left')
    s.text(w - 0.1, h - 0.3, 'Share queried', size=15, weight='bold', ha='right')
    s.line(0.1, h - 0.52, w - 0.1, h - 0.52, lw=1.6)
    rh = (h - 1.05) / len(leaves)
    bx, bw = 5.0, 1.55
    for i, (path, q, n) in enumerate(leaves):
        y = h - 0.55 - (i + 0.5) * rh
        _wrap(s, 0.1, y, 4.75, ', '.join(path), 14, ha='left', color=BODY)
        s.rect(bx, y - 0.13, bw, 0.26, fill=PAPER, edge=INK, lw=1.2)
        s.rect(bx, y - 0.13, bw * q / n, 0.26, fill=GOLD, edge=INK, lw=1.2, z=3)
        s.text(w - 0.1, y, f'{q} of {n}', size=15, weight='bold', ha='right', color=RED if n < 6 else INK)
    s.text(0.1, 0.22, 'Red: too few cases to trust. Recorded run, 5 November 2026; fictional claims.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ demonstration: enough cases (recorded)
@fig('x_l02_enough')
def x_l02_enough(w, h, **_):
    r = _res()
    claims = r['tree_cv']['3'][0]
    m = r['cv_messages']['decision tree depth 3 on words']['mean']
    rights = [str(f['test_right']) for f in r['messages_one_split']]
    s = Scene(w, h)
    cw = (w - 0.3) / 2
    panels = [('receipt', '240 expense claims', 'Amount, receipt, days to file', f'{round(claims * 100)} in 100', 'right on claims it had not seen', 'Average of 100 tests'),
              ('speech', '40 customer messages', 'Free text from shops', f'{round(m * 100)} in 100', 'right on messages it had not seen', 'One round of tests: ' + ', '.join(rights[:-1]) + ' and ' + rights[-1] + ' right out of 8')]
    for i, (ic, hd, sub, big, what, foot) in enumerate(panels):
        x = 0.1 + i * (cw + 0.1)
        s.box(x, 0.65, cw, h - 0.75, '', fill=GOLD if i == 0 else PAPER, lw=2, r=0.08)
        s.icon(ic, x + 0.5, h - 0.6, 0.7)
        s.text(x + 0.95, h - 0.45, hd, size=18, weight='bold', ha='left')
        s.text(x + 0.95, h - 0.8, sub, size=15, color=BODY, ha='left')
        s.text(x + cw / 2, h - 1.95, big, size=36, weight='bold', color=INK if i == 0 else RED)
        _wrap(s, x + cw / 2, h - 2.65, cw - 0.4, what, 16)
        _wrap(s, x + cw / 2, 1.25, cw - 0.4, foot, 15, color=BODY)
    s.text(0.1, 0.25, 'Recorded runs, scikit-learn 1.9.1, 5 and 11 November 2026. The claims are fictional.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ your people: roles, tasks, skills, fears
@fig('x_l02_people')
def x_l02_people(w, h, **_):
    s = Scene(w, h)
    lab_w = 1.45
    cw = (w - 0.1 - lab_w) / 3
    roles = [('Loan officer', ['Checking every routine file', 'The close calls, and talking to the client', 'Reading a score and knowing its limits', 'Fear: replaced. Gain: time for hard cases']),
             ('Demand planner', ['Building every forecast by hand', 'Judging events the past never showed', 'Knowing when to override the number', 'Fear: blamed for a miss. Gain: earlier warning']),
             ('Sales rep', ['Guessing what each shop needs', 'Advice and the relationship', 'Explaining a suggestion to a shopkeeper', 'Fear: the app sells instead. Gain: a ready suggestion'])]
    labels = ['Less of', 'More of', 'Skill to grow', 'Fears and gains']
    top = h - 0.85
    rh = (top - 0.1) / 4
    for i, (role, cells) in enumerate(roles):
        x = 0.1 + lab_w + i * cw
        s.icon('person', x + 0.45, h - 0.42, 0.62, accent=GOLD)
        s.text(x + 0.85, h - 0.42, role, size=18, weight='bold', ha='left')
        for r, txt in enumerate(cells):
            y = top - r * rh
            s.rect(x + 0.05, y - rh + 0.05, cw - 0.1, rh - 0.08, fill=PALE if r == 3 else PAPER, edge=HAIR, lw=1.0, z=1)
            _wrap(s, x + 0.2, y - rh / 2 + 0.02, cw - 0.4, txt, 15, ha='left', color=BODY)
    for r, lab in enumerate(labels):
        y = top - r * rh - rh / 2
        _wrap(s, 0.1, y, lab_w - 0.1, lab, 15, weight='bold', ha='left', color=RED if r == 3 else INK)
    return s


# ------------------------------------------------------------------ who owns the decision
@fig('x_l02_owner')
def x_l02_owner(w, h, **_):
    s = Scene(w, h)
    steps = [('Builds and tests the model', 'Data team or vendor', 'gear'),
             ('Sets the cut-off and the rules', 'Credit committee', 'shield'),
             ('Scores every case', 'The model', 'robot'),
             ('Decides close calls and refusals', 'Loan officer', 'person'),
             ('Can ask why, and appeal', 'The customer', 'speech')]
    bw = 4.25
    bh = 0.7
    gap = (h - 0.2 - 5 * bh) / 4
    for i, (what, who, ic) in enumerate(steps):
        y = h - 0.1 - bh - i * (bh + gap)
        gold = i == 1
        s.box(0.1, y, bw, bh, '', fill=GOLD if gold else PAPER, lw=1.8, r=0.08)
        s.icon(ic, 0.45, y + bh / 2, 0.48)
        s.text(0.8, y + bh / 2 + 0.14, who, size=15, weight='bold', ha='left')
        s.text(0.8, y + bh / 2 - 0.16, what, size=14, ha='left', color=BODY)
        if i < 4:
            s.arrow(0.1 + bw / 2, y - 0.02, 0.1 + bw / 2, y - gap + 0.02, lw=1.8, head=12)
    x = 4.6
    s.box(x, 1.05, w - x - 0.1, h - 1.15, '', fill=PAPER, edge=RED, lw=2.2, r=0.08)
    s.text(x + 0.15, h - 0.4, 'Kenya, April 2026', size=16, weight='bold', color=RED, ha='left')
    hh = _wrap(s, x + 0.15, h - 0.65, w - x - 0.4, 'Petitions in the High Court say M-Shwari and Fuliza limits come from “black box” algorithms customers cannot see or appeal.', 15, ha='left', va='top', color=BODY)
    hh += _wrap(s, x + 0.15, h - 0.8 - hh, w - x - 0.4, 'Orders sought: an audit, and a pause on automated decisions until rules exist.', 15, ha='left', va='top', color=BODY)
    _wrap(s, x + 0.15, h - 0.95 - hh, w - x - 0.4, 'No ruling yet. These are claims.', 15, weight='bold', ha='left', va='top', color=RED)
    _wrap(s, x + 0.15, 0.62, w - x - 0.3, 'Name one owner who answers for the results.', 15, weight='bold', ha='left')
    s.text(x + 0.15, 0.2, 'Source: HapaKenya, 24 April 2026', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ hands-on: one portfolio entry (fictional company)
@fig('x_l02_portfolio')
def x_l02_portfolio(w, h, **_):
    s = Scene(w, h)
    rows = [('The use', 'Rank shops by risk of ordering less next month'),
            ('What goes in', 'Two years of orders for each shop'),
            ('What comes out', 'A ranked list every Monday'),
            ('Who uses it', 'Area sales reps'),
            ('How we would know it works', 'Of the 20 shops ranked top, how many ordered less'),
            ('Today: kind, and the decision it changes', 'A ranking: which shops a rep visits first')]
    s.text(0.05, h - 0.2, 'Nile Valley Foods (fictional): one entry', size=15, weight='bold', ha='left')
    lw_ = 1.85
    vw = w - 0.1 - lw_
    hs = []
    for a, b in rows:
        n = max(len(K.wrap(a, 14, 'bold', lw_ - 0.15)), len(K.wrap(b, 14, 'regular', vw - 0.15)))
        hs.append(n * _lh(14) + 0.1)
    y = h - 0.42
    for i, ((a, b), rh) in enumerate(zip(rows, hs)):
        last = i == len(rows) - 1
        s.rect(0.05, y - rh, lw_, rh, fill=GOLD if last else PALE, edge=INK, lw=1.0)
        s.rect(0.05 + lw_, y - rh, vw, rh, fill=PAPER, edge=INK, lw=1.0)
        _wrap(s, 0.12, y - rh / 2, lw_ - 0.15, a, 14, weight='bold', ha='left')
        _wrap(s, 0.12 + lw_, y - rh / 2, vw - 0.15, b, 14, ha='left', color=BODY)
        y -= rh
    return s


# ------------------------------------------------------------------ take-away: five numbered cards
@fig('x_l02_takeaway')
def x_l02_takeaway(w, h, items=(), **_):
    s = Scene(w, h)
    n = len(items)
    gap = 0.2
    cw = (w - 0.2 - gap * (n - 1)) / n
    for i, it in enumerate(items):
        x = 0.1 + i * (cw + gap)
        s.box(x, 0.1, cw, h - 0.2, '', fill=GOLD if i == n - 1 else PAPER, lw=2, r=0.08)
        s.circle(x + 0.4, h - 0.45, 0.24, fill=INK, edge=INK)
        s.text(x + 0.4, h - 0.45, str(i + 1), size=16, weight='bold', color=PAPER, z=7)
        s.icon(it['icon'], x + cw / 2, h - 1.25, 1.0)
        hh = _wrap(s, x + cw / 2, h - 2.0, cw - 0.3, it['head'], 18, weight='bold', va='top')
        _wrap(s, x + cw / 2, h - 2.15 - hh, cw - 0.3, it['text'], 16, va='top', color=BODY)
    return s
