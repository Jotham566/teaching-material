"""Author D (sessions 10, 11, 12): diagram kinds and the numbers behind the slides, notebooks and workbooks.

Every kind is registered as x_d_<name>, so in a slide it is visual=dict(kind='d_<name>', ...).
Numbers: n10(), n11(), n12() compute everything with NumPy so slides, notebooks and workbooks share one source.
"""
import math
import numpy as np
from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD, fig
import slidekit as K


# =====================================================================  numbers
def _sig(z):
    return 1.0 / (1.0 + np.exp(-z))


def line_data():
    """Illustrative boda-boda fares: distance in km, fare in thousand UGX (made-up numbers)."""
    x = np.arange(1, 9, dtype=float)
    y = np.array([3.2, 4.1, 5.4, 5.9, 7.6, 8.0, 9.9, 10.3])
    return x, y


def gd_line(eta, steps=30, w=0.0, b=0.0):
    """Gradient descent on the centred line fit. Returns w, b, loss list (length steps+1) and the per-step table."""
    x, y = line_data()
    xc = x - x.mean()
    n = len(x)
    L, rows = [], []
    for t in range(steps + 1):
        e = w * xc + b - y
        loss = float((e ** 2).mean())
        dw, db = 2 / n * float((e * xc).sum()), 2 / n * float(e.sum())
        L.append(loss)
        rows.append((t, w, b, loss, dw, db))
        w, b = w - eta * dw, b - eta * db
    return w, b, L, rows


def bowl_path(eta, steps=5, w0=0.0):
    """Gradient descent on L(w) = (w - 3)^2, gradient 2 (w - 3)."""
    p = [w0]
    for _ in range(steps):
        p.append(p[-1] - eta * 2 * (p[-1] - 3))
    return p


def adam_steps(g_fn, w0=0.0, alpha=0.1, b1=0.9, b2=0.999, eps=1e-8, steps=3):
    w, m, v = w0, 0.0, 0.0
    rows = []
    for t in range(1, steps + 1):
        g = g_fn(w)
        m = b1 * m + (1 - b1) * g
        v = b2 * v + (1 - b2) * g * g
        mh, vh = m / (1 - b1 ** t), v / (1 - b2 ** t)
        step = alpha * mh / (math.sqrt(vh) + eps)
        rows.append(dict(t=t, w_before=w, g=g, m=m, v=v, mh=mh, vh=vh, sq=math.sqrt(vh), step=step, w_after=w - step))
        w = w - step
    return rows


def momentum_steps(gs, beta=0.9):
    v, out = 0.0, []
    for g in gs:
        v = beta * v + g
        out.append(v)
    return out


def n10():
    x, y = line_data()
    xc = x - x.mean()
    n = len(x)
    d = dict(x=x, y=y, xc=xc, n=n, mean_x=float(x.mean()))
    d['loss0'] = float((y ** 2).mean())
    d['dw0'] = -2 / n * float((xc * y).sum())
    d['db0'] = -2 / n * float(y.sum())
    d['sum_xy'] = float((xc * y).sum())
    d['sum_y'] = float(y.sum())
    d['sum_xc2'] = float((xc ** 2).sum())
    coef = np.polyfit(xc, y, 1)
    d['w_star'], d['b_star'] = float(coef[0]), float(coef[1])
    d['loss_star'] = float(((d['w_star'] * xc + d['b_star'] - y) ** 2).mean())
    d['runs'] = {}
    for eta in (0.01, 0.05, 0.1, 0.2):
        w, b, L, rows = gd_line(eta, 30)
        d['runs'][eta] = dict(w=w, b=b, L=L, rows=rows)
    d['eta_good'] = 0.1
    r = d['runs'][0.1]['rows']
    d['w1'], d['b1'] = r[1][1], r[1][2]
    d['bowl'] = {eta: bowl_path(eta, 5) for eta in (0.01, 0.1, 1.0, 1.1)}
    d['adam'] = adam_steps(lambda w: 2 * (w - 3), 0.0, 0.1, steps=3)
    d['sgd_steps'] = [0.0]
    for _ in range(3):
        d['sgd_steps'].append(d['sgd_steps'][-1] - 0.1 * 2 * (d['sgd_steps'][-1] - 3))
    d['mom'] = momentum_steps([2, 2, 2], 0.9)
    # the same line fit with three forms of the squared-error loss (Session 10 owns this comparison)
    sse0 = float((y ** 2).sum())
    d['forms'] = dict(mse=d['loss0'], half=0.5 * sse0, sse=sse0, dw_mse=d['dw0'], dw_half=-float((xc * y).sum()), dw_sse=-2 * float((xc * y).sum()),
                      eta_half=0.1 * 2 / n, eta_sse=0.1 / n)
    d['eta_max_w'] = float(1 / (xc ** 2).mean())                     # centred: w is stable below this learning rate
    Xu = np.c_[x, np.ones(n)]
    d['eta_max_uncentred'] = float(2 / np.linalg.eigvalsh(2 / n * Xu.T @ Xu).max())
    return d


