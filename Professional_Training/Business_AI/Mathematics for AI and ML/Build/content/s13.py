"""Session 13: Probability basics. Sample space, events, random variables, independence, pmf and pdf, expectation, variance, covariance and correlation (sample data divide by n - 1)."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'kit'))
import diagrams_math_e  # noqa: E402,F401  (registers the e_ figure kinds)

# ---------------------------------------------------------------- numbers (all slide numbers come from here)
FACES = np.arange(1, 7)
P_DIE = np.full(6, 1 / 6)
E_DIE = float((FACES * P_DIE).sum())                      # 3.5
VAR_DIE = float(((FACES - E_DIE) ** 2 * P_DIE).sum())     # 35/12
SD_DIE = VAR_DIE ** 0.5
TWO = [[a + b for b in FACES] for a in FACES]             # row = die 2, column = die 1
SUM_COUNTS = [sum(1 for a in FACES for b in FACES if a + b == s) for s in range(2, 13)]
P_SUM7 = SUM_COUNTS[5] / 36

WORDS = ['tea', 'coffee', 'water', 'milk', 'soup']
LOGITS = np.array([3.0, 2.6, 1.9, 1.2, 0.4])


def softmax(z, T=1.0):
    e = np.exp((z - z.max()) / T)
    return e / e.sum()


P_WORDS = softmax(LOGITS)
SURPRISE = -np.log(P_WORDS)                                # surprise of each word in nats (ln)
E_SURP = float((P_WORDS * SURPRISE).sum())                 # expected surprise, 1.3093 nats
E_X2 = float((FACES ** 2 * P_DIE).sum())                   # 91/6

X = np.array([1, 2, 3, 5, 6, 7], dtype=float)             # hours of study per week (illustrative)
Y = np.array([4, 2, 8, 5, 7, 10], dtype=float)            # quiz score out of 10 (illustrative)
MX, MY = X.mean(), Y.mean()
PROD = (X - MX) * (Y - MY)
COV = float(PROD.sum() / (len(X) - 1))                    # sample covariance (divide by n - 1), 5.0
VX, VY = float(X.var(ddof=1)), float(Y.var(ddof=1))       # sample variances 5.6 and 8.4
CORR = float(np.corrcoef(X, Y)[0, 1])
COV_P = float(PROD.mean())                                 # population form (divide by n), 4.1667
VY_P = float(Y.var())                                      # 7
ROLLS60 = np.array([6, 6, 5, 6, 1, 5, 6, 2, 2, 1, 5, 6, 4, 4, 5, 1, 6, 6, 1, 6, 6, 2, 3, 5, 6, 1, 4, 3, 3, 5, 5, 3, 6, 4, 6, 1, 6, 5, 4, 3, 2, 2, 2, 5, 3, 6, 3, 4, 3, 5, 3, 6, 4, 1, 6, 4, 5, 6, 2, 1])
M60, V60 = float(ROLLS60.mean()), float(ROLLS60.var(ddof=1))   # 3.9667 and 3.1853
UNIFORM_P = (5 - 2) * 0.1



def build():
    sd_x, sd_y = VX ** 0.5, VY ** 0.5
    tw = [f'{v:.3f}' for v in P_WORDS]
    s = dict(
        num=13, block='Probability and statistics', short_title='Probability basics',
        title='Probability basics: random variables, independence, expectation, variance and covariance',
        question='A chat model gives every possible next word a probability. What does that number mean, and why do they all add up to exactly one?',
        outcomes=['Describe a sample space, an event, a random variable and independence, and use the rules of probability on dice',
                  'Calculate an expectation, a variance, a standard deviation, a covariance and a correlation by hand and by computer, and say whether a list is divided by n or n - 1',
                  'Read a next-word probability list from a chat model as a probability mass function'],
        outcome_icons=['book', 'calculator', 'chart'],
        outcome_note=('Three things to take away today. You can describe a sample space, an event, a random variable and what it means for two of them to be independent, and you can use the rules of probability on dice. '
                      'You can calculate an expectation, a variance, a standard deviation, a covariance and a correlation, first by hand and then by computer, and you can say whether a list of data was divided by n or by n minus one. '
                      'And you can read the list of next-word probabilities that a chat model produces as a probability mass function, which answers the question on the first slide.'),
        clock=[(10, 'Recall and a real question from AI'), (35, 'Concept: a picture, then a hand example'), (10, 'Break'), (45, 'Lab: Python or spreadsheet, predict, run, change one thing'),
               (15, 'Where it appears in AI, plus an exit check'), (5, 'Save the work')],
        plan_title='Your two hours: dice and data first, then the lab, then AI',
        plan_caption='Pictures and hand calculations first. Then the lab on dice, next-word probabilities and a small dataset.',
        plan_note=('We start with ten minutes of recall from Session 12, and the question about next-word probabilities. Then thirty-five minutes of concepts, always a picture first and then one example by hand. '
                   'After the break you spend forty-five minutes in the lab, in Python or in a spreadsheet, on the same numbers. We finish by seeing where this appears in AI, with an exit check, and then you save your work.'),
        recall_from='Session 12',
        recall=[('Why can computing e to the power of a large score break a softmax, and what does the stable softmax do about it?',
                 'The number overflows (too large for the computer). The stable softmax subtracts the largest score first. The probabilities stay the same.'),
                ('What does regularisation (an L2 penalty, also called weight decay) add to the loss, and why?',
                 'A penalty that grows with the size of the weights. It keeps weights small and reduces overfitting.'),
                ('Many models use 16-bit numbers. What is the saving and what is the risk?',
                 'Less memory and less time. The largest number in the 16-bit floating-point format fp16 is only 65,504, so overflow comes sooner (bfloat16 keeps the range but loses precision).')],
        words=[('Random variable', 'A rule that turns the outcome of a chance event into a number. We write it X.'),
               ('Independent random variables', 'Knowing the value of one does not change the probabilities of the other, like two separate dice.'),
               ('Probability mass function (pmf) and density function (pdf)', 'The pmf gives P(X = x) for values you can list. The pdf is a curve, and probability is the area under it.'),
               ('Expectation, variance and standard deviation', 'The probability-weighted average mu, the average squared distance from it, and its square root sigma.'),
               ('Covariance and correlation', 'How two columns move together, and the same thing scaled to lie between -1 and +1.')],
        word_icons=['question', 'switch', 'chart', 'calculator', 'grid'],
        words_note=('Five words today, and these are the real industry names. A random variable turns the outcome of chance into a number. Two random variables are independent when one tells you nothing about the other. '
                    'The probability mass function and the density function describe how likely each value is. Expectation is the probability-weighted average, and variance and standard deviation measure the spread around it. '
                    'Covariance and correlation say whether two columns move together. Each one is defined again on the slide where it first matters.'),
        keep=f'Keep your saved notebook or workbook, and the numbers from the check table: E(X) = 3.5, Var(X) = 2.9167, the sample covariance {COV:g} (n - 1), the correlation 0.729 and the next-word probabilities that add to 1.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Saved lab', value='Notebook or workbook'), dict(label='Five numbers', value='See the check table'),
                                                              dict(label='Next session', value='Distributions and sampling'), dict(label='Bring', value='One question about chance')]),
        keep_title='Save the lab and keep your five numbers',
        next='Session 14: distributions and sampling. We meet the binomial and the Gaussian, the central limit theorem and an A/B test.', next_label='Next session',
        keep_note=('Before you go, save the notebook or the workbook, and keep the numbers from the check table. Next session we meet the common distributions, the Gaussian above all, '
                   'and we use them to see how much an average can wander and to run an A/B test. Independence, which you met today, is the assumption under most of it. If anything about expectation or covariance was unclear, write down the question and bring it.'),
        cover_note=('Welcome to Session 13, and to the third pillar of the course: probability and statistics. Everything so far gave us numbers. From today we deal with chance, '
                    'which is what a language model faces every time it must pick the next word. Today is the vocabulary: random variables, independence, expectation, variance and covariance. We use dice, a small next-word list and a small dataset.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 12', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.2, 6.8], icons=False,
                  note='If one answer surprised you, look back at Session 12 before the lab.',
                  notes=('Three short answers. First, a large score overflows when we take e to its power. The stable softmax subtracts the largest score first, and the probabilities do not change. '
                         'Second, regularisation adds a penalty that grows with the weights, so they stay small and overfitting is reduced. '
                         'Third, 16-bit numbers save memory and time, but in the fp16 format they top out at 65,504, so overflow comes sooner and the stable softmax matters more. The bfloat16 format keeps the range but loses precision. Check your own answers against these.')))

    S.append(dict(kind='idea', title='A sample space lists every outcome, and an event is a group of outcomes',
                  visual=dict(kind='e_grid', cells=TWO, hl=[[r, c] for r in range(6) for c in range(6) if TWO[r][c] == 7], row_label='Die 2', col_label='Die 1'),
                  lead='Two fair dice give 36 equally likely outcomes. Each cell shows the sum.',
                  points=['Sample space: all possible outcomes.', 'Event: a group of outcomes. Gold = "sum is 7".',
                          f'P(sum is 7) = 6/36, about {P_SUM7:.3f}. A probability runs from 0 to 1.'],
                  notes=('Roll two fair dice. Each cell in this table is one outcome, and the number inside is the sum of the two dice. There are thirty-six cells, and they are equally likely. '
                         'The set of all outcomes is called the sample space. An event is any group of outcomes we care about, and the gold cells are the event that the sum is seven. '
                         'A probability is a number from zero, impossible, to one, certain. When outcomes are equally likely it is the count in the event over the count of all outcomes: six over thirty-six, one sixth, about 0.167. Count the cells for a sum of 10 and you get three.')))

    S.append(dict(kind='formula', title='The rules of probability, checked on dice',
                  formulas=[('Range and total', r'$0 \leq P(A) \leq 1, \qquad P(\mathrm{all\ outcomes}) = 1$'), ('Complement', r'$P(\mathrm{not}\ A) = 1 - P(A)$'),
                            ('Either one', r'$P(A\ \mathrm{or}\ B) = P(A) + P(B) - P(A\ \mathrm{and}\ B)$')],
                  symbols=[['A, B', 'Two events. A = the die is even {2, 4, 6}. B = the die shows more than 4 {5, 6}.', 'one fair die'],
                           ['P(A), P(B)', 'Their probabilities: 3/6 and 2/6.', 'P(A) = 0.5, P(B) = 0.333'],
                           ['A and B', 'Both at once: only the face 6.', 'P(A and B) = 1/6'],
                           ['A or B', 'At least one: 2, 4, 5, 6. The 6 is counted once, so we subtract it once.', f'3/6 + 2/6 - 1/6 = 4/6 = {4 / 6:.3f}']],
                  widths=[1.7, 6.2, 4.0], size=22, note='Complement example: P(not even) = 1 - 3/6 = 3/6. The six faces of one die, 1/6 each, add up to 1.',
                  notes=('Four rules, each checked on a single die. The probability is never below zero or above one, and all outcomes together have probability one. That last rule answers half of today\'s question: something must happen, so the probabilities of every possible next word add to one. '
                         'The probability that A does not happen is one minus the probability that it does. For either one of two events, add their probabilities and subtract the overlap, because the overlap was counted twice. '
                         'Take A as even and B as more than four. The six belongs to both, so three sixths plus two sixths minus one sixth gives four sixths. Check by listing 2, 4, 5, 6.')))

    S.append(dict(kind='idea', title='A random variable turns each outcome into a number, and its pmf says how likely each number is',
                  visual=dict(kind='e_pmf', labels=[str(v) for v in range(2, 13)], values=[c / 36 for c in SUM_COUNTS], value_texts=[f'{c}/36' for c in SUM_COUNTS], hl=[5], xlabel='X = sum of two dice',
                              total_text='the 11 bars add up to 36/36 = 1', value_size=14),
                  lead='Let X be the sum of two dice. The bar heights are the probability mass function (pmf): p(x) = P(X = x).',
                  points=['A random variable X gives a number to each outcome.', 'P(X = 7) = 6/36 is the tallest bar (gold).', 'All the bars add up to 1.'],
                  notes=('A random variable is a rule that gives a number to every outcome of a chance event. Here X is the sum of two dice, so X can be any whole number from two to twelve. '
                         'The heights of the bars are the probability mass function, the pmf: for each value x, the probability that X equals x. Seven is the tallest because six of the thirty-six outcomes give it. Two and twelve are the shortest, one outcome each. '
                         'Add all eleven bars and you get thirty-six over thirty-six, which is one. Read P(X = 2) off the first bar: one thirty-sixth.')))

    soft = [[5, c] for c in range(6)] + [[r, 5] for r in range(6)]
    S.append(dict(kind='idea', title='Two random variables are independent when knowing one does not change the probabilities of the other',
                  visual=dict(kind='e_grid', cells=TWO, hl=[[5, 5]], soft=soft, row_label='Die 2', col_label='Die 1'),
                  lead='X₁ = die 1, X₂ = die 2. Independent: P(X₁ = a and X₂ = b) = P(X₁ = a) × P(X₂ = b) for every pair a, b.',
                  points=['Pale: a 6 on one die. Gold: both show 6.', 'Gold: 1/36 = 1/6 × 1/6.', 'Die 1 and the sum are dependent: die 1 = 1 rules out a sum of 12.'],
                  notes=('Two random variables are independent when knowing the value of one tells you nothing new about the other. Two separate dice are the standard example. The first die landing on six does not change the chances of the second. '
                         'In symbols, the probability of both values is the product of the two probabilities, for every pair of values. Check the gold cell: one cell in thirty-six, and one sixth times one sixth is one thirty-sixth. '
                         'Compare die one with the sum of the dice. If die one shows a one, a sum of twelve becomes impossible, so those two are dependent. Sessions 14 and 15 lean on this idea again and again.')))

    S.append(dict(kind='idea', title='A continuous random variable has a density curve, and probability is the area under it',
                  visual=dict(kind='e_pdf', curve='uniform', lo=-1, hi=11, a=0, b=10, ymax=0.16, xticks=[0, 2, 5, 10], xlabel='minutes until the bus arrives (illustrative)',
                              shade=[dict(a=2, b=5, fill='#E0BE36')], ytick_texts=[(0.1, '0.1')],
                              notes=[dict(x=3.5, y=0.14, text='area = 3 × 0.1 = 0.3', color='#111111', size=16)]),
                  lead='A bus arrives at a random moment in a 10 minute window. This is a uniform distribution: every moment is equally likely.',
                  points=['Density f(x) (pdf): the curve, flat at 1/10 = 0.1, so total area = 10 × 0.1 = 1.', 'P(2 to 5 minutes) = width 3 × height 0.1 = 0.3.', 'P(exactly 3.000...) = 0. Only ranges have probability.'],
                  notes=('Some random variables take values that cannot be listed. The waiting time for a bus, in a ten minute window, can be any value, so we call it continuous, and we cannot draw one bar per value. '
                         'Instead we draw a density curve, the probability density function, the pdf. The height of the curve is not a probability. The area under the curve between two values is. '
                         'Here the curve is flat at 0.1, so the area between two and five minutes is three times 0.1, which is 0.3. The probability of one exact instant is zero. This flat curve is called a uniform distribution, and its total area is ten times 0.1, which is one. The numbers are illustrative.')))

    S.append(dict(kind='formula', title='Probability mass function and density function, side by side',
                  formulas=[('pmf (discrete X)', r'$p(x) = P(X = x), \qquad \sum_x p(x) = 1$'), ('pdf (continuous X)', r'$P(a \leq X \leq b) = \int_a^b f(x)\,dx, \qquad \int f(x)\,dx = 1$')],
                  symbols=[['p(x)', 'The probability that X takes exactly the value x. Never negative.', 'die: p(x) = 1/6'],
                           ['f(x)', 'The density: the height of the curve at x. It can be above 1.', 'bus: f(x) = 0.1'],
                           ['Σ over x', 'Sigma (Session 1): add over every value x that X can take.', '6 faces, total 1'],
                           ['∫ from a to b, dx', 'Integral: the area under f from a to b. dx: along the x axis.', '3 × 0.1 = 0.3']],
                  widths=[2.1, 6.0, 3.8], size=22, note='Both say the total probability is 1. Values you can list use a sum, a continuous curve uses an area.',
                  notes=('The two descriptions side by side. For discrete values, which you can list, we have the pmf, written p of x, the probability that X equals x. The sigma sign from Session 1 adds it over every value x, and the total must be one. '
                         'For a continuous variable we have the density f of x, and the probability that X lies between a and b is the area under the curve from a to b. The tall S is the integral sign, and the dx at the end says the area runs along the x axis. '
                         'You never calculate integrals by hand in this course. For flat curves the area is width times height.')))

    S.append(dict(kind='idea', title='A chat model gives every possible next word a probability, and the probabilities add up to 1',
                  visual=dict(kind='e_softmax', words=WORDS, logits=[float(v) for v in LOGITS], panels=[dict(title='probability p(x)', probs=[float(v) for v in P_WORDS], sub='sum = 1.000')]),
                  lead='Illustrative (made-up numbers): next word after "For breakfast I drink hot ...".',
                  points=['Logits z: one raw score per word.', 'Softmax (Session 12) turns the scores into probabilities.', f'{" + ".join(tw)} = 1.'],
                  notes=('This is the answer to our question, with made-up numbers, so please treat them as illustrative. Suppose a model reads the start of a sentence, and it scores five candidate next words. '
                         'These raw scores are called logits. Softmax, from Session 12, turns them into probabilities. Tea gets 0.446, coffee 0.299, and so on. '
                         'The list is a probability mass function. It is never negative, and it adds up to one, because the model must choose some word. A real model does this for every token in its vocabulary. Tea is the best bet, though it wins less than half the time.')))

    S.append(dict(kind='idea', title='Expectation is the probability-weighted average, the balance point of the bars',
                  visual=dict(kind='e_pmf', labels=['1', '2', '3', '4', '5', '6'], values=[1 / 6] * 6, value_texts=['1/6'] * 6, mean_at=2.5, mean_label='E(X) = 3.5', xlabel='face of one fair die'),
                  lead='Expectation E(X), also called the mean and written mu, is the value the average settles on over many repeats.',
                  points=['Picture the bars as weights on a ruler. E(X) is where it balances.', 'It need not be a possible value: no die shows 3.5.', 'No n here: each value is weighted by its probability p(x).'],
                  notes=('Expectation answers the question: what would the average be if we repeated this chance event many times? Put the bars on a ruler as weights. The expectation is the point where the ruler balances. '
                         'For a fair die it is exactly in the middle, 3.5. You can never roll a 3.5. The expectation is an average over many rolls and says nothing certain about one roll. '
                         'Statisticians also call it the mean and write it mu. There is no count of rows here: each value is weighted by its probability. If the six had a heavier bar, the balance point would move to the right.')))

    S.append(dict(kind='formula', title='Expectation: add up each value times its probability',
                  formulas=[('Expectation', r'$E(X) = \mu = \sum_x x\,p(x)$'), ('Fair die', r'$E(X) = 1\cdot\frac{1}{6} + 2\cdot\frac{1}{6} + \cdots + 6\cdot\frac{1}{6} = \frac{21}{6} = 3.5$'),
                            ('A function of X', r'$E(g(X)) = \sum_x g(x)\,p(x)$')],
                  symbols=[['E(X), mu', 'The expectation (mean) of the random variable X.', f'{E_DIE:g}'],
                           ['x and p(x)', 'One possible value of X, and its probability.', 'face 1 to 6, 1/6 each'],
                           ['g(x)', 'Any rule applied to the value, weighted by p(x).', f'x²: 91/6 = {E_X2:.4f}']],
                  widths=[1.9, 6.0, 4.0], size=18,
                  note='The last line is how losses are averaged in AI: g is the loss for one outcome, E(g(X)) is the expected loss.',
                  notes=('The formula says: multiply each possible value by its probability, and add. For the die each face has probability one sixth, so we get twenty-one sixths, which is 3.5. '
                         'The third line is the same idea for any rule g applied to the value. Weight g of x by the probability and add. With g of x equal to x squared, the die gives ninety-one sixths, about 15.17, which we need for the variance shortcut. '
                         'Training a model averages a loss in exactly this way, as Sessions 16 and 17 show. The same formula works on the next word, too.')))

    rows = [[w, f'{p:.4f}', f'{sp:.4f}', f'{p * sp:.4f}'] for w, p, sp in zip(WORDS, P_WORDS, SURPRISE)] + [['', 'sum 1', '', f'{E_SURP:.4f}']]
    S.append(dict(kind='idea', title=f'Expected surprise of the next word: weight each word\'s surprise by its probability, {E_SURP:.3f} nats',
                  visual=dict(kind='sheet', headers=['word x', 'p(x)', 'surprise -ln p(x)', 'p(x) × surprise'], rows=rows, hl=[5, 3], size=18),
                  lead='Surprise g(x) = -ln p(x) (ln from Session 1): a likely word surprises little, a rare word a lot. Unit: nats, because we use ln.',
                  points=[f'Tea: -ln 0.4459 = {SURPRISE[0]:.4f}. Soup: -ln 0.0331 = {SURPRISE[4]:.4f}.', f'E(surprise) = sum of the last column = {E_SURP:.4f} nats.',
                          'Session 17 calls this average surprise the entropy, and builds the training loss from it.'],
                  notes=('An expectation with a real AI meaning. Give each word a surprise, minus the natural log of its probability. Tea, the likely word, has a small surprise of 0.81. Soup, the unlikely one, has 3.41. '
                         f'The expected surprise weights each surprise by its probability and adds. The last column sums to {E_SURP:.4f}. With ln the unit is called a nat. '
                         'Session 17 gives this average surprise its proper name, the entropy, and shows that a language model is trained by making the surprise of the real next word small. For today it is one more use of the same expectation formula. The numbers are illustrative.')))

    S.append(dict(kind='formula', title='Variance and standard deviation measure how far values lie from the mean',
                  formulas=[('Variance', r'$\mathrm{Var}(X) = \sigma^2 = \sum_x (x-\mu)^2\,p(x)$'), ('Standard deviation', r'$\sigma = \sqrt{\mathrm{Var}(X)}$'),
                            ('Shortcut', r'$\mathrm{Var}(X) = E(X^2) - \mu^2$')],
                  symbols=[['Var(X)', 'Variance: average squared distance from mu (units of X squared).', f'{VAR_DIE:.4f}'],
                           ['sigma', 'Standard deviation: the square root, in the units of X.', f'{SD_DIE:.4f}'],
                           ['x - mu', 'How far one value lies from the expectation.', 'for 6: 6 - 3.5 = 2.5'],
                           ['E(X²)', 'The expectation of X squared: sum of x² times p(x).', 'die: 15.1667 - 12.25 = 2.9167']],
                  widths=[1.9, 5.6, 4.4], size=18, note='We square the distances so that below-mean and above-mean values do not cancel. Again no n: the weights are p(x).',
                  notes=('Expectation tells us the centre. Variance tells us the spread. For each value take its distance from the mean, square it, weight it by its probability, and add. '
                         'We square so that values below and above the mean do not cancel each other. The standard deviation, sigma, is the square root of the variance, and it has the same units as X, which makes it easier to read. '
                         'The shortcut uses the expectation of X squared from the previous formula slide: 91 over 6 is 15.1667, minus 3.5 squared, 12.25, gives 2.9167. The direct route gives the same number, and we check it by hand.')))

    rows = [[str(int(x)), f'{x - E_DIE:+.1f}', f'{(x - E_DIE) ** 2:.2f}'] for x in FACES]
    S.append(dict(kind='idea', title=f'By hand: the variance of a fair die is 35/12, about {VAR_DIE:.2f}',
                  visual=dict(kind='sheet', headers=['x', 'x - 3.5', '(x - 3.5) squared'], rows=rows, hl=[5, 2]),
                  lead='Each face has p(x) = 1/6, so add the last column and divide by 6.',
                  points=[f'Sum of the last column = {sum((x - E_DIE) ** 2 for x in FACES):.2f}.', f'Variance = 17.5 / 6 = {VAR_DIE:.4f}.',
                          f'Standard deviation = square root = {SD_DIE:.4f}: a root-mean-square distance from 3.5.'],
                  notes=('The die by hand. Column one is the face. Column two is its distance from 3.5, and column three squares that distance. The ends, 1 and 6, are 2.5 away, and squared that gives 6.25. '
                         'The middle faces are only half a unit away, which gives 0.25. Add the six squared distances and you get 17.5. Every face has probability one sixth, so divide by six. The variance is 2.9167, and the standard deviation is 1.7078. '
                         'The standard deviation is a root-mean-square distance from 3.5. The plain average distance is 1.5, a little smaller, because squaring gives the far faces more weight.')))

    S.append(dict(kind='compare', title='A whole population divides by n, and a sample by n\u00a0-\u00a01',
                  left=dict(head='Sample: divide by n - 1', icon='check', points=['Default since Session 5', 'np.var(x, ddof=1)', 'VAR.S, STDEV.S, COVARIANCE.S']),
                  right=dict(head='Population: divide by n', icon='flag', points=['The list is all there is', 'np.var(x)', 'VAR.P, STDEV.P, COVARIANCE.P']),
                  verdict=f'Distances from x̄ come out a little small; n - 1 corrects it. Var(y): {VY:g} or {VY_P:g}.',
                  notes=('The die had known probabilities. A list of data does not, so give each of the n rows probability one over n. The expectation becomes the plain average, x bar, and the variance becomes the average squared distance, dividing by n. '
                         'That is right when the list is the whole population. Usually it is a sample, and the distances are measured from x bar, which was fitted to the same rows, so they come out slightly small. Dividing by n minus one corrects that. '
                         'Session 5 divided by n minus one, and this course keeps that default for data and always says which. In NumPy np.var divides by n unless you write ddof equals 1, while np.cov and pandas divide by n minus one unless told otherwise.')))

    S.append(dict(kind='idea', title='Covariance asks whether two columns rise and fall together',
                  visual=dict(kind='e_cov', points=[[float(a), float(b)] for a, b in zip(X, Y)], mx=float(MX), my=float(MY), xlabel='hours of study per week, x', ylabel='quiz score out of 10, y',
                              xticks=[1, 3, 5, 7], yticks=[2, 4, 6, 8, 10]),
                  lead='Illustrative: six learners. Dashed red lines: the two means. Shaded corners: product above 0.',
                  points=['Dark dot: both above or both below the means. Product positive.', 'Open dot: product negative.', 'Per learner: (x - x̄)(y - ȳ). Add, divide by n - 1. Session 5 put it in a matrix.'],
                  notes=('Two columns at once. Six learners, with the hours they study per week across and the quiz score up. These numbers are illustrative. '
                         'The two dashed lines are the means, and they cut the picture into four corners. A dark dot sits top right or bottom left: both values above average, or both below. '
                         'Those dots add positive amounts. For each learner we multiply the distance from the mean of x by the distance from the mean of y, then add the products and divide by n minus one, because six learners are a sample. An open dot pulls the total down. '
                         'You met this number in Session 5, off the diagonal of the covariance matrix.')))

    rows = [[f'{x:g}', f'{y:g}', f'{x - MX:+g}', f'{y - MY:+g}', f'{p:+g}'] for x, y, p in zip(X, Y, PROD)] + [['', '', '', 'sum', f'{PROD.sum():g}']]
    S.append(dict(kind='idea', title=f'By hand: the sample covariance of the six learners is 25 / 5 = {COV:g}',
                  visual=dict(kind='sheet', headers=['x', 'y', 'x - 4', 'y - 6', 'product'], rows=rows, hl=[6, 4], size=18),
                  lead='The means are x̄ = 4 hours and ȳ = 6 points. Multiply the two distances for every learner.',
                  points=[f'Sample covariance = {PROD.sum():g} / (6 - 1) = {COV:g}.', f'Sample variances: x {VX:g}, y {VY:g}.', f'Correlation = {COV:g} / ({sd_x:.3f} × {sd_y:.3f}) = {CORR:.3f}.'],
                  notes=('The hand calculation. The mean of x, written x bar, is four hours, and the mean of y, y bar, is six points. For each learner we take the distance from each mean and multiply the two. '
                         'The first learner is three below on hours and two below on score, so the product is plus six. The third learner studied little but scored high, so the product is minus two. '
                         f'The six products add to 25. Six learners are a sample, so divide by n minus one, five, and the covariance is {COV:g}. Two negative products keep it smaller than if every learner had moved together.')))

    S.append(dict(kind='formula', title='Covariance and correlation: how two columns move together',
                  formulas=[('Sample covariance', r'$\mathrm{Cov}(x,y) = \frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y})$'), ('Correlation', r'$r = \frac{\mathrm{Cov}(x,y)}{s_x\,s_y}$')],
                  symbols=[['Cov(x, y)', 'Sum of the products of the two distances, divided by n - 1.', f'{COV:g} (hours × points)'],
                           ['x̄, ȳ', 'The mean of each column.', f'{MX:g} and {MY:g}'],
                           ['s_x, s_y', 'The sample standard deviations (also divide by n - 1).', f'{sd_x:.3f} and {sd_y:.3f}'],
                           ['r', 'Covariance divided by both standard deviations. No units, between -1 and +1.', f'{CORR:.3f}']],
                  widths=[1.9, 5.7, 4.3], size=20, note='The n - 1 cancels top and bottom, so r is the same with either divisor. Cov of a column with itself is its variance.',
                  notes=('Two formulas. The sample covariance adds the products of the distances from the means and divides by n minus one, the same formula as Session 5. Its units are hours times points, which is hard to interpret. '
                         'Correlation fixes that. Divide the covariance by both standard deviations and the units cancel. The result always lies between minus one and plus one. '
                         f'For our six learners it is {CORR:.3f}: a fairly strong positive link. The n minus one appears in the top and in the bottom, so it cancels, and r is the same whichever divisor you use. And the covariance of a column with itself is its variance, the diagonal of the Session 5 matrix.')))

    S.append(dict(kind='idea', title='Correlation runs from -1 to 1, and it only sees straight-line patterns',
                  visual=dict(kind='e_corr', panels=[dict(kind='neg', caption='falls together'), dict(kind='none', caption='no pattern'), dict(kind='pos', caption='rises together')]),
                  lead='Each panel shows 40 made-up points and their correlation r.',
                  points=['r near +1: the columns rise together.', 'r near -1: one rises as the other falls.', 'r near 0: no straight-line trend.'],
                  notes=('Correlation as a picture. Forty made-up points in each panel. On the left the columns move in opposite directions, so r is close to minus one. '
                         'In the middle the dots form a cloud with no trend, and r is near zero. On the right they rise together and r is close to plus one. '
                         'Correlation is a single number that summarises the straight-line trend. That is useful, and it is also its limit, as the next picture shows.')))

    S.append(dict(kind='idea', title='Common mistake: a correlation near 0 does not mean the columns are unrelated',
                  visual=dict(kind='e_corr', panels=[dict(kind='curve', caption='clear U shape'), dict(kind='none', caption='no pattern at all')]),
                  lead='Both panels have r close to 0. Only the right one has no relationship.',
                  points=['Correlation measures straight-line trends only.', 'A strong curve can still give r near 0.', 'High correlation does not prove that one column causes the other.'],
                  notes=('A common mistake. Both of these panels have a correlation near zero. The right panel is a cloud with no pattern. The left panel has a perfect U shape, a very strong relationship, but no straight line. '
                         'Correlation cannot see curves. So always draw the scatter plot before you trust the number. One more caution: even a high correlation does not show that one column causes the other. '
                         'Ice cream sales and sunburn both rise in summer. Which hidden factor links them?')))

    S.append(dict(kind='code', title='Bridge: expectation, variance, covariance and correlation in NumPy',
                  code='import numpy as np\nx = np.array([1, 2, 3, 5, 6, 7])\ny = np.array([4, 2, 8, 5, 7, 10])\nnp.mean(x), np.var(x, ddof=1), np.std(x, ddof=1)\nnp.cov(x, y)[0, 1]\nnp.corrcoef(x, y)[0, 1]',
                  reads=['Lines 2 and 3: the two columns as arrays.', 'Line 4: mean, then sample variance and standard deviation. ddof=1 divides by n - 1.', 'Line 5: np.cov gives a 2 by 2 matrix and divides by n - 1. Row 0, column 1 is Cov(x, y).',
                         'Line 6: np.corrcoef gives the correlation matrix. Same entry is r.', 'Spreadsheet: AVERAGE, VAR.S, STDEV.S, COVARIANCE.S and CORREL.'],
                  notes=('The same work in code. Two arrays, x and y. NumPy has mean, var and std. Without ddof equals one, var and std divide by n, so we add it to get the sample versions. '
                         'For covariance we call np.cov. It divides by n minus one already, and it returns a small matrix, the covariance matrix of Session 5. The covariance of x and y is the entry in row zero, column one. np.corrcoef gives the correlation matrix in the same shape. '
                         'In the spreadsheet you use AVERAGE, VAR.S, STDEV.S, COVARIANCE.S and CORREL, and you see the same numbers in both tools.')))

    S.append(dict(kind='code', title='Bridge: simulate dice with a fixed seed so everyone gets the same rolls',
                  code='rng = np.random.default_rng(13)\nrolls = rng.integers(1, 7, size=60)\nrolls.mean(), rolls.var(ddof=1)\nrng = np.random.default_rng(13)\nbig = rng.integers(1, 7, size=10000)\nbig.mean(), big.var(ddof=1)',
                  reads=['Line 1: a random number generator. Seed 13 fixes the sequence.', 'Line 2: 60 whole numbers from 1 to 6 (7 is excluded).',
                         f'Line 3: 60 rolls give a noisy mean ({M60:.4f}) and sample variance ({V60:.4f}).', 'Lines 4 to 6: start the generator again; 10,000 rolls come much closer to 3.5 and 2.9167.', 'Spreadsheet: the 60 rolls are fixed values, so nothing changes.'],
                  notes=('Simulation means letting the computer roll the dice for us. The generator with seed thirteen gives the same sequence on every machine, so your numbers match mine. '
                         f'The call integers from one to seven gives whole numbers from one to six, because the upper limit is not included. Sixty rolls give a noisy mean, here {M60:.4f}, and a sample variance of {V60:.4f}. '
                         'Line four starts the generator again from seed thirteen, as the notebook does, so your ten thousand rolls match your neighbour\'s. They come much closer to 3.5 and 2.9167. In the spreadsheet we paste fixed rolls, so the numbers stay put.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the concepts. Please close the slides and open either the Python notebook or the spreadsheet workbook. Both use the same numbers, so you can compare with a neighbour who chose the other tool. '
                         'In each step, predict first, then run, then read the output, then change one thing. I will walk around. Raise your hand if a cell gives an error.')))

    S.append(dict(kind='steps', title='The lab has five stages, in Python and in the spreadsheet',
                  steps=[dict(head='1 Two dice', text='Count the outcomes whose sum is 7', icon='grid'), dict(head='2 One die', text='E(X) and variance by formula', icon='calculator'),
                         dict(head='3 Simulate', text='60 fixed rolls, then 10,000 in Python', icon='gear'), dict(head='4 Next words', text='Softmax, then the expected surprise', icon='speech'),
                         dict(head='5 Two columns', text='Sample covariance and correlation', icon='chart')], highlight=2,
                  caption='Python: notebook "Probability basics". Spreadsheet: workbook with the sheets Dice, Die, Words and Covariance. Predict first, run, read, then change one thing.',
                  notes=('Five stages. Stage one, count dice outcomes. Stage two, expectation and variance of a single die, by formula. Stage three, simulate the die and compare with the formula. '
                         'Stage four, take the next-word logits through softmax and compute the expected surprise. Stage five, the sample covariance and the correlation of two columns. The spreadsheet has one sheet per stage, with gold cells for you to fill. '
                         'The Check sheet or the final cell tells you which answers are right.')))

    S.append(dict(kind='table', title='Check your numbers against these before you move on', headers=['What you compute', 'You should see'],
                  rows=[['Two dice: outcomes with sum 7, and P(sum is 7)', f'6 of 36, P = {P_SUM7:.4f}'], ['One fair die: E(X), variance, standard deviation', f'{E_DIE:g}, {VAR_DIE:.4f}, {SD_DIE:.4f}'],
                        ['The 60 fixed rolls: mean and sample variance (n - 1)', f'{M60:.4f} and {V60:.4f}'], ['Next words: P(tea), and the expected surprise in nats', f'{P_WORDS[0]:.4f} and {E_SURP:.4f}'],
                        ['x and y: sample covariance, sample variances of x and y (n - 1)', f'{COV:g}, {VX:g}, {VY:g}'], ['x and y: correlation', f'{CORR:.4f}'], ['CHANGE task: covariance dividing by n (population form)', f'{COV_P:.4f}']],
                  widths=[7.4, 4.4], icons=False, note='If your number differs, stop and find the step that went wrong. Do not change a number to match.',
                  notes=('Use this table as your checkpoint. Each row names something you compute and the number you should see. The sixty fixed rolls are the same in the notebook and in the workbook, so their mean and sample variance match exactly. '
                         'The simulation with ten thousand rolls will differ slightly from the formula, and that is expected. If a number differs from the table, stop and call me. Every later step uses the earlier ones.')))

    S.append(dict(kind='table', title='Errors you will meet, what they mean and what to do', headers=['Where', 'What you see', 'What to do'],
                  rows=[['Python', 'NameError: name x is not defined', 'A cell above was not run. Use Run all from the top.'], ['Python', f'Variance of the 60 rolls {float(ROLLS60.var()):.4f} instead of {V60:.4f}', 'np.var divided by n. Add ddof=1.'],
                        ['Spreadsheet', f'Covariance {COV_P:.4f} instead of {COV:g}', 'You used COVARIANCE.P. Use COVARIANCE.S for sample data.'], ['Spreadsheet', '#NAME? in a formula', 'A function name is misspelled, or the sheet needs the English function names.'],
                        ['Both', f'The 60 rolls give {M60:.4f}, not 3.5', 'Correct. A small sample is noisy. Only many rolls approach 3.5.']],
                  widths=[2.0, 4.8, 5.2], icons=['cross', 'cross', 'cross', 'cross', 'check'],
                  notes=('The errors you will probably meet. A name error in Python means a cell above was not run, so run all from the top. If the variance of the sixty rolls is 3.1322, np.var divided by n, so add ddof equals one. '
                         'In the spreadsheet, COVARIANCE.P gives 4.1667, the population form, and the sample answer needs COVARIANCE.S. A hash NAME error means a misspelled function. The last row is no error at all. Sixty rolls give a mean of 3.9667, and that is exactly what we want to see. '
                         'A small sample wanders, and Session 14 measures by how much.')))

    S.append(dict(kind='idea', title='Where this appears in AI: a language model gives every next token a probability',
                  visual=dict(kind='flow', steps=[dict(head='Text so far', text='Turned into tokens', icon='doc'), dict(head='Model', text='One logit per token in the vocabulary', icon='robot'),
                                                  dict(head='Softmax', text='Probabilities that add up to 1', icon='chart'), dict(head='Choose', text='Pick the next token', icon='check')], highlight=2),
                  lead='Language models of this kind output a probability mass function over the whole vocabulary.',
                  points=['Published transformers end in a softmax over the vocabulary.', 'Llama 2 (open): 32,000 tokens in the vocabulary.', 'Closed products do not publish details.'],
                  notes=('Today in real systems. The published transformer design ends with one score, a logit, for every token in its vocabulary. Softmax turns those scores into a probability mass function that adds to one. '
                         'The open model Llama 2, for example, has a published vocabulary of 32,000 tokens. ChatGPT, Gemini and Claude are products built on models of this kind, but their exact details are not public. '
                         'So we use the published design and open models to show the same mathematics. Next session shows how a program draws one token from this list.')))

    S.append(dict(kind='idea', title='Where this appears in AI: mean and standard deviation rescale numbers inside the model',
                  visual=dict(kind='flow', steps=[dict(head='A vector', text='Numbers inside one layer', icon='grid'), dict(head='Subtract the mean', text='Centre it on zero', icon='calculator'),
                                                  dict(head='Divide by sigma', text='Standard deviation of the vector', icon='bars'), dict(head='Rescaled', text='Easier for the next layer', icon='check')], highlight=2),
                  lead='The original transformer uses layer normalisation: each vector is centred and scaled with its own mean and standard deviation.',
                  points=['Layer normalisation: Ba, Kiros and Hinton, 2016. It divides by n: the vector is the whole population.', 'Some newer open models use a variant (RMSNorm) that scales without centring.'],
                  notes=('Expectation and variance are not only for dice. The published transformer design uses layer normalisation, a step from a 2016 paper by Ba, Kiros and Hinton. '
                         'Inside a layer, each vector of numbers is shifted by its own mean and divided by its own standard deviation. That keeps the numbers in a friendly range, which helps training. '
                         'The vector is the whole list, nothing is estimated from a sample, so the published step divides by n, the population form. Some newer open models, Llama among them, use a variant called RMSNorm that scales without centring.')))

    S.append(dict(kind='practice', title='Where this appears in AI: check an assistant with your numbers', minutes=8, label='Check an AI assistant',
                  task='Ask an AI assistant for the covariance and correlation of your six pairs.',
                  steps=['Type x = 1, 2, 3, 5, 6, 7 and y = 4, 2, 8, 5, 7, 10.', 'Ask for the covariance, the correlation and the divisor.', f'Compare with {COV:g} and {CORR:.3f}.',
                         f'If it says {COV_P:.3f}, it divided by n.', 'Never paste confidential data.'],
                  output='A note: its value, your value, match or not.',
                  notes=('A short activity. Open any AI assistant and give it our six pairs. Ask for the covariance and the correlation, and ask which divisor it used. '
                         f'Then compare with your lab. Assistants sometimes make arithmetic mistakes, and sometimes divide by n, which gives {COV_P:.3f} instead of {COV:g}. Both are right for their own formula, so the useful skill is to know which one it used. The correlation is 0.729 either way. '
                         'Please use only made-up data like this, and never paste confidential data into an assistant.')))

    S.append(dict(kind='table', title='Exit check: three questions', headers=['Question', 'Short answer'],
                  rows=[['A model gives probabilities 0.5, 0.3 and 0.1 to three words and nothing else is possible. What is wrong?', 'They add to 0.9. A pmf must add to exactly 1.'],
                        ['Two fair dice are independent. What is P(both show 1)?', '1/6 × 1/6 = 1/36.'],
                        ['Two columns have correlation 0.02. Are they unrelated?', 'Not necessarily. Correlation only sees straight-line trends. Draw the scatter plot.']],
                  widths=[6.6, 5.4], icons=False,
                  notes=('Three questions to finish. First, three words with probabilities 0.5, 0.3 and 0.1 and nothing else possible: they add to 0.9, so something is missing, and a probability mass function must add to exactly one. '
                         'Second, for two independent dice the probability that both show one is the product, one sixth times one sixth, one thirty-sixth. Third, correlation near zero does not mean no relationship, because correlation only sees straight lines, so draw the scatter plot. '
                         'Write your answers in your lab file.')))

    s['facilitator'] = dict(
        prep=['Open the deck and one notebook (Colab) and one workbook (Excel or Google Sheets) before the class. Run the notebook from the top once.',
              'Share the notebook and the workbook links. Both use the same fixed 60 rolls, so a learner can compare with a neighbour on the other tool.',
              f'Write the check numbers on the board: 3.5, 2.9167, {M60:.4f}, {V60:.4f}, {COV:g}, 0.729.',
              'Have six dice or a dice app ready for the opening demonstration, if you like.'],
        misconceptions=[('Probability 0.5 means the next two trials give one of each', 'It describes the long run. Each trial is independent of the last.'),
                        ('Independent means the two events cannot happen together', 'That is "mutually exclusive". Independent events can happen together; one simply does not change the other\'s probability.'),
                        ('The expectation must be a value the variable can take', 'No. E(X) = 3.5 for a die, which no face shows. It is an average.'),
                        ('Correlation 0 means no relationship', 'It means no straight-line trend. A U shape can have r near 0. Always plot.'),
                        ('A probability density f(x) is a probability, so it cannot exceed 1', 'The area is the probability. A narrow curve can have height above 1.'),
                        ('Dividing by n or by n - 1 is a matter of taste', 'n - 1 is for a sample (our default for data). n is for a whole population, or a known distribution weighted by p(x).')],
        probes=[('Why must the next-word probabilities add up to 1?', 'The model must produce some token, so the probabilities of all the possible tokens cover every case once. That is the total rule.'),
                ('Why do we subtract P(A and B) in the either-one rule?', 'Outcomes in both events were counted twice, once in each probability.'),
                ('Are die 1 and the sum of two dice independent?', 'No. Knowing die 1 = 1 rules out a sum of 12.'),
                ('Why square the distances in the variance?', 'So that values below and above the mean do not cancel, and large distances count more.'),
                ('Why does the covariance have strange units but the correlation does not?', 'Covariance multiplies the units of x and y. Correlation divides by both standard deviations, so the units cancel.'),
                ('Why n - 1 for the six learners?', 'They are a sample. Distances from their own mean come out slightly small, and n - 1 corrects that. VAR.S and COVARIANCE.S do it.')],
        lab_steps=[('Stage 1: two dice', 'Python: 6 of 36, P = 0.1667. Spreadsheet: COUNTIF on the 6 by 6 table gives 6. Watch for learners who count 7 cells or 12.'),
                   ('Stage 2: one die', 'E(X) 3.5, variance 2.9167, standard deviation 1.7078. In the spreadsheet the learner writes the column (x - E(X))^2 * p(x), then SUM.'),
                   ('Stage 3: simulation', f'The 60 fixed rolls give {M60:.4f} and a sample variance of {V60:.4f} (ddof=1, VAR.S) in both tools. 3.1322 means np.var or VAR.P (divide by n). The 10,000 Python rolls give about 3.50 and 2.91.'),
                   ('Stage 4: next words', f'Softmax of the five logits: 0.4459, 0.2989, 0.1484, 0.0737, 0.0331, sum 1. Surprises -ln p from 0.81 to 3.41. Expected surprise {E_SURP:.4f} nats.'),
                   ('Stage 5: covariance', f'Sample covariance {COV:g}, sample variances {VX:g} and {VY:g}, r 0.729. The CHANGE task (divide by n) gives {COV_P:.4f}.')],
        rescue=['If the concepts overrun, show the expected-surprise slide quickly and return to it in lab Stage 4.',
                'If learners struggle with the integral symbol, say: it is the area, and for flat curves it is width times height. No integrals are calculated in this course.',
                'If only 30 minutes remain for the lab, do stages 1, 2, 4 and 5. Set the simulation as home practice.',
                'If a learner gets different simulation numbers in Python, check that the seed line was run and that nothing else drew random numbers first.'],
        after=['Share the notebook and workbook again for absent learners.', 'Collect any question about expectation or covariance and open Session 14 with it.',
               'Remind the class that Session 14 builds on the 60 fixed rolls and on independence, so keep the notebook.'],
        lab_answer_key=[['Step 1 PREDICT: how many of the 36 outcomes have sum 7?', '6, so P = 1/6.'], ['Step 2 READ: why is E(X) = 3.5 though no face shows it?', 'It is a probability-weighted average, not a value of the variable.'],
                        ['Step 3 READ: do 60 rolls or 10,000 rolls give a mean closer to 3.5?', '10,000. The average settles as the sample grows.'],
                        ['Step 4 READ: which word has the largest surprise, and why?', 'Soup (3.41 nats): it has the smallest probability.'],
                        ['Step 5 CHANGE: divide by n instead of n - 1.', f'The covariance becomes {COV_P:.4f} (25 / 6), the variance of y becomes 7. The correlation stays 0.729.'],
                        ['Spreadsheet CHANGE: use COVARIANCE.P.', f'{COV_P:.4f}.']])
    return s
