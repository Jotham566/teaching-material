"""Figures for Session 9: giving a model your knowledge (retrieval, long context, fine-tuning).

Real data drawn here comes from Build/demo_runs/s09/ (retrieve.py, chunking.py, lora_style.py, tokens_output.txt and the recorded runs in runs/).
Registered as x_t09_<name>; content refers to them with dict(kind='t09_<name>').
"""
from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD, fig
import slidekit as K


def wt(s, x, y, w, text, size=16, weight='normal', color=INK, ha='center', va='center'):
    """Wrapped text in a column of width w, centred at (x, y); returns the height used in inches."""
    lines = K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', w)
    s.text(x, y, '\n'.join(lines), size=size, weight=weight, color=color, ha=ha, va=va)
    return len(lines) * size * 1.15 / 72.0


def nlines(text, size, w, weight='normal'):
    return len(K.wrap(text, size, 'bold' if weight == 'bold' else 'regular', w))


# ------------------------------------------------------------------ what a model has in front of it
@fig('x_t09_knowledge')
def knowledge(w, h, **_):
    s = Scene(w, h)
    bw, bh = 3.0, 1.2
    ys = [h - 1.45, h / 2 - 0.6, 0.25]
    items = [('book', 'Learned in training, up to a cut-off date', False), ('doc', 'Your prompt and pasted text, inside the context window', False),
             ('folder', 'Your files and handbook: not seen', True)]
    mx, mw = 4.15, 1.9
    s.box(mx, h / 2 - 1.0, mw, 2.0, '', fill=GOLD, lw=2.2)
    s.icon('robot', mx + mw / 2, h / 2 + 0.35, 0.85)
    s.text(mx + mw / 2, h / 2 - 0.5, 'The model', size=19, weight='bold')
    for (ic, t, red), y in zip(items, ys):
        s.box(0.1, y, bw, bh, '', lw=1.8, dash=red, edge=RED if red else INK)
        s.icon(ic, 0.7, y + bh / 2, 0.65)
        wt(s, 2.15, y + bh / 2, 1.75, t, 16, color=RED if red else INK, weight='bold' if red else 'normal')
        s.arrow(0.1 + bw + 0.05, y + bh / 2, mx - 0.05, h / 2 + (y + bh / 2 - h / 2) * 0.35, lw=2.2, color=RED if red else INK, dash=red)
    s.arrow(mx + mw + 0.05, h / 2, mx + mw + 0.4, h / 2, lw=2.4)
    return s


# ------------------------------------------------------------------ the ladder
@fig('x_t09_ladder')
def ladder(w, h, **_):
    s = Scene(w, h)
    cols = [('1  Prompting', 'Changes the instructions', 'Paste the page you need into the prompt', 'Start here'),
            ('2  RAG', 'Changes the text the model sees', 'Retrieval-augmented generation: a retriever fetches the right chunks first', 'When facts are many or change'),
            ('3  Fine-tuning', 'Changes the model itself', 'More training on your examples', 'When style or habit is wrong')]
    bw = (w - 0.2 - 2 * 0.5) / 3
    heights = [2.9, 3.3, 3.7]
    for i, (head, chg, how, when) in enumerate(cols):
        x = 0.1 + i * (bw + 0.5)
        hh = heights[i]
        top = 0.1 + hh
        s.box(x, 0.1, bw, hh, '', fill=GOLD if i == 0 else PAPER, lw=2.2)
        s.text(x + bw / 2, top - 0.4, head, size=24, weight='bold')
        y = top - 0.8
        used = wt(s, x + bw / 2, y - 0.2, bw - 0.4, chg, 18, weight='bold')
        y -= used + 0.25
        used = wt(s, x + bw / 2, y - 0.2, bw - 0.4, how, 17, color=BODY)
        wt(s, x + bw / 2, 0.5, bw - 0.4, when, 16, weight='bold', color=RED if i else INK)
        if i < 2:
            s.arrow(x + bw + 0.04, 0.1 + hh * 0.5, x + bw + 0.46, 0.1 + heights[i + 1] * 0.5, lw=2.6, head=20)
    wt(s, w / 2, h - 0.15, w - 0.5, 'Add a method only when the one before it measurably falls short', 20, weight='bold', color=RED)
    return s


# ------------------------------------------------------------------ how long are our documents
@fig('x_t09_tokens')
def tokens(w, h, **_):
    s = Scene(w, h)
    docs = [('Staff handbook excerpt', 829, 1074), ('Meeting notes', 753, 1176), ('Vendor proposal', 606, 791), ('Supplier agreement', 576, 747)]
    mx = 1650
    x0 = 0.1
    bar0 = 3.05
    bw = w - bar0 - 0.2
    rowh = (h - 1.6) / len(docs)
    s.text(x0, h - 0.25, 'Tokens in each NVF document', size=18, weight='bold', ha='left')
    for i, (nm, words, tk) in enumerate(docs):
        y = h - 0.85 - (i + 0.5) * rowh
        s.text(x0, y + 0.2, nm, size=17, weight='bold', ha='left')
        s.text(x0, y - 0.18, f'{words} words', size=15, color=MUTE, ha='left')
        L = bw * tk / mx
        s.rect(bar0, y - 0.3, L, 0.6, fill=GOLD if i == 0 else PALE, edge=INK, lw=1.6)
        s.text(bar0 + L + 0.12, y, f'{tk:,}', size=18, weight='bold', ha='left')
    s.line(bar0, 0.55, bar0, h - 0.95, color=INK, lw=1.4)
    wt(s, w / 2, 0.3, w - 0.2, 'Counted with the cl100k_base tokeniser: about 1.3 to 1.6 tokens a word', 15, color=MUTE)
    return s


