"""Figures and reference numbers for Sessions 4, 5 and 6 of Mathematics for AI and ML (author B).

Reference numbers (every number on a slide, in a notebook or in a workbook for these sessions comes from d4(), d5() or d6() below, computed with NumPy, never typed).

Figure kinds registered here (use as visual=dict(kind='name', ...)):
  sysrows   panels of lines a x + b y = c with the crossing point (the row picture of a system)
  colpic    the column picture: scaled columns added head to tail to reach b
  elim      augmented matrices before and after each row operation
  unitsq    the unit square and what a 2 by 2 matrix does to it (area scaling, determinant)
  designmat the tall system X w = y for a line fit, with the data rows
  manyfits  one data point and many lines through it
  eigpic    the unit circle before and after a symmetric matrix, with the eigen-directions
  lambdas   what an eigenvalue does to an arrow: 2, 0.5, 1, -1, 0
  cloud     a cloud of centred points with principal axes and optional projection onto one axis
  centre    raw points beside the same points with the mean subtracted
  power     arrows of power iteration converging to the eigen-direction
  embedmap  invented word vectors and their PCA picture
  svdpic    rotate, stretch, rotate
  imgs      a row of 8 by 8 grey-scale images
  scree     bars of singular values with cumulative share
  outer     a column times a row makes a rank 1 pattern
  lowrank   a big matrix as thin matrices (storage counts)
  lora      the published LoRA picture: frozen W plus trainable B and A
"""
import math
from functools import lru_cache

import numpy as np
from matplotlib.patches import Polygon

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, fig
import slidekit as K

SEED_EMB = 1
PALE = '#F1F1F1'
GOLD_SOFT = '#F3E7B0'


# =====================================================================================================
# Reference numbers
# =====================================================================================================
@lru_cache(maxsize=None)
def d4():
    """Session 4: a 2 by 2 system, a singular matrix, and the advertising data."""
    A = np.array([[2.0, 1.0], [1.0, -1.0]])
    b = np.array([5.0, 1.0])
    sol = np.linalg.solve(A, b)
    Ainv = np.linalg.inv(A)
    S = np.array([[1.0, 2.0], [2.0, 4.0]])
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0])        # advertising spend, UGX million per month (illustrative)
    y = np.array([14.0, 19.0, 27.0, 30.0, 38.0, 41.0, 52.0])  # sales, UGX million per month (illustrative)
    n = len(x)
    X = np.column_stack([np.ones(n), x])
    XtX = X.T @ X
    Xty = X.T @ y
    w = np.linalg.solve(XtX, Xty)
    pred = X @ w
    res = y - pred
    rmse = float(np.sqrt(np.mean(res ** 2)))
    X1 = np.array([[1.0, 4.0]])
    XtX1 = X1.T @ X1
    x2 = np.array([1.0, 2.0])
    X2 = np.column_stack([np.ones(2), x2, x2 ** 2])
    XtX2 = X2.T @ X2
    return dict(A=A, b=b, sol=sol, Ainv=Ainv, det=float(np.linalg.det(A)), S=S, rankS=int(np.linalg.matrix_rank(S)), x=x, y=y, n=n, X=X, XtX=XtX, Xty=Xty,
                detXtX=float(np.linalg.det(XtX)), w=w, pred=pred, res=res, rmse=rmse, sse=float(np.sum(res ** 2)), X1=X1, XtX1=XtX1, X2=X2, XtX2=XtX2,
                rank_X=int(np.linalg.matrix_rank(X)), rank_X2=int(np.linalg.matrix_rank(X2)), rank_XtX2=int(np.linalg.matrix_rank(XtX2)),
                pred7=float(w[0] + 7 * w[1]), mean_y=float(y.mean()))


@lru_cache(maxsize=None)
def d5():
    """Session 5: the matrix [[2,1],[1,2]], the covariance matrix of eight marks, power iteration."""
    A = np.array([[2.0, 1.0], [1.0, 2.0]])
    ev, V = np.linalg.eigh(A)            # ascending
    maths = np.array([53.0, 55.0, 63.0, 67.0, 48.0, 67.0, 56.0, 71.0])
    phys = np.array([53.0, 52.0, 62.0, 65.0, 49.0, 61.0, 57.0, 65.0])
    n = len(maths)
    mm, mp = maths.mean(), phys.mean()
    ca, cb = maths - mm, phys - mp
    C = np.cov(np.vstack([maths, phys]))     # divides by n - 1
    T, D = float(np.trace(C)), float(np.linalg.det(C))
    lam = np.array([(T + math.sqrt(T * T - 4 * D)) / 2, (T - math.sqrt(T * T - 4 * D)) / 2])
    v1 = np.array([C[0, 1], lam[0] - C[0, 0]])
    v1 = v1 / np.linalg.norm(v1)
    v2 = np.array([C[0, 1], lam[1] - C[0, 0]])
    v2 = v2 / np.linalg.norm(v2)
    # power iteration with 'divide by the largest entry'
    def power(M, v0, steps):
        v = np.array(v0, float)
        rows = []
        for k in range(steps):
            Mv = M @ v
            m = float(np.max(np.abs(Mv)))
            rows.append((k, v.copy(), Mv.copy(), m))
            v = Mv / m
        return rows, v
    pa, va = power(A, [1.0, 0.0], 5)
    pc, vc = power(C, [0.0, 1.0], 6)
    return dict(A=A, ev=ev, V=V, maths=maths, phys=phys, n=n, mm=float(mm), mp=float(mp), ca=ca, cb=cb, C=C, T=T, D=D, lam=lam, v1=v1, v2=v2,
                pa=pa, va=va, pc=pc, vc=vc, vc_unit=vc / np.linalg.norm(vc), explained=float(lam[0] / lam.sum()), rotation=np.array([[0.0, -1.0], [1.0, 0.0]]),
                lam_flip=np.linalg.eigvalsh(np.cov(np.vstack([maths, 100 - phys]))), C_flip=np.cov(np.vstack([maths, 100 - phys])))


