"""Figures for Leadership Edition Session 7, Getting good work from AI assistants: prompting for leaders and teams.  Names: x_l07_*  (content kind 'l07_*').

No maths anywhere: pictures and counts only.  Every assistant reply quoted here is a recorded run, copied verbatim (shortened with '...'):
demo_runs/s08/runs/T1 to T6 (Claude, fresh subagent sessions, 11 November 2026, one run each); the weak and strong brief (Executive Edition
Case Runs F1a and F1b, Claude, fresh subagent sessions, 4 November 2026, one run each); the payroll runs R2 to R5 (Claude, fresh subagent sessions,
6 November 2026, ten runs).  Case figures come from research/*.md (IDs in the content file).  Nile Valley Foods is fictional.
"""
from figkit import Scene, INK, BODY, MUTE, HAIR, PALE, PAPER, RED, GOLD, fig
import slidekit as K
from diagrams_l02 import _wrap, _lh, _source
from diagrams_l06 import _six


def _para(s, x, top, w, text, size=15, weight='normal', color=INK, italic=False, hl=False, gap=0.1):
    """A wrapped paragraph from `top` downwards, optionally on a gold band. Returns the new top."""
    kind = 'italic' if italic else ('bold' if weight == 'bold' else 'regular')
    n = len(K.wrap(text, size, kind, w))
    hh = n * _lh(size)
    if hl:
        s.rect(x - 0.08, top - hh - 0.05, w + 0.16, hh + 0.1, fill=GOLD, edge=GOLD, lw=0.5, z=3)
    _wrap(s, x, top - hh / 2, w, text, size, weight=weight, color=color, ha='left', italic=italic)
    return top - hh - gap


# ------------------------------------------------------------------ recall bridge: Session 6 to today
@fig('x_l07_bridge')
def x_l07_bridge(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.3, 'Session 6: a route', size=17, weight='bold', ha='left')
    s.line(0.1, h - 0.55, 2.2, h - 0.55, lw=1.6)
    for i, (ic, t) in enumerate((('cloud', 'Rent'), ('home', 'Host'), ('gear', 'Partner'))):
        y = h - 1.15 - i * 0.85
        s.box(0.1, y - 0.33, 2.0, 0.66, '', fill=GOLD if i == 0 else PAPER, lw=1.6, r=0.08)
        s.icon(ic, 0.5, y, 0.48)
        s.text(0.9, y, t, size=16, weight='bold', ha='left')
    s.arrow(2.2, h - 2.0, 2.55, h - 2.0, lw=2.4, head=16)
    x0 = 2.7
    s.text(x0, h - 0.3, 'Today: the same tool, two briefs', size=17, weight='bold', ha='left', color=RED)
    s.line(x0, h - 0.55, w - 0.1, h - 0.55, lw=1.6, color=RED)
    rows = [('Write the Monday sales email.', 'Invented advice; signed “[Your name]”', 'cross'),
            ('Role, reader, format; use only these figures', 'Kept the format; said what the data cannot show', 'check')]
    for i, (brief, out, ic) in enumerate(rows):
        y = h - 1.35 - i * 1.4
        s.box(x0, y - 0.55, 1.9, 1.1, '', fill=PAPER, lw=1.6, r=0.08)
        _wrap(s, x0 + 0.95, y, 1.7, brief, 14, italic=True)
        s.arrow(x0 + 1.95, y, x0 + 2.25, y, lw=2, head=14)
        s.box(x0 + 2.3, y - 0.55, w - x0 - 2.4, 1.1, '', fill=GOLD if ic == 'check' else PAPER, lw=1.6, r=0.08)
        s.icon(ic, x0 + 2.62, y, 0.42)
        _wrap(s, x0 + 2.92, y, w - x0 - 3.1, out, 14, ha='left')
    _wrap(s, w / 2, 0.35, w - 0.3, 'Same assistant, same figures, different work. Recorded runs, 4 November 2026.', 15, weight='bold', color=RED)
    return s


