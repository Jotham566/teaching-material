"""loans_canon: the ONE shared preparation, split, models and headline numbers for the Nile Microfinance loans in Sessions 14 to 17, 20, 23 and 24.

Imports: numpy and pandas only. From any content file:  from loans_canon import prepare, split, facts, ...
Recipe in words (see also LOANS_RECIPE.md in the Build folder):
  8,000 rows; the two impossible ages (0 and 199) replaced by the median of the valid ages (36); income_missing flag; blank income replaced by the median income;
  instalment_to_income = loan_amount_ugx * 1.15 / term_months / monthly_income_ugx;  12 numeric FEATURES (Session 14);  15 indicator columns (gender 2, occupation 7, loan_purpose 6);
  split = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)  ->  6,000 train / 2,000 test.

ILLUSTRATIVE ASSUMPTION: the factor 1.15 is NOT in the data. It stands for "the borrower repays 15 percent more than the loan amount over the term"
(interest and fees). loans.csv has no interest rate. Say so on any slide that shows instalment_to_income.

HOW FAITHFUL ARE THE REPLICAS (no scikit-learn in the build sandbox; checked 4 Nov 2026)
  split(), stratify=True    Copy of the algorithm of sklearn.model_selection.StratifiedShuffleSplit._iter_indices and _approximate_mode (sklearn 1.x), written from memory of the source,
                            using numpy's own RandomState(42), so the random stream is the real one. NOT checked against a real scikit-learn run here. What was checked: the sizes
                            (6,000 / 2,000), the class counts (753 / 251), that the draws are a valid partition, and that EVERY headline number (test confusion counts at 0.5, 0.3, 0.2,
                            0.15, 0.1, AUC 0.756, tree 41 / 15 / 210, cost 133.1 M at 0.08, leaky 0.996) equals the independent replica written by the reviewer of Sessions 9 to 16
                            (Review_S09-S16.md section 1.3), which makes a wrong row draw very unlikely but is still not a real-library run. If the real library gives different test rows, this module is NOT bit for bit: run the one-line check in LOANS_RECIPE.md
                            (X_test.index[:10] and the sum of X_test.index must equal SPLIT_CHECK below) and recompute every number.
  split(stratify=False)     Copy of ShuffleSplit: rng.permutation(n); first ceil(0.25 n) rows are the test rows, the next floor(0.75 n) the train rows. Simple, high confidence.
  ScaledLogReg              StandardScaler (population standard deviation, ddof=0) then L2 logistic regression C=1.0, intercept not penalised, solved to the exact optimum by Newton steps.
                            Real lbfgs stops when the largest gradient component of the AVERAGED loss is below 1e-4, so its coefficients can differ from the exact optimum in the 3rd or 4th
                            decimal; AUC differs by about 0.0005 or less and a confusion count at a threshold can move by a few loans. Checked here: gradient at the optimum is about 1e-11.
  auc_rank / auc_trapezoid  Two independent methods, agree to 1e-12 (ties count half in both).
  stratified_kfold          Copy of StratifiedKFold._make_test_folds (shuffle=False), including the order of classes by first appearance.
  fit_tree / tree_predict   Port of the line-by-line CART replica in ref/sk_tree_replica.py (float32 inputs, feature order drawn from RandomState(seed), xorshift generator,
                            strict improvement, midpoint thresholds, depth first left first). That replica was checked against real scikit-learn on earlier sessions' slides.
                            Ties between equally good splits on repeated feature values are the remaining risk (stable sort here, not promised by scikit-learn).
                            predict follows scikit-learn: class 1 only if the leaf share of defaults is above 0.5 (argmax of the probabilities).
"""
import functools
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
DATA = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'data'

TOTAL_REPAYMENT_FACTOR = 1.15            # ILLUSTRATIVE assumption (see docstring); not in loans.csv
COST_MISS = 1_000_000                    # UGX per missed default (illustrative teaching cost)
COST_ALARM = 100_000                     # UGX per false alarm (illustrative teaching cost)
RULE_THRESHOLD = COST_ALARM / (COST_ALARM + COST_MISS)   # 100/1100 = 0.0909: flag when p >= this
SEED = 42
TEST_SIZE = 0.25
THRESHOLDS = (0.5, 0.3, 0.2, 0.15, 0.1)
HEADLINE_THRESHOLD = 0.2                 # the cut-off shown on slides for the audit and the evidence slide
CATEGORICAL = ['gender', 'occupation', 'loan_purpose']

FEATURES = ['age', 'monthly_income_ugx', 'income_missing', 'loan_amount_ugx', 'term_months', 'previous_loans', 'previous_late_payments', 'group_loan',
            'savings_balance_ugx', 'has_mobile_money', 'distance_to_branch_km', 'instalment_to_income']      # 12 numeric, Session 14 (burden renamed)

