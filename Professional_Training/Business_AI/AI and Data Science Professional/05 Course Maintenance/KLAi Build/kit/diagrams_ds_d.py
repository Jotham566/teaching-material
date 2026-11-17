"""Figure kinds for Sessions 7 and 8 (pandas I and II), author letter d. Each is registered as x_<kind> and used as visual=dict(kind='<kind>', ...).

  ds_dataframe      a real excerpt of a pandas DataFrame with its index, column names, one Series outlined and its shape
  ds_console        one or more panels: code lines (dark) over their real output (grey), with red call-outs at chosen output lines
  ds_mask           boolean indexing: rows, the True/False mask built from a condition, and the rows that stay
  ds_venn           two conditions drawn as overlapping circles with the real counts, and what &, | and ~ return
  ds_loc_iloc       the same rows with a position column (iloc) and a label column (loc), with the two slice ends marked
  ds_iqr            the IQR rule on a box drawn with real quartiles, the upper fence and the largest value on a broken axis
  ds_before_after   two real grids side by side with the line of code between them
  ds_date_fork      one text date read two ways, and the real counts of what the wrong reading does
  ds_reconcile      control total minus cleaned total equals the reconciliation difference, and its explanation
All text is 14 pt or larger and every figure is audited for overlaps by figkit.
"""
from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, PALE, fig
import slidekit as K
from matplotlib.patches import Rectangle, Circle


def tw(t, size, kind='regular'):
    return K.width_in(str(t), size, kind)


def mono_w(t, size):
    return 0.602 * size / 72 * len(t)


def wrap_text(s, x, y, w, text, size, weight='normal', color=INK, ha='left', va='center', italic=False):
    lines = K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', w)
    s.text(x, y, '\n'.join(lines), size=size, weight=weight, color=color, ha=ha, va=va, italic=italic)
    return len(lines) * size * 1.15 / 72


def col_widths(headers, rows, size, pad=0.26):
    return [max([tw(headers[c], size, 'bold')] + [tw(r[c], size) for r in rows]) + pad for c in range(len(headers))]


def grid(s, x, ytop, headers, rows, size=15, rh=0.4, hl=None, colw=None, pad=0.26, head_fill=PALE):
    colw = colw or col_widths(headers, rows, size, pad)
    cells = {(0, c): head_fill for c in range(len(headers))}
    if hl:
        cells.update(hl)
    s.table(x, ytop, colw, rh, [list(headers)] + [list(r) for r in rows], header=True, size=size, align=['left'] * len(headers), hl_cells=cells)
    return colw, ytop - (len(rows) + 1) * rh


def tag(s, x, y, text, fill=GOLD, size=14, h=0.3):
    w = tw(text, size, 'bold') + 0.22
    s.box(x, y - h / 2, w, h, text, size=size, fill=fill, edge=INK, lw=1.4, weight='bold', r=0.05, z=5)
    return w


def outline(s, x, y, w, h, color=RED, lw=3.0):
    s.ax.add_patch(Rectangle((x, y), w, h, fc='none', ec=color, lw=lw, zorder=7))


