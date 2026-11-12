"""Figure kinds for sessions 7 to 9 (author C): derivatives, partial derivatives and the gradient, the chain rule and the Jacobian.
Registered like the kinds in diagrams_ml.py; render with diagrams.render({'kind': 'mc_curve', ...}, w, h).

  mc_curve    fn, xlim, ylim, tangents, secants, points, triangle, arrows, marks        a function drawn with tangent and secant lines
  mc_contour  fn (two inputs), xlim, ylim, levels, points, arrows, field                 a contour plot with gradient arrows
  mc_slice    fn, fixed, value, point                                                    a contour plot beside the slice that a partial derivative reads
  mc_graph    nodes, edges                                                               a computation graph with forward values and backward derivatives
  mc_jac      rows, cols, cells, nums                                                    a Jacobian matrix with symbols and numbers
  mc_warp     jac, at                                                                    a small square and what the Jacobian does to it
  mc_product  f, g, df, dg                                                               the product rule as a rectangle that grows
  mc_entries  a gradient vector with one entry per parameter
  mc_sheet    cols, rows, cells, hl                                                      a spreadsheet region drawn with its real column letters and row numbers
"""
import math
import numpy as np
from matplotlib.patches import Rectangle
from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, PALE, fig
import slidekit as K

# the delivery data used in sessions 7 to 9: distance in km, fee in thousand UGX (illustrative, made-up numbers)
DX = np.array([1.0, 2.0, 3.0, 4.0])
DY = np.array([3.0, 5.0, 6.0, 9.0])

FUNCS = {
    'square': lambda x: x ** 2,
    'line': lambda x: 2 * x + 1,
    'cubic': lambda x: x ** 3 - 3 * x,
    'exp': lambda x: np.exp(x),
    'ln': lambda x: np.log(x),
    'loss_w': lambda w: np.array([np.mean((wi * DX - DY) ** 2) for wi in np.atleast_1d(w)]),
    'loss_wb': lambda w, b: np.mean((w[..., None] * DX + b[..., None] - DY) ** 2, axis=-1),
    'bowl': lambda x, y: x ** 2 + 3 * y ** 2,
}


def _fn(name):
    return FUNCS[name]


def _fmt(v):
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return f'{v:g}'


class Frame:
    """Plot area inside a Scene: data to inch conversion, axes, ticks and a clip rectangle."""

    def __init__(self, s, x0, x1, y0, y1, xlim, ylim, xlabel='', ylabel='', xticks=None, yticks=None, tick_size=14, label_size=16, fmtx=_fmt, fmty=_fmt, lab_x=0.26):
        self.s, self.L, self.R, self.B, self.T = s, x0, x1, y0, y1
        self.xlim, self.ylim = xlim, ylim
        s.line(x0, y0, x1, y0, color=INK, lw=2)
        s.line(x0, y0, x0, y1, color=INK, lw=2)
        for v in (xticks or []):
            s.line(self.px(v), y0, self.px(v), y0 - 0.07, color=INK, lw=1.5)
            s.text(self.px(v), y0 - 0.25, fmtx(v), size=tick_size, color=GREY)
        for v in (yticks or []):
            s.line(x0, self.py(v), x0 - 0.07, self.py(v), color=INK, lw=1.5)
            s.text(x0 - 0.12, self.py(v), fmty(v), size=tick_size, color=GREY, ha='right')
        if xlabel:
            s.text((x0 + x1) / 2, 0.22, xlabel, size=label_size, color=MUTE)
        if ylabel:
            s.text(lab_x, (y0 + y1) / 2, ylabel, size=label_size, color=MUTE, rot=90)
        self.clip = Rectangle((x0, y0), x1 - x0, y1 - y0, fc='none', ec='none')
        s.ax.add_patch(self.clip)

    def px(self, v):
        return self.L + (v - self.xlim[0]) / (self.xlim[1] - self.xlim[0]) * (self.R - self.L)

    def py(self, v):
        return self.B + (v - self.ylim[0]) / (self.ylim[1] - self.ylim[0]) * (self.T - self.B)

    def plot(self, xs, ys, **kw):
        ln, = self.s.ax.plot([self.px(v) for v in xs], [self.py(v) for v in ys], **kw)
        ln.set_clip_path(self.clip)
        return ln


def _slope(f, x, h=1e-5):
    return float((f(np.array([x + h]))[0] - f(np.array([x - h]))[0]) / (2 * h))


