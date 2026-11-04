"""Session 3: Summarising and showing data fairly (mean, median, mode, quartiles, IQR, standard deviation, skewness, histogram and box plot, pivot tables as GROUP BY,
chart choice, misleading axes). Sheets lab, no notebook.

Every number on a slide, in a note or in sheet_tasks is computed in facts() with pandas from the real Lakeside Mart workbook (lakeside_for_sheets.xlsx) and the other course files.
"""
from functools import lru_cache

import numpy as np
import pandas as pd

import b_facts as BF
from b_facts import n, s


@lru_cache(maxsize=None)
def facts():
    B = BF.base()
    T = B['T']
    o, w = T['orders'], T['branch_weeks']
    v = o.order_value_ugx
    F = dict(B=B)
    # histogram of order value, 5,000 UGX bins up to 150,000
    F['edges'], F['counts'], F['above150'] = BF.hist(v, 0, 150000, 5000)
    F['mode_bin'] = int(np.argmax(F['counts']))
    # the five orders for the by-hand standard deviation (rows 2 to 6 of the orders tab)
    five = v.iloc[:5].astype(float)
    F['five'] = [int(x) for x in five]
    F['five_mean'] = float(five.mean())
    F['five_dev'] = [float(x - five.mean()) for x in five]
    F['five_sq'] = [d * d for d in F['five_dev']]
    F['five_ss'] = float(sum(F['five_sq']))
    F['five_var'] = F['five_ss'] / 4
    F['five_sd'] = float(np.sqrt(F['five_var']))
    assert abs(F['five_sd'] - five.std()) < 1e-6
    # without the largest order
    v2 = v.drop(v.idxmax())
    F['iqr_wo_max'] = float(v2.quantile(0.75) - v2.quantile(0.25))
    F['sd_shift'] = B['sd'] - B['sd_wo_max']
    F['iqr_shift'] = B['iqr'] - F['iqr_wo_max']
    jo = o[o.branch_id == 'B04'].order_value_ugx
    F['jinja_mean'], F['jinja_wo'], F['jinja_median'] = float(jo.mean()), float(jo.drop(jo.idxmax()).mean()), float(jo.median())
    F['jinja_delta'] = F['jinja_mean'] - F['jinja_wo']
    # skewness panels
    loans = pd.read_csv(BF.DATA / 'loans.csv')
    age = loans.age[(loans.age >= 18) & (loans.age <= 80)]
    F['age_n'], F['age_skew'], F['age_mean'], F['age_median'] = len(age), float(age.skew()), float(age.mean()), float(age.median())
    F['age_edges'], F['age_counts'], _ = BF.hist(age, 15, 75, 3)
    F['loans_bad_ages'] = len(loans) - len(age)
    # pivot results
    br = B['by_branch']
    F['branch_rows'] = [[k, n(r['count']), n(r['sum']), n(r['median'])] for k, r in br.iterrows()]
    F['medians'] = [float(x) for x in br['median']]
    F['med_min_id'], F['med_max_id'] = br['median'].idxmin(), br['median'].idxmax()
    F['med_min'], F['med_max'] = float(br['median'].min()), float(br['median'].max())
    F['trunc_ratio'] = (F['med_max'] - 20000) / (F['med_min'] - 20000)
    F['true_ratio'] = F['med_max'] / F['med_min']
    # pivot: branch x month
    o2 = o.assign(month=o.order_date.str[:7])
    piv = o2.pivot_table(index='branch_id', columns='month', values='order_value_ugx', aggfunc='sum')
    F['piv'] = piv
    F['b01_jan'], F['b04_mar'], F['b07_jan'] = int(piv.loc['B01', '2024-01']), int(piv.loc['B04', '2024-03']), int(piv.loc['B07', '2024-01'])
    F['dec24_total'] = int(piv['2024-12'].sum())
    F['grand'] = int(piv.sum().sum())
    assert F['grand'] == B['sum']
    m = B['months']
    F['month_vals'] = [int(x) for x in m['sum']]
    F['month_names'] = list(m.index)
    F['best_month'], F['worst_month'] = m['sum'].idxmax(), m['sum'].idxmin()
    F['best_val'], F['worst_val'] = int(m['sum'].max()), int(m['sum'].min())
    F['dec24'] = int(m.loc['2024-12', 'sum'])
    F['dec24_rank'] = int((m['sum'] > F['dec24']).sum()) + 1
    F['dec24_orders'] = int(m.loc['2024-12', 'count'])
    F['orders_per_month'] = len(o) / len(m)
    # mini charts
    F['scatter_pts'] = [[float(a), float(b)] for a, b in w[['footfall', 'orders']].iloc[::6].values]
    F['hist_small'] = BF.hist(v, 0, 150000, 10000)[1]
    return F


MONTH = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}


def mname(ym):
    return f'{MONTH[ym[5:]]} {ym[:4]}'


