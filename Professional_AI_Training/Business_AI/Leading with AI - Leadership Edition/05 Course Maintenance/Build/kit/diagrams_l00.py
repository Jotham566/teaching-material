"""Figures for Session 0 of the Leadership Edition, The AI landscape for leaders.  Names: x_l00_*  (content kind 'l00_*').

No maths. Every figure is a picture with counts, percentages or shillings. Case figures come from research/*.md (IDs in each docstring).
Demonstration figures come from recorded runs: demo_runs/s02/run_output.txt (40 Nile Valley Foods messages, scikit-learn 1.9.1,
5 and 11 November 2026) and demo_runs/s12_rule_vs_ai.md with the Twelve-Message AI Demonstration Results (Claude, three fresh sessions,
4 November 2026). Nile Valley Foods is fictional.
"""
from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD, fig
import slidekit as K

LH = 1.18   # line height factor


def _lines(text, size, w, weight='normal'):
    return K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', w)


def _h(text, size, w, weight='normal'):
    return len(_lines(text, size, w, weight)) * size * LH / 72


def wt(s, x, y, w, text, size=16, weight='normal', color=INK, ha='center', va='center', italic=False):
    """Wrapped text in a column of width w. (x, y) is the anchor as for Scene.text. Returns the height in inches."""
    ls = _lines(text, size, w, weight)
    s.text(x, y, '\n'.join(ls), size=size, weight=weight, color=color, ha=ha, va=va, italic=italic)
    return len(ls) * size * LH / 72


def source(s, w, text, size=14, y=0.06):
    """A small source line at the bottom, wrapped to the width; y is the bottom edge. Returns its height."""
    return wt(s, 0.08, y, w - 0.2, text, size, ha='left', va='bottom', color=MUTE, italic=True)


# ------------------------------------------------------------------ hook: URA (PUB-01)
@fig('x_l00_ura')
def x_l00_ura(w, h, **_):
    """Records cross-checked, a few flagged for officers (PUB-01)."""
    s = Scene(w, h)
    rows = 6
    top = h - 0.35
    rh = 0.42
    s.text(w / 2, h - 0.15, 'Tax records cross-checked', size=16, weight='bold')
    flagged = (1, 4)
    for i in range(rows):
        y = top - (i + 1) * rh
        fl = i in flagged
        s.box(0.15, y + 0.05, w - 1.3, rh - 0.1, '', fill=GOLD if fl else PAPER, edge=RED if fl else INK, lw=2.2 if fl else 1.4, r=0.04)
        for j in range(4):
            s.line(0.35 + j * 0.7, y + rh / 2, 0.8 + j * 0.7, y + rh / 2, color=GREY if not fl else INK, lw=2.2)
        if fl:
            s.icon('flag', w - 0.75, y + rh / 2, 0.45, accent=RED)
    s.icon('magnifier', w - 0.75, top - 2.5 * rh, 0.6)
    yb = top - rows * rh - 0.15
    wt(s, w / 2, yb - 0.35, w - 0.3, 'AI flags the records that do not match; officers investigate', 15, color=BODY)
    return s


# ------------------------------------------------------------------ the promise and who it is for
@fig('x_l00_promise')
def x_l00_promise(w, h, **_):
    s = Scene(w, h)
    roles = ['CEO or MD', 'Board member', 'Director', 'Senior manager']
    s.text(0.1, h - 0.22, 'Who it is for', size=17, weight='bold', ha='left', color=RED)
    seg = (w - 0.2) / len(roles)
    for i, r in enumerate(roles):
        x = 0.1 + seg * (i + 0.5)
        s.icon('person', x, h - 0.85, 0.75, accent=GOLD if i == 0 else PAPER)
        s.text(x, h - 1.42, r, size=15)
    s.line(0.1, h - 1.72, w - 0.1, h - 1.72, color=HAIR, lw=1.4)
    s.text(0.1, h - 1.98, 'You leave able to', size=17, weight='bold', ha='left', color=RED)
    items = [('magnifier', 'Spot where AI creates value in your industry'), ('question', 'Ask vendors and your teams the right questions'),
             ('shield', 'Judge a claim, a pilot and a risk'), ('people', 'Lead your people through the change'),
             ('calendar', 'Start a governed 90-day plan')]
    rh = (h - 2.2) / len(items)
    for i, (ic, t) in enumerate(items):
        yc = h - 2.2 - (i + 0.5) * rh
        s.box(0.1, yc - rh * 0.42, 0.5, rh * 0.84, str(i + 1), size=17, weight='bold', fill=GOLD, edge=INK, lw=1.6, r=0.05)
        s.icon(ic, 1.05, yc, 0.5)
        s.text(1.45, yc, t, size=17, ha='left')
    return s


