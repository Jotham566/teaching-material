"""Figure kinds for Class 4 (features and choosing a model). Registered like the kinds in diagrams_ml.py; imported automatically by diagrams.py.

  ablation  rows [{label, chips[{t, new}], result, hl}], band (one line under the rows)   two or three versions of a model, same rows, one result each
  curves    points, curves [{label, xs, ys, kind}], xlabel, ylabel                         training dots with fitted curves drawn over them
  knn       train [(x, y)], query (x, y), neighbours [(x, y, label)], xlabel, ylabel, result   the k closest rows and their average
  envelope  head, sub, foot                                                                a sealed envelope: the held-out test set
  latency   items [{label, value}], limit, unit, note                                      prediction time of each model against the client's limit
  refit     rows [{label, chips[{t, kind}], band}]                                         choose on E1 to E4 and E5, then refit on E1 to E5 and score E6 once
"""
import math

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, fig
import slidekit as K


# ------------------------------------------------------------------ ablation
@fig('x_ablation')
def x_ablation(w, h, rows=(), band='', size=17, **_):
    s = Scene(w, h)
    n = len(rows)
    band_h = 0.85 if band else 0.0
    gap = 0.18
    rh = (h - 0.1 - band_h - gap * (n - 1) - (0.15 if band else 0)) / n
    res_w = 2.1
    for i, r in enumerate(rows):
        y = h - 0.05 - (i + 1) * rh - i * gap
        s.box(0.05, y, w - 0.1, rh, '', fill=GOLD if r.get('hl') else PAPER, edge=INK, lw=2.0, r=0.07)
        s.text(0.3, y + rh - 0.3, r['label'], size=size + 1, weight='bold', ha='left')
        x = 0.3
        cy = y + 0.42
        for c in r['chips']:
            tw = K.width_in(c['t'], size - 1, 'bold' if c.get('new') else 'regular') + 0.3
            s.box(x, cy - 0.25, tw, 0.5, c['t'], size=size - 1, fill=RED if c.get('new') else PAPER, color=PAPER if c.get('new') else INK,
                  edge=INK, lw=1.6, r=0.05, weight='bold' if c.get('new') else 'normal')
            x += tw + 0.14
        s.line(w - res_w - 0.1, y + 0.15, w - res_w - 0.1, y + rh - 0.15, color=HAIR, lw=1.4)
        s.text(w - res_w / 2 - 0.1, y + rh * 0.58, r['result'], size=26, weight='bold')
        s.text(w - res_w / 2 - 0.1, y + rh * 0.25, r.get('result_sub', ''), size=size - 3 if size > 17 else 14, color=MUTE)
    if band:
        by = 0.05
        s.box(0.05, by, w - 0.1, band_h, band, size=size, fill=INK, color=PAPER, edge=INK, r=0.06, weight='bold')
    return s