def n11():
    W1 = np.array([[0.2, -0.3], [0.4, 0.1]])
    b1 = np.array([0.1, -0.2])
    W2 = np.array([[0.5, -0.4]])
    b2 = np.array([0.2])
    x = np.array([1.0, 2.0])
    y = 1.0
    eta = 0.5

    def forward(W1, b1, W2, b2):
        z1 = W1 @ x + b1
        a1 = _sig(z1)
        yh = float((W2 @ a1 + b2)[0])
        L = 0.5 * (yh - y) ** 2
        return z1, a1, yh, L

    def backward(W1, b1, W2, b2):
        z1, a1, yh, L = forward(W1, b1, W2, b2)
        d2 = yh - y                                  # dL/dyhat
        gW2 = d2 * a1[None, :]
        gb2 = np.array([d2])
        d1 = (W2[0] * d2) * a1 * (1 - a1)           # delta of hidden layer
        gW1 = np.outer(d1, x)
        gb1 = d1
        return dict(z1=z1, a1=a1, yh=yh, L=L, d2=d2, gW2=gW2, gb2=gb2, d1=d1, gW1=gW1, gb1=gb1)

    out = dict(W1=W1, b1=b1, W2=W2, b2=b2, x=x, y=y, eta=eta)
    s1 = backward(W1, b1, W2, b2)
    nW1, nb1, nW2, nb2 = W1 - eta * s1['gW1'], b1 - eta * s1['gb1'], W2 - eta * s1['gW2'], b2 - eta * s1['gb2']
    s2 = backward(nW1, nb1, nW2, nb2)
    nW1b, nb1b, nW2b, nb2b = nW1 - eta * s2['gW1'], nb1 - eta * s2['gb1'], nW2 - eta * s2['gW2'], nb2 - eta * s2['gb2']
    s3 = backward(nW1b, nb1b, nW2b, nb2b)
    out.update(s1=s1, new1=(nW1, nb1, nW2, nb2), s2=s2, new2=(nW1b, nb1b, nW2b, nb2b), s3=s3)

    # finite differences on W1[0,0] with step h
    def loss_with(W1_):
        return forward(W1_, b1, W2, b2)[3]
    h = 1e-5
    Wp, Wm = W1.copy(), W1.copy()
    Wp[0, 0] += h
    Wm[0, 0] -= h
    out['fd_W1_00'] = (loss_with(Wp) - loss_with(Wm)) / (2 * h)
    # the sigmoid and tanh slopes (Session 11 owns both)
    out['sig_z'] = -0.3
    out['sig_a'] = float(_sig(-0.3))
    out['sig_slope'] = out['sig_a'] * (1 - out['sig_a'])
    out['tanh_z'] = 0.5
    out['tanh_h'] = float(np.tanh(0.5))
    out['tanh_slope'] = 1 - out['tanh_h'] ** 2
    return out


def ridge_fit(X, y, lam):
    if lam == 0:
        return np.linalg.lstsq(X, y, rcond=None)[0]       # no penalty: the plain least squares answer
    D = np.eye(X.shape[1])
    D[0, 0] = 0.0
    return np.linalg.solve(X.T @ X + lam * D, X.T @ y)


def poly_features(x, degree):
    return np.vander(x, degree + 1, increasing=True)


def n12():
    rng = np.random.default_rng(19)
    xtr = np.linspace(-1, 1, 10)
    f = lambda x: np.sin(1.5 * x) + 0.4 * x ** 2
    ytr = np.round(f(xtr) + rng.normal(0, 0.15, 10), 2)
    xte = np.linspace(-0.97, 0.97, 20)                     # validation points: used to choose lambda
    yte = np.round(f(xte) + rng.normal(0, 0.15, 20), 2)
    xts = np.linspace(-0.95, 0.95, 20)                     # test points: used once, after lambda is chosen
    yts = np.round(f(xts) + rng.normal(0, 0.15, 20), 2)
    deg = 9
    Xtr, Xte = poly_features(xtr, deg), poly_features(xte, deg)
    lams = [0.0, 0.001, 0.01, 0.1, 1.0, 10.0]
    rows = []
    for lam in lams:
        w = ridge_fit(Xtr, ytr, lam)
        rows.append(dict(lam=lam, w=w, norm2=float(w[1:] @ w[1:]), rmse_tr=float(np.sqrt(np.mean((Xtr @ w - ytr) ** 2))), rmse_te=float(np.sqrt(np.mean((Xte @ w - yte) ** 2)))))
    xg = np.linspace(-1, 1, 120)
    Xts = poly_features(xts, deg)
    d = dict(xtr=xtr, ytr=ytr, xte=xte, yte=yte, xts=xts, yts=yts, deg=deg, lams=lams, rows=rows, xg=xg, f=f, Xtr=Xtr, Xte=Xte, Xts=Xts)
    d['lam_best'] = min(rows, key=lambda r: r['rmse_te'])['lam']          # chosen on the validation points only
    wb = ridge_fit(Xtr, ytr, d['lam_best'])
    d['rmse_test'] = float(np.sqrt(np.mean((Xts @ wb - yts) ** 2)))        # reported once
    d['rmse_val_02'] = float(np.sqrt(np.mean((Xte @ ridge_fit(Xtr, ytr, 0.2) - yte) ** 2)))
    d['cond0'] = float(np.linalg.cond(Xtr.T @ Xtr))
    d['xrow'] = Xtr[6]                                                   # the row for x = 0.333
    d['curves'] = {r['lam']: poly_features(xg, deg) @ r['w'] for r in rows}
    z = np.array([1000.0, 1001.0, 1002.0])
    e = np.exp(z - z.max())
    d['soft_big'] = e / e.sum()
    z2 = np.array([2.0, 1.0, 0.1])
    e2 = np.exp(z2)
    d['soft_small'] = e2 / e2.sum()
    d['exp_small'] = e2
    d['lse_big'] = float(z.max() + np.log(np.exp(z - z.max()).sum()))
    return d


# =====================================================================  drawing helpers
class Ax:
    """A little set of axes inside a Scene: data coordinates mapped to inches."""

    def __init__(self, s, x0, y0, x1, y1, xlim, ylim, xlabel='', ylabel='', size=14, ticks=True, xt=None, yt=None, axes=True, ydx=0.5):
        self.s, self.x0, self.y0, self.x1, self.y1, self.xlim, self.ylim = s, x0, y0, x1, y1, xlim, ylim
        if axes:
            s.line(x0, y0, x1, y0, color=INK, lw=2)
            s.line(x0, y0, x0, y1, color=INK, lw=2)
        if xlabel:
            s.text((x0 + x1) / 2, y0 - 0.5, xlabel, size=size, color=MUTE)
        if ylabel:
            s.text(x0 - ydx, (y0 + y1) / 2, ylabel, size=size, color=MUTE, rot=90)
        for v in (xt or []):
            s.line(self.px(v), y0, self.px(v), y0 - 0.07, color=INK, lw=1.4)
            s.text(self.px(v), y0 - 0.25, f'{v:g}', size=14, color=GREY)
        for v in (yt or []):
            s.line(x0 - 0.07, self.py(v), x0, self.py(v), color=INK, lw=1.4)
            s.text(x0 - 0.12, self.py(v), f'{v:g}', size=14, color=GREY, ha='right')

    def px(self, v):
        return self.x0 + (v - self.xlim[0]) / (self.xlim[1] - self.xlim[0]) * (self.x1 - self.x0)

    def py(self, v):
        return self.y0 + (v - self.ylim[0]) / (self.ylim[1] - self.ylim[0]) * (self.y1 - self.y0)

    def plot(self, xs, ys, color=INK, lw=3, ls='-', z=3):
        xs, ys = np.asarray(xs, float), np.asarray(ys, float)
        ok = (ys >= self.ylim[0]) & (ys <= self.ylim[1])
        X = np.where(ok, [self.px(v) for v in xs], np.nan)
        Y = np.where(ok, [self.py(v) for v in ys], np.nan)
        self.s.ax.plot(X, Y, color=color, lw=lw, ls=ls, zorder=z, solid_capstyle='round')

    def dot(self, x, y, r=0.09, fill=INK, edge=INK, z=5):
        self.s.circle(self.px(x), self.py(y), r, fill=fill, edge=edge, lw=1.6, z=z)


