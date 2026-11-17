"""Figures for Session 8: prompting and reasoning models.

Kinds: brief, roles, briefs, fivepart, fewshot, delims, orderslip, structured, checkgrid, cot, promptlog, payroll, slip, reasoning, vendors, template, continues, tempformula.
Data drawn here is from recorded runs: Case Runs F1a and F1b (4 November 2026) and demo_runs/s08_prompting_runs.md (6 November 2026).
"""
import matplotlib
from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD, fig
import slidekit as K

matplotlib.rcParams.update({'mathtext.fontset': 'custom', 'mathtext.rm': 'Lato', 'mathtext.it': 'Lato:italic', 'mathtext.bf': 'Lato:bold'})


def _wrap(s, cx, cy, width, text, size, weight='normal', color=INK, ha='center'):
    lines = K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', width)
    x = cx if ha == 'center' else cx - width / 2
    return s.text(x if ha == 'center' else cx, cy, '\n'.join(lines), size=size, weight=weight, color=color, ha=ha)


def _lt(s, x, cy, width, text, size, weight='normal', color=INK):
    """Left aligned wrapped text with its vertical centre at cy."""
    lines = K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', width)
    return s.text(x, cy, '\n'.join(lines), size=size, weight=weight, color=color, ha='left')


# ----------------------------------------------------------------------------------------------- system prompt and user prompt
@fig('x_t08_roles')
def roles(w, h, **_):
    s = Scene(w, h)
    bw = 5.3
    bh = (h - 0.75) / 2
    items = [('System prompt', 'Standing instructions, set once', 'You are the customer-service assistant of Nile Valley Foods. Answer in English. Never promise a refund.', GOLD),
             ('User prompt', 'This request, typed each time', 'The oil jerrycans we received on Monday were leaking. What can you do?', PAPER)]
    for k, (hd, sub, ex, fill) in enumerate(items):
        y = h - 0.05 - bh - k * (bh + 0.15)
        s.box(0.05, y, bw, bh, '', fill=fill, edge=INK, lw=2.0, r=0.05)
        s.text(0.25, y + bh - 0.3, hd, size=19, weight='bold', ha='left')
        s.text(0.25, y + bh - 0.65, sub, size=14, color=BODY, ha='left')
        _lt(s, 0.25, y + 0.5, bw - 0.4, ex, 15, color=INK)
        s.arrow(0.05 + bw + 0.05, y + bh / 2, 0.05 + bw + 0.6, h / 2, lw=2.2, head=15)
    mx = 0.05 + bw + 0.7
    s.box(mx, h / 2 - 0.6, 1.9, 1.2, 'Language\nmodel', size=18, weight='bold', fill=PAPER, lw=2.2)
    s.arrow(mx + 1.95, h / 2, mx + 2.5, h / 2, lw=2.2, head=15)
    s.box(mx + 2.55, h / 2 - 0.6, w - mx - 2.6, 1.2, 'Reply', size=18, weight='bold', fill=PAPER, lw=2.2)
    s.text(0.05, 0.25, 'Analogy: house rules given to a waiter at the start of a shift, then a customer\'s order.', size=14, color=BODY, ha='left')
    return s


