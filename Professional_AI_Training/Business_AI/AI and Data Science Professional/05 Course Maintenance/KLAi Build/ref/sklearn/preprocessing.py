import numpy as np
class StandardScaler:
    def fit(self, X, y=None): A = np.asarray(X, float); self.mean_, self.scale_ = A.mean(0), A.std(0); self.scale_[self.scale_ == 0] = 1; return self
    def transform(self, X): return (np.asarray(X, float) - self.mean_) / self.scale_
    def fit_transform(self, X, y=None): return self.fit(X).transform(X)


class PolynomialFeatures:
    """Powers of the inputs as scikit-learn orders them: for one input column and include_bias=False the columns are x, x**2, ..., x**degree.
    Only the one-input case and the interaction-free multi-input case are needed by the labs, so more than one input column raises an error."""
    def __init__(self, degree=2, include_bias=True): self.degree, self.include_bias = degree, include_bias
    def fit(self, X, y=None):
        if np.asarray(X).ndim == 2 and np.asarray(X).shape[1] != 1: raise NotImplementedError('stand-in supports one input column only')
        return self
    def transform(self, X):
        x = np.asarray(X, float).reshape(-1)
        cols = [x ** k for k in range(0 if self.include_bias else 1, self.degree + 1)]
        return np.column_stack(cols)
    def fit_transform(self, X, y=None): return self.fit(X).transform(X)