# =====================================================================  session 10
@fig('x_d_loss_bowl')
def d_loss_bowl(w, h, size=16, **_):
    s = Scene(w, h)
    a = Ax(s, 1.0, 0.95, w - 0.3, h - 0.3, (-0.5, 6.5), (0, 12), 'parameter w (the number the model can change)', 'loss L (how wrong)', size=size)
    ws = np.linspace(-0.4, 6.4, 100)
    a.plot(ws, (ws - 3) ** 2, INK, 3.2)
    # start point and tangent
    w0 = 0.5
    L0 = (w0 - 3) ** 2
    slope = 2 * (w0 - 3)
    tx = np.array([w0 - 0.5, w0 + 1.0])
    a.plot(tx, L0 + slope * (tx - w0), GREY, 2.4, '--')
    a.dot(w0, L0, 0.15, GOLD)
    s.text(a.px(w0) + 0.25, a.py(L0) + 0.35, 'start', size=size, weight='bold', ha='left')
    s.text(a.px(1.55), a.py(10.6), 'slope of the loss\nat the start:\nnegative (falls to the right)', size=size - 1, color=MUTE, ha='left')
    a.dot(3, 0, 0.15, GOLD)
    s.text(a.px(3), a.py(4.6), 'bottom: smallest loss', size=size, weight='bold')
    s.arrow(a.px(3), a.py(4.6) - 0.25, a.px(3), a.py(0) + 0.25, color=INK, lw=2.0, head=14)
    s.arrow(a.px(w0) + 0.45, a.py(L0) - 0.2, a.px(1.7) + 0.45, a.py((1.7 - 3) ** 2) + 0.2, color=RED, lw=2.8, head=18)
    s.text(a.px(1.0) + 0.9, a.py(8.4), 'step downhill', size=size, color=RED, weight='bold', ha='left')
    return s


@fig('x_d_gd_rates')
def d_gd_rates(w, h, panels=(), size=15, **_):
    """panels: [{title, eta, path, note}] each drawn on L(w) = (w - 3)^2, w from -2 to 9, loss up to 30."""
    s = Scene(w, h)
    n = len(panels)
    gap = 0.55
    pw = (w - 1.3 - gap * (n - 1)) / n
    for i, p in enumerate(panels):
        x0 = 0.9 + i * (pw + gap)
        a = Ax(s, x0, 1.15, x0 + pw, h - 0.95, (-2, 9), (0, 30), 'w', 'L' if i == 0 else '', size=size, xt=[0, 3, 6])
        ws = np.linspace(-2, 9, 150)
        a.plot(ws, (ws - 3) ** 2, INK, 2.8)
        path = p['path']
        for j in range(len(path) - 1):
            x1, x2 = path[j], path[j + 1]
            y1, y2 = (x1 - 3) ** 2, (x2 - 3) ** 2
            if -2 <= x1 <= 9 and -2 <= x2 <= 9 and y1 <= 30 and y2 <= 30:
                s.arrow(a.px(x1), a.py(y1) + 0.07, a.px(x2), a.py(y2) + 0.07, color=RED, lw=1.8, head=12, rad=0.35 if y2 > y1 + 3 or abs(x2 - x1) > 2.5 else 0.0, z=4)
        for j, v in enumerate(path):
            y = (v - 3) ** 2
            if -2 <= v <= 9 and y <= 30:
                a.dot(v, y, 0.1, GOLD if j == 0 else PAPER)
        s.text(x0 + pw / 2, h - 0.35, p['title'], size=size + 2, weight='bold')
        s.text(x0 + pw / 2, h - 0.72, p['note'], size=size, color=MUTE)
    return s


@fig('x_d_batches')
def d_batches(w, h, size=15, **_):
    s = Scene(w, h)
    cols = [dict(t='Batch gradient descent', u=[1] * 8, c1='All 8 rows per step', c2='1 step per epoch', seed=None),
            dict(t='Stochastic (SGD)', u=[0, 0, 0, 1, 0, 0, 0, 0], c1='1 row per step', c2='8 steps per epoch', seed=3),
            dict(t='Mini-batch', u=[0, 0, 1, 1, 0, 0, 1, 1], c1='4 rows per step', c2='2 steps per epoch', seed=5)]
    gap = 0.5
    cw = (w - 0.1 - gap * 2) / 3
    for i, c in enumerate(cols):
        x0 = 0.05 + i * (cw + gap)
        s.text(x0 + cw / 2, h - 0.3, c['t'], size=size + 2, weight='bold')
        sq = 0.4
        sx = x0 + (cw - 8 * sq) / 2
        for k, u in enumerate(c['u']):
            s.box(sx + k * sq, h - 1.05, sq - 0.04, sq - 0.04, '', fill=GOLD if u else PAPER, edge=INK, lw=1.4, r=0.02)
        s.text(x0 + cw / 2, h - 1.45, c['c1'], size=size)
        s.text(x0 + cw / 2, h - 1.8, c['c2'], size=size, color=MUTE)
        # path towards the minimum
        px0, py0, pw, ph = x0 + 0.1, 0.25, cw - 0.2, h - 2.3
        s.rect(px0, py0, pw, ph, fill=PAPER, edge=HAIR, lw=1.2, z=1)
        cx, cy = px0 + pw / 2, py0 + ph / 2
        for r in (0.3, 0.6, 0.9):
            s.ax.add_patch(__import__('matplotlib').patches.Ellipse((cx, cy), 2 * r * pw / 2 * 0.95, 2 * r * ph / 2 * 0.95, fc='none', ec=HAIR, lw=1.2, zorder=1))
        rng = np.random.default_rng(c['seed'] or 0)
        start = np.array([px0 + 0.2, py0 + 0.25])
        goal = np.array([cx, cy])
        pts = [start]
        steps = 6
        for k in range(1, steps + 1):
            base = start + (goal - start) * (1 - 0.72 ** k) / (1 - 0.72 ** steps) if False else start + (goal - start) * k / steps
            if c['seed'] is not None and k < steps:
                amp = 0.42 if c['seed'] == 3 else 0.2
                base = base + rng.normal(0, amp, 2) * np.array([1.0, 0.8])
            pts.append(np.clip(base, [px0 + 0.1, py0 + 0.1], [px0 + pw - 0.1, py0 + ph - 0.1]))
        for k in range(steps):
            s.arrow(pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1], color=RED, lw=2.0, head=12, z=4)
        s.circle(cx, cy, 0.11, fill=GOLD, edge=INK, lw=1.8, z=5)
    return s


