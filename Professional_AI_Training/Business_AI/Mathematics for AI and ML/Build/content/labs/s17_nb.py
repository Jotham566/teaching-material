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
    nb.md('# Session 17 lab: entropy, cross-entropy, softmax and perplexity\n\nKLAi | Mathematics for AI and Machine Learning\n\n'
          'Today you measure surprise in bits, compute entropy, cross-entropy and Kullback-Leibler (KL) divergence, build the softmax, check by numbers that its gradient with cross-entropy is prediction minus target, '
          'and score a toy language model with perplexity.\n\n'
          '**How to use this notebook.** Run the cells in order with Shift and Enter. Each step has the same rhythm: **PREDICT**, **RUN**, **READ**, then **CHANGE one thing**. Type your answers in the lines that start with `>`. '
          'If a number differs from the slide called "Check your numbers", stop and find the step that went wrong.\n\n'
          '**Words.** *Surprise* (self-information): -log2 of the probability of an event, in bits. *Entropy*: the average surprise. *Cross-entropy*: the average surprise when reality follows P but the model believes Q. '
          '*KL divergence*: cross-entropy minus entropy. *Softmax*: turns scores (logits) into probabilities. *Perplexity*: e to the power of the mean negative log-probability.')
    nb.check_setup()
    nb.code('import numpy as np\nimport matplotlib.pyplot as plt\nnp.set_printoptions(suppress=True, precision=6)')

    nb.step(1, 'Surprise in bits', 'The surprise of an event with probability p is -log2(p) bits. Rare events are more surprising.')
    nb.code('events = np.array([1/2, 1/8, 1/1024])      # probabilities of three events\nprint(events)')
    nb.predict('How many bits of surprise do you expect for each event? Hint: 1/8 is one half three times over.')
    _todo(nb, solution, 'surprise in bits of each probability (see the slide "Surprise is the negative logarithm of the probability"). numpy has np.log2', 'surprise_bits = None  # your code here', 'surprise_bits = -np.log2(events)')
    nb.code('print(surprise_bits)\ncheck("surprise of 1/2, 1/8 and 1/1024 in bits", surprise_bits, [1, 3, 10], 0.0001)')
    nb.read('Each time the probability is cut in half, how many bits are added to the surprise?')

    nb.step(2, 'Entropy: the average surprise', 'The entropy of a distribution P is the sum of p times its surprise. It is the smallest possible average cost of describing outcomes drawn from P.')
    nb.code('P = np.array([0.5, 0.25, 0.125, 0.125])     # true probabilities of four next words\nfair = np.array([0.5, 0.5])\nbiased = np.array([0.9, 0.1])')
    nb.predict('Which has the larger entropy: the fair coin or the coin that lands heads 90 percent of the time?')
    _todo(nb, solution, 'entropy: the average surprise of the distribution (see the entropy slides). Write it once as a function so you can reuse it',
          'def entropy(p):\n    return None  # your code here',
          'def entropy(p):\n    return -np.sum(p * np.log2(p))')
    nb.code('H_P, H_fair, H_biased = entropy(P), entropy(fair), entropy(biased)\nprint("entropy of P:", H_P, " fair coin:", H_fair, " biased coin:", round(float(H_biased), 4))\n'
            'check("entropy of the four-word distribution P (bits)", H_P, 1.75, 0.0001)\n'
            'check("entropy of the fair coin (bits)", H_fair, 1.0, 0.0001)\n'
            'check("entropy of the 0.9 / 0.1 coin (bits)", H_biased, 0.469, 0.001)')
    nb.change('Change `biased` to np.array([0.99, 0.01]) and recompute. Does the entropy go up or down? Why does a nearly certain outcome carry little surprise?')

    nb.step(3, 'Cross-entropy and KL divergence', 'Reality follows P. Model A believes all four words are equally likely. Model B believes Q_B. Both are in bits. The formulas are on the slides.')
    nb.code('Q_A = np.array([0.25, 0.25, 0.25, 0.25])     # model A: uniform\nQ_B = np.array([0.4, 0.3, 0.2, 0.1])         # model B')
    nb.predict('Model B is closer to P than model A is. Will its cross-entropy be larger or smaller than model A\'s?')
    _todo(nb, solution, 'cross_entropy(P, Q) and kl(P, Q), both in bits (see the cross-entropy and KL slides)',
          'def cross_entropy(P, Q):\n    return None  # your code here\n\ndef kl(P, Q):\n    return None  # your code here',
          'def cross_entropy(P, Q):\n    return -np.sum(P * np.log2(Q))\n\ndef kl(P, Q):\n    return np.sum(P * np.log2(P / Q))')
    nb.code('ce_A, ce_B = cross_entropy(P, Q_A), cross_entropy(P, Q_B)\nkl_A, kl_B = kl(P, Q_A), kl(P, Q_B)\n'
            'print("cross-entropy A:", round(float(ce_A), 4), " B:", round(float(ce_B), 4))\nprint("KL A:", round(float(kl_A), 4), " B:", round(float(kl_B), 4))\n'
            'print("cross-entropy minus entropy:", round(float(ce_A - H_P), 4), round(float(ce_B - H_P), 4))\n'
            'check("cross-entropy of model A", ce_A, 2.0, 0.0001)\ncheck("cross-entropy of model B", ce_B, 1.8006, 0.0005)\n'
            'check("KL divergence of model A", kl_A, 0.25, 0.0001)\ncheck("KL divergence of model B", kl_B, 0.0506, 0.0005)\n'
            'check("cross-entropy = entropy + KL (model B)", ce_B, H_P + kl_B, 0.000001)')
    nb.read('Cross-entropy is never below the entropy. By how much is model A above it? That gap is the KL divergence.')

    nb.step(4, 'Softmax: scores to probabilities', 'A model produces one score (logit) per class. The softmax turns scores into probabilities that are positive and add to 1: p_i = exp(z_i) / sum(exp(z_j)).')
    nb.code('z = np.array([2.0, 1.0, 0.1])               # logits of a 3-class model\nz_big = np.array([1000.0, 1001.0, 1002.0])   # large logits')
    nb.predict('Which class gets the largest probability? Will the probabilities add to 1?')
    _todo(nb, solution, 'A softmax that does not overflow for logits like 1000 (see the slide "Subtract the largest logit first")',
          'def softmax(z):\n    return None  # your code here',
          'def softmax(z):\n    e = np.exp(z - np.max(z))\n    return e / e.sum()')
    nb.code('probs = softmax(z)\nprint("softmax of z:", np.round(probs, 4), " sum:", round(float(probs.sum()), 6))\n'
            'print("softmax of the large logits:", np.round(softmax(z_big), 4))\n'
            'print("the naive way gives:", np.exp(z_big) / np.exp(z_big).sum())\n'
            'check("softmax of [2, 1, 0.1]", probs, [0.6590, 0.2424, 0.0986], 0.0005)\n'
            'check("softmax of the large logits", softmax(z_big), [0.0900, 0.2447, 0.6652], 0.0005)')
    nb.read('The naive way prints nan. Why does subtracting the largest logit fix it without changing the answer?')
    nb.change('Divide the logits by a temperature T = 0.5 and then by T = 2 before the softmax: `softmax(z / 0.5)` and `softmax(z / 2)`. Which T makes the model more sure of the top class?')

    nb.step(5, 'The gradient of softmax with cross-entropy is prediction minus target', 'For a true class with one-hot target y, the loss is L = -sum(y * ln p). Work out the gradient of L with respect to the logits (the derivation slide shows it) and check it against a numeric gradient.')
    nb.code('y = np.array([0.0, 1.0, 0.0])               # the true class is the second one (one-hot target)\n\ndef loss(z):\n    return -np.sum(y * np.log(softmax(z)))')
    nb.predict('The second class is true, but it only got probability 0.24. Will the gradient for the second logit be positive or negative? (Think: should that logit go up or down?)')
    _todo(nb, solution, 'the gradient of the loss with respect to the logits, from the derivation slide', 'grad = None  # your code here', 'grad = probs - y')
    nb.code('L0 = loss(z)\nnumeric = np.zeros(3)\nfor j in range(3):                        # nudge one logit at a time and watch the loss\n'
            '    zz = z.copy(); zz[j] += 1e-6\n    numeric[j] = (loss(zz) - L0) / 1e-6\n'
            'print("loss:", round(float(L0), 4))\nprint("formula p - y:", np.round(grad, 4))\nprint("numeric gradient:", np.round(numeric, 4))\n'
            'check("loss (cross-entropy, natural log)", L0, 1.4170, 0.001)\ncheck("gradient p - y", grad, [0.6590, -0.7576, 0.0986], 0.0005)\n'
            'check("formula matches the numeric gradient (largest difference)", np.max(np.abs(grad - numeric)), 0.0, 0.00001)')
    nb.read('The three gradient entries add up to 0. Why must they, when p and y each add to 1?')

    nb.step(6, 'Perplexity of a toy language model', 'A toy model gave these probabilities to the six real words of a sentence (illustrative, made-up numbers). The perplexity formula is on the slides.')
    nb.code('words = ["The", "cat", "sat", "on", "the", "mat"]\ntoken_probs = np.array([0.2, 0.1, 0.25, 0.5, 0.4, 0.05])   # probability the model gave to each real word')
    nb.predict('The probabilities are between 0.05 and 0.5. Guess the perplexity: between 1 and 20?')
    _todo(nb, solution, 'the mean negative natural log of the six probabilities, then the perplexity (see the perplexity slides)',
          'mean_nll = None  # your code here\nperplexity = None  # your code here',
          'mean_nll = np.mean(-np.log(token_probs))\nperplexity = np.exp(mean_nll)')
    nb.code('total_nll = float(np.sum(-np.log(token_probs)))\nprint("sum of -ln p:", round(total_nll, 3), " mean:", round(float(mean_nll), 4), " perplexity:", round(float(perplexity), 3))\n'
            'print("in bits:", round(float(np.mean(-np.log2(token_probs))), 4), " 2 ** bits:", round(float(2 ** np.mean(-np.log2(token_probs))), 3))\n'
            'check("sum of -ln p over the six words", total_nll, 9.9035, 0.0005)\ncheck("mean negative log-probability (nats)", mean_nll, 1.6506, 0.0005)\n'
            'check("perplexity", perplexity, 5.2100, 0.0005)')
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
