"""Session 11: Exploring and visualising with Python (EDA routine, matplotlib Figure and Axes, seaborn, count versus rate, seasonality, writing a finding).
Every number comes from f11_facts.facts() (pandas on the real Lakeside Mart CSV files). Code shown on slides is run in run_snippet, so its output is real.
Charts on the slides are drawn by kit/diagrams_ds_f.py from the same files with the same seaborn calls.
"""
import importlib.util
from pathlib import Path

import pandas as pd

_p = Path(__file__).resolve().parent / 'f11_facts.py'
_spec = importlib.util.spec_from_file_location('f11_facts', _p)
f11 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(f11)
n = f11.n

SN1 = ("import pandas as pd\n"
       "orders = pd.read_csv('orders.csv',\n"
       "                     parse_dates=['order_date'])\n"
       "print(orders.shape)\n"
       "orders.isna().sum()")
SN2 = ("import matplotlib.pyplot as plt\n"
       "value = orders['order_value_ugx']\n"
       "by_month = orders['order_date'].dt.to_period('M')\n"
       "monthly = value.groupby(by_month).sum() / 1e6\n"
       "fig, ax = plt.subplots()\n"
       "ax.plot(monthly.index.astype(str), monthly.values)\n"
       "ax.set_title('Monthly revenue')\n"
       "ax.set_ylabel('UGX millions')\n"
       "print(type(fig).__name__, type(ax).__name__)")
SN3 = ("# run once; to run again, first reload orders\n"
       "import seaborn as sns\n"
       "lines = pd.read_csv('order_lines.csv')\n"
       "basket = lines.groupby('order_id').size()\n"
       "basket = basket.rename('basket_size')\n"
       "orders = orders.merge(basket, on='order_id',\n"
       "                     how='left', validate='m:1')\n"
       "sns.histplot(data=orders, x='basket_size',\n"
       "             discrete=True)\n"
       "print(orders.shape, orders.basket_size.median())")


