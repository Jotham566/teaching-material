"""Session 6 Python lab: SVD of a 2 by 2 matrix, a noisy 8 by 8 image and its low-rank approximations, PCA of the eight marks, power iteration for the first singular value, LoRA counts."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[2] / 'kit'
sys.path.insert(0, str(HERE))
import nb as NB  # noqa: E402
import diagrams_math_b as MB  # noqa: E402

TITLE = 'SVD and PCA'


def _todo(n, solution, hint, names, code):
    """A cell the learner completes. Learner version: names set to None. Solution version: the model answer."""
    if solution:
        n.code(f'# {hint}\n{code}')
    else:
        n.code(f'# {hint}\n' + '\n'.join(f'{v} = None  # your code here' for v in names))


def build(solution: bool):
    d = MB.d6()
    p5 = MB.d5()
    Sn, err_k, cum = d['Sn'], d['err_k'], d['cum']
    lam = p5['lam']
    maths = [float(v) for v in p5['maths']]
    phys = [float(v) for v in p5['phys']]
    n = NB.Notebook()
    n.md('# Session 6 lab: SVD and PCA\n\n**Mathematics for AI and Machine Learning, KLAi Professional Learning.**\n\n'
         'You will find the singular values of a small matrix, remove noise from an 8 by 8 image with a low-rank approximation, run principal component analysis (PCA) on the eight marks from Session 5, '
         'find the singular values of the image again by power iteration and deflation, and count the numbers that LoRA saves. Every step has the rhythm PREDICT, run, READ, CHANGE one thing. '
         'After each answer a check line says OK or NOT YET. The image and the marks are illustrative (made-up numbers to show the arithmetic).\n\n'
         'Run the cells from the top, in order. A cell that starts with a comment and the words `your code here` is yours to complete.')
    n.code('import numpy as np\nimport matplotlib.pyplot as plt\nprint("numpy is ready, version", np.__version__)')
    n.check_setup()

    # ---------------------------------------------------------------- step 1
    n.step(1, 'The SVD of a small matrix', 'The recipe slide shows the NumPy function for the SVD. It returns three things: U, the singular values S as a list (largest first), and V transpose, written Vt. A equals U times the diagonal matrix of S times Vt. '
           'The singular values are also the square roots of the eigenvalues of AᵀA.')
    n.predict('A has rows (2, 2) and (−1, 2). By hand, AᵀA has rows (5, 2) and (2, 8), with trace 13 and determinant 36. What are its eigenvalues, and so the singular values of A?')
    n.code('A = np.array([[2.0, 2.0], [-1.0, 2.0]])\nprint("A =\\n", A)')
    _todo(n, solution, 'Get U, S and Vt (recipe slide). Then the eigenvalues of AᵀA (largest first, use the symmetric eigenvalue function from Session 5) and the matrix rebuilt from the three parts.', ['U', 'S', 'Vt', 'lam_ata', 'rebuilt'],
          'U, S, Vt = np.linalg.svd(A)\nlam_ata = np.linalg.eigvalsh(A.T @ A)[::-1]\nrebuilt = U @ np.diag(S) @ Vt')
    n.code('print("singular values:", S)\nprint("eigenvalues of A^T A:", lam_ata)\n'
           'check("singular values are 3 and 2", S, [3.0, 2.0])\ncheck("square roots of the eigenvalues of A^T A agree", None if lam_ata is None else np.sqrt(lam_ata), [3.0, 2.0])\n'
           'check("U, S and Vt rebuild A", rebuilt, A)')
    n.read('Are the singular values listed from largest to smallest? Print Vt: its rows are the right singular vectors. What is the length of each row?')
    n.change('Run the next cell: a matrix whose second row is twice the first. Predict its second singular value first.')
    n.code('S_flat = np.linalg.svd(np.array([[1.0, 2.0], [2.0, 4.0]]))[1]\nprint("singular values:", np.round(S_flat, 6), "so the rank is", int(np.sum(S_flat > 1e-9)))')

    # ---------------------------------------------------------------- step 2
    n.step(2, 'An 8 by 8 image with noise', 'A clean H pattern (cells 1 or 8, on a scale from 0 white to 9 black) plus random noise of 0, 1 or 2 up or down. We take the SVD of the noisy image and look at its singular values.')
    n.code('clean = np.ones((8, 8))\nclean[:, [1, 6]] = 8\nclean[3:5, 1:7] = 8\nnoise = np.random.default_rng(39).integers(-2, 3, size=(8, 8))\nnoisy = np.clip(clean + noise, 0, 9)\n'
           'fig, ax = plt.subplots(1, 2, figsize=(6, 3))\nax[0].imshow(clean, cmap="Greys", vmin=0, vmax=9)\nax[0].set_title("clean")\nax[1].imshow(noisy, cmap="Greys", vmin=0, vmax=9)\nax[1].set_title("noisy")\nplt.show()\n'
           'print("error of the noisy image from the clean one:", round(np.linalg.norm(noisy - clean), 2))')
    n.predict('How many singular values of the noisy image will be large? The clean H has two different kinds of rows, so how many independent patterns does it hold?')
    _todo(n, solution, 'SVD of the noisy image. Then the share of each squared singular value, its running total (cumulative share), and the smallest k that reaches 95 percent.', ['U2', 'S2', 'Vt2', 'cum2', 'k95'],
          'U2, S2, Vt2 = np.linalg.svd(noisy)\nshare = S2 ** 2 / np.sum(S2 ** 2)\ncum2 = np.cumsum(share)\nk95 = int(np.searchsorted(cum2, 0.95)) + 1')
    n.code('print("singular values:", np.round(S2, 2))\nprint("cumulative share:", None if cum2 is None else np.round(cum2, 3))\nprint("k for 95 percent:", k95)\n'
           'check("first two singular values", None if S2 is None else S2[:2], [%s, %s], 0.01)\ncheck("two pieces hold 97 percent", None if cum2 is None else cum2[1], %s, 0.001)\ncheck("k for 95 percent is 2", k95, 2, 0)'
           % (float(Sn[0]), float(Sn[1]), float(cum[1])))
    n.read('Why is there a gap after the second singular value? What does the flat tail of small values stand for?')

    # ---------------------------------------------------------------- step 3
    n.step(3, 'Low-rank approximations and their errors', 'The rank k approximation keeps the first k terms of the sum on the slide. The recipe slide shows how to slice U, S and Vt. We measure the error against the clean image, which we know only because we built it. The error is the square root of the sum of the squared cell differences.')
    n.predict('Which rank will give the smallest error from the clean image: 1, 2 or 3? Will rank 3 be better or worse than rank 2?')
    _todo(n, solution, 'Write a function approx(k) that returns the rank k approximation of the noisy image (recipe slide). Then compute the three errors against the clean image, as defined on the image slide.', ['approx', 'errs'],
          'def approx(k):\n    return (U2[:, :k] * S2[:k]) @ Vt2[:k]\nerrs = [np.linalg.norm(approx(k) - clean) for k in (1, 2, 3)]')
    n.code('print("errors for rank 1, 2, 3:", None if errs is None else np.round(errs, 2))\ncheck("rank 1 error", None if errs is None else errs[0], %s, 0.01)\ncheck("rank 2 error is the smallest", None if errs is None else errs[1], %s, 0.01)\n'
           'check("rank 3 error", None if errs is None else errs[2], %s, 0.01)' % (err_k[1], err_k[2], err_k[3]))
    n.code('if approx is not None:\n    fig, ax = plt.subplots(1, 4, figsize=(9, 2.5))\n    for a, (img, t) in zip(ax, [(noisy, "noisy"), (approx(1), "rank 1"), (approx(2), "rank 2"), (approx(3), "rank 3")]):\n'
           '        a.imshow(img, cmap="Greys", vmin=0, vmax=9)\n        a.set_title(t)\n        a.axis("off")\n    plt.show()')
    n.read('Does rank 2 look more like the clean H than the noisy image does? Why does the error rise again at rank 3?')
    n.change('Run the next cell: the rank 4 error. Predict whether it is higher or lower than rank 3. How many numbers does rank 4 store, 4 × (8 + 8 + 1), compared with 64?')
    n.code('print("rank 4 error:", round(np.linalg.norm(approx(4) - clean), 2), " numbers stored:", 4 * 17, "against 64")')

    # ---------------------------------------------------------------- step 4
    n.step(4, 'PCA of the eight marks, step by step', 'The same eight students as Session 5. Centre the columns, build the covariance matrix, take the top eigenvector, give each student a score (the dot product with it), and measure the explained variance.')
    n.code(f'maths = np.array({maths})\nphys = np.array({phys})\nX = np.column_stack([maths, phys])\nprint("means:", X.mean(axis=0))')
    n.predict('Last session the eigenvalues were 102 and 2 and the top direction (0.8, 0.6). What will the variance of the scores along that direction be? What share of the total variance is that?')
    _todo(n, solution, 'Centre X, build C, get the top eigenvector (largest eigenvalue), the score of each student (the dot product of the centred marks with the top eigenvector), the variance of the scores (divide by n − 1), the explained variance ratio and the squared distance lost.',
          ['Xc', 'C', 'top', 'scores', 'var_scores', 'ratio', 'lost'],
          'Xc = X - X.mean(axis=0)\nC = Xc.T @ Xc / (len(X) - 1)\nvals, vecs = np.linalg.eigh(C)\ntop = vecs[:, -1]\nif top[0] < 0:\n    top = -top\nscores = Xc @ top\n'
          'var_scores = scores.var(ddof=1)\nratio = vals[-1] / vals.sum()\nlost = np.sum((Xc - np.outer(scores, top)) ** 2)')
    n.code('print("top component:", top)\nprint("scores:", None if scores is None else np.round(scores, 1))\nprint("variance of scores:", var_scores, " explained ratio:", ratio, " squared distance lost:", lost)\n'
           'check("top component, up to a sign", None if top is None else np.abs(top), [0.8, 0.6], 0.001)\ncheck("score of the first student", None if scores is None else abs(scores[0]), %s, 0.001)\n'
           'check("variance of the scores is the top eigenvalue 102", var_scores, %s, 0.001)\ncheck("explained variance ratio", ratio, %s, 0.001)\ncheck("squared distance lost is 7 × 2 = 14", lost, %s, 0.001)'
           % (float(abs(d['scores'][0])), float(lam[0]), d['ratio'][0], d['lost']))
    n.read('The second eigenvalue is 2. How is it linked to the squared distance lost, 14? What would happen to the ratio if we kept both components?')

    # ---------------------------------------------------------------- step 5
    n.step(5, 'PCA is the SVD of the centred data', 'Take the SVD of Xc. The rows of Vt are the principal components, and the variance along each is the squared singular value divided by n - 1.')
    n.predict('What will the variances S**2 / (n - 1) be? Will the first row of Vt equal your top component?')
    _todo(n, solution, 'SVD of Xc (the recipe slide shows the version for tall data), then the variances along each component.', ['U3', 'S3', 'Vt3', 'var_svd'],
          'U3, S3, Vt3 = np.linalg.svd(Xc, full_matrices=False)\nvar_svd = S3 ** 2 / (len(X) - 1)')
    n.code('print("singular values of Xc:", S3)\nprint("variances:", var_svd)\ncheck("variances are 102 and 2", var_svd, [%s, %s], 0.001)\ncheck("first row of Vt, up to a sign", None if Vt3 is None else np.abs(Vt3[0]), [0.8, 0.6], 0.001)'
           % (float(lam[0]), float(lam[1])))
    n.change('Replace the physics marks by 100 minus physics, then run PCA again by SVD. Predict whether the explained variance ratio changes and which way the first component points.')
    _todo(n, solution, 'Centre the new data and take its SVD. Compute the first component and the ratio.', ['top_flip', 'ratio_flip'],
          'X_flip = np.column_stack([maths, 100 - phys])\nXf = X_flip - X_flip.mean(axis=0)\nSf, Vtf = np.linalg.svd(Xf, full_matrices=False)[1:]\ntop_flip = Vtf[0]\nratio_flip = Sf[0] ** 2 / np.sum(Sf ** 2)')
    n.code('print("first component:", top_flip, " ratio:", ratio_flip)\ncheck("explained ratio is unchanged", ratio_flip, %s, 0.001)\ncheck("component is (0.8, -0.6) up to a sign", None if top_flip is None else np.abs(top_flip), [0.8, 0.6], 0.001)\n'
           'check("the signs of the two entries now differ", None if top_flip is None else float(np.sign(top_flip[0] * top_flip[1])), -1.0, 0)' % d['ratio'][0])

    # ---------------------------------------------------------------- step 6
    n.step(6, 'Power iteration and deflation find the singular values', 'Neither Excel nor Google Sheets has an SVD, so the spreadsheet does this step with cells. The top eigenvector of M = noisyᵀ noisy is the first right singular vector v₁, and the top eigenvalue of M is σ₁². '
           'Then u₁ = noisy v₁ / σ₁ and the rank 1 term is σ₁ u₁ v₁ᵀ. (Slides: power iteration on AᵀA, then deflation.)')
    n.code('M = noisy.T @ noisy      # an 8 by 8 symmetric matrix\ng = np.ones(8)            # the starting guess g0 = (1, 1, ..., 1)\nprint("M has shape", M.shape)')
    n.predict('After 10 multiplications by M, each followed by dividing by the largest entry, the largest entry should be σ₁². The slide gives σ₁ = 36.85, so what is its square?')
    _todo(n, solution, 'Run 10 steps of power iteration on M, starting from g. Keep the last largest entry in est. Then sigma1, the unit vector v1, u1 and the rank 1 term.', ['est', 'sigma1', 'v1', 'u1', 'rank1'],
          'for k in range(10):\n    Mg = M @ g\n    est = np.max(np.abs(Mg))\n    g = Mg / est\nsigma1 = np.sqrt(est)\nv1 = g / np.linalg.norm(g)\nu1 = noisy @ v1 / sigma1\nrank1 = sigma1 * np.outer(u1, v1)')
    n.code('print("largest entry after 10 steps:", est, " sigma1:", sigma1)\ncheck("largest entry is sigma1 squared, 1357.6", est, %s, 0.1)\ncheck("sigma1 agrees with the SVD", sigma1, %s, 0.001)\n'
           'check("rank 1 term agrees with the SVD rank 1 approximation", None if rank1 is None else np.max(np.abs(rank1 - approx(1))), 0, 0.001)' % (d['its'][-1][1], float(Sn[0])))
    n.read('The rank 1 term has 64 cells but is built from 8 + 8 + 1 numbers. Look at cell (4, 2) of rank1. How does it compare with the noisy value?')
    n.change('Deflation: subtract the rank 1 part of M (σ₁² times v₁ v₁ᵀ) so that its top eigenvalue is removed, then repeat the same 10 steps from a fresh start to find σ₂. Predict σ₂ first: the scree plot slide shows it.')
    _todo(n, solution, 'Deflate M, repeat the power iteration from a fresh start, and keep est2, sigma2, v2, u2. Then add the second term to rank1 and measure the rank 2 error against the clean image.', ['est2', 'sigma2', 'rank2', 'err2'],
          'M2 = M - est * np.outer(v1, v1)\ng = np.ones(8)\nfor k in range(10):\n    Mg = M2 @ g\n    est2 = np.max(np.abs(Mg))\n    g = Mg / est2\nsigma2 = np.sqrt(est2)\nv2 = g / np.linalg.norm(g)\nu2 = noisy @ v2 / sigma2\nrank2 = rank1 + sigma2 * np.outer(u2, v2)\nerr2 = np.linalg.norm(rank2 - clean)')
    n.code('print("largest entry of the second round:", est2, " sigma2:", sigma2)\nprint("rank 2 error from the clean image:", None if err2 is None else round(err2, 2))\n'
           'check("sigma2 agrees with the SVD", sigma2, %s, 0.001)\ncheck("the rank 2 error is 4.54, as in step 3", err2, %s, 0.01)' % (float(Sn[1]), err_k[2]))
    n.read('Why does subtracting σ₁² v₁ v₁ᵀ leave the other eigenvectors of M unchanged? What would a third round give?')

    # ---------------------------------------------------------------- step 7
    n.step(7, 'LoRA: count the numbers', 'LoRA (Hu et al., 2021) keeps a pre-trained weight matrix W frozen and trains the change as B times A, with B of size d by r and A of size r by d. Here we only count numbers and check the rank, with illustrative sizes.')
    n.predict('For d = 1,000 and r = 8, how many numbers are in a full d by d update, and how many in B and A together? What fraction is that?')
    _todo(n, solution, 'Count the numbers in a full update and in B and A together. Then build a small B (50 by 3) and A (3 by 50) with random numbers and find the rank of their product.', ['full_update', 'lora_count', 'share', 'rank_BA'],
          'd, r = 1000, 8\nfull_update = d * d\nlora_count = 2 * d * r\nshare = lora_count / full_update\nrng = np.random.default_rng(6)\nB = rng.normal(size=(50, 3))\nA_small = rng.normal(size=(3, 50))\nrank_BA = np.linalg.matrix_rank(B @ A_small)')
    n.code('print("full update:", full_update, " B and A:", lora_count, " share:", share, " rank of B A:", rank_BA)\ncheck("full update numbers", full_update, %d, 0)\ncheck("LoRA numbers", lora_count, %d, 0)\n'
           'check("share is 1.6 percent", share, 0.016, 0.0001)\ncheck("B A is a 50 by 50 matrix of rank 3", rank_BA, 3, 0)' % (d['lora_full'], d['lora_small']))
    n.read('A 50 by 50 matrix has 2,500 numbers, yet B A has rank 3. Why can such a product never have a rank above r?')
    n.md('---\n## Result\n\nRun the next cell. It must say **All checks pass** before you save.')
    n.code('show_checks()')
    return n


def CHECK(rs):
    d = MB.d6()
    out = '\n'.join(o for _, o, _ in rs)
    probs = []
    for token in ('1357.6', '0.9807', f'{d["err_k"][2]:.2f}', '16000', f'{d["Sn"][1]:.2f}'):
        if token not in out:
            probs.append(f'printed output lacks {token}')
    return probs