# Known split fingerprint of the canonical stratified split (from this module's replica; confirm on real scikit-learn). Filled by _selfcheck at the bottom of the file.
SPLIT_CHECK = {'first10_test_index': [4299, 1151, 2351, 5249, 1328, 3988, 261, 3389, 6878, 5150], 'sum_test_index': 8081998}


# ============================================================================ preparation
def prepare(path=None):
    """The prepared loans DataFrame (8,000 rows, original row order, index 0..7999).
    Columns: the 18 original columns, then income_missing, instalment_to_income and the 15 indicator columns (gender_*, occupation_*, loan_purpose_*).
    Steps: (1) two impossible ages (< 18 or > 100) replaced by the median of the valid ages; (2) income_missing = 1 where income is blank; (3) blank income replaced by the median income
    of the 8,000 loans (computed before the split on purpose: simple, and the leak is tiny; Session 20 shows the Pipeline way); (4) instalment_to_income = loan * 1.15 / term / income
    (1.15 is an ILLUSTRATIVE total-repayment factor, not in the data); (5) one-hot indicators with pd.get_dummies(..., dtype=int)."""
    raw = pd.read_csv(Path(path) if path else DATA / 'loans.csv')
    loans = raw.copy()
    bad = (loans.age < 18) | (loans.age > 100)
    loans.loc[bad, 'age'] = loans.loc[~bad, 'age'].median()
    loans['income_missing'] = loans.monthly_income_ugx.isna().astype(int)
    loans['monthly_income_ugx'] = loans.monthly_income_ugx.fillna(loans.monthly_income_ugx.median())
    loans['instalment_to_income'] = loans.loan_amount_ugx * TOTAL_REPAYMENT_FACTOR / loans.term_months / loans.monthly_income_ugx
    dummies = pd.get_dummies(loans[CATEGORICAL], dtype=int)
    return pd.concat([loans, dummies], axis=1)


def indicator_columns(loans):
    """The 15 one-hot indicator column names, in the order of pd.get_dummies."""
    return [c for c in loans.columns if any(c.startswith(p + '_') for p in CATEGORICAL)]


def feature_columns(loans, which='numeric'):
    """'numeric' = the 12 FEATURES; 'all' = 12 + 15 indicators = 27 columns; or pass your own list."""
    if which == 'numeric':
        return list(FEATURES)
    if which == 'all':
        return list(FEATURES) + indicator_columns(loans)
    return list(which)


# ============================================================================ the splits
def _approximate_mode(class_counts, n_draws, rng):
    """sklearn.utils.extmath._approximate_mode"""
    continuous = class_counts / class_counts.sum() * n_draws
    floored = np.floor(continuous)
    need_to_add = int(n_draws - floored.sum())
    if need_to_add > 0:
        remainder = continuous - floored
        values = np.sort(np.unique(remainder))[::-1]
        for value in values:
            (inds,) = np.where(remainder == value)
            add_now = min(len(inds), need_to_add)
            inds = rng.choice(inds, size=add_now, replace=False)
            floored[inds] += 1
            need_to_add -= add_now
            if need_to_add == 0:
                break
    return floored.astype(int)


def split_indices(y, stratify=True, test_size=TEST_SIZE, random_state=SEED):
    """Positions (train_idx, test_idx) of train_test_split(..., test_size=0.25, [stratify=y,] random_state=42), in scikit-learn's order (rows are shuffled, not sorted)."""
    y = np.asarray(y)
    n = len(y)
    n_test = int(np.ceil(test_size * n))
    n_train = int(np.floor((1 - test_size) * n))
    rng = np.random.RandomState(random_state)
    if not stratify:                                   # ShuffleSplit._iter_indices
        perm = rng.permutation(n)
        return perm[n_test:n_test + n_train], perm[:n_test]
    classes, y_indices = np.unique(y, return_inverse=True)       # StratifiedShuffleSplit._iter_indices
    n_classes = len(classes)
    class_counts = np.bincount(y_indices)
    class_indices = np.split(np.argsort(y_indices, kind='mergesort'), np.cumsum(class_counts)[:-1])
    n_i = _approximate_mode(class_counts, n_train, rng)
    class_counts_remaining = class_counts - n_i
    t_i = _approximate_mode(class_counts_remaining, n_test, rng)
    train, test = [], []
    for i in range(n_classes):
        permutation = rng.permutation(class_counts[i])
        perm_indices_class_i = class_indices[i].take(permutation, mode='clip')
        train.extend(perm_indices_class_i[:n_i[i]])
        test.extend(perm_indices_class_i[n_i[i]:n_i[i] + t_i[i]])
    train = rng.permutation(train)
    test = rng.permutation(test)
    return train, test


