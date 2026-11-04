"""Session 12 Python lab: overflow, stable softmax, log-sum-exp, number formats, ridge closed form, weight decay, a constraint. Author D."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'kit'))
import nb as NB  # noqa: E402
import diagrams_math_d as D  # noqa: E402

TITLE = 'Session 12: Optimisation in practice'


def build(solution: bool):
    d = D.n12()
    R = {r['lam']: r for r in d['rows']}
    ytr = [float(v) for v in d['ytr']]
    yte = [float(v) for v in d['yte']]
    r0, r3, r5 = R[0.0], R[0.1], R[10.0]
    n = NB.Notebook()

    def todo(sol, learner):
        n.code(sol if solution else learner)

    n.md('# Session 12: Optimisation in practice (Python lab)\n\n'
         'You will break a softmax on purpose and fix it by subtracting the maximum, compute a log-sum-exp, meet the limits of 16-bit numbers, and fit a degree 9 curve to 10 points with a ridge (L2) penalty for several values of lambda.\n\n'
         '**How to work.** In each step: read the idea, write a PREDICT guess, run the cell, READ the output, then CHANGE one thing in the experiment cell. Cells with `None  # your code here` are yours to fill. '
         'The automatic checks print OK or NOT YET. Run the cells from the top, in order. Step 1 prints a RuntimeWarning and nan on purpose.')
    n.step(0, 'Set up', 'numpy for numbers, matplotlib for the picture.')
    n.code('import numpy as np\nimport matplotlib.pyplot as plt\n\nprint("ready")')
    n.check_setup()

    n.step(1, 'Break the naive softmax on purpose', 'softmax(z)_i = exp(z_i) / sum of exp(z_j). The scores (logits) are 1000, 1001 and 1002. A float64 number cannot be larger than about 1.8e308, and exp(710) already exceeds that.')
    n.predict('What will the naive softmax of (1000, 1001, 1002) print? Numbers, zeros, inf or nan?')
    n.code('z = np.array([1000.0, 1001.0, 1002.0])\nnaive = np.exp(z) / np.exp(z).sum()      # exp overflows to inf, then inf / inf\nprint(np.exp(z), naive)')
    n.read('What is exp(1000) here, and why is the answer nan? (Read the warning too.)')
    n.code('check("the naive softmax is nan, as expected", float(np.isnan(naive).all()), 1, 0)')
    n.change('Run the experiment cell: exp(709) and exp(710). Where does float64 give up?')
    n.code('print(np.exp(709.0), np.exp(710.0))')

    n.step(2, 'Fix it: subtract the maximum, then log-sum-exp', 'Subtracting the same constant c from every score does not change the softmax, because e^(-c) cancels. Choose c = the maximum so that every exponent is at most 0. Log-sum-exp is m + ln(sum of e^(z - m)).')
    n.predict('What will the stable softmax of (1000, 1001, 1002) be? (The slides say it equals softmax(0, 1, 2).)')
    todo('m = z.max()\n'
         'e = np.exp(z - m)                        # every exponent is at most 0, so e is between 0 and 1\n'
         'stable = e / e.sum()\n'
         'lse = m + np.log(e.sum())                # log-sum-exp\n'
         'logprobs = z - lse                       # the log of each probability\n'
         'small = np.exp(np.array([2.0, 1.0, 0.1]))\n'
         'small = small / small.sum()              # for small scores the naive way is fine\n'
         'print(np.round(stable, 4), round(lse, 4), np.round(logprobs, 4), np.round(small, 4))\n'
         f'check("stable softmax of (1000, 1001, 1002)", stable, {list(map(float, d["soft_big"]))}, 0.0001)\n'
         f'check("log-sum-exp", lse, {d["lse_big"]}, 0.0001)\n'
         'check("log-probabilities equal the log of the stable softmax", logprobs, np.log(stable), 0.0001)\n'
         f'check("softmax(2, 1, 0.1) with the naive way", small, {list(map(float, d["soft_small"]))}, 0.0001)',
         '# Hint: one line per idea. The slide "Read the stable softmax before you write it" shows the pattern.\n'
         'm = None  # your code here: the largest score\n'
         'e = None  # your code here: the exponentials of the shifted scores\n'
         'stable = None  # your code here: each exponential divided by their total\n'
         'lse = None  # your code here: the log-sum-exp\n'
         'logprobs = None  # your code here: the log of each probability, without forming the probability\n'
         'small = None  # your code here: the naive softmax of [2.0, 1.0, 0.1]\n'
         f'check("stable softmax of (1000, 1001, 1002)", stable, {list(map(float, d["soft_big"]))}, 0.0001)\n'
         f'check("log-sum-exp", lse, {d["lse_big"]}, 0.0001)\n'
         'check("log-probabilities equal the log of the stable softmax", logprobs, None if stable is None else np.log(stable), 0.0001)\n'
         f'check("softmax(2, 1, 0.1) with the naive way", small, {list(map(float, d["soft_small"]))}, 0.0001)')
    n.read('The stable result is the same as softmax(0, 1, 2). Why do only the differences between scores matter?')
    n.change('Run the experiment cell: shift the scores by 5000 instead. Predict first whether the stable softmax changes.')
    n.code('z2 = np.array([6000.0, 6001.0, 6002.0])\ne2 = np.exp(z2 - z2.max())\nprint(np.round(e2 / e2.sum(), 4))')

    n.step(3, 'Number formats and a long product', 'float16 stores a number in 16 bits: its largest value is 65504. A product of many probabilities falls below the smallest float64 number (about 5e-324) and becomes exactly 0 from n = 324 tokens on. A sum of logs does not.')
    n.predict('What is exp(12) in float16? What is the product 0.1 to the power 400 in float64, and the sum of 400 copies of ln(0.1)?')
    todo('f16_max = float(np.finfo(np.float16).max)\n'
         'with np.errstate(over="ignore"):\n'
         '    e12 = np.exp(np.float16(12))          # in float16 this is above the largest number\n'
         'lost = np.float16(1) + np.float16(0.0004) # a small update added to 1 in float16\n'
         'prod400 = 0.1 ** 400                       # the product of 400 probabilities of 0.1\n'
         'sumlog400 = 400 * np.log(0.1)              # the sum of their logs\n'
         'print(f16_max, e12, lost, prod400, round(sumlog400, 3))\n'
         'check("largest float16 number", f16_max, 65504, 0)\n'
         'check("exp(12) in float16 is inf", float(np.isinf(e12)), 1, 0)\n'
         'check("1 + 0.0004 in float16 is still 1", float(lost), 1, 0)\n'
         'check("the product of 400 probabilities of 0.1 is 0", prod400, 0, 0)\n'
         'check("the sum of 400 logs of 0.1", sumlog400, -921.034, 0.001)',
         '# Hint: np.finfo describes a number format. Wrap single numbers in np.float16(...) to compute in float16.\n'
         'f16_max = None  # your code here: the largest float16 number\n'
         'e12 = None  # your code here: the exponential of 12 in float16 (put it inside "with np.errstate(over=\\"ignore\\"):" to hide the warning)\n'
         'lost = None  # your code here: 1 plus 0.0004, both as float16\n'
         'prod400 = None  # your code here: the product of 400 probabilities of 0.1\n'
         'sumlog400 = None  # your code here: the sum of the logs of 400 probabilities of 0.1\n'
         'check("largest float16 number", f16_max, 65504, 0)\n'
         'check("exp(12) in float16 is inf", None if e12 is None else float(np.isinf(e12)), 1, 0)\n'
         'check("1 + 0.0004 in float16 is still 1", None if lost is None else float(lost), 1, 0)\n'
         'check("the product of 400 probabilities of 0.1 is 0", prod400, 0, 0)\n'
         'check("the sum of 400 logs of 0.1", sumlog400, -921.034, 0.001)')
    n.read('Why is the update of 0.0004 lost? How many significant digits does float16 keep?')
    n.change('Run the experiment cell: the product and the sum of logs for 300 tokens. Is the product still above zero?')
    n.code('print(0.1 ** 300, round(300 * np.log(0.1), 3))')

    n.step(4, 'Ridge regression in closed form', 'Ten training points, a degree 9 polynomial: columns 1, x, x^2, ..., x^9. The ridge answer is w = (X^T X + lambda P)^-1 X^T y, with P the identity matrix whose first entry is 0, so the intercept is not penalised. Illustrative data (made-up noisy points from a smooth curve).')
    n.predict('Without a penalty the curve passes through every point. Will its weights be small or enormous? Which lambda do you expect to give the lowest error on 20 new points?')
    n.code(f'xtr = np.linspace(-1, 1, 10)\nytr = np.array({ytr})\nxte = np.linspace(-0.97, 0.97, 20)\nyte = np.array({yte})\n'
           'Xtr = np.vander(xtr, 10, increasing=True)     # columns 1, x, ..., x^9\nXte = np.vander(xte, 10, increasing=True)\n'
           'P = np.eye(10)\nP[0, 0] = 0.0                                 # do not penalise the intercept\n'
           'print(Xtr.shape, Xte.shape)')
    todo('def ridge(X, y, lam):\n'
         '    if lam == 0:\n        return np.linalg.lstsq(X, y, rcond=None)[0]   # X^T X is badly conditioned at lambda = 0: use a least squares solver\n'
         '    return np.linalg.solve(X.T @ X + lam * P, X.T @ y)\n'
         'def rmse(X, w, y):\n    return float(np.sqrt(np.mean((X @ w - y) ** 2)))\n'
         'w0, w1, w10 = ridge(Xtr, ytr, 0.0), ridge(Xtr, ytr, 0.1), ridge(Xtr, ytr, 10.0)\n'
         'norm0, norm1, norm10 = w0[1:] @ w0[1:], w1[1:] @ w1[1:], w10[1:] @ w10[1:]   # sum of squared weights without the intercept\n'
         'print(round(norm0), round(norm1, 4), round(norm10, 4))\n'
         'print(round(rmse(Xtr, w0, ytr), 4), round(rmse(Xte, w0, yte), 4), round(rmse(Xte, w1, yte), 4), round(rmse(Xte, w10, yte), 4))\n'
         f'check("sum of squared weights, lambda = 0.1", norm1, {r3["norm2"]}, 0.0001)\n'
         f'check("sum of squared weights, lambda = 10", norm10, {r5["norm2"]}, 0.0001)\n'
         'check("the unpenalised weights are enormous", float(norm0 > 10000), 1, 0)\n'
         f'check("training error, lambda = 0.1", rmse(Xtr, w1, ytr), {r3["rmse_tr"]}, 0.0001)\n'
         f'check("error on the 20 new points, lambda = 0", rmse(Xte, w0, yte), {r0["rmse_te"]}, 0.001)\n'
         f'check("error on the 20 new points, lambda = 0.1", rmse(Xte, w1, yte), {r3["rmse_te"]}, 0.0001)',
         '# Hint: the closed form is on the slide "Ridge has a closed-form answer". np.linalg.solve is better than an explicit inverse. RMSE is defined on the ridge table slide. The intercept is not in the sum of squared weights.\n'
         'def ridge(X, y, lam):\n'
         '    if lam == 0:\n        return np.linalg.lstsq(X, y, rcond=None)[0]\n'
         '    return None  # your code here: the ridge weights for lam > 0\n'
         'def rmse(X, w, y):\n    return None  # your code here: the root of the mean squared error\n'
         'w0, w1, w10 = ridge(Xtr, ytr, 0.0), ridge(Xtr, ytr, 0.1), ridge(Xtr, ytr, 10.0)\n'
         'norm0 = norm1 = norm10 = None  # your code here: the sum of squared weights without the intercept\n'
         f'check("sum of squared weights, lambda = 0.1", norm1, {r3["norm2"]}, 0.0001)\n'
         f'check("sum of squared weights, lambda = 10", norm10, {r5["norm2"]}, 0.0001)\n'
         'check("the unpenalised weights are enormous", None if norm0 is None else float(norm0 > 10000), 1, 0)\n'
         f'check("training error, lambda = 0.1", None if w1 is None else rmse(Xtr, w1, ytr), {r3["rmse_tr"]}, 0.0001)\n'
         f'check("error on the 20 new points, lambda = 0", None if w0 is None else rmse(Xte, w0, yte), {r0["rmse_te"]}, 0.001)\n'
         f'check("error on the 20 new points, lambda = 0.1", None if w1 is None else rmse(Xte, w1, yte), {r3["rmse_te"]}, 0.0001)')
    n.read('The unpenalised training error is almost 0 but its error on new points is the largest. What do we call that? What happens to the training error as lambda grows?')
    n.change('Run the experiment cell: the error on the 20 new points for six values of lambda. Which lambda is lowest?')
    n.code('for lam in [0.0, 0.001, 0.01, 0.1, 1.0, 10.0]:\n    w = ridge(Xtr, ytr, lam)\n    print(lam, round(rmse(Xtr, w, ytr), 4), round(rmse(Xte, w, yte), 4))')
    n.code('xg = np.linspace(-1, 1, 200)\n'
           'if w1 is None:\n    print("Fill in the ridge answer cell above first.")\nelse:\n'
           '    plt.figure(figsize=(6, 3))\n    plt.scatter(xtr, ytr, color="black", zorder=3)\n'
           '    plt.plot(xg, np.sin(1.5 * xg) + 0.4 * xg ** 2, "k--", label="true curve")\n'
           '    plt.plot(xg, np.vander(xg, 10, increasing=True) @ w1, color="#AE2525", label="ridge, lambda = 0.1")\n'
           '    plt.legend()\n    plt.show()')

    n.step(5, 'Weight decay, a constraint and clipping', 'Weight decay: w <- (1 - 2 eta lambda) w - eta dL/dw. A constraint: the lowest loss w1^2 + w2^2 on the line w1 + w2 = 2. Clipping: g <- g c / (length of g) when the length exceeds c.')
    n.predict('One step with w = 2, eta = 0.1, lambda = 0.5 and gradient 1: bigger or smaller than 2? Where on the line is the loss lowest?')
    todo('eta, lam, g = 0.1, 0.5, 1.0\n'
         'w_new = (1 - 2 * eta * lam) * 2.0 - eta * g          # weight decay step for w = 2\n'
         'w1v = np.linspace(0, 2, 5)                           # points on the line w1 + w2 = 2\n'
         'loss = w1v ** 2 + (2 - w1v) ** 2\n'
         'best = w1v[np.argmin(loss)]\n'
         'gvec = np.array([30.0, 40.0])\n'
         'glen = np.sqrt((gvec ** 2).sum())\n'
         'clipped = gvec * (5.0 / glen) if glen > 5.0 else gvec  # limit c = 5\n'
         'print(w_new, loss, best, glen, clipped)\n'
         'check("weight after one step with decay", w_new, 1.7, 0.0001)\n'
         'check("lowest loss on the line", loss.min(), 2, 0.0001)\n'
         'check("best w1 on the line", best, 1, 0.0001)\n'
         'check("clipped gradient", clipped, [3, 4], 0.0001)',
         '# Hint: the weight-decay slide gives the update, and the constraint slide gives the loss. To clip, rescale the vector to length 5.\n'
         'eta, lam, g = 0.1, 0.5, 1.0\n'
         'w_new = None  # your code here: the new w after one decay step, starting from w = 2\n'
         'w1v = np.linspace(0, 2, 5)\n'
         'loss = None  # your code here: the loss at each point of w1v\n'
         'best = None  # your code here: the w1 with the lowest loss\n'
         'gvec = np.array([30.0, 40.0])\n'
         'clipped = None  # your code here: gvec shortened to length 5, same direction\n'
         'check("weight after one step with decay", w_new, 1.7, 0.0001)\n'
         'check("lowest loss on the line", None if loss is None else loss.min(), 2, 0.0001)\n'
         'check("best w1 on the line", best, 1, 0.0001)\n'
         'check("clipped gradient", clipped, [3, 4], 0.0001)')
    n.read('At the best point, the loss slope (2 w1, 2 w2) = (2, 2) is parallel to the line slope (1, 1). Why does that tell us it is the best point?')
    n.change('Run the experiment cell: take lambda = 2 and keep the other numbers. Predict whether w_new is below or above 1.7.')
    n.code('print((1 - 2 * 0.1 * 2.0) * 2.0 - 0.1 * 1.0)')

    n.step(6, 'Show the checks', 'Run this last cell. A learner who has filled every answer sees "All ... checks pass".')
    n.code('show_checks()')
    return n
