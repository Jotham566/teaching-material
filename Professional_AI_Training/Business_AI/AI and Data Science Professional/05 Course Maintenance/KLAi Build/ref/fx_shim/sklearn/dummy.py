import numpy as np


class DummyClassifier:
    def __init__(self, strategy='prior', constant=None, random_state=None):
        self.strategy, self.constant = strategy, constant

    def fit(self, X, y):
        v, c = np.unique(np.asarray(y), return_counts=True)
        self.c_ = self.constant if self.strategy == 'constant' else v[np.argmax(c)]
        return self

    def predict(self, X):
        return np.full(len(X), self.c_)

    def predict_proba(self, X):
        p = np.full(len(X), float(self.c_))
        return np.column_stack([1 - p, p])

    def score(self, X, y):
        return float(np.mean(self.predict(X) == np.asarray(y)))
