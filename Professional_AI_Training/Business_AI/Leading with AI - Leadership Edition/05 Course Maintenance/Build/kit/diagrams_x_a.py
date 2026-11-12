"""Figure kinds for Sessions 2 and 3 (author a).

weekcheck: twelve weeks of sales, the total recounted from the rows, the hand-made figure, the gap, and what each AI run said.
  rows: [{'week': '2026-08-24', 'true': 645561000, 'hand': 645651000, 'ai1': 645561000, 'ai2': 645561000}]
emails: two emails side by side, each a list of lines with a flag.
  left / right: {'head': 'Weak brief', 'sub': 'one run', 'lines': [{'t': 'text', 'flag': None | 'bad' | 'good'}]}
"""
from figkit import Scene, INK, BODY, MUTE, HAIR, PAPER, RED, GOLD, fig
import slidekit as K


@fig('x_weekcheck')
def x_weekcheck(w, h, rows=(), size=14, **_):
    s = Scene(w, h)
    cw = [1.75, 2.75, 2.75, 2.1, 1.275, 1.275]
    xs = [0.0]
    for c in cw:
        xs.append(xs[-1] + c)
    n = len(rows) + 1
    rh = (h - 0.05) / n
    heads = ['Week start', 'Total from the rows', 'Hand-made summary', 'Gap', 'AI run 1', 'AI run 2']
    top = h - 0.02
    for j, t in enumerate(heads):
        s.text(xs[j] + 0.08, top - rh / 2, t, size=size, weight='bold', ha='left')
    s.line(0, top - rh, w, top - rh, color=INK, lw=2.2)
    for i, r in enumerate(rows):
        y1 = top - rh * (i + 1)
        yc = y1 - rh / 2
        gap = r['hand'] - r['true']
        if gap:
            s.rect(xs[3] + 0.04, y1 - rh + 0.03, cw[3] - 0.08, rh - 0.06, fill=GOLD, edge=GOLD, lw=0, z=2)
        s.text(xs[0] + 0.08, yc, r['week'], size=size, weight='bold', ha='left')
        s.text(xs[1] + 0.08, yc, f"{r['true']:,}", size=size, ha='left', color=BODY)
        s.text(xs[2] + 0.08, yc, f"{r['hand']:,}", size=size, ha='left', color=BODY, weight='bold' if gap else 'normal')
        s.text(xs[3] + 0.08, yc, ('0' if not gap else f"{gap:+,}".replace('-', '−')), size=size, ha='left', weight='bold' if gap else 'normal', z=6)
        for k, key in ((4, 'ai1'), (5, 'ai2')):
            ok = r[key] == r['true']
            s.text(xs[k] + 0.08, yc, 'matches' if ok else 'WRONG', size=size, ha='left', weight='normal' if ok else 'bold', color=BODY if ok else RED)
        s.line(0, y1 - rh, w, y1 - rh, color=HAIR, lw=0.8)
    return s


@fig('x_emails')
def x_emails(w, h, left=None, right=None, size=14, **_):
    s = Scene(w, h)
    gap = 0.2
    pw = (w - gap) / 2
    for i, side in enumerate((left, right)):
        x0 = i * (pw + gap)
        s.rect(x0 + 0.02, 0.02, pw - 0.04, h - 0.04, fill=PAPER, edge=INK, lw=1.8)
        s.rect(x0 + 0.02, h - 0.62, pw - 0.04, 0.6, fill=INK, edge=INK, lw=0, z=3)
        s.text(x0 + 0.2, h - 0.32, side['head'], size=17, weight='bold', color=PAPER, ha='left', z=6)
        if side.get('sub'):
            s.text(x0 + pw - 0.2, h - 0.32, side['sub'], size=14, color=GOLD, ha='right', z=6)
        y = h - 0.72
        for ln in side['lines']:
            lines = K.wrap(ln['t'], size, 'regular', pw - 0.6)
            hh = len(lines) * size * 1.2 / 72 + 0.12
            flag = ln.get('flag')
            if flag == 'bad':
                s.rect(x0 + 0.1, y - hh, pw - 0.2, hh, fill=RED, edge=RED, lw=0, z=2)
            elif flag == 'good':
                s.rect(x0 + 0.1, y - hh, pw - 0.2, hh, fill=GOLD, edge=GOLD, lw=0, z=2)
            s.text(x0 + 0.2, y - hh / 2, '\n'.join(lines), size=size, ha='left', color=PAPER if flag == 'bad' else INK,
                   weight='bold' if flag else 'normal', mono=False, italic=ln.get('italic', False), z=6)
            y -= hh + 0.03
    return s
