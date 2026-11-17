"""NumPy-only expected values for the Week 10 and Week 13 parts of Test 2.

Private to the grader. The student solution uses scikit-learn; these functions compute the same numbers from first
principles so the hidden checks do not depend on a pinned scikit-learn build. Agreement to 1e-6 is tested in
tests/test_test2_weeks8_13.py with a scikit-learn reference solution.
"""
import numpy as np

FEATURES = ['load_pct', 'ambient_c']
FOLD_GROUPS = ['E1', 'E2', 'E3', 'E4', 'E5']


def _xy(rows, cols):
    return np.array([[r[c] for c in cols] for r in rows], float), np.array([r['target'] for r in rows], float)


def _ols(X, y):
    A = np.column_stack([np.ones(len(X)), X])
    return np.linalg.lstsq(A, y, rcond=None)[0]


def _ols_predict(w, X): return w[0] + X @ w[1:]


def group_cv(rows):
    """Hold out each of E1 to E5 in turn (E6 is never used) and fit a straight line on the other four groups."""
    usable = [r for r in rows if r['equipment_id'] in FOLD_GROUPS]
    folds = []
    for g in FOLD_GROUPS:
        tr = [r for r in usable if r['equipment_id'] != g]; te = [r for r in usable if r['equipment_id'] == g]
        Xt, yt = _xy(tr, FEATURES); Xe, ye = _xy(te, FEATURES)
        folds.append(float(np.mean(np.abs(ye - _ols_predict(_ols(Xt, yt), Xe)))))
    return dict(folds=folds, mean=float(np.mean(folds)), spread=float(np.std(folds, ddof=1)))


def ridge_and_knn(training, validation, degree=3, alpha=1.0, k=3):
    """Ridge curve on load alone (polynomial features, then standardised) and k nearest neighbours on both inputs."""
    xt = np.array([r['load_pct'] for r in training], float); xv = np.array([r['load_pct'] for r in validation], float)
    yt = np.array([r['target'] for r in training], float); yv = np.array([r['target'] for r in validation], float)
    P = lambda x: np.column_stack([x ** d for d in range(1, degree + 1)])
    Pt, Pv = P(xt), P(xv); mu, sd = Pt.mean(axis=0), Pt.std(axis=0)
    Zt, Zv = (Pt - mu) / sd, (Pv - mu) / sd; ym = yt.mean()
    w = np.linalg.solve(Zt.T @ Zt + alpha * np.eye(Zt.shape[1]), Zt.T @ (yt - ym))
    ridge_mae = float(np.mean(np.abs(yv - (ym + Zv @ w))))
    Xt, _ = _xy(training, FEATURES); Xv, _ = _xy(validation, FEATURES); m, s = Xt.mean(axis=0), Xt.std(axis=0)
    Zt, Zv = (Xt - m) / s, (Xv - m) / s; pred = []
    for z in Zv:
        d = np.sqrt(((Zt - z) ** 2).sum(axis=1)); pred.append(yt[np.argsort(d, kind='stable')[:k]].mean())
    knn_mae = float(np.mean(np.abs(yv - np.array(pred))))
    return dict(ridge_mae=ridge_mae, knn_mae=knn_mae, better='ridge' if ridge_mae < knn_mae else 'knn')
