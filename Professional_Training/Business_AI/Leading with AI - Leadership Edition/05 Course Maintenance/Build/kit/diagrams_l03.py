"""Figures for Leadership Edition Session 3, Is it any good? Accuracy claims and the cost of mistakes.  Names: x_l03_*  (content kind 'l03_*').

No maths: icon grids, counts, percentages and shillings only.  Demonstration numbers are read from the recorded runs in demo_runs/s03/
(results.json and output_s03_threshold*.txt; scikit-learn 1.9.1; 6 November 2026).  The 3,000 invoices are FICTIONAL (Nile Valley Foods,
a fictional company) and the costs per mistake (UGX 20,000 to chase a flagged invoice, UGX 300,000 for a missed late one, and the 100,000
and 600,000 variants) are assumptions for the lesson.  Transfer, applicant and group counts marked 'illustrative' are invented to teach.
Case figures come from research/*.md (IDs in the content file).
"""
import json
from pathlib import Path

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD, fig
import slidekit as K
from diagrams_l02 import _wrap, _source
from diagrams_l01 import _tiles, people_grid, portfolio_entry

RUN = Path(__file__).resolve().parent.parent / 'demo_runs' / 's03'
_C = {}


def _res():
    if not _C:
        _C.update(json.load(open(RUN / 'results.json')))
    return _C


def _row(r, thr):
    return [x for x in _res()['threshold_table'] if abs(x['threshold'] - thr) < 1e-9][0]


# outcome styles: (edge colour, fill colour)
CAUGHT, MISSED, FALSE, CLEAR = (INK, RED), (RED, PAPER), (INK, GOLD), (GREY, PAPER)


def _grid(s, x0, y0, n_cols, styles, step=0.36, size=0.3):
    """Person icons in rows of n_cols, top-left at (x0, y0), one style per icon."""
    for k, (edge, fill) in enumerate(styles):
        r, c = divmod(k, n_cols)
        s.icon('person', x0 + c * step + step / 2, y0 - r * step - step / 2, size, color=edge, accent=fill)


def _legend(s, x, y, items, gap=0.42, size=14):
    for i, (st, lab) in enumerate(items):
        s.icon('person', x + 0.15, y - i * gap, 0.3, color=st[0], accent=st[1])
        s.text(x + 0.4, y - i * gap, lab, size=size, ha='left')


# ------------------------------------------------------------------ bridge: Session 2 cut-off, today the two mistakes
@fig('x_l03_bridge')
def x_l03_bridge(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.3, 'Session 2: ten applicants, a score each, and a cut-off', size=16, weight='bold', ha='left')
    scores = [9, 9, 8, 8, 7, 6, 5, 4, 3, 2]
    step = (w - 0.4) / 10
    y = h - 1.35
    for i, sc in enumerate(scores):
        x = 0.2 + step * (i + 0.5)
        s.text(x, y + 0.5, f'{sc} in 10', size=14, weight='bold')
        s.icon('person', x, y, 0.5, accent=GOLD if i < 6 else PAPER)
    cut = 0.2 + step * 6
    s.line(cut, y - 0.45, cut, y + 0.32, color=RED, lw=3, dash=True, z=6)
    s.arrow(w / 2, y - 0.6, w / 2, y - 0.95, lw=2.2)
    s.text(0.1, y - 1.3, 'Today: whichever line you draw, it makes two kinds of mistake', size=16, weight='bold', ha='left', color=RED)
    cw = (w - 0.3) / 2
    for i, (hd, tx) in enumerate((('A false alarm', 'Sent to a loan officer, though the person would have repaid'),
                                   ('A miss', 'Approved automatically, and the loan was never repaid'))):
        x = 0.1 + i * (cw + 0.1)
        s.box(x, 0.3, cw, 1.3, '', fill=GOLD if i == 0 else PAPER, edge=INK if i == 0 else RED, lw=2, r=0.08)
        s.text(x + 0.2, 1.3, hd, size=17, weight='bold', ha='left', color=INK if i == 0 else RED)
        _wrap(s, x + 0.2, 0.75, cw - 0.4, tx, 15, ha='left', color=BODY)
    return s


