"""Session 13 spreadsheet lab: the same dice, die, next-word and covariance tasks as the notebook, with fixed data (no RAND)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'kit'))
from xl import XL  # noqa: E402

ROLLS60 = [6, 6, 5, 6, 1, 5, 6, 2, 2, 1, 5, 6, 4, 4, 5, 1, 6, 6, 1, 6, 6, 2, 3, 5, 6, 1, 4, 3, 3, 5, 5, 3, 6, 4, 6, 1, 6, 5, 4, 3, 2, 2, 2, 5, 3, 6, 3, 4, 3, 5, 3, 6, 4, 1, 6, 4, 5, 6, 2, 1]
WORDS = ['tea', 'coffee', 'water', 'milk', 'soup']
LOGITS = [3.0, 2.6, 1.9, 1.2, 0.4]
LENGTHS = [3, 6, 5, 4, 4]
HOURS = [1, 2, 3, 5, 6, 7]
SCORE = [4, 2, 8, 5, 7, 10]


def build(solution: bool):
    x = XL('Session 13: Probability basics', 'Dice, expectation, variance, next-word probabilities, covariance and correlation', solution)
    x.start('You calculate the same numbers as the Python notebook: probabilities from two dice, the expectation and variance of a die, the mean and variance of 60 fixed rolls, '
            'next-word probabilities from five logits, and the covariance and correlation of two columns. The rolls are fixed values, so nothing changes when the sheet recalculates.',
            ['Open the sheet Dice. Fill the three gold cells. Look at the table of 36 sums first.',
             'Open the sheet Die. Fill E(X), the variance and the standard deviation with SUMPRODUCT, then the mean and variance of the 60 rolls.',
             'Open the sheet Words. Fill the probability of each word (a softmax by formula), then the expected length.',
             'Open the sheet Covariance. Fill the means, the covariance (by hand and with COVARIANCE.P), the variances and CORREL.',
             'CHANGE task: in Covariance, fill the last gold cell with COVARIANCE.S and say why it differs.',
             'Open the sheet Check. It says All 19 checks pass when every answer is right.'])

    # ------------------------------------------------------------ Dice
    ws = x.sheet('Dice', {'A': 40, 'B': 9, 'C': 9, 'D': 9, 'E': 9, 'F': 9, 'G': 9})
    x.band(ws, 1, 'Two dice: sample space and an event', cols=7)
    x.text(ws, 'A2', 'Each cell is the sum of die 1 (across) and die 2 (down). 36 equally likely outcomes.', color='666666')
    x.text(ws, 'A4', 'Die 2 down, die 1 across', bold=True)
    for j in range(6):
        x.text(ws, f'{"BCDEFG"[j]}4', j + 1, bold=True, align='center', border=True)
    for i in range(6):
        x.text(ws, f'A{5 + i}', i + 1, bold=True, align='right', border=True)
        for j in range(6):
            x.formula(ws, f'{"BCDEFG"[j]}{5 + i}', f'=$A{5 + i}+{"BCDEFG"[j]}$4')
    x.text(ws, 'A12', 'Your answers', bold=True)
    x.text(ws, 'A13', 'Outcomes with sum 7 (COUNTIF)')
    x.input(ws, 'B13', '=COUNTIF(B5:G10,7)')
    x.text(ws, 'A14', 'P(sum is 7) = outcomes / 36')
    x.input(ws, 'B14', '=B13/36')
    x.text(ws, 'A15', 'P(sum is 2 or 12)')
    x.input(ws, 'B15', '=(COUNTIF(B5:G10,2)+COUNTIF(B5:G10,12))/36')
    x.check('Outcomes with sum 7', '=Dice!B13', 6, 0)
    x.check('P(sum is 7)', '=Dice!B14', 1 / 6, 0.0001)
    x.check('P(sum is 2 or 12)', '=Dice!B15', 2 / 36, 0.0001)

    # ------------------------------------------------------------ Die
    ws = x.sheet('Die', {'A': 34, 'B': 12, 'C': 12, 'D': 18, 'E': 3, 'F': 8, 'G': 8, 'H': 3, 'I': 32, 'J': 12})
    x.band(ws, 1, 'One fair die, by formula, and 60 fixed rolls', cols=10)
    x.text(ws, 'A3', 'x (face)', bold=True, border=True)
    x.text(ws, 'B3', 'p(x)', bold=True, border=True)
    x.text(ws, 'C3', 'x times p(x)', bold=True, border=True)
    x.text(ws, 'D3', '(x - E(X)) squared times p(x)', bold=True, border=True, wrap=True)
    for i in range(6):
        r = 4 + i
        x.text(ws, f'A{r}', i + 1, border=True)
        x.formula(ws, f'B{r}', '=1/6')
        x.formula(ws, f'C{r}', f'=A{r}*B{r}')
        x.formula(ws, f'D{r}', f'=(A{r}-SUMPRODUCT($A$4:$A$9,$B$4:$B$9))^2*B{r}')
    x.text(ws, 'A11', 'E(X) = SUMPRODUCT of x and p(x)')
    x.input(ws, 'B11', '=SUMPRODUCT(A4:A9,B4:B9)')
    x.text(ws, 'A12', 'Var(X) = sum of (x - E(X)) squared times p(x)')
    x.input(ws, 'B12', '=SUMPRODUCT((A4:A9-B11)^2,B4:B9)')
    x.text(ws, 'A13', 'Standard deviation = square root of Var(X)')
    x.input(ws, 'B13', '=SQRT(B12)')
    x.text(ws, 'F3', 'Roll', bold=True, border=True)
    x.text(ws, 'G3', 'Face', bold=True, border=True)
    for k, v in enumerate(ROLLS60):
        x.text(ws, f'F{4 + k}', k + 1, border=True, align='right')
        x.text(ws, f'G{4 + k}', v, border=True, align='right')
    x.text(ws, 'I3', 'The 60 fixed rolls (same as the notebook)', bold=True)
    x.text(ws, 'I4', 'Mean of the 60 rolls (AVERAGE)')
    x.input(ws, 'J4', '=AVERAGE(G4:G63)')
    x.text(ws, 'I5', 'Variance of the 60 rolls (VAR.P)')
    x.input(ws, 'J5', '=_xlfn.VAR.P(G4:G63)')
    x.text(ws, 'I7', 'How often each face appeared', bold=True)
    for f in range(1, 7):
        x.text(ws, f'I{7 + f}', f'Face {f}')
        x.formula(ws, f'J{7 + f}', f'=COUNTIF($G$4:$G$63,{f})')
    x.text(ws, 'I14', 'Expected for a fair die: 10 of each')
    x.check('E(X) of a fair die', '=Die!B11', 3.5, 0.0001)
    x.check('Var(X) of a fair die', '=Die!B12', 35 / 12, 0.0001)
    x.check('Standard deviation of a fair die', '=Die!B13', (35 / 12) ** 0.5, 0.0001)
    x.check('Mean of the 60 fixed rolls', '=Die!J4', 3.9667, 0.0001)
    x.check('Variance of the 60 fixed rolls', '=Die!J5', 3.1322, 0.0001)

    # ------------------------------------------------------------ Words
    ws = x.sheet('Words', {'A': 34, 'B': 12, 'C': 22, 'D': 16, 'E': 10})
    x.band(ws, 1, 'Next-word probabilities (illustrative: made-up numbers)', cols=5)
    x.text(ws, 'A2', 'After "For breakfast I drink hot". Stable softmax: subtract the largest logit before EXP.', color='666666')
    for j, h in enumerate(['Word', 'Logit z', 'EXP(z - largest z)', 'Probability p(x)', 'Letters']):
        x.text(ws, f'{"ABCDE"[j]}3', h, bold=True, border=True, wrap=True)
    for i, (w_, z, ln) in enumerate(zip(WORDS, LOGITS, LENGTHS)):
        r = 4 + i
        x.text(ws, f'A{r}', w_, border=True)
        x.text(ws, f'B{r}', z, border=True)
        x.formula(ws, f'C{r}', f'=EXP(B{r}-MAX($B$4:$B$8))')
        x.input(ws, f'D{r}', f'=C{r}/SUM($C$4:$C$8)')
        x.text(ws, f'E{r}', ln, border=True)
    x.text(ws, 'A9', 'Sum of the five probabilities')
    x.input(ws, 'D9', '=SUM(D4:D8)')
    x.text(ws, 'A11', 'Expected length of the next word (letters)')
    x.input(ws, 'D11', '=SUMPRODUCT(D4:D8,E4:E8)')
    x.check('Probability of tea', '=Words!D4', 0.4459, 0.0005)
    x.check('The probabilities add up to 1', '=Words!D9', 1, 0.000001)
    x.check('Expected length of the next word', '=Words!D11', 4.3003, 0.0005)

    # ------------------------------------------------------------ Covariance
    ws = x.sheet('Covariance', {'A': 38, 'B': 12, 'C': 16, 'D': 16, 'E': 12})
    x.band(ws, 1, 'Two columns: covariance and correlation (illustrative data)', cols=5)
    x.text(ws, 'A2', 'Six learners: hours of study per week (x) and a quiz score out of 10 (y).', color='666666')
    for j, h in enumerate(['Hours x', 'Score y', 'x - mean of x', 'y - mean of y', 'Product']):
        x.text(ws, f'{"ABCDE"[j]}3', h, bold=True, border=True)
    # the data table uses columns A to E; the answers sit below
    for i, (hx, sy) in enumerate(zip(HOURS, SCORE)):
        r = 4 + i
        x.text(ws, f'A{r}', hx, border=True, align='right')
        x.text(ws, f'B{r}', sy, border=True)
        x.formula(ws, f'C{r}', f'=A{r}-AVERAGE($A$4:$A$9)')
        x.formula(ws, f'D{r}', f'=B{r}-AVERAGE($B$4:$B$9)')
        x.formula(ws, f'E{r}', f'=C{r}*D{r}')
    rows = [('Mean of x (AVERAGE)', '=AVERAGE(A4:A9)', 11), ('Mean of y', '=AVERAGE(B4:B9)', 12), ('Covariance by hand: the mean of the Product column', '=AVERAGE(E4:E9)', 13),
            ('Covariance with COVARIANCE.P', '=_xlfn.COVARIANCE.P(A4:A9,B4:B9)', 14), ('Variance of x (VAR.P)', '=_xlfn.VAR.P(A4:A9)', 15), ('Variance of y (VAR.P)', '=_xlfn.VAR.P(B4:B9)', 16),
            ('Correlation (CORREL)', '=CORREL(A4:A9,B4:B9)', 17), ('CHANGE task: covariance with COVARIANCE.S (divides by n - 1)', '=_xlfn.COVARIANCE.S(A4:A9,B4:B9)', 18)]
    for label, f, r in rows:
        x.text(ws, f'A{r}', label, wrap=True)
        x.input(ws, f'B{r}', f)
    ws.row_dimensions[13].height = 30
    ws.row_dimensions[18].height = 30
    exp = [('Mean of x', 4, 0.0001), ('Mean of y', 6, 0.0001), ('Covariance by hand', 25 / 6, 0.0001), ('Covariance with COVARIANCE.P', 25 / 6, 0.0001), ('Variance of x', 28 / 6, 0.0001),
           ('Variance of y', 7, 0.0001), ('Correlation', 0.7290, 0.0005), ('Sample covariance (COVARIANCE.S)', 5, 0.0001)]
    for (label, val, tol), (_, _, r) in zip(exp, rows):
        x.check(label, f'=Covariance!B{r}', val, tol)
    return x
