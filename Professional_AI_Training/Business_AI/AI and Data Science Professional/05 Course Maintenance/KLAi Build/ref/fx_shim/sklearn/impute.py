import numpy as np
from ._core import arr


class SimpleImputer:
    def __init__(self, strategy='mean'):
        self.strategy = strategy

    def fit(self, X, y=None):
        A = arr(X)
        self.statistics_ = np.nanmedian(A, axis=0) if self.strategy == 'median' else np.nanmean(A, axis=0)
        return self

    def transform(self, X):
        A = arr(X).copy()
        i, j = np.where(np.isnan(A))
        A[i, j] = self.statistics_[j]
        return A

    def fit_transform(self, X, y=None):
        return self.fit(X).transform(X)