def _contour_loss(w1, w2, k=10.0):
    return 0.5 * (w1 ** 2 + k * w2 ** 2)


@fig('x_d_momentum')
def d_momentum(w, h, size=15, **_):
    s = Scene(w, h)
    k = 10.0
    eta = 0.19
    def run(beta, steps):
        p = np.array([-3.0, 1.0])
        v = np.zeros(2)
        out = [p.copy()]
        for _ in range(steps):
            g = np.array([p[0], k * p[1]])
            v = beta * v + g
            p = p - eta * (v if beta else g) if beta else p - eta * g
            out.append(p.copy())
        return np.array(out)
    gap = 0.6
    pw = (w - 0.9 - gap) / 2
    for i, (title, beta, steps) in enumerate((('Plain gradient descent', 0.0, 14), ('With momentum', 0.5, 14))):
        x0 = 0.5 + i * (pw + gap + 0.4)
        a = Ax(s, x0, 0.45, x0 + pw, h - 0.8, (-3.6, 3.6), (-1.35, 1.35), axes=False)
        s.rect(x0, 0.45, pw, h - 1.25, fill=PAPER, edge=HAIR, lw=1.2, z=1)
        for lv in (0.25, 1.0, 2.2, 4.0, 6.5):
            t = np.linspace(0, 2 * np.pi, 120)
            r1, r2 = math.sqrt(2 * lv), math.sqrt(2 * lv / k)
            xs, ys = r1 * np.cos(t), r2 * np.sin(t)
            ok = (np.abs(xs) < 3.6) & (np.abs(ys) < 1.35)
            X = np.where(ok, [a.px(v) for v in xs], np.nan)
            Y = np.where(ok, [a.py(v) for v in ys], np.nan)
            s.ax.plot(X, Y, color=HAIR, lw=1.5, zorder=1)
        P = run(beta, steps)
        for j in range(len(P) - 1):
            s.arrow(a.px(P[j][0]), a.py(P[j][1]), a.px(P[j + 1][0]), a.py(P[j + 1][1]), color=RED, lw=1.9, head=11, z=4)
        a.dot(P[0][0], P[0][1], 0.12, GOLD)
        a.dot(0, 0, 0.12, GOLD)
        s.text(x0 + pw / 2, h - 0.4, title, size=size + 2, weight='bold')
    return s


@fig('x_d_convex')
def d_convex(w, h, size=15, **_):
    s = Scene(w, h)
    gap = 0.9
    pw = (w - 0.9 - gap) / 2
    xs = np.linspace(0, 1, 200)
    f1 = lambda u: 0.15 + 0.85 * (2 * u - 1) ** 2
    f2 = lambda u: 1.0 - 0.55 * np.exp(-((u - 0.25) / 0.11) ** 2) - 0.8 * np.exp(-((u - 0.75) / 0.12) ** 2) + 0.25 * (u - 0.5) ** 2
    ys2 = f2(xs)
    for i, (title, f) in enumerate((('Convex: one bowl', f1), ('Not convex: several dips', f2))):
        x0 = 0.8 + i * (pw + gap)
        a = Ax(s, x0, 0.95, x0 + pw, h - 1.0, (0, 1), (-0.3, 1.25), 'parameter w', 'loss L' if i == 0 else '', size=size)
        a.plot(xs, f(xs), INK, 3.2)
        s.text(x0 + pw / 2, h - 0.4, title, size=size + 2, weight='bold')
        if i == 0:
            a.dot(0.05, f(0.05), 0.12, GOLD)
            a.dot(0.93, f(0.93), 0.12, GOLD)
            a.dot(0.5, f(0.5), 0.13, RED)
            s.text(a.px(0.5), a.py(f(0.5)) + 0.35, 'the only minimum', size=size, weight='bold')
            s.text(a.px(0.5), a.py(1.02), 'Any start walks downhill\nto the same bottom.', size=size, color=MUTE)
        else:
            i_loc = int(np.argmin(np.where(xs < 0.5, ys2, 9)))
            i_glob = int(np.argmin(np.where(xs > 0.5, ys2, 9)))
            a.dot(xs[i_loc], ys2[i_loc], 0.12, GOLD)
            a.dot(xs[i_glob], ys2[i_glob], 0.12, RED)
            s.text(a.px(xs[i_glob]), a.py(ys2[i_glob]) - 0.38, 'lowest dip', size=size, weight='bold')
            s.text(a.px(xs[i_loc]), a.py(ys2[i_loc]) - 0.38, 'local minimum', size=size, weight='bold')
            s.text(a.px(0.5), a.py(1.14), 'Where you end depends on where you start.', size=size, color=MUTE)
    return s


@fig('x_d_schedule')
def d_schedule(w, h, size=15, T=1000, warm=100, **_):
    s = Scene(w, h)
    a = Ax(s, 1.1, 0.95, w - 0.3, h - 0.5, (0, T), (0, 1.15), 'training step', 'learning rate (share of its peak)', size=size, xt=[0, 250, 500, 750, 1000], yt=[0, 0.5, 1.0])
    t = np.arange(0, T + 1)
    const = np.ones_like(t, dtype=float)
    cos = np.where(t < warm, t / warm, 0.5 * (1 + np.cos(np.pi * (t - warm) / (T - warm))))
    stepd = np.where(t < 400, 1.0, np.where(t < 700, 0.3, 0.09))
    a.plot(t, const, GREY, 2.6, '--')
    a.plot(t, stepd, MUTE, 2.8, '-')
    a.plot(t, cos, RED, 4.0)
    s.text(a.px(T) - 0.1, a.py(1.0) + 0.27, 'constant', size=size, color=GREY, ha='right')
    s.text(a.px(900), a.py(0.09) + 0.45, 'step decay', size=size, color=MUTE, ha='right')
    s.text(a.px(warm) + 0.1, a.py(0.55), 'warm-up: rises\nfrom 0 to the peak', size=size, color=RED, weight='bold', ha='left')
    s.text(a.px(560), a.py(0.7), 'cosine decay:\nfalls smoothly', size=size, color=RED, weight='bold', ha='left')
    return s


