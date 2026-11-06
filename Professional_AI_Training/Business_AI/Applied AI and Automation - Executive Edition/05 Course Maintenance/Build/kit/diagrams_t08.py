"""Figures for Session 8: prompting and reasoning models.

Kinds: brief, briefs, fivepart, fewshot, delims, structured, checkgrid, promptlog, payroll, slip, reasoning, vendors, template.
Data drawn here is from recorded runs: Case Runs F1a and F1b (4 November 2026) and demo_runs/s08_prompting_runs.md (6 November 2026).
"""
from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD, fig
import slidekit as K


def _wrap(s, cx, cy, width, text, size, weight='normal', color=INK, ha='center'):
    lines = K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', width)
    x = cx if ha == 'center' else cx - width / 2
    return s.text(x if ha == 'center' else cx, cy, '\n'.join(lines), size=size, weight=weight, color=color, ha=ha)


def _lt(s, x, cy, width, text, size, weight='normal', color=INK):
    """Left aligned wrapped text with its vertical centre at cy."""
    lines = K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', width)
    return s.text(x, cy, '\n'.join(lines), size=size, weight=weight, color=color, ha='left')


# ----------------------------------------------------------------------------------------------- brief to a colleague
@fig('x_t08_brief')
def brief(w, h, **_):
    s = Scene(w, h)
    s.icon('person', 0.75, h - 0.85, 1.1)
    s.text(1.6, h - 0.7, 'A colleague on day one', size=19, weight='bold', ha='left')
    s.text(1.6, h - 1.1, 'knows nothing about your company', size=16, color=BODY, ha='left')
    rows = [('Role', 'You are the sales analyst'), ('Context', 'The reader is Sarah, the Sales Director'), ('Examples', 'One finished email to copy'),
            ('Format', 'Subject, summary, table'), ('Checks', 'Use only these figures; say when unsure')]
    top = h - 1.65
    rh = (top - 0.05) / 5
    for i, (a, b) in enumerate(rows):
        y = top - (i + 1) * rh
        s.box(0.05, y + 0.06, 1.55, rh - 0.12, a, size=18, weight='bold', fill=GOLD, lw=1.8)
        s.box(1.7, y + 0.06, w - 1.75, rh - 0.12, '', fill=PAPER, lw=1.4)
        _lt(s, 1.85, y + rh / 2, w - 2.05, b, 17)
    return s


# ----------------------------------------------------------------------------------------------- weak vs strong brief
@fig('x_t08_briefs')
def briefs(w, h, **_):
    s = Scene(w, h)
    gap = 0.2
    pw = (w - gap - 0.1) / 2
    cols = [('Weak brief', '"Write the Monday sales email." and the data', [('check', 'Figures right'), ('cross', 'Own layout'), ('cross', 'Advice nobody asked for'), ('cross', '"[Your name]" left in')]),
            ('Strong brief', 'Role, reader, format, limits, "do not invent"', [('check', 'Figures right'), ('check', 'Format followed'), ('check', 'Said the cause is unknown'), ('check', 'One thing to check')])]
    for i, (hd, q, items) in enumerate(cols):
        x0 = 0.05 + i * (pw + gap)
        s.box(x0, 0.05, pw, h - 0.1, '', fill=GOLD if i else PAPER, edge=INK, lw=2.0, r=0.06)
        s.text(x0 + 0.2, h - 0.38, hd, size=20, weight='bold', ha='left')
        _lt(s, x0 + 0.2, h - 1.05, pw - 0.4, q, 15, color=BODY)
        for k, (ic, tx) in enumerate(items):
            yy = h - 1.85 - k * 0.55
            s.icon(ic, x0 + 0.4, yy, 0.4)
            _lt(s, x0 + 0.75, yy, pw - 0.9, tx, 16, weight='bold' if ic == 'cross' else 'normal', color=RED if ic == 'cross' else INK)
    return s