# ------------------------------------------------------------------ mc_curve
@fig('x_mc_curve')
def x_mc_curve(w, h, fn='square', xlim=(0, 5), ylim=(0, 25), xlabel='x', ylabel='f(x)', xticks=None, yticks=None, tangents=(), secants=(), points=(), triangle=None,
               arrows=(), curve_label=None, size=16, **_):
    """tangents: [{x, label, ldx, ldy}] ; secants: [{x, h, label, ldx, ldy, color}] ; points: [{x, label, ldx, ldy, fill}] ; triangle: {x0, x1, run, rise}
    arrows: [{x0, y0, x1, y1, label, ldx, ldy}] in data units (free arrows, used to show a direction of travel)."""
    s = Scene(w, h)
    f = _fn(fn)
    fr = Frame(s, 1.2, w - 0.3, 0.85, h - 0.3, xlim, ylim, xlabel, ylabel, xticks, yticks)
    xs = np.linspace(xlim[0], xlim[1], 400)
    fr.plot(xs, f(xs), color=INK, lw=3.4, zorder=3)
    if curve_label:
        cl = curve_label
        s.text(fr.px(cl['x']), fr.py(cl['y']), cl['text'], size=size, weight='bold', ha=cl.get('ha', 'left'), bbox=dict(boxstyle='round,pad=0.1', fc=PAPER, ec='none'))
    for sc in secants:
        x0, hh = sc['x'], sc['h']
        y0, y1 = f(np.array([x0]))[0], f(np.array([x0 + hh]))[0]
        m = (y1 - y0) / hh
        col = sc.get('color', MUTE)
        fr.plot(xlim, [y0 + m * (xlim[0] - x0), y0 + m * (xlim[1] - x0)], color=col, lw=2.4, zorder=4, ls='--' if sc.get('dash', True) else '-')
        s.circle(fr.px(x0 + hh), fr.py(y1), 0.085, fill=PAPER, edge=col, lw=2, z=6)
        if sc.get('label'):
            s.text(fr.px(x0 + hh) + sc.get('ldx', 0.15), fr.py(y1) + sc.get('ldy', 0.2), sc['label'], size=size, color=col if col != MUTE else BODY, ha='left', weight='bold', bbox=dict(boxstyle='round,pad=0.1', fc=PAPER, ec='none'))
    for t in tangents:
        x0 = t['x']
        y0 = f(np.array([x0]))[0]
        m = _slope(f, x0)
        fr.plot(xlim, [y0 + m * (xlim[0] - x0), y0 + m * (xlim[1] - x0)], color=RED, lw=3.0, zorder=5)
        if t.get('label'):
            s.text(fr.px(x0) + t.get('ldx', 0.15), fr.py(y0) + t.get('ldy', 0.3), t['label'], size=size, color=RED, weight='bold', ha=t.get('ha', 'left'), bbox=dict(boxstyle='round,pad=0.1', fc=PAPER, ec='none'))
    if triangle:
        a, b = triangle['x0'], triangle['x1']
        ya, yb = f(np.array([a]))[0], f(np.array([b]))[0]
        s.line(fr.px(a), fr.py(ya), fr.px(b), fr.py(ya), color=RED, lw=2.4, dash=True, z=5)
        s.line(fr.px(b), fr.py(ya), fr.px(b), fr.py(yb), color=RED, lw=2.4, dash=True, z=5)
        s.text((fr.px(a) + fr.px(b)) / 2, fr.py(ya) - 0.28, triangle.get('run', 'run'), size=size, color=RED, weight='bold')
        s.text(fr.px(b) + 0.15, (fr.py(ya) + fr.py(yb)) / 2, triangle.get('rise', 'rise'), size=size, color=RED, weight='bold', ha='left')
    for p in points:
        y0 = f(np.array([p['x']]))[0]
        s.circle(fr.px(p['x']), fr.py(y0), 0.13, fill=p.get('fill', GOLD), edge=INK, lw=2, z=7)
        if p.get('label'):
            s.text(fr.px(p['x']) + p.get('ldx', 0.2), fr.py(y0) + p.get('ldy', 0.3), p['label'], size=size, ha=p.get('ha', 'left'), weight='bold', color=INK, bbox=dict(boxstyle='round,pad=0.1', fc=PAPER, ec='none'))
    for a in arrows:
        s.arrow(fr.px(a['x0']), fr.py(a['y0']), fr.px(a['x1']), fr.py(a['y1']), color=RED, lw=3.4, head=22, z=8)
        if a.get('label'):
            s.text((fr.px(a['x0']) + fr.px(a['x1'])) / 2 + a.get('ldx', 0), (fr.py(a['y0']) + fr.py(a['y1'])) / 2 + a.get('ldy', 0.3), a['label'], size=size, color=RED, weight='bold', ha=a.get('ha', 'center'), bbox=dict(boxstyle='round,pad=0.1', fc=PAPER, ec='none'))
    return s


