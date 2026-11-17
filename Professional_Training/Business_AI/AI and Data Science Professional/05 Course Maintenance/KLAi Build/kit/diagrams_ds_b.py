"""Figure kinds for Sessions 1, 3 and 4 (author letter b). Registered as x_<kind>; used as visual=dict(kind='<kind>', ...).

  dsb_nested     artificial intelligence, machine learning and deep learning as nested circles, with data science as a way of working
  dsb_notebook   the parts of a Colab notebook: text cell, code cell with its play button, and the output under it
  dsb_hist       one histogram from bin counts, with labelled vertical lines (mean, median, mode)
  dsb_panels     two to three histograms side by side on the same scale (shapes, sample sizes)
  dsb_box        a horizontal box plot with quartiles, the IQR fence and outlier dots
  dsb_groupby    a few records, an arrow labelled GROUP BY, and the grouped result
  dsb_charts     four small real charts (bar, line, histogram, scatter) each with the question it answers
  dsb_axis       the same bars on a truncated axis and on a zero axis
  dsb_line       a line chart over time with the axis starting at zero
  dsb_settle     a running share that settles as more orders are counted
  dsb_popsample  population, random sample and the statistic computed from it
  dsb_scatters   one to three scatter plots with their Pearson r
  dsb_confound   a confounder drawn as a triangle: it lifts two variables that then look linked
All text is 14 pt or larger and every figure is audited for overlaps by figkit.
"""
from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, PALE, fig
import slidekit as K
from matplotlib.patches import Circle

BAR = '#CFCFCF'


def tw(t, size, kind='regular'):
    return K.width_in(str(t), size, kind)


def wrap_text(s, x, y, w, text, size, weight='normal', color=INK, ha='left', va='center', italic=False):
    """Wrapped text in a column of width w centred on y (va centre) or starting at y (va top). Returns its height."""
    lines = K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', w)
    s.text(x, y, '\n'.join(lines), size=size, weight=weight, color=color, ha=ha, va=va, italic=italic)
    return len(lines) * size * 1.15 / 72


def grid(s, x, ytop, headers, rows, size=15, rh=0.38, hl=None, pad=0.26, colw=None):
    colw = colw or [max([tw(headers[c], size, 'bold')] + [tw(r[c], size) for r in rows]) + pad for c in range(len(headers))]
    cells = {(0, c): PALE for c in range(len(headers))}
    if hl:
        cells.update(hl)
    s.table(x, ytop, colw, rh, [list(headers)] + [list(r) for r in rows], header=True, size=size, align=['left'] * len(headers), hl_cells=cells)
    return colw, ytop - (len(rows) + 1) * rh


def _fmt(v):
    return f'{v:,.0f}'


# ------------------------------------------------------------------ AI, ML, DL nested
@fig('x_dsb_nested')
def dsb_nested(w, h, items=(), data_science='', **_):
    """items: three (name, example) from the outside in: artificial intelligence, machine learning, deep learning."""
    s = Scene(w, h)
    d = h - 0.2
    cx0 = 0.1 + d / 2
    base = 0.1
    radii = [d / 2, d / 2 * 0.70, d / 2 * 0.40]
    for r, f in zip(radii, [PAPER, PALE, GOLD]):
        s.ax.add_patch(Circle((cx0, base + r), r, fc=f, ec=INK, lw=2.2, zorder=2))
    short = ['Artificial intelligence', 'Machine learning', 'Deep learning']
    ys = []
    for i, r in enumerate(radii):
        yy = base + 2 * r - (0.5 if i == 0 else 0.42) if i < 2 else base + r
        ys.append(yy)
        s.text(cx0, yy, short[i], size=16 if i < 2 else 15, weight='bold', z=6)
    x0 = 0.1 + d + 0.6
    tw_ = w - x0 - 0.1
    ylev = [h - 0.25, h - 1.2, h - 2.15]
    for i, (nm, ex) in enumerate(items):
        yy = ylev[i]
        hh = wrap_text(s, x0, yy, tw_, nm, 16, 'bold', va='top')
        wrap_text(s, x0, yy - hh - 0.02, tw_, ex, 15, color=BODY, va='top')
        s.line(cx0 + (radii[i] * 0.6 if i < 2 else radii[i] * 0.55), ys[i] if i < 2 else ys[i] + 0.1, x0 - 0.12, yy - 0.12, color=GREY, lw=1.4, z=1)
    if data_science:
        s.box(x0 - 0.05, 0.12, tw_ + 0.05, 1.0, '', fill=GOLD, edge=INK, lw=1.8, r=0.06)
        wrap_text(s, x0 + 0.1, 0.62, tw_ - 0.2, data_science, 15, 'bold')
    return s


