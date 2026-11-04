"""Class 2 (Week 9): binary classification, yes or no, and how to measure it. Concepts first, then the lab. Built once, re-skinned for three cohorts.

Every number comes from ref/week_reference_numpy.py (bundle) or from the same reference helpers run on the cohort's own rows (the per-row probabilities
and the worked example). Nothing is typed. The sealed test group E6 is never used in a descriptive claim.

Terminology: real industry terms (see TERMS.md): positive class, TP/FN/FP/TN, majority-class baseline, decision threshold, sigmoid (logistic) function,
standard deviation, FPR/TPR, ROC curve, AUC. Each is explained in plain words at first use."""
import numpy as np

import common as C

R = C.R

# cohort wording: the label, what the reading is, what someone does with a yes, and the cost of each kind of mistake. Nothing else is invented.
COH = {
    'CML3112': dict(label='high cooling load', reading='Load and air temperature for one building', act='Yes: start extra cooling early', who='plant operator',
                    miss=['The cooling plant is not ready.', 'Rooms can get too warm.'], alarm=['Extra cooling starts early for nothing.', 'It wastes some energy.'],
                    miss_line='Rooms get too warm', verb='reaches'),
    'CML3113': dict(label='high energy demand', reading='Load and air temperature at one crusher', act='Yes: warn the control room', who='control room',
                    miss=['Demand rises with no warning.', 'It can strain the supply.'], alarm=['The control room plans for demand that never comes.', 'It costs some time.'],
                    miss_line='Demand arrives with no warning', verb='reaches'),
    'CML3111': dict(label='overheating', reading='Load and air temperature at one motor', act='Yes: raise a warning and check cooling', who='maintenance team',
                    miss=['A winding overheats with no warning.', 'The insulation can be damaged.'], alarm=['Someone checks a healthy motor.', 'It costs some time.'],
                    miss_line='A winding overheats unseen', verb='reaches'),
}


def _tree_cls(t, names):
    if t[0] == 'leaf':
        return {'v': 'yes' if t[1] >= 0.5 else 'no'}
    return {'q': f'{names[t[1]]} <= {float(t[2]):.1f}?', 'yes': _tree_cls(t[3], names), 'no': _tree_cls(t[4], names)}


def model_numbers(f):
    """Recompute the logistic model with the reference helpers: per-row probabilities and the worked example. Cross-checked against the bundle."""
    code = f['code']
    lim = R.COHORT[code]['limit']
    ltr = (f['tr'].target >= lim).astype(int).to_numpy()
    lva = (f['va'].target >= lim).astype(int).to_numpy()
    mu, sd = R.scaler_fit(f['trf'])
    Xs, Vs = R.scaler_apply(f['trf'], mu, sd), R.scaler_apply(f['vaf'], mu, sd)
    b0, w = R.logreg_fit(Xs, ltr)
    pr = R.logreg_proba(b0, w, Vs)
    bl = f['b']['logit']
    assert np.allclose(pr[:5], bl['proba_first5'], atol=1e-9), 'probabilities differ from the bundle'
    k = 2                                                    # the third validation row, a real yes in every cohort
    z = float(b0 + Vs[k] @ w)
    ex = dict(k=k, raw=(float(f['vaf'].iloc[k, 0]), float(f['vaf'].iloc[k, 1])), x=[float(v) for v in Vs[k]], z=z, p=float(R.sigmoid(z)), actual=int(lva[k]))
    return dict(probs=[float(p) for p in pr], actual=[int(v) for v in lva], ex=ex, mu=mu, sd=sd, b=float(b0), w=[float(v) for v in w], lim=lim)


