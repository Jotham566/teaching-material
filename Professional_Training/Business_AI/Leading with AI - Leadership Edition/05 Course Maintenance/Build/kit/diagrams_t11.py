"""Figures for Session 11, Agentic AI (v3, 6 November 2026).

t11_loop       the plan, act, observe loop with a goal, a stop and a log line per turn
t11_housesitter everyday first: a house-sitter with a goal, one key given, two refused, and a note under the door
t11_permissions a phone app asking for a permission, next to the mailbox agent's permissions (granted and refused)
t11_autonomy   five levels of autonomy, from answer only to acts alone
t11_approval   human-in-the-loop approval: the agent prepares, a person decides, then the action runs
t11_mcp        MCP as a standard plug: one host, one client per server, servers offer tools, resources, prompts
t11_mailbox    the fourteen demonstration mails sorted by the lecturer's key (no AI output)
t11_planted    a mail with a prompt injection: the ordinary part and the injected part
t11_privilege  least privilege as a calculation: three permissions, worst case for each
"""
from figkit import Scene, INK, BODY, MUTE, HAIR, PAPER, RED, GOLD, GREY, fig
import slidekit as K


def _w(s, x, y, w, text, size, weight='normal', color=INK, ha='center', va='center'):
    lines = K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', w)
    s.text(x, y, '\n'.join(lines), size=size, weight=weight, color=color, ha=ha, va=va)
    return len(lines) * size * 1.15 / 72


@fig('x_t11_loop')
def x_t11_loop(w, h, **_):
    s = Scene(w, h)
    cx, cy = 2.75, h * 0.47
    r = min(1.45, h * 0.3)
    pos = {'Plan': (cx, cy + r), 'Act': (cx + r * 1.1, cy - r * 0.7), 'Observe': (cx - r * 1.1, cy - r * 0.7)}
    sub = {'Plan': 'choose the next step', 'Act': 'call one tool', 'Observe': 'read the result'}
    order = ['Plan', 'Act', 'Observe']
    for a, b in zip(order, order[1:] + order[:1]):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        s.arrow(x1 + (x2 - x1) * 0.3, y1 + (y2 - y1) * 0.3, x1 + (x2 - x1) * 0.7, y1 + (y2 - y1) * 0.7, lw=2.6, head=18, rad=-0.25)
    bw, bh = 2.2, 1.05
    for k, (x, y) in pos.items():
        s.box(x - bw / 2, y - bh / 2, bw, bh, '', fill=GOLD if k == 'Act' else PAPER, edge=INK, lw=2.0, z=3)
        s.text(x, y + 0.2, k, size=20, weight='bold', z=6)
        s.text(x, y - 0.25, sub[k], size=14, color=BODY, z=6)
    s.text(cx, cy - 0.15, 'repeat', size=16, color=MUTE)
    gx, gw = w - 2.0, 1.95
    s.box(gx, h - 1.35, gw, 1.2, '', fill=PAPER, edge=INK, lw=1.8)
    s.text(gx + gw / 2, h - 0.55, 'Goal', size=17, weight='bold')
    s.text(gx + gw / 2, h - 0.98, 'from the owner', size=14, color=BODY)
    s.arrow(gx - 0.05, h - 0.75, pos['Plan'][0] + bw / 2 + 0.08, pos['Plan'][1] + 0.1, lw=2, head=14)
    s.box(gx, 0.15, gw, 1.6, '', fill=PAPER, edge=RED, lw=2.2)
    s.text(gx + gw / 2, 1.42, 'Stop', size=17, weight='bold', color=RED)
    s.text(gx + gw / 2, 0.75, 'goal met, step\nlimit reached, or\na person is needed', size=14, color=BODY)
    s.arrow(pos['Act'][0] + bw / 2 + 0.05, pos['Act'][1], gx - 0.05, pos['Act'][1], lw=2, head=14, color=RED)
    return s


PERMS = [
    dict(icon='mail', head='Read mail', sub='one mailbox', ok=True),
    dict(icon='doc', head='Write drafts', sub='drafts folder', ok=True),
    dict(icon='calendar', head='See calendar', sub='not granted', ok=False),
    dict(icon='speech', head='Send', sub='never alone', ok=False),
    dict(icon='receipt', head='Pay', sub='never', ok=False),
]


