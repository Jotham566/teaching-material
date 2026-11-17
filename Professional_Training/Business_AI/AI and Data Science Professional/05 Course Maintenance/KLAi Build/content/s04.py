"""Session 4: Uncertainty, samples and cause (probability, population and sample, sampling error, sampling distribution and standard error, Monte Carlo simulation with RAND in Sheets,
Pearson correlation, confounders, selection and survivorship bias). Sheets lab, no notebook.

Every number on a slide, in a note or in sheet_tasks is computed in facts() with pandas / numpy from the real Lakeside Mart workbook and the other course files.
The simulation is seeded (b_facts.sim), so figures and notes are the same on every build. A learner's own random numbers will differ; sheet_tasks give ranges
from 5,000 repeats of the whole exercise.
"""
from functools import lru_cache

import numpy as np
import pandas as pd

import b_facts as BF
from b_facts import n


@lru_cache(maxsize=None)
def facts():
    B = BF.base()
    S = BF.sim()
    T = B['T']
    w, br = T['branch_weeks'], T['branches']
    F = dict(B=B, S=S)
    v = T['orders'].order_value_ugx
    F['p100k'] = B['share_gt_100k']
    F['n100k'] = B['n_gt_100k']
    F['full_p100k'] = B['full_share_gt_100k']
    F['sum_edges'], F['sum_counts'], F['sum_above'] = BF.hist(S['m30'], 0, 200000, 10000)
    F['m5_counts'] = BF.hist(S['m5'], 0, 250000, 10000)
    F['m30_counts'] = BF.hist(S['m30'], 0, 250000, 10000)
    F['m200_counts'] = BF.hist(S['m200'], 0, 250000, 10000)
    F['panel_edges'] = F['m5_counts'][0]
    F['panel_above'] = (F['m5_counts'][2], F['m30_counts'][2], F['m200_counts'][2])
    F['ymax_panels'] = max(max(F['m5_counts'][1]), max(F['m30_counts'][1]), max(F['m200_counts'][1]))
    F['sd_ratio'] = S['sd5'] / S['sd30']
    F['se_ratio'] = float(S['se5'] / S['se30'])
    # correlations in branch_weeks
    F['r_foot_orders'] = float(w.footfall.corr(w.orders))
    F['r_rain_orders'] = float(w.rainfall_mm.corr(w.orders))
    F['r_foot_rain'] = float(w.footfall.corr(w.rainfall_mm))
    b1 = w[w.branch_id == 'B01']
    F['b1_rows'] = len(b1)
    F['r_b1_foot'], F['r_b1_rain'] = float(b1.footfall.corr(b1.orders)), float(b1.rainfall_mm.corr(b1.orders))
    per = {k: float(g.footfall.corr(g.orders)) for k, g in w.groupby('branch_id')}
    F['r_within'] = per
    F['r_within_min'], F['r_within_max'] = min(per.values()), max(per.values())
    fd = w.footfall - w.groupby('branch_id').footfall.transform('mean')
    od = w.orders - w.groupby('branch_id').orders.transform('mean')
    F['r_pooled_within'] = float(np.corrcoef(fd, od)[0, 1])
    F['r2'] = F['r_foot_orders'] ** 2
    F['weeks_n'] = len(w)
    g = w.groupby('branch_id')[['footfall', 'orders']].mean()
    sizes = br.set_index('branch_id')['size']
    F['branch_rows'] = [[f'{k} {B["branch_names"][k]}', f'{sizes[k]:.1f}', n(r.footfall), f'{r.orders:.1f}'] for k, r in g.iterrows()]
    F['g'] = g
    F['sizes'] = sizes
    F['r_size_foot'] = float(np.corrcoef(sizes.loc[g.index], g.footfall)[0, 1])
    F['r_size_orders'] = float(np.corrcoef(sizes.loc[g.index], g.orders)[0, 1])
    F['scatter_pts'] = [[float(a), float(b)] for a, b in w[['footfall', 'orders']].values]
    F['scatter_rain'] = [[float(a), float(b)] for a, b in w[['rainfall_mm', 'orders']].values]
    F['scatter_fr'] = [[float(a), float(b)] for a, b in w[['footfall', 'rainfall_mm']].values]
    # clinic lag example
    cl = pd.read_csv(BF.DATA / 'clinic_visits.csv').sort_values(['district', 'month'])
    cl['rain_lag'] = cl.groupby('district').rainfall_mm.shift(1)
    F['clinic_r0'] = float(cl.malaria_cases.corr(cl.rainfall_mm))
    F['clinic_r1'] = float(cl.malaria_cases.corr(cl.rain_lag))
    # running share
    F['running'] = S['running']
    # sheet-level facts
    F['mean'] = B['mean']
    return F


def rf(r):
    """r with two decimals, never minus zero."""
    return f'{0.0 if abs(r) < 0.005 else r:.2f}'


