"""Figure kinds for Session 0: t00_roc (gold area is the whole area under the curve) and t00_descent (labels kept clear of the curve)."""
import numpy as np

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, fig


@fig('x_t00_roc')
def x_t00_roc(w, h, size=16, **_):
    s = Scene(w, h)
    x0, x1, y0, y1 = 0.9, w - 0.3, 0.8, h - 0.3
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    s.text((x0 + x1) / 2, 0.3, 'false alarm rate (of the really fine cases)', size=size, color=MUTE)
    s.text(0.3, (y0 + y1) / 2, 'catch rate (of the really fraud cases)', size=size, color=MUTE, rot=90)
    px = lambda u: x0 + u * (x1 - x0)
    py = lambda v: y0 + v * (y1 - y0)
    us = np.linspace(0, 1, 80)
    curve = lambda u: u ** 0.163          # area under this curve is 1 / 1.163 = 0.86
    s.ax.fill_between([px(u) for u in us], [py(0)] * len(us), [py(curve(u)) for u in us], color=GOLD, alpha=0.45, zorder=1)
    s.ax.plot([px(0), px(1)], [py(0), py(1)], color=MUTE, lw=2, ls='--', zorder=2)
    s.ax.plot([px(u) for u in us], [py(curve(u)) for u in us], color=INK, lw=3.4, zorder=3)
    s.circle(px(0.1), py(curve(0.1)), 0.11, fill=RED, edge=INK, lw=1.6, z=5)
    s.text(px(0.1) + 0.2, py(curve(0.1)) - 0.3, 'one threshold', size=size, ha='left', color=RED, weight='bold')
    s.text(px(0.76), py(0.1), 'Dashed line: coin flip,\narea 0.5', size=size, color=MUTE)
    s.text(px(0.76), py(0.36), 'Gold area under\nthe curve = AUC', size=size, ha='center', weight='bold')
    return s


@fig('x_t00_descent')
def x_t00_descent(w, h, size=17, **_):
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
    s.text(px(0.05) + 0.25, py(curve(0.05)) + 0.15, 'Start: a big error', size=size, ha='left', weight='bold')
    s.text(px(0.5), py(0.78), 'Each step: adjust a little', size=size, color=RED, weight='bold')
    s.text(px(0.5), py(0.5), 'Bottom: the\nsmallest error\nwe can find', size=size, weight='bold')
    return s