# ------------------------------------------------------------------ the open-book test (everyday) with the industry terms underneath
@fig('x_t09_openbook')
def openbook(w, h, **_):
    s = Scene(w, h)
    steps = [('person', 'Question: why does water boil at a lower temperature on a mountain?', 'Query'),
             ('book', 'Index: boiling point 112, 113; pressure 87, 240', 'Retriever'),
             ('doc', 'You choose 3 pages: 112, 113 and 87', 'Top-k, k = 3'),
             ('laptop', 'Your desk has room for a few pages, not all 300', 'Context window'),
             ('pin', 'You write the answer from those 3 pages', 'Generation')]
    n = len(steps)
    rh = (h - 0.1) / n
    tw = 2.35
    for i, (ic, txt, term) in enumerate(steps):
        y = h - 0.05 - (i + 1) * rh
        s.box(0.1, y + 0.06, w - 0.2 - tw - 0.15, rh - 0.12, '', fill=PAPER, lw=1.8)
        wt(s, 0.1 + (w - 0.2 - tw - 0.15) / 2, y + rh / 2, w - 0.2 - tw - 0.15 - 0.4, txt, 15, ha='center')
        s.box(w - 0.1 - tw, y + 0.06, tw, rh - 0.12, '', fill=PALE, lw=1.8)
        wt(s, w - 0.1 - tw / 2, y + rh / 2, tw - 0.2, term, 17, weight='bold')
    return s


# ------------------------------------------------------------------ chunking
@fig('x_t09_chunks')
def chunks(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.25, 'Chunking by clause: each rule stays whole', size=18, weight='bold', ha='left')
    xs = 0.1
    bw = (w - 0.2 - 0.2) / 3
    for i, (cl, t) in enumerate([('3.1', 'Receipts within 14 days'), ('3.2', 'Approval limits: Finance Manager up to UGX 2,000,000'), ('3.3', 'Meals and a UGX 180,000 night')]):
        x = xs + i * (bw + 0.1)
        s.box(x, h - 1.9, bw, 1.4, '', fill=GOLD if cl == '3.2' else PAPER, lw=1.8)
        s.text(x + 0.12, h - 0.72, cl, size=17, weight='bold', ha='left')
        wt(s, x + bw / 2, h - 1.4, bw - 0.2, t, 15, color=BODY, va='center')
    s.text(0.1, h - 2.15, 'Cut every 150 characters: a rule can be cut in two', size=18, weight='bold', ha='left')
    s.box(0.1, h - 3.5, (w - 0.3) / 2, 1.05, '', lw=1.8, dash=True, edge=RED)
    wt(s, 0.1 + (w - 0.3) / 4, h - 2.97, (w - 0.3) / 2 - 0.2, '...3.2 Approval limits for one e', 16, color=BODY)
    s.box(0.2 + (w - 0.3) / 2, h - 3.5, (w - 0.3) / 2, 1.05, '', lw=1.8, dash=True, edge=RED)
    wt(s, 0.2 + 3 * (w - 0.3) / 4, h - 2.97, (w - 0.3) / 2 - 0.2, 'xpense claim... the Finance Manager', 16, color=BODY)
    s.text(w / 2, h - 3.75, 'the answer is in the second piece; the top hit was the first', size=15, color=RED, weight='bold')
    s.tag(0.1, 0.4, 'By clause: 8 of 8', size=17, fill=INK)
    s.tag(w / 2 + 0.1, 0.4, '150 characters: 5 of 8', size=17, fill=RED)
    wt(s, w / 2, 0.15, w - 0.2, 'Top hit holds the whole answer, 8 questions, all-MiniLM-L6-v2', 14, color=MUTE)
    return s


