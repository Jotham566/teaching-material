import numpy as np
from ._core import H, arr, sigmoid


class LogisticRegression:
    def __init__(self, penalty='l2', C=1.0, class_weight=None, max_iter=100, random_state=None):
        self.C, self.class_weight, self.max_iter = C, class_weight, max_iter

    def fit(self, X, y, sample_weight=None):
        y = np.asarray(y).astype(int)
        s = None if sample_weight is None else np.asarray(sample_weight, float)
        if self.class_weight == 'balanced':
            cnt = np.bincount(y)
            w = (len(y) / (len(cnt) * cnt))[y]
            s = w if s is None else s * w
        b, w_ = H.logreg_fit(arr(X), y, C=self.C, sample_weight=s)
        self.intercept_, self.coef_, self.classes_ = np.array([b]), np.array([w_]), np.array([0, 1])
        return self

    def decision_function(self, X):
        return self.intercept_[0] + arr(X) @ self.coef_[0]

    def predict_proba(self, X):
        p = sigmoid(self.decision_function(X))
        return np.column_stack([1 - p, p])

    def predict(self, X):
        return (self.decision_function(X) > 0).astype(int)

    def score(self, X, y):
        return float(np.mean(self.predict(X) == np.asarray(y)))
