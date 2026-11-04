"""Author g's verification harness for Sessions 13 and 14: python3 ref/verify_g.py 13 14
Runs the learner and solution notebooks with the NumPy scikit-learn stand-in PLUS small extra stand-ins written here (not shared files):
  statsmodels.formula.api.ols (plain 'y ~ a + b + c' formulas, params, rsquared, rsquared_adj, conf_int)
  sklearn.dummy.DummyClassifier(strategy='most_frequent'), train_test_split(stratify=...), sklearn.metrics.* extras
It checks the NumPy/pandas cells and the use of the library calls. It does not prove what the real libraries print."""
import importlib.util
import shutil
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
sys.path.insert(0, str(BUILD / 'kit'))
import nb as NB  # noqa: E402

TMP = Path('/tmp/ref_g')
if TMP.exists():
    shutil.rmtree(TMP)
shutil.copytree(HERE, TMP, ignore=shutil.ignore_patterns('__pycache__', 'verify_g.py'))
(TMP / 'statsmodels' / 'formula').mkdir(parents=True)
(TMP / 'statsmodels' / '__init__.py').write_text('')
(TMP / 'statsmodels' / 'formula' / '__init__.py').write_text('')
(TMP / 'statsmodels' / 'formula' / 'api.py').write_text('''
import numpy as np, pandas as pd
class _R:
    pass
def ols(formula, data):
    y, rhs = [s.strip() for s in formula.split('~')]
    terms = [t.strip() for t in rhs.split('+')]
    class M:
        def fit(self):
            X = np.column_stack([np.ones(len(data))] + [data[t].values.astype(float) for t in terms])
            yy = data[y].values.astype(float)
            b = np.linalg.lstsq(X, yy, rcond=None)[0]
            e = yy - X @ b
            n, k = X.shape
            r = _R()
            names = ['Intercept'] + terms
            r.params = pd.Series(b, index=names)
            r.rsquared = 1 - (e ** 2).sum() / ((yy - yy.mean()) ** 2).sum()
            r.rsquared_adj = 1 - (1 - r.rsquared) * (n - 1) / (n - k)
            s2 = (e ** 2).sum() / (n - k)
            se = np.sqrt(s2 * np.diag(np.linalg.inv(X.T @ X)))
            r.conf_int = lambda: pd.DataFrame({0: b - 1.9628 * se, 1: b + 1.9628 * se}, index=names)
            return r
    return M()
''')
sk = TMP / 'sklearn'
(sk / 'dummy.py').write_text((sk / 'dummy.py').read_text() + '''
class DummyClassifier:
    def __init__(self, strategy='prior', random_state=None): self.strategy = strategy
    def fit(self, X, y):
        v, c = np.unique(np.asarray(y), return_counts=True); self.c_ = v[np.argmax(c)]; return self
    def predict(self, X): return np.full(len(X), self.c_)
    def score(self, X, y): return float(np.mean(self.predict(X) == np.asarray(y)))
''')
ms = (sk / 'model_selection.py').read_text()
ms = ms.replace("def train_test_split(*arrays, test_size=0.25, random_state=None, shuffle=True):\n    n = len(arrays[0]); idx = np.arange(n)\n    if shuffle: np.random.RandomState(random_state).shuffle(idx)\n    nt = int(np.ceil(test_size * n)); te, tr = idx[:nt], idx[nt:]",
                "def train_test_split(*arrays, test_size=0.25, random_state=None, shuffle=True, stratify=None):\n    n = len(arrays[0]); idx = np.arange(n)\n    if stratify is not None:\n        rng = np.random.RandomState(random_state); st = np.asarray(stratify); te = []\n        for cl in np.unique(st):\n            ii = np.where(st == cl)[0]; rng.shuffle(ii); te += list(ii[:int(round(len(ii) * test_size))])\n        te = np.array(sorted(te)); tr = np.setdiff1d(idx, te)\n    else:\n        if shuffle: np.random.RandomState(random_state).shuffle(idx)\n        nt = int(np.ceil(test_size * n)); te, tr = idx[:nt], idx[nt:]")
assert 'stratify=None' in ms
(sk / 'model_selection.py').write_text(ms)
NB.REF = TMP


def main(nums):
    data = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'data'
    out = BUILD.parent.parent / '04 Facilitator Materials' / 'Lab Solutions'
    lrn = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'notebooks'
    for n in nums:
        sol = sorted(out.glob(f'Session {n:02d} - *(solution).ipynb'))[0]
        lea = sorted(lrn.glob(f'Session {n:02d} - *.ipynb'))[0]
        for label, p in (('solution', sol), ('learner', lea)):
            rs = NB.run(p, data)
            errs = [(i, e.strip().splitlines()[-1]) for i, _, e in rs if e]
            txt = '\n'.join(o for _, o, _ in rs)
            last = [l for l in txt.splitlines() if 'checks pass' in l][-1:]
            nots = [l for l in txt.splitlines() if l.startswith('NOT YET')]
            print(n, label, last, 'errors', len(errs), 'NOT YET', len(nots))
            if label == 'solution':
                for e in errs:
                    print('   ', e)
                for l in nots:
                    print('   ', l)
                print(txt[-1500:])


if __name__ == '__main__':
    main([int(a) for a in sys.argv[1:]])
