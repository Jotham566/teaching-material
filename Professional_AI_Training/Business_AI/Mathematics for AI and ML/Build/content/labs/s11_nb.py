"""Session 11 Python lab: backpropagation by hand on the tiny network, with a finite-difference check. Author D."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'kit'))
import numpy as np  # noqa: E402
import nb as NB  # noqa: E402
import diagrams_math_d as D  # noqa: E402

TITLE = 'Backpropagation by hand'


def todo(b, solution, hint, learner, model):
    """A cell the learner completes: the learner version holds `learner`, the solution version holds `model`."""
    b.code(('# Hint: ' + hint + '\n' if hint else '') + (model if solution else learner))


def run_eta(n, eta, steps):
    """Loss after every step of training the tiny network (same loop as the notebook)."""
    x, y = n['x'], n['y']
    W1, b1, W2, b2 = [n[k].copy() for k in ('W1', 'b1', 'W2', 'b2')]
    out = []
    for _ in range(steps + 1):
        a = 1 / (1 + np.exp(-(W1 @ x + b1)))
        yh = W2 @ a + b2
        out.append(float(0.5 * (yh[0] - y) ** 2))
        d2 = yh - y
        d1 = (W2.T @ d2).ravel() * a * (1 - a)
        W2, b2 = W2 - eta * np.outer(d2, a), b2 - eta * d2
        W1, b1 = W1 - eta * np.outer(d1, x), b1 - eta * d1
    return out


def build(solution):
    n = D.n11()
    s1, s2, s3 = n['s1'], n['s2'], n['s3']
    nW1, nb1, nW2, nb2 = n['new1']
    L50 = run_eta(n, 0.5, 50)
    L5 = run_eta(n, 5.0, 1)
    b = NB.Notebook()
    b.md('# Session 11: Backpropagation by hand\n\n**KLAi | Mathematics for AI and Machine Learning**\n\n'
         'In this lab you run the forward pass, the backward pass and the update on the tiny network from the slides (2 inputs, 2 hidden units with a sigmoid, 1 output, squared-error loss). '
         'Then you prove your nine gradients with finite differences, and you train the network for 50 steps. The same numbers are in the spreadsheet lab. '
         'The network and its numbers are illustrative (made-up numbers to show the arithmetic).\n\n'
         'Each step has the same rhythm: **PREDICT**, run, **READ**, then **CHANGE one thing**. A cell that says `None  # your code here` is yours to fill. The check cells say OK or NOT YET.')
    b.check_setup()

    b.step(1, 'The network and the forward pass', 'The inputs are x = (1, 2) and the target is y = 1. W1 is 2 × 2 (one row per hidden unit), W2 is 1 × 2. '
           'The forward pass is: z(1) = W(1) x + b(1), then a(1) = sigmoid(z(1)), then y-hat = W(2) a(1) + b(2), then L = 0.5 (y-hat - y)^2. '
           'The layer is written in brackets. In the code the same objects are called z1, a1, W1, b1, W2 and b2, and the deltas d1 and d2.')
    b.predict('Is the prediction y-hat going to be bigger or smaller than the target 1? Write your guess before you run.')
    b.code('import numpy as np\nimport matplotlib.pyplot as plt\n\n'
           'x = np.array([1.0, 2.0])               # the two inputs\ny = 1.0                                # the target\n'
           'W1 = np.array([[0.2, -0.3], [0.4, 0.1]])   # weights into the hidden units, one row per hidden unit\n'
           'b1 = np.array([0.1, -0.2])             # biases of the hidden units\n'
           'W2 = np.array([[0.5, -0.4]])           # weights into the output unit (1 × 2)\n'
           'b2 = np.array([0.2])                   # bias of the output unit\n'
           'eta = 0.5                              # the learning rate\n\n'
           'def sigmoid(z):\n    return 1 / (1 + np.exp(-z))')
    todo(b, solution, 'use the forward pass formulas in the step text; @ is matrix multiplication; the output unit gives a one-entry array, so take its entry to get a number',
         'z1 = None    # your code here: the two weighted sums of the hidden units\na1 = None    # your code here: the sigmoid of z1\nyhat = None  # your code here: the prediction, one number\nL = None     # your code here: 0.5 times (yhat - y) squared',
         'z1 = W1 @ x + b1\na1 = sigmoid(z1)\nyhat = (W2 @ a1 + b2)[0]\nL = 0.5 * (yhat - y) ** 2')
    b.code('print("z1 =", z1)\nprint("a1 =", a1)\nprint("y-hat =", yhat, " loss =", L)\n'
           'check("z1 (both hidden units)", z1, [%.4f, %.4f], 0.001)\ncheck("a1 (both hidden units)", a1, [%.4f, %.4f], 0.001)\n'
           'check("prediction y-hat", yhat, %.4f, 0.001)\ncheck("loss L", L, %.4f, 0.001)'
           % (s1['z1'][0], s1['z1'][1], s1['a1'][0], s1['a1'][1], s1['yh'], s1['L']))
    b.read('The prediction is far below the target. Which way must most of the parameters move to raise it?')

    b.step(2, 'The backward pass: deltas and the nine gradients', 'delta(2) = y-hat - y. Then delta(1) = (W(2) transposed times delta(2)) times a(1) times (1 - a(1)), entry by entry. '
           'The gradient of a weight matrix is the delta times the transposed values that enter it. The gradient of a bias is its delta.')
    b.predict('Will delta(2) be positive or negative? Will the gradients of W(2) have the same sign as delta(2)?')
    todo(b, solution, 'd2 has shape (1,) and d1 has shape (2,). Each weight gradient is a matrix with the same shape as its weights; np.outer builds a matrix from two vectors.',
         'd2 = None   # your code here: yhat - y, as an array with one entry\nd1 = None   # your code here: (W2.T @ d2) * a1 * (1 - a1), shape (2,)\n'
         'gW2 = None  # your code here: np.outer(d2, a1), shape (1, 2)\ngb2 = None  # your code here: the same as d2\n'
         'gW1 = None  # your code here: np.outer(d1, x), shape (2, 2)\ngb1 = None  # your code here: the same as d1',
         'd2 = np.array([yhat - y])\nd1 = (W2.T @ d2) * a1 * (1 - a1)\ngW2 = np.outer(d2, a1)\ngb2 = d2\ngW1 = np.outer(d1, x)\ngb1 = d1')
    b.code('print("delta2 =", d2, " delta1 =", d1)\nprint("gradient of W2:", gW2)\nprint("gradient of W1:", gW1)\n'
           'check("delta2", d2, %.4f, 0.001)\ncheck("delta1 (two values)", d1, [%.4f, %.4f], 0.001)\n'
           'check("gradient of W2", gW2, [[%.4f, %.4f]], 0.001)\ncheck("gradient of W1", gW1, [[%.4f, %.4f], [%.4f, %.4f]], 0.001)'
           % (s1['d2'], s1['d1'][0], s1['d1'][1], s1['gW2'][0][0], s1['gW2'][0][1], s1['gW1'][0][0], s1['gW1'][0][1], s1['gW1'][1][0], s1['gW1'][1][1]))
    b.read('Print the shape of each gradient with .shape. Is each gradient the same shape as its parameter?')

    b.step(3, 'Prove the gradients with finite differences', 'To trust the nine gradients, nudge each parameter by +h and -h (h = 0.00001), compute the loss both times, and divide the difference by 2h. '
           'The helper below packs the nine parameters into one list so a loop can nudge them one at a time. Fill in the answer cell of Step 2 first, because this step uses its gradients.')
    b.predict('How close do you expect the two answers to be: within 0.1, within 0.001, or within 0.0000001?')
    b.code('def loss_of(p):\n'
           '    """The loss for a list of the nine parameters: W1 (4 numbers), b1 (2), W2 (2), b2 (1)."""\n'
           '    W1_, b1_, W2_, b2_ = p[0:4].reshape(2, 2), p[4:6], p[6:8].reshape(1, 2), p[8:9]\n'
           '    a_ = sigmoid(W1_ @ x + b1_)\n'
           '    return 0.5 * ((W2_ @ a_ + b2_)[0] - y) ** 2\n\n'
           'p0 = np.concatenate([W1.ravel(), b1, W2.ravel(), b2])             # the nine parameters\n'
           'backprop = np.concatenate([gW1.ravel(), gb1, gW2.ravel(), gb2])   # the nine gradients from step 2\n'
           'h = 0.00001\nnumeric = np.zeros(9)\n'
           'for i in range(9):\n    up, down = p0.copy(), p0.copy()\n    up[i] += h\n    down[i] -= h\n    numeric[i] = (loss_of(up) - loss_of(down)) / (2 * h)\n'
           'print("finite differences:", np.round(numeric, 6))\nprint("backpropagation:   ", np.round(backprop, 6))')
    todo(b, solution, 'the largest absolute difference between the two lists of nine numbers', 'max_diff = None  # your code here',
         'max_diff = np.max(np.abs(numeric - backprop))')
    b.code('print("largest difference:", max_diff)\ncheck("finite differences agree with backpropagation (difference below 1e-7)", max_diff, 0.0, 1e-7)')
    b.change('Break one formula on purpose: in step 2 delete the factor a1 * (1 - a1) from d1, re-run steps 2 and 3, and see which entries of the check disagree. Then put the factor back and re-run.')

    b.step(4, 'The update', 'Every parameter moves by minus eta times its gradient. Then we run the forward pass again with the new parameters.')
    b.predict('Will the loss after one update be about the same, a little smaller, or much smaller than 0.3417?')
    todo(b, solution, 'apply the update rule to each of the four groups of parameters',
         'W1n = None  # your code here\nb1n = None   # your code here\nW2n = None   # your code here\nb2n = None   # your code here',
         'W1n = W1 - eta * gW1\nb1n = b1 - eta * gb1\nW2n = W2 - eta * gW2\nb2n = b2 - eta * gb2')
    b.code('yhat1 = (W2n @ sigmoid(W1n @ x + b1n) + b2n)[0]\nloss1 = 0.5 * (yhat1 - y) ** 2\n'
           'print("new W1 row 1:", W1n[0])\nprint("new prediction:", yhat1, " new loss:", loss1)\n'
           'check("new W1 row 1", W1n[0], [%.4f, %.4f], 0.001)\ncheck("new b2", b2n, %.4f, 0.001)\ncheck("loss after one update", loss1, %.4f, 0.0005)'
           % (nW1[0][0], nW1[0][1], nb2[0], s2['L']))
    b.change('Change eta to 0.1, re-run step 4 and read the new loss. Is a smaller learning rate better or worse here? Put eta back to 0.5 afterwards.')

    b.step(5, 'Repeat: 50 training steps', 'The function below is the whole training step (forward, backward, update) in a loop. Read it line by line before you run it: it is the code from the slides.')
    b.code('def train(eta, steps):\n'
           '    W1_, b1_, W2_, b2_ = W1.copy(), b1.copy(), W2.copy(), b2.copy()\n'
           '    losses = []\n'
           '    for step in range(steps + 1):\n'
           '        a_ = sigmoid(W1_ @ x + b1_)                 # forward pass\n'
           '        yh_ = W2_ @ a_ + b2_\n'
           '        losses.append(0.5 * (yh_[0] - y) ** 2)\n'
           '        d2_ = yh_ - y                               # backward pass\n'
           '        d1_ = (W2_.T @ d2_) * a_ * (1 - a_)\n'
           '        W2_, b2_ = W2_ - eta * np.outer(d2_, a_), b2_ - eta * d2_     # update\n'
           '        W1_, b1_ = W1_ - eta * np.outer(d1_, x), b1_ - eta * d1_\n'
           '    return losses\n\n'
           'losses = train(0.5, 50)\nprint("loss at steps 0, 1, 2, 3:", [round(float(l), 6) for l in losses[:4]])\n'
           'plt.plot(losses)\nplt.yscale("log")\nplt.xlabel("step")\nplt.ylabel("loss (log scale)")\nplt.title("Training the tiny network, eta = 0.5")\nplt.show()')
    b.predict('The log scale shows the loss falling by a roughly constant factor at each step. About what factor: 2, 10 or 50?')
    todo(b, solution, 'losses holds the loss at step 0, 1, 2 and so on; pick the entries you need', 'loss2 = None    # your code here: loss after two updates\nloss50 = None   # your code here: loss after 50 updates',
         'loss2 = losses[2]\nloss50 = losses[50]')
    b.code('print(loss2, loss50)\ncheck("loss after two updates", loss2, %.6f, 0.00002)\ncheck("loss after 50 updates is almost zero (below 1e-6)", loss50, 0.0, 1e-6)' % (s3['L'],))
    b.read('The prediction for these inputs is now very close to 1. Does this mean the network is good in general? (It has seen one example only.)')

    b.step(6, 'A learning rate that is too large', 'Run the same training with eta = 5. You know from Session 10 what to expect. The check records the loss after just one update.')
    b.predict('With eta = 5, will the loss after one update be smaller or larger than at the start (0.3417)?')
    todo(b, solution, 'train returns a list of losses; pick the entry after one update', 'loss_big = None  # your code here: the loss after one update with eta = 5',
         'loss_big = train(5.0, 1)[1]')
    b.code('print("loss at the start 0.3417, loss after one update with eta = 5:", loss_big)\ncheck("loss after one update with eta = 5", loss_big, %.4f, 0.01)' % L5[1])
    b.change('Call train(5.0, 5) and print the losses (train takes its own eta, so nothing needs undoing). How does the loss behave from step to step? Then call train(0.05, 50) and compare its last loss with the eta = 0.5 run.')
    b.md('---\n## Finish\n\nRun the cell below. It should say **All 15 checks pass**. Then restart the kernel, run all cells from the top, and save the notebook.')
    b.code('show_checks()')
    return b
