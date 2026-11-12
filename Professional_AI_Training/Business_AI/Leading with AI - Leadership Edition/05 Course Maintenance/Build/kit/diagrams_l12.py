"""Figures for Leadership Edition Session 12, Leading people through AI.  Names: x_l12_*  (content kind 'l12_*').

No maths: pictures, counts and percentages only.  Case figures come from research/*.md (IDs in content/s12.py), each with a source line.
The Nile Valley Foods examples (the customer service officer, the briefing, the plan) are FICTIONAL and follow the grey example rows of
Templates/People and Skills Plan.docx.  The Session 11 recorded result (AI 9 of 12 exact, one wrong with confidence) is from
demo_runs/s12_rule_vs_ai.md (Claude, three fresh sessions, 4 November 2026).
"""
import numpy as np

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD, fig
import slidekit as K
from diagrams_l02 import _wrap, _fit, _source, _lh


def _bar(s, x, y, w, value, h=0.26, fill=GOLD):
    """A bar of 100 with `value` filled."""
    s.rect(x, y - h / 2, w, h, fill=PAPER, edge=INK, lw=1.1)
    s.rect(x, y - h / 2, w * value / 100.0, h, fill=fill, edge=INK, lw=1.1, z=3)


# ------------------------------------------------------------------ recall bridge: Session 11's workflow lands on people
@fig('x_l12_bridge')
def x_l12_bridge(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.25, 'Session 11: the customer-message workflow (Nile Valley Foods, fictional)', size=15, weight='bold', ha='left')
    steps = [('Message arrives', 'trigger', PAPER), ('Sort it', 'AI step', GOLD), ('Draft a reply', 'AI step', GOLD), ('Check and send', 'person', PAPER)]
    people = [('Customer', 'answered sooner'), ('Officer', 'checks only the doubtful ones'), ('Officer', 'edits a draft, no blank page'), ('Officer', 'owns every reply sent')]
    bw, gap = 1.72, 0.24
    x0 = (w - (4 * bw + 3 * gap)) / 2
    y = h - 1.55
    for i, ((st, tag, fill), (who, chg)) in enumerate(zip(steps, people)):
        x = x0 + i * (bw + gap)
        s.text(x + bw / 2, y + 0.98, tag, size=14, color=RED if tag == 'AI step' else MUTE, weight='bold')
        s.box(x, y, bw, 0.75, '', fill=fill, lw=1.8, r=0.08)
        _wrap(s, x + bw / 2, y + 0.375, bw - 0.2, st, 15, weight='bold')
        if i < 3:
            s.arrow(x + bw + 0.03, y + 0.375, x + bw + gap - 0.03, y + 0.375, lw=2.0, head=13)
        s.arrow(x + bw / 2, y - 0.08, x + bw / 2, y - 0.55, color=RED, lw=2.0, head=13)
        s.icon('person', x + bw / 2, y - 0.98, 0.62, accent=GOLD if who == 'Officer' else PAPER)
        s.text(x + bw / 2, y - 1.48, who, size=15, weight='bold')
        _wrap(s, x + bw / 2, y - 1.72, bw - 0.05, chg, 14, color=BODY, va='top')
    s.text(w / 2, 0.25, 'Every step that changes lands on someone’s working day', size=16, weight='bold', color=RED)
    return s