# ------------------------------------------------------------------ a notebook: text cell, code cell, output
@fig('x_dsb_notebook')
def dsb_notebook(w, h, title='', text_cell='', code=(), output=(), labels=(), **_):
    s = Scene(w, h)
    lw_ = w * 0.62
    x0 = 0.1
    s.box(x0, 0.1, lw_, h - 0.2, '', fill=PAPER, edge=INK, lw=2.0, r=0.05)
    s.rect(x0, h - 0.7, lw_, 0.6, fill=INK, edge=INK, lw=0, z=3)
    s.text(x0 + 0.25, h - 0.4, title, size=16, weight='bold', color=PAPER, ha='left', z=6)
    y = h - 1.0
    hh = wrap_text(s, x0 + 0.3, y, lw_ - 0.6, text_cell, 16, 'bold', va='top')
    ytext = y - hh
    ct = ytext - 0.35
    ch = len(code) * 0.32 + 0.25
    s.box(x0 + 0.95, ct - ch, lw_ - 1.2, ch, '', fill=PALE, edge=GREY, lw=1.4, r=0.04)
    cyc = ct - ch / 2
    s.circle(x0 + 0.5, cyc, 0.24, fill=INK, edge=INK, lw=1.4, z=4)
    s.poly([(x0 + 0.43, cyc + 0.12), (x0 + 0.43, cyc - 0.12), (x0 + 0.62, cyc)], fill=PAPER, edge=PAPER, lw=0.5, z=5)
    for i, ln in enumerate(code):
        s.text(x0 + 1.1, ct - 0.25 - i * 0.32, ln, size=14, mono=True, ha='left', z=6)
    ot = ct - ch - 0.25
    s.text(x0 + 0.95, ot, 'Output', size=14, color=MUTE, ha='left', weight='bold')
    for i, ln in enumerate(output):
        s.text(x0 + 1.1, ot - 0.38 - i * 0.32, ln, size=14, mono=True, ha='left', z=6)
    lx = x0 + lw_ + 0.5
    anchors = [ytext + 0.05, cyc, ot - 0.38]
    for k, (lab, ay) in enumerate(zip(labels, anchors)):
        yy = ay
        s.circle(lx + 0.2, yy, 0.2, fill=GOLD, edge=INK, lw=1.6, z=5)
        s.text(lx + 0.2, yy, str(k + 1), size=14, weight='bold', z=6)
        s.arrow(lx - 0.02, yy, x0 + lw_ + 0.05, yy, color=RED, lw=2.0, head=12, z=4)
        wrap_text(s, lx + 0.55, yy, w - lx - 0.65, lab, 15, va='center')
    return s


# ------------------------------------------------------------------ histogram
def _label_levels(items, px, lo, hi, size=14):
    placed, out = [], []
    for xv, t in items:
        cx = px(xv)
        wd = tw(t, size, 'bold') + 0.15
        a, b = max(lo, cx - wd / 2), min(hi, cx + wd / 2)
        lv = 0
        while any(l == lv and not (b < p0 - 0.05 or a > p1 + 0.05) for l, p0, p1 in placed):
            lv += 1
        placed.append((lv, a, b))
        out.append(lv)
    return out


