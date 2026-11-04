"""Figure kinds for Session 2 (Data as tables), author letter a. Each is registered as x_<kind> and used as visual=dict(kind='<kind>', ...).

  ds_anatomy        a real excerpt of a table with the record (row), variable (column) and cell labelled
  ds_granularity    the same order shown at three levels of detail (levels: title, headers, rows)
  ds_types          variable types (numeric, categorical, datetime, text) over the data types that store them
  ds_key_test       two panels: a variable that passes the primary key test and one that fails (COUNTA against the count of different values)
  ds_composite      a composite key shown on real rows of a table
  ds_fk             a foreign key linking two small real tables, with the lookup formula
  ds_onemany        two one-to-many relationships drawn with a crow's foot
  ds_erd            an entity relationship diagram (tables: name, col, row, rows [(variable, tag)]; links)
  ds_trace          one order followed through four tabs by their keys
  ds_flagged_sheet  a spreadsheet excerpt whose problem cells are gold, with a numbered legend
All text is 14 pt or larger and every figure is audited for overlaps by figkit.
"""
from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, PALE, fig
import slidekit as K
from matplotlib.patches import Rectangle


def tw(t, size, kind='regular'):
    return K.width_in(str(t), size, kind)


def mono_w(t, size):
    return 0.602 * size / 72 * len(t)


def wrap_text(s, x, y, w, text, size, weight='normal', color=INK, ha='left', va='center', italic=False):
    """Wrapped text in a column of width w centred on y (va centre) or starting at y (va top). Returns its height."""
    lines = K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', w)
    s.text(x, y, '\n'.join(lines), size=size, weight=weight, color=color, ha=ha, va=va, italic=italic)
    return len(lines) * size * 1.15 / 72


def col_widths(headers, rows, size, pad=0.26):
    return [max([tw(headers[c], size, 'bold')] + [tw(r[c], size) for r in rows]) + pad for c in range(len(headers))]


def grid(s, x, ytop, headers, rows, size=15, rh=0.4, hl=None, colw=None, pad=0.26, head_fill=PALE):
    """A real-data grid. Returns (column widths, y of the bottom edge)."""
    colw = colw or col_widths(headers, rows, size, pad)
    cells = {(0, c): head_fill for c in range(len(headers))}
    if hl:
        cells.update(hl)
    s.table(x, ytop, colw, rh, [list(headers)] + [list(r) for r in rows], header=True, size=size, align=['left'] * len(headers), hl_cells=cells)
    return colw, ytop - (len(rows) + 1) * rh


def tag(s, x, y, text, fill=GOLD, size=14, h=0.3):
    """A small label with its left edge at x and centre at y. Returns its width."""
    w = tw(text, size, 'bold') + 0.22
    s.box(x, y - h / 2, w, h, text, size=size, fill=fill, edge=INK, lw=1.4, weight='bold', r=0.05, z=5)
    return w


def outline(s, x, y, w, h, color=RED, lw=3.0):
    s.ax.add_patch(Rectangle((x, y), w, h, fc='none', ec=color, lw=lw, zorder=7))


def crow(s, x, y, dx, dy, lw=2.0):
    """A crow's foot at the box edge (x, y); (dx, dy) is the unit direction pointing away from the box along the line."""
    px, py = -dy, dx
    bx, by = x + dx * 0.24, y + dy * 0.24
    for k in (-1, 0, 1):
        s.line(bx, by, x + px * 0.13 * k, y + py * 0.13 * k, color=INK, lw=lw, z=6)


def one(s, x, y, dx, dy, lw=2.0):
    """The 'exactly one' mark: two short bars across the line near the box edge."""
    px, py = -dy, dx
    for t in (0.1, 0.2):
        cx, cy = x + dx * t, y + dy * t
        s.line(cx - px * 0.1, cy - py * 0.1, cx + px * 0.1, cy + py * 0.1, color=INK, lw=lw, z=6)