# ------------------------------------------------------------------ all ten questions
@fig('x_t09_retrieval_table')
def retrieval_table(w, h, **_):
    s = Scene(w, h)
    rows = [['Q', 'Top clause', 'Score', 'Answer in', 'Hit']]
    data = [('01', '2.1', 0.88, '2.1'), ('02', '2.2', 0.90, '2.2'), ('03', '3.2', 0.73, '3.2'), ('04', '3.1', 0.80, '3.1'), ('05', '1.3', 0.76, '1.3'),
            ('06', '4.4', 0.75, '4.4'), ('07', '5.3', 0.71, '5.3'), ('08', '3.3', 0.40, '3.3'), ('09', '2.1', 0.70, 'none'), ('10', '4.3', 0.32, 'none')]
    for q, c, sc, a in data:
        hit = 'yes' if a == c else 'no answer'
        rows.append([q, c, f'{sc:.2f}', a, hit])
    rh = (h - 0.05) / len(rows)
    hl = {(9, 4): RED, (10, 4): RED, (8, 2): GOLD, (10, 2): GOLD}
    hl = {(9, 4): GOLD, (10, 4): GOLD, (8, 2): GOLD}
    s.table(0.05, h - 0.02, [0.7, 1.55, 1.2, 1.65, 2.1], rh, rows, size=15, hl_cells=hl)
    return s


# ------------------------------------------------------------------ same questions, three set-ups
@fig('x_t09_with_without')
def with_without(w, h, **_):
    s = Scene(w, h)
    heads = ['Question', 'No handbook given', 'Three retrieved clauses', 'Whole handbook pasted']
    cw = [2.9, 2.9, 3.0, 3.0]
    rows = [heads,
            ['Q03  Who approves UGX 1,500,000?', 'Not stated: no handbook text was provided', 'The Finance Manager [3.2]', 'The Finance Manager (clause 3.2)'],
            ['Q09  Paid sick days a year?', 'Not stated: no handbook text was provided', 'Not stated in the handbook', 'Not stated in the handbook'],
            ['Score on the key, 10 questions', 'Right 2, missed 8, invented 0', 'Right 10 and 10 (2 runs)', 'Right 10 and 10 (2 runs)']]
    rh = [0.5, 0.95, 0.95, 0.95]
    y = h - 0.05
    x = 0.05
    for r, row in enumerate(rows):
        cx = x
        for c, txt in enumerate(row):
            fill = GOLD if (r == 3 and c > 0) else (INK if r == 0 else PAPER)
            col = PAPER if r == 0 else INK
            s.rect(cx, y - rh[r], cw[c], rh[r], fill=fill, edge=INK, lw=1.3)
            wt(s, cx + cw[c] / 2, y - rh[r] / 2, cw[c] - 0.2, txt, 16, weight='bold' if (r == 0 or c == 0) else 'normal', color=col)
            cx += cw[c]
        y -= rh[r]
    wt(s, w / 2, 0.3, w - 0.3, 'Claude, fresh subagent sessions, 6 November 2026; full handbook runs from 4 November. Not ChatGPT or Gemini.', 15, color=MUTE)
    return s


# ------------------------------------------------------------------ before and after fine-tuning
@fig('x_t09_before_after')
def before_after(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.25, 'Customer: "when will my cooking oil arrive"', size=17, weight='bold', ha='left')
    half = (w - 0.3) / 2
    for i, (head, txt, fill) in enumerate([('Before', 'I have been cooking for a while now and I have been using this recipe for a while now...', PAPER),
                                           ('After a tiny LoRA', 'Hello Ms Nye. We will arrive on Monday. Thank you for choosing Nile Valley Foods. Customer Care, Jinja.', GOLD)]):
        x = 0.1 + i * (half + 0.1)
        s.box(x, 1.0, half, h - 1.6, '', fill=fill, lw=2.0)
        s.text(x + 0.2, h - 0.85, head, size=19, weight='bold', ha='left', color=INK)
        wt(s, x + half / 2, 2.25, half - 0.4, txt, 16, color=BODY)
        if i == 1:
            s.tag(x + 0.2, 1.1, 'Invented: Monday, Ms Nye', size=15, fill=RED)
    s.tag(0.1, 0.3, 'Sign-off: 0 of 6', size=16, fill=INK)
    s.tag(0.1 + half + 0.1, 0.3, 'Sign-off: 6 of 6', size=16, fill=INK)
    return s


# ------------------------------------------------------------------ measure before you climb
@fig('x_t09_measure')
def measure(w, h, **_):
    s = Scene(w, h)
    wt(s, w / 2, h - 0.4, w - 0.3, 'Right answers out of 10 (key: handbook_questions_key.csv)', 18, weight='bold')
    rows = [('No handbook text, run 1', 2), ('No handbook text, run 2', 2), ('Three retrieved clauses, 2 runs', 10), ('Whole handbook pasted, 2 runs', 10)]
    x0, lab = 0.1, 3.6
    bw = w - x0 - lab - 0.9
    rowh = (h - 1.6) / 4
    for i, (t, v) in enumerate(rows):
        y = h - 0.95 - (i + 0.5) * rowh
        wt(s, x0 + lab / 2, y, lab - 0.2, t, 16, ha='center')
        L = bw * v / 10
        s.rect(x0 + lab, y - 0.25, L, 0.5, fill=GOLD if v == 10 else PALE, edge=INK, lw=1.5)
        s.text(x0 + lab + L + 0.12, y, f'{v}', size=20, weight='bold', ha='left')
    s.line(x0 + lab, 0.6, x0 + lab, h - 0.95, color=INK, lw=1.4)
    wt(s, w / 2, 0.3, w - 0.3, 'The 2 are only Q09 and Q10, where "not stated" is the right answer', 15, color=MUTE)
    return s