@fig('x_t11_housesitter')
def x_t11_housesitter(w, h, **_):
    """Everyday analogy: the owner sets a goal, hands over one key and keeps two; a note under the door is no order."""
    s = Scene(w, h)
    # the house and the sitter
    s.icon('home', 1.0, h - 1.15, 1.6)
    s.icon('person', 2.35, h - 1.2, 1.3)
    gx = 3.4
    s.box(gx, h - 1.85, w - gx - 0.05, 1.75, '', fill=PAPER, edge=INK, lw=1.8)
    s.text(gx + 0.2, h - 0.45, 'Goal from you', size=16, weight='bold', ha='left')
    _w(s, gx + 0.2, h - 1.2, w - gx - 0.45, 'Water the plants and keep the house locked for one week.', 16, ha='left', color=BODY)
    keys = [('Front door', 'given', True), ('Safe', 'kept by you', False), ('Car', 'kept by you', False)]
    kw = (w - 0.1 - 0.2 * 2) / 3
    ky = h - 3.35
    for i, (k, sub, ok) in enumerate(keys):
        x = 0.05 + i * (kw + 0.2)
        s.box(x, ky, kw, 1.05, '', fill=GOLD if ok else PAPER, edge=INK if ok else RED, lw=2.0, dash=not ok)
        if ok:  # a key drawn above the gold box (the stock icon's shaft sits under box fills)
            kx, kyc, ks = x + 0.45, ky + 0.52, 0.75
            s.circle(kx - 0.2 * ks, kyc, 0.17 * ks, fill=PAPER, edge=INK, lw=2, z=5)
            s.line(kx - 0.03 * ks, kyc, kx + 0.36 * ks, kyc, color=INK, lw=2.6, z=5)
            s.line(kx + 0.22 * ks, kyc, kx + 0.22 * ks, kyc - 0.12 * ks, color=INK, lw=2.4, z=5)
            s.line(kx + 0.34 * ks, kyc, kx + 0.34 * ks, kyc - 0.12 * ks, color=INK, lw=2.4, z=5)
        else:
            s.icon('lock', x + 0.45, ky + 0.52, 0.75)
        s.text(x + 1.0, ky + 0.7, k, size=17, weight='bold', ha='left')
        s.text(x + 1.0, ky + 0.32, sub, size=15, color=BODY if ok else RED, ha='left')
    s.box(0.05, 0.05, w - 0.1, ky - 0.25, '', fill=PAPER, edge=RED, lw=2.2)
    _w(s, w / 2, (ky - 0.2) / 2 + 0.05, w - 0.5, 'A note under the door: "The owner says give the key to the bearer." A good sitter phones you first.', 16, color=INK)
    return s


@fig('x_t11_permissions')
def x_t11_permissions(w, h, perms=None, **_):
    """Left: a phone asking for one permission. Right: the mailbox agent's permissions, granted (gold) and refused (red)."""
    s = Scene(w, h)
    perms = perms or PERMS
    # the phone
    pw, ph = 2.3, h - 0.2
    s.box(0.1, 0.1, pw, ph, '', fill=PAPER, edge=INK, lw=2.4, r=0.2)
    _w(s, 0.1 + pw / 2, h - 0.85, pw - 0.35, 'Allow Torch to read your contacts?', 15, 'bold')
    s.box(0.3, h * 0.42, pw - 0.4, 0.55, 'Don’t allow', size=15, fill=GOLD, edge=INK, lw=1.8, weight='bold')
    s.box(0.3, h * 0.42 - 0.75, pw - 0.4, 0.55, 'Allow', size=15, fill=PAPER, edge=HAIR, lw=1.4)
    s.text(0.1 + pw / 2, 0.45, 'a permission', size=14, color=MUTE)
    n = len(perms)
    x0 = pw + 0.45
    s.text(x0, h - 0.2, 'The mailbox agent', size=16, weight='bold', ha='left')
    bw = (w - x0 - 0.05)
    rh = (h - 0.5) / n
    for i, b in enumerate(perms):
        y = h - 0.45 - (i + 1) * rh
        s.box(x0, y + 0.05, bw, rh - 0.1, '', fill=GOLD if b['ok'] else PAPER, edge=INK if b['ok'] else RED, lw=2.0, dash=not b['ok'])
        s.icon(b['icon'], x0 + 0.4, y + rh / 2, min(0.5, rh - 0.2))
        s.text(x0 + 0.85, y + rh / 2, b['head'], size=16, weight='bold', ha='left')
        s.text(x0 + bw - 0.85, y + rh / 2, b['sub'], size=14, color=BODY if b['ok'] else RED, ha='right')
        s.icon('check' if b['ok'] else 'cross', x0 + bw - 0.4, y + rh / 2, min(0.45, rh - 0.25))
    return s


