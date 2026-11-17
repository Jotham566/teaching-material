"""Figure kinds for Sessions 5 and 6 (author letter c). Each is registered as x_ds_c_<name> and used as visual=dict(kind='ds_c_<name>', ...).

  ds_c_notebook     a notebook drawn as text cell, code cell with play button, and output, with numbered labels
  ds_c_sheetpy      the same three steps as spreadsheet cells and as Python lines
  ds_c_assign       three named boxes (name, value, data type): the right side is worked out, then stored
  ds_c_types        int, float, str and bool: meaning, a real example, what type() prints, the Excel cousin
  ds_c_trap         numbers with and without quotes: the same plus sign, two different results
  ds_c_list         a list drawn as cells with index numbers, and three lookups
  ds_c_dict         a dictionary as key and value pairs, with one lookup
  ds_c_traceback    a real traceback with its parts labelled in reading order
  ds_c_flowchart    an if / elif / else decision as a flowchart beside the code
  ds_c_numline      loyalty tiers on a number line with the four edge cases marked
  ds_c_logic        the logical operators and / or drawn as bars on a number line
  ds_c_loop         fill down in a sheet beside a for loop
  ds_c_trace        code with line numbers beside a trace table of what happens step by step
  ds_c_function     a function definition with its parts labelled, and one call with its return value
  ds_c_tests        a table of test cases: input, expected, got, PASS or FAIL
All text is 14 pt or larger and every figure is audited for overlaps by figkit.
"""
from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, PALE, fig
import slidekit as K
from matplotlib.patches import Rectangle


def tw(t, size, kind='regular'):
    return K.width_in(str(t), size, kind)


def mono_w(t, size):
    return 0.602 * size / 72 * len(t)


def wrap_text(s, x, y, w, text, size, weight='normal', color=INK, ha='left', va='center', italic=False, mono=False):
    """Wrapped text in a column of width w, centred on y (va centre) or starting at y (va top). Returns its height."""
    lines = K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', w)
    s.text(x, y, '\n'.join(lines), size=size, weight=weight, color=color, ha=ha, va=va, italic=italic, mono=mono)
    return len(lines) * size * 1.15 / 72


def codebox(s, x, ytop, lines, size=14, w=None, pad=0.14, hl=()):
    lh = size * 1.5 / 72
    w = w or max(mono_w(l, size) for l in lines) + 2 * pad + 0.04
    cw, ch = s.code(x, ytop, lines, size=size, line_h=lh, w=w, pad=pad, hl_lines=hl)
    return cw, ch


def badge(s, x, y, text, r=0.19, size=16, fill=GOLD):
    s.circle(x, y, r, fill=fill, edge=INK, lw=1.6, z=5)
    s.text(x, y, str(text), size=size, weight='bold', z=6)


def tag(s, x, y, text, fill=GOLD, size=14, h=0.3, edge=INK):
    w = tw(text, size, 'bold') + 0.22
    s.box(x, y - h / 2, w, h, text, size=size, fill=fill, edge=edge, lw=1.4, weight='bold', r=0.05, z=5)
    return w


