"""Figure kinds for Class 3 (Week 10): can I trust this model? Auto-imported by diagrams.py.

  depthcurve  curve [(depth, train, valid)], best, unit        two error lines against tree depth, a marked chosen depth, zone labels
  student     cards [{head, text, icon, practice, new, hl}]   three students (read nothing, understood, memorised) with invented marks
  folds       labels, subs, scores, summary, held              K-fold or group-fold rounds: gold block = the validation fold (held-out fold), black blocks = the training folds
  leak        (no data)                                        a red arrow carries held-out-row information into the model
"""
from matplotlib.patches import Rectangle

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, fig
import slidekit as K
from diagrams import _wrap


def _nice_ticks(top, n=4):
    """Round tick values from 0 up to just above top."""
    raw = top / n
    for step in (0.1, 0.2, 0.25, 0.5, 1, 2, 2.5, 5, 10, 20, 50):
        if raw <= step:
            break
    k = int(top / step) + 1
    return [round(i * step, 4) for i in range(k + 1)], step


@fig('x_depthcurve')
def x_depthcurve(w, h, curve=(), best=None, unit='', size=16, **_):
    s = Scene(w, h)
    depths = [c[0] for c in curve]
    top = max(max(c[1], c[2]) for c in curve)
    ticks, step = _nice_ticks(top)
    ymax = ticks[-1]
    x0, x1, y0, y1 = 1.2, w - 2.3, 1.55, h - 0.6
    px = lambda d: x0 + 0.25 + (d - depths[0]) / (depths[-1] - depths[0]) * (x1 - x0 - 0.5)
    py = lambda v: y0 + v / ymax * (y1 - y0)
    if best is not None:
        bw = (px(depths[1]) - px(depths[0])) * 0.9
        s.ax.add_patch(Rectangle((px(best) - bw / 2, y0), bw, y1 - y0, fc=GOLD, ec='none', alpha=0.45, zorder=1))
        s.text(px(best), y1 + 0.28, f'Chosen: depth {best}', size=size, weight='bold', color=INK)
    for t in ticks:
        s.line(x0, py(t), x1, py(t), color=HAIR, lw=0.9, z=0)
        s.text(x0 - 0.12, py(t), f'{t:g}', size=14, color=GREY, ha='right')
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    for d in depths:
        s.text(px(d), y0 - 0.22, str(d), size=14, color=GREY)
    s.text((x0 + x1) / 2, 0.22, 'max_depth: most questions a row can be asked', size=size, color=MUTE)
    s.text(0.28, (y0 + y1) / 2, f'error, MAE ({unit})', size=size, color=MUTE, rot=90)
    xs = [px(d) for d in depths]
    s.ax.plot(xs, [py(c[1]) for c in curve], color=INK, lw=3.4, zorder=4)
    s.ax.plot(xs, [py(c[2]) for c in curve], color=RED, lw=3.4, zorder=4)
    for c, x in zip(curve, xs):
        s.circle(x, py(c[1]), 0.065, fill=INK, edge=INK, lw=1, z=5)
        s.circle(x, py(c[2]), 0.065, fill=RED, edge=RED, lw=1, z=5)
    last = curve[-1]
    s.text(xs[-1] + 0.2, py(last[1]) + 0.26, 'Training', size=size, weight='bold', color=INK, ha='left')
    s.text(xs[-1] + 0.2, py(last[2]) + 0.02, 'Validation', size=size, weight='bold', color=RED, ha='left')
    ya, yb = py(last[1]) + 0.3, py(last[2]) - 0.2
    if yb - ya > 0.6:
        s.arrow(xs[-1] + 0.1, (ya + yb) / 2 + 0.01, xs[-1] + 0.1, ya, color=MUTE, lw=1.8, head=12)
        s.arrow(xs[-1] + 0.1, (ya + yb) / 2 - 0.01, xs[-1] + 0.1, yb, color=MUTE, lw=1.8, head=12)
        s.text(xs[-1] + 0.25, (ya + yb) / 2, 'Generalisation gap', size=size, color=MUTE, ha='left', weight='bold')
    # zone labels under the axis
    yz = y0 - 0.5
    lo_u, hi_u = depths[0], depths[1]
    lo_o, hi_o = depths[-2], depths[-1]
    for (a, b, label, col) in ((lo_u, hi_u, 'Underfitting', MUTE), (lo_o, hi_o, 'Overfitting', RED)):
        s.line(px(a) - 0.15, yz, px(b) + 0.15, yz, color=col, lw=3.2)
        s.text((px(a) + px(b)) / 2, yz - 0.25, label, size=size, weight='bold', color=col)
    if best is not None:
        s.line(px(best) - 0.2, yz, px(best) + 0.2, yz, color=INK, lw=3.2)
        s.text(px(best), yz - 0.25, 'Good fit', size=size, weight='bold', color=INK)
    return s