# ------------------------------------------------------------------ hook: Commonwealth Bank of Australia (BNK-09)
@fig('x_l12_cba')
def x_l12_cba(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.28, 'As in Session 9: Commonwealth Bank of Australia', size=17, weight='bold', ha='left')
    events = [('July 2025', 'The bank brought in a voice bot for simple inbound calls and declared 45 customer-service roles redundant.', PAPER),
              ('The union’s case', 'The Finance Sector Union showed call volumes were rising, with overtime offered and team leaders answering calls.', PAPER),
              ('August 2025', '45 jobs restored. The bank said its assessment had not considered all the relevant business factors, and apologised.', GOLD)]
    lx = 0.45
    top = h - 0.6
    bh = 0.92
    gap = 0.16
    s.line(lx, top - 0.2, lx, top - 3 * bh - 2 * gap + 0.2, lw=2.4, z=1)
    for i, (when, txt, fill) in enumerate(events):
        y = top - (i + 1) * bh - i * gap
        s.circle(lx, y + bh / 2, 0.13, fill=RED if i == 2 else INK, edge=INK, z=3)
        s.box(lx + 0.35, y, w - lx - 0.45, bh, '', fill=fill, lw=1.8, r=0.08)
        s.text(lx + 0.55, y + bh - 0.25, when, size=16, weight='bold', ha='left', color=RED if i == 2 else INK)
        _wrap(s, lx + 0.55, y + bh - 0.45, w - lx - 0.85, txt, 15, ha='left', va='top', color=BODY)
    _wrap(s, 0.1, 0.58, w - 0.2, 'Staff could keep their role, move, or take redundancy. No measured result for the bot was published.', 14, ha='left', weight='bold')
    _source(s, 'Sources: The Register, 22 Aug 2025; Information Age (ACS), 21 Aug 2025.', y=0.2)
    return s


# ------------------------------------------------------------------ a job is a bundle of tasks
@fig('x_l12_bundle')
def x_l12_bundle(w, h, **_):
    s = Scene(w, h)
    cards = [('Read and sort messages', 'AI sorts first', GOLD, INK), ('Draft replies', 'AI drafts first', GOLD, INK), ('Look up orders and payments', 'same as today', PAPER, INK),
             ('Handle angry or unusual customers', 'more time', PAPER, INK), ('Call customers back', 'more time', PAPER, INK), ('Report AI mistakes', 'a new task', PAPER, RED)]
    cw, ch = 2.55, 0.98
    ys = [h - 0.1 - ch - k * (ch + 0.22) for k in range(3)]
    cx, cy = w / 2, ys[1] + ch / 2 + 0.25
    for i, (txt, tag, fill, edge) in enumerate(cards):
        left = i < 3
        x = 0.1 if left else w - 0.1 - cw
        y = ys[i % 3]
        s.line(x + cw if left else x, y + ch / 2, cx - 0.55 if left else cx + 0.55, cy, color=HAIR, lw=1.6, z=0)
        s.box(x, y, cw, ch, '', fill=fill, edge=edge, lw=2.2 if edge == RED else 1.8, r=0.08)
        _wrap(s, x + 0.15, y + ch - 0.12, cw - 0.3, txt, 15, weight='bold', ha='left', va='top')
        s.text(x + 0.15, y + 0.2, tag, size=14, ha='left', color=RED if tag != 'same as today' else MUTE, weight='bold')
    s.icon('person', cx, cy, 1.1, accent=GOLD)
    s.text(cx, cy - 0.85, 'Customer service', size=15, weight='bold')
    s.text(cx, cy - 1.1, 'officer', size=15, weight='bold')
    s.text(w / 2, 0.22, 'The job stays. The mix of tasks changes.', size=16, weight='bold', color=RED)
    return s


# ------------------------------------------------------------------ augment, automate, create
@fig('x_l12_three')
def x_l12_three(w, h, **_):
    s = Scene(w, h)
    cols = [('Augment', 'AI helps; the person decides', 'The AI drafts a reply. The officer edits it and sends it.', ('person', 'robot')),
            ('Automate', 'AI does it; a person checks a sample', 'The AI sorts routine messages. A person checks the doubtful ones.', ('robot',)),
            ('Create', 'A new task appears', 'Checking AI output, keeping the error log, being a champion.', ('person', 'flag'))]
    cw = (w - 0.2) / 3
    for i, (hd, sub, ex, ics) in enumerate(cols):
        x = 0.1 + i * cw
        cx = x + cw / 2
        if i:
            s.line(x, 0.2, x, h - 0.15, color=HAIR, lw=1.2)
        s.text(cx, h - 0.35, hd, size=21, weight='bold', color=RED if i == 2 else INK)
        n = len(ics)
        for k, ic in enumerate(ics):
            s.icon(ic, cx + (k - (n - 1) / 2) * 0.85, h - 1.25, 0.75, accent=GOLD)
        _wrap(s, cx, h - 2.05, cw - 0.3, sub, 16, weight='bold')
        s.box(x + 0.12, 0.35, cw - 0.24, 1.55, '', fill=GOLD if i == 0 else PAPER, lw=1.6, r=0.08)
        s.text(x + 0.28, 1.68, 'Example', size=14, color=MUTE, ha='left')
        _wrap(s, x + 0.28, 1.45, cw - 0.55, ex, 15, ha='left', va='top', color=INK)
    return s