def split(loans=None, columns='numeric', stratify=True):
    """X_train, X_test, y_train, y_test: the canonical split, returned as pandas objects with their original row labels (like scikit-learn).
    columns: 'numeric' (12), 'all' (27) or a list. stratify=True is the canonical split (6,000 / 2,000; 753 / 251 defaults).
    stratify=False replicates train_test_split(random_state=42) (6,000 / 2,000 too, but a different 2,000 loans and about 230 test defaults): for contrast only."""
    if loans is None:
        loans = prepare()
    cols = feature_columns(loans, columns)
    X, y = loans[cols], loans['default']
    tr, te = split_indices(y.to_numpy(), stratify=stratify)
    return X.iloc[tr], X.iloc[te], y.iloc[tr], y.iloc[te]


# ============================================================================ cross-validation
def stratified_kfold(y, k=5):
    """Fold number (0..k-1) of every row under StratifiedKFold(n_splits=k) with shuffle=False (sklearn _make_test_folds)."""
    y = np.asarray(y)
    _, y_idx, y_inv = np.unique(y, return_index=True, return_inverse=True)
    _, class_perm = np.unique(y_idx, return_inverse=True)
    y_encoded = class_perm[y_inv]
    n_classes = len(y_idx)
    y_order = np.sort(y_encoded)
    allocation = np.asarray([np.bincount(y_order[i::k], minlength=n_classes) for i in range(k)])
    folds = np.empty(len(y), dtype=int)
    for c in range(n_classes):
        folds[y_encoded == c] = np.arange(k).repeat(allocation[:, c])
    return folds


def cv_splits(y, k=5):
    f = stratified_kfold(y, k)
    return [(np.where(f != i)[0], np.where(f == i)[0]) for i in range(k)]


# ============================================================================ logistic regression
def _sigmoid(z):
    return 0.5 * (1 + np.tanh(0.5 * z))


class ScaledLogReg:
    """numpy replica of make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)), C=1.0 (L2), solved exactly by Newton steps.
    Objective: 0.5 * sum(w^2) + C * sum(log loss); intercept free. Attributes: mean_, scale_, intercept_, coef_ (per 1 standard deviation of each variable), columns_."""

    def __init__(self, C=1.0):
        self.C = C

    def fit(self, X, y):
        self.columns_ = list(X.columns) if hasattr(X, 'columns') else None
        X = np.asarray(X, float)
        y = np.asarray(y, float)
        self.mean_ = X.mean(0)
        sd = X.std(0)                                  # population standard deviation, as StandardScaler
        self.scale_ = np.where(sd == 0, 1.0, sd)
        Z = (X - self.mean_) / self.scale_
        A = np.column_stack([np.ones(len(Z)), Z])
        th = np.zeros(A.shape[1])
        pen = np.eye(A.shape[1])
        pen[0, 0] = 0
        for _ in range(100):
            p = _sigmoid(A @ th)
            g = pen @ th + self.C * A.T @ (p - y)
            H = pen + self.C * (A.T * (p * (1 - p))) @ A
            step = np.linalg.solve(H, g)
            th -= step
            if np.max(np.abs(step)) < 1e-12:
                break
        self.intercept_, self.coef_ = th[0], th[1:]
        p = _sigmoid(A @ th)
        self.grad_max_ = float(np.max(np.abs(pen @ th + self.C * A.T @ (p - y))))     # about 1e-11 at the optimum
        return self

    def decision_function(self, X):
        Z = (np.asarray(X, float) - self.mean_) / self.scale_
        return self.intercept_ + Z @ self.coef_

    def predict_proba(self, X):
        """Probability of default (the second column of scikit-learn's predict_proba), strictly between 0 and 1."""
        return _sigmoid(self.decision_function(X))

    def coef_table(self):
        return dict(zip(self.columns_, [float(c) for c in self.coef_]))


# ============================================================================ metrics
def auc_rank(y, score):
    """AUC by ranks (Mann-Whitney), ties count half."""
    y = np.asarray(y).astype(int)
    r = pd.Series(np.asarray(score, float)).rank(method='average').to_numpy()
    npos, nneg = (y == 1).sum(), (y == 0).sum()
    return float((r[y == 1].sum() - npos * (npos + 1) / 2) / (npos * nneg))


def roc_points(y, score):
    """(fpr, tpr, thresholds) with one point per distinct score, starting at (0, 0), like sklearn.metrics.roc_curve(drop_intermediate=False)."""
    y = np.asarray(y).astype(int)
    s = np.asarray(score, float)
    order = np.argsort(-s, kind='mergesort')
    s, y = s[order], y[order]
    distinct = np.r_[np.where(np.diff(s))[0], len(y) - 1]
    tps = np.cumsum(y)[distinct]
    fps = 1 + distinct - tps
    fpr = np.r_[0, fps / fps[-1]]
    tpr = np.r_[0, tps / tps[-1]]
    return fpr, tpr, np.r_[np.inf, s[distinct]]


