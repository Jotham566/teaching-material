"""Session 9 lab (spreadsheet): chain rule slopes, forward and backward values on the tiny graph, the Jacobian by formula and by nudging, J transposed times a gradient."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'kit'))
from xl import XL  # noqa: E402

X = [1, 2, 3, 4]
Y = [3, 5, 6, 9]


def build(solution: bool) -> XL:
    x = XL('Session 9: The chain rule and the Jacobian', 'Chain rule slopes, forward and backward values on a tiny graph, and the Jacobian', solution)
    x.start('You compute the slope of a function of a function with the chain rule, run the tiny graph of one delivery forwards and backwards, '
            'compute the Jacobian of a function with two inputs and two outputs, and check every answer by nudging the input. '
            'The numbers are the same as in the Python notebook. Gold cells are yours to fill.',
            ['Sheet Chain: fill the gold cells with the outer slope, the inner slope and their product. Predict the product first.',
             'Sheet Backward: fill the forward values and the backward values for one delivery, then the table for all four deliveries.',
             'Sheet Jacobian: write the four entries of the Jacobian, then J transposed times the gradient. Compare with the nudged values.',
             'Open the sheet Check. It must say All checks pass. Then save the file.'])

    # ---------------------------------------------------------------- Chain
    c = x.sheet('Chain', {'A': 34, 'B': 16, 'C': 16, 'D': 34})
    x.band(c, 1, 'Part A: the chain rule on y = (3x + 1) squared and y = e to the 2x', cols=4)
    x.text(c, 'A3', 'Example 1: y = (3x + 1) squared', bold=True)
    x.text(c, 'A4', 'The point x', bold=True)
    x.text(c, 'B4', 2, bold=True, border=True)
    x.text(c, 'A5', 'Inner value u = 3x + 1')
    x.formula(c, 'B5', '=3*B4+1')
    x.text(c, 'A6', 'Outer value y = u squared')
    x.formula(c, 'B6', '=B5^2')
    x.text(c, 'A7', 'Outer slope dy/du = 2u', bold=True)
    x.input(c, 'B7', answer='=2*B5')
    x.text(c, 'A8', 'Inner slope du/dx', bold=True)
    x.input(c, 'B8', answer=3)
    x.text(c, 'A9', 'Chain rule slope dy/dx', bold=True)
    x.input(c, 'B9', answer='=B7*B8')
    x.text(c, 'A10', 'Step h for the nudge')
    x.text(c, 'B10', 0.00001, border=True, bold=True)
    x.text(c, 'A11', 'Nudged slope (central difference)', bold=True)
    x.input(c, 'B11', answer='=((3*(B4+B10)+1)^2-(3*(B4-B10)+1)^2)/(2*B10)')
    c['B11'].number_format = '0.0000'
    x.text(c, 'C9', 'outer slope times inner slope', italic=True, color='666666')
    x.text(c, 'C11', 'it should match B9', italic=True, color='666666')

    x.text(c, 'A13', 'Example 2: y = e to the 2x', bold=True)
    x.text(c, 'A14', 'The point x', bold=True)
    x.text(c, 'B14', 1, bold=True, border=True)
    x.text(c, 'A15', 'Inner value u = 2x')
    x.formula(c, 'B15', '=2*B14')
    x.text(c, 'A16', 'Outer slope (e to the u)', bold=True)
    x.input(c, 'B16', answer='=EXP(B15)')
    x.text(c, 'A17', 'Inner slope du/dx', bold=True)
    x.input(c, 'B17', answer=2)
    x.text(c, 'A18', 'Chain rule slope dy/dx', bold=True)
    x.input(c, 'B18', answer='=B16*B17')
    x.text(c, 'A19', 'Nudged slope (central difference)', bold=True)
    x.input(c, 'B19', answer='=(EXP(2*(B14+B10))-EXP(2*(B14-B10)))/(2*B10)')
    for r in (16, 18, 19):
        c[f'B{r}'].number_format = '0.000'
    x.text(c, 'A21', 'READ: if you see 14 in B9, which slope did you forget? CHANGE one thing: set the inner function to 5x by editing B8 and the formulas for u. Predict first.', italic=True, color='666666')
    x.check('Outer slope at u = 7', '=Chain!B7', 14)
    x.check('Chain rule slope at x = 2', '=Chain!B9', 42)
    x.check('Nudged slope agrees with 42', '=IF(ISNUMBER(Chain!B11),Chain!B11,99)', 42, tol=0.001)
    x.check('Chain rule slope of e to the 2x at x = 1', '=Chain!B18', 14.778, tol=0.001)
    x.check('Nudged slope of e to the 2x agrees', '=IF(ISNUMBER(Chain!B19),Chain!B19,99)', 14.778, tol=0.001)

    # ---------------------------------------------------------------- Backward
    b = x.sheet('Backward', {'A': 30, 'B': 14, 'C': 16, 'D': 18, 'E': 22, 'F': 24})
    x.band(b, 1, 'Part B: forward and backward values on the tiny graph, w to p to L', cols=6)
    x.text(b, 'A3', 'Parameter w', bold=True)
    x.text(b, 'B3', 1, bold=True, border=True)
    x.text(b, 'A4', 'One delivery: distance x', bold=True)
    x.text(b, 'B4', 3, bold=True, border=True)
    x.text(b, 'A5', 'One delivery: fee y', bold=True)
    x.text(b, 'B5', 6, bold=True, border=True)
    x.text(b, 'A7', 'Forward pass', bold=True)
    x.text(b, 'A8', 'Prediction p = w x')
    x.input(b, 'B8', answer='=B3*B4')
    x.text(b, 'A9', 'Loss L = (p - y) squared')
    x.input(b, 'B9', answer='=(B8-B5)^2')
    x.text(b, 'A11', 'Backward pass', bold=True)
    x.text(b, 'A12', 'dL/dL (the start)')
    x.text(b, 'B12', 1, border=True)
    x.text(b, 'A13', 'Local slope dL/dp = 2 (p - y)')
    x.input(b, 'B13', answer='=2*(B8-B5)')
    x.text(b, 'A14', 'Local slope dp/dw = x')
    x.input(b, 'B14', answer='=B4')
    x.text(b, 'A15', 'dL/dw = dL/dp times dp/dw', bold=True)
    x.input(b, 'B15', answer='=B13*B14')
    x.text(b, 'A16', 'Nudged dL/dw (h below)', bold=True)
    x.text(b, 'C16', 'h', align='right')
    x.text(b, 'D16', 0.00001, border=True, bold=True)
    x.input(b, 'B16', answer='=(((B3+D16)*B4-B5)^2-((B3-D16)*B4-B5)^2)/(2*D16)')
    b['B16'].number_format = '0.000'

    x.text(b, 'A18', 'All four deliveries at the same w', bold=True)
    for j, hd in enumerate(['Distance x', 'Fee y', 'Error p - y', 'dL/dp = 2 e', 'dL/dw = x times dL/dp']):
        x.text(b, f'{"ABCDE"[j]}19', hd, bold=True, border=True, wrap=True)
    b.row_dimensions[19].height = 32
    for i in range(4):
        r = 20 + i
        x.text(b, f'A{r}', X[i], border=True)
        x.text(b, f'B{r}', Y[i], border=True)
        x.input(b, f'C{r}', answer=f'=$B$3*A{r}-B{r}')
        x.input(b, f'D{r}', answer=f'=2*C{r}')
        x.input(b, f'E{r}', answer=f'=A{r}*D{r}')
    x.text(b, 'A24', 'Mean of the four dL/dw values', bold=True)
    x.input(b, 'E24', answer='=AVERAGE(E20:E23)')
    x.text(b, 'A26', 'Session 8 slope of the loss in w at (1, 0)')
    x.text(b, 'E26', -18.5, border=True)
    x.text(b, 'A28', 'READ: row 3 is the same graph as the top block. CHANGE one thing: set w to 2 in B3 and predict the sign of the mean before you read E24 (answer -3.5).', italic=True, color='666666')
    x.check('Forward p', '=Backward!B8', 3)
    x.check('Forward L', '=Backward!B9', 9)
    x.check('Backward dL/dp', '=Backward!B13', -6)
    x.check('Backward dL/dw', '=Backward!B15', -18)
    x.check('Nudged dL/dw agrees', '=IF(ISNUMBER(Backward!B16),Backward!B16,99)', -18, tol=0.001)
    x.check('Row 3 backward value equals the top block', '=IF(ISNUMBER(Backward!E22),Backward!E22,99)', -18)
    x.check('Row 4 backward value', '=IF(ISNUMBER(Backward!E23),Backward!E23,99)', -40)
    x.check('Mean of the four backward values', '=IF(ISNUMBER(Backward!E24),Backward!E24,99)', -18.5)

    # ---------------------------------------------------------------- Jacobian
    j = x.sheet('Jacobian', {'A': 34, 'B': 14, 'C': 14, 'D': 40})
    x.band(j, 1, 'Part C: the Jacobian of u = x1 times x2 and v = x1 + x2 squared', cols=4)
    x.text(j, 'A3', 'Input x1', bold=True)
    x.text(j, 'B3', 2, bold=True, border=True)
    x.text(j, 'A4', 'Input x2', bold=True)
    x.text(j, 'B4', 3, bold=True, border=True)
    x.text(j, 'A5', 'Output u = x1 times x2')
    x.formula(j, 'B5', '=B3*B4')
    x.text(j, 'A6', 'Output v = x1 + x2 squared')
    x.formula(j, 'B6', '=B3+B4^2')
    x.text(j, 'A8', 'Jacobian by formula', bold=True)
    x.text(j, 'B8', 'column x1', bold=True, border=True, align='center')
    x.text(j, 'C8', 'column x2', bold=True, border=True, align='center')
    x.text(j, 'A9', 'row u')
    x.text(j, 'A10', 'row v')
    x.input(j, 'B9', answer='=B4')
    x.input(j, 'C9', answer='=B3')
    x.input(j, 'B10', answer=1)
    x.input(j, 'C10', answer='=2*B4')
    x.text(j, 'D9', 'Differentiate u with respect to x1, then x2', italic=True, color='666666')
    x.text(j, 'D10', 'Differentiate v with respect to x1, then x2', italic=True, color='666666')

    x.text(j, 'A12', 'Jacobian by nudging (h below)', bold=True)
    x.text(j, 'C12', 'h', align='right')
    x.text(j, 'D12', 0.00001, border=True, bold=True)
    x.text(j, 'A13', 'row u')
    x.text(j, 'A14', 'row v')
    x.input(j, 'B13', answer='=((B3+D12)*B4-(B3-D12)*B4)/(2*D12)')
    x.input(j, 'C13', answer='=(B3*(B4+D12)-B3*(B4-D12))/(2*D12)')
    x.input(j, 'B14', answer='=((B3+D12)+B4^2-((B3-D12)+B4^2))/(2*D12)')
    x.input(j, 'C14', answer='=(B3+(B4+D12)^2-(B3+(B4-D12)^2))/(2*D12)')
    for cell in ('B13', 'C13', 'B14', 'C14'):
        j[cell].number_format = '0.000'
    x.text(j, 'A15', 'Largest gap between the two Jacobians')
    x.formula(j, 'B15', '=MAX(ABS(B9-B13),ABS(C9-C13),ABS(B10-B14),ABS(C10-C14))')
    j['B15'].number_format = '0.000000'

    x.text(j, 'A17', 'Back to the inputs: the gradient of s = u times v', bold=True)
    x.text(j, 'A18', 'ds/du = v')
    x.formula(j, 'B18', '=B6')
    x.text(j, 'A19', 'ds/dv = u')
    x.formula(j, 'B19', '=B5')
    x.text(j, 'A20', 'ds/dx1 = J transposed, first row', bold=True)
    x.input(j, 'B20', answer='=B9*B18+B10*B19')
    x.text(j, 'D20', 'column 1 of J times (ds/du, ds/dv)', italic=True, color='666666')
    x.text(j, 'A21', 'ds/dx2 = J transposed, second row', bold=True)
    x.input(j, 'B21', answer='=C9*B18+C10*B19')
    x.text(j, 'D21', 'column 2 of J times (ds/du, ds/dv)', italic=True, color='666666')
    x.text(j, 'A22', 'Nudged ds/dx1 (check)')
    x.input(j, 'B22', answer='=(((B3+D12)*B4)*((B3+D12)+B4^2)-((B3-D12)*B4)*((B3-D12)+B4^2))/(2*D12)')
    x.text(j, 'A23', 'Nudged ds/dx2 (check)')
    x.input(j, 'B23', answer='=((B3*(B4+D12))*(B3+(B4+D12)^2)-(B3*(B4-D12))*(B3+(B4-D12)^2))/(2*D12)')
    for cell in ('B22', 'B23'):
        j[cell].number_format = '0.000'
    x.text(j, 'A25', 'READ: which entry is largest, and which input does that output depend on most? CHANGE one thing: set x1 = 1 and x2 = 2 in B3:B4. Predict the Jacobian (answer rows (2, 1) and (1, 4)) and the gradient of s (answer 12 and 13).', italic=True, color='666666', wrap=True)
    j.row_dimensions[25].height = 48
    x.check('du/dx1', '=Jacobian!B9', 3)
    x.check('du/dx2', '=Jacobian!C9', 2)
    x.check('dv/dx1', '=Jacobian!B10', 1)
    x.check('dv/dx2', '=Jacobian!C10', 6)
    x.check('Nudged Jacobian agrees with the formula', '=IF(AND(ISNUMBER(Jacobian!B13),ISNUMBER(Jacobian!C14)),Jacobian!B15,99)', 0, tol=0.001)
    x.check('Gradient of s in x1', '=Jacobian!B20', 39)
    x.check('Gradient of s in x2', '=Jacobian!B21', 58)
    x.check('Nudged slope of s in x1', '=IF(ISNUMBER(Jacobian!B22),Jacobian!B22,99)', 39, tol=0.001)
    x.check('Nudged slope of s in x2', '=IF(ISNUMBER(Jacobian!B23),Jacobian!B23,99)', 58, tol=0.001)
    return x
