"""Figure kinds for Sessions 23 and 24 (author letter l). Each is registered as x_<name> and used as visual=dict(kind='<name>', ...).

  dl_runs        rows of drawn record numbers: the same seed gives the same draw twice (rows: label, values, tone)
  dl_git         the four places of a Git project and the three commands that move work between them
  dl_file        a file or a folder listing in a dark panel, with plain-words notes beside chosen lines
  dl_code2       a short program in two numbered columns, with key lines in gold
  dl_app         a drawn Streamlit web page: inputs on the left, the result on the right
  dl_drift       a monthly line chart: real series, training window, and a hypothetical shifted series
  dl_groupbars   horizontal bars grouped by category, one or two series, with a reference line
  dl_segments    a bar split into labelled parts in proportion to their value (minutes of a talk)
All text is 14 pt or larger; figkit audits every figure for overlaps.
"""
from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, PALE, RED, GOLD, fig
import slidekit as K
from matplotlib.patches import Rectangle


def tw(t, size, kind='regular'):
    return K.width_in(str(t), size, kind)


def mono_w(t, size):
    return 0.602 * size / 72 * len(t)


def wtext(s, x, y, w, text, size, weight='normal', color=INK, ha='left', va='center'):
    """Wrapped text in a column of width w. Returns its height."""
    lines = K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', w)
    s.text(x, y, '\n'.join(lines), size=size, weight=weight, color=color, ha=ha, va=va)
    return len(lines) * size * 1.15 / 72


# ------------------------------------------------------------------ the same seed gives the same draw
@fig('x_dl_runs')
def dl_runs(w, h, rows=(), head='', foot='', **_):
    """rows: dicts label, values, tone ('gold' for the pair that matches, 'plain'), and optional gap_after."""
    s = Scene(w, h)
    cw, ch, size = 0.8, 0.62, 18
    lab_w = 2.0
    y = h - 0.1
    if head:
        s.text(0.1, y - 0.2, head, size=17, weight='bold', ha='left')
        y -= 0.55
    for r in rows:
        s.text(0.1, y - ch / 2, r['label'], size=17, weight='bold', ha='left')
        for i, v in enumerate(r['values']):
            s.box(lab_w + i * (cw + 0.07), y - ch, cw, ch, str(v), size=size, fill=GOLD if r.get('tone') == 'gold' else PAPER, edge=INK, lw=1.8, r=0.04)
        if r.get('tag'):
            tx = lab_w + len(r['values']) * (cw + 0.07) + 0.12
            s.text(tx, y - ch / 2, r['tag'], size=16, weight='bold', ha='left', color=RED if r.get('tone') != 'gold' else INK)
        y -= ch + 0.14 + r.get('gap_after', 0)
    if foot:
        wtext(s, 0.1, 0.45, w - 0.2, foot, 16, color=BODY)
    return s


# ------------------------------------------------------------------ Git: four places, three commands
@fig('x_dl_git')
def dl_git(w, h, places=(), commands=(), **_):
    """places: list of (name, plain words). commands: list of command strings for the arrows between the places."""
    s = Scene(w, h)
    n = len(places)
    bw = 1.8
    gap = (w - 0.1 - n * bw) / (n - 1)
    bh = 2.25
    y0 = 1.35
    for i, (name, plain) in enumerate(places):
        x = 0.05 + i * (bw + gap)
        s.box(x, y0, bw, bh, '', fill=GOLD if i == n - 1 else PAPER, edge=INK, lw=2.0, r=0.07)
        hh = wtext(s, x + bw / 2, y0 + bh - 0.2 - 0.3, bw - 0.25, name, 18, 'bold', ha='center', va='center')
        wtext(s, x + bw / 2, y0 + (bh - 0.75) / 2, bw - 0.25, plain, 16, color=BODY, ha='center')
        if i < n - 1:
            xa, xb = x + bw + 0.05, x + bw + gap - 0.05
            ym = y0 + bh / 2
            s.arrow(xa, ym, xb, ym, lw=2.6, head=18)
            s.text((xa + xb) / 2, ym + 0.32, commands[i], size=16, mono=True, weight='bold')
    s.text(0.1, 0.85, 'Your laptop', size=16, color=MUTE, ha='left')
    xl = 0.05 + (n - 1) * (bw + gap)
    s.text(xl + bw / 2, 0.85, 'On the internet', size=16, color=MUTE)
    s.line(0.1, 1.1, xl - gap / 2, 1.1, color=INK, lw=2)
    s.line(xl, 1.1, xl + bw, 1.1, color=INK, lw=2)
    return s


