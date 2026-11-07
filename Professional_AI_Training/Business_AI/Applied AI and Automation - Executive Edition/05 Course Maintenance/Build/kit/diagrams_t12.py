"""Figures for Session 12, Workflow mapping (v3, 6 November 2026).

t12_map        a mapped workflow in swim lanes: trigger, steps, handoffs between people, the check
t12_decide     each step of the map tagged rule, AI step, agent or person
t12_side       the same twelve customer messages: the rule router and the AI sort side by side (reused records)
t12_hours      hours saved, worked by hand: 4 x 80 = 320 minutes (5.3 hours) before review; 4 x 60 = 240 minutes (4 hours) after 20 minutes of review
t12_assistant  a sketch of a personal email assistant: what goes in, its permissions, what comes out, the approval step
t12_tea        everyday first: making tea as a workflow (trigger, steps, handoff, check)
t12_standing   everyday rule-based automation: a bank standing order (trigger date, fixed rule, statement check)
t12_kettle     everyday baseline, net benefit, ROI and payback period: an electric kettle against charcoal (invented round numbers)
"""
from figkit import Scene, INK, BODY, MUTE, HAIR, PAPER, RED, GOLD, GREY, fig
import slidekit as K


def _w(s, x, y, w, text, size, weight='normal', color=INK, ha='center', va='center'):
    lines = K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', w)
    s.text(x, y, '\n'.join(lines), size=size, weight=weight, color=color, ha=ha, va=va)
    return len(lines) * size * 1.15 / 72


LANES = ['Customer', 'Customer Service', 'Finance']
MAP_STEPS = [  # lane, column, head, tag
    (0, 0, 'Message arrives', 'trigger'),
    (1, 1, 'Read and sort', None),
    (1, 2, 'Draft a reply', None),
    (2, 2, 'Confirm payment', None),
    (1, 3, 'Check and send', 'check'),
]


@fig('x_t12_map')
def x_t12_map(w, h, tags=False, **_):
    s = Scene(w, h)
    lw = 2.3
    n = len(LANES)
    lh = (h - 0.1) / n
    cols = 4
    cw = (w - lw - 0.1) / cols
    for i, lane in enumerate(LANES):
        y = h - 0.05 - (i + 1) * lh
        s.rect(0.05, y, w - 0.1, lh, fill=PAPER, edge=HAIR, lw=1.2)
        _w(s, 0.05 + lw / 2, y + lh / 2, lw - 0.3, lane, 17, 'bold')
    s.line(0.05 + lw, 0.05, 0.05 + lw, h - 0.05, color=INK, lw=1.6)
    centres = {}
    tagmap = {'Read and sort': ('AI step', GOLD), 'Draft a reply': ('AI step', GOLD), 'Confirm payment': ('Rule', PAPER), 'Check and send': ('Person', PAPER), 'Message arrives': ('Trigger', PAPER)}
    bw, bh = cw - 0.35, min(0.95, lh - 0.3)
    for lane, col, head, tag in MAP_STEPS:
        x = 0.05 + lw + col * cw + 0.18
        yc = h - 0.05 - (lane + 0.5) * lh
        fill = GOLD if tag == 'check' else PAPER
        if tags:
            fill = tagmap[head][1]
        s.box(x, yc - bh / 2, bw, bh, '', fill=fill, edge=RED if tag == 'trigger' else INK, lw=2.0, z=3)
        if tags:
            _w(s, x + bw / 2, yc + 0.17, bw - 0.15, head, 15, 'bold')
            s.text(x + bw / 2, yc - 0.25, tagmap[head][0], size=14, color=RED if tagmap[head][0] == 'Person' else BODY, weight='bold')
        else:
            _w(s, x + bw / 2, yc, bw - 0.15, head, 16, 'bold')
        centres[head] = (x, yc, x + bw)
    def link(a, b, label=None):
        ax0, ay, ax1 = centres[a]
        bx0, by, bx1 = centres[b]
        if abs(ay - by) < 0.01:
            s.arrow(ax1 + 0.03, ay, bx0 - 0.03, by, lw=2.2, head=15)
        else:
            s.arrow((ax0 + ax1) / 2, ay - bh / 2 if by < ay else ay + bh / 2, (bx0 + bx1) / 2 if bx0 == ax0 else bx0 - 0.03, by + (bh / 2 if (by < ay and bx0 == ax0) else 0) if bx0 == ax0 else by,
                    lw=2.2, head=15, color=RED if label else INK)
    link('Message arrives', 'Read and sort')
    link('Read and sort', 'Draft a reply')
    link('Draft a reply', 'Check and send')
    # handoff to finance and back
    dx0, dy, dx1 = centres['Draft a reply']
    fx0, fy, fx1 = centres['Confirm payment']
    s.arrow((dx0 + dx1) / 2 - 0.3, dy - bh / 2 - 0.02, (fx0 + fx1) / 2 - 0.3, fy + bh / 2 + 0.02, lw=2.2, head=15, color=RED)
    s.arrow((fx0 + fx1) / 2 + 0.3, fy + bh / 2 + 0.02, (dx0 + dx1) / 2 + 0.3, dy - bh / 2 - 0.02, lw=2.2, head=15, color=RED)
    return s


