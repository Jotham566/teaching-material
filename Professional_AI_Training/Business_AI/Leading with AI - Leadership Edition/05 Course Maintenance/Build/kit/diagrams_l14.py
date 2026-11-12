"""Figures for Leadership Edition Session 14, Data readiness, AI roadmap and your 90-day plan.  Names: x_l14_*  (content kind 'l14_*').

No maths anywhere: pictures, counts and percentages only.  NVF counts come from the recorded run demo_runs/s14/nvf_file_check_output.txt
(plain Python with pandas, no AI model, 6 November 2026, one deterministic run).  Nile Valley Foods is fictional; its scorecard, portfolio,
owners, dates and hours are invented teaching values (they match Templates/Information Inventory.xlsx, AI Opportunity Portfolio.xlsx and
90-Day Roadmap.xlsx).  Case figures come from research/*.md: ADO-03 Gartner, ADO-07 GSMA, GAP-18 and GOV-05 Uganda National Data Strategy,
BNK-02 KCB, TEL-10 Vodacom, AGR-06 Dimitra and NACCU, MFG-05 BEES at Nile Breweries, HLT-04 Makerere AI Health Lab, PUB-01 URA.
"""
from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD, fig
import slidekit as K
from diagrams_l02 import _wrap, _fit, _source, _lh
from diagrams_t14 import x_t14_fivekinds, x_t14_roadmap


# ------------------------------------------------------------------ five kinds of data (wraps the Executive figure with Leadership examples)
FIVE = [dict(icon='grid', head='Tables', example='Loan books, sales sheets, invoices', action='Define each column'),
        dict(icon='mail', head='Text', example='Emails, contracts, policies', action='Find the current version'),
        dict(icon='magnifier', head='Images', example='Scanned forms, photos', action='Read the text; check a sample'),
        dict(icon='phone', head='Audio', example='Calls, meetings', action='Transcribe; remove phone numbers'),
        dict(icon='gear', head='Sensor data', example='Truck GPS, meters', action='Check for gaps')]


@fig('x_l14_fivekinds')
def x_l14_fivekinds(w, h, **_):
    return x_t14_fivekinds(w, h, items=FIVE, size=15)


# ------------------------------------------------------------------ the NVF 90-day roadmap (values as in 90-Day Roadmap.xlsx; fictional)
ROAD = [dict(label='1 Data-sharing rule', owner='Sarah Namukasa', start=0, end=25), dict(label='2 Fix invoice file', owner='Joseph Mugisha', start=0, end=18),
        dict(label='3 Data dictionary', owner='Peter Okello', start=5, end=53), dict(label='4 Mask phones', owner='David Kato', start=25, end=60, after=[0]),
        dict(label='5 Test on 20 questions', owner='Grace Akello', start=60, end=81, hl=True, after=[1, 2, 3]), dict(label='6 Decide', owner='Sarah Namukasa', start=81, end=88, after=[4])]


@fig('x_l14_roadmap')
def x_l14_roadmap(w, h, **_):
    return x_t14_roadmap(w, h, items=ROAD, marks=[dict(day=30, label='3 Mar'), dict(day=60, label='2 Apr'), dict(day=90, label='2 May')], size=16)


# ------------------------------------------------------------------ recall bridge: the portfolio grew a column every session
@fig('x_l14_bridge')
def x_l14_bridge(w, h, **_):
    s = Scene(w, h)
    s.text(0.05, h - 0.25, 'Your AI Opportunity Portfolio, one column at a time', size=16, weight='bold', ha='left')
    cols = [('Sessions 0 to 10', 'The use, what goes in, what comes out, who uses it, how we would know it works', 2.35),
            ('Session 11', 'Value and feasibility', 1.2),
            ('Session 12', 'Roles it touches; tasks that change', 1.2),
            ('Session 13', 'Likelihood, impact, risk score', 1.2),
            ('Today', 'Data ready? Decision; owner', 1.3)]
    gap = 0.07
    x = 0.05
    top, bot = h - 0.6, 1.75
    centres = []
    for i, (sess, txt, cw) in enumerate(cols):
        last = i == len(cols) - 1
        s.rect(x, top - 0.5, cw, 0.5, fill=INK if not last else RED, edge=INK, lw=1.2)
        s.text(x + cw / 2, top - 0.25, sess, size=14, weight='bold', color=PAPER)
        s.box(x, bot, cw, top - 0.55 - bot, '', fill=GOLD if last else PAPER, lw=1.6, r=0.04)
        _wrap(s, x + cw / 2, (top - 0.55 + bot) / 2, cw - 0.2, txt, 15, weight='bold' if last else 'normal', color=INK if last else BODY)
        centres.append(x + cw / 2)
        x += cw + gap
    s.arrow(w / 2, bot - 0.08, w / 2, 1.2, lw=2.4, head=16)
    s.box(1.0, 0.55, w - 2.0, 0.62, '', fill=PAPER, edge=RED, lw=2.2, r=0.08)
    s.text(w / 2, 0.86, 'Your 90-day plan: owners, dates, check-ins', size=16, weight='bold')
    s.text(w / 2, 0.2, 'Builds on Session 8: good documents. Session 13: who may see which data.', size=14, color=MUTE)
    return s