# ----------------------------------------------------------------------------------------------- weak vs strong brief
@fig('x_t08_briefs')
def briefs(w, h, **_):
    s = Scene(w, h)
    gap = 0.2
    pw = (w - gap - 0.1) / 2
    cols = [('Weak prompt', '"Write the Monday sales email." and the data', [('check', 'Figures right'), ('cross', 'Own layout'), ('cross', 'Advice nobody asked for'), ('cross', '"[Your name]" left in')]),
            ('Strong prompt', 'Role, reader, format, constraints, "do not invent"', [('check', 'Figures right'), ('check', 'Format followed'), ('check', 'Said the cause is unknown'), ('check', 'One thing to check')])]
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
            ('Examples', 'None in this prompt. Add one finished email when the format matters.', True),
            ('Format', 'A subject line, a two-sentence summary, a short table, at most three plain sentences.', False),
            ('Constraints', 'Use only the figures below. Do not invent any number, cause or customer. If something cannot be explained, say so.', False)]
    rh = (h - 0.1) / 5
    for i, (a, b, missing) in enumerate(rows):
        y = h - 0.05 - (i + 1) * rh
        s.box(0.05, y + 0.06, 1.9, rh - 0.12, a, size=19, weight='bold', fill=PAPER if missing else PALE, edge=RED if missing else INK, lw=2.0, dash=missing)
        s.box(2.05, y + 0.06, w - 2.1, rh - 0.12, '', fill=PAPER, edge=RED if missing else INK, lw=1.4, dash=missing)
        _lt(s, 2.25, y + rh / 2, w - 2.5, b, 17, color=RED if missing else INK)
    return s


# ----------------------------------------------------------------------------------------------- delimiters
@fig('x_t08_delims')
def delims(w, h, **_):
    s = Scene(w, h)
    s.box(0.05, h - 1.4, w - 0.1, 1.3, '', fill=GOLD, lw=2.0)
    s.text(0.25, h - 0.35, 'Instructions (the cover sheet)', size=16, weight='bold', ha='left')
    _lt(s, 0.25, h - 0.95, w - 0.5, 'Label each SMS below as money in or money out. Return a table.', 17)
    s.text(0.25, h - 1.7, '### SMS START', size=16, weight='bold', ha='left', mono=True)
    s.box(0.05, 1.15, w - 0.1, h - 3.0, '', fill=PALE, edge=INK, lw=1.6)
    s.text(0.25, h - 2.15, 'Data (the folder)', size=16, weight='bold', ha='left')
    s.text(0.25, h - 2.6, '1. You have received UGX 20,000 from Mary.', size=15, ha='left', color=BODY)
    s.text(0.25, h - 2.95, '2. You have sent UGX 50,000 to Peter.', size=15, ha='left', color=BODY)
    s.text(0.25, 0.9, '### SMS END', size=16, weight='bold', ha='left', mono=True)
    s.tag(0.1, 0.3, 'Prompt injection: an order hidden in the data can be followed', size=15, fill=RED)
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
    s.text(0.05, yb - 0.75, 'A person found the two loose fields: my field list allowed one text for two facts.', size=17, ha='left', color=BODY)
    return s


# ----------------------------------------------------------------------------------------------- chain-of-thought (illustration)
@fig('x_t08_cot')
def cot(w, h, **_):
    s = Scene(w, h)
    s.text(0.05, h - 0.25, '"3 kg of sugar at UGX 4,500 and 2 kg of rice at UGX 5,000. What is the total?"', size=17, weight='bold', ha='left')
    gap = 0.3
    pw = (w - 0.1 - gap) / 2
    panels = [('Answer only', ['UGX 23,500'], False), ('Chain-of-thought: show the steps', ['3 x 4,500 = 13,500', '2 x 5,000 = 10,000', '13,500 + 10,000 = 23,500'], True)]
    top = h - 0.65
    ph = top - 0.75
    for i, (hd, lines, good) in enumerate(panels):
        x0 = 0.05 + i * (pw + gap)
        s.box(x0, 0.75, pw, ph, '', fill=GOLD if good else PAPER, edge=INK, lw=2.0, r=0.05)
        s.text(x0 + 0.25, top - 0.35, hd, size=18, weight='bold', ha='left')
        for k, ln in enumerate(lines):
            s.text(x0 + 0.35, top - 1.0 - k * 0.5, ln, size=19, weight='bold' if k == len(lines) - 1 else 'normal', ha='left')
    s.text(0.05, 0.35, 'You can check each line. A wrong step shows up where it happens.', size=16, weight='bold', ha='left')
    s.text(w - 0.05, 0.35, 'Illustration only, no recorded run', size=14, color=MUTE, ha='right')
    return s


