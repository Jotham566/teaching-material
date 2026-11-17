"""Generic business diagrams for the executive edition, drawn from data (no drawing code in the content files).

Each diagram is a registered figure `fn(w, h, **data) -> Scene`; content refers to them by name with a data dict, for example
    {'kind': 'flow', 'steps': [{'head': 'Trigger', 'text': 'A new email arrives', 'icon': 'mail'}, ...]}
Text is measured with the real Lato files and the Scene audit rejects overlaps and anything outside the canvas, so a diagram
that does not fit raises LayoutError and the content is shortened.

Kinds: flow, stack, matrix, cycle, bars, timeline, icons, plan, ladder, sheet (headers, rows, hl), card (title, fields), waffle (filled, label), bubbles (items), versus (left, right, middle), confusion (tp, fp, fn, tn), roc, descent (labels), network (layers).
Pictograms: the figkit set plus mail, shield, people, doc, chart, key and robot, added here in the same line style.
"""
import math
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon

import figkit
from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, fig
import slidekit as K


# ------------------------------------------------------------------ extra pictograms
def _i_mail(self, x, y, s, c, a):
    self.ax.add_patch(FancyBboxPatch((x - 0.38 * s, y - 0.26 * s), 0.76 * s, 0.52 * s, boxstyle=f'round,pad=0,rounding_size={0.04 * s}', fc=PAPER, ec=c, lw=2, zorder=2))
    self.line(x - 0.38 * s, y + 0.26 * s, x, y - 0.04 * s, color=c, lw=2, z=3)
    self.line(x + 0.38 * s, y + 0.26 * s, x, y - 0.04 * s, color=c, lw=2, z=3)
    self.circle(x + 0.3 * s, y + 0.26 * s, 0.07 * s, fill=a, edge=c, lw=1.6, z=4)


def _i_shield(self, x, y, s, c, a):
    self.poly([(x - 0.3 * s, y + 0.38 * s), (x + 0.3 * s, y + 0.38 * s), (x + 0.3 * s, y - 0.02 * s), (x, y - 0.42 * s), (x - 0.3 * s, y - 0.02 * s)], fill=a, edge=c, lw=2)
    self.line(x - 0.12 * s, y, x - 0.03 * s, y - 0.1 * s, color=c, lw=3, z=4)
    self.line(x - 0.03 * s, y - 0.1 * s, x + 0.14 * s, y + 0.12 * s, color=c, lw=3, z=4)


def _i_people(self, x, y, s, c, a):
    for dx, col in ((-0.22, PAPER), (0.22, PAPER), (0.0, a)):
        yy = y + (0.02 if dx == 0 else -0.04) * s
        self.circle(x + dx * s, yy + 0.2 * s, 0.11 * s, fill=PAPER, edge=c, lw=1.8, z=3)
        self.ax.add_patch(FancyBboxPatch((x + dx * s - 0.17 * s, yy - 0.3 * s), 0.34 * s, 0.38 * s, boxstyle=f'round,pad=0,rounding_size={0.12 * s}', fc=col, ec=c, lw=1.8, zorder=2 if dx else 3))


def _i_doc(self, x, y, s, c, a):
    self.poly([(x - 0.26 * s, y + 0.4 * s), (x + 0.12 * s, y + 0.4 * s), (x + 0.28 * s, y + 0.24 * s), (x + 0.28 * s, y - 0.4 * s), (x - 0.26 * s, y - 0.4 * s)], fill=PAPER, edge=c, lw=2)
    for i in range(4):
        self.line(x - 0.16 * s, y + 0.12 * s - i * 0.14 * s, x + 0.18 * s, y + 0.12 * s - i * 0.14 * s, color=GREY, lw=1.4, z=3)
    self.circle(x + 0.12 * s, y - 0.28 * s, 0.07 * s, fill=a, edge=c, lw=1.4, z=4)


def _i_chart(self, x, y, s, c, a):
    self.line(x - 0.36 * s, y - 0.34 * s, x + 0.36 * s, y - 0.34 * s, color=c, lw=2)
    self.line(x - 0.36 * s, y - 0.34 * s, x - 0.36 * s, y + 0.36 * s, color=c, lw=2)
    pts = [(x - 0.26 * s, y - 0.18 * s), (x - 0.06 * s, y + 0.02 * s), (x + 0.1 * s, y - 0.08 * s), (x + 0.3 * s, y + 0.28 * s)]
    for p, q in zip(pts, pts[1:]):
        self.line(p[0], p[1], q[0], q[1], color=c, lw=2.4, z=3)
    for p in pts:
        self.circle(p[0], p[1], 0.05 * s, fill=a, edge=c, lw=1.4, z=4)


