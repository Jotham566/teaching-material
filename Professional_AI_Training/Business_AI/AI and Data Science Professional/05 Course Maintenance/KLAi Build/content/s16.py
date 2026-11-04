"""Session 16: Judging a model (confusion matrix, accuracy and the accuracy paradox, precision, recall, F1, ROC and AUC, precision-recall curve, class_weight, data leakage, stratified k-fold). Python lab.

Every number on a slide, in a note or in the notebook checks comes from facts(): the loans file through content/h_loans.py, which is built on content/loans_canon.py (the one recipe shared by
Sessions 14 to 17, 20, 23 and 24: 8,000 loans, stratified 6,000 / 2,000 split, 27 columns, scaled logistic regression). Every metric is computed in NumPy from those predictions. They are NumPy replica numbers:
re-run on real scikit-learn in Colab before the course starts. The model is the Session 15 logistic regression with the same split.
"""
from functools import lru_cache

import numpy as np

import h_loans as H
from h_loans import n


def pct(x, d=1):
    return f'{x * 100:.{d}f}'


@lru_cache(maxsize=None)
def facts():
    F = dict(H.facts())
    C = H.C
    L, X, y = F['loans'], F['X'], F['y']
    yte, ytr, tr, te = F['yte'], F['ytr'], F['tr'], F['te']
    p = F['p_lr']
    m0 = F['model']
    F['base_acc'] = float((yte == 0).mean())
    F['base_correct'] = int((yte == 0).sum())
    ths = [0.5, 0.3, 0.2, 0.15, 0.1]
    F['ths'] = ths
    F['m'] = {t: dict(F['thr_rows'][t]) for t in ths}
    grid = [round(0.02 + 0.01 * i, 2) for i in range(59)]
    G = {}
    for t in grid:
        c = H.confusion(yte, p >= t)
        G[t] = dict(c, **H.prf(c))
    F['grid'] = G
    F['best_f1_t'] = max(G, key=lambda t: G[t]['f1'])
    F['best_f1_list'] = max(ths, key=lambda t: F['m'][t]['f1'])
    # curves
    fpr, tpr, _ = C.roc_points(yte, p)
    F['roc'] = (fpr, tpr)
    pr, rc, _ = H.pr_points(yte, p)
    F['pr'] = (pr, rc)
    F['auc'] = C.auc_rank(yte, p)
    F['gini'] = 2 * F['auc'] - 1
    F['pairs'] = F['test_pos'] * F['test_neg']
    F['pairs_right'] = int(round(F['auc'] * F['pairs']))
    # AUC computed from yes or no flags instead of probabilities (a common mistake)
    F['auc_from_flags'] = {t: (F['m'][t]['recall'] + 1 - F['m'][t]['fpr']) / 2 for t in ths}
    # class_weight='balanced' inside the same pipeline: the scaler is fitted on the training rows, then the weighted logistic regression
    sw = H.balanced_weights(ytr)
    F['w_repaid'], F['w_default'] = float(len(ytr) / (2 * (ytr == 0).sum())), float(len(ytr) / (2 * (ytr == 1).sum()))
    F['train_neg'] = int((ytr == 0).sum())
    Ztr = (F['Xtr'] - m0.mean_) / m0.scale_
    b, w = H.logreg_fit(Ztr, ytr, sample_weight=sw)
    F['p_w'] = H.predict_p(b, w, F['Zte'])
    F['auc_w'] = C.auc_rank(yte, F['p_w'])
    cw = H.confusion(yte, F['p_w'] >= 0.5)
    F['w05'] = dict(cw, flagged=cw['tp'] + cw['fp'], **H.prf(cw))
    F['plain_match_t'] = min(G, key=lambda t: abs(G[t]['tp'] + G[t]['fp'] - F['w05']['flagged']))
    # leakage: the 27 columns plus collection_calls
    calls = L.collection_calls.to_numpy(float)
    Xl = X.copy()
    Xl['collection_calls'] = L.collection_calls.to_numpy()
    F['Xl'] = Xl
    ml = C.ScaledLogReg().fit(np.column_stack([F['Xtr'], calls[tr]]), ytr)
    F['p_leak'] = ml.predict_proba(np.column_stack([F['Xte'], calls[te]]))
    F['auc_leak'] = C.auc_rank(yte, F['p_leak'])
    cl = H.confusion(yte, F['p_leak'] >= 0.2)
    F['leak02'] = dict(cl, **H.prf(cl))
    F['roc_leak'] = C.roc_points(yte, F['p_leak'])[:2]
    # stratified 5-fold cross-validation on ALL 8,000 loans (folds of 1,600) and on the 6,000 training rows (folds of 1,200)
    fold = C.stratified_kfold(y, 5)
    F['fold'] = fold
    F['fold_n'] = [int((fold == k).sum()) for k in range(5)]
    F['fold_pos'] = [int(y[fold == k].sum()) for k in range(5)]
    F['cv_honest'] = np.array(C.cv_auc(X.to_numpy(float), y))
    F['cv_leak'] = np.array(C.cv_auc(Xl.to_numpy(float), y))
    F['cv_train'] = np.array(C.cv_auc(F['Xtr'], ytr))
    ftr = C.stratified_kfold(ytr, 5)
    F['fold_train_n'] = [int((ftr == k).sum()) for k in range(5)]
    F['fold_train_pos'] = [int(ytr[ftr == k].sum()) for k in range(5)]
    return F


