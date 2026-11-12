"""Figures for Leadership Edition Session 8, Making AI know your business: assistants on your own documents.  Names: x_l08_*  (content kind 'l08_*').

No maths anywhere: pictures, counts and percentages only.  Recorded numbers are read from demo_runs/s09/ (retrieval_results.json,
chunking_results.json, lora_output.txt; 6 November 2026) and the scoring in demo_runs/s10_scoring.md (Claude, fresh sessions, 4 and 6 November 2026).
The staff handbook and its company are FICTIONAL (Nile Valley Foods Ltd).  Case figures come from research/*.md (IDs in the content file).
Anything marked 'illustrative' is invented to teach the idea and is labelled so on the slide.
Generic helpers here (six-tile tour, role grid, portfolio entry) are also used by diagrams_l09.py.
"""
import json
from pathlib import Path

from figkit import Scene, INK, BODY, MUTE, HAIR, PALE, PAPER, RED, GOLD, fig
import slidekit as K
from diagrams_l02 import _wrap, _fit, _lh, _source

RUN = Path(__file__).resolve().parent.parent / 'demo_runs' / 's09'
_C = {}


def _json(name):
    if name not in _C:
        _C[name] = json.load(open(RUN / name))
    return _C[name]


def _h(text, size, w, weight='normal'):
    return len(K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', w)) * _lh(size)


# ================================================================== generic helpers (also used by Session 9)
def six_tiles(w, h, tiles, source=''):
    """Six industries: tiles = [(icon, industry, use, example)]."""
    s = Scene(w, h)
    gap = 0.12
    tw = (w - 0.2 - 2 * gap) / 3
    th = (h - 0.5 - gap) / 2
    for i, (ic, ind, use, ex) in enumerate(tiles):
        x = 0.1 + (i % 3) * (tw + gap)
        y = 0.45 + (1 - i // 3) * (th + gap)
        s.box(x, y, tw, th, '', fill=PAPER, lw=1.8, r=0.08)
        s.icon(ic, x + 0.5, y + th - 0.55, 0.75)
        tx, iw, top = x + 1.0, tw - 1.15, y + th - 0.15
        for hs, bs in ((16, 15), (15, 14), (14, 14)):
            need = _h(ind, hs, iw, 'bold') + _h(use, bs, iw) + _h(ex, bs, iw, 'bold') + 0.14
            if need <= th - 0.25:
                break
        top -= _wrap(s, tx, top, iw, ind, hs, weight='bold', ha='left', va='top') + 0.08
        top -= _wrap(s, tx, top, iw, use, bs, ha='left', va='top', color=BODY) + 0.06
        _wrap(s, tx, top, iw, ex, bs, weight='bold', ha='left', va='top', color=RED)
    if source:
        _source(s, source, y=0.16)
    return s


def role_grid(w, h, roles, labels=('Less of', 'More of', 'Skill to grow', 'Fears and gains'), lab_w=1.45, foot=''):
    """Roles across, rows of change down. roles = [(name, [cell per label])]."""
    s = Scene(w, h)
    cw = (w - 0.1 - lab_w) / len(roles)
    bottom = 0.5 if foot else 0.1
    top = h - 0.85
    rh = (top - bottom) / len(labels)
    for i, (role, cells) in enumerate(roles):
        x = 0.1 + lab_w + i * cw
        s.icon('person', x + 0.45, h - 0.42, 0.62, accent=GOLD)
        _wrap(s, x + 0.85, h - 0.42, cw - 0.95, role, 17, weight='bold', ha='left')
        for r, txt in enumerate(cells):
            y = top - r * rh
            s.rect(x + 0.05, y - rh + 0.05, cw - 0.1, rh - 0.08, fill=PALE if r == len(labels) - 1 else PAPER, edge=HAIR, lw=1.0, z=1)
            _wrap(s, x + 0.2, y - rh / 2 + 0.02, cw - 0.4, txt, _fit(txt, cw - 0.4, rh - 0.12, 15, 14), ha='left', color=BODY)
    for r, lab in enumerate(labels):
        _wrap(s, 0.1, top - r * rh - rh / 2, lab_w - 0.1, lab, 15, weight='bold', ha='left', color=RED if r == len(labels) - 1 else INK)
    if foot:
        s.text(0.1, 0.2, foot, size=14, color=MUTE, ha='left')
    return s


def portfolio_entry(w, h, title, rows, size=14):
    """One AI Opportunity Portfolio entry; the last row is today's column (gold)."""
    s = Scene(w, h)
    s.text(0.05, h - 0.2, title, size=15, weight='bold', ha='left')
    lw_ = 1.85
    vw = w - 0.1 - lw_
    hs = [max(_h(a, size, lw_ - 0.15, 'bold'), _h(b, size, vw - 0.15)) + 0.1 for a, b in rows]
    y = h - 0.42
    for i, ((a, b), rh) in enumerate(zip(rows, hs)):
        last = i == len(rows) - 1
        s.rect(0.05, y - rh, lw_, rh, fill=GOLD if last else PALE, edge=INK, lw=1.0)
        s.rect(0.05 + lw_, y - rh, vw, rh, fill=PAPER, edge=INK, lw=1.0)
        _wrap(s, 0.12, y - rh / 2, lw_ - 0.15, a, size, weight='bold', ha='left')
        _wrap(s, 0.12 + lw_, y - rh / 2, vw - 0.15, b, size, ha='left', color=BODY)
        y -= rh
    return s


def good_bad(w, h, good, bad):
    s = Scene(w, h)
    cw = (w - 0.3) / 2
    for i, (hd, ic, items) in enumerate((('Good at', 'check', good), ('Bad at', 'cross', bad))):
        x = 0.1 + i * (cw + 0.1)
        s.text(x + 0.1, h - 0.35, hd, size=20, weight='bold', ha='left', color=RED if i else INK)
        s.line(x, h - 0.65, x + cw, h - 0.65, lw=1.8)
        step = (h - 0.9) / len(items)
        for k, it in enumerate(items):
            y = h - 0.65 - step * (k + 0.5)
            s.icon(ic, x + 0.35, y, 0.58)
            _wrap(s, x + 0.8, y, cw - 0.95, it, 16, ha='left', color=BODY)
    return s


# ================================================================== recall: a good brief, now with your own pages
@fig('x_l08_bridge')
def x_l08_bridge(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.3, 'Session 7: a good brief', size=18, weight='bold', ha='left')
    s.line(0.1, h - 0.55, 3.55, h - 0.55, lw=1.6)
    parts = [('person', 'Role'), ('folder', 'Context'), ('doc', 'Examples'), ('grid', 'Format'), ('lock', 'Limits')]
    for i, (ic, t) in enumerate(parts):
        y = h - 0.95 - i * 0.56
        s.icon(ic, 0.4, y, 0.45)
        s.text(0.8, y, t, size=16, ha='left')
    s.arrow(3.65, h - 2.05, 4.15, h - 2.05, lw=2.4, head=16)
    x0 = 4.3
    s.text(x0, h - 0.3, 'Today: brief plus your pages', size=17, weight='bold', ha='left', color=RED)
    s.line(x0, h - 0.55, w - 0.1, h - 0.55, lw=1.6)
    s.box(x0, h - 3.45, 1.45, 2.65, '', fill=PAPER, lw=1.8, r=0.06)
    s.text(x0 + 0.72, h - 1.05, 'The brief', size=15, weight='bold')
    for k in range(4):
        s.line(x0 + 0.2, h - 1.45 - k * 0.42, x0 + 1.25, h - 1.45 - k * 0.42, color=HAIR, lw=2)
    px = x0 + 1.75
    for k in range(3):
        s.rect(px + k * 0.12, h - 3.45 + 0.3 - k * 0.1, 1.3, 2.2, fill=GOLD if k == 2 else PAPER, edge=INK, lw=1.4, z=2 + k)
    _wrap(s, px + 0.24 + 0.65, h - 2.15, 1.1, 'Handbook clause 3.2', 15, weight='bold')
    s.text(x0 + 1.6, h - 2.05, '+', size=26, weight='bold')
    _wrap(s, w / 2, 0.75, w - 0.4, 'A good brief cannot supply facts the assistant has never seen.', 17, weight='bold', color=RED)
    _wrap(s, w / 2, 0.25, w - 0.4, 'Today: give it the right pages, and make it show them.', 15, color=BODY)
    return s


# ================================================================== what a general assistant knows, and what it has never seen
@fig('x_l08_knows')
def x_l08_knows(w, h, **_):
    s = Scene(w, h)
    cw = (w - 0.3) / 2
    cols = [('What it learned in training', PAPER, INK, [('book', 'Public books and web pages'), ('calendar', 'Up to a cut-off date'), ('people', 'General knowledge of the world')]),
            ('What it has never seen', GOLD, RED, [('lock', 'Your staff handbook'), ('tag', 'This month’s price list'), ('folder', 'Your contracts and files')])]
    for i, (hd, fill, col, rows) in enumerate(cols):
        x = 0.1 + i * (cw + 0.1)
        s.box(x, 1.25, cw, h - 1.35, '', fill=fill, lw=2, r=0.08)
        s.text(x + cw / 2, h - 0.42, hd, size=17, weight='bold', color=col if i else INK)
        for k, (ic, t) in enumerate(rows):
            y = h - 1.15 - k * 0.78
            s.icon(ic, x + 0.45, y, 0.55)
            _wrap(s, x + 0.85, y, cw - 1.0, t, 16, ha='left')
    _wrap(s, w / 2, 0.85, w - 0.3, 'Recorded: asked ten handbook questions with no handbook, both runs answered “not stated” to all ten.', 15, color=BODY)
    s.text(w / 2, 0.3, 'Claude, two fresh sessions, 6 November 2026. The handbook is fictional.', size=14, color=MUTE)
    return s


# ================================================================== the open-book exam: find, answer, show
@fig('x_l08_openbook')
def x_l08_openbook(w, h, **_):
    s = Scene(w, h)
    cw = (w - 0.2 - 2 * 0.5) / 3
    steps = [('1  Find the right pages', 'Search the documents by meaning, as in Session 4, and keep the closest few.', 'retrieval'),
             ('2  Answer only from them', 'The assistant reads those pages with the question and writes the answer.', 'generation'),
             ('3  Show the source', 'It names the page or clause, so a person can open it and check.', 'citation')]
    top, bot = h - 0.1, 0.95
    for i, (hd, tx, term) in enumerate(steps):
        x = 0.1 + i * (cw + 0.5)
        s.box(x, bot, cw, top - bot, '', fill=GOLD if i == 2 else PAPER, lw=2, r=0.08)
        s.text(x + 0.2, top - 0.35, hd, size=18, weight='bold', ha='left')
        cy = top - 1.25
        if i == 0:
            for k in range(5):
                s.rect(x + 0.35 + k * 0.42, cy - 0.4, 0.34, 0.8, fill=GOLD if k in (1, 3) else PAPER, edge=INK, lw=1.4, z=2)
            s.icon('magnifier', x + cw - 0.6, cy, 0.7)
        elif i == 1:
            s.icon('robot', x + 0.7, cy, 0.8)
            s.rect(x + 1.35, cy - 0.4, 0.34, 0.8, fill=GOLD, edge=INK, lw=1.4)
            s.rect(x + 1.8, cy - 0.4, 0.34, 0.8, fill=GOLD, edge=INK, lw=1.4)
            s.arrow(x + 2.3, cy, x + 2.8, cy, lw=2, head=13)
            s.icon('speech', x + 3.15, cy, 0.6)
        else:
            s.box(x + 0.3, cy - 0.35, cw - 0.6, 0.7, 'The Finance Manager  [3.2]', size=16, weight='bold', fill=PAPER, r=0.08)
        _wrap(s, x + 0.2, top - 1.85, cw - 0.4, tx, 15, ha='left', va='top', color=BODY)
        s.text(x + cw / 2, bot + 0.22, 'Industry word: ' + term, size=14, color=MUTE)
        if i < 2:
            s.arrow(x + cw + 0.05, (top + bot) / 2, x + cw + 0.45, (top + bot) / 2, lw=2.4, head=16)
    _wrap(s, w / 2, 0.45, w - 0.4, 'All three together: retrieval-augmented generation, or RAG', 18, weight='bold', color=RED)
    return s


# ================================================================== step one: rank every page against the question (recorded)
GIST = {'3.2': 'Approval limits for one expense claim', '3.1': 'Receipts reach Finance within 14 days', '3.5': 'Approved claims are paid with salary',
        '3.6': 'A claim without a receipt', '3.3': 'Meal allowance and hotel limit'}


@fig('x_l08_find')
def x_l08_find(w, h, **_):
    d = _json('retrieval_results.json')
    text = {c['id']: c['text'] for c in d['chunks']}
    r = [x for x in d['results'] if x['id'] == 'Q03'][0]
    s = Scene(w, h)
    s.box(0.1, h - 0.85, w - 0.2, 0.7, '', fill=PAPER, lw=2, r=0.08)
    s.icon('question', 0.45, h - 0.5, 0.45)
    s.text(0.8, h - 0.5, 'Who must approve an expense claim of UGX 1,500,000?', size=16, weight='bold', ha='left')
    s.text(0.1, h - 1.15, 'Handbook clauses, closest in meaning first', size=15, color=BODY, ha='left')
    rows = r['top5']
    rh = (h - 2.0) / len(rows)
    for i, row in enumerate(rows):
        y = h - 1.45 - (i + 0.5) * rh
        sent = i < 3
        s.box(0.1, y - rh / 2 + 0.05, 0.75, rh - 0.1, row['clause'], size=16, weight='bold', fill=GOLD if sent else PAPER, r=0.06)
        t = GIST.get(row['clause'], text[row['clause']][:40])
        _wrap(s, 1.0, y, 4.3, t, 15, ha='left', color=BODY)
        bw = 1.9 * row['score'] / rows[0]['score']
        s.rect(5.45, y - 0.12, bw, 0.24, fill=GOLD if sent else PAPER, edge=INK, lw=1.2)
    s.text(0.1, 0.18, 'Gold: the three sent to the assistant. Clauses summarised. Recorded run, 6 Nov 2026.', size=14, color=MUTE, ha='left')
    return s


# ================================================================== step two: answer only from those pages (recorded)
@fig('x_l08_answer')
def x_l08_answer(w, h, **_):
    s = Scene(w, h)
    lw_ = 3.4
    s.text(0.1, h - 0.3, 'The pages it was given', size=16, weight='bold', ha='left')
    pages = [('3.2', 'Up to UGX 200,000: the line manager. UGX 200,001 to 2,000,000: the Finance Manager. Above: the Managing Director.'),
             ('3.1', 'Receipts must reach the Finance office within 14 days.'),
             ('3.5', 'Approved claims are paid with the monthly salary.')]
    y = h - 0.6
    for i, (cid, t) in enumerate(pages):
        hh = _h(t, 14, lw_ - 0.75) + 0.2
        s.box(0.1, y - hh, lw_, hh, '', fill=GOLD if i == 0 else PAPER, lw=1.6, r=0.06)
        s.text(0.22, y - 0.2, cid, size=15, weight='bold', ha='left', va='top')
        _wrap(s, 0.7, y - hh / 2, lw_ - 0.75, t, 14, ha='left', color=INK if i == 0 else BODY)
        y -= hh + 0.12
    s.arrow(lw_ + 0.15, h / 2 + 0.3, lw_ + 0.6, h / 2 + 0.3, lw=2.4, head=16)
    x = lw_ + 0.75
    bw = w - x - 0.1
    s.text(x, h - 0.3, 'The recorded answer', size=16, weight='bold', ha='left', color=RED)
    ans = 'The Finance Manager. A claim of UGX 1,500,000 falls in the band UGX 200,001 to UGX 2,000,000. [3.2]'
    ah = _h(ans, 16, bw - 0.35) + 0.4
    s.box(x, h - 0.6 - ah, bw, ah, '', fill=PAPER, edge=RED, lw=2.2, r=0.08)
    _wrap(s, x + 0.18, h - 0.6 - ah / 2, bw - 0.35, ans, 16, ha='left')
    rule = 'The instruction: answer only from these pages, name the clause, and if they do not say, write “not stated”.'
    _wrap(s, x, h - 1.0 - ah, bw, rule, 15, ha='left', va='top', color=BODY)
    s.text(0.1, 0.18, 'Claude, fresh session, 6 Nov 2026; both runs the same. Clauses shortened.', size=14, color=MUTE, ha='left')
    return s


# ================================================================== messy documents give messy answers
@fig('x_l08_messy')
def x_l08_messy(w, h, **_):
    s = Scene(w, h)
    tiles = [('doc', 'Two versions disagree', 'Version 3 says 2 days of notice, Version 4 says 14. Which one did it find?'),
             ('calendar', 'Out of date', 'Last year’s price list still sits in the folder.'),
             ('receipt', 'Unreadable', 'A photocopied scan, or a table the machine cannot follow.'),
             ('question', 'Never written down', 'The rule lives in one manager’s head, so no page holds it.')]
    tw, th = (w - 0.3) / 2, (h - 0.6) / 2
    for i, (ic, hd, tx) in enumerate(tiles):
        x = 0.1 + (i % 2) * (tw + 0.1)
        y = 0.5 + (1 - i // 2) * (th + 0.1) - 0.05
        s.box(x, y, tw, th - 0.05, '', fill=PAPER, lw=1.8, r=0.08)
        s.icon(ic, x + 0.5, y + th - 0.55, 0.7)
        s.text(x + 1.0, y + th - 0.55, hd, size=17, weight='bold', ha='left')
        _wrap(s, x + 0.25, y + (th - 1.0) / 2 + 0.02, tw - 0.45, tx, 15, ha='left', color=BODY)
    s.text(w / 2, 0.22, 'Illustrative problems. The assistant answers from whatever it finds.', size=14, color=MUTE)
    return s


# ================================================================== where you cut the pages decides what can be found (recorded)
@fig('x_l08_cutting')
def x_l08_cutting(w, h, **_):
    d = _json('chunking_results.json')
    order = [('clause', 'At each numbered clause'), ('fixed150', 'Every 150 characters, about 25 words'), ('fixed300', 'Every 300 characters, about 50 words')]
    keys = list(d.keys())
    s = Scene(w, h)
    s.text(0.1, h - 0.3, 'The same handbook, cut three ways', size=16, weight='bold', ha='left')
    s.text(w - 0.1, h - 0.3, 'Answer in the top piece', size=16, weight='bold', ha='right')
    s.line(0.1, h - 0.55, w - 0.1, h - 0.55, lw=1.6)
    rh = (h - 1.15) / 3
    for i, (k, label) in enumerate(order):
        key = k if k in d else keys[i]
        r = d[key]
        y = h - 0.6 - (i + 0.5) * rh
        _wrap(s, 0.1, y + 0.32, 3.4, label, 15, weight='bold', ha='left')
        s.text(0.1, y - 0.12, f'{r["n_chunks"]} pieces', size=15, color=BODY, ha='left')
        # strip of pieces
        n = 10 if r['n_chunks'] == 30 else 5
        pw = 2.6 / n
        for j in range(n):
            bad = r['answered_by_top_chunk'] < r['of'] and j == 4
            s.rect(3.55 + j * pw, y - 0.25, pw - 0.04, 0.5, fill=PALE if not bad else PAPER, edge=RED if bad else INK, lw=2 if bad else 1)
        ok = r['answered_by_top_chunk'] == r['of']
        s.text(w - 0.1, y, f'{r["answered_by_top_chunk"]} of {r["of"]}', size=24, weight='bold', ha='right', color=INK if ok else RED)
    _wrap(s, 0.1, 0.3, w - 0.2, 'Cut mid-clause, the answer to 3 questions landed in the next piece. Recorded run, 6 Nov 2026, eight answerable questions.', 14, ha='left', color=MUTE)
    return s


# ================================================================== short documents can be pasted whole
@fig('x_l08_paste')
def x_l08_paste(w, h, **_):
    s = Scene(w, h)
    cw = (w - 0.3) / 2
    cols = [('The staff handbook', '829 words, about 3 pages', 'Fits in one go: paste it all.', 'Recorded: pasted whole, 10 of 10 right in both runs.', 1, GOLD),
            ('A whole policy library', 'Thousands of pages', 'Does not fit, and each question would send it all again.', 'Find the right pages first, as in step one.', 12, PAPER)]
    for i, (hd, sub, verdict, foot, n, fill) in enumerate(cols):
        x = 0.1 + i * (cw + 0.1)
        s.box(x, 0.55, cw, h - 0.65, '', fill=fill, lw=2, r=0.08)
        s.text(x + 0.2, h - 0.4, hd, size=17, weight='bold', ha='left')
        s.text(x + 0.2, h - 0.75, sub, size=15, color=BODY, ha='left')
        cx, cy = x + cw / 2, h - 1.75
        if n == 1:
            s.icon('book', cx, cy, 1.1)
        else:
            for k in range(n):
                s.rect(x + 0.35 + (k % 6) * 0.5, cy - 0.15 - (k // 6) * 0.55, 0.38, 0.48, fill=PAPER, edge=INK, lw=1.2)
        _wrap(s, x + 0.2, 1.95, cw - 0.4, verdict, 16, weight='bold', ha='left', va='top', color=INK if i == 0 else RED)
        _wrap(s, x + 0.2, 1.0, cw - 0.4, foot, 15, ha='left', color=BODY)
    s.text(w / 2, 0.22, 'How much text fits at once: the context window', size=15, weight='bold', color=MUTE)
    return s


# ================================================================== customising teaches style, not facts (recorded)
@fig('x_l08_style')
def x_l08_style(w, h, **_):
    s = Scene(w, h)
    lw_ = 3.3
    s.text(0.1, h - 0.3, 'A new customer message', size=16, weight='bold', ha='left')
    s.box(0.1, h - 1.35, lw_, 0.8, '', fill=PAPER, lw=1.8, r=0.08)
    s.icon('speech', 0.45, h - 0.95, 0.42)
    _wrap(s, 0.8, h - 0.95, lw_ - 0.8, 'when will my cooking oil arrive', 15, ha='left', italic=True)
    boxes = [('House sign-off', 'before: 0 of 6 replies; after: 6 of 6', GOLD, INK), ('The facts', 'still invented after customising', PAPER, RED)]
    for i, (hd, tx, fill, ec) in enumerate(boxes):
        x = 0.1 + i * (lw_ / 2 + 0.05)
        bw = lw_ / 2 - 0.05
        s.box(x, 0.75, bw, 1.75, '', fill=fill, lw=1.8, edge=ec, r=0.08)
        _wrap(s, x + bw / 2, 2.15, bw - 0.2, hd, 16, weight='bold', color=ec)
        _wrap(s, x + bw / 2, 1.35, bw - 0.2, tx, 15, color=BODY)
    x0 = lw_ + 0.4
    cw = (w - x0 - 0.2) / 2
    tops = h - 0.6
    for i, hd in enumerate(('Before customising', 'After customising')):
        x = x0 + i * (cw + 0.1)
        s.text(x + 0.1, h - 0.3, hd, size=17, weight='bold', ha='left', color=RED if i else INK)
        s.box(x, 0.75, cw, tops - 0.75, '', fill=PAPER, lw=2, r=0.08)
        if i == 0:
            _wrap(s, x + 0.2, tops - 0.25, cw - 0.4, 'I have been cooking for a while now and I have been using this recipe for a while now ...', 16, ha='left', va='top', italic=True, color=BODY)
        else:
            y = tops - 0.25
            y -= _wrap(s, x + 0.2, y, cw - 0.4, 'Hello Ms Nye.', 16, ha='left', va='top') + 0.12
            y -= _wrap(s, x + 0.2, y, cw - 0.4, 'We will arrive on Monday.', 17, weight='bold', ha='left', va='top', color=RED) + 0.12
            s.rect(x + 0.12, y - 0.95, cw - 0.24, 1.0, fill=GOLD, edge=GOLD, lw=0.5, z=3)
            _wrap(s, x + 0.2, y - 0.03, cw - 0.4, 'Thank you for choosing Nile Valley Foods. Customer Care, Jinja.', 16, ha='left', va='top')
    _wrap(s, x0 + cw + 0.3, 0.92, cw - 0.4, 'Red: invented, no date was ever given. Gold: the sign-off it learned.', 14, ha='left', va='bottom', color=RED)
    s.text(0.1, 0.2, 'Recorded run, 6 Nov 2026: a small, old open model (GPT-2) customised with LoRA on 48 invented replies, 42 seconds on a laptop.', size=14, color=MUTE, ha='left')
    return s


# ================================================================== the climb: prompt, retrieve, customise
@fig('x_l08_climb')
def x_l08_climb(w, h, **_):
    s = Scene(w, h)
    steps = [('Prompt', 'A good brief, with short documents pasted in', 'Start here: short documents, few users.'),
             ('Retrieve', 'Find the right pages, then answer from them', 'Many documents, facts that change, sources needed.'),
             ('Customise', 'Train it further on your own examples', 'A fixed style or format at large volume. Never for facts.')]
    gap = 0.25
    cw = (w - 0.2 - 2 * gap) / 3
    for i, (hd, what, when) in enumerate(steps):
        x = 0.1 + i * (cw + gap)
        top = 3.05 + i * 0.55
        s.box(x, 0.1, cw, top - 0.1, '', fill=GOLD if i == 0 else PAPER, lw=2, edge=RED if i == 2 else INK, r=0.06)
        s.text(x + 0.15, top - 0.32, f'{i + 1}  {hd}', size=19, weight='bold', ha='left')
        yy = top - 0.65
        yy -= _wrap(s, x + 0.15, yy, cw - 0.3, what, 15, ha='left', va='top', color=BODY) + 0.2
        s.text(x + 0.15, yy, 'Use it when', size=14, weight='bold', ha='left', va='top', color=RED if i == 2 else INK)
        _wrap(s, x + 0.15, yy - 0.3, cw - 0.3, when, 15, ha='left', va='top')
        if i < 2:
            s.arrow(x + cw * 0.55, top + 0.12, x + cw + gap + 0.3, top + 0.6, lw=2, head=13, rad=-0.25)
    _wrap(s, 0.1, h - 0.4, 4.4, 'Climb a step only when the one below falls short', 17, weight='bold', ha='left', color=RED)
    return s


# ================================================================== good at, bad at
@fig('x_l08_good_bad')
def x_l08_good_bad(w, h, **_):
    return good_bad(w, h, ['Answering the same policy questions all day', 'Pointing to the page, so staff can check', 'Long, scattered documents nobody reads', 'Staying current when the pages change'],
                    ['Gaps and contradictions in the documents', 'Questions that need a judgement', 'Numbers buried in scans and tables', 'Answers with no page behind them'])


# ================================================================== industry tour
@fig('x_l08_six')
def x_l08_six(w, h, **_):
    tiles = [('calculator', 'Banking and microfinance', 'Staff ask the service desk bot, not a colleague', 'Standard Bank, South Africa'),
             ('phone', 'Telecom and mobile money', 'Frontline staff ask the company’s knowledge bases', 'Telstra, Australia'),
             ('plant', 'Agriculture and agribusiness', 'Farmers ask; answers come only from a vetted library', 'Farmer.Chat, Kenya'),
             ('bottle', 'Manufacturing and FMCG', 'Staff ask the handbook about leave and expenses', 'Nile Valley Foods (fictional), today’s demo'),
             ('clinic', 'Healthcare and insurance', 'Reads the visit’s own notes and flags possible errors', 'Penda Health, Kenya'),
             ('people', 'Public sector', 'Summaries of long judgments in Uganda’s free law library', 'ULII, Uganda')]
    return six_tiles(w, h, tiles, 'Sources: Microsoft 2024; Telstra 2024 and 2026; arXiv 2024; arXiv 2025; The Observer 2026. Company figures where stated.')


# ================================================================== demonstration: the ten questions and their key
@fig('x_l08_questions')
def x_l08_questions(w, h, **_):
    rows = [('Q01', 'Paid annual leave each year?', '21 working days', '2.1'),
            ('Q02', 'Notice for a leave request?', 'At least 14 days', '2.2'),
            ('Q03', 'Who approves a UGX 1,500,000 claim?', 'The Finance Manager', '3.2'),
            ('Q04', 'Days to hand in receipts?', '14 days', '3.1'),
            ('Q05', 'Overtime pay on a Sunday?', '2 times the hourly rate', '1.3'),
            ('Q06', 'Paste a price list into a public AI tool?', 'Only with the MD’s written approval', '4.4'),
            ('Q07', 'Report a lost laptop: when, to whom?', 'Within 4 hours, Operations Manager', '5.3'),
            ('Q08', 'Most for one night’s hotel?', 'UGX 180,000', '3.3'),
            ('Q09', 'Days of paid sick leave?', 'Not stated in the handbook', 'none'),
            ('Q10', 'Rate per kilometre for a private car?', 'Not stated in the handbook', 'none')]
    s = Scene(w, h)
    cols = [0.75, 4.9, 4.6, 1.2]
    xs = [0.1]
    for c in cols[:-1]:
        xs.append(xs[-1] + c)
    heads = ['', 'Question (shortened)', 'The key: the agreed answer', 'Clause']
    rh = (h - 0.75) / (len(rows) + 1)
    y = h - 0.15
    for j, hd in enumerate(heads):
        s.text(xs[j] + 0.08, y - rh / 2, hd, size=15, weight='bold', ha='left')
    s.line(0.1, y - rh, w - 0.1, y - rh, lw=1.6)
    for i, r in enumerate(rows):
        yy = y - (i + 1.5) * rh
        none = r[3] == 'none'
        if none:
            s.rect(0.1, yy - rh / 2, w - 0.2, rh, fill=PALE, edge=PALE, lw=0.5, z=1)
        for j, v in enumerate(r):
            s.text(xs[j] + 0.08, yy, v, size=14, ha='left', weight='bold' if j == 0 else 'normal', color=RED if (none and j >= 2) else (INK if j != 1 else BODY))
    s.text(0.1, 0.2, 'Two questions have no answer in the handbook: the honest answer is “not stated”. Fictional handbook.', size=14, color=MUTE, ha='left')
    return s


# ================================================================== demonstration: question by question (recorded)
@fig('x_l08_scores')
def x_l08_scores(w, h, **_):
    s = Scene(w, h)
    sets = [('No handbook', [False] * 8 + [True, True], '2 of 10'), ('Three closest clauses', [True] * 10, '10 of 10'), ('Whole handbook pasted', [True] * 10, '10 of 10')]
    lab_w = 3.1
    cw = (w - 0.2 - lab_w - 1.6) / 10
    top = h - 0.75
    for q in range(10):
        s.text(0.1 + lab_w + (q + 0.5) * cw, top + 0.3, f'Q{q + 1:02d}', size=14, weight='bold', color=RED if q >= 8 else INK)
    rh = (top - 0.75) / 3
    for i, (name, marks, tot) in enumerate(sets):
        y = top - (i + 0.5) * rh
        _wrap(s, 0.1, y, lab_w - 0.1, name, 17, weight='bold', ha='left')
        for q, ok in enumerate(marks):
            s.icon('check' if ok else 'cross', 0.1 + lab_w + (q + 0.5) * cw, y, 0.5)
        s.text(w - 0.1, y, tot, size=22, weight='bold', ha='right', color=RED if i == 0 else INK)
        if i:
            s.line(0.1, y + rh / 2, w - 0.1, y + rh / 2, color=HAIR, lw=1)
    _wrap(s, 0.1, 0.42, w - 0.2, 'Cross: said “not stated” though the handbook has the answer. No run invented an answer. Two runs of each set, the same result both times. Claude, fresh sessions, 4 and 6 Nov 2026.', 14, ha='left', color=MUTE)
    return s


# ================================================================== demonstration: the closest page held no answer, and the run said so
@fig('x_l08_notstated')
def x_l08_notstated(w, h, **_):
    d = _json('retrieval_results.json')
    r = [x for x in d['results'] if x['id'] == 'Q09'][0]
    names = {'2.1': 'Annual leave: 21 working days a year', '2.4': 'Report sickness by 9 am; a note after 2 days', '2.3': 'Carry over up to 5 unused days'}
    s = Scene(w, h)
    s.box(0.1, h - 0.8, w - 0.2, 0.65, '', fill=PAPER, lw=2, r=0.08)
    s.text(0.3, h - 0.48, 'Q09  How many days of paid sick leave does a staff member get?', size=16, weight='bold', ha='left')
    s.text(0.1, h - 1.12, 'The three closest clauses it was given', size=15, color=BODY, ha='left')
    for i, row in enumerate(r['top5'][:3]):
        y = h - 1.6 - i * 0.55
        s.box(0.1, y - 0.22, 0.75, 0.44, row['clause'], size=15, weight='bold', fill=PALE, r=0.06)
        trap = i == 0
        s.text(1.0, y, names.get(row['clause'], '') + ('   a number, for the wrong question' if trap else ''), size=15, ha='left', color=RED if trap else BODY, weight='bold' if trap else 'normal')
    ans = 'Not stated in the handbook. The passages cover annual leave [2.1] and the sickness rules [2.4], but give no number of paid sick leave days.'
    ah = _h(ans, 15, w - 0.6) + 0.35
    s.box(0.1, 0.5, w - 0.2, ah, '', fill=GOLD, edge=INK, lw=2, r=0.08)
    _wrap(s, 0.3, 0.5 + ah / 2, w - 0.6, ans, 15, ha='left')
    s.text(0.1, 0.2, 'Recorded answer, run 1 of 2, 6 Nov 2026; both runs said “not stated”.', size=14, color=MUTE, ha='left')
    return s


# ================================================================== your people
@fig('x_l08_people')
def x_l08_people(w, h, **_):
    roles = [('Frontline agent', ['Searching many systems while the customer waits', 'Listening, and handling the unusual case', 'Asking well and opening the source', 'Fear: scripted by a bot. Gain: faster, surer answers']),
             ('HR or compliance officer', ['Answering the same policy question again and again', 'Keeping the documents right and current', 'Writing clear, dated, single-version rules', 'Fear: blamed for a wrong answer. Gain: fewer repeat calls']),
             ('Lawyer or analyst', ['First drafts and first searches', 'Reviewing, and signing what goes out', 'Checking every source it cites', 'Fear: junior work disappears. Gain: time on judgement'])]
    return role_grid(w, h, roles, foot='Telstra frontline; Allen & Overy: a lawyer reviews every output; McKinsey: junior tasks change.')


# ================================================================== keepers of knowledge become document owners
@fig('x_l08_owners')
def x_l08_owners(w, h, **_):
    s = Scene(w, h)
    rows = [('book', 'Staff handbook', 'HR Officer'), ('calculator', 'Approval limits', 'Finance Manager'), ('tag', 'Price list', 'Sales Manager'), ('lock', 'Data and IT rules', 'Operations Manager')]
    s.text(0.1, h - 0.3, 'Document', size=16, weight='bold', ha='left')
    s.text(3.1, h - 0.3, 'Owner', size=16, weight='bold', ha='left')
    s.text(5.85, h - 0.3, 'On every page', size=16, weight='bold', ha='left')
    s.line(0.1, h - 0.55, w - 0.1, h - 0.55, lw=1.6)
    rh = (h - 1.35) / 4
    for i, (ic, doc, own) in enumerate(rows):
        y = h - 0.6 - (i + 0.5) * rh
        s.icon(ic, 0.4, y, 0.5)
        s.text(0.8, y, doc, size=16, ha='left')
        s.arrow(2.55, y, 3.05, y, lw=2, head=13)
        s.icon('person', 3.3, y, 0.45, accent=GOLD)
        s.text(3.58, y, own, size=15, weight='bold', ha='left')
        s.tag(5.85, y + 0.03, 'Version', size=14, fill=GOLD, color=INK, h=0.34)
        s.tag(5.85, y - 0.37, 'Review date', size=14, fill=PALE, color=INK, h=0.34)
    _wrap(s, w / 2, 0.35, w - 0.2, 'Nile Valley Foods (fictional). One owner, one current version, a date to review.', 15, color=BODY)
    return s


# ================================================================== hands-on example
@fig('x_l08_portfolio')
def x_l08_portfolio(w, h, **_):
    return portfolio_entry(w, h, 'Nile Valley Foods (fictional): one entry', [
        ('The use', 'Answer staff questions on leave, expenses and IT rules'),
        ('What goes in', 'The staff handbook, version 4, and a staff question'),
        ('What comes out', 'An answer with the clause number, or “not stated”'),
        ('Who uses it', 'All staff; HR owns the handbook'),
        ('How we would know it works', 'Ten questions with agreed answers, rerun monthly'),
        ('Today: route, and the documents', 'Prompt: paste the whole handbook (829 words)')])
