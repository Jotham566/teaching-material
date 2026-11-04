"""Session 15: Classification, yes or no questions (binary classification, logistic regression, one-hot encoding, decision tree, predicted probability, decision threshold and its cost). Python lab.

Every number on a slide, in a note or in the notebook checks is computed in facts() from the real Nile Microfinance loans file (loans.csv) through content/h_loans.py, which is built on
content/loans_canon.py (the one recipe shared by Sessions 14 to 17, 20, 23 and 24): 8,000 loans, stratified 6,000 / 2,000 split, 27 columns, a scaled logistic regression, the CART tree port.
Every count, rate and cost is derived from those predictions. They are NumPy replica numbers: re-run on real scikit-learn in Colab before the course starts. Costs in UGX are illustrative teaching numbers.
The decision threshold is chosen on the TRAINING loans (5-fold cross-validation, or the cost rule 0.0909). The test loans report the result once.
"""
from functools import lru_cache

import numpy as np
import pandas as pd

import h_loans as H
from h_loans import n, COST_MISS, COST_ALARM


def pct(x, d=1):
    return f'{x * 100:.{d}f}'


def tree_dict(node, X, y, cols, idx=None):
    """Turn a replica tree into the nested dict the figure draws: question, loans reaching the node, their default rate."""
    idx = np.arange(len(X)) if idx is None else idx
    rate = float(y[idx].mean())
    if node[0] == 'leaf':
        return dict(leaf=True, n=int(len(idx)), rate=rate)
    _, f, thr, left, right = node
    go = X[idx, f].astype(np.float32).astype(float) <= thr
    return dict(q=f'{cols[f]} <= {thr:,.0f}' if abs(thr) >= 1000 else f'{cols[f]} <= {thr:.2f}', n=int(len(idx)), rate=rate, feature=cols[f], thr=float(thr), yes=tree_dict(left, X, y, cols, idx[go]), no=tree_dict(right, X, y, cols, idx[~go]))


def leaves(d):
    return [d] if d.get('leaf') else leaves(d['yes']) + leaves(d['no'])


@lru_cache(maxsize=None)
def facts():
    F = dict(H.facts())
    L, X, y = F['loans'], F['X'], F['y']
    cols = F['cols']
    # a small real excerpt: two defaulted and two repaid loans, first in the file
    d = L[L.default == 1].head(2)
    r = L[L.default == 0].head(2)
    ex = pd.concat([r.head(1), d.head(1), r.tail(1), d.tail(1)])
    F['ex_target'] = [[str(v.loan_id), str(v.occupation), n(v.loan_amount_ugx), f'{v.instalment_to_income:.2f}', str(int(v.default))] for v in ex.itertuples()]
    # instalment-to-income ratio fifths and occupation rates
    q = pd.qcut(L.instalment_to_income, 5, retbins=True)
    F['burden_edges'] = [float(e) for e in q[1]]
    g = L.groupby(q[0], observed=True).default.mean()
    F['burden_rates'] = [float(v) for v in g.values]
    F['occ'] = L.groupby('occupation').default.agg(['mean', 'size']).sort_values('mean', ascending=False)
    # sigmoid example loan: the first test loan with a probability from 0.20 to 0.30
    p = F['p_lr']
    k = int(np.where((p >= 0.20) & (p < 0.30))[0][0])
    row = F['Zte'][k]                      # the loan's values after StandardScaler (z-scores)
    F['ex_raw'] = F['Xte'][k]
    w = F['lr_w']
    terms = {c: float(w[i] * row[i]) for i, c in enumerate(cols)}
    z = float(F['lr_b'] + (w * row).sum())
    F['ex_k'], F['ex_row'], F['ex_terms'], F['ex_z'] = k, row, terms, z
    F['ex_p'] = float(1 / (1 + np.exp(-z)))
    assert abs(F['ex_p'] - p[k]) < 1e-9
    F['ex_actual'] = int(F['yte'][k])
    F['ex_loan'] = L.iloc[F['te'][k]]
    # odds table
    F['odds'] = [(pp, pp / (1 - pp), float(np.log(pp / (1 - pp)))) for pp in (0.05, 0.10, 0.20, 0.50, 0.80)]
    # coefficient table: coefficients are per 1 standard deviation of each variable (StandardScaler inside the pipeline)
    F['sd'] = dict(zip(cols, F['model'].scale_))
    F['coef_rows'] = [(c, float(F['coef'][c]), float(np.exp(F['coef'][c]))) for c in ('instalment_to_income', 'previous_late_payments', 'occupation_Boda rider', 'occupation_Teacher', 'savings_balance_ugx', 'group_loan')]
    # trees
    F['tree2_d'] = tree_dict(F['tree2'], F['Xtr'], F['ytr'], cols)
    F['tree3_d'] = tree_dict(F['tree3'], F['Xtr'], F['ytr'], cols)
    t3 = F['tree3_d']
    F['root_q'], F['root_feature'], F['root_thr'] = t3['q'], t3['feature'], t3['thr']
    pr = F['train_pos'] / F['n_train']
    F['gini_root'] = 1 - pr ** 2 - (1 - pr) ** 2
    yl, yr = t3['yes'], t3['no']
    F['gini_l'] = 1 - yl['rate'] ** 2 - (1 - yl['rate']) ** 2
    F['gini_r'] = 1 - yr['rate'] ** 2 - (1 - yr['rate']) ** 2
    F['gini_split'] = (yl['n'] * F['gini_l'] + yr['n'] * F['gini_r']) / t3['n']
    F['t3_leaves'] = sorted(leaves(t3), key=lambda l: l['rate'])
    F['t3_rules'] = [lf['rate'] for lf in F['t3_leaves']]
    # histogram of predicted probabilities (share of each group per bin of 0.05, last bin holds 0.60 and above)
    edges = [round(0.05 * i, 2) for i in range(0, 14)]
    clip = np.minimum(p, edges[-1] - 1e-9)
    F['hist_edges'] = edges
    F['hist_repaid'] = [float(v) for v in np.histogram(clip[F['yte'] == 0], bins=edges)[0] / F['test_neg']]
    F['hist_default'] = [float(v) for v in np.histogram(clip[F['yte'] == 1], bins=edges)[0] / F['test_pos']]
    F['share_above_20_default'] = float((p[F['yte'] == 1] >= 0.2).mean())
    F['share_above_20_repaid'] = float((p[F['yte'] == 0] >= 0.2).mean())
    F['rule_thr'] = COST_ALARM / (COST_ALARM + COST_MISS)
    F['cost_rows'] = F['cost_test']
    F['avg_default_loan'] = float(L[L.default == 1].loan_amount_ugx.mean())
    return F