@lru_cache(maxsize=None)
def d6():
    """Session 6: a 2 by 2 SVD, the 8 by 8 'H' image with noise, PCA of the eight marks, LoRA counts."""
    A = np.array([[2.0, 2.0], [-1.0, 2.0]])
    U, S, Vt = np.linalg.svd(A)
    AtA = A.T @ A
    H = np.ones((8, 8))
    H[:, [1, 6]] = 8
    H[3:5, 1:7] = 8
    rng = np.random.default_rng(39)
    noise = rng.integers(-2, 3, size=(8, 8))
    noisy = np.clip(H + noise, 0, 9)
    Un, Sn, Vtn = np.linalg.svd(noisy)

    def approx(k):
        return (Un[:, :k] * Sn[:k]) @ Vtn[:k]
    err_noisy = float(np.linalg.norm(noisy - H))
    err_k = {k: float(np.linalg.norm(approx(k) - H)) for k in range(1, 5)}
    energy = Sn ** 2 / np.sum(Sn ** 2)
    cum = np.cumsum(energy)
    k95 = int(np.searchsorted(cum, 0.95) + 1)
    # power iteration on noisy^T noisy, divide by largest entry
    M = noisy.T @ noisy
    v = np.ones(8)
    its = []
    for k in range(10):
        Mv = M @ v
        m = float(np.max(np.abs(Mv)))
        its.append((v.copy(), m))
        v = Mv / m
    v_unit = v / np.linalg.norm(v)
    # deflation: three rounds of 10 power steps, subtracting the rank 1 part of M each time
    defl = []
    Mk = M.copy()
    approx_sum = np.zeros((8, 8))
    for rnd in range(3):
        vk = np.ones(8)
        for k in range(10):
            Mv = Mk @ vk
            mk = float(np.max(np.abs(Mv)))
            vk = Mv / mk
        vu = vk / np.linalg.norm(vk)
        sk = math.sqrt(mk)
        uk = noisy @ vu / sk
        piece = sk * np.outer(uk, vu)
        approx_sum = approx_sum + piece
        defl.append(dict(m=mk, sigma=sk, v=vu, u=uk, piece=piece, err=float(np.linalg.norm(approx_sum - H))))
        Mk = Mk - mk * np.outer(vu, vu)
    sig1_pi = math.sqrt(its[-1][1])
    u1 = noisy @ v_unit / sig1_pi
    rank1_pi = sig1_pi * np.outer(u1, v_unit)
    # PCA of the eight marks (Session 5 data)
    p = d5()
    Xc = np.column_stack([p['ca'], p['cb']])
    Uc, Sc, Vtc = np.linalg.svd(Xc, full_matrices=False)
    var = Sc ** 2 / (p['n'] - 1)
    top = Vtc[0] if Vtc[0][0] > 0 else -Vtc[0]
    scores = Xc @ top
    return dict(A=A, U=U, S=S, Vt=Vt, AtA=AtA, H=H, noise=noise, noisy=noisy, Sn=Sn, Un=Un, Vtn=Vtn, approx=approx, err_noisy=err_noisy, err_k=err_k, energy=energy, cum=cum, k95=k95,
                its=its, defl=defl, sig1_pi=sig1_pi, v_unit=v_unit, u1=u1, rank1_pi=rank1_pi, rank1_svd=approx(1), Xc=Xc, var=var, ratio=var / var.sum(), top=top, scores=scores,
                score_var=float(np.var(scores, ddof=1)), lost=float(np.sum((Xc - np.outer(scores, top)) ** 2)),
                lora_d=1000, lora_r=8, lora_full=1000 * 1000, lora_small=2 * 1000 * 8, img_full=64, img_k2=2 * (8 + 8 + 1))


# =====================================================================================================
# Drawing helpers
# =====================================================================================================
class Frame:
    """Maps a world rectangle onto a canvas rectangle (inches), keeping equal scale in x and y."""

    def __init__(self, x0, y0, x1, y1, xr, yr, equal=True):
        self.cx0, self.cy0, self.cx1, self.cy1 = x0, y0, x1, y1
        self.xr, self.yr = xr, yr
        sx = (x1 - x0) / (xr[1] - xr[0])
        sy = (y1 - y0) / (yr[1] - yr[0])
        if equal:
            sx = sy = min(sx, sy)
        self.sx, self.sy = sx, sy
        self.ox = (x0 + x1) / 2 - sx * (xr[0] + xr[1]) / 2
        self.oy = (y0 + y1) / 2 - sy * (yr[0] + yr[1]) / 2

    def p(self, x, y):
        return self.ox + self.sx * x, self.oy + self.sy * y

    def box(self):
        a = self.p(self.xr[0], self.yr[0])
        b = self.p(self.xr[1], self.yr[1])
        return a[0], a[1], b[0] - a[0], b[1] - a[1]


def _frame_bg(s, F, grid=True, axes=True, ticks=False, tick_size=14, xt=None, yt=None):
    x, y, w, h = F.box()
    s.rect(x, y, w, h, fill=PAPER, edge=HAIR, lw=1.2, z=1)
    if grid:
        for gx in range(int(math.ceil(F.xr[0])), int(math.floor(F.xr[1])) + 1):
            a, b = F.p(gx, F.yr[0]), F.p(gx, F.yr[1])
            s.line(a[0], a[1], b[0], b[1], color='#E6E6E6', lw=0.8, z=1)
        for gy in range(int(math.ceil(F.yr[0])), int(math.floor(F.yr[1])) + 1):
            a, b = F.p(F.xr[0], gy), F.p(F.xr[1], gy)
            s.line(a[0], a[1], b[0], b[1], color='#E6E6E6', lw=0.8, z=1)
    if axes:
        a, b = F.p(F.xr[0], 0), F.p(F.xr[1], 0)
        s.line(a[0], a[1], b[0], b[1], color=GREY, lw=1.4, z=1)
        a, b = F.p(0, F.yr[0]), F.p(0, F.yr[1])
        s.line(a[0], a[1], b[0], b[1], color=GREY, lw=1.4, z=1)
    if ticks:
        for gx in (xt or []):
            a = F.p(gx, 0)
            s.text(a[0], a[1] - 0.2, f'{gx:g}'.replace('-', '−'), size=tick_size, color=MUTE)
        for gy in (yt or []):
            a = F.p(0, gy)
            s.text(a[0] - 0.18, a[1], f'{gy:g}'.replace('-', '−'), size=tick_size, color=MUTE, ha='right')


def _clip_line(a, b, c, xr, yr):
    """Endpoints of the line a x + b y = c inside the rectangle."""
    pts = []
    if abs(b) > 1e-12:
        for x in xr:
            y = (c - a * x) / b
            if yr[0] - 1e-9 <= y <= yr[1] + 1e-9:
                pts.append((x, y))
    if abs(a) > 1e-12:
        for y in yr:
            x = (c - b * y) / a
            if xr[0] - 1e-9 <= x <= xr[1] + 1e-9:
                pts.append((x, y))
    uniq = []
    for p in pts:
        if all(abs(p[0] - q[0]) + abs(p[1] - q[1]) > 1e-6 for q in uniq):
            uniq.append(p)
    return uniq[:2]


def _shade(v, lo=0.0, hi=9.0):
    t = min(1.0, max(0.0, (v - lo) / (hi - lo)))
    g = int(round(255 * (1 - 0.94 * t)))
    return f'#{g:02x}{g:02x}{g:02x}'


def _fmt(v, nd=2):
    t = f'{v:.{nd}f}'.rstrip('0').rstrip('.')
    return '0' if t in ('-0', '') else t