# ------------------------------------------------------------------ a notebook
@fig('x_ds_c_notebook')
def ds_c_notebook(w, h, heading='', code=(), output=(), **_):
    s = Scene(w, h)
    fw = 7.3
    top = h - 0.08
    s.rect(0.08, 0.05, fw, h - 0.1, fill=PAPER, edge=INK, lw=2.0, z=1)
    th = 0.8
    ty = top - 0.15 - th
    s.box(0.3, ty, fw - 0.4, th, '', fill=PAPER, edge=GREY, lw=1.4, r=0.04, z=2)
    s.text(0.5, ty + th / 2, heading, size=22, weight='bold', ha='left')
    lh = 15 * 1.5 / 72
    ch = len(code) * lh + 0.3
    cy_top = ty - 0.2
    s.circle(0.7, cy_top - ch / 2, 0.24, fill=GOLD, edge=INK, lw=1.8, z=3)
    s.poly([(0.62, cy_top - ch / 2 - 0.12), (0.62, cy_top - ch / 2 + 0.12), (0.8, cy_top - ch / 2)], fill=INK, edge=INK, lw=1, z=4)
    cw = fw - 1.4
    s.code(1.15, cy_top, list(code), size=15, line_h=lh, w=cw, pad=0.15)
    oy_top = cy_top - ch - 0.15
    oh = len(output) * 0.34 + 0.2
    s.box(1.15, oy_top - oh, cw, oh, '', fill=PAPER, edge=HAIR, lw=1.4, r=0.03, z=2)
    for i, l in enumerate(output):
        s.text(1.3, oy_top - 0.1 - (i + 0.5) * 0.34, l, size=16, mono=True, ha='left')
    rx = fw + 0.5
    labels = [(ty + th / 2, 'Text cell: headings and notes for people. Python skips it.'),
              (cy_top - ch / 2, 'Code cell: Python. Press the play button to run it.'),
              (oy_top - oh / 2, 'Output: the answer appears under the cell.')]
    for i, (yy, t) in enumerate(labels):
        s.line(fw + 0.08, yy, rx - 0.22, yy, color=INK, lw=1.4, z=1)
        badge(s, rx, yy, i + 1)
        wrap_text(s, rx + 0.32, yy, w - rx - 0.45, t, 16, ha='left')
    ky = oy_top - oh - 0.15
    s.box(0.3, 0.2, fw - 0.4, max(0.5, ky - 0.2), 'Cells run from the top, in order', size=16, weight='bold', fill=PALE, edge=INK, lw=1.2, r=0.04)
    return s


# ------------------------------------------------------------------ the same three steps in a sheet and in Python
@fig('x_ds_c_sheetpy')
def ds_c_sheetpy(w, h, rows=(), lines=(), formula='', **_):
    s = Scene(w, h)
    colA, colB, rn = 1.35, 1.1, 0.35
    sx = 0.1
    s.text(sx + rn, h - 0.3, 'Excel or Sheets', size=17, weight='bold', ha='left')
    px = sx + rn + colA + colB + 0.25
    pw = w - px - 0.05
    s.text(px, h - 0.3, 'Python', size=17, weight='bold', ha='left')
    rh = 0.78
    ytop = h - 0.95
    s.text(sx + rn + colA / 2, ytop + 0.2, 'A', size=14, color=GREY)
    s.text(sx + rn + colA + colB / 2, ytop + 0.2, 'B', size=14, color=GREY)
    for i, (label, value) in enumerate(rows):
        y = ytop - (i + 1) * rh
        s.text(sx + rn / 2, y + rh / 2, str(i + 2), size=14, color=GREY)
        last = i == len(rows) - 1
        s.box(sx + rn, y, colA, rh, label, size=15, fill=PALE, edge=INK, lw=1.2, r=0.0)
        s.box(sx + rn + colA, y, colB, rh, value, size=16, fill=GOLD if last else PAPER, edge=INK, lw=1.2, r=0.0, weight='bold' if last else 'normal')
    total = rh * len(rows)
    s.box(px, ytop - total, pw, total, '', fill=INK, edge=INK, r=0.08, z=2)
    for i, l in enumerate(lines):
        s.text(px + 0.15, ytop - (i + 0.5) * rh, l, size=14, color=PAPER, mono=True, ha='left', z=4)
    y = ytop - total - 0.45
    s.text(sx + rn, y, formula, size=15, ha='left', mono=True)
    wrap_text(s, sx, y - 0.8, w - 0.2, 'In Python the name you choose takes the place of the cell address.', 16, color=BODY, ha='left')
    return s