def build():
    F = facts()
    B, S = F['B'], F['S']
    N = B['n_orders']
    mu, sig = S['mu'], S['sigma']
    names = B['branch_names']
    rg = S['rng']
    sd_ratio_lo, sd_ratio_hi = S['rng_ratio']
    f1, f2 = S['first_samples'][:2]
    f3 = (3, float(S['m30'][2]), float(S['m30'][2] - mu))   # the real sample 3, so samples 1, 2 and 3 are shown in order
    assert all(x[2] < -10000 for x in (f1, f2, f3))
    sess = dict(
        num=4, block='Module A: Think with data', short_title='Uncertainty, samples and cause',
        title='Uncertainty, samples and cause',
        question='How sure can we be of a number from a sample, and when does a pattern mean that one thing caused another?',
        outcomes=['Explain why a sample differs from the population, and measure that difference with the standard error',
                  'Run a Monte Carlo simulation with RAND in Google Sheets and read the sampling distribution it produces',
                  'Read a Pearson correlation, say what it does not show, and name a confounder and two kinds of bias'],
        outcome_icons=['bars', 'switch', 'magnifier'],
        outcome_note=('Here is what you can do by the end of today. You can explain why a sample differs from the population it came from, and measure that difference with the standard error. '
                      'You can run a Monte Carlo simulation with RAND in Google Sheets and read the sampling distribution it produces. '
                      'And you can read a Pearson correlation, say what it does not show, and name a confounder and two kinds of bias. There is no code today. Every formula is one you can type into a cell.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: picture, plain words, one example by hand'), (10, 'Break'), (45, 'Lab: simulate, correlate, question'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: concepts first, then a Google Sheets lab',
        plan_caption='Ideas with pictures first. Then you open the sheet. Then the checks and what you keep.',
        plan_note=('We have two hours. The first ten minutes bring back Session 3 and set the question for today. Then forty-five minutes of concepts, with no laptops open, so you can watch the pictures. '
                   'After a ten minute break we open the Lakeside Mart workbook in Google Sheets for a forty-five minute lab. You build a simulation of two hundred samples, read a correlation, and question a pattern. '
                   'The last ten minutes are an exit check and what you keep. The lab is where the learning sticks, so please protect that time.'),
        recall_from='Session 3',
        recall=[('A manager asks what a typical order is worth. Which statistic do you lead with, and what else do you give?', f'The median, {n(B["median"])} UGX, with the number of orders and the IQR. The mean, {n(B["mean"])}, is pulled up by a few large orders.'),
                ('What is a pivot table in SQL and in pandas?', 'A GROUP BY in SQL and groupby in pandas: group the records, then aggregate each group.'),
                ('A bar chart makes a small gap between two branches look huge. What do you check first?', 'Whether the vertical axis starts at zero. Cutting the base makes small gaps look large.')],
        words=[('Population and sample', 'The population is every record you care about. A sample is the part you actually look at. The gap between a sample statistic and the population value is sampling error. How much a statistic changes from sample to sample is sampling variability.'),
               ('Standard error', 'The standard deviation of a statistic across many samples, such as the sample mean. It says how far one sample can sit from the truth.'),
               ('Monte Carlo simulation', 'Many random draws done by computer to see what a statistic does. In Sheets: RAND and INDEX, filled down.'),
               ('Correlation (Pearson r)', 'A number from -1 to +1 for how closely two numeric variables rise and fall together. Correlation is not causation.'),
               ('Confounder', 'A variable that influences both of two variables you are comparing, so they look linked. Also called a confounding variable.')],
        word_icons=['people', 'bars', 'switch', 'chart', 'question'],
        words_note=('Five words for today. A population is every record you care about, and a sample is the part you look at. The gap between them is sampling error, and how much it changes from sample to sample is sampling variability. '
                    'The standard error says how far a sample statistic can sit from the truth. A Monte Carlo simulation is many random draws done by computer. '
                    'Correlation, written r, says how closely two variables move together, and it is never proof of cause. And a confounder is a variable that influences both. We use every one of them before the end of the session.'),
        keep='Keep your simulation tab: 200 samples of 30 orders, their histogram, and three sentences on what a correlation does and does not show.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab file', value='A simulation tab'), dict(label='Your finding', value='Three sentences on cause'), dict(label='Next session', value='Your first Python')]),
        keep_title='Save your simulation tab, then bring one question to Session 5',
        next='Session 5: your first Python: variables, lists, dictionaries and error messages. The pandas DataFrame comes in Session 7.', next_label='Next session',
        keep_note=('Before you go, save the workbook with your simulation tab. That tab is your keepsake from today: two hundred samples of thirty orders, the histogram of their means, and three sentences on what a correlation does and does not show. '
                   'If you can explain to a colleague why your sample means spread out, you have the main idea of statistics. Next session we leave Sheets and meet your first Python, and we reach tables again in Session 7. '
                   'If anything was unclear today, write the question down and bring it.'),
        cover_note=('Welcome back. Last session we described the data we hold. Today we ask how sure we can be. If you look at thirty orders, how far can their average sit from the truth? '
                    'We find out by simulating it in Google Sheets, with no code at all. We also look at correlation, at why two things that move together may have nothing to do with each other, and at the ways a sample can quietly mislead you.'),
        use_at_work='State how far a sample figure can sit from the truth, and ask what else could explain a pattern before you act on it.',
        slides=[])
    S_ = sess['slides']

    # ------------------------------------------------------------------ 1 answers
    S_.append(dict(kind='table', title='Answers to the three questions from Session 3', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in sess['recall']], widths=[5.2, 6.8], icons=['calculator', 'grid', 'chart'],
                   notes=(f'Here are the answers to the three warm-up questions. For a typical order you lead with the median, {n(B["median"])} shillings, and give the number of orders and the IQR beside it, because a few very large orders pull the mean up to {n(B["mean"])}. '
                          'A pivot table is a GROUP BY in SQL and groupby in pandas: you group the records, then aggregate each group. '
                          'And when a bar chart makes a small gap between two branches look huge, you check first whether the vertical axis starts at zero. Today we ask a harder question about numbers like these. How much can they move just because of which records we looked at? Which of the three did you find hardest?')))

    # ------------------------------------------------------------------ 2 probability
    S_.append(dict(kind='stat', title='Probability is a share between 0 and 1: about 7 orders in 100 are above 100,000 UGX', big='7%',
                   text=f'{n(F["n100k"])} of {n(N)} orders are above 100,000 UGX. P(order above 100,000) = {n(F["n100k"])} ÷ {n(N)} = {F["p100k"]:.4f}.',
                   visual=dict(kind='waffle', filled=7, label='orders in every 100 are above 100,000 UGX'),
                   notes=(f'Let us start with probability. A probability is a number between zero and one that says how likely an event is. When you can count records, it is the count of the event divided by the count of all records. '
                          f'In the workbook, {n(F["n100k"])} of the {n(N)} orders are above 100,000 shillings. That is {F["p100k"]:.4f}, or about 7 orders in every 100. In Sheets, COUNTIF with greater than 100000, divided by the count of orders, gives it. '
                          'This is a relative frequency: a share observed in data. Does that share tell you whether the next order will be large?')))

    # ------------------------------------------------------------------ 3 long run
    run = F['running']
    S_.append(dict(kind='wide', title='A share settles as you count more records: this is the long run',
                   visual=dict(kind='dsb_settle', points=[list(p) for p in run], final=F['p100k'], final_label=f'{F["p100k"] * 100:.2f} percent after {n(N)} orders', xticks=[(0, '0'), (500, '500'), (1000, '1,000'), (1500, '1,500'), (2000, '2,000')],
                               yticks=[(0, '0%'), (0.05, '5%'), (0.1, '10%'), (0.15, '15%')], xlabel='number of orders counted, in a random order', ylabel='share above 100,000 UGX'),
                   caption='Early shares swing. Later shares settle. This is the law of large numbers.',
                   notes=(f'Here is the same share, but counted as orders arrive in a random order. After 20 orders the share swings a lot, because one or two large orders change it. As we count more, the line settles near the dashed red line, {F["p100k"] * 100:.2f} percent. '
                          'This settling is called the law of large numbers: a share measured over many records stays closer and closer to its long-run value. '
                          f'In the full file of {n(B["full_n"])} orders the share is {F["full_p100k"] * 100:.2f} percent. So the workbook share is close to it but not identical. Why do you think the two differ?')))

    # ------------------------------------------------------------------ 4 population and sample
    S_.append(dict(kind='wide', title='A sample is drawn from a population, and a statistic from the sample estimates a parameter',
                   visual=dict(kind='dsb_popsample', pop_title=f'Population: {n(N)} orders', pop_text=f'For this lesson, the orders in the workbook. A number that describes the whole population is a parameter: the population mean is {n(mu)} UGX.', picked=S['picked'],
                               sample_title='Sample: 30 orders', sample_text=f'Drawn at random. A number computed from the sample is a statistic: here the sample mean is {n(f1[1])} UGX.', arrow_text='random sample, n = 30',
                               foot=f'Sampling error = sample mean minus population mean = {n(f1[1])} minus {n(mu)} = {n(f1[2])} UGX'),
                   caption=f'The workbook is itself a sample of the full file. Here we treat its {n(N)} orders as the population.',
                   notes=(f'Now the key idea. A population is every record you care about. A sample is the part you actually look at. A number that describes the population is a parameter. A number computed from the sample is a statistic. '
                          f'For this lesson we treat the {n(N)} orders in the workbook as the population. Its mean, the parameter, is {n(mu)} shillings. We draw thirty orders at random, the gold dots, and compute their mean, the statistic. Our first sample gave {n(f1[1])}. '
                          f'The difference, {n(f1[2])}, is sampling error. Nobody made a mistake. It comes only from which records were drawn. The workbook is itself a sample of the full file, which is why we say we treat it as the population. Why can we never see the true parameter in real work?')))

    # ------------------------------------------------------------------ 5 sampling error table
    S_.append(dict(kind='table', title='Three random samples of 30 orders give three different means, and the gaps are sampling error',
                   headers=['Sample', 'Sample mean (UGX)', 'Sampling error (UGX)'],
                   rows=[[f'Sample {k}', n(m), f'{e:,.0f}'] for k, m, e in (f1, f2, f3)] + [['Population (all 2,000 orders)', n(mu), '0']],
                   widths=[4.8, 3.6, 3.6], icons=['people', 'people', 'people', 'folder'], note='These samples come from one seeded run of the simulation. Yours will differ. Sampling error = sample mean minus population mean.',
                   notes=(f'Here are three random samples of thirty orders, taken from the simulation we build in a minute. Sample {f1[0]} has a mean of {n(f1[1])}, which is {abs(f1[2]):,.0f} below the population mean. '
                          f'Sample {f2[0]} has {n(f2[1])}, {abs(f2[2]):,.0f} below. Sample {f3[0]} has {n(f3[1])}, only {abs(f3[2]):,.0f} away. Each gap is that sample\'s sampling error. '
                          'Notice that all three sit well below the true mean. Because order values are right-skewed, most samples of thirty contain none of the few huge orders, and a few samples that catch one sit far above. Why would a bigger sample help?')))

    # ------------------------------------------------------------------ 6 Monte Carlo steps
    S_.append(dict(kind='steps', title='A Monte Carlo simulation repeats a random draw many times: five steps in Sheets',
                   steps=[dict(head='1 Draw', text='One random order in A2', icon='switch'), dict(head='2 Fill right', text='To AD2: a sample of 30', icon='bars'), dict(head='3 Average', text='AE2 is the sample mean', icon='calculator'),
                          dict(head='4 Fill down', text='To row 201: 200 samples', icon='grid'), dict(head='5 Freeze', text='Paste values, then chart', icon='lock')], highlight=None,
                   caption='Each draw puts a random row number into INDEX. Drawing the same row twice is allowed: sampling with replacement.',
                   notes=('A Monte Carlo simulation repeats a random draw many times to see what a statistic does. In Sheets it takes five steps. One, in cell A2 draw one random order with INDEX and RAND. '
                          'Two, fill right to column AD, which gives thirty random orders in one row: that row is one sample. Three, in AE2 take the average of A2 to AD2: the sample mean. '
                          'Four, fill the whole row down to row 201, so you have two hundred samples and two hundred sample means. Five, freeze the numbers by pasting values, then chart them. '
                          'Each draw may pick the same row twice. That is called sampling with replacement. Why does it matter that each draw is independent?')))

    # ------------------------------------------------------------------ 7 formulas
    S_.append(dict(kind='table', title='Three small formulas build one random draw and one sample mean',
                   headers=['Piece', 'Formula', 'What you get'],
                   rows=[['A random decimal', '=RAND()', 'A number from 0 up to just below 1, new on every recalculation'], ['A random row number', '=1+INT(RAND()*2000)', 'A whole number from 1 to 2000'],
                         ['One random order', '=INDEX(orders!$G$2:$G$2001,1+INT(RAND()*2000))', 'The order value in that row'], ['The sample mean', '=AVERAGE(A2:AD2)', 'One mean for the row of 30 orders']],
                   widths=[2.6, 5.6, 3.8], icons=['switch', 'pin', 'receipt', 'calculator'], note='=RANDBETWEEN(1,2000) is a shortcut for the second formula. Both can give the same row twice.',
                   notes=('Here are the formulas. RAND gives a random decimal from zero up to just below one. Multiply it by 2000, take INT to cut off the decimals, and add one, and you have a random row number from one to two thousand. '
                          'INDEX uses that row number to read an order value from column G of the orders tab. That is one random order. Fill it across thirty cells and you have a sample. AVERAGE of that row is the sample mean. '
                          'RANDBETWEEN of one and two thousand is a shortcut for the row number. Only INDEX and INT are new to you. Which of these formulas would you change to draw a sample of fifty?')))

    # ------------------------------------------------------------------ 8 freeze
    cells = 200 * 30
    S_.append(dict(kind='compare', title='RAND recalculates on every edit, so freeze the results before you chart them',
                   left=dict(head='Live formulas', icon='cross', points=[f'Every edit redraws all {n(cells)} random draws and 200 means.', 'Your histogram changes while you look at it.', 'Sheets has no setting to fix the draw.']),
                   right=dict(head='Frozen values', icon='check', points=['Copy the block, then Paste special, Values only.', 'The numbers stay fixed.', 'Now compute and chart.']),
                   verdict='Sheets cannot fix a draw, so freeze the values.',
                   notes=(f'Here is the trap in every Sheets simulation. RAND recalculates every time anything changes on the sheet. Your block holds {n(cells)} random draws and the 200 means built on them, so a single edit redraws them all, and your histogram changes under your hands. '
                          'Sheets has no way to fix the random draw. So before you chart or compute anything, copy the block and use Paste special, Values only. Then the numbers stay put. In Excel, you can set Calculation Options to Manual instead. '
                          'In Python you can set a random seed, a starting number that makes the same random numbers appear every run. That is called reproducibility, and we meet random seeds later in the course. Which would you prefer for a report you must defend?')))

    # ------------------------------------------------------------------ 9 sampling distribution
    S_.append(dict(kind='wide', title='200 samples of 30 orders give 200 different means: together they form the sampling distribution',
                   visual=dict(kind='dsb_hist', edges=F['sum_edges'], counts=F['sum_counts'],
                               lines=[dict(x=mu, label=f'population mean {n(mu)}', color='#AE2525'), dict(x=S['mean30'], label=f'mean of the 200 means {n(S["mean30"])}', color='#111111')],
                               xticks=[(0, '0'), (50000, '50,000'), (100000, '100,000'), (150000, '150,000'), (200000, '200,000')], xlabel='sample mean of 30 orders (UGX), bars 10,000 UGX wide', ylabel='number of samples',
                               ymax=max(F['sum_counts']), note=[f'smallest {n(S["min30"])}', f'largest {n(S["max30"])}', f'{S["below_mu"]} of 200 below the population mean']),
                   caption='One seeded run of the exercise. Your own run will look similar but not identical.',
                   notes=(f'Here is what two hundred samples look like. Each bar counts samples whose mean falls in a band of ten thousand shillings. The means run from {n(S["min30"])} to {n(S["max30"])}. '
                          f'They centre near the population mean, the red line: the mean of the two hundred means is {n(S["mean30"])}. So one sample can miss by a lot, yet the samples as a group centre on the truth. '
                          f'Together these 200 sample means form the sampling distribution. Their spread, measured by the standard deviation of the means, is the standard error, which comes next. This is sampling variability on the page. Notice the long tail to the right, the skewness from Session 3. And {S["below_mu"]} of the 200 sample means sit below the population mean. Why would more than half sit below?')))

    # ------------------------------------------------------------------ 10 standard error formula
    S_.append(dict(kind='formula', title='The standard error is the standard deviation of the sample means',
                   formulas=[('Standard error of the mean', r'$SE(\bar{x}) = \frac{\sigma}{\sqrt{n}} = \frac{128{,}062}{\sqrt{30}} = 23{,}381$')],
                   symbols=[['SE', 'Standard error: the spread of the sample means across many samples', f'Simulated: {n(S["sd30"])} (STDEV of 200 means)'], ['sigma', 'Population standard deviation (STDEV.P)', f'{n(sig)} UGX'], ['n', 'The sample size', '30 orders'],
                            ['x-bar', 'The sample mean', 'One value in each sample row']],
                   note='With one real sample you do not know sigma, so you use s, the sample standard deviation.',
                   notes=(f'Here is the standard error. It is the standard deviation of the sample means, the spread of the sampling distribution. A formula gives it without simulating: the population standard deviation, sigma, divided by the square root of the sample size, n. '
                          f'For our orders, sigma is {n(sig)} and n is thirty, so the standard error is {n(S["se30"])} shillings. Our simulation of two hundred means gave a standard deviation of {n(S["sd30"])}, which is close. '
                          'In real work you only have one sample and do not know sigma, so you use the sample standard deviation instead. A smaller standard error means a more trustworthy sample mean. What would make it smaller?')))

    # ------------------------------------------------------------------ 11 bigger sample
    def panel(title, counts_tuple, se, sd_sim):
        e, c, _ = counts_tuple
        return dict(title=title, edges=e, counts=c, ymax=F['ymax_panels'], xticks=[(0, '0'), (100000, '100'), (200000, '200')], xlabel='sample mean (thousand UGX)',
                    lines=[dict(x=mu, label='population mean', color='#AE2525')], note=[f'SE {n(se)}', f'simulated SD {n(sd_sim)}'])
    S_.append(dict(kind='wide', title='A larger sample has a smaller standard error: quadruple n to halve it',
                   visual=dict(kind='dsb_panels', panels=[panel('Samples of n = 5', F['m5_counts'], S['se5'], S['sd5']), panel('Samples of n = 30', F['m30_counts'], S['se30'], S['sd30']), panel('Samples of n = 200', F['m200_counts'], S['se200'], S['sd200'])]),
                   caption='Each panel shows 200 sample means on the same scale. SE = sigma divided by the square root of n.',
                   notes=(f'Now the same exercise for three sample sizes. With five orders in each sample, the standard error is {n(S["se5"])} and the means are spread far and wide. With thirty, it is {n(S["se30"])}. With two hundred it is {n(S["se200"])}, and the means huddle round the population mean. '
                          f'Because of the square root, quadrupling the sample size halves the standard error. Going from thirty to one hundred and twenty would cut it in half. Going from five to thirty cuts it by a factor of {F["se_ratio"]:.1f}. '
                          'More data helps, but with diminishing returns. What would it cost your organisation to collect four times as many records?')))

    # ------------------------------------------------------------------ 12 CLT
    bg = S['big']
    S_.append(dict(kind='table', title='Sample means of skewed data stay skewed at small n and become bell-shaped as n grows',
                   headers=['Sample size n', 'Standard error', 'Skewness of the sample means', 'Share of samples below the population mean'],
                   rows=[[str(k), n(S[f'se{k}']), f'{bg[k]["skew"]:.2f}', f'{bg[k]["below"] * 100:.0f} percent'] for k in (5, 30, 200)],
                   widths=[2.2, 2.6, 3.4, 3.8], icons=['bars', 'bars', 'bars'], note='From 20,000 repeats of each sample size. Order values have skewness 8.76. This pattern is the central limit theorem at work.',
                   notes=(f'This table explains why more than half of our samples sat below the population mean. Order values are very right-skewed, with skewness {B["skew"]:.2f}. For samples of five, the sample means have skewness {bg[5]["skew"]:.2f}, and {bg[5]["below"] * 100:.0f} percent of samples fall below the true mean. '
                          f'For samples of thirty the skewness is {bg[30]["skew"]:.2f}, and for two hundred it is {bg[200]["skew"]:.2f}, with {bg[200]["below"] * 100:.0f} percent below. As n grows, the sampling distribution gets closer to a bell shape and to symmetry. '
                          'That is the central limit theorem. It works slowly when the data is heavily skewed. These figures come from twenty thousand repeats of each size. What does that tell you about a survey of thirty records?')))

    # ------------------------------------------------------------------ 13 correlation scatters
    def sc(title, pts, xl, yl, r, xt, yt, xlim, ylim):
        return dict(title=title, sub=f'r = {rf(r)}', points=pts, xlabel=xl, ylabel=yl, xticks=xt, yticks=yt, xlim=xlim, ylim=ylim, dot=0.03)
    W = F['B']['T']['branch_weeks']
    S_.append(dict(kind='wide', title='Correlation (Pearson r) measures how closely two variables rise and fall together',
                   visual=dict(kind='dsb_scatters', panels=[sc('Strong positive', F['scatter_pts'], 'footfall (visitors a week)', 'orders a week', F['r_foot_orders'], [(1000, '1,000'), (3000, '3,000'), (5000, '5,000')], [(20, '20'), (60, '60')],
                                                                 (float(W.footfall.min()), float(W.footfall.max())), (float(W.orders.min()), float(W.orders.max()))),
                                                           sc('Weak negative', F['scatter_rain'], 'rainfall (mm a week)', 'orders a week', F['r_rain_orders'], [(0, '0'), (50, '50'), (100, '100')], [(20, '20'), (60, '60')],
                                                                 (float(W.rainfall_mm.min()), float(W.rainfall_mm.max())), (float(W.orders.min()), float(W.orders.max()))),
                                                           sc('None', F['scatter_fr'], 'footfall (visitors a week)', 'rainfall (mm a week)', F['r_foot_rain'], [(1000, '1,000'), (3000, '3,000'), (5000, '5,000')], [(0, '0'), (50, '50')],
                                                                 (float(W.footfall.min()), float(W.footfall.max())), (float(W.rainfall_mm.min()), float(W.rainfall_mm.max())))]),
                   caption=f'Each dot is one branch in one week: {F["weeks_n"]} records from the branch_weeks tab.',
                   notes=(f'Correlation measures how closely two numeric variables rise and fall together. The Pearson correlation coefficient, written r, runs from minus one to plus one. Each dot here is one branch in one week. '
                          f'On the left, footfall and orders have r of {F["r_foot_orders"]:.2f}: strongly positive, busier weeks have more orders. In the middle, rainfall and orders have r of {F["r_rain_orders"]:.2f}: weakly negative. '
                          f'On the right, footfall and rainfall have r of {rf(F["r_foot_rain"])}, essentially zero: no linear link. In Sheets, the function is CORREL. Which of the three pictures would you trust for a forecast?')))

    # ------------------------------------------------------------------ 14 Pearson formula
    S_.append(dict(kind='formula', title='Pearson r multiplies how far two variables sit from their means, record by record',
                   formulas=[('Pearson correlation', r'$r = \frac{\sum (x_i-\bar{x})(y_i-\bar{y})}{\sqrt{\sum (x_i-\bar{x})^2 \; \sum (y_i-\bar{y})^2}} = 0.84$')],
                   symbols=[['r', 'Pearson correlation coefficient, from -1 to +1', f'{F["r_foot_orders"]:.2f} for footfall and orders'], ['x_i, y_i', 'Footfall and orders of branch-week i', f'{F["weeks_n"]} records'],
                            ['x-bar, y-bar', 'The mean footfall and the mean orders', 'Means of the two variables'], ['r squared', 'Share of the variance in orders that a straight line on footfall accounts for (coefficient of determination)', f'{F["r2"]:.2f}']],
                   note='In Sheets: =CORREL(branch_weeks!C2:C833,branch_weeks!F2:F833). Pearson r measures only straight-line association.',
                   notes=('Here is the formula. For each record, take how far footfall is above or below its mean and how far orders are above or below its mean, and multiply the two. '
                          'When both are above average together, or both below, the product is positive. When one is above and the other below, it is negative. Add the products and divide by a scaling term so the answer sits between minus one and plus one. '
                          f'For footfall and orders across {F["weeks_n"]} branch weeks, r is {F["r_foot_orders"]:.2f}. Squared, it is {F["r2"]:.2f}, so about {F["r2"] * 100:.0f} percent of the variance in orders is accounted for by a straight line on footfall. That is the coefficient of determination. Pearson r only measures straight-line association. Why would a curve fool it?')))

    # ------------------------------------------------------------------ 15 reading r and the lag trap
    S_.append(dict(kind='table', title='Reading r: size, sign and what it cannot tell you',
                   headers=['Pair of variables', 'r', 'Reading'],
                   rows=[['Footfall and orders', f'{F["r_foot_orders"]:.2f}', 'Strong, positive. Busier weeks have more orders. It says nothing about which causes which.'],
                         ['Rainfall and orders', f'{F["r_rain_orders"]:.2f}', 'Weak, negative. Wetter weeks have somewhat fewer orders, with a lot of scatter.'],
                         ['Footfall and rainfall', rf(F["r_foot_rain"]), 'About zero. No straight-line link.'],
                         ['Malaria cases and rain, same month, District Clinics', f'{F["clinic_r0"]:.2f}', f'Near zero, yet with last month\'s rain r is {F["clinic_r1"]:.2f}. A delay can hide a real link.']],
                   widths=[3.8, 1.2, 7.0], icons=['people', 'cloud', 'sun', 'clinic'], note='Cut-offs such as strong and weak are judgement, not law. Always draw the scatter plot before you trust r.',
                   notes=(f'Let me show you how to read r. Footfall and orders, {F["r_foot_orders"]:.2f}: strong and positive, but it does not say which causes which. Rainfall and orders, {F["r_rain_orders"]:.2f}: weak and negative, with a lot of scatter. '
                          f'Footfall and rainfall, {rf(F["r_foot_rain"])}: about zero. The last row is a warning from the District Clinics file. Malaria cases and rainfall in the same month have r of {F["clinic_r0"]:.2f}, almost nothing. '
                          f'But pair each month\'s cases with the previous month\'s rain and r is {F["clinic_r1"]:.2f}. A delay can hide a real link. Words like strong and weak are judgement, so always draw the scatter plot first. Where might a delay hide a link in your data?')))

    # ------------------------------------------------------------------ 16 confounder
    g = F['g']
    S_.append(dict(kind='idea', title='A confounder influences both variables, so they look linked',
                   visual=dict(kind='dsb_confound', top=dict(head='Branch size', text=f'B01: {F["sizes"]["B01"]:.1f}. B07: {F["sizes"]["B07"]:.1f}.'), left=dict(head='Footfall', text=f'B01: {n(g.loc["B01", "footfall"])} a week. B07: {n(g.loc["B07", "footfall"])}.'),
                               right=dict(head='Orders', text=f'B01: {g.loc["B01", "orders"]:.1f} a week. B07: {g.loc["B07", "orders"]:.1f}.'), middle=f'r = {F["r_foot_orders"]:.2f}',
                               foot=f'Inside one branch, r is lower: {F["r_within_min"]:.2f} to {F["r_within_max"]:.2f}.'),
                   lead='Confounder (confounding variable): a variable that drives both of the variables you compare.',
                   points=['Larger branches have more footfall and more orders.', 'Part of the 0.84 comes from branch size.', 'Correlation alone cannot show cause.'],
                   notes=(f'Here is why correlation is not causation. A confounder is a variable that influences both of the variables you compare, so they look linked even if neither causes the other. '
                          f'Look at branch size. Kampala Central, size {F["sizes"]["B01"]:.1f}, has about {n(g.loc["B01", "footfall"])} visitors and {g.loc["B01", "orders"]:.1f} orders a week. Fort Portal, size {F["sizes"]["B07"]:.1f}, has {n(g.loc["B07", "footfall"])} and {g.loc["B07", "orders"]:.1f}. '
                          f'Size lifts both, which inflates the {F["r_foot_orders"]:.2f}. Inside a single branch the correlation is lower, from {F["r_within_min"]:.2f} to {F["r_within_max"]:.2f}. Footfall may still cause some orders, but the correlation alone cannot separate the two stories. Would flyers that raise footfall raise orders by the same amount?')))

    # ------------------------------------------------------------------ 17 branch table
    S_.append(dict(kind='table', title='Bigger branches have more footfall and more orders, so size confounds the correlation',
                   headers=['Branch', 'Size (relative)', 'Mean footfall a week', 'Mean orders a week'], rows=F['branch_rows'], widths=[4.4, 2.4, 2.8, 2.6], icons=['shop'] * 8,
                   note=f'Across the 8 branches, size and mean footfall have r = {F["r_size_foot"]:.3f}, and size and mean orders have r = {F["r_size_orders"]:.3f}.',
                   notes=(f'This table shows the confounder in numbers. For each of the eight branches, the relative size, then its mean weekly footfall and mean weekly orders. As size rises, both rise. '
                          f'Across the eight branches, size and mean footfall have r of {F["r_size_foot"]:.3f}, and size and mean orders have r of {F["r_size_orders"]:.3f}. The data is generated, so the link is unusually tight. So when a manager sees the correlation of {F["r_foot_orders"]:.2f} between footfall and orders and wants to fund flyers, '
                          'the first question is: how much of that comes from branch size? The best test is an experiment, such as flyers at a few branches for some weeks against similar branches without. Session 12 covers that. What would you compare?')))

    # ------------------------------------------------------------------ 18 bias
    S_.append(dict(kind='compare', title='Selection bias and survivorship bias both come from records that are missing',
                   left=dict(head='Selection bias', icon='question', points=['Records not chosen by chance.', f'Workbook means: loyalty {n(B["loyal_mean"])}, {n(B["walk_n"])} walk-ins {n(B["walk_mean"])}.', f'Full file: {n(B["full_loyal_mean"])} and {n(B["full_walk_mean"])}.']),
                   right=dict(head='Survivorship bias', icon='flag', points=['Studying only what is still there.', 'Hypothetical: judging a strategy only from branches that are still open.']),
                   verdict='Ask who or what could not get into the sample.',
                   notes=(f'Two ways a sample misleads you. Selection bias happens when records are chosen by something other than chance. If you report only loyalty orders, you leave out {n(B["walk_n"])} walk-in orders, {B["walk_n"] / N * 100:.0f} percent of the workbook. '
                          f'Their mean is {n(B["walk_mean"])} against {n(B["loyal_mean"])}, lifted by one huge walk-in order. In the full file the two means are close, {n(B["full_walk_mean"])} and {n(B["full_loyal_mean"])}, so here the effect is mild, but you only know that after you check. '
                          'Survivorship bias is studying only what remains. This example is hypothetical: judging a branch strategy from branches that are still open hides the ones that closed. What might be missing from a table you use at work?')))

    # ------------------------------------------------------------------ 19 use at work
    S_.append(dict(kind='table', title='Where you will use this at work: say how far a figure can sit from the truth, and what else could explain it',
                   headers=['Your job', 'The question', 'What today lets you do'],
                   rows=[['Credit analyst auditing a loan book, using SQL', 'We checked a sample of loans. How far can the sample default rate sit from the whole book?', 'Report the standard error with the sample figure.'],
                         ['Monitoring and evaluation officer running a household survey', 'Is a sample of 300 households enough?', 'Estimate the standard error, and say who is missing from the sample.'],
                         ['Sales analyst at a retail chain, using Excel', 'Busy shops sell more. Do we fund flyers?', 'Name a confounder, such as branch size, before you spend.'],
                         ['Health records officer at a district office, using pandas', 'Do rainy months bring malaria cases?', 'Pair each month\'s malaria_cases with last month\'s rainfall_mm in the same district.']],
                   widths=[3.7, 4.4, 3.9], icons=['coin', 'people', 'shop', 'clinic'],
                   notes=('Where will you use this on Monday? Four examples. A credit analyst auditing a loan book checks a sample of loans and reports the standard error with the sample default rate. '
                          'A monitoring and evaluation officer running a household survey estimates the standard error of a sample of three hundred households and says who might be missing. '
                          'A sales analyst names a confounder such as branch size before funding flyers. And a health records officer tests a lag between rainfall and malaria cases, and plots the data before trusting r. Which of these is closest to your job?')))

    # ------------------------------------------------------------------ 20 bridge
    S_.append(dict(kind='code', title='Read the recipe before the lab: five formulas run the whole lab',
                   code='=INDEX(orders!$G$2:$G$2001,1+INT(RAND()*2000))\n=AVERAGE(A2:AD2)\n=STDEV(AE2:AE201)\n=COUNTIF(AE2:AE201,"<"&AVERAGE(orders!G2:G2001))\n=CORREL(branch_weeks!C2:C833,branch_weeks!F2:F833)',
                   reads=['Line 1 draws one random order. Fill it right to AD for one sample of 30.', 'Line 2 gives the sample mean of that row. Fill down to row 201.', f'Line 3 is the standard error estimate from your 200 means: about {n(rg["sd"][0])} to {n(rg["sd"][1])}.',
                          f'Line 4 counts how many sample means fall below the population mean: about {n(rg["below_mu"][0])} to {n(rg["below_mu"][1])} of 200.', f'Line 5 gives r for footfall and orders: {F["r_foot_orders"]:.2f}.'],
                   notes=(f'Before the lab, read the five formulas that do the work. Line one draws one random order. Fill it right to column AD for one sample of thirty. Line two averages that row, the sample mean, and you fill it down to row 201. '
                          f'Line three, STDEV of the two hundred means, estimates the standard error. Expect a value between about {n(rg["sd"][0])} and {n(rg["sd"][1])}. '
                          f'Line four counts how many sample means fall below the population mean. Expect between about {n(rg["below_mu"][0])} and {n(rg["below_mu"][1])}. A value just outside a range is not necessarily an error: freeze a new run and check again. Line five is CORREL on the branch weeks tab. It gives {F["r_foot_orders"]:.2f}, the same for everyone because it uses no random numbers. Why do the first four differ between learners?')))

    # ------------------------------------------------------------------ 21 divider
    S_.append(dict(kind='divider', title='Part 2: the Sheets lab', lead='Close the slides. Open the sheet.', section='Lab',
                   notes=('That is the end of the ideas. Everything you need is on the slides you have just seen, and the lab sheet repeats each step. '
                          'Open the Lakeside Mart workbook in Google Sheets, or in Excel if you prefer. Add a new tab and call it simulation. You will build two hundred samples on it, then work on correlation and bias. '
                          'Your random numbers will differ from your neighbour\'s, and that is the point. In every task, predict the answer first, then compute it, then write what you found.')))

    # ------------------------------------------------------------------ 22 lab map
    S_.append(dict(kind='steps', title='The lab has five steps, and you keep a simulation tab at the end',
                   steps=[dict(head='1 Population', text='Mean and share', icon='folder'), dict(head='2 Simulate', text='200 samples of 30', icon='switch'), dict(head='3 Read', text='Spread and standard error', icon='bars'),
                          dict(head='4 Correlate', text='CORREL, one branch', icon='chart'), dict(head='5 Question', text='Bias and confounder', icon='magnifier')], highlight=None,
                   caption='Eight tasks in 45 minutes. For each task, predict the answer, compute it, then write it on your simulation tab.',
                   notes=('Here is the map of the lab. Step one, find the population mean and the share of large orders. Step two, build the simulation: two hundred samples of thirty orders, frozen, with a histogram. '
                          'Step three, read the spread of the sample means, compare it with the standard error formula, and repeat with samples of five. Step four, use CORREL on all weeks and on one branch. '
                          'Step five, compare loyalty and walk-in orders, and write three sentences on a confounder. In every task, predict first. Please do not skip the predictions.')))

    # ------------------------------------------------------------------ 23 check numbers
    S_.append(dict(kind='table', title='Check your numbers: fixed answers and ranges for your random ones', headers=['What you compute', 'You should get'],
                   rows=[['Mean of the orders, and orders above 100,000', f'{mu:,.2f} and {n(F["n100k"])}'], ['Formula =STDEV.P(orders!G2:G2001)/SQRT(30)', n(S['se30'])],
                         ['Smallest and largest sample mean', f'{n(rg["min"][0])} to {n(rg["min"][1])}, and {n(rg["max"][0])} to {n(rg["max"][1])}'],
                         ['STDEV of the 200 means (n = 30)', f'{n(rg["sd"][0])} to {n(rg["sd"][1])}'], ['Sample means below the population mean', f'{n(rg["below_mu"][0])} to {n(rg["below_mu"][1])} of 200'],
                         ['STDEV for n = 5 over n = 30', f'{sd_ratio_lo:.1f} to {sd_ratio_hi:.1f}'],
                         ['r for footfall and orders: all weeks, then B01 only', f'{F["r_foot_orders"]:.2f} and {F["r_b1_foot"]:.2f}'], ['Mean order of loyalty orders and of walk-ins', f'{n(B["loyal_mean"])} and {n(B["walk_mean"])}']],
                   widths=[6.4, 5.6], icons=['calculator', 'calculator', 'bars', 'bars', 'bars', 'bars', 'chart', 'person'], note='Ranges cover the middle 98 percent of 5,000 repeats of this lab. If you fall outside, look for a range that is too short.',
                   notes=('Use this table as your own self-check. Nobody marks it. The first, second, seventh and eighth rows have one fixed answer. The rows about your sample means are ranges, because your random numbers are your own. '
                          'The ranges come from repeating the whole exercise five thousand times and keeping the middle ninety-eight percent. If your number falls outside, the most common causes are a range that stops early, a block you forgot to freeze, or a sample row shorter than thirty cells. '
                          'Do not change a number to make it match. What does it mean if your standard deviation of the means is near fifty-seven thousand?')))

    # ------------------------------------------------------------------ 24 error cards
    S_.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                   rows=[['Your numbers change whenever you edit a cell', 'The block is still live RAND formulas.', 'Copy the block, then Paste special, Values only.'],
                         ['#REF! or #NAME? in the INDEX formula', 'The tab name is missing or misspelt.', 'Write orders!$G$2:$G$2001 with the tab name and dollar signs.'],
                         ['All 200 means are the same', 'The block was pasted as values after one draw.', 'Fill the formula again, then freeze the whole block.'],
                         ['Standard deviation near 128,000', 'You took STDEV of the orders, not of the 200 means.', 'Point STDEV at the AE column, AE2:AE201.'],
                         ['CORREL gives #N/A', 'The two ranges have different lengths.', 'Use C2:C833 and F2:F833, both 832 rows.']],
                   widths=[3.7, 4.2, 4.1], icons=['cross', 'cross', 'cross', 'cross', 'cross'],
                   notes=('Five messages you may meet. If your numbers change whenever you touch a cell, the block still holds live RAND formulas, so paste values. A hash REF or hash NAME in the INDEX formula means the tab name is missing or misspelt. '
                          'If all the means are identical, you froze the block after a single draw, so fill the formula again. A standard deviation near one hundred and twenty-eight thousand means you pointed STDEV at the orders and not at the means. '
                          'And hash N A from CORREL means the two ranges have different lengths. Read the message first. It usually tells you the answer.')))

    # ------------------------------------------------------------------ 25 exit check
    S_.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                   rows=[['Samples of 30 give a standard error of 23,381 UGX. What happens to it with samples of 120?', 'It halves, to about 11,690, because it is sigma divided by the square root of n.'],
                         ['A manager sees r = 0.84 between footfall and orders and wants to fund flyers. What do you say?', 'Branch size is a confounder: it lifts both. Inside one branch r is lower. Test flyers at some branches against similar branches without.'],
                         ['Why is reporting only loyalty-card orders risky?', 'It is selection bias: the records were chosen by something other than chance, and walk-in shoppers are left out.']],
                   widths=[5.6, 6.4], icons=['bars', 'chart', 'person'],
                   notes=('Last, the exit check. Three questions. Write your answers in your notes before you look at mine. One, samples of thirty give a standard error of twenty-three thousand three hundred and eighty-one shillings. What happens to it with samples of a hundred and twenty? '
                          'Two, a manager sees an r of zero point eight four between footfall and orders and wants to fund flyers. What do you say? Three, why is reporting only loyalty card orders risky? '
                          'The short answers are on the slide. If you got all three, you are ready for Session 5. If one surprised you, look at that part of your simulation tab again tonight.')))

    # ------------------------------------------------------------------ sheet tasks
    sess['sheet_tasks'] = [
        dict(task='Population. On the orders tab, find the mean of all 2,000 order values with =AVERAGE(orders!G2:G2001) and the share of orders above 100,000 UGX with =COUNTIF(orders!G2:G2001,">100000")/COUNT(orders!G2:G2001). Compare the mean with the full-file mean of 47,491 UGX. How big is the gap, and what do we call it?',
             answer=f'Mean {mu:,.2f} UGX. {n(F["n100k"])} orders are above 100,000, a share of {F["p100k"]:.4f} ({F["p100k"] * 100:.2f} percent). The workbook mean is about {n(mu - B["full_mean"])} UGX above the full-file mean of {n(B["full_mean"])}. That gap is sampling error: the workbook is itself a sample of the full file.'),
        dict(task='Simulate. Add a tab called simulation. In A2 put =INDEX(orders!$G$2:$G$2001,1+INT(RAND()*2000)). Fill right to AD2. In AE2 put =AVERAGE(A2:AD2). Select A2:AE2 and fill down to row 201. Copy the block, then Paste special, Values only. Draw a histogram of column AE. Predict first: will the 200 means be spread out or clustered?',
             answer=f'Column AE holds 200 sample means. Yours differ from everyone else\'s. Ranges (middle 98 percent of 5,000 repeats of this task): the smallest mean is between about {n(rg["min"][0])} and {n(rg["min"][1])}, the largest between about {n(rg["max"][0])} and {n(rg["max"][1])}. '
                    'The histogram leans left with a long tail to the right, as in the slide. The seeded run on the slides gave a smallest mean of ' + f'{n(S["min30"])} and a largest of {n(S["max30"])}.'),
        dict(task='Read the spread. In spare cells find the AVERAGE, STDEV, MIN and MAX of column AE. Compare the average with the population mean, and the STDEV with =STDEV.P(orders!G2:G2001)/SQRT(30). What is the STDEV of the 200 sample means called?',
             answer=f'AVERAGE of the means: between about {n(rg["avg"][0])} and {n(rg["avg"][1])}, close to {n(mu)}. STDEV: between about {n(rg["sd"][0])} and {n(rg["sd"][1])}. The formula gives {n(S["se30"])}. The STDEV of the sample means is the standard error of the mean, and the simulation approximates the formula. '
                    'Any single sample can sit far from the population mean, yet the 200 means centre on it.'),
        dict(task='Skew. Use =COUNTIF(AE2:AE201,"<"&AVERAGE(orders!G2:G2001)) to count how many of your 200 sample means fall below the population mean. Predict: about half, or more than half? Say why.',
             answer=f'Expect between about {n(rg["below_mu"][0])} and {n(rg["below_mu"][1])} of the 200 (the seeded run gave {S["below_mu"]}). It is more than half because order values are right-skewed: most samples of 30 contain none of the few huge orders and give a mean below the population mean, while the few samples that catch one give a very high mean.'),
        dict(task='Sample size. In AF2 put =AVERAGE(A2:E2) (the first 5 orders only) and fill down to row 201. Copy the column and Paste special, Values only. Find the STDEV of column AF and divide it by the STDEV of column AE. Predict first: bigger or smaller than 1?',
             answer=f'STDEV of the n = 5 means: between about {n(rg["sd5"][0])} and {n(rg["sd5"][1])}; the formula gives {n(S["se5"])}. Divided by the STDEV of the n = 30 means the ratio is between about {sd_ratio_lo:.1f} and {sd_ratio_hi:.1f}, near the theoretical {F["se_ratio"]:.2f} (the square root of 30 divided by 5, that is the square root of 6). Smaller samples have a larger standard error.'),
        dict(task='Correlation. On the branch_weeks tab find =CORREL(C2:C833,F2:F833) for footfall and orders and =CORREL(D2:D833,F2:F833) for rainfall and orders. Then repeat both for Kampala Central only (B01, rows 2 to 105). Predict whether the B01 correlation is higher or lower.',
             answer=f'All {F["weeks_n"]} weeks: footfall and orders r = {F["r_foot_orders"]:.2f} ({F["r_foot_orders"]:.4f}); rainfall and orders r = {F["r_rain_orders"]:.2f} ({F["r_rain_orders"]:.4f}). Kampala Central only ({F["b1_rows"]} weeks): footfall and orders r = {F["r_b1_foot"]:.2f} ({F["r_b1_foot"]:.3f}); rainfall and orders r = {F["r_b1_rain"]:.2f} ({F["r_b1_rain"]:.3f}). '
                    f'The footfall link is lower inside one branch. The eight branches on their own give {F["r_within_min"]:.2f} to {F["r_within_max"]:.2f}.'),
        dict(task='Selection bias. Compare loyalty orders and walk-in orders: =AVERAGEIF(orders!D2:D2001,"<>",orders!G2:G2001) and =AVERAGEIF(orders!D2:D2001,"",orders!G2:G2001) for the means, =COUNTIF(orders!D2:D2001,"<>") and =COUNTBLANK(orders!D2:D2001) for the counts. Which bias would you introduce by reporting only loyalty orders, and does it matter here?',
             answer=f'Loyalty orders: {n(B["loyal_n"])} with a mean of {n(B["loyal_mean"])} (median {n(B["loyal_median"])}). Walk-in orders: {n(B["walk_n"])} with a mean of {n(B["walk_mean"])}, lifted by the single {n(B["max"])} order, which has no customer_id (median {n(B["walk_median"])}). '
                    f'Reporting only loyalty orders would be selection bias. In the full file the two means are almost equal ({n(B["full_loyal_mean"])} and {n(B["full_walk_mean"])}), so the effect is mild, but you only know that after you check.'),
        dict(task='Confounder. On branch_weeks use =AVERAGEIF(A2:A833,"B01",C2:C833) and =AVERAGEIF(A2:A833,"B01",F2:F833) (and the same for B07) for mean footfall and orders. A manager sees r = 0.84 and wants flyers to raise footfall. Write three sentences: name a confounder, say what the inside-one-branch figures tell you, and suggest how to test the idea.',
             answer=f'B01 (size {F["sizes"]["B01"]:.1f}) averages {n(g.loc["B01", "footfall"])} visitors and {g.loc["B01", "orders"]:.1f} orders a week; B07 (size {F["sizes"]["B07"]:.1f}) averages {n(g.loc["B07", "footfall"])} and {g.loc["B07", "orders"]:.1f}. Model answer: Branch size is a confounder, because large branches have more of both. '
                    f'Inside a single branch the correlation is lower, between {F["r_within_min"]:.2f} and {F["r_within_max"]:.2f}, so part of the {F["r_foot_orders"]:.2f} comes from branch size. Test flyers at a few branches for some weeks against similar branches without them before spending widely.'),
    ]

    # ------------------------------------------------------------------ facilitator
    sess['facilitator'] = dict(
        prep=['Open the deck and the workbook lakeside_for_sheets.xlsx in Google Sheets before anyone arrives. Share the file so every learner can make their own copy (File, Make a copy).',
              'Build the simulation tab on your own copy first. Check that the INDEX and RAND formula, the freeze step and the AVERAGEIF with "" criterion work in Sheets. The answer ranges were computed in numpy, not yet in Sheets.',
              'Write the check table (slide 28 of the deck) on the board before the lab.',
              'Concepts run with laptops closed. Ask learners to open the workbook only after the Part 2 divider.',
              'Warn learners that every RAND result differs, so no two learners will have the same numbers. The ranges on the check slide are what to compare.'],
        misconceptions=[('A sample that differs from the population means someone made a mistake', 'Sampling error comes from chance in which records were drawn. It is expected, and the standard error measures its typical size.'),
                        ('A bigger population needs a proportionally bigger sample', 'The standard error depends on the sample size and the spread, with a square root. Quadrupling n halves it.'),
                        ('A high correlation shows that one variable causes the other', f'It shows association only. Branch size lifts both footfall and orders, and r drops inside one branch.'),
                        ('r = 0 means no relationship at all', f'Pearson r measures straight-line association. Rain and malaria in the clinic file have r = {F["clinic_r0"]:.2f} in the same month but {F["clinic_r1"]:.2f} with a one-month lag.'),
                        ('Standard deviation and standard error are the same', 'Standard deviation describes the spread of the records. Standard error describes the spread of a statistic, such as the sample mean, across samples.')],
        probes=[('What is the difference between a parameter and a statistic?', 'A parameter describes a population. A statistic is computed from a sample.'),
                ('What does the standard error measure?', 'How far a sample statistic, such as the mean, typically sits from the population value.'),
                ('Why do we freeze the simulation block?', 'RAND recalculates on every edit, so the numbers would change while you chart them.'),
                ('How do you halve the standard error?', 'Quadruple the sample size.'),
                ('Give a confounder in the Lakeside data.', 'Branch size: it lifts both footfall and orders.'),
                ('What is sampling with replacement?', 'Each draw is put back, so the same record can be picked twice.'),
                ('Why is reporting loyalty orders only risky?', 'Selection bias: walk-in shoppers are missing.')],
        lab_steps=[('Task 1: population', f'Mean {mu:,.2f}; {n(F["n100k"])} orders above 100,000. Make sure the word sampling error is used for the gap.'),
                   ('Task 2: build the simulation', 'Check that A2 uses $ signs and that the block is frozen. Common error: a fill that stops at row 100.'),
                   ('Task 3: the spread', f'STDEV of the means near {n(S["se30"])}; the formula answer is {n(S["se30"])}.'),
                   ('Task 4: below the mean', f'About {n(rg["below_mu"][0])} to {n(rg["below_mu"][1])}. Ask why it is more than half.'),
                   ('Task 5: n = 5', f'Ratio near {F["se_ratio"]:.1f}.'),
                   ('Task 6: correlation', f'{F["r_foot_orders"]:.2f}, {F["r_rain_orders"]:.2f}; then {F["r_b1_foot"]:.2f} and {F["r_b1_rain"]:.2f} for B01.'),
                   ('Task 7: selection bias', f'{n(B["loyal_mean"])} against {n(B["walk_mean"])}. Ask learners to check the medians too.'),
                   ('Task 8: three sentences', 'A confounder is named, the inside-one-branch figures are used, and a test is suggested.')],
        rescue=['If the concepts run over, shorten the correlation table (slide 20) and the branch table (slide 22) to a quick look; the lab covers both.',
                'If only 30 minutes of lab remain, do tasks 1, 2, 3, 6 and 8 and set the rest as homework.',
                'If a learner has Excel, use =INDEX(orders!$G$2:$G$2001,1+INT(RAND()*2000)); AVERAGEIF with "" works in Excel. Paste special, Values is in the Paste menu.',
                'If a learner has no laptop, pair them with a neighbour: one types, one predicts aloud.'],
        after=['Share the workbook and this deck again for learners who were absent.', 'Ask each learner to save the simulation tab and bring one question about their own data to Session 5.', 'Note any question you could not answer and open the next session with it.'],
        lab_answer_key=[['Task 1 PREDICT: will the workbook mean equal the full-file mean?', f'No: {n(mu)} against {n(B["full_mean"])}. The difference is sampling error.'],
                        ['Task 2 PREDICT: spread out or clustered?', 'Spread out, with a long tail to the right.'],
                        ['Task 3 READ: how does your STDEV compare with the formula?', f'Close to {n(S["se30"])}, within the range {n(rg["sd"][0])} to {n(rg["sd"][1])}.'],
                        ['Task 4 READ: why more than half below?', 'Right-skewed values: most samples miss the huge orders.'],
                        ['Task 5 CHANGE: use 20 orders instead of 5.', f'The standard error falls to about {n(S["sigma"] / np.sqrt(20))}.'],
                        ['Task 6 READ: is the B01 correlation higher or lower?', f'Lower: {F["r_b1_foot"]:.2f} against {F["r_foot_orders"]:.2f}. Branch size was inflating the overall figure.'],
                        ['Task 7 READ: does selection bias matter here?', 'Only mildly: the full-file means are almost equal. You know that only after checking.'],
                        ['Task 8 CHANGE: suggest an experiment.', 'Flyers at a few branches against similar branches without, over several weeks.']])
    return sess
