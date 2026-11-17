"""Session 9: pandas III: group, join and reshape (groupby and aggregation, merge types, cardinality and fan-out, validate, pivot_table, datetime parts). Python lab in content/labs/s09_nb.py.

Every number on a slide, in a note, in the notebook checks or in the facilitator key is computed in facts() with pandas from the real course files (orders.csv, order_lines.csv ...).
Every code output shown on a slide is produced by running the code shown, here, in run().
"""
import contextlib
import io
import os
from functools import lru_cache
from pathlib import Path

import pandas as pd

BUILD = Path(__file__).resolve().parents[1]
DATA = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'data'

PRE = ("import pandas as pd\n"
       "orders = pd.read_csv('orders.csv')\nlines = pd.read_csv('order_lines.csv')\nbranches = pd.read_csv('branches.csv')\n"
       "products = pd.read_csv('products.csv')\ncustomers = pd.read_csv('customers.csv')\nreturns = pd.read_csv('returns.csv')\n")


def n(x):
    return f'{int(x):,}'


def run(code, pre=PRE):
    """Run the slide code in the data folder after the preamble; return the printed lines (the real output)."""
    old = os.getcwd()
    os.chdir(DATA)
    try:
        ns = {}
        exec(pre, ns)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            exec(code, ns)
    finally:
        os.chdir(old)
    return [l.rstrip() for l in buf.getvalue().rstrip('\n').split('\n')]


C_AGG = ("summary = orders.groupby('branch_id').agg(\n    orders=('order_id', 'count'),\n    revenue=('order_value_ugx', 'sum'),\n    average=('order_value_ugx', 'mean'))\n"
         "print(summary.round(0).astype(int).head(4))")
C_SIZE = ("check = orders.groupby('branch_id').agg(\n    records=('customer_id', 'size'),\n    filled=('customer_id', 'count'))\nprint(check.head(3))")
C_SAFE = ("before = len(orders)\nnamed = orders.merge(branches, on='branch_id',\n                     how='left', validate='m:1')\n"
          "print(before, len(named), len(named) == before)")
C_VALID = ("try:\n    orders.merge(lines, on='order_id',\n                 validate='m:1')\nexcept pd.errors.MergeError as err:\n    print(*str(err).split('; '), sep='\\n')")
C_FIX = ("per_order = lines.groupby('order_id').agg(\n    n_lines=('line_id', 'count'),\n    lines_total=('line_revenue_ugx', 'sum')\n).reset_index()\n"
         "checked = orders.merge(per_order, on='order_id',\n                       how='left', validate='1:1')\n"
         "a = checked.lines_total.sum()\nb = checked.order_value_ugx.sum()\nprint(len(checked), a == b)")
C_WEEK = ("import calendar\nd = pd.to_datetime(orders['order_date'])\norders['weekday'] = d.dt.day_name()\n"
          "by_day = (orders.groupby('weekday')\n          .order_value_ugx.sum())\nby_day = by_day.reindex(list(calendar.day_name))\n"
          "print(by_day.idxmax(), by_day.max())")
C_PIV = ("d = pd.to_datetime(named['order_date'])\nnamed['year'] = d.dt.year\n"
         "table = named.pivot_table(\n    index='region', columns='year', margins=True,\n    values='order_value_ugx', aggfunc='sum')\nprint(table.astype(int))")
PRE_NAMED = PRE + "named = orders.merge(branches, on='branch_id', how='left', validate='m:1')\n"


