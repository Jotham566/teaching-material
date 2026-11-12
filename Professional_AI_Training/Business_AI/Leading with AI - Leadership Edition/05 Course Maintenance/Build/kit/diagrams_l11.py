"""Figures for Leadership Edition Session 11, Redesigning work: workflows, value and the business case (practical).  Names: x_l11_*  (content kind 'l11_*').

No maths: pictures, counts, percentages and shillings only, worked in words and tables.  The business case numbers are the grey Nile Valley Foods
(fictional) example of Templates/Business Case Workbook.xlsx, recomputed by demo_runs/s12/business_case_check.py and teaching_numbers_check.py
(outputs in demo_runs/s12/*.txt): 5.33 hours saved a month, benefit UGX 304,000, monthly cost UGX 145,000, net UGX 159,000, one-off UGX 480,000,
payback 3.0 months, 12-month net UGX 1,428,000, first-year costs UGX 2,220,000, first-year return 64%, UGX 333,600 after a 30% haircut.
These are PLAN figures with invented inputs.  Case figures come from research/*.md (IDs in content/s11.py).
"""
from figkit import Scene, INK, BODY, MUTE, HAIR, PALE, PAPER, RED, GOLD, fig
import slidekit as K
from diagrams_l02 import _wrap, _source
from diagrams_l10 import six


# ------------------------------------------------------------------ recall bridge: one agent, then a whole workflow
@fig('x_l11_bridge')
def x_l11_bridge(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.3, 'Session 10: one agent, its keys and its level of freedom', size=16, weight='bold', ha='left')
    s.box(0.1, h - 1.6, 3.2, 1.05, '', fill=PAPER, lw=1.8, r=0.08)
    s.icon('robot', 0.55, h - 1.07, 0.6)
    s.icon('lock', 1.35, h - 1.07, 0.5)
    _wrap(s, 2.3, h - 1.07, 1.75, 'Level 2: it drafts, a person sends', 14)
    s.line(0.1, h - 1.95, w - 0.1, h - 1.95, color=HAIR, lw=1.2)
    s.text(0.1, h - 2.3, 'Today: a whole workflow, step by step, with its value', size=16, weight='bold', ha='left')
    steps = [('Message arrives', 'Trigger', PAPER), ('Read and sort', 'AI step', GOLD), ('Draft a reply', 'AI step', GOLD), ('Confirm payment', 'Rule', PAPER), ('Check and send', 'Person', PAPER)]
    bw, gap = 1.22, 0.25
    y = h - 3.5
    for i, (t, tag, fill) in enumerate(steps):
        x = 0.1 + i * (bw + gap)
        s.box(x, y, bw, 0.85, '', fill=fill, edge=INK, lw=1.8, r=0.06)
        _wrap(s, x + bw / 2, y + 0.55, bw - 0.12, t, 14, weight='bold')
        s.text(x + bw / 2, y + 0.18, tag, size=14, color=BODY)
        if i < len(steps) - 1:
            s.arrow(x + bw + 0.02, y + 0.42, x + bw + gap - 0.02, y + 0.42, lw=2, head=12)
    return s


# ------------------------------------------------------------------ hook: pilots without profit
@fig('x_l11_pilots')
def x_l11_pilots(w, h, **_):
    s = Scene(w, h)
    panels = [('95%', 'of company generative AI pilots showed little or no measurable profit', 'MIT NANDA, 2025', 'Small, mostly US sample: a provocation'),
              ('82% piloted', 'of African organisations have run AI pilots; 23% of African CEOs who invested saw revenue rise', 'PwC, reported by ITWeb, 2026', 'Only 85 African firms in the sample'),
              ('30%+', 'of generative AI projects to be abandoned after the first trial, by the end of 2025', 'Gartner forecast, July 2024', 'Reasons: poor data, weak controls, rising cost, unclear value')]
    gap = 0.25
    cw = (w - 0.2 - 2 * gap) / 3
    for i, (big, txt, src, cav) in enumerate(panels):
        x = 0.1 + i * (cw + gap)
        if i:
            s.line(x - gap / 2, 0.75, x - gap / 2, h - 0.1, color=HAIR, lw=1.2)
        s.text(x + 0.1, h - 0.55, big, size=34 if len(big) < 5 else 28, weight='bold', color=RED if i == 0 else INK, ha='left')
        _wrap(s, x + 0.1, h - 1.1, cw - 0.3, txt, 17, ha='left', va='top')
        s.text(x + 0.1, 1.55, src, size=14, weight='bold', ha='left')
        _wrap(s, x + 0.1, 1.1, cw - 0.3, cav, 14, ha='left', color=MUTE)
    s.text(0.1, 0.35, 'MIT NANDA found the best returns in back-office work.', size=15, weight='bold', ha='left')
    return s