# ------------------------------------------------------------------ AI as a family
@fig('x_l00_family')
def x_l00_family(w, h, **_):
    s = Scene(w, h)
    # rules, on the left
    rw = 2.25
    s.box(0.05, 0.6, rw, h - 0.65, '', fill=PAPER, edge=INK, lw=2.0, r=0.08)
    s.icon('doc', 0.05 + rw / 2, h - 0.55, 0.65)
    s.text(0.05 + rw / 2, h - 1.15, 'Rules', size=19, weight='bold')
    wt(s, 0.05 + rw / 2, h - 1.75, rw - 0.25, 'A person writes every step', 15, color=BODY)
    wt(s, 0.05 + rw / 2, 1.55, rw - 0.25, 'If a payment is over UGX 5 million, ask a manager', 15, color=MUTE, italic=True)
    # machine learning, nested
    x0 = rw + 0.25
    W = w - x0 - 0.05
    s.box(x0, 0.6, W, h - 0.65, '', fill=PAPER, edge=INK, lw=2.0, r=0.08)
    s.text(x0 + 0.2, h - 0.3, 'Machine learning', size=19, weight='bold', ha='left')
    s.text(x0 + 0.2, h - 0.68, 'Learns the steps from examples', size=15, ha='left', color=BODY)
    s.text(x0 + 0.2, h - 1.05, 'Learns from past loans who repaid', size=15, ha='left', color=MUTE, italic=True)
    gx = x0 + 0.25
    GW = W - 0.5
    s.box(gx, 0.8, GW, h - 2.15, '', fill=PALE, edge=INK, lw=1.8, r=0.08)
    s.text(gx + 0.2, h - 1.6, 'Generative AI', size=19, weight='bold', ha='left')
    s.text(gx + 0.2, h - 1.98, 'Writes new text, pictures or code', size=15, ha='left', color=BODY)
    s.text(gx + 0.2, h - 2.33, 'Drafts a reply to a customer', size=15, ha='left', color=MUTE, italic=True)
    ax = gx + 0.25
    AW = GW - 0.5
    s.box(ax, 1.0, AW, 1.05, '', fill=GOLD, edge=INK, lw=1.8, r=0.08)
    s.text(ax + 0.2, 1.75, 'Agents', size=19, weight='bold', ha='left')
    s.text(ax + 0.2, 1.33, 'Use tools to act: check, book, send', size=15, ha='left', color=INK)
    s.text(w / 2, 0.25, 'Each inner box is a kind of the one around it. Rules sit apart: they do not learn.', size=14, color=MUTE)
    return s


# ------------------------------------------------------------------ a model learns from examples, like a new employee
@fig('x_l00_newhire')
def x_l00_newhire(w, h, **_):
    s = Scene(w, h)
    lab_w = 1.35
    cw = (w - lab_w - 0.2 - 2 * 0.45) / 3
    xs = [lab_w + 0.1 + i * (cw + 0.45) for i in range(3)]
    heads = ['Past files', 'Learning', 'A new case']
    for i, hd in enumerate(heads):
        s.text(xs[i] + cw / 2, h - 0.22, hd, size=17, weight='bold', color=RED)
    rows = [('person', 'New loan officer', ['Reads 500 past loan files, and who repaid', 'Notices what good payers had in common', 'Judges a new application']),
            ('robot', 'Model', ['Thousands of past cases, each with its outcome (a label)', 'Training finds the pattern', 'Gives a likely outcome (a prediction)'])]
    rh = (h - 1.15) / 2
    for r, (ic, who, cells) in enumerate(rows):
        y = h - 0.5 - (r + 1) * rh
        s.icon(ic, lab_w / 2, y + rh / 2 + 0.25, 0.8)
        wt(s, lab_w / 2, y + rh / 2 - 0.45, lab_w, who, 15, 'bold')
        for i, c in enumerate(cells):
            s.box(xs[i], y + 0.12, cw, rh - 0.24, '', fill=GOLD if (r == 1 and i == 2) else PAPER, edge=INK, lw=1.8, r=0.07)
            wt(s, xs[i] + cw / 2, y + rh / 2, cw - 0.25, c, 16)
            if i < 2:
                s.arrow(xs[i] + cw + 0.05, y + rh / 2, xs[i + 1] - 0.05, y + rh / 2, lw=2.2, head=15)
    s.text(w / 2, 0.25, 'Both get better with more and more varied past cases. Both can learn old habits too.', size=14, color=MUTE)
    return s


# ------------------------------------------------------------------ the four jobs AI does
JOBS = [('magnifier', 'See and read', 'Photos, scanned forms, speech', 'Reads a receipt; spots a diseased leaf', 'Session 1'),
        ('chart', 'Predict', 'Past records with known outcomes', 'Who will repay; what will sell', 'Sessions 2 and 3'),
        ('speech', 'Understand and write language', 'Messages, documents, calls', 'Sorts a complaint; drafts a reply', 'Sessions 4 to 8'),
        ('robot', 'Act', 'A goal, tools and permissions', 'Checks stock and books a delivery', 'Sessions 9 and 10')]


