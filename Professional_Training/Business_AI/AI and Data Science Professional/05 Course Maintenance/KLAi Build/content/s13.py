"""Session 13: Regression, explaining and predicting a number (Project milestone 2). Python lab: content/labs/s13_nb.py.

Every number on a slide, in a note or in the notebook checks comes from s13_facts.facts(): numpy least squares on the real branch_weeks.csv.
statsmodels is not installed in the build sandbox, so no statsmodels output is shown; the slides say the library gives the same coefficients.
"""
import importlib.util
from pathlib import Path

import numpy as np

_p = Path(__file__).resolve().parent / 's13_facts.py'
_spec = importlib.util.spec_from_file_location('s13_facts', _p)
FX = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(FX)


def n0(x):
    return f'{int(round(x)):,}'


def build():
    F = FX.facts()
    bw = F['bw']
    m1, m3, mb = F['m1'], F['m3'], F['mb']
    b0, b1 = m1['b']
    c0, c1, c2, c3 = m3['b']
    ci = F['ci']
    se = m3['se']
    X3, y = F['X3'], F['y']
    fit3 = m3['fit']
    n = F['n']
    r0 = F['rec0']
    th = F['res_sd_thirds']
    levels = F['levels']
    assert (F['trap_cols'], F['trap_rank']) == (9, 8) and levels[0] == 'B01' and len(levels) == 8
    assert round(m3['r2'], 3) == 0.795 and round(F['r'], 2) == 0.84 and F['n_te'] == 208 and F['n_tr'] == 624
    sess = dict(
        num=13, block='Module C: Analyse and explain', short_title='Regression',
        title='Regression: explaining and predicting a number',
        question='How much does one thing change when another changes, and how well can a model predict it?',
        outcomes=['Fit a simple and a multiple linear regression by ordinary least squares, and read each coefficient as a sentence a manager can use',
                  'Judge a model with residuals, R squared and a residual plot, and put a category into a model with indicator variables',
                  'Say what a regression can predict, what it can explain, and what it cannot prove'],
        outcome_icons=['chart', 'magnifier', 'shield'],
        outcome_note=('Here is what you can do by the end of today. You can fit a regression line, and a regression with several predictors, by ordinary least squares, and then read each coefficient as one plain sentence for a manager. '
                      'You can judge the model with residuals, R squared and a residual plot, and you can put a category such as the branch into a model with indicator variables. '
                      'And you can say what the model predicts, what it explains, and what it cannot prove. Today is also Project milestone 2, a one page analysis report that you show me for feedback, and you write your project question before you leave.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: picture, plain words, one example by hand'), (10, 'Break'), (45, 'Lab: predict, run, read, change'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: concepts first, then a Python regression lab',
        plan_caption='Ideas with pictures first. Then you open the notebook, fit the model and write your one page report.',
        plan_note=('We have two hours. The first ten minutes bring back Session 12 and set the question for today. Then forty-five minutes of concepts with no laptops open, so you can follow the pictures. '
                   'After a ten minute break we open a Colab notebook for the forty-five minute lab. In every step you predict first, run the cell, read the output and change one thing. '
                   'The last ten minutes are an exit check and what you keep, including your one page report for Project milestone 2.'),
        recall_from='Session 12',
        recall=[('A 95 percent confidence interval for a lift includes zero. What do you tell the manager?', 'We cannot tell yet whether the lift is more than sampling variability. The data are compatible with a gain, with no change and with a loss.'),
                ('A p-value is tiny. Does that make the effect big?', 'No. The p-value says a gap this size is unlikely if nothing is going on. The effect size says whether the gap matters.'),
                ('What does the standard error measure?', 'How much a statistic, such as a sample mean, varies from one sample to the next. It shrinks as the sample grows.')],
        words=[('Regression (linear regression model)', 'A model that predicts a numeric target as an intercept plus a weighted sum of predictors. Ordinary least squares (OLS) finds the weights.'),
               ('Coefficient and intercept', 'The coefficient is the change in the prediction for one more unit of a predictor, with the other predictors held fixed. The intercept is the prediction when every predictor is 0.'),
               ('Residual (prediction error)', 'Actual value minus predicted value for one record. OLS minimises the sum of the squared residuals.'),
               ('R squared (coefficient of determination)', 'The share of the variation in the target that the model accounts for, from 0 to 1.'),
               ('Indicator variable (dummy variable)', 'A variable that is 1 when a record belongs to a category and 0 otherwise. One-hot encoding makes one for each level.')],
        word_icons=['chart', 'calculator', 'magnifier', 'check', 'flag'],
        words_note=('Five words for today. A regression, or linear regression model, predicts a number from a weighted sum of predictors, and ordinary least squares finds the weights. '
                    'A coefficient says how much the prediction changes for one more unit of a predictor, and the intercept is the prediction when every predictor is zero. '
                    'A residual is the actual value minus the predicted value. R squared is the share of the variation the model accounts for. And an indicator variable, also called a dummy variable, marks a category with one or zero.'),
        keep='Keep your notebook and regression_summary.csv, and write your one page analysis report: the question, the model, three coefficients as sentences, R squared, the residual check and what the model cannot prove.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab files', value='Notebook and summary file'), dict(label='Your report', value='One page, Project milestone 2'), dict(label='Next session', value='Machine learning')]),
        keep_title='Save your notebook, your summary file and your report',
        next='Session 14: Machine learning, the workflow. We predict loan default with a train and test split.', next_label='Next session',
        keep_note=('Before you go, save the notebook and the file regression summary dot csv. Together with your one page report they are your Project milestone 2. You show it to me for feedback, and nobody scores it. '
                   'The report states the question, the model, three coefficients written as sentences, the R squared, what the residual plot showed, and what the model cannot prove. '
                   'Also write your project question on the last line. Next session we use the same train and test ideas to predict loan default, which is a yes or no instead of a number.'),
        cover_note=('Welcome back. Over the last twelve sessions you learned to load data, clean it, query it, chart it and test whether a gap is more than luck. Today the question gets bigger. '
                    'When footfall rises, rainfall changes or a promotion runs, how many more orders does a branch get? That is regression. You will fit a model to the Lakeside Mart weekly data, '
                    'read every number in it as a sentence, check where it fails, and say what it does not prove.'),
        use_at_work='Fit, read and check a regression, and report what it can and cannot support.',
        slides=[])
    S = sess['slides']

    # 1 answers
    S.append(dict(kind='table', title='Answers to the three questions from Session 12', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in sess['recall']], widths=[5.2, 6.8], icons=['pin', 'chart', 'calculator'],
                  notes=('Here are the answers to the three warm-up questions. If the interval for a lift includes zero, you tell the manager that the data cannot yet separate a gain from no change or a small loss. '
                         'A tiny p-value says a gap this big would be rare if nothing were going on, but only the effect size says whether the gap is big enough to matter. And the standard error measures how much a statistic such as a sample mean varies from sample to sample. '
                         'Every regression coefficient also comes with a standard error and an interval, so today you use all three ideas again. Which one needed the most thought?')))

    # 2 the cloud and the line
    S.append(dict(kind='idea', title='Regression fits a line through a cloud: weekly orders against footfall',
                  visual=dict(kind='scatter', points=[[float(a), float(b)] for a, b in zip(bw.footfall, bw.orders)], xlabel='footfall: people through the door in a week', ylabel='orders in the week',
                              line=[float(b0), float(b1)], line_label='fitted line', dot=0.035, size=15),
                  alt='Scatter plot of 832 branch weeks with an upward fitted line',
                  lead='A scatter plot has one dot for each record: one branch in one week.',
                  points=[f'{n} dots, one for each record.', 'Along the bottom: footfall, the predictor (independent variable).', 'Up the side: orders, the target (dependent variable).'],
                  notes=(f'Today we answer a question you meet at work all the time. When one thing goes up, how much does another change? In Excel you would draw a scatter chart and add a trendline. That trendline is a regression. '
                         f'Each dot is one record, one Lakeside Mart branch in one week, so there are {n} dots. Footfall, the count at the door, runs along the bottom. It is the predictor, also called the independent variable or the feature. '
                         f'Orders run up the side. That is the target, also called the dependent variable or the response. The red line is the fitted line, the model. Busy weeks sit high and to the right, and the correlation is {F["r"]:.2f}. '
                         'What would the line tell a manager that the correlation alone does not?')))

    # 3 three vocabularies
    S.append(dict(kind='table', title='The Excel word, the statistics word and the machine learning word for each part',
                  headers=['In Excel', 'In statistics', 'In machine learning'],
                  rows=[['Trendline on a scatter chart', 'Linear regression model', 'Model (regressor)'], ['The x column', 'Independent variable (predictor)', 'Feature'], ['The y column', 'Dependent variable (response)', 'Target'],
                        ['SLOPE and INTERCEPT', 'Coefficient and intercept', 'Parameters (weights and bias)'], ['RSQ, or R2 on the trendline', 'R squared', 'Score (model.score)'], ['A row', 'Observation', 'Instance (record)']],
                  widths=[3.6, 4.4, 4.0], icons=['chart', 'tag', 'flag', 'calculator', 'check', 'notebook'],
                  note='LINEST is the Excel function that fits several predictors at once. This course uses predictor and target from here on.',
                  notes=('You already know every part of a regression from Excel, so here is the translation. The trendline on a scatter chart is a linear regression model. The x column is the independent variable, also called the predictor, and in machine learning the feature. '
                         'The y column is the dependent variable, also called the response, and in machine learning the target. SLOPE and INTERCEPT give the coefficient and the intercept, which machine learning calls the weights and the bias. '
                         'RSQ gives R squared. Excel also has LINEST, which fits several predictors at once. From here on I say predictor and target. Which of these words was new to you?')))

    # 4 simple regression formula
    S.append(dict(kind='formula', title='Simple linear regression is a formula with two numbers: an intercept and a coefficient',
                  formulas=[('Simple linear regression', r'$\hat{y} = b_0 + b_1\,x$'), ('Our fitted model', r'$\hat{y} = ' + f'{b0:.2f} + {b1:.4f}' + r'\,x$')],
                  symbols=[['y-hat', 'The predicted target.', 'orders in a week'], ['x', 'The predictor.', f'footfall, {F["ff_min"]:,} to {F["ff_max"]:,} people'],
                           ['b0 (intercept)', 'The prediction when x is 0.', f'{b0:.2f} orders'], ['b1 (coefficient)', 'The change in the prediction for one more unit of x.', f'{b1:.4f} orders per person']],
                  size=26, note=f'1,000 more people at the door goes with about {b1 * 1000:.1f} more orders. R squared is {m1["r2"]:.3f}, the correlation {F["r"]:.2f} squared.',
                  notes=(f'The fitted line is a formula. The predicted target, y hat, equals b zero plus b one times x. B zero is the intercept, the prediction when the predictor is zero. B one is the coefficient, the slope: how much the prediction changes for one more unit of x. '
                         f'For our data b zero is {b0:.2f} and b one is {b1:.4f} orders per person. That is a small number, so we multiply by a thousand: a thousand more people at the door goes with about {b1 * 1000:.1f} more orders. '
                         f'With footfall alone, R squared is {m1["r2"]:.3f}, which equals the correlation squared. Why would a manager prefer the sentence about a thousand people?')))

    # 5 residuals
    S.append(dict(kind='idea', title='A residual is the actual value minus the predicted value',
                  visual=dict(kind='scatter', points=[[float(bw.footfall[i]), float(bw.orders[i])] for i in F['idx25']], xlabel='footfall', ylabel='orders', line=[float(b0), float(b1)], residuals=True, mark=[0], dot=0.075, size=15),
                  alt='Twenty-five weekly records with red segments joining each dot to the fitted line',
                  lead='Each red segment is one residual: how far the line misses one record.',
                  points=['Residual: e = y minus y-hat. Above the line it is positive.', f'Gold dot: {r0["branch"]}, week of {r0["week"]}. Actual {r0["orders"]} orders, predicted {r0["fit"]:.1f}, residual {r0["res"]:+.1f}.', '25 of the 832 records are drawn.'],
                  notes=(f'A model is never perfect, so we measure how far it misses. The gap between a dot and the line is the residual, also called the prediction error. It is the actual value minus the predicted value. A dot above the line gives a positive residual. '
                         f'The gold dot is the first record in the file: branch {r0["branch"]}, the week of {r0["week"]}, with {r0["ff"]:,} people. The line predicts {r0["fit"]:.1f} orders, the actual number was {r0["orders"]}, so the residual is {r0["res"]:+.1f}. '
                         'I drew only twenty-five of the eight hundred and thirty-two records so you can see the segments. Is the gold dot above or below the line?')))

    # 6 OLS
    S.append(dict(kind='formula', title='Ordinary least squares picks the line with the smallest sum of squared residuals',
                  formulas=[('Residual of record i', r'$e_i = y_i - \hat{y}_i$'), ('Ordinary least squares', r'$\min_{b_0,\ b_1}\ \sum_{i=1}^{n} e_i^{2}$')],
                  symbols=[['e_i', 'The residual of record i.', f'{r0["res"]:+.1f} for record 1'], ['y_i and y-hat_i', 'Actual and predicted target of record i.', f'{r0["orders"]} and {r0["fit"]:.1f}'],
                           ['n', 'The number of records.', f'{n}'], ['sum of e_i squared', 'Add the squared residuals of all n records.', f'{n0(m1["sse"])} for our line']],
                  size=22, note=f'A rival line with slope {F["alt_slope"]} (and its own best intercept) gives a sum of {n0(F["alt_sse"])}. OLS finds the smallest sum: {n0(m1["sse"])}.',
                  notes=(f'How does the computer choose the line? Try any line through the cloud. Every dot sits above or below it, and each gap is a residual. We square every residual so that misses above and below both count, and we add them up. That total is the sum of squared residuals. '
                         f'The method called ordinary least squares, or OLS, finds the b zero and b one that make this sum as small as possible. A rival line with a slope of {F["alt_slope"]}, and its own best intercept, gives {n0(F["alt_sse"])}. The OLS line gives {n0(m1["sse"])}, the smallest possible. '
                         'Excel does the same thing when you add a trendline. Why do we square the residuals instead of just adding them?')))

    # 7 multiple regression
    S.append(dict(kind='formula', title='Multiple linear regression adds predictors: footfall, promotion and rainfall',
                  formulas=[('Multiple linear regression', r'$\hat{y} = b_0 + b_1 x_1 + b_2 x_2 + b_3 x_3$'), ('Our fitted model', r'$\hat{y} = ' + f'{c0:.2f} + {c1:.4f}' + r'\,x_1 + ' + f'{c2:.2f}' + r'\,x_2 - ' + f'{abs(c3):.3f}' + r'\,x_3$')],
                  symbols=[['x1', 'footfall, people through the door.', f'{c1:.4f} orders per person'], ['x2', 'promo_on: 1 in a promotion week, 0 otherwise.', f'{c2:.2f} orders'],
                           ['x3', 'rainfall_mm, millimetres of rain in the week.', f'{c3:.3f} orders per mm'], ['b0', 'The intercept.', f'{c0:.2f} orders']],
                  size=24, note='One least squares rule finds all four numbers. statsmodels and scikit-learn give the same numbers as NumPy.',
                  notes=(f'Real weeks have more than one influence, so we add predictors. This is multiple linear regression: the prediction is an intercept plus one coefficient for each predictor. Multivariate means several targets, so we say multiple. '
                         f'Our model has three predictors: footfall, promo on, which is one in a promotion week, and rainfall in millimetres. Ordinary least squares finds all four numbers together: {c0:.2f}, {c1:.4f}, {c2:.2f} and {c3:.3f}. '
                         'NumPy solves them with matrix algebra, and libraries such as statsmodels and scikit-learn return the same numbers. In your own words, what does the minus sign on rainfall say?')))

    # 8 coefficients as sentences
    S.append(dict(kind='table', title='Read each coefficient as one sentence, with its 95 percent confidence interval',
                  headers=['Term', 'Coefficient', '95% interval', 'As a sentence'],
                  rows=[['Intercept', f'{c0:.2f}', f'{ci[0][0]:.2f} to {ci[0][1]:.2f}', f'The starting level. No week has zero footfall (the minimum is {F["ff_min"]}), so do not read it alone.'],
                        ['footfall', f'{c1:.4f}', f'{ci[1][0]:.4f} to {ci[1][1]:.4f}', f'1,000 more people at the door goes with {c1 * 1000:.1f} more orders, other predictors held fixed.'],
                        ['promo_on', f'{c2:.2f}', f'{ci[2][0]:.2f} to {ci[2][1]:.2f}', f'A promotion week has {c2:.1f} more orders than a week without one at the same footfall and rain.'],
                        ['rainfall_mm', f'{c3:.3f}', f'{ci[3][0]:.3f} to {ci[3][1]:.3f}', f'10 mm more rain goes with {abs(c3) * 10:.1f} fewer orders, other predictors held fixed.']],
                  widths=[1.9, 1.7, 2.7, 5.6], icons=['key', 'person', 'flag', 'rain'], note=f'Interval = coefficient plus or minus {F["tcrit"]:.3f} standard errors (Student t, {m3["n"] - m3["k"]} degrees of freedom).',
                  notes=(f'Now the skill your manager cares about: reading each coefficient as a sentence. Footfall: a thousand more people at the door goes with {c1 * 1000:.1f} more orders, holding promotion and rain fixed. Holding the others fixed is part of the meaning, so always say it. '
                         f'Promotion: a promotion week has {c2:.1f} more orders than a week without one, at the same footfall and rain. Rainfall: ten millimetres more rain goes with {abs(c3) * 10:.1f} fewer orders. '
                         f'Each coefficient has a 95 percent confidence interval, built from its standard error as in Session 12. None of the intervals includes zero. Which sentence would you put on a slide for your manager?')))

    # 9 R squared
    S.append(dict(kind='formula', title='R squared is the share of the variation in the target that the model accounts for',
                  formulas=[('R squared', r'$R^{2} = 1 - \frac{\sum e_i^{2}}{\sum (y_i - \bar{y})^{2}}$'), ('Our model', r'$R^{2} = 1 - \frac{' + f'{n0(m3["sse"])}'.replace(',', '{,}') + r'}{' + f'{n0(m3["sst"])}'.replace(',', '{,}') + r'} = ' + f'{m3["r2"]:.3f}' + r'$')],
                  symbols=[['sum of e_i squared', 'Sum of squared residuals: what the model leaves unexplained.', n0(m3['sse'])], ['sum of (y_i - y-bar) squared', 'Total variation of the target around its mean y-bar.', n0(m3['sst'])],
                           ['Adjusted R squared', 'R squared with a penalty for each extra predictor.', f'{m3["adj"]:.3f}']],
                  size=18, note=f'Footfall alone gave {m1["r2"]:.3f}. RMSE ({m3["rmse"]:.1f} orders) is the typical miss, weighting big misses more.',
                  notes=(f'How good is the fit? R squared, also called the coefficient of determination, compares two totals. The top is the sum of squared residuals, what the model leaves unexplained, {n0(m3["sse"])}. The bottom is the total variation of the target around its mean, {n0(m3["sst"])}. '
                         f'One minus that ratio is {m3["r2"]:.3f}, so the model accounts for about {m3["r2"] * 100:.0f} percent of the variation in weekly orders. Adjusted R squared, {m3["adj"]:.3f}, penalises extra predictors. '
                         f'The root mean squared error, RMSE, is {m3["rmse"]:.1f} orders: the root of the mean squared residual, a typical size of a miss that weights big misses more. For comparison, the same predictors give R squared {F["sales_r2"]:.3f} for sales in shillings, because a few huge baskets add variation that footfall cannot explain. '
                         'What does an R squared of zero mean?')))

    # 10 indicator variables
    pk = F['pick']
    onehot_rows = [[str(r.week_start), str(r.branch_id)] for r in pk[:4]]
    S.append(dict(kind='wide', title='A category enters a regression as indicator (dummy) variables: one-hot encoding',
                  visual=dict(kind='ds_onehot', left_headers=['week_start', 'branch_id'], rows=onehot_rows, levels=levels, drop='B01'),
                  caption='promo_on is already an indicator variable. branch_id has 8 levels, so we make 8 columns and keep 7.',
                  notes=('A regression needs numbers, so a category such as the branch has to be turned into numbers. The standard way is an indicator variable, also called a dummy variable: a column that is one when the record belongs to a category and zero otherwise. '
                         'Making one such column for every level is called one-hot encoding. The promotion column is already an indicator. Branch has eight levels, so we get eight columns, and each record has a single one. '
                         'We keep only seven. The dropped level, B01, becomes the reference level, and the other seven coefficients compare each branch with B01. Why can we drop one column without losing any information?')))

    # 11 trap
    trap_rows = []
    for r in pk[:3]:
        ind = [('1' if r.branch_id == l else '0') for l in levels]
        trap_rows.append(['1'] + ind + [str(sum(int(v) for v in ind))])
    S.append(dict(kind='wide', title='Keep all eight indicators and the intercept and the model cannot be solved: the dummy variable trap',
                  visual=dict(kind='ds_dummy_trap', headers=['intercept'] + levels + ['sum'], rows=trap_rows,
                              rank_line=f'{F["trap_cols"]} columns, but the matrix rank is only {F["trap_rank"]}: there is no single best set of coefficients.',
                              fix_line=f'This is perfect multicollinearity. The fix is one-hot encoding with one level dropped: {F["trap_cols"] - 1} columns, rank {F["trap_rank"]}.'),
                  caption='Perfect multicollinearity: one column is a copy of the sum of others.',
                  notes=(f'Here is a classic trap. Put the intercept column and all eight branch indicators into the model. In every row the eight indicators add up to one, which is exactly the intercept column. One column repeats the sum of the others. '
                         f'This is perfect multicollinearity, and it is called the dummy variable trap. The matrix has {F["trap_cols"]} columns but its rank is only {F["trap_rank"]}, so many different sets of coefficients fit equally well and the computer cannot choose. '
                         'The fix is the one you saw on the last slide: drop one level. Libraries such as pandas do this with drop first. What would the coefficient of the dropped branch be?')))

    # 12 branch indicators in the model
    S.append(dict(kind='table', title=f'Seven branch indicators barely change the fit: R squared {mb["r2"]:.3f}, and adjusted R squared falls',
                  headers=['Model', 'Predictors', 'R squared', 'Adjusted R squared'],
                  rows=[['Footfall only', '1', f'{m1["r2"]:.3f}', f'{m1["adj"]:.3f}'], ['Footfall, promotion, rainfall', '3', f'{m3["r2"]:.3f}', f'{m3["adj"]:.3f}'],
                        ['Plus 7 branch indicators (B01 is the reference level)', '10', f'{mb["r2"]:.3f}', f'{mb["adj"]:.3f}']],
                  widths=[5.4, 1.9, 2.1, 2.6], icons=['chart', 'chart', 'shop'],
                  note=f'R squared never falls when you add a predictor. Adjusted R squared falls when the new predictor adds too little. At the same footfall, promotion and rain, B02 has {abs(mb["b"][4]):.2f} fewer orders than B01.',
                  notes=(f'Let us see what the branch indicators do. With footfall alone R squared is {m1["r2"]:.3f}. With promotion and rainfall it is {m3["r2"]:.3f}. Adding seven branch indicators lifts it only to {mb["r2"]:.3f}. '
                         f'R squared can never fall when you add a predictor, so it flatters big models. Adjusted R squared charges a penalty for each predictor, and it falls from {m3["adj"]:.3f} to {mb["adj"]:.3f}. That is the signal that the branch indicators add too little. '
                         f'The branches differ a little: B02 has {abs(mb["b"][4]):.2f} fewer orders than B01 at the same footfall, promotion and rain. Footfall already carries most of the difference between branches. Would you keep the indicators?')))

    # 13 residual plot
    S.append(dict(kind='idea', title='A residual plot should show an even cloud: homoscedasticity',
                  visual=dict(kind='scatter', points=[[float(a), float(b)] for a, b in zip(fit3, m3['e'])], xlabel='predicted orders', ylabel='residual (actual minus predicted)', hline=0.0, dot=0.035, size=15),
                  alt='Residuals plotted against predicted orders, a cloud that widens to the right',
                  lead='Homoscedasticity: the residuals have the same spread at every prediction.',
                  points=[f'Ours grows: standard deviation {th[0]:.1f}, {th[1]:.1f}, then {th[2]:.1f} orders, low to high thirds.', 'A fan shape: mild heteroscedasticity.', 'Intervals for busy weeks are too narrow.'],
                  notes=(f'A residual plot puts the predicted value along the bottom and the residual up the side. If the model is sound, the dots form an even cloud around zero, with the same spread everywhere. That property is called homoscedasticity. '
                         f'Our plot fans out a little to the right. Split the predictions into three equal groups, from low to high, and the standard deviation of the residuals is {th[0]:.1f}, {th[1]:.1f} and {th[2]:.1f} orders. '
                         'That is mild heteroscedasticity: busy weeks are harder to predict than quiet ones, so a confidence interval that treats every week alike is too narrow for busy weeks. What would you tell a manager about forecasts for busy weeks?')))

    # 14 residual patterns
    S.append(dict(kind='table', title='Four patterns in a residual plot and what to do about each',
                  headers=['Pattern', 'What it means', 'What to try'],
                  rows=[['An even cloud around zero', 'The straight-line model and constant spread look reasonable.', 'Report the model with its limits.'], ['A curve, like a smile', 'The relationship is not a straight line.', 'Add a squared term or change the variable.'],
                        ['A fan that widens (heteroscedasticity)', 'The error grows with the size of the prediction.', 'Model the log of the target, or report wider intervals for large predictions.'], ['A few dots far from the rest', 'Outliers or data errors.', 'Check those records. Do not delete without a reason.']],
                  widths=[3.6, 4.4, 4.0], icons=['check', 'chart', 'magnifier', 'flag'],
                  notes=('Learn to read four patterns. An even cloud around zero means the straight-line model and the constant spread look reasonable. A curve, like a smile, means the true relationship bends, so add a squared term or change the variable. '
                         'A fan that widens is heteroscedasticity. The error grows with the size of the prediction, so model the log of the target or report wider intervals for large predictions. '
                         'And a few dots far from the rest are outliers or data errors, so check those records and never delete them without a reason. Which pattern did our plot show?')))

    # 15 prediction on unseen weeks
    S.append(dict(kind='idea', title=f'Prediction: on {F["n_te"]} records it never saw, the regression misses by {F["te_rmse"]:.1f} orders and the baseline model by {F["te_base_rmse"]:.1f}',
                  visual=dict(kind='bars', items=[dict(label='Baseline model: the training mean', value=round(F['te_base_rmse'], 1)), dict(label='Regression model', value=round(F['te_rmse'], 1), hl=True)], unit=' orders', size=17),
                  alt='Two bars: baseline model misses by 14.6 orders, regression model by 6.3 orders',
                  lead='RMSE on the test set: the typical miss on weeks the model never saw.',
                  points=[f'Training set: {F["n_tr"]} records, {F["first"]} to {F["tr_last"]}.', f'Test set: {F["n_te"]} records, {F["cut"]} to {F["te_last"]}.', f'Baseline model: predict the training mean ({F["tr_mean"]:.1f}) every time.'],
                  notes=(f'Explaining is one job. Predicting is another, and it needs a different check. To predict, you score the model on records it never saw. We fit the model on the first seventy-eight weeks, {F["n_tr"]} records, which is the training set. '
                         f'Then we predict the last twenty-six weeks, {F["n_te"]} records, the test set. Splitting by date like this is a time-based split. The baseline model predicts the training mean every time and misses by {F["te_base_rmse"]:.1f} orders. '
                         f'The regression misses by {F["te_rmse"]:.1f}, close to its training miss of {F["tr_rmse"]:.1f}, and its R squared on the test set is {F["te_r2"]:.2f}. Why must the test weeks stay out of the fitting?')))

    # 16 explanation versus prediction
    S.append(dict(kind='compare', title='Explanation and prediction are two jobs with two ways to check the model',
                  left=dict(head='Explanation', points=['How much does the target change when a predictor changes?', 'Read the coefficients and intervals.', 'Check the residual plot.']),
                  right=dict(head='Prediction', points=['What will the target be for a new record?', 'Score the model on records it never saw.', 'Beat the baseline model.']),
                  verdict='Say which job you are doing before you fit the model.',
                  notes=('Keep the two jobs apart. Explanation asks how much the target changes when a predictor changes. You read coefficients and intervals, and you check the assumptions with a residual plot. '
                         'Prediction asks what the target will be for a new record. You do not care how pretty the coefficients are. You score the model on records it never saw, and you check that it beats the baseline model. '
                         'A model can do one job well and the other badly. A manager who asks for a forecast needs prediction. A manager who asks whether the promotion works needs explanation. Which job is your own project?')))

    # 17 coefficient depends on the other predictors, confounder
    S.append(dict(kind='table', title=f'A coefficient depends on the other predictors in the model: promotion is {F["promo_only_b"]:.2f} alone and {c2:.2f} with footfall and rain',
                  headers=['Model', 'promo_on coefficient', 'rainfall_mm coefficient'],
                  rows=[['promo_on alone', f'{F["promo_only_b"]:.2f}', 'not in the model'], ['promo_on, footfall and rainfall_mm', f'{c2:.2f}', f'{c3:.3f}'], ['rainfall_mm alone', 'not in the model', f'{F["rain_only_b"]:.3f}']],
                  widths=[5.4, 3.3, 3.3], icons=['flag', 'chart', 'rain'],
                  note=f'Promotion weeks had slightly lower footfall ({F["promo_ff_mean"][1]:,.0f} people against {F["promo_ff_mean"][0]:,.0f}), so footfall hides part of the promotion effect. Rain and footfall are almost unrelated (correlation {F["corr_ff_rain"]:.3f}), so the rain coefficient hardly moves.',
                  notes=(f'Here is a warning about reading coefficients. The promotion coefficient is {F["promo_only_b"]:.2f} when promotion is the only predictor, and {c2:.2f} once footfall and rain are in the model. Promotion weeks had slightly lower footfall, {F["promo_ff_mean"][1]:,.0f} people on average against {F["promo_ff_mean"][0]:,.0f}, '
                         f'so footfall hid part of the promotion effect. Footfall is related both to the promotion and to orders, so leaving it out changes the promotion coefficient. When a variable is related to both a predictor and the target, it is a confounding variable, a confounder. Rain and footfall are almost unrelated, with a correlation of {F["corr_ff_rain"]:.3f}, so the rain coefficient barely changes, {F["rain_only_b"]:.3f} against {c3:.3f}. '
                         'A coefficient always means: with the other predictors in this model held fixed. Why does that matter when two managers fit different models?')))

    # 18 association not causation
    S.append(dict(kind='compare', title='A coefficient shows an association, and a cause needs more evidence',
                  left=dict(head='What the model supports', points=[f'Promotion weeks go with {c2:.1f} more orders at the same footfall and rain.', 'Predicting a planned week.']),
                  right=dict(head='What it cannot show', points=['That the promotion caused the extra orders.', 'Nobody randomised the promotion weeks, so a confounder could explain part of the gap.']),
                  verdict='A cause needs an experiment or strong evidence.',
                  notes=(f'This is the limit of regression. The model supports a statement about association: promotion weeks go with {c2:.1f} more orders at the same footfall and rain. You can use that to predict orders for a planned week. '
                         'It cannot show that the promotion caused the extra orders. The data does not say how the promotion weeks were chosen, and branches may have run promotions in weeks that were already going to be good. '
                         'In Session 12 the loyalty offer was randomised, which is why a lift there could be read as a cause. Here nobody randomised, so a confounder could explain part of the gap. What experiment would settle it?')))

    # 19 worked prediction
    S.append(dict(kind='example', title=f'Predict one week by hand: 2,000 people, a promotion and 20 mm of rain gives {F["pred"]:.1f} orders',
                  scenario='Worked example with the fitted multiple linear regression model.',
                  blocks=[dict(label='Question', text='A branch expects 2,000 people, a promotion week and 20 mm of rain. How many orders?'),
                          dict(label='Working', text=f'{c0:.3f} + {c1:.5f} x 2,000 + {c2:.3f} x 1 - {abs(c3):.4f} x 20 = {F["pred"]:.2f}', mono=True),
                          dict(label='Answer', text=f'About {F["pred"]:.0f} orders. The same week without a promotion gives {F["pred_noprom"]:.1f}.', red=True),
                          dict(label='Check', text=f'2,000 lies inside the footfall range of the data ({F["ff_min"]:,} to {F["ff_max"]:,}). Outside that range the prediction is an extrapolation.')],
                  notes=(f'Here is the model at work, by hand. A branch expects two thousand people, a promotion and twenty millimetres of rain. Start with the intercept, {c0:.3f}. Add {c1:.5f} times two thousand, which is {c1 * 2000:.2f}. Add {c2:.3f} for the promotion. '
                         f'Subtract {abs(c3):.4f} times twenty, which is {abs(c3) * 20:.2f}. The total is {F["pred"]:.2f}, about {F["pred"]:.0f} orders. Without the promotion it would be {F["pred_noprom"]:.1f}. '
                         f'Always check the inputs against the range of the data. Two thousand people is inside the range {F["ff_min"]:,} to {F["ff_max"]:,}. Predicting for ten thousand people would be extrapolation, and the model has no evidence there. What input would you try next?')))

    # 20 use at work
    S.append(dict(kind='table', title='Where you will use this at work: put a number on what moves your target',
                  headers=['Your job', 'The question you can answer', 'The tool you would use'],
                  rows=[['Retail analyst at a supermarket chain in Kampala', 'How many more orders does a promotion week bring at the same footfall?', 'Excel LINEST, or statsmodels in Python'],
                        ['Planning officer at a district health office', 'How do monthly clinic visits change with population and the season?', 'pandas and scikit-learn, results shared in Excel'],
                        ['Operations manager at a coffee cooperative', 'Illustrative: how do kilograms delivered change with rainfall and price?', 'Excel trendline first, then Python'],
                        ['Finance analyst at a bank', 'What explains branch deposits? One page of coefficients for the credit committee.', 'statsmodels summary, Power BI for the chart']],
                  widths=[3.5, 5.0, 3.5], icons=['shop', 'clinic', 'plant', 'coin'],
                  notes=('Where will you use this on Monday? A retail analyst at a supermarket chain in Kampala can say how many more orders a promotion week brings at the same footfall, with Excel LINEST or statsmodels. '
                         'A planning officer at a district health office can relate monthly clinic visits to population and season, using pandas and scikit-learn and sharing the result in Excel. '
                         'An operations manager at a coffee cooperative can start with an Excel trendline and move to Python. That example is illustrative. A finance analyst at a bank can put one page of coefficients in front of the credit committee, with a chart in Power BI. '
                         'Which of these is closest to your job?')))

    # 21 project question
    S.append(dict(kind='table', title='A good project question names the target, the predictors, the data and the decision',
                  headers=['Weak question', 'Better question', 'What it names'],
                  rows=[['Is our data interesting?', 'Which of footfall, promotion and rainfall best explain weekly orders at Lakeside Mart branches?', 'Target and predictors'],
                        ['Can we predict loans?', 'Can we predict which Nile Microfinance loans default, using only what is known when the loan is approved?', 'Target, data, timing'],
                        ['Will this help clinics?', 'How many visits should a district clinic plan for next month, and how wrong is the forecast likely to be?', 'Decision and error'],
                        ['My own question', 'What will I predict or explain, from which table, to help which decision?', 'Your turn']],
                  widths=[2.8, 6.6, 2.6], icons=['question', 'coin', 'clinic', 'pin'],
                  notes=('Project milestone 2 also asks you to scope your course project. A weak question is a topic, such as is our data interesting. A better question names the target, the predictors, the data and the decision. '
                         'For Lakeside: which of footfall, promotion and rainfall best explain weekly orders? For Nile Microfinance: can we predict which loans default, using only what is known at approval? '
                         'For the clinics: how many visits should a district plan for next month, and how wrong is the forecast likely to be? The last row is yours. Write your own version before you leave today. Which table would you use?')))

    # 22 code bridge
    out_coef = ' '.join(str(v) for v in np.round(m3['b'], 4))
    S.append(dict(kind='code', title='Read the recipe before the lab: four lines fit a multiple regression',
                  code="cols = ['footfall', 'promo_on', 'rainfall_mm']\nX = np.column_stack([np.ones(len(bw)), bw[cols]])\ncoef, *_ = np.linalg.lstsq(X, bw.orders, rcond=None)\nresiduals = bw.orders - X @ coef\nprint(*coef.round(4))",
                  output=[out_coef],
                  reads=['Line 1 names the three predictors.', 'Line 2 adds a column of ones, which carries the intercept, to make the matrix X.', 'Line 3 solves ordinary least squares. coef holds the intercept, then one coefficient for each predictor.', 'Line 4: the residuals are actual minus predicted.'],
                  notes=(f'Before the lab, read the recipe. Line one names the three predictors. Line two adds a column of ones, which carries the intercept, and makes the matrix called X. Line three asks NumPy to solve ordinary least squares against the orders. '
                         f'It returns the four coefficients: {out_coef}. Line four computes the residuals, actual minus predicted. In the lab you turn them into R squared, {m3["r2"]:.4f}. '
                         'In the lab you also run the same model with the statsmodels library, using the formula orders tilde footfall plus promo on plus rainfall mm. It reports the same numbers. Which line would you change to drop rainfall from the model?')))

    # 23 divider
    S.append(dict(kind='divider', title='Part 2: the regression lab', lead='Close the slides. Open the notebook.', section='Lab',
                  notes=('That is the end of the ideas. Everything you need is on the slides you have just seen, and the notebook repeats each step. '
                         'Open the notebook for Session 13 in Google Colab and run the first cell, which puts the data files next to it. '
                         'In every step you predict first, then run, then read the output, then change one thing. Write your prediction before you run the cell.')))

    # 24 lab map
    S.append(dict(kind='steps', title='The lab has seven steps and ends with a one page report and a summary file',
                  steps=[dict(head='1 Look', text='Plot, correlation', icon='magnifier'), dict(head='2 Simple', text='One predictor', icon='calculator'), dict(head='3 Multiple', text='Coefficients, R squared', icon='notebook'),
                         dict(head='4 Check', text='Residuals, indicators', icon='check'), dict(head='5 Libraries', text='statsmodels, scikit-learn', icon='gear'), dict(head='6 Predict', text='Test weeks', icon='chart'), dict(head='7 Keep', text='Summary file, report', icon='doc')], highlight=None,
                  caption='Predict, run, read, change in each step. Checks tell you when your numbers match.',
                  notes=('Here is the map of the lab, in seven steps. Step one, look at the data with a scatter plot and a correlation. Step two, fit the simple regression with NumPy. Step three, fit the multiple regression, read the coefficients as sentences and compute R squared. '
                         'Step four, check the residuals with a plot, add the branch indicators and meet the dummy variable trap. Step five, run the same model in statsmodels and scikit-learn. Step six, predict one week and test on the last twenty-six weeks. Step seven, save the summary file and write your one page report. '
                         'Each step has a predict prompt and a check. Please do not skip the predictions.')))

    # 25 check numbers
    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Records, and the correlation of orders with footfall', f'{n}, and {F["r"]:.2f}'], ['Simple regression: intercept and coefficient of footfall', f'{b0:.2f} and {b1:.4f}'],
                        ['Multiple regression: intercept, footfall, promo_on, rainfall_mm', f'{c0:.2f}, {c1:.4f}, {c2:.2f}, {c3:.3f}'], ['R squared, and the RMSE (a typical size of a miss)', f'{m3["r2"]:.3f} and {m3["rmse"]:.1f} orders'],
                        ['Residual standard deviation, lowest and highest third of predictions', f'{th[0]:.1f} and {th[2]:.1f}'], ['R squared and adjusted R squared with 7 branch indicators', f'{mb["r2"]:.3f} and {mb["adj"]:.3f}'],
                        ['Matrix rank with the intercept and all 8 indicators', f'{F["trap_rank"]} (9 columns)'], ['Test RMSE: baseline model and regression', f'{F["te_base_rmse"]:.1f} and {F["te_rmse"]:.1f}']],
                  widths=[7.4, 4.6], icons=['grid', 'chart', 'calculator', 'check', 'magnifier', 'shop', 'key', 'clock'], note='If your number differs, find the step that went wrong. Do not change a number to match.',
                  notes=('Use this table as your own self-check. Nobody marks it. If your numbers match, carry on. If one does not, stop and call me, because later steps use the earlier ones. '
                         'The most common causes are a missing column of ones in the matrix X, which changes every coefficient, and fitting on the wrong rows when you split by date. '
                         'Do not change a number to make it match. Find out why it is different. If your R squared is higher than the table says, what could you have done differently?')))

    # 26 error cards
    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[['The intercept is missing, or the numbers are far from the table', 'X has no column of ones.', 'Add np.ones(len(bw)) as the first column of X.'], ['A ValueError about shapes', 'X and y have different lengths, or a column is missing.', 'Print X.shape and y.shape. The rows must match.'],
                        ['Huge coefficients, or a statsmodels multicollinearity note', 'All 8 indicators and the intercept: the dummy variable trap.', 'Use drop_first=True. Check np.linalg.matrix_rank.'], ['The residual plot shows a wedge', 'That is the heteroscedasticity from the residual plot slide.', 'It is a finding. Write it in your report.'],
                        ['statsmodels gives a column named Intercept', 'The formula adds an intercept for you.', 'Do not add a column of ones in the formula version.']],
                  widths=[4.0, 4.0, 4.0], icons=['cross', 'cross', 'cross', 'check', 'cross'],
                  notes=('Five messages you may meet. If the intercept is missing or the numbers are far off, X has no column of ones, so add it as the first column. A ValueError about shapes means X and y have different lengths, so print both shapes. '
                         'Huge or unstable coefficients, or a multicollinearity note from statsmodels, mean you kept all eight indicators together with the intercept, which is the dummy variable trap, so use drop first and check the matrix rank. A wedge in the residual plot is a finding, so write it in your report. '
                         'And the statsmodels formula adds the intercept for you, so do not add a column of ones there. Read the message first. It usually tells you the answer.')))

    # 27 deliverable
    S.append(dict(kind='table', title='Your Project milestone 2 keepsake: a one page analysis report written from your notebook',
                  headers=['Section', 'What you write', 'Where it comes from'],
                  rows=[['Question', 'One sentence naming the target, the predictors and the decision.', 'The project question slide and your notebook'], ['Model', 'The multiple regression and the unit of every predictor.', 'Notebook step 3'],
                        ['Findings', 'Three coefficients as sentences, with intervals, and R squared.', 'Notebook step 7: regression_summary.csv and .xlsx'], ['Check', 'What the residual plot showed and what you would do about it.', 'Notebook step 4'],
                        ['Limits', 'What the model cannot prove, and the test RMSE against the baseline.', 'Notebook step 6']],
                  widths=[2.2, 6.0, 3.8], icons=['question', 'chart', 'notebook', 'magnifier', 'shield'],
                  notes=('This is what you keep. The one page analysis report has five parts. The question names the target, the predictors and the decision. The model states the multiple regression and the unit of every predictor. '
                         'The findings are three coefficients written as sentences with their intervals, and the R squared. The check says what the residual plot showed and what you would do about it. '
                         'And the limits say what the model cannot prove, with the test error against the baseline model. The notebook writes the summary file for you, as csv and as an Excel file you can open in Excel or Power BI. Last line: your project question. Which part will be hardest to write?')))

    # 28 exit check
    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[[f'The promo_on coefficient is {c2:.1f}. Say it as one sentence for a manager.', f'A promotion week has about {c2:.0f} more orders than a week without one at the same footfall and rainfall. It shows an association.'],
                        ['A residual plot fans out to the right. What is the name of the problem, and what does it affect?', 'Heteroscedasticity. The spread of the errors grows with the prediction, so intervals for large predictions are too narrow.'],
                        [f'Adding 7 branch indicators moved R squared from {m3["r2"]:.3f} to {mb["r2"]:.3f} and adjusted R squared from {m3["adj"]:.3f} to {mb["adj"]:.3f}. Keep them?', 'No. They add almost nothing, and adjusted R squared fell.']],
                  widths=[5.6, 6.4], icons=['flag', 'magnifier', 'shop'],
                  notes=('Last, the exit check. Three questions. Write your answers in your notes before you look at mine. One, the promotion coefficient is six point eight: say it as one sentence for a manager. '
                         'Two, a residual plot fans out to the right: what is the problem called and what does it affect? Three, seven branch indicators moved R squared from point seven nine five to point seven nine six, and adjusted R squared fell: do you keep them? '
                         'The short answers are on the slide. If you got all three, you are ready for Session 14. If one surprised you, look at that step of your notebook again tonight.')))

    # facilitator
    sess['facilitator'] = dict(
        prep=['Open the Session 13 notebook in Colab before anyone arrives and run it once. statsmodels is preinstalled in Colab at the time of writing; check that import statsmodels works.',
              'The numbers in this deck were computed with NumPy because statsmodels was not available when the deck was built; run the statsmodels cell yourself and check it matches.',
              'Write the check table (the slide titled Check your numbers) on the board before the lab.',
              'Concepts run with laptops closed. Ask learners to open the notebook only after the Part 2 divider.',
              'Project milestone 2 is a one page report. Tell learners when to show it to you for feedback. It is never scored.'],
        misconceptions=[('R squared of 0.795 means the model is right 79.5 percent of the time', 'R squared is the share of the variation in the target that the model accounts for. It is not an accuracy.'),
                        ('The intercept is the average value of the target', f'The intercept is the prediction when every predictor is 0. Here it is {c0:.2f} orders at zero footfall, which no real week has.'),
                        ('A significant coefficient proves a cause', 'It shows an association, adjusted for the other predictors in the model. Cause needs an experiment or strong outside evidence.'),
                        ('More predictors always make a better model', f'R squared never falls, but adjusted R squared can. Seven branch indicators moved R squared from {m3["r2"]:.3f} to {mb["r2"]:.3f} and adjusted R squared fell.'),
                        ('Keep every indicator column to lose no information', 'All k indicators plus the intercept repeat each other (the dummy variable trap). Drop one level, the reference level.')],
        probes=[('What is a residual?', 'Actual value minus predicted value for one record.'), ('What does ordinary least squares minimise?', 'The sum of the squared residuals.'),
                ('What does the footfall coefficient mean?', f'1,000 more people at the door goes with {c1 * 1000:.1f} more orders, other predictors held fixed.'),
                ('Why is the intercept not read alone here?', f'No week has zero footfall; the minimum is {F["ff_min"]}.'), ('What does homoscedasticity mean?', 'The residuals have about the same spread at every predicted value.'),
                ('Why drop one indicator level?', 'To avoid the dummy variable trap: the indicators add up to the intercept column.'),
                ('Why is orders a better target than sales_ugx here?', f'The same predictors give R squared {m3["r2"]:.3f} for orders and {F["sales_r2"]:.3f} for sales, which a few huge baskets inflate.'),
                ('Why split the weeks by date for prediction?', 'To test on later weeks the model never saw, as in real forecasting.')],
        lab_steps=[('Step 1: look', f'{n} records and a correlation of {F["r"]:.2f}. Learners should predict a strong positive correlation before they run it.'),
                   ('Step 2: simple regression', f'Intercept {b0:.2f}, coefficient {b1:.4f}. Watch for a missing column of ones.'),
                   ('Step 3: multiple regression', f'Coefficients {c0:.2f}, {c1:.4f}, {c2:.2f}, {c3:.3f}; R squared {m3["r2"]:.3f}, RMSE {m3["rmse"]:.1f}.'),
                   ('Step 4: residuals and indicators', f'Spread by thirds {th[0]:.1f}, {th[1]:.1f}, {th[2]:.1f}. With 7 indicators R squared {mb["r2"]:.3f}, adjusted {mb["adj"]:.3f}. Rank {F["trap_rank"]} with all 8.'),
                   ('Step 5: library check', 'statsmodels and scikit-learn LinearRegression agree with NumPy. Colab only.'),
                   ('Step 6: predict and test', f'Prediction {F["pred"]:.1f} orders. Test RMSE {F["te_rmse"]:.1f} against {F["te_base_rmse"]:.1f} for the baseline.'),
                   ('Step 7: keep', 'The summary file (csv and xlsx) with intervals, then the one page report.')],
        rescue=['If the concepts run over, shorten the residual patterns table and the project question slide; the lab covers both.', 'If only 30 minutes of lab remain, do steps 1 to 4 and set steps 5 and 6 as homework.',
                'If statsmodels fails to import in Colab, run pip install statsmodels in a cell and restart; the NumPy answers stand on their own.', 'If a learner has no laptop, pair them with a neighbour: one types, one predicts aloud.'],
        after=['Share the notebook and this deck again for learners who were absent.', 'Look at each one page report with its author and give feedback (Project milestone 2). Nothing is scored.', 'Note any question you could not answer and open Session 14 with it.'],
        lab_answer_key=[['Step 1 PREDICT: what sign and size will the correlation have?', f'Strongly positive: {F["r"]:.2f}. Busy weeks have more orders.'],
                        ['Step 2 CHANGE: use rainfall_mm as the only predictor.', f'The coefficient is {F["rain_only_b"]:.3f} orders per mm. It is small, and R squared is far lower than with footfall.'],
                        ['Step 3 READ: say the promo_on coefficient as a sentence.', f'A promotion week has {c2:.1f} more orders than a week without one at the same footfall and rainfall.'],
                        ['Step 4 READ: what does the residual plot show?', f'A mild fan: the residual standard deviation grows from {th[0]:.1f} to {th[2]:.1f} orders. Busy weeks are harder to predict.'],
                        ['Step 4 CHANGE: add the 7 branch indicators.', f'R squared {mb["r2"]:.3f}, adjusted R squared {mb["adj"]:.3f}, which is lower than {m3["adj"]:.3f}. Keep the simpler model.'],
                        ['Step 5 READ: do statsmodels and NumPy agree?', 'Yes, to many decimals. Both solve ordinary least squares.'],
                        ['Step 6 READ: did the model beat the baseline on the test weeks?', f'Yes: RMSE {F["te_rmse"]:.1f} against {F["te_base_rmse"]:.1f} orders.'],
                        ['Step 6 CHANGE: predict the same week without a promotion.', f'{F["pred_noprom"]:.1f} orders, which is {c2:.1f} fewer.']])
    return sess