# ------------------------------------------------------------------ four choices for each step
@fig('x_l11_four')
def x_l11_four(w, h, **_):
    s = Scene(w, h)
    cols = [('calculator', 'A rule', 'The answer is fixed by clear words or numbers', 'A bank standing order', 'A payment reference goes to Finance'),
            ('chart', 'An AI step', 'It needs the meaning of text, and a person can check quickly', 'A spam filter', 'Sort a polite complaint'),
            ('robot', 'An agent', 'It needs several tools and chooses its own next step', 'A house-sitter (Session 10)', 'Draft reminders for overdue invoices'),
            ('person', 'A person', 'Money, trust or the law turns on it', 'You sign the cheque', 'Approve a credit; send the reply')]
    gap = 0.15
    cw = (w - 0.2 - 3 * gap) / 4
    lab_y = [h - 1.95, h - 2.75, h - 3.65]
    for i, (ic, head, when, life, work) in enumerate(cols):
        x = 0.1 + i * (cw + gap)
        s.box(x, 0.1, cw, h - 0.2, '', fill=GOLD if i == 1 else PAPER, edge=INK, lw=2.0, r=0.08)
        s.icon(ic, x + 0.38, h - 0.5, 0.5)
        s.text(x + 0.72, h - 0.5, head, size=17, weight='bold', ha='left')
        _wrap(s, x + 0.15, h - 0.95, cw - 0.3, when, 16, ha='left', va='top')
        s.text(x + 0.15, lab_y[1] + 0.35, 'Everyday', size=14, weight='bold', color=MUTE, ha='left')
        _wrap(s, x + 0.15, lab_y[1], cw - 0.3, life, 15, ha='left', color=BODY)
        s.text(x + 0.15, lab_y[2] + 0.35, 'At work', size=14, weight='bold', color=MUTE, ha='left')
        _wrap(s, x + 0.15, lab_y[2], cw - 0.3, work, 15, ha='left', color=BODY)
    return s


# ------------------------------------------------------------------ three kinds of value, with cases
@fig('x_l11_value')
def x_l11_value(w, h, **_):
    s = Scene(w, h)
    tiles = [('clock', 'Time saved', 'One Acre Fund, Burundi', 'Checking farm forms: from over 1,000 staff-days a cycle to an estimated 300 to 500', 'Dataiku customer story, 2026; vendor estimate'),
             ('check', 'Errors avoided', 'Unilever, Gandhidham, India', 'Quality defects down 30% over four years, with a digital twin of the line', 'Intelligent CIO, 2026; company figures'),
             ('chart', 'Revenue', 'Georgia State University, USA', 'A chatbot for admitted students: enrolment 3.9% higher in a randomised trial', 'Campus Technology, 2017; trial in 2016')]
    gap = 0.2
    cw = (w - 0.2 - 2 * gap) / 3
    for i, (ic, head, org, txt, src) in enumerate(tiles):
        x = 0.1 + i * (cw + gap)
        s.box(x, 0.85, cw, h - 0.95, '', fill=PAPER, lw=2.0, r=0.08)
        s.icon(ic, x + 0.45, h - 0.5, 0.55)
        s.text(x + 0.85, h - 0.5, head, size=19, weight='bold', ha='left')
        s.text(x + 0.2, h - 1.1, org, size=15, weight='bold', ha='left')
        _wrap(s, x + 0.2, h - 1.4, cw - 0.4, txt, 15, ha='left', va='top', color=BODY)
        _wrap(s, x + 0.2, 1.2, cw - 0.4, src, 14, ha='left', color=MUTE)
    s.text(0.1, 0.39, 'Shell predicts failures on over 10,000 machines, and has published no saving in money.', size=15, weight='bold', ha='left')
    return s