# ------------------------------------------------------------------ a DataFrame
@fig('x_ds_dataframe')
def ds_dataframe(w, h, headers=(), rows=(), index=(), shape='', series_col=None, name='orders', **_):
    s = Scene(w, h)
    size, rh = 15, 0.42
    hdr = [''] + list(headers)
    body = [[str(i)] + list(r) for i, r in zip(index, rows)]
    colw = col_widths(hdr, body, size, 0.26)
    colw[0] = max(colw[0], 0.8)
    total = sum(colw)
    if total > w - 0.2:
        raise ValueError(f'ds_dataframe too wide: {total:.2f} in')
    x0, ytop = (w - total) / 2, h - 1.1
    s.text(x0, h - 0.25, f'{name}: a DataFrame, the whole table', size=17, weight='bold', ha='left')
    s.text(x0 + total, h - 0.25, f'shape: {shape}', size=17, weight='bold', ha='right', color=RED)
    hl = {(r + 1, 0): PALE for r in range(len(rows))}
    grid(s, x0, ytop, hdr, body, size=size, rh=rh, hl=hl, colw=colw)
    ybot = ytop - (len(rows) + 1) * rh
    # index
    s.text(x0 + colw[0] / 2, h - 0.62, 'index', size=16, weight='bold')
    s.arrow(x0 + colw[0] / 2, h - 0.8, x0 + colw[0] / 2, ytop - rh - 0.02, color=INK, lw=2.0, head=13)
    # column names
    cx_names = x0 + colw[0] + (total - colw[0]) / 2
    s.text(cx_names, h - 0.62, 'column names', size=16, weight='bold')
    s.arrow(cx_names, h - 0.8, cx_names, ytop - 0.02, color=INK, lw=2.0, head=13)
    # series
    if series_col is not None:
        c = list(headers).index(series_col) + 1
        sx = x0 + sum(colw[:c])
        outline(s, sx, ybot, colw[c], (len(rows) + 1) * rh, color=RED, lw=3.0)
        s.text(sx + colw[c] / 2, ybot - 0.3, f'Series: one column, {series_col}', size=16, weight='bold', color=RED)
    return s


# ------------------------------------------------------------------ code over output, with call-outs
@fig('x_ds_console')
def ds_console(w, h, panels=(), size=14, **_):
    s = Scene(w, h)
    lh = size * 1.22 / 72
    pad = 0.12
    outw = max(mono_w(l, size) for p in panels for l in p['out']) if any(p['out'] for p in panels) else 0
    codew = max(mono_w(l, size) for p in panels for l in p['code'])
    bw = max(outw, codew) + 2 * pad + 0.1
    callx = 0.1 + bw + 0.45
    callw = w - callx - 0.1
    total = sum((0.34 if p.get('title') else 0) + len(p['code']) * lh + 2 * pad + (len(p['out']) * lh + 2 * pad + 0.06 if p['out'] else 0) for p in panels) + 0.18 * (len(panels) - 1)
    if total > h:
        raise ValueError(f'ds_console too tall: {total:.2f} in > {h:.2f}')
    y = h - 0.02
    for p in panels:
        if p.get('title'):
            s.text(0.1, y - 0.15, p['title'], size=16, weight='bold', ha='left')
            y -= 0.34
        ch = len(p['code']) * lh + 2 * pad
        s.box(0.1, y - ch, bw, ch, '', fill=INK, edge=INK, r=0.06, z=2)
        for i, l in enumerate(p['code']):
            s.text(0.1 + pad, y - pad - (i + 0.5) * lh, l, size=size, color=PAPER, mono=True, ha='left', z=4)
        y -= ch
        if p['out']:
            y -= 0.06
            oh = len(p['out']) * lh + 2 * pad
            s.box(0.1, y - oh, bw, oh, '', fill=PALE, edge=INK, lw=1.2, r=0.06, z=2)
            for k in p.get('hl', []):
                s.rect(0.14, y - pad - (k + 1) * lh, bw - 0.08, lh, fill=GOLD, edge=GOLD, lw=0, z=3)
            for i, l in enumerate(p['out']):
                s.text(0.1 + pad, y - pad - (i + 0.5) * lh, l, size=size, color=INK, mono=True, ha='left', z=4)
            for k, t in p.get('notes', []):
                yy = y - pad - (k + 0.5) * lh
                s.line(0.1 + bw, yy, callx - 0.08, yy, color=RED, lw=2.0, z=5)
                s.circle(0.1 + bw, yy, 0.05, fill=RED, edge=RED, z=6)
                hh = wrap_text(s, callx, yy, callw, t, 15, 'bold', color=RED, va='center')
            y -= oh
        y -= 0.18
    return s