# =====================================================================  session 11
@fig('x_d_net')
def d_net(w, h, inputs=(), hidden=(), out='', edges1=(), edges2=(), foot='', head=('Input layer', 'Hidden layer', 'Output'), size=15, ecolor=INK, **_):
    """inputs: two strings; hidden: two strings (may contain newlines); out: string; edges1: [[h1 from x1, h1 from x2],[h2 from x1, h2 from x2]]; edges2: [out from h1, out from h2]."""
    s = Scene(w, h)
    xi0, xi1 = 0.1, 1.45
    xh0, xh1 = 3.3, 5.0
    xo0, xo1 = w - 1.75, w - 0.1
    yi = [h - 1.5, 1.75]
    yh = [h - 1.5, 1.75]
    yo = (yi[0] + yi[1]) / 2
    bh = 0.9
    for txt, x in zip(head, ((xi0 + xi1) / 2, (xh0 + xh1) / 2, (xo0 + xo1) / 2)):
        s.text(x, h - 0.3, txt, size=size, weight='bold', color=MUTE)

    def lab(x1, y1, x2, y2, t, text, col):
        x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        wd = K.width_in(text, size) + 0.12
        s.box(x - wd / 2, y - 0.17, wd, 0.34, text, size=size, fill=PAPER, edge=PAPER, lw=0, z=5, color=col, weight='bold')
    for j in range(2):
        for i in range(2):
            s.line(xi1, yi[i], xh0, yh[j], color=ecolor, lw=1.8, z=1)
    for j in range(2):
        for i in range(2):
            t = 0.2 if i != j else 0.62      # a crossing line is labelled near its own input, far from the crossing point
            lab(xi1, yi[i], xh0, yh[j], t, str(edges1[j][i]), ecolor)
    for j in range(2):
        s.line(xh1, yh[j], xo0, yo, color=ecolor, lw=1.8, z=1)
        lab(xh1, yh[j], xo0, yo, 0.5, str(edges2[j]), ecolor)
    for i in range(2):
        s.box(xi0, yi[i] - bh / 2, xi1 - xi0, bh, inputs[i], size=size, fill=PAPER, edge=INK, lw=2.0)
        s.box(xh0, yh[i] - bh / 2, xh1 - xh0, bh, hidden[i], size=size, fill=PAPER, edge=INK, lw=2.0)
    s.box(xo0, yo - bh / 2, xo1 - xo0, bh, out, size=size, fill=GOLD, edge=INK, lw=2.4)
    if foot:
        s.text(w / 2, 0.55, foot, size=size, color=BODY)
    return s


@fig('x_d_backprop_flow')
def d_backprop_flow(w, h, size=16, **_):
    s = Scene(w, h)
    n = 5
    gap = 0.4
    bw = (w - 0.1 - gap * (n - 1)) / n
    top = ['input $x$', r'$z^{(1)} = W^{(1)} x + b^{(1)}$', r'$a^{(1)} = \sigma(z^{(1)})$', r'$\hat{y} = W^{(2)} a^{(1)} + b^{(2)}$', 'loss $L$']
    shp = ['2 × 1', '2 × 1', '2 × 1', '1 × 1', 'one number']
    xs = [0.05 + i * (bw + gap) for i in range(n)]
    s.text(0.05, h - 0.25, 'Forward pass: left to right, and store every value', size=size, weight='bold', ha='left')
    ytop, bh = h - 1.45, 0.9
    for i in range(n):
        s.box(xs[i], ytop, bw, bh, top[i], size=size, fill=PAPER, edge=INK, lw=2.0)
        s.text(xs[i] + bw / 2, ytop - 0.28, shp[i], size=size - 1, color=MUTE)
        if i < n - 1:
            s.arrow(xs[i] + bw + 0.03, ytop + bh / 2, xs[i + 1] - 0.03, ytop + bh / 2, lw=2.2, head=15)
    s.text(0.05, 2.05, 'Backward pass: right to left, reusing the stored values', size=size, weight='bold', color=RED, ha='left')
    yb = 0.35
    bot = [(0, [r'$\partial L / \partial W^{(1)}$', r'$= \delta^{(1)} x^T$'], PAPER), (1, [r'$\delta^{(1)} = (W^{(2)T} \delta^{(2)})$', r'$\odot\; a^{(1)} \odot (1 - a^{(1)})$'], GOLD),
           (2, [r'$\partial L / \partial W^{(2)}$', r'$= \delta^{(2)} a^{(1)T}$'], PAPER), (3, [r'$\delta^{(2)} = \hat{y} - y$'], GOLD)]
    for i, lines, fill in bot:
        s.box(xs[i], yb, bw, bh, '', fill=fill, edge=INK, lw=2.0)
        if len(lines) == 1:
            s.text(xs[i] + bw / 2, yb + bh / 2, lines[0], size=size)
        else:
            s.text(xs[i] + bw / 2, yb + bh / 2 + 0.18, lines[0], size=size - 1)
            s.text(xs[i] + bw / 2, yb + bh / 2 - 0.19, lines[1], size=size - 1)
        if i < 3:
            s.arrow(xs[i + 1] - 0.03, yb + bh / 2, xs[i] + bw + 0.03, yb + bh / 2, color=RED, lw=2.2, head=15)
    return s


