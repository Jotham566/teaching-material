"""Session 14 spreadsheet lab: binomial, normal, fixed samples and the CLT, confidence interval, A/B test, drawing words from their slices. No RAND."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'kit'))
from xl import XL  # noqa: E402

ROLLS60 = [6, 6, 5, 6, 1, 5, 6, 2, 2, 1, 5, 6, 4, 4, 5, 1, 6, 6, 1, 6, 6, 2, 3, 5, 6, 1, 4, 3, 3, 5, 5, 3, 6, 4, 6, 1, 6, 5, 4, 3, 2, 2, 2, 5, 3, 6, 3, 4, 3, 5, 3, 6, 4, 1, 6, 4, 5, 6, 2, 1]
FIXED12 = [[1, 5, 4, 3, 1, 5, 3, 6, 3, 4, 2, 4, 1, 5, 1, 5, 5, 3, 5, 4, 6, 5, 6, 1, 1, 4, 5, 5, 5, 3], [6, 4, 1, 2, 5, 4, 6, 6, 5, 2, 4, 3, 2, 6, 6, 4, 2, 3, 3, 5, 6, 1, 1, 1, 1, 6, 2, 1, 1, 1], [6, 6, 1, 5, 5, 6, 6, 5, 6, 6, 2, 3, 4, 5, 4, 1, 1, 5, 3, 5, 2, 2, 5, 2, 6, 2, 1, 5, 1, 4], [5, 2, 1, 4, 5, 5, 5, 5, 3, 6, 4, 6, 1, 3, 5, 1, 5, 2, 3, 1, 6, 5, 6, 5, 1, 2, 3, 6, 6, 2], [6, 3, 5, 4, 6, 6, 3, 6, 1, 1, 1, 6, 5, 2, 3, 5, 4, 5, 2, 1, 3, 1, 5, 6, 3, 1, 6, 1, 6, 6], [1, 5, 6, 4, 6, 3, 3, 4, 2, 3, 3, 1, 3, 2, 5, 2, 2, 3, 2, 3, 2, 5, 2, 5, 6, 5, 6, 3, 2, 3], [2, 1, 2, 3, 2, 5, 3, 3, 2, 2, 2, 1, 1, 4, 1, 4, 2, 1, 4, 2, 3, 1, 3, 1, 6, 2, 3, 1, 3, 6], [2, 4, 1, 1, 2, 4, 2, 3, 5, 2, 5, 3, 3, 4, 1, 1, 6, 6, 1, 3, 5, 1, 3, 5, 3, 6, 4, 1, 1, 5], [2, 6, 3, 3, 4, 1, 1, 5, 4, 2, 3, 2, 3, 5, 6, 1, 4, 2, 5, 6, 5, 1, 3, 1, 2, 1, 3, 4, 6, 3], [5, 4, 1, 6, 2, 2, 3, 5, 2, 4, 3, 4, 5, 1, 3, 1, 6, 1, 1, 3, 5, 3, 3, 2, 2, 6, 3, 4, 1, 3], [6, 4, 6, 6, 4, 2, 5, 3, 3, 2, 1, 4, 1, 1, 1, 3, 6, 6, 3, 6, 5, 1, 2, 3, 1, 5, 3, 6, 6, 2], [1, 4, 1, 5, 4, 3, 3, 1, 6, 5, 1, 5, 1, 4, 2, 5, 6, 6, 1, 2, 1, 1, 6, 4, 2, 2, 3, 6, 5, 5]]          # the first 12 of the 20,000 samples of 30 dice in the notebook (default_rng(14))
WORDS = ['tea', 'coffee', 'water', 'milk', 'soup']
LOGITS = [3.0, 2.6, 1.9, 1.2, 0.4]
U = [0.420, 0.926, 0.274, 0.060, 0.311, 0.718, 0.781, 0.539]
COLS = 'BCDEFGHIJKLM'


def build(solution: bool):
    x = XL('Session 14: Distributions and sampling', 'Binomial, Gaussian, sampling, a confidence interval, an A/B test and drawing the next word', solution)
    x.start('You calculate the same numbers as the Python notebook. The sample columns are fixed values, so nothing changes when the sheet recalculates. A sheet cannot hold the notebook\'s 20,000 samples of 30 dice, so the Sampling sheet holds the first 12 of them. The averages of those 12 are therefore the notebook\'s first 12 averages, and the standard error from the formula is the same 0.3118.',
            ['Sheet Binomial: fill the column P(X = k) with BINOM.DIST(k,10,0.3,FALSE), then the gold cells below it with COMBIN and BINOM.DIST.',
             'Sheet Normal: the z-score and two areas with NORM.DIST.',
             'Sheet Sampling: the average of each of the 12 samples of 30 dice is given. Fill the mean and the sample standard deviation (STDEV.S) of the 12 averages, the standard error from the formula and the interval of the 60 rolls (STDEV.S, n - 1).',
             'Sheet ABtest: the rates, the pooled rate, the standard error, z, the p-value and the interval for the gap.',
             'Sheet Words: the running totals (slice edges) of the next-word probabilities, then the word each fixed random number u picks.',
             'Sheet Check: it says All the checks pass when every answer is right.'])

    ws = x.sheet('Binomial', {'A': 46, 'B': 14})
    x.band(ws, 1, 'Binomial: 10 users, each rates helpful with p = 0.3 (illustrative)', cols=4)
    x.text(ws, 'A3', 'k (helpful ratings)', bold=True, border=True)
    x.text(ws, 'B3', 'P(X = k)', bold=True, border=True)
    for k in range(11):
        x.text(ws, f'A{4 + k}', k, border=True, align='right')
        x.input(ws, f'B{4 + k}', f'=_xlfn.BINOM.DIST(A{4 + k},10,0.3,FALSE)')
    rows = [('10 choose 3 = COMBIN(10,3) = 10! / (3! 7!)', '=COMBIN(10,3)', 15, 120), ('P(X = 3) by the formula COMBIN(10,3) * 0.3^3 * 0.7^7', '=COMBIN(10,3)*0.3^3*0.7^7', 16, 0.2668), ('P(X = 3) with BINOM.DIST(3,10,0.3,FALSE)', '=_xlfn.BINOM.DIST(3,10,0.3,FALSE)', 17, 0.2668),
            ('P(X at most 3) with BINOM.DIST(3,10,0.3,TRUE)', '=_xlfn.BINOM.DIST(3,10,0.3,TRUE)', 18, 0.6496), ('Sum of the 11 probabilities', '=SUM(B4:B14)', 19, 1), ('Mean = SUMPRODUCT of k and P(X = k)', '=SUMPRODUCT(A4:A14,B4:B14)', 20, 3)]
    for label, f, r, exp in rows:
        x.text(ws, f'A{r}', label, wrap=True)
        x.input(ws, f'B{r}', f)
        x.check(label, f'=Binomial!B{r}', exp, 0.0001)

    ws = x.sheet('Normal', {'A': 52, 'B': 14})
    x.band(ws, 1, 'Gaussian: quiz scores with mean 60 and standard deviation 10 (illustrative)', cols=3)
    for lab, f, r, exp in [('z-score of 75 = (75 - 60) / 10', '=(75-60)/10', 4, 1.5), ('P(X < 75) with NORM.DIST(75,60,10,TRUE)', '=_xlfn.NORM.DIST(75,60,10,TRUE)', 5, 0.9332),
                           ('P(50 < X < 70) = NORM.DIST(70,...) - NORM.DIST(50,...)', '=_xlfn.NORM.DIST(70,60,10,TRUE)-_xlfn.NORM.DIST(50,60,10,TRUE)', 6, 0.6827)]:
        x.text(ws, f'A{r}', lab, wrap=True)
        x.input(ws, f'B{r}', f)
        x.check(lab, f'=Normal!B{r}', exp, 0.0001)

    ws = x.sheet('Sampling', {'A': 10, 'N': 3, 'O': 8, 'P': 8, 'Q': 3, 'R': 56, 'S': 14})
    x.band(ws, 1, 'Twelve fixed samples of 30 dice (the first 12 of the notebook), and the 60 fixed rolls', cols=19)
    x.text(ws, 'A3', 'Die', bold=True, border=True)
    for j, c in enumerate(COLS):
        x.text(ws, f'{c}3', f'Sample {j + 1}', bold=True, border=True, wrap=True)
    for d in range(30):
        r = 4 + d
        x.text(ws, f'A{r}', d + 1, border=True)
        for j in range(12):
            x.text(ws, f'{COLS[j]}{r}', FIXED12[j][d], border=True, align='right')
    x.text(ws, 'A34', 'Average', bold=True, border=True)
    for c in COLS:
        x.formula(ws, f'{c}34', f'=AVERAGE({c}4:{c}33)')
    x.text(ws, 'O3', 'Roll', bold=True, border=True)
    x.text(ws, 'P3', 'Face', bold=True, border=True)
    for k, v in enumerate(ROLLS60):
        x.text(ws, f'O{4 + k}', k + 1, border=True)
        x.text(ws, f'P{4 + k}', v, border=True)
    lines = [('Mean of the 12 averages (row 34)', '=AVERAGE(B34:M34)', 4, 3.3972, 0.0005), ('Sample standard deviation of the 12 averages (STDEV.S)', '=_xlfn.STDEV.S(B34:M34)', 5, 0.3748, 0.0005),
             ('Standard error from the formula: sqrt(35/12) / sqrt(30)', '=SQRT(35/12)/SQRT(30)', 6, 0.3118, 0.0005), ('Sample standard deviation of the 60 rolls (STDEV.S)', '=_xlfn.STDEV.S(P4:P63)', 7, 1.7847, 0.0005),
             ('Interval of the 60 rolls, lower end: mean - 1.96 * s / sqrt(60)', '=AVERAGE(P4:P63)-1.96*_xlfn.STDEV.S(P4:P63)/SQRT(60)', 8, 3.515, 0.001),
             ('Interval of the 60 rolls, upper end', '=AVERAGE(P4:P63)+1.96*_xlfn.STDEV.S(P4:P63)/SQRT(60)', 9, 4.418, 0.001)]
    for lab, f, r, exp, tol in lines:
        x.text(ws, f'R{r}', lab, wrap=True)
        x.input(ws, f'S{r}', f)
        x.check(lab, f'=Sampling!S{r}', exp, tol)
    x.text(ws, 'R11', 'Why 0.3748 and not 0.3118? Twelve averages are too few to show the standard error exactly. The notebook uses 20,000 averages and gets 0.311.', color='666666', wrap=True)
    ws.row_dimensions[11].height = 45

    ws = x.sheet('ABtest', {'A': 50, 'B': 14, 'C': 14})
    x.band(ws, 1, 'A/B test: two proportions (illustrative counts)', cols=3)
    for j, h in enumerate(['', 'A: current', 'B: new feature']):
        x.text(ws, f'{"ABC"[j]}3', h, bold=True, border=True)
    x.text(ws, 'A4', 'Users', border=True); x.text(ws, 'B4', 2400, border=True); x.text(ws, 'C4', 2400, border=True)
    x.text(ws, 'A5', 'Chats rated helpful', border=True); x.text(ws, 'B5', 288, border=True); x.text(ws, 'C5', 336, border=True)
    items = [('Rate of A', '=B5/B4', 7, 0.12, 0.0001), ('Rate of B', '=C5/C4', 8, 0.14, 0.0001), ('Pooled rate = (288 + 336) / (2400 + 2400)', '=(B5+C5)/(B4+C4)', 9, 0.13, 0.0001),
             ('Standard error under the null', '=SQRT(B9*(1-B9)*(1/B4+1/C4))', 10, 0.009708, 0.00002), ('z = (rate B - rate A) / standard error', '=(B8-B7)/B10', 11, 2.0601, 0.001),
             ('Two-sided p-value = 2 * (1 - NORM.DIST(z,0,1,TRUE))', '=2*(1-_xlfn.NORM.DIST(B11,0,1,TRUE))', 12, 0.0394, 0.0005),
             ('Interval for the gap, lower end (no pooling: the interval does not assume the rates are equal)', '=(B8-B7)-1.96*SQRT(B7*(1-B7)/B4+B8*(1-B8)/C4)', 13, 0.0010, 0.0002),
             ('Interval for the gap, upper end', '=(B8-B7)+1.96*SQRT(B7*(1-B7)/B4+B8*(1-B8)/C4)', 14, 0.0390, 0.0002)]
    for lab, f, r, exp, tol in items:
        x.text(ws, f'A{r}', lab, wrap=True)
        x.input(ws, f'B{r}', f)
        x.check(lab, f'=ABtest!B{r}', exp, tol)

    ws = x.sheet('Words', {'A': 12, 'B': 10, 'C': 14, 'D': 16, 'E': 3, 'F': 8, 'G': 10, 'H': 34})
    x.band(ws, 1, 'Drawing the next word: slices of 0 to 1 (illustrative)', cols=8)
    x.text(ws, 'A2', 'The probabilities are the Session 13 softmax of the logits. Each word owns a slice as wide as its probability; the running total is the slice edge.', color='666666')
    for c, h in zip('ABCD', ['Word', 'Logit z', 'Probability p', 'Running total (gold)']):
        x.text(ws, f'{c}3', h, bold=True, border=True, wrap=True)
    for i, (w_, z) in enumerate(zip(WORDS, LOGITS)):
        r = 4 + i
        x.text(ws, f'A{r}', w_, border=True); x.text(ws, f'B{r}', z, border=True)
        x.formula(ws, f'C{r}', f'=EXP(B{r}-MAX($B$4:$B$8))/SUMPRODUCT(EXP($B$4:$B$8-MAX($B$4:$B$8)))')
        x.input(ws, f'D{r}', f'=SUM($C$4:C{r})')
    x.text(ws, 'F3', 'Draw', bold=True, border=True); x.text(ws, 'G3', 'u', bold=True, border=True)
    x.text(ws, 'H3', 'Word picked: the first word whose running total reaches u', bold=True, wrap=True)
    for i, u in enumerate(U):
        r = 4 + i
        x.text(ws, f'F{r}', i + 1, border=True); x.text(ws, f'G{r}', u, border=True)
        x.input(ws, f'H{r}', f'=INDEX($A$4:$A$8,COUNTIF($D$4:$D$8,"<"&G{r})+1)')
    x.text(ws, 'A13', 'Hint for column H: COUNTIF($D$4:$D$8,"<"&G4) counts the slice edges below u; the word is the next one: INDEX($A$4:$A$8, that count + 1).', color='666666')
    x.text(ws, 'A14', 'Draws equal to tea'); x.input(ws, 'D14', '=COUNTIF(H4:H11,"tea")')
    x.text(ws, 'A15', 'CHANGE: type 0.9 in G4 and watch H4. Then type 0.42 back.', italic=True)
    for lab, ref, exp, tol in [('Running total after coffee', 'D5', 0.7448, 0.0005), ('Running total after soup', 'D8', 1, 0.000001), ('Word picked by u = 0.926', 'H5', 'milk', 0),
                               ('Draws equal to tea', 'D14', 4, 0)]:
        x.check(lab, f'=Words!{ref}', exp, tol)
    return x