# ------------------------------------------------------------------ boolean mask
@fig('x_ds_mask')
def ds_mask(w, h, headers=(), rows=(), index=(), mask=(), cond='', **_):
    s = Scene(w, h)
    size, rh = 15, 0.4
    hdr = [''] + list(headers)
    body = [[str(i)] + list(r) for i, r in zip(index, rows)]
    colw = col_widths(hdr, body, size, 0.24)
    ytop = h - 0.55
    x0 = 0.1
    s.text(x0, h - 0.22, f'1. The rows ({len(rows)} of them)', size=16, weight='bold', ha='left')
    grid(s, x0, ytop, hdr, body, size=size, rh=rh, colw=colw, hl={(r + 1, 0): PALE for r in range(len(rows))})
    mw = max(mono_w(cond, size), tw('True', size, 'bold')) + 0.35
    mx = x0 + sum(colw) + 0.5
    s.arrow(x0 + sum(colw) + 0.05, ytop - 1.5 * rh, mx - 0.05, ytop - 1.5 * rh, lw=2.2, head=14)
    s.text(mx, h - 0.22, '2. The mask (True or False)', size=16, weight='bold', ha='left')
    mrows = [['True' if m else 'False'] for m in mask]
    s.table(mx, ytop, [mw], rh, [[cond]] + mrows, header=True, size=size, mono_cols=(0,), align=['left'],
            hl_cells={(0, 0): PALE, **{(i + 1, 0): GOLD for i, m in enumerate(mask) if m}})
    kept = [b for b, m in zip(body, mask) if m]
    kx = mx + mw + 0.5
    s.arrow(mx + mw + 0.05, ytop - 1.5 * rh, kx - 0.05, ytop - 1.5 * rh, lw=2.2, head=14)
    s.text(kx, h - 0.22, '3. Rows kept: where the mask is True', size=16, weight='bold', ha='left')
    if kx + sum(colw) > w - 0.05:
        raise ValueError('ds_mask too wide')
    grid(s, kx, ytop, hdr, kept, size=size, rh=rh, colw=colw, hl={(r + 1, 0): PALE for r in range(len(kept))})
    s.text(kx, ytop - (len(kept) + 1) * rh - 0.3, 'The index keeps its old labels.', size=15, color=BODY, ha='left')
    return s


# ------------------------------------------------------------------ two conditions as circles
@fig('x_ds_venn')
def ds_venn(w, h, a='', b='', only_a=0, both=0, only_b=0, neither=0, total=0, ops=(), **_):
    s = Scene(w, h)
    r, sep = 1.3, 1.55
    rect_w = 6.3
    s.rect(0.1, 0.1, rect_w, h - 0.2, fill=PAPER, edge=INK, lw=1.8, z=1)
    s.text(0.25, h - 0.3, f'All {total:,} orders', size=16, weight='bold', ha='left')
    cx_a = 0.1 + rect_w / 2 - sep / 2
    cx_b = cx_a + sep
    cy = h / 2 - 0.4
    ca = Circle((cx_a, cy), r, fc=PALE, ec='none', zorder=2)
    cb = Circle((cx_b, cy), r, fc=PALE, ec='none', zorder=2)
    s.ax.add_patch(ca)
    s.ax.add_patch(cb)
    ci = Circle((cx_b, cy), r, fc=GOLD, ec='none', zorder=3)
    s.ax.add_patch(ci)
    ci.set_clip_path(ca)
    for cx in (cx_a, cx_b):
        s.ax.add_patch(Circle((cx, cy), r, fc='none', ec=INK, lw=2.2, zorder=4))
    s.text(cx_a - 0.55, cy + 0.0, f'{only_a:,}', size=22, weight='bold', z=6)
    s.text((cx_a + cx_b) / 2, cy, f'{both:,}', size=22, weight='bold', z=6)
    s.text(cx_b + 0.55, cy, f'{only_b:,}', size=22, weight='bold', z=6)
    s.text(cx_a - 0.55, cy - 0.38, 'A only', size=14, color=BODY, z=6)
    s.text((cx_a + cx_b) / 2, cy - 0.38, 'both', size=14, color=BODY, z=6)
    s.text(cx_b + 0.55, cy - 0.38, 'B only', size=14, color=BODY, z=6)
    s.text(0.3, cy + r + 0.3, a, size=16, weight='bold', ha='left')
    s.text(0.1 + rect_w - 0.2, cy + r + 0.3, b, size=16, weight='bold', ha='right')
    s.text(0.1 + rect_w - 0.2, 0.42, f'neither: {neither:,}', size=16, weight='bold', ha='right')
    x = rect_w + 0.5
    s.text(x, h - 0.35, 'Join two conditions', size=17, weight='bold', ha='left')
    y = h - 0.95
    for sym, name, count, expl in ops:
        s.box(x, y - 0.3, 0.7, 0.6, sym, size=24, fill=GOLD, edge=INK, lw=1.8, weight='bold', r=0.06, mono=True)
        s.text(x + 0.9, y + 0.14, name, size=17, weight='bold', ha='left')
        s.text(x + 0.9, y - 0.2, expl, size=15, color=BODY, ha='left')
        s.text(w - 0.15, y + 0.14, count, size=20, weight='bold', ha='right')
        y -= 1.0
    return s


