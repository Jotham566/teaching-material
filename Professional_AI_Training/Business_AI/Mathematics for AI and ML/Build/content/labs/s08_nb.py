"""Session 8 lab (Python): the loss of a line fit, its gradient by formula and by nudges, a grid and contour plot, and the steepest downhill direction."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'kit'))
import nb  # noqa: E402

TITLE = 'Partial derivatives and the gradient'


def build(solution: bool) -> 'nb.Notebook':
    def T(sol, learner):
        return sol if solution else learner

    n = nb.Notebook()
    n.md('# Session 8 lab: Partial derivatives and the gradient\n\n'
         '**Mathematics for AI and Machine Learning, KLAi Professional Learning**\n\n'
         'Today the line has two parameters, a slope w and an intercept b, and the loss depends on both. You compute the loss, its gradient (one partial derivative for each parameter), '
         'check the gradient by nudging each parameter, draw the loss as a contour plot and find the steepest downhill direction. '
         'The data are the same four illustrative deliveries as Session 7 (made-up numbers): distance x in km, fee y in thousand UGX. The spreadsheet lab uses the same numbers.\n\n'
         'Rhythm of every step: **PREDICT**, run, **READ**, **CHANGE one thing**. Run the cells in order from the top. '
         'A cell that says `None  # your code here` is yours to fill. Lines that start with `check(` tell you whether your answer is right.')
    n.check_setup()

    n.step(0, 'Set up and load the data', 'We use numpy for numbers and matplotlib for charts. The four deliveries are typed in directly.')
    n.code('import numpy as np\nimport matplotlib.pyplot as plt\n\nx = np.array([1.0, 2.0, 3.0, 4.0])   # distance in km\ny = np.array([3.0, 5.0, 6.0, 9.0])   # fee in thousand UGX\nn_rows = len(x)\nprint("rows:", n_rows)')

    n.step(1, 'The loss of the line y-hat = w x + b', 'The loss is the mean of the squared errors, where the error of a row is the prediction minus the actual fee. It takes two inputs, w and b.')
    n.predict('At w = 1 and b = 0 the errors are -2, -3, -3, -5. What is the mean of their squares?')
    n.code('def loss(w, b):\n' +
           T('    return np.mean((w * x + b - y) ** 2)',
             '    # Hint: the mean of (w * x + b - y) ** 2\n    return None  # your code here') +
           "\n\nprint('L(1, 0)     =', loss(1, 0))\nprint('L(1.9, 1)   =', loss(1.9, 1.0))\n"
           "check('loss at the start (1, 0)', loss(1, 0), 11.75)\ncheck('loss at the best line (1.9, 1)', loss(1.9, 1.0), 0.175, tol=0.001)")
    n.read('Which of the two lines has the smaller loss? By how much?')

    n.step(2, 'The gradient by formula', 'The gradient is the vector of the two partial derivatives. For w: 2/n times the sum of x times the error. For b: 2/n times the sum of the errors.')
    n.predict('At the start the errors are all negative. Will the partial derivatives be negative or positive? Guess the sign of each.')
    n.code('def gradient(w, b):\n    e = w * x + b - y   # the four errors, prediction minus actual\n' +
           T('    dw = 2 / n_rows * np.sum(x * e)\n    db = 2 / n_rows * np.sum(e)',
             '    # Hint for dw: 2 / n_rows times the sum of x * e\n    dw = None  # your code here\n    # Hint for db: 2 / n_rows times the sum of e\n    db = None  # your code here') +
           "\n    return np.array([dw, db])\n\ng0 = gradient(1, 0)\ngb = gradient(1.9, 1.0)\nprint('gradient at (1, 0)  :', g0)\nprint('gradient at (1.9, 1):', gb)\n"
           "check('gradient at the start', g0, [-18.5, -6.5])\ncheck('gradient at the best line is zero', gb, [0, 0], tol=0.001)")
    n.code('length = ' + T('np.sqrt(g0[0] ** 2 + g0[1] ** 2)', 'None  # your code here: the square root of the sum of the two entries squared') +
           "\nprint('length of the gradient at the start:', length)\ncheck('length of the gradient', length, 19.61, tol=0.01)")
    n.read('The length is the steepness: the slope of the steepest direction. Which entry of the gradient is larger, and what does that mean for how much w and b should change?')

    n.step(3, 'Check the gradient by nudging one parameter at a time', 'Nudge w up and down with b held fixed, then do the same for b with w held fixed. Use the central difference from Session 7.')
    n.predict('The nudged estimates should be very close to -18.5 and -6.5. How many decimals do you expect to agree?')
    n.code('def numeric_gradient(w, b, h=1e-4):\n' +
           T('    dw = (loss(w + h, b) - loss(w - h, b)) / (2 * h)\n    db = (loss(w, b + h) - loss(w, b - h)) / (2 * h)',
             '    # Hint for dw: (loss(w + h, b) - loss(w - h, b)) / (2 * h)   (b stays fixed)\n    dw = None  # your code here\n    # Hint for db: (loss(w, b + h) - loss(w, b - h)) / (2 * h)   (w stays fixed)\n    db = None  # your code here') +
           "\n    return np.array([dw, db])\n\nprint('nudged estimate:', numeric_gradient(1, 0))\nprint('formula        :', gradient(1, 0))\n"
           "check('nudged gradient agrees with the formula', numeric_gradient(1, 0), gradient(1, 0), tol=0.001)")
    n.change('In a new cell, nudge both w and b together by +h and -h (change both inputs at once) and divide by 2h. Is the number equal to either partial derivative? It measures a slope along a diagonal instead.')

    n.step(4, 'A grid of losses', 'Try many pairs (w, b) and keep the loss for each. A table of losses is the contour map written as numbers. The smallest value is near the bottom of the bowl.')
    n.predict('On a grid with w from 0 to 3.5 and b from -1 to 3, both in steps of 0.5, which pair do you expect to give the smallest loss? Several pairs may tie.')
    n.code('w_values = np.arange(0, 3.51, 0.5)\nb_values = np.arange(-1, 3.01, 0.5)\n' +
           T('Z = np.array([[loss(w, b) for w in w_values] for b in b_values])',
             '# Hint: Z[row, column] is loss(w, b) with b from the row and w from the column\nZ = None  # your code here') +
           "\nif Z is not None:\n    print('grid shape (b rows, w columns):', Z.shape)\n    ties = np.argwhere(np.isclose(Z, Z.min()))\n"
           "    print('smallest loss on the grid:', Z.min(), 'at (w, b) =', [(float(w_values[j]), float(b_values[i])) for i, j in ties])\n"
           "check('smallest loss on the 0.5 grid', Z.min() if Z is not None else None, 0.25)")
    n.code("# A finer grid with steps of 0.1 finds the true bottom\nw_fine = np.round(np.arange(0, 3.51, 0.1), 1)\nb_fine = np.round(np.arange(-1, 3.01, 0.1), 1)\n"
           "Zf = np.array([[loss(w, b) for w in w_fine] for b in b_fine])\nbest = np.unravel_index(np.argmin(Zf), Zf.shape)\n"
           "print('smallest loss on the fine grid:', round(float(Zf.min()), 3), 'at w =', w_fine[best[1]], 'and b =', b_fine[best[0]])\n"
           "check('smallest loss on the 0.1 grid', Zf.min(), 0.175, tol=0.001)")
    n.read('The 0.5 grid shows two grid points that tie for the smallest loss, and the true minimum lies between grid points. The fine grid finds w = 1.9 and b = 1.0. What is lost when the grid is coarse?')

    n.step(5, 'A contour plot with the gradient arrow', 'Draw the contour lines of the loss and the start point, with an arrow along minus the gradient (the direction of steepest decrease). The arrow should cross the contour lines at a right angle.')
    n.predict('Will the arrow point straight at the best line (1.9, 1)? Or will it point somewhere slightly different? Decide before you run.')
    n.code("plt.figure(figsize=(6.4, 4.2))\ncs = plt.contour(w_fine, b_fine, Zf, levels=[0.5, 1, 3, 10, 20, 30], colors='grey')\nplt.clabel(cs, fmt='%g')\n"
           "plt.scatter([1, 1.9], [0, 1], color='#E0BE36', edgecolor='black', s=90, zorder=5)\n"
           "unit = -g0 / np.linalg.norm(g0)\nplt.arrow(1, 0, 0.8 * unit[0], 0.8 * unit[1], color='#AE2525', width=0.02, head_width=0.1, zorder=6)\n"
           "plt.gca().set_aspect('equal')\nplt.xlabel('slope w')\nplt.ylabel('intercept b')\nplt.title('Contours of the loss, arrow = minus the gradient')\nplt.show()")
    n.read('Does the red arrow cross the contour lines at a right angle? Does it point at the gold dot at (1.9, 1)?')

    n.step(6, 'The steepest direction, found by trying every direction', 'From the start, take a tiny step of length 0.01 in each of 360 directions and see which direction lowers the loss most. It should be minus the gradient.')
    n.predict('Minus the gradient is (18.5, 6.5). About how many degrees above the w axis is that direction? Think of the angle of a right triangle with sides 18.5 and 6.5.')
    n.code("angles = np.arange(0, 360)   # whole degrees\nstep = 0.01\n" +
           T("after = [loss(1 + step * np.cos(np.radians(a)), 0 + step * np.sin(np.radians(a))) for a in angles]\nbest_angle = angles[np.argmin(after)]",
             "# Hint: the loss after a step of length 0.01 in direction a; then pick the angle with the smallest loss\nafter = None  # your code here: a list with one loss for each angle\nbest_angle = None  # your code here: the angle with the smallest loss") +
           "\nprint('best direction by trying all:', best_angle, 'degrees')\n"
           "print('minus the gradient points at   :', round(float(np.degrees(np.arctan2(-g0[1], -g0[0]))), 1), 'degrees')\n"
           "check('steepest direction in degrees', best_angle, 19.4, tol=1.0)")
    n.change('In a new cell, start at (3, 0) instead of (1, 0). Compute the gradient there and the best direction. Predict first: will the steepest way down point left or right? (Answer: left and down, because w = 3 is already too large.)')

    n.md('---\n## Finished\n\nRun the next cell for your automatic check. Then use File, Save. Keep the gradient at the start, (-18.5, -6.5), and the best line w = 1.9, b = 1.')
    n.code('show_checks()')
    return n


def CHECK(rs):
    out = '\n'.join(o for _, o, _ in rs)
    probs = []
    for needle in ('L(1, 0)     = 11.75', '[-18.5  -6.5]', 'smallest loss on the grid: 0.25', 'best direction by trying all: 19'):
        if needle not in out:
            probs.append(f'expected output {needle!r} not found')
    return probs