# ------------------------------------------------------------------ assignment: name, value, data type
@fig('x_ds_c_assign')
def ds_c_assign(w, h, inputs=(), result=None, statement='', **_):
    s = Scene(w, h)
    bw, bh = 2.7, 1.25
    ys = [h - 0.15 - bh, h - 0.15 - 2 * bh - 0.3]
    for (name, value, typ), y in zip(inputs, ys):
        s.box(0.1, y, bw, bh, '', fill=PAPER, edge=INK, lw=2.0, r=0.06)
        s.text(0.25, y + bh - 0.28, name, size=16, mono=True, weight='bold', ha='left')
        s.text(0.25, y + 0.42, value, size=26, mono=True, weight='bold', ha='left')
        tag(s, 0.1 + bw - tw(typ, 14, 'bold') - 0.35, y + 0.28, typ, fill=PALE)
    rx = w - bw - 0.1
    ry = (ys[0] + ys[1]) / 2
    name, value, typ = result
    s.box(rx, ry, bw, bh, '', fill=GOLD, edge=INK, lw=2.0, r=0.06)
    s.text(rx + 0.15, ry + bh - 0.28, name, size=16, mono=True, weight='bold', ha='left')
    s.text(rx + 0.15, ry + 0.42, value, size=26, mono=True, weight='bold', ha='left')
    tag(s, rx + bw - tw(typ, 14, 'bold') - 0.25, ry + 0.28, typ, fill=PAPER)
    cx, cy = 0.1 + bw + (rx - 0.1 - bw) / 2, ry + bh / 2
    s.circle(cx, cy, 0.34, fill=PAPER, edge=INK, lw=2.0, z=4)
    s.text(cx, cy + 0.02, '×', size=26, weight='bold', z=6)
    for y in ys:
        s.arrow(0.1 + bw + 0.04, y + bh / 2, cx - 0.3, cy + (0.12 if y > ry else -0.12), lw=2.2, head=14)
    s.arrow(cx + 0.36, cy, rx - 0.04, cy, color=RED, lw=2.6, head=16)
    cwid, chei = codebox(s, 0.1, ys[1] - 0.4, [statement], size=16)
    wrap_text(s, 0.1, ys[1] - 0.4 - chei - 0.1, w - 0.2, 'The right side is worked out first. The answer is then stored under the name on the left of the equals sign.', 16, color=BODY, ha='left', va='top')
    return s


# ------------------------------------------------------------------ four data types
@fig('x_ds_c_types')
def ds_c_types(w, h, cols=(), **_):
    s = Scene(w, h)
    n = len(cols)
    gap = 0.2
    cw = (w - 0.1 - gap * (n - 1)) / n
    labels = ['Real example', 'type() prints', 'Excel cousin']
    for i, c in enumerate(cols):
        x = 0.05 + i * (cw + gap)
        y = h - 0.05
        s.box(x, y - 0.6, cw, 0.6, c['name'], size=24, fill=INK, edge=INK, color=PAPER, weight='bold', r=0.06, mono=True)
        y -= 0.7
        hh = wrap_text(s, x + cw / 2, y - 0.02, cw - 0.2, c['meaning'], 16, color=BODY, ha='center', va='top')
        y -= max(hh, 0.55) + 0.12
        for lab, val, mono in ((labels[0], c['example'], True), (labels[1], c['type'], True), (labels[2], c['excel'], False)):
            s.text(x + 0.05, y - 0.1, lab, size=14, color=MUTE, ha='left')
            fill = GOLD if lab == labels[0] else PALE
            s.box(x, y - 0.82, cw, 0.5, val, size=16, mono=mono, fill=fill, edge=INK, lw=1.4, r=0.05)
            y -= 0.94
    return s


# ------------------------------------------------------------------ the quotes trap
@fig('x_ds_c_trap')
def ds_c_trap(w, h, panels=(), verdict='', **_):
    s = Scene(w, h)
    ph = (h - 0.7) / 2
    for k, p in enumerate(panels):
        y0 = h - 0.05 - k * (ph + 0.1)
        s.box(0.1, y0 - ph, w - 0.2, ph, '', fill=PAPER, edge=INK, lw=1.8, r=0.06)
        s.text(0.3, y0 - 0.3, p['title'], size=17, weight='bold', ha='left')
        cy = y0 - ph + 0.95
        cw, ch = codebox(s, 0.3, cy + 0.3, [p['code']], size=17)
        rx = 0.3 + cw + 0.9
        s.arrow(0.3 + cw + 0.08, cy, rx - 0.08, cy, color=RED, lw=2.4, head=16)
        s.box(rx, cy - 0.3, w - rx - 0.3, 0.6, p['result'], size=20, mono=True, weight='bold', fill=GOLD if p.get('bad') else PAPER, edge=INK, lw=1.8, r=0.05)
        s.text(0.3, y0 - ph + 0.3, p['note'], size=15, color=BODY, ha='left')
    s.text(w / 2, 0.28, verdict, size=18, weight='bold', color=RED)
    return s


