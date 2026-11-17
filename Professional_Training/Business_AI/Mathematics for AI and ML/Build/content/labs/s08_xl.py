"""Session 8 lab (spreadsheet): the loss of a line fit, its gradient by formula and by nudges, a grid of losses and the steepest direction."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'kit'))
from xl import XL  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402

X = [1, 2, 3, 4]
Y = [3, 5, 6, 9]
WV = [i * 0.5 for i in range(8)]          # 0 to 3.5
BV = [-1 + i * 0.5 for i in range(9)]     # -1 to 3


def build(solution: bool) -> XL:
    x = XL('Session 8: Partial derivatives and the gradient', 'The loss of a line fit with two parameters, its gradient, and a grid of losses', solution)
    x.start('You compute the loss of the line y-hat = b + w x, its gradient (one partial derivative for each parameter), check the gradient by nudging one parameter at a time, '
            'and build a grid of losses, which is the contour map written as numbers. The numbers are the same as in the Python notebook. Gold cells are yours to fill.',
            ['Sheet Gradient: fill the gold cells for the loss, the errors, the gradient and the nudged estimates. Predict the signs of the two partial derivatives first.',
             'Sheet Grid: write one loss formula in the first gold cell and copy it across the whole grid. Find the smallest value.',
             'Back on Gradient: fill the length of the gradient and the steepest downhill direction as a unit vector (two cells).',
             'Open the sheet Check. It must say All checks pass. Then save the file.'])

    # ---------------------------------------------------------------- Gradient
    g = x.sheet('Gradient', {'A': 26, 'B': 16, 'C': 16, 'D': 18, 'E': 18, 'F': 16})
    x.band(g, 1, 'Part A: loss and gradient of the line y-hat = b + w x', cols=6)
    x.text(g, 'A3', 'Distance x (km)', bold=True, border=True)
    x.text(g, 'B3', 'Fee y (thousand UGX)', bold=True, border=True, wrap=True)
    g.row_dimensions[3].height = 32
    for i in range(4):
        x.text(g, f'A{4 + i}', X[i], border=True)
        x.text(g, f'B{4 + i}', Y[i], border=True)
    x.text(g, 'A9', 'Number of rows n', bold=True)
    x.formula(g, 'B9', '=COUNT(A4:A7)')
    x.text(g, 'A10', 'Step h for the nudges', bold=True)
    x.text(g, 'B10', 0.0001, bold=True, border=True)

    x.text(g, 'A12', 'Two points to compare', bold=True)
    x.text(g, 'B12', 'Start', bold=True, border=True, align='center')
    x.text(g, 'C12', 'Best line', bold=True, border=True, align='center')
    x.text(g, 'A13', 'Slope w')
    x.text(g, 'B13', 1, border=True, bold=True)
    x.text(g, 'C13', 1.9, border=True, bold=True)
    x.text(g, 'A14', 'Intercept b')
    x.text(g, 'B14', 0, border=True, bold=True)
    x.text(g, 'C14', 1, border=True, bold=True)
    x.text(g, 'A15', 'Loss L(w, b)', bold=True)
    x.text(g, 'A16', 'Gradient ∂L/∂w', bold=True)
    x.text(g, 'A17', 'Gradient ∂L/∂b', bold=True)
    x.text(g, 'A18', 'Nudged estimate of ∂L/∂w')
    x.text(g, 'A19', 'Nudged estimate of ∂L/∂b')
    for c in 'BC':
        x.input(g, f'{c}15', answer=f'=SUMPRODUCT(({c}13*$A$4:$A$7+{c}14-$B$4:$B$7)^2)/$B$9')
        x.input(g, f'{c}16', answer=f'=2/$B$9*SUMPRODUCT($A$4:$A$7,{c}13*$A$4:$A$7+{c}14-$B$4:$B$7)')
        x.input(g, f'{c}17', answer=f'=2/$B$9*SUMPRODUCT({c}13*$A$4:$A$7+{c}14-$B$4:$B$7)')
        x.input(g, f'{c}18', answer=(f'=(SUMPRODUCT((({c}13+$B$10)*$A$4:$A$7+{c}14-$B$4:$B$7)^2)-SUMPRODUCT((({c}13-$B$10)*$A$4:$A$7+{c}14-$B$4:$B$7)^2))/(2*$B$10*$B$9)'))
        x.input(g, f'{c}19', answer=(f'=(SUMPRODUCT(({c}13*$A$4:$A$7+{c}14+$B$10-$B$4:$B$7)^2)-SUMPRODUCT(({c}13*$A$4:$A$7+{c}14-$B$10-$B$4:$B$7)^2))/(2*$B$10*$B$9)'))
        for r in range(15, 20):
            g[f'{c}{r}'].number_format = '0.000'
    x.text(g, 'D15', 'mean of the squared errors', italic=True, color='666666')
    x.text(g, 'D16', '2 / n times the sum of x times error', italic=True, color='666666')
    x.text(g, 'D17', '2 / n times the sum of the errors', italic=True, color='666666')
    x.text(g, 'D18', 'nudge w only, b held fixed', italic=True, color='666666')
    x.text(g, 'D19', 'nudge b only, w held fixed', italic=True, color='666666')

    x.text(g, 'A21', 'Errors at the start (prediction minus actual)', bold=True)
    x.text(g, 'A22', 'Row', bold=True, border=True)
    x.text(g, 'B22', 'Error e', bold=True, border=True)
    x.text(g, 'C22', 'x times e', bold=True, border=True)
    for i in range(4):
        r = 23 + i
        x.text(g, f'A{r}', i + 1, border=True)
        x.input(g, f'B{r}', answer=f'=$B$13*A{4 + i}+$B$14-B{4 + i}')
        x.input(g, f'C{r}', answer=f'=A{4 + i}*B{r}')
    x.text(g, 'A27', 'Sum', bold=True)
    x.formula(g, 'B27', '=SUM(B23:B26)')
    x.formula(g, 'C27', '=SUM(C23:C26)')

    x.text(g, 'A29', 'Length of the gradient at the start', bold=True)
    x.input(g, 'B29', answer='=SQRT(B16^2+B17^2)')
    x.text(g, 'C29', 'the steepness: square root of the two entries squared', italic=True, color='666666')
    x.text(g, 'A30', 'Steepest way down, unit vector: w entry', bold=True, wrap=True)
    x.input(g, 'B30', answer='=-B16/B29')
    x.text(g, 'C30', 'minus the gradient, divided by its length', italic=True, color='666666')
    x.text(g, 'A31', 'Steepest way down, unit vector: b entry', bold=True, wrap=True)
    x.input(g, 'B31', answer='=-B17/B29')
    x.text(g, 'C31', 'the two entries together have length 1', italic=True, color='666666')
    g['B29'].number_format = '0.00'
    for c in ('B30', 'B31'):
        g[c].number_format = '0.000'
    x.text(g, 'A33', 'PREDICT first: both entries at the start are negative. READ: which entry is larger, and what does that say about moving w versus b?', italic=True, color='666666')
    x.text(g, 'A34', 'CHANGE one thing: set the start to w = 3 and b = 0 in B13:B14. Predict the signs of B30 and B31 first, then read them. Set it back to 1 for the Check sheet.', italic=True, color='666666')

    x.check('Loss at the start (1, 0)', '=Gradient!B15', 11.75)
    x.check('Loss at the best line (1.9, 1)', '=Gradient!C15', 0.175, tol=0.001)
    x.check('∂L/∂w at the start', '=Gradient!B16', -18.5)
    x.check('∂L/∂b at the start', '=Gradient!B17', -6.5)
    x.check('Gradient at the best line is zero', '=IF(ISNUMBER(Gradient!C16),ABS(Gradient!C16)+ABS(Gradient!C17),99)', 0, tol=0.001)
    x.check('Nudged estimate of ∂L/∂w agrees', '=IF(ISNUMBER(Gradient!B18),Gradient!B18,99)', -18.5, tol=0.001)
    x.check('Nudged estimate of ∂L/∂b agrees', '=IF(ISNUMBER(Gradient!B19),Gradient!B19,99)', -6.5, tol=0.001)
    x.check('Sum of the errors at the start', '=Gradient!B27', -13)
    x.check('Length of the gradient', '=Gradient!B29', 19.61, tol=0.01)
    x.check('Steepest downhill unit vector: w entry', '=Gradient!B30', 0.943, tol=0.002)
    x.check('Steepest downhill unit vector: b entry', '=Gradient!B31', 0.331, tol=0.002)

    # ---------------------------------------------------------------- Grid
    wg = x.sheet('Grid', {'A': 12})
    for j in range(len(WV)):
        wg.column_dimensions[get_column_letter(2 + j)].width = 10
    x.band(wg, 1, 'Part B: a grid of losses L(w, b), the contour map written as numbers', cols=9)
    x.text(wg, 'A3', 'b \\ w', bold=True, border=True)
    for j, w in enumerate(WV):
        x.text(wg, f'{get_column_letter(2 + j)}3', w, bold=True, border=True)
    for i, b in enumerate(BV):
        r = 4 + i
        x.text(wg, f'A{r}', b, bold=True, border=True)
        for j in range(len(WV)):
            c = get_column_letter(2 + j)
            x.input(wg, f'{c}{r}', answer=f'=SUMPRODUCT(({c}$3*Gradient!$A$4:$A$7+$A{r}-Gradient!$B$4:$B$7)^2)/Gradient!$B$9')
            wg[f'{c}{r}'].number_format = '0.00'
    x.text(wg, 'A14', 'Smallest loss on the grid', bold=True)
    x.input(wg, 'D14', answer='=MIN(B4:I12)')
    x.text(wg, 'A15', 'Loss at w = 1, b = 0 (read from the grid)', bold=True)
    x.input(wg, 'D15', answer='=D6')
    x.text(wg, 'A17', 'Write ONE formula in B4: the loss for the w at the top of its column and the b at the left of its row. Put $ on the row of w (row 3) and on the column of b (column A), then copy it across B4:I12.', italic=True, color='666666')
    x.text(wg, 'A18', 'READ: where is the smallest value, and is it the true minimum of the loss? CHANGE one thing: change the grid steps to 0.1 around the smallest cell and predict first whether the minimum gets smaller.', italic=True, color='666666')
    x.check('Smallest loss on the grid', '=Grid!D14', 0.25)
    x.check('Grid loss at w = 1, b = 0', '=Grid!D15', 11.75)
    x.check('Grid loss at w = 2, b = 1', '=Grid!F8', 0.25)
    x.check('Grid loss at w = 2, b = 0.5 (the tie)', '=Grid!F7', 0.25)
    return x
