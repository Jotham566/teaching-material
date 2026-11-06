"""Paper-exercise worksheets for Sessions 1 to 11, added to the Learner Workbook by make_docs.py.

The sessions' hands-on slides and workbook steps refer to 'the worksheet'. The data below are copied from the facilitator prep lines of
content/sNN.py and from demo_runs/ (s03 results.json, s09 handbook_questions_key.csv, s10 practice_answer_sheet.md). If a session's numbers change,
change them here too. Each function writes into the Word document d and returns nothing.
"""
import csv
import json
import re
from pathlib import Path

from docx_kit import *  # noqa: F401,F403

W = CONTENT_CM
DEMO = Path(__file__).resolve().parent.parent / 'demo_runs'


def _blank(n):
    return [''] * n


def _lines(d, k=3):
    for _ in range(k):
        para(d, '_' * 78, 10, color='A6A6A6', after=4)


def s01(d):
    para(d, 'Five payments, one checklist. Tick each question 1 (yes) or 0 (no), multiply by its weight, add, and flag at 4 or more.', 10, after=4)
    rows = [['P1', 'UGX 1,450,000', 'New', '14:00'], ['P2', 'UGX 85,000', 'New', '23:30'], ['P3', 'UGX 2,300,000', 'Known supplier', '10:00'],
            ['P4', 'UGX 60,000', 'Known supplier', '09:00'], ['P5', 'UGX 1,350,000', 'New', '22:00']]
    h2(d, 'Part 1: weights 3, 2 and 1')
    grid(d, [r + _blank(5) for r in rows], [1.2, 3.4, 3.0, 1.8, 2.0, 2.0, 2.0, 2.0],
         header=['', 'Amount', 'Payee', 'Time', 'Big x3', 'New x2', 'After hours x1', 'Total'], size=9.5, min_h=0.9, label_cols=(0,))
    para(d, 'Big amount means over UGX 1,200,000. After hours means outside 08:00 to 18:00. A person checks any payment that totals 4 or more.', 9, italic=True, color='595959', before=3, after=4)
    h2(d, 'Part 2: now give the big amount a weight of 4')
    grid(d, [[r[0], '', '', ''] for r in rows], [2.0, 4.0, 4.0, 7.4], header=['', 'New total', 'Flagged?', 'Changed from Part 1?'], size=9.5, min_h=0.8, label_cols=(0,))
    para(d, 'Would you accept this change? Why?', 10, before=6, after=2)
    _lines(d, 2)


def s02(d):
    para(d, 'Claim N is new. Decide whether it will be paid or queried by looking at the most similar past claims. One square across is UGX 100,000. One square up is 5 days to file. Distance by city blocks: squares across plus squares up.', 10, after=4)
    claims = [('A', 2, 1, 'paid'), ('B', 3, 2, 'paid'), ('C', 4, 1, 'paid'), ('D', 4, 5, 'queried'), ('E', 5, 6, 'queried'),
              ('F', 7, 3, 'paid'), ('G', 6, 4, 'paid'), ('H', 8, 6, 'queried'), ('I', 7, 2, 'paid'), ('J', 9, 3, 'queried')]
    para(d, 'New claim N: 5 across, 4 up.', 10, True, after=3)
    grid(d, [[c, str(a), str(u), o, '', '', ''] for c, a, u, o in claims], [1.6, 2.4, 2.4, 2.6, 3.0, 2.6, 2.8],
         header=['Claim', 'Across', 'Up', 'Outcome', 'Squares across from N', 'Squares up from N', 'Distance'], size=9.5, min_h=0.75, label_cols=(0,))
    spacer(d, 6)
    grid(d, [['Vote of the 3 nearest', '', 'Vote of the nearest 1', ''], ['Claims my straight line gets wrong', '', 'Does the answer change?', '']], [5.0, 3.7, 5.0, 3.7], size=9.5, min_h=0.9, label_cols=(0, 2))
    para(d, 'Draw the claims on squared paper (across along the bottom, up along the side), mark paid and queried differently, circle the 3 nearest to N, and draw one straight line that best separates paid from queried.', 9, italic=True, color='595959', before=4)


def s03(d):
    para(d, 'Twenty invoices from the test set of the recorded run. The model flags an invoice at a score of 0.20 or more. Late means paid late in fact.', 10, after=4)
    cases = json.loads((DEMO / 's03' / 'results.json').read_text())['cases20']
    rows = [[str(c['case']), c['invoice'], f"{c['amount_ugx']:,}", f"{c['score']:.2f}", 'Late' if c['really_late'] else 'On time', '', ''] for c in cases]
    grid(d, rows, [1.2, 2.4, 3.0, 2.0, 2.4, 3.2, 3.2], header=['No.', 'Invoice', 'Amount, UGX', 'Score', 'In fact', 'Flagged at 0.20? (Y/N)', 'Box (TP FP FN TN)'], size=9, min_h=0.62, label_cols=(0,), hdr_size=8)