def _hist(s, x, y, w, h, d):
    edges, counts = d['edges'], d['counts']
    lines = sorted(d.get('lines', []), key=lambda l: l['x'])
    title = d.get('title', '')
    ml = 0.95 if d.get('ylabel') else 0.7
    mb = 0.62 + (0.32 if d.get('xlabel') else 0)
    px0, px1 = x + ml, x + w - 0.5
    lo, hi = edges[0], edges[-1]
    px = lambda v: px0 + (v - lo) / (hi - lo) * (px1 - px0)
    lv = _label_levels([(l['x'], l['label']) for l in lines], px, px0, px1) if lines else []
    nlev = (max(lv) + 1) if lv else 0
    mt = (0.45 if title else 0.1) + nlev * 0.3 + (0.12 if nlev else 0)
    py0, py1 = y + mb, y + h - mt
    ymax = d.get('ymax') or max(counts)
    py = lambda v: py0 + v / ymax * (py1 - py0)
    if title:
        s.text(x + 0.05, y + h - 0.2, title, size=16, weight='bold', ha='left')
    hl = set(d.get('hl', []))
    for i, c in enumerate(counts):
        if c <= 0:
            continue
        s.rect(px(edges[i]), py0, px(edges[i + 1]) - px(edges[i]), py(c) - py0, fill=GOLD if i in hl else BAR, edge=INK, lw=0.8, z=2)
    s.line(px0, py0, px1, py0, color=INK, lw=2, z=4)
    s.line(px0, py0, px0, py1, color=INK, lw=2, z=4)
    for v, lab in d.get('xticks', []):
        s.line(px(v), py0, px(v), py0 - 0.07, color=INK, lw=1.6, z=4)
        s.text(px(v), py0 - 0.26, lab, size=14, color=BODY)
    for v, lab in (d.get('yticks') or [(0, '0'), (ymax, _fmt(ymax))]):
        s.text(px0 - 0.1, py(v), lab, size=14, color=BODY, ha='right')
    if d.get('xlabel'):
        s.text((px0 + px1) / 2, y + 0.18, d['xlabel'], size=15, color=MUTE)
    if d.get('ylabel'):
        s.text(x + 0.17, (py0 + py1) / 2, d['ylabel'], size=14, color=MUTE, rot=90)
    for l, lev in zip(lines, lv):
        topy = py1 + 0.1 + lev * 0.3
        s.line(px(l['x']), py0, px(l['x']), topy, color=l.get('color', RED), lw=3.2, z=5)
        wd = tw(l['label'], 14, 'bold') + 0.15
        cx = min(max(px(l['x']), px0 + wd / 2), px1 - wd / 2)
        s.text(cx, topy + 0.17, l['label'], size=14, weight='bold', color=l.get('tcolor', l.get('color', RED)), z=6)
    for k, t in enumerate(d.get('note', [])):
        if d.get('note_left'):
            s.text(px0 + 0.15, py1 - 0.2 - k * 0.27, t, size=14, color=BODY, ha='left', z=6)
        else:
            s.text(px1 - 0.1, py1 - 0.2 - k * 0.27, t, size=14, color=BODY, ha='right', z=6)


@fig('x_dsb_hist')
def dsb_hist(w, h, **d):
    s = Scene(w, h)
    _hist(s, 0.05, 0.05, w - 0.1, h - 0.1, d)
    return s


@fig('x_dsb_panels')
def dsb_panels(w, h, panels=(), **_):
    s = Scene(w, h)
    n = len(panels)
    gap = 0.15
    pw = (w - 0.1 - gap * (n - 1)) / n
    for i, p in enumerate(panels):
        _hist(s, 0.05 + i * (pw + gap), 0.05, pw, h - 0.1, p)
    return s


