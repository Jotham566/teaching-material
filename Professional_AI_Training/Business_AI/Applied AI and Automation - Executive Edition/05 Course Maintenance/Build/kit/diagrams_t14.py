"""Figure kinds for Session 14 (Data readiness assessment, roadmap and 90-day plan). Auto-imported by diagrams.py.

t14_fivekinds : the five kinds of data, an NVF example of each and the first action that makes it ready.
t14_docjourney: one document from paper to an index a model can search, and whether a model can use it at each stage.
t14_course    : the 14 sessions as one picture, in three rows.
t14_shelf     : everything the learner now holds, as tiles grouped by purpose.
t14_checkins  : the day 0, 30, 60 and 90 timeline with what you bring and the test at each check-in.
"""
from figkit import Scene, INK, BODY, MUTE, HAIR, PAPER, RED, GOLD, GREY, LayoutError, fig
import slidekit as K


def _fit_text(s, x, y, w, h, text, size, weight='normal', color=INK, ha='center', pad=0.1, italic=False):
    ls = K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', w - 2 * pad)
    th = len(ls) * size * 1.17 / 72.0
    if th > h - 0.02:
        raise LayoutError(f'text too tall for its box: {text!r} needs {th:.2f} in, has {h - 0.02:.2f}')
    tx = x + w / 2 if ha == 'center' else x + pad
    s.text(tx, y + h / 2, '\n'.join(ls), size=size, weight=weight, color=color, ha=ha, italic=italic)


# ------------------------------------------------------------------ five kinds
@fig('x_t14_fivekinds')
def x_t14_fivekinds(w, h, items=(), size=15, **_):
    """items: [{icon, head, example, action}]"""
    s = Scene(w, h)
    n = len(items)
    cw = (w - 0.04) / n
    for i, it in enumerate(items):
        x = 0.02 + i * cw
        cx = x + cw / 2
        s.icon(it['icon'], cx, h - 0.5, 0.8)
        s.text(cx, h - 1.12, it['head'], size=size + 3, weight='bold')
        s.box(x + 0.08, h - 2.4, cw - 0.16, 1.05, '', fill=PAPER, edge=INK, lw=1.6)
        _fit_text(s, x + 0.08, h - 2.4, cw - 0.16, 1.05, it['example'], size)
        s.arrow(cx, h - 2.45, cx, h - 2.85, lw=2.2, head=14)
        s.box(x + 0.08, 0.03, cw - 0.16, h - 2.95, '', fill=GOLD, edge=INK, lw=1.6)
        _fit_text(s, x + 0.08, 0.03, cw - 0.16, h - 2.95, it['action'], size, weight='bold')
    return s