@fig('x_l00_jobs')
def x_l00_jobs(w, h, **_):
    s = Scene(w, h)
    n = len(JOBS)
    gap = 0.3
    bw = (w - 0.1 - gap * (n - 1)) / n
    for i, (ic, head, goes, ex, sess) in enumerate(JOBS):
        x = 0.05 + i * (bw + gap)
        s.box(x, 0.05, bw, h - 0.1, '', fill=PAPER, edge=INK, lw=2.0, r=0.08)
        s.icon(ic, x + bw / 2, h - 0.6, 0.85)
        hh = wt(s, x + bw / 2, h - 1.35, bw - 0.3, head, 19, 'bold', va='top')
        y = h - 1.35 - hh - 0.15
        gh = wt(s, x + bw / 2, y, bw - 0.3, 'In: ' + goes, 14, color=MUTE, va='top', italic=True)
        wt(s, x + bw / 2, y - gh - 0.18, bw - 0.3, ex, 16, color=BODY, va='top')
        s.line(x + 0.25, 0.8, x + bw - 0.25, 0.8, color=HAIR, lw=1.2)
        s.text(x + bw / 2, 0.45, sess, size=17, weight='bold')
    return s


# ------------------------------------------------------------------ good and bad at
@fig('x_l00_goodbad')
def x_l00_goodbad(w, h, **_):
    s = Scene(w, h)
    good = [('bars', 'Large volumes, fast'), ('chart', 'Patterns in past records'), ('doc', 'First drafts and summaries'), ('clock', 'The same care at 2 am')]
    bad = [('flag', 'Rare cases it has seen little of'), ('question', 'Knowing what is true'), ('shield', 'Judging fairness and harm'), ('calendar', 'Keeping up when things change')]
    cw = (w - 0.3) / 2
    for c, (title, items, icon, fill) in enumerate((('Good at', good, 'check', GOLD), ('Bad at', bad, 'cross', PAPER))):
        x = 0.05 + c * (cw + 0.2)
        s.box(x, 0.05, cw, h - 0.1, '', fill=PAPER, edge=INK, lw=2.0, r=0.08)
        s.icon(icon, x + 0.5, h - 0.5, 0.6)
        s.text(x + 0.95, h - 0.5, title, size=20, weight='bold', ha='left', color=INK if c == 0 else RED)
        rh = (h - 1.1) / len(items)
        for i, (ic, t) in enumerate(items):
            yc = h - 1.0 - (i + 0.5) * rh
            if i:
                s.line(x + 0.3, yc + rh / 2, x + cw - 0.3, yc + rh / 2, color=HAIR, lw=1.0)
            wt(s, x + 0.4, yc, cw - 0.7, t, 18, ha='left')
    return s


# ------------------------------------------------------------------ where to start: cost of a mistake x ease of checking
@fig('x_l00_grid')
def x_l00_grid(w, h, **_):
    s = Scene(w, h)
    ml, mb = 0.75, 0.75
    gw, gh = w - ml - 0.1, h - mb - 0.1
    hw, hh = gw / 2, gh / 2
    cells = [  # (col, row) col 0 hard to check, 1 easy; row 0 cheap mistake (bottom), 1 costly (top)
        (1, 0, GOLD, 'Start here', 'Draft a reply; sort messages'),
        (1, 1, PAPER, 'A person checks each one', 'Flag a payment for review'),
        (0, 0, PAPER, 'Sample and spot-check', 'Summarise a long report'),
        (0, 1, PAPER, 'Keep a person in charge', 'Decide a loan or a diagnosis')]
    for c, r, fill, head, ex in cells:
        x = ml + c * hw
        y = mb + r * hh
        s.rect(x, y, hw, hh, fill=fill, edge=INK, lw=1.8)
        wt(s, x + hw / 2, y + hh / 2 + 0.3, hw - 0.3, head, 18, 'bold', color=RED if (c, r) == (0, 1) else INK)
        wt(s, x + hw / 2, y + hh / 2 - 0.35, hw - 0.3, ex, 15, color=BODY, italic=True)
    s.text(ml + gw / 2, 0.42, 'How easy is it to check the answer?', size=16, color=BODY, weight='bold')
    s.text(ml + 0.05, 0.12, 'hard', size=14, color=MUTE, ha='left')
    s.text(ml + gw - 0.05, 0.12, 'easy', size=14, color=MUTE, ha='right')
    s.text(0.3, mb + gh / 2, 'What does a mistake cost?', size=16, color=BODY, weight='bold', rot=90)
    s.text(0.62, mb + 0.2, 'little', size=14, color=MUTE, rot=90)
    s.text(0.62, mb + gh - 0.2, 'a lot', size=14, color=MUTE, rot=90)
    return s


