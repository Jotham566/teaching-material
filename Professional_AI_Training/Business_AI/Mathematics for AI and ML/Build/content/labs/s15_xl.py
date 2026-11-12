"""Session 15 spreadsheet lab: counts table, independence, Bayes with a medical test, Naive Bayes spam filter by formula."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'kit'))
from xl import XL  # noqa: E402


def build(solution: bool):
    x = XL('Session 15: Conditional probability and Bayes', 'Counts, independence, a medical test with Bayes theorem and a Naive Bayes spam filter', solution)
    x.start('You calculate the same numbers as the Python notebook, from the same counts. All numbers are illustrative.',
            ['Sheet Counts: joint, marginal and conditional probabilities, and the expected count if "free" and spam were independent.',
             'Sheet Medical: the evidence, the posterior after one positive test, and after a second one.',
             'Sheet NaiveBayes: smoothed likelihoods, the scores and the posterior of two emails.',
             'CHANGE task: in NaiveBayes, the posterior of email 1 without smoothing. Why is it 1?',
             'Then, below it, the log scores of email 1 and the posterior from them, and the posterior with a spam prior of 0.01.',
             'Sheet Check: it says All the checks pass when every answer is right.'])

    ws = x.sheet('Counts', {'A': 52, 'B': 14, 'C': 14, 'D': 12})
    x.band(ws, 1, '100 emails: spam or ham, with or without the word "free"', cols=4)
    for j, h in enumerate(['', 'Contains "free"', 'No "free"', 'Total']):
        x.text(ws, f'{"ABCD"[j]}3', h, bold=True, border=True)
    x.text(ws, 'A4', 'Spam', border=True); x.text(ws, 'B4', 28, border=True); x.text(ws, 'C4', 12, border=True); x.formula(ws, 'D4', '=B4+C4')
    x.text(ws, 'A5', 'Ham', border=True); x.text(ws, 'B5', 6, border=True); x.text(ws, 'C5', 54, border=True); x.formula(ws, 'D5', '=B5+C5')
    x.text(ws, 'A6', 'Total', border=True); x.formula(ws, 'B6', '=B4+B5'); x.formula(ws, 'C6', '=C4+C5'); x.formula(ws, 'D6', '=D4+D5')
    rows = [('P(spam and free) = joint count / total', '=B4/D6', 9, 0.28, 0.0001), ('P(free) = emails with "free" / total', '=B6/D6', 10, 0.34, 0.0001),
            ('P(spam | free) = joint / P(free)', '=B9/B10', 11, 0.8235, 0.0001), ('P(free | spam) = spam with "free" / spam emails', '=B4/D4', 12, 0.70, 0.0001),
            ('Expected spam emails with "free" if independent = total × P(spam) × P(free)', '=D6*(D4/D6)*B10', 13, 13.6, 0.0001)]
    for lab, f, r, exp, tol in rows:
        x.text(ws, f'A{r}', lab, wrap=True)
        x.input(ws, f'B{r}', f)
        x.check(lab, f'=Counts!B{r}', exp, tol)
        ws.row_dimensions[r].height = 30 if len(lab) > 55 else 16

    ws = x.sheet('Medical', {'A': 58, 'B': 14})
    x.band(ws, 1, 'A medical test (illustrative)', cols=2)
    for lab, v, r in [('Prior: prevalence P(sick)', 0.01, 3), ('Likelihood (sensitivity): P(positive | sick)', 0.90, 4), ('False positive rate: P(positive | healthy)', 0.10, 5)]:
        x.text(ws, f'A{r}', lab); x.text(ws, f'B{r}', v, border=True)
    items = [('Evidence P(positive) = likelihood × prior + false positive rate × (1 - prior)', '=B4*B3+B5*(1-B3)', 7, 0.108, 0.0001), ('Posterior P(sick | positive) = likelihood × prior / evidence', '=B4*B3/B7', 8, 0.0833, 0.0001),
             ('Posterior after a second independent positive test (new prior = the posterior)', '=B4*B8/(B4*B8+B5*(1-B8))', 9, 0.45, 0.0001)]
    for lab, f, r, exp, tol in items:
        x.text(ws, f'A{r}', lab, wrap=True)
        x.input(ws, f'B{r}', f)
        x.check(lab, f'=Medical!B{r}', exp, tol)
        ws.row_dimensions[r].height = 30
    x.text(ws, 'A11', 'CHANGE task: set the prevalence in B3 to 0.10 and watch B8. Then set it back to 0.01.', italic=True, wrap=True)

    ws = x.sheet('NaiveBayes', {'A': 40, 'B': 12, 'C': 12, 'D': 14, 'E': 14, 'F': 10, 'G': 10, 'H': 11, 'I': 11, 'J': 11, 'K': 11})
    x.band(ws, 1, 'Naive Bayes spam filter from counts (illustrative)', cols=11)
    x.text(ws, 'A2', 'Smoothed likelihood = (count + 1) / (emails in the class + 2). A flag of 1 means the word is in the email.', color='666666')
    heads = ['Word', 'Spam count', 'Ham count', 'P(word | spam)', 'P(word | ham)', 'Email 1', 'Email 2', 'E1 spam factor', 'E1 ham factor', 'E2 spam factor', 'E2 ham factor']
    for j, h in enumerate(heads):
        x.text(ws, f'{"ABCDEFGHIJK"[j]}3', h, bold=True, border=True, wrap=True)
    ws.row_dimensions[3].height = 30
    for i, (w_, s_, h_, f1, f2) in enumerate([('free', 28, 6, 1, 1), ('prize', 20, 0, 1, 0), ('meeting', 4, 30, 0, 1)]):
        r = 4 + i
        x.text(ws, f'A{r}', w_, border=True); x.text(ws, f'B{r}', s_, border=True); x.text(ws, f'C{r}', h_, border=True)
        x.input(ws, f'D{r}', f'=(B{r}+1)/(B$8+2)')
        x.input(ws, f'E{r}', f'=(C{r}+1)/(C$8+2)')
        x.text(ws, f'F{r}', f1, border=True); x.text(ws, f'G{r}', f2, border=True)
        x.formula(ws, f'H{r}', f'=IF(F{r}=1,D{r},1-D{r})'); x.formula(ws, f'I{r}', f'=IF(F{r}=1,E{r},1-E{r})')
        x.formula(ws, f'J{r}', f'=IF(G{r}=1,D{r},1-D{r})'); x.formula(ws, f'K{r}', f'=IF(G{r}=1,E{r},1-E{r})')
    x.text(ws, 'A8', 'Emails in the class', border=True); x.text(ws, 'B8', 40, border=True); x.text(ws, 'C8', 60, border=True)
    x.text(ws, 'A9', 'Prior', border=True); x.formula(ws, 'B9', '=B8/(B8+C8)'); x.formula(ws, 'C9', '=C8/(B8+C8)')
    items = [('Email 1 spam score = prior × product of the spam factors', '=B9*PRODUCT(H4:H6)', 12, 0.12166, 0.00005), ('Email 1 ham score', '=C9*PRODUCT(I4:I6)', 13, 0.00055, 0.00005),
             ('Email 1 posterior probability of spam', '=B12/(B12+B13)', 14, 0.9955, 0.0001), ('Email 2 spam score', '=B9*PRODUCT(J4:J6)', 15, 0.01644, 0.00005), ('Email 2 ham score', '=C9*PRODUCT(K4:K6)', 16, 0.03332, 0.00005),
             ('Email 2 posterior probability of spam', '=B15/(B15+B16)', 17, 0.3304, 0.0001),
             ('CHANGE: email 1 posterior with no smoothing (plain counts / class size)', '=(B9*(B4/B8)*(B5/B8)*(1-B6/B8))/((B9*(B4/B8)*(B5/B8)*(1-B6/B8))+(C9*(C4/C8)*(C5/C8)*(1-C6/C8)))', 19, 1.0, 0.0001)]
    for lab, f, r, exp, tol in items:
        x.text(ws, f'A{r}', lab, wrap=True)
        x.input(ws, f'B{r}', f)
        x.check(lab, f'=NaiveBayes!B{r}', exp, tol)
        ws.row_dimensions[r].height = 30
    x.text(ws, 'A21', 'Long emails: add logarithms in place of multiplying', bold=True)
    items = [('Email 1: LN of the spam score', '=LN(B12)', 22, -2.1066, 0.0005), ('Email 1: LN of the ham score', '=LN(B13)', 23, -7.5123, 0.0005),
             ('Email 1 posterior from the logs: 1 / (1 + EXP(ln ham - ln spam)), the two-class softmax', '=1/(1+EXP(B23-B22))', 24, 0.9955, 0.0001),
             ('CHANGE: email 1 posterior with a spam prior of 0.01 (a rare-spam mailbox)', '=0.01*PRODUCT(H4:H6)/(0.01*PRODUCT(H4:H6)+0.99*PRODUCT(I4:I6))', 25, 0.7714, 0.0005)]
    for lab, f, r, exp, tol in items:
        x.text(ws, f'A{r}', lab, wrap=True)
        x.input(ws, f'B{r}', f)
        x.check(lab, f'=NaiveBayes!B{r}', exp, tol)
        ws.row_dimensions[r].height = 30
    x.check('Smoothed likelihood of free in spam', '=NaiveBayes!D4', 0.6905, 0.0001)
    x.check('Smoothed likelihood of prize in ham', '=NaiveBayes!E5', 0.0161, 0.0001)
    return x
