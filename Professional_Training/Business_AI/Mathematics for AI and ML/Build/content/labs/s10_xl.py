"""Session 10 spreadsheet lab: gradient descent for a line fit, one row per step. Author D."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'kit'))
import xl as X  # noqa: E402
import diagrams_math_d as D  # noqa: E402
from openpyxl.chart import LineChart, Reference  # noqa: E402
from openpyxl.utils import get_column_letter as CL  # noqa: E402

ETAS = [0.1, 0.01, 0.05, 0.2]      # block order on the Steps sheet; the first block is the one you fill in


def build(solution):
    n = D.n10()
    R = n['runs']
    x = X.XL('Session 10: Gradient descent for a line fit', 'One row per step, on the same eight boda boda trips as the Python notebook', solution)
    x.start('Fit a line to eight trips (distance in km, fare in thousand UGX) by gradient descent. Each row of the Steps sheet is one step of the update rule. You fill the gold cells of the first block, then compare four learning rates.',
            ['Step 1, sheet Data: fill the gold cell F3 with the formula AVERAGE over the distance column (do not type the number). The centred distance in column D is the distance minus your mean.',
             'Steps 2 and 3, sheet Steps, first block (eta = 0.1): row 6 is step 0 with w = 0 and b = 0. Fill the gold cells D6, E6 and F6 (the loss and the two slopes) and then B7 and C7 (w and b after one step).',
             'Step 4: the rows below your gold cells repeat the same update 30 times. On sheet Compare, fill the gold cells with the least squares slope and intercept (SLOPE and INTERCEPT) and compare with w and b at step 30.',
             'Step 5: predict first which of the four learning rates makes the loss grow. The other three blocks on sheet Steps are given (read only); the chart on sheet Compare shows the four loss curves. Fill the gold cell H5 (did the eta = 0.2 loss grow?).',
             'Change one thing: type 0.19 into the eta cell W3 of the fourth block (it holds 0.2) and watch its loss column. Afterwards put 0.2 back, so the checks stay green.'])

    d = x.sheet('Data', {'A': 8, 'B': 16, 'C': 18, 'D': 18, 'E': 4, 'F': 14, 'G': 40})
    x.band(d, 1, 'Eight trips (illustrative numbers)', 7)
    for j, h in enumerate(['Trip', 'Distance (km)', 'Fare (thousand UGX)', 'Centred distance (km)']):
        x.text(d, f'{"ABCD"[j]}2', h, bold=True, border=True, wrap=True)
    for i in range(8):
        r = 3 + i
        x.text(d, f'A{r}', i + 1, border=True)
        x.text(d, f'B{r}', float(n['x'][i]), border=True)
        x.text(d, f'C{r}', float(n['y'][i]), border=True)
        x.formula(d, f'D{r}', f'=B{r}-$F$3')     # built from the learner's own mean
    x.text(d, 'F2', 'Mean distance', bold=True)
    x.input(d, 'F3', answer='=AVERAGE(B3:B10)')
    x.text(d, 'G3', 'Fill F3 with the mean of the distance column. The centred column D uses it.', italic=True, color=X.GREY)
    x.text(d, 'F4', 'n (rows)', bold=True)
    x.formula(d, 'F5', '=COUNT(B3:B10)')
    x.check('Mean distance is 4.5 km', '=Data!F3', 4.5, 0.001)

    s = x.sheet('Steps', {CL(c): 11 for c in range(1, 30)})
    x.band(s, 1, 'Gradient descent: one row per step. Block 1 is yours.', 28)
    xr, yr = 'Data!$D$3:$D$10', 'Data!$C$3:$C$10'
    for k, eta in enumerate(ETAS):
        c0 = 1 + 7 * k
        cA, cB, cC, cD, cE, cF = (CL(c0 + j) for j in range(6))
        x.text(s, f'{cA}3', 'eta', bold=True)
        s[f'{cB}3'] = eta
        s[f'{cB}3'].font = X.Font(name=X.FONT, bold=True, color=X.RED)
        s[f'{cB}3'].border = X.BOX
        for j, h in enumerate(['Step', 'w', 'b', 'Loss', 'dL/dw', 'dL/db']):
            x.text(s, f'{CL(c0 + j)}5', h, bold=True, border=True)
        err = f'({cB}{{r}}*{xr}+{cC}{{r}}-{yr})'
        for t in range(31):
            r = 6 + t
            x.text(s, f'{cA}{r}', t, border=True)
            if t == 0:
                x.text(s, f'{cB}{r}', 0.0, border=True)
                x.text(s, f'{cC}{r}', 0.0, border=True)
            else:
                p = r - 1
                wf = f'={cB}{p}-${cB}$3*{cE}{p}'
                bf = f'={cC}{p}-${cB}$3*{cF}{p}'
                if k == 0 and t == 1:
                    x.input(s, f'{cB}{r}', answer=wf)
                    x.input(s, f'{cC}{r}', answer=bf)
                else:
                    x.formula(s, f'{cB}{r}', wf)
                    x.formula(s, f'{cC}{r}', bf)
            e = err.format(r=r)
            lf = f'=SUMPRODUCT({e}^2)/Data!$F$5'
            wf2 = f'=2*SUMPRODUCT({e}*{xr})/Data!$F$5'
            bf2 = f'=2*SUMPRODUCT({e})/Data!$F$5'
            if k == 0 and t == 0:
                x.input(s, f'{cD}{r}', answer=lf)
                x.input(s, f'{cE}{r}', answer=wf2)
                x.input(s, f'{cF}{r}', answer=bf2)
            else:
                x.formula(s, f'{cD}{r}', lf)
                x.formula(s, f'{cE}{r}', wf2)
                x.formula(s, f'{cF}{r}', bf2)
    s.freeze_panes = 'A6'

    x.check('Loss at w = 0, b = 0', '=Steps!D6', n['loss0'], 0.01)
    x.check('dL/dw at the start', '=Steps!E6', n['dw0'], 0.01)
    x.check('dL/db at the start', '=Steps!F6', n['db0'], 0.01)
    x.check('w after one step (eta = 0.1)', '=Steps!B7', n['w1'], 0.001)
    x.check('b after one step (eta = 0.1)', '=Steps!C7', n['b1'], 0.001)
    x.check('Loss after 30 steps, eta = 0.1', '=Steps!D36', R[0.1]['L'][-1], 0.001)
    x.check('Loss after 30 steps, eta = 0.01 (given block, read only)', '=Steps!K36', R[0.01]['L'][-1], 0.01)
    x.check('Loss after 30 steps, eta = 0.05 (given block, read only)', '=Steps!R36', R[0.05]['L'][-1], 0.01)
    x.check('Loss after 30 steps, eta = 0.2 (given block, read only)', '=Steps!Y36', R[0.2]['L'][-1], 0.1)

    c = x.sheet('Compare', {'A': 10, 'B': 14, 'C': 14, 'D': 14, 'E': 14, 'F': 4, 'G': 34, 'H': 14})
    x.band(c, 1, 'Four loss curves, and the least squares answer', 8)
    for j, h in enumerate(['Step'] + [f'eta = {e}' for e in (0.01, 0.05, 0.1, 0.2)]):
        x.text(c, f'{"ABCDE"[j]}3', h, bold=True, border=True)
    src = {0.01: 'K', 0.05: 'R', 0.1: 'D', 0.2: 'Y'}
    for t in range(31):
        r = 4 + t
        x.text(c, f'A{r}', t, border=True)
        for j, e in enumerate((0.01, 0.05, 0.1, 0.2)):
            x.formula(c, f'{"BCDE"[j]}{r}', f'=Steps!{src[e]}{6 + t}')
    ch = LineChart()
    ch.title = 'Loss against step (log scale)'
    ch.y_axis.title = 'loss'
    ch.x_axis.title = 'step'
    ch.y_axis.scaling.logBase = 10
    ch.height, ch.width = 9, 16
    ch.add_data(Reference(c, min_col=2, max_col=5, min_row=3, max_row=34), titles_from_data=True)
    ch.set_categories(Reference(c, min_col=1, min_row=4, max_row=34))
    c.add_chart(ch, 'G12')
    x.text(c, 'G3', 'Least squares slope (SLOPE)', bold=True)
    x.input(c, 'H3', answer='=SLOPE(Data!C3:C10,Data!D3:D10)')
    x.text(c, 'G4', 'Least squares intercept (INTERCEPT)', bold=True)
    x.input(c, 'H4', answer='=INTERCEPT(Data!C3:C10,Data!D3:D10)')
    x.text(c, 'G5', 'Did the eta = 0.2 loss grow? (1 = yes)', bold=True)
    x.input(c, 'H5', answer='=IF(E34>E4,1,0)')
    x.text(c, 'G6', 'w at step 30, eta = 0.1', bold=True)
    x.formula(c, 'H6', '=Steps!B36')
    x.text(c, 'G7', 'b at step 30, eta = 0.1', bold=True)
    x.formula(c, 'H7', '=Steps!C36')
    x.check('Least squares slope is 1.05', '=Compare!H3', n['w_star'], 0.001)
    x.check('Least squares intercept is 6.8', '=Compare!H4', n['b_star'], 0.001)
    x.check('The eta = 0.2 loss grew', '=Compare!H5', 1, 0.01)
    return x
