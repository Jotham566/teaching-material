"""Session 9 lab notebook: pandas III, group, join and reshape. Expected numbers come from content/s09.py facts() (pandas on the real files)."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
BUILD = HERE.parents[2]
sys.path.insert(0, str(BUILD / 'kit'))
import nb as NB  # noqa: E402

_sp = importlib.util.spec_from_file_location('s09_facts', BUILD / 'content' / 's09.py')
_m = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(_m)
F = _m.facts()

TITLE = 'pandas III group join reshape'


def merge_checks(nb):
    """Put each check(...) cell at the end of the answer cell before it, so the lab has fewer cells."""
    out = []
    for c in nb.cells:
        src = ''.join(c['source'])
        if c['cell_type'] == 'code' and src.startswith('check(') and out and out[-1]['cell_type'] == 'code':
            prev = ''.join(out[-1]['source'])
            out[-1]['source'] = NB._src(prev + '\n\n# Automatic check\n' + src)
        else:
            out.append(c)
    nb.cells = out


def build(solution: bool):
    nb = NB.Notebook()
    R = F['rows']
    nb.md('# Session 9 lab: group, join and reshape\n\n**Question of the day:** How do we answer a question that needs several groups and several tables, and trust the total?\n\n'
          'In every step: **predict** first, run the code, **read** the output, then **change** one thing. '
          'You keep this notebook. It ends with a join log (the row count before and after every merge) and one written finding.\n\n'
          'Data: Lakeside Mart (fictional, generated). The orders file is a 5 percent sample of till orders, so revenue describes the sample.')
    nb.data_setup()
    nb.check_setup()
    nb.code('import pandas as pd\n\n'
            "orders = pd.read_csv('orders.csv')\nlines = pd.read_csv('order_lines.csv')\nbranches = pd.read_csv('branches.csv')\n"
            "customers = pd.read_csv('customers.csv')\nproducts = pd.read_csv('products.csv')\n"
            'print(len(orders), len(lines))\n\n'
            '# The join log: one row for every merge. Run this cell once. You do not need to read it.\n'
            'join_log = []\n'
            'def log(step, rows_before, rows_after, note):\n'
            "    join_log.append(dict(step=step, rows_before=rows_before, rows_after=rows_after, note=note))\n"
            'def safe(f):\n'
            '    try:\n        return f()\n    except Exception:\n        return -1   # lets a check say NOT YET instead of stopping')

    # ---------------------------------------------------------------- step 1
    nb.step(1, 'groupby and named aggregation', 'groupby splits the records into groups. An aggregate function reduces each group to one number.')
    nb.predict('Add up order_value_ugx for each branch. Will the eight branch totals add up to the total of the whole orders file? Which branch will lead?')
    if solution:
        nb.code("rev_branch = orders.groupby('branch_id')['order_value_ugx'].sum()\nprint(rev_branch)\n\n"
                "summary = orders.groupby('branch_id').agg(\n    orders=('order_id', 'count'),\n    revenue=('order_value_ugx', 'sum'),\n    average=('order_value_ugx', 'mean'))\nsummary.round(0)")
    else:
        nb.code("rev_branch = None   # group orders by branch_id, then sum order_value_ugx\nsummary = None      # named aggregation: orders (count of order_id), revenue (sum), average (mean)")
    nb.code(f"check('B01 revenue', safe(lambda: rev_branch['B01']), {F['b01_rev']})\n"
            f"check('eight branches add up to the total', safe(lambda: rev_branch.sum()), {F['rev']})\n"
            f"check('B01 orders in summary', safe(lambda: summary.loc['B01', 'orders']), {F['b01_orders']})")
    nb.read('Which branch has the largest revenue? Does it also have the largest average order? Look at the summary table.')
    nb.change('Add a fourth named aggregation, biggest=(\'order_value_ugx\', \'max\'). What is the largest order of B01?')

    # ---------------------------------------------------------------- step 1b
    nb.step(2, 'count and size', 'size counts records. count counts only filled values. Walk-in orders have a missing customer_id.')
    nb.predict('For branch B01, will the number of records and the number of filled customer_id values be equal? If not, which is smaller?')
    if solution:
        nb.code("sizes = orders.groupby('branch_id').agg(\n    records=('customer_id', 'size'),\n    filled=('customer_id', 'count'))\nb01_filled = sizes.loc['B01', 'filled']\nsizes")
    else:
        nb.code("sizes = None       # groupby branch_id, agg: records=('customer_id', 'size'), filled=('customer_id', 'count')\nb01_filled = None  # the filled value for B01")
    nb.code(f"check('B01 filled customer_id', safe(lambda: b01_filled), {F['b01_filled']})")
    nb.read('Why is filled smaller than records? Write the reason: the blank means a walk-in shopper.')

    # ---------------------------------------------------------------- step 3
    nb.step(3, 'A safe lookup: left merge, many-to-one, row counts', 'merge adds the branch details to every order. Many-to-one with how=left should keep every order.')
    nb.predict(f'orders has {R["orders"]:,} rows. How many rows will the merged table have?')
    if solution:
        nb.code("named = orders.merge(branches, on='branch_id', how='left', validate='m:1')\n"
                "log('orders + branches (left, m:1)', len(orders), len(named), 'every order keeps one row')\nprint(len(orders), len(named))")
    else:
        nb.code("named = None   # merge branches onto orders: on='branch_id', how='left', validate='m:1'\n"
                "# then add a line to the join log: log('orders + branches (left, m:1)', len(orders), len(named), 'every order keeps one row')")
    nb.code(f"check('rows after the left merge', safe(lambda: len(named)), {R['orders']})")
    nb.change("Delete validate='m:1' and run again. Does the row count change? Then put it back. validate costs nothing and protects you.")

    # ---------------------------------------------------------------- step 4
    nb.step(4, 'Lost rows: inner join and left join', 'An inner join keeps only keys found in both tables. Orders with no customer_id have no match.')
    nb.predict('Merge orders to customers on customer_id with an inner join. How many orders will be lost? Why?')
    if solution:
        nb.code("inner = orders.merge(customers, on='customer_id', how='inner', validate='m:1')\n"
                "left = orders.merge(customers, on='customer_id', how='left', validate='m:1')\n"
                "n_lost = len(orders) - len(inner)\n"
                "log('orders + customers (inner)', len(orders), len(inner), 'walk-in orders lost')\n"
                "log('orders + customers (left)', len(orders), len(left), 'every order kept')\nprint(n_lost)")
    else:
        nb.code("inner = None   # inner join of orders and customers on customer_id, validate='m:1'\nleft = None    # the same with how='left'\nn_lost = None  # rows of orders that the inner join lost\n"
                "# then two lines for the join log, as in step 3")
    nb.code(f"check('orders lost by the inner join', safe(lambda: n_lost), {F['lost']})\ncheck('left join keeps every order', safe(lambda: len(left)), {R['orders']})")
    nb.read('The lost orders have no customer_id. What share of the orders is that, and is losing them acceptable for a report on total sales?')
    nb.change("Repeat the left merge with indicator=True and run left['_merge'].value_counts(). How many orders show left_only? Which number from this step does it equal?")

    # ---------------------------------------------------------------- step 5
    nb.step(5, 'Fan-out: the merge that makes revenue too big', 'A one-to-many merge repeats the order once for every line. Adding order_value_ugx then counts it once per line.')
    nb.predict(f'Merge orders to order_lines on order_id with no validate. The lines average {F["lines_per_order"]:.1f} per order. Roughly how many times too big will the revenue be?')
    if solution:
        nb.code("fan = orders.merge(lines, on='order_id')\ninflated = fan['order_value_ugx'].sum()\ntrue_total = orders['order_value_ugx'].sum()\n"
                "ratio = inflated / true_total\nlog('orders + order_lines (no validate)', len(orders), len(fan), 'fan-out: rows multiplied')\nprint(len(fan), inflated, true_total, round(ratio, 2))")
    else:
        nb.code("fan = None         # merge orders and lines on order_id, with no validate\ninflated = None    # sum of order_value_ugx in fan\ntrue_total = None  # sum of order_value_ugx in orders\n"
                "ratio = None       # inflated divided by true_total\n# then a join log line")
    nb.code(f"check('rows after the fan-out merge', safe(lambda: len(fan)), {F['fan_rows']})\ncheck('inflated revenue', safe(lambda: inflated), {F['fan_sum']})\n"
            f"check('ratio', safe(lambda: ratio), {round(F['fan_ratio'], 4)}, 0.01)")
    nb.read(f'Compare the ratio (about {F["fan_ratio"]:.1f}) with the average number of lines per order (about {F["lines_per_order"]:.1f}). Why is the ratio larger? Hint: which orders have the most lines?')

    # ---------------------------------------------------------------- step 6
    nb.step(6, 'validate refuses the bad merge', "validate='m:1' says the right table must have each key once. order_lines repeats order_id, so pandas raises a MergeError.")
    nb.predict("Will orders.merge(lines, on='order_id', validate='m:1') run, or raise an error?")
    if solution:
        nb.code("try:\n    orders.merge(lines, on='order_id', validate='m:1')\n    message = 'no error'\nexcept pd.errors.MergeError as err:\n    message = str(err)\nprint(message)")
    else:
        nb.code("message = None   # run the merge with validate='m:1' inside try ... except pd.errors.MergeError as err, and keep str(err)")
    nb.code("check('validate refused the merge', safe(lambda: int('not a many-to-one merge' in message)), 1)")
    nb.change("Change validate to '1:m' (one-to-many). Does it run now? Why? Compare len() of the result with the fan-out table from step 5.")

    # ---------------------------------------------------------------- step 7
    nb.step(7, 'One table with category and month, using two many-to-one merges', 'Start from the many side (lines) and look up the one side twice. The row count must stay the same.')
    nb.predict(f'order_lines has {R["lines"]:,} rows. How many rows will full have after two many-to-one merges? Will the revenue change?')
    if solution:
        nb.code("full = lines.merge(products[['product_id', 'category']], on='product_id', how='left', validate='m:1')\n"
                "full = full.merge(orders[['order_id', 'branch_id', 'order_date']], on='order_id', how='left', validate='m:1')\n"
                "full['order_date'] = pd.to_datetime(full['order_date'])\nfull['month'] = full['order_date'].dt.strftime('%Y-%m')\n"
                "log('order_lines + products + orders', len(lines), len(full), 'two many-to-one merges')\nprint(len(full), full['line_revenue_ugx'].sum())")
    else:
        nb.code("full = None   # lines + category from products (on product_id), then branch_id and order_date from orders (on order_id), both m:1\n"
                "# then: order_date with pd.to_datetime, a month column with .dt.strftime('%Y-%m'), and a join log line")
    nb.code(f"check('rows in full', safe(lambda: len(full)), {F['full_rows']})\ncheck('revenue unchanged', safe(lambda: full['line_revenue_ugx'].sum()), {F['full_rev']})")
    nb.read('Why does the revenue of full equal the revenue of the orders file?')

    # ---------------------------------------------------------------- step 8
    nb.step(8, 'Dates: the weekday of every order', 'Convert text to a datetime first. Then .dt.day_name() gives the weekday.')
    nb.predict('Which weekday will have the highest revenue? Write a guess.')
    if solution:
        nb.code("orders['weekday'] = pd.to_datetime(orders['order_date']).dt.day_name()\nby_day = orders.groupby('weekday')['order_value_ugx'].sum()\ntop_day = by_day.idxmax()\nprint(by_day.sort_values(ascending=False))")
    else:
        nb.code("by_day = None    # make a weekday variable, group by it, sum order_value_ugx\ntop_day = None   # the weekday with the largest total (idxmax)")
    nb.code(f"check('revenue of the top weekday', safe(lambda: by_day[{F['top_day']!r}]), {F['top_day_rev']})\ncheck('top weekday', safe(lambda: int(top_day == {F['top_day']!r})), 1)")
    nb.read('How many times larger is the highest weekday than the lowest? Is that a pattern, or could it be chance? Write what you would need to know.')

    # ---------------------------------------------------------------- step 9
    nb.step(9, 'pivot_table: region by year', 'index is the variable down the side, columns is the variable across the top, margins=True adds the totals (All).')
    nb.predict('The bottom right cell of the pivot should equal one number you already know. Which one?')
    if solution:
        nb.code("with_region = orders.merge(branches[['branch_id', 'region']], on='branch_id', how='left', validate='m:1')\n"
                "with_region['year'] = pd.to_datetime(with_region['order_date']).dt.year\n"
                "pivot = with_region.pivot_table(index='region', columns='year', values='order_value_ugx', aggfunc='sum', margins=True)\npivot")
    else:
        nb.code("pivot = None   # merge region onto orders (m:1), add a year variable, then pivot_table with margins=True")
    nb.code(f"check('Central 2024', safe(lambda: pivot.loc['Central', 2024]), {F['central_2024']})\ncheck('grand total', safe(lambda: pivot.loc['All', 'All']), {F['rev']})")
    nb.change('Put payment_method across the top instead of year. What is the grand total now?')

    # ---------------------------------------------------------------- step 10
    nb.step(10, 'Keep: the join log and one finding', 'Your join log shows which merges kept, lost or multiplied rows. Write one finding with a number and its source table.')
    if solution:
        nb.code("log_table = pd.DataFrame(join_log)\nprint(log_table.to_string(index=False))\n\n"
                f"finding = 'Sales are highest in the Central region ({F['central_2024'] + F['central_2025']:,} UGX over 2024 and 2025, from the orders table, sample file). "
                f"An inner join to customers would have lost {F['lost']:,} walk-in orders.'\nprint(finding)")
    else:
        nb.code("log_table = None   # pd.DataFrame(join_log), then print it\nfinding = None      # one sentence with a number and its source table")
    nb.code("check('join log has five rows', safe(lambda: len(log_table)), 5)\ncheck('finding written', safe(lambda: int(len(finding) > 40)), 1)")
    nb.md('**Keep this notebook.** Save a copy to your Drive (File, Save a copy in Drive). Bring one merge from your own work to Session 10.')
    merge_checks(nb)
    nb.code('show_checks()')
    return nb
