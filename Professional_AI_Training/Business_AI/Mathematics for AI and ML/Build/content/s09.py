"""Session 9: The chain rule and the Jacobian. Functions of functions, computation graphs, forward values and backward derivatives, the Jacobian of a vector function."""
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'kit'))

# ---- numbers used on the slides, computed once (same delivery data as Sessions 7 and 8)
X = np.array([1.0, 2.0, 3.0, 4.0])
Y = np.array([3.0, 5.0, 6.0, 9.0])
N = len(X)


def cd(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)


# chain rule example: y = (3x + 1) squared at x = 2
g_ = lambda x: 3 * x + 1
f_ = lambda u: u ** 2
yy = lambda x: f_(g_(x))
X0 = 2.0
U0, Y0 = g_(X0), yy(X0)
DYDU, DUDX = 2 * U0, 3.0
CHAIN = DYDU * DUDX
FD_F = (yy(X0 + 0.001) - yy(X0)) / 0.001
FD_C = cd(yy, X0, 1e-3)
assert (U0, Y0, DYDU, CHAIN) == (7, 49, 14, 42) and abs(FD_C - 42) < 1e-6
# other examples at x = 1
EXP2 = 2 * np.exp(2)                       # y = e^(2x)
LNX2 = 2 * 1 / (1 ** 2 + 1)                # y = ln(x^2 + 1)
assert abs(cd(lambda x: np.exp(2 * x), 1) - EXP2) < 1e-4 and abs(cd(lambda x: np.log(x ** 2 + 1), 1) - LNX2) < 1e-6
# tiny graph: one delivery x = 3, y = 6, model p = w x, loss L = (p - y)^2, at w = 1
XD, YD, W0 = 3.0, 6.0, 1.0
P0 = W0 * XD
E0 = P0 - YD
L0 = E0 ** 2
DLDP = 2 * E0
DPDW = XD
DLDW = DLDP * DPDW
assert (P0, E0, L0, DLDP, DLDW) == (3, -3, 9, -6, -18)
assert abs(cd(lambda w: (w * XD - YD) ** 2, W0) - DLDW) < 1e-5
LP, LM = (1.001 * XD - YD) ** 2, (0.999 * XD - YD) ** 2
# all four rows
ROW_E = W0 * X - Y
ROW_DP = 2 * ROW_E
ROW_DW = X * ROW_DP
MEAN_DW = float(np.mean(ROW_DW))
assert abs(MEAN_DW + 18.5) < 1e-9 and list(ROW_E) == [-2, -3, -3, -5] and list(ROW_DW) == [-4, -12, -18, -40]
# Jacobian: F(x1, x2) = (x1 x2, x1 + x2^2) at (2, 3)
F = lambda a, b: np.array([a * b, a + b ** 2])
AT = (2.0, 3.0)
FV = F(*AT)
JAC = np.array([[AT[1], AT[0]], [1.0, 2 * AT[1]]])
assert list(FV) == [6, 11] and JAC.tolist() == [[3, 2], [1, 6]]


def num_jac(a, b, h=1e-5):
    return np.array([(F(a + h, b) - F(a - h, b)) / (2 * h), (F(a, b + h) - F(a, b - h)) / (2 * h)]).T


assert np.allclose(num_jac(*AT), JAC, atol=1e-6)
NJ = num_jac(*AT)
GUV = np.array([FV[1], FV[0]])           # s = u v: (ds/du, ds/dv) = (v, u) = (11, 6)
GX = JAC.T @ GUV
sfun = lambda a, b: F(a, b)[0] * F(a, b)[1]
assert list(GX) == [39, 58] and abs(cd(lambda a: sfun(a, 3.0), 2.0) - 39) < 1e-4 and abs(cd(lambda b: sfun(2.0, b), 3.0) - 58) < 1e-4
assert abs(0.0 + (yy(3.0) - yy(2.0)) / 1.0 - 51) < 1e-9