# ------------------------------------------------------------------ record, variable, cell
@fig('x_ds_anatomy')
def ds_anatomy(w, h, headers=(), rows=(), cell=(3, 2), tab='orders', **_):
    s = Scene(w, h)
    size = 16
    while size > 14 and sum(col_widths(headers, rows, size, 0.24)) > w - 2.0:
        size -= 1
    rh = 0.5
    x0, ytop = 0.1, h - 1.35
    colw = col_widths(headers, rows, size, 0.24)
    r, c = cell
    hl = {(r + 1, c): GOLD}
    grid(s, x0, ytop, headers, rows, size=size, rh=rh, hl=hl, colw=colw)
    tabw = sum(colw)
    ybot = ytop - (len(rows) + 1) * rh
    cx = x0 + sum(colw[:c]) + colw[c] / 2
    ry0 = ytop - (r + 2) * rh
    # table label
    s.text(x0, h - 0.25, f'Table: the whole grid is the {tab} tab', size=16, weight='bold', ha='left')
    # variable (column)
    outline(s, x0 + sum(colw[:c]), ybot, colw[c], (len(rows) + 1) * rh, color=INK, lw=3.0)
    s.text(cx, h - 0.78, 'Variable (feature, field): one column', size=16, weight='bold', color=INK)
    s.arrow(cx, h - 0.98, cx, ytop + 0.06, color=INK, lw=2.2, head=14)
    # record (row)
    outline(s, x0, ry0, tabw, rh, color=RED, lw=3.0)
    s.line(x0 + tabw + 0.12, ry0 + 0.04, x0 + tabw + 0.12, ry0 + rh - 0.04, color=RED, lw=2.4)
    lx = x0 + tabw + 0.28
    for i, ln in enumerate(['Record', '(observation,', 'instance):', 'one row']):
        s.text(lx, ry0 + rh / 2 + 0.36 - i * 0.25, ln, size=16, weight='bold' if i == 0 else 'normal', color=RED, ha='left')
    # cell
    s.text(cx, 0.3, f'Cell: one value, here {rows[r][c]}', size=16, weight='bold')
    s.arrow(cx, 0.52, cx, ybot + 0.03, color=INK, lw=2.2, head=14)
    return s


# ------------------------------------------------------------------ granularity
@fig('x_ds_granularity')
def ds_granularity(w, h, levels=(), **_):
    s = Scene(w, h)
    size, rh = 15, 0.4
    total = sum(0.36 + (len(l['rows']) + 1) * rh for l in levels) + 0.2 * (len(levels) - 1)
    y = h - 0.05 - max(0, (h - 0.1 - total) / 2)
    for l in levels:
        s.text(0.1, y - 0.18, l['title'], size=16, weight='bold', ha='left')
        y -= 0.36
        colw, yb = grid(s, 0.1, y, l['headers'], l['rows'], size=size, rh=rh, hl={(i + 1, 0): GOLD for i in range(len(l['rows']))})
        n = len(l['rows'])
        tag(s, 0.1 + sum(colw) + 0.25, y - (len(l['rows']) + 1) * rh / 2, f'{n} record' + ('s' if n != 1 else ''), fill=GOLD)
        y = yb - 0.2
    return s


# ------------------------------------------------------------------ variable types over data types
@fig('x_ds_types')
def ds_types(w, h, **_):
    s = Scene(w, h)
    cols = [('Numeric', [('Discrete: counted', 'e.g. quantity'), ('Continuous: measured', 'e.g. order_value_ugx, in UGX')], 'integer or float'),
            ('Categorical', [('Nominal: no order', 'e.g. payment_method'), ('Ordinal: has an order', 'e.g. loyalty_tier: Basic, Silver, Gold')], 'string, or an integer code'),
            ('Datetime', [('A date or a time', 'e.g. order_date'), ('Sorts in time order', 'e.g. week_start')], 'datetime (here: a string)'),
            ('Text', [('Free words', 'e.g. message in feedback.csv'), ('Needs special tools', 'We meet them in Session 21')], 'string')]
    gap = 0.2
    cw = (w - 0.1 - gap * 3) / 4
    y = h - 0.05
    s.text(0.05, y - 0.16, 'Variable type: how a value is measured', size=17, weight='bold', ha='left')
    y -= 0.38
    hb = 0.5
    for i, (head, subs, stored) in enumerate(cols):
        x = 0.05 + i * (cw + gap)
        s.box(x, y - hb, cw, hb, head, size=19, fill=INK, edge=INK, color=PAPER, weight='bold', r=0.06)
    y -= hb + 0.08
    sh = 1.0
    for k in range(2):
        for i, (head, subs, stored) in enumerate(cols):
            x = 0.05 + i * (cw + gap)
            s.box(x, y - sh, cw, sh, '', fill=PAPER, edge=INK, lw=1.6, r=0.06)
            hh = wrap_text(s, x + cw / 2, y - 0.08, cw - 0.2, subs[k][0], 16, 'bold', ha='center', va='top')
            wrap_text(s, x + cw / 2, y - 0.08 - hh - 0.03, cw - 0.2, subs[k][1], 15, color=BODY, ha='center', va='top')
        y -= sh + 0.08
    s.text(0.05, y - 0.16, 'Data type: how the cell stores the value', size=17, weight='bold', ha='left')
    y -= 0.36
    for i, (head, subs, stored) in enumerate(cols):
        x = 0.05 + i * (cw + gap)
        s.box(x, y - 0.5, cw, 0.5, stored, size=16, fill=PALE, edge=INK, lw=1.4, r=0.06, dash=True)
    return s


