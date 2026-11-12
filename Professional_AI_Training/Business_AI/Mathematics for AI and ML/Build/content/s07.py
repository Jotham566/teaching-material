"""Session 7: Derivatives. Slope of a curve, the limit idea, rules, the derivative of a squared-error loss, checking with finite differences, maxima and minima."""
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'kit'))

# ---- the numbers used on the slides, computed once here and reused in the labs
X = np.array([1.0, 2.0, 3.0, 4.0])      # distance in km (illustrative delivery data)
Y = np.array([3.0, 5.0, 6.0, 9.0])      # fee in thousand UGX
N = len(X)


def loss(w):
    return float(np.mean((w * X - Y) ** 2))


def dloss(w):
    return float(2 / N * np.sum(X * (w * X - Y)))


def fd(f, x, h):
    return (f(x + h) - f(x)) / h


def cd(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)


WSTAR = float(np.sum(X * Y) / np.sum(X * X))
L1, L2, L3, LS = loss(1), loss(2), loss(3), loss(WSTAR)
D1, D2, D3 = dloss(1), dloss(2), dloss(3)
assert abs(L1 - 11.75) < 1e-9 and abs(L2 - 0.75) < 1e-9 and abs(L3 - 4.75) < 1e-9 and abs(D1 + 18.5) < 1e-9 and abs(D3 - 11.5) < 1e-9
sq = lambda x: x ** 2
HS = [2, 1, 0.5, 0.1, 0.01, 0.001]
SLOPES = [fd(sq, 3, h) for h in HS]
prod = lambda x: x ** 2 * np.exp(x)
quo = lambda x: x ** 2 / (x + 1)
P1, Q1 = float(3 * np.e), 0.75
assert abs(cd(prod, 1, 1e-5) - P1) < 1e-4 and abs(cd(quo, 1, 1e-5) - Q1) < 1e-6
EX_F, EX_C = fd(np.exp, 1, 1e-3), cd(np.exp, 1, 1e-3)
L1001 = loss(1.001)
FD_L1 = (L1001 - L1) / 0.001
yhat1 = 1 * X
err1 = yhat1 - Y


H15, H16 = fd(sq, 3, 1e-15), fd(sq, 3, 1e-16)     # far too small a step: about 5.33, and exactly 0.0
assert abs(H15 - 6) > 0.5 and H16 == 0.0


