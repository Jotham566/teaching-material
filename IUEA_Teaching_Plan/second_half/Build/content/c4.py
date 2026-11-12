"""Class 4 (Week 11): features and choosing a model, and your project. Features and feature ablation, one-hot encoding and scaling, ridge regression and k-nearest neighbours as previews,
a fair model comparison table, the decision memo and the project rules, then the lab. Built once, re-skinned for three cohorts.

Every number comes from the NumPy reference (ref/week_reference_numpy.py) or from `compute(code)` below, which only calls reference helpers (linreg_fit, ridge_fit, ridge_fit_raw,
knn_fit_predict, tree_reg_fit, scaler_fit). The held-out test set E6 is never used."""
import numpy as np
import pandas as pd
import common as C
from common import fmt

R = C.R
_CACHE = {}

MODEL_NAMES = ['Baseline model', 'Linear regression', 'Decision tree, depth 4', 'Ridge regression, alpha 1', 'k-NN, k = 3']
# the project's client limits and prediction times (Task 7) and costs (Task 4): invented teaching numbers, labelled so on every slide that uses them
MAX_MAE = {'CML3111': 2.0, 'CML3112': 2.0, 'CML3113': 1.0}
MAX_MS = 50
LATENCY_MS = {'Baseline model': 1, 'Linear regression': 3, 'Decision tree, depth 4': 30, 'Ridge regression, alpha 1': 3, 'k-NN, k = 3': 60}
MISSED_COST, FALSE_ALARM_COST = 5, 1


def compute(code):
    """All the Class 4 numbers for one cohort. Cross-validation holds out one whole equipment group (E1 to E4) at a time, so each fold plays 'a machine the model has never seen'."""
    if code in _CACHE:
        return _CACHE[code]
    f = C.facts(code)
    b, tr, va = f['b'], f['tr'], f['va']
    trf, vaf = f['trf'], f['vaf']
    ytr, yva = tr.target.to_numpy(), va.target.to_numpy()
    b13 = R.bundle13(code)
    o = dict(b13=b13)

    # ---- ablation: remove a feature, or add one, and compare on the same validation rows
    def feats(df, extra):
        e = df[R.FEATURES].copy()
        if 'int' in extra:
            e['load_x_ambient'] = e.load_pct * e.ambient_c
        if 'sq' in extra:
            e['load_squared'] = e.load_pct ** 2
        return e

    abl = {}
    for name, extra in (('base', ()), ('int', ('int',)), ('sq', ('sq',))):
        a, c = feats(tr, extra), feats(va, extra)
        med = a.median()
        a, c = a.fillna(med), c.fillna(med)
        bb, w = R.linreg_fit(a, ytr)
        p = R.linreg_predict(bb, w, c)
        abl[name] = dict(mae=R.mae(yva, p), rmse=R.rmse(yva, p))
    abl['load_only'] = dict(mae=b13['line_load']['valid'])
    assert abs(abl['base']['mae'] - b['ablation']['base']) < 1e-12 and abs(abl['int']['mae'] - b['ablation']['extended']) < 1e-12
    o['abl'] = abl

    # ---- the two lines written out with their real weights (formula slide), and row 1 worked by hand
    eb, ew = None, None
    a_ = feats(tr, ('int',))
    a_ = a_.fillna(a_.median())
    eb, ew = R.linreg_fit(a_, ytr)
    b0_, w0_ = R.linreg_fit(trf, ytr)
    r1 = f['clean'].iloc[0]
    x1, x2 = float(r1.load_pct), float(r1.ambient_c)
    x3 = x1 * x2
    wr = [float(v) for v in ew]          # the exact weights: the worked row uses them, so its terms add up to the real prediction
    pred_b = float(eb) + wr[0] * x1 + wr[1] * x2 + wr[2] * x3
    o['lines'] = dict(a=dict(b0=float(b0_), w=[float(v) for v in w0_]), b=dict(b0=float(eb), w=[float(v) for v in ew]),
                      row1=dict(record_id=int(r1.record_id), x1=x1, x2=x2, x3=x3, y=float(r1.target), pred_b=float(pred_b), terms=[wr[0] * x1, wr[1] * x2, wr[2] * x3]))

    # ---- scaling and the two previews
    mu, sd = R.scaler_fit(trf)
    Z, V = R.scaler_apply(trf, mu, sd), R.scaler_apply(vaf, mu, sd)
    o['scaler'] = dict(mu=mu.tolist(), sd=sd.tolist())
    o['ridge2'] = {}
    for a_ in (0.1, 1.0, 10.0):
        i0, w = R.ridge_fit_raw(Z, ytr, a_)
        o['ridge2'][a_] = R.mae(yva, i0 + V @ w)
    o['ridge_poly'] = b13['ridge_rows']          # degree 6 on load_pct alone: none, alpha 1, alpha 100
    o['knn'] = {d['k']: d['valid'] for d in b13['knn']}
    o['knn_ex'] = b13['knn_example']
    xs = tr.load_pct.to_numpy()
    grid = np.linspace(xs.min(), xs.max(), 60)
    P = R.poly_cols(xs, 6)
    o['curves'] = {name: [float(v) for v in R.ridge_predict(R.ridge_fit(P, ytr, a_), R.poly_cols(grid, 6))] for name, a_ in (('none', 0.0), ('alpha 1', 1.0), ('alpha 100', 100.0))}
    o['grid'] = [float(v) for v in grid]
    o['train_scaled'] = [(float(x), float(y)) for x, y in Z]
    o['query_scaled'] = (float(V[0][0]), float(V[0][1]))
    # the ridge loss with its two parts, for the two-feature linear regression on scaled columns: alpha 0 is ordinary linear regression
    rt = []
    for a_ in (0.0, 0.1, 1.0, 10.0):
        i0, w = R.ridge_fit_raw(Z, ytr, a_)
        sse = float(((ytr - (i0 + Z @ w)) ** 2).sum())
        sw2 = float((w ** 2).sum())
        rt.append(dict(alpha=a_, b0=float(i0), w=[float(v) for v in w], sse=sse, sw2=sw2, pen=a_ * sw2, loss=sse + a_ * sw2, valid=(abl['base']['mae'] if a_ == 0 else o['ridge2'][a_])))
    o['ridge_tab'] = rt
    # the k-NN worked example: the four closest training rows to the first validation row, with their Euclidean distances on the scaled features
    q = np.array(o['query_scaled'])
    dist = np.sqrt(((Z - q) ** 2).sum(axis=1))
    order = np.argsort(dist, kind='stable')[:4]
    assert [int(i) for i in order[:3]] == o['knn_ex']['idx']
    o['knn_tab'] = [dict(rid=int(tr.record_id.iloc[i]), x1=float(Z[i][0]), x2=float(Z[i][1]), d=float(dist[i]), y=float(ytr[i])) for i in order]

    # ---- the model comparison table: validation MAE and RMSE, cross-validated MAE over four whole-group folds
    i0, w = R.ridge_fit_raw(Z, ytr, 1.0)
    preds = {'Baseline model': np.full(len(yva), ytr.mean()), 'Linear regression': R.linreg_predict(*R.linreg_fit(trf, ytr), vaf),
             'Decision tree, depth 4': R.tree_predict(R.tree_reg_fit(trf, ytr, 4), vaf), 'Ridge regression, alpha 1': i0 + V @ w,
             'k-NN, k = 3': R.knn_fit_predict(Z, ytr, V, 3)}
    folds = {n: [] for n in MODEL_NAMES}
    g = tr.equipment_id.to_numpy()
    for grp in ('E1', 'E2', 'E3', 'E4'):
        m = g == grp
        trn, hold = tr[~m], tr[m]
        a, c = trn[R.FEATURES], hold[R.FEATURES]
        med = a.median()
        a, c = a.fillna(med), c.fillna(med)
        y1, y2 = trn.target.to_numpy(), hold.target.to_numpy()
        mu_, sd_ = R.scaler_fit(a)
        A, Cc = R.scaler_apply(a, mu_, sd_), R.scaler_apply(c, mu_, sd_)
        i1, w1 = R.ridge_fit_raw(A, y1, 1.0)
        fp = {'Baseline model': np.full(len(y2), y1.mean()), 'Linear regression': R.linreg_predict(*R.linreg_fit(a, y1), c),
              'Decision tree, depth 4': R.tree_predict(R.tree_reg_fit(a.to_numpy(), y1, 4), c.to_numpy()), 'Ridge regression, alpha 1': i1 + Cc @ w1,
              'k-NN, k = 3': R.knn_fit_predict(A, y1, Cc, 3)}
        for n in MODEL_NAMES:
            folds[n].append(R.mae(y2, fp[n]))
    cand = []
    for n in MODEL_NAMES:
        cand.append(dict(name=n, mae=R.mae(yva, preds[n]), rmse=R.rmse(yva, preds[n]), cv_mean=float(np.mean(folds[n])), cv_sd=float(np.std(folds[n], ddof=1)),
                         cv_min=float(min(folds[n])), cv_max=float(max(folds[n])), folds=[float(v) for v in folds[n]], latency=LATENCY_MS[n]))
    o['cand'] = cand
    assert abs(cand[1]['mae'] - b['reg']['linear']['mae']) < 1e-12 and abs(cand[2]['mae'] - b['reg']['tree']['mae']) < 1e-12
    assert abs(cand[4]['mae'] - o['knn'][3]) < 1e-12
    o['best_val'] = min(cand[1:], key=lambda d: d['mae'])['name']

    # ---- the project's rule (Task 7): keep the models within both client limits, then the lowest validation MAE; ties by latency, then name
    mx = MAX_MAE[code]
    kept = [d for d in cand if d['mae'] <= mx and d['latency'] <= MAX_MS]
    ranked = sorted(kept, key=lambda d: (d['mae'], d['latency'], d['name']))
    o['rule'] = dict(max_mae=mx, kept=[d['name'] for d in ranked], chosen=ranked[0]['name'] if ranked else None)
    assert o['rule']['chosen'] == 'Linear regression', 'the slides assume the rule chooses linear regression'

    # ---- the warning threshold chosen by cost (Class 2, project Task 4): cost = 5 FN + 1 FP; lowest cost, a tie goes to the higher threshold
    ct = [dict(th=t['th'], tp=t['tp'], fp=t['fp'], fn=t['fn'], tn=t['tn'], recall=t['recall'], precision=t['precision'], cost=MISSED_COST * t['fn'] + FALSE_ALARM_COST * t['fp'])
          for t in b['thresholds']]
    o['cost_tab'] = ct
    o['threshold'] = sorted(ct, key=lambda r: (r['cost'], -r['th']))[0]

    # ---- the project's group cross-validation (Task 5): linear regression, rows with no missing value, each of E1 to E5 held out in turn
    dev = pd.concat([tr, va])
    comp = dev[dev.ambient_c.notna()]
    cv5 = []
    for grp in ('E1', 'E2', 'E3', 'E4', 'E5'):
        m = comp.equipment_id.to_numpy() == grp
        bb, w = R.linreg_fit(comp[~m][R.FEATURES], comp[~m].target.to_numpy())
        cv5.append(dict(group=grp, n=int(m.sum()), n_train=int((~m).sum()), mae=R.mae(comp[m].target.to_numpy(), R.linreg_predict(bb, w, comp[m][R.FEATURES]))))
    fv = [d['mae'] for d in cv5]
    o['cv5'] = dict(folds=cv5, mean=float(np.mean(fv)), sd=float(np.std(fv, ddof=1)), n=len(comp), n_dev=len(dev))

    # ---- Class 3's tuned depth (simplest max_depth within 5 percent of the lowest validation MAE), said once beside the fixed depth 4
    curve = b['overfit_curve']
    low = min(v for _, _, v in curve)
    td = min(d for d, _, v in curve if v <= low * 1.05)
    o['tuned'] = dict(depth=td, mae=[v for d, _, v in curve if d == td][0])

    # ---- the lab's rehearsal of opening the test set once: refit on E1 to E5 (median imputation from E1 to E5), score E6 (guide and lab check only, never on a slide)
    te = f['te']
    (devf, tef), _ = R.median_fill(dev, [te])
    bb, w = R.linreg_fit(devf, dev.target.to_numpy())
    o['test'] = dict(n=len(te), mae=R.mae(te.target.to_numpy(), R.linreg_predict(bb, w, tef)))
    mu_, sd_ = R.scaler_fit(devf)
    bl, wl = R.logreg_fit(R.scaler_apply(devf, mu_, sd_), (dev.target >= b['limit']).astype(int).to_numpy())
    pt = R.logreg_proba(bl, wl, R.scaler_apply(tef, mu_, sd_))
    cc = R.confusion((te.target >= b['limit']).astype(int).to_numpy(), (pt >= o['threshold']['th']).astype(int))
    o['test'].update(R.prf(cc), **cc)
    _CACHE[code] = o
    return o