@fig('x_d_finite_diff')
def d_finite_diff(w, h, size=15, **_):
    s = Scene(w, h)
    a = Ax(s, 1.0, 0.95, w - 0.3, h - 0.35, (0, 4), (0, 3.2), 'one weight w (all others held fixed)', 'loss L', size=size)
    f = lambda u: 0.35 * (u - 0.4) ** 2 * (u - 3.4) ** 2 / 3 + 0.5 + 0.2 * u
    xs = np.linspace(0.05, 3.95, 160)
    a.plot(xs, f(xs), INK, 3.2)
    w0, hh = 1.6, 0.7
    d = (f(w0 + 1e-5) - f(w0 - 1e-5)) / 2e-5
    ts = np.array([w0 - 1.0, w0 + 1.2])
    a.plot(ts, f(w0) + d * (ts - w0), GREY, 2.4, '--')
    a.plot([w0 - hh, w0 + hh], [f(w0 - hh), f(w0 + hh)], RED, 3.2)
    for v in (w0 - hh, w0, w0 + hh):
        a.dot(v, f(v), 0.1, GOLD if v == w0 else PAPER)
    s.text(a.px(w0 - hh), a.py(0) + 0.2, 'w - h', size=size)
    s.text(a.px(w0), a.py(0) + 0.2, 'w', size=size)
    s.text(a.px(w0 + hh), a.py(0) + 0.2, 'w + h', size=size)
    for v in (w0 - hh, w0, w0 + hh):
        s.line(a.px(v), a.py(0), a.px(v), a.py(f(v)), color=HAIR, lw=1.2, z=1)
    s.text(a.px(0.15), a.py(3.0), 'red line: slope between w - h and w + h\n(a numerical estimate)', size=size, color=RED, weight='bold', ha='left')
    s.text(a.px(0.15), a.py(2.45), 'grey dashed line: the true slope (the derivative)', size=size, color=MUTE, ha='left')
    return s


@fig('x_d_cost')
def d_cost(w, h, size=15, **_):
    s = Scene(w, h)
    u = 0.85
    x0 = 3.55
    rows = [('Answering one question\n(one forward pass per token)', [('forward', 1, PAPER)]),
            ('One training step\n(forward, then backward)', [('forward', 1, PAPER), ('backward\n(about 2x)', 2, GOLD)]),
            ('Training', [('step', 3, PAPER), ('step', 3, PAPER), ('... many more ...', 3.2, PAPER)])]
    bh = 0.85
    for i, (lab, parts) in enumerate(rows):
        y = h - 0.95 - i * 1.3
        s.text(x0 - 0.2, y + bh / 2, lab, size=size, ha='right', weight='bold')
        x = x0
        for t, k, col in parts:
            wd = k * u
            s.box(x, y, wd, bh, t, size=size - (1 if len(t) > 14 else 0), fill=col, edge=INK, lw=2.0)
            x += wd + (0.08 if i == 2 else 0)
        if i == 2:
            s.text(x0, y - 0.35, 'Each step reads a new batch of text. A whole run repeats it a very large number of times.', size=size - 1, color=MUTE, ha='left')
    return s


@fig('x_d_sig_tanh')
def d_sig_tanh(w, h, size=15, **_):
    """Session 11: the sigmoid and tanh (black) with their slopes (red dashed), each slope at its largest at z = 0."""
    s = Scene(w, h)
    gap = 0.9
    pw = (w - 1.2 - gap) / 2
    zs = np.linspace(-6, 6, 241)
    sg = _sig(zs)
    th = np.tanh(zs)
    panels = [('Sigmoid: a = 1 / (1 + e^-z)', (-0.1, 1.1), [0, 0.25, 0.5, 1], sg, sg * (1 - sg), 'slope a(1 - a)', 0.25, 'largest slope 0.25', 'a between 0 and 1'),
              ('Tanh: h = (e^z - e^-z) / (e^z + e^-z)', (-1.15, 1.15), [-1, 0, 1], th, 1 - th ** 2, 'slope 1 - h^2', 1.0, 'largest slope 1', 'h between -1 and 1')]
    for i, (title, yl, yt, f, df, dlab, top, toplab, flab) in enumerate(panels):
        x0 = 0.85 + i * (pw + gap)
        a = Ax(s, x0, 0.95, x0 + pw, h - 0.75, (-6, 6), yl, 'z (the weighted sum)', '', size=size, xt=[-6, -3, 0, 3, 6], yt=yt)
        s.line(a.px(-6), a.py(0), a.px(6), a.py(0), color=HAIR, lw=1.2, z=1)
        a.plot(zs, f, INK, 3.4)
        a.plot(zs, df, RED, 3.0, '--')
        a.dot(0, top, 0.1, GOLD)
        s.text(a.px(0) + 0.15, a.py(top) + 0.25, toplab, size=size, color=RED, weight='bold', ha='left')
        s.text(a.px(-5.8), a.py(yl[1]) - 0.15, dlab + ' (dashed)', size=size, color=RED, ha='left')
        s.text(a.px(5.8), a.py(0.5 if i == 0 else -0.4), flab, size=size, color=INK, ha='right')   # clear of both curves
        s.text(x0 + pw / 2, h - 0.3, title, size=size + 1, weight='bold')
    return s


# =====================================================================  session 12
@fig('x_d_softmax_bars')
def d_softmax_bars(w, h, scores=(2.0, 1.0, 0.1), size=16, **_):
    """Session 12: scores (logits) on the left become probabilities that add to 1 on the right."""
    s = Scene(w, h)
    z = np.asarray(scores, float)
    p = np.exp(z) / np.exp(z).sum()
    names = ['A', 'B', 'C']          # three candidate tokens
    bw, gap = 0.5, 0.2
    base = 1.0
    top = h - 1.0
    lx = 0.35
    rx = w - 0.35 - (3 * bw + 2 * gap)

    def group(x0, vals, vmax, fmt, fill, head):
        s.text(x0 + (3 * bw + 2 * gap) / 2, h - 0.3, head, size=size, weight='bold')
        s.line(x0 - 0.1, base, x0 + 3 * bw + 2 * gap + 0.1, base, color=INK, lw=2)
        for k, v in enumerate(vals):
            x = x0 + k * (bw + gap)
            hh = (top - base) * v / vmax
            s.rect(x, base, bw, max(hh, 0.02), fill=fill, edge=INK, lw=1.6)
            s.text(x + bw / 2, base + hh + 0.22, fmt(v), size=size, weight='bold')
            s.text(x + bw / 2, base - 0.28, names[k], size=size - 1, color=MUTE)
    group(lx, z, z.max(), lambda v: f'{v:g}', PAPER, 'Scores (logits)')
    group(rx, p, p.max(), lambda v: f'{v:.3f}', GOLD, 'Probabilities')
    ax0 = lx + 3 * bw + 2 * gap + 0.25
    s.arrow(ax0, (base + top) / 2, rx - 0.3, (base + top) / 2, color=RED, lw=2.8, head=18)
    s.text((ax0 + rx - 0.3) / 2, (base + top) / 2 + 0.38, 'softmax', size=size + 1, color=RED, weight='bold')
    s.text((ax0 + rx - 0.3) / 2, (base + top) / 2 - 0.4, 'e^z, then divide\nby the total', size=size - 1, color=MUTE)
    s.text(rx + (3 * bw + 2 * gap) / 2, 0.25, f'{p[0]:.3f} + {p[1]:.3f} + {p[2]:.3f} = 1', size=size, weight='bold')
    s.text(lx + (3 * bw + 2 * gap) / 2, 0.25, 'tokens A, B, C', size=size, color=MUTE)
    return s


