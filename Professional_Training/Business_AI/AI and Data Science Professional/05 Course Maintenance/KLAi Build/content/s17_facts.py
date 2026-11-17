"""Numbers for Session 17 (forests, boosting, overfitting), author i. Every number on a slide, in a note or in the notebook checks comes from facts().
scikit-learn is not installed here, so trees, bagging, a random forest, gradient boosting, logistic regression, permutation importance, polynomial fits and stratified folds are
written in NumPy in ds_i_np.py (from the textbook definitions). Logistic regression, one decision tree and gradient boosting (no random numbers) should match scikit-learn closely.
A random forest uses random numbers, so scikit-learn's forest will be close to ours but not identical: the notebook checks allow for that.
The result is cached in content/_cache/ because the grid search takes a few minutes; the cache is rebuilt whenever this file or ds_i_np.py changes."""
import hashlib
import pickle
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ds_i_np as NP  # noqa: E402
import loans_canon as LC  # noqa: E402

BUILD = HERE.parent
DATA = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'data'
COLS = ['age', 'monthly_income_ugx', 'income_missing', 'loan_amount_ugx', 'term_months', 'previous_loans', 'previous_late_payments', 'group_loan', 'savings_balance_ugx', 'has_mobile_money',
        'distance_to_branch_km', 'instalment_to_income']
GRID_DEPTH = [3, 6, None]
GRID_LEAF = [1, 10, 30]
POLY_TRAIN = 15
POLY_SEED = 1
POLY_DEGREES = list(range(0, 8))
TREE_DEPTHS = [1, 2, 3, 4, 6, 8, 12, None]
FOREST_STEPS = [1, 5, 10, 25, 50, 100, 200]
BOOST_STEPS = [10, 25, 50, 100, 200, 300, 500]


def stratified_folds(y, k=5):
    """The fold of each row under scikit-learn's StratifiedKFold(n_splits=k) without shuffling: within each class the rows, in their order, are dealt out in blocks."""
    y = np.asarray(y).astype(int)
    classes, yenc = np.unique(y, return_inverse=True)
    order = np.sort(yenc)
    alloc = np.array([np.bincount(order[i::k], minlength=len(classes)) for i in range(k)])
    fold = np.empty(len(y), int)
    for c in range(len(classes)):
        fold[yenc == c] = np.arange(k).repeat(alloc[:, c])
    return fold


def prepare():
    """The canonical loans preparation and split (loans_canon.py): 8,000 rows, stratified 6,000 / 2,000 split equal to train_test_split(test_size=0.25, stratify=y, random_state=42)."""
    loans = LC.prepare()
    raw = pd.read_csv(DATA / 'loans.csv')
    F = dict(raw_rows=len(raw))
    F['bad_ages'] = int(((raw.age < 18) | (raw.age > 100)).sum())
    F['rows'] = len(loans)
    F['income_blank'] = int(raw.monthly_income_ugx.isna().sum())
    F['median_income'] = float(raw.monthly_income_ugx.median())
    X = loans[COLS]
    y = loans.default.to_numpy()
    F['default_rate'] = float(y.mean())
    F['defaults'] = int(y.sum())
    tr, te = LC.split_indices(y)
    F['n_train'], F['n_test'] = len(tr), len(te)
    F['canon'] = LC.facts()
    return F, loans, X, y, tr, te


def poly_story():
    bw = pd.read_csv(DATA / 'branch_weeks.csv')
    g = bw[bw.branch_id == 'B04'].reset_index(drop=True)
    f = g.footfall.values.astype(float)
    mu, sd = f.mean(), f.std(ddof=1)
    x = (f - mu) / sd
    y = g.orders.values.astype(float)
    idx = np.random.default_rng(POLY_SEED).permutation(len(g))
    tr, te = idx[:POLY_TRAIN], idx[POLY_TRAIN:]
    P = dict(weeks=len(g), n_train=len(tr), n_test=len(te), footfall=f.tolist(), orders=y.tolist(), tr=tr.tolist(), te=te.tolist(), r=float(np.corrcoef(f, y)[0, 1]))
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        rows = []
        for d in POLY_DEGREES:
            c = np.polyfit(x[tr], y[tr], d)
            res = np.polyval(c, x) - y
            rows.append((d, float(np.sqrt(np.mean(res[tr] ** 2))), float(np.sqrt(np.mean(res[te] ** 2)))))
        P['rmse'] = rows
        grid = np.linspace(f.min(), f.max(), 120)
        P['curves'] = {d: (grid.tolist(), np.polyval(np.polyfit(x[tr], y[tr], d), (grid - mu) / sd).tolist()) for d in (0, 1, 6)}
    P['sd_orders'] = float(y.std(ddof=1))
    return P


