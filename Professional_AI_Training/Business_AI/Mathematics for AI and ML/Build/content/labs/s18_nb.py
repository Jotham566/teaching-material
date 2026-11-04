"""Session 18 course project (Python): five builds, with automatic self-checks and no marks.
A learner may type a student ID in the first code cell. It only seeds a personal dataset (regression points, logistic data, PCA cloud, XOR-style data, attention embeddings), so every learner has different numbers.
It is not a test. The learner writes functions with fixed names; the check cell calls them on the learner's data and on a second dataset and compares with reference implementations
(the SHARED block of Build/autocheck/project_selfcheck.py, copied into the notebook so that notebook and script always agree). The checks show OK or NOT YET and nothing is recorded.
The slides and the guided workbook use separate seed-free toy numbers, computed by toy() below."""
import contextlib
import io
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
BUILD = HERE.parents[1]
sys.path.insert(0, str(BUILD / 'kit'))
from nb import Notebook  # noqa: E402

TITLE = 'Course project: five builds from first principles'
CHECKFILE = BUILD / 'autocheck' / 'project_selfcheck.py'
PLACEHOLDER = 'PUT-YOUR-STUDENT-ID-HERE'
SOLUTION_ID = 'KLAI-SOLUTION-0000'


def shared_source():
    t = CHECKFILE.read_text(encoding='utf-8')
    return t.split('# >>> SHARED BEGIN', 1)[1].split('# <<< SHARED END', 1)[0].split('\n', 1)[1]


def n_checks():
    """Number of checks the notebook prints: every check on your data and on the second dataset, plus the ID check."""
    ns = {}
    exec(shared_source(), ns)
    return 2 * len(ns['CHECKS']) + 1


def _todo(nb, solution, hint, stub, code):
    nb.code(f'# {hint}\n' + (code if solution else stub))


HELPER_EXTRA = '''
PLACEHOLDER = "PUT-YOUR-STUDENT-ID-HERE"
HIDDEN = make_datasets(20260518)      # a second small dataset that only the checks use

def run_build(k):
    """Runs the checks of build k on YOUR data and on a second dataset, calling YOUR functions."""
    L = {n: globals().get(n) for n in NAMES}
    for b, cid, label, fn in CHECKS:
        if b == k:
            for tag, D in (("your data", DATA), ("second dataset", HIDDEN)):
                check(BUILD_NAMES[b] + ": " + label + ", " + tag, run_check(fn, D, L), True, 0)

def show(label, thunk):
    """Prints thunk() or says why it does not work yet (so an unfinished function does not stop the notebook)."""
    try:
        print(label + ":", thunk())
    except Exception as e:
        print(label + ": not working yet (" + type(e).__name__ + ")")'''


