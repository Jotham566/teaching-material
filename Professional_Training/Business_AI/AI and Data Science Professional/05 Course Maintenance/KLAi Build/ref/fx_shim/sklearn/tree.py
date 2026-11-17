import numpy as np
from ._core import C, arr


def _depth(t):
    return 0 if t[0] == 'leaf' else 1 + max(_depth(t[3]), _depth(t[4]))


def _leaves(t):
    return 1 if t[0] == 'leaf' else _leaves(t[3]) + _leaves(t[4])


class DecisionTreeClassifier:
    def __init__(self, criterion='gini', max_depth=None, random_state=None):
        self.max_depth, self.random_state = max_depth, random_state

    def fit(self, X, y):
        self.feature_names_ = list(X.columns) if hasattr(X, 'columns') else None
        self.tree_ = C.fit_tree(arr(X), np.asarray(y), self.max_depth or 60, 0 if self.random_state is None else self.random_state)
        self.classes_ = np.array([0, 1])
        return self

    def predict_proba(self, X):
        p = C.tree_proba(self.tree_, arr(X))
        return np.column_stack([1 - p, p])

    def predict(self, X):
        return C.tree_predict(self.tree_, arr(X))

    def score(self, X, y):
        return float(np.mean(self.predict(X) == np.asarray(y)))

    def get_depth(self):
        return _depth(self.tree_)

    def get_n_leaves(self):
        return _leaves(self.tree_)


def export_text(tree, feature_names=None):
    names = feature_names or tree.feature_names_

    def walk(t, ind):
        if t[0] == 'leaf':
            return f'{ind}|--- class: {int(t[1] > 0.5)}\n'
        nm, thr = names[t[1]], t[2]
        return f'{ind}|--- {nm} <= {thr:.2f}\n' + walk(t[3], ind + '|   ') + f'{ind}|--- {nm} >  {thr:.2f}\n' + walk(t[4], ind + '|   ')
    return walk(tree.tree_, '')
