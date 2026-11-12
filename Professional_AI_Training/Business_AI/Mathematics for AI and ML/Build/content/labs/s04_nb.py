"""Session 4 Python lab: solve a 2 by 2 system, inverse and determinant, rank, the normal equation, too few rows."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[2] / 'kit'
sys.path.insert(0, str(HERE))
import nb as NB  # noqa: E402
import diagrams_math_b as MB  # noqa: E402

TITLE = 'Solving linear systems'


def _todo(n, solution, hint, names, code):
    """A cell the learner completes. Learner version: names set to None. Solution version: the model answer."""
    if solution:
        n.code(f'# {hint}\n{code}')
    else:
        n.code(f'# {hint}\n' + '\n'.join(f'{v} = None  # your code here' for v in names))


def build(solution: bool):
    d = MB.d4()
    bi, ws = float(d['w'][0]), float(d['w'][1])   # intercept b and slope w
    n = NB.Notebook()
    n.md('# Session 4 lab: Solving linear systems\n\n**Mathematics for AI and Machine Learning, KLAi Professional Learning.**\n\n'
         'You will solve a system of equations three ways, meet a matrix with no inverse, and fit a line to seven data points with the normal equation. '
         'Every step has the rhythm PREDICT, run, READ, CHANGE one thing. After each answer a check line says OK or NOT YET. The data are illustrative (made-up numbers to show the arithmetic).\n\n'
         'Run the cells from the top, in order. A cell that starts with a comment and the words `your code here` is yours to complete.')
    n.code('import numpy as np\nimport matplotlib.pyplot as plt\nprint("numpy is ready, version", np.__version__)')
    n.check_setup()

    # ---------------------------------------------------------------- step 1
    n.step(1, 'Solve a 2 by 2 system', 'The system is 2x₁ + x₂ = 5 and x₁ − x₂ = 1. In matrix form it is Ax = b, where x = (x₁, x₂). The recipe slide of today names the NumPy function that solves it.')
    n.predict('Which two numbers x₁ and x₂ solve both equations? Think of the point where the two lines cross.')
    n.code('A = np.array([[2.0, 1.0], [1.0, -1.0]])   # the matrix of coefficients\nb = np.array([5.0, 1.0])                  # the right-hand sides (from step 3 on, b means the intercept)\nprint("A =\\n", A)\nprint("b =", b)')
    _todo(n, solution, 'Solve Ax = b. Use the function from the recipe slide.', ['x'], 'x = np.linalg.solve(A, b)')
    n.code('check("x solves the system, x = (2, 1)", x, [%s, %s])\nprint("x =", x)' % (float(d['sol'][0]), float(d['sol'][1])))
    n.read('Put your x back into 2x₁ + x₂ and x₁ − x₂. Do you get 5 and 1? Check both at once with a matrix times vector product.')

    # ---------------------------------------------------------------- step 2
    n.step(2, 'Determinant, inverse and rank', 'The determinant of A scales areas. The inverse A_inv undoes A, so x = A_inv times b. '
           'A square matrix with determinant 0 has no inverse (it is singular), and its rank is below full.')
    n.predict('What is the determinant of A? Work it out by hand as a₁₁ a₂₂ − a₁₂ a₂₁ = 2 × (−1) − 1 × 1 before you run the cell.')
    _todo(n, solution, 'Find the determinant, the inverse, and x again as the inverse times b. The recipe slide lists the np.linalg functions for each one.', ['det_A', 'A_inv', 'x_inv'],
          'det_A = np.linalg.det(A)\nA_inv = np.linalg.inv(A)\nx_inv = A_inv @ b')
    n.code('check("determinant of A is -3", det_A, %s)\ncheck("top-left entry of the inverse is 1/3", A_inv[0, 0], %s)\ncheck("x from the inverse is (2, 1)", x_inv, [%s, %s])\n'
           'print("determinant =", det_A)\nprint("inverse =\\n", A_inv)\nprint("x from the inverse =", x_inv)'
           % (d['det'], float(d['Ainv'][0, 0]), float(d['sol'][0]), float(d['sol'][1])))
    n.read('Multiply A by A_inv. Which matrix do you get, and what is it called?')
    n.change('Use the singular matrix S below (its second row is twice its first). Predict its rank, then complete the cell. Then read what np.linalg.solve says.')
    n.code('S = np.array([[1.0, 2.0], [2.0, 4.0]])\nprint("determinant of S =", np.linalg.det(S))')
    _todo(n, solution, 'Find the rank of S. The recipe slide names the np.linalg function.', ['rank_S'], 'rank_S = np.linalg.matrix_rank(S)')
    n.code('check("rank of the singular matrix is 1", rank_S, %d, 0)\nprint("rank of S =", rank_S)\n'
           'try:\n    np.linalg.solve(S, b)\nexcept np.linalg.LinAlgError as e:\n    print("solve refuses:", e)' % d['rankS'])

    # ---------------------------------------------------------------- step 3
    n.step(3, 'The data and the matrix X', 'Seven months of advertising spend and sales, both in UGX million (illustrative). '
           'To fit the line ŷ = b + w × spend (b the intercept, w the slope) we build X: a column of ones, which carries b, then the spend column.')
    spend = [float(v) for v in d['x']]
    sales = [float(v) for v in d['y']]
    n.code(f'spend = np.array({spend})\nsales = np.array({sales})\n'
           'X = np.column_stack([np.ones(len(spend)), spend])   # a column of ones, then spend\nprint("X has shape", X.shape)\nprint(X)\n'
           'plt.scatter(spend, sales, color="black")\nplt.xlabel("advertising spend (UGX million)")\nplt.ylabel("sales (UGX million)")\nplt.title("Seven months (illustrative)")\nplt.show()')
    n.read('How many equations does X w = sales stand for, and how many unknowns? Is there a line through all seven dots?')

    # ---------------------------------------------------------------- step 4
    n.step(4, 'The normal equation', 'Put the two unknowns in one column, called bw here: b on top, w below. The best fit makes the errors y − X bw meet every column of X at right angles, Xᵀ(y − X bw) = 0, which rearranges to (XᵀX) bw = Xᵀy. XᵀX is a small square matrix, so it can be solved like the 2 by 2 system of step 1.')
    n.predict('XᵀX is 2 by 2. Its top-left entry counts the months. What is it? Its bottom-right entry is the sum of spend squared. Estimate it first.')
    _todo(n, solution, 'Compute XᵀX and Xᵀy, then solve the normal equation for bw = (b, w). The recipe slide shows how.', ['XtX', 'Xty', 'bw'],
          'XtX = X.T @ X\nXty = X.T @ sales\nbw = np.linalg.solve(XtX, Xty)')
    n.code('check("XᵀX is [[7, 29], [29, 155]]", XtX, %s)\ncheck("Xᵀy is (221, 1105)", Xty, %s)\ncheck("intercept b and slope w", bw, [%s, %s])\n'
           'print("X^T X =\\n", XtX)\nprint("X^T y =", Xty)\nif bw is not None:\n    print("b (intercept) = {:.2f}, w (slope) = {:.2f}".format(bw[0], bw[1]))'
           % (d['XtX'].tolist(), d['Xty'].tolist(), bi, ws))
    n.read('What does the slope w say in plain words? Use the units: UGX million of sales per UGX million of spend.')
    _todo(n, solution, 'Predicted sales ŷ for the seven months, the total squared error, then the RMSE from it (the least-squares slide shows how), and the prediction at spend 7.', ['pred', 'sse', 'rmse', 'pred7'],
          'pred = X @ bw\nsse = np.sum((sales - pred) ** 2)\nrmse = np.sqrt(sse / len(sales))\npred7 = bw[0] + bw[1] * 7')
    n.code('check("predicted sales for month 1", None if pred is None else pred[0], %s)\ncheck("total squared error is 8.28", sse, %s)\ncheck("RMSE of the line", rmse, %s)\ncheck("prediction at spend 7", pred7, %s, 0.05)\n'
           'if None not in (sse, rmse, pred7):\n    print("total squared error = {:.2f}".format(sse))\n    print("RMSE = {:.2f} UGX million".format(rmse))\n    print("predicted sales at spend 7 = {:.1f}".format(pred7))' % (float(d['pred'][0]), d['sse'], d['rmse'], d['pred7']))
    _todo(n, solution, 'Solve the same least-squares problem in one call. The recipe slide names the function. It returns several things, and the weights come first.', ['w_lstsq'],
          'w_lstsq = np.linalg.lstsq(X, sales, rcond=None)[0]')
    n.code('check("lstsq agrees with the normal equation", w_lstsq, [%s, %s])\nprint("lstsq gives", w_lstsq)' % (bi, ws))
    n.code('# Draw the fitted line and the errors (a picture, no TODO)\nif bw is not None:\n    xs = np.linspace(0, 9, 50)\n    plt.scatter(spend, sales, color="black")\n'
           '    plt.plot(xs, bw[0] + bw[1] * xs, color="#AE2525")\n    for a, c, p in zip(spend, sales, X @ bw):\n        plt.plot([a, a], [c, p], color="#AE2525", lw=1)\n'
           '    plt.xlabel("advertising spend (UGX million)")\n    plt.ylabel("sales (UGX million)")\n    plt.title("Fitted line and errors")\n    plt.show()')

    # ---------------------------------------------------------------- step 5
    n.step(5, 'Change one thing: too few rows', 'Keep only one month, the one with spend 4. Now there is one equation and two unknowns. Every line through that point fits it exactly.')
    n.predict('For one row, XᵀX has rows (1, 4) and (4, 16). Work out its determinant by hand: 1 × 16 − 4 × 4. What do you expect?')
    n.code('X_one = X[3:4]                 # one row: the month with spend 4\nM = X_one.T @ X_one\nprint("X_one =", X_one)\nprint("X_one^T X_one =\\n", M)')
    _todo(n, solution, 'Find the determinant and the rank of M (the same two functions as in step 2).', ['det_M', 'rank_M'], 'det_M = np.linalg.det(M)\nrank_M = np.linalg.matrix_rank(M)')
    n.code('check("determinant is 0 with one row", det_M, 0, 1e-9)\ncheck("rank is 1, below the 2 unknowns", rank_M, %d, 0)\nprint("determinant =", det_M, " rank =", rank_M)' % int(np_rank(d)))
    n.read('A model has two weights but only one data row. What does the data say about the best line? What would more rows do?')
    n.md('---\n## Result\n\nRun the next cell. It must say **All checks pass** before you save.')
    n.code('show_checks()')
    return n


def np_rank(d):
    import numpy as np
    return np.linalg.matrix_rank(d['X1'].T @ d['X1'])


def CHECK(rs):
    d = MB.d4()
    out = '\n'.join(o for _, o, _ in rs)
    probs = []
    for token in (f'{d["w"][0]:.2f}', f'{d["w"][1]:.2f}', f'{d["rmse"]:.2f}'):
        if token not in out:
            probs.append(f'printed output lacks {token}')
    return probs