def build(code):
    f = C.facts(code)
    b, unit, short, thing = f['b'], f['unit'], f['short'], f['thing']
    K_ = COH[code]
    M = model_numbers(f)
    cc, cm, mt = b['cls_counts'], b['logit_conf'], b['logit_metrics']
    tcm, tmt = b['tree_conf'], b['tree_metrics']
    th = b['thresholds']
    t3, t5, t7 = th
    always, auc = b['always_no_acc'], b['auc']
    lg = b['logit']
    sc = b['scaler']
    lim = M['lim']
    limit = f'{lim:g} {unit}'
    label = K_['label']
    ex = M['ex']
    n_va = cc['va_n']
    n_pos, n_neg = cc['va_pos'], cc['va_n'] - cc['va_pos']
    pairs = n_pos * n_neg
    wins = int(round(auc * pairs))
    assert abs(wins / pairs - auc) < 1e-9
    tp, fn, fp, tn = cm['tp'], cm['fn'], cm['fp'], cm['tn']
    assert tp + fn == n_pos and tp + fn + fp + tn == n_va
    d2 = lambda v: f'{v:.2f}'
    pl = lambda n, w: f'{n} {w}' + ('' if n == 1 else 's')
    tr_ids = f['tr'].record_id.tolist()
    va_id3 = int(f['va'].record_id.iloc[2])
    vr3 = f'validation row 3 (record_id {va_id3})'
    tr1 = f'training row 1 (record_id {int(tr_ids[0])})'
    dec_ex = 'yes' if ex['p'] >= 0.5 else 'no'
    always_pct = int(round(always * 100))
    pts = [(float(x), float(y)) for x, y in zip(f['trf'].load_pct, f['tr'].target)]
    pos_idx = [i for i, (_, y) in enumerate(pts) if y >= lim]
    assert len(pos_idx) == cc['tr_pos']
    names = ['load_pct', 'ambient_c']
    tree_node = _tree_cls(R.tree_clf_fit(f['trf'], (f['tr'].target >= lim).astype(int).to_numpy(), 3), names)

    # ---- decision threshold story, built from the reference table
    def chg(a, b_, what):
        pl_ = what.endswith('s')
        return (f'{what} stay at {a}' if pl_ else f'{what} stays at {a}') if a == b_ else (f'{what} go from {a} to {b_}' if pl_ else f'{what} goes from {a} to {b_}')
    story_lo = f'Lowering the decision threshold from 0.5 to 0.3: {chg(d2(t5["recall"]), d2(t3["recall"]), "recall")}, and {chg(t5["fp"], t3["fp"], "false positives (FP)")}.'
    story_hi = f'Raising it from 0.5 to 0.7: {chg(d2(t5["recall"]), d2(t7["recall"]), "recall")}, and {chg(t5["fp"], t7["fp"], "false positives (FP)")}.'
    note_lo = f'0.5 to 0.3: {chg(d2(t5["recall"]), d2(t3["recall"]), "recall")}; {chg(t5["fp"], t3["fp"], "FP")}.'
    note_hi = f'0.5 to 0.7: {chg(d2(t5["recall"]), d2(t7["recall"]), "recall")}; {chg(t5["fp"], t7["fp"], "FP")}.'
    trade = len({x['fp'] for x in th}) > 1
    free_lunch = '' if trade else ' On these 15 rows no decision threshold adds a false positive, so the precision-recall trade-off is not visible here. A slide with illustrative numbers shows it after the table.'
    nobody = [t['th'] for t in th if t['tp'] + t['fp'] == 0]
    nobody_note = (f' At {nobody[0]:g} the model predicts positive for no row at all, so precision has nothing to divide and we show it as 0.00.' if nobody else '')
    ex_says = [f'{t["th"]:g}' for t in th if ex['p'] >= t['th']]
    p3 = d2(ex['p'])
    if 0 < len(ex_says) < 3:
        s_ = 's' if len(ex_says) > 1 else ''
        no_at = [f'{t["th"]:g}' for t in th if ex['p'] < t['th']]
        row_story = (f'Validation row 3 is an actual positive. Its probability is {p3}, so the model predicts positive at decision threshold{s_} {" and ".join(ex_says)}, and negative at {" and ".join(no_at)}.')
        row_short = f'{vr3.capitalize()} is an actual positive with p = {p3}: predicted positive at {" and ".join(ex_says)}, negative at {" and ".join(no_at)}.'
    elif ex_says:
        row_story = f'Validation row 3 is an actual positive with probability {p3}, and the model predicts positive at all three thresholds.'
        row_short = f'{vr3.capitalize()} is an actual positive with p = {p3}: predicted positive at all three thresholds.'
    else:
        row_story = f'Validation row 3 is an actual positive with probability {p3}, and the model predicts negative at all three thresholds.'
        row_short = f'{vr3.capitalize()} is an actual positive with p = {p3}: predicted negative at all three thresholds.'
    if abs(tmt['f1'] - mt['f1']) < 1e-12:
        model_note = 'On these 15 rows the two models reach the same F1, so we cannot name a winner.'
    elif mt['f1'] > tmt['f1']:
        model_note = f'Logistic regression has the higher F1 here ({d2(mt["f1"])} against {d2(tmt["f1"])}). With 15 rows, read the gap as a hint.'
    else:
        model_note = f'The decision tree has the higher F1 here ({d2(tmt["f1"])} against {d2(mt["f1"])}). With 15 rows, read the gap as a hint.'

    clock = [(10, 'Recall from Class 1'), (35, 'Concepts 1: labels, z-scores, sigmoid'), (30, 'Concepts 2: confusion matrix, thresholds'), (15, 'Break'),
             (70, 'Lab: binary classification, in the notebook'), (15, 'Quiz opens: five questions, open 24 hours'), (5, 'Close and what is assessed')]
    assert sum(m for m, _ in clock) == 180

    s = dict(
        code=code, cohort_name=f['name'], num=2, week=9, when=f['dates'][2] + ', ' + f['slot'], short_title='Classification: yes or no',
        title='Binary classification (yes or no) and how to measure it',
        question=f'Can a binary classifier say yes or no to "{label}", and how do we count its true and false positives and negatives?',
        outcome_head='By the end of today you can',
        outcomes=[f'Turn the {short} into a binary label (positive class or negative class) with a limit', 'Train logistic regression and a decision tree classifier, and work out a confusion matrix and four scores by hand',
                  'Move the decision threshold and explain precision, recall, F1, the ROC curve and AUC in plain words, with the formulas'],
        outcome_icons=['flag', 'gear', 'chart'],
        outcome_note=(f'Here is what you can do by the end of today. You can turn the {short} into a binary label, positive or negative, using a limit. You can train two classifiers, '
                      'and work out their confusion matrix and four scores by hand. And you can move the decision threshold and explain precision, recall, F1, the ROC curve and AUC in plain words, and write the formulas. '
                      'Today ends with a short quiz of five questions that covers Class 1 and Class 2. It opens in the last 20 minutes of the class and stays open for 24 hours, and the lab becomes part B of the first assignment.'),
        clock=clock, plan_title='Your three hours: ideas first, then the lab, then the quiz',
        plan_note=('We have three hours. The first hour and a quarter is concepts only, with no laptop, so you can listen and ask. Then a break. Then the lab, about an hour and ten minutes, '
                   'where you run everything yourself. In the last 20 minutes a short quiz of five questions opens on both classes of Block 1, and it stays open for 24 hours. The ideas come first and the code comes second.'),
        plan_caption='Concepts first, with no laptops. Then the lab, then a short quiz.',
        friday_note='the same deck and the same clock as the Tuesday cohort, because the concepts of this class are new to all three cohorts.',
        recall_from='Class 1',
        recall=[('What is a baseline model for?', 'A baseline model is the simplest possible prediction, here the mean of the training target. Every model must beat it. If a model cannot, it has learned nothing useful.'),
                ('What does the unit of the MAE tell you?', f'The mean absolute error (MAE) is in the unit of the target variable, so an MAE of 2 {unit} means the prediction error is about 2 {unit} on average.'),
                ('Why do we split the rows by equipment group?', f'So that the validation set holds whole {thing} groups the model has never met, which is the situation in real use.')],
        words=[('Binary classification', 'Two possible answers: the positive class (yes, such as "overheating") and the negative class (no). The label is 1 or 0.'),
               ('Decision threshold', 'The probability at or above which the model predicts positive (yes).'),
               ('Confusion matrix', 'A table of actual against predicted classes: TP, FN, FP and TN (true or false, positive or negative).'),
               ('Precision and recall', 'Precision: of the predicted positives, the share that are right. Recall (sensitivity): of the actual positives, the share found.'),
               ('ROC curve and AUC', 'The ROC curve plots true positive rate against false positive rate. AUC, the area under it, is 0 to 1: how well positives rank above negatives.')],
        word_icons=['flag', 'switch', 'grid', 'magnifier', 'chart'],
        words_note=('Five words for today. Binary classification means a model with two possible answers. The positive class is the answer we look for, and the negative class is the other one. '
                    'The decision threshold is the probability at or above which the model predicts positive. A confusion matrix is a table that counts our right and wrong answers. '
                    'Precision and recall are two questions about the positive answers. And the ROC curve and its AUC show how well the model ranks positives above negatives. We use each of them before the break.'),
        keep='Your lab notebook, saved with all cells run in order, and the scores from the confusion matrix and the thresholds.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Saved notebook', value='Restart and run all, then save'), dict(label='Confusion matrix', value='TP, FN, FP and TN'),
                                                              dict(label='Scores', value='Four scores and AUC'), dict(label='Bring next time', value='The same laptop and notebook')]),
        keep_title='Save the notebook and keep your scores',
        next='Class 3: can I trust this model? We test it more carefully.', next_label='Next class',
        keep_note=('Before you go, restart the notebook, run all cells from the top and save it. Keep the confusion matrix and the decision threshold table from your lab, because part B of the assignment builds on them. '
                   'Next class we ask a harder question: can we trust a model, and how would we know if it had only overfitted the training set? Write down any question from today and bring it.'),
        cover_note=(f'Welcome to Class 2. Last week the model gave you a number. Today it answers yes or no, which is called binary classification. We stay with the {thing} data, and the question is whether the {short} reaches its limit. '
                    'You will see how a classifier is built, and the most important lesson of the day: how to count its mistakes. The ideas come first, then the lab, then a short quiz.'),
        slides=[])
    S = s['slides']
    sub4 = ('predicted yes, was yes', 'predicted yes, was no', 'predicted no, was yes', 'predicted no, was no')

    # ------------------------------------------------------------------ concepts
    S.append(dict(kind='table', title='Answers to the three questions from Class 1',
                  headers=['Question', 'Short answer'], rows=[[q, a] for q, a in s['recall']], widths=[4.6, 7.3], icons=False,
                  note='Check your own answer against these before we start today.',
                  notes=('Here are the short answers to the three questions, so you can check yourself and keep them for revision. '
                         'A baseline model is the simplest possible prediction, and every model must beat it. The unit of the MAE is the unit of the target variable, so it tells you the typical size of the prediction error in plain words. '
                         f'And we split by equipment group so that the validation set holds whole {thing} groups the model has never seen. Did your own answer include the reason in each case?')))

    S.append(dict(kind='idea', title=f'Binary classification gives a yes or no answer that tells a {K_["who"]} whether to act',
                  visual=dict(kind='flow', steps=[dict(head='A reading', text=K_['reading'], icon='chart'), dict(head='The model', text=f'Answers yes or no: is it {label}?', icon='robot'),
                                                  dict(head='A person', text=K_['act'], icon='bell')], highlight=1),
                  lead=f'Binary classification has two classes: yes (positive) and no (negative). The question: is it {label}?',
                  points=[f'In Class 1 (regression) the model gave a number, such as the {short} in {unit}.', 'Today the model reads the features and gives one of two classes: yes or no.'],
                  notes=(f'Last week the model gave you a number, for example the {short} in {unit}. A number is useful, but in practice someone has to decide whether to act. '
                         f'So today the question is a yes or no question, which is called binary classification: is it {label}? Yes is the positive class and no is the negative class. A reading arrives, the model says yes or no, and a person acts. '
                         f'For the {thing} data the example is: {K_["act"].lower()}. That is an illustration, and your own plant may do something different. What decision would you attach to a yes in your own field?')))

    S.append(dict(kind='compare', title='Regression predicts a number and classification predicts a class',
                  left=dict(head='Regression', icon='chart', points=[f'The answer is a number in {unit}', 'Class 1: linear regression and a tree', 'Scored by prediction error: MAE and RMSE']),
                  right=dict(head='Classification', icon='flag', points=['The answer is a class: positive or negative', 'Today: logistic regression and a decision tree classifier', 'Scored by counting TP, FN, FP and TN']),
                  verdict='Same data and same split as Class 1. Only the question changes.',
                  notes=('Here is the difference in one slide. In regression the answer is a number, and we measure the size of the prediction error with MAE and RMSE. '
                         'In classification the answer is a class, here positive or negative, and the error is a different thing: the answer is either right or wrong, so we count. '
                         'The data are the same, the split is the same, and the equipment groups are the same. Only the question changes. '
                         'That is why the measures change too, and most of today is about those new measures.')))

    S.append(dict(kind='idea', title=f'A limit on the {short} turns each row into a positive or negative label',
                  visual=dict(kind='scatter', points=pts, xlabel='load_pct (percent)', ylabel=f'{short} ({unit})', hline=lim, hline_label=f'Limit: {limit}', mark=pos_idx),
                  lead=f'The label (target variable) is positive (1, yes) when the {short} is {limit} or more, and negative (0, no) below.',
                  points=[f'Each dot is one row of the training set. Gold dots are positive: {cc["tr_pos"]} of {cc["tr_n"]}.', f'Validation set: {cc["va_pos"]} of {cc["va_n"]} rows are positive.',
                          'The features are still load_pct and ambient_c.'],
                  notes=(f'Here are the training rows again, with load on the bottom and the {short} up the side. The dashed line is the limit, {limit}. '
                         f'A row at or above the line gets the label positive, which is yes, and a row below it gets the label negative, which is no. That rule makes the label. '
                         f'In the training set {cc["tr_pos"]} of {cc["tr_n"]} rows are positive, and in the validation set {cc["va_pos"]} of {cc["va_n"]} are positive. '
                         'The model still sees only load and ambient temperature as features. The label is the answer it must learn to give. Which dots would you worry about most?')))

    S.append(dict(kind='idea', title=f'The majority-class baseline always answers no, is right on {always_pct} percent of rows and finds no actual positive',
                  visual=dict(kind='imbalance', actual=M['actual'], word=label),
                  lead='The majority-class baseline always predicts the more common class, here no. Accuracy is the share of rows answered correctly.',
                  points=[f'Always no is right on {n_neg} of {n_va} validation rows: accuracy {d2(always)}.', f'It finds none of the {n_pos} actual positive rows.', f'A model must beat accuracy {d2(always)} and also find positive rows.'],
                  notes=(f'Look at the validation set. {n_neg} of the {n_va} rows are no, and {n_pos} are yes. A model that says no every time is right on {n_neg} of {n_va} rows, an accuracy of {d2(always)}. '
                         f'That sounds good, yet it finds none of the {n_pos} actual positive cases, and those are the ones we care about. '
                         'This is called the majority-class baseline, because it always predicts the most common class. It is the simplest model, and every real model must beat it. '
                         'The data are imbalanced, which means one class is much rarer than the other, so accuracy cannot be the only measure we use today.')))

    r0 = b['scaling_rows'][0]
    S.append(dict(kind='idea', title='Standardisation (StandardScaler) puts load_pct and ambient_c on the same scale before the model learns',
                  visual=dict(kind='sheet', headers=['load_pct', 'ambient_c', 'load z-score', 'ambient z-score'],
                              rows=[[f'{a:.2f}', f'{b_:.2f}', f'{x:.2f}', f'{y:.2f}'] for a, b_, x, y in b['scaling_rows']], hl=[0, 2]),
                  lead='Standardisation rewrites each feature as a z-score.',
                  points=['A z-score counts how many standard deviations (the typical distance from the mean) a value lies above or below the training mean.', f'Each table row is one training row ({tr1} is first).'],
                  notes=(f'The two features live on different scales. Load runs from about {b["ranges"]["load"][0]:.0f} to {b["ranges"]["load"][1]:.0f}, and ambient temperature from about {b["ranges"]["amb"][0]:.0f} to {b["ranges"]["amb"][1]:.0f}. '
                         'Standardisation rewrites each feature as a z-score, which is how many standard deviations it sits above or below its training mean. The scikit-learn tool is called StandardScaler. '
                         f'Take training row 1: load {r0[0]:.2f} minus the mean {sc["mu"][0]:.2f}, divided by the standard deviation {sc["sd"][0]:.2f}, gives {r0[2]:.2f}. '
                         'The mean and the standard deviation are learned from the training set only, exactly like the median imputation in Class 1. Why must the validation set not help decide them?')))

    S.append(dict(kind='formula', title='The z-score formula: subtract the training mean, then divide by the training standard deviation', size=16,
                  formulas=[('Standardisation (z-score)', r"$x' = \frac{x - \mu}{\sigma}$"),
                            ('Training row 1, load_pct', r"$x_1' = (%.2f - %.2f) / %.2f = %.2f$" % (r0[0], sc['mu'][0], sc['sd'][0], r0[2])),
                            ('Training row 1, ambient_c', r"$x_2' = (%.2f - %.2f) / %.2f = %.2f$" % (r0[1], sc['mu'][1], sc['sd'][1], r0[3]))],
                  symbols=[['x', 'A raw feature value', f'Training row 1: {r0[0]:.2f} % and {r0[1]:.2f} deg C'],
                           ["x'", 'The standardised value (z-score): 0 is the mean, 1 is one standard deviation above', f"Training row 1: x1' = {r0[2]:.2f}, x2' = {r0[3]:.2f}"],
                           ['mu', 'The training mean of that column', f'load {sc["mu"][0]:.2f} %; ambient {sc["mu"][1]:.2f} deg C'],
                           ['sigma', 'The training standard deviation of that column', f'load {sc["sd"][0]:.2f} %; ambient {sc["sd"][1]:.2f} deg C']],
                  widths=[1.2, 5.6, 5.1], note='Subscript 1 is load_pct and 2 is ambient_c. The validation set is standardised with the same mu and sigma.',
                  notes=(f'Here is standardisation in the usual notation. A raw value x, minus the training mean mu, divided by the training standard deviation sigma, gives the z-score x prime. '
                         f'For load, mu is {sc["mu"][0]:.2f} percent and sigma is {sc["sd"][0]:.2f}. For ambient temperature, mu is {sc["mu"][1]:.2f} degrees and sigma is {sc["sd"][1]:.2f}. '
                         f'Training row 1 gives {r0[2]:.2f} for load and {r0[3]:.2f} for ambient temperature. The small numbers 1 and 2 only say which feature we mean. '
                         'Check the load line with your calculator before we go on.')))

    S.append(dict(kind='idea', title='Logistic regression passes a linear score through the sigmoid (logistic) function, which stays between 0 and 1',
                  visual=dict(kind='sigmoid', mark=(ex['z'], ex['p'])),
                  lead='The sigmoid (logistic) function turns any score into a probability from 0 to 1.',
                  points=['A probability of 0.5 means the two classes are equally likely.', 'The decision threshold is the probability at or above which the model predicts positive (yes), and below which it predicts negative (no).'],
                  notes=('Why not use a linear function to predict yes or no? Because a linear function keeps going, below zero and above one, and a probability cannot. '
                         'Logistic regression first builds a score from the features, in the same way as the linear regression in Class 1. Then it passes the score through an S-shaped curve called the sigmoid, or logistic function. '
                         'Very low scores become a probability near 0, very high scores near 1, and a score of 0 becomes exactly 0.5. '
                         'The gold dot is one real row, and we work it out by hand in a moment. Then a decision threshold turns the probability into a prediction.')))

    w0, w1 = M['w']
    parts = [ex['x'][0] * w0, ex['x'][1] * w1]
    zr = M['b'] + sum(round(p_, 2) for p_ in parts)
    assert abs(zr - ex['z']) < 0.0151, 'rounded products do not add up to the score within rounding'
    S.append(dict(kind='formula', title='Logistic regression in three lines: score, probability, prediction', size=16,
                  formulas=[('1  Score', r"$z = b_0 + b_1 x_1' + b_2 x_2'$"), ('2  Probability', r"$p = \frac{1}{1 + e^{-z}}$"),
                            ('3  Prediction', r"$\hat{y} = \mathrm{positive}\ \mathrm{if}\ p \geq t,\ \mathrm{otherwise\ negative}$")],
                  symbols=[['z', 'The score: any number', f'{vr3.capitalize()}: z = {ex["z"]:.2f}'],
                           ['b0', 'Intercept (bias): score at the mean', f'{M["b"]:.2f}'],
                           ['b1, b2', "Weights (coefficients): rise in z per standard deviation", f'b1 = {w0:.2f} (load), b2 = {w1:.2f} (ambient)'],
                           ["x1', x2'", 'Standardised load_pct and ambient_c', f'Validation row 3: {ex["x"][0]:.2f} and {ex["x"][1]:.2f}'],
                           ['p', 'Probability of positive class. e = 2.718', f'Validation row 3: p = {ex["p"]:.2f}'],
                           ['t', 'Decision threshold: predict positive if p is at least t', '0.5 first, then 0.3 and 0.7']],
                  widths=[1.2, 5.6, 5.1],
                  notes=(f'This is the whole of logistic regression in three lines. First the score z: an intercept b zero, plus a weight times each standardised feature. '
                         f'Our learned numbers are an intercept of {M["b"]:.2f}, a weight of {w0:.2f} for load and a weight of {w1:.2f} for ambient temperature. '
                         'Second, the sigmoid function turns the score into a probability p between 0 and 1. Third, the prediction: the class is positive when p is at or above the decision threshold t, and negative otherwise. '
                         'Both weights are positive, so more load or more heat pushes the score toward yes.')))

    fate = 'a true positive (TP)' if dec_ex == 'yes' else 'a false negative (FN)'
    side = 'at or above' if dec_ex == 'yes' else 'below'
    S.append(dict(kind='idea', title=f'Worked example: validation row 3 gets p = {d2(ex["p"])}, so the model predicts {dec_ex}',
                  visual=dict(kind='sheet', headers=['Part', "z-score x'", 'Weight b', 'Product'],
                              rows=[['Intercept b0', '', '', f'{M["b"]:.2f}'], ['load_pct', f'{ex["x"][0]:.2f}', f'{w0:.2f}', f'{parts[0]:.2f}'], ['ambient_c', f'{ex["x"][1]:.2f}', f'{w1:.2f}', f'{parts[1]:.2f}'],
                                    ['Score z (sum)', '', '', f'{ex["z"]:.2f}'], ['Probability p', '', '', f'{ex["p"]:.2f}']], hl=[4, 3]),
                  lead=f'{vr3.capitalize()}: load_pct {ex["raw"][0]:.2f} %, ambient_c {ex["raw"][1]:.2f} deg C. Actual class: positive.',
                  points=[f'p = {d2(ex["p"])} is {side} the threshold 0.5, so the prediction is {dec_ex}: {fate}.',
                          f'One standard deviation more load_pct adds {w0:.2f} to z. One more of ambient_c adds {w1:.2f}.'],
                  notes=(f'This is validation row 3, which is record_id {va_id3} in the file. After standardisation, its load is {ex["x"][0]:.2f} and its ambient temperature {ex["x"][1]:.2f}. '
                         f'Multiply each by its weight, add the intercept of {M["b"]:.2f}, and the score is {ex["z"]:.2f}. The sigmoid turns that into a probability of {d2(ex["p"])}. '
                         f'At the usual decision threshold of 0.5 the model predicts {dec_ex}, and the actual class was positive, so this row is {fate}. '
                         f'Because the features are standardised, one standard deviation more load adds {w0:.2f} to the score and one more of temperature adds {w1:.2f}. The products may differ in the last digit because of rounding.')))

    S.append(dict(kind='idea', title='A decision tree classifier can also answer yes or no, and it does not need standardisation',
                  visual=dict(kind='tree', node=tree_node),
                  lead='A row follows the answers down the tree until it reaches one leaf node, a yellow box.',
                  points=['Each question is an internal node: a split on a feature.', 'A leaf node predicts yes when most training-set rows that ended there are yes.', f'Validation accuracy: {d2(tmt["accuracy"])}.'],
                  notes=('The second model is a decision tree classifier, the same idea as Class 1 with one change at the bottom. In Class 1 each leaf node predicted an average. '
                         'Now each leaf node gives the majority class of the training-set rows that ended there: yes if most of them are yes, otherwise no. '
                         'A row starts at the top, follows the answers to each question, and stops at one leaf node, the yellow box. '
                         f'On the validation set this tree reaches an accuracy of {d2(tmt["accuracy"])}, but accuracy is not the whole story, so we count the mistakes next. Which question comes first?')))

    S.append(dict(kind='list', title='How to read the tree',
                  items=['A leaf node (a yellow box) predicts the majority class of the training-set rows that ended there.',
                         'max_depth is a hyperparameter, a setting chosen before training. It is the largest number of questions (internal nodes) a row can be asked on the way down. Here it is 3.',
                         'A deeper tree can fit the training set so closely that it overfits: it fits the noise. Class 3 tests that.', 'The questions use the real feature values, so a tree needs no standardisation.'],
                  icons=['flag', 'gear', 'lock', 'check'],
                  notes=('Four things to notice about the tree. A leaf node, the yellow box, gives the majority class of the training-set rows that ended there. '
                         'The hyperparameter max_depth is the largest number of questions a row can be asked on the way down, and here it is three. A deeper tree asks more questions and can fit the training set more closely, '
                         'even to the point of overfitting, and Class 3 tests that. Finally, the questions use the real load and temperature, so a tree needs no standardisation. '
                         'Why would a tree not care about the units of load?')))

    S.append(dict(kind='idea', title='The confusion matrix counts true and false positives and negatives',
                  visual=dict(kind='confusion_c2', tp=tp, fp=fp, fn=fn, tn=tn, subs=sub4),
                  lead=f'Logistic regression, decision threshold 0.5, validation set. Positive class: {label}.',
                  points=[f'Each of the {n_va} rows lands in exactly one box.', 'Rows: Actual class. Columns: Predicted class, as in scikit-learn.', 'FP is a false warning. FN is a missed positive.'],
                  notes=(f'Here is the logistic regression on the {n_va} validation rows at decision threshold 0.5. Each row falls into one of four boxes. '
                         f'There are {tp} true positives, TP: the model said yes and it was yes. There are {fn} false negatives, FN: the model said no, but it was yes. There are {fp} false positives, FP: the model said yes, but it was no. '
                         f'And there are {tn} true negatives, TN: the model said no and it was no. The four counts add to {n_va}. '
                         'Rows are the Actual class and columns are the Predicted class, the same layout scikit-learn prints. Everything else today is arithmetic on these four numbers.')))

    P = tp / (tp + fp)
    Rc = tp / (tp + fn)
    assert tp + fp > 0 and abs(P - mt['precision']) < 1e-12 and abs(Rc - mt['recall']) < 1e-12 and abs((tp + tn) / n_va - mt['accuracy']) < 1e-12
    f1_hand = 2 * round(P, 2) * round(Rc, 2) / (round(P, 2) + round(Rc, 2))
    assert abs(f1_hand - mt['f1']) < 0.0051 and abs(2 * tp / (2 * tp + fp + fn) - mt['f1']) < 1e-12
    S.append(dict(kind='formula', title='Accuracy and precision are worked out from the four counts TP, FP, FN and TN', size=16,
                  formulas=[('Accuracy', r"$\mathrm{accuracy} = \frac{TP + TN}{n} = \frac{%d + %d}{%d} = %.2f$" % (tp, tn, n_va, mt['accuracy'])),
                            ('Precision', r"$\mathrm{precision} = \frac{TP}{TP + FP} = \frac{%d}{%d + %d} = %.2f$" % (tp, tp, fp, mt['precision']))],
                  symbols=[['TP', 'True positive: predicted positive, actually positive', pl(tp, 'validation row')], ['FP', 'False positive: predicted positive, actually negative', pl(fp, 'row')],
                           ['FN', 'False negative: predicted negative, actually positive', pl(fn, 'row')], ['TN', 'True negative: predicted negative, actually negative', pl(tn, 'row')],
                           ['n', 'All rows scored: TP + TN + FP + FN', f'{n_va} validation rows']],
                  widths=[1.0, 6.6, 4.3], note='Counts are for logistic regression at decision threshold 0.5.',
                  notes=(f'Now the formulas, with the standard names. TP, FP, FN and TN are the four counts of the confusion matrix. Accuracy is the right answers, TP plus TN, over all n rows: '
                         f'{tp} plus {tn}, over {n_va}, is {d2(mt["accuracy"])}. Precision looks only at the rows where the model predicted positive: TP over TP plus FP, which is {tp} over {tp + fp}, or {d2(mt["precision"])}. '
                         f'Compare the accuracy with the majority-class baseline of {d2(always)}. Which of the four counts does precision ignore?')))

    S.append(dict(kind='formula', title='Recall (sensitivity) and F1: how many actual positives we find, and one blended score', size=16,
                  formulas=[('Recall', r"$R = \mathrm{recall} = \frac{TP}{TP + FN} = \frac{%d}{%d + %d} = %.2f$" % (tp, tp, fn, mt['recall'])),
                            ('F1', r"$F_1 = \frac{2PR}{P + R} = \frac{2 \times %.2f \times %.2f}{%.2f + %.2f} = %.2f$" % (P, Rc, P, Rc, mt['f1']))],
                  symbols=[['R', 'Recall (sensitivity, true positive rate): share of actual positives found', f'{tp} found of {tp + fn} actual positive rows'],
                           ['P', 'Precision: the share of the model\'s positive predictions that are right', f'{d2(P)} (previous slide)'],
                           ['F1', 'The F1 score, a blend of P and R. It is low when either one is low', f'{d2(mt["f1"])}'],
                           ['TP, FN', 'True positives and false negatives (previous slide)', f'{tp} and {fn}']],
                  widths=[1.2, 6.2, 4.5], note=f'Same F1 from the counts: 2TP / (2TP + FP + FN) = {2 * tp} / ({2 * tp} + {fp} + {fn}) = {d2(mt["f1"])}.',
                  notes=(f'Recall asks: of all the rows that are actually positive, how many did we find? That is TP over TP plus FN, which is {tp} over {tp + fn}, or {d2(mt["recall"])}. Recall is also called sensitivity. '
                         f'F1 blends precision P and recall R into one number, two P R over P plus R. With P of {d2(P)} and R of {d2(Rc)} we get {d2(mt["f1"])}. '
                         f'The note shows a second way to write it straight from the counts, and it gives the same {d2(mt["f1"])}. '
                         'F1 is low if either precision or recall is low, so you cannot hide a weak one. Which score would you protect if a false negative is dangerous?')))

    S.append(dict(kind='table', title='The four scores in words: the question each one answers',
                  headers=['Score', 'The question it answers', 'By hand on these counts', 'Result'],
                  rows=[['Accuracy', 'Out of all rows, how often is the prediction right?', f'({tp} + {tn}) / {n_va}', d2(mt['accuracy'])],
                        ['Precision', 'Of the rows the model predicted positive, how many are really positive?', f'{tp} / ({tp} + {fp})', d2(mt['precision'])],
                        ['Recall (sensitivity)', 'Of the rows that are really positive, how many did the model find?', f'{tp} / ({tp} + {fn})', d2(mt['recall'])],
                        ['F1', 'One number that blends precision and recall', f'2 x {d2(P)} x {d2(Rc)} / ({d2(P)} + {d2(Rc)})', d2(mt['f1'])]],
                  widths=[2.1, 4.8, 3.8, 1.2], icons=['check', 'flag', 'magnifier', 'chart'],
                  note=f'Counts: TP {tp}, FN {fn}, FP {fp}, TN {tn}. The majority-class baseline has accuracy {d2(always)}.',
                  notes=(f'Here are the same four scores in plain words, next to the arithmetic you have just seen. Accuracy: how often the prediction is right. Precision: when the model predicts positive, how often it is right. '
                         f'Recall, or sensitivity: of the actual positive cases, how many it found. F1: one number that blends the last two. With your counts they are {d2(mt["accuracy"])}, {d2(mt["precision"])}, {d2(mt["recall"])} and {d2(mt["f1"])}. '
                         f'Notice that accuracy sits above the majority-class baseline of {d2(always)}, but only by a small margin. Please check one line on paper with me before we move on.')))

    S.append(dict(kind='compare', title=f'A false negative and a false positive cost different things for a {thing}',
                  left=dict(head='False negative (FN)', icon='cross', points=['Predicted no, but actually yes.'] + K_['miss'] + ['Every FN lowers recall.']),
                  right=dict(head='False positive (FP)', icon='bell', points=['Predicted yes, but actually no.'] + K_['alarm'] + ['Every FP lowers precision.']),
                  verdict='Here a false negative costs more, so we watch recall.',
                  notes=(f'The two mistakes are not equal. A false negative means the model said no, and the {short} did reach its limit. {" ".join(K_["miss"])} '
                         f'A false positive means the model said yes and nothing happened. {" ".join(K_["alarm"])} '
                         'These descriptions are my illustration, and your own site may weigh them differently. '
                         'The point is that you decide which mistake hurts more before you choose a decision threshold. If false negatives hurt more, you care most about recall. If false positives hurt more, you care most about precision. Which would you protect in your own field?')))

    S.append(dict(kind='table', title=(f'Both models give the same counts on the same {n_va} rows: TP {cm["tp"]}, FN {cm["fn"]}, FP {cm["fp"]}' if cm == tcm else f'Logistic regression and the decision tree give different counts on the same {n_va} rows'),
                  headers=['Measure', 'Logistic regression', 'Decision tree, depth 3', 'Majority-class baseline'],
                  rows=[['True positives (TP)', str(cm['tp']), str(tcm['tp']), '0'], ['False negatives (FN)', str(cm['fn']), str(tcm['fn']), str(n_pos)], ['False positives (FP)', str(cm['fp']), str(tcm['fp']), '0'],
                        ['Accuracy', d2(mt['accuracy']), d2(tmt['accuracy']), d2(always)], ['Precision', d2(mt['precision']), d2(tmt['precision']), '0.00'],
                        ['Recall', d2(mt['recall']), d2(tmt['recall']), '0.00'], ['F1', d2(mt['f1']), d2(tmt['f1']), '0.00']],
                  widths=[2.9, 2.8, 3.0, 3.2], icons=['check', 'cross', 'bell', 'bars', 'flag', 'magnifier', 'chart'],
                  note=model_note + ' Precision of 0.00 for the majority-class baseline means 0 of 0: it never predicts positive.',
                  notes=(f'Here are the two models side by side on the same {n_va} validation rows, with the majority-class baseline for comparison. '
                         f'Logistic regression has {cm["tp"]} true positives and {cm["fn"]} false negatives, with {cm["fp"]} false positives. The tree has {tcm["tp"]} true positives and {tcm["fn"]} false negatives, with {tcm["fp"]} false positives. '
                         f'The baseline has an accuracy of {d2(always)} but finds nothing, so its precision and recall are zero. '
                         f'{model_note} Remember that one row changes these numbers a lot when there are only {n_va} rows.')))

    S.append(dict(kind='idea', title=('Moving the decision threshold changes the precision-recall trade-off: more positives found, more false positives' if trade else f'Moving the decision threshold changes recall, and on these {n_va} rows no threshold adds a false positive'),
                  visual=dict(kind='threshold', probs=M['probs'], actual=M['actual'], ths=[t['th'] for t in th],
                              rows=[f'Threshold {t["th"]:g}: TP {t["tp"]}, FN {t["fn"]}, FP {t["fp"]}, recall {d2(t["recall"])}' for t in th]),
                  lead=('A lower decision threshold raises recall but gives more false positives. This is the precision-recall trade-off.' if trade else 'A lower decision threshold raises recall. Here it adds no false positive, but on other data it usually would.'),
                  points=['Each dot is one validation row. Gold: actual positive. White: actual negative.', row_short],
                  notes=(f'Each dot is one validation row, placed by the probability the model gave it. Gold dots are actual positives and white dots are actual negatives. '
                         f'The dashed lines are three decision thresholds. A row at or above the line is predicted positive. {row_story} '
                         f'Below the picture you can read TP, FN and FP for each threshold. '
                         'Sliding the line left finds more positives, and sliding it right gives fewer false positives. That is the precision-recall trade-off. Where would you put it for your own site?')))

    def trow(t):
        return [f'{t["th"]:g}', str(t['tp']), str(t['fn']), str(t['fp']), d2(t['precision']), d2(t['recall']), d2(t['f1']), d2(t['accuracy'])]
    S.append(dict(kind='table', title='Each decision threshold gives its own counts and its own scores',
                  headers=['Threshold', 'TP', 'FN', 'FP', 'Precision', 'Recall', 'F1', 'Accuracy'],
                  rows=[trow(t) for t in th], widths=[1.7, 1.2, 1.2, 1.2, 1.9, 1.7, 1.4, 1.8], icons=['bell', 'check', 'flag'], hl_col=None,
                  note=('TP: true positives. FN: false negatives. FP: false positives. ' + (f'At {nobody[0]:g} no row is predicted positive, so precision shows 0.00. ' if nobody else '') + note_lo).strip(),
                  notes=(f'These are the three decision thresholds as numbers. {story_lo} {story_hi}{free_lunch}{nobody_note} '
                         'A lower threshold usually raises recall, and a higher one does the opposite. '
                         'So there is no single best threshold, only a best one for the cost of the mistakes at your site.')))

    ill = [(0.2, 10, 27), (0.5, 8, 6), (0.8, 4, 1)]          # illustrative: 10 actual positive rows and 90 actual negative rows
    S.append(dict(kind='table', title='On a larger set, a lower decision threshold finds more positives and also gives more false positives',
                  headers=['Decision threshold', 'TP (of 10 actual positive)', 'FP (of 90 actual negative)', 'True positive rate (TPR)', 'False positive rate (FPR)'],
                  rows=[[f'{a:g}', str(c), str(fa), f'{c / 10:.2f}', f'{fa / 90:.2f}'] for a, c, fa in ill], widths=[1.8, 2.6, 2.8, 2.4, 2.4], icons=['bell', 'check', 'flag'],
                  note='Illustrative example (hypothetical data), not from our data. TPR is the same as recall. Each row of this table becomes one point on a ROC curve.',
                  notes=('This table uses illustrative numbers, made up to show an idea that our 15 rows cannot show for every cohort. Imagine a larger set with 10 actual positive rows and 90 actual negative rows. '
                         'At a low decision threshold of 0.2 the model finds all 10, but it also gives 27 false positives. At a high threshold of 0.8 it gives only 1 false positive, but it finds just 4 of the 10. '
                         'The two right-hand columns are the true positive rate, the share of actual positives found, which is recall, and the false positive rate, the share of actual negatives wrongly flagged positive. '
                         'Each row becomes one point on the ROC curve in a moment. Which row would you choose if a false negative is dangerous?')))

    roc_marks = []
    top_n = 0
    pairs_xy = []
    for t in th:
        fpr = t['fp'] / (t['fp'] + t['tn'])
        tpr = t['tp'] / (t['tp'] + t['fn'])
        pairs_xy.append((f'{fpr:.2f}', f'{tpr:.2f}'))
        if tpr > 0.9:
            dy = -0.3 - 0.4 * top_n
            top_n += 1
        else:
            dy = 0.15 if tpr < 0.05 else -0.28
        roc_marks.append(dict(x=fpr, y=tpr, label=f'threshold {t["th"]:g}', dy=dy, dx=1.0 if tpr < 0.05 else 0.25))
    fpr5, tpr5 = fp / (fp + tn), tp / (tp + fn)
    spec5 = tn / (tn + fp)
    S.append(dict(kind='formula', title='Two rates give the points of the ROC curve: the false positive rate (FPR) and the true positive rate (TPR)', size=16,
                  formulas=[('False positive rate (at 0.5)', r"$\mathrm{FPR} = \frac{FP}{FP + TN} = \frac{%d}{%d + %d} = %.2f$" % (fp, fp, tn, fpr5)),
                            ('True positive rate (at 0.5)', r"$\mathrm{TPR} = \frac{TP}{TP + FN} = \frac{%d}{%d + %d} = %.2f$" % (tp, tp, fn, tpr5))],
                  symbols=[['FPR', 'False positive rate: share of actual negatives (FP + TN) predicted positive', f'{fp} of {fp + tn} actual negative rows'],
                           ['TPR', 'True positive rate: share of actual positives (TP + FN) found. Same as recall', f'{tp} of {tp + fn} actual positive rows'],
                           ['Specificity', 'True negative rate: TN / (TN + FP). Equals 1 - FPR', f'{tn} of {fp + tn} = {spec5:.2f}']],
                  widths=[1.6, 6.2, 4.1], note='Points (FPR, TPR) at thresholds 0.3, 0.5 and 0.7: ' + ', '.join(f'({a}, {c})' for a, c in pairs_xy) + '.',
                  notes=(f'The ROC curve needs two rates. The false positive rate, FPR, is FP over FP plus TN: of all the rows that are actually negative, what share did we wrongly flag as positive. At decision threshold 0.5 that is {fp} over {fp + tn}, or {fpr5:.2f}. '
                         f'The true positive rate, TPR, is the same thing as recall, also called sensitivity: {tp} over {tp + fn}, or {tpr5:.2f}. Specificity is the share of actual negatives we clear correctly, which is one minus FPR. '
                         'Each threshold gives one pair of rates, and each pair is one point on the ROC graph that follows. Why is a low FPR good, and a high TPR good?')))

    auc_text = f'{wins} of {pairs} pairs'
    perfect = f' A perfect score on {n_va} rows is a warm hint, and it promises nothing about new equipment.' if auc >= 0.999 else ''
    n_pts = len(b['roc'])
    S.append(dict(kind='idea', title='The ROC curve plots one point for every decision threshold: FPR across, TPR up',
                  visual=dict(kind='roc_real', points=b['roc'], auc=auc, marks=roc_marks),
                  lead='ROC is short for receiver operating characteristic. It is a graph with one point per decision threshold.',
                  points=[f'Each black dot is one threshold. {n_va} validation rows give only {n_pts} points, so the line is a staircase.', 'The three red dots are our thresholds 0.3, 0.5 and 0.7 from the table. The gold area under the line is the AUC.'],
                  notes=(f'The ROC curve is a graph, and ROC stands for receiver operating characteristic. For every decision threshold we work out two rates and plot one point: the false positive rate across, and the true positive rate up. '
                         f'The black dots are every threshold that changes a prediction on our rows. We have only {n_va} rows, so there are only {n_pts} points, and the line climbs in steps like a staircase. '
                         'The three red dots are the thresholds 0.3, 0.5 and 0.7 from the table. A curve that hugs the top left corner is good, because it finds many positives with few false positives. The dashed line is random guessing. '
                         f'The area under the line is the AUC, here {d2(auc)}. Why does our curve have so few points?')))

    S.append(dict(kind='idea', title='AUC is the area under the ROC curve, and on a large dataset the curve is smooth',
                  visual=dict(kind='roc_smooth'),
                  lead='AUC (area under the curve) is the chance that an actual positive row scores higher than an actual negative row.',
                  points=[f'Ours: {pairs} pairs ({n_pos} x {n_neg}), and {auc_text} are in the right order: AUC {d2(auc)}.', 'The curve is illustrative. With thousands of rows it looks smooth. AUC 0.5 is random guessing.'],
                  notes=(f'Here is what the AUC means in words. Take one actual positive row and one actual negative row. AUC is the chance that the model gives the positive row the higher probability. '
                         f'We have {n_pos} positive rows and {n_neg} negative rows, so {pairs} pairs, and {wins} of them are in the right order. That gives {d2(auc)}.{perfect} '
                         'The curve in the picture is illustrative. On a large dataset there are thousands of thresholds, the dots sit almost on top of each other, and the staircase becomes a smooth curve. '
                         'An AUC of 0.5 is a coin flip, and 1.0 is perfect. Why is this score independent of any single decision threshold?')))

    S.append(dict(kind='list', title=f'With {n_va} rows and {n_pos} actual positives, every score here is shaky',
                  items=[f'The validation set has {n_va} rows and only {n_pos} actual positive rows.', f'If one prediction changed, recall would move by {d2(1 / n_pos)} and accuracy by {d2(1 / n_va)}.',
                         'These numbers teach you how the scores work. They are too few to prove which model is better.', 'Class 3 shows how to test a model with more care.'],
                  icons=['cross', 'calculator', 'lock', 'book'],
                  notes=(f'I want to be careful about the limits. The validation set has only {n_va} rows and {n_pos} of them are actual positives. '
                         f'If the model got one more positive right, the recall would move by {d2(1 / n_pos)}. If it got one more row right, the accuracy would move by {d2(1 / n_va)}. '
                         'So the numbers on these slides are good for learning the scores, and weak as proof that one model beats another. '
                         'Next class we look at tests that use more rows and give us more reason to trust a number. Keep that caution in mind in the lab.')))

    S.append(dict(kind='list', title='Summary: judge a binary classifier by counting each kind of mistake',
                  items=['Make a label from the target with a limit: positive class or negative class.', 'Standardise the features. Logistic regression turns a score into a probability with the sigmoid function.',
                         'A decision threshold turns the probability into a predicted class.', 'Count TP, FP, FN and TN, then work out accuracy, precision, recall and F1.', 'Move the decision threshold, or read the ROC curve and AUC, to balance recall against precision.'],
                  icons=['flag', 'switch', 'bell', 'grid', 'chart'],
                  notes=('Here is the whole class in five lines. Make a label from the target with a limit. Standardise the features, and let logistic regression turn a score into a probability. '
                         'Use a decision threshold to turn the probability into a predicted class. Count the answers in a confusion matrix, and work out accuracy, precision, recall and F1. '
                         'Then move the threshold, or read the ROC curve and AUC, to balance one kind of mistake against the other. Always compare with the majority-class baseline. '
                         'If you can say these five lines in your own words, you are ready for the lab.')))

    S.append(dict(kind='code', title='Read the workflow before you write it: impute, standardise, fit, predict probabilities, count',
                  code='imputer = SimpleImputer(strategy="median")\nX_train = imputer.fit_transform(train_features)\nX_valid = imputer.transform(valid_features)\nmodel = make_pipeline(StandardScaler(),\n                      LogisticRegression())\nmodel.fit(X_train, y_train)\ny_proba = model.predict_proba(X_valid)[:, 1]\nthreshold = 0.5\ny_pred = (y_proba >= threshold).astype(int)\ncm = confusion_matrix(y_valid, y_pred)',
                  reads=['The imputer fills each missing value (NaN) with the training median (imputation).', 'The pipeline chains StandardScaler and LogisticRegression.',
                         'predict_proba gives a probability per class. Column 1 is the positive class.', 'y_proba >= threshold gives True or False. astype(int) makes it 1 or 0: y_pred.',
                         'confusion_matrix puts Actual down the side and Predicted across the top, negative first: TN and FP in the top row, FN and TP below.'],
                  notes=('Before we leave the concepts, look at the workflow. The imputer, SimpleImputer, fills missing values, here with the training median, so a missing value cannot stop the model. X_train is the table of training features, and y_train is the column of labels. '
                         'Chain StandardScaler and the logistic regression in one pipeline. Fit it, which learns the means, the standard deviations and the weights from the training set only. '
                         'Then ask for probabilities, and keep the column for the positive class. Compare each probability with the threshold, here 0.5, to get y_pred, the predicted class. And count the answers in a confusion matrix, cm. '
                         'It has the same layout as our slide: Actual down the side, Predicted across the top. If you can read these lines aloud in plain words, you are ready.')))

    # ------------------------------------------------------------------ lab
    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook. You use the same engineering_data.csv file as in Class 1.', section='Lab',
                  notes=('That is the end of the concepts. Everything you need is on the slides you have just seen, and every term is explained again inside the notebook. '
                         'Please open the notebook now, and keep the slides closed except for the check slides at the end of the deck. I will walk around. Raise your hand if a cell gives an error. '
                         'Run the cells in order from the top, and write your prediction before you run each cell.')))

    S.append(dict(kind='steps', title='The lab notebook has five stages, and each stage ends with a check',
                  steps=[dict(head='Step 1: prepare', text='Load, clean, split, impute the missing value', icon='folder'), dict(head='Step 2: label', text=f'Make the label for {label} and the majority-class baseline', icon='flag'),
                         dict(head='Steps 3 and 4: models', text='Logistic regression, then a decision tree', icon='gear'), dict(head='Step 5: count', text='Confusion matrix and four scores', icon='grid'),
                         dict(head='Steps 6 and 7: thresholds', text='Move the decision threshold, draw the ROC curve', icon='chart')], highlight=3,
                  caption='Predict first, run second, then read the output. CHANGE tasks: steps 3 and 6. Steps 8 and 9: conclusion and saving.',
                  notes=('Here are the five stages of the lab. One, prepare the data as in Class 1: load, clean, split by group and impute the missing value. Two, make the label from the target with the limit. '
                         'Three and four, train the logistic regression with standardisation and the decision tree classifier. Five, count the answers in a confusion matrix and work out the four scores. '
                         'Six and seven, move the decision threshold, and draw the ROC curve. Two CHANGE tasks wait for you: remove the standardisation and watch the weights change, and move the threshold. '
                         'Predict first, then run, then read. That rhythm is how you find out what you understand.')))

    rows_chk = [['Positive labels: training set, validation set', f'{cc["tr_pos"]} of {cc["tr_n"]}, {cc["va_pos"]} of {cc["va_n"]}'],
                ['Majority-class baseline accuracy', d2(always)],
                ['Learned weights (coefficients): load_pct, ambient_c, and the intercept', f'{lg["w"][0]:.2f}, {lg["w"][1]:.2f}, {lg["b"]:.2f}'],
                ['Logistic regression: TP, FN, FP, TN', f'{tp}, {fn}, {fp}, {tn}'],
                ['Logistic regression: accuracy, precision, recall, F1', f'{d2(mt["accuracy"])}, {d2(mt["precision"])}, {d2(mt["recall"])}, {d2(mt["f1"])}'],
                ['Decision tree: TP, FN, FP, TN', f'{tcm["tp"]}, {tcm["fn"]}, {tcm["fp"]}, {tcm["tn"]}'],
                ['Logistic regression recall at decision thresholds 0.3, 0.5, 0.7', f'{d2(t3["recall"])}, {d2(t5["recall"])}, {d2(t7["recall"])}'],
                ['AUC', d2(auc)]]
    S.append(dict(kind='table', title='Check your numbers against these before you move on',
                  headers=['What to check (validation set)', 'You should see'], rows=rows_chk, widths=[7.0, 4.0],
                  icons=['flag', 'cross', 'gear', 'grid', 'check', 'grid', 'switch', 'chart'],
                  note='If your number differs, stop and ask. Do not change a number to match. Find the step that went wrong.',
                  notes=('Use this table as your checkpoint. If your numbers match, you can carry on. If they do not, stop and call me over, because each step builds on the one before. '
                         'The usual reasons are a cell run out of order, or a missing value imputed with the wrong median. Notice that all your numbers should match this table exactly, because we all use the same split and the same settings. '
                         'Do not edit a number to make it match. Find out why it differs. That habit will serve you in every project.')))

    S.append(dict(kind='table', title='Four messages you will meet, what they mean and what to do',
                  headers=['Message', 'What it says', 'What to do'],
                  rows=[['ValueError: contains NaN', 'A missing value (NaN) reached StandardScaler or the model', 'Run the imputation step (SimpleImputer with the training median)'],
                        ['Classification metrics can\'t handle a mix of binary and continuous targets', 'You gave probabilities where a predicted class (0 or 1) was needed', 'Compare y_proba with the threshold first, to get y_pred'],
                        ['ConvergenceWarning', 'The model stopped before it finished learning. The cell still runs', 'Standardise the features, or raise max_iter'],
                        ['NameError', 'A cell above has not been run yet', 'Run all cells from the top, in order']],
                  widths=[4.4, 3.8, 4.4], icons=['cross', 'key', 'bell', 'flag'],
                  notes=('Messages are normal, and reading them is a skill. Here are the four you will most likely meet today. A NaN error means a missing value reached the model, so run the imputation step. '
                         'The long message about binary and continuous targets means you gave the metric a probability where it needed a predicted class, so compare the probability with the threshold first. '
                         'A convergence warning is only a warning, and it appears when features are not standardised. And a name error means you skipped a cell above. Read the last line of any message first.')))

    S.append(dict(kind='list', title='How this class counts towards your coursework',
                  items=['Block 1 is Class 1 and Class 2.', 'Assignment part A (A7, regression) comes from the Class 1 lab. Part B (A8, classification) comes from today\'s lab.',
                         f'The Block 1 assignment closes on {C.COHORTS[code]["b1_close"]} (Kampala time).', 'A short quiz of five questions covers both classes. It opens in the last 20 minutes of today\'s class and stays open for 24 hours.'],
                  icons=['folder', 'doc', 'clock', 'bell'],
                  notes=('A word on how this counts. Block 1 is Class 1 and Class 2 together. The assignment has two parts. Part A is on regression and comes from the lab you did last time, and part B is on classification and comes from today\'s lab. '
                         f'Both parts close on {C.COHORTS[code]["b1_close"]}, Kampala time. There is a short quiz of five questions covering both classes. It opens in the last twenty minutes of the class today and stays open for twenty-four hours. Keep your saved notebooks.')))

    # ------------------------------------------------------------------ facilitator
    s['facilitator'] = dict(
        prep=['Open the deck in Slide Show mode and the lab notebook in Colab before anyone arrives. Run the notebook from the top once on your account.',
              'Put the lab notebook and engineering_data.csv in the shared class folder and post the link. Every learner needs both files in Colab, in the Files panel.',
              'Write the "check your numbers" table on the board before the lab (the numbers for each cohort are in the table below).',
              'Bring the Block 1 quiz paper. The quiz opens in the last 20 minutes of this class, stays open for 24 hours, has five questions and covers Class 1 and Class 2. Learners sit it in class. The paper itself is not part of this deck.',
              'Check the deadline and the form of the assignment before you confirm them in writing. They are not decided in this guide.'],
        misconceptions=[('High accuracy means a good model', f'On the validation set the majority-class baseline (always predict no) already scores {d2(always)}. Compare with that baseline and look at recall.'),
                        ('The model says yes when the probability is high, so the decision threshold is always 0.5', '0.5 is a default. The right decision threshold depends on the cost of a false negative and of a false positive.'),
                        ('Standardisation changes the answer of the model', 'It changes the units of the weights. The probabilities of this model stay almost the same, and the weights become comparable.'),
                        ('An AUC of 1.0 means the model is perfect', f'It means every actual positive scored above every actual negative in these {n_va} rows. New equipment can behave differently.')],
        probes=[('What does a false positive cost for your equipment?', 'Answers differ. Listen for a cost in time or energy, and compare it with the cost of a false negative.'),
                ('Why is accuracy alone not enough?', f'With few positive cases, the majority-class baseline scores {d2(always)} and finds none of them.'),
                ('When is precision the more important score?', 'When a false positive is expensive, for example an unnecessary stop.'),
                ('When is recall the more important score?', 'When a false negative is dangerous or expensive, for example an overheating motor.'),
                ('What happens to recall if you lower the decision threshold?', f'It rises or stays the same. In the {thing} data it goes from {d2(t5["recall"])} at 0.5 to {d2(t3["recall"])} at 0.3.'),
                ('Why do we fit StandardScaler on the training set only?', 'If the validation set helped decide the mean and the standard deviation, information would leak from held-out data into the model. That is data leakage.'),
                ('Does the decision tree need standardisation?', 'No. A tree only asks whether a value is above or below a threshold, and standardisation does not change the order of the values.'),
                ('What does an AUC of 0.5 mean?', 'The model ranks positive and negative cases no better than a coin flip.')],
        lab_steps=[('Step 1: prepare', f'Rows after cleaning {b["n_clean"]}. Split {b["n_tr"]}, {b["n_va"]}, {b["n_te"]}. The same cleaning and split as Class 1, repeated.'),
                   ('Step 2: label', f'Training {cc["tr_pos"]} of {cc["tr_n"]} are positive, validation {cc["va_pos"]} of {cc["va_n"]}. Majority-class baseline accuracy {d2(always)}.'),
                   ('Step 3: logistic regression', f'Weights {lg["w"][0]:.2f} and {lg["w"][1]:.2f}, intercept {lg["b"]:.2f}. The CHANGE task removes StandardScaler. The weights become small, because each weight now belongs to one percent of load or one degree of ambient temperature and no longer to one standard deviation. A ConvergenceWarning may appear.'),
                   ('Step 4: decision tree', f'Depth 3. TP {tcm["tp"]}, FN {tcm["fn"]}, FP {tcm["fp"]}.'),
                   ('Step 5: confusion matrix and scores', f'TP {tp}, FN {fn}, FP {fp}, TN {tn}. Accuracy {d2(mt["accuracy"])}, precision {d2(mt["precision"])}, recall {d2(mt["recall"])}, F1 {d2(mt["f1"])}. Ask one learner to repeat one division at the board.'),
                   ('Step 6: decision thresholds', f'{story_lo} {story_hi}{nobody_note}'),
                   ('Step 7: ROC curve and AUC', f'AUC {d2(auc)}, which is {wins} of {pairs} pairs in the right order. Ask what a score this high on 15 rows promises.'),
                   ('Steps 8 and 9: conclusion and save', 'Three sentences from every learner. Insist on restart and run all before saving.')],
        rescue=['If the concepts run over, skip the slide that compares the two models and say the results in one sentence. Keep the confusion matrix, the four scores and the decision threshold slides.',
                'If only 45 minutes of lab remain, do steps 1 to 5 and the threshold step. Set the decision tree and the ROC curve as practice for next time.',
                'If the quiz time is under pressure, shorten the lab by dropping the decision tree. The quiz covers both classes and must still happen today.',
                'If wifi fails in the room, use the offline set-up from Week 2: the notebook runs unchanged in VS Code.',
                'If several learners are stuck at the same cell, stop the room, run that cell on the projector and let them copy the fix.'],
        after=['Share the lab notebook and engineering_data.csv again so absent learners can follow.', 'Confirm in writing the deadline and the form of the Block 1 assignment. Do not give a date before it is decided.',
               'Note any question you could not answer and start Class 3 with it.'])
    s['numbers_fn'] = 'numbers'
    return s


