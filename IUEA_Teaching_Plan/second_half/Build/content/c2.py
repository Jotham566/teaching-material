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
                    miss=['Energy per tonne runs high unseen.', 'Energy is wasted.'], alarm=['The control room plans for demand that never comes.', 'It costs some time.'],
                    miss_line='Demand arrives with no warning', verb='reaches'),
    'CML3111': dict(label='overheating', reading='Load and air temperature at one motor', act='Yes: raise a warning and check cooling', who='maintenance team',
                    miss=['A winding overheats with no warning.', 'The insulation can be damaged.'], alarm=['Someone checks a healthy motor.', 'It costs some time.'],
                    miss_line='A winding overheats unseen', verb='reaches'),
}


MISSED_COST, FALSE_ALARM_COST = 5, 1      # invented teaching costs (decision of 12 November): a false negative costs five times a false positive


def _leaf_counts(t, X):
    """How many training rows end in each leaf (keyed by id of the leaf tuple)."""
    out = {}
    for x in np.asarray(X, float):
        n = t
        while n[0] == 'split':
            n = n[3] if x[n[1]] <= n[2] else n[4]
        out[id(n)] = out.get(id(n), 0) + 1
    return out


def _tree_cls(t, names, counts):
    if t[0] == 'leaf':
        k = counts.get(id(t), 0)
        return {'v': ('yes' if t[1] >= 0.5 else 'no') + f' ({k})'}
    return {'q': f'{names[t[1]]} <= {float(t[2]):.2f}?', 'yes': _tree_cls(t[3], names, counts), 'no': _tree_cls(t[4], names, counts)}


def roc_points_sklearn(actual, score):
    """Number of points scikit-learn's roc_curve returns with its default drop_intermediate=True (the corner points of the staircase).
    Same rule as scikit-learn 1.9: keep a threshold only where the line bends, then add the (0, 0) start."""
    a = np.asarray(actual, int)
    s = np.asarray(score, float)
    ths = np.unique(s)[::-1]
    fps = np.array([((s >= t) & (a == 0)).sum() for t in ths])
    tps = np.array([((s >= t) & (a == 1)).sum() for t in ths])
    keep = np.where(np.r_[True, np.logical_or(np.diff(fps, 2), np.diff(tps, 2)), True])[0]
    return len(keep) + 1