# ------------------------------------------------------------------ industry tour (BNK-02, TEL-03, AGR-01, MFG-04, HLT-01, PUB-01)
TOUR = [('coin', 'Banking and microfinance', 'Scoring decides who gets a mobile loan, and how much', 'KCB Group, Kenya', 'Predict'),
        ('phone', 'Telecom and mobile money', 'Flags unusual M-Pesa payments for the compliance team', 'Safaricom, Kenya', 'Predict'),
        ('plant', 'Agriculture and agribusiness', 'Names cassava disease from a photo of the leaves', 'PlantVillage Nuru, Tanzania and Kenya', 'See and read'),
        ('bag', 'Manufacturing and FMCG', 'Scores shelf displays from sales reps’ photos', 'Coca-Cola HBC, Europe and Africa', 'See and read'),
        ('clinic', 'Healthcare and insurance', 'Reads clinical notes and flags possible errors', 'Penda Health, Nairobi', 'Understand language'),
        ('shield', 'Public sector', 'Cross-checks tax records to find leakage', 'Uganda Revenue Authority', 'Predict')]


@fig('x_l00_tour')
def x_l00_tour(w, h, **_):
    s = Scene(w, h)
    cols, rows = 3, 2
    gx, gy = 0.2, 0.2
    tw = (w - 0.1 - gx * (cols - 1)) / cols
    th = (h - 0.1 - gy * (rows - 1)) / rows
    for k, (ic, ind, use, ex, job) in enumerate(TOUR):
        c, r = k % cols, k // cols
        x = 0.05 + c * (tw + gx)
        y = h - 0.05 - (r + 1) * th - r * gy
        s.box(x, y, tw, th, '', fill=PAPER, edge=INK, lw=1.8, r=0.07)
        s.icon(ic, x + 0.42, y + th - 0.42, 0.58, **({'text': ''} if ic == 'coin' else {}))
        s.text(x + 0.82, y + th - 0.3, ind, size=15, weight='bold', ha='left')
        jw = K.width_in(job, 14, 'bold') + 0.25
        s.box(x + 0.82, y + th - 0.78, jw, 0.32, job, size=14, weight='bold', fill=GOLD, edge=GOLD, r=0.05)
        wt(s, x + 0.15, y + 0.88, tw - 0.3, use, 15, ha='left', color=BODY)
        s.text(x + 0.15, y + 0.25, ex, size=14, weight='bold', ha='left', color=RED)
    return s


# ------------------------------------------------------------------ a case told as a story: problem, what AI does, result, catch
@fig('x_l00_case')
def x_l00_case(w, h, problem='', does='', big='', result='', catch='', icons=('flag', 'robot', 'chart', 'question'), src='', **_):
    s = Scene(w, h)
    heads = ['The problem', 'What the AI does', 'The result', 'The catch']
    texts = [problem, does, result, catch]
    n = 4
    gap = 0.32
    bw = (w - 0.1 - gap * (n - 1)) / n
    y0 = 0.5
    bh = h - y0 - 0.05
    for i in range(n):
        x = 0.05 + i * (bw + gap)
        fill = GOLD if i == 2 else PAPER
        s.box(x, y0, bw, bh, '', fill=fill, edge=RED if i == 3 else INK, lw=2.2 if i == 3 else 1.8, r=0.08)
        s.icon(icons[i], x + 0.4, y0 + bh - 0.4, 0.55)
        s.text(x + 0.78, y0 + bh - 0.4, heads[i], size=17, weight='bold', ha='left', color=RED if i == 3 else INK)
        top = y0 + bh - 0.85
        if i == 2 and big:
            s.text(x + bw / 2, top - 0.38, big, size=38, weight='bold')
            top -= 0.9
        wt(s, x + bw / 2, top, bw - 0.3, texts[i], 16, va='top', color=INK if i == 2 else BODY)
        if i < n - 1:
            s.arrow(x + bw + 0.03, y0 + bh / 2, x + bw + gap - 0.03, y0 + bh / 2, lw=2.2, head=14)
    source(s, w, src)
    return s


# ------------------------------------------------------------------ adoption reality (ADO-01, ADO-02)
def _waffle(s, x0, y0, side, filled, fill=GOLD):
    r = side / 20
    k = 0
    for row in range(10):
        for col in range(10):
            on = k < filled
            s.circle(x0 + col * 2 * r + r, y0 + (9 - row) * 2 * r + r, r * 0.78, fill=fill if on else PAPER, edge=INK if on else GREY, lw=1.1 if on else 0.8)
            k += 1


@fig('x_l00_adoption')
def x_l00_adoption(w, h, **_):
    s = Scene(w, h)
    blocks = [(88, '88 in 100', 'organisations use AI in at least one part of the business', GOLD),
              (39, '39 in 100', 'see any effect on operating profit; most of them under 5%', GOLD),
              (5, '5 in 100', 'About this many generative AI pilots bring fast revenue gains', RED)]
    n = len(blocks)
    cw = (w - 0.1) / n
    side = 2.05
    for i, (k, big, txt, col) in enumerate(blocks):
        x = 0.05 + i * cw
        _waffle(s, x + 0.1, h - 0.05 - side, side, k, col)
        tx = x + side + 0.3
        s.text(tx, h - 0.05 - side / 2, big.replace(' in ', '\nin '), size=26, weight='bold', ha='left', color=RED if col == RED else INK)
        wt(s, x + 0.1, h - side - 0.2, cw - 0.3, txt, 15, ha='left', va='top', color=BODY)
    h2 = source(s, w, 'Treat the right-hand figure as a warning from a small study. Nearly two in three organisations are still experimenting or piloting.', y=0.04)
    source(s, w, 'Left and middle: McKinsey, The state of AI in 2025 (Nov 2025), a self-reported survey. Right: MIT NANDA, The GenAI Divide (Aug 2025), a small US sample.', y=0.1 + h2)
    return s


