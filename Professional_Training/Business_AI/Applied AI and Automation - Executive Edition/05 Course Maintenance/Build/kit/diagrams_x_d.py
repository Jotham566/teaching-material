"""Figure kinds added by author d for Sessions 5 and 7 (auto-imported by diagrams.py).

runs      a results grid: one row per item, the key and two runs side by side. rows: [{item, key, r1, r2, ok1, ok2}] with ok True (plain), False (red) or None (gold: differs or flagged).
gate      the control picture for Session 7: untrusted text -> assistant -> permission gate -> tools (allowed, approval, blocked).
boundary  the boundary table: rows [{action, may, approve, never}] drawn as three columns, gold for 'a person approves' and red for 'never'.
"""
from figkit import Scene, INK, BODY, MUTE, HAIR, PAPER, RED, GOLD, fig
import slidekit as K


def _fit(rows_cells, widths, w, h, size, head_row, pad=0.12, min_size=14):
    """Find the largest font size (<= size, >= min_size) at which every row fits the height h; return size and row heights."""
    for sz in range(int(size), min_size - 1, -1):
        lh = sz * 1.17 / 72
        hs = []
        for ri, r in enumerate(rows_cells):
            n = max(len(K.wrap(str(c), sz, 'bold' if ((ri == 0 and head_row) or ci == 0) else 'regular', widths[ci] - 0.24)) for ci, c in enumerate(r))
            hs.append(n * lh + 0.13)
        if sum(hs) <= h - 0.05:
            return sz, hs
    return min_size, hs


@fig('x_runs')
def x_runs(w, h, rows=(), heads=('Item', 'The key', 'Run 1', 'Run 2'), fr=(0.2, 0.28, 0.26, 0.26), size=16, legend=(), **_):
    s = Scene(w, h)
    full_h = h
    if legend:
        h = h - 0.42
    cw = [w * f for f in fr]
    xs = [0.0]
    for c in cw:
        xs.append(xs[-1] + c)
    cells = [list(heads)] + [[r['item'], r['key'], r['r1'], r['r2']] for r in rows]
    sz, hs = _fit(cells, cw, w, h, size, True)
    top = full_h - 0.02
    y = top
    for ri, r in enumerate(cells):
        rh = hs[ri]
        if ri > 0:
            d = rows[ri - 1]
            for ci, ok in ((2, d.get('ok1', True)), (3, d.get('ok2', True))):
                if ok is False:
                    s.rect(xs[ci] + 0.03, y - rh + 0.03, cw[ci] - 0.06, rh - 0.06, fill=RED, edge=RED, lw=0, z=2)
                elif ok is None:
                    s.rect(xs[ci] + 0.03, y - rh + 0.03, cw[ci] - 0.06, rh - 0.06, fill=GOLD, edge=GOLD, lw=0, z=2)
        for ci, txt in enumerate(r):
            colour = INK
            if ri > 0 and ci in (2, 3) and rows[ri - 1].get('ok1' if ci == 2 else 'ok2', True) is False:
                colour = PAPER
            lines = K.wrap(str(txt), sz, 'bold' if (ri == 0 or ci == 0) else 'regular', cw[ci] - 0.24)
            s.text(xs[ci] + 0.12, y - rh / 2, '\n'.join(lines), size=sz, weight='bold' if (ri == 0 or ci == 0) else 'normal',
                   ha='left', color=colour if ri > 0 and ci > 1 else (INK if ci == 0 or ri == 0 else BODY), z=6)
        s.line(0, y - rh, w, y - rh, color=INK if ri == 0 else HAIR, lw=2.2 if ri == 0 else 0.9, z=3)
        y -= rh
    lx = 0.05
    for col, txt in legend:
        s.rect(lx, 0.06, 0.26, 0.26, fill=GOLD if col == 'gold' else RED, edge=INK, lw=1.0, z=3)
        s.text(lx + 0.36, 0.19, txt, size=15, ha='left', color=BODY)
        lx += 0.5 + K.width_in(txt, 15) + 0.4
    return s


