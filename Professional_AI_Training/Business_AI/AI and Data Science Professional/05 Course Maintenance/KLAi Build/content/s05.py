"""Session 5: Your first Python, next to the spreadsheet (variables, data types, list, dictionary, error messages). Python lab, notebook in content/labs/s05_nb.py.

Every number and every piece of code output on a slide, in a note or in the notebook checks is computed in facts(): pandas reads the real Lakeside Mart
files, and every code snippet shown on a slide is run here (exec) so the output on the slide is the output Python gave. Nothing is typed from memory.
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


def n(x):
    return f'{int(x):,}'


def run_code(code, ns):
    """Run code in the namespace ns and return the printed lines (the real output)."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(code, '<cell>', 'exec'), ns)
    return buf.getvalue().rstrip('\n').split('\n')


def run_error(code, ns):
    """Run code that must fail. Returns (traceback lines as Python prints them, exception name, message)."""
    linecache.cache['<cell>'] = (len(code), None, code.splitlines(True), '<cell>')
    try:
        exec(compile(code, '<cell>', 'exec'), ns)
    except Exception as e:  # noqa: BLE001
        tb = e.__traceback__.tb_next if e.__traceback__ and e.__traceback__.tb_next else e.__traceback__
        text = ''.join(traceback.format_exception(type(e), e, tb)).rstrip('\n')
        if isinstance(e, SyntaxError):
            text = 'Traceback (most recent call last):\n' + text
        lines = [l for l in text.split('\n')]
        return lines, type(e).__name__, (e.msg if isinstance(e, SyntaxError) else str(e))
    raise AssertionError('the code was expected to fail: ' + code)


@lru_cache(maxsize=None)
def facts():
    P = pd.read_csv(DATA / 'products.csv')
    F = {}
    first5 = P.head(5)
    F['prices'] = [int(v) for v in first5.unit_price_ugx]
    F['ids'] = list(first5.product_id)
    F['p001'] = P.iloc[0]
    F['price_p001'] = int(P.iloc[0].unit_price_ugx)
    F['quantity'] = 12
    ns = {}
    pr, qt = F['price_p001'], F['quantity']
    # slide: first cell
    F['code_assign'] = f'price_p001 = {pr}\nquantity = {qt}\nline_total = price_p001 * quantity\nprint(line_total)'
    F['out_assign'] = run_code(F['code_assign'], ns)
    F['line_total'] = int(ns['line_total'])
    assert F['line_total'] == pr * qt
    # types
    ns['product_name'] = str(F['p001'].product_name)
    ns['prices'] = list(F['prices'])
    ns['average'] = sum(F['prices']) / len(F['prices'])
    ns['is_dear'] = ns['price_p001'] > 5000
    F['types'] = [dict(name='int', value=ns['price_p001'], example=str(ns['price_p001'])), dict(name='float', value=ns['average'], example=repr(ns['average'])),
                  dict(name='str', value=ns['product_name'], example=repr(ns['product_name'])), dict(name='bool', value=ns['is_dear'], example=repr(ns['is_dear']))]
    for t in F['types']:
        t['type'] = run_code(f'print(type({t["example"]}))', {})[0]
        assert t['type'] == f"<class '{t['name']}'>", t
    F['is_dear'] = ns['is_dear']
    F['average'] = ns['average']
    # arithmetic table
    F['ops'] = []
    for py, xl, what in [(f'{pr} * {qt}', f'={pr}*{qt}', 'Multiply. Plus, minus and divide work as in Excel.'), ('sum(prices) / len(prices)', '=AVERAGE(range)', 'Divide. The answer is always a float.'),
                         (f'{F["line_total"]} // 1000', f'=INT({F["line_total"]}/1000)', 'Floor division: the whole part only.'), (f'{F["line_total"]} % 1000', f'=MOD({F["line_total"]},1000)', 'Remainder after dividing.'),
                         ('2 ** 3', '=2^3', 'Power.')]:
        F['ops'].append((py, xl, what, repr(eval(py, {'sum': sum, 'len': len, 'prices': F['prices']}))))
    # the quotes trap
    a, b = str(F['prices'][0]), str(F['prices'][1])
    F['trap_num'] = (f'{a} + {b}', repr(eval(f'{a} + {b}')))
    F['trap_str'] = (f"'{a}' + '{b}'", repr(eval(f"'{a}' + '{b}'")))
    F['trap_int_sum'] = int(a) + int(b)
    F['convert'] = f"int('{a}') + int('{b}')"
    assert F['trap_str'][1] == f"'{a}{b}'"
    F['str_star'] = repr(eval(f"'{a}' * 3"))
    # list
    ps = F['prices']
    F['list_literal'] = repr(ps)
    F['sum'], F['len'], F['max'], F['min'] = sum(ps), len(ps), max(ps), min(ps)
    F['mean'] = F['sum'] / F['len']
    F['plus_total'] = F['sum'] + 3600
    F['lookups'] = [('prices[0]', repr(ps[0]), 'the first item'), ('prices[4]', repr(ps[4]), 'the last of five items'), ('len(prices)', repr(len(ps)), 'how many items')]
    F['list_ops'] = [('len(prices)', '=COUNT(E2:E6)', 'How many items', repr(len(ps))), ('sum(prices)', '=SUM(E2:E6)', 'Add them all', repr(sum(ps))), ('max(prices)', '=MAX(E2:E6)', 'The largest', repr(max(ps))),
                     ('min(prices)', '=MIN(E2:E6)', 'The smallest', repr(min(ps))), ('sum(prices) / len(prices)', '=AVERAGE(E2:E6)', 'The mean', repr(sum(ps) / len(ps))),
                     ('prices.append(3600)', 'Type the next price in E7', 'Add one item at the end', f'{len(ps) + 1} items')]
    # dictionary
    F['price_list'] = {k: v for k, v in zip(F['ids'], ps)}
    F['p003'] = F['price_list']['P003']
    # the file
    F['n_products'] = len(P)
    F['top_price'] = int(P.unit_price_ugx.max())
    F['top_id'] = str(P.loc[P.unit_price_ugx.idxmax(), 'product_id'])
    F['top_name'] = str(P.loc[P.unit_price_ugx.idxmax(), 'product_name'])
    F['mean_price'] = round(float(P.unit_price_ugx.mean()), 2)
    F['code_file'] = ("import pandas as pd\nproducts = pd.read_csv('products.csv')\nall_prices = products['unit_price_ugx'].tolist()\nprint(len(all_prices))\nprint(max(all_prices))\n"
                      "print(round(sum(all_prices) / len(all_prices), 2))")
    old = Path.cwd()
    import os
    os.chdir(DATA)
    try:
        F['out_file'] = run_code(F['code_file'], {})
    finally:
        os.chdir(old)
    assert F['out_file'] == [str(F['n_products']), str(F['top_price']), str(F['mean_price'])], F['out_file']
    # errors, run for real
    en = {'quantity': qt, 'prices': list(ps), 'price_list': dict(F['price_list'])}
    F['err_name_code'] = 'price_p001 = ' + str(pr) + '\nquantity = 12\nline_total = prise_p001 * quantity'
    F['err_name'] = run_error(F['err_name_code'], dict(en))
    F['err_type_code'] = f"basket = [{ps[0]}, {ps[1]}, '{ps[2]}']\nprint(sum(basket))"
    F['err_type'] = run_error(F['err_type_code'], dict(en))
    F['err_key'] = run_error("print(price_list['P099'])", dict(en))
    F['err_index'] = run_error('print(prices[5])', dict(en))
    F['err_syntax'] = run_error("print('Total', 3200", dict(en))
    F['err_value'] = run_error("int('UGX 7,800')", dict(en))
    F['basket_total'] = ps[0] + ps[1] + ps[2]
    # raw export: numbers stored as text
    raw = pd.read_csv(DATA / 'orders_raw.csv', dtype=str, keep_default_na=False)
    bad = raw[~raw.unit_price.str.fullmatch(r'\d+')]
    F['raw_rows'], F['raw_text_prices'] = len(raw), len(bad)
    F['raw_pct'] = F['raw_text_prices'] / F['raw_rows'] * 100
    F['raw_example'] = str(bad.unit_price.iloc[0])
    # bridge recipe output on a slide
    return F