def build():
    F = facts()
    B = F['B']
    N = B['n_orders']
    names = B['branch_names']
    br = B['by_branch']
    sess = dict(
        num=3, block='Module A: Think with data', short_title='Summarising and showing data',
        title='Summarising and showing data fairly',
        question='How do we describe thousands of records in one sentence and one chart without misleading anyone?',
        outcomes=['Choose between the mean, median and mode, and say why, using quartiles, the IQR and the standard deviation',
                  'Read a histogram, a box plot and a line chart, and describe a distribution by its skewness',
                  'Build a pivot table (a GROUP BY) in Google Sheets, choose a chart for a question, and spot a misleading axis'],
        outcome_icons=['calculator', 'chart', 'grid'],
        outcome_note=('Here is what you can do by the end of today. You can choose between the mean, the median and the mode, and say why, using quartiles, the interquartile range and the standard deviation. '
                      'You can read a histogram, a box plot and a line chart, and describe the shape of data by its skewness. '
                      'And you can build a pivot table in Google Sheets, which is a GROUP BY, choose the right chart for a question, and spot a misleading axis. All of it is on the Lakeside Mart workbook, with no code.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: picture, plain words, one example by hand'), (10, 'Break'), (45, 'Lab: predict, compute, chart'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: concepts first, then a Google Sheets lab',
        plan_caption='Ideas with pictures first. Then you open the sheet. Then the checks and what you keep.',
        plan_note=('We have two hours. The first ten minutes bring back Session 2 and set the question for today. Then forty-five minutes of concepts, with no laptops open, so you can watch the pictures. '
                   'After a ten minute break we open the Lakeside Mart workbook in Google Sheets for a forty-five minute lab. You will predict each answer, compute it with a formula, and build a pivot table and charts. '
                   'The last ten minutes are an exit check and what you keep. The lab is where the learning sticks, so please protect that time.'),
        recall_from='Session 2',
        recall=[('Order O000003 has 2 products. How many records does it make in orders, and how many in order_lines?', 'One record in orders and 2 in order_lines. The two tabs have different granularity.'),
                ('Which variable is the primary key of products, and which tab holds it as a foreign key?', 'product_id. The order_lines tab holds product_id as a foreign key.'),
                (f'customer_id is blank on {n(B["walk_n"])} orders. What do you do first?', 'Read the data dictionary: the blank means a walk-in. Keep the records and add a flag, instead of deleting or filling them.')],
        words=[('Mean, median and mode', 'Three ways to say what is typical. The mean is the sum divided by the count. The median is the middle value. The mode is the most common value.'),
               ('Quartiles and IQR', 'Quartiles cut sorted values into four equal groups. The interquartile range (IQR) is Q3 minus Q1: the spread of the middle half.'),
               ('Standard deviation', 'A typical distance from the mean: the square root of the average squared distance (n minus 1 for a sample).'),
               ('Skewness', 'How lopsided a distribution is. Right-skewed means a long tail of large values on the right.'),
               ('Pivot table (GROUP BY)', 'A table that groups records and summarises each group with an aggregation such as SUM, COUNT or AVERAGE (MEDIAN in Sheets and pandas). In SQL and pandas it is GROUP BY.')],
        word_icons=['calculator', 'bars', 'chart', 'flag', 'grid'],
        words_note=('Five words for today, and most of them live in the spreadsheet you already know. Mean, median and mode are three ways to say what is typical. Quartiles cut sorted values into four equal groups, and the interquartile range is the spread of the middle half. '
                    'Standard deviation is a typical distance from the mean. Skewness says how lopsided the shape is. And a pivot table groups records and summarises each group, which SQL and pandas call GROUP BY. '
                    'We use every one of them before the end of the session.'),
        keep='Keep your workbook with three pivot tables, three charts you could show a manager, and two sentences that describe the typical order and the branches.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab file', value='A workbook with pivots and charts'), dict(label='Your finding', value='Two sentences for a manager'), dict(label='Next session', value='Uncertainty, samples and cause')]),
        keep_title='Save your workbook with its pivot tables and charts',
        next='Session 4: Uncertainty, samples and cause. We ask how far a sample can sit from the truth, and when a pattern means that one thing caused another.', next_label='Next session',
        keep_note=('Before you go, save your workbook with the three pivot tables and the charts. Those are your keepsake from today, together with two sentences you could hand to a manager: one on the typical order and one on whether the branches differ. '
                   'Check that each chart has a title, labelled axes with units, and a bar axis that starts at zero. Next session we ask a harder question about numbers like these: how much can they move just because of which records we looked at? '
                   'If anything was unclear today, write the question down and bring it.'),
        cover_note=('Welcome back. Last session we learned what one record of a table stands for and how tables link. Today we describe thousands of records with a few numbers and one chart. '
                    'You will meet a finding that surprises almost everyone: in the Lakeside workbook the mean order is twice the typical order. We will learn why, how to choose the right summary, and how a chart can mislead. '
                    'Everything is done in Google Sheets, with no code.'),
        use_at_work='Report a typical value with the median and the spread, build a pivot table, and choose a chart that is fair.',
        slides=[])
    S = sess['slides']

    # ------------------------------------------------------------------ 1 answers
    S.append(dict(kind='table', title='Answers to the three questions from Session 2', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in sess['recall']], widths=[5.2, 6.8], icons=['receipt', 'key', 'person'],
                  notes=(f'Here are the answers to the three warm-up questions. An order with two products makes one record in orders and two in order lines, because the two tabs have different granularity. '
                         f'The primary key of products is product id, and the order lines tab holds it as a foreign key. '
                         f'And a blank customer id on {n(B["walk_n"])} orders means a walk-in shopper, so you read the data dictionary first and keep the records. Today every number we compute counts or adds those records. Which of the three did you find hardest?')))

    # ------------------------------------------------------------------ 2 six summary jobs
    S.append(dict(kind='table', title='Seven summary jobs on order_value_ugx, each one formula in Sheets',
                  headers=['Statistic', 'Sheets formula', 'Result'],
                  rows=[['Count', '=COUNT(orders!G2:G2001)', n(N)], ['Sum', '=SUM(orders!G2:G2001)', n(B['sum'])], ['Mean', '=AVERAGE(orders!G2:G2001)', f'{B["mean"]:,.2f}'],
                        ['Median', '=MEDIAN(orders!G2:G2001)', n(B['median'])], ['Mode', '=MODE(orders!G2:G2001)', f'{n(B["mode"])} ({B["mode_count"]} orders)'],
                        ['Minimum', '=MIN(orders!G2:G2001)', n(B['min'])], ['Maximum', '=MAX(orders!G2:G2001)', n(B['max'])]],
                  widths=[2.6, 5.4, 4.0], icons=['calculator', 'coin', 'bars', 'pin', 'tag', 'clock', 'flag'], note='All amounts are in UGX. Column G of the orders tab holds order_value_ugx.',
                  notes=(f'Open the workbook. Column G of the orders tab holds the value of each order in shillings. Seven formulas summarise it. Count gives {n(N)} orders. Sum gives {n(B["sum"])} shillings. '
                         f'The mean is the sum divided by the count, {B["mean"]:,.0f}. The median is the middle value after sorting, {n(B["median"])}. The mode is the most common value, {n(B["mode"])} shillings, which appears {B["mode_count"]} times. '
                         f'The smallest order is {n(B["min"])} and the largest is {n(B["max"])}. Notice that the mean is about double the median. That gap is today\'s main story. Why do you think it happens?')))

    # ------------------------------------------------------------------ 3 sample against full file
    S.append(dict(kind='compare', title='The workbook is a sample of the full file, so its figures are close but not identical',
                  left=dict(head=f'Workbook: {n(N)} orders', icon='doc', points=[f'Mean {n(B["mean"])} UGX', f'Median {n(B["median"])} UGX', f'Mean is {B["ratio"]:.2f} times the median']),
                  right=dict(head=f'Full file: {n(B["full_n"])} orders', icon='folder', points=[f'Mean {n(B["full_mean"])} UGX', f'Median {n(B["full_median"])} UGX', f'Mean is {B["full_ratio"]:.2f} times the median']),
                  verdict='The story is the same. Session 4 explains why the figures differ.',
                  notes=(f'The workbook has only {n(N)} orders. It is a sample, a slice drawn from the full Lakeside Mart file of {n(B["full_n"])} orders. On the left are the workbook figures: mean {n(B["mean"])} shillings and median {n(B["median"])}. '
                         f'On the right are the full file figures: mean {n(B["full_mean"])} and median {n(B["full_median"])}. So your answers in Sheets are close to the full file and never match it exactly. '
                         f'In both, the mean is more than double the median. The finding is the same either way. Session 4 is all about why a sample differs from the whole. Which figure would you quote to your manager?')))

    # ------------------------------------------------------------------ 4 histogram
    hist = dict(kind='dsb_hist', edges=F['edges'], counts=F['counts'], hl=[F['mode_bin']],
                lines=[dict(x=B['mode'], label=f'mode {n(B["mode"])}', color='#E0BE36', tcolor='#111111'), dict(x=B['median'], label=f'median {n(B["median"])}', color='#111111'), dict(x=B['mean'], label=f'mean {n(B["mean"])}', color='#AE2525')],
                xticks=[(0, '0'), (50000, '50,000'), (100000, '100,000'), (150000, '150,000')], xlabel='order value (UGX), bars 5,000 UGX wide', ylabel='number of orders',
                ymax=max(F['counts']), note=[f'{F["above150"]} orders above 150,000', 'are not shown'])
    S.append(dict(kind='wide', title='A histogram shows the distribution, and a few large orders pull the mean above the median', visual=hist,
                  caption='Each bar counts the orders in a band. The gold bar holds the mode. The largest order is off the edge.',
                  notes=(f'This is a histogram. It is a chart that counts how many records fall into each band of equal width. Each bar here is a band of 5,000 shillings of order value, and its height is the number of orders in it. '
                         f'Start on the left. Most orders are small, and the tallest bar, in gold, is the mode band. Then follow the bars to the right. They get shorter, and a long thin tail runs out of the picture. '
                         f'The black line is the median, {n(B["median"])}. The red line is the mean, {n(B["mean"])}. The few large orders drag the mean to the right. A manager asks what a typical order is worth. Which line do you give?')))

    # ------------------------------------------------------------------ 5 mean formula
    S.append(dict(kind='formula', title='The mean is the sum of the values divided by how many there are',
                  formulas=[('Mean', r'$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i = \frac{99{,}861{,}360}{2{,}000} = 49{,}930.68$')],
                  symbols=[['x-bar', 'The mean (arithmetic mean)', f'{B["mean"]:,.2f} UGX'], ['n', 'The number of records', n(N)], ['x_i', 'The value of record i', 'order_value_ugx of one order'], ['Σ (sigma)', 'Add up the values from i = 1 to n', f'Sum = {n(B["sum"])}']],
                  note='In Sheets: =AVERAGE(orders!G2:G2001). The median is the middle value after sorting.',
                  notes=(f'Here is the mean as a formula. X-bar is the mean. Add up all n values, which the sigma sign means, and divide by n. In our data the sum of order values is {n(B["sum"])} and n is {n(N)}, so the mean is {B["mean"]:,.2f} shillings. '
                         'In Sheets that is the function AVERAGE. You have done this all your working life. What is new is the median. The median is the middle value after sorting, so it depends on position and not on how large the largest values are. '
                         'Which of the two do you think a few huge orders move?')))

    # ------------------------------------------------------------------ 6 mean against median
    S.append(dict(kind='compare', title='One huge order moves the mean but not the median',
                  left=dict(head='Mean', icon='bars', points=[f'All orders: {n(B["mean"])} UGX', f'Without the largest: {n(B["mean_wo_max"])} UGX', f'It moved by about {n(B["mean_shift"])} UGX ({B["mean"]:,.2f} to {B["mean_wo_max"]:,.2f})']),
                  right=dict(head='Median', icon='pin', points=[f'All orders: {n(B["median"])} UGX', f'Without the largest: {n(B["median_wo_max"])} UGX', 'It did not move at all']),
                  verdict='For money amounts, give the median beside the mean, and say how many records you counted.',
                  notes=(f'Take away the largest order in the workbook, {n(B["max"])} shillings at Jinja. The mean drops from {n(B["mean"])} to {n(B["mean_wo_max"])}, a move of {n(B["mean_shift"])} shillings. The median stays at {n(B["median"])}. '
                         'The median ignores how large the large values are. It only cares about their position in the sorted line. A statistic that barely moves when one extreme value changes is called resistant, or robust. '
                         f'So here is the trap. If you report that a typical order is about {n(round(B["mean"], -3))} shillings, the formula is right but the sentence misleads, because half of all orders are under {n(B["median"])}. Which would you lead with?')))

    # ------------------------------------------------------------------ 7 box plot
    ticks = [(0, '0'), (25000, '25,000'), (50000, '50,000'), (75000, '75,000'), (100000, '100,000'), (125000, '125,000'), (150000, '150,000')]
    out_pts = [float(x) for x in B['T']['orders'].order_value_ugx[(B['T']['orders'].order_value_ugx > B['fence_hi']) & (B['T']['orders'].order_value_ugx <= 150000)].iloc[::2]]
    box = dict(kind='dsb_box', q1=B['q1'], med=B['median'], q3=B['q3'], whisker_lo=B['whisker_lo'], whisker_hi=B['whisker_hi'], fence=B['fence_hi'], fence_label=f'fence {n(B["fence_hi"])}', outliers=out_pts, axis_max=150000, ticks=ticks,
               xlabel='order value (UGX)', off=f'{n(B["n_out"])} outliers; the largest is {n(B["max"])}',
               labels=[dict(x=B['q1'], text=f'Q1 {B["q1"]:,.1f}', side='below', level=0, ha='right'), dict(x=B['median'], text=f'median {n(B["median"])}', side='above', level=0),
                       dict(x=B['q3'], text=f'Q3 {B["q3"]:,.1f}', side='below', level=0, ha='left'), dict(x=B['whisker_lo'], text=f'minimum {n(B["min"])}', side='above', level=1, ha='left')])
    S.append(dict(kind='wide', title='A box plot shows the quartiles: the box holds the middle half of the orders', visual=box,
                  caption=f'IQR = Q3 minus Q1 = {n(B["iqr"])} UGX. Beyond Q3 + 1.5 × IQR, the dots are outliers by the IQR rule.',
                  notes=(f'A box plot draws the quartiles. Quartiles are three cut points that split the sorted orders into four equal groups. The first quartile, Q1, is {B["q1"]:,.1f}. The median, which is the second quartile, is {n(B["median"])}. The third quartile, Q3, is {B["q3"]:,.1f}. '
                         f'The gold box runs from Q1 to Q3, so it holds the middle half of the orders. Its length is the interquartile range, the IQR: Q3 minus Q1, which is {n(B["iqr"])}. '
                         f'The IQR rule calls a value an outlier when it lies beyond Q3 plus one and a half times the IQR, here {n(B["fence_hi"])}. {n(B["n_out"])} orders, {B["n_out_pct"] * 100:.1f} percent, lie beyond it. Why might a retail shop have such orders?')))

    # ------------------------------------------------------------------ 8 five-number summary in Sheets
    S.append(dict(kind='table', title='The five-number summary and the outlier fence, each one formula in Sheets',
                  headers=['What you want', 'Sheets formula', 'Result'],
                  rows=[['Minimum', '=MIN(orders!G2:G2001)', n(B['min'])], ['First quartile, Q1', '=QUARTILE(orders!G2:G2001,1)', f'{B["q1"]:,.1f}'], ['Median, Q2', '=MEDIAN(orders!G2:G2001)', n(B['median'])],
                        ['Third quartile, Q3', '=QUARTILE(orders!G2:G2001,3)', f'{B["q3"]:,.1f}'], ['Maximum', '=MAX(orders!G2:G2001)', n(B['max'])],
                        ['IQR', 'Q3 minus Q1', n(B['iqr'])], ['Orders beyond the fence', '=COUNTIF(orders!G2:G2001,">107925")', n(B['n_out'])]],
                  widths=[3.4, 5.4, 3.2], icons=['clock', 'bars', 'pin', 'bars', 'flag', 'calculator', 'cross'], note=f'The fence is Q3 + 1.5 × IQR = {B["q3"]:,.1f} + 1.5 × {B["iqr"]:,.1f} = {B["fence_hi"]:,.1f}. The fence is exactly 107,925, so the formula uses 107925. A percentile such as the 90th is =PERCENTILE(range,0.9).',
                  notes=(f'Here are the formulas. QUARTILE of the range with a one gives Q1, and with a three gives Q3. The IQR is the difference. The fence is Q3 plus one and a half times the IQR, which is {B["fence_hi"]:,.1f}. '
                         f'COUNTIF with greater than 107925 counts the orders beyond it: {n(B["n_out"])}. Sheets QUARTILE equals QUARTILE.INC and the pandas default, which interpolate between values, so the two agree here. '
                         'QUARTILE.EXC and some textbooks use other rules and give slightly different quartiles. A percentile such as the ninetieth is PERCENTILE of the range with 0.9. What would you do with the orders beyond the fence?')))

    # ------------------------------------------------------------------ 9 standard deviation formula
    S.append(dict(kind='formula', title='The standard deviation is a typical distance of the values from the mean',
                  formulas=[('Sample standard deviation', r'$s = \sqrt{\frac{1}{n-1}\sum_{i=1}^{n}\left(x_i - \bar{x}\right)^2}$')],
                  symbols=[['s', 'The sample standard deviation: root of the average squared distance, n − 1 for a sample. Its square is the variance.', f'{B["sd"]:,.0f} UGX'], ['x_i − x-bar', 'How far record i sits from the mean (a deviation)', 'One order minus 49,930.68'],
                           ['(…)²', 'Square each deviation, so negatives do not cancel', 'Units are UGX squared'], ['n − 1', 'The count minus one (ddof=1 in pandas)', f'{n(N - 1)}']],
                  note='In Sheets: =STDEV(orders!G2:G2001). For a whole population, =STDEV.P divides by n instead.',
                  notes=('Here is the standard deviation. For each record, find its deviation, which is its distance from the mean. Square each deviation so that negatives do not cancel the positives. '
                         'Add the squares, divide by n minus one, and take the square root to get back to shillings. The result, s, is the sample standard deviation, and its square is the variance. '
                         f'For the order values, s is about {n(B["sd"])} shillings. That is larger than the mean itself, which tells you the values are very spread out. In Sheets the function is STDEV. Why do you think we take a square root at the end?')))

    # ------------------------------------------------------------------ 10 by hand
    fm = F['five_mean']
    S.append(dict(kind='table', title='One example by hand: the standard deviation of five orders',
                  headers=['Order value x (UGX)', 'Deviation x − mean', 'Squared deviation'],
                  rows=[[n(x), f'{d:,.0f}', f'{q:,.0f}'] for x, d, q in zip(F['five'], F['five_dev'], F['five_sq'])] + [['Mean ' + n(fm), 'Sum 0', f'Sum {F["five_ss"]:,.0f}']],
                  widths=[4.0, 4.0, 4.0], icons=['receipt'] * 5 + ['calculator'],
                  note=f'Variance = {F["five_ss"]:,.0f} ÷ 4 = {F["five_var"]:,.0f}. Standard deviation = square root = {F["five_sd"]:,.0f} UGX. These are the first five orders in the orders tab.',
                  notes=(f'Let us do it by hand on five orders, the first five in the orders tab. Their mean is {n(fm)}. Subtract the mean from each value to get the deviations. They add up to zero, which is why we square them. '
                         f'The squares add up to {F["five_ss"]:,.0f}. Divide by n minus one, which is four, to get the variance, {F["five_var"]:,.0f}. The square root is the standard deviation, {F["five_sd"]:,.0f} shillings. '
                         f'Check it in Sheets: STDEV of G2 to G6 gives the same. Compare that with the standard deviation of all {n(N)} orders, {n(B["sd"])}. Why is it so much larger for the whole file?')))

    # ------------------------------------------------------------------ 11 SD against IQR
    S.append(dict(kind='table', title=f'One large order moves the standard deviation by {n(F["sd_shift"])} UGX and the IQR by {n(F["iqr_shift"])}',
                  headers=['Measure', f'All {n(N)} orders', 'Without the largest order'],
                  rows=[['Mean', n(B['mean']), n(B['mean_wo_max'])], ['Median', n(B['median']), n(B['median_wo_max'])], ['Standard deviation', n(B['sd']), n(B['sd_wo_max'])], ['IQR', n(B['iqr']), n(F['iqr_wo_max'])]],
                  widths=[4.0, 4.0, 4.0], icons=['bars', 'pin', 'chart', 'calculator'], note='All amounts are in UGX. The mean and the standard deviation react to extreme values. The median and the IQR resist them.',
                  notes=(f'Here is the same comparison for the spread. With the largest order removed, the standard deviation falls from {n(B["sd"])} to {n(B["sd_wo_max"])}, a drop of {n(F["sd_shift"])}. '
                         f'The IQR moves from {n(B["iqr"])} to {n(F["iqr_wo_max"])}, a change of only {n(F["iqr_shift"])}. The mean and the standard deviation both use every value, so extreme values pull on them. '
                         'The median and the IQR use positions in the sorted list, so they resist. A common pair to report is the mean with the standard deviation when data is roughly symmetric, and the median with the IQR when it is skewed. Which pair fits order values?')))

    # ------------------------------------------------------------------ 12 skewness
    ageb = F['age_edges']
    bm = B['mean']
    panels = [dict(title='Right-skewed', edges=F['edges'], counts=F['counts'], xticks=[(0, '0'), (50000, '50'), (100000, '100'), (150000, '150')], xlabel='order value (thousand UGX)', ymax=max(F['counts']),
                   lines=[dict(x=B['median'], label='median', color='#111111'), dict(x=bm, label='mean', color='#AE2525')], note=[f'skewness {B["skew"]:.2f}']),
              dict(title='Roughly symmetric', edges=ageb, counts=F['age_counts'], xticks=[(20, '20'), (35, '35'), (50, '50'), (65, '65')], xlabel='borrower age (years)', ymax=max(F['age_counts']),
                   lines=[dict(x=F['age_median'], label='median = mean', color='#111111')], note=[f'skewness {F["age_skew"]:.2f}']),
              dict(title='Left-skewed (mirror image)', edges=F['edges'], counts=F['counts'][::-1], xticks=[(0, '0'), (50000, '50'), (100000, '100'), (150000, '150')], xlabel='hypothetical: order values mirrored', ymax=max(F['counts']),
                   lines=[dict(x=150000 - bm, label='mean', color='#AE2525'), dict(x=150000 - B['median'], label='median', color='#111111')], note=[f'skewness {-B["skew"]:.2f}'], note_left=True)]
    S.append(dict(kind='wide', title='Skewness describes the shape: a long tail on one side pulls the mean towards it', visual=dict(kind='dsb_panels', panels=panels),
                  caption=f'Left: order values. Middle: ages of {n(F["age_n"])} borrowers. Right: the left picture reversed (hypothetical).',
                  notes=(f'Skewness describes the shape of a distribution. The left picture is right-skewed: a long tail of large values on the right, and the mean, in red, sits to the right of the median. The skewness number for order values is {B["skew"]:.2f}, a large positive number. '
                         f'The middle picture shows ages of {n(F["age_n"])} borrowers in the fictional Nile Microfinance file, after removing {F["loans_bad_ages"]} impossible ages. It is roughly symmetric, a bell shape, with the mean and median together and a skewness near zero. '
                         'The right picture is the first one reversed. It is hypothetical, and it shows a left-skewed shape, with the mean to the left of the median. Which shape do you expect for incomes in your district?')))

    # ------------------------------------------------------------------ 13 group by figure
    res_rows = [[k, n(r['count']), n(r['sum']), n(r['median'])] for k, r in br.iterrows()]
    recs = [[s(r.order_id), s(r.branch_id), n(r.order_value_ugx)] for r in B['T']['orders'].iloc[[0, 1, 400, 401]].itertuples()]
    S.append(dict(kind='wide', title='A pivot table is a GROUP BY: it groups the records and summarises each group',
                  visual=dict(kind='dsb_groupby', records=recs, rec_headers=['order_id', 'branch_id', 'order_value_ugx'], more=f'… {n(N - 4)} more records', result=res_rows, res_headers=['branch_id', 'orders', 'sum (UGX)', 'median (UGX)'],
                              op='Aggregation: COUNT, SUM, MEDIAN'),
                  caption='Each group is one branch. An aggregation turns many records into one number.',
                  notes=(f'A pivot table groups records and summarises each group. On the left are four records from the orders tab, each with a branch id. The arrow says group by branch id. On the right is the result: one record for each of the eight branches. '
                         f'For each group we computed an aggregation, which is an aggregate function such as COUNT, SUM or MEDIAN. Branch B01 has {n(br.loc["B01", "count"])} orders with a median of {n(br.loc["B01", "median"])}. '
                         'In SQL and pandas the same step is called GROUP BY and groupby, so learning the pivot table now teaches you both. What other grouping would help your manager, by month or by payment method?')))

    # ------------------------------------------------------------------ 14 same question in three tools
    S.append(dict(kind='table', title='The same GROUP BY question in three tools',
                  headers=['Tool', 'How you write it', 'What it returns'],
                  rows=[['Google Sheets', 'Insert, Pivot table. Rows: branch_id. Values: SUM of order_value_ugx', 'One row for each branch'],
                        ['SQL', 'SELECT branch_id, SUM(order_value_ugx) FROM orders GROUP BY branch_id', 'The same, from a database'],
                        ['pandas', "orders.groupby('branch_id').order_value_ugx.sum()", 'The same, in Python']],
                  widths=[1.9, 7.6, 2.6], icons=['grid', 'folder', 'laptop'], note='The result is the same in every tool. We meet SQL in Session 10 and pandas groupby in Session 9.',
                  notes=('Here is the same question in three tools. In Sheets you insert a pivot table, put branch id in the rows, and sum order value. In SQL you write SELECT, the branch, the sum of the value, FROM orders, GROUP BY branch. '
                         'In pandas you call groupby on the branch column and then sum. The result is one row per branch in all three. Once you can read a pivot table, the SQL and the pandas are just different spellings of it. '
                         'We meet SQL in Session 10 and pandas groupby in Session 9. Which of these three would your employer expect you to know?')))

    # ------------------------------------------------------------------ 15 branch table
    S.append(dict(kind='table', title=f'{names["B04"]} leads on the mean and the median, but the medians of all eight branches are close',
                  headers=['Branch', 'Orders', 'Mean (UGX)', 'Median (UGX)'],
                  rows=[[f'{k} {names[k]}', n(r['count']), n(r['mean']), n(r['median'])] for k, r in br.iterrows()],
                  widths=[4.2, 2.2, 2.8, 2.8], icons=['shop'] * 8, note=f'Medians run from {n(F["med_min"])} to {n(F["med_max"])} UGX. Without its largest order ({n(B["max"])} UGX), {names["B04"]}\'s mean falls from {n(F["jinja_mean"])} to {n(F["jinja_wo"])} and {names["B04"]} still leads.',
                  notes=(f'This is the pivot result with the mean and the median for each branch. Jinja has the highest mean order, {n(br.loc["B04", "mean"])} shillings. One order of {n(B["max"])} adds about {n(round(F["jinja_delta"], -2))} to it, and Jinja still leads without it. '
                         f'The medians tell a calmer story. They run from {n(F["med_min"])} at {names[F["med_min_id"]]} to {n(F["med_max"])} at {names[F["med_max_id"]]}. So the typical order is similar everywhere. '
                         'A group summary needs the count and a resistant measure beside the mean. Would you have spotted this from the totals alone?')))

    # ------------------------------------------------------------------ 16 chart choice
    S.append(dict(kind='wide', title='Choose the chart from the question you are asking',
                  visual=dict(kind='dsb_charts', bars=dict(values=F['medians'], labels=list(br.index), hl=[int(np.argmax(F['medians']))]), line=dict(values=F['month_vals']), hist=dict(counts=F['hist_small']), scatter=dict(points=F['scatter_pts']),
                              captions=[('Compare groups', 'Bar chart: median order for each branch'), ('Change over time', 'Line chart: sales for each month'), ('Shape of one variable', 'Histogram or box plot: order value'), ('Two variables', 'Scatter plot: footfall and orders')]),
                  caption='Real Lakeside data in every panel. Avoid pie charts: people compare angles badly.',
                  notes=('Pick the chart from the question. To compare groups, use a bar chart: here the median order for each branch. To show change over time, use a line chart: sales for each month. '
                         'To show the shape of one variable, use a histogram or a box plot: the order values. To show how two variables go together, use a scatter plot: weekly footfall against weekly orders for the branches. '
                         'I suggest you avoid pie charts, because people compare angles and areas badly, and a bar chart always does the job better. Every panel here is drawn from the real workbook. Which question do you ask most at work?')))

    # ------------------------------------------------------------------ 17 line chart
    mv = F['month_vals']
    mx = max(mv)
    top = (int(mx / 2e6) + 1) * 2e6
    xt = [(i, mname(m)) for i, m in enumerate(F['month_names']) if i % 6 == 0]
    S.append(dict(kind='wide', title='A line chart shows change over time; start its axis at zero unless you say clearly that you did not',
                  visual=dict(kind='dsb_line', values=mv, xticks=xt, ylabel='sales (million UGX)', yticks=[(0, '0'), (2e6, '2'), (4e6, '4'), (top, f'{top / 1e6:.0f}')], hl=F['month_names'].index(F['best_month']), hl_label=f'{mname(F["best_month"])}: {n(F["best_val"])}'),
                  caption=f'Monthly total of order_value_ugx. About {F["orders_per_month"]:.0f} orders a month, so a few large orders can move a month.',
                  notes=(f'A line chart joins a value for each period, so the eye can follow the change. This one shows the monthly total of order values, January 2024 to December 2025. Its vertical axis starts at zero. '
                         f'The highest month is {mname(F["best_month"])}, at {n(F["best_val"])} shillings. The lowest is {mname(F["worst_month"])}, at {n(F["worst_val"])}. '
                         f'December 2024 is only number {F["dec24_rank"]} of 24, at {n(F["dec24"])}, so it does not stand out the way it does in the full file. The reason is that the sample has about {F["orders_per_month"]:.0f} orders a month, so a few large orders can reorder the months. '
                         'What would you want to know before telling anyone that December is the peak?')))

    # ------------------------------------------------------------------ 18 misleading axis
    S.append(dict(kind='wide', title=f'A truncated axis makes a {(F["true_ratio"] - 1) * 100:.0f} percent gap look {F["trunc_ratio"]:.1f} times taller',
                  visual=dict(kind='dsb_axis', values=F['medians'], labels=list(br.index), base=20000, ymax=30000, hl=[F['medians'].index(F['med_max'])],
                              left_note=f'{F["med_max_id"]} looks {F["trunc_ratio"]:.1f} times as tall as {F["med_min_id"]}.', right_note=f'{F["med_max_id"]} is {F["true_ratio"]:.2f} times {F["med_min_id"]}.'),
                  caption='The same eight branch medians of order value in UGX. A bar chart must start at zero.',
                  notes=(f'Here are the same eight branch medians on two charts. On the left the vertical axis starts at 20,000. {F["med_max_id"]}, in gold, rises {n(F["med_max"] - 20000)} above the base and {F["med_min_id"]} only {n(F["med_min"] - 20000)}, so {F["med_max_id"]} looks {F["trunc_ratio"]:.1f} times as tall. '
                         f'On the right the axis starts at zero. Now {F["med_max_id"]} is {F["true_ratio"]:.2f} times {F["med_min_id"]}, about {(F["true_ratio"] - 1) * 100:.0f} percent more. A bar encodes its value in its length, so cutting the base changes the message. '
                         'A line chart can sometimes zoom in fairly, but a bar chart should start at zero. Which of the two would your manager remember?')))

    # ------------------------------------------------------------------ 19 six checks
    S.append(dict(kind='list', title='Six checks before you show a chart',
                  items=['Does the title state the point?', 'Do the axes have labels and units, such as UGX?', 'Does a bar chart start at zero?', 'Is the chart type right for the question?', 'Does it say how many records it shows, and the source?', 'Would it still look fair to someone who disagrees with you?'],
                  icons=['flag', 'pen', 'bars', 'check', 'doc', 'people'],
                  notes=('Here is a short checklist to run before any chart leaves your desk. Does the title state the point? Do the axes have labels and units, such as UGX? Does a bar chart start at zero? '
                         'Is the chart type right for the question? Does it say how many records it shows, and where they came from? And the last one is the hardest: would the chart still look fair to someone who disagrees with you? '
                         'A chart that passes all six is hard to attack and easy to trust. Which of the six do you most often forget?')))

    # ------------------------------------------------------------------ 20 use at work
    S.append(dict(kind='table', title='Where you will use this at work: report the typical value and the spread beside the total',
                  headers=['Your job', 'The question', 'What today lets you do'],
                  rows=[['Branch manager at a retail chain, using Excel or Sheets', 'What does a typical customer spend?', 'Report the median order with the IQR and the number of orders.'],
                        ['Credit analyst at a bank, using SQL', 'How large is a typical loan in each district?', 'Write a GROUP BY with COUNT and AVG for each district, and take the median in pandas.'],
                        ['Health records officer at a district office, using pandas', 'Monthly visits for 12 districts', 'Report the median visits and the IQR for each district before you rank districts.'],
                        ['Programme officer at an NGO, handing over to Power BI', 'Which region gained most?', 'Pick a chart from the question, and start bar charts at zero.']],
                  widths=[3.8, 3.8, 4.4], icons=['shop', 'coin', 'clinic', 'people'],
                  notes=('Where will you use this on Monday? Four examples. A branch manager at a retail chain asks what a typical customer spends, and reports the median order with the IQR and the number of orders. '
                         'A credit analyst at a bank writes a GROUP BY with COUNT and AVG for each district, and takes the median in pandas. A health records officer reports the median visits and the IQR for each district before ranking the districts. '
                         'And a programme officer at an NGO, handing over to Power BI, picks a chart from the question and starts bar charts at zero. Which of these is closest to your job?')))

    # ------------------------------------------------------------------ 21 bridge
    S.append(dict(kind='code', title='Read the recipe before the lab: five formulas summarise a variable',
                  code='=MEDIAN(orders!G2:G2001)\n=QUARTILE(orders!G2:G2001,3)\n=STDEV(orders!G2:G2001)\n=COUNTIF(orders!G2:G2001,">107925")\n=LEFT(orders!B2,7)',
                  reads=[f'Line 1 gives the median: {n(B["median"])}.', f'Line 2 gives Q3: {B["q3"]:,.1f}.', f'Line 3 gives the sample standard deviation: about {n(B["sd"])}.', f'Line 4 counts the outliers beyond the fence: {n(B["n_out"])}.',
                         'Line 5 takes the first 7 characters of the text date, such as 2024-01. It makes a month column for the pivot table.'],
                  notes=(f'Before the lab, read the five formulas that do most of the work. Line one, MEDIAN of the order values, gives {n(B["median"])}. Line two, QUARTILE with a three, gives Q3, {B["q3"]:,.1f}. '
                         f'Line three, STDEV, gives about {n(B["sd"])}. Line four, COUNTIF with greater than 107925, counts the orders beyond the fence, {n(B["n_out"])}. '
                         'Line five uses LEFT to take the first seven characters of the date. The dates in this workbook are stored as text, so LEFT gives us a month such as 2024 dash 01, which the pivot table can group by. '
                         'Which formula would you change to find the median of the order lines instead?')))

    # ------------------------------------------------------------------ 22 divider
    S.append(dict(kind='divider', title='Part 2: the Sheets lab', lead='Close the slides. Open the sheet.', section='Lab',
                  notes=('That is the end of the ideas. Everything you need is on the slides you have just seen, and the lab sheet repeats each step. '
                         'Open the Lakeside Mart workbook in Google Sheets, or in Excel if you prefer. Today you add a month column, build three pivot tables, and make three charts. '
                         'In every task, predict the answer first, then compute it with a formula or a pivot table, then write what you found.')))

    # ------------------------------------------------------------------ 23 lab map
    S.append(dict(kind='steps', title='The lab has five steps, and you keep a workbook with pivots and charts',
                  steps=[dict(head='1 Summarise', text='Mean, median, mode', icon='calculator'), dict(head='2 Spread', text='Quartiles, IQR, SD', icon='bars'), dict(head='3 Histogram', text='Shape and outliers', icon='chart'),
                         dict(head='4 Pivot', text='Branch, month, median', icon='grid'), dict(head='5 Charts', text='Fix one, then write', icon='pen')], highlight=None,
                  caption='Eight tasks in 45 minutes. For each task, predict the answer, compute it, then write it in a notes tab.',
                  notes=('Here is the map of the lab. Step one, summarise the order values with the mean, median and mode. Step two, find the quartiles, the IQR, the fence and the standard deviation. '
                         'Step three, draw a histogram and check its bars with COUNTIFS. Step four, add a month column and build the pivot tables: branch by month, and the median by branch. '
                         'Step five, make a line chart, fix a misleading bar chart, and write two sentences for a manager. In every task, predict first. Please do not skip the predictions.')))

    # ------------------------------------------------------------------ 24 check numbers
    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Mean, median and mode of order_value_ugx', f'{B["mean"]:,.2f}, {n(B["median"])} and {n(B["mode"])}'], ['Q1, Q3 and the IQR', f'{B["q1"]:,.1f}, {B["q3"]:,.1f} and {n(B["iqr"])}'],
                        ['Sample standard deviation, and orders beyond 107,925', f'{n(B["sd"])} and {n(B["n_out"])}'], ['Orders at most 10,000, at most 50,000 and above 100,000', f'{n(B["n_le_10k"])}, {n(B["n_le_50k"])} and {n(B["n_gt_100k"])}'],
                        ['Orders in December 2024', n(F['dec24_orders'])], ['Pivot grand total, and December 2024 total', f'{n(F["grand"])} and {n(F["dec24_total"])}'],
                        ['Highest and lowest branch median', f'{n(F["med_max"])} ({F["med_max_id"]}) and {n(F["med_min"])} ({F["med_min_id"]})'], ['Highest and lowest month', f'{mname(F["best_month"])} and {mname(F["worst_month"])}']],
                  widths=[6.4, 5.6], icons=['calculator', 'bars', 'chart', 'receipt', 'calendar', 'grid', 'shop', 'clock'], note='If your number differs, find the task that went wrong. Do not change a number to match.',
                  notes=('Use this table as your own self-check. Nobody marks it. If your numbers match, carry on. If one does not, stop and call me, because later tasks use the earlier ones. '
                         'The most common causes are a range that includes the header row, a month column that was not filled all the way down, and a pivot table whose values are counted instead of summed. '
                         'Do not change a number to make it match. Find out why it is different. What does it mean if your grand total is far too small?')))

    # ------------------------------------------------------------------ 25 error cards
    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[['A pivot table shows Count where you wanted Sum', 'The summarise setting is COUNTA.', 'In the pivot editor, set Summarize by to SUM or MEDIAN.'],
                        ['#NAME? or a blank month column', 'The equals sign is missing, or the column is not filled down.', 'Type =LEFT(B2,7) and drag the fill handle to row 2001.'],
                        ['A histogram with one tall bar', 'The huge orders stretch the axis.', 'Customize: outlier percentile 95, bucket size 10000.'],
                        ['A column chart whose axis starts at 20,000', 'The axis minimum is set above zero.', 'Customize, Vertical axis, set Min to 0.'],
                        ['A bar differs by a few orders from the answer', 'Tools treat a bucket edge differently.', 'Accept a difference of up to 3 orders.']],
                  widths=[3.7, 4.2, 4.1], icons=['cross', 'cross', 'cross', 'cross', 'check'],
                  notes=('Five problems you may meet. A pivot table that shows Count where you wanted Sum: open the pivot editor and change Summarize by. A blank month column: type the LEFT formula with the equals sign and fill it down. '
                         'A histogram with one tall bar: the huge orders stretch the axis, so set the outlier percentile to ninety-five and the bucket size to ten thousand. A column chart that starts at twenty thousand: set the vertical axis minimum to zero. '
                         'And a bar that differs by a few orders from the answer is normal, because tools treat bucket edges differently. Read the message first. It usually tells you the answer.')))

    # ------------------------------------------------------------------ 26 exit check
    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[['A manager asks what a typical order is worth. Which statistic do you lead with, and what else do you give?', f'The median, {n(B["median"])} UGX, with the number of orders and the IQR. The mean, {n(B["mean"])}, is pulled up by a few large orders.'],
                        ['What is a pivot table in SQL and in pandas?', 'A GROUP BY in SQL and groupby in pandas: group the records, then aggregate each group.'],
                        ['A bar chart makes a small gap between two branches look huge. What do you check first?', 'Whether the vertical axis starts at zero. Cutting the base makes small gaps look large.']],
                  widths=[5.6, 6.4], icons=['calculator', 'grid', 'chart'],
                  notes=('Last, the exit check. Three questions. Write your answers in your notes before you look at mine. One, a manager asks what a typical order is worth. Which statistic do you lead with, and what do you give beside it? '
                         'Two, what is a pivot table called in SQL and in pandas? Three, a bar chart makes a small gap look huge. What do you check first? '
                         'The short answers are on the slide. If you got all three, you are ready for Session 4. These are also the warm-up questions at the start of that session.')))

    # ------------------------------------------------------------------ sheet tasks
    p = F['piv']
    sess['sheet_tasks'] = [
        dict(task='Open lakeside_for_sheets.xlsx and go to the orders tab. In a new tab called notes, compute for order_value_ugx (column G): the count, the sum, the mean, the median, the mode, the minimum and the maximum. Use COUNT, SUM, AVERAGE, MEDIAN, MODE, MIN and MAX on orders!G2:G2001. Predict first: will the mean be above or below the median?',
             answer=f'Count {n(N)}. Sum {n(B["sum"])}. Mean {B["mean"]:,.2f}. Median {n(B["median"])}. Mode {n(B["mode"])} ({B["mode_count"]} orders). Minimum {n(B["min"])}. Maximum {n(B["max"])}. The mean is {B["ratio"]:.2f} times the median, so it is above it. '
                    f'The full file gives a mean of {n(B["full_mean"])} and a median of {n(B["full_median"])}, a ratio of {B["full_ratio"]:.2f}: close, not identical, because the workbook is a sample.'),
        dict(task='Compute the quartiles and spread: =QUARTILE(orders!G2:G2001,1), =QUARTILE(orders!G2:G2001,3), the IQR (Q3 minus Q1), the fence (Q3 + 1.5 × IQR), the sample standard deviation =STDEV(orders!G2:G2001), and the number of orders above the fence with =COUNTIF(orders!G2:G2001,">107925").',
             answer=f'Q1 {B["q1"]:,.1f}. Q3 {B["q3"]:,.1f}. IQR {B["iqr"]:,.1f}. Fence {B["fence_hi"]:,.1f}. Standard deviation {B["sd"]:,.0f} (about {B["sd"]:,.2f}). {n(B["n_out"])} orders ({B["n_out_pct"] * 100:.1f} percent) lie above the fence, so a box plot would show a short box and a long line of dots to the right. The largest is {n(B["max"])}.'),
        dict(task='Draw a histogram of column G: select the column, Insert, Chart, choose Histogram chart. In Customize set the bucket size to 10000 and the outlier percentile to 95. Then check the bars with =COUNTIFS(orders!G2:G2001,"<=10000"), =COUNTIFS(orders!G2:G2001,"<=50000") and =COUNTIF(orders!G2:G2001,">100000"). Describe the shape and name its skewness.',
             answer=f'{n(B["n_le_10k"])} orders are at most 10,000, {n(B["n_le_50k"])} ({B["n_le_50k"] / N * 100:.1f} percent) are at most 50,000, and {n(B["n_gt_100k"])} are above 100,000. The first bar is the tallest and the bars fall steadily to the right: right-skewed (pandas skewness {B["skew"]:.2f}). '
                    'The first bar you see may differ from the COUNTIFS result by up to 3 orders depending on how Sheets treats the bucket edge.'),
        dict(task='In orders!H1 type month. In H2 type =LEFT(B2,7) and fill down to row 2001. How many orders were placed in December 2024? Use =COUNTIF(H2:H2001,"2024-12").',
             answer=f'{n(F["dec24_orders"])} orders. The dates are stored as text, so LEFT works. If your dates show as real dates, use =TEXT(B2,"yyyy-mm") instead.'),
        dict(task='Build a pivot table: Insert, Pivot table. Rows: branch_id. Columns: month. Values: order_value_ugx summarised by SUM. Read off B01 in 2024-01, B04 in 2024-03, B07 in 2024-01, the 2024-12 column total and the grand total. Predict which cell is unusually large.',
             answer=f'B01 in 2024-01: {n(F["b01_jan"])}. B04 in 2024-03: {n(F["b04_mar"])}, unusually large because it holds the single order of {n(B["max"])}. B07 in 2024-01: {n(F["b07_jan"])}. The 2024-12 total is {n(F["dec24_total"])}. The grand total is {n(F["grand"])} UGX, equal to the sum from task 1.'),
        dict(task='Make a second pivot table: Rows: branch_id. Values: order_value_ugx summarised by MEDIAN. Insert a column chart of it and set the vertical axis minimum to 20000. Which branch looks tallest, and how many times taller than the shortest does it look? Then fix the chart: set the minimum to 0 and add a title and axis labels with units.',
             answer='Medians: ' + ', '.join(f'{k} {n(r["median"])}' for k, r in br.iterrows()) + f'. On the cut axis {F["med_max_id"]} rises {n(F["med_max"] - 20000)} above the base and {F["med_min_id"]} only {n(F["med_min"] - 20000)}, so it looks {F["trunc_ratio"]:.1f} times taller. '
                    f'From zero, {F["med_max_id"]} is {F["true_ratio"]:.2f} times {F["med_min_id"]}, about {(F["true_ratio"] - 1) * 100:.0f} percent more: a modest gap.'),
        dict(task='Make a third pivot table: Rows: month. Values: SUM of order_value_ugx. Insert a line chart with the vertical axis starting at 0. Which month is highest and which is lowest? Does December 2024 stand out?',
             answer=f'Highest: {mname(F["best_month"])}, {n(F["best_val"])} UGX. Lowest: {mname(F["worst_month"])}, {n(F["worst_val"])}. December 2024 is {n(F["dec24"])}, number {F["dec24_rank"]} of 24, so it does not stand out. The sample has about {F["orders_per_month"]:.0f} orders a month, so a few large orders can reorder the months. The full file shows a clearer December peak.'),
        dict(task='Write two sentences for a manager on your notes tab. One gives the typical order value and says how many orders you counted. The other says whether the branches differ much in their typical order.',
             answer=f'Example: In a sample of {n(N)} orders the typical order is worth {n(B["median"])} UGX (the median), while the mean of {n(B["mean"])} is pulled up by a few very large orders. Branch medians run from {n(F["med_min"])} to {n(F["med_max"])} UGX, so the typical order is similar everywhere. '
                    'Any answer that leads with the median, states the count and says it is a sample is correct.'),
    ]

    # ------------------------------------------------------------------ facilitator
    sess['facilitator'] = dict(
        prep=['Open the deck and the workbook lakeside_for_sheets.xlsx in Google Sheets before anyone arrives. Share the file so every learner can make their own copy (File, Make a copy).',
              'Build the three pivot tables on your own copy and check them against the answer key. The answers were computed in pandas, not yet in Sheets. Check the MEDIAN summarise option in the pivot editor.',
              'Write the check table (slide 29 of the deck) on the board before the lab.',
              'Concepts run with laptops closed. Ask learners to open the workbook only after the Part 2 divider.',
              'Remind learners that all data is fictional and generated, and that the workbook is a 2,000-order sample of the full file.'],
        misconceptions=[('The mean is the typical value', f'With skewed data the mean is pulled by a few large values. Here the mean is {n(B["mean"])} and half the orders are under {n(B["median"])}.'),
                        ('Standard deviation is the average distance from the mean', 'It is a typical distance, calculated from squared deviations. It is not the plain average of the distances.'),
                        ('An outlier is a mistake and must be deleted', f'The IQR rule only flags unusual values. The largest order, {n(B["max"])} UGX, may be real. Ask the data owner before deleting.'),
                        ('A chart that starts above zero is fine if the labels are correct', 'For bars, length carries the value, so a cut base exaggerates differences.'),
                        ('A pivot table is a Sheets trick', 'It is a GROUP BY with an aggregation. SQL and pandas do the same thing.')],
        probes=[('Mean, median or mode for a typical order?', 'The median, with the count; the mean is pulled up by a few large orders.'),
                ('What does the IQR measure?', 'The spread of the middle half of the values: Q3 minus Q1.'),
                ('What does right-skewed mean?', 'A long tail of large values on the right, with the mean above the median.'),
                ('Which aggregation is a pivot table using when it shows a total?', 'SUM.'),
                ('Why does the largest order not change the median?', 'The median depends on position in the sorted list, not on how large the largest value is.'),
                ('Which chart for change over time?', 'A line chart, with the axis starting at zero when magnitudes matter.')],
        lab_steps=[('Task 1: summary statistics', f'Mean {B["mean"]:,.2f}, median {n(B["median"])}, mode {n(B["mode"])}. Learners should write the ratio {B["ratio"]:.2f}.'),
                   ('Task 2: quartiles and SD', f'Q1 {B["q1"]:,.1f}, Q3 {B["q3"]:,.1f}, fence {B["fence_hi"]:,.1f}, {n(B["n_out"])} outliers. Watch for STDEV against STDEV.P.'),
                   ('Task 3: histogram', f'{n(B["n_le_10k"])}, {n(B["n_le_50k"])}, {n(B["n_gt_100k"])}. Edge differences of up to 3 orders are fine.'),
                   ('Task 4: month column', f'{n(F["dec24_orders"])} orders in 2024-12. Check that the column is filled to row 2001.'),
                   ('Task 5: first pivot', f'Grand total {n(F["grand"])}. The B04 March cell is the big one.'),
                   ('Task 6: median pivot and axis', f'Medians {n(F["med_min"])} to {n(F["med_max"])}. The cut axis shows {F["trunc_ratio"]:.1f} times, the true figure {F["true_ratio"]:.2f}.'),
                   ('Task 7: line chart', f'{mname(F["best_month"])} highest, {mname(F["worst_month"])} lowest, December 2024 not special.'),
                   ('Task 8: two sentences', 'Accept any answer that leads with the median, gives the count and says it is a sample.')],
        rescue=['If the concepts run over, shorten the three-tool slide (slide 19) and the chart-choice slide (slide 21) to a quick look; the lab covers both.',
                'If only 30 minutes of lab remain, do tasks 1, 2, 5 and 6 and set the rest as homework.',
                'If a learner has Excel, a pivot table cannot summarise by MEDIAN. Use =MEDIAN(IF(orders!C2:C2001="B01",orders!G2:G2001)) entered as an array formula for each branch, or use Google Sheets for task 6.',
                'If a learner has no laptop, pair them with a neighbour: one types, one predicts aloud.'],
        after=['Share the workbook and this deck again for learners who were absent.', 'Ask each learner to save the notes tab, the pivot tables and the charts and bring one question about their own data to Session 4.', 'Note any question you could not answer and open the next session with it.'],
        lab_answer_key=[['Task 1 PREDICT: is the mean above or below the median?', f'Above: {n(B["mean"])} against {n(B["median"])}, a ratio of {B["ratio"]:.2f}.'],
                        ['Task 2 READ: what does the long line of dots tell you?', f'{n(B["n_out"])} orders lie beyond the fence. The distribution is right-skewed.'],
                        ['Task 3 READ: why is the first bar the tallest?', f'Most orders are small: {n(B["n_le_10k"])} of {n(N)} are at most 10,000.'],
                        ['Task 5 PREDICT: which pivot cell is unusually large?', f'B04 in 2024-03, {n(F["b04_mar"])}, because of one order of {n(B["max"])}.'],
                        ['Task 6 CHANGE: set the axis minimum back to 0.', f'The apparent {F["trunc_ratio"]:.1f} times becomes {F["true_ratio"]:.2f} times.'],
                        ['Task 7 READ: does December 2024 stand out?', f'No, it is number {F["dec24_rank"]} of 24. The sample is small.'],
                        ['Task 8 CHANGE: use the mean instead of the median in your sentence.', 'The sentence now describes an order that few shoppers place. That is the point of leading with the median.']])
    return sess