# ------------------------------------------------------------------ the primary key test
@fig('x_ds_key_test')
def ds_key_test(w, h, good=None, bad=None, **_):
    s = Scene(w, h)
    pw = (w - 0.3) / 2
    for i, d in enumerate((good, bad)):
        px = 0.1 + i * (pw + 0.1)
        s.box(px, 0.05, pw, h - 0.1, '', fill=PAPER, edge=INK, lw=2.0, r=0.07)
        s.text(px + 0.2, h - 0.38, f'{d["var"]} in {d["tab"]}', size=17, weight='bold', ha='left')
        cells = d['cells']
        rep = i == 1
        for k, v in enumerate(cells):
            s.box(px + 0.2, h - 1.0 - k * 0.37, 1.3, 0.33, v, size=14, fill=GOLD if rep else PAPER, edge=INK, lw=1.4, r=0.03)
        wrap_text(s, px + 1.7, h - 1.0 - 0.37, pw - 1.85, 'The same customer on three orders' if rep else 'Each value appears once', 14, color=BODY)
        y = h - 2.25
        for lab, f, val in (('Filled cells', d['f1'], d['filled']), ('Different values', d['f2'], d['different'])):
            s.text(px + 0.2, y, lab, size=14, color=MUTE, ha='left')
            s.text(px + pw - 0.2, y - 0.02, f'{val:,}', size=24, weight='bold', ha='right')
            s.text(px + 0.2, y - 0.38, f, size=14, mono=True, ha='left')
            y -= 0.86
        s.box(px + 0.15, 0.15, pw - 0.3, 0.8, '', fill=GOLD if not rep else PAPER, edge=INK, lw=1.8, r=0.06)
        wrap_text(s, px + pw / 2, 0.55, pw - 0.6, 'Counts match: order_id can be a primary key.' if not rep else 'Counts differ: customer_id repeats, so it is not a key.', 15, 'bold', ha='center')
    return s


# ------------------------------------------------------------------ composite key
@fig('x_ds_composite')
def ds_composite(w, h, headers=(), rows=(), total='', **_):
    s = Scene(w, h)
    size, rh = 15, 0.38
    hl = {}
    for i, r in enumerate(rows):
        if r[0] == rows[0][0]:
            hl[(i + 1, 0)] = GOLD
        if r[1] == rows[0][1]:
            hl[(i + 1, 1)] = GOLD
    x0, ytop = 0.1, h - 0.1
    colw, ybot = grid(s, x0, ytop, headers, rows, size=size, rh=rh, hl=hl)
    outline(s, x0, ybot + (len(rows) - 1) * rh, colw[0] + colw[1], rh, color=RED, lw=3.0)
    y = ybot - 0.35
    lines = [(GOLD, INK, f'{rows[0][0]} repeats: it appears {sum(1 for r in rows if r[0] == rows[0][0])} times here.'),
             (GOLD, INK, f'{headers[1]} repeats: {rows[0][1]} appears for both branches.'),
             (PAPER, RED, f'The pair ({rows[0][0]}, {rows[0][1]}) appears once, so the pair is the key.')]
    for fill, edge, t in lines:
        s.box(0.1, y - 0.14, 0.28, 0.28, '', fill=fill, edge=edge, lw=2.4 if edge == RED else 1.4, r=0.03)
        s.text(0.55, y, t, size=15, ha='left')
        y -= 0.42
    s.box(0.1, 0.1, w - 0.2, 0.5, total, size=18, fill=GOLD, edge=INK, lw=1.8, weight='bold', r=0.06)
    return s


