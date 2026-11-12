"""Figures for Leadership Edition Session 13, Governance and buying.  Names: x_l13_*  (content kind 'l13_*').

No maths: risk scores are said in words and shown on a grid; costs are in shillings and counted, never written as formulas.
Case and law facts come from research/*.md (IDs in content/s13.py), each with a source line.  The Nile Valley Foods cost figures are the
plan figures of the Business Case Workbook example (demo_runs/s12/business_case_output.txt; invented inputs).  OrbitDesk is a fictional vendor.
"""
from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD, fig
import slidekit as K
from diagrams_l02 import _wrap, _fit, _source, _lh


# ------------------------------------------------------------------ hook: Kenya Airways, a board-approved AI policy (RTL-06)
@fig('x_l13_kq')
def x_l13_kq(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.28, 'Kenya Airways: every AI use is checked against one policy', size=17, weight='bold', ha='left')
    steps = [('A team proposes an AI use', PAPER), ('Checked against the board-approved data and AI policy', GOLD), ('Approved, changed or stopped', PAPER)]
    bw, gap = 2.3, 0.33
    x0 = (w - (3 * bw + 2 * gap)) / 2
    y = h - 1.75
    for i, (txt, fill) in enumerate(steps):
        x = x0 + i * (bw + gap)
        s.box(x, y, bw, 1.0, '', fill=fill, lw=1.8, r=0.08)
        _wrap(s, x + bw / 2, y + 0.5, bw - 0.25, txt, 15, weight='bold')
        if i < 2:
            s.arrow(x + bw + 0.03, y + 0.5, x + bw + gap - 0.03, y + 0.5, lw=2.2, head=14)
    facts = [('people', 'Over 1,000 staff', 'use an assistant for daily work'), ('doc', 'Maintenance papers', 'reviewed faster with AI'), ('grid', 'A data lake', 'one identifier per customer, still being built')]
    fw = (w - 0.2 - 0.3) / 3
    for i, (ic, a, b) in enumerate(facts):
        x = 0.1 + i * (fw + 0.15)
        s.box(x, 0.7, fw, 1.45, '', fill=PAPER, lw=1.4, r=0.08)
        s.icon(ic, x + 0.4, 1.78, 0.5)
        _wrap(s, x + 0.75, 1.78, fw - 0.85, a, 15, weight='bold', ha='left')
        _wrap(s, x + 0.15, 1.15, fw - 0.3, b, 14, ha='left', color=BODY)
    _source(s, 'Source: CIO Africa, 31 Aug 2026, CIO interview at a vendor event. No measured result.', y=0.25)
    return s


# ------------------------------------------------------------------ a ban hides use; a policy gives a safe route
@fig('x_l13_ban')
def x_l13_ban(w, h, **_):
    s = Scene(w, h)
    cw = (w - 0.3) / 2
    cols = [('Ban only', 'cross', RED, ['Staff use personal accounts', 'You cannot see what data leaves', 'Nobody is trained or checked', 'Errors stay hidden']),
            ('Policy and approved tools', 'shield', INK, ['Company accounts, each with an owner', 'Data rules by sensitivity', 'Training for every level', 'One place to report an error'])]
    for i, (hd, ic, col, items) in enumerate(cols):
        x = 0.1 + i * (cw + 0.1)
        s.box(x, 1.25, cw, h - 1.35, '', fill=PALE if i == 0 else PAPER, lw=1.8, r=0.08)
        s.icon(ic, x + 0.45, h - 0.48, 0.6)
        s.text(x + 0.85, h - 0.48, hd, size=16, weight='bold', ha='left', color=col)
        for k, it in enumerate(items):
            _wrap(s, x + 0.3, h - 1.15 - k * 0.62, cw - 0.45, it, 15, ha='left', color=INK)
    _wrap(s, 0.1, 0.85, w - 0.2, 'Microsoft 2024: 78 in 100 AI users bring their own tools to work. BCG 2025: 54 in 100 staff would use AI tools even if not allowed.', 14, ha='left', weight='bold')
    _source(s, 'Sources: Microsoft, 8 May 2024; BCG, 26 Jun 2025. No African country sampled.', y=0.2)
    return s


