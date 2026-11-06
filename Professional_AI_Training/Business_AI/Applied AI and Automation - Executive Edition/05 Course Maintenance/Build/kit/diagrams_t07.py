"""Figures for Session 7: open weights, file formats, size and running cost.

Kinds (use as dict(kind='t07_...')): openness, licence, weightsfile, memorysum, scale, levels, container, sizegrid, sizes, quality, options, breakeven.
Real data drawn here: the numbers in weightsfile are the first values of layer 0 of SmolLM2-135M-Instruct; sizes, sizegrid and quality come from
demo_runs/s07_sizes_run.md (measured 6 November 2026) and the Hugging Face file listings read the same day.
"""
from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD, fig
import slidekit as K


def _wrap(s, cx, cy, width, text, size, weight='normal', color=INK, ha='center'):
    lines = K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', width)
    return s.text(cx, cy, '\n'.join(lines), size=size, weight=weight, color=color, ha=ha)


def _nlines(text, size, width, kind='regular'):
    return len(K.wrap(text, size, kind, width))


# ----------------------------------------------------------------------------------------------- openness
@fig('x_t07_openness')
def openness(w, h, **_):
    s = Scene(w, h)
    c0 = 2.5
    cw = (w - c0 - 0.05) / 4
    heads = ['Weights\ndownloadable', 'Training\ncode', 'Data\ninformation', 'Licence with\nno use limits']
    rows = [('Open Source AI\n(OSI 1.0)', ['yes', 'yes', 'yes', 'yes'], GOLD),
            ('Open weights', ['yes', 'varies', 'varies', 'varies'], PAPER),
            ('Closed model,\nrented', ['no', 'no', 'no', 'no'], PAPER)]
    top = h - 0.05
    hh = 0.95
    for j, t in enumerate(heads):
        s.text(c0 + j * cw + cw / 2, top - hh / 2, t, size=15, weight='bold')
    s.line(0.05, top - hh, w - 0.05, top - hh, color=INK, lw=2.2)
    rh = (h - 0.1 - hh) / 3
    for i, (lab, vals, fill) in enumerate(rows):
        y = top - hh - (i + 1) * rh
        s.box(0.05, y + 0.1, c0 - 0.2, rh - 0.2, lab, size=18, weight='bold', fill=fill, edge=INK, lw=1.8)
        for j, v in enumerate(vals):
            cx = c0 + j * cw + cw / 2
            if v == 'yes':
                s.circle(cx, y + rh / 2, 0.36, fill=GOLD, edge=INK, lw=2)
                s.text(cx, y + rh / 2, 'yes', size=15, weight='bold')
            elif v == 'no':
                s.circle(cx, y + rh / 2, 0.36, fill=PAPER, edge=INK, lw=1.4)
                s.text(cx, y + rh / 2, 'no', size=15, color=MUTE)
            else:
                s.circle(cx, y + rh / 2, 0.36, fill=PAPER, edge=RED, lw=2, z=2)
                s.text(cx, y + rh / 2, 'varies', size=14, weight='bold', color=RED)
        s.line(0.05, y, w - 0.05, y, color=HAIR, lw=1)
    return s


# ----------------------------------------------------------------------------------------------- licence
@fig('x_t07_licence')
def licence(w, h, **_):
    s = Scene(w, h)
    bw = 2.6
    s.box(0.05, h / 2 - 0.9, bw, 1.8, 'Weights file\nfree to download', size=20, weight='bold', fill=GOLD, lw=2.2)
    s.box(w - bw - 0.05, h / 2 - 0.9, bw, 1.8, 'Your use\nin the company', size=20, weight='bold', lw=2.2)
    gx0, gx1 = bw + 0.7, w - bw - 0.7
    conds = ['Over 700 million monthly users? Ask Meta for a licence',
             'Show "Built with Llama" when you distribute it',
             'Follow the Acceptable Use Policy',
             'A model made with it, if shared, has a name starting "Llama"']
    n = len(conds)
    gh = (h - 0.1 - 0.15 * (n - 1)) / n
    s.arrow(0.05 + bw + 0.05, h / 2, gx0 - 0.08, h / 2, lw=2.6, head=18)
    s.arrow(gx1 + 0.08, h / 2, w - bw - 0.1, h / 2, lw=2.6, head=18)
    for i, c in enumerate(conds):
        y = h - 0.05 - (i + 1) * gh - i * 0.15
        s.box(gx0, y, gx1 - gx0, gh, '', fill=PAPER, edge=RED, lw=2)
        s.icon('lock', gx0 + 0.45, y + gh / 2, 0.6)
        _wrap(s, gx0 + 0.9 + (gx1 - gx0 - 1.0) / 2, y + gh / 2, gx1 - gx0 - 1.2, c, 16)
    return s


