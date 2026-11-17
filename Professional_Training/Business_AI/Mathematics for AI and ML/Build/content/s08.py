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


UNIT = (-G0[0] / MAG, -G0[1] / MAG)        # steepest downhill direction at the start, as a unit vector (length 1)
assert abs(UNIT[0] - 0.943) < 1e-3 and abs(UNIT[1] - 0.331) < 1e-3
G3 = grad(3, 0)                          # the CHANGE task: start at (3, 0)
assert G3 == (11.5, 3.5)
# the workbook sheet Grid with its real addresses: header row 3, b in column A from row 4, w = 0 ... in columns B ...
SHEET_W = [0, 0.5, 1, 1.5, 2]
SHEET_B = [-1, -0.5, 0, 0.5, 1, 1.5]
SHEET = [['b \\ w'] + [f'{w:g}' for w in SHEET_W]] + [[f'{b:g}'] + [f'{loss(w, b):g}' for w in SHEET_W] for b in SHEET_B]
# normal equation for these four deliveries (Session 4): columns of ones and distances
XM = np.column_stack([np.ones(4), X])
XTX, XTY = XM.T @ XM, XM.T @ Y
assert XTX.tolist() == [[4, 10], [10, 30]] and XTY.tolist() == [23, 67] and np.allclose(np.linalg.solve(XTX, XTY), [1, 1.9])
CONT = dict(kind='mc_contour', fn='loss_wb', xlim=(0, 3.5), ylim=(-0.5, 2.5), xlabel='slope w', ylabel='intercept b', xticks=[0, 1, 2, 3], yticks=[0, 1, 2], levels=[0.5, 3, 10, 20],
            level_ray=[[1.6, 1.8, 0], [2.3, -0.3, 180]], equal=True)


