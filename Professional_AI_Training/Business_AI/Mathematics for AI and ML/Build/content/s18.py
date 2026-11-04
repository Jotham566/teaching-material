"""Session 18: course project, five builds from first principles (author F). Every number comes from the solution notebook (labs/s18_nb.py)."""
import importlib.util
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def _mod():
    spec = importlib.util.spec_from_file_location('s18_nb_deck', HERE / 'labs' / 's18_nb.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def build():
    M = _mod()
    N = M.namespace()
    E = M.example()
    nchk = M.n_checks()
    f = lambda a: [round(float(v), 4) for v in np.ravel(a)]
    w_n, mse, p7 = f(N['w_normal']), float(N['mse']), float(N['pred_7'])
    w5, l5 = f(N['w5']), float(N['loss5'])
    ev, pc1, ratio = f(N['eigvals']), f(N['pc1']), float(N['ratio'])
    p0, loss0, p1, lnn = f(N['p0']), float(N['loss0']), f(N['p1']), float(N['loss_nn'])
    Wt, Wa, Wo = np.array(N['weights']), np.array(N['scores']), np.array(N['out'])
    spread = float(N['spread_unscaled'])
    # worked single example for the network slide (input (1, 2), target 1; not an XOR row)
    h, z2, p, d, gW2 = E['h'], E['z2'], E['p'], E['delta'], E['gW2']
    # logistic table
    xl, yl = np.array(N['xl']), np.array(N['yl'])
    Xl = np.column_stack([np.ones(8), xl])
    sig = lambda z: 1 / (1 + np.exp(-z))
    wlist, w = [], np.zeros(2)
    for s_ in range(6):
        pr = sig(Xl @ w)
        wlist.append((s_, w.copy(), float(-np.mean(yl * np.log(pr) + (1 - yl) * np.log(1 - pr)))))
        w = w - 0.1 * Xl.T @ (pr - yl) / 8
    pts = [(float(a), float(b)) for a, b in zip(N['x'], N['y'])]
    xbar, ybar = float(np.mean(N['a'])), float(np.mean(N['b']))
    slope = pc1[1] / pc1[0]
    pca_pts = [(float(a), float(b)) for a, b in zip(N['a'], N['b'])]
    tok = ['Token 1', 'Token 2', 'Token 3']
    ev_n1 = [v * 10 / 9 for v in ev]          # the same eigenvalues if we divided by n - 1
    fm = lambda M_: '(' + '), ('.join(', '.join(f'{v:g}' for v in row) for row in np.atleast_2d(M_)) + ')'

    s = dict(
        num=18, block='Course project', short_title='Course project',
        title='Course project: five builds from first principles, from linear regression to attention',
        question='Can five small builds, written from first principles, reproduce the core of what runs inside modern AI?',
        outcomes=['Build linear regression (normal equation and gradient descent) and logistic regression (gradient descent) with numpy',
                  'Build PCA from the covariance eigen-decomposition and a 2-4-1 neural network with backpropagation',
                  'Build scaled dot-product attention for three tokens, and see OK on the automatic self-checks of your project'],
        outcome_icons=['chart', 'gear', 'check'],
        outcome_note=('By the end of today you can build five things from first principles. Linear regression, with the normal equation and with gradient descent. Logistic regression, with gradient descent. '
                      'PCA, from the eigen-decomposition of the covariance matrix. A small neural network, two inputs, four hidden units and one output, with backpropagation. And scaled dot-product attention for three tokens. '
                      'In the notebook the text you type as a student ID makes your own personal data, and automatic self-checks show OK or NOT YET for each build. There are no marks. The project is yours to keep.'),
        clock=[(10, 'Recall, then a real question from AI'), (35, 'Concept: a picture, then one example by hand'), (10, 'Break'), (45, 'Lab in Python or a spreadsheet: predict, run, change one thing'),
               (15, 'Where this appears in AI, and an exit check'), (5, 'Save the work')],
        plan_title='Your two hours: a guided tour, then your project',
        plan_caption='The tour first. Then your project, with self-checks and no marks. Then AI.',
        plan_note=('Today is the last session. Ten minutes of recall from Session 17. Thirty-five minutes of guided tour of the five builds, with the maths of each on a formula slide and a hand example. A ten minute break. '
                   'Then forty-five minutes on your project. The project is the notebook, which you build with your own personal data and keep. Nothing is marked: the checks only show you what works. The spreadsheet is a guided version with the same five builds. We finish with where this appears in AI, what to learn next, and saving your work.'),
        recall_from='Session 17',
        recall=[('How are cross-entropy, entropy and KL divergence related?', 'Cross-entropy = entropy + KL divergence. The entropy is fixed by the data, so lowering the cross-entropy lowers the KL divergence.'),
                ('What is the gradient of softmax with cross-entropy with respect to the logits?', 'The prediction minus the target: p - y.'),
                ('What does a perplexity of 5 mean?', 'The model is as unsure as if it chose among about five equally likely words at each step.')],
        words=[('Normal equation', 'The direct formula w = (X^T X)^-1 X^T y that gives the least squares weights.'),
               ('Principal component', 'A direction of largest spread in the data: an eigenvector of the covariance matrix.'),
               ('Backpropagation', 'The chain rule applied backwards through a network to get the gradient of the loss for every weight.'),
               ('Query, key, value', 'The three vectors each token makes in attention: what it looks for, what it offers and what it passes on.'),
               ('Attention', 'Each token takes a weighted average of the value vectors, with weights from softmax(Q K^T / sqrt(d)).')],
        word_icons=['calculator', 'chart', 'gear', 'key', 'magnifier'],
        words_note=('Five words for today. The normal equation is the direct formula for least squares. A principal component is a direction of largest spread, an eigenvector of the covariance matrix. '
                    'Backpropagation is the chain rule applied backwards through a network. Query, key and value are the three vectors each token makes in attention. '
                    'And attention is a weighted average of the values, with the weights coming from a softmax. We use each of them today.'),
        keep='Keep your finished project notebook, ideally with all self-checks OK, and write your one-page formula sheet: every formula named in plain words and in the industry term.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your project', value='Self-checks OK'), dict(label='Formula sheet', value='One page'),
                                                              dict(label='Next', value='Machine Learning at KLAi'), dict(label='Then', value='Deep learning')]),
        keep_title='Save your project and write your formula sheet',
        next='Machine Learning at KLAi, then deep learning (to be confirmed).', next_label='What to learn next',
        keep_note=('This is the end of the course, so before you go do two things. Run your project from the top, look at the self-checks and save it. It is yours to keep, and nothing is marked. '
                   'Then write your one-page formula sheet, with every formula named in plain words and in the industry term. It is the page you will use when you read a paper or a library manual. '
                   'Thank you for eighteen sessions. What was the one idea you will remember?'),
        keep_returns=True,
        cover_note=('Welcome to the last session. For seventeen sessions you collected tools: vectors, matrices, eigenvalues, gradients, probability, likelihood, entropy. Today we use them. '
                    'In one session you build linear regression, logistic regression, PCA, a small neural network and attention from first principles. The question is whether such small builds contain the core of modern AI.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 17', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.0, 7.0], icons=False,
                  note='All three come back today: p - y trains the network, and the softmax is inside attention.',
                  notes=('Here are the short answers. Cross-entropy equals entropy plus KL divergence, and because the entropy is fixed by the data, lowering the cross-entropy lowers the KL. '
                         'The gradient of softmax with cross-entropy with respect to the logits is the prediction minus the target. And a perplexity of five means the model is as unsure as if it chose among about five equally likely words. '
                         'Today the second answer trains our network, and the softmax appears inside attention. Which of the three would you like to hear again?')))

    S.append(dict(kind='wide', title='Five builds, and each one uses mathematics you already know',
                  visual=dict(kind='icons', items=[dict(icon='chart', head='Linear regression', text='Linear systems and least squares'), dict(icon='check', head='Logistic regression', text='Gradient descent and cross-entropy'),
                                                   dict(icon='magnifier', head='PCA', text='Covariance, eigenvalues, eigenvectors'), dict(icon='gear', head='Neural network', text='Chain rule and backpropagation'),
                                                   dict(icon='key', head='Attention', text='Matrices, dot products and softmax')]),
                  caption='Illustrative data. Each build is about ten lines of numpy.',
                  notes=('This is the plan for today in one picture. Linear regression uses what we learned about linear systems and least squares. Logistic regression uses gradient descent and the cross-entropy loss. '
                         'PCA uses the covariance matrix and its eigenvalues and eigenvectors. The neural network uses the chain rule, which is backpropagation. And attention uses matrix multiplication, dot products and the softmax. '
                         'Each build is about ten lines of numpy, and all of the data are made up to show the arithmetic. Which of the five do you expect to be hardest?')))

    S.append(dict(kind='table', title='The illustrative data of Builds 1 to 3 (made-up numbers to show the arithmetic)',
                  headers=['Build', 'Data'],
                  rows=[['1 Linear', 'Hours x = 1, 2, 3, 4, 5, 6. Energy y (kWh) = 2.2, 2.9, 4.1, 5.2, 5.8, 7.1.'],
                        ['2 Logistic', 'Hours x = 1 to 8. Passed y = 0, 0, 0, 1, 0, 1, 1, 1.'],
                        ['3 PCA', 'a = 2.5, 0.5, 2.2, 1.9, 3.1, 2.3, 2.0, 1.0, 1.5, 1.1. b = 2.4, 0.7, 2.9, 2.2, 3.0, 2.7, 1.6, 1.1, 1.6, 0.9.']],
                  widths=[2.2, 9.4], icons=False, note='These fixed numbers are for the slides and the guided workbook. In the notebook your student ID makes your own different data.',
                  notes=('Here is every number that the first three guided builds use, so you can recompute them from these slides alone. Build one has six readings of hours and energy. Build two has eight students with hours of study and pass or fail. '
                         'Build three has ten points in two columns, a and b. These numbers are made up to show the arithmetic. In the notebook the text you type as a student ID makes your own, different data. Which build has the most numbers to check?')))

    S.append(dict(kind='table', title='The illustrative data of Builds 4 and 5',
                  headers=['Build', 'Data'],
                  rows=[['4 Network', 'W1 rows (0.5, -0.3), (0.2, 0.8), (-0.6, 0.4), (0.1, -0.9). b1 = 0. W2 = (0.3, -0.5, 0.7, 0.2). b2 = 0.1.'], ['4 XOR rows', 'Inputs (0, 0), (0, 1), (1, 0), (1, 1) with targets 0, 1, 1, 0.'],
                        ['5 Attention', 'X rows (1, 0), (0, 1), (1, 1). Wq rows (1, 0), (1, 1). Wk rows (1, 1), (0, 1). Wv rows (1, 0), (0, 2). d = 2.']],
                  widths=[2.2, 9.4], icons=False, note='Q = X Wq, K = X Wk and V = X Wv give three rows of two numbers each.',
                  notes=('And here are the numbers for builds four and five. The network starts from these weights: a four by two matrix W one, a zero bias b one, four output weights W two and an output bias of 0.1. The four XOR rows have targets zero, one, one, zero. '
                         'For attention, X has one row per token, and three small matrices make the queries, keys and values. The key length d is two. With these you can recompute every number on the next slides by hand. '
                         'Which of the matrices would you check first?')))

    S.append(dict(kind='formula', title='Build 1: linear regression has a direct solution and an iterative one',
                  formulas=[('Normal equation', r'$w=(X^{T}X)^{-1}X^{T}y$'), ('Gradient descent step', r'$w\leftarrow w-\eta\,\frac{2}{n}X^{T}(Xw-y)$')],
                  symbols=[['X', 'The design matrix: a column of ones, then x.', '6 rows by 2 columns'], ['w', 'The weights: intercept w0 and slope w1.', f'({w_n[0]:g}, {w_n[1]:g})'], ['eta', 'The learning rate.', '0.02'],
                           ['n', 'The number of rows.', '6']],
                  size=24, note=f'Same weights from both. MSE {mse:.4f}. 7 hours (beyond the data) predicts {p7:.2f} kWh.',
                  notes=('Build one is linear regression. The model predicts X times w, where X has a column of ones so that w zero is the intercept. The normal equation solves the least squares problem in one line: w equals the inverse of X transpose X, times X transpose y. '
                         f'Gradient descent reaches the same answer by small steps, using the gradient two over n times X transpose times the residual. For our six illustrative points both give an intercept of {w_n[0]:g} and a slope of {w_n[1]:g}. '
                         f'The mean squared error is {mse:.4f}. Seven hours of use is outside the data, which stops at six, so that prediction of {p7:.2f} kilowatt-hours is an extrapolation. Why does the column of ones matter?')))

    S.append(dict(kind='idea', title='Build 1 in a picture: the fitted line and its residuals',
                  visual=dict(kind='scatter', points=pts, xlabel='hours of use', ylabel='energy used (kWh)', line=(w_n[0], w_n[1]), residuals=True),
                  lead=f'The line is y-hat = {w_n[0]:g} + {w_n[1]:g} x. The red segments are the residuals.',
                  points=['Illustrative data: x = 1 to 6 hours, y = 2.2, 2.9, 4.1, 5.2, 5.8, 7.1 kWh.', 'The normal equation and gradient descent give the same line.'],
                  notes=(f'Here is build one as a picture. Six points, and the least squares line with intercept {w_n[0]:g} and slope {w_n[1]:g}. The red segments are the residuals, the gaps between the points and the line. '
                         'Least squares chooses the line that makes the sum of their squares as small as possible. In Session 16 you saw that this is also maximum likelihood under Gaussian noise. '
                         'The data are illustrative. Which point has the largest residual?')))

    S.append(dict(kind='formula', title='Build 2: logistic regression is a sigmoid on a linear score, trained by gradient descent',
                  formulas=[('Model', r'$p=\sigma(w_0+w_1x)=\frac{1}{1+e^{-(w_0+w_1x)}}$'), ('Gradient descent step', r'$w\leftarrow w-\eta\,\frac{1}{n}X^{T}(p-y)$')],
                  symbols=[['p', 'The predicted probability of class 1 (passed).', '0.5 at the start'], ['p - y', 'The prediction minus the target, as in Session 17.', 'one value per row'], ['eta', 'The learning rate.', '0.1'],
                           ['Loss', 'Binary cross-entropy, from Session 16.', f'{wlist[0][2]:.3f} at the start']],
                  size=22, note=f'After 5 steps: w = ({w5[0]:g}, {w5[1]:g}), loss {l5:.3f}. Data: 8 students (see the data slide).',
                  notes=('Build two is logistic regression. The model passes a linear score through the sigmoid, so the output is a probability between zero and one. The loss is the binary cross-entropy from Session 16. '
                         'Its gradient is wonderfully simple, and you already derived it in Session 17: the average of the prediction minus the target, times the inputs. '
                         f'Starting from zero weights every probability is one half and the loss is {wlist[0][2]:.3f}. After five steps with a learning rate of 0.1 the weights are {w5[0]:g} and {w5[1]:g}, and the loss has fallen to {l5:.3f}. '
                         'The data are eight illustrative students: hours of study and pass or fail.')))

    S.append(dict(kind='table', title='Build 2 by hand: the loss falls at every one of the first five gradient steps',
                  headers=['Step', 'w0', 'w1', 'Loss'], rows=[[str(i), f'{round(float(w_[0]), 4) + 0.0:.4f}', f'{round(float(w_[1]), 4) + 0.0:.4f}', f'{lo:.4f}'] for i, w_, lo in wlist], widths=[2.0, 3.0, 3.0, 3.0], icons=False,
                  note='Learning rate 0.1. Step 0 is the start. The workbook has the same table.',
                  notes=(f'Here are the first five gradient steps. Step zero is the start, with both weights at zero and a loss of {wlist[0][2]:.4f}. At step one the intercept stays at zero, because half the students passed and the average of p minus y for the intercept is zero, but the slope moves up. '
                         f'The loss falls at every step, to {wlist[5][2]:.4f} after five. In the lab you let it run for five thousand steps, and in the workbook you fill this same table with formulas. '
                         'What would happen to the table if the learning rate were 2?')))

    S.append(dict(kind='idea', title='Build 3: PCA finds the direction of largest spread in the data',
                  visual=dict(kind='scatter', points=pca_pts, xlabel='a', ylabel='b', line=(ybar - slope * xbar, slope)),
                  lead=f'The red line is the first principal component. It holds {ratio * 100:.1f} percent of the variance.',
                  points=[f'Eigenvalues of the covariance matrix: {ev[1]:.3f} and {ev[0]:.3f}.', f'First component: ({pc1[0]:.3f}, {pc1[1]:.3f}).'],
                  notes=(f'Build three is PCA, principal component analysis. Ten illustrative points in two dimensions. The two columns rise together, so the spread is mostly along one diagonal direction, the red line. '
                         f'That direction is the first principal component. The covariance matrix has two eigenvalues, {ev[1]:.3f} and {ev[0]:.3f}, so the first component holds {ratio * 100:.1f} percent of the total variance. '
                         'If we keep only the position of each point along that line, one number instead of two, we lose very little. Why does the spread across the line matter less?')))

    S.append(dict(kind='formula', title='PCA as formulas: centre, form the covariance, find its eigenvectors, project',
                  formulas=[('Covariance matrix (divide by n)', r'$C=\frac{1}{n}X_c^{T}X_c$'), ('Eigenvector and score', r'$Cv=\lambda v,\qquad \mathrm{score}=X_c\,v_1$')],
                  symbols=[['X_c', 'The data with each column centred on its mean.', '10 rows by 2 columns'], ['lambda', 'An eigenvalue: the variance along its eigenvector.', f'{ev[1]:.3f} and {ev[0]:.3f}'],
                           ['v_1', 'The eigenvector with the largest eigenvalue: the first component.', f'({pc1[0]:.3f}, {pc1[1]:.3f})'], ['n', 'The number of points.', '10']],
                  size=24, note=f'Libraries divide by n - 1: eigenvalues {ev_n1[1]:.3f} and {ev_n1[0]:.3f}, the same {ratio * 100:.1f} percent share.',
                  notes=('Here is PCA as formulas. First centre each column on its mean. Then the covariance matrix is X c transpose times X c, divided by n, the convention of this course. Its eigenvectors are the principal components, and each eigenvalue is the variance along its eigenvector. '
                         f'For our data the largest eigenvalue is {ev[1]:.3f}, with eigenvector {pc1[0]:.3f} and {pc1[1]:.3f}. The score of a point is its centred row times that eigenvector. '
                         'Many libraries divide by n minus one instead. The eigenvalues are then a little larger, but the share of variance and the eigenvectors are the same. The singular value decomposition of the centred data gives the same eigenvectors.')))

    S.append(dict(kind='idea', title='Build 4: a 2-4-1 network has two layers of weights, and the error flows back',
                  visual=dict(kind='f_network', layers=(('Inputs', 2), ('Hidden (tanh)', 4), ('Output', 1))),
                  lead='Two inputs, four hidden units, one output. The task is XOR: 1 when exactly one input is 1.',
                  points=['Forward: h = tanh(W1 x + b1), then p = sigmoid(W2 h + b2). Loss: binary cross-entropy.', 'Backward: the chain rule passes the error signal back, layer by layer.'],
                  notes=('Build four is a small neural network, two inputs, four hidden units and one output. The task is XOR, answer one when exactly one of the inputs is one. '
                         'A straight line cannot solve XOR, which is why we need the hidden layer. The forward pass computes the hidden activations with tanh, then the output probability with a sigmoid. '
                         'The backward pass is backpropagation, the chain rule applied from the output back to the first layer. We use the binary cross-entropy loss, so the first backward quantity is the familiar p minus y. Why does XOR need a hidden layer?')))

    S.append(dict(kind='formula', title='Backpropagation for the 2-4-1 network, in matrix algebra',
                  formulas=[('Forward and loss', r'$h=\tanh(W_1x+b_1),\ \ p=\sigma(W_2h+b_2),\ \ L=-[\,y\ln p+(1-y)\ln(1-p)\,]$'),
                            ('Backward', r'$\delta=p-y,\ \ g_{W_2}=\delta\,h^{T},\ \ g_{b_2}=\delta,\ \ \delta_h=(W_2^{T}\delta)\odot(1-h^{2}),\ \ g_{W_1}=\delta_h\,x^{T},\ \ g_{b_1}=\delta_h$')],
                  symbols=[['delta', 'The error signal at the output. For a sigmoid with binary cross-entropy it is p - y.', f'{d:.4f} in the example'], ['delta_h', 'The error signal arriving at each hidden unit.', 'one value per unit'],
                           ['1 - h^2', 'The slope of tanh at each hidden unit (chain rule).', f'({", ".join(f"{1 - v * v:.3f}" for v in h)})'], ['odot', 'Multiply entry by entry.', 'unit by unit']],
                  size=18, note='Update with learning rate eta: each weight matrix and bias becomes W - eta × its gradient.',
                  notes=('Here is backpropagation in matrix algebra. The forward pass and the loss are on top, the binary cross-entropy. Below, the first backward line says the error signal at the output, delta, is p minus y, as in Session 17. '
                         'That holds for a sigmoid output with this loss. The gradient for the second weight matrix is delta times the hidden activations, and the gradient for its bias is delta. '
                         'The error signal then flows back through the second matrix and is multiplied entry by entry by one minus h squared, the slope of tanh. That gives delta h at the hidden layer, and the gradient for the first weight matrix is delta h times the input. '
                         'Each weight matrix and bias is then updated by subtracting the learning rate times its gradient.')))

    S.append(dict(kind='example', title='By hand: one forward and one backward step for the input (1, 2) with target 1',
                  scenario='One illustrative example (not an XOR row), from the starting weights on the data slide. The notebook trains on many rows and averages their gradients.',
                  blocks=[dict(label='Forward', text=f'h = ({", ".join(f"{v:.3f}" for v in h)}), z2 = {z2:.4f}, p = {p:.4f}'), dict(label='Loss', text=f'-ln p = {-math.log(p):.4f}'),
                          dict(label='Backward', text=f'delta = p - y = {d:.4f}. g_W2 = delta × h = ({", ".join(f"{v:.3f}" for v in gW2)}). First row of g_W1 = ({E["gW1"][0, 0]:.3f}, {E["gW1"][0, 1]:.3f})'),
                          dict(label='Update', text=f'W2 first weight: 0.3 - 0.5 × ({gW2[0]:.3f}) = {0.3 - 0.5 * gW2[0]:.3f}', red=True)],
                  notes=(f'Let us put numbers in. The input is one and two, the target is one. With the starting weights on the data slide the four hidden activations are {h[0]:.3f}, {h[1]:.3f}, {h[2]:.3f} and {h[3]:.3f}. The output probability is {p:.4f}, so the loss is {-math.log(p):.4f}. '
                         f'The error signal delta is p minus y, {d:.4f}. The gradient for the output weights is delta times h. With a learning rate of 0.5 the first output weight moves from 0.3 to {0.3 - 0.5 * gW2[0]:.3f}. '
                         f'The first row of the gradient of W1 is {E["gW1"][0, 0]:.3f} and {E["gW1"][0, 1]:.3f}, and the second is twice the first because the second input is 2. The workbook has this exact example in cells. Which sign tells you the weight should go up?')))

    S.append(dict(kind='table', title='After 5,000 gradient steps the toy network solves XOR (guided example)',
                  headers=['Input', 'Target', 'Output before training', 'Output after training'], rows=[['(0, 0)', '0', f'{p0[0]:.3f}', f'{p1[0]:.4f}'], ['(0, 1)', '1', f'{p0[1]:.3f}', f'{p1[1]:.4f}'], ['(1, 0)', '1', f'{p0[2]:.3f}', f'{p1[2]:.4f}'], ['(1, 1)', '0', f'{p0[3]:.3f}', f'{p1[3]:.4f}']],
                  widths=[2.4, 2.0, 3.8, 3.8], icons=False, note=f'The loss falls from {loss0:.3f} to {lnn:.4f}. Learning rate 0.5.',
                  notes=(f'Here is what training does. Before training all four outputs are close to one half, between {min(p0):.2f} and {max(p0):.2f}, and the loss is {loss0:.3f}. '
                         f'After five thousand steps of gradient descent the outputs are near zero for the first and last inputs and near one for the middle two, and the loss is {lnn:.4f}. The network has learned XOR, which no single straight line can do. '
                         'In the notebook the self-checks compare your backward function with a numeric gradient, on your own data.')))

    S.append(dict(kind='wide', title='Build 5: attention gives every token a weighted average of the value vectors',
                  visual=dict(kind='f_attention', tokens=tok, weights=Wt.tolist(), outputs=Wo.tolist(), note=f'Illustrative numbers. Token 3 reads {Wt[2, 0] * 100:.0f} percent from token 1, {Wt[2, 1] * 100:.0f} from token 2 and {Wt[2, 2] * 100:.0f} from token 3.'),
                  caption='Each row of weights adds to 1. The output is the weights times the value vectors.',
                  notes=('Build five is attention, the core step inside the transformer. Each token asks a question, a query, and every token offers a key. The score between a query and a key says how much that token should read from that one. '
                         f'The grid shows the attention weights after a softmax along each row, so each row adds to one. Darker gold means a larger weight. Token three, in the last row, reads {Wt[2, 0] * 100:.0f} percent from token one, {Wt[2, 1] * 100:.0f} from token two and {Wt[2, 2] * 100:.0f} from itself. '
                         'On the right, the output is that weighted average of the value vectors. The numbers are made up to show the arithmetic.')))

    S.append(dict(kind='formula', title='Attention as a formula: every symbol named',
                  formulas=[('Projections', r'$Q=XW_Q,\qquad K=XW_K,\qquad V=XW_V$'), ('Attention', r'$\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\left(\frac{QK^{T}}{\sqrt{d_k}}\right)V$')],
                  symbols=[['X', 'One row per token: its embedding.', '3 tokens, 2 numbers each'], ['W_Q, W_K, W_V', 'Weight matrices that make queries, keys and values.', 'learned in a real model'],
                           ['Q, K, V', 'Queries (what a token looks for), keys (what it offers), values (what it passes on).', 'each 3 by 2'], ['d_k', 'The length of a key vector.', '2'],
                           ['softmax', 'Applied along each row, so each row adds to 1.', 'weights 0.401, 0.198, 0.401']],
                  size=20, note='Vaswani et al. (2017): large dot products saturate the softmax, so its gradient is tiny.',
                  notes=('Here is the formula for scaled dot-product attention, as published by Vaswani and colleagues in 2017. Each token embedding in X is multiplied by three weight matrices to give queries, keys and values. '
                         'Q times K transpose gives a score for every pair of tokens. We divide by the square root of d k, the length of a key vector, then apply a softmax along each row, so each row of weights adds to one. '
                         'Finally the weights multiply V. The published reason for the square root is that for large d k the dot products grow large and push the softmax into a saturated region, where almost all the weight goes to one token and the gradient is tiny. A simulation in the following picture shows the size of the scores.')))

    S.append(dict(kind='idea', title='Why divide by the square root of d: dot products of long vectors grow, and the softmax saturates',
                  visual=dict(kind='bars', items=[dict(label='Standard deviation of q . k, d = 64, unscaled', value=round(spread, 1), dark=True), dict(label='After dividing by sqrt(64) = 8', value=round(spread / 8, 1), hl=True)], unit=''),
                  lead='If the entries of q and k are independent with mean 0 and standard deviation 1, then q . k has mean 0 and standard deviation sqrt(d).',
                  points=['Large scores make the softmax saturate: almost all the weight goes to one token (nearly one-hot), and the gradient is tiny.', 'Dividing by sqrt(d_k) keeps the standard deviation near 1. The notebook simulates 2,000 pairs.'],
                  notes=(f'Why divide by the square root of d? Take two random vectors of length 64, whose entries are independent with mean zero and standard deviation one. Their dot product is a sum of 64 terms, so its standard deviation is about the square root of 64, which is 8. In a simulation of two thousand pairs I get {spread:.1f}. '
                         'Scores of that size would make the softmax saturate, nearly one-hot, and in that region its gradient is tiny, so training would be slow. Dividing by the square root of d brings the standard deviation back to about one. '
                         'This is the reason given in the original paper. You check the simulation in the notebook.')))

    S.append(dict(kind='table', title='By hand: scaled scores, weights and output for three tokens (d = 2)',
                  headers=['Token', 'Scaled scores', 'Weights', 'Output'],
                  rows=[[f'Token {i + 1}', ', '.join(f'{v:.3f}' for v in Wa[i]), ', '.join(f'{v:.3f}' for v in Wt[i]), ', '.join(f'{v:.3f}' for v in Wo[i])] for i in range(3)],
                  widths=[1.6, 4.0, 4.0, 2.6], icons=False, note='Illustrative. Scores = Q K^T / sqrt(2). Weights = softmax of each row. Output = weights times V.',
                  notes=(f'Here are the numbers. The scaled scores for token one are {Wa[0, 0]:.3f}, {Wa[0, 1]:.3f} and {Wa[0, 2]:.3f}. The softmax of that row gives the weights {Wt[0, 0]:.3f}, {Wt[0, 1]:.3f} and {Wt[0, 2]:.3f}, which add to one. '
                         f'Multiplying the weights by the three value vectors gives the output for token one, {Wo[0, 0]:.3f} and {Wo[0, 1]:.3f}. Token three has the largest score for itself, {Wa[2, 2]:.3f}, so it gives itself the largest weight, {Wt[2, 2]:.3f}. '
                         'In the workbook the softmax is built in cells with the stable trick of subtracting the row maximum.')))

    S.append(dict(kind='compare', title='Three slips that the self-checks will catch',
                  left=dict(head='The slip', points=['No column of ones, so no intercept.', 'PCA without centring the data first.', 'Softmax along the wrong axis, or no sqrt(d).']),
                  right=dict(head='The fix', points=['Add the column of ones to X.', 'Subtract each column mean first.', 'Softmax along each row, then divide scores by sqrt(d_k).']),
                  verdict='Each check names its build, so read the name first.',
                  notes=('Here are three slips that the checks will catch. In linear regression, forgetting the column of ones means there is no intercept. In PCA, forgetting to centre the data means the covariance is wrong. '
                         'In attention, applying the softmax down the columns gives rows of weights that do not add to one, and forgetting the square root of d changes every weight. '
                         'When a check fails, its name tells you which build to look at. Which of these would you have made?')))

    S.append(dict(kind='code', title='Read the five recipes before you write them',
                  code='w = np.linalg.solve(X.T @ X, X.T @ y)\nw = w - lr * X.T @ (sigmoid(X @ w) - y) / n\nvals, vecs = np.linalg.eigh(Dc.T @ Dc / n)\ngW1 = dh.T @ X\nout = softmax_rows(Q @ K.T / np.sqrt(d)) @ V',
                  reads=['Build 1: the normal equation in one line.', 'Build 2: one gradient step of logistic regression.', 'Build 3: eigh returns the eigenvalues smallest first, so take the last column. The sign of an eigenvector is arbitrary.', 'Build 4: a gradient from backpropagation.', 'Build 5: the attention formula.',
                         'Spreadsheet: MMULT, MINVERSE, TRANSPOSE and SUMPRODUCT.'],
                  notes=('Before your project, read the five recipes. Build one, the normal equation in a single line with solve. Build two, one gradient step of logistic regression, the p minus y again. '
                         'Build three, the eigen-decomposition of the covariance matrix with eigh. Build four, a gradient from backpropagation, here the gradient of the first weight matrix. Build five, the attention formula in one line. '
                         'In the spreadsheet the same steps use MMULT, MINVERSE, TRANSPOSE and SUMPRODUCT. The notebook asks you to write the functions that these lines sit in.')))

    S.append(dict(kind='divider', title='Part 2: your project', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the tour. The project is yours. Open the notebook or the workbook and work through the five builds in order. '
                         'Every self-check names its build, so you can see which one needs work. You may use your notes and earlier notebooks, and you may talk with your neighbour. Nothing is marked. '
                         'Raise your hand if something does not run, and I will help you read the error message. Good luck.')))

    S.append(dict(kind='steps', title='Your project has five builds, and every self-check names its build',
                  steps=[dict(head='1 Linear', text='fit_linear, fit_linear_gd', icon='chart'), dict(head='2 Logistic', text='sigmoid, logistic_loss, fit_logistic', icon='check'), dict(head='3 PCA', text='first component, variance share', icon='magnifier'),
                         dict(head='4 Network', text='mlp_forward, mlp_backward, mlp_train', icon='gear'), dict(head='5 Attention', text='softmax_rows, attention', icon='key')],
                  caption=f'Python: {nchk} checks, each run on your own data and on a second dataset. No marks. Spreadsheet: a guided version with fixed toy numbers.',
                  notes=(f'Here are the five builds in the order you will do them, with the names of the functions you write. In the notebook there are {nchk} self-checks. Each one runs your function on your own data and on a second dataset, and every check begins with the name of its build. '
                         'Build one is linear regression. Build two is logistic regression. Build three is PCA. Build four is the network, where you write the forward pass, the backward pass and the training function. Build five is attention. '
                         'The notebook ends with a cell that says how many checks pass. Work in order, because later builds reuse earlier ideas, like p minus y and the sigmoid.')))

    S.append(dict(kind='table', title='How the self-checks work: your own data and your own functions',
                  headers=['Step', 'What happens'],
                  rows=[['1 Student ID', 'Type any text in the first cell. It only makes your own datasets, so your numbers are yours. It is not a test.'], ['2 Functions', 'You write 12 functions with fixed names: fit_linear, fit_linear_gd, sigmoid, logistic_loss, fit_logistic, pca_first_component, pca_variance_share, mlp_forward, mlp_backward, mlp_train, softmax_rows, attention.'],
                        ['3 Self-checks', 'Each one runs your function on your data and on a second dataset, and compares with a reference. No expected number is shown anywhere.'],
                        ['4 No marks', 'You see OK or NOT YET and nothing is recorded. Typed-in numbers show NOT YET. Keep the project and show it to a partner.']],
                  widths=[2.4, 9.2], icons=['key', 'gear', 'check', 'flag'], note='The spreadsheet is a guided version with fixed toy numbers and its own checks.',
                  notes=('Here is how the self-checks work. There is no exam and no mark. You type any text as a student ID in the first cell, and every dataset in the notebook is made from it, so your numbers differ from your neighbour, and it is not a test. '
                         'You write functions with fixed names. Each self-check runs your function on your data and on a second dataset, and compares the result with a reference, so no expected number is printed for you to copy. '
                         'You see OK or NOT YET, and nothing is recorded. A function that only returns typed-in numbers shows NOT YET, and a function that really computes the answer shows OK. The spreadsheet is a guided version with its own checks. Which step is new to you?')))

    S.append(dict(kind='table', title='Guided workbook: check your numbers against these (toy data)',
                  headers=['Build', 'What you should see'],
                  rows=[['1 Linear regression', f'weights {w_n[0]:g}, {w_n[1]:g}; MSE {mse:.4f}; 7 hours gives {p7:.2f}'], ['2 Logistic regression', f'after 5 steps w = ({w5[0]:g}, {w5[1]:g}), loss {l5:.4f}'],
                        ['3 PCA', f'eigenvalues {ev[1]:.4f}, {ev[0]:.4f} (largest first); first component ({pc1[0]:.4f}, {pc1[1]:.4f}); share {ratio:.4f}'],
                        ['4 Neural network', f'input (1, 2), target 1: p = {p:.4f}, loss {-math.log(p):.4f}, delta = {d:.4f}, first g_W2 = {gW2[0]:.4f}'],
                        ['5 Attention', f'weights row 1: {Wt[0, 0]:.3f}, {Wt[0, 1]:.3f}, {Wt[0, 2]:.3f}; output row 3: {Wo[2, 0]:.3f}, {Wo[2, 1]:.3f}']],
                  widths=[3.0, 8.6], icons=['chart', 'check', 'magnifier', 'gear', 'key'], note='These toy numbers are for the guided workbook. The notebook shows no expected numbers. In numpy, eigh gives the eigenvalues smallest first.',
                  notes=('Use this table with the guided workbook. For linear regression you should see weights 1.12 and 0.98. For logistic regression, after five steps, the weights and loss in the table. '
                         'For PCA, the eigenvalues, largest first, and the first component. The numpy function eigh returns the eigenvalues smallest first, so you take the last column, and the sign of an eigenvector is arbitrary. '
                         'For the network, the single worked example. For attention, the first row of weights, 0.401, 0.198 and 0.401, and the output of token three. '
                         'If a check fails, the table tells you what the correct number is. In the notebook no such table exists, because your data are your own.')))

    S.append(dict(kind='table', title='Errors you will meet, what they mean and what to do',
                  headers=['What you see', 'What it means', 'What to do'],
                  rows=[['TypeError: NoneType', 'A function still says return None', 'Write your code in place of the placeholder'], ['ValueError: shapes not aligned', 'A matrix product has the wrong shapes', 'Print the shapes. Transpose one side'],
                        ['A check says NOT YET', 'Your function disagrees with the reference on your data or on the second dataset', 'Call it on a tiny example and work it out by hand'], ['Spreadsheet shows #VALUE!', 'An array formula was not filled over the whole gold block', 'Select the block and enter it as an array formula']],
                  widths=[3.6, 4.2, 4.2], icons=['key', 'bell', 'cross', 'flag'],
                  notes=('Four errors you may meet. A type error about None means a function still holds the placeholder. A value error about shapes means a matrix product has the wrong shapes, so print the shapes and transpose one side. '
                         'A check that says not yet means your function disagrees with the reference, on your data or on the second dataset, so call it on a tiny example and work it out by hand. And in the spreadsheet, a value error usually means an array formula was not filled over the whole gold block. '
                         'Read the last line of any error first.')))

    S.append(dict(kind='list', title='Project checklist: use it alone, then swap with a partner',
                  items=['Every self-check says OK, or I can say what NOT YET still means.', 'I can explain each build in two sentences, with no formulas.',
                         'I changed one thing (learning rate, my own data, no scaling) and wrote what happened.', 'My notebook runs from the top with Restart and run all.'],
                  icons=['check', 'book', 'magnifier', 'notebook'],
                  notes=('Here is a checklist for your project. There are no marks, so this is how you and a partner give each other feedback. First, every self-check says OK, or you can say what a NOT YET still means. '
                         'Second, you can explain each build in two sentences with no formulas, which is the best way to see that you understood it. Third, you changed one thing, such as the learning rate, your own data or no scaling, and wrote down what happened. '
                         'Fourth, the notebook runs from the top with restart and run all. Swap notebooks with a partner and tick the list for each other. Which item do you expect to be hardest?')))

    S.append(dict(kind='idea', title='Where this appears in AI: attention is the core step of every layer of a published transformer',
                  visual=dict(kind='stack', layers=[dict(head='Tokens and embeddings', text='Text becomes vectors', icon='doc'), dict(head='Attention', text='Your Build 5', icon='key', ),
                                                    dict(head='Feed-forward layer', text='Matrix products, nonlinearity', icon='gear'), dict(head='Softmax and loss', text='Next-token probabilities', icon='chart')], highlight=1),
                  lead='Published research describes transformer language models as many repeated layers of attention and feed-forward steps.',
                  points=['Your Build 5 is the published attention formula (Vaswani et al., 2017).', 'Closed products do not publish their designs. Open models such as Llama use the same core formula plus a causal mask, and other changes.'],
                  notes=('Here is where your project appears in real systems, as published research describes transformer language models. Text becomes tokens and embeddings. Then come many repeated layers. '
                         'Each layer has an attention step, which is the core of your build five, and a feed-forward step, which is matrix multiplications with a nonlinearity. At the top a softmax gives next-token probabilities and training minimises the cross-entropy. '
                         'Real models use many tokens, many attention heads and many layers. Open models such as Llama use the same core formula with a causal mask, so a token cannot read later tokens, and other changes. '
                         'The designs of ChatGPT, Gemini and Claude are not published, so I describe only the published framework.')))

    S.append(dict(kind='table', title='Where this appears in AI: the five builds in published models',
                  headers=['Your build', 'Where the same idea appears'],
                  rows=[['Linear regression', 'Every layer multiplies by a weight matrix: a linear map. Its weights are learned by gradient descent, a different method from least squares.'],
                        ['Logistic regression', 'The last step of a classifier is a softmax of linear scores (softmax regression, the many-class version), trained with cross-entropy.'],
                        ['PCA', 'Used to inspect and compress embeddings. LoRA (Hu et al., 2021) learns a low-rank update to a weight matrix: the same low-rank idea that makes the first principal components useful.'],
                        ['Neural network', 'Backpropagation runs in every training step of published models.'], ['Attention', 'The core step of the transformer, repeated in every layer.']],
                  widths=[3.0, 8.6], icons=['chart', 'check', 'magnifier', 'gear', 'key'], note='Phrased as published research describes. No claim about the internals of any closed product.',
                  notes=('Here is each build and where its idea appears. Every layer of a language model multiplies by a weight matrix, a linear map like build one, though its weights are learned by gradient descent, a different method from least squares. '
                         'The last step of a classifier is a softmax of linear scores, which is softmax regression, the many-class version of build two, trained with cross-entropy. '
                         'PCA is a way to inspect and compress embeddings, and LoRA learns a low-rank update to a weight matrix, the same low-rank idea that makes the first principal components useful. Backpropagation runs in every training step. Attention is the core step of the transformer. '
                         'I phrase all of this as published research describes it, with no claim about closed products.')))

    S.append(dict(kind='practice', title="Check an AI assistant's attention against your own numbers", minutes=5, label='Optional, with any assistant',
                  task='Give an assistant the three-token example: X, Wq, Wk, Wv from the data slide, d = 2. Ask for the attention weights.',
                  steps=[f'Compare its row 1 with {Wt[0, 0]:.3f}, {Wt[0, 1]:.3f}, {Wt[0, 2]:.3f}.', 'Ask if it divided by the square root of d. Try without, and see which weights get sharper.', 'Never paste confidential data into an assistant.'],
                  output='A note: where the assistant agreed with your numbers, and where it did not.',
                  notes=('Here is an activity with any assistant. Give it the three-token example with the matrices from the data slide, and ask for the attention weights. '
                         f'Compare its first row with your {Wt[0, 0]:.3f}, {Wt[0, 1]:.3f} and {Wt[0, 2]:.3f}. Ask whether it divided by the square root of d, and then try without the scaling and see which weights get sharper. '
                         'An assistant can slip on matrix arithmetic, and now you can check it. Please do not paste confidential data into any assistant.')))

    S.append(dict(kind='list', title='What to learn next: four steps',
                  items=['Machine Learning at KLAi: use these builds on real data, with scikit-learn.', 'A deep learning course, where PyTorch automatic differentiation replaces your hand-written backpropagation (title and dates to be confirmed by KLAi).',
                         'Read section 3.2 of Vaswani et al. (2017), "Attention Is All You Need", and match every symbol to your Build 5.', 'Rebuild the five builds from a blank notebook, then write your one-page formula sheet.'],
                  icons=['book', 'gear', 'notebook', 'pen'],
                  notes=('This is the end of the course, so here is what comes next, in four steps. First, Machine Learning at KLAi uses these builds on real data, with library tools such as scikit-learn. '
                         'Second, a deep learning course, where automatic differentiation in a library such as PyTorch replaces your hand-written backpropagation. The title and dates are to be confirmed by KLAi. '
                         'Third, read section 3.2 of the attention paper by Vaswani and colleagues, and match every symbol to your build five. Fourth, rebuild the five builds from a blank notebook without notes, then write your one-page formula sheet. '
                         'You can now read the equations in a paper or a library manual. What will you read first?')))

    S.append(dict(kind='table', title='Exit check: three questions and their short answers', headers=['Question', 'Short answer'],
                  rows=[['What does each row of the attention weights add up to, and why?', 'To 1, because a softmax is applied along each row.'], ['Why is the attention score divided by the square root of d_k?', 'Large dot products make the softmax saturate: almost all the weight goes to one token and the gradient is tiny. The scaling keeps the standard deviation near 1.'],
                        ['In PCA, which eigenvector is the first principal component?', 'The one with the largest eigenvalue, the direction of largest variance.']],
                  widths=[6.0, 6.0], icons=False, note='Answer each in one sentence before you read the right-hand column.',
                  notes=('Three questions to finish. One, each row of the attention weights adds up to one, because a softmax is applied along each row. '
                         'Two, the score is divided by the square root of d k because large dot products make the softmax saturate, with almost all the weight on one token and a tiny gradient, and the scaling keeps their standard deviation near one. '
                         'Three, in PCA the first principal component is the eigenvector with the largest eigenvalue. Cover the right-hand column and answer aloud first.')))

    s['facilitator'] = dict(
        prep=['Run the solution notebook once from the top and open the solution workbook. Toy numbers on the slides: weights 1.12 and 0.98, share of variance 0.9632, attention row 1 0.401, 0.198, 0.401.',
              'There are no marks. The project is the notebook, and each learner keeps it. Every learner types any text as a student ID in the first cell and gets personal data. Tell learners they may use notes, earlier notebooks and each other. The self-checks show OK or NOT YET and nothing is recorded.',
              'Optional: Facilitator Materials/Autocheck/project_selfcheck.py (Python with numpy) prints OK or NOT YET per build for a notebook, for a learner who wants a second look. It gives no marks and has no secret seeds.',
              'The spreadsheet is a guided version with fixed toy numbers and its own checks. Open the learner notebook and confirm it ends with 0 checks passing before any work.'],
        misconceptions=[('The normal equation and gradient descent give different models.', 'Both minimise the same loss and reach the same weights. Gradient descent is needed when no direct formula exists.'),
                        ('PCA works on raw columns.', 'It needs centred columns. Otherwise the covariance and the scores are wrong. The checks shift the data to catch this.'), ('Attention is a different kind of maths from the rest of the course.', 'It is matrix multiplication, a dot product score and a softmax.'),
                        ('The sqrt(d) is a detail.', 'It stops the softmax from saturating when d is large. Published in the original transformer paper.')],
        probes=[('Why does the network need a hidden layer for XOR?', 'No straight line separates the two classes. The hidden layer builds new features that do.'), ('Why is the first backward quantity p - y?', 'Sigmoid with cross-entropy has that gradient, as derived in Session 17.'),
                ('What happens to the weights if every row of attention adds to more than 1?', 'The outputs grow in size. The softmax guarantees they add to 1.'), ('How do you know a gradient from backpropagation is right?', 'Compare it with a numeric gradient made by nudging each weight. The notebook checks do exactly this.'),
                ('Is a 2-4-1 network anything like a real language model?', 'It shows the same mathematics at toy size. A real model has many more layers and parameters. Designs of closed products are not published.')],
        lab_steps=[('Build 1', 'Python: fit_linear and fit_linear_gd on the learner\'s own 8 points. Learning rate 0.05 diverges (CHANGE task). Spreadsheet: MMULT and MINVERSE block gives the toy weights 1.12 and 0.98.'),
                   ('Build 2', 'Python: loss at w = 0 is 0.693 and falls with steps; accuracy stays below 1 because the classes overlap. Spreadsheet: the 5-step table only.'),
                   ('Build 3', 'The sign of the eigenvector can flip, and the checks accept either sign. The shifted-data check catches a missing centring step.'),
                   ('Build 4', 'The usual fault is a shape error or a missing input factor in the gradient of W1; the numeric gradient check names it. Spreadsheet: one step for the input (1, 2).'),
                   ('Build 5', 'Rows of weights add to 1. A softmax without the row maximum fails on the large scores. Dividing by sqrt(d_k) is tested on 6-number keys.')],
        rescue=['If time is short, ask learners to finish Builds 1, 2 and 5 in class and the rest at home.', 'If a learner is stuck in Build 4, let them write mlp_backward first and use the given training demo to see the loss fall.', 'Spreadsheet learners can practise Linear, Logistic and Attention first, then do the notebook at home.'],
        after=['Ask learners to swap notebooks with a partner and use the project checklist. Nothing is collected or marked.', 'Remind learners to write the one-page formula sheet. The certificate of completion from KLAi Professional Learning goes to learners who complete the course project.', 'Point learners to Machine Learning at KLAi as the next step (a deep learning course is to be confirmed).'],
        lab_answer_key=[['Build 1 PREDICT: slope', 'Look at how much y rises per hour in the learner\'s own printout. The hidden slope is between 0.5 and 2.5.'], ['Build 1 CHANGE: learning rate 0.05', 'Gradient descent diverges: the steps overshoot, so the weights blow up.'],
                        ['Build 2 PREDICT: first step for w1', 'It moves up, because more hours of study go with passing.'], ['Build 2 READ: confidence', 'Not very confident: the passes and fails overlap, so the loss stays well above zero.'],
                        ['Build 3 PREDICT: direction', 'Along (1, 1) or the tilt of the cloud: both columns rise together.'], ['Build 3 READ: what is kept', 'One score per point, holding most of the spread (the share of variance).'],
                        ['Build 4 PREDICT: outputs before training', 'All near 0.5.'], ['Build 4 READ: what the hidden layer adds', 'New features (combinations of the inputs) that make the classes separable.'],
                        ['Build 5 PREDICT: row sums', '1.'], ['Build 5 CHANGE: no scaling', 'Rows with large scores get sharper (more weight on the largest).']])
    return s