# ------------------------------------------------------------------ box plot
@fig('x_dsb_box')
def dsb_box(w, h, q1=0, med=0, q3=0, whisker_lo=0, whisker_hi=0, fence=0, fence_label='', outliers=(), axis_max=0, ticks=(), xlabel='', labels=(), off='', **_):
    """labels: [{x, text, side: 'above'|'below', level: 0|1, color}] with x in data units."""
    s = Scene(w, h)
    px0, px1 = 0.6, w - 0.6
    px = lambda v: px0 + v / axis_max * (px1 - px0)
    ay = 1.0
    s.line(px0, ay, px1, ay, color=INK, lw=2, z=3)
    for v, lab in ticks:
        s.line(px(v), ay, px(v), ay - 0.07, color=INK, lw=1.6)
        s.text(px(v), ay - 0.28, lab, size=14, color=BODY)
    s.text((px0 + px1) / 2, 0.2, xlabel, size=15, color=MUTE)
    cy, bh = ay + 1.05, 0.8
    s.rect(px(q1), cy - bh / 2, px(q3) - px(q1), bh, fill=GOLD, edge=INK, lw=2.4, z=3)
    s.line(px(med), cy - bh / 2, px(med), cy + bh / 2, color=INK, lw=4, z=5)
    s.line(px(whisker_lo), cy, px(q1), cy, color=INK, lw=2.4, z=3)
    s.line(px(q3), cy, px(whisker_hi), cy, color=INK, lw=2.4, z=3)
    for v in (whisker_lo, whisker_hi):
        s.line(px(v), cy - 0.22, px(v), cy + 0.22, color=INK, lw=2.4, z=3)
    s.line(px(fence), ay + 0.05, px(fence), h - 0.4, color=RED, lw=2.0, dash=True, z=2)
    if fence_label:
        s.text(px(fence) + 0.1, h - 0.22, fence_label, size=14, weight='bold', color=RED, ha='left')
    for i, v in enumerate(outliers):
        yy = cy + (0.0 if i % 3 == 0 else (0.2 if i % 3 == 1 else -0.2))
        s.circle(px(v), yy, 0.07, fill=PAPER, edge=INK, lw=1.6, z=4)
    if off:
        s.arrow(px1 - 0.9, cy - 0.55, px1 - 0.05, cy - 0.55, color=RED, lw=2.2, head=14)
        s.text(px1 + 0.3, cy - 0.85, off, size=14, color=RED, weight='bold', ha='right')
    for lb in labels:
        above = lb['side'] == 'above'
        lev = lb.get('level', 0)
        ly = cy + bh / 2 + 0.42 + lev * 0.34 if above else cy - bh / 2 - 0.42 - lev * 0.34
        yy0 = cy + bh / 2 if above else cy - bh / 2
        xx = px(lb['x'])
        s.line(xx, yy0, xx, ly - 0.14 if above else ly + 0.14, color=lb.get('color', INK), lw=1.4, z=2)
        s.text(xx, ly, lb['text'], size=14, weight='bold', color=lb.get('color', INK), ha=lb.get('ha', 'center'), z=6)
    return s


# ------------------------------------------------------------------ group by
@fig('x_dsb_groupby')
def dsb_groupby(w, h, records=(), rec_headers=(), more='', result=(), res_headers=(), op='', **_):
    s = Scene(w, h)
    size, rh = 15, 0.36
    s.text(0.1, h - 0.22, 'Records in the orders tab', size=16, weight='bold', ha='left')
    colw, yb = grid(s, 0.1, h - 0.5, rec_headers, records, size=size, rh=rh, hl={(i + 1, 1): GOLD for i in range(len(records))})
    s.text(0.1, yb - 0.2, more, size=14, color=MUTE, ha='left', italic=True)
    xl = 0.1 + sum(colw)
    rcw = [max([tw(res_headers[c], size, 'bold')] + [tw(r[c], size) for r in result]) + 0.26 for c in range(len(res_headers))]
    xr = w - 0.1 - sum(rcw)
    s.text(xr, h - 0.22, 'Result: one record per branch', size=16, weight='bold', ha='left')
    grid(s, xr, h - 0.5, res_headers, result, size=size, rh=rh, colw=rcw, hl={(i + 1, 0): GOLD for i in range(len(result))})
    ym = h - 0.5 - (len(records) + 1) * rh / 2
    x1, x2 = xl + 0.2, xr - 0.2
    s.arrow(x1, ym, x2, ym, color=RED, lw=3, head=20)
    wrap_text(s, (x1 + x2) / 2, ym + 0.22, x2 - x1 - 0.1, 'GROUP BY branch_id', 16, 'bold', color=RED, ha='center', va='bottom')
    wrap_text(s, (x1 + x2) / 2, ym - 0.12, x2 - x1 - 0.1, op, 14, color=BODY, ha='center', va='top')
    return s


