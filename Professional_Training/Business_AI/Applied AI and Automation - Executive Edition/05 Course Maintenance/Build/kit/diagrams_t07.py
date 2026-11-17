"""Figures for Session 7: open weights, file formats, size and running cost.

Kinds (use as dict(kind='t07_...')): openness, licence, weightsfile, everyday, memorysum, scale, rounding, levels, container, sizegrid, sizes, quality, options, breakeven, weights_link, quantformula.
Real data drawn here: the numbers in weightsfile are the first values of block 0 of SmolLM2-135M-Instruct; sizes, sizegrid and quality come from
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
        _wrap(s, (gx0 + gx1) / 2, y + gh / 2, gx1 - gx0 - 0.4, c, 16)
    return s


# ----------------------------------------------------------------------------------------------- weights file
@fig('x_t07_weightsfile')
def weightsfile(w, h, **_):
    s = Scene(w, h)
    s.icon('doc', 0.55, h - 0.6, 0.8)
    s.text(1.1, h - 0.45, 'model.safetensors', size=22, weight='bold', ha='left')
    s.text(1.1, h - 0.88, 'SmolLM2-135M-Instruct, Apache 2.0: the first block', size=16, color=BODY, ha='left')
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
    s.text(w / 2, 0.62, '134,515,008 parameters like these', size=22, weight='bold')
    s.text(w / 2, 0.22, 'Real values from the first block. Each is one parameter.', size=15, color=BODY)
    return s


# ----------------------------------------------------------------------------------------------- memory sum
@fig('x_t07_memorysum')
def memorysum(w, h, **_):
    s = Scene(w, h)
    bh = 1.1
    y = h - 0.1 - bh
    widths = [2.6, 0.5, 1.9, 0.5, 2.0]
    gap = (w - 0.1 - sum(widths)) / 4
    xs = []
    x = 0.05
    for ww in widths:
        xs.append(x)
        x += ww + gap
    s.box(xs[0], y, widths[0], bh, '134.5 million\nparameters', size=19, weight='bold')
    s.text(xs[1] + widths[1] / 2, y + bh / 2, '×', size=34, weight='bold')
    s.box(xs[2], y, widths[2], bh, '4 bytes each\n(FP32)', size=19, weight='bold')
    s.text(xs[3] + widths[3] / 2, y + bh / 2, '=', size=34, weight='bold')
    s.box(xs[4], y, widths[4], bh, '538 MB\nfile', size=19, weight='bold', fill=GOLD, lw=2.2)
    # the formula
    s.text(w / 2, y - 0.42, 'Memory ≈ N × b', size=24, weight='bold')
    s.text(w / 2, y - 0.85, 'N = number of parameters.  b = bytes per parameter.', size=16, color=BODY)
    # bytes per parameter by precision
    s.text(0.05, 1.95, 'b for each precision (b = bits ÷ 8), and the size it gives here', size=16, weight='bold', ha='left')
    chips = [('FP32', 'b = 4', '538 MB'), ('FP16', 'b = 2', '269 MB'), ('INT8', 'b = 1', '135 MB'), ('4-bit', 'b = 0.5', '67 MB')]
    g = 0.15
    cw = (w - 0.1 - 3 * g) / 4
    for i, (nm, bb, sz) in enumerate(chips):
        cx = 0.05 + i * (cw + g)
        s.box(cx, 0.75, cw, 1.0, '', fill=GOLD if i == 0 else PAPER, lw=1.8 if i == 0 else 1.4)
        s.text(cx + cw / 2, 1.5, f'{nm}   {bb}', size=17, weight='bold')
        s.text(cx + cw / 2, 1.0, sz, size=19, weight='bold')
    s.text(0.05, 0.4, 'Sums: 134.5 million × b. The 4-bit size is the sum only; the measured file is 76 MB.', size=15, ha='left', color=BODY)
    s.text(0.05, 0.12, 'Measured FP32 file: 538,090,376 bytes. The small extra is the file header.', size=15, ha='left', color=BODY)
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
    s.tag(x0, h - 0.4, 'FP16', size=15, fill=GOLD, color=INK)
    s.box(x0 + 1.4, h - 0.4, 0.13 * 5 * 15 / 16 + 0.32, 0.4, '4-bit', size=15, fill=PAPER, edge=INK, color=INK, weight='bold', r=0.06)
    for i, (lab, a, b) in enumerate(groups):
        top = h - 0.6 - i * gh
        s.text(0.05, top - gh / 2 + 0.05, lab + '\nparameters', size=17, weight='bold', ha='left')
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
    specs = [('FP32: almost any value', None), ('INT8 (8-bit integer): 256 allowed values', 256), ('4-bit: 16 allowed values', 16)]
    s.text(0.05, h - 0.3, 'The parameter to store: 0.37', size=19, weight='bold', ha='left')
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
    s.text(0.05, top - 0.2, 'FILE FORMAT (container): how the file is packed', size=17, weight='bold', ha='left', color=RED)
    items = [('safetensors', 'Parameters only, in a format built to load safely'),
             ('GGUF', 'Parameters plus metadata, read by local tools such as llama.cpp'),
             ('ONNX', 'Open Neural Network Exchange: parameters plus the calculation')]
    bh = 1.5
    for i, (hd, tx) in enumerate(items):
        x = 0.05 + i * (bw + gap)
        y = top - 0.5 - bh
        s.box(x, y, bw, bh, '', fill=PAPER, edge=INK, lw=2.4)
        s.text(x + bw / 2, y + bh - 0.32, hd, size=22, weight='bold')
        _wrap(s, x + bw / 2, y + 0.62, bw - 0.3, tx, 16, color=BODY)
        s.arrow(x + bw / 2, y - 0.05, x + bw / 2, y - 0.32, lw=2, head=14)
    yb = 0.1
    s.text(0.05, 1.5, 'PRECISION: how many bits each parameter gets (quantisation)', size=17, weight='bold', ha='left', color=RED)
    labs = ['FP32', 'FP16', 'INT8', '4-bit']
    cw = (w - 0.1 - 0.2 * 3) / 4
    for i, lab in enumerate(labs):
        s.box(0.05 + i * (cw + 0.2), yb + 0.05, cw, 0.7, lab, size=20, weight='bold', fill=GOLD if i == 3 else PAPER, lw=1.8)
    s.text(w / 2, 1.1, 'Any file format can hold parameters at any of these', size=16, color=BODY)
    return s


# ----------------------------------------------------------------------------------------------- size grid (published listings)
@fig('x_t07_sizegrid')
def sizegrid(w, h, **_):
    s = Scene(w, h)
    c0 = 2.5
    cw = (w - c0 - 0.05) / 3
    heads = ['safetensors', 'GGUF', 'ONNX']
    rows = [('FP32 (32-bit)', ['538*', '-', '540']), ('FP16 (16-bit)', ['269', '271', '270']), ('INT8 (8-bit)', ['135*', '145', '137']),
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
        s.text(0.2, y + rh / 2, lab, size=18, weight='bold', ha='left')
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
    data = [('FP32', 538.1, '100%'), ('FP16', 269.1, '50%'), ('INT8', 135.0, '25%'), ('4-bit', 75.8, '14%')]
    gap = 0.22
    # side of the largest square so that the row fits the width and height
    ratio = [(d[1] / 538.1) ** 0.5 for d in data]
    smax = min((w - 0.1 - gap * 3) / sum(ratio), h - 1.35)
    x = 0.05
    for (lab, mb, pct), r in zip(data, ratio):
        side = smax * r
        s.box(x, 1.2, side, side, '', fill=GOLD if lab == 'FP32' else PAPER, edge=INK, lw=2, r=0.03)
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
    panels = [('FP32', [(' U', 11), (' known', 10), (' the', 8)], False), ('Our rough 4-bit', [(' the', 56), (' a', 6), (' U', 3)], True)]
    s.text(w / 2, h - 0.25, 'After "The capital city of Uganda is", the three likeliest next tokens', size=16, weight='bold')
    for p, (lab, items, hl) in enumerate(panels):
        x0 = 0.05 + p * (pw + 0.3)
        s.box(x0, 1.55, pw, h - 2.35, '', fill=PAPER, edge=INK, lw=2.0 if hl else 1.4, r=0.05)
        s.text(x0 + 0.2, h - 1.15, lab + (' model' if lab=='FP32' else ''), size=18, weight='bold', ha='left', color=RED if hl else INK)
        for k, (word, pc) in enumerate(items):
            yy = h - 1.8 - k * 0.55
            s.text(x0 + 0.2, yy, word.strip() or word, size=16, ha='left')
            bwid = (pw - 2.3) * pc / 56
            s.rect(x0 + 1.25, yy - 0.16, max(0.05, bwid), 0.32, fill=GOLD if hl else PALE, edge=INK, lw=1.4)
            s.text(x0 + 1.25 + max(0.05, bwid) + 0.1, yy, f'{pc}%', size=15, ha='left', weight='bold')
    s.text(0.05, 1.15, 'Average loss (Session 5) over three sentences, lower is better', size=15, weight='bold', ha='left')
    cw = (w - 0.1 - 0.15 * 3) / 4
    for i, (lab, v) in enumerate([('FP32', '4.57'), ('FP16', '4.57'), ('INT8', '4.56'), ('Rough 4-bit', '5.09')]):
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
    s.text(X(1900), Y(1.0), 'Rent: 1,000 a request', size=16, weight='bold', ha='left')
    s.text(X(300), Y(3.0) + 0.3, 'Host: 3,000,000 a month', size=16, weight='bold', color=RED, ha='left')
    for xv in (2000, 5000):
        s.circle(X(xv), Y(xv / 1000), 0.08, fill=PAPER, edge=INK, lw=1.6, z=5)
    return s


# ----------------------------------------------------------------------------------------------- weights link: one neuron to GPT-2
@fig('x_t07_weights_link')
def weights_link(w, h, **_):
    s = Scene(w, h)
    pw, gap = 3.55, 0.55
    xs = [0.1 + i * (pw + gap) for i in range(3)]
    ph, y0 = 3.0, 0.95
    heads = ['Session 1: house price', 'Session 1: digit network', 'GPT-2 small']
    for i, x in enumerate(xs):
        s.box(x, y0, pw, ph, '', fill=PAPER, edge=INK, lw=1.8)
        s.box(x, y0 + ph - 0.55, pw, 0.55, heads[i], size=17, weight='bold', fill=GOLD if i == 2 else PALE, edge=INK, lw=1.8, r=0.05)
        if i < 2:
            s.arrow(x + pw + 0.04, y0 + ph / 2, xs[i + 1] - 0.04, y0 + ph / 2, color=RED, lw=2.6)
    # neuron: weighted sum
    x = xs[0]
    s.text(x + pw / 2, y0 + 1.95, 'w₁x₁ + w₂x₂ + b', size=18, weight='bold')
    s.text(x + pw / 2, y0 + 1.35, '2 weights + 1 bias', size=16, color=BODY)
    s.text(x + pw / 2, y0 + 0.62, '= 3 parameters', size=24, weight='bold', color=RED)
    # digit net
    x = xs[1]
    s.text(x + pw / 2, y0 + 1.95, '64 x 16 + 16\n+ 16 x 10 + 10', size=18, weight='bold')
    s.text(x + pw / 2, y0 + 1.2, 'weights + biases', size=15, color=BODY)
    s.text(x + pw / 2, y0 + 0.62, '= 1,210', size=24, weight='bold', color=RED)
    # GPT-2
    x = xs[2]
    s.text(x + 0.15, y0 + 2.15, '12 blocks × 7,087,872', size=15, ha='left')
    s.text(x + 0.15, y0 + 1.78, '+ token table 50,257 × 768', size=15, ha='left')
    s.text(x + 0.15, y0 + 1.41, '+ position table 1,024 × 768', size=15, ha='left')
    s.text(x + 0.15, y0 + 1.04, '+ 1,536 final scaling numbers', size=15, ha='left')
    s.text(x + pw / 2, y0 + 0.45, '= 124,439,808', size=22, weight='bold', color=RED)
    s.text(w / 2, 0.52, 'Every parameter was adjusted by the training loop of Session 0.', size=17, weight='bold')
    s.text(w / 2, 0.15, 'Weights multiply an input. Biases are added. Together they are the parameters.', size=15, color=MUTE)
    return s


# ----------------------------------------------------------------------------------------------- everyday: size = numbers x bytes
@fig('x_t07_everyday')
def everyday(w, h, **_):
    s = Scene(w, h)
    cx = [2.9, 6.5, 8.6, 10.8]   # column centres: numbers held, bytes each, size
    heads = ['Numbers it holds', 'Bytes each', 'Size']
    c_num, c_by, c_sz = 5.6, 8.35, 10.7
    s.text(c_num, h - 0.25, heads[0], size=16, weight='bold')
    s.text(c_by, h - 0.25, heads[1], size=16, weight='bold')
    s.text(c_sz, h - 0.25, heads[2], size=16, weight='bold')
    s.line(0.05, h - 0.55, w - 0.05, h - 0.55, color=INK, lw=2.2)
    rows = [('phone', 'A phone photo', '12 million pixels x 3 colours', '36 million', '1', '36 MB'),
            ('bars', 'One minute of a song', '44,100 per second x 2 channels x 60', '5.3 million', '2', '10.6 MB'),
            ('calculator', 'A spreadsheet', '1 million cells', '1 million', '8', '8 MB')]
    rh = (h - 0.65 - 0.9) / 3
    for i, (ic, nm, sub, nums, by, sz) in enumerate(rows):
        y = h - 0.55 - (i + 1) * rh
        s.text(0.15, y + rh * 0.68, nm, size=18, weight='bold', ha='left')
        s.text(0.15, y + rh * 0.3, sub, size=14, color=BODY, ha='left')
        s.text(c_num, y + rh / 2, nums, size=20, weight='bold')
        s.text((c_num + c_by) / 2 + 0.2, y + rh / 2, 'x', size=22, weight='bold')
        s.text(c_by, y + rh / 2, by, size=20, weight='bold')
        s.text((c_by + c_sz) / 2 + 0.1, y + rh / 2, '=', size=22, weight='bold')
        s.box(c_sz - 0.8, y + 0.12, 1.6, rh - 0.24, sz, size=19, weight='bold', fill=PAPER, lw=2.0)
        s.line(0.05, y, w - 0.05, y, color=HAIR, lw=1)
    s.text(0.05, 0.5, 'Size = how many numbers  x  bytes per number', size=18, weight='bold', ha='left')
    s.text(0.05, 0.15, 'Saved JPEG and MP3 files are compressed, so they are smaller.', size=14, color=BODY, ha='left')
    return s


# ----------------------------------------------------------------------------------------------- everyday: rounding a price
@fig('x_t07_rounding')
def rounding(w, h, **_):
    s = Scene(w, h)
    x0, x1 = 0.7, w - 0.7
    lo, hi = 4000, 5000

    def px(v):
        return x0 + (v - lo) / (hi - lo) * (x1 - x0)
    price = 4837
    s.text(0.05, h - 0.3, 'The exact price: UGX 4,837', size=19, weight='bold', ha='left')
    specs = [('Rounded to the nearest 100: 11 allowed values here', list(range(4000, 5001, 100)), 4800, GOLD),
             ('Rounded to the nearest 1,000: 2 allowed values here', [4000, 5000], 5000, RED)]
    ys = [h - 1.75, 1.05]
    for (lab, ticks, near, col), y in zip(specs, ys):
        s.text(0.05, y + 0.75, lab, size=17, weight='bold', ha='left')
        s.line(x0, y, x1, y, color=INK, lw=2)
        for tv in ticks:
            s.line(px(tv), y - 0.14, px(tv), y + 0.14, color=INK, lw=1.8)
        s.circle(px(price), y, 0.09, fill=PAPER, edge=INK, lw=2, z=5)
        s.circle(px(near), y, 0.11, fill=GOLD, edge=INK, lw=2, z=6)
        right = near >= 4900
        s.text(px(near) + (0.3 if right else 0), y - 0.45, 'stored as %s  (error %d)' % (format(near, ','), abs(near - price)), size=16, weight='bold',
               color=RED if col == RED else BODY, ha='right' if right else 'center')
    s.text(x0, 0.3, '4,000', size=15, color=MUTE)
    s.text(x1, 0.3, '5,000', size=15, color=MUTE)
    return s


# ----------------------------------------------------------------------------------------------- quantisation formula, worked on three numbers
@fig('x_t07_quantformula')
def quantformula(w, h, **_):
    s = Scene(w, h)
    s.text(0.05, h - 0.35, 'q = round(x ÷ s) + z', size=26, weight='bold', ha='left')
    s.text(6.1, h - 0.35, 'x̂ = s × (q − z)', size=26, weight='bold', ha='left')
    s.text(0.05, h - 0.8, 'store: steps 1 to 3 in one line', size=16, color=BODY, ha='left')
    s.text(6.1, h - 0.8, 'read back: undo the steps', size=16, color=BODY, ha='left')
    parts = [('x', 'the parameter, e.g. 0.42'), ('s', 'the scale: the step between levels, 0.1'), ('z', 'the zero point: the stored value for 0, here 8'),
             ('q', 'the whole number stored, 12'), ('x̂', '"x hat": the value read back, 0.4')]
    g = 0.12
    pw = (w - 0.1 - g * 4) / 5
    for i, (a, b) in enumerate(parts):
        x = 0.05 + i * (pw + g)
        s.box(x, 1.05, pw, 1.75, '', fill=PAPER, lw=1.4)
        s.text(x + pw / 2, 2.45, a, size=22, weight='bold', color=RED)
        _wrap(s, x + pw / 2, 1.6, pw - 0.25, b, 15)
    s.text(0.05, 0.62, 'Rounding error |x − x̂| is at most s ÷ 2. 4-bit: s = 0.1, error up to 0.05.', size=16, weight='bold', ha='left')
    s.text(0.05, 0.2, 'INT8 has 256 levels over the same range: s = 1.5 ÷ 255 ≈ 0.006, error up to 0.003. Fewer bits, bigger steps, bigger error.', size=15, ha='left', color=BODY)
    return s


# ================================================================================================ 11 Nov 2026 rework: explain before use
@fig('x_t07_bits')
def bits(w, h, **_):
    s = Scene(w, h)
    s.text(0.05, h - 0.25, 'A bit is a switch: off (0) or on (1)', size=18, weight='bold', ha='left')
    rows = [(1, '2 patterns: 0, 1'), (2, '4 patterns: 00, 01, 10, 11'), (3, '8 patterns'), (4, '16 patterns'), (8, '256 patterns = one byte')]
    top = h - 0.75
    rh = 0.62
    for i, (n, lab) in enumerate(rows):
        y = top - i * rh
        s.text(0.05, y, f'{n} bit' + ('s' if n > 1 else ''), size=16, weight='bold', ha='left')
        for k in range(n):
            on = (k % 3 == 0)
            s.box(1.0 + k * 0.38, y - 0.2, 0.32, 0.4, '1' if on else '0', size=15, weight='bold', fill=GOLD if on else PAPER, r=0.03, lw=1.2)
        s.text(4.2, y, lab, size=16, ha='left', weight='bold' if n == 8 else 'normal', color=RED if n == 8 else INK)
    s.text(0.05, 0.95, 'Each extra bit doubles the patterns. A byte (8 bits) holds', size=15, ha='left', color=BODY)
    s.text(0.05, 0.62, '0 to 255, like a pixel brightness in Session 1.', size=15, ha='left', color=BODY)
    s.text(0.05, 0.2, '1 MB = 1 million bytes.  1 GB = 1 billion bytes.', size=16, weight='bold', ha='left')
    return s


@fig('x_t07_digits')
def digits(w, h, **_):
    s = Scene(w, h)
    s.text(0.05, h - 0.25, 'One parameter, 0.4321357, stored four ways', size=18, weight='bold', ha='left')
    ws = [2.1, 2.0, 3.6, 2.0, 2.15]
    xs = [0.05]
    for c in ws[:-1]:
        xs.append(xs[-1] + c)
    heads = ['Precision', 'Bytes each', 'What we keep', 'Stored as', 'Error']
    top = h - 0.6
    for j, hd in enumerate(heads):
        s.box(xs[j], top - 0.55, ws[j], 0.55, hd, size=15, weight='bold', fill=PALE, r=0.02, lw=1.2)
    rows = [('FP32', '4 (32 bits)', 'about 7 digits', '0.4321357', 'about 0'),
            ('FP16', '2 (16 bits)', 'about 3 to 4 digits', '0.4321', '0.000007'),
            ('INT8', '1 (8 bits)', 'one of 256 levels', '0.4297', '0.0024'),
            ('4-bit', '0.5 (4 bits)', 'one of 16 levels', '0.375', '0.057')]
    rh = 0.6
    for i, r in enumerate(rows):
        y = top - 0.55 - (i + 1) * rh
        for j, v in enumerate(r):
            fill = GOLD if (j == 3) else PAPER
            s.box(xs[j], y, ws[j], rh, v, size=17 if j != 2 else 16, weight='bold' if j in (0, 3) else 'normal', fill=fill, r=0.02, lw=1.2,
                  color=RED if (j == 4 and i == 3) else INK)
    s.text(0.05, 0.2, 'FP: floating point, a number with a decimal point that can move. INT8: 8-bit integer (whole number).', size=15, ha='left', color=BODY)
    return s


def _numline(s, x0, x1, y, lo, hi, step, label_every=None, size=14):
    def X(v):
        return x0 + (v - lo) / (hi - lo) * (x1 - x0)
    s.line(x0, y, x1, y, color=INK, lw=2)
    n = int(round((hi - lo) / step))
    for k in range(n + 1):
        v = lo + k * step
        s.line(X(v), y - 0.1, X(v), y + 0.1, color=INK, lw=1.4)
    return X


@fig('x_t07_quant_step1')
def quant_step1(w, h, **_):
    s = Scene(w, h)
    s.text(0.05, h - 0.25, 'Three parameters: 0.42, −0.26, 0.64.  4 bits give 16 levels.', size=17, weight='bold', ha='left')
    s.text(0.05, h - 0.65, 'Step 1, the scale s: 16 levels, 0.1 apart, cover −0.8 to 0.7, so s = 0.1 (the step between levels).', size=16, ha='left')
    x0, x1, y = 0.6, w - 0.6, h - 1.75
    X = _numline(s, x0, x1, y, -0.8, 0.7, 0.1)
    for v in (-0.8, -0.3, 0.0, 0.4, 0.6, 0.7):
        s.text(X(v), y - 0.35, ('%.1f' % v).replace('-', '−'), size=14, color=MUTE)
    for v, near in ((0.42, 0.4), (-0.26, -0.3), (0.64, 0.6)):
        s.circle(X(v), y + 0.38, 0.07, fill=PAPER, edge=INK, lw=1.6, z=5)
        s.arrow(X(v), y + 0.3, X(near), y + 0.08, color=RED, lw=1.6, head=8)
        s.circle(X(near), y, 0.08, fill=GOLD, edge=INK, lw=1.6, z=5)
        s.text(X(v), y + 0.65, ('%.2f' % v).replace('-', '−'), size=15, weight='bold')
    s.text(0.05, 1.45, 'Step 2, divide by s and round to the nearest whole number:', size=16, weight='bold', ha='left')
    ws = [1.8, 3.2, 3.2, 3.6]
    xs = [0.05]
    for c in ws[:-1]:
        xs.append(xs[-1] + c)
    rows = [['x', 'x ÷ s', 'round', 'level on the line'],
            ['0.42 | −0.26 | 0.64', '4.2 | −2.6 | 6.4', '4 | −3 | 6', '0.4 | −0.3 | 0.6']]
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            s.box(xs[j], 0.6 - i * 0.5, ws[j], 0.5, v, size=15, weight='bold' if (i == 0 or j == 2) else 'normal',
                  fill=PALE if i == 0 else (GOLD if j == 2 else PAPER), r=0.02, lw=1.2)
    return s


@fig('x_t07_quant_step2')
def quant_step2(w, h, **_):
    s = Scene(w, h)
    s.text(0.05, h - 0.25, 'Step 3, the zero point z: 4 bits store only 0 to 15, with no minus sign.', size=17, weight='bold', ha='left')
    s.text(0.05, h - 0.65, 'Add z = 8 to every rounded value, so −8 to 7 becomes 0 to 15. The level for zero is stored as 8.', size=16, ha='left')
    ws = [1.25, 1.2, 2.3, 2.95, 1.2]
    xs = [0.05]
    for c in ws[:-1]:
        xs.append(xs[-1] + c)
    heads = ['x', 'round', '+ z = q (stored)', 'read back: s × (q − z)', 'error']
    rows = [['0.42', '4', '4 + 8 = 12', '0.1 × 4 = 0.4', '0.02'],
            ['−0.26', '−3', '−3 + 8 = 5', '0.1 × (−3) = −0.3', '0.04'],
            ['0.64', '6', '6 + 8 = 14', '0.1 × 6 = 0.6', '0.04']]
    top = h - 1.0
    for j, hd in enumerate(heads):
        s.box(xs[j], top - 0.55, ws[j], 0.55, hd, size=15, weight='bold', fill=PALE, r=0.02, lw=1.2)
    for i, r in enumerate(rows):
        y = top - 0.55 - (i + 1) * 0.55
        for j, v in enumerate(r):
            s.box(xs[j], y, ws[j], 0.55, v, size=16, weight='bold' if j in (0, 2) else 'normal', fill=GOLD if j == 2 else PAPER,
                  color=RED if j == 4 else INK, r=0.02, lw=1.2)
    xr = sum(ws) + 0.3
    s.box(xr, 0.2, w - xr - 0.05, top - 0.2, '', fill=PAPER, lw=1.4)
    s.text(xr + 0.15, top - 0.35, 'Stored: 12, 5, 14', size=16, weight='bold', ha='left')
    s.text(xr + 0.15, top - 0.8, 'each fits in 4 bits', size=15, ha='left')
    s.text(xr + 0.15, top - 1.35, 'Kept once for the', size=15, ha='left')
    s.text(xr + 0.15, top - 1.7, 'group: s = 0.1, z = 8', size=15, ha='left', weight='bold')
    s.text(xr + 0.15, top - 2.25, 'Every error is at most', size=15, ha='left')
    s.text(xr + 0.15, top - 2.6, 'half a step: 0.05', size=15, ha='left', weight='bold', color=RED)
    return s


@fig('x_t07_breakeven_formula')
def breakeven_formula(w, h, **_):
    s = Scene(w, h)
    pw = 5.7
    s.box(0.05, 0.1, pw, h - 0.2, '', fill=PAPER, lw=1.6)
    s.text(0.25, h - 0.4, 'Add a running cost when you host', size=17, weight='bold', color=RED, ha='left')
    lines = [('Renting costs p = 1,000 a request.', False), ('Hosting costs v = 200 a request', False), ('(power, upkeep) plus F = 3,000,000 a month.', False),
             ('Each request you host saves', False), ('p − v = 1,000 − 200 = 800.', True), ('Requests needed to pay back F:', False), ('3,000,000 ÷ 800 = 3,750 a month.', True)]
    for i, (tx, b) in enumerate(lines):
        s.text(0.25, h - 0.95 - i * 0.43, tx, size=16, ha='left', weight='bold' if b else 'normal')
    x2 = pw + 0.25
    s.box(x2, 0.1, w - x2 - 0.05, h - 0.2, '', fill=PAPER, lw=1.6)
    s.text(x2 + 0.2, h - 0.4, 'The formula', size=17, weight='bold', color=RED, ha='left')
    s.box(x2 + 0.2, h - 1.45, w - x2 - 0.45, 0.75, 'Break-even volume = F ÷ (p − v)', size=19, weight='bold', fill=GOLD)
    defs = ['F: fixed cost a month (the server)', 'p: price per request if you rent', 'v: running cost per request if you host',
            'Check, with v = 0: 3,000,000 ÷ 1,000 = 3,000']
    for i, d in enumerate(defs):
        s.text(x2 + 0.2, h - 1.95 - i * 0.48, d, size=16, ha='left', weight='bold' if i == 3 else 'normal')
    s.text(x2 + 0.2, 0.35, 'Above break-even, hosting is cheaper.', size=15, ha='left', color=BODY)
    return s
