"""Session 17 workbook: surprise, entropy, cross-entropy, KL divergence, softmax, its gradient and perplexity in cells (same numbers as labs/s17_nb.py)."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'kit'))
import xl  # noqa: E402

_spec = importlib.util.spec_from_file_location('s17_nb_for_xl', HERE / 's17_nb.py')
_nb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_nb)


def build(solution=False):
    N = _nb.namespace()
    x = xl.XL('Session 17: Information theory', 'Surprise, entropy, cross-entropy, KL divergence, temperature, top-p and perplexity in cells', solution)
    x.start('The same maths as the Python notebook, in cells. You compute surprise and entropy with logarithms (bits), then cross-entropy and KL divergence for two models, then the stable softmax of Session 12 with temperature and its gradient (nats), a top-p cut, then the perplexity of a six word sentence.',
            ['Sheet Entropy: fill the gold cells. Use LOG(p, 2) for bits. Predict first: which coin has more entropy, the fair one or the 0.9 one?',
             'Sheet Softmax: build the stable softmax in three rows, then the gradient p - y, the loss and the loss after a small nudge (the log-softmax form on the slides). Change one thing: set T in cell B10 to 0.5.',
             'Sheet Sampling: the softmax of five drinks, the running total, which drinks top-p = 0.8 keeps, and their rescaled probabilities.',
             'Sheet Perplexity: -ln p for each word, the mean, and the perplexity.',
             'Open the sheet Check. It says All checks pass when every gold cell is right.'])
    P, QA, QB = [float(v) for v in N['P']], [float(v) for v in N['Q_A']], [float(v) for v in N['Q_B']]

    # ------------------------------------------------------------------ Entropy
    we = x.sheet('Entropy', {'A': 30, 'B': 14, 'C': 16, 'D': 16, 'E': 14, 'F': 14})
    x.band(we, 1, 'Surprise, entropy, cross-entropy and KL divergence', cols=6)
    x.text(we, 'A3', 'Part 1: surprise in bits = -LOG(p, 2)', bold=True)
    x.table(we, 'A4', ['Event', 'p', 'Surprise (bits)'], [['A fair coin shows heads', 0.5, None], ['A random letter from A to H', 0.125, None], ['One of 1,024 equal tickets', '=1/1024', None]])
    for r in (5, 6, 7):
        x.input(we, f'C{r}', answer=f'=-LOG(B{r},2)')
    x.text(we, 'A9', 'Part 2: entropy of four next words', bold=True)
    x.table(we, 'A10', ['Next word', 'P', 'Surprise (bits)', 'P × surprise'], [[w, p, None, None] for w, p in zip(['the', 'a', 'one', 'my'], P)])
    for r in range(11, 15):
        x.input(we, f'C{r}', answer=f'=-LOG(B{r},2)')
        x.input(we, f'D{r}', answer=f'=B{r}*C{r}')
    x.text(we, 'A15', 'Entropy of P (bits)', bold=True)
    x.input(we, 'B15', answer='=SUM(D11:D14)')
    x.text(we, 'A16', 'Entropy of a 0.9 / 0.1 coin (bits)', bold=True)
    x.input(we, 'B16', answer='=-(0.9*LOG(0.9,2)+0.1*LOG(0.1,2))')
    we['B16'].number_format = '0.0000'
    x.text(we, 'A18', 'Part 3: cross-entropy of two models against P', bold=True)
    x.table(we, 'A19', ['Next word', 'P', 'Q_A (uniform)', 'Q_B', 'log2 Q_A', 'log2 Q_B'], [[w, p, a, b, None, None] for w, p, a, b in zip(['the', 'a', 'one', 'my'], P, QA, QB)])
    for r in range(20, 24):
        x.input(we, f'E{r}', answer=f'=LOG(C{r},2)')
        x.input(we, f'F{r}', answer=f'=LOG(D{r},2)')
        we[f'E{r}'].number_format = '0.0000'
        we[f'F{r}'].number_format = '0.0000'
    x.text(we, 'A24', 'Cross-entropy of model A (bits)', bold=True)
    x.input(we, 'B24', answer='=-SUMPRODUCT(B20:B23,E20:E23)')
    x.text(we, 'A25', 'Cross-entropy of model B (bits)', bold=True)
    x.input(we, 'B25', answer='=-SUMPRODUCT(B20:B23,F20:F23)')
    x.text(we, 'A26', 'KL divergence of model A', bold=True)
    x.input(we, 'B26', answer='=B24-B15')
    x.text(we, 'A27', 'KL divergence of model B', bold=True)
    x.input(we, 'B27', answer='=B25-B15')
    for r in (24, 25, 26, 27):
        we[f'B{r}'].number_format = '0.0000'
    x.text(we, 'A29', 'Read: which model has the smaller cross-entropy, and by how much is each above the entropy?', italic=True, color=xl.GREY)
    x.text(we, 'A30', 'Change one thing: set the 0.9 / 0.1 coin to 0.99 / 0.01 in cell B16 and watch the entropy fall.', italic=True, color=xl.GREY)
    x.check('Surprise of 1/1024 in bits', '=Entropy!C7', 10, 0.0001)
    x.check('Entropy of P (bits)', '=Entropy!B15', 1.75, 0.0001)
    x.check('Entropy of the 0.9 / 0.1 coin', '=Entropy!B16', 0.469, 0.001)
    x.check('Cross-entropy of model A', '=Entropy!B24', 2.0, 0.0001)
    x.check('Cross-entropy of model B', '=Entropy!B25', round(float(N['ce_B']), 4), 0.0005)
    x.check('KL divergence of model A', '=Entropy!B26', 0.25, 0.0001)
    x.check('KL divergence of model B', '=Entropy!B27', round(float(N['kl_B']), 4), 0.0005)

    # ------------------------------------------------------------------ Softmax
    ws = x.sheet('Softmax', {'A': 34, 'B': 13, 'C': 13, 'D': 13, 'E': 14})
    x.band(ws, 1, 'Stable softmax, its gradient and the loss', cols=5)
    x.text(ws, 'A2', 'Three classes: cat, dog, fox. Dog is the true word. T is the temperature (1 means the plain softmax). Losses are in nats (ln).', color=xl.GREY, italic=True)
    x.table(ws, 'A3', ['', 'cat', 'dog', 'fox'], [['Logit z', 2.0, 1.0, 0.1], ['Shifted: (z - largest z) / T', None, None, None], ['exp of shifted', None, None, None], ['Softmax p', None, None, None],
                                                           ['Target y', 0, 1, 0], ['Gradient p - y', None, None, None]])
    for cl in 'BCD':
        x.input(ws, f'{cl}5', answer=f'=({cl}4-MAX($B$4:$D$4))/$B$10')
        x.input(ws, f'{cl}6', answer=f'=EXP({cl}5)')
        x.input(ws, f'{cl}7', answer=f'={cl}6/SUM($B$6:$D$6)')
        x.input(ws, f'{cl}9', answer=f'={cl}7-{cl}8')
        for r in (5, 6, 7, 9):
            ws[f'{cl}{r}'].number_format = '0.0000'
    x.text(ws, 'A10', 'Temperature T', bold=True)
    ws['B10'] = 1
    ws['B10'].border = xl.BOX
    x.text(ws, 'A11', 'Loss = -ln(p of dog), nats', bold=True)
    x.input(ws, 'B11', answer='=-LN(SUMPRODUCT(B7:D7,B8:D8))')
    ws['B11'].number_format = '0.0000'
    x.text(ws, 'A12', 'Loss after adding 0.001 to the cat logit (given: log-sum-exp of z / T, minus the dog logit / T)', bold=True)
    x.formula(ws, 'B12', '=LN(EXP((B4+0.001)/$B$10)+EXP(C4/$B$10)+EXP(D4/$B$10))-C4/$B$10')
    ws['B12'].number_format = '0.000000'
    x.text(ws, 'A13', 'Numeric gradient for the cat logit', bold=True)
    x.input(ws, 'B13', answer='=(B12-B11)/0.001')
    ws['B13'].number_format = '0.0000'
    x.text(ws, 'A14', 'Formula gradient for the cat logit, (p - y) / T (given)', bold=True)
    x.formula(ws, 'B14', '=B9/$B$10')
    ws['B14'].number_format = '0.0000'
    x.text(ws, 'A15', 'Large logits (given formulas): the shift keeps them safe', bold=True)
    x.table(ws, 'A16', ['', 'Class 1', 'Class 2', 'Class 3'], [['Logit z', 1000, 1001, 1002], ['Shifted', None, None, None], ['exp of shifted', None, None, None], ['Softmax p', None, None, None]])
    for cl in 'BCD':
        x.formula(ws, f'{cl}18', f'={cl}17-MAX($B$17:$D$17)')
        x.formula(ws, f'{cl}19', f'=EXP({cl}18)')
        x.formula(ws, f'{cl}20', f'={cl}19/SUM($B$19:$D$19)')
        ws[f'{cl}20'].number_format = '0.0000'
    x.text(ws, 'A22', 'Read: the gradient entries add to 0. Dog, the true word, has a negative entry. Why? The numeric gradient (B13) and the formula (B14) agree for any T.', italic=True, color=xl.GREY)
    x.text(ws, 'A23', 'Change one thing: set T to 0.5, then to 2, and watch the top probability (0.8638 and 0.5017). Then set T back to 1.', italic=True, color=xl.GREY)
    x.check('Softmax probability of cat', '=Softmax!B7', round(float(N['probs'][0]), 4), 0.0005)
    x.check('Softmax probability of dog', '=Softmax!C7', round(float(N['probs'][1]), 4), 0.0005)
    x.check('Gradient p - y for dog', '=Softmax!C9', round(float(N['grad'][1]), 4), 0.0005)
    x.check('Loss (nats)', '=Softmax!B11', round(float(N['L0']), 4), 0.001)
    x.check('Numeric gradient matches 0.659', '=Softmax!B13', round(float(N['grad'][0]), 3), 0.001)
    x.check('Softmax of the large logits, class 3', '=Softmax!D20', 0.6652, 0.0005)

    # ------------------------------------------------------------------ Sampling (temperature and top-p)
    wsm = x.sheet('Sampling', {'A': 26, 'B': 12, 'C': 16, 'D': 16, 'E': 14, 'F': 18})
    x.band(wsm, 1, 'Temperature and top-p (nucleus) sampling', cols=6)
    x.text(wsm, 'A2', 'Five next words with illustrative logits, sorted from most to least likely. Predict first: how many will top-p = 0.8 keep?', color=xl.GREY, italic=True)
    x.text(wsm, 'A3', 'Temperature T', bold=True)
    wsm['B3'] = 1
    wsm['B3'].border = xl.BOX
    x.text(wsm, 'C3', 'top-p', bold=True)
    wsm['D3'] = 0.8
    wsm['D3'].border = xl.BOX
    x.table(wsm, 'A5', ['Word', 'Logit', 'Softmax p at T', 'Running total', 'Kept (1 or 0)', 'Rescaled p'], [[w_, float(v), None, None, None, None] for w_, v in zip(N['words5'], N['logits5'])])
    for i in range(5):
        r = 6 + i
        x.input(wsm, f'C{r}', answer=f'=EXP((B{r}-MAX($B$6:$B$10))/$B$3)/SUMPRODUCT(EXP(($B$6:$B$10-MAX($B$6:$B$10))/$B$3))')
        x.input(wsm, f'D{r}', answer=f'=SUM($C$6:C{r})')
        x.input(wsm, f'E{r}', answer=f'=IF(D{r}-C{r}<$D$3,1,0)')
        x.input(wsm, f'F{r}', answer=f'=C{r}*E{r}/SUMPRODUCT($C$6:$C$10,$E$6:$E$10)')
        for cl in 'CDF':
            wsm[f'{cl}{r}'].number_format = '0.0000'
    x.text(wsm, 'A12', 'Number of words kept', bold=True)
    x.input(wsm, 'B12', answer='=SUM(E6:E10)')
    x.text(wsm, 'A14', 'Read: a word is kept while the running total before it is still below p. After the cut, can milk or soup be drawn?', italic=True, color=xl.GREY)
    x.text(wsm, 'A15', 'Change one thing: set T (B3) to 2. How many words does top-p keep now? Then set T back to 1.', italic=True, color=xl.GREY)
    x.check('Softmax p of tea at T = 1', '=Sampling!C6', round(float(N['p5'][0]), 4), 0.0005)
    x.check('Running total after water', '=Sampling!D8', round(float(N['p5'][:3].sum()), 4), 0.0005)
    x.check('Words kept by top-p 0.8', '=Sampling!B12', 3, 0)
    x.check('Rescaled p of tea', '=Sampling!F6', round(float(N['p_nucleus'][0]), 4), 0.0005)

    # ------------------------------------------------------------------ Perplexity
    wp = x.sheet('Perplexity', {'A': 30, 'B': 14, 'C': 16, 'D': 18})
    x.band(wp, 1, 'Cross-entropy and perplexity of a toy language model', cols=4)
    x.text(wp, 'A2', 'Illustrative (made-up) probabilities the model gave to each real word of the sentence.', color=xl.GREY, italic=True)
    x.table(wp, 'A3', ['Word', 'p given by the model', '-ln p', '-log2 p (given)'], [[w, float(p), None, None] for w, p in zip(N['words'], N['token_probs'])])
    for r in range(4, 10):
        x.input(wp, f'C{r}', answer=f'=-LN(B{r})')
        x.formula(wp, f'D{r}', f'=-LOG(B{r},2)')
        wp[f'C{r}'].number_format = '0.0000'
        wp[f'D{r}'].number_format = '0.0000'
    x.text(wp, 'A11', 'Sum of -ln p', bold=True)
    x.input(wp, 'B11', answer='=SUM(C4:C9)')
    x.text(wp, 'A12', 'Mean -ln p (nats per word)', bold=True)
    x.input(wp, 'B12', answer='=AVERAGE(C4:C9)')
    x.text(wp, 'A13', 'Perplexity', bold=True)
    x.input(wp, 'B13', answer='=EXP(B12)')
    x.text(wp, 'A14', 'Perplexity from bits (given)', bold=True)
    x.formula(wp, 'B14', '=2^AVERAGE(D4:D9)')
    for r in (11, 12, 13, 14):
        wp[f'B{r}'].number_format = '0.0000'
    x.text(wp, 'A16', 'Read: the two perplexities agree. Which word hurt the score most?', italic=True, color=xl.GREY)
    x.text(wp, 'A17', 'Change one thing: set all six probabilities to 0.02 (that is 1/50) and read the perplexity.', italic=True, color=xl.GREY)
    x.check('Sum of -ln p over the six words', '=Perplexity!B11', round(float(N['total_nll']), 3), 0.001)
    x.check('Mean -ln p', '=Perplexity!B12', round(float(N['mean_nll']), 4), 0.001)
    x.check('Perplexity', '=Perplexity!B13', round(float(N['perplexity']), 3), 0.002)
    x.check('Perplexity from bits equals perplexity from nats', '=Perplexity!B14', round(float(N['perplexity']), 3), 0.002)
    return x