# ------------------------------------------------------------------ curves
@fig('x_curves')
def x_curves(w, h, points=(), curves=(), xlabel='', ylabel='', size=16, **_):
    s = Scene(w, h)
    x0, x1, y0, y1 = 1.05, w - 0.35, 0.8, h - 0.3
    xs = [p[0] for p in points]
    ys = [p[1] for p in points] + [v for c in curves for v in c['ys']]
    lo_x, hi_x, lo_y, hi_y = min(xs), max(xs), min(ys), max(ys)
    padx, pady = (hi_x - lo_x) * 0.04, (hi_y - lo_y) * 0.06
    lo_x, hi_x, lo_y, hi_y = lo_x - padx, hi_x + padx, lo_y - pady, hi_y + pady
    px = lambda v: x0 + (v - lo_x) / (hi_x - lo_x) * (x1 - x0)
    py = lambda v: y0 + (v - lo_y) / (hi_y - lo_y) * (y1 - y0)
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    s.text((x0 + x1) / 2, 0.28, xlabel, size=size, color=MUTE)
    s.text(0.3, (y0 + y1) / 2, ylabel, size=size, color=MUTE, rot=90)
    for v in (lo_x + padx, hi_x - padx):
        s.text(px(v), y0 - 0.22, f'{v:.0f}', size=14, color=GREY)
    for v in (lo_y + pady, hi_y - pady):
        s.text(x0 - 0.12, py(v), f'{v:.0f}', size=14, color=GREY, ha='right')
    for (x, y) in points:
        s.circle(px(x), py(y), 0.07, fill=PAPER, edge=INK, lw=1.2, z=3)
    style = {'red': dict(color=RED, lw=3.4, ls='-'), 'ink': dict(color=INK, lw=3.6, ls='-'), 'mute': dict(color=MUTE, lw=2.8, ls='--')}
    ly = y1 - 0.2
    for c in curves:
        st = style[c.get('kind', 'ink')]
        s.ax.plot([px(v) for v in c['xs']], [py(v) for v in c['ys']], color=st['color'], lw=st['lw'], ls=st['ls'], zorder=5)
        s.ax.plot([x0 + 0.25, x0 + 0.85], [ly, ly], color=st['color'], lw=st['lw'], ls=st['ls'], zorder=6)
        s.text(x0 + 1.0, ly, c['label'], size=size, ha='left', weight='bold', color=st['color'] if c.get('kind') != 'mute' else MUTE)
        ly -= 0.36
    return s


# ------------------------------------------------------------------ knn
@fig('x_knn')
def x_knn(w, h, train=(), query=(0, 0), neighbours=(), xlabel='', ylabel='', result=('', ''), size=16, **_):
    s = Scene(w, h)
    foot = 0.95
    x0, x1, y0, y1 = 0.95, w - 0.3, 0.75 + foot, h - 0.25
    rmax = max(math.hypot(a - query[0], b - query[1]) for a, b, _ in neighbours)
    half = rmax * 2.4
    lo_x, hi_x, lo_y, hi_y = query[0] - half, query[0] + half, query[1] - half, query[1] + half
    train = [p for p in train if lo_x <= p[0] <= hi_x and lo_y <= p[1] <= hi_y]
    sc = min((x1 - x0) / (hi_x - lo_x), (y1 - y0) / (hi_y - lo_y))
    ox = x0 + ((x1 - x0) - (hi_x - lo_x) * sc) / 2
    oy = y0 + ((y1 - y0) - (hi_y - lo_y) * sc) / 2
    px = lambda v: ox + (v - lo_x) * sc
    py = lambda v: oy + (v - lo_y) * sc
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    s.text((x0 + x1) / 2, y0 - 0.55, xlabel + '.  Red dot: the new row.', size=size, color=MUTE)
    s.text(0.3, (y0 + y1) / 2, ylabel, size=size, color=MUTE, rot=90)
    # tick values every 0.2 on the scaled axes (value of the scaled input, no unit)
    v = math.ceil(lo_x * 2) / 2
    while v <= hi_x:
        s.text(px(v), y0 - 0.25, f'{v:.1f}', size=14, color=GREY)
        v += 0.5
    v = math.ceil(lo_y * 2) / 2
    while v <= hi_y:
        s.text(x0 - 0.1, py(v), f'{v:.1f}', size=14, color=GREY, ha='right')
        v += 0.5
    r = max(math.hypot(a - query[0], b - query[1]) for a, b, _ in neighbours) * sc
    qx, qy = px(query[0]), py(query[1])
    # label positions: straight out from the red dot, beyond the dashed ring
    labs = []
    for a, b, lab in neighbours:
        dx, dy = px(a) - qx, py(b) - qy
        n_ = math.hypot(dx, dy) or 1.0
        ux, uy = dx / n_, dy / n_
        lx, ly = qx + ux * (r + 0.2), qy + uy * (r + 0.2) + (0.12 if uy >= 0 else -0.12)
        tw = K.width_in(lab, size, 'bold')
        right = ux >= 0
        x_lo = lx if right else lx - tw
        labs.append((lab, lx, ly, right, (x_lo - 0.05, ly - 0.2, x_lo + tw + 0.05, ly + 0.2)))
    nb_xy = {(a, b) for a, b, _ in neighbours}
    for (x, y) in train:
        if (x, y) in nb_xy:
            continue
        cx, cy = px(x), py(y)
        if any(bx0 <= cx <= bx1 and by0 <= cy <= by1 for *_, (bx0, by0, bx1, by1) in labs):
            continue
        s.circle(cx, cy, 0.07, fill=PAPER, edge=GREY, lw=1.2, z=3)
    s.ax.add_patch(__import__('matplotlib.patches', fromlist=['Circle']).Circle((qx, qy), r + 0.08, fc='none', ec=RED, lw=2.2, ls='--', zorder=4))
    for a, b, lab in neighbours:
        s.line(qx, qy, px(a), py(b), color=RED, lw=1.4, z=4)
        s.circle(px(a), py(b), 0.12, fill=GOLD, edge=INK, lw=2, z=6)
    for lab, lx, ly, right, _ in labs:
        s.text(lx, ly, lab, size=size, ha='left' if right else 'right', weight='bold')
    s.circle(px(query[0]), py(query[1]), 0.15, fill=RED, edge=INK, lw=2, z=7)
    s.box(0.05, 0.05, w - 0.1, foot - 0.1, '', fill=PAPER, edge=INK, lw=2.0, r=0.07)
    s.text(w / 2, 0.05 + (foot - 0.1) * 0.7, result[0], size=size + 2, weight='bold')
    s.text(w / 2, 0.05 + (foot - 0.1) * 0.28, result[1], size=size, color=BODY)
    return s