@fig('x_gate')
def x_gate(w, h, **_):
    """Untrusted text -> assistant -> the permission gate -> tools: two allowed, one blocked (a person must approve)."""
    s = Scene(w, h)
    bw, bh = 2.0, 1.6
    yc = h / 2 + 0.2
    x1, x2, gx = 0.05, 2.85, 5.85
    for x, icon, head, sub in ((x1, 'mail', 'Email text', 'anyone can write it'), (x2, 'robot', 'Agent', 'reads all of it')):
        s.box(x, yc - bh / 2, bw, bh, '', edge=INK, lw=2.0, r=0.08)
        s.icon(icon, x + bw / 2, yc + 0.38, 0.85)
        s.text(x + bw / 2, yc - 0.3, head, size=18, weight='bold')
        s.text(x + bw / 2, yc - 0.62, sub, size=14, color=MUTE)
    s.arrow(x1 + bw + 0.05, yc, x2 - 0.05, yc, lw=2.4, head=18)
    s.arrow(x2 + bw + 0.05, yc, gx - 0.03, yc, lw=2.4, head=18)
    s.rect(gx, 0.12, 0.34, h - 0.24, fill=GOLD, edge=INK, lw=2.0, z=3)
    s.text(x2 + bw / 2 + 0.2, 0.42, 'The control: tool permissions\nand human approval', size=17, weight='bold', color=RED)
    s.arrow(x2 + bw + 1.15, 0.42, gx - 0.03, 0.42, color=RED, lw=2.0, head=16)
    tx = 7.15
    tw = w - tx - 0.05
    th = 1.0
    gap = (h - 3 * th - 0.24) / 2
    items = [('Read one mail label', 'Allowed', False), ('Save a draft reply', 'Allowed', False), ('Forward to any address', 'Blocked until a person approves', True)]
    for i, (name, tag, red) in enumerate(items):
        y = h - 0.12 - (i + 1) * th - i * gap
        s.box(tx, y, tw, th, '', fill=PAPER, edge=RED if red else INK, lw=2.4 if red else 1.8, r=0.08, dash=red)
        s.text(tx + 0.2, y + th * 0.66, name, size=18, weight='bold', ha='left')
        s.text(tx + 0.2, y + th * 0.3, tag, size=15, color=RED if red else BODY, ha='left', weight='bold' if red else 'normal')
        s.arrow(gx + 0.37, y + th / 2, tx - 0.03, y + th / 2, color=RED if red else INK, lw=2.4, head=18, dash=red)
    return s


@fig('x_boundary')
def x_boundary(w, h, rows=(), heads=('', 'It may', 'A person approves', 'It must never'), fr=(0.11, 0.30, 0.30, 0.29), size=16, **_):
    s = Scene(w, h)
    cw = [w * f for f in fr]
    cw[-1] = w - sum(cw[:-1])
    xs = [0.0]
    for c in cw:
        xs.append(xs[-1] + c)
    cells = [list(heads)] + [[r['action'], r['may'], r['approve'], r['never']] for r in rows]
    sz, hs = _fit(cells, cw, w, h, size, True)
    y = h - 0.02
    for ri, r in enumerate(cells):
        rh = hs[ri]
        for ci, txt in enumerate(r):
            colour = INK
            if ri > 0 and ci == 2:
                s.rect(xs[ci] + 0.03, y - rh + 0.03, cw[ci] - 0.06, rh - 0.06, fill=GOLD, edge=GOLD, lw=0, z=2)
            if ri > 0 and ci == 3:
                s.rect(xs[ci] + 0.03, y - rh + 0.03, cw[ci] - 0.06, rh - 0.06, fill=RED, edge=RED, lw=0, z=2)
                colour = PAPER
            bold = ri == 0 or ci == 0
            lines = K.wrap(str(txt), sz, 'bold' if bold else 'regular', cw[ci] - 0.24)
            s.text(xs[ci] + 0.12, y - rh / 2, '\n'.join(lines), size=sz, weight='bold' if bold else 'normal', ha='left', color=colour if ci else INK, z=6)
        s.line(0, y - rh, w, y - rh, color=INK if ri == 0 else HAIR, lw=2.2 if ri == 0 else 0.9, z=3)
        y -= rh
    return s
