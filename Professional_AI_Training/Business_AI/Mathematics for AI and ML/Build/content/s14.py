"""Session 14: Distributions and sampling. Bernoulli and binomial (with the factorial), Gaussian (and where 1.96 comes from), the central limit theorem,
confidence intervals, an A/B test, and drawing the next word from a probability list. Temperature and top-p are taught in Session 17."""
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
SD_BIN = sqrt(N_B * P_B * (1 - P_B))
MU_Q, SD_Q = 60, 10
Z75 = (75 - MU_Q) / SD_Q
P_LT75 = PHI(Z75)
P_50_70 = PHI(1) - PHI(-1)
P_196 = PHI(1.96) - PHI(-1.96)                     # 0.9500

SD_DIE = (35 / 12) ** 0.5                          # known distribution (Session 13): no n
ROLLS60 = np.array([6, 6, 5, 6, 1, 5, 6, 2, 2, 1, 5, 6, 4, 4, 5, 1, 6, 6, 1, 6, 6, 2, 3, 5, 6, 1, 4, 3, 3, 5, 5, 3, 6, 4, 6, 1, 6, 5, 4, 3, 2, 2, 2, 5, 3, 6, 3, 4, 3, 5, 3, 6, 4, 1, 6, 4, 5, 6, 2, 1])
M60 = float(ROLLS60.mean())
S60 = float(ROLLS60.std(ddof=1))                   # sample standard deviation (n - 1)
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


def softmax(z):
    e = np.exp(z - z.max())
    return e / e.sum()


P1 = softmax(LOGITS)                               # the Session 13 next-word list
CUM1 = np.cumsum(P1)
U = np.random.default_rng(19).random(8)


def pick(u, p):
    return WORDS[int(np.searchsorted(np.cumsum(p), u))]


DRAWS = [pick(u, P1) for u in U]


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
SIM_MEANS = np.random.default_rng(14).integers(1, 7, (20000, 30)).mean(1)
SE_SIM = float(SIM_MEANS.std(ddof=1))              # 0.311


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


COV_M = np.array([[5.6, 5.0], [5.0, 8.4]])         # sample covariance matrix of the six learners (Session 13, n - 1)
EIG = np.linalg.eigvalsh(COV_M)


def gauss_points():
    """150 draws from a Gaussian with the learners' means and covariance. Hours below 0 or scores outside 0 to 10 are impossible, so they are left out."""
    pts = np.random.default_rng(14).multivariate_normal([4, 6], COV_M, 150)
    ok = (pts[:, 0] >= 0) & (pts[:, 1] >= 0) & (pts[:, 1] <= 10)
    return [[float(a), float(b)] for a, b in pts[ok]]


GPTS = gauss_points()


