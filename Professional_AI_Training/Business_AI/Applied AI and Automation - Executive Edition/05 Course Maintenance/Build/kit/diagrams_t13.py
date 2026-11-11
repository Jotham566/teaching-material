"""Figure kinds for Session 13 (Governance and buying). Auto-imported by diagrams.py.

t13_bridge    : what a model can or cannot do (left, with the session that taught it) and the rule that answers it (right).
t13_riskgrid  : the 5 x 5 likelihood and impact grid with the eight typical risks of the Risk Register template placed on it.
t13_dataflow  : four questions that decide where a piece of information may go (personal, confidential, internal, public).
t13_layers    : four layers of rules: the law, standards, guides, your own policy.
t13_redflags  : eight lines from the OrbitDesk proposal with the red flag each one raises.
t13_scales    : the two 1 to 5 scales of the Risk Register template (likelihood, impact) with a flat tyre and a stolen car placed (11 Nov 2026).
t13_tco       : total cost of ownership on an everyday phone contract: 0 today + 24 x UGX 100,000 = UGX 2,400,000 (11 Nov 2026).
t13_contract  : the OrbitDesk commitment drawn as three paid years with no exit, an unknown renewal and an open usage bill.
"""
from figkit import Scene, INK, BODY, MUTE, HAIR, PAPER, RED, GOLD, LayoutError, fig
import slidekit as K


def _lines(text, size, w, kind='regular'):
    return K.wrap(text, size, kind, w)


def _centered(s, x, y, w, h, text, size=15, weight='normal', color=INK, ha='center', pad=0.12):
    """Wrapped text centred vertically in a box; raises if it does not fit."""
    kind = 'bold' if weight == 'bold' else 'regular'
    ls = _lines(text, size, w - 2 * pad, kind)
    th = len(ls) * size * 1.17 / 72.0
    if th > h - 0.04:
        raise LayoutError(f'text too tall for its box: {text!r} needs {th:.2f} in, has {h - 0.04:.2f}')
    tx = x + w / 2 if ha == 'center' else x + pad
    s.text(tx, y + h / 2, '\n'.join(ls), size=size, weight=weight, color=color, ha=ha)


# ------------------------------------------------------------------ bridge
@fig('x_t13_bridge')
def x_t13_bridge(w, h, rows=(), heads=('What the model does', 'The rule you write'), size=15, **_):
    s = Scene(w, h)
    head = 0.45
    n = len(rows)
    gap = 0.1
    rh = (h - 0.05 - head - 0.06 - gap * (n - 1)) / n
    lw = w * 0.45
    rx = w * 0.55
    rw = w - rx - 0.02
    top = h - 0.02
    s.text(0.05, top - head / 2, heads[0], size=size + 1, weight='bold', ha='left')
    s.text(rx, top - head / 2, heads[1], size=size + 1, weight='bold', ha='left')
    s.line(0, top - head, w, top - head, color=INK, lw=2.2)
    for i, r in enumerate(rows):
        y = top - head - 0.06 - (i + 1) * rh - i * gap
        s.box(0.02, y, lw, rh, '', fill=PAPER, edge=INK, lw=1.6)
        tagw = K.width_in(r['when'], size - 1) + 0.2
        ls = _lines(r['what'], size, lw - tagw - 0.3, 'bold')
        if len(ls) * size * 1.17 / 72 > rh - 0.04:
            raise LayoutError('bridge left text too tall: ' + r['what'])
        s.text(0.14, y + rh / 2, '\n'.join(ls), size=size, weight='bold', ha='left')
        s.text(lw - 0.08, y + rh / 2, r['when'], size=size - 1, color=MUTE, ha='right')
        s.arrow(0.02 + lw + 0.04, y + rh / 2, rx - 0.06, y + rh / 2, lw=2.4, head=16)
        s.box(rx, y, rw, rh, '', fill=GOLD, edge=INK, lw=1.6)
        _centered(s, rx, y, rw, rh, r['rule'], size=size, ha='left', pad=0.14)
    return s