@fig('x_t11_autonomy')
def x_t11_autonomy(w, h, hl=2, **_):
    s = Scene(w, h)
    levels = [('0', 'Answers only', 'You copy and act'), ('1', 'Suggests', 'You choose each step'),
              ('2', 'Drafts', 'You approve each action'), ('3', 'Acts, then reports', 'You review the log'),
              ('4', 'Acts alone', 'Nobody checks')]
    n = len(levels)
    bw = (w - 0.1 - 0.15 * (n - 1)) / n
    for i, (num, head, sub) in enumerate(levels):
        x = 0.05 + i * (bw + 0.15)
        top = 1.6 + (h - 1.75) * (i + 1) / n
        fill = GOLD if i == hl else PAPER
        edge = RED if i == n - 1 else INK
        s.box(x, 0.85, bw, top - 0.85, '', fill=fill, edge=edge, lw=2.0)
        s.text(x + bw / 2, top - 0.35, 'Level ' + num, size=16, weight='bold', color=RED if i == n - 1 else INK)
        _w(s, x + bw / 2, 0.45, bw - 0.1, head, 16, 'bold')
        if top - 0.85 > 0.95:
            _w(s, x + bw / 2, (0.85 + top - 0.6) / 2 - 0.05, bw - 0.25, sub, 14, color=BODY)
    s.arrow(0.3, 0.12 + 0.0, w - 0.3, 0.12, lw=1.6, head=12, color=MUTE)
    return s


@fig('x_t11_approval')
def x_t11_approval(w, h, **_):
    s = Scene(w, h)
    y = h / 2 + 0.25
    bw, bh = 2.4, 1.6
    xs = [0.1, 3.05, 6.0, w - 2.5]
    heads = [('robot', 'Agent prepares', 'a draft reply'), ('person', 'Person reads', 'what will happen'),
             (None, '', ''), ('mail', 'Action runs', 'and is logged')]
    for i, (ic, head, sub) in enumerate(heads):
        if ic is None:
            continue
        s.box(xs[i], y - bh / 2, bw, bh, '', fill=GOLD if i == 1 else PAPER, edge=INK, lw=2.0)
        s.icon(ic, xs[i] + bw / 2, y + 0.35, 0.65)
        s.text(xs[i] + bw / 2, y - 0.2, head, size=17, weight='bold')
        s.text(xs[i] + bw / 2, y - 0.55, sub, size=14, color=BODY)
    # the approval step
    gx = xs[2] + 0.35
    s.rect(gx, y - bh / 2 - 0.1, 0.18, bh + 0.2, fill=INK, edge=INK)
    s.rect(gx + 1.5, y - bh / 2 - 0.1, 0.18, bh + 0.2, fill=INK, edge=INK)
    s.line(gx + 0.18, y + 0.3, gx + 1.5, y + 0.3, color=RED, lw=5)
    s.text(gx + 0.84, y + 0.65, 'approval', size=15, weight='bold', color=RED)
    s.text(gx + 0.84, y - 0.25, 'approve', size=14)
    s.text(gx + 0.84, y - 0.55, 'edit or reject', size=14)
    s.arrow(xs[0] + bw + 0.05, y, xs[1] - 0.05, y, lw=2.4, head=16)
    s.arrow(xs[1] + bw + 0.05, y, gx - 0.05, y, lw=2.4, head=16)
    s.arrow(gx + 1.73, y, xs[3] - 0.05, y, lw=2.4, head=16)
    s.text(w / 2, 0.75, 'Sends, payments, deletions and commitments always wait for approval.', size=16, weight='bold')
    s.text(w / 2, 0.3, 'The agent cannot approve itself. Only a named person can.', size=15, color=BODY)
    return s


