"""Session 2: Data as tables (records, variables, keys, missing values, messy data, the data dictionary). Sheets lab, no notebook.

Every number on a slide, in a note or in `sheet_tasks` is computed in facts() with pandas from the real Lakeside Mart workbook (lakeside_for_sheets.xlsx)
and from the raw files in the same data folder. Nothing is typed from memory. Figure data (real excerpts) also comes from facts().
"""
import datetime as dt
from functools import lru_cache
from pathlib import Path

import pandas as pd

BUILD = Path(__file__).resolve().parents[1]
DATA = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'data'
TABS = ['orders', 'order_lines', 'products', 'branches', 'customers', 'branch_weeks']


def n(x):
    """Integer with thousands separators: 2,000."""
    return f'{int(x):,}'


@lru_cache(maxsize=None)
def facts():
    xl = pd.ExcelFile(DATA / 'lakeside_for_sheets.xlsx')
    T = {t: xl.parse(t) for t in TABS}
    o, l, p, b, c, w = (T[t] for t in TABS)
    F = dict(T=T)
    F['rows'] = {t: len(T[t]) for t in TABS}
    F['vars'] = {t: T[t].shape[1] for t in TABS}
    # primary keys
    F['pk_ok'] = dict(orders=bool(o.order_id.is_unique), order_lines=bool(l.line_id.is_unique), products=bool(p.product_id.is_unique),
                      branches=bool(b.branch_id.is_unique), customers=bool(c.customer_id.is_unique))
    F['bw_dup_pairs'] = int(w.duplicated(['branch_id', 'week_start']).sum())
    F['bw_branches'] = int(w.branch_id.nunique())
    F['bw_weeks'] = int(w.week_start.nunique())
    F['bw_pairs'] = F['bw_branches'] * F['bw_weeks']
    F['bw_first'], F['bw_last'] = str(w.week_start.min()), str(w.week_start.max())
    # orphans (foreign keys that find no row)
    F['orphans'] = dict(order_branch=int((~o.branch_id.isin(b.branch_id)).sum()), order_customer=int((~o.customer_id.dropna().isin(c.customer_id)).sum()),
                        line_order=int((~l.order_id.isin(o.order_id)).sum()), line_product=int((~l.product_id.isin(p.product_id)).sum()),
                        customer_home=int((~c.home_branch_id.isin(b.branch_id)).sum()))
    F['all_orders_have_lines'] = bool(o.order_id.isin(l.order_id).all())
    F['lines_sum_to_orders'] = bool((l.groupby('order_id').line_revenue_ugx.sum() == o.set_index('order_id').order_value_ugx).all())
    # missing customer_id
    F['blank'] = int(o.customer_id.isna().sum())
    F['filled'] = int(o.customer_id.notna().sum())
    F['blank_pct'] = F['blank'] / len(o) * 100
    F['distinct_cust'] = int(o.customer_id.nunique())
    vc = o.customer_id.value_counts()
    F['cust_repeat'] = {int(k): int(v) for k, v in vc.value_counts().sort_index().items()}
    F['cust_max_orders'] = int(vc.max())
    F['cust_nonorder'] = len(c) - F['distinct_cust']
    # lines per order
    g = l.groupby('order_id').size()
    F['lines_per_order'] = float(g.mean())
    F['max_basket'] = int(g.max())
    F['max_basket_id'] = str(g.idxmax())
    F['single_line_orders'] = int((g == 1).sum())
    F['distinct_orders_in_lines'] = int(l.order_id.nunique())
    # one order
    F['o3_order'] = o[o.order_id == 'O000003'].iloc[0]
    F['o3_lines'] = l[l.order_id == 'O000003'].reset_index(drop=True)
    F['o3_products'] = p.set_index('product_id').loc[list(F['o3_lines'].product_id)]
    F['o3_branch'] = b.set_index('branch_id').loc[F['o3_order'].branch_id]
    F['o3_sum'] = int(F['o3_lines'].line_revenue_ugx.sum())
    F['b01_orders'] = int((o.branch_id == 'B01').sum())
    # types and dates
    F['dates_are_text'] = bool(o.order_date.map(lambda v: isinstance(v, str)).all())
    F['datevalue_b2'] = (dt.date.fromisoformat(o.order_date.iloc[0]) - dt.date(1899, 12, 30)).days
    # categorical counts
    pm = o.payment_method.value_counts()
    F['pay'] = {k: int(v) for k, v in pm.items()}
    F['pay_pct'] = {k: float(v) / len(o) * 100 for k, v in pm.items()}
    F['pay_n'] = int(o.payment_method.nunique())
    F['promo_weeks'] = int(o.promo_week.sum())
    F['tiers'] = {k: int(v) for k, v in c.loyalty_tier.value_counts().items()}
    # extreme values
    F['max_order'] = int(o.order_value_ugx.max())
    mx = o.loc[o.order_value_ugx.idxmax()]
    F['max_order_id'], F['max_order_branch'], F['max_order_pay'] = str(mx.order_id), str(mx.branch_id), str(mx.payment_method)
    F['max_order_branch_name'] = str(b.set_index('branch_id').loc[mx.branch_id, 'branch_name'])
    F['max_order_blank_cust'] = bool(pd.isna(mx.customer_id))
    F['median_order'] = float(o.order_value_ugx.median())
    F['max_over_median'] = F['max_order'] / F['median_order']
    F['second_order'] = int(o.order_value_ugx.nlargest(2).iloc[1])
    F['first_order_id'] = str(o.order_id.iloc[0])
    # other files: missing values elsewhere
    loans = pd.read_csv(DATA / 'loans.csv')
    F['loans_rows'], F['loans_no_income'] = len(loans), int(loans.monthly_income_ugx.isna().sum())
    cl = pd.read_csv(DATA / 'clinic_visits.csv')
    F['clinic_rows'], F['clinic_blank'] = len(cl), int(cl.total_visits.isna().sum())
    fb = pd.read_csv(DATA / 'feedback.csv')
    F['feedback_example'] = str(fb.message.iloc[0])
    # raw export
    raw = pd.read_csv(DATA / 'orders_raw.csv', dtype=str, keep_default_na=False)
    canon = set(b.branch_name)
    pay_ok = {'Mobile money', 'Cash', 'Card'}
    F['raw_rows'] = len(raw)
    F['raw_pay_spellings'] = int(raw.payment.nunique())
    F['raw_branch_spellings'] = int(raw.branch.nunique())
    F['raw_dupes'] = int(raw.duplicated().sum())
    F['raw_qty_blank'] = int((raw.qty == '').sum())
    F['raw_slash_dates'] = int(raw.order_date.str.contains('/').sum())
    F['raw_slash_pct'] = F['raw_slash_dates'] / len(raw) * 100
    F['raw_price_text'] = int((~raw.unit_price.str.fullmatch(r'\d+')).sum())
    F['raw_price_text_pct'] = F['raw_price_text'] / len(raw) * 100
    F['mm_spellings'] = sorted({v for v in raw.payment.unique() if v.strip().lower() in ('mobile money', 'mm')})
    F['cash_spellings'] = sorted({v for v in raw.payment.unique() if v.strip().lower() == 'cash'})
    F['card_spellings'] = sorted({v for v in raw.payment.unique() if v.strip().lower() == 'card'})

    def flags(r):
        f = set()
        if '/' in r.order_date:
            f.add('date')
        if r.branch not in canon:
            f.add('branch')
        if r.payment not in pay_ok:
            f.add('payment')
        if r.qty == '':
            f.add('qty')
        if not r.unit_price.isdigit():
            f.add('price')
        return f
    fl = raw.apply(flags, axis=1)
    picks = [raw[fl.map(len) == 0].iloc[0],
             raw[(fl.map(lambda s: s == {'date'}))].iloc[0],
             raw[(fl.map(lambda s: s == {'branch'})) & (raw.branch == 'Kampala Cntral')].iloc[0],
             raw[(fl.map(lambda s: s == {'payment'})) & (raw.payment == 'MM')].iloc[0],
             raw[(fl.map(lambda s: s == {'qty'}))].iloc[0],
             raw[(fl.map(lambda s: s == {'price'}))].iloc[0]]
    F['raw_pick'] = pd.DataFrame(picks)[['order_date', 'branch', 'payment', 'qty', 'unit_price']].reset_index(drop=True)
    F['raw_pick_flags'] = [None, ('order_date', 'date'), ('branch', 'branch'), ('payment', 'payment'), ('qty', 'qty'), ('unit_price', 'price')]
    # excerpts for figures
    F['ex_orders'] = o.head(4)
    F['ex_fk_orders'] = pd.concat([o[o.branch_id == k].head(1) for k in ('B01', 'B02', 'B04')])
    F['ex_bw'] = pd.concat([w[w.branch_id == 'B01'].head(3), w[w.branch_id == 'B02'].head(3)])
    F['ex_branches'] = b.head(4)
    F['ex_cust_id_cells'] = list(o.order_id.head(3))
    F['ex_cust_repeat'] = list(o.customer_id.dropna().head(3))
    F['ex_cust_repeat_one'] = str(vc.index[vc == vc.max()].sort_values()[0])
    F['bw_row1'] = w.iloc[0]
    F['ex_lines'] = F['o3_lines']
    return F