PROJ = {'CML3112': 'Tuesday 1 December, 11:00 to 14:00', 'CML3113': 'Friday 4 December, 08:00 to 11:00', 'CML3111': 'Friday 4 December, 11:00 to 14:00'}
PAYER = {'CML3112': 'the client who pays for the cooling plant', 'CML3113': 'the mine manager who pays for the crusher power', 'CML3111': 'the maintenance manager who pays for the motors'}


def sg(v, nd=4):
    """A signed number for a line of maths: '+ 0.3912' or '- 0.3912'."""
    return ('+ ' if v >= 0 else '- ') + f'{abs(v):.{nd}f}'


def build(code):
    f = C.facts(code)
    b, unit, short, thing = f['b'], f['unit'], f['short'], f['thing']
    k = compute(code)
    cand = {d['name']: d for d in k['cand']}
    line, plain, tree, ridge, knn = (cand[n] for n in MODEL_NAMES[1:2] + MODEL_NAMES[0:1] + MODEL_NAMES[2:])
    abl = k['abl']
    rp = k['ridge_poly']
    ex = k['knn_ex']
    payer = PAYER[code]
    proj = PROJ[code]
    if rp[1]['valid'] < rp[0]['valid'] - 0.005:
        ridge_tail = 'A little penalty helped here, and too much hurt.'
    elif rp[1]['valid'] < rp[0]['valid']:
        ridge_tail = 'On your data a little penalty barely helps, which tells us this curve was not chasing much noise, and too much hurts.'
    else:
        ridge_tail = 'Here a little penalty does not help, and a lot clearly hurts, so this curve was not chasing much noise.'
    n_tr, n_va, n_te, n_clean = b['n_tr'], b['n_va'], b['n_te'], b['n_clean']
    f2 = lambda v: f'{v:.2f}'
    u = unit
    L = k['lines']
    la, lb, r1 = L['a'], L['b'], L['row1']
    sc = k['scaler']
    rt = k['ridge_tab']
    kt = k['knn_tab']
    q1, q2 = k['query_scaled']

    clock = [(10, 'Recall from Class 3'), (35, 'Concepts, part 1: features, scaling and two new models'), (35, 'Concepts, part 2: choosing a model, the memo, the project'),
             (15, 'Break'), (55, 'Lab: the comparison table and the client’s rule'), (10, 'Close and questions on the project'), (20, 'Block 2 quiz: the forms open (they stay open 24 hours)')]
    plan_note = ('This is the last full class of the semester. The first part is concepts only, with no laptop: new features, two new models, a fair way to compare them, the client’s rule for choosing, and how to write the decision down. '
                 'Then a break. Then the lab, where you build the comparison table on your own data and apply the rule. The Block 2 quiz opens in the last 20 minutes of this class and stays open for 24 hours.')

    # the client's rule, worked on this cohort's table
    rule = k['rule']
    mx = f'{rule["max_mae"]:.1f}'
    chosen = cand[rule['chosen']]
    lowest = min(k['cand'], key=lambda d: d['mae'])
    th = k['threshold']
    cv5 = k['cv5']
    tuned = k['tuned']
    nd_abl = 3 if f2(abl['base']['mae']) in (f2(abl['int']['mae']), f2(abl['sq']['mae'])) else 2    # three decimals when two decimals cannot tell the versions apart
    fa_ = lambda v: f'{v:.{nd_abl}f}'

    s = dict(
        code=code, cohort_name=f['name'], num=4, week=11, when=f['dates'][4] + ', ' + f['slot'], short_title='Features and choosing a model',
        title='Features and choosing a model, and your project',
        question=f'Which model should we recommend for predicting {short}, and how do we explain the choice to someone who pays?',
        outcome_head='By the end of today you can',
        outcomes=['Build a new feature, test it with a feature ablation (ablation study) and say what the result shows', 'Compare five candidate models with the same protocol and choose one by the client’s limits on error and latency (model selection)',
                  'Choose a warning threshold by cost, open the test set once, write a one-page decision memo and explain how the project works'],
        outcome_icons=['gear', 'check', 'doc'],
        outcome_note=(f'By the end of today you can do three things. You can build a new feature from what you know about the {thing}, test it with a feature ablation, also called an ablation study, and say what the result shows. '
                      'You can compare five candidate models with the same protocol and choose one by the client’s limits on error and on prediction time, which is model selection, exactly as the project asks. '
                      'And you can choose a warning threshold by cost, open the test set once, and write the choice down in a one-page decision memo. The quiz for this block opens in the last 20 minutes of the class.'),
        clock=clock, plan_title='Your three hours: models and memo first, then the lab', plan_note=plan_note,
        plan_caption='Concepts first, with no laptops. Then the lab. The quiz opens in the last 20 minutes (open 24 hours).',
        friday_note='the same deck and the same clock, because from Class 2 on all three cohorts are on the same footing.',
        recall_from='Class 3',
        recall=[('What is overfitting, and how do we spot it?', 'The model fits noise in its training set, so it does very well on training rows and clearly worse on rows it has never seen. We spot it when the training error is small and the validation error is much bigger (a large generalisation gap).'),
                ('What is K-fold cross-validation for?', 'K-fold cross-validation tests a model several times, each time holding out a different fold (part) of the training set, so we see how much the score moves.'),
                ('What is data leakage?', 'Information from held-out rows reaching the model while it learns. It makes the score too kind, so the model looks better than it is.')],
        words=[('Feature engineering', f'Building a new feature (input variable) from existing features, using what you know about the {thing}.'),
               ('Feature ablation', 'Also called an ablation study. Train with a feature and without it, on the same rows and metric, and compare the errors.'),
               ('Ridge regression', 'Linear regression with regularisation: an L2 penalty on large weights. Alpha is the regularisation strength.'),
               ('k-NN', 'k-nearest neighbours: average the targets of the k closest training rows. k is a hyperparameter (a setting chosen before training).'),
               ('Latency', 'Prediction time (inference time): how long a trained model takes to give one prediction, in milliseconds (ms).')],
        word_icons=['gear', 'magnifier', 'lock', 'pin', 'clock'],
        words_note=(f'Five words for today. Feature engineering means building a new feature from what you know about the {thing}. A feature ablation, or ablation study, is a fair test of one change: train the model with the feature and without it, on the same rows, and compare the two errors. '
                    'Ridge regression is linear regression with regularisation, which is an L2 penalty on large weights. k-NN means k-nearest neighbours: predict from the k training rows closest to the new row. '
                    'And latency, also called prediction time or inference time, is how long a trained model takes to give one prediction. A client cares about it as much as about the error.'),
        keep='Your lab notebook, saved with all cells run in order, and your decision memo with its sentences filled in.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Saved notebook', value='Restart and run all, then save'), dict(label='Comparison table', value='Five models, one protocol'),
                                                              dict(label='The client’s rule', value='Limits, then lowest MAE'), dict(label='Next', value='Week 12: project sitting')]),
        keep_title='Save the notebook and keep your memo for the project',
        next='Week 12 (proposed): the timed Engineering ML project, 3 hours in your usual class slot. A rehearsal version is released after this class.', next_label='Next class',
        keep_note=('Before you go, restart the notebook, run all cells from the top and save it. Keep the model comparison table, the rule, the cost table and your memo, because the project uses the same steps. '
                   f'The project is an individual, timed, auto-graded sitting of three hours in your Week 12 class slot. My proposed time for your cohort is {proj}, and your lecturer confirms it. '
                   'A practice version, the rehearsal, is released right after this class and is not marked. Use it.'),
        cover_note=(f'Welcome to the last teaching class of the semester. Over three weeks you have built a model, judged it, and learned how to trust it. Today you compare several models and choose one. '
                    f'In real work you will have several candidate models for predicting {short}, and you must choose one fairly and explain the choice to {payer}. '
                    'The ideas come first, then the lab, then the quiz for this block.'),
        slides=[])
    S = s['slides']

    # 0 recall: the questions and the short model answers on one slide
    S.append(dict(kind='table', title='Class 3 in short: overfitting, cross-validation and data leakage',
                  headers=['Question from Class 3', 'Short answer'],
                  rows=[['What is overfitting, and how do we spot it?', 'The model fits noise in its training set, so it does well on training rows but worse on new rows. We spot it by a large generalisation gap: small training error, much bigger validation error.'],
                        ['What is K-fold cross-validation for?', 'K-fold cross-validation tests a model several times. Each time a different fold (part) of the training set is held out for scoring, so we see how much the score moves.'],
                        ['What is data leakage?', 'Information from the held-out rows reaching the model while it learns, for example a mean worked out on all rows. The score looks too good.']],
                  widths=[3.6, 8.2], icons=['magnifier', 'check', 'lock'],
                  note='Check your own answers against these before we move on to today’s ideas.',
                  notes=('These are the three answers from Class 3, so that you can check yourself and revise from this slide later. Overfitting is a model that fits noise in its training set and so does worse on rows it has never seen. '
                         'K-fold cross-validation tests a model several times, holding out a different fold each time. Data leakage is information from the held-out rows reaching the model while it learns, which makes the score too kind. '
                         'If one of your answers was different, say how, and we will look at it together. Which of the three do you find hardest to explain to a friend?')))

    # 1 why today matters
    S.append(dict(kind='steps', title='In real work you compare several models, choose one and explain why',
                  steps=[dict(head='Candidate models', text='Five candidate models, from a baseline model (predicts the training mean) to k-nearest neighbours', icon='gear'), dict(head='One fair test', text='Every model gets the same protocol and metrics', icon='check'),
                         dict(head='One choice', text='Model selection: the most accurate model within the client’s limits', icon='pin'), dict(head='One memo', text=f'A one-page note for {payer}', icon='doc')], highlight=None,
                  caption=f'The picture shows today’s four moves. Whoever pays for the {thing} work wants the choice, the error in {u} and the doubts on one page.',
                  notes=(f'Last class you learned how to trust one model. In a real project you rarely have one. You have several candidate models, and someone has to choose. That someone is you, and the person who pays, {payer}, will ask why. '
                         'So today has four moves. Build the candidate models. Test them fairly, with the same protocol and metrics. That is model comparison. Then choose by the client’s rule: keep the models within the limits on error and time, and take the lowest error. That is model selection. And write the choice on one page. '
                         'Which of those four do you think is hardest to do well, and why?')))

    # 2 a feature column
    heads = ['record_id', 'load_pct', 'ambient_c', 'load_x_ambient', 'target']
    rows = []
    for r in f['clean'].head(4).itertuples():
        if r.ambient_c == r.ambient_c:
            rows.append([str(int(r.record_id)), f'{r.load_pct:g}', f'{r.ambient_c:g}', f'{r.load_pct * r.ambient_c:.1f}', f'{r.target:.1f}'])
    rows = rows[:3]
    S.append(dict(kind='idea', title=f'A new feature can carry what you know about the {thing}',
                  visual=dict(kind='sheet', headers=heads, rows=rows, hl=[0, 3]),
                  lead='Three training rows. The highlighted column is a new feature: load_pct times ambient_c.',
                  points=['Feature engineering builds a new feature from existing ones. Here, hot air may change what a load costs.', f'A product of two features is an interaction feature. Row 1: {r1["x1"]:g} x {r1["x2"]:g} = {r1["x3"]:.1f}.'],
                  notes=(f'The model sees only the columns in the table. If you know something about the {thing}, you can hand it over as a new feature. This is called feature engineering. '
                         f'Take an idea from engineering sense. A {thing} that is working hard in hot air may behave differently from what the two readings give separately. So we build a column, load times ambient, and call it load_x_ambient. '
                         f'A column made by multiplying two features is called an interaction feature. Check row one by hand: {r1["x1"]:g} times {r1["x2"]:g} is {r1["x3"]:.1f}. Notice that this is only an idea. We have not yet shown that it helps.')))

    # 3 formula: the interaction feature and the extended linear regression model
    b3 = lb['w'][2]
    b3s = f'{b3:.3g}'                     # three significant figures, so a tiny weight keeps its precision
    eff = lb['w'][0] + b3 * r1['x2']      # in model B, one more percent of load also changes x3 = x1 times x2
    S.append(dict(kind='formula', title='The new feature is a product, and the extended model gets one more weight',
                  formulas=[('New column', r'$x₃ = x₁ \times x₂$'),
                            ('Model A, multiple linear regression', r'$\hat{y} = ' + f'{la["b0"]:.4f} {sg(la["w"][0])}\\,x₁ {sg(la["w"][1])}\\,x₂$'),
                            ('Model B, plus interaction feature', r'$\hat{y} = ' + f'{lb["b0"]:.4f} {sg(lb["w"][0])}\\,x₁ {sg(lb["w"][1])}\\,x₂ ' + ('+ ' if b3 >= 0 else '- ') + f'{abs(b3):.3g}\\,x₃$')],
                  size=22,
                  symbols=[['x₁, x₂', 'load_pct (%), ambient_c (deg C)', f'Row 1: {r1["x1"]:g} and {r1["x2"]:g}'],
                           ['x₃', 'load_x_ambient = x₁ x₂', f'Row 1: {r1["x3"]:.1f}'],
                           ['y-hat', f'Prediction ({u})', f'Row 1, B: {lb["b0"]:.4f} + {r1["terms"][0]:.2f} + {r1["terms"][1]:.2f} + {r1["terms"][2]:.2f} = {r1["pred_b"]:.1f}'],
                           ['b₀', 'Intercept (bias): y-hat when all features are 0', f'A: {la["b0"]:.4f}   B: {lb["b0"]:.4f}'],
                           ['b₁, b₂, b₃', 'Weights. In A, one more unit adds its weight', f'A: {la["w"][0]:.4f}, {la["w"][1]:.4f}.  B: {lb["w"][0]:.4f}, {lb["w"][1]:.4f}, {b3s}']],
                  widths=[1.7, 4.6, 5.6],
                  note=f'Model B: x₃ moves with x₁, so one more percent of load adds b₁ + b₃ x₂ = {eff:.2f} {u} (row 1).',
                  notes=(f'The maths for the new feature. The product is x three equals x one times x two, where x one is load and x two is ambient temperature. Model A is the linear regression model you know, with an intercept of {la["b0"]:.2f} and two weights. '
                         f'In model A, each weight is what one more unit of that feature adds while the other feature stays fixed: one more percent of load adds {la["w"][0]:.2f} {u}. '
                         f'Model B adds a weight b three for the product. Now x three moves whenever load moves, so the effect of one more percent of load is b one plus b three times x two, about {eff:.2f} {u} in row one. '
                         f'Work row one by hand with model B: the prediction is {r1["pred_b"]:.1f} {u} and the actual value is {r1["y"]:.1f}. Which weight in model B is the smallest?')))

    # 4 the ablation
    S.append(dict(kind='idea', title='A feature ablation tests one change on its own, with everything else kept the same',
                  visual=dict(kind='ablation', rows=[dict(label='Model A: two features', chips=[dict(t='load_pct'), dict(t='ambient_c')], result=f'{fa_(abl["base"]["mae"])} {u}', result_sub='validation MAE'),
                                                    dict(label='Model B: plus one feature', chips=[dict(t='load_pct'), dict(t='ambient_c'), dict(t='load_x_ambient', new=True)], result=f'{fa_(abl["int"]["mae"])} {u}', result_sub='validation MAE', hl=True)],
                              band=f'Same {n_tr} training rows. Same {n_va} validation rows. Same measure.'),
                  lead='A feature ablation (ablation study): train with a feature and without it, then compare the errors.',
                  points=['Red box: the new feature. MAE is the mean absolute error, the average size of the prediction error.', 'Same training and validation sets. Only the features differ.'],
                  notes=('How do we find out whether a new feature helps? We run a feature ablation, also called an ablation study. Build two versions of the model. They differ in one thing only, here the list of features. '
                         f'Both learn from the same {n_tr} training rows, and both are scored on the same {n_va} validation rows with the same measure, MAE, the mean absolute error. '
                         f'Model A with two features has an MAE of {fa_(abl["base"]["mae"])} {u}. Model B with the extra feature has an MAE of {fa_(abl["int"]["mae"])}. '
                         'If anything else had changed as well, such as the rows or the measure, we could not say which change mattered. Which one is better, A or B?')))

    # 5 result of the ablation
    chg = abl['int']['mae'] - abl['base']['mae']
    S.append(dict(kind='idea', title='Removing ambient_c makes the error clearly worse, and the new features do not help',
                  visual=dict(kind='bars', items=[dict(label='Remove ambient_c', value=round(abl['load_only']['mae'], nd_abl), text=f'{fa_(abl["load_only"]["mae"])} {u}'), dict(label='Two features (start)', value=round(abl['base']['mae'], nd_abl), text=f'{fa_(abl["base"]["mae"])} {u}', hl=True),
                                                  dict(label='Add load_x_ambient', value=round(abl['int']['mae'], nd_abl), text=f'{fa_(abl["int"]["mae"])} {u}'), dict(label='Add load_squared', value=round(abl['sq']['mae'], nd_abl), text=f'{fa_(abl["sq"]["mae"])} {u}')], unit=f' {u}'),
                  lead='Each bar is the validation MAE of one version of the linear regression model. Shorter is better.',
                  points=[f'Without ambient_c the error grows from {fa_(abl["base"]["mae"])} to {fa_(abl["load_only"]["mae"])} {u}.', 'Adding load_x_ambient or load_squared (load times itself) changes it by almost nothing. Test every idea before you keep it.'],
                  notes=(f'Four versions of the linear regression model, all scored on the same validation rows. Remove ambient_c and the error grows from {fa_(abl["base"]["mae"])} to {fa_(abl["load_only"]["mae"])} {u}. So that feature matters. '
                         f'Add our new product column and the error goes from {fa_(abl["base"]["mae"])} to {fa_(abl["int"]["mae"])}, a change of {abs(chg):.3f}. Add the load squared and it is {fa_(abl["sq"]["mae"])}. '
                         + ('I show three decimals, because two cannot tell these versions apart. ' if nd_abl == 3 else '') + 'Those changes are tiny, and slightly the wrong way. A good idea from engineering sense did not help here. That is a normal result, and it is why we test every idea before we keep it. Would you keep the new feature?')))

    # 6 one-hot, and why not equipment_id
    S.append(dict(kind='idea', title='One-hot encoding turns a categorical feature into 0 and 1 columns, and equipment_id stays out of the features',
                  visual=dict(kind='sheet', headers=['equipment_id', 'is_E1', 'is_E2', 'is_E3', 'is_E4'],
                              rows=[['E1', '1', '0', '0', '0'], ['E2', '0', '1', '0', '0'], ['E3', '0', '0', '1', '0'], ['E4', '0', '0', '0', '1'], [f'E5 (new {thing})', '0', '0', '0', '0']], hl=[4, 0]),
                  lead='One-hot encoding gives each category of a categorical feature its own column: 1 if the row is in it, 0 if not.',
                  points=['The model trained on E1 to E4 has no is_E5 column, so E5 in these four columns is all zeros.', f'A column per known {thing} says nothing about a new one, so equipment_id stays out of the features.'],
                  notes=('A model needs numbers, so a categorical feature such as equipment_id has to be turned into numbers. One-hot encoding gives each group its own column, with a one where the row belongs and a zero elsewhere. '
                         'Read a row across and you see a single one. That is a useful tool, and you will meet it again. But look at the last row. A model trained on E1 to E4 has columns for those four only. E5 is a group it never saw, so if we squeeze E5 into those columns we get four zeros, which says nothing about E5. '
                         f'Our aim is a model that works on a {thing} it has never met, so here we leave equipment_id out. Where would a one-hot column be a good idea?')))

    # 7 scaling
    sr = b['scaling_rows']
    S.append(dict(kind='idea', title='Standardisation puts every feature on the same ruler',
                  visual=dict(kind='sheet', headers=['load_pct', 'ambient_c', 'load standardised', 'ambient standardised'], rows=[[f'{a:g}', f'{c:g}', f'{x:.2f}', f'{y:.2f}'] for a, c, x, y in sr], hl=[0, 2]),
                  lead='Standardisation (scaling to z-scores): z = (value minus training mean) divided by training standard deviation.',
                  points=[f'Row 1 by hand: ({sr[0][0]:g} - {sc["mu"][0]:.1f}) / {sc["sd"][0]:.1f} = {sr[0][2]:.2f}.', 'StandardScaler learns the mean and standard deviation (dividing by n) from the training set, then applies them to any rows. Ridge regression and k-NN need standardised features.'],
                  notes=(f'You met standardisation, or scaling, in Class 2. We need it again today, because both new models are sensitive to units. Load runs from about 20 to 90, while ambient temperature runs over a much smaller range, and a distance would be dominated by load. '
                         f'Scaling fixes that. Take the training mean of load, {sc["mu"][0]:.1f}, and the standard deviation, {sc["sd"][0]:.1f}. Row one has load {sr[0][0]:g}, so its z-score, the standardised value, is {sr[0][0]:g} minus {sc["mu"][0]:.1f}, divided by {sc["sd"][0]:.1f}, which is {sr[0][2]:.2f}. '
                         'Remember the data leakage rule from Class 3: the mean and standard deviation come from the training rows only.')))

    # 8 ridge picture
    S.append(dict(kind='idea', title='Ridge regression adds an L2 penalty on large weights, which can stop a flexible curve fitting noise',
                  visual=dict(kind='curves', points=[(float(x), float(y)) for x, y in zip(f['tr'].load_pct, f['tr'].target)],
                              curves=[dict(label='Degree 6, no penalty', xs=k['grid'], ys=k['curves']['none'], kind='red'), dict(label='Degree 6, ridge alpha 1', xs=k['grid'], ys=k['curves']['alpha 1'], kind='ink'),
                                      dict(label='Degree 6, ridge alpha 100', xs=k['grid'], ys=k['curves']['alpha 100'], kind='mute')],
                              xlabel='load_pct (percent)', ylabel=f'{short} ({u})'),
                  lead='Regularisation shrinks the weights (coefficients). Ridge regression adds an L2 penalty: alpha times the sum of squared weights.',
                  points=['Dots: training rows. Curves: degree-6 fits of load_pct. A bigger alpha (the regularisation strength) gives a flatter curve.',
                          f'Validation MAE ({u}): {f2(rp[0]["valid"])} none, {f2(rp[1]["valid"])} alpha 1, {f2(rp[2]["valid"])} alpha 100. These errors belong to the degree-6 curve only.'],
                  notes=(f'This is a flexible curve, a sixth-degree polynomial of load, through our training dots. With no penalty it can bend to follow noise. Regularisation means penalising large weights. Ridge regression uses an L2 penalty, and alpha is the regularisation strength. '
                         f'On the validation rows the error is {f2(rp[0]["valid"])} {u} with no penalty, {f2(rp[1]["valid"])} with alpha 1, and {f2(rp[2]["valid"])} with alpha 100, which flattens the curve too much. '
                         'These curves are sixth-degree polynomials of load alone, so their alpha 1 error is a different model from the ridge regression on two features, with alpha 1, that you meet on the next slides. Do not compare the two numbers. Ridge is a preview. ' + ridge_tail)))

    # 9 ridge formula
    S.append(dict(kind='formula', title='Ridge regression minimises squared errors plus alpha times squared weights',
                  formulas=[('Ridge loss', r'$L = \sum_{i=1}^{n}\left(y_i - \hat{y}_i\right)^2 + \alpha \sum_{j=1}^{p} b_j^{\,2}$'), ('Prediction', r'$\hat{y} = b₀ + b₁ z₁ + b₂ z₂$')],
                  size=24,
                  symbols=[['L', 'Loss function: the number made small', 'One value per choice of weights'], ['yᵢ, ŷᵢ', f'Actual and predicted target of training row i ({u})', f'i = 1 to {n_tr}'],
                           ['n', 'Number of training rows', f'n = {n_tr}'], ['alpha', 'Regularisation strength. 0 gives linear regression', 'We try 0.1, 1 and 10'],
                           ['b₁, b₂, p', 'The p weights, one per feature. b₀ is not penalised', 'b₁ load, b₂ ambient, p = 2'],
                           ['z₁, z₂', 'Standardised features (z-scores)', 'z₁ from load_pct, z₂ from ambient_c']],
                  widths=[1.5, 5.2, 5.2],
                  notes=('This is the ridge regression loss function, the number the computer tries to make small. The first part is the sum of the squared errors over the training rows, the same fit measure as before. '
                         'The second part is the L2 penalty: alpha times the sum of the squared weights. A big weight costs a lot, so the computer is pushed to keep the weights small. '
                         'With alpha equal to zero there is no penalty and you get ordinary linear regression. The prediction below uses the standardised features, the z-scores z one and z two, so every weight is on the same ruler. Why must the features be scaled before we penalise the weights?')))

    # 10 ridge numbers
    rr = lambda d: [('0 (ordinary linear regression)' if d['alpha'] == 0 else f'{d["alpha"]:g}'), f'{d["w"][0]:.2f}', f'{d["w"][1]:.2f}', f'{d["sse"]:.1f}', f'{d["pen"]:.1f}', f'{d["loss"]:.1f}', f'{d["valid"]:.2f}']
    r_ex = rt[2]
    S.append(dict(kind='table', title='A bigger alpha shrinks the weights, and here the validation error grows',
                  headers=['alpha', 'Weight b₁ (load)', 'Weight b₂ (ambient)', 'Sum of squared errors', 'L2 penalty: alpha x sum of squared weights', 'Loss L', f'Validation MAE ({u})'],
                  rows=[rr(d) for d in rt], widths=[2.2, 1.5, 1.6, 1.7, 2.1, 1.2, 1.8], icons=False,
                  note=(f'Ridge regression on two features. load_pct was standardised, so b₁ = {rt[0]["w"][0]:.2f} means: {sc["sd"][0]:.1f} more percent of load adds {rt[0]["w"][0]:.2f} {u}. '
                        f'Alpha 1: loss {r_ex["sse"]:.1f} + {r_ex["pen"]:.1f} = {r_ex["loss"]:.1f}. Its error {r_ex["valid"]:.2f} is not the degree-6 curve error.'),
                  notes=(f'Now the real numbers, from your training rows, for linear regression with two features, here with an L2 penalty added. Each row is one value of alpha. With alpha equal to zero the weights are {rt[0]["w"][0]:.2f} and {rt[0]["w"][1]:.2f}, and the squared errors add up to {rt[0]["sse"]:.1f}. '
                         f'As alpha grows, the weights shrink, to {rt[3]["w"][0]:.2f} and {rt[3]["w"][1]:.2f} at alpha ten, but the squared errors climb to {rt[3]["sse"]:.1f}. '
                         f'Check alpha one by hand: {r_ex["sse"]:.1f} plus {r_ex["pen"]:.1f} gives a loss of about {r_ex["loss"]:.1f}. The linear regression model has few weights to calm down, so here the penalty only costs us accuracy. It pays off when a model has many weights that chase noise.')))

    # 11 k-NN picture
    nbs = [(k['train_scaled'][i][0], k['train_scaled'][i][1], f'{t:.1f} {u}') for i, t in zip(ex['idx'], ex['neighbour_targets'])]
    S.append(dict(kind='idea', title='k-nearest neighbours (k-NN) predicts from the k training rows most like the new row',
                  visual=dict(kind='knn', train=k['train_scaled'], query=k['query_scaled'], neighbours=nbs, xlabel='load_pct (standardised)', ylabel='ambient_c (standardised)',
                              result=(f'Prediction: average of the 3 = {ex["prediction"]:.1f} {u}', f'Actual value: {ex["actual"]:.1f} {u}')),
                  lead='k-NN stands for k-nearest neighbours: find the k training rows closest to the new row and average their targets.',
                  points=[f'Grey dots: training rows near the new row (zoomed in). Red dot: the new row, record {ex["query_row"]}. Gold dots: its 3 nearest neighbours, with their targets.', 'k = 3 is a hyperparameter (a setting chosen before training). Both axes are standardised.'],
                  notes=(f'This picture shows k-nearest neighbours, or k-NN, a very different kind of model. Each grey dot is a training row near the new one, placed by its standardised load and standardised ambient temperature. The red dot is a new row. '
                         f'To predict, we find the three training rows closest to it, the gold dots, and average their targets: {ex["neighbour_targets"][0]:.1f}, {ex["neighbour_targets"][1]:.1f} and {ex["neighbour_targets"][2]:.1f}. '
                         f'The average is {ex["prediction"]:.1f} {u}, and the real value was {ex["actual"]:.1f}. There are no coefficients to learn. The model simply remembers the training rows. Why did we standardise the features first?')))

    # 12 k-NN formula, with the worked example under it
    d0, d3 = kt[0], kt[3]
    S.append(dict(kind='formula', title='k-NN measures distance on the standardised features, then averages the k nearest targets',
                  formulas=[('Distance', r"$d = \sqrt{\sum_{j=1}^{2}\left(x_j - x_j^{\prime}\right)^2}$"), ('Prediction', r'$\hat{y} = \frac{1}{k}\sum_{i \in N_k} y_i$')],
                  size=20,
                  symbols=[['d', 'Distance from the new row to a training row', f'Nearest: {d0["d"]:.3f}'],
                           ['x_j, x′_j', 'Standardised feature j: new row, training row', 'j = 1 load, j = 2 ambient'],
                           ['N_k', 'The k = 3 training rows with the smallest d', f'Records {kt[0]["rid"]}, {kt[1]["rid"]}, {kt[2]["rid"]}'],
                           ['yᵢ', f'Target of neighbour i ({u})', f'{kt[0]["y"]:.1f}, {kt[1]["y"]:.1f}, {kt[2]["y"]:.1f}']],
                  widths=[1.4, 5.2, 5.3],
                  note=(f'Record {d0["rid"]}: d = √(({q1:.3f} − ({d0["x1"]:.3f}))² + ({q2:.3f} − ({d0["x2"]:.3f}))²) = {d0["d"]:.3f}. '
                        f'y-hat = ({kt[0]["y"]:.1f} + {kt[1]["y"]:.1f} + {kt[2]["y"]:.1f}) / 3 = {ex["prediction"]:.1f} {u}.'),
                  notes=('Two formulas run the whole model. The first is the Euclidean distance, the straight-line distance on the picture. For each feature j, subtract the training row from the new row, square the gap, add the gaps up and take the square root. '
                         f'Work it for record {d0["rid"]}, the nearest row. The gap in load is {q1 - d0["x1"]:.3f}, the gap in ambient is {q2 - d0["x2"]:.3f}. Square both, add, take the root: {d0["d"]:.3f}. '
                         f'The second formula is the prediction. Take the k rows with the smallest distance, the set N k, and average their targets. The fourth row, record {d3["rid"]}, is a little farther away, so it is left out. With k equal to three the average is {ex["prediction"]:.1f} {u}.')))

    # 14 value of k, preview
    S.append(dict(kind='idea', title='The size of k matters: too small chases noise, too large flattens the pattern',
                  visual=dict(kind='bars', items=[dict(label='k = 1', value=round(k['knn'][1], 2), text=f'{k["knn"][1]:.2f} {u}'), dict(label='k = 3', value=round(k['knn'][3], 2), text=f'{k["knn"][3]:.2f} {u}', hl=True), dict(label='k = 20', value=round(k['knn'][20], 2), text=f'{k["knn"][20]:.2f} {u}')], unit=f' {u}'),
                  lead='k is a hyperparameter: a setting we choose before training. We try a few values and compare the validation MAE.',
                  points=['Each bar is the k-NN validation MAE for one k. Shorter is better.', 'k = 1 copies one row, noise included. k = 20 averages so many rows that the pattern is lost.'],
                  notes=(f'Same validation rows, three values of k. With k equal to one, the model copies its single nearest row, noise and all, and the error is {f2(k["knn"][1])} {u}. With k equal to three it is {f2(k["knn"][3])}, the best of the three. '
                         f'With k equal to twenty, it averages so many rows that it flattens the pattern, and the error is {f2(k["knn"][20])}. So k is a hyperparameter, chosen before training, and we choose it with the validation set. '
                         'Ridge regression and k-NN are previews today, and the project does not test them. Support vector machines, random forests and boosting are planned for next semester. What would k equal to the whole training set predict?')))

    # 15 the protocol
    S.append(dict(kind='steps', title='A fair model comparison keeps four things the same for every model',
                  steps=[dict(head='Same rows', text=f'{n_tr} training and {n_va} validation rows', icon='folder'), dict(head='Same split', text='E1 to E4 train, E5 validates, E6 is the held-out test set', icon='lock'),
                         dict(head='Same metrics', text=f'MAE and RMSE, in {u}, plus 4-fold cross-validation', icon='calculator'), dict(head='Same seed', text='random_state = 17, so chance choices repeat', icon='gear')],
                  caption='The picture shows the four rules of the protocol that every candidate model follows. Change one thing at a time: if two things change, you cannot say which one caused the difference.',
                  notes=('Now the rules for a fair race. Every candidate gets the same rows, the same split, the same measure and the same seed. '
                         f'The same rows means the same {n_tr} training rows and the same {n_va} validation rows. The same split means whole equipment groups, with E6 held out. '
                         f'The same metrics means MAE and RMSE in {u}, and the same four-fold cross-validation. And the same seed means that wherever chance is involved, such as in the tree, we fix random_state at 17, so the result is repeatable. '
                         'If one model got an easier test, the table would be a story about the test and not about the models. Which of the four is easiest to forget?')))

    # 16 formula: how the comparison table is scored
    fl = line['folds']
    S.append(dict(kind='formula', title='Every model also gets a four-fold cross-validated mean and a sample standard deviation',
                  formulas=[('Cross-validated MAE: the mean of the 4 folds', r'$\mathrm{CV}_m = \frac{1}{4}\sum_{f=1}^{4}\mathrm{MAE}_{m,f}$'),
                            ('Sample standard deviation of the 4 fold MAEs', r'$s_m = \sqrt{\frac{1}{4-1}\sum_{f=1}^{4}\left(\mathrm{MAE}_{m,f} - \mathrm{CV}_m\right)^2}$')],
                  size=20,
                  symbols=[['m', 'Model: one of the five candidates', f'Validation MAE on E5 ({n_va} rows), as in Class 1'],
                           ['f', 'Fold: one held-out equipment group, E1 to E4', 'The model learns from the other three groups'],
                           ['MAE_m,f', 'MAE of model m on fold f', 'Linear: ' + ', '.join(f'E{i + 1} {f2(v)}' for i, v in enumerate(fl))],
                           ['CV, s', 'Mean and sample standard deviation: divide by k − 1 = 3', f'Linear: {f2(line["cv_mean"])} and {f2(line["cv_sd"])} {u}']],
                  widths=[1.7, 5.4, 4.8],
                  notes=('This is how every row of the model comparison table is scored. The validation MAE is the one you know from Class 1, on the rows of group E5. '
                         'The first formula repeats the MAE on four folds. In each fold one equipment group is held out, the model learns from the other three, and we average the four results. '
                         f'The second is the sample standard deviation of the four fold errors. We divide by k minus one, here three, exactly as the project does; in Python that is np.std of the scores with ddof equal to 1. For linear regression the mean is {f2(line["cv_mean"])} {u} and the standard deviation {f2(line["cv_sd"])}.')))

    # 17 the model comparison table
    S.append(dict(kind='table', title=f'Model comparison table: five candidate models on the same {n_va} validation rows',
                  headers=['Model', 'Validation MAE', 'Validation RMSE', 'CV mean (4 folds)', 'CV standard deviation', 'Lowest to highest fold'],
                  rows=[[d['name'], f2(d['mae']), f2(d['rmse']), f2(d['cv_mean']), f2(d['cv_sd']), f'{f2(d["cv_min"])} to {f2(d["cv_max"])}'] for d in k['cand']],
                  widths=[2.9, 1.6, 1.6, 1.8, 1.9, 2.2], icons=['cross', 'chart', 'gear', 'lock', 'pin'],
                  note=(f'Errors in {u}; lower is better. A fold is one held-out group, E1 to E4. '
                        f'The tree keeps max_depth 4, as in the project. Class 3’s tuned depth (seed 17), {tuned["depth"]}, scores {f2(tuned["mae"])} {u}.'),
                  notes=('This is the model comparison table, the centre of today. Each row is one model. The first two numbers are the error on the same validation rows. '
                         'The last three come from cross-validation on the training rows, where each equipment group takes a turn as the held-out group: the mean, the standard deviation and the range from the best fold to the worst. '
                         f'The baseline model has an MAE of {f2(plain["mae"])} {u}. Linear regression, ridge regression and k-NN all do far better. The decision tree sits in between, even at the depth Class 3 tuned. Read the table slowly before we choose.')))

    # 18 latency
    S.append(dict(kind='idea', title='Latency is the time a model takes to give one prediction, and the client sets a limit on it',
                  visual=dict(kind='latency', items=[dict(label=n, value=LATENCY_MS[n]) for n in MODEL_NAMES], limit=MAX_MS, unit=' ms',
                              note='Invented teaching numbers, the same as in the project'),
                  lead='Latency (prediction time, inference time) is how long a trained model takes to give one prediction, in milliseconds (ms).',
                  points=['The red dashed line is the client’s limit, 50 ms. A red bar is over the limit.',
                          'k-NN is slow because it compares each new row with every training row. A control system that must answer within 50 ms cannot wait for it.'],
                  notes=(f'So far we judged models on error alone. A client also cares about time. Latency, also called prediction time or inference time, is how long a trained model takes to give one prediction. For a {thing}, a control system or an alarm may need an answer within a fraction of a second, so the client sets a limit: 50 milliseconds. '
                         'These numbers are invented for teaching, and the project uses the same ones: baseline 1, linear regression 3, tree 30. Ridge regression is as fast as linear regression. k-NN takes 60, because to predict one row it measures the distance to every training row. Which models pass the limit?')))

    # 19 the client's rule
    S.append(dict(kind='idea', title='Model selection follows the client’s rule: meet both limits, then take the lowest validation MAE',
                  visual=dict(kind='ladder', items=[dict(head=f'1 Keep: validation MAE at most {mx} {u}'), dict(head='2 Keep: latency at most 50 ms'),
                                                    dict(head='3 Choose the lowest validation MAE of those kept', hl=True), dict(head='4 A tie: smaller latency, then name A to Z')]),
                  lead='This is the project’s rule. The client’s two limits are invented teaching numbers.',
                  points=['Parsimony (prefer the simpler model) is why a client sets limits: good enough and fast beats slightly better and slow.',
                          'The test set never takes part. Cross-validation is reported, and it does not choose.'],
                  notes=(f'The project uses one rule, and so do we. First, keep only the models whose validation MAE is at most the client’s limit, {mx} {u}. Second, keep only the models whose latency is at most 50 milliseconds. '
                         'Third, of the models left, choose the one with the lowest validation MAE. Fourth, if two tie, take the faster one, and if they still tie, the name that comes first in the alphabet. '
                         'Parsimony is the reason the client sets limits at all: a model that is good enough, cheap and fast is worth more than one that is slightly better and slow. The test set never takes part in the choice.')))

    # 20 the rule worked on our table
    lc = lambda n: n if n.startswith('k-NN') else n[0].lower() + n[1:]
    if lowest['name'] != rule['chosen']:
        rule_title = f'{lowest["name"]} has the lowest validation MAE but fails a limit, so {lc(rule["chosen"])} is chosen'
    else:
        rule_title = f'{rule["chosen"]} meets both limits and has the lowest validation MAE, so it is chosen'
    yn = lambda ok: 'Yes' if ok else 'No'
    rrow = lambda d: [d['name'], f2(d['mae']), yn(d['mae'] <= rule['max_mae']), str(d['latency']), yn(d['latency'] <= MAX_MS),
                      ('Yes, chosen' if d['name'] == rule['chosen'] else yn(d['name'] in rule['kept']))]
    S.append(dict(kind='table', title=rule_title,
                  headers=['Model', f'Validation MAE ({u})', f'MAE at most {mx}?', 'Latency (ms, invented)', 'At most 50 ms?', 'Kept?'],
                  rows=[rrow(d) for d in k['cand']], widths=[3.1, 1.9, 1.8, 2.0, 1.7, 1.5],
                  icons=['check' if d['name'] in rule['kept'] else 'cross' for d in k['cand']],
                  note=(f'Kept, sorted by validation MAE: ' + '; '.join(f'{lc(n)}: {f2(cand[n]["mae"])}' for n in rule['kept']) + f'. The first is chosen: {lc(rule["chosen"])}. '
                        'In the project the candidates are the baseline model, linear regression and the tree.'),
                  notes=(f'Now apply the rule by hand, one row at a time. The baseline model is fast but its error, {f2(plain["mae"])} {u}, is far over the limit of {mx}. '
                         f'The tree is fast enough at 30 milliseconds, and its error is {f2(tree["mae"])}. k-NN has an error of {f2(knn["mae"])} but takes 60 milliseconds, over the limit. '
                         f'That leaves {" and ".join(lc(n) for n in rule["kept"])}. Sort them by validation MAE and take the first: {lc(rule["chosen"])}, with {f2(chosen["mae"])} {u}. '
                         'In the project you write this rule as a Python function, and the lab rehearses it.')))

    # 21 the warning threshold, recalled from Class 2
    lim = b['limit']
    prec = lambda t: f2(t['precision']) if t['tp'] + t['fp'] else '0.00 (no warnings)'
    S.append(dict(kind='table', title=f'The warning threshold is chosen by cost: {th["th"]:g} has the lowest cost on the validation rows',
                  headers=['Decision threshold', 'TP', 'FP', 'FN', 'TN', 'Recall', 'Precision', 'Cost: 5 x FN + 1 x FP'],
                  rows=[[f'{t["th"]:g}', str(t['tp']), str(t['fp']), str(t['fn']), str(t['tn']), f2(t['recall']), prec(t), str(t['cost'])] for t in k['cost_tab']],
                  widths=[2.2, 0.9, 0.9, 0.9, 0.9, 1.3, 2.2, 2.6], icons=['check' if t['th'] == th['th'] else 'cross' for t in k['cost_tab']],
                  note=(f'Recall from Class 2. Warning: target at or above {lim:g} {u}. Invented costs, as in the project: FN 5, FP 1. '
                        'The lowest cost wins; a tie takes the higher threshold.'),
                  notes=(f'The project asks two questions, so the memo recommends two things: a model for the {short} and a decision threshold for the warning. The threshold comes from Class 2. '
                         f'A missed warning, a false negative, costs 5, and a false alarm, a false positive, costs 1. These are invented teaching costs. Cost equals five times FN plus FP. '
                         f'On the validation rows, threshold {th["th"]:g} has the lowest cost, {th["cost"]}. If two thresholds had the same cost, we would take the higher one, which raises fewer alarms. Check one row by hand.')))

    # 22 the limits
    S.append(dict(kind='list', title='The comparison has four limits, and you must say them out loud',
                  items=[f'The data are synthetic, which means invented for teaching. Real {thing} data would behave differently.', f'The validation set is one group, E5, with only {n_va} rows. A small gap between two models may be luck.',
                         f'The test set is one group, E6, with {n_te} rows. Its score is one estimate, luckier or unluckier than the truth.',
                         'The client limits, the latencies, the thresholds and the costs are invented teaching numbers. A real client sets their own.'],
                  icons=['flag', 'cross', 'lock', 'pin'],
                  notes=(f'Before we trust the table, four limits. First, these are synthetic teaching data, so real data would behave differently. Second, there are only {n_va} validation rows, from one equipment group, so a small gap between two models may be luck. '
                         f'Third, the test set is also one group, {n_te} rows, so its score is one estimate that could be luckier or unluckier than the truth. Fourth, the limits, latencies and costs are invented for teaching. '
                         'A good report says its limits out loud, because the person who pays will find them anyway. The project asks you to pick the true limits from a list.')))

    # 23 the project's five-group cross-validation, after the choice
    S.append(dict(kind='table', title='After the choice, the project’s cross-validation holds out each of E1 to E5 in turn',
                  headers=['Held-out group', 'Rows held out', 'Rows trained on', f'Linear regression MAE ({u})'],
                  rows=[[d['group'], str(d['n']), str(d['n_train']), f2(d['mae'])] for d in cv5['folds']] + [['Mean of the 5 folds', '', '', f2(cv5['mean'])], ['Sample standard deviation (divide by 5 − 1 = 4)', '', '', f2(cv5['sd'])]],
                  widths=[4.6, 2.0, 2.2, 3.1], icons=['pin'] * 5 + ['chart', 'calculator'],
                  note=(f'Project Task 5: linear regression on the {cv5["n"]} development rows with no missing value. E5 joins because the choice is made. '
                        'In Python: np.std(folds, ddof=1).'),
                  notes=('Once the model is chosen, the validation group has done its job, so it can join the cross-validation. The project does exactly this. It holds out each of E1 to E5 in turn, five folds, trains linear regression on the other four groups and scores the held-out group. '
                         f'It uses the rows with no missing value, so no imputation is needed inside the folds. The mean of the five fold errors is {f2(cv5["mean"])} {u}. '
                         f'The sample standard deviation squares each fold’s gap from the mean, adds them, divides by four, and takes the square root: {f2(cv5["sd"])}. More folds give a steadier picture of new equipment.')))

    # 24 the test set, opened once
    dev_n = cv5['n_dev']
    S.append(dict(kind='idea', title='The test set is opened once: refit the chosen model on E1 to E5, then score E6',
                  visual=dict(kind='refit', rows=[dict(label='1 Choose: learn from E1 to E4, score on E5', chips=[dict(t=g, kind='train') for g in ('E1', 'E2', 'E3', 'E4')] + [dict(t='E5', kind='valid'), dict(t='E6', kind='sealed')],
                                                       band='Model and threshold chosen. E6 untouched.'),
                                                  dict(label='2 Final score, once: refit on E1 to E5, score E6', chips=[dict(t=g, kind='dev') for g in ('E1', 'E2', 'E3', 'E4', 'E5')] + [dict(t='E6', kind='test')],
                                                       band=f'{dev_n} development rows learn. {n_te} test rows give one honest number.')]),
                  lead='The held-out test set (hold-out set, group E6) gives one honest score for the model and the decision threshold you chose.',
                  points=['The refit on E1 to E5 is allowed: the choice is fixed, more rows make a better model, and E6 is still unseen.',
                          'The threshold is tested on E6 at the same time. Report the result and never change the choice.'],
                  notes=('Here is the last step, the one the project marks most strictly. First you choose, using E1 to E4 to learn and E5 to score. E6 stays sealed. '
                         f'Then, once, you refit the chosen model on all {dev_n} development rows, E1 to E5, and score it on E6. Why is the refit allowed? The choice is already made, so E5 cannot bias it any more. More rows give a better model. And E6 is still unseen. '
                         'The warning threshold you chose is tested at the same moment. Think of an exam paper: if you read it and then revise, the mark no longer tells us what you know.')))

    # 25 the memo
    S.append(dict(kind='idea', title='A decision memo fits on one page, has seven parts and recommends a model and a threshold',
                  visual=dict(kind='memo', title='Decision memo (example wording)', sections=[
                      ('1 QUESTION', f'Predict {short} on a new {thing}; which rows need a warning?'), ('2 DATA', f'{n_tr} training and {n_va} validation rows; synthetic'),
                      ('3 MODELS TRIED', 'Baseline, linear, tree, ridge, k-NN'), ('4 RESULT', f'Linear regression: validation MAE {f2(line["mae"])} {u} (limit {mx}), 3 ms'),
                      ('5 LIMITS', 'Synthetic data; one small validation group; one test group; invented limits and costs'), ('6 RECOMMENDATION', f'Linear regression and warning threshold {th["th"]:g}'),
                      ('7 NEXT STEP', f'Collect real data from more {thing}s and validate again with group cross-validation')]),
                  lead='A decision memo is a one-page note that lets the reader act. A related term is model card.',
                  points=['The picture shows an example memo with its seven numbered parts, filled in with our numbers.', 'After the test set is opened once, its score joins the result line. The next step comes after the test: more real data.'],
                  notes=(f'The last skill today is writing the choice down. A decision memo has seven parts, and it fits on one page. The question. The data. The models you tried. The result, with its unit. The limits. Your recommendation. And what to do next. '
                         f'The recommendation names two things: the model and the warning threshold. The next step is what you would do after the test: collect real data from more {thing}s and check again with group cross-validation. '
                         f'The person who pays, {payer}, will read this and nothing else. Which part would you be most tempted to leave out?')))

    # 26 the project: how it works
    S.append(dict(kind='steps', title='Your project is an individual, timed practical sitting that the computer grades',
                  steps=[dict(head='1 Rehearse', text='Practice version, not marked, released after this class', icon='folder'), dict(head='2 Sit', text='Week 12 slot: 3 hours, alone, in Colab', icon='clock'),
                         dict(head='3 Code', text='Part A: coded notebook, 30 marks', icon='gear'), dict(head='4 Decide', text='Part B: structured decision memo form, 15 marks', icon='doc'),
                         dict(head='5 Submit', text='Same submit steps as Test 1', icon='check')],
                  highlight=None, caption='The five stages of the project: it is individual, timed and auto-graded, covers only Weeks 1 to 11, and is worth 40 percent. There is no demo, no presentation and no clinic.',
                  notes=('Now your project. It works like Practical Test 1. It is individual, timed, highly automated and auto-graded. You sit it alone, for three hours, supervised, in Colab, in your Week 12 class slot. '
                         'It covers only what we taught in Weeks 1 to 11, and it counts for 40 percent of the course. Part A is the coded notebook, out of 30. Part B is a structured decision memo form inside the notebook, out of 15. '
                         'There is no demo, no presentation and no clinic. Right after this class you get a practice version, the rehearsal, which is not marked. Which step do you want to practise first?')))

    # 27 the project: marks, rehearsal, sitting and submission
    S.append(dict(kind='table', title='The project is worth 40 percent, and a rehearsal comes first',
                  headers=['Item', 'What you need to know'],
                  rows=[['Format and marks', 'Individual, timed, auto-graded, 3 hours in Colab, like Practical Test 1. Part A, coded notebook: 30 marks. Part B, memo form: 15 marks. Scaled to 40 percent.'],
                        ['How Part B is marked', 'Structured fields are cross-checked against your own results, plus keyword checks on two short answers.'],
                        ['Rehearsal', 'A practice version, released right after Class 4. It is not marked.'],
                        ['Sitting and submission', f'Proposed: {proj} (lecturer to confirm). Restart and run all, save, then the submit cell, as in Practical Test 1. The Practical Test 1 rule on AI and copying applies.']],
                  widths=[3.4, 8.5], icons=['clock', 'doc', 'folder', 'check'],
                  note='Everything the project tests is taught by the end of today, including the client’s rule, the cost table and the test set opened once.',
                  notes=('This slide says what the project is and how you get ready for it. Part A, the coded notebook, is out of 30. Part B, the decision memo form inside the notebook, is out of 15. Both are auto-graded, and the 45 marks are scaled to 40 percent of the course. '
                         'Part B is checked by structured fields that are cross-checked against your own results, plus keyword checks on two short answers. '
                         f'The rehearsal is released right after this class and is not marked. The proposed sitting for your cohort is {proj}, and your lecturer confirms it. When will you do the rehearsal?')))

    # 28 the bridge: code recipe for the client's rule on records
    S.append(dict(kind='code', title='Read the recipe before you write it: the client’s rule in four lines of Python',
                  code='kept = [c for c in candidates\n        if c["validation_mae"] <= MAX_MAE\n        and c["latency_ms"] <= MAX_MS]\n'
                       'ranked = sorted(kept, key=lambda c: (\n    c["validation_mae"], c["latency_ms"], c["name"]))\nchosen = ranked[0]["name"] if ranked else None',
                  reads=['candidates is a list of records: one dictionary per model, with its name, validation_mae and latency_ms.', 'The list comprehension keeps only the records that meet both limits.',
                         'sorted with key=lambda sorts by validation MAE, then latency, then name, so a tie is broken the way the rule says.', 'The first record after sorting is the choice. If no model qualifies, the answer is None.'],
                  notes=('Before the break, read the recipe you will use in the lab and again in the project. Each candidate is a record, a dictionary with its name, its validation MAE and its latency. '
                         'The first line is a list comprehension: it keeps each record that meets both limits. Then sorted orders the kept records. The key is a small function, written with lambda, that gives three things to sort by: the error first, then the latency, then the name. '
                         'The first record after sorting is the chosen model. If nothing qualifies, the answer is None. Can you read the four lines aloud in plain words?')))

    # 29 summary
    S.append(dict(kind='list', title='Today in five lines: test ideas, compare fairly, choose by the rule, test once, write it down',
                  items=['A new feature is an idea: test it with a feature ablation.', 'A fair model comparison keeps rows, split, metrics and seed the same, and reports a cross-validated mean and standard deviation.',
                         'Keep the models within the client’s limits on error and latency, then choose the lowest validation MAE.', 'Choose the warning threshold with the lowest cost.',
                         'Refit on E1 to E5, open the test set once, and write the memo.'],
                  icons=['gear', 'check', 'pin', 'bell', 'doc'],
                  notes=('Let me gather today into five lines. A new feature is an idea, and we test it with a feature ablation before we keep it. '
                         'A fair model comparison uses the same rows, the same split, the same metrics and the same seed, and reports the cross-validated mean with its standard deviation. '
                         'We choose by the client’s rule: meet both limits, then the lowest validation MAE. The warning threshold is the one with the lowest cost. '
                         'Then we refit on E1 to E5, open the test set once, and write the memo. Say one of these lines to the person next to you in your own words, then we take the break.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook. One model comparison table, five candidate models, your own data.', section='Lab',
                  notes=('That is the end of the concepts. Everything you need is on the slides you have just seen, and every term is explained again inside the notebook. '
                         'Please open the notebook now, and keep the slides closed except for the check slides at the end of the deck. I will walk around. Raise your hand if a cell gives an error. '
                         'Remember to run the cells in order from the top, and to write your predictions before you run each cell.')))

    S.append(dict(kind='steps', title='The lab has twelve notebook steps in five groups, and the client’s rule is the centre',
                  steps=[dict(head='Steps 1 to 3', text='Prepare the data, one loop with three models, a feature ablation', icon='folder'), dict(head='Steps 4 to 6', text='One-hot encoding, standardisation and ridge regression, k-NN', icon='gear'),
                         dict(head='Step 7', text='The model comparison table of five models', icon='chart'),
                         dict(head='Steps 8 to 10', text='The client’s rule, the threshold by cost, the test set once', icon='pin'),
                         dict(head='Steps 11 and 12', text='Write the memo. Restart, run all, save', icon='doc')], highlight=3,
                  caption='The twelve notebook steps, in five groups. In each step: predict, run, then read.',
                  notes=('The notebook has twelve steps, in five groups. Steps one to three: prepare the data, run one loop with three models, and test the new feature with a feature ablation. '
                         'Steps four to six: one-hot encoding, then standardisation and ridge regression, then k-NN with a few values of k. Step seven is the model comparison table of five models. '
                         'Steps eight to ten are the project rehearsal: the client’s rule written as a function on records, the warning threshold chosen by cost, then five-group cross-validation and opening the test set once. '
                         'Steps eleven and twelve: write the memo, then restart, run all and save. Predict before you run each cell.')))

    S.append(dict(kind='table', title='Check your numbers against these before you move on',
                  headers=['Step', 'You should see'],
                  rows=[['Training, validation, test rows', f'{n_tr}, {n_va}, {n_te}'], ['Linear regression, two features, validation MAE', f'{f2(abl["base"]["mae"])} {u}'],
                        ['k-NN, k = 3, validation MAE', f'{f2(k["knn"][3])} {u}'],
                        ['Linear regression, 4-fold cross-validated MAE: mean and standard deviation', f'{f2(line["cv_mean"])} and {f2(line["cv_sd"])} {u}'],
                        [f'Step 8: the client’s rule (MAE at most {mx} {u}, at most 50 ms)', rule['chosen']],
                        ['Step 9: threshold with the lowest cost', f'{th["th"]:g} (cost {th["cost"]})'],
                        ['Step 10: five-group cross-validation, linear regression: mean and standard deviation', f'{f2(cv5["mean"])} and {f2(cv5["sd"])} {u}']],
                  widths=[8.2, 3.4], icons=['lock', 'chart', 'pin', 'check', 'clock', 'bell', 'calculator'],
                  note='If your number differs, stop and ask. Do not change a number to match. Find the step that went wrong.',
                  notes=('Use this table as your checkpoint. If your numbers match, carry on. If they do not, stop and call me over, because every later step builds on the earlier ones. '
                         'The most common reason is a cell that was run out of order, or a new feature built on the training table but not on the validation table. '
                         'Do not edit a number to make it match. The aim is to understand why it is different, and that is a skill you will need in every project, including yours.')))

    S.append(dict(kind='table', title='Four errors you will meet, what they mean and what to do',
                  headers=['Error message', 'What it says', 'What to do'],
                  rows=[['KeyError: load_x_ambient', 'The new feature exists in one table only', 'Build it on both the training table and the validation table'],
                        ['ValueError: contains NaN', 'A model received a missing value (NaN) and has no imputation step', 'Wrap the model with with_imputer(...) or add a SimpleImputer to the pipeline'],
                        ['IndexError: list index out of range', 'ranked is empty: no model met both client limits', 'Print kept and check the limits and the latency numbers'],
                        ['NameError: with_imputer', 'The cell that defines the helper function with_imputer has not been run', 'Run all cells from the top, in order']],
                  widths=[3.4, 4.2, 4.4], icons=['key', 'cross', 'flag', 'bell'],
                  notes=('Errors are normal, and reading them is a skill. These four are the ones you will most likely meet today. A key error on the new feature means you built it on the training table but not on the validation table, so build it on both. '
                         'A value error about NaN means a model has no imputation step, so use with_imputer. An index error in step eight means no model met both limits, so the ranked list is empty: print kept and check your limits. '
                         'And a name error on with_imputer means you skipped the helper cell, so run all cells from the top. Read the last line of the error first.')))

    S.append(dict(kind='list', title='How this class counts towards your coursework',
                  items=['The Block 2 quiz (forms Q9 and Q10) opens in the last 20 minutes of this class and stays open for 24 hours.', f'The Block 2 assignment (A9, A10, A11) closes on {C.COHORTS[code]["b2_close"]} (Kampala time).',
                         'Block work is practice. Your final mark is A1 to A5, Q1 to Q5, Practical Test 1 and the project.',
                         f'The project: 3 hours, 40 percent. Proposed: {proj}, lecturer to confirm. The rehearsal comes first.'],
                  icons=['clock', 'doc', 'check', 'lock'],
                  notes=('A word on how this counts. The Block 2 quiz has two forms, Q9 and Q10. They open in the last twenty minutes of this class, after the lab, and stay open for twenty-four hours. '
                         f'The Block 2 assignment, A9, A10 and A11, closes on {C.COHORTS[code]["b2_close"]}, Kampala time. The block work is practice: it is collected and you get feedback, but it does not count toward your final mark. '
                         'Your final mark is A1 to A5, Q1 to Q5, Practical Test 1 and the Engineering ML project, which is worth 40 percent. '
                         f'The proposed project sitting for your cohort is {proj}, and your lecturer confirms it. The rehearsal is released right after this class. Use it to practise.')))

    s['facilitator'] = dict(
        prep=['Open the deck in Slide Show mode and the lab notebook in Colab before anyone arrives. Run the notebook from the top once so you know it works on your account.',
              'Put the lab notebook and engineering_data.csv in the shared class folder and post the link. Every learner needs both files in Colab, in the Files panel.',
              'Write the "check your numbers" table on the board before the lab (numbers for your cohort are in the table below).',
              f'Prepare the Block 2 quiz (forms Q9 and Q10) for the end of the class. The deck and the student guide say it opens in the last 20 minutes of the class and each form stays open for 24 hours; the last 20 minutes of the clock are for it. The deck has {len(S)} authored slides, so keep the formula slides brisk.',
              'Have the rehearsal (the practice version of the project) ready to release right after the class. The project is an individual, timed, auto-graded 3-hour sitting in the Week 12 class slot, covering Weeks 1 to 11, worth 40 percent (Part A 30, Part B 15, scaled from 45). The deck gives the proposed times as lecturer to confirm (CML3112 Tue 1 Dec 11:00 to 14:00, CML3113 Fri 4 Dec 08:00 to 11:00, CML3111 Fri 4 Dec 11:00 to 14:00). Confirm them in writing.',
              'The deck teaches the project’s own rule for choosing a model (Task 7: client limits on validation MAE, 2.0 deg C, 2.0 kW or 1.0 kWh/t, and on latency, 50 ms; then the lowest validation MAE), the cost table for the threshold (Task 4), the five-group cross-validation with ddof=1 (Task 5) and the refit on E1 to E5 before the one test opening (Task 8). The latencies and costs are the project’s invented teaching numbers.'],
        misconceptions=[('A clever new feature must help', 'Test it. Here the load_x_ambient column changes the error by hardly anything.'),
                        ('The model with the lowest number on the table is the one to choose', 'Only if it meets the client’s limits on error and latency. For CML3113, k-NN has the lowest validation MAE but takes 60 ms, so linear regression is chosen.'),
                        ('Equipment_id should be a feature because it is in the file', 'The model must work on equipment it has never met, and a new group has no column of its own.'),
                        ('A bigger alpha or a bigger k is always safer', 'Too much penalty or too many neighbours flattens the pattern. The error goes up again.'),
                        ('The test set can be used to pick between two close models', 'It is opened once, after the model and the threshold are chosen. After that it cannot give a fair number.'),
                        ('Refitting on E1 to E5 before the test is cheating', 'The choice is already fixed, so E5 cannot bias it. More rows make a better model, and E6 is still unseen.')],
        probes=[('What is a feature ablation?', 'Change one thing, keep everything else the same, and compare on the same validation rows.'),
                ('What is an interaction feature?', 'A column made by multiplying two features, here load_pct times ambient_c.'),
                ('Why do we leave equipment_id out of the features?', 'The model must work on new equipment. A group it never saw would have no column of its own.'),
                ('Why do ridge regression and k-NN need standardised features?', 'The penalty and the distance both depend on units, so a feature with big numbers would dominate.'),
                ('What does a bigger alpha do?', 'Alpha is the regularisation strength. A bigger alpha makes the L2 penalty stronger and the curve flatter. Too big and the model underfits.'),
                ('How does k-NN measure closeness?', 'By the Euclidean distance on the standardised features: square the gaps, add them, take the square root.'),
                ('What is latency, and why is k-NN slow?', 'The time a trained model takes to give one prediction. k-NN measures the distance to every training row for each new row.'),
                ('How does the project choose a model?', 'Keep the models with validation MAE at most the client’s limit and latency at most 50 ms, then take the lowest validation MAE; a tie goes to the faster model, then the name.'),
                ('Why do we divide by k minus 1 for the standard deviation of the folds?', 'It is the sample standard deviation, np.std(scores, ddof=1), which the project asks for. StandardScaler, in contrast, divides by n.'),
                ('How is the warning threshold chosen?', 'Cost = 5 x FN + 1 x FP on the validation rows for 0.3, 0.5 and 0.7; the lowest cost wins, and a tie goes to the higher threshold.'),
                ('Who may open the test set, and when?', 'Nobody until the model and the threshold are chosen, and then only once, after refitting on E1 to E5.')],
        lab_steps=[('Step 1: prepare', 'Rows left to model with: 88. Rows 58, 15, 15. Anyone with different numbers has run a cell twice or changed a cleaning rule.'),
                   ('Step 2: first loop', 'Three models, one loop (pipeline with median imputation). Baseline model, linear regression and decision tree match the Class 1 model comparison table. Ask why the loop keeps the comparison fair.'),
                   ('Step 3: features', 'Four versions of the linear regression model. Removing ambient_c makes the error clearly worse. The product and the squared load change the MAE by less than 0.03. Resist the urge to explain the product away: the lesson is that the data decide.'),
                   ('Step 4: one-hot encoding', 'The validation group has an is_E5 column that the training table lacks. This is the whole argument for leaving equipment_id out.'),
                   ('Step 5: standardisation and ridge regression', 'Ridge regression on two features gets slightly worse as alpha grows. The degree-6 curve on load alone improves at alpha 1 (CML3113: no better) and worsens at alpha 100, and its biggest weight shrinks from thousands to single figures.'),
                   ('Step 6: k-NN', 'k = 3 is best of 1, 3 and 20. The three neighbours of the first validation row are printed, and their average is the prediction.'),
                   ('Step 7: the model comparison table', 'Five rows, with the cross-validated mean and the sample standard deviation (ddof=1). The GroupKFold fold order is chosen by scikit-learn; only the set of groups matters.'),
                   ('Step 8: the client’s rule', 'A function on records (lists of dictionaries), a list comprehension and sorted with key=lambda, as in the project. Linear regression is chosen in every cohort; for CML3113 k-NN has the lowest MAE but fails the 50 ms limit.'),
                   ('Step 9: the threshold by cost', 'The cost table of Class 2 for 0.3, 0.5 and 0.7. CML3111 and CML3112 choose 0.3, CML3113 chooses 0.5.'),
                   ('Step 10: five-group CV and the test set', 'Five folds E1 to E5 on the rows with no missing value, sample standard deviation. Then one refit on E1 to E5 and one test opening; the test numbers are in the table below for you, and are not on the slides.'),
                   ('Steps 11 and 12: memo and save', 'Collect one memo sentence from three learners. Insist on restart and run all before saving.')],
        rescue=['If the concepts run over, the ridge regression and k-NN formula slides are previews the project does not test: read the formula aloud, point at one worked line and move on. Keep the slides on latency, the client’s rule, the cost table, the five-group cross-validation and the test set: the project tests all of them.',
                'If only forty minutes of lab remain, do steps 1, 2, 7, 8, 9 and 10, and set the feature ablation, ridge regression and k-NN as practice in the rehearsal.',
                'If wifi fails in the room, the notebook runs unchanged in VS Code, as in Week 2.', 'If several learners are stuck at the same cell, stop the room, run that cell on the projector and let them copy the fix.',
                'If time runs short before the quiz, cut the memo write-up and ask learners to finish it at home.'],
        after=['Share the lab notebook and engineering_data.csv again so absent learners can follow.', 'Release the rehearsal version of the project (not marked) and confirm the proposed sitting time for your cohort in writing.',
               'Note any question you could not answer and ask it before the Week 12 sitting.'])
    s['numbers_fn'] = 'numbers'
    return s


def numbers(F):
    """Rows of cohort numbers for the guide: F maps cohort code to facts."""
    codes = list(F)

    def row(label, g):
        return [label] + [g(F[c], compute(c)) for c in codes]
    cd = lambda k, n: {d['name']: d for d in k['cand']}[n]
    return [row('Training, validation, test rows', lambda f, k: f'{f["b"]["n_tr"]}, {f["b"]["n_va"]}, {f["b"]["n_te"]}'),
            row('Linear regression, two features, MAE', lambda f, k: f'{k["abl"]["base"]["mae"]:.2f} {f["unit"]}'), row('Linear regression plus load_x_ambient, MAE', lambda f, k: f'{k["abl"]["int"]["mae"]:.2f} {f["unit"]}'),
            row('Linear regression plus load_squared, MAE', lambda f, k: f'{k["abl"]["sq"]["mae"]:.2f} {f["unit"]}'), row('Linear regression with load_pct only, MAE', lambda f, k: f'{k["abl"]["load_only"]["mae"]:.2f} {f["unit"]}'),
            row('Ridge regression, degree 6 on load alone, alpha 1, MAE', lambda f, k: f'{k["ridge_poly"][1]["valid"]:.2f} {f["unit"]}'), row('k-NN, k = 3, MAE', lambda f, k: f'{k["knn"][3]:.2f} {f["unit"]}'),
            row('Ridge regression, two features, alpha 1, MAE', lambda f, k: f'{cd(k, "Ridge regression, alpha 1")["mae"]:.2f} {f["unit"]}'),
            row('Decision tree depth 4, MAE (Class 3 tuned depth and its MAE)', lambda f, k: f'{cd(k, "Decision tree, depth 4")["mae"]:.2f} {f["unit"]} (depth {k["tuned"]["depth"]}: {k["tuned"]["mae"]:.2f})'),
            row('Extended linear regression, intercept b_0 and weights b_1, b_2, b_3', lambda f, k: ', '.join([f'{v:.4f}' for v in [k['lines']['b']['b0']] + k['lines']['b']['w'][:2]] + [f'{k["lines"]["b"]["w"][2]:.3g}'])),
            row('Ridge regression loss at alpha 1 (squared errors + L2 penalty)', lambda f, k: f'{k["ridge_tab"][2]["sse"]:.1f} + {k["ridge_tab"][2]["pen"]:.1f} = {k["ridge_tab"][2]["loss"]:.1f}'),
            row('k-NN worked example, nearest distance and prediction', lambda f, k: f'd = {k["knn_tab"][0]["d"]:.3f}, prediction {k["knn_ex"]["prediction"]:.1f} {f["unit"]}'),
            row('Linear regression, 4-fold CV MAE: mean, sample standard deviation (lowest to highest)', lambda f, k: f'{cd(k, "Linear regression")["cv_mean"]:.2f}, {cd(k, "Linear regression")["cv_sd"]:.2f} ({cd(k, "Linear regression")["cv_min"]:.2f} to {cd(k, "Linear regression")["cv_max"]:.2f})'),
            row('Lowest validation MAE among the four models', lambda f, k: k['best_val']),
            row('Client limit on MAE; models kept by the rule; chosen', lambda f, k: f'{k["rule"]["max_mae"]:.1f} {f["unit"]}; ' + ', '.join(k['rule']['kept']) + f'; {k["rule"]["chosen"]}'),
            row('Threshold chosen by cost (cost)', lambda f, k: f'{k["threshold"]["th"]:g} ({k["threshold"]["cost"]})'),
            row('Five-group CV (E1 to E5), linear regression: mean and sample standard deviation', lambda f, k: f'{k["cv5"]["mean"]:.2f} and {k["cv5"]["sd"]:.2f} {f["unit"]}'),
            row('Lab step 10 only, never on a slide: test MAE after the refit on E1 to E5; warning recall and precision', lambda f, k: f'{k["test"]["mae"]:.2f} {f["unit"]}; {k["test"]["recall"]:.2f} and {k["test"]["precision"]:.2f}')]