# ----------------------------------------------------------------------------------------------- test loop and prompt log
@fig('x_t08_promptlog')
def promptlog(w, h, **_):
    s = Scene(w, h)
    steps = ['Write the prompt', 'Run on evaluation set', 'Score against the key', 'Change one thing']
    n = 4
    gap = 0.45
    bw = (w - 0.1 - gap * 3) / n
    for i, t in enumerate(steps):
        x = 0.05 + i * (bw + gap)
        s.box(x, h - 0.85, bw, 0.75, t, size=16, weight='bold', fill=GOLD if i == 2 else PAPER, lw=1.8)
        if i < n - 1:
            s.arrow(x + bw + 0.04, h - 0.475, x + bw + gap - 0.04, h - 0.475, lw=2.2, head=15)
    rows = [['Version', 'What changed', 'Runs', 'Right (accuracy)', 'Next change'],
            ['Payroll plain', 'One plain paragraph', '2', '1 of 2 = 50%', 'Add the re-add line'],
            ['Payroll framed', 'Goal, rules, output, re-add', '2', '2 of 2 = 100%', 'Split framing from re-add'],
            ['Orders v1', 'JSON with fixed fields', '1', 'Valid JSON', 'Split the reference field']]
    cwid = [1.6, 3.4, 0.9, 2.3, 3.5]
    sc = (w - 0.1) / sum(cwid)
    cwid = [c * sc for c in cwid]
    s.table(0.05, h - 1.15, cwid, 0.62, rows, size=15, align=['left', 'left', 'center', 'center', 'left'], hl_cells={(2, 3): GOLD, (1, 3): PAPER})
    return s


# ----------------------------------------------------------------------------------------------- payroll runs
@fig('x_t08_payroll')
def payroll(w, h, **_):
    s = Scene(w, h)
    c0 = 4.9
    rc = 2.3
    cw = (w - c0 - rc - 0.05) / 3
    s.text(0.1, h - 0.3, 'Prompt variant', size=16, weight='bold', ha='left')
    for j in range(3):
        s.text(c0 + j * cw + cw / 2, h - 0.3, 'Run %d' % (j + 1), size=16, weight='bold')
    s.text(w - rc / 2, h - 0.3, 'Right (accuracy)', size=16, weight='bold')
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
            s.box(cx - cw / 2 + 0.08, y + 0.1, cw - 0.16, rh - 0.2, v, size=16, weight='bold', fill=PAPER, edge=INK if ok else RED, lw=2.0 if ok else 2.6)
        good = sum(v == key for v in vals)
        s.text(w - rc / 2, y + rh / 2, '%d of %d = %d%%' % (good, len(vals), round(100 * good / len(vals))), size=17, weight='bold')
        s.line(0.05, y, w - 0.05, y, color=HAIR, lw=1)
    s.text(0.1, 0.98, 'Accuracy = correct ÷ total.  All ten runs: 9 ÷ 10 = 90%.', size=16, ha='left', weight='bold', color=RED)
    s.text(0.1, 0.62, 'Boxes show net pay (UGX). Key, worked out separately: 1,802,898. Total cost key: 2,261,250.', size=14, ha='left', weight='bold')
    s.text(0.1, 0.26, 'Red border = wrong; the others match the key. 10 runs, Claude fresh subagents, 6 November 2026.', size=14, ha='left', color=BODY)
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
    specs = [('Standard model', 'answers straight away', False), ('Reasoning model', 'writes working, then answers', True)]
    for i, (name, sub, think) in enumerate(specs):
        y = h - 0.1 - (i + 1) * lane_h - i * 0.25
        s.text(0.05, y + lane_h - 0.3, name, size=21, weight='bold', ha='left')
        s.text(0.05, y + lane_h - 0.7, sub, size=16, color=BODY, ha='left')
        s.box(3.6, y + 0.4, 1.6, 0.9, 'Your prompt', size=16, weight='bold')
        if think:
            s.arrow(5.25, y + 0.85, 5.85, y + 0.85, lw=2.2, head=15)
            s.box(5.9, y + 0.3, 3.0, 1.1, 'Writes working\ntokens first', size=16, weight='bold', fill=GOLD, lw=2.0, dash=True)
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
    left = ['Role', 'Context', 'Examples', 'Format', 'Constraints']
    rh = (h - 0.7) / 5
    for i, t in enumerate(left):
        y = h - 0.55 - (i + 1) * rh
        s.box(0.05, y + 0.06, lw_, rh - 0.12, t, size=18, weight='bold', fill=PALE, lw=1.8)
    s.arrow(lw_ + 0.15, h / 2 - 0.1, lw_ + 1.0, h / 2 - 0.1, lw=2.6, head=18)
    x0 = lw_ + 1.15
    s.text(x0 + (w - x0) / 2, h - 0.25, 'Reusable prompt template: seven parts', size=18, weight='bold')
    right = ['1  Goal', '2  Context', '3  Inputs', '4  Constraints', '5  Output format', '6  How I will check', '7  What to say when unsure']
    rh2 = (h - 0.7) / 7
    for i, t in enumerate(right):
        y = h - 0.55 - (i + 1) * rh2
        new = i in (2, 5, 6)
        s.box(x0, y + 0.04, w - x0 - 0.05, rh2 - 0.08, t + ('   (adds to the checklist)' if new else ''), size=16, weight='bold' if new else 'normal', fill=PAPER, edge=RED if new else INK, lw=2.0 if new else 1.4)
    return s


