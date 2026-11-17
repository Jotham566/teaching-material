"""Session 9 lab (Python): chain rule slopes, forward and backward values on a tiny graph, the Jacobian by formula and by nudging, and J transposed times a gradient."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'kit'))
import nb  # noqa: E402

TITLE = 'The chain rule and the Jacobian'


def build(solution: bool) -> 'nb.Notebook':
    def T(sol, learner):
        return sol if solution else learner

    n = nb.Notebook()
    n.md('# Session 9 lab: The chain rule and the Jacobian\n\n'
         '**Mathematics for AI and Machine Learning, KLAi Professional Learning**\n\n'
         'Today you compute the slope of a function of a function with the chain rule, run a tiny computation graph forwards and backwards, '
         'compute the Jacobian of a function with two inputs and two outputs, and check every answer with finite differences (nudges). '
         'The delivery data are the same four illustrative deliveries as Sessions 7 and 8 (made-up numbers): distance x in km, fee y in thousand UGX. The spreadsheet lab uses the same numbers.\n\n'
         'Rhythm of every step: **PREDICT**, run, **READ**, **CHANGE one thing**. Run the cells in order from the top. '
         'A cell that says `None  # your code here` is yours to fill. Lines that start with `check(` tell you whether your answer is right.')
    n.check_setup()

    n.step(0, 'Set up and write the checking tool', 'We use numpy for numbers. The function slope() estimates a slope by nudging the input up and down (the central difference from Session 7). We use it to check every answer today.')
    n.code('import numpy as np\n\n'
           'x = np.array([1.0, 2.0, 3.0, 4.0])   # distance in km\ny = np.array([3.0, 5.0, 6.0, 9.0])   # fee in thousand UGX\n\n'
           'def slope(f, at, h=1e-5):\n    # central difference: change in f over a tiny step on both sides, divided by 2h\n    return (f(at + h) - f(at - h)) / (2 * h)\n\n'
           'print("slope of x squared at 3:", round(slope(lambda t: t ** 2, 3.0), 4))')

    n.step(1, 'The chain rule on y = (3x + 1) squared', 'The inner function is u = 3x + 1 and the outer function is y = u squared. The slope of y with respect to x is the outer slope times the inner slope.')
    n.predict('At x = 2 the inner value is u = 7. What is the outer slope 2u, and what is the product with the inner slope 3? Write the number down before you run.')
    n.code('def inner(x):\n    return 3 * x + 1\n\ndef outer(u):\n    return u ** 2\n\nx0 = 2.0\nu0 = inner(x0)\n' +
           T('dy_du = 2 * u0     # slope of the outer function, evaluated at u0\ndu_dx = 3          # slope of the inner function\nchain = dy_du * du_dx',
             '# Hint: dy_du is the slope of the outer function u squared at u0; du_dx is the slope of the inner function 3x + 1; chain combines the two\ndy_du = None  # your code here\ndu_dx = None  # your code here\nchain = None  # your code here') +
           "\nprint('u =', u0, ' dy/du =', dy_du, ' du/dx =', du_dx, ' chain rule slope =', chain)\n"
           "nudged = None\nif chain is not None:   # the nudged check runs after you have predicted and filled in your answer\n    nudged = slope(lambda t: outer(inner(t)), x0)\n    print('nudged slope:', round(nudged, 4))\n"
           "check('chain rule slope at x = 2', chain, 42)\ncheck('chain rule slope agrees with the nudged slope', chain, nudged, tol=0.001)")
    n.read('Which of the two numbers did you forget if you got 14 instead of 42?')

    n.step(2, 'A second chain: y = e to the 2x', 'The inner function is u = 2x with slope 2. The outer function is e to the u, whose slope is e to the u. Evaluate the outer slope at u = 2x.')
    n.predict('At x = 1 the inner value is u = 2. Using the table of examples on the slides, what do you expect the chain rule slope to be?')
    n.code('x1 = 1.0\n' +
           T('chain_exp = 2 * np.exp(2 * x1)   # inner slope 2 times outer slope e^u at u = 2x',
             '# Hint: the slope of the inner function 2x, times the slope of the outer function e to the u at u = 2 * x1\nchain_exp = None  # your code here') +
           "\nprint('chain rule slope:', chain_exp)\nnudged_exp = None\nif chain_exp is not None:\n    nudged_exp = slope(lambda t: np.exp(2 * t), x1)\n    print('nudged slope    :', round(nudged_exp, 3))\n"
           "check('slope of e to the 2x at x = 1', chain_exp, 14.778, tol=0.001)\ncheck('slope of e to the 2x agrees with the nudged slope', chain_exp, nudged_exp, tol=0.001)")
    n.change('In a new cell, change the inner function to 5x and recompute at x = 1. Predict the answer first with the chain rule, then check it with slope().')

    n.step(3, 'The tiny graph: forward pass, then backward pass', 'One delivery: x = 3 km, fee y = 6. The model is p = w x and the loss is L = (p - y) squared, at w = 1. Forward gives values; backward gives slopes, each one the previous slope times a local slope.')
    n.predict('Forward: what are p and L? Backward: what is dL/dp = 2 (p - y), and then dL/dw = dL/dp times x?')
    n.code('xd, yd, w = 3.0, 6.0, 1.0\n' +
           T('# forward pass\np = w * xd\nL = (p - yd) ** 2\n# backward pass\ndL_dp = 2 * (p - yd)\ndL_dw = dL_dp * xd',
             '# Hint: p is the model prediction and L is the squared error of that one delivery\np = None  # your code here\nL = None  # your code here\n# Hint: dL_dp is the slope of L with respect to p; dL_dw multiplies it by the local slope of p with respect to w\ndL_dp = None  # your code here\ndL_dw = None  # your code here') +
           "\nprint('forward :', p, L)\nprint('backward:', dL_dp, dL_dw)\n"
           "nudged_w = None\nif dL_dw is not None:\n    nudged_w = slope(lambda t: (t * xd - yd) ** 2, w)\n    print('nudged dL/dw:', round(nudged_w, 3))\n"
           "check('forward p', p, 3)\ncheck('forward L', L, 9)\ncheck('backward dL/dp', dL_dp, -6)\ncheck('backward dL/dw', dL_dw, -18)\ncheck('backward dL/dw agrees with the nudged slope', dL_dw, nudged_w, tol=0.001)")
    n.read('The value dL_dw is the slope of the loss with respect to w. Which way should w move, up or down?')

    n.step(4, 'The same graph for all four deliveries', 'Run the backward pass for each row. The loss of the whole dataset is the mean of the four row losses, so its slope is the mean of the four backward values.')
    n.predict('The four errors p minus y at w = 1 are -2, -3, -3 and -5. Guess the mean of the four dL/dw values. Look back at Session 8: what was dL/dw at (1, 0)?')
    n.code('errors = w * x - y\n' +
           T('row_dp = 2 * errors        # dL/dp for each row\nrow_dw = row_dp * x         # dL/dw for each row\nmean_dw = np.mean(row_dw)',
             '# Hint: row_dp is the slope of each row loss with respect to its prediction; row_dw multiplies it by the local slope of the prediction with respect to w; mean_dw averages the four rows\nrow_dp = None  # your code here\nrow_dw = None  # your code here\nmean_dw = None  # your code here') +
           "\nprint('row dL/dw values:', row_dw)\nprint('mean            :', mean_dw)\n"
           "check('row dL/dw values', row_dw, [-4, -12, -18, -40])\ncheck('mean dL/dw equals the Session 8 slope', mean_dw, -18.5)")
    n.change('In a new cell set w = 2 and rerun the backward pass for the four rows. Predict first: will the mean be negative, zero or positive, and what does that say about which way w should move?')

    n.step(5, 'The Jacobian of a function with two inputs and two outputs', 'F(x1, x2) = (u, v) with u = x1 times x2 and v = x1 + x2 squared. The Jacobian has one row for each output and one column for each input.')
    n.predict('At the point (2, 3), what are the four entries? Row u: du/dx1 and du/dx2. Row v: dv/dx1 and dv/dx2.')
    n.code('def F(a, b):\n    return np.array([a * b, a + b ** 2])\n\npoint = (2.0, 3.0)\nprint("outputs u, v at (2, 3):", F(*point))\n\n' +
           T('J = np.array([[point[1], point[0]],     # row u: x2 and x1\n              [1.0, 2 * point[1]]])    # row v: 1 and 2 x2',
             '# Hint: differentiate u with respect to x1, then x2, for row u; do the same for v. Use point[0] for x1 and point[1] for x2.\nJ = None  # your code here: a 2 by 2 array') +
           "\nprint('Jacobian by formula:')\nprint(J)\n"
           "# nudge one input at a time: each nudge gives one whole column\n"
           "h = 1e-5\nJ_nudged = None\nif J is not None:\n    col1 = (F(point[0] + h, point[1]) - F(point[0] - h, point[1])) / (2 * h)\n    col2 = (F(point[0], point[1] + h) - F(point[0], point[1] - h)) / (2 * h)\n"
           "    J_nudged = np.column_stack([col1, col2])\n    print('Jacobian by nudging:')\n    print(np.round(J_nudged, 3))\n"
           "check('Jacobian by formula', J, [[3, 2], [1, 6]])\ncheck('Jacobian by formula agrees with nudging', J, J_nudged, tol=0.001)")
    n.read('Which entry is the largest, and which input does that output depend on most strongly at this point?')

    n.step(6, 'Back to the inputs: J transposed times a gradient', 'Let s = u times v, a single number computed from the two outputs. Its slopes with respect to u and v are v and u. Each input reaches s along two paths (through u and through v), and the path sums stacked together are J transposed times those slopes.')
    n.predict('At the point (2, 3) u = 6 and v = 11, so the slopes of s with respect to u and v are 11 and 6. Guess the sign of the two slopes with respect to x1 and x2.')
    n.code('u_val, v_val = F(*point)\ngrad_uv = np.array([v_val, u_val])   # ds/du = v and ds/dv = u\n' +
           T('grad_x = J.T @ grad_uv',
             '# Hint: the slopes with respect to the inputs are the transposed Jacobian times grad_uv (in numpy, J.T and @)\ngrad_x = None  # your code here') +
           "\nprint('gradient of s in the inputs:', grad_x)\n"
           "s_of = lambda a, b: F(a, b)[0] * F(a, b)[1]\nnudged_s = None\nif grad_x is not None:\n    nudged_s = np.array([slope(lambda t: s_of(t, point[1]), point[0]), slope(lambda t: s_of(point[0], t), point[1])])\n"
           "    print('nudged slopes of s            :', np.round(nudged_s, 3))\n"
           "check('gradient of s in the inputs', grad_x, [39, 58])\ncheck('gradient of s agrees with the nudged slopes', grad_x, nudged_s, tol=0.001)")
    n.change('In a new cell move the point to (1, 2). Predict the Jacobian and the gradient of s first, by hand, then compute J and J.T @ grad_uv again.')

    n.md('---\n## Finished\n\nRun the next cell for your automatic check. Then use File, Save. Keep the numbers 42, -18 and the Jacobian [[3, 2], [1, 6]].')
    n.code('show_checks()')
    return n


def CHECK(rs):
    out = '\n'.join(o for _, o, _ in rs)
    probs = []
    for needle in ('chain rule slope = 42', 'backward: -6.0 -18.0', '[3. 2.]', 'gradient of s in the inputs: [39. 58.]'):
        if needle not in out:
            probs.append(f'expected output {needle!r} not found')
    return probs
