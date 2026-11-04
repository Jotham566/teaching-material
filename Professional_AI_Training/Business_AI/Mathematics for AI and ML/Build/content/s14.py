"""Session 14: Distributions and sampling. Bernoulli, binomial, Gaussian, the central limit theorem, confidence intervals, an A/B test, temperature and top-p sampling."""
import sys
from math import comb, erf, sqrt
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'kit'))
import diagrams_math_e  # noqa: E402,F401

PHI = lambda z: 0.5 * (1 + erf(z / sqrt(2)))

# ---------------------------------------------------------------- numbers
N_B, P_B = 10, 0.3
BIN = [comb(N_B, k) * P_B ** k * (1 - P_B) ** (N_B - k) for k in range(N_B + 1)]
MU_Q, SD_Q = 60, 10
Z75 = (75 - MU_Q) / SD_Q
P_LT75 = PHI(Z75)
P_50_70 = PHI(1) - PHI(-1)

SD_DIE = (35 / 12) ** 0.5
ROLLS60 = np.array([6, 6, 5, 6, 1, 5, 6, 2, 2, 1, 5, 6, 4, 4, 5, 1, 6, 6, 1, 6, 6, 2, 3, 5, 6, 1, 4, 3, 3, 5, 5, 3, 6, 4, 6, 1, 6, 5, 4, 3, 2, 2, 2, 5, 3, 6, 3, 4, 3, 5, 3, 6, 4, 1, 6, 4, 5, 6, 2, 1])
M60 = float(ROLLS60.mean())
S60 = float(ROLLS60.std(ddof=1))
SE60 = S60 / sqrt(60)
CI60 = (M60 - 1.96 * SE60, M60 + 1.96 * SE60)

XA, NA, XB, NB = 288, 2400, 336, 2400
PA, PB = XA / NA, XB / NB
PPOOL = (XA + XB) / (NA + NB)
SE_AB = sqrt(PPOOL * (1 - PPOOL) * (1 / NA + 1 / NB))
Z_AB = (PB - PA) / SE_AB
P_AB = 2 * (1 - PHI(abs(Z_AB)))
SE_DIFF = sqrt(PA * (1 - PA) / NA + PB * (1 - PB) / NB)
CI_DIFF = (PB - PA - 1.96 * SE_DIFF, PB - PA + 1.96 * SE_DIFF)

WORDS = ['tea', 'coffee', 'water', 'milk', 'soup']
LOGITS = np.array([3.0, 2.6, 1.9, 1.2, 0.4])


def softmax(z, T=1.0):
    e = np.exp((z - z.max()) / T)
    return e / e.sum()


P_T = {T: softmax(LOGITS, T) for T in (0.5, 1.0, 2.0)}
CUM1 = np.cumsum(P_T[1.0])
TOP_P = 0.8
KEEP = [True, True, True, False, False]            # smallest set with cumulative probability at least 0.8
P_NUC = np.where(KEEP, P_T[1.0], 0.0)
P_NUC = P_NUC / P_NUC.sum()
U = np.random.default_rng(19).random(8)


def pick(u, p):
    return WORDS[int(np.searchsorted(np.cumsum(p), u))]


def sim_data():
    rng = np.random.default_rng(14)
    ci = []
    S = rng.integers(1, 7, (20, 30))
    for row in S:
        m, se = row.mean(), row.std(ddof=1) / sqrt(30)
        ci.append([float(m - 1.96 * se), float(m + 1.96 * se), float(m)])
    return ci


CI_SIM = sim_data()
N_MISS = sum(1 for a, b, m in CI_SIM if a > 3.5 or b < 3.5)
CI_LO = float(np.floor(min(a for a, b, m in CI_SIM) * 4) / 4) - 0.1
CI_HI = float(np.ceil(max(b for a, b, m in CI_SIM) * 4) / 4) + 0.1


def lln_series(seed):
    rolls = np.random.default_rng(seed).integers(1, 7, 10000)
    rm = np.cumsum(rolls) / np.arange(1, 10001)
    ns = sorted(set(int(v) for v in np.logspace(0, 4, 90)))
    return dict(ns=ns, vals=[float(rm[n - 1]) for n in ns])


def hist_panels():
    rng = np.random.default_rng(14)
    out = []
    for n, bw in ((1, 1.0), (2, 0.5), (5, 0.2), (30, 0.1)):
        m = rng.integers(1, 7, (20000, n)).mean(1)
        edges = np.arange(1 - bw / 2, 6 + bw / 2 + 1e-9, bw)
        cent = (edges[:-1] + edges[1:]) / 2
        h, _ = np.histogram(m, bins=edges)
        out.append(dict(title=f'Mean of {n}' + (' die' if n == 1 else ' dice'), x=[float(c) for c in cent], h=[float(v) / 20000 / bw for v in h], width=bw, lo=0.7, hi=6.3,
                        mu=(3.5 if n > 1 else None), sigma=float(SD_DIE / sqrt(n)), ticks=[2, 3.5, 5], gold=(n == 30)))
    return out


def gauss_points():
    rng = np.random.default_rng(14)
    return [[float(a), float(b)] for a, b in rng.multivariate_normal([4, 6], [[28 / 6, 25 / 6], [25 / 6, 7]], 150)]


COV_M = np.array([[28 / 6, 25 / 6], [25 / 6, 7]])
EIG = np.linalg.eigvalsh(COV_M)


