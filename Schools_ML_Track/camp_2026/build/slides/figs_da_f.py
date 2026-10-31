"""DA figures, part F: hero figures for sessions 12, 21 and 23."""
from figs_da_util import Scene, fig, sales, money, INK, BODY, MUTE, HAIR, PAPER, RED, GOLD


@fig('da_hero_checkpoint_one')
def da_hero_checkpoint_one(w, h, **_):
    s = Scene(w, h)
    by = sales().groupby('branch')['line_value'].sum().sort_values(ascending=False)
    cw = (w - 0.4 - 2 * 0.3) / 3
    for i, (b, v) in enumerate(by.items()):
        x = 0.2 + i * (cw + 0.3)
        s.box(x, 0.35, cw, h - 0.7, '', fill=PAPER, lw=1.8, r=0.05)
        s.icon('shop', x + 0.8, h - 1.0, 0.95)
        s.text(x + 1.5, h - 0.8, b, size=20, weight='bold', ha='left')
        s.text(x + 1.5, h - 1.25, 'revenue, UGX', size=16, color=MUTE, ha='left')
        s.text(x + cw / 2, h - 2.2, money(v), size=28, weight='bold')
        s.rect(x + 0.4, 0.8, (cw - 0.8) * v / by.max(), 0.55, fill=GOLD if i == 0 else PAPER, edge=INK, lw=1.6)
    return s


@fig('da_hero_report')
def da_hero_report(w, h, **_):
    s = Scene(w, h)
    by = sales().groupby('branch')['line_value'].sum().sort_values(ascending=False)
    px, pw = 0.3, 4.3
    s.box(px, 0.25, pw, h - 0.5, '', fill=PAPER, lw=2.0, r=0.02)
    s.text(px + 0.25, h - 0.7, 'Revenue by branch', size=18, weight='bold', ha='left')
    for i, v in enumerate(by.values):
        s.rect(px + 0.5 + i * 1.15, 1.7, 0.85, 1.7 * v / by.max(), fill=GOLD if i == 0 else PAPER, edge=INK, lw=1.6)
    s.line(px + 0.3, 1.7, px + pw - 0.3, 1.7, color=INK, lw=1.8)
    for k, y in enumerate((1.3, 0.95, 0.6)):
        s.line(px + 0.3, y, px + pw - 0.3 - (0.9 if k == 2 else 0), y, color=HAIR, lw=3)
    s.icon('person', 5.6, h - 1.1, 0.9)
    s.text(6.3, h - 1.1, 'leaves the room', size=19, ha='left', color=BODY)
    qs = ['What is shown?', 'Which bar is largest?', 'What can it not show?']
    for i, q in enumerate(qs):
        y = h - 2.0 - i * 0.8
        s.icon('check', 5.6, y, 0.55)
        s.text(6.1, y, q, size=21, weight='bold', ha='left')
    s.text(5.45, 0.4, 'The page answers all three alone.', size=19, ha='left', color=BODY)
    return s


@fig('da_hero_talk')
def da_hero_talk(w, h, **_):
    s = Scene(w, h)
    s.icon('person', 0.9, h - 1.3, 1.1)
    s.text(0.9, h - 2.15, 'you', size=19, weight='bold')
    names = ['question', 'data', 'what I did', 'finding', 'limit']
    fw = 1.4
    for i, n in enumerate(names):
        x = 1.9 + i * (fw + 0.15)
        s.box(x, h - 2.7, fw, 1.9, '', fill=GOLD if i == 3 else PAPER, lw=1.8, r=0.04)
        s.text(x + fw / 2, h - 1.75, n, size=17, weight='bold')
    s.icon('person', w - 0.9, h - 1.3, 1.1)
    s.text(w - 0.9, h - 2.15, 'a parent', size=19, weight='bold')
    s.icon('check', w / 2, 0.85, 0.7)
    s.text(w / 2 + 0.6, 0.85, 'says the finding and its limit', size=21, weight='bold', ha='left')
    return s
