"""Session 12 spreadsheet lab: stable softmax, log-sum-exp, 16-bit limits, ridge in closed form with MMULT and MINVERSE, weight decay, a constraint. Author D."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'kit'))
from xl import XL, BOX  # noqa: E402
import diagrams_math_d as D  # noqa: E402
import numpy as np  # noqa: E402


def build(solution: bool):
    d = D.n12()
    R = {r['lam']: r for r in d['rows']}
    r3, r5 = R[0.1], R[10.0]
    x = XL('Session 12: Optimisation in practice', 'Stable softmax, log-sum-exp, 16-bit limits, a ridge fit in closed form, weight decay and a constraint', solution)
    x.start('You calculate the same numbers as the Python notebook. First a softmax that overflows and its stable version, then the limits of 16-bit numbers, then a ridge fit of a degree 9 curve to ten points with MMULT and MINVERSE.',
            ['Sheet Softmax: the naive column overflows on purpose. Fill the gold cells: the maximum, the shifted exponentials, the probabilities, the log-sum-exp and the log-probabilities.',
             'Sheet Formats: the largest 16-bit number, what exp(12) does in 16 bits, and the sum of logs for 400 tokens.',
             'Sheet Ridge: predict first, then fill the gold blocks from top to bottom: X^T X + lambda P, X^T y, the inverse, the weights, then the training and validation errors. For a matrix result in Excel, select the whole gold block, type the formula and confirm with Ctrl+Shift+Enter. In Google Sheets, type the formula in the top-left gold cell of the block and press Enter; it fills the block.',
             'Still on sheet Ridge: choose lambda by the lowest validation error (try the six values 0, 0.001, 0.01, 0.1, 1, 10 in B2), put your chosen value back in B2, and only then fill the test error at the bottom. Report it once.',
             'Sheet Small: one weight by hand with several values of lambda, one weight-decay step, the best point on a line, and a clipped gradient.',
             'Change one thing: type 10 into the lambda cell (B2) of the Ridge sheet. The validation error should rise to %.4f. Afterwards put 0.1 back, because the Check sheet expects the lambda = 0.1 values.' % r5['rmse_te'],
             'Sheet Check: it says All the checks pass when every answer is right.'])

    # ------------------------------------------------------------------ Softmax
    ws = x.sheet('Softmax', {'A': 46, 'B': 14, 'C': 22, 'D': 16, 'E': 16, 'F': 16})
    x.band(ws, 1, 'Softmax of the scores (logits) 1000, 1001, 1002', cols=6)
    for j, h in enumerate(['Score z', 'Naive: EXP(z)', 'Shifted: EXP(z - max)', 'Probability', 'ln of probability']):
        x.text(ws, f'{"BCDEF"[j]}3', h, bold=True, border=True, wrap=True)
    x.text(ws, 'A3', 'Class', bold=True, border=True)
    for i, z in enumerate([1000, 1001, 1002]):
        r = 4 + i
        x.text(ws, f'A{r}', f'Score {i + 1}', border=True)
        x.text(ws, f'B{r}', z, border=True)
        x.formula(ws, f'C{r}', f'=IFERROR(EXP(B{r}),"overflow")')
        x.input(ws, f'D{r}', f'=EXP(B{r}-$B$8)')
        x.input(ws, f'E{r}', f'=D{r}/$B$9')
        x.input(ws, f'F{r}', f'=B{r}-$B$10')
    x.text(ws, 'A8', 'Maximum score m = MAX(B4:B6)')
    x.input(ws, 'B8', '=MAX(B4:B6)')
    x.text(ws, 'A9', 'Sum of the shifted exponentials')
    x.input(ws, 'B9', '=SUM(D4:D6)')
    x.text(ws, 'A10', 'Log-sum-exp = m + LN(sum)')
    x.input(ws, 'B10', '=B8+LN(B9)')
    x.text(ws, 'A12', 'Check with small scores (2, 1, 0.1): the naive way is fine here', bold=True)
    for i, z in enumerate([2, 1, 0.1]):
        x.text(ws, f'A{13 + i}', f'Score {i + 1}', border=True)
        x.text(ws, f'B{13 + i}', z, border=True)
        x.input(ws, f'C{13 + i}', f'=EXP(B{13 + i})/SUMPRODUCT(EXP($B$13:$B$15))')
    sb = d['soft_big']
    for lab, ref, exp, tol in [('Stable softmax, first score', 'E4', float(sb[0]), 0.0001), ('Stable softmax, second score', 'E5', float(sb[1]), 0.0001), ('Stable softmax, third score', 'E6', float(sb[2]), 0.0001),
                               ('Log-sum-exp of (1000, 1001, 1002)', 'B10', d['lse_big'], 0.0001), ('ln of the first probability', 'F4', 1000 - d['lse_big'], 0.0001),
                               ('Naive softmax of (2, 1, 0.1), first score', 'C13', float(d['soft_small'][0]), 0.0001)]:
        x.check(lab, f'=Softmax!{ref}', exp, tol)

    # ------------------------------------------------------------------ Formats
    ws = x.sheet('Formats', {'A': 66, 'B': 18})
    x.band(ws, 1, 'Limits of 16-bit numbers and a long product', cols=2)
    x.text(ws, 'A3', 'Largest float16 number = (2 - 2^-10) * 2^15', wrap=True)
    x.input(ws, 'B3', '=(2-2^-10)*2^15')
    x.text(ws, 'A4', 'EXP(12), the number a model would have to store')
    x.formula(ws, 'B4', '=EXP(12)')
    x.text(ws, 'A5', 'Does EXP(12) fit in float16? Type yes or no. (Compare B4 with B3.)', wrap=True)
    x.input(ws, 'B5', '=IF(B4>B3,"no","yes")')
    x.text(ws, 'A6', 'The product 0.1^300 (still representable in float64)')
    x.formula(ws, 'B6', '=0.1^300')
    x.text(ws, 'A7', 'The sum of 400 logs of 0.1 = 400 * LN(0.1)')
    x.input(ws, 'B7', '=400*LN(0.1)')
    x.text(ws, 'A8', 'The sum of 300 logs of 0.1 = 300 * LN(0.1)')
    x.input(ws, 'B8', '=300*LN(0.1)')
    x.text(ws, 'A10', 'A product of 400 probabilities of 0.1 is 1E-400. Float64 holds numbers down to about 5E-324 (with few digits below 1E-308), so 0.1^n is stored as exactly 0 from n = 324. The sum of the logs is an ordinary number.', wrap=True, color='666666')
    ws.row_dimensions[10].height = 45
    for lab, ref, exp, tol in [('Largest float16 number', 'B3', 65504, 0.5), ('Does exp(12) fit in float16', 'B5', 'no', 0), ('Sum of 400 logs of 0.1', 'B7', 400 * np.log(0.1), 0.001), ('Sum of 300 logs of 0.1', 'B8', 300 * np.log(0.1), 0.001)]:
        x.check(lab, f'=Formats!{ref}', exp, tol)

    # ------------------------------------------------------------------ Ridge
    ws = x.sheet('Ridge', {'A': 30, **{c: 13 for c in 'BCDEFGHIJKLM'}})
    x.band(ws, 1, 'Ridge fit of a degree 9 polynomial to 10 points (illustrative data)', cols=13)
    x.text(ws, 'A2', 'lambda (change me)', bold=True)
    x.text(ws, 'B2', 0.1, border=True, bold=True)
    x.text(ws, 'A4', 'Training points: x, y and the powers 1, x, ..., x^9 (X is C6:L15)', bold=True)
    x.text(ws, 'A5', 'x', bold=True, border=True)
    x.text(ws, 'B5', 'y', bold=True, border=True)
    for k in range(10):
        x.text(ws, f'{"CDEFGHIJKL"[k]}5', f'x^{k}', bold=True, border=True)
    for i in range(10):
        r = 6 + i
        ws[f'A{r}'] = float(d['xtr'][i]); ws[f'B{r}'] = float(d['ytr'][i])
        for k in range(10):
            ws[f'{"CDEFGHIJKL"[k]}{r}'] = f'=$A{r}^{k}'
        for c in 'ABCDEFGHIJKL':
            ws[f'{c}{r}'].border = BOX
    x.text(ws, 'A17', 'Penalty matrix P (given): the identity, but the intercept entry is 0', bold=True)
    for i in range(10):
        for j in range(10):
            ws[f'{"CDEFGHIJKL"[j]}{18 + i}'] = 1 if (i == j and i > 0) else 0
            ws[f'{"CDEFGHIJKL"[j]}{18 + i}'].border = BOX
    x.text(ws, 'A18', 'P is C18:L27')
    x.text(ws, 'A30', 'Step 1: A = X^T X + lambda P (C31:L40)', bold=True, wrap=True)
    x.array(ws, 'C31:L40', '=MMULT(TRANSPOSE(C6:L15),C6:L15)+$B$2*C18:L27', gold=True)
    x.text(ws, 'A43', 'Step 2: X^T y (C44:C53). MMULT(TRANSPOSE(X), y)', bold=True)
    x.array(ws, 'C44:C53', '=MMULT(TRANSPOSE(C6:L15),B6:B15)', gold=True)
    x.text(ws, 'A56', 'Step 3: inverse of A (C57:L66). MINVERSE(A)', bold=True)
    x.array(ws, 'C57:L66', '=MINVERSE(C31:L40)', gold=True)
    x.text(ws, 'A69', 'Step 4: weights w (C70:C79). MMULT(inverse, X^T y)', bold=True)
    x.array(ws, 'C70:C79', '=MMULT(C57:L66,C44:C53)', gold=True)
    x.text(ws, 'A82', 'Sum of the squared weights, without the intercept: SUMSQ(C71:C79)', bold=True, wrap=True)
    x.input(ws, 'C82', '=SUMSQ(C71:C79)')
    x.text(ws, 'A84', 'Training predictions X w (C85:C94)', bold=True)
    x.array(ws, 'C85:C94', '=MMULT(C6:L15,C70:C79)', gold=True)
    x.text(ws, 'A96', 'Training error RMSE = SQRT(SUMXMY2(C85:C94, B6:B15) / 10)', bold=True, wrap=True)
    x.input(ws, 'C96', '=SQRT(SUMXMY2(C85:C94,B6:B15)/10)')
    # held-out points
    x.text(ws, 'A99', 'Validation points (never used to fit; they choose lambda): x, y and the powers', bold=True)
    x.text(ws, 'A100', 'x', bold=True, border=True); x.text(ws, 'B100', 'y', bold=True, border=True)
    for k in range(10):
        x.text(ws, f'{"CDEFGHIJKL"[k]}100', f'x^{k}', bold=True, border=True)
    for i in range(20):
        r = 101 + i
        ws[f'A{r}'] = float(d['xte'][i]); ws[f'B{r}'] = float(d['yte'][i])
        for k in range(10):
            ws[f'{"CDEFGHIJKL"[k]}{r}'] = f'=$A{r}^{k}'
        for c in 'ABCDEFGHIJKL':
            ws[f'{c}{r}'].border = BOX
    x.text(ws, 'A122', 'Predictions on the 20 validation points (C123:C142)', bold=True, wrap=True)
    x.array(ws, 'C123:C142', '=MMULT(C101:L120,C70:C79)', gold=True)
    x.text(ws, 'A144', 'Validation error RMSE (choose lambda by this)', bold=True, wrap=True)
    x.input(ws, 'C144', '=SQRT(SUMXMY2(C123:C142,B101:B120)/20)')
    # test points: untouched until lambda is chosen, then used once
    x.text(ws, 'A147', 'Test points (use once, after lambda is chosen): x, y and the powers', bold=True)
    x.text(ws, 'A148', 'x', bold=True, border=True); x.text(ws, 'B148', 'y', bold=True, border=True)
    for k in range(10):
        x.text(ws, f'{"CDEFGHIJKL"[k]}148', f'x^{k}', bold=True, border=True)
    for i in range(20):
        r = 149 + i
        ws[f'A{r}'] = float(d['xts'][i]); ws[f'B{r}'] = float(d['yts'][i])
        for k in range(10):
            ws[f'{"CDEFGHIJKL"[k]}{r}'] = f'=$A{r}^{k}'
        for c in 'ABCDEFGHIJKL':
            ws[f'{c}{r}'].border = BOX
    x.text(ws, 'A170', 'Predictions on the 20 test points (C171:C190, given)', bold=True, wrap=True)
    x.array(ws, 'C171:C190', '=MMULT(C149:L168,C70:C79)')
    x.text(ws, 'A192', 'Test error RMSE, reported once', bold=True, wrap=True)
    x.input(ws, 'C192', '=SQRT(SUMXMY2(C171:C190,B149:B168)/20)')
    for lab, ref, exp, tol in [('Weight w0 (intercept) at lambda = 0.1', 'C70', float(r3['w'][0]), 0.001), ('Weight w1 at lambda = 0.1', 'C71', float(r3['w'][1]), 0.001), ('Sum of the squared weights at lambda = 0.1', 'C82', r3['norm2'], 0.0005),
                               ('Training error at lambda = 0.1', 'C96', r3['rmse_tr'], 0.0002), ('Validation error at lambda = 0.1', 'C144', r3['rmse_te'], 0.0002),
                               ('Test error at the chosen lambda = 0.1', 'C192', d['rmse_test'], 0.0002)]:
        x.check(lab, f'=Ridge!{ref}', exp, tol)

    # ------------------------------------------------------------------ Small
    ws = x.sheet('Small', {'A': 56, 'B': 14, 'C': 14, 'D': 14, 'E': 14, 'F': 14})
    x.band(ws, 1, 'One weight, weight decay, a constraint and clipping (illustrative numbers)', cols=6)
    x.text(ws, 'A3', 'Part 1: one weight with y-hat = w x. Data x = 1, 2, 3 and y = 2.1, 3.9, 6.2', bold=True)
    for r, (xv, yv) in enumerate([(1, 2.1), (2, 3.9), (3, 6.2)]):
        x.text(ws, f'A{4 + r}', f'Point {r + 1}: x and y', border=True)
        x.text(ws, f'B{4 + r}', xv, border=True); x.text(ws, f'C{4 + r}', yv, border=True)
    x.text(ws, 'A8', 'Sum of x times y: SUMPRODUCT(B4:B6,C4:C6)'); x.formula(ws, 'B8', '=SUMPRODUCT(B4:B6,C4:C6)')
    x.text(ws, 'A9', 'Sum of x squared: SUMSQ(B4:B6)'); x.formula(ws, 'B9', '=SUMSQ(B4:B6)')
    x.text(ws, 'A10', 'Weight w = sum(x y) / (sum(x^2) + lambda)', bold=True)
    for j, lam in enumerate([0, 1, 14, 140]):
        c = 'BCDE'[j]
        x.text(ws, f'{c}11', lam, border=True, bold=True)
        x.input(ws, f'{c}12', f'=$B$8/($B$9+{c}11)')
    x.text(ws, 'A11', 'lambda'); x.text(ws, 'A12', 'w')
    x.text(ws, 'A14', 'Part 2: one weight-decay step. w = 2, eta = 0.1, lambda = 0.5, dL/dw = 1', bold=True)
    for r, (lab, v) in enumerate([('w', 2), ('eta', 0.1), ('lambda', 0.5), ('dL/dw', 1)]):
        x.text(ws, f'A{15 + r}', lab, border=True); x.text(ws, f'B{15 + r}', v, border=True)
    x.text(ws, 'A19', 'New w = (1 - 2 eta lambda) w - eta dL/dw', bold=True)
    x.input(ws, 'B19', '=(1-2*B16*B17)*B15-B16*B18')
    x.text(ws, 'A21', 'Part 3: the loss w1^2 + w2^2 on the line w1 + w2 = 2', bold=True)
    for j, h in enumerate(['w1', 'w2 = 2 - w1', 'Loss']):
        x.text(ws, f'{"ABC"[j]}22', h, bold=True, border=True)
    for i, v in enumerate([0, 0.5, 1, 1.5, 2]):
        r = 23 + i
        x.text(ws, f'A{r}', v, border=True)
        x.formula(ws, f'B{r}', f'=2-A{r}')
        x.input(ws, f'C{r}', f'=A{r}^2+B{r}^2')
    x.text(ws, 'A28', 'Lowest loss on the line: MIN(C23:C27)'); x.input(ws, 'B28', '=MIN(C23:C27)')
    x.text(ws, 'A29', 'w1 at the lowest loss: INDEX(A23:A27, MATCH(B28, C23:C27, 0))'); x.input(ws, 'B29', '=INDEX(A23:A27,MATCH(B28,C23:C27,0))')
    x.text(ws, 'A31', 'Part 4: clipping a gradient g = (30, 40) to length at most c = 5', bold=True)
    x.text(ws, 'A32', 'g1 and g2', border=True); x.text(ws, 'B32', 30, border=True); x.text(ws, 'C32', 40, border=True)
    x.text(ws, 'A33', 'Length of g = SQRT(SUMSQ(B32:C32))'); x.input(ws, 'B33', '=SQRT(SUMSQ(B32:C32))')
    x.text(ws, 'A34', 'Clipped g1 and g2 (multiply by 5 / length)'); x.input(ws, 'B34', '=B32*5/B33'); x.input(ws, 'C34', '=C32*5/B33')
    for lab, ref, exp, tol in [('One weight at lambda = 0', 'B12', 28.5 / 14, 0.0001), ('One weight at lambda = 1', 'C12', 1.9, 0.0001), ('One weight at lambda = 14', 'D12', 28.5 / 28, 0.0001),
                               ('Weight after one decay step', 'B19', 1.7, 0.0001), ('Lowest loss on the line', 'B28', 2, 0.0001), ('Best w1 on the line', 'B29', 1, 0.0001),
                               ('Length of the gradient', 'B33', 50, 0.0001), ('Clipped g1', 'B34', 3, 0.0001), ('Clipped g2', 'C34', 4, 0.0001)]:
        x.check(lab, f'=Small!{ref}', exp, tol)
    return x
