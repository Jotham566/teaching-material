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


def mt(s, x, y, t, **kw):
    """Maths text (matplotlib mathtext), not passed through clean()."""
    return s.text(x, y, t, **kw)


def keyboard_top3():
    """Top three next tokens from the recorded keyboard run (demo_runs/s05/keyboard_run_thank_you.txt)."""
    import re
    txt = (Path(__file__).resolve().parent.parent / 'demo_runs' / 's05' / 'keyboard_run_thank_you.txt').read_text()
    rows = re.findall(r"^\s+'([^']+)'\s+([0-9.]+)%", txt, re.M)
    return [(w, float(p) / 100) for w, p in rows[:3]]


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
    top3 = keyboard_top3()
    # the phone
    s.box(0.1, 0.15, 3.1, h - 0.3, '', fill=PALE, edge=INK, lw=2.2, r=0.25)
    put(s, 1.65, h - 0.55, 'Phone keyboard', size=17, weight='bold', color=RED)
    s.box(0.3, h - 1.75, 2.7, 0.8, 'Thank you for your', size=15, fill=PAPER, lw=1.4, r=0.05)
    for k, (wd, p) in enumerate(top3):
        s.box(0.3, h - 2.4 - k * 0.62, 2.7, 0.52, '', fill=GOLD if k == 0 else PAPER, lw=1.4, r=0.05)
        put(s, 0.5, h - 2.4 - k * 0.62 + 0.26, show(wd), size=16, weight='bold', ha='left')
        put(s, 2.8, h - 2.4 - k * 0.62 + 0.26, '%.0f%%' % (100 * p), size=16, weight='bold', ha='right')
    put(s, 1.65, 0.72, 'Three suggestions: the top three\nfrom a recorded GPT-2 run', size=14, color=BODY)
    put(s, 1.65, 0.3, 'Tap one, and it suggests again', size=14, color=BODY)
    # the language model loop
    bx, bw, bh, gap = 3.75, 3.85, 0.75, 0.28
    labs = ['1. The text so far goes in', '2. The model gives a logit (a score)\nto each of its 50,257 tokens', '3. One token is picked', '4. It joins the text. Repeat']
    put(s, bx + bw / 2, h - 0.3, 'Language model: the same loop', size=17, weight='bold', color=RED)
    y = h - 0.65 - bh
    for k, lab in enumerate(labs):
        s.box(bx, y, bw, bh, lab, size=15, weight='bold', fill=GOLD if k == 0 else PAPER)
        if k < 3:
            s.arrow(bx + bw / 2, y, bx + bw / 2, y - gap, color=RED, lw=2.4, head=12)
        y -= bh + gap
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
    heads = ['Token', 'Logit', '2.72 to\nthe logit', 'Probability']
    xs = [0.1]
    for c in colw:
        xs.append(xs[-1] + c)
    top = h - 0.15
    rh = 0.62
    for j, t in enumerate(heads):
        s.box(xs[j], top - 0.8, colw[j], 0.8, t, size=16, weight='bold', fill=PALE, edge=INK, lw=1.2, r=0.02)
    for i, ((nm, v), e, sh) in enumerate(zip(rows, ex, shares)):
        y = top - 0.8 - (i + 1) * rh
        s.box(xs[0], y, colw[0], rh, nm, size=18, weight='bold', r=0.02, lw=1.2)
        s.box(xs[1], y, colw[1], rh, str(v), size=20, r=0.02, lw=1.2)
        s.box(xs[2], y, colw[2], rh, '%.2f' % e, size=20, r=0.02, lw=1.2)
        s.box(xs[3], y, colw[3], rh, '', r=0.02, lw=1.2)
        s.rect(xs[3] + 0.1, y + 0.14, (colw[3] - 1.2) * sh / 100 * 1.35, rh - 0.28, fill=GOLD if i == 0 else GREY, edge=INK, lw=1.0)
        put(s, xs[3] + colw[3] - 0.1, y + rh / 2, '%d%%' % sh, size=20, weight='bold', ha='right')
    y = top - 0.8 - 3 * rh - 0.27
    put(s, xs[2] + colw[2] / 2, y, 'Total %.2f' % tot, size=17, weight='bold')
    put(s, xs[3] + colw[3] / 2, y, 'Each one divided by %.2f' % tot, size=16)
    put(s, 0.1, 1.12, 'Formula (softmax):', size=15, weight='bold', color=RED, ha='left')
    mt(s, 2.15, 1.15, r'$p_i = e^{z_i} \,/\, \sum_j e^{z_j}$', size=20, ha='left')
    put(s, 0.1, 0.5, 'p = probability of token i, z = its logit, e = 2.72 (rounded), \u03a3 = add up over all tokens', size=14, ha='left')
    put(s, 0.1, 0.17, 'Toy logits 2, 1, 0: 7.39 / 11.11 = 67%. The probabilities add up to 100%.', size=14, color=MUTE, ha='left')
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
        rh = (top - 0.95) / 6
        for i, (wd, p) in enumerate(rows2):
            yc = top - rh * (i + 0.5)
            last = i == 5
            put(s, x0 + 1.25, yc, wd if last else show(wd), size=15 if last else 16, ha='right', color=MUTE if last else INK)
            bw = (pw - 2.45) * p
            s.rect(x0 + 1.35, yc - rh * 0.3, max(bw, 0.02), rh * 0.6, fill=PAPER if last else (GOLD if i == 0 else GREY), edge=INK, lw=1.0)
            lab = '%.0f%%' % (100 * p) if p >= 0.095 else '%.1f%%' % (100 * p)
            put(s, x0 + 1.45 + bw, yc, lab, size=15, ha='left', weight='bold' if last else 'normal')
    put(s, 0.1, 0.45, 'Formula (softmax with temperature):', size=15, weight='bold', color=RED, ha='left')
    mt(s, 4.6, 0.45, r'$p_i = e^{z_i / T} \,/\, \sum_j e^{z_j / T}$', size=19, ha='left')
    put(s, 8.6, 0.45, 'T = temperature, z = logit.\nT = 1 is plain softmax.', size=14, ha='left', color=BODY)
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
        put(s, gx - 0.12, gy + 12 * cell / 2, 'block 1 to 12 (up)', size=14, rot=90, ha='right')
        put(s, gx + 6 * cell, gy - 0.22, 'head 1 to 12 (right)', size=14)
        put(s, gx + 6 * cell, h - 0.65, note, size=15, color=BODY)
    return s