@fig('x_l11_six')
def x_l11_six(w, h, **_):
    tiles = [('calculator', 'Banking and microfinance', 'Contact-centre agents see client details from an AI tool as they talk', 'Capitec, South Africa'),
             ('phone', 'Telecom and mobile money', 'AI flags odd M-Pesa patterns; the compliance team acts on them', 'Safaricom, Kenya'),
             ('plant', 'Agriculture and agribusiness', 'Software checks paper forms; staff review only the flagged ones', 'One Acre Fund, Burundi'),
             ('gear', 'Manufacturing and FMCG', 'A live copy of each line predicts problems before they happen', 'Unilever with Accenture'),
             ('clinic', 'Healthcare and insurance', 'AI sorts mothers’ messages; the help desk answers urgent ones first', 'Jacaranda Health, Kenya'),
             ('people', 'Public sector', 'AI cross-checks tax records to find revenue leaks', 'Uganda Revenue Authority')]
    return six(w, h, tiles, 'Sources: TechCentral 2026; iGamingToday 2025; Dataiku 2026; Intelligent CIO 2026; Penn State 2023; URA 2025.')


# ------------------------------------------------------------------ Coca-Cola suggested orders as a redesigned workflow (MFG-03)
@fig('x_l11_coke')
def x_l11_coke(w, h, **_):
    s = Scene(w, h)
    rows = [('Before', [('Shopkeeper guesses what to order', PAPER, 'Person'), ('Rep visits and writes the order', PAPER, 'Person')]),
            ('With the AI step', [('App suggests products and amounts', GOLD, 'AI step'), ('Shopkeeper decides', PAPER, 'Person'), ('Rep still visits', PAPER, 'Person')])]
    bw, gap = 1.85, 0.3
    for r, (lab, steps) in enumerate(rows):
        y = h - 0.95 - r * 1.45
        s.text(0.1, y + 0.72, lab, size=16, weight='bold', ha='left')
        for i, (t, fill, tag) in enumerate(steps):
            x = 0.1 + i * (bw + gap)
            s.box(x, y - 0.45, bw, 0.95, '', fill=fill, lw=1.8, r=0.06)
            _wrap(s, x + bw / 2, y + 0.1, bw - 0.15, t, 14, weight='bold')
            s.text(x + bw / 2, y - 0.3, tag, size=14, color=BODY)
            if i < len(steps) - 1:
                s.arrow(x + bw + 0.03, y, x + bw + gap - 0.03, y, lw=2, head=12)
    for i, (big, txt) in enumerate((('83% adopted', 'of shops in the Malaysia campaign, January to April 2026'),
                                    ('3 million+', 'outlets in Latin America got suggestions, early 2024'))):
        x = 0.1 + i * 3.8
        s.text(x + 0.05, 1.33, big, size=24, weight='bold', ha='left')
        _wrap(s, x + 0.05, 0.85, 3.4, txt, 14, ha='left', color=BODY)
    _source(s, 'Source: AI News, 8 September 2026. Company figures.', y=0.2)
    return s


# ------------------------------------------------------------------ worked example: hours on the Monday sales email (plan)
@fig('x_l11_hours')
def x_l11_hours(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.3, 'The Monday sales email, four times a month', size=16, weight='bold', ha='left')
    x0, unit = 1.9, (w - 2.2) / 360.0
    bars = [('Today', [(360, PAPER, '90 minutes each time: 6 hours')]),
            ('New routine', [(40, GOLD, ''), (80, PALE, '')])]
    for r, (lab, segs) in enumerate(bars):
        y = h - 1.3 - r * 1.15
        s.text(0.1, y, lab, size=16, weight='bold', ha='left')
        x = x0
        for m, fill, t in segs:
            s.rect(x, y - 0.3, m * unit, 0.6, fill=fill, edge=INK, lw=1.6)
            if t:
                s.text(x + m * unit / 2, y, t, size=15, weight='bold')
            x += m * unit
        if r == 1:
            s.text(x + 0.15, y, '2 hours', size=15, weight='bold', ha='left')
    y = h - 2.45
    s.text(x0, y - 0.6, 'Gold: your own work, 10 minutes each time', size=14, ha='left', color=BODY)
    s.text(x0, y - 0.95, 'Grey: a person reviews it, 20 minutes each time', size=14, ha='left', color=BODY)
    s.text(0.1, 0.78, 'About 4 hours a month freed, after review', size=18, weight='bold', ha='left')
    s.text(w - 0.1, 0.15, 'Plan figures, Nile Valley Foods (fictional)', size=14, color=MUTE, ha='right')
    return s