# ------------------------------------------------------------------ why pilots stall: Gartner (ADO-03) and GSMA (ADO-07)
@fig('x_l14_stall')
def x_l14_stall(w, h, **_):
    s = Scene(w, h)
    half = (w - 0.3) / 2
    # left: Gartner forecast as 100 squares
    side = 2.55
    n, gap = 10, 0.03
    sq = (side - gap * (n - 1)) / n
    x0, y0 = 0.1, h - 0.15 - side
    k = 0
    for r in range(n):
        for c in range(n):
            s.rect(x0 + c * (sq + gap), y0 + (n - 1 - r) * (sq + gap), sq, sq, fill=RED if k < 30 else PAPER, edge=INK if k < 30 else GREY, lw=0.8)
            k += 1
    tx = x0 + side + 0.25
    s.text(tx, h - 0.4, 'At least 30 in 100', size=22, weight='bold', color=RED, ha='left')
    hh = _wrap(s, tx, h - 0.75, half - side - 0.35, 'generative AI projects abandoned after the pilot by the end of 2025', 15, ha='left', va='top', color=BODY)
    s.text(tx, h - 0.95 - hh, 'Reasons given:', size=15, weight='bold', ha='left')
    reasons = ['Poor data quality', 'Weak risk controls', 'Rising costs', 'Unclear business value']
    for i, r in enumerate(reasons):
        y = h - 1.32 - hh - i * 0.33
        s.text(tx, y, f'{i + 1}  {r}', size=15, weight='bold' if i == 0 else 'normal', color=RED if i == 0 else INK, ha='left')
    s.text(x0, y0 - 0.3, 'Gartner forecast, July 2024', size=15, weight='bold', ha='left')
    s.line(half + 0.15, 0.6, half + 0.15, h - 0.1, color=HAIR, lw=1.4)
    # right: GSMA AI for Africa
    rx = half + 0.4
    rw = w - rx - 0.1
    s.text(rx, h - 0.4, 'GSMA, AI for Africa, July 2024', size=16, weight='bold', ha='left')
    s.icon('chart', rx + 0.4, h - 1.15, 0.6)
    _wrap(s, rx + 0.85, h - 1.15, rw - 0.9, 'Over 90 AI uses found in Kenya, Nigeria and South Africa; 98 in 100 predict from past data', 15, ha='left', color=BODY)
    s.text(rx, h - 1.85, 'Barriers named include', size=15, weight='bold', ha='left')
    bars = [('Too little local and local-language data', True), ('Skills gaps', False), ('Few data centres; costly computing', False)]
    for i, (b, hl) in enumerate(bars):
        y = h - 2.25 - i * 0.4
        s.circle(rx + 0.12, y, 0.07, fill=RED if hl else INK, edge=RED if hl else INK)
        s.text(rx + 0.32, y, b, size=15, ha='left', weight='bold' if hl else 'normal', color=RED if hl else INK)
    _source(s, 'Sources: THE Journal, 6 Aug 2024, reporting Gartner (a forecast, not a count); TelecomTV, 16 Jul 2024, reporting GSMA.', y=0.15, x=0.1)
    return s


