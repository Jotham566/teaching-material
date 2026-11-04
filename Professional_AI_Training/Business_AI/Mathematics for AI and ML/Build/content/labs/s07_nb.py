"""Session 7 lab (Python): numerical derivatives, rules checked by finite differences, the loss of a one-parameter model and which way to move w."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'kit'))
import nb  # noqa: E402

TITLE = 'Derivatives'


def build(solution: bool) -> 'nb.Notebook':
    def T(sol, learner):
        return sol if solution else learner

    n = nb.Notebook()
    n.md('# Session 7 lab: Derivatives\n\n'
         '**Mathematics for AI and Machine Learning, KLAi Professional Learning**\n\n'
         'Today you build a slope estimator from two nearby points (a finite difference), use it to check the derivative rules, and then use it on the loss of a tiny model. '
         'The data are four illustrative deliveries (made-up numbers): the distance x in km and the fee y in thousand UGX. The spreadsheet lab uses the same numbers.\n\n'
         'Rhythm of every step: **PREDICT**, run, **READ**, **CHANGE one thing**. Run the cells in order from the top. '
         'A cell that says `answer = None  # your code here` is yours to fill. Lines that start with `check(` tell you whether your answer is right.')
    n.check_setup()

    n.step(0, 'Set up', 'We use only numpy (numbers), pandas (tables) and matplotlib (charts). Run the cell.')
    n.code('import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\nprint("Ready. numpy", np.__version__)')

    n.step(1, 'The slope from two points', 'A slope is the change in output divided by the change in input. For a curve we use two points that are close together. '
           'The function is f(x) = x squared and the point is x = 3. Here the step is h = 1, so the second point is x = 4.')
    n.predict('For f(x) = x squared, what is the slope between x = 3 and x = 4? Work it out on paper: f(4) minus f(3), divided by 1.')
    n.code('def f(x):\n    return x ** 2\n\nx0 = 3\nh = 1\n' +
           T('slope_h1 = (f(x0 + h) - f(x0)) / h',
             '# Hint: (f(x0 + h) - f(x0)) / h\nslope_h1 = None  # your code here') +
           "\nprint('slope with h = 1:', slope_h1)\ncheck('slope of x^2 at 3 with h = 1', slope_h1, 7)")
    n.read('Is the number the slope of the curve at x = 3, or the slope of the line joining two points? Look at the picture on the slides.')

    n.step(2, 'Shrink the step h', 'The derivative is the value these slopes settle on as h gets smaller. Build the whole table at once: one slope for each h.')
    n.predict('As h gets smaller, what number do the slopes get close to? Guess before you run.')
    n.code('hs = [2, 1, 0.5, 0.1, 0.01, 0.001]\n' +
           T('slopes = [(f(x0 + h) - f(x0)) / h for h in hs]',
             '# Hint: a list with (f(x0 + h) - f(x0)) / h for each h in hs\nslopes = None  # your code here') +
           "\ntable = pd.DataFrame({'h': hs, 'slope': slopes})\nprint(table)\n"
           "check('slopes for the six values of h', slopes, [8, 7, 6.5, 6.1, 6.01, 6.001], tol=0.0005)")
    n.read('What do the slopes approach? Which h gives the answer closest to it?')
    n.change('In a new cell, add h = 1e-12 to the list and run it again. What happened to the slope? Why would a computer have trouble here? (It subtracts two numbers that are almost equal.)')

    n.step(3, 'A better estimate: the central difference', 'Looking on both sides of x gives a more accurate slope. '
           'You write one function, slope, and use it for the rest of the lab. Then you test it on the rules from the slides.')
    n.predict('For x cubed at x = 2 the power rule says the slope is 3 times 2 squared. What number is that?')
    n.code('def slope(f, x, h=1e-5):\n' +
           T('    return (f(x + h) - f(x - h)) / (2 * h)',
             '    # Hint: (f(x + h) - f(x - h)) / (2 * h)\n    return None  # your code here') +
           "\n\nprint('x^2 at 3:', slope(f, 3))")
    n.code("# Each case is: name, function, point, exact slope from the rule\n"
           "cases = [('x^3 at 2 (power rule)', lambda x: x ** 3, 2, 12.0),\n"
           "         ('e^x at 1 (exponential rule)', np.exp, 1, np.e),\n"
           "         ('ln x at 2 (logarithm rule, 1/x)', np.log, 2, 0.5),\n"
           "         ('x^2 e^x at 1 (product rule, 3e)', lambda x: x ** 2 * np.exp(x), 1, 3 * np.e),\n"
           "         ('x^2/(x+1) at 1 (quotient rule)', lambda x: x ** 2 / (x + 1), 1, 0.75)]\n"
           "for name, g, x, exact in cases:\n"
           "    estimate = slope(g, x)\n"
           "    print(name, '| finite difference:', estimate, '| rule:', exact)\n"
           "    check(name, estimate, exact, tol=0.0001)")
    n.read('For each case, how many decimals does the finite difference share with the rule? If one case disagrees, which of the two would you check first?')

    n.step(4, 'The loss of a one-parameter model', 'The model predicts the fee as w times the distance. The loss is the mean of the squared errors. '
           'Write it as a function of w so that you can try many values.')
    n.predict('At w = 1 the predictions are 1, 2, 3, 4 and the fees are 3, 5, 6, 9. The errors are -2, -3, -3, -5. What is the mean of their squares?')
    n.code('x = np.array([1, 2, 3, 4])   # distance in km\ny = np.array([3, 5, 6, 9])   # fee in thousand UGX\nn_rows = len(x)\n\ndef loss(w):\n' +
           T('    return np.mean((w * x - y) ** 2)',
             '    # Hint: the mean of (w * x - y) ** 2\n    return None  # your code here') +
           "\n\nprint('L(1) =', loss(1), '  L(2) =', loss(2), '  L(3) =', loss(3))\n"
           "check('L(1)', loss(1), 11.75)\ncheck('L(2)', loss(2), 0.75)")
    n.read('Which of w = 1, 2 and 3 gives the smallest loss? Does that match the bowl on the slides?')

    n.step(5, 'The derivative of the loss, checked by numbers', 'The slides give dL/dw = 2/n times the sum of x times (w x minus y). Write it, then compare it with your central difference.')
    n.predict('At w = 1 the slides say the slope is -18.5. At w = 3 it is +11.5. What does the sign tell you about the loss?')
    n.code('def dloss(w):\n' +
           T('    return 2 / n_rows * np.sum(x * (w * x - y))',
             '    # Hint: 2 / n_rows times the sum of x * (w * x - y)\n    return None  # your code here') +
           "\n\nprint('formula   :', dloss(1), dloss(3))\n"
           "print('finite diff:', slope(loss, 1), slope(loss, 3))\n"
           "check('slope of the loss at w = 1', dloss(1), -18.5)\n"
           "check('slope of the loss at w = 3', dloss(3), 11.5)\n"
           "check('formula agrees with the finite difference', [dloss(1), dloss(3)], [slope(loss, 1), slope(loss, 3)], tol=0.0001)")
    n.read('The two printed lines should agree to many decimals. If they do not, which one would you trust less, the formula or the finite difference, and how would you find out?')

    n.step(6, 'Which way to move w', 'Move w opposite to the sign of the slope: a negative slope means raise w, a positive slope means lower w. Turn that rule into a number: +1 for raise, -1 for lower.')
    n.predict('At w = 2 the slope of the loss is -3.5. Should w go up or down? Is the loss near its bottom there?')
    n.code('def move(w):\n' +
           T('    return 1 if dloss(w) < 0 else -1',
             '    # Hint: +1 if dloss(w) is negative (raise w), otherwise -1 (lower w)\n    return None  # your code here') +
           "\n\nfor w in [0, 1, 2, 3, 4]:\n    print('w =', w, '| loss =', round(float(loss(w)), 3), '| slope =', round(float(dloss(w)), 3), '| move:', move(w))\n"
           "check('direction at w = 1 and at w = 3', [move(1), move(3)], [1, -1])")
    n.read('Where does the slope change sign? Which two values of w is the bottom between?')

    n.step(7, 'The bottom of the bowl', 'At the lowest point the slope is zero. Solving dL/dw = 0 gives w = (sum of x times y) divided by (sum of x squared). Then draw the loss curve with the tangent line at w = 1.')
    n.predict('The sum of x times y is 67 and the sum of x squared is 30. What is w?')
    n.code(T('w_star = np.sum(x * y) / np.sum(x * x)', '# Hint: the sum of x * y divided by the sum of x * x\nw_star = None  # your code here') +
           "\nprint('best w:', w_star)\n"
           "check('best w', w_star, 2.2333, tol=0.001)\n"
           "check('loss at the best w', loss(w_star), 0.3417, tol=0.001)\n"
           "check('slope at the best w is zero', dloss(w_star), 0, tol=0.0001)")
    n.code("ws = np.linspace(0, 4, 200)\nplt.figure(figsize=(6.4, 3.8))\nplt.plot(ws, [loss(w) for w in ws], color='black', linewidth=2.5, label='loss L(w)')\n"
           "tangent = loss(1) + dloss(1) * (ws - 1)\nplt.plot(ws, tangent, color='#AE2525', linewidth=2, label='tangent at w = 1 (slope -18.5)')\n"
           "plt.scatter([1, 2.2333], [loss(1), loss(2.2333)], color='#E0BE36', edgecolor='black', zorder=5, s=70)\n"
           "plt.ylim(0, 40)\nplt.xlabel('parameter w')\nplt.ylabel('loss L(w)')\nplt.legend()\nplt.show()")
    n.change('In a new cell, change the last fee from 9 to 10, recompute w_star and the loss. Does the best w go up or down? Predict first. (Answer: w goes up to 2.367, because a bigger fee needs a bigger fee per km.)')

    n.md('---\n## Finished\n\nRun the next cell for your automatic check. Then use File, Save. Keep three numbers: -18.5, +11.5 and 2.233.')
    n.code('show_checks()')
    return n


def CHECK(rs):
    """Problems if the printed numbers differ from the slides."""
    out = '\n'.join(o for _, o, _ in rs)
    probs = []
    for needle in ('slope with h = 1: 7', 'L(1) = 11.75', '-18.5', 'best w: 2.2333'):
        if needle not in out:
            probs.append(f'expected output {needle!r} not found')
    return probs