# ------------------------------------------------------------------ contours
def _contour_core(s, fr, f, levels, nx=160, ny=160):
    xs = np.linspace(fr.xlim[0], fr.xlim[1], nx)
    ys = np.linspace(fr.ylim[0], fr.ylim[1], ny)
    X, Y = np.meshgrid(xs, ys)
    Z = f(X, Y)
    Xi = fr.L + (X - fr.xlim[0]) / (fr.xlim[1] - fr.xlim[0]) * (fr.R - fr.L)
    Yi = fr.B + (Y - fr.ylim[0]) / (fr.ylim[1] - fr.ylim[0]) * (fr.T - fr.B)
    cs = s.ax.contour(Xi, Yi, Z, levels=levels, colors=[MUTE], linewidths=1.8, zorder=2)
    return cs, Z, xs, ys


def _ray_cross(f, level, x0, y0, ang, rmax=6.0, n=3000):
    """Distance along a ray from (x0, y0) at angle ang (degrees) where f first reaches `level` (f grows along the ray); None if it does not."""
    r = np.linspace(0, rmax, n)
    xs, ys = x0 + r * math.cos(math.radians(ang)), y0 + r * math.sin(math.radians(ang))
    z = f(xs, ys)
    idx = np.where(z >= level)[0]
    if len(idx) == 0:
        return None
    return xs[idx[0]], ys[idx[0]]


@fig('x_mc_contour')
def x_mc_contour(w, h, fn='bowl', xlim=(-3, 3), ylim=(-2, 2), xlabel='x', ylabel='y', xticks=None, yticks=None, levels=(1, 4, 9, 16), level_ray=None, points=(), arrows=(),
                 field=None, size=16, equal=False, side=(), **_):
    """points: [{x, y, label, ldx, ldy, fill}] ; arrows: [{x, y, dx, dy, label, ldx, ldy, color}] with (dx, dy) in data units ;
    field: {'step': (sx, sy), 'scale': 0.1}  arrows of the gradient on a grid, drawn short ; level_ray: [x0, y0, angle_deg] where the contour values are written."""
    s = Scene(w, h)
    f = _fn(fn)
    x1, y1 = w - 0.3, h - 0.3
    if equal:
        sc = min((x1 - 1.2) / (xlim[1] - xlim[0]), (y1 - 0.85) / (ylim[1] - ylim[0]))
        x1, y1 = 1.2 + sc * (xlim[1] - xlim[0]), 0.85 + sc * (ylim[1] - ylim[0])
    fr = Frame(s, 1.2, x1, 0.85, y1, xlim, ylim, xlabel, ylabel, xticks, yticks)
    s.rect(fr.L, fr.B, fr.R - fr.L, fr.T - fr.B, fill=PAPER, edge=PAPER, lw=0, z=0)
    for sd in side:
        s.text(sd['x'], sd['y'], sd['text'], size=sd.get('size', 16), color=sd.get('color', INK), weight=sd.get('weight', 'normal'), ha=sd.get('ha', 'left'))
    cs, Z, xs, ys = _contour_core(s, fr, f, list(levels))
    rays = []
    if level_ray:
        rays = list(level_ray) if isinstance(level_ray[0], (list, tuple)) else [level_ray]   # one ray, or a list of rays (labels on both sides of the bowl)
    for x0, y0, ang in rays:
        for lv in levels:
            c = _ray_cross(f, lv, x0, y0, ang)
            if c and xlim[0] < c[0] < xlim[1] and ylim[0] < c[1] < ylim[1]:
                s.text(fr.px(c[0]), fr.py(c[1]), _fmt(lv) if abs(lv - round(lv)) < 1e-9 else f'{lv:g}', size=14, color=BODY, z=9,
                       bbox=dict(boxstyle='round,pad=0.12', fc=PAPER, ec='none'))
    if field:
        sx, sy = field['step']
        sc = field.get('scale', 0.1)
        for gx in np.arange(xlim[0] + sx / 2, xlim[1], sx):
            for gy in np.arange(ylim[0] + sy / 2, ylim[1], sy):
                e = 1e-5
                gxv = (f(np.array(gx + e), np.array(gy)) - f(np.array(gx - e), np.array(gy))) / (2 * e)
                gyv = (f(np.array(gx), np.array(gy + e)) - f(np.array(gx), np.array(gy - e))) / (2 * e)
                s.arrow(fr.px(gx), fr.py(gy), fr.px(gx) + float(gxv) * sc * (fr.R - fr.L) / (xlim[1] - xlim[0]), fr.py(gy) + float(gyv) * sc * (fr.T - fr.B) / (ylim[1] - ylim[0]),
                        color=INK, lw=2.0, head=13, z=6)
    for a in arrows:
        col = a.get('color', RED)
        s.arrow(fr.px(a['x']), fr.py(a['y']), fr.px(a['x'] + a['dx']), fr.py(a['y'] + a['dy']), color=col, lw=3.4, head=22, z=8)
        if a.get('label'):
            s.text(fr.px(a['x'] + a['dx'] / 2) + a.get('ldx', 0), fr.py(a['y'] + a['dy'] / 2) + a.get('ldy', 0.3), a['label'], size=size, color=col, weight='bold', ha=a.get('ha', 'center'), z=9, bbox=dict(boxstyle='round,pad=0.1', fc=PAPER, ec='none'))
    for p in points:
        s.circle(fr.px(p['x']), fr.py(p['y']), 0.13, fill=p.get('fill', GOLD), edge=INK, lw=2, z=7)
        if p.get('label'):
            s.text(fr.px(p['x']) + p.get('ldx', 0.2), fr.py(p['y']) + p.get('ldy', 0.3), p['label'], size=size, ha=p.get('ha', 'left'), weight='bold', z=9, bbox=dict(boxstyle='round,pad=0.1', fc=PAPER, ec='none'))
    return s


