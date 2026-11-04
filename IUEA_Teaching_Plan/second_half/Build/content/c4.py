"""Class 4 (Week 11): features and choosing a model, and your project. Features and feature ablation, one-hot encoding and scaling, ridge regression and k-nearest neighbours as previews,
a fair model comparison table, the decision memo and the project rules, then the lab. Built once, re-skinned for three cohorts.

Every number comes from the NumPy reference (ref/week_reference_numpy.py) or from `compute(code)` below, which only calls reference helpers (linreg_fit, ridge_fit, ridge_fit_raw,
knn_fit_predict, tree_reg_fit, scaler_fit). The held-out test set E6 is never used."""
import numpy as np
import common as C
from common import fmt

R = C.R
_CACHE = {}

MODEL_NAMES = ['Baseline model', 'Linear regression', 'Decision tree, depth 4', 'Ridge regression, alpha 1', 'k-NN, k = 3']


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
    wr = [round(float(v), 4) for v in ew]
    pred_b = round(float(eb), 4) + wr[0] * x1 + wr[1] * x2 + wr[2] * x3
    assert abs(pred_b - float(eb + ew @ np.array([x1, x2, x3]))) < 0.15
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
        cand.append(dict(name=n, mae=R.mae(yva, preds[n]), rmse=R.rmse(yva, preds[n]), cv_mean=float(np.mean(folds[n])), cv_min=float(min(folds[n])), cv_max=float(max(folds[n])),
                         folds=[float(v) for v in folds[n]]))
    o['cand'] = cand
    assert abs(cand[1]['mae'] - b['reg']['linear']['mae']) < 1e-12 and abs(cand[2]['mae'] - b['reg']['tree']['mae']) < 1e-12
    assert abs(cand[4]['mae'] - o['knn'][3]) < 1e-12
    assert min(cand[1:], key=lambda d: d['cv_mean'])['name'] == 'Linear regression', 'the story on the slides assumes linear regression has the best cross-validated score'
    o['best_val'] = min(cand[1:], key=lambda d: d['mae'])['name']
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
    if rp[1]['valid'] < rp[0]['valid']:
        ridge_tail = 'A little penalty helped here, and too much hurt.'
    else:
        ridge_tail = 'On your data a little penalty barely helps, which tells us this curve was not chasing much noise, and too much hurts.'
    n_tr, n_va, n_te, n_clean = b['n_tr'], b['n_va'], b['n_te'], b['n_clean']
    f2 = lambda v: f'{v:.2f}'
    u = unit
    L = k['lines']
    la, lb, r1 = L['a'], L['b'], L['row1']
    sc = k['scaler']
    rt = k['ridge_tab']
    kt = k['knn_tab']
    q1, q2 = k['query_scaled']

    clock = [(10, 'Recall from Class 3'), (35, 'Concepts, part 1: features, scaling and two new models'), (30, 'Concepts, part 2: a fair comparison, the memo and the project'),
             (15, 'Break'), (55, 'Lab: the model comparison table, in the notebook'), (25, 'Open and explain the Block 2 quiz (open 24 hours)'), (10, 'Close and the project briefing')]
    plan_note = ('This is the last full class of the semester. The first part is concepts only, with no laptop: new features, two new models, a fair way to compare them and how to write the decision down. '
                 'Then a break. Then the lab, where you build the comparison table on your own data. The Block 2 quiz opens in the last 20 minutes of this class and stays open for 24 hours, and the project rules are part of the concepts.')

    # the honest sentence about who wins on the 15 validation rows and who wins in cross-validation
    if k['best_val'] == 'Linear regression':
        win_pt = f'No other model beats linear regression on the {n_va} validation rows or in cross-validation.'
        win_note = 'The linear regression model has the lowest validation error of the four real models and the lowest cross-validated error too.'
    else:
        bv = cand[k['best_val']]
        win_pt = (f'{bv["name"]} wins on validation ({f2(bv["mae"])} against {f2(line["mae"])}), but linear regression wins in cross-validation ({f2(line["cv_mean"])} against {f2(bv["cv_mean"])}).')
        win_note = (f'Notice that {bv["name"]} beats linear regression on the validation rows, {f2(bv["mae"])} against {f2(line["mae"])} {u}. '
                    f'But when each equipment group takes a turn as the held-out machine, linear regression wins: {f2(line["cv_mean"])} against {f2(bv["cv_mean"])}. '
                    'With fifteen validation rows one lucky group can flip a close race, so we trust the check with more machines.')

    s = dict(
        code=code, cohort_name=f['name'], num=4, week=11, when=f['dates'][4] + ', ' + f['slot'], short_title='Features and choosing a model',
        title='Features and choosing a model, and your project',
        question=f'Which model should we recommend for predicting {short}, and how do we explain the choice to someone who pays?',
        outcome_head='By the end of today you can',
        outcomes=['Build a new feature, test it with a feature ablation (ablation study) and say what the result shows', 'Compare five candidate models with the same cross-validation protocol (model selection) and choose the simplest one that is good enough (parsimony)',
                  'Write a one-page decision memo and explain how the timed, auto-graded project works'],
        outcome_icons=['gear', 'check', 'doc'],
        outcome_note=('Here is what you can do by the end of today. You can build a new feature from what you know about the machine, test it with a feature ablation, also called an ablation study, and say what the result shows. '
                      'You can compare five candidate models with the same cross-validation protocol, which is model selection, and choose the simplest one that is good enough. And you can write the choice down in a one-page decision memo and explain how the project works. '
                      'The quiz for this block opens in the last 20 minutes of the class.'),
        clock=clock, plan_title='Your three hours: models and memo first, then the lab', plan_note=plan_note,
        plan_caption='Concepts first, with no laptops. Then the lab. The quiz opens in the last 20 minutes (open 24 hours).',
        friday_note='the same deck and the same clock, because from Class 2 on all three cohorts are on the same footing.',
        recall_from='Class 3',
        recall=[('What is overfitting, and how do we spot it?', 'The model fits noise in its training set, so it does very well on training rows and clearly worse on rows it has never seen. We spot it when the training error is small and the validation error is much bigger (a large generalisation gap).'),
                ('What is K-fold cross-validation for?', 'K-fold cross-validation tests a model several times, each time holding out a different fold (part) of the training set, so we see how much the score moves.'),
                ('What is data leakage?', 'Information from held-out rows reaching the model while it learns. It makes the score too kind, so the model looks better than it is.')],
        words=[('Feature engineering', 'Building a new feature (input variable) from existing features, using what you know about the machine.'),
               ('Feature ablation', 'Also called an ablation study. Train with a feature and without it, on the same rows and metric, and compare the errors.'),
               ('Ridge regression', 'Linear regression with regularisation: an L2 penalty on large weights. Alpha is the regularisation strength.'),
               ('k-NN', 'k-nearest neighbours: average the targets of the k closest training rows. k is a hyperparameter (a setting chosen before training).'),
               ('Decision memo', 'A one-page note with your choice, numbers and limits. A related industry term is model card.')],
        word_icons=['gear', 'magnifier', 'lock', 'pin', 'doc'],
        words_note=('Five words for today. Feature engineering means building a new feature from what you know about the machine. A feature ablation, or ablation study, is a fair test of one change: train the model with the feature and without it, on the same rows, and compare the two errors. '
                    'Ridge regression is linear regression with regularisation, which is an L2 penalty on large weights. It stops the model fitting noise. k-NN means k-nearest neighbours: predict from the k training rows closest to the new row. '
                    'And a decision memo is the one-page note that gives your choice, your numbers and your limits. In industry a related document is called a model card.'),
        keep='Your lab notebook, saved with all cells run in order, and your decision memo with its sentences filled in.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Saved notebook', value='Restart and run all, then save'), dict(label='Model comparison table', value='Five candidate models, one protocol'),
                                                              dict(label='Decision memo', value='Seven parts, one page'), dict(label='Next', value='Week 12: project sitting')]),
        keep_title='Save the notebook and keep your memo for the project',
        next='Week 12 (proposed): the timed Engineering ML project, 3 hours in your usual class slot. A rehearsal version is released after this class.', next_label='Next class',
        keep_note=('Before you go, restart the notebook, run all cells from the top and save it. Keep the model comparison table and your memo, because the project uses the same steps. '
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
                  notes=('Here are the three answers from Class 3, so that you can check yourself and revise from this slide later. Overfitting is a model that fits noise in its training set and so does worse on rows it has never seen. '
                         'K-fold cross-validation tests a model several times, holding out a different fold each time. Data leakage is information from the held-out rows reaching the model while it learns, which makes the score too kind. '
                         'If one of your answers was different, say how, and we will look at it together. Which of the three do you find hardest to explain to a friend?')))

    # 1 why today matters
    S.append(dict(kind='steps', title='In real work you compare several models, choose one and explain why',
                  steps=[dict(head='Candidate models', text='Five candidate models, from a baseline model (predicts the training mean) to k-nearest neighbours', icon='gear'), dict(head='One fair test', text='Every model gets the same protocol and metrics', icon='check'),
                         dict(head='One choice', text='Model selection: the simplest model that is accurate enough (parsimony)', icon='pin'), dict(head='One memo', text=f'A one-page note for {payer}', icon='doc')], highlight=None,
                  caption=f'The picture shows today’s four moves. Whoever pays for the {thing} work wants the choice, the error in {u} and the doubts on one page.',
                  notes=(f'Last class you learned how to trust one model. In a real project you rarely have one. You have several candidate models, and someone has to choose. That someone is you, and the person who pays, {payer}, will ask why. '
                         'So today has four moves. Build the candidate models. Test them fairly, with the same cross-validation protocol and metrics. That is model comparison. Then choose the simplest model that is accurate enough, which is model selection. And write the choice on one page. '
                         'Which of those four do you think is hardest to do well, and why?')))

    # 2 a feature column
    heads = ['record_id', 'load_pct', 'ambient_c', 'load_x_ambient', 'target']
    rows = []
    for r in f['clean'].head(4).itertuples():
        if r.ambient_c == r.ambient_c:
            rows.append([str(int(r.record_id)), f'{r.load_pct:g}', f'{r.ambient_c:g}', f'{r.load_pct * r.ambient_c:.1f}', f'{r.target:.1f}'])
    rows = rows[:3]
    S.append(dict(kind='idea', title='A new feature can carry what you know about the machine',
                  visual=dict(kind='sheet', headers=heads, rows=rows, hl=[0, 3]),
                  lead='Three training rows. The highlighted column is a new feature: load_pct times ambient_c.',
                  points=['Feature engineering builds a new feature from existing ones. Here, hot air may change what a load costs.', f'A product of two features is an interaction feature. Row 1: {r1["x1"]:g} x {r1["x2"]:g} = {r1["x3"]:.1f}.'],
                  notes=('The model sees only the columns in the table. If you know something about the machine, you can hand it over as a new feature. This is called feature engineering. '
                         f'Here is an idea from engineering sense. A {thing} that is working hard in hot air may behave differently from what the two readings give separately. So we build a column, load times ambient, and call it load_x_ambient. '
                         f'A column made by multiplying two features is called an interaction feature. Check row one by hand: {r1["x1"]:g} times {r1["x2"]:g} is {r1["x3"]:.1f}. Notice that this is only an idea. We have not yet shown that it helps.')))

    # 3 formula: the interaction feature and the extended linear regression model
    S.append(dict(kind='formula', title='The new feature is a product, and the extended linear regression model gets one more weight',
                  formulas=[('New column', r'$x₃ = x₁ \times x₂$'),
                            ('Model A, multiple linear regression', r'$\hat{y} = ' + f'{la["b0"]:.4f} {sg(la["w"][0])}\\,x₁ {sg(la["w"][1])}\\,x₂$'),
                            ('Model B, plus interaction feature', r'$\hat{y} = ' + f'{lb["b0"]:.4f} {sg(lb["w"][0])}\\,x₁ {sg(lb["w"][1])}\\,x₂ {sg(lb["w"][2])}\\,x₃$')],
                  size=22,
                  symbols=[['x₁, x₂', 'load_pct (percent), ambient_c (deg C)', f'Row 1: {r1["x1"]:g} and {r1["x2"]:g}'],
                           ['x₃', 'load_x_ambient: x₁ times x₂', f'Row 1: {r1["x3"]:.1f}'],
                           ['y-hat', f'Prediction ({u})', f'Row 1, B: {lb["b0"]:.4f} + {r1["terms"][0]:.2f} + {r1["terms"][1]:.2f} + {r1["terms"][2]:.2f} = {r1["pred_b"]:.1f}'],
                           ['b₀', 'Intercept (bias): y-hat when every feature is 0', f'A: {la["b0"]:.4f}   B: {lb["b0"]:.4f}'],
                           ['b₁, b₂, b₃', 'Weights (coefficients): one more unit of a feature adds its weight', f'A: {la["w"][0]:.4f}, {la["w"][1]:.4f}.  B: {lb["w"][0]:.4f}, {lb["w"][1]:.4f}, {lb["w"][2]:.4f}']],
                  widths=[1.7, 4.6, 5.6],
                  notes=(f'Here is the maths for the new feature. The product is x three equals x one times x two, where x one is load and x two is ambient temperature. Model A is the linear regression model you know, with an intercept of {la["b0"]:.2f} and two weights. '
                         f'Model B adds a third weight, b three, for the new feature. Each weight tells you what one more unit of that feature adds to the prediction while the other features stay fixed. In model A, one more percent of load adds {la["w"][0]:.2f} {u}. '
                         f'Work row one by hand with model B: the prediction is {r1["pred_b"]:.1f} {u} and the actual value is {r1["y"]:.1f}. Which weight in model B is the smallest, and what might that tell us?')))

    # 4 the ablation
    S.append(dict(kind='idea', title='A feature ablation tests one change on its own, with everything else kept the same',
                  visual=dict(kind='ablation', rows=[dict(label='Model A: two features', chips=[dict(t='load_pct'), dict(t='ambient_c')], result=f'{f2(abl["base"]["mae"])} {u}', result_sub='validation MAE'),
                                                    dict(label='Model B: plus one feature', chips=[dict(t='load_pct'), dict(t='ambient_c'), dict(t='load_x_ambient', new=True)], result=f'{f2(abl["int"]["mae"])} {u}', result_sub='validation MAE', hl=True)],
                              band=f'Same {n_tr} training rows. Same {n_va} validation rows. Same measure.'),
                  lead='A feature ablation (ablation study): train with a feature and without it, then compare the errors.',
                  points=['Red box: the new feature. MAE is the mean absolute error, the average size of the prediction error.', 'Same training and validation sets. Only the features differ.'],
                  notes=('How do we find out whether a new feature helps? We run a feature ablation, also called an ablation study. Build two versions of the model. They differ in one thing only, here the list of features. '
                         f'Both learn from the same {n_tr} training rows, and both are scored on the same {n_va} validation rows with the same measure, MAE, the mean absolute error. '
                         f'Model A with two features has an MAE of {f2(abl["base"]["mae"])} {u}. Model B with the extra feature has an MAE of {f2(abl["int"]["mae"])}. '
                         'If anything else had changed as well, such as the rows or the measure, we could not say which change mattered. Which one is better, A or B?')))

    # 5 result of the ablation
    chg = abl['int']['mae'] - abl['base']['mae']
    S.append(dict(kind='idea', title='Removing ambient_c hurts a lot, and the new features do not help',
                  visual=dict(kind='bars', items=[dict(label='Remove ambient_c', value=round(abl['load_only']['mae'], 2), text=f'{abl["load_only"]["mae"]:.2f} {u}'), dict(label='Two features (start)', value=round(abl['base']['mae'], 2), text=f'{abl["base"]["mae"]:.2f} {u}', hl=True),
                                                  dict(label='Add load_x_ambient', value=round(abl['int']['mae'], 2), text=f'{abl["int"]["mae"]:.2f} {u}'), dict(label='Add load_squared', value=round(abl['sq']['mae'], 2), text=f'{abl["sq"]["mae"]:.2f} {u}')], unit=f' {u}'),
                  lead='Each bar is the validation MAE of one version of the linear regression model. A shorter bar is a better model.',
                  points=[f'Without ambient_c the error grows from {f2(abl["base"]["mae"])} to {f2(abl["load_only"]["mae"])} {u}.', 'Adding load_x_ambient or load_squared (load times itself) changes it by almost nothing.', 'Test every idea before you keep it.'],
                  notes=(f'Here are four versions of the linear regression model, all scored on the same validation rows. Remove ambient_c and the error jumps from {f2(abl["base"]["mae"])} to {f2(abl["load_only"]["mae"])} {u}. So that feature matters. '
                         f'Add our new product column and the error goes from {f2(abl["base"]["mae"])} to {f2(abl["int"]["mae"])}, a change of {abs(chg):.3f}. Add the load squared and it is {f2(abl["sq"]["mae"])}. '
                         'Those changes are tiny, and slightly the wrong way. A good idea from engineering sense did not help here. That is a normal result, and it is why we test every idea before we keep it. Would you keep the new feature?')))

    # 6 one-hot, and why not equipment_id
    S.append(dict(kind='idea', title='One-hot encoding turns a categorical feature into 0 and 1 columns, and equipment_id stays out of the features',
                  visual=dict(kind='sheet', headers=['equipment_id', 'is_E1', 'is_E2', 'is_E3', 'is_E4'],
                              rows=[['E1', '1', '0', '0', '0'], ['E2', '0', '1', '0', '0'], ['E3', '0', '0', '1', '0'], ['E4', '0', '0', '0', '1'], ['E5 (new machine)', '0', '0', '0', '0']], hl=[4, 0]),
                  lead='One-hot encoding gives each category of a categorical feature its own column: 1 if the row is in it, 0 if not.',
                  points=['The model trained on E1 to E4 has no is_E5 column, so E5 in these four columns is all zeros.', 'A column per known machine says nothing about a new one, so equipment_id stays out of the features.'],
                  notes=('A model needs numbers, so a categorical feature such as equipment_id has to be turned into numbers. One-hot encoding gives each group its own column, with a one where the row belongs and a zero elsewhere. '
                         'Read a row across and you see a single one. That is a useful tool, and you will meet it again. But look at the last row. A model trained on E1 to E4 has columns for those four only. E5 is a machine group it never saw, so if we squeeze E5 into those columns we get four zeros, which says nothing about E5. '
                         f'Our aim is a model that works on a {thing} it has never met, so here we leave equipment_id out. Where would a one-hot column be a good idea?')))

    # 7 scaling
    sr = b['scaling_rows']
    S.append(dict(kind='idea', title='Scaling puts every feature on the same ruler',
                  visual=dict(kind='sheet', headers=['load_pct', 'ambient_c', 'load scaled', 'ambient scaled'], rows=[[f'{a:g}', f'{c:g}', f'{x:.2f}', f'{y:.2f}'] for a, c, x, y in sr], hl=[0, 2]),
                  lead='Standardisation (z-score): scaled value = (value minus training mean) divided by training standard deviation.',
                  points=[f'Row 1 by hand: ({sr[0][0]:g} - {sc["mu"][0]:.1f}) / {sc["sd"][0]:.1f} = {sr[0][2]:.2f}.', 'StandardScaler is the scikit-learn tool that learns the mean and standard deviation from the training set, then applies them to any rows. Ridge regression and k-NN need it.'],
                  notes=(f'You met scaling in Class 2. We need it again today, because both new models are sensitive to units. Load runs from about 20 to 90, while ambient temperature runs over a much smaller range, and a distance would be dominated by load. '
                         f'Scaling fixes that. Take the training mean of load, {sc["mu"][0]:.1f}, and the standard deviation, {sc["sd"][0]:.1f}. Row one has load {sr[0][0]:g}, so its scaled value is {sr[0][0]:g} minus {sc["mu"][0]:.1f}, divided by {sc["sd"][0]:.1f}, which is {sr[0][2]:.2f}. '
                         'Remember the data leakage rule from Class 3: the mean and standard deviation come from the training rows only.')))

    # 8 ridge picture
    S.append(dict(kind='idea', title='Ridge regression adds an L2 penalty on large weights so a flexible curve stops fitting noise',
                  visual=dict(kind='curves', points=[(float(x), float(y)) for x, y in zip(f['tr'].load_pct, f['tr'].target)],
                              curves=[dict(label='Degree 6, no penalty', xs=k['grid'], ys=k['curves']['none'], kind='red'), dict(label='Degree 6, ridge alpha 1', xs=k['grid'], ys=k['curves']['alpha 1'], kind='ink'),
                                      dict(label='Degree 6, ridge alpha 100', xs=k['grid'], ys=k['curves']['alpha 100'], kind='mute')],
                              xlabel='load_pct (percent)', ylabel=f'{short} ({u})'),
                  lead='Regularisation shrinks the weights (coefficients). Ridge regression adds an L2 penalty: alpha times the sum of squared weights.',
                  points=['Dots: training rows. Curves: degree-6 fits of load_pct. A bigger alpha (the regularisation strength) gives a flatter curve.',
                          f'Validation MAE ({u}): {f2(rp[0]["valid"])} none, {f2(rp[1]["valid"])} alpha 1, {f2(rp[2]["valid"])} alpha 100. Not the later two-feature model.'],
                  notes=(f'Here is a flexible curve, a sixth-degree polynomial of load, through our training dots. With no penalty it can bend to follow noise. Regularisation means penalising large weights. Ridge regression uses an L2 penalty, and alpha is the regularisation strength. '
                         f'On the validation rows the error is {f2(rp[0]["valid"])} {u} with no penalty, {f2(rp[1]["valid"])} with alpha 1, and {f2(rp[2]["valid"])} with alpha 100, which flattens the curve too much. '
                         'These curves are sixth-degree polynomials of load alone, so their alpha 1 error is a different model from the ridge regression on two features, with alpha 1, that you meet on the next slides. Do not compare the two numbers. Ridge is a preview. ' + ridge_tail + ' Where do you think the right amount lies?')))

    # 9 ridge formula
    S.append(dict(kind='formula', title='Ridge regression minimises squared errors plus alpha times squared weights',
                  formulas=[('Ridge loss', r'$L = \sum_{i=1}^{n}\left(y_i - \hat{y}_i\right)^2 + \alpha \sum_{j=1}^{p} b_j^{\,2}$'), ('Prediction', r'$\hat{y} = b₀ + b₁ z₁ + b₂ z₂$')],
                  size=24,
                  symbols=[['L', 'Loss function: the number made small', 'One value per choice of weights'], ['yᵢ, ŷᵢ', f'Actual and predicted target of training row i ({u})', f'i = 1 to {n_tr}'],
                           ['n', 'Number of training rows', f'n = {n_tr}'], ['alpha', 'Regularisation strength. 0 gives linear regression', 'We try 0.1, 1 and 10'],
                           ['b₁, b₂, p', 'The p weights, one per feature. b₀ is not penalised', 'b₁ load, b₂ ambient, p = 2'],
                           ['z₁, z₂', 'The features after scaling', 'z₁ scaled load_pct, z₂ scaled ambient_c']],
                  widths=[1.5, 5.2, 5.2],
                  notes=('This is the ridge regression loss function, the number the computer tries to make small. The first part is the sum of the squared errors over the training rows, the same fit measure as before. '
                         'The second part is the L2 penalty: alpha times the sum of the squared weights. A big weight costs a lot, so the computer is pushed to keep the weights small. '
                         'With alpha equal to zero there is no penalty and you get ordinary linear regression. The prediction below uses scaled features z, so every weight is on the same ruler. Why must the features be scaled before we penalise the weights?')))

    # 10 ridge numbers
    rr = lambda d: [('0 (ordinary linear regression)' if d['alpha'] == 0 else f'{d["alpha"]:g}'), f'{d["w"][0]:.2f}', f'{d["w"][1]:.2f}', f'{d["sse"]:.1f}', f'{d["pen"]:.1f}', f'{d["loss"]:.1f}', f'{d["valid"]:.2f}']
    r_ex = rt[2]
    S.append(dict(kind='table', title='A bigger alpha shrinks the weights, but on this ridge regression on two features the error grows',
                  headers=['alpha', 'Weight b₁ (load)', 'Weight b₂ (ambient)', 'Sum of squared errors', 'L2 penalty: alpha x sum of squared weights', 'Loss L', f'Validation MAE ({u})'],
                  rows=[rr(d) for d in rt], widths=[2.2, 1.5, 1.6, 1.7, 2.1, 1.2, 1.8], icons=False,
                  note=(f'Ridge regression on two features. load_pct was rescaled, so b₁ = {rt[0]["w"][0]:.2f} means: {sc["sd"][0]:.1f} more percent of load adds {rt[0]["w"][0]:.2f} {u}. '
                        f'Alpha 1: loss {r_ex["sse"]:.1f} + {r_ex["pen"]:.1f} = {r_ex["loss"]:.1f}. Its error {r_ex["valid"]:.2f} is not the degree-6 curve error.'),
                  notes=(f'Now the real numbers, from your training rows, for linear regression with two features, here with an L2 penalty added. Each row is one value of alpha. With alpha equal to zero the weights are {rt[0]["w"][0]:.2f} and {rt[0]["w"][1]:.2f}, and the squared errors add up to {rt[0]["sse"]:.1f}. '
                         f'As alpha grows, the weights shrink, to {rt[3]["w"][0]:.2f} and {rt[3]["w"][1]:.2f} at alpha ten, but the squared errors climb to {rt[3]["sse"]:.1f}. '
                         f'Check alpha one by hand: {r_ex["sse"]:.1f} plus {r_ex["pen"]:.1f} gives a loss of about {r_ex["loss"]:.1f}. The linear regression model has few weights to calm down, so here the penalty only costs us accuracy. When would it pay off?')))

    # 11 k-NN picture
    nbs = [(k['train_scaled'][i][0], k['train_scaled'][i][1], f'{t:.1f} {u}') for i, t in zip(ex['idx'], ex['neighbour_targets'])]
    S.append(dict(kind='idea', title='k-nearest neighbours (k-NN) predicts from the k training rows most like the new row',
                  visual=dict(kind='knn', train=k['train_scaled'], query=k['query_scaled'], neighbours=nbs, xlabel='load_pct (scaled)', ylabel='ambient_c (scaled)',
                              result=(f'Prediction: average of the 3 = {ex["prediction"]:.1f} {u}', f'Actual value: {ex["actual"]:.1f} {u}')),
                  lead='k-NN stands for k-nearest neighbours: find the k training rows closest to the new row and average their targets.',
                  points=[f'Grey dots: training rows. Red dot: the new row, record {ex["query_row"]}. Gold dots: its 3 nearest neighbours, labelled with their targets.', 'k = 3 is a hyperparameter (a setting chosen before training). Both axes are scaled.'],
                  notes=(f'This picture shows k-nearest neighbours, or k-NN, a very different kind of model. Each grey dot is a training row, placed by its scaled load and scaled ambient temperature. The red dot is a new row. '
                         f'To predict, we find the three training rows closest to it, the gold dots, and average their targets: {ex["neighbour_targets"][0]:.1f}, {ex["neighbour_targets"][1]:.1f} and {ex["neighbour_targets"][2]:.1f}. '
                         f'The average is {ex["prediction"]:.1f} {u}, and the real value was {ex["actual"]:.1f}. There are no coefficients to learn. The model simply remembers the training rows. Why did we scale the features first?')))

    # 12 k-NN formula
    S.append(dict(kind='formula', title='k-NN measures distance on the scaled features, then averages the k nearest targets',
                  formulas=[('Distance', r"$d = \sqrt{\sum_{j=1}^{2}\left(x_j - x_j^{\prime}\right)^2}$"), ('Prediction', r'$\hat{y} = \frac{1}{k}\sum_{i \in N_k} y_i$')],
                  size=20,
                  symbols=[['d', 'Distance from the new row to one training row', f'Nearest row: {kt[0]["d"]:.3f} (no unit)'],
                           ["x, x′", 'Scaled feature: new row (x), training row (x′)', 'Two features: scaled load_pct, scaled ambient_c'],
                           ['k', 'How many nearest rows we average. We choose it', 'k = 3'], ['N', 'The k training rows with the smallest d', f'Records {kt[0]["rid"]}, {kt[1]["rid"]}, {kt[2]["rid"]}'],
                           ['y', f'Target of one neighbour ({u})', f'{kt[0]["y"]:.1f}, {kt[1]["y"]:.1f}, {kt[2]["y"]:.1f}'], ['y-hat', f'The prediction for the new row ({u})', f'{ex["prediction"]:.1f} {u}']],
                  widths=[1.5, 5.6, 4.8],
                  notes=('Two formulas run the whole model. The first is the Euclidean distance, the straight-line distance on the picture. For each feature j, subtract the training row from the new row, square the gap, add the gaps up and take the square root. '
                         'We use the scaled features, so load and temperature count equally. The second formula is the prediction. Find the k rows with the smallest distance, call that set N k, and take the plain average of their targets. '
                         f'Here k is three and the average is {ex["prediction"]:.1f} {u}. What would happen to the distance if we skipped the scaling?')))

    # 13 k-NN worked example
    nk = lambda d: [f'{d["rid"]}', f'{d["x1"]:.3f}', f'{d["x2"]:.3f}', f'{d["d"]:.3f}', f'{d["y"]:.1f}']
    d0 = kt[0]
    S.append(dict(kind='table', title=f'Worked example: the four closest training rows to the new row, record {ex["query_row"]}',
                  headers=['Training row (record_id)', 'Scaled load x₁', 'Scaled ambient x₂', 'Distance d', f'Target y ({u})'],
                  rows=[nk(d) for d in kt[:3]] + [nk(kt[3])[:4] + [f'{kt[3]["y"]:.1f} (4th, not used)']],
                  widths=[2.8, 2.2, 2.4, 1.9, 2.8], icons=['pin', 'pin', 'pin', 'cross'],
                  note=(f'New row: x₁ = {q1:.3f}, x₂ = {q2:.3f}. Record {d0["rid"]}: d = square root of (({d0["x1"]:.3f} − ({q1:.3f}))² + ({d0["x2"]:.3f} − ({q2:.3f}))²) = {d0["d"]:.3f}. '
                        f'Prediction = ({kt[0]["y"]:.1f} + {kt[1]["y"]:.1f} + {kt[2]["y"]:.1f}) / 3 = {ex["prediction"]:.1f} {u}. Actual: {ex["actual"]:.1f} {u}.'),
                  notes=(f'Now we work it through with real numbers. The new row is record {ex["query_row"]}, with scaled load {q1:.3f} and scaled ambient {q2:.3f}. The table lists the four training rows closest to it, nearest first. '
                         f'Take the first one, record {d0["rid"]}. The gap in load is {d0["x1"] - q1:.3f}, the gap in ambient is {d0["x2"] - q2:.3f}. Square both, add, and take the square root: the distance is {d0["d"]:.3f}. '
                         f'The fourth row is a little farther away, so with k equal to three it is left out. The prediction is the average of the first three targets, {ex["prediction"]:.1f} {u}. The actual value was {ex["actual"]:.1f}. Why does the fourth row not count?')))

    # 14 value of k, preview
    S.append(dict(kind='idea', title='The size of k matters: too small chases noise, too large flattens the pattern',
                  visual=dict(kind='bars', items=[dict(label='k = 1', value=round(k['knn'][1], 2), text=f'{k["knn"][1]:.2f} {u}'), dict(label='k = 3', value=round(k['knn'][3], 2), text=f'{k["knn"][3]:.2f} {u}', hl=True), dict(label='k = 20', value=round(k['knn'][20], 2), text=f'{k["knn"][20]:.2f} {u}')], unit=f' {u}'),
                  lead='k is a hyperparameter: a setting we choose before training. We try a few values and compare the validation MAE.',
                  points=['Each bar is the k-NN validation MAE for one k. Shorter is better.', 'k = 1 copies one row, noise included. k = 20 averages so many rows that the pattern is lost.'],
                  notes=(f'Same validation rows, three values of k. With k equal to one, the model copies its single nearest row, noise and all, and the error is {f2(k["knn"][1])} {u}. With k equal to three it is {f2(k["knn"][3])}, the best of the three. '
                         f'With k equal to twenty, it averages so many rows that it flattens the pattern, and the error is {f2(k["knn"][20])}. So k is a hyperparameter, chosen before training, and we choose it with the validation set. '
                         'Ridge regression and k-NN are previews today. Next semester you meet support vector machines, random forests and boosting. What would k equal to the whole training set predict?')))

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
    S.append(dict(kind='formula', title='Every model gets MAE, RMSE and four-fold cross-validation scores',
                  formulas=[('Validation MAE of model m', r'$\mathrm{MAE}_m = \frac{1}{n}\sum_{i=1}^{n}\left|\,y_i - \hat{y}_{i,m}\right|$'),
                            ('Validation RMSE of model m', r'$\mathrm{RMSE}_m = \sqrt{\frac{1}{n}\sum_{i=1}^{n}\left(y_i - \hat{y}_{i,m}\right)^2}$'),
                            ('Cross-validated MAE', r'$\mathrm{CV}_m = \frac{1}{4}\sum_{f=1}^{4}\mathrm{MAE}_{m,f}$')],
                  size=15,
                  symbols=[['m, i, n', 'Model, validation row, number of rows', f'Five models; group E5, n = {n_va}'],
                           ['y, ŷ', f'Actual target, and prediction ({u})', f'Linear regression: MAE = {f2(line["mae"])}, RMSE = {f2(line["rmse"])}'],
                           ['MAE, RMSE', 'Mean absolute error; root mean squared error', f'Same unit as the target ({u})'],
                           ['CV (model m)', 'Cross-validated MAE: mean of 4 fold MAEs', f'Linear regression: {", ".join(f2(v) for v in fl)}; mean {f2(line["cv_mean"])} {u}']],
                  widths=[2.4, 5.6, 3.9],
                  notes=('This is how every row of the model comparison table is scored, and it is why the table is fair. The first formula is the mean absolute error: for each validation row, take the gap between the actual target and the prediction, remove the sign, and average. '
                         'The second is the root mean squared error: square each gap, average, then take the square root, so large errors count more. The third repeats the MAE on four folds. In each fold one equipment group is held out, the model learns from the other three, and we average the four results. '
                         f'For the linear regression model the four fold errors are {", ".join(f2(v) for v in fl)}, and their mean is {f2(line["cv_mean"])} {u}. Why do we use four folds as well as the validation rows?')))

    # 17 the model comparison table
    S.append(dict(kind='table', title=f'Model comparison table: five candidate models on the same {n_va} validation rows',
                  headers=['Model', 'Validation MAE', 'Validation RMSE', 'Cross-validated MAE (mean of 4 folds)', 'Lowest to highest fold MAE'],
                  rows=[[d['name'], f2(d['mae']), f2(d['rmse']), f2(d['cv_mean']), f'{f2(d["cv_min"])} to {f2(d["cv_max"])}'] for d in k['cand']],
                  widths=[3.0, 1.9, 1.9, 2.8, 2.4], icons=['cross', 'chart', 'gear', 'lock', 'pin'],
                  note=f'Errors in {u}; lower is better. Baseline model: predicts the training mean. Ridge regression (two features) uses load_pct and ambient_c. A fold is one group, E1 to E4, held out.',
                  notes=('This is the model comparison table, the centre of today. Each row is one model. The first two numbers are the error on the same validation rows. '
                         'The last two come from cross-validation on the training rows, where each equipment group takes a turn as the held-out machine, so we see the average error and how far it moves from fold to fold. '
                         f'The baseline model has an MAE of {f2(plain["mae"])} {u}. Linear regression, ridge regression and k-NN all do far better. The decision tree sits in between. Read the table slowly. Which row would you look at first?')))

    # 18 choosing the simplest
    S.append(dict(kind='idea', title='Model selection: choose the simplest model that is good enough (parsimony)',
                  visual=dict(kind='ladder', items=[dict(head='1 Beat the baseline model clearly'), dict(head='2 Score within 10 percent of the lowest validation error'), dict(head='3 Score well in cross-validation'), dict(head='4 Of those left, pick the simplest (parsimony)', hl=True)]),
                  lead='Model selection: choose one of the candidate models. Parsimony: prefer the simpler model when scores are close.',
                  points=[f'Baseline model: MAE {f2(plain["mae"])} {u}. Linear regression: {f2(line["mae"])}.', win_pt],
                  notes=(f'Work through four tests in order. First, the model must beat the baseline model. The linear regression model has an MAE of {f2(line["mae"])} {u} and the baseline model has {f2(plain["mae"])}, so it does. '
                         'Second, it must score within ten percent of the lowest validation error. Third, it must also do well in cross-validation. Fourth, of those left, pick the simplest. That is parsimony: when scores are close, prefer the simpler model. '
                         f'{win_note} Why does a simple rule help when you explain it to the payer?')))

    # 19 the limits
    S.append(dict(kind='list', title='The model comparison table has three limits, and you must say them out loud',
                  items=['The data are synthetic, which means invented for teaching. Real plant data would behave differently.', f'There are only {n_va} validation rows, all from group E5. A small gap between two models may be luck.',
                         f'The test set E6 has {n_te} rows and no model has used them. We use it once, after we choose.'],
                  icons=['flag', 'cross', 'lock'],
                  notes=(f'Before we trust the table, three limits. First, these are synthetic teaching data, so real plant data would behave differently. Second, there are only {n_va} validation rows, from one equipment group, so a small gap between two models may be luck. '
                         f'Third, the test set has {n_te} rows and nobody has used it. A good report says its limits out loud, because the person who pays will find them anyway. Which limit worries you most, and why?')))

    # 20 the held-out envelope
    S.append(dict(kind='idea', title='The held-out test set is used once, after the model is chosen',
                  visual=dict(kind='envelope', head='Test set E6', sub=f'{n_te} rows, never used', foot='Used once, after you choose'),
                  lead='The held-out test set (hold-out set) is drawn as a sealed envelope. No model has used its rows.',
                  points=['It is the last check. We use it once, after we choose a model, for one honest score of generalisation.', 'Using it and then changing your choice makes it an unfair test.'],
                  notes=(f'Look at the envelope. The test set has {n_te} rows and nobody has used it. It is used once, after you have chosen, to give one honest number for the model you chose. '
                         'Think of an exam paper. If you read the paper first and then revise, your mark no longer tells us what you know. If you use the test set and then change your choice, it is no longer a fair test. '
                         'We do not report test numbers today. In your project you use it once, after you choose your model. Why must you use it only once?')))

    # 21 the memo
    S.append(dict(kind='idea', title='A decision memo fits on one page and has seven parts',
                  visual=dict(kind='memo', title='Decision memo (example wording)', sections=[
                      ('1 QUESTION', f'Can we predict {short} from load and temperature?'), ('2 DATA', f'{n_tr} training rows and {n_va} validation rows; synthetic'),
                      ('3 MODELS TRIED', 'Baseline, linear, tree, ridge, k-NN'), ('4 RESULT', f'Linear regression MAE {f2(line["mae"])} {u}; baseline {f2(plain["mae"])} {u}'),
                      ('5 LIMITS', f'Synthetic data; {n_va} validation rows; test set not yet used'), ('6 RECOMMENDATION', 'Use the linear regression model'),
                      ('7 NEXT STEP', 'Score the held-out test set once and report it')]),
                  lead='A decision memo is a one-page note that lets the reader act. A related term is model card.',
                  points=['The picture shows an example memo with its seven numbered parts, filled in with our numbers.', 'Give the result with its unit, say what you do not know, and end with what to do next.'],
                  notes=(f'The last skill today is writing the choice down. A decision memo has seven parts, and it fits on one page. The question. The data. The models you tried. The result, with its unit. The limits. Your recommendation. And what to do next. '
                         f'The example on the left uses our numbers and invented wording. Notice the result line: it says the linear regression model has an MAE of {f2(line["mae"])} {u}, so the reader knows what the number means. '
                         f'The person who pays, {payer}, will read this and nothing else. Which part would you be most tempted to leave out?')))

    # 22 the project: how it works
    S.append(dict(kind='steps', title='Your project is an individual, timed practical sitting that the computer grades',
                  steps=[dict(head='1 Rehearse', text='Practice version, not marked, released after this class', icon='folder'), dict(head='2 Sit', text='Week 12 slot: 3 hours, alone, in Colab', icon='clock'),
                         dict(head='3 Code', text='Part A: coded notebook, 30 marks', icon='gear'), dict(head='4 Decide', text='Part B: structured decision memo, 15 marks', icon='doc'),
                         dict(head='5 Submit', text='Same submit steps as Test 1', icon='check')],
                  highlight=None, caption='The five stages of the project: it is individual, timed and auto-graded, covers only Weeks 1 to 11, and is worth 45 percent. There is no demo, no presentation and no clinic.',
                  notes=('Here is your project. It works like Practical Test 1. It is individual, timed, highly automated and auto-graded. You sit it alone, for three hours, supervised, in Colab, in your Week 12 class slot. '
                         'It covers only what we taught in Weeks 1 to 11, and it counts for 45 percent of the course. Part A is the coded notebook, out of 30. Part B is a structured decision memo inside the notebook, out of 15. '
                         'There is no demo, no presentation and no clinic. Right after this class you get a practice version, the rehearsal, which is not marked. Which step do you want to practise first?')))

    # 23 the project: format and marks
    S.append(dict(kind='table', title='The project is auto-graded and worth 45 percent of the course',
                  headers=['Item', 'What you need to know'],
                  rows=[['Format', 'Individual, timed, highly automated and auto-graded, like Practical Test 1. A 3-hour supervised practical sitting in Colab. It covers only Weeks 1 to 11.'],
                        ['Part A: 30 marks', 'The coded notebook, auto-graded.'],
                        ['Part B: 15 marks', 'A structured decision memo inside the notebook, auto-graded: structured fields cross-checked against your own results, plus keyword checks on two short answers.']],
                  widths=[3.4, 8.5], icons=['clock', 'gear', 'doc'],
                  note='Nothing in the project is taught after Class 4.',
                  notes=('This slide says what the project is. It is an individual, timed, auto-graded sitting of three hours in Colab, like Practical Test 1, and it covers only Weeks 1 to 11. '
                         'Part A, the coded notebook, is out of 30. Part B is a structured decision memo inside the notebook, out of 15. '
                         'Both parts are auto-graded. Part B is checked by structured fields that are cross-checked against your own results, plus keyword checks on two short answers. Together they count for 45 percent of the course. Which part do you expect to find harder?')))

    # 23b the project: rehearsal, dates, submission
    S.append(dict(kind='table', title='A rehearsal comes first, and the sitting is in your Week 12 class slot',
                  headers=['Item', 'What you need to know'],
                  rows=[['Rehearsal', 'A practice version of the project is released right after Class 4. It is not marked. Use it to practise the same steps.'],
                        ['The sitting', f'Proposed: {proj} (lecturer to confirm). Your own Week 12 class slot.'],
                        ['How to submit', 'Restart and run all, save, then the submit cell, the same mechanism as Practical Test 1. The Practical Test 1 rule on AI and copying applies.']],
                  widths=[3.4, 8.5], icons=['folder', 'clock', 'check'],
                  note='All dates are proposed. Your lecturer confirms them. There is no demo, no presentation and no clinic.',
                  notes=(f'The practice version, the rehearsal, is released right after this class. It is not marked, so use it to practise every step. The sitting itself is in your own Week 12 class slot. '
                         f'The proposed time for your cohort is {proj}, and your lecturer confirms it. You submit the way you did in Practical Test 1: restart and run all, save, then the submit cell. '
                         'The Practical Test 1 rule on AI tools and copying applies. There is no demo, no presentation and no clinic. When will you do the rehearsal?')))

    # 24 the bridge: code recipe
    S.append(dict(kind='code', title='Read the recipe before you write it: a dictionary of models and a loop',
                  code='models = {"linear": with_imputer(LinearRegression()),\n          "tree": with_imputer(DecisionTreeRegressor(\n              max_depth=4, random_state=17))}\n'
                       'for name, model in models.items():\n    model.fit(X_train, y_train)\n    y_pred = model.predict(X_valid)\n    print(name, mean_absolute_error(y_valid, y_pred))',
                  reads=['A dictionary stores each model under a name.', 'with_imputer is a helper, a small function we write once and reuse. It makes a scikit-learn pipeline: median imputation (SimpleImputer) of missing values, then the model.', 'The loop takes each model in turn: train (fit) on the training set, predict the validation set (inference), print the MAE.',
                         'To add a model, add one line to the dictionary.'],
                  notes=('Before the break, look at the recipe you will use. A dictionary holds each candidate under its name. The helper with_imputer wraps a model in a pipeline with median imputation of missing values, using the training medians. '
                         'Then a loop takes each model in turn and gives it the same treatment: train on the training set, predict the validation set, print the score. '
                         'This is how the table stays fair, because no model gets special treatment. To add ridge regression or k-NN, you add one line to the dictionary. Can you read the loop aloud in plain words?')))

    # 25 summary
    S.append(dict(kind='list', title='Today in five lines: test ideas, compare fairly, choose simply, write it down',
                  items=['A new feature is an idea: test it with a feature ablation.', 'Ridge regression and k-NN need scaled features.', 'A fair model comparison keeps rows, split, metrics and seed the same.', 'Choose the simplest model that is good enough (parsimony), and say the limits.', 'Use the held-out test set once, at the end, and write the decision memo.'],
                  icons=['gear', 'lock', 'check', 'pin', 'doc'],
                  notes=('Let me gather today into five lines. A new feature is an idea, and we test it with a feature ablation before we keep it. Ridge and k-NN are two more models, and both need scaled features. '
                         'A fair model comparison uses the same rows, the same split, the same metrics and the same seed. We choose the simplest model that is good enough, and we say what the numbers cannot tell us. '
                         'And the held-out test set is used once, at the end, while the decision memo has seven parts. Say one of these lines to the person next to you in your own words, then we take the break.')))

    S.append(dict(kind='divider', title='Part 2: the lab', lead='Close the slides. Open the notebook. One model comparison table, five candidate models, your own data.', section='Lab',
                  notes=('That is the end of the concepts. Everything you need is on the slides you have just seen, and every term is explained again inside the notebook. '
                         'Please open the notebook now, and keep the slides closed except for the check slides at the end of the deck. I will walk around. Raise your hand if a cell gives an error. '
                         'Remember to run the cells in order from the top, and to write your predictions before you run each cell.')))

    S.append(dict(kind='steps', title='The lab has nine notebook steps in five groups, and the model comparison table is the centre',
                  steps=[dict(head='Steps 1 and 2', text='Prepare the data. One loop with three models', icon='folder'), dict(head='Step 3', text='A new feature and a feature ablation', icon='gear'),
                         dict(head='Steps 4 to 6', text='One-hot encoding, scaling, ridge regression, then k-NN', icon='lock'), dict(head='Step 7', text='The model comparison table: five models in one loop', icon='chart'),
                         dict(head='Steps 8 and 9', text='Write the seven memo sentences. Restart, run all, save', icon='doc')], highlight=None,
                  caption='The nine notebook steps, in five groups. In each step: predict, run, then read.',
                  notes=('Here are the nine steps of the notebook, in five groups. Steps one and two: prepare the data, then run one loop with three models. Step three: test the new feature with a feature ablation. '
                         'Steps four to six: look at one-hot encoding, then scaling and ridge regression, then k-NN with a few values of k. Step seven is the centre: the model comparison table of five models, with the cross-validated range. '
                         'Steps eight and nine: fill in the decision memo with your own sentences, then restart, run all and save. '
                         'Each step asks you to predict first, then run, then read. Predicting before you run is how you find out what you really understand.')))

    S.append(dict(kind='table', title='Check your numbers against these before you move on',
                  headers=['Step', 'You should see'],
                  rows=[['Training, validation, test rows', f'{n_tr}, {n_va}, {n_te}'], ['Linear regression, two features, validation MAE', f'{f2(abl["base"]["mae"])} {u}'], ['Linear regression plus load_x_ambient, validation MAE', f'{f2(abl["int"]["mae"])} {u}'],
                        ['Linear regression with load_pct only, validation MAE', f'{f2(abl["load_only"]["mae"])} {u}'], ['Ridge regression, degree-6 polynomial of load_pct alone, alpha 1, validation MAE', f'{f2(rp[1]["valid"])} {u}'], ['Ridge regression, two features, alpha 1, validation MAE (a different model)', f'{f2(ridge["mae"])} {u}'], ['k-NN, k = 3, validation MAE', f'{f2(k["knn"][3])} {u}'],
                        ['Linear regression, cross-validated MAE (mean of 4 folds; lowest to highest)', f'{f2(line["cv_mean"])} ({f2(line["cv_min"])} to {f2(line["cv_max"])})']],
                  widths=[7.8, 3.4], icons=['lock', 'chart', 'gear', 'cross', 'flag', 'flag', 'pin', 'check'],
                  note='If your number differs, stop and ask. Do not change a number to match. Find the step that went wrong.',
                  notes=('Use this table as your checkpoint. If your numbers match, carry on. If they do not, stop and call me over, because every later step builds on the earlier ones. '
                         'The most common reason is a cell that was run out of order, or a new feature built on the training table but not on the validation table. '
                         'Do not edit a number to make it match. The aim is to understand why it is different, and that is a skill you will need in every project, including yours.')))

    S.append(dict(kind='table', title='Four errors you will meet, what they mean and what to do',
                  headers=['Error message', 'What it says', 'What to do'],
                  rows=[['KeyError: load_x_ambient', 'The new feature exists in one table only', 'Build it on both the training table and the validation table'],
                        ['ValueError: contains NaN', 'A model received a missing value (NaN) and has no imputation step', 'Wrap the model with with_imputer(...) or add a SimpleImputer to the pipeline'],
                        ['inconsistent numbers of samples', 'X and y have different numbers of rows because they come from different tables', 'Rebuild X_train and y_train from the same table'],
                        ['NameError: with_imputer', 'The cell that defines the helper function with_imputer has not been run', 'Run all cells from the top, in order']],
                  widths=[3.4, 4.2, 4.4], icons=['key', 'cross', 'flag', 'bell'],
                  notes=('Errors are normal, and reading them is a skill. Here are four you will most likely meet today. A key error on the new feature means you built it on the training table but not on the validation table, so build it on both. '
                         'A value error about NaN means a model has no imputation step, so use with_imputer. An error about inconsistent numbers of samples means X and y came from different tables. '
                         'And a name error on with_imputer means you skipped the helper cell, so run all cells from the top. Read the last line of the error first. It usually tells you the answer.')))

    S.append(dict(kind='list', title='How this class counts towards your coursework',
                  items=['The Block 2 quiz opens in the last 20 minutes of this class and stays open for 24 hours.', f'The Block 2 assignment (A9, A10, A11) closes on {C.COHORTS[code]["b2_close"]} (Kampala time).',
                         f'The Engineering ML project is an individual, timed, auto-graded 3-hour sitting worth 45 percent (Part A 30, Part B 15). Proposed: {proj}, lecturer to confirm.',
                         'The rehearsal (a practice project) is released after this class and is not marked.'],
                  icons=['clock', 'doc', 'lock', 'folder'],
                  notes=('A word on how this counts. The Block 2 quiz opens in the last twenty minutes of this class, after the lab, and stays open for twenty-four hours. The twenty-five minutes on the clock are for opening it and explaining how it works. '
                         f'The Block 2 assignment has three parts, A9, A10 and A11, and it closes on {C.COHORTS[code]["b2_close"]}, Kampala time. The project is an individual, timed, auto-graded sitting of three hours in Week 12, worth 45 percent of the course: '
                         f'Part A, the coded notebook, out of 30, and Part B, the structured decision memo, out of 15. The proposed time for your cohort is {proj}, and your lecturer confirms it. '
                         'The rehearsal is released right after this class and is not marked. Use it to practise.')))

    s['facilitator'] = dict(
        prep=['Open the deck in Slide Show mode and the lab notebook in Colab before anyone arrives. Run the notebook from the top once so you know it works on your account.',
              'Put the lab notebook and engineering_data.csv in the shared class folder and post the link. Every learner needs both files in Colab, in the Files panel.',
              'Write the "check your numbers" table on the board before the lab (numbers for your cohort are in the table below).',
              'Prepare the Block 2 quiz for the end of the class and confirm in writing how long it stays open. The deck says it opens in the last 20 minutes and stays open for 24 hours. The 25-minute slot on the clock is for opening it and explaining it. The deck has 32 authored slides, so keep the formula slides brisk.',
              'Have the rehearsal (the practice version of the project) ready to release right after the class. The project is an individual, timed, auto-graded 3-hour sitting in the Week 12 class slot, covering Weeks 1 to 11, worth 45 percent (Part A 30, Part B 15). The deck gives the proposed times as lecturer to confirm (CML3112 Tue 1 Dec 11:00 to 14:00, CML3113 Fri 4 Dec 08:00 to 11:00, CML3111 Fri 4 Dec 11:00 to 14:00). Confirm them in writing.'],
        misconceptions=[('A clever new feature must help', 'Test it. Here the load_x_ambient column changes the error by hardly anything.'),
                        ('The model with the lowest number on the table is the one to choose', 'Look at the cross-validated range too, and prefer the simpler model when scores are close.'),
                        ('Equipment_id should be a feature because it is in the file', 'The model must work on a machine it has never met, and a new machine has no column of its own.'),
                        ('A bigger alpha or a bigger k is always safer', 'Too much penalty or too many neighbours flattens the pattern. The error goes up again.'),
                        ('The test set can be used to pick between two close models', 'It is opened once, at the very end. After that it cannot give a fair number.')],
        probes=[('What is a feature ablation?', 'Change one thing, keep everything else the same, and compare on the same validation rows.'),
                ('What is an interaction feature?', 'A column made by multiplying two features, here load_pct times ambient_c.'),
                ('Why do we leave equipment_id out of the features?', 'The model must work on a new machine. A group it never saw would have no column of its own.'),
                ('Why do ridge regression and k-NN need scaled features?', 'The penalty and the distance both depend on units, so a feature with big numbers would dominate.'),
                ('What does a bigger alpha do?', 'Alpha is the regularisation strength. A bigger alpha makes the L2 penalty stronger and the curve flatter. Too big and the model underfits.'),
                ('Write the ridge regression loss in words.', 'The sum of the squared errors on the training rows, plus alpha times the sum of the squared weights.'),
                ('How does k-NN measure closeness?', 'By the Euclidean distance on the scaled features: square the gaps, add them, take the square root.'),
                ('What does k mean in k-NN?', 'The number of closest training rows that are averaged to make the prediction.'),
                ('Why does the table show a cross-validated range?', 'One validation group of 15 rows can mislead. The range shows how much the score moves when other machines take a turn.'),
                ('When two models score about the same, which do you pick?', 'The simpler one (parsimony), because it is easier to explain, check and maintain.'),
                ('Who may open the test set, and when?', 'Nobody until the model is chosen, and then only once. Otherwise it stops being a fair held-out test.')],
        lab_steps=[('Step 1: prepare', 'Rows left to model with: 88. Rows 58, 15, 15. Anyone with different numbers has run a cell twice or changed a cleaning rule.'),
                   ('Step 2: first loop', 'Three models, one loop (pipeline with median imputation). Baseline model, linear regression and decision tree match the Class 1 model comparison table. Ask why the loop keeps the comparison fair.'),
                   ('Step 3: features', 'Four versions of the linear regression model. Removing ambient_c hurts a lot. The product and the squared load change the MAE by less than 0.03. Resist the urge to explain the product away: the lesson is that the data decide.'),
                   ('Step 4: one-hot encoding', 'The validation group has an is_E5 column that the training table lacks. This is the whole argument for leaving equipment_id out.'),
                   ('Step 5: scaling and ridge regression', 'Ridge regression on two features gets slightly worse as alpha grows. The degree-6 curve on load alone improves at alpha 1 and worsens at alpha 100, and its biggest weight shrinks from thousands to single figures.'),
                   ('Step 6: k-NN', 'k = 3 is best of 1, 3 and 20. The three neighbours of the first validation row are printed, and their average is the prediction.'),
                   ('Step 7: the model comparison table', 'Five rows. Linear regression has the lowest cross-validated MAE. In one cohort a different model has a lower validation MAE: use it to talk about 15 rows and luck.'),
                   ('Step 8 and 9: memo and save', 'Collect one memo sentence from three learners. Insist on restart and run all before saving.')],
        rescue=['If the concepts run over, drop the scaling slide and say that ridge and k-NN need scaled features, as in Class 2. The formula slides and the worked-example tables are written for revision at home: read the formula aloud, point at one worked line and move on.', 'If only forty minutes of lab remain, do steps 1, 2, 3 and 7, and set ridge regression and k-NN as practice in the rehearsal.',
                'If wifi fails in the room, the notebook runs unchanged in VS Code, as in Week 2.', 'If several learners are stuck at the same cell, stop the room, run that cell on the projector and let them copy the fix.',
                'If the quiz must start early, cut the memo write-up and ask learners to finish it at home.'],
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
            row('Decision tree depth 4, MAE', lambda f, k: f'{cd(k, "Decision tree, depth 4")["mae"]:.2f} {f["unit"]}'),
            row('Extended linear regression, intercept b_0 and weights b_1, b_2, b_3', lambda f, k: ', '.join(f'{v:.4f}' for v in [k['lines']['b']['b0']] + k['lines']['b']['w'])),
            row('Ridge regression loss at alpha 1 (squared errors + L2 penalty)', lambda f, k: f'{k["ridge_tab"][2]["sse"]:.1f} + {k["ridge_tab"][2]["pen"]:.1f} = {k["ridge_tab"][2]["loss"]:.1f}'),
            row('k-NN worked example, nearest distance and prediction', lambda f, k: f'd = {k["knn_tab"][0]["d"]:.3f}, prediction {k["knn_ex"]["prediction"]:.1f} {f["unit"]}'),
            row('Linear regression, cross-validated MAE (lowest to highest)', lambda f, k: f'{cd(k, "Linear regression")["cv_mean"]:.2f} ({cd(k, "Linear regression")["cv_min"]:.2f} to {cd(k, "Linear regression")["cv_max"]:.2f})'),
            row('Lowest validation MAE among the four models', lambda f, k: k['best_val'])]
