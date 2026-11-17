"""Machine-learning diagrams for the IUEA second-half decks, drawn from data. Registered like the kinds in diagrams.py (render with
`diagrams.render({'kind': 'scatter', ...}, w, h)`). New kinds for classes 2 to 4 go in their own diagrams_ml_cN.py and are imported at the bottom of diagrams.py.

  scatter   points, xlabel, ylabel, hline (value), line (intercept, slope), residuals (bool), mark (list of point indexes), hline_label, line_label
  rowsplit  parts [{label, sub, n, role, fill}]            a strip of rows cut into groups (training, validation, test)
  tree      node {q, yes, no} or leaf {v}                   a small decision tree drawn from data
"""
from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, fig
import slidekit as K


@fig('x_scatter')
def x_scatter(w, h, points=(), xlabel='', ylabel='', hline=None, line=None, residuals=False, mark=(), hline_label='', line_label='', size=16,
              xlim=None, ylim=None, dot=0.075, **_):
    s = Scene(w, h)
    x0, x1, y0, y1 = 1.05, w - 0.35, 0.8, h - 0.3
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    lo_x, hi_x = xlim or (min(xs), max(xs))
    lo_y, hi_y = ylim or (min(ys), max(ys))
    padx, pady = (hi_x - lo_x) * 0.05, (hi_y - lo_y) * 0.08
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
    if line:
        b, m = line
        if residuals:
            for (x, y) in points:
                s.line(px(x), py(y), px(x), py(b + m * x), color=RED, lw=1.6, z=2)
    for i, (x, y) in enumerate(points):
        s.circle(px(x), py(y), dot, fill=GOLD if i in mark else INK, edge=INK, lw=1, z=4)
    if hline is not None:
        s.ax.plot([x0, x1], [py(hline), py(hline)], color=MUTE, lw=2.6, ls='--', zorder=3)
        if hline_label:
            s.text(x0 + 0.2, py(hline) + 0.25, hline_label, size=size, color=MUTE, weight='bold', ha='left')
    if line:
        b, m = line
        s.ax.plot([px(lo_x + padx), px(hi_x - padx)], [py(b + m * (lo_x + padx)), py(b + m * (hi_x - padx))], color=RED, lw=3.4, zorder=5)
        if line_label:
            s.text(px(lo_x + padx) + 0.15, py(b + m * (hi_x - padx)) - 0.1 if False else y1 - 0.15, line_label, size=size, color=RED, weight='bold', ha='left')
    return s


@fig('x_rowsplit')
def x_rowsplit(w, h, parts=(), size=17, **_):
    s = Scene(w, h)
    tot = sum(p['n'] for p in parts)
    x = 0.1
    usable = w - 0.2
    gap = 0.12
    avail = usable - gap * (len(parts) - 1)
    for p in parts:
        bw = max(1.6, avail * p['n'] / tot)
        p['_w'] = bw
    scale = avail / sum(p['_w'] for p in parts)
    for p in parts:
        p['_w'] *= scale
    for p in parts:
        bw = p['_w']
        fill = {'ink': INK, 'gold': GOLD, 'red': RED}.get(p.get('fill', 'paper'), PAPER)
        col = PAPER if fill in (INK, RED) else INK
        by = h - 1.7
        s.box(x, by, bw, 1.3, '', fill=fill, edge=INK, lw=2.0, r=0.06)
        s.text(x + bw / 2, by + 0.88, p['label'], size=size + 3, weight='bold', color=col)
        s.text(x + bw / 2, by + 0.42, f"{p['n']} rows  |  {p['sub']}", size=size - 2, color=col)
        for i, ln in enumerate(K.wrap(p['role'], size, 'regular', bw - 0.2)):
            s.text(x + bw / 2, by - 0.35 - i * size * 1.2 / 72, ln, size=size, color=BODY)
        x += bw + gap
    return s


def _leaves(n):
    return 1 if 'v' in n else _leaves(n['yes']) + _leaves(n['no'])


def _depth(n):
    return 0 if 'v' in n else 1 + max(_depth(n['yes']), _depth(n['no']))


@fig('x_tree')
def x_tree(w, h, node=None, size=16, **_):
    s = Scene(w, h)
    d = _depth(node)
    nl = _leaves(node)
    slot = (w - 0.2) / nl
    ylev = lambda k: h - 0.55 - k * ((h - 1.1) / max(d, 1))

    def draw(n, k, left):
        wd = _leaves(n) * slot
        cx = 0.1 + left + wd / 2
        if 'v' in n:
            bw = min(slot - 0.12, 1.5)
            s.box(cx - bw / 2, ylev(k) - 0.33, bw, 0.66, n['v'], size=size, fill=GOLD, edge=INK, lw=1.8, weight='bold')
            return cx
        lc = draw(n['yes'], k + 1, left)
        rc = draw(n['no'], k + 1, left + _leaves(n['yes']) * slot)
        qw = min(max(K.width_in(n['q'], size, 'bold') + 0.35, 1.6), wd - 0.1 if wd > 1.8 else 3.0)
        s.box(cx - qw / 2, ylev(k) - 0.33, qw, 0.66, n['q'], size=size, fill=PAPER, edge=INK, lw=2.0, weight='bold')
        for c, lab in ((lc, 'yes'), (rc, 'no')):
            s.line(cx + (-0.25 if c < cx else 0.25), ylev(k) - 0.33, c, ylev(k + 1) + 0.33, color=INK, lw=1.8)
            s.text((cx + c) / 2 + (-0.2 if c < cx else 0.2), (ylev(k) + ylev(k + 1)) / 2 + 0.05, lab, size=size - 1, color=RED, weight='bold')
        return cx
    draw(node, 0, 0)
    return s


def math_heights(lines, size=28):
    """Row heights in inches: tall maths (fractions, sums) needs more room."""
    out = []
    for ln in lines:
        t = ln[1] if isinstance(ln, (tuple, list)) else ln
        tall = ('\\frac' in t) or ('\\sum' in t) or ('\\sqrt' in t and '\\frac' in t)
        out.append((1.3 if tall else 0.72) * size / 28)
    return out


@fig('x_math')
def x_math(w, h, lines=(), size=28, **_):
    """Lines of maths, each as mathtext, e.g. r'$\\hat{y} = b_0 + b_1 x_1$'. A line may be a (label, mathtext) pair; the label sits in small grey text on the left."""
    s = Scene(w, h)
    hs = math_heights(lines, size)
    y = h
    for ln, rh in zip(lines, hs):
        yc = y - rh / 2
        y -= rh
        if isinstance(ln, (tuple, list)):
            s.text(0.1, yc, ln[0], size=15, color=MUTE, ha='left')
            s.text(w / 2 + 1.0, yc, ln[1], size=size, ha='center')
        else:
            s.text(w / 2, yc, ln, size=size, ha='center')
    return s