@fig('x_mc_slice')
def x_mc_slice(w, h, fn='loss_wb', fixed='b', value=0.0, xlim=(0, 3.5), ylim=(-1, 3), point=1.0, zlim=(0, 40), xlabel='w', ylabel='b', zlabel='L', levels=(1, 3, 10, 20, 30),
               level_ray=None, slope_label='slope', **_):
    """Left: contour plot with one input held fixed (a straight line through it). Right: the loss along that line, with the tangent at `point`. Only fixed='b' is drawn."""
    s = Scene(w, h)
    f2 = _fn(fn)
    lw_ = w * 0.45
    fr = Frame(s, 1.2, lw_, 0.85, h - 0.3, xlim, ylim, xlabel, ylabel, [0, 1, 2, 3], [-1, 0, 1, 2, 3])
    cs, Z, xs, ys = _contour_core(s, fr, f2, list(levels))
    rays = []
    if level_ray:
        rays = list(level_ray) if isinstance(level_ray[0], (list, tuple)) else [level_ray]
    for x0, y0, ang in rays:
        for lv in levels:
            c = _ray_cross(f2, lv, x0, y0, ang)
            if c and xlim[0] < c[0] < xlim[1] and ylim[0] < c[1] < ylim[1]:
                s.text(fr.px(c[0]), fr.py(c[1]), f'{lv:g}', size=14, color=BODY, z=9, bbox=dict(boxstyle='round,pad=0.1', fc=PAPER, ec='none'))
    s.line(fr.px(xlim[0]), fr.py(value), fr.px(xlim[1]), fr.py(value), color=RED, lw=3.4, z=6)
    s.circle(fr.px(point), fr.py(value), 0.12, fill=GOLD, edge=INK, lw=2, z=8)
    s.text(fr.px(xlim[0]) + 0.1, fr.py(value) - 0.3, f'{fixed} held at {_fmt(value)}', size=15, color=RED, weight='bold', ha='left', z=9, bbox=dict(boxstyle='round,pad=0.1', fc=PAPER, ec='none'))
    # right panel: the curve along the line
    g = lambda ww: f2(np.atleast_1d(ww).astype(float), np.full(np.atleast_1d(ww).shape, float(value)))
    fr2 = Frame(s, lw_ + 1.45, w - 0.3, 0.85, h - 0.3, xlim, zlim, xlabel, zlabel, [0, 1, 2, 3], [0, 10, 20, 30, 40], lab_x=lw_ + 0.5)
    xx = np.linspace(xlim[0], xlim[1], 300)
    fr2.plot(xx, g(xx), color=INK, lw=3.4, zorder=3)
    y0 = float(g(point)[0])
    m = _slope(lambda t: g(t), point)
    fr2.plot(xlim, [y0 + m * (xlim[0] - point), y0 + m * (xlim[1] - point)], color=RED, lw=3.0, zorder=5)
    s.circle(fr2.px(point), fr2.py(y0), 0.12, fill=GOLD, edge=INK, lw=2, z=8)
    s.text(fr2.px(point) + 0.35, fr2.py(y0) + 0.55, f'{slope_label} {m:.1f}', size=16, color=RED, weight='bold', ha='left', z=9)
    return s


