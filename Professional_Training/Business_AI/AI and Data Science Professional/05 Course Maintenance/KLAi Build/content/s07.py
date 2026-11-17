"""Session 7: pandas I, load, look and filter (DataFrame, Series, index, read_csv, shape, dtypes, info, describe, missing values, selecting columns,
Boolean mask, query, sort_values, value_counts, loc and iloc). Python lab: content/labs/s07_nb.py.

Every number on a slide, in a note or in the lab checks is computed in facts() with pandas from the real files in the course data folder.
Every output shown on a slide is the real output of the pandas call written beside it, captured here. Nothing is typed from memory.
"""
import io
from functools import lru_cache
from pathlib import Path

import pandas as pd

BUILD = Path(__file__).resolve().parents[1]
DATA = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'data'


def n(x):
    return f'{int(x):,}'


def lines(obj):
    """The text pandas prints for obj, as a list of lines."""
    return (obj if isinstance(obj, str) else repr(obj)).rstrip('\n').split('\n')


@lru_cache(maxsize=None)
def facts():
    o = pd.read_csv(DATA / 'orders.csv')
    F = dict(o=o)
    F['rows'], F['cols'] = o.shape
    F['n_missing'] = int(o.isna().sum()['customer_id'])
    F['missing_pct'] = F['n_missing'] / len(o) * 100
    F['filled'] = int(o.customer_id.notna().sum())
    F['isna_lines'] = lines(o.isna().sum())
    F['dtypes_lines'] = lines(o.dtypes)
    buf = io.StringIO()
    o.info(buf=buf)
    F['info_lines'] = buf.getvalue().rstrip('\n').split('\n')
    v = o.order_value_ugx
    F['describe_lines'] = lines(v.describe().round().astype(int))
    F['mean'], F['median'], F['std'] = float(v.mean()), float(v.median()), float(v.std())
    F['mean_over_median'] = F['mean'] / F['median']
    F['max'], F['min'] = int(v.max()), int(v.min())
    F['total'] = int(v.sum())
    F['n_branches'] = int(o.branch_id.nunique())
    # filters
    b, m = o.branch_id == 'B04', o.payment_method == 'Mobile money'
    F['n_jinja'] = int(b.sum())
    F['n_mm'] = int(m.sum())
    F['n_both'] = int((b & m).sum())
    F['n_either'] = int((b | m).sum())
    F['n_only_jinja'] = int((b & ~m).sum())
    F['n_only_mm'] = int((~b & m).sum())
    F['n_neither'] = int((~b & ~m).sum())
    F['n_not_mm'] = int((~m).sum())
    jinja = o[b]
    F['jinja'] = jinja
    F['jinja_pay'] = jinja.payment_method.value_counts()
    F['jinja_pay_lines'] = lines(jinja.payment_method.value_counts())
    F['n_query'] = len(o.query("branch_id == 'B04' and payment_method == 'Mobile money'"))
    F['n_query_amp'] = len(o.query("branch_id == 'B04' & payment_method == 'Mobile money'"))
    assert F['n_query'] == F['n_both'] == F['n_query_amp']
    F['jinja_first_label'] = int(jinja.index[0])
    F['jinja_first_order'] = str(jinja.iloc[0].order_id)
    F['jinja_first_value'] = int(jinja.iloc[0].order_value_ugx)
    assert jinja.loc[F['jinja_first_label'], 'order_value_ugx'] == F['jinja_first_value']
    # mask excerpt: a window across the boundary between two branches
    start = F['jinja_first_label'] - 4
    win = o.iloc[start:start + 7]
    F['mask_win'] = win
    F['mask_vals'] = (win.branch_id == 'B04').tolist()
    # errors
    try:
        o[o.branch_id == 'B04' and o.payment_method == 'Mobile money']
    except Exception as e:  # noqa: BLE001
        F['err_and'] = f'{type(e).__name__}: {e}'
    try:
        o[o.branch_id == 'B04' & o.payment_method == 'Mobile money']
    except Exception as e:  # noqa: BLE001
        F['err_amp'] = f'{type(e).__name__}: {e}'
    try:
        compile("orders[orders['branch_id'] = 'B04']", '<cell>', 'exec')
    except SyntaxError as e:  # noqa: BLE001
        F['err_syntax'] = 'SyntaxError: ' + e.msg
    b2, m2 = o.branch_id.isin(['B01', 'B04']), o.payment_method.str.contains('Mobile')
    F['n_isin'] = int(b2.sum())
    F['n_between'] = int(o.order_value_ugx.between(10000, 50000).sum())
    F['n_contains'] = int(m2.sum())
    assert F['n_contains'] == int((o.payment_method == 'Mobile money').sum())
    F['err_and_short'] = F['err_and'].split('. Use')[0] + '.'
    F['err_amp_short'] = F['err_amp']
    # sort and top
    top = o.sort_values('order_value_ugx', ascending=False).head(5)
    F['top5'] = top
    F['top10_sum'] = int(o.order_value_ugx.nlargest(10).sum())
    F['top_order'] = str(top.iloc[0].order_id)
    F['top_branch'] = str(top.iloc[0].branch_id)
    F['top_value'] = int(top.iloc[0].order_value_ugx)
    F['n_over_million'] = int((v > 1_000_000).sum())
    # counts
    pc = o.payment_method.value_counts()
    F['pay'] = {k: int(x) for k, x in pc.items()}
    F['pay_pct'] = {k: float(x) / len(o) * 100 for k, x in pc.items()}
    F['pay_lines'] = lines(pc)
    # loc and iloc
    F['loc_lines'] = lines(o.loc[0:2, ['order_id', 'branch_id']])
    F['iloc_lines'] = lines(o.iloc[0:3, 0:2])
    F['head_branch_lines'] = lines(o['branch_id'].head(3))
    F['head_two_lines'] = lines(o[['branch_id', 'order_value_ugx']].head(3))
    # profile (the lab deliverable)
    prof = pd.DataFrame({'dtype': o.dtypes.astype(str), 'missing': o.isna().sum()})
    prof['missing_pct'] = (prof.missing / len(o) * 100).round(1)
    F['profile'] = prof
    # work examples
    loans = pd.read_csv(DATA / 'loans.csv')
    F['loans_rows'], F['loans_no_income'], F['loans_defaults'] = len(loans), int(loans.monthly_income_ugx.isna().sum()), int(loans.default.sum())
    cl = pd.read_csv(DATA / 'clinic_visits.csv')
    F['clinic_rows'], F['clinic_blank'], F['clinic_districts'] = len(cl), int(cl.total_visits.isna().sum()), int(cl.district.nunique())
    F['clinic_one'] = int((cl.district == cl.district.iloc[0]).sum())
    F['clinic_first_district'] = str(cl.district.iloc[0])
    # shape tag of the recipe
    F['recipe_out'] = [f'({F["rows"]}, {F["cols"]})', str(F['n_jinja']), str(jinja.payment_method.value_counts().to_dict())]
    return F


