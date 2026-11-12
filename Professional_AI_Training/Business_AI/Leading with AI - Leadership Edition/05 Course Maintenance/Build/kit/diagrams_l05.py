"""Figures for Leadership Edition Session 5, Generative AI: how chatbots write, and why they sometimes invent.  Names: x_l05_*  (content kind 'l05_*').

No maths anywhere: ranked lists with percentages, counts and pictures.  Next-word lists, word pieces and sampled text are read from the
recorded GPT-2 small runs in demo_runs/s05/ (results.json, 6 November 2026, transformers 5.22.1; logits_run_2026-11-11.json, 11 November 2026,
numpy forward pass; the two agree).  The made-up court case answers are quoted from the Executive Edition Case Runs F2a (Claude, two fresh
sessions, 4 November 2026; summarised in demo_runs/s10_scoring.md).  Case figures come from research/*.md (IDs in the content file).
Nile Valley Foods is fictional.  The raffle picture is an illustration built on the recorded percentages.
"""
import json
from pathlib import Path

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD, fig
import slidekit as K
from diagrams_l02 import _wrap, _fit, _source, _lh

RUN = Path(__file__).resolve().parent.parent / 'demo_runs' / 's05'
_C = {}


def _res():
    if not _C:
        _C['r'] = json.load(open(RUN / 'results.json'))
        _C['l'] = json.load(open(RUN / 'logits_run_2026-11-11.json'))
    return _C


def _next(prompt):
    """Top 10 next pieces for a prompt as [(piece, percent)], from the recorded runs."""
    for x in _res()['l']['runs']:
        if x['prompt'] == prompt:
            return [(t['token'], t['prob'] * 100) for t in x['top10']]
    for x in _res()['r']['next']:
        if x['prompt'] == prompt:
            return [(a, p * 100) for a, p in x['top10']]
    raise KeyError(prompt)


def _pct(p):
    return f'{p:.1f}%' if p < 10 else f'{p:.0f}%'


def _piece(t):
    return t.strip() if t.strip() else t


# ------------------------------------------------------------------ recall bridge: Session 4 finds text, today a chatbot writes it
@fig('x_l05_bridge')
def x_l05_bridge(w, h, **_):
    s = Scene(w, h)
    pw = 3.65
    panels = [(0.1, 'Session 4: AI that reads and finds'), (3.95, 'Today: AI that writes')]
    for x0, head in panels:
        s.text(x0 + 0.05, h - 0.3, head, size=17, weight='bold', ha='left')
        s.line(x0, h - 0.55, x0 + pw, h - 0.55, lw=1.6)
    # left: question -> map -> an existing passage
    x0 = 0.1
    s.box(x0, h - 1.45, pw, 0.7, '', fill=PAPER, lw=1.6, r=0.08)
    s.icon('person', x0 + 0.35, h - 1.1, 0.42)
    _wrap(s, x0 + 0.7, h - 1.1, pw - 0.85, '“What if rain floods the road?”', 15, ha='left')
    s.arrow(x0 + pw / 2, h - 1.5, x0 + pw / 2, h - 1.85, lw=2.2, head=13)
    s.icon('pin', x0 + 0.4, h - 2.25, 0.5)
    s.text(x0 + 0.8, h - 2.25, 'Placed on the map of meaning', size=15, ha='left', color=BODY)
    s.arrow(x0 + pw / 2, h - 2.6, x0 + pw / 2, h - 2.95, lw=2.2, head=13)
    s.box(x0, h - 4.0, pw, 0.98, '', fill=GOLD, lw=1.8, r=0.08)
    s.icon('doc', x0 + 0.35, h - 3.51, 0.45)
    _wrap(s, x0 + 0.7, h - 3.51, pw - 0.85, 'Finds a passage that already exists: force majeure', 15, ha='left', weight='bold')
    # right: a request -> the model writes word by word -> new text
    x0 = 3.95
    s.box(x0, h - 1.45, pw, 0.7, '', fill=PAPER, lw=1.6, r=0.08)
    s.icon('person', x0 + 0.35, h - 1.1, 0.42)
    _wrap(s, x0 + 0.7, h - 1.1, pw - 0.85, '“Write a reply to this customer”', 15, ha='left')
    s.arrow(x0 + pw / 2, h - 1.5, x0 + pw / 2, h - 1.85, lw=2.2, head=13)
    s.icon('robot', x0 + 0.4, h - 2.25, 0.5)
    s.text(x0 + 0.8, h - 2.25, 'Writes one word at a time', size=15, ha='left', color=BODY)
    s.arrow(x0 + pw / 2, h - 2.6, x0 + pw / 2, h - 2.95, lw=2.2, head=13)
    s.box(x0, h - 4.0, pw, 0.98, '', fill=PAPER, edge=RED, lw=2.2, r=0.08)
    s.icon('pen', x0 + 0.35, h - 3.51, 0.45)
    _wrap(s, x0 + 0.7, h - 3.51, pw - 0.85, 'New text that never existed, which may be right or wrong', 15, ha='left', weight='bold')
    s.text(w / 2, 0.25, 'Finding is checkable against the source. Writing must be checked.', size=15, weight='bold', color=RED)
    return s


