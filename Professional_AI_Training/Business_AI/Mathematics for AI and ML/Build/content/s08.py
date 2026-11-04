"""Session 8: Partial derivatives and the gradient. Functions of two or more inputs, the gradient vector, contour plots, the gradient of the line-fit loss."""
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'kit'))

# ---- numbers used on the slides, computed once (the same delivery data as Session 7)
X = np.array([1.0, 2.0, 3.0, 4.0])
Y = np.array([3.0, 5.0, 6.0, 9.0])
N = len(X)


def loss(w, b):
    return float(np.mean((w * X + b - Y) ** 2))


def grad(w, b):
    e = w * X + b - Y
    return 2 / N * float(np.sum(X * e)), 2 / N * float(np.sum(e))


def numgrad(w, b, h=1e-4):
    return ((loss(w + h, b) - loss(w - h, b)) / (2 * h), (loss(w, b + h) - loss(w, b - h)) / (2 * h))


G0 = grad(1, 0)
GB = grad(1.9, 1.0)
L0, LB = loss(1, 0), loss(1.9, 1.0)
assert abs(L0 - 11.75) < 1e-9 and abs(G0[0] + 18.5) < 1e-9 and abs(G0[1] + 6.5) < 1e-9 and abs(LB - 0.175) < 1e-9 and abs(GB[0]) < 1e-9 and abs(GB[1]) < 1e-9
NG = numgrad(1, 0)
assert abs(NG[0] - G0[0]) < 1e-5 and abs(NG[1] - G0[1]) < 1e-5
E0 = 1 * X + 0 - Y                      # errors at the start
EB = 1.9 * X + 1.0 - Y                  # errors at the best fit
MAG = float(np.hypot(*G0))
ANG = float(np.degrees(np.arctan2(-G0[1], -G0[0])))
GRID_W = [1, 1.5, 2, 2.5]
GRID_B = [0, 0.5, 1, 1.5]
GRID = [[loss(w, b) for w in GRID_W] for b in GRID_B]
f2 = lambda x, y: x ** 2 + 3 * y ** 2
FG = (4.0, 6.0)
FMAG = float(np.hypot(*FG))


