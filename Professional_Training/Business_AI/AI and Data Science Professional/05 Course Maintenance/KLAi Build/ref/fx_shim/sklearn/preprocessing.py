import numpy as np
from ._core import arr


class StandardScaler:
    def fit(self, X, y=None):
        A = arr(X)
        self.mean_, sd = A.mean(0), A.std(0)
        self.scale_ = np.where(sd == 0, 1.0, sd)
        return self

    def transform(self, X):
        return (arr(X) - self.mean_) / self.scale_

    def fit_transform(self, X, y=None):
        return self.fit(X).transform(X)