def build():
    s = dict(
        num=14, block='Probability and statistics', short_title='Distributions and sampling',
        title='Distributions and sampling: the Gaussian, the central limit theorem, A/B tests and drawing the next word',
        question='Why can the same question get a different answer from a chat model, and how do we test whether a new AI feature is better?',
        outcomes=['Describe the Bernoulli, binomial and Gaussian distributions, and work a binomial probability with factorials',
                  'Explain the law of large numbers, the central limit theorem, standard error and a 95% confidence interval, and run a two-proportion A/B test',
                  'Draw the next word from a probability list with a random number, and explain why the same question can get different answers'],
        outcome_icons=['chart', 'calculator', 'speech'],
        outcome_note=('Three things to take away today. First, describe the Bernoulli, binomial and Gaussian distributions, and work out a binomial probability with factorials. '
                      'Second, explain the law of large numbers, the central limit theorem, the standard error and a 95 percent confidence interval, and run an A/B test. '
                      'Third, draw the next word from a probability list with a random number. That third skill answers why a chat model can give different answers to the same question.'),
        clock=[(10, 'Recall and a real question from AI'), (35, 'Concept: a picture, then a hand example'), (10, 'Break'), (45, 'Lab: Python or spreadsheet, predict, run, change one thing'),
               (15, 'Where it appears in AI, plus an exit check'), (5, 'Save the work')],
        plan_title='Your two hours: distributions, averages, a test, then drawing a word',
        plan_caption='Pictures and hand calculations first. Then the lab on averages, an A/B test and drawing words.',
        plan_note=('The first ten minutes recall Session 13 and introduce the question about different answers. Then thirty-five minutes of concepts, with a picture first and a hand example after it. '
                   'After the break you have forty-five minutes in the lab, in Python or in a spreadsheet, on the same numbers. We finish with where this appears in AI, an exit check and saving your work.'),
        recall_from='Session 13',
        recall=[('Two fair dice are independent. What does that mean, and what is P(both show 6)?', 'Knowing one die does not change the probabilities of the other. P = 1/6 × 1/6 = 1/36.'),
                ('What is the expectation of a fair die, and what does it mean?', '3.5. It is the probability-weighted average over many rolls. No single roll shows it.'),
                ('For six learners\' scores, do we divide the variance by n or by n - 1, and why?', 'By n - 1, because the six are a sample (VAR.S, ddof=1). Dividing by n treats the list as the whole population.')],
        words=[('Binomial distribution', 'The number of successes in n independent yes or no trials, each with probability p.'),
               ('Gaussian (normal) distribution', 'The bell curve, set by its mean mu and standard deviation sigma.'),
               ('Central limit theorem', 'Averages of many independent values are close to Gaussian, whatever the original shape.'),
               ('Standard error, confidence interval, p-value', 'How much a sample mean wanders, a range built from it, and how surprising a gap would be if nothing changed.'),
               ('Sampling', 'Drawing a value at random according to its probabilities, as a chat model draws its next word.')],
        word_icons=['bars', 'chart', 'gear', 'calculator', 'speech'],
        words_note=('Five words today, all real industry names. The binomial counts successes in repeated independent trials. The Gaussian is the bell curve, and the central limit theorem explains why averages look Gaussian. '
                    'The standard error, the confidence interval and the p-value tell us how much a sample can wander and whether a gap could be luck. '
                    'Sampling means drawing a value at random according to its probabilities, which is how a chat model picks its next word. Each word is defined again where it first matters.'),
        keep=f'Keep your saved lab and these numbers: binomial P(X = 3) = 0.2668, normal P(X < 75) = 0.9332, the interval of the 60 rolls {CI60[0]:.3f} to {CI60[1]:.3f}, A/B test z = 2.06 and p = 0.039, and tea in 4 of the 8 draws.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Saved lab', value='Notebook or workbook'), dict(label='Key numbers', value='See the check table'),
                                                              dict(label='Next session', value='Bayes theorem'), dict(label='Bring', value='A question about a test result')]),
        keep_title='Save the lab and keep your key numbers',
        next='Session 15: conditional probability and Bayes. We update beliefs with evidence and build a small spam filter by hand.', next_label='Next session',
        keep_note=('Before you go, save your notebook or workbook and keep the key numbers from the check table. Next session is conditional probability and Bayes. '
                   'We will update a belief when new evidence arrives, work through a medical test with natural frequencies, and build a small spam filter by hand. If a p-value or a confidence interval is still unclear, write down your question and bring it.'),
        cover_note=('Welcome to Session 14. Last time we learned the vocabulary of probability. Today we meet the shapes that data and models follow, and the tools to reason from a sample. '
                    'We end with a question you have probably asked yourself: why does a chat model answer the same question differently each time? By the end of the session you can answer it with arithmetic.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 13', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.2, 6.8], icons=False,
                  note='If an answer surprised you, look back at Session 13 before the lab.',
                  notes=('Three short answers. Two dice are independent: knowing one does not change the probabilities of the other, so the probability that both show six is one sixth times one sixth, one thirty-sixth. Today leans on that idea many times. '
                         'The expectation of a fair die is 3.5, the weighted average over many rolls, which no single roll shows. '
                         'And six learners are a sample, so their variance divides by n minus one, as VAR.S and ddof equals one do. Dividing by n would treat the six as the whole population. Check your own answers against these.')))

    S.append(dict(kind='idea', title='A Bernoulli trial is one yes or no, and a binomial counts the yeses in n independent trials',
                  visual=dict(kind='e_pmf', labels=[str(k) for k in range(N_B + 1)], values=BIN, value_texts=[f'{v:.3f}' for v in BIN], hl=[3], xlabel='k = number of helpful ratings among 10 users', total_text='the 11 bars add up to 1', value_size=14),
                  lead='Illustrative: a user rates an answer helpful with p = 0.3. X counts the helpful ratings of 10 users.',
                  points=['One user: Bernoulli(p). Mean p, variance p(1 - p) = 0.21.', 'Independent (Session 13): one rating does not change another.',
                          f'P(X = 3) = {BIN[3]:.4f} (gold). Mean n p = 3, sd {SD_BIN:.3f}.'],
                  notes=('The simplest random variable has two outcomes, yes or no. It is called a Bernoulli random variable: one with probability p, zero with probability one minus p. In our illustrative example a user rates a chat answer as helpful with probability 0.3, so the mean is 0.3 and the variance is 0.3 times 0.7, which is 0.21. '
                         'Now ask ten users, independently, in the sense of Session 13: one rating does not change another. Count the helpful ratings. That count is a binomial random variable, and the bars show how likely each count is. '
                         f'Three is most likely, because the mean is n times p. The gold bar is exactly three: {BIN[3]:.4f}.')))

    S.append(dict(kind='formula', title='The binomial formula counts the ways with factorials, then multiplies the probabilities',
                  formulas=[('Binomial pmf', r'$P(X=k) = \binom{n}{k}\,p^{k}\,(1-p)^{n-k}$'), ('The ways, by hand', r'$\binom{10}{3} = \frac{10!}{3!\;7!} = \frac{10\cdot 9\cdot 8}{3\cdot 2\cdot 1} = \frac{720}{6} = 120$')],
                  symbols=[['n! (n factorial)', 'Multiply every whole number from n down to 1. 0! = 1.', '3! = 3 × 2 × 1 = 6'],
                           ['n choose k', 'The number of ways to place k successes among n trials: n! / (k! (n - k)!).', f'10 choose 3 = {comb(10, 3)}'],
                           ['p to the k, (1-p) to the n-k', 'The k trials all succeed, and the other n - k all fail.', f'{0.3 ** 3:.3f} and {0.7 ** 7:.5f}'],
                           ['P(X = 3)', 'Multiply the three parts.', f'{comb(10, 3)} × {0.3 ** 3:.3f} × {0.7 ** 7:.5f} = {BIN[3]:.4f}']],
                  widths=[2.6, 5.7, 3.6], size=20, note='Spreadsheet: COMBIN(10, 3) = 120. BINOM.DIST(3, 10, 0.3, FALSE) gives the whole answer. TRUE gives P(X at most 3).',
                  notes=('The formula has three parts. The first counts the ways to choose which k of the n trials succeed, and it uses the factorial: n factorial, written n with an exclamation mark, multiplies every whole number from n down to one. Three factorial is six. '
                         'Ten choose three is ten factorial over three factorial times seven factorial. Most of the factors cancel, leaving ten times nine times eight over three times two times one, which is 720 over 6, or 120 ways. '
                         'The second part is the chance that those three succeed, 0.3 cubed. The third is the chance that the other seven fail, 0.7 to the power seven. Multiply them all and you get 0.2668. Multiplying is allowed because the trials are independent.')))

    sig = [dict(a=-1, b=1, fill='#E0BE36', alpha=1.0), dict(a=-1.96, b=-1, fill='#E0BE36', alpha=0.4), dict(a=1, b=1.96, fill='#E0BE36', alpha=0.4)]
    S.append(dict(kind='idea', title='The Gaussian (normal) distribution is the bell curve, and 95% of it lies within 1.96 standard deviations',
                  visual=dict(kind='e_pdf', curve='normal', lo=-3.8, hi=3.8, mu=0, sigma=1, xticks=[-3, -1.96, -1, 0, 1, 1.96, 3], xlabel='distance from the mean, in standard deviations (sigma)', shade=sig, ymax=0.62,
                              notes=[dict(x=0, y=0.2, text='68%', size=22)],
                              brackets=[dict(a=-1, b=1, y=0.45, text='68% within 1 sigma', size=15), dict(a=-1.96, b=1.96, y=0.54, text='95% within 1.96 sigma (about 2)', size=15, color='#AE2525')]),
                  lead='Gaussian (normal): a symmetric bell, centred on the mean mu, width set by sigma.',
                  points=['About 68% lies within 1 sigma of mu.', '95% lies within 1.96 sigma. Every 95% interval today uses this 1.96.', 'Averages of many small effects look Gaussian.'],
                  notes=('This is the most important shape in statistics, the Gaussian, also called the normal distribution. It is a symmetric bell, centred on the mean mu, and its width is the standard deviation sigma. '
                         'The horizontal axis counts distance from the mean in standard deviations. About 68 percent of values lie within one sigma of the mean, the dark gold area. '
                         'Go out to 1.96 sigma on each side and the area is exactly 95 percent. People often round 1.96 to two. Hold on to 1.96: every 95 percent interval later today is the estimate plus or minus 1.96 of its standard deviations.')))

    S.append(dict(kind='formula', title='The Gaussian density, the z-score and the area to the left of z',
                  formulas=[('Gaussian pdf, z-score', r'$f(x) = \frac{1}{\sigma\sqrt{2\pi}}\,e^{-\frac{(x-\mu)^2}{2\sigma^2}}, \qquad z = \frac{x - \mu}{\sigma}$'),
                            ('Area left of z', r'$\Phi(z) = P(Z \leq z) = \frac{1}{2}\left(1 + \mathrm{erf}\left(z/\sqrt{2}\right)\right)$')],
                  symbols=[['mu, sigma', 'Quiz scores (illustrative): Normal with mean 60 and standard deviation 10.', 'mu = 60, sigma = 10'],
                           ['z', 'How many standard deviations x lies above the mean.', f'x = 75 gives z = {Z75:g}'],
                           ['Phi(z)', 'The area to the left of z. erf is a built-in function that computes it.', f'Phi(1.5) = {P_LT75:.4f}']],
                  widths=[1.8, 6.5, 3.6], size=18, note=f'Areas: between z = -1 and 1, {P_50_70:.4f}; between -1.96 and 1.96, {P_196:.4f}. Sheet: NORM.DIST(75, 60, 10, TRUE) = 0.9332.',
                  notes=('Three formulas. The density has the mean and the standard deviation in it, but the shape is always the same bell. The z-score tells us how many standard deviations a value is above the mean. '
                         f'Take illustrative quiz scores with mean 60 and standard deviation 10. A score of 75 has z equal to 1.5. The area to its left is written capital Phi of z, and it is {P_LT75:.4f}, so about 93 percent of learners score below 75. '
                         'Python computes Phi with a built-in function called erf, as the third line shows, and a spreadsheet uses NORM.DIST. The area between minus 1.96 and 1.96 is 0.95, which is where 1.96 comes from.')))

    S.append(dict(kind='idea', title='Recall: two columns at once form a tilted Gaussian cloud, described by the covariance matrix',
                  visual=dict(kind='e_gauss2d', points=GPTS, mean=[4, 6], cov=COV_M.tolist(), xlabel='hours of study per week', ylabel='quiz score out of 10', xticks=[0, 4, 8], yticks=[0, 5, 10], mean_label='mean (4, 6)'),
                  lead='Means (4, 6). Sample covariance matrix (Session 13): variances 5.6 and 8.4, covariance 5.',
                  points=['Ellipses: 1 and 2 sd. Red arrows: eigenvectors (PCA, Session 6).', f'Eigenvalues {EIG[1]:.2f} and {EIG[0]:.2f}: the variance along each arrow.',
                          f'{len(GPTS)} of 150 simulated points: scores outside 0 to 10 are left out.'],
                  notes=('A recall slide, joining Sessions 5, 6 and 13. With two columns, study hours and score, the Gaussian becomes a cloud. Its centre is the vector of means, four and six. Its shape is an ellipse, tilted by the covariance. '
                         'The numbers are the sample covariance matrix of our six learners from last session: variances 5.6 and 8.4 on the diagonal, covariance 5 off it. '
                         f'The red arrows are its eigenvectors, the principal components of Session 6, and the eigenvalues {EIG[1]:.2f} and {EIG[0]:.2f} are the variances along them. A real score cannot leave the range zero to ten, so simulated points outside it are not drawn.')))

    S.append(dict(kind='idea', title='The law of large numbers: the more repeats, the closer the average gets to the true mean',
                  visual=dict(kind='e_lln', series=[lln_series(14), lln_series(15)], target=3.5),
                  lead='Two runs of rolling a die 10,000 times (simulation). The line is the running average.',
                  points=['After 1 roll the average is one of 1 to 6, often far from 3.5.', 'After 100 rolls it is near 3.5.', 'After 10,000 rolls it is usually within about 0.03 of 3.5.'],
                  notes=('The law of large numbers says that the more independent repeats you average, the closer the average gets to the true mean. These are two simulated runs of rolling a die ten thousand times. '
                         'The horizontal axis is logarithmic, so the early rolls get room. After a single roll the average is that one roll, any of one to six, so it is often far off. In these two runs it started at one and at six. By a hundred rolls both lines are near 3.5, and by ten thousand they are very close. '
                         'Our sixty fixed rolls from Session 13 had a mean of 3.97. Sixty is too few to settle.')))

    S.append(dict(kind='wide', title='The central limit theorem: averages of many rolls look Gaussian, though a single die is flat',
                  visual=dict(kind='e_hist', panels=hist_panels(), ymax=1.4),
                  caption='Each panel: 20,000 averages of n dice. n = 1 is flat, not Gaussian. At n = 30 the red curve fits.',
                  notes=('The central limit theorem as a picture. Each panel shows twenty thousand averages. On the left, the average of one die is a single die, flat, with six bars. '
                         'The average of two dice is a triangle. With five dice the shape is already a bell. With thirty dice it is almost exactly the red Gaussian curve, and it is also much narrower. '
                         'The theorem says this happens for averages of independent values from almost any starting shape, as long as there are enough of them. That explains why the Gaussian appears everywhere. Why is the last panel so much narrower?')))

    S.append(dict(kind='formula', title='Standard error: how much a sample mean wanders',
                  formulas=[('Central limit theorem', r'$\bar{X}\ \approx\ \mathrm{Gaussian\ with\ mean}\ \mu\ \mathrm{and\ standard\ deviation}\ \sigma/\sqrt{n}$'), ('Standard error', r'$\mathrm{SE} = \frac{\sigma}{\sqrt{n}}$')],
                  symbols=[['x-bar', 'The mean of a sample of n independent values.', 'mean of 30 dice'],
                           ['sigma, n', 'Standard deviation of one value, and the sample size. The die\'s sigma is known (Session 13), so no n - 1 here.', f'sigma = {SD_DIE:.4f}'],
                           ['SE', 'Standard error: the standard deviation of the sample mean.', f'{SD_DIE:.4f} / sqrt(30) = {SD_DIE / sqrt(30):.4f}']],
                  widths=[1.7, 6.6, 3.6], size=20, note=f'Four times the data halves the SE. Simulated 30-dice averages (seed 14): standard deviation {SE_SIM:.3f}.',
                  notes=('The picture in formulas. The mean of n independent values is close to Gaussian, centred on the true mean mu, with standard deviation sigma over the square root of n. '
                         'That standard deviation of the sample mean is called the standard error. For a die we know sigma exactly from its probabilities, 1.7078, so nothing is estimated and no n minus one appears. For thirty dice, 1.7078 divided by the square root of thirty is 0.3118, and the simulation gave 0.311. '
                         'To halve the standard error you need four times the data.')))

    S.append(dict(kind='idea', title='A 95% confidence interval comes from a method that catches the true mean in about 95 of 100 samples',
                  visual=dict(kind='e_ci', intervals=CI_SIM, target=3.5, lo=CI_LO, hi=CI_HI, ticks=[3, 3.5, 4], xlabel='mean of 30 rolls, with its 95% interval'),
                  lead=f'20 samples of 30 dice (simulation). {20 - N_MISS} of the 20 intervals contain the true mean 3.5. The red one misses.',
                  points=['Interval = sample mean plus or minus 1.96 standard errors: the 95% band of the Gaussian.', 'The 95% describes the method over many samples.', 'It is not the chance that this one interval holds the true value.'],
                  notes=('A confidence interval gives a range for the true mean instead of a single guess. For each sample of thirty dice we compute the mean, then go 1.96 standard errors to each side. Why 1.96? The sample mean is close to Gaussian, and 95 percent of a Gaussian lies within 1.96 standard deviations. '
                         f'Twenty samples are shown. {20 - N_MISS} of the twenty intervals catch the true mean, 3.5, and the red one misses. That matches the promise: about 95 out of 100 intervals catch it. '
                         'Be careful with the wording. The 95 percent describes the method over many samples. Once an interval is computed, the true mean is either inside or outside it.')))

    S.append(dict(kind='formula', title='Confidence interval for a mean, worked on the 60 fixed rolls',
                  formulas=[('Interval', r'$\bar{x} \pm 1.96\,\mathrm{SE}, \qquad \mathrm{SE} = \frac{s}{\sqrt{n}}$')],
                  symbols=[['x-bar, n', 'The mean of the 60 rolls from Session 13, and the sample size.', f'{M60:.4f}, 60'],
                           ['s', 'Sample standard deviation: sigma is unknown, so estimate it with n - 1 (STDEV.S).', f'{S60:.4f}'],
                           ['SE', 'Standard error s over the square root of n.', f'{SE60:.4f}'],
                           ['1.96', 'Phi(1.96) = 0.975, so 95% of a Gaussian lies between -1.96 and 1.96.', '95% band'],
                           ['Interval', 'Mean plus or minus 1.96 SE.', f'{CI60[0]:.3f} to {CI60[1]:.3f}']],
                  widths=[1.9, 6.4, 3.6], size=20,
                  note='With only 60 rolls a statistician uses the t value 2.00: 3.506 to 4.428, and 3.5 is still just outside.',
                  notes=(f'An interval by hand. Our sixty fixed rolls had a mean of {M60:.4f}. In real work sigma is unknown, so we estimate it from the sample, and an estimate from a sample divides by n minus one, as in Session 13. That gives s equal to {S60:.4f}. '
                         f'The standard error is s divided by the square root of sixty, {SE60:.4f}. The interval is the mean plus or minus 1.96 standard errors, from {CI60[0]:.3f} to {CI60[1]:.3f}. '
                         '3.5 is just outside. We know the true mean is 3.5, so this sample is one of the roughly one in twenty that misses. With so few rolls a statistician would use the t value, 2.00, in place of 1.96, and 3.5 is still just outside.')))

    S.append(dict(kind='idea', title='An A/B test splits users at random into two groups and compares one rate',
                  visual=dict(kind='sheet', headers=['Group', 'Users', 'Rated helpful', 'Rate'], rows=[['A: current app', f'{NA:,}', str(XA), f'{PA:.1%}'], ['B: new feature', f'{NB:,}', str(XB), f'{PB:.1%}']], hl=[1, 3], size=20),
                  lead='Illustrative counts: a new suggested follow-up feature in an AI chat app. Metric: share of chats rated helpful.',
                  points=['Random assignment makes the groups alike, apart from the feature.', f'B beats A by {100 * (PB - PA):.1f} percentage points.', 'Question: a real effect, or luck?'],
                  notes=('A decision you may face. A team adds a new feature to an AI chat app, suggested follow-up questions, and wants to know if it helps. '
                         f'They split users at random into group A with the current app and group B with the new feature, then count chats rated helpful. These counts are illustrative. A had {XA} of {NA:,}, which is {PA:.1%}. B had {XB} of {NB:,}, which is {PB:.1%}. '
                         f'The gap is {100 * (PB - PA):.1f} percentage points. Is that a real effect, or could it be luck? A hypothesis test answers that.')))

    S.append(dict(kind='idea', title='A hypothesis test asks how likely a gap this large would be if the feature did nothing',
                  visual=dict(kind='e_pdf', curve='normal', lo=-4, hi=4, mu=0, sigma=1, xticks=[-3, -2, -1, 0, 1, 2, 3], xlabel='gap between the groups, in standard errors, if there is no real difference',
                              shade=[dict(a=Z_AB, b=4, fill='#E0BE36'), dict(a=-4, b=-Z_AB, fill='#E0BE36')],
                              notes=[dict(x=0, y=0.06, text='no real difference', size=16, weight='normal'), dict(x=2.9, y=0.12, text=f'p = {P_AB:.3f}', size=18, color='#AE2525'), dict(x=-2.9, y=0.12, text='both tails', size=14, color='#666666', weight='normal')]),
                  lead=f'Null hypothesis: the true rates are equal. Our gap is z = {Z_AB:.2f} standard errors.',
                  points=[f'The gold tails hold gaps at least this large, in either direction. Their area is the p-value: {P_AB:.3f}.', 'A common, arbitrary convention calls p < 0.05 "significant".', 'Small p-value: this gap would be rare by luck alone.'],
                  notes=('A hypothesis test starts from a sceptical assumption, the null hypothesis, which says the two true rates are equal. If that were true, the gap between the groups would still wobble by chance, '
                         f'following this bell curve, measured in standard errors. Our actual gap sits at z equal to {Z_AB:.2f}. The gold tails show the probability of a gap at least that large in either direction. '
                         f'That area is the p-value, {P_AB:.3f}. Many fields use a threshold of 0.05 and call smaller p-values significant. The threshold is a convention with nothing special about it, and a small p-value says nothing about how big the effect is.')))

    S.append(dict(kind='formula', title='The two-proportion z-test',
                  formulas=[('Standard error under the null', r'$\mathrm{SE} = \sqrt{\hat{p}_{\mathrm{pool}}(1-\hat{p}_{\mathrm{pool}})\left(\frac{1}{n_A} + \frac{1}{n_B}\right)}$'),
                            ('z statistic', r'$z = \frac{\hat{p}_B - \hat{p}_A}{\mathrm{SE}}$')],
                  symbols=[['p-hat_A, p-hat_B', 'The rate in each group: helpful chats k divided by users n.', f'{XA} / {NA} = {PA:.2f}, {XB} / {NB} = {PB:.2f}'],
                           ['p-hat_pool', 'The pooled rate: (k_A + k_B) / (n_A + n_B), both groups together.', f'{PPOOL:.3f}'],
                           ['SE and z', 'The standard error of the gap, and the gap in standard errors.', f'{SE_AB:.5f} and {Z_AB:.3f}']],
                  widths=[1.5, 6.1, 4.3], size=21, note='Two-sided p-value = 2 × (1 - Phi(z)) = 0.0394. Spreadsheet: 2*(1-NORM.DIST(z,0,1,TRUE)).',
                  notes=('The test itself. If the null hypothesis is true, both groups share one rate, so we pool the counts: 624 helpful chats out of 4,800, which is 0.13. '
                         f'The standard error of the gap uses that pooled rate and both sample sizes, and it comes to {SE_AB:.5f}. The z statistic is the observed gap divided by the standard error, {Z_AB:.3f}. '
                         f'The two-sided p-value is twice the area beyond z, which is {P_AB:.4f}. The table that follows puts every step in one place.')))

    S.append(dict(kind='table', title='The A/B test step by step, with a 95% interval for the gap',
                  headers=['Step', 'Calculation', 'Result'],
                  rows=[['1 Rates', f'{XA} / {NA} and {XB} / {NB}', f'{PA:.3f} and {PB:.3f}'], ['2 Pooled rate', f'({XA} + {XB}) / ({NA} + {NB})', f'{PPOOL:.3f}'],
                        ['3 Standard error', 'square root of 0.13 × 0.87 × (1/2400 + 1/2400)', f'{SE_AB:.5f}'], ['4 z statistic', f'{PB - PA:.3f} / {SE_AB:.5f}', f'{Z_AB:.3f}'],
                        ['5 p-value', '2 × (1 - area to the left of z)', f'{P_AB:.4f}'],
                        ['6 Interval for the gap', f'0.020 plus or minus 1.96 × {SE_DIFF:.5f}', f'{CI_DIFF[0]:.4f} to {CI_DIFF[1]:.4f}']],
                  widths=[2.6, 6.2, 3.2], icons=False,
                  note='Step 3 pools because the test assumes no difference. Step 6 does not assume that: SE = sqrt(p_A(1-p_A)/n_A + p_B(1-p_B)/n_B). The interval, 0.1 to 3.9 points, only just excludes 0.',
                  notes=('The whole test in one table, with illustrative counts. Step one, the two rates. Step two, the pooled rate, 0.13. Step three, the standard error of the gap. '
                         f'Step four, z equals {Z_AB:.2f}. Step five, the p-value, {P_AB:.4f}. And step six, a 95 percent confidence interval for the gap itself, again plus or minus 1.96 standard errors: from {100 * CI_DIFF[0]:.1f} to {100 * CI_DIFF[1]:.1f} percentage points. '
                         'The interval only just excludes zero. It tells you more than the p-value alone, because it shows the effect could be tiny. A careful team might run the test longer.')))

    S.append(dict(kind='compare', title='A p-value is easy to misread',
                  left=dict(head='A p-value is', icon='check', points=['The probability of a gap at least this large, either way, if there were truly no difference']),
                  right=dict(head='A p-value is not', icon='cross', points=['The probability that the feature does nothing', 'The size of the effect']),
                  verdict='Testing many features: of 20 useless ones, about 1 passes the 0.05 line by luck. Report the gap and its interval.',
                  notes=('A warning. A p-value is the probability of seeing a gap at least this large, in either direction, if there were truly no difference. That is all. It is not the probability that the feature does nothing, and it says nothing about how big or how useful the effect is. '
                         'A tiny effect can have a tiny p-value with enough users. A separate trap comes from testing many things at once: test twenty useless features and about one will pass the 0.05 line by luck alone. So always report the gap and its interval next to the p-value.')))

    S.append(dict(kind='idea', title='Sampling from a distribution: cut 0 to 1 into slices and see where a random number lands',
                  visual=dict(kind='e_slices', words=WORDS, probs=[float(v) for v in P1], u=0.62),
                  lead='The next-word list of Session 13. Each word owns a slice as wide as its probability. Draw a random number u between 0 and 1.',
                  points=['u = 0.62 lands in the coffee slice (0.446 to 0.745).', 'Draw again and u differs, so the word can differ.', 'Likely words are picked often, unlikely ones sometimes.'],
                  notes=('How does a program pick a word from a probability list? It cuts the line from zero to one into slices, one per word, as wide as each probability. Tea owns the first 0.446, coffee the next 0.299, and so on. The slice edges are running totals. '
                         'Then it draws a random number between zero and one. Here u is 0.62, which falls in the coffee slice, between 0.446 and 0.745, so the program outputs coffee. '
                         'Draw again, and u will be different, so the word can be different. That answers the first half of today\'s question. Session 17 adds the settings that reshape the slices first. The numbers are illustrative.')))

    S.append(dict(kind='code', title='Bridge: sample the central limit theorem and the next word with NumPy',
                  code='rng = np.random.default_rng(14)\nmeans = rng.integers(1, 7, (20000, 30)).mean(axis=1)\nmeans.mean(), means.std(ddof=1)\nnp.cumsum([1, 2, 3])      # running totals: 1, 3, 6\np = np.array([0.446, 0.299, 0.148, 0.074, 0.033])\ncum = np.cumsum(p)        # slice edges\nnp.searchsorted(cum, 0.62)',
                  reads=['Line 2: 20,000 samples of 30 dice. mean(axis=1) averages each row.', f'Line 3: the mean is near 3.5; the standard deviation is near the standard error 0.3118 ({SE_SIM:.3f} with seed 14).',
                         'Line 4: np.cumsum gives running totals.', 'Lines 6 and 7: the slice edges, then the first edge that reaches u: 1 = coffee.', 'Spreadsheet: NORM.DIST, BINOM.DIST and fixed sample columns replace the random draws.'],
                  notes=('The code you will use. The first block repeats the central limit theorem experiment. Generate twenty thousand rows of thirty dice, average each row, and look at the mean and standard deviation of those averages, with ddof equal to one because they are a sample of averages. '
                         'np.cumsum adds as it goes, giving running totals. You need it twice in the lab: for the running average of the law of large numbers, and for the slice edges. '
                         'np.searchsorted then finds the first edge that reaches u, which is the drawn word. In the spreadsheet we use fixed columns, so the numbers do not move.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the concepts. Please open either the Python notebook or the spreadsheet workbook. Both use the same numbers. '
                         'In each step, predict first, then run, then read the output, then change one thing. In the spreadsheet we use fixed sample columns in place of the volatile RAND function, so your numbers match mine. I will walk around.')))

    S.append(dict(kind='steps', title='The lab has five stages, in Python and in the spreadsheet',
                  steps=[dict(head='1 Binomial', text='Factorials, formula and simulation', icon='bars'), dict(head='2 Gaussian', text='Areas and z-scores', icon='chart'), dict(head='3 CLT', text='Averages of 30 dice', icon='gear'),
                         dict(head='4 Interval and A/B test', text='CI, then z, p and the gap', icon='flag'), dict(head='5 Draw words', text='Slices and 8 random numbers', icon='speech')], highlight=3,
                  caption='Python notebook: Distributions and sampling. Workbook sheets: Binomial, Normal, Sampling, ABtest and Words. Predict, run, read, change one thing.',
                  notes=('Five stages in the lab. Stage one, the binomial by formula and by simulation. Stage two, areas under the Gaussian. Stage three, the law of large numbers and the central limit theorem with averages of thirty dice. '
                         'Stage four, the confidence interval of the sixty rolls, then the A/B test with its z statistic, p-value and interval. Stage five, the slices of the next-word list and eight draws with fixed random numbers. '
                         'The workbook has one sheet per stage, with gold cells for you to fill. The Check sheet or the last notebook cell shows which answers are right.')))

    S.append(dict(kind='table', title='Check your numbers against these before you move on', headers=['What you compute', 'You should see'],
                  rows=[['Binomial(10, 0.3): 10 choose 3, and P(X = 3)', f'{comb(10, 3)} and {BIN[3]:.4f}'], ['Normal (mean 60, sd 10): P(X below 75), P(X from 50 to 70)', f'{P_LT75:.4f} and {P_50_70:.4f}'],
                        ['Standard error of the mean of 30 dice: formula, and simulated (seed 14)', f'{SD_DIE / sqrt(30):.4f}; about {SE_SIM:.3f}'], ['Confidence interval of the 60 fixed rolls (s with n - 1)', f'{CI60[0]:.3f} to {CI60[1]:.3f}'],
                        ['A/B test: pooled rate, z, two-sided p-value', f'{PPOOL:.2f}, {Z_AB:.3f}, {P_AB:.4f}'], ['A/B test: 95% interval for the gap', f'{CI_DIFF[0]:.4f} to {CI_DIFF[1]:.4f}'],
                        ['Words: running total after coffee, and tea in the 8 draws', f'{CUM1[1]:.4f} and {DRAWS.count("tea")}']],
                  widths=[7.4, 4.4], icons=False, note='Simulated numbers use the seeds in the notebook. They match the slides only if the seed line runs first.',
                  notes=('Use this table as your checkpoint. The first rows come from formulas, and they must match exactly. The simulated numbers, such as the standard deviation of the averages, will be close to the table, and the checks allow for that. '
                         'The A/B test row deserves a second look: z of 2.06 and a p-value of 0.039. If a number differs, stop and call me over, because every later step builds on the earlier ones.')))

    S.append(dict(kind='table', title='Errors you will meet, what they mean and what to do', headers=['Where', 'What you see', 'What to do'],
                  rows=[['Python', 'Your sample numbers differ from the slides', 'Use Run all from the top. Every random step makes its own seeded generator.'],
                        ['Python', 'p-value 0.0197 instead of 0.0394', 'You used one tail. Double the tail area for a two-sided test.'],
                        ['Spreadsheet', 'BINOM.DIST gives P(X at most 3) = 0.6496', 'The last argument was TRUE. Use FALSE for exactly 3.'],
                        ['Both', 'Interval 3.519 to 4.415, slightly narrow', 'You divided by n. The sample s uses n - 1: STDEV.S or ddof=1.'],
                        ['Both', 'A draw picks the word one slice too late', 'u belongs to the first slice whose running total reaches u.']],
                  widths=[2.0, 4.6, 5.4], icons=['cross'] * 5,
                  notes=('The errors you will probably meet. If your simulated numbers differ from the slides, check that the seeded generator line ran first. '
                         'A p-value of 0.0197 means you used one tail instead of two. In the spreadsheet, BINOM.DIST with TRUE gives the probability of at most three, which differs from exactly three. '
                         'An interval that is a little too narrow usually means the standard deviation divided by n, so use STDEV.S or ddof equal to one. And a draw that lands one word late has skipped the slice whose running total first reaches u.')))

    S.append(dict(kind='idea', title='Where this appears in AI: a language model draws its next token at random from its probabilities',
                  visual=dict(kind='flow', steps=[dict(head='Logits', text='One score per token', icon='robot'), dict(head='Softmax', text='Probabilities that add to 1', icon='chart'),
                                                  dict(head='Slices', text='Running totals from 0 to 1', icon='bars'), dict(head='Random u', text='The slice it hits is the next token', icon='speech')], highlight=3),
                  lead='Published language models produce a probability for every token, and sampling draws one of them.',
                  points=['A new random number each time: the same question can get a different answer.', 'Public APIs document settings that reshape the list first: temperature and top-p (Session 17).'],
                  notes=('Today in real systems. A published language model of this kind ends with a probability for every token in its vocabulary, as you saw in Session 13. When it samples, it draws a random number and takes the token whose slice it lands in, exactly as you did by hand. '
                         'Each answer uses new random numbers, which is why the same question can come back differently. '
                         'The public APIs of OpenAI, Google Gemini and Anthropic document settings, temperature and top-p, that reshape the list before the draw. Session 17 teaches both. What a product does beyond these documented settings is not public.')))

    S.append(dict(kind='idea', title='Where this appears in AI: an A/B test shows whether a new AI feature really is better',
                  visual=dict(kind='flow', steps=[dict(head='Split users', text='At random into A and B', icon='people'), dict(head='Measure', text='The same rate for both', icon='chart'),
                                                  dict(head='Test', text='z, p-value and interval', icon='calculator'), dict(head='Decide', text='Effect size and cost too', icon='flag')], highlight=2),
                  lead='Online experiments compare two versions of a product on one measured rate.',
                  points=['Published practice: Kohavi, Tang and Xu describe it in their 2020 book on online controlled experiments.', 'The mathematics is the same as today. Which AI features a company tests is its own business.'],
                  notes=('The same mathematics in practice. Teams that build products with language models compare versions with online experiments. They split users at random, measure one rate such as helpful ratings, and run the same test you ran today. '
                         'The method is published, for example in the 2020 book by Kohavi, Tang and Xu on online controlled experiments. We do not know which features a specific company tests, so I make no claim about that. '
                         'The decision also weighs the size of the effect and the cost, as well as the p-value.')))

    S.append(dict(kind='practice', title='Where this appears in AI: check an assistant with your numbers', minutes=8, label='Check an AI assistant',
                  task='Ask an AI assistant to run the A/B test on our made-up counts.',
                  steps=['Give it A: 288 of 2,400 and B: 336 of 2,400.', 'Ask for z, p and a 95% interval.', f'Compare with {Z_AB:.2f}, {P_AB:.3f} and {100 * CI_DIFF[0]:.1f} to {100 * CI_DIFF[1]:.1f} points.',
                         'Ask what p means. Look for misreadings.'],
                  output='A note: its numbers, your numbers, and any misreading you spotted.',
                  notes=('A short activity. Give any AI assistant our A and B counts and ask for the z statistic, the two-sided p-value and a 95 percent interval for the gap. '
                         f'Compare with our numbers: z of {Z_AB:.2f}, p of {P_AB:.3f}, and an interval of {100 * CI_DIFF[0]:.1f} to {100 * CI_DIFF[1]:.1f} percentage points. '
                         'Then ask it to explain the p-value in plain words, and see whether it slips into one of the misreadings. Use only made-up data like this, never confidential data.')))

    S.append(dict(kind='table', title='Exit check: three questions', headers=['Question', 'Short answer'],
                  rows=[['A fair coin is flipped 10 times. What are the mean and standard deviation of the number of heads?', f'n p = 5 and the square root of 10 × 0.5 × 0.5, which is {sqrt(2.5):.3f}.'],
                        ['A test gives p = 0.03. Does that mean a 3% chance the feature does nothing?', 'No. It is the chance of a gap this large if there is truly no difference.'],
                        ['With the slices of today, which word does u = 0.90 pick, and why can the next answer differ?', 'Milk (0.893 to 0.967). The next draw uses a new random number.']],
                  widths=[6.6, 5.4], icons=False,
                  notes=('Three questions to finish. First, ten fair coin flips: the mean number of heads is n times p, which is five, and the standard deviation is the square root of 10 times 0.5 times 0.5, about 1.58. '
                         'Second, a p-value of 0.03 does not mean a three percent chance that the feature does nothing. It is the chance of a gap this large if there is truly no difference. '
                         'Third, u equal to 0.90 lands in the milk slice, between 0.893 and 0.967, and the next answer can differ because it draws a new random number. Write your answers in your lab file.')))

    s['facilitator'] = dict(
        prep=['Open the deck, one notebook and one workbook. Run the notebook from the top once. The seeded numbers should match the check table.',
              'In the workbook, the "random-looking" columns are fixed values. No RAND anywhere, so the numbers never move.',
              f'Write on the board: 10 choose 3 = 120, P(X = 3) = 0.2668, P(X < 75) = 0.9332, CI {CI60[0]:.3f} to {CI60[1]:.3f}, z = 2.06, p = 0.039, tea 4 of 8.',
              'Have a coin ready to demonstrate sampling noise: flip ten times and compare with five heads.'],
        misconceptions=[('A 95% confidence interval has a 95% chance of containing the true value, once computed', 'The 95% describes the method over many samples. This interval either contains the truth or it does not.'),
                        ('A p-value of 0.04 means a 4% chance that the feature does nothing', 'It is the probability of a gap at least this large if there is truly no difference.'),
                        ('A significant p-value means an important effect', 'With enough users a tiny effect gives a tiny p-value. Look at the size and the interval.'),
                        ('1.96 is a magic number', 'It is where the Gaussian holds 95%: Phi(1.96) = 0.975, so 2.5% lies in each tail.'),
                        ('The same question can only give different answers if the model changed', 'Sampling draws a new random number each time, so the same model and the same probabilities can give different words.')],
        probes=[('Why does the standard error shrink with the square root of n?', 'Variation in the mean cancels as we average. Four times the data halves the standard error.'),
                ('Why do we use a two-sided test?', 'The new feature could make things worse as well as better, so gaps in both directions count as surprising.'),
                ('Why is the interval for our A/B gap more useful than the p-value alone?', 'It shows the plausible size of the effect. Here it runs from 0.1 to 3.9 points, so the effect could be tiny.'),
                ('Why can we multiply the probabilities in the binomial formula?', 'The trials are independent (Session 13), so the probability of a whole pattern is the product.'),
                ('Why does the die\'s standard error use sigma, but the 60 rolls use s with n - 1?', 'The die\'s sigma is known from its probabilities. For the rolls we pretend sigma is unknown and estimate it from a sample, so n - 1.'),
                ('Why 1.96?', 'About 95% of a Gaussian lies within 1.96 standard deviations of the mean.')],
        lab_steps=[('Stage 1: binomial', 'COMBIN(10,3) = 120, P(X = 3) 0.2668 by formula in both tools. The spreadsheet learner fills the pmf column with BINOM.DIST(k,10,0.3,FALSE). The simulation of 100,000 draws gives about 0.267.'),
                   ('Stage 2: Gaussian', 'P(X < 75) 0.9332. NORM.DIST(75,60,10,TRUE). Python uses Phi (math.erf).'),
                   ('Stage 3: central limit theorem', 'The 12 fixed samples of 30 dice in the sheet are the first 12 of the 20,000 simulated samples in Python: mean 3.3972, sample sd 0.3748 (STDEV.S). Twelve averages are too few to show 0.3118; the 20,000 give 0.311.'),
                   ('Stage 4: interval and A/B test', f'CI {CI60[0]:.3f} to {CI60[1]:.3f} (STDEV.S). Pooled 0.13, SE 0.009708, z 2.060, p 0.0394, gap interval 0.0010 to 0.0390. Watch for one-tailed p of 0.0197.'),
                   ('Stage 5: draw words', 'Running totals 0.4459, 0.7448, 0.8932, 0.9669, 1. The 8 fixed u give tea, milk, tea, tea, tea, coffee, water, coffee: tea 4 times.')],
        rescue=['If the concepts overrun, show the central limit theorem and the A/B table, and leave the multivariate recall slide as a picture.',
                'If learners struggle with confidence intervals, use the coin: the method catches the truth about 19 times in 20.',
                'If only 30 minutes remain for the lab, do stages 3, 4 and 5.', 'If the Python draws differ from the slides, the seed line was skipped or another random call ran first.'],
        after=['Share the lab files again for absent learners.', 'Collect questions about p-values and open Session 15 with the most common one.', 'Remind the class that Session 17 reshapes the same slices with temperature and top-p.'],
        lab_answer_key=[['Stage 1 PREDICT: which count of helpful ratings is most likely?', '3, the mean n p.'], ['Stage 3 READ: why is the histogram of 30-dice means narrower than that of single dice?', 'The standard error is sigma divided by the square root of n.'],
                        ['Stage 4 READ: is the effect convincing?', 'Borderline. p = 0.039, but the interval only just excludes 0.'], ['Stage 4 CHANGE: four times the users.', 'z doubles to about 4.12 and p falls below 0.0001.'],
                        ['Stage 5 CHANGE: 100,000 draws.', 'The share of tea comes out near 0.446, its probability (law of large numbers).']])
    return s