# ------------------------------------------------------------------ hook: the UK civil service trial (PUB-10)
@fig('x_l07_ukgov')
def x_l07_ukgov(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.28, 'UK civil service, September to December 2024', size=17, weight='bold', ha='left')
    s.box(0.1, h - 2.05, 3.5, 1.5, '', fill=PAPER, lw=1.8, r=0.08)
    s.icon('people', 0.6, h - 1.3, 0.75)
    s.text(1.1, h - 1.05, '20,000+', size=24, weight='bold', ha='left')
    _wrap(s, 1.1, h - 1.6, 2.4, 'civil servants got an assistant in Word, Outlook and Teams', 14, ha='left', color=BODY)
    tasks = [('doc', 'Draft documents'), ('people', 'Summarise meetings'), ('mail', 'Handle email')]
    for i, (ic, t) in enumerate(tasks):
        y = h - 2.55 - i * 0.55
        s.icon(ic, 0.45, y, 0.42)
        s.text(0.8, y, t, size=15, ha='left')
    s.box(3.85, h - 2.05, w - 3.95, 1.5, '', fill=GOLD, lw=1.8, r=0.08)
    s.text(3.85 + (w - 3.95) / 2, h - 1.0, '26 minutes a day', size=24, weight='bold')
    _wrap(s, 3.85 + (w - 3.95) / 2, h - 1.6, w - 4.2, 'saved per person, as they reported it: nearly 2 working weeks a year', 14)
    s.box(3.85, 0.55, w - 3.95, 1.7, '', fill=PAPER, edge=RED, lw=2, r=0.08)
    s.text(4.0, 1.98, 'The catch', size=16, weight='bold', color=RED, ha='left')
    _wrap(s, 4.0, 1.25, w - 4.25, 'Staff estimated the time themselves; no one timed the work. One report says 17 in 100 saved no time.', 14, ha='left', color=BODY)
    _source(s, 'Sources: GOV.UK, 2 June 2025; The Register (17 in 100).', y=0.2)
    return s


# ------------------------------------------------------------------ a prompt is a brief to a new colleague
@fig('x_l07_newhire')
def x_l07_newhire(w, h, **_):
    s = Scene(w, h)
    s.icon('person', 0.85, h / 2 + 0.25, 1.3)
    _wrap(s, 0.85, h / 2 - 0.85, 1.5, 'A capable new colleague, day one', 14, weight='bold')
    parts = [('Who should I be?', 'Role', 'who is speaking, at what level'),
             ('What is going on?', 'Context', 'your situation and your reader'),
             ('What does good look like?', 'Examples', 'one or two finished pieces'),
             ('What shape, how long?', 'Format', 'the layout and the length'),
             ('What must I not do?', 'Constraints', 'the limits; what to say if unsure')]
    rh = (h - 0.2) / len(parts)
    for i, (q, part, plain) in enumerate(parts):
        y = h - 0.1 - (i + 0.5) * rh
        s.box(1.62, y - 0.3, 2.3, 0.6, '', fill=PAPER, lw=1.4, r=0.15)
        s.text(2.77, y, q, size=14, italic=True)
        s.arrow(3.95, y, 4.2, y, lw=2, head=13)
        s.box(4.25, y - 0.36, w - 4.35, 0.72, '', fill=GOLD if i == 4 else PALE, lw=1.4, r=0.06)
        s.text(4.4, y + 0.13, part, size=15, weight='bold', ha='left')
        s.text(4.4, y - 0.17, plain, size=14, ha='left', color=BODY)
    return s