# =====================================================================================================
# Session 4 figures
# =====================================================================================================
@fig('x_sysrows')
def x_sysrows(w, h, panels=(), size=16, **_):
    """panels: [{title, lines:[{abc:(a,b,c), label, at:(x,y), color}], pt:(x,y), pt_label, caption, range:((x0,x1),(y0,y1)), ticks}]"""
    s = Scene(w, h)
    n = len(panels)
    gap = 0.3
    pw = (w - 0.1 - gap * (n - 1)) / n
    cap_h = 0.95 if any(p.get('caption') for p in panels) else 0.1
    for i, p in enumerate(panels):
        x0 = 0.05 + i * (pw + gap)
        top = h - 0.1
        if p.get('title'):
            s.text(x0 + pw / 2, h - 0.3, p['title'], size=18, weight='bold')
            top = h - 0.65
        xr, yr = p.get('range', ((-1, 5), (-1, 5)))
        F = Frame(x0 + 0.05, cap_h + 0.1, x0 + pw - 0.05, top, xr, yr)
        _frame_bg(s, F, ticks=p.get('ticks', False), xt=p.get('xt'), yt=p.get('yt'))
        for ln in p['lines']:
            a, b, c = ln['abc']
            ends = _clip_line(a, b, c, xr, yr)
            if len(ends) == 2:
                (xa, ya), (xb, yb) = F.p(*ends[0]), F.p(*ends[1])
                s.line(xa, ya, xb, yb, color=ln.get('color', INK), lw=3.0, z=3)
            if ln.get('label'):
                lx, ly = F.p(*ln['at'])
                s.text(lx, ly, ln['label'], size=size, weight='bold', color=ln.get('color', INK), ha=ln.get('ha', 'left'), z=7)
        if p.get('pt'):
            cx, cy = F.p(*p['pt'])
            s.circle(cx, cy, 0.11, fill=GOLD, edge=INK, lw=2, z=6)
            if p.get('pt_label'):
                s.text(cx + p.get('pt_dx', -0.2), cy + p.get('pt_dy', 0.3), p['pt_label'], size=size, weight='bold', ha=p.get('pt_ha', 'right'), z=7)
        if p.get('caption'):
            s.text(x0 + pw / 2, 0.1 + cap_h / 2, p['caption'], size=size, color=BODY)
    return s


@fig('x_colpic')
def x_colpic(w, h, cols=((2, 1), (1, -1)), coef=(2, 1), size=17, **_):
    s = Scene(w, h)
    (c1x, c1y), (c2x, c2y) = cols
    k1, k2 = coef
    bx, by = k1 * c1x + k2 * c2x, k1 * c1y + k2 * c2y
    xr, yr = (-0.8, 6.2), (-2.0, 3.2)
    F = Frame(0.1, 0.1, w - 0.1, h - 0.1, xr, yr)
    _frame_bg(s, F, ticks=True, xt=[1, 2, 3, 4, 5, 6], yt=[-1, 1, 2, 3], tick_size=14)
    o = F.p(0, 0)
    p1 = F.p(k1 * c1x, k1 * c1y)
    p2 = F.p(bx, by)
    s.arrow(o[0], o[1], p1[0], p1[1], color=INK, lw=3.4, head=22, z=5)
    s.arrow(p1[0], p1[1], p2[0], p2[1], color=RED, lw=3.4, head=22, z=5)
    s.arrow(o[0], o[1], p2[0], p2[1], color=INK, lw=2.4, head=18, dash=True, z=4)
    s.circle(p2[0], p2[1], 0.1, fill=GOLD, edge=INK, lw=2, z=6)
    s.text((o[0] + p1[0]) / 2 - 0.3, (o[1] + p1[1]) / 2 + 0.55, f'{k1:g} × column 1\n= ({k1 * c1x:g}, {k1 * c1y:g})', size=size, weight='bold', ha='right')
    s.text((p1[0] + p2[0]) / 2 + 0.3, (p1[1] + p2[1]) / 2 + 0.35, f'{k2:g} × column 2\n= ({k2 * c2x:g}, {k2 * c2y:g})'.replace('-', '−'), size=size, weight='bold', color=RED, ha='left')
    s.text(p2[0] + 0.2, p2[1] - 0.45, f'b = ({bx:g}, {by:g})', size=size, weight='bold', ha='left')
    return s


def _wrap_chars(text, n):
    words, out, cur = text.split(), [], ''
    for w_ in words:
        if cur and len(cur) + 1 + len(w_) > n:
            out.append(cur)
            cur = w_
        else:
            cur = (cur + ' ' + w_).strip()
    if cur:
        out.append(cur)
    return out


@fig('x_elim')
def x_elim(w, h, stages=(), size=24, **_):
    """stages: [{title, rows:[[str,...]], op}] ; the last column of each matrix is the right-hand side."""
    s = Scene(w, h)
    n = len(stages)
    cw, rh = 0.85, 0.62
    mw = 3 * cw
    gap = (w - 0.2 - n * mw) / max(1, n - 1)
    gap = min(gap, 1.6)
    total = n * mw + (n - 1) * gap
    x0 = (w - total) / 2
    ytop = h - 1.15
    for i, st in enumerate(stages):
        mx = x0 + i * (mw + gap)
        rows = st['rows']
        s.text(mx + mw / 2, h - 0.35, st['title'], size=18, weight='bold')
        mh = rh * len(rows)
        # brackets
        for sgn, bxx in ((1, mx - 0.1), (-1, mx + mw + 0.1)):
            s.line(bxx, ytop + 0.05, bxx, ytop - mh + 0.1, color=INK, lw=2.2)
            s.line(bxx, ytop + 0.05, bxx + sgn * 0.12, ytop + 0.05, color=INK, lw=2.2)
            s.line(bxx, ytop - mh + 0.1, bxx + sgn * 0.12, ytop - mh + 0.1, color=INK, lw=2.2)
        # bar before the last column
        s.line(mx + 2 * cw, ytop + 0.0, mx + 2 * cw, ytop - mh + 0.15, color=GREY, lw=1.6, dash=True)
        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                s.text(mx + cw * (c + 0.5), ytop - rh * (r + 0.5) + 0.12, v, size=size, weight='bold' if (st.get('hl') == r) else 'normal',
                       color=RED if (st.get('hl') == r) else INK)
        if st.get('op'):
            lines = _wrap_chars(st['op'], 24)
            for li, ln in enumerate(lines):
                s.text(mx + mw / 2, ytop - mh - 0.35 - li * 0.3, ln, size=16, color=MUTE)
        if i < n - 1:
            ax = mx + mw + 0.35
            s.arrow(ax, ytop - mh / 2 + 0.1, ax + gap - 0.7, ytop - mh / 2 + 0.1, lw=2.6, head=20)
    return s


