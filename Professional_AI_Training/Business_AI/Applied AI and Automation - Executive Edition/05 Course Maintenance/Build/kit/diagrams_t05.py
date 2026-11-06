"""Session 5 figures: tokens, next-word probability, temperature, attention. All numbers come from demo_runs/s05/results.json (GPT-2 small, recorded 6 November 2026).
Slide use:  dict(kind='t05_two_runs')  ->  figure 'x_t05_two_runs'.
"""
import json
import math
import textwrap
from pathlib import Path

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD, fig

R = json.loads((Path(__file__).resolve().parent.parent / 'demo_runs' / 's05' / 'results.json').read_text())


def clean(s):
    return s.replace('$', r'\$')


def shade(v, lo=(255, 255, 255), hi=(174, 37, 37)):
    v = max(0.0, min(1.0, v))
    return '#%02X%02X%02X' % tuple(int(a + (b - a) * v) for a, b in zip(lo, hi))


def gold_shade(v):
    return shade(v, (255, 255, 255), (224, 190, 54))


def put(s, x, y, t, **kw):
    return s.text(x, y, clean(t), **kw)


def show(piece):
    return piece.strip() or '(space)'


# ---------------------------------------------------------------------------------------------------------------- same question twice
@fig('x_t05_two_runs')
def two_runs(w, h, **_):
    s = Scene(w, h)
    pt = R['temp']['prompt']
    s.box(w / 2 - 3.6, h - 0.95, 7.2, 0.7, pt, size=19, weight='bold', fill=GOLD, edge=INK)
    runs = [R['temp']['settings'][1]['samples'][0], R['temp']['settings'][1]['samples'][5]]
    pw = 5.5
    for i, txt in enumerate(runs):
        x0 = 0.3 + i * (pw + 0.4)
        s.arrow(w / 2 + (i - 0.5) * 1.6, h - 1.0, x0 + pw / 2, h - 1.75, color=INK, lw=2)
        s.box(x0, 0.75, pw, h - 2.5, '', fill=PAPER, edge=INK, lw=1.8)
        put(s, x0 + 0.2, h - 2.05, 'Run %d' % (i + 1), size=18, weight='bold', color=RED, ha='left')
        lines = textwrap.wrap('...' + pt.split()[-1] + txt, 36)
        put(s, x0 + 0.2, 1.45, '\n'.join(lines[:3]), size=18, ha='left', va='center')
    put(s, w / 2, 0.38, 'Same model, same words in, temperature 1.0. GPT-2, recorded run, 6 November 2026.', size=15, color=MUTE)
    return s


# ---------------------------------------------------------------------------------------------------------------- tokens as bricks
@fig('x_t05_tokens')
def tokens(w, h, picks=(0, 1), **_):
    s = Scene(w, h)
    size = 16
    y = h - 0.3
    for k in picks:
        t = R['tokens'][k]
        put(s, 0.1, y - 0.2, t['text'], size=15, color=MUTE, ha='left')
        y -= 0.62
        x = 0.1
        row_h = 0.52
        for i, p in enumerate(t['pieces']):
            lab = show(p)
            bw = 0.13 * len(lab) + 0.3
            if x + bw > w - 0.1:
                x = 0.1
                y -= row_h + 0.1
            s.box(x, y - row_h + 0.05, bw, row_h - 0.08, lab, size=size, fill=GOLD if i % 2 == 0 else PAPER, edge=INK, lw=1.4, r=0.05)
            x += bw + 0.06
        y -= row_h
        put(s, 0.1, y - 0.22, '%d words, %d tokens' % (t['n_words'], len(t['pieces'])), size=16, weight='bold', color=RED, ha='left')
        y -= 0.55
    return s