def gd_path(Xs, y, lr=0.5, steps=500, C_=1.0):
    """Plain gradient descent on the mean log loss plus scikit-learn's L2 penalty (weights only, scaled to the mean form: w^2 / (2 C n)).
    Returns [(step, mean log loss, b0, b1, b2)] for every step."""
    A = np.column_stack([np.ones(len(Xs)), np.asarray(Xs, float)])
    th = np.zeros(A.shape[1])
    n = len(y)
    out = []
    for k in range(steps + 1):
        p = 1 / (1 + np.exp(-A @ th))
        out.append((k, float(np.mean(-(y * np.log(p) + (1 - y) * np.log(1 - p)))), *[float(v) for v in th]))
        g = A.T @ (p - y) / n
        g[1:] += th[1:] / (C_ * n)
        th = th - lr * g
    return out


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
    # log loss: the worked rows are validation row 3 (an actual positive) and the actual negative with the highest probability
    neg = [i for i in range(len(lva)) if lva[i] == 0]
    kn = max(neg, key=lambda i: pr[i])
    rowloss = lambda i: float(-np.log(pr[i]) if lva[i] == 1 else -np.log(1 - pr[i]))
    ptr = R.logreg_proba(b0, w, Xs)
    train_ll = float(np.mean(-(ltr * np.log(ptr) + (1 - ltr) * np.log(1 - ptr))))
    # gradient descent with the same penalty reaches scikit-learn's weights
    path = gd_path(Xs, ltr)
    assert abs(path[-1][2] - b0) < 5e-3 and np.allclose(path[-1][3:], w, atol=5e-3), 'gradient descent did not reach the scikit-learn weights'
    g0 = [float(np.mean(0.5 - ltr)), float(np.mean((0.5 - ltr) * Xs[:, 0])), float(np.mean((0.5 - ltr) * Xs[:, 1]))]
    # no StandardScaler: same penalty on raw units (the Lab 2 CHANGE task)
    braw, wraw = R.logreg_fit(f['trf'].to_numpy(float), ltr)
    praw = R.logreg_proba(braw, wraw, f['vaf'].to_numpy(float))
    raw = dict(b=float(braw), w=[float(v) for v in wraw], conf=R.confusion(lva, (praw >= 0.5).astype(int)), maxdiff=float(np.max(np.abs(praw - pr))))
    cost = []
    for th in (0.3, 0.5, 0.7):
        c = R.confusion(lva, (pr >= th).astype(int))
        cost.append(dict(th=th, **c, **R.prf(c), cost=MISSED_COST * c['fn'] + FALSE_ALARM_COST * c['fp']))
    best = min(cost, key=lambda r: (r['cost'], -r['th']))          # lowest cost; a tie goes to the higher threshold
    low = {th: R.confusion(lva, (pr >= th).astype(int)) for th in (0.1, 0.2)}
    tree = R.tree_clf_fit(f['trf'], ltr, 3)
    counts = _leaf_counts(tree, f['trf'])
    return dict(probs=[float(p) for p in pr], actual=[int(v) for v in lva], ex=ex, mu=mu, sd=sd, b=float(b0), w=[float(v) for v in w], lim=lim,
                kn=kn, loss=rowloss, train_ll=train_ll, path=path, g0=g0, raw=raw, cost=cost, best=best, low=low, tree=tree, counts=counts,
                roc_sk=roc_points_sklearn(lva, pr), sd_sample=[float(v) for v in f['trf'].std(ddof=1).to_numpy()])


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
    tree_node = _tree_cls(M['tree'], names, M['counts'])
    n_one = sum(1 for v in M['counts'].values() if v == 1)
    leaf_line = (f'{n_one} leaf node{"s rest" if n_one != 1 else " rests"} on one row: a sign of overfitting.'
                 if n_one else 'Every leaf node rests on two or more training rows.')
    leaf_spoken = (f'Look at the numbers in brackets: they count the training rows that ended in each leaf node. {n_one} of the leaves hold{"s" if n_one == 1 else ""} only one training row, so that rule rests on a single example. '
                   'Do not read such a rule as physics. The tree has fitted one row, which is a first sign of overfitting, and Class 3 tests it.' if n_one else '')

    # ---- decision threshold story, built from the reference table
    def chg(a, b_, what):
        pl_ = what.split(' (')[0].endswith('s')
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

    # ---- cost of mistakes, how logistic regression learns, the threshold below 0.3
    best = M['best']
    bth = f'{best["th"]:g}'
    costs = {f'{r["th"]:g}': r['cost'] for r in M['cost']}
    low_fp = next(((t_, M['low'][t_]['fp']) for t_ in (0.2, 0.1) if M['low'][t_]['fp'] > t3['fp']), None)
    if not trade:
        free_lunch = (f' None of the thresholds 0.3, 0.5 and 0.7 adds a false positive on these {n_va} rows.'
                      + (f' A lower threshold does: at {low_fp[0]:g} there are {low_fp[1]} false positives, and the CHANGE task in the lab shows it.' if low_fp else ''))
    sd0, sd1 = sc['sd']
    mu0, mu1 = sc['mu']
    ss0, ss1 = M['sd_sample']
    w0, w1 = M['w']
    kn = M['kn']
    pr3, prn = M['probs'][ex['k']], M['probs'][kn]
    l3 = -np.log(round(pr3, 2))                        # by hand from the rounded probability
    ln_ = -np.log(1 - round(prn, 2))
    assert abs(l3 - M['loss'](ex['k'])) < 0.015 and abs(ln_ - M['loss'](kn)) < 0.015, 'hand log loss differs from the exact one'
    vrn = f'validation row {kn + 1}'
    path = M['path']
    g0 = M['g0']
    n_tr = cc['tr_n']
    gd_end = path[-1]
    raw = M['raw']
    rc = raw['conf']
    raw_same = rc == cm
    raw_line = ('the confusion matrix at 0.5 stays the same' if raw_same else
                f'the confusion matrix at 0.5 changes from TP {tp}, FN {fn}, FP {fp} to TP {rc["tp"]}, FN {rc["fn"]}, FP {rc["fp"]}')
    load_vals = f['trf'].load_pct.to_numpy(float)
    in_band = int(np.sum(np.abs(load_vals - mu0) <= sd0))

    clock = [(10, 'Recall from Class 1'), (40, 'Concepts 1: labels, spread, how a classifier learns'),
             (35, 'Concepts 2: counting and pricing mistakes'), (15, 'Break'),
             (60, 'Lab: binary classification, in the notebook'), (15, 'Quiz opens: forms Q7 and Q8, 24 hours'), (5, 'Close and what is assessed')]
    assert sum(m for m, _ in clock) == 180

    s = dict(
        code=code, cohort_name=f['name'], num=2, week=9, when=f['dates'][2] + ', ' + f['slot'], short_title='Classification: yes or no',
        title='Binary classification (yes or no) and how to measure it',
        question=f'Can a binary classifier say yes or no to "{label}", how does it learn, and how do we count and price its mistakes?',
        outcome_head='By the end of today you can',
        outcomes=[f'Turn the {short} into a binary label with a limit, and standardise the features with the mean and standard deviation',
                  'Train logistic regression and a decision tree classifier, and explain how logistic regression learns: log loss and gradient descent',
                  'Count TP, FN, FP and TN, work out precision, recall and F1, and choose a decision threshold with a cost table'],
        outcome_icons=['flag', 'gear', 'chart'],
        outcome_note=(f'Here is what you can do by the end of today. You can turn the {short} into a binary label using a limit, and standardise the features using the mean and the standard deviation. '
                      'You can train two classifiers and explain how logistic regression learns, with log loss and gradient descent. '
                      'And you can count the four kinds of answer, work out precision, recall and F1, and choose a decision threshold from a cost table. '
                      'In the last 20 minutes the Block 1 quiz opens online, and part B of the Block 1 assignment repeats today\'s lab.'),
        clock=clock, plan_title='Your three hours: ideas first, then the lab, then the quiz',
        plan_note=('We have three hours. The first hour and a half is concepts only, with no laptop, so you can listen and ask. Then a break. Then the lab, about an hour, '
                   'where you run everything yourself. In the last 20 minutes the Block 1 quiz opens online as two short forms, Q7 on Class 1 and Q8 on Class 2, and each stays open for 24 hours. '
                   'The ideas come first and the code comes second.'),
        plan_caption='Concepts first, with no laptops. Then the lab, then the quiz.',
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
        keep='Your lab notebook, saved with all cells run in order, and the confusion matrix and the cost table from the lab.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Saved notebook', value='Restart and run all, then save'), dict(label='Confusion matrix', value='TP, FN, FP and TN'),
                                                              dict(label='Cost table', value='Thresholds 0.3, 0.5 and 0.7'), dict(label='Bring next time', value='The same laptop and notebook')]),
        keep_title='Save the notebook and keep your cost table',
        next='Class 3: can I trust this model? We test it more carefully.', next_label='Next class',
        keep_note=('Before you go, restart the notebook, run all cells from the top and save it. Keep the confusion matrix and the cost table from your lab, because part B of the assignment builds on them. '
                   'Next class we ask a harder question: can we trust a model, and how would we know if it had only overfitted the training set? Write down any question from today and bring it.'),
        cover_note=(f'Welcome to Class 2. Last week the model gave you a number. Today it answers yes or no, which is called binary classification. We stay with the {thing} data, and the question is whether the {short} reaches its limit. '
                    'You will see how a classifier is built, how it learns from its errors, and the most important lesson of the day: how to count its mistakes and put a price on them. The ideas come first, then the lab, then the quiz.'),
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
                  points=[f'In Class 1 (regression) the model gave a number, such as the {short} in {unit}, scored by MAE.', 'Today it gives one of two classes, and we count its right and wrong answers.'],
                  notes=(f'Last week the model gave you a number, for example the {short} in {unit}, and we scored it by the size of the prediction error. In practice someone has to decide whether to act. '
                         f'So today the question is a yes or no question, which is called binary classification: is it {label}? Yes is the positive class and no is the negative class. A reading arrives, the model says yes or no, and a person acts. '
                         f'For the {thing} data the example is: {K_["act"].lower()}. That is an illustration, and your own plant may do something different. '
                         'The data and the split are the same as Class 1. Only the question changes, so the way we score the model changes too.')))

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
                         f'The validation set is imbalanced: only {n_pos} of its {n_va} rows are positive. So accuracy cannot be the only measure we use today.')))

    r0 = b['scaling_rows'][0]
    S.append(dict(kind='idea', title='The standard deviation measures how far the values of a column typically sit from their mean',
                  visual=dict(kind='spread', values=load_vals.tolist(), mu=mu0, sd=sd0, mark=0, name='load_pct', unit='%'),
                  lead='Standard deviation (SD): the typical distance of a value from its mean. StandardScaler rewrites each feature as z-scores.',
                  points=[f'load_pct: mean {mu0:.2f} %, SD {sd0:.2f} %. {in_band} of {n_tr} rows lie in the gold band.',
                          'A z-score counts SDs above (+) or below (-) the mean. Red dot: training row 1.'],
                  notes=(f'Before the classifier, one idea from statistics: the standard deviation. Each dot is one training value of load. The red line is the mean, {mu0:.2f} percent. '
                         f'The standard deviation, here {sd0:.2f}, is the typical distance of a value from that mean, and the gold band covers one standard deviation each side. '
                         f'Ambient temperature has a much smaller spread, {sd1:.2f} degrees. So the two features live on different scales. '
                         'Standardisation, done by StandardScaler, rewrites each value as a z-score: how many standard deviations it sits from the mean. The bottom axis shows the same values counted that way. '
                         'Why must the mean and the spread come from the training set only?')))

    S.append(dict(kind='formula', title='The standard deviation and the z-score as formulas, with training row 1 worked by hand', size=20,
                  formulas=[('Standard deviation', r"$\sigma = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(x_i - \mu)^2}$"),
                            ('Standardisation (z-score)', r"$x' = (x - \mu)\,/\,\sigma$"),
                            ('Training row 1, load_pct', r"$x_1' = (%.2f - %.2f) / %.2f = %.2f$" % (r0[0], mu0, sd0, r0[2]))],
                  symbols=[['x_i, n', 'A raw value of row i, and the number of training rows', f'load_pct of the {n_tr} training rows'],
                           ['mu', 'The training mean of that column', f'load {mu0:.2f} %; ambient {mu1:.2f} deg C'],
                           ['sigma', 'The training standard deviation of that column', f'load {sd0:.2f} %; ambient {sd1:.2f} deg C'],
                           ["x'", 'The z-score: 0 is the mean, 1 is one SD above', f"Training row 1: load {r0[2]:.2f}, ambient {r0[3]:.2f}"]],
                  widths=[1.2, 5.6, 5.1],
                  note=f'StandardScaler divides by n. pandas .std() divides by n - 1 and gives {ss0:.2f} for load_pct.',
                  notes=(f'Here are both ideas in the usual notation. The standard deviation sigma: take each value minus the mean, square it, average the squares over the n training rows, and take the square root. '
                         f'For load that gives {sd0:.2f}. Then the z-score: a raw value x, minus the mean mu, divided by sigma. Training row 1 gives {r0[2]:.2f} for load and {r0[3]:.2f} for ambient temperature. '
                         f'One warning for your calculator checks. StandardScaler divides by n. The pandas method .std() that you used in Weeks 1 to 7 divides by n minus 1, so it gives {ss0:.2f}. Both are correct; they are two versions. Check the load line by hand before we go on.')))

    sig_where = 'just below' if ex['p'] < 0.5 else 'just above'
    S.append(dict(kind='idea', title='Logistic regression passes a linear score through the sigmoid (logistic) function, which stays between 0 and 1',
                  visual=dict(kind='sigmoid', mark=(ex['z'], ex['p'])),
                  lead='The sigmoid (logistic) function turns any score s into a probability from 0 to 1.',
                  points=['A probability of 0.5 means the two classes are equally likely.', 'The decision threshold is the probability at or above which the model predicts positive (yes), and below which it predicts negative (no).'],
                  notes=('Why not use a linear function to predict yes or no? Because a linear function keeps going, below zero and above one, and a probability cannot. '
                         'Logistic regression first builds a score, which we call s, from the features, in the same way as the linear regression in Class 1. Then it passes the score through an S-shaped curve called the sigmoid, or logistic function. '
                         'Very low scores become a probability near 0, very high scores near 1, and a score of 0 becomes exactly 0.5. '
                         f'The gold dot is one real row with a score close to 0, so its probability sits {sig_where} 0.5. We work it out by hand in a moment.')))

    parts = [ex['x'][0] * w0, ex['x'][1] * w1]
    zr = M['b'] + sum(round(p_, 2) for p_ in parts)
    assert abs(zr - ex['z']) < 0.0151, 'rounded products do not add up to the score within rounding'
    S.append(dict(kind='formula', title='Logistic regression in three lines: score, probability, prediction', size=18,
                  formulas=[('1  Score', r"$s = b_0 + b_1 x_1' + b_2 x_2'$"), ('2  Probability', r"$p = 1 \,/\, (1 + e^{-s})$"),
                            ('3  Prediction', r"$\hat{y} = \mathrm{positive}\ \mathrm{if}\ p \geq t,\ \mathrm{otherwise\ negative}$")],
                  symbols=[['s', 'The score: any number', f'{vr3.capitalize()}: s = {ex["z"]:.2f}'],
                           ['b0; b1, b2', 'Intercept (bias); weights (coefficients): rise in s per standard deviation', f'{M["b"]:.2f}; {w0:.2f} (load), {w1:.2f} (ambient)'],
                           ["x1', x2'", 'Standardised load_pct and ambient_c (z-scores)', f'Validation row 3: {ex["x"][0]:.2f} and {ex["x"][1]:.2f}'],
                           ['p', 'Probability of the positive class. e = 2.718', f'Validation row 3: p = {ex["p"]:.2f}'],
                           ['t', 'Decision threshold: predict positive if p is at least t', '0.5 first, then 0.3 and 0.7'],
                           ['y-hat', 'The predicted class: positive (1) or negative (0)', f'Validation row 3: {dec_ex}']],
                  widths=[1.6, 5.4, 4.9],
                  notes=(f'This is the whole of logistic regression in three lines. First the score s: an intercept b zero, plus a weight times each standardised feature. '
                         f'Our learned numbers are an intercept of {M["b"]:.2f}, a weight of {w0:.2f} for load and a weight of {w1:.2f} for ambient temperature. '
                         'Second, the sigmoid function turns the score into a probability p between 0 and 1. Third, the prediction y hat: the class is positive when p is at or above the decision threshold t, and negative otherwise. '
                         'We write s for the score, because the letter z already means a z-score. Both weights are positive, so more load or more heat pushes the score toward yes.')))

    fate = 'a true positive (TP)' if dec_ex == 'yes' else 'a false negative (FN)'
    side = 'at or above' if dec_ex == 'yes' else 'below'
    S.append(dict(kind='idea', title=f'Worked example: validation row 3 gets p = {d2(ex["p"])}, so the model predicts {dec_ex}',
                  visual=dict(kind='sheet', headers=['Part', "z-score x'", 'Weight b', 'Product'],
                              rows=[['Intercept b0', '', '', f'{M["b"]:.2f}'], ['load_pct', f'{ex["x"][0]:.2f}', f'{w0:.2f}', f'{parts[0]:.2f}'], ['ambient_c', f'{ex["x"][1]:.2f}', f'{w1:.2f}', f'{parts[1]:.2f}'],
                                    ['Score s (sum)', '', '', f'{ex["z"]:.2f}'], ['Probability p', '', '', f'{ex["p"]:.2f}']], hl=[4, 3]),
                  lead=f'{vr3.capitalize()}: load_pct {ex["raw"][0]:.2f} %, ambient_c {ex["raw"][1]:.2f} deg C. Actual class: positive.',
                  points=[f'p = {d2(ex["p"])} is {side} 0.5: {fate}.',
                          f'One SD of load_pct ({sd0:.2f} %) adds {w0:.2f} to s: {w0 / sd0:.2f} per percent.',
                          f'One SD of ambient_c ({sd1:.2f} deg C) adds {w1:.2f}: {w1 / sd1:.2f} per deg C.'],
                  notes=(f'This is validation row 3, which is record_id {va_id3} in the file. After standardisation, its load is {ex["x"][0]:.2f} and its ambient temperature {ex["x"][1]:.2f}. '
                         f'Multiply each by its weight, add the intercept of {M["b"]:.2f}, and the score is {ex["z"]:.2f}. The sigmoid turns that into a probability of {d2(ex["p"])}. '
                         f'At the usual decision threshold of 0.5 the model predicts {dec_ex}, and the actual class was positive, so this row is {fate}. '
                         f'Each weight belongs to one standard deviation. One standard deviation of load is {sd0:.2f} percent, so one percentage point adds about {w0 / sd0:.2f} to the score. The products may differ in the last digit because of rounding.')))

    # ---- how logistic regression learns (lecturer request, 12 November)
    S.append(dict(kind='idea', title='Log loss (binary cross-entropy) measures how wrong one predicted probability is',
                  visual=dict(kind='logloss', marks=[dict(p=pr3, y=1, label='row 3', dx=0.25, dy=-0.45),
                                                     dict(p=prn, y=0, label=f'row {kn + 1}', dx=-0.1, dy=0.45, ha='right')]),
                  lead='Log loss compares the probability p with the actual class y (1 or 0). It is 0 for a certain, right answer and grows fast as p moves away.',
                  points=['-(y ln p + (1 - y) ln(1 - p))',
                          f'Row 3, actual positive: -ln {pr3:.2f} = {l3:.2f}.',
                          f'Row {kn + 1}, actual negative: -ln(1 - {prn:.2f}) = {ln_:.2f}.'],
                  notes=('How does logistic regression learn its weights? The same way as in Class 1: it measures its error with a loss function and walks downhill. In Class 1 the loss was the MSE. '
                         'For a probability we use log loss, also called binary cross-entropy. If the row is actually positive, the loss is minus the natural log of p. If it is actually negative, it is minus the log of one minus p. '
                         f'Validation row 3 is positive with p {pr3:.2f}, so its loss is {l3:.2f}. {vrn.capitalize()} is negative with p {prn:.2f}, so its loss is {ln_:.2f}. '
                         'A confident wrong answer costs a lot: the curve shoots up. What would the loss be for p equal to 1 on a positive row?')))

    S.append(dict(kind='formula', title='The training loss is the mean log loss, and gradient descent walks the weights downhill', size=18,
                  formulas=[('Training loss', r"$L = \frac{1}{n}\sum_{i=1}^{n} \mathrm{loss}_i$"),
                            ('Slope for weight j', r"$\mathrm{slope}_j = \frac{1}{n}\sum_{i=1}^{n} (p_i - y_i)\, x_{ij}$"),
                            ('Update rule (Class 1)', r"$b_j \leftarrow b_j - \eta \cdot \mathrm{slope}_j$")],
                  symbols=[['L, n', 'Mean log loss over the n training rows', f'n = {n_tr}; L = {M["train_ll"]:.2f} after training'],
                           ['p_i - y_i', 'Error of row i: probability minus actual class', 'Start: all weights 0, so every p_i = 0.5'],
                           ['x_ij', 'Feature j of row i (z-score); x_i0 = 1 for b0', 'j = 1 load_pct, j = 2 ambient_c'],
                           ['slope_j', 'Positive slope: lower b_j', f'Start: {g0[0]:.2f}, {g0[1]:.2f}, {g0[2]:.2f}']],
                  widths=[1.4, 5.8, 4.7],
                  note=f'eta is the learning rate (step size), 0.5 here. Start by hand: slope_0 = 0.5 - {cc["tr_pos"]}/{n_tr} = {g0[0]:.2f}.',
                  notes=('The training loss is the mean of the log loss over all the training rows, just as the MSE was a mean in Class 1. Gradient descent then works exactly as you saw last week: find the slope of the loss for each weight, and step a little downhill. '
                         'For log loss the slope has a friendly form. For weight j it is the mean of the error p minus y, times feature j. '
                         f'At the start every weight is 0, so every p is 0.5. For the intercept the slope is 0.5 minus {cc["tr_pos"]} over {n_tr}, which is {g0[0]:.2f}. It is positive, so b zero moves down. '
                         'Which way does b one move?')))

    marks_gd = []
    for k_, dx_, dy_, ha_ in ((0, 0.25, 0.1, 'left'), (20, 0.25, 0.3, 'left'), (500, -0.1, 0.55, 'right')):
        r_ = path[k_]
        lab_ = f'step {k_}: b1 {r_[3]:.2f}, b2 {r_[4]:.2f}' + ('\n= scikit-learn' if k_ == 500 else '')
        marks_gd.append(dict(step=k_, loss=r_[1], label=lab_, dx=dx_, dy=dy_, ha=ha_))
    S.append(dict(kind='idea', title='scikit-learn minimises the same log loss with a faster solver and a small L2 penalty that keeps the weights small',
                  visual=dict(kind='gd_curve', steps=[(r_[0], r_[1]) for r_ in path], marks=marks_gd),
                  lead='LogisticRegression() minimises C x (total log loss) + 0.5 x (b1² + b2²). This L2 penalty keeps the weights small. C = 1.0.',
                  points=[f'Gradient descent with the same penalty reaches the same weights: {w0:.2f} and {w1:.2f}.',
                          'The lbfgs solver gets there in a few smarter steps.',
                          'The penalty works in raw units, so standardise first.'],
                  notes=('Here is what scikit-learn really does. It minimises the same log loss, plus a penalty: half the sum of the squared weights, called an L2 penalty or regularisation. The intercept is not penalised. '
                         'The penalty keeps the weights small, and C sets the balance: a smaller C means a stronger penalty. Class 4 comes back to this idea with ridge regression. '
                         f'The curve is our own gradient descent on this loss: the training loss falls from {path[0][1]:.2f} and the weights reach {w0:.2f} and {w1:.2f}, the same numbers scikit-learn prints. '
                         'Its solver, lbfgs, is faster. Because the penalty adds squared weights, the units of the features matter. That is one more reason to standardise.')))

    S.append(dict(kind='idea', title='A decision tree classifier can also answer yes or no, and it does not need standardisation',
                  visual=dict(kind='tree', node=tree_node),
                  lead='A row follows the answers down the tree to one leaf node, a yellow box. Each question is an internal node.',
                  points=['A leaf predicts the majority class of its rows. (n): training rows.', 'max_depth = 3: at most 3 questions.', leaf_line],
                  notes=('The second model is a decision tree classifier, the same idea as Class 1 with one change at the bottom. In Class 1 each leaf node predicted an average. '
                         'Now each leaf node gives the majority class of the training rows that ended there. '
                         'max_depth is 3, so a row meets at most three questions. The questions use real load and temperature, so no standardisation is needed. '
                         + leaf_spoken + f' On the validation set this tree reaches an accuracy of {d2(tmt["accuracy"])}.')))

    S.append(dict(kind='idea', title='The confusion matrix counts true and false positives and negatives',
                  visual=dict(kind='confusion_c2', tp=tp, fp=fp, fn=fn, tn=tn, subs=sub4),
                  lead=f'Logistic regression, decision threshold 0.5, validation set. Positive class: {label}.',
                  points=[f'Each of the {n_va} rows lands in exactly one box.', 'Rows: Actual class. Columns: Predicted class, as in scikit-learn.', 'FP is a false warning. FN is a missed positive.'],
                  notes=(f'Here is the logistic regression on the {n_va} validation rows at decision threshold 0.5. Each row falls into one of four boxes. '
                         f'True positives, TP, are {tp}: the model said yes and it was yes. False negatives, FN, are {fn}: the model said no, but it was yes. False positives, FP, are {fp}: the model said yes, but it was no. '
                         f'And true negatives, TN, are {tn}: the model said no and it was no. The four counts add to {n_va}. '
                         'Rows are the Actual class and columns are the Predicted class, the same layout scikit-learn prints. Everything else today is arithmetic on these four numbers.')))

    P = tp / (tp + fp)
    Rc = tp / (tp + fn)
    assert tp + fp > 0 and abs(P - mt['precision']) < 1e-12 and abs(Rc - mt['recall']) < 1e-12 and abs((tp + tn) / n_va - mt['accuracy']) < 1e-12
    f1_hand = 2 * round(P, 2) * round(Rc, 2) / (round(P, 2) + round(Rc, 2))
    assert abs(f1_hand - mt['f1']) < 0.0051 and abs(2 * tp / (2 * tp + fp + fn) - mt['f1']) < 1e-12
    S.append(dict(kind='formula', title='Accuracy and precision are worked out from the four counts TP, FP, FN and TN', size=18,
                  formulas=[('Accuracy', r"$\mathrm{accuracy} = \frac{TP + TN}{n} = \frac{%d + %d}{%d} = %.2f$" % (tp, tn, n_va, mt['accuracy'])),
                            ('Precision', r"$\mathrm{precision} = \frac{TP}{TP + FP} = \frac{%d}{%d + %d} = %.2f$" % (tp, tp, fp, mt['precision']))],
                  symbols=[['TP', 'True positive: predicted positive, actually positive', pl(tp, 'validation row')], ['FP', 'False positive: predicted positive, actually negative', pl(fp, 'row')],
                           ['FN', 'False negative: predicted negative, actually positive', pl(fn, 'row')], ['TN', 'True negative: predicted negative, actually negative', pl(tn, 'row')],
                           ['n', 'All rows scored: TP + TN + FP + FN', f'{n_va} validation rows']],
                  widths=[1.0, 6.6, 4.3], note=f'Counts are for logistic regression at decision threshold 0.5. The majority-class baseline has accuracy {d2(always)}.',
                  notes=(f'Now the formulas, with the standard names. TP, FP, FN and TN are the four counts of the confusion matrix. Accuracy asks: out of all rows, how often is the prediction right? It is TP plus TN over all n rows: '
                         f'{tp} plus {tn}, over {n_va}, is {d2(mt["accuracy"])}. Precision asks: of the rows the model predicted positive, how many are really positive? It is TP over TP plus FP, which is {tp} over {tp + fp}, or {d2(mt["precision"])}. '
                         f'Compare the accuracy with the majority-class baseline of {d2(always)}. Which of the four counts does precision ignore?')))

    S.append(dict(kind='formula', title='Recall (sensitivity) and F1: how many actual positives we find, and one blended score', size=18,
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
                         'F1 is low if either precision or recall is low, so you cannot hide a weak one. Please check one of these divisions on paper with me now.')))

    S.append(dict(kind='compare', title=f'A false negative and a false positive cost different things for a {thing}',
                  left=dict(head='False negative (FN)', icon='cross', points=['Predicted no, but actually yes.'] + K_['miss'] + ['Every FN lowers recall.']),
                  right=dict(head='False positive (FP)', icon='bell', points=['Predicted yes, but actually no.'] + K_['alarm'] + ['Every FP lowers precision.']),
                  verdict='A false negative costs more here, so we watch recall.',
                  notes=(f'The two mistakes are not equal. A false negative means the model said no, and the {short} did reach its limit. {" ".join(K_["miss"])} '
                         f'A false positive means the model said yes and nothing happened. {" ".join(K_["alarm"])} '
                         'These descriptions are my illustration, and your own site may weigh them differently. '
                         'You decide which mistake hurts more before you choose a decision threshold. In a moment we put invented prices on them, 5 for a false negative and 1 for a false positive. Which would you protect in your own field?')))

    S.append(dict(kind='table', title=(f'Both models give the same counts on the same {n_va} rows: TP {cm["tp"]}, FN {cm["fn"]}, FP {cm["fp"]}' if cm == tcm else f'Logistic regression and the decision tree give different counts on the same {n_va} rows'),
                  headers=['Measure', 'Logistic regression', 'Decision tree, depth 3', 'Majority-class baseline'],
                  rows=[['True positives (TP)', str(cm['tp']), str(tcm['tp']), '0'], ['False negatives (FN)', str(cm['fn']), str(tcm['fn']), str(n_pos)], ['False positives (FP)', str(cm['fp']), str(tcm['fp']), '0'],
                        ['Accuracy', d2(mt['accuracy']), d2(tmt['accuracy']), d2(always)], ['Precision', d2(mt['precision']), d2(tmt['precision']), '0.00'],
                        ['Recall', d2(mt['recall']), d2(tmt['recall']), '0.00'], ['F1', d2(mt['f1']), d2(tmt['f1']), '0.00']],
                  widths=[2.9, 2.8, 3.0, 3.2], icons=['check', 'cross', 'bell', 'bars', 'flag', 'magnifier', 'chart'],
                  note=model_note + ' Precision of 0.00 for the majority-class baseline means 0 of 0: it never predicts positive.',
                  notes=(f'Here are the two models side by side on the same {n_va} validation rows, with the majority-class baseline for comparison. '
                         f'Logistic regression has {pl(cm["tp"], "true positive")} and {pl(cm["fn"], "false negative")}, with {pl(cm["fp"], "false positive")}. The tree has {pl(tcm["tp"], "true positive")} and {pl(tcm["fn"], "false negative")}, with {pl(tcm["fp"], "false positive")}. '
                         f'The baseline has an accuracy of {d2(always)} but finds nothing, so its precision and recall are zero. '
                         f'{model_note} Remember that one row changes these numbers a lot when there are only {n_va} rows.')))

    if trade:
        th_title = 'Lowering the decision threshold never lowers recall, and it can add false positives'
        th_lead = 'A lower threshold predicts positive more often: recall rises or stays, and false positives can rise.'
    else:
        th_title = 'Lowering the decision threshold raises recall, and from 0.7 down to 0.3 it adds no false positive here'
        th_lead = ('A lower threshold predicts positive more often: recall rises or stays.'
                   + (f' Below 0.3 false positives appear: {low_fp[1]} at {low_fp[0]:g}.' if low_fp else ''))
    S.append(dict(kind='idea', title=th_title,
                  visual=dict(kind='threshold', probs=M['probs'], actual=M['actual'], ths=[t['th'] for t in th],
                              rows=[f'Threshold {t["th"]:g}: TP {t["tp"]}, FN {t["fn"]}, FP {t["fp"]}, recall {d2(t["recall"])}' for t in th]),
                  lead=th_lead,
                  points=[note_lo, note_hi],
                  notes=(f'Each dot is one validation row, placed by its probability. Gold dots are actual positives. A row at or above a dashed threshold line is predicted positive. {row_story} '
                         f'{story_lo} {story_hi}{free_lunch} '
                         + ('Sliding the line left never loses a positive, and sliding it right never adds a false positive. That is the precision-recall trade-off.' if trade else ''))))

    S.append(dict(kind='formula', title=f'The cost of the mistakes puts a price on each one: here a false negative costs {MISSED_COST} and a false positive costs {FALSE_ALARM_COST}', size=20,
                  formulas=[('Cost of mistakes', r"$\mathrm{cost} = \mathrm{MISSED\_COST} \times FN + \mathrm{FALSE\_ALARM\_COST} \times FP$"),
                            ('At threshold 0.5', r"$\mathrm{cost} = %d \times %d + %d \times %d = %d$" % (MISSED_COST, t5['fn'], FALSE_ALARM_COST, t5['fp'], costs['0.5']))],
                  symbols=[['MISSED_COST', 'The cost of one false negative (a missed positive)', f'{MISSED_COST} (invented teaching cost)'],
                           ['FALSE_ALARM_COST', 'The cost of one false positive (a false alarm)', f'{FALSE_ALARM_COST} (invented teaching cost)'],
                           ['FN, FP', 'False negatives and false positives at the chosen threshold', f'At 0.5: FN {t5["fn"]}, FP {t5["fp"]}'],
                           ['cost', 'The total price of the mistakes on the validation set. Lower is better', f'At 0.5: {costs["0.5"]}']],
                  widths=[2.8, 5.4, 3.7],
                  note='Invented teaching costs: one missed positive costs as much as five false alarms.',
                  notes=(f'Now we put a price on each mistake. The cost is MISSED_COST times the false negatives, plus FALSE_ALARM_COST times the false positives. '
                         f'I have invented the prices for teaching: a missed {label} costs 5 and a false alarm costs 1. A real site would agree its own numbers with the people who pay for the mistakes. '
                         f'At threshold 0.5 we have {pl(t5["fn"], "false negative")} and {pl(t5["fp"], "false positive")}, so the cost is 5 times {t5["fn"]} plus 1 times {t5["fp"]}, which is {costs["0.5"]}. '
                         'The project uses exactly this formula with these two costs. What would the cost be at 0.3?')))

    def crow(t):
        return [f'{t["th"]:g}', str(t['tp']), str(t['fp']), str(t['fn']), str(t['tn']), d2(t['recall']), d2(t['precision']),
                f'{MISSED_COST} x {t["fn"]} + {FALSE_ALARM_COST} x {t["fp"]} = {t["cost"]}']
    ties = [r for r in M['cost'] if r['cost'] == best['cost']]
    tie_txt = f' Thresholds {" and ".join(f"{r["th"]:g}" for r in ties)} tie, so we take the higher one, {bth}.' if len(ties) > 1 else ''
    S.append(dict(kind='table', title=f'The cost table picks decision threshold {bth}, the lowest cost on the validation set',
                  headers=['Threshold', 'TP', 'FP', 'FN', 'TN', 'Recall', 'Precision', 'Cost'],
                  rows=[crow(t) for t in M['cost']], widths=[1.6, 0.9, 0.9, 0.9, 0.9, 1.4, 1.7, 3.6], icons=['bell', 'check', 'flag'], hl_col=None,
                  note=('Rule: choose the threshold with the lowest cost. If two tie, take the higher threshold.' + tie_txt
                        + (f' At {nobody[0]:g} no row is predicted positive, so precision shows 0.00.' if nobody else '')),
                  notes=(f'This is the cost table: for each decision threshold the four counts, recall, precision and the cost. '
                         f'The costs are {", ".join(f"{k} at {v}" for v, k in costs.items())}. The rule is simple: choose the threshold with the lowest cost, and if two tie, take the higher one, because it raises fewer alarms. '
                         f'Here that is {bth}.{tie_txt} We choose on the validation set, never on the test set. {nobody_note} '
                         'Check one cost with me by hand: five times the false negatives, plus the false positives.')))

    ill = [(0.2, 10, 27), (0.5, 8, 6), (0.8, 4, 1)]          # illustrative: 10 actual positive rows and 90 actual negative rows
    S.append(dict(kind='table', title='On a larger set, a lower decision threshold finds more positives and also gives more false positives',
                  headers=['Decision threshold', 'TP (of 10 actual positive)', 'FP (of 90 actual negative)', 'True positive rate (TPR)', 'False positive rate (FPR)'],
                  rows=[[f'{a:g}', str(c), str(fa), f'{c / 10:.2f}', f'{fa / 90:.2f}'] for a, c, fa in ill], widths=[1.8, 2.6, 2.8, 2.4, 2.4], icons=['bell', 'check', 'flag'],
                  note='Illustrative example (hypothetical data), not from our data. TPR is the same as recall. Each row of this table becomes one point on a ROC curve.',
                  notes=('This table uses illustrative numbers, made up to show the trade-off clearly on a larger set. Imagine 10 actual positive rows and 90 actual negative rows. '
                         'At a low decision threshold of 0.2 the model finds all 10, but it also gives 27 false positives. At a high threshold of 0.8 it gives only 1 false positive, but it finds just 4 of the 10. '
                         'The two right-hand columns are the true positive rate, the share of actual positives found, which is recall, and the false positive rate, the share of actual negatives wrongly flagged positive. '
                         'Each row becomes one point on the ROC curve in a moment. Which row has the lowest cost with our prices of 5 and 1?')))

    roc_marks = []
    pairs_xy = []
    tops = []
    for t in th:
        fpr = t['fp'] / (t['fp'] + t['tn'])
        tpr = t['tp'] / (t['tp'] + t['fn'])
        pairs_xy.append((f'{fpr:.2f}', f'{tpr:.2f}'))
        m_ = dict(x=fpr, y=tpr, label=f'{t["th"]:g}: ({fpr:.2f}, {tpr:.2f})', dx=1.0 if tpr < 0.05 else 0.25, dy=0.15 if tpr < 0.05 else -0.28)
        if tpr > 0.9:
            tops.append(m_)
        roc_marks.append(m_)
    for i, m_ in enumerate(sorted(tops, key=lambda m: m['x'])):
        m_['dy'] = -0.3 - 0.4 * i
    fpr5, tpr5 = fp / (fp + tn), tp / (tp + fn)
    S.append(dict(kind='formula', title='Two rates give the points of the ROC curve: the false positive rate (FPR) and the true positive rate (TPR)', size=20,
                  formulas=[('False positive rate (at 0.5)', r"$\mathrm{FPR} = \frac{FP}{FP + TN} = \frac{%d}{%d + %d} = %.2f$" % (fp, fp, tn, fpr5)),
                            ('True positive rate (at 0.5)', r"$\mathrm{TPR} = \frac{TP}{TP + FN} = \frac{%d}{%d + %d} = %.2f$" % (tp, tp, fn, tpr5))],
                  symbols=[['FPR', 'False positive rate: share of actual negatives (FP + TN) predicted positive', f'{fp} of {fp + tn} actual negative rows'],
                           ['TPR', 'True positive rate: share of actual positives (TP + FN) found. Same as recall', f'{tp} of {tp + fn} actual positive rows']],
                  widths=[1.6, 6.2, 4.1], note='Points (FPR, TPR) at thresholds 0.3, 0.5 and 0.7: ' + ', '.join(f'({a}, {c})' for a, c in pairs_xy) + '.',
                  notes=(f'The ROC curve needs two rates. The false positive rate, FPR, is FP over FP plus TN: of all the rows that are actually negative, what share did we wrongly flag as positive. At decision threshold 0.5 that is {fp} over {fp + tn}, or {fpr5:.2f}. '
                         f'The true positive rate, TPR, is the same thing as recall, also called sensitivity: {tp} over {tp + fn}, or {tpr5:.2f}. '
                         'Each threshold gives one pair of rates, and each pair is one point on the ROC graph that follows. Why is a low FPR good, and a high TPR good?')))

    auc_text = f'{wins} of {pairs} pairs'
    perfect = f' A perfect score on {n_va} rows is encouraging, but it promises nothing about new equipment.' if auc >= 0.999 else ''
    n_pts = len(b['roc'])
    S.append(dict(kind='idea', title='The ROC curve plots one point for every decision threshold: FPR across, TPR up',
                  visual=dict(kind='roc_real', points=b['roc'], auc=auc, marks=roc_marks),
                  lead='ROC is short for receiver operating characteristic. It is a graph with one point per decision threshold.',
                  points=[f'{n_pts} black points, so the line is a staircase.', f'Your lab plot shows only the {M["roc_sk"]} corners.', 'Red: thresholds 0.3, 0.5, 0.7.'],
                  notes=(f'The ROC curve is a graph, and ROC stands for receiver operating characteristic. For every decision threshold we work out two rates and plot one point: the false positive rate across, and the true positive rate up. '
                         f'The black dots are every threshold that changes a prediction on our rows, {n_pts} in all, so the line climbs in steps like a staircase. In the lab, roc_curve drops the points in the middle of a straight run, so you will see {M["roc_sk"]}. The line is the same. '
                         'A curve that hugs the top left corner is good, because it finds many positives with few false positives. The dashed line is random guessing. '
                         f'The area under the line is the AUC, here {d2(auc)}.')))

    S.append(dict(kind='idea', title='AUC is the area under the ROC curve, and on a large dataset the curve is smooth',
                  visual=dict(kind='roc_smooth'),
                  lead='AUC (area under the curve) is the chance that an actual positive row scores higher than an actual negative row (ties count half).',
                  points=[f'Ours: {pairs} pairs ({n_pos} x {n_neg}), and {auc_text} are in the right order: AUC {d2(auc)}.', 'The curve is illustrative. With thousands of rows it looks smooth. AUC 0.5 is random guessing.'],
                  notes=(f'Here is what the AUC means in words. Take one actual positive row and one actual negative row. AUC is the chance that the model gives the positive row the higher probability, and a tie counts as half. '
                         f'We have {n_pos} positive rows and {n_neg} negative rows, so {pairs} pairs, and {wins} of them are in the right order. That gives {d2(auc)}.{perfect} '
                         'The curve in the picture is illustrative. On a large dataset there are thousands of thresholds, the dots sit almost on top of each other, and the staircase becomes a smooth curve. '
                         'An AUC of 0.5 is a coin flip, and 1.0 is perfect. Why is this score independent of any single decision threshold?')))

    S.append(dict(kind='list', title=f'With {n_va} rows and {n_pos} actual positives, every score here is shaky',
                  items=[f'The validation set has {n_va} rows and only {n_pos} actual positive rows.', f'If one actual positive row changed its prediction, recall would move by {d2(1 / n_pos)}. One changed row moves accuracy by {d2(1 / n_va)}.',
                         'These numbers teach you how the scores work. They are too few to prove which model is better.', 'Class 3 shows how to test a model with more care.'],
                  icons=['cross', 'calculator', 'lock', 'book'],
                  notes=(f'I want to be careful about the limits. The validation set has only {n_va} rows and {n_pos} of them are actual positives. '
                         f'If the model got one more positive row right, the recall would move by {d2(1 / n_pos)}. If it got one more row of any kind right, the accuracy would move by {d2(1 / n_va)}. '
                         'So the numbers on these slides are good for learning the scores, and weak as proof that one model beats another. The same holds for the cost table. '
                         'Next class we look at tests that use more rows and give us more reason to trust a number. Keep that caution in mind in the lab.')))

    S.append(dict(kind='list', title='Summary: judge a binary classifier by counting each kind of mistake and pricing it',
                  items=['Make a label with a limit. Standardise the features into z-scores.',
                         'Logistic regression turns a score s into a probability with the sigmoid function.',
                         'It learns by gradient descent on the mean log loss, plus an L2 penalty in scikit-learn.',
                         'Count TP, FP, FN and TN, and work out accuracy, precision, recall and F1.',
                         'Choose the decision threshold with the lowest cost. AUC shows how well positives rank above negatives.'],
                  icons=['flag', 'switch', 'gear', 'grid', 'chart'],
                  notes=('Here is the whole class in five lines. Make a label from the target with a limit, and standardise the features with the training mean and standard deviation. '
                         'Logistic regression turns a score into a probability with the sigmoid. It learns by walking downhill on the log loss, and scikit-learn adds a small penalty on the weights. '
                         'Count the answers in a confusion matrix, and work out accuracy, precision, recall and F1. Then price the mistakes, and choose the threshold with the lowest cost. '
                         'If you can say these five lines in your own words, you are ready for the lab.')))

    S.append(dict(kind='code', title='Read the workflow before you write it: impute, standardise, fit, predict probabilities, count',
                  code=('imputer = SimpleImputer(strategy="median")\nX_train = imputer.fit_transform(\n    training_data[feature_columns])\nX_valid = imputer.transform(\n    validation_data[feature_columns])\n'
                        'logistic_model = make_pipeline(\n    StandardScaler(), LogisticRegression())\nlogistic_model.fit(X_train, y_train)\n'
                        'y_proba = logistic_model.predict_proba(X_valid)[:, 1]\nthreshold = 0.5\ny_pred = (y_proba >= threshold).astype(int)\ncm = confusion_matrix(y_valid, y_pred)'),
                  reads=['The imputer fills each missing value (NaN) with the training median (imputation).', 'The pipeline chains StandardScaler and LogisticRegression.',
                         'predict_proba gives a probability per class. Column 1 is the positive class.', 'y_proba >= threshold gives True or False. astype(int) makes it 1 or 0: y_pred.',
                         'confusion_matrix puts Actual down the side and Predicted across the top, negative first: TN and FP in the top row, FN and TP below.'],
                  notes=('Before we leave the concepts, look at the workflow, with the same names as the notebook. The imputer, SimpleImputer, fills missing values with the training median. X_train is the table of training features, and y_train is the column of labels. '
                         'Chain StandardScaler and the logistic regression in one pipeline called logistic_model. Fitting it learns the means, the standard deviations and the weights from the training set only. '
                         'Then ask for probabilities, and keep the column for the positive class. Compare each probability with the threshold to get y_pred, the predicted class, and count the answers in a confusion matrix. '
                         'If you can read these lines aloud in plain words, you are ready.')))

    # ------------------------------------------------------------------ lab
    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook. You use the same engineering_data.csv file as in Class 1.', section='Lab',
                  notes=('That is the end of the concepts. Everything you need is on the slides you have just seen, and every term is explained again inside the notebook. '
                         'Please open the notebook now, and keep the slides closed except for the check slides at the end of the deck. I will walk around. Raise your hand if a cell gives an error. '
                         'Run the cells in order from the top, and write your prediction before you run each cell.')))

    S.append(dict(kind='steps', title='The lab has nine steps in five stages, and each stage ends with a check',
                  steps=[dict(head='Step 1: prepare', text='Load, clean, split, impute the missing value', icon='folder'), dict(head='Step 2: label', text=f'Make the label for {label} and the majority-class baseline', icon='flag'),
                         dict(head='Steps 3 and 4: models', text='Logistic regression, its log loss, then a decision tree', icon='gear'), dict(head='Step 5: count', text='Confusion matrix and four scores', icon='grid'),
                         dict(head='Steps 6 and 7: thresholds', text='Cost table, chosen threshold, ROC curve', icon='chart')], highlight=None,
                  caption='Predict first, run second, then read the output. CHANGE tasks: steps 3 and 6. Steps 8 and 9: conclusion and saving.',
                  notes=('Here are the stages of the lab. One, prepare the data as in Class 1: load, clean, split by group and impute the missing value. Two, make the label from the target with the limit. '
                         'Three and four, train the logistic regression with standardisation, print its training log loss, and train the decision tree classifier. Five, count the answers in a confusion matrix and work out the four scores. '
                         'Six and seven, build the cost table, choose the threshold, and draw the ROC curve. Two CHANGE tasks wait for you: remove the standardisation and see what changes, and try lower thresholds. '
                         'Predict first, then run, then read.')))

    rows_chk = [['Positive labels (training set, validation set); majority-class baseline accuracy', f'{cc["tr_pos"]} of {cc["tr_n"]}, {cc["va_pos"]} of {cc["va_n"]}; {d2(always)}'],
                ['Learned weights (coefficients): load_pct, ambient_c, and the intercept', f'{lg["w"][0]:.2f}, {lg["w"][1]:.2f}, {lg["b"]:.2f}'],
                ['Mean log loss on the training set', f'{M["train_ll"]:.2f}'],
                ['Logistic regression: TP, FN, FP, TN', f'{tp}, {fn}, {fp}, {tn}'],
                ['Logistic regression: accuracy, precision, recall, F1', f'{d2(mt["accuracy"])}, {d2(mt["precision"])}, {d2(mt["recall"])}, {d2(mt["f1"])}'],
                ['Decision tree: TP, FN, FP, TN', f'{tcm["tp"]}, {tcm["fn"]}, {tcm["fp"]}, {tcm["tn"]}'],
                ['Cost at decision thresholds 0.3, 0.5, 0.7, and the chosen threshold', f'{costs["0.3"]}, {costs["0.5"]}, {costs["0.7"]}; {bth}'],
                ['AUC', d2(auc)]]
    S.append(dict(kind='table', title='Check your numbers against these before you move on',
                  headers=['What to check', 'You should see'], rows=rows_chk, widths=[7.6, 4.0],
                  icons=['flag', 'gear', 'calculator', 'grid', 'check', 'grid', 'calculator', 'chart'],
                  note='If your number differs, stop and ask. Do not change a number to match. Find the step that went wrong.',
                  notes=('Use this table as your checkpoint. If your numbers match, you can carry on. If they do not, stop and call me over, because each step builds on the one before. '
                         'The usual reasons are a cell run out of order, or a missing value imputed with the wrong median. All your numbers should match this table exactly, because we all use the same split and the same settings. '
                         'Do not edit a number to make it match. Find out why it differs. That habit will serve you in every project.')))

    S.append(dict(kind='table', title='Four messages you will meet, what they mean and what to do',
                  headers=['Message', 'What it says', 'What to do'],
                  rows=[['ValueError: contains NaN', 'A missing value (NaN) reached StandardScaler or the model', 'Run the imputation step (SimpleImputer with the training median)'],
                        ['Classification metrics can\'t handle a mix of binary and continuous targets', 'You gave probabilities where a predicted class (0 or 1) was needed', 'Compare y_proba with the threshold first, to get y_pred'],
                        ['ConvergenceWarning', 'The solver stopped before it reached the bottom of the loss. The cell still runs', 'Standardise the features, or raise max_iter'],
                        ['NameError', 'A cell above has not been run yet', 'Run all cells from the top, in order']],
                  widths=[4.4, 3.8, 4.4], icons=['cross', 'key', 'bell', 'flag'],
                  notes=('Messages are normal, and reading them is a skill. Here are the four you will most likely meet today. A NaN error means a missing value reached the model, so run the imputation step. '
                         'The long message about binary and continuous targets means you gave the metric a probability where it needed a predicted class, so compare the probability with the threshold first. '
                         'A convergence warning is only a warning. It can appear when the features are on very different scales, because the solver then needs more steps. And a name error means you skipped a cell above. Read the last line of any message first.')))

    S.append(dict(kind='list', title='How this class counts towards your coursework',
                  items=['Block 1 is Class 1 and Class 2. It is practice: it does not count toward your final mark.',
                         'Assignment part A (A7, regression) repeats the Class 1 lab. Part B (A8, classification and cost) repeats today\'s lab.',
                         f'The Block 1 assignment closes on {C.COHORTS[code]["b1_close"]} (Kampala time).',
                         'The Block 1 quiz is two online forms, Q7 (Class 1) and Q8 (Class 2). They open in the last 20 minutes today, each for 24 hours.'],
                  icons=['folder', 'doc', 'clock', 'bell'],
                  notes=('A word on how this counts. The block work is practice: it does not count toward your final mark, but it is collected and you get feedback, and it is the best preparation for the project. '
                         'Your final mark is A1 to A5, Q1 to Q5, Practical Test 1 and the Week 12 project, which is 40 percent. Part A of the Block 1 assignment is on regression and part B on classification and cost, each in the assignment notebook. '
                         f'Both parts close on {C.COHORTS[code]["b1_close"]}, Kampala time. The quiz is two short online forms, Q7 and Q8. They open in the last twenty minutes today and each stays open for twenty-four hours. Keep your saved notebooks.')))

    # ------------------------------------------------------------------ facilitator (cohort-neutral words: the per-cohort numbers are in the guide table)
    closes = '; '.join(f'{c_} {C.COHORTS[c_]["b1_close"]}' for c_ in ('CML3112', 'CML3113', 'CML3111'))
    s['facilitator'] = dict(
        prep=['Open the deck in Slide Show mode and the lab notebook in Colab before anyone arrives. Run the notebook from the top once on your account.',
              'Put the lab notebook and engineering_data.csv in the shared class folder and post the link. Every learner needs both files in Colab, in the Files panel.',
              'Write the "check your numbers" table on the board before the lab. Use your own cohort\'s column of the table "The numbers each cohort should see" below: the numbers differ between cohorts.',
              'The Block 1 quiz is online: forms Q7 (Class 1) and Q8 (Class 2). Open both in the last 20 minutes of the class. Each stays open for 24 hours (arrangement note of 2 November). Nothing is sat on paper.',
              f'The deck states the Block 1 close from the arrangement note: {closes} (Kampala time). Confirm it in writing after the class.'],
        misconceptions=[('High accuracy means a good model', 'On the validation set the majority-class baseline (always predict no) already scores the accuracy in the table below. Compare with that baseline and look at recall.'),
                        ('The decision threshold is always 0.5', '0.5 is a default. Choose the threshold from the cost table: the lowest validation cost, and a tie goes to the higher threshold.'),
                        ('Standardisation cannot change the answer of the model', 'For a tree that is right. For LogisticRegression it can: scikit-learn adds an L2 penalty on the weights (C = 1.0), and the penalty depends on the units. Without StandardScaler the weights change, the probabilities move, and in some cohorts the confusion matrix at 0.5 changes (see the table).'),
                        ('Log loss and accuracy measure the same thing', 'Accuracy only counts right and wrong. Log loss also punishes a confident wrong probability: -ln 0.01 is 4.6, while -ln 0.5 is 0.69.'),
                        ('An AUC of 1.0 means the model is perfect', f'It means every actual positive scored above every actual negative in these {n_va} rows. New equipment can behave differently.')],
        probes=[('What does a false positive cost for your equipment?', 'Answers differ. Listen for a cost in time or energy, and compare it with the cost of a false negative.'),
                ('Why is accuracy alone not enough?', 'With few positive cases, the majority-class baseline scores a high accuracy and finds none of them.'),
                ('When is precision the more important score?', 'When a false positive is expensive, for example an unnecessary stop.'),
                ('When is recall the more important score?', 'When a false negative is dangerous or expensive, for example an overheating motor.'),
                ('What happens to recall if you lower the decision threshold?', 'It rises or stays the same, never falls. The table gives recall at 0.3, 0.5 and 0.7 for each cohort.'),
                ('What is the log loss of an actual positive row with p = 1?', 'Zero: -ln 1 = 0. The model was certain and right.'),
                ('Why do the weights change without StandardScaler?', 'Each weight now belongs to one unit of its feature, and the L2 penalty adds the squared weights in those units, so the fitted model is different.'),
                ('Why do we fit StandardScaler on the training set only?', 'If the validation set helped decide the mean and the standard deviation, information would leak from held-out data into the model. That is data leakage.'),
                ('Does the decision tree need standardisation?', 'No. A tree only asks whether a value is above or below a threshold, and standardisation does not change the order of the values.'),
                ('What does an AUC of 0.5 mean?', 'The model ranks positive and negative cases no better than a coin flip.')],
        lab_steps=[('Step 1: prepare', f'Rows after cleaning {b["n_clean"]}. Split {b["n_tr"]}, {b["n_va"]}, {b["n_te"]}. The same cleaning and split as Class 1, repeated.'),
                   ('Step 2: label', 'Positive labels and the baseline accuracy: see the table below (they differ by cohort).'),
                   ('Step 3: logistic regression', 'Weights, intercept and the mean training log loss as in the table. The CHANGE task removes StandardScaler: the load weight becomes much smaller, because it now belongs to one percent of load, and the fitted model changes because of the default L2 penalty. '
                    'Ask which weight shrank, which grew, and whether the confusion matrix changed (the table has the answer per cohort). No ConvergenceWarning appears with max_iter=1000.'),
                   ('Step 4: decision tree', 'Depth 3. TP, FN, FP, TN as in the table. Some leaves rest on one training row: point at the numbers in brackets on the tree slide.'),
                   ('Step 5: confusion matrix and scores', 'Counts and scores as in the table. Ask one learner to repeat one division at the board.'),
                   ('Step 6: cost table and threshold', f'Costs at 0.3, 0.5 and 0.7 and the chosen threshold as in the table (cost = {MISSED_COST} x FN + {FALSE_ALARM_COST} x FP, invented teaching costs). The CHANGE task adds 0.1 and 0.2: false positives appear in every cohort.'),
                   ('Step 7: ROC curve and AUC', 'AUC as in the table. The plot shows only the corner points that roc_curve keeps (the number is in the table). Ask what a score this high on 15 rows promises.'),
                   ('Steps 8 and 9: conclusion and save', 'Three sentences from every learner. Insist on restart and run all before saving.')],
        rescue=['If the concepts run over, skip the illustrative larger-set table and the smooth AUC slide, and say each in one sentence. Keep the standard deviation, log loss, gradient descent, confusion matrix and cost table slides.',
                'If only 40 minutes of lab remain, do steps 1 to 3, 5 and the cost table in step 6. Set the decision tree and the ROC curve as practice for next time.',
                'If the quiz time is under pressure, shorten the lab by dropping the decision tree. The quiz forms must still open today.',
                'If wifi fails in the room, use the offline set-up from Week 2: the notebook runs unchanged in VS Code.',
                'If several learners are stuck at the same cell, stop the room, run that cell on the projector and let them copy the fix.'],
        after=['Share the lab notebook and engineering_data.csv again so absent learners can follow.', 'Confirm in writing the Block 1 close stated on the deck and the two quiz forms.',
               'Note any question you could not answer and start Class 3 with it.'])
    s['numbers_fn'] = 'numbers'
    return s