def build():
    F = facts()
    L = F['loans']
    T = F['thr_rows']
    p = F['p_lr']
    yte = F['yte']
    cv_t = F['cv_t']
    cost_m = lambda v: f'{v / 1e6:.0f}'
    cost_m1 = lambda v: f'{v / 1e6:.1f}'
    t3 = F['tree3_d']
    t2 = F['tree2_d']
    ex = F['ex_loan']
    bet = F['burden_rates']
    edges = F['burden_edges']
    occ = F['occ']
    lr_acc_05 = T[0.5]['accuracy']
    # literals used in prose must match the data
    assert F['rows'] == 8000 and F['X_shape'] == (8000, 27) and F['n_train'] == 6000 and F['n_test'] == 2000 and F['test_pos'] == 251
    base = 1 - F['test_rate']
    assert occ.index[0] == 'Boda rider' and occ.index[-1] == 'Teacher'
    assert F['root_feature'] == 'instalment_to_income'
    top_occ, low_occ = occ.iloc[0], occ.iloc[-1]
    cof = {c: (b, o) for c, b, o in F['coef_rows']}
    b0 = F['lr_b']
    terms = F['ex_terms']
    t_burden, t_late, t_boda = terms['instalment_to_income'], terms['previous_late_payments'], terms['occupation_' + ex.occupation]
    t_rest = F['ex_z'] - b0 - t_burden - t_late - t_boda
    assert abs(b0 + t_burden + t_late + t_boda + t_rest - F['ex_z']) < 1e-9

    sess = dict(
        num=15, block='Module D: Machine learning', short_title='Classification',
        title='Classification: predicting a yes or no answer with logistic regression and a decision tree',
        question='How do we predict a category, and what does the model\'s confidence mean?',
        outcomes=['Say what binary classification is, and fit a logistic regression and a decision tree on the Nile Microfinance loans',
                  'Read a predicted probability, and turn text variables into numbers with one-hot encoding',
                  'Choose a decision threshold from the cost of a missed default and the cost of a false alarm'],
        outcome_icons=['gear', 'chart', 'coin'],
        outcome_note=('Here is what you can do by the end of today. You can say what binary classification is, and you can fit two models on the Nile Microfinance loans: a logistic regression and a decision tree. '
                      'You can read the predicted probability each model gives, and you can turn text variables such as occupation into numbers a model can use. '
                      'And you can choose a decision threshold from the cost of a missed default and the cost of a false alarm. That last part is where data science meets a manager\'s budget.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: picture, plain words, one example by hand'), (10, 'Break'), (45, 'Lab: predict, run, read, change'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: concepts first, then a Python lab in Colab',
        plan_caption='Ideas with pictures first. Then you open the notebook. Then the checks and what you keep.',
        plan_note=('We have two hours. The first ten minutes bring back Session 14 and set the question for today. Then forty-five minutes of concepts, with no laptops open, so you can watch the pictures and follow the worked examples. '
                   'After a ten minute break you open the Colab notebook for a forty-five minute lab. You will predict each answer, run the cell, read the output, and then change one thing. '
                   'The last ten minutes are an exit check and what you keep. The lab is where the learning sticks, so please protect that time.'),
        recall_from='Session 14',
        recall=[('In the loan file, which variables are the features and which is the target?', 'The features are the inputs, such as income, loan amount and age. The target is default: 1 means the loan defaulted, 0 means it was repaid.'),
                ('Why do we hide a test set from the model?', 'To score the model on loans it has never seen, like a test with new questions. A score on the training set flatters the model.'),
                ('What is a baseline model, and why do we compare against one?', f'The simplest possible model. Here it says "no default" for every loan and is right {pct(1 - F["test_rate"], 2)} percent of the time (1,749 of the 2,000 test loans). Any model we build must beat it.')],
        words=[('Binary classification (positive class, negative class)', f'Predicting one of two categories. The positive class is the outcome we look for: default = 1. The negative class is the other: repaid = 0.'),
               ('Logistic regression (sigmoid, log-odds, regularisation)', 'A model that bends a score from the features into a probability between 0 and 1 with the sigmoid. scikit-learn penalises large coefficients (regularisation, C = 1.0).'),
               ('Decision tree (root node, leaf node)', 'A model made of yes or no questions. Each path ends in a leaf node, and the leaf gives the predicted probability.'),
               ('Decision threshold (cut-off)', 'The probability at or above which we predict the positive class. The default of 0.5 is rarely right for a business.'),
               ('One-hot encoding', 'Turning a text variable into one 0 or 1 indicator column per category, so a model can use it.')],
        word_icons=['flag', 'chart', 'pin', 'switch', 'grid'],
        words_note=('Five words for today. Binary classification means predicting one of two categories, and the positive class is the outcome we look for, which here is a default. '
                    'Logistic regression is a model that turns a score into a probability using the sigmoid function. A decision tree is a set of yes or no questions that ends in a leaf with a probability. '
                    'The decision threshold is the probability at which we say yes. And one-hot encoding turns a text variable into columns of zero and one. We use every one of them before the end of the session.'),
        keep=f'Your notebook, a file loan_risk_scores.csv with a probability and a flag for each of the {n(F["n_test"])} test loans, and a three-line threshold note with its cost in UGX.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab files', value='Notebook and CSV'), dict(label='The decision', value='A priced threshold'), dict(label='Next session', value='Judging a model')]),
        keep_title='Save your notebook and your threshold note',
        next='Session 16: Judging a model. We measure precision, recall and AUC, catch a column that leaks the answer, and test with cross-validation.', next_label='Next session',
        keep_note=('Before you go, save your notebook and the file loan risk scores. The file is your keepsake: one probability and one flag for each of two thousand test loans, with your threshold note beside it. '
                   'If you can show it to a colleague in credit and they can read the threshold and its cost in shillings, it is good. Next session we ask a harder question: how do we tell a model that works from one that only looks good? '
                   'If anything was unclear today, write the question down and bring it.'),
        cover_note=('Welcome back. Last session you built a first model for loan default and compared it with the laziest guesser we can build. Today the question is sharper. '
                    'How confident is the model, and what do we do with that confidence? You will fit two kinds of model on the Nile Microfinance loans, learn to read what they say, and choose a decision threshold using the cost of a mistake. '
                    'That last step is the one a manager cares about.'),
        use_at_work='Score each loan, customer or transaction with a probability, then set the decision threshold from what each mistake costs.',
        slides=[])
    S = sess['slides']

    # ------------------------------------------------------------------ 1 answers
    S.append(dict(kind='table', title='Answers to the three questions from Session 14', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in sess['recall']], widths=[4.6, 7.4], icons=['key', 'lock', 'flag'],
                  notes=(f'Here are the answers to the three warm-up questions. The features are the columns the model looks at, and the target is the column we want to predict, which is default. '
                         f'We hide a test set so the model is scored on loans it has never seen, like a test with new questions. And the baseline model says no default for every loan. On our 2,000 test loans, which hold {F["test_pos"]} defaults, that is right {pct(1 - F["test_rate"], 2)} percent of the time, so any model we build has to beat it. '
                         'Which of the three did you find hardest?')))

    # ------------------------------------------------------------------ 2 binary classification
    S.append(dict(kind='idea', title='Binary classification predicts one of two categories for each loan',
                  visual=dict(kind='dsh_target', headers=['loan_id', 'occupation', 'loan_amount_ugx', 'instalment_to_income', 'default'], rows=F['ex_target']),
                  lead='Classification predicts a category. Binary classification has exactly two.',
                  points=['Positive class: the outcome we look for. Here default = 1.', 'Negative class: the other outcome. Here repaid, default = 0.', 'In Excel: a Yes or No column to fill in for new loans.'],
                  notes=('A few real rows from the Nile Microfinance loans file. Every column on the left is a feature, an input we know when the loan is approved. The gold column is the target, also called the label. '
                         'Predicting a category is called classification, and when there are exactly two categories it is binary classification. One category is the positive class, the outcome we look for, which here is a default and is coded one. '
                         'The other is the negative class, a repaid loan, coded zero. Positive does not mean good. It means the one we are hunting. In Excel this is a Yes or No column you wish you could fill in. Which class is the positive class in your own work?')))

    # ------------------------------------------------------------------ 3 vocabulary
    S.append(dict(kind='table', title='The spreadsheet word and the machine learning word for each idea',
                  headers=['In a spreadsheet', 'In machine learning', 'Plain meaning'],
                  rows=[['A Yes or No column', 'Target (label)', 'The answer we want to predict for each record.'], ['A percentage beside each row', 'Predicted probability', 'The model\'s chance, from 0 to 1, that the record is in the positive class.'],
                        ['=IF(score>=0.2,"Yes","No")', 'Decision threshold', 'The probability at or above which we say yes.'], ['A helper column per category', 'One-hot encoding', 'One 0 or 1 indicator column for each category.'],
                        ['A trendline that returns a probability', 'Logistic regression', 'A linear score bent into a probability.'], ['A nested IF written by the computer', 'Decision tree', 'Yes or no questions that end in a verdict.']],
                  widths=[3.3, 3.0, 5.7], icons=['flag', 'chart', 'switch', 'grid', 'gear', 'pin'],
                  notes=('You already know every idea of today from Excel, so here is the translation. A Yes or No column is the target, or label. A percentage beside each row is the predicted probability. '
                         'The number in an IF formula that decides yes or no is the decision threshold, also called the classification threshold or cut-off. A helper column for each category is one-hot encoding. A trendline that returns a probability is logistic regression, and a nested IF written by the computer is a decision tree. '
                         'When you read documentation or a job advert, this table is your dictionary. Which of these words was new to you?')))

    # ------------------------------------------------------------------ 4 imbalance stat
    S.append(dict(kind='stat', title=f'Only {pct(F["default_rate"], 1)} percent of loans default, so the positive class is rare', big=f'{pct(F["default_rate"], 0)}%',
                  text=f'{n(round(F["default_rate"] * F["rows"]))} of the {n(F["rows"])} loans defaulted. About one loan in eight is in the positive class.', waffle_label=f'About {round(F["default_rate"] * 100)} of every 100 loans defaulted',
                  notes=(f'Before any model, look at how common the positive class is. In the Nile Microfinance file, the same 8,000 loans as in Session 14, {n(round(F["default_rate"] * F["rows"]))} loans defaulted. '
                         f'That is {pct(F["default_rate"], 1)} percent, about one loan in eight, so roughly thirteen in every hundred squares on the picture. When one class is much rarer than the other, we call it class imbalance. '
                         'It is the reason a model can look good and still be useless, and it shapes every choice today and next session. Why is a rare positive class harder to predict?')))

    # ------------------------------------------------------------------ 5 default by burden
    S.append(dict(kind='wide', title='Default rate climbs with the instalment-to-income ratio',
                  visual=dict(kind='bars', unit='%', max_value=40, items=[dict(label=f'{lab}: {rng}', value=round(v * 100, 1), hl=(i == 4)) for i, (lab, rng, v) in enumerate(zip(
                      ['Lightest', 'Second', 'Third', 'Fourth', 'Heaviest'], [f'up to {edges[1]:.2f}', f'{edges[1]:.2f} to {edges[2]:.2f}', f'{edges[2]:.2f} to {edges[3]:.2f}', f'{edges[3]:.2f} to {edges[4]:.2f}', f'above {edges[4]:.2f}'], bet))]),
                  caption='Five equal groups of 1,600 loans. The 1.15 in the ratio is assumed.',
                  notes=(f'In Session 14 we built a feature called instalment to income, the instalment-to-income ratio: the monthly instalment divided by the monthly income, where the instalment is the loan plus a fifteen percent charge, spread over the term. That fifteen percent is an illustrative assumption. '
                         f'A ratio of one means the instalment equals a whole month of income. Here the loans are cut into five equal groups by the ratio. In the lightest fifth, {pct(bet[0], 1)} percent defaulted. '
                         f'In the heaviest fifth, {pct(bet[4], 1)} percent defaulted, about {bet[4] / bet[0]:.0f} times as many. A classification model has to find a pattern like this one. Which loan in your portfolio would you call heavy?')))

    # ------------------------------------------------------------------ 6 occupation bars
    S.append(dict(kind='wide', title='Occupation is text, yet it carries a signal a model can use',
                  visual=dict(kind='bars', unit='%', max_value=24, items=[dict(label=f'{k}', value=round(r['mean'] * 100, 1), hl=(i == 0)) for i, (k, r) in enumerate(occ.iterrows())]),
                  caption='Share of loans that defaulted in each occupation. A model needs these words as numbers.',
                  notes=(f'Now a text variable. Occupation has seven values. {occ.index[0]} borrowers defaulted most, at {pct(top_occ["mean"], 1)} percent, about one loan in five. '
                         f'{occ.index[-1]}s defaulted least, at {pct(low_occ["mean"], 1)} percent. The five jobs in between sit from {pct(occ["mean"].iloc[-2], 1)} to {pct(occ["mean"].iloc[1], 1)} percent. '
                         'So occupation carries some information. But a model works on numbers, and a word like Teacher is not a number. In a few slides you will see how one-hot encoding fixes that. Would you expect occupation to matter in your own lending data?')))

    # ------------------------------------------------------------------ 7 sigmoid
    S.append(dict(kind='idea', title='A straight line can leave the range 0 to 1, so logistic regression bends it with the sigmoid',
                  visual=dict(kind='dsh_sigmoid'),
                  lead='A probability must stay between 0 and 1. A straight line does not.',
                  points=['The sigmoid (logistic) function squeezes any score into 0 to 1.', 'Logistic regression: a linear score, then the sigmoid.', 'Despite the word regression, it is a classification model.'],
                  notes=('Why not use plain linear regression for a yes or no answer? Look at the red dashed line. A straight line keeps going: it would predict minus point two for one loan and one point four for another, and neither is a probability. '
                         'The black curve is the sigmoid, also called the logistic function. It takes any score, however large or small, and squeezes it into a number between zero and one. At a score of zero the probability is exactly point five. '
                         'Logistic regression is a linear score followed by this curve. The word regression is historical. It is a classification model. What would a probability of one point four mean to a credit manager?')))

    # ------------------------------------------------------------------ 8 formula
    S.append(dict(kind='formula', title='Logistic regression: a linear score z becomes a probability p by the sigmoid',
                  formulas=[('score', r'$z = b_0 + b_1 x_1 + b_2 x_2 + \cdots + b_p x_p$'), ('probability', r'$p = \frac{1}{1 + e^{-z}}$')],
                  symbols=[['z', 'The score, also the log-odds ln(p / (1 - p))', f'{F["ex_z"]:.2f} for loan {ex.loan_id}'], ['p', 'Predicted probability of default. In Excel: =1/(1+EXP(-z))', f'{F["ex_p"]:.2f} for that loan'],
                           ['b_0', 'Intercept: the score when every feature is 0', f'{b0:.2f}'], ['b_1 ... b_p', 'One coefficient per feature (per 1 standard deviation), learned from the training set', f'ratio: {cof["instalment_to_income"][0]:+.2f}'],
                           ['x_1 ... x_p', 'The feature values of one loan, standardised (z-scores)', f'ratio: {F["ex_row"][F["cols"].index("instalment_to_income")]:+.2f}']],
                  widths=[1.8, 6.0, 4.1], size=24,
                  notes=('Here is the whole model in three lines. First, a score z: an intercept plus each feature times its coefficient, exactly like the line you know from regression. '
                         'Second, the probability p is one divided by one plus e to the power minus z. In Excel that is one divided by one plus EXP of minus z. Third, the same relationship read backwards: z is the log-odds, the natural log of p over one minus p. '
                         'The coefficients are learned from the training loans, after a StandardScaler has put every variable on the same scale. Each symbol is named in the table with a value from one real test loan, which we work through in a moment. Which part of this is already familiar from Session 13?')))

    # ------------------------------------------------------------------ 9 odds table
    S.append(dict(kind='table', title='Log-odds is another way to write a probability: 0 means even odds',
                  headers=['Probability p', 'Odds = p / (1 - p)', 'In words', 'Log-odds z'],
                  rows=[[f'{pp:.2f}', f'{o:.3f}', {0.05: '1 to 19 against', 0.10: '1 to 9 against', 0.20: '1 to 4 against', 0.50: 'even: 1 to 1', 0.80: '4 to 1 in favour'}[pp], f'{lo:+.2f}'] for pp, o, lo in F['odds']],
                  widths=[2.6, 3.2, 3.6, 2.6], icons=['coin', 'coin', 'coin', 'check', 'chart'], note='Odds are what bookmakers quote. A positive log-odds means the positive class is more likely than not.',
                  notes=(f'Probability, odds and log-odds are three ways to say the same thing. Odds are p divided by one minus p. A probability of point two is odds of point two five, which is one to four against. '
                         f'The log-odds is the natural log of the odds. At probability point five the odds are even and the log-odds is zero. Below point five the log-odds is negative, above it positive. '
                         f'A probability of {F["odds"][1][0]:.2f} has log-odds {F["odds"][1][2]:+.2f}. Why bother? Because the log-odds can take any value, so a linear score can model it freely, and the sigmoid converts it back. Can you read the table from probability to log-odds in one row?')))

    # ------------------------------------------------------------------ 10 worked loan
    S.append(dict(kind='example', title='One loan, step by step: from features to a predicted probability',
                  scenario=f'Loan {ex.loan_id} from the test set: {ex.occupation}, instalment-to-income ratio {ex.instalment_to_income:.2f}, late payments {int(ex.previous_late_payments)}.',
                  blocks=[dict(label='1 Score z', text=f'Intercept {b0:.2f}, ratio {t_burden:+.2f}, late payments {t_late:+.2f}, {ex.occupation} {t_boda:+.2f}, 24 other terms {t_rest:+.2f}. Sum z = {F["ex_z"]:.2f}.', mono=True),
                          dict(label='2 Probability', text=f'p = 1 / (1 + e^{-F["ex_z"]:.2f}) = {F["ex_p"]:.2f}: a {pct(F["ex_p"], 0)} percent chance of default.', mono=True),
                          dict(label='3 Decision', text=f'At threshold 0.20 the loan is flagged. At 0.50 it is not.'),
                          dict(label='4 Reality', text=f'In the data this loan {"defaulted" if F["ex_actual"] else "was repaid"}. One loan proves nothing: we judge all {n(F["n_test"])} test loans.', red=True)],
                  notes=(f'Let us follow one loan from the test set through the model. Step one, the score. The intercept is {b0:.2f}. The ratio term adds {t_burden:.2f}, because the instalment-to-income ratio is the strongest predictor. Each term is a coefficient times the loan\'s standardised value. '
                         f'The late payments term adds {t_late:.2f}, the occupation term adds {t_boda:.2f}, and the other twenty four terms together add {t_rest:.2f}. The score z is {F["ex_z"]:.2f}. '
                         f'Step two, the sigmoid turns that into a probability of {F["ex_p"]:.2f}. Step three, at a threshold of point two the loan is flagged. In the data this loan {"defaulted" if F["ex_actual"] else "was repaid"}, but one loan proves nothing. Which step would you check first if the probability looked wrong?')))

    # ------------------------------------------------------------------ 11 coefficients
    S.append(dict(kind='table', title='A coefficient shows the direction of an effect, and its exponent shows the change in odds per standard deviation',
                  headers=['Variable', 'Coefficient b', 'Odds ratio e^b', 'Reading'],
                  rows=[['instalment_to_income', f'{cof["instalment_to_income"][0]:+.2f}', f'{cof["instalment_to_income"][1]:.2f}', f'Per standard deviation (about {F["sd"]["instalment_to_income"]:.2f}): odds multiplied by this much.'],
                        ['previous_late_payments', f'{cof["previous_late_payments"][0]:+.2f}', f'{cof["previous_late_payments"][1]:.2f}', 'Each late-payment step raises the odds.'],
                        ['occupation_Boda rider', f'{cof["occupation_Boda rider"][0]:+.2f}', f'{cof["occupation_Boda rider"][1]:.2f}', 'Higher odds than the other occupations.'],
                        ['occupation_Teacher', f'{cof["occupation_Teacher"][0]:+.2f}', f'{cof["occupation_Teacher"][1]:.2f}', 'Lower odds than the other occupations.'],
                        ['savings_balance_ugx', f'{cof["savings_balance_ugx"][0]:+.2f}', f'{cof["savings_balance_ugx"][1]:.2f}', 'More savings: lower odds.'],
                        ['group_loan', f'{cof["group_loan"][0]:+.2f}', f'{cof["group_loan"][1]:.2f}', 'Group loans have lower odds.']],
                  widths=[3.0, 1.9, 2.0, 5.1], icons=['chart', 'clock', 'bike', 'book', 'coin', 'people'], note='Per 1 standard deviation, other features fixed. scikit-learn adds a penalty by default (regularisation, C = 1.0), so a different scaling or C changes them.',
                  notes=(f'After fitting, the model is a list of coefficients, and we can read them. A positive coefficient raises the log-odds of default, a negative one lowers it. Raise e to the power of the coefficient and you get the odds ratio: '
                         f'the factor by which the odds of default are multiplied when that feature rises by one standard deviation, holding the others fixed. The instalment-to-income ratio has a coefficient of {cof["instalment_to_income"][0]:.2f}, an odds ratio of {cof["instalment_to_income"][1]:.2f}. '
                         f'Boda rider has an odds ratio of {cof["occupation_Boda rider"][1]:.2f} and teacher {cof["occupation_Teacher"][1]:.2f}. Be careful: scikit-learn also applies a penalty on large coefficients by default, called regularisation, with C equal to one, so the sizes depend on the scaling. What does an odds ratio below one tell you?')))

    # ------------------------------------------------------------------ 12 one-hot
    ohe_cols = ['Boda rider', 'Mechanic', 'Teacher', 'Trader']
    ohe_rows = L[L.occupation.isin(ohe_cols[:3] + ['Trader'])].drop_duplicates('occupation').set_index('occupation').loc[['Mechanic', 'Teacher', 'Trader']]
    S.append(dict(kind='wide', title='One-hot encoding turns each occupation into its own column of 0 and 1',
                  visual=dict(kind='dsh_onehot', headers=['occupation'], rows=[[o] for o in ['Mechanic', 'Teacher', 'Trader']], new_headers=['Boda rider', 'Mechanic', 'Teacher', 'Trader', '+3 more'],
                              new_rows=[[str(int(o == c)) if c != '+3 more' else '0 ...' for c in ['Boda rider', 'Mechanic', 'Teacher', 'Trader', '+3 more']] for o in ['Mechanic', 'Teacher', 'Trader']], hl=[(0, 1), (1, 2), (2, 3)]),
                  caption=f'get_dummies makes 15 indicator columns from 3 text variables: 12 columns become {F["X_shape"][1]}.',
                  notes=(f'Models need numbers, so a text variable must be encoded. One-hot encoding makes one new column for each category. A record gets a one in the column of its own category and zero in all the others, and only one column is hot. '
                         f'On the slide, a mechanic gets a one in the Mechanic column. In our loans file, three text variables, gender, occupation and loan purpose, became fifteen indicator columns, so twelve numeric columns became {F["X_shape"][1]}. '
                         'In regression in statistics software you drop one level to avoid the dummy variable trap, where one column can be predicted exactly from the others. Scikit-learn\'s logistic regression penalises large coefficients, called regularisation, so it copes with all of them. Why can we not simply number the occupations from 1 to 7?')))

    # ------------------------------------------------------------------ 13 tree figure
    S.append(dict(kind='wide', title='A decision tree (depth 2) asks yes or no questions, and each leaf gives a predicted probability',
                  visual=dict(kind='dsh_tree', node=t2),
                  caption=f'Depth 2 (the lab tree has one more level), {n(F["n_train"])} training loans. Gold leaf: 25 percent or more default.',
                  notes=(f'This tree was fitted on the {n(F["n_train"])} training loans. The top question asks whether the instalment to income ratio is at most {t2["thr"]:.2f}. Of all the loans, {pct(t2["rate"], 1)} percent defaulted. '
                         f'Loans that answer yes go left, where the default rate is {pct(t2["yes"]["rate"], 1)} percent, and loans that answer no go right, where it is {pct(t2["no"]["rate"], 1)} percent. Each side asks a second question. '
                         'At the bottom are the leaves, and each leaf gives a probability: the share of training loans in that leaf that defaulted. Follow any loan from the top and you reach exactly one leaf. Which leaf would you worry about?')))

    # ------------------------------------------------------------------ 14 tree vocabulary
    lv = leaves(t3)
    S.append(dict(kind='table', title='A tree has a root node, internal nodes and leaf nodes joined by splits',
                  headers=['Term', 'Plain meaning', f'In our tree'],
                  rows=[['Root node', 'The first question, asked of every training loan.', f'{t3["q"]}, asked of {n(t3["n"])} loans'], ['Split', 'One question on one feature with a threshold. The yes and no answers send loans down two branches.', f'{t3["q"]}'],
                        ['Internal node', 'A question asked after the first one.', f'{t3["yes"]["q"]}'], ['Leaf node', 'An end point with no further question. Its predicted probability is the share of its training loans that defaulted.', f'p from {min(l["rate"] for l in lv):.2f} to {max(l["rate"] for l in lv):.2f}'],
                        ['Depth', 'The most questions on any path from root to leaf. We set max_depth to stop the tree growing without limit.', '3 questions, so 8 leaves']],
                  widths=[2.2, 6.0, 3.8], icons=['pin', 'switch', 'question', 'flag', 'chart'],
                  notes=(f'Here is the vocabulary of trees, with the tree you will fit in the lab, which is three questions deep. The root node is the first question, here {t3["q"]}, asked of all {n(t3["n"])} training loans. '
                         'A split is one question on one feature with a threshold. An internal node is a question asked after the first one. A leaf node is an end point: no more questions, and its probability is the share of training loans that defaulted there. '
                         'Depth is the longest path of questions. We limit it with max depth, because an unlimited tree memorises the training loans. How many leaves can a tree of depth three have at most?')))

    # ------------------------------------------------------------------ 15 gini
    S.append(dict(kind='formula', title='A tree chooses each split to make the two groups purer, measured by Gini impurity',
                  formulas=[('Gini impurity', r'$G = 1 - \sum_{k} p_k^2$'), ('after a split', r'$G_{split} = \frac{n_L}{n} G_L + \frac{n_R}{n} G_R$')],
                  symbols=[['G', 'Impurity: 0 is pure, 0.5 is an even mix', f'Root: {F["gini_root"]:.3f}'],
                           ['p_k', 'Share of the group in class k', f'{pct(F["train_pos"] / F["n_train"], 1)}% default at the root'],
                           ['n_L, n_R', 'Loans sent left and right by the split', f'{n(t3["yes"]["n"])} and {n(t3["no"]["n"])}'], ['G_L, G_R', 'Impurity of each group', f'{F["gini_l"]:.3f} and {F["gini_r"]:.3f}'],
                           ['G_split', 'Weighted average of the two groups: the lowest wins', f'{F["gini_split"]:.3f}, down from {F["gini_root"]:.3f}']],
                  widths=[1.9, 5.7, 4.3], size=24,
                  notes=(f'How does the tree choose its questions? It measures how mixed a group is, using Gini impurity. If a group is all one class the impurity is zero. If it is an even mix it is point five. '
                         f'At the root, {pct(F["train_pos"] / F["n_train"], 1)} percent of the training loans defaulted, which gives an impurity of {F["gini_root"]:.3f}. The tree then tries every feature and every threshold. '
                         f'For each candidate it computes the impurity of the two groups, weighted by their size. The split {t3["q"]} gives {F["gini_split"]:.3f}, the lowest, so it becomes the root. Then the tree repeats the search inside each group. The weights are the group sizes, so a tiny pure group cannot hide a large mixed one. Scikit-learn\'s default criterion is called gini. Why do you think the tree must try every threshold?')))

    # ------------------------------------------------------------------ 16 nested IF vs tree
    S.append(dict(kind='compare', title='A nested IF and a decision tree ask the same kind of question',
                  left=dict(head='A nested IF you write', icon='pen', points=['=IF(ratio>1.5,"flag","clear")', 'You choose the thresholds from experience.']),
                  right=dict(head='A tree the computer writes', icon='gear', points=['It finds the thresholds that best separate defaulted from repaid loans.', f'Our tree starts with {t3["q"]}.']),
                  verdict='Same shape. The tree finds the thresholds from examples.',
                  notes=(f'If you have ever written a nested IF in Excel, you have written a tiny decision tree. On the left, you decide the questions and the thresholds from experience. On the right, the computer searches the training loans for the questions and thresholds that best separate the defaulted loans from the repaid ones. '
                         f'The output has the same shape: a path of yes or no answers that ends in a verdict. The tree gives a probability at the end. The rule on the left, with the ratio above one point five, is only an illustration I made up. '
                         f'The first question the tree found is {t3["q"]}. Which kind of rule would your loan officers write?')))

    # ------------------------------------------------------------------ 17 predicted probability and threshold
    S.append(dict(kind='idea', title='The model gives a predicted probability, and the decision threshold turns it into yes or no',
                  visual=dict(kind='dsh_hist', edges=F['hist_edges'], a=F['hist_repaid'], b=F['hist_default'], a_label=f'repaid loans ({n(F["test_neg"])})', b_label=f'defaulted loans ({n(F["test_pos"])})', threshold=0.2),
                  lead='Flag a loan when its probability is at or above the threshold.',
                  points=[f'Defaulted loans sit further right, but the groups overlap.', f'At 0.20, {pct(F["share_above_20_default"], 0)} percent of defaulted loans are flagged, and {pct(F["share_above_20_repaid"], 0)} percent of repaid loans too.', 'scikit-learn predict() uses 0.5. You can choose another.'],
                  notes=(f'This picture shows the logistic regression\'s predicted probabilities on the {n(F["n_test"])} test loans, as a share of each group in each bin. White bars are repaid loans, gold bars are defaulted loans. '
                         f'Defaulted loans tend to sit further to the right, so the model has learned something. But the groups overlap, so no decision threshold is perfect. The red line is a decision threshold of point two. '
                         f'At that threshold {pct(F["share_above_20_default"], 0)} percent of the defaulted loans are flagged, and also {pct(F["share_above_20_repaid"], 0)} percent of the repaid loans. The function predict in scikit-learn uses point five without telling you. Where would you put the line?')))

    # ------------------------------------------------------------------ 18 threshold table
    S.append(dict(kind='table', title='Moving the decision threshold trades missed defaults for false alarms',
                  headers=['Threshold', 'Loans flagged', 'Defaults caught (TP)', 'False alarms (FP)', 'Defaults missed (FN)'],
                  rows=[[f'{t:.2f}', n(T[t]['flagged']), n(T[t]['tp']), n(T[t]['fp']), n(T[t]['fn'])] for t in (0.5, 0.3, 0.2, 0.15, 0.1)],
                  widths=[1.9, 2.3, 2.7, 2.6, 2.7], icons=['lock', 'lock', 'switch', 'bell', 'bell'], note=f'Logistic regression on the {n(F["n_test"])} test loans, of which {F["test_pos"]} defaulted. For reading only: we do not pick a threshold from this table. TP, FP, FN: true positive, false positive, false negative.',
                  notes=(f'Now we move the threshold and count what happens on the {n(F["n_test"])} test loans, {F["test_pos"]} of which defaulted. At the usual point five, the model flags only {T[0.5]["flagged"]} loans. It catches {T[0.5]["tp"]} defaults and misses {T[0.5]["fn"]}. '
                         f'Lower the threshold to point two and it flags {T[0.2]["flagged"]} loans, catching {T[0.2]["tp"]} and missing {T[0.2]["fn"]}, but it raises {T[0.2]["fp"]} false alarms. At point one it catches {T[0.1]["tp"]} and raises {T[0.1]["fp"]} false alarms. '
                         'A false alarm is a false positive and a missed default is a false negative. No threshold wins on both. We read this table to see the trade-off. We do not pick the threshold from it, because the test loans must stay unseen until the end. So how do we choose?')))

    # ------------------------------------------------------------------ 19 costs
    S.append(dict(kind='compare', title='The two mistakes cost different amounts, so the threshold is a business decision',
                  left=dict(head='A missed default', icon='cross', points=['A false negative: the loan is not repaid.', f'Illustrative cost: UGX {n(COST_MISS)}, the principal lost.']),
                  right=dict(head='A false alarm', icon='bell', points=['A false positive: a good borrower is refused.', f'Illustrative cost: UGX {n(COST_ALARM)}, the interest not earned.']),
                  verdict='These two costs are teaching numbers. Use your own lender\'s.',
                  notes=(f'The threshold is a business decision, because the two mistakes cost different amounts. A missed default is a false negative: the money goes out and does not come back. '
                         f'For teaching we say that costs one million shillings. In our file the average defaulted loan is about {n(round(F["avg_default_loan"], -3))} shillings, so the order of magnitude is realistic, but these costs are illustrative. '
                         f'A false alarm is a false positive: a good borrower is refused and the lender loses the interest, which we set at one hundred thousand shillings, also illustrative. A real lender would use its own figures. Which mistake does your organisation fear more?')))

    # ------------------------------------------------------------------ 20 cost curve (training rows, cross-validated)
    grid = F['cost_grid_cv']
    ts = sorted(t for t in grid if abs(t - F['rule_thr']) > 1e-9)
    CT, RW = F['cost_test'], F['rule_row']
    S.append(dict(kind='wide', title=f'Cross-validation on the training loans finds a threshold of {cv_t:.2f}, close to the cost rule 0.0909',
                  visual=dict(kind='dsh_curve', curves=[dict(points=[(t, grid[t] / 1e6) for t in ts], label='Cost on the training loans, out-of-fold', lx=0.12, ly=232, color='ink'),
                                                        dict(points=[(0.02, F['cost_none_cv'] / 1e6), (0.6, F['cost_none_cv'] / 1e6)], label=f'Flag nobody: {cost_m(F["cost_none_cv"])}', lx=0.35, ly=F['cost_none_cv'] / 1e6 + 9, color='mute', dash=True),
                                                        dict(points=[(0.02, F['cost_all_cv'] / 1e6), (0.6, F['cost_all_cv'] / 1e6)], label=f'Flag everybody: {cost_m(F["cost_all_cv"])}', lx=0.35, ly=F['cost_all_cv'] / 1e6 - 12, color='mute', dash=True)],
                              marks=[dict(x=cv_t, y=F['cost_grid_cv'][cv_t] / 1e6, label=f'cheapest: {cv_t:.2f}', dx=0.25, dy=-0.3)],
                              xlabel='decision threshold', ylabel='cost per 2,000 loans, UGX million', xlim=(0, 0.6), ylim=(100, 270), xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], yticks=[100, 150, 200, 250]),
                  caption=f'Training loans, 5-fold. Illustrative: UGX {n(COST_MISS)} per missed default, UGX {n(COST_ALARM)} per false alarm.',
                  notes=(f'The threshold must be chosen without looking at the test loans. So we use only the {n(F["n_train"])} training loans. Cross-validation splits them into five parts. '
                         f'Each part gets probabilities from a model trained on the other four. Then we price the mistakes at every threshold, scaled to 2,000 loans. '
                         f'It is lowest at {cv_t:.2f}, where it is {cost_m(F["cost_cv_curve_at_cv_t"])} million, against {cost_m(grid[0.5])} million at point five. The dashed lines are the extremes. '
                         f'There is also a handy rule that needs no data. If the probabilities are well calibrated, flag a loan when p is at least the cost of a false alarm divided by the sum of both costs, which is 100,000 over 1,100,000, or {F["rule_thr"]:.4f}. The curve is flat from 0.08 to 0.12, so both answers are as good. '
                         'What would change if a false alarm cost five hundred thousand?')))

    # ------------------------------------------------------------------ 20b report once
    flag_all = dict(flagged=F['n_test'], tp=F['test_pos'], fp=F['test_neg'], fn=0)
    S.append(dict(kind='table', title='The test loans are used once, to report the cost of the choices already made',
                  headers=['Choice', 'Threshold', 'Flagged', 'Caught', 'False alarms', 'Missed', 'Cost, UGX million'],
                  rows=[['Default of predict()', '0.50', n(T[0.5]['flagged']), n(T[0.5]['tp']), n(T[0.5]['fp']), n(T[0.5]['fn']), cost_m1(CT[0.5])],
                        ['Cross-validation, training loans', f'{cv_t:.2f}', n(F['cv_row']['flagged']), n(F['cv_row']['tp']), n(F['cv_row']['fp']), n(F['cv_row']['fn']), cost_m1(F['cv_row']['cost'])],
                        ['Cost rule, no data needed', f'{F["rule_thr"]:.4f}', n(RW['flagged']), n(RW['tp']), n(RW['fp']), n(RW['fn']), cost_m1(RW['cost'])],
                        ['Flag nobody', '-', '0', '0', '0', n(F['test_pos']), cost_m1(F['cost_none'])],
                        ['Flag everybody', '0', n(flag_all['flagged']), n(flag_all['tp']), n(flag_all['fp']), '0', cost_m1(F['cost_all'])]],
                  widths=[3.2, 1.8, 1.2, 1.1, 1.6, 1.1, 2.0], icons=['bell', 'check', 'coin', 'lock', 'cross'], hl_col=6,
                  note=f'Illustrative costs, 2,000 test loans, {F["test_pos"]} defaults. Searching the test loans would find 0.08 at UGX {cost_m1(F["cheapest_on_test_for_contrast"]["cost"])} million, a gain of under UGX 5 million that exists only on these loans. We do not do that.',
                  notes=(f'Now, and only now, we use the test loans, once. The default threshold of point five costs {cost_m1(CT[0.5])} million shillings. The threshold from cross-validation, {cv_t:.2f}, costs {cost_m1(F["cv_row"]["cost"])} million: it flags {n(F["cv_row"]["flagged"])} loans, catches {F["cv_row"]["tp"]} of the {F["test_pos"]} defaults, and raises {n(F["cv_row"]["fp"])} false alarms. '
                         f'The cost rule, {F["rule_thr"]:.4f}, costs {cost_m1(RW["cost"])} million. Flagging nobody costs {cost_m1(F["cost_none"])} million and flagging everybody {cost_m1(F["cost_all"])} million. '
                         f'Someone could ask: why not search the test loans for the cheapest threshold? It would give {F["cheapest_on_test_for_contrast"]["threshold"]:.2f} and {cost_m1(F["cheapest_on_test_for_contrast"]["cost"])} million, a saving of under five million that exists only on these two thousand loans. '
                         'That is tuning on the test set, and the score would be optimistic. Which of the two honest choices would you present to your manager?')))

    # ------------------------------------------------------------------ 21 use at work
    S.append(dict(kind='table', title='Where you will use this at work: score every record, then set the decision threshold from the cost',
                  headers=['Your job', 'The yes or no question', 'What today lets you do'],
                  rows=[['Credit risk analyst at a microfinance institution, using scikit-learn', 'Will this loan default?', 'Score every application with a probability and show the manager the cost of each decision threshold in UGX.'],
                        ['Fraud analyst at a mobile money provider, using Python and SQL', 'Is this transaction suspicious?', 'Choose how many cases go to a human reviewer by moving the threshold.'],
                        ['Programme officer at a health organisation, using Excel and Python', 'Will this patient miss the follow-up visit?', 'Rank patients by probability so nurses phone the highest first.'],
                        ['Sales analyst handing results to Power BI', 'Will this customer stop buying?', 'Export a probability column and a flag column that a dashboard can filter.']],
                  widths=[4.0, 3.2, 4.8], icons=['coin', 'shield', 'clinic', 'chart'],
                  notes=('Where will you use this on Monday? Four examples. A credit risk analyst at a microfinance institution scores every application with a probability, and shows the manager the cost of each decision threshold in shillings. '
                         'A fraud analyst at a mobile money provider decides how many cases go to a human reviewer by moving the threshold. A programme officer at a health organisation ranks patients by probability so that nurses phone the highest first. '
                         'And a sales analyst can export a probability column and a flag column to Power BI. The tools differ, but the pattern is the same: a probability, a threshold and a cost. Which is closest to your job?')))

    # ------------------------------------------------------------------ 22 bridge code
    S.append(dict(kind='code', title='Read the recipe before the lab: six lines fit and use both models',
                  code=("X = pd.get_dummies(features, dtype=int)\nmodel = make_pipeline(StandardScaler(),\n    LogisticRegression(max_iter=1000))\nmodel.fit(X_train, y_train)\n"
                        "y_prob = model.predict_proba(X_test)[:, 1]\ntree = DecisionTreeClassifier(\n    max_depth=3, random_state=42)"),
                  reads=[f'Line 1: one-hot encode the text. 12 numeric columns become {F["X_shape"][1]}.', 'Lines 2 and 3: a StandardScaler, then logistic regression with its defaults (L2 penalty, C = 1.0).',
                         'Line 4: fit on the training loans.', 'Line 5: column 1 of predict_proba is the probability of default.', 'Lines 6 and 7: a tree with at most three questions.'],
                  notes=(f'Before the lab, read the recipe. Line one, get dummies, does the one-hot encoding, and twelve numeric columns become {F["X_shape"][1]}. '
                         f'Lines two and three build a pipeline: a standard scaler puts every variable on the same scale, then the logistic regression runs with its defaults, an L2 penalty and C equal to one, called regularisation. That is why the coefficients depend on the scaling. '
                         f'Line four fits on the training loans, which you split in Session 14: {n(F["n_train"])} to learn from and {n(F["n_test"])} kept hidden. '
                         'Line five asks for probabilities. Predict proba returns two columns, and column one is the probability of default, the positive class. Lines six and seven create a tree with at most three questions. '
                         'To flag loans you then compare y prob with a decision threshold. Which line would you change to try a different threshold?')))

    # ------------------------------------------------------------------ 23 divider
    S.append(dict(kind='divider', title='Part 2: the Python lab', lead='Close the slides. Open the notebook.', section='Lab',
                  notes=('That is the end of the ideas. Everything you need is on the slides you have just seen, and the notebook repeats each step. Open the Colab notebook for Session 15 and run the first cell, which puts the course data next to it. '
                         'In every step you will predict first, then run the cell and read the output, and in some steps change one thing and see what moves. The notebook checks your answers as you go and tells you if a number is off.')))

    # ------------------------------------------------------------------ 24 lab map
    S.append(dict(kind='steps', title='The lab has five steps, and you keep a scored file and a threshold note',
                  steps=[dict(head='1 Prepare', text='Ages, income, ratio, one-hot', icon='folder'), dict(head='2 Logistic', text='Split, fit, probabilities', icon='gear'), dict(head='3 Tree', text='Depth 3, read the rules', icon='pin'),
                         dict(head='4 Price', text='Choose and report', icon='coin'), dict(head='5 Keep', text='CSV and note', icon='doc')], highlight=None,
                  caption='Predict, run, read, change. Step 5 writes loan_risk_scores.csv and your threshold note.',
                  notes=('Here is the map of the lab. Step one, prepare the loans exactly as in Session 14: replace the impossible ages, fill missing income with the median, build the instalment-to-income ratio, and one-hot encode the text. '
                         'Step two, split the loans and fit the logistic regression. Step three, fit a tree three questions deep and read its rules. Step four, choose the decision threshold on the training loans by cross-validation, compare it with the cost rule, and report the cost on the test loans once. '
                         'Step five, write the scored file and your threshold note. Please do not skip the predictions. The checks only confirm your answer, and the prediction is where you learn.')))

    # ------------------------------------------------------------------ 25 check your numbers
    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Loans, and the default rate', f'{n(F["rows"])}, and {pct(F["default_rate"], 1)} percent'], ['Columns of X after one-hot encoding', f'{F["X_shape"][1]}'],
                        ['Loans in X_train and X_test, and defaults in y_test', f'{n(F["n_train"])}, {n(F["n_test"])} and {F["test_pos"]}'],
                        ['Coefficient of the ratio in the logistic regression', f'about {cof["instalment_to_income"][0]:+.2f}'],
                        ['Tree depth, leaves, and the root question', f'3, 8 and {t3["q"]}'],
                        ['Logistic regression at 0.20: flagged, caught, false alarms', f'about {T[0.2]["flagged"]}, {T[0.2]["tp"]} and {T[0.2]["fp"]}'],
                        ['Threshold from 5-fold cross-validation, and the cost rule', f'about {cv_t:.2f}, and {F["rule_thr"]:.4f}'],
                        ['Cost on the test loans at the cross-validated threshold', f'near UGX {cost_m(F["cv_row"]["cost"])} million']],
                  widths=[7.4, 4.6], icons=['folder', 'grid', 'bars', 'chart', 'pin', 'switch', 'coin', 'check'], note='scikit-learn may differ from these by a few loans or a unit in the second decimal. If a number is far away, find the step that went wrong.',
                  notes=('Use this table as your own self-check. Nobody marks it. If your numbers match, carry on. Your scikit-learn run may differ from mine by a few loans or a unit in the second decimal, because the solver stops at a slightly different point, and that is fine. '
                         'If a number is far away, stop and find the step that went wrong, because later steps use the earlier ones. A frequent cause is dropping the wrong columns before one-hot encoding. Do not change a number to make it match. '
                         'What does it mean if your X has twenty six columns instead of twenty seven?')))

    # ------------------------------------------------------------------ 26 error cards
    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[['ValueError: could not convert string to float', 'A text variable such as occupation is still in X.', 'Run pd.get_dummies on the features before fitting.'],
                        ['KeyError on a column name', 'A misspelt or already dropped column.', 'Print df.columns and copy the exact name.'],
                        ['A probability above 0.9 for many loans', 'You used the leaking column collection_calls.', 'Drop it. Session 16 explains why.'],
                        ['predict_proba gives two columns and the numbers look backwards', 'Column 0 is the probability of repaid.', 'Take column 1 for the probability of default.'],
                        ['ValueError: Found input variables with inconsistent numbers of samples', 'X and y have different row counts, for example one was filtered and the other not.', 'Filter both, or filter before you split.']],
                  widths=[3.8, 4.1, 4.1], icons=['cross', 'cross', 'cross', 'cross', 'cross'],
                  notes=('Five messages you may meet. A ValueError about converting a string to a float means a text variable is still in your features, so run get dummies first. A KeyError means a misspelt column name, so print the columns and copy the name. '
                         'Probabilities above point nine for many loans mean you kept the collection calls column. Drop it, and we explain why next session. If the numbers look backwards, you probably took column zero of predict proba, which is the probability of repaid. '
                         'Last, a ValueError about inconsistent numbers of samples means X and y have different row counts, so filter both together. Read the message first. It usually tells you the answer.')))

    # ------------------------------------------------------------------ 27 exit check
    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[['A model gives a loan p = 0.30. What does that number mean, and what does a threshold of 0.20 do with it?', 'A 30 percent chance of default, as the model estimates. At threshold 0.20 the loan is flagged, because 0.30 is at or above 0.20.'],
                        ['Why do we one-hot encode occupation before fitting?', 'The model works on numbers. One-hot encoding gives each occupation its own 0 or 1 column, with no false order between them.'],
                        ['A missed default costs ten times a false alarm. Should the threshold be higher or lower than 0.50, and why?', 'Lower. Missing a default is the dearer mistake, so flag more loans and accept more false alarms.']],
                  widths=[5.8, 6.2], icons=['chart', 'grid', 'coin'],
                  notes=('Last, the exit check. Three questions. Write your answers in your notes before you look at mine. One, a model gives a loan a probability of point three: what does that mean, and what does a threshold of point two do with it? '
                         'Two, why do we one-hot encode occupation before fitting? Three, a missed default costs ten times a false alarm: should the threshold be higher or lower than point five, and why? '
                         'The short answers are on the slide. If you got all three, you are ready for Session 16. If one surprised you, look at that step of the notebook again tonight.')))

    # ------------------------------------------------------------------ facilitator
    sess['facilitator'] = dict(
        prep=['Open the deck and the Session 15 notebook in Colab before anyone arrives. Check that loans.csv, answer_key.json and the data zip load from the first cell.',
              f'IMPORTANT, an honest open item: every number on the slides, in these notes and in the notebook checks comes from a NumPy replica (content/loans_canon.py and h_loans.py), not from real scikit-learn. Before the course starts, run the solution notebook once in Colab. '
              f'First check that X_test.index[:10] is [4299, 1151, 2351, 5249, 1328, 3988, 261, 3389, 6878, 5150] and X_test.index.sum() is 8,081,998. If not, the split differs and every number must be recomputed. '
              f'Then expect small differences only: a real LogisticRegression can move a count at a threshold by a few loans (for example {T[0.2]["tp"]} caught at 0.20) and the AUC by about 0.001. The notebook checks use these tolerances: counts at 0.20 within 4 to 8 loans, the coefficient of the ratio within 0.05, the threshold from cross-validation within 0.03 (the cost curve is flat from 0.08 to 0.12), costs within UGX 6 million.',
              'Write the check table (the slide titled Check your numbers) on the board before the lab.',
              'Concepts run with laptops closed. Ask learners to open Colab only after the Part 2 divider.',
              'Remind learners that all data is fictional and generated. The costs in UGX are teaching numbers, not Nile Microfinance policy. The factor 1.15 in the ratio is an illustrative assumption.',
              'The decision threshold is chosen on the TRAINING loans (cross-validation or the cost rule 0.0909). The test loans are used once, on slide "The test loans are used once". If a learner suggests searching the test loans for the cheapest threshold, use that moment to teach tuning on the test set.'],
        misconceptions=[('Positive class means the good outcome', 'Positive is the outcome we look for. Here it is default, which is bad news for the lender.'),
                        ('Logistic regression is a regression that predicts a number', 'It predicts a probability and is used for classification. The word regression is historical.'),
                        ('A probability of 0.3 means the model predicts no default', 'It predicts no default only if the threshold is above 0.3. The threshold is our choice and is not fixed at 0.5.'),
                        ('Number the occupations 1 to 7 instead of one-hot encoding', 'Numbers 1 to 7 invent an order and a distance between jobs. One-hot columns do not.'),
                        ('The tree with the most leaves is the best tree', 'A deep tree memorises the training loans. We limit depth. Session 17 returns to overfitting.'),
                        ('Pick the threshold that is cheapest on the test loans', 'That tunes on the test set, so the reported cost is optimistic. Choose on the training loans, then report on the test loans once.')],
        probes=[('What is the positive class in the loans file?', 'Default, coded 1.'), ('What does predict_proba[:, 1] return?', 'The probability of the positive class, default.'),
                ('Why does a lower threshold catch more defaults?', 'More loans pass the decision threshold, so more of the defaulted ones are among the flagged. False alarms rise too.'),
                ('What is the log-odds of a probability of 0.5?', '0. The odds are 1 to 1.'), ('How does the tree choose a split?', 'It tries every feature and threshold and keeps the one that gives the lowest weighted Gini impurity.'),
                ('Why is the threshold a business decision?', 'Because the cost of a missed default and the cost of a false alarm differ, and only the business knows them.'),
                ('Why are the coefficients per standard deviation?', 'The pipeline standardises each variable first, and the L2 penalty (C = 1.0) depends on the scale, so a different scaling gives different coefficients.')],
        lab_steps=[('Step 1: prepare and one-hot encode', f'{n(F["rows"])} loans, default rate {pct(F["default_rate"], 1)} percent, the same preparation as Session 14. Watch for learners who drop rows instead of replacing the two impossible ages.'),
                   ('Step 1 check', f'X has {F["X_shape"][1]} columns. If it has 26, a text column was dropped by mistake. If it has errors, text remains.'),
                   ('Step 2: split and fit', f'{n(F["n_train"])} and {n(F["n_test"])}; {F["test_pos"]} defaults in y_test. Coefficient of the ratio near {cof["instalment_to_income"][0]:+.2f} per standard deviation. Test AUC {F["auc_lr"]:.3f}.'),
                   ('Step 3: tree', f'Depth 3, 8 leaves, root {t3["q"]}. Ask learners to read one path aloud in plain words.'),
                   ('Step 4: threshold', f'Cross-validation on the training loans gives about {cv_t:.2f}; the rule gives {F["rule_thr"]:.4f}. Test cost at {cv_t:.2f}: UGX {cost_m1(F["cv_row"]["cost"])} million; rule: {cost_m1(RW["cost"])} million; 0.50: {cost_m1(CT[0.5])} million. Let learners change the two costs and watch both thresholds move.'),
                   ('Step 5: keep', 'loan_risk_scores.csv with 2,000 rows and a three-line threshold note.')],
        rescue=['If the concepts run over, shorten the Gini slide and the coefficients slide to a quick look; the lab covers both.', 'If only 30 minutes of lab remain, do steps 1 to 3 and step 5, and set the tree as homework.',
                'If a learner has no Colab access, run the notebook on your screen and ask the learner to call out the predictions.', 'If a learner is stuck on get_dummies, hand over the X shape check and move on.',
                'If cross_val_predict is slow, use cv=3 and say that the threshold may differ by 0.01.'],
        after=['Share the notebook and this deck again for learners who were absent.', 'Ask each learner to save loan_risk_scores.csv and bring one real yes or no question from their own work to Session 16.', 'Note any question you could not answer and open the next session with it.'],
        lab_answer_key=[['Step 2 PREDICT: will the coefficient of the ratio be positive or negative?', f'Positive, about {cof["instalment_to_income"][0]:+.2f} per standard deviation: a heavier ratio raises the log-odds of default.'],
                        ['Step 2 READ: what is the average predicted probability on the test loans?', f'About {p.mean():.2f}, close to the default rate of {pct(F["default_rate"], 1)} percent.'],
                        ['Step 3 PREDICT: which variable will the first split use?', f'instalment_to_income, at about {t3["thr"]:.2f}.'],
                        ['Step 3 CHANGE: set max_depth=2. How many leaves?', '4 leaves.'],
                        ['Step 4 PREDICT: will the threshold be above or below 0.5?', f'Below. Missing a default costs ten times a false alarm. About {cv_t:.2f} by cross-validation, {F["rule_thr"]:.4f} by the rule.'],
                        ['Step 4 CHANGE: make a false alarm cost 500,000 instead of 100,000.', 'The threshold rises, because false alarms are dearer. The rule gives 500,000 / 1,500,000 = 0.33. Cross-validation on the training loans gives a similar value.'],
                        ['Step 5 READ: how many loans does loan_risk_scores.csv hold?', f'{n(F["n_test"])}, one row for each test loan.']])
    return sess