@fig('x_t12_side')
def x_t12_side(w, h, **_):
    s = Scene(w, h)
    ids = ['M01', 'M02', 'M03', 'M07', 'M10', 'M14', 'M15', 'M21', 'M26', 'M28', 'M32', 'M38']
    rule = ['r', 'r', 'w', 'w', 'w', 'r', 'r', 'r', 'r', 'r', 'w', 'w']
    ai = ['r', 'r', 'r', 'r', 'r', 'w', 'r', 'r', 'u', 'u', 'r', 'r']
    lw = 2.6
    n = len(ids)
    cw = (w - lw - 0.1) / n
    rh = (h - 0.5) / 3.3
    top = h - 0.05
    for j, m in enumerate(ids):
        s.text(lw + (j + 0.5) * cw, top - 0.3, m, size=15, weight='bold')
    rows = [('Rule router', rule, '7 of 12'), ('AI sort, 3 runs', ai, '9 exact, 11 acceptable')]
    for i, (name, marks, total) in enumerate(rows):
        yc = top - 0.6 - (i + 0.5) * rh * 1.15
        s.text(0.1, yc + 0.18, name, size=17, weight='bold', ha='left')
        s.text(0.1, yc - 0.22, total, size=14, color=RED if i == 0 else BODY, ha='left', weight='bold')
        for j, mk in enumerate(marks):
            x = lw + (j + 0.5) * cw
            r = min(cw, rh) * 0.36
            if mk == 'r':
                s.icon('check', x, yc, r * 2.6)
            elif mk == 'w':
                s.icon('cross', x, yc, r * 2.6)
            else:
                s.circle(x, yc, r * 0.8, fill=PAPER, edge=INK, lw=2)
                s.text(x, yc, '?', size=16, weight='bold')
        s.line(0.05, yc - rh * 0.6, w - 0.05, yc - rh * 0.6, color=HAIR, lw=1)
    s.text(0.1, 0.25, '?  UNSURE, sent to a person: acceptable', size=15, color=BODY, ha='left')
    s.text(w - 0.1, 0.25, 'Different measures: a queue for the rule, a category for the AI', size=14, color=MUTE, ha='right')
    return s


@fig('x_t12_hours')
def x_t12_hours(w, h, **_):
    """Minutes per run today, with the new routine, and with the 20 minutes of review added; both monthly totals."""
    s = Scene(w, h)
    x0 = 0.4
    unit = (w - 1.6) / 95
    rows = [('Today, by hand', [(90, PAPER)], '90 min'), ('New routine, before review', [(10, GOLD)], '10 min'),
            ('New routine plus review', [(10, GOLD), (20, GREY)], '10 + 20 review = 30 min')]
    bh, step = 0.4, 0.8
    for i, (lab, parts, txt) in enumerate(rows):
        y = h - 0.75 - i * step
        s.text(x0, y + 0.38, lab, size=15, weight='bold', ha='left')
        x = x0
        for m, fill in parts:
            s.rect(x, y - bh / 2, m * unit, bh, fill=fill, edge=INK, lw=2)
            x += m * unit
        s.text(x + 0.15, y, txt, size=15, weight='bold', ha='left')
    fy = h - 0.75 - 2 * step - 0.55  # the formula, under the bars
    s.text(x0, fy, 'Hours saved  H = n × (t₀ − t₁) ÷ 60', size=17, weight='bold', ha='left')
    s.text(x0, fy - 0.33, 'n runs a month, t₀ minutes today, t₁ minutes with the new routine', size=14, color=BODY, ha='left')
    s.box(0.3, 0.05, w - 0.6, 1.05, '', fill=PAPER, edge=INK, lw=1.8)
    s.text(w / 2, 0.79, 'Before review:  4 × (90 − 10) = 320 min ÷ 60 ≈ 5.3 hours a month', size=16, weight='bold')
    s.text(w / 2, 0.36, 'After review:  4 × (90 − 30) = 240 min ÷ 60 = 4 hours a month', size=16, weight='bold', color=RED)
    return s