# ------------------------------------------------------------------ decision tree
@fig('x_t09_tree')
def tree(w, h, **_):
    s = Scene(w, h)
    def q(x, y, bw, bh, t):
        s.box(x, y, bw, bh, '', fill=PAPER, lw=2.0)
        wt(s, x + bw / 2, y + bh / 2, bw - 0.25, t, 17, weight='bold')
    def a(x, y, bw, bh, t, fill):
        s.box(x, y, bw, bh, '', fill=fill, lw=2.0)
        wt(s, x + bw / 2, y + bh / 2, bw - 0.25, t, 17, weight='bold')
    bw, bh = 3.4, 0.95
    y1 = h - 1.1
    q(0.1, y1, bw, bh, 'Does a clearer prompt with the page pasted in give right answers?')
    a(w - 3.0, y1, 2.9, bh, 'Stay with the prompt', GOLD)
    s.arrow(0.1 + bw + 0.05, y1 + bh / 2, w - 3.05, y1 + bh / 2, lw=2.4, label='yes', label_size=17)
    y2 = h - 2.35
    s.arrow(0.1 + bw / 2, y1 - 0.02, 0.1 + bw / 2, y2 + bh + 0.04, lw=2.4, label='no', label_size=17, label_dx=0.35, label_dy=0)
    q(0.1, y2, bw, bh, 'Are the facts too many, too long or changing?')
    a(w - 3.0, y2, 2.9, bh, 'Use RAG (or paste a short file)', GOLD)
    s.arrow(0.1 + bw + 0.05, y2 + bh / 2, w - 3.05, y2 + bh / 2, lw=2.4, label='yes', label_size=17)
    y3 = h - 3.6
    s.arrow(0.1 + bw / 2, y2 - 0.02, 0.1 + bw / 2, y3 + bh + 0.04, lw=2.4, label='no', label_size=17, label_dx=0.35, label_dy=0)
    q(0.1, y3, bw, bh, 'Is the style or format still wrong after steps 1 and 2?')
    a(w - 3.0, y3, 2.9, bh, 'Consider fine-tuning', GOLD)
    s.arrow(0.1 + bw + 0.05, y3 + bh / 2, w - 3.05, y3 + bh / 2, lw=2.4, label='yes', label_size=17)
    wt(s, w / 2 - 0.2, 0.25, w - 0.3, 'Each step: measure on a test set before you add the next. Combine methods only when each earns its place.', 16, color=RED, weight='bold')
    return s


# ------------------------------------------------------------------ peek inside the retrieval score (real numbers, demo_runs/s09/peek_scoring.json)
@fig('x_t09_peek_score')
def peek_score(w, h, **_):
    import json
    from pathlib import Path
    P = json.loads((Path(__file__).resolve().parent.parent / 'demo_runs' / 's09' / 'peek_scoring.json').read_text())
    f = P['first6']
    fmt = lambda v: ('%.3f' % v).replace('-', '−') if abs(v) >= 0.0005 else '0.000'
    pr = lambda v: ('%.4f' % v).replace('-', '−') if abs(v) >= 0.00005 else '0.0000'
    s = Scene(w, h)
    rows = [['', 'No. 1', 'No. 2', 'No. 3', 'No. 4', 'No. 5', 'No. 6', '...', 'All 384'],
            ['Query q'] + [fmt(v) for v in f['question']] + ['...', ''],
            ['Clause 3.2'] + [fmt(v) for v in f['3.2']] + ['...', ''],
            ['Clause 3.1'] + [fmt(v) for v in f['3.1']] + ['...', ''],
            ['Products: q × c(3.2)'] + [pr(v) for v in P['products6_3.2']] + ['...', 'add to %.2f' % P['score_3.2']],
            ['Products: q × c(3.1)'] + [pr(v) for v in P['products6_3.1']] + ['...', 'add to %.2f' % P['score_3.1']]]
    cw = [2.75, 1.05, 1.05, 1.05, 1.05, 1.05, 1.05, 0.6, 1.75]
    rh = min(0.62, (h - 1.0) / 6)
    s.table(0.05, h - 0.05, cw, rh, rows, size=16, hl_cells={(4, 8): GOLD, (5, 8): GOLD, (4, 0): PALE, (5, 0): PALE}, align=['left'] + ['center'] * 8)
    s.text(w / 2, 0.62, 'cos θ = q·c / (|q| |c|) = q1·c1 + q2·c2 + ... + q384·c384, because both lengths are 1', size=17, weight='bold')
    s.text(w / 2, 0.2, 'q: query, c: chunk, q1: first number of q, |q|: length of q, θ: the angle between them. First 6 of 384 shown.', size=15, color=BODY)
    return s