@fig('x_t05_token_counts')
def token_counts(w, h, **_):
    s = Scene(w, h)
    names = ['Place and company names', 'Invoice with an amount', 'Contract wording', 'Long rare word', 'Swahili order']
    n = len(names)
    lab_w = 3.4
    x0 = lab_w + 0.2
    scale = (w - x0 - 0.9) / 18.0
    top = h - 0.75
    s.box(x0, h - 0.5, 0.3, 0.3, '', fill=GREY, edge=GREY)
    put(s, x0 + 0.4, h - 0.35, 'words', size=16, ha='left')
    s.box(x0 + 1.6, h - 0.5, 0.3, 0.3, '', fill=GOLD, edge=INK)
    put(s, x0 + 2.0, h - 0.35, 'tokens (what the model counts)', size=16, ha='left')
    rh = (top - 0.1) / n
    for i, (nm, t) in enumerate(zip(names, R['tokens'])):
        yc = top - rh * (i + 0.5)
        put(s, lab_w, yc, nm, size=17, ha='right')
        nw, nt = t['n_words'], len(t['pieces'])
        s.rect(x0, yc + 0.03, nw * scale, 0.3, fill=GREY, edge=GREY, lw=0)
        put(s, x0 + nw * scale + 0.1, yc + 0.18, str(nw), size=16, ha='left')
        s.rect(x0, yc - 0.33, nt * scale, 0.3, fill=GOLD, edge=INK, lw=1.2)
        put(s, x0 + nt * scale + 0.1, yc - 0.18, str(nt), size=16, weight='bold', ha='left')
    return s


# ---------------------------------------------------------------------------------------------------------------- the loop
@fig('x_t05_next_loop')
def next_loop(w, h, **_):
    s = Scene(w, h)
    bw, bh = 3.3, 1.15
    xs = [0.2, w - bw - 0.2]
    ys = [h - 2.0, 0.95]
    s.box(xs[0], ys[0], bw, bh, '1. The text so far', size=18, weight='bold', fill=GOLD)
    s.box(xs[1], ys[0], bw, bh, '2. The model scores\nevery piece it knows', size=17, weight='bold')
    s.box(xs[1], ys[1], bw, bh, '3. One piece is picked', size=18, weight='bold')
    s.box(xs[0], ys[1], bw, bh, '4. It joins the text', size=18, weight='bold')
    s.arrow(xs[0] + bw, ys[0] + bh / 2, xs[1], ys[0] + bh / 2, color=RED, lw=2.6)
    s.arrow(xs[1] + bw / 2, ys[0], xs[1] + bw / 2, ys[1] + bh, color=RED, lw=2.6)
    s.arrow(xs[1], ys[1] + bh / 2, xs[0] + bw, ys[1] + bh / 2, color=RED, lw=2.6)
    s.arrow(xs[0] + bw / 2, ys[1] + bh, xs[0] + bw / 2, ys[0], color=RED, lw=2.6)
    put(s, w / 2, (ys[0] + ys[1] + bh) / 2, 'Repeat\nuntil it stops', size=20, weight='bold')
    put(s, xs[0] + bw / 2, ys[0] + bh + 0.35, 'Please pay the invoice\nwithin thirty', size=16, color=BODY)
    put(s, xs[1] + bw / 2, ys[0] + bh + 0.35, 'GPT-2 knows 50,257 pieces', size=16, color=BODY)
    put(s, xs[1] + bw / 2, ys[1] - 0.35, '" days"', size=16, color=BODY)
    put(s, xs[0] + bw / 2, ys[1] - 0.35, '... within thirty days', size=16, color=BODY)
    return s