# ------------------------------------------------------------------ computation graph
@fig('x_mc_graph')
def x_mc_graph(w, h, nodes=(), edges=(), size=18, small=16, box_h=0.7, **_):
    """nodes: [{x, y, label, fwd, bwd, fill, width}] with x, y as fractions of the canvas (0 to 1, centre of the node box) ;
    edges: [{a, b, label, back}] arrows from node a to node b ; `label` sits above the arrow (the operation or local slope), `back` is a red backward arrow
    drawn under it with its value."""
    s = Scene(w, h)
    bws = [n.get('width') or max(1.0, K.width_in(n['label'], size, 'bold') + 0.4) for n in nodes]
    pad = max(bws) / 2 + 0.1
    pos = []
    for n, bw in zip(nodes, bws):
        cx, cy = pad + n['x'] * (w - 2 * pad), 0.55 + n['y'] * (h - 1.1)
        pos.append((cx, cy, bw))
    for n, (cx, cy, bw) in zip(nodes, pos):
        fill = {'gold': GOLD, 'ink': INK}.get(n.get('fill'), PAPER)
        col = PAPER if fill == INK else INK
        if n.get('ellipsis'):
            s.text(cx, cy, '...', size=size + 6, weight='bold', color=MUTE)
            continue
        s.box(cx - bw / 2, cy - box_h / 2, bw, box_h, n['label'], size=size, fill=fill, edge=INK, lw=2.0, weight='bold', color=col)
        if n.get('fwd'):
            s.text(cx, cy - box_h / 2 - 0.25, n['fwd'], size=small, color=INK)
        if n.get('bwd'):
            s.text(cx, cy + box_h / 2 + 0.25, n['bwd'], size=small, color=RED, weight='bold')
    for e in edges:
        (ax_, ay, aw), (bx, by, bw) = pos[e['a']], pos[e['b']]
        horizontal = abs(ay - by) < 0.05
        if horizontal:
            x1, x2 = (ax_ + aw / 2 + 0.05, bx - bw / 2 - 0.05) if bx > ax_ else (ax_ - aw / 2 - 0.05, bx + bw / 2 + 0.05)
            s.arrow(x1, ay + 0.1, x2, by + 0.1, color=INK, lw=2.4, head=18)
            if e.get('label'):
                s.text((x1 + x2) / 2, ay + 0.42, e['label'], size=small, color=INK)
            if e.get('back'):
                s.arrow(x2, by - 0.12, x1, ay - 0.12, color=RED, lw=2.4, head=18)
                s.text((x1 + x2) / 2, ay - 0.42, e['back'], size=small, color=RED, weight='bold')
        else:
            dx, dy = bx - ax_, by - ay
            L = math.hypot(dx, dy)
            ux, uy = dx / L, dy / L
            # start and end at the box borders (rectangle clipping)
            def clip(cx, cy, bw_, sgn):
                tx = (bw_ / 2 + 0.06) / abs(ux) if abs(ux) > 1e-9 else 1e9
                ty = (box_h / 2 + 0.06) / abs(uy) if abs(uy) > 1e-9 else 1e9
                t = min(tx, ty)
                return cx + sgn * ux * t, cy + sgn * uy * t
            x1, y1 = clip(ax_, ay, aw, 1)
            x2, y2 = clip(bx, by, bw, -1)
            s.arrow(x1, y1, x2, y2, color=INK, lw=2.4, head=18)
            if e.get('label'):
                s.text((x1 + x2) / 2 + e.get('ldx', -0.1), (y1 + y2) / 2 + e.get('ldy', 0.25), e['label'], size=small, color=INK, ha=e.get('ha', 'center'))
            if e.get('back'):
                s.text((x1 + x2) / 2 + e.get('bdx', 0.1), (y1 + y2) / 2 + e.get('bdy', -0.25), e['back'], size=small, color=RED, weight='bold', ha=e.get('bha', 'center'))
    return s