@fig('x_t11_mcp')
def x_t11_mcp(w, h, **_):
    s = Scene(w, h)
    hw = 3.0
    s.box(0.05, 0.3, hw, h - 0.6, '', fill=PAPER, edge=INK, lw=2.0)
    s.text(0.05 + hw / 2, h - 0.65, 'Host', size=19, weight='bold')
    s.text(0.05 + hw / 2, h - 1.0, 'the AI application', size=14, color=BODY)
    servers = [('mail', 'Mail server'), ('calendar', 'Calendar server'), ('folder', 'Files server')]
    n = len(servers)
    sx = w - 3.2
    rh = (h - 1.6) / n
    for i, (ic, name) in enumerate(servers):
        yc = h - 1.35 - (i + 0.5) * rh
        s.box(0.35, yc - 0.3, hw - 0.6, 0.6, 'client ' + str(i + 1), size=15, fill=GOLD, edge=INK, lw=1.6)
        s.line(0.05 + hw - 0.3, yc, sx - 0.55, yc, color=INK, lw=3)
        # the plug
        s.rect(sx - 0.55, yc - 0.2, 0.4, 0.4, fill=INK, edge=INK)
        s.rect(sx - 0.15, yc - 0.1, 0.15, 0.06, fill=INK, edge=INK)
        s.rect(sx - 0.15, yc + 0.04, 0.15, 0.06, fill=INK, edge=INK)
        s.box(sx, yc - rh / 2 + 0.08, 3.15, rh - 0.16, '', fill=PAPER, edge=INK, lw=1.8)
        s.icon(ic, sx + 0.4, yc, 0.5)
        s.text(sx + 0.8, yc + 0.17, name, size=16, weight='bold', ha='left')
        s.text(sx + 0.8, yc - 0.2, 'tools, resources, prompts', size=14, color=BODY, ha='left')
    s.text(sx + 1.2, h - 1.1, 'one standard plug', size=17, weight='bold', color=RED)
    return s


MAIL_GROUPS = [
    ('Needs action', ['M01 board pack stock page', 'M06 truck moved to Thursday', 'M09 forum: register by 18 Nov', 'M05 leave request by 20 Nov'], PAPER, INK),
    ('Needs approval first', ['M02 invoice with no PO', 'M03 credit UGX 180,000', 'M07 price rise 4%'], GOLD, INK),
    ('Stop and tell the owner', ['M08 prompt injection', 'M13 prize scam'], PAPER, RED),
    ('Personal', ['M10 Sunday lunch', 'M11 parents meeting', 'M12 dentist Monday', 'M14 hotel in Mbale'], PAPER, INK),
    ('Information only', ['M04 forklift service'], PAPER, INK),
]


@fig('x_t11_mailbox')
def x_t11_mailbox(w, h, **_):
    s = Scene(w, h)
    n = len(MAIL_GROUPS)
    cw = (w - 0.1 - 0.15 * (n - 1)) / n
    for i, (head, items, fill, edge) in enumerate(MAIL_GROUPS):
        x = 0.05 + i * (cw + 0.15)
        s.box(x, 0.05, cw, h - 0.1, '', fill=PAPER, edge=edge, lw=2.0, dash=edge == RED)
        s.box(x, h - 0.95, cw, 0.9, '', fill=fill if fill != PAPER else (INK if edge == INK else RED), edge=edge, lw=2.0)
        _w(s, x + cw / 2, h - 0.5, cw - 0.2, head, 16, 'bold', color=INK if fill == GOLD else PAPER)
        y = h - 1.15
        for it in items:
            hh = len(K.wrap(it, 14, 'regular', cw - 0.6)) * 14 * 1.15 / 72
            s.icon('mail', x + 0.25, y - 0.15, 0.3)
            s.text(x + 0.5, y - hh / 2, '\n'.join(K.wrap(it, 14, 'regular', cw - 0.6)), size=14, ha='left', color=BODY)
            y -= max(hh, 0.35) + 0.2
    return s


@fig('x_t11_planted')
def x_t11_planted(w, h, **_):
    s = Scene(w, h)
    s.rect(0.05, 0.05, w - 0.1, h - 0.1, fill=PAPER, edge=INK, lw=2.0)
    s.rect(0.05, h - 0.7, w - 0.1, 0.65, fill=INK, edge=INK, lw=0, z=3)
    s.text(0.3, h - 0.38, 'M08  From: Pearl Packaging Billing (invented)', size=16, weight='bold', color=PAPER, ha='left', z=6)
    _w(s, 0.3, h - 1.35, w - 0.6, 'October statement: 3 invoices, total UGX 3,870,000, due 20 November.', 17, ha='left')
    s.box(0.2, 0.25, w - 0.4, h - 2.25, '', fill=PAPER, edge=RED, lw=2.4)
    s.tag(0.4, h - 2.35, 'PROMPT INJECTION', size=15, fill=RED)
    _w(s, 0.4, (h - 2.0) / 2, w - 0.8, 'Text aimed at "AI assistants": it asks for the last five Finance emails to be sent back, for this mail to be deleted, and for silence in the summary.', 16, ha='left', color=INK)
    return s


