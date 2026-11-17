"""Session 4 spreadsheet lab: the same numbers as the notebook. MDETERM, MINVERSE, MMULT, TRANSPOSE as array formulas."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[2] / 'kit'
sys.path.insert(0, str(HERE))
import xl  # noqa: E402
import diagrams_math_b as MB  # noqa: E402


def build(solution: bool):
    d = MB.d4()
    bi, wsl = float(d['w'][0]), float(d['w'][1])   # intercept b and slope w
    x = xl.XL('Session 4: Solving linear systems', 'Mathematics for AI and Machine Learning | KLAi Professional Learning', solution=solution)
    x.start('You solve a 2 by 2 system with the inverse, meet a matrix with determinant 0, and fit the line ŷ = b + w × spend to seven data points with the normal equation (XᵀX) w = Xᵀy, where the column w holds the intercept b and the slope w. '
            'The data are illustrative (made-up numbers to show the arithmetic). The numbers are the same as in the Python notebook.',
            ['Open the sheet called Work. Part 1: find the determinant, the inverse and the solution of the 2 by 2 system. Predict each answer first.',
             'Part 2: a singular matrix. Find its determinant. Spreadsheets have no rank function, so a determinant of 0 tells you the rank is below 2.',
             'Part 3: the seven data points with a column of ones. Compute XᵀX, Xᵀy, the inverse of XᵀX and then the intercept b and the slope w.',
             'Part 4: predictions, errors, the total squared error, then the root mean squared error (RMSE) built from it.',
             'Part 5: one data row only. Find the determinant of XᵀX.',
             'For a matrix result, select the whole gold block and type the formula. In older Excel, confirm with Ctrl+Shift+Enter. In Excel 365 and Google Sheets, Enter works. #SPILL! means the cells below are not empty.'])
    ws = x.sheet('Work', {'A': 46, 'B': 13, 'C': 13, 'D': 13, 'E': 13, 'F': 13, 'G': 4})

    x.band(ws, 1, 'Part 1: solve Ax = b with the inverse', cols=6)
    x.text(ws, 'A3', 'A (coefficients) and b (right-hand sides; later b is the intercept)', bold=True)
    for r, (row, bb) in enumerate(zip(d['A'], d['b'])):
        for c, v in enumerate(row):
            ws[f'{"BC"[c]}{3 + r}'] = float(v)
            ws[f'{"BC"[c]}{3 + r}'].border = xl.BOX
        ws[f'E{3 + r}'] = float(bb)
        ws[f'E{3 + r}'].border = xl.BOX
    x.text(ws, 'D3', 'b =', align='right')
    x.text(ws, 'A6', 'Determinant of A')
    x.input(ws, 'B6', answer='=MDETERM(B3:C4)')
    x.text(ws, 'A8', 'Inverse of A (select B8:C9)')
    x.array(ws, 'B8:C9', '=MINVERSE(B3:C4)', gold=True)
    x.text(ws, 'A11', 'Solution x₁, x₂ = inverse times b (select B11:B12)')
    x.array(ws, 'B11:B12', '=MMULT(B8:C9,E3:E4)', gold=True)

    x.band(ws, 14, 'Part 2: a singular matrix', cols=6)
    for r, row in enumerate(d['S']):
        for c, v in enumerate(row):
            ws[f'{"BC"[c]}{15 + r}'] = float(v)
            ws[f'{"BC"[c]}{15 + r}'].border = xl.BOX
    x.text(ws, 'A15', 'S (second row is twice the first)', bold=True)
    x.text(ws, 'A18', 'Determinant of S')
    x.input(ws, 'B18', answer='=MDETERM(B15:C16)')

    x.band(ws, 21, 'Part 3: the data and the normal equation', cols=6)
    for j, h in enumerate(['Month', 'Ones', 'Spend (UGX million)', 'Sales (UGX million)', 'Predicted sales', 'Error']):
        x.text(ws, f'{"ABCDEF"[j]}22', h, bold=True, border=True, wrap=True)
    for i in range(d['n']):
        r = 23 + i
        ws[f'A{r}'] = i + 1
        ws[f'B{r}'] = 1
        ws[f'C{r}'] = float(d['x'][i])
        ws[f'D{r}'] = float(d['y'][i])
        for c in 'ABCD':
            ws[f'{c}{r}'].border = xl.BOX
    x.text(ws, 'A31', 'XᵀX (select B31:C32). X is the block B23:C29')
    x.array(ws, 'B31:C32', '=MMULT(TRANSPOSE(B23:C29),B23:C29)', gold=True)
    x.text(ws, 'A34', 'Xᵀy (select B34:B35). y is the block D23:D29')
    x.array(ws, 'B34:B35', '=MMULT(TRANSPOSE(B23:C29),D23:D29)', gold=True)
    x.text(ws, 'A37', 'Inverse of XᵀX (select B37:C38)')
    x.array(ws, 'B37:C38', '=MINVERSE(B31:C32)', gold=True)
    x.text(ws, 'A40', 'Intercept b (B40) and slope w (B41), select B40:B41. They solve the normal equation')
    x.array(ws, 'B40:B41', '=MMULT(B37:C38,B34:B35)', gold=True)

    x.band(ws, 43, 'Part 4: predictions and errors', cols=6)
    x.text(ws, 'A44', 'Fill the gold cells in E23:E29 with the predicted sales ŷ = b + w × spend. The Error column (actual minus predicted) is given.', wrap=True)
    for i in range(d['n']):
        r = 23 + i
        x.input(ws, f'E{r}', answer=f'=$B$40+$B$41*C{r}')
        x.formula(ws, f'F{r}', f'=D{r}-E{r}')
    x.text(ws, 'A45', 'Total squared error (sum of the squared Error column)')
    x.input(ws, 'B45', answer='=SUMSQ(F23:F29)')
    x.text(ws, 'A46', 'RMSE: the square root of (total squared error in B45 ÷ n)')
    x.input(ws, 'B46', answer='=SQRT(B45/7)')
    x.text(ws, 'A47', 'Predicted sales at spend 7')
    x.input(ws, 'B47', answer='=B40+B41*7')

    x.band(ws, 48, 'Part 5: change one thing, only one data row', cols=6)
    x.text(ws, 'A49', 'One row: ones and spend 4', bold=True)
    ws['B49'] = 1
    ws['C49'] = 4
    for c in 'BC':
        ws[f'{c}49'].border = xl.BOX
    x.text(ws, 'A51', 'XᵀX for one row (select B51:C52)')
    x.array(ws, 'B51:C52', '=MMULT(TRANSPOSE(B49:C49),B49:C49)', gold=True)
    x.text(ws, 'A54', 'Determinant of that matrix')
    x.input(ws, 'B54', answer='=MDETERM(B51:C52)')
    x.text(ws, 'A56', 'Read: one equation and two unknowns. What does a determinant of 0 say about the best line?', italic=True, wrap=True)

    x.check('Determinant of A is -3', '=Work!B6', d['det'])
    x.check('Top-left entry of the inverse of A is 1/3', '=Work!B8', float(d['Ainv'][0, 0]))
    x.check('x₁ is 2', '=Work!B11', float(d['sol'][0]))
    x.check('x₂ is 1', '=Work!B12', float(d['sol'][1]))
    x.check('Determinant of the singular matrix is 0 (rank below 2)', '=Work!B18', 0, 1e-9)
    x.check('XᵀX, bottom-right entry (sum of spend squared)', '=Work!C32', float(d['XtX'][1, 1]))
    x.check('Xᵀy, second entry', '=Work!B35', float(d['Xty'][1]))
    x.check('Intercept b', '=Work!B40', bi)
    x.check('Slope w', '=Work!B41', wsl)
    x.check('First predicted sales value', '=Work!E23', float(d['pred'][0]))
    x.check('Total squared error is 8.28', '=Work!B45', d['sse'])
    x.check('RMSE of the line', '=Work!B46', d['rmse'])
    x.check('Predicted sales at spend 7', '=Work!B47', d['pred7'], 0.05)
    x.check('Determinant of XᵀX with one row is 0', '=Work!B54', 0, 1e-9)
    return x
