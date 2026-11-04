"""Checks for content/loans_canon.py.  Run:  python3 -I ref/verify_loans_canon.py   (uses the NumPy scikit-learn stand-in in ref/ where it covers the same algorithm).
It proves internal consistency and agreement with the stand-ins. It does NOT prove agreement with real scikit-learn: do that on a machine that has it (see LOANS_RECIPE.md)."""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'content'))
sys.path.insert(0, str(HERE))
import loans_canon as L  # noqa: E402
import sk_tree_replica as TREE  # noqa: E402
import week_reference_numpy as WR  # noqa: E402

ok = True


def check(name, cond, detail=''):
    global ok
    ok &= bool(cond)
    print(('PASS ' if cond else 'FAIL ') + name + (f'   {detail}' if detail else ''))


loans = L.prepare()
y = loans.default.to_numpy()
check('8,000 rows, 1,004 defaults', len(loans) == 8000 and y.sum() == 1004)
check('no impossible ages left', loans.age.between(18, 100).all() and loans.age.min() >= 18)
raw_age = L.pd.read_csv(L.DATA / 'loans.csv').age
check('the two impossible ages became 36', (loans.age[(raw_age < 18) | (raw_age > 100)] == 36).all() and ((raw_age < 18) | (raw_age > 100)).sum() == 2)
check('SPLIT_CHECK constants match', L.split_indices(y)[1][:10].tolist() == L.SPLIT_CHECK['first10_test_index'] and int(L.split_indices(y)[1].sum()) == L.SPLIT_CHECK['sum_test_index'])
check('no blank income', loans.monthly_income_ugx.notna().all() and loans.income_missing.sum() == 379)
check('12 numeric + 15 indicators', len(L.FEATURES) == 12 and len(L.indicator_columns(loans)) == 15 and 'burden' not in loans.columns)
r0 = loans.iloc[0]
check('instalment_to_income hand check row 0', abs(r0.instalment_to_income - 1583200 * 1.15 / 6 / 505300) < 1e-12, f'{r0.instalment_to_income:.4f}')

# ---- split
tr, te = L.split_indices(y)
check('partition: 6,000 + 2,000, disjoint, all rows', len(tr) == 6000 and len(te) == 2000 and len(set(tr) | set(te)) == 8000)
check('stratified counts 753 / 251', y[tr].sum() == 753 and y[te].sum() == 251)
rng = np.random.RandomState(0)
cm = L._approximate_mode(np.array([6996, 1004]), 2000, np.random.RandomState(1))
check('_approximate_mode hand check [1749, 251]', list(cm) == [1749, 251], str(cm))
cm2 = L._approximate_mode(np.array([5, 5, 5]), 7, np.random.RandomState(1))
check('_approximate_mode ties sum to n_draws', cm2.sum() == 7 and sorted(cm2) == [2, 2, 3])
from sklearn.model_selection import train_test_split as sk_tts  # the stand-in (non-stratified permutation)  # noqa: E402
X = np.arange(8000)
a, b = sk_tts(X, test_size=0.25, random_state=42)
trn, ten = L.split_indices(y, stratify=False)
check('non-stratified replica equals the stand-in train_test_split', list(b) == list(ten) and list(a) == list(trn), f'test defaults {y[ten].sum()}')
Xtr, Xte, ytr, yte = L.split(loans)
check('split() returns pandas with original labels', list(Xtr.index[:5]) == list(tr[:5]) and Xtr.shape == (6000, 12) and Xte.shape == (2000, 12))
check('split(columns="all") has 27 columns', L.split(loans, 'all')[0].shape == (6000, 27))
f = L.stratified_kfold(ytr, 5)
sizes = [(f == i).sum() for i in range(5)]
check('5 folds of 1,200 with 150 or 151 defaults', sizes == [1200] * 5 and set(int(ytr[f == i].sum()) for i in range(5)) == {150, 151})
sys.path.insert(0, str(HERE.parent / 'content'))
import h_loans as H  # noqa: E402  (older helper that deals blocks by sorted class)
check('stratified_kfold equals the older helper in h_loans.py', list(f) == list(H.stratified_folds(ytr, 5)))

# ---- logistic regression
cols = L.FEATURES
m = L.ScaledLogReg().fit(Xtr, ytr)
p = m.predict_proba(Xte)
check('probabilities strictly inside (0, 1)', (p > 0).all() and (p < 1).all(), f'min {p.min():.2e} max {p.max():.7f}')
check('gradient at the optimum is ~0', m.grad_max_ < 1e-8, f'{m.grad_max_:.1e}')
# independent: the stand-in Newton solver on scaled data (a different code path)
Z = (Xtr.to_numpy(float) - Xtr.to_numpy(float).mean(0)) / Xtr.to_numpy(float).std(0)
b0, w0 = WR.logreg_fit(Z, ytr.to_numpy(float), C=1.0, iters=200)
check('same optimum as the reference-module solver', abs(b0 - m.intercept_) < 1e-8 and np.max(np.abs(w0 - m.coef_)) < 1e-8, f'max coef diff {np.max(np.abs(w0 - m.coef_)):.1e}')
# optimum by perturbation: objective at the optimum <= objective at random nearby points
A = np.column_stack([np.ones(len(Z)), Z])


def obj(th):
    z = A @ th
    return 0.5 * np.sum(th[1:] ** 2) + np.sum(np.logaddexp(0, z) - ytr.to_numpy(float) * z)


