import numpy as np
class KFold:
    def __init__(self, n_splits=5, shuffle=False, random_state=None): self.n_splits, self.shuffle, self.random_state = n_splits, shuffle, random_state
    def split(self, X, y=None, groups=None):
        n = len(X); idx = np.arange(n)
        if self.shuffle: np.random.RandomState(self.random_state).shuffle(idx)
        sizes = np.full(self.n_splits, n // self.n_splits); sizes[: n % self.n_splits] += 1; cur = 0
        for s in sizes:
            te = idx[cur:cur + s]; tr = np.r_[idx[:cur], idx[cur + s:]]; yield tr, te; cur += s
class GroupKFold:
    def __init__(self, n_splits=5): self.n_splits = n_splits
    def split(self, X, y=None, groups=None):
        g = np.asarray(groups); u, inv = np.unique(g, return_inverse=True); counts = np.bincount(inv); order = np.argsort(-counts, kind='stable'); load = np.zeros(self.n_splits); asg = {}
        for k in order: f = int(np.argmin(load)); asg[k] = f; load[f] += counts[k]
        fold = np.array([asg[k] for k in inv])
        for f in range(self.n_splits): yield np.where(fold != f)[0], np.where(fold == f)[0]
def _take(X, i): return X.iloc[i] if hasattr(X, 'iloc') else np.asarray(X)[i]
def cross_val_score(model, X, y, cv=5, scoring=None, groups=None):
    import copy, sys
    from sklearn import metrics as M
    splitter = KFold(cv) if isinstance(cv, int) else cv; out = []
    for tr, te in splitter.split(X, y, groups):
        m = copy.deepcopy(model).fit(_take(X, tr), _take(y, tr)); p = m.predict(_take(X, te)); yt = _take(y, te)
        if scoring == 'neg_mean_absolute_error': out.append(-M.mean_absolute_error(yt, p))
        elif scoring == 'accuracy': out.append(M.accuracy_score(yt, p))
        else: out.append(M.r2_score(yt, p))
    return np.array(out)
def train_test_split(*arrays, test_size=0.25, random_state=None, shuffle=True):
    n = len(arrays[0]); idx = np.arange(n)
    if shuffle: np.random.RandomState(random_state).shuffle(idx)
    nt = int(np.ceil(test_size * n)); te, tr = idx[:nt], idx[nt:]
    out = []
    for a in arrays: out += [_take(a, tr), _take(a, te)]
    return out
