"""Figure kinds for Sessions 13 and 14 (regression, the machine learning workflow), author letter g. Registered as x_<kind>, used as visual=dict(kind='<kind>', ...).

  ds_onehot        a categorical variable beside its indicator (dummy) columns; one level dropped as the reference level
  ds_dummy_trap    the dummy variable trap: the indicator columns add up to the intercept column
  ds_ft_table      real records with every variable marked Feature or Target
  ds_impute        a variable with missing values, its missing-indicator flag and the imputed variable
  ds_crispdm       the six phases of CRISP-DM as a cycle, some phases highlighted
  ds_confusion_pos a confusion matrix with the names of the positive and the negative class
All text is 14 pt or larger and every figure is audited for overlaps by figkit.
"""
import math

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, PALE, fig
import slidekit as K


def tw(t, size, kind='regular'):
    return K.width_in(str(t), size, kind)


def col_widths(headers, rows, size, pad=0.26, minw=0.0):
    return [max([minw, tw(headers[c], size, 'bold')] + [tw(r[c], size) for r in rows]) + pad for c in range(len(headers))]


def grid(s, x, ytop, headers, rows, size=15, rh=0.4, hl=None, colw=None, pad=0.26, head_fill=PALE):
    colw = colw or col_widths(headers, rows, size, pad)
    cells = {(0, c): head_fill for c in range(len(headers))}
    if hl:
        cells.update(hl)
    s.table(x, ytop, colw, rh, [list(headers)] + [list(r) for r in rows], header=True, size=size, align=['left'] * len(headers), hl_cells=cells)
    return colw, ytop - (len(rows) + 1) * rh


def wrap_text(s, x, y, w, text, size, weight='normal', color=INK, ha='left', va='center'):
    lines = K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', w)
    s.text(x, y, '\n'.join(lines), size=size, weight=weight, color=color, ha=ha, va=va)
    return len(lines) * size * 1.15 / 72


# ------------------------------------------------------------------ indicator (dummy) columns
@fig('x_ds_onehot')
def ds_onehot(w, h, left_headers=(), rows=(), levels=(), drop='', size=16, **_):
    """rows: [[week_start, branch_id], ...]; the indicator columns come from `levels`; `drop` is the reference level."""
    s = Scene(w, h)
    rh = 0.38
    ytop = h - 0.8
    lw_ = col_widths(left_headers, rows, size, 0.3)
    s.text(0.1, h - 0.3, 'Before: one categorical variable', size=17, weight='bold', ha='left')
    grid(s, 0.1, ytop, left_headers, rows, size=size, rh=rh, colw=lw_, hl={(i + 1, len(left_headers) - 1): GOLD for i in range(len(rows))})
    x2 = 0.1 + sum(lw_) + 1.3
    rcw = [max(0.78, tw(l, size, 'bold') + 0.26) for l in levels]
    data = [[('1' if r[-1] == l else '0') for l in levels] for r in rows]
    hl = {}
    for i, r in enumerate(rows):
        j = list(levels).index(r[-1])
        hl[(i + 1, j)] = GOLD
    j0 = list(levels).index(drop)
    for i in range(len(rows)):
        if (i + 1, j0) not in hl:
            hl[(i + 1, j0)] = '#D9D9D9'
    s.text(x2, h - 0.3, 'After: one indicator (dummy) column per level', size=17, weight='bold', ha='left')
    grid(s, x2, ytop, list(levels), data, size=size, rh=rh, colw=rcw, hl=hl)
    ybot = ytop - (len(rows) + 1) * rh
    s.arrow(0.1 + sum(lw_) + 0.1, ytop - rh * 2.5, x2 - 0.1, ytop - rh * 2.5, color=RED, lw=2.6, head=16)
    xd = x2 + sum(rcw[:j0])
    s.line(xd, ybot - 0.1, xd + rcw[j0], ybot - 0.1, color=INK, lw=2.4)
    s.text(xd + rcw[j0] / 2, ybot - 0.32, f'{drop}: dropped', size=15, weight='bold')
    wrap_text(s, 0.1, 0.35, w - 0.2, f'One-hot encoding keeps {len(levels) - 1} of the {len(levels)} columns. The dropped level ({drop}) is the reference level. '
                                          f'A record with all {len(levels) - 1} kept indicators at 0 belongs to {drop}.', 16, ha='left', va='center')
    return s