def auc_trapezoid(y, score):
    """AUC as the area under the ROC curve by the trapezoid rule (second, independent method)."""
    fpr, tpr, _ = roc_points(y, score)
    return float(np.sum(np.diff(fpr) * (tpr[1:] + tpr[:-1]) / 2))


def confusion(y, flag):
    """Counts when flag (bool or 0/1) is the model's 'default' call: tp, fp, fn, tn."""
    y = np.asarray(y).astype(int)
    f = np.asarray(flag).astype(int)
    return dict(tp=int(((y == 1) & (f == 1)).sum()), fp=int(((y == 0) & (f == 1)).sum()), fn=int(((y == 1) & (f == 0)).sum()), tn=int(((y == 0) & (f == 0)).sum()))


def prf(c):
    """precision, recall, f1, accuracy, flagged from a confusion dict."""
    tp, fp, fn, tn = c['tp'], c['fp'], c['fn'], c['tn']
    pr = tp / (tp + fp) if tp + fp else 0.0
    rc = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * pr * rc / (pr + rc) if pr + rc else 0.0
    return dict(precision=pr, recall=rc, f1=f1, accuracy=(tp + tn) / (tp + fp + fn + tn), flagged=tp + fp)


def at_threshold(y, p, threshold):
    """Confusion counts plus precision, recall, F1, accuracy, flagged and cost (UGX) when loans with probability >= threshold are flagged."""
    c = confusion(y, np.asarray(p) >= threshold)
    return dict(c, **prf(c), cost=cost(c))


def cost(c, miss=COST_MISS, alarm=COST_ALARM):
    """UGX: missed defaults * 1,000,000 + false alarms * 100,000 (illustrative costs)."""
    return c['fn'] * miss + c['fp'] * alarm


def cost_table(y, p, grid=None):
    """{threshold: cost in UGX} on a grid (default 0.02 to 0.60 step 0.01) plus the rule threshold; also 'none' (flag nobody) and 'all' (flag everybody)."""
    y = np.asarray(y).astype(int)
    grid = np.round(np.arange(0.02, 0.605, 0.01), 2) if grid is None else grid
    t = {float(g): cost(confusion(y, np.asarray(p) >= g)) for g in grid}
    t[float(RULE_THRESHOLD)] = cost(confusion(y, np.asarray(p) >= RULE_THRESHOLD))
    return t, dict(none=int(y.sum()) * COST_MISS, all=int((y == 0).sum()) * COST_ALARM)


def cheapest(table):
    """Threshold with the lowest cost (first on a tie), ignoring the rule threshold entry."""
    return min((k for k in table if abs(k - RULE_THRESHOLD) > 1e-12), key=lambda k: (table[k], k))


def oof_proba(X, y, k=5, C=1.0):
    """Out-of-fold probabilities by stratified k-fold on (X, y): a scaled logistic regression is fitted on k-1 folds and predicts the held-out fold.
    Use on the TRAINING rows to choose a decision threshold without touching the test rows."""
    X = np.asarray(X, float)
    y = np.asarray(y)
    out = np.empty(len(y))
    for tr, te in cv_splits(y, k):
        out[te] = ScaledLogReg(C).fit(X[tr], y[tr]).predict_proba(X[te])
    return out


def cv_auc(X, y, k=5, C=1.0):
    """cross_val_score(make_pipeline(StandardScaler(), LogisticRegression()), X, y, cv=5, scoring='roc_auc') replica: list of k fold AUCs."""
    X = np.asarray(X, float)
    y = np.asarray(y)
    return [auc_rank(y[te], ScaledLogReg(C).fit(X[tr], y[tr]).predict_proba(X[te])) for tr, te in cv_splits(y, k)]


# ============================================================================ decision tree (CART, Gini), port of ref/sk_tree_replica.py
_EPS = float(np.finfo('double').eps)
_FEATURE_THRESHOLD = 1e-7
_RAND_R_MAX = 0x7FFFFFFF


class _Rng:
    def __init__(self, seed):
        self.s = int(seed) & 0xFFFFFFFF

    def rand_int(self, low, high):
        if self.s == 0:
            self.s = 1
        s = self.s
        s ^= (s << 13) & 0xFFFFFFFF
        s ^= s >> 17
        s ^= (s << 5) & 0xFFFFFFFF
        self.s = s
        return low + (s % (_RAND_R_MAX + 1)) % (high - low)


