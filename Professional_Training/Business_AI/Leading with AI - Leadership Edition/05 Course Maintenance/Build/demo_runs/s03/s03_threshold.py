"""Live demonstration helper for Session 3: move the threshold and watch the counts change.

Run from the Build folder:   python demo_runs/s03/s03_threshold.py 0.50 0.20 0.05
It rebuilds exactly the same fictional dataset and model as s03_measure.py (same seeds), then prints one line per threshold you type.
Assumed costs for the lesson: UGX 20,000 to chase a flag, UGX 300,000 for a missed late invoice. Change them with --chase and --miss."""
import argparse
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

ap = argparse.ArgumentParser()
ap.add_argument('thresholds', nargs='+', type=float)
ap.add_argument('--chase', type=int, default=20000)
ap.add_argument('--miss', type=int, default=300000)
a = ap.parse_args()

rng = np.random.default_rng(2026)
N = 3000
amount = np.round(rng.lognormal(mean=13.0, sigma=0.7, size=N) / 1000) * 1000
years = np.round(rng.gamma(2.0, 2.0, size=N), 1)
late12 = rng.poisson(0.7, size=N)
days_since = rng.integers(1, 120, size=N)
momo = rng.integers(0, 2, size=N)
util = np.clip(rng.normal(0.55, 0.25, size=N), 0, 1.2)
z = -4.1 + 0.75 * late12 + 1.0 * (amount > 700000) + 1.5 * (util > 0.75) - 0.12 * years - 0.4 * momo + 0.012 * days_since
late = (rng.random(N) < 1 / (1 + np.exp(-z))).astype(int)
X = np.column_stack([amount, years, late12, days_since, momo, util])
Xtr, Xte, ytr, yte = train_test_split(X, late, test_size=0.3, random_state=42, stratify=late)
m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(Xtr, ytr)
score = m.predict_proba(Xte)[:, 1]
print(f'{len(yte)} test invoices, {yte.sum()} really late.  Always saying "on time" scores {100 * (yte == 0).mean():.1f}% accuracy.')
print('threshold flagged caught false_alarms missed precision recall   F1  accuracy  cost_UGX')
for t in a.thresholds:
    pred = (score >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(yte, pred).ravel()
    pr = tp / (tp + fp) if tp + fp else float('nan')
    rc = tp / (tp + fn)
    f1 = 2 * pr * rc / (pr + rc) if tp else 0.0
    print(f'{t:9.2f} {tp + fp:7d} {tp:6d} {fp:12d} {fn:6d} {100 * pr:8.0f}% {100 * rc:5.0f}% {100 * f1:4.0f}% {100 * (tp + tn) / len(yte):8.1f}% {a.chase * (tp + fp) + a.miss * fn:>12,}')
