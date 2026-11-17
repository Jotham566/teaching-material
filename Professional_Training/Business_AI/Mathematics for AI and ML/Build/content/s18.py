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
    ev_n = [v * 9 / 10 for v in ev]           # the same eigenvalues if we divided by n (ddof = 0)
    wg100, wg5k, wlog = f(N['w_gd100']), f(N['w_gd5000']), f(N['w_log'])
    fm = lambda M_: '(' + '), ('.join(', '.join(f'{v:g}' for v in row) for row in np.atleast_2d(M_)) + ')'

    s = dict(
        num=18, block='Course project', short_title='Course project',
        title='Five small builds, from linear regression to attention, written from first principles',
        question='Can five small builds, written from first principles, reproduce the core of what runs inside modern AI?',
        outcomes=['Build linear regression (normal equation and gradient descent) and logistic regression (gradient descent) with numpy',
                  'Build PCA from the covariance eigen-decomposition, and a 2-4-1 neural network with backpropagation (take-home)',
                  'Learn attention as a ladder of known steps, build it for three tokens, and see OK on the self-checks of your project'],
        outcome_icons=['chart', 'gear', 'check'],
        outcome_note=('By the end of today you can build five things from first principles. Linear regression, with the normal equation and with gradient descent. Logistic regression, with gradient descent. '
                      'PCA, from the eigen-decomposition of the covariance matrix. A small neural network, two inputs, four hidden units and one output, with backpropagation, which is the take-home build. And scaled dot-product attention for three tokens, which is new today and gets the most time. '
                      'In the notebook the text you type as a student ID makes your own personal data, and automatic self-checks show OK or NOT YET for each build. There are no marks. The project is yours to keep.'),
        clock=[(10, 'Recall, then a real question from AI'), (35, 'Concept: a picture, then one example by hand'), (10, 'Break'), (45, 'Lab in Python or a spreadsheet: predict, run, change one thing'),
               (15, 'Where this appears in AI, and an exit check'), (5, 'Save the work')],
        plan_title='Your two hours: a guided tour, attention, then your project',
        plan_caption='The tour first. Then your project, with self-checks and no marks. Then AI.',
        plan_note=('Today is the last session. Ten minutes of recall from Session 17. Thirty-five minutes of concepts: a quick tour of four builds you already have the maths for, then most of the time on attention, which is new. A ten minute break. '
                   'Then forty-five minutes on your project: aim for Builds 1, 2, 3 and 5 in class, with Build 4 at home. The project is the notebook, which you build with your own personal data and keep. Nothing is marked: the checks only show you what works. The spreadsheet is a guided version with the same five builds. We finish with where this appears in AI, what to learn next, and saving your work.'),
        recall_from='Session 17',
        recall=[('How are cross-entropy, entropy and KL divergence related?', 'Cross-entropy = entropy + KL divergence. The entropy is fixed by the data, so lowering the cross-entropy lowers the KL divergence.'),
                ('What is the gradient of softmax with cross-entropy with respect to the logits?', 'The prediction minus the target: p - y.'),
                ('What does a perplexity of 5 mean?', 'The model is as unsure as if it chose among about five equally likely words at each step.')],
        words=[('Logistic regression', 'A model that passes a straight-line score through the sigmoid to give a probability between 0 and 1.'),
               ('Principal component', 'A direction of largest spread in the data: an eigenvector of the covariance matrix.'),
               ('Backpropagation', 'The chain rule applied backwards through a network to get the gradient of the loss for every weight.'),
               ('Query, key, value', 'The three vectors each token makes in attention: what it looks for, what it offers and what it passes on.'),
               ('Attention', 'Each token takes a weighted average of the value vectors, with weights from softmax(Q K^T / sqrt(d)).')],
        word_icons=['check', 'chart', 'gear', 'key', 'magnifier'],
        words_note=('Five words for today. Logistic regression puts a straight-line score through the sigmoid of Session 11, so the output is a probability. A principal component is a direction of largest spread, an eigenvector of the covariance matrix. '
                    'Backpropagation is the chain rule applied backwards through a network. Query, key and value are the three vectors each token makes in attention, and they are new today. '
                    'Attention is a weighted average of the values, with the weights coming from a softmax. Each word gets its picture before the break.'),
        keep='Keep your finished project notebook, ideally with all self-checks OK, and write your one-page formula sheet: every formula named in plain words and in the industry term.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your project', value='Self-checks OK'), dict(label='Formula sheet', value='One page'),
                                                              dict(label='Next', value='Machine Learning at KLAi'), dict(label='Then', value='Deep learning')]),
        keep_title='Save your project and write your formula sheet',
        next='Machine Learning at KLAi, then deep learning (to be confirmed).', next_label='What to learn next',
        keep_note=('This is the end of the course, so before you go do two things. Run your project from the top, look at the self-checks and save it. It is yours to keep, and nothing is marked. '
                   'Then write your one-page formula sheet, with every formula named in plain words and in the industry term. It is the page you will use when you read a paper or a library manual. '
                   'To complete the course, show your last notebook line or your workbook Check sheet to me. Thank you for eighteen sessions.'),
        keep_returns=True,
        cover_note=('Welcome to the last session. For seventeen sessions you collected tools: vectors, matrices, eigenvalues, gradients, probability, likelihood, entropy. Today you use them in five small builds. '
                    'Four of them use only what you already know. The fifth, attention, is new: every part of it is familiar, and how the parts fit together is what you learn today.'),
        slides=[])
    S = s['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 17', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[5.0, 7.0], icons=False,
                  note='All three come back today: p - y trains Builds 2 and 4, and the softmax is inside attention.',
                  notes=('Cross-entropy equals entropy plus KL divergence, and because the entropy is fixed by the data, lowering the cross-entropy lowers the KL. '
                         'The gradient of softmax with cross-entropy with respect to the logits is the prediction minus the target, and Session 17 showed the same form for a sigmoid with binary cross-entropy. A perplexity of five means the model is as unsure as if it chose among about five equally likely words. '
                         'Today the second answer trains two of our builds, and the softmax sits inside attention.')))

    S.append(dict(kind='wide', title='Five builds: four reuse what you know, and attention is new today',
                  visual=dict(kind='icons', items=[dict(icon='chart', head='Linear regression', text='Sessions 4, 10'), dict(icon='check', head='Logistic regression', text='Sessions 11, 17'),
                                                   dict(icon='magnifier', head='PCA', text='Sessions 5, 6'), dict(icon='gear', head='Neural network', text='Sessions 9, 11'),
                                                   dict(icon='key', head='Attention', text='New today')]),
                  caption='Illustrative data. Each build is 3 to 25 lines of numpy.',
                  notes=('The plan in one picture. Linear regression is the least squares of Sessions 4 and 10. Logistic regression is a sigmoid with the p minus y gradient of Session 17. PCA is the covariance and eigenvectors of Sessions 5 and 6. The network is backpropagation from Sessions 9 and 11. '
                         'Attention is different. Its arithmetic is familiar, dot products, matrices and the softmax, but attention itself is new today, so it gets the most time. '
                         'The shortest build is three lines and the network is about twenty-five, and all the data are made up to show the arithmetic.')))

    S.append(dict(kind='table', title='The illustrative data of Builds 1 to 3 (made-up numbers to show the arithmetic)',
                  headers=['Build', 'Data'],
                  rows=[['1 Linear', 'Hours x = 1, 2, 3, 4, 5, 6. Energy y (kWh) = 2.2, 2.9, 4.1, 5.2, 5.8, 7.1.'],
                        ['2 Logistic', 'Hours x = 1 to 8. Passed y = 0, 0, 0, 1, 0, 1, 1, 1.'],
                        ['3 PCA', 'a = 2.5, 0.5, 2.2, 1.9, 3.1, 2.3, 2.0, 1.0, 1.5, 1.1. b = 2.4, 0.7, 2.9, 2.2, 3.0, 2.7, 1.6, 1.1, 1.6, 0.9.']],
                  widths=[2.2, 9.4], icons=False, note='These fixed numbers are for the slides and the guided workbook. In the notebook your student ID makes your own different data.',
                  notes=('Every number the first three guided builds use is on this slide, so you can recompute them from the slides alone. Build one has six readings of hours and energy. Build two has eight students with hours of study and pass or fail. '
                         'Build three has ten points in two columns, a and b. These numbers are made up to show the arithmetic. In the notebook the text you type as a student ID makes your own, different data.')))

    S.append(dict(kind='table', title='The illustrative data of Builds 4 and 5',
                  headers=['Build', 'Data'],
                  rows=[['4 Network', 'W1 rows (0.5, -0.3), (0.2, 0.8), (-0.6, 0.4), (0.1, -0.9). b1 = 0. W2 = (0.3, -0.5, 0.7, 0.2). b2 = 0.1.'], ['4 XOR rows', 'Inputs (0, 0), (0, 1), (1, 0), (1, 1) with targets 0, 1, 1, 0.'],
                        ['5 Attention', 'X rows (1, 0), (0, 1), (1, 1). Wq rows (1, 0), (1, 1). Wk rows (1, 1), (0, 1). Wv rows (1, 0), (0, 2). d_k = 2.']],
                  widths=[2.2, 9.4], icons=False, note='Q = X Wq, K = X Wk and V = X Wv give three rows of two numbers each (one row per token).',
                  notes=('The network starts from these weights: a four by two matrix W one, a zero bias b one, four output weights W two and an output bias of 0.1. The four XOR rows have targets zero, one, one, zero. '
                         'For attention, X has one row per token, and three small matrices make the queries, keys and values. These matrices are stored as the published formula writes them, so they multiply on the right as they are. The key length d k is two. With these you can recompute every number on the next slides by hand.')))

    S.append(dict(kind='formula', title='Build 1: linear regression has a direct solution and an iterative one',
                  formulas=[('Normal equation', r'$w=(X^{T}X)^{-1}X^{T}y$'), ('Gradient descent step', r'$w\leftarrow w-\eta\,\frac{2}{n}X^{T}(Xw-y)$')],
                  symbols=[['X', 'The design matrix: a column of ones, then x.', '6 rows by 2 columns'], ['w', 'The weights: the intercept b (it multiplies the ones), then the slope w1.', f'({w_n[0]:g}, {w_n[1]:g})'], ['eta', 'The learning rate (lr in code).', '0.02'],
                           ['n', 'The number of rows.', '6']],
                  size=24, note=f'At eta 0.02, 100 steps give ({wg100[0]:.3f}, {wg100[1]:.3f}); about 5,000 steps reach ({wg5k[0]:g}, {wg5k[1]:g}). MSE {mse:.4f}.',
                  notes=('Build one is the line fit of Session 4, y-hat equals b plus w one x, in matrix form. X has a column of ones so that the first weight is the intercept b. The normal equation solves least squares in one line: w equals the inverse of X transpose X, times X transpose y. '
                         f'Gradient descent with learning rate eta reaches the same answer in small steps, but not quickly. After a hundred steps it is at {wg100[0]:.3f} and {wg100[1]:.3f}. The slope settles early and the intercept catches up slowly, so it takes about five thousand steps to reach {wg5k[0]:g} and {wg5k[1]:g}. '
                         f'The mean squared error is {mse:.4f}. Seven hours is outside the data, so the prediction of {p7:.2f} kilowatt-hours is an extrapolation.')))

    S.append(dict(kind='idea', title='Build 1 in a picture: the fitted line and its residuals',
                  visual=dict(kind='scatter', points=pts, xlabel='hours of use', ylabel='energy used (kWh)', line=(w_n[0], w_n[1]), residuals=True),
                  lead=f'The line is y-hat = {w_n[0]:g} plus {w_n[1]:g} x. The red segments are the residuals.',
                  points=['Illustrative data: x = 1 to 6 hours, y = 2.2, 2.9, 4.1, 5.2, 5.8, 7.1 kWh.', 'The normal equation and enough gradient steps give the same line.'],
                  notes=(f'Six points, and the least squares line with intercept {w_n[0]:g} and slope {w_n[1]:g}. The red segments are the residuals, the gaps between the points and the line. '
                         'Least squares chooses the line that makes the sum of their squares as small as possible. In Session 16 you saw that this is also maximum likelihood under Gaussian noise. '
                         'The data are illustrative. Which point has the largest residual?')))

    S.append(dict(kind='idea', title='Logistic regression turns a straight-line score into a probability with the sigmoid',
                  visual=dict(kind='f_logistic', xs=[float(v) for v in xl], ys=[float(v) for v in yl], b=wlog[0], w1=wlog[1]),
                  lead='Logistic regression: score = b plus w1 x, then p = sigmoid(score), the probability of class 1.',
                  points=['The sigmoid of Session 11 squeezes any score into 0 to 1.', f'Trained on the 8 students: p = 0.5 at {-wlog[0] / wlog[1]:.1f} hours. Predict "pass" above it.'],
                  notes=('Logistic regression is a named model you have not met yet, but every part is familiar. Take a straight-line score, b plus w one times x, as in Build 1. Pass it through the sigmoid of Session 11, which squeezes any number into the range zero to one. The result is read as the probability of passing. '
                         f'The red curve is the model after training on our eight students. The dots at the top passed and the dots at the bottom failed. The curve crosses one half at {-wlog[0] / wlog[1]:.1f} hours, which is where the prediction switches from fail to pass.')))

    S.append(dict(kind='formula', title='Build 2: logistic regression is trained by gradient descent on the cross-entropy',
                  formulas=[('Model', r'$p=\sigma(b+w_1x)=\frac{1}{1+e^{-(b+w_1x)}}$'), ('Gradient descent step', r'$w\leftarrow w-\eta\,\frac{1}{n}X^{T}(p-y)$')],
                  symbols=[['p', 'The predicted probability of class 1 (passed).', '0.5 at the start'], ['p - y', 'Prediction minus target (Session 17, two classes).', 'one value per row'], ['eta', 'The learning rate.', '0.1'],
                           ['Loss', 'Binary cross-entropy, from Session 16.', f'{wlist[0][2]:.3f} at the start']],
                  size=19, note=f'After 5 steps: w = ({w5[0]:g}, {w5[1]:g}), loss {l5:.3f}. Data: 8 students (see the data slide).',
                  notes=('The loss is the binary cross-entropy from Session 16. Its gradient with respect to the score is p minus y. Session 17 showed this two-class form: a sigmoid is a two-class softmax. Averaged over the rows and multiplied by the inputs, that gives the gradient for b and w one. '
                         f'Starting from zero weights every probability is one half and the loss is {wlist[0][2]:.3f}. After five steps with a learning rate of 0.1 the weights are {w5[0]:g} and {w5[1]:g}, and the loss has fallen to {l5:.3f}. '
                         'The data are eight illustrative students: hours of study and pass or fail.')))

    S.append(dict(kind='table', title='Build 2 by hand: the loss falls at every one of the first five gradient steps',
                  headers=['Step', 'b', 'w1', 'Loss (nats)'], rows=[[str(i), f'{round(float(w_[0]), 4) + 0.0:.4f}', f'{round(float(w_[1]), 4) + 0.0:.4f}', f'{lo:.4f}'] for i, w_, lo in wlist], widths=[2.0, 3.0, 3.0, 3.0], icons=False,
                  note='Learning rate 0.1. Step 0 is the start. The workbook has the same table.',
                  notes=(f'Step zero is the start, with both weights at zero and a loss of {wlist[0][2]:.4f}. At step one the intercept stays at zero, because half the students passed and the average of p minus y is zero, but the slope moves up. '
                         f'The loss falls at every step, to {wlist[5][2]:.4f} after five. In the lab you let it run for thousands of steps, and in the workbook you fill this same table with formulas. '
                         'With a learning rate of two the steps would overshoot and the loss would jump around.')))

    S.append(dict(kind='idea', title='Build 3: PCA finds the direction of largest spread in the data',
                  visual=dict(kind='scatter', points=pca_pts, xlabel='a', ylabel='b', line=(ybar - slope * xbar, slope)),
                  lead=f'The red line is the first principal component. It holds {ratio * 100:.1f} percent of the variance.',
                  points=[f'Eigenvalues of the sample covariance matrix: {ev[1]:.3f} and {ev[0]:.3f}.', f'First component: ({pc1[0]:.3f}, {pc1[1]:.3f}).'],
                  notes=(f'Build three is PCA, principal component analysis, from Sessions 5 and 6. Ten illustrative points in two dimensions. The two columns rise together, so the spread is mostly along one diagonal direction, the red line. '
                         f'That direction is the first principal component. The sample covariance matrix has two eigenvalues, {ev[1]:.3f} and {ev[0]:.3f}, so the first component holds {ratio * 100:.1f} percent of the total variance. '
                         'If we keep only the position of each point along that line, one number instead of two, we lose very little.')))

    S.append(dict(kind='formula', title='PCA as formulas: centre, form the covariance, find its eigenvectors, project',
                  formulas=[('Sample covariance matrix', r'$C=\frac{1}{n-1}X_c^{T}X_c$'), ('Eigenvector and score', r'$Cv=\lambda v,\qquad \mathrm{score}=X_c\,v_1$')],
                  symbols=[['X_c', 'The data with each column centred on its mean.', '10 rows by 2 columns'], ['lambda', 'An eigenvalue: the variance along its eigenvector.', f'{ev[1]:.3f} and {ev[0]:.3f}'],
                           ['v_1', 'The eigenvector with the largest eigenvalue: the first component.', f'({pc1[0]:.3f}, {pc1[1]:.3f})'], ['n - 1', 'Sample data divide by n - 1 (Session 5, np.cov).', '9']],
                  size=24, note=f'Dividing by n instead (ddof = 0) gives {ev_n[1]:.3f} and {ev_n[0]:.3f}: the same eigenvectors and the same {ratio * 100:.1f} percent share.',
                  notes=('First centre each column on its mean. The ten points are a sample, so the covariance matrix is X c transpose times X c divided by n minus one, as in Session 5 and as np.cov does. Its eigenvectors are the principal components, and each eigenvalue is the variance along its eigenvector. '
                         f'The largest eigenvalue is {ev[1]:.3f}, with eigenvector {pc1[0]:.3f} and {pc1[1]:.3f}. The score of a point is its centred row times that eigenvector. '
                         'Some libraries divide by n. The eigenvalues are then a little smaller, but the eigenvectors and the share of variance do not change.')))

    S.append(dict(kind='wide', title='XOR: no single straight line separates the two classes, but two lines can',
                  visual=dict(kind='f_xor'),
                  caption='XOR: 1 (gold) when exactly one input is 1, else 0 (white).',
                  notes=('XOR, short for exclusive or, answers one when exactly one of its two inputs is one. Put the four input pairs on a square and colour them: gold for one, white for zero. The gold points sit on one diagonal and the white points on the other. '
                         'On the left, try any straight line. It always leaves a gold and a white point on the same side, so logistic regression on the two inputs cannot get all four right. '
                         'On the right, two lines do the job: gold sits between them. A hidden layer can learn two such lines as new features, and the output then combines them. That is why Build 4 has a hidden layer.')))

    S.append(dict(kind='idea', title='Build 4: a 2-4-1 network has two layers of weights, and the error flows back',
                  visual=dict(kind='f_network', layers=(('Inputs', 2), ('Hidden (tanh)', 4), ('Output', 1))),
                  lead='Two inputs, four hidden units, one output. The task is XOR.',
                  points=['Forward: h = tanh(W1 x + b1), then p = sigmoid(W2 h + b2).', 'tanh (Session 11): from -1 to 1, slope 1 - h^2.', 'Backward: the chain rule passes the error back.'],
                  notes=('Build four is a small neural network, two inputs, four hidden units and one output, trained on XOR. The forward pass computes the hidden activations with tanh, which you met in Session 11: an S-shaped curve like the sigmoid, but running from minus one to one, with slope one minus h squared. Then a sigmoid gives the output probability. '
                         'The backward pass is backpropagation, the chain rule from Session 9 applied from the output back to the first layer. With a sigmoid output and binary cross-entropy, the first backward quantity is p minus y. Build 4 is the take-home build, with the backward pass scaffolded.')))

    S.append(dict(kind='formula', title='Backpropagation for the 2-4-1 network, in matrix algebra',
                  formulas=[('Forward and loss', r'$h=\tanh(W_1x+b_1),\ \ p=\sigma(W_2h+b_2),\ \ L=-[\,y\ln p+(1-y)\ln(1-p)\,]$'),
                            ('Backward', r'$\delta=p-y,\ \ g_{W_2}=\delta\,h^{T},\ \ g_{b_2}=\delta,\ \ \delta_h=(W_2^{T}\delta)\odot(1-h^{2}),\ \ g_{W_1}=\delta_h\,x^{T},\ \ g_{b_1}=\delta_h$')],
                  symbols=[['delta', 'The error signal at the output: p - y for a sigmoid with binary cross-entropy (Session 17).', f'{d:.4f} in the example'], ['delta_h', 'The error signal arriving at each hidden unit.', 'one value per unit'],
                           ['1 - h^2', 'The slope of tanh at each hidden unit (Session 11).', f'({", ".join(f"{1 - v * v:.3f}" for v in h)})'], ['odot', 'Multiply entry by entry.', 'unit by unit']],
                  size=18, note='Update with learning rate eta: each weight matrix and bias becomes W - eta × its gradient.',
                  notes=('The forward pass and the loss are on top. Below, the first backward line says the error signal at the output, delta, is p minus y, the two-class form from Session 17. The gradient for the second weight matrix is delta times the hidden activations, and the gradient for its bias is delta. '
                         'The error signal then flows back through the second matrix and is multiplied entry by entry by one minus h squared, the slope of tanh. That gives delta h at the hidden layer, and the gradient for the first weight matrix is delta h times the input. '
                         'Each weight matrix and bias is then updated by subtracting the learning rate times its gradient.')))

    S.append(dict(kind='example', title='By hand: one forward and one backward step for the input (1, 2) with target 1',
                  scenario='One illustrative example (not an XOR row), from the starting weights on the data slide. The notebook trains on many rows and averages their gradients.',
                  blocks=[dict(label='Forward', text=f'h = ({", ".join(f"{v:.3f}" for v in h)}), z2 = {z2:.4f}, p = {p:.4f}'), dict(label='Loss', text=f'-ln p = {-math.log(p):.4f} nats'),
                          dict(label='Backward', text=f'delta = p - y = {d:.4f}. g_W2 = delta × h = ({", ".join(f"{v:.3f}" for v in gW2)}). First row of g_W1 = ({E["gW1"][0, 0]:.3f}, {E["gW1"][0, 1]:.3f})'),
                          dict(label='Update', text=f'W2 first weight: 0.3 - 0.5 × ({gW2[0]:.3f}) = {0.3 - 0.5 * gW2[0]:.3f}', red=True)],
                  notes=(f'Put numbers in. The input is one and two, the target is one. With the starting weights the four hidden activations are {h[0]:.3f}, {h[1]:.3f}, {h[2]:.3f} and {h[3]:.3f}. The output probability is {p:.4f}, so the loss is {-math.log(p):.4f}. '
                         f'The error signal delta is p minus y, {d:.4f}. The gradient for the output weights is delta times h. With a learning rate of 0.5 the first output weight moves from 0.3 to {0.3 - 0.5 * gW2[0]:.3f}. '
                         f'The first row of the gradient of W1 is {E["gW1"][0, 0]:.3f} and {E["gW1"][0, 1]:.3f}. In every row of that gradient the second entry is twice the first, because the second input is 2. The workbook has this exact example in cells.')))

    S.append(dict(kind='table', title='After 5,000 gradient steps the toy network solves XOR (guided example)',
                  headers=['Input', 'Target', 'Output before training', 'Output after training'], rows=[['(0, 0)', '0', f'{p0[0]:.3f}', f'{p1[0]:.4f}'], ['(0, 1)', '1', f'{p0[1]:.3f}', f'{p1[1]:.4f}'], ['(1, 0)', '1', f'{p0[2]:.3f}', f'{p1[2]:.4f}'], ['(1, 1)', '0', f'{p0[3]:.3f}', f'{p1[3]:.4f}']],
                  widths=[2.4, 2.0, 3.8, 3.8], icons=False, note=f'The loss falls from {loss0:.3f} to {lnn:.4f} nats. Learning rate 0.5.',
                  notes=(f'Before training all four outputs are close to one half, between {min(p0):.2f} and {max(p0):.2f}, and the loss is {loss0:.3f}. '
                         f'After five thousand steps of gradient descent the outputs are near zero for the first and last inputs and near one for the middle two, and the loss is {lnn:.4f}. The network has learned XOR, which no single straight line can do. '
                         'In the notebook the self-checks compare your backward function with a numeric gradient, on your own data.')))

    S.append(dict(kind='idea', title='Attention is new today: a ladder of five steps you already know',
                  visual=dict(kind='f_attn_ladder', rungs=[dict(head='Query, key, value', src='New: three weight matrices make q, k, v', num='q1 = (1, 0)', new=True),
                                                           dict(head='Score: dot product', src='Session 2: q1 . k for every key', num='1, 0, 1'),
                                                           dict(head='Scale by sqrt(d_k)', src='Sessions 13, 14: keep the spread near 1', num='0.707, 0, 0.707'),
                                                           dict(head='Softmax along the row', src='Sessions 12, 17: scores become weights', num='0.401, 0.198, 0.401'),
                                                           dict(head='Weighted average of values', src='Session 3: weights times V', num='(0.802, 1.198)')]),
                  lead='Each token asks a question (query), every token offers a label (key) and a message (value).',
                  points=['New today: q, k, v and how the steps fit together.', 'Known: dot products, scaling, softmax, matrix products.', 'Red numbers: token 1 of the example.'],
                  notes=('Attention is new, so we build it as a ladder. The first rung is the new idea. Each token makes three vectors from its embedding: a query, what it is looking for; a key, what it offers to be found by; and a value, the message it passes on. '
                         'The other four rungs are tools you have. A dot product from Session 2 scores how well a query matches each key. Dividing by the square root of d k keeps the spread of the scores near one. The softmax of Sessions 12 and 17 turns the scores into weights. '
                         'A matrix product from Session 3 takes the weighted average of the values. The red numbers follow token one through every rung.')))

    S.append(dict(kind='example', title='By hand: attention for token 1, rung by rung',
                  scenario='q1 = (1, 0). Keys k1 = (1, 1), k2 = (0, 1), k3 = (1, 2). Values v1 = (1, 0), v2 = (0, 2), v3 = (1, 2). d_k = 2.',
                  blocks=[dict(label='Scores', text='q1 . k1 = 1, q1 . k2 = 0, q1 . k3 = 1'), dict(label='Scale', text='Divide by sqrt(2) = 1.414: 0.707, 0, 0.707'),
                          dict(label='Softmax', text=f'e^0.707 = 2.028 and e^0 = 1. Sum 5.056. Weights {Wt[0, 0]:.3f}, {Wt[0, 1]:.3f}, {Wt[0, 2]:.3f}.'),
                          dict(label='Average', text=f'{Wt[0, 0]:.3f} × (1, 0) plus {Wt[0, 1]:.3f} × (0, 2) plus {Wt[0, 2]:.3f} × (1, 2) = ({Wo[0, 0]:.3f}, {Wo[0, 1]:.3f})', red=True)],
                  notes=('Follow token one by hand. Its query is one and zero. The dot products with the three keys are one, zero and one, so token one matches tokens one and three equally. Divide by the square root of two and the scores are 0.707, zero and 0.707. '
                         f'The softmax takes e to each: 2.028, one and 2.028, which add to 5.056. The weights are {Wt[0, 0]:.3f}, {Wt[0, 1]:.3f} and {Wt[0, 2]:.3f}, and they add to one. '
                         f'Finally mix the three value vectors with those weights. The output for token one is {Wo[0, 0]:.3f} and {Wo[0, 1]:.3f}: a blend of what the tokens it attends to have to say.')))

    S.append(dict(kind='idea', title='Why divide by the square root of d: dot products of long vectors grow, and the softmax saturates',
                  visual=dict(kind='bars', items=[dict(label='Standard deviation of q . k, d = 64, unscaled', value=round(spread, 1), dark=True), dict(label='After dividing by sqrt(64) = 8', value=round(spread / 8, 1), hl=True)], unit=''),
                  lead='If the entries of q and k are independent with mean 0 and standard deviation 1, then q . k has mean 0 and standard deviation sqrt(d).',
                  points=['Saturate: when scores are large, the softmax puts almost all the weight on one token (nearly one-hot) and its gradient is tiny.', 'Dividing by sqrt(d_k) keeps the standard deviation near 1. The notebook simulates 2,000 pairs.'],
                  notes=(f'Take two random vectors of length 64, whose entries are independent with mean zero and standard deviation one, as in Session 13. Their dot product is a sum of 64 independent terms, each with variance one, so its variance is 64 and its standard deviation is 8. A simulation of two thousand pairs gives {spread:.1f}. '
                         'Scores that large make the softmax saturate: almost all the weight goes to one token, and in that region the gradient is tiny, so training stalls. Dividing by the square root of d brings the standard deviation back to about one. This is the reason given in the original paper.')))

    S.append(dict(kind='wide', title='Build 5: all three tokens at once, as a grid of attention weights',
                  visual=dict(kind='f_attention', tokens=tok, weights=Wt.tolist(), outputs=Wo.tolist(), note=f'Illustrative numbers. Token 3 reads {Wt[2, 0] * 100:.0f} percent from token 1, {Wt[2, 1] * 100:.0f} from token 2 and {Wt[2, 2] * 100:.0f} from token 3.'),
                  caption='Each row of weights adds to 1. The output is the weights times the value vectors.',
                  notes=('Do the same for every token at once and you get a grid. Each row is one token asking, each column one token being read. Darker gold means a larger weight, and each row adds to one because the softmax runs along the row. '
                         f'Token one is the row you worked by hand. Token three, in the last row, reads {Wt[2, 0] * 100:.0f} percent from token one, {Wt[2, 1] * 100:.0f} from token two and {Wt[2, 2] * 100:.0f} from itself. '
                         'On the right, each output is the weighted average of the value vectors. The numbers are made up to show the arithmetic.')))

    S.append(dict(kind='formula', title='The whole ladder in one formula, as published in 2017',
                  formulas=[('Projections', r'$Q=XW_Q,\qquad K=XW_K,\qquad V=XW_V$'), ('Attention', r'$\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\left(\frac{QK^{T}}{\sqrt{d_k}}\right)V$')],
                  symbols=[['X', 'One row per token: its embedding.', '3 tokens, 2 numbers each'], ['W_Q, W_K, W_V', 'Make queries, keys, values. Learned in a real model.', 'given here'],
                           ['Q K^T', 'All query-key dot products at once.', '3 by 3'], ['d_k; softmax', 'Key length; applied along each row.', '2; row 1: 0.401, 0.198, 0.401']],
                  size=20, note='Vaswani et al. (2017). The W matrices are stored one column per output number, so they multiply on the right as they are.',
                  notes=('This is scaled dot-product attention as Vaswani and colleagues published it in 2017, and every piece is a rung of the ladder. X times the three weight matrices gives the queries, keys and values. Q times K transpose computes every dot product at once, one row per query. '
                         'Dividing by the square root of d k is the scaling rung, the softmax runs along each row, and multiplying by V takes the weighted averages. '
                         'One note on shapes: these weight matrices are stored with one column per output number, as the paper writes them, so they multiply on the right without a transpose.')))

    S.append(dict(kind='table', title='By hand: scaled scores, weights and output for three tokens (d_k = 2)',
                  headers=['Token', 'Scaled scores', 'Weights', 'Output'],
                  rows=[[f'Token {i + 1}', ', '.join(f'{v:.3f}' for v in Wa[i]), ', '.join(f'{v:.3f}' for v in Wt[i]), ', '.join(f'{v:.3f}' for v in Wo[i])] for i in range(3)],
                  widths=[1.6, 4.0, 4.0, 2.6], icons=False, note='Illustrative. Scores = Q K^T / sqrt(2). Weights = softmax of each row. Output = weights times V.',
                  notes=(f'The full table. Row one is the token you worked by hand: scaled scores {Wa[0, 0]:.3f}, {Wa[0, 1]:.3f} and {Wa[0, 2]:.3f}, weights {Wt[0, 0]:.3f}, {Wt[0, 1]:.3f} and {Wt[0, 2]:.3f}, and output {Wo[0, 0]:.3f} and {Wo[0, 1]:.3f}. '
                         f'Token three has the largest score for itself, {Wa[2, 2]:.3f}, so it gives itself the largest weight, {Wt[2, 2]:.3f}. '
                         'In the workbook the softmax is built in cells with the stable trick of subtracting the row maximum.')))

    S.append(dict(kind='compare', title='Three slips that the self-checks will catch',
                  left=dict(head='The slip', points=['No column of ones, so no intercept.', 'PCA without centring the data first.', 'Softmax along the wrong axis, or no sqrt(d_k).']),
                  right=dict(head='The fix', points=['Add the column of ones to X.', 'Subtract each column mean first.', 'Softmax along each row; divide scores by sqrt(d_k).']),
                  verdict='Each check names its build, so read the name first.',
                  notes=('Three slips that the checks will catch. In linear regression, forgetting the column of ones means there is no intercept. In PCA, forgetting to centre the data means the covariance is wrong. '
                         'In attention, applying the softmax down the columns gives rows of weights that do not add to one, and forgetting the square root of d changes every weight. '
                         'When a check fails, its name tells you which build to look at. Which of these would you have made?')))

    S.append(dict(kind='code', title='Read the five recipes before you write them',
                  code='w = np.linalg.solve(X.T @ X, X.T @ y)\nw = w - lr * X.T @ (sigmoid(X @ w) - y) / n\nvals, vecs = np.linalg.eigh(Dc.T @ Dc / (n - 1))\ngW1 = dh.T @ X\nout = softmax_rows(Q @ K.T / np.sqrt(d)) @ V',
                  reads=['Build 1: the normal equation in one line.', 'Build 2: one gradient step of logistic regression.', 'Build 3: eigh gives eigenvalues smallest first, so take the last column. An eigenvector\'s sign is arbitrary.', 'Build 4: a gradient from backpropagation.', 'Build 5: the attention formula.',
                         'Spreadsheet: MMULT, MINVERSE, TRANSPOSE and SUMPRODUCT.'],
                  notes=('Read the five recipes before your project. Build one, the normal equation in a single line with solve. Build two, one gradient step of logistic regression, the p minus y again, with lr as the learning rate eta. '
                         'Build three, the eigen-decomposition of the sample covariance matrix with eigh. Build four, a gradient from backpropagation, here the gradient of the first weight matrix. Build five, the attention formula in one line. '
                         'In the spreadsheet the same steps use MMULT, MINVERSE, TRANSPOSE and SUMPRODUCT. The notebook asks you to write the functions that these lines sit in.')))

    S.append(dict(kind='divider', title='Part 2: your project', lead='Close the slides. Open the notebook or the workbook.', section='Lab',
                  notes=('That is the end of the tour. The project is yours. Open the notebook or the workbook and work through the builds in order: one, two, three and five in class, and four at home. '
                         'Every self-check names its build, so you can see which one needs work. You may use your notes and earlier notebooks, and you may talk with your neighbour. Nothing is marked. '
                         'Raise your hand if something does not run, and I will help you read the error message. Good luck.')))

    S.append(dict(kind='steps', title='Your project has five builds, and every self-check names its build',
                  steps=[dict(head='1 Linear', text='fit_linear, fit_linear_gd', icon='chart'), dict(head='2 Logistic', text='sigmoid, logistic_loss, fit_logistic', icon='check'), dict(head='3 PCA', text='first component, variance share', icon='magnifier'),
                         dict(head='4 Network', text='take-home: forward, backward (scaffolded), train', icon='gear'), dict(head='5 Attention', text='softmax_rows, attention', icon='grid')],
                  caption=f'In class: Builds 1, 2, 3 and 5. At home: Build 4. Python: {nchk} checks, each on your data and a second dataset. Spreadsheet: a guided version.',
                  notes=(f'The five builds in order, with the names of the functions you write. In the notebook there are {nchk} self-checks. Each one runs your function on your own data and on a second dataset, and every check begins with the name of its build. '
                         'In class, aim for Builds one, two, three and five. Build four, the network, is the take-home build. Its backward pass is scaffolded: the shapes are given and you write two lines. '
                         'The notebook ends with a cell that says how many checks pass. Later builds reuse earlier ideas, like p minus y and the sigmoid.')))

    S.append(dict(kind='table', title='How the self-checks work, and what counts as completing the project',
                  headers=['Step', 'What happens'],
                  rows=[['1 Student ID', 'Type any text in the first cell. It only makes your own datasets, so your numbers are yours. It is not a test.'], ['2 Functions', 'You write 12 functions with fixed names, from fit_linear to attention.'],
                        ['3 Self-checks', 'Each one runs your function on your data and on a second dataset, and compares with a reference. You see OK or NOT YET; nothing is recorded.'],
                        ['4 Completing', 'Show your facilitator the last line of the notebook (show_checks) or the Check sheet of the guided workbook. Either counts.']],
                  widths=[2.4, 9.2], icons=['key', 'gear', 'check', 'flag'], note='No marks. Typed-in numbers show NOT YET, because the checks also use a second dataset.',
                  notes=('There is no exam and no mark. You type any text as a student ID in the first cell, and every dataset in the notebook is made from it, so your numbers differ from your neighbour. '
                         'You write functions with fixed names. Each self-check runs your function on your data and on a second dataset and compares the result with a reference, so no expected number is printed for you to copy. '
                         'To complete the course project, show me the last line of the notebook or the Check sheet of the guided workbook. Either one counts, and that is what the certificate of completion asks for.')))

    S.append(dict(kind='table', title='Guided workbook: check your numbers against these (toy data)',
                  headers=['Build', 'What you should see'],
                  rows=[['1 Linear regression', f'b {w_n[0]:g}, w1 {w_n[1]:g}; MSE {mse:.4f}; 7 hours gives {p7:.2f}'], ['2 Logistic regression', f'after 5 steps w = ({w5[0]:g}, {w5[1]:g}), loss {l5:.4f}'],
                        ['3 PCA', f'eigenvalues {ev[1]:.4f}, {ev[0]:.4f} (n - 1); first component ({pc1[0]:.4f}, {pc1[1]:.4f}); share {ratio:.4f}'],
                        ['4 Neural network', f'input (1, 2), target 1: p = {p:.4f}, loss {-math.log(p):.4f}, delta = {d:.4f}, first g_W2 = {gW2[0]:.4f}'],
                        ['5 Attention', f'weights row 1: {Wt[0, 0]:.3f}, {Wt[0, 1]:.3f}, {Wt[0, 2]:.3f}; output row 3: {Wo[2, 0]:.3f}, {Wo[2, 1]:.3f}']],
                  widths=[3.0, 8.6], icons=['chart', 'check', 'magnifier', 'gear', 'key'], note='These toy numbers are for the guided workbook. The notebook shows no expected numbers. In numpy, eigh gives the eigenvalues smallest first.',
                  notes=('Use this table with the guided workbook. For linear regression you should see an intercept of 1.12 and a slope of 0.98. For logistic regression, after five steps, the weights and loss in the table. '
                         f'For PCA, the eigenvalues of the sample covariance, largest first, {ev[1]:.4f} and {ev[0]:.4f}, and the first component. The sign of an eigenvector is arbitrary. '
                         'For the network, the single worked example. For attention, the first row of weights, 0.401, 0.198 and 0.401, and the output of token three. '
                         'In the notebook no such table exists, because your data are your own.')))

    S.append(dict(kind='table', title='Errors you will meet, what they mean and what to do',
                  headers=['What you see', 'What it means', 'What to do'],
                  rows=[['TypeError: NoneType', 'A function still says return None', 'Write your code in place of the placeholder'], ['ValueError: shapes not aligned', 'A matrix product has the wrong shapes', 'Print the shapes. Transpose one side'],
                        ['A check says NOT YET', 'Your function disagrees with the reference on your data or on the second dataset', 'Call it on a tiny example and work it out by hand'], ['Spreadsheet shows #VALUE!', 'An array formula was not filled over the whole gold block', 'Select the block and enter it as an array formula']],
                  widths=[3.6, 4.2, 4.2], icons=['key', 'bell', 'cross', 'flag'],
                  notes=('Four errors you may meet. A type error about None means a function still holds the placeholder. A value error about shapes means a matrix product has the wrong shapes, so print the shapes and transpose one side. '
                         'A check that says not yet means your function disagrees with the reference, on your data or on the second dataset, so call it on a tiny example and work it out by hand. In the spreadsheet, a value error usually means an array formula was not filled over the whole gold block. '
                         'Read the last line of any error first.')))

    S.append(dict(kind='list', title='Project checklist: use it alone, then swap with a partner',
                  items=['Every self-check says OK, or I can say what NOT YET still means.', 'I can explain each build in two sentences, with no formulas.',
                         'I changed one thing (learning rate, my own data, no scaling) and wrote what happened.', 'My notebook runs from the top with Restart and run all.'],
                  icons=['check', 'book', 'magnifier', 'notebook'],
                  notes=('A checklist for your project. There are no marks, so this is how you and a partner give each other feedback. First, every self-check says OK, or you can say what a NOT YET still means. '
                         'Second, you can explain each build in two sentences with no formulas, which is the best test that you understood it. Third, you changed one thing, such as the learning rate, your own data or no scaling, and wrote down what happened. '
                         'Fourth, the notebook runs from the top with restart and run all. Swap notebooks with a partner and tick the list for each other.')))

    S.append(dict(kind='idea', title='Where this appears in AI: attention is the core step of every layer of a published transformer',
                  visual=dict(kind='stack', layers=[dict(head='Tokens and embeddings', text='Text becomes vectors', icon='doc'), dict(head='Attention', text='Your Build 5', icon='grid'),
                                                    dict(head='Feed-forward layer', text='Matrices and a nonlinearity', icon='gear'), dict(head='Softmax and loss', text='Next-token probabilities', icon='chart')], highlight=1),
                  lead='Published research describes transformer language models as many repeated layers of attention and feed-forward steps.',
                  points=['Feed-forward layer: a small network like Build 4 applied to each token. Nonlinearity: a curved function such as tanh between the matrices.', 'Open models such as Llama add a causal mask: a token cannot read later tokens.'],
                  notes=('Published research describes how transformer language models are built. Text becomes tokens and embeddings. Then come many repeated layers. '
                         'Each layer has an attention step, the core of your build five, and a feed-forward layer: two weight matrices with a nonlinearity, a curved function like tanh, between them, applied to each token like a small Build 4. At the top a softmax gives next-token probabilities, and training minimises the cross-entropy. '
                         'Open models such as Llama use the same core formula with a causal mask, which stops a token from reading later tokens. The designs of ChatGPT, Gemini and Claude are not published, so I describe only the published framework.')))

    S.append(dict(kind='table', title='Where this appears in AI: the five builds in published models',
                  headers=['Your build', 'Where the same idea appears'],
                  rows=[['Linear regression', 'Every layer multiplies by a weight matrix. Its weights are found by gradient descent rather than a direct formula, usually with a cross-entropy loss rather than squared error.'],
                        ['Logistic regression', 'The last step of a classifier is a softmax of linear scores, trained with cross-entropy. This many-class version is called softmax regression.'],
                        ['PCA', 'Used to inspect and compress embeddings. LoRA (Hu et al., 2021) learns a low-rank update to a weight matrix, the same low-rank idea.'],
                        ['Neural network', 'Backpropagation runs in every training step of published models.'], ['Attention', 'The core step of the transformer, repeated in every layer.']],
                  widths=[3.0, 8.6], icons=['chart', 'check', 'magnifier', 'gear', 'key'], note='Phrased as published research describes. No claim about the internals of any closed product.',
                  notes=('Every layer of a language model multiplies by a weight matrix, a linear map like build one, though its weights are found by gradient descent rather than a direct formula, and usually with a cross-entropy loss. '
                         'The last step of a classifier is a softmax of linear scores, trained with cross-entropy, which is called softmax regression, the many-class version of build two. '
                         'PCA is a way to inspect and compress embeddings, and LoRA learns a low-rank update to a weight matrix. Backpropagation runs in every training step. Attention is the core step of the transformer. '
                         'I phrase all of this as published research describes it, with no claim about closed products.')))

    S.append(dict(kind='practice', title="Check an AI assistant's attention against your own numbers", minutes=5, label='Optional, with any assistant',
                  task='Give an assistant the three-token example: X, Wq, Wk, Wv from the data slide, d_k = 2. Ask for the attention weights.',
                  steps=[f'Compare its row 1 with {Wt[0, 0]:.3f}, {Wt[0, 1]:.3f}, {Wt[0, 2]:.3f}.', 'Ask if it divided by sqrt(d_k). Try without, and see which weights get sharper.', 'Never paste confidential data into an assistant.'],
                  output='A note: where the assistant agreed with your numbers, and where it did not.',
                  notes=('Try this with any assistant. Give it the three-token example with the matrices from the data slide, and ask for the attention weights. '
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
        prep=['Run the solution notebook once from the top and open the solution workbook. Toy numbers on the slides: intercept 1.12 and slope 0.98, eigenvalues 1.2840 and 0.0491 (sample covariance, n - 1), share of variance 0.9632, attention row 1 0.401, 0.198, 0.401. Attention is taught as new today: give the ladder and the by-hand slide the most concept time.',
              'There are no marks. The project is the notebook, and each learner keeps it. Every learner types any text as a student ID in the first cell and gets personal data. Tell learners they may use notes, earlier notebooks and each other. The self-checks show OK or NOT YET and nothing is recorded.',
              'Optional: Facilitator Materials/Autocheck/project_selfcheck.py (Python with numpy) prints OK or NOT YET per build for a notebook, for a learner who wants a second look. It gives no marks and has no secret seeds.',
              'The spreadsheet is a guided version with fixed toy numbers and its own checks. Open the learner notebook and confirm it ends with 0 checks passing before any work.'],
        misconceptions=[('The normal equation and gradient descent give different models.', 'Both minimise the same loss and reach the same weights. Gradient descent is needed when no direct formula exists.'),
                        ('PCA works on raw columns.', 'It needs centred columns. Otherwise the covariance and the scores are wrong. The checks shift the data to catch this.'), ('Attention is a different kind of maths from the rest of the course.', 'Its parts are known (dot products, scaling, softmax, matrix products). Queries, keys, values and how the parts fit together are new.'),
                        ('The sqrt(d) is a detail.', 'It stops the softmax from saturating when d is large. Published in the original transformer paper.')],
        probes=[('Why does the network need a hidden layer for XOR?', 'No straight line separates the two classes. The hidden layer builds new features that do.'), ('Why is the first backward quantity p - y?', 'Sigmoid with binary cross-entropy has that gradient: Session 17 derived the two-class form.'),
                ('What happens to the weights if every row of attention adds to more than 1?', 'The outputs grow in size. The softmax guarantees they add to 1.'), ('How do you know a gradient from backpropagation is right?', 'Compare it with a numeric gradient made by nudging each weight. The notebook checks do exactly this.'),
                ('Is a 2-4-1 network anything like a real language model?', 'It shows the same mathematics at toy size. A real model has many more layers and parameters. Designs of closed products are not published.')],
        lab_steps=[('Build 1', 'Python: fit_linear and fit_linear_gd on the learner\'s own 8 points. The 400-step run is still far off (the intercept lags); the lr 0.01, 20,000-step run matches the normal equation within 0.001 for every ID. Learning rate 0.05 diverges (CHANGE task). Spreadsheet: MMULT and MINVERSE block gives 1.12 and 0.98.'),
                   ('Build 2', 'Python: loss at w = 0 is 0.693 and falls with steps; accuracy stays below 1 because the classes overlap. Spreadsheet: the 5-step table only.'),
                   ('Build 3', 'The sign of the eigenvector can flip, and the checks accept either sign. The shifted-data check catches a missing centring step.'),
                   ('Build 4 (take-home)', 'mlp_backward is scaffolded: learners write delta_h and gW1. The usual fault is a shape error or a missing input factor in gW1; the numeric gradient check names it. Spreadsheet: one step for the input (1, 2).'),
                   ('Build 5', 'Rows of weights add to 1. A softmax without the row maximum fails on the large scores. Dividing by sqrt(d_k) is tested on 6-number keys.')],
        rescue=['The in-class target is Builds 1, 2, 3 and 5. If time is short, finish Builds 1, 2 and 5 in class and the rest at home.', 'If a learner is stuck in Build 4, let them write mlp_backward first and use the given training demo to see the loss fall.', 'Spreadsheet learners can practise Linear, Logistic and Attention first, then do the notebook at home.'],
        after=['Ask learners to swap notebooks with a partner and use the project checklist. Nothing is collected or marked.', 'Remind learners to write the one-page formula sheet. The certificate of completion from KLAi Professional Learning goes to learners who complete the course project: they show you the show_checks() line of the notebook or the Check sheet of the guided workbook. Either counts; nothing is marked.', 'Point learners to Machine Learning at KLAi as the next step (a deep learning course is to be confirmed).'],
        lab_answer_key=[['Build 1 PREDICT: slope', 'Look at how much y rises per hour in the learner\'s own printout. The hidden slope is between 0.5 and 2.5.'], ['Build 1 READ: why the intercept lags', 'The hours are far from 0, so the loss is a long narrow valley along the intercept direction; small steps move along it slowly.'], ['Build 1 CHANGE: learning rate 0.05', 'Gradient descent diverges: the steps overshoot, so the weights blow up.'],
                        ['Build 2 PREDICT: first step for w1', 'It moves up, because more hours of study go with passing.'], ['Build 2 READ: confidence', 'Not very confident: the passes and fails overlap, so the loss stays well above zero.'],
                        ['Build 3 PREDICT: direction', 'Along (1, 1) or the tilt of the cloud: both columns rise together.'], ['Build 3 READ: what is kept', 'One score per point, holding most of the spread (the share of variance).'],
                        ['Build 4 PREDICT: outputs before training', 'All near 0.5.'], ['Build 4 READ: what the hidden layer adds', 'New features (combinations of the inputs) that make the classes separable.'],
                        ['Build 5 PREDICT: row sums', '1.'], ['Build 5 CHANGE: no scaling', 'Rows with large scores get sharper (more weight on the largest).']])
    return s
