"""Session 11 lab notebook: Exploring and visualising with Python. Expected values come from content/f11_facts.py (pandas on the real files)."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[2] / 'kit'))
import nb as NB  # noqa: E402

_spec = importlib.util.spec_from_file_location('f11_facts', HERE.parents[1] / 'f11_facts.py')
f11 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(f11)

TITLE = 'Exploring and visualising'


def build(solution):
    F = f11.facts()
    rb = F['rb']
    bt, br_ = F['top_count'], F['top_rate']
    dr = F['dec_ratio'][2024]
    sol = solution

    def pick(answer, hint, var=None):
        """The model answer in the solution; a blank with a one-line hint for the learner."""
        return answer if sol else (f'{var} = None  # your code here: {hint}' if var else f'# your code here: {hint}')

    nb = NB.Notebook()
    nb.md('# Session 11 lab: Exploring and visualising Lakeside Mart\n\n'
          'You will run the six-step EDA routine on the Lakeside Mart orders, draw eight charts with matplotlib and seaborn, and write three findings.\n\n'
          'Rhythm for every step: **PREDICT** (write your guess), **RUN** the cell, **READ** the output, **CHANGE** one thing. '
          'Cells with `# your code here` are yours to fill. The check cells say OK when your answer is right.')
    nb.data_setup()
    nb.check_setup()
    nb.code('import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nsns.set_theme()   # a clean default look for every chart')

    # step 1
    nb.step(1, 'Look at the new file', 'Always begin with the shape, the data types and the missing values (EDA step 1).')
    nb.predict('How many orders are in orders.csv? Which variable has missing values, and what does a missing customer_id mean?')
    nb.code("orders = pd.read_csv('orders.csv', parse_dates=['order_date'])\nlines = pd.read_csv('order_lines.csv')\nreturns = pd.read_csv('returns.csv')\nbranches = pd.read_csv('branches.csv')\n"
            "print(orders.shape)\nprint(orders.dtypes)\norders.isna().sum()")
    nb.read('Which variable has missing values? Walk-in shoppers have no loyalty number, so what does the blank mean?')
    nb.code(pick("n_missing = orders['customer_id'].isna().sum()", 'count the missing values of customer_id', 'n_missing') +
            f"\ncheck('records in orders', len(orders), {F['rows']})\ncheck('missing customer_id', n_missing, {F['missing_cust']})")
    nb.change('Print orders.isna().mean() * 100. What share of orders is missing a customer_id?')

    # step 2
    nb.step(2, 'One variable: basket size', 'Count the lines on each order (the basket size), attach it to orders, and draw its histogram (EDA step 3).')
    nb.predict('Will the median basket be bigger than, smaller than or equal to the mean basket? Why?')
    nb.code(pick("basket = lines.groupby('order_id').size().rename('basket_size')\norders = orders.merge(basket, on='order_id', how='left', validate='m:1')   # run once; to run again, reload orders first\nmedian_basket = orders['basket_size'].median()\nmean_basket = orders['basket_size'].mean()\nprint(orders.shape, median_basket, round(mean_basket, 2))",
                 'count the lines on each order with groupby and size, name it basket_size, merge it into orders on order_id; then find the median and the mean of basket_size') +
            ("" if sol else "\nmedian_basket = None"))
    nb.code(pick("ax = sns.histplot(data=orders, x='basket_size', discrete=True)\nax.set_title('Lines per order')\nax.set_xlabel('Basket size (lines)')\nax.set_ylabel('Number of orders')\nplt.show()",
                 'draw sns.histplot of basket_size with discrete=True; add a title and axis labels', 'ax') +
            f"\ncheck('orders has 8 variables', orders.shape[1], {F['ob_shape'][1]})\ncheck('median basket size', median_basket, {F['basket_median']})\n"
            "check('basket histogram drawn', ax is not None and len(ax.patches) > 5, 1)")
    nb.read('The tall bar is at one line. What share of orders have only one line? Is the distribution skewed to the right?')
    nb.change('Replace discrete=True with binwidth=5. What does the chart hide?')

    # step 3
    nb.step(3, 'One variable: order value', 'Summarise the order value and draw its histogram, with the mean and the median marked (EDA steps 2 and 3).')
    nb.predict('The mean order value is about twice the median. Which one is the typical order, and why?')
    nb.code(pick("mean_value = orders['order_value_ugx'].mean()\nmedian_value = orders['order_value_ugx'].median()\nn_hidden = (orders['order_value_ugx'] > 200000).sum()\nprint(orders['order_value_ugx'].describe().round(0))",
                 'mean, median, and how many orders are above 200,000 UGX (these will be off the chart)') +
            ("" if sol else "\nmean_value = median_value = n_hidden = None"))
    nb.code(pick("ax = sns.histplot(data=orders, x='order_value_ugx', binwidth=10000, binrange=(0, 200000))\nax.axvline(median_value, color='gold', lw=3, label='median')\nax.axvline(mean_value, color='red', lw=3, ls='--', label='mean')\nax.legend()\nax.set_title('Order value, orders up to 200,000 UGX')\nax.set_xlabel('Order value (UGX)')\nplt.show()",
                 'sns.histplot of order_value_ugx with binwidth=10000 and binrange=(0, 200000), then axvline for the median and the mean', 'ax') +
            f"\ncheck('mean order value', mean_value, {F['mean']:.2f}, 1)\ncheck('median order value', median_value, {F['median']})\ncheck('orders above 200,000 UGX', n_hidden, {F['above200k']})")
    nb.read('Is the mean to the left or to the right of the median? What does that tell you about the shape?')
    nb.change('Change binwidth to 5000. Does the shape change, or only the detail?')

    # step 4
    nb.step(4, 'Two variables: basket size and order value', 'Draw a scatter plot coloured by payment method with hue, and find the correlation (EDA step 4).')
    nb.predict('Will bigger baskets cost more? Will the correlation be near 0, near 0.3 or near 0.9?')
    nb.code(pick("sample = orders.sample(2000, random_state=1)\nax = sns.scatterplot(data=sample, x='basket_size', y='order_value_ugx', hue='payment_method', alpha=0.6)\nax.set_ylim(0, 300000)\nax.set_title('2,000 orders: basket size and order value')\nplt.show()\nr = orders['basket_size'].corr(orders['order_value_ugx'])\nprint(round(r, 2))",
                 'a random sample of 2000 orders (random_state=1), sns.scatterplot with hue=payment_method, then the correlation of basket_size and order_value_ugx on the whole orders table', 'ax') +
            ("" if sol else "\nr = None") +
            f"\ncheck('correlation r', r, {F['corr']:.4f}, 0.01)\ncheck('scatter drawn', ax is not None and len(ax.collections) > 0, 1)")
    nb.read('Do the three colours form separate clouds? What does r tell you, and what does it not tell you?')
    nb.change('Change hue to promo_week. Does the promotion week show up as a separate cloud?')

    # step 5
    nb.step(5, 'Groups: box plot and bar chart', 'Compare order value across payment methods with a box plot, and across branches with a bar chart (EDA step 5).')
    nb.predict('Will the three payment methods have similar medians? Will one branch have a clearly higher mean order value than the others?')
    nb.code(pick("ax = sns.boxplot(data=orders, x='payment_method', y='order_value_ugx', showfliers=False)\nax.set_title('Order value by payment method')\nplt.show()\nmedian_card = orders[orders['payment_method'] == 'Card']['order_value_ugx'].median()\nprint(orders.groupby('payment_method')['order_value_ugx'].median())",
                 'sns.boxplot of order_value_ugx by payment_method with showfliers=False; then the median order value of Card orders', 'ax') +
            ("" if sol else "\nmedian_card = None") +
            f"\ncheck('median Card order', median_card, {F['pay_median']['Card']})\ncheck('box plot drawn', ax is not None and len(ax.patches) + len(ax.lines) > 3, 1)")
    nb.code(pick("ax = sns.barplot(data=orders.sort_values('branch_id'), x='branch_id', y='order_value_ugx', errorbar=('ci', 95))\nax.set_title('Mean order value by branch, with 95 percent interval')\nplt.show()\nmean_b04 = orders[orders['branch_id'] == 'B04']['order_value_ugx'].mean()\nprint(round(mean_b04))",
                 'sns.barplot of order_value_ugx by branch_id (the default shows the mean with a 95 percent interval); then the mean order value of branch B04', 'ax') +
            ("" if sol else "\nmean_b04 = None") +
            f"\ncheck('mean order value of B04', mean_b04, {F['branch_mean']['B04']:.2f}, 1)")
    nb.read('Look at the black lines on the bars. Do they overlap between branches? Would you tell a manager that one branch spends more per order?')
    nb.change('Change the box plot y variable to basket_size. Do payment methods differ in basket size?')

    # step 6
    nb.step(6, 'Count and rate: which branch has a returns problem?', 'Count the returns for each branch, divide by the lines sold to get a rate, and compare the two charts (EDA step 5).')
    nb.predict(f'Will the branch with the most returns also have the highest rate of returns per 100 lines sold?')
    nb.code(pick("orders_branch = orders[['order_id', 'branch_id']]\nreturns_b = returns.merge(orders_branch, on='order_id', how='left', validate='m:1')\nlines_b = lines.merge(orders_branch, on='order_id', how='left', validate='m:1')\ncount = returns_b.groupby('branch_id').size()\nsold = lines_b.groupby('branch_id').size()\nrate = (count / sold * 100).round(2)\ntop_count = count.idxmax()\ntop_rate = rate.idxmax()\nprint(count.max(), top_count, rate.max(), top_rate)",
                 'attach the branch to returns and to lines; count each by branch into count and sold; rate = count / sold * 100; then idxmax for top_count and top_rate') +
            ("" if sol else "\ncount = rate = top_count = top_rate = None"))
    nb.code(pick("fig, axes = plt.subplots(1, 2, figsize=(11, 4))\naxes[0].bar(count.index, count.values)\naxes[0].set_title('Number of returns')\naxes[1].bar(rate.index, rate.values)\naxes[1].set_title('Returns per 100 lines sold')\nplt.show()",
                 'two bar charts side by side: count on axes[0], rate on axes[1], each with a title', 'axes') +
            f"\ncheck('returns at {bt}', count['{bt}'] if count is not None else None, {int(rb.returns[bt])})\ncheck('rate at {br_} per 100 lines', rate['{br_}'] if rate is not None else None, {rb.per_100[br_]:.2f}, 0.01)\n"
            f"check('top branch by count is {bt}', top_count == '{bt}', 1)\ncheck('top branch by rate is {br_}', top_rate == '{br_}', 1)")
    nb.read('Do the two charts name the same branch? Which chart would you show to a manager, and why?')
    nb.change('Divide the returns by the number of ORDERS in each branch instead of the lines. Does the ranking change?')

    # step 7
    nb.step(7, 'Seasonality: revenue by month', 'Total the revenue for each month, draw each year as its own line, and measure the December peak.')
    nb.predict('Which month has the highest revenue? Is it the same in 2024 and 2025?')
    nb.code(pick("orders['year'] = orders['order_date'].dt.year\norders['month'] = orders['order_date'].dt.month\nmonthly = orders.groupby(['year', 'month'])['order_value_ugx'].sum().div(1e6).reset_index(name='revenue_m')\n"
                 "other = monthly[monthly['month'] != 12]['revenue_m'].mean()\ndec_2024 = monthly[(monthly['year'] == 2024) & (monthly['month'] == 12)]['revenue_m'].iloc[0]\ndec_ratio_2024 = dec_2024 / other\nprint(round(other, 1), round(dec_2024, 1), round(dec_ratio_2024, 2))",
                 'add year and month variables; monthly revenue in millions; the mean of the months that are not December; December 2024 divided by that mean') +
            ("" if sol else "\nmonthly = dec_ratio_2024 = None"))
    nb.code(pick("ax = sns.lineplot(data=monthly.assign(year=monthly['year'].astype(str)), x='month', y='revenue_m', hue='year', marker='o')\nax.set_title('Revenue by month')\nax.set_ylabel('UGX millions')\nplt.show()",
                 'sns.lineplot of revenue_m by month with hue for the year (turn year into text first) and marker="o"', 'ax') +
            f"\ncheck('December 2024 over the other months', dec_ratio_2024, {dr:.4f}, 0.01)\ncheck('line chart drawn', ax is not None and len(ax.lines) >= 2, 1)")
    nb.read('Both years peak in December. Is it because customers spend more per order, or because there are more orders? Check with orders.groupby("month").size().')
    nb.change('Draw the number of orders by month instead of the revenue. Does the December peak stay?')

    # step 8
    nb.step(8, 'Write three findings', 'A finding states a number, a comparison and a limit. Write one for the returns, one for December and one for basket size.')
    nb.predict('What is the limit of each finding? Think about the sample, the two years and what a correlation cannot show.')
    fnd = (f"findings = [\n"
           f"    '{F['names'][bt]} has the most returns ({int(rb.returns[bt])}) but the lowest rate, {rb.per_100[bt]:.2f} per 100 lines sold, against {F['rate_all']:.2f} overall. Limit: a sample of orders over two years.',\n"
           f"    'December revenue was {dr:.2f} times the average of the other months in 2024, and {F['dec_ratio'][2025]:.2f} times in 2025. Limit: only two Decembers.',\n"
           f"    'Basket size and order value have a correlation of {F['corr']:.2f}, a modest link. Limit: correlation does not show cause.',\n]\n"
           "for f in findings:\n    print(f)")
    nb.code(fnd if sol else "findings = [\n    'Your turn: the returns finding',\n    'Your turn: the December finding',\n    'Your turn: the basket size finding',\n]\n"
            "for f in findings:\n    print(f)\n# Replace each text with a sentence that has a number, a comparison and a limit.")
    nb.code("done = len(findings) == 3 and all(any(ch.isdigit() for ch in f) for f in findings) and not any('Your turn' in f for f in findings)\n"
            "check('three findings, each with a number', done, 1)\nshow_checks()")
    nb.read('Read each finding aloud. Could a manager check the number, see the comparison, and see what the data cannot tell?')
    nb.change('Write one more finding about the box plot by payment method. What is its limit?')
    nb.md('**Hand-over to Excel or Power BI (optional).** The next cell saves a chart and a table that Excel or Power BI can open.')
    nb.code(pick("fig = ax.get_figure()\nfig.savefig('revenue_by_month.png', dpi=200)\nmonthly.to_excel('revenue_by_month.xlsx', index=False)\nprint('saved: revenue_by_month.png and revenue_by_month.xlsx')",
                 'fig = ax.get_figure(), then fig.savefig("revenue_by_month.png", dpi=200) and monthly.to_excel("revenue_by_month.xlsx", index=False)'))
    nb.md('**You keep this notebook.** Save a copy to your Drive or download it as .ipynb. It holds eight charts and three findings. Next session: is a difference between two groups real, or luck?')
    return nb