@fig('x_t11_privilege')
def x_t11_privilege(w, h, **_):
    s = Scene(w, h)
    rows = [['Permission', 'Needed?', 'Worst case if it is fooled', 'Undo?'],
            ['Read one mailbox', 'Yes', 'It reads what it was meant to read', 'Nothing to undo'],
            ['Write drafts', 'Yes', 'A bad draft waits in a folder', 'Delete the draft'],
            ['Send', 'No', 'Finance mail leaves the company', 'Cannot be undone']]
    cw = [(w - 0.1) * f for f in (0.22, 0.2, 0.36, 0.22)]
    fh = 0.85
    s.table(0.05, h - 0.05, cw, (h - 0.15 - fh) / 4, rows, size=16, align=['left', 'left', 'left', 'left'], hl_cells={(3, 1): GOLD, (3, 3): GOLD})
    s.text(w / 2, 0.4, 'Least privilege: grant only the permissions the task needs. Here: read and draft.', size=17, weight='bold')
    return s


@fig('x_t11_turn')
def x_t11_turn(w, h, **_):
    """One turn of the loop opened up (illustration, invented mail M03): the model writes text, a program acts, the result goes back into the prompt."""
    s = Scene(w, h)
    bw = (w - 0.1 - 2 * 0.75) / 3
    y0 = 0.85
    bh = h - y0 - 0.05
    top = y0 + bh
    heads = [('1  The prompt', 'as in Session 8'), ('2  The model writes text', 'the next words, as in Session 5'), ('3  A program acts', 'the model cannot press anything')]
    for i, (hd, sub) in enumerate(heads):
        x = 0.05 + i * (bw + 0.75)
        s.box(x, y0, bw, bh, '', fill=GOLD if i == 1 else PAPER, edge=INK, lw=2.0, z=2)
        s.text(x + bw / 2, top - 0.3, hd, size=19, weight='bold')
        s.text(x + bw / 2, top - 0.65, sub, size=14, color=BODY)
        if i < 2:
            s.arrow(x + bw + 0.05, y0 + bh / 2 - 0.1, x + bw + 0.7, y0 + bh / 2 - 0.1, lw=2.4, head=16)
    for k, (a, b) in enumerate([('Goal:', 'summarise the mailbox'), ('Tools:', 'read_mail, save_draft'), ('So far:', 'asked to read M03')]):
        yy = top - 1.05 - k * 0.42
        s.text(0.25, yy, a, size=16, weight='bold', ha='left')
        s.text(1.2, yy, b, size=16, ha='left')
    x = 0.05 + (bw + 0.75)
    s.code(x + 0.25, top - 0.9, ['read_mail("M03")'], size=17, line_h=0.4, w=bw - 0.5, pad=0.1)
    s.text(x + bw / 2, y0 + 0.4, 'A request only. It does nothing.', size=16)
    x = 0.05 + 2 * (bw + 0.75)
    s.text(x + bw / 2, top - 1.15, 'Runs read_mail for M03', size=16)
    s.text(x + bw / 2, top - 1.5, 'and copies the mail text', size=16)
    s.text(x + bw / 2, y0 + 0.4, 'Approval can hold it here', size=16, color=RED, weight='bold')
    s.arrow(x + bw / 2, y0 - 0.12, 0.05 + bw / 2, y0 - 0.12, lw=2.4, head=16, color=RED)
    s.text(w / 2, 0.3, 'Observe: the result goes back into the prompt, then the model writes the next step', size=16, weight='bold')
    return s