def build(solution=False):
    nb = Notebook()
    nb.md('# Session 18 course project: five builds from first principles\n\nKLAi | Mathematics for AI and Machine Learning | **Your project. Automatic self-checks, no marks**\n\n'
          'You build five things with numpy only: **(1) linear regression**, **(2) logistic regression**, **(3) PCA**, **(4) a small neural network with backpropagation** and **(5) scaled dot-product attention**. '
          'Each build is one or more **functions with fixed names**, which you write in the cells marked "your code here".\n\n'
          '**How the self-checks work.** There is no exam and there are no marks. Type a student ID in the first code cell (any text you like, even your own name). It only creates a personal dataset, so your numbers are your own and nobody else has the same ones. It is not a test and nothing is sent anywhere. '
          'The checks call YOUR functions on YOUR data and on a second dataset, and compare the results with a reference. Each check shows OK or NOT YET, so you can see which build still needs work. No expected number is printed, so the way to see OK is to write a function that really computes the answer. '
          'Each check names its build. The last cell says "All N checks pass" when everything is right.\n\n'
          '**Rules.** Use numpy only. Run the cells in order from the top. You may look at your notes, the slides and earlier notebooks, and you may talk with others and ask an assistant to explain an idea. The project is yours to build and keep. '
          'The spreadsheet version is a guided workbook with fixed toy numbers and its own checks.')
    nb.code(f'STUDENT_ID = "{SOLUTION_ID if solution else PLACEHOLDER}"      # type your student ID between the quotes, then run this cell')
    nb.check_setup()
    nb.code('# Self-check helper: data generators, reference implementations and checks. Run this cell once. You do not need to read it.\n' + shared_source().strip('\n') + '\n' + HELPER_EXTRA)
    nb.code('SEED = seed_from_id(STUDENT_ID)\nDATA = make_datasets(SEED)            # all your datasets, generated from your ID\n'
            'lin, logd, pca_data, xor_data, att_data = DATA["lin"], DATA["log"], DATA["pca"], DATA["xor"], DATA["att"]\n'
            'check("Setup: a student ID was entered", STUDENT_ID.strip().upper() != PLACEHOLDER and len(STUDENT_ID.strip()) > 2, True, 0)\n'
            'print("student ID:", STUDENT_ID, "  your seed:", SEED)')

    # ================================================================== build 1
    nb.step('1', 'Build 1: linear regression (normal equation and gradient descent)', 'Eight readings: hours of use x and energy used y in kWh. The model is y-hat = w0 + w1 x. '
            'The design matrix X has a column of ones first (for w0) and the hours second. Write two functions that return the weights w.')
    nb.code('X, y = lin["X"], lin["y"]                  # your design matrix (8 rows, 2 columns) and your energy readings\nprint("hours of use:", lin["x"])\nprint("energy used (kWh):", y)')
    nb.predict('Look at your own numbers. Roughly what slope w1 do you expect? (How much does y rise per extra hour?)')
    _todo(nb, solution, 'fit_linear(X, y): the weights that minimise the sum of squared errors, in one step (Build 1 slide). fit_linear_gd(X, y, lr, steps): the same weights by repeated small steps from w = 0',
          'def fit_linear(X, y):\n    return None  # your code here\n\ndef fit_linear_gd(X, y, lr, steps):\n    return None  # your code here',
          'def fit_linear(X, y):\n    return np.linalg.solve(X.T @ X, X.T @ y)\n\n'
          'def fit_linear_gd(X, y, lr, steps):\n    w = np.zeros(X.shape[1])\n    for _ in range(steps):\n        residual = X @ w - y\n        w = w - lr * 2 * X.T @ residual / len(y)\n    return w')
    nb.code('show("normal equation weights (w0, w1)", lambda: fit_linear(X, y))\nshow("gradient descent, lr 0.005, 400 steps", lambda: fit_linear_gd(X, y, 0.005, 400))\n'
            'show("your mean squared error", lambda: np.mean((X @ fit_linear(X, y) - y) ** 2))\nrun_build(1)')
    nb.change('Call `fit_linear_gd(X, y, 0.05, 400)` in a new cell. What happens to the weights, and why?')

    # ================================================================== build 2
    nb.step('2', 'Build 2: logistic regression (gradient descent)', 'Forty students: hours of study x and y = 1 if they passed. The model gives p = sigmoid(w0 + w1 x). The loss is the mean binary cross-entropy from Session 16. '
            'Write the sigmoid, the loss and the gradient descent function.')
    nb.code('Xl, yl = logd["X"], logd["y"]\nprint("hours of study (first 10):", logd["x"][:10])\nprint("passed (first 10):", yl[:10], "  share who passed:", yl.mean())')
    nb.predict('The gradient starts from w = 0, where every predicted probability is 0.5. Will w1 move up or down in the first step?')
    _todo(nb, solution, 'sigmoid(z); logistic_loss(w, X, y) = mean binary cross-entropy; fit_logistic(X, y, lr, steps): gradient descent from w = 0 (Build 2 slide)',
          'def sigmoid(z):\n    return None  # your code here\n\ndef logistic_loss(w, X, y):\n    return None  # your code here\n\ndef fit_logistic(X, y, lr, steps):\n    return None  # your code here',
          'def sigmoid(z):\n    return 1 / (1 + np.exp(-z))\n\n'
          'def logistic_loss(w, X, y):\n    p = sigmoid(X @ w)\n    return -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))\n\n'
          'def fit_logistic(X, y, lr, steps):\n    w = np.zeros(X.shape[1])\n    for _ in range(steps):\n        w = w - lr * X.T @ (sigmoid(X @ w) - y) / len(y)\n    return w')
    nb.code('show("loss at w = 0 (should be ln 2 = 0.693)", lambda: logistic_loss(np.zeros(2), Xl, yl))\nshow("weights after 2000 steps (lr 0.1)", lambda: fit_logistic(Xl, yl, 0.1, 2000))\n'
            'show("training accuracy", lambda: np.mean((sigmoid(Xl @ fit_logistic(Xl, yl, 0.1, 2000)) > 0.5) == (yl == 1)))\nrun_build(2)')
    nb.read('Is the model confident (probabilities near 0 or 1)? Why does the overlap between passes and fails stop it from being sure?')

    # ================================================================== build 3
    nb.step('3', 'Build 3: PCA via the covariance eigen-decomposition', 'Thirty points in two dimensions, in a tilted cloud that is not centred on zero. PCA centres the data, forms the covariance matrix (divide by n, the course convention) and finds its eigenvectors. '
            'The eigenvector with the largest eigenvalue is the first principal component. The sign of an eigenvector is arbitrary, so the checks accept either sign.')
    nb.code('P = pca_data["P"]                         # 30 rows, 2 columns\nprint("column means:", P.mean(axis=0))')
    nb.predict('Look at the first few rows of P. Do the two columns rise together? Which way will the first principal component point: along (1, 1), along (1, -1), or along (1, 0)?')
    _todo(nb, solution, 'pca_first_component(P): the unit vector of largest variance. pca_variance_share(P): the first eigenvalue divided by the sum of both (Build 3 slides)',
          'def pca_first_component(P):\n    return None  # your code here\n\ndef pca_variance_share(P):\n    return None  # your code here',
          'def pca_first_component(P):\n    Pc = P - P.mean(axis=0)\n    cov = Pc.T @ Pc / len(P)\n    vals, vecs = np.linalg.eigh(cov)\n    return vecs[:, np.argmax(vals)]\n\n'
          'def pca_variance_share(P):\n    Pc = P - P.mean(axis=0)\n    vals = np.linalg.eigvalsh(Pc.T @ Pc / len(P))\n    return vals.max() / vals.sum()')
    nb.code('show("first principal component", lambda: pca_first_component(P))\nshow("share of the variance on it", lambda: pca_variance_share(P))\nrun_build(3)')
    nb.read('If you keep only the position of each point along the first component (one number per point), how much of the spread do you keep?')

    # ================================================================== build 4
    nb.step('4', 'Build 4: a small neural network with backpropagation', 'Forty points around the corners of the unit square. The label is XOR: 1 when exactly one of the two inputs is near 1. The network has two inputs, a hidden layer of tanh units and one sigmoid output; '
            'the loss is the mean binary cross-entropy. The starting weights are drawn by `np.random.default_rng(seed)` in this order: W1 = normal(0, 0.5, (hidden, 2)), then W2 = normal(0, 0.5, (1, hidden)); both biases start at 0. '
            'Shapes: W1 is (hidden, 2), b1 is (hidden,), W2 is (1, hidden), b2 is (1,). Write the forward pass, the backward pass and the training function.')
    nb.code('Xn, yn = xor_data["X"], xor_data["y"]\nprint("first rows of X:", Xn[:3].tolist(), "...  labels:", yn[[0, 10, 20, 30]])')
    nb.predict('Before any training, will the network give answers close to 0 and 1, or all near 0.5?')
    _todo(nb, solution, 'mlp_forward returns (h, p); mlp_backward returns (gW1, gb1, gW2, gb2) for the mean loss; mlp_train(X, y, hidden, lr, steps, seed) returns (W1, b1, W2, b2) (Build 4 slides)',
          'def mlp_forward(W1, b1, W2, b2, X):\n    return None, None  # your code here: return h, p\n\ndef mlp_backward(W1, b1, W2, b2, X, y):\n    return None  # your code here: return gW1, gb1, gW2, gb2\n\n'
          'def mlp_train(X, y, hidden, lr, steps, seed):\n    return None  # your code here: return W1, b1, W2, b2',
          'def mlp_forward(W1, b1, W2, b2, X):\n    h = np.tanh(X @ W1.T + b1)              # hidden activations, one row per point\n    p = sigmoid(h @ W2.T + b2)[:, 0]        # output probabilities\n    return h, p\n\n'
          'def mlp_backward(W1, b1, W2, b2, X, y):\n    h, p = mlp_forward(W1, b1, W2, b2, X)\n    delta = ((p - y) / len(y)).reshape(-1, 1)   # error signal at the output (p - y from Session 17), averaged over the rows\n'
          '    gW2 = delta.T @ h\n    gb2 = delta.sum(axis=0)\n    delta_h = (delta @ W2) * (1 - h ** 2)        # the error signal arriving at the hidden layer\n    gW1 = delta_h.T @ X\n    gb1 = delta_h.sum(axis=0)\n    return gW1, gb1, gW2, gb2\n\n'
          'def mlp_train(X, y, hidden, lr, steps, seed):\n    rng = np.random.default_rng(seed)\n    W1 = rng.normal(0, 0.5, (hidden, X.shape[1]))\n    b1 = np.zeros(hidden)\n    W2 = rng.normal(0, 0.5, (1, hidden))\n    b2 = np.zeros(1)\n'
          '    for _ in range(steps):\n        g1, gb1, g2, gb2 = mlp_backward(W1, b1, W2, b2, X, y)\n        W1, b1, W2, b2 = W1 - lr * g1, b1 - lr * gb1, W2 - lr * g2, b2 - lr * gb2\n    return W1, b1, W2, b2')
    nb.code('def mean_loss(p, y):\n    return -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))\n\n'
            'def show_training():\n    start = mlp_train(Xn, yn, 4, 0.5, 0, SEED % 1000000)\n    end = mlp_train(Xn, yn, 4, 0.5, 3000, SEED % 1000000)\n'
            '    print("loss before training:", mean_loss(mlp_forward(*start, Xn)[1], yn))\n    print("loss after 3000 steps:", mean_loss(mlp_forward(*end, Xn)[1], yn))\n'
            '    print("rounded outputs for the four corners:", np.round(mlp_forward(*end, Xn)[1][[0, 10, 20, 30]]))\n'
            'show("training", show_training)\nrun_build(4)')
    nb.read('XOR cannot be solved by logistic regression on the two inputs. What did the hidden layer add?')

    # ================================================================== build 5
    nb.step('5', 'Build 5: scaled dot-product attention', 'Four tokens with 3-number embeddings (your data). Queries, keys and values come from three weight matrices. The attention weights are softmax(Q K^T / sqrt(d_k)) taken along each row, and the output is the weights times V. '
            'Write the row-wise softmax and the attention function. attention returns (weights, output).')
    nb.code('Xt, Wq, Wk, Wv = att_data["X"], att_data["Wq"], att_data["Wk"], att_data["Wv"]\nQ, K, V = Xt @ Wq, Xt @ Wk, Xt @ Wv\nprint("token embeddings:", Xt.tolist())\nprint("shapes of Q, K, V:", Q.shape, K.shape, V.shape)')
    nb.predict('Every row of the attention weights is a probability distribution over the four tokens. What must each row add up to?')
    _todo(nb, solution, 'softmax_rows(S): a softmax along each row that survives scores like 1000. attention(Q, K, V): returns (weights, output) (Build 5 slides)',
          'def softmax_rows(S):\n    return None  # your code here\n\ndef attention(Q, K, V):\n    return None, None  # your code here: return weights, output',
          'def softmax_rows(S):\n    e = np.exp(S - S.max(axis=1, keepdims=True))     # subtract the row maximum so nothing overflows\n    return e / e.sum(axis=1, keepdims=True)\n\n'
          'def attention(Q, K, V):\n    d_k = K.shape[1]\n    weights = softmax_rows(Q @ K.T / np.sqrt(d_k))\n    return weights, weights @ V')
    nb.code('show("attention weights", lambda: np.round(attention(Q, K, V)[0], 3).tolist())\nshow("row sums", lambda: attention(Q, K, V)[0].sum(axis=1))\n'
            '# why divide by sqrt(d_k)? dot products of long random vectors grow with the length (given code, no check)\nrng_demo = np.random.default_rng(SEED)\nqs, ks = rng_demo.normal(size=(2000, 64)), rng_demo.normal(size=(2000, 64))\n'
            'print("standard deviation of q . k for length 64:", np.std(np.sum(qs * ks, axis=1)), " after dividing by sqrt(64):", np.std(np.sum(qs * ks, axis=1)) / 8)\nrun_build(5)')
    nb.change('Change `attention` so it does not divide by the square root of d_k and compare the weights on the 6-number example `att_data["Q2"]`, `att_data["K2"]`. Which rows get sharper (closer to one-hot)?')

    nb.md('---\n## Save your work\n\nRun every cell again from the top (Runtime, Restart and run all). The last line must say all checks pass. Save the notebook and keep it: it is your course project. '
          'There is nothing to hand in for marks. If you would like feedback, show the notebook to a classmate or to your facilitator and use the project checklist below.\n\n'
          '## Make it yours (optional)\n\nTake the same functions to data you care about. Two examples: put two columns of your own numbers in a list and call `fit_linear` to fit a line, or call `pca_first_component` on two columns of a small table from your work. '
          'Never use private or confidential data in a shared notebook. Then go through the checklist, alone or with a partner.\n\n'
          '## Project checklist (for you and a peer)\n\n- [ ] Every self-check says OK, or I can explain what NOT YET still means.\n- [ ] I can explain Build 1 to someone in two sentences, with no formulas.\n- [ ] I can say why the logistic loss is cross-entropy (Session 16).\n- [ ] I can say what the first principal component is, in plain words.\n- [ ] I checked my backpropagation gradient against a numeric gradient.\n- [ ] I can say why attention divides by the square root of d_k.\n- [ ] My notebook runs from the top with Restart and run all.\n- [ ] I tried at least one change (a new learning rate, my own data or no scaling) and wrote down what happened.')
    nb.code('show_checks()')
    return nb