def build():
    tw = lambda p: ', '.join(f'{v:.3f}' for v in p)
    s = dict(
        num=14, block='Probability and statistics', short_title='Distributions and sampling',
        title='Distributions and sampling: Gaussian, central limit theorem, A/B tests and temperature',
        question='Why can the same question get a different answer from a chat model, and how do we test whether a new AI feature is better?',
        outcomes=['Describe the Bernoulli, binomial and Gaussian distributions, and the multivariate Gaussian as a picture',
                  'Explain the law of large numbers, the central limit theorem, standard error and a confidence interval, and run a two-proportion A/B test',
                  'Calculate softmax with temperature and a top-p cut on toy logits, and sample the next word from the result'],
        outcome_icons=['chart', 'calculator', 'speech'],
        outcome_note=('Today you leave able to do three things. First, describe the Bernoulli, binomial and Gaussian distributions, and picture the multivariate Gaussian. '
                      'Second, explain the law of large numbers, the central limit theorem, the standard error and a confidence interval, and run an A/B test. '
                      'Third, calculate softmax with temperature and a top-p cut on toy logits, and sample a next word. That third skill answers why a chat model can give different answers to the same question.'),
        clock=[(10, 'Recall and a real question from AI'), (35, 'Concept: a picture, then a hand example'), (10, 'Break'), (45, 'Lab: Python or spreadsheet, predict, run, change one thing'),
               (15, 'Where it appears in AI, plus an exit check'), (5, 'Save the work')],
        plan_title='Your two hours: distributions, tests, then sampling words',
        plan_caption='Pictures and hand calculations first. Then the lab on sampling, averages and temperature.',
        plan_note=('The first ten minutes recall Session 13 and introduce the question about different answers. Then thirty-five minutes of concepts, with a picture first and a hand example after it. '
                   'After the break you have forty-five minutes in the lab, in Python or in a spreadsheet, on the same numbers. We finish with where this appears in AI, an exit check and saving your work.'),
        recall_from='Session 13',
        recall=[('The probabilities of all possible next words must add up to what number, and which rule says so?', 'To 1. The total rule: all outcomes together have probability 1.'),
                ('What is the expectation of a fair die, and what does it mean?', '3.5. It is the probability-weighted average over many rolls. No single roll shows it.'),
                ('What is the difference between covariance and correlation?', 'Covariance has units. Correlation divides by both standard deviations, has no units and lies between -1 and +1.')],
        words=[('Gaussian (normal) distribution', 'The bell curve, set by its mean mu and standard deviation sigma.'),
               ('Central limit theorem', 'Averages of many independent values are close to Gaussian, whatever the original shape.'),
               ('Standard error and confidence interval', 'The standard deviation of a sample mean, and a range built from it that usually captures the true value.'),
               ('Hypothesis test and p-value', 'A check of whether a gap could be luck. The p-value is the probability of seeing a gap at least this large, in either direction, if there were truly no difference.'),
               ('Temperature and top-p (nucleus) sampling', 'Settings that reshape and trim the next-word probabilities before one word is drawn.')],
        word_icons=['chart', 'bars', 'calculator', 'flag', 'speech'],
        words_note=('Five words today, all real industry names. The Gaussian is the bell curve. The central limit theorem explains why averages look Gaussian. The standard error and the confidence interval tell us how much a sample mean can wander. '
                    'A hypothesis test and its p-value ask whether a gap could be luck. And temperature and top-p are the sampling settings that choose the next word. We define each again where it first matters.'),
        keep='Keep your saved lab and these numbers: binomial P(X = 3) = 0.2668, normal P(X < 75) = 0.9332, A/B test z = 2.06 and p = 0.039, and the three softmax rows for T = 0.5, 1 and 2.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Saved lab', value='Notebook or workbook'), dict(label='Key numbers', value='See the check table'),
                                                              dict(label='Next session', value='Bayes theorem'), dict(label='Bring', value='A question about a test result')]),
        keep_title='Save the lab and keep your key numbers',
        next='Session 15: conditional probability and Bayes. We update beliefs with evidence and build a small spam filter by hand.', next_label='Next session',
        keep_note=('Before you go, save your notebook or workbook and keep the key numbers from the check table. Next session is conditional probability and Bayes. '
                   'We will update a belief when new evidence arrives, work through a medical test with natural frequencies, and build a small spam filter by hand. If a p-value or a confidence interval is still unclear, write down your question and bring it.'),
        cover_note=('Welcome to Session 14. Last time we learned the vocabulary of probability. Today we meet the shapes that data and models actually follow, and the tools to reason from a sample. '
                    'We end with a question you have probably asked yourself: why does a chat model answer the same question differently each time? You will be able to answer it with arithmetic.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 13', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.2, 6.8], icons=False,
                  note='If an answer surprised you, look back at Session 13 before the lab.',
                  notes=('Here are the short answers. First, the probabilities of all the possible next words add up to one, because of the total rule: all outcomes together have probability one. '
                         'Second, the expectation of a fair die is 3.5. It is the weighted average over many rolls, and no single roll shows it. '
                         'Third, covariance carries the units of both columns. Correlation divides by both standard deviations, so it has no units and lies between minus one and plus one. Check your own answers against these.')))

    S.append(dict(kind='idea', title='A Bernoulli random variable is one yes or no event with probability p',
                  visual=dict(kind='e_pmf', labels=['0 (no)', '1 (yes)'], values=[1 - P_B, P_B], value_texts=['0.7', '0.3'], hl=[1], xlabel='X = 1 if the user rates the answer helpful', total_text='0.7 + 0.3 = 1'),
                  lead='Illustrative: one user rates an answer helpful with probability p = 0.3.',
                  points=['Bernoulli(p): X is 1 with probability p and 0 with probability 1 - p.', 'E(X) = p = 0.3.', 'Var(X) = p(1 - p) = 0.21.'],
                  notes=('The simplest random variable has only two outcomes, yes or no. We call it a Bernoulli random variable. It equals one with probability p and zero with probability one minus p. '
                         'Here is an illustrative example: a user rates a chat answer as helpful with probability 0.3. The expectation is simply p, 0.3, and the variance is p times one minus p, which is 0.21. '
                         'A coin flip, a spam or not spam label and a fault or no fault reading are all Bernoulli variables. Which one have you met in your own work?')))

    S.append(dict(kind='idea', title='A binomial random variable counts the successes in n independent Bernoulli trials',
                  visual=dict(kind='e_pmf', labels=[str(k) for k in range(N_B + 1)], values=BIN, value_texts=[f'{v:.3f}' for v in BIN], hl=[3], xlabel='k = number of helpful ratings among 10 users', total_text='the 11 bars add up to 1', value_size=14),
                  lead='Ten users, each rates helpful with p = 0.3 (illustrative). X counts the helpful ratings.',
                  points=[f'P(X = 3) = {BIN[3]:.4f}, the gold bar.', f'Mean n p = 3. Standard deviation = {sqrt(N_B * P_B * (1 - P_B)):.3f}.', 'Binomial(n, p) has a mass function with n + 1 bars.'],
                  notes=('Now repeat the Bernoulli trial n times independently, and count the successes. That count is a binomial random variable. Here ten users each rate helpful with probability 0.3. '
                         'The bars show how likely each count is, from zero up to ten. Three helpful ratings is the most likely, which makes sense because the mean is n times p, which is three. '
                         f'The gold bar is the probability of exactly three: {BIN[3]:.4f}. The bars add up to one, as every pmf must. Which count is least likely?')))

    S.append(dict(kind='formula', title='The binomial formula counts the ways and multiplies the probabilities',
                  formulas=[('Binomial pmf', r'$P(X=k) = \binom{n}{k}\,p^{k}\,(1-p)^{n-k}$'), ('Mean and variance', r'$E(X) = np, \qquad \mathrm{Var}(X) = np(1-p)$')],
                  symbols=[['n choose k', 'The number of ways to place k successes among n trials: n! / (k! (n-k)!).', f'10 choose 3 = {comb(10, 3)}'],
                           ['p to the k', 'Probability that k trials all succeed.', f'0.3 cubed = {0.3 ** 3:.3f}'],
                           ['(1-p) to the n-k', 'Probability that the other n - k trials all fail.', f'0.7 to the 7 = {0.7 ** 7:.5f}'],
                           ['P(X = 3)', 'Multiply the three parts.', f'{comb(10, 3)} × {0.3 ** 3:.3f} × {0.7 ** 7:.5f} = {BIN[3]:.4f}']],
                  widths=[2.2, 5.9, 3.8], size=22, note='Spreadsheet: BINOM.DIST(3, 10, 0.3, FALSE) gives the same number. TRUE gives P(X at most 3).',
                  notes=('Here is the formula. The first part, n choose k, counts the ways to choose which k of the n trials succeed. For ten trials and three successes there are 120 ways. '
                         'The next part is the probability that those three succeed, 0.3 cubed. The last is the probability that the other seven fail, 0.7 to the power seven. Multiply the three parts and you get 0.2668. '
                         'The mean is n times p and the variance is n times p times one minus p. In a spreadsheet, BINOM.DIST does the same arithmetic, and in the lab you check it.')))

    sig = [dict(a=-1, b=1, fill='#E0BE36', alpha=1.0), dict(a=-2, b=-1, fill='#E0BE36', alpha=0.4), dict(a=1, b=2, fill='#E0BE36', alpha=0.4)]
    S.append(dict(kind='idea', title='The Gaussian (normal) distribution is the bell curve set by its mean and standard deviation',
                  visual=dict(kind='e_pdf', curve='normal', lo=-3.8, hi=3.8, mu=0, sigma=1, xticks=[-3, -2, -1, 0, 1, 2, 3], xlabel='distance from the mean, in standard deviations (sigma)', shade=sig,
                              notes=[dict(x=0, y=0.2, text='68%', size=22), dict(x=2.2, y=0.28, text='95% within 2 sigma', size=16, color='#111111', to=(1.5, 0.1))]),
                  lead='Gaussian (normal) distribution: symmetric, centred on the mean mu, with width set by sigma.',
                  points=['About 68% of values lie within 1 sigma of mu, and about 95% within 2 sigma.', 'Averages and sums of many small effects look Gaussian. The central limit theorem says why.'],
                  notes=('This is the most important shape in statistics, the Gaussian, also called the normal distribution. It is a symmetric bell, centred on the mean mu, and its width is the standard deviation sigma. '
                         'The horizontal axis counts distance from the mean in standard deviations. About 68 percent of values lie within one sigma of the mean, the dark gold area. About 95 percent lie within two sigma. '
                         'Real data is never perfectly Gaussian, but the shape is a good model for many measurements, and soon you will see why averages follow it.')))

    S.append(dict(kind='formula', title='The Gaussian density and the z-score',
                  formulas=[('Gaussian pdf', r'$f(x) = \frac{1}{\sigma\sqrt{2\pi}}\,e^{-\frac{(x-\mu)^2}{2\sigma^2}}$'), ('z-score', r'$z = \frac{x - \mu}{\sigma}$')],
                  symbols=[['mu, sigma', 'Mean and standard deviation. Quiz scores (illustrative).', 'mu = 60, sigma = 10'],
                           ['z', 'How many standard deviations x lies above the mean.', f'x = 75 gives z = {Z75:g}'],
                           ['Areas', 'P(X < 75) is the area left of z = 1.5. P(50 < X < 70) is the area between z = -1 and 1.', f'{P_LT75:.4f} and {P_50_70:.4f}']],
                  widths=[1.8, 6.5, 3.6], size=20, note='No integrating by hand: NORM.DIST in a sheet or math.erf in Python gives the areas.',
                  notes=('Here are the formulas. The density has the mean and the standard deviation in it, but the shape is always the same bell. The z-score tells us how many standard deviations a value is above the mean. '
                         f'Take illustrative quiz scores with mean 60 and standard deviation 10. A score of 75 has z equal to 1.5. The area to its left is {P_LT75:.4f}, so about 93 percent of learners score below 75. '
                         f'Between 50 and 70, within one sigma, the area is {P_50_70:.4f}. You get these areas from NORM.DIST in a spreadsheet, so nobody integrates by hand.')))

    S.append(dict(kind='idea', title='A multivariate Gaussian is a cloud with a centre and a tilted ellipse',
                  visual=dict(kind='e_gauss2d', points=gauss_points(), mean=[4, 6], cov=COV_M.tolist(), xlabel='hours of study per week', ylabel='quiz score out of 10', xticks=[0, 4, 8], yticks=[2, 6, 10], mean_label='mean (4, 6)'),
                  lead='Two columns at once: study hours and score from Session 13 (illustrative). 150 simulated points.',
                  points=['Centre: the means, 4 and 6.', 'Ellipses: 1 and 2 standard deviations.', 'Red arrow = eigenvector of the covariance matrix, along an ellipse axis. Its eigenvalue is the variance along it.'],
                  notes=('Real data has many columns, so we need the Gaussian in several dimensions. Picture two columns, study hours and score. The multivariate Gaussian is a cloud of points. '
                         'Its centre is the vector of the two means. Its shape is an ellipse, and the tilt of the ellipse comes from the covariance. If the columns rise together, the ellipse leans up to the right. '
                         'The red arrows are the eigenvectors of the covariance matrix, along the long and short axes. That is exactly the idea behind PCA from Session 6. The points here are simulated from our six-learner statistics.')))

    S.append(dict(kind='idea', title=f'The covariance matrix puts every variance and covariance in one table',
                  visual=dict(kind='sheet', headers=['', 'hours', 'score'], rows=[['hours', f'{28 / 6:.3f}', f'{25 / 6:.3f}'], ['score', f'{25 / 6:.3f}', '7.000']], hl=[0, 1], size=22),
                  lead='The covariance matrix of the two columns from Session 13 (this course divides by n).',
                  points=['Diagonal: the variances 4.667 and 7.', 'Off the diagonal: the covariance 4.167, twice.', f'Its eigenvalues are {EIG[1]:.3f} and {EIG[0]:.3f}: the ellipse is long in one direction and thin in the other.'],
                  notes=('For many columns we collect all the variances and covariances in one square table, the covariance matrix, usually written capital sigma. The variances sit on the diagonal. '
                         'The covariance between each pair of columns sits off the diagonal, and the table is symmetric. For our two columns the diagonal holds 4.667 and 7, and the covariance is 4.167. '
                         f'The eigenvalues of this matrix are {EIG[1]:.3f} and {EIG[0]:.3f}. A big gap between them means a long, thin ellipse. Multivariate Gaussians are described by a mean vector and this matrix.')))

    S.append(dict(kind='idea', title='The law of large numbers: the more repeats, the closer the average gets to the true mean',
                  visual=dict(kind='e_lln', series=[lln_series(14), lln_series(15)], target=3.5),
                  lead='Two runs of rolling a die 10,000 times (simulation). The line is the running average.',
                  points=['After 1 roll the average is one of 1 to 6, often far from 3.5.', 'After 100 rolls it is near 3.5.', 'After 10,000 rolls it is usually within about 0.03 of 3.5.'],
                  notes=('The law of large numbers says that the more repeats you average, the closer the average gets to the true mean. Here are two simulated runs of rolling a die ten thousand times. '
                         'The horizontal axis is logarithmic, so the early rolls get room. After a single roll the average is just that one roll, any of one to six, so it is often far off. In these two runs it started at one and at six. By a hundred rolls both lines are near 3.5, and by ten thousand they are very close. '
                         'Remember our sixty fixed rolls from Session 13, with a mean of 3.97. Sixty is simply too few to settle.')))

    S.append(dict(kind='wide', title='The central limit theorem: averages of many rolls look Gaussian, though a single die is flat',
                  visual=dict(kind='e_hist', panels=hist_panels(), ymax=1.4),
                  caption='Each panel: 20,000 averages of n dice. n = 1 is flat, not Gaussian. At n = 30 the red curve fits.',
                  notes=('Here is the central limit theorem as a picture. Each panel shows twenty thousand averages. On the left, the average of one die is just a die, flat, with six bars. '
                         'The average of two dice is a triangle. With five dice the shape is already a bell. With thirty dice it is almost exactly the red Gaussian curve, and it is also much narrower. '
                         'The theorem says this happens for averages of independent values from almost any starting shape, as long as there are enough of them. That is why the Gaussian appears everywhere. Why is the last panel so much narrower?')))

    S.append(dict(kind='formula', title='Standard error: how much a sample mean wanders',
                  formulas=[('Central limit theorem', r'$\bar{X} \approx \mathrm{Gaussian}\left(\mu,\ \frac{\sigma^{2}}{n}\right)$'), ('Standard error', r'$\mathrm{SE} = \frac{\sigma}{\sqrt{n}}$')],
                  symbols=[['x-bar', 'The mean of a sample of n values.', 'mean of 30 dice'],
                           ['sigma, n', 'Standard deviation of one value, and the sample size.', f'sigma = {SD_DIE:.4f} for a die'],
                           ['SE', 'Standard error: the standard deviation of the sample mean.', f'{SD_DIE:.4f} / sqrt(30) = {SD_DIE / sqrt(30):.4f}']],
                  widths=[1.7, 6.4, 3.8], size=22, note='Four times the data halves the SE. Simulated 30-dice averages (seed 14): standard deviation 0.311.',
                  notes=('Here is what the picture says in formulas. The mean of n independent values is close to Gaussian, centred on the true mean mu, with variance sigma squared over n. '
                         'The standard deviation of the sample mean is called the standard error, sigma over the square root of n. For thirty dice, 1.7078 divided by the square root of thirty is 0.3118, and the simulation gave 0.311. '
                         'Notice the square root. To halve the standard error you need four times the data. For a proportion the standard error uses p hat times one minus p hat.')))

    S.append(dict(kind='idea', title='A 95% confidence interval comes from a method that catches the true mean in about 95 of 100 samples',
                  visual=dict(kind='e_ci', intervals=CI_SIM, target=3.5, lo=CI_LO, hi=CI_HI, ticks=[3, 3.5, 4], xlabel='mean of 30 rolls, with its 95% interval'),
                  lead=f'20 samples of 30 dice (simulation). {20 - N_MISS} of the 20 intervals contain the true mean 3.5. The red one misses.',
                  points=['Interval = sample mean plus or minus 1.96 standard errors.', 'The 95% describes the method over many samples.', 'It is not the chance that this one interval holds the true value.'],
                  notes=('A confidence interval gives a range for the true mean instead of a single guess. For each sample of thirty dice we compute the mean, and then go 1.96 standard errors to each side. '
                         f'Here are twenty samples. {20 - N_MISS} of the twenty intervals catch the true mean, 3.5. The red one misses. That matches the promise: about 95 out of 100 intervals catch it. '
                         'But be careful with the wording. The ninety-five percent describes the method over many samples. Once an interval is computed, the true mean is either inside or outside it.')))

    S.append(dict(kind='formula', title='Confidence interval for a mean, worked on the 60 fixed rolls',
                  formulas=[('Interval', r'$\bar{x} \pm 1.96\,\mathrm{SE}, \qquad \mathrm{SE} = \frac{s}{\sqrt{n}}$')],
                  symbols=[['x-bar, n', 'The mean of the 60 rolls from Session 13, and the sample size.', f'{M60:.4f}, 60'],
                           ['s', 'The sample standard deviation (divides by n - 1).', f'{S60:.4f}'],
                           ['SE', 'Standard error s over the square root of n.', f'{SE60:.4f}'],
                           ['Interval', 'Mean plus or minus 1.96 SE.', f'{CI60[0]:.3f} to {CI60[1]:.3f}']],
                  widths=[1.9, 6.4, 3.6], size=24,
                  note='1.96 is the normal approximation. With n = 60 the t value 2.00 gives 3.506 to 4.428, and 3.5 is still just outside.',
                  notes=(f'Let us compute an interval by hand. Our sixty fixed rolls had a mean of {M60:.4f}. The sample standard deviation, dividing by n minus one, is {S60:.4f}. '
                         f'The standard error is that divided by the square root of sixty, which is {SE60:.4f}. The interval is the mean plus or minus 1.96 standard errors, from {CI60[0]:.3f} to {CI60[1]:.3f}. '
                         'Notice that 3.5 is just outside. We know the true mean is 3.5, so this sample is one of the roughly one in twenty that misses. In real work we never know the truth, which is why we report the interval. One refinement: 1.96 is the normal approximation. With only 60 rolls a statistician would use the t value, 2.00, and the interval becomes 3.506 to 4.428, so 3.5 is still just outside.')))

    S.append(dict(kind='idea', title='An A/B test splits users at random into two groups and compares one rate',
                  visual=dict(kind='sheet', headers=['Group', 'Users', 'Rated helpful', 'Rate'], rows=[['A: current app', f'{NA:,}', str(XA), f'{PA:.1%}'], ['B: new feature', f'{NB:,}', str(XB), f'{PB:.1%}']], hl=[1, 3], size=20),
                  lead='Illustrative counts: a new suggested follow-up feature in an AI chat app. Metric: share of chats rated helpful.',
                  points=['Random assignment makes the groups alike, apart from the feature.', f'B beats A by {100 * (PB - PA):.1f} percentage points.', 'Question: a real effect, or luck?'],
                  notes=('Now to a decision you may face. A team adds a new feature to an AI chat app, suggested follow-up questions, and wants to know if it helps. '
                         f'They split users at random into group A with the current app and group B with the new feature, then count chats rated helpful. These counts are illustrative. A had {XA} of {NA:,}, which is {PA:.1%}. B had {XB} of {NB:,}, which is {PB:.1%}. '
                         f'The gap is {100 * (PB - PA):.1f} percentage points. Is that a real effect, or could it be luck? That is what a hypothesis test answers.')))

    S.append(dict(kind='idea', title='A hypothesis test asks how likely a gap this large would be if the feature did nothing',
                  visual=dict(kind='e_pdf', curve='normal', lo=-4, hi=4, mu=0, sigma=1, xticks=[-3, -2, -1, 0, 1, 2, 3], xlabel='gap between the groups, in standard errors, if there is no real difference',
                              shade=[dict(a=Z_AB, b=4, fill='#E0BE36'), dict(a=-4, b=-Z_AB, fill='#E0BE36')],
                              notes=[dict(x=0, y=0.06, text='no real difference', size=16, weight='normal'), dict(x=2.9, y=0.12, text=f'p = {P_AB:.3f}', size=18, color='#AE2525'), dict(x=-2.9, y=0.12, text='both tails', size=14, color='#666666', weight='normal')]),
                  lead=f'Null hypothesis: the true rates are equal. Our gap is z = {Z_AB:.2f} standard errors.',
                  points=[f'The gold tails hold gaps at least this large, in either direction.', f'Their total area is the p-value: {P_AB:.3f}.', 'Small p-value: this gap would be rare by luck alone.'],
                  notes=('A hypothesis test starts from a sceptical assumption, the null hypothesis, which says the two true rates are equal. If that were true, the gap between the groups would still wobble by chance, '
                         f'following this bell curve, measured in standard errors. Our actual gap sits at z equal to {Z_AB:.2f}. The gold tails show the probability of a gap at least that large in either direction. '
                         f'That area is the p-value, {P_AB:.3f}. A small p-value means: if the feature did nothing, a gap this big would be rare. It does not say how big the effect is.')))

    S.append(dict(kind='formula', title='The two-proportion z-test',
                  formulas=[('Standard error under the null', r'$\mathrm{SE} = \sqrt{\hat{p}_{\mathrm{pool}}(1-\hat{p}_{\mathrm{pool}})\left(\frac{1}{n_A} + \frac{1}{n_B}\right)}$'),
                            ('z statistic', r'$z = \frac{\hat{p}_B - \hat{p}_A}{\mathrm{SE}}$')],
                  symbols=[['p-hat_A, p-hat_B', 'The rate in each group: helpful chats k divided by users n.', f'{XA} / {NA} = {PA:.2f}, {XB} / {NB} = {PB:.2f}'],
                           ['p-hat_pool', 'The pooled rate: (k_A + k_B) / (n_A + n_B), both groups together.', f'{PPOOL:.3f}'],
                           ['SE and z', 'The standard error of the gap, and the gap in standard errors.', f'{SE_AB:.5f} and {Z_AB:.3f}']],
                  widths=[1.5, 6.1, 4.3], size=21, note='Two-sided p-value = 2 × (1 - area to the left of z) = 0.0394. Spreadsheet: 2*(1-NORM.DIST(z,0,1,TRUE)).',
                  notes=('Here is the test. If the null hypothesis is true, both groups share one rate, so we pool the counts: 624 helpful chats out of 4,800, which is 0.13. '
                         f'The standard error of the gap uses that pooled rate and both sample sizes, and it comes to {SE_AB:.5f}. The z statistic is the observed gap divided by the standard error, {Z_AB:.3f}. '
                         f'The two-sided p-value is twice the area beyond z, which is {P_AB:.4f}. Next we put every step in one table.')))

    S.append(dict(kind='table', title='The A/B test step by step, with a 95% interval for the gap',
                  headers=['Step', 'Calculation', 'Result'],
                  rows=[['1 Rates', f'{XA} / {NA} and {XB} / {NB}', f'{PA:.3f} and {PB:.3f}'], ['2 Pooled rate', f'({XA} + {XB}) / ({NA} + {NB})', f'{PPOOL:.3f}'],
                        ['3 Standard error', 'square root of 0.13 × 0.87 × (1/2400 + 1/2400)', f'{SE_AB:.5f}'], ['4 z statistic', f'{PB - PA:.3f} / {SE_AB:.5f}', f'{Z_AB:.3f}'],
                        ['5 p-value', '2 × (1 - area to the left of z)', f'{P_AB:.4f}'],
                        ['6 Interval for the gap', f'0.020 plus or minus 1.96 × {SE_DIFF:.5f}', f'{CI_DIFF[0]:.4f} to {CI_DIFF[1]:.4f}']],
                  widths=[2.6, 6.2, 3.2], icons=False,
                  note='Step 3 pools because the test assumes no difference. Step 6 does not assume that: SE = sqrt(p_A(1-p_A)/n_A + p_B(1-p_B)/n_B). The interval, 0.1 to 3.9 points, only just excludes 0.',
                  notes=('Here is the whole test in one table, with illustrative counts. Step one, the two rates. Step two, the pooled rate, 0.13. Step three, the standard error of the gap. '
                         f'Step four, z equals {Z_AB:.2f}. Step five, the p-value, {P_AB:.4f}. And step six, a confidence interval for the gap itself: from {100 * CI_DIFF[0]:.1f} to {100 * CI_DIFF[1]:.1f} percentage points. '
                         'The interval only just excludes zero. That is more informative than the p-value alone, because it shows the effect could be tiny. A careful team might run the test longer.')))

    S.append(dict(kind='compare', title='A p-value is easy to misread',
                  left=dict(head='A p-value is', icon='check', points=['The probability of a gap at least this large, either way, if there were truly no difference']),
                  right=dict(head='A p-value is not', icon='cross', points=['The probability that the feature does nothing', 'The size of the effect', 'Proof: test 20 useless features and about 1 passes at p < 0.05 by luck']),
                  verdict='Report the gap and its interval beside the p-value.',
                  notes=('Here is the warning. A p-value is the probability of seeing a gap at least this large, in either direction, if there were truly no difference. That is all. It is not the probability that the feature does nothing, and it says nothing about how big or how useful the effect is. '
                         'A tiny effect can have a tiny p-value with enough users. And if you run twenty tests, one will pass the 0.05 line by luck alone. So always report the gap and its interval next to the p-value. What would you want to see before shipping the feature?')))

    S.append(dict(kind='idea', title='Sampling from a distribution: cut 0 to 1 into slices and see where a random number lands',
                  visual=dict(kind='e_slices', words=WORDS, probs=[float(v) for v in P_T[1.0]], u=0.62),
                  lead='Each word owns a slice as wide as its probability. Draw a random number u between 0 and 1.',
                  points=['u = 0.62 lands in the coffee slice (0.446 to 0.745).', 'Draw again and u differs, so the word can differ.', 'Likely words are picked often, unlikely ones sometimes.'],
                  notes=('How does a program pick a word from a probability list? It cuts the line from zero to one into slices, one per word, as wide as each probability. Tea owns the first 0.446, coffee the next 0.299, and so on. '
                         'Then it draws a random number between zero and one. Here u is 0.62, which falls in the coffee slice, between 0.446 and 0.745. So the program outputs coffee. '
                         'Draw again, and u will be different, so the word can be different. This is why the same question can give different answers. The numbers here are illustrative.')))

    S.append(dict(kind='wide', title='Temperature reshapes the probabilities: low is sharp, high is flat',
                  visual=dict(kind='e_softmax', words=WORDS, logits=[float(v) for v in LOGITS],
                              panels=[dict(title='T = 0.5', probs=[float(v) for v in P_T[0.5]], sub='sharper'), dict(title='T = 1', probs=[float(v) for v in P_T[1.0]], sub='as the model scored'),
                                      dict(title='T = 2', probs=[float(v) for v in P_T[2.0]], sub='flatter')]),
                  caption='Illustrative logits. Same five words, three temperatures. Each column of probabilities adds up to 1.',
                  notes=('Temperature is a setting that reshapes the probabilities before sampling. Take the same five logits, and divide them by T before softmax. With T equal to 0.5, the top word tea jumps to 0.628 and the unlikely words nearly vanish. '
                         'With T equal to one, we get the probabilities as the model scored them. With T equal to two, the list flattens, and soup grows from 0.033 to 0.089. '
                         'Low temperature gives predictable answers. High temperature gives more varied, and sometimes stranger, answers. All the numbers are illustrative.')))

    S.append(dict(kind='formula', title='Softmax with temperature',
                  formulas=[('Softmax with temperature', r'$p_i = \frac{e^{z_i / T}}{\sum_{j} e^{z_j / T}}$')],
                  symbols=[['z_i', 'The logit (raw score) of word i.', 'tea: z = 3.0'],
                           ['T', 'The temperature, above 0. T = 1 is the plain softmax.', 'T = 2'],
                           ['Worked', f'tea at T = 2: e to the 1.5 = {np.exp(1.5):.3f}. The five terms add up to {sum(np.exp(LOGITS / 2)):.3f}.', f'{np.exp(1.5):.3f} / {sum(np.exp(LOGITS / 2)):.3f} = {P_T[2.0][0]:.4f}'],
                           ['Limits', 'T near 0 always picks the top word (greedy). T very large makes every word equally likely.', 'T = 0.5 gives tea 0.628']],
                  widths=[1.6, 6.6, 3.7], size=24, note='Use the stable softmax of Session 12: subtract the largest z first. The result is the same.',
                  notes=('Here is the formula. Divide each logit by the temperature T, take e to that power, and divide by the sum over all words. With T equal to one it is the ordinary softmax from Session 12. '
                         f'Worked example for tea at T equal to two. Three divided by two is 1.5, e to the 1.5 is {np.exp(1.5):.3f}. The five terms add up to {sum(np.exp(LOGITS / 2)):.3f}, so the probability is {P_T[2.0][0]:.4f}. '
                         'As T goes toward zero, the top word takes everything, which is called greedy decoding. As T grows, all words approach equal probability. Use the stable version to avoid overflow.')))

    S.append(dict(kind='idea', title='Top-p (nucleus) sampling keeps only the smallest set of likely words, then renormalises',
                  visual=dict(kind='e_softmax', words=WORDS, panels=[dict(title='T = 1, sorted', probs=[float(v) for v in P_T[1.0]], keep=KEEP, sub='cumulative: 0.446, 0.745, 0.893'),
                                                                     dict(title='top-p = 0.8, renormalised', probs=[float(v) for v in P_NUC], keep=KEEP, gold=True, sub='kept words add up to 1')]),
                  lead='Top-p (nucleus) sampling with p = 0.8: add words from the most likely until the total reaches 0.8.',
                  points=['Tea, coffee and water reach 0.893. Milk and soup are cut (grey).', f'Divide the kept words by 0.893: {tw(P_NUC[:3])}.', 'Now milk and soup can never be chosen.'],
                  notes=('Top-p sampling, also called nucleus sampling, was published by Holtzman and colleagues in 2020. It cuts the unlikely tail. Sort the words from most to least likely and add the probabilities until the total reaches p. '
                         'With p equal to 0.8, tea gives 0.446, coffee brings it to 0.745, and water brings it to 0.893, so we stop. Milk and soup are cut. '
                         f'We then divide the kept probabilities by 0.893 so that they add up to one again: tea {P_NUC[0]:.3f}, coffee {P_NUC[1]:.3f}, water {P_NUC[2]:.3f}. Sampling now happens only among those three. The numbers are illustrative.')))

    TAB = {T: [pick(u, P_T[T]) for u in U] for T in (1.0, 0.5, 2.0)}
    rows = [[f'{i + 1}', f'{u:.3f}', TAB[1.0][i], TAB[0.5][i], TAB[2.0][i]] for i, u in enumerate(U)]
    S.append(dict(kind='table', title='The same eight random numbers give different words at different temperatures',
                  headers=['Draw', 'Random number u', 'T = 1', 'T = 0.5', 'T = 2'], rows=rows, widths=[1.3, 3.2, 2.3, 2.3, 2.3], icons=False,
                  note='Each word is the first slice whose running total reaches u. Illustrative probabilities, seed 19.',
                  notes=(f'Let us draw eight times, using the same eight random numbers for each temperature. At T equal to one the draws give {len(set(TAB[1.0]))} different words, with tea {TAB[1.0].count("tea")} times. '
                         f'At T equal to 0.5 the same numbers give only {len(set(TAB[0.5]))} different words, and tea {TAB[0.5].count("tea")} times, because the top slices are bigger. '
                         f'At T equal to two all {len(set(TAB[2.0]))} words appear and tea only {TAB[2.0].count("tea")} times. '
                         'So the same question can give different answers for two reasons. The random number changes from draw to draw, and the temperature changes how the line is cut. With a very low temperature the answers repeat.')))

    S.append(dict(kind='code', title='Bridge: sample the central limit theorem and the next word with NumPy',
                  code='rng = np.random.default_rng(14)\nmeans = rng.integers(1, 7, (20000, 30)).mean(axis=1)\nmeans.mean(), means.std()\nz = np.array([3.0, 2.6, 1.9, 1.2, 0.4])\np = np.exp(z / 0.5 - (z / 0.5).max())\np = p / p.sum()\nrng.choice(5, p=p)',
                  reads=['Line 2: 20,000 samples of 30 dice. mean(axis=1) averages each row.', 'Line 3: the mean is near 3.5 and the standard deviation near the standard error 0.3118 (0.311 with seed 14).',
                         'Lines 4 to 6: softmax with temperature T = 0.5, stable version.', 'Line 7: draw one index from 0 to 4 with these probabilities.', 'Spreadsheet: NORM.DIST, BINOM.DIST and fixed sample columns replace the random draws.'],
                  notes=('Here is the code you will use. The first block repeats the central limit theorem experiment. Generate twenty thousand rows of thirty dice, average each row, and look at the mean and standard deviation of those averages. '
                         'The second block is softmax with temperature. Divide the logits by T, subtract the maximum for stability, exponentiate and divide by the sum. Then rng.choice draws one word index using those probabilities. '
                         'In the spreadsheet we avoid random draws and use fixed columns, so the numbers do not move.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the concepts. Please open either the Python notebook or the spreadsheet workbook. Both use the same numbers. '
                         'In each step, predict first, then run, then read the output, then change one thing. In the spreadsheet we use fixed sample columns instead of the volatile RAND function, so your numbers match mine. I will walk around.')))

    S.append(dict(kind='steps', title='The lab has six stages, in Python and in the spreadsheet',
                  steps=[dict(head='1 Binomial', text='Formula and simulation', icon='bars'), dict(head='2 Gaussian', text='Areas and z-scores', icon='chart'), dict(head='3 CLT', text='Averages of 30 dice', icon='gear'),
                         dict(head='4 A/B test', text='z, p-value and interval', icon='flag'), dict(head='5 Softmax', text='Temperature 0.5, 1 and 2', icon='speech'), dict(head='6 Top-p', text='Cut and draw a word', icon='check')], highlight=3,
                  caption='Python notebook: Session 14. Workbook sheets: Binomial, Normal, Sampling, ABtest and Temperature. Predict, run, read, change one thing.',
                  notes=('Here is the lab plan. Stage one, the binomial by formula and by simulation. Stage two, areas under the Gaussian. Stage three, the central limit theorem with averages of thirty dice. '
                         'Stage four, the A/B test with its z statistic, p-value and interval. Stage five, softmax with temperature on the toy logits. Stage six, the top-p cut and drawing words. '
                         'The workbook has one sheet per stage, with gold cells for you to fill. The Check sheet or the last notebook cell shows which answers are right.')))

    S.append(dict(kind='table', title='Check your numbers against these before you move on', headers=['What you compute', 'You should see'],
                  rows=[['Binomial(10, 0.3): P(X = 3) by formula', f'{BIN[3]:.4f}'], ['Normal(60, 10): P(X < 75) and P(50 < X < 70)', f'{P_LT75:.4f} and {P_50_70:.4f}'],
                        ['Standard error of the mean of 30 dice: formula, and simulated (seed 14)', f'{SD_DIE / sqrt(30):.4f}; about 0.311'], ['Confidence interval of the 60 fixed rolls', f'{CI60[0]:.3f} to {CI60[1]:.3f}'],
                        ['A/B test: pooled rate, z, two-sided p-value', f'{PPOOL:.2f}, {Z_AB:.3f}, {P_AB:.4f}'], ['A/B test: 95% interval for the gap', f'{CI_DIFF[0]:.4f} to {CI_DIFF[1]:.4f}'],
                        ['P(tea) at T = 0.5, 1 and 2', f'{P_T[0.5][0]:.4f}, {P_T[1.0][0]:.4f}, {P_T[2.0][0]:.4f}'], ['Top-p 0.8: renormalised P(tea)', f'{P_NUC[0]:.4f}']],
                  widths=[7.4, 4.4], icons=False, note='Simulated numbers use the seeds in the notebook. They match the slides only if the seed line runs first.',
                  notes=('Use this table as your checkpoint. The first rows come from formulas, and they must match exactly. The simulated numbers, such as the standard deviation of the averages, will be close to the table but are tolerant in the checks. '
                         'The A/B test row is the one to look at twice: z of 2.06 and a p-value of 0.039. If a number differs, stop and call me over, because every later step builds on the earlier ones.')))

    S.append(dict(kind='table', title='Errors you will meet, what they mean and what to do', headers=['Where', 'What you see', 'What to do'],
                  rows=[['Python', 'Your sample numbers differ from the slides', 'Use Run all from the top. Every random step makes its own seeded generator.'],
                        ['Python', 'p-value 0.0197 instead of 0.0394', 'You used one tail. Double the tail area for a two-sided test.'],
                        ['Spreadsheet', 'BINOM.DIST gives P(X at most 3) = 0.6496', 'The last argument was TRUE. Use FALSE for exactly 3.'],
                        ['Spreadsheet', 'NORM.DIST #VALUE!', 'It needs four arguments: x, mean, standard deviation and TRUE.'],
                        ['Both', 'Probabilities after temperature do not add to 1', 'The sum must run over all five words, with the same T in every term.']],
                  widths=[2.0, 4.6, 5.4], icons=['cross'] * 5,
                  notes=('Here are the errors you will probably meet. If your simulated numbers differ from the slides, check that the seeded generator line ran first. '
                         'A p-value of 0.0197 means you used one tail instead of two. In the spreadsheet, BINOM.DIST with TRUE gives the probability of at most three, not exactly three. '
                         'NORM.DIST needs four arguments. And if the temperature probabilities do not add to one, the sum in the denominator is missing a word or uses a different T. Read the message and the formula first.')))

    S.append(dict(kind='idea', title='Where this appears in AI: temperature and top-p are settings you can choose',
                  visual=dict(kind='card', title='Sampling settings in public APIs (names only)', fields=[dict(label='temperature', value='Documented by OpenAI, Gemini, Anthropic'),
                                                                                                      dict(label='top_p (nucleus)', value='Documented by the same three APIs'), dict(label='top_k', value='Documented by some providers'),
                                                                                                      dict(label='Same question twice', value='Above T = 0, words are drawn at random')]),
                  lead='These settings control the sampling you did by hand today.',
                  points=['Low temperature: steadier answers. High: more varied.', 'Nucleus sampling: Holtzman and colleagues, 2020.', 'Only for models that expose these settings. Products may add steps we cannot see.'],
                  notes=('This is where today appears in real tools. The public APIs of OpenAI, Google Gemini and Anthropic all document a temperature setting and a top-p setting, and some providers document top-k as well. '
                         'These are the knobs you just used. The model computes the probability for every token, the settings reshape and trim the list, and one token is drawn at random. '
                         'That randomness is why the same question can give different answers. What a product does beyond these settings is not public, so I will not claim more. Do you now see why low temperature repeats itself?')))

    S.append(dict(kind='idea', title='Where this appears in AI: an A/B test shows whether a new AI feature really is better',
                  visual=dict(kind='flow', steps=[dict(head='Split users', text='At random into A and B', icon='people'), dict(head='Measure', text='The same rate for both', icon='chart'),
                                                  dict(head='Test', text='z, p-value and interval', icon='calculator'), dict(head='Decide', text='Effect size and cost too', icon='flag')], highlight=2),
                  lead='Online experiments compare two versions of a product on one measured rate.',
                  points=['Published practice: Kohavi, Tang and Xu describe it in their 2020 book on online controlled experiments.', 'The mathematics is the same as today. Which AI features a company tests is its own business.'],
                  notes=('Here is the same mathematics in practice. Teams that build products with language models compare versions with online experiments. They split users at random, measure one rate such as helpful ratings, and run the same test you ran today. '
                         'The method is published, for example in the 2020 book by Kohavi, Tang and Xu on online controlled experiments. We do not know which features a specific company tests, so I make no claim about that. '
                         'The decision also weighs the size of the effect and the cost, as well as the p-value.')))

    S.append(dict(kind='practice', title='Where this appears in AI: check an assistant with your numbers', minutes=8, label='Check an AI assistant',
                  task='Ask an AI assistant to run the A/B test on our made-up counts.',
                  steps=['Give it A: 288 of 2,400 and B: 336 of 2,400.', 'Ask for z, p and a 95% interval.', f'Compare with {Z_AB:.2f}, {P_AB:.3f} and {100 * CI_DIFF[0]:.1f} to {100 * CI_DIFF[1]:.1f} points.',
                         'Ask what p means. Look for misreadings.'],
                  output='A note: its numbers, your numbers, and any misreading you spotted.',
                  notes=('Now a short activity. Give any AI assistant our A and B counts and ask for the z statistic, the two-sided p-value and a 95 percent interval for the gap. '
                         f'Compare with our numbers: z of {Z_AB:.2f}, p of {P_AB:.3f}, and an interval of {100 * CI_DIFF[0]:.1f} to {100 * CI_DIFF[1]:.1f} percentage points. '
                         'Then ask it to explain the p-value in plain words, and see whether it slips into one of the misreadings. Use only made-up data like this, never confidential data.')))

    S.append(dict(kind='table', title='Exit check: three questions', headers=['Question', 'Short answer'],
                  rows=[['A fair coin is flipped 10 times. What are the mean and standard deviation of the number of heads?', f'n p = 5 and the square root of 10 × 0.5 × 0.5, which is {sqrt(2.5):.3f}.'],
                        ['A test gives p = 0.03. Does that mean a 3% chance the feature does nothing?', 'No. It is the chance of a gap this large if there is truly no difference.'],
                        ['What does lowering the temperature do to the next-word probabilities?', 'It makes them sharper: the top word gets more probability, and the answers repeat more.']],
                  widths=[6.6, 5.4], icons=False,
                  notes=('Three questions to finish. First, ten fair coin flips: the mean number of heads is n times p, which is five, and the standard deviation is the square root of 10 times 0.5 times 0.5, about 1.58. '
                         'Second, a p-value of 0.03 does not mean a three percent chance that the feature does nothing. It is the chance of a gap this large if there is truly no difference. '
                         'Third, lowering the temperature sharpens the probabilities, so the top word gets more, and answers repeat more. Write your answers in your lab file.')))

    s['facilitator'] = dict(
        prep=['Open the deck, one notebook and one workbook. Run the notebook from the top once. The seeded numbers should match the check table.',
              'In the workbook, the "random-looking" columns are fixed values. No RAND anywhere, so the numbers never move.',
              'Write on the board: P(X = 3) = 0.2668, P(X < 75) = 0.9332, z = 2.06, p = 0.039, P(tea) at T = 0.5, 1, 2 = 0.628, 0.446, 0.325.',
              'Have a coin ready to demonstrate sampling noise: flip ten times and compare with five heads.'],
        misconceptions=[('A 95% confidence interval has a 95% chance of containing the true value, once computed', 'The 95% describes the method over many samples. This interval either contains the truth or it does not.'),
                        ('A p-value of 0.04 means a 4% chance that the feature does nothing', 'It is the probability of a gap at least this large if there is truly no difference.'),
                        ('A significant p-value means an important effect', 'With enough users a tiny effect gives a tiny p-value. Look at the size and the interval.'),
                        ('Higher temperature makes the model smarter or more creative on purpose', 'It only flattens the probabilities, so rarer words are chosen more often. That can read as varied, or as wrong.'),
                        ('The same question can only give different answers if the model changed', 'Sampling draws a random number each time, so the same model gives different answers at nonzero temperature.')],
        probes=[('Why does the standard error shrink with the square root of n?', 'Variation in the mean cancels as we average. Four times the data halves the standard error.'),
                ('Why do we use a two-sided test?', 'The new feature could make things worse as well as better, so gaps in both directions count as surprising.'),
                ('Why is the interval for our A/B gap more useful than the p-value alone?', 'It shows the plausible size of the effect. Here it runs from 0.1 to 3.9 points, so the effect could be tiny.'),
                ('What does T = 0 do?', 'The limit is greedy decoding: always the top word. Many APIs allow a temperature of 0, though results can still vary slightly between runs on some systems.'),
                ('What does top-p change that temperature does not?', 'It removes the unlikely tail entirely, so those words can never be chosen, then renormalises. Temperature keeps every word possible.'),
                ('Why 1.96?', 'About 95% of a Gaussian lies within 1.96 standard deviations of the mean.')],
        lab_steps=[('Stage 1: binomial', 'P(X = 3) 0.2668 by formula in both tools. BINOM.DIST with FALSE. The simulation of 100,000 draws gives about 0.267.'),
                   ('Stage 2: Gaussian', 'P(X < 75) 0.9332. NORM.DIST(75,60,10,TRUE). Python uses math.erf.'),
                   ('Stage 3: central limit theorem', 'The 12 fixed samples of 30 dice in the sheet are the first 12 of the 20,000 simulated samples in Python. Simulated: mean near 3.5, standard deviation near 0.311. Formula: 0.3118.'),
                   ('Stage 4: A/B test', 'z 2.060, p 0.0394, interval 0.0010 to 0.0390. Watch for one-tailed p of 0.0197.'),
                   ('Stage 5: temperature', 'P(tea) 0.628, 0.446, 0.325. In the sheet use EXP(z/T) in a helper column, then divide by the sum.'),
                   ('Stage 6: top-p', 'Keep tea, coffee, water. Renormalised 0.4995, 0.3349, 0.1657. Then draw words with the fixed u column.')],
        rescue=['If the concepts overrun, show the central limit theorem and the A/B table, and leave the multivariate Gaussian as a picture.',
                'If learners struggle with confidence intervals, use the coin: the method catches the truth about 19 times in 20.',
                'If only 30 minutes remain for the lab, do stages 3, 4 and 5.', 'If the Python draws differ from the slides, the seed line was skipped or another random call ran first.'],
        after=['Share the lab files again for absent learners.', 'Collect questions about p-values and open Session 15 with the most common one.', 'Remind the class that Session 15 uses the same toy next-word list in a different way.'],
        lab_answer_key=[['Stage 1 PREDICT: which count of helpful ratings is most likely?', '3, the mean n p.'], ['Stage 3 READ: why is the histogram of 30-dice means narrower than that of single dice?', 'The standard error is sigma divided by the square root of n.'],
                        ['Stage 4 READ: is the effect convincing?', 'Borderline. p = 0.039, but the interval only just excludes 0.'], ['Stage 5 CHANGE: set T = 0.2.', f'P(tea) is about {softmax(LOGITS, 0.2)[0]:.2f}.'],
                        ['Stage 6 CHANGE: set top-p to 0.95.', 'Four words are kept. P(tea) renormalised is 0.461.']])
    return s
