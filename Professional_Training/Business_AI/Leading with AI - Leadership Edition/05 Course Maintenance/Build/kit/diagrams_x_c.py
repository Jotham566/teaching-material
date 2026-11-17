"""Figure kinds added by author c for Sessions 6 and 8 (the two demonstration sessions).

rulechain  : a message router drawn as a chain of rules. data: trigger {head, text}; rules [{head, text, to, to_text}]; otherwise {head, text, to, to_text};
             log {head, text}; hl (index of the rule to highlight in gold; len(rules) means the otherwise row).
draftgrid  : a table of reply drafts. data: rows [{id, promised, avoided, edit (None or text)}]; heads (4 column titles). A cell with an edit is gold.
approval   : the approval step. data: first {head, text, icon}; second {head, text, icon}; outcomes [{head, text}] (3); stop {head, text}.
"""
from figkit import Scene, INK, BODY, MUTE, HAIR, PAPER, RED, GOLD, LayoutError, fig
import slidekit as K


def _lines_h(text, size, w, kind='regular'):
    n = len(K.wrap(text, size, kind, w))
    return n, n * size * 1.15 / 72.0


def _two(s, x, y, w, h, head, body, size=15, fill=PAPER, head_color=INK, lw=1.8):
    """A box with a bold head and a wrapped body, text centred."""
    s.box(x, y, w, h, '', fill=fill, edge=INK, lw=lw, r=0.07)
    hl = K.wrap(head, size + 1, 'bold', w - 0.3)
    bl = K.wrap(body, size, 'regular', w - 0.3) if body else []
    th = (len(hl) * (size + 1) + len(bl) * size) * 1.15 / 72.0
    if th > h - 0.06:
        raise LayoutError(f'box text too tall: {head!r} needs {th:.2f} in, has {h - 0.06:.2f}')
    top = y + h / 2 + th / 2
    hh = len(hl) * (size + 1) * 1.15 / 72.0
    s.text(x + w / 2, top - hh / 2, '\n'.join(hl), size=size + 1, weight='bold', color=head_color)
    if bl:
        s.text(x + w / 2, top - hh - (len(bl) * size * 1.15 / 72.0) / 2, '\n'.join(bl), size=size, color=BODY)


@fig('x_rulechain')
def x_rulechain(w, h, trigger=None, rules=(), otherwise=None, log=None, hl=None, size=15, **_):
    s = Scene(w, h)
    n = 1 + len(rules) + 1
    gap = 0.34
    rh = (h - 0.1 - gap * (n - 1)) / n
    c1, c2 = 4.7, 3.1
    x1 = 0.05
    x2 = x1 + c1 + 0.85
    x3 = x2 + c2 + 0.85
    ytop = h - 0.05
    rows = []
    for i in range(n):
        rows.append(ytop - (i + 1) * rh - i * gap)   # bottom y of row i
    # trigger
    _two(s, x1, rows[0], c1, rh, trigger['head'], trigger.get('text', ''), size, fill=GOLD if hl == 'trigger' else PAPER)
    items = list(rules) + [otherwise]
    for k, it in enumerate(items):
        y = rows[k + 1]
        fill = GOLD if hl == k else PAPER
        _two(s, x1, y, c1, rh, it['head'], it.get('text', ''), size, fill=fill)
        # down arrow from the previous box
        s.arrow(x1 + c1 / 2, rows[k] - 0.02, x1 + c1 / 2, rows[k + 1] + rh + 0.02, lw=2.2, head=16)
        if k < len(rules):
            s.text(x1 + c1 / 2 + 0.32, rows[k] - gap / 2 + 0.0, 'no' if k > 0 else 'start', size=14, color=MUTE, ha='left')
        else:
            s.text(x1 + c1 / 2 + 0.32, rows[k] - gap / 2, 'no rule fired', size=14, color=MUTE, ha='left')
        # to queue
        s.arrow(x1 + c1 + 0.03, y + rh / 2, x2 - 0.03, y + rh / 2, lw=2.2, head=16)
        if k < len(rules):
            s.text(x1 + c1 + 0.42, y + rh / 2 + 0.22, 'yes', size=14, color=MUTE)
        _two(s, x2, y, c2, rh, it['to'], it.get('to_text', ''), size, fill=GOLD if hl == k else PAPER)
    # log column spans the rule rows and the otherwise row
    ly = rows[-1]
    lh = rows[1] + rh - rows[-1]
    c3 = w - 0.05 - x3
    s.box(x3, ly, c3, lh, '', fill=PAPER, edge=INK, lw=1.8, r=0.07)
    hl_ = K.wrap(log['head'], size + 1, 'bold', c3 - 0.3)
    bl = K.wrap(log['text'], size, 'regular', c3 - 0.3)
    th = (len(hl_) * (size + 1) + len(bl) * size) * 1.15 / 72.0
    if th > lh - 0.1:
        raise LayoutError('log text too tall')
    top = ly + lh / 2 + th / 2
    hh = len(hl_) * (size + 1) * 1.15 / 72.0
    s.text(x3 + c3 / 2, top - hh / 2, '\n'.join(hl_), size=size + 1, weight='bold')
    s.text(x3 + c3 / 2, top - hh - (len(bl) * size * 1.15 / 72.0) / 2, '\n'.join(bl), size=size, color=BODY)
    for k in range(len(items)):
        y = rows[k + 1]
        s.arrow(x2 + c2 + 0.03, y + rh / 2, x3 - 0.03, y + rh / 2, lw=2.0, head=14)
    return s


