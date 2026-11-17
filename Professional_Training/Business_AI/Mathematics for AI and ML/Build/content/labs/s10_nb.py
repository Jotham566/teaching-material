"""Session 10 Python lab: gradient descent for a line fit. Author D."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'kit'))
import nb as NB  # noqa: E402
import diagrams_math_d as D  # noqa: E402

TITLE = 'Gradient descent for a line fit'


def todo(b, solution, hint, learner, model):
    """A cell the learner completes: the learner version holds `learner`, the solution version holds `model`."""
    b.code(('# Hint: ' + hint + '\n' if hint else '') + (model if solution else learner))


LOOP_HEAD = ('def gradient_descent(eta, steps=30):\n'
             '    """Run gradient descent on the centred line fit. Returns the final w, b and the loss at every step."""\n'
             '    w, b = 0.0, 0.0\n'
             '    losses = [np.mean((w * xc + b - y) ** 2)]\n'
             '    for step in range(steps):\n'
             '        err = w * xc + b - y                  # the error y-hat - y of every row\n')
LOOP_LEARNER = ('        dw = None      # your code here: the slope for w, the same formula as dw0 in step 2\n'
                '        db = None      # your code here: the slope for b, the same formula as db0 in step 2\n'
                '        w_new = None   # your code here: the update rule of step 3, applied to w\n'
                '        b_new = None   # your code here: the update rule of step 3, applied to b\n')
LOOP_MODEL = ('        dw = 2 * np.mean(err * xc)\n'
              '        db = 2 * np.mean(err)\n'
              '        w_new = w - eta * dw\n'
              '        b_new = b - eta * db\n')
LOOP_TAIL = ('        if w_new is None or b_new is None:\n'
             '            return None, None, None             # the loop body is not written yet\n'
             '        w, b = w_new, b_new\n'
             '        losses.append(np.mean((w * xc + b - y) ** 2))\n'
             '    return w, b, losses')


def build(solution):
    n = D.n10()
    R = n['runs']
    b = NB.Notebook()
    b.md('# Session 10: Gradient descent for a line fit\n\n**KLAi | Mathematics for AI and Machine Learning**\n\n'
         'In this lab you fit a line to eight boda boda trips by gradient descent, with a loop you write yourself, and you watch what four different learning rates do to the loss. '
         'The same numbers are in the spreadsheet lab. The trip data are illustrative (made-up numbers to show the arithmetic).\n\n'
         'The five steps match the lab map on the slides. Each step has the same rhythm: **PREDICT**, run, **READ**, then **CHANGE one thing**. A cell that says `None  # your code here` is yours to fill. The check cells say OK or NOT YET.')
    b.check_setup()

    b.step(1, 'Look at the data and centre the distance', 'Each row is one trip: the distance in km and the fare in thousand UGX. Gradient descent works best when the input is centred, so we subtract the mean distance from every distance. '
           'The centred distance is called `xc`, and it uses the mean you compute.')
    b.predict('The distances run from 1 to 8 km. What is their mean?')
    b.code('import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\n'
           'df = pd.DataFrame({"distance_km": [1, 2, 3, 4, 5, 6, 7, 8],\n'
           '                   "fare": [3.2, 4.1, 5.4, 5.9, 7.6, 8.0, 9.9, 10.3]})   # fare in thousand UGX\n'
           'print(df)')
    todo(b, solution, 'use the mean of the distance column', 'mean_distance = None  # your code here', 'mean_distance = df["distance_km"].mean()')
    b.code('x = df["distance_km"].to_numpy(dtype=float)\ny = df["fare"].to_numpy(dtype=float)\nn = len(x)\n'
           'check("mean distance is 4.5", mean_distance, 4.5)\n'
           'if mean_distance is None:\n'
           '    print("Fill in mean_distance in the cell above first: the centred distance is built from it.")\n'
           '    xc = x - x.mean()                      # a stand-in so that later cells can still run\n'
           'else:\n'
           '    xc = x - mean_distance                 # the centred distance, built from your mean\n'
           '    print("centred distances:", xc)')
    b.read('Why do the centred distances run from -3.5 to +3.5? What does a centred distance of 0 mean for a trip?')

    b.step(2, 'The loss and the gradient at the start', 'The model is y-hat = b + w * xc. We start with w = 0 and b = 0. The loss is the mean squared error. '
           'The gradient has two entries: dL/dw = (2/n) * sum(err * xc) and dL/db = (2/n) * sum(err), where err = y-hat - y.')
    b.predict('With w = 0 and b = 0 every prediction is 0. So what is the loss? (Hint: the mean of y squared.)')
    todo(b, solution, 'err is y-hat minus y. Use np.mean for the averages.',
         'w, b = 0.0, 0.0\nerr = w * xc + b - y\nloss0 = None  # your code here: the mean of err squared\ndw0 = None    # your code here: 2 times the mean of err * xc\ndb0 = None    # your code here: 2 times the mean of err',
         'w, b = 0.0, 0.0\nerr = w * xc + b - y\nloss0 = np.mean(err ** 2)\ndw0 = 2 * np.mean(err * xc)\ndb0 = 2 * np.mean(err)')
    b.code('check("loss at w = 0, b = 0", loss0, %.4f, 0.01)\ncheck("dL/dw at the start", dw0, %.4f, 0.01)\ncheck("dL/db at the start", db0, %.4f, 0.01)\n'
           'if loss0 is not None:\n    print("loss at the start:", loss0, " slopes:", dw0, db0)' % (n['loss0'], n['dw0'], n['db0']))
    b.read('Both slopes are negative. Which way should w and b move to lower the loss?')

    b.step(3, 'One step by hand', 'The update rule is new = old - eta * slope. Use eta = 0.1.')
    b.predict('Will the new w and b be bigger or smaller than 0? Roughly how big?')
    todo(b, solution, 'apply the update rule from the slides to w and to b',
         'eta = 0.1\nw1 = None  # your code here\nb1 = None  # your code here',
         'eta = 0.1\nw1 = w - eta * dw0\nb1 = b - eta * db0')
    b.code('check("w after one step", w1, %.4f, 0.001)\ncheck("b after one step", b1, %.4f, 0.001)\n'
           'if w1 is not None:\n    print("after one step:", w1, b1)' % (n['w1'], n['b1']))
    b.change('Change eta to 0.2 and run Step 3 again. How do w1 and b1 change? Put eta back to 0.1 before you go on.')

    b.step(4, 'Write the loop, run 30 steps, compare with least squares', 'The frame of the loop is given: it starts at w = 0 and b = 0, computes the error of every row, and records the loss after every step. '
           'You write the four lines in the middle: the two slopes and the two updates. Then compare the result with the least squares line of Session 4 for these eight trips: '
           '`np.polyfit(xc, y, 1)` returns the slope and then the intercept.')
    b.predict('After 30 steps with eta = 0.1, will gradient descent reach the least squares line, or stop short of it?')
    b.code(LOOP_HEAD + (LOOP_MODEL if solution else LOOP_LEARNER) + LOOP_TAIL + '\n\n'
           'w_fit, b_fit, losses = gradient_descent(0.1)\n'
           'if losses is None:\n    print("Write the four lines inside the loop, then run this cell again.")\n'
           'else:\n    print("w =", round(w_fit, 4), " b =", round(b_fit, 4))\n'
           '    print("loss at steps 0, 1, 5, 30:", [round(losses[k], 4) for k in (0, 1, 5, 30)])')
    todo(b, solution, 'np.polyfit fits a polynomial; a line is a polynomial of degree 1. It returns the slope first', 'w_ls, b_ls = None, None  # your code here',
         'w_ls, b_ls = np.polyfit(xc, y, 1)')
    b.code('check("loss after 30 steps, eta = 0.1", None if losses is None else losses[-1], %.4f, 0.001)\n'
           'check("least squares slope", w_ls, %.3f, 0.01)\ncheck("least squares intercept", b_ls, %.3f, 0.01)\n'
           'check("gradient descent is within 0.01 of the least squares slope", w_fit, %.3f, 0.01)\n'
           'if w_ls is not None and w_fit is not None:\n    print("least squares: w =", round(w_ls, 4), " b =", round(b_ls, 4), "| gradient descent: w =", round(w_fit, 4), " b =", round(b_fit, 4))'
           % (R[0.1]['L'][-1], n['w_star'], n['b_star'], n['w_star']))
    b.read('Is the loss going down at every step? The intercept b is the fare for a trip of average length (4.5 km). Is it close to the mean of the fares?')

    b.step(5, 'Four learning rates, four loss curves', 'Run your loop with eta = 0.01, 0.05, 0.1 and 0.2 and plot the four loss curves. The vertical axis uses a log scale so that all four fit.')
    b.predict('Which curve falls fastest? Which curve will go up instead of down? Write both guesses first.')
    b.code('etas = [0.01, 0.05, 0.1, 0.2]\ncurves = {}\nfor eta_k in etas:\n    wk, bk, lk = gradient_descent(eta_k)\n    curves[eta_k] = lk\n\n'
           'if curves[0.1] is None:\n    print("Finish the loop in step 4 first.")\nelse:\n'
           '    for eta_k in etas:\n        plt.plot(curves[eta_k], label="eta = " + str(eta_k))\n'
           '    plt.yscale("log")\n    plt.xlabel("step")\n    plt.ylabel("loss (log scale)")\n    plt.legend()\n    plt.title("Loss curves for four learning rates")\n    plt.show()')
    todo(b, solution, 'each list holds the loss at every step; you want the last entry of each, and for "grew" compare the last entry of the eta = 0.2 list with its first',
         'loss_001 = None  # your code here: loss after 30 steps for eta = 0.01\nloss_005 = None  # your code here: eta = 0.05\nloss_02 = None   # your code here: eta = 0.2\ngrew = None      # your code here: True if the eta = 0.2 loss ended higher than it started',
         'loss_001 = curves[0.01][-1]\nloss_005 = curves[0.05][-1]\nloss_02 = curves[0.2][-1]\ngrew = curves[0.2][-1] > curves[0.2][0]')
    b.code('check("loss after 30 steps, eta = 0.01", loss_001, %.4f, 0.01)\ncheck("loss after 30 steps, eta = 0.05", loss_005, %.4f, 0.01)\n'
           'check("loss after 30 steps, eta = 0.2", loss_02, %.2f, 0.1)\ncheck("eta = 0.2 loss grew", grew, 1, 0.01)\n'
           'if loss_02 is not None:\n    print(loss_001, loss_005, loss_02, grew)'
           % (R[0.01]['L'][-1], R[0.05]['L'][-1], R[0.2]['L'][-1]))
    b.read('Which eta makes the loss grow? Why does a step that is too large make the loss bigger? (Think of the bowl picture and overshooting.)')
    b.change('Type a learning rate of your own into the cell below, for example 0.19, which sits close to the limit between falling and growing. Run it and read the losses at steps 0, 10 and 30.')
    b.code(('my_eta = 0.19   # a learning rate close to the limit\n' if solution else 'my_eta = None   # type a learning rate here, for example 0.19\n') +
           'if my_eta is None or curves[0.1] is None:\n    print("Type a number for my_eta (and finish step 4) first.")\n'
           'else:\n    _, _, lk = gradient_descent(my_eta)\n    print([round(lk[k], 4) for k in (0, 10, 30)])')
    b.change('Do not centre the distance: in step 1 replace `x - mean_distance` by `x`, run steps 1 to 5 again and see which etas still work. Write what you saw, then undo the change.')
    b.md('---\n## Finish\n\nRun the cell below. It should say **All checks pass**. Then restart the kernel, run all cells from the top, and save the notebook.')
    b.code('show_checks()')
    return b