# ------------------------------------------------------------------ the acceptable use policy on one page (AI Use Policy Template)
@fig('x_l13_policy')
def x_l13_policy(w, h, **_):
    s = Scene(w, h)
    s.box(0.1, 0.1, w - 0.2, h - 0.2, '', fill=PAPER, lw=2, r=0.06)
    s.text(0.3, h - 0.38, 'AI Use Policy: six sections you draft today', size=16, weight='bold', ha='left')
    s.text(w - 0.3, h - 0.38, 'NVF example, fictional', size=14, color=MUTE, ha='right')
    s.line(0.3, h - 0.6, w - 0.3, h - 0.6, lw=1.4)
    secs = [('3  Approved tools', 'One company assistant, each with an owner'), ('4  What data may go in', 'Four questions; the strictest answer wins'),
            ('5  Human review', 'Money, customers, hiring: a named checker'), ('7  Accounts and owners', 'Company accounts only'),
            ('8  Incidents', 'Tell the Operations Manager within 4 hours'), ('10  Review date', 'The Managing Director, every 6 months')]
    cw = (w - 0.7) / 2
    bh = (h - 0.95 - 2 * 0.12) / 3
    for i, (hd, txt) in enumerate(secs):
        x = 0.3 + (i % 2) * (cw + 0.1)
        y = h - 0.75 - (i // 2 + 1) * bh - (i // 2) * 0.12
        s.box(x, y, cw, bh, '', fill=GOLD if i == 1 else PAPER, lw=1.2, r=0.06)
        s.text(x + 0.15, y + bh - 0.25, hd, size=15, weight='bold', ha='left')
        _wrap(s, x + 0.15, y + bh - 0.48, cw - 0.3, txt, 15, ha='left', va='top', color=BODY)
    return s


# ------------------------------------------------------------------ the 5 by 5 risk grid, with risks placed (no formulas)
@fig('x_l13_grid')
def x_l13_grid(w, h, risks=(), legend='short', numbers=True, **_):
    """risks: [{n, name, l, i}]. Cells show the score as a count; colours: High 15 or more, Medium 8 to 14, Low 7 or less."""
    s = Scene(w, h)
    cell = min((h - 1.0) / 5.0, 0.72)
    gx, gy = 0.75, 0.75
    for L in range(1, 6):
        for I in range(1, 6):
            sc = L * I
            fill = RED if sc >= 15 else (GOLD if sc >= 8 else PAPER)
            s.rect(gx + (L - 1) * cell, gy + (I - 1) * cell, cell, cell, fill=fill, edge=INK, lw=1.0, z=1)
            if numbers:
                s.text(gx + (L - 1) * cell + 0.08, gy + I * cell - 0.15, str(sc), size=14, ha='left', color=PAPER if fill == RED else BODY)
    for k in range(1, 6):
        s.text(gx + (k - 0.5) * cell, gy - 0.22, str(k), size=15, weight='bold')
        s.text(gx - 0.22, gy + (k - 0.5) * cell, str(k), size=15, weight='bold')
    s.text(gx + 2.5 * cell, gy - 0.55, 'Likelihood: how probable', size=15, weight='bold')
    s.text(0.15, gy + 2.5 * cell, 'Impact: how bad', size=15, weight='bold', rot=90)
    spots = {}
    for r in risks:
        spots.setdefault((r['l'], r['i']), []).append(r)
    for (L, I), rs in spots.items():
        cx, cy = gx + (L - 0.5) * cell + (0.1 if numbers else 0.0), gy + (I - 0.5) * cell - (0.1 if numbers else 0.0)
        offs = [0.0] if len(rs) == 1 else [-0.15, 0.15]
        for r, dx in zip(rs, offs):
            s.circle(cx + dx, cy, 0.15, fill=PAPER, edge=INK, lw=2.0, z=4)
            s.text(cx + dx, cy, str(r['n']), size=14, weight='bold', z=6)
    lx = gx + 5 * cell + 0.35
    top = gy + 5 * cell
    lw_ = w - lx - 0.1
    y = top
    s.text(lx, y, 'Risk: likelihood and impact', size=15, weight='bold', ha='left')
    y -= 0.42
    for r in sorted(risks, key=lambda q: q['n']):
        sc = r['l'] * r['i']
        lev = 'High' if sc >= 15 else ('Medium' if sc >= 8 else 'Low')
        lab = f"{r['n']}  {r['name']}: {r['l']} and {r['i']}, so {sc}, {lev}" if legend == 'full' else f"{r['n']}  {r['name']}: {sc}, {lev}"
        hh = _wrap(s, lx, y, lw_, lab, 14, ha='left', va='top', color=INK)
        y -= hh + 0.08
    y -= 0.15
    for col, txt in ((RED, 'High: 15 to 25'), (GOLD, 'Medium: 8 to 14'), (PAPER, 'Low: 1 to 7')):
        s.rect(lx, y - 0.2, 0.24, 0.24, fill=col, edge=INK, lw=1.0)
        s.text(lx + 0.35, y - 0.08, txt, size=14, ha='left')
        y -= 0.34
    return s


# ------------------------------------------------------------------ one row of the register, drawn as a flow
@fig('x_l13_row')
def x_l13_row(w, h, **_):
    s = Scene(w, h)
    cells = [('Risk', 'Data leakage: staff paste customer data into a free AI account', PAPER),
             ('Score', 'Likely enough, 3, and severe, 5: score 15, High', RED),
             ('Owner', 'Managing Director', PAPER),
             ('Control', 'Approved tools only, and a data table in the policy', GOLD),
             ('Left after it', 'Medium: watch it every quarter', PAPER)]
    n = len(cells)
    gap = 0.3
    bw = (w - 0.2 - gap * (n - 1)) / n
    y0, bh = 1.15, h - 1.6
    for i, (hd, txt, fill) in enumerate(cells):
        x = 0.1 + i * (bw + gap)
        s.box(x, y0, bw, bh, '', fill=fill, lw=1.8, r=0.08)
        s.text(x + 0.15, y0 + bh - 0.3, hd, size=17, weight='bold', ha='left', color=PAPER if fill == RED else INK)
        _wrap(s, x + 0.15, y0 + bh - 0.62, bw - 0.3, txt, 16, ha='left', va='top', color=PAPER if fill == RED else INK)
        if i < n - 1:
            s.arrow(x + bw + 0.03, y0 + bh / 2, x + bw + gap - 0.03, y0 + bh / 2, lw=2.2, head=14)
    s.text(0.1, h - 0.22, 'One row of the Risk Register, from its grey example', size=15, weight='bold', ha='left')
    _wrap(s, 0.1, 0.62, w - 0.2, 'A control is an action that lowers the likelihood or the impact. The risk left after it is called the residual risk.', 15, ha='left', color=BODY)
    _source(s, 'Template: Risk Register.xlsx, row 1 of the eight typical AI risks.', y=0.18)
    return s


# ------------------------------------------------------------------ Uganda: the Act, the PDPO acting, the strategy in draft (GOV-01 to GOV-05)
@fig('x_l13_uganda')
def x_l13_uganda(w, h, **_):
    s = Scene(w, h)
    ev = [('May 2019', 'Data Protection and Privacy Act in force', 'Personal data; fines up to 245 currency points; courts can fine firms up to 2 in 100 of turnover', PAPER),
          ('2021', 'Regulations; the PDPO starts work', 'Register with the PDPO; report a breach immediately', PAPER),
          ('July 2025', 'PDPO rules against Google', 'Register within 30 days and show safe transfers abroad. Google withdrew its appeal.', GOLD),
          ('July 2025', 'First criminal conviction', 'For not registering: a debt collector that shared a borrower’s photo', PAPER),
          ('October 2026', 'National Data Strategy launched', 'Groundwork for AI in government', PAPER),
          ('30 Oct 2026', 'National AI strategy', 'Still a draft, awaiting Cabinet', PALE)]
    n = len(ev)
    gap = 0.12
    bw = (w - 0.2 - gap * (n - 1)) / n
    ly = h - 0.55
    s.line(0.1, ly, w - 0.1, ly, lw=2.4, z=1)
    for i, (when, hd, txt, fill) in enumerate(ev):
        x = 0.1 + i * (bw + gap)
        s.circle(x + bw / 2, ly, 0.11, fill=RED if fill == PALE else INK, edge=INK, z=3)
        s.text(x + bw / 2, ly + 0.3, when, size=15, weight='bold', color=RED if fill == PALE else INK)
        s.box(x, 0.55, bw, ly - 0.75, '', fill=fill, edge=RED if fill == PALE else INK, lw=1.8, r=0.08)
        hh = _wrap(s, x + 0.12, ly - 0.35, bw - 0.24, hd, 15, weight='bold', ha='left', va='top')
        _wrap(s, x + 0.12, ly - 0.5 - hh, bw - 0.24, txt, 14, ha='left', va='top', color=BODY)
    _source(s, 'Sources: DLA Piper; URSB 2025; HapaKenya 2025; Lex Africa 2025; Daily Monitor 2026; Ecofin, 30 Oct 2026.', y=0.2)
    return s


# ------------------------------------------------------------------ regulators in the region already fine (GOV-06, GOV-08, GOV-09)
@fig('x_l13_fines')
def x_l13_fines(w, h, **_):
    s = Scene(w, h)
    cw = (w - 0.3) / 2
    panels = [('Kenya: data commissioner', [('KES 5 million', 'Oppo Kenya, 2022: an image posted without consent'), ('KES 5 million', 'WhitePath, a digital lender, 2023: harassing borrowers’ contacts'),
                                                       ('KES 2,975,000', 'Two lending apps, 2023: threats to borrowers’ contacts')]),
              ('Nigeria: data commission', [('NGN 555.8 million', 'Fidelity Bank, 2024: weak security, no breach procedure. The bank disputes it.'), ('NGN 766.2 million', 'Multichoice, 2025: privacy, and personal data sent abroad unlawfully')])]
    for i, (hd, rows) in enumerate(panels):
        x = 0.1 + i * (cw + 0.1)
        s.box(x, 0.85, cw, h - 0.95, '', fill=PAPER, lw=1.8, r=0.08)
        _wrap(s, x + 0.15, h - 0.3, cw - 0.3, hd, 16, weight='bold', ha='left')
        y = h - 0.85
        for big, txt in rows:
            s.text(x + 0.15, y, big, size=17, weight='bold', ha='left', color=RED)
            hh = _wrap(s, x + 0.15, y - 0.2, cw - 0.3, txt, 14, ha='left', va='top', color=BODY)
            y -= 0.45 + hh + 0.1
    _wrap(s, 0.1, 0.55, w - 0.2, 'None of these is an AI case. They are about the personal data your AI tools use.', 15, ha='left', weight='bold')
    _source(s, 'Sources: Kenya News Agency 2023; Infusion Lawyers 2024; Nairametrics 2025.', y=0.17)
    return s


# ------------------------------------------------------------------ names you will hear: EU AI Act dates as amended, AU, ISO, NIST
@fig('x_l13_frameworks')
def x_l13_frameworks(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.25, 'EU AI Act: binds you only if you sell into the EU, or your AI output is used there', size=16, weight='bold', ha='left')
    dates = [('1 Aug 2024', 'In force'), ('2 Feb 2025', 'Bans; staff AI literacy'), ('2 Aug 2025', 'Rules for general-purpose models'),
             ('2 Dec 2027', 'High-risk uses: hiring, credit, education'), ('2 Aug 2028', 'AI inside regulated products')]
    n = len(dates)
    x0, x1 = 1.3, w - 1.3
    ly = h - 1.05
    s.line(0.2, ly, w - 0.2, ly, lw=2.4, z=1)
    sp = (x1 - x0) / (n - 1)
    for i, (d, t) in enumerate(dates):
        x = x0 + i * sp
        moved = i >= 3
        s.circle(x, ly, 0.11, fill=RED if moved else INK, edge=INK, z=3)
        s.text(x, ly + 0.3, d, size=15, weight='bold', color=RED if moved else INK)
        _wrap(s, x, ly - 0.22, sp - 0.15, t, 14, va='top', color=BODY)
    s.text(w - 0.15, ly - 0.98, 'Red: dates moved by the 2026 amendment', size=14, color=RED, ha='right')
    cards = [('flag', 'African Union Continental AI Strategy', 'Endorsed July 2024. A strategy; it does not bind.'),
             ('stamp', 'ISO/IEC 42001', 'December 2023. An AI management system a firm can be certified against. Voluntary.'),
             ('shield', 'NIST AI Risk Management Framework', 'January 2023, voluntary: govern, map, measure, manage. Being revised.')]
    cw = (w - 0.2 - 0.3) / 3
    for i, (ic, hd, txt) in enumerate(cards):
        x = 0.1 + i * (cw + 0.15)
        s.box(x, 0.45, cw, 1.6, '', fill=PAPER, lw=1.6, r=0.08)
        s.icon(ic, x + 0.38, 1.72, 0.5)
        _wrap(s, x + 0.72, 1.72, cw - 0.82, hd, 15, weight='bold', ha='left')
        _wrap(s, x + 0.15, 1.27, cw - 0.3, txt, 14, ha='left', va='top', color=BODY)
    _source(s, 'Sources: European Commission, accessed 11 Nov 2026; AU, 28 Aug 2024; IEC Webstore; NIST. Check before you rely on dates.', y=0.15)
    return s


# ------------------------------------------------------------------ total cost of ownership in shillings (NVF business case, Session 11)
@fig('x_l13_tco')
def x_l13_tco(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.25, 'Nile Valley Foods, first year of the customer-message assistant', size=15, weight='bold', ha='left')
    parts = [('Set-up and training, once', 480000, PALE), ('Licence, 12 months', 720000, GOLD),
             ('People checking, 12 months', 480000, PAPER), ('Upkeep, 12 months', 540000, PAPER)]
    total = sum(p[1] for p in parts)
    bx, bw = 0.3, 1.6
    top = h - 0.55
    H = top - 0.75
    y = top
    for lab, v, fill in parts:
        hh = H * v / total
        s.rect(bx, y - hh, bw, hh, fill=fill, edge=INK, lw=1.4, z=2)
        s.line(bx + bw, y - hh / 2, bx + bw + 0.3, y - hh / 2, lw=1.2)
        s.text(bx + bw + 0.38, y - hh / 2 + 0.13, lab, size=14, ha='left', weight='bold')
        s.text(bx + bw + 0.38, y - hh / 2 - 0.15, f'UGX {v:,}', size=14, ha='left', color=BODY)
        y -= hh
    s.brace(bx - 0.05, bx + bw + 0.05, top + 0.08, depth=-0.08)
    tx = 5.0
    s.text(tx + 0.15, top - 0.3, 'All of it', size=15, weight='bold', ha='left')
    s.text(tx + 0.15, top - 0.72, f'UGX {total:,}', size=24, weight='bold', ha='left')
    _wrap(s, tx + 0.15, top - 1.0, w - tx - 0.4, 'The licence is about a third', 14, ha='left', va='top')
    s.line(tx, top - 1.7, w - 0.1, top - 1.7, color=HAIR, lw=1.2)
    s.text(tx + 0.15, top - 2.02, 'Not yet counted', size=15, weight='bold', ha='left', color=RED)
    yy = top - 2.3
    for it in ['Use above the plan', 'A price rise at renewal', 'Leaving: getting your data back']:
        yy -= _wrap(s, tx + 0.15, yy, w - tx - 0.4, it, 14, ha='left', va='top', color=BODY) + 0.1
    _source(s, 'Plan figures: Session 11 Business Case Workbook example, invented inputs.', y=0.25)
    return s


# ------------------------------------------------------------------ the AI review helped; you still check
@fig('x_l13_check')
def x_l13_check(w, h, **_):
    s = Scene(w, h)
    cw = (w - 0.3) / 2
    cols = [('What the AI reviews did', 'check', GOLD, ['Caught all 11 planted red flags, in both runs', 'Wrote eight questions for the vendor', 'Suggested a small, read-only pilot first']),
            ('What you still do', 'flag', PAPER, ['Check every quote: run 2 quoted two phrases that are not in the proposal', 'Judge the vendor’s answers yourself', 'Test the claims on your own data'])]
    for i, (hd, ic, fill, items) in enumerate(cols):
        x = 0.1 + i * (cw + 0.1)
        s.box(x, 0.65, cw, h - 0.75, '', fill=PAPER, lw=1.8, r=0.08)
        s.icon(ic, x + 0.42, h - 0.45, 0.55)
        s.text(x + 0.8, h - 0.45, hd, size=17, weight='bold', ha='left')
        y = h - 1.0
        for it in items:
            y -= _wrap(s, x + 0.25, y, cw - 0.4, it, 15, ha='left', va='top') + 0.25
    s.text(0.1, 0.25, 'Recorded runs: Claude, two fresh sessions, 4 Nov 2026. OrbitDesk is invented.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ who owns AI governance
@fig('x_l13_owners')
def x_l13_owners(w, h, **_):
    s = Scene(w, h)
    rows = [('Board', 'Approves the policy; hears the top risks every quarter', 'shield', GOLD),
            ('Managing Director', 'Owns AI governance; names an owner for each use', 'person', PAPER),
            ('Owner of each AI use', 'Answers for its results, its risks and its register row', 'flag', PAPER),
            ('IT and data protection', 'Approved tools, access, the log; personal data and the PDPO', 'lock', PAPER),
            ('HR and managers', 'Train staff on the policy; the People and Skills Plan', 'people', PAPER)]
    rh = (h - 0.65) / len(rows)
    for i, (who, what, ic, fill) in enumerate(rows):
        y = h - 0.1 - (i + 1) * rh
        s.box(0.1, y + 0.05, w - 0.2, rh - 0.1, '', fill=fill, lw=1.6, r=0.08)
        s.icon(ic, 0.5, y + rh / 2, 0.5)
        _wrap(s, 0.95, y + rh / 2, 2.4, who, 16, weight='bold', ha='left')
        _wrap(s, 3.45, y + rh / 2, w - 3.65, what, 15, ha='left', color=INK)
        if i < len(rows) - 1:
            pass
    s.text(0.1, 0.22, 'Kenya Airways’ board approved its data and AI policy (CIO Africa, 31 Aug 2026).', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ the board briefing, one page
@fig('x_l13_board')
def x_l13_board(w, h, compact=False, **_):
    s = Scene(w, h)
    s.box(0.1, 0.1, w - 0.2, h - 0.2, '', fill=PAPER, lw=2, r=0.06)
    s.text(0.3, h - 0.38, 'Board briefing on AI: one page' + (' (NVF)' if compact else ', every quarter'), size=16 if not compact else 15, weight='bold', ha='left')
    if not compact:
        s.text(w - 0.3, h - 0.38, 'NVF example, fictional', size=14, color=MUTE, ha='right')
    s.line(0.3, h - 0.6, w - 0.3, h - 0.6, lw=1.4)
    if compact:
        secs = [('What we use', 'One assistant, 2 uses'), ('Top risks', 'Leakage; wrong answer'), ('Policy', 'Draft; legal review'), ('We ask', 'Approve the policy')]
    else:
        secs = [('What we use', 'One company assistant: customer messages and sales notes'), ('Top three risks', 'Data leakage, a wrong answer, a vendor lock-in: owners and controls'),
                ('Policy and training', 'Draft written; lawyer review booked; staff trained by level'), ('The law', 'Personal data under the 2019 Act; national AI strategy still a draft'),
                ('Vendors', 'One proposal declined; questions sent to another'), ('We ask the board', 'Approve the policy; agree the review date')]
    cw = (w - 0.7) / 2
    rows = (len(secs) + 1) // 2
    bh = (h - 0.95 - (rows - 1) * 0.12) / rows
    for i, (hd, txt) in enumerate(secs):
        x = 0.3 + (i % 2) * (cw + 0.1)
        y = h - 0.75 - (i // 2 + 1) * bh - (i // 2) * 0.12
        last = i == len(secs) - 1
        s.box(x, y, cw, bh, '', fill=GOLD if last else PAPER, lw=1.2, r=0.06)
        s.text(x + 0.15, y + bh - 0.24, hd, size=15 if not compact else 14, weight='bold', ha='left')
        _wrap(s, x + 0.15, y + bh - 0.45, cw - 0.3, txt, 14, ha='left', va='top', color=BODY)
    return s


# ------------------------------------------------------------------ a plain two-column pairing (local variant of t13_bridge, without gold on every row)
@fig('x_l13_pairs')
def x_l13_pairs(w, h, rows=(), heads=('', ''), size=16, **_):
    s = Scene(w, h)
    n = len(rows)
    top = h - 0.45
    rh = (top - 0.05) / n
    rx = w * 0.5
    s.text(0.05, h - 0.22, heads[0], size=size + 1, weight='bold', ha='left', color=MUTE)
    s.text(rx, h - 0.22, heads[1], size=size + 1, weight='bold', ha='left', color=MUTE)
    s.line(0, top, w, top, color=INK, lw=2.0)
    for i, r in enumerate(rows):
        y = top - (i + 0.5) * rh
        _wrap(s, 0.05, y, rx - 0.75, r['what'], size, ha='left', color=BODY)
        s.arrow(rx - 0.6, y, rx - 0.15, y, lw=2.0, head=14)
        _wrap(s, rx, y, w - rx - 0.05, r['rule'], size, weight='bold', ha='left')
        s.line(0, top - (i + 1) * rh, w, top - (i + 1) * rh, color=HAIR, lw=1.0)
    return s