# ------------------------------------------------------------------ a list with index numbers
@fig('x_ds_c_list')
def ds_c_list(w, h, name='prices', values=(), lookups=(), **_):
    s = Scene(w, h)
    n = len(values)
    cw = min(1.3, (w - 0.3) / n)
    x0 = (w - n * cw) / 2
    ytop = h - 0.9
    s.text(x0, h - 0.3, f'The list called {name}', size=17, weight='bold', ha='left')
    s.cells(x0, ytop - 0.85, [str(v) for v in values], w=cw, h=0.85, size=20, labels=[str(i) for i in range(n)], label_size=17, hl=(0,))
    s.text(x0 - 0.1, ytop - 0.85 - 0.22, 'index', size=14, color=MUTE, ha='right')
    y = ytop - 2.0
    for expr, val, what in lookups:
        s.text(0.3, y, expr, size=18, mono=True, weight='bold', ha='left')
        s.arrow(0.3 + mono_w(expr, 18) + 0.12, y, 3.2, y, color=RED, lw=2.2, head=14)
        s.text(3.35, y, val, size=18, mono=True, weight='bold', ha='left')
        s.text(4.6, y, what, size=15, color=BODY, ha='left')
        y -= 0.58
    return s


# ------------------------------------------------------------------ a dictionary
@fig('x_ds_c_dict')
def ds_c_dict(w, h, name='price_list', pairs=(), pick=None, lookup=('', ''), excel='', **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.28, f'The dictionary called {name}', size=17, weight='bold', ha='left')
    kx, vx, bw, rh = 0.1, 3.0, 1.9, 0.5
    top = h - 0.55
    s.text(kx + bw / 2, top - 0.2, 'key', size=16, weight='bold', color=MUTE)
    s.text(vx + bw / 2, top - 0.2, 'value', size=16, weight='bold', color=MUTE)
    y = top - 0.4
    for k, v in pairs:
        hit = (k == pick)
        s.box(kx, y - rh + 0.05, bw, rh - 0.1, f"'{k}'", size=17, mono=True, fill=GOLD if hit else PAPER, edge=INK, lw=1.6, r=0.04)
        s.box(vx, y - rh + 0.05, bw, rh - 0.1, str(v), size=17, mono=True, fill=GOLD if hit else PAPER, edge=INK, lw=1.6, r=0.04)
        s.arrow(kx + bw + 0.04, y - rh / 2, vx - 0.04, y - rh / 2, color=RED if hit else GREY, lw=2.2, head=13)
        y -= rh
    y -= 0.3
    expr, res = lookup
    s.text(0.1, y, expr, size=17, mono=True, weight='bold', ha='left')
    s.text(0.1 + mono_w(expr, 17) + 0.2, y, '→', size=20, weight='bold', color=RED, ha='left')
    s.text(0.1 + mono_w(expr, 17) + 0.65, y, res, size=17, mono=True, weight='bold', ha='left')
    y -= 0.5
    s.text(0.1, y, 'Excel cousin:', size=15, color=MUTE, ha='left')
    s.text(0.1 + tw('Excel cousin: ', 15) + 0.1, y, excel, size=15, mono=True, ha='left')
    return s