# ------------------------------------------------------------------ Jacobian drawn as a matrix
@fig('x_mc_jac')
def x_mc_jac(w, h, rows=('u', 'v'), cols=('x1', 'x2'), cells=(), nums=(), size=22, num_size=22, caption_rows='outputs', caption_cols='inputs', **_):
    """cells: [[mathtext]] symbolic entries ; nums: [[text]] the same entries as numbers at one point."""
    s = Scene(w, h)
    nr, nc = len(rows), len(cols)
    cw, rh = min(2.6, (w - 3.2) / nc), min(1.5, (h - 1.7) / nr)
    x0 = (w - nc * cw) / 2 + 0.7
    ytop = h - 1.0
    for j, c in enumerate(cols):
        s.text(x0 + (j + 0.5) * cw, ytop + 0.45, c, size=20, weight='bold', color=MUTE)
    s.text(x0 + nc * cw / 2, ytop + 0.85, 'one column for each ' + caption_cols[:-1], size=15, color=MUTE)
    for i, r in enumerate(rows):
        s.text(x0 - 0.45, ytop - (i + 0.5) * rh, r, size=20, weight='bold', color=MUTE)
    s.text(x0 - 1.3, ytop - nr * rh / 2, 'one row for\neach ' + caption_rows[:-1], size=15, color=MUTE, ha='center')
    for i in range(nr):
        for j in range(nc):
            s.rect(x0 + j * cw, ytop - (i + 1) * rh, cw, rh, fill=PAPER, edge=HAIR, lw=1.2, z=1)
            if cells:
                s.text(x0 + (j + 0.5) * cw, ytop - (i + 0.5) * rh + 0.3, cells[i][j], size=size, ha='center')
            if nums:
                s.box(x0 + j * cw + 0.25, ytop - (i + 1) * rh + 0.08, cw - 0.5, 0.52, nums[i][j], size=num_size, fill=GOLD, edge=INK, lw=1.4, weight='bold', r=0.05)
    for sgn, xb in ((1, x0 - 0.08), (-1, x0 + nc * cw + 0.08)):
        s.line(xb, ytop + 0.05, xb, ytop - nr * rh - 0.05, color=INK, lw=3)
        s.line(xb, ytop + 0.05, xb + sgn * 0.14, ytop + 0.05, color=INK, lw=3)
        s.line(xb, ytop - nr * rh - 0.05, xb + sgn * 0.14, ytop - nr * rh - 0.05, color=INK, lw=3)
    return s


@fig('x_mc_warp')
def x_mc_warp(w, h, jac=((3, 2), (1, 6)), at=(2, 3), size=16, sc=0.42, **_):
    """Left: the input plane with a small square at `at`. Right: the output plane, where the Jacobian turns the square's two sides into the two columns of J."""
    s = Scene(w, h)
    pw = (w - 1.7) / 2
    J = np.array(jac, float)
    ox0, ox1 = 0.45, 0.45 + pw + 0.8
    for title, ox in (('Inputs (x1, x2)', ox0), ('Outputs (u, v)', ox1)):
        s.line(ox, 0.45, ox + pw, 0.45, color=INK, lw=2)
        s.line(ox, 0.45, ox, h - 0.65, color=INK, lw=2)
        s.text(ox + pw / 2, h - 0.3, title, size=17, weight='bold')
    ox, oy, side = ox0 + 0.6, 0.95, 1.3
    s.rect(ox, oy, side, side, fill=PALE, edge=INK, lw=2, z=2)
    s.arrow(ox, oy, ox + side, oy, color=RED, lw=3.4, head=20, z=5)
    s.arrow(ox, oy, ox, oy + side, color=INK, lw=3.4, head=20, z=5)
    s.text(ox + side / 2, oy - 0.0 + 0.3, 'tiny step\nh in x1', size=15, color=RED, weight='bold', z=6)
    s.text(ox + side + 0.1, oy + side + 0.2, 'tiny step h in x2', size=15, weight='bold', ha='left')
    qx, qy = ox1 + 1.6, 0.95
    c1 = (J[0, 0] * sc, J[1, 0] * sc)
    c2 = (J[0, 1] * sc, J[1, 1] * sc)
    s.poly([(qx, qy), (qx + c1[0], qy + c1[1]), (qx + c1[0] + c2[0], qy + c1[1] + c2[1]), (qx + c2[0], qy + c2[1])], fill=PALE, edge=INK, lw=2, z=2)
    s.arrow(qx, qy, qx + c1[0], qy + c1[1], color=RED, lw=3.4, head=20, z=5)
    s.arrow(qx, qy, qx + c2[0], qy + c2[1], color=INK, lw=3.4, head=20, z=5)
    s.text(qx + c1[0] + 0.12, qy + c1[1] - 0.25, f'h × column 1\n= h × ({_fmt(J[0, 0])}, {_fmt(J[1, 0])})', size=15, color=RED, weight='bold', ha='left')
    s.text(qx + c2[0] - 0.2, qy + c2[1] - 0.1, f'h × column 2\n= h × ({_fmt(J[0, 1])}, {_fmt(J[1, 1])})', size=15, weight='bold', ha='right')
    s.arrow(ox0 + pw + 0.12, h / 2, ox1 - 0.12, h / 2, color=INK, lw=2.6, head=20)
    s.text((ox0 + pw + ox1) / 2, h / 2 + 0.3, 'J', size=22, weight='bold')
    return s


