"""Figures for Leadership Edition Session 4, AI that understands language: sort, search, translate and summarise.  Names: x_l04_*  (content kind 'l04_*').

No maths anywhere: pictures, counts and ranks only.  The search-by-meaning numbers are read from the recorded run in demo_runs/s04/
(results.json; sentence-transformers 6.2.0, model all-MiniLM-L6-v2, 6 November 2026).  The clauses, finance terms, HR paragraphs and
customer messages are invented for Nile Valley Foods, the fictional course company.  Case figures come from research/*.md (IDs in the
content file).  The map of meaning, the sorting trays and the summary are illustrations, labelled so on the slide.

Some generic figures here (x_l04_six, x_l04_people, x_l04_portfolio, x_l04_goodbad) take their text as parameters and are reused by Session 5.
"""
import json
from pathlib import Path

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD, fig
import slidekit as K
from diagrams_l02 import _wrap, _fit, _source, _lh

RUN = Path(__file__).resolve().parent.parent / 'demo_runs' / 's04'
_C = {}


def _res():
    if not _C:
        _C.update(json.load(open(RUN / 'results.json')))
    return _C


def _query(qid):
    for skin in _res()['skins'].values():
        for q in skin['queries']:
            if q['qid'] == qid:
                return q
    raise KeyError(qid)


def _all_queries():
    out = []
    for skin in ('contracts', 'finance', 'hr'):
        out += _res()['skins'][skin]['queries']
    return out


