"""Session 6 figures: pretraining, post-training, families, mixture of experts, reasoning, multimodal, diffusion, benchmarks, the recorded comparison and model cards.
Real texts come from demo_runs/s06/qwen_runs.json and demo_runs/s06/prompts/claude_reply_verbatim.txt (recorded 6 November 2026).
Slide use:  dict(kind='t06_library')  ->  figure 'x_t06_library'.
"""
import json
import math
import random
import textwrap
from pathlib import Path

import numpy as np

from figkit import Scene, INK, BODY, MUTE, GREY, HAIR, PALE, PAPER, RED, GOLD, fig

RUN = Path(__file__).resolve().parent.parent / 'demo_runs' / 's06'
Q = json.loads((RUN / 'qwen_runs.json').read_text())


def clean(s):
    return s.replace('$', r'\$')


def put(s, x, y, t, **kw):
    return s.text(x, y, clean(t), **kw)


def mt(s, x, y, t, **kw):
    return s.text(x, y, t, **kw)


def wrap(t, w_in, size=15):
    return '\n'.join(textwrap.wrap(t, max(10, int(w_in / (0.0069 * size)))))


# ---------------------------------------------------------------------------------------------------------------- pretraining
@fig('x_t06_library')
def library(w, h, **_):
    s = Scene(w, h)
    rnd = random.Random(6)
    shelf_y = [h - 1.25, h - 2.2]
    for k, y in enumerate(shelf_y):
        x = 0.3
        while x < w - 0.8:
            bw = rnd.choice([0.14, 0.18, 0.22, 0.26])
            bh = rnd.choice([0.55, 0.62, 0.7, 0.78])
            s.rect(x, y, bw, bh, fill=rnd.choice([GOLD, PAPER, GREY, PAPER, RED if rnd.random() < 0.12 else PAPER]), edge=INK, lw=1.0)
            x += bw + 0.02
        s.line(0.2, y, w - 0.7, y, color=INK, lw=2.4)
    put(s, w / 2, h - 0.3, 'A text corpus: a huge collection of text (analogy: a library)', size=18, weight='bold')
    bw = 2.1
    ys = 0.95
    labs = ['Hide the next\ntoken', 'Predict it', 'Adjust the\nweights']
    for i, t in enumerate(labs):
        x = 0.3 + i * (bw + 0.4)
        s.box(x, ys, bw, 0.95, t, size=16, weight='bold', fill=PALE if i != 1 else GOLD)
        if i < 2:
            s.arrow(x + bw, ys + 0.47, x + bw + 0.4, ys + 0.47, color=RED, lw=2.4)
    put(s, w / 2, 0.5, 'Repeated for every token of the corpus, billions of times.', size=16, color=BODY)
    put(s, w / 2, 2.2, 'The result is a base model: it continues text.', size=17, weight='bold', color=RED)
    return s


@fig('x_t06_coach')
def coach(w, h, **_):
    s = Scene(w, h)
    items = [('Base model', 'Pretrained: continues any text', PAPER, 'book'), ('Supervised fine-tuning', 'Loop again on answers people wrote', GOLD, 'pen'),
             ('RLHF', 'People rank answers; model adjusted to match', GOLD, 'check'), ('Instruction-tuned model', 'Follows instructions and answers', PAPER, 'laptop')]
    n = len(items)
    bh = (h - 0.2) / n - 0.25
    for i, (a, b, f, ic) in enumerate(items):
        y = h - 0.1 - (i + 1) * (bh + 0.25) + 0.25
        s.box(0.1, y, w - 0.2, bh, '', fill=f, edge=INK, lw=1.8)
        s.icon(ic, 0.75, y + bh / 2, 0.7)
        put(s, 1.4, y + bh / 2 + 0.17, a, size=19, weight='bold', ha='left')
        put(s, 1.4, y + bh / 2 - 0.2, b, size=16, ha='left', color=BODY)
        if i < n - 1:
            s.arrow(w / 2, y, w / 2, y - 0.22, color=RED, lw=2.4, head=12)
    return s


@fig('x_t06_base_vs_instruct')
def base_vs_instruct(w, h, **_):
    s = Scene(w, h)
    pw = (w - 0.3) / 2
    base = ' '.join(Q['gpt2_base_greedy'].split())[:112].rsplit(' ', 1)[0]
    inst = Q['runs'][0]['reply']
    inst = inst.replace('**', '').replace('\\( ', '').replace(' \\)', '').replace('\\times', 'x')
    inst = ' '.join(inst.split())
    inst = inst[:inst.index('Dear Shop Owner')] + 'Dear Shop Owner, Thank you for your email regarding the issue ...'
    panels = [('GPT-2: base model (pretraining only)', 'Given the task text, it continues like a news page:', base + ' ...'),
              ('Qwen2.5-1.5B-Instruct: instruction-tuned', 'Given the same text, it follows the instructions:', inst)]
    for i, (hd, sub, body) in enumerate(panels):
        x0 = i * (pw + 0.3)
        s.box(x0, 0.05, pw, h - 0.1, '', fill=PAPER, edge=INK, lw=1.8)
        put(s, x0 + 0.2, h - 0.4, hd, size=19, weight='bold', color=RED, ha='left')
        put(s, x0 + 0.2, h - 0.95, sub, size=16, color=BODY, ha='left')
        put(s, x0 + 0.2, h - 2.3, wrap(body, pw - 0.4, 19), size=19, ha='left', va='center')
    put(s, w / 2, 0.02, '', size=14)
    return s


@fig('x_t06_families')
def families(w, h, **_):
    s = Scene(w, h)
    cols = [('cloud', 'Hosted assistant', 'You use it through the maker\'s service. Your text travels to their computers.', 'Examples: Claude, ChatGPT, Gemini', 'Check: terms, data settings, results on your task'),
            ('folder', 'Open-weights model', 'You can download the files of learned parameters and run them yourself.', 'Examples: GPT-2 (MIT), Qwen2.5 and Mixtral (Apache-2.0)', 'Check: licence, size, model card'),
            ('laptop', 'Small language model', 'A language model with a few billion parameters or fewer, small enough for your own machine. Weaker, and private.', 'Example: Qwen2.5-1.5B-Instruct, used today', 'Check: it on your own sample')]
    pw = (w - 0.4) / 3
    for i, (ic, hd, a, b, c) in enumerate(cols):
        x0 = i * (pw + 0.2)
        s.box(x0, 0.05, pw, h - 0.1, '', fill=PAPER, edge=INK, lw=1.8)
        s.icon(ic, x0 + 0.55, h - 0.65, 0.75)
        put(s, x0 + 1.1, h - 0.65, hd, size=19, weight='bold', ha='left')
        put(s, x0 + 0.2, h - 1.95, wrap(a, pw - 0.4, 16), size=16, ha='left')
        put(s, x0 + 0.2, 1.4, wrap(b, pw - 0.4, 16), size=16, ha='left', weight='bold', color=BODY)
        put(s, x0 + 0.2, 0.55, wrap(c, pw - 0.4, 16), size=16, ha='left', color=RED)
    return s