# ---------------------------------------------------------------------------------------------------------------- softmax by hand
@fig('x_t05_softmax_hand')
def softmax_hand(w, h, **_):
    s = Scene(w, h)
    rows = [('days', 2), ('weeks', 1), ('minutes', 0)]
    ex = [math.exp(v) for _, v in rows]
    tot = sum(ex)
    shares = [round(100 * e / tot) for e in ex]
    colw = [1.45, 0.95, 1.9, 3.2]
    heads = ['Piece', 'Score', 'Raise 2.72\nto the score', 'Share of the total']
    xs = [0.1]
    for c in colw:
        xs.append(xs[-1] + c)
    top = h - 0.15
    rh = 0.78
    for j, t in enumerate(heads):
        s.box(xs[j], top - 0.95, colw[j], 0.95, t, size=16, weight='bold', fill=PALE, edge=INK, lw=1.2, r=0.02)
    for i, ((nm, v), e, sh) in enumerate(zip(rows, ex, shares)):
        y = top - 0.95 - (i + 1) * rh
        s.box(xs[0], y, colw[0], rh, nm, size=18, weight='bold', r=0.02, lw=1.2)
        s.box(xs[1], y, colw[1], rh, str(v), size=20, r=0.02, lw=1.2)
        s.box(xs[2], y, colw[2], rh, '%.2f' % e, size=20, r=0.02, lw=1.2)
        s.box(xs[3], y, colw[3], rh, '', r=0.02, lw=1.2)
        s.rect(xs[3] + 0.1, y + 0.18, (colw[3] - 1.2) * sh / 100 * 1.35, rh - 0.36, fill=GOLD if i == 0 else GREY, edge=INK, lw=1.0)
        put(s, xs[3] + colw[3] - 0.1, y + rh / 2, '%d%%' % sh, size=20, weight='bold', ha='right')
    y = top - 0.95 - 3 * rh - 0.3
    put(s, xs[2] + colw[2] / 2, y, 'Total %.2f' % tot, size=18, weight='bold')
    put(s, xs[3] + colw[3] / 2, y, 'Each one divided by %.2f' % tot, size=16)
    put(s, 0.1, 0.35, 'Toy numbers. The shares always add up to 100.', size=16, color=MUTE, ha='left')
    return s


# ---------------------------------------------------------------------------------------------------------------- real next-word bars
@fig('x_t05_next_bars')
def next_bars(w, h, idx=0, hl=(), n=10, title=True, **_):
    s = Scene(w, h)
    d = R['next'][idx]
    top = h - (0.75 if title else 0.1)
    if title:
        put(s, 0.1, h - 0.35, d['prompt'] + ' ...', size=18, weight='bold', ha='left')
    rows = d['top10'][:n]
    rh = (top - 0.1) / n
    lab_w = 1.6
    mx = max(p for _, p in rows)
    for i, (wd, p) in enumerate(rows):
        yc = top - rh * (i + 0.5)
        is_hl = wd.strip() in hl
        put(s, lab_w, yc, show(wd), size=17, ha='right', weight='bold' if is_hl else 'normal')
        bw = (w - lab_w - 1.5) * p / mx
        s.rect(lab_w + 0.15, yc - rh * 0.33, bw, rh * 0.66, fill=GOLD if is_hl else GREY, edge=INK, lw=1.0)
        put(s, lab_w + 0.25 + bw, yc, '%.1f%%' % (100 * p), size=17, ha='left', weight='bold' if is_hl else 'normal', color=RED if is_hl else INK)
    return s


@fig('x_t05_next_three')
def next_three(w, h, **_):
    s = Scene(w, h)
    panels = [(1, 'Please pay the invoice\nwithin thirty ...', 'Few good choices'), (3, 'The customer was angry\nbecause the delivery was ...', 'Many fair choices'),
              (2, 'Nile Valley Foods is a food\ndistributor based in ...', 'No idea, many guesses')]
    pw = (w - 0.4) / 3
    for k, (idx, ttl, tag) in enumerate(panels):
        x0 = k * (pw + 0.2)
        d = R['next'][idx]
        put(s, x0 + pw / 2, h - 0.42, ttl, size=16, weight='bold')
        rows = d['top10'][:6]
        top = h - 1.0
        rh = (top - 0.65) / 6
        mx = 0.7
        for i, (wd, p) in enumerate(rows):
            yc = top - rh * (i + 0.5)
            put(s, x0 + 1.3, yc, show(wd), size=16, ha='right')
            bw = (pw - 2.5) * p / mx
            s.rect(x0 + 1.4, yc - rh * 0.3, max(bw, 0.02), rh * 0.6, fill=GOLD if i == 0 else GREY, edge=INK, lw=1.0)
            put(s, x0 + 1.5 + bw, yc, '%.0f%%' % (100 * p) if p >= 0.1 else '%.1f%%' % (100 * p), size=15, ha='left')
        put(s, x0 + pw / 2, 0.3, tag, size=17, weight='bold', color=RED)
    return s


