"""Shared numbers for Sessions 15 and 16 (author h). Since 4 Nov 2026 (review fix) every number comes from content/loans_canon.py, the one shared recipe for the Nile Microfinance loans:
8,000 loans, stratified 6,000 / 2,000 split (seed 42, 251 test defaults), 27 columns (12 numeric + 15 indicators), make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
thresholds chosen on the TRAINING rows (cross-validation or the cost rule 0.0909), the test loans used once. All of it is a NumPy replica: re-run on real scikit-learn in Colab before the course starts."""
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

BUILD = Path(__file__).resolve().parents[1]
DATA = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'data'
sys.path.insert(0, str(BUILD / 'ref'))
sys.path.insert(0, str(BUILD / 'content'))
import loans_canon as C  # noqa: E402

MONEY = ['monthly_income_ugx', 'loan_amount_ugx', 'savings_balance_ugx']
HONEST = ['age', 'monthly_income_ugx', 'loan_amount_ugx', 'term_months', 'previous_loans', 'previous_late_payments', 'group_loan', 'savings_balance_ugx', 'has_mobile_money', 'distance_to_branch_km']
COST_MISS, COST_ALARM = 1_000_000, 100_000     # illustrative teaching costs in UGX


def n(x):
    return f'{int(x):,}'


# ------------------------------------------------------------------ models and metrics in NumPy (independent of scikit-learn)
def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def logreg_fit(X, y, C=1.0, sample_weight=None, iters=200):
    """L2 logistic regression by Newton steps. Minimises 0.5*sum(w^2) + C*sum(s_i * log loss_i); the intercept is not penalised (the scikit-learn objective)."""
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    s = np.ones(len(y)) if sample_weight is None else np.asarray(sample_weight, float)
    A = np.column_stack([np.ones(len(X)), X])
    th = np.zeros(A.shape[1])
    pen = np.eye(A.shape[1])
    pen[0, 0] = 0
    for _ in range(iters):
        p = sigmoid(A @ th)
        g = pen @ th + C * A.T @ (s * (p - y))
        H = pen + C * (A.T * (s * p * (1 - p))) @ A
        step = np.linalg.solve(H, g)
        th -= step
        if np.max(np.abs(step)) < 1e-10:
            break
    return th[0], th[1:]


def predict_p(b, w, X):
    return sigmoid(b + np.asarray(X, float) @ w)


def balanced_weights(y):
    y = np.asarray(y)
    cnt = np.bincount(y.astype(int))
    return (len(y) / (2 * cnt))[y.astype(int)]


def confusion(y, flag):
    y = np.asarray(y).astype(int)
    f = np.asarray(flag).astype(int)
    return dict(tp=int(((y == 1) & (f == 1)).sum()), fp=int(((y == 0) & (f == 1)).sum()), fn=int(((y == 1) & (f == 0)).sum()), tn=int(((y == 0) & (f == 0)).sum()))


def prf(c):
    pr = c['tp'] / (c['tp'] + c['fp']) if c['tp'] + c['fp'] else 0.0
    rc = c['tp'] / (c['tp'] + c['fn']) if c['tp'] + c['fn'] else 0.0
    f1 = 2 * pr * rc / (pr + rc) if pr + rc else 0.0
    return dict(precision=pr, recall=rc, f1=f1, accuracy=(c['tp'] + c['tn']) / sum(c.values()), fpr=c['fp'] / (c['fp'] + c['tn']))


def auc_rank(y, score):
    """AUC as the probability that a random positive scores higher than a random negative (ties count half), by ranks."""
    y = np.asarray(y).astype(int)
    r = pd.Series(np.asarray(score, float)).rank(method='average').to_numpy()
    npos, nneg = (y == 1).sum(), (y == 0).sum()
    return float((r[y == 1].sum() - npos * (npos + 1) / 2) / (npos * nneg))