# ------------------------------------------------------------------ East Africa use (ADO-05)
@fig('x_l00_eastafrica')
def x_l00_eastafrica(w, h, **_):
    s = Scene(w, h)
    data = [('Global average', 16.3, False), ('Kenya', 8.1, False), ('Uganda', 6.8, True), ('Tanzania', 6.8, False), ('Rwanda', 6.3, False)]
    s.text(0.05, h - 0.22, 'Working-age people using generative AI, second half of 2025', size=16, weight='bold', ha='left')
    lab = 1.9
    bar_max = w - lab - 1.3
    top = h - 0.55
    rh = (top - 1.15) / len(data)
    for i, (name, v, hl) in enumerate(data):
        yc = top - (i + 0.5) * rh
        s.text(lab - 0.12, yc, name, size=17, ha='right', weight='bold' if hl else 'normal')
        bw = bar_max * v / 17.0
        s.rect(lab, yc - rh * 0.3, bw, rh * 0.6, fill=GOLD if hl else (INK if i == 0 else PAPER), edge=INK, lw=1.8)
        s.text(lab + bw + 0.12, yc, f'{v:g}%', size=17, weight='bold', ha='left')
    source(s, w, 'Microsoft AI Diffusion Report, H2 2025, via Citizen Digital (14 Jan 2026). Estimated from Microsoft product data.', y=0.04)
    return s


# ------------------------------------------------------------------ demonstration set-up
@fig('x_l00_demo')
def x_l00_demo(w, h, **_):
    s = Scene(w, h)
    s.box(0.05, h / 2 - 0.75, 1.75, 1.5, '', fill=PAPER, edge=INK, lw=1.8, r=0.08)
    s.icon('speech', 0.92, h / 2 + 0.25, 0.7)
    wt(s, 0.92, h / 2 - 0.4, 1.6, 'A customer message', 15, 'bold')
    lanes = [('doc', 'A rule', 'written by a person'), ('chart', 'A trained model', 'learns from examples'), ('robot', 'A chatbot', 'generative AI')]
    lx = 2.35
    lw_ = 2.95
    rh = (h - 0.2) / 3
    outs = ['Order', 'Payment', 'Complaint', 'Other']
    for i, (ic, head, sub) in enumerate(lanes):
        yc = h - 0.1 - (i + 0.5) * rh
        s.arrow(1.85, h / 2, lx - 0.05, yc, lw=1.8, head=13)
        s.box(lx, yc - rh * 0.4, lw_, rh * 0.8, '', fill=GOLD if i == 2 else PAPER, edge=INK, lw=1.8, r=0.07)
        s.icon(ic, lx + 0.4, yc, 0.5)
        s.text(lx + 0.8, yc + 0.17, head, size=16, weight='bold', ha='left')
        s.text(lx + 0.8, yc - 0.2, sub, size=14, ha='left', color=BODY)
        s.arrow(lx + lw_ + 0.05, yc, lx + lw_ + 0.45, yc, lw=1.8, head=13)
    ox = lx + lw_ + 0.55
    ow = w - ox - 0.05
    oh = (h - 0.2) / 4
    for j, o in enumerate(outs):
        y = h - 0.1 - (j + 1) * oh
        s.box(ox, y + 0.07, ow, oh - 0.14, o, size=16, weight='bold', fill=PAPER, edge=INK, lw=1.4, r=0.05)
    return s


