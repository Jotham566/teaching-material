"""A line-by-line NumPy/Python replica of scikit-learn's CART (BestSplitter + DepthFirstTreeBuilder) for
DecisionTreeRegressor (squared error) and DecisionTreeClassifier (gini) with max_features=None.

Why it exists: the sandbox has no scikit-learn, and a tree that picks a different split on a tie gives a different
validation score. This copies the details that decide ties: float32 inputs, the random draw of the feature order from
RandomState(seed), the xorshift generator, strictly-greater improvement, midpoint thresholds, the two ways the
criterion accumulates the left sum, and depth-first left-first processing. Verified against real scikit-learn 1.9.1
output on the Week 8 and Week 10 slides (see verify_week_slides_20261030.py). Equal feature values are sorted stably,
which scikit-learn does not promise, so exact float ties among repeated values are the one remaining risk.
"""
import numpy as np

EPS = float(np.finfo("double").eps); FEATURE_THRESHOLD = 1e-7; RAND_R_MAX = 0x7FFFFFFF


class _Rng:
    def __init__(self, seed): self.s = int(seed) & 0xFFFFFFFF
    def rand_int(self, low, high):
        if self.s == 0: self.s = 1
        s = self.s; s ^= (s << 13) & 0xFFFFFFFF; s ^= s >> 17; s ^= (s << 5) & 0xFFFFFFFF; self.s = s
        return low + (s % (RAND_R_MAX + 1)) % (high - low)


class _Mse:
    def __init__(self, y): self.y = y
    def node_reset(self, samples, start, end):
        self.start, self.end = start, end; st = 0.0; sq = 0.0
        for p in range(start, end):
            v = float(self.y[samples[p]]); st += v; sq += v * v
        self.sum_total, self.sq_total, self.n = st, sq, float(end - start)
    def impurity(self): return self.sq_total / self.n - (self.sum_total / self.n) ** 2
    def value(self): return self.sum_total / self.n
    def reset(self): self.pos = self.start; self.sl = 0.0; self.sr = self.sum_total; self.nl = 0.0; self.nr = self.n
    def reverse_reset(self): self.pos = self.end; self.sl = self.sum_total; self.sr = 0.0; self.nl = self.n; self.nr = 0.0
    def update(self, samples, new_pos):
        if (new_pos - self.pos) <= (self.end - new_pos):
            for p in range(self.pos, new_pos): self.sl += float(self.y[samples[p]]); self.nl += 1.0
        else:
            self.reverse_reset()
            for p in range(self.end - 1, new_pos - 1, -1): self.sl -= float(self.y[samples[p]]); self.nl -= 1.0
        self.nr = self.n - self.nl; self.sr = self.sum_total - self.sl; self.pos = new_pos
    def proxy(self): return (self.sl * self.sl) / self.nl + (self.sr * self.sr) / self.nr


class _Gini:
    def __init__(self, y, k): self.y = y; self.k = k
    def node_reset(self, samples, start, end):
        self.start, self.end = start, end; c = [0.0] * self.k
        for p in range(start, end): c[self.y[samples[p]]] += 1.0
        self.total = c; self.n = float(end - start)
    @staticmethod
    def _g(c, n):
        sq = 0.0
        for v in c: sq += v * v
        return 1.0 - sq / (n * n)
    def impurity(self): return self._g(self.total, self.n)
    def value(self): return self.total[1] / self.n if self.k == 2 else None
    def reset(self): self.pos = self.start; self.cl = [0.0] * self.k; self.cr = list(self.total); self.nl = 0.0; self.nr = self.n
    def reverse_reset(self): self.pos = self.end; self.cl = list(self.total); self.cr = [0.0] * self.k; self.nl = self.n; self.nr = 0.0
    def update(self, samples, new_pos):
        if (new_pos - self.pos) <= (self.end - new_pos):
            for p in range(self.pos, new_pos): self.cl[self.y[samples[p]]] += 1.0; self.nl += 1.0
        else:
            self.reverse_reset()
            for p in range(self.end - 1, new_pos - 1, -1): self.cl[self.y[samples[p]]] -= 1.0; self.nl -= 1.0
        self.nr = self.n - self.nl; self.cr = [t - l for t, l in zip(self.total, self.cl)]; self.pos = new_pos
    def proxy(self): return -self.nr * self._g(self.cr, self.nr) - self.nl * self._g(self.cl, self.nl)