def roc_points(y, score):
    y = np.asarray(y).astype(int)
    s = np.asarray(score, float)
    ths = np.r_[np.inf, np.unique(s)[::-1]]
    P, N = (y == 1).sum(), (y == 0).sum()
    fpr = np.array([((s >= t) & (y == 0)).sum() / N for t in ths])
    tpr = np.array([((s >= t) & (y == 1)).sum() / P for t in ths])
    return fpr, tpr, ths


def pr_points(y, score):
    y = np.asarray(y).astype(int)
    s = np.asarray(score, float)
    ths = np.unique(s)
    P = (y == 1).sum()
    prec = np.array([((s >= t) & (y == 1)).sum() / max(1, (s >= t).sum()) for t in ths])
    rec = np.array([((s >= t) & (y == 1)).sum() / P for t in ths])
    return prec, rec, ths


def stratified_folds(y, k=5):
    """The assignment used by scikit-learn's StratifiedKFold(n_splits=k) without shuffling: within each class, rows in their original order are dealt to folds in blocks."""
    y = np.asarray(y).astype(int)
    classes, yenc = np.unique(y, return_inverse=True)
    order = np.sort(yenc)
    alloc = np.array([np.bincount(order[i::k], minlength=len(classes)) for i in range(k)])
    fold = np.empty(len(y), int)
    for c in range(len(classes)):
        fold[yenc == c] = np.arange(k).repeat(alloc[:, c])
    return fold