# ------------------------------------------------------------------ exposure: IMF and ILO (PPL-09, PPL-10)
@fig('x_l12_exposure')
def x_l12_exposure(w, h, **_):
    s = Scene(w, h)
    groups = [('IMF, 2024: jobs exposed to AI', [('The world', 40), ('Advanced economies', 60), ('Emerging markets', 40), ('Low-income countries', 26)]),
              ('ILO, 2025: some exposure to generative AI', [('The world, about 1 in 4', 25), ('Low-income countries', 11), ('High-income countries', 34)])]
    lw_, bx, bw = 2.65, 2.8, 3.75
    y = h - 0.3
    for gi, (head, rows) in enumerate(groups):
        s.text(0.1, y, head, size=15, weight='bold', ha='left', color=RED if gi else INK)
        y -= 0.4
        for lab, v in rows:
            s.text(0.15, y, lab, size=14, ha='left', color=BODY)
            _bar(s, bx, y, bw, v, fill=GOLD if gi == 0 else PALE)
            s.text(w - 0.1, y, f'{v} in 100', size=14, weight='bold', ha='right')
            y -= 0.38
        y -= 0.1
    _wrap(s, w / 2, 0.75, w - 0.3, 'Exposed means a job’s tasks are affected. In rich economies the IMF expects about half of exposed jobs to gain, and half to see less demand.', 14, weight='bold')
    _source(s, 'Sources: IMF Blog, 14 Jan 2024; ILO Working Paper 140, 20 May 2025.', y=0.2)
    return s


# ------------------------------------------------------------------ WEF Future of Jobs 2025 (PPL-08)
@fig('x_l12_wef')
def x_l12_wef(w, h, **_):
    s = Scene(w, h)
    tiles = [('170 million', 'jobs created', GOLD), ('92 million', 'jobs displaced', PAPER), ('78 million', 'more jobs, net', PAPER)]
    tw = (w - 0.2 - 0.3) / 3
    for i, (big, txt, fill) in enumerate(tiles):
        x = 0.1 + i * (tw + 0.15)
        s.box(x, h - 1.2, tw, 1.1, '', fill=fill, lw=1.8, r=0.08)
        s.text(x + tw / 2, h - 0.5, big, size=22, weight='bold', color=RED if i == 1 else INK)
        s.text(x + tw / 2, h - 0.92, txt, size=15, color=BODY)
    rows = [('Workers whose skills will change or go out of date', 39), ('Employers who plan to put upskilling first', 85), ('Employers who expect fewer staff where automation can do the tasks', 40)]
    y = h - 1.65
    for lab, v in rows:
        _wrap(s, 0.1, y, 3.75, lab, 14, ha='left', color=BODY)
        _bar(s, 4.0, y, 2.6, v)
        s.text(w - 0.1, y, f'{v} in 100', size=14, weight='bold', ha='right')
        y -= 0.62
    s.box(0.1, 0.45, w - 0.2, 0.62, '', fill=PAPER, edge=RED, lw=2, r=0.08)
    _wrap(s, w / 2, 0.76, w - 0.5, 'Employers’ expectations to 2030, for every cause of change, AI among them. Over 1,000 employers in 55 economies.', 14, weight='bold')
    _source(s, 'Source: WEF Future of Jobs 2025, via People Matters, 24 Feb 2026.', y=0.18)
    return s


