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


def _new_page(d):
    p = d.add_paragraph(); fmt(p, 0, 0)
    p.paragraph_format.page_break_before = True
    p.paragraph_format.line_spacing = Pt(1)


def s01(d):
    para(d, 'Part 1: a neuron prices a house. Weighted sum = floor area x 2 + bedrooms x 10. Add the bias of 30 to get the price in UGX million.', 10, after=3)
    houses = [('A', 80, 3), ('B', 50, 2), ('C', 120, 4), ('D', 65, 2), ('E', 100, 3)]
    grid(d, [[h, str(a), str(b), '', '', '30', '', ''] for h, a, b in houses], [1.5, 2.2, 2.0, 2.2, 2.4, 1.6, 2.7, 2.8],
         header=['House', 'Floor area (m\u00b2)', 'Beds', 'Area x 2', 'Bedrooms x 10', 'Bias', 'Price (UGX m)', 'Price if a bedroom is 15'], size=9.5, min_h=0.75, label_cols=(0,), hdr_size=8)
    para(d, 'Now make each bedroom worth 15 instead of 10. By how much does every price move? ______________', 10, before=4, after=6)
    para(d, 'Part 2: a neuron decides on an umbrella. Weighted sum = 0.1 x chance of rain (%) + 0.05 x minutes outside. Total = weighted sum + bias. Activation function (step): a total above 0 gives 1, carry an umbrella.', 10, after=3)
    days = [('Mon', 70, 30), ('Tue', 20, 30), ('Wed', 50, 60), ('Thu', 40, 20), ('Fri', 60, 10)]
    grid(d, [[x, str(r), str(m), '', '', '', '', '', '', ''] for x, r, m in days], [1.3, 1.5, 1.6, 1.7, 1.8, 1.8, 1.8, 1.6, 1.8, 1.5],
         header=['Day', 'Rain %', 'Minutes', '0.1 x rain', '0.05 x minutes', 'Weighted sum', 'Total, bias -6', 'Carry? Y/N', 'Total, bias -7', 'Carry? Y/N'], size=9.5, min_h=0.72, label_cols=(0,), hdr_size=7.5)
    para(d, 'Which day changed when the bias went from -6 to -7? ________   What do a weight and a bias do, in one sentence?', 10, before=5, after=2)
    _lines(d, 2)


def s02(d):
    para(d, 'Estimate the price of the new house N from the sold houses most like it. One square across is 20 m\u00b2 of floor area, so N (5 across, 4 up) is 100 m\u00b2. One square up is 1 km to the town centre, so N is 4 km out. Distance is the Manhattan count: squares across plus squares up.', 10, after=4)
    sold = [('A', 2, 1, 80), ('B', 3, 2, 95), ('C', 4, 1, 120), ('D', 4, 5, 100), ('E', 5, 6, 115),
            ('F', 7, 3, 175), ('G', 6, 4, 150), ('H', 8, 6, 180), ('I', 7, 2, 180), ('J', 9, 3, 220)]
    grid(d, [[h, str(a), str(u), '', str(pr)] for h, a, u, pr in sold], [2.0, 3.0, 3.0, 5.0, 4.4],
         header=['House', 'Across', 'Up', 'Distance (across + up from N)', 'Price (UGX million)'], size=10, min_h=0.75, label_cols=(0,))
    spacer(d, 6)
    grid(d, [['k = 3: the three nearest houses', '', 'Average of their prices', ''], ['k = 1: the nearest house', '', 'Price estimate', ''],
             ['Gap between the two estimates', '', 'Which would I quote to a buyer?', '']], [5.0, 3.7, 5.0, 3.7], size=9.5, min_h=0.9, label_cols=(0, 2))
    para(d, 'Draw the houses on squared paper (across along the bottom, up along the side), write each price beside its point, and circle the 3 nearest to N.', 9, italic=True, color='595959', before=4)


def s03a(d):
    h2(d, 'Warm-up (optional): a smoke alarm', before=0)
    para(d, 'In 1,000 events the alarm gave these results (numbers invented for the lesson). Fill the measures in the margin.', 10, after=3)
    grid(d, [['', 'Alarm rings', 'Alarm silent'], ['Real fire', 'TP  16', 'FN  4'], ['No fire', 'FP  34', 'TN  946']], [4.0, 4.5, 4.5], size=10, min_h=0.55, label_cols=(0,))
    spacer(d, 5)
    grid(d, [['Accuracy = (TP + TN) / 1,000', '', 'Precision = TP / (TP + FP)', ''], ['Recall = TP / (TP + FN)', '', 'F1 = 2 x precision x recall / (precision + recall)', ''],
             ['An alarm that never rings: accuracy', '', 'An alarm that never rings: recall', '']], [5.2, 3.0, 6.0, 3.2], size=9.5, min_h=0.6, label_cols=(0, 2))


