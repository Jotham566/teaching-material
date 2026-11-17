"""Figures for Session 12, Workflow mapping (v3, 6 November 2026).

t12_map        a mapped workflow in swim lanes: trigger, steps, handoffs between people, the check
t12_decide     each step of the map tagged rule, AI step, agent or person
t12_side       the same twelve customer messages: the rule router and the AI sort side by side (reused records)
t12_hours      hours saved, worked by hand first (90 - 10 = 80; 4 x 80 = 320; 320 / 60 = 5.3), then the formula with each symbol named
t12_assistant  a sketch of a personal email assistant: what goes in, its permissions, what comes out, the approval step
t12_tea        everyday first: making tea as a workflow (trigger, steps, handoff, check)
t12_standing   everyday rule-based automation: a bank standing order (trigger date, fixed rule, statement check)
t12_teamap     the tea workflow drawn as a workflow map: one lane per person, the handoff crossing lanes (11 Nov 2026)
t12_aistep     an AI step: a spam filter makes one judgement inside a fixed path (11 Nov 2026)
t12_agent      an agent: a goal, a loop of plan, act, observe, tools, and an approval step before anything that commits you (11 Nov 2026)
t12_baseline   kettle: the baseline (charcoal 30,000 a month), the new running cost (10,000) and the net saving (20,000); the one-off cost (60,000)
t12_payback    kettle: savings added up month by month until they reach the 60,000 one-off cost (month 3)
t12_roi        kettle: first-year benefits 360,000 against first-year costs 180,000; net benefit 180,000; ROI 100%
t12_benefits   NVF: the two monthly benefits worked in UGX (time saved 160,000; errors avoided 144,000)
t12_costs      NVF: one-off cost 480,000 and monthly running cost 145,000, line by line from the workbook
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


@fig('x_t12_hours')
def x_t12_hours(w, h, **_):
    """Minutes per run today and with the new routine, then the hours saved worked step by step, then the formula."""
    s = Scene(w, h)
    x0 = 0.3
    unit = (w - 2.4) / 90
    rows = [('Today, by hand (baseline)', 90, PAPER, '90 min'), ('New routine, your own work', 10, GOLD, '10 min')]
    for i, (lab, m, fill, txt) in enumerate(rows):
        y = h - 0.65 - i * 0.85
        s.text(x0, y + 0.36, lab, size=15, weight='bold', ha='left')
        s.rect(x0, y - 0.18, m * unit, 0.36, fill=fill, edge=INK, lw=2)
        s.text(x0 + m * unit + 0.15, y, txt, size=15, weight='bold', ha='left')
    steps = [('Saved each run', '90 − 10 = 80 minutes'), ('Saved a month (4 runs)', '4 × 80 = 320 minutes'), ('In hours (60 minutes = 1 hour)', '320 ÷ 60 ≈ 5.3 hours')]
    y = h - 2.45
    for lab, calc in steps:
        s.text(x0, y, lab, size=15, color=BODY, ha='left')
        s.text(w - 0.3, y, calc, size=16, weight='bold', ha='right')
        s.line(x0, y - 0.22, w - 0.3, y - 0.22, color=HAIR, lw=1)
        y -= 0.48
    s.box(0.2, 0.05, w - 0.4, 0.95, '', fill=PAPER, edge=INK, lw=1.8)
    s.text(w / 2, 0.72, 'Hours saved = n × (t₀ − t₁) ÷ 60', size=17, weight='bold')
    s.text(w / 2, 0.33, 'n = runs a month (4), t₀ = minutes today (90), t₁ = minutes after (10)', size=14, color=BODY)
    return s


@fig('x_t12_teamap')
def x_t12_teamap(w, h, **_):
    """The tea workflow as a map: lane 'You' and lane 'Your guest'; the handoff is the red arrow that crosses lanes."""
    s = Scene(w, h)
    lw_ = 1.55
    lanes = ['You', 'Your guest']
    lh = (h - 0.95) / 2
    for i, lane in enumerate(lanes):
        y = h - 0.05 - (i + 1) * lh
        s.rect(0.05, y, w - 0.1, lh, fill=PAPER, edge=HAIR, lw=1.2)
        s.text(0.05 + lw_ / 2, y + lh / 2, lane, size=17, weight='bold')
    s.line(0.05 + lw_, h - 0.05 - 2 * lh, 0.05 + lw_, h - 0.05, color=INK, lw=1.6)
    cols = 4
    cw = (w - lw_ - 0.15) / cols
    bw, bh = cw - 0.3, 0.95
    def bx(col):
        return 0.05 + lw_ + 0.15 + col * cw
    y1 = h - 0.05 - lh / 2
    y2 = h - 0.05 - 1.5 * lh
    items = [(0, y1, 'Alarm 6:30', RED, PAPER), (1, y1, 'Boil water', INK, PAPER), (2, y1, 'Brew, add milk', INK, PAPER), (3, y2, 'Taste it', INK, GOLD)]
    for col, yc, t, edge, fill in items:
        s.box(bx(col), yc - bh / 2, bw, bh, '', fill=fill, edge=edge, lw=2.2, z=3)
        _w(s, bx(col) + bw / 2, yc, bw - 0.15, t, 15, 'bold')
    for c in (0, 1):
        s.arrow(bx(c) + bw + 0.03, y1, bx(c + 1) - 0.03, y1, lw=2.2, head=14)
    s.arrow(bx(2) + bw / 2, y1 - bh / 2 - 0.03, bx(3) + 0.05, y2 + 0.1, lw=2.6, head=16, color=RED)
    s.text(bx(2) + bw / 2 - 0.05, (y1 + y2) / 2 - 0.15, 'handoff', size=15, weight='bold', color=RED, ha='right')
    ky = 0.35
    s.rect(0.15, ky - 0.13, 0.3, 0.26, fill=PAPER, edge=RED, lw=2)
    s.text(0.55, ky, 'trigger', size=14, ha='left')
    s.line(1.55, ky, 2.05, ky, color=RED, lw=2.6)
    s.text(2.15, ky, 'handoff', size=14, ha='left')
    s.rect(3.25, ky - 0.13, 0.3, 0.26, fill=GOLD, edge=INK, lw=2)
    s.text(3.65, ky, 'check', size=14, ha='left')
    s.text(4.55, ky, 'Lane = one person or system', size=14, ha='left', color=BODY)
    return s


@fig('x_t12_aistep')
def x_t12_aistep(w, h, **_):
    """A spam filter: the path is fixed; one box is a model that judges the meaning; a person glances at the result."""
    s = Scene(w, h)
    y0, bh = h - 1.85, 1.35
    gap = 0.45
    bw = (w - 0.1 - 2 * gap) / 3
    boxes = [('Trigger', 'A new email arrives', PAPER, RED), ('AI step', 'A model reads it: spam or not?', GOLD, INK), ('Fixed rule', 'Spam goes to the spam folder', PAPER, INK)]
    for i, (head, sub, fill, edge) in enumerate(boxes):
        x = 0.05 + i * (bw + gap)
        s.box(x, y0, bw, bh, '', fill=fill, edge=edge, lw=2.2)
        s.text(x + bw / 2, y0 + bh - 0.32, head, size=17, weight='bold', color=RED if edge == RED else INK)
        _w(s, x + bw / 2, y0 + 0.45, bw - 0.2, sub, 15)
        if i < 2:
            s.arrow(x + bw + 0.03, y0 + bh / 2, x + bw + gap - 0.03, y0 + bh / 2, lw=2.2, head=14)
    lines = [('Same path every time:', 'arrive, judge, file.'), ('One judgement by a model:', 'it reads the meaning.'), ('It can be wrong:', 'you glance at the spam folder.')]
    y = y0 - 0.55
    for a, b in lines:
        s.text(0.25, y, a, size=16, weight='bold', ha='left')
        s.text(w - 0.25, y, b, size=16, ha='right', color=BODY)
        y -= 0.62
    return s


@fig('x_t12_agent')
def x_t12_agent(w, h, **_):
    """An agent: a goal, a loop of plan, act, observe that picks its own next step, tools, and an approval step."""
    s = Scene(w, h)
    s.box(0.1, h - 0.85, w - 0.2, 0.7, '', fill=PAPER, edge=RED, lw=2.2)
    s.text(w / 2, h - 0.5, 'Goal: book a dentist visit next week', size=17, weight='bold')
    cx, cy, r = 2.2, (h - 0.9) / 2 + 0.05, 1.25
    pts = [('Plan', cx, cy + r * 0.85), ('Act', cx + r, cy - r * 0.55), ('Observe', cx - r, cy - r * 0.55)]
    for t, x, y in pts:
        s.box(x - 0.62, y - 0.3, 1.24, 0.6, '', fill=GOLD, edge=INK, lw=2, z=3)
        s.text(x, y, t, size=16, weight='bold', z=6)
    s.arrow(cx + 0.55, cy + r * 0.75, cx + r - 0.1, cy - r * 0.25, lw=2.2, head=14, rad=-0.25)
    s.arrow(cx + r - 0.62, cy - r * 0.62, cx - r + 0.62, cy - r * 0.62, lw=2.2, head=14, rad=-0.3)
    s.arrow(cx - r + 0.05, cy - r * 0.25, cx - 0.55, cy + r * 0.75, lw=2.2, head=14, rad=-0.25)
    tx = 4.45
    s.text(tx, cy + 1.25, 'Tools it may use', size=16, weight='bold', ha='left')
    for k, (ic, t) in enumerate([('calendar', 'Read your calendar'), ('magnifier', 'Search free times'), ('mail', 'Draft a booking')]):
        y = cy + 0.75 - k * 0.55
        s.icon(ic, tx + 0.2, y, 0.42)
        s.text(tx + 0.55, y, t, size=15, ha='left')
    s.box(tx - 0.1, 0.1, w - tx, 0.8, '', fill=PAPER, edge=RED, lw=2.2)
    s.text(tx - 0.1 + (w - tx) / 2, 0.5, 'You approve before it books', size=15, weight='bold', color=RED)
    return s


def _bar(s, x, y0, unit, v, bw, fill, label, top_text, size=15):
    s.rect(x, y0, bw, v * unit, fill=fill, edge=INK, lw=2)
    s.text(x + bw / 2, y0 + v * unit + 0.22, top_text, size=size, weight='bold')
    s.text(x + bw / 2, y0 - 0.3, label, size=size, weight='bold')


@fig('x_t12_baseline')
def x_t12_baseline(w, h, **_):
    """Kettle: the baseline today, the running cost after, the gap (net saving a month); the one-off cost in its own box."""
    s = Scene(w, h)
    y0 = 0.75
    unit = (h - 1.6) / 30000
    bw = 1.45
    _bar(s, 0.5, y0, unit, 30000, bw, PAPER, 'Today: charcoal', '30,000')
    _bar(s, 2.6, y0, unit, 10000, bw, GOLD, 'After: electricity', '10,000')
    s.line(0.3, y0, 4.4, y0, lw=2)
    top, low = y0 + 30000 * unit, y0 + 10000 * unit
    s.line(2.6, top, 4.25, top, dash=True, color=MUTE)
    s.arrow(3.95, top - 0.03, 3.95, low + 0.05, color=RED, lw=2.4, head=14)
    s.arrow(3.95, low + 0.05, 3.95, top - 0.03, color=RED, lw=2.4, head=14)
    s.text(4.1, (top + low) / 2, 'saving\n20,000', size=15, weight='bold', color=RED, ha='left')
    s.text(2.4, h - 0.2, 'UGX a month, for tea', size=15, color=MUTE)
    bx = 5.4
    s.box(bx, y0, w - bx - 0.1, 1.9, '', fill=PAPER, edge=INK, lw=2)
    s.icon('receipt', bx + (w - bx - 0.1) / 2, y0 + 1.4, 0.55)
    s.text(bx + (w - bx - 0.1) / 2, y0 + 0.75, 'Kettle, paid once', size=15, weight='bold')
    s.text(bx + (w - bx - 0.1) / 2, y0 + 0.35, '60,000', size=16, weight='bold', color=RED)
    s.text(bx + (w - bx - 0.1) / 2, y0 + 2.3, 'One-off cost', size=15, weight='bold')
    return s


@fig('x_t12_payback')
def x_t12_payback(w, h, **_):
    """Kettle: the saving added up month by month (20,000, 40,000, 60,000, 80,000); the 60,000 cost is reached in month 3."""
    s = Scene(w, h)
    y0 = 0.8
    unit = (h - 1.7) / 80000
    bw, gap, x0 = 1.15, 0.45, 1.0
    vals = [20000, 40000, 60000, 80000]
    for i, v in enumerate(vals):
        x = x0 + i * (bw + gap)
        _bar(s, x, y0, unit, v, bw, GOLD if i == 2 else PAPER, f'Month {i + 1}', f'{v:,}')
    s.line(0.6, y0, w - 0.2, y0, lw=2)
    yl = y0 + 60000 * unit
    s.line(0.6, yl, w - 0.2, yl, color=RED, lw=2.2, dash=True, z=5)
    s.text(0.65, yl + 0.3, 'kettle cost 60,000', size=15, weight='bold', color=RED, ha='left')
    s.text(x0 + 2 * (bw + gap) + bw / 2, yl - 0.35, 'paid back', size=15, weight='bold', z=7)
    s.text(0.1, h - 0.2, 'Savings so far, UGX', size=15, color=MUTE, ha='left')
    return s


@fig('x_t12_roi')
def x_t12_roi(w, h, **_):
    """Kettle, first year: benefits 12 x 30,000 = 360,000; costs 60,000 + 12 x 10,000 = 180,000; the gap is the net benefit."""
    s = Scene(w, h)
    y0 = 0.75
    unit = (h - 1.55) / 360000
    bw = 1.7
    s.rect(0.6, y0, bw, 360000 * unit, fill=PAPER, edge=INK, lw=2)
    s.text(0.6 + bw / 2, y0 + 360000 * unit + 0.22, '360,000', size=15, weight='bold')
    s.text(0.6 + bw / 2, y0 - 0.3, 'Benefits', size=15, weight='bold')
    x2 = 2.9
    s.rect(x2, y0, bw, 60000 * unit, fill=RED, edge=INK, lw=2)
    s.rect(x2, y0 + 60000 * unit, bw, 120000 * unit, fill=GREY, edge=INK, lw=2)
    s.text(x2 + bw / 2, y0 + 30000 * unit, 'kettle 60,000', size=14, weight='bold', color=PAPER)
    s.text(x2 + bw / 2, y0 + 120000 * unit, 'power 120,000', size=14, weight='bold', color=PAPER)
    s.text(x2 + bw / 2, y0 + 180000 * unit + 0.22, '180,000', size=15, weight='bold')
    s.text(x2 + bw / 2, y0 - 0.3, 'Costs', size=15, weight='bold')
    s.line(0.4, y0, x2 + bw + 0.2, y0, lw=2)
    top, low = y0 + 360000 * unit, y0 + 180000 * unit
    s.line(x2, top, x2 + bw + 0.6, top, dash=True, color=MUTE)
    ax = x2 + bw + 0.35
    s.arrow(ax, top - 0.03, ax, low + 0.03, color=GOLD, lw=3, head=14)
    s.arrow(ax, low + 0.03, ax, top - 0.03, color=GOLD, lw=3, head=14)
    s.text(ax + 0.15, (top + low) / 2, 'net\n180,000', size=15, weight='bold', ha='left')
    s.text(w / 2, h - 0.2, 'UGX, first year', size=15, color=MUTE)
    return s


@fig('x_t12_benefits')
def x_t12_benefits(w, h, **_):
    """NVF: the two benefits a month, each worked in UGX from the workbook inputs (invented plan values)."""
    s = Scene(w, h)
    rows = [['Benefit a month', 'Worked out', 'UGX'],
            ['Time saved', '5.33 hours × 30,000 an hour', '160,000'],
            ['Errors avoided', '4 runs × 0.4 × 0.6 × 150,000', '144,000'],
            ['Total benefit', '160,000 + 144,000', '304,000']]
    cw = [(w - 0.1) * 0.27, (w - 0.1) * 0.52, (w - 0.1) * 0.21]
    s.table(0.05, h - 0.05, cw, 0.62, rows, size=15, align=['left', 'left', 'right'], hl_cells={(3, 2): GOLD})
    y = h - 0.05 - 4 * 0.62 - 0.4
    notes = ['30,000 an hour: what one staff hour costs NVF', '0.4: 4 runs in 10 have an error today', '0.6: the new routine removes 6 errors in 10', '150,000: the cost of fixing one error']
    for t in notes:
        s.text(0.15, y, t, size=15, color=BODY, ha='left')
        y -= 0.42
    return s


@fig('x_t12_costs')
def x_t12_costs(w, h, **_):
    """NVF: one-off and monthly costs from the Costs sheet of the workbook (invented plan values)."""
    s = Scene(w, h)
    rows = [['Cost', 'Worked out', 'One-off', 'Monthly'],
            ['Set-up and data', '12 hours × 30,000', '360,000', ''],
            ['Training', '4 hours × 30,000', '120,000', ''],
            ['Tool licence', 'vendor price', '', '60,000'],
            ['Review', '4 × 20 min ÷ 60 × 30,000', '', '40,000'],
            ['Upkeep', '1.5 hours × 30,000', '', '45,000'],
            ['Total', '', '480,000', '145,000']]
    cw = [(w - 0.1) * 0.22, (w - 0.1) * 0.46, (w - 0.1) * 0.16, (w - 0.1) * 0.16]
    s.table(0.05, h - 0.05, cw, (h - 0.15) / len(rows), rows, size=15, align=['left', 'left', 'right', 'right'],
            hl_cells={(6, 2): GOLD, (6, 3): GOLD})
    return s
