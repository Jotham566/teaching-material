"""Session 20: Neural networks and deep learning, without the maths wall.

Every number on a slide, in a note or in the notebook checks is computed in facts() with numpy and pandas: the neuron by hand, the one-weight gradient descent loop, the learning-rate experiment,
and a small feedforward network written in numpy (ReLU hidden layers, sigmoid output, log loss, backpropagation) trained on loans.csv. scikit-learn's MLPClassifier and RandomForestClassifier
are not available in the authoring sandbox, so no output of either is shown anywhere: the notebook compares the learner's results with the numpy reference with a wide tolerance."""
import contextlib
import io
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

BUILD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import loans_canon as LC  # noqa: E402  (the shared split: stratified 6,000 / 2,000, the same rows as Sessions 14 to 17)
DATA = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'data'
LOAN_COLS = list(LC.FEATURES)   # the 12 numeric columns of Session 14 (no indicator columns, to keep the network small)


def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -30, 30)))


def auc_score(y, s):
    """Area under the ROC curve from ranks (ties get the average rank)."""
    y = np.asarray(y)
    s = np.asarray(s, float)
    order = np.argsort(s, kind='mergesort')
    ss = s[order]
    ranks = np.empty(len(s))
    i = 0
    while i < len(ss):
        j = i
        while j + 1 < len(ss) and ss[j + 1] == ss[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2 + 1
        i = j + 1
    n1 = y.sum()
    n0 = len(y) - n1
    return float((ranks[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def logloss(y, p):
    p = np.clip(p, 1e-9, 1 - 1e-9)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


class MLP:
    """A small feedforward network: ReLU hidden layers, sigmoid output, log loss, gradient descent with backpropagation."""
    def __init__(self, sizes, seed=0):
        r = np.random.default_rng(seed)
        self.W = [r.normal(0, np.sqrt(2 / a), (a, b)) for a, b in zip(sizes[:-1], sizes[1:])]
        self.b = [np.zeros(b) for b in sizes[1:]]

    def forward(self, X):
        acts = [X]
        for k, (W, b) in enumerate(zip(self.W, self.b)):
            z = acts[-1] @ W + b
            acts.append(sigmoid(z) if k == len(self.W) - 1 else np.maximum(z, 0))
        return acts

    def predict_proba(self, X):
        return self.forward(X)[-1][:, 0]

    def step(self, X, y, lr):
        acts = self.forward(X)
        d = (acts[-1][:, 0] - y)[:, None] / len(X)
        for k in range(len(self.W) - 1, -1, -1):
            gW = acts[k].T @ d
            gb = d.sum(0)
            if k > 0:
                d = (d @ self.W[k].T) * (acts[k] > 0)
            self.W[k] -= lr * gW
            self.b[k] -= lr * gb

    def n_params(self):
        return sum(W.size + b.size for W, b in zip(self.W, self.b))


def gd_one_weight(lr, steps=8, x=2.0, target=6.0):
    w = 0.0
    ws, losses = [w], []
    for _ in range(steps):
        losses.append((w * x - target) ** 2)
        w = w - lr * 2 * (w * x - target) * x
        ws.append(w)
    return ws, losses


@lru_cache(maxsize=None)
def facts():
    F = {}
    # ---- one neuron
    x, w, b = np.array([2, 0.4, 0.6]), np.array([0.9, -1.2, 1.5]), -1.0
    F['nx'], F['nw'], F['nb'] = x, w, b
    F['nz'] = float(np.dot(x, w) + b)
    F['nout'] = float(sigmoid(F['nz']))
    F['nrelu'] = float(max(F['nz'], 0))
    F['nterms'] = [float(a * c) for a, c in zip(x, w)]
    # the lab neuron
    lx, lw = np.array([1, 0.8, 0.3]), np.array([0.9, -1.2, 1.5])
    F['lab_z'] = float(np.dot(lx, lw) - 1.0)
    F['lab_score'] = float(sigmoid(F['lab_z']))
    lw2 = np.array([4.5, -1.2, 1.5])
    F['lab_score2'] = float(sigmoid(np.dot(lx, lw2) - 1.0))
    F['lab_relu_neg'] = float(max(F['lab_z'], 0))
    # ---- gradient descent on one weight
    F['gd'] = {lr: gd_one_weight(lr) for lr in (0.05, 0.25, 0.5)}
    F['gd_w'], F['gd_loss'] = F['gd'][0.05]
    F['final_w'] = {lr: F['gd'][lr][0][-1] for lr in F['gd']}
    F['final_loss'] = {lr: (F['gd'][lr][0][-1] * 2.0 - 6.0) ** 2 for lr in F['gd']}
    # ---- loans
    # ---- the loans: canonical preparation, but a blank income stays blank here: the median is learned INSIDE the Pipeline from the training rows only (leak-free)
    loans = pd.read_csv(DATA / 'loans.csv')
    F['loans_rows'] = len(loans)
    bad = (loans.age < 18) | (loans.age > 100)
    F['n_bad_age'] = int(bad.sum())
    loans.loc[bad, 'age'] = loans.loc[~bad, 'age'].median()
    loans['income_missing'] = loans.monthly_income_ugx.isna().astype(int)
    loans['instalment_to_income'] = loans.loan_amount_ugx * LC.TOTAL_REPAYMENT_FACTOR / loans.term_months / loans.monthly_income_ugx   # NaN where the income is blank
    F['n_loans'] = len(loans)
    F['default_rate'] = float(loans.default.mean())
    ytot = loans.default.to_numpy()
    tr_i, te_i = LC.split_indices(ytot)   # equal to train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
    F['n_test'], F['n_train'] = len(te_i), len(tr_i)
    F['test_defaults'], F['train_defaults'] = int(ytot[te_i].sum()), int(ytot[tr_i].sum())
    F['test_index_sum'] = int(te_i.sum())
    F['batch'] = 200
    F['n_batches'] = int(np.ceil(F['n_train'] / F['batch']))
    tr, te = loans.iloc[tr_i], loans.iloc[te_i]
    med = tr[LOAN_COLS].median()
    Xtr, Xte = tr[LOAN_COLS].fillna(med).values.astype(float), te[LOAN_COLS].fillna(med).values.astype(float)
    Xtr_raw, Xte_raw = Xtr.copy(), Xte.copy()
    mu, sd = Xtr.mean(0), Xtr.std(0)
    Xtr, Xte = (Xtr - mu) / sd, (Xte - mu) / sd
    ytr, yte = tr.default.values.astype(float), te.default.values.astype(float)
    F['n_missing_income'] = int(loans.monthly_income_ugx.isna().sum())
    F['canon_auc_12'] = LC.facts()['auc_12']
    F['n_features'] = len(LOAN_COLS)
    # logistic regression = a network with no hidden layer
    lg = MLP([len(LOAN_COLS), 1], 0)
    for _ in range(300):
        lg.step(Xtr, ytr, 0.5)
    # the logistic regression of Sessions 15 to 17 (scaled, L2 with C = 1.0, solved exactly) on the same imputed rows
    lr_m = LC.ScaledLogReg().fit(pd.DataFrame(Xtr_raw, columns=LOAN_COLS), ytr)
    F['auc_logit_test'] = auc_score(yte, lr_m.predict_proba(Xte_raw))
    F['auc_logit_train'] = auc_score(ytr, lr_m.predict_proba(Xtr_raw))
    # a leaky version with collection_calls
    cc_tr = tr.collection_calls.values.astype(float)[:, None]
    cc_te = te.collection_calls.values.astype(float)[:, None]
    m2, s2 = cc_tr.mean(), cc_tr.std()
    lr_leak = LC.ScaledLogReg().fit(pd.DataFrame(np.hstack([Xtr_raw, cc_tr]), columns=LOAN_COLS + ['collection_calls']), ytr)
    F['auc_leak_test'] = auc_score(yte, lr_leak.predict_proba(np.hstack([Xte_raw, cc_te])))
    # the numpy network 12-16-8-1, mini-batches of 200, 400 epochs
    net = MLP([len(LOAN_COLS), 16, 8, 1], 1)
    for e in range(1, 401):
        p = np.random.default_rng(e).permutation(len(Xtr))
        for i in range(0, len(p), F['batch']):
            bb = p[i:i + F['batch']]
            net.step(Xtr[bb], ytr[bb], 0.05)
    F['auc_net_test'] = auc_score(yte, net.predict_proba(Xte))
    F['auc_net_train'] = auc_score(ytr, net.predict_proba(Xtr))
    F['net_params'] = net.n_params()
    F['logit_params'] = lg.n_params()
    # overfitting: a large network on only 300 training loans, full-batch gradient descent
    sub = np.random.default_rng(7).permutation(len(Xtr))[:300]
    Xs, ys = Xtr[sub], ytr[sub]
    big = MLP([len(LOAN_COLS), 64, 64, 1], 3)
    ep, trl, tel = [0], [logloss(ys, big.predict_proba(Xs))], [logloss(yte, big.predict_proba(Xte))]
    for e in range(1, 801):
        big.step(Xs, ys, 0.1)
        if e % 10 == 0:
            ep.append(e)
            trl.append(logloss(ys, big.predict_proba(Xs)))
            tel.append(logloss(yte, big.predict_proba(Xte)))
    F['of_epochs'], F['of_train_loss'], F['of_test_loss'] = ep, trl, tel
    F['of_best_epoch'] = int(ep[int(np.argmin(tel))])
    F['of_best_test_loss'] = float(min(tel))
    F['of_auc_train'] = auc_score(ys, big.predict_proba(Xs))
    F['of_auc_test'] = auc_score(yte, big.predict_proba(Xte))
    F['of_params'] = big.n_params()
    F['of_n'] = 300
    return F


def run_snippet(code, ns=None):
    """Run a code string that is shown on a slide and return (what it prints, namespace): a slide never shows an output that was not produced."""
    if ns is None:
        ns = {'np': np, 'pd': pd}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(code, ns)
    return buf.getvalue().strip(), ns


def n(x):
    return f'{int(round(x)):,}'


def build():
    F = facts()
    ws, ls = F['gd_w'], F['gd_loss']
    nout = F['nout']
    assert F['n_train'] == 6000 and F['n_test'] == 2000 and F['test_defaults'] == 251 and F['n_batches'] == 30
    p1 = F['n_features'] * 16 + 16
    p2 = 16 * 8 + 8
    p3 = 8 * 1 + 1
    assert p1 + p2 + p3 == F['net_params']
    t1, t2, t3 = F['nterms']
    # ---- code shown on slides is executed here and its real output is shown
    code_loop = ("x, target, w, lr = 2.0, 6.0, 0.0, 0.05\n"
                 "for step in range(1, 9):\n"
                 "    loss = (w * x - target) ** 2\n"
                 "    grad = 2 * (w * x - target) * x\n"
                 "    w = w - lr * grad\n"
                 "    if step in (1, 2, 4, 8):\n"
                 "        print(step, round(w, 3), round(loss, 3))")
    out_loop, _ = run_snippet(code_loop)
    lines = out_loop.split('\n')
    assert len(lines) == 4 and lines[0] == '1 1.2 36.0', lines
    assert str(round(ws[-1], 3)) in lines[-1]
    code_mlp = ("mlp = make_pipeline(\n"
                "    SimpleImputer(strategy='median'),\n"
                "    StandardScaler(),\n"
                "    MLPClassifier(hidden_layer_sizes=(16, 8),\n"
                "                  max_iter=500, random_state=42))\n"
                "mlp.fit(X_train, y_train)\n"
                "y_prob = mlp.predict_proba(X_test)[:, 1]\n"
                "print(roc_auc_score(y_test, y_prob))")
    fw, fl = F['final_w'], F['final_loss']
    ep = F['of_epochs']

    sess = dict(
        num=20, block='Module E: Neural networks and text', short_title='Neural networks and deep learning',
        title='Neural networks and deep learning, without the maths wall',
        question='What is a neural network, and when is one the right tool?',
        outcomes=['Describe an artificial neuron, layers, a loss function and gradient descent in plain words, with the real terms',
                  'Run a neuron and a real gradient descent loop in numpy, and watch a network overfit',
                  'Compare an MLPClassifier with a random forest on the loans data and say when deep learning is worth it'],
        outcome_icons=['gear', 'chart', 'check'],
        outcome_note=('Here is what you can do by the end of today. You can describe an artificial neuron, the layers of a network, the loss function and gradient descent, using the real terms and a plain explanation of each. '
                      'You can run a neuron and a real gradient descent loop in numpy, and you can watch a network overfit. '
                      'And you can compare an MLPClassifier with a random forest on the loans data, and say when deep learning is worth the trouble. There is very little algebra today. Everything is numbers you can check.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: neuron, layers, loss, training'), (10, 'Break'), (45, 'Lab: predict, run, read, change'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: network ideas first, then the neural network lab',
        plan_caption='Ideas with pictures first. Then you open the notebook and TensorFlow Playground.',
        plan_note=('We have two hours. The first ten minutes bring back Session 19 and set the question. Then forty-five minutes of concepts with laptops closed: the neuron, the layers, the loss, gradient descent, overfitting, and pretrained models. '
                   'After a ten minute break you open the notebook for a forty-five minute lab. You build a neuron and a training loop in numpy, play with TensorFlow Playground, and compare a network with a random forest on the loans. '
                   'The last ten minutes are the exit check and what you keep.'),
        recall_from='Session 19',
        recall=[('Why do we split a time series by date?', 'A random split lets the model see months after the test months, which is data leakage. Next month always lies after the data you have.'),
                ('What must a forecast beat before you trust it?', 'The baseline model: the seasonal naive forecast that copies the same month from last year.'),
                ('Why do we group by district before we shift a lag feature?', 'Without groupby, the first month of a district borrows its lag from the district above it in the file.')],
        words=[('Artificial neuron (perceptron)', 'A small calculation: a weighted sum of the inputs plus a bias, passed through an activation function.'),
               ('Activation function (sigmoid, ReLU)', 'The bend applied to the weighted sum. Sigmoid gives a score from 0 to 1. ReLU gives 0 below zero and the total above it.'),
               ('Feedforward neural network (multilayer perceptron, MLP)', 'Neurons arranged in an input layer, hidden layers and an output layer, with values moving forward only.'),
               ('Gradient descent and backpropagation', 'Training: repeated small steps that lower the loss function. Backpropagation works out how much each weight changed the loss (its gradient).'),
               ('Transfer learning (pretrained model)', 'Start from a network someone else trained and train only a new last layer on your own data.')],
        word_icons=['gear', 'chart', 'grid', 'clock', 'folder'],
        words_note=('Five words for today. An artificial neuron is a weighted sum plus a bias, passed through an activation function such as sigmoid or ReLU. A feedforward neural network, also called a multilayer perceptron, stacks neurons in layers. '
                    'Gradient descent is how a network trains, with backpropagation working out how much each weight changed the loss. And transfer learning starts from a pretrained model. We use every one of them before the end of the session.'),
        keep='Keep your lab notebook with its results table and your three-sentence recommendation: network, random forest or logistic regression for the credit team, and why.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab file', value='A network notebook'), dict(label='The key test', value='Does it beat the simple model?'), dict(label='Next session', value='Text as data')]),
        keep_title='Save your notebook and your recommendation',
        next='Session 21: Text as data. We turn customer messages into numbers with bag of words, TF-IDF and embeddings.', next_label='Next session',
        keep_note=('Before you go, save the notebook. Your keepsake is the results table that compares the models and your three-sentence recommendation to the credit team. If a manager could read those three sentences and decide, they are good. '
                   'Remember the question we started with: when is a neural network the right tool? For a table like the loans, the answer today is: only if it beats the simpler models by enough to matter. Next session we turn text into numbers.'),
        cover_note=('Welcome back. Neural networks have a reputation for being magic, or for needing a wall of mathematics. Today we remove both. A neuron is a weighted sum with a bend. A network is many of them. Training is a loop of small corrections that you will run yourself in numpy. '
                    'And then the practical question: for a table like our loans, is a network worth it, or does a simpler model do the job? You will find out with your own numbers.'),
        use_at_work='Judge whether a neural network earns its place: compare it with a simple model on the same split, and reuse a pretrained model when the data is images or text.',
        slides=[])
    S = sess['slides']

    S.append(dict(kind='table', title='Answers to the three questions from Session 19', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in sess['recall']], widths=[5.2, 6.8], icons=['calendar', 'flag', 'folder'],
                  notes=('Here are the answers to the three warm-up questions. We split a time series by date because a random split would let the model see months after the test months. That is data leakage, and next month always lies after the data you have. '
                         'A forecast must beat the baseline model, the seasonal naive forecast that copies the same month from last year. And we group by district before we shift, because otherwise the first month of a district borrows its lag from the district above it. '
                         'Today the same test applies to a neural network: it must beat a simple model. Which of the three did you find hardest?')))

    S.append(dict(kind='wide', title='An artificial neuron is a weighted sum plus a bias, passed through an activation function',
                  visual=dict(kind='dsj_neuron', inputs=[dict(name='late payments', x=float(F['nx'][0]), w=float(F['nw'][0])), dict(name='savings, UGX m', x=float(F['nx'][1]), w=float(F['nw'][1])), dict(name='loan, UGX m', x=float(F['nx'][2]), w=float(F['nw'][2]))],
                              bias=F['nb'], z=F['nz'], out=nout, act='sigmoid', out_label='risk score'),
                  caption='Illustrative loan and weights, never trained. Spreadsheet word for the sum: SUMPRODUCT.',
                  notes=(f'The smallest piece of a neural network is one artificial neuron, also called a perceptron. Here it scores one loan. The inputs are two late payments, savings of 0.4 million shillings, and a loan of 0.6 million. These weights are made up, to show the arithmetic. '
                         f'Each input is multiplied by its weight, and the three results are added with a bias of minus one. That gives a weighted sum, z, of {F["nz"]:.2f}. Then the activation function, here a sigmoid, bends z into a score between 0 and 1. The score is {nout:.3f}. '
                         'In a spreadsheet the weighted sum is SUMPRODUCT. Which input pushes the risk up, and which pushes it down?')))

    S.append(dict(kind='table', title='You already know the parts: the Excel word and the industry term',
                  headers=['In Excel', 'Industry term', 'Plain meaning'],
                  rows=[['SUMPRODUCT of inputs and multipliers', 'Weighted sum', 'Multiply each input by its weight, then add'], ['The multiplier beside each input', 'Weight (parameter)', 'How much the input counts; training adjusts it'],
                        ['The constant added at the end', 'Bias (intercept)', 'Where the neuron starts'], ['IF or MAX around a formula', 'Activation function', 'Bends the total: sigmoid or ReLU'],
                        ['Helper columns before the answer', 'Hidden layer', 'Neurons that build new variables'], ['Total of an error column', 'Loss function', 'One number for how wrong we are']],
                  widths=[3.8, 2.8, 5.4], icons=['calculator', 'key', 'pin', 'switch', 'grid', 'coin'],
                  notes=('Every part of a neuron has an Excel cousin. The weighted sum is SUMPRODUCT. The weights are the multipliers beside each input, and they are the parameters that training adjusts. The bias is the constant added at the end, the intercept you know from regression. '
                         'The activation function is like an IF or a MAX wrapped round a formula. A hidden layer is a set of helper columns between the data and the answer. And the loss function is the total of an error column. '
                         'Careful with the word bias. Here it is the intercept, which is a different idea from the bias in the bias-variance trade-off. Which of these rows is new to you?')))

    S.append(dict(kind='formula', title='The neuron as formulas: z is the weighted sum plus bias, and a is the activation',
                  formulas=[('Weighted sum plus bias', r'$z = w_1 x_1 + w_2 x_2 + w_3 x_3 + b$'), ('Sigmoid activation', r'$a = \sigma(z) = \frac{1}{1 + e^{-z}}$'),
                            ('Our neuron', r'$z = ' + f'{F["nw"][0]:g} \\times {F["nx"][0]:g} + ({F["nw"][1]:g}) \\times {F["nx"][1]:g} + {F["nw"][2]:g} \\times {F["nx"][2]:g} + ({F["nb"]:g}) = {F["nz"]:.2f}' + r'$')],
                  symbols=[['x_i', 'An input: one variable of the loan.', 'x = 2, 0.4, 0.6'], ['w_i', 'A weight: how much that input counts.', 'w = 0.9, -1.2, 1.5'], ['b', 'The bias (intercept).', 'b = -1'], ['z', 'The weighted sum plus the bias.', f'z = {F["nz"]:.2f}'], ['σ(z)', 'The sigmoid: squashes z into 0 to 1.', f'σ({F["nz"]:.2f}) = {nout:.3f}']],
                  size=18, note='This is the logistic regression you met in Session 15, packaged as one unit.',
                  notes=(f'Here is the same neuron as formulas. The weighted sum plus bias, z, is w one times x one, plus w two times x two, plus w three times x three, plus b. The sigmoid of z is one divided by one plus e to the power of minus z. '
                         f'With our numbers, z is {F["nz"]:.2f}, and the sigmoid of {F["nz"]:.2f} is {nout:.3f}. Notice that this is exactly the logistic regression you met in Session 15. A neuron with a sigmoid is a logistic regression packaged as one unit. '
                         'A network is many of these stacked. Which symbol on the table would training change?')))

    S.append(dict(kind='wide', title='Activation functions bend the total: sigmoid gives a probability and ReLU is common in hidden layers',
                  visual=dict(kind='dsj_activations', z_mark=(round(F['nz'], 2), '')),
                  caption='ReLU (rectified linear unit): 0 for a negative total, the total itself otherwise.',
                  notes=(f'The bend has a proper name, the activation function. On the left, the sigmoid squashes any total into a score between 0 and 1, which makes it right for a probability. On the right, ReLU, the rectified linear unit, gives 0 for a negative total and passes a positive total straight through. '
                         f'The gold dot is our neuron: z of {F["nz"]:.2f} gives {nout:.3f} on the sigmoid, and {F["nrelu"]:.2f} on ReLU. Why bend at all? Without a bend, stacking neurons would still give a straight line, however many you stack. '
                         'The bend is what lets a network learn curves. Which of the two would you put in the output of a default model?')))

    S.append(dict(kind='wide', title='Layers stack neurons into a feedforward neural network (multilayer perceptron, MLP)',
                  visual=dict(kind='dsj_mlp', layers=[('Input layer', F['n_features'], f'{F["n_features"]} variables'), ('Hidden layer 1', 16, '16 neurons'), ('Hidden layer 2', 8, '8 neurons'), ('Output layer', 1, 'chance of default')], note='Every neuron joins every neuron of the next layer'),
                  caption=f'Our loans network: {F["n_features"]} variables in, 16 and 8 neurons, 1 probability out. {F["net_params"]} weights and biases.',
                  notes=(f'Put neurons side by side and you have a layer. Feed one layer into the next and you have a feedforward neural network, also called a multilayer perceptron, or MLP. On the left, the input layer has one node for each of the twelve variables of a loan, the same twelve as Session 17. '
                         'Then two hidden layers, with sixteen and eight neurons. They are hidden because you never see their values in your data. The last circle is the output layer, one sigmoid neuron that gives the chance of default. '
                         f'Every line carries a weight, and every neuron has a bias. Count them all and the network has {F["net_params"]} parameters. Why is it called feedforward?')))

    S.append(dict(kind='table', title='Reading the network: layers, parameters and the arithmetic behind the count',
                  headers=['Term', 'Plain meaning', 'In our loans network'],
                  rows=[['Input layer', 'One node per variable. It holds the data.', f'{F["n_features"]} variables'], ['Hidden layer', 'Neurons that build new variables from the old ones.', '16 neurons, then 8'], ['Output layer', 'The prediction.', '1 sigmoid neuron: chance of default'],
                        ['Parameters', 'Every weight and bias that training adjusts.', f'{F["n_features"]}×16+16, 16×8+8, 8×1+1 = {F["net_params"]}'], ['Feedforward', 'Values move from input to output, never backwards.', 'when predicting']],
                  widths=[2.4, 5.0, 4.6], icons=['grid', 'gear', 'check', 'key', 'flag'], note='More neurons mean more parameters, and more room to memorise the training set.',
                  notes=(f'Here are the terms again, with the loans network. The input layer holds the data, twelve variables. The hidden layers build new variables from the old ones, sixteen neurons and then eight. The output layer is the prediction. '
                         f'The parameters are every weight and bias. Between the inputs and the first hidden layer there are twelve times sixteen weights plus sixteen biases, which is {p1}. Then sixteen times eight plus eight, which is {p2}. Then eight times one plus one, which is {p3}. '
                         f'Together, {F["net_params"]}. Logistic regression on the same data has only {F["logit_params"]}. Why might more parameters be a risk?')))

    S.append(dict(kind='formula', title='The loss function is one number for how wrong the predictions are',
                  formulas=[('Squared error loss for one record', r'$L = (\hat{y} - y)^2$'), ('Our one-weight example: x = 2 and the target is 6', r'$\hat{y} = 2w \quad L(w) = (2w - 6)^2$'), ('At w = 0', r'$L(0) = (0 - 6)^2 = 36$')],
                  symbols=[['y', 'The actual value (the target).', 'y = 6'], ['ŷ (y-hat)', 'The prediction of the model.', 'ŷ = w × x = 2w'], ['w', 'The weight that training adjusts.', 'starts at w = 0'], ['L', 'The loss for one record.', 'L(0) = 36']],
                  size=22, note='A classifier usually uses log loss (cross-entropy). Training means lowering the loss.',
                  notes=('To train a network we need one number that says how wrong it is. That is the loss function. For one record, the squared error loss is the prediction minus the actual value, squared. Here is a tiny example you will run yourself. '
                         'One input, x equals two, and the target is six. The prediction is two times the weight w, so the loss is two w minus six, squared. At w equal to zero, the loss is thirty-six. '
                         'A classifier usually uses log loss instead, also called cross-entropy, but the idea is the same: training means lowering the loss. What weight gives a loss of zero?')))

    S.append(dict(kind='idea', title=f'Gradient descent walks the weight downhill: w goes from 0 to {ws[-1]:.2f} in 8 steps',
                  visual=dict(kind='dsj_descent', weights=[float(v) for v in ws], losses=[float((2 * v - 6) ** 2) for v in ws], start_label='start: w = 0, loss 36', end_label=f'after 8 steps:\nw = {ws[-1]:.2f}'),
                  lead='Gradient descent lowers the loss one small step at a time.',
                  points=['Gradient: the slope of the loss at the current weight.', 'Learning rate: the size of each step.', 'New weight = old weight minus learning rate times gradient.'],
                  notes=(f'This is the loss curve for our one-weight example. The horizontal axis is the weight, the vertical axis is the loss. We start at w equal to zero, where the loss is thirty-six. At each step we measure the gradient, which is the slope of the curve at that point, and we move the weight a little downhill. '
                         f'The size of the move is the learning rate times the gradient. Look at the dots: the first steps are big because the slope is steep, and the steps shrink as we near the bottom. After eight steps the weight is {ws[-1]:.2f}, close to the best value of 3. '
                         'Why do the steps shrink by themselves?')))

    S.append(dict(kind='code', title='Read the recipe: gradient descent on one weight',
                  code=code_loop, output=lines,
                  reads=['Line 1 sets the input, target, start weight and learning rate.', 'Line 3 is the loss. Line 4 is the gradient.', 'Line 5 moves the weight against the slope.', f'Real output: w climbs to {ws[-1]:.2f}, the loss falls toward 0.'],
                  notes=('Read this recipe. Line one sets the input, the target, the starting weight and the learning rate. The loop runs eight steps. Each step computes the loss, then the gradient, which is two times the error times the input, then moves the weight against the slope. '
                         f'The output is real, and it prints steps one, two, four and eight. The weight goes from zero to 1.2 on the first step, then 1.92, then 2.611, and ends at {ws[-1]:.2f}. The loss printed on each line is the loss before that step, so it falls from thirty-six toward zero. '
                         'A real network does exactly this, with thousands of weights instead of one. In the lab you run this loop yourself. What would happen if the learning rate were bigger?')))

    S.append(dict(kind='table', title='The learning rate decides whether training settles, bounces or blows up',
                  headers=['Learning rate', 'Weight after 8 steps', 'Loss after the 8th update', 'What happens'],
                  rows=[['0.05', f'{fw[0.05]:.2f}', f'{fl[0.05]:.3f}', 'Settles: each step is smaller than the last.'], ['0.25', f'{fw[0.25]:.1f}', f'{fl[0.25]:.1f}', 'Bounces: the weight jumps between 0 and 6 and never settles.'],
                        ['0.5', f'{fw[0.5]:,.0f}', f'{fl[0.5]:,.0f}', 'Blows up: each step overshoots by more than the last.']],
                  widths=[2.2, 2.8, 2.8, 4.8], icons=['check', 'question', 'cross'], note='Same loop, same target. Best weight: 3, loss 0. The recipe on the last slide prints the loss before each update, so its last line shows a larger loss.',
                  notes=(f'The learning rate is the size of each step, and it matters a great deal. With 0.05, the weight settles near 3 and the loss after the eighth update is {fl[0.05]:.3f}. The recipe prints the loss before each update, so its last line shows a larger number. '
                         f'With 0.25, every step overshoots exactly to the other side, so the weight jumps between 0 and 6 forever and the loss stays at {fl[0.25]:.0f}. '
                         f'With 0.5, each step overshoots by more than the last, and after eight steps the weight is minus {abs(fw[0.5]):,.0f} and the loss is about {fl[0.5]:,.0f}. '
                         'In real networks you see this as a loss that stops falling or turns into a not-a-number error. What would you try first if the loss rose?')))

    S.append(dict(kind='wide', title='Backpropagation works out how much each weight changed the loss, so gradient descent can adjust them all',
                  visual=dict(kind='network'),
                  caption='Backpropagation: send the error backwards to find each weight\'s gradient, its effect on the loss.',
                  notes=('With one weight, the gradient is easy. A network has thousands. Backpropagation is the method that finds the gradient of every weight. First the network makes a forward pass: the inputs go through the layers and produce a prediction. '
                         'Then we compute the loss. Then the error flows backward, from the output layer toward the inputs, and for each weight we work out how much it changed the loss, which is its gradient, using the chain rule. '
                         'Gradient descent then moves every weight a little against its own gradient. You will not code backpropagation in this course. A library does it. What matters is the loop: forward, loss, backward, adjust. Which step is the new idea for you?')))

    S.append(dict(kind='wide', title='One epoch is one pass over the training set, made of many batches',
                  visual=dict(kind='dsj_epoch', n_rows=F['n_train'], batch=F['batch'], n_batches=F['n_batches']),
                  caption='MLPClassifier uses batches of up to 200 records by default (check your version).',
                  notes=(f'Two more training words. A batch is the group of records the network looks at before it adjusts its weights once. An epoch is one full pass over the training set. '
                         f'In our loans, the training set has {n(F["n_train"])} records. With batches of up to {F["batch"]}, that is {F["n_batches"]} batches, so one epoch makes {F["n_batches"]} adjustments of the weights. '
                         'Training runs for many epochs, and in scikit-learn the setting max_iter limits them. Why not adjust the weights only once per epoch, after all the records?')))

    S.append(dict(kind='wide', title=f'Overfitting again: after epoch {F["of_best_epoch"]} the training loss keeps falling and the test loss rises',
                  visual=dict(kind='dsj_lines', series=[dict(name='Training loss (300 loans)', values=F['of_train_loss'], color='ink'), dict(name='Test loss (2,000 loans)', values=F['of_test_loss'], color='red')],
                              ticks=[(0, '0'), (20, '200'), (40, '400'), (60, '600'), (80, '800')], cut=F['of_best_epoch'] // 10, cut_label='|lowest test loss', ylabel='log loss', yticks=[0.2, 0.4, 0.6], yfmt='{:.1f}', ymin=0.0),
                  caption=f'A {F["n_features"]}-64-64-1 network on only 300 training loans. Epochs run along the bottom.',
                  notes=(f'This picture shows overfitting again. I trained a larger network, with {n(F["of_params"])} parameters, on only 300 loans, and measured the loss on those 300 and on 2,000 loans it never saw. The black line, the training loss, keeps falling toward zero. '
                         f'The red line, the test loss, reaches its lowest value around epoch {F["of_best_epoch"]}, then climbs. The network is memorising the 300 loans. At the end its AUC on the training loans is {F["of_auc_train"]:.2f}, and on the test loans {F["of_auc_test"]:.2f}. '
                         'A training score alone would have fooled us. Which score would you quote to a manager?')))

    S.append(dict(kind='list', title='Four ways to fight overfitting in a network',
                  items=['Use fewer neurons or fewer layers: a smaller network has less room to memorise.', 'Regularisation: MLPClassifier has an alpha setting that penalises large weights.',
                         'Early stopping: stop training when the validation loss stops improving (early_stopping=True).', 'More training records: the most reliable cure when you can get them. Always judge on the test set.'],
                  icons=['gear', 'shield', 'clock', 'folder'],
                  notes=('There are four standard ways to fight overfitting in a network. Use fewer neurons or fewer layers, so there is less room to memorise. Use regularisation: in scikit-learn the alpha setting of MLPClassifier penalises large weights. '
                         'Use early stopping, which stops training when the validation loss stops improving, and which you switch on with early stopping equals true. And get more training records, which is the most reliable cure. '
                         'Whatever you do, judge on the test set and never on the training score. Which of these would you try first on the loans?')))

    S.append(dict(kind='compare', title='Network or forest on a table? Make the network earn its place',
                  left=dict(head='Neural network (MLP)', points=['Needs imputing and scaling first.', 'Many settings. Trains with Adam by default, a smarter gradient descent.', 'Hard to explain to a manager.']),
                  right=dict(head='Random forest', points=['Works on raw numbers, no scaling.', 'Few settings, strong defaults.', 'Shows which variables mattered.']),
                  verdict='On a table, start simple. Keep the network only if it wins by enough to matter.',
                  notes=('Now the practical question. For a table of numbers like the loans, which do you use? A neural network needs imputing and scaling, has many settings, and is hard to explain to a manager. In scikit-learn the MLPClassifier trains with a variant of gradient descent called Adam by default: the same idea with smarter step sizes. '
                         'A random forest works on raw numbers, has few settings with strong defaults, and shows which variables mattered. My understanding of published comparisons is that on tables, tree-based models often match or beat neural networks. '
                         'That is a general finding, so test it on your own data. The rule is simple: start with the simpler model, and make the network earn its place. What would count as winning by enough to matter?')))

    S.append(dict(kind='table', title=f'On the loans table a numpy network does no better than logistic regression: {F["net_params"]} parameters, no gain',
                  headers=['Model', 'Parameters', 'Test AUC', 'Where the number comes from'],
                  rows=[['Logistic regression (numpy)', str(F['logit_params']), f'{F["auc_logit_test"]:.3f}', 'Computed here in numpy'], [f'Network {F["n_features"]}-16-8-1 (numpy)', str(F['net_params']), f'{F["auc_net_test"]:.3f}', 'Computed here in numpy'],
                        ['MLPClassifier (scikit-learn)', str(F['net_params']), 'You compute it', 'Your lab'], ['RandomForestClassifier', 'many trees', 'You compute it', 'Your lab']],
                  widths=[3.4, 2.0, 2.5, 4.1], icons=['coin', 'gear', 'grid', 'plant'],
                  note=f'Same {n(F["n_loans"])} loans and the same {n(F["n_test"])} test loans as Sessions 14 to 17 ({F["test_defaults"]} defaults). collection_calls is left out because it leaks the answer: with it the AUC would be above 0.99.',
                  notes=(f'Here is what I measured in numpy on the same eight thousand loans and the same two thousand test loans as Sessions 14 to 17. Logistic regression, which is a network with no hidden layer, reaches a test AUC of {F["auc_logit_test"]:.3f} with {F["logit_params"]} parameters. '
                         f'My numpy network with sixteen and eight hidden neurons reaches {F["auc_net_test"]:.3f} with {F["net_params"]} parameters. So on this table the extra parameters buy nothing. Your scikit-learn runs in the lab will land near these numbers. '
                         f'And the column collection calls would push the AUC above 0.99, because it only exists after a loan goes bad. That is data leakage again. What would you recommend to the credit team?')))

    S.append(dict(kind='wide', title='Transfer learning reuses a pretrained model and trains only a new last layer',
                  visual=dict(kind='dsj_transfer'),
                  caption='Pretrained model: trained by someone else. Inference: using a trained model to predict.',
                  notes=('Some tasks, like recognising objects in photos, need networks with millions of parameters and huge training sets. You will not train those. You reuse a pretrained model, which someone else trained on a large collection of images. '
                         'The early layers have learned general things, like edges, colours and textures. The middle layers have learned shapes. In transfer learning we freeze those layers and replace the last layer with a new one, which we train on our own photos. '
                         'That needs only a small number of labelled photos. And using a trained model to predict, without training it, is called inference. What photos could you label in your own work?')))

    S.append(dict(kind='table', title='Four terms for using a network somebody else trained',
                  headers=['Term', 'Plain meaning', 'Example'],
                  rows=[['Pretrained model', 'A network already trained on a large dataset by someone else.', 'An image classifier published on the Hugging Face Hub'], ['Inference', 'Using a trained model to predict. No training happens.', 'Classify one new photo'],
                        ['Transfer learning', 'Reuse the early layers and train a new last layer on your own data.', 'A few hundred labelled photos of your own crops (illustrative)'], ['Fine-tuning', 'Also adjust some of the pretrained weights, with a small learning rate.', 'Needs more data and more care']],
                  widths=[2.6, 5.2, 4.2], icons=['folder', 'magnifier', 'gear', 'clock'], note='Before you use a pretrained model at work, read its model page: the licence, the training data and the download size.',
                  notes=('Four terms to keep apart. A pretrained model is a network someone else trained on a large dataset. Inference means using a trained model to predict, with no training. Transfer learning means reusing the early layers and training a new last layer on your own data. '
                         'Fine-tuning goes further and also adjusts some of the pretrained weights, with a small learning rate, so it needs more data and more care. Before you use a pretrained model at work, read its model page, and check the licence, the training data and the download size. '
                         'Which of the four would a small team with a few hundred photos use?')))

    S.append(dict(kind='table', title='When deep learning is worth it: match the tool to the kind of data',
                  headers=['Kind of data', 'Usually the best first tool', 'Why'],
                  rows=[['A table of numbers: loans, orders, clinic visits', 'Logistic regression, random forest, gradient boosting', 'Few records per variable, and you must explain the result'], ['Images and photos', 'Pretrained network with transfer learning', 'Pixels are not meaningful variables on their own'],
                        ['Text and speech', 'Pretrained language or speech model', 'Meaning depends on the words around each word'], ['Very large data with a hard pattern', 'Deep learning trained on a GPU', 'Needs a lot of data and computing power']],
                  widths=[3.8, 4.2, 4.0], icons=['grid', 'phone', 'speech', 'gear'], note='This is my understanding of the usual pattern. Always test the simple model first on your own data.',
                  notes=('So when is deep learning worth it? For a table of numbers, like loans, orders or clinic visits, start with logistic regression, a random forest or gradient boosting, because you have few records per variable and you must explain the result. '
                         'For images, use a pretrained network with transfer learning. For text and speech, use a pretrained language or speech model, which we meet in the next sessions. '
                         'Only for very large data with a hard pattern do you train a deep network yourself, and that needs lots of data and computing power, often a GPU. Which kind of data do you work with most?')))

    S.append(dict(kind='table', title='Where you will use this at work: judge the network, reuse the pretrained model',
                  headers=['Your job', 'The task you meet', 'What today lets you do'],
                  rows=[['Credit analyst at a bank, using scikit-learn', 'Default or late repayment on a table of loans', 'Compare a network, a forest and logistic regression on one split, then recommend the simplest that is good enough.'],
                        ['Agriculture extension officer with a phone', 'Photos of crop leaves (illustrative)', 'Know that a pretrained image model with transfer learning is the starting point, and what labelled photos it needs.'],
                        ['Data team lead reviewing a vendor pitch', 'A vendor says its AI forecast uses deep learning', 'Ask which baseline it beats, on which test set, and by how much.'],
                        ['Analyst handing results to managers', 'A score of 99 percent on training data', 'Recognise overfitting and ask for the test score.']],
                  widths=[3.4, 3.6, 5.0], icons=['coin', 'plant', 'people', 'shield'],
                  notes=('Where will you use this on Monday? Four examples. A credit analyst at a bank who uses scikit-learn can compare a network, a forest and logistic regression on one split, and recommend the simplest one that is good enough. '
                         'An agriculture extension officer can know that photos of crop leaves call for a pretrained image model with transfer learning, and what labelled photos it needs. That example is illustrative. '
                         'A data team lead reviewing a vendor pitch can ask which baseline the deep learning forecast beats, on which test set. And any analyst can recognise a 99 percent score on training data as overfitting. Which of these is closest to your job?')))

    S.append(dict(kind='code', title='Read the recipe before the lab: a network in a scikit-learn Pipeline',
                  code=code_mlp,
                  reads=['make_pipeline chains the imputer, the scaler and the network in order.', 'hidden_layer_sizes=(16, 8) means two hidden layers.', 'max_iter=500 limits the epochs. random_state=42 makes the run repeatable.', 'predict_proba gives the chance of default. roc_auc_score scores it on the test set.', 'You run this in the lab, and the AUC appears in your notebook.'],
                  notes=('Read this recipe before the lab. Make pipeline chains three steps: the imputer fills blank incomes with the median, the scaler standardises each variable, and the MLPClassifier is the network. '
                         'Hidden layer sizes sixteen and eight gives the two hidden layers from our picture. Max iter limits the number of epochs, and random state makes the run repeatable. '
                         'Predict proba gives the chance of default for each test loan, and roc auc score turns those chances into the AUC. Because the imputer sits inside the pipeline, the median comes from the training rows only. Sessions 14 to 17 computed it on all loans before the split, on purpose, to keep things simple. No output is shown here, because you will produce it yourself. Why must the scaler sit inside the pipeline?')))

    S.append(dict(kind='divider', title='Part 2: the neural network lab', lead='Close the slides. Open the notebook.', section='Lab',
                  notes=('That is the end of the ideas. Everything you need is on the slides you have just seen, and the notebook repeats each step. Open the Session 20 notebook in Google Colab and run the setup cell first. '
                         'In every task, predict the answer first and write your guess in the notebook. Then run the cell, read the output, and change one thing. We also spend ten minutes in TensorFlow Playground in your browser.')))

    S.append(dict(kind='steps', title='The lab has five parts and ends with a recommendation to the credit team',
                  steps=[dict(head='1 Neuron', text='Weighted sum, sigmoid, ReLU', icon='gear'), dict(head='2 Training loop', text='Gradient descent on one weight', icon='clock'), dict(head='3 Playground', text='Watch a network learn and overfit', icon='laptop'),
                         dict(head='4 Loans', text='MLPClassifier against a random forest', icon='chart'), dict(head='5 Decide', text='Results table, three sentences', icon='pin')], highlight=None,
                  caption='Predict, run, read, change one thing. Automatic checks tell you when a number is right.',
                  notes=('Here is the map of the lab. Part one, build a neuron in numpy and change its weights. Part two, run the gradient descent loop and try three learning rates. Part three, spend ten minutes in TensorFlow Playground and record what you see. '
                         'Part four, train an MLPClassifier and a random forest on the loans, and compare their AUC on the same test set. Part five, put the results in one table and write three sentences recommending a model to the credit team. '
                         'Those three sentences and the table are what you keep. Please do not skip the predictions.')))

    S.append(dict(kind='wide', title='TensorFlow Playground lets you watch a small network learn in your browser',
                  visual=dict(kind='dsj_playground'),
                  caption='Sketch of the screen. The real page may look different. Free, in the browser, no account.',
                  notes=('TensorFlow Playground is a free page in your browser where you can build a small network and watch it learn. This is a sketch of the screen, and the real page may look a little different. '
                         'On the left you choose the data, such as circles or a spiral, and set the noise. Then you choose the input features. In the middle you add hidden layers and neurons with the plus and minus buttons. On the right you see the dots coloured by the network, and the training loss and test loss. '
                         'The bar at the top holds the learning rate and the activation function. Press play, and watch. What do you expect a network with no hidden layer to do with the circle?')))

    S.append(dict(kind='table', title='Four Playground challenges: change one thing and write down what you see',
                  headers=['Challenge', 'What to change', 'What to record'],
                  rows=[['1 Circle', 'Start with no hidden layer. Then add one hidden layer with 4 neurons.', 'Can it separate the circle each time? How long does it take?'], ['2 Spiral', 'Add a second hidden layer and more neurons.', 'The test loss before and after. Which size is enough?'],
                        ['3 Overfitting', 'Raise the noise, use few training points, train for a long time.', 'When do the training loss and the test loss separate?'], ['4 Learning rate', 'Try a very small and a very large learning rate. Try ReLU and tanh (a bend that gives values from -1 to 1).', 'Which settings fail, which are slow, which are fast?']],
                  widths=[2.0, 5.2, 4.8], icons=['pin', 'chart', 'cross', 'clock'], note='Ten minutes. Write in the notebook text cell. There is no single right answer: record what you see.',
                  notes=('Four challenges, ten minutes in total. One, the circle: start with no hidden layer and then add one with four neurons, and record what changes. Two, the spiral: add layers and neurons until the test loss is low. '
                         'Three, overfitting: raise the noise, use few training points and train for a long time, and record when the training loss and the test loss separate. Four, try a very small and a very large learning rate, and try ReLU against tanh. '
                         'Write what you see in the notebook. There is no single right answer. Which setting surprised you most?')))

    S.append(dict(kind='statement', title='Optional: use a pretrained image classifier in Colab', lead='Only if you finish early.',
                  points=['The first run downloads the model weights from the Hugging Face Hub (free, tens of megabytes or more).', 'Read the model page first: licence and size.', 'Never upload photos of people or customers.', 'Needs torch or TensorFlow: use the Colab CPU runtime.'],
                  icons=['cloud', 'doc', 'shield', 'notebook'],
                  notes=('This part is optional, and only for those who finish early. The notebook has a few lines, commented out, that use a pretrained image classifier. The first run downloads the model weights from the Hugging Face Hub. The download is free, but check the model page for its size and its licence, because both can change. '
                         'Use only photos you are allowed to use, and never upload photos of people or customers. The code is commented out, and it needs torch or TensorFlow and a download of tens to hundreds of megabytes, so use the Colab CPU runtime. The point is inference with a model you did not train. If you do not have time, you lose nothing: the checks do not depend on it. '
                         'Is there a photo task in your own work that this could help with?')))

    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Neuron score for the loan (1, 0.8, 0.3), and with first weight 4.5', f'{F["lab_score"]:.3f} and {F["lab_score2"]:.3f}'], ['ReLU of the weighted sum', 'about 0.0 for z = -0.61'], ['Weight after 8 steps at learning rate 0.05', f'{fw[0.05]:.2f}'],
                        ['Loss after 8 steps at learning rate 0.5', 'above 100 (it blows up)'], ['Parameters of a 10-16-8-1 network, batches per epoch', f'{F["net_params"]} and {F["n_batches"]}'],
                        ['Loans kept, training records, test records (defaults)', f'{n(F["n_loans"])}, {n(F["n_train"])} and {n(F["n_test"])} ({F["test_defaults"]})'], ['Test AUC of the MLPClassifier and of the forest', 'between 0.70 and 0.78; yours will differ'], ['Training AUC minus test AUC of the big network on 300 loans', 'above 0.1']],
                  widths=[7.4, 4.6], icons=['gear', 'switch', 'clock', 'cross', 'grid', 'folder', 'chart', 'shield'], note='If your number differs, find the task that went wrong.',
                  notes=('Use this table as your own self-check. Nobody marks it. The first rows are exact: the neuron scores, the weight after eight steps, the parameter count and the loan counts. If one does not match, stop and call me. '
                         f'The AUC rows are different. A scikit-learn network starts from random weights and uses its own optimiser, so your AUC will land between zero point seven and zero point seven eight. A training AUC far above the test AUC is expected for the network and the forest. The check accepts a range. '
                         'Find out why it differs. What does it mean if your forest scores above 0.85 on the test loans?')))

    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[['ConvergenceWarning: maximum iterations reached', 'Training stopped before the loss settled.', 'Raise max_iter, or accept it if the AUC is stable.'], ['ValueError: input contains NaN', 'Blank incomes reached the network.', 'Put SimpleImputer first in the Pipeline.'],
                        ['AUC above 0.99', 'collection_calls is in X. It leaks the answer.', 'Drop it from the variables.'], ['The loop weight becomes huge or nan', 'The learning rate is too big.', 'Use 0.05 and look at each step.'],
                        ['Your AUC differs from the slides', 'Random starting weights, or a different split.', 'Up to about 0.03 is expected. Above 0.05 means a different split or variable list.']],
                  widths=[3.8, 4.0, 4.2], icons=['cross'] * 5,
                  notes=('Five messages you may meet. A ConvergenceWarning about maximum iterations means training stopped before the loss settled, so raise max iter, or accept it if the AUC is stable. A ValueError about NaN means blank incomes reached the network, so put the imputer first. '
                         'An AUC above 0.99 means collection calls is in your variables, and it leaks the answer. A weight that becomes huge or nan means the learning rate is too big. And a small difference from my numbers is normal. Read the message first. It usually tells you the answer.')))

    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[['What does one artificial neuron compute?', 'A weighted sum of its inputs plus a bias, passed through an activation function such as sigmoid or ReLU.'],
                        ['In gradient descent, what does the learning rate control, and what happens if it is too big?', 'The size of each step. Too big and the weight overshoots, bounces or blows up.'],
                        ['A network scores 1.00 AUC on the training loans and 0.65 on the test loans. What is wrong and what do you try?', 'Overfitting. Try a smaller network, regularisation, early stopping or more records, and quote the test score.']],
                  widths=[5.6, 6.4], icons=['gear', 'clock', 'shield'],
                  notes=('Last, the exit check. Three questions. Write your answers before you look at mine. One, what does one artificial neuron compute? Two, in gradient descent, what does the learning rate control, and what happens if it is too big? '
                         'Three, a network scores 1.00 AUC on the training loans and 0.65 on the test loans: what is wrong and what do you try? '
                         'The short answers are on the slide. If you got all three, you are ready for Session 21. If one surprised you, look at that step in your notebook again tonight.')))

    sess['facilitator'] = dict(
        prep=['Open the deck and the Session 20 notebook in Colab before anyone arrives. Open TensorFlow Playground in a browser tab and check it loads on the room network.',
              'Run the solution notebook once in Colab. The numpy cells were run in the authoring sandbox. The MLPClassifier, RandomForestClassifier and LogisticRegression cells were NOT run there (no scikit-learn), and the reference numbers come from numpy replicas: before the course starts, confirm on real scikit-learn in Colab that the AUC checks pass, and widen a tolerance if they do not. The real MLPClassifier uses the Adam solver and usually overfits more than the numpy network, so a training AUC far above the test AUC is expected.',
              'Write the check table (slide 28) on the board before the lab. Warn learners that the AUC rows are ranges.', 'Concepts run with laptops closed. Learners open the notebook only after the Part 2 divider.',
              'The optional pretrained model cell is commented out. If you run it, check the model page for the licence and download size first, and do not upload photos of people.'],
        misconceptions=[('A neural network is always better than the older models', f'On the loans table a numpy network reaches {F["auc_net_test"]:.3f} AUC against {F["auc_logit_test"]:.3f} for logistic regression. Compare on the same split and prefer the simpler model when scores are close.'),
                        ('A high training score means a good model', f'The big network scores {F["of_auc_train"]:.2f} AUC on its 300 training loans and {F["of_auc_test"]:.2f} on the test loans. Quote the test score.'),
                        ('Deep learning needs a lot of maths to use', 'The idea is a weighted sum with a bend, repeated. Libraries do backpropagation. You need to know the settings and how to test.'),
                        ('A bigger learning rate trains faster, so bigger is better', 'Past a limit it bounces or blows up, as the one-weight experiment shows.'),
                        ('A pretrained model is free to use in any way', 'The download is usually free, but the licence and the training data differ by model. Read the model page.')],
        probes=[('What is the bias of a neuron?', 'The constant added to the weighted sum. It is the intercept, a different idea from the bias of the bias-variance trade-off.'),
                ('Why do we need an activation function?', 'Without it, stacked neurons collapse to a straight line. The bend lets a network learn curves.'),
                ('What is the difference between an epoch and a batch?', f'A batch is the group of records used for one adjustment. An epoch is one pass over all training records: {F["n_batches"]} batches here.'),
                ('What is backpropagation?', 'The method that sends the error backwards and works out the gradient of every weight with the chain rule.'),
                ('Why is the scaler inside the Pipeline?', 'So the mean and standard deviation are learned from the training records only, then reused on the test records.')],
        lab_steps=[('Step 1: neuron', f'{F["lab_score"]:.3f} for the loan [1, 0.8, 0.3]. With the first weight 4.5 it is {F["lab_score2"]:.3f}. ReLU of the negative total is 0.'), ('Step 2: training loop', f'w = {fw[0.05]:.2f} after 8 steps at 0.05. Learning rate 0.25 bounces between 0 and 6. Learning rate 0.5 blows up.'),
                   ('Step 3: Playground', 'Ten minutes. Collect two observations aloud. Praise precise notes (what changed, what was seen).'), ('Step 4: loans', f'{n(F["n_loans"])} loans, {n(F["n_train"])} to train, {n(F["n_test"])} to test ({F["test_defaults"]} defaults). AUCs between 0.70 and 0.78. Make sure collection_calls is out.'),
                   ('Step 5: decide', 'A results table and three sentences. The best answers say that the simple model is good enough unless the network wins clearly.')],
        rescue=['If the concepts run over, shorten the loan comparison slide and the pretrained terms slide; the lab covers both.', 'If only 30 minutes of lab remain, do steps 1, 2 and 4, and set Playground as homework.',
                'If Colab is slow, reduce max_iter to 200 and accept a ConvergenceWarning.', 'If a learner has no laptop, pair them with a neighbour: one types, one predicts aloud.'],
        after=['Collect the results table and the three sentences.', 'Ask each learner to name one task in their work where a pretrained model could replace training.', 'Note any question you could not answer and open Session 21 with it.'],
        lab_answer_key=[['Step 1 PREDICT: will the loan [1, 0.8, 0.3] score above or below 0.5?', f'Below: z = {F["lab_z"]:.2f}, score {F["lab_score"]:.3f}.'],
                        ['Step 1 CHANGE: make the first weight larger.', f'With 4.5 the score is {F["lab_score2"]:.3f}. A larger weight on late payments raises the risk score.'],
                        ['Step 2 READ: what does the weight do after 8 steps?', f'It reaches {fw[0.05]:.2f}, close to the best value 3.'],
                        ['Step 2 CHANGE: learning rate 0.25 and 0.5.', f'At 0.25 the weight jumps between 0 and 6. At 0.5 the loss after 8 steps is about {fl[0.5]:,.0f}.'],
                        ['Step 4 READ: does the network beat logistic regression?', f'Probably not by much: reference AUCs {F["auc_net_test"]:.3f} (numpy network) and {F["auc_logit_test"]:.3f} (numpy logistic regression).'],
                        ['Step 4 CHANGE: add collection_calls.', 'The AUC jumps above 0.99. It is data leakage, so never keep it.'],
                        ['Step 4 READ: what is the gap between training AUC and test AUC for the big network on 300 loans?', f'About {F["of_auc_train"]:.2f} against {F["of_auc_test"]:.2f} in the numpy reference: overfitting. Your scikit-learn gap should also be well above 0.1.'],
                        ['Step 5 READ: which model do you recommend?', 'Any answer backed by the table. If the AUCs are within about 0.02, recommend the simplest, which is logistic regression.']])
    return sess
