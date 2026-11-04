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


def build(solution):
    n = D.n10()
    R = n['runs']
    b = NB.Notebook()
    b.md('# Session 10: Gradient descent for a line fit\n\n**KLAi | Mathematics for AI and Machine Learning**\n\n'
         'In this lab you fit a line to eight boda boda trips by gradient descent, with your own loop, and you watch what four different learning rates do to the loss. '
         'The same numbers are in the spreadsheet lab. The trip data are illustrative (made-up numbers to show the arithmetic).\n\n'
         'Each step has the same rhythm: **PREDICT**, run, **READ**, then **CHANGE one thing**. A cell that says `None  # your code here` is yours to fill. The check cells say OK or NOT YET.')
    b.check_setup()

    b.step(1, 'Look at the data', 'Each row is one trip: the distance in km and the fare in thousand UGX. Gradient descent works best when the input is centred, so we subtract the mean distance from every distance. '
           'The centred distance is called `xc`.')
    b.predict('The distances run from 1 to 8 km. What is their mean?')
    b.code('import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\n'
           'df = pd.DataFrame({"distance_km": [1, 2, 3, 4, 5, 6, 7, 8],\n'
           '                   "fare": [3.2, 4.1, 5.4, 5.9, 7.6, 8.0, 9.9, 10.3]})   # fare in thousand UGX\n'
           'print(df)')
    todo(b, solution, 'use the mean of the distance column', 'mean_distance = None  # your code here', 'mean_distance = df["distance_km"].mean()')
    b.code('x = df["distance_km"].to_numpy(dtype=float)\ny = df["fare"].to_numpy(dtype=float)\nxc = x - x.mean()      # the centred distance\nn = len(x)\nprint("centred distances:", xc)\nprint("mean distance:", mean_distance)\n'
           'check("mean distance is 4.5", mean_distance, 4.5)')
    b.read('Why do the centred distances run from -3.5 to +3.5? What does a centred distance of 0 mean for a trip?')

    b.step(2, 'The loss and the gradient at the start', 'The model is y-hat = w * xc + b. We start with w = 0 and b = 0. The loss is the mean squared error. '
           'The gradient has two entries: dL/dw = (2/n) * sum(err * xc) and dL/db = (2/n) * sum(err), where err = y-hat - y.')
    b.predict('With w = 0 and b = 0 every prediction is 0. So what is the loss? (Hint: the mean of y squared.)')
    todo(b, solution, 'err is y-hat minus y. Use np.mean for the averages.',
         'w, b = 0.0, 0.0\nerr = w * xc + b - y\nloss0 = None  # your code here: the mean of err squared\ndw0 = None    # your code here: 2 times the mean of err * xc\ndb0 = None    # your code here: 2 times the mean of err',
         'w, b = 0.0, 0.0\nerr = w * xc + b - y\nloss0 = np.mean(err ** 2)\ndw0 = 2 * np.mean(err * xc)\ndb0 = 2 * np.mean(err)')
    b.code('print("loss at the start:", loss0)\nprint("slopes:", dw0, db0)\n'
           'check("loss at w = 0, b = 0", loss0, %.4f, 0.01)\ncheck("dL/dw at the start", dw0, %.4f, 0.01)\ncheck("dL/db at the start", db0, %.4f, 0.01)' % (n['loss0'], n['dw0'], n['db0']))
    b.read('Both slopes are negative. Which way should w and b move to lower the loss?')

    b.step(3, 'One step by hand', 'The update rule is new = old - eta * slope. Use eta = 0.1.')
    b.predict('Will the new w and b be bigger or smaller than 0? Roughly how big?')
    todo(b, solution, 'apply the update rule from the slides to w and to b',
         'eta = 0.1\nw1 = None  # your code here\nb1 = None  # your code here',
         'eta = 0.1\nw1 = w - eta * dw0\nb1 = b - eta * db0')
    b.code('print("after one step:", w1, b1)\n'
           'check("w after one step", w1, %.4f, 0.001)\ncheck("b after one step", b1, %.4f, 0.001)' % (n['w1'], n['b1']))
    b.change('Change eta to 0.2 and run Step 3 again. How do w1 and b1 change? Put eta back to 0.1 before you go on.')

    b.step(4, 'The loop', 'Now we repeat the step 30 times and record the loss at every step. The function below is the loop from the slides. Read it line by line before you run it.')
    b.code('def gradient_descent(eta, steps=30):\n'
           '    w, b = 0.0, 0.0\n'
           '    losses = [np.mean((w * xc + b - y) ** 2)]\n'
           '    for step in range(steps):\n'
           '        err = w * xc + b - y\n'
           '        dw = 2 * np.mean(err * xc)\n'
           '        db = 2 * np.mean(err)\n'
           '        w = w - eta * dw\n'
           '        b = b - eta * db\n'
           '        losses.append(np.mean((w * xc + b - y) ** 2))\n'
           '    return w, b, losses\n\n'
           'w_fit, b_fit, losses = gradient_descent(0.1)\n'
           'print("w =", round(w_fit, 4), " b =", round(b_fit, 4))\n'
           'print("loss at steps 0, 1, 5, 30:", [round(losses[k], 4) for k in (0, 1, 5, 30)])')
    b.read('Is the loss going down at every step? After about how many steps does it stop changing in the first three decimals?')

    b.step(5, 'Four learning rates, four loss curves', 'Run the same loop with eta = 0.01, 0.05, 0.1 and 0.2 and plot the four loss curves. The vertical axis uses a log scale so that all four fit.')
    b.predict('Which curve falls fastest? Which curve will go up instead of down? Write both guesses first.')
    b.code('etas = [0.01, 0.05, 0.1, 0.2]\ncurves = {}\nfor eta_k in etas:\n    wk, bk, lk = gradient_descent(eta_k)\n    curves[eta_k] = lk\n\n'
           'for eta_k in etas:\n    plt.plot(curves[eta_k], label="eta = " + str(eta_k))\nplt.yscale("log")\nplt.xlabel("step")\nplt.ylabel("loss (log scale)")\nplt.legend()\nplt.title("Loss curves for four learning rates")\nplt.show()')
    todo(b, solution, 'each list holds the loss at every step; you want the last entry of each',
         'loss_001 = None  # your code here: loss after 30 steps for eta = 0.01\nloss_005 = None  # your code here: eta = 0.05\nloss_01 = None   # your code here: eta = 0.1\nloss_02 = None   # your code here: eta = 0.2',
         'loss_001 = curves[0.01][-1]\nloss_005 = curves[0.05][-1]\nloss_01 = curves[0.1][-1]\nloss_02 = curves[0.2][-1]')
    b.code('print(loss_001, loss_005, loss_01, loss_02)\n'
           'check("loss after 30 steps, eta = 0.01", loss_001, %.4f, 0.01)\ncheck("loss after 30 steps, eta = 0.05", loss_005, %.4f, 0.01)\n'
           'check("loss after 30 steps, eta = 0.1", loss_01, %.4f, 0.001)\ncheck("loss after 30 steps, eta = 0.2", loss_02, %.2f, 0.1)'
           % (R[0.01]['L'][-1], R[0.05]['L'][-1], R[0.1]['L'][-1], R[0.2]['L'][-1]))
    b.read('Which eta makes the loss grow? Why does a step that is too large make the loss bigger? (Think of the bowl picture and overshooting.)')
    b.change('In step 4, call gradient_descent(0.19) and print its losses at steps 0, 10 and 30. It sits close to the limit between falling and growing. What do you see?')

    b.step(6, 'Compare with the least squares answer', 'In Session 4 you fitted a line directly with least squares. Gradient descent should end close to the same line. '
           'np.polyfit(xc, y, 1) returns the slope and then the intercept.')
    todo(b, solution, 'np.polyfit fits a polynomial; a line is a polynomial of degree 1. It returns the slope first', 'w_ls, b_ls = None, None  # your code here',
         'w_ls, b_ls = np.polyfit(xc, y, 1)')
    b.code('print("least squares: w =", w_ls, " b =", b_ls)\nprint("gradient descent (eta = 0.1, 30 steps): w =", w_fit, " b =", b_fit)\n'
           'check("least squares slope", w_ls, %.3f, 0.01)\ncheck("least squares intercept", b_ls, %.3f, 0.01)\n'
           'check("gradient descent is within 0.01 of the slope", w_fit, w_ls, 0.01)' % (n['w_star'], n['b_star']))
    b.read('The intercept b is the fare for a trip of average length (4.5 km). Is it close to the mean of the fares?')

    b.step(7, 'Which curve grew?', 'One last answer: a number that says whether the eta = 0.2 curve is higher at step 30 than at step 0 (1 means yes).')
    todo(b, solution, 'compare the last loss of the eta = 0.2 curve with its first loss; True counts as 1', 'grew = None  # your code here',
         'grew = curves[0.2][-1] > curves[0.2][0]')
    b.code('print("the eta = 0.2 loss grew:", grew)\ncheck("eta = 0.2 loss grew", grew, 1, 0.01)')
    b.change('Do not centre the distance: replace xc by x in step 2 and in the function, and run the four rates again. Which etas still work? Write what you saw, then undo the change.')
    b.md('---\n## Finish\n\nRun the cell below. It should say **All 14 checks pass**. Then restart the kernel, run all cells from the top, and save the notebook.')
    b.code('show_checks()')
    return b
