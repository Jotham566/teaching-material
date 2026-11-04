"""Session 8: pandas II, cleaning the mess (Project milestone 1). Duplicates, data type conversion (to_numeric, to_datetime with format), string methods,
missing-value strategies (drop, impute, indicator flag), outliers (IQR rule), the data cleaning log and the reconciliation to a control total.
Python lab: content/labs/s08_nb.py.

Every number on a slide, in a note or in the lab checks is computed in facts() by running the cleaning pipeline with pandas on the real files.
Terminology: the gap between the cleaned total and the control total is the 'reconciliation difference', never a 'residual'.
"""
import json
from functools import lru_cache
from pathlib import Path

import pandas as pd

BUILD = Path(__file__).resolve().parents[1]
DATA = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'data'


def n(x):
    return f'{int(x):,}'


def s(x):
    return '' if pd.isna(x) else str(x)


@lru_cache(maxsize=None)
def facts():
    raw = pd.read_csv(DATA / 'orders_raw.csv')
    rawt = pd.read_csv(DATA / 'orders_raw.csv', dtype=str, keep_default_na=False)
    key = json.load(open(DATA / 'answer_key.json'))['dirty_export']
    F = dict(raw=raw)
    F['raw_rows'], F['raw_cols'] = raw.shape
    F['control_total'] = int(key['true_net_revenue_ugx'])
    # defects in the raw file
    F['raw_slash'] = int(raw.order_date.str.contains('/').sum())
    F['raw_price_text'] = int(raw.unit_price.str.contains('UGX').sum())
    F['raw_pay_spell'], F['raw_branch_spell'] = int(raw.payment.nunique()), int(raw.branch.nunique())
    F['raw_cust'] = {k: int((rawt.customer_id == v).sum()) for k, v in (('empty', ''), ('na', 'N/A'), ('null', 'NULL'), ('walkin', 'walk-in'))}
    F['raw_cust_nan'] = int(raw.customer_id.isna().sum())
    assert F['raw_cust_nan'] == F['raw_cust']['empty'] + F['raw_cust']['na'] + F['raw_cust']['null']
    F['raw_negative'] = int((raw.qty < 0).sum())
    F['raw_qty_blank'] = int(raw.qty.isna().sum())
    # the pipeline, step by step, with the same code the lab uses
    log = []

    def note(step, before, after, why):
        log.append(dict(step=step, rows_before=before, rows_after=after, why=why))

    df = raw.copy()
    # counts in the raw file and after the duplicates are dropped (for the footnote on the defect table)
    dd = raw.drop_duplicates()
    F['after_dup'] = dict(slash=int(dd.order_date.str.contains('/').sum()), price=int(dd.unit_price.str.contains('UGX').sum()), cust=int(dd.customer_id.isna().sum()), neg=int((dd.qty < 0).sum()))
    # 1 duplicates
    dup_pairs = raw[raw.duplicated(keep=False)].sort_values('line_id')
    F['dup_excerpt'] = dup_pairs.head(4)
    before = len(df)
    F['n_dupes'] = int(df.duplicated().sum())
    df = df.drop_duplicates()
    F['key_unique'] = bool(df['line_id'].is_unique)
    note('Drop exact duplicates', before, len(df), f'{F["n_dupes"]} identical lines')
    F['rows_dedup'] = len(df)
    # 2 prices
    F['price_before'] = df.unit_price.map(type).iloc[0].__name__
    try:
        pd.to_numeric(df['unit_price'])
    except Exception as e:  # noqa: BLE001
        F['err_numeric'] = f'{type(e).__name__}: {e}'
    F['n_price_coerce_nan'] = int(pd.to_numeric(df['unit_price'], errors='coerce').isna().sum())
    F['n_price_text'] = int(df.unit_price.str.contains('UGX').sum())
    price_ex = df[df.unit_price.str.contains('UGX')].iloc[0]
    p = df['unit_price'].str.replace('UGX', '').str.replace(',', '')
    df['unit_price'] = pd.to_numeric(p)
    F['price_dtype'] = str(df['unit_price'].dtype)
    F['price_ex'] = (str(price_ex.line_id), str(price_ex.unit_price), int(df.loc[price_ex.name, 'unit_price']))
    note('Price text to number', len(df), len(df), f'{n(F["n_price_text"])} prices such as UGX 7,800')
    # 3 dates
    d0 = df['order_date']
    F['date_before_ex'] = [(str(df.line_id.iloc[i]), str(d0.iloc[i])) for i in (0, 4, 5)]
    iso = pd.to_datetime(d0, format='%Y-%m-%d', errors='coerce')
    uk = pd.to_datetime(d0, format='%d/%m/%Y', errors='coerce')
    us = pd.to_datetime(d0, format='%m/%d/%Y', errors='coerce')
    F['n_iso_nat'], F['n_uk_nat'] = int(iso.isna().sum()), int(uk.isna().sum())
    sl = d0.str.contains('/')
    F['n_slash'] = int(sl.sum())
    F['n_wrong_month'] = int((us[sl].notna() & (us[sl] != uk[sl])).sum())
    F['n_wrong_nat'] = int(us[sl].isna().sum())
    F['n_same'] = int((us[sl] == uk[sl]).sum())
    assert F['n_wrong_month'] + F['n_wrong_nat'] + F['n_same'] == F['n_slash']
    df['order_date'] = iso.fillna(uk)
    F['n_date_nat'] = int(df['order_date'].isna().sum())
    F['date_min'], F['date_max'] = str(df['order_date'].min().date()), str(df['order_date'].max().date())
    F['date_after_ex'] = [str(df.order_date.iloc[i].date()) for i in (0, 4, 5)]
    F['date_ex_slash'] = str(d0.iloc[4])
    note('Two date formats to dates', len(df), len(df), f'{n(F["n_slash"])} day/month/year dates')
    # 4 text
    df['branch'] = df['branch'].str.strip().str.title()
    df['branch'] = df['branch'].replace({'Kampala Cntral': 'Kampala Central', 'Entebe': 'Entebbe'})
    pay = df['payment'].str.strip().str.lower()
    df['payment'] = pay.replace({'mm': 'mobile money'}).str.capitalize()
    F['branch_n'], F['pay_n'] = int(df['branch'].nunique()), int(df['payment'].nunique())
    F['pay_counts'] = {k: int(v) for k, v in df['payment'].value_counts().items()}
    note('Branch and payment text', len(df), len(df), f'{F["raw_branch_spell"]} branch spellings to {F["branch_n"]}, {F["raw_pay_spell"]} payment spellings to {F["pay_n"]}')
    # 5 missing customers, flag then fill
    F['n_cust_nan'] = int(df['customer_id'].isna().sum())
    F['n_walkin_before'] = int((df['customer_id'] == 'walk-in').sum())
    F['n_dropna_all'] = len(df.dropna())
    F['n_dropna_lost'] = len(df) - F['n_dropna_all']
    F['dropna_share'] = F['n_dropna_lost'] / len(df) * 100
    df['customer_missing'] = df['customer_id'].isna()
    F['n_flag'] = int(df['customer_missing'].sum())
    df['customer_id'] = df['customer_id'].fillna('walk-in')
    F['n_walkin'] = int((df['customer_id'] == 'walk-in').sum())
    note('Flag and fill blank customers', len(df), len(df), f'{n(F["n_flag"])} blanks flagged, then labelled walk-in')
    # 6 blank qty
    lost = df[df.qty.isna()]
    F['n_lost'] = len(lost)
    F['lost_unit_value'] = float((lost.unit_price * (1 - lost.discount_pct / 100)).sum())
    b = len(df)
    df = df.dropna(subset=['qty'])
    F['rows_clean'] = len(df)
    note('Drop lines with blank qty', b, len(df), f'{len(lost)} lines: the quantity cannot be recovered')
    # 7 outliers and checks
    prod = pd.read_csv(DATA / 'products.csv')
    chk = df.merge(prod, on='product_id')
    F['n_mismatch'] = int((chk.unit_price != chk.unit_price_ugx).sum())
    F['n_returns'] = int((df.qty < 0).sum())
    F['n_return_ids'] = int(df.line_id.str.endswith('R').sum())
    F['qty_min'], F['qty_max'] = int(df.qty.min()), int(df.qty.max())
    df['revenue'] = df.qty * df.unit_price * (1 - df.discount_pct / 100)
    rv = df['revenue']
    q1, q3 = rv.quantile([.25, .75])
    F['rev_q1'], F['rev_q3'] = float(q1), float(q3)
    F['rev_iqr'] = float(q3 - q1)
    F['rev_hi'], F['rev_lo'] = float(q3 + 1.5 * (q3 - q1)), float(q1 - 1.5 * (q3 - q1))
    F['n_rev_hi'] = int((rv > F['rev_hi']).sum())
    F['n_rev_lo'] = int((rv < F['rev_lo']).sum())
    note('Check outliers, keep returns', len(df), len(df), f'{n(F["n_returns"])} returns kept. IQR rule on revenue: {n(F["n_rev_hi"])} high and {n(F["n_rev_lo"])} low lines, all kept')
    # 8 reconcile
    F['net'] = int(round(rv.sum()))
    F['diff'] = F['control_total'] - F['net']
    assert F['net'] == key['pipeline_net_revenue_ugx'] and F['diff'] == key['residual_ugx']
    F['units_each'] = F['diff'] / F['lost_unit_value']
    F['mean_qty_pos'] = float(df[df.qty > 0].qty.mean())
    F['log'] = log
    F['df'] = df
    # orders.csv outlier example (same file as Session 7)
    o = pd.read_csv(DATA / 'orders.csv')
    v = o.order_value_ugx
    oq1, oq3 = v.quantile([.25, .75])
    F['o_q1'], F['o_q3'], F['o_med'] = int(oq1), int(oq3), int(v.median())
    F['o_iqr'] = F['o_q3'] - F['o_q1']
    F['o_hi'] = F['o_q3'] + 1.5 * F['o_iqr']
    F['o_lo'] = F['o_q1'] - 1.5 * F['o_iqr']
    F['o_n_hi'] = int((v > F['o_hi']).sum())
    F['o_n_lo'] = int((v < F['o_lo']).sum())
    F['o_min'], F['o_max'], F['o_rows'] = int(v.min()), int(v.max()), len(o)
    F['o_hi_in'] = int(v[v <= F['o_hi']].max())
    # loans
    loans = pd.read_csv(DATA / 'loans.csv')
    F['loans_rows'] = len(loans)
    F['loans_no_income'] = int(loans.monthly_income_ugx.isna().sum())
    F['loans_median_income'] = int(loans.monthly_income_ugx.median())
    ex = loans[loans.monthly_income_ugx.isna()].head(3)
    F['impute_ex'] = [(str(r.loan_id), int(r.age)) for r in ex.itertuples()]
    a = loans.age
    aq1, aq3 = a.quantile([.25, .75])
    F['age_lo'], F['age_hi'] = float(aq1 - 1.5 * (aq3 - aq1)), float(aq3 + 1.5 * (aq3 - aq1))
    F['age_flags'] = int(((a < F['age_lo']) | (a > F['age_hi'])).sum())
    F['age_bad'] = sorted(int(x) for x in a[(a < 15) | (a > 100)])
    cl = pd.read_csv(DATA / 'clinic_visits.csv')
    F['clinic_blank'], F['clinic_rows'] = int(cl.total_visits.isna().sum()), len(cl)
    return F