def build():
    s = dict(
        num=8, block='Calculus and optimisation', short_title='Partial derivatives and the gradient',
        title='Partial derivatives and the gradient: which way is uphill when a model has many numbers to tune',
        question='Many models have billions of adjustable numbers. Which way should each one move to lower the loss?',
        outcome_head='By the end of today you can',
        outcomes=['Compute a partial derivative of a function of two inputs by changing one input and holding the other fixed',
                  'Collect the partial derivatives into the gradient vector and say which way is steepest uphill on a contour plot',
                  'Compute the gradient of the loss of a line fit (intercept and slope) by hand and check it with numbers'],
        outcome_icons=['calculator', 'flag', 'chart'],
        outcome_note=('By the end of today you can do three things. First, take a partial derivative of a function with two inputs, by changing one input and holding the other still. '
                      'Second, collect those partial derivatives into one vector called the gradient, and read on a contour plot which way is steepest uphill. '
                      'Third, work out the gradient of the loss for a line fit, with an intercept and a slope, using real numbers, and check it by nudging each parameter. '
                      'Everything builds on the single slope you met last session.'),
        clock=[(10, 'Recall, and a real question from AI that today answers'), (35, 'Concept: a picture, then a hand example'), (10, 'Break'),
               (45, 'Lab in Python or a spreadsheet: predict, run, change one thing'), (15, 'Where it appears in ChatGPT, Gemini, Claude; exit check'), (5, 'Save the work')],
        plan_title='Your two hours: many inputs, the gradient, then the lab',
        plan_caption='Pictures and hand examples first, then the lab on the same numbers in Python or a spreadsheet.',
        plan_note=('We open with a short recall of Session 7 and the question for today. Then come thirty-five minutes of concepts, with a picture first and then a calculation by hand. '
                   'After the break you spend forty-five minutes in the lab, in Python or in a spreadsheet, on the same delivery data as last time. '
                   'The last twenty minutes show where this appears in AI and give you an exit check.'),
        recall_from='Session 7',
        recall=[('What does the derivative of a function tell you at one point?',
                 'The slope of the tangent line there: how fast the output changes for a small change in the input.'),
                ('The slope of the loss at w = 1 is -18.5. Which way do you move w, and why?',
                 'Up. A negative slope means the loss falls as w grows, so you raise w.'),
                ('How do you check a derivative worked out by hand?',
                 'Nudge the input by a tiny h and compute (f(x + h) minus f(x - h)) divided by 2h. It should match the formula to a few decimals.')],
        words=[('Parameter', 'A number inside a model that training can change. Our line y-hat = b + w x has two: the intercept b and the slope w.'),
               ('Partial derivative', 'The slope of a function when you change one input and hold the others fixed. Written ∂L/∂w and read "partial L, partial w".'),
               ('Gradient', 'The vector of all the partial derivatives, written as a column. It points where the function increases fastest. Symbol: nabla.'),
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
                   'Next session asks how the slope travels backwards through a model made of many steps, which is the chain rule. If anything was unclear, write the question down and bring it.'),
        cover_note=('Welcome to Session 8. Last session your loss had one adjustable number and one slope. Real models have many numbers, so today the single slope becomes a collection of slopes, one for each number, called the gradient. '
                    'We stay with the same four deliveries and give the line a second parameter, an intercept. Then we draw the loss as a map, and read the gradient on that map. The step itself, how far to move, is Session 10.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 7',
                  headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.2, 6.8], icons=False,
                  note='If one answer surprised you, look back at Session 7 before the lab.',
                  notes=('The derivative tells you the slope of the tangent line at one point, so how fast the output changes for a small change in the input. '
                         'A slope of minus eighteen point five means the loss falls as w grows, so you move w up. '
                         'And you check a derivative by nudging the input a tiny amount and computing the central difference, f of x plus h minus f of x minus h, over two h. It should match your formula to a few decimals. '
                         'Everything today is built from these three ideas.')))

    S.append(dict(kind='idea', title='A line fit has two parameters, so its loss depends on two numbers',
                  visual=dict(kind='scatter', points=[(float(a), float(b)) for a, b in zip(X, Y)], xlabel='distance x (km)', ylabel='fee y (thousand UGX)', line=(0.0, 1.0), residuals=True, xlim=(0, 5), ylim=(0, 10)),
                  lead='Last session the model was y-hat = w x. Now the line can also shift up or down: y-hat = b + w x.',
                  points=['Two parameters: the intercept b and the slope w. The red segments are the errors at w = 1 and b = 0.', 'The loss L(w, b) depends on both. L(1, 0) = 11.75. For w = 1.9 and b = 1 it is 0.175.'],
                  notes=('Last session the model had one parameter, w, and the line had to pass through the origin. Today the line may move up and down as well. The model is y hat equals b plus w x, as in Session 4. '
                         'That gives two parameters, an intercept b and a slope w. The red segments show the errors for the starting line, with w equal to one and b equal to zero. '
                         'The loss now depends on two numbers, so we write L of w and b. At the start it is eleven point seven five. For w equal to one point nine and b equal to one it is only point one seven five.')))

    S.append(dict(kind='formula', title='The loss of a line fit is a function of two inputs, w and b',
                  formulas=[('Loss (mean squared error)', r'$L(w, b) = \frac{1}{n}\sum_{i=1}^{n}\left(b + w\,x_i - y_i\right)^{2}$'), ('Our data at (1, 0)', r'$L(1, 0) = (4 + 9 + 9 + 25)/4 = 11.75$')],
                  symbols=[['L(w, b)', 'The loss: the mean of the squared errors for one pair (w, b).', f'L(1, 0) = {L0:.2f}; L(1.9, 1) = {LB:.3f}'],
                           ['w, b', 'The two parameters: slope (fee per km) and intercept (fee at 0 km).', 'start: w = 1, b = 0'],
                           ['x_i, y_i, n', 'Distance and fee of delivery i, and the number of rows.', 'x = 1, 2, 3, 4; y = 3, 5, 6, 9; n = 4']],
                  size=22, note='The error of row i is e_i = b + w x_i - y_i. At (1, 0) the four errors are -2, -3, -3 and -5.',
                  notes=('With two parameters, the prediction for row i is b plus w times x i. The error is the prediction minus the fee y i. Square the errors, add them, and divide by n. '
                         'It is the same mean squared error as last time, but it now takes a pair of numbers. At w equal to one and b equal to zero, the errors are minus two, minus three, minus three and minus five. '
                         'Their squares add to forty-seven, and forty-seven over four is eleven point seven five. Which numbers in the formula are the data, and which are the parameters?')))

    S.append(dict(kind='idea', title='A contour plot is a map of the loss: each curve joins the pairs (w, b) with the same loss',
                  visual=dict(CONT, points=[dict(x=1, y=0, label='start: L = 11.75', ldx=-0.2, ldy=0.35, ha='right'), dict(x=1.9, y=1, label='best: L = 0.175', ldx=0.25, ldy=0.0, ha='left')]),
                  lead='Each grey curve is a contour line, like a height line on a hiking map. The small numbers give the loss on that curve.',
                  points=['The start (1, 0) lies between the curves 20 and 10.', 'The best line, (1.9, 1), sits inside the small closed curve 0.5, where the loss is smallest.'],
                  notes=('How do you draw a function of two inputs on flat paper? Like a hiking map. Each grey curve joins all the pairs of w and b that give the same loss, and the small numbers tell you which loss. '
                         'Close curves mean the loss changes quickly. The start, w equal to one and b equal to zero, sits between the curves twenty and ten, so its loss is eleven point seven five. '
                         'The best line sits inside the small closed curve marked point five, where the loss is smallest, point one seven five. Training is a walk from the start to that centre. In which direction do you think we should walk?')))

    S.append(dict(kind='idea', title='A partial derivative is the slope of one slice: change one input and hold the other fixed',
                  visual=dict(kind='mc_slice', fn='loss_wb', fixed='b', value=0.0, point=1.0, slope_label='slope', levels=(1, 3, 10, 20, 30), level_ray=[[1.4, 2.6, 180]]),
                  lead='Hold b at 0 and change only w. The loss along the red horizontal line (left) is last session\'s curve (right).',
                  points=['Its slope at w = 1 is -18.5. That is the partial derivative of L with respect to w, written ∂L/∂w.', 'Hold w fixed and change only b to get the other partial derivative, ∂L/∂b.'],
                  notes=('On the left is the contour map again. Draw the red line b equal to zero, so we hold b fixed and let only w change. '
                         'The loss along that line is the curve on the right, and it is exactly the curve from last session. Its slope at w equal to one is minus eighteen point five. '
                         'That slope is called the partial derivative of L with respect to w. It is partial because it looks along one input only. To get the partial derivative with respect to b, hold w fixed and slice the other way.')))

    S.append(dict(kind='formula', title='Partial derivatives: differentiate with respect to one input and treat the others as constants',
                  formulas=[('Function', r'$f(x, y) = x^{2} + 3y^{2}$'), ('Partial derivatives', r'$\frac{\partial f}{\partial x} = 2x \qquad \frac{\partial f}{\partial y} = 6y$')],
                  symbols=[['∂ (partial)', 'The partial derivative symbol, read "partial". All other inputs are held fixed.', '∂f/∂x with y held fixed'],
                           ['∂f/∂x = 2x', 'Treat 3 y squared as a constant. Its slope in x is 0. The power rule on x squared gives 2x.', 'at (2, 1): 4'],
                           ['∂f/∂y = 6y', 'Treat x squared as a constant. The power rule on 3 y squared gives 6y.', 'at (2, 1): 6']],
                  size=24, note='Check at (2, 1): f(2.001, 1) minus f(1.999, 1), divided by 0.002, is 4.000. And in y it is 6.000.',
                  notes=('A tiny function first, f of x and y equals x squared plus three y squared. To get the partial derivative with respect to x, treat y as a fixed number. Then three y squared is a constant, its slope is zero, and the power rule on x squared gives two x. '
                         'With respect to y, treat x as fixed, and the power rule on three y squared gives six y. The curly symbol is read partial. At the point two, one, the two partial derivatives are four and six. '
                         'The same central difference check works one input at a time. What are the partial derivatives at the origin?')))

    S.append(dict(kind='idea', title='The gradient points in the direction of steepest increase, at right angles to the contour lines',
                  visual=dict(kind='mc_contour', fn='bowl', xlim=(-3, 3), ylim=(-2, 2), xlabel='x', ylabel='y', xticks=[-2, 0, 2], yticks=[-1, 0, 1], levels=[1, 4, 9, 16], level_ray=[0, 0, -35],
                              field=dict(step=(1, 0.8), scale=0.06), equal=True),
                  lead='The function is f(x, y) = x squared + 3 y squared. Each black arrow is the gradient at its point.',
                  points=['Every arrow points uphill and crosses the contour lines at a right angle.', 'Long arrows mean a steep slope. The arrows shrink towards the centre, where the bowl is flat.'],
                  notes=('This contour map belongs to f of x and y equals x squared plus three y squared, a bowl that is steeper in y than in x. '
                         'At each grid point I drew the gradient, the arrow made from the two partial derivatives. Every arrow points uphill, and every arrow crosses the contour line at a right angle. '
                         'The arrows are long where the bowl is steep and shrink towards the centre where it is flat. So the gradient carries two facts: which way is uphill, and how steep it is. '
                         'To go downhill you walk against the arrows.')))

    S.append(dict(kind='formula', title='The gradient is the column of all the partial derivatives',
                  formulas=[('Gradient (a column vector)', r'$\nabla f = \left(\genfrac{}{}{0}{}{\partial f/\partial x}{\partial f/\partial y}\right)$'), ('At (2, 1)', r'$\nabla f(2, 1) = \left(\genfrac{}{}{0}{}{4}{6}\right)$')],
                  symbols=[['nabla f', 'Read "nabla f" or "grad f". One entry for each input, stood up as a column (Session 3). In text we write (4, 6).', f'({FG[0]:.0f}, {FG[1]:.0f}) at (2, 1)'],
                           ['length of nabla f', 'The steepness: the slope in the steepest direction. It is the L2 norm from Session 2.', f'square root of 16 + 36 = {FMAG:.2f}'],
                           ['minus nabla f', 'The direction of steepest decrease. Machine learning walks this way.', '(-4, -6)']],
                  size=24, note='Uphill direction as a unit vector (length 1): (4, 6) divided by 7.21 is (0.55, 0.83). The slope in that direction is 7.21.',
                  notes=(f'The gradient is the vector of all the partial derivatives. Written with the symbol nabla, it has one entry for each input, and like every vector since Session 3 it stands as a column. In running text we write its entries across, four, six, to save space. '
                         f'Its length, the L2 norm from Session 2, is the square root of sixteen plus thirty-six, {FMAG:.2f}, and that is the steepness, the slope in the steepest direction. '
                         'Minus the gradient points the opposite way, to steepest decrease. That is the direction machine learning walks.')))

    S.append(dict(kind='formula', title='The gradient of the line-fit loss: one partial derivative for w and one for b',
                  formulas=[('Slope of the loss in w', r'$\frac{\partial L}{\partial w} = \frac{2}{n}\sum_{i=1}^{n} x_i\,e_i$'), ('Slope of the loss in b', r'$\frac{\partial L}{\partial b} = \frac{2}{n}\sum_{i=1}^{n} e_i$')],
                  symbols=[['e_i', 'The error of row i: prediction minus actual, b + w x_i - y_i.', 'at (1, 0): -2, -3, -3, -5'],
                           ['x_i e_i', 'Each error times its input. It enters the w slope because w multiplies x_i.', '-2, -6, -9, -20'],
                           ['sum e_i', 'In the b slope each error counts once, because b is added on its own.', '-13']],
                  size=22, note='The 2 / n, the x_i and the 1 in front of e_i all come from the chain rule (Session 9).',
                  notes=('These are the two partial derivatives of the line-fit loss. For w, take each error, multiply it by its input x i, add them up, and multiply by two over n. '
                         'For b, add up the errors and multiply by two over n, because b is added to the prediction on its own, so its multiplier is one. '
                         'Where do the two, the x i and the one come from? All three come from the chain rule, which is next session. Today we check the formulas with numbers. '
                         'Together the two numbers form the gradient. At the start, the errors are minus two, minus three, minus three, and minus five.')))

    S.append(dict(kind='table', title='Worked by hand: at w = 1 and b = 0 the gradient is (-18.5, -6.5)',
                  headers=['Row i', 'Distance x', 'Fee y', 'Prediction b + w x', 'Error e', 'x times e'],
                  rows=[[str(i + 1), f'{X[i]:g}', f'{Y[i]:g}', f'{(1 * X[i]):g}', f'{E0[i]:g}', f'{X[i] * E0[i]:g}'] for i in range(4)] + [['Sum', '', '', '', f'{E0.sum():g}', f'{(X * E0).sum():g}']],
                  widths=[1.3, 1.9, 1.4, 2.8, 1.8, 2.2], icons=False,
                  note=f'∂L/∂w = 2/4 times ({(X * E0).sum():g}) = {G0[0]:g}. ∂L/∂b = 2/4 times ({E0.sum():g}) = {G0[1]:g}. Check: nudging w and b by 0.0001 each way gives {NG[0]:.3f} and {NG[1]:.3f}.',
                  notes=(f'With w equal to one and b equal to zero, the prediction is the distance itself. The errors are minus two, minus three, minus three and minus five, and they sum to minus thirteen. '
                         f'Multiply each by its distance and you get minus two, minus six, minus nine and minus twenty, which sum to minus thirty-seven. '
                         f'So the partial derivative with respect to w is two over four times minus thirty-seven, minus eighteen point five. With respect to b it is two over four times minus thirteen, minus six point five. '
                         f'The gradient is the pair, minus eighteen point five and minus six point five. Nudging each parameter by point zero zero zero one gives {NG[0]:.3f} and {NG[1]:.3f}, which agrees.')))

    S.append(dict(kind='idea', title='Downhill is minus the gradient: at (1, 0) the loss falls fastest towards a larger w and a larger b',
                  visual=dict(CONT, points=[dict(x=1, y=0, label='start', ldx=-0.25, ldy=0.3, ha='right'), dict(x=1.9, y=1, label='')],
                              arrows=[dict(x=1, y=0, dx=UNIT[0] * 0.8, dy=UNIT[1] * 0.8, label='downhill', ldx=0.5, ldy=-0.3, ha='left')]),
                  lead=f'At the start the gradient is ({G0[0]:g}, {G0[1]:g}). The red arrow is minus the gradient, shortened to length 0.8.',
                  points=[f'Both entries are negative, so both w and b should go up. As a unit vector the direction is ({UNIT[0]:.3f}, {UNIT[1]:.3f}).', f'The steepest slope there is the length of the gradient: {MAG:.1f} loss units per unit of step.'],
                  notes=(f'Read the gradient on the map. At the start, the gradient is minus eighteen point five and minus six point five. Minus the gradient is the direction of steepest decrease, and the red arrow shows it, shortened so it fits. '
                         f'Both entries are negative, so to go downhill both w and b should go up, and w should go up much more than b. Divided by its length, the direction is {UNIT[0]:.3f} and {UNIT[1]:.3f}. '
                         f'The length of the gradient, {MAG:.1f}, is how steep the hill is in that direction. The arrow crosses the contour lines at a right angle. It does not point straight at the centre, but it is the steepest way down from where you stand.')))

    S.append(dict(kind='idea', title='At the best fit the gradient is zero: the loss is flat in every direction',
                  visual=dict(CONT, levels=[0.25, 3, 10, 20], points=[dict(x=1.9, y=1, label='gradient (0, 0)', ldx=0.3, ldy=0.35)]),
                  lead='At w = 1.9 and b = 1 the four errors are -0.1, -0.2, 0.7 and -0.4.',
                  points=['Errors sum to 0, so ∂L/∂b = 0. x times error sums to -0.1 - 0.4 + 2.1 - 1.6 = 0, so ∂L/∂w = 0.', 'The Session 4 normal equation agrees: XᵀX rows (4, 10), (10, 30), Xᵀy = (23, 67), so b = 1, w = 1.9.'],
                  notes=('At the centre of the map the loss is flat in every direction. At w equal to one point nine and b equal to one, the four errors are minus point one, minus point two, point seven and minus point four. '
                         'Add them and you get zero, so the partial derivative with respect to b is zero. Multiply each by its distance and add: minus point one, minus point four, plus two point one, minus one point six, which is also zero. '
                         'So the gradient is zero. Solve the Session 4 normal equation for these four deliveries and you get the same line, b equal to one and w equal to one point nine. A zero gradient marks a flat spot, and here it is the bottom.')))

    S.append(dict(kind='idea', title='The spreadsheet lab computes the loss for a grid of (w, b) pairs',
                  visual=dict(kind='mc_sheet', cols=['A', 'B', 'C', 'D', 'E', 'F'], rows=[3, 4, 5, 6, 7, 8, 9], cells=SHEET, hl=[(4, 5), (5, 5)]),
                  lead='This is the top left of sheet Grid. Each cell holds L(w, b) for the w in row 3 above it and the b in column A beside it.',
                  points=['Start D6 = 11.75 (w = 1, b = 0). The smallest values, 0.25, tie in F7 and F8 (gold).', 'One formula in B4, with B$3 for w and $A4 for b, copies to every cell.'],
                  notes=('The same loss as a table is how you will build it in the spreadsheet, and this picture uses the real cell addresses of sheet Grid. The values of w run along row three and the values of b down column A. '
                         'Each cell is the loss for that pair, from a single formula written in B4 and copied across. The dollar signs keep row three and column A fixed while you copy. '
                         'The start is in D6, eleven point seven five. The smallest values in this corner are point two five, a tie in F7 and F8. The true minimum, point one seven five, lies between grid points.')))

    S.append(dict(kind='steps', title='Check a gradient with numbers: nudge one parameter at a time',
                  steps=[dict(head='Nudge w', text='Compute L(w + h, b) and L(w - h, b)', icon='gear'), dict(head='Divide', text='(L(w + h, b) minus L(w - h, b)) divided by 2h', icon='calculator'),
                         dict(head='Nudge b', text='Do the same for b with w held fixed', icon='gear'), dict(head='Compare', text='Both numbers should match the formulas', icon='check')], highlight=1,
                  caption=f'With h = 0.0001 at (1, 0): {NG[0]:.3f} for w and {NG[1]:.3f} for b. The formulas gave -18.5 and -6.5.',
                  notes=('The numerical check from last session works one parameter at a time. Nudge w up and down by a tiny h, with b held fixed, and compute the central difference of the loss. That is your estimate of the partial derivative with respect to w. '
                         'Then do the same for b with w held fixed. At the start, with h equal to point zero zero zero one, you get minus eighteen point five and minus six point five, which match the formulas. '
                         'Libraries that compute gradients automatically are routinely tested in this way. What would you conclude if one of the two numbers did not match?')))

    S.append(dict(kind='idea', title='A gradient has one entry for each parameter, whatever the size of the model',
                  visual=dict(kind='mc_entries', count_label='Our line fit: N = 2 (w and b)', sub=r'$\theta_1 \ldots \theta_N$: the N parameters'),
                  lead='Papers write all of a model\'s numbers together as θ (theta). With N parameters θ₁, θ₂ and so on, the gradient has N entries.',
                  points=['For our line fit, N = 2: θ is (w, b) and the gradient is (∂L/∂w, ∂L/∂b).', 'Nothing else changes when N grows. Only the length of the list does.'],
                  notes=('Machine learning papers use one symbol, theta, for all of a model\'s numbers together, and write the single numbers as theta one up to theta N. That is the only meaning of theta in this course from now on. '
                         'A model with N parameters has a loss that depends on N numbers, so its gradient has N entries, one partial derivative for each parameter. '
                         'For our line fit, N is two, theta is the pair w and b, and the gradient has two entries. Nothing else changes when N grows. You still hold all the other parameters fixed and nudge one. Only the length of the list grows.')))

    S.append(dict(kind='compare', title='The gradient points uphill, and a partial derivative moves one input only',
                  left=dict(head='Walking with the gradient', icon='cross', points=['The gradient points uphill.', 'To reduce the loss, go the other way.', 'Use minus the gradient.']),
                  right=dict(head='Changing both at once', icon='flag', points=['A partial derivative changes one input.', 'All the others stay fixed.', 'Nudge w alone, then b alone.']),
                  verdict='The gradient says where the loss rises. Step the opposite way.',
                  notes=('The first trap is walking in the direction of the gradient. The gradient points uphill, so to reduce the loss we step the other way, along minus the gradient. A model that steps with the gradient gets worse every step. '
                         'The second trap is changing both inputs at once when you check a partial derivative. A partial derivative changes one input and holds every other input fixed, so nudge w on its own, then b on its own. '
                         'If you nudge both together you measure a different quantity, a slope along a diagonal.')))

    S.append(dict(kind='code', title='Seven lines of numpy compute both partial derivatives at once',
                  code='import numpy as np\nx = np.array([1, 2, 3, 4])\ny = np.array([3, 5, 6, 9])\nw, b, n = 1, 0, 4\ne = b + w * x - y\ngrad_w = 2 / n * np.sum(x * e)\ngrad_b = 2 / n * np.sum(e)\nprint(grad_w, grad_b)',
                  output=['-18.5 -6.5'],
                  reads=['Lines 1 to 4: the data, and the starting values w = 1, b = 0, n = 4.', 'Line 5: e holds the four errors, prediction minus actual.', 'Line 6: multiply each error by its x, add them, and multiply by 2 / n. This is ∂L/∂w.', 'Line 7: add the errors and multiply by 2 / n. This is ∂L/∂b.',
                         'With w = 1 and b = 0 it prints -18.5 and -6.5.'],
                  notes=('Before the lab, this is the recipe. The first four lines set up the data and the starting values, w equal to one, b equal to zero, n equal to four. Line five makes the errors, prediction minus actual, for all four rows at once. '
                         'Line six multiplies each error by its x, adds them, and multiplies by two over n. That is the partial derivative with respect to w. '
                         'Line seven adds the errors and multiplies by two over n, the partial derivative with respect to b. It prints minus eighteen point five and minus six point five. '
                         'The notebook walks you through each line. In the spreadsheet you build the same thing with SUMPRODUCT.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('Time to build it yourself. Everything you need is on the slides, and each step of the lab explains itself. '
                         'Please open the Python notebook or the spreadsheet workbook now. Both use the same four deliveries, so you can compare numbers with someone who chose the other tool. '
                         'Work through the steps in order. Raise your hand if a cell gives an error. Remember the rhythm: predict first, then run, then change one thing.')))

    S.append(dict(kind='steps', title='The lab goes from the loss, to its gradient, to a map, to the steepest way down',
                  steps=[dict(head='1 The loss', text='L(w, b) at the start and at the best line', icon='calculator'), dict(head='2 The gradient', text='By formula, then check with nudges', icon='check'),
                         dict(head='3 The map', text='A grid of losses and a contour plot', icon='chart'), dict(head='4 Steepest way', text='Find the downhill direction and test it', icon='flag')], highlight=1,
                  caption='Python: Steps 1 to 6 of the notebook. Spreadsheet: sheets Gradient and Grid. In every step predict first, then run, then change one thing.',
                  notes=('Stage one computes the loss at the start and at the best line. Stage two computes the gradient by formula and checks it with nudges. '
                         'Stage three builds the grid of losses and draws a contour plot. Stage four finds the steepest downhill direction as a unit vector, and tests it against small steps in many directions. '
                         'In Python you work through steps one to six. In the spreadsheet you use two sheets named Gradient and Grid. Predict first in each step.')))

    S.append(dict(kind='table', title='Your gradient at the start should read (-18.5, -6.5); check the rest here',
                  headers=['What you compute', 'You should see'],
                  rows=[['Loss L(1, 0) and L(1.9, 1)', f'{L0:.2f} and {LB:.3f}'], ['Gradient at (1, 0): ∂L/∂w and ∂L/∂b', f'{G0[0]:g} and {G0[1]:g}'],
                        ['Nudged estimates at (1, 0), h = 0.0001', f'{NG[0]:.3f} and {NG[1]:.3f}'], ['Gradient at (1.9, 1)', '0 and 0 (to 3 decimals)'],
                        ['Smallest loss on the grid, w = 0 to 3.5, b = -1 to 3, step 0.5', '0.25 (two grid points tie)'], ['Length of the gradient at (1, 0)', f'{MAG:.2f}'],
                        ['Steepest downhill direction at (1, 0), as a unit vector', f'({UNIT[0]:.3f}, {UNIT[1]:.3f})']],
                  widths=[7.4, 4.0], icons=['calculator', 'chart', 'check', 'flag', 'pin', 'gear', 'flag'],
                  note='If your number differs, stop and ask. Do not change a number to match. Find the step that went wrong.',
                  notes=('Use this table as your checkpoint, and stop and call me if a number differs. '
                         'The loss at the start is eleven point seven five and at the best line it is point one seven five. The gradient at the start is minus eighteen point five and minus six point five, and the nudged estimates agree. '
                         f'The steepest downhill direction, minus the gradient divided by its length, is {UNIT[0]:.3f} and {UNIT[1]:.3f}: mostly more w, a little more b. Do not edit a number to make it match. Finding why it differs is the skill you will use on every project.')))

    S.append(dict(kind='table', title='Four errors that spoil a gradient, and how to fix each one',
                  headers=['What you see', 'What it means', 'What to do'],
                  rows=[['NameError in Python', 'A cell that defines a name was skipped', 'Run all cells from the top, in order'],
                        ['Gradient has the wrong sign', 'Errors computed as actual minus prediction', 'Use prediction minus actual: b + w x - y'],
                        ['Both entries equal', 'The x multiplier was left out of the w entry', '∂L/∂w needs x times e; ∂L/∂b needs e only'],
                        ['Grid cells all show the same number', 'A cell reference moved when copied', 'In B4 write w as B$3 and b as $A4, then copy']],
                  widths=[3.4, 4.4, 4.2], icons=['bell', 'cross', 'flag', 'key'],
                  notes=('A name error means a cell was skipped, so run all cells from the top. '
                         'A gradient with the wrong sign usually means the error was computed as actual minus prediction. Use prediction minus actual, the same as on the slides. '
                         'If both entries are equal, the multiplier x was left out of the w entry. And in the spreadsheet, if all the grid cells show the same number, a cell reference moved when you copied the formula. In B4, lock the row of w, written B dollar 3, and the column of b, written dollar A 4.')))

    S.append(dict(kind='idea', title='Where this appears in AI: a gradient with billions of entries',
                  visual=dict(kind='mc_scale', items=[dict(label='Our line fit', value=2, text='2 parameters'), dict(label='Open model, 8 billion class', value=8e9, text='8,000,000,000 parameters'),
                                                      dict(label='Open model, 70 billion class', value=7e10, text='70,000,000,000 parameters')]),
                  lead='Open models such as Llama 3 list 8 billion and 70 billion parameters. The gradient has one entry for each.',
                  points=['At 2 bytes each, 8 billion entries take 16 GB. Published mixed-precision training also keeps 32-bit copies: several times more memory.', 'Sizes of ChatGPT, Gemini and Claude are not published.'],
                  notes=('This is the scale of what you computed today. Published open models, such as the Llama 3 family, list sizes of eight billion and seventy billion parameters. '
                         'The gradient of the loss has one entry for each parameter, so a training step produces billions of partial derivatives. '
                         'If each entry is stored in sixteen bits, or two bytes, eight billion entries alone take sixteen gigabytes. Published mixed-precision training also keeps a thirty-two bit copy of the weights and the optimiser state, so the memory is several times larger. '
                         'The sizes of ChatGPT, Gemini and Claude are not published, so we do not guess them. The mathematics is the one you did by hand with two parameters.')))

    S.append(dict(kind='steps', title='Where this appears in AI: one training step moves every parameter against its own gradient entry',
                  steps=[dict(head='Loss', text='Run some text through the model and measure one loss number', icon='calculator'), dict(head='Gradient', text='One partial derivative for each of the N parameters', icon='chart'),
                         dict(head='Step', text='Each parameter moves a little against its own entry', icon='gear'), dict(head='Repeat', text='A new loss, a new gradient, another step', icon='flag')], highlight=2,
                  caption='How the gradient is found through many layers is Sessions 9 and 11 (the backward pass). How big each step is, the learning rate, is Session 10.',
                  notes=('Published research describes training as a loop around today\'s idea. Run some text through the model and measure the loss. Compute the gradient, one entry for each of the billions of parameters. '
                         'Then move every parameter a little against its own entry, so a parameter with a large negative entry rises the most. Repeat with new text. '
                         'Two pieces are still missing. Finding the gradient through many layers needs the chain rule, Session 9, and the backward pass of Session 11. Choosing how big a step to take is the learning rate, Session 10.')))

    S.append(dict(kind='practice', title='Ask an AI assistant for the same two partial derivatives and compare', minutes=8, label='Hands-on, with any assistant',
                  task='Ask an assistant for the partial derivatives of the mean squared error of y-hat = b + w x at w = 1, b = 0.',
                  steps=['Give it x = 1, 2, 3, 4 and y = 3, 5, 6, 9.', f'Compare with ours: ({G0[0]:g}, {G0[1]:g}).', 'Run your lab gradient code.',
                         'If it differs, find the first line that differs.'],
                  output='One line: its gradient, yours, match or not. Never paste confidential data into an assistant.',
                  notes=('A short hands-on activity. Ask any AI assistant for the partial derivatives of the mean squared error for our model at w equal to one and b equal to zero, and give it the four data points. '
                         f'Our answer is minus eighteen point five and minus six point five. Check the assistant\'s numbers against that and against your own lab code. '
                         'Assistants are often right on this kind of calculation, but they can slip on a sign or a factor of two. If the assistant differs, ask for the steps and find the first line that differs. '
                         'Please never paste confidential data into an assistant.')))

    S.append(dict(kind='table', title='Exit check: a partial derivative, a downhill step and the size of a gradient',
                  headers=['Question', 'Short answer'],
                  rows=[['For f(x, y) = x squared times y, what is the partial derivative with respect to y at (3, 2)?', '9. Treat x squared as a constant: the slope in y is x squared, which is 9.'],
                        ['The gradient of a loss at some point is (4, -2). In which direction do you step to reduce the loss?', 'Along minus the gradient: (-4, 2). Decrease the first parameter, increase the second.'],
                        ['How many entries does the gradient of a model with 20 parameters have?', '20, one partial derivative for each parameter.']],
                  widths=[5.8, 6.2], icons=False, note='Write your own answer before you read ours. The automatic check counts the lab numbers.',
                  notes=('Three questions to close. One: f of x and y equals x squared times y. The partial derivative with respect to y treats x squared as a constant, so it equals x squared, which is nine at x equal to three. '
                         'Two: the gradient is four and minus two. We step along minus the gradient, minus four and plus two, so the first parameter goes down and the second goes up. '
                         'Three: a model with twenty parameters has a gradient with twenty entries. Write your own answers first, then compare. Then save your work.')))

    s['facilitator'] = dict(
        prep=['Open the deck in Slide Show mode, the notebook in Colab and the workbook in Excel or Google Sheets. Run the solution notebook once from the top and check it ends with All 10 checks pass; the workbook Check sheet has 15 checks.',
              'Put the notebook and workbook in the shared class folder and post the link. Both use the same four deliveries as Session 7.',
              f'Write the check numbers on the board: L(1,0) = 11.75, gradient (-18.5, -6.5), best (1.9, 1), steepest downhill unit vector ({UNIT[0]:.3f}, {UNIT[1]:.3f}).',
              'Bring a printed contour map (a hiking map or a weather pressure map) to show that contour lines are everyday objects.'],
        misconceptions=[('The gradient points downhill', 'It points uphill, in the direction of steepest increase. Training steps along minus the gradient.'),
                        ('A partial derivative changes all inputs a little', 'It changes one input and holds the others fixed. Nudging two together measures a diagonal slope.'),
                        ('The gradient points straight at the minimum', 'It points in the steepest direction at the current point, which crosses the contour lines at a right angle. On a long narrow bowl that is far from the centre direction.'),
                        ('A zero gradient always means a minimum', 'It can be a maximum or a saddle point. In our bowl it is the minimum.'),
                        ('The 2 / n in the gradient comes from the power rule alone', 'The 2, the x_i and the 1 all come from the chain rule (Session 9).')],
        probes=[('Why does ∂L/∂b have no x in it?', 'Because b is added to the prediction, so a change in b shifts every prediction by the same amount. Its multiplier is 1.'),
                ('What are the partial derivatives of x squared plus y squared at (3, 4)?', '6 and 8. The gradient is (6, 8) with length 10.'),
                ('Which way is the loss falling fastest at the start?', f'Along minus the gradient (18.5, 6.5), or as a unit vector ({UNIT[0]:.3f}, {UNIT[1]:.3f}): mostly more w, a little more b.'),
                ('What does a long, thin contour ellipse tell you?', 'The loss changes quickly in one direction and slowly in the other. This slows down simple training (Session 10).'),
                ('Why does the gradient have the same length as the parameter list?', 'There is one partial derivative for each parameter.'),
                ('Is the gradient of the loss at the best fit exactly zero in the spreadsheet?', 'Up to rounding, yes. Excel shows a tiny number such as 1E-15.')],
        lab_steps=[('Python step 1: the loss', 'L(1, 0) = 11.75 and L(1.9, 1) = 0.175. Spreadsheet: sheet Gradient, the loss cells.'),
                   ('Python step 2: the gradient by formula', '(-18.5, -6.5) at the start, length 19.61. Learners who get (18.5, 6.5) subtracted in the wrong order. Spreadsheet: SUMPRODUCT with the same four rows.'),
                   ('Python step 3: nudges', 'Both estimates agree with the formulas to 3 decimals. If one is far off, h is too large or the nudge changed both parameters.'),
                   ('Python step 4: the grid', 'Smallest loss 0.25 on the 0.5 grid, a tie between (w = 2, b = 0.5) and (w = 2, b = 1), cells F7 and F8 of sheet Grid. A 0.1 grid finds 0.175 at (1.9, 1).'),
                   ('Python steps 5 and 6: contour plot and steepest direction', f'Unit vector ({UNIT[0]:.3f}, {UNIT[1]:.3f}); the best of 360 small steps points the same way to within 0.02. Spreadsheet: Gradient B30 and B31. The CHANGE task moves the start to (3, 0).')],
        rescue=['If the concepts run over, skip the grid slide and the numeric check slide. Say them in the lab.', 'If only half of the lab time remains, do stages one and two. Stages three and four become practice at home.',
                'If Colab is slow, use the spreadsheet track for everyone. The numbers are identical.', 'If a learner is lost on partial derivatives, return to f(x, y) = x squared + 3 y squared: treat the other input as a number.'],
        after=['Share the notebook, the workbook and the slides as PDF.', 'Ask learners to write one sentence on why the gradient has one entry for each parameter.', 'Note any question you could not answer and start Session 9 with it.'],
        lab_answer_key=[['PREDICT: sign of ∂L/∂w at the start?', 'Negative, because the line is too low: all four errors are negative (-2, -3, -3, -5).'],
                        ['READ: gradient at (1, 0)', '(-18.5, -6.5).'],
                        ['READ: gradient at (1.9, 1)', 'About (0, 0). The loss is flat there.'],
                        ['CHANGE: nudge w and b together', 'About -25: a slope along the diagonal, equal to neither partial derivative (it is their sum).'],
                        ['READ: the 0.5 grid', 'Two cells tie at 0.25, (w = 2, b = 0.5) and (w = 2, b = 1). The true minimum 0.175 lies between grid points at w = 1.9, b = 1.'],
                        ['PREDICT: direction of steepest decrease at the start', f'Minus the gradient divided by its length, ({UNIT[0]:.3f}, {UNIT[1]:.3f}): much more w than b.'],
                        ['CHANGE: start at (3, 0)', f'The gradient is ({G3[0]:g}, {G3[1]:g}): both entries turn positive, so downhill points left and down (smaller w, smaller b).']])
    return s
