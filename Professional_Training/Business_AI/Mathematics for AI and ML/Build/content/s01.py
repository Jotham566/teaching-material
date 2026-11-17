"""Session 1: Functions, notation and logarithms. Every number on the slides is computed here with numpy and reused by the lab files."""
import numpy as np

WORDS = ['Kampala', 'Entebbe', 'a', 'the', 'Nairobi']
P = np.array([0.62, 0.18, 0.10, 0.06, 0.04])
SENT_WORDS = ['The', 'capital', 'of', 'Uganda', 'is', 'Kampala']
SENT_P = np.array([0.30, 0.20, 0.50, 0.40, 0.70, 0.62])


def facts():
    neg_log_p = -np.log(P)
    return dict(p=P, words=WORDS, total=float(P.sum()), f3=2 * 3 + 1, ln6=float(np.log(6)), ln9=float(np.log(9)), ln2=float(np.log(2)), ln3=float(np.log(3)),
                neg_log_p=neg_log_p, avg_neg_log_p=float(np.sum(P * neg_log_p)), sent_p=SENT_P, sent_prod=float(np.prod(SENT_P)),
                sent_logsum=float(np.sum(np.log(SENT_P))), sent_avg=float(-np.mean(np.log(SENT_P))), long_logsum=float(1000 * np.log(0.2)),
                three_p=[0.30, 0.20, 0.50], three_prod=0.03, three_logsum=float(np.sum(np.log([0.30, 0.20, 0.50]))))