def s(x):
    return '' if pd.isna(x) else str(x)


def erd_spec(F):
    """The six tabs for the entity relationship diagram: which variables to show, the key tags, and the links. Checked against the data."""
    T = F['T']
    tags = {('customers', 'customer_id'): 'PK', ('customers', 'home_branch_id'): 'FK', ('orders', 'order_id'): 'PK', ('orders', 'branch_id'): 'FK', ('orders', 'customer_id'): 'FK',
            ('branches', 'branch_id'): 'PK', ('products', 'product_id'): 'PK', ('order_lines', 'line_id'): 'PK', ('order_lines', 'order_id'): 'FK', ('order_lines', 'product_id'): 'FK',
            ('branch_weeks', 'branch_id'): 'PK FK', ('branch_weeks', 'week_start'): 'PK'}
    shown = {'customers': (0, 0, ['customer_id', 'home_branch_id', 'signup_date', 'age_band', 'loyalty_tier']), 'orders': (1, 0, ['order_id', 'order_date', 'branch_id', 'customer_id']),
             'branches': (2, 0, ['branch_id', 'branch_name', 'region', 'size', 'opened_year']), 'products': (0, 1, ['product_id', 'product_name', 'category', 'unit_cost_ugx', 'unit_price_ugx']),
             'order_lines': (1, 1, ['line_id', 'order_id', 'product_id', 'quantity']), 'branch_weeks': (2, 1, ['branch_id', 'week_start', 'footfall', 'orders'])}
    tables = []
    for name, (col, row, cols) in shown.items():
        assert set(cols) <= set(T[name].columns)
        rows = [(c, tags.get((name, c), '')) for c in cols]
        more = T[name].shape[1] - len(cols)
        if more:
            rows.append((f'+ {more} more variables', 'more'))
        assert len(rows) == 5, name
        tables.append(dict(name=name, col=col, row=row, rows=rows))
    for k, v in F['pk_ok'].items():
        assert v, k
    assert F['bw_dup_pairs'] == 0 and all(x == 0 for x in F['orphans'].values())
    links = [dict(many='orders', many_var='customer_id', one='customers', one_var='customer_id'), dict(many='orders', many_var='branch_id', one='branches', one_var='branch_id'),
             dict(many='order_lines', many_var='order_id', one='orders', one_var='order_id'), dict(many='order_lines', many_var='product_id', one='products', one_var='product_id'),
             dict(many='branch_weeks', many_var='branch_id', one='branches', one_var='branch_id'), dict(many='customers', many_var='home_branch_id', one='branches', one_var='branch_id', route='over')]
    return tables, links