@fig('x_d_ridge')
def d_ridge(w, h, panels=(), size=15, **_):
    """panels: [{title, note, x, y (curve), xt, yt (training points), xf, yf (true curve)}]"""
    s = Scene(w, h)
    n = len(panels)
    gap = 0.5
    pw = (w - 0.7 - gap * (n - 1)) / n
    for i, p in enumerate(panels):
        x0 = 0.7 + i * (pw + gap)
        a = Ax(s, x0, 1.0, x0 + pw, h - 0.95, (-1.05, 1.05), (-1.3, 1.6), 'x', 'y' if i == 0 else '', size=size, xt=[-1, 0, 1])
        a.plot(p['xf'], p['yf'], GREY, 2.4, '--')
        a.plot(p['x'], p['y'], RED, 3.6)
        for xv, yv in zip(p['xt'], p['yt']):
            a.dot(xv, yv, 0.085, INK)
        s.text(x0 + pw / 2, h - 0.35, p['title'], size=size + 2, weight='bold')
        s.text(x0 + pw / 2, h - 0.68, p['note'], size=size, color=MUTE)
    return s


@fig('x_d_lagrange')
def d_lagrange(w, h, which='line', size=15, **_):
    s = Scene(w, h)
    xl, yl = ((-0.5, 6.0), (-0.5, 3.3)) if which == 'line' else ((-2.2, 5.0), (-1.7, 2.33))
    # equal aspect: one unit of w2 is as long on the page as one unit of w1, so a circle looks round
    mid, half = (yl[0] + yl[1]) / 2, (xl[1] - xl[0]) * (h - 0.6) / (w - 0.7) / 2
    yl = (mid - half, mid + half)
    a = Ax(s, 0.5, 0.35, w - 0.2, h - 0.25, xl, yl, axes=False)
    s.line(a.px(xl[0] + 0.1), a.py(0), a.px(xl[1] - 0.1), a.py(0), color=GREY, lw=1.4, z=1)
    s.line(a.px(0), a.py(yl[0] + 0.1), a.px(0), a.py(yl[1] - 0.1), color=GREY, lw=1.4, z=1)
    s.text(a.px(xl[1] - 0.2), a.py(0) + 0.22, 'w1', size=size, color=MUTE)
    s.text(a.px(0) + 0.25, a.py(yl[1] - 0.15), 'w2', size=size, color=MUTE)
    t = np.linspace(0, 2 * np.pi, 400)

    def curve(xs, ys, col, lw, z=3):
        ok = (xs > xl[0]) & (xs < xl[1]) & (ys > yl[0]) & (ys < yl[1])
        s.ax.plot(np.where(ok, [a.px(v) for v in xs], np.nan), np.where(ok, [a.py(v) for v in ys], np.nan), color=col, lw=lw, zorder=z)

    def tag(x, y, text, col=INK, ha='left'):
        s.text(a.px(x), a.py(y), text, size=size, weight='bold', color=col, ha=ha, bbox=dict(fc='white', ec='none', pad=2.0))
    if which == 'line':
        for r in (0.7, 1.0, 1.414, 2.0, 2.6, 3.2):
            curve(r * np.cos(t), r * np.sin(t), HAIR if abs(r - 1.414) > 0.01 else INK, 1.6 if abs(r - 1.414) > 0.01 else 3.0)
        xs = np.linspace(-0.5, 2.5, 20)
        curve(xs, 2 - xs, RED, 3.6)
        a.dot(1, 1, 0.13, GOLD)
        tag(1.5, 2.25, 'best point on the line: (1, 1)\nthe ring just touches the line', INK)
        s.arrow(a.px(1.5), a.py(2.0), a.px(1.07), a.py(1.1), color=INK, lw=1.8, head=12)
        tag(2.55, 0.35, 'boundary: w1 + w2 = 2', RED)
        tag(3.7, 2.7, 'rings: loss = w1^2 + w2^2', MUTE)
    else:
        cx, cy, R = 2.9, 0.7, 1.5
        for lv in (0.2, 0.5, 1.0, 1.6):
            curve(cx + math.sqrt(lv) * np.cos(t), cy + math.sqrt(lv) * 0.6 * np.sin(t), HAIR, 1.6)
        th = np.linspace(0, math.pi / 2, 4000)
        px_, py_ = R * np.cos(th), R * np.sin(th)
        L = ((px_ - cx) / 1.0) ** 2 + ((py_ - cy) / 0.6) ** 2
        k = int(np.argmin(L))
        lv = L[k]
        curve(cx + math.sqrt(lv) * np.cos(t), cy + math.sqrt(lv) * 0.6 * np.sin(t), INK, 3.0)
        curve(R * np.cos(t), R * np.sin(t), RED, 3.6)
        a.dot(cx, cy, 0.11, PAPER)
        tag(cx - 0.8, cy + 1.2, 'unconstrained best fit\n(outside the circle)', MUTE)
        a.dot(px_[k], py_[k], 0.13, GOLD)
        tag(-2.2, 1.95, 'best allowed point (on the circle)', INK)
        s.arrow(a.px(-0.3), a.py(1.75), a.px(px_[k]) - 0.05, a.py(py_[k]) + 0.12, color=INK, lw=1.8, head=12)
        tag(-2.1, -0.7, 'allowed: inside the circle\nw1^2 + w2^2 <= r^2', RED)
    return s