def numbers(F):
    """Rows of cohort numbers for the guide: F maps cohort code to facts."""
    codes = list(F)
    MM = {c: model_numbers(F[c]) for c in codes}

    def row(label, g):
        return [label] + [g(F[c]) for c in codes]

    def mrow(label, g):
        return [label] + [g(MM[c]) for c in codes]
    d = lambda v: f'{v:.2f}'
    cmf = lambda c: f'{c["tp"]}, {c["fn"]}, {c["fp"]}, {c["tn"]}'
    return [row('Label limit', lambda f: f'{f["b"]["limit"]:g} {f["unit"]}'),
            row('Standard deviation load_pct, ambient_c: StandardScaler (divide by n); pandas .std() (n - 1)',
                lambda f: f'{f["b"]["scaler"]["sd"][0]:.2f}, {f["b"]["scaler"]["sd"][1]:.2f}; {f["trf"].load_pct.std():.2f}, {f["trf"].ambient_c.std():.2f}'),
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
            row('AUC', lambda f: d(f['b']['auc'])),
            mrow('Mean training log loss', lambda m: d(m['train_ll'])),
            mrow('Log loss by hand (p rounded to 2 decimals): validation row 3; the actual negative with the highest p',
                 lambda m: f'{-np.log(round(m["probs"][m["ex"]["k"]], 2)):.2f}; row {m["kn"] + 1}, {-np.log(1 - round(m["probs"][m["kn"]], 2)):.2f}'),
            mrow('Gradient-descent slopes at the start (b0, b1, b2)', lambda m: ', '.join(d(v) for v in m['g0'])),
            mrow('Cost (5 FN + 1 FP) at 0.3, 0.5, 0.7; chosen threshold', lambda m: ', '.join(str(r['cost']) for r in m['cost']) + f'; {m["best"]["th"]:g}'),
            mrow('No StandardScaler (Step 3 CHANGE): weights load, ambient', lambda m: f'{m["raw"]["w"][0]:.3f}, {m["raw"]["w"][1]:.3f}'),
            mrow('No StandardScaler: TP, FN, FP, TN at 0.5; largest probability change', lambda m: cmf(m['raw']['conf']) + f'; {m["raw"]["maxdiff"]:.2f}'),
            mrow('FP at thresholds 0.1 and 0.2 (Step 6 CHANGE)', lambda m: f'{m["low"][0.1]["fp"]}, {m["low"][0.2]["fp"]}'),
            mrow('Points in the student ROC plot (roc_curve default)', lambda m: str(m['roc_sk']))]