# ----------------------------------------------------------------------------------------------- five parts on the real strong prompt
@fig('x_t08_fivepart')
def fivepart(w, h, **_):
    s = Scene(w, h)
    rows = [('Role', 'You are the sales analyst at Nile Valley Foods Ltd.', False),
            ('Context', 'Write the Monday sales email to the Sales Director, Sarah Namukasa.', False),
            ('Format', 'A subject line, a two-sentence summary, a short table, at most three plain sentences.', False),
            ('Checks', 'Use only the figures below. Do not invent any number, cause or customer. If something cannot be explained, say so.', False),
            ('Examples', 'None in this brief. Add one finished email when the format matters.', True)]
    rh = (h - 0.1) / 5
    for i, (a, b, missing) in enumerate(rows):
        y = h - 0.05 - (i + 1) * rh
        s.box(0.05, y + 0.06, 1.9, rh - 0.12, a, size=19, weight='bold', fill=PAPER if missing else GOLD, edge=RED if missing else INK, lw=2.0, dash=missing)
        s.box(2.05, y + 0.06, w - 2.1, rh - 0.12, '', fill=PAPER, edge=RED if missing else INK, lw=1.4, dash=missing)
        _lt(s, 2.25, y + rh / 2, w - 2.5, b, 17, color=RED if missing else INK)
    return s


# ----------------------------------------------------------------------------------------------- few-shot
@fig('x_t08_fewshot')
def fewshot(w, h, **_):
    s = Scene(w, h)
    s.text(0.05, h - 0.2, 'Two finished examples, then the new case', size=17, weight='bold', ha='left')
    rows = [('Example 1', '"Please send 30 bags of rice to Kamuli."', 'Order', False),
            ('Example 2', '"Invoice paid by mobile money today."', 'Payment', False),
            ('Your case', '"The oil we got was leaking."', '?', True)]
    top = h - 0.55
    rh = (top - 0.05) / 3
    for i, (lab, msg, ans, new) in enumerate(rows):
        y = top - (i + 1) * rh
        s.box(0.05, y + 0.1, w - 0.1, rh - 0.2, '', fill=GOLD if new else PAPER, edge=RED if new else INK, lw=2.0, dash=new)
        s.text(0.25, y + rh - 0.35, lab, size=15, weight='bold', ha='left', color=RED if new else MUTE)
        _lt(s, 0.25, y + rh / 2 - 0.1, w - 3.2, msg, 17)
        s.arrow(w - 2.85, y + rh / 2 - 0.05, w - 2.1, y + rh / 2 - 0.05, lw=2, head=14)
        s.box(w - 2.0, y + rh / 2 - 0.4, 1.85, 0.7, ans, size=20, weight='bold', fill=PAPER, lw=1.8)
    return s


# ----------------------------------------------------------------------------------------------- delimiters
@fig('x_t08_delims')
def delims(w, h, **_):
    s = Scene(w, h)
    s.box(0.05, h - 1.7, w - 0.1, 1.6, '', fill=GOLD, lw=2.0)
    s.text(0.25, h - 0.4, 'Instructions (the cover sheet)', size=16, weight='bold', ha='left')
    _lt(s, 0.25, h - 1.15, w - 0.5, 'Label each message below as order, payment, complaint or question. Return a table.', 17)
    s.text(0.25, h - 2.05, '### MESSAGES START', size=16, weight='bold', ha='left', mono=True)
    s.box(0.05, 1.45, w - 0.1, h - 3.75, '', fill=PALE, edge=INK, lw=1.6)
    s.text(0.25, h - 2.55, 'Data (the folder)', size=16, weight='bold', ha='left')
    _lt(s, 0.25, h - 3.2, w - 0.5, '1. Please send 40 bags of sugar.   2. Invoice INV-2291 is paid.', 16, color=BODY)
    s.text(0.25, 1.2, '### MESSAGES END', size=16, weight='bold', ha='left', mono=True)
    s.tag(0.1, 0.35, 'Orders hidden in the data can still be followed', size=15, fill=RED)
    return s


# ----------------------------------------------------------------------------------------------- structured output (real record)
@fig('x_t08_structured')
def structured(w, h, **_):
    s = Scene(w, h)
    lw_ = 2.7
    s.box(0.05, 0.9, lw_, h - 1.0, '', fill=PAPER, lw=1.8)
    s.icon('mail', 0.45, h - 0.5, 0.55)
    s.text(0.8, h - 0.5, 'Message 3', size=16, weight='bold', ha='left')
    _lt(s, 0.2, h / 2 - 0.1, lw_ - 0.3, 'The cooking oil jerrycans delivered yesterday to Busia were leaking and 6 of them are unusable. I want a replacement today or my money back.', 15)
    s.arrow(0.05 + lw_ + 0.05, h / 2, 0.05 + lw_ + 0.5, h / 2, lw=2.4, head=16)
    cx = 0.05 + lw_ + 0.6
    lines = ['{ "id": 3,', '  "customer": null,', '  "type": "complaint",', '  "items": [{"product":', '    "cooking oil jerrycans",', '    "quantity": 6}],',
             '  "amount_ugx": null,', '  "urgency": "high",', '  "reference": null }']
    s.code(cx, h - 0.35, lines, size=14, line_h=0.28, w=w - cx - 0.05, hl_lines=(2, 7))
    s.text(cx, 0.3, 'Real reply of the recorded run', size=15, color=BODY, ha='left')
    return s


