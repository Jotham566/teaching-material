"""Session 7 lab (spreadsheet): columns of (f(x+h) - f(x)) / h, the rules against finite differences, the loss and its slope for the delivery data."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'kit'))
from xl import XL  # noqa: E402
from openpyxl.chart import ScatterChart, Reference, Series  # noqa: E402

HS = [2, 1, 0.5, 0.1, 0.01, 0.001]
WS = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
X = [1, 2, 3, 4]
Y = [3, 5, 6, 9]


def build(solution: bool) -> XL:
    x = XL('Session 7: Derivatives', 'Slopes from two nearby points, the rules, and the loss of a one-parameter model', solution)
    x.start('You build the slope of a curve from two nearby points, check the derivative rules against finite differences, and find the slope of a loss. '
            'The numbers are the same as in the Python notebook. Gold cells are yours to fill.',
            ['Sheet Shrink: fill the gold slope column. Predict first: what number do the slopes approach as h shrinks?',
             'Sheet Rules: write the slope each rule gives in the gold cells, then compare with the finite difference beside it.',
             'Sheet Loss: fill the gold loss and slope columns for the delivery data, then the best w. Predict the sign of the slope at w = 1 first.',
             'Open the sheet Check. It must say All checks pass. Then save the file.'])

    # ---------------------------------------------------------------- Shrink
    ws = x.sheet('Shrink', {'A': 24, 'B': 14, 'C': 14, 'D': 30, 'E': 4})
    x.band(ws, 1, 'Part A: shrink the step h for f(x) = x squared', cols=5)
    x.text(ws, 'A3', 'The point x', bold=True)
    x.text(ws, 'B3', 3, bold=True, border=True)
    x.text(ws, 'A4', 'f(x) = x squared at the point', bold=True)
    x.formula(ws, 'B4', '=B3^2')
    x.text(ws, 'A6', 'Step h', bold=True, border=True)
    x.text(ws, 'B6', 'x + h', bold=True, border=True)
    x.text(ws, 'C6', 'f(x + h)', bold=True, border=True)
    x.text(ws, 'D6', 'Slope = (f(x + h) - f(x)) / h', bold=True, border=True)
    for i, h in enumerate(HS):
        r = 7 + i
        x.text(ws, f'A{r}', h, border=True)
        x.formula(ws, f'B{r}', f'=$B$3+A{r}')
        x.formula(ws, f'C{r}', f'=B{r}^2')
        x.input(ws, f'D{r}', answer=f'=(C{r}-$B$4)/A{r}')
        ws[f'D{r}'].number_format = '0.0000'
    x.text(ws, 'A13', 'Read: what do the slopes approach? Which h gets closest?', italic=True, color='666666')
    x.band(ws, 15, 'The central difference, a better estimate', cols=5)
    x.text(ws, 'A17', 'Step h', bold=True)
    x.text(ws, 'B17', 0.001, bold=True, border=True)
    x.text(ws, 'A18', 'f(x - h)')
    x.formula(ws, 'B18', '=(B3-B17)^2')
    x.text(ws, 'A19', 'f(x + h)')
    x.formula(ws, 'B19', '=(B3+B17)^2')
    x.text(ws, 'A20', 'Central slope', bold=True)
    x.input(ws, 'B20', answer='=(B19-B18)/(2*B17)')
    ws['B20'].number_format = '0.0000'
    x.text(ws, 'C20', '(f(x + h) - f(x - h)) / (2 h)', italic=True, color='666666')
    x.text(ws, 'A22', 'CHANGE one thing: set the step in A12 to 0.00000000001 and look at D12. Why does the slope become unreliable?', italic=True, color='666666')
    x.check('Slope of x squared at 3 with h = 1', '=Shrink!D8', 7)
    x.check('Slope with h = 0.01', '=Shrink!D11', 6.01)
    x.check('Slope with h = 0.001', '=Shrink!D12', 6.001, tol=0.0005)
    x.check('Central slope with h = 0.001', '=Shrink!B20', 6, tol=0.0005)

    # ---------------------------------------------------------------- Rules
    wr = x.sheet('Rules', {'A': 34, 'B': 8, 'C': 16, 'D': 20, 'E': 20, 'F': 14})
    x.band(wr, 1, 'Part B: each rule against a finite difference', cols=6)
    x.text(wr, 'A3', 'Step h for the finite difference', bold=True)
    x.text(wr, 'B3', 0.00001, bold=True, border=True)
    for j, hd in enumerate(['Function', 'x', 'Rule used', 'Slope from the rule', 'Finite difference', 'Gap']):
        x.text(wr, f'{"ABCDEF"[j]}5', hd, bold=True, border=True)
    rows = [('x cubed', 2, 'power rule', '=3*B6^2', '=((B6+$B$3)^3-(B6-$B$3)^3)/(2*$B$3)', 12),
            ('e to the x', 1, 'exponential rule', '=EXP(B7)', '=(EXP(B7+$B$3)-EXP(B7-$B$3))/(2*$B$3)', 2.718282),
            ('ln x', 2, 'logarithm rule, 1/x', '=1/B8', '=(LN(B8+$B$3)-LN(B8-$B$3))/(2*$B$3)', 0.5),
            ('x squared times e to the x', 1, 'product rule', '=2*B9*EXP(B9)+B9^2*EXP(B9)', '=((B9+$B$3)^2*EXP(B9+$B$3)-(B9-$B$3)^2*EXP(B9-$B$3))/(2*$B$3)', 8.154845),
            ('x squared divided by (x + 1)', 1, 'quotient rule', '=(2*B10*(B10+1)-B10^2)/(B10+1)^2', '=((B10+$B$3)^2/(B10+$B$3+1)-(B10-$B$3)^2/(B10-$B$3+1))/(2*$B$3)', 0.75)]
    for i, (name, xv, rule, ans, fd, exp) in enumerate(rows):
        r = 6 + i
        x.text(wr, f'A{r}', name, border=True)
        x.text(wr, f'B{r}', xv, border=True)
        x.text(wr, f'C{r}', rule, border=True)
        x.input(wr, f'D{r}', answer=ans)
        wr[f'D{r}'].number_format = '0.0000'
        x.formula(wr, f'E{r}', fd)
        wr[f'E{r}'].number_format = '0.0000'
        x.formula(wr, f'F{r}', f'=ABS(D{r}-E{r})')
        wr[f'F{r}'].number_format = '0.000000'
        x.check(f'Rule slope: {name} at {xv}', f'=Rules!D{r}', exp, tol=0.001)
    x.text(wr, 'A12', 'Write each rule in the gold cell using the x in column B. The gap column should be close to zero. If it is not, one of the two is wrong.', italic=True, color='666666', wrap=True)
    wr.row_dimensions[12].height = 45

    # ---------------------------------------------------------------- Loss
    wl = x.sheet('Loss', {'A': 22, 'B': 18, 'C': 18, 'D': 22, 'E': 16})
    x.band(wl, 1, 'Part C: the loss of the model y-hat = w x and its slope', cols=5)
    x.text(wl, 'A3', 'Distance x (km)', bold=True, border=True)
    x.text(wl, 'B3', 'Fee y (thousand UGX)', bold=True, border=True)
    for i in range(4):
        x.text(wl, f'A{4 + i}', X[i], border=True)
        x.text(wl, f'B{4 + i}', Y[i], border=True)
    x.text(wl, 'A9', 'Number of rows n', bold=True)
    x.formula(wl, 'B9', '=COUNT(A4:A7)')
    x.text(wl, 'A10', 'Step h for the check', bold=True)
    x.text(wl, 'B10', 0.0001, border=True, bold=True)
    for j, hd in enumerate(['w', 'Loss L(w)', 'Slope dL/dw', 'Slope by finite difference', 'Which way to move w']):
        x.text(wl, f'{"ABCDE"[j]}11', hd, bold=True, border=True, wrap=True)
    wl.row_dimensions[11].height = 32
    for i, w in enumerate(WS):
        r = 12 + i
        x.text(wl, f'A{r}', w, border=True)
        x.input(wl, f'B{r}', answer=f'=SUMPRODUCT((A{r}*$A$4:$A$7-$B$4:$B$7)^2)/$B$9')
        x.input(wl, f'C{r}', answer=f'=2/$B$9*SUMPRODUCT($A$4:$A$7,A{r}*$A$4:$A$7-$B$4:$B$7)')
        x.formula(wl, f'D{r}', f'=(SUMPRODUCT(((A{r}+$B$10)*$A$4:$A$7-$B$4:$B$7)^2)-SUMPRODUCT(((A{r}-$B$10)*$A$4:$A$7-$B$4:$B$7)^2))/(2*$B$10*$B$9)')
        x.formula(wl, f'E{r}', f'=IF(C{r}<0,"raise w",IF(C{r}>0,"lower w","stay"))')
        for c in 'BCD':
            wl[f'{c}{r}'].number_format = '0.000'
    x.text(wl, 'A22', 'Best w (slope zero): sum of x times y, divided by sum of x squared', bold=True)
    x.input(wl, 'B23', answer='=SUMPRODUCT(A4:A7,B4:B7)/SUMPRODUCT(A4:A7,A4:A7)')
    x.text(wl, 'A23', 'Best w')
    x.text(wl, 'A24', 'Loss at the best w')
    x.input(wl, 'B24', answer='=SUMPRODUCT((B23*A4:A7-B4:B7)^2)/B9')
    x.text(wl, 'A25', 'Slope at the best w')
    x.input(wl, 'B25', answer='=2/B9*SUMPRODUCT(A4:A7,B23*A4:A7-B4:B7)')
    for c in ('B23', 'B24', 'B25'):
        wl[c].number_format = '0.0000'
    x.text(wl, 'A27', 'At w = 1 the slope is negative. Type raise or lower:')
    x.input(wl, 'B27', answer='raise')
    x.text(wl, 'A29', 'CHANGE one thing: change the last fee in B7 from 9 to 10. Predict the new best w, then read B23 (answer 2.367).', italic=True, color='666666')
    ch = ScatterChart()
    ch.title = 'Loss L(w)'
    ch.style = 13
    ch.x_axis.title = 'w'
    ch.y_axis.title = 'loss'
    s = Series(Reference(wl, min_col=2, min_row=12, max_row=20), Reference(wl, min_col=1, min_row=12, max_row=20), title='L(w)')
    s.marker.symbol = 'circle'
    ch.series.append(s)
    ch.height, ch.width = 8, 12
    wl.add_chart(ch, 'G3')
    x.check('Loss at w = 1', '=Loss!B14', 11.75)
    x.check('Loss at w = 2', '=Loss!B16', 0.75)
    x.check('Slope of the loss at w = 1', '=Loss!C14', -18.5)
    x.check('Slope of the loss at w = 3', '=Loss!C18', 11.5)
    x.check('Formula and finite difference agree at w = 1', '=ABS(Loss!C14-Loss!D14)', 0, tol=0.001)
    x.check('Best w', '=Loss!B23', 2.2333, tol=0.001)
    x.check('Loss at the best w', '=Loss!B24', 0.3417, tol=0.001)
    x.check('Slope at the best w is zero', '=IF(ISNUMBER(Loss!B25),Loss!B25,99)', 0, tol=0.001)
    x.check('Direction at w = 1', '=Loss!B27', 'raise')
    return x
