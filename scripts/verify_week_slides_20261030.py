"""Run the code shown on the Week 8 to 12 slides, in slide order, and compare each printed result with the
output panel on the slide.

With scikit-learn installed (the real check, run it on your Mac):
    python3 scripts/verify_week_slides_20261030.py
Without scikit-learn, a small NumPy stand-in (built from week_reference_numpy) is used. That checks the code
flow, names and output formatting only. It cannot confirm that real scikit-learn prints the same numbers.

Options: --dir DIR  --weeks 8 9 10 11 12  --cohorts CML3111 ...  --tolerance 0.005
"""
import argparse, contextlib, copy, io, os, re, shutil, sys, tempfile, traceback, types
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import pandas as pd
from pptx import Presentation
import week_reference_numpy as R
from patch_weeks8b_12_20261030 import deck_name, first_title, DECKS, p8


# ------------------------------------------------------------------ NumPy stand-in for scikit-learn
def install_shim():
    def arr(X): return X.to_numpy(float) if hasattr(X, "to_numpy") else np.asarray(X, float)

    class _Est:
        def get_params(self): return {}

    class DummyRegressor(_Est):
        def __init__(self, strategy="mean"): pass
        def fit(self, X, y): self.m = float(np.mean(np.asarray(y, float))); return self
        def predict(self, X): return np.full(len(X), self.m)

    class LinearRegression(_Est):
        def fit(self, X, y):
            A = arr(X); assert not np.isnan(A).any(), "Input X contains NaN. LinearRegression does not accept missing values."
            self.intercept_, self.coef_ = R.linreg_fit(A, np.asarray(y, float)); return self
        def predict(self, X): return R.linreg_predict(self.intercept_, self.coef_, arr(X))

    class DecisionTreeRegressor(_Est):
        def __init__(self, max_depth=None, random_state=None): self.d = max_depth if max_depth is not None else 99; self.rs = random_state if random_state is not None else 0
        def fit(self, X, y):
            A = arr(X); assert not np.isnan(A).any(), "shim: tree input has NaN"
            self.t = R.tree_reg_fit(A, np.asarray(y, float), self.d, self.rs); return self
        def predict(self, X): return R.tree_predict(self.t, arr(X))

    class DecisionTreeClassifier(_Est):
        def __init__(self, max_depth=None, random_state=None): self.d = max_depth if max_depth is not None else 99; self.rs = random_state if random_state is not None else 0
        def fit(self, X, y): self.t = R.tree_clf_fit(arr(X), np.asarray(y, int), self.d, self.rs); return self
        def predict_proba(self, X): p = R.tree_predict(self.t, arr(X)); return np.column_stack([1 - p, p])
        def predict(self, X): return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)

    class LogisticRegression(_Est):
        def __init__(self, **kw): pass
        def fit(self, X, y): self.b, self.w = R.logreg_fit(arr(X), np.asarray(y, int)); return self
        def predict_proba(self, X): p = R.logreg_proba(self.b, self.w, arr(X)); return np.column_stack([1 - p, p])
        def predict(self, X): return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)

    class SimpleImputer(_Est):
        def __init__(self, strategy="median"): pass
        def fit(self, X, y=None): self.med = np.nanmedian(arr(X), axis=0); return self
        def transform(self, X): A = arr(X).copy(); i = np.where(np.isnan(A)); A[i] = np.take(self.med, i[1]); return A
        def fit_transform(self, X, y=None): return self.fit(X).transform(X)

    class StandardScaler(_Est):
        def fit(self, X, y=None): self.mu, self.sd = R.scaler_fit(arr(X)); return self
        def transform(self, X): return R.scaler_apply(arr(X), self.mu, self.sd)
        def fit_transform(self, X, y=None): return self.fit(X).transform(X)

    class Pipeline(_Est):
        def __init__(self, steps): self.steps = steps
        def fit(self, X, y):
            for s in self.steps[:-1]: X = s.fit_transform(X, y)
            self.steps[-1].fit(X, y); return self
        def _t(self, X):
            for s in self.steps[:-1]: X = s.transform(X)
            return X
        def predict(self, X): return self.steps[-1].predict(self._t(X))
        def predict_proba(self, X): return self.steps[-1].predict_proba(self._t(X))

    class PolynomialFeatures(_Est):
        def __init__(self, degree=2, include_bias=True): self.d = degree
        def fit(self, X, y=None): return self
        def transform(self, X): return R.poly_cols(arr(X), self.d)
        def fit_transform(self, X, y=None): return self.transform(X)

    class Ridge(_Est):
        def __init__(self, alpha=1.0): self.alpha = alpha
        def fit(self, X, y): self.m = R.ridge_fit_raw(arr(X), np.asarray(y, float), self.alpha); self.coef_ = self.m[1]; return self
        def predict(self, X): return self.m[0] + arr(X) @ self.m[1]

    class KNeighborsRegressor(_Est):
        def __init__(self, n_neighbors=5): self.k = n_neighbors
        def fit(self, X, y): self.X, self.y = arr(X), np.asarray(y, float); return self
        def predict(self, X): return R.knn_fit_predict(self.X, self.y, arr(X), self.k)

    def make_pipeline(*steps): return Pipeline(list(steps))

    def mean_absolute_error(a, p): return R.mae(a, p)

    class GroupKFold:
        def __init__(self, n_splits=5): self.n = n_splits
        def split(self, X, y=None, groups=None):
            g = np.asarray(groups); uniq, inv = np.unique(g, return_inverse=True); counts = np.bincount(inv)
            order = np.argsort(counts)[::-1]; load = np.zeros(self.n); assign = np.zeros(len(uniq), int)
            for gi in order:
                f = int(np.argmin(load)); load[f] += counts[gi]; assign[gi] = f
            fold_of = assign[inv]
            for f in range(self.n):
                yield np.where(fold_of != f)[0], np.where(fold_of == f)[0]

    def cross_val_score(model, X, y, groups=None, cv=None, scoring=None):
        out = []
        for tr, te in cv.split(X, y, groups):
            m = copy.deepcopy(model); Xi = X.iloc if hasattr(X, "iloc") else X; yi = y.iloc if hasattr(y, "iloc") else y
            m.fit(Xi[tr], yi[tr]); err = R.mae(np.asarray(yi[te]), m.predict(Xi[te])); out.append(-err if scoring == "neg_mean_absolute_error" else err)
        return np.array(out)

    mods = {"sklearn": {}, "sklearn.dummy": dict(DummyRegressor=DummyRegressor), "sklearn.linear_model": dict(LinearRegression=LinearRegression, LogisticRegression=LogisticRegression, Ridge=Ridge),
            "sklearn.neighbors": dict(KNeighborsRegressor=KNeighborsRegressor),
            "sklearn.tree": dict(DecisionTreeRegressor=DecisionTreeRegressor, DecisionTreeClassifier=DecisionTreeClassifier),
            "sklearn.impute": dict(SimpleImputer=SimpleImputer), "sklearn.preprocessing": dict(StandardScaler=StandardScaler, PolynomialFeatures=PolynomialFeatures),
            "sklearn.pipeline": dict(make_pipeline=make_pipeline, Pipeline=Pipeline), "sklearn.metrics": dict(mean_absolute_error=mean_absolute_error),
            "sklearn.model_selection": dict(GroupKFold=GroupKFold, cross_val_score=cross_val_score)}
    for name, attrs in mods.items():
        m = types.ModuleType(name); m.__dict__.update(attrs); sys.modules[name] = m
    sys.modules["sklearn"].__version__ = "stand-in"