# ------------------------------------------------------------------ the RAG pipeline (overview; scores come later in the session)
@fig('x_t09_librarian')
def librarian(w, h, **_):
    s = Scene(w, h)
    steps = [('doc', 'Chunking', 'Cut the handbook into 30 chunks, one per clause'),
             ('grid', 'Embedding', 'Each chunk, and later the query, becomes a vector (Session 4)'),
             ('magnifier', 'Retriever', 'Gives every chunk a closeness score against the query'),
             ('pin', 'Top-k', 'Keeps the k closest chunks; here k = 3'),
             ('robot', 'Generation', 'The model answers from those chunks and cites the clause')]
    n = len(steps)
    gap = 0.4
    bw = (w - 0.2 - gap * (n - 1)) / n
    bh = h - 0.75
    for i, (ic, head, ex) in enumerate(steps):
        x = 0.1 + i * (bw + gap)
        s.box(x, 0.65, bw, bh, '', fill=GOLD if i == 3 else PAPER, lw=2.0)
        s.icon(ic, x + bw / 2, 0.65 + bh - 0.6, 0.8)
        wt(s, x + bw / 2, 0.65 + bh - 1.4, bw - 0.25, head, 19, weight='bold')
        wt(s, x + bw / 2, 0.65 + bh - 2.45, bw - 0.25, ex, 16, color=BODY)
        if i < n - 1:
            s.arrow(x + bw + 0.03, 0.65 + bh / 2, x + bw + gap - 0.03, 0.65 + bh / 2, lw=2.4, head=18)
    s.text(0.1, 0.3, 'Done once, ahead of time: chunking and embedding the chunks (stored in a vector database).', size=15, ha='left', color=BODY)
    return s


# ------------------------------------------------------------------ cosine similarity recalled from Session 4, and what a score of 0.6 means
@fig('x_t09_cosine')
def cosine(w, h, **_):
    import math
    s = Scene(w, h)
    ox, oy, L = 0.3, 0.55, 2.6
    s.arrow(ox, oy, ox + L, oy, lw=3.0, head=18)
    s.text(ox + L + 0.1, oy + 0.05, 'query', size=16, weight='bold', ha='left')
    for c, lab, col in [(0.96, '0.96', GOLD), (0.6, '0.60', INK), (0.0, '0.00', MUTE)]:
        a = math.acos(c)
        x2, y2 = ox + L * math.cos(a), oy + L * math.sin(a)
        s.arrow(ox, oy, x2, y2, lw=2.6, head=16, color=INK if col != MUTE else MUTE)
        deg = round(math.degrees(a))
        s.text(x2 + 0.12, y2 + 0.12, f'cos = {lab}, {deg}°', size=16, weight='bold', ha='left', color=RED if c == 0.6 else INK)
    x0 = 4.65
    s.text(x0, h - 0.3, 'Worked: q = (4, 3), c = (3, 4)', size=16, weight='bold', ha='left')
    lines = ['dot product: 4×3 + 3×4 = 24', 'length of q: √(16 + 9) = 5; of c: 5', 'cos = 24 ÷ (5 × 5) = 0.96']
    for i, l in enumerate(lines):
        s.text(x0, h - 0.75 - 0.4 * i, l, size=15, ha='left')
    s.box(x0, 0.1, w - x0 - 0.05, 2.3, '', fill=PALE, lw=1.4)
    wt(s, x0 + (w - x0) / 2, 2.0, w - x0 - 0.3, 'Range: 1 same direction, 0 unrelated.', 15, weight='bold')
    wt(s, x0 + (w - x0) / 2, 0.95, w - x0 - 0.3, '0.6 is about 53° apart: related, far from the same. No score is good in itself; compare scores for one question.', 15)
    return s


# ------------------------------------------------------------------ scores for one question, with the top-k cut drawn
def _bars(s, x0, y_top, w, rows, rowh, size=17, hl=0, label_w=2.6, vmax=1.0, red_rows=(), gold_rows=None):
    bw = w - label_w - 0.9
    for i, (lab, v) in enumerate(rows):
        y = y_top - (i + 0.5) * rowh
        gold = (i == hl) if gold_rows is None else (i in gold_rows)
        s.text(x0, y, lab, size=size, ha='left', weight='bold' if gold else 'normal')
        L = bw * v / vmax
        s.rect(x0 + label_w, y - rowh * 0.3, L, rowh * 0.6, fill=(RED if i in red_rows else GOLD) if gold else PALE, edge=INK, lw=1.4)
        s.text(x0 + label_w + L + 0.1, y, f'{v:.2f}', size=size, weight='bold', ha='left')
    s.line(x0 + label_w, y_top - len(rows) * rowh, x0 + label_w, y_top, color=INK, lw=1.4)