# ---------------------------------------------------------------------------------------------------------------- seed-free toy numbers (slides and the guided workbook)
def toy():
    sig = lambda z: 1 / (1 + np.exp(-z))
    T = {}
    x = np.array([1, 2, 3, 4, 5, 6], dtype=float)
    y = np.array([2.2, 2.9, 4.1, 5.2, 5.8, 7.1])
    X = np.column_stack([np.ones(6), x])
    w = np.linalg.solve(X.T @ X, X.T @ y)
    T.update(x=x, y=y, w_normal=w, mse=float(np.mean((X @ w - y) ** 2)), pred_7=float(w @ [1, 7]))
    xl = np.arange(1, 9, dtype=float)
    yl = np.array([0, 0, 0, 1, 0, 1, 1, 1], dtype=float)
    Xl = np.column_stack([np.ones(8), xl])
    loss = lambda w_: float(-np.mean(yl * np.log(sig(Xl @ w_)) + (1 - yl) * np.log(1 - sig(Xl @ w_))))

    def gd(steps):
        w_ = np.zeros(2)
        for _ in range(steps):
            w_ = w_ - 0.1 * Xl.T @ (sig(Xl @ w_) - yl) / 8
        return w_
    w5, wf = gd(5), gd(5000)
    T.update(xl=xl, yl=yl, w5=w5, loss5=loss(w5), w_log=wf, loss_log=loss(wf), accuracy=float(np.mean((sig(Xl @ wf) > 0.5) == (yl == 1))))
    a = np.array([2.5, 0.5, 2.2, 1.9, 3.1, 2.3, 2.0, 1.0, 1.5, 1.1])
    b = np.array([2.4, 0.7, 2.9, 2.2, 3.0, 2.7, 1.6, 1.1, 1.6, 0.9])
    Dc = np.column_stack([a, b])
    Dc = Dc - Dc.mean(axis=0)
    cov = Dc.T @ Dc / len(a)
    vals, vecs = np.linalg.eigh(cov)
    pc1 = vecs[:, -1] * (1 if vecs[0, -1] > 0 else -1)
    T.update(a=a, b=b, cov=cov, eigvals=vals, pc1=pc1, ratio=float(vals[-1] / vals.sum()), pca_scores=Dc @ pc1)
    Xx = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    Yx = np.array([0, 1, 1, 0], dtype=float)
    W1 = np.array([[0.5, -0.3], [0.2, 0.8], [-0.6, 0.4], [0.1, -0.9]])
    b1 = np.zeros(4)
    W2 = np.array([[0.3, -0.5, 0.7, 0.2]])
    b2 = np.array([0.1])

    def fwd(W1, b1, W2, b2, X):
        h = np.tanh(X @ W1.T + b1)
        return h, sig(h @ W2.T + b2)[:, 0]
    bce = lambda p, y: float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))
    p0 = fwd(W1, b1, W2, b2, Xx)[1]
    T.update(p0=p0, loss0=bce(p0, Yx))
    for _ in range(5000):
        h, p = fwd(W1, b1, W2, b2, Xx)
        d = ((p - Yx) / 4)[:, None]
        dh = (d @ W2) * (1 - h ** 2)
        W1, b1, W2, b2 = W1 - 0.5 * dh.T @ Xx, b1 - 0.5 * dh.sum(0), W2 - 0.5 * d.T @ h, b2 - 0.5 * d.sum(0)
    p1 = fwd(W1, b1, W2, b2, Xx)[1]
    T.update(p1=p1, loss_nn=bce(p1, Yx))
    Xt = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    Wq = np.array([[1.0, 0.0], [1.0, 1.0]])
    Wk = np.array([[1.0, 1.0], [0.0, 1.0]])
    Wv = np.array([[1.0, 0.0], [0.0, 2.0]])
    Q, K, V = Xt @ Wq, Xt @ Wk, Xt @ Wv
    S = Q @ K.T / np.sqrt(2)
    A = np.exp(S - S.max(1, keepdims=True))
    A /= A.sum(1, keepdims=True)
    rng = np.random.default_rng(18)
    qs, ks = rng.normal(size=(2000, 64)), rng.normal(size=(2000, 64))
    T.update(Xt=Xt, Wq=Wq, Wk=Wk, Wv=Wv, scores=S, weights=A, out=A @ V, spread_unscaled=float(np.std(np.sum(qs * ks, axis=1))))
    return T


def example():
    """One illustrative forward and backward step of the 2-4-1 network (not an XOR row): input (1, 2), target 1, the same starting weights as the XOR toy network.
    Used by the slides and the guided workbook."""
    W1 = np.array([[0.5, -0.3], [0.2, 0.8], [-0.6, 0.4], [0.1, -0.9]])
    b1 = np.zeros(4)
    W2 = np.array([0.3, -0.5, 0.7, 0.2])
    b2 = 0.1
    xin = np.array([1.0, 2.0])
    z1 = W1 @ xin + b1
    h = np.tanh(z1)
    z2 = float(W2 @ h + b2)
    p = 1 / (1 + np.exp(-z2))
    delta = p - 1.0
    gW2 = delta * h
    dh = delta * W2 * (1 - h ** 2)
    return dict(W1=W1, b1=b1, W2=W2, b2=b2, x=xin, z1=z1, h=h, z2=z2, p=p, loss=-np.log(p), delta=delta, gW2=gW2, dh=dh, gW1=np.outer(dh, xin), W2new=W2 - 0.5 * gW2)


def namespace():
    """Seed-free toy numbers for the slides and the guided workbook."""
    return toy()