# ----------------------------------------------------------------------------------------------- weights file
@fig('x_t07_weightsfile')
def weightsfile(w, h, **_):
    s = Scene(w, h)
    s.icon('doc', 0.55, h - 0.6, 0.8)
    s.text(1.1, h - 0.45, 'model.safetensors', size=22, weight='bold', ha='left')
    s.text(1.1, h - 0.88, 'SmolLM2-135M, 16-bit: 269 MB', size=16, color=BODY, ha='left')
    vals = [[-0.075, 0.162, -0.099, -0.730, 1.172, -0.119],
            [-0.099, 0.398, 0.027, -1.273, 0.816, -0.355],
            [-0.133, 0.104, -0.283, -0.346, 0.945, -0.090],
            [-0.184, 0.268, 0.041, -0.562, 0.033, -0.009],
            [-0.066, -0.279, 0.120, 0.605, -0.283, 0.235]]
    cw, ch = 1.1, 0.46
    x0 = (w - 6 * cw - 0.7) / 2
    y0 = h - 1.25 - 5 * ch
    for r, row in enumerate(vals):
        for c, v in enumerate(row):
            s.box(x0 + c * cw, y0 + (4 - r) * ch, cw, ch, f'{v:.3f}'.replace('-', '−'), size=15, r=0.02, lw=1.2,
                  fill=GOLD if (r, c) == (1, 3) else PAPER)
    s.text(x0 + 6 * cw + 0.3, y0 + 2.5 * ch, '...', size=20, weight='bold')
    s.text(x0 + 3 * cw, y0 - 0.22, '...', size=20, weight='bold')
    s.text(w / 2, 0.62, '134,515,008 numbers like these', size=22, weight='bold')
    s.text(w / 2, 0.22, 'Real values from the first layer. Each number is one weight.', size=15, color=BODY)
    return s


# ----------------------------------------------------------------------------------------------- memory sum
@fig('x_t07_memorysum')
def memorysum(w, h, **_):
    s = Scene(w, h)
    bh = 1.25
    y = h - 0.15 - bh
    widths = [2.6, 0.5, 1.9, 0.5, 2.0]
    gap = (w - 0.1 - sum(widths)) / 4
    xs = []
    x = 0.05
    for ww in widths:
        xs.append(x)
        x += ww + gap
    s.box(xs[0], y, widths[0], bh, '134.5 million\nnumbers', size=19, weight='bold')
    s.text(xs[1] + widths[1] / 2, y + bh / 2, '×', size=34, weight='bold')
    s.box(xs[2], y, widths[2], bh, '4 bytes\neach', size=19, weight='bold')
    s.text(xs[3] + widths[3] / 2, y + bh / 2, '=', size=34, weight='bold')
    s.box(xs[4], y, widths[4], bh, '538 MB\nfile', size=19, weight='bold', fill=GOLD, lw=2.2)
    s.text(w / 2, y - 0.45, 'Parameters  ×  bytes per number  =  size of the weights', size=17, color=BODY)
    # one number = 4 bytes = 32 bits
    yb = 1.55
    s.text(0.05, yb + 0.95, 'One number in 32-bit form', size=16, weight='bold', ha='left')
    for i in range(4):
        s.box(0.05 + i * 1.15, yb, 1.1, 0.7, '1 byte', size=15, r=0.03, fill=GOLD if i == 0 else PAPER)
    s.text(0.05 + 4.6 + 0.2, yb + 0.35, '= 4 bytes = 32 bits', size=16, ha='left', color=BODY)
    s.text(0.05, 0.75, 'In 16-bit form: 2 bytes each, so half. 269 MB.', size=17, ha='left', weight='bold')
    s.text(0.05, 0.3, 'Measured file: 538,090,376 bytes. The small extra is the file header.', size=15, ha='left', color=BODY)
    return s