@fig('x_t09_scores_q03')
def scores_q03(w, h, **_):
    s = Scene(w, h)
    wt(s, w / 2, h - 0.3, w - 0.3, 'Who must approve an expense claim of UGX 1,500,000?', 18, weight='bold')
    rows = [('3.2 Approval limits', 0.73), ('3.1 Receipts', 0.47), ('3.5 Paid with salary', 0.46), ('3.6 No receipt', 0.40), ('3.3 Travel allowance', 0.29)]
    rowh = 0.55
    top = h - 0.7
    _bars(s, 0.1, top, w - 1.3, rows, rowh, size=16, label_w=2.55, gold_rows=(0, 1, 2))
    ycut = top - 3 * rowh
    s.line(0.1, ycut, w - 0.1, ycut, color=RED, lw=2.2, dash=True)
    s.line(w - 0.75, top - 0.05, w - 0.75, ycut + 0.05, color=INK, lw=2)
    s.text(w - 0.45, top - 1.5 * rowh, 'top-k\nk = 3:\nsent', size=14, weight='bold', color=INK)
    s.text(w - 0.45, ycut - rowh, 'left\nout', size=14, color=MUTE)
    s.text(0.1, 0.55, 'Gap: 0.73 − 0.47 = 0.26. The right clause leads clearly.', size=15, weight='bold', ha='left')
    s.text(0.1, 0.18, 'Recorded run, all-MiniLM-L6-v2, cosine similarity, 6 Nov 2026', size=14, color=MUTE, ha='left')
    return s


@fig('x_t09_miss')
def miss(w, h, **_):
    s = Scene(w, h)
    wt(s, w / 2, h - 0.45, w - 0.3, 'Best score for two different questions', 19, weight='bold')
    s.text(0.1, h - 1.15, 'Q03 has an answer in the handbook', size=17, ha='left', weight='bold')
    _bars(s, 0.1, h - 1.4, w - 0.2, [('3.2 Approval limits', 0.73)], 0.6, size=17, label_w=2.7)
    s.text(0.1, h - 2.4, 'Q09 asks for paid sick days: none stated', size=17, ha='left', weight='bold', color=RED)
    _bars(s, 0.1, h - 2.65, w - 0.2, [('2.1 Annual leave', 0.70)], 0.6, size=17, label_w=2.7, red_rows=(0,))
    wt(s, w / 2, 1.1, w - 0.3, '0.73 against 0.70: a score cannot tell the two cases apart', 18, weight='bold', color=RED)
    s.text(w / 2, 0.45, 'Q10 (car mileage rate, not stated): best score 0.32', size=16, color=BODY)
    return s


# ------------------------------------------------------------------ the context window and the prompt budget
@fig('x_t09_context')
def context(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.3, 'Budget: instructions and question + retrieved text + answer ≤ context window', size=17, weight='bold', ha='left')
    s.text(0.1, h - 0.68, '≤ means "no more than". Counted in tokens (cl100k_base).', size=15, color=BODY, ha='left')
    rows = [('RAG for Q03', [(94, 'instructions + question', PALE), (104, '3 clauses', GOLD), (300, 'answer', PAPER)], 498),
            ('Whole handbook', [(94, '', PALE), (1074, 'whole handbook, 1,074', GOLD), (300, 'answer', PAPER)], 1468)]
    x0 = 2.4
    scale = (w - x0 - 1.2) / 1468
    for i, (lab, segs, tot) in enumerate(rows):
        y = h - 1.45 - i * 0.95
        s.text(0.1, y, lab, size=17, weight='bold', ha='left')
        x = x0
        for v, t, f in segs:
            L = v * scale
            s.rect(x, y - 0.3, L, 0.6, fill=f, edge=INK, lw=1.4)
            if t and L > 1.0:
                wt(s, x + L / 2, y, L - 0.1, t, 14)
            x += L
        s.text(x + 0.1, y, f'{tot:,}', size=17, weight='bold', ha='left')
        if i == 0:
            s.text(x0, y - 0.5, '94: instructions + question;  104: the 3 retrieved clauses', size=14, ha='left', color=BODY)
    s.text(0.1, h - 3.0, '94 + 104 + 300 = 498 tokens.   94 + 1,074 + 300 = 1,468 tokens.   300 is a limit you choose.', size=15, ha='left')
    s.text(0.1, 0.62, 'Long inputs: facts in the middle can be missed (Liu and others, 2023, in their tests).', size=15, ha='left', color=BODY)
    for i, (ic, tx) in enumerate([('clock', 'More tokens: slower, dearer'), ('lock', 'All of it goes to the model')]):
        x = 0.1 + i * (w - 0.2) / 2
        s.text(x, 0.2, tx, size=15, ha='left')
    return s