# ------------------------------------------------------------------ a traceback
@fig('x_ds_c_traceback')
def ds_c_traceback(w, h, lines=(), labels=(), **_):
    s = Scene(w, h)
    size = 18
    lh = size * 1.9 / 72
    pw = min(max(mono_w(l, size) for l in lines) + 0.6, 7.6)
    ph = len(lines) * lh + 0.4
    top = (h + ph) / 2
    s.box(0.1, top - ph, pw, ph, '', fill=PAPER, edge=INK, lw=2.0, r=0.05, z=2)
    ys = []
    for i, l in enumerate(lines):
        yy = top - 0.2 - (i + 0.5) * lh
        ys.append(yy)
        last = i == len(lines) - 1
        if last:
            s.ax.add_patch(Rectangle((0.16, yy - lh / 2), pw - 0.12, lh, fc=GOLD, ec='none', zorder=3))
        s.text(0.3, yy, l, size=size, mono=True, ha='left', weight='bold' if last else 'normal', z=5)
    rx = 0.1 + pw + 0.9
    n = len(labels)
    slot = 1.15
    order = sorted(range(n), key=lambda i: labels[i][0])
    for k, idx in enumerate(order):
        li, t_ = labels[idx]
        sy = h / 2 + (n - 1) / 2 * slot - k * slot
        yy = ys[li]
        s.line(0.1 + pw + 0.04, yy, rx - 0.24, sy, color=INK, lw=1.4, z=1)
        badge(s, rx, sy, idx + 1)
        wrap_text(s, rx + 0.32, sy, w - rx - 0.4, t_, 17, ha='left')
    return s


# ------------------------------------------------------------------ an if / elif / else decision
@fig('x_ds_c_flowchart')
def ds_c_flowchart(w, h, start='', tests=(), results=(), code=(), picked=None, **_):
    """tests: [condition text, ...] top to bottom; results: [Gold, Silver, Basic]; picked: index of the result reached."""
    s = Scene(w, h)
    bw, bh = 2.55, 0.66
    x0 = 0.1
    s.text(x0, h - 0.3, start, size=16, mono=True, weight='bold', ha='left')
    ys = [h - 1.45, h - 2.7]
    rx = x0 + bw + 0.95
    rw = 1.1
    for i, (cond, y) in enumerate(zip(tests, ys)):
        s.box(x0, y, bw, bh, cond, size=16, mono=True, fill=PAPER, edge=INK, lw=2.0, r=0.05, weight='bold')
        s.arrow(x0 + bw + 0.03, y + bh / 2, rx - 0.03, y + bh / 2, lw=2.2, head=14, color=INK)
        s.text(x0 + bw + 0.47, y + bh / 2 + 0.22, 'True', size=14, weight='bold', color=MUTE)
        s.box(rx, y + 0.04, rw, bh - 0.08, results[i], size=18, weight='bold', fill=GOLD if picked == i else PAPER, edge=INK, lw=1.8, r=0.05)
    s.arrow(x0 + bw / 2, h - 0.55, x0 + bw / 2, ys[0] + bh + 0.03, lw=2.2, head=14)
    s.arrow(x0 + bw / 2, ys[0] - 0.03, x0 + bw / 2, ys[1] + bh + 0.03, lw=2.2, head=14)
    s.text(x0 + bw / 2 + 0.12, ys[0] - 0.3, 'False', size=14, weight='bold', color=MUTE, ha='left')
    yb = h - 3.95
    s.arrow(x0 + bw / 2, ys[1] - 0.03, x0 + bw / 2, yb + bh + 0.03, lw=2.2, head=14)
    s.text(x0 + bw / 2 + 0.12, ys[1] - 0.3, 'False', size=14, weight='bold', color=MUTE, ha='left')
    s.box(x0, yb, bw, bh, 'else: everyone left', size=16, fill=PAPER, edge=INK, lw=2.0, r=0.05)
    s.arrow(x0 + bw + 0.03, yb + bh / 2, rx - 0.03, yb + bh / 2, lw=2.2, head=14)
    s.box(rx, yb + 0.04, rw, bh - 0.08, results[2], size=18, weight='bold', fill=GOLD if picked == 2 else PAPER, edge=INK, lw=1.8, r=0.05)
    cx = rx + rw + 0.35
    codebox(s, cx, h - 0.9, list(code), size=14, w=w - cx - 0.05)
    return s