# ---------------------------------------------------------------------------------------------------------------- temperature
@fig('x_t05_temp_bars')
def temp_bars(w, h, **_):
    s = Scene(w, h)
    pw = (w - 0.4) / 3
    names = {0.2: 'Temperature 0.2\nlow: stays on the favourite', 1.0: 'Temperature 1.0\nthe model as trained', 1.8: 'Temperature 1.8\nhigh: flattens the odds'}
    for k, st in enumerate(R['temp']['settings']):
        x0 = k * (pw + 0.2)
        put(s, x0 + pw / 2, h - 0.42, names[st['T']], size=16, weight='bold')
        rows = st['top8'][:5]
        rest = 1 - sum(p for _, p in rows)
        rows2 = [(wd, p) for wd, p in rows] + [('all other\n50,252', rest)]
        top = h - 0.95
        rh = (top - 0.1) / 6
        for i, (wd, p) in enumerate(rows2):
            yc = top - rh * (i + 0.5)
            last = i == 5
            put(s, x0 + 1.25, yc, wd if last else show(wd), size=15 if last else 16, ha='right', color=MUTE if last else INK)
            bw = (pw - 2.45) * p
            s.rect(x0 + 1.35, yc - rh * 0.3, max(bw, 0.02), rh * 0.6, fill=PAPER if last else (GOLD if i == 0 else GREY), edge=INK, lw=1.0)
            lab = '%.0f%%' % (100 * p) if p >= 0.095 else '%.1f%%' % (100 * p)
            put(s, x0 + 1.45 + bw, yc, lab, size=15, ha='left', weight='bold' if last else 'normal')
    return s


@fig('x_t05_temp_samples')
def temp_samples(w, h, **_):
    s = Scene(w, h)
    pw = (w - 0.4) / 3
    for k, st in enumerate(R['temp']['settings']):
        x0 = k * (pw + 0.2)
        s.box(x0, 0.05, pw, h - 0.1, '', fill=PAPER, edge=INK, lw=1.6, r=0.05)
        put(s, x0 + 0.15, h - 0.35, 'Temperature %s' % st['T'], size=18, weight='bold', color=RED, ha='left')
        y = h - 0.75
        for sm in st['samples'][:3]:
            lines = textwrap.wrap(sm.strip(), 36)[:3]
            put(s, x0 + 0.15, y - 0.35, '\n'.join(lines), size=15, ha='left')
            y -= 1.0
            s.line(x0 + 0.1, y + 0.3, x0 + pw - 0.1, y + 0.3, color=HAIR, lw=1)
    return s


# ---------------------------------------------------------------------------------------------------------------- attention
ATT = R['attn_head']['matrix']
TOK = R['attn_tokens']


@fig('x_t05_attn_arrows')
def attn_arrows(w, h, **_):
    s = Scene(w, h)
    n = len(TOK)
    row = ATT[-1]
    top = h - 0.15
    rh = (h - 0.3) / n
    lx = 2.0
    s.box(w - 1.6, h / 2 - 0.4, 1.4, 0.8, 'it', size=24, weight='bold', fill=GOLD, lw=2)
    for i, t in enumerate(TOK[:-1]):
        yc = top - rh * (i + 0.5)
        put(s, lx, yc, t.strip(), size=17, ha='right', weight='bold' if row[i] > 0.5 else 'normal')
        lw = 1 + 14 * row[i]
        s.line(lx + 0.15, yc, w - 1.65, h / 2, color=RED if row[i] > 0.3 else GREY, lw=lw)
        if row[i] >= 0.04:
            put(s, lx + 1.4, yc + 0.0, '%d%%' % round(100 * row[i]), size=15, weight='bold', color=RED if row[i] > 0.3 else BODY, ha='left')
    return s