# ------------------------------------------------------------------ a file or folder listing with notes
@fig('x_dl_file')
def dl_file(w, h, name='', lines=(), notes=(), size=16, gold=(), **_):
    """lines: strings (mono). notes: list of (line index, plain-words text) shown to the right of the panel. gold: line indices to highlight."""
    s = Scene(w, h)
    lh = size * 1.7 / 72
    cw = max(mono_w(l, size) for l in lines) + 0.5
    cw = max(cw, mono_w(name, size) + 0.5)
    note_x = cw + 0.6
    pad = 0.18
    ph = len(lines) * lh + 2 * pad
    top = h - 0.62
    s.box(0.05, top - ph, cw, ph, '', fill=INK, edge=INK, r=0.08, z=2)
    s.box(0.05, top + 0.04, tw(name, size, 'bold') + 0.5, 0.46, name, size=size, fill=GOLD, edge=INK, lw=1.6, weight='bold', r=0.05, mono=False)
    ys = {}
    for i, l in enumerate(lines):
        yc = top - pad - (i + 0.5) * lh
        ys[i] = yc
        if i in gold:
            s.rect(0.1, yc - lh / 2, cw - 0.1, lh, fill=GOLD, edge=GOLD, lw=0, z=3)
        s.text(0.05 + 0.2, yc, l, size=size, color=INK if i in gold else PAPER, mono=True, ha='left', z=6)
    nw = w - note_x - 0.05
    for i, t in notes:
        s.line(cw + 0.1, ys[i], note_x - 0.12, ys[i], color=RED, lw=2)
        wtext(s, note_x, ys[i], nw, t, 16, color=BODY)
    return s


# ------------------------------------------------------------------ code in two numbered columns
@fig('x_dl_code2')
def dl_code2(w, h, lines=(), per_col=14, gold=(), size=14, **_):
    s = Scene(w, h)
    lh = 0.27
    cols = [lines[i:i + per_col] for i in range(0, len(lines), per_col)]
    n = len(cols)
    gap = 0.2
    cw = (w - 0.1 - gap * (n - 1)) / n
    for c, chunk in enumerate(cols):
        x = 0.05 + c * (cw + gap)
        ph = len(chunk) * lh + 0.3
        s.box(x, h - 0.05 - ph, cw, ph, '', fill=INK, edge=INK, r=0.08, z=2)
        for k, l in enumerate(chunk):
            idx = c * per_col + k
            yc = h - 0.05 - 0.15 - (k + 0.5) * lh
            if (idx + 1) in gold:
                s.rect(x + 0.05, yc - lh / 2, cw - 0.1, lh, fill=GOLD, edge=GOLD, lw=0, z=3)
            s.text(x + 0.15, yc, f'{idx + 1:>2}  {l}', size=size, color=INK if (idx + 1) in gold else PAPER, mono=True, ha='left', z=6)
    return s