def s03(d):
    h2(d, 'The twenty cases', before=6)
    para(d, 'Twenty invoices from the recorded run. Flag an invoice at a score of 0.20 or more. Late means paid late in fact.', 10, after=4)
    cases = json.loads((DEMO / 's03' / 'results.json').read_text())['cases20']
    rows = [[str(c['case']), c['invoice'], f"{c['amount_ugx']:,}", f"{c['score']:.2f}", 'Late' if c['really_late'] else 'On time', '', ''] for c in cases]
    grid(d, rows, [1.2, 2.4, 3.0, 2.0, 2.4, 3.2, 3.2], header=['No.', 'Invoice', 'Amount, UGX', 'Score', 'In fact', 'Flagged? (Y/N)', 'Cell (TP FP FN TN)'], size=9, min_h=0.42, label_cols=(0,), hdr_size=8)


def s03b(d):
    h2(d, 'The confusion matrix and two measures', before=2)
    grid(d, [['', 'Flagged', 'Not flagged'], ['In fact late', 'TP (true positive)', 'FN (false negative)'], ['In fact on time', 'FP (false positive)', 'TN (true negative)']], [4.4, 6.5, 6.5], size=9.5, min_h=0.95, label_cols=(0,))
    para(d, 'The four counts add up to 20.  Precision = TP / (TP + FP) = ______.   Recall = TP / (TP + FN) = ______.', 10, before=6, after=6)
    h2(d, 'Move the threshold')
    grid(d, [['0.50', '', '', '', ''], ['0.20', '', '', '', ''], ['0.15', '', '', '', '']], [2.6, 3.4, 3.4, 4.0, 4.0], header=['Threshold', 'Flagged', 'TP', 'Precision', 'Recall'], size=10, min_h=0.9, label_cols=(0,))
    para(d, 'Which threshold would you choose, and why?', 10, before=6, after=2)
    _lines(d, 2)


def s04(d):
    para(d, 'Four measures of closeness between two vectors. Euclidean distance: square root of (gap1 squared + gap2 squared). Manhattan distance: size of gap1 + size of gap2. Dot product: first x first + second x second. Cosine similarity: dot product / (length of the first x length of the second).', 9.5, after=4)
    h2(d, 'Warm-up (optional): three friends rate two films', before=2)
    para(d, 'Ana (3, 4), Ben (6, 8), Chloe (4, 3). Lengths: Ana 5, Ben 10, Chloe 5.', 9.5, after=3)
    grid(d, [[m, '', ''] for m in ('Euclidean distance', 'Manhattan distance', 'Dot product', 'Cosine similarity')], [6.0, 5.7, 5.7], header=['Measure', 'Ana to Ben', 'Ana to Chloe'], size=10, min_h=0.7, label_cols=(0,))
    h2(d, 'Three viewers')
    para(d, 'A is 3 across and 4 up. B is 3 across and 1 up. C is 6 across and 0 up. Lengths: A 5, B 3.16, C 6. Mark them on squared paper and draw an arrow from (0, 0) to each.', 9.5, after=3)
    grid(d, [[m, '', '', ''] for m in ('Euclidean distance', 'Manhattan distance', 'Dot product', 'Cosine similarity')], [5.4, 4.0, 4.0, 4.0], header=['Measure', 'A to B', 'A to C', 'B to C'], size=10, min_h=0.85, label_cols=(0,))
    para(d, 'Which pair does each measure call closest? Smaller distance, bigger dot product or cosine = closer.  ____________', 10, before=4, after=4)
    h2(d, 'Three searches from my own work')
    grid(d, [['', '', '', ''] for _ in range(3)], [3.6, 6.0, 3.9, 3.9], header=['Formal term', 'Plain description (none of its words)', 'Word search finds it?', 'Meaning search finds it?'], size=9.5, min_h=0.9)


def s05(d):
    para(d, 'Turn logits into probabilities with softmax. Raise 2.72 to each logit, add the three answers, and divide each answer by the total. The temperature divides the logits first.', 10, after=4)
    h2(d, 'Temperature 1 (logits as they are)')
    grid(d, [['days', '3', '', ''], ['weeks', '2', '', ''], ['minutes', '0', '', ''], ['Total', '', '', '']], [4.0, 3.0, 5.0, 5.4], header=['Token', 'Logit', '2.72 to the logit', 'Probability'], size=10, min_h=0.8, label_cols=(0,))
    h2(d, 'Temperature 2 (divide each logit by 2 first)')
    grid(d, [['days', '1.5', '', ''], ['weeks', '1', '', ''], ['minutes', '0', '', ''], ['Total', '', '', '']], [4.0, 3.0, 5.0, 5.4], header=['Token', 'Logit / 2', '2.72 to the logit', 'Probability'], size=10, min_h=0.8, label_cols=(0,))
    para(d, 'Which temperature gives the safer, more repeatable answer, and which gives more variety?', 10, before=6, after=2)
    _lines(d, 2)