def build():
    s = dict(
        num=9, block='Calculus and optimisation', short_title='The chain rule and the Jacobian',
        title='The chain rule and the Jacobian: how a slope travels backwards through a model made of many steps',
        question='A model is a long chain of steps from the input to the loss. How does the slope of the loss reach a number buried many steps deep?',
        outcome_head='By the end of today you can',
        outcomes=['Differentiate a function of a function with the chain rule and check the answer with a finite difference',
                  'Draw a computation graph, then compute forward values and backward derivatives on a tiny two-step graph',
                  'Write down and compute the Jacobian matrix of a vector function with two inputs and two outputs'],
        outcome_icons=['calculator', 'chart', 'flag'],
        outcome_note=('By the end of today you can do three things. First, differentiate a function of a function with the chain rule, and check the result with ordinary arithmetic. '
                      'Second, draw a computation graph and run it twice, forwards to get values and backwards to get derivatives, on a graph with two steps. '
                      'Third, write down the Jacobian, the matrix that holds every slope of a function with several inputs and several outputs, and compute it for two inputs and two outputs. '
                      'Everything today feeds Session 11, where you build backpropagation by hand.'),
        clock=[(10, 'Recall, and a real question from AI that today answers'), (35, 'Concept: a picture, then a hand example'), (10, 'Break'),
               (45, 'Lab in Python or a spreadsheet: predict, run, change one thing'), (15, 'Where it appears in ChatGPT, Gemini, Claude; exit check'), (5, 'Save the work')],
        plan_title='Your two hours: chain rule, graphs, the Jacobian, then the lab',
        plan_caption='Pictures and hand examples first, then the lab on the same numbers in Python or a spreadsheet.',
        plan_note=('Here is how the two hours run. We start with a short recall of Session 8 and the question for today. Then thirty-five minutes of concepts, with a picture first and then a calculation by hand. '
                   'After the break you spend forty-five minutes in the lab, in Python or in a spreadsheet, on the same delivery data as the last two sessions. '
                   'The last twenty minutes show where this appears in AI and give you an exit check.'),
        recall_from='Session 8',
        recall=[('What is a partial derivative?',
                 'The slope of a function when you change one input and hold all the other inputs fixed.'),
                ('What is the gradient, and which way does it point?',
                 'The vector of all the partial derivatives. It points in the direction of steepest increase, so training steps along minus the gradient.'),
                ('The loss of the line y-hat = w x + b at w = 1, b = 0 has gradient (-18.5, -6.5). What does it tell you to do?',
                 'Raise both w and b, because both entries are negative. The w entry is larger in size (18.5 against 6.5), so the loss is more sensitive to w here.')],
        words=[('Composite function', 'A function of a function: the output of one function becomes the input of the next. Written f(g(x)).'),
               ('Chain rule', 'The derivative of a composite function is the derivative of the outer function times the derivative of the inner function.'),
               ('Computation graph', 'A picture of a calculation as boxes (values) and arrows (operations), from the inputs to the loss.'),
               ('Jacobian', 'The matrix of all the partial derivatives of a function with several inputs and several outputs. One row for each output, one column for each input.'),
               ('Backpropagation', 'Computing the derivatives of the loss by applying the chain rule backwards through the computation graph.')],
        word_icons=['gear', 'key', 'pin', 'chart', 'flag'],
        words_note=('Five words for today. A composite function is a function of a function. The chain rule gives its derivative as the outer derivative times the inner derivative. '
                    'A computation graph is a picture of a calculation, with boxes for values and arrows for operations. The Jacobian is the matrix of all the partial derivatives of a function with several outputs. '
                    'And backpropagation is the chain rule applied backwards through a computation graph. These are the real industry names, and you will see them in every machine learning paper and library manual.'),
        keep='Keep your saved lab. Write down the chain rule slope 42, the backward value -18 for the tiny graph, and the Jacobian, rows (3, 2) and (1, 6).',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Saved lab', value='Notebook or workbook'), dict(label='Chain rule slope', value='42'),
                                                              dict(label='Backward value', value='dL/dw = -18'), dict(label='Next session', value='Gradient descent')]),
        keep_title='Save the lab and keep the chain rule slope, the backward value and the Jacobian',
        next='Session 10: gradient descent.', next_label='Next session',
        keep_note=('Before you go, save your notebook or workbook. Keep three numbers. The chain rule slope, forty-two. The backward value for the tiny graph, minus eighteen. '
                   'And the Jacobian, with rows three, two and one, six. Next session we use these slopes to take steps downhill, which is gradient descent. If anything was unclear, write the question down and bring it.'),
        cover_note=('Welcome to Session 9. In Session 8 you computed a gradient by a direct formula. Real models are not one formula. They are many steps stacked on top of each other, and the slope has to be passed back through every step. '
                    'The tool for that is the chain rule. Today we learn it with small numbers, draw it as a graph, and meet the Jacobian, the matrix version of a slope.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 8',
                  headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.2, 6.8], icons=False,
                  note='If one answer surprised you, look back at Session 8 before the lab.',
                  notes=('Here are the short answers. A partial derivative is the slope when you change one input and hold the others fixed. '
                         'The gradient is the vector of all the partial derivatives. It points to steepest increase, so training steps along minus the gradient. '
                         'And at w equal to one and b equal to zero, both entries of the gradient are negative, so we raise both parameters, and the loss is more sensitive to w, because its entry is larger in size. '
                         'Today the question is how such a gradient is found when the model has many steps.')))

    S.append(dict(kind='wide', title='A function of a function: the output of one step becomes the input of the next',
                  visual=dict(kind='mc_graph', nodes=[dict(x=0.0, y=0.5, label='x', fwd='x = 2', width=1.3), dict(x=0.5, y=0.5, label='u', fwd='u = 7', width=1.3),
                                                      dict(x=1.0, y=0.5, label='y', fwd='y = 49', width=1.3, fill='gold')],
                              edges=[dict(a=0, b=1, label='u = 3x + 1'), dict(a=1, b=2, label='y = u squared')], size=24, small=20, box_h=0.9),
                  caption='Two steps. The input x = 2 becomes u = 7, and u becomes y = 49.',
                  notes=('Here is a function of a function, called a composite function. We start with x equal to two. The first step makes u, which is three x plus one, so u is seven. '
                         'The second step takes u and squares it, so y is forty-nine. The output of the first step is the input of the second. '
                         'We write the whole thing as y equals f of g of x, where g is the inner step and f is the outer step. '
                         'A model is exactly this, with many more steps. What would the picture look like with three steps?')))

    S.append(dict(kind='wide', title='The chain rule: slopes along the chain multiply',
                  visual=dict(kind='mc_graph', nodes=[dict(x=0.0, y=0.5, label='x', fwd='x = 2', width=1.3), dict(x=0.5, y=0.5, label='u', fwd='u = 7', width=1.3),
                                                      dict(x=1.0, y=0.5, label='y', fwd='y = 49', width=1.3, fill='gold')],
                              edges=[dict(a=0, b=1, label='u = 3x + 1', back='du/dx = 3'), dict(a=1, b=2, label='y = u squared', back='dy/du = 14')], size=24, small=20, box_h=0.9),
                  caption='A tiny step in x moves u 3 times as far; in u, y 14 times as far. So y moves 3 × 14 = 42 times as far.',
                  notes=('Now the slopes. The first step has slope three: a tiny step in x moves u three times as much. The second step, squaring, has slope two u, which is fourteen at u equal to seven. '
                         'A tiny step in u moves y fourteen times as much. So a tiny step in x moves u three times as much, and that moves y fourteen times as much again. '
                         'The total is three times fourteen, forty-two times as much. That is the chain rule: slopes along the chain multiply. Can you see why they multiply and not add?')))

    S.append(dict(kind='formula', title='The chain rule: dy/dx is dy/du times du/dx',
                  formulas=[('Chain rule', r'$\frac{dy}{dx} = \frac{dy}{du}\cdot\frac{du}{dx}$'), ('Our data at x = 2', r'$\frac{dy}{dx} = 14 \times 3 = 42$')],
                  symbols=[['y = f(u)', 'The outer function: it takes u and returns y.', 'y = u squared; dy/du = 2u = 14 at u = 7'],
                           ['u = g(x)', 'The inner function: it takes x and returns u.', 'u = 3x + 1; du/dx = 3'],
                           ['dy/dx', 'The slope of the whole chain: how fast y changes when x changes.', f'{CHAIN:g} at x = 2']],
                  size=24, note='Evaluate dy/du at the value of u that the forward step produced (u = 7), not at x.',
                  notes=('Here is the chain rule as a formula. The slope of y with respect to x equals the slope of y with respect to u, times the slope of u with respect to x. '
                         'In our example the outer function is y equals u squared, so its slope is two u, which is fourteen at u equal to seven. '
                         'The inner function is u equal to three x plus one, with slope three. Multiply and you get forty-two. '
                         'One detail matters. The outer slope is evaluated at the value of u that the forward step produced, not at x. Why does that matter?')))

    S.append(dict(kind='table', title='Check the chain rule with a finite difference: y = (3x + 1) squared at x = 2',
                  headers=['Step h', 'y(2 + h)', 'y(2)', 'Forward slope = (y(2 + h) minus y(2)) / h'],
                  rows=[[f'{h:g}', f'{yy(X0 + h):.6g}', '49', f'{(yy(X0 + h) - yy(X0)) / h:.4f}'] for h in (1, 0.1, 0.01, 0.001)],
                  widths=[1.6, 2.6, 1.6, 6.2], icons=False,
                  note=f'The slopes settle on 42, the chain rule answer. The central difference with h = 0.001 gives {FD_C:.4f}. In the lab you check every chain rule answer this way.',
                  notes=(f'Never trust a derivative you have not checked. Here we nudge x by a small step h and divide the change in y by h. With h equal to one, the slope is fifty-one, which is too crude. '
                         f'As h shrinks the slopes settle on forty-two, the chain rule answer. The forward difference with h equal to point zero zero one gives {FD_F:.3f}, and the central difference, which looks on both sides, gives {FD_C:.3f}. '
                         'This is the same check you used in Sessions 7 and 8. What would you suspect if the check gave fourteen?')))

    S.append(dict(kind='table', title='Three more chain rule examples, worked with numbers at x = 1',
                  headers=['Function y(x)', 'Inner u', 'Outer in u', 'du/dx', 'dy/du', 'dy/dx at x = 1'],
                  rows=[['y = (3x + 1) squared', '3x + 1', 'u squared', '3', '2u = 8', '24'],
                        ['y = e to the 2x', '2x', 'e to the u', '2', 'e^u = 7.389', f'{EXP2:.3f}'],
                        ['y = ln(x squared + 1)', 'x squared + 1', 'ln u', '2x = 2', '1/u = 0.5', f'{LNX2:g}']],
                  widths=[3.1, 1.9, 1.9, 1.1, 1.8, 2.3], icons=False,
                  note='The second row explains the remark in Session 7: e to the 2x has slope 2 times e to the 2x.',
                  notes=('Three more examples at x equal to one. The first is the one we just did, now at x equal to one: the outer slope two u is eight, the inner slope is three, so twenty-four. '
                         'The second is e to the two x. The inner function is two x with slope two, the outer function is e to the u, whose slope is e to the u, seven point three eight nine, so the answer is fourteen point seven seven eight. '
                         'That is the remark from Session 7. The third is the natural logarithm of x squared plus one. The inner slope is two x, the outer slope is one over u, which is one half, and the product is one. '
                         'Which of these three would you check first with a finite difference?')))

    S.append(dict(kind='compare', title='Two mistakes to avoid with the chain rule',
                  left=dict(head='Forgetting the inner slope', icon='cross', points=['The slope of u squared is 2u.', 'But u = 3x + 1 also changes with x.', 'Multiply by du/dx = 3 as well.']),
                  right=dict(head='Adding instead of multiplying', icon='flag', points=['Slopes along a chain multiply.', '14 + 3 = 17 is wrong here.', '14 times 3 = 42 is right.']),
                  verdict='Outer slope times inner slope, each evaluated at its own value.',
                  notes=('Two mistakes catch many people. First, forgetting the inner slope. If you differentiate u squared and write two u, you have only done the outer step. Since u itself depends on x, you must also multiply by the slope of the inner step. '
                         'In our example that gives fourteen, instead of forty-two. Second, adding the slopes instead of multiplying them. If a step makes u grow three times as fast as x, and y grows fourteen times as fast as u, the effects compound, so we multiply. '
                         'The finite difference check catches both mistakes immediately. Which of the two would you be more likely to make when tired?')))

    S.append(dict(kind='wide', title='A computation graph draws a calculation as boxes for values and arrows for operations',
                  visual=dict(kind='mc_graph', nodes=[dict(x=0.0, y=0.5, label='w', fwd='w = 1', width=1.3), dict(x=0.5, y=0.5, label='p', fwd='p = 3', width=1.3),
                                                      dict(x=1.0, y=0.5, label='L', fwd='L = 9', width=1.3, fill='gold')],
                              edges=[dict(a=0, b=1, label='p = w x'), dict(a=1, b=2, label='L = (p - y) squared')], size=24, small=20, box_h=0.9),
                  caption='One delivery: x = 3 km, y = 6. Forward: p = 1 times 3 = 3, then L = (3 - 6) squared = 9.',
                  notes=('Now a computation graph for the model you know. Take one delivery, three kilometres, fee six thousand shillings. The model predicts p equals w times x. With w equal to one, p is three. '
                         'The loss for that delivery is p minus six, squared, which is nine. Each box holds a value, and each arrow is an operation. '
                         'Running the graph from left to right, from the parameter to the loss, is called the forward pass. '
                         'This graph has only two steps. What would be a third step in a bigger model?')))

    S.append(dict(kind='wide', title='Backward: each box gets the slope of the loss with respect to it',
                  visual=dict(kind='mc_graph', nodes=[dict(x=0.0, y=0.5, label='w', fwd='w = 1', bwd='dL/dw = -18', width=1.5), dict(x=0.5, y=0.5, label='p', fwd='p = 3', bwd='dL/dp = -6', width=1.5),
                                                      dict(x=1.0, y=0.5, label='L', fwd='L = 9', bwd='dL/dL = 1', width=1.5, fill='gold')],
                              edges=[dict(a=0, b=1, label='p = w x', back='dp/dw = x = 3'), dict(a=1, b=2, label='L = (p - y) squared', back='dL/dp = 2(p - y) = -6')], size=22, small=18, box_h=0.9),
                  caption='Black: forward values. Red: backward derivatives. Start at 1, multiply by each local slope.',
                  notes=('Now the backward pass, in red. We start at the loss, where the slope of L with respect to itself is one. '
                         'Moving one step back, the local slope of the loss with respect to p is two times p minus y, which is minus six. So the red value at p is minus six. '
                         'Moving one more step back, the local slope of p with respect to w is x, which is three. The red value at w is minus six times three, minus eighteen. '
                         'Each red value is the previous red value times the local slope of one arrow. Why is the red value at w the slope we wanted?')))

    S.append(dict(kind='formula', title='Backward pass on the tiny graph: multiply the local slopes along the path',
                  formulas=[('Chain rule on the graph', r'$\frac{dL}{dw} = \frac{dL}{dp}\cdot\frac{dp}{dw}$'), ('Our data', r'$\frac{dL}{dw} = (-6)\times 3 = -18$')],
                  symbols=[['dL/dp', 'Local slope of the loss in p: 2 (p - y), with p = 3, y = 6.', f'{DLDP:g}'],
                           ['dp/dw', 'Local slope of p in w: p = w x, so the slope is x.', f'{DPDW:g}'],
                           ['dL/dw', 'The slope of the loss in w: the product of the two.', f'{DLDW:g}']],
                  size=24, note='A local slope is the derivative of one box\'s output with respect to its own input.',
                  notes=(f'The same result as a formula. The slope of L with respect to w equals the slope of L with respect to p times the slope of p with respect to w. '
                         'The first factor is two times p minus y, two times minus three, minus six. The second is x, three. The product is minus eighteen. '
                         f'You can check it by nudging w by point zero zero one up and down. The loss goes to {LP:.3f} and {LM:.3f}, and the central difference is minus eighteen. '
                         'Which sign does minus eighteen tell you to move w?')))

    S.append(dict(kind='table', title='Backward values for all four deliveries at w = 1: the average is the Session 8 slope',
                  headers=['Row i', 'Distance x', 'Error p minus y', 'dL/dp = 2 e', 'dL/dw = x times dL/dp'],
                  rows=[[str(i + 1), f'{X[i]:g}', f'{ROW_E[i]:g}', f'{ROW_DP[i]:g}', f'{ROW_DW[i]:g}'] for i in range(4)] + [['Mean', '', '', '', f'{MEAN_DW:g}']],
                  widths=[1.4, 2.0, 2.6, 2.4, 3.6], icons=False,
                  note='Row 3 is the graph we just drew: -6 and -18. The mean loss has the mean of the four backward values: -18.5, as in Session 8.',
                  notes=('Now all four deliveries. For each row we run the tiny graph backwards. The error p minus y is minus two, minus three, minus three and minus five. '
                         'Twice the error gives the slope of that row loss in p, and multiplying by x gives the slope in w, minus four, minus twelve, minus eighteen and minus forty. '
                         'Row three is exactly the graph we drew. The loss of the whole dataset is the mean of the four row losses, so its slope is the mean of the four backward values, minus seventy-four over four, minus eighteen point five. '
                         'That is the same number you found in Session 8 by the direct formula.')))

    S.append(dict(kind='wide', title='A vector function has several outputs: the Jacobian holds every slope',
                  visual=dict(kind='mc_warp', jac=[[3, 2], [1, 6]], at=[2, 3], sc=0.3),
                  caption='A very small square becomes almost a parallelogram with the columns of J as sides.',
                  notes=('Now functions with several outputs. Take a function with two inputs and two outputs. Picture a very small square of inputs, one tiny step in x one and one tiny step in x two. '
                         'The function sends that square to a parallelogram, almost exactly,  in the output plane. The two sides of the parallelogram are the two columns of a two by two matrix, called the Jacobian. '
                         'So near one point, the function acts like the matrix multiplication you met in Session 3. For the point and the function we use in a moment, the columns are three, one and two, six. '
                         'What does a bigger column tell you?')))

    S.append(dict(kind='formula', title='The Jacobian: one row for each output, one column for each input',
                  formulas=[('Jacobian entry', r'$J_{ij} = \frac{\partial F_i}{\partial x_j}$'), ('Our function', r'$u = x_1 x_2 \qquad v = x_1 + x_2^{2}$')],
                  symbols=[['F_i', 'Output i of the function F. Here F_1 = u, F_2 = v.', 'at (2, 3): u = 6, v = 11'],
                           ['x_j', 'Input number j. Here x_1 and x_2.', 'the point (2, 3)'],
                           ['J_ij', 'The slope of output i in input j. J has 2 rows and 2 columns.', 'J = rows (3, 2) and (1, 6)']],
                  size=24, note='Row 1: du/dx1 = x2 = 3, du/dx2 = x1 = 2. Row 2: dv/dx1 = 1, dv/dx2 = 2 x2 = 6.',
                  notes=('Here is the definition. The Jacobian entry in row i and column j is the partial derivative of output i with respect to input j. '
                         'Our function has u equal to x one times x two, and v equal to x one plus x two squared. At the point two, three the outputs are six and eleven. '
                         'The first row holds the slopes of u: with respect to x one it is x two, which is three, and with respect to x two it is x one, which is two. '
                         'The second row holds the slopes of v: one, and two times x two, which is six. Why does each row come from one output?')))

    S.append(dict(kind='idea', title='The Jacobian drawn as a matrix, with the numbers at the point (2, 3)',
                  visual=dict(kind='mc_jac', rows=['u', 'v'], cols=['x1', 'x2'],
                              cells=[[r'$\frac{\partial u}{\partial x_1}$', r'$\frac{\partial u}{\partial x_2}$'], [r'$\frac{\partial v}{\partial x_1}$', r'$\frac{\partial v}{\partial x_2}$']],
                              nums=[['3', '2'], ['1', '6']], caption_rows='outputs', caption_cols='inputs'),
                  lead='Each gold number is one partial derivative at the point (2, 3).',
                  points=['Row u: x2 = 3 and x1 = 2.', 'Row v: 1 and 2 x2 = 6.', 'Check one entry: nudging x2 from 3 to 3.001 raises v by 0.006001, so 6.001 per unit.'],
                  notes=('The same Jacobian drawn as a matrix. The rows are the outputs, u and v, and the columns are the inputs, x one and x two. '
                         'Each cell holds one partial derivative, with the symbol on top and the number at the point two, three in gold. '
                         'To check one entry, nudge x two from three to three point zero zero one with x one held fixed. The output v goes up by point zero zero six zero zero one, so the slope is six point zero zero one, close to six. '
                         'The central difference gives exactly six. How would you check the other three entries?')))

    S.append(dict(kind='table', title='Check the Jacobian with finite differences: nudge one input at a time',
                  headers=['Nudge', 'u changes to', 'v changes to', 'Column of J'],
                  rows=[['x1: 2 + h and 2 - h, h = 0.00001', f'{F(2.00001, 3)[0]:.5f} and {F(1.99999, 3)[0]:.5f}', f'{F(2.00001, 3)[1]:.5f} and {F(1.99999, 3)[1]:.5f}', f'({NJ[0, 0]:.3f}, {NJ[1, 0]:.3f})'],
                        ['x2: 3 + h and 3 - h, h = 0.00001', f'{F(2, 3.00001)[0]:.5f} and {F(2, 2.99999)[0]:.5f}', f'{F(2, 3.00001)[1]:.5f} and {F(2, 2.99999)[1]:.5f}', f'({NJ[0, 1]:.3f}, {NJ[1, 1]:.3f})']],
                  widths=[3.9, 2.9, 2.9, 2.3], icons=False,
                  note='Each column is (change in u, change in v) divided by 2h. Two inputs, two nudges, two columns.',
                  notes=('To check a Jacobian we nudge one input at a time. Nudge x one up and down with x two held fixed, and look at both outputs. The change in u divided by two h is three, and the change in v is one. That is the first column, three, one. '
                         'Then nudge x two with x one held fixed. The changes give two and six, the second column. '
                         'So one nudge of one input gives one whole column of the Jacobian, and a function with a thousand inputs needs a thousand nudges, which is why libraries use the chain rule instead. '
                         'Can you see why?')))

    S.append(dict(kind='formula', title='The chain rule with a Jacobian: the backward step multiplies by J transposed',
                  formulas=[('Backward through a vector step', r'$\nabla_x\, s = J^{T}\,\nabla_{(u,v)}\, s$'), ('Our data for s = u v', r'$\nabla_x\, s = (3 \cdot 11 + 1 \cdot 6,\ 2 \cdot 11 + 6 \cdot 6) = (39,\ 58)$')],
                  symbols=[['s', 'A single number computed from the outputs: s = u v = 6 times 11 = 66.', 'ds/du = v = 11; ds/dv = u = 6'],
                           ['J transposed', 'The Jacobian with rows and columns swapped. It sends output slopes back to the inputs.', 'J^T = rows (3, 1) and (2, 6)'],
                           ['gradient of s in x', 'The slope of s in each input, by the chain rule.', f'({GX[0]:g}, {GX[1]:g})']],
                  size=22, note='Check directly: s = x1 squared x2 + x1 x2 cubed, so ds/dx1 = 39 and ds/dx2 = 58.',
                  notes=('Here is the chain rule when a step has several outputs. Suppose a single number s is computed from u and v, say s equals u times v. Its slopes with respect to u and v are v and u, which are eleven and six. '
                         'To bring them back to the inputs, multiply by the transpose of the Jacobian. The first input gets three times eleven plus one times six, thirty-nine. The second gets two times eleven plus six times six, fifty-eight. '
                         'You can check that directly, because s expands to x one squared x two plus x one x two cubed, and its two partial derivatives are thirty-nine and fifty-eight. '
                         'This one line is the backward step of every layer of a neural network.')))

    S.append(dict(kind='wide', title='Many steps: the backward value is the product of the local slopes along the whole chain',
                  visual=dict(kind='mc_graph', nodes=[dict(x=0.0, y=0.5, label='input x', fwd='', bwd='dL/dx', width=1.7), dict(x=0.27, y=0.5, label='step 1', fwd='value 1', width=1.7),
                                                      dict(x=0.54, y=0.5, label='step 2', fwd='value 2', width=1.7), dict(x=0.77, y=0.5, ellipsis=True, label='...', width=0.7),
                                                      dict(x=1.0, y=0.5, label='loss L', fwd='L', bwd='start: 1', width=1.6, fill='gold')],
                              edges=[dict(a=0, b=1, back='slope 1'), dict(a=1, b=2, back='slope 2'), dict(a=2, b=3), dict(a=3, b=4)], size=18, small=15),
                  caption='Start at the loss with 1. Going back, each step multiplies by its local slope (red).',
                  notes=('Now what happens with many steps. Put as many boxes between the input and the loss as you like. Going backwards, each box multiplies the running value by one more local slope. '
                         'After the first step back you have one slope. After the second you have the product of two slopes, and so on. '
                         'A model with dozens of layers has dozens of such factors, and each one is computed by the same rule that you used for the tiny graph. '
                         'Nothing new is needed for the long chain. That is the whole idea of backpropagation. Why is it a good thing that every step uses the same rule?')))

    S.append(dict(kind='code', title='Read the recipe before you write it: forward, backward and a check',
                  code='p = w * x\nL = (p - y) ** 2\ndL_dp = 2 * (p - y)\ndL_dw = dL_dp * x\nprint(p, L, dL_dp, dL_dw)',
                  output=['3.0 9.0 -6.0 -18.0'],
                  reads=['Lines 1 and 2: the forward pass. p is the prediction, L the loss.', 'Line 3: the local slope of the loss in p, 2 (p - y).',
                         'Line 4: times the local slope of p in w, which is x. This is the chain rule.', 'With w = 1, x = 3, y = 6 it prints 3, 9, -6 and -18.'],
                  notes=('Before the lab, here is the recipe. The first two lines are the forward pass: the prediction p and the loss L. '
                         'The third line is the local slope of the loss with respect to p, two times p minus y. The fourth line multiplies it by the local slope of p with respect to w, which is just x. That is the chain rule in code. '
                         'With w equal to one, x equal to three and y equal to six, it prints three, nine, minus six and minus eighteen. '
                         'The notebook then checks it by nudging w. In the spreadsheet the same steps become columns.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the concepts. Everything you need is on the slides, and each step of the lab explains itself. '
                         'Please open the Python notebook or the spreadsheet workbook now. Both use the same numbers, so you can compare with someone who chose the other tool. '
                         'Work through the steps in order. Raise your hand if a cell gives an error. Remember the rhythm: predict first, then run, then change one thing.')))

    S.append(dict(kind='steps', title='The lab has four stages, in Python and in the spreadsheet',
                  steps=[dict(head='1 Chain rule', text='Slope of (3x + 1) squared and of e to the 2x', icon='calculator'), dict(head='2 Forward, backward', text='The tiny graph for one delivery, then four', icon='check'),
                         dict(head='3 Jacobian', text='By formula, then by nudging each input', icon='chart'), dict(head='4 Back to inputs', text='Multiply by J transposed and check', icon='flag')], highlight=1,
                  caption='Python: Steps 1 to 6 of the notebook. Spreadsheet: sheets Chain, Backward and Jacobian. Predict first, then run.',
                  notes=('Here is the lab map. Stage one computes the chain rule slope of two composite functions and checks them by nudging. '
                         'Stage two runs the tiny graph forward and backward for one delivery, and then for all four rows. '
                         'Stage three computes the Jacobian by formula and by nudging each input. Stage four multiplies by J transposed to bring the slopes back to the inputs, and checks the answer. '
                         'In Python you work through steps one to six. In the spreadsheet you use three sheets, named Chain, Backward and Jacobian.')))

    S.append(dict(kind='table', title='Check your numbers against these before you move on',
                  headers=['What you compute', 'You should see'],
                  rows=[['Chain rule slope of (3x + 1) squared at x = 2', '42'], ['Chain rule slope of e to the 2x at x = 1', f'{EXP2:.3f}'],
                        ['Forward values for the delivery x = 3, y = 6 at w = 1: p and L', '3 and 9'], ['Backward values: dL/dp and dL/dw', '-6 and -18'],
                        ['Mean of the four dL/dw values at w = 1', '-18.5'], ['Jacobian of (x1 x2, x1 + x2 squared) at (2, 3)', 'rows (3, 2) and (1, 6)'],
                        ['Gradient of s = u v in the inputs, J transposed times (11, 6)', '(39, 58)']],
                  widths=[7.6, 3.8], icons=['calculator', 'chart', 'check', 'flag', 'pin', 'gear', 'flag'],
                  note='If your number differs, stop and ask. Do not change a number to match. Find the step that went wrong.',
                  notes=('Use this table as your checkpoint. If your numbers match, carry on. If they do not, stop and call me. '
                         'The chain rule slope is forty-two, and for e to the two x it is fourteen point seven seven eight. For the tiny graph the forward values are three and nine, and the backward values minus six and minus eighteen. '
                         'The mean of the four backward values is minus eighteen point five. The Jacobian is three, two, one, six, and the gradient of s is thirty-nine and fifty-eight. '
                         'Do not edit a number to make it match. Finding why it differs is the skill you will use on every project.')))

    S.append(dict(kind='table', title='Errors you will meet, what they mean and what to do',
                  headers=['What you see', 'What it means', 'What to do'],
                  rows=[['NameError in Python', 'A cell that defines a name was skipped', 'Run all cells from the top, in order'],
                        ['Chain slope is 14 instead of 42', 'The inner slope du/dx was left out', 'Multiply by 3 as well as by 2u'],
                        ['Jacobian looks flipped', 'Rows and columns swapped: outputs are rows', 'Row i is output i, column j is input j'],
                        ['Spreadsheet shows #VALUE!', 'A range with text or a gap in a formula', 'Check that every cell in the range holds a number']],
                  widths=[3.4, 4.4, 4.2], icons=['bell', 'cross', 'flag', 'key'],
                  notes=('Errors are normal, and reading them is a skill. A name error means a cell was skipped, so run all cells from the top. '
                         'If your chain rule slope is fourteen instead of forty-two, you left out the inner slope. If your Jacobian looks flipped, remember that outputs are rows and inputs are columns. '
                         'And in the spreadsheet, a value error means a range holds text or a gap, so check that every cell in the range holds a number.')))

    S.append(dict(kind='wide', title='Where this appears in AI: the chain rule is used once for every layer',
                  visual=dict(kind='mc_graph', nodes=[dict(x=0.0, y=0.5, label='tokens', fwd='input', width=1.7), dict(x=0.3, y=0.5, label='layer 1', fwd='values', width=1.7),
                                                      dict(x=0.6, y=0.5, label='layer 2', fwd='values', width=1.7), dict(x=0.8, y=0.5, ellipsis=True, label='...', width=0.7),
                                                      dict(x=1.0, y=0.5, label='loss', fwd='one number', bwd='start: 1', width=1.5, fill='gold')],
                              edges=[dict(a=0, b=1, back='slopes'), dict(a=1, b=2, back='slopes'), dict(a=2, b=3), dict(a=3, b=4)], size=20, small=17, box_h=0.9),
                  caption='Red: backward slopes. Meta\'s Llama 3 paper (2024) lists 32 and 80 transformer layers (8B, 70B).',
                  notes=('Here is where this appears in AI. Published language models of this kind are stacks of layers. In the open Llama 3 family, Meta\'s Llama 3 paper from 2024 lists thirty-two transformer layers for the eight billion model and eighty for the seventy billion model. '
                         'Training does a forward pass through every layer to reach the loss, and then a backward pass that passes through every layer, and through the steps inside each layer, applying the chain rule at each one. '
                         'The exact designs of ChatGPT, Gemini and Claude are not published, so we do not quote their layer counts. '
                         'The mathematics is the same as the tiny graph you just built. In Session 11, you build backpropagation by hand.')))

    S.append(dict(kind='idea', title='Where this appears in AI: libraries run the chain rule for you, and you can check them',
                  visual=dict(kind='mc_entries', count_label='Backward pass: N slopes'),
                  lead='PyTorch and JAX record the computation graph and run the chain rule backwards for you.',
                  points=['This is automatic differentiation. Nudge checks like today\'s test it.', 'A layer\'s Jacobian can have millions of entries, so libraries never build it. They multiply slopes by J transposed directly.'],
                  notes=('Today you did by hand what libraries do automatically. Libraries such as PyTorch and JAX record the computation graph while the forward pass runs, and then run the chain rule backwards. '
                         'This is called automatic differentiation, and their manuals describe it. The result is a gradient with one entry for each parameter, like the one in Session 8. '
                         'The Jacobian of a whole layer can have millions of entries, so the libraries never build it. They multiply the incoming slopes by J transposed directly, which is called a vector-Jacobian product, just as we did with J transposed. '
                         'And the finite difference check you used today is how developers test that this code is correct.')))

    S.append(dict(kind='practice', title='Check an AI assistant\'s answer with your own numbers', minutes=8, label='Hands-on, with any assistant',
                  task='Ask an assistant for the Jacobian of F(x1, x2) = (x1 x2, x1 + x2 squared) at the point (2, 3).',
                  steps=['Ask it to explain each entry.', 'Compare with ours: rows (3, 2) and (1, 6).', 'Run your lab Jacobian code.',
                         'If it differs, find the first entry that differs.'],
                  output='One line: its Jacobian, yours, match or not. Never paste confidential data into an assistant.',
                  notes=('A short hands-on activity. Ask any AI assistant for the Jacobian of our function, x one times x two and x one plus x two squared, at the point two, three. '
                         'Our answer is three, two, one, six. Check the assistant against that and against your own lab code. '
                         'Assistants are often right on this kind of calculation, but they can swap rows and columns, so check which entry is which. '
                         'If it differs, ask for the steps and find the first entry that differs. Please never paste confidential data into an assistant.')))

    S.append(dict(kind='table', title='Exit check: three questions with short answers',
                  headers=['Question', 'Short answer'],
                  rows=[['What is the slope of y = (2x + 5) cubed at x = 0?', '150. Outer: 3u squared = 75. Inner: 2. Product 150.'],
                        ['A chain has three steps with local slopes 2, -3 and 0.5. What is the slope of the output with respect to the input?', '2 times -3 times 0.5 = -3.'],
                        ['What is the shape of the Jacobian of F(x1, x2) = (2 x1, x1 + x2), and what are its entries?', '2 rows (outputs) by 2 columns (inputs): rows (2, 0) and (1, 1).']],
                  widths=[5.8, 6.2], icons=False, note='Write your own answer before you read ours. The automatic check counts the lab numbers.',
                  notes=('Three questions to close. One: y equals two x plus five, cubed, at x equal to zero. The inner value u is five, the outer slope is three u squared, seventy-five, the inner slope is two, and the product is one hundred and fifty. '
                         'Two: three local slopes, two, minus three and one half. Multiply them and you get minus three. '
                         'Three: the Jacobian has two rows, one for each output, and two columns, one for each input. The first row is two and zero, the second row is one and one. '
                         'Write your own answers first, then compare. Then save your work.')))

    s['facilitator'] = dict(
        prep=['Open the deck in Slide Show mode, the notebook in Colab and the workbook in Excel or Google Sheets. Run the notebook once from the top and check it ends with All checks pass.',
              'Put the notebook and workbook in the shared class folder and post the link. They use the same delivery data as Sessions 7 and 8.',
              'Write the check numbers on the board: chain slope 42, backward values -6 and -18, mean -18.5, Jacobian rows (3, 2) and (1, 6), gradient (39, 58).',
              'Draw the two-box and three-box chains on the board before class. Learners will redraw them in the lab.'],
        misconceptions=[('Slopes along a chain add', 'They multiply, because each step scales the change that arrives from the step before.'),
                        ('The outer slope is evaluated at x', 'It is evaluated at the value of the inner function, u = g(x). For (3x + 1) squared at x = 2 that is u = 7.'),
                        ('The Jacobian has one row for each input', 'One row for each output and one column for each input. Row i is the gradient of output i.'),
                        ('Backpropagation is a different kind of mathematics', 'It is the chain rule, applied backwards through a graph and reusing the values from the forward pass.')],
        probes=[('Why must the forward pass come before the backward pass?', 'The local slopes depend on the forward values, for example 2 (p - y) needs p.'),
                ('What is the chain rule slope of y = e to the 3x at x = 0?', '3. Outer slope e^0 = 1, inner slope 3.'),
                ('If a layer has 1000 inputs and 1000 outputs, what shape is its Jacobian?', '1000 by 1000, a million entries. This is why libraries never write it out.'),
                ('What does a Jacobian entry of 0 mean?', 'That output does not change when that input is nudged, to first order.'),
                ('Why is the mean of the four backward values the slope of the mean loss?', 'The slope of an average is the average of the slopes (sum rule from Session 7).'),
                ('Why did the finite difference give 42.009 with h = 0.001 and 42.000 centrally?', 'The forward difference has an error of the order of h. The central difference cancels it for a quadratic.')],
        lab_steps=[('Python step 1: chain rule slopes', 'Slope 42 for (3x + 1) squared and 14.778 for e to the 2x. Learners who print 14 left out the inner slope. Spreadsheet: sheet Chain.'),
                   ('Python step 2: forward and backward on one delivery', 'p = 3, L = 9, dL/dp = -6, dL/dw = -18. Spreadsheet: sheet Backward, top block.'),
                   ('Python step 3: all four rows', 'Row backward values -4, -12, -18, -40 with mean -18.5, matching Session 8. Spreadsheet: sheet Backward, table.'),
                   ('Python steps 4 and 5: the Jacobian', 'Formula rows (3, 2) and (1, 6) and nudged values agree to 3 decimals. Spreadsheet: sheet Jacobian. If entries look transposed, rows and columns were swapped.'),
                   ('Python step 6: back to the inputs', 'J transposed times (11, 6) gives (39, 58); the nudged slopes of s agree. The CHANGE task moves the point to (1, 2).')],
        rescue=['If the concepts run over, skip the table of three more examples and the nudge table for the Jacobian. Say them in the lab.', 'If only half of the lab time remains, do stages one and two. Stages three and four become practice at home.',
                'If Colab is slow, use the spreadsheet track for everyone. The numbers are identical.', 'If a learner is lost on the Jacobian, go back to two outputs as two separate gradients stacked as rows.'],
        after=['Share the notebook, the workbook and the slides as PDF.', 'Ask learners to write one sentence on why slopes along a chain multiply.', 'Note any question you could not answer and start Session 10 with it.'],
        lab_answer_key=[['PREDICT: chain rule slope of (3x + 1) squared at x = 2', '42, which is 14 times 3.'],
                        ['READ: forward and backward values for one delivery', 'p = 3, L = 9, dL/dp = -6, dL/dw = -18.'],
                        ['READ: mean of the four row slopes', '-18.5, the same as the Session 8 gradient entry for w.'],
                        ['PREDICT: shape of the Jacobian', '2 by 2: rows are outputs u and v, columns are inputs x1 and x2.'],
                        ['CHANGE: move the point to (1, 2)', 'Jacobian rows (2, 1) and (1, 4); the outputs are 2 and 5; gradient of s is (2 x1 x2 + x2 cubed, x1 squared + 3 x1 x2 squared) = (12, 13).']])
    return s