# ------------------------------------------------------------------ a drawn web app
@fig('x_dl_app')
def dl_app(w, h, url='', title='', caption='', inputs=(), button='', result_label='', result_value='', **_):
    """inputs: list of (label, value, kind) with kind 'number' or 'slider' (value is a string; for sliders also 'frac' 0..1 in a 4th item)."""
    s = Scene(w, h)
    s.box(0.05, 0.05, w - 0.1, h - 0.1, '', fill=PAPER, edge=INK, lw=2.2, r=0.08)
    s.box(0.05, h - 0.62, w - 0.1, 0.57, '', fill=PALE, edge=INK, lw=2.2, r=0.08)
    for k, col in enumerate((RED, GOLD, GREY)):
        s.circle(0.4 + k * 0.3, h - 0.335, 0.09, fill=col, edge=INK, lw=1.2, z=4)
    s.box(1.45, h - 0.55, w - 1.7, 0.43, url, size=15, fill=PAPER, edge=INK, lw=1.4, r=0.05, mono=True, ha='left', pad=0.15)
    s.text(0.3, h - 1.0, title, size=24, weight='bold', ha='left')
    s.text(0.3, h - 1.42, caption, size=15, color=MUTE, ha='left')
    y = h - 2.0
    cx0, colw = 2.0, 3.0
    for it in inputs:
        label, value, kind = it[0], it[1], it[2]
        s.text(0.3, y, label, size=15, ha='left', color=BODY)
        if kind == 'number':
            s.box(cx0, y - 0.21, colw, 0.42, value, size=16, fill=PAPER, edge=INK, lw=1.4, r=0.04, ha='left', pad=0.12)
            s.text(cx0 + colw - 0.12, y, '- +', size=15, color=MUTE, ha='right')
        else:
            frac = it[3]
            s.line(cx0, y, cx0 + colw, y, color=HAIR, lw=4)
            s.line(cx0, y, cx0 + colw * frac, y, color=RED, lw=4)
            s.circle(cx0 + colw * frac, y, 0.13, fill=RED, edge=INK, lw=1.2, z=4)
            s.text(cx0 + colw + 0.15, y, value, size=15, weight='bold', ha='left')
        y -= 0.65
    s.box(0.3, y - 0.2, 2.6, 0.5, button, size=16, fill=PAPER, edge=INK, lw=2.0, r=0.06, weight='bold')
    rx = 5.35
    s.line(rx - 0.2, h - 1.7, rx - 0.2, 0.3, color=HAIR, lw=1.6)
    s.text(rx, h - 2.3, result_label, size=17, color=BODY, ha='left')
    s.text(rx, h - 3.0, result_value, size=44, weight='bold', ha='left')
    return s


# ------------------------------------------------------------------ monthly line chart with a training window
@fig('x_dl_drift')
def dl_drift(w, h, labels=(), real=(), shifted=(), train_n=24, ymin=500, ymax=800, ytick=100, ylabel='', real_label='', shift_label='', train_label='', alert='', **_):
    s = Scene(w, h)
    x0, x1 = 1.25, w - 0.25
    y0, y1 = 0.85, h - 0.55
    n = len(real)

    def px(i):
        return x0 + (x1 - x0) * i / (n - 1)

    def py(v):
        return y0 + (y1 - y0) * (v - ymin) / (ymax - ymin)
    s.ax.add_patch(Rectangle((px(0), y0), px(train_n - 1) - px(0), y1 - y0, fc=PALE, ec='none', zorder=0))
    s.text((px(0) + px(train_n - 1)) / 2, y1 - 0.2, train_label, size=16, weight='bold', color=BODY)
    v = ymin
    while v <= ymax:
        s.line(x0, py(v), x1, py(v), color=HAIR, lw=1.0, z=0.5)
        s.text(x0 - 0.12, py(v), f'{v:,}', size=15, color=MUTE, ha='right')
        v += ytick
    s.line(x0, y0, x1, y0, color=INK, lw=2)
    s.line(x0, y0, x0, y1, color=INK, lw=2)
    for i in range(0, n, 6):
        s.text(px(i), y0 - 0.25, labels[i], size=15, color=MUTE)
    s.text(0.1, y1 + 0.28, ylabel, size=15, color=BODY, ha='left')
    # real line
    s.ax.plot([px(i) for i in range(n)], [py(v) for v in real], color=INK, lw=3.2, zorder=4, solid_capstyle='round')
    # hypothetical
    if shifted:
        a = train_n
        s.ax.plot([px(i) for i in range(a - 1, n)], [py(real[a - 1])] + [py(v) for v in shifted[a:]], color=RED, lw=3.2, ls='--', zorder=5)
        s.line(px(a - 0.5), y0, px(a - 0.5), y1 - 0.45, color=RED, lw=2, dash=True, z=3)
        s.text(px(a - 0.5) + 0.12, py(530), alert, size=16, weight='bold', color=RED, ha='left')
    # legend
    lx, ly = x0 + 0.1, y0 + 0.28
    s.line(lx, ly + 0.28, lx + 0.5, ly + 0.28, color=INK, lw=3.2, z=5)
    s.text(lx + 0.6, ly + 0.28, real_label, size=15, ha='left')
    if shifted:
        s.line(lx, ly, lx + 0.5, ly, color=RED, lw=3.2, dash=True, z=5)
        s.text(lx + 0.6, ly, shift_label, size=15, ha='left')
    return s