class _Gini:
    def __init__(self, y):
        self.y = y
        self.k = 2

    def node_reset(self, samples, start, end):
        self.start, self.end = start, end
        c = [0.0] * self.k
        for p in range(start, end):
            c[self.y[samples[p]]] += 1.0
        self.total = c
        self.n = float(end - start)

    @staticmethod
    def _g(c, n):
        sq = 0.0
        for v in c:
            sq += v * v
        return 1.0 - sq / (n * n)

    def impurity(self):
        return self._g(self.total, self.n)

    def value(self):
        return self.total[1] / self.n

    def reset(self):
        self.pos = self.start
        self.cl = [0.0] * self.k
        self.cr = list(self.total)
        self.nl = 0.0
        self.nr = self.n

    def reverse_reset(self):
        self.pos = self.end
        self.cl = list(self.total)
        self.cr = [0.0] * self.k
        self.nl = self.n
        self.nr = 0.0

    def update(self, samples, new_pos):
        if (new_pos - self.pos) <= (self.end - new_pos):
            for p in range(self.pos, new_pos):
                self.cl[self.y[samples[p]]] += 1.0
                self.nl += 1.0
        else:
            self.reverse_reset()
            for p in range(self.end - 1, new_pos - 1, -1):
                self.cl[self.y[samples[p]]] -= 1.0
                self.nl -= 1.0
        self.nr = self.n - self.nl
        self.cr = [t - l for t, l in zip(self.total, self.cl)]
        self.pos = new_pos

    def proxy(self):
        return -self.nr * self._g(self.cr, self.nr) - self.nl * self._g(self.cl, self.nl)


def fit_tree(X, y, max_depth=3, seed=SEED):
    """DecisionTreeClassifier(max_depth=max_depth, random_state=seed) port. Returns a nested tuple: ('split', feature_index, threshold, left, right) or ('leaf', share_of_defaults)."""
    X = np.asarray(X, float).astype(np.float32)
    n, nf = X.shape
    seed = int(np.random.RandomState(seed).randint(0, _RAND_R_MAX))
    rng = _Rng(seed)
    y = np.asarray(y, int)
    crit = _Gini(y)
    samples = np.arange(n)
    features = list(range(nf))
    const = list(range(nf))

    def node_split(start, end, n_known):
        best = None
        best_prox = -np.inf
        n_found = 0
        n_drawn = 0
        n_total = n_known
        f_i = nf
        visited = 0
        while f_i > n_total and (visited < nf or visited <= n_found + n_drawn):
            visited += 1
            f_j = rng.rand_int(n_drawn, f_i - n_found)
            if f_j < n_known:
                features[n_drawn], features[f_j] = features[f_j], features[n_drawn]
                n_drawn += 1
                continue
            f_j += n_found
            feat = features[f_j]
            vals = X[samples[start:end], feat]
            order = np.argsort(vals, kind='stable')
            samples[start:end] = samples[start:end][order]
            fv = vals[order].astype(np.float64)
            if fv[-1] <= fv[0] + _FEATURE_THRESHOLD:
                features[f_j], features[n_total] = features[n_total], features[f_j]
                n_found += 1
                n_total += 1
                continue
            f_i -= 1
            features[f_i], features[f_j] = features[f_j], features[f_i]
            crit.reset()
            p = start
            while p < end:
                while p + 1 < end and fv[p + 1 - start] <= fv[p - start] + _FEATURE_THRESHOLD:
                    p += 1
                p += 1
                if p < end:
                    crit.update(samples, p)
                    prox = crit.proxy()
                    if prox > best_prox:
                        best_prox = prox
                        thr = fv[p - 1 - start] / 2.0 + fv[p - start] / 2.0
                        if thr == fv[p - start] or thr in (np.inf, -np.inf):
                            thr = fv[p - 1 - start]
                        best = (feat, thr, p)
        for i in range(n_known):
            features[i] = const[i]
        for i in range(n_found):
            const[n_known + i] = features[n_known + i]
        return best, n_total

    root = [None]
    stack = [(0, n, 0, 0, root, 0)]
    while stack:
        start, end, depth, n_const, holder, idx = stack.pop()
        crit.node_reset(samples, start, end)
        leaf = depth >= max_depth or (end - start) < 2 or crit.impurity() <= _EPS
        best = None
        if not leaf:
            best, n_const = node_split(start, end, n_const)
            leaf = best is None
        if leaf:
            holder[idx] = ('leaf', crit.value())
            continue
        feat, thr, _ = best
        p, pe = start, end
        while p < pe:
            if float(X[samples[p], feat]) <= thr:
                p += 1
            else:
                pe -= 1
                samples[p], samples[pe] = samples[pe], samples[p]
        node = ['split', feat, thr, None, None]
        holder[idx] = node
        stack.append((p, end, depth + 1, n_const, node, 4))
        stack.append((start, p, depth + 1, n_const, node, 3))

    def freeze(t):
        return t if t[0] == 'leaf' else ('split', t[1], t[2], freeze(t[3]), freeze(t[4]))

    return freeze(root[0])


