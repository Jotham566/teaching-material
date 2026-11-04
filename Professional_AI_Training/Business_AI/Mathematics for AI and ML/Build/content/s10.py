"""Session 10: Gradient descent. Author D."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'kit'))
import diagrams_math_d as D  # noqa: E402


def build():
    n = D.n10()
    f2 = lambda v: f'{v:.2f}'
    f3 = lambda v: f'{v:.3f}'
    f4 = lambda v: f'{v:.4f}'
    x, y, xc = n['x'], n['y'], n['xc']
    bw = n['bowl']
    ad = n['adam']
    R = n['runs']
    L0 = n['loss0']

    def fmt(v):
        return f'{v:.3f}'.rstrip('0').rstrip('.')

    def slope(w):
        return 2 * (w - 3)

    s = dict(
        num=10, block='Calculus and optimisation', short_title='Gradient descent',
        title='Gradient descent: training is walking downhill on the loss, one step at a time',
        question='How does a model with millions or billions of numbers find good values for all of them?',
        outcomes=['Apply the update rule w = w - eta times the gradient by hand, for one step and for several steps',
                  'Explain what happens when the learning rate is too small or too large, and what mini-batches, momentum and Adam change',
                  'Fit a line with gradient descent in Python or in a spreadsheet and compare the loss curves of several learning rates'],
        outcome_icons=['calculator', 'chart', 'gear'],
        outcome_note=('By the end of today you can do three things. First, apply the update rule by hand: the new w equals the old w minus the learning rate times the gradient. '
                      'Second, say what goes wrong when the learning rate is too small or too large, and what mini-batches, momentum and Adam change. '
                      'Third, fit a line with gradient descent, in Python or in a spreadsheet, and compare the loss curves for several learning rates. Which of the three sounds hardest to you right now?'),
        clock=[(10, 'Recall and a real question from AI'), (35, 'Concept: a picture, then a hand example'), (10, 'Break'),
               (45, 'Lab: Python or spreadsheet, predict, run, change'), (15, 'Where it appears in AI, plus an exit check'), (5, 'Save the work')],
        plan_title='Your two hours: learn the update rule, then watch it run',
        plan_caption='Pictures and hand calculations first. Then the lab: a loop in Python or one row per step.',
        plan_note=('We have two hours. The first ten minutes recall the chain rule from Session 9 and ask the question of the day. Then thirty-five minutes of concepts, with no laptop: the update rule, the learning rate, batches, momentum and Adam. '
                   'After a break comes the lab, forty-five minutes, where you run gradient descent yourself on a line fit. The last fifteen minutes show where it appears in ChatGPT, Gemini, Claude and other AI, then an exit check.'),
        recall_from='Session 9',
        recall=[('Use the chain rule: what is the derivative of y = (3x + 1) squared with respect to x?', 'It is 6(3x + 1): the outer derivative 2(3x + 1) multiplied by the inner derivative 3.'),
                ('A function takes 3 inputs and gives 2 outputs. What shape is its Jacobian matrix?', 'Two rows and three columns: one row for each output and one column for each input.'),
                ('Why does backpropagation need the chain rule?', 'A network is a function of functions, so the slope of the loss for an early weight is a product of the slopes along the path to the loss.')],
        words=[('Gradient descent', 'Repeatedly changing the parameters a little in the direction that lowers the loss.'),
               ('Learning rate (eta)', 'The size of each step. We write it as the Greek letter eta; some books write alpha.'),
               ('Epoch and mini-batch', 'An epoch is one pass through all the training rows. A mini-batch is a small group of rows used for one step.'),
               ('Momentum', 'A running memory of past gradients that smooths the path and speeds it up.'),
               ('Adam', 'An optimiser (Kingma and Ba, 2014) that gives each parameter its own step size.')],
        word_icons=['gear', 'clock', 'folder', 'chart', 'robot'],
        words_note=('Five words for today, and these are the names you will meet in papers and library manuals. Gradient descent is repeated small steps downhill on the loss. The learning rate, written eta, is the size of each step. '
                    'An epoch is one pass through all the training rows, and a mini-batch is a small group of rows used for a single step. Momentum is a running memory of past gradients. Adam is an optimiser published by Kingma and Ba in 2014. We use all five before the break.'),
        keep='Keep your saved notebook or workbook, and your four loss curves: learning rates 0.01, 0.05, 0.1 and 0.2. Write one sentence on what each curve shows.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Update rule', value='w = w - eta × gradient'), dict(label='Best of the four tried', value=f'eta = 0.1, loss {f3(R[0.1]["L"][-1])}'),
                                                              dict(label='Too large', value='eta = 0.2: loss grows'), dict(label='Next session', value='Backpropagation by hand')]),
        keep_title='Save your lab and keep the four loss curves',
        next='Session 11: backpropagation by hand, the gradient of a tiny network with every number written out.', next_label='Next session',
        keep_note=('Before you go, save your notebook or workbook with all four loss curves. Write one sentence for each learning rate on what its curve shows. '
                   'Next session we compute the gradient of a tiny network by hand, using the chain rule from Session 9, and then feed it into the update rule you learned today. If anything about the learning rate is still unclear, bring the question.'),
        cover_note=('Welcome to Session 10. Last time you learned the chain rule, which gives the gradient of the loss. Today we use that gradient. A model with billions of numbers cannot be solved with a formula, so it is trained by taking many small steps downhill. '
                    'That one idea, gradient descent, is how language models are trained. We will do the arithmetic by hand, then watch it run.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 9', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.6, 6.4], icons=False,
                  note='Check your answers. If one surprised you, look at Session 9 before the lab.',
                  notes=('Here are the short answers. For y equals three x plus one, all squared, the chain rule gives six times three x plus one. The outer derivative is two times the bracket, and the inner derivative is three. '
                         'A function with three inputs and two outputs has a Jacobian with two rows and three columns. And backpropagation uses the chain rule because a network is a function of functions, so the slope for an early weight is a product of local slopes. '
                         'Today we use those slopes. If you got all three, you are ready.')))

    S.append(dict(kind='idea', title='Training a model means walking downhill on the loss',
                  visual=dict(kind='d_loss_bowl'),
                  lead='The loss L measures how wrong the model is. Training lowers it.',
                  points=['The curve shows the loss for each value of one parameter w.', 'At the start the slope is negative, so the loss falls if w grows. We step that way.', 'The bottom of the curve is the best value of w.'],
                  notes=('Look at the curve. The horizontal axis is one parameter of the model, called w. The vertical axis is the loss, a single number for how wrong the model is. '
                         'We start at the gold dot on the left. There the slope is negative, which means the loss goes down if we increase w. So we take a step to the right, then measure the slope again, and step again. '
                         'The bottom of the bowl is the best w. This walk downhill is called gradient descent. Why do we need the slope to decide which way to go?')))

    S.append(dict(kind='formula', title='The update rule: new w equals old w minus the learning rate times the gradient',
                  formulas=[('One parameter', r'$w \leftarrow w - \eta \, \frac{dL}{dw}$'), ('Many parameters', r'$\mathbf{w} \leftarrow \mathbf{w} - \eta \, \nabla L(\mathbf{w})$')],
                  symbols=[['w', 'The parameter we improve. The arrow means: replace the old value. Bold w is the list of all the parameters.', 'start at w = 0'],
                           ['eta (learning rate)', 'The size of each step. Some books write alpha.', 'eta = 0.1'],
                           ['dL/dw', 'The slope of the loss with respect to w (a derivative).', f'{slope(0):.0f} at w = 0, for L = (w - 3)^2'],
                           ['nabla L', 'The gradient: all partial derivatives (Session 8).', 'one entry per parameter']],
                  size=20, note=f'Worked: w = 0 - 0.1 × ({slope(0):.0f}) = {bw[0.1][1]:.1f}. The minus sign sends w downhill.',
                  notes=('This is the update rule, the heart of training. The new w equals the old w minus eta times the slope of the loss. Eta is the learning rate, the size of each step. '
                         f'Try it on the bowl from the last slide, where the loss is w minus three, squared. At w equals zero the slope is minus six. So the new w is zero minus point one times minus six, which is {bw[0.1][1]:.1f}. '
                         'With many parameters we write the same thing with the gradient, the vector of partial derivatives from Session 8. Why is there a minus sign in front of eta?')))

    rows3 = [[str(k + 1), fmt(bw[0.1][k]), fmt(slope(bw[0.1][k])), fmt(bw[0.1][k + 1])] for k in range(5)]
    S.append(dict(kind='table', title='By hand: five steps of gradient descent on L(w) = (w - 3)^2 with eta = 0.1',
                  headers=['Step', 'w before', 'Slope 2(w - 3)', 'w after = w before - 0.1 × slope'], rows=rows3, widths=[1.4, 2.4, 3.2, 5.0], icons=False,
                  note='Each step closes one fifth of the remaining gap to 3. The best value is w = 3, where the slope is 0. These are illustrative numbers.',
                  notes=(f'Here are five steps by hand. Start at w equals zero. The slope is minus six, so the new w is {rows3[0][3]}. Next, the slope at {rows3[1][1]} is {rows3[1][2]}, so the new w is {rows3[1][3]}. '
                         f'Notice that the steps shrink: as w approaches three the slope gets smaller, so the step gets smaller without us doing anything. After five steps w is {rows3[4][3]}, close to the best value of three. '
                         'Take your calculator and check the third row yourself.')))

    S.append(dict(kind='formula', title='A line fit as a loss: the model, and the mean squared error',
                  formulas=[('Model', r'$\hat{y}_i = w\,x_i + b$'), ('Loss (MSE)', r'$L(w, b) = \frac{1}{n}\sum_{i=1}^{n}\left(\hat{y}_i - y_i\right)^2$')],
                  symbols=[['x_i', 'Centred distance of row i: distance minus the average 4.5 km. Distances are 1 to 8 km.', 'x = -3.5, -2.5, ..., 3.5'],
                           ['y_i, y-hat_i', 'Actual fare and predicted fare of row i, in thousand UGX.', 'illustrative fares 3.2 to 10.3'],
                           ['w, b', 'Slope (thousand UGX per km) and intercept (fare at the average distance).', 'both start at 0'],
                           ['n', 'The number of rows.', f'n = {n["n"]} trips']],
                  size=22, note=f'At w = 0 and b = 0 every prediction is 0, so the loss is the mean of y squared: {L0:.2f}.',
                  notes=(f'Now a real problem: fit a line to eight boda boda trips. The numbers are illustrative, made up to show the arithmetic. The input x is the trip distance minus the average of 4.5 kilometres, and y is the fare in thousand shillings. '
                         f'The model is y hat equals w times x plus b. The loss is the mean squared error: the average of the squared prediction errors. We start with w and b both zero, so every prediction is zero and the loss is the mean of y squared, which is {L0:.2f}. '
                         'Why do we subtract the average distance? We come back to that in the lab.')))

    S.append(dict(kind='formula', title='The gradient of the line-fit loss has one entry for w and one for b',
                  formulas=[('Gradient', r'$\frac{\partial L}{\partial w} = \frac{2}{n}\sum_{i=1}^{n}(\hat{y}_i - y_i)\,x_i \qquad \frac{\partial L}{\partial b} = \frac{2}{n}\sum_{i=1}^{n}(\hat{y}_i - y_i)$')],
                  symbols=[['dL/dw', 'How fast the loss changes when w changes (a partial derivative).', f'{f3(n["dw0"])} at w = 0, b = 0'],
                           ['dL/db', 'How fast the loss changes when b changes.', f'{f3(n["db0"])} at w = 0, b = 0'],
                           ['(y-hat_i - y_i)', 'The prediction error of row i. Positive means too high.', 'at w = 0, b = 0 it is -y_i'],
                           ['sum and 2/n', 'Add over all rows, then multiply by 2/n (twice the average).', f'2/{n["n"]} = 0.25; sum = {-n["sum_xy"]:.2f}']],
                  size=20, note='Both slopes are negative here, so the update raises both w and b.',
                  notes=('The gradient has two entries, one for each parameter. Both come from the chain rule you learned last time. The outer function is the square, whose derivative is two times the error. '
                         'The inner function is w times x plus b, whose derivative with respect to w is x, and with respect to b is one. So the slope for w is two over n times the sum of error times x, and the slope for b is two over n times the sum of the errors. '
                         f'At our start, the values are {f3(n["dw0"])} and {f3(n["db0"])}. What does a negative slope tell us to do with w and b?')))

    rows_h = [[str(i + 1), f'{xc[i]:+.1f}', f'{y[i]:.1f}', f'{-y[i]:.1f}', f'{-y[i] * xc[i]:.2f}'] for i in range(8)]
    S.append(dict(kind='table', title='Step 1 of the line fit by hand, starting from w = 0 and b = 0',
                  headers=['Row i', 'x (km)', 'y (thousand UGX)', 'Error y-hat - y', 'Error times x'], rows=rows_h, widths=[1.3, 1.6, 2.9, 2.6, 2.4], icons=False,
                  note=(f'Sums: error times x = {-n["sum_xy"]:.2f}, error = {-y.sum():.1f}. dL/dw = 0.25 × ({-n["sum_xy"]:.2f}) = {f3(n["dw0"])}, dL/db = 0.25 × ({-y.sum():.1f}) = {f3(n["db0"])}. '
                        f'With eta = 0.1: w = {f4(n["w1"])}, b = {f4(n["b1"])}.'),
                  notes=(f'Here is step one with every number written out. With w and b at zero, each prediction is zero, so the error is simply minus y. The last column multiplies each error by x. The sums are in the note. '
                         f'The slope for w is two over eight, that is point two five, times {-n["sum_xy"]:.2f}, which gives {f3(n["dw0"])}. The slope for b is point two five times {-y.sum():.1f}, which gives {f3(n["db0"])}. '
                         f'With eta equal to point one, the new w is {f4(n["w1"])} and the new b is {f4(n["b1"])}. This is exactly the first row of the spreadsheet lab.')))

    S.append(dict(kind='wide', title='The learning rate sets the size of each step: too small crawls, good arrives, too large overshoots',
                  visual=dict(kind='d_gd_rates', panels=[dict(title='Too small: eta = 0.01', path=bw[0.01][:6], note='Tiny steps, very slow'),
                                                         dict(title='Good: eta = 0.1', path=bw[0.1][:6], note='Steps shrink as the slope shrinks'),
                                                         dict(title='Too large: eta = 1.1', path=bw[1.1][:4], note='Each step overshoots further')]),
                  caption='Each panel: L(w) = (w - 3)^2, starting at w = 0. Dots are w after each step; arrows are the steps.',
                  notes=('The learning rate is the one setting you must get right. On the left, eta is point zero one: every step is tiny, and after five steps we have barely moved. '
                         'In the middle, eta is point one: the steps start big and shrink as the slope flattens, so we arrive at the bottom. '
                         'On the right, eta is one point one: the step is so large that we jump past the bottom and land higher up the other side. The next jump is bigger again. The loss grows instead of falling. Which panel would you find hardest to spot in a real training run?')))

    lr_rows = [[str(k), fmt(bw[0.01][k]), fmt(bw[0.1][k]), fmt(bw[1.1][k])] for k in range(6)]
    lr_rows.append(['Loss (w - 3)^2 at step 5', fmt((bw[0.01][5] - 3) ** 2), fmt((bw[0.1][5] - 3) ** 2), fmt((bw[1.1][5] - 3) ** 2)])
    S.append(dict(kind='table', title='The same three learning rates as numbers: w after each step',
                  headers=['Step', 'eta = 0.01 (too small)', 'eta = 0.1 (good)', 'eta = 1.1 (too large)'], rows=lr_rows, widths=[3.3, 2.9, 2.7, 3.0], icons=False,
                  note='The loss at step 0 is 9 in all three columns. With eta = 1.0 exactly, w would bounce between 0 and 6 forever.',
                  notes=(f'The numbers behind the picture. With eta point zero one, w creeps from zero to {fmt(bw[0.01][5])} in five steps, and the loss is still {fmt((bw[0.01][5] - 3) ** 2)}. '
                         f'With eta point one, w reaches {fmt(bw[0.1][5])} and the loss is {fmt((bw[0.1][5] - 3) ** 2)}. '
                         f'With eta one point one, w goes to {fmt(bw[1.1][1])}, then {fmt(bw[1.1][2])}, then {fmt(bw[1.1][3])}. It swings further from three every time, and the loss grows to {fmt((bw[1.1][5] - 3) ** 2)}. '
                         'The rule of thumb: if the loss goes up, the learning rate is too large.')))

    S.append(dict(kind='wide', title='Batch, stochastic and mini-batch gradient descent use different numbers of rows for each step',
                  visual=dict(kind='d_batches'),
                  caption='Gold squares are the rows used for one gradient. An epoch is one pass through all 8 rows.',
                  notes=('So far every gradient used all eight rows. That is called batch gradient descent. With millions of rows it is slow, because one step needs a pass over everything. '
                         'Stochastic gradient descent, SGD, uses a single row per step. Each step is cheap, but the path is noisy, because one row is a poor guide. '
                         'The compromise is the mini-batch: a small group of rows, here four. This is what almost everyone uses. One pass through all the rows is an epoch. Why does the noisy path still arrive near the bottom on average?')))

    S.append(dict(kind='table', title='Three ways to choose the rows for each step',
                  headers=['Method', 'Rows per step', 'Steps per epoch (n = 8)', 'What to expect'],
                  rows=[['Batch gradient descent', 'All n rows', '1', 'Smooth path, but one step costs a pass over all the data'],
                        ['Stochastic gradient descent (SGD)', '1 row', '8', 'Cheap steps, a noisy path'],
                        ['Mini-batch gradient descent', 'A small group, for example 4', '2', 'Less noise than SGD, and fast on modern hardware']],
                  widths=[3.5, 2.7, 2.4, 4.2], icons=['folder', 'pin', 'grid'],
                  note='In everyday speech, "SGD" often means the mini-batch version. The gradient of a mini-batch is an estimate of the gradient of all the rows.',
                  notes=('Here is the same comparison as a table. Batch uses all n rows and takes one step per epoch. SGD takes one row per step, so eight steps per epoch with our eight rows. '
                         'A mini-batch of four gives two steps per epoch. A warning about words: when people say SGD in a library, they usually mean mini-batch gradient descent. '
                         'The mini-batch gradient is an estimate of the full gradient. It is noisy, but it is cheap, and it works well in practice. How many steps per epoch would a batch size of two give us?')))

    S.append(dict(kind='wide', title='Momentum keeps a running memory of past gradients, which smooths a zigzag path',
                  visual=dict(kind='d_momentum'),
                  caption='Same valley, same start. Momentum damps the sideways swings that make plain descent zigzag.',
                  notes=('Here the loss is a long narrow valley. The gradient points mostly across the valley, not along it, so plain gradient descent zigzags and makes slow progress along the floor. '
                         'Momentum adds a memory. Sideways gradients point one way, then the other, so they largely cancel in the memory. Gradients along the valley all point the same way, so they add up. '
                         'The result on the right is a smoother, faster path. Think of a ball rolling down: it carries speed from earlier steps.')))

    mom = n['mom']
    S.append(dict(kind='formula', title='Momentum: the velocity is a decaying sum of past gradients',
                  formulas=[('Velocity', r'$u_t = \beta\, u_{t-1} + g_t$'), ('Update', r'$w \leftarrow w - \eta\, u_t$')],
                  symbols=[['g_t', 'The gradient at step t.', 'illustrative: g = 2 at every step'],
                           ['u_t', 'The velocity: a running total of past gradients, each older one counted less. It starts at 0. (Not the same as Adam\'s v on the next slides.)', f'u = {mom[0]:.0f}, {mom[1]:.1f}, {mom[2]:.2f}'],
                           ['beta', 'The momentum coefficient, between 0 and 1. A common choice is 0.9.', 'beta = 0.9'],
                           ['eta', 'The learning rate.', 'as before']],
                  size=26, note=f'Steady gradient 2: u = 2, then 0.9 × 2 + 2 = {mom[1]:.1f}, then 0.9 × {mom[1]:.1f} + 2 = {mom[2]:.2f}. It grows towards 20.',
                  notes=('This is the momentum update, in the form used by common libraries. The velocity, written u, is beta times the old velocity plus the new gradient. The weight then moves by eta times u. We use the letter u so it is not confused with the v of Adam, which comes next. '
                         f'Take a gradient that stays at two. The first u is two. The second is point nine times two plus two, which is {mom[1]:.1f}. The third is point nine times {mom[1]:.1f} plus two, which is {mom[2]:.2f}. '
                         'The velocity keeps growing while the gradient keeps its sign, up to ten times the gradient when beta is point nine. If the gradient flips sign, the velocity shrinks. Which situation does that rescue us from?')))

    S.append(dict(kind='formula', title='Adam, part 1: two running averages and a correction for the start (Kingma and Ba, 2014)',
                  formulas=[('Average gradient', r'$m_t = \beta_1 m_{t-1} + (1-\beta_1)\,g_t$'), ('Average squared gradient', r'$v_t = \beta_2 v_{t-1} + (1-\beta_2)\,g_t^2$'),
                            ('Correction', r'$\hat{m}_t = \frac{m_t}{1-\beta_1^{\,t}} \qquad \hat{v}_t = \frac{v_t}{1-\beta_2^{\,t}}$')],
                  symbols=[['m_t', 'A running average of the gradients, like momentum. Starts at 0.', 'beta1 = 0.9'],
                           ['v_t', 'A running average of the squared gradients. Starts at 0.', 'beta2 = 0.999'],
                           ['g_t', 'The gradient at step t. Squaring is done entry by entry.', 'from L = (w - 3)^2'],
                           ['t', 'The step number, starting at 1.', 't = 1, 2, 3'],
                           ['m-hat, v-hat', 'The corrected averages. Without the correction both would be too small in the first steps, because they start at 0.', 'used in the update']],
                  size=20, widths=[1.9, 6.4, 3.6],
                  notes=('Adam, published by Kingma and Ba in 2014, keeps two running averages for each parameter. The first, m, is an average of the gradients, which works like momentum. '
                         'The second, v, is an average of the squared gradients, which measures how large the gradients typically are. '
                         'Both start at zero, so in the first steps they are too small. The correction divides by one minus beta to the power t, which fixes that. At step one it exactly undoes the shrinkage. Why do we square the gradient for v?')))

    S.append(dict(kind='formula', title='Adam, part 2: each parameter takes a step of about the learning rate, whatever its gradient size',
                  formulas=[('Update', r'$w \leftarrow w - \alpha\,\frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon}$')],
                  symbols=[['alpha', 'The step size of Adam (the learning rate; the paper uses alpha).', 'alpha = 0.1 here; the paper suggests 0.001'],
                           ['m-hat / sqrt(v-hat)', 'The average gradient divided by the typical gradient size. It is near +1 or -1 when the gradient is steady.', 'about -1 in the example'],
                           ['epsilon', 'A tiny number that avoids dividing by zero.', '1e-8 (the paper default)'],
                           ['beta1, beta2', 'Defaults suggested in the paper.', '0.9 and 0.999']],
                  size=26, note='Dividing by the typical gradient size gives every parameter a step of similar size.',
                  notes=('Now the update. The step is alpha times the corrected average gradient, divided by the square root of the corrected average squared gradient, plus a tiny epsilon. '
                         'When the gradient is steady, the top and bottom are almost equal in size, so the ratio is about plus or minus one and the step is about alpha. '
                         'A parameter with huge gradients and a parameter with tiny gradients both move by about alpha. That is why Adam is popular for models whose parameters have very different gradient sizes. The defaults from the paper are beta one point nine, beta two point nine nine nine, epsilon ten to the minus eight.')))

    arows = [[str(r['t']), f4(r['g']), f4(r['m']), f4(r['v']), f4(r['mh']), f4(r['sq']), f4(r['step']), f4(r['w_after'])] for r in ad]
    S.append(dict(kind='table', title='Adam by hand: three steps on L(w) = (w - 3)^2, starting at w = 0',
                  headers=['t', 'g', 'm', 'v', 'm-hat', 'sqrt(v-hat)', 'Step', 'w after'], rows=arows, widths=[0.7, 1.5, 1.5, 1.5, 1.5, 1.7, 1.5, 1.6], icons=False,
                  note='alpha = 0.1, beta1 = 0.9, beta2 = 0.999, epsilon = 1e-8. Step = alpha × m-hat / (sqrt(v-hat) + epsilon). Illustrative numbers.',
                  notes=(f'Three Adam steps with real numbers. At step one the gradient is minus six. The average m is point one times minus six, which is {f4(ad[0]["m"])}. The average v is point zero zero one times thirty-six, which is {f4(ad[0]["v"])}. '
                         f'After the correction, m hat is minus six and the square root of v hat is six, so the step is alpha times minus one: w moves by {f4(-ad[0]["step"])} to {f4(ad[0]["w_after"])}. '
                         f'At step two the gradient is {f4(ad[1]["g"])} and the step is again almost exactly alpha. By step three w is {f4(ad[2]["w_after"])}. Notice the steps do not shrink with the slope. Check one cell on your calculator.')))

    S.append(dict(kind='wide', title='Convexity in plain words: a convex loss has one bottom, while other losses have several dips',
                  visual=dict(kind='d_convex'),
                  caption='Left: a convex loss, one bowl. Right: several dips. A local minimum is a dip that is not the lowest.',
                  notes=('Convexity tells us how safe gradient descent is. A convex loss, on the left, is a single bowl. From any start, walking downhill reaches the one bottom. The mean squared error of a line fit is convex. '
                         'On the right is a loss with several dips. A dip that is lower than its neighbours but not the lowest is a local minimum. Gradient descent can stop there, depending on where it started. '
                         'The loss of a neural network is not convex. Even so, published experience is that large networks usually train well with the methods in this session, though we cannot prove that from this picture.')))

    S.append(dict(kind='idea', title='A learning-rate schedule changes eta during training',
                  visual=dict(kind='d_schedule'),
                  lead='A schedule gives a different learning rate at each step.',
                  points=['Constant: the same eta all the time.', 'Step decay: cut eta at fixed steps.', 'Warm-up then cosine decay: rise slowly, then fall smoothly.'],
                  notes=('A learning-rate schedule changes eta as training goes on. The grey dashed line is a constant rate. The grey solid line cuts the rate in steps. '
                         'The red line is warm-up followed by cosine decay. In warm-up the rate rises from zero to its peak over the first steps, because the first gradients can be unreliable. '
                         'Then it falls smoothly, so the late steps are small and settle into a minimum. Why would large steps help early and hurt late?')))

    sched = lambda t: (0.001 * t / 100) if t < 100 else 0.001 * 0.5 * (1 + math.cos(math.pi * (t - 100) / 900))
    S.append(dict(kind='formula', title='Warm-up followed by cosine decay, with illustrative numbers',
                  formulas=[('Warm-up, t < T_w', r'$\eta_t = \eta_{max}\,\frac{t}{T_w}$'), ('Decay, t >= T_w', r'$\eta_t = \frac{\eta_{max}}{2}\left(1 + \cos\!\left(\pi\,\frac{t - T_w}{T - T_w}\right)\right)$')],
                  symbols=[['eta_max', 'The peak learning rate.', '0.001 (illustrative)'],
                           ['T_w, T', 'The number of warm-up steps and of all steps.', 'T_w = 100, T = 1000'],
                           ['t', 'The current step.', f't = 50: eta = {sched(50):.4f}'],
                           ['More steps', 'The same schedule at other steps.', f't = 100: {sched(100):.4f}. t = 550: {sched(550):.4f}. t = 1000: {sched(1000):.4f}']],
                  size=20, widths=[1.8, 5.4, 4.7],
                  notes=(f'Here is the schedule in the figure as two formulas. During warm-up the rate grows in a straight line from zero to eta max. With eta max point zero zero one and a hundred warm-up steps, step fifty has rate {sched(50):.4f}. '
                         f'After warm-up the rate follows half a cosine wave down to zero. At step five hundred and fifty, halfway through the decay, the rate is exactly half the peak, {sched(550):.4f}. At the last step it is {sched(1000):.4f}. '
                         'These numbers are illustrative. The original transformer paper, Vaswani and colleagues in 2017, also used Adam with a warm-up of four thousand steps.')))

    S.append(dict(kind='table', title='Four mistakes with gradient descent, what you see, and the fix',
                  headers=['Mistake', 'What you see', 'Fix'],
                  rows=[['Learning rate too large', 'The loss goes up, or becomes nan (not a number)', 'Divide eta by 3 or 10 and run again'],
                        ['Learning rate too small', 'The loss falls, but so slowly that it looks flat', 'Multiply eta by 3 or 10, or train for more steps'],
                        ['Wrong sign in the update', 'The loss climbs from the first step', 'Use w - eta × gradient, with the minus sign'],
                        ['Inputs on very different scales', 'One learning rate is too large for one parameter and too small for another', 'Centre and scale the inputs, as the lab does']],
                  widths=[3.3, 4.4, 4.2], icons=['cross', 'clock', 'flag', 'key'],
                  notes=('Four mistakes to watch for. Learning rate too large: the loss goes up or turns into nan, which means not a number. Divide eta by three or ten. '
                         'Learning rate too small: the loss falls, but so slowly it looks flat. Increase eta or run longer. A wrong sign: if you add the gradient instead of subtracting it, you walk uphill, and the loss climbs from step one. '
                         'And inputs on very different scales make one learning rate wrong for some parameter, which is why the lab subtracts the average distance. Which of these have you already seen in your own work?')))

    S.append(dict(kind='compare', title='Momentum and Adam both smooth the steps, but Adam also rescales them',
                  left=dict(head='SGD with momentum', icon='gear', points=['One learning rate eta for all parameters', 'Remembers past gradients', 'Needs eta tuned with care']),
                  right=dict(head='Adam', icon='robot', points=['A separate effective step for each parameter', 'Remembers past gradients and their typical size', 'Works with the default settings in many cases']),
                  verdict='Both are optimisers: rules that turn a gradient into a step.',
                  notes=('Two optimisers side by side. SGD with momentum uses one learning rate for all parameters and remembers past gradients. Adam also remembers the typical size of each parameter gradient, and uses it to rescale the step for that parameter. '
                         'That makes Adam forgiving: the default settings often work. An optimiser is just a rule that turns the gradient into a step, and plain gradient descent is the simplest one. '
                         'Which would you try first on a new problem, and why?')))

    S.append(dict(kind='code', title='Read the loop before you write it: gradient, then update, repeated',
                  code='for step in range(30):\n    err = w * xc + b - y\n    dw = 2 * np.mean(err * xc)\n    db = 2 * np.mean(err)\n    w = w - eta * dw\n    b = b - eta * db',
                  reads=['err holds the error y-hat - y of every row.', 'dw and db are the two slopes of the loss: the gradient.', 'The last two lines are the update rule.', 'The loop repeats it 30 times. xc is the centred distance.'],
                  notes=('Before the lab, read the whole algorithm. This is gradient descent in six lines. The loop runs thirty steps. Inside, the first line computes the error for every row. '
                         'The next two lines are the two slopes from the formulas, written with numpy means. The last two lines are the update rule, once for w and once for b. '
                         'In the lab you will wrap this loop in a function, call it for four learning rates, and plot the loss. In the spreadsheet, each pass through the loop becomes one row.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the concepts. Please close the slides and open either the Python notebook or the spreadsheet workbook. Both use the same eight trips and the same numbers, so you can compare answers with someone on the other track. '
                         'In every step, write your prediction first, then run, then read, then change one thing. Raise your hand when a check says not yet.')))

    S.append(dict(kind='steps', title='The lab in five stages, in Python and in the spreadsheet',
                  steps=[dict(head='1 Look', text='Load the 8 trips and centre the distance', icon='folder'), dict(head='2 Gradient', text='Loss and two slopes at w = 0, b = 0', icon='calculator'),
                         dict(head='3 One step', text='Apply the update rule once', icon='pin'), dict(head='4 Loop', text='30 steps; one row per step in the sheet', icon='gear'), dict(head='5 Compare', text='Four learning rates, four loss curves', icon='chart')], highlight=3,
                  caption='Predict first, run, read the output, then change one thing. The check cells tell you when a number is right.',
                  notes=('Here is the lab in five stages. One, look at the eight trips and subtract the average distance. Two, compute the loss and the two slopes at w and b equal to zero. Three, apply the update rule once. '
                         'Four, run thirty steps: in Python with a loop, in the spreadsheet with one row for each step. Five, repeat with four learning rates and compare the loss curves. '
                         'Predicting before you run is how you find out what you understand, so please do not skip the predict boxes.')))

    S.append(dict(kind='table', title='Check your numbers against these before you move on',
                  headers=['What you compute', 'You should see'],
                  rows=[['Loss at w = 0, b = 0', f2(L0)], ['dL/dw and dL/db at w = 0, b = 0', f'{f3(n["dw0"])} and {f3(n["db0"])}'], ['w and b after one step with eta = 0.1', f'{f4(n["w1"])} and {f4(n["b1"])}'],
                        ['Loss after 30 steps, eta = 0.1', f4(R[0.1]['L'][-1])], ['Loss after 30 steps, eta = 0.01', f3(R[0.01]['L'][-1])], ['Loss after 30 steps, eta = 0.2', f'{R[0.2]["L"][-1]:.1f} (it grew)'],
                        ['Best line from least squares (Session 4)', f'w = {f3(n["w_star"])}, b = {f3(n["b_star"])}']],
                  widths=[7.2, 4.4], icons=['chart', 'calculator', 'pin', 'check', 'clock', 'cross', 'flag'],
                  note='If your number differs, find the step that went wrong. Do not change a number to match.',
                  notes=('Use this table as your checkpoint. If your numbers match, carry on. If one does not, stop and look for the step that went wrong, because every later step builds on it. '
                         f'Notice that with eta point one, the loss after thirty steps is {f4(R[0.1]["L"][-1])}, very close to the least squares answer from Session 4, and the weights approach {f3(n["w_star"])} and {f3(n["b_star"])}. '
                         'With eta point two the loss has grown, so that curve is the one that goes up.')))

    S.append(dict(kind='table', title='Errors you will meet in the lab, what they mean and what to do',
                  headers=['What you see', 'What it means', 'What to do'],
                  rows=[['The loss is nan or inf', 'The learning rate is too large and the numbers overflowed', 'Divide eta by 10'],
                        ['NameError in Python', 'A cell that defines a name was not run', 'Run all cells from the top'],
                        ['A flat loss curve', 'The learning rate is too small, or the loop did not update w', 'Check that w = w - eta * dw is inside the loop'],
                        ['Sheet formula shows #REF! or 0', 'A row refers to the wrong previous row', 'Compare with the row above: step t uses row t - 1']],
                  widths=[3.3, 4.6, 4.0], icons=['cross', 'bell', 'clock', 'key'],
                  notes=('Four things you may meet. A loss of nan or inf means the learning rate is too large and the numbers blew up, so divide eta by ten. A name error means you skipped a cell, so run all cells from the top. '
                         'A flat curve means eta is too small or the update is outside the loop. And in the sheet, a reference error or a zero usually means a row points at the wrong previous row. Read the last line of any message first. It often tells you the answer.')))

    S.append(dict(kind='idea', title='Where this appears in AI: every training step ends with an optimiser update',
                  visual=dict(kind='d_loop', items=['Take a batch of text', 'Forward pass: predict the next token', 'Loss: cross-entropy', 'Backward pass: the gradient', 'Optimiser update (Adam type)'], center='one training step'),
                  lead='Training is one loop, repeated a very large number of times.',
                  points=['Published work trains language models with Adam and a learning-rate warm-up.', 'The 2017 transformer paper used 4000 warm-up steps.', 'The settings of ChatGPT, Gemini and Claude are not published.'],
                  notes=('Here is where today appears. Language models of this kind are trained by a loop. Take a batch of text, run the model forward to predict each next token, measure the loss, run backward to get the gradient, and apply an optimiser update. '
                         'Published research describes Adam and related optimisers and a learning-rate schedule with warm-up, like the one on the schedule slide. The original transformer paper, in 2017, used Adam with four thousand warm-up steps. '
                         'The makers of ChatGPT, Gemini and Claude have not published their exact settings, so we use the open literature. What in this loop did you meet today?')))

    S.append(dict(kind='practice', title='Check an AI assistant with your own numbers', minutes=10, label='Hands-on, with no private data',
                  task='Ask any AI assistant to do three Adam steps. Then compare with the table.',
                  steps=['Type: "For L(w) = (w - 3)^2, start w = 0, alpha = 0.1, beta1 = 0.9, beta2 = 0.999. Show m, v and w for three Adam steps."',
                         f'Compare its w after step 3 with the table: {f4(ad[2]["w_after"])}.', 'If it differs, find the first number that differs.', 'Never paste confidential data.'],
                  output='A note: did the assistant match your table?',
                  notes=('A hands-on check. Ask any assistant to carry out three Adam steps with exactly the numbers on the slide. Then compare its answer with your table, row by row. '
                         f'The w after step three should be {f4(ad[2]["w_after"])}. Assistants sometimes make arithmetic slips, so find the first number that differs and work out which formula it applied wrongly. '
                         'This is a good habit: use the assistant to explain, and use your own calculation to check. Please never paste confidential data into an assistant. Did the assistant match you?')))

    S.append(dict(kind='table', title='Exit check: three questions with short answers',
                  headers=['Question', 'Short answer'],
                  rows=[['With eta = 0.1 and a slope of -4, what is the new w if the old w is 1?', 'w = 1 - 0.1 × (-4) = 1.4.'],
                        ['The loss grows at every step. What is the most likely cause and the fix?', 'The learning rate is too large. Divide it by 3 or 10.'],
                        ['Give one difference between SGD and Adam.', 'SGD uses one learning rate for all parameters. Adam rescales the step for each parameter using the typical size of its gradient.']],
                  widths=[5.8, 6.2], icons=False,
                  notes=('Three questions to finish. First, with a learning rate of point one and a slope of minus four, the new w from an old w of one is one minus point one times minus four, which is one point four. '
                         'Second, if the loss grows at every step, the learning rate is almost certainly too large, so divide it by three or ten. '
                         'Third, SGD uses a single learning rate for every parameter, while Adam rescales the step for each parameter using the typical size of its gradient. Write your own answers first, then compare.')))

    s['facilitator'] = dict(
        prep=['Open the notebook in Colab and the workbook in Excel or Google Sheets before the class, and run both once.',
              'Write the four numbers eta = 0.01, 0.05, 0.1, 0.2 on the board. Learners predict which curve falls fastest and which one grows.',
              'Check the by-hand table on the slide "Step 1 of the line fit" with a calculator; the first row of the sheet must match it.'],
        misconceptions=[('A bigger learning rate always trains faster', 'Only up to a limit. Above it the loss grows. Here the limit is about 0.19.'),
                        ('Gradient descent always finds the best answer', 'Only for a convex loss. A neural network loss has many dips.'),
                        ('SGD means one row at a time', 'In libraries it usually means mini-batch gradient descent.'),
                        ('Adam does not need a learning rate', 'It still has alpha, and a schedule is still used in published training.')],
        probes=[('What happens to the step size as w approaches the bottom of a bowl?', 'The slope shrinks, so the step shrinks even with a fixed learning rate.'),
                ('Why subtract the average distance before running gradient descent?', 'It makes the loss bowl round, so one learning rate suits both w and b. Without it the loop is slow or unstable.'),
                ('Why does Adam correct m and v?', 'They start at 0, so early values are too small. The correction divides by 1 minus beta to the power t.'),
                ('Is the learning rate learned by gradient descent?', 'No. It is a hyperparameter chosen before training, or given by a schedule.')],
        lab_steps=[('Python: look and centre (steps 1 to 2)', 'Eight trips, x centred, mean distance 4.5. Loss at zero is 52.11. Spreadsheet: the Data sheet shows the same.'),
                   ('Python: gradient and one step (steps 3 to 4)', f'Slopes {f3(n["dw0"])} and {f3(n["db0"])}. After one step w = {f4(n["w1"])} and b = {f4(n["b1"])}. Spreadsheet: gold cells in row 0 and row 1.'),
                   ('Python: loop and four rates (steps 5 to 6)', 'The curve for 0.2 climbs; the curve for 0.01 is still high at step 30; 0.1 reaches the minimum.'),
                   ('Spreadsheet: one row per step', 'Row 0 holds w = 0, b = 0. Each next row applies the update rule to the row above. The loss column falls for eta = 0.1.'),
                   ('Spreadsheet: change eta', 'Changing the eta cell redraws everything. At 0.2 the loss column grows.')],
        rescue=['If the concepts overrun, skip the momentum formula slide and say: momentum is a running memory of gradients.', 'If the sheet confuses a learner, do the Python loop on the projector and map each line to a sheet column.',
                'If only 20 minutes remain for the lab, run steps 1 to 4 and the single learning rate 0.1.'],
        after=['Share the solution notebook with absent learners.', 'Ask learners to bring one question about backpropagation.'],
        lab_answer_key=[['PREDICT: which learning rate gives the fastest fall?', 'Among 0.01, 0.05 and 0.1 the largest, 0.1. The value 0.2 is too large.'], ['READ: what does the 0.2 curve do?', 'It rises. The step overshoots by more each time.'],
                        ['CHANGE: use 0.19', 'The loss neither falls nor grows quickly: it is near the stability limit of about 0.19.'], ['CHANGE: do not centre x', 'The loop becomes slow for b or unstable unless eta is much smaller.']])
    return s