# ------------------------------------------------------------------ worked example: a month in shillings (plan)
@fig('x_l11_month')
def x_l11_month(w, h, **_):
    s = Scene(w, h)
    cw = (w - 0.3) / 2
    sides = [('Benefits a month', GOLD, [('Time saved', '5 hours 20 minutes at UGX 30,000 an hour', '160,000'),
                                         ('Errors avoided', 'nearly one a month, UGX 150,000 each', '144,000')], '304,000'),
             ('Costs a month', PAPER, [('Tool licence', 'the vendor’s quote', '60,000'), ('Review', '1 hour 20 minutes of checking', '40,000'),
                                      ('Upkeep', '1 hour 30 minutes of fixing', '45,000')], '145,000')]
    for i, (head, fill, items, tot) in enumerate(sides):
        x = 0.1 + i * (cw + 0.1)
        s.text(x + 0.1, h - 0.3, head, size=17, weight='bold', ha='left')
        s.line(x, h - 0.55, x + cw, h - 0.55, lw=1.8)
        for k, (a, b, v) in enumerate(items):
            y = h - 0.95 - k * 0.68
            s.text(x + 0.1, y + 0.12, a, size=15, weight='bold', ha='left')
            _wrap(s, x + 0.1, y - 0.2, cw - 1.4, b, 14, ha='left', color=BODY)
            s.text(x + cw - 0.1, y, v, size=16, weight='bold', ha='right')
        s.box(x, 0.98, cw, 0.55, '', fill=fill, lw=1.8, r=0.06)
        s.text(x + 0.15, 1.255, 'Total, UGX', size=15, weight='bold', ha='left')
        s.text(x + cw - 0.15, 1.255, tot, size=17, weight='bold', ha='right')
    s.text(0.1, 0.55, 'Net gain a month: UGX 304,000 less UGX 145,000, which is UGX 159,000', size=18, weight='bold', ha='left')
    s.text(w - 0.1, 0.12, 'Plan figures, Nile Valley Foods (fictional)', size=14, color=MUTE, ha='right')
    return s


# ------------------------------------------------------------------ worked example: payback month by month (plan)
@fig('x_l11_payback')
def x_l11_payback(w, h, **_):
    s = Scene(w, h)
    vals = [159000, 318000, 477000, 636000, 795000]
    base, top = 0.75, h - 0.55
    unit = (top - base) / 800000.0
    x0, bw, gap = 1.0, 1.0, 0.35
    s.line(x0 - 0.2, base, w - 0.1, base, lw=1.8)
    for i, v in enumerate(vals):
        x = x0 + i * (bw + gap)
        over = v >= 480000
        s.rect(x, base, bw, v * unit, fill=GOLD if over else PAPER, edge=INK, lw=1.6)
        s.text(x + bw / 2, base + v * unit + 0.2, f'{v:,}', size=14, weight='bold')
        s.text(x + bw / 2, base - 0.25, f'Month {i + 1}', size=14)
    ly = base + 480000 * unit
    s.line(x0 - 0.2, ly, w - 0.1, ly, color=INK, lw=2.0, dash=True, z=5)
    s.text(0.1, ly + 0.5, 'One-off cost', size=14, weight='bold', ha='left')
    s.text(0.1, ly + 0.22, 'UGX 480,000', size=14, weight='bold', ha='left')
    s.text(0.1, h - 0.2, 'Savings added up, UGX', size=14, color=MUTE, ha='left')
    s.text(w - 0.1, 0.15, 'Plan figures, Nile Valley Foods (fictional)', size=14, color=MUTE, ha='right')
    return s


# ------------------------------------------------------------------ worked example: the first year (plan)
@fig('x_l11_year')
def x_l11_year(w, h, **_):
    s = Scene(w, h)
    cards = [('Twelve months of net gain', 'UGX 1,908,000', PAPER, INK),
             ('Less the one-off cost', 'UGX 480,000', PAPER, INK),
             ('First-year gain', 'UGX 1,428,000', GOLD, INK)]
    gap = 0.35
    cw = (w - 0.2 - 2 * gap) / 3
    for i, (a, b, fill, col) in enumerate(cards):
        x = 0.1 + i * (cw + gap)
        s.box(x, h - 1.5, cw, 1.35, '', fill=fill, lw=2.0, r=0.08)
        s.text(x + cw / 2, h - 0.5, a, size=15, weight='bold', color=BODY)
        s.text(x + cw / 2, h - 1.05, b, size=20, weight='bold', color=col)
        if i < 2:
            s.arrow(x + cw + 0.04, h - 0.82, x + cw + gap - 0.04, h - 0.82, lw=2.2, head=14)
    rows = [('Return', 'UGX 2,220,000 spent in the first year brings back that sum plus UGX 1,428,000: about 64 shillings on top of every 100 spent, a first-year return of 64%.'),
            ('If hopes run high', 'Count only 70% of the benefits, as careful estimators do, and the first-year gain is still UGX 333,600.')]
    for k, (a, b) in enumerate(rows):
        y = h - 2.15 - k * 0.95
        s.text(0.15, y, a, size=16, weight='bold', ha='left')
        _wrap(s, 2.35, y, w - 2.55, b, 15, ha='left', color=BODY)
    s.text(w - 0.1, 0.15, 'Plan figures from the Business Case Workbook example, Nile Valley Foods (fictional)', size=14, color=MUTE, ha='right')
    return s