def build():
    F = facts()
    df = F['df']
    R, C = F['raw_rows'], F['control_total']
    log = F['log']
    sess = dict(
        num=8, block='Module B: Python for data', short_title='pandas II cleaning the mess',
        title='pandas II: cleaning the mess, with a log and a reconciled total',
        question='How do we make a raw export trustworthy, and prove what we changed?',
        outcomes=['Remove duplicates, convert data types and dates, and clean text, each step with a stated rule',
                  'Handle missing values by dropping, imputing or flagging, and check outliers with the IQR rule before removing anything',
                  'Write a data cleaning log and reconcile the cleaned total to a control total'],
        outcome_icons=['gear', 'magnifier', 'calculator'],
        outcome_note=('Here is what you can do by the end of today. You can remove duplicates, convert data types and dates, and clean text, with a rule you can state for every step. '
                      'You can handle missing values by dropping, imputing or flagging, and you can check outliers with the interquartile range rule before you remove anything. '
                      'And you can write a data cleaning log and reconcile your cleaned total to a control total, then explain the reconciliation difference. Today is also Project milestone 1: a cleaned file with its log, which you show me for feedback and nobody scores.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: picture, plain words, one example by hand'), (10, 'Break'), (45, 'Lab: predict, run, read, change'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: concepts first, then the Project milestone 1 lab',
        plan_caption='Ideas with pictures first. Then you clean the file in the notebook. Then the checks and what you keep.',
        plan_note=('We have two hours. The first ten minutes bring back Session 7 and set the question for today. Then forty-five minutes of concepts, with laptops closed: the eight defects in the file, the fix for each, and how we prove the total. '
                   'After a ten minute break we open the notebook for a forty-five minute lab. You clean the raw export step by step, keep a log, and reconcile the total. '
                   'The last ten minutes are the exit check and what you keep. Today the lab produces Project milestone 1, so please protect that time.'),
        recall_from='Session 7',
        recall=[('Which line counts the empty cells in each column of a DataFrame?', 'orders.isna().sum(): isna marks each empty cell True, and sum adds the Trues for each column.'),
                ('How do you filter rows on two conditions?', 'Put each test in round brackets and join them with & for and, or | for or.'),
                ('You report a figure from a filtered table. What goes beside it?', 'The row count, so the reader knows how many rows the figure covers.')],
        words=[('Data cleaning log', 'A table of every change to the data, with the row counts before and after and the reason. It is the audit trail of the cleaning.'),
               ('Imputation', 'Filling a missing value with a stated value, such as the median or a constant. Keep a flag to show which values were filled.'),
               ('Outlier (IQR rule)', 'A value far from the rest. The IQR rule flags values more than 1.5 times the interquartile range beyond the quartiles.'),
               ('Control total', 'A total that comes from a trusted source, such as the till system, used to test your own total.'),
               ('Reconciliation difference', 'The gap between your cleaned total and the control total. Explain it, or find the defect behind it.')],
        word_icons=['doc', 'tag', 'magnifier', 'calculator', 'flag'],
        words_note=('Five words for today. A data cleaning log is the table of every change, with row counts before and after. Imputation means filling a missing value with a stated value. '
                    'An outlier is a value far from the rest, and the IQR rule is the standard way to flag one. A control total is a trusted total, for example from the till system. '
                    'And the reconciliation difference is the gap between your cleaned total and that control total. We use every one of them before the end of the session.'),
        keep='Keep your notebook, the file orders_clean.csv, and your data cleaning log with its reconciliation note: a file you can hand to a manager with the proof of what you changed.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab file', value='orders_clean.csv'), dict(label='The key proof', value='Log and reconciled total'), dict(label='Next session', value='Group, join, reshape')]),
        keep_title='Save your notebook, orders_clean.csv and the log',
        next='Session 9: pandas III, group, join and reshape. We answer questions that need several tables and several groups.', next_label='Next session',
        keep_note=('Before you go, save your notebook to Google Drive and download orders clean dot csv. Together with your cleaning log and your note on the reconciliation difference, that is the proof of your work, and it is your Project milestone 1. You show it to me for feedback, and nobody scores it. '
                   'The same method works on any export you receive at work: copy the raw file, fix one defect at a time, log each step, and reconcile the total to a number you trust. '
                   'Next session we group, join and reshape tables. If anything was unclear today, write the question down and bring it.'),
        cover_note=('Welcome back. Last session we opened a tidy file and asked it questions. Today the file is the kind that arrives in daily life: an export straight from a till system, with copies of the same line, two date formats, prices stored as text and spellings that wander. '
                    'We will clean it one defect at a time, keep a log of every change, and prove that the total is right. Today you also produce Project milestone 1, which you keep and show me for feedback.'),
        use_at_work='Clean any raw export, log each change, and reconcile the total to a control total.',
        slides=[])
    S = sess['slides']

    # ---- 1 answers
    S.append(dict(kind='table', title='Answers to the three questions from Session 7', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in sess['recall']], widths=[5.2, 6.8], icons=['question', 'check', 'calculator'],
                  notes=('Here are the answers to the three warm-up questions. The line that counts the empty cells is isna followed by sum: isna marks each empty cell as True, and sum adds the Trues for each column. '
                         'To filter on two conditions, put each test in round brackets and join them with the ampersand for and, or the vertical bar for or. '
                         'And a figure from a filtered table always needs its row count beside it. Today that habit grows into the data cleaning log, where we write the row count before and after every change. Which of the three did you find hardest?')))

    # ---- 2 workflow
    S.append(dict(kind='steps', title='Cleaning is a workflow: keep the raw file, fix one defect at a time, log it, then reconcile',
                  steps=[dict(head='Keep raw', text='Never edit the original', icon='lock'), dict(head='Copy', text='Clean the copy, df', icon='folder'), dict(head='Fix one defect', text='Then check the row count', icon='gear'),
                         dict(head='Log it', text='Rows before, rows after, why', icon='doc'), dict(head='Reconcile', text='Match a control total', icon='calculator')], highlight=None,
                  caption='Data cleaning means making a file correct and consistent enough to analyse. Each change is small, checked and written down.',
                  notes=('Cleaning is a workflow, and the workflow is the same on every file. First, keep the raw file exactly as it arrived, and never edit it. Second, make a copy, which we call df, and clean the copy. '
                         'Third, fix one defect at a time, and check the row count after each fix. Fourth, write each change in a log, with the rows before, the rows after and the reason. '
                         'Fifth, reconcile: compare your total with a total that comes from a trusted source. Why do you think we change only one thing at a time?')))

    # ---- 3 eight defects
    S.append(dict(kind='table', title=f'Eight defects are hidden in the {n(R)} lines of the raw export', headers=['Defect', 'What you see in the raw file', 'Fix'],
                  rows=[['Exact duplicates', f'{F["n_dupes"]} lines repeat another line', 'drop_duplicates'], ['Date as text, two formats', f'{n(F["raw_slash"])} dates like 04/09/2025', 'to_datetime with a format'],
                        ['Price as text', f'{n(F["raw_price_text"])} prices like UGX 7,800', 'to_numeric'], ['Payment spellings', f'{F["raw_pay_spell"]} spellings of 3 methods', 'String methods'],
                        ['Branch spellings', f'{F["raw_branch_spell"]} spellings of 8 branches', 'String methods'], ['Blank customer', f'{n(F["raw_cust_nan"])} blanks in 3 spellings', 'Flag, then fill'],
                        ['Blank quantity (qty)', f'{F["raw_qty_blank"]} lines', 'Drop, and explain'], ['Returns', f'{n(F["raw_negative"])} negative quantities', 'Check, then keep']],
                  widths=[3.4, 5.0, 3.5], icons=['doc', 'calendar', 'coin', 'tag', 'shop', 'person', 'question', 'cross'], note='Counts are for the raw file. After the {D} duplicates are dropped: slash dates {a}, text prices {b}, blank customers {c}, negative quantities {d}.'.format(D=F['n_dupes'], a=n(F['after_dup']['slash']), b=n(F['after_dup']['price']), c=n(F['after_dup']['cust']), d=n(F['after_dup']['neg'])),
                  notes=(f'The raw export has {n(R)} lines, and eight defects. Eighty lines are exact copies of other lines. Dates come in two formats, and prices are sometimes text with the letters UGX in front. '
                         f'The same payment method is spelled {F["raw_pay_spell"]} ways, and the branches {F["raw_branch_spell"]} ways. Customers are blank in three different spellings. Twelve lines have no quantity. '
                         'And some quantities are negative, which are returns. The counts in the table are for the raw file. Later slides use the counts after the duplicates are dropped, which are a little smaller. Each defect has a fix, and today we do all eight in order. Which of them would you spot first in Excel?')))

    # ---- 4 read_csv NaN gotcha
    rc = F['raw_cust']
    S.append(dict(kind='wide', title='read_csv turns N/A and NULL into NaN, so three blank spellings are already one',
                  visual=dict(kind='ds_console', panels=[
                      dict(code=["t = pd.read_csv('orders_raw.csv', dtype=str, keep_default_na=False)", "t['customer_id'].value_counts().head(4)"],
                           out=['customer_id', f'{"":<10}{rc["empty"]:>6}', f'N/A{"":<7}{rc["na"]:>6}', f'NULL{"":<6}{rc["null"]:>6}', f'walk-in{"":<3}{rc["walkin"]:>6}'], hl=[1, 2, 3], notes=[(2, 'Read as plain text: three spellings of a blank.')]),
                      dict(code=["raw = pd.read_csv('orders_raw.csv')", "raw['customer_id'].isna().sum()"], out=[str(F['raw_cust_nan'])], notes=[(0, f'The default read turns all three into NaN: {n(rc["empty"])} + {n(rc["na"])} + {n(rc["null"])}.')])]),
                  caption='The 1,833 walk-in labels stay as text. value_counts(dropna=False) counts the NaN too.'.replace('1,833', n(rc['walkin'])),
                  notes=(f'A useful surprise. When I read the file as plain text, the customer column holds {n(rc["empty"])} empty cells, {n(rc["na"])} cells that say N slash A, {n(rc["null"])} that say NULL, and {n(rc["walkin"])} that say walk-in. Four spellings of the same idea. '
                         f'But the normal read csv already treats empty, N slash A and NULL as missing, and turns them into NaN. So pandas counts {n(F["raw_cust_nan"])} missing values, the sum of the three. Only the label walk-in stays as text. '
                         'That is helpful, and you should know it happens. Adding dropna equals False to value counts makes it count the blanks as well. What would you check if a column should never be blank?')))

    # ---- 5 duplicates
    de = F['dup_excerpt']
    left_rows = [[s(r.line_id), s(r.order_id), s(r.qty), s(r.unit_price)] for r in de.itertuples()]
    S.append(dict(kind='wide', title='An exact duplicate repeats another record in every variable, and drop_duplicates keeps the first',
                  visual=dict(kind='ds_before_after', left=dict(title=f'Before: {n(R)} lines', headers=['line_id', 'order_id', 'qty', 'unit_price'], rows=left_rows, hl=[(1, 0), (3, 0)]),
                              right=dict(title=f'After: {n(F["rows_dedup"])} lines', headers=['line_id', 'order_id', 'qty', 'unit_price'], rows=[left_rows[0], left_rows[2]], hl=[]),
                              code=['df = raw.drop_duplicates()', 'df["line_id"].is_unique'], caption=f'{F["n_dupes"]} duplicates removed. After the cleaning line_id is unique: {F["key_unique"]}. line_id is the primary key.'),
                  caption='Excel: Data, Remove Duplicates. pandas: duplicated(subset=...) checks chosen variables only.',
                  notes=(f'The first defect is the duplicate. A duplicate is a record that repeats another record in every variable. Look at the four real lines on the left. The two pairs are exact copies. '
                         f'The method drop duplicates keeps the first of each and drops the rest, so {F["n_dupes"]} lines disappear and {n(F["rows_dedup"])} remain. '
                         f'Then we test the key. Each line has a line id, the primary key, so after cleaning it should be unique, and the test returns {F["key_unique"]}. That proves no line id repeats, which exact duplicates would break. It does not find two different lines for the same sale: duplicated with the subset setting checks repeats on chosen variables only. In Excel the same tool is Remove Duplicates. '
                         'Why is a unique key a good proof that the duplicates are gone?')))

    # ---- 6 to_numeric
    S.append(dict(kind='compare', title='to_numeric converts text to numbers, and errors decides what happens to a bad value',
                  left=dict(head='errors raise (the default)', points=['Stops at the first bad value and names it.', 'Safe: you see the problem.']),
                  right=dict(head='errors coerce', points=['Turns each bad value into NaN and carries on.', f'Here: {n(F["n_price_coerce_nan"])} silent NaN values.', 'Risky: no warning.']),
                  verdict='Remove the text first, convert, then count the NaN.',
                  notes=(f'Next, data type conversion. The prices are stored as text, so they cannot be added. The function to numeric converts text to numbers, and its errors setting decides what happens to a bad value. '
                         f'By default it raises an error and stops, and the message names the first value it could not read: UGX seven thousand eight hundred. That is the safe behaviour. '
                         f'With errors set to coerce, every bad value silently becomes NaN. On our raw prices that would blank {n(F["n_price_coerce_nan"])} prices without a word. So remove the letters and the comma first, then convert, and always count the NaN afterwards. What would that count have told you here?')))

    # ---- 7 price before after
    pe = F['price_ex']
    S.append(dict(kind='wide', title='Strip the letters and the comma, then to_numeric: object becomes int64',
                  visual=dict(kind='ds_before_after', left=dict(title='Before: unit_price is object (text)', headers=['line_id', 'unit_price'], rows=[[pe[0], pe[1]], ['L084580', '7000']], hl=[(0, 1)]),
                              right=dict(title=f'After: unit_price is {F["price_dtype"]}', headers=['line_id', 'unit_price'], rows=[[pe[0], str(pe[2])], ['L084580', '7000']], hl=[(0, 1)]),
                              code=["p = df['unit_price'].str.replace('UGX', '')", "p = p.str.replace(',', '')", "df['unit_price'] = pd.to_numeric(p)"], caption=f'{n(F["n_price_text"])} prices had the UGX text. After the conversion the type is {F["price_dtype"]} and no value is NaN.'),
                  caption='A price stored as text cannot be added up. A number can.',
                  notes=(f'Here is the fix. The str dot replace method removes the letters UGX, and a second call removes the comma. The cleaned text goes into to numeric. Look at the real line on the left: UGX seven thousand eight hundred becomes the number 7800. '
                         f'{n(F["n_price_text"])} prices had that text. The data type of the column changes from object, which means text, to {F["price_dtype"]}, a whole number, and now it can be added. '
                         'Notice the habit: we check the type and count the NaN straight after the conversion. Where else might a number hide as text in your own files?')))

    # ---- 8 dates: to_datetime
    S.append(dict(kind='wide', title='to_datetime with a format reads each date style on its own, then fillna joins the two',
                  visual=dict(kind='ds_console', panels=[
                      dict(code=["d = df['order_date']", "iso = pd.to_datetime(d, format='%Y-%m-%d', errors='coerce')", "uk = pd.to_datetime(d, format='%d/%m/%Y', errors='coerce')", 'print(iso.isna().sum(), uk.isna().sum())'],
                           out=[f'{F["n_iso_nat"]} {F["n_uk_nat"]}'], notes=[(0, f'{n(F["n_iso_nat"])} dates do not fit the year-month-day format, and {n(F["n_uk_nat"])} do not fit day/month/year.')]),
                      dict(code=["df['order_date'] = iso.fillna(uk)", "d = df['order_date']", 'print(d.isna().sum(), d.min().date(), d.max().date())'],
                           out=[f'{F["n_date_nat"]} {F["date_min"]} {F["date_max"]}'], notes=[(0, 'No date is missing. The range is the two years of the file.')])]),
                  caption='%Y is the year, %m the month, %d the day. NaT means not a time: a date that failed.',
                  notes=(f'Dates come in two formats, so we read the column twice. The first read uses year, month, day and the second uses day, month, year, and each read turns what does not fit into NaT, which means not a time. '
                         f'The first read fails on {n(F["n_iso_nat"])} dates, the slash ones, and the second fails on {n(F["n_uk_nat"])}, the dash ones. The method fillna takes the first reading and fills the gaps from the second. '
                         f'After that no date is missing, and the earliest is {F["date_min"]} and the latest {F["date_max"]}, which matches the two years of the file. Always check the range after a date conversion. Why does the range prove something?')))

    # ---- 9 date fork
    S.append(dict(kind='wide', title='Reading day/month dates the wrong way round raises no error, so learn the rule first',
                  visual=dict(kind='ds_date_fork', text=F['date_ex_slash'], right_fmt="format='%d/%m/%Y'  (day first)", right_read='4 September 2025: the rule for this file', wrong_fmt="format='%m/%d/%Y'  (month first)", wrong_read='9 April 2025: valid, wrong, no error',
                                  parts=[('wrong month, no error', F['n_wrong_month'], '#E0BE36'), ('cannot be read: NaT', F['n_wrong_nat'], '#F0F0F0'), ('same either way', F['n_same'], '#FFFFFF')], total=F['n_slash']),
                  caption='Ask the data owner which date style the file uses, and write it in the log.',
                  notes=(f'This is the dangerous one. The text zero four slash zero nine slash twenty twenty five is a valid date both ways. Our rule says day first, so it is the fourth of September. '
                         f'If you guess month first, pandas reads it as the ninth of April and says nothing. Of the {n(F["n_slash"])} slash dates, {n(F["n_wrong_month"])} would silently get the wrong month, {n(F["n_wrong_nat"])} would fail because the day is above twelve, and only {F["n_same"]} would be right by luck. '
                         'The only defence is to learn the rule from whoever made the file, and to check the range afterwards. Who owns the data in your workplace?')))

    # ---- 10 string methods table
    S.append(dict(kind='table', title='String methods fix text one rule at a time', headers=['Method', 'What it does', 'Real example from the file'],
                  rows=[['str.strip', 'Removes spaces at both ends', 'a trailing space after Cash'], ['str.lower', 'Makes every letter lower case', 'CASH and cash become cash'], ['str.title', 'Capital letter on each word', 'KAMPALA NTINDA becomes Kampala Ntinda'],
                        ['replace with a dictionary', 'Swaps each listed value', 'MM becomes mobile money, Entebe becomes Entebbe'], ['str.capitalize', 'Capital letter on the first word', 'mobile money becomes Mobile money']],
                  widths=[3.3, 3.9, 4.8], icons=['tag', 'tag', 'tag', 'tag', 'tag'], note='Excel twins: TRIM, LOWER, PROPER and SUBSTITUTE.',
                  notes=('Text defects are fixed with string methods, which you write after dot str. Strip removes stray spaces at the ends. Lower makes every letter lower case, so CASH and cash match. Title puts a capital letter on each word, so KAMPALA NTINDA becomes Kampala Ntinda. '
                         'A dictionary with replace swaps listed values, such as MM to mobile money and the typo Entebe to Entebbe. And capitalize fixes the first letter. In Excel the twins are TRIM, LOWER, PROPER and SUBSTITUTE. '
                         'The order matters: strip and lower first, then replace, so the dictionary only needs one spelling of each. Why does the order matter?')))

    # ---- 11 string result
    S.append(dict(kind='wide', title=f'The same rules cut {F["raw_pay_spell"]} payment spellings to {F["pay_n"]} and {F["raw_branch_spell"]} branch spellings to {F["branch_n"]}',
                  visual=dict(kind='ds_console', panels=[
                      dict(code=["print(raw['payment'].nunique(), raw['branch'].nunique())"], out=[f'{F["raw_pay_spell"]} {F["raw_branch_spell"]}'], notes=[(0, 'Different values before cleaning: payment, then branch.')]),
                      dict(code=["b = df['branch'].str.strip().str.title()", "fix = {'Kampala Cntral': 'Kampala Central', 'Entebe': 'Entebbe'}", "df['branch'] = b.replace(fix)", "pay = df['payment'].str.strip().str.lower()",
                                 "df['payment'] = pay.replace({'mm': 'mobile money'}).str.capitalize()", "print(df['payment'].nunique(), df['branch'].nunique())"], out=[f'{F["pay_n"]} {F["branch_n"]}'], notes=[(0, 'After cleaning: three payment methods and eight branches.')])]),
                  caption='Check with value_counts that every remaining spelling is one you expect.',
                  notes=(f'Here are the rules applied. Branch gets strip and title, then a dictionary fixes the two typos. Payment gets strip and lower, then the dictionary changes MM to mobile money, and capitalize makes the first letter a capital. '
                         f'Before cleaning there were {F["raw_pay_spell"]} payment spellings and {F["raw_branch_spell"]} branch spellings. After cleaning there are {F["pay_n"]} payment methods and {F["branch_n"]} branches, which is what the business has. '
                         'A pivot table on the raw text would have split each real group into several. Always look at value counts afterwards to confirm. What would you do if a ninth branch appeared?')))

    # ---- 12 three strategies
    S.append(dict(kind='idea', title='A missing value has three treatments: drop, impute or flag',
                  visual=dict(kind='icons', items=[dict(head='Drop', text='Remove the record. Use it when the record is useless without the value.', icon='cross'), dict(head='Impute', text='Fill with a stated value: the median, the mean or a constant.', icon='calculator'),
                                                   dict(head='Flag', text='Add an indicator variable that says the value was missing.', icon='flag')]),
                  lead='First ask what the blank means. Then choose, and write the rule in the log.',
                  points=['Drop: a sale with no quantity (qty) cannot be priced.', 'Impute: a constant such as walk-in, or the median of a number.', 'Flag: keeps the memory that the value was missing.'],
                  notes=('Missing values need a decision, and there are three treatments. Drop means remove the record, which is right when it is useless without the value, like a sale with a blank quantity, the qty variable. '
                         'Impute means fill the blank with a stated value. For a number that is often the median, and for a label it can be a constant such as walk-in. And flag means add an indicator variable, a column of True and False that says this value was missing. '
                         'You can combine them: flag first, then impute. Whatever you choose, ask first what the blank means, and write the rule in your log. Which treatment would you use for a blank phone number?')))

    # ---- 13 customer flag and fill
    S.append(dict(kind='wide', title=f'Flag first, then fill: {n(F["n_flag"])} blank customers become walk-in, and the flag remembers them',
                  visual=dict(kind='ds_console', panels=[
                      dict(code=["df['customer_missing'] = df['customer_id'].isna()", "df['customer_id'] = df['customer_id'].fillna('walk-in')", "print(df['customer_missing'].sum(), (df['customer_id'] == 'walk-in').sum())"],
                           out=[f'{F["n_flag"]} {F["n_walkin"]}'], notes=[(0, f'{n(F["n_flag"])} flagged. {n(F["n_walkin"])} walk-in lines in all.')])]),
                  caption='The flag is an indicator variable: True where the value was missing before we filled it.',
                  notes=(f'Our customer blanks are walk-in shoppers, so we keep the records and fill the blank with the label walk-in. That is constant imputation. But first we add a flag, an indicator variable called customer missing, so we remember which blanks we filled. '
                         f'The print shows {n(F["n_flag"])} flagged. After filling there are {n(F["n_walkin"])} walk-in lines, which is the flagged blanks plus the {n(F["n_walkin_before"])} lines that already said walk-in. '
                         'This is informative missingness from Session 2. Why is it better to flag before you fill than after?')))

    # ---- 14 dropna trap
    S.append(dict(kind='wide', title=f'dropna with no settings would delete {F["dropna_share"]:.0f} percent of the lines, so name the column',
                  visual=dict(kind='ds_console', panels=[
                      dict(code=['len(df)', 'len(df.dropna())'], out=[str(F['rows_dedup']), str(F['n_dropna_all'])], hl=[1], notes=[(1, f'Any blank cell removes the line: {n(F["n_dropna_lost"])} lines gone, with their revenue.')]),
                      dict(code=["len(df.dropna(subset=['qty']))"], out=[str(F['rows_dedup'] - F['n_lost'])], notes=[(0, f'Only the {F["n_lost"]} lines with a blank qty are dropped.')])]),
                  caption='Run these before the customer step. Print the row count before and after every drop.',
                  notes=(f'A trap that runs without any error. You have blanks, you want a tidy table, so you call dropna with nothing in the brackets. It removes every line that has any empty cell. Because most walk-in lines have an empty customer, '
                         f'{n(F["n_dropna_lost"])} lines disappear, which is {F["dropna_share"]:.0f} percent of the file, and every shilling they brought in goes with them. '
                         f'Name the one variable that matters with the subset setting, and only the {F["n_lost"]} lines with a blank quantity go. These counts come from the table before we filled the customers. Always print the row count before and after a drop. Which count would have warned you?')))

    # ---- 15 imputation
    ie = F['impute_ex']
    S.append(dict(kind='wide', title='Median imputation fills a blank number, and an indicator variable keeps the memory',
                  visual=dict(kind='ds_before_after', left=dict(title='Before: income is missing', headers=['loan_id', 'monthly_income_ugx'], rows=[[a, 'NaN'] for a, _ in ie], hl=[(0, 1), (1, 1), (2, 1)]),
                              right=dict(title='After: filled with the median', headers=['loan_id', 'monthly_income_ugx', 'income_missing'], rows=[[a, n(F['loans_median_income']), 'True'] for a, _ in ie], hl=[(0, 1), (1, 1), (2, 1)]),
                              code=["median = loans['monthly_income_ugx'].median()", "loans['income_missing'] = loans['monthly_income_ugx'].isna()", "loans['monthly_income_ugx'] = loans['monthly_income_ugx'].fillna(median)"],
                              caption=f'loans.csv: {n(F["loans_no_income"])} of {n(F["loans_rows"])} loans had no income. Median income: UGX {n(F["loans_median_income"])}.'),
                  caption='The median resists extreme values. We do not impute quantities, which would change revenue.',
                  notes=(f'Imputation for a number. In the Nile Microfinance loans file, {n(F["loans_no_income"])} of {n(F["loans_rows"])} loans have no monthly income. A standard treatment is median imputation: fill each blank with the median income, which is {n(F["loans_median_income"])} shillings. '
                         'We use the median because a few very high incomes would pull the mean upward. And before filling we add an indicator variable, so a later model or a reader can tell the filled values from real ones. '
                         'We do not impute the quantity in our orders, because an invented quantity would change the revenue we are trying to prove. When is a made-up value more harmful than a missing one?')))

    # ---- 16 IQR formula
    S.append(dict(kind='formula', title='The IQR rule flags a value beyond 1.5 interquartile ranges from the quartiles',
                  formulas=[('IQR rule', r'$\mathrm{IQR} = Q_3 - Q_1 \qquad \mathrm{fences} = Q_1 - 1.5\,\mathrm{IQR},\; Q_3 + 1.5\,\mathrm{IQR}$'),
                            ('Our order values', f'${n(F["o_q3"])} - {n(F["o_q1"])} = {n(F["o_iqr"])} \\qquad \\mathrm{{upper\\ fence}} = {n(F["o_hi"])}$')],
                  symbols=[['Q1', 'First quartile: 25 percent of the values are smaller.', f'{n(F["o_q1"])} UGX'], ['Q3', 'Third quartile: 75 percent of the values are smaller.', f'{n(F["o_q3"])} UGX'],
                           ['IQR', 'Interquartile range: the spread of the middle half.', f'{n(F["o_iqr"])} UGX'], ['Fences', 'Values outside them are flagged as outliers.', f'lower {n(F["o_lo"])}, upper {n(F["o_hi"])}']],
                  size=24, note='A negative lower fence means no value can be flagged on the low side.',
                  notes=(f'The standard way to flag an outlier is the interquartile range rule. The first quartile, Q one, is the value that 25 percent of the data lie below, and Q three is the value for 75 percent. Their difference is the interquartile range, the spread of the middle half. '
                         f'For the order values in the orders file, Q one is {n(F["o_q1"])} and Q three is {n(F["o_q3"])}, so the range is {n(F["o_iqr"])}. The upper fence is Q three plus one and a half ranges, which is {n(F["o_hi"])}. '
                         f'The lower fence is negative, so nothing can be too small. Any order above the upper fence is flagged. In pandas you get the quartiles with the quantile method. Why one and a half? It is the box plot convention of the statistician John Tukey.')))

    # ---- 17 IQR figure
    S.append(dict(kind='wide', title=f'The IQR rule flags {n(F["o_n_hi"])} of {n(F["o_rows"])} orders, and each flag is a question to ask',
                  visual=dict(kind='ds_iqr', q1=F['o_q1'], med=F['o_med'], q3=F['o_q3'], lo=F['o_min'], hi_in=F['o_hi_in'], fence=int(F['o_hi']), n_out=F['o_n_hi'], vmax=F['o_max']),
                  caption='Order values from orders.csv, the full file. The gold box is the middle half of the orders.',
                  notes=(f'Here is the rule drawn on the real order values. The gold box holds the middle half of the orders, from {n(F["o_q1"])} to {n(F["o_q3"])} shillings, with the median line at {n(F["o_med"])}. '
                         f'The dashed fence sits at {n(F["o_hi"])}, and {n(F["o_n_hi"])} orders lie above it. The axis is broken because the largest order, {n(F["o_max"])} shillings, is far to the right. '
                         'Being flagged does not mean being wrong. A flag is a question to ask about the record. Is it a real big purchase, a typing error, or a different kind of record? What do you do next?')))

    # ---- 18 outlier decision
    S.append(dict(kind='table', title='Check an outlier before you remove it: real, error or a different kind of record', headers=['Case', 'Evidence from our files', 'Action'],
                  rows=[['A real extreme', f'Largest order {n(F["o_max"])} UGX: possible, so ask the data owner.', 'Keep. Note it in the log.'],
                        ['An impossible value', f'loans.csv: ages {F["age_bad"][0]} and {F["age_bad"][-1]} among {n(F["loans_rows"])} loans. The IQR rule flags {F["age_flags"]} ages, only 2 impossible.', 'Set to missing, then treat as missing.'],
                        ['A different kind of record', f'{n(F["n_returns"])} negative quantities: returns, with line_id ending in R.', 'Keep. They reduce revenue.'],
                        ['A value that should match a list', f'Prices differing from the price list: {F["n_mismatch"]}.', 'Nothing to fix. Log the check.']],
                  widths=[3.0, 5.6, 3.3], icons=['coin', 'cross', 'receipt', 'check'],
                  notes=(f'Four cases, four actions. A real extreme, like the largest order, is kept and noted, after asking the data owner. An impossible value is an error. In the loans file there are two impossible ages, {F["age_bad"][0]} and {F["age_bad"][-1]}. '
                         f'The IQR rule flags {F["age_flags"]} ages in all, so most flagged values are real older borrowers. Only the impossible ones are set to missing. Negative quantities are returns, a different kind of record, and we keep them because they reduce revenue. '
                         f'And we check our prices against the price list, finding {F["n_mismatch"]} differences. So what does the rule give you? A short list to investigate, never a delete button.')))

    # ---- 19 cleaning log
    S.append(dict(kind='table', title='The data cleaning log records every change with its row counts and its reason', headers=['Step', 'Rows before', 'Rows after', 'Why'],
                  rows=[[r['step'], n(r['rows_before']), n(r['rows_after']), r['why']] for r in log], widths=[3.0, 1.5, 1.5, 5.9], icons=False,
                  note='Equal counts: a step changed values and left the rows alone.',
                  notes=(f'Here is the log from our own cleaning, generated by the code we run in the lab. Read down. Dropping duplicates takes us from {n(log[0]["rows_before"])} to {n(log[0]["rows_after"])} lines. Five steps change values but leave the count alone, and equal counts are good news, '
                         f'because they prove we edited values without losing rows. Dropping the blank quantities takes us down to {n(F["rows_clean"])}. Anyone can read this table and see what changed and why. '
                         'It is the audit trail of the cleaning, and it is what makes a cleaned file trustworthy. Who would read your log at work?')))

    # ---- 20 reconcile figure
    S.append(dict(kind='wide', title='Reconcile: the cleaned total is compared with the control total, and the gap is explained',
                  visual=dict(kind='ds_reconcile', control=dict(label='Control total', value=n(C), unit='UGX, till system total'), cleaned=dict(label='Cleaned total', value=n(F['net']), unit='UGX, from our DataFrame'),
                              diff=dict(label='Reconciliation difference', value=n(F['diff']), unit='UGX'),
                              why=f'Likely cause: the {F["n_lost"]} dropped lines with a blank qty. One unit of each is worth {n(F["lost_unit_value"])} UGX after discount, so the difference equals about {F["units_each"]:.1f} units per line, a normal quantity. This is an estimate, because the true quantities are not in the file.'),
                  caption='Returns are already inside the cleaned total as negative lines.',
                  notes=(f'This is the proof. The control total is the till system total for the same lines: {n(C)} shillings. Our cleaned total is quantity times price, less the discount, summed over every cleaned line, and returns are inside it as negative amounts: {n(F["net"])}. '
                         f'The difference is {n(F["diff"])} shillings. We call it the reconciliation difference, and we must explain it. The {F["n_lost"]} dropped lines have a blank quantity, which is the likely cause. One unit of each would be worth {n(F["lost_unit_value"])} shillings, so the difference equals about {F["units_each"]:.1f} units per line, which is a normal quantity. '
                         'This is an estimate, because the true quantities are not in the file. We can name a likely cause, and we say so plainly. Could you explain a gap you had not traced?')))

    # ---- 21 formula reconciliation
    S.append(dict(kind='formula', title='The reconciliation difference is the control total minus the cleaned total',
                  formulas=[('Definition', r'$\mathrm{difference} = \mathrm{control\ total} - \mathrm{cleaned\ total}$'), ('Our data', f'${n(C)} - {n(F["net"])} = {n(F["diff"])}$')],
                  symbols=[['Control total', 'A total from a trusted source, here the till system.', f'{n(C)} UGX'], ['Cleaned total', 'Your total after cleaning, from the code.', f'{n(F["net"])} UGX'],
                           ['Difference', 'What is left unexplained. It must be explained, or it is a defect.', f'{n(F["diff"])} UGX']],
                  size=24, note='Use the name reconciliation difference. The word residual belongs to models, from Session 13.',
                  notes=('The reconciliation difference is the control total minus the cleaned total. A zero would be a perfect tie. A small difference with a named cause is acceptable. A difference that nobody can explain is a defect to hunt down. '
                         f'In our data the control total is {n(C)}, the cleaned total is {n(F["net"])}, and the difference is {n(F["diff"])} shillings. Please use the name reconciliation difference. '
                         'The word residual belongs to models, and we meet it in the regression sessions, where it means something different. Why is a tidy zero sometimes a warning sign?')))

    # ---- 22 project milestone
    S.append(dict(kind='table', title='Project milestone 1: what you produce and what a finished version contains', headers=['You produce', 'A finished version has'],
                  rows=[['The cleaned notebook', 'Every check cell says OK and the run ends with All checks pass.'], ['The data cleaning log', f'It has one row for each of the seven steps, and the last row ends at {n(F["rows_clean"])}.'],
                        ['A reconciliation note', f'One or two sentences name the reconciliation difference ({n(F["diff"])} UGX) and its likely cause.'], ['The files orders_clean.csv and cleaning_log.csv', 'They are saved from df and the log, and open in Excel or Sheets.']],
                  widths=[3.6, 8.3], icons=['notebook', 'doc', 'calculator', 'folder'], note='The log is saved as cleaning_log.csv. Your tutor reviews it with you for feedback. It is never scored.',
                  notes=('This session has Project milestone 1. You produce four things. The cleaned notebook, where every check cell says OK. The data cleaning log, with one row for each of the seven steps. '
                         f'A short reconciliation note, which names the reconciliation difference and its cause in your own words. And the cleaned file, orders clean dot csv. I will review them with you and give feedback, and nothing is scored. '
                         'You can ask me for help during the lab, but the explanation in the note has to be yours. What will your note say in one sentence?')))

    # ---- 23 use at work
    S.append(dict(kind='table', title='Where you will use this at work: clean, log and reconcile every export', headers=['Your job', 'The mess you meet', 'What you do with today'],
                  rows=[['Credit analyst at a bank, with pandas', f'loans.csv: {n(F["loans_no_income"])} blank incomes, ages {F["age_bad"][0]} and {F["age_bad"][-1]}.', 'Impute with a flag, set impossible ages to missing, and log both.'],
                        ['Finance officer reconciling till exports', f'A till export with {F["n_dupes"]} duplicate lines and prices stored as text.', 'Drop duplicates, convert prices, and reconcile it to the end-of-day control total.'],
                        ['Health records officer at a district office', f'Clinic file: {F["clinic_blank"]} blank months out of {n(F["clinic_rows"])}.', 'Flag the blank months instead of treating them as zero.'],
                        ['SACCO officer, using Excel', 'Member payment exports with several spellings.', 'Write the cleaning rules once and rerun them on each new export.']],
                  widths=[3.3, 4.4, 4.2], icons=['coin', 'receipt', 'clinic', 'people'],
                  notes=('Where will you use this on Monday? A credit analyst at a bank gets a loans file with blank incomes and impossible ages, and can impute with a flag and set the impossible ages to missing, logging each change. '
                         f'A finance officer who reconciles till exports meets duplicate lines and prices stored as text, and can reconcile the cleaned total to the end of day control total. '
                         f'A health records officer can flag the {F["clinic_blank"]} blank clinic months so that none is treated as zero. And a SACCO officer who uses Excel can write the cleaning rules once and rerun them on each new export. Which of these is closest to your job?')))

    # ---- 24 bridge
    S.append(dict(kind='code', title='Read the recipe before the lab: copy, drop duplicates, convert the price',
                  code="df = raw.copy()\ndf = df.drop_duplicates()\np = df['unit_price'].str.replace('UGX', '')\np = p.str.replace(',', '')\ndf['unit_price'] = pd.to_numeric(p)\nprint(df['unit_price'].dtype, len(df))",
                  output=[f'{F["price_dtype"]} {F["rows_dedup"]}'],
                  reads=['Line 1 copies raw. We never edit raw.', f'Line 2 drops {F["n_dupes"]} duplicate lines.', 'Lines 3 and 4 remove the text UGX and the comma.', 'Line 5 converts the text to numbers.', f'Line 6 prints the type, {F["price_dtype"]}, and the row count.'],
                  notes=(f'Before the lab, read this recipe. Line one copies the raw table, because we never edit the original. Line two drops the duplicates, {F["n_dupes"]} of them. Lines three and four take the text UGX and the comma out of the price. '
                         f'Line five converts the cleaned text to numbers. Line six prints the new data type, {F["price_dtype"]}, and the row count, {n(F["rows_dedup"])}. The output panel shows what the lines really printed. '
                         'In the lab you do this and every other step yourself, with a log entry after each. Which line would you change if the file used a different currency word?')))

    # ---- 25 divider
    S.append(dict(kind='divider', title='Part 2: the cleaning lab and Project milestone 1', lead='Close the slides. Open the notebook.', section='Lab',
                  notes=('That is the end of the ideas. Everything you need is on the slides you have just seen, and the notebook repeats each step. '
                         'Open the Session 8 notebook in Google Colab, run the first two cells, and upload the data file when it asks. Work down the notebook, and write a log entry after each cleaning step. '
                         'In every step, predict the answer first, run the cell, read the output, then change one thing. This lab produces Project milestone 1. The check cells tell you where you stand, and nobody marks them.')))

    # ---- 26 lab map
    S.append(dict(kind='steps', title='The lab has eight steps: seven cleaning steps and the reconciliation',
                  steps=[dict(head='1 Load, copy', text='raw, df and the log', icon='folder'), dict(head='2 Duplicates', text='drop_duplicates', icon='doc'), dict(head='3 Types, dates', text='to_numeric, to_datetime', icon='calendar'),
                         dict(head='4 Text, blanks', text='str methods, flag, fill, drop', icon='tag'), dict(head='5 Outliers, reconcile', text='IQR rule, reconcile, save', icon='calculator')], highlight=None,
                  caption='Eight steps in 45 minutes, grouped in five boxes. For each step: predict, run, read, change one thing, and add a log row.',
                  notes=('Here is the map of the lab. Step one, load the raw file, copy it, and set up the log. Step two, drop the duplicates. Step three, convert the prices and the dates. '
                         'Step four, clean the branch and payment text. Step five, flag and fill the blank customers and drop the blank quantities. Step six, check the outliers with the IQR rule and keep the returns. '
                         'Step seven, reconcile your total with the control total and name the reconciliation difference. Step eight, save the cleaned file and read your log. Please add a log row after each cleaning step.')))

    # ---- 27 check numbers
    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Shape of raw', f'({n(R)}, {F["raw_cols"]})'], ['Duplicates removed, rows after', f'{F["n_dupes"]}, {n(F["rows_dedup"])}'], ['Prices with UGX text, dtype after to_numeric', f'{n(F["n_price_text"])}, {F["price_dtype"]}'],
                        ['Dates missing after the two formats, earliest and latest', f'{F["n_date_nat"]}, {F["date_min"]} and {F["date_max"]}'], ['Different branches and payment methods after cleaning', f'{F["branch_n"]} and {F["pay_n"]}'],
                        ['Blank customers flagged, walk-in lines after filling', f'{n(F["n_flag"])} and {n(F["n_walkin"])}'], ['Lines with blank qty dropped, rows left', f'{F["n_lost"]}, {n(F["rows_clean"])}'],
                        ['Cleaned total and reconciliation difference', f'{n(F["net"])} and {n(F["diff"])}']],
                  widths=[7.2, 4.8], icons=['grid', 'doc', 'coin', 'calendar', 'shop', 'person', 'question', 'calculator'], note='If your number differs, find the step that went wrong. Do not change a number to match.',
                  notes=('Use this table as your own self-check. Nobody marks it. If your numbers match, carry on. If one does not, stop and ask, because later steps use the earlier ones. '
                         'The most common causes are cleaning raw instead of the copy, converting the dates in the wrong order, and calling dropna with no settings. '
                         'Do not change a number to make it match. Find out why it is different. What does it mean if your row count after the duplicates is the same as before?')))

    # ---- 28 error cards
    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[['ValueError: Unable to parse string', 'Text is left in the price, so to_numeric cannot read it.', 'Remove UGX and the comma first, then convert.'],
                        ['Dates still missing after the fill', 'A format string does not match the text.', 'Match each format to its separator: dash or slash.'],
                        ['AttributeError: Can only use .str accessor', 'The column is already a number or a date.', 'Run each string method before the conversion.'],
                        ['Row count drops by about ten thousand', 'dropna was called with no settings.', 'Use dropna with subset set to the column qty.'],
                        ['Your net total is a little different', 'A step ran twice, or the returns were removed.', 'Restart and run all cells from the top. Keep the returns.']],
                  widths=[3.9, 4.1, 4.0], icons=['cross', 'cross', 'cross', 'cross', 'cross'],
                  notes=('Five likely mistakes. A value error that says unable to parse string means some text is still in the price, so remove the letters and the comma first. Dates still missing after the fill means a format string does not match the text, so match each format to its separator. '
                         'An attribute error about the dot str accessor means the column is already numbers or dates, so run string methods before converting. A row count that falls by about ten thousand means dropna was called with no settings. '
                         'And a total that is slightly different usually means a step ran twice, so restart and run all cells from the top. Read the last line of the message first.')))

    # ---- 29 exit check
    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[['Why should you flag a blank before you fill it?', 'The flag is an indicator variable that remembers which values were filled. After filling, you can no longer tell.'],
                        ['The IQR rule flags 25 of 8,000 loan ages. Do you delete them?', 'No. A flag is a question. Only the impossible ages, 0 and 199, are errors. The rest are real borrowers.'],
                        ['Your cleaned total is 132,690 below the control total. What do you write?', 'The reconciliation difference is 132,690 UGX. Likely cause: the 12 dropped lines with a blank qty, about 2 units each. It is an estimate, because the true quantities are not in the file.']],
                  widths=[5.4, 6.6], icons=['flag', 'magnifier', 'calculator'],
                  notes=('Last, the exit check. Three questions. Write your answers before you look at mine. One, why should you flag a blank before you fill it? '
                         'Two, the interquartile range rule flags twenty five of eight thousand loan ages. Do you delete them? '
                         'Three, your cleaned total is one hundred and thirty two thousand six hundred and ninety below the control total. What do you write? '
                         'The short answers are on the slide. If you got all three, you are ready for session nine. If one surprised you, read that part of your log again tonight.')))

    # ------------------------------------------------------------------ facilitator
    sess['facilitator'] = dict(
        prep=['Open the deck and the Session 8 notebook in Colab before anyone arrives. Run the solution once to confirm the data upload step works on your laptop.',
              'Check that data.zip includes orders_raw.csv and products.csv. Learners do not need answer_key.json. It holds the control total, and it names the same gap with the field residual_ugx. In this course the gap is called the reconciliation difference, so use that name in the room.',
              'Write the check table (slide 27 of the deck) on the board before the lab.',
              'Explain that this is Project milestone 1: a practical deliverable that each learner shows you for feedback. It is never scored. Learners may ask questions, but the reconciliation note must be in their own words.',
              'Concepts run with laptops closed. Ask learners to open the notebook only after the Part 2 divider.'],
        misconceptions=[('dropna() is the safe way to remove blanks', f'It deletes any line with any blank. On this file it removes {n(F["n_dropna_lost"])} lines. Name the column with subset.'),
                        ('errors coerce is a good way to make a conversion work', 'It silently turns every bad value into NaN. Clean the text first, convert, then count the NaN.'),
                        ('A date that converts without error is a correct date', 'Day and month can be swapped with no error. Learn the format from the data owner and check the range.'),
                        ('An outlier should be deleted', 'The IQR rule flags values to investigate. Real extreme values and returns are kept.'),
                        ('The reconciliation difference is the same as a residual', 'A residual is a model quantity (actual minus predicted). The gap between two totals is a reconciliation difference.')],
        probes=[('Why do we copy raw before cleaning?', 'So the original is never lost and every change can be repeated and checked.'),
                ('Which defect raises no error when done wrong?', 'The date format: day/month read as month/day.'),
                ('Why does read_csv show NaN for N/A and NULL?', 'By default read_csv treats those strings as missing values.'),
                ('What does a log row with equal rows before and after tell you?', 'The step changed values but removed no rows.'),
                ('Why not impute the 12 blank quantities?', 'An invented quantity changes revenue, which is the number we are trying to prove.'),
                ('What is the reconciliation difference here and why?', f'{n(F["diff"])} UGX, most likely from the {F["n_lost"]} dropped lines with a blank quantity (an estimate).')],
        lab_steps=[('Step 1: load, copy, log', f'raw shape ({n(R)}, {F["raw_cols"]}); df is a copy; note() adds a log row.'),
                   ('Step 2: duplicates', f'{F["n_dupes"]} removed, {n(F["rows_dedup"])} rows, line_id unique.'),
                   ('Step 3: prices and dates', f'{F["price_dtype"]}; no missing dates; range {F["date_min"]} to {F["date_max"]}.'),
                   ('Step 4: text', f'{F["branch_n"]} branches, {F["pay_n"]} payment methods.'),
                   ('Step 5: blanks', f'{n(F["n_flag"])} flagged, {n(F["n_walkin"])} walk-in, {F["n_lost"]} lines dropped, {n(F["rows_clean"])} rows left.'),
                   ('Step 6: outliers', f'No price differs from the price list; {n(F["n_returns"])} returns kept; the IQR rule on line revenue flags {n(F["n_rev_hi"])} high and {n(F["n_rev_lo"])} low lines, all kept.'),
                   ('Step 7: reconcile', f'Cleaned total {n(F["net"])}; reconciliation difference {n(F["diff"])}.'),
                   ('Step 8: save', f'orders_clean.csv with {n(F["rows_clean"])} rows and cleaning_log.csv with {len(log)} rows.')],
        rescue=['If concepts run over, shorten the string methods slides and the IQR formula slide; the lab covers both.',
                'If only 30 minutes of lab remain, do steps 1, 2, 3, 5 and 7 and set the rest as homework before Session 9.',
                'If a learner falls behind, give them the solution for the step they are stuck on and let them continue.',
                'If a learner has no laptop, pair them with a neighbour: one types, one predicts aloud.'],
        after=['Review Project milestone 1 with each learner and give feedback: all checks say OK, the log has 7 rows, the reconciliation note names the difference and its likely cause.', 'Share the notebook and this deck again for learners who were absent.', 'Note any question you could not answer and open the next session with it.'],
        lab_answer_key=[['Step 2 PREDICT: how many duplicate lines?', f'{F["n_dupes"]}, leaving {n(F["rows_dedup"])} lines.'],
                        ['Step 3 READ: what does coerce do on the unit_price column?', f'It turns the {n(F["n_price_coerce_nan"])} text prices into NaN without a warning.'],
                        ['Step 3 CHANGE: read the dates month first.', f'{n(F["n_wrong_month"])} slash dates get the wrong month and {n(F["n_wrong_nat"])} become NaT.'],
                        ['Step 5 PREDICT: what happens if you call dropna() on the whole table?', f'About {F["dropna_share"]:.0f} percent of the lines vanish: {n(F["n_dropna_lost"])} lines.'],
                        ['Step 6 READ: are the IQR flags errors?', 'No. They are real lines. Check against the price list and the returns, then keep them.'],
                        ['Step 7 READ: what explains the reconciliation difference?', f'The likely cause is the {F["n_lost"]} dropped lines with a blank quantity: about {F["units_each"]:.1f} units each. This is an estimate, not proof.']])
    return sess