def _i_key(self, x, y, s, c, a):
    self.circle(x - 0.2 * s, y, 0.17 * s, fill=a, edge=c, lw=2)
    self.line(x - 0.03 * s, y, x + 0.36 * s, y, color=c, lw=2.6)
    self.line(x + 0.22 * s, y, x + 0.22 * s, y - 0.12 * s, color=c, lw=2.4)
    self.line(x + 0.34 * s, y, x + 0.34 * s, y - 0.12 * s, color=c, lw=2.4)


def _i_robot(self, x, y, s, c, a):
    self.ax.add_patch(FancyBboxPatch((x - 0.3 * s, y - 0.28 * s), 0.6 * s, 0.5 * s, boxstyle=f'round,pad=0,rounding_size={0.08 * s}', fc=PAPER, ec=c, lw=2, zorder=2))
    self.circle(x - 0.12 * s, y - 0.03 * s, 0.06 * s, fill=a, edge=c, lw=1.4, z=4)
    self.circle(x + 0.12 * s, y - 0.03 * s, 0.06 * s, fill=a, edge=c, lw=1.4, z=4)
    self.line(x - 0.1 * s, y - 0.17 * s, x + 0.1 * s, y - 0.17 * s, color=c, lw=1.8, z=4)
    self.line(x, y + 0.22 * s, x, y + 0.36 * s, color=c, lw=2)
    self.circle(x, y + 0.4 * s, 0.05 * s, fill=RED, edge=c, lw=1.2, z=4)


for _n, _f in (('mail', _i_mail), ('shield', _i_shield), ('people', _i_people), ('doc', _i_doc), ('chart', _i_chart), ('key', _i_key), ('robot', _i_robot)):
    setattr(Scene, '_i_' + _n, _f)


def _i_question(self, x, y, s, c, a):
    self.circle(x, y, 0.38 * s, fill=a, edge=c, lw=2.2)
    self.text(x, y - 0.02 * s, '?', size=max(14, 34 * s), weight='bold', color=c, z=6)


def _i_speech(self, x, y, s, c, a):
    self.ax.add_patch(FancyBboxPatch((x - 0.38 * s, y - 0.2 * s), 0.76 * s, 0.52 * s, boxstyle=f'round,pad=0,rounding_size={0.12 * s}', fc=PAPER, ec=c, lw=2, zorder=2))
    self.poly([(x - 0.18 * s, y - 0.2 * s), (x - 0.3 * s, y - 0.42 * s), (x, y - 0.2 * s)], fill=PAPER, edge=c, lw=2)
    for dx in (-0.18, 0, 0.18):
        self.circle(x + dx * s, y + 0.06 * s, 0.045 * s, fill=a, edge=c, lw=1.2, z=4)


def _i_flag(self, x, y, s, c, a):
    self.line(x - 0.22 * s, y - 0.4 * s, x - 0.22 * s, y + 0.4 * s, color=c, lw=2.6)
    self.poly([(x - 0.22 * s, y + 0.38 * s), (x + 0.32 * s, y + 0.22 * s), (x - 0.22 * s, y + 0.04 * s)], fill=a, edge=c, lw=2)


def _i_bell(self, x, y, s, c, a):
    self.poly([(x - 0.3 * s, y - 0.18 * s), (x - 0.2 * s, y + 0.15 * s), (x - 0.1 * s, y + 0.34 * s), (x + 0.1 * s, y + 0.34 * s), (x + 0.2 * s, y + 0.15 * s), (x + 0.3 * s, y - 0.18 * s)], fill=a, edge=c, lw=2)
    self.line(x - 0.34 * s, y - 0.18 * s, x + 0.34 * s, y - 0.18 * s, color=c, lw=2.2)
    self.circle(x, y - 0.3 * s, 0.07 * s, fill=c, edge=c, lw=1, z=4)


def _i_switch(self, x, y, s, c, a):
    self.ax.add_patch(FancyBboxPatch((x - 0.38 * s, y - 0.18 * s), 0.76 * s, 0.36 * s, boxstyle=f'round,pad=0,rounding_size={0.18 * s}', fc=a, ec=c, lw=2, zorder=2))
    self.circle(x + 0.2 * s, y, 0.14 * s, fill=PAPER, edge=c, lw=2, z=4)


def _i_grid(self, x, y, s, c, a):
    for i in range(3):
        for j in range(3):
            self.rect(x - 0.3 * s + j * 0.2 * s, y - 0.3 * s + i * 0.2 * s, 0.2 * s, 0.2 * s, fill=a if (i == 0 or j == 0) else PAPER, edge=c, lw=1.6)