# ------------------------------------------------------------------ hook: Kenya SHA (HLT-05)
@fig('x_l03_sha')
def x_l03_sha(w, h, **_):
    s = Scene(w, h)
    cw = (w - 0.3) / 2
    sides = [('Praised for what it caught', 'check', PAPER, INK,
              ['One parent in Kwale registered with 381 dependants', 'Patients recorded as dialysed up to 10 times a day']),
             ('Blamed for what it wrongly stopped', 'cross', PAPER, RED,
              ['MPs found unjust denials, with too little human oversight', 'One hospital: 8.8% of KSh 10 million in claims rejected for clerical errors'])]
    for i, (hd, ic, fill, edge, items) in enumerate(sides):
        x = 0.1 + i * (cw + 0.1)
        s.box(x, 0.75, cw, h - 0.85, '', fill=fill, edge=edge, lw=2.2, r=0.08)
        s.icon(ic, x + 0.45, h - 0.5, 0.55)
        _wrap(s, x + 0.85, h - 0.5, cw - 1.0, hd, 16, weight='bold', ha='left', color=edge)
        for k, t in enumerate(items):
            _wrap(s, x + 0.25, h - 1.6 - k * 1.3, cw - 0.45, t, 17, ha='left', color=BODY)
    _source(s, 'Capital FM 29 Jan 2026; The Star 15 Oct 2025; HapaKenya 9 Mar 2026.', y=0.3)
    return s


# ------------------------------------------------------------------ two ways to be wrong
@fig('x_l03_four')
def x_l03_four(w, h, **_):
    s = Scene(w, h)
    ml, mt = 1.6, 0.75
    cw, ch = (w - ml - 0.1) / 2, (h - mt - 0.1) / 2
    s.text(ml + cw / 2, h - 0.3, 'Really fraud', size=16, weight='bold')
    s.text(ml + cw * 1.5, h - 0.3, 'Really honest', size=16, weight='bold')
    s.text(0.1, h - mt - ch / 2, 'Flagged', size=16, weight='bold', ha='left')
    s.text(0.1, h - mt - ch * 1.5, 'Let through', size=16, weight='bold', ha='left')
    cells = [(0, 0, CAUGHT, 'Caught', 'true positive', PAPER, INK), (1, 0, FALSE, 'False alarm', 'false positive', GOLD, INK),
             (0, 1, MISSED, 'Miss', 'false negative', PAPER, RED), (1, 1, CLEAR, 'Rightly cleared', 'true negative', PAPER, INK)]
    for c, r, st, hd, term, fill, col in cells:
        x = ml + c * cw
        y = h - mt - (r + 1) * ch
        s.rect(x, y, cw, ch, fill=fill, edge=RED if hd == 'Miss' else INK, lw=2.2 if hd == 'Miss' else 1.6)
        s.icon('person', x + 0.5, y + ch / 2, 0.6, color=st[0], accent=st[1])
        s.text(x + 0.95, y + ch / 2 + 0.2, hd, size=18, weight='bold', ha='left', color=col)
        s.text(x + 0.95, y + ch / 2 - 0.25, term, size=15, ha='left', color=BODY, italic=True)
    return s