# ------------------------------------------------------------------ the dummy variable trap
@fig('x_ds_dummy_trap')
def ds_dummy_trap(w, h, headers=(), rows=(), rank_line='', fix_line='', size=16, **_):
    """headers: intercept, B01 ... B08, sum; rows hold 0 and 1; the last column is the row sum of the indicators."""
    s = Scene(w, h)
    rh = 0.4
    ytop = h - 0.65
    s.text(0.1, h - 0.3, 'Design matrix for three records (one row each)', size=17, weight='bold', ha='left')
    colw = [max(0.85, tw(t, size, 'bold') + 0.28) for t in headers]
    n = len(headers)
    hl = {}
    for i in range(len(rows)):
        hl[(i + 1, 0)] = GOLD
        hl[(i + 1, n - 1)] = GOLD
    grid(s, 0.1, ytop, headers, rows, size=size, rh=rh, colw=colw, hl=hl)
    ybot = ytop - (len(rows) + 1) * rh
    y = ybot - 0.38
    s.box(0.1, y - 0.14, 0.28, 0.28, '', fill=GOLD, edge=INK, lw=1.4, r=0.03)
    s.text(0.55, y, 'The intercept column is always 1. The indicators add up to 1 in every row, so they repeat it.', size=16, ha='left')
    y -= 0.5
    wrap_text(s, 0.1, y, w - 0.2, rank_line, 17, 'bold', color=RED, va='center')
    y -= 0.55
    wrap_text(s, 0.1, y, w - 0.2, fix_line, 16, va='center')
    return s


# ------------------------------------------------------------------ features and target on real records
@fig('x_ds_ft_table')
def ds_ft_table(w, h, headers=(), rows=(), roles=(), record_label='one record = one loan', size=16, **_):
    """roles: 'feature' or 'target' for every column."""
    s = Scene(w, h)
    rh = 0.46
    colw = col_widths(headers, rows, size, 0.3, minw=1.25)
    tot = sum(colw)
    if tot < w - 0.3:
        colw = [c * (w - 0.3) / tot for c in colw]
    x0 = 0.1
    ytop = h - 1.15
    hl = {}
    for c, r in enumerate(roles):
        if r == 'target':
            for i in range(len(rows) + 1):
                hl[(i, c)] = GOLD
    grid(s, x0, ytop, headers, rows, size=size, rh=rh, colw=colw, hl=hl)
    x = x0
    for c, r in enumerate(roles):
        t = 'TARGET' if r == 'target' else 'FEATURE'
        s.box(x + 0.06, ytop + 0.12, colw[c] - 0.12, 0.42, t, size=15, fill=INK if r == 'target' else PAPER, edge=INK, color=PAPER if r == 'target' else INK, lw=1.6, weight='bold', r=0.05)
        x += colw[c]
    ybot = ytop - (len(rows) + 1) * rh
    s.brace(x0, x0 + sum(colw), ybot - 0.15, depth=0.12, up=True)
    s.text(x0 + sum(colw) / 2, ybot - 0.5, 'Each row is one record (an observation). The model reads the features and predicts the target.', size=16, weight='bold')
    return s


