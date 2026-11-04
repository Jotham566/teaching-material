"""Class 3 (Week 10): can I trust this model? Overfitting, cross-validation, leakage and reproducibility, then the lab.

Every number on a slide comes from `refs(f)` below, which re-computes it with the NumPy reference module (trees from sk_tree_replica, folds re-implemented with NumPy).
The lab notebook (lab3.py) prints the same numbers with the scikit-learn stand-in and its CHECK compares them with `refs`.
"""
import numpy as np
import pandas as pd

import common as C

R = C.R
FEATS = R.FEATURES
SEEDS = (1, 17, 99)
TREE_SEED = 17
TOL = 1.05        # a depth is within the tolerance of the best one when its validation MAE is within 5 percent of the lowest
_CACHE = {}


# ------------------------------------------------------------------ reference calculations
def _fit_predict(tr_df, te_df, depth, extra=(), fill_df=None, seed=TREE_SEED):
    """Median-fill the inputs (medians from fill_df, default the training rows), grow a tree, predict the other rows."""
    cols = FEATS + list(extra)
    med = (fill_df if fill_df is not None else tr_df)[cols].median()
    a, b = tr_df[cols].fillna(med), te_df[cols].fillna(med)
    t = R.tree_reg_fit(a.to_numpy(), tr_df.target.to_numpy(), depth, seed)
    return R.tree_predict(t, b.to_numpy())


