"""Facts about model results that the content authors may quote. Computed with numpy only (no scikit-learn here), so they are
approximate stand-ins: scikit-learn will give close but not identical numbers. Writes Content/_facts.json."""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd
HERE = Path(__file__).resolve().parent
import figs
from build_course import DATA
figs.DATA = str(DATA)
m = figs.loan_model(); y = m['y_te']; p = figs.sigmoid(m['s']); out = {}
def conf(th):
    pred = p >= th; tp = int((pred & (y == 1)).sum()); fp = int((pred & (y == 0)).sum()); fn = int((~pred & (y == 1)).sum()); tn = int((~pred & (y == 0)).sum())
    return dict(threshold=th, tp=tp, fp=fp, fn=fn, tn=tn, accuracy=round((tp + tn) / len(y), 3), precision=round(tp / max(tp + fp, 1), 3), recall=round(tp / max(tp + fn, 1), 3))
out['loan_model_numpy_logistic'] = dict(note='75/25 random split with seed 1, standardised features, plain logistic regression. scikit-learn LogisticRegression will be close, not identical.', n_test=int(len(y)), defaults_in_test=int(y.sum()),
    auc_honest=round(figs.auc(y, m['s']), 3), auc_with_leaked_collection_calls=round(figs.auc(y, m['sl']), 3), confusion=[conf(t) for t in (0.5, 0.3, 0.2, 0.15)],
    accuracy_if_always_no=round(float(1 - y.mean()), 3))
g = figs.rfm().copy(); X = np.c_[np.log1p(g.recency), np.log1p(g.frequency), np.log1p(g.spend)]; Z = (X - X.mean(0)) / X.std(0); lab, C, _ = figs.kmeans(Z, 4, seed=3); g['seg'] = lab
prof = g.groupby('seg').agg(customers=('customer_id', 'count'), mean_recency_days=('recency', 'mean'), mean_orders=('frequency', 'mean'), mean_spend_ugx=('spend', 'mean')).round(0)
out['customer_segments_numpy_kmeans_k4'] = dict(note='RFM on log scale, standardised, seed 3. scikit-learn KMeans gives similar groups; their numbering may differ.', segments=prof.reset_index().to_dict('records'), customers=int(len(g)))
(HERE.parent / 'Content' / '_facts.json').write_text(json.dumps(out, indent=1), encoding='utf-8'); print(json.dumps(out, indent=1)[:2500])