# ----------------------------------------------------------------------------------------------- the model continues your text (recall of Session 5)
@fig('x_t08_continues')
def continues(w, h, **_):
    """Two real next-word lists from the Session 5 run (GPT-2 small, demo_runs/s05/results.json): a loose start and a tight start."""
    import json
    from pathlib import Path
    R = json.loads((Path(__file__).resolve().parent.parent / 'demo_runs' / 's05' / 'results.json').read_text())
    s = Scene(w, h)
    pw = (w - 0.3) / 2
    panels = [(0, 'The capital of\nUganda is ...', 'Loose start: many tokens fit', 'Top ten tokens hold only 42%'),
              (1, 'Please pay the invoice\nwithin thirty ...', 'Tight start: few tokens fit', 'Top three tokens hold 97%')]
    taxi = ['Like telling a taxi driver: "Take me to town"', 'Like: "Take me to Garden City, main entrance"']
    for k, (idx, ttl, tag, foot) in enumerate(panels):
        x0 = 0.05 + k * (pw + 0.2)
        s.box(x0, h - 1.0, pw, 0.9, '', fill=PAPER, edge=INK, lw=1.8, r=0.06)
        s.text(x0 + pw / 2, h - 0.55, ttl, size=17, weight='bold')
        _wrap(s, x0 + pw / 2, h - 1.45, pw - 0.2, taxi[k], 14, color=BODY)
        rows = R['next'][idx]['top10'][:3]
        top = h - 1.9
        rh = (top - 1.1) / 3
        mx = 0.75
        for i, (wd, p) in enumerate(rows):
            yc = top - rh * (i + 0.5)
            s.text(x0 + 1.5, yc, wd.strip() or '(space)', size=17, ha='right')
            bw = (pw - 3.0) * p / mx
            s.rect(x0 + 1.65, yc - rh * 0.3, max(bw, 0.03), rh * 0.6, fill=GOLD if i == 0 else GREY, edge=INK, lw=1.0)
            s.text(x0 + 1.8 + bw, yc, '%.0f%%' % (100 * p), size=16, ha='left')
        s.text(x0 + pw / 2, 0.7, tag, size=17, weight='bold', color=RED)
        s.text(x0 + pw / 2, 0.3, foot, size=15, color=BODY)
    return s




