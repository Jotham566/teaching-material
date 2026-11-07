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
    put(s, w / 2, h - 0.3, 'Pretraining on a huge text corpus (analogy: a library)', size=20, weight='bold')
    bw = 2.1
    ys = 0.95
    labs = ['Hide the next\ntoken', 'Predict it', 'Adjust the\nweights']
    for i, t in enumerate(labs):
        x = 0.3 + i * (bw + 0.4)
        s.box(x, ys, bw, 0.95, t, size=16, weight='bold', fill=PALE if i != 1 else GOLD)
        if i < 2:
            s.arrow(x + bw, ys + 0.47, x + bw + 0.4, ys + 0.47, color=RED, lw=2.4)
    put(s, w / 2, 0.5, 'Repeated billions of times. GPT-2 read about 40 GB of web pages.', size=16, color=BODY)
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
        s.box(x0, 0.95, pw, h - 1.0, '', fill=PAPER, edge=INK, lw=1.8)
        s.icon(ic, x0 + pw / 2, h - 0.6, 0.7)
        put(s, x0 + pw / 2, h - 1.2, hd, size=18, weight='bold', color=RED)
        put(s, x0 + pw / 2, h - 2.2, wrap(tx, pw - 0.3, 15), size=15)
    mt(s, 0.1, 0.5, r'$\mathrm{accuracy} = \mathrm{correct} \,/\, \mathrm{total}$', size=19, ha='left')
    put(s, 4.7, 0.65, 'Toy example: 70 correct out of 100 questions = 70%.', size=15, weight='bold', ha='left')
    put(s, 4.7, 0.27, 'MMLU has four options per question, so random guessing scores about 25%.', size=15, ha='left')
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