# ------------------------------------------------------------------ fine-tuning is the Session 0 training loop, started from trained weights
@fig('x_t09_ftloop')
def ftloop(w, h, **_):
    s = Scene(w, h)
    s.box(0.05, h - 1.0, w - 0.1, 0.9, '', fill=PALE, lw=1.6)
    wt(s, w / 2, h - 0.55, w - 0.4, 'Start: the trained weights of GPT-2, all 124,439,808 (Session 7), instead of random numbers', 15, weight='bold')
    steps = [('Predict', 'a reply to one of your 48 example messages'), ('Loss', 'how far it is from your reply'), ('Adjust', 'move the weights a little against the gradient'), ('Repeat', 'over all examples, 4 epochs')]
    bw = (w - 0.1 - 3 * 0.25) / 4
    for i, (hd, tx) in enumerate(steps):
        x = 0.05 + i * (bw + 0.25)
        s.box(x, 1.05, bw, 1.85, '', fill=GOLD if i == 2 else PAPER, lw=1.8)
        s.text(x + bw / 2, 2.6, hd, size=18, weight='bold')
        wt(s, x + bw / 2, 1.75, bw - 0.2, tx, 14, color=BODY)
        if i < 3:
            s.arrow(x + bw + 0.02, 1.98, x + bw + 0.23, 1.98, lw=2, head=13)
    s.arrow(w - 0.3, 1.0, 0.35, 1.0, lw=1.8, head=13, rad=-0.0, color=MUTE)
    wt(s, w / 2, 0.42, w - 0.2, 'Problem: adjusting every weight is slow, and each task needs a full copy of the model.', 15, weight='bold', color=RED)
    return s


# ------------------------------------------------------------------ a matrix is a table of numbers
@fig('x_t09_matrix')
def matrix(w, h, **_):
    s = Scene(w, h)
    vals = [[2, 0, 1, 3], [1, 1, 0, 2], [0, 2, 1, 1]]
    cw, ch = 0.75, 0.62
    x0, ytop = 1.1, h - 0.75
    for j in range(4):
        s.text(x0 + (j + 0.5) * cw, ytop + 0.25, f'col {j + 1}', size=14, color=MUTE)
    for i, row in enumerate(vals):
        s.text(x0 - 0.15, ytop - (i + 0.5) * ch, f'row {i + 1}', size=14, color=MUTE, ha='right')
        for j, v in enumerate(row):
            s.box(x0 + j * cw, ytop - (i + 1) * ch, cw, ch, str(v), size=18, fill=GOLD if (i, j) == (1, 3) else PAPER, r=0.02)
    s.text(x0, ytop - 3 * ch - 0.35, '3 rows × 4 columns = 12 numbers', size=17, weight='bold', ha='left')
    s.text(x0, ytop - 3 * ch - 0.75, 'Gold: row 2, column 4 holds 2', size=15, color=BODY, ha='left')
    s.box(0.05, 0.1, w - 0.1, 1.1, '', fill=PALE, lw=1.4)
    wt(s, w / 2, 0.85, w - 0.4, 'One GPT-2 weight table: 768 rows × 2,304 columns', 16, weight='bold')
    wt(s, w / 2, 0.42, w - 0.4, '768 × 2,304 = 1,769,472 weights, in each of the 12 blocks', 16)
    return s


# ------------------------------------------------------------------ low rank: a times table is rebuilt from two short lists
@fig('x_t09_lowrank')
def lowrank(w, h, **_):
    s = Scene(w, h)
    cw, ch = 0.66, 0.5
    col = [1, 2, 3, 4]
    row = [1, 2, 3, 4]
    x0, ytop = 1.3, h - 0.95
    s.text(0.05, h - 0.25, 'A times table: each cell = its row number × its column number', size=17, weight='bold', ha='left')
    for j, v in enumerate(row):
        s.box(x0 + j * cw, ytop + 0.1, cw, ch, str(v), size=17, fill=GOLD, r=0.02)
    for i, v in enumerate(col):
        s.box(x0 - cw - 0.1, ytop - (i + 1) * ch, cw, ch, str(v), size=17, fill=GOLD, r=0.02)
        for j, u in enumerate(row):
            s.box(x0 + j * cw, ytop - (i + 1) * ch, cw, ch, str(v * u), size=17, fill=PALE if (i, j) == (2, 1) else PAPER, r=0.02)
    s.text(x0 + 4 * cw + 0.15, ytop + 0.35, 'row list A', size=14, color=RED, weight='bold', ha='left')
    s.text(x0 - cw - 0.1, ytop - 4 * ch - 0.3, 'column list B', size=14, color=RED, weight='bold', ha='left')
    s.text(x0 + 4 * cw + 0.15, ytop - 2.5 * ch, 'row 3, column 2:\n3 × 2 = 6', size=15, ha='left')
    xr = 6.4
    lines = [('16 numbers in the table', False), ('rebuilt from 4 + 4 = 8 numbers', True), ('', False),
             ('Written B A: the column B times the row A', False), ('The width of B and A is the rank, r.', False), ('Here r = 1.', False)]
    for i, (t, b) in enumerate(lines):
        if t:
            s.text(xr, h - 0.85 - 0.45 * i, t, size=16, weight='bold' if b else 'normal', color=RED if b else INK, ha='left')
    s.text(0.05, 0.25, 'A table built this way is low rank. In LoRA the numbers in B and A are learned in training.', size=15, color=BODY, ha='left')
    return s


