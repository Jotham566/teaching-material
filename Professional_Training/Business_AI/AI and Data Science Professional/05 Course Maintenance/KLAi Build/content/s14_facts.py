"""Numbers for Session 14 (the machine learning workflow). Since the review fix of 4 Nov 2026 every number comes from content/loans_canon.py, the one shared recipe for the loans
(8,000 rows, stratified split with seed 42: 6,000 train and 2,000 test, 251 test defaults, 12 numeric features). The tree is the port of the scikit-learn CART replica in loans_canon.
These are NumPy replica numbers: re-run the notebook on real scikit-learn in Colab before the course starts. Ten other seeds give the range a learner may see if the library breaks a tie differently."""
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

BUILD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BUILD / 'content'))
import loans_canon as C  # noqa: E402

DATA = C.DATA
FEATURES = list(C.FEATURES)


def _conf(y, pred):
    c = C.confusion(y, pred)
    return c['tn'], c['fp'], c['fn'], c['tp']


@lru_cache(maxsize=None)
def facts():
    raw = pd.read_csv(DATA / 'loans.csv')
    CF = C.facts()
    L = C.prepare()
    F = dict(raw=raw, canon=CF)
    n = len(raw)
    F.update(n=n, cols=raw.shape[1], dflt=int(raw.default.sum()), rate=float(raw.default.mean()), repaid=int((raw.default == 0).sum()))
    bad = (raw.age < 18) | (raw.age > 100)
    F['bad_n'] = int(bad.sum())
    F['bad_ages'] = sorted(int(a) for a in raw.age[bad])
    F['age_med'] = int(raw.age[~bad].median())
    F['age_min_ok'], F['age_max_ok'] = int(raw.age[~bad].min()), int(raw.age[~bad].max())
    F['miss_n'] = int(raw.monthly_income_ugx.isna().sum())
    F['miss_pct'] = F['miss_n'] / n * 100
    F['inc_med'] = float(raw.monthly_income_ugx.median())
    F['known_n'] = n - F['miss_n']
    F['miss_rate'] = float(raw.default[raw.monthly_income_ugx.isna()].mean())
    F['known_rate'] = float(raw.default[raw.monthly_income_ugx.notna()].mean())
    F['L'] = L
    F['ratio_med'] = float(L.instalment_to_income.median())
    F['ratio_max'] = float(L.instalment_to_income.max())
    q = pd.qcut(L.instalment_to_income, 4)
    F['q_rates'] = [float(v) for v in L.groupby(q, observed=True).default.mean()]
    F['q_edges'] = [float(i.right) for i in sorted(q.cat.categories)]
    F['q_n'] = [int(v) for v in L.groupby(q, observed=True).size()]
    hand = L.instalment_to_income > 0.6
    F['hand_flag'], F['hand_rate'] = int(hand.sum()), float(L.default[hand].mean())
    F['hand_caught'] = int(L.default[hand].sum())
    r0 = raw.iloc[0]
    F['ex'] = dict(id=str(r0.loan_id), loan=int(r0.loan_amount_ugx), term=int(r0.term_months), inc=float(r0.monthly_income_ugx), ratio=float(L.instalment_to_income.iloc[0]))
    F['calls_default'] = float((raw.collection_calls[raw.default == 1] > 0).mean())
    F['calls_repaid'] = float((raw.collection_calls[raw.default == 0] > 0).mean())
    X, y = L[FEATURES], L.default
    F['X'], F['y'] = X, y
    yv = y.to_numpy()
    tr, te = C.split_indices(yv)
    F.update(n_tr=len(tr), n_te=len(te), d_tr=int(yv[tr].sum()), d_te=int(yv[te].sum()))
    F['rate_tr'], F['rate_te'] = F['d_tr'] / len(tr), F['d_te'] / len(te)
    F['base_acc'] = float((yv[te] == 0).mean())
    F['base_correct'] = int((yv[te] == 0).sum())
    Xn = X.to_numpy(float)
    tree = C.fit_tree(Xn[tr], yv[tr], 3)
    pred = C.tree_predict(tree, Xn[te])
    tn, fp, fn, tp = _conf(yv[te], pred)
    F.update(tn=tn, fp=fp, fn=fn, tp=tp)
    F['acc'] = (tp + tn) / len(te)
    F['recall'] = tp / (tp + fn)
    F['precision'] = tp / (tp + fp)
    F['root_feat'] = FEATURES[tree[1]]
    F['root_thr'] = float(tree[2])
    F['tree_auc'] = C.auc_rank(yv[te], C.tree_proba(tree, Xn[te]))
    F['depth'] = {}
    for d in (1, 6):
        t_ = C.fit_tree(Xn[tr], yv[tr], d)
        pd_ = C.tree_predict(t_, Xn[te])
        a, _, b, c_ = _conf(yv[te], pd_)[0], 0, _conf(yv[te], pd_)[2], _conf(yv[te], pd_)[3]
        tn_, fp_, fn_, tp_ = _conf(yv[te], pd_)
        F['depth'][d] = ((tp_ + tn_) / len(te), tp_ / (tp_ + fn_), tp_)
    accs, recs, tps = [], [], []
    for sd in range(1, 11):
        a_, b_ = C.split_indices(yv, random_state=sd)
        t2 = C.fit_tree(Xn[a_], yv[a_], 3)
        pp = C.tree_predict(t2, Xn[b_])
        tn2, fp2, fn2, tp2 = _conf(yv[b_], pp)
        accs.append((tp2 + tn2) / len(b_))
        tps.append(tp2)
        recs.append(tp2 / (tp2 + fn2))
    F.update(acc_lo=float(min(accs)), acc_hi=float(max(accs)), rec_lo=float(min(recs)), rec_hi=float(max(recs)), tp_lo=min(tps), tp_hi=max(tps))
    hp = (L.instalment_to_income.to_numpy()[te] > 0.6).astype(int)
    h_tn, h_fp, h_fn, h_tp = _conf(yv[te], hp)
    F.update(h_tn=h_tn, h_fp=h_fp, h_fn=h_fn, h_tp=h_tp, h_acc=(h_tp + h_tn) / len(te))
    F['h_recall'] = h_tp / (h_tp + h_fn)
    # the median income computed on the 6,000 training rows only (the leak-free value) against the median on all 8,000 loans (what the prepared file uses)
    F['inc_med_train'] = float(raw.monthly_income_ugx.iloc[tr].median())
    F['age_med_train'] = float(raw.age.iloc[tr][~bad.iloc[tr]].median())
    # picture rows
    F['pic'] = raw.iloc[[0, 1, 2, 3]]
    miss_ids = raw.index[raw.monthly_income_ugx.isna()][:2]
    F['imp_rows'] = [raw.index[0], miss_ids[0], raw.index[1], miss_ids[1]]
    F['rule_threshold'] = CF['rule_threshold']
    return F


if __name__ == '__main__':
    F = facts()
    for k, v in F.items():
        if k not in ('raw', 'L', 'X', 'y', 'pic', 'canon'):
            print(k, v)