# ------------------------------------------------------------------ missing values: flag, then impute
@fig('x_ds_impute')
def ds_impute(w, h, headers=(), rows=(), note='', size=16, **_):
    """headers: id, variable raw, flag, variable imputed. rows: strings; a blank raw cell is shown as 'blank'."""
    s = Scene(w, h)
    rh = 0.5
    colw = col_widths(headers, rows, size, 0.34)
    ytop = h - 0.9
    hl = {}
    for i, r in enumerate(rows):
        if r[1] == 'blank':
            hl[(i + 1, 1)] = GOLD
            hl[(i + 1, 2)] = GOLD
            hl[(i + 1, 3)] = GOLD
    s.text(0.1, h - 0.3, 'Step 1: make the flag. Step 2: fill the blank with the median.', size=17, weight='bold', ha='left')
    grid(s, 0.1, ytop, headers, rows, size=size, rh=rh, colw=colw, hl=hl)
    ybot = ytop - (len(rows) + 1) * rh
    wrap_text(s, 0.1, ybot - 0.5, w - 0.2, note, 16, ha='left', va='center')
    return s


# ------------------------------------------------------------------ CRISP-DM
@fig('x_ds_crispdm')
def ds_crispdm(w, h, items=(), highlight=(), center='Data', size=18, **_):
    s = Scene(w, h)
    n = len(items)
    cx, cy = w / 2, h / 2
    rx, ry = w / 2 - 1.65, h / 2 - 0.62
    bw, bh = 2.9, 0.95
    pts = []
    for i in range(n):
        a = math.pi / 2 - 2 * math.pi * i / n
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    for i, (x, y) in enumerate(pts):
        nx, ny = pts[(i + 1) % n]
        s.arrow(x + (nx - x) * 0.36, y + (ny - y) * 0.36, x + (nx - x) * 0.64, y + (ny - y) * 0.64, lw=2.2, head=16, rad=-0.2)
    for i, ((x, y), t) in enumerate(zip(pts, items)):
        s.box(x - bw / 2, y - bh / 2, bw, bh, '', fill=GOLD if i in highlight else PAPER, edge=INK, lw=2.0, r=0.07, z=3)
        lines = K.wrap(t, size, 'bold', bw - 0.2)
        s.text(x, y, '\n'.join(lines), size=size, weight='bold', z=6)
    s.text(cx, cy + 0.15, center, size=22, weight='bold', color=INK)
    s.text(cx, cy - 0.3, 'Gold: the phases\nof today\'s lab', size=15, color=MUTE)
    return s


# ------------------------------------------------------------------ confusion matrix with class names
@fig('x_ds_confusion_pos')
def ds_confusion_pos(w, h, tp=0, fp=0, fn=0, tn=0, pos='defaulted', neg='repaid', size=18, **_):
    s = Scene(w, h)
    lw_, top = 2.1, 0.9
    cw = (w - lw_ - 0.1) / 2
    ch = (h - top - 0.1) / 2
    x0 = lw_
    s.text(x0 + cw / 2, h - 0.45, f'Really {pos}', size=size, weight='bold')
    s.text(x0 + cw * 1.5, h - 0.45, f'Really {neg}', size=size, weight='bold')
    s.text(lw_ / 2, 0.1 + ch * 1.5, f'Model said\n"{pos}"', size=size, weight='bold')
    s.text(lw_ / 2, 0.1 + ch * 0.5, f'Model said\n"{neg}"', size=size, weight='bold')
    cells = [(0, 1, tp, 'True positive', 'default caught', GOLD), (1, 1, fp, 'False positive', 'false alarm', PAPER),
             (0, 0, fn, 'False negative', 'default missed', PAPER), (1, 0, tn, 'True negative', 'rightly cleared', PAPER)]
    for cx, cy, n, nm, sub, fill in cells:
        x = x0 + cx * cw + 0.05
        y = 0.1 + cy * ch + 0.05
        s.box(x, y, cw - 0.1, ch - 0.1, '', fill=fill, edge=INK, lw=2.0, r=0.06)
        s.text(x + (cw - 0.1) / 2, y + (ch - 0.1) * 0.66, f'{n:,}', size=36, weight='bold')
        s.text(x + (cw - 0.1) / 2, y + (ch - 0.1) * 0.26, nm + '\n' + sub, size=size - 3, color=BODY)
    return s