# ------------------------------------------------------------------ six industries: whose work changes first
@fig('x_l12_six')
def x_l12_six(w, h, **_):
    s = Scene(w, h)
    tiles = [('calculator', 'Banking and microfinance', 'Every role trained to work with AI', 'Equity Group, Kenya: over 7,300 staff trained'),
             ('phone', 'Telecom and mobile money', 'Customer service, by plan over years', 'BT, UK: about 10,000 roles to AI by 2030'),
             ('plant', 'Agriculture and agribusiness', 'Review staff check only flagged forms', 'One Acre Fund, Burundi: about 120 reviewers'),
             ('bottle', 'Manufacturing and FMCG', 'Newer staff reach the work of experienced ones', 'Procter & Gamble product teams, about 780 staff'),
             ('clinic', 'Healthcare and insurance', 'Help-desk agents answer urgent messages first', 'Jacaranda Health, Kenya: workload down about 12%'),
             ('people', 'Public sector', 'Officers augmented; hiring in data, legal and audit', 'South African Revenue Service')]
    gap = 0.12
    tw = (w - 0.2 - 2 * gap) / 3
    th = (h - 0.5 - gap) / 2
    for i, (ic, ind, use, ex) in enumerate(tiles):
        x = 0.1 + (i % 3) * (tw + gap)
        y = 0.45 + (1 - i // 3) * (th + gap)
        s.box(x, y, tw, th, '', fill=PAPER, lw=1.8, r=0.08)
        s.icon(ic, x + 0.5, y + th - 0.55, 0.75)
        tx = x + 1.0
        iw = tw - 1.15
        top = y + th - 0.15
        hh = _wrap(s, tx, top, iw, ind, 16, weight='bold', ha='left', va='top')
        top -= hh + 0.1
        uh = _wrap(s, tx, top, iw, use, 15, ha='left', va='top', color=BODY)
        top -= uh + 0.08
        _wrap(s, tx, top, iw, ex, 15, weight='bold', ha='left', va='top', color=RED)
    _source(s, 'Sources: TechTrends Kenya 2026; The Guardian 2023; Dataiku 2026; HBS 2025; Penn State 2023; The Citizen 2025.', y=0.16)
    return s


# ------------------------------------------------------------------ announced cuts are plans: DBS and BT (BNK-11, TEL-11)
@fig('x_l12_routes')
def x_l12_routes(w, h, **_):
    s = Scene(w, h)
    pw = (w - 0.3) / 2
    panels = [('calculator', 'DBS Bank, Singapore', 'February 2025', [('About 4,000', 'temporary and contract roles to go over three years, as contracts end'), ('Permanent staff', 'not affected'), ('About 1,000', 'new AI-related jobs expected')],
               'Source: Reuters, 24 Feb 2025'),
              ('phone', 'BT Group, United Kingdom', 'May 2023', [('Up to 55,000', 'roles to go by 2030, most as its fibre build ends'), ('About 10,000', 'of them replaced by AI, mainly in customer service'), ('Unions', 'asked for contractors and natural leaving to go first')],
               'Source: The Guardian, 18 May 2023')]
    for i, (ic, org, when, rows, src) in enumerate(panels):
        x = 0.1 + i * (pw + 0.1)
        s.box(x, 0.55, pw, h - 0.65, '', fill=PAPER, lw=1.8, r=0.08)
        s.icon(ic, x + 0.45, h - 0.5, 0.6)
        s.text(x + 0.85, h - 0.4, org, size=16, weight='bold', ha='left')
        s.text(x + 0.85, h - 0.68, 'announced ' + when, size=14, ha='left', color=MUTE)
        y = h - 1.15
        for big, txt in rows:
            s.text(x + 0.2, y, big, size=17, weight='bold', ha='left', color=RED)
            hh = _wrap(s, x + 0.2, y - 0.2, pw - 0.4, txt, 14, ha='left', va='top', color=BODY)
            y -= 0.38 + hh + 0.12
        s.text(x + 0.2, 0.75, src, size=14, ha='left', color=MUTE)
    s.text(w / 2, 0.22, 'Both are plans. Check what happened before you quote them.', size=15, weight='bold')
    return s


# ------------------------------------------------------------------ adoption curve and the frontline stall (PPL-12)
@fig('x_l12_curve')
def x_l12_curve(w, h, **_):
    s = Scene(w, h)
    # left: a bell-shaped adoption curve in three bands
    lx, lw_, base = 0.15, 3.35, 1.55
    xs = np.linspace(0, 1, 200)
    ys = np.exp(-((xs - 0.5) ** 2) / (2 * 0.17 ** 2)) * 2.0
    X = lx + xs * lw_
    Y = base + ys
    bands = [(0.0, 0.25, GOLD), (0.25, 0.75, PAPER), (0.75, 1.0, PALE)]
    for a, b, col in bands:
        m = (xs >= a) & (xs <= b)
        s.ax.fill_between(X[m], base, Y[m], color=col, zorder=1)
    s.ax.plot(X, Y, color=INK, lw=2.2, zorder=3)
    s.line(lx, base, lx + lw_, base, lw=1.6, z=3)
    for a in (0.25, 0.75):
        s.line(lx + a * lw_, base, lx + a * lw_, base + float(np.interp(a, xs, ys)), lw=1.2, z=3)
    s.text(lx + lw_ / 2, h - 0.25, 'How people take up a new tool', size=15, weight='bold')
    labs = [(0.12, 'Try it early', 'your champions'), (0.5, 'Wait for proof', 'most of your staff'), (0.88, 'Hold back', 'need help or a reason')]
    for u, a, b in labs:
        _wrap(s, lx + u * lw_, base - 0.3, 1.1, a, 14, weight='bold', va='top')
        _wrap(s, lx + u * lw_, base - 0.82, 1.15, b, 14, color=BODY, va='top')
    s.line(3.75, 0.45, 3.75, h - 0.1, color=HAIR, lw=1.2)
    # right: BCG AI at Work 2025
    rx = 3.95
    s.text(rx, h - 0.25, 'BCG survey, 2025: out of every 100', size=15, weight='bold', ha='left')
    rows = [('Frontline staff using AI regularly', 51), ('Would use AI tools even if not allowed', 54),
            ('Fear their job could go in ten years', 41), ('Feel trained enough', 36), ('Frontline staff with enough guidance', 25)]
    y = h - 0.62
    bw = w - rx - 0.85
    for lab, v in rows:
        _wrap(s, rx, y, w - rx - 0.1, lab, 14, ha='left', va='top', color=BODY)
        _bar(s, rx, y - 0.36, bw, v, h=0.22, fill=RED if v in (51, 25) else GOLD)
        s.text(w - 0.1, y - 0.36, str(v), size=15, weight='bold', ha='right')
        y -= 0.7
    _source(s, 'Source: BCG AI at Work, 26 Jun 2025; office staff in 11 countries. The curve is a sketch.', y=0.18)
    return s


# ------------------------------------------------------------------ three fears and the answers (People and Skills Plan, part 3)
@fig('x_l12_fears')
def x_l12_fears(w, h, **_):
    s = Scene(w, h)
    rows = [('Will I lose my job?', 'No role is cut in this pilot.', 'Time saved goes to callbacks. We review it with you at day 90.'),
            ('Is my work being watched?', 'The log records the tool. It does not time you.', 'We never use the log to rate people.'),
            ('Will I be blamed for the AI’s mistakes?', 'The sender owns the reply. The AI only drafts.', 'Reporting an AI error is praised, and logged.')]
    c = [(0.1, 2.3, 'The fear'), (2.75, 2.35, 'What we say'), (5.3, w - 5.4, 'What we do')]
    for x, cw, hd in c:
        s.text(x + 0.1, h - 0.25, hd, size=16, weight='bold', ha='left', color=RED if hd == 'The fear' else INK)
    s.line(0.1, h - 0.48, w - 0.1, h - 0.48, lw=1.8)
    rh = (h - 1.05) / 3
    for i, row in enumerate(rows):
        y = h - 0.6 - (i + 1) * rh + 0.08
        for k, ((x, cw, _), txt) in enumerate(zip(c, row)):
            s.box(x, y, cw, rh - 0.14, '', fill=PALE if k == 0 else (GOLD if k == 1 else PAPER), lw=1.6, r=0.08)
            _wrap(s, x + 0.15, y + (rh - 0.14) / 2, cw - 0.3, txt, 15, weight='bold' if k == 0 else 'normal', ha='left')
            if k < 2:
                s.arrow(x + cw + 0.02, y + (rh - 0.14) / 2, c[k + 1][0] - 0.03, y + (rh - 0.14) / 2, lw=1.8, head=12)
    s.text(0.1, 0.2, 'Nile Valley Foods example, fictional. Promise only what you will keep.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ skills by level (People and Skills Plan, part 2)
@fig('x_l12_skills')
def x_l12_skills(w, h, **_):
    s = Scene(w, h)
    rows = [('Leaders', 'the top team', 'Read the monthly results; decide to widen, pause or stop', 1, 'person'),
            ('Builders', 'IT or the vendor', 'Set up the tool, its permissions and its log', 1, 'gear'),
            ('Power users', 'a few per team', 'Write and test briefs; check outputs against the source', 2, 'person'),
            ('Everyone', 'all staff', 'What the tool may do; the use policy; how to report an error', 4, 'person')]
    top = h - 0.1
    rh = (h - 0.95) / 4
    for i, (lev, who, learn, n, ic) in enumerate(rows):
        y = top - (i + 1) * rh
        indent = (3 - i) * 0.0
        s.box(0.1 + indent, y + 0.05, w - 0.2, rh - 0.1, '', fill=GOLD if i == 3 else PAPER, lw=1.8, r=0.08)
        for k in range(n):
            s.icon(ic, 0.45 + k * 0.32, y + rh / 2, 0.42, accent=PAPER if i == 3 else GOLD)
        s.text(1.75, y + rh / 2 + 0.15, lev, size=17, weight='bold', ha='left')
        s.text(1.75, y + rh / 2 - 0.17, who, size=14, ha='left', color=BODY)
        _wrap(s, 3.75, y + rh / 2, w - 3.95, learn, 16, ha='left', color=INK)
    _wrap(s, 0.1, 0.42, w - 0.2, 'Equity Group, Kenya, trained over 7,300 staff, about 62 in 100. Source: TechTrends Kenya, 25 Mar 2026.', 14, ha='left', color=MUTE)
    return s


# ------------------------------------------------------------------ the employee briefing (fictional example)
@fig('x_l12_briefing')
def x_l12_briefing(w, h, compact=False, **_):
    s = Scene(w, h)
    s.box(0.1, 0.1, w - 0.2, h - 0.2, '', fill=PAPER, lw=2, r=0.06)
    if compact:
        s.text(0.3, h - 0.38, 'Employee briefing (NVF, fictional)', size=15, weight='bold', ha='left')
        blocks = [('Why', 'Customers wait too long', PAPER, INK), ('What changes', 'AI drafts; you check and send', PAPER, INK),
                  ('Approved', 'The company assistant', GOLD, INK), ('Not approved', 'Customer data in personal tools', PAPER, RED),
                  ('No change', 'No role cut in the pilot', PAPER, INK), ('Errors', 'Tell your shift champion', PAPER, INK)]
        top, tsz, hsz = h - 0.58, 14, 14
    else:
        s.text(0.3, h - 0.4, 'Employee briefing: the customer-message assistant', size=16, weight='bold', ha='left')
        s.text(w - 0.3, h - 0.4, 'NVF, fictional', size=14, color=MUTE, ha='right')
        blocks = [('Why', 'Customers wait too long. The assistant drafts, so you answer faster and better.', PAPER, INK),
                  ('What changes for you', 'The AI sorts and drafts. You check, edit and send.', PAPER, INK),
                  ('Approved', 'The company assistant, for sorting and drafts.', GOLD, INK),
                  ('Not approved', 'Pasting customer data into personal AI tools.', PAPER, RED),
                  ('What does not change', 'No role is cut in this pilot. We review it with you at day 90.', PAPER, INK),
                  ('Questions and errors', 'Ask your shift champion. Log every AI error.', PAPER, INK)]
        top, tsz, hsz = h - 0.75, 14, 15
    s.line(0.3, top + 0.13, w - 0.3, top + 0.13, lw=1.4)
    cw = (w - 0.7) / 2
    bh = (top - 0.25 - 2 * 0.1) / 3
    for i, (hd, txt, fill, edge) in enumerate(blocks):
        x = 0.3 + (i % 2) * (cw + 0.1)
        y = top - (i // 2 + 1) * bh - (i // 2) * 0.1
        s.box(x, y, cw, bh, '', fill=fill, edge=edge, lw=2 if edge == RED else 1.2, r=0.06)
        s.text(x + 0.12, y + bh - 0.2, hd, size=hsz, weight='bold', ha='left', color=RED if edge == RED else INK)
        _wrap(s, x + 0.12, y + bh - 0.38, cw - 0.24, txt, tsz, ha='left', va='top', color=BODY)
    return s


# ------------------------------------------------------------------ champions and the feedback loop
@fig('x_l12_champions')
def x_l12_champions(w, h, **_):
    s = Scene(w, h)
    s.box(0.1, h - 0.95, 2.05, 0.82, '', fill=PAPER, lw=1.8, r=0.08)
    s.text(1.125, h - 0.38, 'Sponsor', size=15, weight='bold')
    s.text(1.125, h - 0.7, 'Managing Director', size=14, color=BODY)
    s.box(2.55, h - 0.95, 2.25, 0.82, '', fill=GOLD, lw=1.8, r=0.08)
    s.text(3.675, h - 0.38, 'Plan owner', size=15, weight='bold')
    s.text(3.675, h - 0.7, 'Customer Service Lead', size=14, color=BODY)
    s.arrow(2.17, h - 0.54, 2.53, h - 0.54, lw=1.8, head=12)
    for cx, lab in ((1.25, 'Morning champion'), (3.75, 'Afternoon champion')):
        s.arrow(3.675, h - 0.98, cx, h - 1.48, lw=1.8, head=12)
        s.icon('person', cx, h - 1.88, 0.66, accent=RED)
        s.text(cx, h - 2.4, lab, size=14, weight='bold')
        for k in range(4):
            px = cx - 0.84 + k * 0.56
            s.icon('person', px, h - 3.25, 0.44, accent=PAPER)
            s.line(cx, h - 2.58, px, h - 2.98, color=HAIR, lw=1.2, z=0)
    s.text(2.5, h - 3.72, 'Officers on each shift', size=14, color=BODY)
    rx = 5.15
    s.box(rx, 0.7, w - rx - 0.1, h - 0.8, '', fill=PAPER, edge=RED, lw=2, r=0.08)
    s.text(rx + 0.18, h - 0.38, 'The loop', size=16, weight='bold', color=RED, ha='left')
    items = ['Tips and answers go out', 'Errors and ideas come back', 'A weekly 15-minute review', 'One shared error log', 'Check-ins at day 30, 60, 90']
    yy = h - 0.75
    for it in items:
        yy -= _wrap(s, rx + 0.18, yy, w - rx - 0.4, it, 15, ha='left', va='top', color=BODY) + 0.2
    s.text(0.1, 0.3, 'Nile Valley Foods example, fictional: from the People and Skills Plan', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ worked example: the officer's role, task by task
@fig('x_l12_role')
def x_l12_role(w, h, **_):
    s = Scene(w, h)
    heads = ['Task today', 'With AI', 'Time on it', 'Skill it needs']
    cws = [3.0, 3.75, 1.35, w - 0.2 - 3.0 - 3.75 - 1.35]
    rows = [('Read and sort each message', 'AI sorts; the officer checks the doubtful ones', 'Less', 'Checking the AI’s doubtful cases'),
            ('Draft a reply', 'AI drafts; the officer edits and sends', 'Less', 'Editing, tone, knowing the policy'),
            ('Handle angry or unusual customers', 'Person only', 'More', 'Judgement, calm, authority to settle'),
            ('Call customers back', 'Person only, with the time freed', 'More', 'Listening and follow-through'),
            ('Report AI mistakes', 'Person, in the shared error log', 'New', 'Spotting and describing an error')]
    top = h - 0.05
    hh = 0.45
    x = 0.1
    for cw, hd in zip(cws, heads):
        s.rect(x, top - hh, cw, hh, fill=INK, edge=INK, lw=1.0)
        s.text(x + 0.12, top - hh / 2, hd, size=15, weight='bold', color=PAPER, ha='left')
        x += cw
    rh = (top - hh - 0.55) / len(rows)
    for r, row in enumerate(rows):
        y = top - hh - (r + 1) * rh
        x = 0.1
        for c, (cw, txt) in enumerate(zip(cws, row)):
            fill = PAPER
            if c == 2:
                fill = {'Less': PALE, 'More': GOLD, 'New': PAPER}[txt]
            s.rect(x, y, cw, rh, fill=fill, edge=RED if (c == 2 and txt == 'New') else INK, lw=2.0 if (c == 2 and txt == 'New') else 1.0, z=2 if c != 2 else 3)
            _wrap(s, x + 0.12, y + rh / 2, cw - 0.24, txt, 15, weight='bold' if c in (0, 2) else 'normal', ha='left', color=RED if (c == 2 and txt == 'New') else INK)
            x += cw
    _source(s, 'Why the officer checks: in Session 11 the AI got 9 of 12 right and one wrong with confidence (recorded, Claude, 4 Nov 2026).', y=0.22)
    return s


# ------------------------------------------------------------------ the People and Skills Plan, one page in four parts
@fig('x_l12_plan')
def x_l12_plan(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.25, 'People and Skills Plan: one page for your first AI use', size=16, weight='bold', ha='left')
    _wrap(s, 0.1, h - 0.52, w - 0.2, 'Nile Valley Foods example, fictional: sort and draft replies to customer messages. Sponsor: Managing Director. Owner: Customer Service Lead.', 14, ha='left', va='top', color=BODY)
    parts = [('1  The role, task by task', 'Task today, with AI, time on it, the skill it needs', 'grid'),
             ('2  Skills by level', 'Everyone, power users, builders, leaders', 'people'),
             ('3  Fears and answers', 'Jobs, being watched, being blamed: what we say and do', 'question'),
             ('4  Communication and champions', 'The why, what is approved, champions, feedback, check-ins', 'speech')]
    gap = 0.15
    pw = (w - 0.2 - gap) / 2
    ph = (h - 1.25 - gap) / 2
    for i, (hd, txt, ic) in enumerate(parts):
        x = 0.1 + (i % 2) * (pw + gap)
        y = 0.1 + (1 - i // 2) * (ph + gap)
        s.box(x, y, pw, ph, '', fill=GOLD if i == 0 else PAPER, lw=1.8, r=0.08)
        s.icon(ic, x + 0.45, y + ph - 0.5, 0.62)
        _wrap(s, x + 0.9, y + ph - 0.5, pw - 1.05, hd, 16, weight='bold', ha='left')
        _wrap(s, x + 0.2, y + 0.2, pw - 0.4, txt, 15, ha='left', va='bottom', color=BODY)
    return s
