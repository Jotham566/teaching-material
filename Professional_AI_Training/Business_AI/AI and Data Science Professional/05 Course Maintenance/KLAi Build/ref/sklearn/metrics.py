import numpy as np
def mean_absolute_error(a, p): return float(np.mean(np.abs(np.asarray(a, float) - np.asarray(p, float))))
def mean_squared_error(a, p, squared=True):
    m = float(np.mean((np.asarray(a, float) - np.asarray(p, float)) ** 2)); return m if squared else m ** 0.5
def root_mean_squared_error(a, p): return mean_squared_error(a, p) ** 0.5


def confusion_matrix(a, p):
    a, p = np.asarray(a).astype(int), np.asarray(p).astype(int)
    return np.array([[int(((a == 0) & (p == 0)).sum()), int(((a == 0) & (p == 1)).sum())], [int(((a == 1) & (p == 0)).sum()), int(((a == 1) & (p == 1)).sum())]])
def accuracy_score(a, p): return float(np.mean(np.asarray(a) == np.asarray(p)))
def precision_score(a, p, zero_division=0):
    c = confusion_matrix(a, p); d = c[0, 1] + c[1, 1]; return float(c[1, 1] / d) if d else float(zero_division)
def recall_score(a, p, zero_division=0):
    c = confusion_matrix(a, p); d = c[1, 0] + c[1, 1]; return float(c[1, 1] / d) if d else float(zero_division)
def f1_score(a, p, zero_division=0):
    pr, rc = precision_score(a, p), recall_score(a, p); return float(2 * pr * rc / (pr + rc)) if pr + rc else float(zero_division)
def roc_auc_score(a, s):
    a, s = np.asarray(a), np.asarray(s, float); pos, neg = s[a == 1], s[a == 0]
    return float(np.mean([(x > y) + 0.5 * (x == y) for x in pos for y in neg]))
def roc_curve(a, s):
    a, s = np.asarray(a), np.asarray(s, float); th = np.r_[np.inf, np.unique(s)[::-1]]
    P, N = (a == 1).sum(), (a == 0).sum()
    return np.array([((s >= t) & (a == 0)).sum() / N for t in th]), np.array([((s >= t) & (a == 1)).sum() / P for t in th]), th
def r2_score(a, p):
    a, p = np.asarray(a, float), np.asarray(p, float); return float(1 - ((a - p) ** 2).sum() / ((a - a.mean()) ** 2).sum())
