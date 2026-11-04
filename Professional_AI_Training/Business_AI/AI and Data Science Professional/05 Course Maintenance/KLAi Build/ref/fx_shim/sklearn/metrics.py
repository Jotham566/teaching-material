import numpy as np
from ._core import C


def _a(y, p):
    return np.asarray(y).astype(int), np.asarray(p).astype(int)


def accuracy_score(y, p):
    y, p = _a(y, p)
    return float(np.mean(y == p))


def confusion_matrix(y, p):
    c = C.confusion(*_a(y, p))
    return np.array([[c['tn'], c['fp']], [c['fn'], c['tp']]])


def precision_score(y, p, zero_division=0):
    c = C.confusion(*_a(y, p))
    return c['tp'] / (c['tp'] + c['fp']) if c['tp'] + c['fp'] else float(zero_division)


def recall_score(y, p, zero_division=0):
    c = C.confusion(*_a(y, p))
    return c['tp'] / (c['tp'] + c['fn']) if c['tp'] + c['fn'] else float(zero_division)


def f1_score(y, p, zero_division=0):
    pr, rc = precision_score(y, p), recall_score(y, p)
    return 2 * pr * rc / (pr + rc) if pr + rc else float(zero_division)


def roc_auc_score(y, s):
    return C.auc_rank(np.asarray(y), np.asarray(s, float))


def roc_curve(y, s):
    fpr, tpr, thr = C.roc_points(np.asarray(y), np.asarray(s, float))
    return fpr, tpr, thr


def precision_recall_curve(y, s):
    y = np.asarray(y).astype(int)
    s = np.asarray(s, float)
    ths = np.unique(s)
    P = (y == 1).sum()
    prec = np.array([((s >= t) & (y == 1)).sum() / max(1, (s >= t).sum()) for t in ths])
    rec = np.array([((s >= t) & (y == 1)).sum() / P for t in ths])
    return np.r_[prec, 1.0], np.r_[rec, 0.0], ths


def classification_report(y, p, zero_division=0):
    return f'precision {precision_score(y, p):.2f} recall {recall_score(y, p):.2f} f1 {f1_score(y, p):.2f}'