@lru_cache(maxsize=None)
def facts():
    F = {}
    CF = C.facts()
    F['canon'] = CF
    raw = pd.read_csv(DATA / 'loans.csv')
    F['raw_rows'], F['raw_cols'] = raw.shape
    F['bad_ages'] = len(CF['bad_ages'])
    F['missing_income'] = CF['income_blank']
    loans = C.prepare()
    F['median_income'] = CF['income_median']
    F['loans'] = loans
    F['rows'] = len(loans)
    F['default_rate'] = float(loans.default.mean())
    F['raw_default_rate'] = F['default_rate']
    F['raw_repaid'], F['raw_defaulted'] = int((raw.default == 0).sum()), int((raw.default == 1).sum())
    feat_cols = C.feature_columns(loans, 'all')
    F['features_text'] = list(C.CATEGORICAL)
    F['feat_shape'] = (len(loans), len(C.FEATURES) + len(C.CATEGORICAL))      # 12 numeric + 3 text variables = 15 features
    F['cols'] = feat_cols
    X = loans[feat_cols]
    F['X'] = X
    F['X_shape'] = X.shape
    y = loans.default.to_numpy()
    F['y'] = y
    tr, te = C.split_indices(y)
    F['tr'], F['te'] = tr, te
    Xtr, Xte, ytr, yte = X.to_numpy(float)[tr], X.to_numpy(float)[te], y[tr], y[te]
    F['Xtr'], F['Xte'], F['ytr'], F['yte'] = Xtr, Xte, ytr, yte
    F['n_train'], F['n_test'] = len(tr), len(te)
    F['test_pos'], F['test_neg'] = int(yte.sum()), int((yte == 0).sum())
    F['train_pos'] = int(ytr.sum())
    F['test_rate'] = F['test_pos'] / F['n_test']
    # logistic regression: make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)), C = 1.0 (L2), coefficients per 1 standard deviation
    m = C.ScaledLogReg().fit(pd.DataFrame(Xtr, columns=feat_cols), ytr)
    F['model'] = m
    F['lr_b'], F['lr_w'] = float(m.intercept_), m.coef_
    F['Zte'] = (Xte - m.mean_) / m.scale_
    F['p_lr'] = m.predict_proba(Xte)
    F['coef'] = dict(zip(feat_cols, m.coef_))
    F['auc_lr'] = C.auc_rank(yte, F['p_lr'])
    F['thr_rows'] = {}
    for t in (0.5, 0.3, 0.2, 0.15, 0.1):
        c = confusion(yte, F['p_lr'] >= t)
        F['thr_rows'][t] = dict(c, flagged=c['tp'] + c['fp'], **prf(c), cost=c['fn'] * COST_MISS + c['fp'] * COST_ALARM)
    rule = C.RULE_THRESHOLD
    c = confusion(yte, F['p_lr'] >= rule)
    F['rule_row'] = dict(c, flagged=c['tp'] + c['fp'], **prf(c), cost=c['fn'] * COST_MISS + c['fp'] * COST_ALARM)
    # decision trees on the 27 columns (depth 3 for the lab, depth 2 for the concepts slide)
    F['tree3'] = C.fit_tree(Xtr, ytr, 3)
    F['tree2'] = C.fit_tree(Xtr, ytr, 2)
    F['p_tree'] = C.tree_proba(F['tree3'], Xte)
    F['auc_tree'] = C.auc_rank(yte, F['p_tree'])
    F['tree_leaves'] = len(set(np.round(F['p_tree'], 9)))
    # THRESHOLD CHOICE ON THE TRAINING ROWS: 5-fold out-of-fold probabilities, cost per 2,000 loans (training cost x 2000 / 6000)
    oof = C.oof_proba(Xtr, ytr)
    F['oof'] = oof
    ttab, _ = C.cost_table(ytr, oof)
    scale = len(te) / len(tr)
    F['cost_grid_cv'] = {t: v * scale for t, v in ttab.items()}
    F['cv_t'] = C.cheapest(ttab)
    F['cost_cv_curve_at_cv_t'] = F['cost_grid_cv'][F['cv_t']]
    F['cost_none_cv'] = int(ytr.sum()) * COST_MISS * scale
    F['cost_all_cv'] = int((ytr == 0).sum()) * COST_ALARM * scale
    cvc = confusion(yte, F['p_lr'] >= F['cv_t'])
    F['cv_row'] = dict(cvc, flagged=cvc['tp'] + cvc['fp'], **prf(cvc), cost=cvc['fn'] * COST_MISS + cvc['fp'] * COST_ALARM)
    # test-set costs: used ONCE, to report the choices above (never to search)
    F['cost_test'] = {t: F['thr_rows'][t]['cost'] for t in F['thr_rows']}
    F['cost_none'] = F['test_pos'] * COST_MISS                 # flag nobody
    F['cost_all'] = F['test_neg'] * COST_ALARM                 # flag everybody
    F['cheapest_on_test_for_contrast'] = CF['cheapest_on_test_27']
    # leakage and weights (S16)
    F['calls_mean'] = {int(k): float(v) for k, v in loans.groupby('default').collection_calls.mean().items()}
    F['calls_max'] = {int(k): int(v) for k, v in loans.groupby('default').collection_calls.max().items()}
    F['calls_min_default'] = int(loans[loans.default == 1].collection_calls.min())
    F['share_repaid_with_call'] = float((loans[loans.default == 0].collection_calls > 0).mean())
    F['share_default_with_call'] = float((loans[loans.default == 1].collection_calls > 0).mean())
    num = loans[C.FEATURES + ['collection_calls', 'default']].corr()['default'].drop('default').abs().sort_values(ascending=False)
    F['corr_top'] = [(k, float(v)) for k, v in num.head(3).items()]
    F['corr_calls'] = float(loans[['collection_calls', 'default']].corr().iloc[0, 1])
    F['no_calls_default'] = int(((loans.default == 1) & (loans.collection_calls == 0)).sum())
    return F


if __name__ == '__main__':
    F = facts()
    for k in ('rows', 'default_rate', 'X_shape', 'n_train', 'n_test', 'test_pos', 'auc_lr', 'auc_tree', 'tree_leaves', 'cv_t', 'cost_none', 'cost_all', 'calls_mean', 'calls_max', 'corr_top', 'corr_calls', 'share_repaid_with_call', 'no_calls_default'):
        print(k, F[k])
    for t, r in F['thr_rows'].items():
        print(t, r)
    print({t: round(c / 1e6, 1) for t, c in F['cost_grid_cv'].items() if t in (0.05, 0.08, 0.1, 0.12, 0.15, 0.2, 0.3, 0.5)})
