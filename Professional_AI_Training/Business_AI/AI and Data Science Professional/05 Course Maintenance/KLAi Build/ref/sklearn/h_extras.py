"""Extra pieces of scikit-learn for the Session 15 and 16 labs (author h). A NEW file: it changes none of the existing stand-in files.
Call install() once; it adds to the stand-in modules the classes and functions the two labs use and the stand-in lacks:
LogisticRegression with class_weight, DecisionTreeClassifier with predict_proba, export_text, get_depth and get_n_leaves, DummyClassifier,
StratifiedKFold, cross_val_score that scores classifiers (accuracy, f1, precision, recall, roc_auc) and uses stratified folds for a classifier as scikit-learn does,
roc_auc_score by ranks, precision_recall_curve and classification-style helpers. Behaviour follows the real library (same objective, same fold assignment, same text format).
It is only for checking the notebooks here; learners use the real scikit-learn."""
import copy
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sk_tree_replica as T  # noqa: E402


def _sig(z):
    return 1 / (1 + np.exp(-z))


class LogisticRegression:
    """L2-penalised logistic regression, objective 0.5*||w||^2 + C*sum(s_i*logloss_i), intercept not penalised, solved by Newton steps (the optimum is the one lbfgs finds)."""

    def __init__(self, penalty='l2', C=1.0, class_weight=None, random_state=None, solver='lbfgs', max_iter=100):
        self.C, self.class_weight, self.max_iter, self.random_state = C, class_weight, max_iter, random_state

    def get_params(self, deep=True):
        return dict(C=self.C, class_weight=self.class_weight, max_iter=self.max_iter, random_state=self.random_state)

    def fit(self, X, y, sample_weight=None):
        X = np.asarray(X, float)
        y = np.asarray(y).astype(int)
        s = np.ones(len(y)) if sample_weight is None else np.asarray(sample_weight, float)
        if self.class_weight == 'balanced':
            cnt = np.bincount(y)
            s = s * (len(y) / (len(cnt) * cnt))[y]
        elif isinstance(self.class_weight, dict):
            s = s * np.array([self.class_weight[v] for v in y])
        A = np.column_stack([np.ones(len(X)), X])
        th = np.zeros(A.shape[1])
        pen = np.eye(A.shape[1])
        pen[0, 0] = 0
        for _ in range(100):
            p = _sig(A @ th)
            g = pen @ th + self.C * A.T @ (s * (p - y))
            H = pen + self.C * (A.T * (s * p * (1 - p))) @ A
            step = np.linalg.solve(H, g)
            th -= step
            if np.max(np.abs(step)) < 1e-10:
                break
        self.intercept_, self.coef_, self.classes_ = np.array([th[0]]), np.array([th[1:]]), np.array([0, 1])
        return self

    def decision_function(self, X):
        return self.intercept_[0] + np.asarray(X, float) @ self.coef_[0]

    def predict_proba(self, X):
        p = _sig(self.decision_function(X))
        return np.column_stack([1 - p, p])

    def predict(self, X):
        return (self.decision_function(X) > 0).astype(int)

    def score(self, X, y):
        return float(np.mean(self.predict(X) == np.asarray(y)))


def _walk(t, fn):
    if t[0] == 'leaf':
        return fn(t)
    return [t] + _walk(t[3], fn) + _walk(t[4], fn)


class DecisionTreeClassifier:
    def __init__(self, criterion='gini', max_depth=None, random_state=None):
        self.max_depth, self.random_state = max_depth, random_state

    def get_params(self, deep=True):
        return dict(max_depth=self.max_depth, random_state=self.random_state)

    def fit(self, X, y):
        self.n_features_in_ = np.asarray(X).shape[1]
        self.feature_names_in_ = np.array(list(X.columns)) if hasattr(X, 'columns') else None
        self.t_ = T.fit(np.asarray(X, float), np.asarray(y).astype(int), self.max_depth or 99, 'clf', self.random_state or 0)
        self.classes_ = np.array([0, 1])
        return self

    def predict_proba(self, X):
        p = np.asarray(T.predict(self.t_, np.asarray(X, float)))
        return np.column_stack([1 - p, p])

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] > 0.5).astype(int)

    def score(self, X, y):
        return float(np.mean(self.predict(X) == np.asarray(y)))

    def _depth(self, t):
        return 0 if t[0] == 'leaf' else 1 + max(self._depth(t[3]), self._depth(t[4]))

    def get_depth(self):
        return self._depth(self.t_)

    def _leaves(self, t):
        return 1 if t[0] == 'leaf' else self._leaves(t[3]) + self._leaves(t[4])

    def get_n_leaves(self):
        return self._leaves(self.t_)