# ---------------------------------------------------------------------------------------------------------------- mixture of experts, reasoning, multimodal
@fig('x_t06_moe')
def moe(w, h, **_):
    s = Scene(w, h)
    s.box(w / 2 - 1.1, h - 0.8, 2.2, 0.55, 'token: invoice', size=19, weight='bold', fill=GOLD)
    s.arrow(w / 2, h - 0.8, w / 2, h - 1.3, color=INK, lw=2)
    s.box(w / 2 - 1.5, h - 1.9, 3.0, 0.6, 'Router: picks 2 of 8', size=18, weight='bold')
    n = 8
    gap = 0.12
    bw = (w - 0.4 - gap * (n - 1)) / n
    y = 1.5
    chosen = (1, 5)
    gates = {1: 0.65, 5: 0.35}
    for i in range(n):
        x = 0.2 + i * (bw + gap)
        s.box(x, y, bw, 0.85, 'E%d' % (i + 1), size=17, weight='bold', fill=GOLD if i in chosen else PAPER, edge=INK if i in chosen else GREY, color=INK if i in chosen else MUTE)
        if i in chosen:
            s.arrow(w / 2 + (-0.5 if i == chosen[0] else 0.5), h - 1.9, x + bw / 2, y + 0.85, color=RED, lw=2.4)
            put(s, x + bw / 2 + (-0.55 if i == chosen[0] else 0.55), y + 1.3, 'g = %.2f' % gates[i], size=15, weight='bold', color=RED)
    mt(s, 0.2, 0.98, r'Formula:  $y = \sum_{i \in \mathrm{chosen}} g_i(x)\, E_i(x)$', size=18, ha='left')
    put(s, 0.2, 0.55, 'Toy: expert outputs 4 and 8, so y = 0.65 x 4 + 0.35 x 8 = 5.4', size=15, weight='bold', ha='left')
    put(s, 0.2, 0.2, 'g = router gate weight (toy), E = expert output. Only the chosen two are added.', size=14, ha='left', color=BODY)
    return s


@fig('x_t06_reasoning')
def reasoning(w, h, **_):
    s = Scene(w, h)
    lane_h = 1.3
    ys = [h - 0.75 - lane_h, h - 0.75 - 2 * lane_h - 0.75]
    put(s, 0.1, ys[0] + lane_h + 0.3, 'Standard model', size=19, weight='bold', ha='left')
    s.box(0.1, ys[0], 1.7, lane_h, 'Question', size=17, weight='bold', fill=PALE)
    s.arrow(1.8, ys[0] + lane_h / 2, 5.2, ys[0] + lane_h / 2, color=RED, lw=2.4)
    s.box(5.2, ys[0], 1.7, lane_h, 'Answer', size=17, weight='bold', fill=GOLD)
    put(s, 0.1, ys[1] + lane_h + 0.3, 'Reasoning model', size=19, weight='bold', ha='left')
    s.box(0.1, ys[1], 1.7, lane_h, 'Question', size=17, weight='bold', fill=PALE)
    s.arrow(1.8, ys[1] + lane_h / 2, 2.1, ys[1] + lane_h / 2, color=RED, lw=2.4)
    s.box(2.1, ys[1], 3.1, lane_h, 'Long working-out:\nmany extra tokens', size=16, weight='bold', dash=True)
    s.arrow(5.2, ys[1] + lane_h / 2, 5.4, ys[1] + lane_h / 2, color=RED, lw=2.4)
    s.box(5.4, ys[1], 1.5, lane_h, 'Answer', size=17, weight='bold', fill=GOLD)
    put(s, w / 2, 0.3, 'More tokens written means more time and more cost.', size=17, weight='bold', color=RED)
    return s


