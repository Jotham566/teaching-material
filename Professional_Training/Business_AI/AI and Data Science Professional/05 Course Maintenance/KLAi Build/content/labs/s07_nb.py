"""Session 7 Python lab: pandas I, load, look and filter. Expected values come from content/s07.py facts() (pandas on the real files)."""
import importlib.util
import sys
from pathlib import Path

BUILD = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BUILD / 'kit'))
import nb as NB  # noqa: E402

_spec = importlib.util.spec_from_file_location('s07', BUILD / 'content' / 's07.py')
S7 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(S7)

TITLE = 'pandas I load, look and filter'


def todo(b, solution, hint, learner, model):
    """A cell the learner completes: the learner version holds `learner`, the solution holds `model`."""
    b.code(('# Hint: ' + hint + '\n' if hint else '') + (model if solution else learner))


ATTEMPT = (
    '# Helper for the checks. Run this cell once. You do not need to read it.\n'
    '# attempt() runs a check on your answer. If the answer is not written yet it says NOT YET instead of stopping with an error.\n'
    'def attempt(label, expr, expected, tol=0.01):\n'
    '    try:\n'
    '        value = eval(expr)\n'
    '        want = eval(expected) if isinstance(expected, str) else expected\n'
    '    except Exception:\n'
    '        value, want = None, 0\n'
    '    check(label, value, want, tol)')


def guard(text):
    """Wrap display lines in try/except so an unfinished answer above gives a hint and not a traceback."""
    body = '\n'.join('    ' + l for l in text.split('\n'))
    return 'try:\n' + body + '\nexcept Exception:\n    print("Not yet: finish the cell above, then run this cell again.")'


def chk(label, expr, expected, tol=0):
    return f'attempt({label!r}, {expr!r}, {expected!r}, {tol})'