def build():
    F = facts()
    sp = F['neg_log_p']
    s = dict(
        num=1, block='Foundations', short_title='Functions and logarithms',
        title='Functions, notation and logarithms: why AI adds log-probabilities',
        question='A language model gives every possible next word a probability. Why does training work with the logarithm of that probability?',
        outcomes=['Read sigma notation and function notation, and evaluate both by hand',
                  'Use exponentials and logarithms, and the three log rules, to turn a product into a sum',
                  'Compute the log-probability of a word and of a sentence in Python and in a spreadsheet'],
        outcome_icons=['calculator', 'chart', 'check'],
        outcome_note=('By the end of today you can read sigma notation and function notation and work them out by hand. '
                      'You can use exponentials and logarithms, with the three log rules, to turn a product into a sum. And you can compute the log-probability of a word and of a whole sentence, in Python or in a spreadsheet, with the same answers in both. '
                      'We build up to one real question from AI, and you will be able to answer it before we leave.'),
        clock=[(10, 'Welcome and what we will do'), (35, 'Concept: a picture, then one example by hand'), (10, 'Break'), (45, 'Lab: predict, run, then change one thing'),
               (15, 'Where it appears in AI, and an exit check'), (5, 'Save the work')],
        plan_title='Your two hours: sums, functions and logarithms, then the lab, then AI',
        plan_note=('We have two hours. The first ten minutes are this welcome. Then thirty-five minutes of ideas with pictures, a break, and a forty-five minute lab where you work in Python or in a spreadsheet on the same numbers. '
                   'The last twenty minutes show where today appears in AI tools, with an exit check, and then you save your work. The lab is where the learning sticks, so please protect that time.'),
        recall_from='', recall=[],
        words=[('Sigma notation', 'The symbol Σ means add up. Sigma notation is a short way to write a long sum.'),
               ('Function', 'A rule that turns each input number into one output number, written f(x).'),
               ('Exponential function', 'A function where the input is a power, such as 2ˣ (2 to the power x). It grows by repeated multiplying.'),
               ('Logarithm (ln)', 'The inverse of an exponential. The natural logarithm ln uses the base e ≈ 2.71828.'),
               ('Log-probability', 'The natural logarithm of a probability. It is zero or negative, because a probability is at most 1.')],
        word_icons=['calculator', 'gear', 'chart', 'magnifier', 'check'],
        words_note=('Five words for today. Sigma notation is the symbol that means add up. A function is a rule from one number to one number. '
                    'An exponential function has the input as a power. A logarithm undoes it, and the natural logarithm, written ln, is the one AI uses. '
                    'And a log-probability is the natural logarithm of a probability. We use every one of them before the end of the session.'),
        keep='Keep your saved notebook or workbook, with every check on OK. Keep the one idea of the day: the logarithm of a product is the sum of the logarithms, and that is why AI adds log-probabilities.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab file', value='Saved, all checks OK'), dict(label='The idea', value='ln(u × v) = ln u + ln v'),
                                                                 dict(label='Formula sheet', value='Σ, f(x) = wx + b, log rules'), dict(label='Next session', value='Vectors')]),
        keep_title='Save your lab file and start your formula sheet',
        next='Session 2: Vectors. A row of data becomes a list of numbers that we can add, scale and compare.', next_label='Next session',
        keep_note=('Before you go, save your notebook or workbook with every check on OK. Start the one-page formula sheet that you will build across the course. Write down three things today: the sigma sum, f of x equals w x plus b, and the three log rules, each with its industry name. '
                   'Next session we turn a row of data into a vector and find out how an AI search tool measures how close two pieces of text are. If anything was unclear today, write the question down and bring it.'),
        cover_note=('Welcome to Mathematics for AI and Machine Learning. I am Jotham, and I will teach you the mathematics under modern AI, with a picture first, then a calculation by hand, then the same idea on a computer, and then where it appears in real AI tools. '
                    'Today is the first step. We learn the notation, and we meet the logarithm. By the end you will understand why training a language model uses the logarithm of a probability.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='idea', title='The sigma symbol is a short way to write a long sum',
                  visual=dict(kind='ma_sigma', values=[3, 5, 2, 8], name='x'),
                  lead='Sigma notation: the capital Greek letter Σ means add up.',
                  points=['Below Σ, i = 1 is where to start. Above Σ, the 4 is where to stop.', 'Each box is one value, x with its index i.', 'The values 3, 5, 2 and 8 add up to 18.'],
                  notes=('This is sigma notation. The big symbol is the Greek capital letter sigma, and it means add up. '
                         'Underneath it, i equals one tells you where to start counting. On top, the four tells you where to stop. Then x with a little i is the value at position i. '
                         'So this expression says add the first, second, third and fourth values. Here that is three plus five plus two plus eight, which is eighteen. '
                         'The small letter i is called the index, and it counts the position in the list. Try writing the sum of the first three values yourself: it comes to ten.')))

    S.append(dict(kind='formula', title='Sigma notation in action: the five next-word probabilities add up to 1',
                  formulas=[('General sum', r'$\sum_{i=1}^{n} x_i = x_1 + x_2 + \cdots + x_n$'),
                            ('Our five words', r'$\sum_{i=1}^{5} p_i = 0.62 + 0.18 + 0.10 + 0.06 + 0.04 = 1.00$')],
                  symbols=[['Σ (sigma)', 'Add up everything after it.', 'a sum of five numbers'], ['i', 'The index: the position in the list (1, 2, 3 ...).', 'i = 1 to 5'],
                           ['n', 'How many values there are.', 'n = 5 words'], ['pᵢ', 'The probability of word i after "The capital of Uganda is".', 'p₁ = 0.62 for Kampala']],
                  size=20, note='Illustrative (made-up numbers): Kampala 0.62, Entebbe 0.18, a 0.10, the 0.06, Nairobi 0.04.',
                  notes=('The same idea now meets the numbers we use all day. A language model has to guess the next word after the capital of Uganda is. It gives five candidate words a probability each. '
                         'A probability is a number from zero to one, where one means certain. These numbers are made up to show the arithmetic. '
                         'The sigma sum adds them: zero point six two, plus zero point one eight, plus zero point one, plus zero point zero six, plus zero point zero four. The total is exactly one, because the model must choose something. '
                         'A total of two would be a mistake: the model would be more than certain, which makes no sense.')))

    S.append(dict(kind='idea', title='A function turns each input number into exactly one output number',
                  visual=dict(kind='ma_function', rule='f(x) = 2x + 1', pairs=[(0, 1), (1, 3), (2, 5), (3, 7)]),
                  lead='A function is a rule. Give it an input x and it returns one output, written f(x).',
                  points=['Here the rule is f(x) = 2x + 1: double the input, then add 1.', 'Put in x = 3. Double it to get 6, add 1, and f(3) = 7.', 'The same input always gives the same output.'],
                  notes=('A function is a rule with one job. You give it an input, called x, and it gives back exactly one output, which we write f of x. '
                         'In this picture the rule is two x plus one. So double the input and add one. If x is three, double it to get six, add one, and f of three is seven. '
                         'The machine in the middle is the rule. The important property is that the same input always gives the same output, every time you ask. '
                         'What does f of ten give?')))

    S.append(dict(kind='idea', title='A graph draws every input and its output as a point',
                  visual=dict(kind='ma_graph', curves=[dict(fn='2*x+1', color='ink', label='f(x) = 2x + 1', lx=0.15, ly=10.3)], points=[dict(x=0, y=1, label='(0, 1)', dx=0.1, dy=0.75), dict(x=1, y=3, label='(1, 3)', dx=0.2, dy=-0.4),
                                                                                           dict(x=2, y=5, label='(2, 5)', dx=0.2, dy=-0.4), dict(x=3, y=7, label='(3, 7)', dx=0.2, dy=-0.4)],
                              xlim=(0, 5), ylim=(0, 12), yticks=[0, 2, 4, 6, 8, 10, 12], xlabel='input x', ylabel='output f(x)'),
                  lead='A graph plots each pair (x, f(x)) as a point. Joining the points draws the curve.',
                  points=['Across: the inputs x. Up: the outputs f(x).', 'Each gold dot is one pair, such as x = 3 and f(3) = 7.', 'Each step of 1 in x adds 2: a straight line.'],
                  notes=('A graph is a picture of a function. The horizontal axis holds the inputs and the vertical axis holds the outputs. Each gold dot is one pair, an input and the output the rule gave. '
                         'At x equals three the output is seven, so there is a dot at three across and seven up. Join all the dots and you get the curve of the function. '
                         'For this rule the curve is a straight line, because every step of one in x adds two to the output. That number two is the slope. With the rule three x plus one, the slope would be three.')))

    S.append(dict(kind='formula', title='The function f(x) = wx + b is the building block of machine learning',
                  formulas=[('A linear function', r'$f(x) = w\,x + b$'), ('With w = 2 and b = 1, at x = 3', r'$f(3) = 2 \times 3 + 1 = 7$')],
                  symbols=[['x', 'The input.', 'x = 3'], ['f(x)', 'The output for the input x.', 'f(3) = 7'], ['w', 'The weight: how much the output grows when x grows by 1. It is also called the slope.', 'w = 2'],
                           ['b', 'The bias (intercept): the output when the input is 0.', 'b = 1']],
                  size=26, note='w and b are parameters: numbers a model learns. In this course b always means the bias.',
                  notes=('The same function, written with letters, is the building block of machine learning. F of x equals w times x plus b. '
                         'The letter w is the weight, how much the output grows for each extra unit of input. The letter b is the bias, also called the intercept, which is the output when the input is zero. '
                         'With w equal to two and b equal to one, and x equal to three, we get seven again. In machine learning, w and b are the parameters, the numbers a model learns from data. '
                         'From today, the letter b in this course always means the bias, so whenever you see it, you know what it is.')))

    S.append(dict(kind='idea', title='An exponential function multiplies again and again, so it grows very fast',
                  visual=dict(kind='ma_graph', curves=[dict(fn='2**x', color='red', label='$2^x$', lx=3.3, ly=29)],
                              points=[dict(x=0, y=1, label='1', dx=0.15, dy=0.28), dict(x=1, y=2, label='2', dx=-0.12, dy=0.25, ha='right'), dict(x=2, y=4, label='4', dx=-0.12, dy=0.25, ha='right'), dict(x=3, y=8, label='8', dx=-0.12, dy=0.25, ha='right'),
                                      dict(x=4, y=16, label='16', dx=-0.12, dy=0.25, ha='right'), dict(x=5, y=32, label='32', dx=-0.15, dy=-0.1, ha='right')],
                              xlim=(0, 5), ylim=(0, 34), yticks=[0, 8, 16, 24, 32], xlabel='power x', ylabel='$2^x$'),
                  lead='Exponential function: the input is the power. 2ˣ means x copies of 2 multiplied together: 2³ = 2 × 2 × 2 = 8.',
                  points=['2¹ = 2, 2² = 4, 2³ = 8: each step right doubles. Each step left halves, so 2⁰ = 1.',
                          'The base e ≈ 2.71828 gives eˣ: EXP(x), np.exp(x). eˣ is always above 0: e⁻¹ ≈ 0.37.'],
                  notes=('An exponential function has the input up in the power. Two to the power x means x copies of two multiplied together, so two to the power three is two times two times two, which is eight. The values for one to five are two, four, eight, sixteen, thirty-two. '
                         'Each step to the right doubles the height. Walk the other way and each step halves, so two to the power zero is one. There is one special base in mathematics and machine learning, e, about two point seven one eight. '
                         'In a spreadsheet you write EXP, and in Python np dot exp. And e to any power is above zero, even for a negative power.')))

    S.append(dict(kind='idea', title='A logarithm undoes an exponential: it answers "which power gives this number?"',
                  visual=dict(kind='ma_graph', curves=[dict(fn='np.exp(x)', color='red', label='$e^x$', lx=-2.9, ly=3.6), dict(fn='np.log(x)', color='ink', label='ln x', lx=3.6, ly=0.35)],
                              points=[dict(x=0, y=1, label='(0, 1)', dx=-0.2, dy=0.3, ha='right'), dict(x=1, y=0, label='(1, 0)', dx=0.15, dy=-0.4)], xlim=(-3, 6), ylim=(-3, 6),
                              mirror=True, xlabel='x', ylabel='y', labels=[(4.3, 3.3, 'y = x', 'grey')]),
                  lead='The logarithm is the inverse of the exponential. If 2³ = 8, then log base 2 of 8 is 3.',
                  points=['The curves eˣ and ln x are mirror images across the dashed line y = x.', 'ln x is the natural logarithm: the logarithm with base e.', 'ln 1 = 0, because e⁰ = 1. And ln x exists only for x above 0.'],
                  notes=('A logarithm answers one question: which power gives this number? Two to the power three is eight, so the logarithm base two of eight is three. '
                         'In machine learning we almost always use the natural logarithm, written ln, which has base e. Look at the picture. The red curve is e to the x, and the black curve is ln of x. '
                         'They are mirror images across the dashed line, which is what inverse means. Look where ln of one sits: at zero. And ln only exists for numbers above zero. '
                         'What do you think happens to ln x as x gets closer and closer to zero?')))

    S.append(dict(kind='formula', title='The logarithm as a formula: the answer x is the power that gives y',
                  formulas=[('Definition, base a', r'$\log_a(y) = x \;\Longleftrightarrow\; a^{x} = y$'), ('Examples', r'$\log_2 8 = 3,\quad \log_{10} 1000 = 3,\quad \ln e = 1$')],
                  symbols=[['a', 'The base: the number that is multiplied by itself. Common bases are 2, 10 and e ≈ 2.71828. (b stays the bias.)', 'a = 2 in log₂ 8 = 3'], ['ln', 'The natural logarithm: the logarithm with base e.', 'ln 6 = 1.7918'],
                           ['y', 'The number we take the logarithm of. It must be above 0.', 'y = 8 in log₂ 8 = 3'], ['x', 'The answer: the power that a must be raised to, to give y.', 'x = 3 in log₂ 8 = 3']],
                  size=26, note='Python: np.log is natural, np.log10 is base 10. Spreadsheet: LN is natural, LOG10 is base 10.',
                  notes=('As a formula: the logarithm base a of y equals x exactly when a to the power x equals y. I call the base a, because b is kept for the bias. '
                         'So log base two of eight is three, log base ten of a thousand is three, and ln of e is one. The base is the number being multiplied. The number y must be above zero. '
                         'And the answer x is the power. Watch the names in the tools. In Python, np dot log is the natural logarithm, and the base ten one is np dot log ten. In a spreadsheet, LN is natural and LOG10 is base ten.')))

    S.append(dict(kind='idea', title='A probability lies between 0 and 1, so its natural logarithm is zero or negative',
                  visual=dict(kind='ma_graph', curves=[dict(fn='np.log(x)', color='ink', x0=0.01, label='ln p', lx=0.62, ly=-0.9)],
                              points=[dict(x=1, y=0, label='p = 1: 0', dx=-0.03, dy=0.35, ha='right'), dict(x=0.5, y=float(np.log(0.5)), label='0.5: −0.693', dx=0.04, dy=-0.4), dict(x=0.1, y=float(np.log(0.1)), label='0.1: −2.303', dx=0.05, dy=-0.4),
                                      dict(x=0.01, y=float(np.log(0.01)), label='0.01: −4.605', dx=0.2, dy=0.3)],
                              xlim=(0, 1), ylim=(-5, 1), xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[-5, -4, -3, -2, -1, 0, 1], xlabel='probability p', ylabel='ln p'),
                  lead='A certain event (p = 1) has ln p = 0. The smaller the probability, the more negative ln p.',
                  points=['p = 1 gives 0. p = 0.5 gives −0.693.', 'Minus ln p grows as p shrinks.', 'For the right word it is the loss (the number training makes small).'],
                  notes=('Logarithms and probabilities meet on this slide. A probability is between zero and one. Look at the curve of ln p on that range. At p equals one, the logarithm is zero. '
                         'At one half it is minus zero point six nine three. At one tenth it is minus two point three, and at one in a hundred it is minus four point six. The smaller the probability, the more negative the logarithm. '
                         'If we flip the sign we get minus ln p, the negative log-probability, which is positive and grows as the event gets less likely. Training calls this number the loss, the score it tries to make small, and we see it at work near the end of today.')))

    S.append(dict(kind='formula', title='Log rules: a logarithm turns multiplying into adding',
                  formulas=[('Product rule', r'$\ln(u \times v) = \ln u + \ln v$'), ('Quotient rule', r'$\ln\!\left(\frac{u}{v}\right) = \ln u - \ln v$'), ('Power rule', r'$\ln(u^{k}) = k\,\ln u$')],
                  symbols=[['u and v', 'Any two numbers above 0.', 'u = 2, v = 3'], ['k', 'Any number, used as a power.', 'k = 2'],
                           ['Product rule', 'ln 6 = ln 2 + ln 3', f'{F["ln6"]:.4f} = {F["ln2"]:.4f} + {F["ln3"]:.4f}'], ['Power rule', 'ln 9 = ln(3²) = 2 ln 3', f'{F["ln9"]:.4f} = 2 × {F["ln3"]:.4f}']],
                  size=22, note='Check the quotient rule: ln(6 ÷ 2) = ln 3 = 1.0986, and ln 6 − ln 2 = 1.7918 − 0.6931 = 1.0986.',
                  notes=('Three log rules. The product rule says the log of u times v is the log of u plus the log of v. The quotient rule says the log of u divided by v is the log of u minus the log of v. '
                         'And the power rule says the log of u to the power k is k times the log of u. All three say one thing: a logarithm turns multiplying into adding. '
                         'In the worked rows, ln six is one point seven nine one eight, the sum of ln two and ln three. And ln nine is twice ln three, two point one nine seven two, because nine is three squared. '
                         'If you know the log of ten, what is the log of a hundred?')))

    S.append(dict(kind='idea', title='Check the product rule on the curve: ln 2 plus ln 3 equals ln 6',
                  visual=dict(kind='ma_graph', curves=[dict(fn='np.log(x)', color='ink', x0=0.3, label='ln x', lx=4.2, ly=1.35)],
                              points=[dict(x=2, y=F['ln2'], label='ln 2 = 0.693', dx=0.15, dy=-0.18), dict(x=3, y=F['ln3'], label='ln 3 = 1.099', dx=0.15, dy=-0.18), dict(x=6, y=F['ln6'], label='ln 6 = 1.792', dx=-0.2, dy=0.28, ha='right')],
                              segs=[(0, F['ln2'], 2, F['ln2']), (2, 0, 2, F['ln2']), (0, F['ln3'], 3, F['ln3']), (3, 0, 3, F['ln3']), (0, F['ln6'], 6, F['ln6']), (6, 0, 6, F['ln6'])],
                              xlim=(0, 7), ylim=(0, 2.2), xticks=list(range(8)), yticks=[0, 0.5, 1, 1.5, 2], xlabel='x', ylabel='ln x'),
                  lead='Product rule check with u = 2 and v = 3: ln 2 + ln 3 should equal ln 6.',
                  points=['ln 2 = 0.6931 and ln 3 = 1.0986. Their sum is 1.7918.', 'The height of the curve at x = 6 is also 1.7918, because 2 × 3 = 6.', 'Heights on the curve add when the inputs multiply.'],
                  notes=('We can check the product rule by hand. Read the heights from the curve. The natural log of two is zero point six nine three one. The natural log of three is one point zero nine eight six. Add them and you get one point seven nine one eight. '
                         'Now read the height of the curve at six, and it is one point seven nine one eight too, because two times three is six. The rule says heights on the curve add when the inputs multiply. '
                         'This picture is the whole reason logarithms matter in AI: a long chain of multiplications becomes a chain of additions.')))

    S.append(dict(kind='wide', title='A sentence has the probability of all its words multiplied together',
                  visual=dict(kind='ma_chain', words=SENT_WORDS, probs=[float(v) for v in SENT_P], sentence_note='The lab sentence, one word at a time (illustrative: made-up probabilities)'),
                  caption='Multiply the six word probabilities for the sentence. Add their logarithms for its log-probability.',
                  notes=('This is the sentence you will use in the lab, six words, with made-up probabilities. Each word has a probability that the model gave it, knowing the words before it. The sentence probability is all six multiplied: zero point three, times zero point two, times zero point five, times zero point four, times zero point seven, times zero point six two. That is zero point zero zero five two zero eight. '
                         'Now take the natural log of each word probability and add the six numbers. We get minus five point two five seven six, and the natural log of the product is the same number. Same answer, and now only additions, which is what you want for a thousand words.')))

    S.append(dict(kind='formula', title='The log of a product is the sum of the logs: ln P is the sum of the ln pᵢ',
                  formulas=[r'$P = \prod_{i=1}^{n} p_i \quad\Longrightarrow\quad \ln P = \sum_{i=1}^{n} \ln p_i$', ('Our six words', r'$\ln P = -1.204 - 1.609 - 0.693 - 0.916 - 0.357 - 0.478 = -5.2576$')],
                  symbols=[['Π (capital pi)', 'Multiply everything that comes after it. It is the product symbol.', 'six probabilities'], ['pᵢ', 'The probability the model gave to word i, knowing the words before it.', '0.3, 0.2, 0.5, 0.4, 0.7, 0.62'],
                           ['P', 'The probability of the whole sentence.', f'{F["sent_prod"]:.6f}'], ['ln P', 'The log-probability of the sentence: zero or negative.', f'{F["sent_logsum"]:.4f}'.replace('-', '−')]],
                  size=18, note='Plain average per word: 5.2576 ÷ 6 = 0.8763 nats, the training loss (cross-entropy, Session 17).',
                  notes=('The formula has a new symbol. A capital pi means multiply, the way a capital sigma means add. So P equals the product of all the word probabilities, p one times p two, and so on up to p n. '
                         'The product rule, used again and again, says the log of P is the sum of the logs of the p values. The right side has only additions. '
                         'For our six words, the product is zero point zero zero five two zero eight, and the sum of the logs is minus five point two five seven six. Flip the sign and divide by six: the plain average per word is zero point eight seven six three. '
                         'That average over the words of a real text is the training loss of a language model, called cross-entropy, and its unit is nats because we used ln. Session seventeen returns to it.')))

    S.append(dict(kind='wide', title='A long product of probabilities shrinks to zero, but the sum of the logarithms stays usable',
                  visual=dict(kind='ma_scale'),
                  caption='A computer stores numbers down to about 10⁻³⁰⁸. Below that, a product rounds to 0 (underflow).',
                  notes=('The practical reason is about storage. A computer stores numbers only down to about ten to the minus three hundred and eight. Below that it rounds to zero, which is called underflow. '
                         'Take a text of one thousand words, where each word has probability zero point two. The product is about ten to the minus six hundred and ninety-nine, far below the limit, so the computer shows zero. '
                         'But the sum of the logarithms is one thousand times minus one point six one, which is minus one thousand six hundred and nine, an ordinary number. Real texts are long, so AI software always works with log-probabilities.')))

    S.append(dict(kind='compare', title='Common mistake: ln(u + v) differs from ln u + ln v',
                  left=dict(head='Wrong', points=['ln(2 + 3) = ln 2 + ln 3', 'That gives 1.7918, but ln 5 is 1.6094.', 'np.log is base 10.']),
                  right=dict(head='Right', points=['ln(2 + 3) = ln 5 = 1.6094.', 'ln(2 × 3) = ln 2 + ln 3 = 1.7918.', 'np.log is the natural logarithm (base e).']),
                  verdict='The log rules are for products only.',
                  notes=('This is the mistake I see most often. People read that a logarithm turns multiplying into adding, and then apply it to a sum. It does not. Take the natural log of two plus three. That is the log of five, which is one point six zero nine four. '
                         'The log of two plus the log of three is one point seven nine one eight, a different number. The rules are about products, quotients and powers only. '
                         'The second trap is about tools. In Python, np dot log is the natural logarithm, and the base ten one has its own name. Which of the two traps would catch you first?')))

    S.append(dict(kind='code', title='Read the recipe before you run it: sums, logarithms and exponentials',
                  code='p = np.array([0.62, 0.18, 0.10, 0.06, 0.04])\ntotal = np.sum(p)\nneg_log_p = -np.log(p)\nentropy = np.sum(p * neg_log_p)\nsentence_p = np.prod(word_p)\nback = np.exp(np.log(6))',
                  reads=['Line 1: the five probabilities in a list called an array.', 'Line 2: add them up, which is the sigma sum.', 'Line 3: minus ln of each one, all at once.',
                         'Line 4: each p times its minus ln p, added up: the entropy, 1.133 nats (Session 17). Spreadsheet: SUMPRODUCT.', 'Line 5: multiply all six word probabilities. Spreadsheet: =PRODUCT(B27:B32).', 'Line 6: EXP undoes LN, so you get 6 back.'],
                  notes=('Read the recipe before the lab. In Python, np dot array makes a list of numbers we can compute with. Np dot sum is the sigma sum. Minus np dot log of p takes minus ln of every probability at once. '
                         'Line four multiplies each probability by its own minus ln and adds the results. That number has a name, the entropy, one point one three three nats, and Session seventeen explains it. In a spreadsheet it is SUMPRODUCT. '
                         'Line five multiplies a whole list, np dot prod in Python and PRODUCT in a spreadsheet. The last line shows that EXP and LN undo each other.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the ideas. Everything you need is on the slides you have just seen, and the notebook and the workbook explain every step again. '
                         'Open whichever you prefer. Coders use the Python notebook in Colab. Everyone else uses the spreadsheet in Excel or Google Sheets. The numbers are the same in both. '
                         'Run the cells in order from the top, and in every step predict first. I will walk around.')))

    S.append(dict(kind='steps', title='The lab has seven steps, and each one uses a number from the slides',
                  steps=[dict(head='1 Add up', text='Sigma sum', icon='calculator'), dict(head='2 Function', text='f(3) for 2x + 1', icon='gear'),
                         dict(head='3 LN, EXP', text='ln 6, product rule', icon='chart'), dict(head='4 Minus ln p', text='Each word', icon='magnifier'),
                         dict(head='5 Entropy', text='p times minus ln p, added', icon='folder'), dict(head='6 Sentence', text='Product and sum of logs', icon='check'), dict(head='7 1000 words', text='Underflow', icon='clock')], highlight=3,
                  caption='Predict first, run, read, then change one thing. Steps 6 and 7 are the sentence of six words, then the 1000-word test.',
                  notes=('The lab has seven steps. Step one, the sigma sum of the five probabilities. Step two, the function f of three. Step three, the natural log and the product rule. '
                         'Step four, minus ln p for each candidate word. Step five, the entropy: each probability times its minus ln p, added up. Step six, a six-word sentence, once as a product and once as a sum of logs, with its plain average per word. Step seven tests a thousand words. '
                         'In every step, predict first, then run, then read the output, then change one thing. Please do not skip the predictions.')))

    S.append(dict(kind='table', title='Check your numbers before you move on',
                  headers=['What you compute', 'You should get'],
                  rows=[['Sum of the five probabilities', f'{F["total"]:.2f}'], ['f(3) for f(x) = 2x + 1', '7'], ['ln 6, and ln 2 + ln 3', f'{F["ln6"]:.4f}'],
                        ['Minus ln p for Kampala (p = 0.62)', f'{sp[0]:.3f}'], ['Entropy: sum of p times minus ln p, five words', f'{F["avg_neg_log_p"]:.3f} nats'],
                        ['Six word p: product, then sum of ln', f'{F["sent_prod"]:.6f} and ' + f'{F["sent_logsum"]:.4f}'.replace('-', '−')], ['Plain average of minus ln p per word, sentence', f'{F["sent_avg"]:.4f}'],
                        ['1000 words, p = 0.2: sum of logs', f'{F["long_logsum"]:.2f}'.replace('-', '−')]],
                  widths=[7.2, 4.0], icons=['calculator', 'gear', 'chart', 'magnifier', 'check', 'folder', 'calculator', 'clock'],
                  note='If your number differs, find the step that went wrong. Do not change a number to match.',
                  notes=('Use this table as your checkpoint. If your numbers match, carry on. If one does not, stop and call me, because later steps use the earlier ones. '
                         'The most common cause is a cell run out of order, or a minus sign missing in front of the logarithm. Do not change a number to make it match. Find out why it is different. '
                         'The Check sheet in the workbook and the last cell of the notebook do the same comparison for you, so you never have to judge a number by eye alone.')))

    S.append(dict(kind='table', title='Four messages you may meet, what they mean and what to do',
                  headers=['What you see', 'What it means', 'What to do'],
                  rows=[['nan or a RuntimeWarning from np.log, or #NUM! from LN', 'You took the log of 0 or of a negative number. A logarithm needs a number above 0.', 'Check the probabilities. None may be 0 or negative.'],
                        ['My log-probability is negative', 'That is correct. A probability below 1 has a negative natural logarithm.', 'Use minus ln p when you want a positive number.'],
                        ['The 1000-word product shows 0.0', 'Underflow: the true value is about 10⁻⁶⁹⁹, too small to store.', 'Use the sum of the logs. That is the point of the step.'],
                        ['#NAME? in a spreadsheet', 'The function name is misspelt, or your region uses a semicolon between the arguments.', 'Retype the function. Try ; instead of ,']],
                  widths=[3.6, 4.6, 3.8], icons=['cross', 'check', 'clock', 'key'],
                  notes=('Four messages you may meet. A nan, a warning, or the error hash NUM means you took the log of zero or of a negative number, so check the probabilities. '
                         'A negative log-probability is correct, because a probability below one has a negative natural log. A product that shows zero is underflow, which is exactly what step seven is about. '
                         'And hash NAME in a spreadsheet usually means a misspelt function, or a region that wants a semicolon. Read the message first. It usually tells you the answer.')))

    S.append(dict(kind='idea', title='Where this appears in AI: a probability for every possible next word',
                  visual=dict(kind='ma_nextword', words=WORDS, probs=[float(x) for x in P], highlight=0, prompt='The capital of Uganda is ...', loss=False),
                  lead='Language models of this kind give every possible next token a probability.',
                  points=['A token is a piece of text, often a word or part of a word.', 'These numbers are illustrative (made up). They add up to 1.', 'Vocabulary of open models: Llama 2, 32,000 tokens; Gemma, 256,000.'],
                  notes=('ChatGPT, Gemini, Claude and other assistants are products built on large language models. Their exact designs are not published, but published research describes how models of this kind work. '
                         'They read the text so far and give every possible next token a probability. A token is a piece of text, often a word or part of a word. '
                         'Here are five candidate tokens with made-up probabilities that add up to one. Open models publish their vocabulary size: Llama 2 has thirty-two thousand tokens and Gemma about two hundred and fifty-six thousand, and the model scores all of them at every step. '
                         'Which token would the model most likely choose here?')))

    S.append(dict(kind='idea', title='Where this appears in AI: training uses ln of the right word probability',
                  visual=dict(kind='ma_graph', curves=[dict(fn='-np.log(x)', color='red', x0=0.02, label='loss = −ln p', lx=0.38, ly=3.55)],
                              points=[dict(x=0.62, y=float(sp[0]), label='Kampala 0.62: 0.478', dx=0.04, dy=0.4), dict(x=0.18, y=float(sp[1]), label='0.18: 1.715', dx=0.04, dy=0.4), dict(x=0.04, y=float(sp[4]), label='0.04: 3.219', dx=0.04, dy=0.4)],
                              xlim=(0, 1), ylim=(0, 4), xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 1, 2, 3, 4], xlabel='probability the model gave to the right word', ylabel='loss for that word (nats)'),
                  lead='Training scores the model by minus ln p, where p is the probability it gave the word that really came next.',
                  points=['The right word is Kampala. With p = 0.62 the loss is 0.478.', 'With only p = 0.04 the loss is 3.219. A low probability on the right word gives a high loss.', 'Averaged over a text: cross-entropy (Session 17).'],
                  notes=('This graph is the link to training. Published research describes language models of this kind as trained to predict the next token. For each position in a text, the model gives a probability to the token that really came next. '
                         'The training score for that position is minus ln of that probability, called the loss. If the model gave Kampala zero point six two, the loss is zero point four seven eight. If it gave only zero point zero four, the loss is three point two one nine. '
                         'So a low probability on the right word means a high loss, and training pushes the loss down. Averaged over every word of a text, as you did for the six-word sentence, it is called the cross-entropy loss, and we meet it properly in Session seventeen.')))

    S.append(dict(kind='practice', title='Where this appears in AI: check an assistant with your numbers', minutes=8, label='Hands-on activity',
                  task='Ask any AI assistant: "What is ln 6, and what is ln 2 plus ln 3?"',
                  steps=['Use only public maths. Never paste confidential data.', 'Compare its ln 6 with your lab number, 1.7918.', 'Ask why the two answers agree. Does the reasoning match the product rule?', 'Ask the same question again. Does the answer change?'],
                  output='A note: the assistant answer, your lab number, and whether they agree.',
                  notes=('A short activity. Open any AI assistant you like. Ask it: what is ln six, and what is ln two plus ln three. Then compare its answer with the number you computed in the lab, one point seven nine one eight. '
                         'Ask it to explain why the two agree, and judge for yourself whether its explanation matches the product rule from today. Then ask the same question a second time. Does the answer stay the same? '
                         'Never paste anything confidential into an assistant. These numbers are public maths, so they are safe. Write down what you found, because we compare notes before the exit check.')))

    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers',
                  headers=['Question', 'Short answer'],
                  rows=[['What is Σ pᵢ for i = 1 to 3, when p₁ = 0.5, p₂ = 0.3 and p₃ = 0.2?', '1.0. Sigma means add: 0.5 + 0.3 + 0.2.'],
                        ['Fill the gap: ln 12 = ln 3 + ln ?', 'ln 4, because 3 × 4 = 12 and the logarithm of a product is the sum of the logarithms.'],
                        ['Why do AI programs add log-probabilities instead of multiplying probabilities?', 'A product of many small probabilities underflows to 0. A sum of logs stays an ordinary number.']],
                  widths=[5.4, 6.6], icons=['calculator', 'chart', 'check'],
                  notes=('Last, the exit check. Three questions. Write your answers in your notes before you look at mine. One, with p one equal to point five, p two point three and p three point two, what is the sigma sum? '
                         'Two, fill the gap: ln twelve equals ln three plus ln what? Three, why do AI programs add log-probabilities and not multiply probabilities? '
                         'The short answers are on the slide. If you got all three, you are ready for vectors next session. If one surprised you, look at that part of the lab again tonight.')))

    s['facilitator'] = dict(
        prep=['Open the deck, the Python notebook in Colab and the workbook in Excel or Google Sheets before anyone arrives. Run the notebook once from the top so you know it works.',
              'Share the notebook link and the workbook file. Every learner needs one of them open for the lab, and they choose by habit: coders use Python, others use the spreadsheet.',
              'Write the "check your numbers" table on the board before the lab.',
              'Have a calculator with an LN key at hand. A phone calculator in scientific mode is enough.',
              'This is the first session. Spend the welcome ten minutes on the course shape: picture, hand example, lab, then AI. Explain that there are no exams and no marks, only automatic checks that learners run for themselves, and that each learner finishes with a course project to keep.'],
        misconceptions=[('The entropy (1.133) and the per-word loss (0.876) are the same kind of average', 'The entropy weights minus ln p by p over the five candidates. The per-word loss is a plain average over the words of a real text. Session 17 links them.'),
                        ('A logarithm of a probability should be positive', 'Probabilities are at most 1, so their natural logarithms are zero or negative. We use minus ln p when we want a positive number.'),
                        ('ln(u + v) equals ln u + ln v', 'The rule is for products: ln(u × v) = ln u + ln v. The log of a sum has no simple rule.'),
                        ('np.log is the base 10 logarithm', 'np.log is the natural logarithm (base e). Base 10 is np.log10. In a spreadsheet LN is natural and LOG is base 10.'),
                        ('The probabilities of a model are chosen by a person', 'The model computes them from the text so far. In this session the numbers are made up only to show the arithmetic.')],
        probes=[('What does the index i do in sigma notation?', 'It counts the position of a value in the list, from the start value to the stop value.'),
                ('What is f(0) for f(x) = wx + b?', 'It is b, the bias or intercept.'),
                ('What power of 2 gives 8, and what is the logarithm base 2 of 8?', 'The power is 3, and that is the logarithm: log2 of 8 is 3.'),
                ('Why is ln 1 equal to 0?', 'Because e to the power 0 is 1.'),
                ('Is a low probability on the right word good for the model?', 'No. It gives a high loss (minus ln p is large), and training tries to reduce it.'),
                ('Can the log-probability of a long text be positive?', 'No. Each term is zero or negative, so the sum is zero or negative.'),
                ('Why does a computer show 0 for a product of 1000 numbers of 0.2?', 'The true value, about 10^-699, is below the smallest number it can store (about 10^-308). That is underflow.'),
                ('Does a smaller log-probability mean a more likely sentence?', 'No. A log-probability closer to 0 means a more likely sentence. More negative means less likely.')],
        lab_steps=[('Step 1: sigma sum', 'Python: np.sum(p) gives 1.0. Spreadsheet: =SUM of the five cells. Anyone who gets 0.9 or 1.1 has mistyped a probability.'),
                   ('Step 2: the function', 'f(3) = 7 in both. In the workbook the gold cell is a formula with the cell reference for x, not the typed number 3.'),
                   ('Step 3: LN and EXP', 'ln 6 = 1.7918 and ln 2 + ln 3 is the same. Python: np.log, not np.log10. Spreadsheet: LN, not LOG.'),
                   ('Step 4: minus ln p', 'Five numbers, 0.478 to 3.219, adding up to 10.528. The common slip is a missing minus sign, which gives negative numbers.'),
                   ('Step 5: entropy with SUMPRODUCT or a dot product', 'Result 1.133 nats (1.634 bits if someone uses log base 2). In the spreadsheet it is SUMPRODUCT of the p column and the minus ln p column. It is a p-weighted sum over the five candidates, unlike the plain average per word in Step 6.'),
                   ('Step 6: product against sum of logs', 'Product 0.005208 (np.prod or PRODUCT), sum of logs −5.2576, and EXP of the sum equals the product. The plain average per word is 0.876 nats: the training loss of this text.'),
                   ('Step 7: 1000 words', 'Python prints 0.0 for the product and −1609.44 for the sum of logs. The spreadsheet formula for the product may show 0 or an error, and that is the lesson.')],
        rescue=['If the concepts run over, skip the quotient rule and the power rule on the log-rules slide. The product rule is what the lab needs.',
                'If only thirty minutes of lab remain, do steps 1 to 5 and step 7, and leave the six-word sentence for homework.',
                'If a learner has no laptop, pair them with a neighbour. One computes, the other predicts aloud.',
                'If the notebook will not open, run the same cells in any Python environment that has numpy, or use the workbook.'],
        after=['Share the lab files again so absent learners can follow.', 'Remind everyone to save and to check that every line on the Check sheet or the last notebook cell says OK.', 'Note any question you could not answer and open the next session with it.'],
        lab_answer_key=[['Step 1 PREDICT: what will the five probabilities add up to?', '1.0, because the model has to pick one of the five.'],
                        ['Step 2 CHANGE: set w = 3 in f(x) = wx + b. What is f(3)?', '10. The line is steeper.'],
                        ['Step 3 READ: ln 2 + ln 3 and ln 6?', 'Both are 1.7918. The product rule works.'],
                        ['Step 4 PREDICT: which word has the biggest minus ln p?', 'Nairobi, the least likely word: 3.219.'],
                        ['Step 4 CHANGE: run p[0] = 0.9 and repeat Step 4. What happens to its minus ln p?', 'It falls to 0.105. A more confident right answer means a lower loss.'],
                        ['Step 5 PREDICT and READ: entropy near 0.5 or 3? Why do nats and bits differ?', '1.133 nats, nearer 0.5 than 3, because Kampala holds most of the probability. In bits it is 1.634: log base 2 of a number is ln of it divided by ln 2 (0.693), so the unit changes the size of the number.'],
                        ['Step 6 READ: how does exp of the sum of logs compare with the product?', 'They are equal, 0.005208.'],
                        ['Step 6c PREDICT: is the per-word loss closer to 0.1 or to 1?', 'Closer to 1: 0.876 nats per word.'],
                        ['Step 7 READ: why is the product 0.0 and the sum of logs fine?', 'The product underflows below about 10^-308. The sum of logs is −1609.44, an ordinary number.']])
    return s