@fig('x_t05_toy_attention')
def toy_attention(w, h, **_):
    s = Scene(w, h)
    words = [('supplier', 0.5, 2), ('invoice', 1.5, 6), ('manager', 1.0, 4)]
    q = 2
    sc = [q * k for _, k, _ in words]
    ex = [math.exp(x) for x in sc]
    tot = sum(ex)
    shr = [round(100 * e / tot) for e in ex]
    prod = [p / 100 * v for p, (_, _, v) in zip(shr, words)]
    colw = [1.8, 1.0, 2.1, 1.7, 1.8, 1.1, 1.8]
    heads = ['Earlier token', 'Key', 'Score =\nquery 2 x key', '2.72 to\nthe score', 'Attention\nweight', 'Value', 'Weight\nx value']
    xs = [0.1]
    for c in colw:
        xs.append(xs[-1] + c)
    top = h - 0.05
    hh = 0.7
    for j, t_ in enumerate(heads):
        s.box(xs[j], top - hh, colw[j], hh, t_, size=15, weight='bold', fill=PALE, r=0.02, lw=1.2)
    rh = 0.5
    for i, ((wd, k, v), a, e, p, pr) in enumerate(zip(words, sc, ex, shr, prod)):
        y = top - hh - (i + 1) * rh
        hl = i == 1
        vals = [wd, '%.1f' % k, '%.1f' % a, '%.2f' % e, '%d%%' % p, str(v), '%.2f' % pr]
        for j, t_ in enumerate(vals):
            s.box(xs[j], y, colw[j], rh, t_, size=18, weight='bold' if (hl and j in (0, 4)) else 'normal', fill=GOLD if (hl and j == 4) else PAPER, r=0.02, lw=1.2)
    y = top - hh - 3 * rh - 0.22
    put(s, xs[3] + colw[3] / 2, y, 'Total %.1f' % tot, size=16, weight='bold')
    put(s, xs[6] + colw[6] / 2, y, 'Sum %.2f' % sum(prod), size=16, weight='bold', color=RED)
    put(s, 0.1, 1.08, 'Output for "it" = 0.09 x 2 + 0.67 x 6 + 0.24 x 4 = %.2f. It leans towards the value of "invoice" (6).' % sum(prod), size=15, weight='bold', ha='left')
    mt(s, 0.1, 0.68, r'Formula (scaled dot-product attention):  $\mathrm{Attention}(Q,K,V) = \mathrm{softmax}(QK^{T} / \sqrt{d_k})\,V$', size=17, ha='left')
    put(s, 0.1, 0.32, 'Q, K, V = queries, keys, values. Toy: one number each, so d_k = 1 and \u221ad_k = 1. Real GPT-2 head: d_k = 64, scores divided by 8.', size=14, ha='left', color=BODY)
    return s