@lru_cache(maxsize=None)
def facts():
    o = pd.read_csv(DATA / 'orders.csv')
    l = pd.read_csv(DATA / 'order_lines.csv')
    p = pd.read_csv(DATA / 'products.csv')
    b = pd.read_csv(DATA / 'branches.csv')
    c = pd.read_csv(DATA / 'customers.csv')
    r = pd.read_csv(DATA / 'returns.csv')
    F = dict(rows=dict(orders=len(o), lines=len(l), products=len(p), branches=len(b), customers=len(c), returns=len(r)))
    F['rev'] = int(o.order_value_ugx.sum())
    F['lines_rev'] = int(l.line_revenue_ugx.sum())
    F['lines_match_orders'] = bool((l.groupby('order_id').line_revenue_ugx.sum() == o.set_index('order_id').order_value_ugx).all())
    F['n_branches'] = int(o.branch_id.nunique())
    g = o.groupby('branch_id').agg(orders=('order_id', 'count'), revenue=('order_value_ugx', 'sum'), average=('order_value_ugx', 'mean'))
    F['g'] = g
    F['b01_rev'], F['b01_orders'], F['b01_avg'] = int(g.loc['B01', 'revenue']), int(g.loc['B01', 'orders']), float(g.loc['B01', 'average'])
    F['b01_filled'] = int(o[o.branch_id == 'B01'].customer_id.count())
    F['top_branch'] = str(g.revenue.idxmax())
    F['top_branch_name'] = str(b.set_index('branch_id').loc[F['top_branch'], 'branch_name'])
    # join to customers
    inner = o.merge(c, on='customer_id', how='inner')
    left = o.merge(c, on='customer_id', how='left')
    F['inner_rows'], F['left_rows'] = len(inner), len(left)
    F['walkin'] = int(o.customer_id.isna().sum())
    F['lost'] = len(o) - len(inner)
    F['lost_pct'] = F['lost'] / len(o) * 100
    F['lost_rev'] = int(o.loc[o.customer_id.isna(), 'order_value_ugx'].sum())
    F['lost_rev_pct'] = F['lost_rev'] / F['rev'] * 100
    assert F['lost'] == F['walkin']
    # fan-out
    m = o.merge(l, on='order_id')
    F['fan_rows'] = len(m)
    F['fan_sum'] = int(m.order_value_ugx.sum())
    F['fan_ratio'] = F['fan_sum'] / F['rev']
    F['lines_per_order'] = len(l) / len(o)
    F['max_lines'] = int(l.groupby('order_id').size().max())
    # many-to-many
    F['mm_rows'] = len(l.merge(r, on='order_id'))
    F['mm_rows_2keys'] = len(l.merge(r, on=['order_id', 'product_id']))
    F['returns_orders'] = int(r.order_id.nunique())
    F['returns_lines_have_order'] = bool(r.order_id.isin(o.order_id).all())
    # one order with three distinct products for the fan-out picture
    gl = l.groupby('order_id').agg(k=('line_id', 'count'), d=('product_id', 'nunique'))
    ex_id = gl[(gl.k == 3) & (gl.d == 3)].index[0]
    F['ex_order'] = o[o.order_id == ex_id].iloc[0]
    F['ex_lines'] = l[l.order_id == ex_id].reset_index(drop=True)
    F['ex_n'] = len(F['ex_lines'])
    F['ex_value'] = int(F['ex_order'].order_value_ugx)
    assert F['ex_lines'].line_revenue_ugx.sum() == F['ex_value']
    F['ex_after'] = F['ex_value'] * F['ex_n']
    # category and month table (two many-to-one merges)
    full = l.merge(p[['product_id', 'category']], on='product_id', how='left', validate='m:1').merge(o[['order_id', 'branch_id', 'order_date']], on='order_id', how='left', validate='m:1')
    full['order_date'] = pd.to_datetime(full.order_date)
    full['month'] = full.order_date.dt.strftime('%Y-%m')
    F['full_rows'] = len(full)
    F['full_rev'] = int(full.line_revenue_ugx.sum())
    F['n_categories'] = int(full.category.nunique())
    pv = full.pivot_table(index='branch_id', columns='category', values='line_revenue_ugx', aggfunc='sum')
    F['pv_shape'] = pv.shape
    F['pv_b01_staples'] = int(pv.loc['B01', 'Staples'])
    F['pv_total'] = int(pv.sum().sum())
    det = full.groupby(['branch_id', 'category', 'month']).line_revenue_ugx.sum()
    F['detail_rows'] = len(det)
    F['b01_staples_dec'] = int(det.loc[('B01', 'Staples', '2024-12')])
    F['months'] = int(full.month.nunique())
    # dates on orders
    o2 = o.copy()
    o2['d'] = pd.to_datetime(o2.order_date)
    o2['weekday'] = o2.d.dt.day_name()
    o2['year'] = o2.d.dt.year
    o2['month'] = o2.d.dt.month
    wd = o2.groupby('weekday').order_value_ugx.sum()
    F['week'] = wd
    F['top_day'], F['top_day_rev'] = str(wd.idxmax()), int(wd.max())
    F['low_day'], F['low_day_rev'] = str(wd.idxmin()), int(wd.min())
    F['day_ratio'] = F['top_day_rev'] / F['low_day_rev']
    ry = o2.merge(b[['branch_id', 'region']], on='branch_id', how='left', validate='m:1').pivot_table(index='region', columns='year', values='order_value_ugx', aggfunc='sum', margins=True)
    F['reg_year'] = ry
    F['central_2024'], F['central_2025'] = int(ry.loc['Central', 2024]), int(ry.loc['Central', 2025])
    F['all_2024'], F['all_2025'] = int(ry.loc['All', 2024]), int(ry.loc['All', 2025])
    F['year_change_pct'] = (F['all_2025'] / F['all_2024'] - 1) * 100
    F['ex_date'] = str(F['ex_order'].order_date)
    F['ex_dt'] = pd.Timestamp(F['ex_date'])
    F['orders_2024'] = int((o2.year == 2024).sum())
    # excerpt for groupby picture: first two orders of three branches, in date order
    ex = pd.concat([o[o.branch_id == k].head(2) for k in ('B01', 'B02', 'B03')]).sort_values(['order_date', 'order_id'])
    F['gb_rows'] = [[s_, f'{v:,}'] for s_, v in zip(ex.branch_id, ex.order_value_ugx)]
    F['gb_sums'] = ex.groupby('branch_id').order_value_ugx.sum().to_dict()
    # excerpt for join types: two filled customers and one walk-in; two customers matched and one without an order here
    oo = pd.concat([o[o.customer_id.notna()].head(2), o[o.customer_id.isna()].head(1)]).sort_values('order_id')
    keys = set(oo.customer_id.dropna())
    cu = pd.concat([c[c.customer_id.isin(keys)], c[~c.customer_id.isin(keys)].head(1)]).sort_values('customer_id')
    F['jt_orders'] = [(str(a), '' if pd.isna(k) else str(k)) for a, k in zip(oo.order_id, oo.customer_id)]
    F['jt_customers'] = [(str(a), str(k)) for a, k in zip(cu.customer_id, cu.loyalty_tier)]
    lt, rt = oo[['order_id', 'customer_id']], cu[['customer_id', 'loyalty_tier']]
    F['jt'] = {}
    for how in ('inner', 'left', 'right', 'outer'):
        mm = lt.merge(rt, on='customer_id', how=how)
        F['jt'][how] = [['' if pd.isna(v) else str(v) for v in (x.order_id, x.customer_id, x.loyalty_tier)] for x in mm.itertuples()]
    # reshape excerpt: three branches by year
    by = o2[o2.branch_id.isin(['B01', 'B02', 'B03'])].groupby(['branch_id', 'year']).order_value_ugx.sum().reset_index()
    F['long_rows'] = [[a, str(y), f'{v:,}'] for a, y, v in by.itertuples(index=False)]
    wide = by.pivot_table(index='branch_id', columns='year', values='order_value_ugx', aggfunc='sum')
    F['wide_rows'] = [[a] + [f'{int(v):,}' for v in wide.loc[a]] for a in wide.index]
    F['wide_headers'] = ['branch_id', '2024', '2025']
    # other files for the work slide
    cv = pd.read_csv(DATA / 'clinic_visits.csv')
    F['clinic_rows'], F['clinic_districts'] = len(cv), int(cv.iloc[:, 0].nunique())
    F['clinic_cols'] = list(cv.columns)
    ln = pd.read_csv(DATA / 'loans.csv')
    F['loans_rows'] = len(ln)
    # real outputs of every code slide
    F['out'] = {k: run(v) for k, v in dict(agg=C_AGG, size=C_SIZE, safe=C_SAFE, valid=C_VALID, fix=C_FIX, week=C_WEEK).items()}
    F['out']['piv'] = run(C_PIV, PRE_NAMED)
    assert any(str(F['central_2024']) in l for l in F['out']['piv']) and any(str(F['rev']) in l for l in F['out']['piv'])
    F['valid_msg'] = ' '.join(F['out']['valid'])
    assert F['out']['safe'][0] == f'{len(o)} {len(o)} True'
    assert F['out']['fix'][0] == f'{len(o)} True'
    return F