def tree_proba(tree, X):
    """Share of defaults in the leaf each row lands in (predict_proba[:, 1])."""
    X = np.asarray(X, float).astype(np.float32)
    out = np.empty(len(X))
    for r, x in enumerate(X):
        node = tree
        while node[0] == 'split':
            node = node[3] if float(x[node[1]]) <= node[2] else node[4]
        out[r] = node[1]
    return out


def tree_predict(tree, X):
    """Class 0 or 1 as DecisionTreeClassifier.predict: 1 only when the leaf share of defaults is above 0.5."""
    return (tree_proba(tree, X) > 0.5).astype(int)


def tree_rules(tree, names, indent=''):
    """Text rules like sklearn.tree.export_text (thresholds to 2 decimals)."""
    if tree[0] == 'leaf':
        return f'{indent}default share {tree[1]:.3f}\n'
    nm, t = names[tree[1]], tree[2]
    return (f'{indent}{nm} <= {t:.2f}\n' + tree_rules(tree[3], names, indent + '    ') + f'{indent}{nm} >  {t:.2f}\n' + tree_rules(tree[4], names, indent + '    '))


# ============================================================================ headline numbers
def _r(x, d=6):
    return round(float(x), d)


def _thr_block(y, p):
    return {t: at_threshold(y, p, t) for t in THRESHOLDS} | {'rule': at_threshold(y, p, RULE_THRESHOLD)}


