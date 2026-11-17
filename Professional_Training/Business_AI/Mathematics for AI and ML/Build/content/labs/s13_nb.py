"""Session 13 Python lab: dice, expectation and variance, next-word probabilities, covariance and correlation."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'kit'))
import nb as NB  # noqa: E402

TITLE = 'Session 13: Probability basics'

ROLLS60 = [6, 6, 5, 6, 1, 5, 6, 2, 2, 1, 5, 6, 4, 4, 5, 1, 6, 6, 1, 6, 6, 2, 3, 5, 6, 1, 4, 3, 3, 5, 5, 3, 6, 4, 6, 1, 6, 5, 4, 3, 2, 2, 2, 5, 3, 6, 3, 4, 3, 5, 3, 6, 4, 1, 6, 4, 5, 6, 2, 1]


def build(solution: bool):
    n = NB.Notebook()

    def todo(sol, learner):
        n.code(sol if solution else learner)

    n.md('# Session 13: Probability basics (Python lab)\n\n'
         'You will roll dice, calculate an expectation and a variance, turn scores into next-word probabilities and an expected surprise, and calculate a sample covariance and a correlation.\n\n'
         '**How to work.** In each step: read the idea, write a PREDICT guess, run the cell, READ the output, then CHANGE one thing. Cells with `None  # your code here` are yours to fill. '
         'The automatic checks print OK or NOT YET. Run the cells from the top, in order.\n\n'
         'The numbers on the slides (check your numbers table) are the numbers you should see.')
    n.step(0, 'Set up', 'We use numpy for the numbers, pandas for a small table and matplotlib for pictures. Run the cell, then the check helper below it.')
    n.code('import numpy as np\nimport pandas as pd\nimport matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\nprint("numpy", np.__version__)')
    n.check_setup()

    # ------------------------------------------------------------ step 1
    n.step(1, 'Two dice: a sample space and an event', 'The sample space of two dice has 36 equally likely outcomes. The table `sums` holds the sum of each outcome (rows: die 2, columns: die 1). You will compute P(sum is 7), and also P(sum is 2 or 12): the share of outcomes that give one of the two extreme sums.')
    n.predict('How many of the 36 outcomes have a sum of exactly 7? Then what is P(sum is 7)?')
    n.code('faces = np.arange(1, 7)\nsums = np.add.outer(faces, faces)      # 6 by 6 table of sums\nprint(sums)')
    todo('count7 = int((sums == 7).sum())          # how many cells equal 7\n'
         'p7 = count7 / 36                         # probability of the event\n'
         'p_2_or_12 = ((sums == 2) | (sums == 12)).sum() / 36   # CHANGE task: the two extreme sums\n'
         'print(count7, round(p7, 4), round(p_2_or_12, 4))\n'
         'check("number of outcomes with sum 7", count7, 6, 0)\n'
         'check("P(sum is 7)", p7, 1/6, 0.0001)\n'
         'check("P(sum is 2 or 12)", p_2_or_12, 2/36, 0.0001)',
         '# Hint: comparing the table with a number gives True or False for each cell. Count the True cells.\n'
         'count7 = None  # your code here\n'
         'p7 = None  # your code here: the share of all 36 outcomes\n'
         'p_2_or_12 = None  # your code here: the share of outcomes that give the smallest or the largest sum\n'
         'check("number of outcomes with sum 7", count7, 6, 0)\n'
         'check("P(sum is 7)", p7, 1/6, 0.0001)\n'
         'check("P(sum is 2 or 12)", p_2_or_12, 2/36, 0.0001)')
    n.change('Predict P(sum is 8) before you run the experiment cell below, and say whether it is larger or smaller than P(sum is 7). Then run it. Also say why P(sum is 2 or 12) in the cell above is much smaller than P(sum is 7).')
    n.code('print("P(sum is 8) =", round((sums == 8).sum() / 36, 4))')

    # ------------------------------------------------------------ step 2
    n.step(2, 'One fair die: expectation and variance by formula', 'For a random variable X with probability mass function p(x): E(X) = sum of x p(x), and Var(X) = sum of (x - E(X)) squared times p(x).')
    n.predict('What will E(X) be for a fair die? Will it be a value you can roll?')
    todo('x = np.arange(1, 7)                 # the six faces\n'
         'p = np.full(6, 1 / 6)                 # each face has probability 1/6\n'
         'e_x = (x * p).sum()                   # expectation\n'
         'var_x = ((x - e_x) ** 2 * p).sum()    # variance\n'
         'sd_x = np.sqrt(var_x)                 # standard deviation\n'
         'print(e_x, round(var_x, 4), round(sd_x, 4))\n'
         'check("E(X) of a fair die", e_x, 3.5, 0.0001)\n'
         'check("Var(X) of a fair die", var_x, 35/12, 0.0001)\n'
         'check("standard deviation of a fair die", sd_x, (35/12) ** 0.5, 0.0001)',
         'x = np.arange(1, 7)                 # the six faces\n'
         'p = np.full(6, 1 / 6)                 # each face has probability 1/6\n'
         '# Hint: weight each face by its probability and add up. For the variance, weight each squared distance from E(X) the same way. The standard deviation is the square root of the variance.\n'
         'e_x = None  # your code here\n'
         'var_x = None  # your code here\n'
         'sd_x = None  # your code here\n'
         'check("E(X) of a fair die", e_x, 3.5, 0.0001)\n'
         'check("Var(X) of a fair die", var_x, 35/12, 0.0001)\n'
         'check("standard deviation of a fair die", sd_x, (35/12) ** 0.5, 0.0001)')
    n.read('E(X) is 3.5, yet no face shows 3.5. In one sentence, what does the expectation mean?')
    n.change('A loaded die gives the face 6 a probability of 0.5 and each other face 0.1. Predict whether E(X) goes up or down, then run the experiment cell below. It has no checks.')
    n.code('p_loaded = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.5])\nprint("probabilities add up to", p_loaded.sum(), "and E(X) =", (x * p_loaded).sum())')

    # ------------------------------------------------------------ step 3
    n.step(3, 'Simulation: let the computer roll the dice', 'We use 60 fixed rolls (the same ones are in the spreadsheet), then 10,000 rolls from a random number generator with a fixed seed. Rolls are sample data, so their variance divides by n - 1 (ddof=1).')
    n.predict('Will the mean of 60 rolls be exactly 3.5? Will the mean of 10,000 rolls be closer to 3.5 than the mean of 60?')
    n.code('# These 60 rolls came from np.random.default_rng(13).integers(1, 7, size=60). They are typed in so the spreadsheet has the same rolls.\n'
           f'rolls60 = np.array({ROLLS60})\n'
           'print(len(rolls60), "rolls; faces 1 to 6 appeared", np.bincount(rolls60, minlength=7)[1:], "times")')
    todo('mean60 = rolls60.mean()\n'
         'var60 = rolls60.var(ddof=1)            # sample variance: ddof=1 divides by n - 1\n'
         'rng = np.random.default_rng(13)\n'
         'big = rng.integers(1, 7, size=10000)   # 10,000 simulated rolls\n'
         'mean_big, var_big = big.mean(), big.var(ddof=1)\n'
         'print(round(mean60, 4), round(var60, 4), round(mean_big, 4), round(var_big, 4))\n'
         'check("mean of the 60 fixed rolls", mean60, 3.9667, 0.0001)\n'
         'check("sample variance of the 60 fixed rolls (n - 1)", var60, 3.1853, 0.0001)\n'
         'check("mean of 10,000 rolls is near 3.5", mean_big, E_FORMULA, 0.05)\n'
         'check("sample variance of 10,000 rolls is near 2.9167", var_big, V_FORMULA, 0.05)'.replace('E_FORMULA', '3.5').replace('V_FORMULA', '35/12'),
         '# Hint: numpy arrays have methods for the mean and the variance. The rolls are a sample, so pass ddof=1 to the variance (divide by n - 1). The 10,000 rolls are already in the array big.\n'
         'mean60 = None  # your code here\n'
         'var60 = None  # your code here\n'
         'rng = np.random.default_rng(13)\n'
         'big = rng.integers(1, 7, size=10000)\n'
         'mean_big, var_big = None, None  # your code here\n'
         'check("mean of the 60 fixed rolls", mean60, 3.9667, 0.0001)\n'
         'check("sample variance of the 60 fixed rolls (n - 1)", var60, 3.1853, 0.0001)\n'
         'check("mean of 10,000 rolls is near 3.5", mean_big, 3.5, 0.05)\n'
         'check("sample variance of 10,000 rolls is near 2.9167", var_big, 35/12, 0.05)')
    n.code('freq = np.bincount(big, minlength=7)[1:] / len(big)\nplt.figure(figsize=(6, 3))\nplt.bar(np.arange(1, 7), freq, color="#E0BE36", edgecolor="black")\n'
           'plt.axhline(1 / 6, color="#AE2525", linestyle="--", label="1/6")\nplt.xlabel("face")\nplt.ylabel("share of 10,000 rolls")\nplt.legend()\nplt.savefig("s13_dice.png", dpi=80)\nprint(np.round(freq, 3))')
    n.read('How close is each bar to 1/6 = 0.167? Which is closer to 3.5, the 60 rolls or the 10,000 rolls?')
    n.change('Roll only 100 dice with the same seed and look at the mean and the variance. Run the experiment cell below, then change 100 to 1000. What happens to the numbers?')
    n.code('small = np.random.default_rng(13).integers(1, 7, size=100)\nprint(small.mean(), small.var(ddof=1))')

    # ------------------------------------------------------------ step 4
    n.step(4, 'A next-word probability mass function and its expected surprise', 'Illustrative (made-up numbers to show the arithmetic): after "For breakfast I drink hot" a model gives these logits to five words. Softmax (Session 12) turns logits into probabilities. '
           'The surprise of a word is -ln p (ln from Session 1, unit: nats). The expected surprise is E(g(X)) = sum of g(x) p(x) with g(x) = -ln p(x).')
    n.predict('Which word gets the highest probability? Which word has the largest surprise? What must the five probabilities add up to?')
    todo('words = ["tea", "coffee", "water", "milk", "soup"]\n'
         'logits = np.array([3.0, 2.6, 1.9, 1.2, 0.4])\n'
         'e = np.exp(logits - logits.max())                # stable softmax: subtract the largest logit\n'
         'p_next = e / e.sum()\n'
         'surprise = -np.log(p_next)                       # surprise of each word, in nats\n'
         'e_surp = (p_next * surprise).sum()               # expected surprise\n'
         'check("probability of tea", p_next[0], 0.4459, 0.0005)\n'
         'check("probabilities add up to 1", p_next.sum(), 1, 0.000001)\n'
         'check("expected surprise in nats", e_surp, 1.3093, 0.0005)\n'
         'print(dict(zip(words, np.round(p_next, 4))), np.round(surprise, 4), round(e_surp, 4))',
         'words = ["tea", "coffee", "water", "milk", "soup"]\n'
         'logits = np.array([3.0, 2.6, 1.9, 1.2, 0.4])\n'
         '# Hint: use the stable softmax from Session 12 on the logits. np.log is ln. Weight each surprise by its probability and add.\n'
         'p_next = None  # your code here\n'
         'surprise = None  # your code here: -ln of each probability\n'
         'e_surp = None  # your code here\n'
         'check("probability of tea", None if p_next is None else p_next[0], 0.4459, 0.0005)\n'
         'check("probabilities add up to 1", None if p_next is None else p_next.sum(), 1, 0.000001)\n'
         'check("expected surprise in nats", e_surp, 1.3093, 0.0005)')
    n.read('The probabilities add to exactly 1. Why must they? Soup has the largest surprise. Why?')
    n.change('Give "soup" a logit of 3.0 instead of 0.4. Predict which probabilities go down, and whether the expected surprise goes up or down, then run the experiment cell below.')
    n.code('logits2 = logits.copy()\nlogits2[4] = 3.0\ne2 = np.exp(logits2 - logits2.max())\np2 = e2 / e2.sum()\nprint(dict(zip(words, np.round(p2, 4))), "expected surprise:", round(float((p2 * -np.log(p2)).sum()), 4))')

    # ------------------------------------------------------------ step 5
    n.step(5, 'Two columns: sample covariance and correlation', 'Illustrative data: six learners, hours of study per week (x) and a quiz score out of 10 (y). The six learners are a sample, so the covariance adds the products of the distances from the means and divides by n - 1. Correlation divides it by both sample standard deviations.')
    n.predict('Do you expect a positive or a negative covariance? Will the correlation be near 0, near 1 or near -1?')
    n.code('data = pd.DataFrame({"hours": [1, 2, 3, 5, 6, 7], "score": [4, 2, 8, 5, 7, 10]})\nprint(data)\nx = data["hours"].to_numpy(dtype=float)\ny = data["score"].to_numpy(dtype=float)\nprint("means:", x.mean(), y.mean())')
    todo('cov_xy = ((x - x.mean()) * (y - y.mean())).sum() / (len(x) - 1)   # sample covariance: divide by n - 1\n'
         'var_x2, var_y = x.var(ddof=1), y.var(ddof=1)                     # sample variances\n'
         'corr = cov_xy / (np.sqrt(var_x2) * np.sqrt(var_y))\n'
         'cov_pop = ((x - x.mean()) * (y - y.mean())).mean()               # CHANGE task: population form, divide by n\n'
         'check("sample covariance of x and y (n - 1)", cov_xy, 5, 0.0001)\n'
         'check("sample variance of x", var_x2, 5.6, 0.0001)\n'
         'check("sample variance of y", var_y, 8.4, 0.0001)\n'
         'check("correlation of x and y", corr, 0.7290, 0.0005)\n'
         'check("population covariance (divide by n)", cov_pop, 25/6, 0.0001)\n'
         'print(round(cov_xy, 4), round(var_x2, 4), round(var_y, 4), round(corr, 4), round(cov_pop, 4))\n'
         'print("numpy agrees:", np.cov(x, y)[0, 1], np.corrcoef(x, y)[0, 1])',
         '# Hint: for every row multiply the distance of x from its mean by the distance of y from its mean. Add the products and divide by n - 1.\n'
         'cov_xy = None  # your code here\n'
         'var_x2 = None  # your code here: sample variance, ddof=1\n'
         'var_y = None  # your code here\n'
         'corr = None  # your code here: covariance divided by both standard deviations\n'
         'cov_pop = None  # your code here: the same products, divided by n instead\n'
         'check("sample covariance of x and y (n - 1)", cov_xy, 5, 0.0001)\n'
         'check("sample variance of x", var_x2, 5.6, 0.0001)\n'
         'check("sample variance of y", var_y, 8.4, 0.0001)\n'
         'check("correlation of x and y", corr, 0.7290, 0.0005)\n'
         'check("population covariance (divide by n)", cov_pop, 25/6, 0.0001)')
    n.read('The covariance is in "hours times points". The correlation has no units. Which one would you quote to a colleague, and why? Did the correlation change when you divided by n?')
    n.change('Reverse the scores, so that the learner who studied least gets the highest score. Predict the sign of the covariance first, then run the experiment cell below.')
    n.code('y_rev = y[::-1]\nprint("sample covariance:", np.cov(x, y_rev)[0, 1])\nprint("correlation:", np.corrcoef(x, y_rev)[0, 1])')

    n.step(6, 'Show the checks', 'Run this last cell. A learner who has filled every answer sees "All 18 checks pass".')
    n.code('show_checks()')
    return n
