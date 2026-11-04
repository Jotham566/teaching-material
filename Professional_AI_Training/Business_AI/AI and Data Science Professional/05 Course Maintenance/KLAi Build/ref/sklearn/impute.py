import numpy as np
class SimpleImputer:
    def __init__(self, strategy='mean'): self.strategy = strategy
    def fit(self, X, y=None):
        A = np.asarray(X, float); self.statistics_ = np.nanmedian(A, axis=0) if self.strategy == 'median' else np.nanmean(A, axis=0); return self
    def transform(self, X):
        A = np.array(X, float); idx = np.where(np.isnan(A)); A[idx] = np.take(self.statistics_, idx[1]); return A
    def fit_transform(self, X, y=None): return self.fit(X).transform(X)
