"""Session 14 Python lab: binomial, Gaussian, law of large numbers, central limit theorem, confidence interval, A/B test, drawing the next word from its slices."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'kit'))
import nb as NB  # noqa: E402

TITLE = 'Session 14: Distributions and sampling'

ROLLS60 = [6, 6, 5, 6, 1, 5, 6, 2, 2, 1, 5, 6, 4, 4, 5, 1, 6, 6, 1, 6, 6, 2, 3, 5, 6, 1, 4, 3, 3, 5, 5, 3, 6, 4, 6, 1, 6, 5, 4, 3, 2, 2, 2, 5, 3, 6, 3, 4, 3, 5, 3, 6, 4, 1, 6, 4, 5, 6, 2, 1]


def build(solution: bool):
    n = NB.Notebook()

    def todo(sol, learner):
        n.code(sol if solution else learner)

    n.md('# Session 14: Distributions and sampling (Python lab)\n\n'
         'You will calculate binomial and Gaussian probabilities, watch the law of large numbers and the central limit theorem happen, build a confidence interval, run an A/B test, and draw next words at random from their probabilities.\n\n'
         '**How to work.** In each step: read the idea, write a PREDICT guess, run the cell, READ the output, then CHANGE one thing in the experiment cell. Cells with `None  # your code here` are yours to fill. '
         'The automatic checks print OK or NOT YET. Run the cells from the top, in order. Every random step makes its own seeded generator, so your numbers match the slides.')
    n.step(0, 'Set up', 'numpy for numbers, matplotlib for pictures, math for combinations and the error function.')
    n.code('import math\nimport numpy as np\nimport matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\n\n'
           'def Phi(z):\n    """Area under the standard Gaussian curve to the left of z."""\n    return 0.5 * (1 + math.erf(z / math.sqrt(2)))\n\nprint("ready")')
    n.check_setup()

    n.step(1, 'Binomial: ten users, each rates helpful with probability 0.3', 'P(X = k) = (n choose k) p^k (1 - p)^(n - k), where n choose k = n! / (k! (n - k)!) and n! = n × (n - 1) × ... × 1. math.comb(10, 3) gives 120. The users are independent. Illustrative numbers.')
    n.predict('Which count k is the most likely? Roughly what share of 100,000 simulated groups of ten will have exactly 3 helpful ratings?')
    todo('p3 = math.comb(10, 3) * 0.3**3 * 0.7**7                         # P(X = 3) by the formula\n'
         'pmf = [math.comb(10, k) * 0.3**k * 0.7**(10 - k) for k in range(11)]\n'
         'rng = np.random.default_rng(14)\n'
         'draws = rng.binomial(10, 0.3, size=100000)                    # 100,000 simulated groups of ten users\n'
         'sim_p3 = (draws == 3).mean()\n'
         'sim_mean = draws.mean()\n'
         'print(round(p3, 4), round(sum(pmf), 6), round(sim_p3, 4), sim_mean)\n'
         'check("P(X = 3) by formula", p3, 0.2668, 0.0001)\n'
         'check("the pmf adds up to 1", sum(pmf), 1, 0.000001)\n'
         'check("simulated share with exactly 3 is near the formula", sim_p3, 0.2668, 0.01)\n'
         'check("simulated mean is near n p = 3", sim_mean, 3, 0.03)',
         '# Hint: the formula from the slides, with math.comb for the number of ways. The pmf repeats it for every k from 0 to 10.\n'
         'p3 = None  # your code here\n'
         'pmf = None  # your code here: a list of 11 probabilities\n'
         'rng = np.random.default_rng(14)\n'
         'draws = rng.binomial(10, 0.3, size=100000)\n'
         'sim_p3 = None  # your code here: the share of draws equal to 3\n'
         'sim_mean = None  # your code here: the mean number of helpful ratings per group\n'
         'check("P(X = 3) by formula", p3, 0.2668, 0.0001)\n'
         'check("the pmf adds up to 1", None if pmf is None else sum(pmf), 1, 0.000001)\n'
         'check("simulated share with exactly 3 is near the formula", sim_p3, 0.2668, 0.01)\n'
         'check("simulated mean is near n p = 3", sim_mean, 3, 0.03)')
    n.change('Run the experiment cell: P(at most 3 helpful ratings). Predict whether it is about 0.27, 0.65 or 0.95 first.')
    n.code('print("P(X <= 3) =", round(sum(math.comb(10, k) * 0.3**k * 0.7**(10 - k) for k in range(4)), 4))')

    n.step(2, 'Gaussian: quiz scores with mean 60 and standard deviation 10', 'Illustrative numbers. The z-score is (x - mu) / sigma. `Phi(z)` from Step 0 gives the area to the left.')
    n.predict('About what share of learners score below 75? About what share score between 50 and 70?')
    todo('z75 = (75 - 60) / 10\n'
         'p75 = Phi(z75)                          # P(X < 75)\n'
         'p_mid = Phi(1) - Phi(-1)                # P(50 < X < 70)\n'
         'scores = np.random.default_rng(14).normal(60, 10, size=100000)\n'
         'sim75 = (scores < 75).mean()\n'
         'print(z75, round(p75, 4), round(p_mid, 4), round(sim75, 4))\n'
         'check("z-score of 75", z75, 1.5, 0.0001)\n'
         'check("P(X < 75)", p75, 0.9332, 0.0001)\n'
         'check("P(50 < X < 70)", p_mid, 0.6827, 0.0001)\n'
         'check("simulated share below 75 is near the formula", sim75, 0.9332, 0.01)',
         '# Hint: Phi(z) is the area to the left of z. For the area between two values, think of subtracting one area from another.\n'
         'z75 = None  # your code here\n'
         'p75 = None  # your code here\n'
         'p_mid = None  # your code here\n'
         'scores = np.random.default_rng(14).normal(60, 10, size=100000)\n'
         'sim75 = None  # your code here\n'
         'check("z-score of 75", z75, 1.5, 0.0001)\n'
         'check("P(X < 75)", p75, 0.9332, 0.0001)\n'
         'check("P(50 < X < 70)", p_mid, 0.6827, 0.0001)\n'
         'check("simulated share below 75 is near the formula", sim75, 0.9332, 0.01)')
    n.change('Run the experiment cell: the share within 2 standard deviations of the mean, between 40 and 80. Predict it first (the slides say about 95%).')
    n.code('print("P(40 < X < 80) =", round(Phi(2) - Phi(-2), 4))')

    n.step(3, 'Law of large numbers and the central limit theorem', 'Roll a die many times and watch the running average settle. Then average 30 dice, 20,000 times, and see the bell shape. The standard deviation of one die is sqrt(35/12) = 1.7078.')
    n.predict('How close to 3.5 is the average after 10,000 rolls? What will the standard deviation of the averages of 30 dice be? (standard deviation of one die divided by the square root of 30)')
    todo('rolls = np.random.default_rng(14).integers(1, 7, size=10000)\n'
         'running = np.cumsum(rolls) / np.arange(1, 10001)      # the average after each roll\n'
         'rng = np.random.default_rng(14)\n'
         'means = rng.integers(1, 7, size=(20000, 30)).mean(axis=1)   # 20,000 averages of 30 dice\n'
         'se_theory = (35 / 12) ** 0.5 / math.sqrt(30)           # standard error from the formula\n'
         'se_sim = means.std(ddof=1)                             # a sample of 20,000 averages: ddof=1\n'
         'first12 = means[:12]                                    # the 12 samples that the workbook uses\n'
         'mean_means = means.mean()\n'
         'print(round(running[9], 2), round(running[99], 2), round(running[-1], 3), round(se_theory, 4), round(se_sim, 4), round(means.mean(), 4))\n'
         'check("running average after 10,000 rolls is near 3.5", running[-1], 3.5, 0.05)\n'
         'check("standard error from the formula", se_theory, 0.3118, 0.0001)\n'
         'check("simulated standard deviation of the 30-dice averages", se_sim, 0.3118, 0.01)\n'
         'check("mean of the 30-dice averages is near 3.5", mean_means, 3.5, 0.01)\n'
         'check("mean of the first 12 averages (the workbook samples)", first12.mean(), 3.3972, 0.0005)\n'
         'check("sample standard deviation of the first 12 averages", first12.std(ddof=1), 0.3748, 0.0005)',
         '# Hint: np.cumsum(rolls) gives the total so far after each roll; divide it by np.arange(1, 10001), the number of rolls so far. The standard error formula is on the slides. Use ddof=1 for the standard deviation of the averages.\n'
         'rolls = np.random.default_rng(14).integers(1, 7, size=10000)\n'
         'running = None  # your code here\n'
         'rng = np.random.default_rng(14)\n'
         'means = rng.integers(1, 7, size=(20000, 30)).mean(axis=1)\n'
         'se_theory = None  # your code here\n'
         'se_sim = None  # your code here: the sample standard deviation of means\n'
         'first12 = None  # your code here: the first 12 of the 20,000 averages\n'
         'mean_means = None  # your code here: the mean of all 20,000 averages\n'
         'check("running average after 10,000 rolls is near 3.5", None if running is None else running[-1], 3.5, 0.05)\n'
         'check("standard error from the formula", se_theory, 0.3118, 0.0001)\n'
         'check("simulated standard deviation of the 30-dice averages", se_sim, 0.3118, 0.01)\n'
         'check("mean of the 30-dice averages is near 3.5", mean_means, 3.5, 0.01)\n'
         'check("mean of the first 12 averages (the workbook samples)", None if first12 is None else first12.mean(), 3.3972, 0.0005)\n'
         'check("sample standard deviation of the first 12 averages", None if first12 is None else first12.std(ddof=1), 0.3748, 0.0005)')
    n.code('xs = np.linspace(2.2, 4.8, 200)\nplt.figure(figsize=(6, 3))\nplt.hist(means, bins=40, density=True, color="#E0BE36", edgecolor="black")\n'
           'plt.plot(xs, np.exp(-0.5 * ((xs - 3.5) / 0.3118) ** 2) / (0.3118 * math.sqrt(2 * math.pi)), color="#AE2525")\n'
           'plt.xlabel("average of 30 dice")\nplt.savefig("s14_clt.png", dpi=80)\nprint("histogram saved")')
    n.read('How well does the red Gaussian curve follow the histogram? A single die is flat. Why are the averages bell shaped?')
    n.change('Run the experiment cell: averages of 120 dice instead of 30. Predict the standard error first (four times the data).')
    n.code('m120 = np.random.default_rng(14).integers(1, 7, size=(20000, 120)).mean(axis=1)\nprint(round(m120.std(), 4), round((35 / 12) ** 0.5 / math.sqrt(120), 4))')

    n.step(4, 'Confidence interval, then an A/B test', 'First the 60 fixed rolls from Session 13: a 95% interval is the mean plus or minus 1.96 standard errors, with s the sample standard deviation (ddof=1). '
           'Then illustrative A/B counts: A 288 of 2,400 rated helpful, B 336 of 2,400.')
    n.predict('Will the 95% interval from the 60 rolls contain the true mean 3.5? Will the A/B p-value be below 0.05?')
    n.code(f'rolls60 = np.array({ROLLS60})\nxa, na, xb, nb = 288, 2400, 336, 2400\nprint(len(rolls60), "rolls;", na, "and", nb, "users")')
    todo('m60 = rolls60.mean()\n'
         's60 = rolls60.std(ddof=1)                         # sample standard deviation (divide by n - 1)\n'
         'se60 = s60 / math.sqrt(60)\n'
         'ci_lo, ci_hi = m60 - 1.96 * se60, m60 + 1.96 * se60\n'
         'check("sample standard deviation of the 60 rolls", s60, 1.7847, 0.0005)\n'
         'check("interval of the 60 rolls, lower end", ci_lo, 3.515, 0.001)\n'
         'check("interval of the 60 rolls, upper end", ci_hi, 4.418, 0.001)\n'
         'print(round(s60, 4), round(ci_lo, 3), round(ci_hi, 3))',
         '# Hint: s60 is the standard deviation with ddof=1. The standard error is s60 divided by the square root of 60. Then go 1.96 standard errors each side of the mean.\n'
         's60 = None  # your code here\n'
         'ci_lo, ci_hi = None, None  # your code here\n'
         'check("sample standard deviation of the 60 rolls", s60, 1.7847, 0.0005)\n'
         'check("interval of the 60 rolls, lower end", ci_lo, 3.515, 0.001)\n'
         'check("interval of the 60 rolls, upper end", ci_hi, 4.418, 0.001)')
    todo('pa, pb = xa / na, xb / nb\n'
         'pooled = (xa + xb) / (na + nb)\n'
         'se_ab = math.sqrt(pooled * (1 - pooled) * (1 / na + 1 / nb))\n'
         'z = (pb - pa) / se_ab\n'
         'p_value = 2 * (1 - Phi(abs(z)))                    # two-sided\n'
         'se_diff = math.sqrt(pa * (1 - pa) / na + pb * (1 - pb) / nb)\n'
         'gap_lo, gap_hi = (pb - pa) - 1.96 * se_diff, (pb - pa) + 1.96 * se_diff\n'
         'check("A/B pooled rate", pooled, 0.13, 0.0001)\n'
         'check("A/B standard error under the null", se_ab, 0.009708, 0.00002)\n'
         'check("A/B test z statistic", z, 2.0601, 0.001)\n'
         'check("A/B test two-sided p-value", p_value, 0.0394, 0.0005)\n'
         'check("interval for the gap, lower end", gap_lo, 0.0010, 0.0002)\n'
         'check("interval for the gap, upper end", gap_hi, 0.0390, 0.0002)\n'
         'print(round(z, 3), round(p_value, 4), round(gap_lo, 4), round(gap_hi, 4))',
         '# Hint: follow steps 1 to 6 of the A/B table on the slides, one line each. The test pools the two groups; the interval for the gap does not.\n'
         'pa, pb = xa / na, xb / nb\n'
         'pooled = None  # your code here: (288 + 336) / (2400 + 2400)\n'
         'se_ab = None  # your code here: the standard error under the null, from pooled\n'
         'z = None  # your code here\n'
         'p_value = None  # your code here: two-sided, use Phi\n'
         'se_diff = None  # your code here: square root of pa(1-pa)/na + pb(1-pb)/nb\n'
         'gap_lo, gap_hi = None, None  # your code here\n'
         'check("A/B pooled rate", pooled, 0.13, 0.0001)\n'
         'check("A/B standard error under the null", se_ab, 0.009708, 0.00002)\n'
         'check("A/B test z statistic", z, 2.0601, 0.001)\n'
         'check("A/B test two-sided p-value", p_value, 0.0394, 0.0005)\n'
         'check("interval for the gap, lower end", gap_lo, 0.0010, 0.0002)\n'
         'check("interval for the gap, upper end", gap_hi, 0.0390, 0.0002)')
    n.read('The interval from the 60 rolls is just above 3.5. We know the true mean is 3.5. What does that tell you about a 95% interval? Is the A/B effect convincing, given the interval for the gap?')
    n.change('Run the experiment cell: the same rates with 4 times the users (9,600 each). Predict whether the p-value gets smaller or larger.')
    n.code('na2 = nb2 = 9600\nse2 = math.sqrt(0.13 * 0.87 * (1 / na2 + 1 / nb2))\nz2 = 0.02 / se2\nprint(round(z2, 3), round(2 * (1 - Phi(z2)), 6))')

    n.step(5, 'Draw the next word: slices and random numbers', 'The next-word list of Session 13 (illustrative). Each word owns a slice of 0 to 1 as wide as its probability; the slice edges are the running totals. '
           'A random number u picks the first word whose running total reaches u. The helper `draw` below does that for a list of u values.')
    n.predict('Which word owns the biggest slice? In 8 draws, about how many times do you expect tea?')
    n.code('words = ["tea", "coffee", "water", "milk", "soup"]\nz = np.array([3.0, 2.6, 1.9, 1.2, 0.4])\ne = np.exp(z - z.max())\np1 = e / e.sum()                       # stable softmax (Session 12)\n'
           'u = np.random.default_rng(19).random(8)  # eight fixed random numbers\n\n'
           'def draw(cum, us):\n    """For each u, the first word whose running total reaches u."""\n    return [words[i] for i in np.searchsorted(cum, us)]\n\nprint(np.round(p1, 4), np.round(u, 3))')
    todo('cum = np.cumsum(p1)                               # slice edges\n'
         'drawn = draw(cum, u)\n'
         'tea_count = drawn.count("tea")\n'
         'many = np.random.default_rng(19).choice(5, p=p1, size=100000)\n'
         'share_tea = (many == 0).mean()                   # share of tea in 100,000 draws\n'
         'check("running total after coffee", cum[1], 0.7448, 0.0005)\n'
         'check("the second draw is milk (1 = yes)", int(drawn[1] == "milk"), 1, 0)\n'
         'check("tea in the 8 draws", tea_count, 4, 0)\n'
         'check("share of tea in 100,000 draws is near its probability", share_tea, 0.4459, 0.01)\n'
         'print(np.round(cum, 4), drawn, round(share_tea, 4))',
         '# Hint: np.cumsum(p1) gives the slice edges. Pass them and u to draw. A list counts its items with .count("tea").\n'
         'cum = None  # your code here\n'
         'drawn = None  # your code here\n'
         'tea_count = None  # your code here\n'
         'many = np.random.default_rng(19).choice(5, p=p1, size=100000)\n'
         'share_tea = None  # your code here: the share of the 100,000 draws equal to 0 (tea)\n'
         'check("running total after coffee", None if cum is None else cum[1], 0.7448, 0.0005)\n'
         'check("the second draw is milk (1 = yes)", None if drawn is None else int(drawn[1] == "milk"), 1, 0)\n'
         'check("tea in the 8 draws", tea_count, 4, 0)\n'
         'check("share of tea in 100,000 draws is near its probability", share_tea, 0.4459, 0.01)')
    n.read('Which u gave milk, and why? Why does the same question give different words when u changes? Why is the share of tea in 100,000 draws so close to 0.446?')
    n.change('Run the experiment cell: eight new random numbers (seed 20). Predict whether tea still appears about half the time.')
    n.code('u2 = np.random.default_rng(20).random(8)\nprint(np.round(u2, 3), draw(np.cumsum(p1), u2))')

    n.step(6, 'Show the checks', 'Run this last cell. A learner who has filled every answer sees "All 27 checks pass".')
    n.code('show_checks()')
    return n