def s03b(d):
    h2(d, 'The four boxes and two measures', before=2)
    grid(d, [['Caught (flagged and late)', '', 'False alarms (flagged, on time)', ''], ['Missed (not flagged, late)', '', 'Rightly cleared (not flagged, on time)', '']], [5.2, 3.5, 5.2, 3.5], size=9.5, min_h=1.0, label_cols=(0, 2))
    para(d, 'The four numbers add up to 20.  Precision = caught / flagged = ______.   Recall = caught / really late = ______.', 10, before=6, after=6)
    h2(d, 'Move the line')
    grid(d, [['0.50', '', '', '', ''], ['0.20', '', '', '', ''], ['0.15', '', '', '', '']], [2.6, 3.4, 3.4, 4.0, 4.0], header=['Line', 'Flagged', 'Caught', 'Precision', 'Recall'], size=10, min_h=0.9, label_cols=(0,))
    para(d, 'Which line would you choose, and why?', 10, before=6, after=2)
    _lines(d, 2)


def s04(d):
    para(d, 'Three toy arrows, drawn from the starting point (0, 0). A is 3 across and 4 up. B is 3 across and 1 up. C is 6 across and 0 up. Mark them on squared paper.', 10, after=4)
    grid(d, [['A', '3', '4', '5'], ['B', '3', '1', '3.16'], ['C', '6', '0', '6']], [2.0, 3.0, 3.0, 4.0], header=['Arrow', 'Across', 'Up', 'Length'], size=10, min_h=0.7, label_cols=(0,))
    spacer(d, 6)
    grid(d, [[p, '', '', '', ''] for p in ('A with B', 'A with C', 'B with C')], [3.0, 3.6, 3.6, 3.6, 3.6],
         header=['Pair', 'Straight line', 'City blocks', 'Agreement score', 'Cosine'], size=10, min_h=1.0, label_cols=(0,))
    para(d, 'Agreement score: multiply the across numbers, multiply the up numbers, add. Cosine: agreement score divided by (length of the first arrow x length of the second).', 9, italic=True, color='595959', before=4, after=4)
    para(d, 'Which pair does each measure call closest? ______________________________', 10, before=4, after=4)
    h2(d, 'Three searches from my own work')
    grid(d, [['', '', '', ''] for _ in range(3)], [3.6, 6.0, 3.9, 3.9], header=['Formal term', 'Plain description (none of its words)', 'Word search finds it?', 'Meaning search finds it?'], size=9.5, min_h=1.0)


def s05(d):
    para(d, 'Turn scores into percentages. Raise 2.72 to the score, add the three answers, and divide each answer by the total. Scores: days 3, weeks 2, minutes 0.', 10, after=4)
    h2(d, 'Temperature 1 (scores as they are)')
    grid(d, [['days', '3', '', ''], ['weeks', '2', '', ''], ['minutes', '0', '', '']], [4.0, 3.0, 5.0, 5.4], header=['Piece', 'Score', '2.72 to the score', 'Share of the total'], size=10, min_h=0.8, label_cols=(0,))
    h2(d, 'Temperature 2 (divide each score by 2 first)')
    grid(d, [['days', '1.5', '', ''], ['weeks', '1', '', ''], ['minutes', '0', '', '']], [4.0, 3.0, 5.0, 5.4], header=['Piece', 'Score / 2', '2.72 to the score', 'Share of the total'], size=10, min_h=0.8, label_cols=(0,))
    para(d, 'Which setting gives the safer, more repeatable answer, and which gives more variety?', 10, before=6, after=2)
    _lines(d, 2)


def s06(d):
    para(d, 'Read the printed model card (GPT-2, from its Hugging Face page) and answer four questions with a line from the card.', 10, after=4)
    grid(d, [[q, '', ''] for q in ('What is the licence, and may you use it at work?', 'How big is it, and what was it trained on?', 'What does the maker say it should not be used for?', 'What is missing that you would want to know?')],
         [6.4, 8.0, 3.0], header=['Question', 'Line from the card', 'Found? (Y/N)'], size=9.5, min_h=1.5, label_cols=(0,))


def s07(d):
    para(d, 'Memory for the numbers inside a model = number of numbers x bytes for each number. 1 billion numbers at 1 byte is 1 gigabyte (GB).', 10, after=4)
    grid(d, [['7 billion at 2 bytes (16-bit)', '7 x 2 =', ''], ['7 billion at half a byte (4-bit)', '7 x 0.5 =', ''], ['70 billion at 2 bytes (16-bit)', '70 x 2 =', ''], ['70 billion at half a byte (4-bit)', '70 x 0.5 =', '']],
         [7.0, 4.0, 6.4], header=['Model', 'Sum', 'GB'], size=10, min_h=0.9, label_cols=(0,))
    para(d, 'Decision sheet: one task of mine and its data, rent, host or own, my reason, and the licence question I would ask first.', 10, before=6, after=3)
    grid(d, [[l, ''] for l in ('Task and the data it touches', 'Route (rent, host or own)', 'Reason', 'First licence question')], [5.4, 12.0], size=9.5, min_h=1.1, label_cols=(0,))