@fig('x_student')
def x_student(w, h, cards=(), size=17, lab_a='Practice paper (seen)', lab_b='New paper (unseen)', **_):
    s = Scene(w, h)
    n = len(cards)
    gap = 0.22
    cw = (w - 0.1 - gap * (n - 1)) / n
    for i, c in enumerate(cards):
        x = 0.05 + i * (cw + gap)
        s.box(x, 0.05, cw, h - 0.1, '', fill=GOLD if c.get('hl') else PAPER, edge=INK, lw=2.0, r=0.07)
        cx = x + cw / 2
        s.icon(c.get('icon', 'person'), cx, h - 0.75, 0.95)
        s.text(cx, h - 1.55, c['head'], size=20, weight='bold')
        _wrap(s, cx, h - 2.45, cw - 0.3, c['text'], size, color=INK if c.get('hl') else BODY)
        for j, (lab, val) in enumerate(((lab_a, c['practice']), (lab_b, c['new']))):
            yy = 1.55 - j * 0.85
            s.text(cx, yy + 0.2, lab, size=15, color=INK if c.get('hl') else MUTE)
            s.text(cx, yy - 0.12, val, size=26, weight='bold', color=RED if (j == 1 and c.get('hl')) else INK)
    return s


@fig('x_folds')
def x_folds(w, h, labels=(), subs=(), scores=(), summary='', unit='MAE', size=16, row_word='Fold', held='Validation fold', **_):
    s = Scene(w, h)
    n = len(labels)
    lab_w = 1.3
    score_w = 1.4 if scores else 0.0
    gap = 0.06
    bw = (w - 0.1 - lab_w - score_w - gap * (n - 1)) / n
    top = h - 0.6
    # legend
    s.box(lab_w + 0.05, h - 0.5, 0.45, 0.32, '', fill=INK, edge=INK, r=0.04)
    s.text(lab_w + 0.6, h - 0.34, 'Training folds', size=size, ha='left')
    s.box(lab_w + 2.2, h - 0.5, 0.45, 0.32, '', fill=GOLD, edge=INK, r=0.04)
    s.text(lab_w + 2.75, h - 0.34, held, size=size, ha='left')
    if scores:
        s.text(w - 0.05 - score_w / 2, h - 0.34, unit, size=size, weight='bold', color=MUTE)
    foot = 0.75 if summary else 0.1
    rh = (top - 0.1 - foot) / n
    for r in range(n):
        yy = top - (r + 1) * rh + 0.04
        s.text(0.05, yy + (rh - 0.08) / 2, f'{row_word} {r + 1}', size=size, weight='bold', ha='left')
        for c in range(n):
            x = 0.05 + lab_w + c * (bw + gap)
            held = c == r
            s.box(x, yy, bw, rh - 0.1, '', fill=GOLD if held else INK, edge=INK, lw=1.6, r=0.04)
            col = INK if held else PAPER
            txt = f'{labels[c]}\n{subs[c]}' if subs else labels[c]
            s.text(x + bw / 2, yy + (rh - 0.1) / 2, txt, size=size - 1 if subs else size, color=col, weight='bold' if not subs else 'normal')
        if scores:
            s.text(w - 0.05 - score_w / 2, yy + (rh - 0.1) / 2, scores[r], size=size + 2, weight='bold', color=RED)
    if summary:
        s.text(w / 2, 0.38, summary, size=size + 2, weight='bold', color=RED)
    return s


@fig('x_leak')
def x_leak(w, h, exam='Held-out rows', size=18, **_):
    s = Scene(w, h)
    bw = 3.6
    bx = (w - bw) / 2
    s.box(bx, h - 1.15, bw, 0.95, '', fill=GOLD, edge=INK, lw=2.0, r=0.07)
    s.icon('lock', bx + 0.55, h - 0.67, 0.65)
    s.text(bx + 1.0 + (bw - 1.0) / 2, h - 0.67, exam, size=size + 1, weight='bold')
    ry, rh = 1.25, 1.05
    s.box(0.1, ry, 2.2, rh, 'Training rows', size=size, fill=INK, edge=INK, color=PAPER, weight='bold')
    s.arrow(2.3, ry + rh / 2, 2.95, ry + rh / 2, lw=2.4, head=18)
    mx = 2.95
    s.box(mx, ry, 1.8, rh, 'Model', size=size + 2, fill=PAPER, edge=INK, lw=2.2, weight='bold')
    s.arrow(mx + 1.8, ry + rh / 2, mx + 2.45, ry + rh / 2, lw=2.4, head=18)
    s.box(mx + 2.45, ry, 2.2, rh, 'Score', size=size + 2, fill=PAPER, edge=INK, lw=2.0, weight='bold')
    s.arrow(w / 2 - 0.05, h - 1.2, mx + 0.9, ry + rh + 0.05, color=RED, lw=3.4, head=22, dash=True)
    s.text(w / 2 + 0.55, 3.15, 'Data leakage', size=size, weight='bold', color=RED, ha='left')
    s.text(0.1, 0.95, 'Normal path: training rows train the model, then it gets a score', size=15, color=MUTE, ha='left')
    s.text(w / 2, 0.45, 'Held-out rows must never reach the model', size=size - 1, color=RED, weight='bold')
    return s