# ------------------------------------------------------------------ three ways: the recorded results
@fig('x_l00_three')
def x_l00_three(w, h, **_):
    s = Scene(w, h)
    cols = [('doc', 'A rule', '7 of 12', 'sent to the right desk', 'Its words were chosen after reading the messages, which flatters it.', PAPER),
            ('chart', 'A trained model', '54 to 58 in 100', 'sorted right, on 40 messages', 'Learned from 32 labelled messages at a time; tested on the 8 it had not seen, 100 times.', PAPER),
            ('robot', 'A chatbot', '9 of 12', 'exactly right; 11 of 12 acceptable', 'One confident mistake. All three runs gave the same answers.', GOLD)]
    n = 3
    gap = 0.3
    bw = (w - 0.1 - gap * (n - 1)) / n
    y0 = 0.9
    bh = h - y0 - 0.05
    for i, (ic, head, big, unit, note, fill) in enumerate(cols):
        x = 0.05 + i * (bw + gap)
        s.box(x, y0, bw, bh, '', fill=fill, edge=INK, lw=2.0, r=0.08)
        s.icon(ic, x + 0.45, y0 + bh - 0.42, 0.6)
        s.text(x + 0.85, y0 + bh - 0.42, head, size=19, weight='bold', ha='left')
        s.text(x + bw / 2, y0 + bh - 1.15, big, size=32 if len(big) < 10 else 26, weight='bold')
        s.text(x + bw / 2, y0 + bh - 1.68, unit, size=15, color=INK)
        wt(s, x + bw / 2, y0 + bh - 2.05, bw - 0.35, note, 15, color=BODY, va='top')
    h2 = source(s, w, 'Trained model: 40 messages, scikit-learn 1.9.1, recorded 5 and 11 Nov 2026. A different test, so read the three side by side.', y=0.03)
    source(s, w, 'Rule and chatbot: the same 12 fictional Nile Valley Foods messages; chatbot Claude, 3 fresh sessions, 4 Nov 2026.', y=0.06 + h2)
    return s


# ------------------------------------------------------------------ message by message
MSGS = [('M38', '“Please deliver late in the afternoon, after 4pm ... 12 bags of rice.”', 'Order', 'x', 'ok', 'ok'),
        ('M10', '“I wanted to gently mention ... the third Tuesday in a row that our delivery has arrived after the shop has closed.”', 'Complaint', 'x', 'x', 'ok'),
        ('M32', '“Wow, thank you so much for delivering my sugar in the rain with no cover.”', 'Complaint', 'x', 'x', 'ok'),
        ('M14', '“I paid UGX 2,100,000 on MoMo ... still shows my account as overdue ... driver refused to deliver.”', 'Payment first', 'ok', 'ok', 'x'),
        ('M28', '“Hello, about the rice. Please call me.”', 'Other: ask', 'ok', 'x', 'unsure')]


def _mark(s, x, y, m):
    if m == 'ok':
        s.circle(x, y, 0.2, fill=GOLD, edge=INK, lw=1.6)
        s.icon('check', x, y, 0.32)
    elif m == 'x':
        s.circle(x, y, 0.2, fill=PAPER, edge=RED, lw=2.0)
        s.icon('cross', x, y, 0.3, color=RED)
    else:
        s.text(x, y, 'Unsure', size=14, weight='bold', color=BODY)


@fig('x_l00_messages')
def x_l00_messages(w, h, **_):
    s = Scene(w, h)
    cw = [0.75, 6.1, 1.55, 1.15, 1.25, 1.1]
    heads = ['', 'Message (shortened)', 'The key', 'Rule', 'Trained model', 'Chatbot']
    x0 = 0.05
    hy = h - 0.28
    xs = [x0]
    for c in cw[:-1]:
        xs.append(xs[-1] + c)
    for i, hd in enumerate(heads):
        s.text(xs[i] + cw[i] / 2 if i != 1 else xs[i] + 0.1, hy, hd, size=15, weight='bold', ha='center' if i != 1 else 'left')
    s.line(x0, h - 0.52, x0 + sum(cw), h - 0.52, color=INK, lw=1.8)
    rh = (h - 0.55 - 0.6) / len(MSGS)
    for r, (mid, txt, key, a, b, c) in enumerate(MSGS):
        y = h - 0.55 - (r + 1) * rh
        yc = y + rh / 2
        s.text(xs[0] + 0.05, yc, mid, size=15, weight='bold', ha='left')
        wt(s, xs[1] + 0.1, yc, cw[1] - 0.2, txt, 14, ha='left', color=BODY)
        s.text(xs[2] + cw[2] / 2, yc, key, size=15, weight='bold')
        for k, m in enumerate((a, b, c)):
            _mark(s, xs[3 + k] + cw[3 + k] / 2, yc, m)
        s.line(x0, y, x0 + sum(cw), y, color=HAIR, lw=1.0)
    source(s, w, 'Rule and chatbot: twelve-message record, 4 Nov 2026 (the rule sends a message to a desk). Trained model: 3 nearest neighbours, recorded 5 Nov 2026; each message was sorted by a model that learned from the other 39.', y=0.03)
    return s