def export_text(tree, feature_names=None, decimals=2, **_):
    names = list(feature_names) if feature_names is not None else [f'feature_{i}' for i in range(tree.n_features_in_)]
    out = []

    def rec(t, depth):
        ind = '|   ' * depth
        if t[0] == 'leaf':
            out.append(f'{ind}|--- class: {int(t[1] > 0.5)}')
            return
        out.append(f'{ind}|--- {names[t[1]]} <= {t[2]:.{decimals}f}')
        rec(t[3], depth + 1)
        out.append(f'{ind}|--- {names[t[1]]} >  {t[2]:.{decimals}f}')
        rec(t[4], depth + 1)
    rec(tree.t_, 0)
    return '\n'.join(out) + '\n'


class DummyClassifier:
    def __init__(self, strategy='prior', random_state=None, constant=None):
        self.strategy, self.constant = strategy, constant

    def fit(self, X, y):
        y = np.asarray(y).astype(int)
        self.class_prior_ = np.bincount(y) / len(y)
        self.classes_ = np.arange(len(self.class_prior_))
        self.c_ = int(np.argmax(self.class_prior_)) if self.strategy in ('most_frequent', 'prior') else int(self.constant)
        return self

    def predict(self, X):
        return np.full(len(X), self.c_)

    def predict_proba(self, X):
        return np.tile(self.class_prior_ if self.strategy == 'prior' else np.eye(len(self.class_prior_))[self.c_], (len(X), 1))

    def score(self, X, y):
        return float(np.mean(self.predict(X) == np.asarray(y)))


class StratifiedKFold:
    """Same assignment as scikit-learn: with shuffle=False the rows of each class are dealt to the folds in order, in blocks."""

    def __init__(self, n_splits=5, shuffle=False, random_state=None):
        self.n_splits, self.shuffle, self.random_state = n_splits, shuffle, random_state

    def split(self, X, y, groups=None):
        y = np.asarray(y)
        classes, yenc = np.unique(y, return_inverse=True)
        k = self.n_splits
        if self.shuffle:
            rng = np.random.RandomState(self.random_state)
            fold = np.empty(len(y), int)
            for c in range(len(classes)):
                idx = np.where(yenc == c)[0]
                rng.shuffle(idx)
                fold[idx] = np.arange(len(idx)) % k
        else:
            order = np.sort(yenc)
            alloc = np.array([np.bincount(order[i::k], minlength=len(classes)) for i in range(k)])
            fold = np.empty(len(y), int)
            for c in range(len(classes)):
                fold[yenc == c] = np.arange(k).repeat(alloc[:, c])
        for f in range(k):
            yield np.where(fold != f)[0], np.where(fold == f)[0]


def roc_auc_score(a, s):
    a = np.asarray(a).astype(int)
    s = np.asarray(s, float)
    order = np.argsort(s, kind='mergesort')
    ss = s[order]
    ranks = np.empty(len(s))
    i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and ss[j + 1] == ss[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2 + 1
        i = j + 1
    npos, nneg = (a == 1).sum(), (a == 0).sum()
    return float((ranks[a == 1].sum() - npos * (npos + 1) / 2) / (npos * nneg))


def precision_recall_curve(a, s):
    a = np.asarray(a).astype(int)
    s = np.asarray(s, float)
    ths = np.unique(s)
    P = (a == 1).sum()
    prec = np.array([((s >= t) & (a == 1)).sum() / (s >= t).sum() for t in ths])
    rec = np.array([((s >= t) & (a == 1)).sum() / P for t in ths])
    return np.r_[prec, 1.0], np.r_[rec, 0.0], ths


def cross_val_score(model, X, y, cv=5, scoring=None, groups=None):
    from sklearn import metrics as M
    splitter = StratifiedKFold(cv) if isinstance(cv, int) and set(np.unique(np.asarray(y))) <= {0, 1} else cv
    if isinstance(splitter, int):
        from sklearn.model_selection import KFold
        splitter = KFold(splitter)
    take = lambda A, i: A.iloc[i] if hasattr(A, 'iloc') else np.asarray(A)[i]
    out = []
    for tr, te in splitter.split(X, y):
        m = copy.deepcopy(model).fit(take(X, tr), take(y, tr))
        yt = take(y, te)
        if scoring == 'roc_auc':
            out.append(roc_auc_score(yt, m.predict_proba(take(X, te))[:, 1]))
            continue
        p = m.predict(take(X, te))
        f = {'accuracy': M.accuracy_score, 'f1': M.f1_score, 'precision': M.precision_score, 'recall': M.recall_score, 'neg_mean_absolute_error': lambda a, b: -M.mean_absolute_error(a, b),
             None: M.accuracy_score}.get(scoring)
        out.append(f(yt, p) if f else M.r2_score(yt, p))
    return np.array(out)


def install():
    import sklearn.dummy as dummy
    import sklearn.linear_model as lm
    import sklearn.metrics as me
    import sklearn.model_selection as ms
    import sklearn.tree as tr
    lm.LogisticRegression = LogisticRegression
    tr.DecisionTreeClassifier = DecisionTreeClassifier
    tr.export_text = export_text
    dummy.DummyClassifier = DummyClassifier
    ms.StratifiedKFold = StratifiedKFold
    ms.cross_val_score = cross_val_score
    me.roc_auc_score = roc_auc_score
    me.precision_recall_curve = precision_recall_curve
