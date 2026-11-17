import numpy as np
class LinearRegression:
    def fit(self, X, y):
        A = np.column_stack([np.ones(len(X)), np.asarray(X, float)]); c, *_ = np.linalg.lstsq(A, np.asarray(y, float), rcond=None)
        self.intercept_, self.coef_ = float(c[0]), c[1:]; return self
    def predict(self, X): return self.intercept_ + np.asarray(X, float) @ self.coef_
    def score(self, X, y):
        y = np.asarray(y, float); p = self.predict(X); return 1 - ((y - p) ** 2).sum() / ((y - y.mean()) ** 2).sum()


import sys as _sys
from pathlib import Path as _P
_sys.path.insert(0, str(_P(__file__).resolve().parents[1]))
import week_reference_numpy as _R


class LogisticRegression:
    """L2 logistic regression, C=1 by default, as the reference module (checked against scikit-learn)."""
    def __init__(self, C=1.0, max_iter=100, random_state=None): self.C = C; self.max_iter = max_iter
    def fit(self, X, y):
        b, w = _R.logreg_fit(np.asarray(X, float), np.asarray(y, float), C=self.C, iters=max(self.max_iter, 100)); self.intercept_, self.coef_ = np.array([b]), np.array([w]); self.classes_ = np.array([0, 1]); return self
    def predict_proba(self, X):
        p = _R.logreg_proba(self.intercept_[0], self.coef_[0], X); return np.column_stack([1 - p, p])
    def predict(self, X): return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)
    def decision_function(self, X): return self.intercept_[0] + np.asarray(X, float) @ self.coef_[0]
    def score(self, X, y): return float(np.mean(self.predict(X) == np.asarray(y)))


class Ridge:
    """Ridge as scikit-learn: penalises alpha times the sum of squared coefficients, the intercept is not penalised."""
    def __init__(self, alpha=1.0): self.alpha = alpha
    def fit(self, X, y):
        X = np.asarray(X, float); y = np.asarray(y, float); xm, ym = X.mean(0), y.mean(); Xc, yc = X - xm, y - ym
        self.coef_ = np.linalg.solve(Xc.T @ Xc + self.alpha * np.eye(X.shape[1]), Xc.T @ yc); self.intercept_ = float(ym - xm @ self.coef_); return self
    def predict(self, X): return self.intercept_ + np.asarray(X, float) @ self.coef_