@fig('x_t05_attn_heat')
def attn_heat(w, h, **_):
    s = Scene(w, h)
    n = len(TOK)
    cell = 0.31
    lab_w = 1.05
    gx = lab_w + 0.1
    gy = 0.15
    for i in range(n):
        yc = gy + (n - 1 - i) * cell + cell / 2
        put(s, gx - 0.08, yc, TOK[i].strip(), size=14, ha='right', weight='bold' if i == n - 1 else 'normal')
        put(s, gx + i * cell + cell / 2, gy + n * cell + 0.07, TOK[i].strip(), size=14, ha='center', va='bottom', rot=90)
        for j in range(n):
            v = ATT[i][j]
            s.rect(gx + j * cell, gy + (n - 1 - i) * cell, cell, cell, fill=shade(v) if j <= i else '#F1F1F1', edge=HAIR, lw=0.6, z=2)
    s.rect(gx, gy + 0, n * cell, cell, fill='none', edge=RED, lw=2.8, z=5)
    put(s, gx + n * cell + 0.25, gy + cell / 2 + 0.55, 'Row for "it"', size=18, weight='bold', color=RED, ha='left')
    put(s, gx + n * cell + 0.25, gy + cell / 2 + 0.15, '85% on "invoice"', size=18, weight='bold', ha='left')
    put(s, gx + n * cell + 0.25, gy + 2.3, 'Darker red =\nmore attention', size=16, ha='left', color=BODY)
    put(s, gx + n * cell + 0.25, gy + 3.1, 'Row: the word that\nis looking', size=16, ha='left', color=BODY)
    return s


@fig('x_t05_head_grid')
def head_grid(w, h, **_):
    s = Scene(w, h)
    cell = 0.265
    panels = [('Share on the first word', R['attn_grid_first'], 'Dark: resting on "The"'), ('Share on "invoice"', R['attn_grid_invoice'], 'Only one head is dark')]
    for k, (ttl, g, note) in enumerate(panels):
        gx = 0.55 + k * 3.85
        gy = 0.55
        put(s, gx + 6 * cell, h - 0.3, ttl, size=16, weight='bold')
        for L in range(12):
            for H in range(12):
                v = g[L][H]
                s.rect(gx + H * cell, gy + (11 - L) * cell, cell, cell, fill=shade(v), edge=HAIR, lw=0.5, z=2)
        s.rect(gx + 3 * cell, gy + (11 - 4) * cell, cell, cell, fill='none', edge=GOLD, lw=3.2, z=5)
        put(s, gx - 0.12, gy + 12 * cell / 2, 'layer 1 to 12 (up)', size=14, rot=90, ha='right')
        put(s, gx + 6 * cell, gy - 0.22, 'head 1 to 12 (right)', size=14)
        put(s, gx + 6 * cell, h - 0.65, note, size=15, color=BODY)
    return s


