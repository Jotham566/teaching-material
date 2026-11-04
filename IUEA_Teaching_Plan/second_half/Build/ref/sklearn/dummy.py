import numpy as np
class DummyRegressor:
    def __init__(self, strategy='mean'): self.strategy = strategy
    def fit(self, X, y): self.c_ = float(np.mean(y)) if self.strategy == 'mean' else float(np.median(y)); return self
    def predict(self, X): return np.full(len(X), self.c_)
