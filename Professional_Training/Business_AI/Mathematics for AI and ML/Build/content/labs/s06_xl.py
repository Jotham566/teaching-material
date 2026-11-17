"""Session 6 spreadsheet lab: the same numbers as the notebook. Neither Excel nor Google Sheets has an SVD function, so: A^T A and the characteristic-equation formula for the 2 by 2 matrix,
power iteration in cells for the first piece of the noisy image, and PCA of the eight marks with centring, covariance, eigenvector by formula and projection."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[2] / 'kit'
sys.path.insert(0, str(HERE))
import xl  # noqa: E402
import diagrams_math_b as MB  # noqa: E402

COLS = 'BCDEFGHI'
MVCOLS = 'JKLMNOPQ'


def build(solution: bool):
    d = MB.d6()
    p5 = MB.d5()
    lam = p5['lam']
    x = xl.XL('Session 6: SVD and PCA', 'Mathematics for AI and Machine Learning | KLAi Professional Learning', solution=solution)
    x.start('Neither Excel nor Google Sheets has an SVD function, so you build the ideas from cells. Sheet Small: the singular values of a 2 by 2 matrix from AᵀA. '
            'Sheet Image: the first rank 1 term of a noisy 8 by 8 image by power iteration. Sheet Deflation: the second and third singular values and the errors for ranks 1, 2 and 3. Sheet PCA: principal component analysis of the eight marks from Session 5. Sheet LoRA: count the numbers. '
            'The image and the marks are illustrative (made-up numbers to show the arithmetic). The numbers are the same as in the Python notebook.',
            ['Sheet Small: AᵀA, then trace, determinant, eigenvalues, singular values and the first singular vectors. Predict first.',
             'Sheet Image: AᵀA for the noisy image (an array formula), then ten rows of power iteration. Fill the gold guess cells, then sigma1, the unit vector, u1 and the rank 1 grid.',
             'Sheet Deflation: the rank 1 error, then round 2. The deflated matrix is given. Fill the gold guess cells of the power iteration, then sigma2, the unit vector, u2 and the rank 2 error. Round 3 is filled in, so you can read sigma3 and the rank 3 error.',
             'Sheet PCA: centre the marks, build the covariance matrix, find the eigenvalues and the top direction, then the scores, their variance, the explained variance and the squared distance lost.',
             'Sheet LoRA: count the numbers in a full update and in B and A together.',
             'For a matrix result, select the whole gold block and type the formula. In older Excel, confirm with Ctrl+Shift+Enter. In Excel 365 and Google Sheets, Enter works. #SPILL! means the cells below are not empty.'])

    # ------------------------------------------------------------------ Small
    ws = x.sheet('Small', {'A': 54, 'B': 13, 'C': 13})
    x.band(ws, 1, 'The singular values of a 2 by 2 matrix from A^T A', cols=3)
    x.text(ws, 'A3', 'A (rows 3 and 4)', bold=True)
    for r, row in enumerate(d['A']):
        for c, v in enumerate(row):
            ws[f'{"BC"[c]}{3 + r}'] = float(v)
            ws[f'{"BC"[c]}{3 + r}'].border = xl.BOX
    x.text(ws, 'A6', 'AᵀA (select B7:C8)')
    x.array(ws, 'B7:C8', '=MMULT(TRANSPOSE(B3:C4),B3:C4)', gold=True)
    x.text(ws, 'A10', 'Trace T of AᵀA')
    x.input(ws, 'B10', answer='=B7+C8')
    x.text(ws, 'A11', 'Determinant D of AᵀA')
    x.input(ws, 'B11', answer='=B7*C8-C7*B8')
    x.text(ws, 'A12', 'Square root of T² − 4D (given)')
    x.formula(ws, 'B12', '=SQRT(B10^2-4*B11)')
    x.text(ws, 'A13', 'Larger eigenvalue of AᵀA')
    x.input(ws, 'B13', answer='=(B10+B12)/2')
    x.text(ws, 'A14', 'Smaller eigenvalue of AᵀA')
    x.input(ws, 'B14', answer='=(B10-B12)/2')
    x.text(ws, 'A15', 'First singular value sigma1')
    x.input(ws, 'B15', answer='=SQRT(B13)')
    x.text(ws, 'A16', 'Second singular value sigma2')
    x.input(ws, 'B16', answer='=SQRT(B14)')
    x.text(ws, 'A18', 'Unit vector v1: first entry = C7 / length of (C7, B13 − B7)')
    x.input(ws, 'B18', answer='=C7/SQRT(C7^2+(B13-B7)^2)')
    x.text(ws, 'A19', 'Unit vector v1: second entry = (B13 - B7) / length')
    x.input(ws, 'B19', answer='=(B13-B7)/SQRT(C7^2+(B13-B7)^2)')
    x.text(ws, 'A21', 'u1 = A v1 / sigma1 (select B22:B23)')
    x.array(ws, 'B22:B23', '=MMULT(B3:C4,B18:B19)/B15', gold=True)
    x.text(ws, 'A24', 'Read: u1 has length 1 too. Check with SQRT(SUMSQ(B22:B23)).', italic=True)

    # ------------------------------------------------------------------ Image
    ws = x.sheet('Image', {'A': 30, **{c: 9 for c in COLS}, **{c: 10 for c in MVCOLS}, 'R': 11})
    x.band(ws, 1, 'A noisy 8 by 8 image: AᵀA, power iteration, and the first rank 1 term', cols=18)
    x.text(ws, 'A3', 'Noisy image (given), values 0 to 9', bold=True)
    for i in range(8):
        for j in range(8):
            c = ws[f'{COLS[j]}{4 + i}']
            c.value = float(d['noisy'][i, j])
            c.border = xl.BOX
    x.text(ws, 'A13', 'M = noisyᵀ noisy (select B14:I21). The noisy image is the block B4:I11', wrap=True)
    ws.row_dimensions[13].height = 30
    x.array(ws, 'B14:I21', '=MMULT(TRANSPOSE(B4:I11),B4:I11)', gold=True)
    x.band(ws, 23, 'Power iteration on M: the guess v, the product M v, and the largest entry', cols=18)
    x.text(ws, 'A24', 'Step k', bold=True, border=True)
    for j in range(8):
        x.text(ws, f'{COLS[j]}24', f'v{j + 1}', bold=True, border=True, align='center')
        x.text(ws, f'{MVCOLS[j]}24', f'M v {j + 1}', bold=True, border=True, align='center')
    x.text(ws, 'R24', 'Largest size', bold=True, border=True, align='center')
    for k in range(10):
        r = 25 + k
        ws[f'A{r}'] = k
        ws[f'A{r}'].border = xl.BOX
        for j in range(8):
            if k == 0:
                ws[f'{COLS[j]}{r}'] = 1.0
                ws[f'{COLS[j]}{r}'].border = xl.BOX
            else:
                x.input(ws, f'{COLS[j]}{r}', answer=f'={MVCOLS[j]}{r - 1}/$R{r - 1}')
            x.formula(ws, f'{MVCOLS[j]}{r}', f'=SUMPRODUCT($B${14 + j}:$I${14 + j},$B{r}:$I{r})')
        x.formula(ws, f'R{r}', f'=MAX(MAX(J{r}:Q{r}),-MIN(J{r}:Q{r}))')
    x.text(ws, 'A35', 'Gold cells in rows 26 to 34: each guess is the previous M v divided by the previous largest entry.', italic=True)
    x.text(ws, 'A36', 'Guess after 10 steps (M v / largest, row 34)')
    for j in range(8):
        x.input(ws, f'{COLS[j]}36', answer=f'={MVCOLS[j]}34/$R$34')
    x.text(ws, 'A37', 'Unit vector v1 (the guess divided by its length)')
    for j in range(8):
        x.input(ws, f'{COLS[j]}37', answer=f'={COLS[j]}36/SQRT(SUMSQ($B$36:$I$36))')
    x.text(ws, 'A39', 'sigma1 = square root of the largest entry (R34)')
    x.input(ws, 'B39', answer='=SQRT(R34)')
    x.text(ws, 'A40', 'u1 = N v1 / sigma1, N the noisy image (select B41:B48)')
    x.array(ws, 'B41:B48', '=MMULT(B4:I11,TRANSPOSE(B37:I37))/B39', gold=True)
    x.text(ws, 'A50', 'Rank 1 term = sigma1 × u1 × v1ᵀ. Cell in row i, column j: sigma1 × (i-th entry of u1) × (j-th entry of v1) (B52:I59)', wrap=True)
    ws.row_dimensions[50].height = 30
    for i in range(8):
        for j in range(8):
            x.input(ws, f'{COLS[j]}{52 + i}', answer=f'=$B$39*$B${41 + i}*{COLS[j]}$37')
    x.text(ws, 'A60', 'Read: every row of the grid is a multiple of v1. The grid holds 64 cells but only 8 + 8 + 1 numbers. Values can leave the 0 to 9 range (row 4, column 2 is about 10.4): it is an approximation.', italic=True, wrap=True)
    ws.row_dimensions[60].height = 45

    # ------------------------------------------------------------------ Deflation
    ws = x.sheet('Deflation', {'A': 34, **{c: 9 for c in COLS}, **{c: 10 for c in MVCOLS}, 'R': 11})
    x.band(ws, 1, 'Deflation: the second and third singular values, and the errors for ranks 1, 2 and 3', cols=18)
    x.text(ws, 'A3', 'Clean H (given), values 1 or 8', bold=True)
    for i in range(8):
        for j in range(8):
            c = ws[f'{COLS[j]}{4 + i}']
            c.value = float(d['H'][i, j])
            c.border = xl.BOX
    x.text(ws, 'A13', 'Error of the rank 1 approximation: the square root of the sum of the squared cell differences from the clean H', wrap=True)
    ws.row_dimensions[13].height = 45
    x.input(ws, 'B13', answer='=SQRT(SUMPRODUCT((Image!B52:I59-B4:I11)^2))')

    def round_block(top, k, src_m_row, v_sheet, v_row, m_cell, gold, grids_before):
        """One deflation round. src_m_row: first row of the source M grid (columns B to I) on sheet v_sheet's M sheet reference prefix."""
        pre_m, pre_v = src_m_row[0], v_sheet
        x.band(ws, top, f'Round {k}: subtract the previous rank 1 term from M, then power iteration', cols=18)
        x.text(ws, f'A{top + 1}', f'M{k} = previous M minus (largest entry) × v × vᵀ (given)', wrap=True)
        ws.row_dimensions[top + 1].height = 30
        m0 = top + 2
        for i in range(8):
            for j in range(8):
                x.formula(ws, f'{COLS[j]}{m0 + i}', f'={pre_m}{COLS[j]}{src_m_row[1] + i}-{m_cell}*{pre_v}${COLS[i]}${v_row}*{pre_v}${COLS[j]}${v_row}')
        h0 = top + 11
        x.text(ws, f'A{h0}', 'Step k', bold=True, border=True)
        for j in range(8):
            x.text(ws, f'{COLS[j]}{h0}', f'g{j + 1}', bold=True, border=True, align='center')
            x.text(ws, f'{MVCOLS[j]}{h0}', f'M g {j + 1}', bold=True, border=True, align='center')
        x.text(ws, f'R{h0}', 'Largest', bold=True, border=True, align='center')
        for s_ in range(10):
            r = h0 + 1 + s_
            ws[f'A{r}'] = s_
            ws[f'A{r}'].border = xl.BOX
            for j in range(8):
                if s_ == 0:
                    ws[f'{COLS[j]}{r}'] = 1.0
                    ws[f'{COLS[j]}{r}'].border = xl.BOX
                elif gold:
                    x.input(ws, f'{COLS[j]}{r}', answer=f'={MVCOLS[j]}{r - 1}/$R{r - 1}')
                else:
                    x.formula(ws, f'{COLS[j]}{r}', f'={MVCOLS[j]}{r - 1}/$R{r - 1}')
                x.formula(ws, f'{MVCOLS[j]}{r}', f'=SUMPRODUCT($B{m0 + j}:$I{m0 + j},$B{r}:$I{r})')
            x.formula(ws, f'R{r}', f'=MAX(MAX(J{r}:Q{r}),-MIN(J{r}:Q{r}))')
        last = h0 + 10
        g0 = last + 2
        put = x.input if gold else None
        x.text(ws, f'A{g0}', 'Guess after 10 steps (the last row of M g divided by its largest entry)', wrap=True)
        ws.row_dimensions[g0].height = 30
        x.text(ws, f'A{g0 + 1}', f'Unit vector v{k} (the guess divided by its length)', wrap=True)
        for j in range(8):
            f1 = f'={MVCOLS[j]}{last}/$R${last}'
            f2 = f'={COLS[j]}{g0}/SQRT(SUMSQ($B${g0}:$I${g0}))'
            if gold:
                x.input(ws, f'{COLS[j]}{g0}', answer=f1)
                x.input(ws, f'{COLS[j]}{g0 + 1}', answer=f2)
            else:
                x.formula(ws, f'{COLS[j]}{g0}', f1)
                x.formula(ws, f'{COLS[j]}{g0 + 1}', f2)
        s0 = g0 + 3
        x.text(ws, f'A{s0}', f'sigma{k} = square root of the largest entry (R{last})')
        if gold:
            x.input(ws, f'B{s0}', answer=f'=SQRT(R{last})')
        else:
            x.formula(ws, f'B{s0}', f'=SQRT(R{last})')
        x.text(ws, f'A{s0 + 1}', f'u{k} = noisy v{k} / sigma{k} (select B{s0 + 2}:B{s0 + 9})', wrap=True)
        ws.row_dimensions[s0 + 1].height = 30
        x.array(ws, f'B{s0 + 2}:B{s0 + 9}', f'=MMULT(Image!B4:I11,TRANSPOSE(B{g0 + 1}:I{g0 + 1}))/B{s0}', gold=gold)
        t0 = s0 + 11
        x.text(ws, f'A{t0}', f'Rank 1 term {k} = sigma{k} × u{k} × v{k}ᵀ (given), cells B{t0 + 1}:I{t0 + 8}', wrap=True)
        ws.row_dimensions[t0].height = 30
        for i in range(8):
            for j in range(8):
                x.formula(ws, f'{COLS[j]}{t0 + 1 + i}', f'=$B${s0}*$B${s0 + 2 + i}*{COLS[j]}${g0 + 1}')
        e0 = t0 + 10
        terms = '+'.join(grids_before + [f'B{t0 + 1}:I{t0 + 8}'])
        x.text(ws, f'A{e0}', f'Error of the rank {k} approximation from the clean H', wrap=True)
        ws.row_dimensions[e0].height = 30
        f_err = f'=SQRT(SUMPRODUCT(({terms}-$B$4:$I$11)^2))'
        if gold:
            x.input(ws, f'B{e0}', answer=f_err)
        else:
            x.formula(ws, f'B{e0}', f_err)
        return dict(last=last, sigma=f'B{s0}', vrow=g0 + 1, err=f'B{e0}', grid=f'B{t0 + 1}:I{t0 + 8}', m0=m0, end=e0)

    r2 = round_block(15, 2, ('Image!', 14), 'Image!', 37, 'Image!$R$34', True, ['Image!B52:I59'])
    r3 = round_block(r2['end'] + 3, 3, ('', r2['m0']), '', r2['vrow'], f'$R${r2["last"]}', False, ['Image!B52:I59', r2['grid']])

    # ------------------------------------------------------------------ PCA
    ws = x.sheet('PCA', {'A': 54, 'B': 13, 'C': 13, 'D': 13, 'E': 13, 'F': 13, 'G': 13})
    x.band(ws, 1, 'PCA of the eight marks from Session 5', cols=7)
    for j, h in enumerate(['Student', 'Maths mark', 'Physics mark', 'Centred maths', 'Centred physics', 'Score on component 1', '100 − physics']):
        x.text(ws, f'{"ABCDEFG"[j]}3', h, bold=True, border=True, wrap=True)
    ws.row_dimensions[3].height = 32
    for i in range(8):
        r = 4 + i
        ws[f'A{r}'] = i + 1
        ws[f'B{r}'] = float(p5['maths'][i])
        ws[f'C{r}'] = float(p5['phys'][i])
        for c in 'ABC':
            ws[f'{c}{r}'].border = xl.BOX
        x.input(ws, f'D{r}', answer=f'=B{r}-B$12')
        x.input(ws, f'E{r}', answer=f'=C{r}-C$12')
        x.input(ws, f'F{r}', answer=f'=$B$26*D{r}+$B$27*E{r}')
        x.formula(ws, f'G{r}', f'=100-C{r}')
    x.text(ws, 'A12', 'Mean of each column (given)', bold=True)
    x.formula(ws, 'B12', '=AVERAGE(B4:B11)')
    x.formula(ws, 'C12', '=AVERAGE(C4:C11)')
    x.text(ws, 'A14', 'Covariance matrix C: variance of maths (B15), covariance (C15), variance of physics (C16)', wrap=True)
    ws.row_dimensions[14].height = 30
    x.input(ws, 'B15', answer='=SUMPRODUCT(D4:D11,D4:D11)/(COUNT(D4:D11)-1)')
    x.input(ws, 'C15', answer='=SUMPRODUCT(D4:D11,E4:E11)/(COUNT(D4:D11)-1)')
    x.input(ws, 'C16', answer='=SUMPRODUCT(E4:E11,E4:E11)/(COUNT(E4:E11)-1)')
    x.input(ws, 'B16', answer='=C15')
    x.text(ws, 'A18', 'Trace of C (given)')
    x.formula(ws, 'B18', '=B15+C16')
    x.text(ws, 'A19', 'Determinant of C (given)')
    x.formula(ws, 'B19', '=B15*C16-C15*B16')
    x.text(ws, 'A20', 'Square root of T² − 4D (given)')
    x.formula(ws, 'B20', '=SQRT(B18^2-4*B19)')
    x.text(ws, 'A21', 'Larger eigenvalue of C')
    x.input(ws, 'B21', answer='=(B18+B20)/2')
    x.text(ws, 'A22', 'Smaller eigenvalue of C')
    x.input(ws, 'B22', answer='=(B18-B20)/2')
    x.text(ws, 'A23', 'Top eigenvector before scaling (given). Row 1 of (C − λI)v = 0 gives (s, t) = (C15, B21 − B15)', wrap=True)
    ws.row_dimensions[23].height = 30
    x.formula(ws, 'B23', '=C15')
    x.formula(ws, 'C23', '=B21-B15')
    x.text(ws, 'A24', 'Length of that vector (given)')
    x.formula(ws, 'B24', '=SQRT(B23^2+C23^2)')
    x.text(ws, 'A26', 'Principal component 1 at length 1: first entry')
    x.input(ws, 'B26', answer='=B23/B24')
    x.text(ws, 'A27', 'Principal component 1 at length 1: second entry')
    x.input(ws, 'B27', answer='=C23/B24')
    x.text(ws, 'A28', 'Scores: fill F4:F11 with entry 1 of component 1 × centred maths + entry 2 × centred physics', wrap=True)
    ws.row_dimensions[28].height = 30
    x.text(ws, 'A30', 'Variance of the 8 scores in F4:F11, dividing by n − 1')
    x.input(ws, 'B30', answer='=_xlfn.VAR.S(F4:F11)')
    x.text(ws, 'A31', 'Explained variance ratio = larger eigenvalue / trace')
    x.input(ws, 'B31', answer='=B21/B18')
    x.text(ws, 'A32', 'Squared distance lost = sum of the squared centred marks minus sum of the squared scores')
    x.input(ws, 'B32', answer='=SUMSQ(D4:E11)-SUMSQ(F4:F11)')
    x.text(ws, 'A34', 'Change one thing: covariance of maths with column G (100 − physics)')
    x.input(ws, 'B34', answer='=_xlfn.COVARIANCE.S(B4:B11,G4:G11)')
    x.text(ws, 'A35', 'Explained variance ratio with the new covariance')
    x.input(ws, 'B35', answer='=((B15+C16)+SQRT((B15+C16)^2-4*(B15*C16-B34^2)))/2/(B15+C16)')
    x.text(ws, 'A36', 'Read: the covariance changed sign. Did the explained variance ratio change?', italic=True)

    # ------------------------------------------------------------------ LoRA
    ws = x.sheet('LoRA', {'A': 62, 'B': 16})
    x.band(ws, 1, 'LoRA: count the numbers (illustrative sizes)', cols=2)
    x.text(ws, 'A3', 'd, the size of the square weight matrix W')
    ws['B3'] = d['lora_d']
    ws['B3'].border = xl.BOX
    x.text(ws, 'A4', 'r, the small inner size of B (d by r) and A (r by d)')
    ws['B4'] = d['lora_r']
    ws['B4'].border = xl.BOX
    x.text(ws, 'A6', 'Numbers in a full update of W (d × d)')
    x.input(ws, 'B6', answer='=B3*B3')
    x.text(ws, 'A7', 'Numbers in B and A together (2 × d × r)')
    x.input(ws, 'B7', answer='=2*B3*B4')
    x.text(ws, 'A8', 'Share of the full update')
    x.input(ws, 'B8', answer='=B7/B6')
    x.text(ws, 'A10', 'Change one thing: set r to 16 in B4. Predict the share first.', italic=True)

    x.check('Small: first entry of A^T A is 5', '=Small!B7', 5.0)
    x.check('Small: determinant of A^T A is 36', '=Small!B11', 36.0)
    x.check('Small: first singular value is 3', '=Small!B15', 3.0)
    x.check('Small: second singular value is 2', '=Small!B16', 2.0)
    x.check('Small: v1, first entry 0.447', '=Small!B18', float(abs(d['Vt'][0][0])), 0.001)
    x.check('Small: u1, first entry 0.894', '=Small!B22', float(abs(d['U'][0][0])), 0.001)
    x.check('Image: largest entry after 10 steps is about 1357.6', '=Image!R34', float(d['its'][-1][1]), 0.1)
    x.check('Image: sigma1', '=Image!B39', float(d['Sn'][0]), 0.001)
    x.check('Image: first entry of the unit vector v1', '=Image!B37', float(d['v_unit'][0]), 0.001)
    x.check('Image: first entry of u1', '=Image!B41', float(d['u1'][0]), 0.001)
    x.check('Image: rank 1 piece, row 4 column 2', '=Image!C55', float(d['rank1_svd'][3, 1]), 0.01)
    x.check('Image: the rank 1 piece has squared total sigma1 squared', '=SUMSQ(Image!B52:I59)', float(d['Sn'][0] ** 2), 0.1)
    x.check('Deflation: rank 1 error is 15.40', '=Deflation!B13', float(d['err_k'][1]), 0.01)
    x.check('Deflation: largest entry of round 2 is about 227.1', f'=Deflation!R{r2["last"]}', float(d['defl'][1]['m']), 0.1)
    x.check('Deflation: sigma2 is 15.07', f'=Deflation!{r2["sigma"]}', float(d['Sn'][1]), 0.001)
    x.check('Deflation: rank 2 error is 4.54', f'=Deflation!{r2["err"]}', float(d['err_k'][2]), 0.01)
    x.check('Deflation: sigma3 is about 4.89', f'=Deflation!{r3["sigma"]}', float(d['Sn'][2]), 0.01)
    x.check('Deflation: rank 3 error is 6.73', f'=Deflation!{r3["err"]}', float(d['err_k'][3]), 0.01)
    x.check('PCA: first centred maths mark', '=PCA!D4', float(d['Xc'][0, 0]))
    x.check('PCA: variance of maths is 66', '=PCA!B15', float(p5['C'][0, 0]))
    x.check('PCA: covariance is 48', '=PCA!C15', float(p5['C'][0, 1]))
    x.check('PCA: larger eigenvalue is 102', '=PCA!B21', float(lam[0]), 0.001)
    x.check('PCA: component 1, first entry 0.8', '=PCA!B26', float(d['top'][0]), 0.001)
    x.check('PCA: component 1, second entry 0.6', '=PCA!B27', float(d['top'][1]), 0.001)
    x.check('PCA: score of the first student', '=PCA!F4', float(d['scores'][0]), 0.001)
    x.check('PCA: variance of the scores is 102', '=PCA!B30', float(d['score_var']), 0.001)
    x.check('PCA: explained variance ratio', '=PCA!B31', float(d['ratio'][0]), 0.001)
    x.check('PCA: squared distance lost is 14', '=PCA!B32', float(d['lost']), 0.001)
    x.check('PCA: covariance with 100 minus physics is -48', '=PCA!B34', -48.0, 0.001)
    x.check('PCA: explained ratio is unchanged', '=PCA!B35', float(d['ratio'][0]), 0.001)
    x.check('LoRA: full update numbers', '=LoRA!B6', float(d['lora_full']))
    x.check('LoRA: numbers in B and A', '=LoRA!B7', float(d['lora_small']))
    x.check('LoRA: share is 0.016', '=LoRA!B8', 0.016, 0.0001)
    return x