def kfold_indices(n, k, shuffle=False, seed=None):
    """Same folds as scikit-learn's KFold: the first n % k folds get one extra row."""
    idx = np.arange(n)
    if shuffle:
        np.random.RandomState(seed).shuffle(idx)
    sizes = np.full(k, n // k)
    sizes[:n % k] += 1
    cur, out = 0, []
    for sz in sizes:
        out.append((np.r_[idx[:cur], idx[cur + sz:]], idx[cur:cur + sz]))
        cur += sz
    return out


def pick_depth(curve):
    lowest = min(v for _, _, v in curve)
    return min(d for d, _, v in curve if v <= lowest * TOL)


def count_leaves(t):
    return 1 if t[0] == 'leaf' else count_leaves(t[3]) + count_leaves(t[4])


def refs(f):
    code = f['code']
    if code in _CACHE:
        return _CACHE[code]
    b = f['b']
    tr = f['tr'].reset_index(drop=True)
    va = f['va'].reset_index(drop=True)
    out = {}
    curve = b['overfit_curve']
    out['curve'] = curve
    out['best'] = pick_depth(curve)
    out['lowest'] = min(v for _, _, v in curve)
    out['leaves'] = {d: count_leaves(R.tree_reg_fit(f['trf'].to_numpy(), tr.target.to_numpy(), d)) for d in range(1, 11)}
    out['line_mae'] = b['reg']['linear']['mae']
    out['tree4_valid'] = b['reg']['tree']['mae']
    # plain 5-fold cross-validation on the training rows (depth-4 tree, imputer fitted inside each fold)
    sc, sizes = [], []
    for a, t in kfold_indices(len(tr), 5):
        sc.append(R.mae(tr.target.iloc[t], _fit_predict(tr.iloc[a], tr.iloc[t], 4)))
        sizes.append((len(a), len(t)))
    out['cv5'] = dict(scores=sc, mean=float(np.mean(sc)), std=float(np.std(sc)), lo=min(sc), hi=max(sc), sizes=sizes)
    # GroupKFold: each training group held out once
    gs = {}
    for g in sorted(tr.equipment_id.unique()):
        a, t = tr[tr.equipment_id != g], tr[tr.equipment_id == g]
        gs[g] = (R.mae(t.target, _fit_predict(a, t, 4)), len(t))
    gv = [v[0] for v in gs.values()]
    out['grp'] = dict(scores={g: v[0] for g, v in gs.items()}, sizes={g: v[1] for g, v in gs.items()}, mean=float(np.mean(gv)), std=float(np.std(gv)), lo=min(gv), hi=max(gv))
    assert out['tree4_valid'] > out['grp']['mean'], 'slide claim: the single E5 split is harder than the average group'
    assert out['line_mae'] < min(v for _, _, v in curve), 'slide claim: the linear regression model beats every tree depth'
    # leaks
    allr = pd.concat([tr, va])
    honest = R.mae(va.target, _fit_predict(tr, va, 10))
    out['leak'] = dict(honest=b['leak_demo']['honest'], leaky=b['leak_demo']['leaky'])
    assert abs(honest - out['leak']['honest']) < 1e-9
    out['fill'] = dict(train=float(tr[FEATS].median()['ambient_c']), allrows=float(allr[FEATS].median()['ambient_c']),
                       mae_all=R.mae(va.target, _fit_predict(tr, va, 10, fill_df=allr)), mae_train=honest)
    tr2, va2 = tr.copy(), va.copy()
    tr2['target_rounded'] = tr2.target.round()
    va2['target_rounded'] = va2.target.round()
    out['disguise'] = R.mae(va.target, _fit_predict(tr2, va2, 4, extra=['target_rounded']))
    out['disguise_rows'] = [(float(r.load_pct), float(r.ambient_c), int(round(r.target)), float(r.target)) for r in f['trf'].assign(target=tr.target.to_numpy()).head(3).itertuples()]
    # seeds
    out['seed_tree'] = {}
    out['seed_cv'] = {}
    for sd in SEEDS:
        out['seed_tree'][sd] = R.mae(va.target, _fit_predict(tr, va, 10, seed=sd))
        out['seed_cv'][sd] = float(np.mean([R.mae(tr.target.iloc[t], _fit_predict(tr.iloc[a], tr.iloc[t], 4)) for a, t in kfold_indices(len(tr), 5, True, sd)]))
    out['n_rows'] = len(f['raw'])
    # the simplest-model-within-a-tolerance rule, worked
    lowest = out['lowest']
    out['tie'] = dict(vmin=lowest, limit=lowest * TOL, depth_low=min(d for d, _, v in curve if v == lowest), passing=[d for d, _, v in curve if v <= lowest * TOL])
    assert min(out['tie']['passing']) == out['best']
    # the real five scores, worked by hand (distance from the average and its square)
    m5 = out['cv5']['mean']
    out['cv5']['dist'] = [x - m5 for x in sc]
    out['cv5']['sq'] = [(x - m5) ** 2 for x in sc]
    out['cv5']['msq'] = float(np.mean(out['cv5']['sq']))
    assert abs(np.sqrt(out['cv5']['msq']) - out['cv5']['std']) < 1e-9
    assert out['tree4_valid'] > out['cv5']['mean'], 'slide claim: the single E5 split is harder than the plain 5-fold average'
    # scaler and imputer numbers for the pipeline formula (training rows only)
    out['scale'] = dict(mu=list(b['scaler']['mu']), sd=list(b['scaler']['sd']), row=b['scaling_rows'][0])
    _CACHE[code] = out
    return out


# ------------------------------------------------------------------ the class
def build(code):
    f = C.facts(code)
    b, unit, short, thing = f['b'], f['unit'], f['short'], f['thing']
    N = refs(f)
    n_raw, n_clean, n_tr, n_va, n_te = N['n_rows'], b['n_clean'], b['n_tr'], b['n_va'], b['n_te']
    curve, best = N['curve'], N['best']
    cv5, grp = N['cv5'], N['grp']
    tr10, va10 = curve[-1][1], curve[-1][2]
    cur = {d: (t, v) for d, t, v in curve}
    va4 = N['tree4_valid']
    seeds = SEEDS
    d2 = lambda v: f'{v:.2f}'
    um = unit.replace(' ', r'\ ')                         # the unit inside mathtext
    tie = N['tie']
    th = b['thresholds']
    t3, t5, t7 = th
    always_pct = int(round(b['always_no_acc'] * 100))
    gcodes = list(grp['scores'])
    sc_ = N['scale']
    row1 = sc_['row']

    stories = {'CML3112': ['A model is built from data on four buildings and then used on a fifth building.', 'The size of the cooling plant is chosen from the model’s prediction.',
                           'If the prediction is wrong, the building is too hot or the plant is too big.'],
               'CML3113': ['A model is built from data on four crushers and then used on a fifth crusher.', 'The power plan for the new pit is chosen from the model’s prediction.',
                           'If the prediction is wrong, the energy bill holds a surprise.'],
               'CML3111': ['A model is built from data on four motors and then used on a fifth motor at another site.', 'A winding temperature warning is based on the model’s prediction.',
                           'If the prediction is wrong, a winding burns or a motor stops when it did not need to.']}[code]

    clock = [(10, 'Recall from Class 2, and why trust matters'), (40, 'Concepts, part 1: overfitting, validation curve, cross-validation'), (30, 'Concepts, part 2: data leakage, random seed, pipeline'), (15, 'Break'),
             (75, 'Lab: validation curve, cross-validation, leakage, seeds'), (10, 'Close and how this class counts')]
    plan_note = ('We have three hours. The first seventy minutes are concepts only, with no laptop, so you can listen and ask. Then a break. '
                 'Then the lab, about an hour and a quarter, where you run everything on your own data. The ideas come first and the code comes second.')

    recall = [('Why is a majority-class baseline (a model that always predicts no) a poor model, even when its accuracy is about ' + f'{always_pct} percent?', 'It finds none of the real positive cases, so its recall is 0. Accuracy hides that.'),
              ('In a confusion matrix, what is a false negative (FN) and what is a false positive (FP)?', 'False negative: the model said no (negative) and the truth was yes (positive). False positive: the model said yes and the truth was no.'),
              ('What happened to recall and false positives when we lowered the decision threshold from 0.5 to 0.3?', (f'Recall rose from {d2(t5["recall"])} to {d2(t3["recall"])}. False positives stayed at {t3["fp"]}.' if t5['fp'] == t3['fp'] else f'Recall rose from {d2(t5["recall"])} to {d2(t3["recall"])}. False positives went from {t5["fp"]} to {t3["fp"]}.'))]

    s = dict(
        code=code, cohort_name=f['name'], num=3, week=10, when=f['dates'][3] + ', ' + f['slot'], short_title='Can I trust this model',
        title='Can I trust this model? Overfitting, cross-validation and leakage',
        question=f'How do we know a model that predicts {short} will still work on a {thing} it has never seen?',
        outcome_head='By the end of today you can',
        outcomes=['Explain underfitting, a good fit and overfitting (the bias-variance trade-off), and choose max_depth with a validation curve',
                  'Work out training error, validation error, the generalisation gap, and a cross-validation mean and standard deviation, by hand',
                  'Score a model with K-fold and GroupKFold cross-validation, and report the mean with its standard deviation',
                  'Name three kinds of data leakage and use a checklist that blocks them'],
        outcome_icons=['chart', 'calculator', 'grid', 'shield'],
        outcome_note=('Here is what you can do by the end of today. You can explain underfitting, a good fit and overfitting, the bias-variance trade-off, and you can choose max_depth by looking at a validation curve. '
                      'You can work out the training error, the validation error, the generalisation gap, and the mean and standard deviation of cross-validation scores, by hand. You can score a model with K-fold and GroupKFold. '
                      'And you can name three kinds of data leakage and keep a checklist that blocks them. Nothing is submitted today. At the end I explain how the class counts.'),
        clock=clock, plan_title='Your three hours: ideas first, then the lab', plan_note=plan_note,
        plan_caption='Concepts first, with no laptops. Then the lab, with the notebook open.',
        recall_from='Class 2',
        recall=recall,
        words=[('Overfitting', 'The model fits the noise in the training set (it nearly memorises it) and does worse on new rows. Underfitting is the opposite: too simple to learn the pattern.'),
               ('Cross-validation', 'Scoring a model K times. The rows are cut into K parts called folds. Each fold takes one turn as the validation fold (held-out fold).'),
               ('Data leakage', 'Information from outside the training set reaches the model while it is trained, so the score looks better than it really is.'),
               ('Bias-variance trade-off', 'Too simple a model misses the pattern (high bias, underfitting). Too flexible a model chases noise (high variance, overfitting).'),
               ('Random seed', 'A fixed number (random_state in scikit-learn) that makes a random choice repeat exactly.')],
        word_icons=['cross', 'grid', 'key', 'chart', 'clock'],
        words_note=('Five words for today. Overfitting is when a model fits the noise in its training set and does worse on new rows. Underfitting is the opposite: too simple to learn the pattern. Cross-validation means scoring a model K times. The rows are cut into K parts called folds, and each fold takes one turn as the validation fold, which some books call the held-out fold. '
                    'Data leakage is information from outside the training set reaching the model, so the score looks better than it is. The bias-variance trade-off is the industry name for the balance between too simple and too flexible. '
                    'And a random seed, set with random_state, makes a random choice repeat exactly. We use all five before the end.'),
        keep='Your saved lab notebook, the chosen max_depth, and the five-question checklist for trusting a score.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Notebook', value='Restart, run all, save'), dict(label='max_depth', value='Chosen on the validation set'),
                                                              dict(label='Checklist', value='Five questions'), dict(label='Next class', value='Features and models')]),
        keep_title='Save the notebook and keep the checklist',
        next='Class 4: features and choosing a model, plus the project brief.', next_label='Next class',
        keep_note=('Before you go, restart the notebook, run all cells from the top and save it. Keep the max_depth you chose and the checklist, because you will use both again. '
                   'Next class we look at which columns the model should use and how to choose between models, and I explain how the project sitting works. If anything today was unclear, write the question down and bring it.'),
        cover_note=(f'Welcome back. In the first two classes you built models that predict {short} and models that answer yes or no. Today we ask the question an engineer must always ask: can I trust this? '
                    'A score that looks good is not enough. We learn how a model fools us, and how to test it so that it cannot.'),
        friday_note='the same deck and the same clock as the Tuesday cohort. There is no separate recap version for this class.',
        slides=[])
    S = s['slides']

    # ------------------------------------------------------------------ recall answers
    S.append(dict(kind='table', title='Answers to the three questions from Class 2',
                  headers=['Question', 'Short answer'], rows=[[q, a] for q, a in recall], widths=[5.4, 6.4], icons=['bars', 'grid', 'switch'],
                  notes=('Here are the answers, so you can check yourself and use this slide to revise. A majority-class baseline, a model that always predicts no, can have a high accuracy, but it finds no real positive case, so its recall is zero. '
                         'A false negative is a no when the truth was yes, and a false positive is a yes when the truth was no. '
                         f'Lowering the decision threshold from 0.5 to 0.3 moved recall from {d2(t5["recall"])} to {d2(t3["recall"])} on the validation rows. '
                         'Today we ask a different question about the same models: can we trust a score at all?')))

    S.append(dict(kind='list', title='A model that looks good on paper can fail on a new machine or site', items=stories, icons=['folder', 'gear', 'bell'],
                  notes=(f'Start with a story from your own field. {stories[0]} {stories[1]} {stories[2]} '
                         'In the office the model looked excellent, so everybody trusted it. The trouble is that the office score came from rows the model had already been trained on, or from a test that was too easy. '
                         'Today is about checking a model the way real life will check it. Have you ever trusted a number from a machine or a spreadsheet and then been surprised?')))

    S.append(dict(kind='idea', title='A model must do well on rows it has never seen',
                  visual=dict(kind='versus', left=dict(head='Training set', big=f'{tr10:.2f}', unit=f'{unit} error', icon='book'),
                              right=dict(head='Validation set', big=f'{va10:.2f}', unit=f'{unit} error', icon='question'), middle='Same tree, max_depth 10'),
                  lead='Generalisation means doing well on held-out data: rows the model has never seen.',
                  points=['The tree was trained on the training set, so its error there is almost zero.', 'The validation set was held out. On it the prediction error is far larger. The difference is the generalisation gap.'],
                  notes=(f'Here is one tree, grown ten questions deep, scored two ways. The training set is the rows it was trained on, and there its error is {tr10:.2f} {unit}, which is almost perfect. '
                         f'The validation set was held out, and there its error is {va10:.2f} {unit}. The difference between the two is called the generalisation gap. '
                         'Same model, same data, two very different stories. Doing well on held-out rows it has never seen is called generalisation, and it is the only thing we really want. '
                         'A score on rows the model was trained on tells us about its memory, and a score on new rows tells us about its skill. Which score would you show a client?')))

    S.append(dict(kind='idea', title='Underfitting, a good fit and overfitting look like three students',
                  visual=dict(kind='student', cards=[dict(head='Underfitting', text='Read nothing: high bias.', icon='person', practice='40%', new='40%'),
                                                      dict(head='Good fit', text='Learned the ideas.', icon='book', practice='85%', new='80%'),
                                                      dict(head='Overfitting', text='Memorised answers: high variance.', icon='notebook', practice='100%', new='45%', hl=True)]),
                  lead='The marks in the picture are illustrative (made up). Each student stands for one kind of model.',
                  points=['Practice paper = training set. New paper = held-out rows.', 'Bias-variance trade-off: too simple a model misses the pattern, too flexible a model chases noise.'],
                  notes=('Think of three students. The first read nothing, so the practice paper and the new paper both go badly. That is underfitting: a model too simple to learn the pattern, which the industry calls high bias. '
                         'The second understood the ideas, so the marks are good on both papers. That is a good fit. The third memorised last year’s answers. Perfect on the practice paper and poor on the new paper. '
                         'That is overfitting: the model fits the noise, which the industry calls high variance. Balancing the two is the bias-variance trade-off. The practice paper stands for the training set, the new paper for held-out rows, and the marks are made up. '
                         'Can you think of someone who passed by memory and then struggled on the job?')))

    lin = b['reg']['linear']
    S.append(dict(kind='formula', title='Reminder from Class 1: MAE and RMSE measure the prediction error',
                  size=20,
                  formulas=[('MAE: mean absolute error', r'$\mathrm{MAE} = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|$'),
                            ('MSE and RMSE', r'$\mathrm{MSE} = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2 \quad \mathrm{RMSE} = \sqrt{\mathrm{MSE}}$')],
                  symbols=[['MAE', 'The mean size of the error. The bars drop any minus sign', f'Class 1 model: {d2(lin["mae"])} {unit}'],
                           ['MSE, RMSE', 'MSE: mean of the squared errors. RMSE: its square root, in the target unit', f'Class 1 model: RMSE {d2(lin["rmse"])} {unit}'],
                           ['n, y, ŷ', 'n rows scored; y is the actual target of row i; ŷ (y-hat) is the prediction', f'{n_va} validation rows; {short} in {unit}']],
                  widths=[1.9, 6.0, 4.0],
                  note='Illustrative example (made up): errors of 1, 2 and 3 give MAE = 2, MSE = 4.67 and RMSE = 2.16.',
                  notes=('Before we use the word MAE all class, here is a reminder from Class 1. For every row, take the actual target and the prediction, and look at the size of the prediction error. The MAE is the mean of those errors, and the bars mean we drop any minus sign. '
                         'The RMSE squares each error first, averages, and then takes the square root, so one big error counts for more. '
                         f'Our linear regression model from Class 1 had an MAE of {d2(lin["mae"])} {unit} and an RMSE of {d2(lin["rmse"])} {unit} on the validation rows. Today we mostly use the MAE. Why would one very large error matter more to an engineer?')))

    S.append(dict(kind='idea', title='The validation curve: as max_depth grows, training error keeps falling but validation error stops',
                  visual=dict(kind='depthcurve', curve=[[d, t, v] for d, t, v in curve], best=best, unit=unit),
                  lead='A validation curve plots both errors against model complexity, here max_depth (most questions a row is asked).',
                  points=[f'Each dot is one tree. Black: training error, falling to {tr10:.2f}. Red: validation error. Between them: the generalisation gap.', 'The gold band is the max_depth we choose.'],
                  notes=(f'This is a validation curve from our data. It plots error against model complexity. Each point is a tree with a different max_depth, the largest number of questions a row can be asked on the way down the tree. '
                         f'The black line is the error on the training rows, and it falls all the way to {tr10:.2f}. '
                         f'The red line is the validation error. It falls at first and then stops improving, and at depth 10 it sits at {va10:.2f}. The distance between the lines is the generalisation gap. The gold band is the depth we choose, depth {best}. '
                         'At the end of the Class 1 lab you tried depths 1, 2 and 8. This curve is what you were seeing. Where does the generalisation gap start to grow?')))

    S.append(dict(kind='formula', title='Training error, validation error and the generalisation gap are short formulas',
                  size=20,
                  formulas=[('Training error', r'$\mathrm{MAE}_{\mathrm{train}} = \frac{1}{n_{tr}} \sum_{i \in \mathrm{train}} |y_i - \hat{y}_i|$'),
                            ('Validation error', r'$\mathrm{MAE}_{\mathrm{val}} = \frac{1}{n_{va}} \sum_{i \in \mathrm{val}} |y_i - \hat{y}_i|$')],
                  symbols=[['MAE', 'Mean absolute error: the average size of the prediction error. The small label train or val says which rows', f'Depth 10: {d2(tr10)} and {d2(va10)} {unit}'],
                           ['n', 'How many rows. The small label tr means training and va means validation', f'{n_tr} and {n_va} rows'],
                           ['i', 'A row number. The sum adds up the rows of that group', 'Row 1, row 2, and so on'],
                           ['y, ŷ', 'The real target of row i, and the model’s prediction for it. The bars | | drop any minus sign', f'{short} and the tree’s answer, in {unit}']],
                  widths=[2.3, 5.6, 4.0],
                  notes=('Class 1 gave you the MAE. Here it is again, written for two groups of rows. The training error adds up the size of the prediction error on every training row, then divides by the number of training rows. '
                         'The validation error does the same on the validation rows. The bars mean the size of the error, so a plus or a minus makes no difference. '
                         f'In our data at depth 10 the training error is {d2(tr10)} {unit} and the validation error is {d2(va10)} {unit}. Which rows is the tree trained on, and which rows does it never see?')))

    gap10 = va10 - tr10
    S.append(dict(kind='formula', title='The generalisation gap is the validation error minus the training error',
                  size=24,
                  formulas=[('Generalisation gap', r'$\mathrm{gap} = \mathrm{MAE}_{\mathrm{val}} - \mathrm{MAE}_{\mathrm{train}}$'),
                            ('Depth 10', rf'$\mathrm{{gap}} = {d2(va10)} - {d2(tr10)} = {d2(gap10)}\ \mathrm{{{um}}}$'),
                            (f'Depth {best}', rf'$\mathrm{{gap}} = {d2(cur[best][1])} - {d2(cur[best][0])} = {d2(cur[best][1] - cur[best][0])}\ \mathrm{{{um}}}$')],
                  symbols=[['gap', 'Generalisation gap: how much worse the model is on new rows', f'Depth 10: {d2(gap10)} {unit}'],
                           ['MAE_val', 'Validation error, from the formula before', f'{d2(va10)} {unit} at depth 10'],
                           ['MAE_train', 'Training error, from the formula before', f'{d2(tr10)} {unit} at depth 10']],
                  widths=[2.3, 5.6, 4.0],
                  note='A gap near 0 means about the same error on new rows as on the training set. A big gap means overfitting.',
                  notes=(f'The generalisation gap is one subtraction: the validation error minus the training error. At depth 10 it is {d2(va10)} minus {d2(tr10)}, which is {d2(gap10)} {unit}. '
                         f'At our chosen depth, depth {best}, it is {d2(cur[best][1])} minus {d2(cur[best][0])}, which is {d2(cur[best][1] - cur[best][0])} {unit}. '
                         'A small gap says the model does about as well on new rows as on its training set. A big gap says it is overfitting, fitting the noise in the training set. Next we see the gap for five depths in one table.')))

    depths_shown = sorted({1, 2, 4, best, 10})
    rows5 = [[f'{d}' + (' (chosen)' if d == best else ''), str(N['leaves'][d]), f'{cur[d][0]:.2f}', f'{cur[d][1]:.2f}', f'{cur[d][1] - cur[d][0]:.2f}'] for d in depths_shown]
    S.append(dict(kind='table', title='As max_depth grows, the training error keeps falling but the validation error does not',
                  headers=['max_depth', 'Leaf nodes', 'Training MAE', 'Validation MAE', 'Generalisation gap (validation minus training)'], rows=rows5, widths=[2.2, 2.2, 2.0, 2.2, 3.2],
                  icons=False,
                  note=f'MAE in {unit}. A leaf node is a final node at the bottom of the tree, and it holds the prediction. A deeper tree has more leaf nodes. The linear regression model from Class 1 scores {N["line_mae"]:.2f} {unit}, better than every tree.',
                  notes=(f'Same numbers as the curve, in a table. Look at the leaf nodes, the final nodes at the bottom of the tree. Every row ends in exactly one leaf node, and the tree gives every row in it the same prediction. '
                         f'At depth 1 there are {N["leaves"][1]} leaf nodes. At depth 10 there are {N["leaves"][10]}, for only {n_tr} training rows, so the tree is close to keeping one answer for each row. That is overfitting. '
                         f'The last column is the generalisation gap from the last slide. One more fact for later: the linear regression model from Class 1 scored {N["line_mae"]:.2f} {unit}, better than every tree. '
                         'A deeper tree is not a better model. What does that suggest about the shape of this data?')))

    S.append(dict(kind='idea', title='We choose max_depth on the validation set and keep the test set sealed',
                  visual=dict(kind='rowsplit', parts=[dict(label='Training', sub='E1 to E4', n=n_tr, role='The tree is trained here.', fill='ink'),
                                                      dict(label='Validation', sub='E5', n=n_va, role='We compare depths here.', fill='paper'),
                                                      dict(label='Test', sub='E6', n=n_te, role='Sealed. Not used today.', fill='gold')]),
                  lead='Each set is made of whole equipment groups. The picture shows how many rows each set has.',
                  points=[f'There are only {n_va} validation rows, so a score can move by luck.', 'We never tune anything on the test set.'],
                  notes=(f'How did we choose depth {best}? We looked at the validation set only. The picture shows the three sets of our data: the training set from groups E1 to E4, the validation set from group E5, and the test set from group E6. '
                         f'We never touch the test set today. And we must be honest about the validation set: it has only {n_va} rows, so its scores are noisy, and a change of a few percent could be luck. '
                         'So we need a rule for choosing a model that does not chase small differences. That rule comes next. Why would picking the lowest score alone be risky with so few rows?')))

    S.append(dict(kind='formula', title='Choose the simplest model within a tolerance of the best score',
                  size=24,
                  formulas=[('Tolerance limit', r'$\mathrm{limit} = 1.05 \times V_{\mathrm{min}}$'),
                            ('Chosen depth', r'$d^{*} = \mathrm{smallest}\ d\ \mathrm{with}\ V(d) \leq \mathrm{limit}$'),
                            ('Our data', rf'$1.05 \times {d2(tie["vmin"])} = {d2(tie["limit"])}\ \mathrm{{{um}}}, \ d^{{*}} = {best}$')],
                  symbols=[['V(d)', 'Validation MAE of the tree with max_depth d', f'{d2(cur[1][1])} at depth 1, {d2(cur[10][1])} at depth 10'],
                           ['V_min', 'The lowest validation MAE over depths 1 to 10', f'{d2(tie["vmin"])} {unit}, at depth {tie["depth_low"]}'],
                           ['limit', 'The tolerance limit: the lowest value plus 5 percent', f'{d2(tie["limit"])} {unit}'],
                           ['d*', 'The chosen depth: the smallest d that passes', 'Depths that pass: ' + ', '.join(str(d) for d in tie['passing'])]],
                  widths=[1.6, 5.6, 4.7],
                  note=f'A rule of thumb (parsimony: prefer the simpler model), like the one-standard-error rule. d* = chosen max_depth.',
                  notes=(f'Here is the rule for choosing the simplest model within a tolerance of the best validation score, as arithmetic. Find the lowest validation error, V min. For us it is {d2(tie["vmin"])} {unit}, at depth {tie["depth_low"]}. Add 5 percent by multiplying by 1.05, which gives the limit, {d2(tie["limit"])} {unit}. '
                         f'Any depth whose validation error is at or below the limit is within the tolerance of the best. The depths that pass are {", ".join(str(d) for d in tie["passing"])}. '
                         f'We take the smallest of them, depth {best}, because a simpler tree is less likely to overfit. This is a common practical rule, the idea of parsimony, similar in spirit to the one-standard-error rule. The 5 percent is our own choice and it is not a law. What would change if the limit were 1.00?')))

    S.append(dict(kind='idea', title='One split can be lucky, so K-fold cross-validation lets every fold take a turn as the validation fold',
                  visual=dict(kind='folds', labels=[f'Fold {i + 1}' for i in range(5)], subs=[f'{t} rows' for _, t in cv5['sizes']], scores=[f'{x:.2f}' for x in cv5['scores']],
                              summary=f'Mean {cv5["mean"]:.2f} {unit}   Standard deviation {cv5["std"]:.2f} {unit}', unit=f'MAE ({unit})', row_word='Fold', held='Validation fold'),
                  lead=f'K-fold cross-validation cuts the {n_tr} training rows into K = 5 folds (parts of the rows), in the order the rows appear (no shuffle).',
                  points=['In each row, the tree is trained on 4 folds and scored on the gold fold: the validation fold (held-out fold).', 'After 5 rows each fold has been the validation fold once. The 5 scores of a max_depth 4 tree are on the right.'],
                  notes=(f'A single validation split is one test on one day, and the day may be lucky or unlucky. K-fold cross-validation takes several tests. Cut the {n_tr} training rows into five folds. '
                         'In the first row of the picture, the tree is trained on folds two to five, and fold one is the validation fold, also called the held-out fold. It is used only to score the tree. '
                         'Some books call it the test fold, but it is not the sealed test set E6. In the next row a different fold is the validation fold, and so on, until every fold has had its turn. '
                         f'Here are the five scores for a depth-4 tree, from {cv5["lo"]:.2f} to {cv5["hi"]:.2f} {unit}. Five scores tell us more than one.')))

    S.append(dict(kind='formula', title='K-fold gives k scores, and we report their mean and their standard deviation',
                  size=22,
                  formulas=[('Mean of the k scores', r'$\bar{s} = \frac{1}{k} \sum_{j=1}^{k} s_j$'),
                            ('Standard deviation of the k scores', r'$\sigma_s = \sqrt{\frac{1}{k} \sum_{j=1}^{k} (s_j - \bar{s})^2}$')],
                  symbols=[['s', 'The MAE when fold j is the validation fold (j is the fold number)', ', '.join(f'{x:.2f}' for x in cv5['scores']) + f' {unit}'],
                           ['k', 'The number of folds, so the number of scores', '5 folds'],
                           ['s̄', 'The mean (average) of the k scores (s with a bar)', f'{d2(cv5["mean"])} {unit}'],
                           ['σ', 'The standard deviation (sigma): the typical distance of a score from the mean. We divide by k, as np.std does', f'{d2(cv5["std"])} {unit}']],
                  widths=[1.6, 6.3, 4.0],
                  notes=('Two formulas turn the five scores into two numbers. The mean adds up the k scores and divides by k. '
                         'The standard deviation asks how far each score sits from the average, squares those distances so plus and minus cannot cancel, takes their average, and then the square root. '
                         f'For our five scores the mean is {d2(cv5["mean"])} {unit} and the standard deviation is {d2(cv5["std"])} {unit}. We divide by k, the same as NumPy, so your numbers match the notebook. '
                         'A small standard deviation means the folds agree. A large one means the score depends on which fold you ask. First we do it by hand with four easy numbers.')))

    S.append(dict(kind='table', title='By hand with four illustrative scores: the mean is 3 and the standard deviation is 0.71',
                  headers=['Fold', 'Score (MAE)', 'Distance from the mean', 'Squared distance'],
                  rows=[['1', '2', '-1', '1'], ['2', '3', '0', '0'], ['3', '3', '0', '0'], ['4', '4', '+1', '1']], widths=[1.4, 2.2, 3.4, 3.0], icons=False,
                  note='Mean = (2 + 3 + 3 + 4) / 4 = 3. Mean of the squared distances = (1 + 0 + 0 + 1) / 4 = 0.5 (the variance). The square root of 0.5 is 0.71, the standard deviation. These four scores are illustrative (made up).',
                  notes=('Let us do it by hand with four illustrative, made-up fold scores: two, three, three and four. The mean is twelve divided by four, which is three. Now the standard deviation. How far is each score from the mean? Minus one, zero, zero and plus one. '
                         'Square them, so that plus and minus cannot cancel: one, zero, zero, one. Their mean is a half, which is the variance. The square root of a half is 0.71. That number is the standard deviation, the typical distance of a fold score from the mean. '
                         'Check the 0.71 on your own page.')))

    ss = sum(cv5['sq'])
    S.append(dict(kind='table', title=f'The same steps on our five real scores: mean {d2(cv5["mean"])}, standard deviation {d2(cv5["std"])} {unit}',
                  headers=['Fold', f'Score (MAE, {unit})', 'Distance from the mean', 'Squared distance'],
                  rows=[[str(j + 1), d2(x), f'{x - cv5["mean"]:+.2f}', f'{(x - cv5["mean"]) ** 2:.3f}'] for j, x in enumerate(cv5['scores'])] + [['Sum', d2(sum(cv5['scores'])), '0.00', f'{ss:.3f}']],
                  widths=[1.4, 2.8, 3.4, 2.8], icons=False,
                  note=f'Mean = {sum(cv5["scores"]):.2f} / 5 = {d2(cv5["mean"])}. Mean of squares = {ss:.3f} / 5 = {cv5["msq"]:.3f}. Square root = {d2(cv5["std"])}, the standard deviation. Worked from unrounded scores, so the last digit can differ.',
                  notes=(f'Now the same steps on the five real scores from our depth-4 tree. The scores add up to {sum(cv5["scores"]):.2f}, so the mean is {d2(cv5["mean"])} {unit}. '
                         f'Each score has a distance from that mean, some above and some below, and the distances add up to zero. We square them, and the squares add up to {ss:.3f}. '
                         f'Divide by five to get {cv5["msq"]:.3f}, and the square root of that is {d2(cv5["std"])} {unit}. That is the standard deviation you will see in the notebook. '
                         'Compare it with the mean. Is it small or large?')))

    S.append(dict(kind='idea', title='GroupKFold holds out a whole equipment group in each fold, which is how the model is really used',
                  visual=dict(kind='folds', labels=gcodes, subs=[f'{n} rows' for n in grp['sizes'].values()], scores=[f'{x:.2f}' for x in grp['scores'].values()],
                              summary=f'Mean {grp["mean"]:.2f} {unit}   Standard deviation {grp["std"]:.2f} {unit}', unit=f'MAE ({unit})', row_word='Fold', held='Validation group'),
                  lead='GroupKFold keeps each equipment group whole. In each fold one group, E1, E2, E3 or E4, is the validation fold.',
                  points=[f'The tree is trained on the other three groups and scored on the held-out {thing} group, like a new site.', 'Each fold gives one score. The mean and standard deviation are worked out as before.'],
                  notes=(f'Plain K-fold mixes rows from every group, so the model has already seen the same {thing} while it is trained. In real use a new {thing} arrives, and nobody has seen it. '
                         'GroupKFold fixes that by keeping each equipment group whole. In each fold it holds out one group, E1, E2, E3 or E4, trains on the other three, and scores the held-out group. '
                         f'The four scores run from {grp["lo"]:.2f} to {grp["hi"]:.2f} {unit}, with a mean of {grp["mean"]:.2f}. Which of the two designs looks more like the situation you will face at work?')))

    S.append(dict(kind='formula', title='GroupKFold uses the same formulas, with equipment groups as the folds',
                  size=22,
                  formulas=[('Score of group g', r'$s_g = \frac{1}{n_g} \sum_{i \in g} |y_i - \hat{y}_i|$'),
                            ('Mean and standard deviation over the 4 groups', r'$\bar{s} = \frac{1}{4} \sum_{g} s_g, \quad \sigma_s = \sqrt{\frac{1}{4} \sum_{g} (s_g - \bar{s})^2}$')],
                  symbols=[['g', 'The group held out in one fold: E1, E2, E3 or E4', 'E1, then E2, E3, E4 in turn'],
                           ['n', 'Number of rows in group g (the small label g)', ', '.join(f'{g} {n}' for g, n in grp['sizes'].items()) + ' rows'],
                           ['s', 'MAE on group g (the small label g), using a tree that was never trained on g', ', '.join(f'{g} {v:.2f}' for g, v in grp['scores'].items()) + f' {unit}'],
                           ['s̄, σ', 'Mean of the 4 scores, and their standard deviation', f'{d2(grp["mean"])} and {d2(grp["std"])} {unit}']],
                  widths=[2.1, 5.4, 4.4],
                  notes=('GroupKFold needs no new maths. The score for a group g is the MAE on the rows of that group, using a tree trained on the other three groups that never saw g. '
                         'Then we take the mean of the four scores and their standard deviation, with the same two formulas as before, with four in place of k. '
                         f'Our four scores have a mean of {d2(grp["mean"])} {unit} and a standard deviation of {d2(grp["std"])} {unit}. Which group was hardest to predict?')))

    S.append(dict(kind='table', title='The same max_depth 4 tree gets three different scores, depending on how we test it',
                  headers=['Way of testing', 'Scores (MAE)', 'Mean', 'Standard deviation'],
                  rows=[['Single validation split (group E5)', f'{va4:.2f}', f'{va4:.2f}', 'one score only'],
                        ['K-fold, k = 5 (rows in order, no shuffle)', f'{cv5["lo"]:.2f} to {cv5["hi"]:.2f}', f'{cv5["mean"]:.2f}', f'{cv5["std"]:.2f}'],
                        ['GroupKFold, k = 4', f'{grp["lo"]:.2f} to {grp["hi"]:.2f}', f'{grp["mean"]:.2f}', f'{grp["std"]:.2f}']],
                  widths=[3.7, 2.7, 1.7, 3.0], icons=['lock', 'grid', 'people'],
                  note=f'MAE in {unit}. Group E5 turned out harder than the average group, so its single score is higher than both averages. The standard deviation shows how far to trust each mean.',
                  notes=(f'Here is the same tree scored three ways. The single split on group E5 says {va4:.2f}. Plain K-fold says {cv5["mean"]:.2f}, with a standard deviation of {cv5["std"]:.2f}. GroupKFold says {grp["mean"]:.2f}, with a standard deviation of {grp["std"]:.2f}. '
                         'Group E5 happened to be harder than the average group, so the single split gave a gloomier answer than cross-validation. It could just as easily have been luckier. '
                         'Report the mean and the standard deviation, and say how the folds were made. Which of the three would you quote to a client, and what would you add?')))

    S.append(dict(kind='idea', title='Data leakage is information from outside the training set reaching the model',
                  visual=dict(kind='leak', exam='Held-out rows'),
                  lead='Data leakage: information from held-out data, which the model should not see, reaches the model while it is trained.',
                  points=['Held-out rows are the validation or test rows. The dashed red arrow is the leakage.', 'The score looks excellent, then the model fails on real new rows.'],
                  notes=('Now the second big danger. Data leakage means information from outside the training set reaches the model while it is trained. The picture shows the normal path along the bottom: the training rows train the model, and then the model gets a score. '
                         'The held-out rows are the validation or test rows, and they must stay out of training. '
                         'If anything from them slips in, along the red arrow, the model has seen the answers. The score then looks excellent, and the first real machine breaks the spell. '
                         'The worst part is that nothing warns you. There is no error message, only a score that is too good. Have you seen a result that looked too good to be true?')))

    S.append(dict(kind='wide', title='Data leakage comes in three common kinds',
                  visual=dict(kind='icons', items=[dict(icon='folder', head='1 Train-test contamination', text='Validation rows are in the training set'),
                                                   dict(icon='calculator', head='2 Preprocessing leakage', text='Imputer (fills missing values) or scaler (rescales columns) fitted on all rows'),
                                                   dict(icon='key', head='3 Target leakage', text='A feature is built from the target')]),
                  caption='All three make the score look too good.',
                  notes=('Three kinds cover most cases. Train-test contamination: validation rows end up in the training set, for example by joining two files, or by tuning on the test rows again and again. '
                         'Preprocessing leakage: an imputer, which fills missing values, or a scaler, which rescales columns to a common scale, is fitted on all rows before the split, so the training set carries information about the validation rows. '
                         'Target leakage: a feature is computed from the target, such as a column that is only filled in after the failure has happened. We show each one with real numbers.')))

    S.append(dict(kind='idea', title='Train-test contamination: validation rows in the training set make the score look perfect',
                  visual=dict(kind='bars', items=[dict(label='Honest: validation rows held out', value=N['leak']['honest'], dark=True, text=f'{N["leak"]["honest"]:.2f} {unit}'),
                                                  dict(label='Leaky: validation rows in the training set', value=max(N['leak']['leaky'], 0.04), hl=True, text=f'{N["leak"]["leaky"]:.2f} {unit}')],
                              unit=f' {unit}', max_value=max(N['leak']['honest'], 0.1)),
                  lead='Same max_depth 10 tree. Only the training set changed.',
                  points=['In the leaky run the tree was already trained on the validation rows, so it reproduces their answers (overfitting).', 'The honest score is the real one.'],
                  notes=(f'This is the real demonstration from our data. The same tree, depth ten. In the honest version the validation rows are held out, and the validation error is {N["leak"]["honest"]:.2f} {unit}. '
                         f'In the leaky version we put the validation rows into the training set first, which is train-test contamination. The error drops to {N["leak"]["leaky"]:.2f}. The tree has simply memorised those rows, so the leaky score is perfect and tells us nothing. '
                         'Nobody would do this on purpose, but a join or a copy and paste can do it quietly. Which of the two scores would predict a new machine?')))

    S.append(dict(kind='steps', title='A Pipeline fits the imputer on the training set only, which prevents preprocessing leakage',
                  steps=[dict(head='1 Fit the imputer', text='The imputer fills missing values (empty cells). It learns each column’s median from the training set only', icon='calculator'),
                         dict(head='2 Train the tree', text='Fit the tree on the training set, after the missing values are filled', icon='gear'),
                         dict(head='3 Predict', text='Fill the validation set with the same medians, then predict', icon='check')],
                  caption=f'Median of ambient_c: {N["fill"]["train"]:.2f} from the training set, {N["fill"]["allrows"]:.2f} from all rows (preprocessing leakage). Only one value is missing, so the score did not change.',
                  notes=('Preprocessing leakage is the quiet one. If you fill missing values, or scale columns, using all the rows, the validation rows have helped to decide the fill. '
                         f'In our data the median ambient temperature is {N["fill"]["train"]:.2f} from the training set and {N["fill"]["allrows"]:.2f} from all rows. We tried both, and the validation error did not change, because only one value is missing. '
                         'So here the habit costs nothing. That is exactly why it is dangerous: a clean score does not prove a clean method. '
                         'The fix is a Pipeline, which chains the imputer and the tree. In every fold it fits the imputer on the training folds only, then fills the validation fold with those same numbers.')))

    S.append(dict(kind='formula', title='The pipeline rule: fit on the training set only, then apply the same numbers',
                  size=22,
                  formulas=[('Imputer: the median fill', r'$m_j = \mathrm{median}\{\, x_{ij} : i \in \mathrm{train} \,\}$'),
                            ('StandardScaler: mean, then z-score', r'$\mu_j = \frac{1}{n_{tr}} \sum_{i \in \mathrm{train}} x_{ij}, \qquad z_{ij} = \frac{x_{ij} - \mu_j}{\sigma_j}$')],
                  symbols=[['i, j, x, n', 'i is the row, j the column, x the value in row i and column j, n the number of training rows. In preprocessing leakage, i includes validation rows', f'j = 1 load_pct, j = 2 ambient_c; n = {n_tr}'],
                           ['m', 'Median of column j over the training rows', f'ambient_c: {N["fill"]["train"]:.2f}. From all rows: {N["fill"]["allrows"]:.2f}, leakage'],
                           ['μ, σ', 'Mean and standard deviation of column j over the training rows', f'load_pct: {sc_["mu"][0]:.2f} and {sc_["sd"][0]:.2f}'],
                           ['z', 'The z-score (scaled value) of row i in column j', f'Row 1: ({row1[0]:.2f} - {sc_["mu"][0]:.2f}) / {sc_["sd"][0]:.2f} = {row1[2]:.2f}']],
                  widths=[1.5, 5.6, 4.8],
                  notes=('Here is the pipeline rule as a formula. The median for column j is taken over the training rows only. The mean and the standard deviation for column j are also taken over the training rows only. '
                         'Then the same three numbers are applied to every row, including the validation rows. The leakage is simple to state: if the row number i also runs over the validation rows, the imputer or scaler has seen them. '
                         f'Take row one of our training data. Its load is {row1[0]:.2f}. Subtract the mean {sc_["mu"][0]:.2f}, divide by the standard deviation {sc_["sd"][0]:.2f}, and the z-score is {row1[2]:.2f}. '
                         'Class 2 used this scaler, and the pipeline does it for you inside every fold.')))

    rd = N['disguise_rows']
    S.append(dict(kind='idea', title='Target leakage: a feature built from the target gives a great score that cannot be repeated',
                  visual=dict(kind='sheet', headers=['load_pct', 'ambient_c', 'target_rounded', 'target'], rows=[[f'{a:.1f}', f'{c:.1f}', str(r), f'{t:.1f}'] for a, c, r, t in rd], hl=[0, 2]),
                  lead=f'With that feature a max_depth 4 tree scores {N["disguise"]:.2f} {unit}. With honest features it scores {va4:.2f} {unit}.',
                  points=['target_rounded is the target rounded to a whole number. At prediction time the target is unknown.', 'A feature recorded after the event is also target leakage.'],
                  notes=(f'This is target leakage. Suppose someone adds a feature that is the target rounded to a whole number. A depth-4 tree with that feature scores {N["disguise"]:.2f} {unit} on the validation rows, against {va4:.2f} without it. '
                         'It looks like a miracle. But when a new reading arrives, the target is exactly what we do not know yet, so the feature cannot be filled in. '
                         'Real examples are a repair code written after the failure, or a daily total computed from the very value we predict. Ask of every feature: will I have this at the moment I need the prediction?')))

    S.append(dict(kind='list', title='Keep this checklist: five questions before you trust a score',
                  items=['Was the score measured on held-out data (rows the model never saw)?', 'Were the imputer and the scaler fitted on the training set only (no preprocessing leakage)?', 'Does any feature come from the target, or only exist after the event (target leakage)?',
                         'Is the test set (group E6) still sealed?', 'Is the score a cross-validation mean, shown with its standard deviation?'],
                  icons=['lock', 'calculator', 'key', 'shield', 'chart'],
                  notes=('Here is the checklist I want you to keep, and I will ask for it again next class. One: was the score measured on held-out data, rows the model never saw? Two: were the imputer and the scaler fitted on the training set only? '
                         'Three: does any feature come from the target, or only exist after the event? Four: is the test set, group E6, still sealed? Five: is the score a cross-validation mean, shown with its standard deviation? '
                         'If you can answer yes to all five, you may trust the number a little. If you cannot, find out why before you show it to anyone. Take a photo of this slide now.')))

    S.append(dict(kind='table', title='The same code can give different numbers, so we fix the random seed (random_state) and write it down',
                  headers=['random_state (the random seed)', 'max_depth 10 tree: validation MAE', 'Shuffled 5-fold: mean MAE'],
                  rows=[[str(sd), f'about {N["seed_tree"][sd]:.1f}', f'about {N["seed_cv"][sd]:.1f}'] for sd in seeds], widths=[3.8, 4.0, 4.0], icons=False,
                  note=f'MAE in {unit}. The data and the code are the same in every row. Only the seed changed. A random seed makes a random choice repeat exactly. Your last digit can differ.',
                  notes=(f'Random choices sit inside many tools. A tree breaks ties at random, and shuffled folds mix the rows at random. A random seed, which scikit-learn calls random_state, is a number that makes those choices repeat exactly. '
                         f'Look at the table. With the same data and the same code, the depth-10 tree scores about {N["seed_tree"][seeds[0]]:.1f}, {N["seed_tree"][seeds[1]]:.1f} or {N["seed_tree"][seeds[2]]:.1f} {unit}, depending on the seed. '
                         'So a number without its random seed is only half a result. We use random_state equal to seventeen everywhere, and the difference between seeds also tells us how much of a score is luck. Why does a colleague need your seed?')))

    S.append(dict(kind='idea', title='Write down what you ran, so anyone can repeat it',
                  visual=dict(kind='card', title='Run record', fields=[dict(label='Data file', value=f'engineering_data.csv, {n_raw} rows in the file'), dict(label='Split', value='Training E1 to E4, validation E5, test E6 sealed'),
                                                                      dict(label='Random seed', value='random_state = 17 (Step 5 tries 1, 99)'), dict(label='Versions', value='Python, NumPy, pandas, scikit-learn')]),
                  lead=f'Anyone with this record should get your numbers. After cleaning in Class 1, {n_clean} rows remain: {n_tr}, {n_va}, {n_te}.',
                  points=['The notebook prints the record for you.', 'Paste it under every result you report.'],
                  notes=('Reproducibility means that someone else, or you in six months, can run the same code and get the same numbers. For that you need a short record. Which data file, and how many rows. After cleaning in Class 1, the usable rows are fewer than the rows in the file, and the record says so. How the rows were split. The random seed. '
                         'And the versions of Python, NumPy, pandas and scikit-learn, because a new version can change a result slightly. The notebook prints this record in the last step. '
                         'Paste it under every result you report. It takes ten seconds. It is the difference between a result and a claim.')))

    S.append(dict(kind='wide', title='Trust comes from four habits',
                  visual=dict(kind='icons', items=[dict(icon='lock', head='Held-out data', text='Score on rows the model never saw'), dict(icon='grid', head='Cross-validation', text='Report mean and standard deviation'),
                                                   dict(icon='shield', head='No leakage', text='Fit every preprocessing step on the training set'), dict(icon='notebook', head='Reproducibility', text='Record seed, file, versions')]),
                  caption='Next class: features and choosing a model. These habits are the rulebook.',
                  notes=('Let us gather it up in four habits. Score on rows the model never saw. Use cross-validation, so you report a mean with a standard deviation, and GroupKFold when the model will meet new machines. '
                         'Fit every preprocessing step, the imputer and the scaler, on the training set only. And keep a record for reproducibility: the random seed, the data file and the versions. '
                         'With these four habits, a score becomes something you can defend. Before the break, say aloud which habit you are most likely to forget.')))

    S.append(dict(kind='code', title='Read the workflow before you write it',
                  code='pipeline = make_pipeline(imputer, tree_model)\ngroup_kfold = GroupKFold(n_splits=4)\ncv_scores = cross_val_score(\n    pipeline, X_train, y_train,\n    groups=groups, cv=group_kfold,\n    scoring="neg_mean_absolute_error")\nprint(-cv_scores.mean(), cv_scores.std())',
                  reads=['make_pipeline chains the imputer and the tree into one model (a Pipeline).', 'GroupKFold(n_splits=4) makes 4 folds. Each fold holds out one equipment group as the validation fold.',
                         'cross_val_score runs the whole pipeline on every fold and returns one score per fold.', 'The scoring name gives the MAE with a minus sign, so we print -cv_scores.mean().', 'cv_scores.std() is the standard deviation of the scores.'],
                  notes=('Before the break, here is the workflow in six lines. First the Pipeline: the imputer and the tree, chained into one model, so the imputer is fitted inside every fold. Then GroupKFold with four splits, so each fold holds out one equipment group, and we pass the group labels with groups. '
                         'Then cross_val_score, which runs that pipeline on every fold and returns one score per fold. The scoring name has the word neg in it, because scikit-learn likes bigger to be better, so errors come back negative. '
                         'We put a minus in front to get the MAE back. Finally we print the mean and the standard deviation. You can read this aloud now. In the lab you run it.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook. Same steps, your own data.', section='Lab',
                  notes=('That is the end of the concepts. Everything you need is on the slides you have just seen, and every term is explained again inside the notebook. '
                         'Please open the notebook now, and keep the slides closed except for the check slides at the end of the deck. I will walk around. Raise your hand if a cell gives an error. '
                         'Remember to run the cells in order from the top.')))

    S.append(dict(kind='steps', title='The lab has six steps, and the first five end with a check',
                  steps=[dict(head='1 Prepare', text='Load, clean and split the data again', icon='folder'), dict(head='2 Validation curve', text='Train 10 depths, plot the curve, choose max_depth', icon='chart'),
                         dict(head='3 K-fold CV', text='KFold and GroupKFold', icon='grid'), dict(head='4 Data leakage', text='Contamination, preprocessing, target', icon='key'),
                         dict(head='5 Random seed', text='Change the seed, print the run record', icon='clock'), dict(head='6 Save', text='Write three sentences, run all, save', icon='notebook')],
                  caption='In each step, predict first, run second, then read what the output tells you.',
                  notes=('Here are the six steps. One, prepare the data again, briefly. Two, train trees of depth one to ten, plot the validation curve and choose max_depth using the validation set only. '
                         'Three, run K-fold and GroupKFold cross-validation and print the mean and the standard deviation. Four, reproduce the three kinds of leakage: contamination, a fill value from all rows, and a feature built from the target. '
                         'Five, change the random seed and watch a number move, then print the run record. In each step, predict first, then run, then read. Six is your short conclusion and a save.')))

    S.append(dict(kind='table', title='Check your numbers against these before you move on',
                  headers=['What you print', 'You should see'],
                  rows=[['Rows: training, validation, test', f'{n_tr}, {n_va}, {n_te}'], ['Validation MAE at max_depth 1 and at 10', f'{cur[1][1]:.2f} and {cur[10][1]:.2f} {unit}'], ['Chosen max_depth', str(best)],
                        ['K-fold, k = 5: mean and standard deviation', f'{cv5["mean"]:.2f} and {cv5["std"]:.2f}'], ['GroupKFold, k = 4: mean and standard deviation', f'{grp["mean"]:.2f} and {grp["std"]:.2f}'],
                        ['max_depth 10: honest and leaky validation MAE', f'{N["leak"]["honest"]:.2f} and {N["leak"]["leaky"]:.2f}'], [f'max_depth 10 tree, random_state {seeds[0]} and {seeds[2]}', f'about {N["seed_tree"][seeds[0]]:.1f} and about {N["seed_tree"][seeds[2]]:.1f}']],
                  widths=[6.4, 4.0], icons=['folder', 'chart', 'pin', 'grid', 'people', 'key', 'clock'],
                  note=f'MAE in {unit}. If your number differs, stop and ask. Find the step that went wrong. The two seed numbers are about values: a difference in the second decimal is fine.',
                  notes=('Use this table as your checkpoint. If your numbers match, carry on. If they do not, call me over, because every later step builds on the earlier ones. '
                         'The most common reasons are a cell run out of order, a missing random_state, or a depth typed wrongly. A leaky score of zero point zero zero is correct, because that is the whole point of the demonstration. '
                         'Do not edit a number to make it match. Find the cause.')))

    S.append(dict(kind='table', title='Four problems you will meet, what they mean and what to do',
                  headers=['What you see', 'What it means', 'What to do'],
                  rows=[['NameError: X_train', 'Step 1 was not run', 'Run all cells from the top, in order'], ['An error that mentions groups', 'GroupKFold needs the group labels (a groups argument)', 'Pass groups=groups'],
                        ['All scores are negative', 'scikit-learn gives errors a minus sign (neg_ scoring: bigger is better)', 'Put a minus in front: -scores'], ['Numbers differ a little from the slide', 'The random seed (random_state) is missing or different', 'Use random_state=17 in every tree, except in Step 5 where the seeds 1 and 99 are tested on purpose']],
                  widths=[3.6, 4.0, 4.4], icons=['cross', 'key', 'bell', 'flag'],
                  notes=('Four problems come up most often. A name error on X_train means Step 1 was not run, so run all cells from the top. An error that mentions groups means GroupKFold needs the group labels, so pass groups equals groups. '
                         'Negative scores are not a bug. scikit-learn gives errors a minus sign so that bigger is better, so put a minus in front. '
                         'And if your numbers differ a little from the slide, check that random_state equals seventeen in every tree, except in Step 5, where we try other seeds on purpose. Read the last line of any error first.')))

    S.append(dict(kind='list', title='How this class counts towards your coursework',
                  items=['Nothing is submitted today.', 'Block 2 is Classes 3 and 4. Its assignment has three parts: A9 (validation and trust, from today\'s lab), A10 (features) and A11 (model recommendation), both from Class 4.',
                         f'The Block 2 assignment closes on {C.COHORTS[code]["b2_close"]} (Kampala time).', 'The Block 2 quiz opens in the last 20 minutes of Class 4, stays open for 24 hours, and covers Classes 3 and 4.'],
                  icons=['lock', 'doc', 'clock', 'bell'],
                  notes=('A word on how this counts. Nothing is submitted today. Block 2 is this class and the next one. Its assignment has three parts: A9 on validation and trust, which repeats the steps of today\'s lab, and A10 and A11 on features and on recommending a model, which come from Class 4. '
                         f'All three close on {C.COHORTS[code]["b2_close"]}, Kampala time. The Block 2 quiz opens in the last twenty minutes of Class 4, stays open for twenty-four hours, and covers both classes. Keep your saved notebook, because next class we extend it.')))

    s['facilitator'] = dict(
        prep=['Before the class, run the notebook in real Colab and confirm the depth-10 numbers for random_state 1 and 99 (the slides show about 4.7 and about 3.9 for CML3111, worked out with a stand-in for scikit-learn that cannot check them). If real scikit-learn gives different values, correct the seed table and the check slide.',
              'Open the deck in Slide Show mode and the lab notebook in Colab before anyone arrives. Run the notebook from the top once so you know it works on your account.',
              'Put the lab notebook and engineering_data.csv in the shared class folder and post the link. Learners need both files in Colab, in the Files panel.',
              'Write the "check your numbers" table on the board before the lab (numbers for your cohort are in the table below).',
              'Say early that the test group E6 stays sealed. Nobody tunes on it today. Say that the validation fold in K-fold cross-validation is a different thing from the test set E6.',
              'The deck has seven formula slides (MAE and RMSE, training and validation error, the generalisation gap, the simplest-model-within-a-tolerance rule, K-fold mean and standard deviation, GroupKFold, the pipeline rule). Each names every symbol and works the cohort numbers. Students can revise from the PDF alone.',
              'All three cohorts use the same deck and the same clock for this class.'],
        misconceptions=[('The model with the lowest training error is the best model', 'Training error can reach zero by overfitting (fitting the noise in the training set). Judge on held-out rows.'),
                        ('More folds in cross-validation always give a better model', 'Folds give a better estimate of the score. They do not change the model itself.'),
                        ('Data leakage always shows as an error message', 'It shows as a score that is too good. Only the checklist and the order of steps prevent it.'),
                        ('If the score did not change, there was no leakage', 'Preprocessing leakage did not move the score here because only one value is missing. It is still a bad habit.'),
                        ('A random seed is a trick to get a better number', 'A seed only makes a random choice repeat. Trying seeds until one looks good is its own form of cheating.')],
        probes=[('Why does the training error keep falling as the tree gets deeper?', 'A deeper tree has more leaf nodes, so it can keep an answer for almost every row. That is overfitting.'),
                ('How do we choose max_depth, and which rows do we use?', 'The depth with the lowest validation error, or the simplest depth within 5 percent of it (a common practical rule, parsimony). The test set stays sealed.'),
                ('Why is the validation set a weak guide on its own?', 'It has only 15 rows, so its scores are noisy.'),
                ('What does the standard deviation of the fold scores tell you?', 'How much the score depends on which rows were held out. A big standard deviation means less trust in the mean.'),
                ('Why use GroupKFold?', 'In real use a new machine arrives. GroupKFold tests the model on machine groups it has never met.'),
                ('What is the bias-variance trade-off?', 'A model that is too simple misses the pattern (high bias, underfitting). One that is too flexible chases noise (high variance, overfitting). We look for the middle.'),
                ('Name the three kinds of data leakage.', 'Train-test contamination (validation rows in the training set), preprocessing leakage (an imputer or scaler fitted on all rows), target leakage (a feature built from the target).'),
                ('Why is a leaky score of zero not good news?', 'It means the model saw the answers. The honest score is the one to quote.'),
                ('Why do we write down the random seed (random_state)?', 'So that someone else, or you later, gets the same numbers from the same code.')],
        lab_steps=[('Step 1: prepare', 'Rows left to model with: 88. Training, validation, test rows: 58, 15, 15. Anyone with different numbers ran a cleaning cell twice.'),
                   ('Step 2: validation curve', 'Ten lines of training MAE, validation MAE and generalisation gap. Training error falls to near zero. The chosen max_depth is printed. Ask why we accept the simplest depth within 5 percent of the lowest validation MAE.'),
                   ('Step 3: cross-validation', 'Five fold scores, a mean and a standard deviation, then four group scores labelled E1 to E4. The shortcut with cross_val_score must give the same means. The validation fold is not the sealed test set E6.'),
                   ('Step 4: data leakage', 'Honest and leaky MAE at depth 10. The leaky one is 0.00 or 0.01. The preprocessing leakage demo prints two different medians and the same MAE. The target-leakage feature gives a very small error.'),
                   ('Step 5: seeds and record', 'Three seeds, three different numbers. The run record prints versions: they will differ from the stand-in used to check the notebook, which is fine.'),
                   ('Step 6: conclusion and save', 'Three written sentences, then restart and run all, then save a copy.')],
        rescue=['If the concepts run over, skip the by-hand table with the illustrative scores and say: the standard deviation is the typical distance of a fold score from the mean. You can do the arithmetic in the lab.',
                'If only thirty minutes of lab remain, do steps 1 to 3 and the first kind of leakage in step 4. Set the rest as practice for next time.',
                'If wifi fails in the room, the notebook runs unchanged in VS Code with the same libraries.',
                'If several learners are stuck at the same cell, stop the room, run that cell on the projector and let them copy the fix.'],
        after=['Share the lab notebook and engineering_data.csv again so absent learners can follow.', 'Tell the class that nothing is submitted today, and that the lecturer confirms assignment instructions and deadlines in writing.',
               'Note any question you could not answer and start the next class with it.'])
    s['numbers_fn'] = 'numbers'
    return s


def numbers(F):
    """Rows of cohort numbers for the guide: F maps cohort code to facts."""
    codes = list(F)

    def row(label, g):
        return [label] + [g(F[c], refs(F[c])) for c in codes]
    return [row('Training, validation, test rows', lambda f, N: f'{f["b"]["n_tr"]}, {f["b"]["n_va"]}, {f["b"]["n_te"]}'),
            row('Depth 1, validation MAE', lambda f, N: f'{N["curve"][0][2]:.2f} {f["unit"]}'), row('Depth 10, training and validation MAE', lambda f, N: f'{N["curve"][9][1]:.2f} and {N["curve"][9][2]:.2f}'),
            row('Chosen max_depth (simplest within 5 percent of the lowest)', lambda f, N: str(N['best'])), row('Depth-4 tree on E5 (one split), MAE', lambda f, N: f'{N["tree4_valid"]:.2f}'),
            row('K-fold, k = 5: mean and standard deviation', lambda f, N: f'{N["cv5"]["mean"]:.2f} and {N["cv5"]["std"]:.2f}'),
            row('GroupKFold, k = 4: mean and standard deviation', lambda f, N: f'{N["grp"]["mean"]:.2f} and {N["grp"]["std"]:.2f}'),
            row('Honest and leaky MAE, depth 10', lambda f, N: f'{N["leak"]["honest"]:.2f} and {N["leak"]["leaky"]:.2f}'),
            row('ambient_c median: training rows and all rows', lambda f, N: f'{N["fill"]["train"]:.2f} and {N["fill"]["allrows"]:.2f}'),
            row('Target-leakage feature, max_depth 4, MAE', lambda f, N: f'{N["disguise"]:.2f}'),
            row('Depth-10 tree, random_state 1, 17, 99', lambda f, N: ', '.join(f'{N["seed_tree"][s]:.2f}' for s in SEEDS))]