def _nlines(text, size, w, weight='normal'):
    return len(K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', w))


# ------------------------------------------------------------------ recall bridge: records in Sessions 2 and 3, messages today
@fig('x_l04_bridge')
def x_l04_bridge(w, h, **_):
    s = Scene(w, h)
    panels = [
        (0.1, 'Sessions 2 and 3: records', 'doc', [('New client, 3 late payments', 'not repaid'), ('5 years a client, always on time', 'repaid'), ('Claim, no receipt, UGX 90,000', 'queried')],
         'A score, then false alarms and misses'),
        (3.95, 'Today: messages', 'speech', [('“Please send 20 bags of maize flour to Mbale”', 'order'), ('“The maize flour was late and the invoice is wrong”', 'complaint'), ('“Please send the invoice for the rice order”', 'payment')],
         'Same idea: learn the label, then judge it'),
    ]
    pw = 3.65
    for x0, head, ic, rows, out in panels:
        s.text(x0 + 0.05, h - 0.3, head, size=18, weight='bold', ha='left')
        s.line(x0, h - 0.55, x0 + pw, h - 0.55, lw=1.6)
        for i, (txt, lab) in enumerate(rows):
            y = h - 1.1 - i * 0.75
            s.icon(ic, x0 + 0.28, y, 0.48)
            _wrap(s, x0 + 0.62, y, 1.7, txt, 14, ha='left', color=BODY)
            gold = lab in ('not repaid', 'queried', 'complaint')
            s.box(x0 + 2.42, y - 0.2, 1.2, 0.4, lab, size=14, fill=GOLD if gold else PAPER, weight='bold', r=0.06)
        s.arrow(x0 + pw / 2, h - 2.85, x0 + pw / 2, h - 3.2, lw=2.2)
        s.icon('robot', x0 + 0.45, h - 3.68, 0.62)
        s.box(x0 + 0.85, h - 4.04, pw - 0.85, 0.72, '', fill=PAPER, lw=1.8, r=0.08)
        _wrap(s, x0 + 0.85 + (pw - 0.85) / 2, h - 3.68, pw - 1.05, out, 15, weight='bold')
    s.text(w / 2, 0.22, 'A message is a record too: AI sorts it, and Session 3 judges it', size=16, weight='bold', color=RED)
    return s


# ------------------------------------------------------------------ hook: ULII, Uganda (GAP-08)
@fig('x_l04_ulii')
def x_l04_ulii(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.28, 'ULII: Uganda’s free online library of laws and judgments', size=17, weight='bold', ha='left')
    stats = [('41,000+', 'decisions in the library'), ('350,000', 'users a month, in 45 countries'), ('50+ pages', 'the length of some judgments')]
    bw = (w - 0.2 - 2 * 0.15) / 3
    for i, (big, txt) in enumerate(stats):
        x = 0.1 + i * (bw + 0.15)
        s.box(x, h - 1.95, bw, 1.3, '', fill=PAPER, lw=1.6, r=0.08)
        s.text(x + bw / 2, h - 1.0, big, size=24, weight='bold', color=RED)
        _wrap(s, x + bw / 2, h - 1.6, bw - 0.25, txt, 15, color=BODY)
    s.text(0.1, h - 2.3, 'What it added in 2025 and 2026', size=16, weight='bold', ha='left')
    steps = [('doc', 'A long judgment'), ('robot', 'An AI summary'), ('book', 'Links to the laws it cites'), ('bell', 'Alerts on new decisions')]
    sw = (w - 0.2 - 3 * 0.3) / 4
    y = h - 3.3
    for i, (ic, txt) in enumerate(steps):
        x = 0.1 + i * (sw + 0.3)
        s.box(x, y - 0.62, sw, 1.24, '', fill=GOLD if i == 1 else PAPER, lw=1.8, r=0.08)
        s.icon(ic, x + sw / 2, y + 0.3, 0.45)
        _wrap(s, x + sw / 2, y - 0.3, sw - 0.2, txt, 15, weight='bold' if i == 1 else 'normal')
        if i < 3:
            s.arrow(x + sw + 0.02, y, x + sw + 0.28, y, lw=2.2, head=13)
    s.text(0.1, 0.6, 'No accuracy or time-saved figures have been published.', size=15, weight='bold', color=RED, ha='left')
    _source(s, 'Sources: The Observer, 26 Mar 2026; Judiciary of Uganda, 19 Feb 2026.')
    return s


# ------------------------------------------------------------------ four language jobs
@fig('x_l04_four_jobs')
def x_l04_four_jobs(w, h, **_):
    s = Scene(w, h)
    # the pile of text on the left
    s.box(0.1, 0.55, 2.0, h - 0.65, '', fill=PALE, lw=1.8, r=0.08)
    s.text(1.1, h - 0.4, 'Your text', size=17, weight='bold')
    for k, (ic, lab) in enumerate((('speech', 'messages'), ('doc', 'contracts'), ('phone', 'calls, as text'), ('book', 'reports'))):
        y = h - 1.15 - k * 0.85
        s.icon(ic, 0.5, y, 0.5)
        s.text(0.85, y, lab, size=15, ha='left', color=BODY)
    jobs = [('grid', 'Sort', 'Each message gets a label: order, payment, complaint, urgent'),
            ('magnifier', 'Search by meaning', 'Describe it in plain words; find the right clause'),
            ('speech', 'Translate', 'English to Luganda or Swahili, and back'),
            ('doc', 'Summarise', 'Fifty pages to one, for a busy reader')]
    rh = (h - 0.65) / 4
    for i, (ic, hd, tx) in enumerate(jobs):
        yc = h - 0.1 - (i + 0.5) * rh
        s.arrow(2.15, (0.55 + h - 0.1) / 2, 2.85, yc, lw=1.8, head=12)
        s.box(2.9, yc - rh / 2 + 0.06, w - 3.0, rh - 0.12, '', fill=PAPER, lw=1.8, r=0.08)
        s.icon(ic, 3.3, yc, 0.55)
        s.text(3.7, yc + 0.17, hd, size=17, weight='bold', ha='left')
        _wrap(s, 3.7, yc - 0.2, w - 3.9, tx, 14, ha='left', color=BODY)
    return s


# ------------------------------------------------------------------ sorting is prediction
@fig('x_l04_sort')
def x_l04_sort(w, h, **_):
    s = Scene(w, h)
    msgs = ['“Send 20 bags of sugar”', '“Paid by mobile money”', '“The flour was wet”', '“Please call me today”']
    s.text(0.1, h - 0.3, 'Messages arrive', size=16, weight='bold', ha='left')
    for i, m in enumerate(msgs):
        y = h - 0.9 - i * 0.72
        s.icon('speech', 0.4, y, 0.45)
        _wrap(s, 0.75, y, 2.1, m, 14, ha='left', color=BODY)
    s.arrow(2.85, h - 2.0, 3.35, h - 2.0, lw=2.4, head=15)
    s.icon('robot', 3.75, h - 2.0, 0.75)
    s.text(3.75, h - 2.65, 'the model', size=14, color=BODY)
    trays = [('Orders', PAPER, INK), ('Payments', PAPER, INK), ('Complaints', GOLD, INK), ('Urgent: to a person now', PAPER, RED)]
    for i, (lab, fill, edge) in enumerate(trays):
        y = h - 0.95 - i * 0.72
        s.arrow(4.2, h - 2.0, 4.85, y, lw=1.6, head=11)
        s.box(4.9, y - 0.27, w - 5.0, 0.54, '', fill=fill, edge=edge, lw=2.2 if edge == RED else 1.6, r=0.06)
        s.text(5.05, y, lab, size=15, weight='bold', ha='left', color=RED if edge == RED else INK)
    s.box(0.1, 0.5, w - 0.2, 0.75, '', fill=PALE, lw=1.2, r=0.06)
    _wrap(s, w / 2, 0.875, w - 0.5, 'Each label comes with a score, as in Session 2. A wrong tray is a false alarm or a miss, as in Session 3.', 15)
    s.text(w - 0.1, 0.2, 'Illustrative messages', size=14, color=MUTE, ha='right')
    return s


# ------------------------------------------------------------------ word matching misses meaning (recorded corpus, Q1)
@fig('x_l04_nowords')
def x_l04_nowords(w, h, **_):
    s = Scene(w, h)
    q = _query('Q1')
    s.text(0.1, h - 0.3, 'The question, in plain words', size=16, weight='bold', ha='left')
    s.box(0.1, h - 1.45, w - 0.2, 0.95, '', fill=PAPER, lw=1.8, r=0.08)
    s.icon('person', 0.5, h - 0.98, 0.55)
    _wrap(s, 0.95, h - 0.98, w - 1.2, '“' + q['query'] + '”', 16, ha='left')
    s.text(0.1, h - 1.85, 'The clause that answers it', size=16, weight='bold', ha='left')
    s.box(0.1, h - 3.05, w - 0.2, 1.0, '', fill=GOLD, lw=1.8, r=0.08)
    s.icon('doc', 0.5, h - 2.55, 0.55)
    _wrap(s, 0.95, h - 2.55, w - 1.2, 'Force majeure: “Neither party is liable for delay or failure caused by events beyond its reasonable control, including flood, fire, strike or government action.”', 15, ha='left')
    s.icon('cross', 0.45, 1.1, 0.55)
    s.text(0.85, 1.25, 'Word search: no passage shares a word with the question.', size=16, weight='bold', color=RED, ha='left')
    s.text(0.85, 0.9, '“Floods” and “flood” are different words to a word counter.', size=15, color=BODY, ha='left')
    s.text(0.1, 0.25, 'Recorded run, 6 November 2026. The clause is invented for Nile Valley Foods (fictional).', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ meaning as closeness on a map (illustration)
@fig('x_l04_map')
def x_l04_map(w, h, **_):
    s = Scene(w, h)
    s.rect(0.1, 0.55, w - 0.2, h - 0.65, fill=PAPER, edge=HAIR, lw=1.2, z=1)
    groups = [
        ('Delays and weather', (0.3, h - 0.45), [((0.75, h - 0.95), 'star', 'Your question: rain floods the road'),
                                                 ((0.9, h - 1.5), 'gold', 'Force majeure clause'),
                                                 ((0.7, h - 2.05), 'dot', 'Lorry stuck after the rain')]),
        ('Payments', (4.75, h - 0.45), [((5.0, h - 0.95), 'dot', 'Invoice paid'),
                                         ((5.25, h - 1.45), 'dot', 'Please send the invoice'),
                                         ((5.0, h - 1.95), 'dot', 'Bank reconciliation')]),
        ('Staff leave', (4.75, 2.05), [((5.0, 1.6), 'dot', 'I have malaria'),
                                       ((5.25, 1.15), 'dot', 'Sick leave policy'),
                                       ((5.0, 0.75), 'dot', 'Annual leave')]),
    ]
    pts = {}
    for head, (hx, hy), items in groups:
        s.text(hx, hy, head, size=16, weight='bold', color=RED, ha='left')
        for (x, y), kind, lab in items:
            if kind == 'star':
                s.ax.plot([x], [y], marker='*', ms=22, color=RED, zorder=6)
            elif kind == 'gold':
                s.rect(x - 0.1, y - 0.1, 0.2, 0.2, fill=GOLD, edge=INK, lw=1.4, z=5)
            else:
                s.circle(x, y, 0.08, fill=PALE, edge=INK, lw=1.4, z=5)
            s.text(x + 0.2, y, lab, size=14, ha='left', color=INK if kind != 'dot' else BODY)
            pts[lab] = (x, y)
    a = pts['Your question: rain floods the road']
    b = pts['Force majeure clause']
    s.line(a[0] + 0.02, a[1] - 0.13, b[0] - 0.02, b[1] + 0.12, color=RED, lw=2.6, z=4)
    s.text(0.14, (a[1] + b[1]) / 2, 'close', size=14, weight='bold', color=RED, ha='left')
    s.arrow(1.2, h - 2.35, 4.7, 1.45, color=GREY, lw=1.8, head=12, z=3)
    s.arrow(4.7, 1.45, 1.2, h - 2.35, color=GREY, lw=1.8, head=12, z=3)
    s.text(2.3, 1.45, 'far apart: different meanings', size=14, weight='bold', color=MUTE)
    s.text(0.1, 0.25, 'Illustration. A real map has hundreds of directions, and a model works out each position.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ search by meaning, step by step (recorded top 3 for Q1)
@fig('x_l04_search')
def x_l04_search(w, h, **_):
    s = Scene(w, h)
    q = _query('Q1')
    steps = [('person', 'A plain question', 'in your own words'),
             ('pin', 'Placed on the map', 'where its meaning sits'),
             ('magnifier', 'The closest passages', 'ranked, nearest first'),
             ('check', 'A person chooses', 'reads the top few')]
    sw = (w - 0.2 - 3 * 0.3) / 4
    y = h - 1.15
    for i, (ic, hd, tx) in enumerate(steps):
        x = 0.1 + i * (sw + 0.3)
        s.box(x, y - 0.95, sw, 1.9, '', fill=GOLD if i == 3 else PAPER, lw=1.8, r=0.08)
        s.icon(ic, x + sw / 2, y + 0.5, 0.55)
        _wrap(s, x + sw / 2, y - 0.08, sw - 0.2, hd, 15, weight='bold')
        _wrap(s, x + sw / 2, y - 0.6, sw - 0.2, tx, 14, color=BODY)
        if i < 3:
            s.arrow(x + sw + 0.02, y, x + sw + 0.28, y, lw=2.2, head=13)
    s.text(0.1, 1.95, 'Recorded run: the three closest clauses for the flood question', size=15, weight='bold', ha='left')
    for k, t in enumerate(q['top3']):
        yy = 1.5 - k * 0.42
        s.text(0.3, yy, f'{k + 1}', size=15, weight='bold', color=RED if k == 0 else INK)
        s.text(0.55, yy, t['head'], size=15, ha='left', weight='bold' if k == 0 else 'normal')
        if k == 0:
            s.icon('check', 3.3, yy, 0.32)
    s.text(4.0, 1.07, 'Word search looks for the same words.', size=15, ha='left', color=BODY)
    s.text(4.0, 0.67, 'This looks for the same meaning.', size=15, ha='left', weight='bold')
    s.text(0.1, 0.18, 'all-MiniLM-L6-v2, 6 November 2026; invented clauses', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ translation: quality follows the amount of text (illustration)
@fig('x_l04_library')
def x_l04_library(w, h, **_):
    s = Scene(w, h)
    cols = [(0.1, 'English', 'A vast library to learn from', 9, 5), (4.0, 'Luganda, Acholi, Lugbara', 'A small shelf to learn from', 3, 1)]
    cw = 3.6
    for x0, head, sub, nper, nrows in cols:
        s.text(x0 + 0.05, h - 0.3, head, size=18, weight='bold', ha='left')
        s.text(x0 + 0.05, h - 0.62, sub, size=15, color=BODY, ha='left')
        base = h - 0.85
        for r in range(5):
            yb = base - (r + 1) * 0.47
            s.line(x0 + 0.1, yb, x0 + cw - 0.1, yb, lw=2.2)
            if r < nrows:
                for k in range(nper):
                    bx = x0 + 0.2 + k * 0.36
                    hh = 0.28 + 0.05 * ((k * 7 + r * 3) % 3)
                    s.rect(bx, yb + 0.02, 0.26, hh, fill=GOLD if (k + r) % 3 == 0 else PAPER, edge=INK, lw=1.2)
    s.box(0.1, 0.42, w - 0.2, 0.9, '', fill=PALE, lw=1.2, r=0.06)
    _wrap(s, w / 2, 0.87, w - 0.5, 'Less text to learn from means weaker translation and understanding. Test it in your languages, with native speakers.', 15)
    s.text(w - 0.1, 0.17, 'Illustration', size=14, color=MUTE, ha='right')
    return s


# ------------------------------------------------------------------ who is building for African languages (GAP-09, GAP-11, GAP-10, TEL-09, AGR-09)
@fig('x_l04_builders')
def x_l04_builders(w, h, **_):
    s = Scene(w, h)
    tiles = [('Sunbird AI', 'Uganda', 'Models for Ugandan languages, launched with the Ministry of ICT in October 2025'),
             ('Masakhane', 'Pan-African', '400+ volunteers in 20+ countries built 46 open translation test sets'),
             ('Lelapa AI', 'South Africa', 'A small, cheap open model for five African languages, and a paid language service'),
             ('Orange', 'West Africa', 'Adapting OpenAI and Meta models to Wolof and Pulaar: plans, announced 2024')]
    tw, th = (w - 0.3) / 2, (h - 0.65) / 2
    for i, (org, where, tx) in enumerate(tiles):
        x = 0.1 + (i % 2) * (tw + 0.1)
        y = 0.55 + (1 - i // 2) * (th + 0.1) - 0.05
        s.box(x, y, tw, th - 0.05, '', fill=GOLD if i == 0 else PAPER, lw=1.8, r=0.08)
        s.icon('speech', x + 0.42, y + th - 0.45, 0.5)
        s.text(x + 0.8, y + th - 0.38, org, size=17, weight='bold', ha='left')
        s.text(x + tw - 0.15, y + th - 0.38, where, size=14, color=RED, ha='right', weight='bold')
        _wrap(s, x + 0.2, y + (th - 0.75) / 2 + 0.05, tw - 0.4, tx, 15, ha='left', color=BODY)
    _source(s, 'Sources: Sunbird, Masakhane, Lelapa papers (arXiv); Capacity, Nov 2024.', y=0.2)
    return s


# ------------------------------------------------------------------ summarise: saves reading, can drop the sentence that matters (illustration)
@fig('x_l04_summary')
def x_l04_summary(w, h, **_):
    s = Scene(w, h)
    s.text(1.65, h - 0.3, 'A 12-page supply contract', size=16, weight='bold')
    s.box(0.2, 0.75, 2.9, h - 1.25, '', fill=PAPER, lw=1.8, r=0.06)
    for k in range(9):
        y = h - 0.85 - k * 0.36
        if k == 5:
            s.text(0.4, y, 'Except deliveries to Gulu', size=15, color=RED, weight='bold', ha='left')
        else:
            s.line(0.4, y, 2.9 - (0.4 if k % 3 == 2 else 0.0), y, color=GREY, lw=2.4, z=4)
    s.arrow(3.25, h / 2 + 0.2, 4.0, h / 2 + 0.2, lw=2.6, head=16)
    s.icon('robot', 3.62, h / 2 + 0.7, 0.5)
    s.text(5.75, h - 0.3, 'The summary', size=16, weight='bold')
    s.box(4.15, h - 2.25, 3.45, 1.65, '', fill=GOLD, lw=1.8, r=0.06)
    lines = ['Delivery within 5 days', 'Price fixed for 12 months', 'Either side may end it with notice']
    for k, ln in enumerate(lines):
        s.text(4.3, h - 0.9 - k * 0.42, ln, size=14, ha='left')
    s.icon('cross', 4.45, h - 2.75, 0.4)
    _wrap(s, 4.75, h - 2.75, 2.8, 'The Gulu exception is gone', 15, weight='bold', color=RED, ha='left')
    _wrap(s, 5.85, 1.15, 3.4, 'Check what a summary drops: the exception, the number, the deadline.', 15, color=BODY)
    s.text(w - 0.1, 0.2, 'Illustration', size=14, color=MUTE, ha='right')
    return s


# ------------------------------------------------------------------ good at, bad at (generic; reused by Session 5)
@fig('x_l04_goodbad')
def x_l04_goodbad(w, h, good=(), bad=(), heads=('Good at', 'Bad at'), **_):
    s = Scene(w, h)
    cw = (w - 0.3) / 2
    n = max(len(good), len(bad))
    step = min(0.98, (h - 0.95) / max(n, 1))
    for i, (hd, ic, items) in enumerate(((heads[0], 'check', good), (heads[1], 'cross', bad))):
        x = 0.1 + i * (cw + 0.1)
        s.text(x + 0.1, h - 0.35, hd, size=20, weight='bold', ha='left', color=RED if i else INK)
        s.line(x, h - 0.65, x + cw, h - 0.65, lw=1.8)
        for k, it in enumerate(items):
            y = h - 0.65 - step * (k + 0.5)
            s.icon(ic, x + 0.35, y, 0.55)
            _wrap(s, x + 0.8, y, cw - 0.95, it, 16, ha='left', color=BODY)
    return s


# ------------------------------------------------------------------ industry tour: six industries (generic; reused by Session 5)
@fig('x_l04_six')
def x_l04_six(w, h, tiles=(), source='', **_):
    s = Scene(w, h)
    gap = 0.12
    tw = (w - 0.2 - 2 * gap) / 3
    th = (h - 0.5 - gap) / 2
    for i, t in enumerate(tiles):
        ic, ind, use, ex = t['icon'], t['industry'], t['use'], t['example']
        x = 0.1 + (i % 3) * (tw + gap)
        y = 0.45 + (1 - i // 3) * (th + gap)
        s.box(x, y, tw, th, '', fill=PAPER, lw=1.8, r=0.08)
        s.icon(ic, x + 0.5, y + th - 0.55, 0.75)
        tx = x + 1.0
        iw = tw - 1.15
        top = y + th - 0.15
        hh = _wrap(s, tx, top, iw, ind, 16, weight='bold', ha='left', va='top')
        top -= hh + 0.1
        avail = top - (y + 0.12) - _nlines(ex, 15, iw, 'bold') * _lh(15) - 0.08
        us = _fit(use, iw, avail, 15, 14)
        uh = _wrap(s, tx, top, iw, use, us, ha='left', va='top', color=BODY)
        top -= uh + 0.08
        _wrap(s, tx, top, iw, ex, 15, weight='bold', ha='left', va='top', color=RED)
    _source(s, source, y=0.16)
    return s


# ------------------------------------------------------------------ demonstration: the flood question, meaning against words (recorded)
@fig('x_l04_flood')
def x_l04_flood(w, h, **_):
    s = Scene(w, h)
    q = _query('Q1')
    s.box(0.1, h - 1.0, w - 0.2, 0.8, '', fill=PAPER, lw=1.8, r=0.08)
    s.icon('person', 0.5, h - 0.6, 0.5)
    _wrap(s, 0.9, h - 0.6, w - 1.2, '“' + q['query'] + '”', 17, ha='left', weight='bold')
    cw = (w - 0.5) / 2
    # meaning search
    x = 0.1
    s.text(x + 0.05, h - 1.4, 'Search by meaning', size=18, weight='bold', ha='left')
    s.line(x, h - 1.65, x + cw, h - 1.65, lw=1.6)
    top = q['top3'][0]['cosine']
    for k, t in enumerate(q['top3']):
        y = h - 2.1 - k * 0.55
        s.text(x + 0.2, y, str(k + 1), size=17, weight='bold', color=RED if k == 0 else INK)
        s.text(x + 0.5, y, t['head'], size=16, ha='left', weight='bold' if k == 0 else 'normal')
        bw = 1.6 * t['cosine'] / top
        s.rect(x + 3.4, y - 0.13, bw, 0.26, fill=GOLD if k == 0 else PALE, edge=INK, lw=1.2)
        if k == 0:
            s.icon('check', x + 3.4 + bw + 0.3, y, 0.36)
    s.text(x + 3.4, h - 3.65, 'longer bar: closer in meaning', size=14, color=MUTE, ha='left')
    # word search
    x = 0.4 + cw
    s.text(x + 0.05, h - 1.4, 'Word search', size=18, weight='bold', ha='left')
    s.line(x, h - 1.65, x + cw, h - 1.65, lw=1.6)
    s.icon('cross', x + 0.45, h - 2.45, 0.7)
    _wrap(s, x + 0.95, h - 2.45, cw - 1.1, 'No passage shares a word with the question, so it finds nothing.', 17, ha='left', weight='bold', color=RED)
    _wrap(s, x + 0.95, h - 3.35, cw - 1.1, 'The clause says “events beyond its reasonable control, including flood”.', 15, ha='left', color=BODY)
    s.text(0.1, 0.18, 'Recorded run: sentence-transformers, model all-MiniLM-L6-v2, 6 November 2026; same numbers in five runs. Ten invented clauses.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ demonstration: two more wins and one slip (recorded)
@fig('x_l04_three')
def x_l04_three(w, h, **_):
    s = Scene(w, h)
    cases = [('Q11', 'HR policy'), ('Q9', 'HR policy'), ('Q7', 'Finance terms')]
    right = {'Q11': 'Sick leave', 'Q9': 'Whistleblowing', 'Q7': 'Bank reconciliation'}
    gap = 0.25
    cw = (w - 0.2 - 2 * gap) / 3
    for i, (qid, skin) in enumerate(cases):
        q = _query(qid)
        x = 0.1 + i * (cw + gap)
        slip = q['want_rank'] != 1
        s.box(x, 0.55, cw, h - 0.65, '', fill=PAPER, edge=RED if slip else INK, lw=2.2 if slip else 1.8, r=0.08)
        s.text(x + 0.15, h - 0.35, skin, size=15, weight='bold', color=MUTE, ha='left')
        qh = _wrap(s, x + 0.15, h - 0.6, cw - 0.3, '“' + q['query'] + '”', 15, ha='left', va='top', weight='bold')
        y = h - 0.75 - qh - 0.25
        s.text(x + 0.15, y, 'By meaning, first:', size=14, color=BODY, ha='left')
        y -= 0.38
        s.icon('cross' if slip else 'check', x + 0.32, y, 0.36)
        _wrap(s, x + 0.6, y, cw - 0.75, q['top3'][0]['head'], 15, ha='left', weight='bold')
        y -= 0.42
        if slip:
            _wrap(s, x + 0.6, y, cw - 0.75, f'{right[qid]} came {["", "first", "second", "third", "fourth"][q["want_rank"]]}', 15, ha='left', color=RED)
            y -= 0.42
        s.text(x + 0.15, y - 0.08, 'Word search, first:', size=14, color=BODY, ha='left')
        kw = q['keyword_top'][0]['head'] if q['keyword_top'] else 'no shared word'
        kok = bool(q.get('keyword_hit_at1'))
        s.icon('check' if kok else 'cross', x + 0.32, y - 0.5, 0.36)
        _wrap(s, x + 0.6, y - 0.5, cw - 0.75, kw, 15, ha='left', color=BODY)
    s.text(0.1, 0.22, 'Recorded run, 6 November 2026; invented passages for Nile Valley Foods (fictional).', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ demonstration: the tally over twelve questions (recorded)
@fig('x_l04_tally')
def x_l04_tally(w, h, **_):
    s = Scene(w, h)
    qs = _all_queries()
    sm = _res()['summary']
    n = len(qs)
    cell = (w - 2.2) / n
    rows = [('By meaning', [q['want_rank'] for q in qs]), ('By words', [1 if q.get('keyword_hit_at1') else 9 for q in qs])]
    s.text(0.1, h - 0.3, f'{n} plain questions, one square each', size=15, color=BODY, ha='left')
    for r, (lab, ranks) in enumerate(rows):
        y = h - 1.15 - r * 1.25
        s.text(0.1, y, lab, size=16, weight='bold', ha='left')
        for k, rk in enumerate(ranks):
            x = 1.9 + k * cell
            fill = GOLD if rk == 1 else (PALE if rk <= 3 else PAPER)
            edge = RED if rk > 3 and r == 0 else INK
            s.rect(x, y - 0.3, cell - 0.08, 0.6, fill=fill, edge=edge, lw=2.2 if edge == RED else 1.2)
        tx = (f'first in {sm["emb_hit1"]}, in the top three in {sm["emb_hit3"]}' if r == 0 else f'first in {sm["kw_hit1"]}')
        s.text(1.9, y - 0.58, tx, size=15, weight='bold', color=RED if r == 0 else INK, ha='left')
    ly = 0.95
    for k, (fill, lab) in enumerate(((GOLD, 'right answer first'), (PALE, 'second or third'), (PAPER, 'not in the top three'))):
        x = 0.1 + k * 2.55
        s.rect(x, ly - 0.13, 0.3, 0.26, fill=fill, edge=RED if k == 2 else INK, lw=2.0 if k == 2 else 1.2)
        s.text(x + 0.42, ly, lab, size=14, ha='left')
    s.text(0.1, 0.3, 'Recorded run, 6 Nov 2026. 30 short invented passages: a demonstration only.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ your people: roles, tasks, skills, fears (generic; reused by Session 5)
@fig('x_l04_people')
def x_l04_people(w, h, roles=(), labels=('Less of', 'More of', 'Skill to grow', 'Fears and gains'), **_):
    s = Scene(w, h)
    lab_w = 1.45
    cw = (w - 0.1 - lab_w) / len(roles)
    top = h - 0.85
    rh = (top - 0.1) / len(labels)
    for i, r in enumerate(roles):
        role, cells = r['role'], r['cells']
        x = 0.1 + lab_w + i * cw
        s.icon('person', x + 0.45, h - 0.42, 0.62, accent=GOLD)
        s.text(x + 0.85, h - 0.42, role, size=18, weight='bold', ha='left')
        for k, txt in enumerate(cells):
            y = top - k * rh
            s.rect(x + 0.05, y - rh + 0.05, cw - 0.1, rh - 0.08, fill=PALE if k == len(labels) - 1 else PAPER, edge=HAIR, lw=1.0, z=1)
            sz = _fit(txt, cw - 0.4, rh - 0.18, 15, 14)
            _wrap(s, x + 0.2, y - rh / 2 + 0.02, cw - 0.4, txt, sz, ha='left', color=BODY)
    for k, lab in enumerate(labels):
        y = top - k * rh - rh / 2
        _wrap(s, 0.1, y, lab_w - 0.1, lab, 15, weight='bold', ha='left', color=RED if k == len(labels) - 1 else INK)
    return s


# ------------------------------------------------------------------ always a door to a person (TEL-04)
@fig('x_l04_route')
def x_l04_route(w, h, **_):
    s = Scene(w, h)
    s.icon('speech', 0.45, h - 0.6, 0.6)
    s.text(0.85, h - 0.6, 'A customer writes', size=16, weight='bold', ha='left')
    s.arrow(1.0, h - 1.0, 1.0, h - 1.4, lw=2.2, head=13)
    s.box(0.1, h - 2.05, 4.3, 0.62, '', fill=PAPER, lw=1.8, r=0.08)
    s.icon('robot', 0.45, h - 1.74, 0.45)
    s.text(0.85, h - 1.74, 'AI sorts it and answers the routine', size=15, ha='left')
    s.arrow(1.0, h - 2.1, 1.0, h - 2.5, lw=2.2, head=13)
    s.arrow(3.0, h - 2.1, 3.0, h - 2.5, lw=2.2, head=13)
    s.box(0.1, h - 3.25, 1.95, 0.72, '', fill=PAPER, lw=1.6, r=0.08)
    _wrap(s, 1.075, h - 2.89, 1.75, 'Routine: answered', 15)
    s.box(2.2, h - 3.25, 2.2, 0.72, '', fill=GOLD, lw=2.0, r=0.08)
    _wrap(s, 3.3, h - 2.89, 2.0, 'Urgent or unhappy: a person', 15, weight='bold')
    s.box(0.1, 0.55, 4.3, 0.85, '', fill=PALE, lw=1.2, r=0.08)
    _wrap(s, 2.25, 0.975, 4.0, 'And any customer can ask for a person at any time.', 15, weight='bold')
    x = 4.6
    s.box(x, 0.55, w - x - 0.1, h - 0.65, '', fill=PAPER, edge=RED, lw=2.2, r=0.08)
    s.text(x + 0.15, h - 0.4, 'Kenya, April 2026', size=16, weight='bold', color=RED, ha='left')
    hh = _wrap(s, x + 0.15, h - 0.65, w - x - 0.4, 'A petition in the High Court says Safaricom customers are trapped in loops with the Zuri chatbot, with no easy route to a human.', 15, ha='left', va='top', color=BODY)
    _wrap(s, x + 0.15, h - 0.85 - hh, w - x - 0.4, 'No ruling yet. These are claims.', 15, weight='bold', ha='left', va='top', color=RED)
    s.text(x + 0.15, 1.05, 'Source: HapaKenya,', size=14, color=MUTE, ha='left')
    s.text(x + 0.15, 0.8, '24 April 2026', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ hands-on: one portfolio entry (generic; reused by Session 5)
@fig('x_l04_portfolio')
def x_l04_portfolio(w, h, title='', rows=(), **_):
    s = Scene(w, h)
    s.text(0.05, h - 0.2, title, size=15, weight='bold', ha='left')
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