# ----------------------------------------------------------------------------------------------- check grid of the structured run
@fig('x_t08_checkgrid')
def checkgrid(w, h, **_):
    s = Scene(w, h)
    cw = [1.4, 2.1, 1.5, 1.6, 1.5, 1.6, 2.2]
    s_ = sum(cw)
    cw = [c * (w - 0.1) / s_ for c in cw]
    heads = ['Message', 'Customer', 'Type', 'Items', 'Amount', 'Urgency', 'Reference']
    cells = [['1', 'name + shop in one', 'ok', 'ok', 'ok', 'ok', 'ok'],
             ['2', 'ok', 'ok', 'ok', 'ok', 'ok', 'two joined'],
             ['3', 'ok', 'ok', 'ok', 'ok', 'ok', 'ok'],
             ['4', 'ok', 'ok', 'ok', 'ok', 'ok', 'ok']]
    top = h - 0.05
    rh = 0.52
    x = 0.05
    for j, t in enumerate(heads):
        s.text(x + cw[j] / 2, top - rh / 2, t, size=16, weight='bold')
        x += cw[j]
    s.line(0.05, top - rh, w - 0.05, top - rh, color=INK, lw=2.2)
    for i, row in enumerate(cells):
        y = top - rh * (i + 2)
        x = 0.05
        for j, v in enumerate(row):
            flag = v not in ('ok',) and j > 0
            if flag:
                s.rect(x + 0.03, y + 0.04, cw[j] - 0.06, rh - 0.08, fill=GOLD, edge=INK, lw=1.4, z=1)
            s.text(x + cw[j] / 2, y + rh / 2, v, size=15 if flag else 16, weight='bold' if (flag or j == 0) else 'normal', color=INK if (flag or j == 0) else MUTE)
            x += cw[j]
        s.line(0.05, y, w - 0.05, y, color=HAIR, lw=1)
    yb = top - rh * 6
    s.text(0.05, yb - 0.3, 'A program checked the shape: valid JSON, four records, the right fields.', size=17, ha='left', weight='bold')
    s.text(0.05, yb - 0.75, 'A person found the two loose fields: the schema allowed one text for two facts.', size=17, ha='left', color=BODY)
    return s


# ----------------------------------------------------------------------------------------------- test loop and prompt log
@fig('x_t08_promptlog')
def promptlog(w, h, **_):
    s = Scene(w, h)
    steps = ['Write the prompt', 'Run it on a checked set', 'Score against the key', 'Change one thing']
    n = 4
    gap = 0.45
    bw = (w - 0.1 - gap * 3) / n
    for i, t in enumerate(steps):
        x = 0.05 + i * (bw + gap)
        s.box(x, h - 0.85, bw, 0.75, t, size=16, weight='bold', fill=GOLD if i == 2 else PAPER, lw=1.8)
        if i < n - 1:
            s.arrow(x + bw + 0.04, h - 0.475, x + bw + gap - 0.04, h - 0.475, lw=2.2, head=15)
    rows = [['Version', 'What changed', 'Runs', 'Right', 'Next change'],
            ['Payroll plain', 'One plain paragraph', '2', '1 of 2', 'Add the re-add line'],
            ['Payroll framed', 'Goal, rules, output, re-add', '2', '2 of 2', 'Split framing from re-add'],
            ['Orders v1', 'JSON with fixed fields', '1', 'Valid JSON', 'Split the reference field']]
    cwid = [1.6, 3.7, 0.9, 1.7, 3.8]
    sc = (w - 0.1) / sum(cwid)
    cwid = [c * sc for c in cwid]
    s.table(0.05, h - 1.15, cwid, 0.62, rows, size=15, align=['left', 'left', 'center', 'center', 'left'], hl_cells={(2, 3): GOLD, (1, 3): PAPER})
    return s