# ------------------------------------------------------------------ 100 transfers, 10 frauds (illustrative)
@fig('x_l03_grid100')
def x_l03_grid100(w, h, **_):
    s = Scene(w, h)
    styles = [CAUGHT] * 8 + [MISSED] * 2 + [FALSE] * 16 + [CLEAR] * 74
    s.text(0.1, h - 0.25, '100 mobile-money transfers checked by a fraud tool', size=16, weight='bold', ha='left')
    _grid(s, 0.15, h - 0.45, 10, styles, step=0.37, size=0.32)
    gx = 4.4
    for i, (st, lab) in enumerate([(CAUGHT, '8 frauds caught'), (MISSED, '2 frauds missed'), (FALSE, '16 false alarms'), (CLEAR, '74 honest, let through')]):
        s.icon('person', gx + 0.25, h - 0.75 - i * 0.62, 0.5, color=st[0], accent=st[1])
        s.text(gx + 0.65, h - 0.75 - i * 0.62, lab, size=17, ha='left', weight='bold' if i < 3 else 'normal')
    x = 8.1
    s.box(x, 1.0, w - x - 0.1, h - 1.5, '', fill=GOLD, lw=2, r=0.08)
    _wrap(s, x + (w - x - 0.1) / 2, h - 1.25, w - x - 0.4, 'Caught 8 of 10 frauds', 18, weight='bold')
    _wrap(s, x + (w - x - 0.1) / 2, 1.85, w - x - 0.4, '2 false alarms for every fraud caught', 18, weight='bold', color=RED)
    s.text(w - 0.1, 0.4, 'Illustrative counts', size=14, color=MUTE, ha='right')
    return s


# ------------------------------------------------------------------ rare events: 95% and useless (illustrative)
@fig('x_l03_rare')
def x_l03_rare(w, h, **_):
    s = Scene(w, h)
    styles = [MISSED] * 5 + [CLEAR] * 95
    s.text(0.1, h - 0.25, '100 claims, 5 of them fraud', size=16, weight='bold', ha='left')
    _grid(s, 0.15, h - 0.5, 10, styles, step=0.37, size=0.32)
    x = 4.2
    s.box(x, 1.6, w - x - 0.1, h - 2.0, '', fill=GOLD, lw=2, r=0.08)
    _wrap(s, x + (w - x - 0.1) / 2, h - 0.85, w - x - 0.4, 'A tool that always says “honest”', 16, weight='bold')
    s.text(x + (w - x - 0.1) / 2, h - 1.65, '95% right', size=30, weight='bold')
    _wrap(s, x + (w - x - 0.1) / 2, 2.05, w - x - 0.4, 'and it catches none of the 5', 16, weight='bold', color=RED)
    _legend(s, x + 0.1, 1.15, [(MISSED, 'fraud, missed'), (CLEAR, 'honest')], gap=0.4)
    s.text(w - 0.1, 0.2, 'Illustrative counts', size=14, color=MUTE, ha='right')
    return s


# ------------------------------------------------------------------ two questions in place of accuracy (illustrative)
@fig('x_l03_two_questions')
def x_l03_two_questions(w, h, **_):
    s = Scene(w, h)
    cw = (w - 0.3) / 2
    qs = [('Of the real cases, how many does it catch?', [CAUGHT] * 8 + [MISSED] * 2, 5, '8 of 10', 'The industry calls it recall, or the detection rate'),
          ('Of its alarms, how many are real?', [CAUGHT] * 8 + [FALSE] * 16, 8, '8 of 24', 'The industry calls it precision')]
    for i, (q, styles, cols, big, term) in enumerate(qs):
        x = 0.1 + i * (cw + 0.1)
        s.box(x, 0.1, cw, h - 0.2, '', fill=PAPER, lw=1.8, r=0.08)
        _wrap(s, x + cw / 2, h - 0.55, cw - 0.4, q, 16, weight='bold')
        st = 0.55 if cols == 5 else 0.43
        gw = cols * st
        _grid(s, x + (cw - gw) / 2, h - 1.15, cols, styles, step=st, size=st * 0.85)
        s.text(x + cw / 2, 1.45, big, size=30, weight='bold', color=RED if i else INK)
        _wrap(s, x + cw / 2, 0.65, cw - 0.4, term, 15, color=BODY)
    return s