# ------------------------------------------------------------------ foreign key
@fig('x_ds_fk')
def ds_fk(w, h, orders=(), branches=(), lookup='', result='', **_):
    s = Scene(w, h)
    size, rh = 16, 0.4
    ytop = h - 1.15
    ho, hb = ['order_id', 'branch_id'], ['branch_id', 'branch_name']
    cwo = col_widths(ho, orders, size)
    cwb = col_widths(hb, branches, size)
    xo, xb = 0.1, w - 0.1 - sum(cwb)
    s.text(xo, h - 0.25, 'orders: the many side', size=16, weight='bold', ha='left')
    s.text(xb, h - 0.25, 'branches: the one side', size=16, weight='bold', ha='left')
    tag(s, xo + cwo[0], h - 0.7, 'FK', fill=PAPER)
    tag(s, xb, h - 0.7, 'PK', fill=GOLD)
    grid(s, xo, ytop, ho, orders, size=size, rh=rh, colw=cwo, hl={(i + 1, 1): GOLD for i in range(len(orders))})
    grid(s, xb, ytop, hb, branches, size=size, rh=rh, colw=cwb, hl={(j + 1, 0): GOLD for j in range(len(branches)) if branches[j][0] in [o[1] for o in orders]})
    for i, o in enumerate(orders):
        j = [b[0] for b in branches].index(o[1])
        s.arrow(xo + sum(cwo) + 0.04, ytop - (i + 1.5) * rh, xb - 0.04, ytop - (j + 1.5) * rh, color=RED, lw=2.2, head=14)
    ybot = ytop - (max(len(orders), len(branches)) + 1) * rh
    cwid, chei = s.code(0.1, ybot - 0.3, [lookup], size=14, w=mono_w(lookup, 14) + 0.4)
    s.text(0.1, ybot - 0.3 - chei - 0.28, f'The lookup returns {result}.', size=16, weight='bold', ha='left')
    return s


# ------------------------------------------------------------------ one-to-many
@fig('x_ds_onemany')
def ds_onemany(w, h, top=None, bottom=None, **_):
    s = Scene(w, h)
    ph = (h - 0.3) / 2
    for k, d in enumerate((top, bottom)):
        y0 = h - 0.05 - k * (ph + 0.3)
        s.text(0.1, y0 - 0.2, f'{d["one_label"].capitalize()} has {d["many_label"]}', size=16, weight='bold', ha='left')
        gy = y0 - 0.45
        gh = ph - 0.5
        gx, gw = 3.9, w - 4.0
        s.box(gx, gy - gh, gw, gh, '', fill=PALE, edge=INK, lw=1.8, r=0.06)
        n = len(d['many'])
        rowh = gh / (n + 1)
        for i, v in enumerate(d['many']):
            s.box(gx + 0.2, gy - (i + 1) * rowh + 0.04, 1.5, rowh - 0.08, v, size=14, fill=PAPER, edge=INK, lw=1.4, r=0.03)
        s.text(gx + 0.2, gy - (n + 0.5) * rowh, d['more'], size=14, weight='bold', ha='left')
        cy = gy - gh / 2
        s.box(0.1, cy - 0.35, 2.3, 0.7, d['one'], size=15, fill=GOLD, edge=INK, lw=1.8, weight='bold', r=0.06)
        s.line(2.4, cy, gx, cy, color=INK, lw=2.2)
        one(s, 2.4, cy, 1, 0)
        crow(s, gx, cy, -1, 0)
        s.text(2.65, cy + 0.25, 'one', size=14, color=MUTE)
        s.text(gx - 0.5, cy + 0.25, 'many', size=14, color=MUTE)
    return s


