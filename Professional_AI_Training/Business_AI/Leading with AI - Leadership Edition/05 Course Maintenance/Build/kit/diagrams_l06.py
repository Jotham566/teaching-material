"""Figures for Leadership Edition Session 6, The AI market: models, vendors, and buy, rent or build.  Names: x_l06_*  (content kind 'l06_*').

No maths anywhere: pictures, counts, percentages and shillings only.  Recorded numbers come from demo_runs/ (s06_comparison_runs.md, the
two-assistant comparison of 6 November 2026; s07_sizes_run.md, the file sizes of one small open model, 6 November 2026).  Case figures come
from research/*.md (IDs in the content file).  The rent and host prices on the cost slide are invented to show the idea and are labelled so.
"""
from figkit import Scene, INK, BODY, MUTE, HAIR, PALE, PAPER, RED, GOLD, fig
import slidekit as K
from diagrams_l02 import _wrap, _fit, _source, _lh


def _six(s, w, h, tiles, src):
    """Six industry tiles (icon, industry, use, named example), as in Session 2."""
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
    _source(s, src, y=0.16)


def _server(s, x, y, size=0.8, accent=GOLD):
    """A plain server rack: three stacked units with lights."""
    u = size / 3.2
    for k in range(3):
        yy = y - size / 2 + k * (u + 0.04)
        s.box(x - size * 0.42, yy, size * 0.84, u, '', fill=PAPER, lw=1.6, r=0.03)
        s.circle(x - size * 0.28, yy + u / 2, 0.035 * size / 0.8, fill=accent, edge=INK, lw=1)
        s.line(x - size * 0.1, yy + u / 2, x + size * 0.3, yy + u / 2, lw=1.4)


# ------------------------------------------------------------------ recall bridge: Session 5 to today
@fig('x_l06_bridge')
def x_l06_bridge(w, h, **_):
    s = Scene(w, h)
    lw_ = 3.0
    s.text(0.1, h - 0.3, 'Session 5: how a chatbot writes', size=17, weight='bold', ha='left')
    s.line(0.1, h - 0.55, 0.1 + lw_, h - 0.55, lw=1.6)
    for i, (ic, t) in enumerate((('speech', 'It writes one likely word at a time'), ('question', 'Fluent is not the same as true'),
                                 ('check', 'So a person checks what it writes'))):
        y = h - 1.15 - i * 0.95
        s.icon(ic, 0.45, y, 0.58)
        _wrap(s, 0.9, y, lw_ - 0.85, t, 15, ha='left', color=BODY)
    x0 = 3.55
    s.text(x0, h - 0.3, 'Today: before you choose one', size=17, weight='bold', ha='left', color=RED)
    s.line(x0, h - 0.55, w - 0.1, h - 0.55, lw=1.6, color=RED)
    qs = [('robot', 'Who made the model, and on whose model is it built?'), ('cloud', 'Where does it run, and where does our data go?'),
          ('receipt', 'What does each use cost, and can we leave?')]
    for i, (ic, t) in enumerate(qs):
        y = h - 1.15 - i * 0.95
        s.box(x0, y - 0.38, w - x0 - 0.1, 0.76, '', fill=GOLD if i == 1 else PAPER, lw=1.6, r=0.08)
        s.icon(ic, x0 + 0.38, y, 0.55, **({'text': ''} if ic == 'coin' else {}))
        _wrap(s, x0 + 0.75, y, w - x0 - 0.95, t, 15, ha='left', weight='bold' if i == 1 else 'normal')
    s.arrow(3.15, h - 2.1, 3.45, h - 2.1, lw=2.2, head=15)
    _wrap(s, w / 2, 0.35, w - 0.3, 'The chatbot idea stays the same. The choice is about the supplier, the data and the cost.', 15, weight='bold', color=RED)
    return s


# ------------------------------------------------------------------ hook: Uganda's data protection office rules against Google (GAP-17)
@fig('x_l06_pdpo')
def x_l06_pdpo(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.28, 'Uganda’s Personal Data Protection Office (PDPO)', size=17, weight='bold', ha='left')
    rows = [('8 Nov 2024', 'Four Ugandans complain', 'Google processed their data without registering in Uganda, and moved it abroad without safeguards.', PAPER),
            ('Google’s reply', 'Uganda’s law does not apply', 'Google is not based in Uganda.', PAPER),
            ('18 Jul 2025', 'The PDPO rules: the law applies', 'Google must register within 30 days and show safe rules for moving data out of Uganda.', GOLD)]
    top = h - 0.6
    rh = 0.98
    for i, (d, head, txt, fill) in enumerate(rows):
        y = top - i * (rh + 0.12)
        s.box(0.1, y - rh, 1.6, rh, '', fill=INK if i != 1 else PAPER, lw=1.6, r=0.08)
        _wrap(s, 0.9, y - rh / 2, 1.45, d, 15, weight='bold', color=PAPER if i != 1 else INK)
        s.box(1.85, y - rh, w - 1.95, rh, '', fill=fill, lw=1.6, r=0.08)
        s.text(2.0, y - 0.25, head, size=16, weight='bold', ha='left', color=RED if i == 2 else INK)
        _wrap(s, 2.0, y - 0.62, w - 2.25, txt, 15, ha='left', color=BODY)
    _source(s, 'Source: Uganda Registration Services Bureau, August 2025.', y=0.18)
    return s


