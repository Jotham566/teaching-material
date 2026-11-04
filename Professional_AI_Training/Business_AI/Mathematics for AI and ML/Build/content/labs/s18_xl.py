"""Session 18 GUIDED workbook of the course project (no marks): the five builds with fixed, seed-free toy numbers (the same as on the slides of Session 18), with its own checks.
Linear regression by the normal equation, logistic regression as a table of 5 gradient steps, PCA by formulas for a 2 by 2 covariance matrix, one forward and one backward step of the
2-4-1 network for a single example, and attention for 3 tokens. The Python notebook is the same project on your own personal data, with its own self-checks."""
import importlib.util
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'kit'))
import xl  # noqa: E402

_spec = importlib.util.spec_from_file_location('s18_nb_for_xl', HERE / 's18_nb.py')
_nb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_nb)


def one_example():
    return _nb.example()


def build(solution=False):
    N = _nb.namespace()
    E = one_example()
    x = xl.XL('Session 18: Course project', 'Five builds from first principles, in cells', solution)
    x.start('This is the GUIDED version of the course project. There are no marks: the checks only show you what works. It uses fixed toy numbers (the same as on the slides, made up to show the arithmetic) and has its own checks, labelled by build. '
            'In the Python notebook the same project runs on your own personal data, made from any text you type as a student ID, and you write functions that the self-checks run on two datasets. '
            'What this workbook covers: Build 1 by the normal equation only (no gradient descent). Build 2 for the first 5 gradient steps only (the notebook trains for thousands). '
            'Build 3 with the formula for a 2 by 2 covariance matrix. Build 4 as ONE forward and backward step for ONE example (the notebook trains a network on 40 points). Build 5 for 3 tokens with d = 2.',
            ['Sheet Linear: build the normal equation with MMULT and MINVERSE, then the mean squared error.',
             'Sheet Logistic: a table of 5 gradient steps. Fill the gradient columns and the weight updates.',
             'Sheet PCA: the covariance entries (divide by n), the two eigenvalues from the 2 by 2 formula, the first component and the scores.',
             'Sheet Network: one forward step and one backward step through the 2-4-1 network for the input (1, 2) and target 1, then one weight update.',
             'Sheet Attention: queries, keys and values with MMULT, scaled scores, a stable softmax in cells, and the output.',
             'Open the sheet Check. Every check names its build. It says All checks pass when everything is right.'])

    # ------------------------------------------------------------------ Build 1: Linear
    ws = x.sheet('Linear', {'A': 26, 'B': 12, 'C': 12, 'D': 14, 'E': 4, 'F': 14, 'G': 12, 'H': 4, 'I': 12, 'J': 12, 'K': 4, 'L': 12})
    x.band(ws, 1, 'Build 1: linear regression by the normal equation', cols=12)
    x.text(ws, 'A2', 'w = (X^T X)^-1 X^T y. Column x0 is all ones, so w0 is the intercept.', color=xl.GREY, italic=True)
    x.table(ws, 'A3', ['x0 (ones)', 'x (hours)', 'y (kWh)', 'Prediction'], [[1, float(a), float(b), None] for a, b in zip(N['x'], N['y'])])
    x.array(ws, 'D4:D9', '=MMULT(A4:B9,F8:F9)', gold=True)
    x.text(ws, 'F3', 'X^T X', bold=True)
    x.array(ws, 'F4:G5', '=MMULT(TRANSPOSE(A4:B9),A4:B9)', gold=True)
    x.text(ws, 'I3', 'Inverse', bold=True)
    x.array(ws, 'I4:J5', '=MINVERSE(F4:G5)', gold=True)
    x.text(ws, 'L3', 'X^T y', bold=True)
    x.array(ws, 'L4:L5', '=MMULT(TRANSPOSE(A4:B9),C4:C9)', gold=True)
    x.text(ws, 'F7', 'Weights w0 and w1', bold=True)
    x.array(ws, 'F8:F9', '=MMULT(I4:J5,L4:L5)', gold=True)
    x.text(ws, 'A12', 'Mean squared error', bold=True)
    x.input(ws, 'B12', answer='=SUMPRODUCT((D4:D9-C4:C9)^2)/6')
    x.text(ws, 'A13', 'Prediction for 7 hours', bold=True)
    x.input(ws, 'B13', answer='=F8+F9*7')
    x.text(ws, 'A15', 'Change one thing: change one y value by 1 and watch w1.', italic=True, color=xl.GREY)
    x.check('Build 1 (linear regression): weight w0', '=Linear!F8', 1.12, 0.001)
    x.check('Build 1 (linear regression): weight w1', '=Linear!F9', 0.98, 0.001)
    x.check('Build 1 (linear regression): mean squared error', '=Linear!B12', 0.02133, 0.0005)
    x.check('Build 1 (linear regression): prediction for 7 hours', '=Linear!B13', 7.98, 0.01)

    # ------------------------------------------------------------------ Build 2: Logistic
    wl = x.sheet('Logistic', {'A': 16, **{c: 9 for c in 'BCDEFGHIJK'}, 'L': 11, 'M': 11, 'N': 10})
    x.band(wl, 1, 'Build 2: logistic regression, 5 gradient steps', cols=14)
    x.text(wl, 'A2', 'Each row is one step. p = 1 / (1 + EXP(-(w0 + w1 x))). Gradient of the loss: average of (p - y) and of (p - y) × x. Update: w = w - learning rate × gradient.', color=xl.GREY, italic=True)
    x.text(wl, 'A3', 'x (hours)', bold=True)
    x.text(wl, 'A4', 'y (passed)', bold=True)
    for j in range(8):
        wl.cell(row=3, column=2 + j, value=float(N['xl'][j])).border = xl.BOX
        wl.cell(row=4, column=2 + j, value=float(N['yl'][j])).border = xl.BOX
    x.text(wl, 'A6', 'Learning rate', bold=True)
    wl['B6'] = 0.1
    wl['B6'].border = xl.BOX
    hdr = ['Step', 'w0', 'w1'] + [f'p{i}' for i in range(1, 9)] + ['grad w0', 'grad w1', 'Loss']
    x.table(wl, 'A8', hdr, [[s] + [None] * 13 for s in range(6)])
    cols = 'DEFGHIJK'
    xc = 'BCDEFGHI'
    for s in range(6):
        r = 9 + s
        if s == 0:
            wl[f'B{r}'] = 0
            wl[f'C{r}'] = 0
        else:
            x.input(wl, f'B{r}', answer=f'=B{r - 1}-$B$6*L{r - 1}')
            x.input(wl, f'C{r}', answer=f'=C{r - 1}-$B$6*M{r - 1}')
        for cc, xcol in zip(cols, xc):
            x.formula(wl, f'{cc}{r}', f'=1/(1+EXP(-($B{r}+$C{r}*{xcol}$3)))')
            wl[f'{cc}{r}'].number_format = '0.000'
        x.input(wl, f'L{r}', answer=f'=SUMPRODUCT(D{r}:K{r}-$B$4:$I$4)/8')
        x.input(wl, f'M{r}', answer=f'=SUMPRODUCT(D{r}:K{r}-$B$4:$I$4,$B$3:$I$3)/8')
        x.formula(wl, f'N{r}', f'=-SUMPRODUCT($B$4:$I$4*LN(D{r}:K{r})+(1-$B$4:$I$4)*LN(1-D{r}:K{r}))/8')
        for cc in 'BCLMN':
            wl[f'{cc}{r}'].number_format = '0.0000'
    x.text(wl, 'A16', 'Probability of passing at 4.5 hours after 5 steps', bold=True)
    x.input(wl, 'A17', answer='=1/(1+EXP(-(B14+C14*4.5)))')
    wl['A17'].number_format = '0.0000'
    x.text(wl, 'A19', 'Read: the loss starts at 0.693 (every p is 0.5). Does it fall at every step?', italic=True, color=xl.GREY)
    x.text(wl, 'A20', 'Change one thing: set the learning rate to 2 and watch the weights.', italic=True, color=xl.GREY)
    w5 = N['w5']
    x.check('Build 2 (logistic regression): w0 after 5 steps', '=Logistic!B14', round(float(w5[0]), 5), 0.0005)
    x.check('Build 2 (logistic regression): w1 after 5 steps', '=Logistic!C14', round(float(w5[1]), 5), 0.0005)
    x.check('Build 2 (logistic regression): loss after 5 steps', '=Logistic!N14', round(float(N['loss5']), 5), 0.0005)
    x.check('Build 2 (logistic regression): probability at 4.5 hours after 5 steps', '=Logistic!A17', round(float(1 / (1 + np.exp(-(w5[0] + w5[1] * 4.5)))), 5), 0.0005)

    # ------------------------------------------------------------------ Build 3: PCA
    wp = x.sheet('PCA', {'A': 12, 'B': 12, 'C': 14, 'D': 14, 'E': 14, 'F': 36, 'G': 14, 'H': 4, 'I': 16, 'J': 16})
    x.band(wp, 1, 'Build 3: PCA by formulas', cols=7)
    x.text(wp, 'A2', 'Centre the data, form the covariance matrix (divide by n, the course convention), find its eigenvalues with the 2 by 2 formula, then project on the first component.', color=xl.GREY, italic=True)
    x.table(wp, 'A3', ['a', 'b', 'a centred', 'b centred', 'Score on PC1'], [[float(p), float(q), None, None, None] for p, q in zip(N['a'], N['b'])])
    for r in range(4, 14):
        x.formula(wp, f'C{r}', f'=A{r}-$A$15')
        x.formula(wp, f'D{r}', f'=B{r}-$B$15')
        x.input(wp, f'E{r}', answer=f'=C{r}*$G$9+D{r}*$G$10')
        wp[f'C{r}'].number_format = '0.00'
        wp[f'D{r}'].number_format = '0.00'
        wp[f'E{r}'].number_format = '0.0000'
    x.formula(wp, 'A15', '=AVERAGE(A4:A13)')
    x.formula(wp, 'B15', '=AVERAGE(B4:B13)')
    x.text(wp, 'C15', '<- means', italic=True)
    rows = [('c11 (variance of a)', '=SUMPRODUCT(C4:C13,C4:C13)/10'), ('c12 (covariance)', '=SUMPRODUCT(C4:C13,D4:D13)/10'), ('c22 (variance of b)', '=SUMPRODUCT(D4:D13,D4:D13)/10'),
            ('Eigenvalue 1 (larger)', '=(G4+G6)/2+SQRT(((G4-G6)/2)^2+G5^2)'), ('Eigenvalue 2', '=(G4+G6)/2-SQRT(((G4-G6)/2)^2+G5^2)'),
            ('PC1, a part: c12 / length', '=G5/SQRT(G5^2+(G7-G4)^2)'), ('PC1, b part: (eigenvalue 1 - c11) / length', '=(G7-G4)/SQRT(G5^2+(G7-G4)^2)'), ('Share of variance on PC1', '=G7/(G7+G8)')]
    for i, (lab, f) in enumerate(rows):
        r = 4 + i
        x.text(wp, f'F{r}', lab, bold=True)
        x.input(wp, f'G{r}', answer=f)
        wp[f'G{r}'].number_format = '0.0000'
    x.text(wp, 'F14', 'Change one thing: change one value of a and watch the eigenvalues and the share of variance.', italic=True, color=xl.GREY)
    for lab, cell, val, tol in (('c11', 'G4', round(float(N['cov'][0, 0]), 5), 0.0005), ('c12', 'G5', round(float(N['cov'][0, 1]), 5), 0.0005), ('c22', 'G6', round(float(N['cov'][1, 1]), 5), 0.0005), ('larger eigenvalue', 'G7', round(float(N['eigvals'][1]), 5), 0.0005), ('smaller eigenvalue', 'G8', round(float(N['eigvals'][0]), 5), 0.0005),
                                ('first component, a part', 'G9', round(float(N['pc1'][0]), 5), 0.001), ('first component, b part', 'G10', round(float(N['pc1'][1]), 5), 0.001), ('share of variance on component 1', 'G11', round(float(N['ratio']), 5), 0.0005), ('score of the first point', 'E4', round(float(N['pca_scores'][0]), 5), 0.001)):
        x.check(f'Build 3 (PCA): {lab}', f'=PCA!{cell}', val, tol)

    # ------------------------------------------------------------------ Build 4: Network
    wn = x.sheet('Network', {'A': 24, 'B': 10, 'C': 10, 'D': 12, 'E': 14, 'F': 10, 'G': 16, 'H': 26, 'I': 14, 'J': 14, 'K': 16})
    x.band(wn, 1, 'Build 4: the 2-4-1 network, one forward and one backward step', cols=11)
    x.text(wn, 'A2', 'ONE illustrative example, not an XOR row: input (1, 2), target 1. Hidden layer: tanh. Output: sigmoid. Loss: -ln p. The notebook trains on 40 points; here you do one step by hand.', color=xl.GREY, italic=True)
    x.table(wn, 'A3', ['Hidden unit', 'W1 col 1', 'W1 col 2', 'z1 = W1 x', 'h = tanh(z1)', 'W2', 'gW2 = delta × h', 'delta_h = delta × W2 × (1 - h^2)', 'gW1 col 1', 'gW1 col 2', 'W2 after 1 step'],
            [[k + 1, float(E['W1'][k, 0]), float(E['W1'][k, 1]), None, None, float(E['W2'][k]), None, None, None, None, None] for k in range(4)])
    for r in range(4, 8):
        x.input(wn, f'D{r}', answer=f'=B{r}*$B$9+C{r}*$C$9')
        x.input(wn, f'E{r}', answer=f'=TANH(D{r})')
        x.input(wn, f'G{r}', answer=f'=$B$14*E{r}')
        x.input(wn, f'H{r}', answer=f'=$B$14*F{r}*(1-E{r}^2)')
        x.input(wn, f'I{r}', answer=f'=H{r}*$B$9')
        x.input(wn, f'J{r}', answer=f'=H{r}*$C$9')
        x.input(wn, f'K{r}', answer=f'=F{r}-0.5*G{r}')
        for cc in 'DEGHIJK':
            wn[f'{cc}{r}'].number_format = '0.0000'
    x.text(wn, 'A9', 'Input x1, x2', bold=True)
    wn['B9'] = 1
    wn['C9'] = 2
    x.text(wn, 'A10', 'Target y', bold=True)
    wn['B10'] = 1
    x.text(wn, 'A11', 'Output bias b2 (b1 = 0)', bold=True)
    wn['B11'] = 0.1
    x.text(wn, 'A12', 'z2 = W2 . h + b2', bold=True)
    x.input(wn, 'B12', answer='=SUMPRODUCT(F4:F7,E4:E7)+B11')
    x.text(wn, 'A13', 'p = sigmoid(z2)', bold=True)
    x.input(wn, 'B13', answer='=1/(1+EXP(-B12))')
    x.text(wn, 'A14', 'delta = p - y', bold=True)
    x.input(wn, 'B14', answer='=B13-B10')
    x.text(wn, 'A15', 'Loss = -ln p', bold=True)
    x.input(wn, 'B15', answer='=-LN(B13)')
    for r in (12, 13, 14, 15):
        wn[f'B{r}'].number_format = '0.0000'
    x.text(wn, 'A17', 'Read: delta = p - y is the same gradient as in Session 17. The gradient of b2 is delta, and the gradient of b1 is delta_h (column H). Which hidden unit gets the largest error signal (column H)?', italic=True, color=xl.GREY)
    x.text(wn, 'A18', 'Read: gW1 col 2 is twice gW1 col 1 because the second input is 2. If you leave out the input factor, the two columns would be equal.', italic=True, color=xl.GREY)
    x.check('Build 4 (neural network): output probability p', '=Network!B13', round(float(E['p']), 4), 0.0005)
    x.check('Build 4 (neural network): loss', '=Network!B15', round(float(E['loss']), 4), 0.0005)
    x.check('Build 4 (neural network): delta = p - y', '=Network!B14', round(float(E['delta']), 4), 0.0005)
    x.check('Build 4 (neural network): gradient of the first W2 weight', '=Network!G4', round(float(E['gW2'][0]), 4), 0.0005)
    x.check('Build 4 (neural network): error signal delta_h of the first hidden unit', '=Network!H4', round(float(E['dh'][0]), 4), 0.0005)
    x.check('Build 4 (neural network): gradient of W1 (unit 1, input 1)', '=Network!I4', round(float(E['gW1'][0, 0]), 4), 0.0005)
    x.check('Build 4 (neural network): gradient of W1 (unit 1, input 2)', '=Network!J4', round(float(E['gW1'][0, 1]), 4), 0.0005)
    x.check('Build 4 (neural network): gradient of W1 (unit 3, input 2)', '=Network!J6', round(float(E['gW1'][2, 1]), 4), 0.0005)
    x.check('Build 4 (neural network): first W2 weight after one step', '=Network!K4', round(float(E['W2new'][0]), 4), 0.0005)

    # ------------------------------------------------------------------ Build 5: Attention
    wa = x.sheet('Attention', {'A': 12, 'B': 12, 'C': 12, 'D': 12, 'E': 12, 'F': 4, 'G': 12, 'H': 12, 'I': 4, 'J': 12, 'K': 12})
    x.band(wa, 1, 'Build 5: scaled dot-product attention, 3 tokens', cols=11)
    x.text(wa, 'A2', 'output = softmax(Q K^T / sqrt(d)) V. Each row is shifted by its row maximum before the exponential (stable softmax).', color=xl.GREY, italic=True)
    x.text(wa, 'A3', 'X (tokens)', bold=True)
    x.text(wa, 'D3', 'Wq', bold=True)
    x.text(wa, 'G3', 'Wk', bold=True)
    x.text(wa, 'J3', 'Wv', bold=True)
    for (r0, c0, M) in ((4, 1, N['Xt']), (4, 4, N['Wq']), (4, 7, N['Wk']), (4, 10, N['Wv'])):
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                wa.cell(row=r0 + i, column=c0 + j, value=float(M[i, j])).border = xl.BOX
    x.text(wa, 'A8', 'Q = X Wq', bold=True)
    x.text(wa, 'D8', 'K = X Wk', bold=True)
    x.text(wa, 'G8', 'V = X Wv', bold=True)
    x.array(wa, 'A9:B11', '=MMULT(A4:B6,D4:E5)', gold=True)
    x.array(wa, 'D9:E11', '=MMULT(A4:B6,G4:H5)', gold=True)
    x.array(wa, 'G9:H11', '=MMULT(A4:B6,J4:K5)', gold=True)
    x.text(wa, 'A13', 'd (key dimension)', bold=True)
    wa['C13'] = 2
    wa['C13'].border = xl.BOX
    x.text(wa, 'A14', 'Scores = Q K^T / sqrt(d)', bold=True)
    x.array(wa, 'A15:C17', '=MMULT(A9:B11,TRANSPOSE(D9:E11))/SQRT(C13)', gold=True)
    x.text(wa, 'E14', 'Row maximum', bold=True)
    for r in (15, 16, 17):
        x.formula(wa, f'E{r}', f'=MAX(A{r}:C{r})')
    x.text(wa, 'A19', 'exp(score - row maximum)', bold=True)
    x.text(wa, 'E19', 'Row sum', bold=True)
    for i, r in enumerate((20, 21, 22)):
        for cc in 'ABC':
            x.input(wa, f'{cc}{r}', answer=f'=EXP({cc}{15 + i}-$E{15 + i})')
            wa[f'{cc}{r}'].number_format = '0.0000'
        x.formula(wa, f'E{r}', f'=SUM(A{r}:C{r})')
    x.text(wa, 'A24', 'Attention weights = each row divided by its row sum', bold=True)
    x.text(wa, 'E24', 'Row sum', bold=True)
    for i, r in enumerate((25, 26, 27)):
        for cc in 'ABC':
            x.input(wa, f'{cc}{r}', answer=f'={cc}{20 + i}/$E{20 + i}')
            wa[f'{cc}{r}'].number_format = '0.0000'
        x.formula(wa, f'E{r}', f'=SUM(A{r}:C{r})')
    x.text(wa, 'A29', 'Output = weights V', bold=True)
    x.array(wa, 'A30:B32', '=MMULT(A25:C27,G9:H11)', gold=True)
    x.text(wa, 'D30', 'Change one thing: set d (cell C13) to 1 and see which weights get sharper.', italic=True, color=xl.GREY)
    A = N['weights']
    x.check('Build 5 (attention): query of token 3, first entry', '=Attention!A11', 2, 0.0001)
    x.check('Build 5 (attention): key of token 3, second entry', '=Attention!E11', 2, 0.0001)
    x.check('Build 5 (attention): scaled score, token 1 query with token 3 key', '=Attention!C15', round(float(N['scores'][0, 2]), 5), 0.0005)
    x.check('Build 5 (attention): attention weight, token 1 on token 1', '=Attention!A25', round(float(A[0, 0]), 5), 0.0005)
    x.check('Build 5 (attention): attention weight, token 2 on token 1', '=Attention!A26', round(float(A[1, 0]), 5), 0.0005)
    x.check('Build 5 (attention): each row of weights adds to 1', '=Attention!E26', 1, 0.000001)
    x.check('Build 5 (attention): output of token 3, first entry', '=Attention!A32', round(float(N['out'][2, 0]), 5), 0.0005)
    x.check('Build 5 (attention): output of token 3, second entry', '=Attention!B32', round(float(N['out'][2, 1]), 5), 0.0005)
    return x
