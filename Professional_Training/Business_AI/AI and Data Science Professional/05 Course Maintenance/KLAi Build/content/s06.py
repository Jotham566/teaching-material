"""Session 6: Decisions, repeats and functions (conditional statements, Boolean expressions, for loops with an accumulator, functions, edge cases, unit tests with assert).
Python lab, notebook in content/labs/s06_nb.py.

Every number and every piece of code output on a slide, in a note or in the notebook checks is computed in facts(): pandas reads the real Lakeside Mart orders,
and every snippet shown on a slide is run here (exec), so the output on the slide is the output Python gave.
"""
import contextlib
import io
import linecache
import traceback
from functools import lru_cache
from pathlib import Path

import pandas as pd

BUILD = Path(__file__).resolve().parents[1]
DATA = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'data'
CUSTOMERS = ['C0009', 'C0010', 'C0021', 'C1322', 'C0947', 'C0230']

FUNC = '''def loyalty_tier(spend_ugx):
    """Return Basic, Silver or Gold."""
    points = spend_ugx // 1000
    if points >= 6000:
        return "Gold"
    elif points >= 2000:
        return "Silver"
    else:
        return "Basic"'''

V1 = '''def tier_v1(spend_ugx):
    points = spend_ugx // 1000
    if points >= 2000:
        return "Silver"
    elif points >= 6000:
        return "Gold"
    else:
        return "Basic"'''


def n(x):
    return f'{int(x):,}'


def run_code(code, ns):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(code, '<cell>', 'exec'), ns)
    return buf.getvalue().rstrip('\n').split('\n')


def run_error(code, ns):
    """Run code that must fail. Returns (message, exception name)."""
    linecache.cache['<cell>'] = (len(code), None, code.splitlines(True), '<cell>')
    try:
        exec(compile(code, '<cell>', 'exec'), ns)
    except Exception as e:  # noqa: BLE001
        return (e.msg if isinstance(e, SyntaxError) else str(e)), type(e).__name__
    raise AssertionError('expected an error: ' + code)