# ------------------------------------------------------------------ W' = W + B A on a 4 x 4 example (numbers from demo_runs/s09/check_numbers.py)
@fig('x_t09_lora_small')
def lora_small(w, h, **_):
    s = Scene(w, h)
    W = [[2, 0, 1, 3], [1, 1, 0, 2], [0, 2, 1, 1], [3, 1, 2, 0]]
    B = [1, 0, 2, 0]
    A = [1, 0, 0, 1]
    BA = [[b * a for a in A] for b in B]
    Wp = [[W[i][j] + BA[i][j] for j in range(4)] for i in range(4)]
    c = 0.45
    ytop = h - 0.75

    def grid(x, M, fill=PAPER, hl=None):
        for i, r in enumerate(M):
            for j, v in enumerate(r):
                s.box(x + j * c, ytop - (i + 1) * c, c, c, str(v), size=16, fill=GOLD if (hl and hl(i, j)) else fill, r=0.01)
    xw = 0.1
    grid(xw, W, PALE)
    s.text(xw + 2 * c, ytop - 4 * c - 0.3, 'W (frozen)', size=15, weight='bold')
    s.text(xw + 4 * c + 0.25, ytop - 2 * c, '+', size=26, weight='bold')
    xb = xw + 4 * c + 0.5
    for i, v in enumerate(B):
        s.box(xb, ytop - (i + 1) * c, c, c, str(v), size=16, fill=GOLD, r=0.01)
    s.text(xb + c / 2, ytop + 0.3, 'B', size=15, weight='bold', color=RED)
    xg = xb + c + 0.1
    for j, v in enumerate(A):
        s.box(xg + j * c, ytop + 0.1, c, c, str(v), size=16, fill=GOLD, r=0.01)
    s.text(xg + 4 * c + 0.2, ytop + 0.1 + c / 2, 'A', size=15, weight='bold', color=RED)
    grid(xg, BA)
    s.text(xg + 2 * c, ytop - 4 * c - 0.3, 'B A', size=15, weight='bold')
    s.text(xg + 4 * c + 0.25, ytop - 2 * c, '=', size=26, weight='bold')
    xp = xg + 4 * c + 0.55
    grid(xp, Wp, PAPER, hl=lambda i, j: BA[i][j] != 0)
    s.text(xp + 2 * c, ytop - 4 * c - 0.3, "W\u2032 (after training)", size=15, weight='bold')
    xt = xp + 4 * c + 0.35
    notes = ['W: the original table, d rows \u00d7 k columns', 'B: a tall thin table, d \u00d7 r', 'A: a short wide table, r \u00d7 k',
             'r: the rank, the width of B and A', "W\u2032 = W + B A: the table used after", '', 'Here d = 4, k = 4, r = 1:', 'W has d \u00d7 k = 16 numbers', 'B and A have r(d + k) = 8']
    for i, t_ in enumerate(notes):
        if t_:
            s.text(xt, h - 0.3 - 0.38 * i, t_, size=15, ha='left', weight='bold' if i >= 6 else 'normal', color=RED if i == 8 else INK)
    s.text(0.1, 0.55, 'B A is a times table of B and A: row 3 is 2 \u00d7 (1, 0, 0, 1) = (2, 0, 0, 2).', size=15, ha='left')
    s.text(0.1, 0.18, 'Add cell by cell: row 3 of W\u2032 is (0, 2, 1, 1) + (2, 0, 0, 2) = (2, 2, 1, 3). Gold: the cells that changed.', size=15, ha='left', color=BODY)
    return s


# ------------------------------------------------------------------ the same count with GPT-2's numbers: where 294,912 comes from
@fig('x_t09_lora_peek')
def lora_peek(w, h, **_):
    s = Scene(w, h)
    rows = [['In each of 12 blocks', 'Size', 'Count', 'Trained?'],
            ['W, one weight table', 'd × k = 768 × 2,304', '1,769,472', 'Frozen'],
            ['B (tall, thin)', 'd × r = 768 × 8', '6,144', 'Yes'],
            ['A (short, wide)', 'r × k = 8 × 2,304', '18,432', 'Yes'],
            ['B and A together', 'r(d + k) = 8 × 3,072', '24,576', 'Yes']]
    cw = [3.3, 3.6, 1.9, 1.5]
    rh = 0.5
    s.table(0.05, h - 0.05, cw, rh, rows, size=16, hl_cells={(4, 2): GOLD}, align=['left', 'left', 'center', 'center'])
    y = h - 0.05 - 5 * rh - 0.4
    s.text(0.1, y, 'All 12 blocks: 12 × 24,576 = 294,912 trained weights', size=18, weight='bold', ha='left')
    s.text(0.1, y - 0.45, 'Share of GPT-2: 294,912 ÷ 124,439,808 = 0.0024, about 0.24 percent', size=18, weight='bold', ha='left', color=RED)
    s.text(0.1, 0.2, 'd = 768 rows, k = 2,304 columns as stored in GPT-2; r = 8. Matches the recorded run: trainable 294,912.', size=14, ha='left', color=BODY)
    return s