# ------------------------------------------------------------------ envelope
@fig('x_envelope')
def x_envelope(w, h, head='Test set', sub='', foot='', size=18, **_):
    s = Scene(w, h)
    ew, eh = min(w - 1.0, 5.6), min(h - 1.9, 3.1)
    ex, ey = (w - ew) / 2, 1.15
    s.rect(ex, ey, ew, eh, fill=PAPER, edge=INK, lw=3.0, z=2)
    s.poly([(ex, ey + eh), (ex + ew, ey + eh), (ex + ew / 2, ey + eh * 0.42)], fill='#EFE7C8', edge=INK, lw=3.0, z=3)
    s.line(ex, ey, ex + ew * 0.42, ey + eh * 0.5, color=GREY, lw=1.6, z=3)
    s.line(ex + ew, ey, ex + ew * 0.58, ey + eh * 0.5, color=GREY, lw=1.6, z=3)
    s.circle(ex + ew / 2, ey + eh * 0.42, 0.34, fill=RED, edge=INK, lw=2.4, z=5)
    s.icon('lock', ex + ew / 2, ey + eh * 0.42, 0.5, color=PAPER, accent=PAPER)
    s.text(ex + ew / 2, ey + eh * 0.24, head, size=size + 4, weight='bold', z=6)
    if sub:
        s.text(ex + ew / 2, ey + eh * 0.24 - 0.4, sub, size=size - 1, color=BODY, z=6)
    if foot:
        s.text(w / 2, 0.45, foot, size=size, weight='bold', color=RED)
    return s


# ------------------------------------------------------------------ memo: a one-page note with seven labelled parts
@fig('x_memo')
def x_memo(w, h, title='', sections=(), size=16, **_):
    s = Scene(w, h)
    s.rect(0.05, 0.05, w - 0.1, h - 0.1, fill=PAPER, edge=INK, lw=2.0)
    s.rect(0.05, h - 0.65, w - 0.1, 0.6, fill=INK, edge=INK, lw=0, z=3)
    s.text(0.3, h - 0.35, title, size=18, weight='bold', color=PAPER, ha='left', z=6)
    n = len(sections)
    row = (h - 0.8) / n
    lw_ = 2.75
    for i, (lab, val) in enumerate(sections):
        yc = h - 0.65 - (i + 0.5) * row
        s.text(0.3, yc, lab, size=14, weight='bold', color=RED, ha='left')
        lines = K.wrap(val, size, 'regular', w - lw_ - 0.5)
        s.text(lw_, yc, '\n'.join(lines), size=size, color=BODY, ha='left')
        if i < n - 1:
            s.line(0.3, yc - row / 2, w - 0.3, yc - row / 2, color=HAIR, lw=1.0)
    return s


