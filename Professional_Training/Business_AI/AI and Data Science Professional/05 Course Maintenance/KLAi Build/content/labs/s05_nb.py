"""Session 5 lab notebook: Your first Python, next to the spreadsheet. Expected numbers come from content/s05.py (pandas on the real files)."""
import importlib.util
from pathlib import Path

import nb as NB

TITLE = 'Your first Python next to the spreadsheet'
_p = Path(__file__).resolve().parents[1] / 's05.py'
_spec = importlib.util.spec_from_file_location('s05_session', _p)
_m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_m)
N = _m.lab_numbers()


def build(solution: bool) -> NB.Notebook:
    nb = NB.Notebook()
    ps = N['prices']
    ids = N['ids']
    nb.md('# Session 5: Your first Python, next to the spreadsheet\n\n**Question of the day:** what does the same price-list task look like in Excel and in Python, and what do I do when Python says no?\n\n'
          'Work top to bottom. In every step: **predict**, **run**, **read** the output, **change one thing**. Cells marked `your code here` are yours to fill in; the check line under each answer prints OK or NOT YET.\n\n'
          '`None` means no value yet. Every cell you complete starts as `None`: replace it with your answer.\n\n'
          'What you keep: this notebook, saved with *File, Save a copy in Drive*.')
    nb.data_setup()
    nb.check_setup()

    # step 1
    nb.step(1, 'Variables and data types', 'A variable is a name that stands for a stored value, like a named cell in Excel. (In Session 2 a variable was a column of a table. In programming it is a name that holds a value.) Product P001 costs '
            f'{N["price"]} UGX and you sell {N["quantity"]} units.')
    nb.predict(f'You store the price {N["price"]} under the name `price_p001` and {N["quantity"]} under `quantity`. What will `line_total = price_p001 * quantity` hold?')
    if solution:
        nb.code(f'price_p001 = {N["price"]}\nquantity = {N["quantity"]}\nline_total = price_p001 * quantity\nprint(line_total)\n'
                'check("line_total", line_total, %d)' % N['line_total'])
    else:
        nb.code(f'price_p001 = None   # your code here: the price of P001 is {N["price"]} UGX\nquantity = None      # your code here: {N["quantity"]} units\n'
                'line_total = None    # your code here: price times quantity\nprint(line_total)\n'
                'check("line_total", line_total, %d)' % N['line_total'])
    nb.read('Run `print(type(price_p001))`. What data type does Python report, and what is the spreadsheet cousin of that type?')
    if solution:
        nb.code('print(type(price_p001))\nis_dear = price_p001 > 5000   # a comparison gives True or False\nprint(is_dear)\n'
                'check("price_p001 is an int", type(price_p001) is int, True)\ncheck("is_dear is False", is_dear is False, True)')
    else:
        nb.code('print(type(price_p001))\nis_dear = None   # your code here: is the price above 5000? A comparison gives True or False\nprint(is_dear)\n'
                'check("price_p001 is an int", type(price_p001) is int, True)\ncheck("is_dear is False", is_dear is False, True)')
    nb.change('Change the price to 6000 and run the cells again from the top. What does `is_dear` become? Change it back afterwards.')

    # step 2
    nb.step(2, 'The typed number versus string trap', 'A number inside quotes is a string. Plus on two strings joins them, and Python raises no error.')
    nb.predict(f"What will `'{ps[0]}' + '{ps[1]}'` give? And what will `{ps[0]} + {ps[1]}` give?")
    if solution:
        nb.code(f"joined = '{ps[0]}' + '{ps[1]}'\nprint(joined)\nprint(type(joined))\n"
                f'total_price = int(\'{ps[0]}\') + int(\'{ps[1]}\')   # int() converts a string to a whole number\nprint(total_price)\n'
                "check('joined text', joined == '%s', True)\ncheck('total_price', total_price, %d)" % (N['joined'], N['int_sum']))
    else:
        nb.code(f"joined = None        # your code here: add the two strings '{ps[0]}' and '{ps[1]}' (keep the quotes)\nprint(joined)\n"
                'total_price = None   # your code here: convert each string with int() before adding\nprint(total_price)\n'
                "check('joined text', joined == '%s', True)\ncheck('total_price', total_price, %d)" % (N['joined'], N['int_sum']))
    nb.change(f'Remove the quotes around {ps[0]} and {ps[1]} in the first line. What does Python print now?')

    # step 3
    nb.step(3, 'A list is one column of values', f'The first five Lakeside prices, in UGX, from `products.csv`: {", ".join(str(p) for p in ps)}. The first index of a list is 0.')
    nb.predict('Before you run: how many items will `len(prices)` report, and what is the index of the last item?')
    if solution:
        nb.code(f'prices = {N["prices_text"]}\ntotal = sum(prices)\naverage = sum(prices) / len(prices)\ntop = max(prices)\nprint(len(prices), total, average, top)\n'
                'check("sum", total, %d)\ncheck("mean", average, %s)\ncheck("max", top, %d)' % (N['sum'], N['mean'], N['max']))
    else:
        nb.code(f'prices = None    # your code here: a list of the five prices, in square brackets, with no quotes\ntotal = None     # your code here: sum(prices)\n'
                'average = None   # your code here: the sum divided by len(prices)\ntop = None       # your code here: max(prices)\n'
                'print(total, average, top)\n'
                'check("sum", total, %d)\ncheck("mean", average, %s)\ncheck("max", top, %d)' % (N['sum'], N['mean'], N['max']))
    nb.read('The mean prints with a decimal point. Which data type is it, and why did Python choose it?')
    if solution:
        nb.code('prices_plus = prices + [3600]   # one more price at the end\nprint(sum(prices_plus))\ncheck("sum with 3600 added", sum(prices_plus), %d)' % N['plus_total'])
    else:
        nb.code('prices_plus = None   # your code here: the list prices plus one more item, 3600\nprint(prices_plus)\n'
                'check("sum with 3600 added", sum(prices_plus) if prices_plus else None, %d)' % N['plus_total'])
    nb.change('Print the first item with `prices[0]` and the last with `prices[4]`. Then try `prices[5]` and read the last line of the error. Which exception is it?')

    # step 4
    nb.step(4, 'A dictionary stores key-value pairs', 'A dictionary finds a value by its label (its key), as VLOOKUP does in a sheet.')
    nb.predict("`price_list['P003']` will give which price? And what will `price_list['P099']` do?")
    pairs = ', '.join(f"'{k}': {v}" for k, v in zip(ids, ps))
    if solution:
        nb.code('price_list = {%s}\np003 = price_list[\'P003\']\nprice_list[\'P006\'] = 3600   # add a new key-value pair\nprint(p003, len(price_list))\n'
                'p002_dear = price_list[\'P002\'] > 8000\nprint(p002_dear)\n'
                'check("price of P003", p003, %d)\ncheck("six entries", len(price_list), 6)\ncheck("P002 is above 8000", p002_dear is True, True)' % (pairs, N['p003']))
    else:
        nb.code('price_list = None   # your code here: a dictionary with keys \'P001\' to \'P005\' (in quotes) and the five prices as values, in curly brackets\n'
                'p003 = None         # your code here: look up the key \'P003\'\n# your code here: add a new entry with key \'P006\' and value 3600\n'
                'p002_dear = None    # your code here: is the P002 price above 8000?\nprint(p003)\n'
                'check("price of P003", p003, %d)\ncheck("six entries", len(price_list) if price_list else 0, 6)\ncheck("P002 is above 8000", p002_dear is True, True)' % N['p003'])
    nb.change("Look up a key that is not there, such as `price_list['P099']`. Read the last line. Which exception is it?")

    # step 5
    nb.step(5, 'Read the error: the last line first', 'The next cell arrives broken on purpose. Run it, read the last line of the traceback, name the exception, then fix the list.')
    nb.predict('Which exception do you expect when a list holds numbers and one text value and you call `sum` on it?')
    if solution:
        nb.code(f"basket = [{ps[0]}, {ps[1]}, {ps[2]}]   # fixed: the quotes around {ps[2]} are removed\nbasket_total = sum(basket)\nprint(basket_total)\n"
                "error_name = 'TypeError'   # the exception name from the last line of the broken version\n"
                f"check('basket total', basket_total, {N['basket_total']})\ncheck('exception name', error_name == '{N['err_type']}', True)")
    else:
        nb.md('**First, run the broken cell below.** It stops with an error on purpose. Read the LAST line.')
        nb.code(f"basket = [{ps[0]}, {ps[1]}, '{ps[2]}']\nbasket_total = sum(basket)\nprint(basket_total)")
        nb.code("# Now fix the basket: write the list again without the quotes around the third price.\n"
                "# Then type the exception name from the last line above, as text, for example 'KeyError'.\n"
                "basket = None        # your code here: the fixed list\n"
                "error_name = None    # your code here: the exception name from the last line\n"
                "basket_total = sum(basket) if basket else None\nprint(basket_total)\n"
                f"check('basket total', basket_total, {N['basket_total']})\ncheck('exception name', error_name == '{N['err_type']}', True)")
    nb.md('**Optional: ask a free chat assistant.** Paste the last line of the error and the code. Ask: *what does this mean, in plain words?* Run its fix in your notebook and check the number against a sheet. '
          'An assistant predicts likely words, so check its answer by running it. Never paste personal or confidential data.\n\n> What I asked, and what I checked: ')
    nb.change('Change `basket` so it holds a misspelt name, for example `basket = [prise_p001]`. Which exception do you get now? Then undo it.')

    # step 6
    nb.step(6, 'The same lists, read from the real products file', 'You will meet pandas properly in Session 7. For now, three lines read a file into a list.')
    nb.predict('The file has one row per product. Will `len(all_prices)` be a small number or a big number? Guess before you run.')
    if solution:
        nb.code("import pandas as pd\n\nproducts = pd.read_csv('products.csv')\nall_prices = products['unit_price_ugx'].tolist()\n"
                'n_products = len(all_prices)\ntop_price = max(all_prices)\nmean_price = round(sum(all_prices) / len(all_prices), 2)\nprint(n_products, top_price, mean_price)\n'
                'top_name = products.loc[products["unit_price_ugx"].idxmax(), "product_name"]\n'
                'check("products", n_products, %d)\ncheck("largest price", top_price, %d)\ncheck("mean price", mean_price, %s)\ncheck("most expensive product", top_name == %r, True)' % (N['n_products'], N['top_price'], N['mean_price'], N['top_name']))
    else:
        nb.code("import pandas as pd\n\nproducts = pd.read_csv('products.csv')\nall_prices = None   # your code here: products['unit_price_ugx'].tolist()\n"
                'n_products = None  # your code here: how many prices\ntop_price = None   # your code here: the largest price\nmean_price = None  # your code here: the mean, rounded to 2 decimals\n'
                'top_name = None    # your code here: the product_name of the row with the largest price\n'
                'check("products", n_products, %d)\ncheck("largest price", top_price, %d)\ncheck("mean price", mean_price, %s)\ncheck("most expensive product", top_name == %r, True)' % (N['n_products'], N['top_price'], N['mean_price'], N['top_name']))
    nb.read('Which product has the largest price, and how far above the mean is it? What does that tell you about the mean? Hint: `products.loc[products["unit_price_ugx"].idxmax(), "product_name"]` gives the name.')
    nb.md('## Compare with a sheet\n\nOpen `products.csv` in Google Sheets. Use `=SUM(E2:E6)` for the first five prices and `=MAX(E2:E151)` and `=AVERAGE(E2:E151)` for the whole column. '
          'Do they match Python?\n\n> My comparison: ')
    nb.md('## Your error note (keep this)\n\nWrite one error you read today: the exception name, the message from the last line, and the fix, in plain words.\n\n> My error note: ')
    nb.code('show_checks()')
    return nb