# ---------------------------------------------------------------------------------------------------------------- the stack
@fig('x_t05_stack')
def stack(w, h, **_):
    s = Scene(w, h)
    c = R['gpt2_config']
    items = [('Your text', 'Please pay the invoice within thirty', PAPER),
             ('Tokens', 'cut by the tokenizer; each has an id', GOLD),
             ('Embeddings', 'numbers per token (Session 4), plus position', PAPER),
             ('%d blocks' % c['layers'], 'each: self-attention, feed-forward (%d heads)' % c['heads'], GOLD),
             ('Logits', 'one score for each of %s tokens' % format(c['vocab'], ','), PAPER),
             ('Probabilities', 'softmax turns the logits into a distribution', GOLD)]
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
    put(s, w / 2, h - 1.35, 'The model never saw this company. Its top five next tokens (San, Los, Salt: American places):', size=16, color=BODY)
    n = 5
    cw = (w - 0.4 - 0.15 * (n - 1)) / n
    for i, (wd, p) in enumerate(d['top10'][:n]):
        x = 0.2 + i * (cw + 0.15)
        s.box(x, h - 2.5, cw, 0.85, '%s\n%.1f%%' % (show(wd), 100 * p), size=17, weight='bold')
    s.box(0.2, 0.35, w - 0.4, 1.0, '', fill=PAPER, edge=RED, lw=2.2, dash=True)
    put(s, w / 2, 0.85, 'The real answer, Jinja, is not here. A fluent answer still comes out.\nNothing in this loop checks the facts.', size=18, weight='bold', color=RED)
    return s