# ------------------------------------------------------------------ what the demonstration teaches
@fig('x_l00_lessons')
def x_l00_lessons(w, h, **_):
    s = Scene(w, h)
    rows = [('doc', 'Rule', 'Cheap, predictable, easy to explain', 'Misses anything nobody wrote down'),
            ('chart', 'Trained model', 'Learns your own patterns from your records', 'Needs many labelled examples; 40 was too few'),
            ('robot', 'Chatbot', 'Reads meaning, sarcasm and politeness', 'Can be wrong and sound sure')]
    lab = 1.95
    cw = (w - lab - 0.1 - 0.2) / 2
    xs = [lab, lab + cw + 0.2]
    s.text(xs[0] + cw / 2, h - 0.22, 'Strength', size=17, weight='bold')
    s.text(xs[1] + cw / 2, h - 0.22, 'Weakness', size=17, weight='bold', color=RED)
    rh = (h - 0.5 - 0.55) / 3
    for i, (ic, name, good, bad) in enumerate(rows):
        y = h - 0.5 - (i + 1) * rh
        s.icon(ic, 0.45, y + rh / 2, 0.6)
        wt(s, 0.85, y + rh / 2, lab - 0.95, name, 17, 'bold', ha='left')
        s.box(xs[0], y + 0.08, cw, rh - 0.16, '', fill=GOLD if i == 2 else PAPER, edge=INK, lw=1.6, r=0.07)
        wt(s, xs[0] + cw / 2, y + rh / 2, cw - 0.3, good, 16)
        s.box(xs[1], y + 0.08, cw, rh - 0.16, '', fill=PAPER, edge=RED, lw=1.8, r=0.07)
        wt(s, xs[1] + cw / 2, y + rh / 2, cw - 0.3, bad, 16)
    return s


# ------------------------------------------------------------------ shadow AI (PPL-11, PPL-12)
@fig('x_l00_shadow')
def x_l00_shadow(w, h, **_):
    s = Scene(w, h)
    data = [(75, 'of office workers use generative AI at work', False),
            (78, 'of those users bring their own AI tools', True),
            (52, 'are reluctant to admit using it for their most important tasks', True),
            (39, 'of users have had any AI training from their employer', False),
            (54, 'would use AI tools even if not authorised (BCG)', True)]
    top = h - 0.1
    rh = (top - 1.15) / len(data)
    bx = 0.05
    bmax = 2.6
    for i, (v, txt, hl) in enumerate(data):
        yc = top - (i + 0.5) * rh
        s.rect(bx, yc - rh * 0.3, bmax, rh * 0.6, fill=PALE, edge=HAIR, lw=1.0)
        s.rect(bx, yc - rh * 0.3, bmax * v / 100, rh * 0.6, fill=GOLD if hl else INK, edge=INK, lw=1.4, z=3)
        s.text(bx + bmax * v / 100 - 0.08, yc, f'{v}%', size=16, weight='bold', ha='right', color=INK if hl else PAPER, z=7)
        wt(s, bx + bmax + 0.2, yc, w - bmax - 0.35, txt, 15, ha='left')
    h2 = source(s, w, 'BCG, AI at Work 2025 (June 2025), 10,600 people in 11 countries. Gold bars: hidden or unapproved use.', y=0.03)
    source(s, w, 'Microsoft and LinkedIn Work Trend Index (May 2024), 31,000 workers in 31 countries, none in Africa.', y=0.08 + h2)
    return s


# ------------------------------------------------------------------ your people
@fig('x_l00_people')
def x_l00_people(w, h, **_):
    s = Scene(w, h)
    quads = [('people', 'Who uses it', 'Front desk, finance clerks, analysts, managers, often on their own phones'),
             ('doc', 'Tasks that change', 'Drafting, summarising, sorting, searching, first analysis'),
             ('book', 'Skills they need', 'Clear instructions, checking the output, keeping data safe'),
             ('question', 'Fear and gain', 'Fear: their job and being found out. Gain: time and less routine')]
    gw = (w - 0.25) / 2
    gh = (h - 0.25) / 2
    for k, (ic, head, txt) in enumerate(quads):
        c, r = k % 2, k // 2
        x = 0.05 + c * (gw + 0.15)
        y = h - 0.05 - (r + 1) * gh - r * 0.15
        s.box(x, y, gw, gh, '', fill=GOLD if k == 3 else PAPER, edge=INK, lw=1.8, r=0.08)
        s.icon(ic, x + 0.45, y + gh - 0.45, 0.6)
        s.text(x + 0.85, y + gh - 0.45, head, size=18, weight='bold', ha='left')
        wt(s, x + 0.2, y + gh - 0.95, gw - 0.4, txt, 16, ha='left', va='top', color=BODY)
    return s


