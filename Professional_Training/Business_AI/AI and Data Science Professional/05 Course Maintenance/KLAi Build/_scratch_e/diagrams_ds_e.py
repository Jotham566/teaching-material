"""Figure kinds for Sessions 9 and 10 (pandas III and SQL for analysts), author letter e. Each is registered as x_<kind> and used as visual=dict(kind='<kind>', ...).

  ds_split_apply    split a real excerpt into groups, apply a sum, combine into one row per group
  ds_join_types     two small real tables and the result of up to four join types (rows kept, NaN or NULL gold)
  ds_fanout         one order joined to its lines: the order value repeats on every line (row multiplication)
  ds_reshape        the same numbers in long format and in wide format (pivot_table and melt)
  ds_datetime_parts a date stored as text, converted to a datetime, then split into its parts
  ds_sql_order      the order in which you write a query and the order in which the database runs it
  ds_three_valued   TRUE, FALSE and UNKNOWN for a test on a NULL value, and which rows WHERE keeps
All text is 14 pt or larger and every figure is audited for overlaps by figkit.
"""
from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PAPER, RED, GOLD, PALE, fig
import slidekit as K


def tw(t, size, kind='regular'):
    return K.width_in(str(t), size, kind)


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


def tagbox(s, x, y, text, fill=GOLD, size=14, h=0.3):
    w = tw(text, size, 'bold') + 0.22
    s.box(x, y - h / 2, w, h, text, size=size, fill=fill, edge=INK, lw=1.4, weight='bold', r=0.05, z=5)
    return w


def wrapped(s, x, y, w, text, size, weight='normal', color=INK, ha='left', va='center'):
    lines = K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', w)
    s.text(x, y, '\n'.join(lines), size=size, weight=weight, color=color, ha=ha, va=va)
    return len(lines) * size * 1.15 / 72


# ------------------------------------------------------------------ groupby: split, apply, combine
@fig('x_ds_split_apply')
def ds_split_apply(w, h, headers=(), rows=(), key=0, value=1, result_head='revenue_ugx', **_):
    """rows: the excerpt (strings); key: index of the grouping variable; value: index of the numeric variable."""
    s = Scene(w, h)
    size, rh = 15, 0.4
    groups = []
    for r in rows:
        if r[key] not in groups:
            groups.append(r[key])
    def num(t):
        return int(str(t).replace(',', ''))
    sums = {g: sum(num(r[value]) for r in rows if r[key] == g) for g in groups}
    # headings
    ytop = h - 0.55
    s.text(0.1, h - 0.22, 'The table, one record per row', size=16, weight='bold', ha='left')
    cols = [headers[key], headers[value]]
    src = [[r[key], r[value]] for r in rows]
    colw = col_widths(cols, src, size, 0.3)
    hl = {}
    shade = [GOLD, PALE, PAPER]
    for i, r in enumerate(rows):
        hl[(i + 1, 0)] = shade[groups.index(r[key]) % 3]
    grid(s, 0.1, ytop, cols, src, size=size, rh=rh, colw=colw, hl=hl)
    x1 = 0.1 + sum(colw)
    # piles
    px = x1 + 1.5
    pw = 2.7
    s.text(px, h - 0.22, f'1  Split by {headers[key]}', size=16, weight='bold', ha='left')
    ph_total = h - 0.65
    gh = (ph_total - 0.2 * (len(groups) - 1)) / len(groups)
    centres = []
    for gi, g in enumerate(groups):
        yt = h - 0.6 - gi * (gh + 0.2)
        s.box(px, yt - gh, pw, gh, '', fill=PAPER, edge=INK, lw=1.8, r=0.06)
        s.box(px, yt - 0.38, pw, 0.38, g, size=15, fill=shade[gi % 3], edge=INK, lw=1.8, weight='bold', r=0.04)
        vals = [r[value] for r in rows if r[key] == g]
        s.text(px + pw / 2, yt - 0.38 - 0.22, ' + '.join(vals), size=15, ha='center')
        s.text(px + pw / 2, yt - 0.38 - 0.5, f'sum = {sums[g]:,}', size=15, weight='bold', ha='center')
        centres.append(yt - gh / 2)
    for i, r in enumerate(rows):
        gi = groups.index(r[key])
        s.arrow(x1 + 0.08, ytop - (i + 1.5) * rh, px - 0.08, centres[gi], color=RED, lw=1.6, head=12)
    # combine
    rx = px + pw + 1.0
    s.text(rx, h - 0.22, '2 Apply the sum, 3 Combine', size=16, weight='bold', ha='left')
    res = [[g, f'{sums[g]:,}'] for g in groups]
    rcols = [headers[key], result_head]
    rcw = col_widths(rcols, res, size, 0.3)
    grid(s, rx, ytop, rcols, res, size=size, rh=rh, colw=rcw, hl={(i + 1, 0): shade[i % 3] for i in range(len(groups))})
    for gi in range(len(groups)):
        s.arrow(px + pw + 0.08, centres[gi], rx - 0.08, ytop - (gi + 1.5) * rh, color=RED, lw=1.8, head=13)
    s.text(rx, ytop - (len(groups) + 1) * rh - 0.35, f'{len(groups)} rows come back: one per group', size=15, weight='bold', ha='left')
    return s