# ------------------------------------------------------------------ scoring the portfolio: value and feasibility (illustrative)
PORT = [('A', 'Sort customer messages', 4, 5), ('B', 'Rank shops by risk of ordering less', 4, 4), ('C', 'Draft overdue-invoice reminders', 3, 4),
        ('D', 'Forecast demand for each shop', 5, 2), ('E', 'An agent that pays suppliers', 3, 1)]


@fig('x_l11_grid')
def x_l11_grid(w, h, **_):
    s = Scene(w, h)
    gx, gy, gs = 0.75, 0.75, (h - 1.0) / 5
    for k in range(6):
        s.line(gx, gy + k * gs, gx + 5 * gs, gy + k * gs, color=HAIR, lw=1)
        s.line(gx + k * gs, gy, gx + k * gs, gy + 5 * gs, color=HAIR, lw=1)
    s.rect(gx + 2.5 * gs, gy + 2.5 * gs, 2.5 * gs, 2.5 * gs, fill=PALE, edge=PALE, lw=0, z=0)
    s.text(gx + 4.0 * gs, gy + 4.6 * gs, 'Start here', size=14, weight='bold')
    s.text(gx + 1.25 * gs, gy + 0.3 * gs, 'Later, or drop', size=14, color=MUTE)
    for k in range(1, 6):
        s.text(gx + (k - 0.5) * gs, gy - 0.2, str(k), size=14, color=MUTE)
        s.text(gx - 0.2, gy + (k - 0.5) * gs, str(k), size=14, color=MUTE)
    s.text(gx + 2.5 * gs, 0.15, 'Feasibility', size=14, weight='bold')
    s.text(0.2, gy + 2.5 * gs, 'Value', size=14, weight='bold', rot=90)
    for lab, name, v, f in PORT:
        cx, cy = gx + (f - 0.5) * gs, gy + (v - 0.5) * gs
        s.circle(cx, cy, 0.24, fill=GOLD if v + f >= 8 else PAPER, edge=INK, lw=1.8, z=4)
        s.text(cx, cy, lab, size=15, weight='bold', z=7)
    x = gx + 5 * gs + 0.35
    s.text(x, h - 0.25, 'Priority: value plus feasibility', size=15, weight='bold', ha='left')
    for i, (lab, name, v, f) in enumerate(sorted(PORT, key=lambda r: -(r[2] + r[3]))):
        y = h - 0.75 - i * 0.62
        s.text(x, y, lab, size=15, weight='bold', ha='left')
        _wrap(s, x + 0.35, y, w - x - 1.0, name, 14, ha='left', color=BODY)
        s.text(w - 0.15, y, str(v + f), size=16, weight='bold', ha='right')
    s.text(x, 0.55, 'Feasibility: the data exists, it is easy to check, a team can start.', size=14, color=BODY, ha='left')
    s.text(x, 0.15, 'Illustrative, Nile Valley Foods (fictional)', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ your people in the redesigned workflows
@fig('x_l11_people')
def x_l11_people(w, h, **_):
    from diagrams_l10 import x_l10_people
    roles = [('Customer service', ['Reading and sorting every message', 'Resolving complaints, calling customers', 'Checking what the AI sorted', 'Fear: watched or replaced. Gain: fewer piles']),
             ('Finance officer', ['Hunting for payment messages', 'Confirming payments the same day', 'Reading a flagged case quickly', 'Fear: errors blamed on them. Gain: clear queue']),
             ('Sales manager', ['90 minutes building the Monday email', '20 minutes reviewing; time with reps', 'Judging a draft against the figures', 'Fear: losing control. Gain: about 4 hours a month'])]
    return x_l10_people(w, h, roles=roles)