# ------------------------------------------------------------------ four small real charts
@fig('x_dsb_charts')
def dsb_charts(w, h, bars=None, line=None, hist=None, scatter=None, captions=(), **_):
    s = Scene(w, h)
    n = 4
    gap = 0.3
    pw = (w - 0.1 - gap * (n - 1)) / n
    ph = h - 1.85
    y0 = h - 0.1 - ph
    for i in range(n):
        x = 0.05 + i * (pw + gap)
        s.rect(x, y0, pw, ph, fill=PAPER, edge=HAIR, lw=1.4, z=1)
        head, sub = captions[i]
        hh = wrap_text(s, x, y0 - 0.1, pw, head, 17, 'bold', va='top')
        wrap_text(s, x, y0 - 0.1 - hh - 0.06, pw, sub, 15, color=BODY, va='top')
    # bars
    x = 0.05
    vals = bars['values']
    mx = max(vals)
    bw = (pw - 0.5) / len(vals)
    for i, v in enumerate(vals):
        s.rect(x + 0.25 + i * bw + 0.02, y0 + 0.25, bw - 0.04, v / mx * (ph - 0.5), fill=GOLD if i in bars.get('hl', ()) else BAR, edge=INK, lw=1.0, z=2)
    s.line(x + 0.25, y0 + 0.25, x + pw - 0.25, y0 + 0.25, color=INK, lw=2)
    # line
    x = 0.05 + (pw + gap)
    vals = line['values']
    mx = max(vals)
    lx0, lx1, ly0, ly1 = x + 0.25, x + pw - 0.25, y0 + 0.25, y0 + ph - 0.25
    pts = [(lx0 + i / (len(vals) - 1) * (lx1 - lx0), ly0 + v / mx * (ly1 - ly0)) for i, v in enumerate(vals)]
    s.line(lx0, ly0, lx1, ly0, color=INK, lw=2)
    s.line(lx0, ly0, lx0, ly1, color=INK, lw=2)
    for a, b in zip(pts, pts[1:]):
        s.line(a[0], a[1], b[0], b[1], color=INK, lw=2.4, z=3)
    # histogram
    x = 0.05 + 2 * (pw + gap)
    cs = hist['counts']
    mx = max(cs)
    bw = (pw - 0.5) / len(cs)
    for i, c in enumerate(cs):
        s.rect(x + 0.25 + i * bw, y0 + 0.25, bw, c / mx * (ph - 0.5), fill=BAR, edge=INK, lw=0.8, z=2)
    s.line(x + 0.25, y0 + 0.25, x + pw - 0.25, y0 + 0.25, color=INK, lw=2)
    # scatter
    x = 0.05 + 3 * (pw + gap)
    pts = scatter['points']
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    sx0, sx1, sy0, sy1 = x + 0.3, x + pw - 0.2, y0 + 0.3, y0 + ph - 0.2
    for a, b in pts:
        s.circle(sx0 + (a - min(xs)) / (max(xs) - min(xs)) * (sx1 - sx0), sy0 + (b - min(ys)) / (max(ys) - min(ys)) * (sy1 - sy0), 0.03, fill=INK, edge=INK, lw=0.4, z=3)
    s.line(sx0 - 0.05, sy0 - 0.05, sx1, sy0 - 0.05, color=INK, lw=2)
    s.line(sx0 - 0.05, sy0 - 0.05, sx0 - 0.05, sy1, color=INK, lw=2)
    return s