# ------------------------------------------------------------------ three threads across fifteen sessions
@fig('x_l00_threads')
def x_l00_threads(w, h, **_):
    s = Scene(w, h)
    lab = 2.3
    x0, x1 = lab + 0.3, w - 0.3
    step = (x1 - x0) / 14
    xs = [x0 + i * step for i in range(15)]
    ytop = h - 0.3
    for i, x in enumerate(xs):
        s.text(x, ytop, str(i), size=15, weight='bold', color=RED if i == 0 else INK)
    s.text(lab - 0.1, ytop, 'Session', size=15, color=MUTE, ha='right')
    threads = [('plant', 'Your industry', [(0, 'choose'), (1, 'tour and cases in every session from 1 to 10', 10)]),
               ('people', 'Your people', [(0, 'shadow AI'), (1, 'one people slide in every session from 1 to 10', 10), (12, 'all together')]),
               ('folder', 'Your portfolio', [(0, 'start'), (1, 'one or two entries each session', 10), (11, 'score'), (12, 'people'), (13, 'risk'), (14, 'plan')])]
    rh = (ytop - 0.35) / 3
    for t, (ic, name, marks) in enumerate(threads):
        yc = ytop - 0.35 - (t + 0.5) * rh
        s.icon(ic, 0.4, yc, 0.55)
        s.text(0.8, yc, name, size=17, weight='bold', ha='left')
        s.line(xs[0], yc, xs[-1], yc, color=HAIR, lw=6)
        for m in marks:
            if len(m) == 3:
                a, txt, b = m
                s.rect(xs[a] - 0.1, yc - 0.13, xs[b] - xs[a] + 0.2, 0.26, fill=GOLD, edge=INK, lw=1.4, z=3)
                s.text((xs[a] + xs[b]) / 2, yc - 0.42, txt, size=14, color=BODY)
            else:
                a, txt = m
                s.circle(xs[a], yc, 0.15, fill=RED if a == 0 else INK, edge=INK, lw=1.4, z=4)
                s.text(xs[a], yc + 0.36, txt, size=14, color=RED if a == 0 else BODY, weight='bold')
    return s


# ------------------------------------------------------------------ fifteen sessions in four phases
PHASE = [('A', 'Understand what AI can do', [(0, 'The AI landscape'), (1, 'AI that sees and reads'), (2, 'AI that predicts'), (3, 'Is it any good?'),
                                               (4, 'AI and language'), (5, 'How chatbots write')]),
         ('B', 'Choose it and use it well', [(6, 'The AI market'), (7, 'Working with assistants'), (8, 'AI on your documents')]),
         ('C', 'Control the risk', [(9, 'When AI goes wrong'), (10, 'AI agents that act')]),
         ('D', 'Lead the change', [(11, 'Redesigning work'), (12, 'Leading people'), (13, 'Governance and buying'), (14, 'Data and 90-day plan')])]


@fig('x_l00_route')
def x_l00_route(w, h, **_):
    s = Scene(w, h)
    widths = [3.0, 3.0, 2.75, 2.95]
    gap = (w - 0.1 - sum(widths)) / 3
    x = 0.05
    for i, (letter, name, sess) in enumerate(PHASE):
        bw = widths[i]
        s.box(x, h - 0.95, bw, 0.9, '', fill=INK if i < 3 else GOLD, edge=INK, lw=1.6, r=0.06)
        s.text(x + 0.15, h - 0.3, f'Phase {letter}', size=15, weight='bold', ha='left', color=PAPER if i < 3 else INK)
        s.text(x + 0.15, h - 0.68, name, size=15, ha='left', color=PAPER if i < 3 else INK)
        rh = 0.5
        for j, (n, t) in enumerate(sess):
            yc = h - 1.3 - j * rh
            s.circle(x + 0.25, yc, 0.19, fill=RED if n == 0 else PAPER, edge=INK, lw=1.4)
            s.text(x + 0.25, yc, str(n), size=14, weight='bold', color=PAPER if n == 0 else INK)
            s.text(x + 0.55, yc, t, size=15, ha='left', weight='bold' if n == 0 else 'normal')
        x += bw + gap
    return s


# ------------------------------------------------------------------ the AI Opportunity Portfolio page
@fig('x_l00_portfolio')
def x_l00_portfolio(w, h, compact=False, **_):
    s = Scene(w, h)
    rows = [('The use', 'Sort incoming customer messages'), ('What goes in', 'WhatsApp and email messages'),
            ('What comes out', 'Order, payment, complaint or other'), ('Who uses it', 'The customer service desk'),
            ('How we would know it works', 'A person checks a sample each week'), ('Which job (Session 0)', 'Understand language')]
    if compact:
        rows = rows[:1] + rows[2:3] + rows[4:]
    size = 14 if compact else 15
    s.rect(0.05, 0.05, w - 0.1, h - 0.1, fill=PAPER, edge=INK, lw=2.0)
    s.rect(0.05, h - 0.62, w - 0.1, 0.57, fill=INK, edge=INK, lw=0, z=3)
    s.text(0.25, h - 0.335, 'AI Opportunity Portfolio, entry 1', size=16, weight='bold', color=PAPER, ha='left', z=6)
    lw_ = 2.25 if compact else 2.75
    rh = (h - 1.2) / len(rows)
    for i, (lab, val) in enumerate(rows):
        y = h - 0.72 - (i + 1) * rh
        yc = y + rh / 2
        wt(s, 0.2, yc, lw_ - 0.2, lab, size, 'bold', ha='left', color=MUTE)
        wt(s, lw_ + 0.1, yc, w - lw_ - 0.3, val, size, ha='left', italic=True, color=BODY if i < len(rows) - 1 else RED)
        s.line(0.2, y, w - 0.2, y, color=HAIR, lw=1.0)
    s.text(w - 0.2, 0.2, 'Example: Nile Valley Foods (fictional)', size=14, color=MUTE, ha='right', italic=True)
    return s