@fig('x_unitsq')
def x_unitsq(w, h, A=((2, 1), (1, -1)), area='3', note_before='Unit square: area 1', note_after='', size=17, **_):
    s = Scene(w, h)
    M = np.array(A, float)
    c1, c2 = M[:, 0], M[:, 1]
    pts = [(0, 0), tuple(c1), tuple(c1 + c2), tuple(c2)]
    allx = [0, 1] + [p[0] for p in pts]
    ally = [0, 1] + [p[1] for p in pts]
    xr = (min(allx) - 0.6, max(allx) + 0.6)
    yr = (min(ally) - 0.6, max(ally) + 0.6)
    pw = (w - 0.4) / 2
    for i in range(2):
        x0 = 0.05 + i * (pw + 0.3)
        F = Frame(x0, 0.75, x0 + pw, h - 0.1, xr, yr)
        _frame_bg(s, F)
        o = F.p(0, 0)
        if i == 0:
            q = [F.p(0, 0), F.p(1, 0), F.p(1, 1), F.p(0, 1)]
            s.ax.add_patch(Polygon(q, closed=True, fc=PALE, ec=INK, lw=2, zorder=3))
            e1, e2 = F.p(1, 0), F.p(0, 1)
            s.arrow(o[0], o[1], e1[0], e1[1], color=INK, lw=3, head=18, z=5)
            s.arrow(o[0], o[1], e2[0], e2[1], color=RED, lw=3, head=18, z=5)
            s.text(F.p(0.5, 0.5)[0], F.p(0.5, 0.5)[1], '1', size=20, weight='bold')
            s.text(pw / 2 + x0, 0.4, note_before, size=size, color=BODY)
        else:
            q = [F.p(*p) for p in pts]
            s.ax.add_patch(Polygon(q, closed=True, fc=GOLD_SOFT, ec=INK, lw=2, zorder=3))
            a1, a2 = F.p(*c1), F.p(*c2)
            s.arrow(o[0], o[1], a1[0], a1[1], color=INK, lw=3, head=18, z=5)
            s.arrow(o[0], o[1], a2[0], a2[1], color=RED, lw=3, head=18, z=5)
            cen = F.p(*((c1 + c2) / 2))
            s.text(cen[0], cen[1], area, size=20, weight='bold', z=7)
            s.text(pw / 2 + x0, 0.4, note_after, size=size, color=BODY)
    return s


@fig('x_designmat')
def x_designmat(w, h, xs=(), ys=(), size=18, xname='spend', yname='sales', **_):
    s = Scene(w, h)
    n = len(xs)
    top = h - 0.95
    rh = min(0.46, (top - 0.1) / n)
    colw = 0.95
    blocks = [('X', [('1', 0), (xname, 1)]), ('w', None), ('y', None)]
    x = 0.15
    # X matrix
    s.text(x, h - 0.3, 'X: one row per point', size=16, weight='bold', color=INK, ha='left')
    s.text(x + colw / 2, h - 0.75, 'ones', size=15, color=MUTE)
    s.text(x + colw * 1.5, h - 0.75, xname, size=15, color=MUTE)
    for r in range(n):
        yy = top - rh * (r + 0.5)
        s.text(x + colw / 2, yy, '1', size=size)
        s.text(x + colw * 1.5, yy, _fmt(xs[r]), size=size)
    s.line(x - 0.05, top, x - 0.05, top - rh * n, color=INK, lw=2.2)
    s.line(x + 2 * colw + 0.05, top, x + 2 * colw + 0.05, top - rh * n, color=INK, lw=2.2)
    # times w
    xm = x + 2 * colw + 0.55
    s.text(xm, top - rh * n / 2, '×', size=26)
    wx = xm + 0.75
    s.text(wx + 0.1, h - 0.3, 'w: the two\nunknowns', size=16, weight='bold', ha='center')
    s.text(wx + 0.1, top - rh * n / 2 + 0.4, '$w_0$', size=24)
    s.text(wx + 0.1, top - rh * n / 2 - 0.4, '$w_1$', size=24)
    s.line(wx - 0.4, top - rh * n / 2 + 0.85, wx - 0.4, top - rh * n / 2 - 0.85, color=INK, lw=2.2)
    s.line(wx + 0.6, top - rh * n / 2 + 0.85, wx + 0.6, top - rh * n / 2 - 0.85, color=INK, lw=2.2)
    # approx y
    am = wx + 1.35
    s.text(am, top - rh * n / 2, '$\\approx$', size=30)
    yx = am + 1.0
    s.text(yx, h - 0.3, 'y: ' + yname, size=16, weight='bold')
    for r in range(n):
        s.text(yx, top - rh * (r + 0.5), _fmt(ys[r]), size=size)
    s.line(yx - 0.45, top, yx - 0.45, top - rh * n, color=INK, lw=2.2)
    s.line(yx + 0.45, top, yx + 0.45, top - rh * n, color=INK, lw=2.2)
    return s


@fig('x_fitline')
def x_fitline(w, h, points=(), line=(0, 1), xlabel='', ylabel='', size=16, **_):
    """Top: scatter with the fitted line (red) and each error as a short gold segment. Bottom: the same errors on a larger scale as gold bars around a zero line, with their signed values."""
    s = Scene(w, h)
    x0, x1 = 1.05, w - 0.35
    y0, y1 = 2.55, h - 0.3
    lo_x, hi_x, lo_y, hi_y = 0.0, 9.0, 0.0, 60.0
    px = lambda v: x0 + (v - lo_x) / (hi_x - lo_x) * (x1 - x0)
    py = lambda v: y0 + (v - lo_y) / (hi_y - lo_y) * (y1 - y0)
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    s.text(0.3, (y0 + y1) / 2, ylabel, size=size, color=MUTE, rot=90)
    for v in (0, 2, 4, 6, 8):
        s.text(px(v), y0 - 0.2, f'{v}', size=14, color=GREY)
    for v in (0, 20, 40, 60):
        s.text(x0 - 0.12, py(v), f'{v}', size=14, color=GREY, ha='right')
    b, m = line
    s.ax.plot([px(0.4), px(8.6)], [py(b + m * 0.4), py(b + m * 8.6)], color=RED, lw=3.2, zorder=3)
    for (xv, yv) in points:
        pred = b + m * xv
        s.ax.plot([px(xv), px(xv)], [py(yv), py(pred)], color=INK, lw=7.5, zorder=4, solid_capstyle='butt')
        s.ax.plot([px(xv), px(xv)], [py(yv), py(pred)], color=GOLD, lw=4.5, zorder=5, solid_capstyle='butt')
        s.circle(px(xv), py(yv), 0.09, fill=INK, edge=INK, lw=1, z=6)
    # errors on a larger scale
    zero = 1.05
    unit = 0.22   # inches per UGX million of error
    s.line(x0, zero, x1, zero, color=GREY, lw=1.4)
    s.text(x0 - 0.12, zero, '0', size=14, color=GREY, ha='right')
    s.text((x0 + x1) / 2, 2.1, xlabel, size=size, color=MUTE)
    s.text((x0 + x1) / 2, 0.22, 'The same errors on a larger scale (UGX million)', size=size, color=MUTE)
    for (xv, yv) in points:
        e = yv - (b + m * xv)
        top = zero + e * unit
        s.rect(px(xv) - 0.12, min(zero, top), 0.24, abs(top - zero), fill=GOLD, edge=INK, lw=1.2, z=4)
        s.text(px(xv), top + (0.2 if e >= 0 else -0.2), f'{e:+.1f}'.replace('-', '−'), size=14, color=INK, weight='bold')
    return s