# ------------------------------------------------------------------ document journey
@fig('x_t14_docjourney')
def x_t14_docjourney(w, h, stages=(), size=15, **_):
    """stages: [{head, sub, use, ok}] five stages, ok True gives a gold badge."""
    s = Scene(w, h)
    n = len(stages)
    cw = (w - 0.04) / n
    top = h - 0.1
    for i, st in enumerate(stages):
        x = 0.02 + i * cw
        cx = x + cw / 2
        pw, ph = 0.95, 1.3
        px, py = cx - pw / 2, top - 1.55
        if i in (0, 1, 2):
            s.rect(px, py, pw, ph, fill=PAPER, edge=INK, lw=1.8)
        if i == 0:
            for k in range(6):
                s.line(px + 0.12, py + ph - 0.18 - k * 0.15, px + pw - 0.12, py + ph - 0.18 - k * 0.15, color=GREY, lw=1.6, z=3)
        elif i == 1:
            for r in range(6):
                for c in range(4):
                    shade = '#BDBDBD' if (r + c) % 2 == 0 else '#E4E4E4'
                    s.rect(px + 0.06 + c * 0.17, py + 0.06 + r * 0.155, 0.17, 0.155, fill=shade, edge=shade, lw=0, z=3)
        elif i == 2:
            for k in range(6):
                ln = pw - 0.24 - (0.2 if k in (2, 5) else 0)
                s.line(px + 0.12, py + ph - 0.18 - k * 0.15, px + 0.12 + ln, py + ph - 0.18 - k * 0.15, color=INK, lw=2.4, z=3)
        elif i == 3:
            for k in range(3):
                yy = py + ph - 0.3 - k * 0.36
                s.rect(cx - 0.45, yy, 0.62, 0.3, fill=PAPER, edge=INK, lw=1.6)
                s.rect(cx + 0.2, yy + 0.04, 0.25, 0.22, fill=GOLD, edge=INK, lw=1.2, z=3)
        else:
            s.icon('magnifier', cx, py + ph / 2, 1.0)
        s.text(cx, top - 1.9, st['head'], size=size + 2, weight='bold')
        sl = K.wrap(st['sub'], size, 'regular', cw - 0.16)
        s.text(cx, top - 2.6, '\n'.join(sl), size=size, color=BODY)
        bw = cw - 0.2
        s.box(x + 0.1, top - 4.05, bw, 0.55, '', fill=GOLD if st.get('ok') else PAPER, edge=INK, lw=1.6)
        s.text(cx, top - 3.775, st['use'], size=size, weight='bold')
        if i < n - 1:
            s.arrow(x + cw - 0.07, top - 0.95, x + cw + 0.07, top - 0.95, lw=2.2, head=13)
    s.text(0.1, top - 3.3, 'Can a model use it?', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ the course
@fig('x_t14_course')
def x_t14_course(w, h, rows=(), size=15, **_):
    """rows: [{band, items: [{n, label}], hl}]"""
    s = Scene(w, h)
    nr = len(rows)
    gap = 0.1
    rh = (h - 0.04 - gap * (nr - 1)) / nr
    lw = 2.5
    for r, row in enumerate(rows):
        y = h - 0.02 - (r + 1) * rh - r * gap
        hl = bool(row.get('hl'))
        s.box(0.02, y, w - 0.04, rh, '', fill=GOLD if hl else PAPER, edge=INK, lw=1.8)
        _fit_text(s, 0.02, y, lw, rh, row['band'], size + 1, weight='bold', ha='left', pad=0.15)
        items = row['items']
        k = len(items)
        sw = (w - 0.04 - lw - 0.1) / max(k, 6)
        for j, it in enumerate(items):
            cx = lw + 0.1 + sw * (j + 0.5)
            s.circle(cx, y + rh - 0.38, 0.27, fill=INK, edge=INK, lw=1.0, z=3)
            s.text(cx, y + rh - 0.38, str(it['n']), size=16, weight='bold', color=PAPER, z=6)
            ls = K.wrap(it['label'], size, 'regular', sw - 0.1)
            if len(ls) > 2:
                raise LayoutError('course label too long: ' + it['label'])
            s.text(cx, y + 0.33, '\n'.join(ls), size=size, color=INK)
            if j < k - 1:
                s.arrow(cx + 0.31, y + rh - 0.38, cx + sw - 0.31, y + rh - 0.38, lw=1.8, head=11)
    return s


# ------------------------------------------------------------------ shelf of everything held
@fig('x_t14_shelf')
def x_t14_shelf(w, h, rows=(), size=15, **_):
    """rows: [{band, tiles: [names]}] tiles are file names; the last row is the follow-up kit (gold)."""
    s = Scene(w, h)
    nr = len(rows)
    gap = 0.07
    rh = (h - 0.04 - gap * (nr - 1)) / nr
    lw = 2.6
    tw = (w - 0.04 - lw - 0.1) / 3.0
    for r, row in enumerate(rows):
        y = h - 0.02 - (r + 1) * rh - r * gap
        s.text(0.1, y + rh / 2, row['band'], size=size + 1, weight='bold', ha='left')
        for j, name in enumerate(row['tiles']):
            x = lw + 0.1 + j * tw
            s.box(x + 0.03, y + 0.04, tw - 0.1, rh - 0.08, '', fill=GOLD if row.get('hl') else PAPER, edge=INK, lw=1.5, r=0.05)
            _fit_text(s, x + 0.03, y + 0.04, tw - 0.1, rh - 0.08, name, size)
    return s


# ------------------------------------------------------------------ check-ins
@fig('x_t14_checkins')
def x_t14_checkins(w, h, start=None, stops=(), size=17, **_):
    """start: {day, date, text}; stops: [{day, date, bring, test}] in order."""
    s = Scene(w, h)
    xs = [1.0, 4.0, 7.1, 10.2]
    ly = h - 1.2
    s.line(0.3, ly, w - 0.3, ly, color=INK, lw=3)
    allp = [start] + list(stops)
    for x, p in zip(xs, allp):
        s.circle(x, ly, 0.13, fill=GOLD if p is not start else INK, edge=INK, lw=2, z=4)
        s.text(x, h - 0.28, p['day'], size=size + 2, weight='bold')
        s.text(x, h - 0.72, p['date'], size=size, color=BODY)
    s.box(0.02, 0.03, 1.95, ly - 0.35, '', fill=PAPER, edge=INK, lw=1.6)
    _fit_text(s, 0.02, 0.03, 1.95, ly - 0.35, start['text'], size)
    for x, p in zip(xs[1:], stops):
        bx, bw = x - 1.5, 3.0
        bh = ly - 0.35
        s.box(bx, 0.03, bw, bh, '', fill=PAPER, edge=INK, lw=1.8)
        s.line(x, ly - 0.14, x, ly - 0.35, color=INK, lw=1.6)
        parts = [('You bring', 'bold', RED), (p['bring'], 'regular', BODY), ('The test', 'bold', RED), (p['test'], 'regular', BODY)]
        lines = []
        for t, kind, colr in parts:
            for ln in K.wrap(t, size, kind, bw - 0.3):
                lines.append((ln, kind, colr))
        lh = size * 1.2 / 72.0
        if len(lines) * lh > bh - 0.1:
            raise LayoutError('check-in box too full: ' + p['day'])
        yy = 0.03 + bh - 0.1 - lh / 2
        for ln, kind, colr in lines:
            s.text(bx + 0.15, yy, ln, size=size, weight='bold' if kind == 'bold' else 'normal', color=colr, ha='left')
            yy -= lh
    return s