# ------------------------------------------------------------------ position (iloc) and label (loc)
@fig('x_ds_loc_iloc')
def ds_loc_iloc(w, h, headers=(), rows=(), labels=(), iloc_n=2, loc_n=3, iloc_code='', loc_code='', iloc_say='', loc_say='', **_):
    s = Scene(w, h)
    size, rh = 15, 0.42
    hdr = ['position', 'label'] + list(headers)
    body = [[str(i), str(l)] + list(r) for i, (l, r) in enumerate(zip(labels, rows))]
    colw = col_widths(hdr, body, size, 0.24)
    ytop = h - 0.7
    x0 = 0.1
    s.text(x0, h - 0.25, 'The same rows of jinja, numbered two ways', size=17, weight='bold', ha='left')
    hl = {(0, 0): PALE, (0, 1): PALE}
    for r in range(len(rows)):
        hl[(r + 1, 0)] = PALE
        hl[(r + 1, 1)] = PALE
    grid(s, x0, ytop, hdr, body, size=size, rh=rh, colw=colw, hl=hl)
    # iloc: first iloc_n rows, position column
    outline(s, x0 + 0.03, ytop - rh * (iloc_n + 1) + 0.03, colw[0] - 0.06, rh * iloc_n - 0.06, color=RED, lw=3.0)
    outline(s, x0 + colw[0] + 0.03, ytop - rh * (loc_n + 1) + 0.03, colw[1] - 0.06, rh * loc_n - 0.06, color=INK, lw=3.0)
    tx = x0 + sum(colw) + 0.45
    tw_ = w - tx - 0.1
    s.text(tx, ytop - 0.15, iloc_code, size=17, weight='bold', color=RED, mono=True, ha='left')
    wrap_text(s, tx, ytop - 0.62, tw_, iloc_say, 16, color=BODY, va='top')
    s.text(tx, ytop - 1.75, loc_code, size=17, weight='bold', color=INK, mono=True, ha='left')
    wrap_text(s, tx, ytop - 2.22, tw_, loc_say, 16, color=BODY, va='top')
    return s