# ----------------------------------------------------------------------------------------------- scale
@fig('x_t07_scale')
def scale(w, h, **_):
    s = Scene(w, h)
    groups = [('1 billion', 2, 0.5), ('7 billion', 14, 3.5), ('70 billion', 140, 35)]
    x0 = 2.1
    maxw = w - x0 - 1.7
    gh = (h - 0.55) / 3
    s.text(0.05, h - 0.2, 'Model size', size=16, weight='bold', ha='left', color=MUTE)
    s.tag(x0, h - 0.4, '16-bit', size=15, fill=GOLD, color=INK)
    s.tag(x0 + 1.4, h - 0.4, '4-bit', size=15, fill=INK)
    for i, (lab, a, b) in enumerate(groups):
        top = h - 0.6 - i * gh
        s.text(0.05, top - gh / 2 + 0.05, lab + '\nnumbers', size=17, weight='bold', ha='left')
        for k, (val, fill) in enumerate(((a, GOLD), (b, PAPER))):
            bwid = max(0.06, maxw * val / 140)
            yy = top - 0.55 - k * 0.55
            s.rect(x0, yy, bwid, 0.45, fill=fill, edge=INK, lw=1.6)
            s.text(x0 + bwid + 0.12, yy + 0.22, (f'{val:g} GB'), size=17, weight='bold', ha='left')
    return s


# ----------------------------------------------------------------------------------------------- levels (quantisation)
@fig('x_t07_levels')
def levels(w, h, **_):
    s = Scene(w, h)
    x0, x1 = 0.55, w - 0.55
    v = 0.37

    def px(val):
        return x0 + (val + 1) / 2 * (x1 - x0)

    rowsy = [h - 1.6, h / 2 - 0.15, 1.05]
    specs = [('32-bit: almost any value', None), ('8-bit: 256 allowed values', 256), ('4-bit: 16 allowed values', 16)]
    s.text(0.05, h - 0.3, 'The number to store: 0.37', size=19, weight='bold', ha='left')
    for (lab, n), y in zip(specs, rowsy):
        s.text(0.05, y + 0.62, lab, size=17, weight='bold', ha='left')
        s.line(x0, y, x1, y, color=INK, lw=2)
        if n is None:
            s.circle(px(v), y, 0.09, fill=GOLD, edge=INK, lw=2, z=5)
            s.text(px(v), y - 0.42, 'stored as 0.37', size=16, color=BODY)
            continue
        step = 2 / (n - 1)
        k = round((v + 1) / step)
        near = -1 + k * step
        count = n if n <= 16 else 64
        if n <= 16:
            for j in range(n):
                xx = px(-1 + j * step)
                s.line(xx, y - 0.14, xx, y + 0.14, color=INK, lw=1.8)
        else:
            for j in range(0, n, 4):
                xx = px(-1 + j * step)
                s.line(xx, y - 0.1, xx, y + 0.1, color=GREY, lw=0.8)
        s.circle(px(near), y, 0.1, fill=GOLD, edge=INK, lw=2, z=5)
        s.text(px(near), y - 0.45, f'stored as {near:.2f}', size=16, weight='bold', color=RED if n == 16 else BODY)
    s.text(x0, 0.35, '−1', size=16, color=MUTE)
    s.text(x1, 0.35, '1', size=16, color=MUTE)
    return s


# ----------------------------------------------------------------------------------------------- container vs compression
@fig('x_t07_container')
def container(w, h, **_):
    s = Scene(w, h)
    n = 3
    gap = 0.3
    bw = (w - 0.1 - gap * (n - 1)) / n
    top = h - 0.05
    s.text(0.05, top - 0.2, 'CONTAINER: how the file is packed', size=17, weight='bold', ha='left', color=RED)
    items = [('Safetensors', 'The numbers, in a file built to load safely'),
             ('GGUF', 'The numbers plus settings, in one file for local tools'),
             ('ONNX', 'The numbers plus the calculation, to move between tools')]
    bh = 1.5
    for i, (hd, tx) in enumerate(items):
        x = 0.05 + i * (bw + gap)
        y = top - 0.5 - bh
        s.box(x, y, bw, bh, '', fill=PAPER, edge=INK, lw=2.4)
        s.text(x + bw / 2, y + bh - 0.32, hd, size=22, weight='bold')
        _wrap(s, x + bw / 2, y + 0.62, bw - 0.3, tx, 16, color=BODY)
        s.arrow(x + bw / 2, y - 0.05, x + bw / 2, y - 0.32, lw=2, head=14)
    yb = 0.1
    s.text(0.05, 1.5, 'COMPRESSION: how many bits each number gets (quantisation)', size=17, weight='bold', ha='left', color=RED)
    labs = ['32-bit', '16-bit', '8-bit', '4-bit']
    cw = (w - 0.1 - 0.2 * 3) / 4
    for i, lab in enumerate(labs):
        s.box(0.05 + i * (cw + 0.2), yb + 0.05, cw, 0.7, lab, size=20, weight='bold', fill=GOLD if i == 3 else PAPER, lw=1.8)
    s.text(w / 2, 1.1, 'Any container can hold numbers at any of these', size=16, color=BODY)
    return s