# ---------------------------------------------------------------------------------------------------------------- how it learns: the Session 0 loop on text
@fig('x_t05_learn_loop')
def learn_loop(w, h, **_):
    s = Scene(w, h)
    d = R['next'][1]
    top3 = d['top10'][:3]
    days = [p for wd, p in d['top10'] if wd.strip() == 'days'][0]
    bw, bh, gap = 3.55, 2.1, 0.55
    y0 = 2.1
    xs = [0.1 + i * (bw + gap) for i in range(3)]
    heads = ['1. Hide the next token', '2. The model predicts', '3. Measure the loss, adjust']
    for i, x in enumerate(xs):
        s.box(x, y0, bw, bh, '', fill=PAPER, edge=INK, lw=1.8)
        s.box(x, y0 + bh - 0.5, bw, 0.5, heads[i], size=17, weight='bold', fill=GOLD, edge=INK, lw=1.8, r=0.05)
        if i < 2:
            s.arrow(x + bw + 0.04, y0 + bh / 2, xs[i + 1] - 0.04, y0 + bh / 2, color=RED, lw=2.6)
    # step 1
    put(s, xs[0] + bw / 2, y0 + 1.2, 'Please pay the invoice\nwithin thirty', size=17, weight='bold')
    s.box(xs[0] + 1.0, y0 + 0.34, 1.55, 0.44, '? (hidden)', size=16, weight='bold', fill=PALE, dash=True)
    put(s, xs[0] + bw / 2, y0 + 0.16, 'The text holds its own answer: days', size=14, color=BODY)
    # step 2
    for k, (wd, p) in enumerate(top3):
        yc = y0 + bh - 0.8 - k * 0.33
        hit = wd.strip() == 'days'
        put(s, xs[1] + 1.05, yc, show(wd), size=16, ha='right', weight='bold' if hit else 'normal')
        s.rect(xs[1] + 1.2, yc - 0.12, max(1.5 * p / 0.7, 0.03), 0.24, fill=GOLD if hit else GREY, edge=INK, lw=1.0)
        put(s, xs[1] + 1.3 + 1.5 * p / 0.7, yc, '%.0f%%' % (100 * p), size=15, ha='left', weight='bold' if hit else 'normal')
    put(s, xs[1] + bw / 2, y0 + 0.17, 'True token, days: only %.0f%%' % (100 * days), size=15, weight='bold', color=RED)
    # step 3
    put(s, xs[2] + bw / 2, y0 + 1.15, 'loss  L = \u2212ln p(correct token)', size=16, weight='bold')
    mt(s, xs[2] + bw / 2, y0 + 0.75, r'$L = -\ln 0.18 \approx 1.71$', size=18, ha='center')
    put(s, xs[2] + bw / 2, y0 + 0.33, 'Gradient descent adjusts the weights\nso days gets more probability', size=14, color=BODY)
    # bottom band
    yb = 1.75
    s.arrow(xs[2] + bw / 2, y0 - 0.02, xs[2] + bw / 2, yb, color=RED, lw=2.0, head=10)
    s.arrow(xs[2] + bw / 2, yb, xs[0] + bw / 2, yb, color=RED, lw=2.0, head=10)
    s.arrow(xs[0] + bw / 2, yb, xs[0] + bw / 2, y0 - 0.02, color=RED, lw=2.0, head=10)
    put(s, w / 2, 1.42, 'Repeat on the next sentence in the training text, billions of times (the Session 0 loop).', size=15, weight='bold')
    mt(s, 0.1, 0.95, r'Probability of a whole text:  $P(x_1 \ldots x_n) = \prod_{t=1}^{n} P(x_t \mid x_1 \ldots x_{t-1})$', size=16, ha='left')
    put(s, 0.1, 0.55, 'x_t = the token at position t; \u03a0 = multiply over all positions. Training minimises the average loss, which raises this probability.', size=14, ha='left', color=BODY)
    put(s, 0.1, 0.2, 'No one writes labels: the next token is the label (self-supervised learning).', size=15, color=RED, weight='bold', ha='left')
    return s