@fig('x_t05_toy_attention')
def toy_attention(w, h, **_):
    s = Scene(w, h)
    words = [('supplier', 0.5), ('invoice', 1.5), ('manager', 1.0)]
    q = 2
    sc = [q * v for _, v in words]
    ex = [math.exp(x) for x in sc]
    tot = sum(ex)
    sh = [e / tot for e in ex]
    shr = [round(100 * x) for x in sh]
    colw = [1.9, 1.5, 2.1, 2.2, 1.9, 2.2]
    heads = ['Earlier word', 'Its number', 'Score = 2 x number', 'Raise 2.72\nto the score', 'Share', 'Share x number']
    xs = [0.1]
    for c in colw:
        xs.append(xs[-1] + c)
    top = h - 0.1
    hh = 0.8
    for j, t in enumerate(heads):
        s.box(xs[j], top - hh, colw[j], hh, t, size=15, weight='bold', fill=PALE, r=0.02, lw=1.2)
    rh = 0.7
    prod = [x * v for x, (_, v) in zip(sh, words)]
    for i, ((wd, v), a, e, p, pr) in enumerate(zip(words, sc, ex, shr, prod)):
        y = top - hh - (i + 1) * rh
        hl = i == 1
        vals = [wd, '%.1f' % v, '%.1f' % a, '%.2f' % e, '%d%%' % p, '%.2f' % (p / 100 * v + 1e-9)]
        for j, t in enumerate(vals):
            s.box(xs[j], y, colw[j], rh, t, size=19, weight='bold' if (hl and j in (0, 4)) else 'normal', fill=GOLD if (hl and j == 4) else PAPER, r=0.02, lw=1.2)
    y = top - hh - 3 * rh - 0.35
    put(s, xs[3] + colw[3] / 2, y, 'Total %.1f' % tot, size=17, weight='bold')
    put(s, xs[5] + colw[5] / 2 - 0.3, y, 'Add up: about 1.3', size=19, weight='bold', color=RED)
    put(s, 0.1, 0.55, 'The word "it" asks with the number 2. The answer 1.3 sits close to the number of "invoice" (1.5).', size=17, ha='left')
    put(s, 0.1, 0.12, 'Toy numbers. A real model uses hundreds of numbers per word, learned in training.', size=15, color=MUTE, ha='left')
    return s


# ---------------------------------------------------------------------------------------------------------------- the stack
@fig('x_t05_stack')
def stack(w, h, **_):
    s = Scene(w, h)
    c = R['gpt2_config']
    items = [('Your text', 'Please pay the invoice within thirty', PAPER),
             ('Tokens', 'cut into pieces, each with an id', GOLD),
             ('Numbers', 'a list of numbers per piece (Session 4)', PAPER),
             ('Attention + processing', '%d times over, %d heads each' % (c['layers'], c['heads']), GOLD),
             ('Scores', 'one for each of %s pieces' % format(c['vocab'], ','), PAPER),
             ('Percentages', 'softmax turns scores into shares', GOLD)]
    n = len(items)
    bh = (h - 0.1) / n - 0.12
    for i, (a, b, f) in enumerate(items):
        y = h - 0.05 - (i + 1) * (bh + 0.12) + 0.12
        s.box(0.1, y, w - 0.2, bh, '', fill=f, edge=INK, lw=1.6)
        put(s, 0.3, y + bh / 2, a, size=18, weight='bold', ha='left')
        put(s, 3.0, y + bh / 2, b, size=16, ha='left', color=BODY)
        if i < n - 1:
            s.arrow(w - 0.5, y, w - 0.5, y - 0.1, color=RED, lw=2, head=10)
    return s


@fig('x_t05_sure_wrong')
def sure_wrong(w, h, **_):
    s = Scene(w, h)
    d = R['next'][2]
    s.box(0.2, h - 1.0, w - 0.4, 0.7, 'Nile Valley Foods is a food distributor based in ...', size=19, weight='bold', fill=GOLD)
    put(s, w / 2, h - 1.35, 'The model never saw this company. Its top five next pieces (San, Los, Salt: American places):', size=16, color=BODY)
    n = 5
    cw = (w - 0.4 - 0.15 * (n - 1)) / n
    for i, (wd, p) in enumerate(d['top10'][:n]):
        x = 0.2 + i * (cw + 0.15)
        s.box(x, h - 2.5, cw, 0.85, '%s\n%.1f%%' % (show(wd), 100 * p), size=17, weight='bold')
    s.box(0.2, 0.35, w - 0.4, 1.0, '', fill=PAPER, edge=RED, lw=2.2, dash=True)
    put(s, w / 2, 0.85, 'The real answer, Jinja, is not here. A fluent answer still comes out.\nNothing in this loop checks the facts.', size=18, weight='bold', color=RED)
    return s