# ----------------------------------------------------------------------------------------------- payroll runs
@fig('x_t08_payroll')
def payroll(w, h, **_):
    s = Scene(w, h)
    c0 = 4.9
    rc = 1.5
    cw = (w - c0 - rc - 0.05) / 3
    s.text(0.1, h - 0.3, 'Prompt variant', size=16, weight='bold', ha='left')
    for j in range(3):
        s.text(c0 + j * cw + cw / 2, h - 0.3, 'Run %d' % (j + 1), size=16, weight='bold')
    s.text(w - rc / 2, h - 0.3, 'Right', size=16, weight='bold')
    s.line(0.05, h - 0.6, w - 0.05, h - 0.6, color=INK, lw=2.2)
    key = '1,802,898'
    rows = [('Plain', 'facts and a question', ['1,802,898', '1,612,898']),
            ('Plain + re-add', 'plain, plus one re-add sentence', ['1,802,898'] * 3),
            ('Framed, no re-add', 'goal, rules, output; no re-add', ['1,802,898'] * 3),
            ('Framed + re-add', 'framed, plus re-add sentence', ['1,802,898'] * 2)]
    rh = (h - 0.6 - 1.2) / 4
    for i, (name, sub, vals) in enumerate(rows):
        y = h - 0.6 - (i + 1) * rh
        s.text(0.1, y + rh * 0.68, name, size=17, weight='bold', ha='left')
        s.text(0.1, y + rh * 0.3, sub, size=14, color=BODY, ha='left')
        for j, v in enumerate(vals):
            ok = v == key
            cx = c0 + j * cw + cw / 2
            s.box(cx - cw / 2 + 0.08, y + 0.1, cw - 0.16, rh - 0.2, v, size=16, weight='bold', fill=GOLD if ok else PAPER, edge=INK if ok else RED, lw=2.0 if ok else 2.6)
        good = sum(v == key for v in vals)
        s.text(w - rc / 2, y + rh / 2, '%d of %d' % (good, len(vals)), size=18, weight='bold')
        s.line(0.05, y, w - 0.05, y, color=HAIR, lw=1)
    s.text(0.1, 0.8, 'Boxes show net pay (UGX). Key, worked out separately: 1,802,898. Total cost key: 2,261,250.', size=14, ha='left', weight='bold')
    s.text(0.1, 0.4, 'Gold = matches the key. Red = wrong. 10 runs, Claude fresh subagents, 6 November 2026.', size=14, ha='left', color=BODY)
    return s


# ----------------------------------------------------------------------------------------------- the slip
@fig('x_t08_slip')
def slip(w, h, **_):
    s = Scene(w, h)
    s.text(0.05, h - 0.25, 'Gross pay: salary + overtime - leave deduction', size=17, weight='bold', ha='left')
    bw = (w - 0.1 - 0.9) / 3
    items = ['1,800,000', '+ 337,500', '- 81,818']
    for i, t in enumerate(items):
        s.box(0.05 + i * (bw + 0.45), h - 1.45, bw, 0.9, t, size=21, weight='bold')
    s.box(0.05, h / 2 - 0.2, w - 0.1, 0.9, '= 2,055,682   The key', size=22, weight='bold', fill=GOLD, lw=2.0)
    s.box(0.05, 1.05, w - 0.1, 0.9, '= 1,855,682   Plain run 2', size=22, weight='bold', edge=RED, lw=2.6)
    s.text(w / 2, 0.45, '200,000 out. Every line was shown. The tone was calm.', size=17, weight='bold', color=RED)
    return s