# ---------------------------------------------------------------------------------------------------------------- a peek inside one block
@fig('x_t05_block_peek')
def block_peek(w, h, **_):
    s = Scene(w, h)
    X = json.loads((Path(__file__).resolve().parent.parent / 'demo_runs' / 's07' / 'gpt2_count.json').read_text())
    inv = X['invoice_piece_numbers']
    top = h - 0.1
    # in
    s.box(0.1, 1.95, 2.35, 1.95, '', fill=PAPER, edge=INK, lw=1.8)
    put(s, 1.275, 3.62, 'Embedding in', size=17, weight='bold')
    put(s, 1.275, 3.18, 'token "invoice":', size=14, color=BODY)
    for k, v in enumerate(inv):
        s.box(0.28 + k * 0.5, 2.32, 0.5, 0.5, ('%.2f' % v).replace('-', '\u2212').replace('0.', '.'), size=14, r=0.02, lw=1.1, fill=GOLD if k == 0 else PAPER)
    put(s, 1.275, 2.62 - 0.55, '... 768 numbers', size=14, color=BODY)
    # block container
    bx, bwid = 2.9, 6.3
    s.box(bx, 1.5, bwid, 2.55, '', fill=PALE, edge=RED, lw=2.4, dash=True)
    put(s, bx + bwid / 2, 3.83, 'ONE TRANSFORMER BLOCK, opened up', size=17, weight='bold', color=RED)
    s.arrow(2.5, 2.92, bx + 0.28, 2.92, color=RED, lw=2.6)
    # attention
    ax0 = bx + 0.3
    s.box(ax0, 1.65, 2.55, 1.8, '', fill=PAPER, edge=INK, lw=1.8)
    put(s, ax0 + 1.275, 3.2, 'Self-attention', size=18, weight='bold')
    put(s, ax0 + 1.275, 2.8, 'each token looks back\nand blends earlier tokens', size=14, color=BODY)
    for k in range(4):
        s.circle(ax0 + 0.45 + k * 0.55, 2.3, 0.13, fill=GOLD if k == 3 else PAPER, edge=INK, lw=1.4, z=4)
    for k in range(3):
        s.arrow(ax0 + 0.45 + 3 * 0.55 - 0.1, 2.38, ax0 + 0.45 + k * 0.55 + 0.1, 2.38, color=RED, lw=1.5, head=7, rad=0.0)
    put(s, ax0 + 1.275, 1.82, '2.4 million weights', size=14, weight='bold')
    s.arrow(ax0 + 2.55, 2.75, ax0 + 2.95, 2.75, color=RED, lw=2.4, head=12)
    # neurons
    nx0 = ax0 + 2.95
    s.box(nx0, 1.65, 2.55, 1.8, '', fill=PAPER, edge=INK, lw=1.8)
    put(s, nx0 + 1.275, 3.25, 'Feed-forward network', size=15, weight='bold')
    put(s, nx0 + 1.275, 2.9, 'neurons, 3,072 wide', size=14, color=BODY)
    ins = [nx0 + 0.45, 2.22 + 0.0]
    for a in range(3):
        for b_ in range(4):
            s.line(nx0 + 0.5, 2.2 + a * 0.18, nx0 + 1.2, 2.05 + b_ * 0.16 + 0.15, color=GREY, lw=0.9, z=2)
    for a in range(3):
        s.circle(nx0 + 0.5, 2.2 + a * 0.18, 0.06, fill=PAPER, edge=INK, lw=1.1, z=4)
    for b_ in range(4):
        s.circle(nx0 + 1.2, 2.2 + b_ * 0.16 - 0.03, 0.06, fill=GOLD, edge=INK, lw=1.1, z=4)
    put(s, nx0 + 1.9, 2.35, '...', size=18, weight='bold')
    put(s, nx0 + 1.275, 1.82, '4.7 million weights', size=14, weight='bold')
    s.arrow(bx + bwid, 2.92, bx + bwid + 0.4, 2.92, color=RED, lw=2.6)
    # out
    ox = bx + bwid + 0.4
    s.box(ox, 1.95, w - ox - 0.1, 1.95, '', fill=PAPER, edge=INK, lw=1.8)
    put(s, ox + (w - ox - 0.1) / 2, 3.45, 'Numbers out', size=17, weight='bold')
    put(s, ox + (w - ox - 0.1) / 2, 2.75, 'still 768 per token,\nnow enriched', size=14, color=BODY)
    # the stack of 12
    put(s, 0.1, 0.95, 'GPT-2 small stacks 12 of these, one after another:', size=16, weight='bold', ha='left')
    bwid2 = 0.43
    x = 5.9
    for k in range(12):
        s.box(x + k * (bwid2 + 0.05), 0.62, bwid2, 0.5, str(k + 1), size=14, weight='bold', r=0.04, fill=GOLD if k in (0, 11) else PAPER, lw=1.4)
    s.arrow(x + 12 * (bwid2 + 0.05), 0.91, w - 0.08, 0.91, color=RED, lw=2.0, head=10)
    put(s, 5.9 + 6 * (bwid2 + 0.05), 0.3, '7,087,872 weights in each block', size=15, color=BODY)
    put(s, 0.1, 0.38, 'then 50,257 logits and softmax', size=15, color=BODY, ha='left')
    return s