def build():
    s = dict(
        num=7, block='Calculus and optimisation', short_title='Derivatives',
        title='Derivatives: the slope of the loss tells a model which way to change a number',
        question='A model has a number it can adjust. How does it know whether to raise it or lower it? (Session 10 answers how much.)',
        outcome_head='By the end of today you can',
        outcomes=['Find the slope of a curve at a point as change in output divided by change in input, and check it with a finite difference',
                  'Use the power, sum, product, quotient, exponential and logarithm rules',
                  'Take the derivative of a squared-error loss for a one-parameter model and say which way to move the parameter'],
        outcome_icons=['chart', 'calculator', 'flag'],
        outcome_note=('By the end of today you can do three things. First, find the slope of a curve at a point, and check that slope with ordinary arithmetic. '
                      'Second, use the standard rules for derivatives: power, sum, product, quotient, exponential and logarithm. '
                      'Third, take the derivative of a loss function for a model with one adjustable number, and read the sign of the answer to decide whether to raise or lower that number. '
                      'No calculus is assumed. We start from the idea of slope, and every rule is checked with numbers.'),
        clock=[(10, 'Recall, and a real question from AI that today answers'), (35, 'Concept: a picture, then a hand example'), (10, 'Break'),
               (45, 'Lab in Python or a spreadsheet: predict, run, change one thing'), (15, 'Where it appears in ChatGPT, Gemini, Claude; exit check'), (5, 'Save the work')],
        plan_title='Your two hours: slope, rules, the loss, then the lab',
        plan_caption='Pictures and hand examples first, then the lab on the same numbers in Python or a spreadsheet.',
        plan_note=('The two hours open with a short recall of Session 6 and the question for today. Then come thirty-five minutes of concepts, where every idea arrives as a picture and then a calculation by hand. '
                   'After the break you spend forty-five minutes in the lab, either in Python or in a spreadsheet. Both use the same numbers, so you can compare answers with the person next to you. '
                   'The last twenty minutes show where this appears in AI and give you an exit check.'),
        recall_from='Session 6',
        recall=[('What three pieces does the singular value decomposition (SVD) split a matrix into?',
                 'U, a diagonal matrix of singular values called Sigma, and V transpose. Read right to left: turn (a rotation, possibly with a flip), stretch along the axes, turn again.'),
                ('What does the first principal component in PCA point along?',
                 'The direction in which the data vary the most. Each later component is at right angles to the ones before and captures less variation.'),
                ('How can keeping only the largest singular values compress a matrix?',
                 'Keep the k largest and drop the rest. The result is a low-rank approximation that stores far fewer numbers. LoRA fine-tuning trains small matrices in the same spirit.')],
        words=[('Derivative', 'The slope of a function at one point: how fast the output changes when the input changes. Written f-prime of x or df/dx.'),
               ('Tangent line', 'The straight line that just touches a curve at one point. Its slope is the derivative there.'),
               ('Loss function', 'One number that says how wrong a model is on the data. Smaller is better. Here: the mean squared error.'),
               ('Finite difference', 'An estimate of a slope from two nearby points: change in output divided by a small change in input.'),
               ('Minimum', 'A lowest point of a curve. At a minimum, or a maximum, the slope is zero.')],
        word_icons=['chart', 'pin', 'cross', 'calculator', 'flag'],
        words_note=('Five words for today, and they are the real industry terms. A derivative is the slope of a function at one point. A tangent line is the straight line that just touches the curve there. '
                    'A loss function is one number that says how wrong a model is, and smaller is better. A finite difference is an estimate of a slope from two nearby points, and it is how we check our work. '
                    'A minimum is a lowest point, where the slope is zero. We use every one of these before the break.'),
        keep='Keep your saved lab. Write down three numbers: the loss slope -18.5 at w = 1, +11.5 at w = 3, and the best w = 2.233.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Saved lab', value='Notebook or workbook'), dict(label='Three numbers', value='-18.5, +11.5, 2.233'),
                                                              dict(label='Next session', value='The gradient'), dict(label='Bring', value='Your slope function')]),
        keep_title='Save the lab and keep three slope numbers',
        next='Session 8: partial derivatives and the gradient.', next_label='Next session',
        keep_note=('Before you go, save your notebook or workbook. Keep three numbers: the slope of the loss at w equal to one, which is minus eighteen point five, the slope at w equal to three, which is plus eleven point five, and the best w, two point two three three. '
                   'Next session the model gets two adjustable numbers, a slope and an intercept, and the single slope becomes a pair of slopes called the gradient. If anything today was unclear, write the question down and bring it.'),
        cover_note=('Welcome to Session 7. Until now this course used algebra and matrices. Today we add the first idea of calculus, the derivative, and we start from something you already know, the slope of a line. '
                    'The reason is practical. A model learns by changing its numbers a little, and the derivative of the loss tells it which way to go. '
                    'We calculate everything by hand first, and then check each answer with plain arithmetic on a computer.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 6',
                  headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.2, 6.8], icons=False,
                  note='If one answer surprised you, look back at Session 6 before the lab. Session 9 uses matrices again.',
                  notes=('The singular value decomposition splits a matrix into U, a diagonal matrix of singular values, and V transpose. Reading from the right, that is a turn, a stretch along the axes, and another turn, where a turn may include a flip. '
                         'The first principal component points along the direction in which the data vary the most. And keeping only the largest singular values gives a low-rank approximation that stores far fewer numbers. '
                         'Low-rank adaptation, or LoRA, trains small matrices in that spirit. If you answered all three, you are ready. Today the matrices rest and we meet the slope.')))

    S.append(dict(kind='idea', title='The slope of a straight line is the change in output divided by the change in input',
                  visual=dict(kind='mc_curve', fn='line', xlim=(0, 5), ylim=(0, 12), xlabel='distance x (km)', ylabel='fee (thousand UGX)', xticks=[0, 1, 2, 3, 4, 5], yticks=[0, 4, 8, 12],
                              triangle=dict(x0=1, x1=2, run='run: 1 km', rise='rise: 2'), points=[dict(x=1), dict(x=2)]),
                  lead='An illustrative delivery fee rises by 2 thousand UGX for every extra kilometre.',
                  points=['The red dashes are the run (change in input) and the rise (change in output).', 'Slope = rise divided by run = 2 divided by 1 = 2.', 'On a straight line the slope is the same everywhere.'],
                  notes=('Start with something you know from school. This straight line shows a delivery fee against distance, with made-up numbers. Move one kilometre to the right. That is the run, the change in the input. '
                         'The fee goes up by two thousand shillings. That is the rise, the change in the output. Rise divided by run is two, and that is the slope. '
                         'On a straight line the slope is the same everywhere. A curve behaves differently, and that is the first idea of today.')))

    S.append(dict(kind='idea', title='A curve has a different slope at every point, and a tangent line shows it',
                  visual=dict(kind='mc_curve', fn='square', xlim=(-3, 4), ylim=(0, 16), xticks=[-2, 0, 2, 4], yticks=[0, 4, 8, 12, 16],
                              tangents=[dict(x=-1, label='slope -2', ldx=0.35, ldy=0.9), dict(x=1, label='slope 2', ldx=-0.1, ldy=0.55, ha='right'), dict(x=3, label='slope 6', ldx=-0.25, ldy=0.1, ha='right')],
                              points=[dict(x=-1), dict(x=1), dict(x=3)]),
                  lead='The curve is f(x) = x squared. Each of the three red lines is a tangent line: the straight line that just touches the curve at one point.',
                  points=['At x = -1 the slope is -2: the curve is falling.', 'At x = 1 the slope is 2.', 'At x = 3 the slope is 6: the curve is climbing steeply.', 'The slope of the tangent line is called the derivative.'],
                  notes=('The curve f of x equals x squared falls on the left, is flat at the bottom and climbs on the right. So its slope changes from point to point. '
                         'At each gold dot I have drawn a tangent line, the straight line that just touches the curve there. At x equal to minus one the tangent slopes down with slope minus two. At x equal to three it climbs with slope six. '
                         'The slope of the tangent line at a point is called the derivative at that point. What do you expect the slope to be at x equal to zero?')))

    S.append(dict(kind='idea', title='The limit idea in one picture: shrink the step h and the secant line becomes the tangent line',
                  visual=dict(kind='mc_curve', fn='square', xlim=(0, 6), ylim=(0, 36), xticks=[0, 1, 2, 3, 4, 5, 6], yticks=[0, 10, 20, 30],
                              secants=[dict(x=3, h=2, label='h = 2: slope 8', ldx=-0.3, ldy=0.45, ha='right'), dict(x=3, h=1, label='h = 1: slope 7', ldx=-0.3, ldy=-0.45, ha='right')],
                              tangents=[dict(x=3, label='tangent: slope 6', ldx=0.35, ldy=-0.5)], points=[dict(x=3, label='x = 3', ldx=-0.3, ldy=0.45, ha='right')]),
                  lead='A secant line joins the points at x = 3 and x = 3 + h. Its slope is (f(3 + h) minus f(3)) divided by h.',
                  points=['Make h smaller and the second point slides towards the first. The secant turns into the tangent.', 'The value the slopes settle on is the derivative. Here it is 6. This is the limit idea.'],
                  notes=('Take two points on the curve: x equal to three and x equal to three plus h. The line through them is a secant line, and its slope is the change in the output divided by h. '
                         'With h equal to two the slope is eight. With h equal to one it is seven. Shrink h further and the second point slides towards the first, and the secant line rotates into the tangent line. '
                         'The slope it settles on, six, is the derivative. That settling value is what a mathematician calls the limit as h goes to zero.')))

    S.append(dict(kind='table', title='Worked by hand: for f(x) = x squared at x = 3, the slopes settle on 6',
                  headers=['Step h', 'f(3 + h)', 'f(3)', 'Slope = (f(3 + h) minus f(3)) divided by h'],
                  rows=[[f'{h:g}', f'{sq(3 + h):.7g}', '9', f'{sl:.4g}'] for h, sl in zip(HS, SLOPES)],
                  widths=[1.6, 2.4, 1.6, 6.4], icons=False,
                  note='Each slope equals 6 + h, so it approaches 6 as h shrinks. In the lab you build this table yourself, in Python and in a spreadsheet.',
                  notes=('The same idea as a table, and it is exactly what you will build in the lab. For f of x equal to x squared at x equal to three, f of three is nine. '
                         'With h equal to two, f of five is twenty-five, and twenty-five minus nine is sixteen, divided by two gives eight. With h equal to one we get seven. Half gives six and a half. '
                         'Point one gives six point one. With h equal to point zero zero one, f is nine point zero zero six zero zero one, and the slope is six point zero zero one. Each slope is exactly six plus h, so as h shrinks the slope closes in on six.')))

    S.append(dict(kind='formula', title='The derivative is the limit of the secant slope as h goes to zero',
                  formulas=[('Definition', r"$f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$"), ('Other notation', r"$df/dx = f'(x)$")],
                  symbols=[['f(x)', 'The function whose slope we want. It turns an input x into an output.', 'x squared'],
                           ['h', 'A small step in the input. The limit asks what happens as h goes to 0.', '2, 1, 0.5, 0.1 ...'],
                           ["f'(x) or df/dx", 'The derivative: the slope of the tangent line at x. Read df/dx as change in f per change in x.', "f'(3) = 6"]],
                  size=26, note='Both notations mean the same thing, and you will meet both in papers and library manuals.',
                  notes=('Written as a formula, the derivative of f at x is the limit, as h goes to zero, of f of x plus h, minus f of x, all divided by h. '
                         'That is exactly the secant slope from the table, with h shrinking. There are two notations for the answer. F prime of x is short. D f by d x reminds you that it is a change in f per change in x. '
                         'You will meet both. In our example the derivative at three is six. Say the formula aloud once, word by word.')))

    S.append(dict(kind='formula', title='Three rules cover polynomials: the power rule, the constant multiple rule and the sum rule',
                  formulas=[('Power rule', r'$\frac{d}{dx}\,x^{n} = n\,x^{n-1}$'), ('Constant multiple and sum', r"$(c\,f + g)' = c\,f' + g'$")],
                  symbols=[['n', 'The power. Bring n down in front and lower the power by one.', 'x cubed: slope 3 x squared'],
                           ['c', 'A fixed number multiplying a function. It stays in front.', 'the 3 in 3 x squared'],
                           ['f, g', 'Any two functions. The slope of a sum is the sum of the slopes.', 'f = 3 x squared, g = 2x']],
                  size=26, note='Example: f(x) = 3 x squared + 2x has f-prime(x) = 6x + 2. At x = 2 the slope is 14.',
                  notes=('Three rules do most of the work for polynomials. The power rule says the derivative of x to the n is n times x to the n minus one. Bring the power down and lower it by one. '
                         'The constant multiple rule says a fixed number in front stays in front. The sum rule says the slope of a sum is the sum of the slopes. '
                         'Put them together on three x squared plus two x. The first term gives three times two x, which is six x. The second term gives two. So the derivative is six x plus two, and at x equal to two that is fourteen. Try x equal to one.')))

    S.append(dict(kind='idea', title='The exponential e to the x is its own slope: at every point the slope equals the height',
                  visual=dict(kind='mc_curve', fn='exp', xlim=(-1, 3), ylim=(0, 21), xticks=[-1, 0, 1, 2, 3], yticks=[0, 5, 10, 15, 20],
                              tangents=[dict(x=0, label='slope 1', ldx=-0.15, ldy=0.5, ha='right'), dict(x=1, label='height and slope 2.72', ldx=-0.3, ldy=0.6, ha='right')], points=[dict(x=0), dict(x=1)]),
                  lead='e is about 2.718. The curve y = e to the x is the one whose slope at each point equals its height there.',
                  points=['Rule: the derivative of e to the x is e to the x.', 'With a constant inside, e to the 2x has slope 2 times e to the 2x. Session 9 shows why.'],
                  notes=('The exponential function e to the x is special. At x equal to zero the curve is one high and its slope is one. At x equal to one the curve is two point seven two high, and its slope is also two point seven two. '
                         'At every point the slope equals the height. So the rule is short: the derivative of e to the x is e to the x. '
                         'This tidy rule is one reason e to the x is convenient in growth models and in the softmax of Session 12, and later the sigmoid of Session 11. What would the slope be where the curve is twenty high?')))

    S.append(dict(kind='idea', title='The natural logarithm flattens out: its slope at x is 1 divided by x',
                  visual=dict(kind='mc_curve', fn='ln', xlim=(0.2, 5), ylim=(-1.8, 2.2), xticks=[1, 2, 3, 4, 5], yticks=[-1, 0, 1, 2],
                              tangents=[dict(x=1, label='slope 1', ldx=0.3, ldy=-0.5), dict(x=4, label='slope 0.25', ldx=-0.2, ldy=-0.55, ha='right')], points=[dict(x=1), dict(x=4)]),
                  lead='ln x is the natural logarithm from Session 1. It is the inverse of e to the x.',
                  points=['Rule: the derivative of ln x is 1 divided by x. At x = 1 the slope is 1. At x = 4 it is only 0.25.', 'Cross-entropy (Session 17), the loss that language models are trained with, is built from logarithms.'],
                  notes=('The natural logarithm from Session 1 rises quickly near zero and then flattens. At x equal to one the slope is one. At x equal to four the slope is only a quarter. '
                         'The rule is that the derivative of the natural logarithm of x is one divided by x. Large x means small slope, which is the flattening you can see. '
                         'This matters for AI because published language model training minimises cross-entropy, a loss made of logarithms of probabilities that Session 17 teaches. For now, keep the rule: one over x.')))

    S.append(dict(kind='idea', title='The product rule: when two quantities both change, the area of the rectangle grows in two strips',
                  visual=dict(kind='mc_product', f='f', g='g', df='Δf', dg='Δg'),
                  lead='A rectangle has width f and height g. If f grows by a small change Δf and g by a small change Δg, the area gains two strips.',
                  points=['Product rule: the derivative of f times g is f-prime times g, plus f times g-prime.', 'The tiny corner, Δf times Δg, shrinks to nothing in the limit.'],
                  notes=('Why does the product rule have two terms? Draw a rectangle with width f and height g, so its area is f times g. Now let both sides grow a little. '
                         'The width grows by a small change, delta f, which adds a strip of area delta f times g on the right. The height grows by delta g, which adds a strip of f times delta g on top. '
                         'There is also a tiny corner, delta f times delta g, but it is so small that it disappears in the limit. Divide by the small step in x and you get f prime g plus f g prime. Which strip is bigger if f is large?')))

    S.append(dict(kind='formula', title='Product and quotient rules, worked with numbers at x = 1',
                  formulas=[('Product rule', r"$(f\,g)' = f'\,g + f\,g'$"), ('Quotient rule', r"$\left(\frac{f}{g}\right)' = \frac{f'\,g - f\,g'}{g^{2}}$")],
                  symbols=[['f, g', 'Two functions of x. In the quotient rule g must not be zero.', 'f = x squared'],
                           ["f', g'", 'Their derivatives, each found with the rules before.', "f' = 2x, g' = e to the x"],
                           ['Product at x = 1', 'x squared times e to the x: (2x + x squared) e to the x.', f'3e = {P1:.3f}'],
                           ['Quotient at x = 1', 'x squared divided by (x + 1): (2x(x + 1) minus x squared) divided by (x + 1) squared.', '(4 minus 1) / 4 = 0.75']],
                  widths=[2.3, 5.8, 3.8], size=22, note='The quotient rule follows from the product and chain rules (Session 9). Use it as given and check it in the lab.',
                  notes=(f'Two more rules. The product rule says the derivative of f times g is f prime g plus f g prime. The quotient rule says the derivative of f over g is f prime g minus f g prime, all over g squared. '
                         f'Two worked cases at x equal to one. For x squared times e to the x, the derivative is two x plus x squared, times e to the x. At x equal to one that is three e, about {P1:.3f}. '
                         'For x squared divided by x plus one, the top works out to four minus one, over four, which is zero point seven five. You will confirm both with finite differences in the lab.')))

    S.append(dict(kind='idea', title='A loss function turns the errors of a model into one number',
                  visual=dict(kind='scatter', points=[(float(a), float(b)) for a, b in zip(X, Y)], xlabel='distance x (km)', ylabel='fee y (thousand UGX)', line=(0.0, 1.0), residuals=True, xlim=(0, 5), ylim=(0, 10)),
                  lead='Each dot is one delivery (made-up numbers). The model y-hat = w x has one adjustable number, w. Here w = 1.',
                  points=['The red segments are the errors: the gap between each dot and the line.', 'The loss function squares each error and takes the mean. With w = 1 the loss is 11.75. With w = 2 it is only 0.75.'],
                  notes=('All of this matters because of loss functions. Each dot is one delivery, with made-up numbers: distance in kilometres and the fee in thousand shillings. Our model has one adjustable number, w, and predicts the fee as w times the distance. '
                         'Here w equals one, and the red segments show the errors. A loss function squares each error and takes the mean, so it gives one number for how wrong the model is. '
                         'For w equal to one that number is eleven point seven five. For w equal to two it is only zero point seven five, so w equal to two is the better line.')))

    S.append(dict(kind='formula', title='The squared-error loss for a one-parameter model, with real numbers',
                  formulas=[('Loss (mean squared error)', r'$L(w) = \frac{1}{n}\sum_{i=1}^{n}\left(w\,x_i - y_i\right)^{2}$'), ('Our data at w = 1', r'$L(1) = (4 + 9 + 9 + 25)/4 = 11.75$')],
                  symbols=[['L(w)', 'The loss: the mean of the squared errors, for a given w.', f'L(1) = {L1:.2f}, L(2) = {L2:.2f}'],
                           ['w', 'The one parameter (adjustable number) of the model y-hat = w x.', 'fee per kilometre'],
                           ['x_i, y_i', 'Distance and fee of delivery i. Subscript i counts the rows.', 'x = 1, 2, 3, 4; y = 3, 5, 6, 9'],
                           ['n', 'The number of rows.', '4 deliveries']],
                  size=22, note='The errors at w = 1 are -2, -3, -3 and -5. Squared: 4, 9, 9, 25.',
                  notes=('As a formula: for each row i, the model predicts w times x i. The error is the prediction minus the actual fee y i. Square it, add up over the n rows, and divide by n. '
                         'That is the mean squared error, and we call it L of w because it depends on w. With w equal to one, the four errors are minus two, minus three, minus three and minus five. '
                         'Their squares are four, nine, nine and twenty-five, which add up to forty-seven, and forty-seven over four is eleven point seven five. Check that on your calculator before we go on.')))

    S.append(dict(kind='idea', title='The loss is a curve in w, and its lowest point is the best parameter',
                  visual=dict(kind='mc_curve', fn='loss_w', xlim=(0, 4), ylim=(0, 40), xlabel='parameter w', ylabel='loss L(w)', xticks=[0, 1, 2, 3, 4], yticks=[0, 10, 20, 30, 40],
                              points=[dict(x=1, label='w = 1: L = 11.75', ldx=0.25, ldy=0.45), dict(x=2, label='w = 2: L = 0.75', ldx=0.0, ldy=0.9, ha='center'), dict(x=3, label='w = 3: L = 4.75', ldx=0.25, ldy=-0.1)]),
                  lead='Try many values of w and plot the loss L(w). The curve is a bowl.',
                  points=['Each gold dot is one value of w and its loss.', 'Training a model means finding the w at the bottom of the bowl.'],
                  notes=('Try many values of w and plot the loss for each. You get a bowl. At w equal to one the loss is eleven point seven five. At two it is point seven five. At three it is four point seven five. '
                         'So the bottom of the bowl is somewhere near two. Finding that bottom is what training a model means. We could try values one after another, but a model with millions of numbers cannot do that. '
                         'The derivative gives a much better way: at the current w, it says which way is downhill. Where do you think the bottom is?')))

    S.append(dict(kind='idea', title='The slope of the loss tells the model which way to change w',
                  visual=dict(kind='mc_curve', fn='loss_w', xlim=(0, 4), ylim=(0, 40), xlabel='parameter w', ylabel='loss L(w)', xticks=[0, 1, 2, 3, 4], yticks=[0, 10, 20, 30, 40],
                              tangents=[dict(x=1, label='slope -18.5', ldx=0.3, ldy=0.45), dict(x=3, label='slope +11.5', ldx=-0.3, ldy=0.55, ha='right')], points=[dict(x=1), dict(x=3), dict(x=WSTAR, label='best w, slope 0', ldx=-0.3, ldy=0.65, ha='center')],
                              arrows=[dict(x0=0.9, y0=36, x1=1.7, y1=36, label='raise w', ldy=0.35), dict(x0=3.1, y0=36, x1=2.3, y1=36, label='lower w', ldy=0.35)]),
                  lead='At w = 1 the slope of the loss is -18.5: negative, so the loss falls as w grows. At w = 3 it is +11.5: positive, so the loss falls as w shrinks.',
                  points=['Move w opposite to the sign of the slope. The third gold dot, w = 2.233, is the best w, where the slope is 0.', 'A steeper slope means the loss changes more for the same step.'],
                  notes=('The red lines are tangent lines to the loss curve. At w equal to one the tangent slopes steeply downwards, with slope minus eighteen point five. '
                         'Going right makes the loss smaller, so we should raise w. At w equal to three the slope is plus eleven point five, so going right makes the loss bigger, and we should lower w. '
                         'The rule is to move w opposite to the sign of the slope. That one sentence is how a model with billions of numbers knows which way to go. Which way do we move at w equal to two?')))

    S.append(dict(kind='formula', title='The derivative of the squared-error loss, and its value at w = 1',
                  formulas=[('Derivative of the loss', r'$\frac{dL}{dw} = \frac{2}{n}\sum_{i=1}^{n} x_i\left(w\,x_i - y_i\right)$'), ('Our data at w = 1', r'$dL/dw = (2/4) \times (-37) = -18.5$')],
                  symbols=[['dL/dw', 'The slope of the loss curve: how fast the loss changes with w.', f'{D1:.1f} at w = 1; {D3:.1f} at w = 3'],
                           ['2 / n', 'The 2 and the factor x_i both come from the chain rule, taught in Session 9. n is the number of rows.', '2 / 4'],
                           ['x_i (w x_i - y_i)', 'Each error times its input x_i. Today we check the formula with numbers.', 'products add up to -37']],
                  size=22, note='In the lab you check this formula against a finite difference.',
                  notes=('The derivative of that loss has a two in front, and each error is multiplied by its input x i. Both the two and the x i come from the chain rule, which Session 9 teaches. '
                         'Today we take the formula as given and check it with numbers, which is a fair way to trust a rule before you can prove it. '
                         'The formula says the slope of the loss is two over n, times the sum of x i times the error. At w equal to one the sum is minus thirty-seven, so the slope is minus eighteen point five. '
                         'The table that follows shows the arithmetic row by row.')))

    S.append(dict(kind='table', title='Worked by hand at w = 1: the sum of x times error is -37, so the slope is -18.5',
                  headers=['Row i', 'Distance x', 'Fee y', 'Prediction w x', 'Error (prediction minus y)', 'x times error'],
                  rows=[[str(i + 1), f'{X[i]:g}', f'{Y[i]:g}', f'{yhat1[i]:g}', f'{err1[i]:g}', f'{X[i] * err1[i]:g}'] for i in range(4)] + [['Sum', '', '', '', '', f'{np.sum(X * err1):g}']],
                  widths=[1.3, 1.8, 1.4, 2.3, 3.2, 2.0], icons=False,
                  note=f'Slope = 2/4 times (-37) = -18.5. Check by finite difference: L(1.001) = {L1001:.4f}, so (L(1.001) minus L(1)) divided by 0.001 = {FD_L1:.2f}, close to -18.5.',
                  notes=(f'Row by row, with w equal to one, the prediction is the distance itself. The errors are minus two, minus three, minus three and minus five. Multiply each error by its distance and you get minus two, minus six, minus nine and minus twenty. '
                         f'Those add up to minus thirty-seven. Multiply by two over four and the slope is minus eighteen point five. As an independent check, nudge w to one point zero zero one. The loss becomes {L1001:.4f}, and the change divided by zero point zero zero one is {FD_L1:.2f}. '
                         'That is close to minus eighteen point five, so the formula passes the check.')))

    S.append(dict(kind='idea', title='At a minimum or a maximum the slope is zero',
                  visual=dict(kind='mc_curve', fn='cubic', xlim=(-2.2, 2.2), ylim=(-3.5, 3.5), xticks=[-2, -1, 0, 1, 2], yticks=[-2, 0, 2],
                              tangents=[dict(x=-1, label='slope 0', ldx=-0.3, ldy=0.45, ha='right'), dict(x=1, label='slope 0', ldx=0.3, ldy=0.45)],
                              points=[dict(x=-1, label='local maximum', ldx=0.3, ldy=0.5), dict(x=1, label='local minimum', ldx=-0.2, ldy=-0.5, ha='right')]),
                  lead='For f(x) = x cubed minus 3x the slope is 3 x squared minus 3. It is zero at x = -1 and at x = 1.',
                  points=['At x = -1 the curve tops out, a local maximum. The slope goes from positive to negative.', 'At x = 1 it bottoms out, a local minimum. The slope goes from negative to positive.'],
                  notes=('To find the bottom of a bowl we look for the place where the slope is zero. This different curve, x cubed minus three x, has slope three x squared minus three, which is zero at x equal to minus one and at x equal to one. '
                         'At minus one the curve tops out, a local maximum, and the slope changes from positive to negative. At one the curve bottoms out, a local minimum, and the slope changes from negative to positive. '
                         'So a zero slope marks a candidate, and the pattern of signs on each side tells you which kind it is. A loss function wants the minimum.')))

    S.append(dict(kind='formula', title='Setting the slope of the loss to zero gives the best w directly',
                  formulas=[('Slope equals zero', r'$\frac{2}{n}\left(w\sum x_i^{2} - \sum x_i\,y_i\right) = 0 \;\Rightarrow\; w\sum x_i^{2} = \sum x_i\,y_i$'),
                            ('Divide both sides', r'$w^{*} = \frac{\sum x_i\,y_i}{\sum x_i^{2}} = \frac{67}{30} = 2.233$')],
                  symbols=[['w*', 'The best w: the value where the loss is lowest. Read it as w-star.', f'{WSTAR:.3f}; loss there {LS:.3f}'],
                           ['sum of x_i y_i', 'Add the product of each distance and fee.', '3 + 10 + 18 + 36 = 67'],
                           ['sum of x_i squared', 'Add the square of each distance.', '1 + 4 + 9 + 16 = 30']],
                  size=22, note='This is the Session 4 normal equation (XᵀX) w = Xᵀy with X a single column of distances: XᵀX = 30 and Xᵀy = 67.',
                  notes=(f'Set the slope of the loss to zero and solve. Multiply out the bracket in the slope: two over n times the quantity w times the sum of x squared, minus the sum of x times y. Setting that to zero means w times the sum of x squared equals the sum of x y. '
                         f'Divide both sides and w star is sixty-seven over thirty, about {WSTAR:.3f}, with loss {LS:.3f}. This is the Session 4 normal equation with a single column of distances. '
                         'The catch is that a model with many parameters rarely has a tidy formula like this. So real training walks downhill using slopes, which is Session 10.')))

    S.append(dict(kind='compare', title='Read the sign the right way round, and do not assume every flat point is a minimum',
                  left=dict(head='Reading the sign backwards', icon='cross', points=['Negative slope: raise w.', 'Positive slope: lower w.', 'Move opposite to the slope.']),
                  right=dict(head='Assuming a minimum', icon='flag', points=['It can be a maximum or a flat spot.', 'Look at the loss on both sides.', 'Our bowl has one bottom.']),
                  verdict='Check the direction and the type of point.',
                  notes=('The first trap is reading the sign backwards. A negative slope means the loss falls as w grows, so you raise w. A positive slope means you lower w. Say it as: move opposite to the slope. '
                         'The second trap is calling every zero slope a minimum. A zero slope can be a maximum, or a flat spot. Look at the loss on both sides of the point. '
                         'The bowl in our example has one bottom, so it is safe. In bigger models the picture is more complicated, and Session 10 comes back to it.')))

    S.append(dict(kind='steps', title='Check a derivative with numbers: nudge the input and divide the change in output by the nudge',
                  steps=[dict(head='Pick a point', text='Choose x, for example x = 3', icon='pin'), dict(head='Nudge', text='Choose a tiny step, for example h = 0.001', icon='gear'),
                         dict(head='Compute', text='Work out (f(x + h) minus f(x)) divided by h', icon='calculator'), dict(head='Compare', text='It should match the formula to a few decimals', icon='check')], highlight=2,
                  caption='This is a finite difference: an estimate of a slope from two nearby points. Library developers routinely test derivatives this way (gradient checking).',
                  notes=('This habit will save you many hours. Whenever you work out a derivative by hand, check it with numbers. Pick a point. Choose a tiny step h, like zero point zero zero one. '
                         'Compute f of x plus h, subtract f of x, and divide by h. That estimate is called a finite difference. If it matches your formula to a few decimals, you are done. '
                         'If not, one of them is wrong, and it is usually the formula. Library developers routinely test their derivatives this way, and they call it gradient checking. Why does the check not need any calculus?')))

    S.append(dict(kind='formula', title='Forward and central differences, with numbers',
                  formulas=[('Forward difference', r"$f'(x) \approx \frac{f(x+h) - f(x)}{h}$"), ('Central difference', r"$f'(x) \approx \frac{f(x+h) - f(x-h)}{2h}$")],
                  symbols=[['h', 'The step. About 0.001 to 0.00001 (1e-3 to 1e-5) works well. Far smaller values give rounding noise.', 'h = 0.001'],
                           ['x squared at x = 3', 'Exact slope 6.', f'forward {fd(sq, 3, 1e-3):.3f}, central {cd(sq, 3, 1e-3):.3f}'],
                           ['e to the x at x = 1', 'Exact slope 2.71828.', f'forward {EX_F:.5f}, central {EX_C:.5f}']],
                  size=22, note=f'Use the central difference for checks. Too small an h fails: h = 1e-15 gives {H15:.2f} for x squared at 3, and 1e-16 gives 0.',
                  notes=(f'There are two ways to estimate a slope. The forward difference uses the point and one step ahead. The central difference uses one step on each side and divides by two h. '
                         f'With h equal to zero point zero zero one, x squared at three gives {fd(sq, 3, 1e-3):.3f} forward and {cd(sq, 3, 1e-3):.3f} central. For e to the x at one, the exact slope is two point seven one eight two eight; forward gives {EX_F:.5f} and central {EX_C:.5f}, much closer. '
                         'So use the central difference for checks. Do not make h extremely small. At ten to the minus fifteen the computer subtracts two nearly equal numbers and the slope comes out near five point three three, and at ten to the minus sixteen it is zero.')))

    S.append(dict(kind='code', title='Five lines of Python estimate the slope of any function',
                  code='def slope(f, x, h=1e-5):\n    return (f(x + h) - f(x - h)) / (2 * h)\n\nsquare = lambda x: x ** 2\nprint(round(slope(square, 3), 4))',
                  output=['6.0'],
                  reads=['Line 1: slope takes a function f, a point x and a small step h.', 'Line 2: the central difference formula from the last slide.', 'Line 4: lambda is a short way to write f(x) = x squared.',
                         'Line 5: slope at x = 3, rounded to 4 decimals. It prints 6.0.', 'The same function checks any derivative in this course.'],
                  notes=('Before we leave the concepts, this is the recipe you will use in Python. The function called slope takes another function f, a point x, and a small step h. '
                         'Line two is the central difference from the last slide, written in code. Line four creates the function x squared using lambda, which is a short way to write a small function. '
                         'Line five calls slope at x equal to three, rounds it to four decimals, and prints six point zero. In a spreadsheet you would do the same with a column of cells. You do not need to memorise any of this, because the notebook explains every line.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('The concepts are done. Everything you need is on the slides you have just seen, and each step of the lab explains itself. '
                         'Please open either the Python notebook or the spreadsheet workbook now. Both use the same numbers, so you can compare answers with someone who chose the other tool. '
                         'Run or fill every step in order from the top. Raise your hand if something gives an error. Remember the rhythm: predict first, then run, then change one thing.')))

    S.append(dict(kind='steps', title='Four stages take you from a shrinking step to the bottom of the bowl',
                  steps=[dict(head='1 Shrink h', text='Slopes of x squared at x = 3 for smaller and smaller h', icon='calculator'), dict(head='2 Rules', text='Compare each rule with a finite difference', icon='check'),
                         dict(head='3 The loss', text='Loss and its slope at w = 1, 2, 3 for the delivery data', icon='chart'), dict(head='4 The bottom', text='Find the w where the slope is zero', icon='flag')], highlight=2,
                  caption='Python: Steps 1 to 7 of the notebook. Spreadsheet: sheets Shrink, Rules and Loss. In every step predict first, then run, then change one thing.',
                  notes=('Stage one builds the table of slopes for shrinking h. Stage two checks each derivative rule against a finite difference. Stage three computes the loss for the delivery data and its slope at three values of w. '
                         'Stage four finds the w where the slope is zero. In Python you work through steps one to seven of the notebook. In the spreadsheet you use three sheets named Shrink, Rules and Loss. '
                         'Every step asks you to predict first. That habit is how you find out what you really understand.')))

    S.append(dict(kind='table', title='Your slopes should come out at 7, 6.01, 12, 3e and 0.75, and the loss slopes at -18.5 and +11.5',
                  headers=['What you compute', 'You should see'],
                  rows=[['Slope of x squared at 3, forward difference with h = 1', '7'], ['Same, with h = 0.01', '6.01'], ['Slope of x cubed at 2, central difference', '12'],
                        ['Slope of x squared times e to the x at 1', f'{P1:.3f}'], ['Slope of x squared / (x + 1) at 1', '0.75'], ['Loss L(1), L(2)', f'{L1:.2f}, {L2:.2f}'],
                        ['Slope of the loss at w = 1 and at w = 3', f'{D1:.1f} and {D3:.1f}'], ['Best w (slope zero)', f'{WSTAR:.3f}']],
                  widths=[7.4, 4.0], icons=['calculator', 'calculator', 'check', 'chart', 'chart', 'flag', 'chart', 'pin'],
                  note='If your number differs, stop and ask. Do not change a number to match. Find the step that went wrong.',
                  notes=('Use this table as your checkpoint. If your numbers match, carry on. If they do not, stop and call me, because later steps build on the earlier ones. '
                         'The most common cause in Python is a cell run out of order. In the spreadsheet it is a cell reference that moved when you copied a formula. '
                         'Do not edit a number to make it match. Finding why it differs is the skill that you will use in every project.')))

    S.append(dict(kind='table', title='A slope that is zero, noisy or the wrong sign usually has one of these causes',
                  headers=['What you see', 'What it means', 'What to do'],
                  rows=[['NameError in Python', 'A cell that defines a name was skipped', 'Run all cells from the top, in order'],
                        ['ZeroDivisionError or #DIV/0!', 'The step h is 0 or the h cell is empty', 'Set h to a small number such as 0.001'],
                        ['Slope far from 6, or exactly 0', 'h is far too small, for example 1e-15 or 1e-16', 'Use h of about 0.001 to 0.00001'],
                        ['Slope has the wrong sign', 'You subtracted in the wrong order', 'Use f(x + h) minus f(x), never the reverse']],
                  widths=[3.4, 4.4, 4.2], icons=['bell', 'cross', 'flag', 'key'],
                  notes=('A name error means a cell was skipped, so run all cells from the top. Zero division means the step h is zero or the h cell is empty. '
                         'A slope far from six, or exactly zero, means h is far too small, around ten to the minus fifteen, so the computer subtracts two nearly equal numbers and loses the digits that matter. And a wrong sign means you subtracted in the wrong order. '
                         'Always put f of x plus h first. Read the last line of any error message first, because it usually tells you the answer.')))

    S.append(dict(kind='steps', title='Where this appears in AI: the slope of the loss decides how each number changes',
                  steps=[dict(head='Show an example', text='A piece of text goes into the model', icon='doc'), dict(head='Measure the loss', text='One number: how wrong the model was', icon='calculator'),
                         dict(head='Take the slope', text='The slope of the loss for every adjustable number', icon='chart'), dict(head='Nudge', text='Change each number a little, opposite to its slope', icon='gear')], highlight=2,
                  caption='Published research describes language models of this kind as trained by this loop, repeated a very large number of times. The exact training details of ChatGPT, Gemini and Claude are not published.',
                  notes=('Published research describes this training loop for language models of this kind. Show the model some text. Measure the loss, one number for how wrong it was; for language models the loss is called cross-entropy, which Session 17 teaches. '
                         'Take the slope of that loss with respect to every adjustable number in the model. Then nudge each number a little, opposite to its slope, and repeat. '
                         'Today you did that for one number. The next three sessions extend it to many numbers. The exact training details of the commercial assistants are not published, but this loop is how open models are trained.')))

    S.append(dict(kind='practice', title='Test an AI assistant on the product rule with your own numbers', minutes=8, label='Hands-on, with any assistant',
                  task='Ask an assistant for the derivative of x squared times e to the x, and its value at x = 1.',
                  steps=['Write down its answer and its value at x = 1.', f'Compare with ours: 3e = {P1:.3f} at x = 1.', 'Run your lab slope function at x = 1.',
                         'If it differs, find the first line that differs.'],
                  output='One line: its value, your value, match or not. Never paste confidential data into an assistant.',
                  notes=('A short hands-on activity. Ask any AI assistant for the derivative of x squared times e to the x, and its value at x equal to one. Then check it with your own numbers. '
                         f'We worked out two x plus x squared, times e to the x, which is three e, about {P1:.3f}. Your slope function from the lab gives the same number. '
                         'Assistants are often right on rules like this, but they can slip, and you now have a tool to check them. If the assistant differs, ask it to show its steps and find the first line that differs. '
                         'Please never paste confidential data into an assistant.')))

    S.append(dict(kind='table', title='Exit check: the sign of a slope, the power rule and a finite difference',
                  headers=['Question', 'Short answer'],
                  rows=[['The slope of the loss at w is -4. Which way do you move w?', 'Up, so raise w. A negative slope means the loss falls as w grows.'],
                        ['What is the derivative of 5 x cubed at x = 2?', '15 x squared, which is 60 at x = 2.'],
                        ['For f(x) = x cubed, a finite difference gives 12.0003 at x = 2 and the rule gives 12. Pass or fail?', 'Pass. They agree to 3 decimals. A finite difference is only an estimate.']],
                  widths=[5.6, 6.4], icons=False, note='Write your own answer before you read ours. The automatic check in your notebook or workbook counts the lab numbers.',
                  notes=('Three questions to close. One: the slope of the loss at w is minus four. Which way do you move w? Up, because a negative slope means the loss falls as w grows. '
                         'Two: the derivative of five x cubed at x equal to two. The power rule gives fifteen x squared, which is sixty. '
                         'Three: for x cubed, a finite difference gives twelve point zero zero zero three at x equal to two, and the rule says twelve. That is a pass. They agree to three decimals, and a finite difference is only an estimate. '
                         'Write your own answers first, then compare. Then save your work.')))

    s['facilitator'] = dict(
        prep=['Open the deck in Slide Show mode, the notebook in Colab and the workbook in Excel or Google Sheets. Run the solution notebook once from the top and check it ends with All 16 checks pass; the workbook Check sheet has 18 checks.',
              'Put the notebook and workbook in the shared class folder and post the link. Learners choose one tool, and both use the same numbers.',
              'Write the check numbers (7, 6.01, 12, 3e, 0.75, -18.5, 11.5, 2.233) on the board before the lab.',
              'Have a ruler or a printed graph of x squared to hold up when you explain a tangent line.'],
        misconceptions=[('The slope of a curve is a single number', 'It changes from point to point. The derivative is a function that gives the slope at each x.'),
                        ('A smaller h is always better in a finite difference', 'Below about 1e-10 rounding error starts to grow, and by 1e-15 it swamps the answer (5.33 instead of 6; 0 at 1e-16). Use 1e-3 to 1e-5.'),
                        ('A zero slope means a minimum', 'It can be a maximum or a flat spot. Look at the sign of the slope on each side.'),
                        ('The derivative of a product is the product of the derivatives', 'Wrong: it is f-prime g plus f g-prime. The rectangle picture shows why there are two terms.'),
                        ('The 2 in the loss slope comes from the power rule alone', 'The 2 and the x_i both come from the chain rule (Session 9): the square is applied to (w x_i - y_i), which itself changes with w.')],
        probes=[('Why is the derivative a limit and not just a division?', 'The division gives the secant slope, which depends on h. The limit is the value those slopes settle on as h shrinks.'),
                ('The loss slope at w is +11.5. Which way do you move w?', 'Down. A positive slope means the loss grows as w grows.'),
                ('Why does the central difference beat the forward difference?', 'It looks on both sides of x, so the first error term cancels. Its error shrinks like h squared.'),
                ('What is the slope of e to the x at x = 0?', '1. The height is 1 and the slope equals the height.'),
                ('Where does the factor x_i in the loss derivative come from?', 'The chain rule: w sits inside the bracket multiplied by x_i. Session 9 treats it properly.'),
                ('Why does training not just solve the slope equal to zero?', 'Models with many parameters and nonlinear parts rarely have a closed form. Session 10 walks downhill with slopes.')],
        lab_steps=[('Python steps 1 and 2: forward slope and the table', 'Slope 7 for h = 1 and 6.01 for h = 0.01. The learner should see slope equals 6 plus h. Spreadsheet: sheet Shrink, the slope column and the central difference cell.'),
                   ('Python step 3: the rules against finite differences', 'Each analytic value matches within 0.0001. Spreadsheet: sheet Rules, the five gold cells. Watch for 3 x squared written without the multiplication sign.'),
                   ('Python steps 4 and 5: the loss and its derivative', 'L(1) = 11.75, L(2) = 0.75, slope -18.5 at w = 1. Spreadsheet: sheet Loss, the loss column and slope column. SUMPRODUCT must reference the same four rows.'),
                   ('Python step 6: which way to move', 'Slopes -18.5, -3.5, +11.5 at w = 1, 2, 3. Everyone should say raise, raise a little, lower.'),
                   ('Python step 7: the bottom', 'Best w is 2.233 and the loss there is 0.342. The CHANGE task (a new fee) moves the bottom: check that learners recompute rather than guess.')],
        rescue=['If the concepts run over, drop the quotient rule and keep the product rule picture. The lab needs only power, exponential and logarithm.',
                'If only half of the lab time remains, do stages one and three. Stage two (rules) becomes practice at home.',
                'If Colab is slow, use the spreadsheet track for everyone. The numbers are identical.',
                'If a learner is lost on the limit, go back to the table slide: slope equals 6 plus h, so it closes in on 6.'],
        after=['Share the notebook, the workbook and the slides as PDF.', 'Ask learners to write one sentence on why the sign of a slope matters for training.', 'Note any question you could not answer and start Session 8 with it.'],
        lab_answer_key=[['PREDICT: slope of x squared at 3 with h = 1?', '7, because (16 minus 9) divided by 1.'],
                        ['READ: what do the slopes approach as h shrinks?', '6, which is 2 times 3.'],
                        ['CHANGE: add h = 1e-15 and 1e-16 to the list (spreadsheet: A12 = 1E-15)', f'About {H15:.2f} and exactly 0.0: far from 6, because the computer subtracts two nearly equal numbers and loses the digits that matter. A spreadsheet may show 0 or a value far from 6.'],
                        ['PREDICT: sign of the loss slope at w = 1?', 'Negative, so the loss falls as w grows and we raise w.'],
                        ['READ: slopes of the loss at w = 1, 2, 3', f'{D1:.1f}, {D2:.1f}, {D3:.1f}.'],
                        ['CHANGE: the last fee 9 becomes 10', 'The best w rises to 71/30 = 2.367, because a bigger fee needs a bigger fee per km. The Python and spreadsheet answers must agree.']])
    return s