# ------------------------------------------------------------------ slide code extraction
def courier_blocks(slide):
    blocks = []
    for sh in slide.shapes:
        if sh.has_text_frame and sh.text_frame.paragraphs and any(r.font.name == "Courier New" for p in sh.text_frame.paragraphs for r in p.runs):
            blocks.append("\n".join("".join(r.text for r in p.runs) for p in sh.text_frame.paragraphs))
    return blocks


def norm(txt): return "\n".join(l.rstrip() for l in txt.strip().splitlines())


def close(a, b, tol):
    ta, tb = re.split(r"(-?\d+\.\d+|-?\d+)", a), re.split(r"(-?\d+\.\d+|-?\d+)", b)
    if len(ta) != len(tb): return False
    for x, y in zip(ta, tb):
        if re.fullmatch(r"-?\d+\.\d+|-?\d+", x or "") and re.fullmatch(r"-?\d+\.\d+|-?\d+", y or ""):
            if abs(float(x) - float(y)) > tol: return False
        elif x != y: return False
    return True


def run_deck(path, code, week, tol):
    prs = Presentation(str(path)); ns = {"__name__": "__main__"}; problems = []; checked = 0; ran = 0; buf = []
    tmp = Path(tempfile.mkdtemp()); old = os.getcwd(); os.chdir(tmp)
    shutil.copy(DECKS.parent / "assessment_banks" / "W08" / code / "A" / "engineering_data.csv", "engineering_data.csv")
    shutil.copy(DECKS.parent / "assessment_banks" / "W09" / code / "A" / "classification_case.csv", "classification_case.csv")
    try:
        for i, s in enumerate(prs.slides, 1):
            blocks = courier_blocks(s)
            if not blocks: continue
            title = first_title(s); src = blocks[0]; expect = blocks[1] if len(blocks) > 1 else None
            m = re.search(r"\((\d+)/(\d+)\)\s*$", title)
            if m:
                buf.append(src)
                if int(m.group(1)) < int(m.group(2)): continue
                src = "\n".join(buf); buf = []
            out = io.StringIO()
            try:
                with contextlib.redirect_stdout(out): exec(compile(src, f"slide{i}", "exec"), ns)
                ran += 1
            except Exception as e:
                problems.append((i, title, f"{type(e).__name__}: {str(e)[:90]}")); continue
            if expect is not None:
                checked += 1
                got, want = norm(out.getvalue()), norm(expect)
                if want.startswith("(nothing printed)"): want = ""
                if want.startswith("(your "): continue
                if not (got == want or close(got, want, tol)):
                    problems.append((i, title, f"OUTPUT DIFFERS\n  slide : {want!r}\n  actual: {got!r}"))
    finally:
        os.chdir(old)
    return ran, checked, problems


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dir", default=None); ap.add_argument("--weeks", nargs="*", type=int, default=[8, 9, 10, 11, 12, 13])
    ap.add_argument("--cohorts", nargs="*", default=list(R.COHORT)); ap.add_argument("--tolerance", type=float, default=0.005); a = ap.parse_args()
    try:
        import sklearn; mode = f"real scikit-learn {sklearn.__version__}"
    except ImportError:
        install_shim(); mode = "NumPy stand-in (flow and formatting check only)"
    print("mode:", mode); d = Path(a.dir) if a.dir else DECKS; bad = 0
    for code in a.cohorts:
        for w in a.weeks:
            ran, checked, probs = run_deck(d / deck_name(code, w), code, w, a.tolerance)
            print(f"{code} W{w}: {ran} code cells run, {checked} outputs compared, {len(probs)} problems")
            for i, t, msg in probs: print(f"   slide {i} [{t[:55]}]: {msg}")
            bad += len(probs)
    print("TOTAL PROBLEMS:", bad); return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