# ----------------------------------------------------------------------------------------------- recall: the next-token loop (real Session 5 run)
@fig('x_t08_loop')
def loop(w, h, **_):
    """'Thank you for your' from demo_runs/s05/keyboard_run_thank_you.txt (GPT-2 small, 7 November 2026)."""
    s = Scene(w, h)
    s.box(0.05, h - 0.95, w - 0.1, 0.8, '', fill=PAPER, lw=1.8)
    s.text(0.25, h - 0.55, 'Text so far:', size=16, color=BODY, ha='left')
    s.text(1.75, h - 0.55, '"Thank you for your"', size=19, weight='bold', ha='left')
    s.text(0.05, h - 1.3, 'The model gives every token a probability', size=16, weight='bold', ha='left')
    rows = [(' support', 30.4), (' continued', 10.3), (' patience', 5.4)]
    top = h - 1.6
    for i, (tk, p) in enumerate(rows):
        yc = top - 0.3 - i * 0.52
        s.text(1.85, yc, tk.strip(), size=17, ha='right', weight='bold' if i == 0 else 'normal')
        L = 3.2 * p / 32
        s.rect(1.95, yc - 0.17, L, 0.34, fill=GOLD if i == 0 else GREY, edge=INK, lw=1.0)
        s.text(2.05 + L, yc, f'{p:.1f}%', size=16, ha='left')
    s.text(1.95, top - 1.95, '... and 50,254 more tokens share the rest', size=15, color=BODY, ha='left')
    s.box(0.05, 0.1, w - 0.1, 0.8, '', fill=GOLD, lw=1.8)
    s.text(0.25, 0.5, 'One token is picked and added:', size=16, ha='left')
    s.text(3.6, 0.5, '"Thank you for your support"', size=18, weight='bold', ha='left')
    s.arrow(w - 0.45, 0.95, w - 0.45, h - 1.0, lw=2.4, head=16, rad=0.0)
    s.text(w - 0.75, h / 2 - 0.2, 'repeat', size=16, weight='bold', color=RED, rot=90)
    return s


# ----------------------------------------------------------------------------------------------- temperature recalled: worked numbers first, then the formula
@fig('x_t08_tempformula')
def tempformula(w, h, **_):
    import math
    s = Scene(w, h)
    logits = [('days', 3), ('weeks', 2), ('minutes', 0)]
    pw = (w - 0.3) / 2
    ph = 2.55
    for k, T in enumerate((1, 2)):
        x0 = 0.05 + k * (pw + 0.2)
        ez = [math.exp(z / T) for _, z in logits]
        tot = sum(ez)
        y0 = h - 0.05 - ph
        s.box(x0, y0, pw, ph, '', fill=PAPER, edge=INK, lw=1.8, r=0.06)
        s.text(x0 + 0.2, y0 + ph - 0.32, 'T = 1: logits as they are' if T == 1 else 'T = 2: halve the logits first', size=17, weight='bold', ha='left', color=INK if T == 1 else RED)
        for i, ((nm, z), e) in enumerate(zip(logits, ez)):
            yc = y0 + ph - 0.85 - 0.45 * i
            s.text(x0 + 1.25, yc, nm, size=16, ha='right')
            s.text(x0 + 1.35, yc, f'z = {z}:  e^({z}÷{T}) = {e:.2f}', size=15, color=BODY, ha='left')
            p = e / tot
            s.rect(x0 + 3.75, yc - 0.14, max(1.3 * p / 0.75, 0.03), 0.28, fill=GOLD if i == 0 else GREY, edge=INK, lw=1.0)
            s.text(x0 + 3.85 + 1.3 * p / 0.75, yc, f'{100 * p:.1f}%', size=15, ha='left', weight='bold' if i == 0 else 'normal')
        s.text(x0 + 0.2, y0 + 0.28, f'Add: total {tot:.2f}. Divide each by the total.', size=15, color=BODY, ha='left')
    s.text(0.3, 0.7, r'$p_i = \dfrac{e^{z_i / T}}{\sum_j e^{z_j / T}}$', size=24, ha='left')
    lab = ['pᵢ: probability of token i (i counts the tokens)', 'zᵢ: its logit, the raw score;  T: the temperature',
           'e ≈ 2.72;  Σ: add up, one term for each token j']
    for i, tx in enumerate(lab):
        s.text(4.0, 1.12 - 0.37 * i, tx, size=15, ha='left', color=INK)
    return s


