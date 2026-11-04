"""Session 12: Inference, is the difference real? (standard error, confidence interval, bootstrap, hypothesis test, p-value, permutation test, Welch t test,
test of two proportions, effect size, false positives, multiple comparisons, optional stopping). Python lab (needs SciPy and statsmodels in Colab).

Every number on a slide is computed in f12_facts.facts() with numpy and pandas only (SciPy and statsmodels are not installed where this deck was written).
Where a slide says that SciPy or statsmodels gives the same value, that is the mathematical definition of the same statistic. The SciPy calls were not run when the deck was built.
"""
import importlib.util
from pathlib import Path

_d = Path(__file__).resolve().parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name, _d / f'{name}.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


f12 = _load('f12_facts')
f11 = _load('f11_facts')
n = f12.n
GOLD_C, INK_C, RED_C = '#E0BE36', '#111111', '#AE2525'

SN_A = ("import numpy as np\n"
        "import pandas as pd\n"
        "test = pd.read_csv('offer_test.csv')\n"
        "spend = test.next_month_spend_ugx\n"
        "offer = spend[test.group == 'offer'].to_numpy()\n"
        "control = spend[test.group == 'control'].to_numpy()\n"
        "lift = offer.mean() - control.mean()\n"
        "v_o = offer.var(ddof=1) / len(offer)\n"
        "v_c = control.var(ddof=1) / len(control)\n"
        "se = np.sqrt(v_o + v_c)\n"
        "print(round(lift), round(se), round(lift / se, 2))\n"
        "print(f'{lift - 1.96*se:.0f} {lift + 1.96*se:.0f}')")
SN_B = ("rng = np.random.default_rng(42)\n"
        "boot = [rng.choice(offer, len(offer)).mean()\n"
        "        - rng.choice(control, len(control)).mean()\n"
        "        for _ in range(5000)]\n"
        "low, high = np.percentile(boot, [2.5, 97.5])\n"
        "print(round(low), round(high))")
SN_C = ("values = spend.to_numpy()\n"
        "is_offer = (test.group == 'offer').to_numpy()\n"
        "rng = np.random.default_rng(42)\n"
        "gaps = []\n"
        "for _ in range(5000):\n"
        "    s = rng.permutation(is_offer)\n"
        "    gaps.append(values[s].mean() - values[~s].mean())\n"
        "hits = (np.abs(gaps) >= abs(lift)).sum()\n"
        "print(hits, hits / 5000)")