@fig('x_d_precision')
def d_precision(w, h, size=15, **_):
    s = Scene(w, h)
    rows = [('float64', 1, 11, 52, 'about 16 digits', 'largest about 1.8e308'),
            ('float32', 1, 8, 23, 'about 7 digits', 'largest about 3.4e38'),
            ('bfloat16', 1, 8, 7, 'about 2 digits', 'largest about 3.4e38'),
            ('float16', 1, 5, 10, 'about 3 digits', 'largest 65,504')]
    bit = 0.056
    x0 = 1.45
    rh = (h - 1.5) / len(rows)
    s.text(x0, h - 0.25, 'Bar length = bits. Number above = bits in that part.', size=size, color=MUTE, ha='left')
    for i, (nm, sg, ex, ma, dig, mx) in enumerate(rows):
        y = h - 0.7 - (i + 0.5) * rh
        s.text(x0 - 0.15, y, nm, size=size + 1, weight='bold', ha='right')
        x = x0
        for k, (cnt, col) in enumerate(((sg, RED), (ex, GOLD), (ma, PAPER))):
            wd = cnt * bit
            s.rect(x, y - 0.17, wd, 0.34, fill=col, edge=INK, lw=1.6)
            s.text(x + wd / 2, y + 0.37, f'{cnt}', size=size - 1, weight='bold')
            x += wd
        s.text(x + 0.2, y + 0.13, f'{dig}', size=size, ha='left', weight='bold')
        s.text(x + 0.2, y - 0.19, mx, size=size - 1, ha='left', color=MUTE)
    s.rect(x0, 0.12, 0.3, 0.22, fill=RED, edge=INK, lw=1.2)
    s.text(x0 + 0.4, 0.23, 'sign', size=size, ha='left')
    s.rect(x0 + 1.2, 0.12, 0.3, 0.22, fill=GOLD, edge=INK, lw=1.2)
    s.text(x0 + 1.6, 0.23, 'exponent (the range)', size=size, ha='left')
    s.rect(x0 + 3.9, 0.12, 0.3, 0.22, fill=PAPER, edge=INK, lw=1.2)
    s.text(x0 + 4.3, 0.23, 'mantissa (the digits)', size=size, ha='left')
    return s


@fig('x_d_vanish')
def d_vanish(w, h, size=15, layers=10, **_):
    s = Scene(w, h)
    a = Ax(s, 1.1, 0.95, w - 2.9, h - 0.4, (0, layers), (-8, 3), 'layers walked back from the output', 'gradient size (powers of 10)', size=size, xt=[0, 5, 10], yt=[-6, -3, 0, 3])
    ks = np.arange(0, layers + 1)
    for fac, col, lab, ls in ((0.25, RED, 'factor 0.25 per layer: vanishes', '-'), (1.0, INK, 'factor 1: steady', '-'), (1.8, GOLD, 'factor 1.8 per layer: explodes', '-')):
        a.plot(ks, np.log10(fac ** ks), col, 4.0 if col != GOLD else 5.0, ls)
        yend = math.log10(fac ** layers)
        s.text(a.px(layers) + 0.15, a.py(yend), lab.replace(': ', ':\n'), size=size - 1, color=INK if col == GOLD else col, weight='bold', ha='left')
    s.line(a.px(0), a.py(0), a.px(layers), a.py(0), color=HAIR, lw=1.2, z=1)
    return s


@fig('x_d_longprod')
def d_longprod(w, h, size=15, **_):
    s = Scene(w, h)
    a = Ax(s, 1.2, 0.95, w - 0.4, h - 0.5, (0, 400), (-500, 50), 'tokens in the output (each with probability 0.1)', 'log10 of the result', size=size, xt=[0, 100, 200, 300, 400], yt=[-400, -300, -200, -100, 0], ydx=0.85)
    n = np.arange(0, 401)
    a.plot(n, -n.astype(float), RED, 3.8)
    s.text(a.px(400) - 0.1, a.py(-55) + 0.1, 'the true value of the product 0.1^n', size=size, color=RED, weight='bold', ha='right')
    s.line(a.px(0), a.py(-324), a.px(400), a.py(-324), color=INK, lw=2.4, dash=True, z=3)
    s.text(a.px(5), a.py(-324) - 0.3, 'smallest float64 number, about 5e-324 (n = 324)', size=size, ha='left', weight='bold')
    s.text(a.px(300), a.py(-455), 'below the dashed line the\nstored product is exactly 0', size=size, color=INK, weight='bold')
    return s


@fig('x_d_loop')
def d_loop(w, h, items=(), center='', size=16, highlight=None, **_):
    """A loop of up to 6 boxes in two rows: the top row runs left to right, the bottom row right to left, arrows close the loop."""
    s = Scene(w, h)
    n = len(items)
    top_n = (n + 1) // 2
    bot_n = n - top_n
    bw, gap = (w - 0.2 - 0.5 * (top_n - 1)) / top_n, 0.5
    bh = 1.15
    ytop, ybot = h - 0.35 - bh, 0.55
    pos = []
    for i in range(top_n):
        pos.append((0.1 + i * (bw + gap), ytop))
    for j in range(bot_n):
        pos.append((0.1 + (top_n - 1 - j) * (bw + gap) - ((top_n - bot_n) * (bw + gap) / 2 if bot_n < top_n else 0) * 0, ybot))
    # centre the bottom row under the top row
    off = (top_n - bot_n) * (bw + gap) / 2
    pos = pos[:top_n] + [(0.1 + (bot_n - 1 - j) * (bw + gap) + off, ybot) for j in range(bot_n)]
    for i, ((x, y), t) in enumerate(zip(pos, items)):
        s.box(x, y, bw, bh, '', fill=GOLD if highlight == i else PAPER, edge=INK, lw=2.0, z=3)
        lines = K.wrap(t, size, 'bold', bw - 0.2)
        s.text(x + bw / 2, y + bh / 2, '\n'.join(lines), size=size, weight='bold')
    for i in range(n - 1):
        (x1, y1), (x2, y2) = pos[i], pos[i + 1]
        if y1 == y2:
            if x2 > x1:
                s.arrow(x1 + bw + 0.03, y1 + bh / 2, x2 - 0.03, y2 + bh / 2, lw=2.4, head=16)
            else:
                s.arrow(x1 - 0.03, y1 + bh / 2, x2 + bw + 0.03, y2 + bh / 2, lw=2.4, head=16)
        else:
            s.arrow(x1 + bw / 2, y1 - 0.03, x2 + bw / 2, y2 + bh + 0.03, lw=2.4, head=16)
    (xl, yl), (xf, yf) = pos[-1], pos[0]
    s.arrow(xl + bw / 2, yl + bh + 0.03, xf + bw / 2, yf - 0.03, lw=2.4, head=16, color=RED) if yl != yf else None
    if center:
        s.text(w / 2, (ytop + ybot + bh) / 2, center, size=size, color=MUTE, weight='bold')
    return s