# ----------------------------------------------------------------------------------------------- the five parts, each removing a guess (recipe request)
@fig('x_t08_brief')
def brief(w, h, **_):
    s = Scene(w, h)
    rows = [('Role', 'Guess: which voice and level?', 'You are a home cook'),
            ('Context', 'Guess: what is my situation?', 'Four people, one vegetarian'),
            ('Examples', 'Guess: which labels and layout?', 'Like the bean stew last week'),
            ('Format', 'Guess: how long, what shape?', 'Ingredients, then numbered steps'),
            ('Constraints', 'Guess: what is off limits?', 'Under UGX 30,000; say if unsure')]
    rh = (h - 0.1) / 5
    for i, (a, g, ex) in enumerate(rows):
        y = h - 0.05 - (i + 1) * rh
        s.box(0.05, y + 0.06, 1.75, rh - 0.12, a, size=17, weight='bold', fill=PALE, lw=1.8)
        s.box(1.9, y + 0.06, w - 1.95, rh - 0.12, '', fill=PAPER, lw=1.4)
        s.text(2.05, y + rh / 2 + 0.17, g, size=15, color=RED, weight='bold', ha='left')
        s.text(2.05, y + rh / 2 - 0.19, ex, size=16, ha='left')
    return s


# ----------------------------------------------------------------------------------------------- before and after, one technique at a time (recorded runs of 11 November 2026)
def _ba(s, w, h, cols):
    """cols: two tuples (head, prompt, reply_lines or callable, verdict, good)."""
    gap = 0.25
    pw = (w - 0.1 - gap) / 2
    for i, (head, prompt, reply, verdict, good) in enumerate(cols):
        x0 = 0.05 + i * (pw + gap)
        s.text(x0, h - 0.22, head, size=18, weight='bold', ha='left', color=INK if i == 0 else RED)
        s.box(x0, h - 1.42, pw, 0.95, '', fill=PALE if i == 0 else GOLD, lw=1.6)
        _lt(s, x0 + 0.12, h - 0.945, pw - 0.24, prompt, 15)
        s.arrow(x0 + pw / 2, h - 1.47, x0 + pw / 2, h - 1.75, lw=2.0, head=13)
        s.box(x0, 0.5, pw, h - 2.3, '', fill=PAPER, lw=1.6)
        s.text(x0 + 0.12, h - 1.98, 'Recorded reply', size=14, color=MUTE, ha='left')
        if callable(reply):
            reply(x0, pw)
        else:
            _lt(s, x0 + 0.12, 0.5 + (h - 2.3) / 2 - 0.12, pw - 0.24, reply, 15)
        s.text(x0, 0.27, verdict, size=15, weight='bold', ha='left', color=INK if good else RED)


@fig('x_t08_ba_role')
def ba_role(w, h, **_):
    s = Scene(w, h)
    _ba(s, w, h, [('Before: no role', '"Explain what inflation is. Answer in at most 60 words."',
                   '"...the general rise in prices across an economy over time... measured yearly with a price index such as the Consumer Price Index... rapid growth in the money supply."',
                   'Right, in an economist’s words', False),
                  ('After: add a role', 'Adds: "You are a primary school teacher talking to a class of ten-year-olds."',
                   '"Imagine a chocolate bar costs 1,000 shillings today. Next year, the same bar costs 1,200 shillings... That’s inflation!"',
                   'Same idea, at the level of the audience', True)])
    return s


