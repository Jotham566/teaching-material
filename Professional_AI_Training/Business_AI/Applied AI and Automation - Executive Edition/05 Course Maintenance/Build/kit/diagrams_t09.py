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
    items = [('book', 'Learned in training, up to a cut-off date', False), ('doc', 'Your prompt and what you paste in', False),
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
    cols = [('1  Prompt', 'Changes the instructions', 'Paste the page you need into the prompt', 'Start here'),
            ('2  Retrieve', 'Changes the pages the model sees', 'A search step fetches the right pages first', 'When facts are missing or change'),
            ('3  Fine-tune', 'Changes the model itself', 'Extra training on your examples', 'When style or habit is wrong')]
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
    wt(s, w / 2, h - 0.15, w - 0.5, 'Climb a rung only when the one below measurably falls short', 20, weight='bold', color=RED)
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


# ------------------------------------------------------------------ the librarian
@fig('x_t09_librarian')
def librarian(w, h, **_):
    s = Scene(w, h)
    steps = [('person', 'Question', 'Who must approve a claim of UGX 1,500,000?'),
             ('grid', 'Turn into numbers', 'The question becomes an embedding'),
             ('magnifier', 'Search the index', 'Score every chunk against the question'),
             ('doc', 'Fetch the top 3', 'Clause 3.2 scores 0.73, 3.1 scores 0.47, 3.5 scores 0.46'),
             ('robot', 'Write from the pages', 'The Finance Manager (clause 3.2)')]
    n = len(steps)
    gap = 0.4
    bw = (w - 0.2 - gap * (n - 1)) / n
    bh = h - 0.3
    for i, (ic, head, ex) in enumerate(steps):
        x = 0.1 + i * (bw + gap)
        s.box(x, 0.1, bw, bh, '', fill=GOLD if i == 3 else PAPER, lw=2.0)
        s.icon(ic, x + bw / 2, 0.1 + bh - 0.65, 0.85)
        used = wt(s, x + bw / 2, 0.1 + bh - 1.5, bw - 0.25, head, 19, weight='bold')
        wt(s, x + bw / 2, 0.1 + bh - 1.75 - 0.75, bw - 0.25, ex, 16, color=BODY)
        if i < n - 1:
            s.arrow(x + bw + 0.03, 0.1 + bh / 2, x + bw + gap - 0.03, 0.1 + bh / 2, lw=2.4, head=18)
    return s


# ------------------------------------------------------------------ chunking
@fig('x_t09_chunks')
def chunks(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.25, 'Cut by clause: each rule stays whole', size=18, weight='bold', ha='left')
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


# ------------------------------------------------------------------ scores for one question
def _bars(s, x0, y_top, w, rows, rowh, size=17, hl=0, label_w=2.6, vmax=1.0, red_rows=()):
    bw = w - label_w - 0.9
    for i, (lab, v) in enumerate(rows):
        y = y_top - (i + 0.5) * rowh
        s.text(x0, y, lab, size=size, ha='left', weight='bold' if i == hl else 'normal')
        L = bw * v / vmax
        s.rect(x0 + label_w, y - rowh * 0.3, L, rowh * 0.6, fill=(RED if i in red_rows else GOLD) if i == hl else PALE, edge=INK, lw=1.4)
        s.text(x0 + label_w + L + 0.1, y, f'{v:.2f}', size=size, weight='bold', ha='left')
    s.line(x0 + label_w, y_top - len(rows) * rowh, x0 + label_w, y_top, color=INK, lw=1.4)


@fig('x_t09_scores_q03')
def scores_q03(w, h, **_):
    s = Scene(w, h)
    wt(s, w / 2, h - 0.5, w - 0.3, 'Who must approve an expense claim of UGX 1,500,000?', 19, weight='bold')
    rows = [('3.2 Approval limits', 0.73), ('3.1 Receipts', 0.47), ('3.5 Paid with salary', 0.46), ('3.6 No receipt', 0.40), ('3.3 Travel allowance', 0.29)]
    _bars(s, 0.1, h - 1.05, w - 0.2, rows, 0.55, size=17, label_w=2.7)
    s.text(w / 2, 0.75, 'Score = how close the meaning is (1.00 is identical)', size=16, color=BODY)
    s.text(w / 2, 0.3, 'all-MiniLM-L6-v2, cosine similarity, real run', size=14, color=MUTE)
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


# ------------------------------------------------------------------ long context
@fig('x_t09_context')
def context(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.3, 'The context window: everything the model reads at once', size=18, weight='bold', ha='left')
    bx, bw = 0.1, w - 0.2
    zone = bw / 3
    labels = [('Start', 'Used well', GOLD), ('Middle', 'Can be missed', PALE), ('End', 'Used well', GOLD)]
    for i, (a, b, f) in enumerate(labels):
        s.rect(bx + i * zone, h - 2.5, zone, 1.6, fill=f, edge=INK, lw=2)
        s.text(bx + i * zone + zone / 2, h - 1.55, a, size=22, weight='bold')
        s.text(bx + i * zone + zone / 2, h - 2.05, b, size=18)
    s.text(w / 2, h - 3.0, 'Pattern reported by Liu and others (2023), not a measure of your product', size=15, color=MUTE)
    for i, (ic, t) in enumerate([('clock', 'Longer input, slower and dearer'), ('folder', 'A whole archive does not fit'), ('lock', 'Everything pasted is seen by the model')]):
        x = 0.1 + i * (w - 0.2) / 3
        s.icon(ic, x + 0.45, 1.05, 0.7)
        wt(s, x + 0.85 + (w - 0.2) / 6 - 0.45, 1.05, (w - 0.2) / 3 - 1.1, t, 16, ha='center')
    return s


# ------------------------------------------------------------------ LoRA
@fig('x_t09_lora')
def lora(w, h, **_):
    s = Scene(w, h)
    s.text(0.1, h - 0.3, 'GPT-2: 124,439,808 weights', size=18, weight='bold', ha='left')
    s.box(0.1, h - 2.4, 3.6, 1.8, 'Frozen\n(not changed)', size=22, fill=PALE, weight='bold', lw=2)
    s.text(4.2, h - 1.5, '+', size=34, weight='bold')
    s.box(4.7, h - 1.95, 0.7, 1.35, '', fill=GOLD, lw=2)
    s.box(5.55, h - 2.4, 1.35, 0.5, '', fill=GOLD, lw=2)
    s.text(5.05, h - 1.28, 'A', size=18, weight='bold')
    s.text(6.2, h - 2.15, 'B', size=18, weight='bold')
    wt(s, 5.9, h - 3.0, 3.2, 'Two thin added tables', 16, weight='bold')
    s.text(0.1, 1.55, 'LoRA trains only the added tables:', size=19, weight='bold', ha='left')
    s.text(0.1, 1.0, '294,912 weights = 0.24 percent', size=24, weight='bold', ha='left', color=RED)
    wt(s, w / 2, 0.3, w - 0.3, 'Rank 8, on the attention layers. A drawing of the idea, not to scale.', 15, color=MUTE)
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
    a(w - 3.0, y2, 2.9, bh, 'Retrieve (or paste a short file)', GOLD)
    s.arrow(0.1 + bw + 0.05, y2 + bh / 2, w - 3.05, y2 + bh / 2, lw=2.4, label='yes', label_size=17)
    y3 = h - 3.6
    s.arrow(0.1 + bw / 2, y2 - 0.02, 0.1 + bw / 2, y3 + bh + 0.04, lw=2.4, label='no', label_size=17, label_dx=0.35, label_dy=0)
    q(0.1, y3, bw, bh, 'Is the style or format still wrong after steps 1 and 2?')
    a(w - 3.0, y3, 2.9, bh, 'Consider fine-tuning', GOLD)
    s.arrow(0.1 + bw + 0.05, y3 + bh / 2, w - 3.05, y3 + bh / 2, lw=2.4, label='yes', label_size=17)
    wt(s, w / 2 - 0.2, 0.25, w - 0.3, 'Each step: measure on a test set before you climb. Combine rungs only when each one earns its place.', 16, color=RED, weight='bold')
    return s