def s06(d):
    para(d, 'Read the printed model card (GPT-2, from its Hugging Face page) and answer four questions with a line from the card.', 10, after=4)
    grid(d, [[q, '', ''] for q in ('What is the licence, and may you use it at work?', 'How big is it, and what was it trained on?', 'What does the maker say it should not be used for?', 'What is missing that you would want to know?')],
         [6.4, 8.0, 3.0], header=['Question', 'Line from the card', 'Found? (Y/N)'], size=9.5, min_h=1.5, label_cols=(0,))


def s07(d):
    para(d, 'Size = how many numbers x bytes for each number. 1 million bytes is 1 megabyte (MB). 1 billion bytes is 1 gigabyte (GB).', 10, after=3)
    h2(d, 'Part A: everyday sums', before=2)
    grid(d, [['A photo of 12 million pixels, 3 colour numbers each', '', '1', ''], ['One minute of music, about 5.3 million numbers', '5.3 million', '2', ''], ['A spreadsheet of 1 million numbers', '1 million', '8', '']],
         [7.0, 3.6, 2.8, 4.0], header=['Item', 'How many numbers', 'Bytes each', 'Size in MB'], size=9.5, min_h=0.85, label_cols=(0,))
    h2(d, 'Part B: the memory sum for a model')
    grid(d, [['1 billion', '', ''], ['7 billion', '', ''], ['70 billion', '', '']], [5.0, 6.2, 6.2], header=['Parameters', 'At FP16 (x 2 bytes), GB', 'At 4-bit (x 0.5 byte), GB'], size=10, min_h=0.85, label_cols=(0,))
    h2(d, 'Part C: the decision sheet')
    para(d, 'One task of mine and its data: rent, host or own, my reason, and the licence question I would ask first.', 10, after=3)
    grid(d, [[l, ''] for l in ('Task and the data it touches', 'Route (rent, host or own)', 'Reason', 'First licence question')], [5.4, 12.0], size=9.5, min_h=1.0, label_cols=(0,))


def s08(d):
    parts = ('Role', 'Context', 'Examples', 'Format', 'Constraints')
    para(d, 'Rewrite a weak prompt as five parts: role, context, examples, format and constraints (and what to say when unsure).', 10, after=3)
    h2(d, 'Part A: "Make dinner."', before=2)
    grid(d, [[p, ''] for p in parts], [3.6, 13.8], header=['Part', 'My sentence'], size=9.5, min_h=0.7, label_cols=(0,))
    h2(d, 'Part B: "Reply to this customer complaint."')
    para(d, 'Customer: Mercy Atim, whose jerrycans of oil leaked for the third time (a Nile Valley Foods example).', 9.5, after=3)
    grid(d, [[p, ''] for p in parts], [3.6, 13.8], header=['Part', 'My sentence'], size=9.5, min_h=0.7, label_cols=(0,))
    h2(d, 'Part C: label three mobile money SMS')
    grid(d, [['"You have received UGX 20,000 from Mary."', 'Money in'], ['"You have sent UGX 50,000 to Peter."', 'Money out'], ['"You have received UGX 8,000 from John."', '']],
         [11.4, 6.0], header=['SMS (the first two are the examples)', 'Label'], size=9.5, min_h=0.65, label_cols=(0,))
    _new_page(d)
    h2(d, 'Part D: prompt log', before=0)
    grid(d, [['', '', '', '', ''] for _ in range(3)], [2.6, 5.4, 1.8, 3.0, 4.6], header=['Version', 'What changed', 'Runs', 'How many right', 'Next change'], size=9.5, min_h=0.9)
    h2(d, 'Part E: my evaluation set of three cases')
    para(d, 'Three cases for which I know the right answer, then the result of one run.', 9.5, after=3)
    grid(d, [['Case %d' % (i + 1), '', '', '', ''] for i in range(3)], [2.2, 5.2, 4.0, 3.8, 2.2], header=['Case', 'Input', 'Known answer', 'Result of run 1', 'Right? Y/N'], size=9.5, min_h=1.3, label_cols=(0,))
    para(d, 'Who checks the figures before I use the answer? ______________________________', 10, before=6)