# ------------------------------------------------------------------ truncated axis against zero axis
@fig('x_dsb_axis')
def dsb_axis(w, h, values=(), labels=(), base=20000, ymax=30000, left_note='', right_note='', hl=(), **_):
    s = Scene(w, h)
    pw = (w - 0.4) / 2
    n = len(values)
    for k, (lo, title, note) in enumerate(((base, f'Axis starts at {_fmt(base)}', left_note), (0, 'Axis starts at 0', right_note))):
        x0 = 0.1 + k * (pw + 0.4)
        s.text(x0 + 0.05, h - 0.2, title, size=17, weight='bold', ha='left', color=RED if k == 0 else INK)
        ax0, ax1 = x0 + 0.95, x0 + pw - 0.1
        ay0, ay1 = 0.75, h - 1.2
        scale = (ay1 - ay0) / (ymax - lo)
        s.line(ax0, ay0, ax1, ay0, color=INK, lw=2, z=4)
        s.line(ax0, ay0, ax0, ay1, color=INK, lw=2, z=4)
        for v in (lo, ymax):
            s.text(ax0 - 0.1, ay0 + (v - lo) * scale, _fmt(v), size=14, ha='right', color=BODY)
        bw = (ax1 - ax0) / n
        for i, v in enumerate(values):
            s.rect(ax0 + i * bw + 0.05, ay0, bw - 0.1, (v - lo) * scale, fill=GOLD if i in hl else BAR, edge=INK, lw=1.2, z=2)
            s.text(ax0 + i * bw + bw / 2, ay0 - 0.25, labels[i], size=14, color=BODY)
        wrap_text(s, x0 + 0.05, h - 0.5, pw - 0.1, note, 15, color=BODY, va='top')
    return s


# ------------------------------------------------------------------ line chart over time
@fig('x_dsb_line')
def dsb_line(w, h, values=(), xticks=(), ylabel='', yticks=(), hl=None, hl_label='', **_):
    s = Scene(w, h)
    px0, px1 = 1.05, w - 0.35
    py0, py1 = 0.8, h - 0.45
    mx = yticks[-1][0]
    n = len(values)
    px = lambda i: px0 + i / (n - 1) * (px1 - px0)
    py = lambda v: py0 + v / mx * (py1 - py0)
    s.line(px0, py0, px1, py0, color=INK, lw=2, z=4)
    s.line(px0, py0, px0, py1, color=INK, lw=2, z=4)
    for v, lab in yticks:
        s.text(px0 - 0.1, py(v), lab, size=14, ha='right', color=BODY)
        if v:
            s.line(px0, py(v), px1, py(v), color=HAIR, lw=1.0, z=1)
    for i, lab in xticks:
        s.line(px(i), py0, px(i), py0 - 0.07, color=INK, lw=1.6)
        s.text(px(i), py0 - 0.27, lab, size=14, color=BODY)
    s.text(0.3, (py0 + py1) / 2, ylabel, size=14, color=MUTE, rot=90)
    for i in range(n - 1):
        s.line(px(i), py(values[i]), px(i + 1), py(values[i + 1]), color=INK, lw=2.8, z=3)
    for i, v in enumerate(values):
        s.circle(px(i), py(v), 0.06, fill=GOLD if i == hl else PAPER, edge=INK, lw=1.4, z=5)
    if hl is not None:
        s.text(px(hl), py(values[hl]) + 0.3, hl_label, size=15, weight='bold', z=6)
    return s


