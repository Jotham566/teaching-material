"""Session 5 spreadsheet lab: the same numbers as the notebook. Eigenvalues by the characteristic-equation formula and power iteration in rows of cells (no eigenvalue function exists in Excel or Google Sheets)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[2] / 'kit'
sys.path.insert(0, str(HERE))
import xl  # noqa: E402
import diagrams_math_b as MB  # noqa: E402


def build(solution: bool):
    d = MB.d5()
    C, lam, v1 = d['C'], d['lam'], d['v1']
    x = xl.XL('Session 5: Eigenvalues and eigenvectors', 'Mathematics for AI and Machine Learning | KLAi Professional Learning', solution=solution)
    x.start('You test an eigenvector, find eigenvalues from the trace and the determinant, build the covariance matrix of eight students\' marks, find the top direction of the data, '
            'and run power iteration in rows of cells. Neither Excel nor Google Sheets has an eigenvalue function, so you build the formulas yourself. '
            'The marks are illustrative (made-up numbers to show the arithmetic). The numbers are the same as in the Python notebook.',
            ['Open the sheet called Work. Part 1: multiply the matrix A by the arrow (1, 1) and find the stretch factor. Predict first.',
             'Part 2: the trace T and the determinant D of A, then the two eigenvalues from the quadratic formula.',
             'Part 3: centre the eight maths and physics marks and build the covariance matrix.',
             'Part 4: the eigenvalues of the covariance matrix, the top eigenvector (scaled to length 1) and the share of the variance.',
             'Part 5: power iteration. Fill the gold guess cells so that each row divides the previous product by its largest entry. The last row is the sixth multiplication (k = 5).',
             'Part 6: change one thing, replace physics by 100 minus physics.',
             'For a matrix result, select the whole gold block, type the formula, then press Ctrl+Shift+Enter in Excel or Enter in Google Sheets.'])
    ws = x.sheet('Work', {'A': 50, 'B': 13, 'C': 13, 'D': 13, 'E': 13, 'F': 13, 'G': 4})

    # ---- Part 1
    x.band(ws, 1, 'Part 1: does A keep the direction of (1, 1)?', cols=6)
    x.text(ws, 'A3', 'A (rows 3 and 4)  and the arrow v (column E)', bold=True)
    for r, row in enumerate(d['A']):
        for c, v in enumerate(row):
            ws[f'{"BC"[c]}{3 + r}'] = float(v)
            ws[f'{"BC"[c]}{3 + r}'].border = xl.BOX
    x.text(ws, 'D3', 'v =', align='right')
    for r, v in enumerate((1.0, 1.0)):
        ws[f'E{3 + r}'] = v
        ws[f'E{3 + r}'].border = xl.BOX
    x.text(ws, 'A6', 'Av (select B6:B7)')
    x.array(ws, 'B6:B7', '=MMULT(B3:C4,E3:E4)', gold=True)
    x.text(ws, 'A8', 'Stretch factor: first entry of Av divided by first entry of v')
    x.input(ws, 'B8', answer='=B6/E3')

    # ---- Part 2
    x.band(ws, 10, 'Part 2: eigenvalues of A from the trace and the determinant', cols=6)
    x.text(ws, 'A11', 'Trace T = a₁₁ + a₂₂')
    x.input(ws, 'B11', answer='=B3+C4')
    x.text(ws, 'A12', 'Determinant D = a₁₁a₂₂ − a₁₂a₂₁')
    x.input(ws, 'B12', answer='=B3*C4-C3*B4')
    x.text(ws, 'A13', 'Square root of T² − 4D (given)')
    x.formula(ws, 'B13', '=SQRT(B11^2-4*B12)')
    x.text(ws, 'A14', 'Larger eigenvalue (T + root) / 2')
    x.input(ws, 'B14', answer='=(B11+B13)/2')
    x.text(ws, 'A15', 'Smaller eigenvalue (T - root) / 2')
    x.input(ws, 'B15', answer='=(B11-B13)/2')
    x.text(ws, 'A16', 'Read: do the eigenvalues add up to T and multiply to D?', italic=True)

    # ---- Part 3
    x.band(ws, 18, 'Part 3: eight students, centred, and the covariance matrix', cols=6)
    for j, h in enumerate(['Student', 'Maths mark', 'Physics mark', 'Centred maths', 'Centred physics', '100 − physics']):
        x.text(ws, f'{"ABCDEF"[j]}19', h, bold=True, border=True, wrap=True)
    for i in range(d['n']):
        r = 20 + i
        ws[f'A{r}'] = i + 1
        ws[f'B{r}'] = float(d['maths'][i])
        ws[f'C{r}'] = float(d['phys'][i])
        for c in 'ABC':
            ws[f'{c}{r}'].border = xl.BOX
        x.input(ws, f'D{r}', answer=f'=B{r}-B$28')
        x.input(ws, f'E{r}', answer=f'=C{r}-C$28')
        x.formula(ws, f'F{r}', f'=100-C{r}')
    x.text(ws, 'A28', 'Mean of each column (given)', bold=True)
    x.formula(ws, 'B28', '=AVERAGE(B20:B27)')
    x.formula(ws, 'C28', '=AVERAGE(C20:C27)')
    x.text(ws, 'A30', 'Covariance matrix C is the block B31:C32. Divide by n − 1 (n is the number of students).', bold=True)
    x.text(ws, 'A31', 'Row 1 of C: variance of maths in B31, covariance in C31', wrap=True)
    ws.row_dimensions[31].height = 30
    x.input(ws, 'B31', answer='=SUMPRODUCT(D20:D27,D20:D27)/(COUNT(D20:D27)-1)')
    x.input(ws, 'C31', answer='=SUMPRODUCT(D20:D27,E20:E27)/(COUNT(D20:D27)-1)')
    x.text(ws, 'A32', 'Row 2 of C: covariance in B32 (the same as C31), variance of physics in C32', wrap=True)
    ws.row_dimensions[32].height = 30
    x.input(ws, 'C32', answer='=SUMPRODUCT(E20:E27,E20:E27)/(COUNT(E20:E27)-1)')
    x.input(ws, 'B32', answer='=C31')
    x.text(ws, 'A34', 'Read: C is B31:C32. Is it symmetric? Check with VAR.S and COVARIANCE.S: they give the same numbers.', italic=True, wrap=True)

    # ---- Part 4
    x.band(ws, 36, 'Part 4: eigenvalues, top eigenvector and share of variance of C', cols=6)
    x.text(ws, 'A37', 'Trace of C (given)')
    x.formula(ws, 'B37', '=B31+C32')
    x.text(ws, 'A38', 'Determinant of C (given)')
    x.formula(ws, 'B38', '=B31*C32-C31*B32')
    x.text(ws, 'A39', 'Square root of T² − 4D (given)')
    x.formula(ws, 'B39', '=SQRT(B37^2-4*B38)')
    x.text(ws, 'A40', 'Larger eigenvalue of C')
    x.input(ws, 'B40', answer='=(B37+B39)/2')
    x.text(ws, 'A41', 'Smaller eigenvalue of C')
    x.input(ws, 'B41', answer='=(B37-B39)/2')
    x.text(ws, 'A42', 'Top eigenvector before scaling: (C31, larger eigenvalue − B31) (given)')
    x.formula(ws, 'B42', '=C31')
    x.formula(ws, 'C42', '=B40-B31')
    x.text(ws, 'A43', 'Length of that vector (given)')
    x.formula(ws, 'B43', '=SQRT(B42^2+C42^2)')
    x.text(ws, 'A44', 'Top eigenvector at length 1: first entry')
    x.input(ws, 'B44', answer='=B42/B43')
    x.text(ws, 'A45', 'Top eigenvector at length 1: second entry')
    x.input(ws, 'B45', answer='=C42/B43')
    x.text(ws, 'A46', 'Share of the total variance on direction 1')
    x.input(ws, 'B46', answer='=B40/(B40+B41)')

    # ---- Part 5
    x.band(ws, 48, 'Part 5: power iteration on C, start at v = (0, 1)', cols=6)
    for j, h in enumerate(['Step k', 'Guess, first entry', 'Guess, second entry', 'C × guess, first entry', 'C × guess, second entry', 'Largest entry']):
        x.text(ws, f'{"ABCDEF"[j]}49', h, bold=True, border=True, wrap=True)
    x.text(ws, 'A56', 'Gold cells: each guess is the previous C × guess divided by the previous largest entry.', italic=True)
    for k in range(6):
        r = 50 + k
        ws[f'A{r}'] = k
        ws[f'A{r}'].border = xl.BOX
        if k == 0:
            ws[f'B{r}'] = 0.0
            ws[f'C{r}'] = 1.0
            ws[f'B{r}'].border = xl.BOX
            ws[f'C{r}'].border = xl.BOX
        else:
            x.input(ws, f'B{r}', answer=f'=D{r - 1}/F{r - 1}')
            x.input(ws, f'C{r}', answer=f'=E{r - 1}/F{r - 1}')
        x.formula(ws, f'D{r}', f'=$B$31*B{r}+$C$31*C{r}')
        x.formula(ws, f'E{r}', f'=$B$32*B{r}+$C$32*C{r}')
        x.formula(ws, f'F{r}', f'=MAX(ABS(D{r}),ABS(E{r}))')
    x.text(ws, 'A57', 'Guess after 6 steps: first entry')
    x.input(ws, 'B57', answer='=D55/F55')
    x.text(ws, 'A58', 'Guess after 6 steps: second entry')
    x.input(ws, 'B58', answer='=E55/F55')

    # ---- Part 6
    x.band(ws, 60, 'Part 6: change one thing, physics replaced by 100 minus physics (column F)', cols=6)
    x.text(ws, 'A61', 'New covariance of maths and the new column (COVARIANCE.S)')
    x.input(ws, 'B61', answer='=_xlfn.COVARIANCE.S(B20:B27,F20:F27)')
    x.text(ws, 'A62', 'Larger eigenvalue with the same two variances and the new covariance')
    x.input(ws, 'B62', answer='=((B31+C32)+SQRT((B31+C32)^2-4*(B31*C32-B61^2)))/2')
    x.text(ws, 'A63', 'Read: the covariance changed sign. Did the larger eigenvalue change?', italic=True)

    x.check('A v, first entry is 3', '=Work!B6', 3.0)
    x.check('A v, second entry is 3', '=Work!B7', 3.0)
    x.check('Stretch factor is 3', '=Work!B8', 3.0)
    x.check('Trace of A is 4', '=Work!B11', 4.0)
    x.check('Determinant of A is 3', '=Work!B12', 3.0)
    x.check('Larger eigenvalue of A is 3', '=Work!B14', 3.0)
    x.check('Smaller eigenvalue of A is 1', '=Work!B15', 1.0)
    x.check('First centred maths mark', '=Work!D20', float(d['ca'][0]))
    x.check('Last centred physics mark', '=Work!E27', float(d['cb'][-1]))
    x.check('Variance of maths is 66', '=Work!B31', float(C[0, 0]))
    x.check('Covariance of maths and physics is 48', '=Work!C31', float(C[0, 1]))
    x.check('Variance of physics is 38', '=Work!C32', float(C[1, 1]))
    x.check('Larger eigenvalue of C is 102', '=Work!B40', float(lam[0]), 0.001)
    x.check('Smaller eigenvalue of C is 2', '=Work!B41', float(lam[1]), 0.001)
    x.check('Top eigenvector, first entry 0.8', '=Work!B44', float(abs(v1[0])), 0.001)
    x.check('Top eigenvector, second entry 0.6', '=Work!B45', float(abs(v1[1])), 0.001)
    x.check('Share of the variance on direction 1', '=Work!B46', d['explained'], 0.001)
    x.check('Largest entry after 6 steps is about 102', '=Work!F55', float(d['pc'][-1][3]), 0.01)
    x.check('Guess after 6 steps, first entry 1', '=Work!B57', 1.0, 0.001)
    x.check('Guess after 6 steps, second entry 0.75', '=Work!B58', 0.75, 0.001)
    x.check('Covariance with 100 minus physics is -48', '=Work!B61', -48.0, 0.001)
    x.check('Larger eigenvalue stays 102', '=Work!B62', float(lam[0]), 0.001)
    return x