# ----------------------------------------------------------------------------------------------- size grid (published listings)
@fig('x_t07_sizegrid')
def sizegrid(w, h, **_):
    s = Scene(w, h)
    c0 = 1.7
    cw = (w - c0 - 0.05) / 3
    heads = ['Safetensors', 'GGUF', 'ONNX']
    rows = [('32-bit', ['538*', '-', '540']), ('16-bit', ['269', '271', '270']), ('8-bit', ['135*', '145', '137']),
            ('4-bit', ['76*', '105', '118 to 182'])]
    top = h - 0.05
    hh = 0.6
    for j, t in enumerate(heads):
        s.text(c0 + j * cw + cw / 2, top - hh / 2, t, size=20, weight='bold')
    s.line(0.05, top - hh, w - 0.05, top - hh, color=INK, lw=2.2)
    foot = 0.8
    rh = (h - hh - foot - 0.05) / 4
    for i, (lab, vals) in enumerate(rows):
        y = top - hh - (i + 1) * rh
        if i == 1:
            s.rect(0.05, y + 0.04, w - 0.1, rh - 0.08, fill=GOLD, edge=GOLD, lw=0, z=1)
        s.text(0.2, y + rh / 2, lab, size=20, weight='bold', ha='left')
        for j, v in enumerate(vals):
            s.text(c0 + j * cw + cw / 2, y + rh / 2, v + (' MB' if v not in ('-',) else ''), size=20, color=INK if v != '-' else MUTE, weight='bold' if i == 1 else 'normal')
        s.line(0.05, y, w - 0.05, y, color=HAIR, lw=1)
    s.text(0.05, 0.62, 'File size in MB for the same small model (SmolLM2-135M). Read from the published file lists, 6 Nov 2026.', size=14, ha='left', color=BODY)
    s.text(0.05, 0.22, '* our own conversion with torch. "-" = no such file listed.', size=14, ha='left', color=MUTE)
    return s


# ----------------------------------------------------------------------------------------------- sizes as proportional boxes
@fig('x_t07_sizes')
def sizes(w, h, **_):
    s = Scene(w, h)
    data = [('32-bit', 538.1, '100%'), ('16-bit', 269.1, '50%'), ('8-bit', 135.0, '25%'), ('4-bit', 75.8, '14%')]
    gap = 0.22
    # side of the largest square so that the row fits the width and height
    ratio = [(d[1] / 538.1) ** 0.5 for d in data]
    smax = min((w - 0.1 - gap * 3) / sum(ratio), h - 1.35)
    x = 0.05
    for (lab, mb, pct), r in zip(data, ratio):
        side = smax * r
        s.box(x, 1.2, side, side, '', fill=GOLD if lab == '32-bit' else PAPER, edge=INK, lw=2, r=0.03)
        s.text(x + side / 2, 0.9, lab, size=17, weight='bold')
        s.text(x + side / 2, 0.5, f'{mb:.0f} MB', size=17)
        s.text(x + side / 2, 0.15, pct, size=14, color=MUTE)
        x += side + gap
    return s


# ----------------------------------------------------------------------------------------------- quality
@fig('x_t07_quality')
def quality(w, h, **_):
    s = Scene(w, h)
    pw = (w - 0.4) / 2
    panels = [('32-bit', [(' U', 11), (' known', 10), (' the', 8)], False), ('Our rough 4-bit', [(' the', 56), (' a', 6), (' U', 3)], True)]
    s.text(w / 2, h - 0.25, 'After "The capital city of Uganda is", the three likeliest next words', size=16, weight='bold')
    for p, (lab, items, hl) in enumerate(panels):
        x0 = 0.05 + p * (pw + 0.3)
        s.box(x0, 1.55, pw, h - 2.35, '', fill=PAPER, edge=INK, lw=2.0 if hl else 1.4, r=0.05)
        s.text(x0 + 0.2, h - 1.15, lab + (' model' if lab=='32-bit' else ''), size=18, weight='bold', ha='left', color=RED if hl else INK)
        for k, (word, pc) in enumerate(items):
            yy = h - 1.8 - k * 0.55
            s.text(x0 + 0.2, yy, word.strip() or word, size=16, ha='left')
            bwid = (pw - 2.3) * pc / 56
            s.rect(x0 + 1.25, yy - 0.16, max(0.05, bwid), 0.32, fill=GOLD if hl else PALE, edge=INK, lw=1.4)
            s.text(x0 + 1.25 + max(0.05, bwid) + 0.1, yy, f'{pc}%', size=15, ha='left', weight='bold')
    s.text(0.05, 1.15, 'Average miss over three sentences (lower is better)', size=15, weight='bold', ha='left')
    cw = (w - 0.1 - 0.15 * 3) / 4
    for i, (lab, v) in enumerate([('32-bit', '4.57'), ('16-bit', '4.57'), ('8-bit', '4.56'), ('Rough 4-bit', '5.09')]):
        s.box(0.05 + i * (cw + 0.15), 0.1, cw, 0.8, f'{lab}  {v}', size=17 if len(lab)<8 else 15, weight='bold', fill=GOLD if lab == '4-bit' else PAPER, lw=1.6)
    return s