def compute():
    F, loans, X, y, tr, te = prepare()
    Xv = X.to_numpy(float)
    Xtr, Xte, ytr, yte = Xv[tr], Xv[te], y[tr], y[te]
    F['train_default_rate'], F['test_default_rate'] = float(ytr.mean()), float(yte.mean())
    F['poly'] = poly_story()
    # logistic regression: scaled, then fitted (Pipeline of StandardScaler and LogisticRegression)
    mu, sd = Xtr.mean(0), Xtr.std(0)
    Z = lambda A: (A - mu) / sd
    b, w = NP.logreg_fit(Z(Xtr), ytr)
    p_tr, p_te = NP.logreg_p(b, w, Z(Xtr)), NP.logreg_p(b, w, Z(Xte))
    F['lr'] = dict(b=b, w=w.tolist(), train=NP.auc(ytr, p_tr), test=NP.auc(yte, p_te), cols=COLS, mu=mu.tolist(), sd=sd.tolist())
    # a worked loan for the log-odds slide: the test loan whose predicted chance is closest to the median predicted chance
    k = int(np.argsort(np.abs(p_te - np.median(p_te)))[0])
    F['lr']['example'] = dict(row=Xte[k].tolist(), z=Z(Xte[k:k + 1])[0].tolist(), logodds=float(b + Z(Xte[k:k + 1])[0] @ w), p=float(p_te[k]), actual=int(yte[k]))
    # baseline (predict the training default share for everyone): AUC is 0.5 by definition; accuracy for always-no
    F['baseline_acc'] = float(1 - yte.mean())
    # single trees by depth
    rows = []
    for d in TREE_DEPTHS:
        T = NP.Tree(d).fit(Xtr, ytr)
        rows.append(dict(depth=d, real_depth=T.depth(), leaves=T.n_leaves(), train=NP.auc(ytr, T.predict(Xtr)), test=NP.auc(yte, T.predict(Xte))))
    F['tree_rows'] = rows
    F['tree_best'] = max(rows, key=lambda r: r['test'])
    # the first splits of three trees grown on three bootstrap samples (depth 3)
    rng = np.random.default_rng(11)
    boots = []
    for i in range(3):
        bi = rng.integers(0, len(ytr), len(ytr))
        T = NP.Tree(3).fit(Xtr[bi], ytr[bi])
        boots.append(dict(root=COLS[T.feat[0]], root_thr=float(T.thr[0]), left=COLS[T.feat[T.left[0]]] if T.feat[T.left[0]] >= 0 else None, right=COLS[T.feat[T.right[0]]] if T.feat[T.right[0]] >= 0 else None,
                          test=NP.auc(yte, T.predict(Xte)), oob=float(1 - len(np.unique(bi)) / len(ytr))))
    F['boot_trees'] = boots
    # bootstrap example on eight row numbers
    r8 = np.random.default_rng(5)
    ex = [sorted((r8.integers(1, 9, 8)).tolist()) for _ in range(3)]
    F['boot_demo'] = ex
    # forest: AUC against the number of trees (random forest: fully grown trees, 3 of the 12 variables tried at each split)
    forest = NP.Forest(200, None, 1, 3, seed=42).fit(Xtr, ytr)
    F['forest_curve'] = [dict(trees=k, test=NP.auc(yte, forest.predict_proba1(Xte, k))) for k in FOREST_STEPS]
    F['forest100'] = dict(train=NP.auc(ytr, forest.predict_proba1(Xtr, 100)), test=NP.auc(yte, forest.predict_proba1(Xte, 100)))
    single = [NP.auc(yte, t.predict(Xte)) for t in forest.trees[:100]]
    F['single_tree'] = dict(mean=float(np.mean(single)), lo=float(np.min(single)), hi=float(np.max(single)), n=len(single))
    # plain bagging (all 12 variables tried at each split), 100 trees, for comparison
    bag = NP.Forest(100, None, 1, None, seed=42).fit(Xtr, ytr)
    F['bag100'] = dict(train=NP.auc(ytr, bag.predict_proba1(Xtr)), test=NP.auc(yte, bag.predict_proba1(Xte)))
    # gradient boosting: learning rate 0.1, depth 3
    boost = NP.Boost(max(BOOST_STEPS), 0.1, 3).fit(Xtr, ytr)
    F['boost_curve'] = [dict(trees=k, train=NP.auc(ytr, boost.predict_proba1(Xtr, k)), test=NP.auc(yte, boost.predict_proba1(Xte, k))) for k in BOOST_STEPS]
    F['boost_stage_test'] = [NP.auc(yte, boost.predict_proba1(Xte, k)) for k in range(1, max(BOOST_STEPS) + 1)]
    F['boost_stage_best_n'] = int(np.argmax(F['boost_stage_test'])) + 1
    F['boost_stage_best'] = float(max(F['boost_stage_test']))
    F['boost100'] = next(r for r in F['boost_curve'] if r['trees'] == 100)
    F['boost_best'] = max(F['boost_curve'], key=lambda r: r['test'])
    # boosting by hand on six Jinja weeks (squared error; stumps; learning rate 0.5)
    P = F['poly']
    rr = np.random.default_rng(3).permutation(P['weeks'])[:6]
    rr = rr[np.argsort(np.array(P['footfall'])[rr])]
    fx, oy = np.array(P['footfall'])[rr], np.array(P['orders'])[rr]
    pred = np.full(6, oy.mean()); steps = [dict(pred=pred.copy(), resid=oy - pred, sse=float(((oy - pred) ** 2).sum()))]
    stumps = []
    for _ in range(2):
        T = NP.Tree(1).fit(fx.reshape(-1, 1), oy - pred)
        corr = 0.5 * T.predict(fx.reshape(-1, 1)); pred = pred + corr
        stumps.append(dict(feat_thr=float(T.thr[0]), corr=corr.copy()))
        steps.append(dict(pred=pred.copy(), resid=oy - pred, sse=float(((oy - pred) ** 2).sum())))
    F['hand'] = dict(footfall=fx.tolist(), orders=oy.tolist(), steps=[{k: (v.tolist() if hasattr(v, 'tolist') else v) for k, v in s.items()} for s in steps],
                     stumps=[{k: (v.tolist() if hasattr(v, 'tolist') else v) for k, v in s.items()} for s in stumps], lr=0.5)
    # grid search: 5-fold stratified cross-validation on the training rows, forest of 100 trees
    fold = stratified_folds(ytr, 5)
    grid = {}
    for md in GRID_DEPTH:
        for ml in GRID_LEAF:
            sc = []
            for k in range(5):
                a, v = fold != k, fold == k
                f = NP.Forest(100, md, ml, 3, seed=42).fit(Xtr[a], ytr[a])
                sc.append(NP.auc(ytr[v], f.predict_proba1(Xtr[v])))
            grid[(md, ml)] = dict(mean=float(np.mean(sc)), sd=float(np.std(sc)), folds=[float(s) for s in sc])
    F['grid'] = {f'{md}|{ml}': v for (md, ml), v in grid.items()}
    best = max(grid, key=lambda k: grid[k]['mean'])
    F['grid_best'] = dict(max_depth=best[0], min_leaf=best[1], **grid[best])
    tuned = NP.Forest(100, best[0], best[1], 3, seed=42).fit(Xtr, ytr)
    F['tuned'] = dict(train=NP.auc(ytr, tuned.predict_proba1(Xtr)), test=NP.auc(yte, tuned.predict_proba1(Xte)))
    F['grid_default_cv'] = grid[(None, 1)]['mean']
    # cross-validation scores of the other models, same folds
    def cv(make):
        sc = []
        for k in range(5):
            a, v = fold != k, fold == k
            sc.append(make(Xtr[a], ytr[a], Xtr[v], ytr[v]))
        return dict(mean=float(np.mean(sc)), sd=float(np.std(sc)))

    def lr_cv(A, ya, V, yv):
        m, s = A.mean(0), A.std(0); bb, ww = NP.logreg_fit((A - m) / s, ya)
        return NP.auc(yv, NP.logreg_p(bb, ww, (V - m) / s))
    F['cv_lr'] = cv(lr_cv)
    F['cv_boost'] = cv(lambda A, ya, V, yv: NP.auc(yv, NP.Boost(100, 0.1, 3).fit(A, ya).predict_proba1(V)))
    F['cv_tree3'] = cv(lambda A, ya, V, yv: NP.auc(yv, NP.Tree(3).fit(A, ya).predict(V)))
    # permutation importance of the tuned forest and the logistic regression on the test rows, 10 repeats
    imp, sdv = NP.perm_importance(lambda A: tuned.predict_proba1(A), Xte, yte, 10, seed=42)
    F['perm_forest'] = [dict(col=COLS[j], mean=float(imp[j]), sd=float(sdv[j])) for j in range(len(COLS))]
    imp, sdv = NP.perm_importance(lambda A: NP.logreg_p(b, w, Z(A)), Xte, yte, 10, seed=42)
    F['perm_lr'] = [dict(col=COLS[j], mean=float(imp[j]), sd=float(sdv[j])) for j in range(len(COLS))]
    # the limit: give the model a second copy of the most important variable
    top = int(np.argmax([r['mean'] for r in F['perm_forest']]))
    Xtr2, Xte2 = np.column_stack([Xtr, Xtr[:, top]]), np.column_stack([Xte, Xte[:, top]])
    tuned2 = NP.Forest(100, best[0], best[1], 3, seed=42).fit(Xtr2, ytr)
    imp2, sd2 = NP.perm_importance(lambda A: tuned2.predict_proba1(A), Xte2, yte, 10, seed=42)
    F['dup'] = dict(col=COLS[top], before=F['perm_forest'][top]['mean'], after_orig=float(imp2[top]), after_copy=float(imp2[-1]), test_auc=NP.auc(yte, tuned2.predict_proba1(Xte2)))
    # how strongly are the variables related to each other? (why importance shares credit)
    cm = pd.DataFrame(Xtr, columns=COLS).corr()
    F['corr'] = dict(burden_loan=float(cm.loc['instalment_to_income', 'loan_amount_ugx']), burden_income=float(cm.loc['instalment_to_income', 'monthly_income_ugx']), burden_term=float(cm.loc['instalment_to_income', 'term_months']),
                     loan_term=float(cm.loc['loan_amount_ugx', 'term_months']))
    return F