@fig('x_t08_ba_context')
def ba_context(w, h, **_):
    s = Scene(w, h)
    _ba(s, w, h, [('Before: no context', '"Suggest a dinner I can cook tonight. Answer in at most 60 words."',
                   '"Try a lemon-garlic chicken stir-fry... bell peppers, broccoli and snap peas... soy sauce, honey..."',
                   'Chicken for a vegetarian; food you may not have', False),
                  ('After: add the context', 'Adds: four people, one vegetarian; beans, rice, tomatoes and onions at home; 45 minutes.',
                   '"Make a vegetarian bean and tomato stew over rice... Start the rice first... simmer for 15 minutes." It also added cumin, paprika and an egg.',
                   'Fits. The extras call for a constraint', True)])
    return s


@fig('x_t08_ba_constraints')
def ba_constraints(w, h, **_):
    s = Scene(w, h)
    _ba(s, w, h, [('Before: context, no constraints', 'Four people, one vegetarian; beans, rice, tomatoes and onions at home; 45 minutes.',
                   '"Make a vegetarian bean and tomato stew... add diced tomatoes, garlic, cumin, paprika and salt... with a fried egg on top..."',
                   'Fits, but adds four things not at home', False),
                  ('After: add the constraints', 'Adds: "Use only the ingredients I listed, plus salt, oil and water. If a good dish needs anything else, say so."',
                   '"Fry the onions in oil, add chopped tomatoes and salt... 45 minutes only if the beans are canned or precooked. Garlic, chili or cumin would improve it, but you didn\'t list them."',
                   'Kept to the list, and said what it lacked', True)])
    return s


@fig('x_t08_ba_fewshot')
def ba_fewshot(w, h, **_):
    s = Scene(w, h)
    _ba(s, w, h, [('Before: zero-shot (no examples)', 'Label each mobile money SMS: 1. received 8,000 from John; 2. paid 35,000 to Kampala Water; 3. received 120,000 from Grace.',
                   '1. Money In (Received)... 2. Money Out (Bill Payment)... 3. Money In (Received)... "Totals: UGX 128,000 in and UGX 35,000 out." 73 words.',
                   'Right, but its own labels, plus totals', False),
                  ('After: few-shot (two examples first)', 'Adds two shots: "received UGX 20,000 from Mary" Label: IN; "sent UGX 50,000 to Peter" Label: OUT.',
                   '1. IN\n2. OUT\n3. IN',
                   'The exact labels and layout of the shots', True)])
    return s


@fig('x_t08_ba_format')
def ba_format(w, h, **_):
    s = Scene(w, h)

    def table(x0, pw):
        rows = [['', 'Renting', 'Buying'], ['Monthly cost', 'Rent, often lower...', 'Mortgage, taxes...'],
                ['Flexibility', 'Easy to move', 'Selling takes time'], ['Risk', 'Rent increases', 'Market drops...']]
        cw = [1.45, (pw - 1.65) / 2, (pw - 1.65) / 2]
        s.table(x0 + 0.1, h - 2.15, cw, 0.36, rows, size=14, align=['left', 'left', 'left'])
    _ba(s, w, h, [('Before: no format', '"Compare renting and buying a house."',
                   '529 words: seven headings (upfront costs, monthly costs, wealth building...), rules of thumb, and advice to see a financial adviser.',
                   'Useful, too long to compare at a glance', False),
                  ('After: state the format', 'Adds: "Answer only with a table: columns Renting, Buying; rows Monthly cost, Flexibility, Risk; at most eight words a cell."',
                   table, 'The shape asked for: 3 rows, 2 columns', True)])
    return s