# ------------------------------------------------------------------ before and after, one part of a brief at a time (recorded T1 to T6)
_BA = {
    'role': dict(before='Explain what inflation is. Answer in at most 60 words.',
                 before_reply=[('“Inflation is the general rise in prices across an economy over time ...', False),
                               ('It is usually measured yearly with a price index such as the Consumer Price Index ... rapid growth in the money supply.”', False)],
                 change='+ You are a primary school teacher talking to a class of ten-year-olds.',
                 after_reply=[('“Imagine a chocolate bar costs 1,000 shillings today. Next year, the same bar costs 1,200 shillings.', True),
                              ('The chocolate didn’t change, but the price went up. That’s inflation!”', False)],
                 foot=('Written for an economist', 'Written for a child: same idea, new level')),
    'context': dict(before='Suggest a dinner I can cook tonight. Answer in at most 60 words.',
                    before_reply=[('“Try a lemon-garlic chicken stir-fry ... bell peppers, broccoli and snap peas.', False),
                                  ('Stir in soy sauce, honey, lemon juice ...”', False)],
                    change='+ We are four people and one of us is vegetarian. We have beans, rice, tomatoes and onions at home, and I have 45 minutes.',
                    after_reply=[('“Make a vegetarian bean and tomato stew over rice ...', False),
                                 ('... add diced tomatoes, garlic, cumin, paprika and salt ... with a fried egg on top for anyone who wants one.”', True)],
                    foot=('Nothing it could know about us', 'It fits us, and still added what we never listed')),
    'examples': dict(before='Label each mobile money SMS below. 1. You have received UGX 8,000 from John. 2. You have paid UGX 35,000 to Kampala Water. 3. ...',
                     before_reply=[('“1. ... is Money In (Received) ...  2. ... is Money Out (Bill Payment) ...', False),
                                   ('Totals: UGX 128,000 in and UGX 35,000 out, so you are UGX 93,000 up.”', False)],
                     change='+ Two finished examples first:  You have received UGX 20,000 from Mary. Label: IN   You have sent UGX 50,000 to Peter. Label: OUT',
                     after_reply=[('“1. IN   2. OUT   3. IN”', True)],
                     foot=('Its own labels, and totals nobody asked for: 73 words', 'Exactly the labels and layout of the examples')),
    'format': dict(before='Compare renting and buying a house.',
                   before_reply=[('529 words under seven headings, with rules of thumb and advice to see a financial adviser.', False)],
                   change='+ Answer only with a table: two columns, three rows ... At most eight words in each cell.',
                   after_reply=[('Monthly cost | Rent, often lower upfront | Mortgage, taxes, insurance, maintenance', True),
                                ('Flexibility | Easy to move when lease ends | Selling takes time and money', True),
                                ('Risk | Rent increases; no equity built | Market drops, repairs, debt exposure', True)],
                   foot=('Correct, and too long to compare at a glance', 'A three-row table, as asked')),
    'constraints': dict(before='The context brief from two slides ago: four people, one vegetarian, beans, rice, tomatoes, onions, 45 minutes.',
                        before_reply=[('“... add diced tomatoes, garlic, cumin, paprika and salt ...', True),
                                      ('Serve it over the rice, with a fried egg on top for anyone who wants one.”', True)],
                        change='+ Use only the ingredients I listed, plus salt, oil and water. If a good dish needs anything else, say so instead of adding it.',
                        after_reply=[('“Fry the onions in oil, add chopped tomatoes and salt ...', False),
                                     ('This takes 45 minutes only if the beans are canned or precooked.', True),
                                     ('Garlic, chili or cumin would improve it, but you didn’t list them.”', True)],
                        foot=('Added four things we never mentioned', 'Kept to the list, and said what it would add')),
}