# ------------------------------------------------------------------ the IQR rule
@fig('x_ds_iqr')
def ds_iqr(w, h, q1=0, med=0, q3=0, lo=0, hi_in=0, fence=0, n_out=0, vmax=0, unit='UGX', **_):
    s = Scene(w, h)
    x0, span, vscale = 0.5, 8.0, 150000.0
    X = lambda v: x0 + span * v / vscale
    yb = 2.35
    bh = 0.8
    s.line(x0, yb - 0.75, x0 + span, yb - 0.75, color=GREY, lw=1.4, z=1)
    for v in (0, 50000, 100000, 150000):
        s.line(X(v), yb - 0.75, X(v), yb - 0.82, color=GREY, lw=1.2)
        s.text(X(v), yb - 1.0, f'{v:,}', size=14, color=MUTE, va='center')
    # box and whiskers
    s.line(X(lo), yb, X(q1), yb, color=INK, lw=2.4)
    s.line(X(q3), yb, X(hi_in), yb, color=INK, lw=2.4)
    s.line(X(lo), yb - 0.15, X(lo), yb + 0.15, color=INK, lw=2.4)
    s.line(X(hi_in), yb - 0.15, X(hi_in), yb + 0.15, color=INK, lw=2.4)
    s.rect(X(q1), yb - bh / 2, X(q3) - X(q1), bh, fill=GOLD, edge=INK, lw=2.4, z=3)
    s.line(X(med), yb - bh / 2, X(med), yb + bh / 2, color=INK, lw=3.4, z=4)
    # fence
    s.line(X(fence), yb - 0.7, X(fence), yb + 1.0, color=RED, lw=2.6, dash=True, z=4)
    # axis break and largest value
    bx = x0 + span + 0.35
    for dx in (0, 0.14):
        s.line(bx + dx - 0.05, yb - 0.85, bx + dx + 0.05, yb - 0.65, color=INK, lw=2.0)
    xm = bx + 1.7
    s.line(x0 + span, yb - 0.75, bx - 0.05, yb - 0.75, color=GREY, lw=1.4)
    s.line(bx + 0.2, yb - 0.75, xm + 0.4, yb - 0.75, color=GREY, lw=1.4)
    s.circle(xm, yb, 0.11, fill=RED, edge=INK, lw=1.6, z=5)
    s.text(xm, yb - 1.0, f'{vmax:,}', size=14, color=MUTE)
    s.text(xm + 0.3, yb + 1.15, f'largest order: {vmax:,}', size=15, weight='bold', color=RED, ha='right')
    s.line(xm, yb + 0.12, xm, yb + 0.95, color=RED, lw=1.4)
    s.text(bx + 0.1, yb - 1.35, 'axis broken here', size=14, color=MUTE)
    # labels
    s.text(X(med), yb + 0.72, f'median {med:,}', size=15, weight='bold')
    s.text(X(q1) - 0.1, yb + 1.35, f'Q1 (25th percentile) {q1:,}', size=15, weight='bold', ha='left')
    s.text(X(q3) + 0.1, yb + 1.0, f'Q3 (75th percentile) {q3:,}', size=15, weight='bold', ha='left')
    s.line(X(q1), yb + bh / 2, X(q1), yb + 1.35 - 0.12, color=INK, lw=1.4)
    s.line(X(q3), yb + bh / 2, X(q3), yb + 1.0 - 0.12, color=INK, lw=1.4)
    s.brace(X(q1), X(q3), yb - 1.5, depth=0.12, up=True)
    s.text((X(q1) + X(q3)) / 2, yb - 1.78, f'IQR = Q3 - Q1 = {q3 - q1:,}', size=16, weight='bold')
    s.text(X(fence) + 0.12, yb + 0.55, f'upper fence', size=15, weight='bold', color=RED, ha='left')
    s.text(X(fence) + 0.12, yb + 0.3, f'Q3 + 1.5 x IQR = {fence:,}', size=15, weight='bold', color=RED, ha='left')
    s.text(X(fence) + 0.12, yb - 0.18, f'{n_out:,} orders sit above it', size=15, color=BODY, ha='left')
    return s


# ------------------------------------------------------------------ two grids and the code between
@fig('x_ds_before_after')
def ds_before_after(w, h, left=None, right=None, code=(), caption='', **_):
    s = Scene(w, h)
    size, rh = 15, 0.4
    for size in (15, 14):
        wl = col_widths(left['headers'], left['rows'], size, 0.22)
        wr = col_widths(right['headers'], right['rows'], size, 0.22)
        if sum(wl) + sum(wr) + 1.0 <= w - 0.2:
            break
    else:
        raise ValueError(f'ds_before_after too wide: {sum(wl) + sum(wr) + 1.0:.2f}')
    nrows = max(len(left['rows']), len(right['rows']))
    ytop = h - 0.55
    xl = 0.1
    xr = w - 0.1 - sum(wr)
    for x, d, cw in ((xl, left, wl), (xr, right, wr)):
        s.text(min(x, w - 0.1 - tw(d['title'], 16, 'bold') - 0.05), h - 0.22, d['title'], size=16, weight='bold', ha='left')
        grid(s, x, ytop, d['headers'], d['rows'], size=size, rh=rh, colw=cw, hl={(r + 1, c): GOLD for r, c in d.get('hl', [])})
    s.arrow(xl + sum(wl) + 0.1, ytop - 1.5 * rh, xr - 0.1, ytop - 1.5 * rh, lw=2.4, head=16)
    ybot = ytop - (nrows + 1) * rh
    cw_ = max(mono_w(l, 14) for l in code) + 0.4
    cwid, chei = s.code((w - cw_) / 2, ybot - 0.3, list(code), size=14, w=cw_)
    if caption:
        wrap_text(s, 0.1, ybot - 0.3 - chei - 0.3, w - 0.2, caption, 16, 'bold', va='center')
    return s