def s(x):
    return '' if pd.isna(x) else str(x)


def build():
    F = facts()
    o = F['o']
    pay = F['pay']
    sess = dict(
        num=7, block='Module B: Python for data', short_title='pandas I load, look and filter',
        title='pandas I: load, look and filter a table of 30,229 orders',
        question=f'How do we open a file of {n(F["rows"])} rows, look at it, and ask it the first questions?',
        outcomes=['Load a CSV file into a pandas DataFrame and take a first look: shape, data types, missing values and describe',
                  'Select columns and filter rows with a Boolean mask, join two conditions with & and |, and write the same filter with query',
                  'Sort, count with value_counts, pick rows with loc and iloc, and save a data profile of the file'],
        outcome_icons=['grid', 'magnifier', 'doc'],
        outcome_note=('Here is what you can do by the end of today. You can load a CSV file into a pandas DataFrame and take a first look at it: its shape, its data types, its missing values and a summary. '
                      'You can select columns and filter rows with a Boolean mask, and join two conditions. You can sort, count and pick rows with loc and iloc. '
                      'And you leave with a data profile of the Lakeside Mart orders file, saved as a small CSV that you can reuse on any file.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: picture, plain words, one example by hand'), (10, 'Break'), (45, 'Lab: predict, run, read, change'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: concepts first, then a pandas lab',
        plan_caption='Ideas with pictures first. Then you open the notebook. Then the checks and what you keep.',
        plan_note=('We have two hours. The first ten minutes bring back Session 6 and set the question for today. Then forty-five minutes of concepts, with laptops closed, so you can follow the pictures and the real output on the slides. '
                   'After a ten minute break we open a Colab notebook for a forty-five minute lab on the Lakeside Mart orders. In every step you predict, run, read the result and change one thing. '
                   'The last ten minutes are the exit check and what you keep. The lab is where the learning sticks, so please protect that time.'),
        recall_from='Session 6',
        recall=[('You wrote a function that gives a loyalty tier from spend. How did you test it?', 'Run it on examples whose answer you already know, including the values exactly on each tier boundary.'),
                ('In Excel you drag a formula down 5,000 rows. What does a for loop do instead?', 'It repeats the same steps once for each item in a list, so you write the step one time.'),
                ('What does the word return do inside a function?', 'It hands the result back to the code that called the function, so you can store it or print it.')],
        words=[('DataFrame', 'A table held in Python memory, with labelled rows and named columns. In Excel words: one tab of a workbook.'),
               ('Series', 'One column of a DataFrame. It has a name, a data type and the same index as the table.'),
               ('Index', 'The row labels down the left edge of a DataFrame. A fresh file is labelled 0, 1, 2 and so on.'),
               ('Boolean mask (Boolean indexing)', 'A column of True and False values, one per row, used to keep only the rows marked True.'),
               ('Missing value (NaN)', 'A cell with no value. pandas shows it as NaN, SQL as NULL, and Excel as a blank cell.')],
        word_icons=['grid', 'tag', 'pin', 'check', 'question'],
        words_note=('Five words for today. A DataFrame is a table held in Python memory. A Series is one column of that table. The index is the set of row labels. '
                    'A Boolean mask is a column of True and False that chooses which rows to keep, and the technique is called Boolean indexing. And a missing value is a cell with no value, which pandas shows as NaN. '
                    'You already do every one of these things in Excel. Only the names are new.'),
        keep='Keep your notebook and the file orders_profile.csv: a data profile with one row for each variable, giving its data type, how many values are missing and the share missing.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab file', value='A data profile'), dict(label='The key habit', value='Look, then filter'), dict(label='Next session', value='Cleaning the mess')]),
        keep_title='Save your notebook and the orders_profile.csv file',
        next='Session 8: pandas II, cleaning the mess. We clean a raw export and prove its total. Project milestone 1.',
        next_label='Next session',
        keep_note=('Before you go, save your notebook to Google Drive and download the file orders_profile.csv. That small file is your keepsake from today: one row for each variable, with its data type and how much is missing. '
                   'You can build the same profile for any file at work in about a minute. Next session we meet a raw export with eight planted defects, and we clean it and prove the total. '
                   'If anything was unclear today, write the question down and bring it.'),
        cover_note=('Welcome back. Until now you have worked with a few numbers and a price list. Today we open the real Lakeside Mart orders file, thirty thousand two hundred and twenty nine rows, and we start asking it questions in Python. '
                    'You will load it into a pandas DataFrame, look at it before you trust it, and filter it. Everything you do has a spreadsheet twin, and we will name it each time.'),
        use_at_work='Load any CSV, look before you trust it, then filter and count with pandas.',
        slides=[])
    S = sess['slides']
    mw = F['mask_win']

    # ---- 1 answers
    S.append(dict(kind='table', title='Answers to the three questions from Session 6', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in sess['recall']],
                  widths=[5.2, 6.8], icons=['check', 'gear', 'doc'],
                  notes=('Here are the answers to the three warm-up questions. You test a function by running it on examples whose answers you already know, and you include the edge values, the ones exactly on a boundary. '
                         'A for loop repeats the same steps once for each item in a list, so you write the step one time instead of dragging a formula down. '
                         'And return hands the result back to the code that called the function. Today we use the same testing habit on every pandas answer, because we check each one against a count we can verify. Which of the three was hardest?')))

    # ---- 2 DataFrame anatomy
    h5 = o.head(5)
    S.append(dict(kind='wide', title='A pandas DataFrame is a table in memory, and its index labels the rows',
                  visual=dict(kind='ds_dataframe', headers=list(o.columns), rows=[[s(v) for v in r] for r in h5.itertuples(index=False)], index=list(h5.index), shape=f'({n(F["rows"])}, {F["cols"]})', series_col='branch_id', name='orders'),
                  caption='A Series is one column of a DataFrame. The shape is rows first, then columns.',
                  notes=(f'Here are the first five rows of the Lakeside Mart orders file, held as a pandas DataFrame. A DataFrame is a table in the memory of your notebook. The grey column on the left is the index, the label of each row. '
                         f'It starts at zero, because Python counts from zero, where Excel starts at one. The names across the top are the column names. Each column is a variable, and the red box outlines one of them, branch_id. One column on its own is called a Series. '
                         f'The shape of the whole table is {n(F["rows"])} rows by {F["cols"]} columns. Which column here would you call an identifier?')))

    # ---- 3 vocabulary table
    S.append(dict(kind='table', title='The Excel word, the pandas word and what each means',
                  headers=['In Excel', 'In pandas', 'Plain meaning'],
                  rows=[['A tab', 'DataFrame', 'A table held in Python memory.'], ['A column', 'Series (a variable)', 'One column, with a name and a data type.'], ['Row numbers', 'Index', 'The label of each row.'],
                        ['AutoFilter', 'Boolean indexing', 'Keep the rows where a test is True.'], ['Sort A to Z', 'sort_values', 'Order the rows by a column.'], ['PivotTable count', 'value_counts', 'Count each different value.']],
                  widths=[2.4, 3.4, 6.1], icons=['grid', 'tag', 'pin', 'magnifier', 'chart', 'calculator'],
                  note='A row is called a record or an observation. A column is called a variable, or a feature in machine learning.',
                  notes=('You already know every part of this from Excel, so here is the translation. A tab is a DataFrame. A column is a Series, and in statistics words it is a variable. The row numbers are the index. '
                         'AutoFilter becomes Boolean indexing, which keeps the rows where a test is true. Sort becomes sort_values, and a PivotTable count becomes value_counts. '
                         'A row is a record, also called an observation, and a column is a variable, which machine learning calls a feature. Which of these six jobs do you do most often in Excel?')))

    # ---- 4 read_csv
    S.append(dict(kind='steps', title='read_csv turns a file into a DataFrame, and then we look before we ask',
                  steps=[dict(head='orders.csv', text='A text file: values separated by commas', icon='folder'), dict(head='pd.read_csv', text='Reads the file into memory', icon='gear'),
                         dict(head='DataFrame', text='Named orders, 30,229 rows', icon='grid'), dict(head='Look first', text='shape, dtypes, head, info, describe', icon='magnifier')], highlight=1,
                  caption='CSV means comma-separated values. In Colab the file sits next to the notebook, so its name is enough. pd is the usual short name for the pandas library.',
                  notes=('Every pandas job starts the same way. The file is orders dot csv, a plain text file where each line is a row and commas separate the values. The function pd dot read csv reads it into memory and gives you a DataFrame. '
                         'We store it under a name, here orders, and the name is ours to choose, so pick one that says what is inside. The letters pd are the usual short name for the pandas library. '
                         'Then comes the habit we practise today: look at the data before you ask it anything. What would go wrong if you skipped the looking?')))

    # ---- 5 shape and dtypes
    S.append(dict(kind='wide', title='shape gives the size, and dtypes gives the data type of every column',
                  visual=dict(kind='ds_console', panels=[
                      dict(code=["orders = pd.read_csv('orders.csv')", 'orders.shape'], out=[f'({F["rows"]}, {F["cols"]})'], notes=[(0, f'{n(F["rows"])} records (rows) and {F["cols"]} variables (columns). shape has no brackets after it.')]),
                      dict(code=['orders.dtypes'], out=F['dtypes_lines'], hl=[1, 5], notes=[(1, 'object means text (a string; pandas 3 and later shows str). order_date is stored as text, so it cannot yet be sorted as a date.'), (5, 'int64 is a whole number. promo_week is a 0 or 1 flag.')])]),
                  caption='A data type is how a column stores its values. Session 8 converts the dates.',
                  notes=(f'Now two quick looks. The attribute shape gives rows first, then columns: {n(F["rows"])} by {F["cols"]}. It is an attribute, a fact stored on the table, so it has no round brackets. '
                         'Next, dtypes lists the data type of every column. Python calls text object, which pandas 3 and later shows as str, and whole numbers int64. Notice that order_date says object. The dates are stored as text, so Python cannot yet sort them as dates or take their month. '
                         'We fix that in Session 8. And promo_week is a whole number that only holds zero or one. Which other column here is text?')))

    # ---- 6 info
    S.append(dict(kind='wide', title='info lists each column with how many values are filled, and customer_id is short',
                  visual=dict(kind='ds_console', panels=[dict(code=['orders.info()'], out=F['info_lines'], hl=[8], notes=[(8, f'Only {n(F["filled"])} of {n(F["rows"])} orders have a customer_id. The rest are missing.'), (3, 'Non-Null Count: how many cells hold a value.'), (12, 'Python lists the data types it found.')])]),
                  caption='info is a method: it has round brackets. Non-null means "not missing".',
                  notes=(f'The method info gives the table card of a DataFrame. For every column it shows the count of cells that hold a value, called the non-null count, and the data type. The table has {n(F["rows"])} entries. '
                         f'Six columns are full. But customer_id has only {n(F["filled"])} values, so the rest are missing. That is the first thing a good analyst spots. Notice that info is a method, so it has round brackets, and shape was an attribute, so it did not. '
                         'What does the last line before memory usage tell you about the file?')))

    # ---- 7 missing values
    S.append(dict(kind='idea', title=f'isna().sum() counts the missing values, and {F["missing_pct"]:.0f} percent of orders have no customer_id',
                  visual=dict(kind='ds_console', panels=[dict(code=['orders.isna().sum()'], out=F['isna_lines'], hl=[3], notes=[])]),
                  lead=f'A missing value (NaN) is a cell with no value. {n(F["n_missing"])} orders have no customer_id.',
                  points=['isna() marks each empty cell True. sum() adds the Trues.', 'Ask what the blank means. Here it is a walk-in shopper.', f'Do not delete {F["missing_pct"]:.0f} percent of the orders.'],
                  notes=(f'To count the missing values, chain two calls. isna marks every empty cell as True, and sum adds the Trues for each column. The answer: {n(F["n_missing"])} orders have no customer id, which is {F["missing_pct"]:.1f} percent. '
                         'Remember Session 2: the data dictionary says a blank customer id is a walk-in, a shopper with no loyalty number. So the blank carries information, and deleting those rows would throw away three orders in ten. '
                         'In pandas this blank is shown as NaN, short for not a number. Where have you seen blanks that mean something in your own files?')))

    # ---- 8 describe
    S.append(dict(kind='wide', title=f'describe summarises a numeric variable, and the mean is {F["mean_over_median"]:.2f} times the median',
                  visual=dict(kind='ds_console', panels=[dict(code=["orders['order_value_ugx'].describe().round().astype(int)"], out=F['describe_lines'], hl=[1, 5, 7],
                                                              notes=[(1, f'mean: the arithmetic mean, UGX {n(F["mean"])}'), (5, f'50% is the median: UGX {n(F["median"])}. Half the orders are smaller.'), (7, f'max: UGX {n(F["max"])}, one very large order')])]),
                  caption='A few very large orders pull the mean above the median: the variable is right-skewed.',
                  notes=(f'The method describe summarises a numeric variable. Count is the number of values. The mean is {n(F["mean"])} shillings, the sum divided by the count. The line marked fifty percent is the median, {n(F["median"])}, the middle value: half the orders are smaller. '
                         f'The mean is {F["mean_over_median"]:.2f} times the median, because a few very large orders pull it up. Statisticians call that a right-skewed variable. The largest order is {n(F["max"])} shillings. '
                         'So which number would you quote as the typical order, the mean or the median?')))

    # ---- 9 data types table
    S.append(dict(kind='table', title='pandas data types and the variable types they usually store',
                  headers=['pandas dtype', 'Stores', 'Example in our files'],
                  rows=[['object (shown as str in pandas 3 and later)', 'Text (a string)', 'order_id, branch_id, order_date'], ['int64', 'Whole numbers', 'promo_week, order_value_ugx'], ['float64', 'Numbers with decimals, and NaN', 'monthly_income_ugx in loans.csv'],
                        ['bool', 'True or False', 'A Boolean mask'], ['datetime64', 'Dates and times', 'order_date after Session 8']],
                  widths=[2.6, 4.2, 5.1], icons=['tag', 'calculator', 'coin', 'check', 'calendar'],
                  note='A whole-number column that has a missing value becomes float64, because NaN is a float.',
                  notes=('A table of the data types you will meet. Object holds text. Int64 holds whole numbers, like promo week and the order value. Float64 holds numbers with decimals, and also any number column that has a missing value, '
                         'because NaN is stored as a float. You will see that in the loans file, where monthly income has blanks. Bool holds True and False, which is what a mask is made of. And datetime64 holds real dates, which we create in Session 8. '
                         'Remember that the data type is how the cell stores a value. The variable type, numeric or categorical, is how it is measured. Which type surprised you?')))

    # ---- 10 first look routine
    S.append(dict(kind='steps', title='The first look at any file: five calls before any question',
                  steps=[dict(head='shape', text='How many rows and columns?', icon='grid'), dict(head='dtypes', text='Is each type right?', icon='tag'), dict(head='head', text='Do the rows look sane?', icon='doc'),
                         dict(head='isna().sum()', text='What is missing?', icon='question'), dict(head='describe', text='Are the numbers plausible?', icon='chart')], highlight=None,
                  caption='This routine is the start of exploratory data analysis (EDA): getting to know a dataset before you answer questions with it.',
                  notes=('Here is the routine you will use on every new file for the rest of your career. First, shape: how many rows and columns. Second, dtypes: is each column stored as the right type. Third, head: do the first rows look sensible. '
                         'Fourth, isna and sum: what is missing. Fifth, describe: are the numbers plausible, with a sensible minimum and maximum. It takes about a minute and it catches most of the surprises. '
                         'This whole habit is called exploratory data analysis, or EDA. Which of the five would have warned you about the dates?')))

    # ---- 11 select columns
    S.append(dict(kind='wide', title='One column name returns a Series, and a list of names returns a DataFrame',
                  visual=dict(kind='ds_console', panels=[
                      dict(code=["orders['branch_id'].head(3)"], out=F['head_branch_lines'], notes=[(3, 'A Series: one column. The last line gives its name and data type.')]),
                      dict(code=["orders[['branch_id', 'order_value_ugx']].head(3)"], out=F['head_two_lines'], notes=[(0, 'A DataFrame: two columns. The inner brackets make the list.')])]),
                  caption='Selecting columns is like hiding the other columns in Excel. head(3) keeps three rows.',
                  notes=('Selecting columns. Put one column name inside square brackets and you get a Series, one column with its index. Put a list of names, which means a second pair of square brackets inside the first, and you get a smaller DataFrame. '
                         'That is why you see double brackets in so much pandas code: the outer pair is the selection, and the inner pair is the list. Both outputs here are cut to three rows with head. '
                         'The last line of the Series output gives its name and data type. Which would you use to get just the order values?')))

    # ---- 12 mask
    S.append(dict(kind='wide', title='A Boolean mask is a column of True and False that chooses the rows to keep',
                  visual=dict(kind='ds_mask', headers=['order_id', 'branch_id'], rows=[[s(r.order_id), s(r.branch_id)] for r in mw.itertuples()], index=list(mw.index), mask=F['mask_vals'], cond="branch_id == 'B04'"),
                  caption='The test builds the mask. The mask in square brackets after orders keeps the True rows.',
                  notes=('This is the idea behind every filter. Step one: we have the rows. Step two: a test, branch id equals B04, is applied to every row, and it produces a mask, a column of True and False with one value per row. '
                         'A Boolean is a value that is only ever True or False. Step three: pandas keeps only the rows where the mask is True. This is Boolean indexing, and it is what AutoFilter does for you behind the scenes. '
                         'Look at the index on the right: the kept rows keep their old labels. We come back to that. Why are the first four rows False?')))

    # ---- 13 filter result
    S.append(dict(kind='wide', title=f'Filter, count and look: {n(F["n_jinja"])} orders were sold at Jinja',
                  visual=dict(kind='ds_console', panels=[dict(code=["jinja = orders[orders['branch_id'] == 'B04']", 'len(jinja)'], out=[str(F['n_jinja'])], notes=[(0, 'len gives the number of rows. Report it beside every filtered figure.')]),
                                                         dict(code=["jinja['payment_method'].value_counts()"], out=F['jinja_pay_lines'], hl=[1], notes=[(1, f'Mobile money leads at Jinja: {n(F["jinja_pay"]["Mobile money"])} orders.')])]),
                  caption='B04 is the Jinja branch. value_counts counts each different value of a Series, like a PivotTable count.',
                  notes=(f'Now a real filter. We keep the orders where branch id is B04, the Jinja branch, and store them in a new DataFrame called jinja. The function len gives the number of rows, {n(F["n_jinja"])}. '
                         f'Always write that row count beside any figure you report from a filtered table. Then value counts on the payment method column counts each different value, like a PivotTable count. '
                         f'At Jinja, Mobile money leads with {n(F["jinja_pay"]["Mobile money"])} orders, then cash and card. Does Mobile money lead across all branches too?')))

    # ---- 14 value_counts bars
    S.append(dict(kind='idea', title=f'value_counts on all {n(F["rows"])} orders shows Mobile money and cash nearly level',
                  visual=dict(kind='bars', items=[dict(label=f'{k} ({F["pay_pct"][k]:.1f}%)', value=pay[k], text=f'{pay[k]:,}', hl=(k == 'Mobile money')) for k in ('Mobile money', 'Cash', 'Card')], size=17),
                  lead='value_counts counts each different value of one variable.',
                  points=['It sorts the counts from largest to smallest.', 'value_counts(normalize=True) returns shares instead of counts.', f'The three counts add up to {n(sum(pay.values()))}, the number of orders.'],
                  notes=(f'The method value counts is the pandas PivotTable count. On the whole orders file, Mobile money has {n(pay["Mobile money"])} orders, cash {n(pay["Cash"])} and card {n(pay["Card"])}. '
                         f'As shares, that is {F["pay_pct"]["Mobile money"]:.1f}, {F["pay_pct"]["Cash"]:.1f} and {F["pay_pct"]["Card"]:.1f} percent. With the option normalize equals True you get the shares directly. '
                         f'A good check is that the three counts add up to {n(sum(pay.values()))}, the number of orders, because every order has exactly one payment method. What would it mean if they added to less?')))

    # ---- 15 two conditions
    S.append(dict(kind='wide', title='Join two conditions with & for and, | for or and ~ for not',
                  visual=dict(kind='ds_venn', a=f'Jinja (B04): {n(F["n_jinja"])}', b=f'Mobile money: {n(F["n_mm"])}', only_a=F['n_only_jinja'], both=F['n_both'], only_b=F['n_only_mm'], neither=F['n_neither'], total=F['rows'],
                              ops=[('&', 'and: both are True', n(F['n_both']), 'Jinja and Mobile money'), ('|', 'or: at least one is True', n(F['n_either']), 'Jinja or Mobile money'), ('~', 'not: flips True and False', n(F['n_not_mm']), 'not Mobile money')]),
                  caption='Real counts from the orders file. Circles are not to scale. Put each test in round brackets.',
                  notes=(f'Two conditions are two masks, and you combine them. The ampersand means and: both must be True. Jinja and Mobile money gives {n(F["n_both"])} orders, the gold overlap. '
                         f'The vertical bar means or: at least one is True. Jinja or Mobile money gives {n(F["n_either"])}. The tilde means not: it flips every True and False, so not Mobile money gives {n(F["n_not_mm"])}. '
                         f'The four regions add up to all {n(F["rows"])} orders. In code, wrap each condition in its own round brackets. Which count would you use to find the share of Jinja orders paid by Mobile money?')))

    # ---- 16 the two errors
    S.append(dict(kind='wide', title='Writing and instead of &, or leaving out the brackets, fails with a confusing error',
                  visual=dict(kind='ds_console', panels=[
                      dict(code=["orders[orders['branch_id'] == 'B04' and orders['payment_method'] == 'Mobile money']"], out=[F['err_and_short']], hl=[0], notes=[]),
                      dict(code=["orders[orders['branch_id'] == 'B04' & orders['payment_method'] == 'Mobile money']"], out=__import__('textwrap').wrap(F['err_amp_short'], 66), hl=[0, 1], notes=[])]),
                  caption='Both errors come from running these lines. Fix: join with &, each test in round brackets.',
                  notes=('Two traps, and you will meet both. The Python word and does not work on a whole column, so pandas stops and says the truth value of a Series is ambiguous. Use the ampersand. '
                         'Then the second trap: the ampersand without brackets. Python does the ampersand before the comparisons, so it tries to combine a text column with a True, and the message mentions something called rand underscore, which tells you nothing. '
                         'The fix is the same every time: put each test in its own round brackets. When you see these two messages, think brackets and ampersand. What do you do first when an error message looks strange?')))

    # ---- 17 query
    S.append(dict(kind='wide', title=f'query writes the same filter as text, and both give {n(F["n_both"])} orders',
                  visual=dict(kind='ds_console', panels=[
                      dict(code=["mm_jinja = orders[(orders['branch_id'] == 'B04') &", "                  (orders['payment_method'] == 'Mobile money')]", 'len(mm_jinja)'], out=[str(F['n_both'])], notes=[(0, 'Boolean indexing')]),
                      dict(code=["mm_jinja = orders.query(\"branch_id == 'B04' and payment_method == 'Mobile money'\")", 'len(mm_jinja)'], out=[str(F['n_query'])], notes=[(0, 'query: the condition is text. and, or, & and | all work.')])]),
                  caption='Use whichever you read more easily. query is shorter when there are many conditions.',
                  notes=(f'Here is the same filter written two ways. The first is Boolean indexing: two masks joined with the ampersand, each in round brackets. The second uses the query method, where the whole condition is written as a piece of text. '
                         f'Inside that text you can write and, or, or the symbols, and you do not repeat the name of the DataFrame. Both return {n(F["n_both"])} orders. '
                         'Use whichever you can read more easily, and remember that the text goes in quotes inside the brackets. Which of the two would you prefer for a filter with five conditions?')))

    # ---- 17b more filters
    S.append(dict(kind='table', title='Four more filters you will use every week: isin, between, str.contains and nunique',
                  headers=['pandas method', 'Excel twin', 'What it does', 'On orders'],
                  rows=[['isin', 'OR of two tests', 'True where branch_id is B01 or B04', f'{n(F["n_isin"])} orders'],
                        ['between', 'AND of two tests', 'True where order_value_ugx is 10,000 to 50,000, ends included', f'{n(F["n_between"])} orders'],
                        ['str.contains', 'SEARCH', 'True where payment_method holds the text Mobile', f'{n(F["n_contains"])} orders'],
                        ['nunique', 'COUNTUNIQUE', 'How many different branch_id values', f'{F["n_branches"]} branches']],
                  widths=[2.4, 2.4, 5.2, 2.0], icons=['check', 'calculator', 'magnifier', 'tag'],
                  note='The first three each build a mask, so put them inside the square brackets after orders to keep the True rows. nunique returns one number.',
                  notes=(f'Four more tools that you will use every week. The method isin keeps the rows whose value is in a list, so branches B01 and B04 give {n(F["n_isin"])} orders. '
                         f'The method between keeps values from a low end to a high end, with both ends included: {n(F["n_between"])} orders from 10,000 to 50,000 shillings. '
                         f'The method str dot contains finds rows whose text holds a piece of text, such as Mobile, and gives {n(F["n_contains"])} orders. And nunique counts the different values in a column: {F["n_branches"]} branches. '
                         'The first three produce masks, so they go inside the square brackets after the DataFrame, exactly like the filters we have just written. Which of these would you use to keep only two districts?')))

    # ---- 18 sort
    t5 = F['top5']
    S.append(dict(kind='table', title=f'sort_values puts the largest orders first, and the top order is UGX {n(F["top_value"])}',
                  headers=['order_id', 'order_date', 'branch_id', 'order_value_ugx'],
                  rows=[[s(r.order_id), s(r.order_date), s(r.branch_id), n(r.order_value_ugx)] for r in t5.itertuples()],
                  widths=[2.6, 2.8, 2.4, 4.1], icons=['coin', 'coin', 'coin', 'coin', 'coin'],
                  note="Code: orders.sort_values('order_value_ugx', ascending=False).head(5). ascending=False puts the largest first. nlargest(5) gives the same rows.",
                  notes=(f'Sorting. The method sort values orders the rows by one column. With ascending equals False the largest comes first, and head of five keeps the top five. These are the five largest orders in the file. '
                         f'The largest is {s(t5.iloc[0].order_id)}, at {n(F["top_value"])} shillings, which is {F["top_value"] / F["median"]:.0f} times the median order. The method nlargest gives the same result in one call. '
                         'In Sessions 2 and 3 you asked whether such an order is a real sale or a typing error. The sort finds it. It cannot decide that for you. Who would you ask?')))

    # ---- 19 loc and iloc
    j5 = F['jinja'].head(5)
    S.append(dict(kind='wide', title='iloc counts positions and loc reads labels, and after a filter the two differ',
                  visual=dict(kind='ds_loc_iloc', headers=['order_id', 'branch_id', 'order_value_ugx'], rows=[[s(r.order_id), s(r.branch_id), s(r.order_value_ugx)] for r in j5.itertuples()], labels=list(j5.index),
                              iloc_code='jinja.iloc[0:2]', iloc_say='By position, counting from 0. The end is left out: positions 0 and 1, so 2 rows.',
                              loc_code=f'jinja.loc[{j5.index[0]}:{j5.index[2]}]', loc_say=f'By label. The end is included: labels {j5.index[0]}, {j5.index[1]} and {j5.index[2]}, so 3 rows.'),
                  caption='The filter kept the old labels: position 0 is label 14060. Label 0 does not exist here.',
                  notes=(f'Two ways to pick rows. The attribute iloc selects by position, counting from zero. Position zero is the first row, whatever its label. The end of a slice is left out, so zero to two gives two rows. '
                         f'The attribute loc selects by label, the value in the index. Here the Jinja rows kept their old labels, starting at {j5.index[0]}. The end of a loc slice is included, so these three labels give three rows. '
                         'These two behave differently at the end, and they disagree after any filter. Use loc when you mean a label, and iloc when you mean a position. Which would you use for the first row?')))

    # ---- 20 loc with columns
    S.append(dict(kind='wide', title='loc and iloc take rows first, then columns, and give the same rows on a fresh index',
                  visual=dict(kind='ds_console', panels=[
                      dict(code=["orders.loc[0:2, ['order_id', 'branch_id']]"], out=F['loc_lines'], notes=[(0, 'loc: rows with labels 0 to 2 (3 rows), and two named columns.')]),
                      dict(code=['orders.iloc[0:3, 0:2]'], out=F['iloc_lines'], notes=[(0, 'iloc: positions 0 up to 3 (3 rows), and positions 0 and 1 for the columns.')])]),
                  caption='On a fresh index both lines return the same rows. The slice ends still behave differently.',
                  notes=('Both loc and iloc take rows first, then a comma, then columns. With loc you name the columns. With iloc you give their positions. These two lines return the same first three rows and the same first two columns. '
                         'Look at the end of each slice. Loc from zero to two includes label two, so it gives three rows. Iloc from zero to three leaves out position three, so it also gives three rows. '
                         'On a fresh index the labels equal the positions, so it is easy to mix them up. The trouble starts after a filter. Which do you think is safer to read in code written by someone else?')))

    # ---- 21 three habits
    S.append(dict(kind='statement', title='Three habits keep a filtered answer honest',
                  lead='A filter that runs without an error can still be wrong.',
                  points=[f'Write the row count beside the result: len(jinja) is {n(F["n_jinja"])}.', 'Check one number a second way, for example a filter in Sheets.', 'Look at the mask: its sum() counts the True rows.'],
                  icons=['calculator', 'magnifier', 'check'],
                  notes=('Three habits for today and every day. First, write the row count beside any filtered result, so the reader knows how many rows a figure covers. Second, check one number a second way. In the lab you will repeat two of the filters in Google Sheets with AutoFilter. '
                         'Third, look at the mask itself: summing a mask counts its True values, so it tells you how many rows the filter will keep before you apply it. A filter that runs without an error can still be wrong, '
                         'for instance with a wrong spelling or the wrong brackets. Which habit do you already have from Excel?')))

    # ---- 22 use at work
    S.append(dict(kind='table', title='Where you will use this at work: load, look, filter and count',
                  headers=['Your job', 'The file you meet', 'What today lets you do'],
                  rows=[['Credit analyst at a bank, with pandas', f'loans.csv: {n(F["loans_rows"])} loans, {n(F["loans_no_income"])} with no monthly income.', f'Filter default equal to 1 ({n(F["loans_defaults"])} loans) and count the blanks.'],
                        ['Health records officer at a district office', f'Clinic visits: {n(F["clinic_rows"])} district-months, {F["clinic_blank"]} blank.', f'Keep one district ({F["clinic_one"]} months) and find the blank months.'],
                        ['Sales analyst before a Power BI report', f'orders.csv: {n(F["rows"])} orders.', f'Count Jinja Mobile money orders ({n(F["n_both"])}) in one line.'],
                        ['Officer at a SACCO or cooperative, using Excel', 'A monthly export of member payments.', 'Repeat the same filter every month by running the notebook.']],
                  widths=[3.3, 4.4, 4.2], icons=['coin', 'clinic', 'chart', 'people'],
                  notes=('Where will you use this on Monday? A credit analyst at a bank with the loans file can load it, count the loans with no monthly income, and filter the defaulted loans. '
                         f'A health records officer can keep one district out of the {F["clinic_districts"]} and find its blank months. A sales analyst preparing a Power BI report can answer a question like how many Jinja orders were paid by Mobile money in one line, and check it against the report later. '
                         'And an officer at a SACCO or a cooperative who uses Excel can write the filter once and run it every month on the new export. Which of these is closest to your job?')))

    # ---- 23 bridge
    S.append(dict(kind='code', title='Read the recipe before the lab: seven lines load, size and filter the file',
                  code="import pandas as pd\norders = pd.read_csv('orders.csv')\nprint(orders.shape)\njinja = orders[orders['branch_id'] == 'B04']\nprint(len(jinja))\npay = jinja['payment_method'].value_counts()\nprint(pay.to_dict())",
                  output=F['recipe_out'],
                  reads=['Lines 1 and 2: bring in pandas, then load the file.', 'Line 3 prints the shape: rows, then columns.', 'Line 4 keeps the Jinja rows.', f'Line 5 prints how many: {n(F["n_jinja"])}.', 'Lines 6 and 7 count the payment methods at Jinja and print them as a dictionary.'],
                  notes=('Before the lab, read this recipe. Line one brings in pandas under the short name pd. Line two loads the file into a DataFrame called orders. Line three prints the shape. '
                         f'Line four keeps the rows where the branch is B04. Line five prints how many: {n(F["n_jinja"])}. Lines six and seven count the payment methods among those rows and print them. The output panel shows what the lines really printed when we ran them. '
                         'In the notebook you will not copy this. You will write each step yourself and use the checks to see whether you are right. Which line would you change to look at a different branch?')))

    # ---- 24 divider
    S.append(dict(kind='divider', title='Part 2: the pandas lab', lead='Close the slides. Open the notebook.', section='Lab',
                  notes=('That is the end of the ideas. Everything you need is on the slides you have just seen, and the notebook repeats each step. '
                         'Open the Session 7 notebook in Google Colab, run the first two cells, and upload data.zip when it asks. Then work down the notebook. '
                         'In every step, predict the answer first, then run the cell, then read the output, then change one thing. A cell with None and the words your code here is yours to fill. The check cells will say OK or NOT YET.')))

    # ---- 25 lab map
    S.append(dict(kind='steps', title='The lab has seven steps, and you keep a data profile at the end',
                  steps=[dict(head='1 Load', text='read_csv and shape', icon='folder'), dict(head='2 Look', text='missing, describe', icon='magnifier'), dict(head='3 Filter', text='mask and &', icon='check'),
                         dict(head='4 Query, sort', text='top ten, counts', icon='chart'), dict(head='5 loc, iloc, save', text='profile CSV', icon='doc')], highlight=None,
                  caption='Seven steps in 45 minutes, grouped in five boxes. Each step: predict, run, read, change one thing.',
                  notes=('Here is the map of the lab. Step one, load the file and read its shape. Step two, count the missing values and describe the order values, and compare the mean with the median. '
                         'Step three, filter with a Boolean mask. Step four, join two conditions and repeat with query. Step five, sort for the top ten and count the payment methods. Step six, pick rows with loc and iloc. '
                         'Step seven, build the data profile and save it. In every step, predict first. Please do not skip the predictions, because that is where you find out what you actually understand.')))

    # ---- 26 check numbers
    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Shape of orders', f'({n(F["rows"])}, {F["cols"]})'], ['Missing customer_id, and its share', f'{n(F["n_missing"])}, which is {F["missing_pct"]:.1f} percent'], ['Mean and median of order_value_ugx', f'{n(F["mean"])} and {n(F["median"])}'],
                        ['Orders at branch B04', n(F['n_jinja'])], ['B04 and Mobile money, and B04 or Mobile money', f'{n(F["n_both"])} and {n(F["n_either"])}'], ['Largest order_value_ugx, and its order_id', f'{n(F["top_value"])}, {F["top_order"]}'],
                        ['Orders paid by Mobile money, Cash, Card', f'{n(pay["Mobile money"])}, {n(pay["Cash"])}, {n(pay["Card"])}'], ['Label of the first B04 row, and its order_id', f'{F["jinja_first_label"]}, {F["jinja_first_order"]}']],
                  widths=[7.4, 4.6], icons=['grid', 'question', 'calculator', 'shop', 'check', 'coin', 'chart', 'pin'], note='If your number differs, find the step that went wrong. Do not change a number to match.',
                  notes=('Use this table as your own self-check. Nobody marks it. If your numbers match, carry on. If one does not, stop and ask, because later steps use the earlier ones. '
                         'The most common causes are a missing round bracket around one condition, a double equals sign written as a single one, and a filter that you applied to the wrong DataFrame. '
                         'Do not change a number to make it match. Find out why it is different. What does it mean if your count for Jinja is larger than the table says?')))

    # ---- 27 error cards
    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[['ValueError: truth value of a Series is ambiguous', 'You wrote and or or between two tests.', 'Use & or |, with each test in round brackets.'],
                        ['TypeError mentioning rand_', 'You left out the round brackets around a test.', 'Wrap each test: (a == 1) & (b == 2).'],
                        ['KeyError on a column name', 'The name is misspelt or has the wrong case.', 'Print orders.columns and copy the name.'],
                        [F['err_syntax'], 'You wrote one = where a test needs ==.', 'Use == to test and = to store.'],
                        ['Your count is 0', 'The text does not match, such as b04 for B04.', 'Check the value with value_counts first.']],
                  widths=[4.0, 4.0, 4.0], icons=['cross', 'cross', 'cross', 'cross', 'cross'],
                  notes=('Five messages you may meet. The truth value of a Series is ambiguous means you wrote and or or between two tests, so use the ampersand or the bar. '
                         'A type error that mentions rand underscore means you left out the round brackets. A key error is almost always a misspelt column name, so print the columns and copy. '
                         'A syntax error that suggests you meant a double equals sign means you used one equals sign where the test needs two. And a count of zero usually means the text does not match, such as a lower case b. '
                         'Read the last line of the message first. It usually tells you the answer.')))

    # ---- 28 exit check
    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[['What is the difference between a DataFrame and a Series?', 'A DataFrame is a whole table. A Series is one column of it, with the same index.'],
                        ['A filter with two tests gives a TypeError that mentions rand_. What is the most likely cause?', 'The two tests are not each in round brackets, so & is applied too early.'],
                        [f'jinja has {n(F["n_jinja"])} rows and keeps its old labels. Does iloc with position 0 give the same row as loc with label 0?', f'No. Position 0 is the first row, label {F["jinja_first_label"]}. Label 0 is not in jinja, so loc gives a KeyError.']],
                  widths=[5.6, 6.4], icons=['grid', 'cross', 'pin'],
                  notes=('Last, the exit check. Three questions. Write your answers before you look at mine. One, what is the difference between a DataFrame and a Series? '
                         'Two, a filter with two tests gives a type error that mentions rand underscore. What is the most likely cause? '
                         'Three, the jinja table keeps its old labels. Does iloc zero give the same row as loc zero? The short answers are on the slide. If you got all three, you are ready for session eight. If one surprised you, look at that step of the notebook again tonight.')))

    # ------------------------------------------------------------------ facilitator
    sess['facilitator'] = dict(
        prep=['Open the deck and the Session 7 notebook in Colab before anyone arrives. Run it once with the solution version to confirm the data upload step works on your laptop.',
              'Check that data.zip is on every learner laptop, or share the link. The notebook asks for the upload only once.',
              'Write the check table (slide 27 of the deck) on the board before the lab.',
              'Concepts run with laptops closed. Ask learners to open the notebook only after the Part 2 divider.',
              'Remind learners that all data is fictional and generated. orders.csv is a 5 percent sample of till orders.'],
        misconceptions=[('and and or work between two conditions in pandas', 'On a column, Python and or or raises an error. Use & and |, with each test in round brackets.'),
                        ('loc and iloc are the same', 'iloc counts positions from 0 and leaves out the slice end. loc reads index labels and includes the slice end.'),
                        ('A filter changes the original table', 'A filter makes a new DataFrame. The original orders is unchanged.'),
                        ('A missing customer_id is a mistake to delete', f'Here {n(F["n_missing"])} blanks are walk-in shoppers. Ask what the blank means before you drop anything.'),
                        ('The index is a column of data', 'The index is the label of each row. After a filter it keeps the old labels.')],
        probes=[('What is the shape of orders, and what does each number mean?', f'({n(F["rows"])}, {F["cols"]}): records first, then variables.'),
                ('Why is order_date shown as object?', 'It is stored as text. We convert it to a real date in Session 8.'),
                ('What does the mean being twice the median tell you?', 'A few very large orders pull the mean up: the variable is right-skewed. The median is the typical order.'),
                ('What does isna().sum() return?', 'The count of missing values in each column.'),
                ('How do you filter on two conditions?', 'Put each test in round brackets and join them with & (and) or | (or).'),
                ('What does value_counts() do?', 'It counts each different value of a Series, largest count first.'),
                ('Why does jinja.loc[0] fail?', 'The filter kept the old labels, and label 0 belongs to a B01 row that was filtered out.')],
        lab_steps=[('Step 1: load and shape', f'orders loaded, shape ({n(F["rows"])}, {F["cols"]}). Watch for a wrong file name.'),
                   ('Step 2: missing and describe', f'{n(F["n_missing"])} missing customer_id; mean {n(F["mean"])} against median {n(F["median"])}.'),
                   ('Step 3: filter', f'jinja has {n(F["n_jinja"])} rows. A single = is the usual error.'),
                   ('Step 4: two conditions and query', f'{n(F["n_both"])} with &, {n(F["n_either"])} with |, and the same {n(F["n_query"])} with query.'),
                   ('Step 5: sort and count', f'Top order {F["top_order"]} at {n(F["top_value"])}; Mobile money {n(pay["Mobile money"])}.'),
                   ('Step 6: loc and iloc', f'First Jinja label {F["jinja_first_label"]}. loc[0] fails on jinja.'),
                   ('Step 7: profile', 'Seven rows, with customer_id the only variable that has missing values. Saved as orders_profile.csv.')],
        rescue=['If concepts run over, shorten the info slide and the query slide; the lab covers both.',
                'If only 30 minutes of lab remain, do steps 1, 2, 3, 4 and 7, and set steps 5 and 6 as homework.',
                'If a learner cannot upload data.zip, share the five CSV files individually through the Colab file panel.',
                'If a learner has no laptop, pair them with a neighbour: one types, one predicts aloud.'],
        after=['Share the notebook and this deck again for learners who were absent.', 'Ask each learner to save orders_profile.csv and bring a CSV from their own work to Session 8 if it is not confidential.', 'Note any question you could not answer and open the next session with it.'],
        lab_answer_key=[['Step 1 PREDICT: how many rows and columns?', f'{n(F["rows"])} rows and {F["cols"]} columns.'],
                        ['Step 2 PREDICT: will the mean order value be bigger or smaller than the median?', f'Bigger: {n(F["mean"])} against {n(F["median"])}, because a few very large orders pull the mean up.'],
                        ['Step 3 READ: why does the mask have {} values?'.format(n(F['rows'])), 'One True or False for every row of orders.'],
                        ['Step 4 PREDICT: will the count for | be bigger or smaller than for &?', f'Bigger: {n(F["n_either"])} against {n(F["n_both"])}. Or keeps more rows than and.'],
                        ['Step 5 CHANGE: sort ascending instead.', 'The smallest orders come first. The smallest is UGX 800.'],
                        ['Step 6 PREDICT: what does jinja.iloc[0] give?', f'The first Jinja row, order {F["jinja_first_order"]}, label {F["jinja_first_label"]}.'],
                        ['Step 7 READ: which variable has missing values?', f'Only customer_id: {n(F["n_missing"])}, {F["missing_pct"]:.1f} percent.']])
    return sess
