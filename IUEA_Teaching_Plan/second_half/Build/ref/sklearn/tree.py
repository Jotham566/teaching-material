import sys, numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sk_tree_replica as T
class DecisionTreeRegressor:
    def __init__(self, max_depth=None, random_state=None): self.max_depth, self.random_state = max_depth, random_state
    def fit(self, X, y): self.t_ = T.fit(np.asarray(X, float), np.asarray(y, float), self.max_depth or 99, 'reg', self.random_state or 0); return self
    def predict(self, X): return np.asarray(T.predict(self.t_, np.asarray(X, float)))
class DecisionTreeClassifier:
    def __init__(self, max_depth=None, random_state=None): self.max_depth, self.random_state = max_depth, random_state
    def fit(self, X, y): self.t_ = T.fit(np.asarray(X, float), np.asarray(y, float), self.max_depth or 99, 'clf', self.random_state or 0); return self
    def predict(self, X): return (np.asarray(T.predict(self.t_, np.asarray(X, float))) >= 0.5).astype(int)