@fig('x_l07_ba')
def x_l07_ba(w, h, part='role', **_):
    d = _BA[part]
    s = Scene(w, h)
    pw = (w - 0.3) / 2
    for i, (head, prompt, reply, foot) in enumerate((('Before', d['before'], d['before_reply'], d['foot'][0]),
                                                     ('After: one change', d['change'], d['after_reply'], d['foot'][1]))):
        x = 0.1 + i * (pw + 0.1)
        s.box(x, 0.45, pw, h - 0.55, '', fill=PAPER, lw=1.8, r=0.08, edge=RED if i else INK)
        s.text(x + 0.2, h - 0.35, head, size=17, weight='bold', ha='left', color=RED if i else INK)
        s.text(x + 0.2, h - 0.72, 'Prompt', size=14, weight='bold', ha='left', color=MUTE)
        sz = 14 if part in ('format', 'constraints', 'examples') else 15
        top = _para(s, x + 0.2, h - 0.9, pw - 0.4, prompt, sz, weight='bold' if i else 'normal', gap=0.15)
        s.text(x + 0.2, top - 0.12, 'Reply', size=14, weight='bold', ha='left', color=MUTE)
        top -= 0.32
        if part == 'format' and i == 1:
            cw3 = [1.1, (pw - 1.5) / 2, (pw - 1.5) / 2]
            for t, hl in reply:
                cells = [c.strip() for c in t.split('|')]
                nl = max(len(K.wrap(c, 14, 'italic', cw3[k] - 0.1)) for k, c in enumerate(cells))
                rh = nl * _lh(14) + 0.05
                cx = x + 0.2
                for k, c in enumerate(cells):
                    s.rect(cx, top - rh, cw3[k], rh, fill=GOLD if k else PALE, edge=INK, lw=0.8, z=3)
                    _wrap(s, cx + 0.05, top - rh / 2, cw3[k] - 0.1, c, 14, ha='left', italic=k > 0, weight='bold' if k == 0 else 'normal')
                    cx += cw3[k]
                top -= rh
            reply = []
        for t, hl in reply:
            top = _para(s, x + 0.2, top, pw - 0.4, t, sz, italic=True, hl=hl and i == 1 or (hl and part == 'constraints' and i == 0), gap=0.08)
        _wrap(s, x + 0.2, 0.68, pw - 0.4, foot, 15, weight='bold', ha='left', color=RED if i else INK)
    s.text(0.1, 0.18, 'Gold: the effect to notice. Claude, fresh session, one run each, 11 November 2026.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ test a brief on ten real tasks, and count
@fig('x_l07_testset')
def x_l07_testset(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.28, 'Like testing a new cashier on ten bills whose totals you know (illustration)', size=15, weight='bold', ha='left')
    cw, ch, gap = 1.3, 1.0, 0.18
    x0 = (w - (5 * cw + 4 * gap)) / 2
    for k in range(10):
        r, c = divmod(k, 5)
        x = x0 + c * (cw + gap)
        y = h - 0.65 - (r + 1) * ch - r * gap
        wrong = k == 6
        s.box(x, y, cw, ch, '', fill=PAPER if not wrong else PALE, lw=1.6, r=0.06, edge=RED if wrong else INK)
        s.icon('receipt', x + 0.38, y + ch / 2, 0.55)
        s.text(x + 0.38, y + 0.12, str(k + 1), size=14, weight='bold')
        s.icon('cross' if wrong else 'check', x + 0.95, y + ch / 2, 0.42)
    s.box(w / 2 - 1.2, 1.25, 2.4, 0.62, '9 of 10 right', size=20, weight='bold', fill=GOLD, r=0.08)
    steps = ['Ten real tasks, answers known', 'Run the brief on all ten', 'Count the right ones', 'Change one thing, run again']
    sw = (w - 0.2 - 3 * 0.25) / 4
    for i, t in enumerate(steps):
        x = 0.1 + i * (sw + 0.25)
        s.box(x, 0.12, sw, 0.85, '', fill=PAPER, lw=1.4, r=0.06)
        _wrap(s, x + sw / 2, 0.545, sw - 0.15, t, 14)
        if i < 3:
            s.arrow(x + sw + 0.02, 0.545, x + sw + 0.23, 0.545, lw=1.8, head=12)
    return s


# ------------------------------------------------------------------ reasoning models write out their working first
@fig('x_l07_reasoning')
def x_l07_reasoning(w, h, **_):
    s = Scene(w, h)
    bh = 0.75

    def lane(y, head, items, tag, red):
        s.text(0.1, y + bh + 0.28, head, size=17, weight='bold', ha='left', color=RED if red else INK)
        x = 0.1
        for i, (txt, wd, fill) in enumerate(items):
            s.box(x, y, wd, bh, '', fill=fill, lw=1.8, r=0.08)
            _wrap(s, x + wd / 2, y + bh / 2, wd - 0.2, txt, 15, weight='bold' if fill == GOLD else 'normal')
            if i < len(items) - 1:
                s.arrow(x + wd + 0.04, y + bh / 2, x + wd + 0.3, y + bh / 2, lw=2.2, head=15)
            x += wd + 0.34
        s.text(0.1, y - 0.28, tag, size=14, color=BODY, ha='left')
    lane(h - 1.45, 'A standard model', [('Your question', 1.9, PAPER), ('The answer, straight away', 2.6, GOLD)], 'Fast. Good for well-defined work: sorting, rewriting, short summaries.', False)
    lane(h - 3.2, 'A reasoning model', [('Your question', 1.9, PAPER), ('Working: step, check, step', 2.5, PALE), ('The answer', 2.2, GOLD)],
         'Slower, and the working is paid for. Often better on many-step work. Still check it.', True)
    s.box(0.1, 0.1, w - 0.2, 0.85, '', fill=PAPER, edge=RED, lw=1.8, r=0.08)
    _wrap(s, w / 2, 0.525, w - 0.5, 'OpenAI’s, Anthropic’s and Google’s guides: state the goal, the rules and the output. You need not ask it to go step by step.', 14, weight='bold')
    return s


# ------------------------------------------------------------------ the jagged frontier (PPL-02)
@fig('x_l07_jagged')
def x_l07_jagged(w, h, **_):
    s = Scene(w, h)
    fw = 3.9
    pts = [(0.1, 0.55), (0.1, h - 0.6), (0.75, h - 0.6), (1.05, h - 1.3), (1.6, h - 0.75), (2.0, h - 1.9), (2.65, h - 1.2), (2.95, 2.1),
           (2.25, 1.55), (2.6, 0.55)]
    s.poly(pts, fill=GOLD, edge=INK, lw=2.2, z=1)
    s.text(0.2, h - 0.3, 'Where AI helps: inside the frontier', size=15, weight='bold', ha='left', z=7)
    for (x, y, t) in ((0.8, h - 1.55, 'Product ideas'), (0.8, 2.35, 'Drafting, rewriting'), (0.8, 1.3, 'Summaries')):
        s.circle(x - 0.55, y, 0.07, fill=INK, edge=INK, z=4)
        s.text(x - 0.4, y, t, size=14, ha='left', z=6)
    s.icon('cross', 3.6, 2.45, 0.42)
    _wrap(s, 3.62, 1.45, 1.15, 'A business problem with numbers and interviews', 14, color=RED, weight='bold')
    x0 = fw + 0.35
    cards = [('Inside the frontier', 'About 40% better quality on a creative product task', GOLD),
             ('Outside the frontier', '84.5% got it right without AI; 70.6% with GPT-4', PAPER)]
    for i, (hd, t, fill) in enumerate(cards):
        y = h - 0.1 - i * 1.85
        s.box(x0, y - 1.7, w - x0 - 0.1, 1.7, '', fill=fill, lw=1.8, r=0.08, edge=RED if i else INK)
        s.text(x0 + 0.15, y - 0.32, hd, size=16, weight='bold', ha='left', color=RED if i else INK)
        _wrap(s, x0 + 0.15, y - 1.0, w - x0 - 0.4, t, 15, ha='left')
    _source(s, '758 consultants, GPT-4. BCG, 21 Sep 2023; HBS AI Institute, 9 Apr 2026.', y=0.2)
    return s


# ------------------------------------------------------------------ good at, bad at
@fig('x_l07_good_bad')
def x_l07_good_bad(w, h, **_):
    s = Scene(w, h)
    cols = [('Good at', 'check', ['First drafts, rewrites and summaries', 'Changing level and tone for a reader', 'Sorting and labelling to your examples', 'Ideas to start from']),
            ('Watch closely', 'cross', ['Facts and figures it was not given', 'Sums: re-add the lines yourself', 'Your own policies and prices', 'Tasks outside the frontier'])]
    cw = (w - 0.3) / 2
    for i, (hd, ic, items) in enumerate(cols):
        x = 0.1 + i * (cw + 0.1)
        s.text(x + 0.1, h - 0.35, hd, size=20, weight='bold', ha='left', color=RED if i else INK)
        s.line(x, h - 0.65, x + cw, h - 0.65, lw=1.8)
        for k, it in enumerate(items):
            y = h - 1.25 - k * 0.98
            s.icon(ic, x + 0.35, y, 0.6)
            _wrap(s, x + 0.8, y, cw - 0.95, it, 16, ha='left', color=BODY)
    return s


# ------------------------------------------------------------------ industry tour: six industries
@fig('x_l07_six')
def x_l07_six(w, h, **_):
    s = Scene(w, h)
    tiles = [('calculator', 'Banking and microfinance', 'Office assistant for every desk', 'Absa: 30,000+ staff a month'),
             ('phone', 'Telecom and mobile money', 'Assistants licensed across the company', 'Telstra: 18,000 Copilot licences'),
             ('plant', 'Agriculture and agribusiness', 'Farmers ask by voice in their own language', 'ITC Krishi Mitra, India'),
             ('bottle', 'Manufacturing and FMCG', 'Teams generate and refine product ideas', 'Procter & Gamble, about 780 staff'),
             ('clinic', 'Healthcare and insurance', 'Flags possible errors while clinicians work', 'Penda Health, Kenya'),
             ('people', 'Public sector', 'Teachers set the prompts for an AI tutor', 'Edo State, Nigeria')]
    _six(s, w, h, tiles, 'Sources: TechCentral 2026; Telstra 2026; ITC 2024; HBS 2025; arXiv 2025; World Bank 2025. Company figures where stated.')
    return s


# ------------------------------------------------------------------ demonstration: weak and strong brief (recorded F1a, F1b)
@fig('x_l07_weak_strong')
def x_l07_weak_strong(w, h, **_):
    s = Scene(w, h)
    pw = (w - 0.3) / 2
    panels = [('Weak brief', '“Write the Monday sales email.” + the figures', [
                ('“Revenue for the week starting 19 October was UGX 739,684,000 ... (4.3%) more ...', False),
                ('Please keep stock of beans and sugar high, as demand is rising on both.', True),
                ('Regards, [Your name]”', True)], 'Figures right; advice nobody asked for'),
              ('Strong brief', 'Role, reader, format, “use only the figures below” + the same figures', [
                ('“Subject: Monday sales: week of 19 Oct, UGX 739.7M, up 4.3%', False),
                ('Beans grew fastest at 9.0% ... The data does not show why volumes rose.', True),
                ('To check: ask the sales team whether the beans jump came from a particular order or promotion.”', True)],
               'Figures right; it said what the data cannot show')]
    for i, (hd, sub, lines, foot) in enumerate(panels):
        x = 0.1 + i * (pw + 0.1)
        s.box(x, 0.45, pw, h - 0.55, '', fill=PAPER, lw=1.8, r=0.08, edge=RED if i else INK)
        s.text(x + 0.2, h - 0.35, hd, size=17, weight='bold', ha='left', color=RED if i else INK)
        top = _para(s, x + 0.2, h - 0.6, pw - 0.4, sub, 14, color=MUTE, gap=0.18)
        for t, hl in lines:
            top = _para(s, x + 0.2, top, pw - 0.4, t, 15, italic=True, hl=hl, gap=0.12)
        _wrap(s, x + 0.2, 0.75, pw - 0.4, foot, 15, weight='bold', ha='left', color=RED if i else INK)
    s.text(0.1, 0.18, 'Gold: left, what nobody asked for; right, what the brief asked for. Claude, fresh session, one run each, 4 November 2026.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ the strong brief taken apart (F1b prompt)
@fig('x_l07_taken_apart')
def x_l07_taken_apart(w, h, **_):
    s = Scene(w, h)
    rows = [('Role', 'You are the sales analyst at Nile Valley Foods Ltd, a food distributor in Jinja, Uganda.', PALE),
            ('Context', 'Write the Monday sales email to the Sales Director, Sarah Namukasa.', PALE),
            ('Examples', 'None in this brief. When the layout matters, paste one past email and say: like this.', PAPER),
            ('Format', 'A subject line, a two-sentence summary, a short table, at most three plain sentences. Under 150 words. Brief, plain, no hype.', PALE),
            ('Constraints', 'Use only the figures below. Do not invent any number, cause or customer. If something cannot be explained from the data, say so.', GOLD)]
    lab_w = 2.0
    top = h - 0.1
    rh = (top - 0.5) / len(rows)
    for i, (lab, txt, fill) in enumerate(rows):
        y = top - i * rh
        s.rect(0.1, y - rh + 0.04, lab_w, rh - 0.08, fill=INK if fill != PAPER else PAPER, edge=INK, lw=1.4)
        s.text(0.25, y - rh / 2, lab, size=17, weight='bold', ha='left', color=PAPER if fill != PAPER else MUTE)
        s.rect(0.1 + lab_w, y - rh + 0.04, w - 0.2 - lab_w, rh - 0.08, fill=fill, edge=INK, lw=1.4)
        _wrap(s, 0.3 + lab_w, y - rh / 2, w - 0.6 - lab_w, txt, 15, ha='left', italic=fill != PAPER, color=INK if fill != PAPER else MUTE)
    s.text(0.1, 0.2, 'The strong brief of the recorded run, word for word, sorted into the five parts. Nile Valley Foods is fictional.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ one payroll sum, ten recorded runs (R2 to R5)
@fig('x_l07_payroll')
def x_l07_payroll(w, h, **_):
    s = Scene(w, h)
    groups = [('Plain', 'the facts and the question', [1, 0]),
              ('Plain + re-add', 'one closing line: check by re-adding', [1, 1, 1]),
              ('Framed', 'goal, rules and output stated first', [1, 1, 1]),
              ('Framed + re-add', 'both', [1, 1])]
    gw = 1.75
    x = 0.1
    for name, plain, runs in groups:
        s.text(x + gw / 2, h - 0.3, name, size=16, weight='bold')
        _wrap(s, x + gw / 2, h - 0.8, gw - 0.1, plain, 14, color=BODY)
        for k, ok in enumerate(runs):
            y = h - 1.6 - k * 0.62
            s.box(x + 0.25, y - 0.26, gw - 0.5, 0.52, '', fill=PAPER if ok else PALE, edge=INK if ok else RED, lw=1.6, r=0.06)
            s.text(x + 0.45, y, f'run {k + 1}', size=14, ha='left')
            s.icon('check' if ok else 'cross', x + gw - 0.5, y, 0.36)
        s.text(x + gw / 2, 0.75, f'{sum(runs)} of {len(runs)}', size=20, weight='bold', color=RED if sum(runs) < len(runs) else INK)
        x += gw + 0.12
    x0 = 7.75
    s.box(x0, 0.45, w - x0 - 0.1, h - 0.55, '', fill=PAPER, edge=RED, lw=2, r=0.08)
    s.text(x0 + 0.2, h - 0.35, 'The one wrong run', size=17, weight='bold', color=RED, ha='left')
    top = _para(s, x0 + 0.2, h - 0.7, w - x0 - 0.5, 'Gross pay 1,855,682 shillings; the key says 2,055,682.', 15, weight='bold', gap=0.15)
    top = _para(s, x0 + 0.2, top, w - x0 - 0.5, 'A slip of 200,000 in one addition, so the net pay came out 190,000 short.', 15, color=BODY, gap=0.15)
    _para(s, x0 + 0.2, top, w - x0 - 0.5, 'Every line was shown, and it sounded sure.', 15, weight='bold', hl=True)
    s.text(0.1, 0.25, '9 of 10 right in all. Claude, fresh sessions, 6 November 2026. Too few runs to say which change helps.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ your people: who gains, training, permission (PPL-01, BNK-01, PPL-11, PPL-12)
@fig('x_l07_people')
def x_l07_people(w, h, **_):
    s = Scene(w, h)
    pw = (w - 0.4) / 3
    heads = [('Who gains most', 'people'), ('Who is trained', 'book'), ('Who uses it anyway', 'phone')]
    for i, (hd, ic) in enumerate(heads):
        x = 0.1 + i * (pw + 0.1)
        s.box(x, 0.45, pw, h - 0.55, '', fill=PAPER, lw=1.8, r=0.08)
        s.icon(ic, x + 0.4, h - 0.45, 0.55)
        s.text(x + 0.8, h - 0.45, hd, size=17, weight='bold', ha='left')
    # panel 1: NBER support agents
    x = 0.1
    bars = [('All 5,179 agents', 14, INK), ('Newest, least skilled', 34, GOLD)]
    for k, (lab, v, col) in enumerate(bars):
        y = h - 1.35 - k * 0.8
        s.text(x + 0.2, y + 0.22, lab, size=14, ha='left', color=BODY)
        s.rect(x + 0.2, y - 0.2, (pw - 1.3) * v / 34, 0.3, fill=col, edge=INK, lw=1.2)
        s.text(x + 0.3 + (pw - 1.3) * v / 34, y - 0.05, f'+{v}%', size=15, weight='bold', ha='left')
    _wrap(s, x + pw / 2, 1.35, pw - 0.3, 'more issues resolved per hour, with an assistant suggesting replies. The most experienced: little change.', 14, color=BODY)
    # panel 2: Equity training
    x = 0.1 + pw + 0.1
    s.text(x + pw / 2, h - 1.35, '7,300', size=30, weight='bold')
    _wrap(s, x + pw / 2, h - 2.0, pw - 0.3, 'of 11,900 Equity Group staff trained in generative AI: over 62 in 100', 15)
    _wrap(s, x + pw / 2, 1.35, pw - 0.3, 'Mandatory, every role. Training counts, with no business result published yet.', 14, color=BODY)
    # panel 3: shadow AI
    x = 0.1 + 2 * (pw + 0.1)
    for k, (v, t) in enumerate(((78, 'of AI users bring their own tools'), (39, 'had AI training from their employer'), (54, 'would use AI even if not authorised'))):
        y = h - 1.3 - k * 0.72
        s.text(x + 0.2, y, f'{v}%', size=20, weight='bold', ha='left', color=RED if k != 1 else INK)
        _wrap(s, x + 1.05, y, pw - 1.2, t, 14, ha='left', color=BODY)
    _wrap(s, x + pw / 2, 1.0, pw - 0.3, 'Session 0 called this shadow AI.', 14, weight='bold')
    _source(s, 'Sources: NBER 2023 (QJE 2025); TechTrends Kenya, 25 Mar 2026; Microsoft and LinkedIn, May 2024; BCG, June 2025.', y=0.2)
    return s


# ------------------------------------------------------------------ what a leader provides
@fig('x_l07_provide')
def x_l07_provide(w, h, **_):
    s = Scene(w, h)
    s.poly([(0.1, h - 0.95), (w / 2, h - 0.1), (w - 0.1, h - 0.95)], fill=INK, edge=INK, lw=1.6)
    s.text(w / 2, h - 0.68, 'What a leader provides', size=16, weight='bold', color=PAPER)
    cols = [('shield', 'An approved tool', 'So staff stop pasting work into their own', 'Nestlé: NesGPT, 7,000+ US staff in 3 months'),
            ('book', 'Training', 'How to brief, test and check', 'Equity: mandatory, every role'),
            ('folder', 'A shared library of tested briefs', 'Each with its owner, version and count', 'Your Reusable Brief Template')]
    gap = 0.15
    cw = (w - 0.2 - 2 * gap) / 3
    for i, (ic, hd, t, ex) in enumerate(cols):
        x = 0.1 + i * (cw + gap)
        s.box(x, 0.75, cw, h - 1.85, '', fill=GOLD if i == 2 else PAPER, lw=1.8, r=0.06)
        s.icon(ic, x + cw / 2, h - 1.55, 0.6)
        top = h - 2.0
        hh = _wrap(s, x + cw / 2, top, cw - 0.2, hd, 16, weight='bold', va='top')
        _wrap(s, x + cw / 2, top - hh - 0.12, cw - 0.2, t, 14, color=BODY, va='top')
        _wrap(s, x + cw / 2, 1.25, cw - 0.2, ex, 14, weight='bold', color=RED if i < 2 else INK)
    s.rect(0.1, 0.55, w - 0.2, 0.2, fill=INK, edge=INK)
    s.text(0.1, 0.2, 'Sources: WorkLife (Digiday), 23 Jul 2024; TechTrends Kenya, 25 Mar 2026.', size=14, color=MUTE, ha='left')
    return s


# ------------------------------------------------------------------ hands-on: one team task with its tested brief (fictional company)
@fig('x_l07_portfolio')
def x_l07_portfolio(w, h, **_):
    s = Scene(w, h)
    rows = [('The use', 'Draft the Monday sales email for the Sales Director'),
            ('What goes in', 'Last two weeks of sales by product'),
            ('What comes out', 'Subject, summary, table, three sentences'),
            ('Who uses it', 'The sales analyst, who checks and sends'),
            ('How we would know it works', 'Run on 10 past weeks: count the right ones'),
            ('Today: the tested brief', 'Five parts written; 10 past weeks to run and count')]
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