# ------------------------------------------------------------------ entity relationship diagram
@fig('x_ds_erd')
def ds_erd(w, h, tables=(), links=(), **_):
    s = Scene(w, h)
    rh, bw = 0.27, 2.85
    gap = (w - 0.1 - 3 * bw) / 2
    cx = [0.05 + i * (bw + gap) for i in range(3)]
    ytops = [h - 0.32, h - 0.32 - 6 * rh - 0.62]
    pos = {}
    for t in tables:
        x, yt = cx[t['col']], ytops[t['row']]
        pos[t['name']] = (x, yt, t)
        s.box(x, yt - rh * 6, bw, rh * 6, '', fill=PAPER, edge=INK, lw=1.8, r=0.05, z=2)
        s.box(x, yt - rh, bw, rh, t['name'], size=16, fill=INK, edge=INK, color=PAPER, weight='bold', r=0.05, z=3)
        for i, (v, tg) in enumerate(t['rows']):
            yc = yt - rh * (i + 1.5)
            if tg == 'more':
                s.text(x + 0.12, yc, v, size=14, color=MUTE, ha='left', italic=True)
                continue
            s.text(x + 0.12, yc, v, size=15, ha='left')
            tx = x + bw - 0.1
            for part in reversed(tg.split()):
                tww = tw(part, 14, 'bold') + 0.2
                tx -= tww
                s.box(tx, yc - 0.12, tww, 0.24, part, size=14, fill=GOLD if part == 'PK' else PAPER, edge=INK, lw=1.2, weight='bold', r=0.04, z=5)
                tx -= 0.06

    def var_y(name, var):
        x, yt, t = pos[name]
        idx = [v for v, _ in t['rows']].index(var)
        return yt - rh * (idx + 1.5)

    for lk in links:
        a, av, b, bv = lk['many'], lk['many_var'], lk['one'], lk['one_var']
        ax, ayt, _ = pos[a]
        bx, byt, _ = pos[b]
        kind = lk.get('route', 'auto')
        if kind == 'over':
            xa, xb = ax + bw * 0.62, bx + bw * 0.62
            ya, yb, yo = ayt, byt, h - 0.1
            pts = [(xa, ya), (xa, yo), (xb, yo), (xb, yb)]
            s_ends = ((xa, ya, 0, 1), (xb, yb, 0, 1))
        elif ax == bx:    # vertical link
            xx = ax + bw * lk.get('at', 0.5)
            if ayt < byt:  # many side below
                ya, yb = ayt, byt - rh * 6
                s_ends = ((xx, ya, 0, 1), (xx, yb, 0, -1))
            else:
                ya, yb = ayt - rh * 6, byt
                s_ends = ((xx, ya, 0, -1), (xx, yb, 0, 1))
            pts = [(xx, ya), (xx, yb)]
        else:             # horizontal link, elbow in the gap
            if ax > bx:
                xa, xb, da, db = ax, bx + bw, -1, 1
            else:
                xa, xb, da, db = ax + bw, bx, 1, -1
            ya, yb = var_y(a, av), var_y(b, bv)
            xm = (xa + xb) / 2
            pts = [(xa, ya), (xm, ya), (xm, yb), (xb, yb)]
            s_ends = ((xa, ya, da, 0), (xb, yb, db, 0))
        for p, q in zip(pts, pts[1:]):
            s.line(p[0], p[1], q[0], q[1], color=INK, lw=2.0, z=1)
        (x1, y1, dx1, dy1), (x2, y2, dx2, dy2) = s_ends
        crow(s, x1, y1, dx1, dy1)
        one(s, x2, y2, dx2, dy2)
    return s


