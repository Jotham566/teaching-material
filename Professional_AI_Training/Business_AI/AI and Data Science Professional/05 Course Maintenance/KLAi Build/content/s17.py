"""Session 17: Forests, boosting and overfitting (author i). Python lab, notebook in content/labs/s17_nb.py.

Every number on a slide, in a note or in the notebook checks comes from s17_facts.facts(): the Lakeside branch_weeks and the Nile Microfinance loans, with trees, bagging, a random forest,
gradient boosting, logistic regression and permutation importance written in NumPy (scikit-learn is not installed in the build sandbox). The slides say so where it matters."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import s17_facts as SF  # noqa: E402

RED_, INK_, MUTE_ = '#AE2525', '#111111', '#666666'   # figure colours: the KLAi red, ink and mute grey
E = 2.718281828459045


def n(x):
    return f'{int(x):,}'


def d3(x):
    return f'{x:.3f}'


def d2(x):
    return f'{x:.2f}'


def build():
    F = SF.facts()
    P = F['poly']
    rm = {d: (a, b) for d, a, b in P['rmse']}
    L = F['lr']
    cols = SF.COLS
    coef = dict(zip(cols, L['w']))
    C = F['canon']
    ITI = 'instalment_to_income'
    trows = {r['depth']: r for r in F['tree_rows']}
    t3, tnone = trows[3], trows[None]
    fc = {r['trees']: r['test'] for r in F['forest_curve']}
    bc = {r['trees']: r for r in F['boost_curve']}
    g = F['grid']
    gb = F['grid_best']
    tu = F['tuned']
    h = F['hand']
    pf = {r['col']: r for r in F['perm_forest']}
    dup = F['dup']
    st = F['single_tree']
    cv_lr, cv_b, cv_t = F['cv_lr'], F['cv_boost'], F['cv_tree3']
    ex = L['example']
    f100 = F['forest100']
    b100 = F['boost100']
    gdepth = 'no depth limit' if gb['max_depth'] is None else f'depth {gb["max_depth"]}'
    close = sorted([k for k, v in g.items() if v['mean'] >= gb['mean'] - 0.005], key=lambda k: -g[k]['mean'])
    sess = dict(
        num=17, block='Module D: Machine learning', short_title='Forests, boosting and overfitting',
        title='Forests, boosting and overfitting: a stronger model without fooling ourselves',
        question='How do we get a stronger model without fooling ourselves?',
        outcomes=['Explain overfitting, underfitting and the bias-variance trade-off from training error and test error',
                  'Describe how bagging (a random forest) and gradient boosting build an ensemble, and tune their hyperparameters with cross-validation',
                  'Read logistic regression coefficients and permutation importance without over-claiming, and ship the simpler model when scores are close'],
        outcome_icons=['chart', 'gear', 'check'],
        outcome_note=('Here is what you can do by the end of today. You can explain overfitting and underfitting, and the bias-variance trade-off, by comparing training error with test error. '
                      'You can describe how a random forest and gradient boosting each combine many trees into one ensemble, and tune their settings with cross-validation. '
                      'And you can read the coefficients of a logistic regression and the permutation importance of a forest without claiming more than they show, then choose the simpler model when the scores are close. '
                      'We use the Nile Microfinance loans for all of it.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: picture, plain words, one example by hand'), (10, 'Break'), (45, 'Lab: predict, run, read, change'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: concepts first, then a Python lab',
        plan_caption='Ideas with pictures first. Then you open the notebook. Then the checks and what you keep.',
        plan_note=('We have two hours. The first ten minutes bring back Session 16 and set the question for today. Then forty-five minutes of concepts, with no laptops open, so you can watch the pictures and the worked numbers. '
                   'After a ten minute break we open the notebook for a forty-five minute lab on the Nile Microfinance loans. You will predict each result, run it, read it, and change one thing. '
                   'The last ten minutes are an exit check and what you keep. The lab is where the learning sticks, so please protect that time.'),
        recall_from='Session 16',
        recall=[('A loan model scored far too well after one column was added. What kind of column does that, and what is it called?',
                 'A column that is only recorded after the outcome is known, here collection_calls. It is data leakage.'),
                ('Why use 5-fold cross-validation instead of one train and test split?',
                 'Each part of the data takes a turn as the test fold, so you get five scores and their average depends less on luck.'),
                ('What does an AUC of 0.5 mean?', 'The model ranks a defaulted loan above a repaid one no better than a coin toss.')],
        words=[('Overfitting and underfitting', 'Overfitting: the model fits noise, so training rows score well and new rows score worse. Underfitting: too simple to see the pattern.'),
               ('Ensemble (random forest, gradient boosting)', 'Many small models combined into one. A forest averages trees (bagging). Boosting adds trees, each fitting the residual errors so far.'),
               ('Hyperparameter', 'A setting chosen before training, such as max_depth. Parameters are learned from the data. Tuning tries combinations with cross-validation.'),
               ('Permutation importance', 'The drop in test score when one variable is shuffled. It shows what the model relies on. It does not show a cause.'),
               ('Parsimony (model selection)', 'When scores are close, ship the simpler model. It is easier to explain, check and maintain.')],
        word_icons=['chart', 'people', 'gear', 'magnifier', 'check'],
        words_note=('Five words for today. Overfitting is a model that has learned the noise in its training rows, and underfitting is a model too simple to see the pattern. '
                    'An ensemble is many small models combined into one, and the two famous kinds are the random forest and gradient boosting. A hyperparameter is a setting you choose before training, and tuning means trying combinations with cross-validation. '
                    'Permutation importance shows what a model relies on. And parsimony is the rule that when scores are close, you ship the simpler model. We use each word before the end of the session.'),
        keep='Keep your model comparison table: train, cross-validated and test AUC for four models on the Nile Microfinance loans, plus a three-sentence model decision memo that says which model you would ship and why.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab file', value='Comparison table'), dict(label='The decision', value='Memo: which model'), dict(label='Next session', value='Groups, no labels')]),
        keep_title='Save your notebook with the comparison table and the decision memo',
        next='Session 18: Finding structure without labels. We group customers with k-means and flag unusual orders.', next_label='Next session',
        keep_note=('Before you go, save your notebook with the comparison table and your decision memo. The table is your keepsake from today: four models, three scores each, and the gap between training and test. '
                   'If you can show it to a credit manager and they can see why you chose the model you chose, it is good. Next session we have no answer column at all, and we look for groups of customers. '
                   'If anything was unclear today, write the question down and bring it.'),
        cover_note=('Welcome back. Last session we learned to judge a model with a confusion matrix, precision, recall and AUC, and to catch a column that leaks the answer. '
                    'Today we ask how to build a stronger model without fooling ourselves. We start with a curve you can draw in Excel, then forests and boosting on the Nile Microfinance loans, then cross-validation to tune them. '
                    'The question at the end is a business one: when two models score about the same, which one do you ship?'),
        use_at_work='Compare models on cross-validated and test scores, check the training-test gap, and ship the simpler model when scores are close.',
        slides=[])
    S = sess['slides']

    # ------------------------------------------------------------------ 1 answers
    S.append(dict(kind='table', title='Answers to the three questions from Session 16', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in sess['recall']], widths=[5.2, 6.8], icons=['key', 'grid', 'chart'],
                  notes=('Here are the answers to the three warm-up questions. A column that is recorded only after the outcome is known, like collection calls, leaks the answer into the model. That is data leakage, and the score looks wonderful and means nothing. '
                         'Cross-validation gives every part of the data a turn as the test fold, so you get five scores and their average depends less on luck. '
                         'And an AUC of zero point five means the model ranks a defaulted loan above a repaid one no better than a coin toss. Today we keep all three habits. Which one do you use already at work?')))

    # ------------------------------------------------------------------ 2 three curves
    S.append(dict(kind='wide', title='Underfitting, a good fit and overfitting on 15 training weeks at the Jinja branch',
                  visual=dict(kind='ds_i_fitpanels', panels=[
                      dict(title='Underfitting: degree 0', sub=f'training error {rm[0][0]:.1f}, test error {rm[0][1]:.1f}', curve=P['curves'][0]),
                      dict(title='Good fit: degree 1', sub=f'training error {rm[1][0]:.1f}, test error {rm[1][1]:.1f}', curve=P['curves'][1]),
                      dict(title='Overfitting: degree 6', sub=f'training error {rm[6][0]:.1f}, test error {rm[6][1]:.1f}', curve=P['curves'][6], color=RED_)],
                      train=[(P['footfall'][i], P['orders'][i]) for i in P['tr']], test=[(P['footfall'][i], P['orders'][i]) for i in P['te']], xlabel='footfall: visitors counted at the door in one week',
                      ylabel='orders per week', xr=(1350, 2900), yr=(0, 60), yticks=[20, 40]),
                  caption='Each dot is one week. Degree is the number of bends the red curve may have.',
                  notes=(f'Let us start with a picture you can draw in Excel. Each dot is one week at the Jinja branch of Lakeside Mart: footfall, the visitors counted at the door, against orders. '
                         f'We fitted a curve on only {P["n_train"]} of the {P["weeks"]} weeks, the filled dots, and kept {P["n_test"]} weeks hidden, the hollow dots. In an Excel scatter chart this is a trendline: Linear is degree one, and the Polynomial option with order 2 to 6 gives higher degrees. Degree zero is an AVERAGE formula. '
                         f'Degree zero is a flat line at the mean, and it misses the pattern: that is underfitting. Degree one is about right. Degree six follows the training dots closely but swings wildly between them: that is overfitting. '
                         f'The error is RMSE, the typical size of the miss in orders per week. Which panel would you trust to forecast next week?')))

    # ------------------------------------------------------------------ 3 error curves
    S.append(dict(kind='idea', title='Training error keeps falling as the curve gets more flexible, but test error rises again',
                  visual=dict(kind='ds_i_curves', xs=[0, 1, 2, 3, 4, 5, 6], series=[dict(label='Training', ys=[rm[d][0] for d in range(7)], kind='ink'), dict(label='Test', ys=[rm[d][1] for d in range(7)], kind='red')],
                              xlabel='polynomial degree: number of bends allowed', ylabel='RMSE, orders per week', ymin=0, ymax=20, ticks=[0, 5, 10, 15, 20], fmt='{:.0f}', mark=2, mark_label='lowest test error',
                              zones=[(0, 0, 'Underfitting', MUTE_), (5, 6, 'Overfitting', RED_)], right=1.6),
                  lead='Training error always improves. Test error is the honest score.',
                  points=[f'Training error: {rm[0][0]:.1f} down to {rm[6][0]:.1f}.', f'Test error: lowest at degrees 1 and 2 ({rm[2][1]:.1f}), then {rm[6][1]:.1f} at degree 6.', 'RMSE: the typical miss, in orders per week.'],
                  notes=(f'Now the same experiment for degrees zero to six. The dark line is the training error, measured on the weeks the curve learned from. It only goes down, from {rm[0][0]:.1f} to {rm[6][0]:.1f}. '
                         f'The red line is the test error, measured on weeks the curve never saw. It is lowest at degrees one and two, {rm[2][1]:.1f} orders per week, and then it climbs: {rm[6][1]:.1f} at degree six. The chart stops there. Degree seven, which the Excel trendline menu cannot draw, has a test error of {rm[7][1]:.0f}. '
                         'So training error cannot tell you when to stop, because it rewards memorising. Only error on held-back rows can. '
                         'Why would a very flexible curve do well on the weeks it has seen and badly on a new week?')))

    # ------------------------------------------------------------------ 4 bias variance
    S.append(dict(kind='compare', title='The bias-variance trade-off: two ways to be wrong',
                  left=dict(head='High bias: underfitting', points=['Bias is error from a model too simple for the pattern.', 'Wrong on training and new rows alike.']),
                  right=dict(head='High variance: overfitting', points=['Variance is how much the model changes when the training rows change.', 'Right on training rows, wrong on new rows.']),
                  verdict='More flexibility lowers bias and raises variance. Pick the best test score.',
                  notes=('These two words come up in every machine learning interview. Bias is the error that comes from a model that is too simple for the pattern, like the flat line. It is wrong in the same way on the training rows and on new rows. '
                         'Variance is how much the fitted model would change if you gave it a different set of training rows. A model with high variance chases the noise of the particular rows it saw, so it is right on those and wrong on new ones. '
                         'The bias-variance trade-off says you cannot lower both together by adding flexibility. You look for the setting where the test score is best. Which of the two worries you more at your own work?')))

    # ------------------------------------------------------------------ 5 tree depth
    S.append(dict(kind='idea', title='A decision tree overfits as max_depth grows: training AUC reaches 1.00 and test AUC falls',
                  visual=dict(kind='ds_i_curves', xs=['1', '2', '3', '4', '6', '8', '12', 'none'],
                              series=[dict(label='Training', ys=[trows[d]['train'] for d in SF.TREE_DEPTHS], kind='ink'), dict(label='Test', ys=[trows[d]['test'] for d in SF.TREE_DEPTHS], kind='red')],
                              xlabel='max_depth: most questions a loan can be asked', ylabel='AUC', ymin=0.5, ymax=1.0, ticks=[0.5, 0.6, 0.7, 0.8, 0.9, 1.0], mark=2, mark_label='best test AUC', right=1.6),
                  lead='max_depth: the most yes or no questions a loan can be asked.',
                  points=[f'Depth 3: train {d3(t3["train"])}, test {d3(t3["test"])}.', f'No limit ({tnone["real_depth"]} deep): train {tnone["train"]:.3f}, test {d3(tnone["test"])}.', 'Gap = train AUC minus test AUC.'],
                  notes=(f'Now the same idea on the Nile Microfinance loans, with a decision tree. The setting max_depth is the largest number of yes or no questions a loan can be asked on the way down. At depth three, training AUC is {d3(t3["train"])} and test AUC is {d3(t3["test"])}. '
                         f'With no limit, the tree grows {tnone["real_depth"]} questions deep and has {tnone["leaves"]} leaf nodes. It scores a perfect {tnone["train"]:.3f} on the training loans, because it has memorised them, and only {d3(tnone["test"])} on the test loans, which is barely better than a coin toss. '
                         'The distance between the two scores is the generalisation gap. The tree here is our own NumPy copy of the scikit-learn algorithm, so rerun it in Colab before you quote the decimals. Where does the gap start to open?')))

    # ------------------------------------------------------------------ 6 parameter vs hyperparameter
    S.append(dict(kind='table', title='Parameters are learned from the data. Hyperparameters are chosen before training',
                  headers=['', 'Parameter', 'Hyperparameter'],
                  rows=[['Who sets it', 'The learning algorithm, from the training rows', 'You, before training starts'],
                        ['In a decision tree', 'Each split question and its threshold', 'max_depth, min_samples_leaf'],
                        ['In a random forest or boosting', 'The splits inside every tree', 'n_estimators, max_features, learning_rate'],
                        ['In logistic regression', 'The coefficients and the intercept', 'C, the strength of the regularisation penalty (default 1.0, L2). The penalty makes the coefficients depend on the scaling'],
                        ['How to choose it', 'Fit the model', 'Hyperparameter tuning with cross-validation']],
                  widths=[2.6, 4.7, 4.7], icons=['key', 'tag', 'people', 'chart', 'gear'],
                  notes=('This table separates two kinds of numbers. Parameters are learned from the training rows: the split questions in a tree, or the coefficients in a logistic regression. You never type them in. '
                         'Hyperparameters are settings you choose before training. In a tree they are max depth and the minimum number of loans in a leaf. In a forest or in boosting they are the number of trees, the number of variables tried at each split and the learning rate. '
                         'You cannot learn a hyperparameter from the training rows, because the best training score always asks for more flexibility. So you choose it with cross-validation. Which hyperparameter have you met before?')))

    # ------------------------------------------------------------------ 7 bagging
    S.append(dict(kind='wide', title='Bagging: grow many trees on bootstrap samples and average their predictions',
                  visual=dict(kind='ds_i_bootstrap', ids=list(range(1, 9)), samples=F['boot_demo']),
                  caption='Gold rows were drawn twice or more (x2, x3). About 37 percent are left out. Illustrative: 8 rows.',
                  notes=('A single tree is unstable, because a different set of training rows gives a different tree. Bagging fixes that by averaging. Bagging is short for bootstrap aggregation. '
                         'A bootstrap sample draws rows at random with replacement, so some rows appear twice or more, shown in gold, and others are left out. About thirty seven percent of the rows are left out of each sample. '
                         'The picture uses eight made-up rows. We grow one tree on each sample and average their predictions into one. Each tree is a little wrong in its own way, and averaging cancels much of that. '
                         'Why would averaging help a model that has high variance?')))

    # ------------------------------------------------------------------ 8 forest curve
    S.append(dict(kind='idea', title=f'Averaging many trees lifts test AUC from {d2(st["mean"])} for one tree to {d2(f100["test"])} for a forest',
                  visual=dict(kind='ds_i_curves', xs=[str(k) for k in SF.FOREST_STEPS], series=[dict(label='Test AUC', ys=[fc[k] for k in SF.FOREST_STEPS], kind='red')],
                              xlabel='number of trees averaged', ylabel='test AUC', ymin=0.5, ymax=0.8, ticks=[0.5, 0.6, 0.7, 0.8], right=1.9),
                  lead='More trees help up to about 50. After that the curve is flat and small ups and downs are noise.',
                  points=[f'One tree: test AUC {d3(st["mean"])} on average ({d3(st["lo"])} to {d3(st["hi"])}).', f'Forest of 100 trees: {d3(f100["test"])}.', f'Training AUC is still {f100["train"]:.3f}.'],
                  notes=(f'Here is what averaging buys on the loans. One fully grown tree scores about {d3(st["mean"])} on the test loans on average, and the {st["n"]} trees range from {d3(st["lo"])} to {d3(st["hi"])}. '
                         f'Average five trees and the test AUC is {d3(fc[5])}. Average a hundred and it is {d3(f100["test"])}. After about fifty trees the curve is flat, and the small ups and downs after that are noise, so adding more trees costs time and gains little. '
                         f'Notice that the training AUC of the forest is still {f100["train"]:.3f}. Each tree memorises its sample, yet the average generalises much better. These are NumPy forests that follow the textbook algorithm, so scikit-learn will give similar but not identical numbers. '
                         'Why does the curve stop rising?')))

    # ------------------------------------------------------------------ 9 random forest
    S.append(dict(kind='steps', title='A random forest is bagging plus a random subset of variables at every split',
                  steps=[dict(head='1 Sample', text='Draw a bootstrap sample of the training rows', icon='bag'), dict(head='2 Grow', text='Grow a deep tree. At each split, try only 3 of the 12 variables', icon='plant'),
                         dict(head='3 Repeat', text='Do this for 100 trees', icon='clock'), dict(head='4 Average', text='Average the predicted probabilities', icon='calculator')], highlight=None,
                  caption=f'An ensemble is many models combined into one prediction. Test AUC on our loans: bagging with all 12 variables {d3(F["bag100"]["test"])}, random forest {d3(f100["test"])} (100 trees).',
                  notes=(f'A random forest is bagging with one extra idea. At every split, the tree may look at only a random subset of the variables, here three of the twelve. That stops every tree from asking the same strongest question first, so the trees differ more, and averaging different trees works better. '
                         f'An ensemble is the general word: many models combined into one prediction. On our loans, plain bagging with all twelve variables gives a test AUC of {d3(F["bag100"]["test"])}, and the random forest gives {d3(f100["test"])}. '
                         'In scikit-learn the class is RandomForestClassifier. Its settings include n_estimators, the number of trees, and max_features, which is the square root of the number of variables by default, so three of twelve. Plain bagging is BaggingClassifier. Which step makes the trees different from each other?')))

    # ------------------------------------------------------------------ 10 boosting picture
    S.append(dict(kind='wide', title='Gradient boosting: each new tree fits the residual errors of the ensemble so far',
                  visual=dict(kind='ds_i_boost', x=h['footfall'], y=h['orders'], xlabel='footfall: visitors per week', ylabel='orders per week', yr=(0, 60), panels=[
                      dict(title='Start: the mean', sub=f'sum of squared residuals {h["steps"][0]["sse"]:.1f}', pred=h['steps'][0]['pred']),
                      dict(title='After tree 1', sub=f'sum of squared residuals {h["steps"][1]["sse"]:.1f}', pred=h['steps'][1]['pred']),
                      dict(title='After tree 2', sub=f'sum of squared residuals {h["steps"][2]["sse"]:.1f}', pred=h['steps'][2]['pred'])]),
                  caption='Red line: prediction. Dashed: residual (actual minus predicted). Learning rate 0.5.',
                  notes=(f'Boosting grows trees one after another. Look at six Jinja weeks. We start with the mean, {h["steps"][0]["pred"][0]:.1f} orders, as the prediction for every week. The dashed lines are the residuals: actual minus predicted. The sum of the squared residuals is {h["steps"][0]["sse"]:.1f}. '
                         f'Tree one is a single question about footfall. It predicts the average residual on each side, and we add half of that correction, because the learning rate is one half. The sum falls to {h["steps"][1]["sse"]:.1f}. '
                         f'Tree two fits the residuals that are left, and the sum falls again to {h["steps"][2]["sse"]:.1f}. That is gradient boosting: each tree fits the residual errors of the ensemble so far. What would happen if we kept adding trees for ever?')))

    # ------------------------------------------------------------------ 11 boosting arithmetic
    hs = h['steps']
    rows = []
    for i in range(6):
        rows.append([n(h['footfall'][i]), n(h['orders'][i]), f'{hs[0]["pred"][i]:.1f}', f'{hs[0]["resid"][i]:+.1f}', f'{h["stumps"][0]["corr"][i]:+.3f}', f'{hs[1]["pred"][i]:.3f}', f'{hs[1]["resid"][i]:+.3f}'])
    S.append(dict(kind='table', title='The arithmetic of one boosting step on six weeks',
                  headers=['Footfall', 'Orders', 'Start: mean', 'Residual', 'Tree 1 adds', 'Prediction now', 'New residual'], rows=rows, widths=[1.5, 1.4, 1.7, 1.6, 1.8, 2.0, 1.9], icons=False,
                  note=f'Tree 1 asks: is footfall at most {n(h["stumps"][0]["feat_thr"])}? The mean residual is +5.5 on the yes side and -2.75 on the no side. The learning rate 0.5 halves each correction.',
                  notes=(f'Here are the same numbers in a table, so you can check the arithmetic. The start is the mean, {hs[0]["pred"][0]:.1f} orders. The residual is the actual orders minus that mean. '
                         f'Tree one asks one question: is footfall at most {n(h["stumps"][0]["feat_thr"])}? The two weeks on the yes side have an average residual of plus five point five, and the four weeks on the no side have minus two point seven five. '
                         'We add half of each, because the learning rate is one half. That gives plus two point seven five and minus one point three seven five in the Tree 1 column. The new residuals are smaller on the whole, and the sum of squares fell. Can you check one row yourself?')))

    # ------------------------------------------------------------------ 12 forest vs boosting
    S.append(dict(kind='compare', title='Forest or boosting: two ways to build an ensemble',
                  left=dict(head='Random forest (bagging)', points=['Deep trees grow side by side on bootstrap samples.', 'Each tree overfits. Averaging cancels the noise.', 'Settings: n_estimators, max_depth, max_features.']),
                  right=dict(head='Gradient boosting', points=['Shallow trees grow in a sequence, each fitting the residual errors so far.', 'Settings: n_estimators, learning_rate, max_depth.']),
                  verdict='Both are ensembles. Both need tuning, and both can overfit.',
                  notes=('Here is the contrast. A random forest grows deep trees side by side and averages them. Each tree overfits, and the average smooths that out. Its main settings are the number of trees, the depth and how many variables to try at each split. '
                         'Gradient boosting grows shallow trees in a sequence, each fitting the residual errors of the ensemble so far, and adds a small correction each time. Its main settings are the number of trees, the learning rate and the depth. '
                         'Both are called ensembles, because many models make one prediction. Boosting is the more sensitive of the two, as the boosting curve will show. Which one would you try first on a new table?')))

    # ------------------------------------------------------------------ 13 boosting curve
    S.append(dict(kind='idea', title=f'Boosting keeps improving the training AUC, but the test AUC peaks near {F["boost_stage_best_n"]} trees',
                  visual=dict(kind='ds_i_curves', xs=[str(k) for k in SF.BOOST_STEPS], series=[dict(label='Training', ys=[bc[k]['train'] for k in SF.BOOST_STEPS], kind='ink'), dict(label='Test', ys=[bc[k]['test'] for k in SF.BOOST_STEPS], kind='red')],
                              xlabel='trees added (learning rate 0.1, depth 3)', ylabel='AUC', ymin=0.5, ymax=1.0, ticks=[0.5, 0.6, 0.7, 0.8, 0.9, 1.0], mark=2, mark_label='near the best', right=1.6),
                  lead='Past the peak, extra trees fit noise.',
                  points=[f'50 trees: train {d3(bc[50]["train"])}, test {d3(bc[50]["test"])}.', f'500 trees: train {d3(bc[500]["train"])}, test {d3(bc[500]["test"])}.', f'Best test AUC {d3(F["boost_stage_best"])}, at {F["boost_stage_best_n"]} trees. Picked from the test curve, for illustration only.'],
                  notes=(f'This is boosting on the loans, with learning rate zero point one and trees of depth three. The training AUC keeps climbing, from {d3(bc[10]["train"])} at ten trees to {d3(bc[500]["train"])} at five hundred. '
                         f'The test AUC rises to {d3(F["boost_stage_best"])} at about {F["boost_stage_best_n"]} trees, then slowly falls to {d3(bc[500]["test"])}. After the peak, each new tree fits noise. This is why the number of trees is a hyperparameter to tune. Picking the best number from the test curve, as I just did, is for illustration only: choose it with cross-validation. '
                         'These numbers come from a NumPy copy of boosting that follows the same algorithm as scikit-learn. What would you do to pick the number of trees without using the test rows?')))

    # ------------------------------------------------------------------ 14 grid search
    vals = [[g[f'{md}|{ml}']['mean'] for ml in SF.GRID_LEAF] for md in SF.GRID_DEPTH]
    S.append(dict(kind='wide', title='Hyperparameter tuning: grid search scores every combination with 5-fold cross-validation',
                  visual=dict(kind='ds_i_grid', row_title='max_depth', col_title='min_samples_leaf', rows=['3', '6', 'none'], cols=[str(c) for c in SF.GRID_LEAF], values=vals,
                              best=(SF.GRID_DEPTH.index(gb['max_depth']), SF.GRID_LEAF.index(gb['min_leaf'])), folds=gb['folds'], fold_mean=gb['mean'], fold_sd=gb['sd']),
                  caption=f'9 combinations × 5 folds = 45 fits. The best cell, refitted, scores {d3(tu["test"])} on the test rows.',
                  notes=(f'Grid search is the standard way to tune hyperparameters. In scikit-learn it is GridSearchCV. Here max depth is three, six or no limit, and the minimum loans in a leaf is one, ten or thirty: nine combinations. '
                         f'Each is scored with five-fold cross-validation on the training rows only, so the test rows stay hidden: forty five fits. '
                         f'The best is {gdepth} with thirty loans in a leaf, a mean of {d3(gb["mean"])}, with a spread of {d3(gb["sd"])} between folds. {len(close)} cells are within 0.005 of it, nearly a tie. Thirty is the largest leaf size tried, so a real project would also try 50 and 100. The default forest scores {d3(F["grid_default_cv"])} in the same cross-validation. '
                         f'Refit the best, score it once on the test rows, and you get {d3(tu["test"])}. Why do we keep the test rows out of the search?')))

    # ------------------------------------------------------------------ 15 formula: logistic regression
    S.append(dict(kind='formula', title='Logistic regression models the log-odds of default as a weighted sum of the variables',
                  size=18,
                  formulas=[('Log-odds (logit)', r'$z = b_0 + b_1 x_1 + b_2 x_2 + \dots + b_{12} x_{12}$'), ('Chance of default (sigmoid)', r'$p = \frac{1}{1 + e^{-z}}$'),
                            ('One test loan', rf'$z = {ex["logodds"]:.2f} \quad p = {ex["p"]:.3f}$')],
                  symbols=[['b_0, b_1, ...', 'Intercept and coefficients, learned from the training rows', f'b for the ratio = {coef[ITI]:+.2f}'], ['x_1, ..., x_12', 'The 12 variables, each scaled to mean 0 and standard deviation 1 (the 12 columns of Session 14)', 'age, income, ...'],
                           ['x_12 ratio', 'instalment_to_income: loan x 1.15 / term in months / monthly income. The 1.15 is an illustrative assumption', f'median {C["instalment_to_income_median"]:.2f}'],
                           ['z and p', 'z: the log-odds, ln(p / (1 - p)). p: the chance of default', f'z {ex["logodds"]:.2f}, p {ex["p"]:.3f}']],
                  widths=[2.3, 6.4, 3.2],
                  notes=(f'Logistic regression is the simple model we will beat, or fail to beat, today. It adds up the variables, each multiplied by its coefficient, plus an intercept. That sum is the log-odds of default. The sigmoid function turns the log-odds into a chance between zero and one. '
                         f'Take one test loan, the one whose predicted chance is closest to the median. Its log-odds is {ex["logodds"]:.2f}, so the chance is one over one plus e to the power {-ex["logodds"]:.2f}, which is {ex["p"]:.3f}, about {ex["p"] * 100:.0f} in a hundred. '
                         f'The coefficients are learned from the training rows, after scaling. The test AUC is {L["test"]:.3f}. Session 15 shows {C["auc_27"]:.3f} for the same model with 15 more indicator columns. Why must the variables be on the same scale before we compare coefficients?')))

    # ------------------------------------------------------------------ 16 coefficients
    order = sorted(cols, key=lambda c: -abs(coef[c]))
    S.append(dict(kind='idea', title='Standardised coefficients: the instalment-to-income ratio and previous late payments raise the log-odds of default',
                  visual=dict(kind='ds_i_hbars', items=[(c, coef[c]) for c in order], signed=True, fmt='{:+.2f}', xlabel='change in log-odds per +1 standard deviation', pos_note='raises risk', neg_note='lowers risk', label_w=3.2),
                  lead='Sign gives the direction. Length gives the size.',
                  points=[f'instalment_to_income {coef[ITI]:+.2f}: odds of default x {E ** coef[ITI]:.1f} per standard deviation.', f'late payments {coef["previous_late_payments"]:+.2f}, group_loan {coef["group_loan"]:+.2f}.', 'Associations only.'],
                  notes=(f'This is the readable part of logistic regression. Each bar is a coefficient after scaling, so a bar shows the change in log-odds for a one standard deviation rise in that variable, with the others held fixed. Red bars raise the risk of default and dark bars lower it. '
                         f'The instalment-to-income ratio, the monthly instalment divided by monthly income with the illustrative 1.15 charge factor from Session 14, is the largest at plus {coef[ITI]:.2f}. Raising e to that power gives {E ** coef[ITI]:.1f}, so one standard deviation of the ratio multiplies the odds of default by about that factor. '
                         f'Late payments in the past raise the risk, and being in a group loan lowers it. These are associations in this table, and they do not prove causes. How would you explain the instalment-to-income bar to a credit committee?')))

    # ------------------------------------------------------------------ 17 permutation importance
    top6 = sorted(F['perm_forest'], key=lambda r: -r['mean'])
    S.append(dict(kind='idea', title='Permutation importance: shuffle one variable and see how far the test AUC falls',
                  visual=dict(kind='ds_i_hbars', items=[(r['col'], r['mean'], r['sd']) for r in top6[:8]], signed=False, fmt='{:.3f}', xlabel='drop in test AUC (gold line: spread over 10 repeats)', label_w=3.2),
                  lead='A variable the model relies on hurts the score when shuffled.',
                  points=['Shuffle one test column, rescore, repeat 10 times. Pass scoring="roc_auc", or the drop is in accuracy.', f'instalment_to_income: AUC falls {d3(pf[ITI]["mean"])}. loan_amount_ugx: {d3(pf["loan_amount_ugx"]["mean"])}.', 'age: about zero.'],
                  notes=(f'Permutation importance answers a question about a fitted model: which variables does it rely on? Take the test rows, shuffle the values of one variable so they no longer match the loans, and score the model again. If the AUC falls a lot, the model was relying on that variable. '
                         f'We repeat the shuffle ten times and show the spread as the gold line. For the tuned forest, shuffling the instalment-to-income ratio costs {d3(pf[ITI]["mean"])} of AUC, loan amount costs {d3(pf["loan_amount_ugx"]["mean"])}, and age costs about nothing. '
                         'Notice that the instalment-to-income ratio and the loan amount are the variables a credit officer would expect. Does that match what you saw in the logistic coefficients?')))

    # ------------------------------------------------------------------ 18 limits of importance
    S.append(dict(kind='compare', title='Permutation importance has limits, and you must state them',
                  left=dict(head='What it tells you', points=['Which variables this fitted model relies on, measured on test rows.']),
                  right=dict(head='What it cannot tell you', points=[f'Correlated variables share the credit. With a copy added, instalment_to_income fell from {d3(dup["before"])} to {d3(dup["after_orig"])}; the copy scored {d3(dup["after_copy"])}.',
                                                                     'It shows no cause.']),
                  verdict='Say: this model relies on the ratio. Avoid saying the ratio causes default.',
                  notes=(f'Permutation importance is useful and easy to over-read. It tells you which variables this fitted model relies on, measured on test rows. It cannot split credit between correlated variables. We tested that: we added a second copy of the instalment-to-income ratio. '
                         f'Its importance fell from {d3(dup["before"])} to {d3(dup["after_orig"])}, and the copy scored {d3(dup["after_copy"])}, because shuffling one copy leaves the other copy to carry the signal. The credit was split. '
                         'And a high importance never proves a cause. The sentence to use is: this model relies on the instalment-to-income ratio. Where in your own data do two variables carry the same information?')))

    # ------------------------------------------------------------------ 19 model selection
    S.append(dict(kind='idea', title='Model selection: the scores are close, so ship the simpler model (parsimony)',
                  visual=dict(kind='ds_i_models', rows=[dict(label='Logistic regression', note='12 coefficients', cv=cv_lr['mean'], sd=cv_lr['sd'], test=L['test']),
                                                        dict(label='Tuned random forest', note=f'100 trees, {gdepth}', cv=gb['mean'], sd=gb['sd'], test=tu['test']),
                                                        dict(label='Gradient boosting', note='100 trees, depth 3', cv=cv_b['mean'], sd=cv_b['sd'], test=b100['test']),
                                                        dict(label='Decision tree', note='depth 3, 8 leaves', cv=cv_t['mean'], sd=cv_t['sd'], test=t3['test'])], lo=0.66, hi=0.82, band=(0.72, 0.78, 'close enough to call a tie')),
                  lead='The top three scores differ by about 0.01, about as much as one fold differs from the next.',
                  points=[f'Cross-validated AUC: {d3(cv_lr["mean"])}, {d3(gb["mean"])}, {d3(cv_b["mean"])}.', f'Test AUC: {d3(L["test"])}, {d3(tu["test"])}, {d3(b100["test"])}.', 'Parsimony: prefer the simpler model.'],
                  notes=(f'Now we put four models side by side, all on the same loans. The black dot is the cross-validated AUC with one standard deviation either side, and the gold dot is the test AUC. '
                         f'Logistic regression scores {d3(cv_lr["mean"])} in cross-validation and {d3(L["test"])} on the test rows. The tuned forest scores {d3(gb["mean"])} and {d3(tu["test"])}, and boosting {d3(cv_b["mean"])} and {d3(b100["test"])}. '
                         f'The three differ by about one hundredth, and a single fold score moves by about one hundredth from one fold to the next, so we cannot say one of them is better. When scores are close, the rule is parsimony: ship the simpler model. '
                         'A list of twelve coefficients is easier to explain, check and maintain than a hundred trees. When would you accept a more complex model anyway?')))

    # ------------------------------------------------------------------ 20 decision
    S.append(dict(kind='decision', title='Decision: which model would you ship to a credit committee?', question='A credit committee asks which model to ship. What do you recommend, and what would change your mind?',
                  options=[dict(head='Logistic regression', text=f'Test AUC {d3(L["test"])}. Twelve readable coefficients. Easy to explain to the committee.', icon='check'),
                           dict(head='Tuned random forest', text=f'Test AUC {d3(tu["test"])}. Strong, but a hundred trees to explain and to monitor.', icon='chart'),
                           dict(head='Gradient boosting', text=f'Test AUC {d3(b100["test"])}. Needs the number of trees tuned with care.', icon='gear')],
                  record='Write your choice and one reason in your notes. We compare after the lab.',
                  notes=('Here is a decision to take as a group. A credit committee asks which model to ship. On the cross-validated and test scores, the three are close. Think about the committee: they must understand the model, a regulator or auditor may ask how it decides, and someone must maintain it. '
                         'My recommendation would be logistic regression, with the forest or boosting kept as a challenger, to be tested again if the data grows or the scores separate. '
                         'But I want to hear yours. Tell your neighbour your choice and one reason, then one thing that would change your mind.')))

    # ------------------------------------------------------------------ 21 use at work
    S.append(dict(kind='table', title='Where you will use this at work: compare models fairly before you recommend one',
                  headers=['Your job', 'The model question you meet', 'What today lets you do'],
                  rows=[['Credit analyst at a bank or SACCO, using scikit-learn', 'A vendor says a boosted model beats the scorecard.', 'Ask for cross-validated and test AUC, and the training-test gap, before you agree.'],
                        ['Data analyst on a mobile money fraud team', 'A forest flags thousands of transactions.', 'Tune the number of trees and depth with GridSearchCV, and keep logistic regression as the baseline.'],
                        ['Health records officer at a district office', 'Clinicians ask which factors drive a missed appointment.', 'Report coefficients and permutation importance, and say they show association only.'],
                        ['Team lead who reviews a model report', 'The report shows one training score.', 'Ask for the test score, the tuning method and a simple benchmark before the model is approved.']],
                  widths=[3.3, 4.2, 4.5], icons=['coin', 'phone', 'clinic', 'people'],
                  notes=('Where will you use this on Monday? Four examples. A credit analyst at a bank or a SACCO hears that a boosted model beats the scorecard. Today lets you ask for cross-validated and test AUC and the gap between training and test before you agree. '
                         'A data analyst on a mobile money fraud team can tune the number of trees and the depth with GridSearchCV and keep logistic regression as the baseline. '
                         'A health records officer can report coefficients and permutation importance, and say clearly that they show association only. And a team lead reviewing a model report can ask for the test score, the tuning method and a simple benchmark. '
                         'My understanding is that libraries such as XGBoost and LightGBM are common gradient boosting tools in industry, and the ideas you learned today carry over to them. Which one is closest to your job?')))

    # ------------------------------------------------------------------ 22 bridge
    S.append(dict(kind='code', title='Read the recipe before the lab: fit, score twice, then tune',
                  code='model = RandomForestClassifier(random_state=42)\nmodel.fit(X_train, y_train)\np_test = model.predict_proba(X_test)[:, 1]\nauc_test = roc_auc_score(y_test, p_test)\ngrid = {"max_depth": [3, 6, None]}\nsearch = GridSearchCV(model, grid, cv=5,\n                      scoring="roc_auc")\nsearch.fit(X_train, y_train)',
                  reads=['Lines 1 and 2 fit a forest (100 trees by default).', 'Line 3: the predicted chance of default for each test loan.', 'Line 4 scores it. Score the training rows too, to see the gap.',
                         'The last lines try each max_depth with 5-fold cross-validation.', 'search.best_params_ holds the winner.'],
                  notes=('Before the lab, read the recipe. Lines one and two create a random forest, a hundred trees by default, and fit it on the training rows. Lines three and four get the predicted chance of default for each test loan and score it with AUC. Do the same on the training rows, and the difference between the two scores is the generalisation gap. '
                         'Lines five to seven hand the forest to GridSearchCV with a dictionary of settings to try, and ask for five-fold cross-validation scored by AUC. '
                         'After fitting, search dot best params underscore tells you the winning combination. In the lab you will run this and then shuffle the variables with permutation importance. Which line creates the gap you want to look at?')))

    # ------------------------------------------------------------------ 23 divider
    S.append(dict(kind='divider', title='Part 2: the Python lab', lead='Close the slides. Open the notebook.', section='Lab',
                  notes=('That is the end of the ideas. Everything you need is on the slides you have just seen, and the notebook repeats each step in plain words. '
                         'Open Google Colab and open the notebook for Session 17. Run the first cell to load the data, then the second cell to load the check helper. '
                         'In every step, predict first, run second, read third, and change one thing last. If you are stuck for more than three minutes, call me.')))

    # ------------------------------------------------------------------ 24 lab map
    S.append(dict(kind='steps', title='The lab has six parts, and you keep a comparison table and a decision memo',
                  steps=[dict(head='1 Prepare', text='Load, prepare, split 6,000 and 2,000', icon='folder'), dict(head='2 Baseline', text='Scaled logistic regression', icon='calculator'), dict(head='3 Trees', text='Depth against train and test AUC', icon='chart'),
                         dict(head='4 Ensembles', text='Forest and boosting', icon='people'), dict(head='5 Tune', text='GridSearchCV, importance', icon='gear'), dict(head='6 Decide', text='Table and memo', icon='notebook')], highlight=None,
                  caption='Eight tasks in 45 minutes. In each task, predict first, run second, read what the output tells you, then change one thing.',
                  notes=('Here is the map of the lab. Step one, prepare the loans and split them. Step two, fit the scaled logistic regression as the baseline and note its coefficients. Step three, grow trees of different depths and watch the gap open. '
                         'Step four, fit a random forest and a gradient boosting model, and see when boosting peaks. Step five, tune the forest with GridSearchCV and compute permutation importance. '
                         'Step six, build the comparison table, save it, and write your decision memo. In every task, predict first, run second, read, then change one thing. Please do not skip the predictions.')))

    # ------------------------------------------------------------------ 25 check numbers
    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Loans kept, defaults, default share', f'{n(F["rows"])}, {n(F["defaults"])}, {F["default_rate"] * 100:.2f} percent'], ['Training rows and test rows (defaults in each)', f'{n(F["n_train"])} ({n(C["train_defaults"])}) and {n(F["n_test"])} ({n(C["test_defaults"])})'],
                        ['Logistic regression: train and test AUC', f'{d3(L["train"])} and {d3(L["test"])}'], ['Tree: test AUC at depth 3. Train AUC, no limit', f'about {d3(t3["test"])}. {tnone["train"]:.3f}'],
                        ['Forest, 100 trees: train and test AUC', f'about {f100["train"]:.2f} and {d2(f100["test"])} (within 0.03)'],
                        ['Boosting, 100 trees: train and test AUC', f'{d3(b100["train"])} and {d3(b100["test"])}'], ['Grid search: best settings, mean AUC', f'{len(close)} cells tie within 0.005; mean about {d3(gb["mean"])}'],
                        ['Top permutation importance', f'instalment_to_income, about {d3(pf[ITI]["mean"])}']],
                  widths=[6.4, 5.6], icons=['folder', 'grid', 'calculator', 'chart', 'people', 'gear', 'key', 'magnifier'], note='The median income is computed on all 8,000 loans before the split, on purpose (simple, tiny leak). Session 20 shows the leak-free way. Forests use random numbers.',
                  notes=('Use this table as a self-check. The logistic regression and the boosting numbers should agree to about two decimals. The tree is close. Your split should give six thousand and two thousand rows, with two hundred and fifty one defaults in the test rows, and X test index should start 4299, 1151, 2351. The median income is computed on all eight thousand loans before the split, on purpose, because it is simple and the leak is small. Session 20 shows the leak-free way. '
                         'The forest uses random numbers, and the grid search depends on them, so accept a small difference, within the range shown, and do not chase the third decimal. '
                         'If a score is far off, stop and call me, because later tasks use the earlier ones. Find out why it is different. What is the first thing you check if your test AUC is 0.99?')))

    # ------------------------------------------------------------------ 26 error cards
    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[['Forest training AUC about 1.00, test AUC about 0.72', 'That is correct. The forest memorises its training rows.', 'Write it down as the generalisation gap. Leave it as it is.'],
                        ['Test AUC about 0.99', 'collection_calls leaked back into X.', 'Build X from the 12 listed columns only.'],
                        ['ValueError: could not convert string to float', 'X still holds text columns such as district.', 'Select the 12 numeric columns by name.'],
                        ['GridSearchCV runs for minutes', 'It fits 45 forests.', 'Add n_jobs=-1 and run it once. Skip rerunning the cell.'],
                        ['Scores differ in the third decimal', 'Random numbers and library versions.', 'Set random_state=42. Accept the ranges in the check table.']],
                  widths=[3.7, 4.2, 4.1], icons=['check', 'cross', 'cross', 'clock', 'calculator'],
                  notes=('Five situations you may meet. A forest with a training AUC near one and a test AUC near zero point seven two is correct, so leave it. That gap is what we came to see. '
                         'A test AUC near zero point nine nine means the leaking column collection calls has come back into X. A value error about a string means a text column such as district is still in X. '
                         'The grid search can take a few minutes because it fits forty five forests, so add n jobs minus one and run it once. And scores that differ in the third decimal come from random numbers, so set the random state and accept the ranges. Which of these would you have guessed?')))

    # ------------------------------------------------------------------ 27 exit check
    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[[f'A model scores AUC {tnone["train"]:.2f} on the training rows and {d2(tnone["test"])} on the test rows. What is happening, and what is the gap called?', 'Overfitting: it memorised the training rows. The difference is the generalisation gap.'],
                        ['How does gradient boosting differ from a random forest?', 'A forest averages deep trees grown side by side on bootstrap samples. Boosting adds shallow trees in a sequence, each fitting the residual errors so far.'],
                        [f'Logistic regression scores {d3(L["test"])} and a forest {d3(tu["test"])}. Which do you ship?', 'The logistic regression: the scores are close, so choose the simpler model (parsimony), and say what would change your mind.']],
                  widths=[5.6, 6.4], icons=['chart', 'people', 'check'],
                  notes=(f'Last, the exit check. Three questions. Write your answers in your notes before you look at mine. One, a model scores {tnone["train"]:.2f} on the training rows and about {d2(tnone["test"])} on the test rows. What is happening, and what is the gap called? '
                         f'Two, how does gradient boosting differ from a random forest? Three, logistic regression scores {d3(L["test"])} and a forest {d3(tu["test"])}. Which do you ship? '
                         'The short answers are on the slide. If you got all three, you are ready for Session 18. If one surprised you, look at that part of your notebook again tonight.')))

    # ------------------------------------------------------------------ facilitator
    sess['facilitator'] = dict(
        prep=['Open the deck and the notebook for Session 17 in Colab before anyone arrives, and run the whole notebook once on the free Colab runtime to confirm the check numbers. The slide numbers were computed in NumPy replicas of the algorithms, because scikit-learn is not installed in the build environment. Before the course starts, run the solution notebook on real scikit-learn in Colab and compare every number with the slides.',
              'Upload data.zip to your own Colab session first, so you can show where the file goes.', 'Write the check table (slide 25) on the board before the lab.', 'Concepts run with laptops closed. Ask learners to open Colab only after the Part 2 divider.',
              'GridSearchCV fits 45 forests. Test its run time on the free Colab runtime and tell learners to run it once.'],
        misconceptions=[('A high training score means a good model', f'Only the score on rows the model has not seen counts. A deep tree gets {tnone["train"]:.2f} training AUC and {d2(tnone["test"])} test AUC.'),
                        ('More trees always overfit a forest', f'Adding trees to a random forest flattens the test AUC (about {d2(f100["test"])} from 50 trees on). Boosting is the one that overfits with too many trees.'),
                        ('Tuning on the test rows is fine if you only do it once', 'Every choice made by looking at the test score uses it up. Tune with cross-validation on the training rows and score the test rows once.'),
                        ('A high permutation importance means the variable causes default', 'It means this model relies on the variable. Correlated variables share the credit, and no causal claim follows.'),
                        ('The more complex model is always the better choice', f'Here logistic regression ({d3(L["test"])}) is as good as the forest ({d3(tu["test"])}) and boosting ({d3(b100["test"])}). When scores are close, ship the simpler model.')],
        probes=[('What is a hyperparameter? Give one for a tree and one for boosting.', 'A setting chosen before training. max_depth for a tree, learning_rate or n_estimators for boosting.'),
                ('What does bagging stand for, and what does it do to variance?', 'Bootstrap aggregation. Averaging many trees lowers variance.'),
                ('What does each new tree in gradient boosting fit?', 'The residual errors of the ensemble so far.'),
                ('Why do we score a forest on its training rows and on its test rows?', 'The gap between the two is the generalisation gap, the signal of overfitting.'),
                ('How many model fits does a 3 by 3 grid with 5 folds need?', '45, plus one refit of the best on all the training rows.'),
                ('Why did adding a copy of instalment_to_income lower its importance?', 'Shuffling one copy leaves the other to carry the signal, so the credit is split.'),
                ('When do you ship the simpler model?', 'When the scores are close, inside the spread between folds, and you can explain it more easily.')],
        lab_steps=[('Task 1: prepare and split', f'{n(F["rows"])} loans (the {F["bad_ages"]} impossible ages are replaced by the median age, no row is deleted), {n(F["defaults"])} defaults, 12 columns, {n(F["n_train"])} training rows and {n(F["n_test"])} test rows, {n(C["test_defaults"])} defaults in the test rows. Watch for collection_calls creeping in.'),
                   ('Task 2: baseline', f'Training {d3(L["train"])}, test {d3(L["test"])}. The instalment-to-income ratio has the largest coefficient, {coef[ITI]:+.2f}.'),
                   ('Task 3: tree depth', f'Depth 3 test about {d3(t3["test"])}. No limit: training 1.000, test about {d3(tnone["test"])}. The gap opens after depth 3 or 4. A tree with no limit is {tnone["real_depth"]} questions deep.'),
                   ('Task 4: forest', f'Training about {f100["train"]:.2f}, test about {d2(f100["test"])}. Learners may be upset that training is 1.00. That is the point.'),
                   ('Task 5: boosting', f'100 trees: training {d3(b100["train"])}, test {d3(b100["test"])}. The staged test curve peaks near {F["boost_stage_best_n"]} trees at {d3(F["boost_stage_best"])}.'),
                   ('Task 6: GridSearchCV', f'Best max_depth {gb["max_depth"]}, min_samples_leaf {gb["min_leaf"]}, mean AUC about {d3(gb["mean"])}. Refit test AUC about {d3(tu["test"])}. Another cell may win a tie in a different run.'),
                   ('Task 7: permutation importance', f'instalment_to_income first, drop about {d3(pf[ITI]["mean"])}. Variables such as age and has_mobile_money are about zero.'),
                   ('Task 8: results and memo', 'Logistic regression is as good as the rest. A good memo names the model, quotes two numbers and says what would change the decision.')],
        rescue=['If the concepts run over, shorten the logistic regression coefficient slide (slide 16) and the decision slide; the lab covers both.', 'If only 30 minutes of lab remain, do tasks 1, 2, 4, 6 and 8 and set the rest as homework.',
                'If GridSearchCV is too slow on a learner laptop, reduce the grid to max_depth [3, 6] and min_samples_leaf [10, 30] and say so in the memo.', 'If a learner has no laptop, pair them with a neighbour: one types, one predicts aloud.'],
        after=['Share the deck and the solution notebook again for learners who were absent.', 'Ask each learner to save the comparison table and bring one question about overfitting to Session 18.', 'Note any question you could not answer and open the next session with it.'],
        lab_answer_key=[['Task 2 PREDICT: will the logistic regression score higher on the training rows or the test rows?', f'The training rows, slightly: {d3(L["train"])} against {d3(L["test"])}. The gap is small because the model is simple.'],
                        ['Task 3 PREDICT: what is the training AUC of a tree with no depth limit?', 'About 1.000. It memorises every training loan.'],
                        ['Task 3 READ: at which depth does the test AUC peak, and what happens after?', f'Depth 3 ({d3(t3["test"])}; depth 4 is almost the same). After that, training AUC rises and test AUC falls.'],
                        ['Task 4 READ: how big is the forest generalisation gap?', f'About {f100["train"] - f100["test"]:.2f}: training near 1.00 against test near {d2(f100["test"])}.'],
                        ['Task 5 CHANGE: use 500 trees. What happens to the training and test AUC?', f'Training rises to {d3(bc[500]["train"])} and test falls to {d3(bc[500]["test"])}. Too many trees overfit.'],
                        ['Task 6 READ: is the best cell clearly better than the others?', f'No. {len(close)} cells score within 0.005 of the best, about as close as one fold is to the next ({d3(gb["sd"])}). The best cell is also at the edge of the grid.'],
                        ['Task 7 CHANGE: add a copy of instalment_to_income to X. What happens to its importance?', f'It splits: about {d3(dup["after_orig"])} and {d3(dup["after_copy"])} instead of {d3(dup["before"])}.'],
                        ['Task 8 READ: which model do you ship?', 'Logistic regression, with a reason about close scores and readability, and a statement of what would change the decision.']])
    return sess