def _key():
    h = hashlib.sha1()
    for p in (HERE / 'ds_i_np.py', HERE / 'loans_canon.py', Path(__file__)):
        h.update(p.read_bytes())
    h.update(str((DATA / 'loans.csv').stat().st_size).encode())
    return h.hexdigest()


_MEM = {}


def facts():
    if 'F' in _MEM:
        return _MEM['F']
    cdir = HERE / '_cache'
    cdir.mkdir(exist_ok=True)
    cp = cdir / 's17_facts.pkl'
    key = _key()
    if cp.exists():
        d = pickle.loads(cp.read_bytes())
        if d.get('key') == key:
            _MEM['F'] = d['F']
            return d['F']
    F = compute()
    cp.write_bytes(pickle.dumps(dict(key=key, F=F)))
    _MEM['F'] = F
    return F


if __name__ == '__main__':
    import time
    t = time.time()
    F = facts()
    print('seconds', round(time.time() - t))
    for k, v in F.items():
        if k in ('poly', 'lr'):
            continue
        print(k, v)
    print('poly rmse', [(d, round(a, 1), round(b, 1)) for d, a, b in F['poly']['rmse']])
    print('lr', F['lr']['train'], F['lr']['test'], dict(zip(COLS, np.round(F['lr']['w'], 3))), F['lr']['example'])