# ---------------------------------------------------------------------------------------------------------------- token id selects a row
@fig('x_t05_lookup')
def lookup(w, h, **_):
    s = Scene(w, h)
    X = json.loads((Path(__file__).resolve().parent.parent / 'demo_runs' / 's07' / 'gpt2_count.json').read_text())
    inv = X['invoice_piece_numbers']
    vocab, nums = X['vocab'], X['numbers_per_token']
    pid = X['sentence_ids'][3]
    # left: the piece and its id
    s.box(0.1, h - 1.55, 2.1, 0.7, 'invoice', size=20, weight='bold', fill=GOLD, lw=1.8)
    put(s, 1.15, h - 0.65, 'a token', size=15, color=BODY)
    s.arrow(1.15, h - 1.6, 1.15, h - 2.2, color=RED, lw=2.2, head=12)
    s.box(0.1, h - 3.0, 2.1, 0.75, 'id %s' % format(pid, ','), size=20, weight='bold', fill=PAPER, lw=1.8)
    put(s, 1.15, h - 3.35, 'its token id', size=14, color=BODY)
    # the table
    tx, tw = 3.4, w - 3.6
    put(s, tx + tw / 2, h - 0.3, 'The embedding matrix (lookup table): one row per token, %s rows' % format(vocab, ','), size=18, weight='bold')
    rows = [('row 1', ['.02', '-.01', '.05', '.00']), ('row 2', ['.11', '.03', '-.07', '.04']), ('...', None),
            ('row %s' % format(pid, ','), [('%.2f' % v).replace('0.', '.') for v in inv]), ('...', None), ('row %s' % format(vocab, ','), ['-.01', '.06', '.02', '-.09'])]
    top = h - 0.65
    rh = 0.4
    for i, (lab, vals) in enumerate(rows):
        y = top - (i + 1) * rh
        hot = (i == 3)
        if vals is None:
            put(s, tx + 0.9, y + rh / 2, lab, size=20, weight='bold', color=MUTE)
            continue
        s.box(tx, y + 0.03, 2.3, rh - 0.06, lab, size=15, weight='bold' if hot else 'normal', fill=GOLD if hot else PAPER, r=0.03, lw=1.6 if hot else 1.0)
        for k, v in enumerate(vals):
            s.box(tx + 2.4 + k * 0.95, y + 0.03, 0.9, rh - 0.06, v.replace('-', '−'), size=15, fill=GOLD if hot else PAPER, r=0.03, lw=1.6 if hot else 1.0)
        put(s, tx + 2.4 + 4 * 0.95 + 0.2, y + rh / 2, '... %d numbers' % nums, size=15, color=BODY, ha='left')
    hy = top - 4 * rh + rh / 2
    s.arrow(2.25, h - 2.62, tx - 0.05, hy, color=RED, lw=2.4, head=12, rad=0.0)
    mt(s, tx + 0.1, 0.72, r'Formula (input to block 1):  $x_t = E[\mathrm{id}_t] + P[t]$', size=18, ha='left')
    put(s, tx + 0.1, 0.3, 'E = token table, P = position table (1,024 rows); x_t = 768 numbers. Both learned.', size=14, ha='left', color=BODY)
    return s


