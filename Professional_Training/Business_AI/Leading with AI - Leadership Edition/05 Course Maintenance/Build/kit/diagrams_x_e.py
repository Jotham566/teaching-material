"""Figure kinds added by author e (Sessions 9, 10 and 11).

catch: a table of planted problems against the runs that were checked.
rows: [{'id': '3', 'text': 'Trains on your data', 'marks': [{'state': 'yes', 'label': 'caught'}, {'state': 'part', 'label': 'unsure'}]}]
state: 'yes' (plain), 'no' (red fill: missed or wrong), 'part' (gold fill: flagged but not decided).
heads: [id header, text header, run headers...]."""
from figkit import Scene, INK, BODY, MUTE, HAIR, PAPER, RED, GOLD, fig
import slidekit as K


@fig('x_catch')
def x_catch(w, h, heads=('No.', 'Planted problem', 'Run 1', 'Run 2'), rows=(), size=15, **_):
    s = Scene(w, h)
    nm = len(heads) - 2
    idw = 0.8
    mw = 1.75
    tw = w - idw - mw * nm
    xs = [0.0, idw, idw + tw] + [idw + tw + mw * (i + 1) for i in range(nm)]
    n = len(rows) + 1
    rh = (h - 0.05) / n
    top = h - 0.02
    for sz in range(int(size), 12, -1):
        if all(K.width_in(r['text'], sz) <= tw - 0.2 for r in rows):
            break
    sz = max(sz, 14)
    hs = max(sz, 14)
    s.text(xs[0] + 0.08, top - rh / 2, heads[0], size=hs, weight='bold', ha='left')
    s.text(xs[1] + 0.08, top - rh / 2, heads[1], size=hs, weight='bold', ha='left')
    for j in range(nm):
        s.text(xs[2] + mw * j + mw / 2, top - rh / 2, heads[2 + j], size=hs, weight='bold')
    s.line(0, top - rh, w, top - rh, color=INK, lw=2.2)
    for i, r in enumerate(rows):
        y1 = top - rh * (i + 1)
        yc = y1 - rh / 2
        s.text(xs[0] + 0.08, yc, str(r['id']), size=sz, weight='bold', ha='left')
        s.text(xs[1] + 0.08, yc, r['text'], size=sz, ha='left', color=BODY)
        for j, m in enumerate(r['marks']):
            x0 = xs[2] + mw * j
            st = m['state']
            if st == 'no':
                s.rect(x0 + 0.05, y1 - rh + 0.03, mw - 0.1, rh - 0.06, fill=RED, edge=RED, lw=0, z=2)
            elif st == 'part':
                s.rect(x0 + 0.05, y1 - rh + 0.03, mw - 0.1, rh - 0.06, fill=GOLD, edge=GOLD, lw=0, z=2)
            s.text(x0 + mw / 2, yc, m['label'], size=sz, weight='bold', color=PAPER if st == 'no' else INK, z=6)
        s.line(0, y1 - rh, w, y1 - rh, color=HAIR, lw=0.8)
    return s