@lru_cache(maxsize=None)
def facts():
    o = pd.read_csv(DATA / 'orders.csv')
    o['year'] = o.order_date.str[:4]
    o25 = o[(o.year == '2025') & o.customer_id.notna()]
    F = {}
    g = o25.groupby('customer_id').order_value_ugx
    F['orders_2025'] = {c: [int(v) for v in o25[o25.customer_id == c].order_value_ugx] for c in CUSTOMERS}
    F['totals'] = {c: sum(v) for c, v in F['orders_2025'].items()}
    for c in CUSTOMERS:
        assert F['totals'][c] == int(g.sum()[c])
    allt = g.sum()
    F['cust_2025'] = int(len(allt))
    F['n_silver_all'] = int((allt // 1000 >= 2000).sum())
    F['n_gold_all'] = int((allt // 1000 >= 6000).sum())
    ns = {}
    # the if / elif / else snippet
    F['code_if'] = 'points = 2450\nif points >= 6000:\n    tier = "Gold"\nelif points >= 2000:\n    tier = "Silver"\nelse:\n    tier = "Basic"\nprint(points, "points is", tier)'
    F['out_if'] = run_code(F['code_if'], ns)
    # comparison operators
    P = 2450
    F['cmp'] = [('points == 2450', '=A2=2450', 'Equal to', repr(P == 2450)), ('points != 2000', '=A2<>2000', 'Not equal to', repr(P != 2000)), ('points < 6000', '=A2<6000', 'Less than', repr(P < 6000)),
                ('points <= 2450', '=A2<=2450', 'Less than or equal to', repr(P <= 2450)), ('points > 2450', '=A2>2450', 'Greater than', repr(P > 2450)), ('points >= 2000', '=A2>=2000', 'Greater than or equal to', repr(P >= 2000))]
    F['and_2450'] = (P >= 2000 and P < 6000)
    F['and_6000'] = (6000 >= 2000 and 6000 < 6000)
    # loop over spends
    order = ['C0009', 'C1322', 'C0010', 'C0947', 'C0021']
    F['spends'] = [F['totals'][c] for c in order]
    F['code_loop'] = f'spends = {F["spends"]}\nfor spend in spends:\n    points = spend // 1000\n    print(spend, "UGX is", points, "points")'
    F['out_loop'] = run_code(F['code_loop'], ns)
    F['loop_rows'] = [(n(s), n(s // 1000)) for s in F['spends']]
    # accumulator, customer C1322
    F['acc_orders'] = F['orders_2025']['C1322']
    F['code_acc'] = f'orders = {F["acc_orders"]}\ntotal = 0\nfor value in orders:\n    total = total + value\nprint(total)'
    F['out_acc'] = run_code(F['code_acc'], {})
    run_ = 0
    F['acc_rows'] = [('start', '', '0')]
    for i, v in enumerate(F['acc_orders'], 1):
        run_ += v
        F['acc_rows'].append((str(i), n(v), n(run_)))
    assert run_ == F['totals']['C1322'] == int(F['out_acc'][0])
    # points function and tier function
    F['code_points'] = 'def loyalty_points(spend_ugx):\n    """UGX spent to points."""\n    points = spend_ugx // 1000\n    return points'
    exec(F['code_points'], ns)
    F['pts_call'] = f'loyalty_points({F["totals"]["C1322"]})'
    F['pts_val'] = str(eval(F['pts_call'], ns))
    F['code_func'] = FUNC + f'\n\nprint(loyalty_tier({F["totals"]["C1322"]}))\nprint(loyalty_tier({F["totals"]["C0009"]}))'
    F['out_func'] = run_code(F['code_func'], ns)
    exec(FUNC, ns)
    exec(V1, ns)
    lt, v1 = ns['loyalty_tier'], ns['tier_v1']
    # tests
    F['tests'] = [(0, 'Basic', 'Zero spend'), (1999999, 'Basic', 'One shilling below Silver'), (2000000, 'Silver', 'Exactly Silver'), (5999999, 'Silver', 'One shilling below Gold'), (6000000, 'Gold', 'Exactly Gold')]
    F['test_rows_ok'] = [[name, n(s), exp, lt(s)] for s, exp, name in F['tests']]
    F['test_status_ok'] = ['PASS' if lt(s) == exp else 'FAIL' for s, exp, _ in F['tests']]
    F['test_rows_v1'] = [[name, n(s), exp, v1(s)] for s, exp, name in F['tests']]
    F['test_status_v1'] = ['PASS' if v1(s) == exp else 'FAIL' for s, exp, _ in F['tests']]
    assert all(x == 'PASS' for x in F['test_status_ok'])
    F['v1_fails'] = F['test_status_v1'].count('FAIL')
    F['v1_7_5m'] = v1(7500000)
    F['lt_7_5m'] = lt(7500000)
    F['code_assert'] = ('assert loyalty_tier(0) == "Basic"\nassert loyalty_tier(1999999) == "Basic"\nassert loyalty_tier(2000000) == "Silver"\nassert loyalty_tier(5999999) == "Silver"\n'
                        'assert loyalty_tier(6000000) == "Gold"\nprint("All 5 tests pass")')
    F['out_assert'] = run_code(F['code_assert'], ns)
    F['assert_fail_msg'], _ = run_error('assert tier_v1(6000000) == "Gold"', ns)
    # apply to the six customers
    F['tiers'] = {c: lt(t) for c, t in F['totals'].items()}
    F['counts'] = {k: list(F['tiers'].values()).count(k) for k in ('Basic', 'Silver', 'Gold')}
    F['grand'] = sum(F['totals'].values())
    alt = {c: ('Basic' if v // 1000 < 2500 else 'Silver') for c, v in F['totals'].items()}
    F['alt_counts'] = (list(alt.values()).count('Basic'), list(alt.values()).count('Silver'))
    F['alt_changed'] = [c for c in F['totals'] if alt[c] != F['tiers'][c]]
    F['code_bridge'] = ("totals = {'C0009': %d, 'C1322': %d}\ncounts = {'Basic': 0, 'Silver': 0, 'Gold': 0}\nfor customer in totals:\n    tier = loyalty_tier(totals[customer])\n"
                        "    counts[tier] = counts[tier] + 1\nprint(counts)") % (F['totals']['C0009'], F['totals']['C1322'])
    F['out_bridge'] = run_code(F['code_bridge'], ns)
    # mistakes, run for real
    m1, e1 = run_error('points = 2450\nif points = 2000:\n    print("Silver")', {})
    m2, e2 = run_error('print(loyalty_tier("2,388,850"))', ns)
    m3, e3 = run_error('points = 2450\nif points >= 2000:\nprint("Silver")', {})
    F['mis_eq'] = (e1, m1)
    F['mis_type'] = (e2, m2)
    F['mis_indent'] = (e3, m3)
    F['no_return'] = run_code('def loyalty_points(spend_ugx):\n    points = spend_ugx // 1000\nprint(loyalty_points(2450000))', {})[0]
    F['clean_text'] = int('2,388,850'.replace(',', ''))
    assert F['clean_text'] == F['totals']['C1322']
    # the policy text
    pol = (DATA / 'policies' / 'loyalty_programme.txt').read_text()
    assert '1 point for every UGX 1,000' in pol.replace('\n', ' ') and '2,000 points' in pol and '6,000 points' in pol
    return F


def build():
    F = facts()
    T = F['totals']
    sess = dict(
        num=6, block='Module B: Python for data', short_title='Decisions, repeats and functions',
        title='Decisions, repeats and functions: if, for, and a tested function',
        question='How do we make Python decide and repeat, so we never copy a formula down thousands of rows?',
        outcomes=['Write a conditional statement with if, elif and else, using Boolean expressions with comparison and logical operators',
                  'Repeat steps with a for loop and an accumulator, and wrap steps in a function with a parameter and a return value',
                  'Test the function with test cases that include the edge cases (boundary values), using assert, and trace code by hand'],
        outcome_icons=['pin', 'gear', 'check'],
        outcome_note=('By the end of today you can make Python decide, with if, elif and else, and you can build the tests that go inside them from comparison and logical operators. '
                      'You can repeat steps with a for loop and keep a running total with an accumulator. You can wrap steps in a function with a parameter and a return value. '
                      'And you can test that function at its edge cases with assert, and trace code by hand to find a fault. We build one real rule, the Lakeside Mart loyalty tiers.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: picture, plain words, one example by hand'), (10, 'Break'), (45, 'Lab: predict, run, read, change'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: concepts first, then a Python notebook lab',
        plan_caption='Pictures and plain words first. Then you open the notebook. Then the tests and what you keep.',
        plan_note=('We have two hours. The first ten minutes bring back Session 5 and set the question for today. Then forty-five minutes of concepts, with laptops closed. '
                   'After a ten minute break you open a Colab notebook for a forty-five minute lab, where you write the loyalty tier function, test it at its edges, and use it on six customers. '
                   'The last ten minutes are an exit check and what you keep. The lab is where the learning sticks, so please protect that time.'),
        recall_from='Session 5',
        recall=[("An error ends with: NameError: name 'price' is not defined. Which line do you read first, and what does it tell you?", 'The last line. Python has nothing stored under the name price: check the spelling, or run the cell that creates it.'),
                ("What does '3200' + '8400' give in Python, and why?", "'32008400'. Both values are strings, so plus joins them. Convert them with int() first to add."),
                ('A list and a dictionary both hold several values. How do you find one value in each?', 'In a list by its index, counting from 0. In a dictionary by its key.')],
        words=[('Conditional statement (if, elif, else)', 'Code that runs one branch, chosen by a test that is True or False. It is the IF function written as code.'),
               ('Boolean expression', 'A test that gives True or False, built with comparison operators such as >= and logical operators such as and.'),
               ('Iteration (for loop)', 'Repeating the same steps for each item in a list. It is fill down written as code.'),
               ('Function (parameter, argument, return value)', 'A named set of steps. The parameter is the name for the value that comes in, the argument is the value you pass, and the return value is the answer.'),
               ('Edge case (boundary value) and test case', 'An edge case sits exactly where a rule changes. A test case pairs an input with the output you expect.')],
        word_icons=['pin', 'check', 'gear', 'calculator', 'flag'],
        words_note=('Five words for today. A conditional statement runs one branch of code, chosen by a test. A Boolean expression is that test, and it gives True or False. '
                    'Iteration means repeating steps for each item, which a for loop does. A function is a named set of steps with a parameter, an argument and a return value. '
                    'And an edge case is a value exactly where a rule changes, which a test case checks. Each word has a spreadsheet cousin.'),
        keep='Keep your saved notebook: the loyalty_tier function with its docstring, five test cases that pass, six customers sorted into tiers, and a fault you traced in a colleague\'s version.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab file', value='A tested function'), dict(label='Your test cases', value='Five, with the edge cases'), dict(label='Next session', value='pandas: load, look, filter')]),
        keep_title='Save your notebook to Drive, with its tested function',
        next='Session 7: pandas I, load, look and filter. We open a file of 30,229 orders and ask the first questions of it.', next_label='Next session',
        keep_note=('Before you go, save your notebook with File, then Save a copy in Drive. The tested loyalty_tier function is your keepsake from today. '
                   'You can paste it into any notebook, and the five test cases tell the next person that it works, including at the edges. Next session we meet pandas, where one line replaces most loops. '
                   'If anything was unclear today, write the question down and bring it.'),
        cover_note=('Welcome back. Last session you stored values and read error messages. So far your code has run straight down the page. '
                    'Today it learns to decide with if, to repeat with for, and to reuse steps in a function. You already do all three in a spreadsheet, with IF, fill down and a formula you name. '
                    'We write each one in Python beside its spreadsheet cousin, on one real rule: the Lakeside Mart loyalty tiers.'),
        use_at_work='Turn a business rule into a tested function that you can run on thousands of records.',
        slides=[])
    S = sess['slides']
    cust = {c: n(v) for c, v in T.items()}
    spends = F['spends']

    S.append(dict(kind='table', title='Answers to the three questions from Session 5', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in sess['recall']], widths=[5.2, 6.8], icons=['magnifier', 'question', 'grid'],
                  notes=('Here are the answers to the three warm-up questions. A traceback is read from its last line, which names the exception. For a NameError it says Python has nothing stored under that name, so check the spelling or run the cell that creates it. '
                         "Plus on two quoted prices joins them into the string 32008400 with no error, because both are strings. Convert with int first. "
                         'And you find an item in a list by its index, counting from zero, and in a dictionary by its key. Today the list carries customer spending, and a dictionary holds the orders of each customer. Which of the three did you find hardest?')))

    S.append(dict(kind='table', title='The rule we will code: the Lakeside Mart loyalty tiers',
                  headers=['Tier', 'Points in 12 months', 'UGX spent in 12 months'], rows=[['Basic', '0 to 1,999', 'Under 2,000,000'], ['Silver', '2,000 to 5,999', '2,000,000 to 5,999,999'], ['Gold', '6,000 or more', '6,000,000 or more']],
                  widths=[2.4, 4.4, 5.2], icons=['person', 'coin', 'flag'], note='1 point for every UGX 1,000 spent. Source: loyalty_programme.txt, one of the Lakeside Mart policy files.',
                  notes=('Here is the rule we code today. It comes from the Lakeside Mart loyalty programme policy. A customer who gives a phone number joins as Basic and earns one point for every thousand shillings spent. '
                         'Silver starts at two thousand points in twelve months, and Gold at six thousand. The last column turns points into shillings: two million for Silver, six million for Gold. '
                         'Keep those two numbers in mind. They are the boundaries where the rule changes, and the places where a function most often goes wrong. How would you write this rule as nested IFs in Excel?')))

    S.append(dict(kind='idea', title='A conditional statement chooses one branch: Python takes the first test that is True',
                  visual=dict(kind='ds_c_flowchart', start='points = 2450', tests=['points >= 6000', 'points >= 2000'], results=['Gold', 'Silver', 'Basic'], picked=1,
                              code=['if points >= 6000:', '    tier = "Gold"', 'elif points >= 2000:', '    tier = "Silver"', 'else:', '    tier = "Basic"']),
                  lead='Conditional statement: if, elif and else.',
                  points=['Tests run from the top. The first True branch runs.', 'elif means else if. else catches the rest.', 'The indent shows which lines belong to which test.'],
                  notes=('In Excel you decide with the IF function, and a third tier means one IF inside another. Python writes the same decision as a conditional statement: if, then elif, short for else if, then else. '
                         'The flowchart follows a customer with 2,450 points. The first test, 6,000 or more, is False, so Python moves down. The second test, 2,000 or more, is True, so the answer is Silver and Python skips the rest. '
                         'The order matters, because the first True branch wins. The indented lines belong to the test above them. Which test must come first if you swapped them?')))

    S.append(dict(kind='table', title='A Boolean expression is a test that gives True or False, built with comparison operators',
                  headers=['Python', 'Excel', 'Meaning', 'With points = 2450'], rows=[[a, b, c, d] for a, b, c, d in F['cmp']], widths=[3.0, 2.6, 3.6, 2.8], icons=['pin', 'cross', 'clock', 'tag', 'chart', 'check'],
                  note='One equals sign stores a value. The comparison equal to is two equals signs. Excel uses one for both jobs.',
                  notes=('A Boolean expression is a test that gives True or False, named after the mathematician George Boole. You build one with a comparison operator. '
                         'Two equals signs ask whether two values are equal, where Excel uses a single sign. Not equal is exclamation mark equals, where Excel writes less than, greater than. '
                         'The other four are the comparisons you know. With 2,450 points, the table shows each result, computed by Python. Notice that greater than or equal to 2,000 is True, and greater than 2,450 is False. Which of these would catch someone who spent exactly the boundary?')))

    S.append(dict(kind='idea', title='Logical operators and, or and not combine tests, like AND and OR in Excel',
                  visual=dict(kind='ds_c_logic', rows=[('A: points >= 2000', 2000, 8000, '#F1F1F1'), ('B: points < 6000', 0, 6000, '#F1F1F1'), ('A and B: both True', 2000, 6000, '#E0BE36')]),
                  lead='Logical operators: and, or, not.',
                  points=['and is True only when both tests are True.', f'2,450 points: A and B is {F["and_2450"]}. 6,000 points: it is {F["and_6000"]}.', 'or needs one True. not flips True and False.'],
                  notes=(f'Logical operators combine tests. The picture draws two tests along the points axis. Test A, 2,000 or more, is True from 2,000 upwards. Test B, below 6,000, is True up to 6,000. '
                         f'A and B is True only where both bars overlap, which is the gold band, and that is exactly the Silver tier. With 2,450 points it is {F["and_2450"]}. With exactly 6,000 points it is {F["and_6000"]}, because 6,000 is not below 6,000. '
                         'Or is True when at least one test is True, and not flips the answer. Excel has AND, OR and NOT for the same jobs. What would A or B give for 7,000 points?')))

    outi = F['out_if']
    S.append(dict(kind='code', title='Read the recipe: if, elif and else decide a tier', code=F['code_if'], output=outi,
                  reads=['The first test is False, so Python skips Gold.', 'The second test is True, so tier becomes Silver.', 'Python skips the else.', 'The indent and the colon mark each branch.', 'print runs once, whichever branch ran.'],
                  notes=(f'Read the recipe aloud with me. Points is stored as 2,450. The first test asks whether it is 6,000 or more. It is False, so the Gold line is skipped. The elif asks whether it is 2,000 or more. That is True, so tier becomes Silver, and Python skips the else. '
                         f'Notice the colon at the end of each test and the indent under it. They are part of the grammar. The last line, at the left edge, runs once whichever branch was taken. The output was produced by running this exact code here: {outi[0]}. What would print if points were 1,999?')))

    S.append(dict(kind='idea', title='A for loop repeats the same steps for each item, like fill down in a sheet',
                  visual=dict(kind='ds_c_loop', headers=['spend_ugx', 'points'], rows=[list(r) for r in F['loop_rows']], formula='=INT(A2/1000)', code=['for spend in spends:', '    points = spend // 1000']),
                  lead='Iteration: repeating steps for each item.',
                  points=['The for line takes one item at a time.', 'The indented lines run once per item.', '// keeps the whole part: one point per UGX 1,000.'],
                  notes=('In a spreadsheet you write a formula once and drag it down the column. That is fill down. Python does the same with a for loop, which is a form of iteration, repeating steps for each item in a list. '
                         'On the left is the column of spend, with the formula INT of A2 over a thousand filled down. On the right, the for line takes one spend at a time, and the indented line works out its points. '
                         f'The double slash keeps the whole part, so {n(spends[0])} shillings gives {n(spends[0] // 1000)} points. Five items or five thousand, the code stays the same. Why is that better than dragging a formula down?')))

    S.append(dict(kind='code', title='Read the recipe: a loop over five customer spends', code=F['code_loop'], output=F['out_loop'],
                  reads=['spends is a list of five 2025 totals from orders.csv.', 'The loop takes one spend at a time.', 'The indented lines run once for each item.', 'print shows the spend and its points.'],
                  notes=(f'Here is the loop on real numbers. These five totals are the 2025 order totals of five Lakeside customers, computed from orders dot csv. The loop takes one spend at a time, works out the points, and prints a line. '
                         f'So {n(spends[0])} gives {n(spends[0] // 1000)} points, and {n(spends[1])} gives {n(spends[1] // 1000)}. Nothing here decides a tier yet. Next we add a function that does. '
                         'These totals are small because orders dot csv is a five percent sample of till transactions, so real spending is much higher. What would you change to print the tier instead of the points?')))

    S.append(dict(kind='wide', title='An accumulator builds a running total inside a loop, like SUM or a running balance',
                  visual=dict(kind='ds_c_trace', code=F['code_acc'].split('\n'), headers=['Pass', 'value', 'total after the pass'], rows=[list(r) for r in F['acc_rows']], hl_rows=[len(F['acc_rows']) - 1]),
                  caption=f'Customer C1322 placed three orders in 2025. The accumulator ends at {n(T["C1322"])} UGX.',
                  notes=(f'This is a trace table. It follows the code one pass at a time. Customer C1322 made three orders in 2025. Before the loop, total starts at zero. '
                         f'That variable is the accumulator, a variable that collects a result as the loop goes round. Pass one adds {n(F["acc_orders"][0])}. Pass two adds {n(F["acc_orders"][1])}. Pass three adds {n(F["acc_orders"][2])}, and the total is {n(T["C1322"])}. '
                         'The pattern is always the same: start at zero, then total equals total plus value. Python also has a sum function, but the accumulator is the idea behind it. What would the accumulator start at if you wanted the largest value?')))

    S.append(dict(kind='idea', title='A function is a named set of steps: a parameter goes in and a return value comes out',
                  visual=dict(kind='ds_c_function', code=F['code_points'].split('\n'), call=F['pts_call'], returned=F['pts_val'],
                              parts=[(0, 'def names the function. spend_ugx is the parameter.'), (1, 'Docstring: one line saying what it does.'), (2, 'The body: indented lines that run when you call it.'), (3, 'return sends the answer back.')]),
                  lead='Function: a formula you name yourself.',
                  points=['Parameter: the name for the value that comes in.', 'Argument: the value you pass when you call it.', 'return sends the value back to the caller.'],
                  notes=(f'A function is a formula you name yourself. This one is called loyalty points. The def line gives the name and one parameter, spend ugx, which is the name for the value that comes in. The line in triple quotes is the docstring, a short note on what the function does. '
                         f'The indented lines are the body, and return sends the answer back. To use it you call it with an argument. Here the argument is {n(T["C1322"])}, and the return value is {F["pts_val"]}. '
                         'The parameter is the name inside the function, and the argument is the actual value. Why is a docstring useful for a colleague?')))

    S.append(dict(kind='code', title='Read the recipe: the loyalty_tier function', code=F['code_func'], output=F['out_func'],
                  reads=['def, the name and the parameter spend_ugx.', 'The docstring says what it does.', 'The body works out points, then tests Gold first.', 'return gives the tier back.', f'Two calls: {n(T["C1322"])} gives {F["out_func"][0]}, {n(T["C0009"])} gives {F["out_func"][1]}.'],
                  notes=(f'Here is the whole rule as one function. The def line names it and its parameter. The docstring says what it returns. The body turns spend into points with a double slash, then tests Gold first, Silver second, and Basic for everyone left. '
                         f'Each branch uses return, which sends the tier back to whoever called the function. The two calls at the bottom were run here. {n(T["C1322"])} shillings gives {F["out_func"][0]}, and {n(T["C0009"])} shillings gives {F["out_func"][1]}. '
                         'Notice that the function does not print. It returns. Why might returning be more useful than printing?')))

    S.append(dict(kind='steps', title='Write the function once, then call it for every customer',
                  steps=[dict(head='Totals', text='Accumulator in a loop', icon='coin'), dict(head='Loop', text='One customer at a time', icon='gear'), dict(head='Function', text='One tested rule', icon='flag'),
                         dict(head='Counts', text='Basic, Silver, Gold', icon='chart')], highlight=2,
                  caption='A loop repeats the work. A function holds the rule. Together they answer the question for six customers or six million.',
                  notes=('Now we put the loop and the function together. First an accumulator in a loop builds each customer total. Then a loop goes through the customers one at a time. '
                         'For each one it calls loyalty tier, the single tested rule, and gets a tier back. Finally we count how many customers fall in each tier. '
                         'The rule lives in one place. If the policy moves Silver to two thousand five hundred points, you change one line in one function and every result updates. How would that change work in a sheet with the IF copied in many cells?')))

    S.append(dict(kind='wide', title='An edge case (boundary value) sits exactly where the rule changes',
                  visual=dict(kind='ds_c_numline', top_note='Where the rule changes, test the value just below and the value exactly on the boundary',
                              bands=[(0, 2000000, 'Basic', 'under 2,000,000 UGX', '#FFFFFF'), (2000000, 6000000, 'Silver', '2,000,000 to 5,999,999 UGX', '#F1F1F1'), (6000000, 8000000, 'Gold', '6,000,000 UGX or more', '#E0BE36')],
                              edges=[(2000000, '1,999,999 gives Basic', '2,000,000 gives Silver'), (6000000, '5,999,999 gives Silver', '6,000,000 gives Gold')], bottom='Four edge cases, two at each boundary. Add zero as a fifth test case.'),
                  caption='Off-by-one error: writing > where the rule needs >=. Only the boundary value exposes it.',
                  notes=('An edge case, also called a boundary value, is an input exactly where a rule changes. The picture marks the two boundaries of our rule. At two million shillings the tier changes from Basic to Silver, and at six million from Silver to Gold. '
                         'Bugs hide here. If someone writes greater than where the rule needs greater than or equal to, the function passes every ordinary value and fails only the value exactly on the line. That slip has a name, the off-by-one error. '
                         'So test the value just below each boundary and the value exactly on it. Which value would you test for a boundary of 5,000?')))

    S.append(dict(kind='wide', title='A test case pairs an input with the expected output, and it passes or fails',
                  visual=dict(kind='ds_c_tests', headers=['Test case', 'spend_ugx', 'Expected', 'Got', 'Result'], rows=F['test_rows_ok'], status=F['test_status_ok']),
                  caption='Expected comes from the policy. Got is what the function returned.',
                  notes=('A test case is one input paired with the output you expect, worked out by hand from the policy before you run anything. '
                         'The table has five test cases for our function: zero spend, one shilling below Silver, exactly Silver, one shilling below Gold, and exactly Gold. Each one compares the expected tier with what the function returned. '
                         'All five pass. A small set of tests like this for one function is called a set of unit tests. Writing the expected column first, from the policy, is what makes the test honest. Why must the expected column come from the policy and not from the code?')))

    S.append(dict(kind='code', title='Read the recipe: assert stops with an AssertionError when a test fails', code=F['code_assert'], output=F['out_assert'],
                  reads=['assert checks that a test is True.', 'If it is True, Python carries on silently.', 'If it is False, Python stops with an AssertionError.', 'Five asserts, five test cases.', 'The last line prints only if all five passed.'],
                  notes=(f'The assert statement is how you run a test in code. It says: this must be True. If it is True, Python carries on without a word. If it is False, Python stops with an AssertionError, and the notebook shows you which line failed. '
                         f'Here are our five test cases written as asserts. Nothing appears until the last line, which prints that all five tests pass. That silence is the good news. '
                         f'If I assert that the buggy version returns Gold for six million, Python stops and the last line of the error is an AssertionError. What does silence from an assert tell you?')))

    S.append(dict(kind='wide', title='Trace code by hand to find a fault: tier_v1 tests Silver before Gold',
                  visual=dict(kind='ds_c_trace', code=V1.split('\n'), headers=['Step', 'Line', 'What Python does'], rows=[['1', '2', 'points = 7500000 // 1000 stores 7500'], ['2', '3', '7500 >= 2000 is True'], ['3', '4', 'return "Silver": the function ends'],
                                                                                                                          ['4', 'none', 'The Gold test on line 5 is never reached']], hl_rows=[3]),
                  caption=f'A colleague\'s tier_v1 returns {F["v1_7_5m"]} for 7,500,000 UGX. The correct tier is {F["lt_7_5m"]}.',
                  notes=(f'Reading and tracing someone else\'s code is a daily job. Here is a colleague\'s function, tier v1. Trace it with 7,500,000 shillings. Line two stores 7,500 points. Line three asks whether 7,500 is 2,000 or more. It is True, so line four returns Silver and the function ends. '
                         f'The Gold test on line five is never reached. So a customer who spent seven and a half million is called {F["v1_7_5m"]}. The fault lies in the order of the branches, and every number in the code is correct. '
                         'Tracing with one value by hand found it in four steps. What is the rule for ordering the branches?')))

    S.append(dict(kind='wide', title=f'The same test cases catch the fault: tier_v1 fails {F["v1_fails"]} of 5',
                  visual=dict(kind='ds_c_tests', headers=['Test case', 'spend_ugx', 'Expected', 'Got', 'Result'], rows=F['test_rows_v1'], status=F['test_status_v1']),
                  caption='A failed test shows the input, the expected output and the actual output.',
                  notes=(f'Run the same five test cases against tier v1, and the fault shows up at once. {"one of the five test cases fails" if F["v1_fails"] == 1 else str(F["v1_fails"]) + " of the five test cases fail"}, and the failing row tells you the input, the expected output and what the function actually returned. '
                         'Only the exact Gold boundary case fails, because the Silver test catches everything above two million first. That points straight at the order of the branches. '
                         'This is why you write test cases before you trust a function, and why you keep them afterwards: if someone edits the function next year, the tests tell them at once whether it still works. '
                         'Which of the five test cases found the fault first?')))

    S.append(dict(kind='table', title='Four common mistakes, and the message Python gives for each',
                  headers=['What you wrote', 'What Python says', 'Fix'],
                  rows=[['if points = 2000:', f'{F["mis_eq"][0]}: {F["mis_eq"][1]}', 'Use == to compare.'], ['A function with no return line', f'print(...) shows {F["no_return"]}', 'Add return, so the caller gets the value.'],
                        ['A spend written as text, 2,388,850', f'{F["mis_type"][0]}: {F["mis_type"][1]}', 'Remove the commas and convert with int().'], ['An if with nothing indented under it', f'{F["mis_indent"][0]}: {F["mis_indent"][1]}', 'Indent the lines that belong to the if.']],
                  widths=[3.4, 5.2, 3.4], icons=['cross', 'question', 'doc', 'pen'], note='Messages copied from real runs. Newer Python versions may word a message slightly differently.',
                  notes=('Four mistakes you will make this week, with the real message for each. One equals sign inside an if is a SyntaxError, and the message even suggests two equals signs. '
                         'A function with no return line quietly gives back None, which prints as None, and no error appears. A spend that arrives as text with commas gives a TypeError, because the double slash cannot divide a string. '
                         'And an if with nothing indented under it gives an IndentationError. In each case read the last line first, as in Session 5. Which of these will you check for in a colleague\'s code?')))

    S.append(dict(kind='steps', title='An assistant can review your function, and your own test cases decide whether it is right',
                  steps=[dict(head='Paste the function', text='With its docstring', icon='doc'), dict(head='Ask for edge cases', text='What inputs might break it?', icon='speech'), dict(head='Add them as tests', text='Work out expected by hand', icon='pen'),
                         dict(head='Run all the tests', text='assert decides', icon='check')], highlight=3,
                  caption='An assistant may miss the policy or misread a boundary. Never paste personal or confidential data into a public chat tool.',
                  notes=('A free chat assistant is useful for review. Paste your function with its docstring, and ask what inputs might break it. It may suggest edge cases you missed, such as a negative spend or a spend of zero. '
                         'Then add each suggestion as a test case, and work out the expected answer yourself from the policy. Run all your asserts. '
                         'An assistant predicts likely words, so it may misread a boundary or quote a rule you do not have. Your own tests are the judge. And never paste personal or confidential data into a public chat tool. What edge case would you ask it about?')))

    S.append(dict(kind='table', title='Where you will use this at work: write the rule once, test it, run it on every record',
                  headers=['Your job', 'The rule', 'What today lets you do'],
                  rows=[['Credit officer at a bank or microfinance, using Python', 'Illustrative: a risk band from a score, with cut-offs.', 'Write the bands as one function and test each cut-off.'],
                        ['Loyalty analyst at a retailer', f'Tiers from spend. In our 5 percent sample of 2025 orders, {F["n_silver_all"]} of {n(F["cust_2025"])} customers reach Silver. Sample spend is far below real annual spend.', 'Apply one tested function to thousands of customers.'],
                        ['Health records officer at a district office', 'Illustrative: flag a month when visits fall below a threshold.', 'Loop over the months and test the threshold month.'],
                        ['Officer at a SACCO, using Excel and Python', 'Illustrative: a fee band by contribution.', 'Replace a nest of IFs with a function a colleague can test.']],
                  widths=[3.4, 4.5, 4.1], icons=['coin', 'bag', 'clinic', 'people'],
                  notes=(f'Where will you use this on Monday? A credit officer at a bank or microfinance can write risk bands as one function and test each cut-off. A loyalty analyst at a retailer applies one tested function to thousands of customers. '
                         f'In our five percent sample of 2025 orders, only {F["n_silver_all"]} of {n(F["cust_2025"])} customers with a customer id reach Silver, and sample spend is far below real annual spend. '
                         'A health records officer can flag a month whose visits fall below a threshold. And a SACCO officer can replace a nest of IFs with a function a colleague can test. The bands in three of these are illustrative. Which rule in your own job needs this?')))

    S.append(dict(kind='code', title='Read the recipe before the lab: count customers by tier', code=F['code_bridge'], output=F['out_bridge'],
                  reads=['totals is a dictionary: customer id to spend.', 'counts starts at zero for each tier.', 'The loop takes one customer id at a time.', 'It calls loyalty_tier and adds 1 to that tier.', 'print shows the counts.'],
                  notes=(f'Before the lab, read this recipe. It uses the function from earlier on two real customers. Totals is a dictionary from customer id to spend. Counts starts at zero for each tier. '
                         f'The loop takes one customer id at a time, calls loyalty tier on that customer\'s total, and adds one to the matching count. The output was produced by running this code here: {F["out_bridge"][0]}. '
                         'In the lab you do this for six customers. What do you expect for C0009, who spent 46,660 shillings?')))

    S.append(dict(kind='divider', title='Part 2: the Python lab', lead='Close the slides. Open the notebook.', section='Lab',
                  notes=('That is the end of the ideas. Everything you need is on the slides you have just seen, and the notebook repeats each step. '
                         'Open the Colab notebook for Session 6. Run the first two cells. They put the course data next to your notebook and set up the automatic checks. '
                         'In every task, predict the answer first, then run, then read the output, then change one thing.')))

    S.append(dict(kind='steps', title='The lab has six steps, and you keep a tested function at the end',
                  steps=[dict(head='Steps 1 and 2', text='Function and tests', icon='gear'), dict(head='Steps 3 and 4', text='Totals, then tiers', icon='coin'),
                         dict(head='Step 5', text='Trace tier_v1', icon='magnifier'), dict(head='Step 6', text='Spend as text', icon='doc')], highlight=None,
                  caption='For every task: predict, run, read the output, change one thing.',
                  notes=('Here is the map of the lab. Step one, write the loyalty tier function with its docstring, and practise the Boolean expressions behind it. Step two, write the five test cases and run them with assert. '
                         'Step three, total each customer\'s orders in a loop with an accumulator. Step four, apply the function to every total and count the tiers. '
                         'Step five, trace the colleague\'s tier v1 and write a corrected version. Step six, handle a spend that arrives as text. Please do not skip the predictions.')))

    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Tier for 46,660, for 2,388,850 and for 7,500,000 UGX', 'Basic, Silver and Gold'], ['A and B for 2,450 points, and for exactly 6,000 points', f'{F["and_2450"]} and {F["and_6000"]}'],
                        ['Test cases that pass for your function', '5 of 5'], ['Totals for C0009, C0010, C0021, C0230, C0947, C1322 and all six together', f'{cust["C0009"]}, {cust["C0010"]}, {cust["C0021"]}, {cust["C0230"]}, {cust["C0947"]}, {cust["C1322"]}; all {n(F["grand"])}'],
                        ['Customers in Basic, Silver and Gold', f'{F["counts"]["Basic"]}, {F["counts"]["Silver"]} and {F["counts"]["Gold"]}'], ['tier_v1 for 7,500,000, and test cases it fails', f'{F["v1_7_5m"]}, and {F["v1_fails"]} of 5'],
                        ['The spend text 2,388,850 as an int, and its tier', f'{n(F["clean_text"])} and {F["tiers"]["C1322"]}']],
                  widths=[7.4, 4.6], icons=['flag', 'check', 'clock', 'coin', 'people', 'cross', 'doc'], note='If your number differs, find the task that went wrong. Do not change a number to match.',
                  notes=('Use this table as your own self-check. Nobody marks it. If your numbers match, carry on. If one does not, stop and call me, because later tasks use the earlier ones. '
                         'The automatic checks in the notebook print OK or NOT YET after each task. A common cause of a wrong number is a name that holds an old value, because a cell was run out of order, so restart the session and run all cells from the top. '
                         'Do not change a number to make it match. What does it mean if your count of Silver customers is four?')))

    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[['IndentationError', 'Lines under a def, if or for are not indented.', 'Indent the body by four spaces.'], ['The function prints a tier, but the result is None', 'The function has no return line.', 'Use return, not print, inside the function.'],
                        ['A check says NOT YET for the edge cases', 'The test uses > where the rule needs >=.', 'Compare with >= for 2,000 and 6,000 points.'], ['AssertionError on a test case', 'The function returned a different tier than expected.', 'Read the failing line, trace that one input by hand.'],
                        ['TypeError on //', 'The spend is a string.', 'Clean the commas, then use int().']],
                  widths=[3.7, 4.2, 4.1], icons=['cross', 'cross', 'cross', 'cross', 'cross'],
                  notes=('Five messages you may meet. An IndentationError means the lines under def, if or for are not indented. A function that prints but returns None has no return line. '
                         'A check that says NOT YET for the edge cases usually means a greater than where the rule needs greater than or equal to. An AssertionError means the function returned a different tier than you expected, so trace that single input by hand. '
                         'And a TypeError on the double slash means the spend is a string. Read the last line first. It usually tells you the answer.')))

    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[['What is the tier for exactly 6,000,000 UGX, and why is it a good test case?', 'Gold. It is an edge case: exactly on the boundary, where a greater than slip would give Silver.'],
                        ['What is the difference between a parameter and an argument?', f'The parameter is the name inside the function, such as spend_ugx. The argument is the value you pass, such as {n(T["C1322"])}.'],
                        ['An accumulator holds 0 before the loop. What does it hold after the pass over each of three orders?', 'It holds the running total: the first order, then the first two together, then all three.']],
                  widths=[5.6, 6.4], icons=['flag', 'gear', 'coin'],
                  notes=('Last, the exit check. Three questions. Write your answers before you look at mine. One, what is the tier for exactly six million shillings, and why is it a good test case? '
                         'Two, what is the difference between a parameter and an argument? Three, an accumulator starts at zero: what does it hold after each pass over three orders? '
                         'The short answers are on the slide. If you got all three, you are ready for session seven. If one surprised you, look at that step of your notebook again tonight.')))

    sess['facilitator'] = dict(
        prep=['Open the learner notebook in Colab before anyone arrives and run it from the top. The first cell asks for data.zip: have the file ready to upload or share a link.',
              'Check that loyalty_programme.txt says 1 point per UGX 1,000, Silver from 2,000 points and Gold from 6,000 points. The deck and notebook use exactly that.',
              'Write the check table (slide 24 of the deck) on the board before the lab.',
              'Concepts run with laptops closed. Ask learners to open the notebook only after the Part 2 divider.',
              f'Remind learners that orders.csv is a 5 percent sample, so the 2025 totals are small. Only {F["n_silver_all"]} of {n(F["cust_2025"])} customers with a customer id reach Silver and none reach Gold. The six lab customers were chosen to show all the branches of the rule.'],
        misconceptions=[('One equals sign tests equality', 'One stores a value. Two equals signs compare. A single sign inside an if is a SyntaxError.'),
                        ('print and return do the same thing', 'print shows a value to a person. return hands the value back to the code that called the function. Without return the caller gets None.'),
                        ('If the function works on a few normal values it is correct', 'Bugs hide at the boundaries. Test the value just below and exactly on each boundary.'),
                        ('The order of elif branches does not matter', 'The first True branch wins. Testing Silver before Gold makes Gold unreachable.'),
                        ('A parameter and an argument are the same thing', 'The parameter is the name in the def line. The argument is the value passed in the call.')],
        probes=[('What is the spreadsheet cousin of an if statement?', 'The IF function, with a nested IF for a third tier.'),
                ('What is the spreadsheet cousin of a for loop?', 'Fill down: one formula applied to each row.'),
                ('What is an accumulator?', 'A variable that starts at zero and collects a result as the loop goes round.'),
                ('What does a docstring do?', 'It says in one line what the function does, for the next reader.'),
                ('What is an edge case?', 'An input exactly where a rule changes, such as 2,000,000 UGX.'),
                ('What does silence from an assert mean?', 'The test passed.'),
                ('Why write the expected column from the policy before running?', 'So the test checks the function against the rule, not against itself.')],
        lab_steps=[('Step 1: the function', f'Basic for 46,660, Silver for 2,388,850 and Gold for 7,500,000. The docstring is present. Boolean practice: A and B is {F["and_2450"]} at 2,450 points and {F["and_6000"]} at 6,000.'),
                   ('Step 2: the tests', 'Five test pairs, zero failures. Learners who used > see two failures at the exact boundaries.'),
                   ('Step 3: the accumulator', f'C0009 {cust["C0009"]}, C1322 {cust["C1322"]}, all six {n(F["grand"])}. The total must restart at 0 for each customer.'),
                   ('Step 4: apply the function', f'Counts: Basic {F["counts"]["Basic"]}, Silver {F["counts"]["Silver"]}, Gold {F["counts"]["Gold"]}. C0230 is Silver at {cust["C0230"]}.'),
                   ('Step 5: trace tier_v1', f'tier_v1(7500000) returns {F["v1_7_5m"]}. It fails {F["v1_fails"]} of 5 test cases. The fix is to test Gold first.'),
                   ('Step 6: text spend', f'Remove the commas, convert with int(): {n(F["clean_text"])}, tier {F["tiers"]["C1322"]}.')],
        rescue=['If the concepts run over, skip slide 5 (logical operators) and read the loop slides quickly; the notebook covers them.',
                'If only 30 minutes of lab remain, do steps 1, 2, 4 and 5 and set steps 3 and 6 as homework.',
                'If a learner has the function but the tests fail at the boundaries, ask them to read the line of the policy that says starts at.',
                'If a learner has no laptop, pair them with a neighbour: one types, one predicts aloud.'],
        after=['Share the notebook and this deck again for learners who were absent.', 'Ask each learner to save the notebook and bring one business rule from their own job that could become a function.', 'Note any question you could not answer and open the next session with it.'],
        lab_answer_key=[['Step 1 PREDICT: what tier will 2,388,850 UGX get?', 'Silver, because 2,388 points is 2,000 or more and under 6,000.'],
                        ['Step 1 READ: why is 6,000 below 6,000 False?', 'A number is not less than itself, so A and B is False for exactly 6,000 points.'],
                        ['Step 2 PREDICT: which test cases are most likely to fail?', 'The ones exactly on the boundary: 2,000,000 and 6,000,000.'],
                        ['Step 3 READ: why must total restart at 0 for each customer?', 'Otherwise each customer total includes the earlier customers.'],
                        ['Step 4 CHANGE: move Silver to 2,500 points. What changes?', f'{", ".join(F["alt_changed"])} drop to Basic. Counts become {F["alt_counts"][0]} Basic, {F["alt_counts"][1]} Silver, 0 Gold.'],
                        ['Step 5 READ: why does tier_v1 return Silver for 7,500,000?', 'The Silver test comes first and is True for 7,500 points, so Gold is never tested.'],
                        ['Step 6 CHANGE: use a spend text with spaces.', 'Remove them too: replace the comma and the space before int().']])
    return sess


def lab_numbers():
    F = facts()
    return dict(totals=F['totals'], orders=F['orders_2025'], counts=F['counts'], tiers=F['tiers'], grand=F['grand'], tests=[(s, e) for s, e, _ in F['tests']], v1_7_5m=F['v1_7_5m'],
                v1_fails=F['v1_fails'], clean_text=F['clean_text'], c0230=F['totals']['C0230'])