# ------------------------------------------------------------------ a share that settles
@fig('x_dsb_settle')
def dsb_settle(w, h, points=(), final=0.0, final_label='', xticks=(), yticks=(), xlabel='', ylabel='', **_):
    s = Scene(w, h)
    px0, px1 = 1.0, w - 0.3
    py0, py1 = 0.95, h - 0.4
    xmax = max(p[0] for p in points)
    ymax = yticks[-1][0]
    px = lambda v: px0 + v / xmax * (px1 - px0)
    py = lambda v: py0 + v / ymax * (py1 - py0)
    s.line(px0, py0, px1, py0, color=INK, lw=2, z=4)
    s.line(px0, py0, px0, py1, color=INK, lw=2, z=4)
    for v, lab in xticks:
        s.line(px(v), py0, px(v), py0 - 0.07, color=INK, lw=1.6)
        s.text(px(v), py0 - 0.26, lab, size=14, color=BODY)
    for v, lab in yticks:
        s.text(px0 - 0.1, py(v), lab, size=14, ha='right', color=BODY)
    s.text((px0 + px1) / 2, 0.2, xlabel, size=15, color=MUTE)
    s.text(0.25, (py0 + py1) / 2, ylabel, size=14, color=MUTE, rot=90)
    s.ax.plot([px(0), px1], [py(final), py(final)], color=RED, lw=2.2, ls='--', zorder=3)
    s.ax.plot([px(p[0]) for p in points], [py(p[1]) for p in points], color=INK, lw=2.6, zorder=4)
    s.text(px1 - 0.05, py(final) + 0.32, final_label, size=15, weight='bold', color=RED, ha='right', z=6)
    return s


# ------------------------------------------------------------------ population, sample, statistic
@fig('x_dsb_popsample')
def dsb_popsample(w, h, pop_title='', pop_text='', sample_title='', sample_text='', arrow_text='', foot='', picked=(), **_):
    s = Scene(w, h)
    pw = w * 0.5
    ph = h - 1.15
    y0 = 1.0
    s.box(0.1, y0, pw, ph, '', fill=PAPER, edge=INK, lw=2.2, r=0.07)
    s.text(0.3, y0 + ph - 0.3, pop_title, size=17, weight='bold', ha='left')
    wrap_text(s, 0.3, y0 + ph - 0.58, pw - 0.4, pop_text, 15, color=BODY, va='top')
    cols, rows = 24, 7
    gx0, gx1 = 0.35, pw - 0.15
    gy0, gy1 = y0 + 0.2, y0 + 1.5
    for r in range(rows):
        for c in range(cols):
            on = (r * cols + c) in picked
            s.circle(gx0 + (c + 0.5) * (gx1 - gx0) / cols, gy0 + (r + 0.5) * (gy1 - gy0) / rows, 0.055, fill=GOLD if on else BAR, edge=INK if on else GREY, lw=1.0 if on else 0.6, z=3)
    sx = 0.1 + pw + 1.25
    sw = w - sx - 0.1
    s.box(sx, y0 + ph * 0.12, sw, ph * 0.76, '', fill=GOLD, edge=INK, lw=2.2, r=0.07)
    s.text(sx + 0.2, y0 + ph * 0.88 - 0.3, sample_title, size=17, weight='bold', ha='left')
    wrap_text(s, sx + 0.2, y0 + ph * 0.88 - 0.6, sw - 0.4, sample_text, 15, va='top')
    ym = y0 + ph * 0.5
    s.arrow(0.1 + pw + 0.06, ym, sx - 0.06, ym, color=RED, lw=3, head=20)
    wrap_text(s, 0.1 + pw + 0.65, ym + 0.15, 1.1, arrow_text, 14, color=RED, weight='bold', ha='center', va='bottom')
    s.box(0.1, 0.1, w - 0.2, 0.7, '', fill=PAPER, edge=INK, lw=1.6, r=0.05)
    wrap_text(s, w / 2, 0.45, w - 0.5, foot, 16, 'bold', ha='center')
    return s