# ---------------------------------------------------------------------------------------------------------------- sampling: greedy, top-k, top-p
@fig('x_t05_sampling')
def sampling(w, h, **_):
    s = Scene(w, h)
    rows = R['next'][1]['top10'][:5]
    cum, c = [], 0.0
    for _, p in rows:
        c += p
        cum.append(c)
    k_keep = [i < 2 for i in range(5)]
    p_keep, run = [], 0.0
    for i, (_, p) in enumerate(rows):
        p_keep.append(run < 0.9)
        run += p
    colw = [1.7, 3.0, 1.7, 1.7, 1.8, 1.9]
    heads = ['Token', 'Probability', 'Running\ntotal', 'Greedy\ndecoding', 'Top-k\n(k = 2)', 'Top-p\n(p = 0.9)']
    xs = [0.1]
    for cw_ in colw:
        xs.append(xs[-1] + cw_)
    top = h - 0.05
    hh = 0.7
    for j, t_ in enumerate(heads):
        s.box(xs[j], top - hh, colw[j], hh, t_, size=15, weight='bold', fill=PALE, r=0.02, lw=1.2)
    rh = 0.4
    for i, (wd, p) in enumerate(rows):
        y = top - hh - (i + 1) * rh
        s.box(xs[0], y, colw[0], rh, show(wd), size=16, weight='bold', r=0.02, lw=1.0)
        s.box(xs[1], y, colw[1], rh, '', r=0.02, lw=1.0)
        s.rect(xs[1] + 0.08, y + 0.1, max((colw[1] - 1.2) * p / 0.7, 0.03), rh - 0.2, fill=GREY, edge=INK, lw=0.9)
        put(s, xs[1] + colw[1] - 0.1, y + rh / 2, '%.1f%%' % (100 * p), size=15, ha='right')
        s.box(xs[2], y, colw[2], rh, '%.1f%%' % (100 * cum[i]), size=15, r=0.02, lw=1.0)
        for j, keep in ((3, i == 0), (4, k_keep[i]), (5, p_keep[i])):
            s.box(xs[j], y, colw[j], rh, 'kept' if keep else 'dropped', size=15, weight='bold' if keep else 'normal', fill=GOLD if keep else '#F1F1F1', color=INK if keep else MUTE, r=0.02, lw=1.0)
    k2 = sum(p for _, p in rows[:2])
    p3 = sum(p for _, p in rows[:3])
    put(s, 0.1, 1.27, 'Top-k: keep the k most probable tokens.   Top-p: keep the fewest top tokens whose probabilities add up to at least p.', size=15, ha='left', weight='bold')
    put(s, 0.1, 0.8, 'After the cut, rescale and draw one token at random:', size=15, ha='left')
    mt(s, 5.0, 0.8, r"$p'_i = p_i \,/\, \sum_{j \in \mathrm{kept}} p_j$", size=17, ha='left')
    put(s, 8.6, 0.8, 'kept = tokens left after the cut', size=14, ha='left', color=BODY)
    put(s, 0.1, 0.3, 'Top-k 2: "(" %.0f%%, days %.0f%%.   Top-p 0.9 keeps 3 tokens (97%% in total): "(" %.0f%%, days %.0f%%, "-" %.0f%%.' % (
        100 * rows[0][1] / k2, 100 * rows[1][1] / k2, 100 * rows[0][1] / p3, 100 * rows[1][1] / p3, 100 * rows[2][1] / p3), size=15, ha='left', weight='bold', color=RED)
    return s


# ---------------------------------------------------------------------------------------------------------------- the classroom analogy for self-attention
@fig('x_t05_classroom')
def classroom(w, h, **_):
    s = Scene(w, h)
    pupils = [('Amina', 'blue pen', 15), ('Brian', 'red pen', 70), ('Chipo', 'ruler', 5), ('David', 'lunch box', 10)]
    n = len(pupils)
    cw = 1.7
    gap = (w - 0.2 - n * cw) / (n - 1)
    ex, ey, ew, eh = w / 2 - 1.75, h - 1.0, 3.5, 0.85
    s.box(ex, ey, ew, eh, 'You are Esther. Your query:\n"Who has a red pen?"', size=15, weight='bold', fill=GOLD, lw=2)
    for i, (nm, item, pct) in enumerate(pupils):
        x0 = 0.1 + i * (cw + gap)
        xc = x0 + cw / 2
        hot = pct >= 50
        s.icon('person', xc, 0.95, 0.9)
        put(s, xc, 0.3, nm, size=15, weight='bold')
        s.box(x0, 1.55, cw, 0.75, 'Key:\n%s' % item, size=15, fill=GOLD if hot else PAPER, lw=1.6)
        s.line(w / 2 + (i - 1.5) * 0.7, ey, xc, 2.3, color=RED if hot else GREY, lw=1 + pct / 6.0, z=1)
        sx = w / 2 + (i - 1.5) * 0.7
        tx = sx + (xc - sx) * 0.63
        s.box(tx - 0.4, 2.85 - 0.0, 0.8, 0.38, '%d%%' % pct, size=15, weight='bold', color=RED if hot else INK, fill=PAPER, edge=PAPER, lw=0.5, z=5)
    return s