@fig('x_manyfits')
def x_manyfits(w, h, pt=(4, 30), slopes=(1, 3, 5.4, 8, -2), xr=(0, 8), yr=(0, 60), xlabel='advertising spend', ylabel='sales', size=16, **_):
    s = Scene(w, h)
    F = Frame(0.9, 0.75, w - 0.3, h - 0.3, xr, yr, equal=False)
    _frame_bg(s, F, grid=False)
    s.text((F.cx0 + F.cx1) / 2, 0.3, xlabel, size=size, color=MUTE)
    s.text(0.3, (F.cy0 + F.cy1) / 2, ylabel, size=size, color=MUTE, rot=90)
    for m in slopes:
        b = pt[1] - m * pt[0]
        ends = _clip_line(-m, 1, b, xr, yr)
        if len(ends) == 2:
            a, c = F.p(*ends[0]), F.p(*ends[1])
            s.line(a[0], a[1], c[0], c[1], color=RED, lw=2.6, z=3)
    c = F.p(*pt)
    s.circle(c[0], c[1], 0.13, fill=GOLD, edge=INK, lw=2, z=6)
    s.text(c[0], c[1] + 0.45, 'the one data point', size=size, weight='bold', ha='center', z=7)
    return s


# =====================================================================================================
# Session 5 figures
# =====================================================================================================
def _ellipse_pts(M, n=100):
    t = np.linspace(0, 2 * np.pi, n)
    return M @ np.vstack([np.cos(t), np.sin(t)])


@fig('x_eigpic')
def x_eigpic(w, h, A=((2, 1), (1, 2)), size=16, **_):
    s = Scene(w, h)
    M = np.array(A, float)
    ev, V = np.linalg.eigh(M)
    ev, V = ev[::-1], V[:, ::-1]
    if V[0, 0] < 0:
        V[:, 0] = -V[:, 0]
    if V[0, 1] < 0:
        V[:, 1] = -V[:, 1]
    R = 3.0
    pw = (w - 0.3) / 2
    ttl = ['Before: the unit circle', 'After the matrix: an ellipse']
    for i in range(2):
        x0 = 0.05 + i * (pw + 0.2)
        F = Frame(x0, 0.2, x0 + pw, h - 0.65, (-R, R), (-R, R))
        s.text(x0 + pw / 2, h - 0.33, ttl[i], size=18, weight='bold')
        _frame_bg(s, F, grid=True)
        o = F.p(0, 0)
        for k, col in ((0, RED), (1, INK)):
            v = V[:, k]
            a, b = F.p(*(-R * v)), F.p(*(R * v))
            s.line(a[0], a[1], b[0], b[1], color=col, lw=1.6, dash=True, z=2)
        T = np.eye(2) if i == 0 else M
        pts = _ellipse_pts(T)
        q = [F.p(px, py) for px, py in pts.T]
        s.ax.add_patch(Polygon(q, closed=True, fc=GOLD_SOFT if i else PALE, ec=INK, lw=2, zorder=3))
        u = np.array([1.0, 0.0])
        for vec, col, lab, off in ((u, GREY, 'v', (0.12, -0.3)), (V[:, 0], RED, 'e₁', (-0.1, 0.25)), (V[:, 1], INK, 'e₂', (0.25, -0.2))):
            tip = T @ vec
            p = F.p(*tip)
            s.arrow(o[0], o[1], p[0], p[1], color=col, lw=3.2, head=20, z=5)
        halo = dict(boxstyle='square,pad=0.12', fc='white', ec='none')
        if i == 0:
            s.text(*F.p(1.5, 0.3), 'v', size=size, weight='bold', color=GREY, z=7, bbox=halo)
            s.text(*F.p(0.2, 1.25), 'e₁', size=size, weight='bold', color=RED, z=7, bbox=halo)
            s.text(*F.p(0.35, -1.3), 'e₂', size=size, weight='bold', color=INK, z=7, bbox=halo)
        else:
            s.text(*F.p(2.15, 0.35), 'v turned', size=size, weight='bold', color=GREY, z=7, bbox=halo)
            s.text(*F.p(0.9, 2.55), f'e₁ × {ev[0]:g}', size=size, weight='bold', color=RED, z=7, bbox=halo)
            s.text(*F.p(0.5, -1.55), f'e₂ × {ev[1]:g}', size=size, weight='bold', color=INK, z=7, bbox=halo)
    return s


@fig('x_lambdas')
def x_lambdas(w, h, items=((2, 'doubled'), (0.5, 'halved'), (1, 'unchanged'), (-1, 'flipped'), (0, 'squashed to zero')), size=16, **_):
    s = Scene(w, h)
    n = len(items)
    pw = (w - 0.1) / n
    for i, (lam, word) in enumerate(items):
        cx = 0.05 + i * pw + pw / 2
        sc = pw * 0.30
        yb = h * 0.58
        s.line(cx - pw * 0.46, yb, cx + pw * 0.46, yb, color=HAIR, lw=1.4, z=1)
        s.circle(cx, yb, 0.05, fill=INK, edge=INK, lw=1, z=4)
        s.arrow(cx, yb + 0.28, cx + sc, yb + 0.28, color=GREY, lw=3.2, head=18, z=4)
        if abs(lam) > 1e-9:
            s.arrow(cx, yb - 0.28, cx + lam * sc, yb - 0.28, color=RED, lw=3.2, head=18, z=4)
        else:
            s.circle(cx, yb - 0.28, 0.07, fill=RED, edge=RED, lw=1, z=4)
        s.text(cx, h - 0.4, f'$\\lambda$ = {lam:g}'.replace('-', '−'), size=20, weight='bold')
        s.text(cx, 0.55, word, size=size, color=BODY)
    s.text(0.1, yb + 0.28, 'in', size=14, color=GREY, ha='left') if False else None
    return s


@fig('x_cloud')
def x_cloud(w, h, points=(), axes=(), project=None, xlabel='', ylabel='', size=16, rng=None, arrows=True, annotate_first=False, **_):
    """points: centred (x, y) pairs. axes: [{v:(vx,vy), len:L, label, color}] drawn from the origin both ways; project: index of the axis to drop points onto."""
    s = Scene(w, h)
    P = np.array(points, float)
    r = rng or float(np.max(np.abs(P))) * 1.15
    F = Frame(0.1, 0.65, w - 0.1, h - 0.1, (-r, r), (-r * 0.75, r * 0.75))
    _frame_bg(s, F, grid=False)
    s.text((F.cx0 + F.cx1) / 2, 0.3, xlabel, size=size, color=MUTE)
    for k, ax_ in enumerate(axes):
        v = np.array(ax_['v'], float)
        v = v / np.linalg.norm(v)
        L = ax_['len']
        a, b = F.p(*(-L * v)), F.p(*(L * v))
        col = ax_.get('color', RED)
        s.arrow(a[0], a[1], b[0], b[1], color=col, lw=3.0, head=20, z=4)
        if ax_.get('label'):
            lx, ly = F.p(*(L * v * ax_.get('at', 0.8)))
            lx = min(lx, F.cx1 - 1.9 if ax_.get('ha', 'left') == 'left' else F.cx1)
            ly = min(max(ly, F.cy0 + 0.3), F.cy1 - 0.5)
            s.text(lx + ax_.get('dx', 0.1), ly + ax_.get('dy', 0.3), ax_['label'], size=size, weight='bold', color=col, ha=ax_.get('ha', 'left'), z=7)
    if project is not None:
        v = np.array(axes[project]['v'], float)
        v = v / np.linalg.norm(v)
        for (px, py) in P:
            t = px * v[0] + py * v[1]
            q = F.p(t * v[0], t * v[1])
            a = F.p(px, py)
            s.line(a[0], a[1], q[0], q[1], color=INK, lw=2.6, dash=True, z=3)
            s.circle(q[0], q[1], 0.09, fill=RED, edge=RED, lw=1, z=5)
    for (px, py) in P:
        a = F.p(px, py)
        s.circle(a[0], a[1], 0.085, fill=INK, edge=INK, lw=1, z=6)
    if annotate_first and project is not None:
        v = np.array(axes[project]['v'], float)
        v = v / np.linalg.norm(v)
        px, py = P[0]
        t0 = px * v[0] + py * v[1]
        q = F.p(t0 * v[0], t0 * v[1])
        a = F.p(px, py)
        s.text(a[0] - 0.22, a[1] + 0.05, 'student 1 (−7, −5)', size=15, weight='bold', ha='right', z=8)
        s.text(q[0] + 0.15, q[1] - 0.38, f'score {t0:.1f}'.replace('-', '−'), size=15, weight='bold', color=RED, ha='left', z=8)
    return s