# ------------------------------------------------------------------ who makes the models
@fig('x_l06_makers')
def x_l06_makers(w, h, **_):
    s = Scene(w, h)
    cols = [('Global labs', 'cloud', ['OpenAI: ChatGPT', 'Google: Gemini', 'Anthropic: Claude'], 'Hosted: you reach them over the internet'),
            ('Open-weights makers', 'folder', ['Meta: Llama', 'Alibaba: Qwen', 'Mistral AI, DeepSeek'], 'The model file can be downloaded, under a licence'),
            ('African-language builders', 'speech', ['Sunbird AI, Uganda', 'Lelapa AI, South Africa', 'Jacaranda Health, Kenya'], 'Most adapt an open model')]
    gap = 0.3
    cw = (w - 0.2 - 2 * gap) / 3
    for i, (hd, ic, items, foot) in enumerate(cols):
        x = 0.1 + i * (cw + gap)
        s.box(x, 0.1, cw, h - 0.2, '', fill=GOLD if i == 2 else PAPER, lw=1.8, r=0.08)
        s.icon(ic, x + cw / 2, h - 0.6, 0.7)
        _wrap(s, x + cw / 2, h - 1.3, cw - 0.2, hd, 16, weight='bold')
        top = h - 1.75
        for k, it in enumerate(items):
            top -= _wrap(s, x + cw / 2, top, cw - 0.2, it, 16, color=BODY, va='top') + 0.14
        s.line(x + 0.2, 1.3, x + cw - 0.2, 1.3, color=HAIR, lw=1.2)
        _wrap(s, x + cw / 2, 0.72, cw - 0.25, foot, 14, weight='bold', color=RED if i == 1 else INK)
        if i == 1:
            s.arrow(x + cw + 0.02, h / 2 - 0.1, x + cw + gap - 0.02, h / 2 - 0.1, lw=2.4, head=16, color=RED)
    return s