# ----------------------------------------------------------------------------------------------- standard vs reasoning
@fig('x_t08_reasoning')
def reasoning(w, h, **_):
    s = Scene(w, h)
    lane_h = 1.7
    specs = [('Standard model', 'answers straight away', False), ('Reasoning model', 'thinks first, then answers', True)]
    for i, (name, sub, think) in enumerate(specs):
        y = h - 0.1 - (i + 1) * lane_h - i * 0.25
        s.text(0.05, y + lane_h - 0.3, name, size=21, weight='bold', ha='left')
        s.text(0.05, y + lane_h - 0.7, sub, size=16, color=BODY, ha='left')
        s.box(3.6, y + 0.4, 1.6, 0.9, 'Your prompt', size=16, weight='bold')
        if think:
            s.arrow(5.25, y + 0.85, 5.85, y + 0.85, lw=2.2, head=15)
            s.box(5.9, y + 0.3, 3.0, 1.1, 'Works through\nthe problem first', size=16, weight='bold', fill=GOLD, lw=2.0, dash=True)
            s.arrow(8.95, y + 0.85, 9.55, y + 0.85, lw=2.2, head=15)
            s.box(9.6, y + 0.4, 1.9, 0.9, 'Answer', size=17, weight='bold')
            s.tag(5.9, y - 0.15, 'Slower', size=15, fill=RED)
            s.tag(7.1, y - 0.15, 'Thinking can add to the bill', size=15, fill=INK)
        else:
            s.arrow(5.25, y + 0.85, 9.55, y + 0.85, lw=2.2, head=15)
            s.box(9.6, y + 0.4, 1.9, 0.9, 'Answer', size=17, weight='bold')
            s.tag(5.9, y + 0.05, 'Faster', size=15, fill=INK)
    return s


# ----------------------------------------------------------------------------------------------- vendor guidance
@fig('x_t08_vendors')
def vendors(w, h, **_):
    s = Scene(w, h)
    c0 = 1.6
    c1 = 6.2
    c2 = w - c0 - c1 - 0.05
    s.text(c0 + c1 / 2, h - 0.25, 'What the guide says about reasoning or thinking models', size=15, weight='bold')
    s.text(c0 + c1 + c2 / 2, h - 0.25, 'What it says about testing', size=15, weight='bold')
    s.line(0.05, h - 0.55, w - 0.05, h - 0.55, color=INK, lw=2.2)
    rows = [('OpenAI', 'Use short, direct prompts. Step-by-step instructions are unnecessary and can sometimes hurt.', 'Give a precise end goal and success criteria.'),
            ('Anthropic', 'Claude can think before it answers. Newer models decide how much, with an effort setting.', 'Define success criteria and test against them first.'),
            ('Google', 'Gemini thinking models reason on their own. You usually need not ask for steps.', 'Prompt design is iterative: change, retest.')]
    rh = (h - 0.65) / 3
    for i, (v, a, b) in enumerate(rows):
        y = h - 0.55 - (i + 1) * rh
        s.text(0.15, y + rh / 2, v, size=19, weight='bold', ha='left')
        _lt(s, c0, y + rh / 2, c1 - 0.3, a, 16)
        _lt(s, c0 + c1, y + rh / 2, c2 - 0.2, b, 16, color=BODY)
        s.line(0.05, y, w - 0.05, y, color=HAIR, lw=1)
    return s


# ----------------------------------------------------------------------------------------------- five parts to the template
@fig('x_t08_template')
def template(w, h, **_):
    s = Scene(w, h)
    lw_ = 3.2
    s.text(lw_ / 2, h - 0.25, 'Five-part checklist', size=18, weight='bold')
    left = ['Role', 'Context', 'Examples', 'Format', 'Checks']
    rh = (h - 0.7) / 5
    for i, t in enumerate(left):
        y = h - 0.55 - (i + 1) * rh
        s.box(0.05, y + 0.06, lw_, rh - 0.12, t, size=18, weight='bold', fill=GOLD, lw=1.8)
    s.arrow(lw_ + 0.15, h / 2 - 0.1, lw_ + 1.0, h / 2 - 0.1, lw=2.6, head=18)
    x0 = lw_ + 1.15
    s.text(x0 + (w - x0) / 2, h - 0.25, 'Reusable Brief Template: seven parts', size=18, weight='bold')
    right = ['1  Goal', '2  Context', '3  Inputs', '4  Constraints', '5  Output format', '6  How I will check', '7  What to say when unsure']
    rh2 = (h - 0.7) / 7
    for i, t in enumerate(right):
        y = h - 0.55 - (i + 1) * rh2
        new = i in (2, 3, 6)
        s.box(x0, y + 0.04, w - x0 - 0.05, rh2 - 0.08, t + ('   (adds to the checklist)' if new else ''), size=16, weight='bold' if new else 'normal', fill=PAPER, edge=RED if new else INK, lw=2.0 if new else 1.4)
    return s