def numbers(F):
    """Rows of cohort numbers for the guide: F maps cohort code to facts."""
    codes = list(F)

    def row(label, g):
        return [label] + [g(F[c]) for c in codes]
    d = lambda v: f'{v:.2f}'
    return [row('Label limit', lambda f: f'{f["b"]["limit"]:g} {f["unit"]}'),
            row('Positive labels, training set', lambda f: f'{f["b"]["cls_counts"]["tr_pos"]} of {f["b"]["cls_counts"]["tr_n"]}'),
            row('Positive labels, validation set', lambda f: f'{f["b"]["cls_counts"]["va_pos"]} of {f["b"]["cls_counts"]["va_n"]}'),
            row('Majority-class baseline accuracy', lambda f: d(f['b']['always_no_acc'])),
            row('Logistic weights: load, ambient, intercept', lambda f: f'{f["b"]["logit"]["w"][0]:.2f}, {f["b"]["logit"]["w"][1]:.2f}, {f["b"]["logit"]["b"]:.2f}'),
            row('Logistic: TP, FN, FP, TN', lambda f: '{tp}, {fn}, {fp}, {tn}'.format(**f['b']['logit_conf'])),
            row('Logistic: accuracy, precision, recall, F1', lambda f: ', '.join(d(f['b']['logit_metrics'][k]) for k in ('accuracy', 'precision', 'recall', 'f1'))),
            row('Decision tree depth 3: TP, FN, FP, TN', lambda f: '{tp}, {fn}, {fp}, {tn}'.format(**f['b']['tree_conf'])),
            row('Decision tree depth 3: accuracy, precision, recall, F1', lambda f: ', '.join(d(f['b']['tree_metrics'][k]) for k in ('accuracy', 'precision', 'recall', 'f1'))),
            row('Recall at decision thresholds 0.3, 0.5, 0.7', lambda f: ', '.join(d(t['recall']) for t in f['b']['thresholds'])),
            row('FP at decision thresholds 0.3, 0.5, 0.7', lambda f: ', '.join(str(t['fp']) for t in f['b']['thresholds'])),
            row('AUC', lambda f: d(f['b']['auc']))]
