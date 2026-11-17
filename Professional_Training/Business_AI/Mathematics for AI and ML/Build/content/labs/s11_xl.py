"""Session 11 spreadsheet lab: backpropagation by hand, step by step in cells, plus 50 training steps. Author D."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'kit'))
import xl as X  # noqa: E402
import diagrams_math_d as D  # noqa: E402
import numpy as np  # noqa: E402
from openpyxl.chart import LineChart, Reference  # noqa: E402


def _loss_after(n, steps):
    """Loss of the tiny network after `steps` updates with eta = 0.5 (same loop as the Train sheet)."""
    x, y, eta = n['x'], n['y'], n['eta']
    W1, b1, W2, b2 = [n[k].copy() for k in ('W1', 'b1', 'W2', 'b2')]
    for _ in range(steps):
        a = 1 / (1 + np.exp(-(W1 @ x + b1)))
        d2 = (W2 @ a + b2) - y
        d1 = (W2.T @ d2).ravel() * a * (1 - a)
        W2, b2, W1, b1 = W2 - eta * np.outer(d2, a), b2 - eta * d2, W1 - eta * np.outer(d1, x), b1 - eta * d1
    a = 1 / (1 + np.exp(-(W1 @ x + b1)))
    return float(0.5 * ((W2 @ a + b2)[0] - y) ** 2)


def sig(e):
    return f'1/(1+EXP(-({e})))'


def build(solution):
    n = D.n11()
    s1, s2, s3 = n['s1'], n['s2'], n['s3']
    W1, b1, W2, b2 = n['W1'], n['b1'], n['W2'], n['b2']
    x = X.XL('Session 11: Backpropagation by hand', 'The tiny network of the slides: forward pass, backward pass, update, finite-difference check and 50 training steps, all in cells', solution)
    x.start('Run one training step of the tiny network (2 inputs, 2 hidden units with a sigmoid, 1 output) in cells: the forward pass, the backward pass with the chain rule, the update, and a check with finite differences. '
            'Then a second sheet repeats the step 50 times, one row per step.',
            ['Sheet Network: layers are written in brackets, so W(1) and b(1) belong to the hidden layer, W(2) and b(2) to the output, and delta(1)_2 is the delta of hidden unit 2. The inputs, the target, the learning rate and the nine parameters are given. Fill the gold cells from top to bottom: forward pass (z, a, y-hat, L), then the deltas, then the nine gradients.',
             'Predict first: is y-hat bigger or smaller than the target 1? Which gradients are negative?',
             'Fill the gold cells of the update (the new parameters) and the new loss. The loss should fall a lot.',
             'Fill the gold cell of the finite difference and compare it with the backpropagation gradient next to it.',
             'Sheet Train: each row is one training step. Row 1 copies your new parameters from the Network sheet, so the rows below build on your work. Find the loss after 1, 2 and 50 steps and look at the chart (log scale).',
             'Change one thing: type 5 into the eta cell (B6) of the Network sheet and watch the Train sheet. What happens to the loss? Afterwards put 0.5 back, because the last checks depend on it.'])
    ws = x.sheet('Network', {'A': 40, 'B': 18, 'C': 18, 'D': 14, 'E': 4})
    x.band(ws, 1, 'The tiny network (illustrative numbers)', 4)
    for r, lab, v in [(3, 'x1 (input 1)', 1.0), (4, 'x2 (input 2)', 2.0), (5, 'y (target)', 1.0), (6, 'eta (learning rate)', 0.5)]:
        x.text(ws, f'A{r}', lab, bold=True)
        x.text(ws, f'B{r}', v, border=True)
    for j, h in enumerate(['W(1) and b(1)', 'weight from x1', 'weight from x2', 'bias']):
        x.text(ws, f'{"ABCD"[j]}8', h, bold=True, border=True)
    for i in range(2):
        x.text(ws, f'A{9 + i}', f'Hidden unit {i + 1}', border=True)
        x.text(ws, f'B{9 + i}', float(W1[i][0]), border=True)
        x.text(ws, f'C{9 + i}', float(W1[i][1]), border=True)
        x.text(ws, f'D{9 + i}', float(b1[i]), border=True)
    for j, h in enumerate(['W(2) and b(2)', 'weight from hidden 1', 'weight from hidden 2', 'bias']):
        x.text(ws, f'{"ABCD"[j]}12', h, bold=True, border=True)
    x.text(ws, 'A13', 'Output unit', border=True)
    x.text(ws, 'B13', float(W2[0][0]), border=True)
    x.text(ws, 'C13', float(W2[0][1]), border=True)
    x.text(ws, 'D13', float(b2[0]), border=True)

    x.band(ws, 15, 'Step 1: the forward pass', 4)
    for j, h in enumerate(['Hidden unit', 'z(1) = weighted sum + bias', 'a(1) = sigmoid(z(1))']):
        x.text(ws, f'{"ABC"[j]}16', h, bold=True, border=True)
    for i in range(2):
        r = 17 + i
        x.text(ws, f'A{r}', f'Hidden unit {i + 1}', border=True)
        x.input(ws, f'B{r}', answer=f'=B{9 + i}*$B$3+C{9 + i}*$B$4+D{9 + i}')
        x.input(ws, f'C{r}', answer=f'=1/(1+EXP(-B{r}))')
    x.text(ws, 'A19', 'Prediction y-hat = W(2) a(1) + b(2)', bold=True)
    x.input(ws, 'B19', answer='=B13*C17+C13*C18+D13')
    x.text(ws, 'A20', 'Loss L = 0.5 (y-hat - y)^2', bold=True)
    x.input(ws, 'B20', answer='=0.5*(B19-B5)^2')

    x.band(ws, 22, 'Step 2: the backward pass', 4)
    x.text(ws, 'A23', 'delta(2) = y-hat - y', bold=True)
    x.input(ws, 'B23', answer='=B19-B5')
    x.text(ws, 'A24', 'delta(1)_1 = W(2)_1 × delta(2) × a(1)_1 × (1 - a(1)_1)', bold=True, wrap=True)
    x.input(ws, 'B24', answer='=B13*B23*C17*(1-C17)')
    x.text(ws, 'A25', 'delta(1)_2', bold=True)
    x.input(ws, 'B25', answer='=C13*B23*C18*(1-C18)')
    for j, h in enumerate(['The nine gradients', 'first', 'second', 'bias']):
        x.text(ws, f'{"ABCD"[j]}27', h, bold=True, border=True)
    x.text(ws, 'A28', 'dL/dW(1) row 1 (input 1, input 2, bias)', border=True)
    x.input(ws, 'B28', answer='=B24*$B$3')
    x.input(ws, 'C28', answer='=B24*$B$4')
    x.input(ws, 'D28', answer='=B24')
    x.text(ws, 'A29', 'dL/dW(1) row 2 (input 1, input 2, bias)', border=True)
    x.input(ws, 'B29', answer='=B25*$B$3')
    x.input(ws, 'C29', answer='=B25*$B$4')
    x.input(ws, 'D29', answer='=B25')
    x.text(ws, 'A30', 'dL/dW(2) (hidden 1, hidden 2, bias)', border=True)
    x.input(ws, 'B30', answer='=B23*C17')
    x.input(ws, 'C30', answer='=B23*C18')
    x.input(ws, 'D30', answer='=B23')

    x.band(ws, 32, 'Step 3: the update, new = old - eta × gradient', 4)
    for j, h in enumerate(['New parameters', 'first', 'second', 'bias']):
        x.text(ws, f'{"ABCD"[j]}33', h, bold=True, border=True)
    for r, lab, src, par in [(34, 'New W(1) row 1', 28, 9), (35, 'New W(1) row 2', 29, 10), (36, 'New W(2)', 30, 13)]:
        x.text(ws, f'A{r}', lab, border=True)
        for c in 'BCD':
            x.input(ws, f'{c}{r}', answer=f'={c}{par}-$B$6*{c}{src}')
    x.text(ws, 'A38', 'New z (hidden 1, hidden 2)', border=True)
    x.formula(ws, 'B38', '==B34*$B$3+C34*$B$4+D34'.replace('==', '='))
    x.formula(ws, 'C38', '=B35*$B$3+C35*$B$4+D35')
    x.text(ws, 'A39', 'New a (hidden 1, hidden 2)', border=True)
    x.formula(ws, 'B39', '=1/(1+EXP(-B38))')
    x.formula(ws, 'C39', '=1/(1+EXP(-C38))')
    x.text(ws, 'A40', 'New prediction y-hat', border=True)
    x.formula(ws, 'B40', '=B36*B39+C36*C39+D36')
    x.text(ws, 'A41', 'Loss after one update', bold=True)
    x.input(ws, 'B41', answer='=0.5*(B40-B5)^2')

    x.band(ws, 43, 'Step 4: check one gradient with a finite difference', 4)
    x.text(ws, 'A44', 'h (the nudge)', bold=True)
    x.text(ws, 'B44', 0.00001, border=True)

    def loss_with(dw):
        h1 = sig(f'($B$9{dw})*$B$3+$C$9*$B$4+$D$9')
        h2 = sig('$B$10*$B$3+$C$10*$B$4+$D$10')
        return f'=0.5*(($B$13*{h1}+$C$13*{h2}+$D$13)-$B$5)^2'
    x.text(ws, 'A45', 'Loss with the first weight of W1 row 1 plus h', border=True)
    x.formula(ws, 'B45', loss_with('+$B$44'))
    x.text(ws, 'A46', 'Loss with that weight minus h', border=True)
    x.formula(ws, 'B46', loss_with('-$B$44'))
    x.text(ws, 'A47', 'Finite difference (L plus - L minus) / (2h)', bold=True)
    x.input(ws, 'B47', answer='=(B45-B46)/(2*B44)')
    x.text(ws, 'A48', 'Backpropagation gradient of that weight', bold=True)
    x.formula(ws, 'B48', '=B28')
    x.text(ws, 'A49', 'Difference', bold=True)
    x.formula(ws, 'B49', '=ABS(B47-B48)')
    ws['B49'].number_format = '0.0E+00'

    t = x.sheet('Train', {'A': 6, **{c: 11 for c in 'BCDEFGHIJ'}, **{c: 12 for c in 'KLMNOPQRS'}})
    x.band(t, 1, 'Training: one row per step. Step 0 is the starting network; step 1 is your update from the Network sheet; the rows below are given.', 19)
    x.text(t, 'A3', 'eta', bold=True)
    x.formula(t, 'B3', '=Network!B6')
    heads = ['Step', 'W(1)_11', 'W(1)_12', 'W(1)_21', 'W(1)_22', 'b(1)_1', 'b(1)_2', 'W(2)_1', 'W(2)_2', 'b(2)', 'z(1)_1', 'z(1)_2', 'a(1)_1', 'a(1)_2', 'y-hat', 'Loss', 'delta(2)', 'delta(1)_1', 'delta(1)_2']
    for j, h in enumerate(heads):
        x.text(t, f'{X.get_column_letter(j + 1) if hasattr(X, "get_column_letter") else "ABCDEFGHIJKLMNOPQRS"[j]}5', h, bold=True, border=True)
    first = 6
    last = first + 50
    for k in range(51):
        r = first + k
        x.text(t, f'A{r}', k, border=True)
        if k == 0:
            for c, src in zip('BCDEFGHIJ', ['B9', 'C9', 'B10', 'C10', 'D9', 'D10', 'B13', 'C13', 'D13']):
                x.formula(t, f'{c}{r}', f'=Network!{src}')
        elif k == 1:     # step 1 is your own update from the Network sheet, so the rows below build on your work
            for c, src in zip('BCDEFGHIJ', ['B34', 'C34', 'B35', 'C35', 'D34', 'D35', 'B36', 'C36', 'D36']):
                x.formula(t, f'{c}{r}', f'=Network!{src}')
        else:
            p = r - 1
            x.formula(t, f'B{r}', f'=B{p}-$B$3*R{p}*Network!$B$3')
            x.formula(t, f'C{r}', f'=C{p}-$B$3*R{p}*Network!$B$4')
            x.formula(t, f'D{r}', f'=D{p}-$B$3*S{p}*Network!$B$3')
            x.formula(t, f'E{r}', f'=E{p}-$B$3*S{p}*Network!$B$4')
            x.formula(t, f'F{r}', f'=F{p}-$B$3*R{p}')
            x.formula(t, f'G{r}', f'=G{p}-$B$3*S{p}')
            x.formula(t, f'H{r}', f'=H{p}-$B$3*Q{p}*M{p}')
            x.formula(t, f'I{r}', f'=I{p}-$B$3*Q{p}*N{p}')
            x.formula(t, f'J{r}', f'=J{p}-$B$3*Q{p}')
        x.formula(t, f'K{r}', f'=B{r}*Network!$B$3+C{r}*Network!$B$4+F{r}')
        x.formula(t, f'L{r}', f'=D{r}*Network!$B$3+E{r}*Network!$B$4+G{r}')
        x.formula(t, f'M{r}', f'=1/(1+EXP(-K{r}))')
        x.formula(t, f'N{r}', f'=1/(1+EXP(-L{r}))')
        x.formula(t, f'O{r}', f'=H{r}*M{r}+I{r}*N{r}+J{r}')
        x.formula(t, f'P{r}', f'=0.5*(O{r}-Network!$B$5)^2')
        x.formula(t, f'Q{r}', f'=O{r}-Network!$B$5')
        x.formula(t, f'R{r}', f'=H{r}*Q{r}*M{r}*(1-M{r})')
        x.formula(t, f'S{r}', f'=I{r}*Q{r}*N{r}*(1-N{r})')
    t.freeze_panes = 'B6'
    ch = LineChart()
    ch.title = 'Loss against training step (log scale)'
    ch.y_axis.title = 'loss (log scale)'
    ch.y_axis.scaling.logBase = 10
    ch.x_axis.title = 'step'
    ch.height, ch.width = 8, 14
    ch.add_data(Reference(t, min_col=16, min_row=5, max_row=26), titles_from_data=True)
    ch.set_categories(Reference(t, min_col=1, min_row=6, max_row=26))
    t.add_chart(ch, 'U5')
    x.text(t, 'U22', 'The chart shows steps 0 to 20 on a log scale: each gridline is ten times smaller than the one above.', italic=True, color=X.GREY)

    L50 = None
    x.check('z(1) of hidden unit 1', '=Network!B17', float(s1['z1'][0]), 0.001)
    x.check('z(1) of hidden unit 2', '=Network!B18', float(s1['z1'][1]), 0.001)
    x.check('a(1) of hidden unit 1', '=Network!C17', float(s1['a1'][0]), 0.001)
    x.check('a(1) of hidden unit 2', '=Network!C18', float(s1['a1'][1]), 0.001)
    x.check('Prediction y-hat', '=Network!B19', float(s1['yh']), 0.001)
    x.check('Loss L', '=Network!B20', float(s1['L']), 0.001)
    x.check('delta(2)', '=Network!B23', float(s1['d2']), 0.001)
    x.check('delta(1)_1', '=Network!B24', float(s1['d1'][0]), 0.001)
    x.check('delta(1)_2', '=Network!B25', float(s1['d1'][1]), 0.001)
    x.check('Gradient of W(1) row 1, input 2', '=Network!C28', float(s1['gW1'][0][1]), 0.001)
    x.check('Gradient of W(1) row 2, input 1', '=Network!B29', float(s1['gW1'][1][0]), 0.001)
    x.check('Gradient of W(2), hidden 1', '=Network!B30', float(s1['gW2'][0][0]), 0.001)
    x.check('New W(1) row 1, input 1', '=Network!B34', float(n['new1'][0][0][0]), 0.001)
    x.check('New bias of the output unit', '=Network!D36', float(n['new1'][3][0]), 0.001)
    x.check('Loss after one update', '=Network!B41', float(s2['L']), 0.0001)
    x.check('Finite difference of the first weight', '=Network!B47', float(n['fd_W1_00']), 0.0001)
    x.check('Finite difference agrees with backpropagation (difference below 1e-7)', '=IF(ISNUMBER(Network!B47),Network!B49,1)', 0.0, 1e-7)
    x.check('Train sheet: loss after 2 steps', '=Train!P8', float(s3['L']), 0.00002)
    x.check('Train sheet: loss after 3 steps (shown in millionths)', '=Train!P9*1000000', _loss_after(n, 3) * 1e6, 0.001)
    x.check('Train sheet: loss after 50 steps is almost zero', '=Train!P56', 0.0, 1e-6)
    return x
