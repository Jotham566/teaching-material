"""Figure kinds for Session 14 (Data readiness assessment, roadmap and 90-day plan). Auto-imported by diagrams.py.

t14_fivekinds : the five kinds of data, an NVF example of each and the first action that makes it ready.
t14_docjourney: one document from paper to an index a model can search, and whether a model can use it at each stage.
t14_course    : the 14 sessions as one chain: the Session 0 question, three rows joined end to start, and an arrow from 14 back to the question.
t14_shelf     : everything the learner now holds, as tiles grouped by purpose.
t14_invhome   : a tiny data inventory of the data on your own phone: source, owner, where, who may see, sensitivity (11 Nov 2026).
t14_tiny      : a five-row contact list with one blank phone and one duplicate person, for completeness and uniqueness by hand (11 Nov 2026).
t14_kpichange : KPI change built by hand: 6 to 9 is +3, 3 / 6 = +50%; 8 faults to 0 is -8, -8 / 8 = -100% (11 Nov 2026).
t14_checkins  : the day 0, 30, 60 and 90 timeline with what you bring and the test at each check-in.
t14_readiness : the readiness scorecard with a Points column, and the total added in the order of the rows (11 Nov 2026 coherence pass;
                replaces the shared x_readiness on Session 14 slides so the sum reads top to bottom).
t14_roadmap   : the 90-day roadmap; day lines stop below the date labels, dependency arrows enter the top of the bar that waits
                and pass behind any bar they must cross (11 Nov 2026 coherence pass; replaces the shared x_roadmap on Session 14).
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
def x_t14_course(w, h, rows=(), start=None, back='', size=14, **_):
    """rows: [{band, items: [{n, label}], hl}]; start: {band, n, label} the Session 0 question drawn above the rows.
    One chain: 0 leads into 1, the last station of each row leads into the first of the next, and the last station returns to the question."""
    s = Scene(w, h)
    nr = len(rows)
    ch = 0.75                      # right channel for the connectors
    rw = w - 0.04 - ch             # width of the row boxes
    top_h, top_gap = (0.5, 0.2) if start else (0.0, 0.0)
    gap = 0.2
    rh = (h - 0.04 - top_h - top_gap - gap * (nr - 1)) / nr
    lw = 2.5
    R = 0.22
    sw = (rw - lw - 0.1) / max(max(len(r['items']) for r in rows), 6)
    first_cx = lw + 0.1 + sw * 0.5
    ty = h - 0.02 - top_h
    if start:
        s.box(0.02, ty, rw, top_h, '', fill=PAPER, edge=INK, lw=2.2)
        s.text(0.17, ty + top_h / 2, start['band'], size=size + 1, weight='bold', ha='left')
        s.circle(first_cx, ty + top_h / 2, R, fill=INK, edge=INK, lw=1.0, z=3)
        s.text(first_cx, ty + top_h / 2, str(start['n']), size=15, weight='bold', color=PAPER, z=6)
        s.text(first_cx + R + 0.2, ty + top_h / 2, start['label'], size=size + 2, weight='bold', ha='left')
    ends = []
    for r, row in enumerate(rows):
        y = h - 0.02 - top_h - top_gap - (r + 1) * rh - r * gap
        hl = bool(row.get('hl'))
        s.box(0.02, y, rw, rh, '', fill=GOLD if hl else PAPER, edge=INK, lw=1.8)
        _fit_text(s, 0.02, y, lw, rh, row['band'], size + 1, weight='bold', ha='left', pad=0.15)
        items = row['items']
        k = len(items)
        cy = y + rh - 0.29
        for j, it in enumerate(items):
            cx = lw + 0.1 + sw * (j + 0.5)
            s.circle(cx, cy, R, fill=INK, edge=INK, lw=1.0, z=3)
            s.text(cx, cy, str(it['n']), size=15, weight='bold', color=PAPER, z=6)
            ls = K.wrap(it['label'], size, 'regular', sw - 0.1)
            if len(ls) > 2:
                raise LayoutError('course label too long: ' + it['label'])
            s.text(cx, y + 0.27, '\n'.join(ls), size=size, color=INK)
            if j < k - 1:
                s.arrow(cx + R + 0.04, cy, cx + sw - R - 0.04, cy, lw=1.8, head=11)
        ends.append((y, cy, lw + 0.1 + sw * (k - 0.5)))
    if start:   # 0 leads into 1
        s.arrow(first_cx, ty + top_h / 2 - R - 0.02, first_cx, ends[0][1] + R + 0.03, lw=1.8, head=11)
    xa = rw + 0.02 + 0.28
    for r in range(nr - 1):   # last station of a row leads into the first of the next row
        y, cy, lx = ends[r]
        ny, ncy, _ = ends[r + 1]
        ym = y - gap / 2
        xd = first_cx - 0.6
        for (x1, y1, x2, y2) in [(lx + R + 0.02, cy, xa, cy), (xa, cy, xa, ym), (xa, ym, xd, ym), (xd, ym, xd, ncy)]:
            s.line(x1, y1, x2, y2, color=INK, lw=1.8, z=4)
        s.arrow(xd, ncy, first_cx - R - 0.04, ncy, lw=1.8, head=11)
    if start:   # the last station returns to the question
        y, cy, lx = ends[-1]
        xb = w - 0.2
        for (x1, y1, x2, y2) in [(lx + R + 0.02, cy, xb, cy), (xb, cy, xb, ty + top_h / 2)]:
            s.line(x1, y1, x2, y2, color=INK, lw=2.4, z=4)
        s.arrow(xb, ty + top_h / 2, rw + 0.05, ty + top_h / 2, lw=2.4, head=13)
        if back:
            s.text((lx + R + xb) / 2, cy - 0.3, back, size=size, weight='bold', color=INK)
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


# ------------------------------------------------------------------ inventory at home
@fig('x_t14_invhome')
def x_t14_invhome(w, h, size=15, **_):
    s = Scene(w, h)
    rows = [['Source', 'Owner', 'Where it lives', 'Sensitivity'],
            ['Contacts', 'You', 'Phone and cloud', 'Personal'],
            ['Mobile money SMS', 'You', 'Phone inbox', 'Confidential'],
            ['Family photos', 'You', 'Phone gallery', 'Personal'],
            ['School timetable', 'The school', 'A shared PDF', 'Public']]
    cw = [(w - 0.1) * f for f in (0.30, 0.18, 0.27, 0.25)]
    s.table(0.05, h - 0.05, cw, (h - 0.15) / len(rows), rows, size=size, align=['left'] * 4, hl_cols=(0,))
    return s


# ------------------------------------------------------------------ tiny contact list
@fig('x_t14_tiny')
def x_t14_tiny(w, h, mode='complete', size=15, **_):
    """mode 'complete': the blank phone cell is marked; mode 'unique': the repeated row is marked."""
    s = Scene(w, h)
    rows = [['Row', 'Name', 'Phone'],
            ['1', 'Amina', '0700 000 001'],
            ['2', 'Brian', '0700 000 002'],
            ['3', 'Carol', ''],
            ['4', 'David', '0700 000 004'],
            ['5', 'Brian', '0700 000 002']]
    tw = 4.3
    cw = [0.7, 1.6, tw - 2.3]
    rh = (h - 0.15) / len(rows)
    hl = {(3, 2): RED} if mode == 'complete' else {(5, 1): GOLD, (5, 2): GOLD, (2, 1): GOLD, (2, 2): GOLD}
    s.table(0.05, h - 0.05, cw, rh, rows, size=size, align=['center', 'left', 'left'], hl_cells=hl)
    x = tw + 0.35
    if mode == 'complete':
        lines = [('Phone cells: 5', INK), ('Filled: 4 (row 3 is blank)', INK), ('4 ÷ 5 = 0.8', INK), ('0.8 × 100% = 80%', RED)]
        head = 'Completeness'
    else:
        lines = [('Rows: 5', INK), ('Different people: 4', INK), ('(Brian appears twice)', BODY), ('4 ÷ 5 = 0.8 = 80%', RED), ('Duplicates: 1 − 0.8 = 20%', BODY)]
        head = 'Uniqueness'
    s.text(x, h - 0.35, head, size=size + 2, weight='bold', ha='left')
    y = h - 0.95
    for t, c in lines:
        s.text(x, y, t, size=size + 1, weight='bold' if c == RED else 'normal', color=c, ha='left')
        y -= 0.55
    return s


# ------------------------------------------------------------------ KPI change
@fig('x_t14_kpichange')
def x_t14_kpichange(w, h, size=15, **_):
    s = Scene(w, h)
    half = w / 2
    y0 = 0.55
    def pair(x0, old, new, top, unit_lab, lines):
        s.text(x0 + 0.2, h - 0.25, unit_lab, size=size + 1, weight='bold', ha='left')
        yy = h - 0.7
        for t, c in lines:
            s.text(x0 + 0.2, yy, t, size=size, color=c, weight='bold', ha='left')
            yy -= 0.42
        unit = (h - 2.35) / top
        bw = 1.0
        for k, (v, lab, fill) in enumerate([(old, 'Today', PAPER), (new, 'Day 90', GOLD)]):
            x = x0 + 0.4 + k * 1.5
            s.rect(x, y0, bw, max(v * unit, 0.02), fill=fill, edge=INK, lw=2)
            s.text(x + bw / 2, y0 + v * unit + 0.22, str(v), size=size + 1, weight='bold')
            s.text(x + bw / 2, y0 - 0.28, lab, size=size, weight='bold')
        s.line(x0 + 0.2, y0, x0 + 3.2, y0, lw=2)
    pair(0.05, 6, 9, 9, 'Readiness score (of 12)', [('Change: 9 − 6 = +3', INK), ('3 ÷ 6 = 0.5 = +50%', RED)])
    pair(half + 0.05, 8, 0, 9, 'Invoice faults', [('Change: 0 − 8 = −8', INK), ('−8 ÷ 8 = −1 = −100%', RED)])
    s.line(half, 0.2, half, h - 0.1, color=HAIR, lw=1)
    return s


# ------------------------------------------------------------------ readiness scorecard with points
_PTS = {'Green': 2, 'Amber': 1, 'Red': 0}


@fig('x_t14_readiness')
def x_t14_readiness(w, h, rows=(), total=False, size=16, **_):
    s = Scene(w, h)
    n = len(rows)
    foot = 0.55 if total else 0.0
    head = 0.45
    rh = (h - 0.05 - head - foot) / max(n, 1)
    big = w > 8
    cw = 1.35 if big else 1.05
    c1 = 2.75 if big else 1.45
    cp = c1 + cw + 0.2
    pw = 0.95 if big else 0.75
    c2 = cp + pw + 0.1
    top = h - 0.02
    for x, t, ha in ((0.0 + 0.08, 'Area', 'left'), (c1 + 0.08, 'Rating', 'left'), (cp + pw / 2, 'Points', 'center'), (c2 + 0.08, 'Why', 'left')):
        s.text(x, top - head / 2, t, size=size - 1, weight='bold', ha=ha)
    s.line(0, top - head, w, top - head, color=INK, lw=2.2)
    pts = []
    for i, r in enumerate(rows):
        y1 = top - head - rh * i
        yc = y1 - rh / 2
        s.text(0.08, yc, '\n'.join(K.wrap(r['area'], size, 'bold', c1 - 0.15)), size=size, weight='bold', ha='left')
        rating = r['rating']
        ch = min(rh - 0.14, 0.46)
        fill, edge, col = {'Red': (RED, RED, PAPER), 'Amber': (GOLD, GOLD, INK)}.get(rating, (PAPER, INK, INK))
        s.rect(c1 + 0.08, yc - ch / 2, cw, ch, fill=fill, edge=edge, lw=1.6 if rating == 'Green' else 0, z=2)
        s.text(c1 + 0.08 + cw / 2, yc, rating.upper(), size=size - 1, weight='bold', color=col, z=6)
        p = _PTS[rating]
        pts.append(p)
        s.text(cp + pw / 2, yc, str(p), size=size + 1, weight='bold', color=RED if p == 0 else INK)
        lines = K.wrap(r['why'], size - 1, 'regular', w - c2 - 0.2)
        s.text(c2 + 0.08, yc, '\n'.join(lines), size=size - 1, ha='left', color=BODY)
        s.line(0, y1 - rh, w, y1 - rh, color=HAIR, lw=0.8)
    if total:
        txt = 'Total: ' + ' + '.join(str(p) for p in pts) + f' = {sum(pts)} of {2 * n}   (Green 2, Amber 1, Red 0)'
        s.text(0.08, foot / 2 + 0.02, txt, size=size, weight='bold', ha='left')
    return s


# ------------------------------------------------------------------ roadmap
def _behind_line(s, xs, ys, color=RED, lw=1.8):
    # drawn under the bars (z 2 < 3), so a line that must cross another action's bar passes behind it
    s.ax.plot(xs, ys, color=color, lw=lw, zorder=2, solid_capstyle='butt')


@fig('x_t14_roadmap')
def x_t14_roadmap(w, h, items=(), marks=(), start_label='1 Feb', size=16, **_):
    s = Scene(w, h)
    n = len(items)
    label_w = min(5.0, w * 0.44)
    gx0, gx1 = label_w + 0.2, w - 0.45
    head = 0.72
    rh = (h - 0.05 - head) / max(n, 1)
    top = h - 0.02
    rule = top - head

    def X(d):
        return gx0 + (gx1 - gx0) * d / 90.0

    for d, lab in [(0, start_label)] + [(m['day'], m.get('label', '')) for m in marks]:
        x = X(d)
        s.text(x, top - 0.12, 'Day ' + str(d), size=size - 2, weight='bold', color=INK)
        s.text(x, top - 0.44, lab, size=size - 2, color=MUTE)
        if d:
            s.line(x, 0.02, x, rule - 0.04, color=HAIR, lw=1.4, dash=True, z=1)
    s.line(0, rule, w, rule, color=INK, lw=2.0)
    ys, bh = [], min(rh * 0.42, 0.34)
    for i, it in enumerate(items):
        y1 = rule - rh * i
        yc = y1 - rh / 2
        ys.append(yc)
        s.text(0.08, yc + 0.12, '\n'.join(K.wrap(it['label'], size, 'bold', label_w - 0.2)), size=size, weight='bold', ha='left')
        s.text(0.08, yc - 0.15, it.get('owner', ''), size=size - 2, color=MUTE, ha='left')
        a, b = it['start'], it['end']
        s.rect(X(a), yc - bh / 2, X(b) - X(a), bh, fill=GOLD if it.get('hl') else INK, edge=INK, lw=1.2, z=3)
        if i < n - 1:
            s.line(0, y1 - rh, w, y1 - rh, color=HAIR, lw=0.8)
    # dependency arrows: out of the end of the bar it waits for, along that row, then down into the top of the waiting bar.
    # The dependency from the lowest row gets the left-most drop, so the lines never cross each other.
    for i, it in enumerate(items):
        deps = sorted(it.get('after', []) or [], reverse=True)
        for rank, j in enumerate(deps):
            x1 = X(items[j]['end'])
            xv = max(x1 + 0.15, X(it['start']) + 0.22 * (rank + 1))
            if xv > X(it['end']) - 0.05:
                raise LayoutError(f'roadmap arrow for item {i} falls outside its bar')
            yt = ys[i] + bh / 2
            _behind_line(s, [x1, xv, xv], [ys[j], ys[j], yt + 0.12])
            s.arrow(xv, yt + 0.14, xv, yt, color=RED, lw=1.8, head=11, z=6)
    return s