@fig('x_centre')
def x_centre(w, h, raw=(), mean=(0, 0), xlabel='Maths mark', ylabel='Physics mark', size=16, **_):
    s = Scene(w, h)
    P = np.array(raw, float)
    C = P - np.array(mean)
    pw = (w - 1.2) / 2
    xr = (P[:, 0].min() - 4, P[:, 0].max() + 4)
    yr = (P[:, 1].min() - 4, P[:, 1].max() + 4)
    F1 = Frame(0.1, 0.7, 0.1 + pw, h - 0.65, xr, yr, equal=True)
    rr = max(abs(C).max() + 4, 12)
    F2 = Frame(0.1 + pw + 1.0, 0.7, w - 0.1, h - 0.65, (-rr, rr), (-rr, rr), equal=True)
    s.text(0.1 + pw / 2, h - 0.33, 'Raw marks', size=18, weight='bold')
    s.text(0.1 + pw + 1.0 + pw / 2, h - 0.33, 'Centred: mean subtracted', size=18, weight='bold')
    s.arrow(0.1 + pw + 0.2, h / 2, 0.1 + pw + 0.8, h / 2, lw=2.6, head=20)
    for F, pts, mark, lab in ((F1, P, np.array(mean), 'mean'), (F2, C, np.zeros(2), 'origin')):
        _frame_bg(s, F, grid=False, axes=(F is F2))
        for (px, py) in pts:
            a = F.p(px, py)
            s.circle(a[0], a[1], 0.085, fill=INK, edge=INK, lw=1, z=6)
        m = F.p(*mark)
        s.line(m[0] - 0.2, m[1], m[0] + 0.2, m[1], color=RED, lw=3, z=7)
        s.line(m[0], m[1] - 0.2, m[0], m[1] + 0.2, color=RED, lw=3, z=7)
    m = F1.p(*mean)
    s.text(m[0] + 0.25, m[1] - 0.35, f'mean ({_fmt(mean[0])}, {_fmt(mean[1])})', size=15, weight='bold', color=RED, ha='left', z=8)
    s.text(0.1 + pw / 2, 0.3, xlabel + ' (across), ' + ylabel + ' (up)', size=15, color=MUTE)
    s.text(0.1 + pw + 1.0 + pw / 2, 0.3, 'The mean is now at (0, 0)', size=15, color=MUTE)
    return s


@fig('x_power')
def x_power(w, h, A=((2, 1), (1, 2)), v0=(1, 0), nsteps=4, size=16, **_):
    s = Scene(w, h)
    M = np.array(A, float)
    ev, V = np.linalg.eigh(M)
    top = V[:, -1] if V[0, -1] > 0 else -V[:, -1]
    F = Frame(0.15, 0.15, w - 0.15, h - 0.15, (-0.3, 4.0), (-0.3, 3.6))
    _frame_bg(s, F, grid=True)
    o = F.p(0, 0)
    a, b = F.p(*(-0.2 * top)), F.p(*(3.4 * top))
    s.line(a[0], a[1], b[0], b[1], color=RED, lw=1.8, dash=True, z=2)
    v = np.array(v0, float)
    shades = [GREY, '#555555', BODY, INK, INK]
    for k in range(nsteps + 1):
        m = np.max(np.abs(v))
        t = F.p(*(v / m * 3.0 if k else v * 2.8))
        s.arrow(o[0], o[1], t[0], t[1], color=RED if k == nsteps else shades[min(k, 3)], lw=3.0, head=18, z=5)
        angle = math.degrees(math.atan2(v[1], v[0]))
        lab = 'g' + '₀₁₂₃₄₅₆₇₈₉'[k]
        off = {0: (0.0, -0.32), 1: (0.45, 0.0), 2: (0.45, -0.05)}.get(k, (0.0, 0.4))
        if k <= 2 or k == nsteps:
            s.text(t[0] + off[0], t[1] + off[1], lab, size=size, weight='bold', color=RED if k == nsteps else INK, z=7)
        v = M @ v
        v = v / np.max(np.abs(v))
    return s