@fig('x_mc_product')
def x_mc_product(w, h, f='f', g='g', df='df', dg='dg', size=17, **_):
    """The product rule as area: a rectangle f wide and g tall grows by a strip on the right and a strip on top (the tiny corner is ignored)."""
    s = Scene(w, h)
    fw, gh, sf, sg = 3.6, 2.2, 0.55, 0.42
    x0, y0 = (w - fw - sf) / 2 - 0.3, 0.9
    s.rect(x0, y0, fw, gh, fill=PALE, edge=INK, lw=2.4, z=2)
    s.text(x0 + fw / 2, y0 + gh / 2, f'area = {f} × {g}', size=size + 2, weight='bold')
    s.rect(x0 + fw, y0, sf, gh, fill=GOLD, edge=INK, lw=2, z=3)
    s.rect(x0, y0 + gh, fw, sg, fill=GOLD, edge=INK, lw=2, z=3)
    s.rect(x0 + fw, y0 + gh, sf, sg, fill=PAPER, edge=GREY, lw=1.2, z=3)
    s.text(x0 + fw / 2, y0 - 0.3, f'{f}', size=size, weight='bold')
    s.text(x0 - 0.2, y0 + gh / 2, f'{g}', size=size, weight='bold', ha='right')
    s.text(x0 + fw + sf / 2, y0 - 0.3, f'{df}', size=size, weight='bold', color=RED)
    s.text(x0 + fw + sf + 0.2, y0 + gh + sg / 2, f'{dg}', size=size, weight='bold', color=RED, ha='left')
    s.text(x0 + fw + sf + 0.2, y0 + gh / 2, f'new strip:\n{df} × {g}', size=15, color=INK, ha='left')
    s.text(x0 + fw / 2, y0 + gh + sg + 0.35, f'new strip: {f} × {dg}', size=15, color=INK)
    s.text(x0 + fw + sf + 0.2, y0 + gh + sg + 0.35, 'tiny corner,\nignored', size=14, color=MUTE, ha='left')
    return s


@fig('x_mc_entries')
def x_mc_entries(w, h, count_label='8 billion entries', size=18, sub='N = number of parameters', **_):
    """A gradient vector drawn as a tall column: one entry per parameter, with the middle left out."""
    s = Scene(w, h)
    bx, bw, bh = 0.7, 3.2, 0.62
    labels = [r'$\partial L/\partial\theta_1$', r'$\partial L/\partial\theta_2$', r'$\partial L/\partial\theta_3$', None, r'$\partial L/\partial\theta_N$']
    y = h - 0.6
    ys = []
    for lab in labels:
        if lab is None:
            s.text(bx + bw / 2, y - 0.2, '.  .  .', size=26, weight='bold', color=MUTE)
            y -= 0.5
            continue
        s.box(bx, y - bh, bw, bh, lab, size=size + 2, fill=PAPER, edge=INK, lw=1.8, r=0.04)
        ys.append((y - bh, y))
        y -= bh + 0.1
    top, bot = ys[0][1], ys[-1][0]
    s.line(bx + bw + 0.2, top, bx + bw + 0.2, bot, color=RED, lw=3)
    s.line(bx + bw + 0.2, top, bx + bw + 0.05, top, color=RED, lw=3)
    s.line(bx + bw + 0.2, bot, bx + bw + 0.05, bot, color=RED, lw=3)
    tx = bx + bw + 0.5
    mid = (top + bot) / 2
    s.text(tx, mid + 0.8, 'One entry for every\nparameter of the model', size=size, weight='bold', ha='left', va='center')
    s.text(tx, mid - 0.2, sub, size=size - 2, color=BODY, ha='left')
    s.text(tx, mid - 0.95, count_label, size=size + 1, weight='bold', color=RED, ha='left')
    return s