# ------------------------------------------------------------------ quality checks as counts on a five-row list
@fig('x_l14_counts')
def x_l14_counts(w, h, **_):
    s = Scene(w, h)
    rows = [['Row', 'Name', 'Phone'],
            ['1', 'Amina', '0700 000 001'],
            ['2', 'Brian', '0700 000 002'],
            ['3', 'Carol', ''],
            ['4', 'David', '0700 000 004'],
            ['5', 'Brian', '0700 000 002']]
    tw = 3.65
    cw = [0.6, 1.15, tw - 1.75]
    rh = (h - 0.65) / len(rows)
    hl = {(3, 2): RED, (2, 1): GOLD, (2, 2): GOLD, (5, 1): GOLD, (5, 2): GOLD}
    s.table(0.05, h - 0.05, cw, rh, rows, size=15, align=['center', 'left', 'left'], hl_cells=hl)
    s.text(0.05, 0.25, 'An invented contact list', size=14, color=MUTE, ha='left')
    x = tw + 0.3
    bw = w - x - 0.05
    cards = [(h - 0.1, RED, '4 of 5', 'phone numbers filled; row 3 is blank', 'Completeness'),
             (h / 2 - 0.1, GOLD, '4 of 5', 'rows are different people; Brian is there twice', 'Uniqueness')]
    ch = h / 2 - 0.2
    for top, col, big, txt, term in cards:
        s.box(x, top - ch, bw, ch, '', fill=PAPER, edge=col, lw=2.4, r=0.08)
        s.text(x + 0.2, top - 0.42, big, size=28, weight='bold', ha='left', color=RED if col == RED else INK)
        _wrap(s, x + 0.2, top - 0.8, bw - 0.35, txt, 15, ha='left', va='top', color=BODY)
        s.text(x + bw - 0.15, top - ch + 0.25, term, size=15, weight='bold', ha='right', color=RED)
    return s


# ------------------------------------------------------------------ the readiness scorecard: six areas, Green when, Red when
@fig('x_l14_rule')
def x_l14_rule(w, h, **_):
    s = Scene(w, h)
    rows = [('folder', 'Inventory', 'A written list with an owner for each source', 'No list; files on personal phones'),
            ('magnifier', 'Readable', 'Text can be selected and copied', 'Paper, photos, faint scans'),
            ('doc', 'Complete and unique', 'One current copy, no gaps', 'Copies disagree; rows missing'),
            ('tag', 'Metadata', 'Date, owner and version on each file', 'Names such as “final2”'),
            ('lock', 'Rights', 'Who may use it is written down', 'Unknown; personal data unchecked'),
            ('calendar', 'Current', 'Updated on a set schedule', 'Nobody knows the latest version')]
    c0, c1, c2 = 0.1, 3.2, 7.55
    top = h - 0.05
    head = 0.5
    s.text(c0 + 0.6, top - head / 2, 'Area', size=16, weight='bold', ha='left')
    s.rect(c1, top - head + 0.06, 0.32, 0.32, fill=PAPER, edge=INK, lw=1.6)
    s.text(c1 + 0.45, top - head / 2, 'Green when', size=16, weight='bold', ha='left')
    s.rect(c2, top - head + 0.06, 0.32, 0.32, fill=RED, edge=RED, lw=0)
    s.text(c2 + 0.45, top - head / 2, 'Red when', size=16, weight='bold', ha='left', color=RED)
    s.line(0, top - head, w, top - head, lw=2)
    foot = 0.5
    rh = (top - head - foot) / len(rows)
    for i, (ic, area, g, r) in enumerate(rows):
        yc = top - head - (i + 0.5) * rh
        s.icon(ic, c0 + 0.25, yc, 0.42)
        s.text(c0 + 0.6, yc, area, size=16, weight='bold', ha='left')
        s.text(c1, yc, g, size=15, ha='left', color=BODY)
        s.text(c2, yc, r, size=15, ha='left', color=BODY)
        s.line(0, yc - rh / 2, w, yc - rh / 2, color=HAIR, lw=0.8)
    s.text(0.1, 0.22, 'Amber: usable after a named fix.   Points: Green 2, Amber 1, Red 0, so six areas make at most 12.', size=15, weight='bold', ha='left')
    return s


