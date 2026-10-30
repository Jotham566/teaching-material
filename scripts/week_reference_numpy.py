"""NumPy reference calculations for the Week 8 to 12 teaching slides.

Every number printed on the new Week 8b to 12 slides comes from this module, so the
slides never carry a typed result. The module re-implements, in plain NumPy, the
scikit-learn pieces the slides show: LinearRegression, DummyRegressor, the CART
decision trees, StandardScaler and L2 LogisticRegression (C=1).

scikit-learn was not installed where these slides were written. Run
`python3 scripts/verify_week_reference_with_sklearn.py` on a machine that has
scikit-learn; it compares every value here with the real library.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "IUEA_Teaching_Plan"
FEATURES = ["load_pct", "ambient_c"]

COHORT = {
    "CML3111": dict(short="motor temperature", unit="deg C", limit=80.0, thing="motor"),
    "CML3112": dict(short="cooling load", unit="kW", limit=54.0, thing="building"),
    "CML3113": dict(short="crusher energy demand", unit="kWh/t", limit=13.5, thing="crusher"),
}


def load(code):
    raw = pd.read_csv(BASE / "assessment_banks" / "W08" / code / "A" / "engineering_data.csv")
    d = raw.drop_duplicates("record_id").copy()
    d = d[d.target.notna() & d.load_pct.between(0, 100)].copy()
    tr = d[d.equipment_id.isin(["E1", "E2", "E3", "E4"])].copy()
    va = d[d.equipment_id == "E5"].copy()
    te = d[d.equipment_id == "E6"].copy()
    return raw, d, tr, va, te


# ---------------------------------------------------------------- basic pieces
def median_fill(tr, others):
    med = tr[FEATURES].median()
    return [x[FEATURES].fillna(med) for x in [tr] + others], med


def mae(a, p): return float(np.mean(np.abs(np.asarray(a) - np.asarray(p))))
def mse(a, p): return float(np.mean((np.asarray(a) - np.asarray(p)) ** 2))
def rmse(a, p): return mse(a, p) ** 0.5


def linreg_fit(X, y):
    A = np.column_stack([np.ones(len(X)), np.asarray(X, float)])
    coef, *_ = np.linalg.lstsq(A, np.asarray(y, float), rcond=None)
    return coef[0], coef[1:]


def linreg_predict(b, w, X): return b + np.asarray(X, float) @ w


# ---------------------------------------------------------------- CART trees
def _best_split(X, y, crit):
    n, p = X.shape
    best = None
    for j in range(p):
        order = np.argsort(X[:, j], kind="mergesort")
        xs, ys = X[order, j], y[order]
        for i in range(1, n):
            if xs[i] == xs[i - 1]: continue
            L, R = ys[:i], ys[i:]
            score = crit(L) * len(L) + crit(R) * len(R)
            if best is None or score < best[0] - 1e-12:
                best = (score, j, (xs[i] + xs[i - 1]) / 2)
    return best


def _grow(X, y, depth, max_depth, crit, leaf):
    if depth == max_depth or len(y) < 2 or crit(y) == 0:
        return ("leaf", leaf(y))
    b = _best_split(X, y, crit)
    if b is None: return ("leaf", leaf(y))
    _, j, t = b
    m = X[:, j] <= t
    return ("split", j, t, _grow(X[m], y[m], depth + 1, max_depth, crit, leaf),
            _grow(X[~m], y[~m], depth + 1, max_depth, crit, leaf))


def _walk(node, x):
    while node[0] == "split":
        node = node[3] if x[node[1]] <= node[2] else node[4]
    return node[1]


def tree_reg_fit(X, y, max_depth):
    return _grow(np.asarray(X, float), np.asarray(y, float), 0, max_depth, lambda v: float(np.var(v)), lambda v: float(np.mean(v)))


def gini(v):
    if len(v) == 0: return 0.0
    p = np.mean(v); return 2 * p * (1 - p)


def tree_clf_fit(X, y, max_depth):
    return _grow(np.asarray(X, float), np.asarray(y, int), 0, max_depth, gini, lambda v: float(np.mean(v)))


def tree_predict(tree, X): return np.array([_walk(tree, x) for x in np.asarray(X, float)])


def tree_depth_and_rules(tree, names, unit="", depth=0, out=None):
    out = [] if out is None else out
    pad = "  " * depth
    if tree[0] == "leaf":
        out.append(f"{pad}predict {tree[1]:.2f}")
    else:
        out.append(f"{pad}if {names[tree[1]]} <= {tree[2]:.2f}:")
        tree_depth_and_rules(tree[3], names, unit, depth + 1, out)
        out.append(f"{pad}else:")
        tree_depth_and_rules(tree[4], names, unit, depth + 1, out)
    return out


# ---------------------------------------------------------------- scaler, logistic
def scaler_fit(X):
    X = np.asarray(X, float); return X.mean(axis=0), X.std(axis=0)  # population std, as StandardScaler


def scaler_apply(X, mu, sd): return (np.asarray(X, float) - mu) / sd


def sigmoid(z): return 1.0 / (1.0 + np.exp(-z))


def logreg_fit(X, y, C=1.0, iters=100):
    """Minimise 0.5*||w||^2 + C * sum(log loss); the intercept is not penalised (scikit-learn's objective)."""
    X = np.asarray(X, float); y = np.asarray(y, float)
    A = np.column_stack([np.ones(len(X)), X]); theta = np.zeros(A.shape[1])
    pen = np.eye(A.shape[1]); pen[0, 0] = 0
    for _ in range(iters):
        p = sigmoid(A @ theta)
        g = pen @ theta + C * A.T @ (p - y)
        H = pen + C * (A.T * (p * (1 - p))) @ A
        step = np.linalg.solve(H, g); theta -= step
        if np.max(np.abs(step)) < 1e-12: break
    return theta[0], theta[1:]


def logreg_proba(b, w, X): return sigmoid(b + np.asarray(X, float) @ w)


# ---------------------------------------------------------------- classification metrics
def confusion(actual, pred):
    a = np.asarray(actual, int); p = np.asarray(pred, int)
    return dict(tp=int(((a == 1) & (p == 1)).sum()), fn=int(((a == 1) & (p == 0)).sum()),
                fp=int(((a == 0) & (p == 1)).sum()), tn=int(((a == 0) & (p == 0)).sum()))


def prf(c):
    prec = c["tp"] / (c["tp"] + c["fp"]) if c["tp"] + c["fp"] else 0.0
    rec = c["tp"] / (c["tp"] + c["fn"]) if c["tp"] + c["fn"] else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    acc = (c["tp"] + c["tn"]) / sum(c.values())
    return dict(precision=prec, recall=rec, f1=f1, accuracy=acc)


def auc(actual, score):
    a = np.asarray(actual, int); s = np.asarray(score, float)
    pos, neg = s[a == 1], s[a == 0]
    wins = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return float(wins / (len(pos) * len(neg)))


def roc_points(actual, score):
    a = np.asarray(actual, int); s = np.asarray(score, float)
    ths = np.r_[np.inf, np.sort(np.unique(s))[::-1]]
    pts = []
    for t in ths:
        pred = (s >= t).astype(int); c = confusion(a, pred)
        pts.append((c["fp"] / max(c["fp"] + c["tn"], 1), c["tp"] / max(c["tp"] + c["fn"], 1)))
    return pts


# ---------------------------------------------------------------- bundle used by the slides
def bundle(code):
    c = COHORT[code]; raw, d, tr, va, te = load(code)
    (trf, vaf), med = median_fill(tr, [va])
    out = dict(code=code, unit=c["unit"], short=c["short"], limit=c["limit"], n_clean=len(d), n_tr=len(tr), n_va=len(va), n_te=len(te),
               median=med.to_dict())
    ytr, yva = tr.target.to_numpy(), va.target.to_numpy()
    # regression
    out["baseline"] = float(ytr.mean())
    b, w = linreg_fit(trf, ytr)
    pl = linreg_predict(b, w, vaf)
    t4 = tree_reg_fit(trf, ytr, 4)
    pt = tree_predict(t4, vaf)
    out["lin"] = dict(intercept=float(b), w_load=float(w[0]), w_amb=float(w[1]))
    out["reg"] = {k: dict(mae=mae(yva, p), rmse=rmse(yva, p), mse=mse(yva, p)) for k, p in
                  [("baseline", np.full(len(yva), ytr.mean())), ("linear", pl), ("tree", pt)]}
    t2 = tree_reg_fit(trf, ytr, 2)
    out["tree2_rules"] = tree_depth_and_rules(t2, FEATURES)
    # line from load only, used for the by-hand equation slide
    b1, w1 = linreg_fit(trf[["load_pct"]], ytr)
    out["line_load_only"] = dict(intercept=float(b1), slope=float(w1[0]))
    # overfitting curve
    depths = list(range(1, 11)); curve = []
    for dpt in depths:
        tt = tree_reg_fit(trf, ytr, dpt)
        curve.append((dpt, mae(ytr, tree_predict(tt, trf)), mae(yva, tree_predict(tt, vaf))))
    out["overfit_curve"] = curve
    # classification
    lab = lambda df: (df.target >= c["limit"]).astype(int).to_numpy()
    ltr, lva = lab(tr), lab(va)
    out["cls_counts"] = dict(tr_pos=int(ltr.sum()), tr_n=len(ltr), va_pos=int(lva.sum()), va_n=len(lva),
                             all_pos=int(lab(d).sum()), all_n=len(d))
    out["always_no_acc"] = float((lva == 0).mean())
    mu, sd = scaler_fit(trf)
    out["scaler"] = dict(mu=mu.tolist(), sd=sd.tolist())
    out["ranges"] = dict(load=(float(trf.load_pct.min()), float(trf.load_pct.max())), amb=(float(trf.ambient_c.min()), float(trf.ambient_c.max())))
    Xs, Vs = scaler_apply(trf, mu, sd), scaler_apply(vaf, mu, sd)
    bl, wl = logreg_fit(Xs, ltr)
    pr = logreg_proba(bl, wl, Vs)
    out["logit"] = dict(b=float(bl), w=wl.tolist(), proba_first5=[float(x) for x in pr[:5]], actual_first5=[int(x) for x in lva[:5]])
    pred5 = (pr >= 0.5).astype(int); c5 = confusion(lva, pred5)
    out["logit_conf"] = c5; out["logit_metrics"] = prf(c5)
    out["thresholds"] = []
    for th in (0.3, 0.5, 0.7):
        cc = confusion(lva, (pr >= th).astype(int)); m = prf(cc)
        out["thresholds"].append(dict(th=th, **cc, **m))
    out["auc"] = auc(lva, pr); out["roc"] = roc_points(lva, pr)
    tc = tree_clf_fit(trf, ltr, 3); ptc = tree_predict(tc, vaf); cct = confusion(lva, (ptc >= 0.5).astype(int))
    out["tree_conf"] = cct; out["tree_metrics"] = prf(cct)
    # scaling example (first 3 training rows)
    out["scaling_rows"] = [(float(a), float(b_), float(x), float(y)) for (a, b_), (x, y) in zip(trf.head(3).to_numpy(), Xs[:3])]
    # data-leak demonstration: duplicate the validation rows into the training table
    leak_train = pd.concat([trf, vaf]); leak_y = np.r_[ytr, yva]
    tl = tree_reg_fit(leak_train, leak_y, 10); out["leak_demo"] = dict(honest=mae(yva, tree_predict(tree_reg_fit(trf, ytr, 10), vaf)),
                                                                      leaky=mae(yva, tree_predict(tl, vaf)))
    # feature engineering ablation (Week 11), following the slide code: the product is built from the raw columns
    # (so a blank ambient_c gives a blank product) and each pipeline then fills every column with its training median
    def with_int(df):
        e = df.copy(); e["load_ambient"] = e.load_pct * e.ambient_c; return e
    cols_ext = R_FEATURES = FEATURES + ["load_ambient"]
    trI, vaI = with_int(tr), with_int(va)
    medE = trI[cols_ext].median()
    trIf, vaIf = trI[cols_ext].fillna(medE), vaI[cols_ext].fillna(medE)
    b0, w0 = linreg_fit(trf, ytr); bI, wI = linreg_fit(trIf, ytr)
    out["ablation"] = dict(base=mae(yva, linreg_predict(b0, w0, vaf)), extended=mae(yva, linreg_predict(bI, wI, vaIf)))
    out["ablation"]["gain"] = out["ablation"]["base"] - out["ablation"]["extended"]
    # candidates for Week 12
    out["candidates"] = [("baseline", out["reg"]["baseline"]["mae"]), ("linear", out["reg"]["linear"]["mae"]), ("tree", out["reg"]["tree"]["mae"])]
    return out


if __name__ == "__main__":
    import json
    for code in COHORT:
        o = bundle(code)
        print(code, json.dumps({k: o[k] for k in ("n_clean", "n_tr", "n_va", "cls_counts", "always_no_acc", "reg", "logit_conf", "logit_metrics", "auc")}, indent=1, default=float))


# ---------------------------------------------------------------- Week 13: polynomial ridge and k-nearest neighbours
def poly_cols(x, degree):
    x = np.asarray(x, float).reshape(-1)
    return np.column_stack([x ** k for k in range(1, degree + 1)])


def ridge_fit(X, y, alpha):
    """PolynomialFeatures -> StandardScaler -> Ridge(alpha), the intercept not penalised: closed form on standardised columns."""
    mu, sd = X.mean(axis=0), X.std(axis=0); Z = (X - mu) / sd; ym = float(np.mean(y)); yc = np.asarray(y, float) - ym
    if alpha == 0:
        w = np.linalg.lstsq(Z, yc, rcond=None)[0]          # plain least squares, as LinearRegression does
    else:
        w = np.linalg.solve(Z.T @ Z + alpha * np.eye(Z.shape[1]), Z.T @ yc)
    return mu, sd, ym, w


def ridge_predict(m, X):
    mu, sd, ym, w = m; return ym + ((X - mu) / sd) @ w


def knn_fit_predict(Xtr, ytr, Xq, k):
    Xtr, Xq = np.asarray(Xtr, float), np.asarray(Xq, float); out = []
    for q in Xq:
        d = np.sqrt(((Xtr - q) ** 2).sum(axis=1)); idx = np.argsort(d, kind="stable")[:k]; out.append(float(np.mean(np.asarray(ytr)[idx])))
    return np.array(out)


def bundle13(code, degree=6):
    c = COHORT[code]; raw, d, tr, va, te = load(code); (trf, vaf), med = median_fill(tr, [va])
    ytr, yva = tr.target.to_numpy(), va.target.to_numpy(); o = bundle(code)
    xt, xv = tr.load_pct.to_numpy(), va.load_pct.to_numpy(); Pt, Pv = poly_cols(xt, degree), poly_cols(xv, degree)
    out = dict(degree=degree)
    b1, w1 = linreg_fit(xt[:, None], ytr)
    out["line_load"] = dict(train=mae(ytr, linreg_predict(b1, w1, xt[:, None])), valid=mae(yva, linreg_predict(b1, w1, xv[:, None])))
    m0 = ridge_fit(Pt, ytr, 0.0)
    rows = [("none", 0.0)] + [(f"alpha {a:g}", a) for a in (1.0, 100.0)]
    out["ridge_rows"] = []
    for name, a in rows:
        m = ridge_fit(Pt, ytr, a)
        out["ridge_rows"].append(dict(name=name, alpha=a, train=mae(ytr, ridge_predict(m, Pt)), valid=mae(yva, ridge_predict(m, Pv)), coef=float(np.abs(m[3]).max())))
    # knn on the two scaled features
    mu, sd = scaler_fit(trf); Ztr, Zva = scaler_apply(trf, mu, sd), scaler_apply(vaf, mu, sd)
    out["knn"] = [dict(k=k, valid=mae(yva, knn_fit_predict(Ztr, ytr, Zva, k))) for k in (1, 3, 20)]
    q = Zva[0]; dist = np.sqrt(((Ztr - q) ** 2).sum(axis=1)); idx = np.argsort(dist, kind="stable")[:3]
    out["knn_example"] = dict(query_row=int(va.record_id.iloc[0]), actual=float(yva[0]), neighbours=[int(tr.record_id.iloc[i]) for i in idx],
                              neighbour_targets=[float(ytr[i]) for i in idx], prediction=float(np.mean(ytr[idx])), idx=[int(i) for i in idx])
    out["candidates"] = [("baseline", o["reg"]["baseline"]["mae"]), ("straight line, two inputs", o["reg"]["linear"]["mae"]),
                         ("decision tree, depth 4", o["reg"]["tree"]["mae"]), (f"ridge, degree {degree}, alpha 1", out["ridge_rows"][1]["valid"]),
                         ("nearest neighbours, k = 3", out["knn"][1]["valid"])]
    return out


def ridge_fit_raw(X, y, alpha):
    """Ridge on columns that are already scaled: returns (intercept, coef)."""
    X = np.asarray(X, float); xm = X.mean(axis=0); ym = float(np.mean(y)); Z = X - xm
    w = np.linalg.solve(Z.T @ Z + alpha * np.eye(Z.shape[1]), Z.T @ (np.asarray(y, float) - ym))
    return ym - xm @ w, w