@fig('x_mc_scale')
def x_mc_scale(w, h, items=(), size=17, **_):
    """Horizontal bars on a log scale: items [{label, value, text}]. Shows how far apart parameter counts are."""
    s = Scene(w, h)
    x0, x1 = 0.4, w - 0.5
    top = h - 0.5
    lo, hi = 0, 11.5
    px = lambda e: x0 + (e - lo) / (hi - lo) * (x1 - x0)
    n = len(items)
    row = (top - 1.0) / n
    for k in (0, 2, 4, 6, 8, 10):
        s.line(px(k), 0.9, px(k), top, color=HAIR, lw=1.2, z=0)
        s.text(px(k), 0.6, '1' if k == 0 else f'10^{k}', size=14, color=GREY)
    s.text((x0 + x1) / 2, 0.22, 'number of parameters, on a scale where each tick is 100 times larger', size=15, color=MUTE)
    for i, it in enumerate(items):
        yc = top - (i + 0.5) * row
        e = math.log10(it['value'])
        s.rect(x0, yc - 0.22, px(e) - x0, 0.44, fill=GOLD if it.get('hl') else INK, edge=INK, lw=1.4, z=3)
        s.text(x0 + 0.05, yc + 0.5, it['label'], size=size, weight='bold', ha='left')
        s.text(min(px(e) + 0.1, x1 - 2.2) if px(e) + 2.4 < x1 else px(e) - 0.1, yc - 0.0, it['text'], size=size - 1, ha='left' if px(e) + 2.4 < x1 else 'right',
               color=INK if px(e) + 2.4 < x1 else PAPER, weight='bold', z=6)
    return s


# ------------------------------------------------------------------ a spreadsheet region drawn with its real cell addresses
@fig('x_mc_sheet')
def x_mc_sheet(w, h, cols=('A', 'B'), rows=(1, 2), cells=(), hl=(), bold_first=True, size=16, **_):
    """cols: column letters shown across the top; rows: row numbers shown down the left; cells: [[text]] one list per row ;
    hl: [(i, j)] cells (row index, column index into cells) filled gold. The first row and first column are drawn bold (the headers)."""
    s = Scene(w, h)
    nr, nc = len(rows), len(cols)
    rw = 0.55
    cw = (w - 0.2 - rw) / nc
    rh = min(0.62, (h - 0.2 - 0.45) / nr)
    x0, top = 0.1 + rw, h - 0.1
    s.rect(0.1, top - 0.45 - nr * rh, rw + nc * cw, 0.45 + nr * rh, fill=PAPER, edge=INK, lw=1.8)
    for j, c in enumerate(cols):
        s.text(x0 + (j + 0.5) * cw, top - 0.22, c, size=14, color=GREY)
    s.line(0.1, top - 0.45, x0 + nc * cw, top - 0.45, color=HAIR, lw=1.2)
    s.line(x0, top, x0, top - 0.45 - nr * rh, color=HAIR, lw=1.2)
    for i, r in enumerate(rows):
        yc = top - 0.45 - (i + 0.5) * rh
        s.text(0.1 + rw / 2, yc, str(r), size=14, color=GREY)
        s.line(0.1, top - 0.45 - (i + 1) * rh, x0 + nc * cw, top - 0.45 - (i + 1) * rh, color=HAIR, lw=0.8)
        for j in range(nc):
            if (i, j) in [tuple(q) for q in hl]:
                s.rect(x0 + j * cw + 0.03, top - 0.45 - (i + 1) * rh + 0.03, cw - 0.06, rh - 0.06, fill=GOLD, edge=GOLD, lw=0, z=2)
            head = bold_first and (i == 0 or j == 0)
            s.text(x0 + (j + 0.5) * cw, yc, str(cells[i][j]), size=size, weight='bold' if head else 'normal', color=INK if head else BODY, z=5)
    for j in range(1, nc):
        s.line(x0 + j * cw, top - 0.45, x0 + j * cw, top - 0.45 - nr * rh, color=HAIR, lw=0.8)
    return s