@fig('x_t08_ba_json')
def ba_json(w, h, **_):
    s = Scene(w, h)

    def code(x0, pw):
        s.code(x0 + 0.12, h - 2.13, ['{"table": 4,', ' "items": [', '   {"dish": "chapati", "quantity": 2},', '   {"dish": "tea", "quantity": 1}],', ' "note": "no sugar"}'],
               size=14, line_h=0.255, w=pw - 0.24)
    _ba(s, w, h, [('Before: free text', '"Two chapati and a tea for table 4, no sugar please." Write down this order for the kitchen.',
                   'KITCHEN ORDER - TABLE 4\n- 2 x Chapati\n- 1 x Tea (NO SUGAR)',
                   'Fine for a cook; a program cannot rely on it', False),
                  ('After: ask for JSON', 'Adds: "Return JSON only, fields table (a number), items (dish, quantity), note (text, or null)."',
                   code, 'Fixed fields: a program can read them', True)])
    return s


# ----------------------------------------------------------------------------------------------- JSON taken apart (the restaurant order)
@fig('x_t08_jsonparts')
def jsonparts(w, h, **_):
    s = Scene(w, h)
    lines = ['{', '  "table": 4,', '  "items": [', '    {"dish": "chapati", "quantity": 2},', '    {"dish": "tea", "quantity": 1}', '  ],', '  "note": "no sugar"', '}']
    cw, ch = s.code(0.05, h - 0.1, lines, size=16, line_h=0.42, w=5.6)
    notes = [(0, '{ } holds one record: a set of named fields'),
             (1, '"table": 4  a field name in quotes, a colon, its value'),
             (2, '[ ] holds a list: here, two items'),
             (3, 'each item is a small record of its own'),
             (6, 'a text value sits in quotes; null would mean empty')]
    for li, tx in notes:
        y = h - 0.1 - 0.15 - (li + 0.5) * 0.42
        s.line(5.75, y, 6.15, y, color=RED, lw=2)
        s.text(6.25, y, tx, size=15, ha='left', weight='bold' if li in (0, 1) else 'normal')
    s.text(0.05, 0.25, 'JSON, JavaScript Object Notation: plain text that any program can read field by field.', size=15, ha='left', color=BODY)
    return s


# ----------------------------------------------------------------------------------------------- evaluation set and accuracy (everyday: checking a new cashier)
@fig('x_t08_evalset')
def evalset(w, h, **_):
    s = Scene(w, h)
    s.text(0.05, h - 0.25, 'A new cashier adds up 10 bills whose totals you already know', size=17, weight='bold', ha='left')
    bw = (w - 0.1 - 9 * 0.12) / 10
    for i in range(10):
        x = 0.05 + i * (bw + 0.12)
        bad = i == 6
        s.box(x, h - 1.75, bw, 1.05, '', fill=PAPER if bad else PALE, edge=RED if bad else INK, lw=2.4 if bad else 1.6)
        s.text(x + bw / 2, h - 0.95, f'Bill {i + 1}', size=14, color=BODY)
        s.icon('cross' if bad else 'check', x + bw / 2, h - 1.4, 0.4)
    s.text(0.05 + 6 * (bw + 0.12) + bw / 2, h - 2.05, 'wrote 23,000; key 23,500', size=14, color=RED, weight='bold')
    s.text(0.05, h - 2.55, 'Count:  correct = 9,  total = 10', size=17, ha='left')
    s.text(0.05, h - 3.0, 'Accuracy = correct ÷ total = 9 ÷ 10 = 0.9 = 90%', size=19, weight='bold', ha='left', color=RED)
    s.text(0.05, 0.62, 'Evaluation set: the 10 bills with their known totals (the key).', size=15, ha='left')
    s.text(0.05, 0.25, 'Small sets: 1 of 2 = 50%, 3 of 3 = 100%. One bill more or less changes them a lot.', size=15, ha='left', color=BODY)
    return s