def _i_stamp(self, x, y, s, c, a):
    self.circle(x, y + 0.05 * s, 0.3 * s, fill=PAPER, edge=c, lw=2.2)
    self.circle(x, y + 0.05 * s, 0.2 * s, fill=a, edge=c, lw=1.6)
    self.line(x - 0.34 * s, y - 0.36 * s, x + 0.34 * s, y - 0.36 * s, color=c, lw=2.6)


for _n, _f in (('question', _i_question), ('speech', _i_speech), ('flag', _i_flag), ('bell', _i_bell), ('switch', _i_switch), ('grid', _i_grid), ('stamp', _i_stamp)):
    setattr(Scene, '_i_' + _n, _f)


ICONS = ['person', 'shop', 'laptop', 'notebook', 'folder', 'tag', 'bag', 'cloud', 'magnifier', 'calculator', 'clock', 'coin', 'bars', 'receipt', 'check', 'cross',
         'phone', 'calendar', 'home', 'gear', 'lock', 'pin', 'mail', 'shield', 'people', 'doc', 'chart', 'key', 'robot', 'question', 'speech', 'flag', 'bell', 'switch', 'grid', 'stamp', 'book']


def _wrap(s, x, y, w, text, size, weight='normal', color=INK, ha='center', va='center'):
    """Draw wrapped text in a column of width w; returns its height in inches."""
    kind = 'bold' if weight == 'bold' else 'regular'
    lines = K.wrap(text, size, kind, w)
    s.text(x, y, '\n'.join(lines), size=size, weight=weight, color=color, ha=ha, va=va)
    return len(lines) * size * 1.15 / 72.0