def tb(lines):
    return list(lines)


def build():
    F = facts()
    ps, ids = F['prices'], F['ids']
    pr, qt = F['price_p001'], F['quantity']
    err_name, err_type = F['err_name'], F['err_type']
    sess = dict(
        num=5, block='Module B: Python for data', short_title='Your first Python next to the spreadsheet',
        title='Your first Python: variables, lists and error messages, next to the spreadsheet',
        question='What does the same price-list task look like in Excel and in Python, and how do you read an error message when Python stops?',
        outcomes=['Run and save a notebook, and store values in variables with the right data type: int, float, str or bool',
                  'Hold many values in a list or a dictionary of key-value pairs, and look one up',
                  'Read a traceback from its last line, name the exception, and fix the typed-number-versus-string trap'],
        outcome_icons=['notebook', 'grid', 'magnifier'],
        outcome_note=('By the end of today you can run and save a notebook in Google Colab, and store values in variables. You can say what data type each value has: int, float, str or bool. '
                      'You can keep many values in a list or in a dictionary, and look one up. And you can read an error message from its last line, name the exception, and fix it. '
                      'You will do all of it on the Lakeside Mart price list, with the spreadsheet answer beside every Python answer.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: picture, plain words, one example by hand'), (10, 'Break'), (45, 'Lab: predict, run, read, change'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: concepts first, then a Python notebook lab',
        plan_caption='Pictures and plain words first. Then you open the notebook. Then the checks and what you keep.',
        plan_note=('We have two hours. The first ten minutes bring back Session 4 and set the question for today. Then forty-five minutes of concepts, with laptops closed, so you can watch the pictures and ask questions. '
                   'After a ten minute break you open a Google Colab notebook for a forty-five minute lab. For every task you predict, run, read the output and change one thing. '
                   'The last ten minutes are an exit check and what you keep. The lab is where the learning sticks, so please protect that time.'),
        recall_from='Session 4',
        recall=[('You drew 200 samples of 30 orders and the 200 averages were not all the same. What is that variation called?', 'Sampling variability. Its size is the standard error, and it gets smaller when each sample is bigger.'),
                ('A survey asks only the customers who come to the till on a Saturday. What goes wrong?', 'Selection bias. Shoppers who never come on a Saturday are left out, so the sample does not stand for all customers.'),
                ('Branch footfall and orders rise together. Does that show footfall causes orders?', 'No. Correlation is not causation. A confounder such as branch size can lift both.')],
        words=[('Variable (assignment)', 'A name that stands for a stored value, like a named cell in Excel. In Python you choose the name, such as price_p001. In Session 2 a variable was a column of a table. Here it is a name that holds a value.'),
               ('Data type (int, float, str, bool)', 'How Python stores a value: a whole number, a decimal number, text (a string) or True or False.'),
               ('List', 'Values in order inside square brackets. Each has an index, and the first index is 0. It is like one column of a sheet.'),
               ('Dictionary (key-value pairs)', 'Values stored under labels called keys. You look a value up by its key, as VLOOKUP does.'),
               ('Exception (traceback)', 'The error Python raises when a line cannot run. The traceback is its report. Its last line names the exception.')],
        word_icons=['pin', 'tag', 'grid', 'key', 'cross'],
        words_note=('Five words for today. A variable is a name that stands for a stored value, which you create by assignment. This is a second meaning of the word: in Session 2 a variable was a column of a table, and in programming it is a name that holds a value. Context tells you which. A data type says how Python stores the value: int, float, str or bool. '
                    'A list holds values in order, and a dictionary holds key-value pairs. And an exception is the error Python raises when a line cannot run, with a traceback that reports where. '
                    'Each word has a spreadsheet cousin, and we meet every one of them before the end of the session.'),
        keep='Keep your saved notebook: the Lakeside price list built with variables, a list and a dictionary, a fixed number-versus-string trap, and a short note on one error you read and fixed.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab file', value='A saved notebook'), dict(label='Your error note', value='Last line in plain words'), dict(label='Next session', value='Decisions and functions')]),
        keep_title='Save your notebook to Drive, with your error note',
        next='Session 6: Decisions, repeats and functions. Your code learns to choose with if, repeat with for, and reuse steps in a function.', next_label='Next session',
        keep_note=('Before you go, save your notebook with File, then Save a copy in Drive. That notebook is your keepsake from today: a price list built three ways, a trap you fixed, and one error you read from the last line. '
                   'If a colleague can open it, run it from the top and see the same numbers, it is good. Next session your code learns to decide and to repeat. '
                   'If anything was unclear, write the question down and bring it.'),
        cover_note=('Welcome back. For four sessions you thought with data in a spreadsheet. Today you write your first lines of Python, and every idea arrives next to the spreadsheet thing you already know. '
                    'We build a small Lakeside Mart price list, make mistakes on purpose, and learn to read what Python says back. '
                    'Nobody writes code without seeing errors, so reading them is the main skill of the day.'),
        use_at_work='Keep prices, loans or visits in a list or a dictionary, and read an error message from its last line.',
        slides=[])
    S = sess['slides']

    # 1 answers
    S.append(dict(kind='table', title='Answers to the three questions from Session 4', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in sess['recall']], widths=[5.2, 6.8], icons=['chart', 'people', 'magnifier'],
                  notes=('Here are the answers to the three warm-up questions. The two hundred averages differed because every sample holds different orders. That variation is sampling variability, and its size is the standard error. '
                         'A survey of Saturday shoppers only is selection bias, because the shoppers who never come on a Saturday are left out. '
                         'And footfall and orders rising together is a correlation. It does not show cause, because a confounder such as branch size can lift both. Which of the three did you find hardest?')))

    # 2 notebook
    S.append(dict(kind='wide', title='A notebook mixes text cells and code cells, and runs them from the top',
                  visual=dict(kind='ds_c_notebook', heading='Lakeside Mart price list', code=F['code_assign'].split('\n'), output=F['out_assign']),
                  caption='A Jupyter notebook is a document of cells. Colab runs it in a browser. The kernel is its engine.',
                  notes=('This is a notebook. A notebook is a Jupyter document made of cells, and Google Colab lets you open one in your browser, free, with nothing to install. '
                         'A text cell holds headings and notes for people, and Python skips it. A code cell holds Python. You press the play button on its left, and the output appears directly under the cell. '
                         'Behind the notebook sits the kernel, the Python engine that remembers what you stored. Cells run in the order you press play, so a later cell can use what an earlier cell stored. Have you used a notebook before?')))

    # 3 working habits
    S.append(dict(kind='statement', title='Run the cells from the top, and save a copy to Drive',
                  lead='Three habits keep a notebook honest.',
                  points=['Cells run in the order you press play. A later cell uses only what an earlier one stored.', 'If it goes odd, restart and run all cells from the top.',
                          'Save a copy in Drive. An idle session ends.'], icons=['notebook', 'gear', 'folder'],
                  notes=('Three habits will save you hours. One, cells run in the order you press play. If a cell uses a name that an earlier cell never created, Python tells you. '
                         'Two, when the notebook behaves oddly, restart the session from the Runtime menu and run all the cells again from the top. If it works from the top, it is trustworthy. '
                         'Three, save a copy in Drive. A Colab session that sits idle ends, and everything in memory goes with it. Which of these habits do you already have from Excel?')))

    # 4 variable: sheet vs python
    S.append(dict(kind='idea', title='A variable is a name you give to a stored value, like a named cell in Excel',
                  visual=dict(kind='ds_c_sheetpy', rows=[('price_p001', str(pr)), ('quantity', str(qt)), ('line_total', str(F['line_total']))], lines=F['code_assign'].split('\n')[:3], formula=f'B4 holds =B2*B3 and shows {F["line_total"]}'),
                  lead='Variable: a name that stands for a stored value.',
                  points=['Sheet: the value sits in cell B2, which you could name Price. Python: it is stored under the name price_p001.', 'In Session 2 a variable was a column of a table. In programming a variable is a name that holds a value.'],
                  notes=(f'Here is a sum you could do in your sleep: {qt} units of product P001, at {n(pr)} shillings each. On the left is the spreadsheet. On the right is Python. '
                         f'In the sheet the price sits in cell B2, which you could give a name such as Price. In Python it is stored under a name you choose. That name is a variable: a name that stands for a stored value. In Session 2 a variable meant a column of a table, so this is a second meaning of the word, and context tells you which. '
                         f'The formula multiplies the two names, just as B4 multiplies B2 and B3, and the answer is {n(F["line_total"])}. A name tells the reader what the number means, and B2 cannot. Which names would you choose for a loan amount and a term?')))

    # 5 assignment
    S.append(dict(kind='idea', title='Assignment works out the right side first, then stores the answer under the name',
                  visual=dict(kind='ds_c_assign', inputs=[('price_p001', str(pr), 'int'), ('quantity', str(qt), 'int')], result=('line_total', str(F['line_total']), 'int'), statement='line_total = price_p001 * quantity'),
                  lead='Assignment: the equals sign stores a value under a name.',
                  points=['Names use letters, digits and underscores. Case matters.', 'One equals sign stores. Two, ==, compare.', 'print() shows a value.'],
                  notes=('This picture shows the third line of the first cell. The two boxes on the left hold what we already stored, each with its name and its data type, int. '
                         'Python first works out the right side of the equals sign, which is the price times the quantity. Then it stores the answer under the name on the left, line total. '
                         'So the equals sign stores a value under a name. To ask a question you use two equals signs. Names have rules: letters, digits and underscores, with no spaces. What would happen if you wrote the name with a space?')))

    # 6 data types
    S.append(dict(kind='wide', title='Every value has a data type: int, float, str or bool',
                  visual=dict(kind='ds_c_types', cols=[dict(name='int', meaning='Whole number', example=F['types'][0]['example'], type=F['types'][0]['type'], excel='A number with no decimals'),
                                                       dict(name='float', meaning='Decimal number', example=F['types'][1]['example'], type=F['types'][1]['type'], excel='A number with decimals'),
                                                       dict(name='str', meaning='String: text in quotes', example=F['types'][2]['example'], type=F['types'][2]['type'], excel='A text cell'),
                                                       dict(name='bool', meaning='True or False', example=F['types'][3]['example'], type=F['types'][3]['type'], excel='TRUE or FALSE')]),
                  caption='type() asks Python for a value\'s data type: how it is stored, as in Session 2.',
                  notes=(f'Every value has a data type, which is how Python stores it. An int is a whole number, like the price {n(pr)}. A float is a decimal number, like the mean price {F["average"]}. '
                         f'A str, short for string, is text in quotes, like the product name Staples item 001. And a bool is True or False, like the answer to the question: is the price above five thousand? Here it is {F["is_dear"]}. '
                         'The function type tells you which kind a value is. This is the same data type idea from Session 2, now in code. Which type would you give a phone number?')))

    # 7 arithmetic
    S.append(dict(kind='table', title='Python does the arithmetic you know, plus a few new signs',
                  headers=['Python', 'Excel', 'What it does', 'Result'], rows=[[a, b, c, d] for a, b, c, d in F['ops']], widths=[3.0, 3.4, 4.0, 1.6], icons=['calculator', 'chart', 'pin', 'clock', 'gear'],
                  note='prices is the list of five prices from the next slides. Floor division and remainder come back in Session 6, when we turn spend into loyalty points.',
                  notes=(f'Python does the arithmetic you already know. Multiply with a star, divide with a slash. Dividing always gives a float, so the mean of the five prices is {F["mean"]}. '
                         f'Two new signs matter. Double slash is floor division: it keeps the whole part only, so {n(F["line_total"])} divided by a thousand gives 38. In Session 6 that gives loyalty points. '
                         'Percent gives the remainder, and double star is a power. Excel has the same ideas under other names, such as INT and MOD. Which of these would you have used in a formula last month?')))

    # 8 strings and the quotes trap
    S.append(dict(kind='idea', title='Quotes turn a number into a string, and plus then joins instead of adding',
                  visual=dict(kind='ds_c_trap', panels=[dict(title='No quotes: two ints', code=F['trap_num'][0], result=F['trap_num'][1], note='Plus adds the numbers.'),
                                                        dict(title='Quotes: two strings', code=F['trap_str'][0], result=F['trap_str'][1], note='Plus joins the text. Python raises no error.', bad=True)], verdict='A quiet wrong answer is worse than an error.'),
                  lead='String (str): text inside quotes. A number in quotes is text.',
                  points=['Plus on ints adds. Plus on strings joins.', 'int() or float() converts a string: type conversion (casting).', 'Check type() when a total looks odd.'],
                  notes=(f'Here is the trap that catches everyone once. Without quotes, {ps[0]} plus {ps[1]} is {F["trap_int_sum"]}. With quotes, the same plus sign joins the two strings into {F["trap_str"][1]}. '
                         'Python raises no error, because joining two strings is perfectly legal. The answer is simply wrong. The cure is type conversion, also called casting: int turns a string into a whole number, and float turns it into a decimal number. '
                         'Whenever a total looks odd, ask Python for the data type first. Where might numbers arrive as text in your own work?')))

    # 9 list
    S.append(dict(kind='idea', title='A list holds values in order, and the first position is index 0',
                  visual=dict(kind='ds_c_list', name='prices', values=ps, lookups=F['lookups']),
                  lead='List: values in order, inside square brackets.',
                  points=['A list is like one column of a sheet.', 'Index: the position of an item, counting from 0.', 'len, sum and max work on the whole list.'],
                  notes=(f'A list is Python\'s version of one column of a sheet. This list is called prices, and it holds the first five Lakeside prices: {", ".join(n(v) for v in ps)}. '
                         'The numbers below the cells are the index, the position of each item. The index starts at zero, not one, which surprises everyone at first. '
                         f'So prices with a zero in square brackets is the first item, {n(ps[0])}. The function len tells you how many items there are: {len(ps)}. Why do you think programmers count from zero?')))

    # 10 list operations
    S.append(dict(kind='table', title='Functions on a list do what SUM, MAX and AVERAGE do on a column',
                  headers=['Python', 'Excel', 'What it does', 'Result'], rows=[[a, b, c, d] for a, b, c, d in F['list_ops']], widths=[3.4, 3.3, 3.2, 2.1], icons=['clock', 'coin', 'chart', 'tag', 'calculator', 'notebook'],
                  note='The five prices are in E2 to E6 of products.csv when you open it in a sheet. append changes the list itself.',
                  notes=(f'Here is the list at work, with the Excel formula beside each step. Len counts the items, like COUNT: {F["len"]}. Sum adds them, like SUM: {n(F["sum"])}. Max gives the largest, {n(F["max"])}, and min the smallest, {n(F["min"])}. '
                         f'The mean is the sum divided by the length, {F["mean"]}, and it is a float. And append adds one item at the end of the list, as typing the next price in a new cell would. '
                         'Each function has a Python name and an Excel name, but the idea is the same. Which Excel function would you reach for to find the second largest price?')))

    # 11 dictionary
    S.append(dict(kind='idea', title='A dictionary stores key-value pairs, so you find a value by its label',
                  visual=dict(kind='ds_c_dict', name='price_list', pairs=[(k, v) for k, v in F['price_list'].items()], pick='P003', lookup=("price_list['P003']", str(F['p003'])), excel='=VLOOKUP("P003", table, 2, FALSE)'),
                  lead='Dictionary: values stored under labels called keys.',
                  points=['Each key is paired with one value: a key-value pair.', 'Curly brackets hold the pairs.', 'You ask by key, so the order does not matter.'],
                  notes=(f'A dictionary stores key-value pairs. The keys on the left are the product codes. The values on the right are the prices. To find one you ask by key: the price for P003 is {n(F["p003"])}. '
                         'In Excel you do the same lookup with VLOOKUP, a table, and a column number. A dictionary does it with the key alone. Curly brackets hold the pairs, and each key can appear only once. '
                         'You will use dictionaries for every lookup table in this course. What other lookup tables do you keep in Excel?')))

    # 12 list or dictionary
    S.append(dict(kind='compare', title='List or dictionary: choose by how you will look things up',
                  left=dict(head='List', points=['Values in order.', 'Find an item by its index: 0, 1, 2.', 'Excel twin: one column to add up.']),
                  right=dict(head='Dictionary', points=['Values with labels.', "Find an item by its key, such as 'P003'.", 'Excel twin: a VLOOKUP table, for a lookup.']),
                  verdict='Ask first: will I find it by position or by label?',
                  notes=('How do you choose between the two? Ask how you will look the value up. A list is ordered, and you find an item by its index, so it suits one column of values that you add up or average. '
                         'A dictionary has labels, and you find an item by its key, so it suits a lookup table such as a price list. '
                         'If you would write a VLOOKUP in Excel, you want a dictionary. If you would write a SUM over a column, you want a list. Which would you use for the loan amounts of one branch?')))

    # 13 traceback
    S.append(dict(kind='wide', title='A traceback is the report of a failure: read its last line first',
                  visual=dict(kind='ds_c_traceback', lines=err_name[0], labels=[(len(err_name[0]) - 1, 'Read this last line first: the exception type, then its message.'), (len(err_name[0]) - 3, 'Where: the cell and the line number.'), (len(err_name[0]) - 2, 'The line of code that failed.')]),
                  caption='From a real run. Colab adds colours and an arrow. The last line is the same.',
                  notes=(f'When a line cannot run, Python raises an exception and prints a traceback, a report of where it failed. Here I misspelt price as prise. '
                         f'Read the last line first. It names the exception, NameError, and gives a message: {err_name[2]}. Python has nothing stored under that name, so it is a spelling slip or a cell you have not run. '
                         'The lines above it tell you where: the cell, the line number, and the line of code that failed. Beginners read from the top and get lost. Read from the bottom. What would you check first for a NameError?')))

    # 14 five exceptions
    ex = [('NameError', F['err_name'], 'No variable has that name: a spelling slip, or its cell has not run.', 'Check the spelling. Run the earlier cell.'),
          ('TypeError', F['err_type'], 'An operation met the wrong data type, such as int plus str.', 'Convert with int() or float().'),
          ('KeyError', F['err_key'], 'The dictionary has no such key.', 'Check the key spelling and its quotes.'),
          ('IndexError', F['err_index'], 'The list has no item at that index.', 'The last index is len minus 1.'),
          ('SyntaxError', F['err_syntax'], 'The line breaks a grammar rule.', 'Close every bracket and quote.')]
    S.append(dict(kind='table', title='Five exceptions cover most beginner errors', headers=['Exception', 'Last line says', 'What it means', 'Usual fix'],
                  rows=[[a, f'{b[1]}: {b[2]}', c, d] for a, b, c, d in ex], widths=[2.0, 4.0, 3.5, 2.8], icons=['question', 'tag', 'key', 'grid', 'pen'],
                  note='Messages copied from real runs in Python 3.10 or later. Newer Python versions may word a message slightly differently.',
                  notes=('Five exceptions will account for most of your errors this week. NameError: the name does not exist. TypeError: an operation met the wrong data type, such as an int and a string. '
                         'KeyError: the dictionary has no such key. IndexError: the list has no item at that position. And SyntaxError: the line breaks the grammar of Python, usually a bracket or quote that was never closed. '
                         'Each message on the slide is copied from a real run. The wording can differ a little between Python versions, but the exception name does not. Which of the five do you expect to meet first?')))

    # 15 four steps
    S.append(dict(kind='steps', title='Four steps read any error and fix it',
                  steps=[dict(head='Read the last line', text='Exception and message', icon='magnifier'), dict(head='Find the line', text='Line number in the traceback', icon='pin'),
                         dict(head='Name the cause', text='Spelling, type or position?', icon='question'), dict(head='Fix, then run again', text='From the top', icon='gear')], highlight=0,
                  caption='Change one thing at a time. An error is information.',
                  notes=('Here are the four steps I would like you to follow every time. One, read the last line. Two, find the line number in the traceback. Three, name the cause: is it a spelling slip, a wrong data type, or a wrong position? '
                         'Four, fix one thing and run the cell again, from the top if the notebook has grown. Do not change three things at once, because then you cannot tell which one fixed it. '
                         'An error message is information. It is Python telling you exactly where it got stuck. What do you usually do first when Excel shows an error?')))

    # 16 stat raw prices as text
    S.append(dict(kind='stat', title=f'A quarter of the raw export stores the price as text, so Python needs a conversion', big=f'{F["raw_pct"]:.0f}%',
                  text=f'{n(F["raw_text_prices"])} of the {n(F["raw_rows"])} rows in orders_raw.csv hold unit_price as text such as {F["raw_example"]}. Python cannot add text until you clean it.',
                  waffle_label='raw rows in every 100 with a text price',
                  notes=(f'This is the same trap on real data. In the raw order line export, {n(F["raw_text_prices"])} of {n(F["raw_rows"])} rows store the unit price as text, with the letters UGX in front and a comma inside, like {F["raw_example"]}. '
                         f'That is about {F["raw_pct"]:.0f} in every 100 rows. Python will not add those values, because they are strings. Calling int on one raises a ValueError, and the last line reads: {F["err_value"][1]}: {F["err_value"][2]}. '
                         'Cleaning it is the work of Session 8, and today you learn to recognise the problem from the data type. Which column in your own files might be stored as text?')))

    # 17 AI assistant
    S.append(dict(kind='steps', title='A free chat assistant can explain an error, and you still check the fix',
                  steps=[dict(head='Copy the last line', text='Add the cell code', icon='doc'), dict(head='Ask in plain words', text='What does this mean?', icon='speech'),
                         dict(head='Run the fix', text='In your own notebook', icon='gear'), dict(head='Check the number', text='Compare with Sheets', icon='calculator')], highlight=3,
                  caption='An assistant predicts likely words, so it can explain well and still be wrong about your data. Never paste personal or confidential data into a public chat tool.',
                  notes=('A free chat assistant is a good tutor for errors. Copy the last line of the traceback with the code from the cell, and ask what it means in plain words. '
                         'Then run its fix in your own notebook, and check the number against a sheet or against a sum you do by hand. An assistant predicts likely words, so it can explain an error well and still give a fix that changes your answer. '
                         'It is optional help, never the last step. And never paste personal or confidential data into a public chat tool. What would you check after running its fix?')))

    # 18 use at work
    S.append(dict(kind='table', title='Where you will use this at work: keep values in a list or a dictionary, and read the error',
                  headers=['Your job', 'What it looks like', 'What today lets you do'],
                  rows=[['Credit analyst at a bank, using Python and SQL', 'Loan amounts in a list. An interest rate per product in a dictionary.', 'Add up a list in one line. Look a rate up by key.'],
                        ['Finance officer at a SACCO, using Excel', 'Contributions copied from a statement as text, such as UGX 7,800.', 'Spot a string that looks like a number and convert it.'],
                        ['Data officer at a ministry, using pandas', f'A file of {F["n_products"]} products read into a list of prices.', 'Check the count, the largest value and the mean in three lines.'],
                        ['Analyst handing work to a colleague', 'A Colab notebook with notes in text cells.', 'Share a notebook that runs from the top.']],
                  widths=[3.4, 4.2, 4.4], icons=['coin', 'people', 'folder', 'laptop'],
                  notes=('Where will you use this on Monday? Four examples. A credit analyst at a bank who uses Python and SQL can keep loan amounts in a list and the interest rate for each product in a dictionary. '
                         'A finance officer at a SACCO often copies contributions from a statement as text, such as UGX 7,800, and now knows to convert them before totalling. '
                         'A data officer at a ministry using pandas can read a file into a list and check its count, its largest value and its mean in three lines. And any analyst can hand over a notebook that runs from the top. Which is closest to your job?')))

    # 19 bridge
    outf = F['out_file']
    S.append(dict(kind='code', title='Read the recipe before the lab: six lines read a real file into a list',
                  code=F['code_file'], output=outf,
                  reads=['Line 1 loads pandas, a library for tables.', "Line 2 reads products.csv into a table.", 'Line 3 puts the price column into a list.',
                         f'Line 4: how many prices, {outf[0]}.', f'Line 5: the largest, {n(outf[1])} UGX.', f'Line 6: the mean, {outf[2]}.'],
                  notes=(f'Before the lab, read this recipe. It is the last task of the lab, and it brings together everything you saw. Line one loads pandas, a library for tables that we meet properly in Session 7. '
                         f'Line two reads the file products dot csv. Line three takes the unit price column and turns it into a list. Then three lines print what we learned: {outf[0]} products, a largest price of {n(outf[1])} shillings, and a mean of {outf[2]}. '
                         'All those outputs were produced by running this exact code here. What would you add to check it against a sheet?')))

    # 20 divider
    S.append(dict(kind='divider', title='Part 2: the Python lab', lead='Close the slides. Open the notebook.', section='Lab',
                  notes=('That is the end of the ideas. Everything you need is on the slides you have just seen, and the notebook repeats each step. '
                         'Open the Colab notebook for Session 5. Run the first two cells. They put the course data next to your notebook and set up the automatic checks. '
                         'In every task, predict the answer first, then run, then read the output, then change one thing. Write your prediction before you run.')))

    # 21 lab map
    S.append(dict(kind='steps', title='The lab has six steps, and you keep a saved notebook at the end',
                  steps=[dict(head='Steps 1 and 2', text='Variables and the quotes trap', icon='pin'), dict(head='Step 3', text='List: sum, mean, max', icon='grid'),
                         dict(head='Step 4', text='Dictionary: look up by key', icon='key'), dict(head='Steps 5 and 6', text='Read an error, then the file', icon='magnifier')], highlight=None,
                  caption='For every task: predict, run, read the output, change one thing. None means no value yet: the lab cells start as None, and you replace it.',
                  notes=('Here is the map of the lab. In the notebook, None means no value yet. Every cell you must complete starts as None, and you replace it with your answer. Step one, store the price and quantity in variables and ask for their data types. Step two, meet the quotes trap and fix it with int. '
                         'Step three, build the list of five prices and find the sum, the mean and the largest. Step four, build the dictionary and look prices up by key. '
                         'Step five, a cell arrives already broken: read its last line, name the exception and fix it. Step six reads the real products file. Please do not skip the predictions.')))

    # 22 check numbers
    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[[f'line_total from price_p001 = {pr} and quantity = {qt}', n(F['line_total'])], [f'{ps[0]} + {ps[1]} as strings, then as ints', f'{F["trap_str"][1]}, then {F["trap_int_sum"]}'],
                        ['sum, mean and max of the five prices', f'{n(F["sum"])}, {F["mean"]} and {n(F["max"])}'], [f'The sum after adding one more price of 3600', n(F['plus_total'])],
                        ['The price of P003 in price_list, and its size after adding P006', f'{n(F["p003"])}, and 6'], ['The exception name and the fixed basket total', f'TypeError, and {n(F["basket_total"])}'],
                        ['Products in products.csv, the largest price, the mean', f'{F["n_products"]}, {n(F["top_price"])} and {F["mean_price"]}']],
                  widths=[7.4, 4.6], icons=['calculator', 'question', 'chart', 'coin', 'key', 'cross', 'folder'], note='If your number differs, find the task that went wrong. Do not change a number to match.',
                  notes=('Use this table as your own self-check. Nobody marks it. If your numbers match, carry on. If one does not, stop and call me, because later tasks use the earlier ones. '
                         'The notebook also has automatic checks that print OK or NOT YET after each task. A common cause of a wrong number is a name that holds an old value, because a cell was run out of order. '
                         'Restart the session and run all the cells from the top. What does it tell you if the check says NOT YET but you think your answer is right?')))

    # 23 error cards
    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[["NameError: name 'price_p001' is not defined", 'The cell that creates the name has not run, or the spelling differs.', 'Run the cells from the top. Match the spelling and the capital letters.'],
                        ['TypeError on a sum or a plus', 'A string is mixed with a number.', 'Convert it with int() or float(). Check the quotes.'],
                        ["KeyError: 'P003'", 'The key is missing from the dictionary, or it is not a string.', "Write the key in quotes: 'P003'."],
                        ['SyntaxError: was never closed', 'A bracket or a quote was not closed.', 'Count the opening and closing signs on the line.'],
                        ['NOT YET after your answer is right', 'The cell was run before the answer was typed, or the name differs.', 'Run the answer cell again, then the check line.']],
                  widths=[3.7, 4.2, 4.1], icons=['cross', 'cross', 'cross', 'cross', 'check'],
                  notes=('Five messages you may meet. A NameError means the cell that creates the name has not run, or the spelling differs, including the capital letters. A TypeError on a sum means a string is mixed with a number, so convert it. '
                         'A KeyError means the key is missing from the dictionary. Check the quotes, because the keys are strings. A SyntaxError about a bracket means something was never closed. '
                         'And NOT YET after a right answer usually means the cell ran before you typed the answer. Read the last line first. It usually tells you the answer.')))

    # 24 exit check
    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[[f"Two prices are typed in quotes. What does '{ps[0]}' + '{ps[1]}' give, and why?", f'{F["trap_str"][1]}. Both values are strings, so plus joins them. Convert with int() to add.'],
                        ['A dictionary has no key P099. What does the last line of the error say, and what is the exception?', F['err_key'][1] + ': ' + F['err_key'][2] + '. The exception is a KeyError.'],
                        ['How many items does a list of five prices have, and what is the index of the last one?', 'Five items. The last index is 4, because counting starts at 0.']],
                  widths=[5.6, 6.4], icons=['question', 'key', 'grid'],
                  notes=('Last, the exit check. Three questions. Write your answers before you look at mine. One, a price is typed in quotes: what does the plus of two quoted prices give, and why? '
                         'Two, a dictionary has no key P099: what does the last line say, and what is the exception? Three, a list holds five prices: how many items, and what is the last index? '
                         'The short answers are on the slide. If you got all three, you are ready for session six. If one surprised you, look at that step of your notebook again tonight.')))

    # facilitator
    sess['facilitator'] = dict(
        prep=['Open the learner notebook in Colab before anyone arrives and run it from the top. The first cell asks for data.zip: have the file (03 Learner Materials, Practice Files) ready to upload or share a link.',
              'Check that Runtime, Restart session and run all exists in your Colab menu, and that pandas loads without installing anything.',
              'Write the check table (slide 22 of the deck) on the board before the lab.',
              'Concepts run with laptops closed. Ask learners to open the notebook only after the Part 2 divider.',
              'Remind learners that all data is fictional and generated. products.csv has 150 products, and orders_raw.csv is the dirty export that Session 8 cleans.'],
        misconceptions=[('The equals sign asks whether two values are equal', 'One equals sign stores a value under a name. Two equals signs, ==, ask the question. Session 6 uses ==.'),
                        ('A number in quotes is still a number', f"It is a string. {F['trap_str'][0]} joins the text and gives {F['trap_str'][1]}. Use int() to convert."),
                        ('Python counts items from 1, like Excel rows', 'Python counts from 0. The first item is index 0, and the last of five is index 4.'),
                        ('An error means I broke the computer or the notebook', 'An exception is information. The last line names the problem and the traceback shows where.'),
                        ('If the assistant gave a fix, the fix is right', 'An assistant predicts likely words. Run the fix, then check the number against a sheet.')],
        probes=[('What is a variable, in spreadsheet words?', 'A named cell: a name that stands for a stored value.'),
                ('Which line of a traceback do you read first?', 'The last line. It names the exception and gives the message.'),
                ("What does type('3200') print, and what does type(3200) print?", "<class 'str'> and <class 'int'>."),
                ('Why does the list index start at 0?', 'It counts the steps from the start of the list. The first item is zero steps from the start.'),
                ('When do you choose a dictionary over a list?', 'When you find values by a label, as with VLOOKUP, and not by position.'),
                ('What does a TypeError on a sum usually mean?', 'A string is mixed with numbers. Convert it with int() or float().'),
                ('What is the difference between a traceback and an exception?', 'The exception is the error that Python raises. The traceback is the printed report of where it happened.')],
        lab_steps=[('Step 1: variables and types', f'price_p001 = {pr}, quantity = {qt}, line_total = {n(F["line_total"])}. is_dear is False.'),
                   ('Step 2: the quotes trap', f"The joined string is {F['trap_str'][1]}. The int version is {F['trap_int_sum']}. Several learners will expect {F['trap_int_sum']} from the quoted line."),
                   ('Step 3: the list', f'Sum {n(F["sum"])}, mean {F["mean"]}, max {n(F["max"])}. With 3600 added the sum is {n(F["plus_total"])}.'),
                   ('Step 4: the dictionary', f'P003 is {n(F["p003"])}. After adding P006 the dictionary has 6 entries. P002 at {n(F["price_list"]["P002"])} is above 8000.'),
                   ('Step 5: the broken cell', f'The last line says TypeError: {err_type[2]}. The fix is to remove the quotes around {ps[2]}. The basket total is {n(F["basket_total"])}.'),
                   ('Step 6: the real file', f'{F["n_products"]} products, a largest price of {n(F["top_price"])} (product {F["top_id"]}) and a mean of {F["mean_price"]}. Compare with Sheets: =MAX, =AVERAGE on the unit_price_ugx column.')],
        rescue=['If the concepts run over, skip slide 7 (arithmetic) and slide 12 (list or dictionary) and go from slide 11 to the traceback.',
                'If only 30 minutes of lab remain, do steps 1, 2, 3 and 5 and set steps 4 and 6 as homework.',
                'If Colab will not load, the same code runs in any Jupyter notebook or in a local Python window. The checks need only numpy.',
                'If a learner has no laptop, pair them with a neighbour: one types, one predicts aloud.'],
        after=['Share the notebook and this deck again for learners who were absent.', 'Ask each learner to save the notebook to Drive and to bring one error message they could not read to Session 6.', 'Note any question you could not answer and open the next session with it.'],
        lab_answer_key=[['Step 1 PREDICT: what will line_total print?', f'{n(F["line_total"])}, the price times the quantity.'],
                        ['Step 1 READ: what does type(price_p001) print?', "<class 'int'>, a whole number."],
                        ['Step 2 PREDICT: what does the quoted plus print?', f"{F['trap_str'][1]}: the two strings are joined, with no error."],
                        ['Step 2 CHANGE: remove the quotes.', f'{F["trap_int_sum"]}. The two ints are added.'],
                        ['Step 3 READ: why is the mean a float?', 'Division with a slash always gives a float, here ' + str(F['mean']) + '.'],
                        ['Step 3 CHANGE: add one price of 3600 to the list.', f'The sum becomes {n(F["plus_total"])}.'],
                        ['Step 4 PREDICT: what does price_list lookup of P006 give before you add it?', 'A KeyError, because the key is not in the dictionary yet.'],
                        ['Step 5 READ: what is the exception and the message?', f'TypeError: {err_type[2]}.'],
                        ['Step 6 READ: what does the largest price tell you?', f'The most expensive product costs {n(F["top_price"])} UGX, product {F["top_id"]}. The mean is pulled up by a few such products.']])
    return sess


def lab_numbers():
    """The expected values for the notebook checks (all computed in facts())."""
    F = facts()
    return dict(price=F['price_p001'], quantity=F['quantity'], line_total=F['line_total'], joined=F['trap_str'][1].strip("'"), int_sum=F['trap_int_sum'], prices=F['prices'], ids=F['ids'],
                sum=F['sum'], mean=F['mean'], max=F['max'], plus_total=F['plus_total'], p003=F['p003'], p002=F['price_list']['P002'], basket_total=F['basket_total'],
                err_type=F['err_type'][1], top_name=F['top_name'], n_products=F['n_products'], top_price=F['top_price'], mean_price=F['mean_price'], prices_text=F['list_literal'])