th0 = np.r_[m.intercept_, m.coef_]
r = np.random.RandomState(1)
check('objective is lowest at the optimum (200 random perturbations)', all(obj(th0 + 1e-3 * r.randn(13)) > obj(th0) for _ in range(200)))
# AUC: three methods
auc1, auc2 = L.auc_rank(yte, p), L.auc_trapezoid(yte, p)
pos, neg = p[yte.to_numpy() == 1], p[yte.to_numpy() == 0]
auc3 = ((pos[:, None] > neg[None, :]).sum() + 0.5 * (pos[:, None] == neg[None, :]).sum()) / (len(pos) * len(neg))
check('AUC by ranks = trapezoid = all-pairs count', abs(auc1 - auc2) < 1e-12 and abs(auc1 - auc3) < 1e-12, f'{auc1:.6f}')
from sklearn import metrics as SM  # noqa: E402  (stand-in; may lack roc_auc_score)
if hasattr(SM, 'roc_auc_score'):
    check('AUC equals the stand-in roc_auc_score', abs(SM.roc_auc_score(yte, p) - auc1) < 1e-9)
c = L.at_threshold(yte, p, 0.2)
check('confusion at 0.2 adds to 2,000 and matches a manual count', c['tp'] + c['fp'] + c['fn'] + c['tn'] == 2000 and c['tp'] == int(((p >= 0.2) & (yte.to_numpy() == 1)).sum()))
check('rule threshold 100/1100', abs(L.RULE_THRESHOLD - 1 / 11) < 1e-15)
tab, extra = L.cost_table(yte, p)
check('flag nobody 251 M, flag everybody 174.9 M', extra == dict(none=251_000_000, all=174_900_000))

# ---- tree equals the ref replica
t_new = L.fit_tree(Xtr, ytr, 3, 42)
t_old = TREE.fit(Xtr.to_numpy(float), ytr.to_numpy(), 3, 'clf', 42)
check('tree identical to ref/sk_tree_replica.py (structure, features, thresholds, leaves)', repr(t_new) == repr(t_old))
from sklearn.tree import DecisionTreeClassifier as DT  # stand-in, which wraps the same replica  # noqa: E402
pred_stand = DT(max_depth=3, random_state=42).fit(Xtr, ytr).predict(Xte)
pred_new = L.tree_predict(t_new, Xte)
check('tree predictions equal the stand-in (differs only if a leaf is exactly 0.5)', (pred_stand == pred_new).all())

# ---- sensitivity to the lbfgs stopping rule: a small L-BFGS with scikit-learn's stop rule (max |gradient of the AVERAGED loss| < 1e-4)
def lbfgs(th, tol=1e-4, mem=10, maxit=1000):
    n = len(Z)
    def fg(t):
        z = A @ t
        pr = 1 / (1 + np.exp(-z))
        f = (np.sum(np.logaddexp(0, z) - ytr.to_numpy(float) * z) + 0.5 * np.sum(t[1:] ** 2)) / n
        g = (A.T @ (pr - ytr.to_numpy(float)) + np.r_[0, t[1:]]) / n
        return f, g
    f, g = fg(th)
    S, Y = [], []
    for it in range(maxit):
        if np.max(np.abs(g)) <= tol:
            return th, it
        q = g.copy()
        al = []
        for s, yv in reversed(list(zip(S, Y))):
            a_ = (s @ q) / (yv @ s)
            al.append(a_)
            q -= a_ * yv
        if S:
            q *= (S[-1] @ Y[-1]) / (Y[-1] @ Y[-1])
        for (s, yv), a_ in zip(zip(S, Y), reversed(al)):
            q += s * (a_ - (yv @ q) / (yv @ s))
        d = -q
        step = 1.0 if S else 1 / max(1e-12, np.linalg.norm(g))
        while True:
            f2, g2 = fg(th + step * d)
            if f2 <= f + 1e-4 * step * (g @ d) or step < 1e-12:
                break
            step *= 0.5
        s_, y_ = step * d, g2 - g
        if s_ @ y_ > 1e-12:
            S.append(s_)
            Y.append(y_)
            S, Y = S[-mem:], Y[-mem:]
        th, f, g = th + step * d, f2, g2
    return th, maxit


th_lb, its = lbfgs(np.zeros(13))
p_lb = 1 / (1 + np.exp(-(np.column_stack([np.ones(2000), (Xte.to_numpy(float) - Xtr.to_numpy(float).mean(0)) / Xtr.to_numpy(float).std(0)]) @ th_lb)))
d_auc = abs(L.auc_rank(yte, p_lb) - auc1)
cnt = [L.at_threshold(yte, p_lb, t) for t in (0.5, 0.3, 0.2, 0.15, 0.1)]
ref_cnt = [L.at_threshold(yte, p, t) for t in (0.5, 0.3, 0.2, 0.15, 0.1)]
dtp = max(abs(a['tp'] - b['tp']) + abs(a['fp'] - b['fp']) for a, b in zip(cnt, ref_cnt))
print(f'INFO  own L-BFGS stopped after {its} iterations at the scikit-learn tolerance: max coefficient difference {np.max(np.abs(th_lb - th0)):.1e}, AUC difference {d_auc:.1e}, largest change in tp+fp across thresholds {dtp}')
check('lbfgs-tolerance solution changes AUC by < 0.001', d_auc < 1e-3)
print('\nALL PASS' if ok else '\nSOME FAILED')
sys.exit(0 if ok else 1)