def fit(X, y, max_depth, kind="reg", seed=0):
    """Return a tree in the ("split", j, thr, left, right) / ("leaf", value) format used by week_reference_numpy."""
    X = np.asarray(X, float).astype(np.float32); n, nf = X.shape
    seed = int(np.random.RandomState(seed).randint(0, RAND_R_MAX)); rng = _Rng(seed)
    if kind == "reg": crit = _Mse(np.asarray(y, float))
    else:
        y = np.asarray(y, int); crit = _Gini(y, int(y.max()) + 1)
    samples = np.arange(n); features = list(range(nf)); const = list(range(nf))   # constant_features array

    def node_split(start, end, n_known):
        nonlocal features
        best = None; best_prox = -np.inf
        n_found = 0; n_drawn = 0; n_total = n_known; f_i = nf; visited = 0
        maxf = nf
        while f_i > n_total and (visited < maxf or visited <= n_found + n_drawn):
            visited += 1
            f_j = rng.rand_int(n_drawn, f_i - n_found)
            if f_j < n_known:
                features[n_drawn], features[f_j] = features[f_j], features[n_drawn]; n_drawn += 1; continue
            f_j += n_found; feat = features[f_j]
            vals = X[samples[start:end], feat]; order = np.argsort(vals, kind="stable")
            samples[start:end] = samples[start:end][order]; fv = vals[order].astype(np.float64)
            if fv[-1] <= fv[0] + FEATURE_THRESHOLD:
                features[f_j], features[n_total] = features[n_total], features[f_j]; n_found += 1; n_total += 1; continue
            f_i -= 1; features[f_i], features[f_j] = features[f_j], features[f_i]
            crit.reset(); p = start; m = end - start
            while p < end:
                while p + 1 < end and fv[p + 1 - start] <= fv[p - start] + FEATURE_THRESHOLD: p += 1
                p += 1
                if p < end:
                    crit.update(samples, p); prox = crit.proxy()
                    if prox > best_prox:
                        best_prox = prox; thr = fv[p - 1 - start] / 2.0 + fv[p - start] / 2.0
                        if thr == fv[p - start] or thr in (np.inf, -np.inf): thr = fv[p - 1 - start]
                        best = (feat, thr, p)
        # keep the invariant for constant features
        for i in range(n_known): features[i] = const[i]
        for i in range(n_found): const[n_known + i] = features[n_known + i]
        return best, n_total

    def build():
        stack = [(0, n, 0, 0, None)]; nodes = []   # (start,end,depth,n_const, slot)
        root = [None]; slots = {}
        stack = [(0, n, 0, 0, root, 0)]
        while stack:
            start, end, depth, n_const, holder, idx = stack.pop()
            crit.node_reset(samples, start, end)
            leaf = depth >= max_depth or (end - start) < 2
            leaf = leaf or crit.impurity() <= EPS
            best = None
            if not leaf:
                best, n_const = node_split(start, end, n_const)
                leaf = best is None
            if leaf:
                holder[idx] = ("leaf", crit.value()); continue
            feat, thr, pos = best
            # partition samples by the winning feature
            p = start; pe = end
            while p < pe:
                if float(X[samples[p], feat]) <= thr: p += 1
                else: pe -= 1; samples[p], samples[pe] = samples[pe], samples[p]
            node = ["split", feat, thr, None, None]; holder[idx] = node
            stack.append((p, end, depth + 1, n_const, node, 4)); stack.append((start, p, depth + 1, n_const, node, 3))
        return root[0]

    def freeze(t): return t if t is None or t[0] == "leaf" else ("split", t[1], t[2], freeze(t[3]), freeze(t[4]))
    return freeze(build())


def predict(tree, X):
    X = np.asarray(X, float).astype(np.float32); out = np.empty(len(X))
    for r, x in enumerate(X):
        node = tree
        while node[0] == "split": node = node[3] if float(x[node[1]]) <= node[2] else node[4]
        out[r] = node[1]
    return out
