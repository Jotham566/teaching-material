"""Session 11: Backpropagation by hand. Author D."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'kit'))
import diagrams_math_d as D  # noqa: E402


def build():
    n = D.n11()
    f4 = lambda v: f'{float(v):.4f}'
    W1, b1, W2, b2, x, y, eta = n['W1'], n['b1'], n['W2'], n['b2'], n['x'], n['y'], n['eta']
    s1, s2, s3 = n['s1'], n['s2'], n['s3']
    nW1, nb1, nW2, nb2 = n['new1']
    sig = lambda v: 1 / (1 + 2.718281828459045 ** (-v))
    z, a, yh, L = s1['z1'], s1['a1'], s1['yh'], s1['L']
    d2, d1 = s1['d2'], s1['d1']
    gW1, gW2, gb1, gb2 = s1['gW1'], s1['gW2'], s1['gb1'], s1['gb2']
    red = (L - s2['L']) / L * 100

    s = dict(
        num=11, block='Calculus and optimisation', short_title='Backpropagation by hand',
        title='Backpropagation by hand: the chain rule, run backwards through a tiny network',
        question='What happens in every training step of a language model, and why does training cost far more computing than answering a question?',
        outcomes=['Compute the forward pass and the loss of a tiny network, with every number written out',
                  'Derive the slopes of the sigmoid and tanh, then compute every gradient in the backward pass, apply the update, and see the loss fall',
                  'Write the same computation with the matrices W, b and delta, and check the gradients with finite differences in code'],
        outcome_icons=['calculator', 'gear', 'check'],
        outcome_note=('By the end of today you can do three things with a network small enough to calculate by hand. Run the forward pass, with every number written out. '
                      'Derive the slopes of the sigmoid and tanh, run the backward pass, update the weights, and see the loss fall. And write the same computation with matrices, then check your gradients in code with finite differences. '
                      'The ideas are the ones you already know: the chain rule from Session 9 and the update rule from Session 10. Which part do you expect to be the hardest?'),
        clock=[(10, 'Recall and a real question from AI'), (35, 'Concept: a picture, then a hand example'), (10, 'Break'), (45, 'Lab: Python or spreadsheet, predict, run, change'),
               (15, 'Where it appears in AI, plus an exit check'), (5, 'Save the work')],
        plan_title='Your two hours: one network, forward then backward',
        plan_caption='Pictures and hand calculations first. Then the lab: numpy, or cells in the spreadsheet.',
        plan_note=('We have two hours. The first ten minutes recall gradient descent and ask the question of the day. Then thirty-five minutes at the board: a tiny network, forward and backward, with every number written out, then the same in matrix form. '
                   'After the break, forty-five minutes of lab where you implement it and check it with finite differences. The last fifteen minutes show what each training step of a language model does, and why training costs so much more than answering.'),
        recall_from='Session 10',
        recall=[('With eta = 0.1, old w = 2 and a slope of 5, what is the new w?', 'New w = 2 - 0.1 × 5 = 1.5.'),
                ('The loss grows at every step of gradient descent. What is the most likely cause?', 'The learning rate is too large, so each step overshoots the bottom. Divide it by 3 or 10.'),
                ('What does Adam add to plain gradient descent?', 'A running average of past gradients, and a separate step size for each parameter based on the typical size of its gradient.')],
        words=[('Forward pass', 'Computing the output and the loss from the inputs, layer by layer.'),
               ('Backward pass', 'Computing the gradient of the loss for every parameter, from the output back to the input.'),
               ('Backpropagation', 'The backward pass that applies the chain rule from the loss back to every parameter, reusing the values stored in the forward pass.'),
               ('Delta', 'The gradient of the loss with respect to the input of a unit, written with the Greek letter delta.'),
               ('Sigmoid and tanh', 'Sigmoid 1 / (1 + e^-z) squeezes any number into 0 to 1; tanh squeezes it into -1 to 1.')],
        word_icons=['pin', 'flag', 'gear', 'calculator', 'chart'],
        words_note=('Five words for today. The forward pass computes the output and the loss. The backward pass computes the gradient of the loss for every parameter, from the output back to the input. '
                    'Backpropagation is the backward pass: the chain rule applied from the loss back to every parameter, reusing the values stored in the forward pass. A delta is the gradient of the loss with respect to the input of one unit. The sigmoid squeezes any number into the range zero to one, and tanh into minus one to one. We use every one of these before the break.'),
        keep='Keep your saved notebook or workbook, with the nine gradients of the tiny network and the check that finite differences agree with them. Write down the loss before and after one update.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Loss, before', value=f4(L)), dict(label='Loss, after one update', value=f4(s2['L'])), dict(label='Check', value='Finite differences agree'),
                                                              dict(label='Next session', value='Optimisation in practice')]),
        keep_title='Save your lab and keep the nine gradients',
        next='Session 12: optimisation in practice: a penalty that keeps the weights small, then softmax and the arithmetic that keeps numbers in range.', next_label='Next session',
        keep_note=('Before you go, save your notebook or workbook. Keep the nine gradients of the tiny network and the finite-difference check that proves them right. Note the loss before and after one update. '
                   'Next session is about what goes wrong in practice: overfitting, which a penalty controls, and numbers that overflow, which a small algebra trick fixes. Bring any question about the delta formulas today.'),
        cover_note=('Welcome to Session 11. In Session 9 you learned the chain rule, and in Session 10 you learned to take steps along a gradient. Today we put them together. '
                    'We take a network with nine numbers inside, small enough to compute by hand, and we find the gradient of every one of them. That computation is backpropagation, and it is what happens in every training step of every large model.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 10', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.6, 6.4], icons=False,
                  note='Check your answers. If one surprised you, look at Session 10 before the lab.',
                  notes=('With eta point one, old w of two and a slope of five, the new w is two minus point five, which is one point five. '
                         'If the loss grows at every step, the learning rate is almost certainly too large, and each step overshoots the bottom. '
                         'And Adam adds two things to plain gradient descent: a running average of past gradients, and a separate step size for each parameter based on how large its gradients typically are. Today we find the gradients that those methods use.')))

    S.append(dict(kind='idea', title='A tiny network: 2 inputs, 2 hidden units with a sigmoid, and 1 output',
                  visual=dict(kind='d_net', inputs=[f'x1 = {x[0]:.1f}', f'x2 = {x[1]:.1f}'], hidden=[f'hidden 1\nbias {b1[0]:.1f}', f'hidden 2\nbias {b1[1]:.1f}'], out=f'output\nbias {b2[0]:.1f}',
                              edges1=[[f'{W1[0][0]:g}', f'{W1[0][1]:g}'], [f'{W1[1][0]:g}', f'{W1[1][1]:g}']], edges2=[f'{W2[0][0]:g}', f'{W2[0][1]:g}'], foot='The numbers on the lines are the weights.'),
                  lead='Nine numbers can change: 6 weights and 3 biases.',
                  points=['A hidden unit adds its weighted inputs and bias, then applies the sigmoid.', f'The output unit adds its weighted inputs and its bias and applies no sigmoid. The target is y = {y:.1f}.'],
                  notes=('This is the network we compute by hand today. Two inputs on the left, two hidden units in the middle, one output on the right. The numbers on the lines are the weights, and each unit also has a bias. '
                         'That gives six weights and three biases, nine parameters in total. Each hidden unit adds up its weighted inputs and its bias, then applies the sigmoid. The output unit adds up its weighted inputs and bias, and applies no sigmoid. '
                         'The numbers are illustrative, chosen small and simple. What would the picture look like for a network with a billion parameters?')))

    S.append(dict(kind='table', title='Every number we start with: the inputs, the target and the nine parameters',
                  headers=['Name', 'Meaning', 'Value'],
                  rows=[['x', 'The two inputs of the example', f'{x[0]:.1f} and {x[1]:.1f}'], ['y', 'The target (the answer we want)', f'{y:.1f}'],
                        ['W(1)', 'Weights into the hidden units (layer 1): one row per hidden unit', f'({W1[0][0]:g}, {W1[0][1]:g}) and ({W1[1][0]:g}, {W1[1][1]:g})'], ['b(1)', 'Biases of the two hidden units', f'{b1[0]:g} and {b1[1]:g}'],
                        ['W(2)', 'Weights into the output unit (layer 2)', f'{W2[0][0]:g} and {W2[0][1]:g}'], ['b(2)', 'Bias of the output unit', f'{b2[0]:g}'], ['eta', 'The learning rate', f'{eta:g}']],
                  widths=[1.6, 6.2, 4.0], icons=False,
                  note='These are illustrative numbers, chosen small and simple. Results are rounded to 4 decimals on the slides; the computer keeps full precision.',
                  notes=('Every number we start with sits in this one table. The inputs are one and two. The target is one. The weights into the hidden layer form a matrix called W one, with one row for each hidden unit. '
                         'The biases are b one. The weights into the output are W two, and the bias is b two. The learning rate is point five. '
                         'All of these are illustrative, chosen small and simple. Results on the slides are rounded to four decimals, while the computer keeps full precision, so a last digit may differ in your own calculation.')))

    S.append(dict(kind='formula', title='The forward pass: weighted sum, sigmoid, weighted sum, then the loss',
                  formulas=[('Hidden unit j', r'$z^{(1)}_j = W^{(1)}_{j1}x_1 + W^{(1)}_{j2}x_2 + b^{(1)}_j \qquad a^{(1)}_j = \sigma(z^{(1)}_j) = \frac{1}{1+e^{-z^{(1)}_j}}$'),
                            ('Output', r'$\hat{y} = W^{(2)}_{1}a^{(1)}_1 + W^{(2)}_{2}a^{(1)}_2 + b^{(2)}$'), ('Loss', r'$L = \frac{1}{2}(\hat{y} - y)^2$')],
                  symbols=[['x_i, y; σ', 'Inputs and target. σ is the sigmoid 1 / (1 + e^-z), between 0 and 1.', 'x = (1, 2), y = 1'],
                           ['z(1)_j, a(1)_j', 'Input of hidden unit j and its output after the sigmoid.', 'j = 1, 2'],
                           ['W(1), b(1), W(2), b(2)', 'Weights and biases of layer 1 and of the output. W(1)_ji: input i to unit j.', 'the starting table'],
                           ['y-hat, L', 'Prediction; loss = half the squared error (Session 10: same minimum as MSE).', 'one number each']],
                  size=17, widths=[2.3, 6.4, 3.2],
                  notes=('The forward pass in formulas. For hidden unit j, the input z is the weighted sum of the two inputs plus the bias, and the output a is the sigmoid of z. '
                         'The prediction y hat is the weighted sum of the two hidden outputs plus the output bias. The loss is one half of the squared difference between the prediction and the target. '
                         'The one half is a convenience: when we differentiate the square, the two cancels it. The small numbers in brackets say which layer a quantity belongs to, and the subscript says which unit: z one in brackets, subscript two, is the input of hidden unit two. Without a subscript we mean the list of both units. Can you find where each symbol sits on the picture?')))

    S.append(dict(kind='idea', title='The forward pass with our numbers: the loss is 0.3417',
                  visual=dict(kind='d_net', inputs=[f'x1 = {x[0]:.1f}', f'x2 = {x[1]:.1f}'], hidden=[f'z = {z[0]:.4f}\na = {a[0]:.4f}', f'z = {z[1]:.4f}\na = {a[1]:.4f}'], out=f'y-hat =\n{yh:.4f}',
                              edges1=[[f'{W1[0][0]:g}', f'{W1[0][1]:g}'], [f'{W1[1][0]:g}', f'{W1[1][1]:g}']], edges2=[f'{W2[0][0]:g}', f'{W2[0][1]:g}'], foot=f'L = 0.5 × ({yh:.4f} - {y:.1f})^2 = {L:.4f}'),
                  lead=f'The prediction is {yh:.4f}, far from the target {y:.1f}.',
                  points=['z is the weighted sum in a hidden unit; a is its sigmoid.', 'The loss is large, so the gradients will push the weights hard.'],
                  notes=(f'These are the values flowing through the network. Hidden unit one has z equal to {z[0]:.4f}, and its sigmoid is {a[0]:.4f}. Hidden unit two has z equal to {z[1]:.4f}, and its sigmoid is {a[1]:.4f}. '
                         f'The output is the weighted sum of those two values plus the bias, which is {yh:.4f}. The target is one, so the prediction is far too low, and the loss is {L:.4f}. '
                         'The table after this one follows each calculation step by step. Why is the output so much smaller than the target?')))

    S.append(dict(kind='table', title='The forward pass, one calculation at a time',
                  headers=['Quantity', 'Calculation', 'Value'],
                  rows=[['z(1)_1', f'{W1[0][0]:g} × {x[0]:.1f} + ({W1[0][1]:g}) × {x[1]:.1f} + {b1[0]:g}', f4(z[0])], ['a(1)_1 = sigmoid(z(1)_1)', f'1 / (1 + e^({-z[0]:.4f}))', f4(a[0])],
                        ['z(1)_2', f'{W1[1][0]:g} × {x[0]:.1f} + {W1[1][1]:g} × {x[1]:.1f} + ({b1[1]:g})', f4(z[1])], ['a(1)_2 = sigmoid(z(1)_2)', f'1 / (1 + e^({-z[1]:.4f}))', f4(a[1])],
                        ['y-hat', f'{W2[0][0]:g} × {a[0]:.4f} + ({W2[0][1]:g}) × {a[1]:.4f} + {b2[0]:g}', f4(yh)], ['L', f'0.5 × ({yh:.4f} - {y:.1f})^2', f4(L)]],
                  widths=[2.6, 6.0, 1.8], icons=False,
                  notes=(f'Every calculation for the forward pass. The first hidden unit: point two times one, plus minus point three times two, plus the bias point one, gives {z[0]:.4f}. Its sigmoid is {a[0]:.4f}. '
                         f'The second: point four times one, plus point one times two, minus point two, gives {z[1]:.4f}, and the sigmoid is {a[1]:.4f}. '
                         f'The output is point five times {a[0]:.4f} minus point four times {a[1]:.4f} plus point two, which is {yh:.4f}. The loss is {L:.4f}. Please check the second row with a calculator, because the sigmoid is the step that is easiest to get wrong.')))

    S.append(dict(kind='wide', title='The sigmoid squeezes into 0 to 1 and tanh into minus 1 to 1; both are steepest at z = 0',
                  visual=dict(kind='d_sig_tanh'),
                  caption='Black: the function. Red dashed: its slope (at most 0.25 for the sigmoid, 1 for tanh).',
                  notes=('Two activation functions you will meet everywhere. On the left is the sigmoid, the one in our network. Very negative inputs give nearly zero, very positive inputs give nearly one, and z equal to zero gives exactly one half. '
                         'On the right is tanh, the hyperbolic tangent. It has the same S shape, stretched to run from minus one to one, and it passes through zero. '
                         'The red dashed curves are their slopes. Both slopes are largest in the middle and fall towards zero at the edges, which matters a great deal for training deep networks in Session 12.')))

    S.append(dict(kind='formula', title='The slope of the sigmoid, derived step by step, is a times (1 minus a)',
                  formulas=[('Write it as a power', r'$a = \sigma(z) = \left(1 + e^{-z}\right)^{-1}$'),
                            ('Chain rule (Session 9)', r'$\frac{da}{dz} = -\left(1 + e^{-z}\right)^{-2} \cdot \left(-e^{-z}\right) = \frac{e^{-z}}{\left(1 + e^{-z}\right)^{2}}$'),
                            ('Split into two factors', r'$\frac{da}{dz} = \frac{1}{1 + e^{-z}} \cdot \frac{e^{-z}}{1 + e^{-z}} = a\,(1 - a)$')],
                  symbols=[['Outer and inner', 'Outer: u to the power -1 has slope -u^-2. Inner: u = 1 + e^-z has slope -e^-z (Session 7).', 'multiply the two'],
                           ['Second factor', 'e^-z / (1 + e^-z) = 1 - 1 / (1 + e^-z) = 1 - a.', 'a + (1 - a) = 1'],
                           ['Largest slope', 'At z = 0, a = 0.5, so a(1 - a) = 0.25. Elsewhere it is smaller.', '0.5 × 0.5 = 0.25'],
                           ['Check on our unit 1', f'z = {n["sig_z"]:g}: a = {n["sig_a"]:.4f}, slope = {n["sig_a"]:.4f} × {1 - n["sig_a"]:.4f}.', f'{n["sig_slope"]:.4f}']],
                  size=19, widths=[2.2, 6.4, 3.3],
                  notes=('This is where a times one minus a comes from. Write the sigmoid as one plus e to the minus z, to the power minus one. The chain rule from Session 9 gives the outer slope, minus that bracket to the power minus two, times the inner slope, minus e to the minus z. The two minus signs cancel. '
                         'Now split the fraction into two factors. The first is the sigmoid itself, a. The second is e to the minus z over one plus e to the minus z, which equals one minus a. So the slope is a times one minus a. '
                         f'At z equal to zero that is a quarter, the largest it can be. For our first hidden unit it is {n["sig_slope"]:.4f}.')))

    S.append(dict(kind='formula', title='Tanh is a stretched sigmoid, and its slope is 1 minus h squared',
                  formulas=[('Definition', r'$h = \tanh(z) = \frac{e^{z} - e^{-z}}{e^{z} + e^{-z}} = 2\,\sigma(2z) - 1$'),
                            ('Slope', r'$\frac{dh}{dz} = 4\,\sigma(2z)\left(1 - \sigma(2z)\right) = 4 \cdot \frac{1 + h}{2} \cdot \frac{1 - h}{2} = 1 - h^{2}$')],
                  symbols=[['h', 'The output of tanh, between -1 and 1.', f'tanh({n["tanh_z"]:g}) = {n["tanh_h"]:.4f}'],
                           ['2 σ(2z) minus 1', 'Tanh is the sigmoid of 2z, stretched by 2 and moved down by 1.', f'2 × σ(1) - 1 = {n["tanh_h"]:.4f}'],
                           ['Slope steps', 'Chain rule: the inner 2z gives a factor 2, the outer stretch another 2. Then σ(2z) = (1 + h) / 2 and 1 - σ(2z) = (1 - h) / 2.', '2 × 2 = 4'],
                           ['1 minus h^2', 'The slope of tanh. It is 1 at z = 0 and falls towards 0 at the edges.', f'1 - {n["tanh_h"]:.4f}^2 = {n["tanh_slope"]:.4f}']],
                  size=19, widths=[2.0, 6.6, 3.3],
                  notes=('Tanh, the hyperbolic tangent, is defined with exponentials, and it turns out to be a stretched sigmoid: two times the sigmoid of two z, minus one. You can check that at z equals point five. '
                         'Its slope follows from the sigmoid slope we just derived. The chain rule brings a factor two from the inner two z and another two from the outer stretch, so four times sigma times one minus sigma. '
                         f'Write sigma of two z as one plus h over two, and the slope becomes one minus h squared. At z equals point five that is {n["tanh_slope"]:.4f}. Session 18 uses tanh in a small network.')))

    S.append(dict(kind='steps', title='The backward pass multiplies local slopes along each path from the loss back to a weight',
                  steps=[dict(head='Loss', text='dL/d(y-hat) = y-hat - y', icon='flag'), dict(head='Output', text='d(y-hat)/dW(2)_j = a(1)_j, and d(y-hat)/da(1)_j = W(2)_j', icon='pin'),
                         dict(head='Sigmoid', text='da(1)_j/dz(1)_j = a(1)_j × (1 - a(1)_j)', icon='chart'), dict(head='Hidden sum', text='dz(1)_j/dW(1)_ji = x_i, and dz(1)_j/db(1)_j = 1', icon='calculator')],
                  caption='Chain rule from Session 9: the slope for a weight is the product of the slopes along the path.',
                  notes=('The backward pass is the chain rule. To find how the loss changes with a weight deep in the network, we multiply the local slopes along the path from the loss back to that weight. '
                         'There are four local slopes. The loss with respect to the prediction is the prediction minus the target. The prediction with respect to a weight in the last layer is the hidden output, and with respect to a hidden output it is the weight. '
                         'The sigmoid contributes a times one minus a, which we derived a moment ago. And the hidden sum with respect to a first-layer weight is the input itself. The next two tables combine them.')))

    S.append(dict(kind='table', title='At the output layer, delta(2) is the prediction minus the target',
                  headers=['Quantity', 'Calculation', 'Value'],
                  rows=[['delta(2) = dL/d(y-hat)', f'{yh:.4f} - {y:.1f}', f4(d2)], ['dL/dW(2)_1 (first weight)', f'delta(2) × a(1)_1 = ({d2:.4f}) × {a[0]:.4f}', f4(gW2[0][0])],
                        ['dL/dW(2)_2 (second weight)', f'delta(2) × a(1)_2 = ({d2:.4f}) × {a[1]:.4f}', f4(gW2[0][1])], ['dL/db(2)', 'delta(2) × 1', f4(gb2[0])]],
                  widths=[3.4, 5.2, 1.8], icons=False,
                  note='delta(2) is the gradient of the loss with respect to the output y-hat. Negative values mean: raise this parameter to lower the loss.',
                  notes=(f'We start at the loss and walk back. The first delta, delta two, is the slope of the loss with respect to the prediction, the prediction minus the target: {d2:.4f}. The output unit has no sigmoid, so its input and its output are the same number, y hat. '
                         f'The slope for each output weight is delta two times the hidden output that the weight multiplies: {gW2[0][0]:.4f} for the first and {gW2[0][1]:.4f} for the second. '
                         f'The slope for the output bias is delta two, since the bias multiplies one. All are negative, so raising these parameters lowers the loss.')))

    S.append(dict(kind='table', title='In the hidden layer, each delta picks up the sigmoid slope a times (1 minus a)',
                  headers=['Quantity', 'Calculation', 'Value'],
                  rows=[['dL/da(1)_1', f'W(2)_1 × delta(2) = {W2[0][0]:g} × ({d2:.4f})', f4(W2[0][0] * d2)], ['delta(1)_1', f'({W2[0][0] * d2:.4f}) × a(1)_1 × (1 - a(1)_1) = ({W2[0][0] * d2:.4f}) × {a[0] * (1 - a[0]):.4f}', f4(d1[0])],
                        ['dL/da(1)_2', f'W(2)_2 × delta(2) = ({W2[0][1]:g}) × ({d2:.4f})', f4(W2[0][1] * d2)], ['delta(1)_2', f'{W2[0][1] * d2:.4f} × a(1)_2 × (1 - a(1)_2) = {W2[0][1] * d2:.4f} × {a[1] * (1 - a[1]):.4f}', f4(d1[1])],
                        ['dL/dW(1) (row 1)', f'delta(1)_1 × inputs = ({d1[0]:.4f}) × ({x[0]:.1f}, {x[1]:.1f})', f'{gW1[0][0]:.4f}, {gW1[0][1]:.4f}'],
                        ['dL/dW(1) (row 2)', f'delta(1)_2 × inputs = {d1[1]:.4f} × ({x[0]:.1f}, {x[1]:.1f})', f'{gW1[1][0]:.4f}, {gW1[1][1]:.4f}'], ['dL/db(1)', 'the two values of delta(1)', f'{gb1[0]:.4f}, {gb1[1]:.4f}']],
                  widths=[2.6, 6.4, 2.8], icons=False,
                  notes=(f'One layer further back. The slope of the loss with respect to hidden output one is the weight that leaves it, point five, times delta two: {W2[0][0] * d2:.4f}. Multiply by the sigmoid slope, a times one minus a, to get delta one for that unit: {d1[0]:.4f}. '
                         f'For unit two the weight is minus point four, so the slope is {W2[0][1] * d2:.4f} and delta one is {d1[1]:.4f}. The sign flips because that weight is negative. '
                         'The gradient of each first-layer weight is delta one times the input it multiplies. The bias gradients are the deltas themselves.')))

    S.append(dict(kind='idea', title='All nine gradients, drawn on the network',
                  visual=dict(kind='d_net', inputs=[f'x1 = {x[0]:.1f}', f'x2 = {x[1]:.1f}'], hidden=[f'delta = {d1[0]:.4f}', f'delta = {d1[1]:.4f}'], out=f'delta = {d2:.4f}',
                              edges1=[[f'{gW1[0][0]:.3f}', f'{gW1[0][1]:.3f}'], [f'{gW1[1][0]:.3f}', f'{gW1[1][1]:.3f}']], edges2=[f'{gW2[0][0]:.3f}', f'{gW2[0][1]:.3f}'], ecolor='#AE2525',
                              foot='Red numbers: dL/d(weight). Boxes: delta. Bias gradients equal the deltas.'),
                  lead='Each red number is the slope of the loss for that weight: the change in loss per unit change in the weight, for a tiny step.',
                  points=['Negative gradient: raise that weight to lower the loss.', 'The output layer has the largest gradients.'],
                  notes=('All nine gradients now sit on the network. The red numbers on the lines are the slopes of the loss for each weight, and the boxes show the deltas, which are also the bias gradients. '
                         'Most gradients are negative, which means: increase those weights and the loss falls. The second hidden unit has positive gradients on its input weights, because its output weight is negative, so lowering those weights helps. '
                         'The gradients nearest the loss are the largest. Do you see how the signs follow from the signs of the output weights?')))

    new_rows = []
    names = ['W(1) row 1, input 1', 'W(1) row 1, input 2', 'W(1) row 2, input 1', 'W(1) row 2, input 2', 'b(1) unit 1', 'b(1) unit 2', 'W(2), hidden 1', 'W(2), hidden 2', 'b(2)']
    olds = [W1[0][0], W1[0][1], W1[1][0], W1[1][1], b1[0], b1[1], W2[0][0], W2[0][1], b2[0]]
    grs = [gW1[0][0], gW1[0][1], gW1[1][0], gW1[1][1], gb1[0], gb1[1], gW2[0][0], gW2[0][1], gb2[0]]
    news = [nW1[0][0], nW1[0][1], nW1[1][0], nW1[1][1], nb1[0], nb1[1], nW2[0][0], nW2[0][1], nb2[0]]
    for nm, o, g, nn in zip(names, olds, grs, news):
        new_rows.append([nm, f'{o:.4f}', f'{g:.4f}', f'{nn:.4f}'])
    S.append(dict(kind='table', title='The update: every parameter moves by minus eta times its gradient, with eta = 0.5',
                  headers=['Parameter', 'Old value', 'Gradient', 'New value = old minus 0.5 × gradient'], rows=new_rows, widths=[3.0, 2.3, 2.3, 4.3], icons=False,
                  notes=(f'The update rule from last session, applied to all nine parameters at once. The new value is the old value minus point five times the gradient. '
                         f'For the first weight, point two minus point five times minus {abs(gW1[0][0]):.4f} gives {nW1[0][0]:.4f}. For the output bias, point two minus point five times minus {abs(gb2[0]):.4f} gives {nb2[0]:.4f}. '
                         'Every parameter with a negative gradient goes up, and the three with positive gradients, all belonging to hidden unit two, go down. Then we run the forward pass again with the new numbers to see whether the loss fell.')))

    S.append(dict(kind='stat', title='After one update the loss falls from 0.3417 to 0.0085', big=f'{red:.0f}%', text=f'of the loss is gone after a single step (rounded to the nearest percent). The new prediction is {s2["yh"]:.4f}, close to the target {y:.1f}.',
                  waffle_label='of the loss removed', source='Computed from the illustrative network of this session. A second step brings the loss to ' + f'{s3["L"]:.4f}.',
                  notes=(f'We run the forward pass again with the new parameters. The prediction is now {s2["yh"]:.4f}, much closer to the target of one. The loss has fallen from {L:.4f} to {s2["L"]:.4f}, which removes about {red:.0f} percent of it in a single step. '
                         f'A second round of the same backward pass and update brings the loss to {s3["L"]:.4f}. You will reproduce all of these numbers in the lab. This is training in miniature: forward, backward, update, repeat. '
                         'A learning rate of point five is large, but this loss surface is gentle enough that it works. What would happen with a learning rate of ten?')))

    S.append(dict(kind='formula', title='In matrix form the same computation uses W, b and delta',
                  formulas=[('Output layer', r'$\delta^{(2)} = \hat{y} - y \qquad \frac{\partial L}{\partial W^{(2)}} = \delta^{(2)}\,a^{(1)T} \qquad \frac{\partial L}{\partial b^{(2)}} = \delta^{(2)}$'),
                            ('Hidden delta', r'$\delta^{(1)} = \left(W^{(2)T}\delta^{(2)}\right) \odot a^{(1)} \odot \left(1 - a^{(1)}\right)$'),
                            ('Hidden gradients', r'$\frac{\partial L}{\partial W^{(1)}} = \delta^{(1)}\,x^{T} \qquad \frac{\partial L}{\partial b^{(1)}} = \delta^{(1)}$')],
                  symbols=[['delta(2), delta(1)', 'The deltas of the output layer and of the hidden layer.', f'{d2:.4f}; ({d1[0]:.4f}, {d1[1]:.4f})'],
                           ['T and \u2299', 'T: transpose (rows become columns). \u2299: multiply entry by entry (Hadamard product).', 'W(2)^T is 2 × 1'],
                           ['∂L/∂W', 'Gradient of the loss L with respect to W: one slope per weight, shaped like W.', '∂L/∂W(1) is 2 × 2']],
                  size=19, widths=[2.0, 6.2, 3.7],
                  notes=('Libraries do the same work in matrix form. The output delta is the prediction minus the target. The gradient of the last weight matrix is that delta times the transpose of the hidden outputs. '
                         'To get the hidden delta, send the output delta backward through the transpose of W two, then multiply entry by entry with the sigmoid slope. The gradient of the first weight matrix is the hidden delta times the transpose of the input. '
                         f'Check it against our numbers: delta two is {d2:.4f}, and delta one is {d1[0]:.4f} and {d1[1]:.4f}, exactly what the tables gave.')))

    S.append(dict(kind='wide', title='The forward pass stores every value, and the backward pass reuses them',
                  visual=dict(kind='d_backprop_flow'),
                  caption='Top: forward pass with the shape of each value. Bottom: backward pass. Gold boxes are the deltas.',
                  notes=('This picture shows why backpropagation is efficient. The forward pass on the top computes each value from the previous one, and we store them all, with their shapes: two by one, two by one, and so on. '
                         'The backward pass on the bottom starts at the right with delta two, and moves left. Each box needs only a stored value from the forward pass and the delta that came before it. '
                         'No part is computed twice. That is the chain rule applied once, from the loss back to the input. Which stored value does the gradient of W two need?')))

    S.append(dict(kind='table', title='Shapes in the matrix form: check them before you code',
                  headers=['Object', 'Shape', 'Why'],
                  rows=[['x, z(1), a(1)', '2 × 1', 'Two inputs, two hidden units'], ['W(1)', '2 × 2', 'One row per hidden unit, one column per input'], ['W(2)', '1 × 2', 'One output, two hidden units'],
                        ['delta(2) and y-hat', '1 × 1', 'One output'], ['delta(1)', '2 × 1', 'One per hidden unit'], ['∂L/∂W(2) = delta(2) a(1)^T', '(1 × 1)(1 × 2) = 1 × 2', 'Same shape as W(2)'],
                        ['∂L/∂W(1) = delta(1) x^T', '(2 × 1)(1 × 2) = 2 × 2', 'Same shape as W(1)']],
                  widths=[3.6, 3.6, 4.7], icons=False,
                  note='Rule: the gradient of a parameter always has the same shape as the parameter. For a batch of n examples the gradients are averaged over the n rows.',
                  notes=('Shapes catch most mistakes. The inputs and the hidden values are two by one. W one is two by two and W two is one by two. The last delta is one by one, and the hidden delta is two by one. '
                         'The gradient for W two is delta two, one by one, times a one transposed, one by two, so it is one by two, the same shape as W two. The same holds for W one. '
                         'The rule to remember: the gradient of a parameter always has the shape of that parameter. If your shapes do not match, a transpose is missing.')))

    S.append(dict(kind='idea', title='Check a gradient with finite differences: nudge one weight and watch the loss',
                  visual=dict(kind='d_finite_diff'),
                  lead='A finite difference estimates a slope from two nearby values of the loss.',
                  points=['Nudge one weight by +h and -h. Keep all others fixed.', 'The red slope should match backpropagation. The check is slow, so it is only a test.'],
                  notes=('How do you know your backward pass is right? Test it. Take one weight, nudge it up by a tiny amount h, and compute the loss. Nudge it down by h and compute the loss again. '
                         'The slope of the red line between those two points is an estimate of the gradient. If your backpropagation is right, the two agree to many decimals. '
                         'This check is slow, because it needs two forward passes for every parameter, so we never use it for training. We use it once, on a small case, to prove the code is right.')))

    fd = n['fd_W1_00']
    S.append(dict(kind='formula', title='The central finite difference, checked on one weight of our network',
                  formulas=[('Central difference', r'$\frac{\partial L}{\partial w} \approx \frac{L(w + h) - L(w - h)}{2h}$')],
                  symbols=[['w', 'The first weight of the first layer, W(1) row 1, input 1.', f'{W1[0][0]:g}'],
                           ['h', 'A tiny nudge.', '0.00001'],
                           ['Finite difference', 'The estimate from the formula.', f'{fd:.10f}'],
                           ['Backpropagation', 'The gradient from the backward pass.', f'{gW1[0][0]:.10f}'],
                           ['Difference', 'The two estimates agree to about 10 decimals.', f'{abs(fd - gW1[0][0]):.1e}']],
                  size=26, note=f'Relative difference = |a - b| / max(|a|, |b|), here {abs(fd - gW1[0][0]) / abs(gW1[0][0]):.0e}. Below about 1e-6 is a good sign.',
                  notes=(f'The check on one real weight, the first weight in the first layer. We nudge it by plus and minus one hundred-thousandth, run the forward pass twice, and divide the difference in loss by two h. '
                         f'The result is {fd:.6f}. Backpropagation gave {gW1[0][0]:.6f}. They agree. This is called the central difference, and it is more accurate than nudging in only one direction. '
                         'In the lab you do this for all nine parameters. If one of them disagrees, you know exactly which formula to look at.')))

    S.append(dict(kind='table', title='Four slips in backpropagation, and the symptom each one leaves',
                  headers=['Mistake', 'What you see', 'Fix'],
                  rows=[['Update the weights before all gradients are computed', 'The gradients of earlier layers are wrong', 'Compute all gradients first, then update everything'],
                        ['Forget the sigmoid slope a × (1 minus a)', 'Hidden gradients are too large and fail the finite-difference check', 'Multiply by a × (1 - a) entry by entry'],
                        ['A missing transpose', 'A shape error in numpy, or a result of the wrong shape', 'The gradient has the shape of its parameter'],
                        ['A sign error in delta(2)', 'The loss goes up after the update', 'delta(2) = y-hat - y, and the update subtracts']],
                  widths=[4.0, 4.0, 3.9], icons=False,
                  notes=('The first slip is updating a weight before you have computed every gradient, which spoils the gradients that use the old values. '
                         'Forgetting the sigmoid slope for the hidden layer, which the finite-difference check catches immediately. A missing transpose, which shows as a shape error. '
                         'And a sign slip in delta two, after which the loss goes up instead of down. The finite-difference test tells you which of these you made, because it points at the parameter that disagrees.')))

    S.append(dict(kind='code', title='Read the training step before you write it: forward, backward, update',
                  code='z1 = W1 @ x + b1\na1 = 1 / (1 + np.exp(-z1))\nyhat = W2 @ a1 + b2\nd2 = yhat - y\nd1 = (W2.T @ d2) * a1 * (1 - a1)\nW2 = W2 - eta * np.outer(d2, a1)\nW1 = W1 - eta * np.outer(d1, x)',
                  reads=['In code, z1, a1, W1 and b1 stand for z(1), a(1), W(1) and b(1); d2 and d1 stand for delta(2) and delta(1).', 'The first three lines are the forward pass; d2 and d1 are the backward pass.', 'np.outer(a, b) is a times b-transposed.', 'The last lines are the update. The biases follow the same pattern.'],
                  notes=('The whole training step fits in seven lines. The first three lines are the forward pass: weighted sum, sigmoid, weighted sum. Then d two is the output delta, and d one sends it backward through the transpose of W two and multiplies by the sigmoid slope. '
                         'The update lines use np dot outer, which builds the delta times transposed input matrix. The bias updates, left out for space, follow the same pattern. '
                         'In the lab you write the forward and backward passes yourself and check them against finite differences.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the concepts. Please close the slides and open the Python notebook or the spreadsheet workbook. Both hold the same network and the same numbers as the slides. '
                         'You will compute the forward pass, the backward pass and the update, check the gradients, and run a second step. For each step, write your prediction first, then run, then read, then change one thing.')))

    S.append(dict(kind='steps', title='Six lab steps: one training step by hand, a proof, then fifty more steps',
                  steps=[dict(head='1 Forward', text='z(1), a(1), y-hat and the loss', icon='pin'), dict(head='2 Backward', text='delta(2), delta(1) and the nine gradients', icon='gear'),
                         dict(head='3 Check', text='Finite differences for every parameter', icon='check'), dict(head='4 Update', text='New parameters, new loss', icon='calculator'),
                         dict(head='5 Repeat', text='A second step, then 50 steps', icon='chart'), dict(head='6 Too large', text='eta = 5: the loss grows', icon='bell')], highlight=2,
                  caption='The notebook has the same six steps. Predict first, run, read, then change one thing.',
                  notes=('The lab has six steps, numbered the same way in the notebook. One, the forward pass: z, a, the prediction and the loss. Two, the backward pass: the two deltas and the nine gradients. '
                         'Three, the finite-difference check, which proves your gradients. Four, the update, and the new loss. Five, a second step, then fifty steps with a plot of the loss. Six, a learning rate of five, to see the loss grow. '
                         'In the spreadsheet the first step is in gold cells and the Train sheet carries your update forward. Predict before you run.')))

    S.append(dict(kind='table', title='Every lab number to four decimals, from the forward pass to the second update',
                  headers=['What you compute', 'You should see'],
                  rows=[['z(1) (both hidden units)', f'{z[0]:.4f} and {z[1]:.4f}'], ['a(1) (both hidden units)', f'{a[0]:.4f} and {a[1]:.4f}'], ['Prediction y-hat, loss L', f'{yh:.4f}, {L:.4f}'],
                        ['delta(2), then delta(1) (two values)', f'{d2:.4f}; {d1[0]:.4f} and {d1[1]:.4f}'], ['Gradient of W(1) row 1 (two values)', f'{gW1[0][0]:.4f} and {gW1[0][1]:.4f}'], ['New W(1) row 1 after the update', f'{nW1[0][0]:.4f} and {nW1[0][1]:.4f}'],
                        ['Loss after one update, after two', f'{s2["L"]:.4f} and {s3["L"]:.4f}']],
                  widths=[6.2, 5.6], icons=False,
                  note='If your number differs, find the step that went wrong. Do not change a number to match.',
                  notes=('The values are rounded to four decimals. If the forward pass matches but delta two does not, look at your sign. '
                         'If delta two matches but delta one does not, look at the sigmoid slope and the transpose. If the gradients match but the new loss is wrong, look at the update. '
                         'Every later step builds on the earlier ones, so stop at the first number that differs and fix it there.')))

    S.append(dict(kind='table', title='When the lab complains: four messages and what each one means',
                  headers=['What you see', 'What it means', 'What to do'],
                  rows=[['ValueError: shapes not aligned', 'A matrix product has the wrong shape', 'Print the shapes. The gradient has the shape of its parameter'],
                        ['Finite-difference check shows a large difference', 'One gradient formula is wrong', 'Compare parameter by parameter to find which one'],
                        ['The loss goes up after the update', 'A sign error, or eta is too large', 'delta(2) = y-hat - y; update is minus eta × gradient'],
                        ['NameError', 'A cell that defines a name was not run', 'Run all cells from the top']],
                  widths=[4.0, 3.9, 4.0], icons=False,
                  notes=('A shape error means a matrix product has the wrong shape, so print the shapes and remember that a gradient has the shape of its parameter. '
                         'A large difference in the finite-difference check means one gradient formula is wrong, so compare parameter by parameter. A loss that rises after the update points to a sign error or a too-large learning rate. '
                         'And a name error means a cell was skipped. Python puts the useful part of an error at the bottom, so read the last line first.')))

    S.append(dict(kind='idea', title='Where this appears in AI: every training step is a forward pass, a loss and a backward pass',
                  visual=dict(kind='d_loop', items=['Take a batch of text', 'Forward pass: probability of each next token', 'Loss: cross-entropy', 'Backward pass: gradients by the chain rule', 'Update: Adam or a similar optimiser'], center='one training step', highlight=3),
                  lead='The loop you did by hand is the loop used for large models.',
                  points=['Published work describes these steps for models of this kind.', 'The steps are the same; the model, its loss (cross-entropy, Session 17) and its size differ. Product designs are not published.'],
                  notes=('This is what happens in every training step of a language model, as described in published work. Take a batch of text. Run the forward pass to get a probability for each next token. '
                         'Compute the loss, which is cross-entropy, a topic for Session 17. Run the backward pass, which gives the gradient of the loss for every parameter by the chain rule. Then an optimiser such as Adam updates the parameters. '
                         'The steps are the ones you did by hand. The model is far larger, with attention layers, and its loss is cross-entropy instead of squared error. The makers of ChatGPT, Gemini and Claude have not published their exact designs, so we describe only the published method.')))

    S.append(dict(kind='wide', title='Where this appears in AI: why training needs far more computing than answering',
                  visual=dict(kind='d_cost'),
                  caption='Illustrative picture. Published analyses count the backward pass as about twice the forward pass.',
                  notes=('Why does training cost so much more than answering a question? There are two reasons, and neither needs a number. First, each training step needs a forward pass and a backward pass. '
                         'Published analyses of transformer training, for example Kaplan and colleagues in 2020, count about two operations per parameter per token for the forward pass and about twice that for the backward pass, so a training step costs roughly three times as much as one answer on the same text. '
                         'Second, training repeats that step a very large number of times, over a very large amount of text. Answering a question needs only the forward pass, once per generated token. Which of the two reasons matters more?')))

    S.append(dict(kind='practice', title='Check an AI assistant with your own numbers', minutes=10, label='Hands-on, with no private data',
                  task='Ask any AI assistant to run the forward pass of our network. Then compare with your table.',
                  steps=[f'Give it x = ({x[0]:.1f}, {x[1]:.1f}), the table of parameters, and target 1. Ask for z, a, y-hat and L.', f'Expected y-hat: {yh:.4f}.', 'If it differs, find the first number that differs.', 'Never paste confidential data.'],
                  output='A note: did the assistant match your table?',
                  notes=('Give any assistant the inputs, the weights and the biases of our network, and ask for the forward pass with target one. '
                         f'The prediction should be {yh:.4f} and the loss {L:.4f}. Assistants sometimes slip on the sigmoid or on a sign, so find the first number that differs from your table. '
                         'Use the assistant to explain, and your own calculation to check. Please never paste confidential data into an assistant. Did it get the sigmoid right?')))

    S.append(dict(kind='table', title='Exit check: three questions with short answers',
                  headers=['Question', 'Short answer'],
                  rows=[['What is delta(2) in this network, in words and as a formula?', 'The slope of the loss with respect to the prediction: y-hat - y. For us it was -0.8267.'],
                        ['Why does the hidden delta contain a × (1 minus a)?', 'It is the slope of the sigmoid. The chain rule multiplies it into the slope that arrives from the output.'],
                        ['Give two reasons training costs more computing than answering.', 'Each step needs a backward pass as well as a forward pass, and training repeats the step a very large number of times. Answering needs one forward pass per generated token.']],
                  widths=[5.2, 6.8], icons=False,
                  notes=('First, delta two is the slope of the loss with respect to the prediction, which is the prediction minus the target. For us it was minus point eight two six seven. '
                         'Second, the hidden delta contains a times one minus a because that is the slope of the sigmoid, and the chain rule multiplies it into the slope that arrives from the output. '
                         'Third, training costs more because every step needs a backward pass as well as a forward pass, and training repeats the step a very large number of times, while answering runs one forward pass per new token. Session 18 reuses these exact formulas for a slightly larger network.')))

    s['facilitator'] = dict(
        prep=['Run the notebook and the workbook once. Check that the Step 1 values match the slide tables.', 'Draw the network on the board with the nine parameters, so learners can point at each gradient.',
              'Print or share the slide "The forward pass, one calculation at a time": learners read from it during the lab.'],
        misconceptions=[('Backpropagation is a different learning algorithm from gradient descent', 'It only computes the gradient. Gradient descent or Adam then uses the gradient to update.'),
                        ('The backward pass runs the network backwards', 'It runs the chain rule backwards, reusing values stored in the forward pass.'),
                        ('A larger network needs a different method', 'The same two passes are used for every size.'),
                        ('Finite differences could replace backpropagation', 'They need two forward passes per parameter, far too slow for billions of parameters. They are a test only.')],
        probes=[('Why do we store the forward values?', 'The backward pass needs a(1) and the sigmoid slopes. Recomputing them would repeat work.'),
                ('Which gradients are the largest here, and why?', 'The output layer, because they are closest to the loss and are not multiplied by the small sigmoid slopes.'),
                ('What would change with a ReLU instead of a sigmoid?', 'The slope a × (1 - a) becomes 1 where z > 0 and 0 elsewhere.'),
                ('Why check with finite differences only once?', 'It is slow. One pass on a small case is enough to prove the code is right.')],
        lab_steps=[('Python: forward (step 1)', f'z(1) = ({z[0]:.4f}, {z[1]:.4f}), y-hat = {yh:.4f}, loss {L:.4f}. Spreadsheet: gold cells in the Step 1 forward block.'),
                   ('Python: backward (step 2)', f'delta(2) = {d2:.4f}; delta(1) = ({d1[0]:.4f}, {d1[1]:.4f}). Common slip: forgetting a × (1 - a).'),
                   ('Python: finite differences (step 3)', 'The largest difference is below 1e-8. Learners who see a large one have a wrong formula. Spreadsheet: compare the gold gradient cells with the given ones in the check table.'),
                   ('Python: update and repeat (steps 4 and 5)', f'Loss after one update {s2["L"]:.4f}; after two {s3["L"]:.4f}. Spreadsheet: Train row 1 copies the learner\'s update, so a wrong update shows up in the later rows.'),
                   ('Python: eta = 5 (step 6)', 'After one update the loss is 16.28, then 317, 5078: from the third step it grows exactly 16-fold every step.')],
        rescue=['If the matrix form takes too long, stay with the scalar tables and show the matrix formulas only as a summary.', 'If a learner has no Python, do the spreadsheet: it has the same values.',
                'If time runs short, skip the 50-step plot: steps 1 to 4 are enough for the checks.'],
        after=['Share the solution notebook with absent learners.', 'Ask learners to bring one question about overfitting for Session 12.'],
        lab_answer_key=[['PREDICT: is y-hat bigger or smaller than the target 1?', 'Smaller: 0.1733.'], ['READ: why are most gradients negative?', 'The prediction is below the target, so raising most parameters lowers the loss.'],
                        ['PREDICT (step 3): how close are finite differences and backpropagation?', 'Within 0.0000001: the largest difference is about 1e-11.'],
                        ['PREDICT (step 5): near which factor does the fall settle?', 'Near 60: the ratios are 40, 54, 64, then about 65.6 at every step.'],
                        ['CHANGE (steps 6 and the sheet): use eta = 5', 'The loss explodes: 0.34, 16.3, 317, 5078, 81240, growing about 16-fold every step from the third. Put eta back to 0.5 afterwards.'],
                        ['CHANGE: remove a × (1 - a) in delta(1)', 'The finite-difference check fails for the first-layer weights.']])
    return s