def s08(d):
    para(d, 'Weak prompt: "Reply to this customer complaint." Rewrite it using the five parts. Customer to answer: Mercy Atim, whose jerrycans of oil leaked for the third time (an NVF example).', 10, after=4)
    grid(d, [[p, ''] for p in ('Role and reader', 'Context (what happened, which customer)', 'One example, or "none yet"', 'Format and length', 'Checks, and what to say when unsure')], [5.4, 12.0], header=['Part', 'My sentence'], size=9.5, min_h=1.3, label_cols=(0,))
    h2(d, 'Prompt log')
    grid(d, [['', '', '', '', ''] for _ in range(3)], [2.0, 6.0, 3.0, 3.2, 3.2], header=['Version', 'What changed', 'Runs', 'How many right', 'Who checked'], size=9, min_h=0.9)


def s09(d):
    para(d, 'Choose a rung for each request: P (prompt), R (retrieve) or F (fine-tune). Give one line of reason.', 10, after=4)
    reqs = ['Summarise one supplier email.', 'Answer staff questions from a handbook that changes each quarter.', 'Every customer reply ends with the house sign-off.',
            'Check a price against one pasted quote.', 'Answer questions about 400 contracts.', 'Draft replies in the Sales Manager voice from 200 past emails.']
    grid(d, [[chr(97 + i), r, '', ''] for i, r in enumerate(reqs)], [1.0, 7.4, 1.8, 7.2], header=['', 'Request', 'P, R or F', 'Reason'], size=9.5, min_h=1.0, label_cols=(0,))
    para(d, 'The ten-question test I would run first on the cheapest rung: write it on the Session 10 test-set page or on paper.', 9, italic=True, color='595959', before=4)


def s10(d):
    para(d, 'Mark each answer on the practice sheet against the key: right, wrong, missed or invented. The key is handed out in class.', 10, after=4)
    qs = {r['id']: r['question'] for r in csv.DictReader(open(DEMO / 's09' / 'handbook_questions_key.csv', encoding='utf-8'))}
    ans = dict(re.findall(r'^(Q\d\d)\.\s*(.*?)\s*$', (DEMO / 's10' / 'practice_answer_sheet.md').read_text(encoding='utf-8'), re.M))
    rows = [[k, qs.get(k, ''), ans[k], '', ''] for k in sorted(ans)]
    grid(d, rows, [1.1, 6.0, 5.0, 2.8, 2.5], header=['Q', 'Question', 'Sheet says', 'Key says', 'Mark'], size=8.5, min_h=0.9, label_cols=(0,), hdr_size=8)
    para(d, 'Right ___   Wrong ___   Missed ___   Invented ___.  Which error would cost most, and why?', 10, before=6, after=2)
    _lines(d, 1)
    h2(d, 'My ten-question test set')
    grid(d, [['Q%d' % (i + 1), '', '', '', '', ''] for i in range(10)], [1.2, 5.2, 3.2, 2.4, 2.6, 2.8], header=['Id', 'Question', 'Known answer', 'Source', 'Run 1 / Run 2', 'Cost of a wrong answer'], size=8.5, min_h=0.8, label_cols=(0,), hdr_size=8)
    para(d, 'Two of the ten questions should have no answer in the document. The right answer to those is "not stated".', 9, italic=True, color='595959', before=3)


def s11(d):
    para(d, 'Fill the four rows for the mailbox assistant, then name the row that stops each risky mail. The printed mails M01, M03 and M08 come from the demonstration mailbox (all invented).', 10, after=4)
    grid(d, [[r, '', '', ''] for r in ('Read', 'Write', 'Send', 'Spend')], [2.4, 5.0, 5.0, 5.0], header=['Row', 'It may', 'A person approves', 'It must never'], size=9.5, min_h=1.2, label_cols=(0,))
    spacer(d, 6)
    grid(d, [[m, '', '', ''] for m in ('M01', 'M03', 'M08')], [2.0, 5.0, 5.0, 5.4], header=['Mail', 'Plan', 'Act (one tool)', 'Observe, and where the loop must stop'], size=9.5, min_h=1.5, label_cols=(0,))
    para(d, 'Approvals a week x minutes each = ______ minutes a week.   Owner: ____________   Off switch: ____________', 10, before=6)


# which sessions get a worksheet page after their workbook page, and the title
SHEETS = {1: ('Score five payments', [s01]), 2: ('Find the nearest claims', [s02]), 3: ('Twenty cases and the four boxes', [s03, s03b]), 4: ('Four distances for three arrows', [s04]),
          5: ('A softmax and a temperature by hand', [s05]), 6: ('Read a model card', [s06]), 7: ('The memory sum and the decision sheet', [s07]), 8: ('The five-part prompt', [s08]),
          9: ('Choose the rung', [s09]), 10: ('Score an answer sheet and write a test set', [s10]), 11: ('The boundary sheet and the loop', [s11])}