def build(solution):
    F = S7.facts()
    n = S7.n
    b = NB.Notebook()
    b.md('# Session 7: pandas I, load, look and filter\n\n**KLAi | AI and Data Science Professional**\n\n'
         'In this lab you load the Lakeside Mart orders file (fictional, generated data), look at it before you trust it, filter it, and save a data profile. '
         'Each step has the same rhythm: **PREDICT**, run, **READ**, then **CHANGE one thing**. A cell that says `None  # your code here` is yours to fill. '
         'The check cells say OK or NOT YET, and they keep running while an answer is still `None`. Keep your answers to each prediction in the grey boxes.')
    b.data_setup()
    b.check_setup()
    b.code(ATTEMPT)

    b.step(1, 'Load the file and look at its shape', 'read_csv reads a CSV file into a DataFrame. shape gives the number of rows, then the number of columns.')
    b.predict('The file holds one record for each till order. Roughly how many rows do you expect: hundreds, thousands or hundreds of thousands?')
    todo(b, solution, "pd.read_csv('orders.csv')", 'import pandas as pd\n\norders = None  # your code here: read orders.csv into a DataFrame',
         "import pandas as pd\n\norders = pd.read_csv('orders.csv')")
    b.code(guard('print(orders.shape)\nprint(orders.dtypes)\nprint(orders.head(3))') + '\n'
           + chk('number of rows', 'orders.shape[0]', F['rows']) + '\n' + chk('number of columns', 'orders.shape[1]', F['cols']))
    b.read('Which column is stored as text but holds dates? What data type does pandas call text? (It is object, and pandas 3 and later shows it as str.)')
    b.change('Change head(3) to head(8) and run the cell. What do you see about the index?')

    b.step(2, 'Missing values and a summary', 'isna() marks each empty cell True and sum() counts the Trues for each column. describe() summarises a numeric variable.')
    b.predict('Which column do you expect to have missing values? (Remember the walk-in shoppers from Session 2.) Will the mean order value be bigger or smaller than the median?')
    todo(b, solution, 'chain isna() and sum(), then pick the customer_id entry. Use .mean() and .median() on the column order_value_ugx',
         'n_missing = None  # your code here: the number of missing customer_id values\nmean_value = None  # your code here\nmedian_value = None  # your code here',
         "n_missing = orders.isna().sum()['customer_id']\nmean_value = orders['order_value_ugx'].mean()\nmedian_value = orders['order_value_ugx'].median()")
    b.code(guard('print(orders.isna().sum())\nprint(orders["order_value_ugx"].describe())') + '\n'
           + chk('missing customer_id', 'n_missing', F['n_missing']) + '\n' + chk('mean order value', 'mean_value', round(F['mean'], 2), 0.5) + '\n' + chk('median order value', 'median_value', round(F['median'], 1), 0.5))
    b.read('The mean is about twice the median. What does that tell you about the largest orders?')
    b.change('Add .info() on its own line: orders.info(). Find the line that shows how many customer_id values are filled.')

    b.step(3, 'Select columns and filter with a Boolean mask', 'A comparison such as orders["branch_id"] == "B04" builds a mask of True and False, one per row. Putting the mask inside square brackets after the DataFrame keeps the True rows.')
    b.predict('Branch B04 is Jinja. About how many of the orders do you expect to come from one branch, out of eight branches?')
    todo(b, solution, 'mask = a comparison with ==; then orders[mask]. Take a list of two names for two_columns',
         'two_columns = None  # your code here: a DataFrame with only order_id and order_value_ugx\nmask = None  # your code here: the comparison for branch B04\njinja = None  # your code here: orders where the mask is True',
         "two_columns = orders[['order_id', 'order_value_ugx']]\nmask = orders['branch_id'] == 'B04'\njinja = orders[mask]")
    b.code(guard('print(two_columns.shape)\nprint(mask.sum(), len(jinja))') + '\n'
           + chk('two columns kept', 'two_columns.shape[1]', 2) + '\n' + chk('Jinja orders', 'len(jinja)', F['n_jinja']) + '\n' + chk('mask sum equals row count', 'mask.sum()', 'len(jinja)'))
    b.read('Why does mask.sum() give the same number as len(jinja)?')
    b.change('Filter for branch B01 instead. How many orders does it have? Change it back to B04 afterwards.')

    b.step(4, 'Two conditions, and query', 'Join two masks with & (and) or | (or). Each condition goes in its own round brackets. query() writes the condition as text.')
    b.predict('Jinja orders paid by Mobile money: will the count be bigger or smaller than the number of Jinja orders? And will "Jinja or Mobile money" be bigger or smaller than "Jinja and Mobile money"?')
    todo(b, solution, "(test one) & (test two); then (test one) | (test two). query(\"branch_id == 'B04' and payment_method == 'Mobile money'\")",
         'n_both = None  # your code here: Jinja AND Mobile money\nn_either = None  # your code here: Jinja OR Mobile money\nn_query = None  # your code here: the same as n_both, written with query',
         "n_both = len(orders[(orders['branch_id'] == 'B04') & (orders['payment_method'] == 'Mobile money')])\n"
         "n_either = len(orders[(orders['branch_id'] == 'B04') | (orders['payment_method'] == 'Mobile money')])\n"
         "n_query = len(orders.query(\"branch_id == 'B04' and payment_method == 'Mobile money'\"))")
    b.code('print(n_both, n_either, n_query)\n'
           + chk('Jinja and Mobile money', 'n_both', F['n_both']) + '\n' + chk('Jinja or Mobile money', 'n_either', F['n_either']) + '\n' + chk('query gives the same as &', 'n_query', 'n_both'))
    b.read('Which is larger, n_both or n_either? Why must that always be true?')
    b.change('On purpose, write the first filter with the word and instead of &, and run it. Read the last line of the error. Then fix it.')
    b.change('Try three more filters and read each count: `orders["branch_id"].isin(["B01", "B04"])`, `orders["order_value_ugx"].between(10000, 50000)` and `orders["payment_method"].str.contains("Mobile")`. Put each inside `orders[...]` and use `len`. Then run `orders["branch_id"].nunique()`.')

    b.step(5, 'Sort and count', 'sort_values orders the rows. head(10) keeps ten. value_counts() counts each different value of a Series.')
    b.predict('Will the largest order be near the mean order value, or many times larger? Which payment method do you expect to be the most common?')
    todo(b, solution, "sort_values('order_value_ugx', ascending=False).head(10); value_counts() on payment_method",
         'top10 = None  # your code here: the ten largest orders\ncounts = None  # your code here: the number of orders for each payment method',
         "top10 = orders.sort_values('order_value_ugx', ascending=False).head(10)\ncounts = orders['payment_method'].value_counts()")
    b.code(guard('print(top10[["order_id", "branch_id", "order_value_ugx"]])\nprint(counts)') + '\n'
           + chk('largest order value', 'top10["order_value_ugx"].iloc[0]', F['top_value']) + '\n' + chk('sum of the ten largest', 'top10["order_value_ugx"].sum()', F['top10_sum']) + '\n'
           + chk('Mobile money orders', 'counts["Mobile money"]', F['pay']['Mobile money']) + '\n' + chk('counts add up to all orders', 'counts.sum()', F['rows']))
    b.read('How many times larger than the median order is the largest order? Is it a sale or a typing error? What would you ask the data owner?')
    b.change('Use ascending=True. What is the smallest order value?')

    b.step(6, 'Pick rows with loc and iloc', 'iloc picks by position (counting from 0, end left out). loc picks by label (the index value, end included). After a filter the labels are no longer 0, 1, 2.')
    b.predict('jinja.iloc[0] is the first row of jinja. What do you think its index label is: 0, or something else?')
    todo(b, solution, 'jinja.index[0] is the first label. Use iloc with a position and loc with a label',
         "first_label = None  # your code here: the index label of the first row of jinja\nvalue_by_position = None  # your code here: order_value_ugx of the row at position 0\nvalue_by_label = None  # your code here: order_value_ugx of the row with that label",
         "first_label = jinja.index[0]\nvalue_by_position = jinja.iloc[0]['order_value_ugx']\nvalue_by_label = jinja.loc[first_label, 'order_value_ugx']")
    b.code('print(first_label, value_by_position, value_by_label)\n'
           + chk('first label of jinja', 'first_label', F['jinja_first_label']) + '\n' + chk('value of the first Jinja row', 'value_by_position', F['jinja_first_value']) + '\n' + chk('loc gives the same row', 'value_by_label', 'value_by_position'))
    b.read('Why would jinja.loc[0] give an error?')
    b.change('Run jinja.loc[0] in a new cell and read the last line. Then delete the cell.')

    b.step(7, 'Build and save a data profile', 'A data profile has one row for each variable: its data type, how many values are missing, and the share missing. You keep it, and you can build the same profile for any file.')
    b.predict('How many rows will the profile have, and which variable will have a share missing above zero?')
    todo(b, solution, 'a DataFrame from a dictionary; dtypes.astype(str) gives readable names; share = missing / number of rows * 100',
         'profile = None  # your code here: a DataFrame with columns dtype, missing and missing_pct, one row per variable',
         "profile = pd.DataFrame({'dtype': orders.dtypes.astype(str), 'missing': orders.isna().sum()})\n"
         "profile['missing_pct'] = (profile['missing'] / len(orders) * 100).round(1)")
    b.code(guard('profile.to_csv("orders_profile.csv")\nprint(profile)') + '\n'
           + chk('profile rows', 'len(profile)', F['cols']) + '\n' + chk('missing share of customer_id', 'profile.loc["customer_id", "missing_pct"]', float(F['profile'].loc['customer_id', 'missing_pct']), 0.05) + '\n'
           + chk('variables with missing values', '(profile["missing"] > 0).sum()', 1))
    b.read('If a colleague sent you this profile of a file you had never seen, what would you know about it?')
    b.change('Add one more column, n_unique, with the number of different values in each variable (orders.nunique()). Which variable has the most?')

    b.md('## Check against Sheets\n\nOpen `orders.csv` in Google Sheets. Use a filter to reproduce the Jinja count from step 3 and the Jinja and Mobile money count from step 4. '
         'Write one sentence about anything that did not match.\n\n> My sentence: ')
    b.md('---\n## Finish\n\nRun the cell below. It should say **All 21 checks pass**. Then download `orders_profile.csv` from the file panel on the left, and save the notebook to your Drive.')
    b.code('show_checks()')
    return b