# ------------------------------------------------------------------ the cut-off is a business dial (illustrative)
@fig('x_l03_dial')
def x_l03_dial(w, h, **_):
    import math
    s = Scene(w, h)
    cx, cy, r = w / 2, h - 2.0, 1.45
    from matplotlib.patches import Wedge
    s.ax.add_patch(Wedge((cx, cy), r, 0, 180, width=0.35, fc=PALE, ec=INK, lw=1.8, zorder=2))
    sets = [(150, 'Strict'), (90, 'Middle'), (30, 'Loose')]
    for ang, lab in sets:
        a = math.radians(ang)
        s.text(cx + (r + 0.35) * math.cos(a), cy + (r + 0.25) * math.sin(a), lab, size=16, weight='bold')
    a = math.radians(90)
    s.arrow(cx, cy, cx + (r - 0.45) * math.cos(a), cy + (r - 0.45) * math.sin(a), color=RED, lw=3, head=18)
    s.circle(cx, cy, 0.1, fill=INK, edge=INK)
    rows = [('Frauds caught, of 10', ['5', '8', '10']), ('False alarms', ['4', '16', '40'])]
    colx = [2.2, 4.0, 5.8]
    for j, (lab, vals) in enumerate(rows):
        y = 1.05 - j * 0.55
        s.text(0.1, y, lab, size=15, weight='bold', ha='left')
        for k, v in enumerate(vals):
            s.text(colx[k] + 0.6, y, v, size=17, weight='bold', color=RED if j == 1 and k == 2 else INK)
    for k, (_, lab) in enumerate(sets):
        s.text(colx[k] + 0.6, 1.55, lab, size=15, color=BODY)
    s.text(w - 0.1, h - 0.2, 'Illustrative counts, 100 transfers', size=14, color=MUTE, ha='right')
    return s


# ------------------------------------------------------------------ price each mistake (demo assumptions)
@fig('x_l03_price')
def x_l03_price(w, h, **_):
    s = Scene(w, h)
    cw = (w - 0.3) / 2
    items = [('One false alarm', 'A credit controller chases an invoice that would have been paid', 'UGX 20,000', GOLD, INK),
             ('One miss', 'A late invoice nobody chased: cash late, some of it lost', 'UGX 300,000', PAPER, RED)]
    for i, (hd, tx, big, fill, edge) in enumerate(items):
        x = 0.1 + i * (cw + 0.1)
        s.box(x, 1.25, cw, h - 1.35, '', fill=fill, edge=edge, lw=2.2, r=0.08)
        s.text(x + 0.2, h - 0.45, hd, size=18, weight='bold', ha='left', color=edge)
        _wrap(s, x + 0.2, h - 1.25, cw - 0.4, tx, 15, ha='left', color=BODY)
        s.text(x + cw / 2, 1.8, big, size=26, weight='bold', color=edge)
    _wrap(s, w / 2, 0.75, w - 0.4, 'Here one miss costs as much as 15 false alarms.', 17, weight='bold', color=RED)
    s.text(w - 0.1, 0.2, 'Costs assumed for the lesson', size=14, color=MUTE, ha='right')
    return s


# ------------------------------------------------------------------ test on unseen cases (recalls of Sessions 1 and 2)
@fig('x_l03_unseen')
def x_l03_unseen(w, h, **_):
    s = Scene(w, h)
    cards = [('On the cases it learned from', 'Flatters', 'Session 2: the unlimited tree got 192 of 192 claims it had seen', PAPER, INK),
             ('On cases kept aside', 'Fair', 'Session 2: the same tree got 42 of 48 claims it never saw', PAPER, INK),
             ('On your own, recent cases', 'The real test', 'Session 1: digits moved one dot fell from 97 in 100 right to 46', GOLD, RED)]
    cw = (w - 0.2 - 2 * 0.15) / 3
    for i, (hd, verdict, tx, fill, col) in enumerate(cards):
        x = 0.1 + i * (cw + 0.15)
        s.box(x, 0.4, cw, h - 0.5, '', fill=fill, lw=2, r=0.08)
        _wrap(s, x + cw / 2, h - 0.6, cw - 0.3, hd, 16, weight='bold')
        s.text(x + cw / 2, h - 1.55, verdict, size=22, weight='bold', color=col)
        _wrap(s, x + cw / 2, 1.5, cw - 0.3, tx, 15, color=BODY)
        if i < 2:
            s.arrow(x + cw + 0.01, h / 2, x + cw + 0.14, h / 2, lw=2, head=12)
    return s