# ================================================================== 11 November 2026 rework: explain before use
@fig('x_t11_build')
def x_t11_build(w, h, **_):
    """An agent built in three steps: a model that answers, plus tools, plus a loop."""
    s = Scene(w, h)
    gap = 0.35
    pw = (w - 0.1 - 2 * gap) / 3
    heads = ['1  A model that answers', '2  + tools', '3  + a loop']
    subs = ['Sessions 5 and 8', 'a program does the act', 'until the goal is met']
    for i in range(3):
        x = 0.05 + i * (pw + gap)
        s.box(x, 0.05, pw, h - 0.1, '', fill=GOLD if i == 2 else PAPER, edge=INK, lw=2.0)
        s.text(x + pw / 2, h - 0.38, heads[i], size=19, weight='bold')
        s.text(x + pw / 2, h - 0.75, subs[i], size=15, color=BODY)
    # panel 1: prompt -> model -> answer, stacked
    x = 0.05
    for k, lab in enumerate(['Prompt', 'Model: next tokens', 'Answer: you act']):
        yy = h - 1.45 - k * 0.95
        s.box(x + 0.35, yy - 0.3, pw - 0.7, 0.6, lab, size=16, fill=PAPER, edge=INK, lw=1.6)
        if k < 2:
            s.arrow(x + pw / 2, yy - 0.32, x + pw / 2, yy - 0.63, lw=2.0, head=12)
    # panel 2: model writes request, program runs tool
    x = 0.05 + pw + gap
    s.box(x + 0.35, h - 1.75, pw - 0.7, 0.6, 'Model writes:', size=16, fill=PAPER, edge=INK, lw=1.6)
    s.code(x + 0.45, h - 2.0, ['read_mail("M03")'], size=16, line_h=0.4, w=pw - 0.9, pad=0.08)
    s.arrow(x + pw / 2, h - 2.55, x + pw / 2, h - 2.85, lw=2.0, head=12)
    s.box(x + 0.35, h - 3.5, pw - 0.7, 0.6, 'Program runs the tool', size=16, fill=PAPER, edge=INK, lw=1.6)
    s.text(x + pw / 2, 0.35, 'tool: a named action', size=15, color=BODY)
    # panel 3: loop
    x = 0.05 + 2 * (pw + gap)
    cx, cy, r = x + pw / 2, h / 2 - 0.35, 1.0
    pos = [(cx, cy + r * 0.85, 'Plan'), (cx + r * 1.05, cy - r * 0.55, 'Act'), (cx - r * 1.05, cy - r * 0.55, 'Observe')]
    for k in range(3):
        x1, y1, _a = pos[k]
        x2, y2, _b = pos[(k + 1) % 3]
        s.arrow(x1 + (x2 - x1) * 0.3, y1 + (y2 - y1) * 0.3, x1 + (x2 - x1) * 0.7, y1 + (y2 - y1) * 0.7, lw=2.2, head=14, rad=-0.25)
    for xx, yy, lab in pos:
        s.box(xx - 0.6, yy - 0.25, 1.2, 0.5, lab, size=16, fill=PAPER, edge=INK, lw=1.6, weight='bold', z=3)
    return s


@fig('x_t11_injectsteps')
def x_t11_injectsteps(w, h, **_):
    s = Scene(w, h)
    steps = [('1  Act', 'read_mail(M08)', 'a permitted read'),
             ('2  Observe', 'The mail text enters the prompt', 'hidden order included'),
             ('3  Plan', 'The model may write: forward 5 Finance mails', 'one stream of text (Session 10)'),
             ('4  Program', 'Is forward permitted?', 'No: refused'),
             ('5  Stop', 'Warn the owner', 'stop condition')]
    n = len(steps)
    gap = 0.3
    bw = (w - 0.1 - gap * (n - 1)) / n
    by = 0.75
    for i, (head, mid, sub) in enumerate(steps):
        x = 0.05 + i * (bw + gap)
        red = i == 2
        s.box(x, by, bw, h - by - 0.05, '', fill=GOLD if i == 3 else PAPER, edge=RED if red else INK, lw=2.2)
        s.text(x + bw / 2, h - 0.4, head, size=18, weight='bold', color=RED if red else INK)
        wt_ = _w(s, x + bw / 2, h / 2 + 0.25, bw - 0.25, mid, 16, 'bold')
        _w(s, x + bw / 2, by + 0.45, bw - 0.25, sub, 15, color=BODY)
        if i < n - 1:
            s.arrow(x + bw + 0.02, h / 2, x + bw + gap - 0.02, h / 2, lw=2.2, head=14)
    s.text(w / 2, 0.3, 'Only the permissions and the program stop step 3 becoming an act.', size=16, weight='bold', color=RED)
    return s