@fig('x_t12_money')
def x_t12_money(w, h, **_):
    """A month in money for the NVF plan example: two gains, one cost, the net (invented inputs, recomputed from the workbook)."""
    s = Scene(w, h)
    items = [('Time saved', 160000, PAPER, '+160,000'), ('Errors avoided', 144000, PAPER, '+144,000'),
             ('Running cost', -145000, RED, '−145,000'), ('Net a month', 159000, INK, '159,000')]
    x0, base, top = 0.7, 0.95, h - 0.7
    unit = (top - base) / 320000.0
    bw, gap = (w - x0 - 0.3) / 4 - 0.25, 0.25
    s.line(x0 - 0.1, base, w - 0.2, base, color=INK, lw=2)
    run = 0
    for i, (lab, v, col, txt) in enumerate(items):
        x = x0 + i * (bw + gap)
        if i == 3:
            lo, hi = 0, v
        elif v >= 0:
            lo, hi = run, run + v
            run += v
        else:
            lo, hi = run + v, run
            run += v
        s.rect(x, base + lo * unit, bw, (hi - lo) * unit, fill=col if col != INK else GOLD, edge=INK, lw=2)
        s.text(x + bw / 2, base + hi * unit + 0.25, txt, size=16, weight='bold', color=RED if v < 0 else INK)
        s.text(x + bw / 2, base - 0.35, lab, size=15, weight='bold')
    s.text(w / 2, h - 0.2, 'UGX a month, invented NVF plan', size=15, color=MUTE)
    return s


@fig('x_t12_assistant')
def x_t12_assistant(w, h, **_):
    s = Scene(w, h)
    cx = w / 2
    bw = 2.2
    yb = h / 2 + 0.25
    s.box(cx - bw / 2, yb - 0.85, bw, 1.7, '', fill=GOLD, edge=INK, lw=2.2)
    s.icon('robot', cx, yb + 0.35, 0.7)
    s.text(cx, yb - 0.25, 'Assistant', size=17, weight='bold')
    s.text(cx, yb - 0.58, 'level 2: drafts', size=14, color=BODY)
    ins = [('mail', 'Mailbox'), ('doc', 'Your rules')]
    outs = [('chart', 'Summary'), ('speech', 'Drafts')]
    for i, ((ic, t), (oc, ot)) in enumerate(zip(ins, outs)):
        y = yb + 0.55 - i * 1.1
        s.icon(ic, 0.4, y, 0.55)
        s.text(0.8, y, t, size=15, ha='left')
        s.arrow(2.1, y, cx - bw / 2 - 0.05, y, lw=2, head=14)
        s.arrow(cx + bw / 2 + 0.05, y, w - 2.05, y, lw=2, head=14)
        s.icon(oc, w - 1.75, y, 0.55)
        s.text(w - 1.38, y, ot, size=15, ha='left')
    s.box(0.3, 0.1, w - 0.6, 0.75, '', fill=PAPER, edge=RED, lw=2.2)
    s.text(w / 2, 0.47, 'Human-in-the-loop: you send. It never sends, pays or deletes.', size=16, weight='bold', color=RED)
    return s