# ------------------------------------------------------------------ one date, two readings
@fig('x_ds_date_fork')
def ds_date_fork(w, h, text='', right_fmt='', right_read='', wrong_fmt='', wrong_read='', parts=(), total=0, **_):
    s = Scene(w, h)
    s.box(w / 2 - 1.4, h - 0.7, 2.8, 0.6, text, size=22, fill=GOLD, edge=INK, lw=2.0, weight='bold', mono=True, r=0.06)
    bw = 5.6
    for i, (fmt, read, ok) in enumerate(((right_fmt, right_read, True), (wrong_fmt, wrong_read, False))):
        x = 0.15 + i * (w - 0.3 - bw)
        s.box(x, h - 2.35, bw, 1.1, '', fill=PAPER if ok else PALE, edge=INK if ok else RED, lw=2.0, r=0.06)
        s.text(x + 0.2, h - 1.62, fmt, size=15, mono=True, ha='left')
        s.text(x + 0.2, h - 2.02, read, size=18, weight='bold', ha='left', color=INK if ok else RED)
        s.arrow(w / 2 + (-0.6 if i == 0 else 0.6), h - 0.74, x + bw / 2 + (0.6 if i == 0 else -0.6), h - 1.22, lw=2.2, head=14, color=INK if ok else RED)
    s.text(0.15, h - 2.75, f'Read the {total:,} slash dates the wrong way round and this happens:', size=16, weight='bold', ha='left')
    x = 0.15
    bwid = w - 0.3
    y = h - 3.55
    for lab, v, fill in parts:
        ww = bwid * v / total
        s.rect(x, y, ww, 0.55, fill=fill, edge=INK, lw=1.8, z=2)
        if ww >= 0.9:
            s.text(x + ww / 2, y + 0.275, f'{v:,}', size=17, weight='bold', z=6)
            wrap_text(s, x + ww / 2, y - 0.1, max(ww, 2.4) - 0.15, lab, 14, color=BODY, ha='center', va='top')
        else:
            s.text(x + ww, y - 0.2, f'{v:,}: {lab}', size=15, color=BODY, ha='right', weight='bold')
        x += ww
    return s


# ------------------------------------------------------------------ reconciliation
@fig('x_ds_reconcile')
def ds_reconcile(w, h, control=None, cleaned=None, diff=None, why='', **_):
    s = Scene(w, h)
    bw, gap = 3.35, 0.78
    x0 = (w - 3 * bw - 2 * gap) / 2
    y = h - 1.95
    for i, (d, fill) in enumerate(((control, PAPER), (cleaned, PAPER), (diff, GOLD))):
        x = x0 + i * (bw + gap)
        s.box(x, y, bw, 1.55, '', fill=fill, edge=INK, lw=2.2 if i < 2 else 3.0, r=0.07)
        s.text(x + bw / 2, y + 1.22, d['label'], size=16, weight='bold')
        s.text(x + bw / 2, y + 0.72, d['value'], size=26, weight='bold')
        s.text(x + bw / 2, y + 0.28, d['unit'], size=15, color=BODY)
    for i, sym in enumerate(('-', '=')):
        s.text(x0 + (i + 1) * bw + i * gap + gap / 2, y + 0.78, sym, size=38, weight='bold')
    yb = y - 0.35
    s.arrow(x0 + 2 * (bw + gap) + bw / 2, yb + 0.28, x0 + 2 * (bw + gap) + bw / 2, yb + 0.02, lw=2.2, head=14, color=RED)
    s.box(0.2, yb - 1.45, w - 0.4, 1.45, '', fill=PAPER, edge=RED, lw=2.4, r=0.07)
    wrap_text(s, 0.45, yb - 0.72, w - 0.9, why, 18, va='center')
    return s