def build():
    F = f12.facts()
    G = f11.facts()
    ns, outA = f12.run_snippet(SN_A)
    ns, outB = f12.run_snippet(SN_B, ns)
    ns, outC = f12.run_snippet(SN_C, ns)
    la = outA.splitlines()
    assert la[0] == f'{round(F["lift"])} {round(F["se_lift"])} {F["t"]:.2f}' and la[1] == f'{round(F["ci_lift"][0])} {round(F["ci_lift"][1])}', outA
    assert outB == f'{round(F["boot_ci"][0])} {round(F["boot_ci"][1])}' and outC == f'{F["perm_hits"]} {F["p_perm"]}', (outB, outC)
    lift, se = F['lift'], F['se_lift']
    lo, hi = F['ci_lift']
    sc = F['sampling']
    rb, bt, br_ = G['rb'], G['top_count'], G['top_rate']
    pt = F['p_t']
    lift_plan = 5000   # a planning lift for the sample size slide
    cost = 3000   # hypothetical offer cost per customer, labelled as such on the slide
    sess = dict(
        num=12, block='Module C: Analyse and explain', short_title='Inference',
        title='Inference: is the difference real, or could it be luck?',
        question='When two groups differ, how do I know the gap is real and that chance does not explain it?',
        outcomes=['Compute and read a standard error, a 95 percent confidence interval and a bootstrap interval',
                  'Run and read a permutation test, a Welch two-sample t-test and a test of two proportions, with the null hypothesis and the p-value',
                  'Report a decision with its effect size, and avoid false positives from many tests and from stopping early'],
        outcome_icons=['calculator', 'check', 'shield'],
        outcome_note=('Here is what you can do by the end of today. You can measure how much a sample average varies from one sample to the next, which is sampling variability, and name it with the standard error. You can then build a confidence interval and a bootstrap interval from it. '
                      'You can run a permutation test, a t-test and a test of two proportions, and say exactly what a p-value tells you and what it does not. '
                      'And you can report a decision with its effect size, and you know the two ways these tests mislead people: running many tests, and stopping early when the result looks good. The data is the Lakeside Mart loyalty offer test.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: picture, plain words, one example by hand'), (10, 'Break'), (45, 'Lab: predict, run, read, change'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: concepts first, then a Python lab in Colab',
        plan_caption='Ideas and pictures first. Then you open the notebook and test the offer yourself.',
        plan_note=('We have two hours. The first ten minutes bring back Session 11 and set the question for today. Then forty-five minutes of concepts with laptops closed, because the pictures carry most of the ideas. '
                   'After a ten minute break you open the notebook in Google Colab for a forty-five minute lab. You compute the numbers by hand with NumPy, then check them against SciPy. The last ten minutes are an exit check and what you keep. '
                   'Please protect the lab time.'),
        recall_from='Session 11',
        recall=[(f'Branch {bt} has the most returns. Is it the branch with the worst returns problem?', f'Not yet known. Divide by lines sold to get the rate: {bt} has {rb.per_100[bt]:.2f} per 100 lines and {br_} has {rb.per_100[br_]:.2f}, the highest.'),
                ('What three parts does every finding need?', 'A number, a comparison and a limit.'),
                ('Which chart shows whether two numeric variables move together?', 'A scatter plot, drawn with sns.scatterplot. The correlation r puts a number on it.')],
        words=[('Standard error (SE)', 'How much a sample mean varies from one random sample to the next. It is the standard deviation divided by the square root of the sample size.'),
               ('Confidence interval (CI)', 'A range built from the data. A 95 percent interval is the estimate plus or minus 1.96 standard errors.'),
               ('Null hypothesis (H0) and p-value', 'H0 says there is no real difference. The p-value says how often chance alone would give a gap at least this big if H0 were true.'),
               ('Effect size', 'How big the gap is, in units a person can feel, such as shillings or percent. Practical significance asks whether that size matters.'),
               ('False positive (Type I error)', 'Declaring a difference when there is none. Running many tests, or stopping early, makes it far more likely.')],
        word_icons=['calculator', 'chart', 'question', 'coin', 'shield'],
        words_note=('Five words for today. The standard error is how much a sample mean varies from sample to sample. A confidence interval is a range built from it. '
                    'The null hypothesis says nothing is going on, and the p-value measures how surprising the data are if that is true. Effect size is how big the gap is in useful units. '
                    'And a false positive, or Type I error, is a difference declared where none exists. Each word has a cousin in your spreadsheet, and we will see them in action.'),
        keep='Keep your inference notebook: the offer test done five ways (formula, bootstrap, permutation, t-test, two proportions) and a decision paragraph with the lift, its interval, the p-value and the limit.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab file', value='Offer test notebook'), dict(label='Your writing', value='A decision note'), dict(label='Next session', value='Regression')]),
        keep_title='Save your notebook with its decision note',
        next='Session 13: Regression. How much does one thing change when another changes? We model weekly orders and reach Project milestone 2.', next_label='Next session',
        keep_note=('Before you go, save your notebook with the decision note. That paragraph is the keepsake from today: it states the lift, its confidence interval, the p-value, the effect size and one limit, in words a manager can use. '
                   'Check that you could defend each number. Next session we move from comparing two groups to modelling a number with regression, and it brings Project milestone 2. '
                   'If anything about p-values is still unclear, write the question down and bring it.'),
        cover_note=('Welcome back. A gap between two averages is easy to find. Deciding whether it is luck is the job today. '
                    'Last session you explored data and found findings worth reporting. Today we test one: did the Lakeside Mart loyalty offer raise how much customers spend? '
                    'By the end you will have a confidence interval, a p-value and a decision you can defend, and you will know the two ways these tests mislead people.'),
        use_at_work='Test whether a gap between two groups is real, report its size and interval, and avoid false alarms.',
        slides=[])
    S = sess['slides']

    # 1 answers
    S.append(dict(kind='table', title='Answers to the three questions from Session 11', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in sess['recall']], widths=[5.2, 6.8], icons=['shop', 'notebook', 'pin'],
                  notes=(f'Here are the answers to the three warm-up questions. A branch with the most returns is not necessarily the worst, because a big branch sells more. Divide returns by lines sold to get the rate. Branch {bt} has the most returns and the lowest rate, and {br_} has the highest rate. '
                         'Every finding needs a number, a comparison and a limit. And a scatter plot, drawn with seaborn scatterplot, shows whether two numeric variables move together. '
                         'Today we add one more habit to the finding: before you report a gap, ask whether it could be luck. Which of the three would you answer differently now?')))

    # 2 A/B test
    S.append(dict(kind='idea', title='An A/B test: chance decides who gets the offer (treatment) and who does not (control)',
                  visual=dict(kind='sheet', headers=['customer_id', 'group', 'next_month_spend_ugx', 'returned_within_30d'], rows=[[str(r.customer_id), str(r.group), n(r.next_month_spend_ugx), str(int(r.returned_within_30d))] for r in F['test'].head(6).itertuples()], hl=[1, 1], size=15),
                  lead='Random assignment makes the groups alike on average in everything except the offer.',
                  points=['Each record is one loyalty customer.', f'{n(F["n_o"])} got the offer (treatment). {n(F["n_c"])} did not (control).', 'The outcome is next month spend.'],
                  notes=(f'Today the question comes from a manager. We gave a loyalty offer to some customers. Did it work? The test was set up by chance. Lakeside Mart took {n(F["n"])} loyalty customers and gave a random half the offer. '
                         f'That is an A/B test, a controlled experiment. The {n(F["n_o"])} customers who got the offer are the treatment group, and the {n(F["n_c"])} who did not are the control group. '
                         'Because chance chose who got what, the two groups should be alike on average in everything except the offer, and the larger the groups the better this works. Each record is one customer. The outcome we look at is the spend in the next month. '
                         'Why does random assignment matter so much?')))

    # 3 lift
    S.append(dict(kind='stat', title='The lift in average spend is 5,044 UGX. Is it the offer, or luck?', big=n(lift),
                  text=f'UGX more per customer in the treatment group: a mean of {n(F["mean_o"])} against {n(F["mean_c"])} in the control group. The lift is the treatment mean minus the control mean.',
                  visual=dict(kind='f_panels', panels=[dict(type='bar', labels=['Control', 'Offer'], values=[round(F['mean_c']), round(F['mean_o'])], hl=[1], hl_color=GOLD_C, fmt='{:,.0f}', pad=1500, ylim=(0, 80000), yk=True, title='Mean spend (UGX)')], ncols=1, left=0.2, right=0.96, bottom=0.12, top=0.88),
                  notes=(f'Here is the result. Offer customers spent {n(F["mean_o"])} shillings next month on average, and control customers spent {n(F["mean_c"])}. The difference is {n(lift)} shillings, which we call the lift: the treatment mean minus the control mean. '
                         f'That is {F["lift_pct"]:.1f} percent more than the control mean. The question for the manager is whether the {n(lift)} comes from the offer or from the luck of who landed in which group. '
                         'To judge luck we first need to measure how much a sample mean varies from one sample to the next. What do you think moves more, a mean of ten customers or a mean of a thousand?')))

    # 4 sampling variability
    S.append(dict(kind='idea', title='Sampling variability: every random sample gives a slightly different mean',
                  visual=dict(kind='f_panels', panels=[dict(type='hist', edges=F['h_means100'][0], counts=F['h_means100'][1], vlines=[(F['pop_mean'], f'population mean {n(F["pop_mean"])}', RED_C, '--')], title='1,000 sample means, 100 customers each', xlabel='Sample mean (UGX)', ylabel='Samples', xk=True, legend='upper right')], ncols=1, left=0.14, right=0.95, bottom=0.17, top=0.9),
                  lead='A sample mean is an estimate of the population mean. Its spread is the standard error.',
                  points=['Population: all 2,500 customers. Sample: 100 drawn at random, with replacement.', f'The 1,000 means range from {n(F["means100"].min())} to {n(F["means100"].max())}.', f'Their standard deviation, {n(sc[100]["sim_se"])}, is the standard error.'],
                  notes=(f'To judge a gap we need to see how much a sample mean varies. For this picture we treat all {n(F["n"])} customers as the population. A sample is a smaller group drawn from it. '
                         f'We draw 100 customers at random, with replacement, find their mean spend, and repeat that a thousand times. This is a Monte Carlo simulation. Each bar counts how many samples gave a mean in that range. '
                         f'The means run from {n(F["means100"].min())} to {n(F["means100"].max())}, around the population mean of {n(F["pop_mean"])}. That spread is called sampling variability, and its standard deviation, {n(sc[100]["sim_se"])} shillings, is the standard error. '
                         'Any one sample is only an estimate. Which sample would you have trusted?')))

    # 5 SE formula
    S.append(dict(kind='formula', title='The standard error of a mean is the standard deviation divided by the square root of n',
                  formulas=[('Formula', r'$\mathrm{SE} = \frac{s}{\sqrt{n}}$'), ('Control group', rf'$\frac{{{n(F["sd_c"])}}}{{\sqrt{{{F["n_c"]}}}}} = {n(F["se_c"])}$')],
                  symbols=[['SE', 'The standard error: the typical distance of a sample mean from the population mean.', f'{n(F["se_c"])} UGX'], ['s', 'The sample standard deviation (ddof=1): the spread of customers.', f'{n(F["sd_c"])} UGX'],
                           ['n', 'The sample size: how many customers.', f'{n(F["n_c"])} control customers']],
                  size=21, note='Excel: =STDEV.S(range)/SQRT(COUNT(range)). NumPy: x.std(ddof=1) / np.sqrt(len(x)).',
                  notes=(f'You do not have to simulate the standard error. There is a formula. The standard error equals the sample standard deviation, s, divided by the square root of the sample size, n. '
                         f'For the control group the standard deviation is {n(F["sd_c"])} shillings and there are {F["n_c"]} customers. The square root of {F["n_c"]} is about 35.4, and the division gives {n(F["se_c"])}. '
                         f'The check on the slide compares the simulation with the formula for samples of 100: the simulation gave {n(sc[100]["sim_se"])} and the formula gives {n(sc[100]["formula_se"])}. They agree. '
                         'In Excel this is STDEV.S divided by the square root of COUNT. What happens to the standard error when n gets bigger?')))

    # 6 SE falls with n
    S.append(dict(kind='wide', title='A bigger sample has a smaller standard error: four times the customers halves it',
                  visual=dict(kind='f_panels', panels=[dict(type='bar', labels=[f'n = {n(m)}' for m in sc], values=[round(sc[m]['sim_se']) for m in sc], fmt='{:,.0f}', pad=150, hl=[1], hl_color=GOLD_C, ylim=(0, 9000), yk=True, title='Simulated standard error of the mean (UGX)', ylabel='UGX')], ncols=1, left=0.08, right=0.98, bottom=0.14, top=0.87),
                  caption=f'Formula values: {", ".join(n(sc[m]["formula_se"]) for m in sc)}. Each bar is 1,000 samples with replacement.',
                  notes=(f'Here is the same experiment with four sample sizes. With 25 customers in each sample the standard error is about {n(sc[25]["sim_se"])} shillings. With 100 it is {n(sc[100]["sim_se"])}. With 400 it is {n(sc[400]["sim_se"])}, and with 1,600 it is {n(sc[1600]["sim_se"])}. '
                         'Each time we multiply the sample by four, the standard error falls to about half. That is the square root in the formula at work. '
                         'It also explains why a test with 2,500 customers can say more than a test with 50. The price is that halving the error costs four times the data. Is that worth it for a test that costs money to run?')))

    # 7 CI formula
    S.append(dict(kind='formula', title='A 95 percent confidence interval is the estimate plus or minus 1.96 standard errors',
                  formulas=[('Formula', r'$\mathrm{CI} = \mathrm{estimate} \pm 1.96 \times \mathrm{SE}$'), ('The lift', rf'$5{{,}}044 \pm 1.96 \times 1{{,}}526 = 2{{,}}054 \ \mathrm{{to}}\ 8{{,}}035$')],
                  symbols=[['estimate', 'The number from the sample. Here the lift.', f'{n(lift)} UGX'], ['SE', 'The standard error of the lift: the square root of the two squared standard errors added.', f'{n(se)} UGX'],
                           ['1.96', 'The critical value for a 95 percent confidence level, from the normal distribution.', '95 percent'], ['CI', 'The interval. It excludes zero when the lift is clearly above or below zero.', f'{n(lo)} to {n(hi)}']],
                  size=22, note='Each group alone: control CI {} to {}. Offer CI {} to {}.'.format(n(F['ci_c'][0]), n(F['ci_c'][1]), n(F['ci_o'][0]), n(F['ci_o'][1])),
                  notes=(f'A confidence interval is built from the standard error. For a 95 percent interval, take the estimate and go 1.96 standard errors below and above it. The number 1.96 comes from the normal distribution, and 95 percent is the confidence level. '
                         f'Our estimate is the lift, {n(lift)} shillings. The standard error of the lift combines the errors of the two groups: the square root of the sum of their squared standard errors, which is {n(se)}. '
                         f'So the interval runs from {n(lo)} to {n(hi)} shillings. It does not include zero. That is the first evidence of a lift. What would zero inside the interval have told us?')))

    # 8 meaning of 95 percent
    S.append(dict(kind='idea', title='What 95 percent means: it describes the method over many samples, not one interval',
                  visual=dict(kind='f_panels', panels=[dict(type='interval', labels=[''] * 30, est=[x[0] for x in F['cover']], low=[x[1] for x in F['cover']], high=[x[2] for x in F['cover']], miss=F['cover_miss'], ref=(F['pop_mean'], 'population mean', GOLD_C), lw=2.2, ms=4, show_labels=False, xlabel='Sample mean and 95% interval (UGX)', xk=True, title='30 samples of 100 customers', legend='lower right')], ncols=1, left=0.06, right=0.97, bottom=0.17, top=0.9),
                  lead='Draw many samples. About 95 in 100 intervals catch the population mean.',
                  points=[f'{F["cover_hits"]} of these 30 intervals catch it. The red ones miss.', f'Over 1,000 samples, {F["cover_rate"]:.1f} percent did.', 'Spend is skewed, so small samples fall a little short of 95.'],
                  notes=(f'This is the most misread idea in statistics. A 95 percent confidence interval describes the method and makes no promise about one interval. We drew 1,000 samples of 100 customers, and built an interval from each. Here are the first 30. '
                         f'The gold line is the true population mean, which we know here. {F["cover_hits"]} of these 30 intervals catch it, and the red ones miss. Over all 1,000 samples, {F["cover_rate"]:.1f} percent caught it. '
                         'That is close to 95, a little short because spend is skewed and each sample is small. So when you report one interval, you are using a method that catches the truth about 95 times in 100. '
                         'Does the picture show that any single interval is guaranteed to catch it?')))

    # 9 bootstrap
    S.append(dict(kind='idea', title='The bootstrap resamples your own data to measure sampling variability without a formula',
                  visual=dict(kind='f_panels', panels=[dict(type='hist', edges=F['h_boot'][0], counts=F['h_boot'][1], vlines=[(F['boot_ci'][0], '2.5th and 97.5th percentiles', GOLD_C, '--'), (F['boot_ci'][1], '_nolegend_', GOLD_C, '--'), (lift, f'observed lift {n(lift)}', RED_C, '-')], title='5,000 bootstrap lifts', xlabel='Lift (UGX)', ylabel='Resamples', xk=True, legend='upper right')], ncols=1, left=0.14, right=0.95, bottom=0.17, top=0.9),
                  lead='Bootstrap: resample each group with replacement, same size, and recompute the lift. Repeat 5,000 times.',
                  points=[f'The spread of the 5,000 lifts is {n(F["boot_se"])}, close to the formula SE {n(se)}.', f'Percentile interval: {n(F["boot_ci"][0])} to {n(F["boot_ci"][1])}.', 'It needs no formula, so it works for medians too.'],
                  notes=(f'The bootstrap is a way to measure the sampling variability from the data you already have. Pretend your sample is the whole world. Draw a new sample of the same size from it, with replacement, so a customer can appear twice. Do that for the offer group and for the control group, and compute the lift. '
                         f'Repeat 5,000 times, with a fixed random seed so the numbers repeat. The 5,000 lifts form this picture. Their standard deviation is {n(F["boot_se"])}, close to the formula answer of {n(se)}. '
                         f'Cut off the lowest 2.5 percent and the highest 2.5 percent, and the ends are {n(F["boot_ci"][0])} and {n(F["boot_ci"][1])}. That is the bootstrap percentile interval, and it agrees with the formula interval. Where would a bootstrap help when no formula exists?')))

    # 10 hypotheses
    S.append(dict(kind='table', title='A hypothesis test asks: how surprising are the data if nothing is going on?',
                  headers=['Term', 'Plain meaning', 'In the offer test'],
                  rows=[['Null hypothesis (H0)', 'There is no real difference. Any gap is chance.', 'The offer does not change average spend.'], ['Alternative hypothesis (H1)', 'There is a real difference.', 'The offer changes average spend.'],
                        ['Test statistic', 'One number that measures the gap against the noise.', f'The lift, or t = {F["t"]:.2f}'], ['p-value', 'How often chance alone gives a gap at least this big, if H0 is true.', f'About {F["p_t"]:.5f} (see the next slides)'],
                        ['Significance level (alpha)', 'The threshold chosen before the test. Usually 0.05.', 'alpha = 0.05'], ['Decision', 'p below alpha: reject H0. Otherwise, keep H0.', f'{F["p_t"]:.5f} is below 0.05: reject H0']],
                  widths=[3.0, 4.6, 4.4], icons=['question', 'flag', 'calculator', 'chart', 'key', 'check'],
                  notes=('Now the logic of a hypothesis test. Start by assuming that nothing is going on. That assumption is the null hypothesis, H0: the offer does not change average spend. The alternative hypothesis, H1, says it does. '
                         'Then compute a test statistic, one number that measures the gap against the noise. The p-value answers a precise question: if H0 were true, how often would chance alone give a gap at least this big? '
                         f'Before the test we choose a threshold called the significance level, alpha, usually 0.05. If the p-value is below alpha, we reject H0. For our test the p-value is about {F["p_t"]:.5f}, so we reject it. Why do we fix alpha before looking at the data?')))

    # 11 permutation
    S.append(dict(kind='idea', title='A permutation test shuffles the group labels to see what chance alone produces',
                  visual=dict(kind='f_panels', panels=[dict(type='hist', edges=F['h_perm'][0], counts=F['h_perm'][1], red_abs=abs(lift), vlines=[(lift, f'observed lift {n(lift)}', RED_C, '-')], title='5,000 gaps from shuffled labels', xlabel='Gap in mean spend (UGX)', ylabel='Shuffles', xk=True, legend='upper left')], ncols=1, left=0.14, right=0.95, bottom=0.17, top=0.9),
                  lead='Shuffle offer and control labels at random. If H0 is true, the labels carry no information.',
                  points=[f'Only {F["perm_hits"]} of 5,000 shuffled gaps were as big as {n(lift)} (red).', f'p = {F["perm_hits"]} / 5,000 = {F["p_perm"]}, or {F["perm_hits"] + 1} / 5,001 = {(F["perm_hits"] + 1) / 5001:.4f}.', 'The p-value is the share of shuffles at least as extreme.'],
                  notes=(f'Here is a test you can do with no formula at all. If the offer has no effect, then which customers are labelled offer and which control is arbitrary. So we shuffle the labels at random, keeping the group sizes, and compute the gap in mean spend. We do that 5,000 times. '
                         f'The histogram shows the gaps that chance alone produces. They centre on zero and spread about {n(F["perm_sd"])} either way. The red bars are shuffles with a gap at least as big as ours, in either direction. '
                         f'Only {F["perm_hits"]} of 5,000 reached that size, so the p-value is {F["perm_hits"]} divided by 5,000, which is {F["p_perm"]}. Many analysts report {F["perm_hits"] + 1} over 5,001, which is {(F["perm_hits"] + 1) / 5001:.4f}, so that p is never exactly zero. Why do we count both directions?')))

    # 12 what p says
    S.append(dict(kind='compare', title='A p-value is easy to misread: know what it says and what it does not',
                  left=dict(head='It says', points=[f'If H0 were true, data this extreme would be rare: p = {F["p_t"]:.5f}.']),
                  right=dict(head='It does not say', points=['The probability that H0 is true.', 'How big the effect is.', 'That the result will repeat.']),
                  verdict='A small p-value is evidence against H0. Effect size tells you how much it matters.',
                  notes=(f'A p-value is easy to misread. It says one thing: if the null hypothesis were true, data as extreme as ours would be rare. Our p-value is {F["p_t"]:.5f}. '
                         'It does not say the probability that the null hypothesis is true. It does not say how big or important the effect is, because a huge sample can give a tiny p-value for a tiny gap. And it does not promise the result will repeat. '
                         'A small p-value is evidence against H0, and the effect size tells you how much it matters. Which of these misreadings have you heard in a meeting?')))

    # 13 Welch t
    S.append(dict(kind='formula', title="Welch's two-sample t-test: the lift divided by its standard error",
                  formulas=[('Test statistic', r'$t = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}$'), ('Offer against control', rf'$t = \frac{{{n(lift)}}}{{{n(se)}}} = {F["t"]:.2f}$')],
                  symbols=[['x-bar 1, x-bar 2', 'The two group means.', f'{n(F["mean_o"])} and {n(F["mean_c"])}'], ['s, n', 'Standard deviation and size of each group. Welch lets the two spreads differ.', f'{n(F["sd_o"])}, {n(F["n_o"])} and {n(F["sd_c"])}, {n(F["n_c"])}'],
                           ['df and p-value', 'Welch-Satterthwaite degrees of freedom, and the two-sided p-value from the t distribution.', f'{F["df"]:.1f} and {F["p_t"]:.5f}']],
                  size=22, note='SciPy: stats.ttest_ind(offer, control, equal_var=False) gives the same t and p-value.',
                  notes=(f'The Welch two-sample t-test is the standard test for a gap between two means. The test statistic t is the difference in means divided by its standard error, so it counts how many standard errors the lift is from zero. '
                         f'Here t is {n(lift)} divided by {n(se)}, which is {F["t"]:.2f}. Welch means we do not assume the two groups have the same spread. The degrees of freedom, {F["df"]:.1f}, come from the Welch-Satterthwaite formula. '
                         f'The two-sided p-value from the t distribution is {F["p_t"]:.5f}. SciPy computes the same statistic with ttest underscore ind and equal underscore var equal False. We computed this one by hand with NumPy. Why is a t of 3.3 convincing?')))

    # 14 two proportions
    S.append(dict(kind='formula', title='A test of two proportions asks the same question for a yes or no outcome',
                  formulas=[('Test statistic', r'$z = \frac{\hat{p}_1 - \hat{p}_2}{\sqrt{\hat{p}\,(1-\hat{p})\left(\frac{1}{n_1}+\frac{1}{n_2}\right)}}$'), ('Came back within 30 days', rf'$z = \frac{{{F["gap"]:.4f}}}{{{F["se_pool"]:.4f}}} = {F["z"]:.2f}$')],
                  symbols=[['p-hat 1, p-hat 2', 'The share who returned within 30 days in each group.', f'{F["p1"]:.4f} and {F["p2"]:.4f}'], ['p-hat', 'The pooled share: all returners over all customers. It is the rate if H0 is true.', f'{F["p_pool"]:.4f}'],
                           ['z and p-value', 'The test statistic, and the two-sided p-value from the normal distribution.', f'{F["z"]:.2f} and {F["p_z"]:.2f}']],
                  size=20, note='statsmodels proportions_ztest gives the same z. This z uses the pooled share. The interval after it does not.',
                  notes=(f'The second question from the manager was whether more customers came back within 30 days. That outcome is a yes or no, so we compare two proportions. {F["x_o"]} of {n(F["n_o"])} offer customers returned, a share of {F["p1"]:.4f}. '
                         f'{F["x_c"]} of {n(F["n_c"])} control customers returned, {F["p2"]:.4f}. The gap is {F["gap"]:.4f}. Under the null hypothesis both groups share one rate, the pooled share {F["p_pool"]:.4f}, and that gives the standard error. '
                         f'The statistic z is {F["z"]:.2f} and the p-value is {F["p_z"]:.2f}. That is far above 0.05, so we cannot reject the null hypothesis. The statsmodels function proportions underscore ztest computes the same z. Does this mean the offer does not bring customers back?')))

    # 15 two intervals
    S.append(dict(kind='wide', title='The spend interval stays above zero. The return-rate interval crosses zero.',
                  visual=dict(kind='f_panels', panels=[dict(type='interval', labels=['Lift'], est=[lift], low=[lo], high=[hi], ref=(0, 'no difference', GOLD_C), title='Lift in mean spend (UGX)', xlabel='UGX', xlim=(-2500, 10000), xk=True, show_labels=False, legend='upper right', lw=4, ms=10),
                                                       dict(type='interval', labels=['Gap'], est=[F['gap'] * 100], low=[F['ci_gap'][0] * 100], high=[F['ci_gap'][1] * 100], ref=(0, 'no difference', GOLD_C), title='Gap in share who came back (points)', xlabel='Percentage points', xlim=(-3, 8), show_labels=False, legend='upper right', lw=4, ms=10)], ncols=2, wspace=0.25, left=0.05, right=0.97, bottom=0.25, top=0.85),
                  caption=f'Spend: {n(lo)} to {n(hi)}. Return rate: {F["ci_gap"][0] * 100:.1f} to {F["ci_gap"][1] * 100:.1f} points. 95 percent intervals, formula method.',
                  notes=(f'Here are the two results as intervals. On the left, the lift in mean spend, {n(lift)} shillings, with a 95 percent interval from {n(lo)} to {n(hi)}. The whole interval is above zero, the gold dashed line, so the offer raised spend. '
                         f'On the right, the gap in the share of customers who came back, {F["gap"] * 100:.1f} percentage points, with an interval from {F["ci_gap"][0] * 100:.1f} to {F["ci_gap"][1] * 100:.1f}. That interval crosses zero. '
                         'The data are compatible with a small gain, with no change, and with a small loss. The interval is often more useful than the p-value, because it shows the range of plausible effects. Which of the two would you act on?')))

    # 16 decisions
    S.append(dict(kind='table', title='Two questions, two different answers',
                  headers=['Question', 'Estimate and 95% interval', 'p-value', 'Decision'],
                  rows=[['Did the offer raise next-month spend?', f'+{n(lift)} UGX ({n(lo)} to {n(hi)})', f'{F["p_t"]:.5f}', 'Reject H0. Strong evidence of a lift.'],
                        ['Did more customers come back within 30 days?', f'+{F["gap"] * 100:.1f} points ({F["ci_gap"][0] * 100:.1f} to {F["ci_gap"][1] * 100:.1f})', f'{F["p_z"]:.2f}', 'Keep H0. No evidence of a change.']],
                  widths=[3.8, 3.6, 1.6, 3.0], icons=['coin', 'person'], note='Not rejecting H0 is different from proving the offer has no effect on returning. The interval is wide, and more customers could narrow it.',
                  notes=(f'Putting the two together. For spend, the estimate is plus {n(lift)} shillings, the interval is {n(lo)} to {n(hi)}, and the p-value is {F["p_t"]:.5f}. We reject the null hypothesis, because chance alone would rarely give a gap this big. '
                         f'For coming back within 30 days, the estimate is plus {F["gap"] * 100:.1f} points, the interval runs from {F["ci_gap"][0] * 100:.1f} to {F["ci_gap"][1] * 100:.1f}, and the p-value is {F["p_z"]:.2f}. We keep the null hypothesis. '
                         'But keeping it is different from proving there is no effect. The interval is wide, so a small gain is still possible. The honest sentence is that we found no evidence of a change. How would you word that for a manager?')))

    # 17 effect size
    S.append(dict(kind='idea', title='Effect size: the lift is small next to how much customers differ',
                  visual=dict(kind='f_panels', panels=[dict(type='hist', edges=F['h_spend_o'][0], counts=F['h_spend_c'][1], counts2=F['h_spend_o'][1], label1='Control', label2='Offer', vlines=[(F['mean_c'], f'control mean {n(F["mean_c"])}', INK_C, '--'), (F['mean_o'], f'offer mean {n(F["mean_o"])}', RED_C, '--')], title='Spend per customer, by group', xlabel='Next-month spend (UGX)', ylabel='Customers', xk=True, legend='upper right')], ncols=1, left=0.14, right=0.95, bottom=0.17, top=0.9),
                  lead=f"The groups overlap heavily. Cohen's d = {F['d']:.2f}, below the usual 0.2 mark for a small effect.",
                  points=[f'Lift: {n(lift)} UGX, {F["lift_pct"]:.1f} percent of the control mean.', f"Cohen's d is the lift over the pooled standard deviation, {n(F['sp'])}.", 'Statistically clear, practically modest.'],
                  notes=(f'The p-value says chance alone would rarely give a gap this big. It does not say the lift is big. The picture shows the spend of every customer in the two groups, overlapping heavily. The two means are only {n(lift)} shillings apart, while customers differ from each other by about {n(F["sp"])}. '
                         f'The effect size is the size of the gap in useful units. In shillings it is {n(lift)}, which is {F["lift_pct"]:.1f} percent of the control mean. A standard way to express it is Cohen\'s d, the lift divided by the pooled standard deviation. Here d is {F["d"]:.2f}, which is below the conventional 0.2 mark for a small effect. '
                         'A big sample can detect a small effect. Whether it matters is a business question. What would make a gain of eight percent worth having?')))

    # 18 practical
    margin = 0.20   # hypothetical margin: the shop keeps 20 percent of each extra shilling spent
    net = margin * lift - cost
    S.append(dict(kind='compare', title='Statistical significance and practical significance answer different questions',
                  left=dict(head='Statistical significance', points=[f'Is the gap bigger than chance? p = {F["p_t"]:.5f}, below alpha 0.05.']),
                  right=dict(head='Practical significance', points=[f'Hypothetical: cost {n(cost)} UGX per customer, margin {margin * 100:.0f} percent of extra spend.', f'{margin * 100:.0f} percent of {n(lift)} is {n(margin * lift)}, minus {n(cost)}: a loss of {n(-net)}.']),
                  verdict='Report both: is it real, and is it big enough to act on?',
                  notes=(f'These are two different questions. Statistical significance asks whether the gap is bigger than chance, and our p-value of {F["p_t"]:.5f} says yes. Practical significance asks whether the gap is big enough to matter for the decision. '
                         f'Suppose, as made-up numbers, the offer costs {n(cost)} shillings per customer and the shop keeps {margin * 100:.0f} percent of each extra shilling a customer spends. Both are hypothetical. The extra spend is revenue, not profit. '
                         f'So {margin * 100:.0f} percent of the lift of {n(lift)} is {n(margin * lift)}, and after the cost of {n(cost)} that is a loss of {n(-net)} per customer. Even the top of the interval, {n(hi)}, gives only {n(margin * hi)} at that margin. '
                         'The gap is real and still not worth buying at that price. That is a better decision statement than significant or not. What are the real cost and margin in your business?')))

    # 19 false positives
    S.append(dict(kind='idea', title='A false positive (Type I error): a test can raise an alarm when nothing is going on',
                  visual=dict(kind='f_alarm', alarms=F['aa_alarms'], label_a=f'{len(F["aa_alarms"])} of 100 fake tests raise an alarm (red)'),
                  lead='Alpha = 0.05 means about 5 in 100 tests of a true H0 give p below 0.05.',
                  points=['Fake test: split the control group at random into two halves. The true gap is zero.', f'{len(F["aa_alarms"])} of 100 splits had p below 0.05.', 'A false negative (Type II error) is a real effect that a test misses.'],
                  notes=(f'Here is why alpha matters. We took the control group only, {n(F["n_c"])} customers who all got no offer, and split them at random into two halves. The true gap is zero by construction. Then we ran the t-test on the halves. We did that 100 times. '
                         f'{len(F["aa_alarms"])} of the 100 tests gave a p-value below 0.05, the red squares. Each one is a false positive, also called a Type I error: an alarm where nothing is going on. That is exactly what alpha of 0.05 promises, about 5 in 100. '
                         'The opposite mistake, missing a real effect, is a false negative, or Type II error. If you run one test, five percent is acceptable. What happens if you run many?')))

    # 20 multiple comparisons
    ms = list(range(1, 41))
    S.append(dict(kind='idea', title='Multiple comparisons: run many tests and some alarms will be false',
                  visual=dict(kind='f_panels', panels=[dict(type='line', series=[dict(x=ms, y=[round(100 * (1 - 0.95 ** m), 2) for m in ms], color=INK_C, marker='o', ms=4)], hlines=[(5, 'alpha = 5% for one test', GOLD_C, '--')], title='Chance of at least one false alarm (%)', xlabel='Number of tests, each at alpha 0.05', ylabel='Percent', ylim=(0, 100), legend='lower right')], ncols=1, left=0.13, right=0.95, bottom=0.17, top=0.9),
                  lead='With m independent tests at alpha 0.05, the chance of at least one false alarm is 1 minus 0.95 to the power m.',
                  points=[f'5 tests: {F["family"][5] * 100:.0f} percent. 20 tests: {F["family"][20] * 100:.0f} percent.', 'Bonferroni correction: test each at alpha divided by m.', 'Decide the tests before you look.'],
                  notes=(f'One test at alpha 0.05 has a five percent chance of a false alarm. Run more, and the chance of at least one false alarm grows quickly. The formula is one minus 0.95 to the power m, for m independent tests. '
                         f'With 5 tests it is {F["family"][5] * 100:.0f} percent. With 10 it is {F["family"][10] * 100:.0f} percent. With 20 it is {F["family"][20] * 100:.0f} percent, and with 40 it is {F["family"][40] * 100:.0f} percent. This is the multiple comparisons problem. '
                         'Slice the offer test by branch, by age band and by tier, and one slice will look significant by luck. A simple fix is the Bonferroni correction: test each at alpha divided by the number of tests. Better still, decide the tests before you look. How many slices have you looked at in a report?')))

    # 21 optional stopping
    S.append(dict(kind='idea', title='Optional stopping: peeking at a running test and stopping when p is small inflates false alarms',
                  visual=dict(kind='f_panels', panels=[dict(type='bar', labels=['Look once, at the end', f'Peek {F["peek_looks"]} times'], values=[round(F['peek_final'], 1), round(F['peek_any'], 1)], hl=[1], fmt='{:.1f}%', pad=0.6, ylim=(0, 25), hlines=[(5, 'alpha = 5%', GOLD_C, '--')], title='A/A experiments called significant (%)', ylabel='Percent', legend='upper left')], ncols=1, left=0.14, right=0.95, bottom=0.17, top=0.9),
                  lead='Decide the sample size in advance. Stopping when p dips below 0.05 is a form of p-hacking.',
                  points=[f'{n(F["peek_runs"])} A/A experiments, no real difference.', f'One look at the end: {F["peek_final"]:.1f} percent significant.', f'Stop at the first of {F["peek_looks"]} looks with p below 0.05: {F["peek_any"]:.1f} percent.'],
                  notes=(f'The last trap is peeking. Imagine you run a test and check the p-value every day, and stop the first time it dips below 0.05. That is optional stopping, a form of p-hacking. We simulated {n(F["peek_runs"])} experiments with no real difference. '
                         f'If you look once, at the planned end, {F["peek_final"]:.1f} percent come out significant, close to the five percent promised. If you look {F["peek_looks"]} times and stop at the first small p-value, {F["peek_any"]:.1f} percent come out significant. '
                         'The p-value was built for a single planned look. So fix the sample size and the tests in advance, write them down, and look once. Have you ever stopped a test early because it looked good?')))

    # 21b sample size
    sp_ = F['sp']
    rows_n = [[n(m_) + (' (our offer group)' if m_ == F['n_o'] else ''), f'{1.96 * sp_ * (2 / m_) ** 0.5:,.0f}'] for m_ in (250, 500, 1000, F['n_o'], 2500)]
    n_need = int(-(-2 * ((1.96 + 0.8416) * sp_ / lift_plan) ** 2 // 1))
    S.append(dict(kind='table', title=f'How many customers does the test need? About {n(n_need)} per group to catch a lift of {n(lift_plan)} UGX',
                  headers=['Customers per group', 'Margin of error of the lift (95% interval, plus or minus UGX)'],
                  rows=rows_n, widths=[4.2, 7.8], icons=['people'] * 5,
                  note=f'Margin = 1.96 x s x square root of (2 / n), with s = {n(sp_)} UGX. Power: with {n(n_need)} per group, a test at alpha 0.05 catches a true lift of {n(lift_plan)} about 80 times in 100 (power 80 percent, a common choice).',
                  notes=(f'A manager will ask how many customers the next test needs. The margin of error of the lift shrinks with the square root of the group size. With 250 customers per group the margin is about {rows_n[0][1]} shillings. With {n(F["n_o"])} per group, like our test, it is about {rows_n[3][1]}. With 2,500 it is about {rows_n[4][1]}. '
                         f'Another way to ask is about power: the chance that a test catches a real lift of a given size. Power is one minus the Type II error rate, and 80 percent is a common target. To catch a true lift of {n(lift_plan)} shillings with 80 percent power at alpha 0.05, you need about {n(n_need)} customers per group. '
                         'Smaller lifts need many more, because halving the lift needs four times the customers. Decide the number before the test starts. What lift would be worth detecting in your business?')))

    # 22 use at work
    S.append(dict(kind='table', title='Where you will use this at work: check that a gap is real before you act on it',
                  headers=['Your job', 'The comparison', 'What today lets you do'],
                  rows=[['Marketing analyst at a telecom, using Python', 'A promotion sent to half the subscribers.', 'Report the lift with an interval and a p-value, and the cost per customer.'],
                        ['Credit risk analyst at a bank, using Python', 'Default rate in two branches or two scorecards.', 'Run a two-proportion test and report the interval together with the two rates.'],
                        ['Programme officer at an NGO', 'Test scores in a pilot school and a comparison school.', 'Use a permutation test when the groups are small or skewed.'],
                        ['Operations manager at a retailer', 'Return rates before and after a change in supplier.', 'Fix the test before the data arrive, and avoid peeking.']],
                  widths=[3.6, 3.8, 4.6], icons=['phone', 'coin', 'people', 'shop'],
                  notes=('Where will you use this on Monday? A marketing analyst at a telecom who uses Python can report the lift of a promotion with an interval and a p-value, and set it against the cost per customer. '
                         'A credit risk analyst at a bank can compare default rates in two branches with a test of two proportions, and report the interval and not only the two rates. '
                         'A programme officer at an NGO comparing a pilot school with a comparison school can use a permutation test when the groups are small or skewed. '
                         'And an operations manager can fix the test before the data arrive and avoid peeking. Which of these is closest to your job?')))

    # 23 and 24 recipes
    S.append(dict(kind='code', title='Read recipe 1 before the lab: the lift, its standard error, t and the interval by hand', code=SN_A, output=la,
                  reads=['Split the spend into offer and control arrays.', 'v_o and v_c are the squared standard errors. Their sum under a square root is the standard error of the lift.', f't is the lift over its standard error: {F["t"]:.2f}.',
                         'The interval is the lift plus or minus 1.96 standard errors. SciPy ttest_ind with equal_var=False gives the same t.'],
                  notes=(f'Before the lab, read the first recipe. It splits the spend into two arrays, offer and control. The lines with v underscore o and v underscore c compute the two squared standard errors, and the square root of their sum is the standard error of the lift. '
                         f'The first print shows the lift, {n(lift)}, the standard error, {n(se)}, and the t statistic, {F["t"]:.2f}. The second print shows the interval, {n(lo)} to {n(hi)}. '
                         'In the lab you will compare these numbers with the SciPy function ttest underscore ind, using equal underscore var equal False, and they should agree. Which line would you change for the control group alone?')))
    S.append(dict(kind='code', title='Read recipe 2: the bootstrap interval, with a fixed seed', code=SN_B, output=[outB],
                  reads=['default_rng(42) fixes the seed, so everyone gets the same random draws.', 'choice with a size draws with replacement. Each pass resamples both groups and takes the lift.',
                         'percentile cuts off the lowest and highest 2.5 percent.', f'The print is the 95 percent bootstrap interval: {n(F["boot_ci"][0])} to {n(F["boot_ci"][1])}.'],
                  notes=(f'The second recipe is the bootstrap. The default underscore rng call with seed 42 makes the random draws repeat for everyone, so your numbers can match mine. Inside the list, rng dot choice draws a resample of the offer group with replacement, at the original size, and another of the control group. '
                         f'We take the difference of their means, the lift, and repeat 5,000 times. The percentile call cuts off the lowest and highest 2.5 percent. The print shows the interval, {n(F["boot_ci"][0])} to {n(F["boot_ci"][1])}. '
                         'It takes a second or two to run. Why does a fixed seed matter when you share a notebook?')))
    S.append(dict(kind='code', title='Read recipe 3: the permutation test shuffles the offer labels', code=SN_C, output=[outC],
                  reads=['values holds every customer spend. is_offer is True for the offer group.', 'rng.permutation shuffles the labels, keeping the group sizes.', 'Each shuffle gives one gap in mean spend. hits counts gaps at least as big as the real lift, ignoring the sign.',
                         f'{F["perm_hits"]} hits in 5,000 gives p = {F["p_perm"]}.'],
                  notes=(f'The third recipe is the permutation test. The array values holds every customer spend, and is underscore offer marks which customers got the offer. Inside the loop, rng dot permutation shuffles those labels at random, which keeps the group sizes. '
                         f'We compute the gap in mean spend for the shuffled groups, and keep it. After 5,000 shuffles, we count how many gaps are at least as big as the real lift. We use the absolute value, so a big gap in either direction counts. '
                         f'The print shows {F["perm_hits"]} hits, and a p-value of {F["p_perm"]}. Where would you shuffle labels in your own data?')))

    # 25 divider
    S.append(dict(kind='divider', title='Part 2: the Python lab', lead='Close the slides. Open the notebook.', section='Lab',
                  notes=('That is the end of the ideas. Everything you need is on the slides you have just seen, and the notebook repeats each step. '
                         'Open Google Colab and open the notebook for Session 12. Run the first cells to load the data. In every step, predict first, then run, then read, then change one thing. '
                         'You compute each number by hand with NumPy, and then check it against SciPy or statsmodels. The checks turn from NOT YET to OK when your answer is right.')))

    # 26 lab map
    S.append(dict(kind='steps', title='The lab has seven steps, and you keep a decision note about the offer',
                  steps=[dict(head='1 Split', text='Offer and control', icon='folder'), dict(head='2 Lift and SE', text='Formula and CI', icon='calculator'), dict(head='3 Bootstrap', text='Resample 5,000', icon='gear'),
                         dict(head='4 Permute', text='Shuffle, p-value', icon='question'), dict(head='5 Tests', text='t-test, two proportions', icon='check'), dict(head='6 Decide', text='Effect, 3 sentences', icon='notebook'), dict(head='7 False alarms', text='Fake tests, Bonferroni', icon='shield')], highlight=None,
                  caption='Twenty-one automatic checks in 45 minutes. Predict, run, read, change.',
                  notes=('Here is the map of the lab, in seven steps. Step one, split the spend into offer and control. Step two, compute the lift, its standard error and the formula interval. '
                         'Step three, bootstrap the lift with a fixed seed. Step four, run the permutation test and get the p-value. Step five, run the Welch t-test and the test of two proportions with SciPy and statsmodels, and compare them with your by-hand numbers. '
                         'Step six, compute the effect size and write a decision note of three sentences. Step seven, run 100 fake tests and see about 5 false positives (false alarms), then work out the Bonferroni cut-off. Please write your prediction before every step.')))

    # 27 check numbers
    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Customers in offer and in control', f'{n(F["n_o"])} and {n(F["n_c"])}'], ['Mean spend in offer and in control (UGX)', f'{n(F["mean_o"])} and {n(F["mean_c"])}'], ['The lift (UGX)', n(lift)],
                        ['Standard error of the lift, and the 95% interval', f'{n(se)}, and {n(lo)} to {n(hi)}'], ['Bootstrap interval (seed 42, 5,000 resamples)', f'{n(F["boot_ci"][0])} to {n(F["boot_ci"][1])}'],
                        ['Permutation test (seed 42): hits and p-value', f'{F["perm_hits"]} of 5,000, p = {F["p_perm"]}'], ["Welch t statistic and p-value", f'{F["t"]:.2f} and {F["p_t"]:.5f}'], ['Two proportions: z and p-value', f'{F["z"]:.2f} and {F["p_z"]:.2f}']],
                  widths=[7.0, 5.0], icons=['people', 'coin', 'chart', 'calculator', 'gear', 'question', 'check', 'person'], note='Bootstrap and permutation numbers repeat only with the same seed and the same order of calls.',
                  notes=('Use this table as your own self-check. Nobody marks it. If your numbers match, carry on. If one does not, stop and call me, because later steps use the earlier ones. '
                         'The bootstrap and permutation numbers match only if you use the same seed, 42, and the same order of random calls. If your numbers differ slightly, check the seed first. '
                         'Do not change a number to make it match. What would a p-value of exactly zero from a permutation test mean?')))

    # 28 errors
    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[['Bootstrap interval differs from the slide', 'A different seed or call order.', 'Make rng once, before the loop.'],
                        ['p-value is 0.0 from the permutation test', 'No shuffle was this extreme.', 'Report p below 1 in 5,000.'],
                        ['NameError: name \'stats\' is not defined', 'The import cell was not run.', 'Run the first code cell: from scipy import stats.'],
                        ['t is 0.002 instead of 3.31', 'The lift was divided by the variance.', 'Take the square root: np.sqrt(v_o + v_c).'],
                        ['p-value is half of the expected value', 'A one-sided test was run.', 'Use the two-sided p-value: multiply the tail area by 2.']],
                  widths=[3.9, 4.1, 4.0], icons=['cross', 'cross', 'cross', 'cross', 'cross'],
                  notes=('Five problems you may meet. If your bootstrap interval differs from the slide, you used a different seed or made the draws in a different order, so create the random generator once, before the loop. '
                         'If the permutation p-value is zero, no shuffle was as extreme in 5,000 tries, so report that it is below one in 5,000 and never write exactly zero. A name error for stats means the import cell was not run. '
                         'A t statistic close to zero, like 0.002, usually means you divided by the variance instead of the standard error, so take the square root. '
                         'And a p-value that is half what you expected means a one-sided test. Read the message first. It usually tells you the answer.')))

    # 29 exit
    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[['A test gives p = 0.03 with alpha = 0.05. What do you conclude, and what do you still need to report?', 'Reject H0: if H0 were true, a gap this big would be rare. Also report the effect size and the confidence interval.'],
                        ['You run 20 tests at alpha = 0.05 on a dataset with no real effects. About how many false positives do you expect?', 'About one, because 20 times 0.05 is 1. The chance of at least one is about 64 percent.'],
                        ['A 95 percent confidence interval for the lift is -200 to 5,000 UGX. Is the lift significant at 0.05?', 'No. The interval includes zero, so the data are compatible with no difference.']],
                  widths=[5.8, 6.2], icons=['calculator', 'flag', 'chart'],
                  notes=('Last, the exit check. Write your answers before you look at mine. One, a test gives a p-value of 0.03 with alpha 0.05: what do you conclude, and what else do you report? '
                         'Two, you run 20 tests at alpha 0.05 on data with no real effects: about how many false positives do you expect? '
                         'Three, a 95 percent interval for a lift runs from minus 200 to 5,000 shillings: is the lift significant? The short answers are on the slide. If you got all three, you are ready for Session 13.')))

    sess['facilitator'] = dict(
        prep=['Open the deck and the Colab notebook before anyone arrives. Share the data.zip step.',
              'Run the solution notebook once in Colab. The NumPy numbers in this deck were computed without SciPy or statsmodels; the notebook compares them with stats.ttest_ind(equal_var=False) and proportions_ztest. Confirm they agree before class.',
              'Fix the seed 42 rule on the board: bootstrap and permutation numbers repeat only with the same seed and call order.',
              'Concepts run with laptops closed. Ask learners to open Colab only after the Part 2 divider.',
              'The 100 A/A tests, the 30 intervals and the peeking simulation are seed-fixed illustrations. State that the cost of 3,000 UGX per customer is hypothetical.'],
        misconceptions=[('A p-value of 0.03 means a 3 percent chance that H0 is true', 'It is the chance of data this extreme if H0 is true. It is not the probability of H0.'),
                        ('A 95 percent interval means there is a 95 percent chance the true value is inside this interval', 'It describes the method: about 95 in 100 intervals built this way catch the true value.'),
                        ('Significant means important', f'Cohen\'s d is {F["d"]:.2f} here. A small effect can be significant in a large sample.'),
                        ('Not significant proves there is no effect', f'The return-rate interval is {F["ci_gap"][0] * 100:.1f} to {F["ci_gap"][1] * 100:.1f} points. A small gain is still possible.'),
                        ('Checking the test every day is harmless', f'Peeking at {F["peek_looks"]} looks gives about {F["peek_any"]:.0f} percent false positives instead of 5.')],
        probes=[('Why does the standard error fall when n grows?', 'The mean averages out more of the random variation. The formula divides by the square root of n.'),
                ('What does the bootstrap resample?', 'The observed data, with replacement, to the original sample size.'),
                ('What is shuffled in a permutation test?', 'The group labels, under the null hypothesis that labels carry no information.'),
                ('What is the null hypothesis in the offer test?', 'The offer does not change average spend.'),
                ('Why Welch?', 'It does not assume the two groups have equal variance.'),
                ('What is Bonferroni?', 'Test each of m tests at alpha divided by m.')],
        lab_steps=[('Step 1: split', f'{n(F["n_o"])} offer, {n(F["n_c"])} control.'), ('Step 2: lift and SE', f'Lift {n(lift)}, SE {n(se)}, interval {n(lo)} to {n(hi)}. Check ddof=1.'),
                   ('Step 3: bootstrap', f'Seed 42: {n(F["boot_ci"][0])} to {n(F["boot_ci"][1])}.'), ('Step 4: permutation', f'Seed 42: {F["perm_hits"]} of 5,000, p = {F["p_perm"]}.'),
                   ('Step 5: tests', f't = {F["t"]:.2f}, p = {F["p_t"]:.5f}. z = {F["z"]:.2f}, p = {F["p_z"]:.2f}. Compare SciPy with NumPy.'), ('Step 6: decide', f'Effect size d = {F["d"]:.2f}. The note needs the lift, the interval, the p-value and a limit.')],
        rescue=['If the concepts run over, shorten the multiple comparisons and optional stopping slides to one minute each; the lab covers the core.', 'If only 30 minutes of lab remain, do steps 1, 2, 4 and 6 and set steps 3 and 5 as homework.',
                'If a learner has no Colab, SciPy and statsmodels are installed in most Jupyter environments.', 'If a learner has no laptop, pair them with a neighbour: one types, one predicts aloud.'],
        after=['Share the deck and the solution notebook again for absent learners.', 'Ask each learner to save the decision note and bring one regression question to Session 13.', 'Note any question you could not answer and open the next session with it.'],
        lab_answer_key=[['Step 2 PREDICT: will the interval for the lift include zero?', f'No. It runs from {n(lo)} to {n(hi)}.'],
                        ['Step 3 READ: how does the bootstrap SE compare with the formula SE?', f'{n(F["boot_se"])} against {n(se)}. They are close.'],
                        ['Step 4 READ: what does p = 0.0014 mean?', f'Only {F["perm_hits"]} of 5,000 shuffles gave a gap as big as the lift. Chance alone rarely does that.'],
                        ['Step 5 READ: do SciPy and NumPy agree?', f'Yes: t = {F["t"]:.2f}, p = {F["p_t"]:.5f}.'],
                        ['Step 5 CHANGE: test the return rate. Is the offer effective for coming back?', f'No evidence: z = {F["z"]:.2f}, p = {F["p_z"]:.2f}, interval {F["ci_gap"][0] * 100:.1f} to {F["ci_gap"][1] * 100:.1f} points.'],
                        ['Step 6 READ: is the effect large?', f"Below the 0.2 mark for a small effect: Cohen's d = {F['d']:.2f}, {F['lift_pct']:.1f} percent of the control mean. The decision depends on the cost and the margin."],
                        ['Step 7 CHANGE: peek after every batch of 100 customers.', 'The false alarm rate climbs well above 5 percent, as on the optional stopping slide.']])
    return sess