# ------------------------------------------------------------------ scatter plots with r
def _scatter(s, x, y, w, h, d):
    pts = d['points']
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    lo_x, hi_x = d.get('xlim', (min(xs), max(xs)))
    lo_y, hi_y = d.get('ylim', (min(ys), max(ys)))
    ml, mb, mt = 0.95, 0.85, 0.75
    px0, px1, py0, py1 = x + ml, x + w - 0.2, y + mb, y + h - mt
    px = lambda v: px0 + (v - lo_x) / (hi_x - lo_x) * (px1 - px0)
    py = lambda v: py0 + (v - lo_y) / (hi_y - lo_y) * (py1 - py0)
    s.text(x + 0.05, y + h - 0.2, d['title'], size=16, weight='bold', ha='left')
    if d.get('sub'):
        s.text(x + 0.05, y + h - 0.52, d['sub'], size=15, color=RED, weight='bold', ha='left')
    s.line(px0, py0, px1, py0, color=INK, lw=2, z=4)
    s.line(px0, py0, px0, py1, color=INK, lw=2, z=4)
    for v, lab in d.get('xticks', []):
        s.text(px(v), py0 - 0.25, lab, size=14, color=BODY)
    for v, lab in d.get('yticks', []):
        s.text(px0 - 0.1, py(v), lab, size=14, color=BODY, ha='right')
    s.text((px0 + px1) / 2, y + 0.17, d['xlabel'], size=14, color=MUTE)
    s.text(x + 0.15, (py0 + py1) / 2, d['ylabel'], size=14, color=MUTE, rot=90)
    for a, b in pts:
        s.circle(px(a), py(b), d.get('dot', 0.035), fill=INK, edge=INK, lw=0.3, z=3)
    if d.get('line'):
        b0, b1 = d['line']
        s.ax.plot([px(lo_x), px(hi_x)], [py(b0 + b1 * lo_x), py(b0 + b1 * hi_x)], color=RED, lw=2.6, zorder=5)
    for v in d.get('mark', []):
        s.circle(px(v[0]), py(v[1]), 0.1, fill=GOLD, edge=INK, lw=1.8, z=6)


@fig('x_dsb_scatters')
def dsb_scatters(w, h, panels=(), **_):
    s = Scene(w, h)
    n = len(panels)
    gap = 0.15
    pw = (w - 0.1 - gap * (n - 1)) / n
    for i, p in enumerate(panels):
        _scatter(s, 0.05 + i * (pw + gap), 0.05, pw, h - 0.1, p)
    return s


# ------------------------------------------------------------------ a confounder
@fig('x_dsb_confound')
def dsb_confound(w, h, top=None, left=None, right=None, middle='', foot='', **_):
    """top, left, right: {head, text}."""
    s = Scene(w, h)
    bw, bh = 3.0, 1.25

    def node(cx, cy, d, fill):
        s.box(cx - bw / 2, cy - bh / 2, bw, bh, '', fill=fill, edge=INK, lw=2.2, r=0.07)
        s.text(cx, cy + 0.38, d['head'], size=17, weight='bold', z=6)
        wrap_text(s, cx, cy + 0.15, bw - 0.3, d['text'], 14, color=BODY, ha='center', va='top')
    tx, ty = w / 2, h - 0.15 - bh / 2
    lx, rx, by = 0.1 + bw / 2, w - 0.1 - bw / 2, 1.6 + bh / 2
    node(tx, ty, top, GOLD)
    node(lx, by, left, PAPER)
    node(rx, by, right, PAPER)
    s.arrow(tx - 0.8, ty - bh / 2 - 0.03, lx + 0.5, by + bh / 2 + 0.03, color=RED, lw=2.8, head=18)
    s.arrow(tx + 0.8, ty - bh / 2 - 0.03, rx - 0.5, by + bh / 2 + 0.03, color=RED, lw=2.8, head=18)
    s.line(lx + bw / 2 + 0.05, by, rx - bw / 2 - 0.05, by, color=INK, lw=2.2, dash=True)
    s.text(w / 2, by + 0.2, middle, size=16, weight='bold')
    s.box(0.1, 0.1, w - 0.2, 0.95, '', fill=PAPER, edge=INK, lw=1.6, r=0.05)
    wrap_text(s, w / 2, 0.58, w - 0.5, foot, 16, 'bold', ha='center')
    return s