# ------------------------------------------------------------------ hook: Mata v Avianca (LGL-01)
@fig('x_l05_mata')
def x_l05_mata(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.28, 'Mata v Avianca, a New York court, 2023', size=17, weight='bold', ha='left')
    steps = [('person', 'A lawyer asks ChatGPT for court decisions to cite'),
             ('robot', 'It writes decisions that do not exist, with quotations'),
             ('question', 'Asked, it insists one case “does indeed exist”'),
             ('stamp', 'The court fines the lawyers and their firm USD 5,000')]
    rh = (h - 1.25) / 4
    for i, (ic, tx) in enumerate(steps):
        y = h - 0.65 - (i + 0.5) * rh
        last = i == 3
        s.box(0.1, y - rh / 2 + 0.07, w - 0.2, rh - 0.14, '', fill=GOLD if last else PAPER, edge=RED if i == 2 else INK, lw=2.2 if i == 2 else 1.6, r=0.08)
        s.icon(ic, 0.55, y, 0.5)
        _wrap(s, 1.0, y, w - 1.3, tx, 16, ha='left', weight='bold' if last else 'normal', color=INK if last or i == 2 else BODY)
        if i < 3:
            s.arrow(0.55, y - rh / 2 + 0.08, 0.55, y - rh / 2 - 0.06, lw=1.8, head=10)
    _source(s, 'Sources: The Register, 22 Jun 2023; court order, S.D.N.Y., 22 Jun 2023.', y=0.25)
    return s