# ----------------------------------------------------------------------------------------------- rent / host / own
@fig('x_t07_options')
def options(w, h, **_):
    s = Scene(w, h)
    c0 = 2.3
    cw = (w - c0 - 0.05) / 3
    heads = [('Rent', 'cloud'), ('Host', 'gear'), ('Own', 'home')]
    rows = [('Who runs it', ['The vendor', 'You, on a server you rent', 'You, on your own machines']),
            ('Your data goes to', ['The vendor’s servers', 'The server you chose', 'Stays in your building']),
            ('You pay for', ['Each use', 'The server, busy or idle', 'Machines, power, people']),
            ('The model is', ['Closed or open', 'Open weights', 'Open weights'])]
    top = h - 0.05
    hh = 0.95
    for j, (t, ic) in enumerate(heads):
        cx = c0 + j * cw + cw / 2
        s.icon(ic, cx - 0.85, top - hh / 2, 0.7)
        s.text(cx + 0.1, top - hh / 2, t, size=24, weight='bold')
    s.line(0.05, top - hh, w - 0.05, top - hh, color=INK, lw=2.2)
    rh = (h - 0.1 - hh) / 4
    for i, (lab, vals) in enumerate(rows):
        y = top - hh - (i + 1) * rh
        s.text(0.1, y + rh / 2, lab, size=17, weight='bold', ha='left')
        for j, v in enumerate(vals):
            _wrap(s, c0 + j * cw + cw / 2, y + rh / 2, cw - 0.3, v, 17, color=BODY)
        s.line(0.05, y, w - 0.05, y, color=HAIR, lw=1)
    return s


# ----------------------------------------------------------------------------------------------- break-even
@fig('x_t07_breakeven')
def breakeven(w, h, **_):
    s = Scene(w, h)
    ax0, ay0 = 1.05, 0.95
    ax1, ay1 = w - 0.4, h - 0.55
    s.line(ax0, ay0, ax0, ay1, color=INK, lw=2)
    s.line(ax0, ay0, ax1, ay0, color=INK, lw=2)
    xmax, ymax = 6000, 6.0

    def X(v): return ax0 + (ax1 - ax0) * v / xmax

    def Y(v): return ay0 + (ay1 - ay0) * v / ymax
    for yv in (0, 3, 6):
        s.text(ax0 - 0.12, Y(yv), str(yv), size=15, ha='right')
        s.line(ax0, Y(yv), ax1, Y(yv), color=HAIR, lw=0.8, z=0)
    for xv in (0, 3000, 6000):
        s.text(X(xv), ay0 - 0.3, f'{xv:,}', size=15)
    s.text(w / 2, 0.2, 'Requests a month', size=16, color=BODY)
    s.text(0.05, h - 0.2, 'UGX million a month (invented figures)', size=15, ha='left', color=BODY)
    s.line(X(0), Y(0), X(6000), Y(6.0), color=INK, lw=3)
    s.line(X(0), Y(3.0), X(6000), Y(3.0), color=RED, lw=3)
    s.circle(X(3000), Y(3.0), 0.13, fill=GOLD, edge=INK, lw=2, z=5)
    s.text(X(3000) + 0.2, Y(3.0) - 0.45, '3,000 requests', size=16, weight='bold', ha='left')
    s.text(X(4700), Y(5.35), 'Pay per use', size=16, weight='bold')
    s.text(X(1500), Y(3.0) + 0.3, 'Fixed monthly cost', size=16, weight='bold', color=RED)
    return s