# ------------------------------------------------------------------ one order through four tabs
@fig('x_ds_trace')
def ds_trace(w, h, order=(), lines=(), products=(), branch=(), **_):
    s = Scene(w, h)
    size = 16
    rh = 0.38
    # left column: orders, branches (variable and value)
    lw_ = 3.85
    xl, xr = 0.05, 5.0
    ytop1 = h - 0.45
    ybr = ytop1 - (len(order) * rh) - 0.85
    # orders
    s.text(xl, h - 0.2, 'orders: one record', size=16, weight='bold', ha='left')
    cw1 = col_widths(['', ''], order, size, 0.3)
    s.table(xl, ytop1, cw1, rh, [list(r) for r in order], header=False, size=size, align=['left', 'left'], hl_cells={(2, 1): GOLD, (0, 0): PALE, (1, 0): PALE, (2, 0): PALE, (3, 0): PALE})
    # order lines
    hl_ = ['line_id', 'product_id', 'quantity', 'line_revenue_ugx']
    s.text(xr, h - 0.2, 'order_lines: two records for this order', size=16, weight='bold', ha='left')
    cw2, y2b = grid(s, xr, ytop1, hl_, lines, size=size, rh=0.4)
    # branches
    s.text(xl, ybr + 0.3, 'branches: one record', size=16, weight='bold', ha='left')
    cw3 = col_widths(['', ''], branch, size, 0.3)
    s.table(xl, ybr, cw3, rh, [list(r) for r in branch], header=False, size=size, align=['left', 'left'], hl_cells={(i, 0): PALE for i in range(len(branch))})
    # products
    s.text(xr, ybr + 0.3, 'products: one record for each product', size=16, weight='bold', ha='left')
    hp = ['product_id', 'product_name', 'unit_price_ugx']
    grid(s, xr, ybr, hp, products, size=size, rh=0.4)
    # arrows and key labels
    ya = ytop1 - rh
    s.arrow(xl + sum(cw1) + 0.04, ya, xr - 0.04, ya, color=RED, lw=2.4, head=16)
    s.circle(xl + sum(cw1) + 0.3, ya + 0.3, 0.16, fill=GOLD, edge=INK, lw=1.6, z=5)
    s.text(xl + sum(cw1) + 0.3, ya + 0.3, '1', size=14, weight='bold', z=6)
    s.text(xl + sum(cw1) + 0.5, ya - 0.27, 'order_id', size=14, color=RED, weight='bold', ha='left')
    xv = xl + 1.6
    s.arrow(xv, ytop1 - len(order) * rh - 0.04, xv, ybr + 0.62, color=RED, lw=2.4, head=16)
    s.circle(xv + 0.3, (ytop1 - len(order) * rh + ybr + 0.62) / 2, 0.16, fill=GOLD, edge=INK, lw=1.6, z=5)
    s.text(xv + 0.3, (ytop1 - len(order) * rh + ybr + 0.62) / 2, '3', size=14, weight='bold', z=6)
    s.text(xv + 0.55, (ytop1 - len(order) * rh + ybr + 0.62) / 2, 'branch_id', size=14, color=RED, weight='bold', ha='left')
    xp = xr + cw2[0] + cw2[1] / 2
    ymid = (y2b + ybr + 0.62) / 2
    s.arrow(xp, y2b - 0.04, xp, ybr + 0.62, color=RED, lw=2.4, head=16)
    s.circle(xp + 0.3, ymid, 0.16, fill=GOLD, edge=INK, lw=1.6, z=5)
    s.text(xp + 0.3, ymid, '2', size=14, weight='bold', z=6)
    s.text(xp + 0.55, ymid, 'product_id', size=14, color=RED, weight='bold', ha='left')
    return s


# ------------------------------------------------------------------ a spreadsheet excerpt with flagged cells
@fig('x_ds_flagged_sheet')
def ds_flagged_sheet(w, h, headers=(), rows=(), flags=(), **_):
    s = Scene(w, h)
    size, rh = 16, 0.4
    x0, ytop = 0.55, h - 0.12
    colw = col_widths(headers, rows, size, 0.3)
    hl = {(r + 1, c): GOLD for r, c, _ in flags}
    grid(s, x0, ytop, headers, rows, size=size, rh=rh, hl=hl, colw=colw)
    for i in range(len(rows) + 1):
        s.text(x0 - 0.15, ytop - (i + 0.5) * rh, str(i + 1), size=14, color=GREY, ha='right')
    lx = x0 + sum(colw) + 0.45
    y = ytop - 0.1
    for r, c, t in flags:
        tg = tag(s, lx, y - 0.2, f'Row {r + 2}', fill=GOLD)
        hh = wrap_text(s, lx + tg + 0.15, y - 0.05, w - lx - tg - 0.25, t, 15, va='top')
        y -= max(0.55, hh + 0.2)
    return s