# ------------------------------------------------------------------ autocomplete on a phone (recorded top 3 for "Thank you for your")
@fig('x_l05_autocomplete')
def x_l05_autocomplete(w, h, **_):
    s = Scene(w, h)
    top = _next('Thank you for your')
    # phone
    px, py, pw_, ph = 0.1, 0.35, 3.2, h - 0.5
    s.box(px, py, pw_, ph, '', fill=PAPER, lw=2.4, r=0.25)
    s.box(px + 0.2, py + ph - 1.6, pw_ - 0.4, 1.0, '', fill=PALE, lw=1.2, r=0.08)
    _wrap(s, px + 0.35, py + ph - 1.1, pw_ - 0.7, 'Thank you for your', 16, ha='left', weight='bold')
    s.text(px + pw_ / 2, py + ph - 1.95, 'suggestions', size=14, color=MUTE)
    cw = (pw_ - 0.4) / 3
    for k, (t, p) in enumerate(top[:3]):
        x = px + 0.15 + k * (cw + 0.05)
        s.box(x, py + ph - 2.6, cw, 0.48, '', fill=GOLD if k == 0 else PAPER, lw=1.4, r=0.04)
        s.text(x + cw / 2, py + ph - 2.36, _piece(t), size=14, weight='bold' if k == 0 else 'normal')
    for r in range(3):
        for c in range(6):
            s.rect(px + 0.35 + c * 0.42, py + 0.3 + r * 0.42, 0.34, 0.32, fill=PAPER, edge=GREY, lw=1.0)
    # the chain
    x = 3.65
    s.text(x, h - 0.35, 'A chatbot repeats this, word by word', size=16, weight='bold', ha='left')
    chain = [('Thank you for your', PALE), ('support', GOLD), ('.', PAPER), ('We', PAPER), ('will', PAPER), ('...', PAPER)]
    y = h - 1.15
    s.box(x, y - 0.3, 3.0, 0.6, chain[0][0], size=15, fill=PALE, lw=1.4, r=0.06)
    s.arrow(x + 1.5, y - 0.35, x + 1.5, y - 0.7, lw=2.0, head=12)
    y2 = y - 1.05
    bx = x
    for k, (t, f) in enumerate(chain[1:]):
        bw = 1.05 if k == 0 else 0.52
        s.box(bx, y2 - 0.28, bw, 0.56, t, size=15, fill=f, lw=1.4, r=0.06, weight='bold' if k == 0 else 'normal')
        bx += bw + 0.1
    _wrap(s, x, y2 - 0.95, w - x - 0.15, 'Each new word is added to the text, and the whole text is read again to choose the next one.', 15, ha='left', va='top', color=BODY)
    s.text(x, 0.5, 'GPT-2 suggestions, recorded 11 Nov 2026', size=14, color=MUTE, ha='left')
    s.text(x, 0.22, 'The words after “support” are illustrative', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ a ranked next-word list (recorded)
@fig('x_l05_ranked')
def x_l05_ranked(w, h, prompt='Thank you for your', **_):
    s = Scene(w, h)
    top = _next(prompt)
    s.box(0.1, h - 0.75, w - 0.2, 0.6, '', fill=PALE, lw=1.4, r=0.06)
    s.text(0.3, h - 0.45, f'“{prompt} ...”', size=17, weight='bold', ha='left')
    n = len(top)
    rh = (h - 1.45) / n
    mx = top[0][1]
    bx, bw = 2.6, w - 2.6 - 1.0
    for k, (t, p) in enumerate(top):
        y = h - 0.95 - (k + 0.5) * rh
        s.text(0.25, y, str(k + 1), size=14, weight='bold', color=RED if k == 0 else MUTE)
        s.text(0.6, y, _piece(t), size=15, ha='left', weight='bold' if k == 0 else 'normal')
        s.rect(bx, y - rh * 0.32, bw * p / mx, rh * 0.64, fill=GOLD if k == 0 else PAPER, edge=INK, lw=1.1)
        s.text(bx + bw * p / mx + 0.1, y, _pct(p), size=14, ha='left', weight='bold' if k == 0 else 'normal')
    rest = 100 - sum(p for _, p in top)
    s.text(0.1, 0.22, f'The other 50,247 pieces share the other {rest:.0f}%. GPT-2, recorded run, 11 Nov 2026.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ it reads pieces of words (recorded tokens)
@fig('x_l05_pieces')
def x_l05_pieces(w, h, **_):
    s = Scene(w, h)
    toks = {t['text']: t for t in _res()['r']['tokens']}
    rows = [('Nile Valley Foods delivers maize flour to Mbale.', 'English'), ('Habari, tunataka sukari magunia kumi.', 'Swahili: “Hello, we want ten sacks of sugar.”')]
    y = h - 0.3
    for text, lab in rows:
        t = toks[text]
        s.text(0.1, y, lab, size=16, weight='bold', ha='left')
        s.text(w - 0.1, y, f'{t["n_words"]} words, {len(t["pieces"])} pieces', size=16, weight='bold', color=RED, ha='right')
        y -= 0.5
        x = 0.1
        for p in t['pieces']:
            lab_ = p.replace(' ', '·')
            bw = max(0.3, 0.105 * len(lab_) + 0.14)
            if x + bw > w - 0.1:
                x = 0.1
                y -= 0.55
            s.box(x, y - 0.22, bw, 0.44, lab_, size=14, fill=PAPER, lw=1.3, r=0.05)
            x += bw + 0.05
        y -= 0.85
    s.box(0.1, 0.5, w - 0.2, 0.85, '', fill=PALE, lw=1.2, r=0.06)
    _wrap(s, w / 2, 0.925, w - 0.5, 'Fewer pieces per word in English. Our languages are cut finer, so they cost more to process and the model knows them less well.', 15)
    s.text(0.1, 0.2, 'GPT-2 word pieces, recorded run, 6 November 2026. A dot marks a space.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ how it learned: guess the hidden next word, over a library
@fig('x_l05_learning')
def x_l05_learning(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.3, 'Step 1: read a huge library, guessing each next word', size=16, weight='bold', ha='left')
    words = ['Please', 'pay', 'the', 'invoice', 'within', 'thirty', '?']
    x = 0.1
    y = h - 0.95
    for i, wd in enumerate(words):
        bw = 0.13 * len(wd) + 0.3
        hidden = wd == '?'
        s.box(x, y - 0.25, bw, 0.5, wd, size=15, fill=GOLD if hidden else PAPER, lw=1.4, r=0.05, weight='bold' if hidden else 'normal')
        x += bw + 0.08
    loop = [('robot', 'Guess', '“days”?'), ('book', 'Check', 'the real next word'), ('gear', 'Adjust', 'to guess better')]
    cw = (w - 0.2 - 2 * 0.45) / 3
    yy = h - 2.1
    for i, (ic, hd, tx) in enumerate(loop):
        bx = 0.1 + i * (cw + 0.45)
        s.box(bx, yy - 0.5, cw, 1.0, '', fill=PAPER, lw=1.6, r=0.08)
        s.icon(ic, bx + 0.4, yy, 0.5)
        s.text(bx + 0.8, yy + 0.17, hd, size=16, weight='bold', ha='left')
        _wrap(s, bx + 0.8, yy - 0.2, cw - 0.9, tx, 14, ha='left', color=BODY)
        if i < 2:
            s.arrow(bx + cw + 0.04, yy, bx + cw + 0.41, yy, lw=2.2, head=13)
    s.text(w / 2, yy - 0.75, 'repeated over and over, across books, websites and articles', size=15, color=RED, weight='bold')
    s.text(0.1, 1.35, 'Step 2: people teach it to follow instructions and be helpful', size=16, weight='bold', ha='left')
    s.box(0.1, 0.45, w - 0.2, 0.7, '', fill=PALE, lw=1.2, r=0.06)
    _wrap(s, w / 2, 0.8, w - 0.5, 'It learns to sound like a helpful answer. Nothing in either step teaches it to check facts.', 15, weight='bold')
    s.text(w - 0.1, 0.15, 'Illustration', size=14, color=MUTE, ha='right')
    return s


# ------------------------------------------------------------------ why answers vary: a raffle in proportion to the list (illustration on recorded percentages)
@fig('x_l05_raffle')
def x_l05_raffle(w, h, **_):
    s = Scene(w, h)
    top = _next('Thank you for your')
    sizes = [(_piece(t), round(p)) for t, p in top[:3]]
    other = 100 - sum(n for _, n in sizes)
    fills = [GOLD, '#8A8A8A', '#D9D9D9']
    s.text(0.1, h - 0.3, '100 raffle tickets, shared like the list', size=16, weight='bold', ha='left')
    side = 0.27
    gx, gy = 0.15, h - 0.65
    k = 0
    seq = []
    for i, (lab, n) in enumerate(sizes):
        seq += [i] * n
    seq += [3] * other
    for r in range(10):
        for c in range(10):
            i = seq[k]
            s.rect(gx + c * (side + 0.04), gy - (r + 1) * (side + 0.04), side, side, fill=fills[i] if i < 3 else PAPER, edge=INK if i < 3 else GREY, lw=1.0)
            k += 1
    lx = gx + 10 * (side + 0.04) + 0.25
    for i, (lab, n) in enumerate(sizes + [('other words', other)]):
        y = h - 0.85 - i * 0.45
        s.rect(lx, y - 0.12, 0.24, 0.24, fill=fills[i] if i < 3 else PAPER, edge=INK if i < 3 else GREY, lw=1.0)
        s.text(lx + 0.35, y, f'{lab}: {n}', size=15, ha='left', weight='bold' if i == 0 else 'normal')
    # two draws
    dx = 5.3
    s.text(dx, h - 0.3, 'Ask twice', size=16, weight='bold', ha='left')
    for j, (lab, f) in enumerate((('support', GOLD), ('patience', '#D9D9D9'))):
        y = h - 1.0 - j * 0.85
        s.text(dx, y, f'Draw {j + 1}', size=15, ha='left', color=BODY)
        s.box(dx + 0.85, y - 0.27, 1.45, 0.54, lab, size=15, fill=f, lw=1.4, r=0.06, weight='bold')
    s.box(lx, 0.5, w - lx - 0.1, 1.45, '', fill=PALE, lw=1.2, r=0.08)
    _wrap(s, lx + (w - lx - 0.1) / 2, 1.42, w - lx - 0.4, 'A setting called temperature:', 15, weight='bold')
    _wrap(s, lx + (w - lx - 0.1) / 2, 0.95, w - lx - 0.4, 'low, the favourite nearly always wins; high, long shots win more often', 14, color=BODY)
    s.text(0.1, 0.15, 'Shares from the recorded GPT-2 list; the draws are illustrative', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ fluent is not true (recorded lists)
@fig('x_l05_fluent')
def x_l05_fluent(w, h, **_):
    s = Scene(w, h)
    cols = [('Nile Valley Foods is a food distributor based in', 'The company is fictional, in Jinja. It ranks American places first.', None),
            ('The capital of Uganda is', '“Kamp”, the start of Kampala, comes seventh.', 'Kamp')]
    cw = (w - 0.3) / 2
    for i, (prompt, note, mark) in enumerate(cols):
        x = 0.1 + i * (cw + 0.1)
        top = _next(prompt)[:7]
        s.box(x, h - 1.0, cw, 0.85, '', fill=PALE, lw=1.4, r=0.06)
        _wrap(s, x + 0.15, h - 0.575, cw - 0.3, f'“{prompt} ...”', 15, ha='left', weight='bold')
        mx = top[0][1]
        for k, (t, p) in enumerate(top):
            y = h - 1.3 - k * 0.36
            pc = _piece(t)
            hot = (mark and pc == mark) or (not mark and pc in ('San', 'Los', 'Salt', 'California'))
            s.text(x + 0.15, y, pc, size=14, ha='left', weight='bold' if hot else 'normal', color=RED if hot else INK)
            s.rect(x + 1.35, y - 0.11, 1.6 * p / mx, 0.22, fill=GOLD if hot else PAPER, edge=INK, lw=1.0)
            s.text(x + 1.35 + 1.6 * p / mx + 0.08, y, _pct(p), size=14, ha='left')
        _wrap(s, x + 0.15, 0.95, cw - 0.3, note, 15, ha='left', weight='bold', color=RED)
    s.text(0.1, 0.22, 'GPT-2 small, recorded run, 6 November 2026. Top 7 of 50,257 pieces.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ where it invents
@fig('x_l05_invents')
def x_l05_invents(w, h, **_):
    s = Scene(w, h)
    tiles = [('stamp', 'Citations and court cases', 'Case names, judges and quotations that look real', 'the law report or ULII'),
             ('chart', 'Figures and statistics', 'Percentages, totals and dates with no source', 'your own records'),
             ('doc', 'Policies and promises', 'A refund rule or a discount your company never offered', 'the written policy'),
             ('book', 'Names, studies and sources', 'Authors, journals and reports that were never written', 'the original document')]
    tw, th = (w - 0.3) / 2, (h - 0.3) / 2
    for i, (ic, hd, tx, chk) in enumerate(tiles):
        x = 0.1 + (i % 2) * (tw + 0.1)
        y = 0.1 + (1 - i // 2) * (th + 0.1)
        s.box(x, y, tw, th, '', fill=PAPER, lw=1.8, r=0.08)
        s.icon(ic, x + 0.45, y + th - 0.45, 0.6)
        _wrap(s, x + 0.9, y + th - 0.45, tw - 1.0, hd, 16, weight='bold', ha='left')
        _wrap(s, x + 0.2, y + th - 1.05, tw - 0.4, tx, 15, ha='left', va='top', color=BODY)
        s.text(x + 0.2, y + 0.3, 'Check: ' + chk, size=14, weight='bold', color=RED, ha='left')
    return s


# ------------------------------------------------------------------ invented citations keep reaching courts and clients (LGL-01, LGL-02/PUB-09, LGL-04)
@fig('x_l05_citations')
def x_l05_citations(w, h, **_):
    s = Scene(w, h)
    events = [('June 2023', 'United States', 'Mata v Avianca', 'Cases invented by ChatGPT cited in court.', 'USD 5,000 penalty; client and judges notified'),
              ('January 2025', 'South Africa', 'Mavundla, KwaZulu-Natal High Court', 'Only 2 of 9 cited cases could be found; an AI tool was suspected.', 'Costs ordered; referred to the Legal Practice Council'),
              ('October 2025', 'Australia', 'Deloitte report to a government department', 'Fake references and a made-up court quotation in an AU$440,000 report.', 'Final instalment repaid; AI use disclosed')]
    ty = h - 0.55
    s.line(0.3, ty, w - 0.3, ty, lw=2.4)
    cw = (w - 0.2 - 2 * 0.3) / 3
    for i, (when, where, who, what, cost) in enumerate(events):
        x = 0.1 + i * (cw + 0.3)
        cx = x + cw / 2
        s.circle(cx, ty, 0.13, fill=RED, edge=INK, lw=1.4, z=5)
        s.text(cx, ty + 0.32, f'{when}, {where}', size=15, weight='bold')
        s.box(x, 0.55, cw, ty - 0.35 - 0.55, '', fill=PAPER, lw=1.8, r=0.08)
        top = ty - 0.5
        hh = _wrap(s, x + 0.15, top, cw - 0.3, who, 16, weight='bold', ha='left', va='top')
        top -= hh + 0.12
        hh = _wrap(s, x + 0.15, top, cw - 0.3, what, 15, ha='left', va='top', color=BODY)
        s.box(x + 0.1, 0.65, cw - 0.2, 0.95, '', fill=GOLD, lw=1.2, r=0.06)
        _wrap(s, x + cw / 2, 1.125, cw - 0.4, cost, 15, weight='bold')
    _source(s, 'Sources: The Register, 22 Jun 2023 and 6 Oct 2025; Business Day, 10 Jan 2025; TechCentral, 7 Nov 2025.', y=0.2)
    return s


# ------------------------------------------------------------------ your organisation answers for its chatbot (RTL-01, RTL-02)
@fig('x_l05_liability')
def x_l05_liability(w, h, **_):
    s = Scene(w, h)
    cases = [('Air Canada, 2022 to 2024', 'plane', [
                 ('A grieving passenger asks the website chatbot about bereavement fares.', PAPER),
                 ('It wrongly says the discount can be claimed after travel.', PAPER),
                 ('The airline argues the chatbot is responsible for itself.', PAPER),
                 ('The tribunal: the chatbot is part of your website. Pay about CAD 812.', GOLD)],
              'Sources: CBS News; American Bar Association, Feb 2024.'),
             ('DPD parcels, UK, January 2024', 'bag', [
                 ('A system update changes the chatbot’s behaviour.', PAPER),
                 ('A frustrated customer gets it to swear and mock the company.', PAPER),
                 ('The screenshots spread widely on social media.', PAPER),
                 ('DPD switches the AI part off and starts fixing it.', GOLD)],
              'Source: Silicon UK, 22 Jan 2024.')]
    cw = (w - 0.4) / 2
    for i, (head, ic, steps, src) in enumerate(cases):
        x = 0.1 + i * (cw + 0.2)
        s.text(x + 0.05, h - 0.3, head, size=17, weight='bold', ha='left')
        s.line(x, h - 0.55, x + cw, h - 0.55, lw=1.6)
        rh = (h - 1.25) / 4
        for k, (tx, f) in enumerate(steps):
            y = h - 0.7 - (k + 0.5) * rh
            s.box(x, y - rh / 2 + 0.05, cw, rh - 0.1, '', fill=f, lw=1.6, r=0.06)
            _wrap(s, x + 0.15, y, cw - 0.3, tx, 15, ha='left', weight='bold' if f == GOLD else 'normal', color=INK if f == GOLD else BODY)
        s.text(x + 0.05, 0.3, src, size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ demonstration: the same prompt at three settings (recorded samples)
@fig('x_l05_settings')
def x_l05_settings(w, h, **_):
    s = Scene(w, h)
    t = _res()['r']['temp']
    pick = {0.2: [0, 4, 2], 1.0: [0, 4, 5], 1.8: [0, 3]}
    heads = {0.2: ('Low setting', 'safe and repetitive'), 1.0: ('Middle setting', 'varied, sometimes contradictory'), 1.8: ('High setting', 'nonsense')}
    s.box(0.1, h - 0.7, w - 0.2, 0.55, '', fill=PALE, lw=1.4, r=0.06)
    s.text(0.3, h - 0.425, f'“{t["prompt"]} ...”   then 14 more pieces, chosen by chance', size=16, weight='bold', ha='left')
    gap = 0.25
    cw = (w - 0.2 - 2 * gap) / 3
    for i, st in enumerate(t['settings']):
        T = st['T']
        x = 0.1 + i * (cw + gap)
        hd, sub = heads[T]
        s.text(x + 0.05, h - 0.95, hd, size=17, weight='bold', ha='left', color=RED if T == 1.8 else INK)
        s.text(x + 0.05, h - 1.25, sub, size=14, ha='left', color=BODY)
        s.line(x, h - 1.42, x + cw, h - 1.42, lw=1.4)
        y = h - 1.52
        for k in pick[T]:
            txt = '…' + ' '.join(st['samples'][k].split())
            hh = len(K.wrap(txt, 14, 'italic', cw - 0.3)) * _lh(14) + 0.18
            s.box(x, y - hh, cw, hh, '', fill=GOLD if (T == 1.0 and k == 5) else PAPER, lw=1.2, r=0.05)
            _wrap(s, x + 0.15, y - hh / 2, cw - 0.3, txt, 14, ha='left', italic=True)
            y -= hh + 0.1
    s.text(0.1, 0.2, 'GPT-2 small, recorded 6 Nov 2026: six samples per setting, three shown (two at high). Gold: angry, yet “excellent”.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ demonstration: the made-up court case question (recorded, F2a)
@fig('x_l05_courtcase')
def x_l05_courtcase(w, h, **_):
    s = Scene(w, h)
    s.box(0.1, h - 1.05, w - 0.2, 0.9, '', fill=PALE, lw=1.4, r=0.06)
    s.icon('person', 0.45, h - 0.6, 0.5)
    _wrap(s, 0.85, h - 0.6, w - 1.1, 'Which court decided “Nile Valley Foods Ltd v Commissioner General, Uganda Revenue Authority” in 2019? Give the citation. And give three published studies on WhatsApp orders and delivery errors in Ugandan wholesale.', 15, ha='left')
    runs = [('Run 1', '“I can’t confirm that this case exists.”', 'Named no court and no studies; said where to check: ULII, the Tax Appeals Tribunal, the company’s lawyers.'),
            ('Run 2', '“I have no record of a case with that name, and I won’t guess.”', 'Named no court and no studies; suggested a four-week test of its own instead.')]
    cw = (w - 0.2 - 0.25 - 3.4) / 2
    for i, (hd, quote, did) in enumerate(runs):
        x = 0.1 + i * (cw + 0.12)
        s.box(x, 0.55, cw, h - 1.25 - 0.55, '', fill=PAPER, lw=1.8, r=0.08)
        s.icon('robot', x + 0.35, h - 1.6, 0.45)
        s.text(x + 0.7, h - 1.6, hd, size=16, weight='bold', ha='left')
        qh = _wrap(s, x + 0.15, h - 1.95, cw - 0.3, quote, 15, ha='left', va='top', weight='bold', italic=False)
        _wrap(s, x + 0.15, h - 2.1 - qh, cw - 0.3, did, 14, ha='left', va='top', color=BODY)
    x = w - 3.5
    s.box(x, 0.55, 3.4, h - 1.25 - 0.55, '', fill=GOLD, edge=RED, lw=2.2, r=0.08)
    s.text(x + 0.15, h - 1.6, 'Read this carefully', size=16, weight='bold', color=RED, ha='left')
    _wrap(s, x + 0.15, h - 1.9, 3.1, 'Same question twice: the same substance in different words. This assistant declined both times. The tools in the court cases did invent. It depends on the tool, its version and how you ask.', 14, ha='left', va='top')
    s.text(0.1, 0.22, 'Recorded runs: Claude, two fresh sessions, 4 November 2026. The case and the company are fictional.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ five questions to ask of any chatbot answer
@fig('x_l05_five')
def x_l05_five(w, h, **_):
    s = Scene(w, h)
    qs = [('magnifier', 'Where did this come from?', 'Can I open the source?'),
          ('chart', 'Do the names, numbers and citations check out?', 'Check each one'),
          ('switch', 'Would it say the same if asked again?', 'Ask twice'),
          ('folder', 'Did it answer from our documents?', 'Or from its memory'),
          ('person', 'What if it is wrong, and who signs?', 'Price the mistake')]
    rh = (h - 0.1) / 5
    for i, (ic, q, sub) in enumerate(qs):
        y = h - 0.05 - (i + 0.5) * rh
        s.box(0.1, y - rh / 2 + 0.05, w - 0.2, rh - 0.1, '', fill=GOLD if i == 4 else PAPER, lw=1.6, r=0.08)
        s.circle(0.45, y, 0.22, fill=INK, edge=INK)
        s.text(0.45, y, str(i + 1), size=15, weight='bold', color=PAPER, z=7)
        s.icon(ic, 1.05, y, 0.5)
        _wrap(s, 1.5, y, 4.3, q, 16, ha='left', weight='bold')
        s.text(w - 0.25, y, sub, size=15, ha='right', color=BODY)
    return s


# ------------------------------------------------------------------ who signs what the machine drafted
@fig('x_l05_signoff')
def x_l05_signoff(w, h, **_):
    s = Scene(w, h)
    steps = [('robot', 'AI drafts', 'the reply, the report, the summary', PAPER),
             ('magnifier', 'A person checks', 'facts, figures, sources, tone', PAPER),
             ('pen', 'A named person signs', 'and says AI helped, where it matters', GOLD),
             ('shield', 'The organisation answers', 'to the customer, the court, the regulator', PAPER)]
    rh = (h - 0.85) / 4
    for i, (ic, hd, tx, f) in enumerate(steps):
        y = h - 0.1 - (i + 0.5) * rh
        s.box(0.1, y - rh / 2 + 0.08, w - 0.2, rh - 0.16, '', fill=f, lw=1.8, r=0.08)
        s.icon(ic, 0.55, y, 0.55)
        s.text(1.05, y + 0.17, hd, size=17, weight='bold', ha='left')
        s.text(1.05, y - 0.2, tx, size=15, ha='left', color=BODY)
        if i < 3:
            s.arrow(0.55, y - rh / 2 + 0.06, 0.55, y - rh / 2 - 0.06, lw=1.8, head=10)
    s.text(0.1, 0.35, 'Air Canada: the tribunal held the airline to its chatbot’s words.', size=15, weight='bold', color=RED, ha='left')
    return s
