"""Figure kind for the Session 1 results slides: `verdicts`, a table of the twelve messages with the key, one answer column and a result mark.

rows: [{'id': 'M07', 'msg': 'short text', 'key': 'Order', 'said': 'Complaints', 'ok': True | False | None}] ; ok None means flagged as mixed or unsure (gold).
cols: headers (key header, answer header)."""
from figkit import Scene, INK, BODY, MUTE, HAIR, PAPER, RED, GOLD, fig
import slidekit as K


@fig('x_verdicts')
def x_verdicts(w, h, rows=(), key_head='The key', said_head='Answer', size=14, **_):
    s = Scene(w, h)
    cw = [0.75, w - 0.75 - 1.9 - 2.6 - 1.25, 1.9, 2.6, 1.25]
    xs = [0.0]
    for c in cw:
        xs.append(xs[-1] + c)
    n = len(rows) + 1
    rh = (h - 0.05) / n
    heads = ['Id', 'Message (shortened)', key_head, said_head, 'Result']
    top = h - 0.02
    for j, t in enumerate(heads):
        s.text(xs[j] + 0.08, top - rh / 2, t, size=size, weight='bold', ha='left')
    s.line(0, top - rh, w, top - rh, color=INK, lw=2.2)
    for i, r in enumerate(rows):
        y1 = top - rh * (i + 1)
        yc = y1 - rh / 2
        ok = r['ok']
        if ok is False:
            s.rect(xs[4] + 0.04, y1 - rh + 0.03, cw[4] - 0.08, rh - 0.06, fill=RED, edge=RED, lw=0, z=2)
        elif ok is None:
            s.rect(xs[4] + 0.04, y1 - rh + 0.03, cw[4] - 0.08, rh - 0.06, fill=GOLD, edge=GOLD, lw=0, z=2)
        s.text(xs[0] + 0.08, yc, r['id'], size=size, weight='bold', ha='left')
        s.text(xs[1] + 0.08, yc, r['msg'], size=size, ha='left', color=BODY)
        s.text(xs[2] + 0.08, yc, r['key'], size=size, ha='left')
        s.text(xs[3] + 0.08, yc, r['said'], size=size, ha='left', weight='bold' if ok is not True else 'normal')
        mark = 'yes' if ok is True else ('NO' if ok is False else 'flagged')
        s.text(xs[4] + cw[4] / 2, yc, mark, size=size, weight='bold', color=PAPER if ok is False else INK, z=6)
        s.line(0, y1 - rh, w, y1 - rh, color=HAIR, lw=0.8)
    return s