# ------------------------------------------------------------------ join types
@fig('x_ds_join_types')
def ds_join_types(w, h, orders=(), customers=(), panels=(), null='NaN', **_):
    """orders: [(order_id, customer_id)] (blank = ''), customers: [(customer_id, loyalty_tier)], panels: [dict(title, rows [[order_id, customer_id, tier]], keeps)]. Empty cells are NaN or NULL and drawn gold."""
    s = Scene(w, h)
    size, rh = 14, 0.26
    ncol = 2
    # inputs on the left
    lw_ = 3.3
    s.text(0.05, h - 0.2, 'Left table: orders', size=15, weight='bold', ha='left')
    oh = ['order_id', 'customer_id']
    orows = [[a, b if b else null] for a, b in orders]
    cw1 = col_widths(oh, [[a, b if b else null] for a, b in orders], size, 0.22)
    grid(s, 0.05, h - 0.4, oh, orows, size=size, rh=0.34, colw=cw1, hl={(i + 1, 1): GOLD for i, r in enumerate(orows) if r[1] == null})
    y2 = h - 0.4 - (len(orows) + 1) * 0.34 - 0.5
    s.text(0.05, y2 + 0.2, 'Right table: customers', size=15, weight='bold', ha='left')
    ch = ['customer_id', 'loyalty_tier']
    cw2 = col_widths(ch, customers, size, 0.22)
    grid(s, 0.05, y2, ch, [list(r) for r in customers], size=size, rh=0.34, colw=cw2)
    s.text(0.05, y2 - (len(customers) + 1) * 0.34 - 0.3, 'Join key: customer_id', size=15, weight='bold', color=RED, ha='left')
    # panels
    n = len(panels)
    nrow = (n + ncol - 1) // ncol
    gx = 0.35
    px0 = lw_ + 0.4
    pw = (w - px0 - gx * (ncol - 1)) / ncol
    ph = min(2.05, (h - 0.05 - 0.1 * (nrow - 1)) / nrow)
    hdr = ['order_id', 'customer_id', 'loyalty_tier']
    maxrows = max(len(p['rows']) for p in panels) + 1
    for i, p in enumerate(panels):
        cx = px0 + (i % ncol) * (pw + gx)
        top = h - 0.02 - (i // ncol) * (ph + 0.1)
        if nrow == 1:
            top = h - 0.9
        s.box(cx, top - ph, pw, ph, '', fill=PAPER, edge=INK, lw=1.8, r=0.05)
        s.text(cx + 0.15, top - 0.2, p['title'], size=15, weight='bold', ha='left')
        tg = f'{len(p["rows"])} rows'
        tagbox(s, cx + pw - tw(tg, 14, 'bold') - 0.35, top - 0.2, tg)
        rows = [[(v if v else null) for v in r] for r in p['rows']]
        colw = [max(0.9, c) for c in col_widths(hdr, rows, size, 0.2)]
        hl = {}
        for ri, r in enumerate(p['rows']):
            for ci, v in enumerate(r):
                if not v:
                    hl[(ri + 1, ci)] = GOLD
        grid(s, cx + 0.15, top - 0.4, hdr, rows, size=size, rh=rh, colw=colw, hl=hl)
        if p.get('keeps'):
            s.text(cx + 0.15, top - 0.4 - maxrows * rh - 0.16, p['keeps'], size=14, color=BODY, ha='left')
    return s


# ------------------------------------------------------------------ fan-out
@fig('x_ds_fanout')
def ds_fanout(w, h, order=None, lines=(), total_each='', total_after='', **_):
    """order: dict(order_id, value); lines: [(line_id, product_id, revenue)], all strings."""
    s = Scene(w, h)
    size, rh = 14, 0.34
    n = len(lines)
    s.text(0.05, h - 0.2, 'orders: one record', size=15, weight='bold', ha='left')
    h1 = ['order_id', 'order_value_ugx']
    r1 = [[order['order_id'], order['value']]]
    cw1, yb1 = grid(s, 0.05, h - 0.4, h1, r1, size=size, rh=rh)
    x2 = 0.05 + sum(cw1) + 0.9
    s.text(x2, h - 0.2, f'order_lines: {n} records for this order', size=15, weight='bold', ha='left')
    h2 = ['line_id', 'order_id', 'line_revenue_ugx']
    r2 = [[a, order['order_id'], c] for a, b, c in lines]
    cw2, yb2 = grid(s, x2, h - 0.4, h2, r2, size=size, rh=rh)
    s.text(0.05 + sum(cw1) / 2, yb1 - 0.3, 'one-to-many', size=14, color=MUTE)
    s.arrow(0.05 + sum(cw1) + 0.08, h - 0.4 - 1.5 * rh, x2 - 0.08, h - 0.4 - 1.5 * rh, color=RED, lw=2.2, head=14)
    # result
    ytop = yb2 - 0.85
    s.arrow(0.5, yb2 - 0.1, 0.5, ytop + 0.45, color=RED, lw=2.4, head=16)
    s.text(0.75, yb2 - 0.32, "orders.merge(order_lines, on='order_id')", size=14, mono=True, ha='left')
    s.text(0.05, ytop + 0.2, f'Result: {n} rows. The order value is repeated on every row.', size=15, weight='bold', ha='left')
    h3 = ['order_id', 'order_value_ugx', 'line_id', 'line_revenue_ugx']
    r3 = [[order['order_id'], order['value'], a, c] for a, b, c in lines]
    cw3, yb3 = grid(s, 0.05, ytop, h3, r3, size=size, rh=rh, hl={(i + 1, 1): GOLD for i in range(n)})
    s.box(0.05, yb3 - 0.78, w - 0.1, 0.62, '', fill=PAPER, edge=RED, lw=2.2, r=0.05)
    s.text(w / 2, yb3 - 0.47, f'Sum of order_value_ugx after the merge: {total_after}. True order value: {total_each}.', size=15, weight='bold', color=RED)
    return s


# ------------------------------------------------------------------ long and wide
@fig('x_ds_reshape')
def ds_reshape(w, h, long_headers=(), long_rows=(), wide_headers=(), wide_rows=(), **_):
    s = Scene(w, h)
    size, rh = 15, 0.42
    s.text(0.1, h - 0.22, 'Long format: one record per branch and year', size=16, weight='bold', ha='left')
    cw1, yb1 = grid(s, 0.1, h - 0.5, long_headers, long_rows, size=size, rh=rh, hl={(i + 1, 1): GOLD for i in range(len(long_rows))})
    x2 = w - 0.1 - sum(col_widths(wide_headers, wide_rows, size, 0.3))
    s.text(x2, h - 0.22, 'Wide format: one record per branch', size=16, weight='bold', ha='left')
    cw2, yb2 = grid(s, x2, h - 0.5, wide_headers, wide_rows, size=size, rh=rh, hl={(0, c): GOLD for c in range(1, len(wide_headers))})
    xm1, xm2 = 0.1 + sum(cw1) + 0.25, x2 - 0.25
    ym = h - 0.5 - 1.6 * rh
    s.arrow(xm1, ym, xm2, ym, color=RED, lw=2.4, head=16)
    s.text((xm1 + xm2) / 2, ym + 0.3, 'pivot_table', size=16, mono=True, weight='bold', color=RED)
    s.arrow(xm2, ym - 1.0, xm1, ym - 1.0, color=INK, lw=2.4, head=16)
    s.text((xm1 + xm2) / 2, ym - 0.7, 'melt', size=16, mono=True, weight='bold')
    s.text(0.1, 0.55, 'The values are the same. The year moves from a row value to a column heading.', size=16, ha='left')
    s.text(0.1, 0.2, 'Long format suits groupby and charts. Wide format suits reading by eye.', size=16, color=BODY, ha='left')
    return s


# ------------------------------------------------------------------ datetime parts
@fig('x_ds_datetime_parts')
def ds_datetime_parts(w, h, text='', parts=(), **_):
    """parts: [(accessor, value)], for example ('.dt.month', '1')."""
    s = Scene(w, h)
    y = h - 0.9
    s.text(0.1, h - 0.22, 'Step 1: the date arrives as text', size=16, weight='bold', ha='left')
    s.box(0.1, y - 0.35, 2.4, 0.65, text, size=20, fill=PALE, edge=INK, lw=1.8, mono=True, r=0.05)
    s.text(1.3, y - 0.55, 'string (object)', size=14, color=MUTE)
    s.arrow(2.65, y - 0.03, 5.3, y - 0.03, color=RED, lw=2.4, head=16)
    s.text(3.97, y + 0.22, 'pd.to_datetime()', size=15, mono=True, weight='bold', color=RED)
    s.text(5.5, h - 0.22, 'Step 2: now it is a real date', size=16, weight='bold', ha='left')
    s.box(5.5, y - 0.35, 2.4, 0.65, text, size=20, fill=GOLD, edge=INK, lw=1.8, mono=True, r=0.05)
    s.text(6.7, y - 0.55, 'datetime64', size=14, color=MUTE)
    s.text(0.1, y - 1.0, 'Step 3: ask for one part with .dt', size=16, weight='bold', ha='left')
    per = 3
    bw = (w - 0.1 - 0.2 * (per - 1)) / per
    for i, (acc, val) in enumerate(parts):
        r, c = divmod(i, per)
        bx = 0.1 + c * (bw + 0.2)
        by = y - 1.3 - r * 1.0
        s.box(bx, by - 0.85, bw, 0.85, '', fill=PAPER, edge=INK, lw=1.8, r=0.05)
        s.text(bx + bw / 2, by - 0.25, val, size=20, weight='bold')
        s.text(bx + bw / 2, by - 0.62, acc, size=15, mono=True, color=BODY)
    return s


# ------------------------------------------------------------------ SQL: written order and running order
@fig('x_ds_sql_order')
def ds_sql_order(w, h, written=(), executed=(), hints=None, **_):
    s = Scene(w, h)
    n = len(written)
    gap = 0.12
    bw = (w - 0.1 - gap * (n - 1)) / n
    xs = {name: 0.05 + i * (bw + gap) for i, name in enumerate(written)}
    s.text(0.05, h - 0.22, 'You write the clauses in this order', size=17, weight='bold', ha='left')
    ytop = h - 0.55
    for name in written:
        s.box(xs[name], ytop - 0.55, bw, 0.55, name, size=16, fill=PALE, edge=INK, lw=1.8, weight='bold', r=0.05)
    ybot = 1.55
    s.text(0.05, 0.25, 'The database runs them in this order (gold boxes, numbered)', size=17, weight='bold', ha='left')
    for k, name in enumerate(executed):
        bx = 0.05 + k * (bw + gap)
        s.box(bx, ybot, bw, 0.55, name, size=16, fill=GOLD, edge=INK, lw=1.8, weight='bold', r=0.05)
        s.circle(bx + 0.18, ybot + 0.65 + 0.0, 0.16, fill=INK, edge=INK)
        s.text(bx + 0.18, ybot + 0.65, str(k + 1), size=14, weight='bold', color=PAPER, z=7)
        if hints:
            wrapped(s, bx + bw / 2, ybot - 0.12, bw, hints[name], 14, color=BODY, ha='center', va='top')
        s.line(xs[name] + bw / 2, ytop - 0.55, bx + bw / 2, ybot + 0.55, color=RED, lw=1.6, z=1)
    return s


# ------------------------------------------------------------------ NULL and three-valued logic
@fig('x_ds_three_valued')
def ds_three_valued(w, h, test='', rows=(), counts=(), **_):
    """rows: [(order_id, customer_id text, result 'TRUE'|'FALSE'|'UNKNOWN')]; counts: [(label, number string)]."""
    s = Scene(w, h)
    size, rh = 15, 0.42
    s.text(0.05, h - 0.22, f'Test written in WHERE:  {test}', size=16, weight='bold', ha='left')
    hdr = ['order_id', 'customer_id', 'test gives', 'WHERE keeps the row?']
    body = [[a, b, c, 'yes' if c == 'TRUE' else 'no'] for a, b, c in rows]
    colw = col_widths(hdr, body, size, 0.24)
    hl = {}
    for i, r in enumerate(rows):
        if r[2] == 'UNKNOWN':
            for c in range(4):
                hl[(i + 1, c)] = GOLD
    cw, yb = grid(s, 0.05, h - 0.5, hdr, body, size=size, rh=rh, colw=colw, hl=hl)
    y = yb - 0.3
    wrapped(s, 0.05, y - 0.25, w - 0.1, 'A missing value (NULL) means unknown. Is an unknown value different from C0495? SQL answers UNKNOWN, and WHERE keeps only TRUE.', 16, 'bold', ha='left', va='center')
    y -= 0.95
    cwid = (w - 0.1 - 0.2 * (len(counts) - 1)) / len(counts)
    for i, (lab, num) in enumerate(counts):
        bx = 0.05 + i * (cwid + 0.2)
        s.box(bx, y - 0.95, cwid, 0.95, '', fill=GOLD if lab.startswith('UNKNOWN') else PAPER, edge=INK, lw=1.8, r=0.05)
        s.text(bx + cwid / 2, y - 0.3, num, size=22, weight='bold')
        wrapped(s, bx + cwid / 2, y - 0.62, cwid - 0.1, lab, 14, color=INK, ha='center', va='top')
    return s