def build():
    F = facts()
    m = F['m']
    M2 = m[0.2]
    M5 = m[0.5]
    G = F['grid']
    W = F['w05']
    lk = F['leak02']
    loans = F['loans']
    base = F['base_acc']
    npos, nneg, nte = F['test_pos'], F['test_neg'], F['n_test']
    best_f1_t = F['best_f1_t']
    cvh, cvl = F['cv_honest'], F['cv_leak']
    assert F['rows'] == 8000 and nte == 2000 and npos == 251 and F['X_shape'][1] == 27
    assert abs(F['auc'] - 0.756) < 0.001 and F['calls_min_default'] == 1 and F['no_calls_default'] == 0
    c_def, c_rep = F['calls_mean'][1], F['calls_mean'][0]
    tp, fp, fn, tn = M2['tp'], M2['fp'], M2['fn'], M2['tn']
    prec, rec, f1, acc = M2['precision'], M2['recall'], M2['f1'], M2['accuracy']
    f1_extreme = 2 * 1.0 * 0.01 / (1.0 + 0.01)

    sess = dict(
        num=16, block='Module D: Machine learning', short_title='Judging a model',
        title='Judging a model: metrics, leakage and imbalance',
        question='How do we tell a model that works from one that only looks good?',
        outcomes=['Read a confusion matrix and compute accuracy, precision, recall and F1 from its four counts',
                  'Read an ROC curve and a precision-recall curve, and choose the metric that matches the cost of each mistake',
                  'Find a leaked column and test a model with stratified cross-validation'],
        outcome_icons=['grid', 'chart', 'shield'],
        outcome_note=('Here is what you can do by the end of today. You can read a confusion matrix and work out accuracy, precision, recall and F1 from its four counts. '
                      'You can read an ROC curve and a precision-recall curve, and choose the metric that fits the cost of each mistake. '
                      'And you can find a column that leaks the answer and test a model with stratified cross-validation. In the lab you will do all of this on the same loans as last session.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: picture, plain words, one example by hand'), (10, 'Break'), (45, 'Lab: predict, run, read, change'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: concepts first, then a Python lab in Colab',
        plan_caption='Ideas with pictures first. Then you open the notebook. Then the checks and what you keep.',
        plan_note=('We have two hours. The first ten minutes bring back Session 15 and set the question for today. Then forty-five minutes of concepts, with no laptops open, so you can watch the pictures and follow the arithmetic. '
                   'After a ten minute break you open the Colab notebook for a forty-five minute lab. You will compute each measure yourself first, then check it against scikit-learn. '
                   'The last ten minutes are an exit check and what you keep. The lab is where the learning sticks, so please protect that time.'),
        recall_from='Session 15',
        recall=[('A logistic regression gives a loan p = 0.30. What does that number mean?', 'The model estimates a 30 percent chance that the loan defaults. A decision threshold turns that probability into a yes or no.'),
                ('Why is 0.50 rarely the right decision threshold?', f'A missed default and a false alarm cost different amounts. At 0.50 our model flags only {m[0.5]["flagged"]} of {n(nte)} loans and misses {m[0.5]["fn"]} of the {npos} defaults.'),
                ('What does one-hot encoding do?', 'It turns a text variable such as occupation into one 0 or 1 indicator column per category, so a model can use it.')],
        words=[('Confusion matrix (TP, FP, FN, TN)', 'A table that counts every kind of right and wrong prediction: true positives, false positives, false negatives and true negatives.'),
               ('Precision, recall and F1', 'Precision: of the loans flagged, the share that defaulted. Recall: of the loans that defaulted, the share flagged. F1 combines both.'),
               ('ROC curve and AUC', 'The ROC curve plots the true positive rate (recall, sensitivity) against the false positive rate at every threshold. AUC, the area under it, is 0.5 for a coin flip and 1.0 for a perfect model.'),
               ('Data leakage (target leakage)', 'A feature that contains the answer, or information only known after the outcome. It makes a model look brilliant and fail in real use.'),
               ('Stratified k-fold cross-validation', 'Test the model k times, each time on a different fold, with every fold keeping the same share of defaults. Average the scores. Use it to tune before you test.')],
        word_icons=['grid', 'chart', 'magnifier', 'lock', 'calendar'],
        words_note=('Five words for today. A confusion matrix counts every kind of right and wrong prediction. Precision, recall and F1 answer different questions about the loans we flag. '
                    'The ROC curve and its area, AUC, judge a model at every threshold at once. Data leakage means a column hides the answer. '
                    'And stratified k-fold cross-validation tests the model several times on different parts of the data. We use every one of them before the end of the session.'),
        keep='Your notebook and a file model_comparison.csv with the evaluation metrics of each model you tested, plus one sentence on the leaked column and what it did to the AUC.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab files', value='Notebook, comparison'), dict(label='The habit', value='Never trust one number'), dict(label='Next session', value='Forests and boosting')]),
        keep_title='Save your notebook and your model comparison table',
        next='Session 17: Forests, boosting and overfitting. We build stronger models and learn to stop fooling ourselves with them.', next_label='Next session',
        keep_note=('Before you go, save your notebook and the model comparison table. The table is your keepsake: one row per model with precision, recall, F1 and AUC, so a colleague can see at a glance which model to trust and why. '
                   'Keep the sentence about the leaked column too. It is the most valuable habit of today, because a model that looks too good should always make you ask where the answer came from. '
                   'Next session we build stronger models. If anything was unclear today, write the question down and bring it.'),
        cover_note=('Welcome back. Last session you built two models that give each loan a probability of default, and you chose a decision threshold on the training loans from the cost of a mistake. Today the question is harder. '
                    'How do we tell a model that works from one that only looks good? We stay with the same loans. You will read a confusion matrix, say what precision and recall mean in plain words, and catch a model that cheats.'),
        use_at_work='Judge any classifier with the right metric, catch leaked columns, and test with cross-validation before you report a score.',
        slides=[])
    S = sess['slides']

    # ------------------------------------------------------------------ 1 answers
    S.append(dict(kind='table', title='Answers to the three questions from Session 15', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in sess['recall']], widths=[4.4, 7.6], icons=['chart', 'switch', 'grid'],
                  notes=(f'Here are the answers to the three warm-up questions. A probability of point three is the model\'s estimate of a thirty percent chance of default, and the threshold turns it into yes or no. '
                         f'Point five is rarely right, because the two mistakes cost different amounts. At point five our model flags only {m[0.5]["flagged"]} loans out of {n(nte)} and misses {m[0.5]["fn"]} of the {npos} defaults. '
                         'And one-hot encoding gives each category its own column of zero and one. Which of the three did you find hardest?')))

    # ------------------------------------------------------------------ 2 baseline stat
    S.append(dict(kind='stat', title=f'A baseline model that flags nobody is right {pct(base, 2)} percent of the time', big=f'{pct(base, 2)}%',
                  text=f'{n(nneg)} of the {n(nte)} test loans were repaid. Saying "no default" for every loan is correct for all of them, and it finds none of the {npos} defaults.', waffle_label=f'About {round(base * 100)} of every 100 test loans are right',
                  notes=(f'Start with a trick question. Take the baseline model from Session 14: it says no default for every loan. On our {n(nte)} test loans, which hold {npos} defaults, {n(nneg)} were repaid, so the baseline is right {pct(base, 2)} percent of the time. '
                         f'It looks like a strong number, and it finds none of the {npos} defaults. The reason is class imbalance: the positive class is rare, so the majority class wins by doing nothing. '
                         'The share of answers that are right is called accuracy, and today we see why it cannot be the only number we look at. Would you hire a credit officer who approves every loan?')))

    # ------------------------------------------------------------------ 3 confusion matrix
    S.append(dict(kind='idea', title='The confusion matrix counts every kind of right and wrong prediction',
                  visual=dict(kind='dsh_confusion', tp=tp, fp=fp, fn=fn, tn=tn, focus='none'),
                  lead=f'Logistic regression at threshold 0.20 on the {n(nte)} test loans.',
                  points=['Rows: what really happened (actual). Columns: what the model said (predicted).', 'Positive class: default. Negative class: repaid.', 'Each loan lands in exactly one of the four cells.'],
                  notes=(f'This table is the most useful picture for judging a classifier. It is called a confusion matrix, and it is just a count table. In Excel you would build it with COUNTIFS. '
                         f'The rows are what really happened and the columns are what the model said. We use the scikit-learn layout, with the negative class first. These are the {n(nte)} test loans at a threshold of point two. '
                         f'Bottom right, true positives: {n(tp)} defaults the model flagged. Top right, false positives: {n(fp)} repaid loans flagged by mistake. Bottom left, false negatives: {n(fn)} defaults the model missed. Top left, true negatives: {n(tn)} repaid loans rightly cleared. '
                         f'The four numbers add up to {n(tp + fp + fn + tn)}. Which cell worries a lender most?')))

    # ------------------------------------------------------------------ 4 the four outcomes
    S.append(dict(kind='table', title='Each cell has a name: the second word is the prediction, the first says whether it was right',
                  headers=['Cell', 'Name', 'Plain meaning', 'Count'],
                  rows=[['TP', 'True positive', 'Flagged, and it really defaulted: a good catch.', n(tp)], ['FP', 'False positive', 'Flagged, but the loan was repaid: a false alarm.', n(fp)],
                        ['FN', 'False negative', 'Not flagged, but it defaulted: a missed default.', n(fn)], ['TN', 'True negative', 'Not flagged, and it was repaid: rightly cleared.', n(tn)]],
                  widths=[1.2, 2.8, 6.2, 1.8], icons=['check', 'bell', 'cross', 'shield'], note='In pandas: ((y_pred == 1) & (y_test == 1)).sum() counts the true positives. A type I error is a false positive, a type II error a false negative (Session 12).',
                  notes=(f'Here are the four names. The second word is what the model predicted: positive means flagged, negative means cleared. The first word says whether the prediction was right: true or false. '
                         f'So a false positive is flagged but wrong, a false alarm, and a false negative is cleared but wrong, a missed default. At threshold point two we have {n(tp)} true positives, {n(fp)} false positives, {n(fn)} false negatives and {n(tn)} true negatives. '
                         'If you studied statistics, a false positive is a type one error and a false negative is a type two error, as in Session 12. Which of the four counts would you report to a credit committee first?')))

    # ------------------------------------------------------------------ 5 accuracy formula
    S.append(dict(kind='formula', title='Accuracy is the share of right answers, and it can reward doing nothing',
                  formulas=[('accuracy', r'$\mathrm{accuracy} = \frac{TP + TN}{TP + FP + FN + TN}$')],
                  symbols=[['TP, TN', 'True positives and true negatives: the right answers', f'{n(tp)} and {n(tn)}'], ['FP, FN', 'False positives and false negatives: the wrong answers', f'{n(fp)} and {n(fn)}'],
                           ['Model at 0.20', f'({n(tp)} + {n(tn)}) / {n(nte)}', f'{M2["accuracy"]:.3f}'], ['Baseline: flag nobody', f'(0 + {n(nneg)}) / {n(nte)}', f'{base:.3f}'],
                           ['Verdict', 'The baseline has higher accuracy and catches no default', 'accuracy paradox']],
                  widths=[2.8, 5.6, 3.5], size=26, note='Accuracy paradox: with a rare positive class, accuracy can rise while the model gets less useful.',
                  notes=(f'Accuracy is the number of right answers divided by all answers. Our model at threshold point two has {n(tp)} true positives and {n(tn)} true negatives, out of {n(nte)} loans, so accuracy is {M2["accuracy"]:.3f}. '
                         f'Now the baseline that flags nobody: no true positives, but {n(nneg)} true negatives, so its accuracy is {base:.3f}. The baseline beats our model on accuracy, yet it finds no defaults. '
                         'That is the accuracy paradox: when the positive class is rare, accuracy rewards doing nothing. So we need measures that look at the positive class on purpose. Is a high accuracy ever enough?')))

    # ------------------------------------------------------------------ 6 paradox bars
    S.append(dict(kind='wide', title='The accuracy paradox: the model that finds nothing has a high accuracy',
                  visual=dict(kind='dsh_groupbars', legend=['accuracy', 'recall'], groups=[dict(label='Baseline: flag nobody', values=[base, 0.0], texts=[f'{base:.2f}', '0.00']),
                                                                                         dict(label='Model, threshold 0.50', values=[M5['accuracy'], M5['recall']], texts=[f'{M5["accuracy"]:.2f}', f'{M5["recall"]:.2f}']),
                                                                                         dict(label='Model, threshold 0.20', values=[M2['accuracy'], M2['recall']], texts=[f'{M2["accuracy"]:.2f}', f'{M2["recall"]:.2f}']),
                                                                                         dict(label='Model, threshold 0.10', values=[m[0.1]['accuracy'], m[0.1]['recall']], texts=[f'{m[0.1]["accuracy"]:.2f}', f'{m[0.1]["recall"]:.2f}'])]),
                  caption=f'Recall: the share of the {npos} defaults flagged. Accuracy falls as the model finds more.',
                  notes=(f'Look at the gold bars, recall, the share of the {npos} real defaults that the model flags. The baseline has recall zero and an accuracy of {base:.2f}, within {(M5["accuracy"] - base) * 100:.0f} points of the model at point five. '
                         f'At a threshold of point five the model has accuracy {M5["accuracy"]:.2f} and recall {M5["recall"]:.2f}: it finds only one default in five. At point two accuracy drops to {M2["accuracy"]:.2f} and recall rises to {M2["recall"]:.2f}. '
                         f'At point one recall reaches {m[0.1]["recall"]:.2f} and accuracy is {m[0.1]["accuracy"]:.2f}. The model that is more useful has a lower accuracy. Which bar would you show your manager?')))

    # ------------------------------------------------------------------ 7 precision and recall formulas
    S.append(dict(kind='formula', title='Precision and recall each ask a different question about the positive class',
                  formulas=[('precision', r'$\mathrm{precision} = \frac{TP}{TP + FP}$'), ('recall', r'$\mathrm{recall} = \frac{TP}{TP + FN}$')],
                  symbols=[['Precision', 'Of the loans flagged, the share that really defaulted', f'{n(tp)} / ({n(tp)} + {n(fp)}) = {prec:.3f}'],
                           ['Recall', 'Of the loans that defaulted, the share flagged. Also sensitivity or true positive rate', f'{n(tp)} / ({n(tp)} + {n(fn)}) = {rec:.3f}'],
                           ['TP + FP', 'All loans flagged (the predicted-positive column)', f'{n(tp + fp)}'], ['TP + FN', 'All loans that defaulted (the actual-positive row)', f'{n(tp + fn)}']],
                  widths=[1.9, 6.0, 4.0], size=26,
                  notes=(f'Precision and recall both start from the true positives, but divide by different things. Precision divides by everything we flagged, true positives plus false positives. It answers: when the model says default, how often is it right? '
                         f'Here {n(tp)} divided by {n(tp + fp)} is {prec:.3f}, about {pct(prec, 0)} percent. Recall divides by everything that really defaulted, true positives plus false negatives. It answers: of the real defaults, how many did we catch? '
                         f'{n(tp)} divided by {n(tp + fn)} is {rec:.3f}, about {pct(rec, 0)} percent. Recall is also called sensitivity or the true positive rate. Which of the two would a lender with little cash worry about first?')))

    # ------------------------------------------------------------------ 8 precision picture
    S.append(dict(kind='idea', title='Precision reads down the column of flagged loans',
                  visual=dict(kind='dsh_confusion', tp=tp, fp=fp, fn=fn, tn=tn, focus='precision'),
                  lead=f'Of {n(tp + fp)} loans flagged, {n(tp)} defaulted: precision {prec:.2f}.',
                  points=['High precision: few false alarms. A flag can be trusted.', 'Watch it when each flag costs a person\'s time, such as a manual review.', f'Low here: about {pct(1 - prec, 0)} percent of flags are good borrowers.'],
                  notes=(f'Here is precision as a picture. The gold column holds every loan the model flagged: {n(tp)} true positives and {n(fp)} false positives, {n(tp + fp)} in all. Precision is the gold cell divided by the whole column, {prec:.2f}. '
                         f'So when this model says default, it is right about {pct(prec, 0)} percent of the time, and about {pct(1 - prec, 0)} percent of the flags are good borrowers. '
                         'Precision matters most when each flag costs something, for example when a fraud analyst must review every flagged transaction by hand. What would a precision of ninety percent let you do?')))

    # ------------------------------------------------------------------ 9 recall picture
    S.append(dict(kind='idea', title='Recall reads along the row of loans that really defaulted',
                  visual=dict(kind='dsh_confusion', tp=tp, fp=fp, fn=fn, tn=tn, focus='recall'),
                  lead=f'Of {npos} defaults, {n(tp)} were flagged: recall {rec:.2f}.',
                  points=['High recall: few missed defaults.', 'Watch it when a miss is expensive, as in lending, disease screening and fraud.', f'Here the model misses {n(fn)} of the {npos} defaults.'],
                  notes=(f'And recall as a picture. The gold row holds every loan that really defaulted: {n(tp)} caught and {n(fn)} missed, {npos} in all. Recall is the gold cell divided by the whole row, {rec:.2f}. '
                         f'The model finds about {pct(rec, 0)} percent of the defaults and misses the other {pct(1 - rec, 0)} percent. Recall matters most when a miss is expensive, as with a lender who never recovers a defaulted loan, '
                         'or a clinic that must not miss a sick patient. Notice that you can always get recall of one hundred percent by flagging every loan. That is why recall alone is not enough. Why would that be a bad model?')))

    # ------------------------------------------------------------------ 10 F1
    S.append(dict(kind='formula', title='F1 combines precision and recall in one number, and punishes a big gap between them',
                  formulas=[('F1 score', r'$F_1 = \frac{2 \times \mathrm{precision} \times \mathrm{recall}}{\mathrm{precision} + \mathrm{recall}}$')],
                  symbols=[['Model at 0.20', f'2 x {prec:.3f} x {rec:.3f} / ({prec:.3f} + {rec:.3f})', f'{f1:.3f}'], ['Why not the plain mean?', 'Precision 1.00 and recall 0.01: the mean is 0.505, F1 is', f'{f1_extreme:.3f}'],
                           ['Name', 'F1 is the harmonic mean of precision and recall', ''], ['Use', 'One number to compare thresholds or models when both mistakes matter', '']],
                  widths=[2.8, 6.4, 2.7], size=26, note='F1 ignores the true negatives. It is 0 when nothing is caught and 1 when every flag is right and every default is found.',
                  notes=(f'F1 is the harmonic mean of precision and recall. At threshold point two, precision is {prec:.3f} and recall {rec:.3f}, and F1 is {f1:.3f}. '
                         f'Why do we avoid the plain average of the two? Imagine a model that flags one loan, gets it right, and finds one in a hundred defaults: precision one, recall point zero one. The plain mean says point five, which sounds respectable. '
                         f'F1 says {f1_extreme:.3f}, which is honest. F1 stays low unless both numbers are decent. It ignores true negatives completely, and it treats precision and recall as equally important, which a lender may not. Where would you want a weighted version?')))

    # ------------------------------------------------------------------ 11 thresholds table
    S.append(dict(kind='table', title=f'Every threshold gives different metrics, and F1 is highest at {F["best_f1_list"]:.2f} of these five' + (f' ({best_f1_t:.2f} if you check every step of 0.01)' if abs(best_f1_t - F['best_f1_list']) > 1e-9 else ''),
                  headers=['Threshold', 'Precision', 'Recall', 'F1', 'Accuracy'], rows=[[f'{t:.2f}', f'{m[t]["precision"]:.3f}', f'{m[t]["recall"]:.3f}', f'{m[t]["f1"]:.3f}', f'{m[t]["accuracy"]:.3f}'] for t in F['ths']],
                  widths=[2.2, 2.4, 2.4, 2.4, 2.4], icons=['lock', 'lock', 'switch', 'bell', 'bell'], hl_col=3, note=f'Baseline for comparison: accuracy {base:.3f}, recall 0. Logistic regression on {n(nte)} test loans. Gold: F1.',
                  notes=(f'Now the same four measures at five thresholds. As the threshold falls, recall rises from {m[0.5]["recall"]:.2f} to {m[0.1]["recall"]:.2f}, because we flag more loans. Precision falls from {m[0.5]["precision"]:.2f} to {m[0.1]["precision"]:.2f}, because more of the flags are false alarms. '
                         f'Accuracy falls too. F1, the gold column, is highest at {F["best_f1_list"]:.2f} in this list, with {m[F["best_f1_list"]]["f1"]:.3f}. Searching every threshold in steps of point zero one, the best F1 is at {best_f1_t:.2f}. '
                         'No threshold wins on every column. The choice depends on which mistake costs more. Which row would you choose for a lender with plenty of cash?')))

    # ------------------------------------------------------------------ 12 lines vs threshold
    ts = sorted(G)
    S.append(dict(kind='wide', title='Raising the threshold buys precision and spends recall',
                  visual=dict(kind='dsh_curve', xlabel='decision threshold', ylabel='metric value', xlim=(0, 0.6), ylim=(0, 1), xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], yticks=[0, 0.25, 0.5, 0.75, 1],
                              curves=[dict(points=[(t, G[t]['recall']) for t in ts], label='recall', lx=0.07, ly=0.6, color='red'), dict(points=[(t, G[t]['precision']) for t in ts], label='precision', lx=0.5, ly=0.76, color='ink'),
                                      dict(points=[(t, G[t]['f1']) for t in ts], label=f'F1 (dashed): highest near {best_f1_t:.2f}', lx=0.26, ly=0.07, color='mute', dash=True)],
                              marks=[dict(x=best_f1_t, y=G[best_f1_t]['f1'], label='', fill='#E0BE36')]),
                  caption=f'Logistic regression on the {n(nte)} test loans, thresholds 0.02 to 0.60.',
                  notes=(f'This picture draws the table for every threshold. The red line is recall: it is high when the threshold is low and falls as we raise it. The black line is precision: it climbs as the threshold rises, '
                         'although it gets jumpy on the right where only a few loans are flagged. The dashed line is F1, which peaks in the middle, here near ' + f'{best_f1_t:.2f}' + ', and the gold dot marks it. '
                         'No threshold gives high precision and high recall together, because the model cannot separate every defaulter from every good borrower. A better model pushes both lines up. Where do the red and black lines cross?')))

    # ------------------------------------------------------------------ 13 which metric
    S.append(dict(kind='table', title='Choose the metric from the cost of the mistake, not from habit',
                  headers=['If the costly mistake is', 'Watch', 'Example'],
                  rows=[['A missed positive (false negative)', 'Recall', 'A lender who cannot recover a defaulted loan.'], ['A false alarm (false positive)', 'Precision', 'A fraud team that can review only 50 cases a day.'],
                        ['Both matter and the classes are lopsided', 'F1', 'Comparing two thresholds in one number.'], ['You need the quality of the ranking, before choosing a threshold', 'AUC', 'Choosing between two models.'],
                        ['The classes are balanced and the costs are equal', 'Accuracy', 'Rare: check the balance first.']],
                  widths=[4.8, 1.8, 5.4], icons=['cross', 'bell', 'chart', 'magnifier', 'check'],
                  notes=('Which measure should you report? Ask which mistake costs more. If missing a positive is the expensive mistake, as with an unrecovered loan, watch recall. If false alarms are expensive, as when a fraud team can review only fifty cases a day, watch precision. '
                         'If both matter and the classes are lopsided, F1 gives one number. If you want to judge the quality of the ranking before you pick a threshold, use AUC, which we meet next. Accuracy is fine only when the classes are balanced and the mistakes cost the same, which is rare. Which row describes your own work?')))

    # ------------------------------------------------------------------ 14 ROC
    fpr, tpr = F['roc']
    pts = [(float(a), float(b)) for a, b in zip(fpr, tpr)]
    S.append(dict(kind='wide', title='The ROC curve plots the true positive rate against the false positive rate at every threshold',
                  visual=dict(kind='dsh_curve', curves=[dict(points=pts, label='', color='ink')], area=0, area_label=f'Gold area = AUC {F["auc"]:.2f}', baseline='diag', baseline_label='Coin flip: AUC 0.50', baseline_at=(0.72, 0.4),
                              xlabel='false positive rate, FPR = FP / (FP + TN)', ylabel='true positive rate, TPR = recall', xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.25, 0.5, 0.75, 1],
                              marks=[dict(x=m[t]['fpr'], y=m[t]['recall'], label=f'threshold {t:.2f}', dx=0.2, dy=-0.22) for t in (0.5, 0.2, 0.1)]),
                  caption='Each dot is one threshold. Lower threshold: more defaults caught, more false alarms.',
                  notes=(f'The ROC curve, short for receiver operating characteristic, draws every threshold on one picture. Up is the true positive rate, which is recall, also called sensitivity: the share of defaults caught. Across is the false positive rate: the share of repaid loans that were flagged by mistake. '
                         f'Each dot is a threshold. At point five we sit near the bottom left: false positive rate {m[0.5]["fpr"]:.2f}, recall {m[0.5]["recall"]:.2f}. At point two we reach recall {m[0.2]["recall"]:.2f} for a false positive rate of {m[0.2]["fpr"]:.2f}. At point one, recall {m[0.1]["recall"]:.2f} and false positive rate {m[0.1]["fpr"]:.2f}. '
                         'The dashed diagonal is a coin flip. The further the curve bows towards the top left, the better the model. Which threshold would you pick on this curve?')))

    # ------------------------------------------------------------------ 15 AUC
    S.append(dict(kind='stat', title=f'AUC {F["auc"]:.2f}: a random defaulter outranks a random repaid loan {pct(F["auc"], 0)} percent of the time', big=f'{F["auc"]:.2f}',
                  text=f'{npos} defaults and {n(nneg)} repaid loans make {n(F["pairs"])} pairs. In {n(F["pairs_right"])} the defaulter ranks higher. 0.50 is a coin flip. Gini = 2 x AUC - 1 = {F["gini"]:.2f}.',
                  notes=(f'AUC is the area under the ROC curve, and it has a friendly meaning. Take one loan that defaulted and one that was repaid, both picked at random. The AUC is the chance that the model gave the defaulter the higher probability. '
                         f'We have {npos} defaults and {n(nneg)} repaid test loans, which makes {n(F["pairs"])} pairs. In {n(F["pairs_right"])} of them the defaulter ranks higher, and that share is {F["auc"]:.3f}. '
                         f'A coin flip scores point five and a perfect model scores one. As a rule of thumb, 0.5 to 0.7 is weak, 0.7 to 0.8 is fair, and above 0.9 deserves a leakage check. Credit teams report the Gini coefficient, two times AUC minus one, here {F["gini"]:.2f}. How would you describe a fair model to a manager?')))

    # ------------------------------------------------------------------ 16 PR curve
    pr, rc = F['pr']
    sel = [(float(r), float(p_)) for p_, r in zip(pr, rc) if r > 0.02]
    S.append(dict(kind='wide', title='The precision-recall curve is the clearer view when the positive class is rare',
                  visual=dict(kind='dsh_curve', curves=[dict(points=sel, label='', color='ink')], baseline=F['test_rate'], baseline_label=f'Flag at random: precision {F["test_rate"]:.3f}', baseline_at=(0.32, 0.2),
                              xlabel='recall = TP / (TP + FN)', ylabel='precision = TP / (TP + FP)', xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.25, 0.5, 0.75, 1],
                              marks=[dict(x=m[t]['recall'], y=m[t]['precision'], label=f'threshold {t:.2f}', dx=0.2, dy=0.12) for t in (0.5, 0.2, 0.1)]),
                  caption='Each dot is one threshold. A model with no skill sits on the dashed line.',
                  notes=(f'The precision recall curve plots precision against recall at every threshold. Here a model with no skill would flag loans at random and have a precision equal to the default rate in the test set, {F["test_rate"]:.3f}, the dashed line. '
                         f'Our model sits well above it. At point five, precision is {m[0.5]["precision"]:.2f} but recall only {m[0.5]["recall"]:.2f}. At point one, recall is {m[0.1]["recall"]:.2f} and precision has fallen to {m[0.1]["precision"]:.2f}. '
                         'When the positive class is rare, this curve is more honest than the ROC curve, because the ROC curve counts the huge number of true negatives and can look flattering. Which curve would you show a risk committee?')))

    # ------------------------------------------------------------------ 17 class weight picture
    S.append(dict(kind='wide', title='class_weight="balanced" makes each rare default count more when the model learns',
                  visual=dict(kind='dsh_weights', repaid=F['train_neg'], defaulted=F['train_pos'], w_repaid=F['w_repaid'], w_default=F['w_default']),
                  caption=f'Weight = rows / (2 x rows in class). Each default counts like {F["w_default"] / F["w_repaid"]:.1f} repaid loans.',
                  notes=(f'Class imbalance means the model sees far more repaid loans than defaults: {n(F["train_neg"])} against {n(F["train_pos"])} in the training set. A model trained on that can drift toward always saying no. '
                         f'The setting class weight equal to balanced gives each row a weight, the number of training rows divided by two times the rows in its class. A repaid loan gets {F["w_repaid"]:.2f}, a default gets {F["w_default"]:.2f}. '
                         f'So each default counts like {F["w_default"] / F["w_repaid"]:.1f} repaid loans, and both classes carry the same total weight, about {n(round(F["train_neg"] * F["w_repaid"]))}. Why might that change what the model predicts?')))

    # ------------------------------------------------------------------ 18 class weight effect
    S.append(dict(kind='table', title='class_weight shifts the probabilities upward, but the ranking and the AUC hardly change',
                  headers=['Logistic regression', 'Flagged', 'Recall', 'Precision', 'F1', 'AUC'],
                  rows=[['Plain, threshold 0.50', n(M5['flagged']), f'{M5["recall"]:.3f}', f'{M5["precision"]:.3f}', f'{M5["f1"]:.3f}', f'{F["auc"]:.3f}'],
                        ['Balanced, threshold 0.50', n(W['flagged']), f'{W["recall"]:.3f}', f'{W["precision"]:.3f}', f'{W["f1"]:.3f}', f'{F["auc_w"]:.3f}'],
                        [f'Plain, threshold {F["plain_match_t"]:.2f}', n(G[F["plain_match_t"]]['tp'] + G[F["plain_match_t"]]['fp']), f'{G[F["plain_match_t"]]["recall"]:.3f}', f'{G[F["plain_match_t"]]["precision"]:.3f}', f'{G[F["plain_match_t"]]["f1"]:.3f}', f'{F["auc"]:.3f}']],
                  widths=[3.9, 1.4, 1.5, 1.7, 1.2, 1.2], icons=['lock', 'switch', 'bell'], note=f'On the {n(nte)} test loans. Balanced weights at 0.50 behave like the plain model at a threshold near {F["plain_match_t"]:.2f}.',
                  notes=(f'Here is what the weights do. With the usual threshold of point five, the plain model flags {n(M5["flagged"])} loans and has recall {M5["recall"]:.2f}. The balanced model flags {n(W["flagged"])} loans and has recall {W["recall"]:.2f}, with a lower precision of {W["precision"]:.2f}. '
                         f'That is very close to what the plain model does at a threshold of about {F["plain_match_t"]:.2f}, which you can see in the last row. The AUC barely moves, {F["auc"]:.3f} against {F["auc_w"]:.3f}, because the ranking of loans is nearly the same. '
                         'So class weight is another way of moving the decision threshold, and it distorts the probabilities, so they no longer mean a true chance. If you need honest probabilities, keep the plain model and move the threshold. Which would you prefer?')))

    # ------------------------------------------------------------------ 19 leakage timeline
    S.append(dict(kind='wide', title='Target leakage: collection_calls is recorded only after the loan has gone bad',
                  visual=dict(kind='dsh_leak_timeline', decision=1, events=[dict(when='Application', what='age, income, loan amount, occupation'), dict(when='Approval: predict here', what='instalment-to-income ratio, savings, late payments'),
                                                                           dict(when='Missed payments', what='the loan is in default'), dict(when='Recovery', what='collection_calls: staff phone the borrower')]),
                  caption='A feature is usable only if it exists at the moment the lender must decide.',
                  notes=(f'Now a danger that has fooled many professionals. Data leakage means the model sees information it would not have in real use. Here the loans file has a column called collection calls. It counts the phone calls the collections team made to the borrower. '
                         f'Those calls happen only after a borrower stops paying. On the timeline, the lender must decide at approval, the red dashed line. Application and approval data exists then. The collection calls come after the default. '
                         f'The data dictionary says it plainly: the column is recorded only after a loan goes bad. A model that uses it is told the answer by the answer. This kind is called target leakage. Which columns in your own files appear only after the outcome?')))

    # ------------------------------------------------------------------ 20 leak numbers
    S.append(dict(kind='table', title=f'The leaked column almost equals the answer: {c_def:.2f} calls on average for defaults, {c_rep:.2f} for repaid loans',
                  headers=['Check on the loans file', 'Result'],
                  rows=[['Average collection_calls, defaulted loans', f'{c_def:.2f}'], ['Average collection_calls, repaid loans', f'{c_rep:.2f}'], ['Fewest calls on any defaulted loan', f'{F["calls_min_default"]}: every default has at least one call'],
                        ['Repaid loans with at least one call', f'{pct(F["share_repaid_with_call"], 0)} percent'], ['Correlation with default, the strongest of all variables', f'{F["corr_calls"]:.2f}'], ['Next strongest: instalment_to_income', f'{F["corr_top"][1][1]:.2f}']],
                  widths=[7.0, 5.0], icons=['phone', 'phone', 'flag', 'people', 'chart', 'chart'],
                  notes=(f'Here is how you would find a leaked column. Compare the column across the two outcomes. Defaulted loans average {c_def:.2f} calls and repaid loans {c_rep:.2f}. Every single defaulted loan has at least one call. '
                         f'The correlation of collection calls with default is {F["corr_calls"]:.2f}, far above the next strongest variable, the instalment-to-income ratio, at {F["corr_top"][1][1]:.2f}. '
                         'A feature that predicts almost perfectly and is recorded after the event is the signature of target leakage. The honest question is when the feature is recorded. Who in your organisation could tell you when each column is filled in?')))

    # ------------------------------------------------------------------ 21 leaky ROC
    S.append(dict(kind='wide', title=f'An AUC of {F["auc_leak"]:.3f} should make you suspicious: the leaky model peeks at the answer',
                  visual=dict(kind='dsh_curve', curves=[dict(points=[(float(a), float(b)) for a, b in zip(*F['roc_leak'])], label=f'With collection_calls: AUC {F["auc_leak"]:.3f}', lx=0.2, ly=0.8, color='red'),
                                                        dict(points=pts, label=f'Honest model: AUC {F["auc"]:.3f}', lx=0.52, ly=0.45, color='ink')], baseline='diag',
                              xlabel='false positive rate', ylabel='true positive rate = recall', xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.25, 0.5, 0.75, 1]),
                  caption=f'Same loans, same method. At 0.20 the leaky model shows precision {lk["precision"]:.2f}, recall {lk["recall"]:.2f}.',
                  notes=(f'Add collection calls to the features and fit the same logistic regression. The red curve hugs the top left corner: AUC {F["auc_leak"]:.3f}. The honest model, in black, has {F["auc"]:.3f}. '
                         f'At a threshold of point two the leaky model reports precision {lk["precision"]:.2f} and recall {lk["recall"]:.2f}, against {prec:.2f} and {rec:.2f} for the honest one. It looks wonderful. '
                         'But it would fail on the day you use it, because a new applicant has no collection calls yet. The rule of thumb: a result that looks too good to be true usually is. Investigate before you celebrate. What would you ask the analyst who showed you this curve?')))

    # ------------------------------------------------------------------ 22 types of leakage
    S.append(dict(kind='table', title='Leakage has several forms, and each has a habit that prevents it',
                  headers=['Form of leakage', 'Example', 'Prevention'],
                  rows=[['Target leakage: a feature recorded after the outcome', 'collection_calls in the loans file', 'Ask when each column is recorded. Drop what is not known at decision time.'],
                        ['Train-test contamination: test rows influence training', 'Filling missing income with the median of all loans, before the split', 'Split first. Fit imputers and scalers on the training set only. A scikit-learn Pipeline does this.'],
                        ['Duplicates across the split', 'The same borrower in the training and test sets', 'Remove duplicates before splitting, or split by borrower.'],
                        ['Future information (time)', 'Using next month\'s repayment to predict this month', 'Split by date: train on the past, test on the future.']],
                  widths=[3.9, 3.9, 4.2], icons=['clock', 'folder', 'people', 'calendar'],
                  notes=('Target leakage is the most famous form, but not the only one. Train test contamination happens when information from the test rows reaches the model, for example when you fill missing incomes with the median of all loans before you split. '
                         'The fix is to split first and fit every imputer and scaler on the training set only, which a scikit-learn pipeline does for you. Duplicates can sit in both sets, so the model has seen the test borrower already. '
                         'And in time series, using the future to predict the past is leakage too, so split by date. Note that in Sessions 14 and 15 we computed the median income before splitting, on purpose: a small contamination that we accepted for teaching. The safe-order slide of Session 14 shows the pipeline version. Which form could affect your data?')))

    # ------------------------------------------------------------------ 23 cv picture
    fold_subs = [f'{n(F["fold_n"][k])} loans\n{F["fold_pos"][k]} defaults' for k in range(5)]
    S.append(dict(kind='wide', title='Stratified 5-fold cross-validation tests the model five times, each fold with the same default rate',
                  visual=dict(kind='dsh_folds', k=5, subs=fold_subs, scores=[f'{v:.3f}' for v in cvh], summary=f'Mean AUC {cvh.mean():.3f}, standard deviation {cvh.std(ddof=1):.3f}', unit='AUC'),
                  caption='Five folds of 1,600 loans from all 8,000. Every loan is in the validation fold (gold) once.',
                  notes=(f'One train test split can be lucky or unlucky. Cross-validation repeats the test. We cut the {n(F["rows"])} loans into five folds. In each round, one fold is the validation fold, in gold, and the other four train the model, in black. '
                         f'Stratified means each fold keeps the same share of defaults as the whole file: {n(F["fold_n"][0])} loans and 200 or 201 defaults in every fold, so no fold is accidentally easy. The file is in date order, so without shuffling each fold is a block of months. '
                         f'The five AUC scores are {", ".join(f"{v:.3f}" for v in cvh)}. Their mean is {cvh.mean():.3f} and the standard deviation is {cvh.std(ddof=1):.3f}. The spread tells you how much one lucky split could mislead. Why report the spread as well as the mean?')))

    # ------------------------------------------------------------------ 24 cv table honest vs leaky
    S.append(dict(kind='table', title=f'Cross-validation agrees: the honest model is about {cvh.mean():.2f}, and the leaky one is too good to be true',
                  headers=['Model', 'Round 1', '2', '3', '4', '5', 'Mean', 'Std'],
                  rows=[['Honest features'] + [f'{v:.3f}' for v in cvh] + [f'{cvh.mean():.3f}', f'{cvh.std(ddof=1):.3f}'], ['Plus collection_calls'] + [f'{v:.3f}' for v in cvl] + [f'{cvl.mean():.3f}', f'{cvl.std(ddof=1):.3f}']],
                  widths=[3.0, 1.2, 1.0, 1.0, 1.0, 1.0, 1.4, 1.2], icons=['check', 'cross'], hl_col=6, note='AUC on each validation fold of the 8,000 loans. Std: sample standard deviation. Cross-validation cannot detect leakage by itself: the leaked column is in every fold.',
                  notes=(f'Here are all five rounds for the two models. The honest model scores between {cvh.min():.2f} and {cvh.max():.2f}, mean {cvh.mean():.3f}. The leaky model scores above {cvl.min():.3f} in every round, mean {cvl.mean():.3f}. '
                         'Notice an important point: cross-validation did not catch the leak. The leaked column is available in every fold, so every fold looks wonderful. Cross-validation tells you whether a score is stable. It cannot tell you whether the score is honest. '
                         'Only asking when a column is recorded can do that. Which job does cross-validation do, and which job does the question when is it recorded do?')))

    # ------------------------------------------------------------------ 24b tune before you test
    cvt = F['cv_train']
    S.append(dict(kind='table', title='Tune before you test: choose settings on a validation set or by cross-validation, then score the test loans once',
                  headers=['Job', 'Which loans', 'Example in this course'],
                  rows=[['Fit the parameters', f'Training loans ({n(F["n_train"])})', 'The coefficients of the logistic regression'],
                        ['Tune the settings (decision threshold, tree depth: hyperparameters)', f'A validation set, or 5-fold cross-validation inside the training loans (folds of {n(F["fold_train_n"][0])})', f'The threshold {F["cv_t"]:.2f} in Session 15. Cross-validated AUC {cvt.mean():.3f}, spread {cvt.std(ddof=1):.3f}'],
                        ['Report the final score, once', f'Test loans ({n(nte)}), never used for tuning', f'AUC {F["auc"]:.3f} and the cost of the chosen threshold']],
                  widths=[3.5, 4.8, 3.7], icons=['gear', 'calendar', 'lock'], note='Tuning on the test loans makes the final score optimistic. A validation set is a hold-out part of the training loans; cross-validation repeats that hold-out five times.',
                  notes=(f'This is the habit that protects every score you report. A model has three jobs, and each job gets its own loans. Fitting the parameters uses the training loans. '
                         f'Tuning the settings, such as the decision threshold or the depth of a tree, called hyperparameters, uses a validation set, which is a part of the training loans held out for comparing choices. Cross-validation does the same five times, and we used it in Session 15 to find the threshold of {F["cv_t"]:.2f}. '
                         f'On the {n(F["n_train"])} training loans the five folds of {n(F["fold_train_n"][0])} loans give an AUC of {cvt.mean():.3f} with a spread of {cvt.std(ddof=1):.3f}. '
                         f'Only then do we score the {n(nte)} test loans, once, and get {F["auc"]:.3f}. If you tune on the test loans, the final score is optimistic. Which job is the easiest to get wrong?')))

    # ------------------------------------------------------------------ 25 use at work
    S.append(dict(kind='table', title='Where you will use this at work: report the right metric and check for leaks before you present',
                  headers=['Your job', 'What you report', 'What today lets you do'],
                  rows=[['Credit risk analyst at a bank, using scikit-learn', 'Recall at the chosen decision threshold, and AUC', 'Show a committee the confusion matrix counts, with more than an accuracy.'],
                        ['Fraud analyst at a mobile money provider, using Python', 'Precision of the flags the review team receives', 'Set the threshold so reviewers see a number of cases they can handle.'],
                        ['Data scientist reviewing a colleague\'s model at a telecom', 'A leakage check and a cross-validated score', 'Ask when each feature is recorded before trusting an AUC of 0.99.'],
                        ['Monitoring and evaluation officer at an NGO, using Excel and Python', 'Recall for a screening model, with the number of false alarms', 'Explain the trade-off to programme staff in plain counts.']],
                  widths=[4.2, 3.6, 4.2], icons=['coin', 'shield', 'lock', 'clinic'],
                  notes=('Where will you use this on Monday? Four examples. A credit risk analyst at a bank shows the committee the confusion matrix counts and the recall of defaults, with more than an accuracy. '
                         'A fraud analyst at a mobile money provider sets the threshold so that the review team receives a number of cases it can handle, which is a precision question. '
                         'A data scientist reviewing a colleague\'s model asks when each feature is recorded before believing an AUC of point nine nine. And a monitoring and evaluation officer at an NGO explains a screening model\'s trade-off in plain counts. Which is closest to your job?')))

    # ------------------------------------------------------------------ 26 bridge
    S.append(dict(kind='code', title='Read the recipe before the lab: seven lines judge a model',
                  code=("cm = confusion_matrix(y_test, flag)\nprint(classification_report(y_test, flag))\nauc = roc_auc_score(y_test, y_prob)\n"
                        "w_model = LogisticRegression(max_iter=1000,\n    class_weight=\"balanced\")\ncv = StratifiedKFold(n_splits=5)\ncross_val_score(model, X, y, cv=cv, scoring=\"roc_auc\")"),
                  reads=['Line 1: the four counts as a 2 by 2 array. flag is the yes or no at your threshold.', 'Line 2: precision, recall and F1 for each class in one table.', 'Line 3: AUC from the probabilities, not from the yes or no flags.',
                         'Lines 4 and 5: a model that weights the rare class more.', 'Lines 6 and 7: five stratified folds, one AUC score for each.'],
                  notes=('Before the lab, read the recipe. Line one returns the confusion matrix as a two by two array, with the negative class first. Line two, classification report, prints precision, recall and F1 for each class. '
                         'Line three computes the AUC, and notice that it takes the probabilities and never the yes or no flags, because AUC judges the ranking. Lines four and five create a logistic regression with balanced class weights, and the max iter of one thousand avoids a ConvergenceWarning. In the lab it sits inside the same pipeline as the Session 15 model. '
                         'Lines six and seven define five stratified folds and score the model on each one by AUC. In the lab you will also compute each of these numbers yourself with NumPy first, so you know what the library is doing. Why compute them twice?')))

    # ------------------------------------------------------------------ 27 divider
    S.append(dict(kind='divider', title='Part 2: the Python lab', lead='Close the slides. Open the notebook.', section='Lab',
                  notes=('That is the end of the ideas. Everything you need is on the slides you have just seen, and the notebook repeats each step. Open the Colab notebook for Session 16 and run the first two cells. '
                         'In each step you will compute a measure with NumPy yourself, then ask scikit-learn for the same number and compare. The notebook checks your answers as you go. '
                         'In every step, predict first, then run, then read.')))

    # ------------------------------------------------------------------ 28 lab map
    S.append(dict(kind='steps', title='The lab has five steps, and you keep a model comparison table',
                  steps=[dict(head='1 Baseline', text='Dummy classifier', icon='flag'), dict(head='2 Counts', text='Confusion, P, R, F1', icon='grid'), dict(head='3 Curves', text='ROC, AUC, weights', icon='chart'),
                         dict(head='4 Leak hunt', text='Find the column', icon='lock'), dict(head='5 Folds', text='Stratified CV, table', icon='calendar')], highlight=None,
                  caption='Compute by hand, then compare with scikit-learn. Step 5 writes model_comparison.csv.',
                  notes=('Here is the map of the lab. Step one, the baseline model and its accuracy. Step two, the four counts of the confusion matrix with NumPy, then precision, recall and F1 by hand, compared with scikit-learn. '
                         'Step three, the ROC curve and AUC, and the effect of class weight. Step four, the leak hunt: find the column that gives the answer away, and see what it does to the AUC. '
                         'Step five, stratified cross-validation with and without the leak, and the model comparison table that you keep. Please predict before you run each step.')))

    # ------------------------------------------------------------------ 29 check numbers
    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Baseline accuracy on the test loans, and its recall', f'{base:.4f} and 0'], ['Confusion matrix at 0.20: TP, FP, FN, TN', f'about {n(tp)}, {n(fp)}, {n(fn)}, {n(tn)}'],
                        ['Precision, recall, F1 at 0.20', f'about {prec:.2f}, {rec:.2f} and {f1:.2f}'], ['AUC of the logistic regression on the test loans', f'about {F["auc"]:.2f}'],
                        ['Balanced class weight at 0.50: flagged loans and recall', f'about {n(W["flagged"])} and {W["recall"]:.2f}'], ['Column with the strongest correlation with default', f'collection_calls, about {F["corr_calls"]:.2f}'],
                        ['Mean 5-fold AUC on all 8,000 loans, honest and leaky', f'about {cvh.mean():.3f} and {cvl.mean():.3f}']],
                  widths=[7.4, 4.6], icons=['flag', 'grid', 'chart', 'magnifier', 'switch', 'lock', 'calendar'], note='scikit-learn may differ by a few loans or a unit in the third decimal. If a number is far away, find the step that went wrong.',
                  notes=('Use this table as your own self-check. Nobody marks it. Your scikit-learn run may differ from mine by a few loans, because the solver stops at a slightly different point, and that is fine. '
                         'If a number is far away, stop and find the step that went wrong. A frequent cause is using the predicted flags instead of the probabilities for AUC, which gives a much lower number. '
                         'Do not change a number to make it match. What does it mean if your AUC with the leaked column is only point seven six?')))

    # ------------------------------------------------------------------ 30 error cards
    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[[f'AUC is about 0.6 ({F["auc_from_flags"][0.5]:.2f} for flags at 0.50) instead of {F["auc"]:.2f}', 'You passed yes or no flags, not probabilities.', 'Pass y_prob, the probability column, to roc_auc_score.'],
                        ['Confusion matrix is the wrong way round', 'scikit-learn puts the negative class first.', 'Read it as TN and FP on top, FN and TP below.'],
                        ['Precision gives a zero division warning', 'Nothing was flagged, so TP + FP is 0.', 'Lower the threshold, or pass zero_division=0.'],
                        ['Cross-validation AUC is 0.99', 'collection_calls is still in X.', 'Drop it from the honest features.'],
                        ['Fold scores differ a lot from the single split', 'That is normal variation.', 'Report the mean and the standard deviation.']],
                  widths=[3.8, 4.1, 4.1], icons=['cross', 'cross', 'cross', 'cross', 'check'],
                  notes=('Five messages you may meet. An AUC around point six, point five eight to point six seven depending on the threshold, means you passed yes or no flags instead of probabilities. The confusion matrix has the negative class first, so the true positives are bottom right. '
                         'A zero division warning on precision means nothing was flagged, so lower the threshold. A cross-validation AUC of point nine nine means the leaked column is still in your features. '
                         'And folds that differ from your single split are normal, so report the mean and the spread. If a yellow ConvergenceWarning appears, raise max iter or scale the features. Read the message first. It usually tells you the answer.')))

    # ------------------------------------------------------------------ 31 exit check
    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[['A model has 95 percent accuracy on a file where 5 percent of cases are positive. Is it good?', 'Not necessarily. Saying negative for every case also gives 95 percent. Check recall and precision for the positive class.'],
                        ['Precision is 0.40 and recall is 0.60. Say each in a sentence about flagged loans.', 'Of the loans flagged, 40 percent defaulted. Of the loans that defaulted, 60 percent were flagged.'],
                        ['A feature gives an AUC of 0.99. What is the first question to ask?', 'When is this feature recorded? If it is only known after the outcome, it is leakage and must be dropped.']],
                  widths=[5.8, 6.2], icons=['grid', 'chart', 'lock'],
                  notes=('Last, the exit check. Three questions. Write your answers in your notes before you look at mine. One, a model has ninety five percent accuracy on a file where five percent of cases are positive: is it good? '
                         'Two, precision is point four and recall is point six: say each in a sentence about flagged loans. Three, a feature gives an AUC of point nine nine: what is the first question to ask? '
                         'The short answers are on the slide. If you got all three, you are ready for Session 17. If one surprised you, look at that step of the notebook again tonight.')))

    # ------------------------------------------------------------------ facilitator
    sess['facilitator'] = dict(
        prep=['Open the deck and the Session 16 notebook in Colab before anyone arrives. Check that loans.csv loads from the first cell.',
              f'IMPORTANT, an honest open item: every number on the slides, in these notes and in the notebook checks comes from a NumPy replica (content/loans_canon.py and h_loans.py), not from real scikit-learn. Before the course starts, run the solution notebook once in Colab. First check that X_test.index[:10] is [4299, 1151, 2351, 5249, 1328, 3988, 261, 3389, 6878, 5150] and X_test.index.sum() is 8,081,998. If not, the split differs and every number must be recomputed. Then expect small differences only: a real LogisticRegression can move a count at a threshold by a few loans (for example {tp} caught at 0.20) and the AUC by about 0.001. The notebook checks use tolerances: counts 4 to 30 loans, AUC 0.01, cross-validated AUC 0.01.',
              'Write the check table (slide titled Check your numbers) on the board before the lab.',
              'Concepts run with laptops closed. Ask learners to open Colab only after the Part 2 divider.',
              'Remind learners that all data is fictional. The leaked column collection_calls is deliberate, and the data dictionary says so.'],
        misconceptions=[('High accuracy means a good model', f'With a rare positive class a model that flags nobody scores {pct(base, 1)} percent. Look at recall and precision of the positive class.'),
                        ('Precision and recall are the same idea', 'Precision divides by what the model flagged. Recall divides by what really was positive.'),
                        ('A higher AUC means I have found the right threshold', 'AUC judges the ranking at all thresholds. The threshold still comes from the cost of the mistakes.'),
                        ('Choosing the threshold on the test loans is fine because I only do it once', 'Searching the test loans for the best setting is tuning on the test set. Choose on the training loans (validation set or cross-validation) and score the test loans once.'),
                        ('Cross-validation protects me from leakage', 'The leaked column is in every fold, so every fold looks great. Only asking when a column is recorded finds it.'),
                        ('class_weight gives better probabilities', 'It shifts the probabilities upward and distorts them. It behaves like a lower threshold.')],
        probes=[('Which cell of the confusion matrix is a missed default?', 'False negative: actual positive, predicted negative.'), ('When would you prefer precision over recall?', 'When each flag costs time or money, such as manual fraud review.'),
                ('Why does F1 use a harmonic mean?', 'It stays low unless both precision and recall are decent.'), ('What does AUC 0.5 mean?', 'The ranking is no better than a coin flip.'),
                ('Why is collection_calls leakage?', 'It is recorded only after the loan has gone bad, so it is not known at decision time.'), ('Why stratified folds?', 'Each fold keeps the same default rate, so no fold is accidentally easy or hard.')],
        lab_steps=[('Step 1: baseline', f'DummyClassifier accuracy {base:.3f}, recall 0. Make sure learners say why it is high.'), ('Step 2: counts by hand', f'TP, FP, FN, TN about {tp}, {fp}, {fn}, {tn}. precision {prec:.3f}, recall {rec:.3f}, F1 {f1:.3f}. The NumPy and scikit-learn answers must match exactly.'),
                   ('Step 3: AUC and weights', f'AUC about {F["auc"]:.3f}. Balanced at 0.50 flags about {W["flagged"]} loans.'), ('Step 4: leak hunt', f'collection_calls tops the correlation list at {F["corr_calls"]:.2f}. AUC with the leak about {F["auc_leak"]:.3f}.'),
                   ('Step 5: folds and comparison table', f'Five folds of {n(F["fold_n"][0])} loans with 200 or 201 defaults each. Mean AUC honest {cvh.mean():.3f} (spread {cvh.std(ddof=1):.3f}), leaky {cvl.mean():.3f}. model_comparison.csv with 4 rows.')],
        rescue=['If the concepts run over, shorten the types-of-leakage slide and the class weight slides to a quick look; the lab covers both.', 'If only 30 minutes of lab remain, do steps 1, 2 and 4 and set the rest as homework.',
                'If a learner has no Colab access, run the notebook on your screen and ask the learner to call out the predictions.', 'If the cross-validation cell is slow, use cv=3 and say the numbers will differ slightly.'],
        after=['Share the notebook and this deck again for learners who were absent.', 'Ask each learner to save model_comparison.csv and to find one column in their own data that may leak.', 'Note any question you could not answer and open the next session with it.'],
        lab_answer_key=[['Step 1 PREDICT: will the baseline accuracy be above or below 0.80?', f'Above: {base:.3f}, because most loans are repaid.'], ['Step 2 PREDICT: will precision be higher or lower than recall at 0.20?', f'Lower: precision {prec:.2f}, recall {rec:.2f}.'],
                        ['Step 2 CHANGE: raise the threshold to 0.50. What happens to precision and recall?', f'Precision rises to {M5["precision"]:.2f} and recall falls to {M5["recall"]:.2f}.'],
                        ['Step 3 READ: what does the AUC mean in one sentence?', f'A random defaulter gets a higher probability than a random repaid loan about {pct(F["auc"], 0)} percent of the time.'],
                        ['Step 3 CHANGE: use class_weight="balanced". What happens to AUC?', f'It barely changes ({F["auc_w"]:.3f}), but more loans are flagged at 0.50.'],
                        ['Step 4 READ: which column leaks, and why?', 'collection_calls: it is recorded only after a loan goes bad.'], ['Step 4 CHANGE: what AUC do you get with the leak?', f'About {F["auc_leak"]:.3f}, far above the honest {F["auc"]:.3f}.'],
                        ['Step 5 READ: does cross-validation find the leak?', 'No. Both models score stably. Only the question when is it recorded finds the leak.']])
    return sess