# ------------------------------------------------------------------ bias: errors fall on one group (illustrative + HLT-12)
@fig('x_l03_bias')
def x_l03_bias(w, h, **_):
    s = Scene(w, h)
    groups = [('Group A: 20 honest customers', 1), ('Group B: 20 honest customers', 6)]
    for i, (lab, fa) in enumerate(groups):
        y = h - 0.3 - i * 1.55
        s.text(0.1, y, lab, size=15, weight='bold', ha='left')
        _grid(s, 0.1, y - 0.2, 10, [FALSE] * fa + [CLEAR] * (20 - fa), step=0.3, size=0.26)
        s.text(3.25, y - 0.7, f'{fa} false alarm' + ('s' if fa > 1 else ''), size=16, weight='bold', ha='left', color=RED if fa > 1 else INK)
    s.text(0.1, 0.55, 'Same tool, one overall score;', size=15, ha='left', color=BODY)
    s.text(0.1, 0.25, 'one group carries most mistakes. Illustrative.', size=15, ha='left', color=BODY)
    x = 5.0
    s.box(x, 0.45, w - x - 0.1, h - 0.55, '', fill=PAPER, edge=RED, lw=2.2, r=0.08)
    s.text(x + 0.15, h - 0.4, 'Optum, USA, 2019', size=16, weight='bold', color=RED, ha='left')
    _wrap(s, x + 0.15, h - 0.65, w - x - 0.4, 'It ranked patients for extra care by predicted cost. Black patients were 17.7% of the top group; ranked by illness, 46.5%.', 14, ha='left', va='top', color=BODY)
    _wrap(s, x + 0.15, (h + 1.2) / 2, w - x - 0.4, 'Why: less had been spent on Black patients, so cost made them look healthier.', 14, ha='left', va='top', color=RED)
    _wrap(s, x + 0.15, 1.55, w - x - 0.4, 'Retrained with health measures, the gap shrank by 84%.', 14, weight='bold', ha='left', va='top')
    s.text(x + 0.15, 0.65, 'Science News, 24 Oct 2019', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ industry tour
@fig('x_l03_six')
def x_l03_six(w, h, **_):
    s = Scene(w, h)
    tiles = [('calculator', 'Banking and microfinance', 'Blocked most attempted fraud; the AI’s share unknown', 'Four Nigerian banks'),
             ('phone', 'Telecom and mobile money', 'Spam alerts on SMS; fraud cases fell 56% in Tanzania', 'Airtel Africa'),
             ('plant', 'Agriculture and agribusiness', '74 to 88% right on six leaves, 49% on one', 'PlantVillage Nuru'),
             ('bottle', 'Manufacturing and FMCG', 'Typical use: a camera rejects faulty bottles; false rejects are waste', 'No published case yet'),
             ('clinic', 'Healthcare and insurance', 'Caught 96 in 100 abnormal smears, more false alarms', 'Kinondo Kwetu, Kenya'),
             ('people', 'Public sector', 'A results model marked down 39% of teacher assessments, then was dropped', 'Ofqual, England, 2020')]
    _tiles(s, w, h, tiles, 'Sources: BusinessDay 2026; The Citizen 2025; Frontiers 2020; JAMA Network Open 2021; Tes 2020.')
    return s


# ------------------------------------------------------------------ demonstration: three ways to flag invoices (recorded)
@fig('x_l03_baselines')
def x_l03_baselines(w, h, **_):
    r = _res()
    n, late = r['n_test'], r['late_test']
    m = _row(r, 0.2)
    cols = [('Do nothing', 'say “on time” to all', 0, 0, round(r['always_no']['accuracy'] * n)),
            ('A simple rule', 'flag anyone late before', r['rule']['tp'], r['rule']['fp'], round(r['rule']['accuracy'] * n)),
            ('The model', 'flag at 20% risk or more', m['tp'], m['fp'], round(m['accuracy'] * n))]
    s = Scene(w, h)
    cw = (w - 0.2 - 2 * 0.15) / 3
    for i, (hd, sub, tp, fp, right) in enumerate(cols):
        x = 0.1 + i * (cw + 0.15)
        s_fill = GOLD if i == 2 else PAPER
        s.box(x, 0.55, cw, h - 0.65, '', fill=s_fill, lw=2, r=0.08)
        s.text(x + cw / 2, h - 0.4, hd, size=18, weight='bold')
        s.text(x + cw / 2, h - 0.78, sub, size=14, color=BODY)
        for k, (lab, val, col) in enumerate((('late ones caught', f'{tp} of {late}', RED if tp == 0 else INK),
                                             ('false alarms', f'{fp}', RED if fp > 100 else INK),
                                             ('right overall', f'{round(right / n * 100)} in 100', INK))):
            y = h - 1.45 - k * 0.95
            s.text(x + cw / 2, y, val, size=22, weight='bold', color=col)
            s.text(x + cw / 2, y - 0.38, lab, size=14, color=BODY)
    s.text(0.1, 0.25, f'{n} invoices it never saw, {late} paid late. Recorded run, 6 Nov 2026; fictional data.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ demonstration: turning the dial (recorded)
@fig('x_l03_dial_run')
def x_l03_dial_run(w, h, **_):
    r = _res()
    late = r['late_test']
    rows = r['threshold_table']
    s = Scene(w, h)
    lab_w = 2.6
    cx0, cw_ = lab_w + 0.2, 3.6
    fx0, fw_ = cx0 + cw_ + 1.6, 3.0
    s.text(0.1, h - 0.25, 'Flag when risk is', size=15, weight='bold', ha='left')
    s.text(cx0, h - 0.25, f'Late invoices caught, of {late}', size=15, weight='bold', ha='left', color=RED)
    s.text(fx0, h - 0.25, 'False alarms', size=15, weight='bold', ha='left')
    rh = (h - 0.8) / len(rows)
    fmax = max(x['fp'] for x in rows)
    for i, x in enumerate(rows):
        y = h - 0.6 - (i + 0.5) * rh
        s.text(0.1, y, f'{round(x["threshold"] * 100)}% or more', size=16, ha='left', weight='bold' if i in (0, len(rows) - 1) else 'normal')
        s.rect(cx0, y - 0.15, cw_, 0.3, fill=PAPER, edge=HAIR, lw=1)
        s.rect(cx0, y - 0.15, cw_ * x['tp'] / late, 0.3, fill=RED, edge=INK, lw=1, z=3)
        s.text(cx0 + cw_ + 0.1, y, f'{x["tp"]}', size=16, weight='bold', ha='left')
        s.rect(fx0, y - 0.15, max(0.02, fw_ * x['fp'] / fmax), 0.3, fill=GOLD, edge=INK, lw=1, z=3)
        s.text(fx0 + fw_ * x['fp'] / fmax + 0.1, y, f'{x["fp"]}', size=16, weight='bold', ha='left')
    s.text(w - 0.1, 0.12, 'Recorded run, 6 Nov 2026; 900 fictional invoices', size=14, color=MUTE, ha='right')
    return s


# ------------------------------------------------------------------ demonstration: the price of each setting (recorded)
def _cost_bars(s, x0, y0, bw_max, bh, gap, items, unit=1e6, size=15):
    vmax = max(v for _, v in items)
    vmin = min(v for _, v in items)
    for i, (lab, v) in enumerate(items):
        y = y0 - i * (bh + gap)
        s.text(x0 - 0.1, y + bh / 2, lab, size=size, ha='right', weight='bold' if v == vmin else 'normal')
        s.rect(x0, y, bw_max * v / vmax, bh, fill=GOLD if v == vmin else PAPER, edge=INK, lw=1.2)
        s.text(x0 + bw_max * v / vmax + 0.08, y + bh / 2, f'{v / unit:.1f}m', size=size, ha='left', weight='bold' if v == vmin else 'normal')


@fig('x_l03_cost_run')
def x_l03_cost_run(w, h, **_):
    r = _res()
    s = Scene(w, h)
    items = [('Never flag', r['cost_never_flag_ugx'])] + [(f'{round(x["threshold"] * 100)}% or more', x['cost_ugx']) for x in r['threshold_table']]
    s.text(0.1, h - 0.25, 'Cost of all the mistakes, UGX, on 900 invoices', size=15, weight='bold', ha='left')
    _cost_bars(s, 1.85, h - 0.95, 4.6, 0.4, 0.13, items)
    s.text(0.1, 0.2, 'Assumed: UGX 20,000 per check, UGX 300,000 per miss. Recorded run, 6 Nov 2026.', size=14, color=MUTE, ha='left')
    return s


@fig('x_l03_flip')
def x_l03_flip(w, h, **_):
    s = Scene(w, h)
    sets = [('A miss costs UGX 100,000', [7880000, 6840000, 11020000]),
            ('A miss costs UGX 300,000', [23280000, 16440000, 12020000]),
            ('A miss costs UGX 600,000', [46380000, 30840000, 13520000])]
    labs = ['50%', '20%', '5%']
    ph = (h - 0.5) / 3
    for i, (hd, vals) in enumerate(sets):
        top = h - 0.1 - i * ph
        s.text(0.1, top - 0.2, hd, size=15, weight='bold', ha='left', color=RED if i != 1 else INK)
        _cost_bars(s, 0.75, top - 0.65, 5.5, 0.27, 0.06, list(zip(labs, vals)), size=14)
    s.text(0.1, 0.18, 'Gold: cheapest of the three settings run. Output files, 6 Nov 2026.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ demonstration: a model that memorised (recorded)
@fig('x_l03_memorise')
def x_l03_memorise(w, h, **_):
    r = _res()
    s = Scene(w, h)
    base = round(r['always_no']['accuracy'] * 100)
    pairs = [('A simple tree', round(r['small_tree']['train_acc'] * 100), round(r['small_tree']['test_acc'] * 100)),
             ('A tree with no limit', round(r['deep_tree']['train_acc'] * 100), round(r['deep_tree']['test_acc'] * 100))]
    y0, y1 = 0.95, h - 0.75
    py = lambda v: y0 + (y1 - y0) * (v - 70) / 30
    s.line(0.5, y0, w - 0.1, y0, lw=2)
    s.text(0.1, h - 0.25, 'Right, out of 100 invoices', size=15, weight='bold', ha='left')
    bw = 1.1
    for i, (lab, tr, te) in enumerate(pairs):
        cx = 2.0 + i * 3.6
        for k, (v, sub, fill) in enumerate(((tr, 'invoices it learned from', PAPER), (te, 'invoices it never saw', GOLD))):
            x = cx - bw - 0.05 + k * (bw + 0.1)
            s.rect(x, y0, bw, py(v) - y0, fill=fill, edge=INK, lw=1.4)
            s.text(x + bw / 2, py(v) + 0.2, str(v), size=17, weight='bold', color=RED if (i == 1 and k == 1) else INK, bbox=dict(fc=PAPER, ec='none', pad=1))
        s.text(cx, 0.6, lab, size=16, weight='bold')
    s.line(0.5, py(base), w - 0.1, py(base), color=RED, lw=2, dash=True, z=5)
    s.text(w - 0.1, py(base) + 0.42, f'Do nothing: {base}', size=15, color=RED, ha='right', weight='bold')
    s.rect(0.5, 0.12, 0.25, 0.22, fill=PAPER, edge=INK, lw=1.2)
    s.text(0.85, 0.23, 'learned from', size=14, ha='left')
    s.rect(2.4, 0.12, 0.25, 0.22, fill=GOLD, edge=INK, lw=1.2)
    s.text(2.75, 0.23, 'never saw', size=14, ha='left')
    s.text(w - 0.1, 0.23, 'Scale starts at 70', size=14, color=MUTE, ha='right')
    return s


# ------------------------------------------------------------------ your people
@fig('x_l03_people')
def x_l03_people(w, h, **_):
    s = Scene(w, h)
    roles = [('Fraud or credit analyst', ['Reviewing every case by hand', 'Reviewing what the tool flags', 'Reading the two numbers, catches and alarms', 'Fear: drowned in alarms. Gain: fewer misses']),
             ('Claims or service officer', ['Hunting for problems', 'Calling customers wrongly flagged', 'Explaining a flag, and fixing it fast', 'Fear: the angry customer. Gain: faster clean claims']),
             ('Manager who sets the dial', ['Guessing how strict to be', 'Pricing each kind of mistake', 'Reading a vendor’s accuracy claim', 'Fear: blamed for a miss. Gain: a reasoned setting'])]
    people_grid(s, w, h, roles)
    return s


# ------------------------------------------------------------------ the customer wrongly flagged (BNK-13, HLT-05)
@fig('x_l03_customer')
def x_l03_customer(w, h, **_):
    s = Scene(w, h)
    boxes = [('Apple Card, USA, 2019 to 2021', ['Viral complaints said women got lower credit limits.', 'The regulator checked about 400,000 applicants and found no unlawful bias.', 'It criticised poor service and a lack of transparency.'], 'Banking Dive, 24 Mar 2021'),
             ('One Kenyan hospital, 2026', ['8.8% of KSh 10 million in claims was rejected for clerical errors.', 'There was no way to resubmit.', 'Reported by the Kenya Medical Association president.'], 'HapaKenya, 9 Mar 2026')]
    cw = (w - 0.3) / 2
    for i, (hd, lines, src) in enumerate(boxes):
        x = 0.1 + i * (cw + 0.1)
        s.box(x, 0.95, cw, h - 1.05, '', fill=PAPER, edge=RED if i else INK, lw=2, r=0.08)
        s.text(x + 0.15, h - 0.35, hd, size=15, weight='bold', ha='left', color=RED if i else INK)
        top = h - 0.65
        for t in lines:
            top -= _wrap(s, x + 0.15, top, cw - 0.3, t, 14, ha='left', va='top', color=BODY) + 0.15
        s.text(x + 0.15, 1.15, src, size=14, color=MUTE, ha='left')
    _wrap(s, w / 2, 0.45, w - 0.3, 'Name who explains a flag, who corrects it, and how fast.', 16, weight='bold', color=RED)
    return s


# ------------------------------------------------------------------ hands-on: a portfolio entry with the cost of a mistake
@fig('x_l03_portfolio')
def x_l03_portfolio(w, h, **_):
    s = Scene(w, h)
    rows = [('The use', 'Flag invoices likely to be paid late'),
            ('What comes out', 'A weekly list for credit control'),
            ('Who uses it', 'Credit controllers'),
            ('How we would know it works', 'Late ones caught, and false alarms, on unseen invoices'),
            ('Cost of a false alarm', 'A call to a good customer: about UGX 20,000'),
            ('Cost of a miss', 'Cash late or lost: about UGX 300,000')]
    portfolio_entry(s, w, h, rows, gold_last=2)
    return s
