"""DA figures, part E: sessions 19 to 24 (project plan, reliable analysis, chart report, handover, talk, showcase)."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from figs_da_util import (SUN, Scene, fig, Chart, chart, sales, products, daily, money, fmt_axis_money, clean_pipeline, INK, BODY, MUTE, GREY, HAIR, PAPER, RED,
                          GOLD)
import figkit


def _sugar():
    su = sales()
    sg = su[su['product_id'] == 14]
    return sg.groupby('unit_price_ugx')['units'].mean()


# ------------------------------------------------------------------ session 19
@fig('da_hero_plan')
def da_hero_plan(w, h, **_):
    s = Scene(w, h)
    cards = [('Which category earns\nthe most at each branch?', 'sales + products + branches', True, 'columns exist, one merge'),
             ('Which shop earns the most\nfor each customer counted?', 'sales + daily summary', True, 'columns exist, one division'),
             ('Why do people like\nCampus Gate?', 'no column holds opinions', False, 'the data cannot answer it')]
    cw = (w - 0.4 - 2 * 0.3) / 3
    for i, (q, need, ok, note) in enumerate(cards):
        x = 0.2 + i * (cw + 0.3)
        s.box(x, 0.3, cw, h - 0.6, '', fill=PAPER, lw=2.0, r=0.06, edge=INK if ok else RED)
        s.text(x + cw / 2 - 0.0, h - 1.15, q, size=19, weight='bold', va='center')
        s.text(x + 0.2, h - 2.15, 'needs', size=16, color=MUTE, ha='left')
        s.text(x + 0.2, h - 2.55, need, size=17, ha='left')
        s.icon('check' if ok else 'cross', x + cw / 2, 1.4, 0.75)
        s.text(x + cw / 2, 0.7, note, size=17, color=BODY if ok else RED, weight='bold')
    return s


@fig('da_question_ladder')
def da_question_ladder(w, h, **_):
    s = Scene(w, h)
    lo, hi = _sugar()[4500], _sugar()[5000]
    steps = [('topic', 'the Sugar price rise'), ('question', 'Did the rise change units sold?'), ('columns', 'product_id, units, unit_price_ugx'),
             ('method', 'average units per sale at each price'), ('chart', f'{lo:.2f} before, {hi:.2f} after')]
    for i, (a, b) in enumerate(steps):
        y = h - 0.5 - i * 0.92
        s.box(0.2, y - 0.38, 1.55, 0.76, a, size=18, weight='bold', fill=GOLD if i == 1 else PAPER, r=0.05)
        s.text(1.95, y, b, size=19, ha='left')
        if i < len(steps) - 1:
            s.arrow(0.97, y - 0.4, 0.97, y - 0.52, color=RED, lw=2.2, head=12)
    return s


@fig('da_plan_page')
def da_plan_page(w, h, **_):
    s = Scene(w, h)
    heads = [('question', 'Did the Sugar price rise change units?'), ('reader and use', 'the shop owner, deciding the price'),
             ('data and licence', 'Sunrise Shops, invented data'), ('measures and columns', 'units, unit_price_ugx, sale_date'),
             ('method', 'average units before and after day 31'), ('charts', 'two bars with labelled axes'), ('limitations', 'invented data, no costs, one product')]
    s.box(0.15, 0.1, w - 0.3, h - 0.2, '', fill=PAPER, lw=1.8, r=0.03)
    s.text(0.4, h - 0.4, 'PROJECT_PLAN.md', size=17, mono=True, weight='bold', ha='left')
    for i, (a, b) in enumerate(heads):
        y = h - 0.95 - i * 0.58
        s.text(0.4, y, a, size=17, weight='bold', ha='left')
        s.text(3.05, y, b, size=17, ha='left', color=BODY)
        s.line(0.4, y - 0.29, w - 0.4, y - 0.29, color=HAIR, lw=1)
    return s


@fig('da_data_dictionary_card')
def da_data_dictionary_card(w, h, **_):
    s = Scene(w, h)
    rows = [['column', 'what it holds', 'unit'], ['sale_date', 'the day of the sale', 'YYYY-MM-DD'], ['product_id', 'which product', 'whole number'],
            ['units', 'items in the sale', 'whole number'], ['unit_price_ugx', 'price of one item', 'UGX']]
    s.table(0.15, h - 0.6, [2.15, 2.9, 1.9], 0.62, rows, size=16, align=['left', 'left', 'left'], mono_cols=(0,))
    s.text(0.15, h - 0.3, 'data dictionary', size=19, weight='bold', ha='left')
    s.text(0.15, 0.95, 'Every column you use: what it holds and its unit.', size=19, ha='left', color=BODY)
    s.text(0.15, 0.45, 'A reader who has never seen the file can follow your work.', size=19, ha='left', color=BODY)
    return s


@fig('da_licence_check')
def da_licence_check(w, h, **_):
    s = Scene(w, h)
    steps = [('Read the licence', 'at the source, on the owner\'s page', 'magnifier'), ('Instructor approves', 'before you build anything', 'person'),
             ('No personal details', 'no names, phones or ID numbers', 'check'), ('Say where it came from', 'a source note in the report', 'notebook')]
    for i, (a, b, ic) in enumerate(steps):
        y = h - 0.7 - i * 1.15
        s.icon(ic, 0.7, y, 0.75)
        s.text(1.5, y + 0.15, a, size=21, weight='bold', ha='left')
        s.text(1.5, y - 0.28, b, size=17, color=BODY, ha='left')
    return s


@fig('da_ai_log_card')
def da_ai_log_card(w, h, **_):
    s = Scene(w, h)
    rows = [['AI_USE_LOG.md', 'what you write'], ['date and tool', 'or: teacher demonstration'], ['your first attempt', 'saved before any help'], ['the question you asked', 'and the reply'],
            ['accepted or rejected', 'and why'], ['the test you ran', 'and its result']]
    s.table(0.15, h - 0.3, [2.9, 3.2], 0.56, rows, size=17, align=['left', 'left'], mono_cols=())
    s.text(0.15, 0.95, 'No help used? Write: No AI assistance used.', size=19, weight='bold', ha='left')
    s.text(0.15, 0.45, 'The log is evidence that you checked, not a reward for using AI.', size=18, ha='left', color=BODY)
    return s


# ------------------------------------------------------------------ session 20
@fig('da_hero_reliable')
def da_hero_reliable(w, h, **_):
    s = Scene(w, h)
    clean, excluded, steps = clean_pipeline()
    nodes = [('raw file', 'folder'), ('cleaning log', 'notebook'), ('calculation', 'calculator'), ('check', 'magnifier'), ('number in\nthe report', 'receipt')]
    n = len(nodes)
    gap = (w - 1.8) / (n - 1)
    y = h - 1.9
    for i, (lab, ic) in enumerate(nodes):
        x = 0.9 + i * gap
        s.icon(ic, x, y, 1.15)
        s.text(x, y - 1.0, lab, size=19, weight='bold')
        if i < n - 1:
            s.arrow(x + 0.75, y, x + gap - 0.75, y, color=RED, lw=2.6)
    s.icon('person', w / 2, 0.9, 0.7)
    s.text(w / 2 + 0.7, 0.9, 'a stranger can follow every arrow', size=20, ha='left', weight='bold')
    return s


@fig('da_hand_check')
def da_hand_check(w, h, **_):
    s = Scene(w, h)
    d = sales().head(5)
    rows = [['sale', 'units', '×', 'price', '=', 'by hand']] + [[str(r.sale_id), str(r.units), '×', str(r.unit_price_ugx), '=', money(r.line_value)] for r in d.itertuples()]
    s.table(0.15, h - 0.25, [0.8, 0.9, 0.4, 1.0, 0.4, 1.4], 0.46, rows, size=16, hl_cols=(5,))
    tot = int(d['line_value'].sum())
    s.text(0.15, 1.6, f'by hand, the five add to {money(tot)}', size=19, weight='bold', ha='left')
    s.code(0.15, 1.35, ['sales.head(5)["line_value"].sum()'], size=14, line_h=0.4, w=4.3)
    s.text(4.6, 0.85, f'→ {money(tot)}', size=20, weight='bold', ha='left')
    s.icon('check', 6.5, 0.85, 0.7)
    s.text(0.15, 0.22, 'Hand and code agree on five rows, so we trust the code on 1,513.', size=16, ha='left', color=BODY)
    return s


@fig('da_second_route')
def da_second_route(w, h, **_):
    s = Scene(w, h)
    su = sales()
    by = su.groupby('branch')['line_value'].sum()
    total = int(su['line_value'].sum())
    s.text(0.3, h - 0.5, 'Route one: add the three branch totals', size=19, weight='bold', ha='left')
    xs = [0.3, 2.05, 3.8]
    for i, (b_, v) in enumerate(by.items()):
        s.box(xs[i], h - 1.65, 1.6, 0.7, money(v), size=18, r=0.05)
        s.text(xs[i] + 0.8, h - 1.9, b_, size=15, color=MUTE)
    s.text(5.55, h - 1.3, '= ' + money(sum(by.values)), size=20, weight='bold', ha='left')
    s.line(0.3, h - 2.5, w - 0.3, h - 2.5, color=HAIR, lw=1.2)
    s.text(0.3, h - 3.0, 'Route two: add every sale at once', size=19, weight='bold', ha='left')
    s.code(0.3, h - 3.3, ['sales["line_value"].sum()'], size=15, line_h=0.4, w=3.7)
    s.text(4.3, h - 3.65, '= ' + money(total), size=20, weight='bold', ha='left')
    s.icon('check', 1.0, 0.55, 0.65)
    s.text(1.55, 0.55, 'the two routes agree', size=19, weight='bold', ha='left')
    return s


@fig('da_partner_rerun')
def da_partner_rerun(w, h, **_):
    s = Scene(w, h)
    s.icon('person', 0.8, h - 1.0, 0.8)
    s.text(0.8, h - 1.8, 'you', size=19, weight='bold')
    s.icon('person', w - 0.8, h - 1.0, 0.8)
    s.text(w - 0.8, h - 1.8, 'partner', size=19, weight='bold')
    s.arrow(1.6, h - 1.0, w - 1.7, h - 1.0, color=INK, lw=2.4)
    s.text(w / 2, h - 0.6, 'notebook and data file', size=17)
    s.box(w / 2 - 1.7, h - 3.0, 3.4, 0.75, 'restart, run all', size=20, weight='bold', r=0.05)
    s.arrow(w - 1.0, h - 2.05, w / 2 + 1.7, h - 2.5, color=RED, lw=2.2)
    s.box(0.3, 0.25, 3.2, 0.85, 'same numbers', size=19, weight='bold', fill=GOLD, r=0.05)
    s.box(w - 3.5, 0.25, 3.2, 0.85, 'a different number:\nfix the first cell\nthat differs', size=15, weight='bold', edge=RED, lw=2.4, r=0.05)
    s.arrow(w / 2 - 0.8, h - 3.05, 1.9, 1.2, color=INK, lw=2)
    s.arrow(w / 2 + 0.8, h - 3.05, w - 1.9, 1.2, color=RED, lw=2)
    return s


@fig('da_cleaning_log_card')
def da_cleaning_log_card(w, h, **_):
    s = Scene(w, h)
    su = pd.read_csv(SUN / 'sales.csv')
    miss = int(su.isna().sum().sum())
    dups = int(su.duplicated().sum())
    rows = [['check', 'rows', 'what we did'], ['missing values', str(miss), 'none found: no change'], ['duplicate rows', str(dups), 'none found: no change'],
            ['rows read', f'{len(su):,}', 'raw file kept as it came']]
    s.text(0.15, h - 0.3, 'cleaning_log.md', size=19, weight='bold', ha='left', mono=True)
    s.table(0.15, h - 0.6, [2.4, 1.0, 3.5], 0.62, rows, size=17, align=['left', 'center', 'left'])
    s.text(0.15, 1.2, '"No change needed" is a finding.', size=20, weight='bold', ha='left')
    s.text(0.15, 0.65, 'Write the check and its count even when nothing needed fixing.', size=18, ha='left', color=BODY)
    return s


# ------------------------------------------------------------------ session 21
@fig('da_report_anatomy')
def da_report_anatomy(w, h, **_):
    s = Scene(w, h)
    by = sales().groupby('branch')['line_value'].sum().sort_values(ascending=False)
    px, pw = 0.2, 3.5
    s.box(px, 0.15, pw, h - 0.3, '', fill=PAPER, lw=2.0, r=0.02)
    s.text(px + 0.2, h - 0.5, 'Revenue by branch', size=17, weight='bold', ha='left')
    for i, (b, v) in enumerate(by.items()):
        s.rect(px + 0.35 + i * 1.0, 1.65, 0.8, 1.9 * v / by.max(), fill=GOLD if i == 0 else PAPER, edge=INK, lw=1.6)
    s.line(px + 0.3, 1.65, px + pw - 0.3, 1.65, color=INK, lw=1.8)
    s.text(px + 0.2, 1.4, 'two findings, two sentences', size=14, ha='left')
    s.text(px + 0.2, 0.95, 'one limitation', size=14, ha='left')
    s.text(px + 0.2, 0.45, 'source: invented data', size=14, ha='left', color=MUTE)
    labels = [('title says what is shown', h - 0.5), ('one chart, axes\nlabelled with units', h - 1.9), ('findings with evidence', 1.4), ('limitation in plain words', 0.95), ('data source note', 0.45)]
    for t, y in labels:
        s.text(px + pw + 0.85, y, t, size=16, weight='bold', ha='left', color=RED)
        s.arrow(px + pw + 0.8, y, px + pw - 0.15, y, color=RED, lw=2, head=12)
    return s


@fig('da_30_second_test')
def da_30_second_test(w, h, **_):
    s = Scene(w, h)
    by = sales().groupby('branch')['line_value'].sum().sort_values(ascending=False)
    s.icon('person', 0.8, h - 1.2, 0.8)
    s.text(0.8, h - 1.95, 'a peer', size=18, weight='bold')
    s.icon('clock', 2.5, h - 1.2, 0.9)
    s.text(2.5, h - 1.95, '30 seconds', size=18, weight='bold')
    s.arrow(3.15, h - 1.2, 4.1, h - 1.2, color=INK, lw=2.4)
    s.box(4.2, h - 1.7, 3.2, 1.0, f'{by.index[0]}\n{money(by.iloc[0])}', size=18, fill=GOLD, weight='bold', r=0.05)
    s.text(5.8, h - 2.0, 'the largest bar and its total', size=16, color=MUTE)
    s.line(0.3, h - 2.55, w - 0.3, h - 2.55, color=HAIR, lw=1.2)
    s.text(0.3, h - 3.05, 'Peer found it fast?  Keep the headings.', size=19, ha='left', weight='bold')
    s.text(0.3, h - 3.6, 'Peer hesitated?  Write down where, and', size=19, ha='left', weight='bold', color=RED)
    s.text(0.3, h - 4.1, 'change that heading or label.', size=19, ha='left', weight='bold', color=RED)
    return s


@fig('da_savefig_flow')
def da_savefig_flow(w, h, **_):
    s = Scene(w, h)
    s.text(0.3, h - 0.4, 'Right order', size=20, weight='bold', ha='left')
    s.code(0.3, h - 0.65, ['plt.bar(by.index, by.values)', 'plt.savefig("revenue.png", bbox_inches="tight")', 'plt.show()'], size=14, line_h=0.38, w=6.6)
    s.icon('check', 7.0, h - 1.4, 0.55)
    s.line(0.3, h - 2.3, w - 0.3, h - 2.3, color=HAIR, lw=1.2)
    s.text(0.3, h - 2.7, 'Wrong order: a blank picture', size=20, weight='bold', ha='left', color=RED)
    s.code(0.3, h - 2.95, ['plt.bar(by.index, by.values)', 'plt.show()', 'plt.savefig("revenue.png", bbox_inches="tight")'], size=14, line_h=0.38, w=6.6, hl_lines=(2,))
    s.icon('cross', 7.0, h - 3.7, 0.55)
    s.text(0.3, 0.3, 'show clears the figure, so save first. tight keeps the labels in.', size=17, ha='left', color=BODY)
    return s


@fig('da_ai_critique_loop')
def da_ai_critique_loop(w, h, **_):
    s = Scene(w, h)
    nodes = [('Your own attempt first', 'notebook'), ('Ask for a hint, not an answer', 'magnifier'), ('Predict, run, test it', 'calculator'), ('Keep or reject, and say why', 'check')]
    for i, (lab, ic) in enumerate(nodes):
        y = h - 0.7 - i * 1.05
        s.icon(ic, 0.9, y, 0.6)
        s.text(1.5, y, lab, size=19, ha='left', weight='bold')
        if i < 3:
            s.arrow(0.9, y - 0.36, 0.9, y - 0.7, color=RED, lw=2.4)
    s.text(0.3, 0.4, 'Write each turn in AI_USE_LOG.md. You explain every line you keep.', size=15, color=BODY, ha='left')
    return s


# ------------------------------------------------------------------ session 22
@fig('da_hero_handover')
def da_hero_handover(w, h, **_):
    s = Scene(w, h)
    files = [('project.ipynb', 'notebook'), ('cleaning_log.md', 'receipt'), ('data dictionary', 'tag'), ('report.pdf', 'book'), ('AI_USE_LOG.md', 'pen')]
    n = len(files)
    gap = (w - 0.6) / n
    s.icon('folder', 0.9, h - 0.9, 1.2)
    s.text(1.75, h - 0.9, 'my project folder', size=22, weight='bold', ha='left')
    for i, (lab, ic) in enumerate(files):
        x = 0.3 + gap / 2 + i * gap
        s.box(x - gap / 2 + 0.1, 0.7, gap - 0.2, 2.3, '', fill=PAPER, lw=1.8, r=0.05)
        s.icon(ic, x, 2.15, 0.9)
        s.text(x, 1.2, lab, size=16.5, weight='bold')
    s.text(w / 2, 0.3, 'Each file opens, reruns and agrees with the others.', size=19, color=BODY)
    return s


@fig('da_handover_checklist')
def da_handover_checklist(w, h, **_):
    s = Scene(w, h)
    items = ['notebook reruns from a restarted kernel', 'every number in the report is in an output', 'cleaning log counts each row removed',
             'data dictionary covers every column used', 'AI log filled in, or No AI assistance used', 'every file opens after you reopen it']
    for i, t in enumerate(items):
        y = h - 0.55 - i * 0.78
        s.icon('check', 0.5, y, 0.58)
        s.text(1.0, y, t, size=19, ha='left')
    return s


@fig('da_report_page')
def da_report_page(w, h, **_):
    s = Scene(w, h)
    su = sales()
    by = su.groupby('branch')['line_value'].sum().sort_values(ascending=False)
    total = int(su['line_value'].sum())
    s.box(0.2, 0.1, w - 0.4, h - 0.2, '', fill=PAPER, lw=2.0, r=0.02)
    rows = [('question', 'Which shop earns the most?'), ('data', 'Sunrise Shops sales, invented, 60 days, 1,513 rows'), ('method', 'total each shop, check against the grand total'),
            ('finding', f'{by.index[0]} earns {money(by.iloc[0])} of {money(total)}'), ('finding', f'{by.index[-1]} earns the least, {money(by.iloc[-1])}'),
            ('recommend', 'compare cost per shop before any decision'), ('limit', 'no costs, so no profit; data is invented')]
    for i, (a, b) in enumerate(rows):
        y = h - 0.5 - i * 0.62
        s.text(0.45, y, a, size=16, weight='bold', ha='left', color=RED if a == 'limit' else INK)
        s.text(2.0, y, b, size=16, ha='left')
    return s


@fig('da_submit_route')
def da_submit_route(w, h, **_):
    s = Scene(w, h)
    steps = [('Save', 'notebook'), ('Export\nPDF', 'book'), ('Reopen\nboth', 'magnifier'), ('Upload', 'folder'), ('Keep the\nconfirmation', 'receipt')]
    n = len(steps)
    gap = (w - 0.4) / n
    for i, (lab, ic) in enumerate(steps):
        x = 0.2 + gap / 2 + i * gap
        s.icon(ic, x, h - 1.3, 0.95)
        s.text(x, h - 2.35, lab, size=18, weight='bold')
        if i < n - 1:
            s.arrow(x + 0.65, h - 1.3, x + gap - 0.65, h - 1.3, color=RED, lw=2.4, head=13)
    s.text(w / 2, 0.9, 'A file on your laptop has not been submitted.', size=21, weight='bold', color=RED)
    s.text(w / 2, 0.4, 'It is submitted when the confirmation arrives.', size=19, color=BODY)
    return s


# ------------------------------------------------------------------ session 23
@fig('da_talk_storyboard')
def da_talk_storyboard(w, h, **_):
    s = Scene(w, h)
    su = sales()
    by = su.groupby('branch')['line_value'].sum().sort_values(ascending=False)
    frames = [('My question', 'Which shop\nearns the most?'), ('My data', '1,513 sales,\n3 shops, 60 days,\ninvented'), ('What I did', 'cleaned, merged,\nadded up,\nchecked'),
              ('What I found', f'{by.index[0]}: {money(by.iloc[0])}'), ('What it cannot show', 'costs, so\nno profit')]
    n = 5
    fw = (w - 0.4 - 4 * 0.2) / n
    for i, (a, b) in enumerate(frames):
        x = 0.2 + i * (fw + 0.2)
        s.box(x, 0.9, fw, h - 1.6, '', fill=PAPER, lw=1.8, r=0.04)
        s.text(x + fw / 2, h - 1.15, a.replace('What it cannot show', 'What it cannot\nshow'), size=18, weight='bold')
        if i == 3:
            for k, v in enumerate(by.values):
                s.rect(x + 0.3 + k * 0.62, 1.7, 0.5, 1.4 * v / by.max(), fill=GOLD if k == 0 else PAPER, edge=INK, lw=1.4)
            s.text(x + fw / 2, 1.25, b.replace(': ', '\n'), size=15)
        else:
            s.text(x + fw / 2, h / 2 - 0.1, b, size=17, va='center')
    s.text(w / 2, 0.4, 'One idea on each slide. A parent can say what was found and what it cannot show.', size=18, color=BODY)
    return s


@fig('da_talk_timeline')
def da_talk_timeline(w, h, **_):
    s = Scene(w, h)
    parts = [('question', 0.5), ('data', 0.5), ('what I did', 1.0), ('finding', 2.0), ('limit and next step', 1.0), ('questions', 3.0)]
    total = sum(m for _, m in parts)
    x0, sc = 0.2, (w - 0.4) / total
    t = 0
    for i, (lab, m) in enumerate(parts):
        bw = m * sc
        last = i == len(parts) - 1
        s.box(x0 + t * sc, h - 2.0, bw, 1.0, '', fill=GOLD if i == 3 else (PAPER if last else INK), edge=INK if (last or i == 3) else PAPER, lw=1.8, r=0.02)
        s.text(x0 + t * sc + bw / 2, h - 2.0 - 0.35 - (i % 2) * 0.45, lab, size=16, color=INK)
        t += m
    s.text(x0, h - 0.6, 'The five minutes', size=22, weight='bold', ha='left')
    s.text(x0 + 2.5 * sc, h - 0.85, '5 minutes of talking', size=17, color=BODY)
    s.text(x0 + 6.5 * sc, h - 0.85, '3 minutes of questions', size=17, color=BODY)
    s.text(x0, 0.7, 'A timer in the corner of the room. Practise with it twice.', size=19, ha='left')
    return s


@fig('da_three_questions')
def da_three_questions(w, h, **_):
    s = Scene(w, h)
    rows = [('"Where did this number come from?"', 'the output cell\nin your notebook'), ('"What did you clean?"', 'your\ncleaning log'), ('"What can this data not tell us?"', 'the limitation\nyou wrote')]
    for i, (q, a) in enumerate(rows):
        y = h - 0.95 - i * 1.35
        s.icon('person', 0.6, y, 0.65)
        s.box(1.2, y - 0.4, 3.3, 0.8, q, size=14, r=0.05)
        s.arrow(4.6, y, 5.2, y, color=RED, lw=2.4)
        s.box(5.3, y - 0.4, 2.25, 0.8, a, size=14.5, fill=GOLD, r=0.05, weight='bold')
    s.text(w / 2, 0.35, 'Point to the evidence. Do not read the number from memory.', size=17, color=BODY)
    return s


@fig('da_backup_plan')
def da_backup_plan(w, h, **_):
    s = Scene(w, h)
    s.box(0.3, h - 1.8, 2.8, 1.2, 'live notebook', size=21, weight='bold', r=0.05)
    s.arrow(3.2, h - 1.35, 4.7, h - 1.35, color=RED, lw=2.4)
    s.text(3.95, h - 0.85, 'if the laptop fails', size=14, color=RED, weight='bold')
    s.box(4.8, h - 1.8, 2.6, 1.2, 'PDF and\nscreenshots', size=19, weight='bold', fill=GOLD, r=0.05)
    s.text(w / 2, h - 2.7, 'Save the backup before the day.', size=20, weight='bold')
    s.text(w / 2, h - 3.3, 'Explain the workflow aloud while the pictures stay on screen.', size=17, color=BODY)
    s.text(w / 2, h - 3.85, 'Arrange a short live rerun afterwards if evidence is missing.', size=17, color=BODY)
    return s


# ------------------------------------------------------------------ session 24
@fig('da_hero_showcase')
def da_hero_showcase(w, h, **_):
    s = Scene(w, h)
    parts = [('setup and\nbackups', 30), ('welcome', 10), ('presentations and questions', 40), ('break', 10), ('feedback, certificates', 20), ('reflection and next steps', 70)]
    total = sum(m for _, m in parts)
    x0, sc = 0.2, (w - 0.4) / total
    t = 0
    for i, (lab, m) in enumerate(parts):
        bw = m * sc
        fill = GOLD if i == 2 else (PAPER if i in (1, 3, 4) else INK)
        col = INK if fill != INK else PAPER
        s.box(x0 + t * sc, h - 2.1, bw, 1.1, str(m), size=24, fill=fill, edge=INK, lw=1.8, r=0.02, color=col, weight='bold')
        s.text(x0 + t * sc + bw / 2, h - 2.5 - (i % 2) * 0.62, lab, size=17, ha='center')
        t += m
    s.text(x0, h - 0.6, 'The showcase session, in minutes', size=22, weight='bold', ha='left')
    s.text(x0, 0.5, 'Parents and guardians join for welcome, presentations and certificates.', size=19, ha='left', color=BODY)
    return s


@fig('da_unaided_change')
def da_unaided_change(w, h, **_):
    s = Scene(w, h)
    steps = [('The instructor picks one small change', 'person'), ('Close the assistant windows', 'cross'), ('You make the change and run it', 'laptop'), ('You say what changed and how you checked', 'magnifier')]
    for i, (t, ic) in enumerate(steps):
        y = h - 0.75 - i * 1.1
        s.icon(ic, 0.6, y, 0.7)
        s.text(1.3, y, t, size=19, ha='left')
        if i < len(steps) - 1:
            s.arrow(0.6, y - 0.4, 0.6, y - 0.7, color=RED, lw=2.2, head=12)
    s.text(0.3, 0.3, 'For example: filter one branch, or change 5 units to 10.', size=17, color=BODY, ha='left')
    return s


@fig('da_next_goal')
def da_next_goal(w, h, **_):
    s = Scene(w, h)
    s.box(0.3, 0.3, w - 0.6, h - 0.6, '', fill=PAPER, lw=2.0, r=0.04)
    labels = ['my next goal', 'my first step', 'by when']
    for i, lab in enumerate(labels):
        y = h - 1.1 - i * 1.25
        s.text(0.7, y + 0.1, lab, size=21, weight='bold', ha='left')
        s.line(0.7, y - 0.35, w - 0.7, y - 0.35, color=INK, lw=1.4)
    s.icon('pen', w - 1.1, h - 0.95, 0.9)
    s.text(0.7, 0.62, 'Write it in your own words. Keep this card with your project folder.', size=16, ha='left', color=BODY)
    return s