def build():
    s = dict(
        num=8, block='Calculus and optimisation', short_title='Partial derivatives and the gradient',
        title='Partial derivatives and the gradient: which way is uphill when a model has many numbers to tune',
        question='Many models have billions of adjustable numbers. How does one step change all of them at once?',
        outcome_head='By the end of today you can',
        outcomes=['Compute a partial derivative of a function of two inputs by changing one input and holding the other fixed',
                  'Collect the partial derivatives into the gradient vector and say which way is steepest uphill on a contour plot',
                  'Compute the gradient of the loss of a line fit (slope and intercept) by hand and check it with numbers'],
        outcome_icons=['calculator', 'flag', 'chart'],
        outcome_note=('By the end of today you can do three things. First, take a partial derivative of a function with two inputs, by changing one input and holding the other still. '
                      'Second, collect those partial derivatives into one vector called the gradient, and read on a contour plot which way is steepest uphill. '
                      'Third, work out the gradient of the loss for a line fit, with a slope and an intercept, using real numbers, and check it by nudging each parameter. '
                      'Everything builds on the single slope you met last session.'),
        clock=[(10, 'Recall, and a real question from AI that today answers'), (35, 'Concept: a picture, then a hand example'), (10, 'Break'),
               (45, 'Lab in Python or a spreadsheet: predict, run, change one thing'), (15, 'Where it appears in ChatGPT, Gemini, Claude; exit check'), (5, 'Save the work')],
        plan_title='Your two hours: many inputs, the gradient, then the lab',
        plan_caption='Pictures and hand examples first, then the lab on the same numbers in Python or a spreadsheet.',
        plan_note=('Here is how the two hours run. We start with a short recall of Session 7 and the question for today. Then thirty-five minutes of concepts, with a picture first and then a calculation by hand. '
                   'After the break you spend forty-five minutes in the lab, in Python or in a spreadsheet, on the same delivery data as last time. '
                   'The last twenty minutes show where this appears in AI and give you an exit check.'),
        recall_from='Session 7',
        recall=[('What does the derivative of a function tell you at one point?',
                 'The slope of the tangent line there: how fast the output changes for a small change in the input.'),
                ('The slope of the loss at w = 1 is -18.5. Which way do you move w, and why?',
                 'Up. A negative slope means the loss falls as w grows, so you raise w.'),
                ('How do you check a derivative worked out by hand?',
                 'Nudge the input by a tiny h and compute (f(x + h) minus f(x - h)) divided by 2h. It should match the formula to a few decimals.')],
        words=[('Parameter', 'A number inside a model that training can change. Our line y-hat = w x + b has two: the slope w and the intercept b.'),
               ('Partial derivative', 'The slope of a function when you change one input and hold the others fixed. Written ∂L/∂w and read "partial L, partial w".'),
               ('Gradient', 'The vector of all the partial derivatives. It points in the direction in which the function increases fastest. Written with the symbol nabla.'),
               ('Contour plot', 'A map of a function of two inputs. Each curve joins the points where the function has the same value.'),
               ('Steepest increase', 'The direction in which a function rises fastest. Its opposite, minus the gradient, is the direction of steepest decrease.')],
        word_icons=['gear', 'magnifier', 'flag', 'pin', 'chart'],
        words_note=('Five words for today. A parameter is a number inside a model that training can change. A partial derivative is the slope of a function when you change one input and hold the others fixed. '
                    'The gradient is the vector that collects all the partial derivatives, and it points where the function rises fastest. A contour plot is a map of a function of two inputs, with a curve for each value. '
                    'Steepest increase is the direction in which the function rises fastest. These are the real industry terms, and you will meet them in every machine learning paper.'),
        keep='Keep your saved lab. Write down the gradient of the loss at the start, (-18.5, -6.5), and the best line, w = 1.9 and b = 1, where the gradient is (0, 0).',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Saved lab', value='Notebook or workbook'), dict(label='Gradient at start', value='(-18.5, -6.5)'),
                                                              dict(label='Best line', value='w = 1.9, b = 1'), dict(label='Next session', value='The chain rule')]),
        keep_title='Save the lab and keep the gradient at the start and at the best fit',
        next='Session 9: the chain rule and the Jacobian.', next_label='Next session',
        keep_note=('Before you go, save your notebook or workbook. Keep two things. The gradient of the loss at the start, w equal to one and b equal to zero, which is minus eighteen point five and minus six point five. '
                   'And the best line, w equal to one point nine and b equal to one, where the gradient is zero. '
                   'Next session we ask how the slope travels backwards through a model made of many steps, which is the chain rule. If anything was unclear, write the question down and bring it.'),
        cover_note=('Welcome to Session 8. Last session your loss had one adjustable number and one slope. Real models have many numbers, so today the single slope becomes a collection of slopes, one for each number, called the gradient. '
                    'We stay with the same four deliveries and give the line a second parameter, an intercept. Then we draw the loss as a map, and read the gradient on that map.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 7',
                  headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.2, 6.8], icons=False,
                  note='If one answer surprised you, look back at Session 7 before the lab.',
                  notes=('Here are the short answers. The derivative tells you the slope of the tangent line at one point, so how fast the output changes for a small change in the input. '
                         'A slope of minus eighteen point five means the loss falls as w grows, so you move w up. '
                         'And you check a derivative by nudging the input a tiny amount and computing the central difference, f of x plus h minus f of x minus h, over two h. It should match your formula to a few decimals. '
                         'Everything today is built from these three ideas.')))

    S.append(dict(kind='idea', title='A line fit has two parameters, so its loss depends on two numbers',
                  visual=dict(kind='scatter', points=[(float(a), float(b)) for a, b in zip(X, Y)], xlabel='distance x (km)', ylabel='fee y (thousand UGX)', line=(0.0, 1.0), residuals=True, xlim=(0, 5), ylim=(0, 10)),
                  lead='Last session the model was y-hat = w x. Now the line can also shift up or down: y-hat = w x + b.',
                  points=['Two parameters: the slope w and the intercept b. The red segments are the errors at w = 1 and b = 0.', 'The loss L(w, b) depends on both. L(1, 0) = 11.75. For w = 1.9 and b = 1 it is 0.175.'],
                  notes=('Last session the model had one parameter, w, and the line had to pass through the origin. Now we let the line move up and down as well. The model is y hat equals w x plus b. '
                         'That gives two parameters, a slope w and an intercept b. The red segments show the errors for the starting line, with w equal to one and b equal to zero. '
                         'The loss now depends on two numbers, so we write L of w and b. At the start it is eleven point seven five. For w equal to one point nine and b equal to one it is only point one seven five. What would a one-parameter picture miss?')))

    S.append(dict(kind='formula', title='The loss of a line fit is a function of two inputs, w and b',
                  formulas=[('Loss (mean squared error)', r'$L(w, b) = \frac{1}{n}\sum_{i=1}^{n}\left(w\,x_i + b - y_i\right)^{2}$'), ('Our data at (1, 0)', r'$L(1, 0) = (4 + 9 + 9 + 25)/4 = 11.75$')],
                  symbols=[['L(w, b)', 'The loss: the mean of the squared errors for one pair (w, b).', f'L(1, 0) = {L0:.2f}; L(1.9, 1) = {LB:.3f}'],
                           ['w, b', 'The two parameters: slope (fee per km) and intercept (fee at 0 km).', 'start: w = 1, b = 0'],
                           ['x_i, y_i, n', 'Distance and fee of delivery i, and the number of rows.', 'x = 1, 2, 3, 4; y = 3, 5, 6, 9; n = 4']],
                  size=22, note='The error of row i is e_i = w x_i + b - y_i. At (1, 0) the four errors are -2, -3, -3 and -5.',
                  notes=('Here is the loss with two parameters. For each row i the prediction is w times x i plus b. The error is the prediction minus the fee y i. Square the errors, add them, and divide by n. '
                         'It is the same mean squared error as last time, but it now takes a pair of numbers. At w equal to one and b equal to zero, the errors are minus two, minus three, minus three and minus five. '
                         'Their squares add to forty-seven, and forty-seven over four is eleven point seven five. Which numbers in the formula are the data, and which are the parameters?')))

    S.append(dict(kind='idea', title='A contour plot is a map of the loss: each curve joins the pairs (w, b) with the same loss',
                  visual=dict(kind='mc_contour', fn='loss_wb', xlim=(0, 3.5), ylim=(-0.5, 2.5), xlabel='slope w', ylabel='intercept b', xticks=[0, 1, 2, 3], yticks=[0, 1, 2], levels=[1, 3, 10, 20],
                              level_ray=[1.9, 1, 19], equal=True, points=[dict(x=1, y=0, label='start: L = 11.75', ldx=0.2, ldy=-0.3), dict(x=1.9, y=1, label='best: L = 0.175', ldx=-0.25, ldy=0.3, ha='right')]),
                  lead='Each grey curve is a contour line, like a height line on a hiking map. The small numbers give the loss on that curve.',
                  points=['The start (1, 0) lies between the curves 10 and 20.', 'The best line, (1.9, 1), sits at the centre where the loss is smallest.'],
                  notes=('How do you draw a function of two inputs on flat paper? Like a hiking map. Each grey curve joins all the pairs of w and b that give the same loss, and the small numbers tell you which loss. '
                         'Close curves mean the loss changes quickly. The start, w equal to one and b equal to zero, sits between the curves ten and twenty, so its loss is eleven point seven five. '
                         'The best line sits at the centre, where the loss is smallest, point one seven five. Training is a walk from the start to that centre. In which direction do you think we should walk?')))

    S.append(dict(kind='idea', title='A partial derivative is the slope of one slice: change one input and hold the other fixed',
                  visual=dict(kind='mc_slice', fn='loss_wb', fixed='b', value=0.0, point=1.0, slope_label='slope'),
                  lead='Hold b at 0 and change only w. The loss along the red horizontal line (left) is last session\'s curve (right).',
                  points=['Its slope at w = 1 is -18.5. That is the partial derivative of L with respect to w.', 'Hold w fixed and change only b to get the other partial derivative.'],
                  notes=('Here is the idea of a partial derivative in one picture. On the left is the contour map. Draw the red line b equal to zero, so we hold b fixed and let only w change. '
                         'The loss along that line is the curve on the right, and it is exactly the curve from last session. Its slope at w equal to one is minus eighteen point five. '
                         'That slope is called the partial derivative of L with respect to w. To get the partial derivative with respect to b, hold w fixed and slice the other way. '
                         'Why is it called partial?')))

    S.append(dict(kind='formula', title='Partial derivatives: differentiate with respect to one input and treat the others as constants',
                  formulas=[('Function', r'$f(x, y) = x^{2} + 3y^{2}$'), ('Partial derivatives', r'$\frac{\partial f}{\partial x} = 2x \qquad \frac{\partial f}{\partial y} = 6y$')],
                  symbols=[['∂ (partial)', 'The partial derivative symbol, read "partial" (also "del"). All other inputs are held fixed.', '∂f/∂x with y held fixed'],
                           ['∂f/∂x = 2x', 'Treat 3 y squared as a constant. Its slope in x is 0. The power rule on x squared gives 2x.', 'at (2, 1): 4'],
                           ['∂f/∂y = 6y', 'Treat x squared as a constant. The power rule on 3 y squared gives 6y.', 'at (2, 1): 6']],
                  size=24, note='Check at (2, 1): f(2.001, 1) minus f(1.999, 1), divided by 0.002, is 4.000. And in y it is 6.000.',
                  notes=('A tiny function first, f of x and y equals x squared plus three y squared. To get the partial derivative with respect to x, treat y as a fixed number. Then three y squared is a constant, its slope is zero, and the power rule on x squared gives two x. '
                         'With respect to y, treat x as fixed, and the power rule on three y squared gives six y. The curly symbol, ∂, is read partial. At the point two, one, the two partial derivatives are four and six. '
                         'The same central difference check works one input at a time. What are the partial derivatives at the origin?')))

    S.append(dict(kind='idea', title='The gradient points in the direction of steepest increase, at right angles to the contour lines',
                  visual=dict(kind='mc_contour', fn='bowl', xlim=(-3, 3), ylim=(-2, 2), xlabel='x', ylabel='y', xticks=[-2, 0, 2], yticks=[-1, 0, 1], levels=[1, 4, 9, 16], level_ray=[0, 0, -35],
                              field=dict(step=(1, 0.8), scale=0.06), equal=True),
                  lead='The function is f(x, y) = x squared + 3 y squared. Each black arrow is the gradient at its point.',
                  points=['Every arrow points uphill and crosses the contour lines at a right angle.', 'Long arrows mean a steep slope. The arrows shrink towards the centre, where the bowl is flat.'],
                  notes=('Now the picture of the gradient. This is the contour map of f of x and y equals x squared plus three y squared, a bowl that is steeper in y than in x. '
                         'At each grid point I drew the gradient, the arrow made from the two partial derivatives. Every arrow points uphill, and every arrow crosses the contour line at a right angle. '
                         'The arrows are long where the bowl is steep and shrink towards the centre where it is flat. So the gradient carries two facts: which way is uphill, and how steep it is. '
                         'Which way would you walk to go downhill?')))

    S.append(dict(kind='formula', title='The gradient is the vector of all the partial derivatives',
                  formulas=[('Gradient', r'$\nabla f = \left(\frac{\partial f}{\partial x},\ \frac{\partial f}{\partial y}\right)$'), ('At (2, 1)', r'$\nabla f(2, 1) = (4,\ 6)$')],
                  symbols=[['nabla f', 'Read it as grad f or del f. One entry for each input.', f'({FG[0]:.0f}, {FG[1]:.0f}) at (2, 1)'],
                           ['length of nabla f', 'The steepness: the slope of the steepest direction. Square root of 4 squared + 6 squared.', f'{FMAG:.2f}'],
                           ['minus nabla f', 'The direction of steepest decrease. Machine learning walks this way.', '(-4, -6)']],
                  size=24, note='Uphill direction as a unit vector: (4, 6) divided by 7.21 is (0.55, 0.83). Slope in that direction: 7.21.',
                  notes=(f'The gradient is the vector of all the partial derivatives. Written with the symbol nabla, it has one entry for each input. For our function at the point two, one, it is the vector four, six. '
                         f'Its length, the square root of sixteen plus thirty-six, is {FMAG:.2f}, and that is the steepness, the slope in the steepest direction. '
                         'Minus the gradient points the opposite way, to steepest decrease. That is the direction machine learning walks. The next two slides compute the gradient of a real loss.')))

    S.append(dict(kind='formula', title='The gradient of the line-fit loss: one partial derivative for w and one for b',
                  formulas=[('Slope of the loss in w', r'$\frac{\partial L}{\partial w} = \frac{2}{n}\sum_{i=1}^{n} x_i\,e_i$'), ('Slope of the loss in b', r'$\frac{\partial L}{\partial b} = \frac{2}{n}\sum_{i=1}^{n} e_i$')],
                  symbols=[['e_i', 'The error of row i: prediction minus actual, w x_i + b - y_i.', 'at (1, 0): -2, -3, -3, -5'],
                           ['x_i e_i', 'Each error times its input. It enters the w slope because w multiplies x_i.', '-2, -6, -9, -20'],
                           ['sum e_i', 'In the b slope each error counts once, because b is simply added.', '-13']],
                  size=22, note='2/n comes from the power rule. Session 9 explains x_i and 1 (chain rule).',
                  notes=('Here are the two partial derivatives of the line-fit loss. For w, we take each error, multiply it by its input x i, add them up, and multiply by two over n. '
                         'For b, we simply add up the errors, multiply by two over n, because b is just added to the prediction, so it has an input of one. '
                         'The factor two over n comes from the power rule on the square. The extra factors, x i and one, appear because w multiplies x i and b is only added. Next session explains this with the chain rule. '
                         'Together the two numbers form the gradient. At the start, the errors are minus two, minus three, minus three, and minus five.')))

    S.append(dict(kind='table', title='Worked by hand: at w = 1 and b = 0 the gradient is (-18.5, -6.5)',
                  headers=['Row i', 'Distance x', 'Fee y', 'Prediction w x + b', 'Error e', 'x times e'],
                  rows=[[str(i + 1), f'{X[i]:g}', f'{Y[i]:g}', f'{(1 * X[i]):g}', f'{E0[i]:g}', f'{X[i] * E0[i]:g}'] for i in range(4)] + [['Sum', '', '', '', f'{E0.sum():g}', f'{(X * E0).sum():g}']],
                  widths=[1.3, 1.9, 1.4, 2.8, 1.8, 2.2], icons=False,
                  note=f'dL/dw = 2/4 times ({(X * E0).sum():g}) = {G0[0]:g}. dL/db = 2/4 times ({E0.sum():g}) = {G0[1]:g}. Check: nudging w and b by 0.0001 each way gives {NG[0]:.3f} and {NG[1]:.3f}.',
                  notes=(f'Here is the arithmetic. With w equal to one and b equal to zero, the prediction is just the distance. The errors are minus two, minus three, minus three and minus five, and they sum to minus thirteen. '
                         f'Multiply each by its distance and you get minus two, minus six, minus nine and minus twenty, which sum to minus thirty-seven. '
                         f'So the partial derivative with respect to w is two over four times minus thirty-seven, minus eighteen point five. With respect to b it is two over four times minus thirteen, minus six point five. '
                         f'The gradient is the pair, minus eighteen point five and minus six point five. Nudging each parameter by point zero zero zero one gives {NG[0]:.3f} and {NG[1]:.3f}, which agrees.')))

    S.append(dict(kind='idea', title='Downhill is minus the gradient: at (1, 0) the loss falls fastest towards a larger w and a larger b',
                  visual=dict(kind='mc_contour', fn='loss_wb', xlim=(0, 3.5), ylim=(-0.5, 2.5), xlabel='slope w', ylabel='intercept b', xticks=[0, 1, 2, 3], yticks=[0, 1, 2], levels=[1, 3, 10, 20],
                              level_ray=[1.9, 1, 19], equal=True,
                              points=[dict(x=1, y=0, label='start', ldx=-0.25, ldy=-0.3, ha='right'), dict(x=1.9, y=1, label='')],
                              arrows=[dict(x=1, y=0, dx=-G0[0] / MAG * 0.8, dy=-G0[1] / MAG * 0.8, label='downhill', ldx=0.5, ldy=-0.3, ha='left')]),
                  lead=f'At the start the gradient is ({G0[0]:g}, {G0[1]:g}). The red arrow is minus the gradient, shortened to fit.',
                  points=['Both entries are negative, so both w and b should go up.', f'The steepest slope there is the length of the gradient: {MAG:.1f} loss units per unit of step.'],
                  notes=(f'Now read the gradient on the map. At the start, the gradient is minus eighteen point five and minus six point five. Minus the gradient is the direction of steepest decrease, and the red arrow shows it, shortened so it fits. '
                         'Both entries are negative, so to go downhill both w and b should go up, and w should go up much more than b. '
                         f'The length of the gradient, {MAG:.1f}, is how steep the hill is in that direction. Notice that the arrow crosses the contour lines at a right angle. It does not point straight at the centre, but it is the steepest way down from where you stand.')))

    S.append(dict(kind='idea', title='At the best fit the gradient is zero: the loss is flat in every direction',
                  visual=dict(kind='mc_contour', fn='loss_wb', xlim=(0, 3.5), ylim=(-0.5, 2.5), xlabel='slope w', ylabel='intercept b', xticks=[0, 1, 2, 3], yticks=[0, 1, 2], levels=[0.25, 0.5, 1, 3, 10],
                              equal=True, points=[dict(x=1.9, y=1, label='gradient (0, 0)', ldx=0.3, ldy=0.35)]),
                  lead='At w = 1.9 and b = 1 the four errors are -0.1, -0.2, 0.7 and -0.4.',
                  points=['The errors sum to 0, so dL/db = 0.', 'The sum of x times error is -0.1 - 0.4 + 2.1 - 1.6 = 0, so dL/dw = 0. This is the least-squares line from Session 4.'],
                  notes=('At the centre of the map the loss is flat in every direction. At w equal to one point nine and b equal to one, the four errors are minus point one, minus point two, point seven and minus point four. '
                         'Add them and you get zero, so the partial derivative with respect to b is zero. Multiply each by its distance and add: minus point one, minus point four, plus two point one, minus one point six, which is also zero. '
                         'So the partial derivative with respect to w is zero too. The gradient is zero, and that is the least-squares line you found in Session 4. A zero gradient marks a flat spot, and here it is the bottom.')))

    S.append(dict(kind='idea', title='The spreadsheet lab computes the loss for a grid of (w, b) pairs',
                  visual=dict(kind='sheet', headers=['b \\ w'] + [f'w = {w:g}' for w in GRID_W], rows=[[f'b = {b:g}'] + [f'{v:.3f}'.rstrip('0').rstrip('.') for v in row] for b, row in zip(GRID_B, GRID)], hl=[2, 3]),
                  lead='Each cell holds the loss L(w, b) for the w at the top of its column and the b at the left of its row.',
                  points=['In this part of the grid the smallest value is 0.25. It appears twice, at (w = 2, b = 0.5) and at (w = 2, b = 1, the gold cell). The true minimum, 0.175, lies between grid points.', 'A grid like this is the contour map in table form.'],
                  notes=('Here is the same loss as a table, which is how you will build it in the spreadsheet. The columns are values of w and the rows are values of b. Each cell is the loss for that pair, computed by a single formula copied across the grid. '
                         'Look for the smallest value in this part of the grid. It is point two five, and it appears twice, at w equal to two with b equal to point five, and at w equal to two with b equal to one. The true minimum, point one seven five, lies between grid points, at one point nine and one. '
                         'A table like this is the contour map written as numbers. Which neighbouring cells tell you the direction of downhill from the start?')))

    S.append(dict(kind='steps', title='Check a gradient with numbers: nudge one parameter at a time',
                  steps=[dict(head='Nudge w', text='Compute L(w + h, b) and L(w - h, b)', icon='gear'), dict(head='Divide', text='(L(w + h, b) minus L(w - h, b)) divided by 2h', icon='calculator'),
                         dict(head='Nudge b', text='Do the same for b with w held fixed', icon='gear'), dict(head='Compare', text='Both numbers should match the formulas', icon='check')], highlight=1,
                  caption=f'With h = 0.0001 at (1, 0): {NG[0]:.3f} for w and {NG[1]:.3f} for b. The formulas gave -18.5 and -6.5.',
                  notes=('The numerical check from last session works one parameter at a time. Nudge w up and down by a tiny h, with b held fixed, and compute the central difference of the loss. That is your estimate of the partial derivative with respect to w. '
                         'Then do the same for b with w held fixed. At the start, with h equal to point zero zero zero one, you get minus eighteen point five and minus six point five, which match the formulas. '
                         'Every library that computes gradients automatically is tested in exactly this way. What would you conclude if one of the two numbers did not match?')))

    S.append(dict(kind='idea', title='A gradient has one entry for each parameter, whatever the size of the model',
                  visual=dict(kind='mc_entries', count_label='Our line fit: N = 2 (w and b)'),
                  lead='A model with N parameters has a gradient with N entries: one partial derivative of the loss for each parameter.',
                  points=['For our line fit, N = 2: the gradient is (dL/dw, dL/db).', 'Nothing else changes when N grows. Only the length of the list does.'],
                  notes=('Here is the general picture. A model with N parameters has a loss that depends on N numbers, so its gradient has N entries, one partial derivative for each parameter. '
                         'For our line fit, N is two, and the gradient has two entries, one for w and one for b. Nothing else changes when N grows. You still hold all the other parameters fixed, and nudge one. '
                         'Only the length of the list grows. In a moment we look at how long that list is for the large open models. Before that, how many entries would a plane fit with two slopes and an intercept have?')))

    S.append(dict(kind='compare', title='Two mistakes to avoid with the gradient',
                  left=dict(head='Walking with the gradient', icon='cross', points=['The gradient points uphill.', 'To reduce the loss, go the other way.', 'Use minus the gradient.']),
                  right=dict(head='Changing both at once', icon='flag', points=['A partial derivative changes one input.', 'All the others stay fixed.', 'Nudge w alone, then b alone.']),
                  verdict='The gradient says where the loss rises. Step the opposite way.',
                  notes=('Two mistakes catch many people. First, walking in the direction of the gradient. The gradient points uphill, so to reduce the loss we step the other way, along minus the gradient. '
                         'Second, changing both inputs at once when you check a partial derivative. A partial derivative changes one input and holds every other input fixed, so nudge w on its own, then b on its own. '
                         'If you nudge both together you measure a different quantity, a slope along a diagonal. Which of these two mistakes would lead to a model getting worse in training?')))

    S.append(dict(kind='code', title='Read the recipe before you write it: the gradient of the line-fit loss',
                  code='import numpy as np\nx = np.array([1, 2, 3, 4])\ny = np.array([3, 5, 6, 9])\nw, b, n = 1, 0, 4\ne = w * x + b - y\ngrad_w = 2 / n * np.sum(x * e)\ngrad_b = 2 / n * np.sum(e)\nprint(grad_w, grad_b)',
                  output=['-18.5 -6.5'],
                  reads=['Lines 1 to 4: the data, and the starting values w = 1, b = 0, n = 4.', 'Line 5: e holds the four errors, prediction minus actual.', 'Line 6: multiply each error by its x, add them, and multiply by 2 / n. This is dL/dw.', 'Line 7: add the errors and multiply by 2 / n. This is dL/db.',
                         'With w = 1 and b = 0 it prints -18.5 and -6.5.'],
                  notes=('Before the lab, here is the recipe. The first four lines set up the data and the starting values, w equal to one, b equal to zero, n equal to four. Line five makes the errors, prediction minus actual, for all four rows at once. '
                         'Line six multiplies each error by its x, adds them, and multiplies by two over n. That is the partial derivative with respect to w. '
                         'Line seven adds the errors and multiplies by two over n, the partial derivative with respect to b. It prints minus eighteen point five and minus six point five. '
                         'The notebook walks you through each line. In the spreadsheet you build the same thing with SUMPRODUCT.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the concepts. Everything you need is on the slides, and each step of the lab explains itself. '
                         'Please open the Python notebook or the spreadsheet workbook now. Both use the same four deliveries, so you can compare numbers with someone who chose the other tool. '
                         'Work through the steps in order. Raise your hand if a cell gives an error. Remember the rhythm: predict first, then run, then change one thing.')))

    S.append(dict(kind='steps', title='The lab has four stages, in Python and in the spreadsheet',
                  steps=[dict(head='1 The loss', text='L(w, b) at the start and at the best line', icon='calculator'), dict(head='2 The gradient', text='By formula, then check with nudges', icon='check'),
                         dict(head='3 The map', text='A grid of losses and a contour plot', icon='chart'), dict(head='4 Steepest way', text='Find the downhill direction and test it', icon='flag')], highlight=1,
                  caption='Python: Steps 1 to 6 of the notebook. Spreadsheet: sheets Gradient and Grid. In every step predict first, then run, then change one thing.',
                  notes=('Here is the lab map. Stage one computes the loss at the start and at the best line. Stage two computes the gradient by formula and checks it with nudges. '
                         'Stage three builds the grid of losses and draws a contour plot. Stage four finds the steepest downhill direction by trying many directions, and tests that it is minus the gradient. '
                         'In Python you work through steps one to six. In the spreadsheet you use two sheets named Gradient and Grid. Predict first in each step.')))

    S.append(dict(kind='table', title='Check your numbers against these before you move on',
                  headers=['What you compute', 'You should see'],
                  rows=[['Loss L(1, 0) and L(1.9, 1)', f'{L0:.2f} and {LB:.3f}'], ['Gradient at (1, 0): dL/dw and dL/db', f'{G0[0]:g} and {G0[1]:g}'],
                        ['Nudged estimates at (1, 0), h = 0.0001', f'{NG[0]:.3f} and {NG[1]:.3f}'], ['Gradient at (1.9, 1)', '0 and 0 (to 3 decimals)'],
                        ['Smallest loss on the grid, w = 0 to 3.5, b = -1 to 3, step 0.5', '0.25 (two grid points tie)'], ['Length of the gradient at (1, 0)', f'{MAG:.2f}'],
                        ['Steepest downhill direction at (1, 0), in degrees', f'{ANG:.1f}']],
                  widths=[7.4, 4.0], icons=['calculator', 'chart', 'check', 'flag', 'pin', 'gear', 'flag'],
                  note='If your number differs, stop and ask. Do not change a number to match. Find the step that went wrong.',
                  notes=('Use this table as your checkpoint. If your numbers match, carry on. If they do not, stop and call me. '
                         'The loss at the start is eleven point seven five and at the best line it is point one seven five. The gradient at the start is minus eighteen point five and minus six point five, and the nudged estimates agree. '
                         'The steepest downhill direction is about nineteen degrees above the w axis. Do not edit a number to make it match. Finding why it differs is the skill you will use on every project.')))

    S.append(dict(kind='table', title='Errors you will meet, what they mean and what to do',
                  headers=['What you see', 'What it means', 'What to do'],
                  rows=[['NameError in Python', 'A cell that defines a name was skipped', 'Run all cells from the top, in order'],
                        ['Gradient has the wrong sign', 'Errors computed as actual minus prediction', 'Use prediction minus actual: w x + b - y'],
                        ['Both entries equal', 'The x multiplier was left out of the w entry', 'dL/dw needs x times e; dL/db needs e only'],
                        ['Grid cells all show the same number', 'A cell reference moved when copied', 'Write w as B$3 and b as $A4 so the right reference stays fixed when you copy']],
                  widths=[3.4, 4.4, 4.2], icons=['bell', 'cross', 'flag', 'key'],
                  notes=('Errors are normal, and reading them is a skill. A name error means a cell was skipped, so run all cells from the top. '
                         'A gradient with the wrong sign usually means the error was computed as actual minus prediction. Use prediction minus actual, the same as on the slides. '
                         'If both entries are equal, the multiplier x was left out of the w entry. And in the spreadsheet, if all the grid cells show the same number, a cell reference moved when you copied the formula. Use the dollar sign to lock the row of w, written B dollar 3, and the column of b, written dollar A 4.')))

    S.append(dict(kind='idea', title='Where this appears in AI: a gradient with billions of entries',
                  visual=dict(kind='mc_scale', items=[dict(label='Our line fit', value=2, text='2 parameters'), dict(label='Open model, 8 billion class', value=8e9, text='8,000,000,000 parameters'),
                                                      dict(label='Open model, 70 billion class', value=7e10, text='70,000,000,000 parameters')]),
                  lead='Open models such as Llama 3 list 8 billion and 70 billion parameters. The gradient has one entry for each.',
                  points=['If each entry is stored in 16 bits (2 bytes), 8 billion entries take 16 gigabytes. Many training setups keep more bits than that.', 'The sizes of ChatGPT, Gemini and Claude are not published, so we do not quote them.'],
                  notes=('Here is the scale of what you computed today. Published open models, such as the Llama 3 family, list sizes of eight billion and seventy billion parameters. '
                         'The gradient of the loss has one entry for each parameter, so a training step produces billions of partial derivatives. '
                         'If each entry is stored in sixteen bits, or two bytes, eight billion entries alone take sixteen gigabytes. Many training setups keep more bits than that, which is one reason training needs specialised hardware. '
                         'The sizes of ChatGPT, Gemini and Claude are not published, so we do not guess them. The mathematics is the same one you did by hand with two parameters. How many entries did your gradient have?')))

    S.append(dict(kind='practice', title='Check an AI assistant\'s answer with your own numbers', minutes=8, label='Hands-on, with any assistant',
                  task='Ask an assistant for the partial derivatives of the mean squared error of y-hat = w x + b at w = 1, b = 0.',
                  steps=['Give it x = 1, 2, 3, 4 and y = 3, 5, 6, 9.', f'Compare with ours: ({G0[0]:g}, {G0[1]:g}).', 'Run your lab gradient code.',
                         'If it differs, find the first line that differs.'],
                  output='One line: its gradient, yours, match or not. Never paste confidential data into an assistant.',
                  notes=('A short hands-on activity. Ask any AI assistant for the partial derivatives of the mean squared error for our model at w equal to one and b equal to zero, and give it the four data points. '
                         f'Our answer is minus eighteen point five and minus six point five. Check the assistant\'s numbers against that and against your own lab code. '
                         'Assistants are often right on this kind of calculation, but they can slip on a sign or a factor of two. If the assistant differs, ask for the steps and find the first line that differs. '
                         'Please never paste confidential data into an assistant.')))

    S.append(dict(kind='table', title='Exit check: three questions with short answers',
                  headers=['Question', 'Short answer'],
                  rows=[['For f(x, y) = x squared times y, what is the partial derivative with respect to y at (3, 2)?', '9. Treat x squared as a constant: the slope in y is x squared, which is 9.'],
                        ['The gradient of a loss at some point is (4, -2). In which direction do you step to reduce the loss?', 'Along minus the gradient: (-4, 2). Decrease the first parameter, increase the second.'],
                        ['How many entries does the gradient of a model with 20 parameters have?', '20, one partial derivative for each parameter.']],
                  widths=[5.8, 6.2], icons=False, note='Write your own answer before you read ours. The automatic check counts the lab numbers.',
                  notes=('Three questions to close. One: f of x and y equals x squared times y. The partial derivative with respect to y treats x squared as a constant, so it equals x squared, which is nine at x equal to three. '
                         'Two: the gradient is four and minus two. We step along minus the gradient, minus four and plus two, so the first parameter goes down and the second goes up. '
                         'Three: a model with twenty parameters has a gradient with twenty entries. Write your own answers first, then compare. Then save your work.')))

    s['facilitator'] = dict(
        prep=['Open the deck in Slide Show mode, the notebook in Colab and the workbook in Excel or Google Sheets. Run the notebook once from the top and check it ends with All checks pass.',
              'Put the notebook and workbook in the shared class folder and post the link. Both use the same four deliveries as Session 7.',
              'Write the check numbers on the board: L(1,0) = 11.75, gradient (-18.5, -6.5), best (1.9, 1), steepest direction 19.4 degrees.',
              'Bring a printed contour map (a hiking map or a weather pressure map) to show that contour lines are everyday objects.'],
        misconceptions=[('The gradient points downhill', 'It points uphill, in the direction of steepest increase. Training steps along minus the gradient.'),
                        ('A partial derivative changes all inputs a little', 'It changes one input and holds the others fixed. Nudging two together measures a diagonal slope.'),
                        ('The gradient points straight at the minimum', 'It points in the steepest direction at the current point, which crosses the contour lines at a right angle. On a long narrow bowl that is far from the centre direction.'),
                        ('A zero gradient always means a minimum', 'It can be a maximum or a saddle point. In our bowl it is the minimum.')],
        probes=[('Why does dL/db have no x in it?', 'Because b is added to the prediction, so a change in b shifts every prediction by the same amount. Its multiplier is 1.'),
                ('What are the partial derivatives of x squared plus y squared at (3, 4)?', '6 and 8. The gradient is (6, 8) with length 10.'),
                ('Which way is the loss falling fastest at the start?', 'Along minus the gradient (18.5, 6.5), about 19 degrees above the w axis.'),
                ('What does a long, thin contour ellipse tell you?', 'The loss changes quickly in one direction and slowly in the other. This slows down simple training (Session 10).'),
                ('Why does the gradient have the same length as the parameter list?', 'There is one partial derivative for each parameter.'),
                ('Is the gradient of the loss at the best fit exactly zero in the spreadsheet?', 'Up to rounding, yes. Excel shows a tiny number such as 1E-15.')],
        lab_steps=[('Python step 1: the loss', 'L(1, 0) = 11.75 and L(1.9, 1) = 0.175. Spreadsheet: sheet Gradient, the loss cells.'),
                   ('Python step 2: the gradient by formula', '(-18.5, -6.5) at the start. Learners who get (18.5, 6.5) subtracted in the wrong order. Spreadsheet: SUMPRODUCT with the same four rows.'),
                   ('Python step 3: nudges', 'Both estimates agree with the formulas to 3 decimals. If one is far off, h is too large or the nudge changed both parameters.'),
                   ('Python step 4: the grid', 'Smallest loss 0.25 on the 0.5 grid, a tie between (w = 2, b = 0.5) and (w = 2, b = 1). A 0.1 grid finds 0.175 at (1.9, 1). Spreadsheet: sheet Grid, colour scale to read the bowl.'),
                   ('Python steps 5 and 6: contour plot and steepest direction', 'Best direction 19.4 degrees (to within 1 degree), the direction of minus the gradient. The CHANGE task moves the start and shows a different direction.')],
        rescue=['If the concepts run over, skip the grid slide and the numeric check slide. Say them in the lab.', 'If only half of the lab time remains, do stages one and two. Stages three and four become practice at home.',
                'If Colab is slow, use the spreadsheet track for everyone. The numbers are identical.', 'If a learner is lost on partial derivatives, return to f(x, y) = x squared + 3 y squared: treat the other input as a number.'],
        after=['Share the notebook, the workbook and the slides as PDF.', 'Ask learners to write one sentence on why the gradient has one entry for each parameter.', 'Note any question you could not answer and start Session 9 with it.'],
        lab_answer_key=[['PREDICT: sign of dL/dw at the start?', 'Negative, because the line is too flat and the errors are mostly negative.'],
                        ['READ: gradient at (1, 0)', '(-18.5, -6.5).'],
                        ['READ: gradient at (1.9, 1)', 'About (0, 0). The loss is flat there.'],
                        ['PREDICT: direction of steepest decrease at the start', 'About 19 degrees above the w axis: more w than b.'],
                        ['CHANGE: start at (3, 0)', 'The gradient changes sign for w and the downhill direction turns to point left and down.']])
    return s