@functools.lru_cache(maxsize=None)
def facts():
    """One dict with every headline number sessions quote. Numbers are from the numpy replicas (see module docstring): recompute with real scikit-learn before printing on a handout.
    Keys ending _12 use the 12 numeric columns, keys ending _27 use 12 numeric + 15 indicator columns (Sessions 15 to 17 headline model)."""
    F = {}
    loans = prepare()
    raw = pd.read_csv(DATA / 'loans.csv')
    bad = (raw.age < 18) | (raw.age > 100)
    F.update(rows=len(loans), cols_original=raw.shape[1], defaults=int(loans.default.sum()), default_rate=_r(loans.default.mean()), bad_ages=sorted(int(a) for a in raw.age[bad]),
             age_median=float(raw.age[~bad].median()), income_blank=int(raw.monthly_income_ugx.isna().sum()), income_median=float(raw.monthly_income_ugx.median()),
             instalment_to_income_median=_r(loans.instalment_to_income.median()), instalment_to_income_max=_r(loans.instalment_to_income.max()),
             n_features_numeric=len(FEATURES), n_indicators=len(indicator_columns(loans)), n_features_all=len(FEATURES) + len(indicator_columns(loans)),
             repayment_factor=TOTAL_REPAYMENT_FACTOR, cost_miss=COST_MISS, cost_alarm=COST_ALARM, rule_threshold=_r(RULE_THRESHOLD, 4))
    y = loans.default.to_numpy()
    tr, te = split_indices(y)
    ytr, yte = y[tr], y[te]
    F.update(n_train=len(tr), n_test=len(te), train_defaults=int(ytr.sum()), test_defaults=int(yte.sum()), test_repaid=int((yte == 0).sum()), test_rate=_r(yte.mean()),
             baseline_accuracy=_r((yte == 0).mean(), 4), baseline_correct=int((yte == 0).sum()), baseline_recall=0.0,
             test_index_first10=[int(i) for i in te[:10]], test_index_sum=int(te.sum()), train_index_first10=[int(i) for i in tr[:10]])
    # non-stratified, for contrast
    tr_u, te_u = split_indices(y, stratify=False)
    F.update(unstratified_test_defaults=int(y[te_u].sum()), unstratified_baseline_accuracy=_r(1 - y[te_u].mean(), 4), unstratified_n_train=len(tr_u), unstratified_n_test=len(te_u))

    models = {}
    for tag, which in (('12', 'numeric'), ('27', 'all')):
        cols = feature_columns(loans, which)
        Xtr, Xte = loans[cols].to_numpy(float)[tr], loans[cols].to_numpy(float)[te]
        m = ScaledLogReg().fit(pd.DataFrame(Xtr, columns=cols), ytr)
        p = m.predict_proba(Xte)
        ptr = m.predict_proba(Xtr)
        models[tag] = (m, p, ptr, cols, Xtr, Xte)
        F[f'auc_{tag}'] = _r(auc_rank(yte, p))
        F[f'auc_{tag}_check_trapezoid'] = _r(auc_trapezoid(yte, p))
        F[f'auc_train_{tag}'] = _r(auc_rank(ytr, ptr))
        F[f'p_min_{tag}'], F[f'p_max_{tag}'] = _r(p.min()), _r(p.max())
        F[f'grad_max_{tag}'] = m.grad_max_
        F[f'thr_{tag}'] = {t: {k: (_r(v) if isinstance(v, float) else v) for k, v in d.items()} for t, d in _thr_block(yte, p).items()}
        tab, extra = cost_table(yte, p)
        F[f'cost_none'] = extra['none']
        F[f'cost_all'] = extra['all']
        F[f'cost_{tag}'] = {t: tab[t] for t in tab if t in THRESHOLDS or abs(t - RULE_THRESHOLD) < 1e-12}
        F[f'cheapest_on_test_{tag}'] = dict(threshold=cheapest(tab), cost=tab[cheapest(tab)], note='chosen by looking at the test loans: for contrast only, do NOT teach this')
        # threshold chosen on the TRAINING rows by 5-fold cross-validation, then used once on the test loans
        oof = oof_proba(Xtr, ytr)
        ttab, _ = cost_table(ytr, oof)
        tcv = cheapest(ttab)
        F[f'cv_threshold_{tag}'] = dict(threshold=tcv, train_oof_cost=ttab[tcv], train_oof_cost_per_test_size=int(round(ttab[tcv] * len(te) / len(tr))),
                                        test=at_threshold(yte, p, tcv), rule_test_cost=tab[float(RULE_THRESHOLD)])
        F[f'cv_auc_train_{tag}'] = dict(folds=[_r(a) for a in cv_auc(Xtr, ytr)])
        a = F[f'cv_auc_train_{tag}']['folds']
        F[f'cv_auc_train_{tag}'].update(mean=_r(np.mean(a)), sd=_r(np.std(a, ddof=1)), sd_ddof0=_r(np.std(a)), fold_size=len(tr) // 5, fold_defaults=sorted(set(int(ytr[te_].sum()) for _, te_ in cv_splits(ytr))))
        Xall = loans[cols].to_numpy(float)
        a = cv_auc(Xall, y)
        F[f'cv_auc_all_{tag}'] = dict(folds=[_r(v) for v in a], mean=_r(np.mean(a)), sd=_r(np.std(a, ddof=1)), sd_ddof0=_r(np.std(a)), fold_size=len(y) // 5,
                                      fold_defaults=sorted(set(int(y[te_].sum()) for _, te_ in cv_splits(y))))
    F['cost_note'] = 'cost = missed defaults * 1,000,000 + false alarms * 100,000 UGX on the 2,000 test loans; none = flag nobody; all = flag everybody'

    # coefficients (27 columns, per 1 standard deviation; sign tells direction; ratio is exp(coef))
    m27 = models['27'][0]
    ct = m27.coef_table()
    F['coef_27'] = {k: _r(v, 4) + 0.0 for k, v in ct.items()}
    F['coef_27_ranked'] = [(k, _r(v, 4) + 0.0) for k, v in sorted(ct.items(), key=lambda kv: -abs(kv[1]))]
    F['coef_gender_note'] = 'gender_F and gender_M are mirror columns (they add to 1); under L2 their coefficients are equal and opposite and here both are about 0.00 per standard deviation'
    F['coef_intercept_27'] = _r(m27.intercept_, 4)
    F['coef_12'] = {k: _r(v, 4) for k, v in models['12'][0].coef_table().items()}
    key = ['instalment_to_income', 'previous_late_payments', 'savings_balance_ugx', 'monthly_income_ugx', 'age', 'distance_to_branch_km', 'income_missing', 'has_mobile_money', 'group_loan']
    F['key_coef_signs_27'] = {k: ('+' if ct[k] > 0 else '-') for k in key}

    # decision tree depth 3 on the 12 numeric columns (as Session 14)
    Xtr12, Xte12 = models['12'][4], models['12'][5]
    tree = fit_tree(Xtr12, ytr, 3, SEED)
    pt = tree_predict(tree, Xte12)
    ct_ = confusion(yte, pt)
    F['tree'] = dict(ct_, **{k: _r(v) for k, v in prf(ct_).items() if k != 'flagged'}, flagged=ct_['tp'] + ct_['fp'], root_feature=FEATURES[tree[1]], root_threshold=_r(tree[2], 4),
                     auc=_r(auc_rank(yte, tree_proba(tree, Xte12))), leaves=len(set(np.round(tree_proba(tree, Xte12), 9))), rules=tree_rules(tree, FEATURES),
                     faithfulness='port of the sklearn CART replica in ref/sk_tree_replica.py; ties between equal splits are the residual risk')
    # the same tree on 27 columns (Session 15 shows a tree after one-hot)
    Xtr27, Xte27 = models['27'][4], models['27'][5]
    tree27 = fit_tree(Xtr27, ytr, 3, SEED)
    p27 = tree_predict(tree27, Xte27)
    c27 = confusion(yte, p27)
    F['tree_27'] = dict(c27, accuracy=_r(prf(c27)['accuracy']), recall=_r(prf(c27)['recall']), root_feature=models['27'][3][tree27[1]], root_threshold=_r(tree27[2], 4))
    # the Excel rule: instalment_to_income > 0.6
    hand = loans.instalment_to_income.to_numpy()[te] > 0.6
    hc = confusion(yte, hand)
    F['excel_rule_0_6'] = dict(hc, **{k: _r(v) for k, v in prf(hc).items()})
    # leakage: collection_calls
    calls = loans.collection_calls.to_numpy(float)
    F['calls_share_with_call'] = {int(k): _r(((calls[y == k]) > 0).mean()) for k in (0, 1)}
    for tag in ('12', '27'):
        Xl_tr = np.column_stack([models[tag][4], calls[tr]])
        Xl_te = np.column_stack([models[tag][5], calls[te]])
        ml = ScaledLogReg().fit(Xl_tr, ytr)
        F[f'leaky_auc_{tag}'] = _r(auc_rank(yte, ml.predict_proba(Xl_te)))
    # S23 simplified four-variable model
    four = ['monthly_income_ugx', 'loan_amount_ugx', 'term_months', 'previous_late_payments']
    X4 = loans[four].to_numpy(float)
    m4 = ScaledLogReg().fit(X4[tr], ytr)
    p4 = m4.predict_proba(X4[te])
    F['four_variable'] = dict(columns=four, auc=_r(auc_rank(yte, p4)), thr_0_2=at_threshold(yte, p4, 0.2), thr_0_15=at_threshold(yte, p4, 0.15),
                              note='deliberately small model for the S23 app; income is the prepared (median-filled) column')

    # gender audit on the 2,000 test loans: approve a loan when the model's probability of default is BELOW the cut-off (flag it when >= cut-off)
    cut = HEADLINE_THRESHOLD
    g = loans.gender.to_numpy()[te]
    audit = {}
    for tag in ('27', '12'):
        p = models[tag][1]
        rows = {}
        for gv in ('F', 'M'):
            mk = g == gv
            appr = p[mk] < cut
            rows[gv] = dict(n=int(mk.sum()), default_rate=_r(yte[mk].mean()), approved=int(appr.sum()), approval_rate=_r(appr.mean()), flagged=int((~appr).sum()),
                            defaults=int(yte[mk].sum()), caught=int(((p[mk] >= cut) & (yte[mk] == 1)).sum()),
                            recall=_r(((p[mk] >= cut) & (yte[mk] == 1)).sum() / max(1, yte[mk].sum())),
                            false_alarm_rate=_r(((p[mk] >= cut) & (yte[mk] == 0)).sum() / max(1, (yte[mk] == 0).sum())))
        rows['approval_ratio_F_over_M'] = _r(rows['F']['approval_rate'] / rows['M']['approval_rate'])
        rows['disparate_impact_ratio'] = _r(min(rows['F']['approval_rate'], rows['M']['approval_rate']) / max(rows['F']['approval_rate'], rows['M']['approval_rate']))   # four-fifths rule: below 0.8 is a flag
        rows['rule'] = f'approve when predicted probability of default < {cut}, model with {tag} columns, on the 2,000 test loans' + (' (gender is one of the inputs)' if tag == '27' else ' (gender is NOT an input)')
        audit[tag] = rows
    F['gender_audit'] = audit
    F['gender_audit_cutoff'] = cut
    return F


def write_split_file(path=None):
    """Writes loans_canon_split.csv (row, loan_id, subset) so any tool can reproduce the canonical 6,000 / 2,000 rows."""
    loans = prepare()
    tr, te = split_indices(loans.default.to_numpy())
    subset = np.empty(len(loans), object)
    subset[tr] = 'train'
    subset[te] = 'test'
    out = pd.DataFrame(dict(row=np.arange(len(loans)), loan_id=loans.loan_id, subset=subset, test_position=-1))
    out.loc[te, 'test_position'] = np.arange(len(te))
    p = Path(path) if path else BUILD / 'loans_canon_split.csv'
    out.to_csv(p, index=False)
    return p


if __name__ == '__main__':
    import json
    F = facts()
    print(json.dumps({k: v for k, v in F.items() if k not in ('coef_27', 'coef_12')}, indent=1, default=str))
