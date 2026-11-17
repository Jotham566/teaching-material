"""Session 5 Python lab: test an eigenvector, eigenvalues by formula and by library, the covariance matrix of eight marks, its top direction, power iteration."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[2] / 'kit'
sys.path.insert(0, str(HERE))
import nb as NB  # noqa: E402
import diagrams_math_b as MB  # noqa: E402

TITLE = 'Eigenvalues and eigenvectors'


def _todo(n, solution, hint, names, code):
    """A cell the learner completes. Learner version: names set to None. Solution version: the model answer."""
    if solution:
        n.code(f'# {hint}\n{code}')
    else:
        n.code(f'# {hint}\n' + '\n'.join(f'{v} = None  # your code here' for v in names))


def build(solution: bool):
    d = MB.d5()
    C, lam, v1 = d['C'], d['lam'], d['v1']
    maths = [float(v) for v in d['maths']]
    phys = [float(v) for v in d['phys']]
    n = NB.Notebook()
    n.md('# Session 5 lab: Eigenvalues and eigenvectors\n\n**Mathematics for AI and Machine Learning, KLAi Professional Learning.**\n\n'
         'You will test whether a direction is an eigenvector, find eigenvalues by the formula and with a library, build the covariance matrix of eight students\' marks, find the direction in which the marks vary most, '
         'and find the same direction again by power iteration. Every step has the rhythm PREDICT, run, READ, CHANGE one thing. After each answer a check line says OK or NOT YET. The marks are illustrative (made-up numbers to show the arithmetic).\n\n'
         'Run the cells from the top, in order. A cell that starts with a comment and the words `your code here` is yours to complete.')
    n.code('import numpy as np\nimport matplotlib.pyplot as plt\nprint("numpy is ready, version", np.__version__)')
    n.check_setup()

    # ---------------------------------------------------------------- step 1
    n.step(1, 'Does the matrix keep the direction of (1, 1)?', 'The matrix A has rows (2, 1) and (1, 2). A vector v is an eigenvector of A when A v is a multiple of v. The multiple is the eigenvalue.')
    n.predict('Work out A times (1, 1) by hand: each row of A takes a dot product with (1, 1). Is the answer on the same line as (1, 1)? By what factor?')
    n.code('A = np.array([[2.0, 1.0], [1.0, 2.0]])\nv = np.array([1.0, 1.0])\nprint("A =\\n", A)')
    _todo(n, solution, 'Compute A v (matrix times vector), then the factor by which the first entry grew.', ['Av', 'factor'], 'Av = A @ v\nfactor = Av[0] / v[0]')
    n.code('check("A times (1, 1) is (3, 3)", Av, [3.0, 3.0])\ncheck("the stretch factor is 3", factor, 3.0)\nprint("A v =", Av, " factor =", factor)')
    n.read('Is A v equal to factor times v in both entries? What does that say about (1, 1)?')
    n.change('Run the next cell: the arrow (1, 0) instead of (1, 1). Does A turn it, or only stretch it?')
    n.code('w = np.array([1.0, 0.0])\nprint("A w =", A @ w, "which is not a multiple of", w)')

    # ---------------------------------------------------------------- step 2
    n.step(2, 'Eigenvalues from the formula: trace and determinant', 'For a 2 by 2 matrix, lambda squared minus T lambda plus D equals 0, where T is the trace (a₁₁ + a₂₂) and D is the determinant (a₁₁ a₂₂ − a₁₂ a₂₁). '
           'The two eigenvalues are (T plus or minus the square root of T squared minus 4 D) divided by 2.')
    n.predict('For A, T = 2 + 2 and D = 2 × 2 − 1 × 1. What are the two eigenvalues? Check that they add up to T and multiply to D.')
    _todo(n, solution, 'Find T, D and the two eigenvalues (the larger one first).', ['T', 'D', 'lam_a', 'lam_b'],
          'T = A[0, 0] + A[1, 1]\nD = A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0]\nroot = np.sqrt(T ** 2 - 4 * D)\nlam_a = (T + root) / 2\nlam_b = (T - root) / 2')
    n.code('check("trace of A", T, 4.0)\ncheck("determinant of A", D, 3.0)\n'
           'check("larger eigenvalue", lam_a, 3.0)\ncheck("smaller eigenvalue", lam_b, 1.0)\nprint("T =", T, " D =", D, " eigenvalues:", lam_a, lam_b)')
    n.read('Do lam_a + lam_b and lam_a * lam_b equal T and D? This is a quick check you can always run on a hand calculation.')
    n.change('Run the next cell: a matrix that is not symmetric, with rows (4, 1) and (2, 3). Predict its eigenvalues first (T = 7, D = 10).')
    n.code('B = np.array([[4.0, 1.0], [2.0, 3.0]])\nT2 = B[0, 0] + B[1, 1]\nD2 = np.linalg.det(B)\nr2 = np.sqrt(T2 ** 2 - 4 * D2)\nprint("eigenvalues of B:", (T2 + r2) / 2, (T2 - r2) / 2)')

    # ---------------------------------------------------------------- step 3
    n.step(3, 'Eigenvalues and eigenvectors with a library', 'The eigenvalue function for symmetric matrices (see the recipe slide) suits covariance matrices, which are always symmetric. It returns the eigenvalues from smallest to largest, and the eigenvectors as the columns of a matrix.')
    n.predict('Will the eigenvalues agree with your formula? In which order will eigh list them? Which vector do you expect for the eigenvalue 3?')
    _todo(n, solution, 'Get the eigenvalues and the eigenvectors of A with the library function from the recipe slide. It returns two things.', ['values', 'vectors'], 'values, vectors = np.linalg.eigh(A)')
    n.code('check("eigenvalues from eigh, smallest first", values, [1.0, 3.0])\n'
           'check("eigenvector for 3, up to a sign", None if vectors is None else np.abs(vectors[:, 1]), [0.7071, 0.7071], 0.001)\n'
           'print("eigenvalues:", values)\nif vectors is not None:\n    print("eigenvectors (columns):\\n", np.round(vectors, 4))')
    n.read('The vector for 3 has length 1, so it is (1, 1) divided by the square root of 2. The sign may differ from the slides. Why is that still correct?')
    n.change('Run the next cell: check A v = lambda v for both columns.')
    n.code('if vectors is not None:\n    for k in range(2):\n        print(np.round(A @ vectors[:, k], 4), np.round(values[k] * vectors[:, k], 4))')

    # ---------------------------------------------------------------- step 4
    n.step(4, 'The covariance matrix of eight marks', 'Eight students, with a maths mark and a physics mark each (illustrative). Centre each column by subtracting its mean, then C = (X_c transpose times X_c) divided by (n - 1), the sample covariance from the slides (np.cov divides by n - 1 too).')
    n.code(f'maths = np.array({maths})\nphys = np.array({phys})\nX = np.column_stack([maths, phys])      # 8 rows, 2 columns\nprint("means:", X.mean(axis=0))\n'
           'plt.scatter(maths, phys, color="black")\nplt.xlabel("maths mark")\nplt.ylabel("physics mark")\nplt.title("Eight students (illustrative)")\nplt.show()')
    n.predict('The cloud runs from bottom left to top right. Will the covariance between the two marks be positive or negative? Which variance is larger, maths or physics?')
    _todo(n, solution, 'Centre the columns, then build the covariance matrix with the formula.', ['Xc', 'C'], 'Xc = X - X.mean(axis=0)\nC = Xc.T @ Xc / (len(X) - 1)')
    n.code('check("C matches the slides: rows (66, 48) and (48, 38)", C, %s)\ncheck("C matches np.cov", C, np.cov(X.T))\nprint("C =\\n", C)' % C.tolist())
    n.read('Which entry of C is the variance of maths? Which entry is the covariance? Is C symmetric?')

    # ---------------------------------------------------------------- step 5
    n.step(5, 'The top direction of the data', 'The eigenvectors of C are the directions of the cloud. The eigenvalue of each is the variance along it. '
           'The share of the total variance on direction 1 is the larger eigenvalue divided by the sum of both.')
    n.predict('Use the 2 by 2 formula on C. T = 66 + 38 and D = 66 × 38 − 48 × 48. Which two eigenvalues do you expect? What share of the variance is on direction 1?')
    _todo(n, solution, 'Get the eigenvalues and eigenvectors of C, as in step 3. Reverse them so that the largest comes first, then compute the share of the total.', ['lam_c', 'top', 'share'],
          'vals, vecs = np.linalg.eigh(C)\nlam_c = vals[::-1]\ntop = vecs[:, ::-1][:, 0]\nshare = lam_c[0] / lam_c.sum()')
    n.code('check("eigenvalues of C are 102 and 2", lam_c, [%s, %s], 0.001)\ncheck("top eigenvector, up to a sign", None if top is None else np.abs(top), [%s, %s], 0.001)\ncheck("share of variance on direction 1", share, %s, 0.001)\n'
           'print("eigenvalues of C:", lam_c)\nif share is not None:\n    print("top eigenvector:", top, " share of variance:", round(share, 3))'
           % (float(lam[0]), float(lam[1]), float(abs(v1[0])), float(abs(v1[1])), d['explained']))
    n.read('Direction 1 is (0.8, 0.6). What does that say about maths and physics marks? How much of the total spread is lost if we keep only direction 1?')
    n.code('Xc_ = X - X.mean(axis=0)\nplt.scatter(Xc_[:, 0], Xc_[:, 1], color="black")\nif top is not None:\n    plt.plot([-14 * top[0], 14 * top[0]], [-14 * top[1], 14 * top[1]], color="#AE2525")\n'
           'plt.axhline(0, color="grey", lw=0.5)\nplt.axvline(0, color="grey", lw=0.5)\nplt.gca().set_aspect("equal")\nplt.xlabel("centred maths mark")\nplt.ylabel("centred physics mark")\nplt.title("Centred marks and direction 1")\nplt.show()')

    # ---------------------------------------------------------------- step 6
    n.step(6, 'Power iteration: find the top direction by repeated multiplying', 'Start with a guess g. Multiply by C, then divide by the largest entry of the result. Repeat. The guess swings towards the top eigenvector, and the largest entry tends to the top eigenvalue.')
    n.predict('Start at g = (0, 1). After 6 multiplications (row k = 5 of the slide table) what will the largest entry be? Which vector will the guess settle on, with largest entry 1?')
    _todo(n, solution, 'Run 6 multiplications of power iteration on C. Keep the last largest entry in est.', ['est', 'g_final'],
          'g = np.array([0.0, 1.0])\nfor k in range(6):\n    Cg = C @ g\n    est = np.max(np.abs(Cg))\n    g = Cg / est\ng_final = g')
    n.code('check("estimate after 6 multiplications is about 102", est, %s, 0.01)\ncheck("guess settles at (1, 0.75), the direction (0.8, 0.6)", g_final, [1.0, 0.75], 0.001)\nprint("estimate of the top eigenvalue:", est)\nprint("guess:", g_final)'
           % float(d['pc'][-1][3]))
    n.read('The second eigenvalue (2) is tiny compared with the first (102). Why does that make the guess settle in just a few steps?')
    n.change('Replace the physics marks by 100 minus the physics mark: a feature that now moves the opposite way. Predict the sign of the covariance and whether the eigenvalues change.')
    _todo(n, solution, 'Build the new covariance matrix and take its eigenvalues (largest first).', ['C_flip', 'lam_flip'],
          'X2 = np.column_stack([maths, 100 - phys])\nC_flip = np.cov(X2.T)\nlam_flip = np.linalg.eigvalsh(C_flip)[::-1]')
    n.code('check("the covariance changes sign to -48", None if C_flip is None else C_flip[0, 1], -48.0, 0.001)\ncheck("the eigenvalues stay 102 and 2", lam_flip, [%s, %s], 0.001)\nprint("C_flip =\\n", C_flip)\nprint("eigenvalues:", lam_flip)'
           % (float(lam[0]), float(lam[1])))
    n.md('---\n## Result\n\nRun the next cell. It must say **All checks pass** before you save.')
    n.code('show_checks()')
    return n


def CHECK(rs):
    d = MB.d5()
    out = '\n'.join(o for _, o, _ in rs)
    probs = []
    for token in ('102.0', '0.981', '-48'):
        if token not in out:
            probs.append(f'printed output lacks {token}')
    return probs
