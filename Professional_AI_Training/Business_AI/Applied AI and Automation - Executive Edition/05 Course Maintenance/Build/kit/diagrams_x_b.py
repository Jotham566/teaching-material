"""Figure kinds written by author b (Sessions 4 and 12).

readiness: the readiness scorecard. rows: [{'area': 'Rights', 'rating': 'Red' | 'Amber' | 'Green', 'why': 'short reason'}];
           total: text for the foot line, for example '6 of 12' (Green 2, Amber 1, Red 0); size: font size.
roadmap:   a 90-day data roadmap. items: [{'label': ..., 'owner': ..., 'start': day, 'end': day, 'hl': bool, 'after': [index of item it waits for]}];
           marks: [{'day': 30, 'label': '3 Mar'}, ...]; size: font size.
"""
from figkit import Scene, INK, BODY, MUTE, HAIR, PAPER, RED, GOLD, fig
import slidekit as K


@fig('x_readiness')
def x_readiness(w, h, rows=(), total='', size=17, **_):
    s = Scene(w, h)
    n = len(rows)
    foot = 0.55 if total else 0.0
    head = 0.45
    rh = (h - 0.05 - head - foot) / max(n, 1)
    big = w > 8
    cw = 1.35 if big else 0.95
    c0, c1 = 0.0, (2.75 if big else 1.5)
    c2 = c1 + cw + 0.25
    top = h - 0.02
    for x, t in ((c0, 'Area'), (c1, 'Rating'), (c2, 'Why')):
        s.text(x + 0.08, top - head / 2, t, size=size - 1, weight='bold', ha='left')
    s.line(0, top - head, w, top - head, color=INK, lw=2.2)
    for i, r in enumerate(rows):
        y1 = top - head - rh * i
        yc = y1 - rh / 2
        s.text(c0 + 0.08, yc, '\n'.join(K.wrap(r['area'], size, 'bold', c1 - 0.15)), size=size, weight='bold', ha='left')
        rating = r['rating']
        ch = min(rh - 0.14, 0.46)
        if rating == 'Red':
            s.rect(c1 + 0.08, yc - ch / 2, cw, ch, fill=RED, edge=RED, lw=0, z=2)
            s.text(c1 + 0.08 + cw / 2, yc, 'RED', size=size - 1, weight='bold', color=PAPER, z=6)
        elif rating == 'Amber':
            s.rect(c1 + 0.08, yc - ch / 2, cw, ch, fill=GOLD, edge=GOLD, lw=0, z=2)
            s.text(c1 + 0.08 + cw / 2, yc, 'AMBER', size=size - 1, weight='bold', z=6)
        else:
            s.rect(c1 + 0.08, yc - ch / 2, cw, ch, fill=PAPER, edge=INK, lw=1.6, z=2)
            s.text(c1 + 0.08 + cw / 2, yc, 'GREEN', size=size - 1, weight='bold', z=6)
        lines = K.wrap(r['why'], size - 1, 'regular', w - c2 - 0.2)
        s.text(c2 + 0.08, yc, '\n'.join(lines), size=size - 1, ha='left', color=BODY)
        s.line(0, y1 - rh, w, y1 - rh, color=HAIR, lw=0.8)
    if total:
        s.text(c0 + 0.08, foot / 2 + 0.02, 'Total: ' + total + '  (Green 2, Amber 1, Red 0)', size=size, weight='bold', ha='left')
    return s


@fig('x_roadmap')
def x_roadmap(w, h, items=(), marks=(), size=16, **_):
    s = Scene(w, h)
    n = len(items)
    label_w = min(5.0, w * 0.44)
    gx0, gx1 = label_w + 0.2, w - 0.35
    head = 0.62
    rh = (h - 0.05 - head) / max(n, 1)
    top = h - 0.02

    def X(d):
        return gx0 + (gx1 - gx0) * d / 90.0

    # day marks
    for m in marks:
        x = X(m['day'])
        s.line(x, 0.02, x, top - 0.3, color=HAIR, lw=1.4, dash=True, z=1)
        s.text(x, top - 0.08, 'Day ' + str(m['day']), size=size - 2, weight='bold', color=INK)
        s.text(x, top - 0.36, m.get('label', ''), size=size - 2, color=MUTE)
    s.text(X(0), top - 0.08, 'Day 0', size=size - 2, weight='bold', color=INK)
    s.text(X(0), top - 0.36, '1 Feb', size=size - 2, color=MUTE)
    s.line(0, top - head, w, top - head, color=INK, lw=2.0)
    ys = []
    for i, it in enumerate(items):
        y1 = top - head - rh * i
        yc = y1 - rh / 2
        ys.append(yc)
        lab = K.wrap(it['label'], size, 'bold', label_w - 0.2)
        s.text(0.08, yc + 0.12, '\n'.join(lab), size=size, weight='bold', ha='left')
        s.text(0.08, yc - 0.15, it.get('owner', ''), size=size - 2, color=MUTE, ha='left')
        bh = min(rh * 0.42, 0.34)
        a, b = it['start'], it['end']
        fill = GOLD if it.get('hl') else INK
        s.rect(X(a), yc - bh / 2, X(b) - X(a), bh, fill=fill, edge=INK, lw=1.2, z=3)
        s.line(0, y1 - rh, w, y1 - rh, color=HAIR, lw=0.8)
    for i, it in enumerate(items):
        for j in it.get('after', []) or []:
            x1, y1 = X(items[j]['end']), ys[j] - 0.19
            x2, y2 = X(it['start']), ys[i] + 0.19
            s.arrow(x1, y1, x2, y2, color=RED, lw=1.8, head=11, z=5, rad=0.0)
    return s
