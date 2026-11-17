"""Session 16 workbook: maximum likelihood, MAP, cross-entropy and weight decay in cells (same numbers as the notebook labs/s16_nb.py).
The bias-variance simulation is Python only; the Bias-variance sheet here takes its three results from the notebook and asks for the total."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'kit'))
import xl  # noqa: E402

_spec = importlib.util.spec_from_file_location('s16_nb_for_xl', HERE / 's16_nb.py')
_nb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_nb)


def build(solution=False):
    N = _nb.namespace()
    x = xl.XL('Session 16: Maximum likelihood and MAP', 'Likelihood tables, squared error, cross-entropy and weight decay in cells', solution)
    x.start('The same maths as the Python notebook, in cells. You scan a likelihood over a grid, find the maximum with MAX and INDEX with MATCH, show that squared error and the Gaussian log-likelihood peak together, '
            'compute a cross-entropy, add a prior (MAP) and shrink a weight.',
            ['Sheet Coin: fill the gold cells. Predict first which theta (the chance of heads) is best. Columns B to E hold the likelihood p(data | theta) of the exact sequence, its log l(theta) in nats, the prior weight and their product for each theta. Then read the maximum likelihood estimate (MLE) and the MAP estimate.',
             'Sheet Gaussian: in the first gold cell (B8) write the natural log of the Gaussian density of the first width at mu = 9 (use LN of NORM.DIST with FALSE). The other cells of that block are already filled. Then fill the three gold columns J, K and L: the sum of the eight log densities, the sum of squared errors and the gap, minus the log-likelihood minus SSE / (2 sigma squared).',
             'Sheet Shrink: the loss of each of the four labels and their mean (the cross-entropy), the loss of the 3-class example, then the best weight for each penalty (lambda).',
             'Sheet Bias-variance: the three results come from the Python simulation. Add them up. Change one thing: read which degree has the smallest total.',
             'Open the sheet Check. It says All checks pass when every gold cell is right.'])

    # ------------------------------------------------------------------ Coin
    ws = x.sheet('Coin', {'A': 30, 'B': 16, 'C': 18, 'D': 14, 'E': 18, 'F': 12, 'G': 12, 'H': 12, 'I': 12, 'J': 12, 'K': 12})
    x.band(ws, 1, 'Coin: likelihood over a grid of theta, the chance of heads', cols=11)
    x.text(ws, 'A2', 'Flips: 1 = heads, 0 = tails. Predict first: which theta (chance of heads) will make these flips most likely?', color=xl.GREY, italic=True)
    flips = [int(v) for v in N['flips']]
    x.text(ws, 'A3', 'Flips', bold=True)
    for j, v in enumerate(flips):
        c = ws.cell(row=3, column=2 + j, value=v)
        c.border = xl.BOX
    x.text(ws, 'A4', 'Heads k', bold=True)
    x.formula(ws, 'B4', '=SUM(B3:K3)')
    x.text(ws, 'A5', 'Flips n', bold=True)
    x.formula(ws, 'B5', '=COUNT(B3:K3)')
    heads = ['theta', 'Likelihood p(data | theta)', 'Log-likelihood l(theta), nats', 'Prior weight', 'Likelihood × prior']
    x.table(ws, 'A8', heads, [[float(p), None, None, int(round(float(w))), None] for p, w in zip(N['theta_grid'], N['prior'])])
    for i in range(9):
        r = 9 + i
        x.input(ws, f'B{r}', answer=f'=A{r}^$B$4*(1-A{r})^($B$5-$B$4)')
        x.input(ws, f'C{r}', answer=f'=$B$4*LN(A{r})+($B$5-$B$4)*LN(1-A{r})')
        x.input(ws, f'E{r}', answer=f'=B{r}*D{r}')
        ws[f'B{r}'].number_format = '0.000000'
        ws[f'C{r}'].number_format = '0.0000'
        ws[f'E{r}'].number_format = '0.000000'
    x.text(ws, 'A19', 'Largest likelihood', bold=True)
    x.input(ws, 'B19', answer='=MAX(B9:B17)')
    ws['B19'].number_format = '0.000000'
    x.text(ws, 'A20', 'MLE of theta (the theta beside it)', bold=True)
    x.input(ws, 'B20', answer='=INDEX(A9:A17,MATCH(MAX(B9:B17),B9:B17,0))')
    x.text(ws, 'A21', 'MAP estimate of theta', bold=True)
    x.input(ws, 'B21', answer='=INDEX(A9:A17,MATCH(MAX(E9:E17),E9:E17,0))')
    x.text(ws, 'A22', 'Probability of 7 heads in any order at theta = 0.7', bold=True)
    x.input(ws, 'B22', answer='=COMBIN(B5,B4)*B15')
    ws['B22'].number_format = '0.0000'
    x.text(ws, 'A23', 'Read: is the MLE the same as k / n? Which way did the prior move the answer? The likelihood columns are for the exact sequence; the row above multiplies by 120 for any order. Dividing the prior weights by their total, 25, makes them probabilities and does not change the MAP estimate.', italic=True, color=xl.GREY)
    x.text(ws, 'A24', 'Change one thing: set all ten flips to 1 and watch the MLE.', italic=True, color=xl.GREY)
    x.check('Likelihood of the exact sequence at theta = 0.7', '=Coin!B15', 0.0022236, 0.000001)
    x.check('Probability of 7 heads in any order at theta = 0.7', '=Coin!B22', 0.2668, 0.0001)
    x.check('Log-likelihood of the exact sequence at theta = 0.7', '=Coin!C15', -6.1086, 0.001)
    x.check('Largest likelihood', '=Coin!B19', 0.0022236, 0.000001)
    x.check('MLE of theta', '=Coin!B20', 0.7, 0.0001)
    x.check('Likelihood × prior at theta = 0.6', '=Coin!E14', 0.0071664, 0.000001)
    x.check('MAP estimate of theta', '=Coin!B21', 0.6, 0.0001)

    # ------------------------------------------------------------------ Gaussian
    wg = x.sheet('Gaussian', {'A': 14, **{c: 11 for c in 'BCDEFGHI'}, 'J': 16, 'K': 12, 'L': 14})
    x.band(wg, 1, 'Gaussian mean: log-likelihood and squared error', cols=12)
    x.text(wg, 'A2', 'Widths of a part in mm. The model predicts the same width mu for every part (y-hat = mu), plus Gaussian noise with a known standard deviation sigma. Predict the best mu before you look.', color=xl.GREY, italic=True)
    x.text(wg, 'A3', 'Widths y', bold=True)
    for j, v in enumerate(N['y']):
        c = wg.cell(row=3, column=2 + j, value=float(v))
        c.border = xl.BOX
    x.text(wg, 'A4', 'sigma', bold=True)
    wg['B4'] = 1.0
    wg['B4'].border = xl.BOX
    x.text(wg, 'A6', 'Each cell B8 to I18 is the natural log of the Gaussian density of one width at that mu. The first cell is yours; the rest follow the same pattern.', italic=True, color=xl.GREY)
    hdr = ['mu'] + [f'ln dens y{i}' for i in range(1, 9)] + ['Log-likelihood', 'SSE', 'Gap']
    x.table(wg, 'A7', hdr, [[float(m)] + [None] * 11 for m in N['mu_grid']])
    cols = 'BCDEFGHI'
    for i in range(11):
        r = 8 + i
        for cl in cols:
            f = f'=LN(_xlfn.NORM.DIST({cl}$3,$A{r},$B$4,FALSE))'
            if cl == 'B' and r == 8:
                x.input(wg, 'B8', answer=f)
            else:
                x.formula(wg, f'{cl}{r}', f)
            wg[f'{cl}{r}'].number_format = '0.000'
        x.input(wg, f'J{r}', answer=f'=SUM(B{r}:I{r})')
        x.input(wg, f'K{r}', answer=f'=SUMPRODUCT(($B$3:$I$3-A{r})^2)')
        x.input(wg, f'L{r}', answer=f'=-J{r}-K{r}/(2*$B$4^2)')
        wg[f'J{r}'].number_format = '0.0000'
        wg[f'K{r}'].number_format = '0.00'
        wg[f'L{r}'].number_format = '0.0000'
    x.text(wg, 'A20', 'Best mu', bold=True)
    x.input(wg, 'B20', answer='=INDEX(A8:A18,MATCH(MAX(J8:J18),J8:J18,0))')
    x.text(wg, 'A21', 'Largest log-likelihood', bold=True)
    x.input(wg, 'B21', answer='=MAX(J8:J18)')
    x.text(wg, 'A22', 'SSE at the best mu', bold=True)
    x.input(wg, 'B22', answer='=INDEX(K8:K18,MATCH(MAX(J8:J18),J8:J18,0))')
    x.text(wg, 'A23', 'The constant (average gap)', bold=True)
    x.input(wg, 'B23', answer='=AVERAGE(L8:L18)')
    x.text(wg, 'A25', 'Read: the gap column is the same number in every row: n/2 ln(2 pi sigma squared), 7.3515 when sigma = 1. What does that say about squared error and the log-likelihood?', italic=True, color=xl.GREY)
    x.text(wg, 'A26', 'Change one thing: set sigma (B4) to 2 and watch which mu is best and what the gap becomes (12.8967). Then set it back to 1.', italic=True, color=xl.GREY)
    x.check('Best mu', '=Gaussian!B20', 10.25, 0.0001)
    x.check('Largest log-likelihood', '=Gaussian!B21', -10.0215, 0.001)
    x.check('Sum of squared errors at the best mu', '=Gaussian!B22', 5.34, 0.001)
    x.check('The constant n/2 ln(2 pi sigma^2), sigma = 1', '=Gaussian!B23', 7.3515, 0.001)

    # ------------------------------------------------------------------ Shrink
    wsh = x.sheet('Shrink', {'A': 34, 'B': 16, 'C': 16, 'D': 14})
    x.band(wsh, 1, 'Cross-entropy and weight decay', cols=4)
    x.text(wsh, 'A3', 'Cross-entropy of four labels', bold=True)
    x.table(wsh, 'A4', ['True label y', 'Probability of class 1', 'Loss for the row'], [[int(v), float(p), None] for v, p in zip(N['y_true'], N['p_pred'])])
    for i in range(4):
        r = 5 + i
        x.input(wsh, f'C{r}', answer=f'=-(A{r}*LN(B{r})+(1-A{r})*LN(1-B{r}))')
        wsh[f'C{r}'].number_format = '0.0000'
    x.text(wsh, 'A10', 'Binary cross-entropy (mean loss, nats)', bold=True)
    x.input(wsh, 'B10', answer='=AVERAGE(C5:C8)')
    x.text(wsh, 'A11', 'Three classes: probabilities', bold=True)
    for j, v in enumerate(N['probs3']):
        c = wsh.cell(row=11, column=2 + j, value=float(v))
        c.border = xl.BOX
    x.text(wsh, 'A12', 'Loss when the first class is true', bold=True)
    x.input(wsh, 'B12', answer='=-LN(B11)')
    x.text(wsh, 'A14', 'Weight decay: fit y = w x', bold=True)
    x.text(wsh, 'A15', 'x', bold=True)
    x.text(wsh, 'A16', 'y', bold=True)
    for j in range(3):
        wsh.cell(row=15, column=2 + j, value=float(N['x'][j])).border = xl.BOX
        wsh.cell(row=16, column=2 + j, value=float(N['y_reg'][j])).border = xl.BOX
    x.text(wsh, 'A17', 'Sum of x times y', bold=True)
    x.formula(wsh, 'B17', '=SUMPRODUCT(B15:D15,B16:D16)')
    x.text(wsh, 'A18', 'Sum of x squared', bold=True)
    x.formula(wsh, 'B18', '=SUMPRODUCT(B15:D15,B15:D15)')
    x.table(wsh, 'A20', ['lambda', 'Best weight w'], [[float(v), None] for v in (0, 1, 5, 14)])
    for i in range(4):
        r = 21 + i
        x.input(wsh, f'B{r}', answer=f'=$B$17/($B$18+A{r})')
        wsh[f'B{r}'].number_format = '0.0000'
    x.text(wsh, 'A26', 'Read: as lambda grows, does w grow or shrink?', italic=True, color=xl.GREY)
    x.check('Binary cross-entropy of the four labels', '=Shrink!B10', 0.2990, 0.001)
    x.check('Loss for the 3-class example', '=Shrink!B12', 0.3567, 0.001)
    for i, (lam, w) in enumerate(zip((0, 1, 5, 14), N['w_ridge'])):
        x.check(f'Best weight with lambda = {lam}', f'=Shrink!B{21 + i}', round(float(w), 4), 0.001)

    # ------------------------------------------------------------------ Bias-variance
    wb = x.sheet('Bias-variance', {'A': 22, 'B': 18, 'C': 14, 'D': 14, 'E': 18})
    x.band(wb, 1, 'Bias and variance (results of the Python simulation)', cols=5)
    x.text(wb, 'A2', 'Three models fitted to 300 noisy training sets. The noise standard deviation is 0.3.', color=xl.GREY, italic=True)
    x.table(wb, 'A4', ['Model', 'Bias squared', 'Variance', 'Noise variance', 'Expected error'],
            [[f'Degree {d}', round(float(N['bias2'][d]), 4), round(float(N['variance'][d]), 4), 0.09, None] for d in N['degrees']])
    for i in range(3):
        r = 5 + i
        x.input(wb, f'E{r}', answer=f'=B{r}+C{r}+D{r}')
        wb[f'E{r}'].number_format = '0.0000'
    x.text(wb, 'A9', 'Smallest expected error', bold=True)
    x.input(wb, 'B9', answer='=MIN(E5:E7)')
    wb['B9'].number_format = '0.0000'
    x.text(wb, 'A10', 'Degree with the smallest error', bold=True)
    x.input(wb, 'B10', answer='=INDEX(A5:A7,MATCH(MIN(E5:E7),E5:E7,0))')
    x.text(wb, 'A12', 'Change one thing: type 0.36 for the noise variance of degree 9 (a noisier world) and watch its total.', italic=True, color=xl.GREY)
    for i, d in enumerate(N['degrees']):
        x.check(f'Expected error, degree {d}', f'=\'Bias-variance\'!E{5 + i}', round(float(N['expected_error'][d]), 4), 0.001)
    x.check('Degree with the smallest expected error', "='Bias-variance'!B10", 'Degree 3')
    return x