def build():
    F = facts()
    R = F['rows']
    g = F['g']
    ex = F['ex_order']
    sess = dict(
        num=9, block='Module B: Python for data', short_title='pandas III group join reshape',
        title='pandas III: group, join and reshape',
        question='How do we answer a question that needs several groups and several tables, and trust the total?',
        outcomes=['Summarise records by group with groupby and named aggregation, and lay the result out with pivot_table',
                  'Merge tables on a join key, say what each join type keeps, and prove with row counts and validate that nothing was lost or multiplied',
                  'Read months and weekdays from a datetime variable and report revenue by branch, region and year'],
        outcome_icons=['chart', 'key', 'calendar'],
        outcome_note=('Here is what you can do by the end of today. You can summarise records by group, which is a PivotTable written as code, and lay the result out as a grid. '
                      'You can merge two tables on a join key, say which rows each kind of join keeps, and prove with a row count and with the validate option that no rows were lost and none were multiplied. '
                      'And you can pull months and weekdays out of a date and report revenue by branch, region and year. All of it runs on the Lakeside Mart files in a Google Colab notebook.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: picture, plain words, one example by hand'), (10, 'Break'), (45, 'Lab: predict, run, read, change'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: concepts first, then a Colab lab',
        plan_caption='Ideas with pictures first. Then you open the notebook. Then the checks and what you keep.',
        plan_note=('We have two hours. The first ten minutes bring back Session 8 and set the question for today. Then forty-five minutes of concepts with no laptops open, so you can watch the pictures and the recipes. '
                   'After a ten minute break you open the Colab notebook for a forty-five minute lab, where you predict, run, read and change. The last ten minutes are an exit check and what you keep. '
                   'The lab is where the learning sticks, so please protect that time.'),
        recall_from='Session 8',
        recall=[('The order dates arrive as text. What do you do before you use them as dates?', 'Convert them with pd.to_datetime, then check the data type again to prove it worked.'),
                ('You removed exact duplicate lines from a raw file. What goes in the data cleaning log?', 'The rule you used and the row count before and after, so someone else can trust the result.'),
                ('Two totals that should agree are different. What do you call that gap?', 'A reconciliation difference. Explain it or reduce it to zero. Never call it a residual, which is a model word.')],
        words=[('groupby and aggregation', 'Split records into groups by a key, then reduce each group to one number, such as a sum or a mean.'),
               ('Merge (join) and join key', 'Combine two tables by matching a shared variable. The join type says which unmatched records survive.'),
               ('Cardinality (one-to-many, many-to-one)', 'How many records on each side match one key value. It decides if a merge keeps, loses or multiplies rows.'),
               ('Fan-out (row multiplication) and lost rows', 'Fan-out: a merge repeats a record, so totals inflate. Lost rows: records with no match that an inner join drops.'),
               ('pivot_table (wide and long format)', 'A summary grid with one variable down the side and one across the top, which is wide format.')],
        word_icons=['chart', 'key', 'grid', 'cross', 'calendar'],
        words_note=('Five words for today. A groupby splits records into groups and an aggregation reduces each group to one number. A merge, also called a join, combines two tables on a join key. '
                    'Cardinality says how many records on each side match one key value. Fan-out, which is row multiplication, and lost rows are the two ways a merge goes wrong without an error message. '
                    'And pivot table lays a summary out as a grid, in wide format. We use all five before the end of the session.'),
        keep='Keep your Colab notebook: the revenue tables by branch, region and year, a join log with the row count before and after every merge, and one written finding.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab file', value='A join log'), dict(label='The habit', value='Count rows twice'), dict(label='Next session', value='SQL for analysts')]),
        keep_title='Save your notebook with its join log',
        next='Session 10: SQL for analysts. The same grouping and joining, written in the language every database understands.', next_label='Next session',
        keep_note=('Before you go, save your notebook with its join log. The log is your keepsake: for every merge, the row count before, the row count after, and a sentence saying whether the change is what you expected. '
                   'A colleague who reads that log can trust your totals without rerunning anything. Next session we write the same questions in SQL, so today is also the best preparation for it. '
                   'If anything was unclear, write the question down and bring it.'),
        cover_note=('Welcome back. Last session you cleaned a raw file and proved what you changed. Today your clean tables go to work. '
                    'We ask questions that need groups and several tables: which branch sells the most, in which category, in which month. '
                    'You will also meet a merge that runs without a single error and makes revenue more than five times too big. By the end you will know how to catch it.'),
        use_at_work='Group, merge and reshape tables, and prove with row counts that a total is right.',
        slides=[])
    S = sess['slides']

    # ------------------------------------------------------------------ 1 recall answers
    S.append(dict(kind='table', title='Answers to the three questions from Session 8', headers=['Question', 'Short answer'],
                  rows=[[q, a] for q, a in sess['recall']], widths=[5.2, 6.8], icons=['calendar', 'doc', 'calculator'],
                  notes=('Here are the answers to the three warm-up questions. Dates that arrive as text are converted with pd.to_datetime, and then you check the data type again to prove it worked. That same move opens the last topic today. '
                         'The data cleaning log records the rule and the row count before and after, which is exactly the habit we use again for merges. '
                         'And a reconciliation difference is the gap between two totals that should agree. A residual belongs to models, so we do not use that word here. Which of the three did you find hardest?')))

    # ------------------------------------------------------------------ 2 groupby picture
    S.append(dict(kind='wide', title='groupby splits the records into groups and reduces each group to one number',
                  visual=dict(kind='ds_split_apply', headers=['branch_id', 'order_value_ugx'], rows=F['gb_rows'], key=0, value=1, result_head='revenue_ugx'),
                  caption='An excerpt of six orders. Colours mark the groups. An aggregation turns many values into one.',
                  notes=('This is groupby, in three steps: split, apply, combine. On the left are six real orders from the Lakeside orders file, with the branch and the order value. '
                         'Step one splits them into one pile per branch. Step two applies an aggregation to each pile, here a sum, which turns many values into one. '
                         'Step three combines the answers into a small table with one record per group. In Excel you do the same when you drag branch to the rows box of a PivotTable and the value to the values box. '
                         'The numbers here are only for these six orders. How many records come back when you group by branch?')))

    # ------------------------------------------------------------------ 3 vocabulary
    S.append(dict(kind='table', title='The PivotTable, VLOOKUP and filter you know, and what pandas calls each',
                  headers=['In Excel', 'In pandas', 'Industry term'],
                  rows=[['PivotTable rows box', 'groupby(branch_id)', 'The grouping key: the variable that makes the groups'],
                        ['PivotTable values box: Sum, Count, Average', 'sum, count, mean', 'Aggregate functions (aggregation)'],
                        ['VLOOKUP or XLOOKUP', 'merge', 'Join on a join key (a many-to-one lookup)'],
                        ['A lookup column next to your full list (IFERROR hides the #N/A)', 'merge with how=left', 'Left join: keep every left record, NaN where no match'],
                        ['PivotTable with a field across the top', 'pivot_table', 'Wide format (long format is the opposite)']],
                  widths=[3.6, 3.2, 5.2], icons=['chart', 'calculator', 'key', 'check', 'grid'], note='Each pandas name is a real function name you will meet in documentation and in job tests.',
                  notes=('You already know every one of these tools from Excel, so here is the translation. The rows box of a PivotTable is the grouping key in groupby. '
                         'The values box, with Sum, Count or Average, is an aggregation. VLOOKUP becomes merge, which is a join on a join key. '
                         'A lookup column next to your whole list, where the missing ones show blank, is a left join. And a PivotTable with a field across the top is a pivot table in wide format. '
                         'The pandas names are the real function names, so you will see them in documentation, in tests at interviews and in other people\'s notebooks. Which row do you use most in Excel today?')))

    # ------------------------------------------------------------------ 4 named aggregation
    S.append(dict(kind='code', title='Named aggregation gives several answers per group in one step',
                  code='# orders.csv is already loaded as orders\n' + C_AGG, output=F['out']['agg'],
                  reads=['groupby names the variable that makes the groups: one group per branch.',
                         'Each line inside agg is a new column: its name, then the variable and the aggregate function.',
                         f'Branch B01 has {n(F["b01_orders"])} orders and revenue of UGX {n(F["b01_rev"])}.',
                         'These totals describe the 5 percent sample of till orders in the file.'],
                  notes=(f'Usually one number per group is not enough. A manager wants the count of orders, the revenue and the average order, side by side. In pandas that is agg with named aggregation. '
                         f'Each line inside agg makes one new column: the name you choose, then in brackets the variable and the aggregate function. The result has one record per branch and three variables. '
                         f'Branch B01 has {n(F["b01_orders"])} orders, revenue of {n(F["b01_rev"])} shillings and an average order of about {n(round(F["b01_avg"]))}. '
                         'All of these figures describe only the sample of till orders in the file. Which aggregate function would you add to see the largest order?')))

    # ------------------------------------------------------------------ 5 count vs size
    S.append(dict(kind='code', title='count skips missing values and size counts every record',
                  code='# orders is already loaded\n' + C_SIZE, output=F['out']['size'],
                  reads=['size counts the records in each group, filled or not.',
                         f'count counts only the filled values of one variable. Walk-in orders have a missing customer_id, so filled is smaller.',
                         f'In B01: {n(F["b01_orders"])} records but {n(F["b01_filled"])} filled customer_id values.',
                         'Say which you mean before you report a number of orders.'],
                  notes=(f'A small trap in aggregation. Size counts the records in each group. Count counts only the values that are filled in for one variable. '
                         f'In branch B01 there are {n(F["b01_orders"])} orders, but only {n(F["b01_filled"])} of them have a customer id, because the others are walk-in shoppers with a missing value. '
                         'So if you count customer ids you get a smaller number than if you count orders, and nothing warns you. Decide what you are counting, records or filled values, and use size or count to match. '
                         'Which one would you use for the number of orders?')))

    # ------------------------------------------------------------------ 6 VLOOKUP vs merge
    S.append(dict(kind='compare', title='VLOOKUP returns the first match and merge returns every match',
                  left=dict(head='VLOOKUP in Sheets', points=['Finds the first match and stops.', 'Fills one helper column at a time.', 'A missing key shows #N/A.']),
                  right=dict(head='merge in pandas', points=['Returns every match, one row per pair.', 'Adds all the variables you pick in one line.', 'A missing key shows NaN.']),
                  verdict='Returning every match is useful, and it means the row count can change.',
                  notes=('The second big idea today is bringing information in from another table, which is the job you give to VLOOKUP. VLOOKUP looks for your key in a second table and returns the first match, then stops. '
                         'You also fill one helper column at a time. In pandas the function is merge. It adds every variable you ask for in one line, and it does not stop at the first match. It returns every match. '
                         'When a key is not found, VLOOKUP shows hash N slash A, and pandas leaves NaN. Read the verdict. Returning every match is the whole power of a merge, and it is also why the row count can change under you. Have you ever seen a VLOOKUP list grow?')))

    # ------------------------------------------------------------------ 7 join types
    jt = F['jt']
    panels = [dict(title="inner join: how='inner'", rows=jt['inner'], keeps='Only keys found in both tables.'),
              dict(title="left join: how='left'", rows=jt['left'], keeps='Every left record. No match gives NaN.'),
              dict(title="right join: how='right'", rows=jt['right'], keeps='Every right record. No match gives NaN.'),
              dict(title="full outer join: how='outer'", rows=jt['outer'], keeps='Every record from both tables.')]
    S.append(dict(kind='wide', title='A join type decides which records without a match survive',
                  visual=dict(kind='ds_join_types', orders=F['jt_orders'], customers=F['jt_customers'], panels=panels),
                  caption='A real excerpt, joined on customer_id. Gold cells are NaN (missing).',
                  notes=('Here are the four join types, on a real excerpt. The left table has three orders. One of them is a walk-in with no customer id. The right table has three customers, and one of them has no order in the excerpt. '
                         'An inner join keeps only the keys found in both tables, so two rows. A left join keeps every order, and the walk-in gets NaN for the loyalty tier. '
                         'A right join keeps every customer, so the customer without an order appears with NaN for the order. And a full outer join keeps everything, four rows. '
                         'In practice you will use left and inner joins most. Which one would you use to list every order with its customer details?')))

    # ------------------------------------------------------------------ 8 lost rows
    S.append(dict(kind='stat', title=f'An inner join to customers loses {n(F["lost"])} orders, the walk-in sales', big=f'{F["lost_pct"]:.0f}%',
                  text=f'of the {n(R["orders"])} orders have no customer_id. An inner join with customers keeps {n(F["inner_rows"])} rows. The {n(F["lost"])} lost rows hold UGX {n(F["lost_rev"])} of revenue.',
                  waffle_label='orders in every 100 are lost by the inner join',
                  notes=(f'Now the first way a merge goes wrong without an error message: lost rows. The orders file has {n(R["orders"])} orders. Of those, {n(F["walkin"])} have no customer id, because the shopper was a walk-in. '
                         f'If you inner join orders to customers, those orders have no match, so they disappear. You keep {n(F["inner_rows"])} rows. The lost rows are about {F["lost_pct"]:.0f} in every 100 orders, and they hold {n(F["lost_rev"])} shillings of revenue. '
                         'Your report would say revenue is lower than the tills say, and nothing would warn you. The fix is a left join and a row count. Which join would you choose to keep every order?')))

    # ------------------------------------------------------------------ 9 cardinality table
    S.append(dict(kind='table', title='Cardinality tells you in advance whether a merge keeps, loses or multiplies rows',
                  headers=['Cardinality', 'Lakeside example', 'What happens to the row count'],
                  rows=[['many-to-one (m:1)', 'orders to branches on branch_id: each branch appears once.', f'Safe. Every order keeps one row: {n(R["orders"])} stays {n(R["orders"])}.'],
                        ['one-to-many (1:m)', f'orders to order_lines on order_id: about {F["lines_per_order"]:.1f} lines per order.', f'Fan-out. {n(R["orders"])} orders become {n(F["fan_rows"])} rows.'],
                        ['many-to-many (m:m)', 'order_lines to returns on order_id: both sides repeat the key.', f'Rows multiply: the lines of a returned order meet each of its returns. An inner join gives {n(F["mm_rows"])} rows, about {F["mm_rows"] / R["returns"]:.0f} times the {n(R["returns"])} returns. Join on order_id and product_id.']],
                  widths=[2.7, 5.1, 4.2], icons=['key', 'bag', 'cross'], note='Check first: is the join key unique on each side? A key that is unique on one side only is one-to-many.',
                  notes=(f'Cardinality is how many records on each side match one key value, and it tells you in advance what a merge will do. Merge orders to branches on branch id. Each branch appears once on the right, so this is many-to-one, and every order keeps exactly one row. '
                         f'Merge orders to order lines on order id. One order has about {F["lines_per_order"]:.1f} lines, so this is one-to-many, and {n(R["orders"])} orders become {n(F["fan_rows"])} rows. That is fan-out. '
                         f'Merge order lines to returns on order id and both sides repeat the key. That is many-to-many. The lines of each returned order meet each of its returns, so you get {n(F["mm_rows"])} rows, about {F["mm_rows"] / R["returns"]:.0f} times the {n(R["returns"])} returns. The fix is to join on order id and product id. Before any merge, ask whether the key is unique on each side.')))

    # ------------------------------------------------------------------ 10 fan-out picture
    lines_ex = [[str(r_.line_id), str(r_.product_id), f'{int(r_.line_revenue_ugx):,}'] for r_ in F['ex_lines'].itertuples()]
    S.append(dict(kind='idea', title='Fan-out repeats the order value on every line, so a sum counts it several times',
                  visual=dict(kind='ds_fanout', order=dict(order_id=str(ex.order_id), value=f'{F["ex_value"]:,}'), lines=lines_ex, total_each=f'{F["ex_value"]:,}', total_after=f'{F["ex_after"]:,}'),
                  lead='Fan-out (row multiplication): a one-to-many merge repeats the left record once for every match.',
                  points=[f'Order {ex.order_id} has {F["ex_n"]} lines, so it becomes {F["ex_n"]} rows.', 'order_value_ugx belongs to the whole order, so adding it up now counts it once per line.', 'No error message appears.'],
                  notes=(f'Here is fan-out, also called row multiplication, on one real order. Order {ex.order_id} is one record in the orders table, with an order value of {F["ex_value"]:,} shillings. '
                         f'It has {F["ex_n"]} records in the order lines table. When you merge on order id, the order record is repeated once for each line, so you get {F["ex_n"]} rows. The order value is a fact about the whole order, so it is now written {F["ex_n"]} times. '
                         f'If you add up that variable, you get {F["ex_after"]:,}, which is {F["ex_n"]} times the real {F["ex_value"]:,}. The merge ran without any error. How would you notice, if you did not look at the row count?')))

    # ------------------------------------------------------------------ 11 fan-out at scale
    S.append(dict(kind='idea', title=f'On the full file, fan-out makes revenue {F["fan_ratio"]:.1f} times too big',
                  visual=dict(kind='bars', items=[dict(label='True revenue (orders)', value=round(F['rev'] / 1e6, 1), text=f'{F["rev"] / 1e6:,.1f}M'),
                                                  dict(label='After the merge with order_lines', value=round(F['fan_sum'] / 1e6, 1), text=f'{F["fan_sum"] / 1e6:,.1f}M', hl=True)], unit=''),
                  lead=f'{n(R["orders"])} orders became {n(F["fan_rows"])} rows after the merge.',
                  points=[f'True revenue: UGX {n(F["rev"])}.', f'Inflated total: UGX {n(F["fan_sum"])}.', f'Ratio {F["fan_ratio"]:.1f}, above the {F["lines_per_order"]:.1f} times rows grew: big orders have more lines.'],
                  notes=(f'Now the same mistake on the whole orders file. The true revenue is {F["rev"] / 1e6:,.1f} million shillings. After merging orders to order lines and adding up the order value, the total is {F["fan_sum"] / 1e6:,.1f} million. '
                         f'That is {F["fan_ratio"]:.1f} times too big. Look at the number of rows: {n(R["orders"])} orders became {n(F["fan_rows"])} rows. Rows grew {F["lines_per_order"]:.1f} times, but the revenue grew {F["fan_ratio"]:.1f} times, because big orders have more lines, so they are repeated more often. '
                         'A manager who saw the bigger figure might celebrate. Which check would have caught this at once?')))

    # ------------------------------------------------------------------ 12 validate
    S.append(dict(kind='code', title="validate='m:1' makes pandas stop a merge that is not many-to-one",
                  code='# orders and lines are already loaded\n' + C_VALID, output=F['out']['valid'],
                  reads=['validate states the cardinality you expect: m:1 is many-to-one.',
                         'order_lines repeats order_id, so the right side is not unique and pandas raises a MergeError.',
                         'The merge never runs, so the revenue cannot inflate.',
                         "The other values are '1:1', '1:m' and 'm:m'."],
                  notes=('Here is the best protection. When you merge, tell pandas what cardinality you expect with the validate option. Here we ask for many-to-one, which means the key must be unique in the right table. '
                         'But order lines repeats the order id, so the right table is not unique. pandas stops with a MergeError and a message that says the merge keys are not unique in the right dataset. The merge never runs. '
                         'The other values you can give are one-to-one, one-to-many and many-to-many. Make validate a habit on every merge, because it turns a silent mistake into a loud one. Where in your own work would a loud error be better than a quiet wrong number?')))

    # ------------------------------------------------------------------ 13 four checks
    S.append(dict(kind='steps', title='Four checks around every merge protect the total',
                  steps=[dict(head='1 Key', text='Is it unique on each side? Name the cardinality.', icon='key'), dict(head='2 Count', text='Write down the row count before.', icon='calculator'),
                         dict(head='3 Validate', text="Merge with how and validate='m:1'.", icon='check'), dict(head='4 Compare', text='Row count after. Total after.', icon='magnifier')],
                  highlight=None, caption='Join log (an audit trail for merges): a small table with the step, rows before, rows after and a note, like the data cleaning log. A change you cannot explain is a stop sign.',
                  notes=('These are the four checks to run around every merge. One, check the key: is it unique on each side, and what is the cardinality? Two, write down the row count before. '
                         'Three, merge with an explicit how and with validate, so pandas can refuse a merge that is not what you expected. Four, compare the row count after, and compare the total of a variable that must not change. '
                         'Keep the counts in a join log. That is an audit trail for merges: a small table with the step, the rows before, the rows after and a note, just like the data cleaning log from Session 8. A change you cannot explain is a stop sign. Which check do you think people skip most often?')))

    # ------------------------------------------------------------------ 14 safe lookup
    S.append(dict(kind='code', title='A safe lookup: many-to-one, left join, row counts before and after',
                  code='# orders and branches are loaded\n' + C_SAFE, output=F['out']['safe'],
                  reads=['how=left keeps every order. validate says the join key must be unique in branches.',
                         'The printed line shows the count before, the count after and whether they are equal.',
                         f'{n(R["orders"])} orders in, {n(R["orders"])} rows out: nothing lost, nothing multiplied.',
                         'Add a line to your join log every time.'],
                  notes=(f'Here is the safe pattern for a lookup. Merge orders to branches with how equal to left and validate many-to-one. Before the merge we store the row count. After the merge we print the count before, the count after and whether the two are equal. '
                         f'Both counts are {n(R["orders"])}, so nothing was lost and nothing was multiplied. This is the line you copy into your join log. Many-to-one with a left join is the standard way to add names, categories and regions to a table of events. '
                         'What would the output show if two branches had the same branch id?')))

    # ------------------------------------------------------------------ 14b summarise first
    S.append(dict(kind='code', title='To use the many side, summarise it first and then merge one-to-one',
                  code='# orders and lines are loaded\n' + C_FIX, output=F['out']['fix'],
                  reads=['groupby reduces the lines to one record per order, with the number of lines and their total.',
                         "validate='1:1' confirms the key is unique on both sides.",
                         f'{n(R["orders"])} rows come out. The total of the lines equals the total of the orders: True. The == test is safe here because both totals are whole shillings; with decimals use abs(a - b) < 0.01.',
                         'The pattern: summarise the many side, then merge.'],
                  notes=(f'And when you do need information from the many side, such as the number of lines on each order, first reduce the lines to one record per order with groupby. Then merge one-to-one. '
                         f'The row count stays at {n(R["orders"])}, and the total of the line revenue equals the total of the order values, which prints True. That second check is a reconciliation: two totals that should agree do agree. '
                         'The pattern is simple to remember: summarise the many side first, then merge. What would you put in the summary if you needed the largest line on each order?')))

    # ------------------------------------------------------------------ 15 datetime parts
    parts = [('.dt.year', str(F['ex_dt'].year)), ('.dt.month', str(F['ex_dt'].month)), ('.dt.day', str(F['ex_dt'].day)), ('.dt.day_name()', F['ex_dt'].day_name()),
             ('.dt.month_name()', F['ex_dt'].month_name()), ('.dt.dayofweek', str(F['ex_dt'].dayofweek))]
    S.append(dict(kind='wide', title='Convert text to a datetime first, and then read its parts with .dt',
                  visual=dict(kind='ds_datetime_parts', text=F['ex_date'], parts=parts),
                  caption=f'Order {ex.order_id} was placed on {F["ex_date"]}. dayofweek counts Monday as 0.',
                  notes=(f'The last topic is dates. In Session 8 you saw that dates arrive as text. Step one is pd.to_datetime, which turns the text into a real datetime. Then the dot dt gives you the parts. '
                         f'For order {ex.order_id}, placed on {F["ex_date"]}, the year is {F["ex_dt"].year}, the month is {F["ex_dt"].month}, the day is {F["ex_dt"].day}, and the weekday name is {F["ex_dt"].day_name()}. '
                         'Day of week as a number counts Monday as zero. Text has no month or weekday, and it sorts alphabetically, so a month taken from text is a guess. With a month and a weekday you can group revenue by them. Which part would you group by to compare months?')))

    # ------------------------------------------------------------------ 16 dates code
    S.append(dict(kind='code', title='Revenue by weekday: derive the part, group by it, then put it in calendar order',
                  code=C_WEEK, output=F['out']['week'],
                  reads=['orders is already loaded. dt.day_name() gives the weekday name of each order.',
                         'groupby adds up the order value for each weekday.',
                         'reindex puts the rows in calendar order, Monday first. Without it they sort alphabetically.',
                         'idxmax gives the weekday with the largest total. max gives the total.'],
                  notes=(f'Here is revenue by weekday. We turn the date into a datetime, take the weekday name, group by it and add up the order value. Then reindex puts the rows in calendar order, because otherwise groupby sorts them alphabetically. '
                         f'The last line asks which weekday has the largest total. The answer is {F["top_day"]}, with {n(F["top_day_rev"])} shillings. The picture after this shows all seven days. '
                         'Notice that the date conversion is the first line. Without it nothing else works. Which other part of a date could you group by?')))

    # ------------------------------------------------------------------ 16b weekday bars
    wk = F['week']
    S.append(dict(kind='idea', title=f'{F["top_day"]} has the highest weekday revenue, about {F["day_ratio"]:.2f} times the lowest',
                  visual=dict(kind='bars', items=[dict(label=d_, value=round(float(wk[d_]) / 1e6, 1), text=f'{wk[d_] / 1e6:.1f}M', hl=(d_ == F['top_day']))
                                                   for d_ in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']], unit=''),
                  lead='Revenue in millions of UGX, by weekday, for the whole orders file.',
                  points=[f'Highest: {F["top_day"]}, UGX {n(F["top_day_rev"])}.', f'Lowest: {F["low_day"]}, UGX {n(F["low_day_rev"])}.', 'This describes the sample. We have no test yet to say if the gap is more than chance.'],
                  notes=(f'Here are all seven weekdays. {F["top_day"]} is the highest with {n(F["top_day_rev"])} shillings, and {F["low_day"]} is the lowest with {n(F["low_day_rev"])}. The highest day is about {F["day_ratio"]:.2f} times the lowest. '
                         'Is that a real pattern or just noise? We cannot say yet, because we have no measure of how much totals vary by chance. That comes in a later session. For now we report it as a description of this sample. '
                         'What would you want to check before telling a manager to staff more on that day?')))

    # ------------------------------------------------------------------ 17 pivot_table
    S.append(dict(kind='code', title='pivot_table lays a summary out as a grid, in wide format',
                  code='# named: the merged table from the safe lookup\n' + C_PIV, output=F['out']['piv'],
                  reads=['index: the variable down the side. columns: the variable across the top.',
                         'values and aggfunc: what to add up. margins=True adds the totals, labelled All.',
                         f'Central region in 2024: UGX {n(F["central_2024"])}.',
                         f'All branches: UGX {n(F["all_2024"])} in 2024 and UGX {n(F["all_2025"])} in 2025.'],
                  notes=('Here is pivot table, the PivotTable written as code. First we add the year to each order and merge the region from branches, many-to-one, so the row count is safe. '
                         'Then pivot_table takes the variable for the rows, the variable for the columns, the variable to add up and the aggregate function. Margins equal True adds the totals, which pandas labels All. '
                         f'The Central region sold {n(F["central_2024"])} shillings in 2024. All branches together sold {n(F["all_2024"])} in 2024 and {n(F["all_2025"])} in 2025. The bottom right cell must equal the true total, {n(F["rev"])}. '
                         'That is another check. What would you put across the top if you wanted to compare payment methods?')))

    # ------------------------------------------------------------------ 18 reshape
    S.append(dict(kind='wide', title='pivot_table makes wide format and melt makes long format',
                  visual=dict(kind='ds_reshape', long_headers=['branch_id', 'year', 'revenue_ugx'], long_rows=F['long_rows'], wide_headers=F['wide_headers'], wide_rows=F['wide_rows']),
                  caption='Revenue of three branches by year. The numbers are the same in both layouts.',
                  notes=('Reshaping means changing the layout of the same numbers. In long format, there is one record for each branch and year, so the year is a value in a column. In wide format there is one record for each branch, and each year has its own column. '
                         'pivot_table goes from long to wide, and melt goes back from wide to long. Long format is what groupby returns and what most chart tools want. Wide format is easier for people to read, and it is what a PivotTable shows. '
                         'The revenue numbers are identical, only the year moves between a row value and a column heading. You will use both layouts in your course project. Which layout would you send to a manager, and which would you give to a chart?')))

    # ------------------------------------------------------------------ 19 use at work
    S.append(dict(kind='table', title='Where you will use this at work: totals you can defend',
                  headers=['Your job', 'The tables you meet', 'What today lets you do'],
                  rows=[['Credit analyst at a bank in Kampala, using pandas', f'loans: one record per loan ({n(F["loans_rows"])} here). A real bank also has a borrowers table.', 'Merge with validate many-to-one, so no loan is counted twice, and report by branch and month.'],
                        ['Sales analyst at a retail chain, handing over to Power BI', 'Orders, lines, products, branches.', 'Build one clean table of revenue by branch, category and month, with its join log.'],
                        ['Monitoring officer at a district office or NGO', f'Clinic reports: one record per district per month ({n(F["clinic_rows"])} in our file).', 'Pivot to wide format for the quarterly report.'],
                        ['Finance officer at a SACCO or coffee cooperative', 'Member register and deliveries.', 'Left join to list members with no deliveries, and tell lost rows from zeros.']],
                  widths=[3.4, 4.3, 4.3], icons=['coin', 'chart', 'clinic', 'people'],
                  notes=('Where will you use this on Monday? Four examples. A credit analyst at a bank in Kampala who uses pandas merges loans to customers with validate many-to-one, so no loan is counted twice, and then reports arrears by branch and month. '
                         'A sales analyst at a retail chain builds one clean table of revenue by branch, category and month, and hands it to Power BI together with the join log. '
                         'A monitoring officer at a district office pivots clinic reports into wide format for the quarterly report. And a finance officer at a SACCO uses a left join to list members with no deliveries. '
                         'Which of these is closest to your job?')))

    # ------------------------------------------------------------------ 20 bridge
    S.append(dict(kind='code', title='Read the recipe before the lab: five lines do most of the work',
                  code=("orders.groupby('branch_id')['order_value_ugx'].sum()\n"
                        "named = orders.merge(branches, on='branch_id',\n                     how='left', validate='m:1')\n"
                        "len(orders) == len(named)\n"
                        "d = pd.to_datetime(named['order_date'])\n"
                        "named.pivot_table(\n    index='region', columns=d.dt.year,\n    values='order_value_ugx', aggfunc='sum')"),
                  reads=['First: one revenue total for each branch.', 'Second: add the branch details. validate stops a merge that would multiply rows.',
                         'Third: the row count check. It must say True.', 'Fourth: make the date a real datetime.', 'Fifth: a grid of region by year.'],
                  notes=('Before the lab, read the five lines that do most of the work. Line one adds up the revenue for each branch. Line two merges the branch details onto each order, with how left and validate many-to-one, so a merge that would multiply rows is refused. '
                         'Line three is the row count check and it must say True. Line four turns the date into a real datetime. Line five lays out a grid of region by year. '
                         'In the lab you will run these on the real files, predict each result before you run it, and keep a join log of the row counts. Which line will you check most carefully?')))

    # ------------------------------------------------------------------ 21 divider
    S.append(dict(kind='divider', title='Part 2: the Colab lab', lead='Close the slides. Open the notebook.', section='Lab',
                  notes=('That is the end of the ideas. Everything you need is on the slides you have just seen, and the notebook repeats each step. '
                         'Open the notebook for Session 9 in Google Colab. Run the first cell, which puts the course data files next to the notebook, and then the check cell. '
                         'In every step, write your prediction in the text cell before you run the code. Then read the output, and change one thing.')))

    # ------------------------------------------------------------------ 22 lab map
    S.append(dict(kind='steps', title='The lab has ten steps and ends with a join log you keep',
                  steps=[dict(head='1 to 2 Group', text='groupby, agg, count and size', icon='chart'), dict(head='3 Join safely', text='left merge, row counts', icon='key'),
                         dict(head='4 to 6 Break it', text='lost rows, fan-out, validate', icon='cross'), dict(head='7 to 9 Table', text='category, weekday, pivot', icon='calendar'),
                         dict(head='10 Keep', text='join log and one finding', icon='notebook')], highlight=None,
                  caption='Ten short tasks in 45 minutes. In each one, predict, run, read the output, and change one thing.',
                  notes=('Here is the map of the lab, in ten steps. Steps one and two, group and aggregate, then count versus size. Step three, a safe left merge with a row count check. Steps four to six, break things on purpose: the lost rows from an inner join, the fan-out, and validate refusing a merge. '
                         'Steps seven to nine build one table with category and month, read the weekday from a date and build a pivot table of region by year. Step ten writes the join log and one finding with a number in it. '
                         'Each task has a check that tells you whether your number matches. If it says not yet, read the output again before you ask me. Please do not skip the predictions.')))

    # ------------------------------------------------------------------ 23 check numbers
    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Revenue of branch B01, and of all eight branches', f'{n(F["b01_rev"])} and {n(F["rev"])}'],
                        ['Orders and filled customer_id in B01 (size, count)', f'{n(F["b01_orders"])} and {n(F["b01_filled"])}'],
                        ['Rows after the left merge to branches', f'{n(R["orders"])}: the same as before'],
                        ['Orders lost by an inner join to customers', f'{n(F["lost"])}, which is {F["lost_pct"]:.0f} percent'],
                        ['Rows after merging orders to order_lines, and the inflated revenue', f'{n(F["fan_rows"])} rows and {n(F["fan_sum"])}, which is {F["fan_ratio"]:.1f} times too big'],
                        ['Revenue on the weekday with the highest total', f'{F["top_day"]}, {n(F["top_day_rev"])}'],
                        ['Region by year pivot: Central 2024 and all branches 2025', f'{n(F["central_2024"])} and {n(F["all_2025"])}']],
                  widths=[7.4, 4.6], icons=['chart', 'bag', 'check', 'cross', 'calculator', 'calendar', 'grid'], note='If your number differs, find the task that went wrong. Do not change a number to match.',
                  notes=('Use this table as your own self-check. Nobody marks it. If your numbers match, carry on. If one does not, stop and call me, because the later tasks build on the earlier ones. '
                         'The most common causes are a merge on the wrong variable, a total taken from the wrong table, or a merge repeated in the same cell so that rows pile up. Do not change a number to make it match. Find out why it is different. '
                         'What does it mean if your row count after a left merge is bigger than before?')))

    # ------------------------------------------------------------------ 24 error cards
    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[['A row count after the merge is bigger than before', 'The right table repeats the key: fan-out.', "Add validate='m:1'. Find which key repeats. Summarise the right table first."],
                        ["KeyError: 'branch_name'", 'The variable is not in the table you are using.', 'Print the column names with .columns and check the spelling.'],
                        ['MergeError: not a many-to-one merge', 'That is validate working correctly.', 'Read the message. Decide whether the merge is wrong or the expectation is.'],
                        ['Weekday rows are in alphabetical order', 'groupby sorts the keys.', 'Add .reindex with the list of weekday names.'],
                        ['Totals double after running a cell twice', 'The cell merged into a table that was already merged.', 'Rerun from the cell that loads the files.']],
                  widths=[3.7, 4.0, 4.3], icons=['cross', 'cross', 'check', 'calendar', 'cross'],
                  notes=('Five messages and symptoms you may meet. A row count bigger after the merge means the right table repeats the key, so add validate and summarise the right side first. '
                         'A KeyError for a variable name means the variable is not in the table you are using, so print the column names. A MergeError that says not a many-to-one merge is validate doing its job, so read it before you silence it. '
                         'Weekdays in alphabetical order need reindex. And totals that double after you run a cell twice mean you merged into a table that was already merged, so rerun from the loading cell. Read the message first. It usually tells you the answer.')))

    # ------------------------------------------------------------------ 25 exit check
    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[[f'Order {ex.order_id} has {F["ex_n"]} lines and an order value of {F["ex_value"]:,}. What do you get when you add up order_value_ugx after merging orders to order_lines?', f'{F["ex_after"]:,}, which is {F["ex_n"]} times too big, because the order value is repeated on each of the {F["ex_n"]} rows.'],
                        ['You must list every order with its customer tier. Which join type, and why?', 'A left join from orders to customers. It keeps every order, including walk-ins, who get NaN for the tier.'],
                        ['Which option makes pandas refuse a merge where the right table repeats the key?', "validate='m:1' (many-to-one). It raises a MergeError before the merge runs."]],
                  widths=[5.8, 6.2], icons=['bag', 'key', 'check'],
                  notes=(f'Last, the exit check. Three questions. Write your answers before you look at mine. One, order {ex.order_id} has {F["ex_n"]} lines and an order value of {F["ex_value"]:,} shillings. What do you get when you add up the order value after merging orders to order lines? '
                         'Two, you must list every order with its customer tier. Which join type, and why? Three, which option makes pandas refuse a merge where the right table repeats the key? '
                         'The short answers are on the slide. If you got all three, you are ready for SQL next session. If one surprised you, look at that part of your notebook again tonight.')))

    # ------------------------------------------------------------------ facilitator
    sess['facilitator'] = dict(
        prep=['Open the Session 9 notebook in Colab on your own account before class. Run it top to bottom once and confirm that the check cells match the numbers in the key.',
              'Share the data.zip link or the uploaded zip with learners, so the first cell works for everyone. The notebook needs orders.csv, order_lines.csv, branches.csv, customers.csv and products.csv.',
              'Write the check table (slide 23) on the board before the lab.',
              'Concepts run with laptops closed. Ask learners to open Colab only after the Part 2 divider.',
              'All data is fictional and generated. The orders file is a 5 percent sample of till transactions, so revenue figures describe the sample.'],
        misconceptions=[('A join that runs without an error must be correct', f'A merge never checks that your totals are right. Fan-out raised revenue to {F["fan_ratio"]:.1f} times the truth with no message.'),
                        ('A left join is always safe', 'A left join keeps every left record, but it still multiplies rows when the right side repeats the key. Use validate.'),
                        ('count and size are the same', 'size counts records. count counts only the filled values of one variable, so it skips missing values.'),
                        ('A pivot table and groupby are different tools', 'pivot_table is groupby with one grouping variable moved across the top, so the same aggregation, in wide format.'),
                        ('The weekday can be read from the text date', 'Text has no weekday. Convert to datetime first, then use .dt.day_name().')],
        probes=[('What does groupby return when you group by branch_id?', 'One record per branch, holding the aggregate for each group.'),
                ('What is the difference between how=inner and how=left?', 'Inner keeps only keys found in both tables. Left keeps every left record and fills NaN where there is no match.'),
                ('What is the cardinality of orders to order_lines?', 'One-to-many: one order has many lines.'),
                ('What is fan-out and why is it dangerous?', 'A one-to-many merge repeats the left record, so any total of a left variable is multiplied. There is no error.'),
                ('How do you protect a merge?', 'Know the cardinality, count rows before and after, and set validate.'),
                ('Why reindex the weekdays?', 'groupby sorts keys alphabetically. Reindex puts them in calendar order.'),
                ('What is the difference between wide and long format?', 'Long has one record per value. Wide has a column per value. pivot_table goes long to wide and melt goes back.')],
        lab_steps=[('Step 1: groupby, agg, count and size', f'B01 revenue {n(F["b01_rev"])}, eight branches total {n(F["rev"])}, B01 has {n(F["b01_orders"])} orders and {n(F["b01_filled"])} filled customer_id.'),
                   ('Step 2: left merge to branches', f'Row count stays {n(R["orders"])}. A learner who merged branches without how=left may see the same number but should still say which join they used.'),
                   ('Step 3: lost rows, fan-out, validate', f'Inner join keeps {n(F["inner_rows"])} of {n(R["orders"])}: {n(F["lost"])} lost. The line merge gives {n(F["fan_rows"])} rows and {n(F["fan_sum"])}. validate raises the MergeError.'),
                   ('Step 4: category table, weekday and pivot', f'full has {n(F["full_rows"])} rows and the revenue still {n(F["full_rev"])}. {F["top_day"]} has the highest weekday revenue. The region by year pivot totals {n(F["rev"])}.'),
                   ('Step 5: join log and finding', 'Every row of the log shows a before and after count. The finding states a number and its source table. Reject a finding with no number.')],
        rescue=['If the concepts run over, shorten slide 3 (the Excel to pandas table) and slide 18 (reshape); the lab uses both ideas again.',
                'If only 30 minutes of lab remain, do steps 1, 2 and 3 and set steps 4 and 5 as homework.',
                'If Colab will not open the data zip, run the data setup cell again and upload data.zip from the computer instead of using a link.',
                'If a learner has no laptop, pair them with a neighbour: one types, one predicts aloud.'],
        after=['Share the notebook and the deck again for learners who were absent.', 'Ask each learner to keep the join log and bring one merge from their own work to Session 10.', 'Note any question you could not answer and open the next session with it.'],
        lab_answer_key=[['Step 1 PREDICT: will the eight branch revenues add up to the total of the orders file?', f'Yes: {n(F["rev"])}. Every order belongs to exactly one branch.'],
                        ['Step 1 READ: why is filled smaller than records?', f'Walk-in orders have a missing customer_id, and count skips missing values. B01: {n(F["b01_filled"])} against {n(F["b01_orders"])}.'],
                        ['Step 2 PREDICT: how many rows after a left merge to branches?', f'{n(R["orders"])}. Each branch appears once, so the merge is many-to-one.'],
                        ['Step 3 PREDICT: how many orders does the inner join to customers lose?', f'{n(F["lost"])}, the walk-in orders, which is {F["lost_pct"]:.0f} percent, holding UGX {n(F["lost_rev"])}.'],
                        ['Step 3 CHANGE: merge lines to returns on order_id only. How many rows?', f'{n(F["mm_rows"])}, many-to-many. Merging on order_id and product_id gives {n(F["mm_rows_2keys"])}.'],
                        ['Step 3 READ: why is the ratio not exactly the average lines per order?', f'The ratio is {F["fan_ratio"]:.2f} against {F["lines_per_order"]:.2f} lines per order. Orders with many lines have larger values and count more.'],
                        ['Step 4 READ: which weekday leads, and is it a pattern?', f'{F["top_day"]} with {n(F["top_day_rev"])}, about {F["day_ratio"]:.2f} times {F["low_day"]}. We have no test yet, so it is only a description.'],
                        ['Step 4 CHANGE: build the pivot with payment_method across the top.', 'Three columns: Card, Cash and Mobile money, and the grand total is unchanged.'],
                        ['Step 5 READ: what does the join log tell a reader?', 'Which merges kept the row count, which lost rows and which multiplied them, so they can trust the totals.']])
    return sess