# ------------------------------------------------------------------ tiers on a number line, with the edge cases
@fig('x_ds_c_numline')
def ds_c_numline(w, h, top_note='', bands=(), edges=(), bottom='', vmax=8000000, **_):
    """bands: [(from, to, label, sub, fill)]; edges: [(boundary value, left text, right text)]."""
    s = Scene(w, h)
    x0, x1 = 0.5, w - 0.5
    sc = (x1 - x0) / vmax
    X = lambda v: x0 + v * sc
    s.text(w / 2, h - 0.25, top_note, size=18, weight='bold')
    yb, bh = 1.55, 0.7
    for a, b, lab, sub, fill in bands:
        s.rect(X(a), yb, X(b) - X(a), bh, fill=fill, edge=INK, lw=2.0, z=2)
        s.text((X(a) + X(b)) / 2, yb + bh / 2, lab, size=20, weight='bold', z=6)
        s.text((X(a) + X(b)) / 2, yb - 0.3, sub, size=15, color=BODY)
    for v, left, right in edges:
        s.line(X(v), yb + bh + 0.02, X(v), h - 1.25, color=RED, lw=2.6, z=5)
        s.text(X(v) - 0.12, h - 1.0, left, size=16, weight='bold', ha='right')
        s.text(X(v) + 0.12, h - 1.0, right, size=16, weight='bold', ha='left')
        s.text(X(v), yb - 0.75, f'{v:,}', size=15, color=RED, weight='bold')
    s.text(w / 2, 0.35, bottom, size=17, weight='bold', color=RED)
    return s


# ------------------------------------------------------------------ and / or on a number line
@fig('x_ds_c_logic')
def ds_c_logic(w, h, vmax=8000, cuts=(2000, 6000), rows=(), **_):
    """rows: [(label, from, to, fill)] drawn as bars on a 0..vmax axis."""
    s = Scene(w, h)
    x0, x1 = 0.3, w - 0.35
    sc = (x1 - x0) / vmax
    X = lambda v: x0 + v * sc
    y = h - 0.15
    spans = []
    for lab, a, b, fill in rows:
        s.text(x0, y - 0.15, lab, size=16, weight='bold', ha='left')
        y -= 0.38
        s.rect(X(a), y - 0.55, X(b) - X(a), 0.55, fill=fill, edge=INK, lw=1.8, z=2)
        spans.append((y - 0.55, y))
        y -= 0.8
    ya = y + 0.05
    s.line(x0, ya, x1, ya, color=INK, lw=2.0)
    for v in (0,) + tuple(cuts) + (vmax,):
        s.line(X(v), ya + 0.07, X(v), ya - 0.07, color=INK, lw=2.0)
        s.text(X(v), ya - 0.3, f'{v:,}', size=15, ha='center' if 0 < v < vmax else ('left' if v == 0 else 'right'))
    for v in cuts:
        for y0_, y1_ in spans:
            s.line(X(v), y0_, X(v), y1_, color=RED, lw=1.4, dash=True, z=3)
    s.text(w / 2, 0.15, 'points', size=15, color=MUTE)
    return s


# ------------------------------------------------------------------ fill down beside a for loop
@fig('x_ds_c_loop')
def ds_c_loop(w, h, headers=(), rows=(), formula='', code=(), **_):
    s = Scene(w, h)
    size, rh = 15, 0.42
    cws = [max([tw(headers[c], size, 'bold')] + [tw(r[c], size) for r in rows]) + 0.3 for c in range(2)]
    s.text(0.1, h - 0.3, 'Spreadsheet: fill down', size=17, weight='bold', ha='left')
    ytop = h - 0.65
    cells = {(0, 0): PALE, (0, 1): PALE}
    cells.update({(r + 1, 1): GOLD for r in range(len(rows))})
    s.table(0.1, ytop, cws, rh, [list(headers)] + [list(r) for r in rows], header=True, size=size, align=['right', 'right'], hl_cells=cells)
    ybot = ytop - (len(rows) + 1) * rh
    s.text(0.1, ybot - 0.35, formula, size=15, mono=True, ha='left')
    px = 0.1 + sum(cws) + 0.55
    s.text(px, h - 0.3, 'Python: for loop', size=17, weight='bold', ha='left')
    cw, ch = codebox(s, px, h - 0.65, list(code), size=15, w=w - px - 0.05)
    wrap_text(s, px, h - 0.65 - ch - 0.2, w - px - 0.05, 'The indented lines run once for each item in the list. Five items or five thousand: the code stays the same.', 16, color=BODY, ha='left', va='top')
    return s