# ------------------------------------------------------------------ latency: prediction time of each model against the client's limit
@fig('x_latency')
def x_latency(w, h, items=(), limit=50, unit=' ms', note='', size=17, **_):
    """items [{label, value}]: horizontal bars of prediction time; a dashed red line at the client's limit; bars over the limit are red."""
    s = Scene(w, h)
    n = len(items)
    top, foot = 0.55, (0.55 if note else 0.15)
    lab_w = 3.3
    bx0 = lab_w + 0.2
    bar_w = w - bx0 - 1.3
    mv = max(max(i['value'] for i in items), limit) * 1.05
    row = (h - top - foot) / n
    lx = bx0 + bar_w * limit / mv
    for i, it in enumerate(items):
        yc = h - top - (i + 0.5) * row
        over = it['value'] > limit
        s.text(lab_w, yc, it['label'], size=size, ha='right')
        bw = max(0.05, bar_w * it['value'] / mv)
        s.rect(bx0, yc - row * 0.27, bw, row * 0.54, fill=RED if over else PAPER, edge=INK, lw=2)
        s.text(bx0 + bw + 0.12, yc, f"{it['value']:g}{unit}", size=size, weight='bold', ha='left', color=RED if over else INK)
    s.line(bx0, foot, bx0, h - top + 0.05, color=INK, lw=2)
    s.line(lx, foot, lx, h - top + 0.1, color=RED, lw=2.6, dash=True, z=5)
    s.text(lx, h - top + 0.3, f'Client limit: {limit:g}{unit}', size=size, weight='bold', color=RED)
    if note:
        s.text(w / 2, 0.25, note, size=size - 2, color=MUTE)
    return s


# ------------------------------------------------------------------ refit: choose on E1 to E4 and E5, then refit on E1 to E5 and score E6 once
@fig('x_refit')
def x_refit(w, h, rows=(), size=17, **_):
    """rows: [{label, chips: [{t, kind}], band}]; kind is 'train', 'valid', 'dev' or 'test'. band: text under the chips of the row."""
    s = Scene(w, h)
    n = len(rows)
    gap = 0.3
    rh = (h - 0.1 - gap * (n - 1)) / n
    style = {'train': (PAPER, INK), 'valid': (GOLD, INK), 'dev': (INK, PAPER), 'test': (RED, PAPER), 'sealed': (PAPER, GREY)}
    for i, r in enumerate(rows):
        y = h - 0.05 - (i + 1) * rh - i * gap
        s.box(0.05, y, w - 0.1, rh, '', fill=PAPER, edge=INK, lw=2.0, r=0.07)
        s.text(0.3, y + rh - 0.32, r['label'], size=size + 1, weight='bold', ha='left')
        chips = r['chips']
        cw = (w - 0.6 - 0.12 * (len(chips) - 1)) / len(chips)
        cy = y + rh * 0.42
        for j, c in enumerate(chips):
            fill, col = style[c.get('kind', 'train')]
            x = 0.3 + j * (cw + 0.12)
            s.box(x, cy - 0.32, cw, 0.64, c['t'], size=size, fill=fill, color=col, edge=GREY if c.get('kind') == 'sealed' else INK, lw=2.0, r=0.06,
                  weight='bold', dash=c.get('kind') == 'sealed')
        if r.get('band'):
            s.text(0.3, y + 0.32, r['band'], size=size - 2, color=BODY, ha='left')
    return s