# ------------------------------------------------------------------ most organisations adapt or use a model someone else trained
@fig('x_l06_ladder')
def x_l06_ladder(w, h, **_):
    s = Scene(w, h)
    tiers = [('Train a model from scratch', 'A few global labs: vast computers, a library of text', 3.9, INK, PAPER),
             ('Adapt an open model with your own examples', 'Sunbird on Qwen; Jacaranda on Llama', 5.1, GOLD, INK),
             ('Use a ready model through an app or a connection', 'Most organisations, most of the time', 6.3, PAPER, INK)]
    th = 1.2
    cx = 3.35
    for i, (head, sub, tw, fill, col) in enumerate(tiers):
        y = h - 0.15 - (i + 1) * th - i * 0.12
        s.box(cx - tw / 2, y, tw, th, '', fill=fill, lw=1.8, r=0.08)
        _wrap(s, cx, y + th - 0.38, tw - 0.3, head, 16, weight='bold', color=col)
        _wrap(s, cx, y + 0.34, tw - 0.3, sub, 15, color=col if fill != PAPER else BODY)
    s.arrow(7.05, 0.5, 7.05, h - 0.4, lw=2.4, head=16, color=RED)
    s.text(7.25, h - 0.55, 'cost', size=15, weight='bold', color=RED, rot=90)
    s.text(7.25, 1.4, 'and skill', size=15, weight='bold', color=RED, rot=90)
    s.text(0.1, 0.18, 'The big trained model at the top is called a foundation model.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ hosted or open weights
@fig('x_l06_hosted_open')
def x_l06_hosted_open(w, h, **_):
    s = Scene(w, h)
    bh = 0.78

    def lane(y, head, items, tags, hl):
        s.text(0.1, y + bh + 0.3, head, size=17, weight='bold', ha='left', color=RED if hl else INK)
        x = 0.1
        for i, (txt, wd, gold) in enumerate(items):
            s.box(x, y, wd, bh, '', fill=GOLD if gold else PAPER, lw=1.8, r=0.08)
            _wrap(s, x + wd / 2, y + bh / 2, wd - 0.2, txt, 15, weight='bold' if gold else 'normal')
            if i < len(items) - 1:
                s.arrow(x + wd + 0.04, y + bh / 2, x + wd + 0.3, y + bh / 2, lw=2.2, head=15)
            x += wd + 0.34
        for k, t in enumerate(tags):
            s.text(0.1 + k * 3.8, y - 0.3, t, size=14, color=BODY, ha='left')
    lane(h - 1.7, 'Hosted: the model stays with the vendor', [('Your text', 1.6, False), ('Over the internet to the vendor’s computers', 3.1, False), ('A reply comes back', 2.1, True)],
         ['You pay per use or per seat', 'Your text leaves your building'], False)
    lane(h - 3.85, 'Open weights: you take the model file home', [('Download the model file', 2.0, False), ('Run it on your server, or a cloud you choose', 3.0, False), ('Your text stays there', 1.8, True)],
         ['You pay for the computer, busy or idle', 'A licence sets the rules'], True)
    s.line(0.1, h - 2.38, w - 0.1, h - 2.38, color=HAIR, lw=1.2)
    return s


# ------------------------------------------------------------------ size decides where an open model can run (recorded, s07)
@fig('x_l06_sizes')
def x_l06_sizes(w, h, **_):
    s = Scene(w, h)
    data = [('Full detail', 538), ('Half the detail', 269), ('A quarter', 135), ('An eighth', 76)]
    unit = 1.55 / (538 ** 0.5)
    x = 0.2
    base = 2.0
    for i, (lab, mb) in enumerate(data):
        side = unit * mb ** 0.5
        s.rect(x, base, side, side, fill=GOLD if i == 3 else PAPER, edge=INK, lw=1.8)
        s.text(x + side / 2, base + side + 0.25, f'{mb} MB', size=17, weight='bold')
        s.text(x + side / 2, base - 0.3, lab, size=15, color=BODY)
        x += max(side, 1.25) + 0.35
    s.text(0.1, h - 0.25, 'One small open model, saved with less detail in each number', size=15, weight='bold', ha='left')
    s.box(0.1, 0.5, w - 0.2, 0.85, '', fill=PAPER, edge=RED, lw=1.8, r=0.08)
    _wrap(s, w / 2, 0.925, w - 0.5, 'At a quarter, its top two answers held; at an eighth, the list changed.', 15, weight='bold')
    s.text(0.1, 0.18, 'Recorded run, SmolLM2 135M, 6 November 2026, one run. MB: millions of bytes.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ three routes
@fig('x_l06_routes')
def x_l06_routes(w, h, **_):
    s = Scene(w, h)
    lab_w = 1.75
    cw = (w - 0.1 - lab_w) / 3
    heads = [('cloud', 'Rent a hosted assistant'), ('home', 'Host an open model'), ('gear', 'Build on a partner’s platform')]
    rows = ['Who runs it', 'Your data sits', 'You pay', 'You need', 'Example']
    cells = [['The vendor', 'Your IT team, or a local provider', 'The partner, with your data platform on its cloud'],
             ['On the vendor’s computers, often abroad', 'Where you choose', 'In the partner’s cloud region'],
             ['Per use, or per seat each month', 'A server each month, busy or idle', 'A contract over several years'],
             ['Data terms you have read', 'People who can run a server', 'Your own data in order first'],
             ['PwC: ChatGPT Enterprise for 100,000 staff', 'Jacaranda: its own Kiswahili model on Llama 3', 'Vodacom: data to Google Cloud, then AI']]
    top = h - 0.75
    rh = (top - 0.1) / len(rows)
    for j, (ic, hd) in enumerate(heads):
        x = 0.1 + lab_w + j * cw
        s.icon(ic, x + 0.4, h - 0.38, 0.55)
        _wrap(s, x + 0.75, h - 0.38, cw - 0.85, hd, 16, weight='bold', ha='left')
    for r, lab in enumerate(rows):
        y = top - r * rh
        _wrap(s, 0.1, y - rh / 2, lab_w - 0.1, lab, 15, weight='bold', ha='left', color=RED if r == 4 else INK)
        for j in range(3):
            x = 0.1 + lab_w + j * cw
            s.rect(x + 0.05, y - rh + 0.04, cw - 0.1, rh - 0.06, fill=PALE if r == 4 else PAPER, edge=HAIR, lw=1.0, z=1)
            _wrap(s, x + 0.18, y - rh / 2 + 0.01, cw - 0.36, cells[r][j], 14, ha='left', color=INK if r == 4 else BODY, weight='bold' if r == 4 else 'normal')
    return s


# ------------------------------------------------------------------ four questions decide the route
@fig('x_l06_four')
def x_l06_four(w, h, **_):
    s = Scene(w, h)
    tiles = [('shield', 'Data location and the law', 'Where is our data kept and used, and does that meet Uganda’s law?'),
             ('receipt', 'Cost per use', 'What does each use cost at our volume, this year and next?'),
             ('lock', 'Lock-in', 'How hard would it be to move to another supplier?'),
             ('flag', 'Vendor survival', 'Will the supplier still be here, and what if it is not?')]
    tw, th = (w - 0.3) / 2, (h - 0.3) / 2
    for i, (ic, hd, tx) in enumerate(tiles):
        x = 0.1 + (i % 2) * (tw + 0.1)
        y = 0.1 + (1 - i // 2) * (th + 0.1)
        s.box(x, y, tw, th, '', fill=PAPER, lw=1.8, r=0.08)
        s.icon(ic, x + 0.55, y + th - 0.55, 0.75, **({'text': ''} if ic == 'coin' else {}))
        _wrap(s, x + 1.05, y + th - 0.55, tw - 1.2, hd, 18, weight='bold', ha='left')
        _wrap(s, x + 0.25, y + (th - 1.0) / 2 + 0.05, tw - 0.45, tx, 15, ha='left', color=BODY)
    return s


# ------------------------------------------------------------------ where your data goes, and the checks on the way
@fig('x_l06_dataflow')
def x_l06_dataflow(w, h, **_):
    s = Scene(w, h)
    y = h - 0.9
    s.box(0.1, y - 0.7, 1.9, 1.4, '', fill=PAPER, lw=1.8, r=0.08)
    s.icon('folder', 1.05, y + 0.22, 0.6)
    _wrap(s, 1.05, y - 0.4, 1.75, 'Your records, Kampala', 15, weight='bold')
    s.box(w - 2.1, y - 0.7, 2.0, 1.4, '', fill=GOLD, lw=1.8, r=0.08)
    _server(s, w - 1.1, y + 0.22, 0.6)
    _wrap(s, w - 1.1, y - 0.4, 1.85, 'Vendor’s data centre, often abroad', 14, weight='bold')
    s.arrow(2.05, y, w - 2.15, y, lw=2.6, head=18)
    gates = ['Is the vendor registered with Uganda’s PDPO?', 'Are there safe rules for data leaving Uganda?', 'Does the contract say where it is kept, who sees it, when deleted?']
    gx0, gw = 2.05, (w - 4.2) / 3
    bw = (w - 0.4) / 3
    for i, g in enumerate(gates):
        gx = gx0 + i * gw + gw / 2
        s.line(gx, y - 0.45, gx, y + 0.45, color=RED, lw=3, z=5)
        s.circle(gx, y + 0.62, 0.17, fill=RED, edge=RED, z=6)
        s.text(gx, y + 0.62, str(i + 1), size=14, weight='bold', color=PAPER, z=7)
        bx = 0.1 + i * (bw + 0.1)
        s.box(bx, 1.55, bw, 1.45, '', fill=PAPER, lw=1.6, r=0.08)
        s.circle(bx + 0.3, 2.275, 0.17, fill=RED, edge=RED, z=6)
        s.text(bx + 0.3, 2.275, str(i + 1), size=14, weight='bold', color=PAPER, z=7)
        _wrap(s, bx + 0.55, 2.275, bw - 0.65, g, 14, ha='left', weight='bold')
    s.box(0.1, 0.45, w - 0.2, 0.95, '', fill=PAPER, edge=RED, lw=1.8, r=0.08)
    _wrap(s, w / 2, 1.08, w - 0.5, 'Uganda’s Data Protection and Privacy Act, 2019, reaches any vendor handling Ugandans’ personal data.', 15, weight='bold')
    _wrap(s, w / 2, 0.66, w - 0.5, 'The PDPO said so of Google in July 2025.', 15, color=BODY)
    s.text(0.1, 0.15, 'Not legal advice: your lawyer confirms what applies to you.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ data centres in Africa (GAP-14, GAP-15)
@fig('x_l06_datacentres')
def x_l06_datacentres(w, h, **_):
    s = Scene(w, h)
    pw = (w - 0.3) / 2
    panels = [('Cassava Technologies and Nvidia, South Africa', [('Mar 2025', 'Announced: up to US$720 million (another outlet says US$700 million)'),
                                                                 ('Jun 2025', 'First 3,000 GPUs, the chips that run AI, in a centre in South Africa'),
                                                                 ('Planned', 'About 12,000 more across Egypt, Nigeria, Kenya and Morocco')], PAPER, 'Opened'),
              ('Microsoft and G42, Kenya', [('May 2024', 'A US$1 billion data centre at Olkaria, on geothermal power'),
                                            ('May 2026', 'The President: one centre would need 1,000 MW, when Kenya has 2,300 MW'),
                                            ('2026', 'Stalled over power; the government says it is not abandoned')], PAPER, 'Stalled')]
    for i, (hd, items, fill, badge) in enumerate(panels):
        x = 0.1 + i * (pw + 0.1)
        s.box(x, 0.55, pw, h - 0.65, '', fill=fill, lw=1.8, r=0.08, edge=RED if i else INK)
        _server(s, x + 0.45, h - 0.5, 0.55)
        _wrap(s, x + 0.85, h - 0.45, pw - 2.25, hd, 16, weight='bold', ha='left')
        s.box(x + pw - 1.3, h - 0.68, 1.15, 0.45, badge, size=15, weight='bold', fill=GOLD if i == 0 else RED, color=INK if i == 0 else PAPER, r=0.06)
        rh = (h - 1.75) / 3
        for k, (d, t) in enumerate(items):
            y = h - 1.2 - k * rh
            s.text(x + 0.2, y - 0.02, d, size=15, weight='bold', ha='left', color=RED if (i and k == 2) else INK, va='top')
            _wrap(s, x + 1.35, y, pw - 1.5, t, 15, ha='left', va='top', color=BODY)
    _source(s, 'Sources: TechCentral, Apr 2025; Intelligent CIO, Nov 2025; Microsoft, May 2024; Citizen Digital, May 2026.', y=0.22)
    return s


# ------------------------------------------------------------------ cost per use: where renting and hosting meet (illustrative)
@fig('x_l06_breakeven')
def x_l06_breakeven(w, h, **_):
    s = Scene(w, h)
    vols = [1000, 2000, 3000, 4000, 5000]
    base = 1.05
    scale = 0.55   # inches per UGX million
    gx = (w - 0.6) / len(vols)
    s.line(0.3, base, w - 0.2, base, lw=1.8)
    for i, v in enumerate(vols):
        cx = 0.5 + gx * (i + 0.5)
        rent = v / 1000
        host = 3
        bw = 0.42
        s.rect(cx - bw - 0.03, base, bw, rent * scale, fill=PAPER, edge=INK, lw=1.6)
        s.rect(cx + 0.03, base, bw, host * scale, fill=GOLD, edge=INK, lw=1.6)
        s.text(cx - bw / 2 - 0.03, base + rent * scale + 0.2, f'{rent:g}m', size=14, weight='bold')
        s.text(cx + bw / 2 + 0.03, base + host * scale + 0.2, '3m', size=14, weight='bold')
        s.text(cx, base - 0.25, f'{v:,}', size=15, weight='bold', color=RED if v == 3000 else INK)
    s.text(w / 2, base - 0.6, 'Requests a month', size=15, color=BODY)
    s.rect(0.3, h - 0.42, 0.25, 0.25, fill=PAPER, edge=INK, lw=1.4)
    s.text(0.65, h - 0.3, 'Rent: UGX 1,000 a request', size=15, ha='left')
    s.rect(3.6, h - 0.42, 0.25, 0.25, fill=GOLD, edge=INK, lw=1.4)
    s.text(3.95, h - 0.3, 'Host: UGX 3 million a month', size=15, ha='left')
    cx = 0.5 + gx * 2.5
    s.line(cx, base, cx, h - 1.12, color=RED, lw=2.6, dash=True, z=6)
    s.text(cx, h - 0.92, 'They meet', size=15, weight='bold', color=RED)
    s.text(0.1, 0.12, 'Illustrative prices in UGX millions, invented to show the idea.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ lock-in and vendor survival
@fig('x_l06_lockin')
def x_l06_lockin(w, h, **_):
    s = Scene(w, h)
    pw = (w - 0.3) / 2
    cols = [('What ties you in', 'key', ['Your data stored in their format', 'Briefs and workflows tuned to their model', 'Staff trained on their tool', 'A long contract, and prices you cannot refuse']),
            ('Will they still be here?', 'flag', ['Who owns them, and how are they funded?', 'What happens if they are bought or close?', 'Can we take our data back, in a usable format?', 'Is the exit written into the contract?'])]
    for i, (hd, ic, items) in enumerate(cols):
        x = 0.1 + i * (pw + 0.1)
        s.icon(ic, x + 0.35, h - 0.35, 0.55)
        s.text(x + 0.75, h - 0.35, hd, size=18, weight='bold', ha='left', color=RED if i else INK)
        s.line(x, h - 0.7, x + pw, h - 0.7, lw=1.6)
        for k, it in enumerate(items):
            y = h - 1.15 - k * 0.72
            s.box(x, y - 0.3, pw, 0.6, '', fill=PALE if i == 0 else PAPER, edge=HAIR, lw=1.2, r=0.06)
            _wrap(s, x + 0.15, y, pw - 0.3, it, 15, ha='left', color=BODY)
    s.text(0.1, 0.395, 'Every question on the right has an answer you can write into the contract.', size=16, weight='bold', ha='left')
    return s


# ------------------------------------------------------------------ benchmarks: someone else's test
@fig('x_l06_bench')
def x_l06_bench(w, h, **_):
    from matplotlib.patches import Circle
    s = Scene(w, h)
    cy = h - 1.45
    s.ax.add_patch(Circle((1.45, cy), 1.25, fc=PALE, ec=INK, lw=1.8, zorder=2))
    s.ax.add_patch(Circle((3.35, cy), 1.0, fc=GOLD, ec=INK, lw=1.8, zorder=3, alpha=0.9))
    _wrap(s, 0.95, cy, 1.2, 'The benchmark’s fixed questions', 15, weight='bold')
    _wrap(s, 3.6, cy, 1.15, 'Your own work', 15, weight='bold')
    s.text(2.45, cy - 1.45, 'They overlap only a little', size=15, color=RED, weight='bold')
    cards = [('It may have seen the answers', 'Test questions leak into its training text.'),
             ('The settings differ', 'One try or five, with or without examples.'),
             ('The builder may mark its own test', 'Ask who set it and who scored it.')]
    x = 4.85
    for k, (hd, t) in enumerate(cards):
        y = h - 0.1 - k * 1.42
        s.box(x, y - 1.3, w - x - 0.1, 1.3, '', fill=PAPER, lw=1.6, r=0.08)
        hh = _wrap(s, x + 0.15, y - 0.12, w - x - 0.4, hd, 15, weight='bold', ha='left', va='top')
        _wrap(s, x + 0.15, y - 0.2 - hh, w - x - 0.4, t, 14, ha='left', color=BODY, va='top')
    s.text(0.1, 0.2, 'A benchmark is a fixed public test, like the vendor’s 95% in Session 3.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ the three routes compared on the four questions
@fig('x_l06_route_grid')
def x_l06_route_grid(w, h, **_):
    s = Scene(w, h)
    lab_w = 2.3
    cw = (w - 0.1 - lab_w) / 3
    heads = ['Rent', 'Host', 'Build on a partner']
    rows = [('Data location', [('Vendor’s computers, often abroad', 0), ('Where you choose', 1), ('Partner’s cloud region', 0)]),
            ('Cost per use', [('Cheapest at low volume', 1), ('Cheapest at high volume, plus staff', 1), ('Fixed by a contract over years', 0)]),
            ('Lock-in', [('Moderate: briefs and habits', 0), ('Lowest: you hold the file', 1), ('Highest: data and work on their platform', 0)]),
            ('Vendor survival', [('Your service ends with theirs', 0), ('You keep the model if the maker stops', 1), ('Tied to the partner for years', 0)]),
            ('Time to start', [('Days', 1), ('Weeks to months', 0), ('Months', 0)])]
    top = h - 0.6
    rh = (top - 0.55) / len(rows)
    for j, hd in enumerate(heads):
        s.text(0.1 + lab_w + j * cw + cw / 2, h - 0.3, hd, size=18, weight='bold')
    for r, (lab, cells) in enumerate(rows):
        y = top - r * rh
        _wrap(s, 0.15, y - rh / 2, lab_w - 0.2, lab, 16, weight='bold', ha='left')
        for j, (t, good) in enumerate(cells):
            x = 0.1 + lab_w + j * cw
            s.rect(x + 0.05, y - rh + 0.05, cw - 0.1, rh - 0.08, fill=GOLD if good else PAPER, edge=INK if good else HAIR, lw=1.2, z=1)
            _wrap(s, x + cw / 2, y - rh / 2 + 0.01, cw - 0.3, t, 15, color=INK if good else BODY)
    s.rect(0.15, 0.12, 0.25, 0.25, fill=GOLD, edge=INK, lw=1.2)
    s.text(0.5, 0.245, 'a strength of that route. General tendencies: check each offer on its own terms.', size=14, ha='left', color=MUTE)
    return s


# ------------------------------------------------------------------ industry tour: six industries
@fig('x_l06_six')
def x_l06_six(w, h, **_):
    s = Scene(w, h)
    tiles = [('calculator', 'Banking and microfinance', 'Rents AI from several vendors at once', 'Absa: Microsoft, Amazon, Salesforce'),
             ('phone', 'Telecom and mobile money', 'Plans to adapt global models to local languages', 'Orange: Wolof and Pulaar, with OpenAI and Meta'),
             ('plant', 'Agriculture and agribusiness', 'Builds a farmer chatbot on a vendor’s template', 'ITC Krishi Mitra, India, on Microsoft'),
             ('bottle', 'Manufacturing and FMCG', 'Gives staff its own approved assistant', 'Nestlé: NesGPT'),
             ('clinic', 'Healthcare and insurance', 'Builds its own model on an open one', 'Jacaranda Health, Kenya: UlizaLlama'),
             ('people', 'Public sector', 'Backs a model for its own languages', 'Uganda: Sunflower, with Sunbird AI')]
    _six(s, w, h, tiles, 'Sources: TechCentral 2026; Capacity 2024; ITC 2024; WorkLife 2024; IDRC 2025; Ministry of ICT 2025. Company figures where stated.')
    return s


# ------------------------------------------------------------------ demonstration: the two replies (recorded, s06)
@fig('x_l06_two_answers')
def x_l06_two_answers(w, h, **_):
    s = Scene(w, h)
    pw = (w - 0.3) / 2
    panels = [('A hosted assistant: Claude', 'Fresh session, one run, 6 November 2026', [
                ('“Your payment of UGX 1,560,000 for 20 bags at UGX 78,000 matches the price list.', False),
                ('We have passed your complaint to our team, who will check the delivery and your MoMo payment and contact you.', False),
                ('Please keep the damaged bags and, if you can, send photos.”', False)],
               'No refund or date promised: the company gave none. 59 words.'),
              ('A small open model on a laptop: Qwen 2.5, 1.5 billion', 'Greedy run, one of three, 6 November 2026', [
                ('“... the correct charge should be based on the actual number of usable bags received, which is 17 bags ...', True),
                ('For the 17 usable bags: UGX 1,326,000.', True),
                ('Please settle the remaining balance within two business days ...”', True)],
               'Other runs invented a waived fee and a replacement.')]
    for i, (hd, sub, lines, foot) in enumerate(panels):
        x = 0.1 + i * (pw + 0.1)
        s.box(x, 0.1, pw, h - 0.2, '', fill=PAPER, lw=1.8, r=0.08, edge=RED if i else INK)
        _wrap(s, x + 0.2, h - 0.4, pw - 0.4, hd, 16, weight='bold', ha='left', color=RED if i else INK)
        s.text(x + 0.2, h - 0.78, sub, size=14, color=MUTE, ha='left')
        top = h - 1.08
        for t, bad in lines:
            n = len(K.wrap(t, 15, 'italic', pw - 0.5))
            hh = n * _lh(15)
            if bad:
                s.rect(x + 0.15, top - hh - 0.04, pw - 0.3, hh + 0.08, fill=GOLD, edge=GOLD, lw=0.5, z=3)
            _wrap(s, x + 0.25, top - hh / 2, pw - 0.5, t, 15, ha='left', italic=True, color=INK)
            top -= hh + 0.14
        _wrap(s, x + 0.2, 0.45, pw - 0.4, foot, 15, weight='bold', ha='left', color=RED if i else INK)
    return s


# ------------------------------------------------------------------ demonstration: five checks (recorded, s06)
@fig('x_l06_scorecard')
def x_l06_scorecard(w, h, **_):
    s = Scene(w, h)
    cols = ['Claude\none run', 'Qwen 1.5B\nrun 1', 'Qwen 1.5B\nrun 2', 'Qwen 1.5B\nrun 3']
    rows = [('Label: product quality (my judgement)', [1, 0, 0, 0]), ('Sum checked: UGX 1,560,000 matches', [1, 1, 1, 1]), ('Reply within 70 words', [1, 0, 0, 0]),
            ('Invents nothing the company never said', [1, 0, 0, 0]), ('Says what it cannot confirm', [1, 0, 0, 0])]
    lw_ = 5.0
    cw = (w - lw_ - 0.2) / 4
    top = h - 0.1
    hh = 0.75
    for j, c in enumerate(cols):
        s.text(lw_ + 0.1 + j * cw + cw / 2, top - hh / 2, c, size=15, weight='bold')
    rh = (top - hh - 0.65) / len(rows)
    for i, (nm, vals) in enumerate(rows):
        y = top - hh - (i + 1) * rh
        s.line(0.1, y + rh, w - 0.1, y + rh, color=HAIR, lw=1)
        s.text(0.15, y + rh / 2, nm, size=16, ha='left')
        for j, v in enumerate(vals):
            s.icon('check' if v else 'cross', lw_ + 0.1 + j * cw + cw / 2, y + rh / 2, 0.4)
    y = 0.1
    s.rect(0.1, y, w - 0.2, 0.5, fill=PALE, edge=INK, lw=1.2)
    s.text(0.15, y + 0.25, 'Checks passed', size=16, weight='bold', ha='left')
    for j, t in enumerate(['5 of 5', '1 of 5', '1 of 5', '1 of 5']):
        s.text(lw_ + 0.1 + j * cw + cw / 2, y + 0.25, t, size=16, weight='bold', color=INK if j == 0 else RED)
    return s


# ------------------------------------------------------------------ your people: four seats at one table
@fig('x_l06_people')
def x_l06_people(w, h, **_):
    s = Scene(w, h)
    cx, cy = w / 2, h / 2 - 0.05
    s.box(cx - 1.7, cy - 0.65, 3.4, 1.3, '', fill=GOLD, lw=2, r=0.12)
    _wrap(s, cx, cy + 0.22, 3.1, 'The vendor decision', 17, weight='bold')
    _wrap(s, cx, cy - 0.25, 3.1, 'One named owner: the business head who uses it', 14)
    seats = [(0.1, h - 0.1, 'IT lead', 'Where does it run? Is it secure? How do we leave?', 'gear'),
             (w - 3.75, h - 0.1, 'Procurement', 'Cost per use at our volume, price changes, contract length', 'receipt'),
             (0.1, 1.5, 'Legal and data protection', 'PDPO registration, data leaving Uganda, consent', 'shield'),
             (w - 3.75, 1.5, 'The business owner', 'Does it work on our own tasks? Who checks the output?', 'person')]
    for x, ytop, role, q, ic in seats:
        s.box(x, ytop - 1.45, 3.65, 1.45, '', fill=PAPER, lw=1.6, r=0.08)
        s.icon(ic, x + 0.4, ytop - 0.4, 0.55, **({'text': ''} if ic == 'coin' else {}))
        s.text(x + 0.8, ytop - 0.4, role, size=16, weight='bold', ha='left')
        _wrap(s, x + 0.2, ytop - 0.98, 3.3, q, 14, ha='left', color=BODY)
    for (x, ytop, *_r) in seats:
        mx = x + 3.65 if x < cx else x
        my = ytop - 0.72
        s.line(mx, my, cx - 1.7 if x < cx else cx + 1.7, cy, color=INK, lw=1.4, z=1)
    return s


# ------------------------------------------------------------------ hands-on: one portfolio entry with its route (fictional company)
@fig('x_l06_portfolio')
def x_l06_portfolio(w, h, **_):
    s = Scene(w, h)
    rows = [('The use', 'Draft replies to shop complaints for staff to check'),
            ('What goes in', 'The complaint, the order and the price list'),
            ('What comes out', 'A draft reply, flagged where unsure'),
            ('Who uses it', 'Customer service officers'),
            ('How we would know it works', 'Tested on 10 past complaints: count the good drafts'),
            ('Today: route, data, exit', 'Rent; names and orders go to the vendor, so read the data terms; export briefs monthly')]
    s.text(0.05, h - 0.2, 'Nile Valley Foods (fictional): one entry', size=15, weight='bold', ha='left')
    lw_ = 1.85
    vw = w - 0.1 - lw_
    hs = []
    for a, b in rows:
        n = max(len(K.wrap(a, 14, 'bold', lw_ - 0.15)), len(K.wrap(b, 14, 'regular', vw - 0.15)))
        hs.append(n * _lh(14) + 0.1)
    y = h - 0.42
    for i, ((a, b), rh) in enumerate(zip(rows, hs)):
        last = i == len(rows) - 1
        s.rect(0.05, y - rh, lw_, rh, fill=GOLD if last else PALE, edge=INK, lw=1.0)
        s.rect(0.05 + lw_, y - rh, vw, rh, fill=PAPER, edge=INK, lw=1.0)
        _wrap(s, 0.12, y - rh / 2, lw_ - 0.15, a, 14, weight='bold', ha='left')
        _wrap(s, 0.12 + lw_, y - rh / 2, vw - 0.15, b, 14, ha='left', color=BODY)
        y -= rh
    return s