@fig('x_embedmap')
def x_embedmap(w, h, size=16, **_):
    """Invented 4-number word vectors (rows of the little table) and their picture after PCA keeps two directions."""
    s = Scene(w, h)
    words = ['cat', 'dog', 'lion', 'car', 'bus', 'train', 'rice', 'bread', 'maize']
    rng = np.random.default_rng(SEED_EMB)
    centres = {0: np.array([0.9, 0.8, 0.1, 0.2]), 1: np.array([0.1, 0.2, 0.9, 0.7]), 2: np.array([0.5, -0.3, 0.2, -0.8])}
    E = np.array([centres[i // 3] + rng.normal(0, 0.3, 4) for i in range(9)])
    Ec = E - E.mean(0)
    U, S, Vt = np.linalg.svd(Ec, full_matrices=False)
    Z = Ec @ Vt[:2].T
    lw_ = 4.2
    s.text(lw_ / 2 + 0.1, h - 0.3, 'Each word is a list of numbers', size=17, weight='bold')
    s.text(lw_ / 2 + 0.1, h - 0.65, '(illustrative: 4 numbers, made up)', size=15, color=MUTE)
    for r, wd in enumerate(['cat', 'car', 'rice']):
        i = words.index(wd)
        y = h - 1.3 - r * 0.55
        s.text(0.15, y, wd, size=17, weight='bold', ha='left')
        for c in range(4):
            s.text(1.15 + c * 0.75, y, f'{E[i, c]:.2f}'.replace('-', '−'), size=16, ha='left')
    s.text(0.15, h - 3.05, 'PCA keeps the two\ndirections with the\nmost spread', size=16, color=RED, weight='bold', ha='left')
    s.arrow(lw_ + 0.2, h / 2 - 0.3, lw_ + 0.9, h / 2 - 0.3, lw=2.6, head=20)
    F = Frame(lw_ + 1.1, 0.45, w - 0.1, h - 0.1, (Z[:, 0].min() - 0.3, Z[:, 0].max() + 0.5), (Z[:, 1].min() - 0.3, Z[:, 1].max() + 0.3), equal=False)
    _frame_bg(s, F, grid=False, axes=False)
    s.text((F.cx0 + F.cx1) / 2, 0.2, 'principal component 1 (across) and 2 (up)', size=15, color=MUTE)
    cols = [INK, RED, GREY]
    for i, wd in enumerate(words):
        a = F.p(Z[i, 0], Z[i, 1])
        s.circle(a[0], a[1], 0.09, fill=cols[i // 3], edge=cols[i // 3], lw=1, z=5)
        mode = i % 3
        if mode == 0:
            s.text(a[0] + 0.14, a[1] + 0.05, wd, size=15, ha='left', z=7)
        elif mode == 1:
            s.text(a[0] - 0.14, a[1] + 0.05, wd, size=15, ha='right', z=7)
        else:
            s.text(a[0], a[1] - 0.3, wd, size=15, ha='center', z=7)
    return s


# =====================================================================================================
# Session 6 figures
# =====================================================================================================
def _R(deg):
    t = math.radians(deg)
    return np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])


@fig('x_svdpic')
def x_svdpic(w, h, size=16, **_):
    s = Scene(w, h)
    d = d6()
    Vt, S, U = d['Vt'], d['S'], d['U']
    # use proper rotations: make det +1 by flipping the second pair of vectors if needed
    V = Vt.T.copy()
    Uu = U.copy()
    if np.linalg.det(V) < 0:
        V[:, 1] = -V[:, 1]
        Uu[:, 1] = -Uu[:, 1]
    if np.linalg.det(Uu) < 0:       # both flips undone: fall back to showing a flip
        pass
    if V[0, 0] < 0:
        V[:, 0] = -V[:, 0]
        Uu[:, 0] = -Uu[:, 0]
        V[:, 1] = -V[:, 1]
        Uu[:, 1] = -Uu[:, 1]
    T = [np.eye(2), V.T, np.diag(S) @ V.T, Uu @ np.diag(S) @ V.T]
    ttl = ['1  A circle', '2  Rotate  ($V^T$)', '3  Stretch  ($\\Sigma$)', '4  Rotate  ($U$)']
    cap = ['red arrow v₁, black\narrow v₂ (zoomed in)', 'v₁ now lies along\nthe across axis', f'across × {S[0]:.0f},\nup × {S[1]:.0f}', 'This is A applied\nto the circle']
    n = 4
    gap = 0.22
    pw = (w - 0.1 - gap * (n - 1)) / n
    Rs = [1.75, 1.75, 3.25, 3.25]
    for i in range(n):
        R = Rs[i]
        x0 = 0.05 + i * (pw + gap)
        F = Frame(x0, 1.35, x0 + pw, h - 0.65, (-R, R), (-R, R))
        s.text(x0 + pw / 2, h - 0.33, ttl[i], size=18, weight='bold')
        _frame_bg(s, F, grid=True)
        pts = T[i] @ np.vstack([np.cos(np.linspace(0, 2 * np.pi, 100)), np.sin(np.linspace(0, 2 * np.pi, 100))])
        q = [F.p(px, py) for px, py in pts.T]
        s.ax.add_patch(Polygon(q, closed=True, fc=GOLD_SOFT if i == 3 else PALE, ec=INK, lw=2, zorder=3))
        o = F.p(0, 0)
        for k, col in ((0, RED), (1, INK)):
            vec = T[i] @ V[:, k]
            t = F.p(*vec)
            s.arrow(o[0], o[1], t[0], t[1], color=col, lw=3.2, head=18, z=5)
        s.text(x0 + pw / 2, 0.88, cap[i], size=15, color=BODY)
    s.text(w / 2, 0.3, 'v₁ and v₂ are the right singular vectors: the two directions that A turns onto the axes.', size=15, color=MUTE)
    return s


@fig('x_imgs')
def x_imgs(w, h, items=(), size=16, numbers=False, **_):
    """items: [{title, sub, m}] with m an 8 by 8 list of numbers 0..9 (0 white, 9 black)."""
    s = Scene(w, h)
    n = len(items)
    gap = 0.3
    pw = (w - 0.1 - gap * (n - 1)) / n
    cell = min(pw / 8, (h - 1.5) / 8)
    for i, it in enumerate(items):
        x0 = 0.05 + i * (pw + gap) + (pw - 8 * cell) / 2
        ytop = h - 0.75
        s.text(0.05 + i * (pw + gap) + pw / 2, h - 0.3, it['title'], size=18, weight='bold')
        M = np.array(it['m'], float)
        for r in range(8):
            for c in range(8):
                s.rect(x0 + c * cell, ytop - (r + 1) * cell, cell, cell, fill=_shade(M[r, c]), edge='#DDDDDD', lw=0.4, z=2)
                if numbers:
                    s.text(x0 + (c + 0.5) * cell, ytop - (r + 0.5) * cell, f'{M[r, c]:.0f}', size=14, color='#FFFFFF' if M[r, c] >= 5 else INK, z=4)
        s.rect(x0, ytop - 8 * cell, 8 * cell, 8 * cell, fill='none', edge=INK, lw=2, z=3)
        if it.get('sub'):
            s.text(0.05 + i * (pw + gap) + pw / 2, ytop - 8 * cell - 0.32, it['sub'], size=size, color=BODY)
    return s


@fig('x_scree')
def x_scree(w, h, values=(), label='Singular value', size=16, cum=None, mark=None, **_):
    s = Scene(w, h)
    n = len(values)
    x0, x1 = 0.9, w - 0.2
    yb, yt = 1.5, h - 0.6
    mx = max(values)
    bw = (x1 - x0) / n
    s.line(x0, yb, x1, yb, color=INK, lw=2)
    s.text(0.1, (yb + yt) / 2, label, size=size, color=MUTE, rot=90, ha='center')
    for i, v in enumerate(values):
        bx = x0 + i * bw + bw * 0.15
        bh = (yt - yb - 0.35) * v / mx
        s.rect(bx, yb, bw * 0.7, bh, fill=GOLD if (mark is not None and i < mark) else PAPER, edge=INK, lw=2, z=3)
        s.text(bx + bw * 0.35, yb + bh + 0.22, f'{v:.1f}', size=15, weight='bold')
        s.text(bx + bw * 0.35, yb - 0.25, str(i + 1), size=15, color=MUTE)
    s.text(x1 - 1.2, yb - 0.55, 'component number', size=15, color=MUTE)
    if cum is not None:
        s.text(0.1, 0.62, 'Cumulative share of the total:', size=16, color=MUTE, ha='left')
        for i, c in enumerate(cum):
            s.text(x0 + i * bw + bw * 0.5, 0.25, f'{100 * c:.0f}%', size=16, weight='bold', color=RED if (mark is not None and i == mark - 1) else INK)
    return s


@fig('x_outer')
def x_outer(w, h, u=(), v=(), size=16, **_):
    s = Scene(w, h)
    u = np.array(u, float)
    v = np.array(v, float)
    M = np.outer(u, v)
    lo, hi = M.min(), M.max()
    cell = min(0.33, (h - 1.3) / 8)
    ytop = h - 0.8
    ymid = ytop - 4 * cell
    ux = 0.3
    nu = max(abs(u).max(), 1e-9)
    nv = max(abs(v).max(), 1e-9)
    s.text(ux + cell / 2, h - 0.3, 'column u', size=16, weight='bold')
    for r in range(8):
        s.rect(ux, ytop - (r + 1) * cell, cell, cell, fill=_shade(abs(u[r]) / nu * 9), edge='#DDDDDD', lw=0.4, z=2)
    s.rect(ux, ytop - 8 * cell, cell, 8 * cell, fill='none', edge=INK, lw=2, z=3)
    s.text(ux + cell + 0.35, ymid, '×', size=26)
    rx = ux + cell + 0.7
    s.text(rx + 4 * cell, h - 0.3, 'row v', size=16, weight='bold')
    for c in range(8):
        s.rect(rx + c * cell, ymid - cell / 2, cell, cell, fill=_shade(abs(v[c]) / nv * 9), edge='#DDDDDD', lw=0.4, z=2)
    s.rect(rx, ymid - cell / 2, 8 * cell, cell, fill='none', edge=INK, lw=2, z=3)
    s.text(rx + 8 * cell + 0.35, ymid, '=', size=30)
    px = rx + 8 * cell + 0.7
    s.text(px + 4 * cell, h - 0.3, 'u × v: 64 cells', size=16, weight='bold')
    for r in range(8):
        for c in range(8):
            tt = (M[r, c] - lo) / (hi - lo + 1e-12) * 9
            s.rect(px + c * cell, ytop - (r + 1) * cell, cell, cell, fill=_shade(tt), edge='#DDDDDD', lw=0.4, z=2)
    s.rect(px, ytop - 8 * cell, 8 * cell, 8 * cell, fill='none', edge=INK, lw=2, z=3)
    s.text(w / 2, 0.35, 'made from only 16 numbers (8 in u and 8 in v)', size=16, color=BODY)
    return s


@fig('x_lowrank')
def x_lowrank(w, h, m=8, n=8, k=2, size=16, **_):
    s = Scene(w, h)
    base = 0.12
    sc = min((h - 1.6) / m, 0.5)
    big = 8 * sc
    ytop = h - 0.9
    # A
    x = 0.2
    s.rect(x, ytop - big, big, big, fill=PALE, edge=INK, lw=2.2)
    s.text(x + big / 2, ytop - big / 2, f'A\n{m} × {n}', size=20, weight='bold')
    s.text(x + big / 2, h - 0.35, f'{m * n} numbers', size=16, color=MUTE)
    x += big + 0.35
    s.text(x, ytop - big / 2, '$\\approx$', size=30)
    x += 0.45
    kw = k * sc * 0.9
    s.rect(x, ytop - big, kw, big, fill=GOLD_SOFT, edge=INK, lw=2.2)
    s.text(x + kw / 2, ytop - big / 2, f'$U_k$\n{m} × {k}', size=16, weight='bold')
    x += kw + 0.2
    s.text(x, ytop - big / 2, '×', size=22)
    x += 0.35
    kk = k * sc * 0.9
    cw_ = kk / k
    for ii in range(k):
        for jj in range(k):
            s.rect(x + jj * cw_, ytop - big / 2 + kk / 2 - (ii + 1) * cw_, cw_, cw_, fill=GOLD if ii == jj else PALE, edge=INK, lw=1.2)
    s.text(x + kk / 2, ytop - big / 2 - kk / 2 - 0.55, f'$\\Sigma_k$ {k} × {k}\nonly the {k} gold\ndiagonal numbers\nare stored', size=15, weight='bold')
    x += kk + 0.2
    s.text(x, ytop - big / 2, '×', size=22)
    x += 0.35
    s.rect(x, ytop - kw - (big - kw) / 2 + (big - kw) / 2 - 0.0 - (big - big), big, kw, fill=GOLD_SOFT, edge=INK, lw=2.2) if False else None
    s.rect(x, ytop - big / 2 - kw / 2, big, kw, fill=GOLD_SOFT, edge=INK, lw=2.2)
    s.text(x + big / 2, ytop - big / 2, f'$V_k^T$   {k} × {n}', size=16, weight='bold')
    stored = k * (m + n + 1)
    s.text(x + big / 2, h - 0.35, f'{stored} numbers to keep', size=16, color=RED, weight='bold')
    return s


@fig('x_lora')
def x_lora(w, h, d=1000, r=8, size=16, **_):
    """Published LoRA picture (Hu et al. 2021): the pre-trained weight W is frozen; a trainable update B A of low rank r is added."""
    s = Scene(w, h)
    big = min(h - 2.0, 3.1)
    y0 = 0.95
    x = 0.2
    s.rect(x, y0, big, big, fill=PALE, edge=INK, lw=2.4)
    s.text(x + big / 2, y0 + big / 2 + 0.25, 'W', size=30, weight='bold')
    s.text(x + big / 2, y0 + big / 2 - 0.25, f'{d} × {d}', size=17)
    s.icon('lock', x + big / 2, y0 + 0.5, 0.65)
    s.text(x + big / 2, h - 0.35, 'Frozen (not trained)', size=17, weight='bold')
    x += big + 0.2
    s.text(x + 0.3, y0 + big / 2, '+', size=34)
    x += 0.7
    bw = 0.6
    s.rect(x, y0, bw, big, fill=GOLD, edge=INK, lw=2.4)
    s.text(x + bw / 2, y0 + big / 2, 'B', size=26, weight='bold')
    s.text(x + bw / 2, y0 - 0.32, f'{d} × {r}', size=16)
    s.text(x + bw / 2 + 0.9, h - 0.35, 'Trained', size=17, weight='bold', color=RED)
    x += bw + 0.25
    s.text(x, y0 + big / 2, '×', size=24)
    x += 0.35
    ah = 0.6
    s.rect(x, y0 + big / 2 - ah / 2, big, ah, fill=GOLD, edge=INK, lw=2.4)
    s.text(x + big / 2, y0 + big / 2, 'A', size=26, weight='bold')
    s.text(x + big / 2, y0 + big / 2 - ah / 2 - 0.32, f'{r} × {d}', size=16)
    full, small = d * d, 2 * d * r
    s.text(w - 0.15, 0.45, f'Full update of W: {full:,} numbers.   B and A together: {small:,} numbers.', size=16, ha='right', color=BODY)
    s.text(w - 0.15, h - 0.35, '(illustrative sizes: d = 1000, r = 8)', size=15, ha='right', color=MUTE)
    return s