def build():
    F = f11.facts()
    ns, out1 = f11.run_snippet(SN1)
    ns, out2 = f11.run_snippet(SN2, ns)
    ns, out3 = f11.run_snippet(SN3, ns)
    assert out1.splitlines()[0] == f'({F["rows"]}, {F["cols"]})' and out2 == 'Figure Axes' and out3 == f'({F["ob_shape"][0]}, {F["ob_shape"][1]}) {F["basket_median"]}'
    D = F['desc']
    rb = F['rb']
    names = F['names']
    bt, br_ = F['top_count'], F['top_rate']
    dr = F['dec_ratio']
    sess = dict(
        num=11, block='Module C: Analyse and explain', short_title='Exploring and visualising',
        title='Exploring and visualising data with Python: from a new file to a finding',
        question='How do I explore an unfamiliar dataset in one sitting and find what is worth reporting?',
        outcomes=['Run a repeatable exploratory data analysis (EDA) routine on a new dataset',
                  'Draw histograms, box plots, scatter plots, bar charts and line charts with matplotlib and seaborn',
                  'Tell a count from a rate and spot seasonality, then write a finding with a number, a comparison and a limit'],
        outcome_icons=['magnifier', 'chart', 'notebook'],
        outcome_note=('Here is what you can do by the end of today. You can run the same exploratory data analysis routine on any new file, in the same order. '
                      'You can draw five kinds of chart with matplotlib and seaborn and say which one fits which question. '
                      'And you can tell a count from a rate, spot a seasonal pattern, and write a finding that states a number, a comparison and a limit. The charts come from the Lakeside Mart orders, and you will draw your own in the lab.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: picture, plain words, one example by hand'), (10, 'Break'), (45, 'Lab: predict, run, read, change'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: concepts first, then a Python lab in Colab',
        plan_caption='Pictures and ideas first. Then you open the notebook and draw your own charts.',
        plan_note=('We have two hours. The first ten minutes bring back SQL from Session 10 and set the question for today. Then forty-five minutes of concepts with laptops closed, so you can watch the charts and follow the reasoning. '
                   'After a ten minute break you open the notebook in Google Colab for a forty-five minute lab: predict, run, read and change. The last ten minutes are an exit check and what you keep. '
                   'Please protect the lab time. Drawing charts yourself is where the learning sticks.'),
        recall_from='Session 10',
        recall=[('In SQL, what is the difference between WHERE and HAVING?', 'WHERE keeps rows before the grouping. HAVING keeps groups after the aggregation, such as a count or a sum.'),
                ('Why did you check each SQL result against pandas?', 'Two different routes to the same number is the best evidence that the number is right.'),
                ('Which SQL clause turns many order lines into one number per branch?', 'GROUP BY, together with an aggregate function such as COUNT or SUM.')],
        words=[('Exploratory data analysis (EDA)', 'A repeatable routine of looks, summaries and charts that you run on a new dataset before you model it or report on it.'),
               ('Figure and Axes (matplotlib)', 'The Figure is the whole page. The Axes is the plot area on that page where the data are drawn and labelled.'),
               ('Count and rate', 'A count is how many. A rate divides the count by what could have happened, such as returns per 100 lines sold.'),
               ('Seasonality (with trend and noise)', 'A pattern that comes back at the same time every year, such as a December peak.'),
               ('Finding', 'One sentence that states a number, a comparison and a limit.')],
        word_icons=['magnifier', 'chart', 'calculator', 'calendar', 'notebook'],
        words_note=('Five words for today. Exploratory data analysis, or EDA, is the routine of getting to know a new file. In matplotlib the Figure is the page and the Axes is the plot area on it. '
                    'A count says how many, and a rate divides by what could have happened. Seasonality is a pattern that returns each year. And a finding is one sentence with a number, a comparison and a limit. We use every one of them before we finish.'),
        keep='Keep your exploration notebook: eight charts of the Lakeside orders and returns, and three findings written in plain words, each with a number, a comparison and a limit.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab file', value='Notebook, 8 charts'), dict(label='Your writing', value='3 findings'), dict(label='Next session', value='Is it real?')]),
        keep_title='Save your notebook with its eight charts and three findings',
        next='Session 12: Inference. When two groups differ, how do we know chance alone does not explain it? We test the loyalty offer.', next_label='Next session',
        keep_note=('Before you go, save your notebook with the charts and the three findings. That is your keepsake from today, and it is the kind of page you can show a manager on Monday. '
                   'Read each finding once more and check it has a number, a comparison and a limit. Next session we take a gap between two groups and ask whether it could be luck. '
                   'If any chart was unclear today, write the question down and bring it.'),
        cover_note=('Welcome back. Last session you asked a database questions in SQL. Today you meet a file you have never seen, which is where most analysts start. '
                    'You will learn the routine for your first hour with a new file, you will draw charts with matplotlib and seaborn, and you will meet a result that fools almost everyone the first time. '
                    'By the end you will have a notebook with eight charts and three findings.'),
        use_at_work='Explore a new file in a fixed order, draw the right chart, and write a finding with a number and a limit.',
        slides=[])
    S = sess['slides']

    # 1 answers
    S.append(dict(kind='table', title='Answers to the three questions from Session 10', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in sess['recall']], widths=[5.2, 6.8], icons=['pin', 'check', 'folder'],
                  notes=('Here are the answers to the three warm-up questions. WHERE keeps rows before any grouping happens, and HAVING keeps groups after the aggregation, so a branch with more than a thousand orders is a HAVING. '
                         'You checked each SQL result against pandas because two different routes to the same number is the best evidence that the number is right. We use that habit again today, because a chart can look convincing when the numbers behind it are wrong. '
                         'And GROUP BY with an aggregate function such as COUNT or SUM turns many order lines into one number per branch. Which of the three did you find hardest?')))

    # 2 routine
    S.append(dict(kind='steps', title='Exploratory data analysis (EDA) is a six-step routine you repeat on every new file',
                  steps=[dict(head='1 Look', text='Shape, data types, missing', icon='magnifier'), dict(head='2 Summarise', text='One summary per number', icon='calculator'),
                         dict(head='3 One variable', text='Histogram for its shape', icon='chart'), dict(head='4 Two variables', text='Scatter plot', icon='pin'),
                         dict(head='5 Groups', text='Counts and rates', icon='people'), dict(head='6 Write', text='A finding', icon='notebook')], highlight=None,
                  caption='Exploratory data analysis (EDA) is what you do in Excel when you scroll, filter and pivot a new sheet. Python lets you write the routine down so it runs the same way every time.',
                  notes=('When you meet a new file, you do not start with a model or a report. You explore it. The name is exploratory data analysis, or EDA. In Excel you do it by scrolling, filtering and building a quick pivot table. '
                         'In Python we write the routine down. Step one is to look: the shape, the data types and the missing values. Step two is to summarise each numeric variable. Step three is to draw one variable at a time, and step four to draw two together. '
                         'Step five is to compare groups with counts and rates. Step six is to write a finding. If you cannot write the sentence, you have not finished exploring. Which step do you already do in Excel?')))

    # 3 first look code
    S.append(dict(kind='code', title='Step 1, the first look: read the file, then count the records and the missing values', code=SN1,
                  output=out1.splitlines(),
                  reads=['read_csv loads the file into a DataFrame. parse_dates makes order_date a real date.', f'shape: {n(F["rows"])} records and {F["cols"]} variables.',
                         'isna().sum() counts the missing values in each variable.', f'customer_id has {n(F["missing_cust"])} missing: walk-in shoppers.'],
                  notes=(f'This is step one. We load the orders file into a pandas DataFrame, and we ask pandas to read order underscore date as a real date, which matters when we draw a line over time. '
                         f'The shape is {n(F["rows"])} records by {F["cols"]} variables. The isna dot sum call counts the missing values in every variable. '
                         f'Look at customer id. It has {n(F["missing_cust"])} missing values out of {n(F["rows"])}. You met that in Session 2: the blank means a walk-in shopper. '
                         'Always check missing values before you draw anything. In Session 7 you also met the dtypes attribute, which lists the data type of each variable. Which variable would you check first?')))

    # 4 describe
    S.append(dict(kind='table', title=f'Step 2, summarise: the mean order value is {F["mean_over_median"]:.1f} times the median, so the distribution is right-skewed',
                  headers=['Statistic', 'Order value (UGX)', 'What it tells you'],
                  rows=[['count', n(D['count']), 'How many orders have a value.'], ['mean', n(D['mean']), 'The arithmetic mean: the total divided by the count.'], ['std', n(D['std']), 'The standard deviation: the typical distance from the mean.'],
                        ['min', n(D['min']), 'The smallest order.'], ['25% (Q1)', n(D['25%']), 'A quarter of the orders are below this.'], ['50% (median)', n(D['50%']), 'Half of the orders are below this.'],
                        ['75% (Q3)', n(D['75%']), 'Three quarters of the orders are below this.'], ['max', n(D['max']), 'The largest order.']],
                  widths=[2.4, 2.6, 7.0], icons=['calculator', 'chart', 'clock', 'cross', 'flag', 'pin', 'flag', 'coin'], note='Python: the describe method. Excel: AVERAGE, STDEV.S, MIN, QUARTILE, MEDIAN, MAX.',
                  notes=(f'The describe call gives eight summary numbers for a numeric variable, and here they are for the order value. The mean is {n(D["mean"])} shillings and the median, the middle order, is {n(D["50%"])}. '
                         f'The mean is {F["mean_over_median"]:.1f} times the median. That gap is the sign of a right-skewed distribution: a few very large orders pull the mean up. The largest order is {n(D["max"])} shillings. '
                         f'The standard deviation of {n(D["std"])} is bigger than the mean, which tells you the values are spread widely. Quartile one and quartile three, {n(D["25%"])} and {n(D["75%"])}, mark the middle half of the orders. '
                         'So which would you quote as the typical order, the mean or the median?')))

    # 5 histogram
    S.append(dict(kind='idea', title='Step 3, one variable: a histogram shows the shape of the distribution',
                  visual=dict(kind='f_panels', panels=[dict(type='sns', recipe='hist_value', title='Order value, orders up to 200,000 UGX', xlabel='Order value (UGX)', ylabel='Number of orders', xk=True, xlim=(0, 200000), legend='upper right')], ncols=1, left=0.14, right=0.94, bottom=0.17, top=0.9),
                  lead='A histogram counts how many records fall in each bin (a range of values).',
                  points=['Tall bars on the left: most orders are small.', f'Long right tail: the mean {n(F["mean"])} is right of the median {n(F["median"])}.', f'{n(F["above200k"])} orders above 200,000 are off the chart.'],
                  notes=(f'This is a histogram. It splits the order value into bins, each ten thousand shillings wide, and the height of a bar counts the orders in that bin. The picture is drawn with seaborn histplot. '
                         f'Most orders are small, so the tall bars sit on the left. The gold line is the median and the dashed red line is the mean. The mean sits to the right because of the long tail, which is the right skew. '
                         f'The chart stops at two hundred thousand shillings for readability. {n(F["above200k"])} orders, {F["above200k_pct"]:.1f} percent, are larger and are off the chart, and the largest is {n(D["max"])}. '
                         'Why would a bar chart of the average hide this shape?')))

    # 6 anatomy
    mo24 = F['monthly'][F['monthly'].year == 2024].rev_m.tolist()
    S.append(dict(kind='wide', title='matplotlib draws on a Figure that holds an Axes',
                  visual=dict(kind='f_anatomy', months=f11.MONTHS, values=mo24, parts=[['Figure (fig): the page', 'plt.subplots()'], ['Axes (ax): the plot area', 'same call'], ['Title', 'ax.set_title()'], ['y-axis label', 'ax.set_ylabel()'], ['x-axis label', 'ax.set_xlabel()'], ['Tick labels', 'automatic'], ['Line: the data', 'ax.plot()']]),
                  caption='An axis is one scale. The Axes holds both.',
                  notes=('matplotlib is the drawing library under almost every Python chart, and it has two objects to know. The Figure is the whole page. The Axes is the plot area on that page, with its scales, the line or bars, and their labels. '
                         'One call, plt dot subplots, gives you both, and the convention is to name them fig and ax. Then you draw on ax and label it: a title, a y label, an x label. '
                         'Be careful with the word. An axis is one scale, the x or the y. The Axes is the whole plot area that holds them. In Excel you would select a chart and add axis titles. Here each is one line of code, so the chart can be rebuilt tomorrow with new data. '
                         'Which number on the picture is the Axes?')))

    # 7 matplotlib code
    S.append(dict(kind='code', title='Draw a line chart with matplotlib: make the Figure and Axes, draw, label', code=SN2, output=out2.splitlines(),
                  reads=['Total the order value for each month and divide by a million, so the axis reads in UGX millions.', 'plt.subplots() returns the Figure and the Axes.', 'ax.plot draws one line. set_title and set_ylabel add the words.',
                         'The last line checks the types: a Figure and an Axes. In Colab the chart appears under the cell.'],
                  notes=('Read this recipe before we use it in the lab. The first two lines total the order value for each month, in millions of shillings. Then plt dot subplots makes the Figure and the Axes. '
                         'We draw one line on the Axes with ax dot plot, then label it with a title and a y label that says the units. Without units nobody knows what the numbers mean. '
                         'The final print confirms what we hold: a Figure and an Axes. When you run it in Colab, the chart appears under the cell. Why do we put the unit in the label?')))

    # 8 choose the chart
    S.append(dict(kind='table', title='Choose the chart from the question, then the seaborn function that draws it',
                  headers=['Question you ask', 'Chart', 'seaborn function', 'Lakeside example'],
                  rows=[['How is one numeric variable spread?', 'Histogram', 'sns.histplot', 'Order value, basket size'], ['How does a numeric variable differ between groups?', 'Box plot', 'sns.boxplot', 'Order value by payment method'],
                        ['Do two numeric variables move together?', 'Scatter plot', 'sns.scatterplot', 'Basket size and order value'], ['Which group has the larger mean or count?', 'Bar chart', 'sns.barplot', 'Mean order value by branch'],
                        ['How does a number change over time?', 'Line chart', 'sns.lineplot', 'Revenue by month']],
                  widths=[4.3, 1.9, 2.6, 3.4], icons=['chart', 'people', 'pin', 'shop', 'calendar'], note='seaborn builds on matplotlib. You pass a DataFrame and the column names, and it returns an Axes. hue colours the marks by a categorical variable.',
                  notes=('Before more code, a decision guide. Start from the question and the chart follows. One numeric variable, and you want its shape: a histogram. A numeric variable compared across groups: a box plot. '
                         'Two numeric variables together: a scatter plot. Which group has the larger mean or count: a bar chart. A number over time: a line chart. '
                         'seaborn is a library built on matplotlib. You give it the DataFrame and the names of the columns, and it draws the chart and returns an Axes that you can still label. Its hue setting colours the marks by a categorical variable. '
                         'Which question in this table is closest to one you ask at work?')))

    # 9 boxplot
    pm = F['pay_median']
    _o = pd.read_csv(f11.DATA / 'orders.csv')
    _f = {k: g.order_value_ugx.quantile(.75) + 1.5 * (g.order_value_ugx.quantile(.75) - g.order_value_ugx.quantile(.25)) for k, g in _o.groupby('payment_method')}
    fdev = max(abs(v_ - F['fence']) for v_ in _f.values())
    fmax, fmin = max(_f.values()), min(_f.values())
    assert fdev < 1500
    S.append(dict(kind='idea', title='A box plot compares the spread of order value across payment methods',
                  visual=dict(kind='f_panels', panels=[dict(type='sns', recipe='box_pay', title='Order value by payment method', xlabel='Payment method', ylabel='Order value (UGX)', yk=True)], ncols=1, left=0.16, bottom=0.17, top=0.9),
                  lead='Each box holds the middle half of the orders, from Q1 to Q3. The line inside is the median.',
                  points=['Whiskers end at the last order within 1.5 x IQR of the box.', f'About {n(F["outliers_iqr"])} orders ({F["outliers_iqr_pct"]:.1f}%) are above the fence, {n(F["fence"])} UGX.', f'Medians within {n(max(pm.values()) - min(pm.values()))} UGX. Each box fence is within {n(fdev)} of it.'],
                  notes=(f'A box plot shows the shape of a numeric variable for each group, side by side. The box runs from quartile one to quartile three, so it holds the middle half of the orders. The line inside the box is the median. '
                         f'The whiskers end at the last order that lies within one and a half times the interquartile range beyond the box. Values beyond are outliers. About {n(F["outliers_iqr"])} orders, {F["outliers_iqr_pct"]:.1f} percent, lie above the fence of {n(F["fence"])} shillings, which is Q3 plus one and a half times the IQR for all orders. Each box has its own fence, within {n(fdev)} shillings of that. We hide those orders with showfliers equals False. '
                         f'The finding is that the three boxes are almost identical. The medians are {n(pm["Card"])}, {n(pm["Cash"])} and {n(pm["Mobile money"])}. Payment method does not change the typical order. Would you have guessed that?')))

    # 10 scatter
    S.append(dict(kind='idea', title='Step 4, two variables: a scatter plot shows whether they move together',
                  visual=dict(kind='f_panels', panels=[dict(type='sns', recipe='scatter_hue', title='2,000 orders: basket size and value', xlabel='Lines on the order (basket size)', ylabel='Order value (UGX)')], ncols=1, left=0.16, bottom=0.17, top=0.9),
                  lead=f'Bigger baskets cost more. The correlation is r = {F["corr"]:.2f}.',
                  points=['r runs from -1 to 1. About 0.3 is modest.', 'hue colours points by payment method. No colour stands apart.', f'{F["sample_above300k"]} points above 300,000 are off the chart.'],
                  notes=(f'A scatter plot puts one numeric variable on each axis, and every point is one record. Here are two thousand randomly chosen orders. Basket size, the number of lines on the order, runs along the bottom, and the order value up the side. '
                         f'The points rise to the right, so bigger baskets cost more. The correlation coefficient, Pearson r, is {F["corr"]:.2f}. That is a modest link, because the price of the products varies a lot. '
                         f'The hue setting colours each point by payment method. The three colours are mixed, so payment method does not explain anything here. {F["sample_above300k"]} points are above three hundred thousand and are off the chart. '
                         'Correlation is not causation. What else could drive both?')))

    # 11 barplot
    bmax, bmin = F['branch_max'], F['branch_min']
    S.append(dict(kind='idea', title='A bar chart of means needs its error bars: the branches barely differ',
                  visual=dict(kind='f_panels', panels=[dict(type='sns', recipe='bar_branch', title='Mean order value by branch', xlabel='Branch', ylabel='Order value (UGX)', yk=True)], ncols=1, left=0.16, bottom=0.17, top=0.9),
                  lead='sns.barplot draws each group mean. The black line is a 95 percent confidence interval.',
                  points=[f'Highest mean {bmax}: {n(F["branch_mean"][bmax])}. Lowest {bmin}: {n(F["branch_mean"][bmin])}.', 'The intervals overlap: the gap may be sampling variability. This is no test.', 'Session 12 tests it properly.'],
                  notes=(f'Now a bar chart, drawn with seaborn barplot. By default it plots the mean of each group, and the black line on each bar is a confidence interval, a range that is built to catch the true mean about ninety five times in a hundred. '
                         f'The highest branch mean is {bmax}, {n(F["branch_mean"][bmax])} shillings, and the lowest is {bmin}, {n(F["branch_mean"][bmin])}. The bars look alike, and the lines overlap. '
                         'When intervals overlap like this, it is a warning that the gap between the two branches may be sampling variability. Overlap is not a formal test, and here we also picked the highest and the lowest of eight branches. We do not claim a difference from these bars. '
                         'Next session we learn how to test it properly. Why does a bar chart without the error bars invite a wrong conclusion?')))

    # 12 count vs rate figure
    S.append(dict(kind='wide', title=f'Step 5, groups: {bt} has the most returns, but {br_} has the highest rate',
                  visual=dict(kind='f_panels', panels=[dict(type='sns', recipe='count_branch', title='Count: number of returns', xlabel='Branch', ylabel='Returns'),
                                                       dict(type='sns', recipe='rate_branch', title='Rate: returns per 100 lines sold', xlabel='Branch', ylabel='Returns per 100 lines')], ncols=2, wspace=0.28, left=0.08, bottom=0.2, top=0.87),
                  caption=f'Red marks the top bar. {bt} is {names[bt]}. {br_} is {names[br_]}.',
                  notes=(f'Here is a result that fools almost everyone the first time. On the left, the count of returns. Branch {bt}, {names[bt]}, has the most, {int(rb.returns[bt])}. '
                         f'On the right, the rate, which is returns per hundred lines sold. Now the top bar is branch {br_}, {names[br_]}, at {rb.per_100[br_]:.2f}. The two charts name different branches. '
                         f'The count favours big branches, because a branch that sells more has more things to return. {bt} sold {n(rb.lines[bt])} lines. The rate divides by what was sold, so branches of different size can be compared fairly. '
                         'Which chart would you show to the manager who asks which branch has a returns problem?')))

    # 13 formula rate
    S.append(dict(kind='formula', title='A rate divides the count by what could have happened: returns per 100 lines sold',
                  formulas=[('Rate', r'$\mathrm{rate} = \frac{\mathrm{count\ of\ returns}}{\mathrm{lines\ sold}} \times 100$'),
                            (f'Branch {br_}', rf'$\frac{{{int(rb.returns[br_])}}}{{{int(rb.lines[br_])}}} \times 100 = {rb.per_100[br_]:.2f}$')],
                  symbols=[['count', 'How many events happened.', f'{int(rb.returns[br_])} returns at {br_}'], ['denominator', 'What could have happened: the lines sold.', f'{n(rb.lines[br_])} lines at {br_}'],
                           ['x 100', 'Gives events per 100 lines.', f'{rb.per_100[br_]:.2f} per 100'], ['All branches', 'Total returns over total lines, times 100.', f'{n(F["returns_rows"])} / {n(F["lines_rows"])} = {F["rate_all"]:.2f}']],
                  size=22, note='A rate is a ratio of events to opportunities. A percentage is a rate per 100.',
                  notes=(f'The rate is a short formula. Take the count of returns, divide by the lines sold, and multiply by one hundred. The lines sold are the denominator: everything that could have been returned. '
                         f'For branch {br_}, {int(rb.returns[br_])} returns divided by {n(rb.lines[br_])} lines, times one hundred, gives {rb.per_100[br_]:.2f} returns per hundred lines. '
                         f'Across all branches the rate is {n(F["returns_rows"])} returns over {n(F["lines_rows"])} lines, which is {F["rate_all"]:.2f}. So {br_} returns about one and a half times as often as the whole company. '
                         'In Excel this is a calculated column that divides one column by another. What would the denominator be for a complaint rate?')))

    # 14 rank table
    rows = [[f'{k} {names[k]}', n(rb.returns[k]), n(rb.lines[k]), f'{rb.per_100[k]:.2f}', str(rb.rank_count[k]), str(rb.rank_rate[k])] for k in rb.index]
    S.append(dict(kind='table', title=f'The ranking reverses: {bt} is first by count and last by rate',
                  headers=['Branch', 'Returns (count)', 'Lines sold', 'Rate per 100 lines', 'Rank by count', 'Rank by rate'], rows=rows, widths=[3.4, 1.8, 1.7, 2.0, 1.5, 1.5],
                  icons=['shop'] * 8, note='Rank 1 is the highest. Returns are counted in the returns file and lines sold in order_lines (lines, not units), both joined to the branch of the order.',
                  notes=(f'Here are all eight branches with the count, the lines sold, the rate and the two rankings. Branch {bt} ranks first by count and {int(rb.rank_rate[bt])}th, which is last, by rate. '
                         f'Branch {br_} ranks {int(rb.rank_count[br_])}nd by count and first by rate. The count told us about the size of the branch. The rate tells us about behaviour. '
                         'To build this table we joined the returns and the order lines to the orders, to get the branch, then counted each. That is the merge you practised in Session 9. '
                         'When you see a ranking by count in a report, which question should you ask before you believe it?')))

    # 15 seasonality figure
    S.append(dict(kind='wide', title='Seasonality: revenue peaked in December in both years, because there were more orders',
                  visual=dict(kind='f_panels', panels=[dict(type='sns', recipe='line_season', title='Revenue by month', xlabel='Month of the year', ylabel='UGX millions'),
                                                       dict(type='sns', recipe='line_orders', title='Number of orders by month', xlabel='Month of the year', ylabel='Orders')], ncols=2, wspace=0.28, left=0.08, bottom=0.2, top=0.87),
                  caption='Each line is one year over the same twelve months. Both years rise in December.',
                  notes=(f'Now a line chart over time, with a trick. Instead of one long line, we draw each year as its own line over the same twelve months. That makes a repeating pattern easy to see. '
                         f'On the left is revenue. Both years climb in December, to {F["dec_rev"][2024]:.1f} million in 2024 and {F["dec_rev"][2025]:.1f} million in 2025. On the right is the number of orders, which climbs in the same month. '
                         f'The December order count was {n(F["dec_orders"][2024])} and {n(F["dec_orders"][2025])}. The average order value barely moved, {n(F["aov_dec"][2024])} in December 2024 against {n(F["aov_other"])} in the other months of both years. '
                         f'So the peak comes from more orders: the average order value stayed near {n(round(F["aov_other"], -2))}. What might bring more shoppers in December?')))

    # 16 trend seasonality noise
    mon = F['monthly']
    S.append(dict(kind='idea', title=f'December revenue was {dr[2024]:.2f} and {dr[2025]:.2f} times the average of the other months',
                  visual=dict(kind='f_panels', panels=[dict(type='bar', labels=[x[0] for x in f11.MONTHS] * 2, values=mon.rev_m.round(1).tolist(), hl=[i for i in range(24) if i % 12 == 11], width=0.8,
                                                            hlines=[(F['rev_other_mean'], f'mean of the 22 other months: {F["rev_other_mean"]:.1f}', GOLD_C, '--')], title='Revenue by month, Jan 2024 to Dec 2025', xlabel='Month (J to D, twice)', ylabel='UGX millions', legend='upper left', ylim=(0, 112))], ncols=1, left=0.13, bottom=0.17, top=0.9),
                  lead='A time series has a trend, seasonality and noise. This one has a clear seasonal peak.',
                  points=['Trend: slow rise or fall. Seasonality: yearly repeat. Noise: random variation.', f'Mean of the 22 other months: {F["rev_other_mean"]:.1f} million.', 'Limit: only two Decembers.'],
                  notes=(f'A time series, which is a number measured over time, is usually described by three parts. The trend is the slow movement up or down. The seasonality is the pattern that repeats each year. And the noise is the random variation that is left. Together they are called the decomposition. '
                         f'Here the red bars are the two Decembers. The dashed line is the average of the other twenty two months, {F["rev_other_mean"]:.1f} million shillings. December 2024 was {dr[2024]:.2f} times that and December 2025 was {dr[2025]:.2f} times. '
                         'The limit is important. We have only two Decembers, so we can say the pattern repeated once. With more years we could say more. How many years of data would you want?')))

    # 17 finding
    S.append(dict(kind='compare', title='Step 6, write: a finding states a number, a comparison and a limit',
                  left=dict(head='Weak', points=['Returns are high in Kampala Central.', 'No number, comparison or limit.']),
                  right=dict(head='Strong', points=[f'{names[bt]} has the most returns ({int(rb.returns[bt])}) but the lowest rate: {rb.per_100[bt]:.2f} per 100 lines sold, against {F["rate_all"]:.2f} overall.', 'Limit: a 5 percent sample, 2024 to 2025.']),
                  verdict='If you cannot write the sentence, you have not finished exploring.',
                  notes=(f'The last step of the routine is to write. A finding is one sentence with three parts. A number says how big the thing is. A comparison says against what. And a limit says what the data cannot tell us. '
                         f'The weak version says returns are high in Kampala Central. A reader cannot check it. The strong version says {names[bt]} has the most returns, {int(rb.returns[bt])}, but the lowest rate, {rb.per_100[bt]:.2f} per hundred lines sold, against {F["rate_all"]:.2f} for all branches, '
                         'and it names the limit: this is a sample of orders over two years. Which of your own reports would you rewrite this way?')))

    # 18 chart habits
    S.append(dict(kind='table', title='Five habits make a chart honest before you send it',
                  headers=['Habit', 'Why', 'Example from today'],
                  rows=[['Title that states the point', 'The reader should not have to guess.', 'Revenue by month, with both years'], ['Axis labels with units', 'A number without a unit has no meaning.', 'UGX millions, returns per 100 lines'],
                        ['Bars start at zero', 'A truncated axis makes small gaps look large.', 'The branch means chart starts at 0'], ['Say what hidden values exist', 'Limits on an axis can hide records.', f'{n(F["above200k"])} orders above 200,000 UGX'],
                        ['Explain every colour', 'Colour needs a legend or a caption.', 'Red marks the top bar; hue is payment method']],
                  widths=[3.4, 4.2, 4.4], icons=['doc', 'ruler' if False else 'calculator', 'chart', 'magnifier', 'flag'],
                  notes=('Before you send any chart, run through five habits. One, a title that states the point, so the reader does not have to guess. Two, axis labels with units. A number without a unit has no meaning. '
                         f'Three, start bars at zero, because a truncated axis makes small gaps look large. Four, say what you hid. Our first histogram stops at two hundred thousand, and {n(F["above200k"])} orders are beyond it, so the caption says so. '
                         'Five, explain every colour. None of these needs more than one line of code. Which habit does your last report miss?')))

    # 19 use at work
    S.append(dict(kind='table', title='Where you will use this at work: explore a new file in the same order every time',
                  headers=['Your job', 'The new file', 'What today lets you do'],
                  rows=[['Credit analyst at a bank in Kampala, using pandas and seaborn', 'A loan book of 8,000 loans.', 'Check missing incomes and loan sizes before any model.'],
                        ['District health officer preparing a monthly report', 'Clinic visits by district and month.', 'Plot each district by month, spot the seasonal peak, and report visits per clinic day, or a rate per 1,000 people when you have the population.'],
                        ['Retail analyst handing charts to a manager', 'Till orders and returns by branch.', 'Show rate and count side by side, with a finding and its limit. Export with savefig and to_excel.'],
                        ['Programme officer at an NGO', 'A survey export with text and numeric answers.', 'Run the six steps in a notebook a colleague can rerun.']],
                  widths=[3.6, 3.8, 4.6], icons=['coin', 'clinic', 'shop', 'people'],
                  notes=('Where will you use this on Monday? A credit analyst at a bank in Kampala who uses pandas and seaborn can look at the missing incomes and the spread of loan sizes before any model is built. '
                         'A district health officer can plot each district by month, spot the seasonal peak, and report a rate per thousand people. A retail analyst can show the count and the rate side by side with a finding that states its limit. '
                         'And a programme officer at an NGO can run the six steps in a notebook, so a colleague can rerun it next quarter. These example files are fictional here, but the routine is the same. Which of these is closest to your job?')))

    # 20 bridge
    S.append(dict(kind='code', title='Read the recipe before the lab: merge, draw, check', code=SN3, output=out3.splitlines(),
                  reads=['Read the order lines and count the lines on each order. That count is the basket size.', 'merge adds basket_size to each order. It now has one more variable.', 'sns.histplot draws the distribution of basket size, one bar per size.',
                         f'The median basket is {int(F["basket_median"])} lines. The mean is {F["basket_mean"]:.2f}, because a few baskets are large.'],
                  notes=(f'Before the lab, read this recipe. We read the order lines and count the lines on each order with groupby and size. That count is the basket size. Then merge attaches it to every order, which gives {F["ob_shape"][1]} variables. '
                         f'Then sns dot histplot draws the distribution of basket size, with discrete equals True, so each basket size gets its own bar. The print gives the shape and the median basket, which is {int(F["basket_median"])} lines. '
                         f'The mean is {F["basket_mean"]:.2f}, higher than the median, because a few baskets are large. The largest has {F["basket_max"]}. In the lab you use the same pattern for every chart. Which line would you change to chart the order value instead?')))

    # 21 divider
    S.append(dict(kind='divider', title='Part 2: the Python lab', lead='Close the slides. Open the notebook.', section='Lab',
                  notes=('That is the end of the ideas. Everything you need is on the slides you have just seen, and the notebook repeats each step. '
                         'Open Google Colab, and open the notebook for Session 11. Run the first cell to load the data. In every step, predict first, then run the cell, then read the output, then change one thing. '
                         'The checks turn from NOT YET to OK when your answer is right. Please do not skip the predictions.')))

    # 22 lab map
    S.append(dict(kind='steps', title='The lab has eight steps, and you keep a notebook with eight charts and three findings',
                  steps=[dict(head='1 Look', text='Load, shape, missing', icon='magnifier'), dict(head='2 Basket', text='Basket size histogram', icon='bag'), dict(head='3 Value', text='Order value histogram', icon='chart'), dict(head='4 Scatter', text='Hue and r', icon='pin'),
                         dict(head='5 Box, bars', text='Box plot, bar chart', icon='people'), dict(head='6 Count, rate', text='Returns by branch', icon='calculator'), dict(head='7 Season', text='Revenue by month', icon='calendar'), dict(head='8 Write', text='Three findings', icon='notebook')], highlight=None,
                  caption='Twenty automatic checks. In each step: predict, run, read, change.',
                  notes=('Here is the map of the lab. Step one, load the orders and look: the shape and the missing values. Step two, build the basket size and draw its histogram. Step three, draw the order value histogram with the mean and the median. '
                         'Step four, draw the scatter plot with hue and find the correlation. Step five, draw the box plot by payment method and the bar chart by branch. '
                         'Step six is the one to enjoy: count the returns and the rate for each branch, and find the reversal. Step seven, find the seasonal peak. Step eight, write three findings. '
                         'Every step has a predict prompt first. Please write your guess before you run the cell.')))

    # 23 check numbers
    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Records in orders, and missing customer_id', f'{n(F["rows"])} and {n(F["missing_cust"])}'], ['Median order value', f'{n(F["median"])} UGX'],
                        ['Median basket size, and its largest value', f'{int(F["basket_median"])} and {F["basket_max"]}'], ['Correlation of basket size and order value', f'{F["corr"]:.2f}'],
                        ['Median order value of Card orders', f'{n(pm["Card"])} UGX'], [f'Mean order value of branch {bmax}', f'{n(F["branch_mean"][bmax])} UGX'],
                        [f'Returns at {bt} and rate at {br_} (per 100 lines)', f'{int(rb.returns[bt])} and {rb.per_100[br_]:.2f}'], [f'December revenue over the other months, 2024 and 2025', f'{dr[2024]:.2f} and {dr[2025]:.2f}']],
                  widths=[7.4, 4.6], icons=['grid', 'coin', 'bag', 'pin', 'tag', 'shop', 'flag', 'calendar'], note='If your number differs, find the step that went wrong. Do not change a number to match.',
                  notes=('Use this table as your own self-check. Nobody marks it. If your numbers match, carry on. If one does not, stop and call me, because later steps use the earlier ones. '
                         'The most common cause is a merge that was not saved back into the orders variable, which leaves the basket size missing. Another is drawing the chart with the wrong column name. '
                         'Do not change a number to make it match. Find out why it is different. What does it mean if your correlation comes out at exactly one?')))

    # 24 errors
    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[['ValueError: Could not interpret value `branch` for `x`', 'The column name does not exist in the DataFrame.', 'Print orders.columns and copy the exact name, such as branch_id.'],
                        ['KeyError: basket_size', 'The merge result was not saved back.', 'Write orders = orders.merge(basket, on="order_id").'],
                        ['A chart with one tall bar and nothing else', 'A few huge orders stretch the axis.', 'Set the axis limit, and say how many records are hidden.'],
                        ['The histogram shows no gaps between sizes', 'Basket size counts whole lines, so bins should be whole numbers.', 'Add discrete=True.'],
                        ['NameError: name sns is not defined', 'The import cell was not run.', 'Run the first code cell again, then the cell that failed.']],
                  widths=[4.0, 4.0, 4.0], icons=['cross', 'cross', 'cross', 'cross', 'cross'],
                  notes=('Five messages you may meet. A value error that says it could not interpret a column name means the column does not exist, so print the columns and copy the exact name. '
                         'A key error on basket size means the merge result was not saved back into the orders variable. A chart with one tall bar and nothing else means a few huge orders have stretched the axis, so set a limit and say how many records are hidden. '
                         'A histogram with gaps and odd bars means you should add discrete equals True. And a name error on sns means the import cell was not run. Read the last line of the message first. It usually tells you the answer.')))

    # 25 exit check
    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[[f'Branch {bt} has the most returns. Does that make it the branch with the worst returns problem?', f'Not yet known. Divide by lines sold to get the rate: {bt} has {rb.per_100[bt]:.2f} per 100 lines, the lowest, and {br_} has {rb.per_100[br_]:.2f}, the highest.'],
                        ['Which chart answers "do two numeric variables move together?", and which seaborn function draws it?', 'A scatter plot, drawn by sns.scatterplot. The correlation r puts a number on it.'],
                        ['Write the three parts of a finding.', 'A number, a comparison and a limit.']],
                  widths=[5.6, 6.4], icons=['shop', 'pin', 'notebook'],
                  notes=('Last, the exit check. Write your answers in your notes before you look at mine. One, a branch has the most returns. Does that make it the branch with the worst problem? '
                         'Two, which chart answers whether two numeric variables move together, and which seaborn function draws it? Three, write the three parts of a finding. '
                         'The short answers are on the slide. If you got all three, you are ready for Session 12. If one surprised you, look at that step of your notebook again tonight.')))

    # facilitator
    sess['facilitator'] = dict(
        prep=['Open the deck and the Colab notebook before anyone arrives. Share the data.zip link or the upload step.',
              'Run the solution notebook once in Colab. Charts here were drawn with matplotlib 3.10 and seaborn 0.13; older seaborn versions do not accept err_kws or linecolor, so check the Colab version.',
              'Write the check table (the slide titled Check your numbers) on the board before the lab.',
              'Concepts run with laptops closed. Ask learners to open Colab only after the Part 2 divider.',
              'All data is fictional and generated. orders.csv is a 5 percent sample of till orders.'],
        misconceptions=[('The branch with the most returns has the worst problem', f'A count favours big branches. Divide by lines sold: {bt} is last by rate and {br_} is first.'),
                        ('The December peak means customers spend more', f'Order value barely moved ({n(F["aov_dec"][2024])} against {n(F["aov_other"])}). The number of orders rose.'),
                        ('A bar chart shows that branches differ', 'The bars are means with wide confidence intervals that overlap. Do not claim a difference without a test (Session 12).'),
                        ('Correlation 0.3 means one thing causes the other', 'It means a modest association. Basket size is part of how order value is built, and other variables matter.'),
                        ('Hiding outliers with an axis limit is the same as deleting them', 'The records are still in the data. A limit only changes the picture, so say how many are hidden.')],
        probes=[('Why is the mean order value larger than the median?', 'The distribution is right-skewed: a few very large orders pull the mean up.'),
                ('What is the difference between a Figure and an Axes?', 'The Figure is the whole page. The Axes is the plot area on the page.'),
                ('What does hue do in seaborn?', 'It colours the marks by the values of a categorical variable.'),
                ('What is the denominator of the returns rate?', 'The lines sold in that branch.'),
                ('Why did we draw each year as its own line?', 'To compare the same months across years and see the repeating pattern.'),
                ('How many Decembers do we have, and why does it matter?', 'Two. A seasonal claim from two repeats is weak, so state the limit.')],
        lab_steps=[('Step 1: load and look', f'{n(F["rows"])} orders, {n(F["missing_cust"])} missing customer_id. Watch for a missing parse_dates.'),
                   ('Step 2: basket size and histogram', f'Median basket {int(F["basket_median"])}. The merge must be saved back to orders.'),
                   ('Step 3: scatter, hue and r', f'r = {F["corr"]:.2f}. Learners often write corr with the wrong columns.'),
                   ('Step 4: box plot and barplot', f'Medians near {n(pm["Card"])}. Branch {bmax} mean {n(F["branch_mean"][bmax])}. Ask what the error bars say.'),
                   ('Step 5: count and rate', f'{bt}: {int(rb.returns[bt])} returns. {br_}: {rb.per_100[br_]:.2f} per 100 lines. The reversal is the main point.'),
                   ('Step 6: season and findings', f'Peak is December. Ratios {dr[2024]:.2f} and {dr[2025]:.2f}. Each finding needs a number, a comparison and a limit.')],
        rescue=['If the concepts run over, shorten the chart habits and the use at work slides.', 'If only 30 minutes of lab remain, do steps 1, 2, 5 and 6 and set steps 3 and 4 as homework.',
                'If a learner has no Colab, matplotlib and seaborn run in any Jupyter environment with pandas.', 'If a learner has no laptop, pair them with a neighbour: one types, one predicts aloud.'],
        after=['Share the deck and the solution notebook again for learners who were absent.', 'Ask each learner to save the notebook and bring one question about a gap between two groups to Session 12.', 'Note any question you could not answer and open the next session with it.'],
        lab_answer_key=[['Step 2 PREDICT: will the median basket be bigger or smaller than the mean?', f'Smaller: {int(F["basket_median"])} against {F["basket_mean"]:.2f}. A few large baskets pull the mean up.'],
                        ['Step 3 READ: what does r = 0.30 tell you?', 'A modest positive link: bigger baskets tend to cost more, but other things matter too.'],
                        ['Step 4 READ: do the branch bars show a real difference?', 'No. The error bars overlap, so the gaps may be luck.'],
                        ['Step 5 PREDICT: will the branch with most returns also have the highest rate?', f'No. {bt} has the most ({int(rb.returns[bt])}) and the lowest rate ({rb.per_100[bt]:.2f}). {br_} has the highest ({rb.per_100[br_]:.2f}).'],
                        ['Step 5 CHANGE: use the count of returns per 100 orders instead of lines.', 'The ranking can differ again, because the denominator changed. State which denominator you used.'],
                        ['Step 6 READ: what causes the December peak?', f'More orders: {n(F["dec_orders"][2024])} in December 2024 against an average of {n(F["orders_other_mean"])} in other months. The average order value is about the same.']])
    return sess


GOLD_C = '#E0BE36'
