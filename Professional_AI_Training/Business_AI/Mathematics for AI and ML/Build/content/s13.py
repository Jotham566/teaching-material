"""Session 13: Probability basics. Sample space, events, random variables, pmf and pdf, expectation, variance, covariance and correlation."""
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
LENGTHS = np.array([3, 6, 5, 4, 4])


def softmax(z, T=1.0):
    e = np.exp((z - z.max()) / T)
    return e / e.sum()


P_WORDS = softmax(LOGITS)
E_LEN = float((P_WORDS * LENGTHS).sum())

X = np.array([1, 2, 3, 5, 6, 7], dtype=float)             # hours of study per week (illustrative)
Y = np.array([4, 2, 8, 5, 7, 10], dtype=float)            # quiz score out of 10 (illustrative)
MX, MY = X.mean(), Y.mean()
PROD = (X - MX) * (Y - MY)
COV = float(PROD.mean())
VX, VY = float(X.var()), float(Y.var())
CORR = float(np.corrcoef(X, Y)[0, 1])
COV_S = float(PROD.sum() / (len(X) - 1))
UNIFORM_P = (5 - 2) * 0.1


def build():
    sd_x, sd_y = VX ** 0.5, VY ** 0.5
    tw = [f'{v:.3f}' for v in P_WORDS]
    s = dict(
        num=13, block='Probability and statistics', short_title='Probability basics',
        title='Probability basics: random variables, expectation, variance and covariance',
        question='A chat model gives every possible next word a probability. What does that number mean, and why do they all add up to exactly one?',
        outcomes=['Describe a sample space, an event and a random variable, and use the rules of probability on dice',
                  'Calculate an expectation, a variance, a standard deviation, a covariance and a correlation by hand and by computer',
                  'Read a next-word probability list from a chat model as a probability mass function'],
        outcome_icons=['book', 'calculator', 'chart'],
        outcome_note=('Here is what you take away today. You can describe a sample space, an event and a random variable, and you can use the rules of probability on dice. '
                      'You can calculate an expectation, a variance, a standard deviation, a covariance and a correlation, first by hand and then by computer. '
                      'And you can read the list of next-word probabilities that a chat model produces as a probability mass function. That last one answers the question on the first slide.'),
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
               ('Probability mass function (pmf) and density function (pdf)', 'The pmf gives P(X = x) for discrete values (values you can list, such as the faces 1 to 6). The pdf is a curve, and probability is the area under it.'),
               ('Expectation', 'The probability-weighted average of X, written E(X) or mu.'),
               ('Variance and standard deviation', 'The average squared distance from mu, and its square root sigma.'),
               ('Covariance and correlation', 'How two columns move together, and the same thing scaled to lie between -1 and +1.')],
        word_icons=['question', 'chart', 'calculator', 'bars', 'grid'],
        words_note=('Five words today, and these are the real industry names. A random variable turns the outcome of chance into a number. The probability mass function and the density function describe how likely each value is. '
                    'Expectation is the probability-weighted average. Variance and standard deviation say how spread out the values are. Covariance and correlation say whether two columns move together. We define each again on the slide where it first matters.'),
        keep='Keep your saved notebook or workbook, and the five numbers from the check table: E(X) = 3.5, variance 2.9167, covariance 4.1667, correlation 0.729 and the next-word probabilities that add to 1.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Saved lab', value='Notebook or workbook'), dict(label='Five numbers', value='See the check table'),
                                                              dict(label='Next session', value='Distributions and sampling'), dict(label='Bring', value='One question about chance')]),
        keep_title='Save the lab and keep your five numbers',
        next='Session 14: distributions and sampling. We meet the Gaussian, the central limit theorem, an A/B test, and temperature and top-p sampling.', next_label='Next session',
        keep_note=('Before you go, save the notebook or the workbook, and keep the five numbers from the check table. Next session we meet the common distributions, the Gaussian above all, '
                   'and we use them to run an A/B test and to see how temperature and top-p sampling pick the next word. If anything about expectation or covariance was unclear, write down the question and bring it.'),
        cover_note=('Welcome to Session 13, and to the third pillar of the course: probability and statistics. Everything so far gave us numbers. Now we deal with chance, '
                    'which is what a language model faces every time it must pick the next word. Today is the vocabulary: random variables, expectation, variance and covariance. We use dice, a small next-word list and a small dataset.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 12', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.2, 6.8], icons=False,
                  note='If one answer surprised you, look back at Session 12 before the lab.',
                  notes=('Here are the short answers. First, a large score overflows when we take e to its power. The stable softmax subtracts the largest score first, and the probabilities do not change. '
                         'Second, regularisation adds a penalty that grows with the weights, so they stay small and overfitting is reduced. '
                         'Third, 16-bit numbers save memory and time, but in the fp16 format they top out at 65,504, so overflow comes sooner and the stable softmax matters more. The bfloat16 format keeps the range but loses precision. Check your own answers against these.')))

    S.append(dict(kind='idea', title='A sample space lists every outcome, and an event is a group of outcomes',
                  visual=dict(kind='e_grid', cells=TWO, hl=[[r, c] for r in range(6) for c in range(6) if TWO[r][c] == 7], row_label='Die 2', col_label='Die 1'),
                  lead='Two fair dice give 36 equally likely outcomes. Each cell shows the sum.',
                  points=['Sample space: the set of all possible outcomes.', 'Event: a group of outcomes we care about. Gold = the event "sum is 7".', f'P(sum is 7) = 6 / 36 = 1/6, about {P_SUM7:.3f}.'],
                  notes=('Roll two fair dice. Each cell in this table is one outcome, and the number inside is the sum of the two dice. There are thirty-six cells, and they are equally likely. '
                         'The set of all outcomes is called the sample space. An event is any group of outcomes we care about. The gold cells are the event: the sum is seven. '
                         'Six cells are gold out of thirty-six, so the probability is six over thirty-six, which is one sixth, about 0.167. Count the cells for the event "the sum is 10". What do you get?')))

    S.append(dict(kind='idea', title='Probability is a number from 0 to 1, and all the outcomes together add up to 1',
                  visual=dict(kind='e_pmf', labels=['1', '2', '3', '4', '5', '6'], values=[1 / 6] * 6, value_texts=['1/6'] * 6, xlabel='face of one fair die', total_text='6 bars of 1/6 add up to 1'),
                  lead='Probability P(A) measures how likely an event A is.',
                  points=['0 means impossible. 1 means certain.', 'For equally likely outcomes: P(A) = outcomes in A divided by all outcomes.', 'The probabilities of all the outcomes add up to 1.'],
                  notes=('A probability is a number between zero and one. Zero means the event cannot happen, and one means it is certain. When all outcomes are equally likely, the probability of an event is the number of outcomes in it, divided by the number of all outcomes. '
                         'Here is one fair die. Six faces, each with probability one sixth. And the six bars together add up to exactly one, because something must happen when you roll. '
                         'Hold on to that last sentence. It is the answer to our question from the first slide.')))

    S.append(dict(kind='formula', title='The rules of probability, checked on dice',
                  formulas=[('Range and total', r'$0 \leq P(A) \leq 1, \qquad P(\mathrm{all\ outcomes}) = 1$'), ('Complement', r'$P(\mathrm{not}\ A) = 1 - P(A)$'),
                            ('Either one', r'$P(A\ \mathrm{or}\ B) = P(A) + P(B) - P(A\ \mathrm{and}\ B)$')],
                  symbols=[['A, B', 'Two events. A = the die is even {2, 4, 6}. B = the die shows more than 4 {5, 6}.', 'one fair die'],
                           ['P(A), P(B)', 'Their probabilities: 3/6 and 2/6.', 'P(A) = 0.5, P(B) = 0.333'],
                           ['A and B', 'Both at once: only the face 6.', 'P(A and B) = 1/6'],
                           ['A or B', 'At least one: 2, 4, 5, 6. The 6 is counted once, so we subtract it once.', f'3/6 + 2/6 - 1/6 = 4/6 = {4 / 6:.3f}']],
                  widths=[1.7, 6.2, 4.0], size=22, note='Complement example: P(not even) = 1 - 3/6 = 3/6.',
                  notes=('Here are the four rules, and each one is checked on a single die. The probability is never below zero or above one. All outcomes together have probability one. '
                         'The probability that A does not happen is one minus the probability that it does. And for either one of two events, add their probabilities and subtract the overlap, because the overlap was counted twice. '
                         'Take A as even and B as more than four. The six belongs to both, so three sixths plus two sixths minus one sixth gives four sixths. Check by listing 2, 4, 5, 6.')))

    S.append(dict(kind='idea', title='A random variable turns each outcome into a number, and its pmf says how likely each number is',
                  visual=dict(kind='e_pmf', labels=[str(v) for v in range(2, 13)], values=[c / 36 for c in SUM_COUNTS], value_texts=[f'{c}/36' for c in SUM_COUNTS], hl=[5], xlabel='X = sum of two dice',
                              total_text='the 11 bars add up to 36/36 = 1', value_size=14),
                  lead='Let X be the sum of two dice. The bar heights are the probability mass function (pmf): p(x) = P(X = x).',
                  points=['A random variable X gives a number to each outcome.', 'P(X = 7) = 6/36 is the tallest bar (gold).', 'All the bars add up to 1.'],
                  notes=('A random variable is a rule that gives a number to every outcome of a chance event. Here X is the sum of two dice, so X can be any whole number from two to twelve. '
                         'The heights of the bars are the probability mass function, the pmf: for each value x, the probability that X equals x. Seven is the tallest because six of the thirty-six outcomes give it. Two and twelve are the shortest, one outcome each. '
                         'Add all eleven bars and you get thirty-six over thirty-six, which is one. What is P(X = 2)?')))

    S.append(dict(kind='idea', title='A continuous random variable has a density curve, and probability is the area under it',
                  visual=dict(kind='e_pdf', curve='uniform', lo=-1, hi=11, a=0, b=10, ymax=0.16, xticks=[0, 2, 5, 10], xlabel='minutes until the bus arrives (illustrative)',
                              shade=[dict(a=2, b=5, fill='#E0BE36')], ytick_texts=[(0.1, '0.1')],
                              notes=[dict(x=3.5, y=0.14, text='area = 3 × 0.1 = 0.3', color='#111111', size=16)]),
                  lead='A bus arrives at a random moment in a 10 minute window. This is a uniform distribution: every moment is equally likely.',
                  points=['Density f(x) (pdf): the curve, flat at 1/10 = 0.1, so total area = 10 × 0.1 = 1.', 'P(2 to 5 minutes) = width 3 × height 0.1 = 0.3.', 'P(exactly 3.000...) = 0. Only ranges have probability.'],
                  notes=('Now a random variable whose values cannot be listed. The waiting time for a bus, in a ten minute window, can be any value, so we call it continuous. For these we cannot list bars. '
                         'Instead we draw a density curve, the probability density function, the pdf. The height of the curve is not a probability. The area under the curve between two values is. '
                         'Here the curve is flat at 0.1, so the area between two and five minutes is three times 0.1, which is 0.3. The probability of one exact instant is zero. This flat curve is called a uniform distribution: every moment in the ten minutes is equally likely, so the height is one tenth and the total area is ten times 0.1, which is one. These numbers are illustrative, made up to show the arithmetic.')))

    S.append(dict(kind='formula', title='Probability mass function and density function, side by side',
                  formulas=[('pmf (discrete X)', r'$p(x) = P(X = x), \qquad \sum_x p(x) = 1$'), ('pdf (continuous X)', r'$P(a \leq X \leq b) = \int_a^b f(x)\,dx, \qquad \int f(x)\,dx = 1$')],
                  symbols=[['p(x)', 'The probability that X takes exactly the value x. Never negative.', 'die: p(x) = 1/6'],
                           ['f(x)', 'The density: the height of the curve at x. It can be above 1.', 'bus: f(x) = 0.1'],
                           ['sum', 'Add the probabilities of every possible value x.', '6 faces, total 1'],
                           ['integral', 'The area under the curve from a to b. Here we read it as width times height.', '3 × 0.1 = 0.3']],
                  widths=[1.7, 6.4, 3.8], size=24, note='Both say the same thing: the total probability is 1. Discrete values use a sum, a continuous curve uses an area.',
                  notes=('Here are the two descriptions side by side. For discrete values, which you can list, we have the pmf, written p of x, which is the probability that X equals x, and the sum over all values must be one. '
                         'For a continuous variable we have the density f of x, and the probability that X lies between a and b is the area under the curve from a to b. That area symbol is called an integral. '
                         'You do not need to calculate integrals by hand in this course. For flat curves it is width times height. The total area under the whole curve must also be one.')))

    S.append(dict(kind='idea', title='A chat model gives every possible next word a probability, and the probabilities add up to 1',
                  visual=dict(kind='e_softmax', words=WORDS, logits=[float(v) for v in LOGITS], panels=[dict(title='probability p(x)', probs=[float(v) for v in P_WORDS], sub='sum = 1.000')]),
                  lead='Illustrative (made-up numbers): next word after "For breakfast I drink hot ...".',
                  points=['Logits z: one raw score per word.', 'Softmax turns the scores into probabilities.', f'{" + ".join(tw)} = 1.'],
                  notes=('This is the answer to our question, with made-up numbers, so please treat them as illustrative. Suppose a model reads the start of a sentence, and it scores five candidate next words. '
                         'These raw scores are called logits. Softmax, which you met in Session 12, turns them into probabilities. Tea gets 0.446, coffee 0.299, and so on. '
                         'This list is a probability mass function. It is never negative, and it adds up to one, because the model must choose some word. A real model does this for every token in its vocabulary. Which word would you bet on?')))

    S.append(dict(kind='idea', title='Expectation is the probability-weighted average, the balance point of the bars',
                  visual=dict(kind='e_pmf', labels=['1', '2', '3', '4', '5', '6'], values=[1 / 6] * 6, value_texts=['1/6'] * 6, mean_at=2.5, mean_label='E(X) = 3.5', xlabel='face of one fair die'),
                  lead='Expectation E(X), also called the mean and written mu, is the value the average settles on over many repeats.',
                  points=['Picture the bars as weights on a ruler. E(X) is where it balances.', 'It need not be a possible value: no die shows 3.5.'],
                  notes=('Expectation answers the question: what would the average be if we repeated this chance event many times? Imagine the bars as weights on a ruler. The expectation is the point where the ruler balances. '
                         'For a fair die it is exactly in the middle, 3.5. Notice that you can never roll a 3.5. The expectation is an average over many rolls and says nothing certain about one roll. '
                         'Statisticians also call it the mean and write it mu. If the bars were not equal, which way would the balance point move?')))

    S.append(dict(kind='formula', title='Expectation: add up each value times its probability',
                  formulas=[('Expectation', r'$E(X) = \mu = \sum_x x\,p(x)$'), ('Fair die', r'$E(X) = 1\cdot\frac{1}{6} + 2\cdot\frac{1}{6} + \cdots + 6\cdot\frac{1}{6} = \frac{21}{6} = 3.5$')],
                  symbols=[['E(X), mu', 'The expectation (mean) of the random variable X.', f'{E_DIE:g}'],
                           ['x and p(x)', 'One possible value of X, and its probability.', 'face 1 to 6, 1/6 each'],
                           ['sum', 'Add the products x times p(x) over all values.', 'six terms']],
                  widths=[1.9, 6.0, 4.0], size=20,
                  note=f'Next-word example (illustrative): lengths 3, 6, 5, 4, 4 letters give E(length) = {E_LEN:.2f} letters.',
                  notes=('The formula says: multiply each possible value by its probability, and add. For the die each face has probability one sixth, so we get twenty-one sixths, which is 3.5. '
                         f'The same formula works on any pmf. Take our five next words, with lengths of three, six, five, four and four letters. Weight each length by its probability and you get {E_LEN:.2f} letters. '
                         'That is the expected length of the next word, in the toy model. Try the first two terms yourself: three times 0.446, plus six times 0.299.')))

    S.append(dict(kind='formula', title='Variance and standard deviation measure how far values lie from the mean',
                  formulas=[('Variance', r'$\mathrm{Var}(X) = \sigma^2 = \sum_x (x-\mu)^2\,p(x)$'), ('Standard deviation', r'$\sigma = \sqrt{\mathrm{Var}(X)}$'),
                            ('Shortcut', r'$\mathrm{Var}(X) = E(X^2) - \mu^2$')],
                  symbols=[['Var(X)', 'Variance: average squared distance from mu (units of X squared).', f'{VAR_DIE:.4f}'],
                           ['sigma', 'Standard deviation: the square root, in the units of X.', f'{SD_DIE:.4f}'],
                           ['x - mu', 'How far one value lies from the expectation.', 'for 6: 6 - 3.5 = 2.5'],
                           ['E(X^2)', 'The expectation of X squared: sum of x squared times p(x).', 'die: 15.1667 - 12.25 = 2.9167']],
                  widths=[1.9, 5.6, 4.4], size=18, note='We square the distances so that below-mean and above-mean values do not cancel.',
                  notes=('Expectation tells us the centre. Variance tells us the spread. For each value take its distance from the mean, square it, weight it by its probability, and add. '
                         'We square so that values below and above the mean do not cancel each other. The standard deviation, sigma, is the square root of the variance, and it has the same units as X, which makes it easier to read. '
                         'There is also a shortcut: the expectation of X squared, minus mu squared. For the die the expectation of X squared is 91 over 6, which is 15.1667, minus 12.25, and both routes give 2.9167. Next we do it by hand.')))

    rows = [[str(int(x)), f'{x - E_DIE:+.1f}', f'{(x - E_DIE) ** 2:.2f}'] for x in FACES]
    S.append(dict(kind='idea', title=f'By hand: the variance of a fair die is 35/12, about {VAR_DIE:.2f}',
                  visual=dict(kind='sheet', headers=['x', 'x - 3.5', '(x - 3.5) squared'], rows=rows, hl=[5, 2]),
                  lead='Each face has p(x) = 1/6, so add the last column and divide by 6.',
                  points=[f'Sum of the last column = {sum((x - E_DIE) ** 2 for x in FACES):.2f}.', f'Variance = 17.5 / 6 = {VAR_DIE:.4f}.', f'Standard deviation = square root = {SD_DIE:.4f}.'],
                  notes=('Let us do the die by hand. Column one is the face. Column two is its distance from 3.5, and column three squares that distance. The ends, 1 and 6, are 2.5 away, and squared that gives 6.25. '
                         'The middle faces are only half a unit away, which gives 0.25. Add the six squared distances and you get 17.5. Every face has probability one sixth, so divide by six. The variance is 2.9167, and the standard deviation is 1.7078. '
                         'A typical roll lands about 1.7 away from 3.5.')))

    S.append(dict(kind='idea', title='Covariance asks whether two columns rise and fall together',
                  visual=dict(kind='e_cov', points=[[float(a), float(b)] for a, b in zip(X, Y)], mx=float(MX), my=float(MY), xlabel='hours of study per week, x', ylabel='quiz score out of 10, y'),
                  lead='Illustrative data: six learners. Dashed red lines mark the two means. Shaded corners are marked +.',
                  points=['Dark dot: both above or both below the means. Product positive.', 'Open dot: product negative.', 'Per learner: (x - mean of x) times (y - mean of y). Covariance = mean of these products.'],
                  notes=('Now two columns at once. Here are six learners, with the hours they study per week on the horizontal axis and the quiz score on the vertical axis. These numbers are illustrative. '
                         'The two dashed lines are the means, and they cut the picture into four corners. A dark dot sits in the top right or bottom left corner, which means both values are above or both below average. '
                         'Those dots add positive amounts to the covariance. For each learner we multiply the distance from the mean of x by the distance from the mean of y, and the covariance is the mean of those products. An open dot sits in the other corners and pulls it down. Most dots here are dark, so the covariance is positive.')))

    rows = [[f'{x:g}', f'{y:g}', f'{x - MX:+g}', f'{y - MY:+g}', f'{p:+g}'] for x, y, p in zip(X, Y, PROD)] + [['', '', '', 'sum', f'{PROD.sum():g}']]
    S.append(dict(kind='idea', title=f'By hand: the covariance of the six learners is 25/6, about {COV:.3f}',
                  visual=dict(kind='sheet', headers=['x', 'y', 'x - 4', 'y - 6', 'product'], rows=rows, hl=[6, 4], size=18),
                  lead='The means are 4 hours and 6 points. Multiply the two distances for every learner.',
                  points=[f'Covariance = {PROD.sum():g} / 6 = {COV:.4f}.', f'Variance of x = {VX:.4f}. Variance of y = {VY:g}.', f'Correlation = {COV:.4f} / ({sd_x:.3f} × {sd_y:.3f}) = {CORR:.3f}.'],
                  notes=('Here is the hand calculation. The mean of x is four hours and the mean of y is six points. For each learner we take the distance from each mean and multiply the two. '
                         'The first learner is three below on hours and two below on score, so the product is plus six. The third learner studied little but scored high, so the product is minus two. '
                         f'The six products add to 25, and 25 over 6 is {COV:.4f}. That is the covariance. Because two products are negative, the answer is smaller than if all had moved together.')))

    S.append(dict(kind='formula', title='Covariance and correlation: how two columns move together',
                  formulas=[('Covariance', r'$\mathrm{Cov}(X,Y) = \frac{1}{n}\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y})$'), ('Correlation', r'$r = \frac{\mathrm{Cov}(X,Y)}{\sigma_X\,\sigma_Y}$')],
                  symbols=[['Cov(X, Y)', 'The mean of the products of the two distances.', f'{COV:.4f} (hours × points)'],
                           ['x-bar, y-bar', 'The mean of each column.', f'{MX:g} and {MY:g}'],
                           ['sigma X, Y', 'The two standard deviations.', f'{sd_x:.3f} and {sd_y:.3f}'],
                           ['r', 'Covariance divided by both standard deviations. No units, between -1 and +1. (rho: same, for a population.)', f'{CORR:.3f}']],
                  widths=[1.9, 5.7, 4.3], size=20, note='This course divides by n (population form). Cov of a column with itself is its variance.',
                  notes=('Here are the two formulas. Covariance is the average of the products of the distances from the means. The rho symbol is the same quantity for a whole population, and r is the one computed from data. Its units are the units of x times the units of y, so here hours times points, which is hard to interpret. '
                         'Correlation fixes that. Divide the covariance by both standard deviations and the units cancel. The result always lies between minus one and plus one. '
                         f'For our six learners it is {CORR:.3f}: a fairly strong positive link. Notice a useful fact. The covariance of a column with itself is its variance.')))

    S.append(dict(kind='idea', title='Correlation runs from -1 to +1, and it only sees straight-line patterns',
                  visual=dict(kind='e_corr', panels=[dict(kind='neg', caption='falls together'), dict(kind='none', caption='no pattern'), dict(kind='pos', caption='rises together')]),
                  lead='Each panel shows 40 made-up points and their correlation r.',
                  points=['r near +1: the columns rise together.', 'r near -1: one rises as the other falls.', 'r near 0: no straight-line trend.'],
                  notes=('Here is correlation as a picture. Forty made-up points in each panel. On the left the columns move in opposite directions, so r is close to minus one. '
                         'In the middle the dots form a cloud with no trend, and r is near zero. On the right they rise together and r is close to plus one. '
                         'Correlation is a single number that summarises the straight-line trend. That is useful, and it is also its limit, as the picture after this one shows.')))

    S.append(dict(kind='idea', title='Common mistake: a correlation near 0 does not mean the columns are unrelated',
                  visual=dict(kind='e_corr', panels=[dict(kind='curve', caption='clear U shape'), dict(kind='none', caption='really no pattern')]),
                  lead='Both panels have r close to 0. Only the right one has no relationship.',
                  points=['Correlation measures straight-line trends only.', 'A strong curve can still give r near 0.', 'High correlation does not prove that one column causes the other.'],
                  notes=('A common mistake. Both of these panels have a correlation near zero. The right panel is a cloud with no pattern. The left panel has a perfect U shape, a very strong relationship, but not a straight line. '
                         'Correlation cannot see curves. So always draw the scatter plot before you trust the number. And one more caution. Even a high correlation does not show that one column causes the other. '
                         'Ice cream sales and sunburn both rise in summer. Which hidden factor links them?')))

    S.append(dict(kind='compare', title='Two versions of variance: divide by n or divide by n minus 1',
                  left=dict(head='Population: divide by n', icon='check', points=['VAR.P, COVARIANCE.P', 'np.var, np.cov(bias=True)', 'This course uses this version']),
                  right=dict(head='Sample: divide by n - 1', icon='flag', points=['VAR.S, COVARIANCE.S', 'pandas .var(), .cov()', 'Used to estimate from a sample']),
                  verdict=f'Divide by n: variance of y {VY:g}, covariance {COV:.3f}. By n - 1: {Y.var(ddof=1):g} and {COV_S:g}.',
                  notes=('A trap you will meet. There are two versions of variance and covariance. The population version divides by n. The sample version divides by n minus one, and it is used when you estimate from a small sample. '
                         'Spreadsheets have both: VAR.P and VAR.S. NumPy divides by n by default, but pandas divides by n minus one by default. '
                         'In this course we divide by n, so the notebook and the workbook agree. When a tool gives you a different number, check which version it uses. Dividing by n, our covariance is 4.167 and the variance of y is 7. Dividing by n minus one, they are 5 and 8.4.')))

    S.append(dict(kind='code', title='Bridge: expectation, variance, covariance and correlation in NumPy',
                  code='import numpy as np\nx = np.array([1, 2, 3, 5, 6, 7])\ny = np.array([4, 2, 8, 5, 7, 10])\nnp.mean(x), np.var(x), np.std(x)\nnp.cov(x, y, bias=True)[0, 1]\nnp.corrcoef(x, y)[0, 1]',
                  reads=['Lines 2 and 3: the two columns as arrays.', 'Line 4: mean, variance and standard deviation. np.var divides by n.', 'Line 5: np.cov gives a 2 by 2 matrix. bias=True divides by n. The entry in row 0, column 1 is Cov(x, y).',
                         'Line 6: np.corrcoef gives the correlation matrix. Same entry is r.', 'Spreadsheet: AVERAGE, VAR.P, STDEV.P, COVARIANCE.P and CORREL do the same.'],
                  notes=('Here is the same work in code. Two arrays, x and y. NumPy has mean, var and std, and var divides by n. For covariance we call np.cov with bias equals True, so it divides by n, '
                         'and it returns a small matrix. The covariance of x and y is the entry in row zero, column one. np.corrcoef gives the correlation matrix in the same shape. '
                         'In the spreadsheet you use AVERAGE, VAR.P, STDEV.P, COVARIANCE.P and CORREL. You will see the same numbers in both tools.')))

    S.append(dict(kind='code', title='Bridge: simulate dice with a fixed seed so everyone gets the same rolls',
                  code='rng = np.random.default_rng(13)\nrolls = rng.integers(1, 7, size=60)\nrolls.mean(), rolls.var()\nbig = rng.integers(1, 7, size=10000)\nbig.mean(), big.var()',
                  reads=['Line 1: a random number generator. Seed 13 fixes the sequence.', 'Line 2: 60 whole numbers from 1 to 6 (7 is excluded).',
                         'Line 3: 60 rolls give a noisy mean (here 3.9667) and variance (3.1322).', 'Lines 4 and 5: 10,000 rolls come much closer to 3.5 and 2.9167.', 'Spreadsheet: the 60 rolls are fixed values, so nothing changes.'],
                  notes=('Simulation means letting the computer roll the dice for us. The generator with seed thirteen gives the same sequence on every machine, so your numbers match mine. '
                         'The call integers from one to seven gives whole numbers from one to six, because the upper limit is not included. Sixty rolls give a noisy mean, here 3.9667, and variance, here 3.1322. '
                         'Ten thousand rolls come much closer to 3.5 and 2.9167. In the spreadsheet we avoid the volatile RAND function and paste fixed rolls instead, so the numbers stay put.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the concepts. Please close the slides and open either the Python notebook or the spreadsheet workbook. Both use the same numbers, so you can compare with a neighbour who chose the other tool. '
                         'In each step, predict first, then run, then read the output, then change one thing. I will walk around. Raise your hand if a cell gives an error.')))

    S.append(dict(kind='steps', title='The lab has five stages, in Python and in the spreadsheet',
                  steps=[dict(head='1 Two dice', text='Count the outcomes whose sum is 7', icon='grid'), dict(head='2 One die', text='E(X) and variance by formula', icon='calculator'),
                         dict(head='3 Simulate', text='60 fixed rolls, then 10,000 in Python', icon='gear'), dict(head='4 Next words', text='Softmax, then the expected length', icon='speech'),
                         dict(head='5 Two columns', text='Covariance and correlation', icon='chart')], highlight=2,
                  caption='Python: notebook "Session 13: Probability basics". Spreadsheet: workbook with the sheets Dice, Die, Words and Covariance. Predict first, run, read, then change one thing.',
                  notes=('Here is the plan for the lab. Stage one, count dice outcomes. Stage two, expectation and variance of a single die, by formula. Stage three, simulate the die and compare with the formula. '
                         'Stage four, take the next-word logits through softmax and compute an expected word length. Stage five, covariance and correlation of two columns. The spreadsheet has one sheet per stage, with gold cells for you to fill. '
                         'The Check sheet or the final cell tells you which answers are right.')))

    S.append(dict(kind='table', title='Check your numbers against these before you move on', headers=['What you compute', 'You should see'],
                  rows=[['Two dice: outcomes with sum 7, and P(sum is 7)', f'6 of 36, P = {P_SUM7:.4f}'], ['One fair die: E(X), variance, standard deviation', f'{E_DIE:g}, {VAR_DIE:.4f}, {SD_DIE:.4f}'],
                        ['The 60 fixed rolls: mean and variance', '3.9667 and 3.1322'], ['Next words: P(tea), and the expected length in letters', f'{P_WORDS[0]:.4f} and {E_LEN:.4f}'],
                        ['x and y: covariance, variance of x, variance of y', f'{COV:.4f}, {VX:.4f}, {VY:g}'], ['x and y: correlation', f'{CORR:.4f}'], ['CHANGE task: covariance dividing by n - 1', f'{COV_S:g}']],
                  widths=[7.4, 4.4], icons=False, note='If your number differs, stop and find the step that went wrong. Do not change a number to match.',
                  notes=('Use this table as your checkpoint. Each row names something you compute and the number you should see. The sixty fixed rolls are the same in the notebook and in the workbook, so their mean and variance match exactly. '
                         'The simulation with ten thousand rolls will differ slightly from the formula, and that is expected. If a number differs from the table, stop and call me. Every later step uses the earlier ones.')))

    S.append(dict(kind='table', title='Errors you will meet, what they mean and what to do', headers=['Where', 'What you see', 'What to do'],
                  rows=[['Python', 'NameError: name x is not defined', 'A cell above was not run. Use Run all from the top.'], ['Python', 'Covariance 5.0 instead of 4.1667', 'You divided by n - 1. Add bias=True to np.cov.'],
                        ['Spreadsheet', 'Result 5 instead of 4.1667', 'You used COVARIANCE.S. Use COVARIANCE.P.'], ['Spreadsheet', '#NAME? in a formula', 'A function name is misspelled, or the sheet needs the English function names.'],
                        ['Both', 'The 60 rolls give 3.9667, not 3.5', 'Correct. A small sample is noisy. Only many rolls approach 3.5.']],
                  widths=[2.0, 4.8, 5.2], icons=['cross', 'cross', 'cross', 'cross', 'check'],
                  notes=('Here are the errors you will probably meet. A name error in Python means a cell above was not run, so run all from the top. If your covariance is 5.0 instead of 4.1667, you divided by n minus one. '
                         'In the spreadsheet, COVARIANCE.S gives the same trap. A hash NAME error means a misspelled function. And the last row is not an error. Sixty rolls give a mean of 3.9667, and that is exactly what we want to see. '
                         'Why does a small sample wander away from 3.5?')))

    S.append(dict(kind='idea', title='Where this appears in AI: a language model gives every next token a probability',
                  visual=dict(kind='flow', steps=[dict(head='Text so far', text='Turned into tokens', icon='doc'), dict(head='Model', text='One logit per token in the vocabulary', icon='robot'),
                                                  dict(head='Softmax', text='Probabilities that add up to 1', icon='chart'), dict(head='Choose', text='Pick the next token', icon='check')], highlight=2),
                  lead='Language models of this kind output a probability mass function over the whole vocabulary.',
                  points=['Published transformers end in a softmax over the vocabulary.', 'Llama 2 (open): 32,000 tokens in the vocabulary.', 'Closed products do not publish details.'],
                  notes=('Here is where today appears in real systems. The published transformer design ends with one score, a logit, for every token in its vocabulary. Softmax turns those scores into a probability mass function that adds to one. '
                         'The open model Llama 2, for example, has a published vocabulary of 32,000 tokens. ChatGPT, Gemini and Claude are products built on models of this kind, but their exact details are not public. '
                         'So we use the published design and open models to show the same mathematics. Next session we study how the model then chooses from this list.')))

    S.append(dict(kind='idea', title='Where this appears in AI: mean and standard deviation rescale numbers inside the model',
                  visual=dict(kind='flow', steps=[dict(head='A vector', text='Numbers inside one layer', icon='grid'), dict(head='Subtract the mean', text='Centre it on zero', icon='calculator'),
                                                  dict(head='Divide by sigma', text='Standard deviation of the vector', icon='bars'), dict(head='Rescaled', text='Easier for the next layer', icon='check')], highlight=2),
                  lead='The original transformer uses layer normalisation: each vector is centred and scaled with its own mean and standard deviation.',
                  points=['Layer normalisation: Ba, Kiros and Hinton, 2016.', 'Some newer open models use a variant (RMSNorm) that scales without centring.'],
                  notes=('Expectation and variance are not only for dice. The published transformer design uses layer normalisation, a step from a 2016 paper by Ba, Kiros and Hinton. '
                         'Inside a layer, each vector of numbers is shifted by its own mean and divided by its own standard deviation. That keeps the numbers in a friendly range, which helps training. '
                         'It is exactly the mean and the standard deviation you computed today, applied to a long list of numbers. Some newer open models, Llama among them, use a variant called RMSNorm that scales without centring.')))

    S.append(dict(kind='practice', title='Where this appears in AI: check an assistant with your numbers', minutes=8, label='Check an AI assistant',
                  task='Ask an AI assistant for the covariance and correlation of your six pairs.',
                  steps=['Type x = 1, 2, 3, 5, 6, 7 and y = 4, 2, 8, 5, 7, 10.', 'Ask for the covariance, the correlation and the divisor.', f'Compare with {COV:.3f} and {CORR:.3f}.',
                         f'If it says {COV_S:g}, it divided by n - 1.', 'Never paste confidential data.'],
                  output='A note: its value, your value, match or not.',
                  notes=('Now a short activity. Open any AI assistant and give it our six pairs. Ask for the covariance and the correlation, and ask which formula it used. '
                         'Then compare with your lab. Assistants sometimes make arithmetic mistakes, and sometimes divide by n minus one, which gives five instead of 4.167. Both can be right for their own formula, so the useful skill is to know which one it used. '
                         'Please use only made-up data like this, and never paste confidential data into an assistant.')))

    S.append(dict(kind='table', title='Exit check: three questions', headers=['Question', 'Short answer'],
                  rows=[['A model gives probabilities 0.5, 0.3 and 0.1 to three words and nothing else is possible. What is wrong?', 'They add to 0.9. A pmf must add to exactly 1.'],
                        ['What is the expectation of a fair die, and can you roll it?', '3.5. No: it is an average, and no face shows 3.5.'],
                        ['Two columns have correlation 0.02. Are they unrelated?', 'Not necessarily. Correlation only sees straight-line trends. Draw the scatter plot.']],
                  widths=[6.6, 5.4], icons=False,
                  notes=('Three questions to finish. First, three words with probabilities 0.5, 0.3 and 0.1 and nothing else possible: they add to 0.9, so something is missing, and a probability mass function must add to exactly one. '
                         'Second, the expectation of a fair die is 3.5, and you cannot roll it, because it is an average. Third, correlation near zero does not mean no relationship, because correlation only sees straight lines, so draw the scatter plot. '
                         'Write your answers in your lab file.')))

    s['facilitator'] = dict(
        prep=['Open the deck and one notebook (Colab) and one workbook (Excel or Google Sheets) before the class. Run the notebook from the top once.',
              'Share the notebook and the workbook links. Both use the same fixed 60 rolls, so a learner can compare with a neighbour on the other tool.',
              'Write the check numbers on the board: 3.5, 2.9167, 3.9667, 4.1667, 0.729.',
              'Have six dice or a dice app ready for the opening demonstration, if you like.'],
        misconceptions=[('Probability 0.5 means the next two trials give one of each', 'It describes the long run. Each trial is independent of the last.'),
                        ('The expectation must be a value the variable can take', 'No. E(X) = 3.5 for a die, which no face shows. It is an average.'),
                        ('Correlation 0 means no relationship', 'It means no straight-line trend. A U shape can have r near 0. Always plot.'),
                        ('A probability density f(x) is a probability, so it cannot exceed 1', 'The area is the probability. A narrow curve can have height above 1.'),
                        ('Variance and standard deviation are two different things', 'The standard deviation is the square root of the variance. Same information, units that match X.')],
        probes=[('Why must the next-word probabilities add up to 1?', 'The model must produce some token, so the probabilities of all the possible tokens cover every case once. That is the total rule.'),
                ('Why do we subtract P(A and B) in the either-one rule?', 'Outcomes in both events were counted twice, once in each probability.'),
                ('Why square the distances in the variance?', 'So that values below and above the mean do not cancel, and large distances count more.'),
                ('Why does the covariance have strange units but the correlation does not?', 'Covariance multiplies the units of x and y. Correlation divides by both standard deviations, so the units cancel.'),
                ('Why do 60 rolls give 3.97 and not 3.5?', 'A small sample is noisy. The average approaches 3.5 only as the number of rolls grows. We see this properly in Session 14.'),
                ('Which version of variance does our spreadsheet use?', 'VAR.P, which divides by n. VAR.S divides by n - 1.')],
        lab_steps=[('Stage 1: two dice', 'Python: 6 of 36, P = 0.1667. Spreadsheet: COUNTIF on the 6 by 6 table gives 6. Watch for learners who count 7 cells or 12.'),
                   ('Stage 2: one die', 'E(X) 3.5, variance 2.9167, standard deviation 1.7078. In the spreadsheet SUMPRODUCT of x and p.'),
                   ('Stage 3: simulation', 'The 60 fixed rolls give 3.9667 and 3.1322 in both tools. The 10,000 Python rolls give about 3.50 and 2.91. Ask: which is closer, and why?'),
                   ('Stage 4: next words', 'Softmax of the five logits. Probabilities 0.4459, 0.2989, 0.1484, 0.0737, 0.0331 sum to 1. Expected length 4.3003.'),
                   ('Stage 5: covariance', 'Cov 4.1667, var x 4.6667, var y 7, r 0.729. The CHANGE task (divide by n - 1) gives 5.')],
        rescue=['If the concepts overrun, skip the compare slide on n versus n - 1 and return to it in the lab CHANGE task.',
                'If learners struggle with the integral symbol, say: it is the area, and for flat curves it is width times height. No integrals are calculated in this course.',
                'If only 30 minutes remain for the lab, do stages 1, 2, 4 and 5. Set the simulation as home practice.',
                'If a learner gets different simulation numbers in Python, check that the seed line was run and that nothing else drew random numbers first.'],
        after=['Share the notebook and workbook again for absent learners.', 'Collect any question about expectation or covariance and open Session 14 with it.',
               'Remind the class that Session 14 builds on the toy next-word list, so keep the notebook.'],
        lab_answer_key=[['Step 1 PREDICT: how many of the 36 outcomes have sum 7?', '6, so P = 1/6.'], ['Step 2 READ: why is E(X) = 3.5 though no face shows it?', 'It is a probability-weighted average, not a value of the variable.'],
                        ['Step 3 READ: do 60 rolls or 10,000 rolls give a mean closer to 3.5?', '10,000. The average settles as the sample grows.'],
                        ['Step 4 READ: which words are most likely, and what do the probabilities add to?', 'Tea and coffee. They add to 1.'],
                        ['Step 5 CHANGE: divide by n - 1 instead of n.', 'The covariance becomes 5.0 (25 / 5), the variance of y becomes 8.4.'],
                        ['Spreadsheet CHANGE: use COVARIANCE.S.', '5.0.']])
    return s