def s09(d):
    para(d, 'Choose the method for each request: P (prompting), R (RAG, retrieval-augmented generation) or F (fine-tuning). Give one line of reason and the first test you would run.', 10, after=4)
    reqs = ['Summarise one supplier email.', 'Answer staff questions from a handbook that changes each quarter.', 'Every customer reply ends with the house sign-off.',
            'Check a price against one pasted quote.', 'Answer questions about 400 contracts.', 'Draft replies in the Sales Manager voice from 200 past emails.']
    grid(d, [[chr(97 + i), r, '', '', ''] for i, r in enumerate(reqs)], [0.9, 6.0, 1.9, 4.6, 4.0], header=['', 'Request', 'Method (P, R or F)', 'Reason (one line)', 'First test'], size=9.5, min_h=1.2, label_cols=(0,))
    para(d, 'The ten-question test I would run first on the cheapest method: write it on the Session 10 evaluation set page or on paper.', 9, italic=True, color='595959', before=4)


def s10(d):
    para(d, 'Mark each answer on the practice sheet against the ground truth: right, wrong, missed or invented. The key is handed out in class.', 10, after=4)
    qs = {r['id']: r['question'] for r in csv.DictReader(open(DEMO / 's09' / 'handbook_questions_key.csv', encoding='utf-8'))}
    ans = dict(re.findall(r'^(Q\d\d)\.\s*(.*?)\s*$', (DEMO / 's10' / 'practice_answer_sheet.md').read_text(encoding='utf-8'), re.M))
    rows = [[k, qs.get(k, ''), ans[k], '', ''] for k in sorted(ans)]
    rows.append(['', 'Count', 'Right ___  Wrong ___  Missed ___  Invented ___', '', ''])
    grid(d, rows, [1.1, 6.0, 5.0, 2.8, 2.5], header=['Q', 'Question', 'Sheet says', 'Ground truth', 'Mark'], size=8.5, min_h=0.85, label_cols=(0,), hdr_size=8)
    para(d, 'Which error would cost most, and why?', 10, before=6, after=2)
    _lines(d, 1)
    _new_page(d)
    h2(d, 'My ten-question evaluation set', before=0)
    grid(d, [['Q%d' % (i + 1), '', '', '', '', '', ''] for i in range(10)], [1.1, 4.4, 2.8, 2.0, 2.0, 2.0, 3.1], header=['Id', 'Question', 'Ground truth', 'Source', 'Run 1', 'Run 2', 'Cost of a wrong answer'], size=8.5, min_h=1.0, label_cols=(0,), hdr_size=8)
    para(d, 'Two of the ten questions should have no answer in the document. The right answer to those is "not stated".', 9, italic=True, color='595959', before=3)


def s11(d):
    para(d, 'Fill the four rows of the permissions table for the mailbox assistant (all mails in the demonstration mailbox are invented).', 10, after=3)
    grid(d, [[r, '', '', ''] for r in ('Read', 'Write', 'Send', 'Spend')], [2.0, 5.0, 5.2, 5.2], header=['Row', 'It may', 'A person approves', 'It must never'], size=9.5, min_h=1.0, label_cols=(0,))
    spacer(d, 5)
    grid(d, [['M02', 'Invoice with no purchase order', ''], ['M03', 'Credit of UGX 180,000', ''], ['M07', 'Price rise of 4 percent', ''], ['M08', 'An instruction hidden in a statement', '']],
         [2.0, 7.4, 8.0], header=['Mail', 'What it asks', 'Row that stops the assistant'], size=9.5, min_h=0.7, label_cols=(0,))
    h2(d, 'The agent loop for three mails')
    grid(d, [[m, '', '', ''] for m in ('M01', 'M03', 'M08')], [1.8, 4.4, 4.4, 6.8], header=['Mail', 'Plan', 'Act (one tool)', 'Observe, and where the loop must stop'], size=9.5, min_h=1.2, label_cols=(0,))
    para(d, 'Approvals a week x minutes each = ______ minutes a week.   Owner: ____________   Off switch: ____________', 10, before=6)


# which sessions get a worksheet page after their workbook page, and the title
SHEETS = {1: ('A neuron prices houses and decides on an umbrella', [s01]), 2: ('Estimate a house price from its nearest neighbours', [s02]), 3: ('A smoke alarm, twenty cases and the confusion matrix', [s03a, s03, s03b]),
          4: ('Four measures of closeness', [s04]), 5: ('A softmax and a temperature by hand', [s05]), 6: ('Read a model card', [s06]), 7: ('The memory sum and the decision sheet', [s07]),
          8: ('The five-part prompt', [s08]), 9: ('Choose the method', [s09]), 10: ('Score an answer sheet and write an evaluation set', [s10]), 11: ('The permissions table and the agent loop', [s11])}