@fig('x_t06_multimodal')
def multimodal(w, h, **_):
    s = Scene(w, h)
    # inputs
    s.box(0.1, h - 1.2, 1.9, 0.9, 'Text', size=17, weight='bold')
    gx, gy, c = 0.55, h - 3.0, 0.2
    pat = [[0, 1, 1, 1, 0], [1, 0, 1, 0, 1], [1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [0, 1, 1, 1, 0]]
    for r in range(5):
        for k in range(5):
            s.rect(gx + k * c, gy + (4 - r) * c, c, c, fill=GOLD if pat[r][k] else PAPER, edge=INK, lw=0.8)
    put(s, 1.05, gy - 0.25, 'Photo, cut in patches', size=14, color=BODY)
    xs = np.linspace(0.2, 1.9, 40)
    s.ax.plot(xs, 0.75 + 0.3 * np.sin(xs * 9) * np.exp(-((xs - 1.05) ** 2)), color=INK, lw=2, zorder=3)
    put(s, 1.05, 0.28, 'Sound', size=15, color=BODY)
    # pieces column
    s.box(3.0, 0.75, 1.5, h - 1.5, 'Tokens\nof every\nkind', size=17, weight='bold', fill=PALE)
    for y in (h - 0.75, h - 2.0, 0.75):
        s.arrow(2.05, y if y > 1 else 0.9, 3.0, h / 2 + (0.3 if y > h / 2 else (-0.3 if y < 1 else 0)), color=RED, lw=2)
    s.arrow(4.5, h / 2, 5.2, h / 2, color=RED, lw=2.4)
    s.box(5.2, h / 2 - 1.1, 2.3, 2.2, 'One model\n\nAnswers in\ntext', size=17, weight='bold', fill=GOLD)
    return s


# ---------------------------------------------------------------------------------------------------------------- diffusion (computed, not a real image model)
@fig('x_t06_diffusion')
def diffusion(w, h, **_):
    s = Scene(w, h)
    n = 24
    img = np.full((n, n), 0.92)
    img[6:20, 6:18] = 0.18      # a simple sack shape
    img[10:13, 6:18] = 0.85     # a band
    img[3:6, 9:15] = 0.35       # the neck
    rng = np.random.RandomState(6)
    noise = rng.normal(0.5, 0.3, size=(n, n))
    levels = [0.0, 0.25, 0.5, 0.75, 1.0]
    side = 1.75
    gap = (w - 5 * side - 0.4) / 4
    top = h - 0.9
    for i, a in enumerate(levels):
        x = 0.2 + i * (side + gap)
        pic = np.clip(np.sqrt(1 - a) * img + np.sqrt(a) * noise, 0, 1)
        s.ax.imshow(pic, cmap='gray', vmin=0, vmax=1, extent=(x, x + side, top - side, top), interpolation='nearest', zorder=2, aspect='auto')
        s.rect(x, top - side, side, side, fill='none', edge=INK, lw=1.4, z=3)
        put(s, x + side / 2, top - side - 0.25, ['clean', 'a little noise', 'half noise', 'mostly noise', 'pure noise'][i], size=14, color=BODY)
        if i < 4:
            s.arrow(x + side + 0.05, top + 0.35, x + side + gap - 0.05, top + 0.35, color=INK, lw=2, head=11)
            s.arrow(x + side + gap - 0.05, top - side - 0.62, x + side + 0.05, top - side - 0.62, color=RED, lw=2, head=11)
    put(s, w / 2, h - 0.25, 'Training: add noise a step at a time (computed here, easy)', size=16, weight='bold')
    put(s, w / 2, 0.22, 'Making an image: start from noise and remove a little at each step (learned)', size=16, weight='bold', color=RED)
    return s


# ---------------------------------------------------------------------------------------------------------------- benchmarks
@fig('x_t06_bench_cards')
def bench_cards(w, h, **_):
    s = Scene(w, h)
    cards = [('book', 'MMLU, 2020', 'Massive Multitask Language Understanding: 57 subjects, from elementary mathematics to law'),
             ('calculator', 'GSM8K, 2021', 'Grade School Math 8K: about 8,500 school maths word problems'),
             ('laptop', 'HumanEval, 2021', 'Write a program from a description, then run it to check'),
             ('person', 'Chatbot Arena, 2024', 'People vote for the better of two answers: over 240,000 votes at the time of the paper')]
    n = 4
    pw = (w - 0.2 * (n - 1) - 0.2) / n
    for i, (ic, hd, tx) in enumerate(cards):
        x0 = 0.1 + i * (pw + 0.2)
        s.box(x0, 0.05, pw, h - 0.1, '', fill=PAPER, edge=INK, lw=1.8)
        s.icon(ic, x0 + pw / 2, h - 0.6, 0.7)
        put(s, x0 + pw / 2, h - 1.2, hd, size=18, weight='bold', color=RED)
        put(s, x0 + pw / 2, h - 2.5, wrap(tx, pw - 0.3, 16), size=16)
    return s


@fig('x_t06_bench_limits')
def bench_limits(w, h, **_):
    s = Scene(w, h)
    r = 1.55
    cy = h / 2 + 0.25
    from matplotlib.patches import Circle
    s.ax.add_patch(Circle((w / 2 - 1.3, cy), r, fc=GOLD, ec=INK, lw=2, alpha=0.55, zorder=2))
    s.ax.add_patch(Circle((w / 2 + 1.3, cy), r, fc=PAPER, ec=RED, lw=2.4, alpha=0.8, zorder=2))
    put(s, w / 2 - 2.0, cy + 0.2, 'What the\nbenchmark\nasks', size=17, weight='bold')
    put(s, w / 2 + 2.0, cy + 0.2, 'Your\ninvoices,\nclients, rules', size=17, weight='bold', color=RED)
    put(s, w / 2, 1.0, 'small overlap', size=15, weight='bold')
    s.arrow(w / 2, 1.2, w / 2, cy - 0.55, color=INK, lw=1.6, head=8)
    put(s, w / 2, 0.45, 'A score describes the left circle. Your work is the right one.', size=17, weight='bold')
    return s


# ---------------------------------------------------------------------------------------------------------------- the recorded comparison
def _claude():
    t = (RUN / 'prompts' / 'claude_reply_verbatim.txt').read_text()
    a = t.index('"Good morning')
    b = t.index('"', a + 1)
    return t[a + 1:b]


@fig('x_t06_two_answers')
def two_answers(w, h, **_):
    s = Scene(w, h)
    pw = (w - 0.3) / 2
    left = _claude()
    q = Q['runs'][0]['reply'].replace('**', '').replace('\\( ', '').replace(' \\)', '').replace('\\times', 'x')
    q = ' '.join(q.split())
    right = q[:q.index('Dear Shop Owner')] + '... Therefore, the correct charge should be based on the actual number of usable bags received, which is 17 bags ... we kindly request that you pay the following amount: ... UGX 1,326,000. Please settle the remaining balance within two business days ...'
    panels = [('Claude, fresh subagent session', 'Reply, in full', left), ('Qwen2.5-1.5B-Instruct, greedy run', 'Excerpts, marked with ...', right)]
    for i, (hd, sub, body) in enumerate(panels):
        x0 = i * (pw + 0.3)
        s.box(x0, 0.05, pw, h - 0.1, '', fill=PAPER, edge=INK, lw=1.8)
        put(s, x0 + 0.15, h - 0.3, hd, size=17, weight='bold', color=RED, ha='left')
        put(s, x0 + 0.15, h - 0.7, sub, size=14, color=MUTE, ha='left')
        put(s, x0 + 0.15, (h - 0.9) / 2, wrap(body, pw - 0.3, 16.5), size=16.5, ha='left', va='center')
    return s


@fig('x_t06_scorecard')
def scorecard(w, h, **_):
    s = Scene(w, h)
    cols = ['Claude\n(1 run)', 'Qwen 1.5B\ngreedy', 'Qwen 1.5B\nsample 1', 'Qwen 1.5B\nsample 2']
    rows = [('Label: product quality (my call)', [1, 0, 0, 0]), ('Sum 1,560,000 correct', [1, 1, 1, 1]), ('Reply within 70 words', [1, 0, 0, 0]),
            ('Invents nothing the company never said', [1, 0, 0, 0]), ('Says what it cannot confirm', [1, 0, 0, 0])]
    lw = 4.6
    cw = (w - lw - 0.2) / 4
    top = h - 0.15
    hh = 0.8
    for j, c in enumerate(cols):
        put(s, lw + 0.1 + j * cw + cw / 2, top - hh / 2, c, size=16, weight='bold')
    rh = (top - hh - 0.65) / len(rows)
    for i, (nm, vals) in enumerate(rows):
        y = top - hh - (i + 1) * rh
        s.line(0.1, y, w - 0.1, y, color=HAIR, lw=1)
        put(s, 0.15, y + rh / 2, nm, size=17, ha='left')
        for j, v in enumerate(vals):
            s.icon('check' if v else 'cross', lw + 0.1 + j * cw + cw / 2, y + rh / 2, 0.42)
    return s


# ---------------------------------------------------------------------------------------------------------------- model cards
@fig('x_t06_model_card')
def model_card(w, h, **_):
    s = Scene(w, h)
    pw = (w - 0.3) / 2
    cards = [('Qwen2.5-1.5B-Instruct', [('Licence', 'Apache-2.0'), ('Size', '1.54 billion parameters'), ('Context window', '32,768 tokens'), ('Languages', 'over 29'),
                                        ('Stage', '"Pretraining & Post-training"'), ('Sections', 'Introduction, Requirements, Quickstart, Evaluation, Citation')],
              'No section on limitations'),
             ('GPT-2 (small)', [('Licence', 'MIT'), ('Size', '124 million parameters'), ('Trained on', 'WebText, about 40 GB, not released'), ('Use', 'text generation or fine-tuning'),
                                ('Warns', 'cannot tell fact from fiction'), ('Bias', 'reflects its training data')],
              'Has a limitations and bias part')]
    for i, (hd, rows, foot) in enumerate(cards):
        x0 = i * (pw + 0.3)
        s.box(x0, 0.05, pw, h - 0.1, '', fill=PAPER, edge=INK, lw=1.8)
        s.box(x0, h - 0.65, pw, 0.6, hd, size=18, weight='bold', fill=INK, color=PAPER, edge=INK)
        rh = (h - 1.4) / len(rows)
        for k, (a, b) in enumerate(rows):
            y = h - 0.65 - (k + 1) * rh
            put(s, x0 + 0.15, y + rh / 2, a, size=15, weight='bold', ha='left', color=MUTE)
            put(s, x0 + 1.85, y + rh / 2, wrap(b, pw - 2.0, 15), size=15, ha='left')
        put(s, x0 + pw / 2, 0.3, foot, size=16, weight='bold', color=RED)
    return s


# ---------------------------------------------------------------------------------------------------------------- scale build-up
@fig('x_t06_scale')
def scale(w, h, **_):
    import math
    s = Scene(w, h)
    rows = [('Session 1 digit network', 1210, '1,210', False), ('GPT-2 small (12 blocks)', 124439808, '124 million', True),
            ('Qwen2.5-1.5B-Instruct', 1540000000, '1.54 billion', False), ('GPT-3, as named in the 2022 InstructGPT paper', 175000000000, '175 billion', False)]
    n = len(rows)
    top = h - 0.3
    rh = (top - 0.95) / n
    x0, bw0 = 4.5, w - 4.5 - 2.0
    lo, hi = 2.9, 11.3
    for i, (name, v, lab, hl) in enumerate(rows):
        yc = top - rh * (i + 0.5)
        put(s, 0.1, yc, name.replace(', as named in', '\nas named in') if len(name) > 30 else name, size=16, weight='bold' if hl else 'normal', ha='left')
        L = max(0.15, bw0 * (math.log10(v) - lo) / (hi - lo))
        s.rect(x0, yc - rh * 0.28, L, rh * 0.56, fill=GOLD if hl else GREY, edge=INK, lw=1.2)
        put(s, x0 + L + 0.12, yc, lab, size=17, weight='bold', ha='left')
    put(s, w / 2, 0.55, 'Same loop at every step: predict the next token, measure the loss, adjust the weights.', size=16, weight='bold', color=RED)
    put(s, w / 2, 0.2, 'Bar length shows the power of ten. A bar twice as long is far more than twice the parameters.', size=15, color=MUTE)
    return s


# ---------------------------------------------------------------------------------------------------------------- loss and perplexity
@fig('x_t06_formula')
def formula(w, h, **_):
    s = Scene(w, h)
    ps = [0.18, 0.50, 0.25]
    losses = [-math.log(p) for p in ps]
    avg = sum(losses) / 3
    ppl = math.exp(avg)
    colw = [2.4, 2.2, 2.0]
    heads = ['Token', 'p of the true token', 'loss = \u2212ln p']
    xs = [0.1]
    for c in colw:
        xs.append(xs[-1] + c)
    top = h - 0.05
    for j, t in enumerate(heads):
        s.box(xs[j], top - 0.6, colw[j], 0.6, t, size=15, weight='bold', fill=PALE, r=0.02, lw=1.2)
    names = ['1 (days, Session 5)', '2', '3']
    for i, (nm, p, l) in enumerate(zip(names, ps, losses)):
        y = top - 0.6 - (i + 1) * 0.52
        for j, v in enumerate([nm, '%.2f' % p, '%.2f' % l]):
            s.box(xs[j], y, colw[j], 0.52, v, size=17, weight='bold' if i == 0 else 'normal', fill=GOLD if (i == 0 and j == 2) else PAPER, r=0.02, lw=1.2)
    put(s, 0.1, 1.5, 'Average loss  L = (%.2f + %.2f + %.2f) / 3 = %.2f' % (losses[0], losses[1], losses[2], avg), size=16, weight='bold', ha='left', color=RED)
    put(s, 0.1, 0.95, 'Three tokens of one text: the probability the model gave to the\ntrue next token. Only the first is a recorded number.', size=14, ha='left', color=BODY)
    x1 = 6.9
    s.box(x1, 0.05, w - x1 - 0.05, h - 0.1, '', fill=PAPER, edge=INK, lw=1.6)
    put(s, x1 + 0.2, h - 0.4, 'Pretraining objective', size=17, weight='bold', color=RED, ha='left')
    mt(s, x1 + 0.2, h - 0.95, r'$L = -(1/N)\,\sum_{t=1}^{N} \ln P(x_t \mid x_{<t})$', size=17, ha='left')
    put(s, x1 + 0.2, h - 1.5, 'N = tokens in the corpus (billions), x_t = token t,\nx_<t = all tokens before it. Same loss as Session 5.', size=14, ha='left', color=BODY)
    put(s, x1 + 0.2, h - 2.25, 'Perplexity', size=17, weight='bold', color=RED, ha='left')
    mt(s, x1 + 0.2, h - 2.75, r'$\mathrm{PPL} = e^{L} = e^{%.2f} \approx %.1f$' % (avg, ppl), size=17, ha='left')
    put(s, x1 + 0.2, h - 3.35, 'As unsure as picking among about %.1f equally\nlikely tokens. Lower is better.' % ppl, size=14, ha='left', color=BODY)
    return s


# ================================================================================================ 11 Nov 2026 rework: explain before use
def _cell_row(s, xs, ws, y, h, vals, size=16, bold=(), fills=None):
    for j, v in enumerate(vals):
        f = fills[j] if fills else PAPER
        s.box(xs[j], y, ws[j], h, v, size=size, weight='bold' if j in bold else 'normal', fill=f, r=0.02, lw=1.2)


def _cols(x0, ws):
    xs = [x0]
    for c in ws[:-1]:
        xs.append(xs[-1] + c)
    return xs


@fig('x_t06_avgloss')
def avgloss(w, h, **_):
    """Average next-token loss over three tokens, step by step. Token 1 is the recorded Session 5 number."""
    s = Scene(w, h)
    ps = [0.18, 0.50, 0.25]
    ls = [-math.log(p) for p in ps]
    tot = sum(round(l, 2) for l in ls)
    ws = [1.0, 2.2, 2.2, 1.9]
    xs = _cols(0.05, ws)
    top = h - 0.1
    _cell_row(s, xs, ws, top - 0.75, 0.75, ['Token', 'True next token', 'p the model gave it', 'loss = −ln p'], size=15, bold=(0, 1, 2, 3), fills=[PALE] * 4)
    names = [('1', 'days (Session 5)'), ('2', 'a full stop'), ('3', 'The')]
    for i, ((n, tok), p, l) in enumerate(zip(names, ps, ls)):
        y = top - 0.75 - (i + 1) * 0.6
        _cell_row(s, xs, ws, y, 0.6, [n, tok, '%.2f' % p, '%.2f' % l], size=17, bold=(3,), fills=[PAPER, PAPER, PAPER, GOLD])
    put(s, 0.05, 0.75, 'Token 1 is the recorded Session 5 number. Tokens 2 and 3 are an illustration.', size=14, ha='left', color=MUTE)
    put(s, 0.05, 0.3, 'Low p (an unsure model) gives a high loss. p = 1 gives loss 0.', size=15, ha='left', color=BODY)
    x1 = 7.75
    s.box(x1, 0.1, w - x1 - 0.05, h - 0.2, '', fill=PAPER, edge=INK, lw=1.6)
    put(s, x1 + 0.2, h - 0.5, 'Average loss, step by step', size=17, weight='bold', color=RED, ha='left')
    put(s, x1 + 0.2, h - 1.15, 'Add the three losses:', size=16, ha='left')
    put(s, x1 + 0.2, h - 1.6, '%.2f + %.2f + %.2f = %.2f' % (ls[0], ls[1], ls[2], tot), size=18, weight='bold', ha='left')
    put(s, x1 + 0.2, h - 2.25, 'Divide by the 3 tokens:', size=16, ha='left')
    put(s, x1 + 0.2, h - 2.7, '%.2f ÷ 3 = %.2f' % (tot, tot / 3), size=18, weight='bold', ha='left')
    s.box(x1 + 0.2, 0.35, w - x1 - 0.45, 0.75, 'Average loss = %.2f' % (tot / 3), size=19, weight='bold', fill=GOLD)
    return s


@fig('x_t06_lossformula')
def lossformula(w, h, **_):
    s = Scene(w, h)
    mt(s, w / 2, h - 0.55, r'$L \;=\; -\,\frac{1}{N}\;\sum_{t=1}^{N}\; \ln\, p_t$', size=26, ha='center')
    parts = [(r'$p_t$', 'The probability the model gave to the true token number t, given the tokens before it. t counts the tokens: t = 1 is the first.'),
             (r'$-\ln\, p_t$', 'The loss for one token, as in Session 5. Minus ln makes it positive.'),
             (r'$\sum_{t=1}^{N}$', 'Add up: one term for each token, from the first to the last.'),
             (r'$1/N$', 'Divide by N, the number of tokens. That makes the sum an average.')]
    n = len(parts)
    g = 0.15
    pw = (w - 0.1 - g * (n - 1)) / n
    for i, (a, b) in enumerate(parts):
        x = 0.05 + i * (pw + g)
        s.box(x, 0.95, pw, 2.15, '', fill=PAPER, edge=INK, lw=1.4)
        mt(s, x + pw / 2, 2.7, a, size=19, color=RED)
        put(s, x + pw / 2, 1.75, wrap(b, pw - 0.3, 15), size=15)
    put(s, w / 2, 0.55, 'Our example: N = 3, so L = (1.71 + 0.69 + 1.39) ÷ 3 = 1.26.', size=17, weight='bold')
    put(s, w / 2, 0.15, 'In pretraining N is billions of tokens. Industry name: cross-entropy loss.', size=15, color=BODY)
    return s


@fig('x_t06_perplexity')
def perplexity(w, h, **_):
    s = Scene(w, h)
    # panel 1: four equally likely words
    pw = 3.75
    s.box(0.05, 0.1, pw, h - 0.2, '', fill=PAPER, edge=INK, lw=1.6)
    put(s, 0.05 + pw / 2, h - 0.45, 'A blind guess among 4 words', size=17, weight='bold', color=RED)
    for k, wd in enumerate(['days', 'weeks', 'hours', 'months']):
        x = 0.25 + k * 0.85
        s.box(x, h - 1.65, 0.75, 0.8, '', fill=GOLD if k == 0 else PALE, lw=1.2)
        put(s, x + 0.375, h - 1.25, '25%', size=15, weight='bold')
        put(s, x + 0.375, h - 1.95, wd, size=14, color=BODY)
    put(s, 0.25, 1.6, 'loss each time = −ln 0.25 = 1.39', size=15, ha='left')
    put(s, 0.25, 1.15, 'average loss L = 1.39', size=15, ha='left')
    mt(s, 0.25, 0.6, r'$e^{1.39} = 4.0$', size=19, ha='left')
    # panel 2: perplexity
    x2 = 4.05
    s.box(x2, 0.1, pw, h - 0.2, '', fill=PAPER, edge=INK, lw=1.6)
    put(s, x2 + pw / 2, h - 0.45, 'Perplexity undoes the ln', size=17, weight='bold', color=RED)
    mt(s, x2 + pw / 2, h - 1.15, r'$\mathrm{perplexity} = e^{L}$', size=22, ha='center')
    put(s, x2 + 0.2, h - 2.0, wrap('e to the power undoes ln, as e did in softmax (Session 5).', pw - 0.4, 15) + '\n' + wrap('A blind guess among 4 words: perplexity 4.', pw - 0.4, 15), size=15, ha='left')
    mt(s, x2 + 0.2, 0.95, r'Our text: $L = 1.26$, $e^{1.26} \approx 3.5$', size=16, ha='left')
    put(s, x2 + 0.2, 0.45, 'As unsure as 3.5 equal words', size=15, weight='bold', ha='left')
    # panel 3: how to read it
    x3 = 8.05
    s.box(x3, 0.1, w - x3 - 0.05, h - 0.2, '', fill=PAPER, edge=INK, lw=1.6)
    put(s, x3 + (w - x3) / 2, h - 0.45, 'How to read it', size=17, weight='bold', color=RED)
    rows = [('1', 'always sure and right'), ('3.5', 'our three tokens'), ('50,257', 'blind guess over all GPT-2 tokens')]
    for i, (a, b) in enumerate(rows):
        y = h - 1.25 - i * 0.85
        s.box(x3 + 0.15, y - 0.3, 1.2, 0.6, a, size=16, weight='bold', fill=GOLD if i == 1 else PALE, r=0.03)
        put(s, x3 + 1.5, y, wrap(b, w - x3 - 1.7, 14), size=14, ha='left')
    put(s, x3 + (w - x3) / 2, 0.45, 'Lower is better.', size=16, weight='bold')
    return s


@fig('x_t06_posttrain')
def posttrain(w, h, **_):
    s = Scene(w, h)
    ws = [2.9, 4.4, 4.5]
    xs = _cols(0.05, ws)
    top = h - 0.05
    heads = ['Stage', 'Data it uses', 'What changes']
    for j, t in enumerate(heads):
        put(s, xs[j] + 0.1, top - 0.3, t, size=17, weight='bold', ha='left')
    s.line(0.05, top - 0.6, w - 0.05, top - 0.6, color=INK, lw=2)
    rows = [('Pretraining', 'Raw text, billions of tokens, nobody labels it', 'Weights learn to continue any text', PALE, 'book'),
            ('Supervised fine-tuning (SFT)', 'Instructions, each with a good answer written by a person', 'Same weights nudged so the model writes answers like those', GOLD, 'pen'),
            ('Preference tuning, e.g. RLHF', 'A prompt, two answers, and which one a person preferred', 'Same weights nudged towards answers people prefer', GOLD, 'check')]
    rh = (top - 0.6 - 0.1) / 3
    for i, (a, b, c, f, ic) in enumerate(rows):
        y = top - 0.6 - (i + 1) * rh
        s.box(xs[0], y + 0.08, ws[0] - 0.15, rh - 0.16, '', fill=f, lw=1.4)
        s.icon(ic, xs[0] + 0.35, y + rh / 2, 0.5)
        put(s, xs[0] + 0.7, y + rh / 2, wrap(a, ws[0] - 0.95, 16), size=16, weight='bold', ha='left')
        put(s, xs[1] + 0.1, y + rh / 2, wrap(b, ws[1] - 0.3, 16), size=16, ha='left')
        put(s, xs[2] + 0.1, y + rh / 2, wrap(c, ws[2] - 0.3, 16), size=16, ha='left')
        s.line(0.05, y, w - 0.05, y, color=HAIR, lw=1)
    return s


@fig('x_t06_sft')
def sft(w, h, **_):
    s = Scene(w, h)
    s.box(0.05, h - 2.15, w - 0.1, 2.05, '', fill=PAPER, edge=INK, lw=1.6)
    put(s, 0.25, h - 0.4, 'One training example (a pair)', size=17, weight='bold', color=RED, ha='left')
    put(s, 0.25, h - 0.95, wrap('Instruction: Write a one-line thank-you to a colleague who covered my shift.', w - 0.5, 16), size=16, ha='left')
    put(s, 0.25, h - 1.7, wrap('Answer written by a person: Thank you for covering my shift on Friday. I owe you one.', w - 0.5, 16), size=16, ha='left', weight='bold')
    put(s, 0.05, h - 2.55, 'Same next-token loss, counted on the answer tokens', size=16, weight='bold', ha='left')
    ws = [2.1, 2.6, 2.8]
    xs = _cols(0.05, ws)
    yb = h - 3.55
    _cell_row(s, xs, ws, yb, 0.55, ['First token', 'p before SFT', 'p after SFT'], size=15, bold=(0, 1, 2), fills=[PALE] * 3)
    _cell_row(s, xs, ws, yb - 0.55, 0.55, ['Thank', '0.05, loss 3.00', '0.60, loss 0.51'], size=16, fills=[PAPER, PAPER, GOLD])
    put(s, 0.05, 0.25, 'Illustration numbers: loss = −ln p, as in Session 5.', size=14, ha='left', color=MUTE)
    return s


@fig('x_t06_rlhf')
def rlhf(w, h, **_):
    s = Scene(w, h)
    # step 1: the data
    pw = 3.9
    s.box(0.05, 0.1, pw, h - 0.2, '', fill=PAPER, edge=INK, lw=1.6)
    put(s, 0.25, h - 0.4, '1  The data: a person compares', size=16, weight='bold', color=RED, ha='left')
    put(s, 0.25, h - 0.85, 'Prompt: Explain a late fee.', size=15, ha='left')
    s.box(0.25, h - 2.0, pw - 0.4, 0.85, '', fill=GOLD, lw=1.2)
    put(s, 0.4, h - 1.58, wrap('A: short, polite, correct', pw - 1.4, 15), size=15, ha='left', weight='bold')
    s.icon('check', pw - 0.45, h - 1.58, 0.45)
    s.box(0.25, h - 3.0, pw - 0.4, 0.85, '', fill=PALE, lw=1.2)
    put(s, 0.4, h - 2.58, wrap('B: long, rude, wrong', pw - 1.4, 15), size=15, ha='left')
    s.icon('cross', pw - 0.45, h - 2.58, 0.45)
    put(s, 0.25, 0.5, 'The person prefers A.', size=15, weight='bold', ha='left')
    # step 2: reward model
    x2 = pw + 0.25
    s.box(x2, 0.1, pw, h - 0.2, '', fill=PAPER, edge=INK, lw=1.6)
    put(s, x2 + 0.2, h - 0.4, '2  A reward model learns', size=16, weight='bold', color=RED, ha='left')
    put(s, x2 + 0.2, h - 1.2, wrap('A second network that gives an answer a score. Trained so the preferred answer scores higher.', pw - 0.4, 15), size=15, ha='left')
    _cell_row(s, [x2 + 0.3, x2 + 0.3 + 1.7], [1.7, 1.6], 1.4, 0.55, ['Answer A', '2.1'], size=16, bold=(1,), fills=[PALE, GOLD])
    _cell_row(s, [x2 + 0.3, x2 + 0.3 + 1.7], [1.7, 1.6], 0.85, 0.55, ['Answer B', '−0.4'], size=16, bold=(1,), fills=[PALE, PAPER])
    put(s, x2 + 0.2, 0.45, 'Scores: illustration', size=14, ha='left', color=MUTE)
    # step 3: RL loop
    x3 = 2 * (pw + 0.25) - 0.05
    s.box(x3, 0.1, w - x3 - 0.05, h - 0.2, '', fill=PAPER, edge=INK, lw=1.6)
    put(s, x3 + 0.2, h - 0.4, '3  Reinforcement learning', size=16, weight='bold', color=RED, ha='left')
    steps = ['The model writes an answer', 'The reward model scores it', 'Weights nudged towards high scores']
    steps = ['The model writes\nan answer', 'The reward model\nscores it', 'Weights nudged\ntowards high scores']
    for i, t in enumerate(steps):
        y = h - 1.3 - i * 0.95
        s.box(x3 + 0.2, y - 0.36, w - x3 - 0.45, 0.72, t, size=15, fill=GOLD if i == 2 else PALE, lw=1.2)
        if i < 2:
            s.arrow(x3 + (w - x3) / 2, y - 0.36, x3 + (w - x3) / 2, y - 0.59, color=RED, lw=2, head=10)
    put(s, x3 + 0.2, 0.45, 'Repeat many times.', size=15, weight='bold', ha='left')
    return s


@fig('x_t06_moe_pic')
def moe_pic(w, h, **_):
    s = Scene(w, h)
    s.box(w / 2 - 1.2, h - 0.75, 2.4, 0.6, 'token: invoice', size=18, weight='bold', fill=GOLD)
    s.arrow(w / 2, h - 0.75, w / 2, h - 1.15, color=INK, lw=2)
    s.box(w / 2 - 1.6, h - 1.75, 3.2, 0.6, 'Router: picks 2 of 8', size=17, weight='bold')
    n, gap = 8, 0.12
    bw = (w - 0.4 - gap * (n - 1)) / n
    y = 1.6
    chosen = (1, 5)
    for i in range(n):
        x = 0.2 + i * (bw + gap)
        on = i in chosen
        s.box(x, y, bw, 0.85, 'E%d' % (i + 1), size=17, weight='bold', fill=GOLD if on else PAPER, edge=INK if on else GREY, color=INK if on else MUTE)
        if on:
            s.arrow(w / 2 + (-0.6 if i == 1 else 0.6), h - 1.75, x + bw / 2, y + 0.85, color=RED, lw=2.4)
            s.arrow(x + bw / 2, y, w / 2 + (-0.35 if i == 1 else 0.35), 0.95, color=RED, lw=2.4)
    s.box(w / 2 - 0.95, 0.35, 1.9, 0.6, 'Add the two', size=17, weight='bold', fill=PALE)
    put(s, 0.15, 0.85, 'Each expert: a feed-', size=14, ha='left', color=BODY)
    put(s, 0.15, 0.55, 'forward network', size=14, ha='left', color=BODY)
    put(s, w - 0.2, 0.85, 'Grey experts do', size=14, ha='right', color=BODY)
    put(s, w - 0.2, 0.55, 'no work on this token', size=14, ha='right', color=BODY)
    return s


@fig('x_t06_moe_gate')
def moe_gate(w, h, **_):
    s = Scene(w, h)
    scores = [0.1, 1.2, -0.3, 0.4, -1.0, 0.6, 0.2, -0.5]
    # 1 router scores
    put(s, 0.05, h - 0.25, '1  Router scores', size=16, weight='bold', color=RED, ha='left')
    for i, v in enumerate(scores):
        x = 0.05 + (i % 4) * 0.72
        y = h - 1.15 - (i // 4) * 0.95
        on = i in (1, 5)
        s.box(x, y, 0.66, 0.5, ('%.1f' % v).replace('-', '−'), size=15, weight='bold' if on else 'normal', fill=GOLD if on else PAPER, r=0.03, lw=1.2)
        put(s, x + 0.33, y - 0.2, 'E%d' % (i + 1), size=14, color=BODY)
    put(s, 0.05, 1.05, 'Keep the top 2:', size=15, ha='left')
    put(s, 0.05, 0.65, 'E2 (1.2) and E6 (0.6)', size=15, weight='bold', ha='left')
    # 2 softmax of the two
    x2 = 3.15
    s.line(x2 - 0.1, 0.1, x2 - 0.1, h - 0.1, color=HAIR, lw=1)
    put(s, x2 + 0.1, h - 0.25, '2  Softmax of the two (Session 5)', size=16, weight='bold', color=RED, ha='left')
    mt(s, x2 + 0.1, h - 0.9, r'$e^{1.2} = 3.32 \qquad e^{0.6} = 1.82$', size=17, ha='left')
    put(s, x2 + 0.1, h - 1.5, 'Total: 3.32 + 1.82 = 5.14', size=16, ha='left')
    put(s, x2 + 0.1, h - 2.15, 'Gate weight g₂ = 3.32 ÷ 5.14 = 0.65', size=16, weight='bold', ha='left')
    put(s, x2 + 0.1, h - 2.7, 'Gate weight g₆ = 1.82 ÷ 5.14 = 0.35', size=16, weight='bold', ha='left')
    put(s, x2 + 0.1, 0.65, 'The two gate weights add up to 1.', size=15, ha='left', color=BODY)
    # 3 blend
    x3 = 7.75
    s.line(x3 - 0.1, 0.1, x3 - 0.1, h - 0.1, color=HAIR, lw=1)
    put(s, x3 + 0.1, h - 0.25, '3  Blend the expert outputs', size=16, weight='bold', color=RED, ha='left')
    put(s, x3 + 0.1, h - 0.9, 'E2 outputs 4, E6 outputs 8', size=16, ha='left')
    put(s, x3 + 0.1, h - 1.5, 'y = 0.65 × 4 + 0.35 × 8', size=17, ha='left')
    put(s, x3 + 0.1, h - 2.05, '   = 2.6 + 2.8 = 5.4', size=17, weight='bold', ha='left')
    s.box(x3 + 0.1, 0.45, w - x3 - 0.2, 0.75, '', fill=GOLD, lw=1.4)
    mt(s, x3 + 0.1 + (w - x3 - 0.2) / 2, 0.82, r'$y = g_2 E_2 + g_6 E_6$', size=19, ha='center')
    return s


@fig('x_t06_reasoning2')
def reasoning2(w, h, **_):
    s = Scene(w, h)
    put(s, 0.05, h - 0.25, 'Question: 3 bags at UGX 78,000 and 2 at UGX 45,000. Total?', size=15, weight='bold', ha='left')
    put(s, 0.05, h - 0.85, 'Standard model', size=17, weight='bold', ha='left', color=RED)
    s.box(0.05, h - 1.75, w - 0.1, 0.6, 'Answer: UGX 324,000', size=17, fill=GOLD)
    put(s, 0.05, h - 2.15, 'Reasoning model', size=17, weight='bold', ha='left', color=RED)
    lines = ['3 × 78,000 = 234,000', '2 × 45,000 = 90,000', '234,000 + 90,000 = 324,000']
    s.box(0.05, 1.05, w - 0.1, 1.45, '', fill=PAPER, dash=True, lw=1.6)
    for i, t in enumerate(lines):
        put(s, 0.3, 2.2 - i * 0.43, t, size=16, ha='left')
    put(s, w - 0.25, 2.2, 'working', size=15, ha='right', color=MUTE)
    put(s, w - 0.25, 1.77, 'tokens', size=15, ha='right', color=MUTE)
    s.box(0.05, 0.3, w - 0.1, 0.6, 'Answer: UGX 324,000', size=17, fill=GOLD)
    return s


@fig('x_t06_patches')
def patches(w, h, **_):
    s = Scene(w, h)
    # photo grid 14 x 14 drawn small
    g, c = 14, 0.17
    x0, y0 = 0.15, h - 0.6 - g * c
    rng = np.random.RandomState(3)
    for r in range(g):
        for k in range(g):
            v = rng.rand()
            s.rect(x0 + k * c, y0 + r * c, c, c, fill=GOLD if v > 0.55 else (PALE if v > 0.25 else GREY), edge=INK, lw=0.4)
    s.rect(x0 + 3 * c, y0 + 9 * c, c, c, fill=RED, edge=INK, lw=1.4, z=3)
    put(s, x0 + g * c / 2, h - 0.3, 'Photo, 224 × 224 pixels', size=15, weight='bold')
    put(s, x0 + g * c / 2, y0 - 0.3, 'cut into 14 × 14 = 196', size=15)
    put(s, x0 + g * c / 2, y0 - 0.65, 'patches of 16 × 16 pixels', size=15)
    xr = 2.85
    s.arrow(x0 + g * c + 0.1, h - 1.8, xr - 0.05, h - 1.8, color=RED, lw=2.2)
    s.box(xr, h - 2.6, w - xr - 0.05, 1.5, '', fill=PAPER, lw=1.4)
    put(s, xr + 0.15, h - 1.4, 'One patch (red)', size=16, weight='bold', ha='left', color=RED)
    put(s, xr + 0.15, h - 1.85, '16 × 16 pixels × 3 colours', size=16, ha='left')
    put(s, xr + 0.15, h - 2.3, '= 768 numbers → one input vector', size=16, weight='bold', ha='left')
    s.box(xr, 0.15, w - xr - 0.05, 1.75, '', fill=GOLD, lw=1.4)
    put(s, xr + 0.15, 1.55, 'Text tokens + 196 patch vectors', size=16, weight='bold', ha='left')
    put(s, xr + 0.15, 1.05, 'go in side by side; attention', size=16, ha='left')
    put(s, xr + 0.15, 0.6, '(Session 5) mixes them', size=16, ha='left')
    return s


@fig('x_t06_bench_what')
def bench_what(w, h, **_):
    s = Scene(w, h)
    parts = [('Fixed questions', 'the same for every model', 'book'), ('Answer key', 'the right answer to each', 'check'), ('Scoring rule', 'how a reply counts as right', 'calculator')]
    pw = (w - 0.3) / 3
    for i, (a, b, ic) in enumerate(parts):
        x = 0.05 + i * (pw + 0.1)
        s.box(x, h - 1.75, pw, 1.65, '', fill=PALE, lw=1.4)
        s.icon(ic, x + pw / 2, h - 0.5, 0.55)
        put(s, x + pw / 2, h - 1.05, a, size=16, weight='bold')
        put(s, x + pw / 2, h - 1.45, wrap(b, pw - 0.2, 14), size=14, color=BODY)
    put(s, 0.05, 2.65, 'Accuracy = correct ÷ total (Session 3)', size=18, weight='bold', ha='left', color=RED)
    put(s, 0.05, 2.1, '1,000 questions, 712 right:', size=17, ha='left')
    put(s, 0.05, 1.6, '712 ÷ 1,000 = 0.712 = 71.2%', size=19, weight='bold', ha='left')
    s.box(0.05, 0.15, w - 0.1, 1.05, '', fill=PAPER, lw=1.4)
    put(s, 0.25, 0.9, 'Baseline: 4 options per question, so a blind', size=15, ha='left')
    put(s, 0.25, 0.45, 'guess is right 1 time in 4 = 25%.', size=15, ha='left')
    return s


@fig('x_t06_contamination')
def contamination(w, h, **_):
    s = Scene(w, h)
    put(s, 0.05, h - 0.25, 'Pretraining corpus (web text)', size=16, weight='bold', ha='left')
    rnd = random.Random(4)
    for r in range(2):
        for k in range(12):
            x = 0.05 + k * 0.42
            y = h - 0.95 - r * 0.42
            leak = (r, k) == (1, 7)
            s.rect(x, y, 0.36, 0.34, fill=RED if leak else (PALE if rnd.random() > 0.4 else PAPER), edge=INK, lw=0.8)
    put(s, 0.05, h - 1.65, 'Red: a benchmark question copied onto a web page', size=15, ha='left', color=RED)
    ws = [3.6, 2.0]
    xs = [0.05, 3.65]
    _cell_row(s, xs, ws, 1.6, 0.55, ['Benchmark questions', 'Accuracy'], size=15, bold=(0, 1), fills=[PALE, PALE])
    _cell_row(s, xs, ws, 1.05, 0.55, ['Seen in training', '90%'], size=15, bold=(1,), fills=[PAPER, GOLD])
    _cell_row(s, xs, ws, 0.5, 0.55, ['Fresh, never seen', '70%'], size=15, bold=(1,), fills=[PAPER, PAPER])
    put(s, 0.05, 0.2, 'Illustration numbers', size=14, ha='left', color=MUTE)
    return s


@fig('x_t06_settings')
def settings(w, h, **_):
    s = Scene(w, h)
    ws = [6.6, 2.4, 2.8]
    xs = _cols(0.05, ws)
    top = h - 0.05
    _cell_row(s, xs, ws, top - 0.6, 0.6, ['Setting used for the same 100 questions', 'Correct', 'Accuracy'], size=16, bold=(0, 1, 2), fills=[PALE] * 3)
    rows = [('One try, no examples in the prompt', '64', '64 ÷ 100 = 64%'),
            ('Five solved examples shown in the prompt first', '70', '70 ÷ 100 = 70%'),
            ('Five tries, counted right if any try is right', '81', '81 ÷ 100 = 81%')]
    for i, (a, b, c) in enumerate(rows):
        y = top - 0.6 - (i + 1) * 0.68
        _cell_row(s, xs, ws, y, 0.68, [a, b, c], size=17, bold=(2,), fills=[PAPER, PAPER, GOLD if i == 2 else PAPER])
    put(s, 0.05, 0.75, 'Same model, same questions, three scores. Illustration numbers.', size=16, weight='bold', ha='left', color=RED)
    put(s, 0.05, 0.3, 'Compare two scores only when the settings match: prompt, examples, tries, date.', size=15, ha='left', color=BODY)
    return s
