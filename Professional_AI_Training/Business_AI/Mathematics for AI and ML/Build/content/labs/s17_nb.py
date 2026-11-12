"""Session 17 lab (Python): surprise, entropy, cross-entropy, KL divergence, softmax, the softmax gradient and perplexity.
The deck (content/s17.py) and the figures take every number from namespace(), which runs the SOLUTION cells of this notebook."""
import contextlib
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'kit'))
from nb import Notebook  # noqa: E402

TITLE = 'Entropy, cross-entropy, softmax and perplexity'


def _todo(nb, solution, hint, stub, code):
    nb.code(f'# {hint}\n' + (code if solution else stub))


def build(solution=False):
    nb = Notebook()
    nb.md('# Session 17 lab: entropy, cross-entropy, temperature, top-p and perplexity\n\nKLAi | Mathematics for AI and Machine Learning\n\n'
          'Today you measure surprise in bits, compute entropy, cross-entropy and Kullback-Leibler (KL) divergence, reshape a softmax with temperature and cut it with top-p, check by numbers that the gradient of softmax with cross-entropy is prediction minus target, '
          'and score a toy language model with perplexity.\n\n'
          '**How to use this notebook.** Run the cells in order with Shift and Enter. Each step has the same rhythm: **PREDICT**, **RUN**, **READ**, then **CHANGE one thing**. Type your answers in the lines that start with `>`. '
          'If a number differs from the slide called "Check your numbers", stop and find the step that went wrong.\n\n'
          '**Words and units.** *Surprise* (self-information): -log2 of the probability of an event, in bits. *Entropy*: the average surprise. *Cross-entropy*: the average surprise when reality follows P but the model believes Q. '
          '*KL divergence*: cross-entropy minus entropy. Steps 1 to 3 use log2, so they are in bits. Steps 4 to 7 use ln, like every library, so they are in nats (1 bit = 0.693 nats). '
          '*Softmax* (Session 12): turns scores (logits) into probabilities. *Temperature* and *top-p*: settings that reshape and trim those probabilities before a word is drawn. *Perplexity*: e to the power of the mean negative log-probability.')
    nb.check_setup()
    nb.code('import numpy as np\nimport matplotlib.pyplot as plt\nnp.set_printoptions(suppress=True, precision=6)')

    nb.step(1, 'Surprise in bits', 'The surprise of an event with probability p is -log2(p) bits. Rare events are more surprising.')
    nb.code('events = np.array([1/2, 1/8, 1/1024])      # probabilities of three events\nprint(events)')
    nb.predict('How many bits of surprise do you expect for each event? Hint: 1/8 is one half three times over.')
    _todo(nb, solution, 'surprise in bits of each probability (see the slide "Surprise is the negative logarithm of the probability"). numpy has np.log2', 'surprise_bits = None  # your code here', 'surprise_bits = -np.log2(events)')
    nb.code('if surprise_bits is None:\n    print("NOT YET: write your code in the cell above, then run both cells again.")\nelse:\n    check("surprise of 1/2, 1/8 and 1/1024 in bits", surprise_bits, [1, 3, 10], 0.0001)\n    print(surprise_bits)')
    nb.read('Each time the probability is cut in half, how many bits are added to the surprise?')

    nb.step(2, 'Entropy: the average surprise', 'The entropy of a distribution P is the sum of p times its surprise. It is the smallest possible average cost, in bits, of describing outcomes drawn from P.')
    nb.code('P = np.array([0.5, 0.25, 0.125, 0.125])     # true probabilities of four next words\nfair = np.array([0.5, 0.5])\nbiased = np.array([0.9, 0.1])')
    nb.predict('Which has the larger entropy: the fair coin or the coin that lands heads 90 percent of the time?')
    _todo(nb, solution, 'entropy: the average surprise of the distribution (see the entropy slides). Write it once as a function so you can reuse it',
          'def entropy(p):\n    return None  # your code here',
          'def entropy(p):\n    return -np.sum(p * np.log2(p))')
    nb.code('H_P, H_fair, H_biased = entropy(P), entropy(fair), entropy(biased)\n'
            'if H_P is None:\n    print("NOT YET: write your code in the cell above, then run both cells again.")\nelse:\n'
            '    check("entropy of the four-word distribution P (bits)", H_P, 1.75, 0.0001)\n'
            '    check("entropy of the fair coin (bits)", H_fair, 1.0, 0.0001)\n'
            '    check("entropy of the 0.9 / 0.1 coin (bits)", H_biased, 0.469, 0.001)\n'
            '    print("entropy of P:", H_P, " fair coin:", H_fair, " biased coin:", round(float(H_biased), 4))')
    nb.change('Change `biased` to np.array([0.99, 0.01]) and recompute. Does the entropy go up or down? Why does a nearly certain outcome carry little surprise? Put 0.9 and 0.1 back afterwards.')

    nb.step(3, 'Cross-entropy and KL divergence', 'Reality follows P. Model A believes all four words are equally likely. Model B believes Q_B. Both are in bits. The formulas are on the slides.')
    nb.code('Q_A = np.array([0.25, 0.25, 0.25, 0.25])     # model A: uniform\nQ_B = np.array([0.4, 0.3, 0.2, 0.1])         # model B')
    nb.predict('Model B is closer to P than model A is. Will its cross-entropy be larger or smaller than model A\'s?')
    _todo(nb, solution, 'cross_entropy(P, Q) and kl(P, Q), both in bits (see the cross-entropy and KL slides)',
          'def cross_entropy(P, Q):\n    return None  # your code here\n\ndef kl(P, Q):\n    return None  # your code here',
          'def cross_entropy(P, Q):\n    return -np.sum(P * np.log2(Q))\n\ndef kl(P, Q):\n    return np.sum(P * np.log2(P / Q))')
    nb.code('ce_A, ce_B = cross_entropy(P, Q_A), cross_entropy(P, Q_B)\nkl_A, kl_B = kl(P, Q_A), kl(P, Q_B)\n'
            'if ce_A is None or kl_A is None or H_P is None:\n    print("NOT YET: write your code in the cell above, then run both cells again.")\nelse:\n'
            '    check("cross-entropy of model A", ce_A, 2.0, 0.0001)\n    check("cross-entropy of model B", ce_B, 1.8007, 0.0001)\n'
            '    check("KL divergence of model A", kl_A, 0.25, 0.0001)\n    check("KL divergence of model B", kl_B, 0.0507, 0.0001)\n'
            '    check("cross-entropy = entropy + KL (model B)", ce_B, H_P + kl_B, 0.000001)\n'
            '    print("cross-entropy A:", round(float(ce_A), 4), " B:", round(float(ce_B), 4), "bits")\n    print("KL A:", round(float(kl_A), 4), " B:", round(float(kl_B), 4), "bits")')
    nb.read('Cross-entropy is never below the entropy. By how much is model A above it? That gap is the KL divergence.')

    nb.step(4, 'Softmax (Session 12): scores to probabilities', 'A model produces one score (logit) per class: cat, dog and fox. The softmax of Session 12 turns them into probabilities that are positive and add to 1: p_i = exp(z_i) / sum(exp(z_j)). The stable form subtracts the largest logit first.')
    nb.code('classes = ["cat", "dog", "fox"]\nz = np.array([2.0, 1.0, 0.1])               # logits of a 3-class model\nz_big = np.array([1000.0, 1001.0, 1002.0])   # large logits')
    nb.predict('Which class gets the largest probability? Will the probabilities add to 1?')
    _todo(nb, solution, 'A softmax that does not overflow for logits like 1000 (the stable form from Session 12)',
          'def softmax(z):\n    return None  # your code here',
          'def softmax(z):\n    e = np.exp(z - np.max(z))\n    return e / e.sum()')
    nb.code('probs = softmax(z)\n'
            'if probs is None:\n    print("NOT YET: write your code in the cell above, then run both cells again.")\nelse:\n'
            '    check("softmax of [2, 1, 0.1]", probs, [0.6590, 0.2424, 0.0986], 0.0005)\n'
            '    check("softmax of the large logits", softmax(z_big), [0.0900, 0.2447, 0.6652], 0.0005)\n'
            '    print("softmax of z:", np.round(probs, 4), " sum:", round(float(probs.sum()), 6))\n'
            '    print("softmax of the large logits:", np.round(softmax(z_big), 4))\n'
            '    with np.errstate(all="ignore"):\n        print("the naive way gives:", np.exp(z_big) / np.exp(z_big).sum())')
    nb.read('The naive way prints nan. Why does subtracting the largest logit fix it without changing the answer?')

    nb.step(5, 'Temperature and top-p (nucleus) sampling', 'Temperature T divides every logit before the softmax. Top-p keeps the most likely words until their running total first reaches p, then rescales the kept words so they add to 1. '
            'Five next words with illustrative logits, already sorted from most to least likely.')
    nb.code('words5 = ["tea", "coffee", "water", "milk", "soup"]\nlogits5 = np.array([3.0, 2.6, 1.9, 1.2, 0.4])   # illustrative, sorted from largest to smallest\ntop_p = 0.8')
    nb.predict('At T = 0.5, will the top class (cat) get more or less than 0.659? And how many of the five drinks will top-p = 0.8 keep?')
    _todo(nb, solution, 'p_T: the softmax of z at T = 0.5, 1 and 2 (one row each). p5: the softmax of logits5 at T = 1. Then keep the most likely words until their running total first reaches top_p (np.cumsum gives running totals), and rescale the kept ones so they add to 1',
          'p_T = None  # your code here\np5 = None  # your code here\np_nucleus = None  # your code here: the rescaled probabilities of the kept words',
          'p_T = np.array([softmax(z / T) for T in (0.5, 1.0, 2.0)])\np5 = softmax(logits5)\nn_keep = int(np.searchsorted(np.cumsum(p5), top_p) + 1)\np_nucleus = p5[:n_keep] / p5[:n_keep].sum()')
    nb.code('if p_T is None or p5 is None or p_nucleus is None:\n    print("NOT YET: write your code in the cell above, then run both cells again.")\nelse:\n'
            '    check("top class (cat) at T = 0.5, 1 and 2", p_T[:, 0], [0.8638, 0.6590, 0.5017], 0.0005)\n'
            '    check("number of drinks top-p 0.8 keeps", len(p_nucleus), 3, 0)\n'
            '    check("rescaled probabilities of the kept drinks", p_nucleus, [0.4992, 0.3346, 0.1662], 0.0005)\n'
            '    print("cat, dog, fox at T = 0.5, 1, 2:\\n", np.round(p_T, 4))\n'
            '    print("drinks at T = 1:", np.round(p5, 4), " running total:", np.round(np.cumsum(p5), 4))\n'
            '    print("kept and rescaled:", dict(zip(words5, np.round(p_nucleus, 4))))')
    nb.read('A low temperature sharpens the probabilities and a high one flattens them. After the top-p cut, can milk or soup ever be drawn?')
    nb.change('Apply top-p to the drinks at T = 2 instead: `softmax(logits5 / 2)`. How many drinks does top-p = 0.8 keep now, and why?')

    nb.step(6, 'The gradient of softmax with cross-entropy is prediction minus target', 'Dog is the true word, so the one-hot target is y = (0, 1, 0). The loss is L = -sum(y * ln p), in nats. Work out the gradient of L with respect to the logits (the derivation slide shows it) and check it against a numeric gradient.')
    nb.code('y = np.array([0.0, 1.0, 0.0])               # dog is the true word (one-hot target)\n\ndef loss(z):\n    return -np.sum(y * np.log(softmax(z)))')
    nb.predict('Dog is true, but it only got probability 0.24. Will the gradient for the dog logit be positive or negative? (Should that logit go up or down?)')
    _todo(nb, solution, 'the gradient of the loss with respect to the logits, from the derivation slide', 'grad = None  # your code here', 'grad = probs - y')
    nb.code('if grad is None or probs is None:\n    print("NOT YET: write your code in the cell above, then run both cells again.")\nelse:\n'
            '    L0 = loss(z)\n    numeric = np.zeros(3)\n'
            '    for j in range(3):                        # nudge one logit at a time and watch the loss\n'
            '        zz = z.copy(); zz[j] += 1e-6\n        numeric[j] = (loss(zz) - L0) / 1e-6\n'
            '    lse_form = np.log(np.sum(np.exp(z))) - z[1]   # log-softmax: log-sum-exp (Session 12) minus the true logit\n'
            '    zs = np.array([0.5, 0.0])                 # two classes: the softmax of (z1, z2) is the sigmoid of z1 - z2\n'
            '    check("loss (cross-entropy, nats)", L0, 1.4170, 0.001)\n'
            '    check("gradient p - y", grad, [0.6590, -0.7576, 0.0986], 0.0005)\n'
            '    check("formula matches the numeric gradient (largest difference)", np.max(np.abs(grad - numeric)), 0.0, 0.00001)\n'
            '    check("log-sum-exp form gives the same loss", lse_form, L0, 0.000001)\n'
            '    check("two-class softmax equals the sigmoid of z1 - z2", softmax(zs)[0], 1 / (1 + np.exp(-(zs[0] - zs[1]))), 0.000001)\n'
            '    print("loss:", round(float(L0), 4), "nats   log-sum-exp form:", round(float(lse_form), 4))\n'
            '    print("formula p - y:", np.round(grad, 4))\n    print("numeric gradient:", np.round(numeric, 4))')
    nb.read('The three gradient entries add up to 0. Why must they, when p and y each add to 1?')

    nb.step(7, 'Perplexity of a toy language model', 'A toy model gave these probabilities to the six real words of a sentence (illustrative, made-up numbers). The perplexity formula is on the slides.')
    nb.code('words = ["The", "cat", "sat", "on", "the", "mat"]\ntoken_probs = np.array([0.2, 0.1, 0.25, 0.5, 0.4, 0.05])   # probability the model gave to each real word')
    nb.predict('The probabilities are between 0.05 and 0.5. Guess the perplexity: between 1 and 20?')
    _todo(nb, solution, 'the mean negative natural log of the six probabilities, then the perplexity (see the perplexity slides)',
          'mean_nll = None  # your code here\nperplexity = None  # your code here',
          'mean_nll = np.mean(-np.log(token_probs))\nperplexity = np.exp(mean_nll)')
    nb.code('total_nll = float(np.sum(-np.log(token_probs)))\n'
            'if mean_nll is None or perplexity is None:\n    print("NOT YET: write your code in the cell above, then run both cells again.")\nelse:\n'
            '    check("sum of -ln p over the six words", total_nll, 9.9035, 0.0005)\n    check("mean negative log-probability (nats)", mean_nll, 1.6506, 0.0005)\n'
            '    check("perplexity", perplexity, 5.2100, 0.0005)\n'
            '    print("sum of -ln p:", round(total_nll, 3), " mean:", round(float(mean_nll), 4), "nats  perplexity:", round(float(perplexity), 3))\n'
            '    print("in bits:", round(float(np.mean(-np.log2(token_probs))), 4), " 2 ** bits:", round(float(2 ** np.mean(-np.log2(token_probs))), 3))')
    nb.read('Perplexity is the same whether we use bits or nats. It reads as the effective number of equally likely words the model chooses between. How many?')
    nb.change('Replace token_probs with a model that gives every word probability 1/50 (`np.full(6, 1/50)`). What is the perplexity? Then try all 1.0.')

    nb.md('---\n## Save your work\n\nRun every cell again from the top (Runtime, Restart and run all), check the last line says all checks pass, then save the notebook.')
    nb.code('show_checks()')
    return nb


def namespace():
    import matplotlib
    matplotlib.use('Agg')
    nb = build(True)
    import warnings
    warnings.filterwarnings('ignore')
    ns = {'__name__': 's17_ns'}
    for c in nb.cells:
        if c['cell_type'] == 'code':
            with contextlib.redirect_stdout(io.StringIO()):
                exec(''.join(c['source']), ns)
    import matplotlib.pyplot as plt
    plt.close('all')
    return ns