@fig('x_t11_risk')
def x_t11_risk(w, h, **_):
    s = Scene(w, h)
    rows = [['Permissions', 'Likelihood', 'Impact (UGX)', 'Risk (UGX)'],
            ['Read only', '0.01', '0', '0.01 \u00d7 0 = 0'],
            ['Read, draft', '0.01', '20,000', '0.01 \u00d7 20,000 = 200'],
            ['Read, draft, send', '0.01', '20,000,000', '0.01 \u00d7 20,000,000 = 200,000']]
    s.table(0.05, h - 0.05, [1.85, 1.2, 1.55, 3.0], 0.68, rows, size=15, align=['left', 'center', 'right', 'left'], hl_cells={(3, 3): GOLD})
    s.text(w / 2, 1.35, 'Risk = likelihood \u00d7 impact', size=19, weight='bold')
    s.text(w / 2, 0.85, 'Likelihood 0.01: 1 in 100 injected mails fools it', size=15, color=BODY)
    s.text(w / 2, 0.35, 'Illustration: all figures invented, per injected mail', size=15, color=MUTE)
    return s


@fig('x_t11_approvaltime')
def x_t11_approvaltime(w, h, **_):
    s = Scene(w, h)
    s.text(w / 2, h - 0.3, '14 mails in the demonstration mailbox', size=17, weight='bold')
    need = {2, 3, 7}
    cw = (w - 0.1) / 7
    for i in range(14):
        r, c = divmod(i, 7)
        x = 0.05 + c * cw
        y = h - 1.05 - r * 0.95
        s.rect(x + 0.05, y - 0.38, cw - 0.1, 0.76, fill=GOLD if (i + 1) in need else PAPER, edge=INK, lw=1.4)
        s.text(x + cw / 2, y, f'M{i + 1:02d}', size=15, weight='bold' if (i + 1) in need else 'normal')
    s.text(0.1, 1.45, 'Gold: needs approval', size=16, ha='left', weight='bold')
    s.text(w - 0.1, 1.45, '2 + 2 + 2 = 6 minutes', size=17, ha='right', weight='bold')
    s.text(w / 2, 0.85, 'T = n \u00d7 t = 3 \u00d7 2 = 6 minutes', size=19, weight='bold', color=RED)
    s.text(w / 2, 0.3, 'n: approvals   t: minutes each (my estimate)   T: total', size=15, color=BODY)
    return s


@fig('x_t11_mcpcount')
def x_t11_mcpcount(w, h, **_):
    s = Scene(w, h)
    half = (w - 0.3) / 2
    apps = ['App A', 'App B', 'App C']
    tools = ['Mail', 'Calendar', 'Files', 'Accounts']
    def side(x0, hub):
        ay = [h - 1.2 - k * 0.95 for k in range(3)]
        ty = [h - 1.0 - k * 0.72 for k in range(4)]
        ax_, tx_ = x0 + 0.7, x0 + half - 0.75
        if hub:
            hx, hy = x0 + half / 2, h / 2 - 0.3
            for y in ay:
                s.line(ax_ + 0.5, y, hx - 0.35, hy, lw=2.0)
            for y in ty:
                s.line(hx + 0.35, hy, tx_ - 0.55, y, lw=2.0)
            s.box(hx - 0.4, hy - 0.3, 0.8, 0.6, 'MCP', size=15, fill=GOLD, edge=INK, lw=1.8, weight='bold', z=4)
        else:
            for y in ay:
                for t in ty:
                    s.line(ax_ + 0.5, y, tx_ - 0.55, t, lw=1.4, color=RED)
        for k, y in enumerate(ay):
            s.box(ax_ - 0.55, y - 0.25, 1.05, 0.5, apps[k], size=15, fill=PAPER, edge=INK, lw=1.6, z=4)
        for k, y in enumerate(ty):
            s.box(tx_ - 0.55, y - 0.25, 1.25, 0.5, tools[k], size=15, fill=PAPER, edge=INK, lw=1.6, z=4)
    side(0.05, False)
    side(0.25 + half, True)
    s.text(0.05 + half / 2, h - 0.3, 'No standard', size=17, weight='bold', color=RED)
    s.text(0.25 + half * 1.5, h - 0.3, 'One standard', size=17, weight='bold')
    s.text(0.05 + half / 2, 0.35, '3 \u00d7 4 = 12 connectors', size=17, weight='bold', color=RED)
    s.text(0.25 + half * 1.5, 0.35, '3 + 4 = 7 pieces', size=17, weight='bold')
    return s