# ------------------------------------------------------------------ trace table
@fig('x_ds_c_trace')
def ds_c_trace(w, h, code=(), headers=(), rows=(), hl_rows=(), size=15, **_):
    """Code with line numbers on the left; on the right a table of what happens step by step."""
    s = Scene(w, h)
    lines = [f'{i + 1:>2}  {l}' for i, l in enumerate(code)]
    s.text(0.1, h - 0.28, 'The code, with line numbers', size=17, weight='bold', ha='left')
    cw, ch = codebox(s, 0.1, h - 0.55, lines, size=size)
    tx = 0.1 + cw + 0.45
    s.text(tx, h - 0.28, 'What happens, one step at a time', size=17, weight='bold', ha='left')
    avail = w - tx - 0.05
    colw = [max([tw(headers[c], size, 'bold')] + [tw(r[c], size) for r in rows]) + 0.3 for c in range(len(headers))]
    if sum(colw) > avail:
        colw = [c * avail / sum(colw) for c in colw]
    rh = 0.46
    cells = {(0, c): PALE for c in range(len(headers))}
    for r in hl_rows:
        for c in range(len(headers)):
            cells[(r + 1, c)] = GOLD
    s.table(tx, h - 0.55, colw, rh, [list(headers)] + [list(r) for r in rows], header=True, size=size, align=['left'] * len(headers), hl_cells=cells)
    return s


# ------------------------------------------------------------------ a function definition with its parts
@fig('x_ds_c_function')
def ds_c_function(w, h, code=(), parts=(), call='', returned='', **_):
    """parts: [(line index, label)], labels drawn at the right of the code with a leader line."""
    s = Scene(w, h)
    size = 14
    lh = size * 1.5 / 72
    top = h - 0.1
    cw, ch = codebox(s, 0.1, top, list(code), size=size)
    rx = 0.1 + cw + 0.5
    slot = 0.7
    k_ = len(parts)
    for n, (li, t_) in enumerate(parts, 1):
        yy = top - 0.14 - (li + 0.5) * lh
        sy = top - 0.35 - (n - 1) * slot
        s.line(0.1 + cw + 0.03, yy, rx - 0.22, sy, color=INK, lw=1.4, z=1)
        badge(s, rx, sy, n, r=0.16, size=14)
        wrap_text(s, rx + 0.28, sy, w - rx - 0.35, t_, 15, ha='left')
    y = min(top - ch - 0.45, top - 0.35 - (k_ - 1) * slot - 0.75)
    s.text(0.1, y + 0.3, 'Call the function', size=16, weight='bold', ha='left')
    c1w, c1h = codebox(s, 0.1, y, [call], size=16)
    ax = 0.1 + c1w + 0.1
    s.arrow(ax, y - c1h / 2, ax + 0.7, y - c1h / 2, color=RED, lw=2.4, head=16)
    s.box(ax + 0.8, y - c1h / 2 - 0.25, 1.4, 0.5, returned, size=18, mono=True, weight='bold', fill=GOLD, edge=INK, lw=1.8, r=0.05)
    s.text(ax + 1.5, y - c1h / 2 - 0.5, 'return value', size=14, color=MUTE)
    wrap_text(s, 0.1, y - c1h - 0.2, c1w, 'The value in the brackets is the argument.', 15, color=BODY, ha='left', va='top')
    return s


# ------------------------------------------------------------------ test cases
@fig('x_ds_c_tests')
def ds_c_tests(w, h, headers=(), rows=(), status=(), size=20, **_):
    s = Scene(w, h)
    rh = 0.62
    allrows = [list(headers)] + [list(r) + [st] for r, st in zip(rows, status)]
    ncol = len(allrows[0])
    colw = [max(tw(r[c], size, 'bold' if i == 0 else 'regular') for i, r in enumerate(allrows)) + 0.35 for c in range(ncol)]
    cells = {(0, c): PALE for c in range(ncol)}
    for i, st in enumerate(status):
        cells[(i + 1, ncol - 1)] = PAPER if st == 'PASS' else GOLD
    s.table(0.1, h - 0.1, colw, rh, allrows, header=True, size=size, align=['left'] * ncol, hl_cells=cells)
    return s