def build():
    F = facts()
    R, V = F['rows'], F['vars']
    # literals used in prose and formulas must match the data
    assert F['ex_branches'].iloc[0].branch_id == 'B01' and F['o3_order'].branch_id == 'B01' and F['o3_lines'].product_id.tolist() == ['P117', 'P043']
    assert F['ex_orders'].iloc[2].customer_id == F['ex_cust_repeat'][0] and F['ex_orders'].iloc[0].order_id == 'O000003' and set(F['pay']) == {'Cash', 'Mobile money', 'Card'}
    assert F['rows']['orders'] == 2000 and F['rows']['order_lines'] == 6590 and F['rows']['branch_weeks'] == 832 and F['rows']['branches'] == 8 and F['rows']['products'] == 150 and F['rows']['customers'] == 2500
    o54 = F['T']['orders'].set_index('order_id').loc['O000054']
    assert o54.customer_id == 'C0229' and o54.order_value_ugx == 52200 and o54.payment_method == 'Cash' and o54.order_date == '2024-01-02' and o54.branch_id == 'B01' and o54.promo_week == 0
    o3, o3l, o3p, o3b = F['o3_order'], F['o3_lines'], F['o3_products'], F['o3_branch']
    p1, p2 = o3l.iloc[0], o3l.iloc[1]
    pn1, pn2 = o3p.iloc[0], o3p.iloc[1]
    blank, filled, distinct = F['blank'], F['filled'], F['distinct_cust']
    lpo = F['lines_per_order']
    ratio = F['max_over_median']
    pay = F['pay']
    sess = dict(
        num=2, block='Module A: Think with data', short_title='Data as tables',
        title='Data as tables: records, variables and keys',
        question='What exactly is one row of a table, and how does one table connect to another?',
        outcomes=['Say what one record stands for in a table (its granularity), and choose the right variable type for each variable',
                  'Find a primary key, a composite key and a foreign key, and read an entity relationship diagram',
                  'Test a table in Google Sheets for missing values and messy data, and write a data dictionary'],
        outcome_icons=['notebook', 'key', 'magnifier'],
        outcome_note=('Here is what you can do by the end of today. You can say what one record of a table stands for, which is its granularity, and you can pick the right variable type for every variable. '
                      'You can find a primary key, a composite key and a foreign key, and read a diagram that shows how tables link. '
                      'And you can test a table in Google Sheets for missing values and messy data, and then write a data dictionary. You will do all of it on the Lakeside Mart workbook, with no code.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: picture, plain words, one example by hand'), (10, 'Break'), (45, 'Lab: predict, check, write the dictionary'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: concepts first, then a Google Sheets lab',
        plan_caption='Ideas with pictures first. Then you open the sheet. Then the checks and what you keep.',
        plan_note=('We have two hours. The first ten minutes bring back Session 1 and set the question for today. Then forty-five minutes of concepts, with no laptops open, so you can watch the pictures. '
                   'After a ten minute break we open the Lakeside Mart workbook in Google Sheets for a forty-five minute lab. You will predict each answer, check it with a formula, and write what you find on a new tab. '
                   'The last ten minutes are an exit check and what you keep. The lab is where the learning sticks, so please protect that time.'),
        recall_from='Session 1',
        recall=[('In CRISP-DM, which phase comes straight after business understanding, and what do you do in it?', 'Data understanding: find the tables that could answer the question and check what they mean.'),
                ('In Excel words, what is a dataset, and how does a model differ from a formula?', 'A dataset is a workbook in which each tab is one table. A model is a rule found from data, where a formula is typed by a person.'),
                ('An assistant gives you the share of orders paid by Mobile money. What do you do before you report it?', f'Recompute it from your own data: {F["pay"]["Mobile money"] / F["rows"]["orders"] * 100:.1f} percent, {n(F["pay"]["Mobile money"])} of {n(F["rows"]["orders"])}. Write the source beside it.')],
        words=[('Record (observation, instance, row)', 'One row of a table: one thing the table describes. In the orders tab each record is one till order.'),
               ('Granularity (grain)', 'The level of detail of a table: one record per order, per order line or per branch per week.'),
               ('Variable type and data type', 'Variable type: how a variable is measured (numeric, categorical, datetime, text). Data type: how the cell stores it (integer, float, string). They are different ideas.'),
               ('Primary key and foreign key', 'A primary key never repeats and names one record. A foreign key holds the primary key of another table and links the two.'),
               ('Missing value (NaN, NULL)', 'A cell with no value. Ask whether it means unknown, not applicable or something real. Informative missingness: the blank itself is a fact, such as a walk-in shopper.')],
        word_icons=['notebook', 'grid', 'tag', 'key', 'question'],
        words_note=('Five words for today. A record is one row of a table, and you will also hear it called an observation or an instance. Granularity is the level of detail of a table. '
                    'A variable type tells you how a value is measured, and a data type tells you how the cell stores it. They are different ideas. A primary key never repeats, and a foreign key holds the primary key of another table. '
                    'And a missing value is a cell with no value. When the blank itself tells you something, that is informative missingness. We use every one of them before the end of the session.'),
        keep='Keep your dictionary tab: for each of the six Lakeside tabs, one sentence saying what a record is, its key, and the problems you found, each with a number.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab file', value='A dictionary tab'), dict(label='The key test', value='Two counts match'), dict(label='Next session', value='Summarising data')]),
        keep_title='Save your workbook with its dictionary tab',
        next='Session 3: Summarising and showing data fairly. We describe thousands of records with a few numbers and one chart.', next_label='Next session',
        keep_note=('Before you go, save your workbook with the dictionary tab. That tab is your keepsake from today: one sentence per table saying what a record is, the key of each table, and three problems with a number each. '
                   'If you can show it to a colleague and they understand the workbook without asking you anything, it is good. Next session we use these tables to summarise thousands of records in a few numbers and one honest chart. '
                   'If anything was unclear today, write the question down and bring it.'),
        cover_note=('Welcome back. Last session we drew the map of the whole course. Today we look closely at the thing every later session depends on, the table. '
                    'You will open the Lakeside Mart workbook and learn to read a table the way a data scientist does: what one row stands for, how a column is measured, and how one table links to another. '
                    'These ideas decide whether a total you report is right or wrong, so we take our time.'),
        use_at_work='Check keys, granularity and missing values before you count, join or report.',
        slides=[])
    S = sess['slides']
    erd_tables, erd_links = erd_spec(F)

    # ------------------------------------------------------------------ 1 answers to the recall questions
    S.append(dict(kind='table', title='Answers to the three questions from Session 1', headers=['Question', 'Short answer'],
                  rows=[[q, a] for q, a in sess['recall']], widths=[5.2, 6.8], icons=['pin', 'folder', 'shield'],
                  notes=('Here are the answers to the three warm-up questions. After business understanding, the next CRISP-DM phase is data understanding. You cannot answer a question until you know which tables could answer it and what they mean, and that is exactly where we are today. '
                         'A dataset, in Excel words, is a workbook where each tab is one table, and a model is a rule found from data where a formula is typed by a person. And an assistant predicts likely words, so it can state a share that nobody calculated. Recompute it from your own data and write the source beside it. '
                         'Which of the three did you find hardest?')))

    # ------------------------------------------------------------------ 2 anatomy
    S.append(dict(kind='idea', title='A table holds records in rows and variables in columns',
                  visual=dict(kind='ds_anatomy', headers=['order_id', 'order_date', 'customer_id', 'order_value_ugx'],
                              rows=[[s(r.order_id), s(r.order_date), s(r.customer_id), s(r.order_value_ugx)] for r in F['ex_orders'].itertuples()], cell=[3, 2]),
                  lead='A record is one row. A variable is one column.',
                  points=['Record (observation, instance): one row. Here, one till order.', 'Variable (feature, field): one column.', 'Cell: one value of one variable in one record.'],
                  notes=('Here are the first four rows of the orders tab of the Lakeside Mart workbook. The whole grid is one table. Each column is a variable, which is one fact recorded for every order, such as the order date. '
                         'Each row is a record. Data scientists also call it an observation or an instance, and in machine learning you will hear instance. In this table each record is one till order. '
                         'And a cell is a single value, one variable for one record. Look at the gold cell: it holds the customer id of the fourth order. Notice two empty cells in the customer column. We come back to them. '
                         'Can you point to one record on the slide?')))

    # ------------------------------------------------------------------ 3 vocabulary
    S.append(dict(kind='table', title='The spreadsheet word and the data science word for each part',
                  headers=['In a spreadsheet', 'In data science', 'Plain meaning'],
                  rows=[['Row', 'Record (observation, instance)', 'One thing the table describes, such as one till order.'], ['Column', 'Variable (feature, field, attribute)', 'The same fact about every record, such as branch_id.'],
                        ['Cell', 'Value', 'One variable for one record.'], ['Tab', 'Table (a DataFrame in pandas)', 'All the records of one kind.'], ['Workbook', 'Dataset or database', 'Tables that belong together.']],
                  widths=[2.3, 4.2, 5.4], icons=['grid', 'tag', 'pin', 'doc', 'folder'], note='In machine learning a variable is either a feature (an input) or the target (the answer you predict).',
                  notes=('You already know every part of a table from Excel, so here is the translation. A row is a record, also called an observation or an instance. A column is a variable, also called a feature, a field or an attribute. '
                         'A cell holds a value. A tab is a table, and in pandas, the Python library we meet in Session 7, a table is called a DataFrame. A whole workbook is a dataset, or a database when it is stored in a system. '
                         'The words differ between statistics, databases and machine learning, but the idea is the same. When you read documentation or a job advert, this table is your dictionary. Which of these words was new to you?')))

    # ------------------------------------------------------------------ 4 granularity
    S.append(dict(kind='idea', title='Granularity is the level of detail: one record per order, per order line or per branch per week',
                  visual=dict(kind='ds_granularity', levels=[
                      dict(title='orders: each record is one till order', headers=['order_id', 'order_date', 'order_value_ugx'], rows=[[s(o3.order_id), s(o3.order_date), s(o3.order_value_ugx)]]),
                      dict(title='order_lines: each record is one product on one order', headers=['line_id', 'order_id', 'product_id', 'line_revenue_ugx'],
                           rows=[[s(r.line_id), s(r.order_id), s(r.product_id), s(r.line_revenue_ugx)] for r in o3l.itertuples()]),
                      dict(title='branch_weeks: each record is one branch in one week', headers=['branch_id', 'week_start', 'orders', 'sales_ugx'],
                           rows=[[s(F['bw_row1'].branch_id), s(F['bw_row1'].week_start), s(F['bw_row1'].orders), s(F['bw_row1'].sales_ugx)]])]),
                  lead='Granularity is the level of detail of a table. It says what one record stands for.',
                  points=['The unit of observation is what one record stands for.', 'Data warehouse teams call the level of detail the grain.', 'Finish this sentence first: each record is one ...'],
                  notes=('Now the question in the title of today: what exactly is one row? The standard name is granularity, the level of detail of a table. What one record stands for is called the unit of observation. '
                         'People who build data warehouses call this the grain, so if a colleague says grain, they mean the same thing. Look at the picture. The same order, O000003, appears at three levels. '
                         'In orders it is one record. In order_lines it is two records, one for each product. And branch_weeks has one record for a whole branch and a whole week. '
                         'Before you count or total anything, finish the sentence: each record is one what?')))

    # ------------------------------------------------------------------ 5 six tabs
    S.append(dict(kind='table', title='Each of the six tabs has its own record and its own count',
                  headers=['Tab', 'Each record is', 'Records', 'Variables'],
                  rows=[['orders', 'one till order', n(R['orders']), str(V['orders'])], ['order_lines', 'one product on one order', n(R['order_lines']), str(V['order_lines'])],
                        ['products', 'one product', n(R['products']), str(V['products'])], ['branches', 'one branch', n(R['branches']), str(V['branches'])],
                        ['customers', 'one loyalty customer', n(R['customers']), str(V['customers'])], ['branch_weeks', 'one branch in one week', n(R['branch_weeks']), str(V['branch_weeks'])]],
                  widths=[2.6, 5.6, 1.9, 1.9], icons=['receipt', 'bag', 'tag', 'shop', 'person', 'calendar'],
                  note=f'The workbook holds a {n(R["orders"])}-order sample of the full Lakeside Mart file. Records are counted without the header row.',
                  notes=(f'Here are the six data tabs of your workbook, each with its unit of observation. Orders has {n(R["orders"])} records, one per till order. Order lines has {n(R["order_lines"])}, one per product on an order. '
                         f'Products has {R["products"]}, branches has {R["branches"]}, customers has {n(R["customers"])} loyalty customers, and branch weeks has {R["branch_weeks"]}, one for each branch in each week. '
                         'There is also a seventh tab called READ ME, which is only a note. The workbook holds a sample of two thousand orders from the full file, so totals here will differ from the full file. Session 4 explains why. '
                         'In the lab you will write this table yourself on a new tab.')))

    # ------------------------------------------------------------------ 6 count the wrong tab
    S.append(dict(kind='compare', title=f'Counting records in the wrong tab: {n(R["order_lines"])} lines are not {n(R["order_lines"])} orders',
                  left=dict(head='Wrong', points=[f'order_lines has {n(R["order_lines"])} records.', 'Reporting that as the number of orders counts every product on every order.']),
                  right=dict(head='Right', points=[f'Count the orders tab: {n(R["orders"])} orders.', f'Or count each order_id once in order_lines: {n(F["distinct_orders_in_lines"])}.', f'That is {lpo:.1f} lines per order on average.']),
                  verdict='State the granularity first. Then count.',
                  notes=(f'This is the most common mistake with tables. You open the order lines tab, you see {n(R["order_lines"])} rows, and you tell your manager the shop sold {n(R["order_lines"])} orders. Nothing warns you. '
                         f'But a record in order lines is one product on one order, and a basket of five products adds five records. The orders tab has {n(R["orders"])} orders, and the lines average {lpo:.1f} per order, which is {n(R["order_lines"])} divided by {n(R["orders"])}. '
                         'To count each order once in the order lines, use COUNTA of UNIQUE of the order id range. So say the granularity first, then count. Which tab would you count to get the number of customers who bought something?')))

    # ------------------------------------------------------------------ 7 variable types and data types
    S.append(dict(kind='wide', title='Every variable has a variable type (how it is measured) and a data type (how it is stored)',
                  visual=dict(kind='ds_types'),
                  caption='Discrete: counted. Continuous: measured. An identifier (order_id) is a label: never add it up.',
                  notes=('Every variable has two kinds of type, and people mix them up. The variable type is how the value is measured. Numeric values are numbers you can add. They are discrete when you count them, like quantity, and continuous when you measure them, like money. '
                         'Categorical values are labels. They are nominal when there is no order, like payment method, and ordinal when there is an order, like Basic, Silver and Gold. Datetime values are dates and times, and text is free words. '
                         'The data type is how the cell stores it: integer, float, string or datetime. A date can be stored as a string, and we will see that happen in this workbook. An identifier such as order_id or customer_id names a record, so you never add it up. Which type is branch_id?')))

    # ------------------------------------------------------------------ 8 the seven variables
    S.append(dict(kind='table', title='The seven variables of the orders tab and their types',
                  headers=['Variable', 'Example (order O000054)', 'Data type in this workbook', 'Variable type'],
                  rows=[['order_id', 'O000054', 'string', 'identifier (a label)'], ['order_date', s(o54.order_date), 'string: not a real date', 'datetime'],
                        ['branch_id', s(o54.branch_id), 'string', 'categorical (nominal)'], ['customer_id', s(o54.customer_id), f'string, {blank} blank', 'identifier, with missing values'],
                        ['payment_method', s(o54.payment_method), 'string', 'categorical (nominal)'], ['promo_week', str(int(o54.promo_week)), 'integer', 'categorical (a 0 or 1 flag)'],
                        ['order_value_ugx', s(o54.order_value_ugx), 'integer', 'numeric (continuous, UGX)']],
                  widths=[2.8, 2.0, 3.4, 3.8], icons=['key', 'calendar', 'shop', 'person', 'coin', 'flag', 'calculator'], note='An identifier can look like a number or a code. You never add it up.',
                  notes=(f'Now we apply both kinds of type to the seven variables of the orders tab. Order_id and customer_id are identifiers, labels that name something, and you never average a label. '
                         f'Order_date should be a datetime, but in this workbook it is stored as a string, which is text. We test that in the lab with a function called ISNUMBER. Branch_id and payment_method are categorical with no order. '
                         f'Promo_week is stored as an integer, but it only holds zero or one, so it is a categorical flag. And order_value_ugx is numeric, a continuous amount in shillings. '
                         'Why does the type matter? Because it decides which questions make sense. Would an average of branch_id mean anything?')))

    # ------------------------------------------------------------------ 9 primary key
    S.append(dict(kind='idea', title='A primary key is a variable that is different in every record',
                  visual=dict(kind='ds_key_test', good=dict(var='order_id', tab='orders', cells=F['ex_cust_id_cells'], filled=R['orders'], different=R['orders'], f1='=COUNTA(A2:A2001)', f2='=COUNTA(UNIQUE(A2:A2001))'),
                              bad=dict(var='customer_id', tab='orders', cells=[F['ex_cust_repeat_one']] * 3, filled=filled, different=distinct, f1='=COUNTA(D2:D2001)', f2='=COUNTUNIQUE(D2:D2001)')),
                  lead='Primary key: a variable whose value is different in every record, so it names exactly one record.',
                  points=['Test it: count the filled cells, then count the different values.', 'If the two counts match, it can be a primary key.', f'order_id passes. customer_id repeats, so it fails.'],
                  notes=(f'A primary key is a variable whose value never repeats, so it names exactly one record, like an invoice number in Excel. You can test a candidate in two steps. First count the filled cells with COUNTA. Then count the different values with COUNTA of UNIQUE, a Google Sheets formula. '
                         f'For order_id both counts are {n(R["orders"])}, so order_id is the primary key of the orders tab. For customer_id the first count is {n(filled)} and the second is only {n(distinct)}. Some customers ordered more than once, so the value repeats. '
                         'Customer_id is not a key of the orders tab. With blanks in a range, use COUNTUNIQUE in Sheets. Which variable would you test as the key of the order lines tab?')))

    # ------------------------------------------------------------------ 10 composite key
    S.append(dict(kind='idea', title='Two variables together can form a composite key',
                  visual=dict(kind='ds_composite', headers=['branch_id', 'week_start', 'orders', 'sales_ugx'], rows=[[s(r.branch_id), s(r.week_start), s(r.orders), s(r.sales_ugx)] for r in F['ex_bw'].itertuples()],
                              total=f'{F["bw_branches"]} branches × {F["bw_weeks"]} weeks = {F["bw_pairs"]} records'),
                  lead='Composite key: two or more variables that are unique together, although each repeats alone.',
                  points=['branch_id repeats: every branch appears once per week.', 'week_start repeats: every week appears once per branch.', f'Each pair appears once, so the pair is the key: {F["bw_pairs"]} records.'],
                  notes=(f'Sometimes no single variable is unique. Look at the branch weeks tab. Branch_id repeats, because every branch appears in every week. Week_start repeats too, because every week appears for every branch. '
                         f'But the pair, branch and week together, never repeats. That is a composite key. There are {F["bw_branches"]} branches and {F["bw_weeks"]} weeks, and {F["bw_branches"]} times {F["bw_weeks"]} is {F["bw_pairs"]}, which is exactly the number of records in the tab. '
                         'The product matches the record count, which fits with every pair appearing once but does not prove it. The proof is to count the distinct pairs and get the same number again, which you do in the lab. Where else might you meet a pair like this at work?')))

    # ------------------------------------------------------------------ 11 foreign key
    S.append(dict(kind='idea', title='A foreign key holds the primary key of another table and links the two',
                  visual=dict(kind='ds_fk', orders=[[s(r.order_id), s(r.branch_id)] for r in F['ex_fk_orders'].itertuples()], branches=[[s(r.branch_id), s(r.branch_name)] for r in F['ex_branches'].itertuples()],
                              lookup=f'=VLOOKUP("B01", branches!A2:B9, 2, FALSE)', result=s(F['ex_branches'].iloc[0].branch_name)),
                  lead='Foreign key: a variable whose values are primary keys of another table.',
                  points=['branch_id in orders is a foreign key. branch_id in branches is the primary key.', 'Look up B01 in branches to find the branch name.', 'In SQL and pandas this lookup is called a join or a merge.'],
                  notes=('A foreign key is a variable in one table that holds the primary key of another table. Look at the picture. The orders tab on the left has a branch_id on every order. That branch_id is a foreign key. '
                         'The branches tab on the right has one record per branch, and there branch_id is the primary key. Each arrow goes from an order to the one branch record it belongs to. '
                         'You already do this lookup in Excel with VLOOKUP or XLOOKUP, where B01 returns Kampala Central. In SQL and in pandas the same step is called a join or a merge, and we meet it in later sessions. '
                         'Which other variable in orders is a foreign key?')))

    # ------------------------------------------------------------------ 12 one-to-many
    S.append(dict(kind='idea', title='Tables relate one-to-many: one branch has many orders and one order has many lines',
                  visual=dict(kind='ds_onemany', top=dict(one='branches: B01', many=[s(r.order_id) for r in F['ex_orders'].head(3).itertuples()], more=f'{F["b01_orders"]} orders at B01 in all', one_label='one branch', many_label='many orders'),
                              bottom=dict(one=f'orders: {s(o3.order_id)}', many=[s(r.line_id) for r in o3l.itertuples()], more=f'largest basket: {F["max_basket"]} lines', one_label='one order', many_label='many lines')),
                  lead='A relationship says how records of two tables match. The common kind is one-to-many.',
                  points=[f'One branch has many orders: B01 has {F["b01_orders"]}.', f'One order has many lines: {s(o3.order_id)} has {len(o3l)}.', 'Many-to-many: orders and products, joined by the junction table order_lines.'],
                  notes=(f'A relationship says how the records of two tables match. The most common kind is one-to-many. One branch has many orders: in this sample branch B01 has {F["b01_orders"]}. One order has many lines: order {s(o3.order_id)} has {len(o3l)}, and the largest basket in the sample has {F["max_basket"]}. '
                         'Read from the other side it is many-to-one: many orders belong to one branch. The lines on the picture end in three prongs on the many side. There is a third kind, many-to-many. Products and orders are like that, because a product appears on many orders and an order has many products. '
                         'The order lines tab sits in between as a junction table, also called a bridge table, and turns it into two one-to-many links. Is customers to orders one-to-many?')))

    # ------------------------------------------------------------------ 13 ERD
    S.append(dict(kind='wide', title='An entity relationship diagram (ERD) draws the six tabs and how their keys link',
                  visual=dict(kind='ds_erd', tables=erd_tables, links=erd_links),
                  caption='PK marks a primary key and FK a foreign key. A line ends in three prongs on its many side.',
                  notes=('This picture is an entity relationship diagram, or ERD. It is the standard way to draw how tables link. Each box is a table, with its primary key marked PK and its foreign keys marked FK. '
                         'Each line is a one-to-many relationship, and the three prongs sit on the many side. Orders points to customers and to branches. Order lines points to orders and to products. '
                         'Branch weeks points to branches, and its branch id is part of a composite key. Customers also holds a home branch id that points to branches, which is the line that goes over the top. '
                         'Each box shows only some of its variables. Which table would you start from to find the branch of a product sold?')))

    # ------------------------------------------------------------------ 14 trace one order
    S.append(dict(kind='wide', title=f'Follow order {s(o3.order_id)} through four tabs by their keys',
                  visual=dict(kind='ds_trace', order=[['order_id', s(o3.order_id)], ['branch_id', s(o3.branch_id)], ['customer_id', '(blank)'], ['order_value_ugx', s(o3.order_value_ugx)]],
                              lines=[[s(r.line_id), s(r.product_id), s(r.quantity), s(r.line_revenue_ugx)] for r in o3l.itertuples()],
                              products=[[s(k), s(v.product_name), s(v.unit_price_ugx)] for k, v in o3p.iterrows()], branch=[['branch_id', s(o3.branch_id)], ['branch_name', s(o3b.branch_name)], ['region', s(o3b.region)]]),
                  caption='customer_id is blank, so this order has no row in customers: it was a walk-in.',
                  notes=(f'Let us follow one order through the tabs using only keys. Start in the orders tab: order {s(o3.order_id)}, at branch {s(o3.branch_id)}, with a value of {n(o3.order_value_ugx)} shillings. '
                         f'Step one, look up its order_id in the order lines tab. You find {len(o3l)} lines, for products {s(p1.product_id)} and {s(p2.product_id)}. Step two, look those product ids up in the products tab to get their names. '
                         f'Step three, look the branch id up in branches: {s(o3b.branch_name)}. The two line amounts, {n(p1.line_revenue_ugx)} and {n(p2.line_revenue_ugx)}, add up to {n(F["o3_sum"])}, the order total. '
                         'The customer id is blank, so there is no customer to look up. Why do you think that is?')))

    # ------------------------------------------------------------------ 15 missing values
    S.append(dict(kind='stat', title='A blank customer_id is a missing value, and it appears on 29 percent of orders', big=f'{F["blank_pct"]:.0f}%',
                  text=f'{n(blank)} of the {n(R["orders"])} orders have no customer_id. The data dictionary says the blank means a walk-in: a shopper with no loyalty number.',
                  waffle_label='orders in every 100 have a blank customer_id',
                  notes=(f'Now missing values. A missing value is a cell with no value. In the orders tab, {n(blank)} of the {n(R["orders"])} orders have a blank customer id, which is {F["blank_pct"]:.0f} percent, about 29 orders in every 100. '
                         'Before you delete those rows or fill them in, ask what the blank means. The data dictionary tells us: the shopper was a walk-in, with no loyalty number. So the blank is not an error. It records a real fact about the shopper. '
                         'We call that informative missingness. If you deleted these records you would throw away three out of ten orders. What would you do with them if you wanted the average spend of loyalty customers only?')))

    # ------------------------------------------------------------------ 16 meanings of a blank
    S.append(dict(kind='table', title='A blank can mean unknown, not applicable or a walk-in, and each needs different handling',
                  headers=['What the blank means', 'Example', 'What to do'],
                  rows=[['Unknown: the value exists but was not recorded', f'loans.csv: {n(F["loans_no_income"])} of {n(F["loans_rows"])} loans have no monthly_income_ugx', 'Impute (fill in) with the median, and add a missing-indicator flag'],
                        ['Not applicable: no value can exist', 'Illustrative: a refund reason on an order that was never refunded', 'Leave it blank, or write none'],
                        ['Informative missingness: the blank itself is a fact', f'orders: {n(blank)} blank customer_id values mean a walk-in', 'Keep it, and add a flag such as is_walk_in']],
                  widths=[3.9, 4.4, 3.7], icons=['question', 'cross', 'person'], note='Names for a blank: NaN in pandas, NULL in SQL, an empty cell in Sheets.',
                  notes=(f'Not every blank means the same thing, and each meaning needs different handling. A blank can mean unknown: the value exists but nobody recorded it, like the {n(F["loans_no_income"])} loans out of {n(F["loans_rows"])} in the Nile Microfinance file with no monthly income. '
                         'There, a common fix is imputation, which means filling in the blank with the median, and adding a flag column so you remember which values were filled. A blank can mean not applicable, like a refund reason on an order that was never refunded. That example is made up. '
                         'Or the blank can be informative, like our walk-in customers. There you keep the blank and add a flag. Tools name it differently: NaN in pandas, NULL in SQL. Which of the three is a blank in your own data?')))

    # ------------------------------------------------------------------ 17 messy excerpt
    S.append(dict(kind='wide', title=f'A raw export is messy: three payment methods appear under {F["raw_pay_spellings"]} spellings',
                  visual=dict(kind='ds_flagged_sheet', headers=list(F['raw_pick'].columns), rows=[[s(v) for v in r] for r in F['raw_pick'].itertuples(index=False)], flags=[
                      [1, 0, 'Date written day/month/year. Most dates in the file are year-month-day.'], [2, 1, 'Branch name misspelt: Kampala Cntral.'], [3, 2, 'MM is short for Mobile money.'],
                      [4, 3, 'Quantity is missing.'], [5, 4, 'Price stored as text, with a UGX prefix and a comma.']]),
                  caption='A raw order-line export (orders_raw.csv). Gold cells are the problems. Session 8 cleans this file.',
                  notes=(f'Real exports are messy. This is a small piece of a raw order line export, the file we clean in Session 8. The gold cells are the problems. One date is written day, month, year while most are year, month, day. A branch name is misspelt. '
                         f'Mobile money appears as MM. One quantity is missing, and one price is stored as text with the letters UGX in front. Across the whole file the three payment methods appear under {F["raw_pay_spellings"]} different spellings, and the eight branches under {F["raw_branch_spellings"]}. '
                         'A pivot table would treat each spelling as a separate group and quietly give you wrong totals. Which of these would be hardest to spot in a file of forty thousand rows?')))

    # ------------------------------------------------------------------ 18 six checks
    S.append(dict(kind='table', title='Six messy-data checks you can run in Sheets before you trust a total',
                  headers=['Problem', 'What we found', 'First check in Sheets'],
                  rows=[['Blank cells', f'customer_id: {n(blank)} blank in orders', '=COUNTBLANK(D2:D2001)'], ['Dates stored as text', 'order_date in orders is text', '=ISNUMBER(B2) gives FALSE'],
                        ['Inconsistent labels', f'{F["raw_pay_spellings"]} spellings of 3 payment methods (raw export)', '=COUNTUNIQUE(range) in Sheets'],
                        ['Extreme values', f'Largest order {n(F["max_order"])} UGX, median {n(F["median_order"])}', '=MAX(G2:G2001) and =MEDIAN(G2:G2001)'],
                        ['Duplicate records', f'{F["raw_dupes"]} exact duplicate lines (raw export)', '=ROWS(range)-ROWS(UNIQUE(range)) in Sheets'], ['Numbers stored as text', 'UGX 1,700 in unit_price (raw export)', '=ISNUMBER(cell)']],
                  widths=[2.7, 4.6, 4.6], icons=['question', 'calendar', 'tag', 'chart', 'doc', 'calculator'],
                  notes=(f'Here are six checks you can run on any table before you trust a total, each with the Sheets formula and a real finding. Blank cells: COUNTBLANK found {n(blank)} in customer id. Dates stored as text: ISNUMBER on an order date returns FALSE. '
                         f'Inconsistent labels: the raw export has {F["raw_pay_spellings"]} spellings of three payment methods, which COUNTUNIQUE reveals in Sheets. In Excel 365 use COUNTA of UNIQUE of FILTER. Extreme values: the largest order is {n(F["max_order"])} shillings against a median of {n(F["median_order"])}. '
                         f'Duplicates: the raw export has {F["raw_dupes"]} exact duplicate lines. And numbers stored as text, like UGX 1,700. In the lab you will run the first, second and fourth of these. Which check would you run first on a file someone emails you?')))

    # ------------------------------------------------------------------ 19 data dictionary
    S.append(dict(kind='wide', title='A data dictionary says what each variable means, its type and its key',
                  visual=dict(kind='sheet', headers=['variable', 'variable type', 'key', 'meaning'], rows=[
                      ['order_id', 'identifier', 'primary key', 'One till order'], ['order_date', 'datetime', '', 'Date of the order'], ['branch_id', 'categorical', 'foreign key', 'Branch that sold it'],
                      ['customer_id', 'identifier', 'foreign key', 'Loyalty customer; blank for a walk-in'], ['payment_method', 'categorical', '', 'Cash, Mobile money or Card'],
                      ['promo_week', 'categorical', '', '1 if the branch ran a promotion that week'], ['order_value_ugx', 'numeric', '', 'Sum of the order lines, in UGX']], hl=[3, 3], size=15),
                  caption='The orders tab, written as a data dictionary. You write one for every tab in the lab.',
                  notes=('The last idea is the data dictionary. It is a short document that explains every variable in a table: its meaning, its variable type and its key. Look at the orders tab written as a dictionary. '
                         'The gold cell is the one that saves you from a wrong decision. It says that customer id is blank for a walk-in, so you do not delete or fill those records. Without that line, someone would call the blanks an error. '
                         'The full Lakeside dictionary comes with your workbook files. A good dictionary lets a new colleague read the table without asking you anything. In the lab you start your own dictionary tab. What would you add to it for your own data?')))

    # ------------------------------------------------------------------ 20 use at work
    S.append(dict(kind='table', title='Where you will use this at work: check keys and granularity before you report',
                  headers=['Your job', 'The tables you meet', 'What today lets you do'],
                  rows=[['Credit analyst at a bank in Kampala, using SQL', 'loans: one record per loan (loans.csv).', 'Check loan_id is unique before you join it to anything, so no loan is counted twice.'],
                        ['Health records officer at a district office, using pandas', f'Monthly clinic reports: {F["clinic_blank"]} of {F["clinic_rows"]} district-months blank in our file.', 'Tell a blank (not reported) from a zero before you total a district.'],
                        ['Sales analyst handing a workbook to Power BI', 'Orders, order lines and branches.', 'Mark each key first, so the relationships in Power BI do not multiply totals.'],
                        ['Officer at a SACCO or coffee cooperative, using Excel', 'Member register, deliveries and payments.', 'Draw the ERD and write the data dictionary, so a new colleague can read the workbook.']],
                  widths=[3.4, 4.2, 4.4], icons=['coin', 'clinic', 'chart', 'people'],
                  notes=('Where will you use this on Monday? Four examples. A credit analyst at a bank in Kampala who uses SQL should check that loan id is unique before joining the loans table to anything, so that no loan is counted twice. '
                         f'A health records officer at a district office who uses pandas has monthly reports where a blank means not reported, which is different from a zero. Our clinic file has {F["clinic_blank"]} blank months out of {F["clinic_rows"]}. '
                         'A sales analyst who hands a workbook to Power BI should mark every key first. And an officer at a SACCO or a coffee cooperative using Excel can draw the diagram and write the dictionary so that a new colleague understands the workbook. '
                         'Which of these is closest to your job?')))

    # ------------------------------------------------------------------ 21 bridge
    S.append(dict(kind='code', title='Read the recipe before the lab: five formulas test a table',
                  code='=COUNTA(A2:A2001)\n=COUNTA(UNIQUE(A2:A2001))\n=COUNTBLANK(D2:D2001)\n=COUNTIF(E2:E2001,"Mobile money")\n=ISNUMBER(B2)',
                  reads=[f'Line 1 counts the filled cells of order_id: {n(R["orders"])} records.', f'Line 2 counts the different values. Equal to line 1 means a primary key.', f'Line 3 counts the empty cells of customer_id: {n(blank)}.',
                         f'Line 4 counts the orders paid by Mobile money: {n(pay["Mobile money"])}.', 'Line 5 is TRUE for a real date or number. Here it is FALSE: the date is text.'],
                  notes=(f'Before the lab, read the five formulas that do most of the work. Line one, COUNTA of A2 to A2001, counts the filled cells in the order id column, which gives {n(R["orders"])}. '
                         f'Line two counts the different values: if it equals line one, the variable can be a primary key. Line three, COUNTBLANK on the customer column, counts the empty cells and gives {n(blank)}. '
                         f'Line four, COUNTIF, counts the records where the payment method is Mobile money, {n(pay["Mobile money"])}. Line five, ISNUMBER on B2, says whether the date is a real date, and here it says FALSE. '
                         'Tab names go in front of the range with an exclamation mark, like orders!A2:A2001, when you work from another tab. Which formula would you use to count orders paid by cash?')))

    # ------------------------------------------------------------------ 22 divider
    S.append(dict(kind='divider', title='Part 2: the Sheets lab', lead='Close the slides. Open the sheet.', section='Lab',
                  notes=('That is the end of the ideas. Everything you need is on the slides you have just seen, and the lab sheet repeats each step. '
                         'Open the Lakeside Mart workbook in Google Sheets, or in Excel if you prefer. The file is called lakeside for sheets. '
                         'Add a new tab and call it dictionary. You will write on it as you go. In every task, predict the answer first, then check it with a formula, then write what you found.')))

    # ------------------------------------------------------------------ 23 lab map
    S.append(dict(kind='steps', title='The lab has five steps, and you keep a dictionary tab at the end',
                  steps=[dict(head='1 Records', text='Count each tab', icon='notebook'), dict(head='2 Keys', text='Test with COUNTA', icon='key'), dict(head='3 Links', text='Follow one order', icon='pin'),
                         dict(head='4 Types, blanks', text='ISNUMBER, COUNTBLANK', icon='question'), dict(head='5 Messy data', text='Largest order, one question', icon='magnifier')], highlight=None,
                  caption='Ten tasks in 45 minutes. For each task, predict the answer, check it with a formula, then write it on your dictionary tab.',
                  notes=('Here is the map of the lab. Step one, count the records of each tab and write what a record is. Step two, test the keys with the two counts, including the composite key of branch weeks. '
                         'Step three, check the foreign keys and follow order O000003 through the tabs. Step four, label the variable types, count the blanks, and test whether the date is a real date. '
                         'Step five, find the largest order and write one question for the owner of the data. In every task, predict first, check with a formula, and write the answer on the dictionary tab. Please do not skip the predictions.')))

    # ------------------------------------------------------------------ 24 check numbers
    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Records in the six tabs, in the order of the table on slide 10', f'{n(R["orders"])}, {n(R["order_lines"])}, {R["products"]}, {R["branches"]}, {n(R["customers"])}, {R["branch_weeks"]}'],
                        ['Different order_id values in orders', f'{n(R["orders"])}: a primary key'], ['Lines per order on average, and in O000003', f'{lpo:.1f}, and {len(o3l)}'],
                        ['Different branch_id, week_start and pairs in branch_weeks', f'{F["bw_branches"]}, {F["bw_weeks"]} and {F["bw_pairs"]}'], ['Blank customer_id in orders, and its share', f'{n(blank)}, which is {F["blank_pct"]:.0f} percent'],
                        [f'Different customer_id values among the {n(filled)} filled', n(distinct)], ['ISNUMBER of an order_date', 'FALSE'], ['Largest order_value_ugx, and the median', f'{n(F["max_order"])} and {n(F["median_order"])}']],
                  widths=[7.4, 4.6], icons=['grid', 'key', 'bag', 'calendar', 'question', 'person', 'clock', 'coin'], note='If your number differs, find the task that went wrong. Do not change a number to match.',
                  notes=('Use this table as your own self-check. Nobody marks it. If your numbers match, carry on. If one does not, stop and call me, because later tasks use the earlier ones. '
                         'The most common cause is a range that includes the header row, which makes every count one too big, or a range that stops too early. Do not change a number to make it match. Find out why it is different. '
                         'What does it mean if your count of different customers is higher than the table says?')))

    # ------------------------------------------------------------------ 25 error cards
    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[[f'A count of {n(R["orders"] + 1)} where you expected {n(R["orders"])}', 'The range includes the header cell in row 1.', 'Start the range in row 2: A2:A2001.'],
                        ['#REF! or #NAME? when you point to another tab', 'The tab name is missing or misspelt.', 'Write the tab, then !, then the range: orders!A2:A2001.'],
                        ['#N/A from VLOOKUP', 'The key was not found, or FALSE is missing.', 'Add FALSE as the last argument. Check for stray spaces.'],
                        ['Array result was not expanded', 'Cells below the UNIQUE formula hold data.', 'Clear them, or move the formula to an empty column.'],
                        ['ISNUMBER on a date gives FALSE', 'That is correct: the date is stored as text.', 'Write it on your dictionary tab as a finding.']],
                  widths=[3.7, 4.2, 4.1], icons=['cross', 'cross', 'cross', 'cross', 'check'],
                  notes=('Five messages you may meet. A count that is one too big means your range includes the header row, so start in row 2. Hash REF or hash NAME when you point to another tab means the tab name is missing or misspelt, so write the tab, an exclamation mark and then the range. '
                         'Hash N A from VLOOKUP means the key was not found, or you forgot FALSE as the last argument. The message array result was not expanded means the cells below a UNIQUE formula already hold data, so clear them. '
                         'And ISNUMBER returning FALSE on a date is correct, because the date is stored as text. That one is a finding, so write it down. Read the message first. It usually tells you the answer.')))

    # ------------------------------------------------------------------ 26 exit check
    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[[f'Order {s(o3.order_id)} has {len(o3l)} products. How many records does it make in orders, and how many in order_lines?', f'One record in orders and {len(o3l)} in order_lines. The two tabs have different granularity.'],
                        ['Which variable is the primary key of products, and which tab holds it as a foreign key?', 'product_id. The order_lines tab holds product_id as a foreign key.'],
                        [f'customer_id is blank on {n(blank)} orders. What do you do first?', 'Read the data dictionary: the blank means a walk-in. Keep the records and add a flag, instead of deleting or filling them.']],
                  widths=[5.6, 6.4], icons=['bag', 'key', 'person'],
                  notes=('Last, the exit check. Three questions. Write your answers in your notes before you look at mine. One, an order has two products: how many records does it make in orders and how many in order lines? '
                         'Two, which variable is the primary key of products, and which tab holds it as a foreign key? Three, the customer id is blank on 580 orders: what do you do first? '
                         'The short answers are on the slide. If you got all three, you are ready for session three. If one surprised you, look at that part of your dictionary tab again tonight.')))

    # ------------------------------------------------------------------ sheet tasks
    t = F['T']
    sess['sheet_tasks'] = [
        dict(task='Create a new tab called dictionary. In columns A to D list the six data tabs, write one sentence for each saying what a record is, and count its records with =COUNTA(orders!A2:A2001) (change the tab name and last row for each tab).',
             answer=f'orders: one till order, {n(R["orders"])} records. order_lines: one product on one order, {n(R["order_lines"])}. products: one product, {R["products"]}. branches: one branch, {R["branches"]}. customers: one loyalty customer, {n(R["customers"])}. '
                    f'branch_weeks: one branch in one week, {R["branch_weeks"]}. The formula is =COUNTA(orders!A2:A2001), and the same for each tab with its own name and last row. Do not count the header row.'),
        dict(task='Orders tab. Predict whether order_id is a primary key. Then test it: =COUNTA(orders!A2:A2001) and =COUNTA(UNIQUE(orders!A2:A2001)).',
             answer=f'Both formulas give {n(R["orders"])}. The counts match, so order_id is a primary key. branch_id and customer_id are foreign keys.'),
        dict(task='Order_lines tab. Write what a record is, name its primary key and its two foreign keys. How many different orders do the lines cover (=COUNTA(UNIQUE(order_lines!B2:B6591)))? How many lines does order O000003 have (=COUNTIF(order_lines!B2:B6591,"O000003"))?',
             answer=f'One record is one product on one order. Primary key: line_id. Foreign keys: order_id (to orders) and product_id (to products). The lines cover {n(F["distinct_orders_in_lines"])} different orders, which is every order, '
                    f'and {n(R["order_lines"])} divided by {n(R["orders"])} gives {lpo:.1f} lines per order. O000003 has {len(o3l)} lines. The order with the most lines, {F["max_basket_id"]}, has {F["max_basket"]}: test with =COUNTIF(order_lines!B2:B6591,"{F["max_basket_id"]}").'),
        dict(task='Foreign key check. Does every branch_id in orders exist in branches? Use =SUMPRODUCT(--ISNA(MATCH(orders!C2:C2001,branches!A2:A9,0))). Then repeat for product_id in order_lines against products.',
             answer=f'The first formula returns {F["orphans"]["order_branch"]}, so no order points to a missing branch. The same check for order_lines!C2:C6591 against products!A2:A151 returns {F["orphans"]["line_product"]}. '
                    f'A foreign key that finds no row would be an orphan; there are none here.'),
        dict(task='Branch_weeks tab. No single variable is unique. Count the different branch_id values and week_start values, multiply the two counts, and compare with the record count. Then test the pair: =COUNTA(UNIQUE(ARRAYFORMULA(branch_weeks!A2:A833&"|"&branch_weeks!B2:B833))).',
             answer=f'{F["bw_branches"]} different branches and {F["bw_weeks"]} different weeks ({F["bw_first"]} to {F["bw_last"]}). {F["bw_branches"]} × {F["bw_weeks"]} = {F["bw_pairs"]}, which equals the {R["branch_weeks"]} records. '
                    f'The pair test also gives {R["branch_weeks"]}, so branch_id and week_start together are a composite key.'),
        dict(task=f'Is customer_id a primary key of orders? Count the blanks (=COUNTBLANK(orders!D2:D2001)), the filled cells (=COUNTA(orders!D2:D2001)) and the different filled values (=COUNTUNIQUE(orders!D2:D2001)). What share of orders is blank?',
             answer=f'{n(blank)} blank, {n(filled)} filled, {n(distinct)} different values. The counts differ, so customer_id repeats and is not a primary key: it is a foreign key to customers. '
                    f'The blank share is {n(blank)} / {n(R["orders"])} = {F["blank_pct"]:.0f} percent: =COUNTBLANK(orders!D2:D2001)/COUNTA(orders!A2:A2001). The dictionary says a blank means a walk-in. '
                    f'{F["cust_repeat"][1]} customers ordered once, {F["cust_repeat"][2]} twice, {F["cust_repeat"][3]} three times and {F["cust_repeat"][4]} four times. COUNTUNIQUE ignores blank cells, so the blank is not counted as a customer. In Excel 365 use =COUNTA(UNIQUE(FILTER(orders!D2:D2001,orders!D2:D2001<>""))).'),
        dict(task='Add a variable type column to your dictionary for the seven variables of orders. Then test order_date with =ISNUMBER(orders!B2), =ISTEXT(orders!B2) and =DATEVALUE(orders!B2).',
             answer=f'order_id: identifier. order_date: datetime. branch_id: categorical (nominal). customer_id: identifier, with missing values. payment_method: categorical (nominal). promo_week: categorical (a 0 or 1 flag). order_value_ugx: numeric (continuous). '
                    f'ISNUMBER gives FALSE and ISTEXT gives TRUE, so the dates are stored as text. DATEVALUE turns {t["orders"].order_date.iloc[0]} into the serial number {F["datevalue_b2"]}, which Sheets can format as a date.'),
        dict(task=f'Follow order {s(o3.order_id)}. How many lines does it have, and what is their total (=SUMIF(order_lines!B2:B6591,"{s(o3.order_id)}",order_lines!G2:G6591))? Look up its products with =VLOOKUP("{s(p1.product_id)}",products!A2:E151,2,FALSE) and its branch with =VLOOKUP("B01",branches!A2:E9,2,FALSE).',
             answer=f'{len(o3l)} lines. The total is {n(F["o3_sum"])} UGX, equal to order_value_ugx in orders ({n(o3.order_value_ugx)}). Product {s(p1.product_id)} is {pn1.product_name} at {n(pn1.unit_price_ugx)} UGX, quantity {p1.quantity}, {n(p1.line_revenue_ugx)} UGX. '
                    f'Product {s(p2.product_id)} is {pn2.product_name} at {n(pn2.unit_price_ugx)} UGX, quantity {p2.quantity}, {n(p2.line_revenue_ugx)} UGX. The branch is {s(o3b.branch_name)} ({s(o3b.region)} region). The customer_id is blank, so there is no customer to look up.'),
        dict(task='Categorical variable. Count the orders for each payment method with =COUNTIF(orders!E2:E2001,"Cash"), then Mobile money and Card. How many different values does the variable have (=COUNTA(UNIQUE(orders!E2:E2001)))? Which spelling problems would you look for?',
             answer=f'Cash {n(pay["Cash"])}, Mobile money {n(pay["Mobile money"])}, Card {n(pay["Card"])}; together {n(sum(pay.values()))}. Different values: {F["pay_n"]}, so this workbook has one spelling for each method. '
                    f'The raw export has {F["raw_pay_spellings"]} spellings of the same three methods, which is why you check this before any pivot table.'),
        dict(task='Extreme values. Find the largest order_value_ugx with =MAX(orders!G2:G2001) and the median with =MEDIAN(orders!G2:G2001). Which order is it, at which branch? How many times larger than the median is it? Finish by writing one question you would send to the owner of this data.',
             answer=f'Largest: {n(F["max_order"])} UGX, order {F["max_order_id"]} at {F["max_order_branch"]} ({F["max_order_branch_name"]}), paid by {F["max_order_pay"].lower()}, with a blank customer_id. The median is {n(F["median_order"])} UGX, so the largest is about {ratio:.0f} times the median '
                    f'(=MAX(orders!G2:G2001)/MEDIAN(orders!G2:G2001) gives {ratio:.2f}). The second largest is {n(F["second_order"])} UGX. The question can be any clear one, for example: Is the {n(F["max_order"])} UGX order a real sale or a typing error?'),
    ]

    # ------------------------------------------------------------------ facilitator
    sess['facilitator'] = dict(
        prep=['Open the deck and the workbook lakeside_for_sheets.xlsx in Google Sheets before anyone arrives. Share the file so every learner can make their own copy (File, Make a copy).',
              'Check on your own copy that =COUNTA(UNIQUE(A2:A2001)), =COUNTUNIQUE(D2:D2001) and the ARRAYFORMULA pair test in task 5 return the numbers in the answer key. These were computed in pandas, not yet in Sheets.',
              'Write the check table (slide 24 of the deck) on the board before the lab.',
              'Concepts run with laptops closed. Ask learners to open the workbook only after the Part 2 divider.',
              'Remind learners that all data is fictional and generated; the Lakeside workbook holds a 2,000-order sample of the full file.'],
        misconceptions=[('Granularity or grain is a new idea invented for this course', 'Record, observation and unit of observation are standard statistics words. Granularity is standard database wording, and data warehouse teams say grain.'),
                        ('An ID like order_id is a number, so I can sum or average it', 'An identifier is a label. Adding or averaging it has no meaning.'),
                        ('A blank cell is an error, so delete the row or fill it with 0', f'Ask what the blank means first. Here {n(blank)} blank customer_id values are walk-in customers, and 0 would be an invented customer.'),
                        ('The number of rows in order_lines is the number of orders', f'A record in order_lines is a product on an order. Orders are counted in the orders tab: {n(R["orders"])}.'),
                        ('If a value repeats it cannot be a key of any kind', 'A foreign key repeats on purpose. Only a primary key must never repeat. A composite key repeats in each part but not as a pair.')],
        probes=[('What is the unit of observation of the branch_weeks tab?', 'One branch in one week.'),
                ('What does a record, an observation and an instance mean?', 'The same thing: one row of the table.'),
                ('How do you test a primary key in Sheets?', 'Count the filled cells with COUNTA and the different values with COUNTA(UNIQUE()). If equal, it can be a primary key.'),
                ('Why is branch_id in orders a foreign key and in branches a primary key?', 'In branches each branch appears once. In orders it repeats and points to a record in branches.'),
                ('What does one-to-many mean for branches and orders?', 'One branch has many orders. Many orders belong to one branch.'),
                ('Why not delete the 580 orders without a customer_id?', 'They are walk-in orders, 29 percent of the data, and they hold real sales.'),
                ('Is promo_week numeric?', 'It is stored as an integer, but it is a 0 or 1 flag, so its variable type is categorical.'),
                ('Why does ISNUMBER on an order_date return FALSE?', 'The dates are stored as text in this workbook.')],
        lab_steps=[('Task 1: dictionary tab and record counts', f'Six record sentences and counts {n(R["orders"])}, {n(R["order_lines"])}, {R["products"]}, {R["branches"]}, {n(R["customers"])}, {R["branch_weeks"]}. Watch for a range that includes the header row.'),
                   ('Task 2: orders key', f'Both counts equal {n(R["orders"])}. The answer is a primary key, written with the test as evidence.'),
                   ('Task 3: order_lines', f'Key line_id, two foreign keys. {n(F["distinct_orders_in_lines"])} orders and {lpo:.1f} lines per order. Do not accept {n(R["order_lines"])} orders.'),
                   ('Task 4: foreign key check', 'Both SUMPRODUCT checks return 0. If one returns a large number the range is the wrong size, and MATCH is comparing against a short range.'),
                   ('Task 5: composite key', f'{F["bw_branches"]} × {F["bw_weeks"]} = {F["bw_pairs"]}. Learners who find it hard to see why can write three rows on the board.'),
                   ('Task 6: customer_id', f'{n(blank)} blank, {n(filled)} filled, {n(distinct)} different. Not a key. Make sure the blank is called a walk-in.'),
                   ('Task 7: types and the date', 'Seven types written; ISNUMBER FALSE. Several learners will think the formula is wrong. It is right.'),
                   ('Task 8: follow one order', f'{len(o3l)} lines totalling {n(F["o3_sum"])} UGX at {s(o3b.branch_name)}; no customer.'),
                   ('Task 9: categories', f'Counts {n(pay["Cash"])}, {n(pay["Mobile money"])}, {n(pay["Card"])}, summing to {n(R["orders"])}.'),
                   ('Task 10: extreme value and one question', f'{n(F["max_order"])} UGX, about {ratio:.0f} times the median. Praise questions that ask the data owner a specific thing.')],
        rescue=['If the concepts run over, shorten the six-checks table (slide 18) and the ERD to a quick look; the lab covers both.',
                'If only 30 minutes of lab remain, do tasks 1, 2, 3, 6, 7 and 10 and set the rest as homework.',
                'If a learner has Excel and not Sheets, COUNTUNIQUE does not exist: use =SUMPRODUCT(1/COUNTIF(range,range)) on a range without blanks, or =COUNTA(UNIQUE(FILTER(range,range<>""))) in Excel 365.',
                'If a learner has no laptop, pair them with a neighbour: one types, one predicts aloud.'],
        after=['Share the workbook and this deck again for learners who were absent.', 'Ask each learner to save the dictionary tab and bring one question about their own data to Session 3.', 'Note any question you could not answer and open the next session with it.'],
        lab_answer_key=[['Task 2 PREDICT: will COUNTA(UNIQUE()) of order_id equal COUNTA?', f'Yes, both {n(R["orders"])}. Every order has its own order_id.'],
                        ['Task 3 PREDICT: how many different orders do the lines cover?', f'{n(F["distinct_orders_in_lines"])}, every order, with {lpo:.1f} lines on average.'],
                        ['Task 5 READ: which two variables make the composite key of branch_weeks?', f'branch_id and week_start. {F["bw_branches"]} × {F["bw_weeks"]} = {F["bw_pairs"]}.'],
                        ['Task 6 READ: why do the two counts differ for customer_id?', 'Some customers ordered more than once, so the value repeats. And the walk-in orders are blank.'],
                        ['Task 7 READ: what does FALSE from ISNUMBER tell you?', 'The date is stored as text, so it will not sort or group by month until converted.'],
                        ['Task 8 CHANGE: look up product P043 instead.', f'{pn2.product_name}, unit price {n(pn2.unit_price_ugx)} UGX.'],
                        ['Task 9 CHANGE: add the three counts. What do you get?', f'{n(R["orders"])}, the number of orders, because each order has exactly one payment method.'],
                        ['Task 10 READ: is the largest order an error?', f'Unknown. It is {ratio:.0f} times the median. Ask the data owner. Do not delete it without an answer.']])
    return sess
