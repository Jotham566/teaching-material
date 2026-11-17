"""Session 12 Python lab: overflow, softmax and its stable form, log-sum-exp, number formats, ridge with a validation split and a test set, weight decay, a constraint, clipping. Author D."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'kit'))
import nb as NB  # noqa: E402
import diagrams_math_d as D  # noqa: E402

TITLE = 'Optimisation in practice'


def todo(b, solution, hint, learner, model):
    """A cell the learner completes: the learner version holds `learner`, the solution version holds `model`."""
    b.code(('# Hint: ' + hint + '\n' if hint else '') + (model if solution else learner))


def build(solution: bool):
    d = D.n12()
    R = {r['lam']: r for r in d['rows']}
    ytr = [float(v) for v in d['ytr']]
    yva = [float(v) for v in d['yte']]
    yts = [float(v) for v in d['yts']]
    r0, r3, r5 = R[0.0], R[0.1], R[10.0]
    b = NB.Notebook()
    b.md('# Session 12: Optimisation in practice\n\n**KLAi | Mathematics for AI and Machine Learning**\n\n'
         'In this lab you break a softmax on purpose and fix it by subtracting the maximum, compute a log-sum-exp, meet the limits of 16-bit numbers, '
         'and fit a degree 9 curve to 10 points with a ridge (L2) penalty: you choose lambda on validation points and report the error on test points once. '
         'The same numbers are in the spreadsheet lab. The curve data are illustrative (made-up noisy points from a smooth curve).\n\n'
         'The five steps match the lab map on the slides. Each step has the same rhythm: **PREDICT**, run, **READ**, then **CHANGE one thing**. A cell that says `None  # your code here` is yours to fill. '
         'The check cells say OK or NOT YET. Step 1 prints a RuntimeWarning and nan on purpose.')
    b.check_setup()

    b.step(1, 'Break the naive softmax on purpose', 'softmax(z)_i = exp(z_i) / sum of exp(z_j). The scores (logits) are 1000, 1001 and 1002. A float64 number cannot be larger than about 1.8e308, and exp(710) already exceeds that.')
    b.predict('What will the naive softmax of (1000, 1001, 1002) print? Numbers, zeros, inf or nan?')
    b.code('import numpy as np\nimport matplotlib.pyplot as plt\n\n'
           'z = np.array([1000.0, 1001.0, 1002.0])\nnaive = np.exp(z) / np.exp(z).sum()      # exp overflows to inf, then inf / inf\nprint(np.exp(z), naive)\n'
           'check("the naive softmax is nan, as expected", float(np.isnan(naive).all()), 1, 0)')
    b.read('What is exp(1000) here, and why is the answer nan? (Read the warning too.)')
    b.change('Type a power of your own into the cell below, for example 709 and then 710. Where does float64 give up?')
    b.code(('power = 710.0   # try 709 and 710\n' if solution else 'power = None   # type a number here, for example 709, then 710\n') +
           'if power is None:\n    print("Type a number for power first.")\nelse:\n    print(np.exp(power))')

    b.step(2, 'Fix it: subtract the maximum, then log-sum-exp', 'Subtracting the same constant c from every score does not change the softmax, because e^(-c) cancels. Choose c = the maximum so that every exponent is at most 0. '
           'Log-sum-exp is m + ln(sum of e^(z - m)), and the log of each probability is z - LSE. For small scores such as (2, 1, 0.1) the naive way is fine.')
    b.predict('What will the stable softmax of (1000, 1001, 1002) be? (The slides say it equals softmax(0, 1, 2).)')
    todo(b, solution, 'one line per idea; the slide "Read the stable softmax before you write it" shows the pattern',
         'm = None         # your code here: the largest score\n'
         'e = None         # your code here: the exponentials of the shifted scores\n'
         'stable = None    # your code here: each exponential divided by their total\n'
         'lse = None       # your code here: the log-sum-exp\n'
         'logprobs = None  # your code here: the log of each probability, without forming the probability\n'
         'small = None     # your code here: the naive softmax of [2.0, 1.0, 0.1]',
         'm = z.max()\n'
         'e = np.exp(z - m)                        # every exponent is at most 0, so e is between 0 and 1\n'
         'stable = e / e.sum()\n'
         'lse = m + np.log(e.sum())                # log-sum-exp\n'
         'logprobs = z - lse                       # the log of each probability\n'
         'small = np.exp(np.array([2.0, 1.0, 0.1]))\n'
         'small = small / small.sum()')
    b.code(f'check("stable softmax of (1000, 1001, 1002)", stable, {list(map(float, d["soft_big"]))}, 0.0001)\n'
           f'check("log-sum-exp", lse, {d["lse_big"]}, 0.0001)\n'
           'check("log-probabilities equal the log of the stable softmax", logprobs, None if stable is None else np.log(stable), 0.0001)\n'
           f'check("softmax(2, 1, 0.1) with the naive way", small, {list(map(float, d["soft_small"]))}, 0.0001)\n'
           'if stable is not None and small is not None:\n    print(np.round(stable, 4), np.round(small, 4))')
    b.read('The stable result is the same as softmax(0, 1, 2). Why do only the differences between scores matter?')
    b.change('Type a shift of your own into the cell below, for example 5000, so the scores become 6000, 6001, 6002. Predict first whether the stable softmax changes.')
    b.code(('shift = 5000.0\n' if solution else 'shift = None   # type a number here, for example 5000\n') +
           'if shift is None:\n    print("Type a number for shift first.")\nelse:\n    z2 = z + shift\n    e2 = np.exp(z2 - z2.max())\n    print(np.round(e2 / e2.sum(), 4))')

    b.step(3, 'Number formats and a long product', 'float16 stores a number in 16 bits: its largest value is 65504. A product of many probabilities falls below the smallest float64 number (about 5e-324) and becomes exactly 0 from n = 324 tokens on. A sum of logs does not.')
    b.predict('What is exp(12) in float16? What is the product 0.1 to the power 400 in float64, and the sum of 400 copies of ln(0.1)?')
    todo(b, solution, 'np.finfo describes a number format. Wrap single numbers in np.float16(...) to compute in float16.',
         'f16_max = None    # your code here: the largest float16 number\n'
         'e12 = None        # your code here: the exponential of 12 in float16 (put it inside "with np.errstate(over=\\"ignore\\"):" to hide the warning)\n'
         'lost = None       # your code here: 1 plus 0.0004, both as float16\n'
         'prod400 = None    # your code here: the product of 400 probabilities of 0.1\n'
         'sumlog400 = None  # your code here: the sum of the logs of 400 probabilities of 0.1',
         'f16_max = float(np.finfo(np.float16).max)\n'
         'with np.errstate(over="ignore"):\n'
         '    e12 = np.exp(np.float16(12))          # in float16 this is above the largest number\n'
         'lost = np.float16(1) + np.float16(0.0004) # a small update added to 1 in float16\n'
         'prod400 = 0.1 ** 400                       # the product of 400 probabilities of 0.1\n'
         'sumlog400 = 400 * np.log(0.1)              # the sum of their logs')
    b.code('check("largest float16 number", f16_max, 65504, 0)\n'
           'check("exp(12) in float16 is inf", None if e12 is None else float(np.isinf(e12)), 1, 0)\n'
           'check("1 + 0.0004 in float16 is still 1", None if lost is None else float(lost), 1, 0)\n'
           'check("the product of 400 probabilities of 0.1 is 0", prod400, 0, 0)\n'
           'check("the sum of 400 logs of 0.1", sumlog400, -921.034, 0.001)\n'
           'if sumlog400 is not None:\n    print(f16_max, e12, lost, prod400, round(sumlog400, 3))')
    b.read('Why is the update of 0.0004 lost? How many significant digits does float16 keep?')
    b.change('Type a number of tokens into the cell below, for example 300 or 330. Is the product still above zero? Is the sum of logs still an ordinary number?')
    b.code(('tokens = 330\n' if solution else 'tokens = None   # type a number of tokens here, for example 300 or 330\n') +
           'if tokens is None:\n    print("Type a number for tokens first.")\nelse:\n    print(0.1 ** tokens, round(tokens * np.log(0.1), 3))')

    b.step(4, 'Ridge regression: fit, choose lambda on validation points, then test once', 'Ten training points, a degree 9 polynomial: columns 1, x, x^2, ..., x^9. The ridge answer is w = (X^T X + lambda P)^-1 X^T y, with P the identity matrix whose first entry is 0, so the intercept is not penalised. '
           'Twenty validation points choose lambda. Twenty test points stay untouched until lambda is chosen, then give one honest error.')
    b.predict('Without a penalty the curve passes through every point. Will its weights be small or enormous? Which of the six lambdas will give the lowest validation error?')
    b.code(f'xtr = np.linspace(-1, 1, 10)\nytr = np.array({ytr})\n'
           f'xva = np.linspace(-0.97, 0.97, 20)      # validation points: used to choose lambda\nyva = np.array({yva})\n'
           f'xts = np.linspace(-0.95, 0.95, 20)      # test points: used once, at the very end\nyts = np.array({yts})\n'
           'Xtr = np.vander(xtr, 10, increasing=True)     # columns 1, x, ..., x^9\nXva = np.vander(xva, 10, increasing=True)\nXts = np.vander(xts, 10, increasing=True)\n'
           'P = np.eye(10)\nP[0, 0] = 0.0                                 # do not penalise the intercept\n'
           'print(Xtr.shape, Xva.shape, Xts.shape)')
    todo(b, solution, 'the closed form is on the slide "Ridge has a closed-form answer"; np.linalg.solve is better than an explicit inverse. RMSE is the root of the mean squared error. The intercept is not in the sum of squared weights.',
         'def ridge(X, y, lam):\n'
         '    if lam == 0:\n        return np.linalg.lstsq(X, y, rcond=None)[0]   # X^T X is badly conditioned at lambda = 0: use a least squares solver\n'
         '    return None  # your code here: the ridge weights for lam > 0\n'
         'def rmse(X, w, y):\n    return None  # your code here: the root of the mean squared error of the predictions X w\n'
         'w0, w1, w10 = ridge(Xtr, ytr, 0.0), ridge(Xtr, ytr, 0.1), ridge(Xtr, ytr, 10.0)\n'
         'norm0 = norm1 = norm10 = None  # your code here: the sum of squared weights without the intercept, for each of the three',
         'def ridge(X, y, lam):\n'
         '    if lam == 0:\n        return np.linalg.lstsq(X, y, rcond=None)[0]   # X^T X is badly conditioned at lambda = 0: use a least squares solver\n'
         '    return np.linalg.solve(X.T @ X + lam * P, X.T @ y)\n'
         'def rmse(X, w, y):\n    return float(np.sqrt(np.mean((X @ w - y) ** 2)))\n'
         'w0, w1, w10 = ridge(Xtr, ytr, 0.0), ridge(Xtr, ytr, 0.1), ridge(Xtr, ytr, 10.0)\n'
         'norm0, norm1, norm10 = w0[1:] @ w0[1:], w1[1:] @ w1[1:], w10[1:] @ w10[1:]   # sum of squared weights without the intercept')
    b.code('ok = w1 is not None and rmse(Xtr, w0, ytr) is not None\n'
           f'check("sum of squared weights, lambda = 0.1", norm1, {r3["norm2"]}, 0.0001)\n'
           f'check("sum of squared weights, lambda = 10", norm10, {r5["norm2"]}, 0.0001)\n'
           'check("the unpenalised weights are enormous", None if norm0 is None else float(norm0 > 10000), 1, 0)\n'
           f'check("training error, lambda = 0.1", rmse(Xtr, w1, ytr) if ok else None, {r3["rmse_tr"]}, 0.0001)\n'
           f'check("validation error, lambda = 0", rmse(Xva, w0, yva) if ok else None, {r0["rmse_te"]}, 0.001)\n'
           f'check("validation error, lambda = 0.1", rmse(Xva, w1, yva) if ok else None, {r3["rmse_te"]}, 0.0001)\n'
           'if ok:\n    for lam in [0.0, 0.001, 0.01, 0.1, 1.0, 10.0]:\n        w = ridge(Xtr, ytr, lam)\n        print("lambda", lam, " training", round(rmse(Xtr, w, ytr), 4), " validation", round(rmse(Xva, w, yva), 4))')
    b.read('The unpenalised training error is almost 0 but its validation error is the largest. What do we call that? Which lambda gives the lowest validation error?')
    todo(b, solution, 'use the lambda you chose from the validation errors above, fit on the training points, and compute the RMSE on the test points; do this once',
         'lam_chosen = None  # your code here: the lambda with the lowest validation error\ntest_rmse = None   # your code here: the test error at that lambda',
         'lam_chosen = 0.1\ntest_rmse = rmse(Xts, ridge(Xtr, ytr, lam_chosen), yts)')
    b.code(f'check("chosen lambda", lam_chosen, {d["lam_best"]}, 1e-9)\ncheck("test error at the chosen lambda", test_rmse, {d["rmse_test"]}, 0.0001)\n'
           'if test_rmse is not None:\n    print("test error, reported once:", round(test_rmse, 4))')
    b.read('Is the test error higher or lower than the validation error at the same lambda? Why is that usual?')
    b.code('xg = np.linspace(-1, 1, 200)\n'
           'if w1 is None:\n    print("Fill in the ridge answer cell above first.")\nelse:\n'
           '    plt.figure(figsize=(6, 3))\n    plt.scatter(xtr, ytr, color="black", zorder=3)\n'
           '    plt.plot(xg, np.sin(1.5 * xg) + 0.4 * xg ** 2, "k--", label="true curve")\n'
           '    plt.plot(xg, np.vander(xg, 10, increasing=True) @ w1, color="#AE2525", label="ridge, lambda = 0.1")\n'
           '    plt.legend()\n    plt.show()')
    b.change('Type a lambda of your own into the cell below, for example 10, and compare its training and validation errors with lambda = 0.1.')
    b.code(('my_lam = 10.0\n' if solution else 'my_lam = None   # type a lambda here, for example 10\n') +
           'if my_lam is None or w1 is None:\n    print("Type a number for my_lam (and fill in the ridge cell) first.")\nelse:\n'
           '    w = ridge(Xtr, ytr, my_lam)\n    print("training", round(rmse(Xtr, w, ytr), 4), " validation", round(rmse(Xva, w, yva), 4))')

    b.step(5, 'Weight decay, a weight limit and clipping', 'Weight decay: w <- (1 - 2 eta lambda) w - eta dL/dw. A limit on the weights: the lowest loss w1^2 + w2^2 on the line w1 + w2 = 2. Clipping: g <- g c / (length of g) when the length exceeds c.')
    b.predict('One step with w = 2, eta = 0.1, lambda = 0.5 and gradient 1: bigger or smaller than 2? Where on the line is the loss lowest?')
    todo(b, solution, 'the weight-decay slide gives the update, and the weight-limit slide gives the loss. To clip, rescale the vector to length 5.',
         'eta, lam, g = 0.1, 0.5, 1.0\n'
         'w_new = None    # your code here: the new w after one decay step, starting from w = 2\n'
         'w1v = np.linspace(0, 2, 5)                           # points on the line w1 + w2 = 2\n'
         'loss = None     # your code here: the loss at each point of w1v\n'
         'best = None     # your code here: the w1 with the lowest loss\n'
         'gvec = np.array([30.0, 40.0])\n'
         'clipped = None  # your code here: gvec shortened to length 5, same direction',
         'eta, lam, g = 0.1, 0.5, 1.0\n'
         'w_new = (1 - 2 * eta * lam) * 2.0 - eta * g          # weight decay step for w = 2\n'
         'w1v = np.linspace(0, 2, 5)                           # points on the line w1 + w2 = 2\n'
         'loss = w1v ** 2 + (2 - w1v) ** 2\n'
         'best = w1v[np.argmin(loss)]\n'
         'gvec = np.array([30.0, 40.0])\n'
         'glen = np.sqrt((gvec ** 2).sum())\n'
         'clipped = gvec * (5.0 / glen) if glen > 5.0 else gvec  # limit c = 5')
    b.code('check("weight after one step with decay", w_new, 1.7, 0.0001)\n'
           'check("lowest loss on the line", None if loss is None else loss.min(), 2, 0.0001)\n'
           'check("best w1 on the line", best, 1, 0.0001)\n'
           'check("clipped gradient", clipped, [3, 4], 0.0001)\n'
           'if clipped is not None:\n    print(w_new, loss, best, clipped)')
    b.read('At the best point, the loss slope (2 w1, 2 w2) = (2, 2) is parallel to the line slope (1, 1). Why does that tell us it is the best point?')
    b.change('Type a stronger penalty into the cell below, for example lambda = 2, keeping the other numbers. Predict whether the new w is below or above 1.7.')
    b.code(('lam_try = 2.0\n' if solution else 'lam_try = None   # type a lambda here, for example 2\n') +
           'if lam_try is None:\n    print("Type a number for lam_try first.")\nelse:\n    print((1 - 2 * 0.1 * lam_try) * 2.0 - 0.1 * 1.0)')
    b.md('---\n## Finish\n\nRun the cell below. It should say **All checks pass**. Then restart the kernel, run all cells from the top, and save the notebook.')
    b.code('show_checks()')
    return b