def _lines(text, size, w, weight='normal'):
    return len(K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', w))


# ------------------------------------------------------------------ flow
@fig('x_flow')
def x_flow(w, h, steps=(), highlight=None, head_size=20, text_size=17, **_):
    s = Scene(w, h)
    n = len(steps)
    gap = 0.42
    bw = (w - 0.1 - gap * (n - 1)) / n
    inner = bw - 0.3
    has_icon = any(st.get('icon') for st in steps)
    content_h = []
    for st in steps:
        hh = _lines(st['head'], head_size, inner, 'bold') * head_size * 1.15 / 72 + 0.1
        if st.get('text'):
            hh += _lines(st['text'], text_size, inner) * text_size * 1.15 / 72 + 0.1
        content_h.append(hh)
    bh = max(content_h) + (0.95 if has_icon else 0.0) + 0.4
    bh = min(bh, h - 0.2)
    y0 = (h - bh) / 2
    for i, st in enumerate(steps):
        x = 0.05 + i * (bw + gap)
        fill = GOLD if highlight == i else PAPER
        s.box(x, y0, bw, bh, '', fill=fill, edge=INK, lw=2.0, r=0.07)
        top = y0 + bh - 0.2
        if st.get('icon'):
            s.icon(st['icon'], x + bw / 2, top - 0.42, 0.9)
            top -= 0.95
        hh = _lines(st['head'], head_size, inner, 'bold') * head_size * 1.15 / 72
        _wrap(s, x + bw / 2, top - hh / 2, inner, st['head'], head_size, 'bold')
        top -= hh + 0.12
        if st.get('text'):
            th = _lines(st['text'], text_size, inner) * text_size * 1.15 / 72
            _wrap(s, x + bw / 2, top - th / 2, inner, st['text'], text_size, color=BODY)
        if i < n - 1:
            s.arrow(x + bw + 0.04, y0 + bh / 2, x + bw + gap - 0.04, y0 + bh / 2, lw=2.4, head=18)
    return s


# ------------------------------------------------------------------ stack (layers, top to bottom)
@fig('x_stack')
def x_stack(w, h, layers=(), highlight=None, head_size=20, text_size=17, side=None, **_):
    s = Scene(w, h)
    n = len(layers)
    gap = 0.14
    lh = (h - 0.1 - gap * (n - 1)) / n
    x0 = 0.05
    bw = w - 0.1
    for i, ly in enumerate(layers):
        y = h - 0.05 - (i + 1) * lh - i * gap
        s.box(x0, y, bw, lh, '', fill=GOLD if highlight == i else PAPER, edge=INK, lw=2.0, r=0.07)
        if ly.get('icon'):
            s.icon(ly['icon'], x0 + 0.55, y + lh / 2, 0.7)
            tx = x0 + 1.15
        else:
            tx = x0 + 0.3
        hw = 3.2
        _wrap(s, tx, y + lh / 2, hw, ly['head'], head_size, 'bold', ha='left')
        if ly.get('text'):
            _wrap(s, tx + hw + 0.2, y + lh / 2, bw - (tx - x0) - hw - 0.5, ly['text'], text_size, color=BODY, ha='left')
    return s


# ------------------------------------------------------------------ 2x2 matrix
@fig('x_matrix')
def x_matrix(w, h, x_label='', y_label='', quadrants=('', '', '', ''), points=(), size=17, **_):
    s = Scene(w, h)
    ml, mb = 0.9, 0.7
    gx0, gy0, gw, gh = ml, mb, w - ml - 0.1, h - mb - 0.1
    s.rect(gx0, gy0, gw, gh, fill=PAPER, edge=INK, lw=2)
    s.line(gx0 + gw / 2, gy0, gx0 + gw / 2, gy0 + gh, color=HAIR, lw=1.6)
    s.line(gx0, gy0 + gh / 2, gx0 + gw, gy0 + gh / 2, color=HAIR, lw=1.6)
    pos = [(gx0 + 0.15, gy0 + gh - 0.2, 'left'), (gx0 + gw - 0.15, gy0 + gh - 0.2, 'right'), (gx0 + 0.15, gy0 + 0.2, 'left'), (gx0 + gw - 0.15, gy0 + 0.2, 'right')]
    for q, (qx, qy, ha) in zip(quadrants, pos):
        if q:
            s.text(qx, qy, q, size=15, color=MUTE, weight='bold', ha=ha)
    s.text(gx0 + gw / 2, 0.28, x_label, size=17, color=BODY)
    s.text(0.3, gy0 + gh / 2, y_label, size=17, color=BODY, rot=90)
    for p in points:
        px = gx0 + 0.45 + p['x'] * (gw - 0.9)
        py = gy0 + 0.55 + p['y'] * (gh - 1.1)
        s.circle(px, py, 0.13, fill=GOLD if p.get('hl') else PAPER, edge=INK, lw=2, z=4)
        left = p['x'] > 0.55
        s.text(px - 0.22 if left else px + 0.22, py, p['label'], size=size, ha='right' if left else 'left', weight='bold' if p.get('hl') else 'normal')
    return s


# ------------------------------------------------------------------ cycle
@fig('x_cycle')
def x_cycle(w, h, items=(), center='', size=18, **_):
    s = Scene(w, h)
    n = len(items)
    cx, cy = w / 2, h / 2
    rx, ry = w / 2 - 1.55, h / 2 - 0.62
    bw, bh = 2.7, 0.9
    pts = []
    for i in range(n):
        a = math.pi / 2 - 2 * math.pi * i / n
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    for i, (x, y) in enumerate(pts):
        nx, ny = pts[(i + 1) % n]
        s.arrow(x + (nx - x) * 0.34, y + (ny - y) * 0.34, x + (nx - x) * 0.66, y + (ny - y) * 0.66, lw=2.2, head=16, rad=-0.2)
    for (x, y), t in zip(pts, items):
        s.box(x - bw / 2, y - bh / 2, bw, bh, '', fill=PAPER, edge=INK, lw=2.0, r=0.07, z=3)
        _wrap(s, x, y, bw - 0.2, t, size, 'bold')
    if center:
        _wrap(s, cx, cy, 2.6, center, 20, color=MUTE)
    return s


# ------------------------------------------------------------------ bars
@fig('x_bars')
def x_bars(w, h, items=(), unit='', size=18, max_value=None, **_):
    s = Scene(w, h)
    n = len(items)
    lab_w = 3.4
    mv = max_value or max(i['value'] for i in items)
    row = (h - 0.2) / n
    bx0 = lab_w + 0.2
    bar_w = w - bx0 - 1.6
    for i, it in enumerate(items):
        yc = h - 0.1 - (i + 0.5) * row
        _wrap(s, lab_w, yc, lab_w - 0.1, it['label'], size, ha='right')
        bw = max(0.04, bar_w * it['value'] / mv)
        s.rect(bx0, yc - row * 0.28, bw, row * 0.56, fill=GOLD if it.get('hl') else INK if it.get('dark') else PAPER, edge=INK, lw=2)
        s.text(bx0 + bw + 0.15, yc, f"{it['value']:g}{unit}" if not it.get('text') else it['text'], size=size, weight='bold', ha='left')
    return s


# ------------------------------------------------------------------ timeline
@fig('x_timeline')
def x_timeline(w, h, items=(), size=17, **_):
    s = Scene(w, h)
    n = len(items)
    y = h * 0.52
    s.line(0.2, y, w - 0.2, y, color=INK, lw=3)
    seg = (w - 0.4) / n
    for i, it in enumerate(items):
        x = 0.2 + seg * (i + 0.5)
        s.circle(x, y, 0.14, fill=GOLD if it.get('hl') else PAPER, edge=INK, lw=2.4, z=4)
        _wrap(s, x, y + 0.75, seg - 0.2, it['when'], 20, 'bold')
        _wrap(s, x, y - 0.8, seg - 0.2, it['what'], size, color=BODY)
    return s


# ------------------------------------------------------------------ icon columns
@fig('x_icons')
def x_icons(w, h, items=(), head_size=20, text_size=17, **_):
    s = Scene(w, h)
    n = len(items)
    seg = (w - 0.1) / n
    for i, it in enumerate(items):
        x = 0.05 + seg * (i + 0.5)
        s.icon(it['icon'], x, h - 0.9, 1.3)
        hh = _wrap(s, x, h - 1.95, seg - 0.3, it['head'], head_size, 'bold')
        if it.get('text'):
            th = _lines(it['text'], text_size, seg - 0.3) * text_size * 1.15 / 72
            _wrap(s, x, h - 1.95 - hh / 2 - 0.15 - th / 2, seg - 0.3, it['text'], text_size, color=BODY)
    return s


# ------------------------------------------------------------------ plan (clock bars)
@fig('x_plan')
def x_plan(w, h, parts=(), **_):
    s = Scene(w, h)
    n = len(parts)
    row = h / n
    mx = max(m for _, m in parts)
    t = 0
    for i, (label, m) in enumerate(parts):
        yc = h - (i + 0.5) * row
        s.text(0.95, yc, f'{t // 60}:{t % 60:02d}', size=17, color=MUTE, ha='right')
        bw = max(0.5, 3.2 * m / mx)
        s.box(1.15, yc - row * 0.3, bw, row * 0.6, str(m), size=18, weight='bold', fill=GOLD if label.startswith(('Your', 'Lab')) else INK if m >= 25 else PAPER,
              color=INK if (label.startswith(('Your', 'Lab')) or m < 25) else PAPER, edge=INK, lw=1.8, r=0.05)
        s.text(1.15 + 3.2 + 0.35, yc, label, size=19, ha='left')
        t += m
    return s


# ------------------------------------------------------------------ ladder (levels from low to high, bottom to top)
@fig('x_ladder')
def x_ladder(w, h, items=(), size=19, **_):
    s = Scene(w, h)
    n = len(items)
    step_h = (h - 0.1) / n
    for i, it in enumerate(items):
        x = 0.05 + i * (w - 0.1 - 5.0) / max(1, n - 1)
        y = 0.05 + i * step_h
        s.box(x, y, 5.0, step_h - 0.12, '', fill=GOLD if it.get('hl') else PAPER, edge=INK, lw=2, r=0.06)
        _wrap(s, x + 0.2, y + (step_h - 0.12) / 2, 4.6, it['head'] + (': ' + it['text'] if it.get('text') else ''), size, ha='left')
    return s


# ------------------------------------------------------------------ sheet: a spreadsheet thumbnail (what a finished template looks like)
@fig('x_sheet')
def x_sheet(w, h, headers=(), rows=(), hl=None, size=18, **_):
    """headers: column titles; rows: lists of cell texts (example values); hl: [row, col] of one cell to highlight in gold."""
    s = Scene(w, h)
    n = len(headers)
    for sz in range(int(size), 13, -1):
        raw = [max([K.width_in(str(headers[c]), sz, 'bold')] + [K.width_in(str(r[c]), sz) for r in rows]) + 0.3 for c in range(n)]
        if sum(raw) + 0.5 <= w:
            break
    cw = [min(x, 3.2) for x in raw]
    scale = (w - 0.1 - 0.5) / sum(cw)
    cw = [c * scale for c in cw] if scale < 1 or scale > 1.0 else cw
    if sum(cw) < w - 0.6:
        extra = (w - 0.6 - sum(cw)) / n
        cw = [c + extra for c in cw]
    lh = sz * 1.15 / 72
    def cell_lines(txt, wd):
        return K.wrap(str(txt), sz, 'regular', wd - 0.2)
    heights = [max([len(K.wrap(str(headers[c]), sz, 'bold', cw[c] - 0.2)) for c in range(n)]) * lh + 0.2]
    for r in rows:
        heights.append(max(len(cell_lines(r[c], cw[c])) for c in range(n)) * lh + 0.18)
    total = sum(heights) + 0.38
    top = h - 0.05
    x0 = 0.5
    s.rect(x0, top - total, sum(cw), total, fill=PAPER, edge=INK, lw=1.8)
    letters = 'ABCDEFGH'
    cx = x0
    for c in range(n):
        s.text(cx + cw[c] / 2, top - 0.19, letters[c], size=14, color=GREY)
        cx += cw[c]
    s.line(x0, top - 0.38, x0 + sum(cw), top - 0.38, color=HAIR, lw=1.2)
    y = top - 0.38
    for ri, hh in enumerate(heights):
        cx = x0
        if ri == 0:
            s.rect(x0, y - hh, sum(cw), hh, fill=PAPER, edge=PAPER, lw=0)
        for c in range(n):
            txt = headers[c] if ri == 0 else rows[ri - 1][c]
            lines = K.wrap(str(txt), sz, 'bold' if ri == 0 else 'regular', cw[c] - 0.2)
            if hl and ri > 0 and hl[0] == ri - 1 and hl[1] == c:
                s.rect(cx + 0.02, y - hh + 0.02, cw[c] - 0.04, hh - 0.04, fill=GOLD, edge=GOLD, lw=0, z=2)
            s.text(cx + 0.1, y - hh / 2, '\n'.join(lines), size=sz, weight='bold' if ri == 0 else 'normal', ha='left', color=INK if ri == 0 else BODY, z=5)
            cx += cw[c]
        if ri == 0:
            s.line(x0, y - hh, x0 + sum(cw), y - hh, color=INK, lw=2.0, z=4)
        else:
            s.line(x0, y - hh, x0 + sum(cw), y - hh, color=HAIR, lw=1.0, z=3)
        s.text(x0 - 0.28, y - hh / 2, '' if ri == 0 else str(ri), size=14, color=GREY)
        y -= hh
    return s


# ------------------------------------------------------------------ card: a one-page form with labelled lines
@fig('x_card')
def x_card(w, h, title='', fields=(), size=19, **_):
    """fields: [{'label': ..., 'value': ...}]; the value is shown as an example in grey italic."""
    s = Scene(w, h)
    s.rect(0.05, 0.05, w - 0.1, h - 0.1, fill=PAPER, edge=INK, lw=2.0)
    s.rect(0.05, h - 0.75, w - 0.1, 0.7, fill=INK, edge=INK, lw=0, z=3)
    s.text(0.3, h - 0.4, title, size=19, weight='bold', color=PAPER, ha='left', z=6)
    n = len(fields)
    row = (h - 0.95) / n
    for size in range(int(size), 13, -1):
        if all(0.3 + len(K.wrap(f['value'], size, 'italic', w - 0.8)) * size * 1.2 / 72 <= row for f in fields):
            break
    for i, f in enumerate(fields):
        yc = h - 0.75 - (i + 0.5) * row
        s.text(0.3, yc + row * 0.2, f['label'], size=14, weight='bold', color=MUTE, ha='left')
        val = '\n'.join(K.wrap(f['value'], size, 'italic', w - 0.8))
        s.text(0.3, yc - row * 0.12, val, size=size, color=BODY, ha='left', italic=True)
        s.line(0.3, h - 0.75 - (i + 1) * row + 0.05, w - 0.3, h - 0.75 - (i + 1) * row + 0.05, color=HAIR, lw=1.0)
    return s


# ------------------------------------------------------------------ waffle: n out of 100
@fig('x_waffle')
def x_waffle(w, h, filled=50, label='', size=18, **_):
    s = Scene(w, h)
    lab = K.wrap(label, size, 'regular', w - 0.2) if label else []
    side = min(w, h - (0.25 + len(lab) * size * 1.2 / 72 if label else 0.05)) - 0.1
    r = side / 10 / 2
    x0 = (w - side) / 2
    y0 = h - 0.05 - side
    k = 0
    for row in range(10):
        for col in range(10):
            on = k < filled
            s.circle(x0 + col * 2 * r + r, y0 + (9 - row) * 2 * r + r, r * 0.8, fill=GOLD if on else PAPER, edge=INK, lw=1.4 if on else 1.0)
            k += 1
    if label:
        s.text(w / 2, 0.1 + len(lab) * size * 1.2 / 72 / 2, '\n'.join(lab), size=size, color=BODY)
    return s


# ------------------------------------------------------------------ bubbles: messages with optional tags
@fig('x_bubbles')
def x_bubbles(w, h, items=(), size=17, **_):
    """items: [{'who': 'Shop owner', 'text': '...', 'tag': 'Order', 'hl': False}]"""
    s = Scene(w, h)
    n = len(items)
    gap = 0.15
    bh = (h - 0.1 - gap * (n - 1)) / n
    for i, it in enumerate(items):
        y = h - 0.05 - (i + 1) * bh - i * gap
        s.box(0.05, y, w - 0.1, bh, '', fill=GOLD if it.get('hl') else PAPER, edge=INK, lw=1.8, r=0.1)
        s.icon('person', 0.55, y + bh / 2, 0.75)
        tw = 0
        if it.get('tag'):
            tw = s.tag(w - 0.3 - (0.13 * len(it['tag']) * 16 / 16 + 0.32), y + bh / 2 - 0.2, it['tag'], size=15, fill=RED if it.get('red') else INK)
        short = bh < 1.3
        txt = (it['who'] + ': ' + it['text']) if (short and it.get('who')) else it['text']
        body = '\n'.join(K.wrap(txt, size, 'regular', w - 1.3 - (tw + 0.4 if it.get('tag') else 0.2)))
        s.text(1.05, y + bh / 2 + (0.2 if (it.get('who') and not short) else 0), body, size=size, ha='left')
        if it.get('who') and not short:
            s.text(1.05, y + bh - 0.2, it['who'], size=14, color=MUTE, weight='bold', ha='left')
    return s


# ------------------------------------------------------------------ versus: before and after numbers
@fig('x_versus')
def x_versus(w, h, left=None, right=None, middle='', size=18, **_):
    """left/right: {'head': 'By hand', 'big': '90', 'unit': 'minutes', 'icon': 'person'}; middle: text under the arrow."""
    s = Scene(w, h)
    pw = (w - 2.6) / 2
    for i, side in enumerate((left, right)):
        x = 0.05 + i * (pw + 2.5)
        s.box(x, 0.05, pw, h - 0.1, '', fill=GOLD if i else PAPER, edge=INK, lw=2.0, r=0.08)
        s.icon(side.get('icon', 'clock'), x + pw / 2, h - 1.0, 1.1)
        s.text(x + pw / 2, h - 1.95, side['head'], size=22, weight='bold')
        s.text(x + pw / 2, h / 2 - 0.55, side['big'], size=60, weight='bold')
        s.text(x + pw / 2, 1.0, side.get('unit', ''), size=size, color=BODY)
    s.arrow(0.05 + pw + 0.2, h / 2, 0.05 + pw + 2.3, h / 2, lw=3, head=22)
    if middle:
        _wrap(s, 0.05 + pw + 1.25, h / 2 - 0.65, 2.0, middle, 17, 'bold', color=RED)
    return s


# ------------------------------------------------------------------ descent: gradient descent as walking downhill
@fig('x_descent')
def x_descent(w, h, labels=('Start: a big error', 'Each step: adjust a little', 'Bottom: the smallest\nerror we can find'), size=17, **_):
    import numpy as np
    s = Scene(w, h)
    x0, x1, y0, y1 = 0.7, w - 0.4, 0.7, h - 0.5
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    s.text((x0 + x1) / 2, 0.3, 'the setting the model can change', size=16, color=MUTE)
    s.text(0.3, (y0 + y1) / 2, 'error', size=16, color=MUTE, rot=90)
    xs = np.linspace(0, 1, 120)
    curve = lambda u: 0.12 + 0.88 * (2 * u - 1) ** 2
    px = lambda u: x0 + 0.25 + u * (x1 - x0 - 0.5)
    py = lambda v: y0 + 0.15 + v * (y1 - y0 - 0.3)
    s.ax.plot([px(u) for u in xs], [py(curve(u)) for u in xs], color=INK, lw=3, zorder=3)
    steps = [0.05, 0.2, 0.33, 0.42, 0.47, 0.5]
    for i, u in enumerate(steps):
        s.circle(px(u), py(curve(u)), 0.13 if i not in (0, len(steps) - 1) else 0.17, fill=GOLD if i in (0, len(steps) - 1) else PAPER, edge=INK, lw=2, z=5)
        if i:
            s.arrow(px(steps[i - 1]) + 0.1, py(curve(steps[i - 1])) - 0.05, px(u) - 0.1, py(curve(u)) + 0.05, color=RED, lw=2, head=14, z=4)
    s.text(px(0.05) + 0.25, py(curve(0.05)) + 0.15, labels[0], size=size, ha='left', weight='bold')
    s.text(px(0.5), py(0.72), labels[1], size=size, color=RED, weight='bold')
    s.text(px(0.55), py(0.40), labels[2], size=size, ha='center', weight='bold')
    return s


# ------------------------------------------------------------------ network: layers with the error flowing back
@fig('x_network')
def x_network(w, h, layers=(('Inputs', 3), ('Hidden layer', 4), ('Hidden layer', 4), ('Output', 1)), size=16, **_):
    s = Scene(w, h)
    n = len(layers)
    xs = [0.9 + i * (w - 1.8) / (n - 1) for i in range(n)]
    pos = []
    for (nm, k), x in zip(layers, xs):
        col = []
        for j in range(k):
            y = 0.95 + (h - 2.55) * (j + 0.5) / k
            col.append((x, y))
        pos.append(col)
        s.text(x, h - 0.35, nm, size=size, weight='bold')
    for a, b in zip(pos, pos[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b:
                s.line(x1, y1, x2, y2, color=HAIR, lw=1.2, z=1)
    for col in pos:
        for (x, y) in col:
            s.circle(x, y, 0.2, fill=PAPER, edge=INK, lw=2, z=4)
    s.circle(pos[-1][0][0], pos[-1][0][1], 0.26, fill=GOLD, edge=INK, lw=2.4, z=5)
    s.arrow(xs[0] + 0.3, 0.38, xs[-1] - 0.3, 0.38, color=INK, lw=2.4, head=16)
    s.text((xs[0] + xs[-1]) / 2, 0.08 + 0.02, 'forward: the guess', size=size, color=INK)
    s.arrow(xs[-1] - 0.3, h - 1.2, xs[0] + 0.3, h - 1.2, color=RED, lw=2.4, head=16)
    s.text((xs[0] + xs[-1]) / 2, h - 0.85, 'backward: share out the blame for the error, then adjust each connection', size=size, color=RED, weight='bold')
    return s


# ------------------------------------------------------------------ confusion matrix
@fig('x_confusion')
def x_confusion(w, h, tp=8, fp=12, fn=2, tn=978, size=18, **_):
    """2 x 2 grid: rows are what the model said, columns what was true; counts in the cells."""
    s = Scene(w, h)
    lw_, top = 1.9, 0.9
    cw = (w - lw_ - 0.1) / 2
    ch = (h - top - 0.1) / 2
    x0 = lw_
    s.text(x0 + cw / 2, h - 0.45, 'Really fraud', size=size, weight='bold')
    s.text(x0 + cw * 1.5, h - 0.45, 'Really fine', size=size, weight='bold')
    s.text(lw_ / 2, 0.1 + ch * 1.5, 'Model said\n"fraud"', size=size, weight='bold')
    s.text(lw_ / 2, 0.1 + ch * 0.5, 'Model said\n"fine"', size=size, weight='bold')
    cells = [(0, 1, tp, 'True positive', 'caught', GOLD), (1, 1, fp, 'False positive', 'false alarm', PAPER),
             (0, 0, fn, 'False negative', 'missed', PAPER), (1, 0, tn, 'True negative', 'rightly cleared', PAPER)]
    for cx, cy, n, nm, sub, fill in cells:
        x = x0 + cx * cw + 0.05
        y = 0.1 + cy * ch + 0.05
        s.box(x, y, cw - 0.1, ch - 0.1, '', fill=fill, edge=INK, lw=2.0, r=0.06)
        s.text(x + (cw - 0.1) / 2, y + (ch - 0.1) * 0.66, f'{n:,}', size=36, weight='bold')
        s.text(x + (cw - 0.1) / 2, y + (ch - 0.1) * 0.26, nm + '\n' + sub, size=size - 3, color=BODY)
    return s


# ------------------------------------------------------------------ roc curve
@fig('x_roc')
def x_roc(w, h, size=16, **_):
    import numpy as np
    s = Scene(w, h)
    x0, x1, y0, y1 = 0.9, w - 0.3, 0.8, h - 0.3
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    s.text((x0 + x1) / 2, 0.3, 'false alarm rate (of the really fine cases)', size=size, color=MUTE)
    s.text(0.3, (y0 + y1) / 2, 'catch rate (of the really fraud cases)', size=size, color=MUTE, rot=90)
    px = lambda u: x0 + u * (x1 - x0)
    py = lambda v: y0 + v * (y1 - y0)
    us = np.linspace(0, 1, 80)
    curve = lambda u: u ** 0.163
    s.ax.fill_between([px(u) for u in us], [py(u) for u in us], [py(curve(u)) for u in us], color=GOLD, alpha=0.45, zorder=1)
    s.ax.plot([px(0), px(1)], [py(0), py(1)], color=MUTE, lw=2, ls='--', zorder=2)
    s.ax.plot([px(u) for u in us], [py(curve(u)) for u in us], color=INK, lw=3.4, zorder=3)
    s.circle(px(0.1), py(curve(0.1)), 0.11, fill=RED, edge=INK, lw=1.6, z=5)
    s.text(px(0.1) + 0.2, py(curve(0.1)) - 0.3, 'one threshold', size=size, ha='left', color=RED, weight='bold')
    s.text(px(0.76), py(0.30), 'Dashed line:\na coin flip, AUC 0.5', size=size, color=MUTE)
    s.text(px(0.45), py(0.68), 'Gold area = AUC', size=size, ha='center', weight='bold')
    return s



def render(data, w, h):
    """Render a diagram data dict {'kind': ..., ...} at w x h inches and return the PNG path."""
    kind = data['kind']
    params = {k: v for k, v in data.items() if k != 'kind'}
    return figkit.render_figure('x_' + kind, w, h, params)


import diagrams_ml  # noqa: E402,F401  (registers scatter, rowsplit, tree)

for _m in ('diagrams_ml_c2', 'diagrams_ml_c3', 'diagrams_ml_c4'):   # per-class figure kinds, each in its own file
    try:
        __import__(_m)
    except ModuleNotFoundError:
        pass
