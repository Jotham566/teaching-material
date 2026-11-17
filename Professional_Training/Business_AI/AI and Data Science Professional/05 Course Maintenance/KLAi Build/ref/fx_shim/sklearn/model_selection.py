import copy
import numpy as np
import pandas as pd
from ._core import C, take, arr


def train_test_split(*arrays, test_size=0.25, stratify=None, random_state=None, shuffle=True):
    n = len(arrays[0])
    y = np.zeros(n, int) if stratify is None else np.asarray(stratify)
    assert test_size == 0.25 and random_state == 42, 'the shim only knows the course split'
    tr, te = C.split_indices(y, stratify=stratify is not None)
    out = []
    for a in arrays:
        out += [take(a, tr), take(a, te)]
    return out


class StratifiedKFold:
    def __init__(self, n_splits=5, shuffle=False, random_state=None):
        assert not shuffle
        self.n_splits = n_splits

    def split(self, X, y=None, groups=None):
        yield from C.cv_splits(np.asarray(y), self.n_splits)


def _splitter(cv, y):
    return StratifiedKFold(cv) if isinstance(cv, int) else cv


def _score(name, model, Xt, yt):
    if name == 'roc_auc':
        return C.auc_rank(yt, model.predict_proba(Xt)[:, 1])
    if name in (None, 'accuracy'):
        return float(np.mean(model.predict(Xt) == np.asarray(yt)))
    raise ValueError(name)


def cross_val_score(model, X, y, cv=5, scoring=None):
    out = []
    for tr, te in _splitter(cv, y).split(X, y):
        m = copy.deepcopy(model).fit(take(X, tr), take(y, tr))
        out.append(_score(scoring, m, take(X, te), take(y, te)))
    return np.array(out)


def cross_val_predict(model, X, y, cv=5, method='predict'):
    res = None
    for tr, te in _splitter(cv, y).split(X, y):
        m = copy.deepcopy(model).fit(take(X, tr), take(y, tr))
        p = getattr(m, method)(take(X, te))
        if res is None:
            res = np.zeros((len(y),) + p.shape[1:])
        res[te] = p
    return res
