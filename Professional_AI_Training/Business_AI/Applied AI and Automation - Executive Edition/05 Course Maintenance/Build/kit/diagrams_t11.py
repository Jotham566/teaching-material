"""Figures for Session 11, Agentic AI (v3, 6 November 2026).

t11_loop       the plan, act, observe loop with a goal, a stop and a log line per turn
t11_badges     the agent as a junior assistant wearing access badges (granted and refused)
t11_autonomy   five levels of autonomy, from answer only to acts alone
t11_gate       the approval gate: the agent prepares, a person decides, then the action runs
t11_mcp        MCP as a standard plug: one host, one client per server, servers offer tools, resources, prompts
t11_mailbox    the fourteen demonstration mails sorted by the lecturer's key (no AI output)
t11_planted    a mail with a planted instruction: the ordinary part and the planted part
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


BADGES = [
    dict(icon='mail', head='Read mail', sub='one mailbox', ok=True),
    dict(icon='doc', head='Write drafts', sub='drafts folder', ok=True),
    dict(icon='calendar', head='See calendar', sub='not given', ok=False),
    dict(icon='speech', head='Send', sub='never alone', ok=False),
    dict(icon='receipt', head='Pay', sub='never', ok=False),
]


@fig('x_t11_badges')
def x_t11_badges(w, h, badges=None, **_):
    s = Scene(w, h)
    badges = badges or BADGES
    # the junior assistant
    s.icon('person', 1.2, h / 2 + 0.35, 2.0)
    s.text(1.2, h / 2 - 1.15, 'The agent:', size=16, weight='bold')
    s.text(1.2, h / 2 - 1.5, 'a junior assistant', size=15, color=BODY)
    n = len(badges)
    x0 = 2.6
    bw = (w - x0 - 0.1)
    rh = (h - 0.1) / n
    for i, b in enumerate(badges):
        y = h - 0.05 - (i + 1) * rh
        s.box(x0, y + 0.06, bw, rh - 0.12, '', fill=GOLD if b['ok'] else PAPER, edge=INK if b['ok'] else RED, lw=2.0, dash=not b['ok'])
        s.icon(b['icon'], x0 + 0.45, y + rh / 2, min(0.6, rh - 0.2))
        s.text(x0 + 0.95, y + rh / 2, b['head'], size=18, weight='bold', ha='left')
        s.text(x0 + bw - 1.0, y + rh / 2, b['sub'], size=15, color=BODY if b['ok'] else RED, ha='right')
        s.icon('check' if b['ok'] else 'cross', x0 + bw - 0.45, y + rh / 2, min(0.55, rh - 0.25))
        s.line(1.75, h / 2 + 0.3, x0, y + rh / 2, color=HAIR, lw=1.2, z=1)
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


@fig('x_t11_gate')
def x_t11_gate(w, h, **_):
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
    # the gate itself
    gx = xs[2] + 0.35
    s.rect(gx, y - bh / 2 - 0.1, 0.18, bh + 0.2, fill=INK, edge=INK)
    s.rect(gx + 1.5, y - bh / 2 - 0.1, 0.18, bh + 0.2, fill=INK, edge=INK)
    s.line(gx + 0.18, y + 0.3, gx + 1.5, y + 0.3, color=RED, lw=5)
    s.text(gx + 0.84, y + 0.65, 'the gate', size=15, weight='bold', color=RED)
    s.text(gx + 0.84, y - 0.25, 'approve', size=14)
    s.text(gx + 0.84, y - 0.55, 'edit or reject', size=14)
    s.arrow(xs[0] + bw + 0.05, y, xs[1] - 0.05, y, lw=2.4, head=16)
    s.arrow(xs[1] + bw + 0.05, y, gx - 0.05, y, lw=2.4, head=16)
    s.arrow(gx + 1.73, y, xs[3] - 0.05, y, lw=2.4, head=16)
    s.text(w / 2, 0.75, 'Sends, payments, deletions and commitments always pass the gate.', size=16, weight='bold')
    s.text(w / 2, 0.3, 'The agent cannot open it. Only a named person can.', size=15, color=BODY)
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
    s.text(sx + 1.55, h - 0.55, 'one standard plug', size=17, weight='bold', color=RED)
    return s


MAIL_GROUPS = [
    ('Needs action', ['M01 board pack stock page', 'M06 truck moved to Thursday', 'M09 forum: register by 18 Nov', 'M05 leave request by 20 Nov'], PAPER, INK),
    ('Needs approval first', ['M02 invoice with no PO', 'M03 credit UGX 180,000', 'M07 price rise 4%'], GOLD, INK),
    ('Stop and tell the owner', ['M08 planted instruction', 'M13 prize scam'], PAPER, RED),
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
    s.tag(0.4, h - 2.35, 'PLANTED', size=15, fill=RED)
    _w(s, 0.4, (h - 2.0) / 2, w - 0.8, 'Text aimed at "AI assistants": it asks for the last five Finance emails to be sent back, for this mail to be deleted, and for silence in the summary.', 16, ha='left', color=INK)
    return s


@fig('x_t11_privilege')
def x_t11_privilege(w, h, **_):
    s = Scene(w, h)
    rows = [['Permission given', 'Worst case if it is fooled', 'Undo?'],
            ['Read one mailbox', 'It reads what it was meant to read', 'Nothing to undo'],
            ['Read and draft', 'A bad draft waits in a folder', 'Delete the draft'],
            ['Read, draft and send', 'Finance mail leaves the company', 'Cannot be undone']]
    cw = [(w - 0.1) * 0.3, (w - 0.1) * 0.43, (w - 0.1) * 0.27]
    s.table(0.05, h - 0.05, cw, (h - 0.15) / 4, rows, size=16, align=['left', 'left', 'left'], hl_cells={(3, 2): GOLD, (3, 1): GOLD})
    return s