# ------------------------------------------------------------------ grouped horizontal bars
@fig('x_dl_groupbars')
def dl_groupbars(w, h, groups=(), series=(), maxv=100.0, unit='%', ref=None, ref_label='', size=17, lab_w=3.0, **_):
    """groups: list of (label, [value per series]); series: list of names (gold, then ink). ref: a reference value drawn as a dashed line."""
    s = Scene(w, h)
    n, k = len(groups), len(series)
    top = h - (0.45 if k > 1 else 0.15)
    row = (top - 0.5) / n
    bx0 = lab_w + 0.1
    bw_max = w - bx0 - 0.9
    fills = [GOLD, INK, PAPER]
    if k > 1:
        lx = bx0
        for j, nm in enumerate(series):
            s.rect(lx, h - 0.3, 0.3, 0.22, fill=fills[j], edge=INK, lw=1.4)
            s.text(lx + 0.4, h - 0.19, nm, size=15, ha='left')
            lx += 0.4 + tw(nm, 15) + 0.4
    bh = min(0.42, row * 0.78 / k)
    for i, (lab, vals) in enumerate(groups):
        yc = top - (i + 0.5) * row
        wtext(s, lab_w, yc, lab_w - 0.1, lab, size, 'bold' if k > 1 else 'normal', ha='right')
        for j, v in enumerate(vals):
            yb = yc + (k / 2 - j - 1) * bh
            bw = max(0.03, bw_max * v / maxv)
            s.rect(bx0, yb, bw, bh * 0.9, fill=fills[j], edge=INK, lw=1.6, z=3)
            s.text(bx0 + bw + 0.1, yb + bh * 0.45, f'{v:.1f}{unit}', size=15, weight='bold', ha='left')
    s.line(bx0, 0.45, bx0, top, color=INK, lw=2)
    if ref is not None:
        rx = bx0 + bw_max * ref / maxv
        s.line(rx, 0.45, rx, top, color=RED, lw=2, dash=True, z=2)
        s.text(rx, 0.22, ref_label, size=15, color=RED, weight='bold')
    return s


# ------------------------------------------------------------------ a bar split into parts
@fig('x_dl_segments')
def dl_segments(w, h, parts=(), total_label='', **_):
    """parts: (name, value, unit word). Widths follow the values."""
    s = Scene(w, h)
    tot = sum(v for _, v, _u in parts)
    x = 0.05
    W = w - 0.1
    bh = 1.5
    y = (h - bh) / 2 + 0.2
    for i, (nm, v, u) in enumerate(parts):
        bw = W * v / tot
        s.box(x, y, bw, bh, '', fill=GOLD if i == 2 else PAPER, edge=INK, lw=2.0, r=0.05)
        wtext(s, x + bw / 2, y + bh * 0.62, bw - 0.12, nm, 17, 'bold', ha='center')
        s.text(x + bw / 2, y + bh * 0.2, f'{v} {u}', size=16, color=BODY)
        x += bw
    s.brace(0.05, 0.05 + W, y - 0.2, depth=0.22, up=False)
    s.text(w / 2, y - 0.75, total_label, size=18, weight='bold')
    return s
