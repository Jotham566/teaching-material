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
    F = n['forms']

    def fmt(v):
        return f'{v:.3f}'.rstrip('0').rstrip('.')

    def slope(w):
        return 2 * (w - 3)

    sched = lambda t: (0.001 * t / 100) if t < 100 else 0.001 * 0.5 * (1 + math.cos(math.pi * (t - 100) / 900))

    s = dict(
        num=10, block='Calculus and optimisation', short_title='Gradient descent',
        title='Gradient descent: training is walking downhill on the loss, one step at a time',
        question='How does a model with millions or billions of numbers find good values for all of them?',
        outcomes=['Apply the update rule w = w - eta times the gradient by hand, for one step and for several steps',
                  'Explain what happens when the learning rate is too small or too large, and what mini-batches, momentum and Adam change',
                  'Write the gradient descent loop for a line fit in Python, or one row per step in a spreadsheet, and compare four learning rates'],
        outcome_icons=['calculator', 'chart', 'gear'],
        outcome_note=('By the end of today you can do three things. First, apply the update rule by hand: the new w equals the old w minus the learning rate times the gradient. '
                      'Second, say what goes wrong when the learning rate is too small or too large, and what mini-batches, momentum and Adam change. '
                      'Third, write the loop yourself for a line fit, in Python or as one spreadsheet row per step, and compare the loss curves for four learning rates.'),
        clock=[(10, 'Recall and a real question from AI'), (35, 'Concept: a picture, then a hand example'), (10, 'Break'),
               (45, 'Lab: Python or spreadsheet, predict, run, change'), (15, 'Where it appears in AI, plus an exit check'), (5, 'Save the work')],
        plan_title='Your two hours: learn the update rule, then watch it run',
        plan_caption='Pictures and hand calculations first. Then the lab: a loop in Python or one row per step.',
        plan_note=('We have two hours. The first ten minutes recall the chain rule from Session 9 and ask the question of the day. Then thirty-five minutes of concepts, with no laptop: the update rule, the learning rate, batches, momentum and Adam. '
                   'After a break comes the lab, forty-five minutes, where you write gradient descent yourself for a line fit. The last fifteen minutes show where it appears in ChatGPT, Gemini, Claude and other AI, then an exit check.'),
        recall_from='Session 9',
        recall=[('Use the chain rule: what is the derivative of y = (3x plus 1) squared with respect to x?', 'It is 6(3x + 1): the outer derivative 2(3x + 1) multiplied by the inner derivative 3.'),
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
                  notes=('For y equals three x plus one, all squared, the chain rule gives six times three x plus one. The outer derivative is two times the bracket, and the inner derivative is three. '
                         'A function with three inputs and two outputs has a Jacobian with two rows and three columns. And backpropagation uses the chain rule because a network is a function of functions, so the slope for an early weight is a product of local slopes. '
                         'Today those slopes finally get used. If you got all three, you are ready.')))

    S.append(dict(kind='idea', title='Training a model means walking downhill on the loss',
                  visual=dict(kind='d_loss_bowl'),
                  lead='The loss L measures how wrong the model is. Training lowers it.',
                  points=['The curve shows the loss for each value of one parameter w.', 'At the start the slope is negative, so the loss falls if w grows. We step that way.', 'The bottom of the curve is the best value of w.'],
                  notes=('Look at the curve. The horizontal axis is one parameter of the model, called w. The vertical axis is the loss, a single number for how wrong the model is. '
                         'We start at the gold dot on the left. There the slope is negative, which means the loss goes down if we increase w. So we take a step to the right, then measure the slope again, and step again. '
                         'The bottom of the bowl is the best w. This walk downhill is called gradient descent. Why do we need the slope to decide which way to go?')))

    S.append(dict(kind='formula', title='The update rule: new w equals old w minus the learning rate times the gradient',
                  formulas=[('One parameter', r'$w \leftarrow w - \eta \, \frac{dL}{dw}$'), ('Many parameters', r'$\mathbf{w} \leftarrow \mathbf{w} - \eta \, \nabla L(\mathbf{w})$')],
                  symbols=[['w', 'The parameter we improve. The arrow means: replace the old value. Bold w is the column of all the parameters (Session 8 also calls it theta).', 'start at w = 0'],
                           ['eta (learning rate)', 'The size of each step. Some books write alpha.', 'eta = 0.1'],
                           ['dL/dw', 'The slope of the loss with respect to w (a derivative).', f'{slope(0):.0f} at w = 0, for L = (w - 3)^2'],
                           ['nabla L', 'The gradient: the column of all partial derivatives (Session 8).', 'one entry per parameter']],
                  size=20, note=f'Worked: w = 0 - 0.1 × ({slope(0):.0f}) = {bw[0.1][1]:.1f}. The minus sign moves w the way that lowers the loss.',
                  notes=('This one line is what every training run repeats. The new w equals the old w minus eta times the slope of the loss. Eta is the learning rate, the size of each step. '
                         f'Try it on the bowl from the last slide, where the loss is w minus three, squared. At w equals zero the slope is minus six. So the new w is zero minus point one times minus six, which is {bw[0.1][1]:.1f}. '
                         'With many parameters we write the same thing with the gradient, the column of partial derivatives from Session 8. The minus sign matters: the slope points uphill, so we step the other way.')))

    rows3 = [[str(k + 1), fmt(bw[0.1][k]), fmt(slope(bw[0.1][k])), fmt(bw[0.1][k + 1])] for k in range(5)]
    S.append(dict(kind='table', title='Five steps by hand on the bowl (w minus 3) squared with eta = 0.1: the steps shrink by themselves',
                  headers=['Step', 'w before', 'Slope 2(w minus 3)', 'w after = w before minus 0.1 × slope'], rows=rows3, widths=[1.4, 2.4, 3.2, 5.0], icons=False,
                  note='Each step closes one fifth of the remaining gap to 3. The best value is w = 3, where the slope is 0.',
                  notes=(f'Five steps by hand. Start at w equals zero. The slope is minus six, so the new w is {rows3[0][3]}. Next, the slope at {rows3[1][1]} is {rows3[1][2]}, so the new w is {rows3[1][3]}. '
                         f'The steps shrink: as w approaches three the slope gets smaller, so the step gets smaller without us changing anything. After five steps w is {rows3[4][3]}, close to the best value of three. '
                         'Each step closes one fifth of the remaining gap, because point one times two is one fifth. Take your calculator and check the third row yourself.')))

    S.append(dict(kind='formula', title='A line fit becomes a loss: a straight-line model and its mean squared error',
                  formulas=[('Model', r'$\hat{y}_i = b + w\,x_i$'), ('Loss (MSE)', r'$L(w, b) = \frac{1}{n}\sum_{i=1}^{n}\left(\hat{y}_i - y_i\right)^2$')],
                  symbols=[['x_i', 'Centred distance of row i: distance minus the average 4.5 km.', 'x = -3.5, -2.5, ..., 3.5'],
                           ['y_i, y-hat_i', 'Actual fare and predicted fare of row i, in thousand UGX.', 'illustrative fares 3.2 to 10.3'],
                           ['b, w', 'Intercept (the fare at the average distance) and slope (thousand UGX per km).', 'both start at 0'],
                           ['n', 'The number of rows.', f'n = {n["n"]} trips']],
                  size=22, note=f'Start: the loss is the mean of y squared, {L0:.2f}. Centred x adds up to 0, so ∂L/∂w does not involve b.',
                  notes=(f'A real problem: fit a line to eight boda boda trips. The numbers are illustrative, made up to show the arithmetic. The input x is the trip distance minus the average of 4.5 kilometres, and y is the fare in thousand shillings. '
                         f'The model is y hat equals b plus w times x, and the loss is the mean squared error. With w and b at zero every prediction is zero, so the loss is the mean of y squared, {L0:.2f}. '
                         'Why centre? The centred distances add up to zero, so the slope for w stops depending on b, and one learning rate suits both. This is the Session 8 gradient again, on new data.')))

    S.append(dict(kind='formula', title='The gradient of the line-fit loss has one entry for w and one for b',
                  formulas=[('Gradient', r'$\frac{\partial L}{\partial w} = \frac{2}{n}\sum_{i=1}^{n}(\hat{y}_i - y_i)\,x_i \qquad \frac{\partial L}{\partial b} = \frac{2}{n}\sum_{i=1}^{n}(\hat{y}_i - y_i)$')],
                  symbols=[['∂L/∂w', 'How fast the loss changes when w changes (a partial derivative, Session 8).', f'{f3(n["dw0"])} at w = 0, b = 0'],
                           ['∂L/∂b', 'How fast the loss changes when b changes.', f'{f3(n["db0"])} at w = 0, b = 0'],
                           ['(y-hat_i minus y_i)', 'The error of row i. Positive means too high.', 'at the start: -y_i'],
                           ['2/n and the sums', 'Add over the rows, then multiply by 2/n.', f'2/{n["n"]} = 0.25; sum of error × x = {-n["sum_xy"]:.2f}; sum of errors = {-n["sum_y"]:.1f}']],
                  size=20, widths=[2.0, 5.2, 4.7], note='Both slopes are negative here, so the update raises both w and b.',
                  notes=('The gradient has two entries, one for each parameter. Both come from the chain rule of Session 9. The outer function is the square, whose derivative is two times the error. '
                         'The inner function is b plus w times x, whose derivative with respect to w is x, and with respect to b is one. So the slope for w is two over n times the sum of error times x, and the slope for b is two over n times the sum of the errors. '
                         f'At our start the two values are {f3(n["dw0"])} and {f3(n["db0"])}. Both are negative, so both parameters should grow.')))

    rows_h = [[str(i + 1), f'{xc[i]:+.1f}', f'{y[i]:.1f}', f'{-y[i]:.1f}', f'{-y[i] * xc[i]:.2f}'] for i in range(8)]
    S.append(dict(kind='table', title='Step 1 of the line fit by hand, starting from w = 0 and b = 0',
                  headers=['Row i', 'x (km)', 'y (thousand UGX)', 'Error: y-hat minus y', 'Error times x'], rows=rows_h, widths=[1.3, 1.6, 2.9, 2.6, 2.4], icons=False,
                  note=(f'Sums: error times x = {-n["sum_xy"]:.2f}, error = {-y.sum():.1f}. ∂L/∂w = 0.25 × ({-n["sum_xy"]:.2f}) = {f3(n["dw0"])}, ∂L/∂b = 0.25 × ({-y.sum():.1f}) = {f3(n["db0"])}. '
                        f'With eta = 0.1: w = {f4(n["w1"])}, b = {f4(n["b1"])}.'),
                  notes=(f'Step one with every number written out. With w and b at zero, each prediction is zero, so the error is minus y. The last column multiplies each error by x, and the two sums sit under the table. '
                         f'The slope for w is two over eight, that is point two five, times {-n["sum_xy"]:.2f}, which gives {f3(n["dw0"])}. The slope for b is point two five times {-y.sum():.1f}, which gives {f3(n["db0"])}. '
                         f'With eta equal to point one, the new w is {f4(n["w1"])} and the new b is {f4(n["b1"])}. This is exactly the first row of the spreadsheet lab.')))

    S.append(dict(kind='formula', title='Mean, half-sum and full-sum squared error share one minimum; only the step size changes',
                  formulas=[('MSE (today)', r'$L_{MSE} = \frac{1}{n}\sum_{i}(\hat{y}_i - y_i)^2$'),
                            ('Half sum and SSE', r'$L_{half} = \frac{1}{2}\sum_{i}(\hat{y}_i - y_i)^2 = \frac{n}{2}\,L_{MSE} \qquad L_{SSE} = \sum_{i}(\hat{y}_i - y_i)^2 = n\,L_{MSE}$')],
                  symbols=[['MSE', 'Loss and slope for w at w = 0, b = 0.', f'{F["mse"]:.2f}; slope {F["dw_mse"]:.3f}'],
                           ['Half sum (Session 11)', f'n/2 = {n["n"] // 2} times the MSE, and so is every slope.', f'{F["half"]:.2f}; slope {F["dw_half"]:.2f}'],
                           ['SSE (Session 12)', f'n = {n["n"]} times the MSE, and so is every slope.', f'{F["sse"]:.2f}; slope {F["dw_sse"]:.2f}'],
                           ['Best w and b', 'The same for all three: multiplying by a positive number moves no minimum.', f'w = {n["w_star"]:.2f}, b = {n["b_star"]:.2f}']],
                  size=19, widths=[2.4, 5.7, 3.8],
                  note=f'Same step, smaller eta: 0.1 with MSE equals {F["eta_half"]:g} with the half sum or {F["eta_sse"]:g} with SSE.',
                  notes=('Books and libraries write the squared-error loss in three ways, and you will meet all three in this course. Today we use the mean. Session 11 uses one half of the sum, and Session 12 uses the plain sum plus a penalty. '
                         f'They differ only by a constant factor. With our eight trips the half sum is four times the mean, and the full sum is eight times the mean, so every slope is four or eight times larger too. '
                         'The bottom of the bowl does not move, so the best line is the same. Only the step size changes, which is why the learning rate must shrink by the same factor.')))

    S.append(dict(kind='wide', title='The learning rate sets the size of each step: too small crawls, good arrives, too large overshoots',
                  visual=dict(kind='d_gd_rates', panels=[dict(title='Too small: eta = 0.01', path=bw[0.01][:6], note='Tiny steps, very slow'),
                                                         dict(title='Good: eta = 0.1', path=bw[0.1][:6], note='Steps shrink as the slope shrinks'),
                                                         dict(title='Too large: eta = 1.1', path=bw[1.1][:4], note='Each step overshoots further')]),
                  caption='Each panel: L(w) = (w - 3)^2, starting at w = 0. Dots are w after each step; arrows are the steps.',
                  notes=('The learning rate is the one setting you must get right. On the left, eta is point zero one: every step is tiny, and after five steps we have barely moved. '
                         'In the middle, eta is point one: the steps start big and shrink as the slope flattens, so we arrive at the bottom. '
                         'On the right, eta is one point one: the step is so large that we jump past the bottom and land higher up the other side. The next jump is bigger again, and the loss grows instead of falling. In a real run you see only the loss, never this picture.')))

    lr_rows = [[str(k), fmt(bw[0.01][k]), fmt(bw[0.1][k]), fmt(bw[1.1][k])] for k in range(6)]
    lr_rows.append(['Loss at step 5', fmt((bw[0.01][5] - 3) ** 2), fmt((bw[0.1][5] - 3) ** 2), fmt((bw[1.1][5] - 3) ** 2)])
    S.append(dict(kind='table', title='The same three learning rates as numbers: w after each step',
                  headers=['Step', 'eta = 0.01 (too small)', 'eta = 0.1 (good)', 'eta = 1.1 (too large)'], rows=lr_rows, widths=[3.3, 2.9, 2.7, 3.0], icons=False,
                  note='The loss at step 0 is 9 in all three columns. With eta = 1.0 exactly, w would bounce between 0 and 6 forever.',
                  notes=(f'The numbers behind the picture. With eta point zero one, w creeps from zero to {fmt(bw[0.01][5])} in five steps, and the loss is still {fmt((bw[0.01][5] - 3) ** 2)}. '
                         f'With eta point one, w reaches {fmt(bw[0.1][5])} and the loss is {fmt((bw[0.1][5] - 3) ** 2)}. '
                         f'With eta one point one, w goes to {fmt(bw[1.1][1])}, then {fmt(bw[1.1][2])}, then {fmt(bw[1.1][3])}. It swings further from three every time, and the loss grows to {fmt((bw[1.1][5] - 3) ** 2)}. '
                         'The rule of thumb: if the loss goes up, the learning rate is too large.')))

    S.append(dict(kind='wide', title='Batch, stochastic and mini-batch gradient descent use different numbers of rows for each step',
                  visual=dict(kind='d_batches'),
                  caption='Gold squares: the rows used for one gradient. An epoch is one pass through all 8 rows.',
                  notes=('So far every gradient used all eight rows. That is called batch gradient descent, one step per epoch. With millions of rows it is slow, because one step needs a pass over everything. '
                         'Stochastic gradient descent, SGD, uses a single row per step, so eight steps per epoch here. Each step is cheap, but the path is noisy, because one row is a poor guide. '
                         'The compromise is the mini-batch: a small group of rows, here four, so two steps per epoch. Its gradient is a noisy estimate of the full one, and in library manuals the name SGD usually means this version.')))

    S.append(dict(kind='wide', title='Momentum keeps a running memory of past gradients, which smooths a zigzag path',
                  visual=dict(kind='d_momentum'),
                  caption='Same valley, same start. Momentum damps the sideways swings that make plain descent zigzag.',
                  notes=('Here the loss is a long narrow valley. The gradient points mostly across the valley rather than along it, so plain gradient descent zigzags and makes slow progress along the floor. '
                         'Momentum adds a memory. Sideways gradients point one way, then the other, so they largely cancel in the memory. Gradients along the valley all point the same way, so they add up. '
                         'The result on the right is a smoother, faster path, because each step carries some speed from the steps before it.')))

    mom = n['mom']
    S.append(dict(kind='formula', title='The momentum velocity is a decaying sum of past gradients',
                  formulas=[('Velocity', r'$u_t = \beta\, u_{t-1} + g_t$'), ('Update', r'$w \leftarrow w - \eta\, u_t$')],
                  symbols=[['g_t', 'The gradient at step t.', 'illustrative: g = 2 at every step'],
                           ['u_t', 'The velocity: a running total of past gradients, each older one counted less. It starts at 0. (Adam\'s v, which follows, is a different thing.)', f'u = {mom[0]:.0f}, {mom[1]:.1f}, {mom[2]:.2f}'],
                           ['beta', 'The momentum coefficient, between 0 and 1. A common choice is 0.9.', 'beta = 0.9'],
                           ['eta', 'The learning rate.', 'as before']],
                  size=26, note=f'Steady gradient 2: u = 2, then 0.9 × 2 + 2 = {mom[1]:.1f}, then 0.9 × {mom[1]:.1f} + 2 = {mom[2]:.2f}. It grows towards 20.',
                  notes=('This is the momentum update, in the form used by common libraries. The velocity, written u, is beta times the old velocity plus the new gradient. The weight then moves by eta times u. We use the letter u so it is not confused with the v of Adam, which comes next. '
                         f'Take a gradient that stays at two. The first u is two. The second is point nine times two plus two, which is {mom[1]:.1f}. The third is point nine times {mom[1]:.1f} plus two, which is {mom[2]:.2f}. '
                         'The velocity keeps growing while the gradient keeps its sign, up to ten times the gradient when beta is point nine. If the gradient flips sign, the velocity shrinks.')))

    S.append(dict(kind='formula', title='Adam divides the average gradient by its typical size, so each parameter steps by about alpha',
                  formulas=[('Average gradient', r'$m_t = \beta_1 m_{t-1} + (1-\beta_1)\,g_t$'), ('Average squared gradient', r'$v_t = \beta_2 v_{t-1} + (1-\beta_2)\,g_t^2$'),
                            ('Update', r'$w \leftarrow w - \alpha\,\frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon}, \qquad \hat{m}_t = \frac{m_t}{1-\beta_1^{\,t}}, \quad \hat{v}_t = \frac{v_t}{1-\beta_2^{\,t}}$')],
                  symbols=[['m_t, v_t', 'Running averages of the gradients (like momentum) and of the squared gradients. Both start at 0.', 'beta1 = 0.9, beta2 = 0.999'],
                           ['m-hat, v-hat', 'The corrected averages. β1ᵗ is β1 to the power t, and t is the step number.', 'β1ᵗ = 0.9, 0.81, 0.729 for t = 1, 2, 3'],
                           ['alpha', 'Adam\'s learning rate (the paper writes alpha).', '0.1 here; the paper suggests 0.001'],
                           ['epsilon', 'A tiny number that avoids dividing by zero.', '1e-8']],
                  size=19, widths=[1.9, 6.2, 3.8],
                  notes=('Adam, published by Kingma and Ba in 2014, keeps two running averages for each parameter. The first, m, averages the gradients, which works like momentum. The second, v, averages the squared gradients, which measures how large the gradients typically are. '
                         'Both start at zero, so the first values are too small, and the correction divides by one minus beta to the power t to fix that. '
                         'The step is alpha times m hat over the root of v hat. When the gradient is steady, top and bottom have the same size, so every parameter moves by about alpha, whatever the size of its gradient.')))

    arows = [[str(r['t']), f4(r['g']), f4(r['m']), f4(r['v']), f4(r['mh']), f4(r['sq']), f4(r['step']), f4(r['w_after'])] for r in ad]
    S.append(dict(kind='table', title='Adam by hand: three steps on the same bowl, starting at w = 0',
                  headers=['t', 'g', 'm', 'v', 'm-hat', 'sqrt(v-hat)', 'Subtracted', 'w after'], rows=arows, widths=[0.7, 1.5, 1.5, 1.5, 1.5, 1.7, 1.6, 1.5], icons=False,
                  note='alpha = 0.1, beta1 = 0.9, beta2 = 0.999, epsilon = 1e-8. Subtracted = alpha × m-hat / (sqrt(v-hat) + epsilon). Subtracting a negative amount moves w to the right.',
                  notes=(f'Three Adam steps with real numbers. At step one the gradient is minus six. The average m is point one times minus six, which is {f4(ad[0]["m"])}. The average v is point zero zero one times thirty-six, which is {f4(ad[0]["v"])}. '
                         f'After the correction, m hat is minus six and the square root of v hat is six, so the amount subtracted is alpha times minus one. Subtracting minus point one moves w up to {f4(ad[0]["w_after"])}. '
                         f'At step two the gradient is {f4(ad[1]["g"])} and the step is again almost exactly alpha. By step three w is {f4(ad[2]["w_after"])}. The steps stay near alpha even though the slope shrinks.')))

    S.append(dict(kind='wide', title='A convex loss has a single bottom, while a network loss can have several dips',
                  visual=dict(kind='d_convex'),
                  caption='Left: a convex loss, one bowl. Right: several dips. A local minimum is a dip that is not the lowest.',
                  notes=('Convexity tells us how safe gradient descent is. A convex loss, on the left, is a single bowl. From any start, walking downhill reaches the one bottom. The mean squared error of a line fit is convex. '
                         'On the right is a loss with several dips. A dip that is lower than its neighbours but not the lowest is a local minimum. Gradient descent can stop there, depending on where it started. '
                         'The loss of a neural network is not convex. Even so, published experience is that large networks usually train well with the methods in this session, though we cannot prove that from this picture.')))

    S.append(dict(kind='idea', title='A learning-rate schedule changes eta during training',
                  visual=dict(kind='d_schedule'),
                  lead='A schedule gives a different learning rate at each step.',
                  points=['Grey: constant, or cut in steps.',
                          f'Red: warm-up to the peak over 100 steps, then a smooth cosine fall to 0 at step 1000. Peak 0.001: {sched(50):.4f} at steps 50 and 550.'],
                  notes=('A learning-rate schedule changes eta as training goes on. The grey dashed line is a constant rate. The grey solid line cuts the rate in steps. '
                         'The red line is warm-up followed by cosine decay. In warm-up the rate rises from zero to its peak over the first hundred steps, because the first gradients can be unreliable. Then it falls along half a cosine wave, so the late steps are small and settle into a minimum. '
                         f'With an illustrative peak of point zero zero one, step fifty and step five hundred and fifty both have half the peak, {sched(50):.4f}. Large steps help early; small steps help late.')))

    S.append(dict(kind='table', title='Four ways gradient descent goes wrong, and how each one shows itself',
                  headers=['Mistake', 'What you see', 'Fix'],
                  rows=[['Learning rate too large', 'The loss goes up, or becomes nan (not a number)', 'Divide eta by 3 or 10 and run again'],
                        ['Learning rate too small', 'The loss falls, but so slowly that it looks flat', 'Multiply eta by 3 or 10, or train for more steps'],
                        ['Wrong sign in the update', 'The loss climbs from the first step', 'Use w - eta × gradient, with the minus sign'],
                        ['Inputs on very different scales', 'One learning rate is too large for one parameter and too small for another', 'Centre (and, with several inputs, scale) the inputs. The lab centres the distance.']],
                  widths=[3.3, 4.4, 4.2], icons=False,
                  notes=('A learning rate that is too large shows as a loss that goes up or turns into nan, which means not a number. Divide eta by three or ten. '
                         'Too small, and the loss falls so slowly it looks flat, so increase eta or run longer. A wrong sign means you add the gradient instead of subtracting it, and you walk uphill from step one. '
                         f'Inputs on very different scales make one learning rate wrong for some parameter. With centred distances our w is stable for any eta below {n["eta_max_w"]:.2f}; with raw distances the limit drops to about {n["eta_max_uncentred"]:.3f}.')))

    S.append(dict(kind='compare', title='Momentum and Adam both smooth the steps, but Adam also rescales them',
                  left=dict(head='SGD with momentum', icon='gear', points=['One learning rate eta for all parameters', 'Remembers past gradients', 'Needs eta tuned with care']),
                  right=dict(head='Adam', icon='robot', points=['A separate effective step for each parameter', 'Remembers past gradients and their typical size', 'Works with the default settings in many cases']),
                  verdict='Both are optimisers: rules that turn a gradient into a step.',
                  notes=('Two optimisers side by side. SGD with momentum uses one learning rate for all parameters and remembers past gradients. Adam also remembers the typical size of each parameter gradient, and uses it to rescale the step for that parameter. '
                         'That makes Adam forgiving: the default settings often work. An optimiser is a rule that turns the gradient into a step, and plain gradient descent is the simplest one. '
                         'Which would you try first on a new problem, and why?')))

    S.append(dict(kind='code', title='Read the loop before you write it: gradient, then update, repeated',
                  code='for step in range(30):\n    err = w * xc + b - y\n    dw = 2 * np.mean(err * xc)\n    db = 2 * np.mean(err)\n    w = w - eta * dw\n    b = b - eta * db',
                  reads=['err holds the error y-hat - y of every row.', 'dw and db are the two slopes of the loss: the gradient.', 'The last two lines are the update rule.', 'The loop repeats it 30 times. xc is the centred distance.'],
                  notes=('Before the lab, read the whole algorithm. This is gradient descent in six lines. The loop runs thirty steps. Inside, the first line computes the error for every row. '
                         'The next two lines are the two slopes from the formulas, written with numpy means. The last two lines are the update rule, once for w and once for b. '
                         'In the lab the notebook gives you the outer frame and you write the four lines for the slopes and the update yourself. In the spreadsheet, each pass through the loop becomes one row.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the concepts. Please close the slides and open either the Python notebook or the spreadsheet workbook. Both use the same eight trips and the same numbers, so you can compare answers with someone on the other track. '
                         'In every step, write your prediction first, then run, then read, then change one thing. Raise your hand when a check says not yet.')))

    S.append(dict(kind='steps', title='Five lab steps take the eight trips from one hand step to four loss curves',
                  steps=[dict(head='1 Look', text='Load the 8 trips and centre the distance', icon='folder'), dict(head='2 Gradient', text='Loss and two slopes at w = 0, b = 0', icon='calculator'),
                         dict(head='3 One step', text='Apply the update rule once', icon='pin'), dict(head='4 Loop', text='Write the loop, run 30 steps, compare with least squares', icon='gear'),
                         dict(head='5 Compare', text='Four learning rates, four loss curves', icon='chart')], highlight=3,
                  caption='The notebook and the workbook follow these five steps. Predict first, run, read the output, then change one thing.',
                  notes=('The lab has five steps, and the notebook uses the same five numbers. One, look at the eight trips and subtract the average distance. Two, compute the loss and the two slopes at w and b equal to zero. Three, apply the update rule once. '
                         'Four, write the loop and run thirty steps, then compare the line with the least squares answer: in Python a loop, in the spreadsheet one row for each step. Five, repeat with four learning rates and compare the loss curves. '
                         'Predicting before you run is how you find out what you understand, so please do not skip the predict boxes.')))

    S.append(dict(kind='table', title='Your lab numbers should match these at every step',
                  headers=['What you compute', 'You should see'],
                  rows=[['Loss at w = 0, b = 0', f2(L0)], ['∂L/∂w and ∂L/∂b at w = 0, b = 0', f'{f3(n["dw0"])} and {f3(n["db0"])}'], ['w and b after one step with eta = 0.1', f'{f4(n["w1"])} and {f4(n["b1"])}'],
                        ['Loss after 30 steps, eta = 0.1', f4(R[0.1]['L'][-1])], ['Best line by the least squares method of Session 4, on these eight trips', f'w = {f3(n["w_star"])}, b = {f3(n["b_star"])}'],
                        ['Loss after 30 steps, eta = 0.01 and 0.05', f'{f3(R[0.01]["L"][-1])} and {f4(R[0.05]["L"][-1])}'], ['Loss after 30 steps, eta = 0.2', f'{R[0.2]["L"][-1]:.1f} (it grew)']],
                  widths=[7.2, 4.4], icons=False,
                  note='If your number differs, find the step that went wrong. Do not change a number to match.',
                  notes=('If your numbers match, carry on. If one does not, stop and look for the step that went wrong, because every later step builds on it. '
                         f'With eta point one, the loss after thirty steps is {f4(R[0.1]["L"][-1])}, very close to the least squares answer for the same eight trips, and the weights approach {f3(n["w_star"])} and {f3(n["b_star"])}. '
                         f'With eta point zero five the loss is {f4(R[0.05]["L"][-1])}, still a little behind. With eta point two the loss has grown to about {R[0.2]["L"][-1]:.0f}, so that curve is the one that goes up.')))

    S.append(dict(kind='table', title='Lab messages, what they mean and what to do next',
                  headers=['What you see', 'What it means', 'What to do'],
                  rows=[['The loss is nan or inf', 'The learning rate is too large and the numbers overflowed', 'Divide eta by 10'],
                        ['NameError in Python', 'A cell that defines a name was not run', 'Run all cells from the top'],
                        ['A flat loss curve', 'The learning rate is too small, or the loop did not update w', 'Check that w = w - eta * dw is inside the loop'],
                        ['Sheet formula shows #REF! or 0', 'A row refers to the wrong previous row', 'Compare with the row above: step t uses row t - 1']],
                  widths=[3.3, 4.6, 4.0], icons=False,
                  notes=('A loss of nan or inf means the learning rate is too large and the numbers blew up, so divide eta by ten. A name error means you skipped a cell, so run all cells from the top. '
                         'A flat curve means eta is too small or the update sits outside the loop. In the sheet, a reference error or a zero usually means a row points at the wrong previous row. '
                         'Python puts the most useful part of an error at the bottom, so read the last line of any message first.')))

    S.append(dict(kind='idea', title='Where this appears in AI: every training step ends with an optimiser update',
                  visual=dict(kind='d_loop', items=['Take a batch of text', 'Forward pass: predict the next token', 'Loss: how wrong the next-token probabilities were', 'Backward pass: the gradient', 'Optimiser update (Adam type)'], center='one training step'),
                  lead='Training is one loop, repeated a very large number of times.',
                  points=['Forward and backward pass: Session 11. Cross-entropy, the loss for next tokens: Session 17.',
                          'Published work uses Adam-type optimisers with warm-up. Product settings are not published.'],
                  notes=('Language models of this kind are trained by a loop. Take a batch of text, run the model forward to predict each next token, measure how wrong those predictions were, run backward to get the gradient, and apply an optimiser update. '
                         'You meet the forward and backward pass properly next session, and the loss for next tokens, called cross-entropy, in Session 17. '
                         'The 2017 transformer paper used Adam with four thousand warm-up steps, followed by a decay in proportion to one over the square root of the step number; cosine decay is another common choice. The exact settings of ChatGPT, Gemini and Claude are not published.')))

    S.append(dict(kind='practice', title='Check an AI assistant with your own numbers', minutes=10, label='Hands-on, with no private data',
                  task='Ask any AI assistant to do three Adam steps. Then compare with the table.',
                  steps=['Type: "For L(w) = (w - 3)^2, start w = 0, alpha = 0.1, beta1 = 0.9, beta2 = 0.999. Show m, v and w for three Adam steps."',
                         f'Compare its w after step 3 with the table: {f4(ad[2]["w_after"])}.', 'If it differs, find the first number that differs.', 'Never paste confidential data.'],
                  output='A note: did the assistant match your table?',
                  notes=('Ask any assistant to carry out three Adam steps with exactly the numbers on the slide. Then compare its answer with your table, row by row. '
                         f'The w after step three should be {f4(ad[2]["w_after"])}. Assistants sometimes make arithmetic slips, so find the first number that differs and work out which formula it applied wrongly. '
                         'Use the assistant to explain, and use your own calculation to check. Please never paste confidential data into an assistant.')))

    S.append(dict(kind='table', title='Exit check: three questions with short answers',
                  headers=['Question', 'Short answer'],
                  rows=[['With eta = 0.1 and a slope of minus 4, what is the new w if the old w is 1?', 'w = 1 - 0.1 × (-4) = 1.4.'],
                        ['The loss grows at every step. What is the most likely cause and the fix?', 'The learning rate is too large. Divide it by 3 or 10.'],
                        ['Give one difference between SGD and Adam.', 'SGD uses one learning rate for all parameters. Adam rescales the step for each parameter using the typical size of its gradient.']],
                  widths=[5.8, 6.2], icons=False,
                  notes=('With a learning rate of point one and a slope of minus four, the new w from an old w of one is one minus point one times minus four, which is one point four. '
                         'If the loss grows at every step, the learning rate is almost certainly too large, so divide it by three or ten. '
                         'And SGD uses a single learning rate for every parameter, while Adam rescales the step for each parameter using the typical size of its gradient. Write your own answers first, then compare.')))

    s['facilitator'] = dict(
        prep=['Open the notebook in Colab and the workbook in Excel or Google Sheets before the class, and run both once.',
              'Write the four numbers eta = 0.01, 0.05, 0.1, 0.2 on the board. Learners predict which curve falls fastest and which one grows.',
              'Check the by-hand table on the slide "Step 1 of the line fit" with a calculator; the first row of the sheet must match it.'],
        misconceptions=[('A bigger learning rate always trains faster', f'Only up to a limit. Above it the loss grows. Here the limit for w is about {n["eta_max_w"]:.2f}.'),
                        ('Gradient descent always finds the best answer', 'Only for a convex loss. A neural network loss has many dips.'),
                        ('SGD means one row at a time', 'In libraries it usually means mini-batch gradient descent.'),
                        ('Adam does not need a learning rate', 'It still has alpha, and a schedule is still used in published training.'),
                        ('MSE and the sum of squares give different best lines', 'They differ by a constant factor, so the minimum is the same. Only the slopes, and so the right eta, scale.')],
        probes=[('What happens to the step size as w approaches the bottom of a bowl?', 'The slope shrinks, so the step shrinks even with a fixed learning rate.'),
                ('Why subtract the average distance before running gradient descent?', f'The centred distances add up to 0, so the slope for w no longer depends on b and one learning rate suits both (w is stable below {n["eta_max_w"]:.2f}, b below 1). Uncentred, the limit drops to about {n["eta_max_uncentred"]:.3f}.'),
                ('Why does Adam correct m and v?', 'They start at 0, so early values are too small. The correction divides by 1 minus beta to the power t.'),
                ('Is the learning rate learned by gradient descent?', 'No. It is a hyperparameter chosen before training, or given by a schedule.')],
        lab_steps=[('Python and spreadsheet: step 1, look and centre', 'Eight trips, x centred with the learner\'s own mean distance 4.5. Loss at zero is 52.11. Spreadsheet: Data!F3 feeds the centred column.'),
                   ('Python and spreadsheet: steps 2 and 3, gradient and one step', f'Slopes {f3(n["dw0"])} and {f3(n["db0"])}. After one step w = {f4(n["w1"])} and b = {f4(n["b1"])}. Spreadsheet: gold cells in row 0 and row 1 of block 1.'),
                   ('Python: step 4, the loop', f'Learners write four lines inside the loop. With eta 0.1, w = {n["runs"][0.1]["w"]:.4f} after 30 steps, within 0.01 of the least squares slope {n["w_star"]:.2f}.'),
                   ('Python: step 5, four rates', 'The curve for 0.2 climbs; the curve for 0.01 is still high at step 30; 0.1 reaches the minimum.'),
                   ('Spreadsheet: one row per step', 'Row 0 holds w = 0, b = 0. Each next row applies the update rule to the row above. The other three blocks are given and read only. At 0.2 the loss column grows.')],
        rescue=['If the concepts overrun, skip the momentum formula slide and say: momentum is a running memory of gradients.', 'If the sheet confuses a learner, do the Python loop on the projector and map each line to a sheet column.',
                'If only 20 minutes remain for the lab, run steps 1 to 4 and the single learning rate 0.1.'],
        after=['Share the solution notebook with absent learners.', 'Ask learners to bring one question about backpropagation.'],
        lab_answer_key=[['PREDICT (step 1): the mean distance', '4.5 km.'], ['READ (step 1): why do the centred distances run from -3.5 to +3.5?', 'Subtracting 4.5 from 1 and from 8. A centred distance of 0 is a trip of average length.'],
                        ['PREDICT (step 2): the loss at w = 0, b = 0', 'The mean of y squared, 52.11.'],
                        ['PREDICT (step 5): which learning rate gives the fastest fall?', 'Among 0.01, 0.05 and 0.1 the largest, 0.1. The value 0.2 is too large.'], ['READ (step 5): what does the 0.2 curve do?', 'It rises. The step overshoots by more each time.'],
                        ['CHANGE: use 0.19', 'The loss still falls, but slowly (4.37 after 30 steps): w swings from side to side because 0.19 is just under its limit of about 0.19.'], ['CHANGE: do not centre x', f'Only eta = 0.01 still works. The limit is about {n["eta_max_uncentred"]:.3f}, so 0.05, 0.1 and 0.2 blow up.']])
    return s
