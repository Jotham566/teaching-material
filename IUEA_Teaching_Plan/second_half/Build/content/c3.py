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

# the Engineering ML project (decision of 13 November 2026): one online window for all three cohorts, Kampala time
WINDOW = 'Monday 23 November 00:00 to Wednesday 25 November 23:59'
PROJECT_NEXT = {'CML3112': 'The project, online, Mon 23 Nov 00:00 to Wed 25 Nov 23:59 (Kampala time). Class 4 is on Tue 24 Nov.',
                'CML3113': 'The project, online, Mon 23 Nov 00:00 to Wed 25 Nov 23:59 (Kampala time). Class 4 is on Fri 27 Nov.',
                'CML3111': 'The project, online, Mon 23 Nov 00:00 to Wed 25 Nov 23:59 (Kampala time). Class 4 is on Fri 27 Nov.'}


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
    # spread of fold scores: the sample standard deviation (divide by k - 1, np.std(scores, ddof=1))
    groups_in = [{g: int(n) for g, n in tr.equipment_id.iloc[t].value_counts().sort_index().items()} for _, t in kfold_indices(len(tr), 5)]
    out['cv5'] = dict(scores=sc, mean=float(np.mean(sc)), std=float(np.std(sc, ddof=1)), lo=min(sc), hi=max(sc), sizes=sizes, groups=groups_in)
    assert all(len(gi) == 4 for gi in groups_in), 'slide claim: every plain K-fold fold holds rows of all four groups'
    # GroupKFold: each training group held out once
    gs = {}
    for g in sorted(tr.equipment_id.unique()):
        a, t = tr[tr.equipment_id != g], tr[tr.equipment_id == g]
        gs[g] = (R.mae(t.target, _fit_predict(a, t, 4)), len(t))
    gv = [v[0] for v in gs.values()]
    out['grp'] = dict(scores={g: v[0] for g, v in gs.items()}, sizes={g: v[1] for g, v in gs.items()}, mean=float(np.mean(gv)), std=float(np.std(gv, ddof=1)), lo=min(gv), hi=max(gv))
    assert out['tree4_valid'] > out['grp']['mean'], 'slide claim: the single E5 split is harder than the average group'
    assert out['line_mae'] < min(v for _, _, v in curve), 'slide claim: the linear regression model beats every tree depth'
    # leaks
    allr = pd.concat([tr, va])
    honest = R.mae(va.target, _fit_predict(tr, va, 10))
    out['leak'] = dict(honest=b['leak_demo']['honest'], leaky=b['leak_demo']['leaky'])
    assert abs(honest - out['leak']['honest']) < 1e-9
    out['fill'] = dict(train=float(tr[FEATS].median()['ambient_c']), trva=float(allr[FEATS].median()['ambient_c']), n_trva=len(allr),
                       mae_all=R.mae(va.target, _fit_predict(tr, va, 10, fill_df=allr)), mae_train=honest)
    tr2, va2 = tr.copy(), va.copy()
    tr2['target_rounded'] = tr2.target.round()
    va2['target_rounded'] = va2.target.round()
    out['disguise'] = R.mae(va.target, _fit_predict(tr2, va2, 4, extra=['target_rounded']))
    out['disguise_rows'] = [(float(r.load_pct), float(r.ambient_c), int(round(r.target)), float(r.target)) for r in f['trf'].assign(target=tr.target.to_numpy()).head(3).itertuples()]
    # seeds
    out['seed_tree'] = {}
    out['seed_cv'] = {}
    out['seed_pick'] = {}
    for sd in SEEDS:
        out['seed_tree'][sd] = R.mae(va.target, _fit_predict(tr, va, 10, seed=sd))
        out['seed_pick'][sd] = pick_depth([(d, 0.0, R.mae(va.target, _fit_predict(tr, va, d, seed=sd))) for d in range(1, 11)])
        out['seed_cv'][sd] = float(np.mean([R.mae(tr.target.iloc[t], _fit_predict(tr.iloc[a], tr.iloc[t], 4)) for a, t in kfold_indices(len(tr), 5, True, sd)]))
    out['n_rows'] = len(f['raw'])
    # the simplest-model-within-a-tolerance rule, worked
    lowest = out['lowest']
    out['tie'] = dict(vmin=lowest, limit=lowest * TOL, depth_low=min(d for d, _, v in curve if v == lowest), passing=[d for d, _, v in curve if v <= lowest * TOL])
    assert min(out['tie']['passing']) == out['best']
    assert out['seed_pick'][TREE_SEED] == out['best']
    # honest reading of the curve: where the training error is near 0, whether the curve is flat after the chosen depth, near misses
    out['over_from'] = min(d for d, t, _ in curve if t < 0.1 * curve[0][1])
    out['flat'] = out['tie']['passing'] == list(range(out['best'], 11))
    out['near_miss'] = [d for d, _, v in curve if lowest * TOL < v <= lowest * TOL * 1.01]
    after = [(d, v) for d, _, v in curve if d > out['best']]
    out['worst_after'] = max(after, key=lambda x: x[1]) if after else None
    # the real five scores, worked by hand (distance from the average and its square)
    m5 = out['cv5']['mean']
    out['cv5']['dist'] = [x - m5 for x in sc]
    out['cv5']['sq'] = [(x - m5) ** 2 for x in sc]
    out['cv5']['var'] = float(np.sum(out['cv5']['sq']) / (len(sc) - 1))      # divide by k - 1
    assert abs(np.sqrt(out['cv5']['var']) - out['cv5']['std']) < 1e-9
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

    clock = [(10, 'Recall from Class 2, and why trust matters'), (40, 'Concepts, part 1: overfitting, validation curve, cross-validation'), (25, 'Concepts, part 2: data leakage, random seed, pipeline'), (15, 'Break'),
             (70, 'Lab: curve, cross-validation, leakage, seeds, records'), (20, 'The project, and how this class counts')]
    plan_note = ('We have three hours. The first seventy-five minutes are concepts only, with no laptop, so you can listen and ask. Then a break. '
                 'Then the lab, about seventy minutes, where you run everything on your own data. In the last twenty minutes I explain the project, which opens online on Monday 23 November.')

    # recall and false positives from threshold 0.5 to 0.3, with a branch for each one that does not change
    rec_said = (f'Recall stayed at {d2(t3["recall"])}.' if d2(t5['recall']) == d2(t3['recall']) else f'Recall rose from {d2(t5["recall"])} to {d2(t3["recall"])}.')
    fp_said = (f'False positives stayed at {t3["fp"]}.' if t5['fp'] == t3['fp'] else f'False positives went from {t5["fp"]} to {t3["fp"]}.')
    recall = [('Why is a majority-class baseline (a model that always predicts no) a poor model, even when its accuracy is about ' + f'{always_pct} percent?', 'It finds none of the real positive cases, so its recall is 0. Accuracy hides that.'),
              ('In a confusion matrix, what is a false negative (FN) and what is a false positive (FP)?', 'False negative: the model said no (negative) and the truth was yes (positive). False positive: the model said yes and the truth was no.'),
              ('What happened to recall and false positives when we lowered the decision threshold from 0.5 to 0.3?', f'{rec_said} {fp_said}')]

    s = dict(
        code=code, cohort_name=f['name'], num=3, week=10, when=f['dates'][3] + ', ' + f['slot'], short_title='Can I trust this model',
        title='Can I trust this model? Overfitting, cross-validation and leakage',
        question=f'How do we know a model that predicts {short} will still work on a {thing} it has never seen?',
        outcome_head='By the end of today you can',
        outcomes=['Explain underfitting, a good fit and overfitting (the bias-variance trade-off), and tune the hyperparameter max_depth with a validation curve',
                  'Work out training error, validation error, the generalisation gap, and a cross-validation mean and standard deviation, by hand',
                  'Score a model with K-fold and GroupKFold cross-validation, and report the mean with its standard deviation',
                  'Name three kinds of data leakage and use a checklist that blocks them'],
        outcome_icons=['chart', 'calculator', 'grid', 'shield'],
        outcome_note=('Here is what you can do by the end of today. You can explain underfitting, a good fit and overfitting, the bias-variance trade-off, and you can tune max_depth, a hyperparameter, by looking at a validation curve. '
                      'You can work out the training error, the validation error, the generalisation gap, and the mean and standard deviation of cross-validation scores, by hand. You can score a model with K-fold and GroupKFold. '
                      'And you can name three kinds of data leakage and keep a checklist that blocks them. Nothing is submitted today. At the end I explain the project, which opens online on Monday 23 November, and how this class counts.'),
        clock=clock, plan_title='Your three hours: ideas first, then the lab', plan_note=plan_note,
        plan_caption='Concepts first, with no laptops. Then the lab, with the notebook open.',
        recall_from='Class 2',
        recall=recall,
        words=[('Overfitting', 'The model fits the noise in the training set (it nearly memorises it) and does worse on new rows. Underfitting is the opposite: too simple to learn the pattern.'),
               ('Cross-validation', 'Scoring a model K times. The rows are cut into K parts called folds. Each fold takes one turn as the validation fold (held-out fold).'),
               ('Data leakage', 'Information the model would not have at prediction time (held-out rows, or the target itself) reaches it while it is trained, so the score looks better than it really is.'),
               ('Bias-variance trade-off', 'Too simple a model misses the pattern (high bias, underfitting). Too flexible a model chases noise (high variance, overfitting).'),
               ('Random seed', 'A fixed number (random_state in scikit-learn) that makes a random choice repeat exactly.')],
        word_icons=['cross', 'grid', 'key', 'chart', 'clock'],
        words_note=('Five words for today. Overfitting is when a model fits the noise in its training set and does worse on new rows. Underfitting is the opposite: too simple to learn the pattern. Cross-validation means scoring a model K times. The rows are cut into K parts called folds, and each fold takes one turn as the validation fold, which some books call the held-out fold. '
                    'Data leakage is information the model would not have at prediction time, such as held-out rows or the target itself, reaching it while it is trained, so the score looks better than it is. The bias-variance trade-off is the industry name for the balance between too simple and too flexible. '
                    'And a random seed, set with random_state, makes a random choice repeat exactly. We use all five before the end.'),
        keep='Your saved lab notebook, the five-question checklist, and the project window: online, Monday 23 to Wednesday 25 November.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Notebook', value='Restart, run all, save'), dict(label='max_depth', value='Chosen on the validation set'),
                                                              dict(label='Rehearsal', value='Released today, not marked'), dict(label='Project', value='Online, 23 to 25 November')]),
        keep_title='Save the notebook, then do the rehearsal before the project opens',
        next=PROJECT_NEXT[code], next_label='Next',
        keep_note=('Before you go, restart the notebook, run all cells from the top and save it. Keep the max_depth you chose and the checklist, because you will use both again. '
                   'The rehearsal is released right after this class. Do it before Monday 23 November, when the project window opens. If anything today was unclear, ask on the class channel.'),
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
                         f'When we lowered the decision threshold from 0.5 to 0.3 on the validation rows: {rec_said} {fp_said} '
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
                         'Doing well on held-out rows it has never seen is called generalisation, and it is the only thing we really want. '
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

    ov = N['over_from']
    wa = N['worst_after']
    curve_said = (f'From depth {best} to depth 10 every validation error is within 5 percent of the lowest, so the red curve is flat there.' if N['flat']
                  else f'After depth {best} the validation error rises a little, to {wa[1]:.2f} {unit} at depth {wa[0]}.')
    over_said = f'From depth {ov} up, the training error is near 0: those trees fit the training rows almost exactly, which is overfitting.'
    S.append(dict(kind='idea', title='The validation curve: as max_depth grows, training error keeps falling but validation error stops improving',
                  visual=dict(kind='depthcurve', curve=[[d, t, v] for d, t, v in curve], best=best, unit=unit, under=(1, 2), over=(ov, 10)),
                  lead='A validation curve plots both errors against max_depth, a hyperparameter (set before training).',
                  points=['Each dot is one tree. Black: training error. Red: validation error. Between them: the gap.',
                          f'Depths 1 and 2: both errors high. From depth {ov}: training error near 0. Gold: chosen depth {best}.'],
                  notes=(f'This is a validation curve from our data. Each point is a tree with a different max_depth, a hyperparameter: a setting we choose before training. '
                         f'The black line is the training error, and it falls all the way to {tr10:.2f}. At depths 1 and 2 both errors are high: that is underfitting. {over_said} '
                         f'The red line is the validation error. {curve_said} The gold band is the depth we choose, depth {best}; the next slides show why. '
                         'In Class 1 you tried depths 1, 2 and 8: this is what you were seeing. Where does the gap start to grow?')))

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
                  note='Small gap: similar error on new rows. Big gap: overfitting. We choose max_depth by validation error.',
                  notes=(f'The generalisation gap is one subtraction: the validation error minus the training error. At depth 10 it is {d2(va10)} minus {d2(tr10)}, which is {d2(gap10)} {unit}. '
                         f'At our chosen depth, depth {best}, it is {d2(cur[best][1])} minus {d2(cur[best][0])}, which is {d2(cur[best][1] - cur[best][0])} {unit}. '
                         'A small gap says the model does about as well on new rows as on its training set. A big gap says it is overfitting, fitting the noise in the training set. '
                         + (f'At depth {best} the gap is large too, so this tree also overfits its training rows. We still choose it, because we choose by the validation error, and no simpler tree does as well on new rows. '
                            if best >= ov else f'At depth {best} the gap is smaller than at depth 10, yet the training error is already below the validation error. We choose by the validation error alone. ')
                         + 'Next, five depths in one table.')))

    depths_shown = sorted({1, 2, 4, best, 10})
    rows5 = [[f'{d}' + (' (chosen)' if d == best else ''), str(N['leaves'][d]), f'{cur[d][0]:.2f}', f'{cur[d][1]:.2f}', f'{cur[d][1] - cur[d][0]:.2f}'] for d in depths_shown]
    S.append(dict(kind='table', title='Five depths in one table: leaf nodes, errors and the generalisation gap',
                  headers=['max_depth', 'Leaf nodes', 'Training MAE', 'Validation MAE', 'Generalisation gap (validation minus training)'], rows=rows5, widths=[2.2, 2.2, 2.0, 2.2, 3.2],
                  icons=False,
                  note=f'MAE in {unit}. A leaf node is a final node: it holds the prediction. The Class 1 linear regression model scores {N["line_mae"]:.2f} {unit}, better than every tree: the target is close to a straight line, and a tree only makes steps.',
                  notes=(f'Same numbers as the curve, in a table. Look at the leaf nodes, the final nodes at the bottom of the tree. Every row ends in exactly one leaf node, and the tree gives every row in it the same prediction. '
                         f'At depth 1 there are {N["leaves"][1]} leaf nodes. At depth 10 there are {N["leaves"][10]}, for only {n_tr} training rows, so the tree is close to keeping one answer for each row. That is overfitting. '
                         f'The last column is the generalisation gap from the last slide. One more fact for later: the linear regression model from Class 1 scored {N["line_mae"]:.2f} {unit}, better than every tree. '
                         'Why? The target rises smoothly, close to a straight line, and a tree can only make steps. So today the tree is our test case for trust. Which depth would you call too deep?')))

    S.append(dict(kind='idea', title='We choose max_depth on the validation set and keep the test set sealed',
                  visual=dict(kind='rowsplit', parts=[dict(label='Training', sub='E1 to E4', n=n_tr, role='The tree is trained here.', fill='ink'),
                                                      dict(label='Validation', sub='E5', n=n_va, role='We compare depths here.', fill='paper'),
                                                      dict(label='Test', sub='E6', n=n_te, role='Sealed. Opened once, at the end.', fill='gold')]),
                  lead='Each set is made of whole equipment groups. The picture shows the rows in each set.',
                  points=[f'Only {n_va} validation rows, so a score can move by luck. Never tune on the test set.',
                          'Test set rule: open it once, after the model and any threshold are chosen. Refit the chosen model on E1 to E5, score it once on E6.'],
                  notes=(f'How did we choose depth {best}? We looked at the validation set only. The picture shows the three sets: training from groups E1 to E4, validation from group E5, and test from group E6. '
                         'The test set has one rule. It is opened once, at the very end, after the model and any decision threshold are chosen. For that final number the chosen model is refitted on all development rows, E1 to E5, and scored once on E6. In the project a supplied cell opens the test set once for you, and Class 4 shows the step in full. '
                         f'The validation set has only {n_va} rows, so its scores are noisy. We need a rule that does not chase small differences. Why would the lowest score alone be risky?')))

    d3 = lambda v: f'{v:.3f}'
    passing = tie['passing']
    if len(passing) == 1:
        rule_said = f'Only depth {best} passes: here the rule and the lowest score agree.'
        change_mult = '1.10'
    elif N['near_miss']:
        nm = N['near_miss'][0]
        rule_said = f'Depth {nm} ({d3(cur[nm][1])}) misses the limit ({d3(tie["limit"])}) by a hair: the rule is sensitive.'
        change_mult = '1.00'
    else:
        rule_said = 'The passing depths are about equally good, so we take the simplest.'
        change_mult = '1.00'
    S.append(dict(kind='formula', title='Tuning a hyperparameter: choose the simplest max_depth within 5 percent of the lowest validation error',
                  size=24,
                  formulas=[('Tolerance limit', r'$\mathrm{limit} = 1.05 \times V_{\mathrm{min}}$'),
                            ('Chosen depth', r'$d^{*} = \mathrm{smallest}\ d\ \mathrm{with}\ V(d) \leq \mathrm{limit}$'),
                            ('Our data', rf'$1.05 \times {d3(tie["vmin"])} = {d3(tie["limit"])}\ \mathrm{{{um}}}, \ d^{{*}} = {best}$')],
                  symbols=[['V(d)', 'Validation MAE of the tree with max_depth d', f'{d2(cur[1][1])} at depth 1, {d2(cur[10][1])} at depth 10'],
                           ['V_min', 'The lowest validation MAE over depths 1 to 10', f'{d3(tie["vmin"])} {unit}, at depth {tie["depth_low"]}'],
                           ['limit', 'The tolerance limit: the lowest value plus 5 percent', f'{d3(tie["limit"])} {unit}'],
                           ['d*', 'The chosen depth: the smallest d that passes', 'Depths that pass: ' + ', '.join(str(d) for d in passing)]],
                  widths=[1.6, 5.6, 4.7],
                  note=f'{rule_said} d* = chosen max_depth (parsimony).',
                  notes=(f'Choosing a hyperparameter such as max_depth is called tuning a hyperparameter. Our rule: find the lowest validation error, V min. For us it is {d3(tie["vmin"])} {unit}, at depth {tie["depth_low"]}. Multiply by 1.05 to get the limit, {d3(tie["limit"])} {unit}. '
                         f'Any depth at or below the limit passes: {", ".join(str(d) for d in passing)}. We take the smallest, depth {best}, because a simpler tree is easier to explain. That is parsimony. {rule_said} '
                         f'The 5 percent is our own choice and it is not a law. The chosen depth can also move with the random seed, as we see later. What would change if we multiplied by {change_mult} instead of 1.05?')))

    S.append(dict(kind='idea', title='One split can be lucky, so K-fold cross-validation lets every fold take a turn as the validation fold',
                  visual=dict(kind='folds', labels=[f'Fold {i + 1}' for i in range(5)], subs=[f'{t} rows' for _, t in cv5['sizes']], scores=[f'{x:.2f}' for x in cv5['scores']],
                              summary=f'Mean {cv5["mean"]:.2f} {unit}   Standard deviation {cv5["std"]:.2f} {unit}', unit=f'MAE ({unit})', row_word='Fold', held='Validation fold'),
                  lead=f'K-fold cross-validation cuts the {n_tr} training rows into K = 5 folds (parts of the rows), in the order the rows appear (no shuffle).',
                  points=['In each line, the tree is trained on 4 folds and scored on the gold validation fold.',
                          'Rows of E1 to E4 are interleaved: every fold holds all four groups (fold 1: ' + ', '.join(f'{g} {n}' for g, n in cv5['groups'][0].items()) + ').'],
                  notes=(f'A single validation split is one test on one day, and the day may be lucky or unlucky. K-fold cross-validation takes several tests. Cut the {n_tr} training rows into five folds. '
                         'In the first line of the picture, the tree is trained on folds two to five, and fold one is the validation fold, also called the held-out fold. Some books call it the test fold, but it is not the sealed test set E6. '
                         f'Here are the five scores for a depth-4 tree, from {cv5["lo"]:.2f} to {cv5["hi"]:.2f} {unit}. One warning: the rows of the four groups are interleaved, so every fold holds rows of all four {thing}s. '
                         f'The model has already met each {thing} in training. Is that how it will be used on a new {thing}?')))

    S.append(dict(kind='formula', title='K-fold gives k scores, and we report their mean and their standard deviation',
                  size=22,
                  formulas=[('Mean of the k scores', r'$\bar{s} = \frac{1}{k} \sum_{j=1}^{k} s_j$'),
                            ('Sample standard deviation of the k scores', r'$\sigma_s = \sqrt{\frac{1}{k - 1} \sum_{j=1}^{k} (s_j - \bar{s})^2}$')],
                  symbols=[['s_j', 'The MAE when fold j is the validation fold (j is the fold number)', ', '.join(f'{x:.2f}' for x in cv5['scores']) + f' {unit}'],
                           ['k', 'The number of folds, so the number of scores', '5 folds'],
                           ['s̄', 'The mean (average) of the k scores (s with a bar)', f'{d2(cv5["mean"])} {unit}'],
                           ['σ_s', 'Sample standard deviation: typical distance of a score from the mean. np.std(scores, ddof=1)', f'{d2(cv5["std"])} {unit}']],
                  widths=[1.6, 6.3, 4.0],
                  notes=('Two formulas turn the five scores into two numbers. The mean adds up the k scores and divides by k. '
                         'The standard deviation asks how far each score sits from the average, squares those distances so plus and minus cannot cancel, adds them, divides by k minus 1, and takes the square root. '
                         'Dividing by k minus 1 gives the sample standard deviation, the usual choice for a few scores. In NumPy you write ddof equals 1, because np.std divides by k unless you say so. '
                         f'Our five scores give a mean of {d2(cv5["mean"])} {unit} and a standard deviation of {d2(cv5["std"])} {unit}. '
                         'A small standard deviation means the folds agree. A large one means the score depends on which fold you ask. Next we work it by hand on our five scores.')))

    ss = sum(cv5['sq'])
    S.append(dict(kind='table', title='By hand: our five fold scores give their mean and standard deviation',
                  headers=['Fold', f'Score (MAE, {unit})', 'Distance from the mean', 'Squared distance'],
                  rows=[[str(j + 1), d2(x), f'{x - cv5["mean"]:+.2f}', f'{(x - cv5["mean"]) ** 2:.3f}'] for j, x in enumerate(cv5['scores'])] + [['Sum', d2(sum(cv5['scores'])), '0.00', f'{ss:.3f}']],
                  widths=[1.4, 2.8, 3.4, 2.8], icons=False,
                  note=f'Mean = {sum(cv5["scores"]):.2f} / 5 = {d2(cv5["mean"])} {unit}. Sum of squares / (k - 1) = {ss:.3f} / 4 = {cv5["var"]:.3f}. Square root = {d2(cv5["std"])} {unit}, the standard deviation. Worked from unrounded scores, so the last digit can differ.',
                  notes=(f'Let us work it by hand on the five real scores from our depth-4 tree. The scores add up to {sum(cv5["scores"]):.2f}, so the mean is {d2(cv5["mean"])} {unit}. '
                         f'Each score has a distance from that mean, some above and some below, and the distances add up to zero. We square them, and the squares add up to {ss:.3f}. '
                         f'Divide by k minus 1, which is four, to get {cv5["var"]:.3f}, and the square root of that is {d2(cv5["std"])} {unit}. That is the standard deviation you will see in the notebook. '
                         'Compare it with the mean. Is it small or large?')))

    S.append(dict(kind='idea', title='GroupKFold holds out a whole equipment group in each fold, which is how the model is really used',
                  visual=dict(kind='folds', labels=gcodes, subs=[f'{n} rows' for n in grp['sizes'].values()], scores=[f'{x:.2f}' for x in grp['scores'].values()],
                              summary=f'Mean {grp["mean"]:.2f} {unit}   Standard deviation {grp["std"]:.2f} {unit}', unit=f'MAE ({unit})', row_word='Fold', held='Validation group'),
                  lead='GroupKFold keeps each group whole: each of E1 to E4 is held out once (scikit-learn picks the order).',
                  points=[f'Plain K-fold put every {thing} in every fold. Here the tree trains on three groups and is scored on the fourth, like a new site.',
                          'Score s_g: MAE on group g. Mean and sample standard deviation as before (divide by 3).'],
                  notes=(f'Plain K-fold mixes rows from every group, so the model has already seen the same {thing} while it is trained. In real use a new {thing} arrives, and nobody has seen it. '
                         'GroupKFold fixes that by keeping each equipment group whole. In each fold it holds out one group, trains on the other three, and scores the held-out group. Each of E1 to E4 takes one turn, in an order scikit-learn chooses to balance the fold sizes. '
                         f'The four scores run from {grp["lo"]:.2f} to {grp["hi"]:.2f} {unit}, with a mean of {grp["mean"]:.2f} and a sample standard deviation of {grp["std"]:.2f}, the same two formulas with four scores. Class 4 shows a five-group version. Which design looks more like your work?')))

    far = max((va4 - cv5['mean']) / cv5['std'], (va4 - grp['mean']) / grp['std']) > 1.5
    e5_said = ('Group E5 scores higher than both means by more than one and a half standard deviations, so it looks harder than the average group.' if far
               else 'The single E5 score is within about one standard deviation of both means: the normal spread from one fold to another.')
    S.append(dict(kind='table', title='The same max_depth 4 tree gets three different scores, depending on how we test it',
                  headers=['Way of testing', 'Scores (MAE)', 'Mean', 'Standard deviation'],
                  rows=[['Single validation split (group E5)', f'{va4:.2f}', f'{va4:.2f}', 'one score only'],
                        ['K-fold, k = 5 (rows in order, no shuffle)', f'{cv5["lo"]:.2f} to {cv5["hi"]:.2f}', f'{cv5["mean"]:.2f}', f'{cv5["std"]:.2f}'],
                        ['GroupKFold, k = 4', f'{grp["lo"]:.2f} to {grp["hi"]:.2f}', f'{grp["mean"]:.2f}', f'{grp["std"]:.2f}']],
                  widths=[3.7, 2.7, 1.7, 3.0], icons=['lock', 'grid', 'people'],
                  note=f'MAE in {unit}. {e5_said} The standard deviation shows how far to trust each mean.',
                  notes=(f'Here is the same tree scored three ways. The single split on group E5 says {va4:.2f}. Plain K-fold says {cv5["mean"]:.2f}, with a standard deviation of {cv5["std"]:.2f}. GroupKFold says {grp["mean"]:.2f}, with a standard deviation of {grp["std"]:.2f}. '
                         f'{e5_said} One split could just as easily have been luckier or unluckier. '
                         'Report the mean and the standard deviation, and say how the folds were made. Which of the three would you quote to a client, and what would you add?')))

    S.append(dict(kind='idea', title='Data leakage is information the model would not have at prediction time reaching it during training',
                  visual=dict(kind='leak', exam='Held-out rows'),
                  lead='Data leakage: information the model would not have at prediction time (held-out rows, or the target itself) reaches it while it is trained.',
                  points=['Held-out rows are the validation or test rows. The dashed red arrow is the leakage.', 'The score looks excellent, then the model fails on real new rows.'],
                  notes=('Now the second big danger. Data leakage means information the model would not have at prediction time, such as held-out rows or the target itself, reaches it while it is trained. The picture shows the normal path along the bottom: the training rows train the model, and then the model gets a score. '
                         'The held-out rows are the validation or test rows, and they must stay out of training. '
                         'If anything from them slips in, along the red arrow, the model has seen the answers. The score then looks excellent, and the model fails on the first real new rows. '
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
                  points=['In the leaky run the tree was already trained on the validation rows, so it reproduces their answers: it has already seen them.', 'The honest score is the real one.'],
                  notes=(f'This is the real demonstration from our data. The same tree, depth ten. In the honest version the validation rows are held out, and the validation error is {N["leak"]["honest"]:.2f} {unit}. '
                         f'In the leaky version we put the validation rows into the training set first, which is train-test contamination. The error drops to {N["leak"]["leaky"]:.2f}. The tree has simply memorised those rows, so the leaky score is {"perfect" if N["leak"]["leaky"] < 0.005 else "almost perfect"} and tells us nothing. '
                         'Nobody would do this on purpose, but a join or a copy and paste can do it quietly. Which of the two scores would predict a new machine?')))

    S.append(dict(kind='steps', title='A Pipeline fits the imputer on the training set only, which prevents preprocessing leakage',
                  steps=[dict(head='1 Fit the imputer', text='The imputer fills missing values (empty cells). It learns each column’s median from the training set only', icon='calculator'),
                         dict(head='2 Train the tree', text='Fit the tree on the training set, after the missing values are filled', icon='gear'),
                         dict(head='3 Predict', text='Fill the validation set with the same medians, then predict', icon='check')],
                  caption=f'Median of ambient_c: {N["fill"]["train"]:.2f} from the training set, {N["fill"]["trva"]:.2f} from training plus validation rows ({N["fill"]["n_trva"]} rows, leakage). Only one value is missing, so the score did not change.',
                  notes=('Preprocessing leakage is the quiet one. If you fill missing values, or scale columns, using all the rows, the validation rows have helped to decide the fill. '
                         f'In our data the median ambient temperature is {N["fill"]["train"]:.2f} from the training set and {N["fill"]["trva"]:.2f} from the training and validation rows together. We tried both, and the validation error did not change, because only one value is missing. '
                         'So here the habit costs nothing. That is exactly why it is dangerous: a clean score does not prove a clean method. '
                         'The fix is a Pipeline, which chains the imputer and the tree. In every fold it fits the imputer on the training folds only, then fills the validation fold with those same numbers.')))

    S.append(dict(kind='formula', title='The pipeline rule: fit on the training set only, then apply the same numbers',
                  size=22,
                  formulas=[('Imputer: the median fill', r'$m_j = \mathrm{median}\{\, x_{ij} : i \in \mathrm{train} \,\}$'),
                            ('StandardScaler: mean, then z-score', r'$\mu_j = \frac{1}{n_{tr}} \sum_{i \in \mathrm{train}} x_{ij}, \qquad z_{ij} = \frac{x_{ij} - \mu_j}{\sigma_j}$')],
                  symbols=[['i, j, x_ij, n_tr', 'Row i, column j, the value x_ij there, n_tr training rows. In preprocessing leakage, i also runs over validation rows', f'j = 1 load_pct, j = 2 ambient_c; n = {n_tr}'],
                           ['m_j', 'Median of column j over the training rows', f'ambient_c: {N["fill"]["train"]:.2f}. Training plus validation: {N["fill"]["trva"]:.2f} (leakage)'],
                           ['μ_j, σ_j', 'Mean and standard deviation of column j, training rows (divide by n_tr, Class 2)', f'load_pct: {sc_["mu"][0]:.2f} and {sc_["sd"][0]:.2f}'],
                           ['z_ij', 'The z-score (standardised value) of row i in column j', f'Row 1: ({row1[0]:.2f} - {sc_["mu"][0]:.2f}) / {sc_["sd"][0]:.2f} = {row1[2]:.2f}']],
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
                  items=['Was the score measured on held-out data (rows the model never saw)?', 'Were the imputer and the scaler fitted on the training set only (no preprocessing leakage)?',
                         'Is every feature available at the moment you need the prediction, and none built from the target (no target leakage)?',
                         'Is the test set (group E6) still sealed, to be opened once after the final choice?', 'Is the score a cross-validation mean, shown with its standard deviation?'],
                  icons=['lock', 'calculator', 'key', 'shield', 'chart'],
                  notes=('Here is the checklist I want you to keep. Questions one to four apply in the project too, and all five return in Class 4. One: was the score measured on held-out data, rows the model never saw? Two: were the imputer and the scaler fitted on the training set only? '
                         'Three: is every feature available at the moment you need the prediction, and none built from the target? Four: is the test set, group E6, still sealed, to be opened once after the final choice? Five: is the score a cross-validation mean, shown with its standard deviation? '
                         'If you can answer yes to all five, you may trust the number a little. If you cannot, find out why before you show it to anyone.')))

    picks = [N['seed_pick'][sd] for sd in seeds]
    seed_said = (f'The chosen max_depth is {picks[0]} with every seed here: the choice is stable for this data.' if len(set(picks)) == 1
                 else f'Even the chosen max_depth moves ({", ".join(str(p) for p in picks)}): on {n_va} validation rows the choice is partly luck. That is why we cross-validate.')
    S.append(dict(kind='table', title='The same code can give different numbers, so we fix the random seed (random_state) and write it down',
                  headers=['random_state (the random seed)', 'max_depth 10 tree: validation MAE', 'Shuffled 5-fold: mean MAE', 'max_depth chosen by the 5 percent rule'],
                  rows=[[str(sd), d2(N['seed_tree'][sd]), d2(N['seed_cv'][sd]), str(N['seed_pick'][sd])] for sd in seeds], widths=[3.0, 3.0, 2.8, 3.0], icons=False,
                  note=f'MAE in {unit}. Only the seed changed. ' + ('The chosen max_depth is the same for every seed here.' if len(set(picks)) == 1 else f'Even the chosen max_depth moves: with {n_va} validation rows it is partly luck.'),
                  notes=(f'Random choices sit inside many tools. A tree breaks ties at random, and shuffled folds mix the rows at random. A random seed, which scikit-learn calls random_state, is a number that makes those choices repeat exactly. '
                         f'With the same data and code, the depth-10 tree scores {d2(N["seed_tree"][seeds[0]])}, {d2(N["seed_tree"][seeds[1]])} or {d2(N["seed_tree"][seeds[2]])} {unit}, depending on the seed. '
                         f'The last column reruns our tuning rule with each seed. {seed_said} So a number without its seed is only half a result. We use random_state equal to seventeen everywhere. Why does a colleague need your seed?')))

    S.append(dict(kind='idea', title='Write down what you ran, so anyone can repeat it',
                  visual=dict(kind='card', title='Run record', fields=[dict(label='Data file', value=f'engineering_data.csv, {n_raw} rows in the file'), dict(label='Split', value='Training E1 to E4, validation E5, test E6 sealed'),
                                                                      dict(label='Random seed', value='random_state = 17 (Step 5 tries 1, 99)'), dict(label='Versions', value='Python, NumPy, pandas, scikit-learn')]),
                  lead=f'Anyone with this record should get your numbers. After cleaning in Class 1, {n_clean} rows remain: {n_tr}, {n_va}, {n_te}.',
                  points=['The notebook prints the record for you.', 'Paste it under every result you report.'],
                  notes=('Reproducibility means that someone else, or you in six months, can run the same code and get the same numbers. For that you need a short record. Which data file, and how many rows. After cleaning in Class 1, the usable rows are fewer than the rows in the file, and the record says so. How the rows were split. The random seed. '
                         'And the versions of Python, NumPy, pandas and scikit-learn, because a new version can change a result slightly. The notebook prints this record in the last step. '
                         'Paste it under every result you report. It takes ten seconds. Who in your team would need to repeat your numbers?')))

    S.append(dict(kind='wide', title='Trust comes from four habits',
                  visual=dict(kind='icons', items=[dict(icon='lock', head='Held-out data', text='Score on rows the model never saw'), dict(icon='grid', head='Cross-validation', text='Report mean and standard deviation'),
                                                   dict(icon='shield', head='No leakage', text='Fit every preprocessing step on the training set'), dict(icon='notebook', head='Reproducibility', text='Record seed, file, versions')]),
                  caption='The project needs all but cross-validation, which returns in Class 4.',
                  notes=('Let us gather it up in four habits. Score on rows the model never saw. Use cross-validation, so you report a mean with a standard deviation, and GroupKFold when the model will meet new machines. '
                         'Fit every preprocessing step, the imputer and the scaler, on the training set only. And keep a record for reproducibility: the random seed, the data file and the versions. '
                         'With these four habits, a score becomes something you can defend. Before the break, say aloud which habit you are most likely to forget.')))

    S.append(dict(kind='code', title='Read the workflow before you write it',
                  code='pipeline = make_pipeline(imputer, tree_model)\ngroup_kfold = GroupKFold(n_splits=4)\ncv_scores = -cross_val_score(\n    pipeline, X_train, y_train,\n    groups=groups, cv=group_kfold,\n    scoring="neg_mean_absolute_error")\nprint(cv_scores.mean(), cv_scores.std(ddof=1))',
                  reads=['make_pipeline chains the imputer and the tree into one model (a Pipeline).', 'GroupKFold(n_splits=4): each fold holds out one equipment group.',
                         'cross_val_score runs the pipeline on every fold: one score per fold.', 'The scoring gives the MAE with a minus sign; the minus in front turns it back.', 'std(ddof=1): sample standard deviation (divide by k - 1).'],
                  notes=('Before the break, here is the workflow in seven lines. First the Pipeline: the imputer and the tree, chained into one model, so the imputer is fitted inside every fold. Then GroupKFold with four splits, so each fold holds out one equipment group, and we pass the group labels with groups. '
                         'Then cross_val_score, which runs that pipeline on every fold and returns one score per fold. The scoring name has the word neg in it, because scikit-learn likes bigger to be better, so errors come back negative. '
                         'We put a minus in front to get the MAE back. Finally we print the mean and the standard deviation, with ddof equals 1 so it divides by k minus 1. In the lab you run it.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook. Same steps, your own data.', section='Lab',
                  notes=('That is the end of the concepts. Everything you need is on the slides you have just seen, and every term is explained again inside the notebook. '
                         'Please open the notebook now, and keep the slides closed except for the check slides at the end of the deck. I will walk around. Raise your hand if a cell gives an error. '
                         'Remember to run the cells in order from the top.')))

    S.append(dict(kind='steps', title='The lab has seven steps, and the first six end with a check',
                  steps=[dict(head='1 Prepare', text='Load, clean and split the data again', icon='folder'), dict(head='2 Validation curve', text='Train 10 depths, choose max_depth', icon='chart'),
                         dict(head='3 K-fold CV', text='KFold and GroupKFold', icon='grid'), dict(head='4 Data leakage', text='Three kinds, planted on purpose', icon='shield'),
                         dict(head='5 Random seed', text='Change the seed, print the run record', icon='clock'), dict(head='6 Records', text='A function on records, as in the project', icon='doc'),
                         dict(head='7 Save', text='Three sentences, run all, save', icon='notebook')],
                  caption='In each step: predict, run, then read the output. Steps 1 to 6 end with a CHECK of your numbers.',
                  notes=('Here are the seven steps. One, prepare the data again, briefly. Two, train trees of depth one to ten, plot the validation curve and choose max_depth using the validation set only. '
                         'Three, run K-fold and GroupKFold cross-validation and print the mean and the standard deviation. Four, reproduce the three kinds of leakage. Five, change the random seed and print the run record. '
                         'Six is new and the project needs it: you wrap a pipeline in a function that takes records, a list of dictionaries, and you rank models with a list comprehension and sorted. Seven is your short conclusion and a save.')))

    S.append(dict(kind='table', title='Check your numbers against these before you move on',
                  headers=['What you print', 'You should see'],
                  rows=[['Rows: training, validation, test', f'{n_tr}, {n_va}, {n_te}'], ['Validation MAE at max_depth 1 and at 10', f'{cur[1][1]:.2f} and {cur[10][1]:.2f} {unit}'], ['Chosen max_depth', str(best)],
                        ['K-fold, k = 5: mean and standard deviation', f'{cv5["mean"]:.2f} and {cv5["std"]:.2f}'], ['GroupKFold, k = 4: mean and standard deviation', f'{grp["mean"]:.2f} and {grp["std"]:.2f}'],
                        ['max_depth 10: honest and leaky validation MAE', f'{N["leak"]["honest"]:.2f} and {N["leak"]["leaky"]:.2f}'], [f'max_depth 10 tree, random_state {seeds[0]} and {seeds[2]}', f'{d2(N["seed_tree"][seeds[0]])} and {d2(N["seed_tree"][seeds[2]])}']],
                  widths=[6.4, 4.0], icons=['folder', 'chart', 'pin', 'grid', 'people', 'key', 'clock'],
                  note=f'MAE in {unit}. Standard deviations divide by k - 1 (ddof=1). If your number differs, stop and ask. With another scikit-learn version a difference in the second decimal is fine.',
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

    c4day = 'Tuesday 24 November, while the window is still open' if code == 'CML3112' else 'Friday 27 November, after the window has closed'
    S.append(dict(kind='list', title='How this class counts towards your coursework',
                  items=['Nothing is submitted today. Block 2 (Classes 3 and 4) is practice with feedback. It does not count toward your final mark.',
                         f'Its assignment (A9 from today, A10 and A11 from Class 4) closes on {C.COHORTS[code]["b2_close"]}, Kampala time.',
                         'The Block 2 quiz opens in the last 20 minutes of Class 4, stays open 24 hours, and covers both classes.',
                         'Your final mark: A1 to A5, Q1 to Q5, Practical Test 1 and the Engineering ML project (40 percent).'],
                  icons=['lock', 'doc', 'bell', 'check'],
                  notes=('A word on how this counts. The block work is practice: it is collected and you get feedback, but it does not count toward your final mark. Nothing is submitted today. Block 2 is this class and the next one. '
                         'Its assignment has three parts: A9 on validation and trust, which repeats the steps of today\'s lab, and A10 and A11, which come from Class 4. '
                         f'All three close on {C.COHORTS[code]["b2_close"]}, Kampala time. The Block 2 quiz opens in the last twenty minutes of Class 4 and stays open for twenty-four hours. '
                         'Your final mark comes from A1 to A5, Q1 to Q5, Practical Test 1 and the Engineering ML project, which is worth 40 percent. The project opens before Class 4, so the next three slides are about it.')))

    S.append(dict(kind='steps', title='The project is one online sitting of 3 hours between 23 and 25 November',
                  steps=[dict(head='1 Rehearse', text='The unmarked rehearsal, in the revision class', icon='folder'),
                         dict(head='2 Enter', text='Any time from Mon 23 Nov 00:00 to Wed 25 Nov 23:59', icon='calendar'),
                         dict(head='3 Press Start', text='Your 3 hours (180 minutes) begin', icon='clock'),
                         dict(head='4 Work', text='Part A notebook, 30 marks. Part B memo form, 15 marks', icon='gear'),
                         dict(head='5 Check, submit', text='Before your countdown ends', icon='check')],
                  highlight=None,
                  caption='Individual, online from anywhere, marked by computer, 40 percent. Kampala time. Start by Wednesday 20:59 for the full 3 hours.',
                  notes=('Here is how the Engineering ML project works. It is individual, it is online, and the computer marks it. It counts 40 percent of the course. '
                         'You sit it from anywhere, on your own laptop, with your own Google account and an internet connection. '
                         'Part A is a coded notebook worth 30 marks. Part B is a decision memo form inside the notebook, worth 15. '
                         'The window opens on Monday 23 November at midnight and closes on Wednesday 25 November at 23:59, Kampala time. When you press Start, you have three hours, '
                         'but the window still closes at 23:59 on Wednesday, so if you start after 20:59 you lose time. Which day will you sit it?')))

    S.append(dict(kind='table', title='You enter with your registration number, check your notebook, then submit from the last cell',
                  headers=['Step', 'What you do'],
                  rows=[['Enter', 'Open your course entry link and type your registration number. Check that the name shown is yours, then press Start. A countdown shows your 3 hours.'],
                        ['Check my notebook', 'Restart session and run all, then run the Check my notebook cell. It runs your code again from the top and names any failing cell or missing function. It shows no mark.'],
                        ['Submit', 'Run the last cell, Submit your test, and press Submit test. Keep the receipt code. You may submit again before your deadline: the latest one on time is marked.'],
                        ['Your result', 'Your mark is shown after the window closes.'],
                        ['Help', 'Class channel, 08:00 to 20:00 each day. If something fails, post a screenshot at once: I can allow one fresh attempt.']],
                  widths=[3.0, 8.9], icons=['pin', 'check', 'doc', 'chart', 'bell'],
                  notes=('Open the entry link for your course and type your registration number. The page shows your name. If the name is not yours, stop and tell me on the class channel. Then press Start, and the countdown begins. '
                         'Before you submit, restart and run all, then run the Check my notebook cell. It runs your code again from the top, the way the marking computer does, and tells you what is missing. '
                         'Then run the last cell and press Submit test. Keep the receipt code. Your mark comes after the window closes. '
                         'I answer questions on the class channel from 08:00 to 20:00 each day. If your laptop or connection fails, post a screenshot at once. I can allow one fresh attempt, and it still closes on Wednesday at 23:59. Have you ever lost marks because a notebook did not run from the top?')))

    S.append(dict(kind='table', title='The project tests data cleaning, three regression models, a warning question and one honest test',
                  headers=['Part', 'What it tests'],
                  rows=[['The data', 'Real steel plant meter readings, one every 15 minutes for a year, the same file for everyone. You predict the energy used (kWh) in months the model has not seen.'],
                        ['Part A, 30 marks', 'Clean the data, two labelled charts, split by month (rule given), baseline, linear regression and decision tree in pipelines, MAE and RMSE, no leakage, the warning question, the test set opened once, results and functions. Not tested: cross-validation, Class 4.'],
                        ['Warning question', 'Logistic regression probabilities, then TP, FP, FN, TN, precision and recall at the fixed threshold 0.5.'],
                        ['Part B, 15 marks', 'The memo form: the chosen model, your numbers, limits, a next step.'],
                        ['Rules', 'Work alone, with no AI tool. Anyone may be asked online to explain their code.']],
                  widths=[3.0, 8.9], icons=['chart', 'gear', 'bell', 'doc', 'shield'],
                  notes=('Here is what the project tests. The data are real: meter readings from a steel plant, one every fifteen minutes for a whole year, the same file for every student. You predict the energy used in kilowatt hours, for months the model has not seen. '
                         'In Part A you clean the data, draw two labelled charts, split by month with the rule given, fit a baseline, a linear regression and a decision tree in pipelines, and score them with MAE and RMSE. '
                         'Then a light warning question with logistic regression at the fixed threshold 0.5, and the test set opened once with the supplied cell. Part B is the memo form. '
                         f'You work alone, with no AI tool. Class 4 is on {c4day}. Which item worries you most?')))

    s['facilitator'] = dict(
        prep=['Week 10 is a revision class (CML3112 Tuesday 17 November; CML3113 and CML3111 Friday 20 November): Class 3 is not taught as a lecture. Work through the project rehearsal with the run sheet Revision_Class_<code>_*.docx in Lecturer Guides. This deck stays as reading for students.',
              'Before the class, run the notebook in real Colab and compare the depth-10 numbers for random_state 1, 17 and 99 with the row "Depth-10 tree, random_state 1, 17, 99" of the table below (correct for every cohort; real scikit-learn 1.9.1 gives exactly these). Another version may differ in the second decimal.',
              'The slide map below shows the CML3112 titles. Titles carry no cohort numbers, but the numbers on the slides differ by cohort: use the per-cohort table.',
              'Decision on choosing max_depth (tuning a hyperparameter): the simplest depth within 5 percent of the lowest validation MAE. The slides say plainly where the curve is flat, where the chosen tree also overfits its training rows, and that the chosen depth moves with the seed (CML3111 and CML3112: 6, 7, 8 for seeds 1, 17, 99; CML3113: 5 for all three).',
              'Cross-validation spread is the sample standard deviation (divide by k - 1, np.std(scores, ddof=1)). Cross-validation is not in the project. The Class 2 StandardScaler divides by n: say once that these are two different jobs.',
              'Open the deck in Slide Show mode and the lab notebook in Colab before anyone arrives. Run the notebook from the top once so you know it works on your account.',
              'Put the lab notebook and engineering_data.csv in the shared class folder and post the link. Learners need both files in Colab, in the Files panel.',
              'Write the "check your numbers" table on the board before the lab (numbers for your cohort are in the table below).',
              'Say early that the test group E6 stays sealed. It is opened once, after the model and any threshold are chosen; the chosen model is then refitted on E1 to E5 and scored once on E6 (Class 4 shows this). Say that the validation fold in K-fold cross-validation is a different thing from the test set E6.',
              'The deck has five formula slides (training and validation error, the generalisation gap, the simplest-model-within-a-tolerance rule, K-fold mean and standard deviation, the pipeline rule). Each names every symbol and works the cohort numbers. The GroupKFold slide states that the same formulas apply with four groups. Students can revise from the PDF alone.',
              'The project slides at the end follow the blueprint of 14 November 2026: online window Monday 23 November 00:00 to Wednesday 25 November 23:59 Kampala time, 3 hours from Start (start by 20:59 on Wednesday for the full time), 40 percent, Part A 30 and Part B 15, marked by computer; enter with the registration number, Check my notebook, Submit test, the mark shown after the window closes; support on the class channel 08:00 to 20:00 each day (confirm these hours before you say them); one fresh attempt after a reported technical failure. No cross-validation, no cost table and no threshold choice in the project: the warning question uses the fixed threshold 0.5. Describe the data only as a steel plant\'s real meter readings, split by month.',
              'Have the rehearsal (practice notebook and practice data, not marked) and the entry link ready to release right after the class: CML3112 Tuesday 17 November, CML3113 and CML3111 Friday 20 November.',
              'All three cohorts use the same deck and the same clock for this class.'],
        misconceptions=[('The model with the lowest training error is the best model', 'Training error can reach zero by overfitting (fitting the noise in the training set). Judge on held-out rows.'),
                        ('More folds in cross-validation always give a better model', 'Folds give a better estimate of the score. They do not change the model itself.'),
                        ('Data leakage always shows as an error message', 'It shows as a score that is too good. Only the checklist and the order of steps prevent it.'),
                        ('If the score did not change, there was no leakage', 'Preprocessing leakage did not move the score here because only one value is missing. It is still a bad habit.'),
                        ('A random seed is a trick to get a better number', 'A seed only makes a random choice repeat. Trying seeds until one looks good is its own form of cheating.'),
                        ('The chosen max_depth is a fact about the data', 'With only 15 validation rows it can move with the seed (6, 7 or 8 for two cohorts). Cross-validation gives a steadier picture.'),
                        ('The chosen depth is a good fit, so its gap must be small', 'We choose by validation error. Where the curve is flat, the chosen tree can still overfit its training rows (CML3111 depth 7 has a gap of 3.79 deg C).')],
        probes=[('Why does the training error keep falling as the tree gets deeper?', 'A deeper tree has more leaf nodes, so it can keep an answer for almost every row. That is overfitting.'),
                ('How do we choose max_depth, and which rows do we use?', 'Tuning a hyperparameter: the simplest depth whose validation MAE is within 5 percent of the lowest (parsimony). Validation set only; the test set stays sealed.'),
                ('Why does the linear regression model beat every tree here?', 'The target rises smoothly with load and ambient temperature, close to a straight line. A tree can only make steps.'),
                ('Why divide by k - 1 for the standard deviation of fold scores?', 'It is the sample standard deviation, the usual choice for a few scores: np.std(scores, ddof=1).'),
                ('Why is the validation set a weak guide on its own?', 'It has only 15 rows, so its scores are noisy.'),
                ('What does the standard deviation of the fold scores tell you?', 'How much the score depends on which rows were held out. A big standard deviation means less trust in the mean.'),
                ('Why use GroupKFold?', 'Plain K-fold puts rows of all four groups in every fold, so the model has met each machine. GroupKFold tests on a group it has never met, as in real use.'),
                ('What is the bias-variance trade-off?', 'A model that is too simple misses the pattern (high bias, underfitting). One that is too flexible chases noise (high variance, overfitting). We look for the middle.'),
                ('Name the three kinds of data leakage.', 'Train-test contamination (validation rows in the training set), preprocessing leakage (an imputer or scaler fitted on all rows), target leakage (a feature built from the target).'),
                ('Why is a leaky score of zero not good news?', 'It means the model saw the answers. The honest score is the one to quote.'),
                ('Why do we write down the random seed (random_state)?', 'So that someone else, or you later, gets the same numbers from the same code.')],
        lab_steps=[('Step 1: prepare', 'Rows left to model with: 88. Training, validation, test rows: 58, 15, 15. Anyone with different numbers ran a cleaning cell twice.'),
                   ('Step 2: validation curve', 'Ten lines of training MAE, validation MAE and generalisation gap, then each depth to 3 decimals with passes or fails. The chosen max_depth is printed. Ask why we accept the simplest depth within 5 percent of the lowest validation MAE.'),
                   ('Step 3: cross-validation', 'Five fold scores with the groups in each validation fold (all four every time), a mean and a sample standard deviation (ddof=1), then four group scores, sorted E1 to E4 (scikit-learn holds them out in its own order). The shortcut with cross_val_score must give the same means.'),
                   ('Step 4: data leakage', 'Honest and leaky MAE at depth 10. The leaky one is 0.00 or 0.01. The preprocessing leakage demo prints two different medians and the same MAE. The target-leakage feature gives a very small error.'),
                   ('Step 5: seeds and record', 'Three seeds, three different numbers, and the chosen max_depth for each seed. The run record prints versions: they will differ from the stand-in used to check the notebook, which is fine.'),
                   ('Step 6: records', 'The project form: a pipeline wrapped in predict_records, which takes lists of dictionaries and returns a list. A list comprehension gives one error per row, and sorted with key=lambda ranks three models by validation MAE. Linear regression comes first in every cohort.'),
                   ('Step 7: conclusion and save', 'Three written sentences, then restart and run all, then save a copy.')],
        rescue=['If the concepts run over, skip the by-hand table of the five fold scores and say: the standard deviation is the typical distance of a fold score from the mean. The notebook does the arithmetic.',
                'If the concepts still run over, show the run record slide briefly: the notebook prints the record in Step 5.',
                'If only thirty minutes of lab remain, do steps 1 to 3, the first kind of leakage in step 4, and step 6 (records), which the project needs. Set the rest as practice before the rehearsal.',
                'Never cut the three project slides at the end. If time is short, read them aloud and post them on the class channel.',
                'If wifi fails in the room, the notebook runs unchanged in VS Code with the same libraries.',
                'If several learners are stuck at the same cell, stop the room, run that cell on the projector and let them copy the fix.'],
        after=['Share the lab notebook and engineering_data.csv again so absent learners can follow.', 'Release the rehearsal right after the class and post the project window, the entry link and the support hours on the class channel.',
               'Tell the class that nothing is submitted today, and that the lecturer confirms assignment instructions and deadlines in writing.',
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
            row('Chosen max_depth (simplest within 5 percent of the lowest)', lambda f, N: str(N['best'])), row('Chosen max_depth with random_state 1, 17, 99', lambda f, N: ', '.join(str(N['seed_pick'][s]) for s in SEEDS)), row('Depth-4 tree on E5 (one split), MAE', lambda f, N: f'{N["tree4_valid"]:.2f}'),
            row('K-fold, k = 5: mean and sample standard deviation (ddof=1)', lambda f, N: f'{N["cv5"]["mean"]:.2f} and {N["cv5"]["std"]:.2f}'),
            row('GroupKFold, k = 4: mean and sample standard deviation (ddof=1)', lambda f, N: f'{N["grp"]["mean"]:.2f} and {N["grp"]["std"]:.2f}'),
            row('Honest and leaky MAE, depth 10', lambda f, N: f'{N["leak"]["honest"]:.2f} and {N["leak"]["leaky"]:.2f}'),
            row('ambient_c median: training rows, and training plus validation rows', lambda f, N: f'{N["fill"]["train"]:.2f} and {N["fill"]["trva"]:.2f}'),
            row('Target-leakage feature, max_depth 4, MAE', lambda f, N: f'{N["disguise"]:.2f}'),
            row('Depth-10 tree, random_state 1, 17, 99', lambda f, N: ', '.join(f'{N["seed_tree"][s]:.2f}' for s in SEEDS))]