# ------------------------------------------------------------------ industry tour: data first, in six industries
@fig('x_l14_six')
def x_l14_six(w, h, **_):
    s = Scene(w, h)
    tiles = [('calculator', 'Banking and microfinance', 'Adds new data sources to score more customers', 'KCB Group, Kenya'),
             ('phone', 'Telecom and mobile money', 'Joins its data platforms before the AI', 'Vodacom Group, eight countries'),
             ('plant', 'Agriculture and agribusiness', 'Maps every coffee plot by GPS first', 'Dimitra and NACCU, Kenya'),
             ('bottle', 'Manufacturing and FMCG', 'Digital orders create the data AI needs', 'BEES at Nile Breweries, Uganda'),
             ('clinic', 'Healthcare and insurance', 'Needs more labelled local slide images', 'Makerere AI Health Lab, Uganda'),
             ('people', 'Public sector', 'Cleans the taxpayer register; data for 36% of plan indicators', 'URA; National Data Strategy')]
    gap = 0.12
    tw = (w - 0.2 - 2 * gap) / 3
    th = (h - 0.5 - gap) / 2
    for i, (ic, ind, use, ex) in enumerate(tiles):
        x = 0.1 + (i % 3) * (tw + gap)
        y = 0.45 + (1 - i // 3) * (th + gap)
        s.box(x, y, tw, th, '', fill=PAPER, lw=1.8, r=0.08)
        s.icon(ic, x + 0.5, y + th - 0.55, 0.75)
        tx = x + 1.0
        iw = tw - 1.15
        top = y + th - 0.15
        hh = _wrap(s, tx, top, iw, ind, 16, weight='bold', ha='left', va='top')
        top -= hh + 0.1
        uh = _wrap(s, tx, top, iw, use, 15, ha='left', va='top', color=BODY)
        top -= uh + 0.08
        _wrap(s, tx, top, iw, ex, 15, weight='bold', ha='left', va='top', color=RED)
    _source(s, 'Sources: The Star 2026; Google Cloud 2025; AgNavigator 2025; Watchdog Uganda 2022; Makerere 2025; Daily Monitor 2026.', y=0.16)
    return s


# ------------------------------------------------------------------ Uganda's National Data Strategy (GAP-18, GOV-05)
@fig('x_l14_nds')
def x_l14_nds(w, h, **_):
    s = Scene(w, h)
    pw = (w - 0.2 - 2 * 0.3) / 3
    xs = [0.1 + i * (pw + 0.3) for i in range(3)]
    heads = ['Today: data kept apart', 'The gap', 'The plan: five years']
    for x, hd in zip(xs, heads):
        s.text(x + 0.05, h - 0.3, hd, size=17, weight='bold', ha='left')
        s.line(x, h - 0.55, x + pw, h - 0.55, lw=1.6)
    # panel 1: separate databases
    x = xs[0]
    for i, nm in enumerate(['UBOS', 'NIRA', 'DCIC']):
        bx = x + 0.1 + i * 1.22
        s.box(bx, h - 1.75, 1.05, 0.85, nm, size=15, weight='bold', fill=PAPER, lw=1.6, r=0.06)
    _wrap(s, x + pw / 2, h - 2.3, pw - 0.2, 'Each agency runs its own database to its own standard', 15, color=BODY)
    s.icon('person', x + 0.35, 1.0, 0.55)
    _wrap(s, x + 0.75, 1.0, pw - 0.85, 'Citizens hand in the same records again', 15, ha='left', weight='bold')
    # panel 2: 36% to 80%
    x = xs[1]
    bl, bw_ = x + 0.1, pw - 0.2
    for i, (v, lab, fill) in enumerate(((36, 'have data today', RED), (80, 'the five-year target', GOLD))):
        y = h - 1.3 - i * 1.15
        s.text(bl, y + 0.25, f'{v}%', size=26, weight='bold', ha='left', color=RED if i == 0 else INK)
        s.text(bl + 1.15, y + 0.25, lab, size=15, ha='left', color=BODY)
        s.rect(bl, y - 0.35, bw_, 0.3, fill=PAPER, edge=INK, lw=1.2)
        s.rect(bl, y - 0.35, bw_ * v / 100, 0.3, fill=fill, edge=INK, lw=1.2, z=3)
    _wrap(s, x + pw / 2, 0.95, pw - 0.2, 'of the indicators in the Fourth National Development Plan', 15, color=BODY)
    # panel 3: three pillars and the people
    x = xs[2]
    for i, p in enumerate(['Pillar 1: governance', 'Pillar 2: infrastructure', 'Pillar 3: use']):
        s.box(x + 0.1, h - 1.07 - i * 0.48, pw - 0.2, 0.42, p, size=15, weight='bold', fill=GOLD, lw=1.4, r=0.04)
    _wrap(s, x + pw / 2, 1.62, pw - 0.2, 'A National Data Steering Committee and a National Data Office', 15, color=BODY)
    _wrap(s, x + pw / 2, 0.85, pw - 0.2, 'A data focal point in every institution; public servants trained', 15, weight='bold')
    _source(s, 'Source: Daily Monitor, 21 October 2026. These are targets, not results.', y=0.2)
    return s


# ------------------------------------------------------------------ the NVF files: six quality checks, each a count (recorded run)
@fig('x_l14_checks')
def x_l14_checks(w, h, **_):
    s = Scene(w, h)
    tiles = [('check', 'Completeness', 'Is it all there?', '58 of 60', 'invoices have a PO number'),
             ('magnifier', 'Accuracy', 'Is it correct?', '4 of 60', 'invoice totals do not add up'),
             ('doc', 'Consistency', 'Does it agree with the rest?', '1 line', 'at 0% VAT; the same supplier charges 18% elsewhere'),
             ('calendar', 'Timeliness', 'Is it current?', '19 Oct 2026', 'the last week in the sales file'),
             ('tag', 'Uniqueness', 'Recorded once?', '1 invoice', 'appears twice in the 60 rows'),
             ('stamp', 'Validity', 'Does it follow the rules?', '32 of 40', 'sender cells hold a phone number, not a name')]
    gap = 0.12
    tw = (w - 0.2 - 2 * gap) / 3
    th = (h - 0.5 - gap) / 2
    for i, (ic, term, q, big, txt) in enumerate(tiles):
        x = 0.1 + (i % 3) * (tw + gap)
        y = 0.45 + (1 - i // 3) * (th + gap)
        s.box(x, y, tw, th, '', fill=PAPER, lw=1.8, r=0.08)
        s.icon(ic, x + 0.42, y + th - 0.42, 0.55)
        s.text(x + 0.8, y + th - 0.3, term, size=16, weight='bold', ha='left')
        s.text(x + 0.8, y + th - 0.6, q, size=15, ha='left', color=BODY)
        s.text(x + 0.2, y + 0.72, big, size=24, weight='bold', ha='left', color=RED)
        _wrap(s, x + 0.2, y + 0.3, tw - 0.3, txt, 15, ha='left')
    _source(s, 'Every count from the recorded run of a Python script, 6 Nov 2026, no AI model. NVF is fictional.', y=0.16)
    return s


# ------------------------------------------------------------------ the NVF readiness scorecard (invented teaching values)
@fig('x_l14_readiness')
def x_l14_readiness(w, h, rows=(), total=True, size=16, **_):
    s = Scene(w, h)
    pts_of = {'Green': 2, 'Amber': 1, 'Red': 0}
    n = len(rows)
    foot = 0.5 if total else 0.0
    head = 0.42
    rh = (h - 0.05 - head - foot) / max(n, 1)
    big = w > 8
    c1 = 2.75 if big else 1.4
    cw = 1.3 if big else 1.05
    cp = c1 + cw + 0.15
    pw = 0.95 if big else 0.75
    c2 = cp + pw + 0.1
    top = h - 0.02
    for x, t, ha in ((0.08, 'Area', 'left'), (c1 + 0.08, 'Rating', 'left'), (cp + pw / 2, 'Points', 'center'), (c2 + 0.08, 'Evidence', 'left')):
        s.text(x, top - head / 2, t, size=size - 1, weight='bold', ha=ha)
    s.line(0, top - head, w, top - head, color=INK, lw=2.2)
    tot = 0
    for i, r in enumerate(rows):
        y1 = top - head - rh * i
        yc = y1 - rh / 2
        s.text(0.08, yc, '\n'.join(K.wrap(r['area'], size, 'bold', c1 - 0.15)), size=size, weight='bold', ha='left')
        rating = r['rating']
        ch = min(rh - 0.12, 0.44)
        fill, edge, col = {'Red': (RED, RED, PAPER), 'Amber': (GOLD, GOLD, INK)}.get(rating, (PAPER, INK, INK))
        s.rect(c1 + 0.08, yc - ch / 2, cw, ch, fill=fill, edge=edge, lw=1.6 if rating == 'Green' else 0, z=2)
        s.text(c1 + 0.08 + cw / 2, yc, rating.upper(), size=max(14, size - 2), weight='bold', color=col, z=6)
        p = pts_of[rating]
        tot += p
        s.text(cp + pw / 2, yc, str(p), size=size + 1, weight='bold', color=RED if p == 0 else INK)
        s.text(c2 + 0.08, yc, '\n'.join(K.wrap(r['why'], size - 1, 'regular', w - c2 - 0.2)), size=size - 1, ha='left', color=BODY)
        s.line(0, y1 - rh, w, y1 - rh, color=HAIR, lw=0.8)
    if total:
        s.text(0.08, foot / 2, f'Total: {tot} of {2 * n} points', size=size + 1, weight='bold', ha='left')
        if any(r['rating'] == 'Red' and r['area'] == 'Rights' for r in rows):
            s.text(w - 0.08, foot / 2, 'A Red on rights stops the work, whatever the total', size=size - 1, weight='bold', color=RED, ha='right')
    return s


# ------------------------------------------------------------------ the final portfolio, every entry decided (NVF, fictional)
PORT = [('Answer staff questions from the handbook and files', '4', '4', 'All staff; HR keeps the handbook', '9 Medium', 'Amber', 'Start now', 'Mary Nabirye'),
        ('Check supplier invoices before payment', '4', '4', 'Finance clerks', '12 Medium', 'Amber', 'Prepare first', 'Joseph Mugisha'),
        ('Sort incoming customer messages', '4', '5', 'Customer service desk', '12 Medium', 'Red', 'Prepare first', 'David Kato'),
        ('Rank shops by risk of ordering less', '4', '4', 'Area sales reps, sales manager', '6 Low', 'Amber', 'Prepare first', 'Peter Okello'),
        ('Shortlist CVs for the dispatch clerk post', '2', '2', 'HR officer; applicants', '20 High', 'Red', 'Drop', 'Mary Nabirye')]


@fig('x_l14_portfolio')
def x_l14_portfolio(w, h, **_):
    s = Scene(w, h)
    heads = [('The use', 'Sessions 0 to 10'), ('Value', '11'), ('Feasi-\nbility', '11'), ('Roles it touches', '12'), ('Risk score', '13'), ('Data ready?', '14'), ('Decision', '14'), ('Owner', '14')]
    cws = [3.1, 0.8, 0.9, 2.2, 1.25, 1.2, 1.5, 1.55]
    sc = (w - 0.1) / sum(cws)
    cws = [c * sc for c in cws]
    xs = [0.05]
    for c in cws[:-1]:
        xs.append(xs[-1] + c)
    top = h - 0.02
    hh = 0.78
    for j, ((hd, se), x, cw) in enumerate(zip(heads, xs, cws)):
        last = se == '14'
        s.rect(x, top - hh, cw, hh, fill=RED if last else INK, edge=INK, lw=1.0)
        s.text(x + cw / 2, top - 0.3, hd, size=15 if '\n' not in hd else 14, weight='bold', color=PAPER)
        if j == 2:
            continue
        cx = x + cw / 2 if j != 1 else x + (cw + cws[2]) / 2
        s.text(cx, top - hh + 0.14, 'Session ' + se if len(se) < 4 else se, size=14, color=PAPER)
    rh = (top - hh - 0.42) / len(PORT)
    for i, row in enumerate(PORT):
        y = top - hh - (i + 1) * rh
        for j, (val, x, cw) in enumerate(zip(row, xs, cws)):
            fill = PAPER
            col = INK
            if j == 5:
                fill, col = {'Red': (RED, PAPER), 'Amber': (GOLD, INK)}.get(val, (PAPER, INK))
            if j == 6 and val == 'Start now':
                fill = GOLD
            s.rect(x, y, cw, rh, fill=fill, edge=INK, lw=1.0)
            if j in (0, 3, 7):
                _wrap(s, x + 0.08, y + rh / 2, cw - 0.16, val, 14, ha='left', color=col)
            else:
                s.text(x + cw / 2, y + rh / 2, val, size=15, weight='bold' if j >= 5 else 'normal', color=col)
    s.text(0.05, 0.18, 'Nile Valley Foods is fictional. Value and feasibility out of 5; risk score is likelihood times impact (15 or more is High).', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ practice example: one entry with its last two columns
@fig('x_l14_entry')
def x_l14_entry(w, h, **_):
    s = Scene(w, h)
    rows = [('The use', 'Check supplier invoices before payment'),
            ('Value, feasibility', '4 and 4 out of 5 (Session 11)'),
            ('Roles it touches', 'Finance clerks: check the flags'),
            ('Risk score', '3 times 4, so 12, Medium (Session 13)'),
            ('Data ready?', 'Amber: 8 faults in 60 rows'),
            ('Decision, owner', 'Prepare first; Joseph Mugisha')]
    s.text(0.05, h - 0.2, 'Nile Valley Foods (fictional): one entry', size=15, weight='bold', ha='left')
    lw_ = 1.85
    vw = w - 0.1 - lw_
    rh = (h - 0.45) / len(rows)
    y = h - 0.42
    for i, (a, b) in enumerate(rows):
        today = i >= 4
        s.rect(0.05, y - rh, lw_, rh, fill=GOLD if today else PALE, edge=INK, lw=1.0)
        s.rect(0.05 + lw_, y - rh, vw, rh, fill=PAPER, edge=INK, lw=1.0)
        _wrap(s, 0.12, y - rh / 2, lw_ - 0.15, a, 14, weight='bold', ha='left')
        _wrap(s, 0.12 + lw_, y - rh / 2, vw - 0.15, b, 14, ha='left', color=BODY)
        y -= rh
    return s


# ------------------------------------------------------------------ from the portfolio to the 90-day plan
@fig('x_l14_toplan')
def x_l14_toplan(w, h, **_):
    s = Scene(w, h)
    lw_ = 3.3
    s.text(0.1, h - 0.3, 'The portfolio decides', size=17, weight='bold', ha='left')
    decs = [('Start now', '1 use: test it in days 61 to 90', GOLD), ('Prepare first', '3 uses: fix their data in days 1 to 60', PAPER),
            ('Later', 'Keep it on the list', PAPER), ('Drop', '1 use: the CV shortlist', PALE)]
    bh = 0.72
    for i, (d, t, f) in enumerate(decs):
        y = h - 0.7 - (i + 1) * (bh + 0.12) + 0.12
        s.box(0.1, y, lw_, bh, '', fill=f, lw=1.6, r=0.06)
        s.text(0.25, y + bh - 0.22, d, size=16, weight='bold', ha='left', color=RED if d == 'Drop' else INK)
        s.text(0.25, y + 0.2, t, size=14, ha='left', color=BODY)
    px = lw_ + 0.7
    s.arrow(lw_ + 0.15, h / 2 - 0.2, px - 0.1, h / 2 - 0.2, lw=2.6, head=18)
    pw = (w - px - 0.1 - 2 * 0.15) / 3
    phases = [('Days 1 to 30', 'Protect and clean', ['Settle who may use which data', 'Fix the worst file', 'Name an owner for each source']),
              ('Days 31 to 60', 'Describe and prepare', ['Define every column', 'Remove personal data from copies', 'Write 20 real questions and their answers']),
              ('Days 61 to 90', 'Test and decide', ['Test the start-now use on the 20 questions', 'Continue, expand, pause or stop', 'Brief the sponsor at day 90'])]
    for i, (days, name, items) in enumerate(phases):
        x = px + i * (pw + 0.15)
        last = i == 2
        s.rect(x, h - 1.15, pw, 0.85, fill=GOLD if last else INK, edge=INK, lw=1.2)
        s.text(x + 0.15, h - 0.5, days, size=15, weight='bold', ha='left', color=INK if last else PAPER)
        s.text(x + 0.15, h - 0.88, name, size=15, ha='left', color=INK if last else PAPER)
        s.box(x, 0.55, pw, h - 1.8, '', fill=PAPER, lw=1.6, r=0.04)
        top = h - 1.4
        for it in items:
            hh = _wrap(s, x + 0.15, top, pw - 0.3, it, 15, ha='left', va='top', color=BODY)
            top -= hh + 0.25
        if i < 2:
            s.arrow(x + pw + 0.01, h - 0.72, x + pw + 0.14, h - 0.72, lw=1.8, head=11)
    s.text(px, 0.22, 'Nile Valley Foods is fictional. Phase names as in the 90-Day Roadmap template.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ your people: who owns the data work
@fig('x_l14_people')
def x_l14_people(w, h, **_):
    s = Scene(w, h)
    roles = [('Sponsor', 'A director who owns the 90-day plan and clears blockers', 'shield', GOLD),
             ('Data owners', 'One per source: decides who may use it, signs off fixes', 'folder', PAPER),
             ('Data stewards', 'The clerks who enter and correct the data every day', 'pen', PAPER),
             ('IT', 'Access, copies, backups and the systems', 'gear', PAPER),
             ('Legal', 'Rights, and personal data under the 2019 Act', 'lock', PAPER),
             ('The users', 'Write the 20 test questions and judge the answers', 'people', PAPER)]
    lw_ = 6.9
    gap = 0.08
    bh = (h - 0.1 - gap * 5) / 6
    for i, (role, txt, ic, f) in enumerate(roles):
        y = h - 0.05 - (i + 1) * bh - i * gap
        s.box(0.05, y, lw_, bh, '', fill=f, lw=1.5, r=0.06)
        s.icon(ic, 0.4, y + bh / 2, 0.42)
        s.text(0.8, y + bh / 2, role, size=15, weight='bold', ha='left')
        s.text(3.05, y + bh / 2, '\n'.join(K.wrap(txt, 14, 'regular', lw_ - 3.1)), size=14, ha='left', color=BODY)
    x = lw_ + 0.3
    pw = w - x - 0.05
    s.box(x, 2.25, pw, h - 2.3, '', fill=PAPER, edge=INK, lw=1.8, r=0.08)
    s.text(x + 0.2, h - 0.33, 'What staff fear and gain', size=16, weight='bold', ha='left')
    hh = _wrap(s, x + 0.2, h - 0.62, pw - 0.4, 'Fear: blamed for old errors, or watched more closely.', 15, ha='left', va='top', color=BODY)
    _wrap(s, x + 0.2, h - 0.75 - hh, pw - 0.4, 'Gain: fewer corrections, and data work that is seen and valued.', 15, ha='left', va='top', color=BODY)
    s.box(x, 0.05, pw, 2.05, '', fill=PAPER, edge=RED, lw=2.2, r=0.08)
    s.text(x + 0.2, 1.8, 'In Uganda', size=16, weight='bold', color=RED, ha='left')
    hh = _wrap(s, x + 0.2, 1.55, pw - 0.4, 'URA’s own staff wrote the 2019 study of its taxpayer register.', 15, ha='left', va='top', color=BODY)
    _wrap(s, x + 0.2, 1.45 - hh, pw - 0.4, 'The National Data Strategy names a data focal point in every institution.', 15, ha='left', va='top', color=BODY)
    return s


# ------------------------------------------------------------------ the whole course: fifteen sessions in four phases
PHASES = [('A', 'Understand what AI can do', [(0, 'Landscape'), (1, 'Sees, reads'), (2, 'Predicts'), (3, 'Any good?'), (4, 'Language'), (5, 'Chatbots')],
           'Say what AI can do, and judge a claim'),
          ('B', 'Choose it and use it well', [(6, 'Market'), (7, 'Assistants'), (8, 'Documents')], 'Choose a supplier; brief it; give it your documents'),
          ('C', 'Control the risk', [(9, 'Failures'), (10, 'Agents')], 'Check it; decide what an agent may do'),
          ('D', 'Lead the change', [(11, 'Redesign'), (12, 'People'), (13, 'Governance'), (14, 'Data, plan')], 'A decided portfolio and a 90-day plan')]


@fig('x_l14_course')
def x_l14_course(w, h, **_):
    s = Scene(w, h)
    lab_w, can_w = 2.5, 2.0
    cx0 = lab_w + 0.2
    cx1 = w - can_w - 0.15
    chip = (cx1 - cx0) / 6
    strip = 0.45
    gap = 0.07
    bh = (h - 0.05 - strip - 3 * gap) / 4
    for i, (letter, name, sess, can) in enumerate(PHASES):
        y = h - 0.05 - (i + 1) * bh - i * gap
        last = i == 3
        s.box(0.05, y, lab_w, bh, '', fill=GOLD if last else INK, edge=INK, lw=1.4, r=0.06)
        s.text(0.2, y + bh - 0.27, f'Phase {letter}', size=15, weight='bold', ha='left', color=INK if last else PAPER)
        s.text(0.2, y + 0.25, name, size=14, ha='left', color=INK if last else PAPER)
        s.line(cx0 - 0.05, y + bh * 0.62, cx0 + chip * (len(sess) - 0.5), y + bh * 0.62, color=HAIR, lw=5, z=1)
        for j, (n, t) in enumerate(sess):
            x = cx0 + j * chip + chip / 2
            hl = n in (0, 14)
            s.circle(x, y + bh * 0.62, 0.2, fill=RED if hl else PAPER, edge=INK, lw=1.6, z=3)
            s.text(x, y + bh * 0.62, str(n), size=14, weight='bold', color=PAPER if hl else INK)
            s.text(x, y + 0.17, t, size=14, weight='bold' if hl else 'normal')
        s.box(cx1 + 0.1, y, can_w + 0.0, bh, '', fill=PAPER, edge=RED if last else INK, lw=2.0 if last else 1.3, r=0.06)
        _wrap(s, cx1 + 0.1 + can_w / 2, y + bh / 2, can_w - 0.2, can, 14, weight='bold' if last else 'normal', color=INK if last else BODY)
        if i < 3:
            s.arrow(0.45, y - 0.005, 0.45, y - gap + 0.005, lw=1.6, head=9)
    s.text(cx1 + 0.1 + can_w / 2, h - 0.02 + 0.0, '', size=14)
    s.text(w / 2, 0.2, 'Session 14 leads back to the Session 0 question, now answered with your own plan', size=15, weight='bold', color=RED)
    return s
