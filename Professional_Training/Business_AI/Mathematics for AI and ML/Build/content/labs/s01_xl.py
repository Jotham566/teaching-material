"""Session 1 spreadsheet lab: the same numbers as the notebook."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'kit'))
sys.path.insert(0, str(HERE.parent))
import xl as XL  # noqa: E402
import s01  # noqa: E402


def build(solution):
    F = s01.facts()
    x = XL.XL('Session 1: Functions and logarithms', 'Sigma sums, functions, LN and EXP, and log-probabilities', solution=solution)
    x.start('Compute in cells the numbers from the slides: a sigma sum, a function, logarithms, and the log-probability of a word and of a sentence. The numbers are the same as in the Python notebook.',
            ['Open the sheet called Work. Gold cells are yours.', 'In every block, predict first, then fill the gold cell with a formula.', 'Open the sheet Check. Every line must say OK.',
             'Change one thing in each block (the text tells you what) and watch the numbers move.', 'All numbers are illustrative (made-up numbers to show the arithmetic).'])
    ws = x.sheet('Work', {'A': 46, 'B': 16, 'C': 18, 'D': 18, 'E': 50})
    x.band(ws, 1, 'Session 1 lab: the numbers from the slides', 5)
    # block 1
    x.text(ws, 'A3', 'Step 1. Sigma sum of the probabilities', bold=True)
    x.text(ws, 'A4', 'Candidate next word', bold=True); x.text(ws, 'B4', 'p', bold=True); x.text(ws, 'C4', 'Step 4: minus LN(p)', bold=True)
    for i, (w_, p_) in enumerate(zip(s01.WORDS, s01.P)):
        r = 5 + i
        x.text(ws, f'A{r}', w_, border=True); x.formula(ws, f'B{r}', float(p_))
        x.input(ws, f'C{r}', answer=f'=-LN(B{r})')
    x.text(ws, 'A10', 'Sum of p', bold=True); x.input(ws, 'B10', answer='=SUM(B5:B9)')
    x.text(ws, 'E10', 'PREDICT: what will it be, and why?', italic=True, color='666666')
    x.text(ws, 'E4', 'Step 4 (after Step 3). Fill C5:C9 with minus LN(p) of each word.', italic=True, color='666666')
    x.text(ws, 'E5', 'PREDICT for Step 4: which word gets the largest number?', italic=True, color='666666')
    # block 2
    x.text(ws, 'A12', 'Step 2. A function f(x) = w x + b', bold=True)
    x.text(ws, 'A13', 'w'); x.formula(ws, 'B13', 2); x.text(ws, 'A14', 'b'); x.formula(ws, 'B14', 1); x.text(ws, 'A15', 'x'); x.formula(ws, 'B15', 3)
    x.text(ws, 'A16', 'f(x) = w * x + b', bold=True); x.input(ws, 'B16', answer='=B13*B15+B14')
    x.text(ws, 'E16', 'CHANGE: set w to 3. What is f(3) now? Set it back to 2.', italic=True, color='666666')
    # block 3
    x.text(ws, 'A18', 'Step 3. LN and EXP', bold=True)
    x.text(ws, 'A19', 'LN(6)'); x.input(ws, 'B19', answer='=LN(6)')
    x.text(ws, 'A20', 'LN(2) + LN(3)'); x.input(ws, 'B20', answer='=LN(2)+LN(3)')
    x.text(ws, 'A21', 'EXP(LN(6))  (EXP undoes LN)'); x.formula(ws, 'B21', '=EXP(LN(6))')
    x.text(ws, 'E19', 'READ: are rows 19 and 20 equal? Which log rule is this?', italic=True, color='666666')
    x.text(ws, 'E20', 'CHANGE: compare LN(2+3) with LN(2)+LN(3).', italic=True, color='666666')
    # block 4/5
    x.text(ws, 'A23', 'Step 5. Entropy: sum of p times minus LN(p), in nats', bold=True); x.input(ws, 'B23', answer='=SUMPRODUCT(B5:B9,C5:C9)')
    x.text(ws, 'E23', 'Hint: =SUMPRODUCT(range of p, range of minus LN(p)). PREDICT: closer to 0.5 or to 3?', italic=True, color='666666')
    # block 6
    x.text(ws, 'A25', 'Step 6. A sentence of six words', bold=True)
    x.text(ws, 'A26', 'Word', bold=True); x.text(ws, 'B26', 'p', bold=True); x.text(ws, 'C26', 'LN(p)', bold=True)
    for i, (w_, p_) in enumerate(zip(s01.SENT_WORDS, s01.SENT_P)):
        r = 27 + i
        x.text(ws, f'A{r}', w_, border=True); x.formula(ws, f'B{r}', float(p_)); x.input(ws, f'C{r}', answer=f'=LN(B{r})')
    x.text(ws, 'E27', 'Fill C27:C32 with LN(p) of each word.', italic=True, color='666666')
    x.text(ws, 'A33', 'Product of the six p', bold=True); x.input(ws, 'B33', answer='=PRODUCT(B27:B32)')
    x.text(ws, 'E33', 'Hint: =PRODUCT(range) multiplies every cell in the range.', italic=True, color='666666')
    x.text(ws, 'A34', 'Sum of the six LN(p)', bold=True); x.input(ws, 'B34', answer='=SUM(C27:C32)')
    x.text(ws, 'A35', 'EXP of that sum'); x.formula(ws, 'B35', '=EXP(B34)')
    x.text(ws, 'E35', 'READ: how does row 35 compare with row 33?', italic=True, color='666666')
    x.text(ws, 'A36', 'Plain average of minus LN(p) per word (nats)', bold=True); x.input(ws, 'B36', answer='=-B34/6')
    # block 7
    x.text(ws, 'A37', 'Step 7. A text of 1000 words, each p = 0.2', bold=True)
    x.text(ws, 'A38', 'p of each word'); x.formula(ws, 'B38', 0.2); x.text(ws, 'A39', 'Number of words'); x.formula(ws, 'B39', 1000)
    x.text(ws, 'A40', 'Sum of the logs = number of words * LN(p)', bold=True); x.input(ws, 'B40', answer='=B39*LN(B38)')
    x.text(ws, 'A41', 'The product B38^B39 (most tools show 0)'); x.formula(ws, 'B41', '=B38^B39')
    x.text(ws, 'E41', 'READ: why 0? Compare with row 40. CHANGE: set p to 0.5.', italic=True, color='666666')
    x.check('Step 1: the five probabilities add up to 1', '=Work!B10', 1.0)
    x.check('Step 2: f(3) = 7', '=Work!B16', 7)
    x.check('Step 3a: LN(6) = 1.7918', '=Work!B19', 1.7918, 0.001)
    x.check('Step 3b: LN(2) + LN(3) = 1.7918', '=Work!B20', 1.7918, 0.001)
    x.check('Step 4: minus LN(p) of Kampala = 0.478', '=Work!C5', 0.478, 0.001)
    x.check('Step 4: minus LN(p) of Entebbe = 1.715', '=Work!C6', 1.715, 0.001)
    x.check('Step 4: minus LN(p) of a = 2.303', '=Work!C7', 2.303, 0.001)
    x.check('Step 4: minus LN(p) of the = 2.813', '=Work!C8', 2.813, 0.001)
    x.check('Step 4: minus LN(p) of Nairobi = 3.219', '=Work!C9', 3.219, 0.001)
    x.check('Step 5: entropy, SUMPRODUCT of p and minus LN(p) = 1.133', '=Work!B23', 1.133, 0.001)
    x.check('Step 6a: product of the six probabilities = 0.005208', '=Work!B33', 0.005208, 0.000001)
    x.check('Step 6: LN(p) of the first word = -1.204', '=Work!C27', -1.204, 0.001)
    x.check('Step 6b: sum of the six logs = -5.2576', '=Work!B34', -5.2576, 0.001)
    x.check('Step 6c: average minus LN(p) per word = 0.8763', '=Work!B36', 0.8763, 0.0005)
    x.check('Step 7: sum of the logs for 1000 words = -1609.44', '=Work!B40', -1609.44, 0.01)
    return x