@fig('x_draftgrid')
def x_draftgrid(w, h, rows=(), heads=('Draft', 'What it promised', 'What it avoided', 'What I would edit'), size=14, **_):
    s = Scene(w, h)
    cw = [0.75, 4.1, 2.9, w - 0.75 - 4.1 - 2.9]
    xs = [0.0]
    for c in cw:
        xs.append(xs[-1] + c)
    n = len(rows) + 1
    hh = 0.45
    rh = (h - 0.05 - hh) / len(rows)
    top = h - 0.02
    for j, t in enumerate(heads):
        s.text(xs[j] + 0.08, top - hh / 2, t, size=size + 1, weight='bold', ha='left')
    s.line(0, top - hh, w, top - hh, color=INK, lw=2.2)
    for i, r in enumerate(rows):
        y1 = top - hh - rh * i
        yc = y1 - rh / 2
        edit = r.get('edit')
        if edit:
            s.rect(xs[3] + 0.03, y1 - rh + 0.03, cw[3] - 0.06, rh - 0.06, fill=GOLD, edge=GOLD, lw=0, z=2)
        cells = [r['id'], r['promised'], r['avoided'], edit or 'No edit']
        for j, t in enumerate(cells):
            kind = 'bold' if j == 0 else 'regular'
            lines = K.wrap(t, size, kind, cw[j] - 0.18)
            if len(lines) * size * 1.15 / 72.0 > rh - 0.06:
                raise LayoutError(f'draftgrid cell too tall: {t[:30]!r} {len(lines)} lines')
            s.text(xs[j] + 0.08, yc, '\n'.join(lines), size=size, weight='bold' if j == 0 else 'normal', ha='left', color=INK if (j == 0 or j == 3) else BODY, z=6)
        s.line(0, y1 - rh, w, y1 - rh, color=HAIR, lw=0.8)
    return s


@fig('x_approval')
def x_approval(w, h, first=None, second=None, outcomes=(), stop=None, size=15, **_):
    s = Scene(w, h)
    bh = 1.55
    top_y = h - 0.05 - bh - 0.15
    # first and second boxes, top band
    bw1, bw2 = 2.9, 3.6
    x1 = 0.05
    x2 = x1 + bw1 + 0.7
    s.box(x1, top_y, bw1, bh, '', edge=INK, lw=1.8)
    s.icon(first.get('icon', 'robot'), x1 + bw1 / 2, top_y + bh - 0.42, 0.7)
    _two_text(s, x1, top_y, bw1, bh - 0.8, first['head'], first.get('text', ''), size)
    s.arrow(x1 + bw1 + 0.03, top_y + bh / 2, x2 - 0.03, top_y + bh / 2, lw=2.4, head=18)
    s.box(x2, top_y, bw2, bh, '', fill=GOLD, edge=INK, lw=2.2)
    s.icon(second.get('icon', 'person'), x2 + bw2 / 2, top_y + bh - 0.42, 0.7)
    _two_text(s, x2, top_y, bw2, bh - 0.8, second['head'], second.get('text', ''), size)
    # outcomes on the right
    n = len(outcomes)
    ox = x2 + bw2 + 0.8
    ow = w - 0.05 - ox
    og = 0.12
    oh = (bh + 0.1 + 0.0) / 1.0
    # stack outcomes beside the top band, spanning the full height above the stop band
    stop_h = 1.15
    avail = h - 0.1 - stop_h - 0.25
    oh = (avail - og * (n - 1)) / n
    for i, o in enumerate(outcomes):
        y = h - 0.05 - (i + 1) * oh - i * og
        _two(s, ox, y, ow, oh, o['head'], o.get('text', ''), size)
        s.arrow(x2 + bw2 + 0.03, top_y + bh / 2, ox - 0.03, y + oh / 2, lw=1.8, head=14)
    # stop band, bottom
    sy = 0.05
    s.box(0.05, sy, w - 0.1, stop_h, '', fill=PAPER, edge=RED, lw=2.2)
    tw = s.tag(0.3, sy + stop_h - 0.5, stop['head'], size=size, fill=RED)
    lines = K.wrap(stop['text'], size, 'regular', w - 0.6)
    s.text(0.3, sy + (stop_h - 0.55) / 2, '\n'.join(lines), size=size, ha='left', color=BODY)
    return s


def _two_text(s, x, y, w, h, head, body, size):
    hl = K.wrap(head, size + 1, 'bold', w - 0.3)
    bl = K.wrap(body, size, 'regular', w - 0.3) if body else []
    th = (len(hl) * (size + 1) + len(bl) * size) * 1.15 / 72.0
    top = y + h / 2 + th / 2
    hh = len(hl) * (size + 1) * 1.15 / 72.0
    s.text(x + w / 2, top - hh / 2, '\n'.join(hl), size=size + 1, weight='bold')
    if bl:
        s.text(x + w / 2, top - hh - (len(bl) * size * 1.15 / 72.0) / 2, '\n'.join(bl), size=size, color=BODY)
