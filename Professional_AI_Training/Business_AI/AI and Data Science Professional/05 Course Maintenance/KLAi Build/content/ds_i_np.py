"""Independent NumPy implementations used to compute the numbers on the Session 17 and 18 slides (author i).
They are written from the textbook definitions and do not use scikit-learn: CART trees (Gini for a 0/1 target equals squared error up to a factor),
bagging, a random forest, gradient boosting with log loss, logistic regression by Newton steps, permutation importance, k-means (k-means++ start), PCA by SVD, AUC.
scikit-learn's own results will be close but not identical for anything that uses random numbers."""
import numpy as np


# ------------------------------------------------------------------ AUC
def auc(y, s):
    y = np.asarray(y); s = np.asarray(s, float)
    order = np.argsort(s, kind='mergesort'); ranks = np.empty(len(s)); ss = s[order]
    i = 0; r = np.empty(len(s))
    while i < len(s):
        j = i
        while j + 1 < len(s) and ss[j + 1] == ss[i]:
            j += 1
        r[i:j + 1] = (i + j) / 2 + 1; i = j + 1
    ranks[order] = r
    pos = y == 1; n1 = pos.sum(); n0 = len(y) - n1
    return float((ranks[pos].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


# ------------------------------------------------------------------ one decision tree (CART)
class Tree:
    """Binary tree on numeric features. Split rule: maximise sl^2/nl + sr^2/nr (squared error reduction; for a 0/1 target this is the Gini rule)."""

    def __init__(self, max_depth=None, min_leaf=1, max_features=None, rng=None):
        self.max_depth, self.min_leaf, self.max_features, self.rng = max_depth, min_leaf, max_features, rng

    def fit(self, X, y):
        X = np.asarray(X, float); y = np.asarray(y, float)
        self.feat, self.thr, self.left, self.right, self.val = [], [], [], [], []
        self._grow(X, y, np.arange(len(y)), 0)
        self.feat, self.thr = np.array(self.feat), np.array(self.thr)
        self.left, self.right, self.val = np.array(self.left), np.array(self.right), np.array(self.val)
        return self

    def _new(self, v):
        self.feat.append(-1); self.thr.append(0.0); self.left.append(-1); self.right.append(-1); self.val.append(v)
        return len(self.val) - 1

    def _grow(self, X, y, idx, depth):
        me = self._new(float(y[idx].mean()))
        n = len(idx)
        if (self.max_depth is not None and depth >= self.max_depth) or n < 2 * self.min_leaf or n < 2:
            return me
        yi = y[idx]
        if yi.min() == yi.max():
            return me
        p = X.shape[1]
        cand = np.arange(p)
        if self.max_features and self.max_features < p:
            cand = self.rng.choice(p, self.max_features, replace=False)
        best, bf, bt = -np.inf, -1, 0.0
        tot = yi.sum()
        base = tot * tot / n
        for f in cand:
            v = X[idx, f]
            o = np.argsort(v, kind='stable'); vs = v[o]; cs = np.cumsum(yi[o])
            k = np.arange(1, n)             # left size
            ok = (vs[1:] > vs[:-1]) & (k >= self.min_leaf) & (n - k >= self.min_leaf)
            if not ok.any():
                continue
            sl = cs[:-1]; sr = tot - sl
            g = sl * sl / k + sr * sr / (n - k)
            g = np.where(ok, g, -np.inf)
            j = int(np.argmax(g))
            if g[j] > best + 1e-12:
                best, bf, bt = g[j], int(f), float((vs[j] + vs[j + 1]) / 2)
                if bt >= vs[j + 1]:   # as scikit-learn: if the midpoint rounds up to the upper value, use the lower value
                    bt = float(vs[j])
        if bf < 0 or best <= base + 1e-12:
            return me
        m = X[idx, bf] <= bt
        self.feat[me], self.thr[me] = bf, bt
        l = self._grow(X, y, idx[m], depth + 1); r = self._grow(X, y, idx[~m], depth + 1)
        self.left[me], self.right[me] = l, r
        return me

    def apply(self, X):
        X = np.asarray(X, float); node = np.zeros(len(X), int)
        while True:
            f = self.feat[node]; act = f >= 0
            if not act.any():
                return node
            go_left = X[np.arange(len(X)), np.where(act, f, 0)] <= self.thr[node]
            node = np.where(act, np.where(go_left, self.left[node], self.right[node]), node)

    def predict(self, X):
        return self.val[self.apply(X)]

    def n_leaves(self):
        return int((self.feat < 0).sum())

    def depth(self):
        d = np.zeros(len(self.val), int)
        for i in range(len(self.val)):
            if self.feat[i] >= 0:
                d[self.left[i]] = d[self.right[i]] = d[i] + 1
        return int(d.max())


# ------------------------------------------------------------------ bagging and random forest
class Forest:
    """Bootstrap aggregation of trees. max_features=None gives plain bagging; an integer gives a random forest."""

    def __init__(self, n_trees=100, max_depth=None, min_leaf=1, max_features=None, seed=42):
        self.n_trees, self.max_depth, self.min_leaf, self.max_features, self.seed = n_trees, max_depth, min_leaf, max_features, seed

    def fit(self, X, y):
        X = np.asarray(X, float); y = np.asarray(y, float); rng = np.random.default_rng(self.seed); self.trees = []; n = len(y)
        for _ in range(self.n_trees):
            b = rng.integers(0, n, n)
            self.trees.append(Tree(self.max_depth, self.min_leaf, self.max_features, rng).fit(X[b], y[b]))
        return self

    def predict_proba1(self, X, upto=None):
        ts = self.trees[:upto] if upto else self.trees
        return np.mean([t.predict(X) for t in ts], axis=0)


# ------------------------------------------------------------------ gradient boosting with log loss
class Boost:
    """Gradient boosting for a 0/1 target: start from the log-odds of the training share; each tree fits the residual y - p; leaf value is the Newton step."""

    def __init__(self, n_trees=100, lr=0.1, max_depth=3, min_leaf=1):
        self.n_trees, self.lr, self.max_depth, self.min_leaf = n_trees, lr, max_depth, min_leaf

    def fit(self, X, y):
        X = np.asarray(X, float); y = np.asarray(y, float)
        p0 = y.mean(); self.f0 = float(np.log(p0 / (1 - p0))); F = np.full(len(y), self.f0); self.trees = []
        for _ in range(self.n_trees):
            p = 1 / (1 + np.exp(-F)); r = y - p
            t = Tree(self.max_depth, self.min_leaf).fit(X, r)
            leaf = t.apply(X)
            for L in np.unique(leaf):
                m = leaf == L
                t.val[L] = r[m].sum() / max((p[m] * (1 - p[m])).sum(), 1e-12)
            F = F + self.lr * t.val[leaf]; self.trees.append(t)
        return self

    def decision(self, X, upto=None):
        X = np.asarray(X, float); F = np.full(len(X), self.f0)
        for t in (self.trees[:upto] if upto else self.trees):
            F = F + self.lr * t.predict(X)
        return F

    def predict_proba1(self, X, upto=None):
        return 1 / (1 + np.exp(-self.decision(X, upto)))


# ------------------------------------------------------------------ logistic regression (L2, C=1, intercept not penalised: scikit-learn's objective)
def logreg_fit(X, y, C=1.0, iters=100):
    X = np.asarray(X, float); y = np.asarray(y, float)
    A = np.column_stack([np.ones(len(X)), X]); th = np.zeros(A.shape[1]); pen = np.eye(A.shape[1]); pen[0, 0] = 0
    for _ in range(iters):
        p = 1 / (1 + np.exp(-(A @ th)))
        g = pen @ th + C * A.T @ (p - y); H = pen + C * (A.T * (p * (1 - p))) @ A
        step = np.linalg.solve(H, g); th -= step
        if np.max(np.abs(step)) < 1e-12:
            break
    return float(th[0]), th[1:]


def logreg_p(b, w, X):
    return 1 / (1 + np.exp(-(b + np.asarray(X, float) @ w)))


# ------------------------------------------------------------------ permutation importance
def perm_importance(score_fn, X, y, repeats=10, seed=42):
    """score_fn(X) -> predicted score; returns (mean drop in AUC, std) per column."""
    rng = np.random.default_rng(seed); X = np.asarray(X, float); base = auc(y, score_fn(X)); drops = np.zeros((X.shape[1], repeats))
    for j in range(X.shape[1]):
        for r in range(repeats):
            Xp = X.copy(); Xp[:, j] = rng.permutation(Xp[:, j]); drops[j, r] = base - auc(y, score_fn(Xp))
    return drops.mean(1), drops.std(1)


# ------------------------------------------------------------------ k-means (Lloyd's algorithm with a k-means++ start), PCA and an isolation forest
def kmeans_once(X, k, rng, iters=300):
    X = np.asarray(X, float)
    C = [X[rng.integers(len(X))]]
    for _ in range(k - 1):
        d = np.min(((X[:, None, :] - np.array(C)[None]) ** 2).sum(2), axis=1)
        C.append(X[rng.choice(len(X), p=d / d.sum())])
    C = np.array(C); lab = None
    for it in range(iters):
        nl = ((X[:, None, :] - C[None]) ** 2).sum(2).argmin(1)
        if lab is not None and (nl == lab).all():
            break
        lab = nl
        C = np.array([X[lab == j].mean(0) if (lab == j).any() else C[j] for j in range(k)])
    return float(((X - C[lab]) ** 2).sum()), lab, C, it


def kmeans(X, k, seed=42, n_init=10):
    """The best of n_init starts (lowest inertia = within-cluster sum of squares)."""
    best = None
    for s in range(n_init):
        r = kmeans_once(X, k, np.random.default_rng(seed * 1000 + s))
        if best is None or r[0] < best[0]:
            best = r
    return best


def pca(X):
    """Principal components of the columns of X (centred first): eigenvalues, explained variance ratio, components (rows) and the projected scores."""
    Xc = np.asarray(X, float) - np.mean(X, axis=0)
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    ev = S ** 2 / (len(Xc) - 1)
    return ev, ev / ev.sum(), Vt, Xc @ Vt.T


def _c(n):
    return 2 * (np.log(n - 1) + 0.5772156649) - 2 * (n - 1) / n if n > 2 else (1.0 if n == 2 else 0.0)


def isolation_scores(X, n_trees=100, max_samples=256, seed=42):
    """Isolation forest: random cuts isolate an odd row in few steps. Returns the anomaly score in (0, 1) (higher is more odd)."""
    X = np.asarray(X, float); rng = np.random.default_rng(seed); n = len(X); m = min(max_samples, n); limit = int(np.ceil(np.log2(m)))
    depth = np.zeros(n)

    def path(idx, rows, d, out):
        if d >= limit or len(rows) <= 1:
            out[idx] = d + _c(len(rows)); return
        f = rng.integers(X.shape[1]); v = X[rows, f]; lo, hi = v.min(), v.max()
        if lo == hi:
            out[idx] = d + _c(len(rows)); return
        cut = rng.uniform(lo, hi)
        # idx here are positions in the full data of the rows that reached this node; rows are those of the training sample
        go = X[idx, f] < cut
        path(idx[go], rows[X[rows, f] < cut], d + 1, out); path(idx[~go], rows[X[rows, f] >= cut], d + 1, out)
    for _ in range(n_trees):
        sample = rng.choice(n, m, replace=False); out = np.zeros(n)
        path(np.arange(n), sample, 0, out); depth += out
    return 2 ** (-(depth / n_trees) / _c(m))