@fig('x_t12_tea')
def x_t12_tea(w, h, **_):
    """Everyday workflow: making morning tea. Trigger, three steps, a handoff (red arrow) and a check (gold)."""
    s = Scene(w, h)
    parts = [('Trigger', 'Alarm at 6:30', PAPER, RED), ('Step 1', 'Boil the water', PAPER, INK), ('Step 2', 'Brew 3 minutes', PAPER, INK),
             ('Step 3', 'Add milk and sugar', PAPER, INK), ('Check', 'Taste it', GOLD, INK)]
    n = len(parts)
    gap = 0.4
    bw = (w - 0.1 - gap * (n - 1)) / n
    y0, bh = h - 2.0, 1.6
    for i, (head, sub, fill, edge) in enumerate(parts):
        x = 0.05 + i * (bw + gap)
        s.box(x, y0, bw, bh, '', fill=fill, edge=edge, lw=2.2)
        s.text(x + bw / 2, y0 + bh - 0.4, head, size=17, weight='bold', color=RED if edge == RED else INK)
        _w(s, x + bw / 2, y0 + 0.55, bw - 0.15, sub, 16, color=BODY)
        if i < n - 1:
            s.arrow(x + bw + 0.03, y0 + bh / 2, x + bw + gap - 0.03, y0 + bh / 2, lw=2.2, head=14, color=RED if i == 3 else INK)
    # the handoff: the cup passes to someone else before the check
    s.text(0.05 + 4 * (bw + gap) - gap / 2, y0 - 0.3, 'handoff', size=15, weight='bold', color=RED)
    s.box(0.3, 0.1, w - 0.6, y0 - 0.75, '', fill=PAPER, edge=INK, lw=1.6)
    _w(s, w / 2, (y0 - 0.65) / 2 + 0.1, w - 1.0, 'The cup passes from you to the person who drinks it. That handoff is where a wait or a mistake shows.', 18)
    return s


@fig('x_t12_standing')
def x_t12_standing(w, h, **_):
    """Everyday rule-based automation: a bank standing order runs every month without you; you check the statement."""
    s = Scene(w, h)
    y0, bh = h - 2.1, 1.7
    bw = (w - 0.1 - 2 * 0.55) / 3
    boxes = [('calendar', 'Trigger', 'The 25th of each month'), ('gear', 'Rule', 'Pay UGX 500,000 to the landlord'), ('receipt', 'Check', 'You read the statement')]
    for i, (ic, head, sub) in enumerate(boxes):
        x = 0.05 + i * (bw + 0.55)
        s.box(x, y0, bw, bh, '', fill=GOLD if i == 1 else PAPER, edge=RED if i == 0 else INK, lw=2.2)
        s.icon(ic, x + 0.45, y0 + bh - 0.45, 0.55)
        s.text(x + 0.9, y0 + bh - 0.45, head, size=17, weight='bold', ha='left')
        _w(s, x + bw / 2, y0 + 0.5, bw - 0.25, sub, 15, color=INK)
        if i < 2:
            s.arrow(x + bw + 0.04, y0 + bh / 2, x + bw + 0.51, y0 + bh / 2, lw=2.4, head=16)
    s.box(0.3, 0.1, w - 0.6, y0 - 0.45, '', fill=PAPER, edge=INK, lw=1.6)
    _w(s, w / 2, (y0 - 0.35) / 2 + 0.1, w - 1.0, 'The same rule every time, no judgement. When the rent changes, a person changes the rule.', 18)
    return s


@fig('x_t12_kettle')
def x_t12_kettle(w, h, **_):
    """Everyday business case: an electric kettle replaces charcoal for tea. Invented round numbers."""
    s = Scene(w, h)
    rows = [['Item', 'Formula', 'UGX'],
            ['Baseline: charcoal for tea', 'measured today', '30,000 a month'],
            ['After: electricity for the kettle', 'measured after', '10,000 a month'],
            ['Saving', '30,000 − 10,000', '20,000 a month'],
            ['One-off cost: the kettle', 'price paid', '60,000'],
            ['Payback period', '60,000 ÷ 20,000', '3 months'],
            ['Net benefit, first year', '12 × 20,000 − 60,000', '180,000'],
            ['ROI, first year', '180,000 ÷ 60,000 × 100%', '300%']]
    cw = [(w - 0.1) * 0.38, (w - 0.1) * 0.38, (w - 0.1) * 0.24]
    s.table(0.05, h - 0.05, cw, (h - 0.15) / len(rows), rows, size=15, align=['left', 'left', 'left'],
            hl_cells={(5, 2): GOLD, (6, 2): GOLD, (7, 2): GOLD})
    return s