# ------------------------------------------------------------------ risk grid
@fig('x_t13_riskgrid')
def x_t13_riskgrid(w, h, risks=(), size=15, scores=False, formula=False, **_):
    """risks: [{n: 1, name: 'Data leakage', l: 3, i: 5}]; cell colour by score: High 15+, Medium 8 to 14, Low below 8."""
    s = Scene(w, h)
    cell = min((h - 0.95) / 5.0, 0.78)
    gx, gy = 0.75, 0.62
    for L in range(1, 6):
        for I in range(1, 6):
            sc = L * I
            fill = RED if sc >= 15 else (GOLD if sc >= 8 else PAPER)
            s.rect(gx + (L - 1) * cell, gy + (I - 1) * cell, cell, cell, fill=fill, edge=INK, lw=1.0, z=1)
            if scores:
                s.text(gx + (L - 1) * cell + 0.07, gy + I * cell - 0.15, str(sc), size=14, ha='left', color=PAPER if fill == RED else BODY)
    for k in range(1, 6):
        s.text(gx + (k - 0.5) * cell, gy - 0.22, str(k), size=15, weight='bold')
        s.text(gx - 0.2, gy + (k - 0.5) * cell, str(k), size=15, weight='bold')
    s.text(gx + 2.5 * cell, gy - 0.5, 'Likelihood', size=16, weight='bold')
    s.text(0.12, gy + 2.5 * cell, 'Impact', size=16, weight='bold', rot=90)
    cellspots = {}
    for r in risks:
        cellspots.setdefault((r['l'], r['i']), []).append(r)
    for (L, I), rs in cellspots.items():
        cx = gx + (L - 0.5) * cell
        cy = gy + (I - 0.5) * cell
        offs = [0.0] if len(rs) == 1 else [-0.19, 0.19]
        for r, dx in zip(rs, offs):
            s.circle(cx + dx, cy, 0.17, fill=PAPER, edge=INK, lw=2.0, z=4)
            s.text(cx + dx, cy, str(r['n']), size=14, weight='bold', z=6)
    lx = gx + 5 * cell + 0.3
    y0 = gy + 5 * cell
    s.text(lx, y0 + 0.02, 'Risk and score', size=15, weight='bold', ha='left')
    step = min(0.44, (y0 - 0.3) / (len(risks) + 3.4))
    for k, r in enumerate(sorted(risks, key=lambda q: q['n'])):
        yy = y0 - 0.32 - k * step
        lab = f"{r['n']}  {r['name']}: {r['l']} × {r['i']} = {r['l'] * r['i']}" if formula else f"{r['n']}  {r['name']}  {r['l'] * r['i']}"
        s.text(lx, yy, lab, size=15 if formula else 14, ha='left', color=INK if formula else BODY, weight='bold' if formula else 'normal')
    yy = y0 - 0.32 - len(risks) * step - 0.1
    s.rect(lx, yy - 0.09, 0.24, 0.24, fill=RED, edge=INK, lw=1.0)
    s.text(lx + 0.34, yy + 0.03, 'High 15 or more', size=14, ha='left')
    s.rect(lx, yy - 0.09 - step, 0.24, 0.24, fill=GOLD, edge=INK, lw=1.0)
    s.text(lx + 0.34, yy + 0.03 - step, 'Medium 8 to 14', size=14, ha='left')
    s.rect(lx, yy - 0.09 - 2 * step, 0.24, 0.24, fill=PAPER, edge=INK, lw=1.0)
    s.text(lx + 0.34, yy + 0.03 - 2 * step, 'Low 1 to 7', size=14, ha='left')
    return s


# ------------------------------------------------------------------ data flow
@fig('x_t13_dataflow')
def x_t13_dataflow(w, h, gates=(), size=16, **_):
    """gates: [{q: 'Does it name a living person?', out_head: 'Personal flag', out: 'text'}], last gate has no q (the default route)."""
    s = Scene(w, h)
    n = len(gates)
    gap = 0.22
    rh = (h - 0.05 - gap * (n - 1)) / n
    qw = w * 0.38
    ow = w - qw - 0.75
    ox = qw + 0.65
    for i, g in enumerate(gates):
        y = h - 0.03 - (i + 1) * rh - i * gap
        s.box(0.02, y, qw, rh, '', fill=PAPER, edge=INK, lw=1.8)
        _centered(s, 0.02, y, qw, rh, g['q'], size=size, weight='bold')
        s.arrow(0.02 + qw + 0.03, y + rh / 2, ox - 0.04, y + rh / 2, lw=2.4, head=16)
        s.text(0.02 + qw + 0.32, y + rh / 2 + 0.2, 'yes', size=14, color=MUTE)
        s.box(ox, y, ow, rh, '', fill=GOLD if i < n - 1 else PAPER, edge=INK, lw=1.8)
        txt = g['out_head'] + ': ' + g['out']
        ls = _lines(txt, size - 1, ow - 0.28)
        if len(ls) * (size - 1) * 1.17 / 72 > rh - 0.05:
            raise LayoutError('dataflow outcome too tall: ' + txt)
        s.text(ox + ow / 2, y + rh / 2, '\n'.join(ls), size=size - 1, color=INK)
        if i < n - 1:
            s.arrow(0.02 + qw / 2, y - 0.01, 0.02 + qw / 2, y - gap + 0.01, lw=2.0, head=14)
            s.text(0.02 + qw / 2 + 0.3, y - gap / 2, 'no', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ layers of rules
@fig('x_t13_layers')
def x_t13_layers(w, h, rows=(), size=18, **_):
    """rows: [{name, tag, text, hl}]. Four rows from the outside in; the last (hl) is the company's own policy."""
    s = Scene(w, h)
    n = len(rows)
    gap = 0.1
    rh = (h - 0.05 - gap * (n - 1)) / n
    c0 = 2.3
    c1 = 2.9
    for i, r in enumerate(rows):
        y = h - 0.03 - (i + 1) * rh - i * gap
        hl = bool(r.get('hl'))
        s.box(0.02, y, w - 0.04, rh, '', fill=GOLD if hl else PAPER, edge=INK, lw=1.8)
        s.text(0.2, y + rh / 2, r['name'], size=size + 2, weight='bold', ha='left')
        s.line(c0, y + 0.1, c0, y + rh - 0.1, color=INK, lw=1.0)
        _centered(s, c0, y, c1, rh, r['tag'], size=size, weight='bold', color=RED if not hl else INK)
        s.line(c0 + c1, y + 0.1, c0 + c1, y + rh - 0.1, color=INK, lw=1.0)
        _centered(s, c0 + c1, y, w - c0 - c1 - 0.02, rh, r['text'], size=size, ha='left', pad=0.2)
    return s


# ------------------------------------------------------------------ red flags
@fig('x_t13_redflags')
def x_t13_redflags(w, h, rows=(), size=15, **_):
    """rows: [{sec, quote, flag}] eight lines of the proposal, each with the red flag it raises."""
    s = Scene(w, h)
    n = len(rows)
    gap = 0.07
    rh = (h - 0.04 - gap * (n - 1)) / n
    secw, flw = 0.72, 1.5
    qw = w - secw - flw - 0.1
    for i, r in enumerate(rows):
        y = h - 0.02 - (i + 1) * rh - i * gap
        s.box(0.02, y, w - 0.04, rh, '', fill=PAPER, edge=HAIR, lw=1.0, r=0.04)
        s.text(0.14, y + rh / 2, r['sec'], size=max(14, size - 1), weight='bold', ha='left', color=MUTE)
        ls = _lines('“' + r['quote'] + '”', size, qw - 0.1)
        if len(ls) * size * 1.17 / 72 > rh - 0.03:
            raise LayoutError('redflags quote too tall: ' + r['quote'])
        s.text(secw + 0.1, y + rh / 2, '\n'.join(ls), size=size, ha='left', italic=True, color=INK)
        fx = w - flw - 0.06
        s.box(fx, y + 0.04, flw, rh - 0.08, '', fill=RED, edge=RED, lw=0, r=0.05, z=3)
        s.text(fx + flw / 2, y + rh / 2, r['flag'], size=max(14, size - 1), weight='bold', color=PAPER, z=6)
    return s


# ------------------------------------------------------------------ contract
@fig('x_t13_contract')
def x_t13_contract(w, h, size=16, **_):
    s = Scene(w, h)
    top = h - 0.1
    s.text(0.05, top - 0.15, 'What you sign in the OrbitDesk proposal', size=size + 1, weight='bold', ha='left')
    bx, by, bh = 0.1, top - 1.55, 0.95
    uw = (w - 0.2 - 1.9) / 3.0
    for k in range(3):
        s.box(bx + k * uw, by, uw - 0.06, bh, '', fill=INK, edge=INK, lw=1.0, r=0.05)
        s.text(bx + k * uw + (uw - 0.06) / 2, by + bh * 0.66, f'Year {k + 1}', size=size, weight='bold', color=PAPER)
        s.text(bx + k * uw + (uw - 0.06) / 2, by + bh * 0.3, 'USD 28,800', size=size, color=PAPER)
    s.box(bx + 3 * uw, by, 1.8, bh, '', fill=PAPER, edge=RED, lw=2.2, r=0.05, dash=True)
    s.text(bx + 3 * uw + 0.9, by + bh * 0.66, 'Year 4 on', size=size, weight='bold', color=RED)
    s.text(bx + 3 * uw + 0.9, by + bh * 0.3, 'price unknown', size=size - 1, color=RED)
    s.brace(bx, bx + 3 * uw - 0.06, by - 0.14, depth=0.16, up=True)
    s.text(bx + 1.5 * uw, by - 0.48, '36 months, no early exit', size=size, weight='bold')
    s.text(bx + 1.5 * uw, by - 0.84, 'TCO = set-up + months × fee', size=size, weight='bold', color=INK)
    s.text(bx + 1.5 * uw, by - 1.18, '= 0 + 36 × 2,400 = USD 86,400 at least', size=size, weight='bold', color=INK)
    y2 = by - 1.95
    s.box(0.1, y2 - 0.55, w - 0.2, 0.9, '', fill=GOLD, edge=INK, lw=1.6)
    s.text(w / 2, y2 - 0.1, 'On top: USD 0.40 an action, no monthly cap, and nobody defines an action', size=size, weight='bold')
    s.arrow(0.4, y2 - 0.8, w - 0.4, y2 - 0.8, color=RED, lw=2.6, head=18)
    s.text(w / 2, y2 - 1.1, 'The bill has no ceiling', size=size, color=RED, weight='bold')
    return s


# ------------------------------------------------------------------ scales
@fig('x_t13_scales')
def x_t13_scales(w, h, size=15, **_):
    """Likelihood and impact, 1 to 5, in the words of the Risk Register template (Scale sheet); a flat tyre and a stolen car placed."""
    s = Scene(w, h)
    L = ['Rare', 'Unlikely', 'Possible', 'Likely', 'Almost certain']
    I = ['Small', 'Minor', 'Moderate', 'Major', 'Severe']
    cw = 2.05
    cols = [(0.05, 'Likelihood: how probable?', L, {4: ('Flat tyre', RED), 1: ('Car stolen', INK)}),
            (w / 2 - 0.05, 'Impact: how bad?', I, {2: ('Flat tyre', RED), 5: ('Car stolen', INK)})]
    rh = (h - 0.65) / 5
    for x, head, words, marks in cols:
        s.text(x, h - 0.25, head, size=size + 1, weight='bold', ha='left')
        for k in range(5):
            v = k + 1
            y = 0.05 + k * rh
            s.box(x, y + 0.04, cw, rh - 0.08, '', fill=GOLD if v in marks else PAPER, edge=INK, lw=1.6)
            s.text(x + 0.15, y + rh / 2, f'{v}  {words[k]}', size=size, weight='bold', ha='left')
            if v in marks:
                t, col = marks[v]
                s.arrow(x + cw + 0.45, y + rh / 2, x + cw + 0.05, y + rh / 2, color=col, lw=2, head=12)
                s.text(x + cw + 0.5, y + rh / 2, t, size=size, color=col, weight='bold', ha='left')
    return s


# ------------------------------------------------------------------ total cost of ownership, everyday
@fig('x_t13_tco')
def x_t13_tco(w, h, size=16, **_):
    """A 'free' phone on a 24-month plan at UGX 100,000 a month: what you commit to is 0 + 24 x 100,000."""
    s = Scene(w, h)
    s.icon('phone', 0.55, h - 0.6, 0.8)
    s.text(1.1, h - 0.45, 'Phone today: UGX 0', size=size + 1, weight='bold', ha='left')
    s.text(1.1, h - 0.85, 'on a 24-month plan', size=size, color=BODY, ha='left')
    bw = (w - 0.5) / 12
    for k in range(24):
        r, c = divmod(k, 12)
        x = 0.25 + c * bw
        y = h - 1.75 - r * 0.5
        s.rect(x + 0.03, y, bw - 0.06, 0.4, fill=GOLD, edge=INK, lw=1.2)
    s.brace(0.25, w - 0.25, h - 2.35, depth=0.15, up=True)
    s.text(w / 2, h - 2.6, '24 months × 100,000 = 2,400,000', size=size, weight='bold')
    s.box(0.2, 0.75, w - 0.4, 0.8, '', fill=PAPER, edge=INK, lw=1.8)
    s.text(w / 2, 1.15, 'You commit to: 0 + 2,400,000 = UGX 2,400,000', size=size, weight='bold')
    s.text(w / 2, 0.35, 'Extra data bundles come on top: usage', size=size - 1, color=RED, weight='bold')
    return s
