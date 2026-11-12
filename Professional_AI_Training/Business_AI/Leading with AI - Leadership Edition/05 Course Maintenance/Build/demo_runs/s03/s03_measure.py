"""Session 3 demonstration: measuring a model on a fictional late-payment scoring dataset (Nile Valley Foods Ltd, all data invented).

Run:  python demo_runs/s03/s03_measure.py        (from the Build folder; writes demo_runs/s03/results.json and invoices.csv)
Task: for each invoice sent to a shop, predict whether it will be paid late (more than 30 days after the due date).
Fixed seeds: dataset seed 2026, split seed 42. Tool: Python, scikit-learn, numpy.
"""
import csv, json, sys
from pathlib import Path
import numpy as np
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix

OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(2026)
N = 3000
amount = np.round(rng.lognormal(mean=13.0, sigma=0.7, size=N) / 1000) * 1000      # invoice size, UGX
years = np.round(rng.gamma(2.0, 2.0, size=N), 1)                                    # years as a customer
late12 = rng.poisson(0.7, size=N)                                                   # late payments in the last 12 months
days_since = rng.integers(1, 120, size=N)                                           # days since the shop's last order
momo = rng.integers(0, 2, size=N)                                                   # pays by mobile money (1) or cash/bank (0)
util = np.clip(rng.normal(0.55, 0.25, size=N), 0, 1.2)                              # share of credit limit used
z = -4.1 + 0.75 * late12 + 1.0 * (amount > 700000) + 1.5 * (util > 0.75) - 0.12 * years - 0.4 * momo + 0.012 * days_since
p = 1 / (1 + np.exp(-z))
late = (rng.random(N) < p).astype(int)
X = np.column_stack([amount, years, late12, days_since, momo, util])
names = ['invoice_ugx', 'years_as_customer', 'late_last_12m', 'days_since_last_order', 'pays_by_momo', 'credit_used']
with open(OUT / 'invoices.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['id'] + names + ['paid_late'])
    for i in range(N):
        w.writerow([f'INV{i+1:04d}'] + [X[i, 0], X[i, 1], X[i, 2], X[i, 3], X[i, 4], round(X[i, 5], 3), late[i]])
idx = np.arange(N)
Xtr, Xte, ytr, yte, itr, ite = train_test_split(X, late, idx, test_size=0.3, random_state=42, stratify=late)
res = dict(tool=f'Python {sys.version.split()[0]}, scikit-learn {sklearn.__version__}, numpy {np.__version__}', run_date='2026-11-06', n=N,
           n_train=len(ytr), n_test=len(yte), late_rate_all=float(late.mean()), late_test=int(yte.sum()), on_time_test=int((1 - yte).sum()))

# baseline 1: always say "on time" (never flag)
res['always_no'] = dict(accuracy=float(((yte == 0).mean())), recall=0.0, flagged=0)
# baseline 2: a plain rule - flag if the shop paid late at least once in the last 12 months
rule = (Xte[:, 2] >= 1).astype(int)
tn, fp, fn, tp = confusion_matrix(yte, rule).ravel()
res['rule'] = dict(desc='flag if at least one late payment in the last 12 months', tp=int(tp), fp=int(fp), fn=int(fn), tn=int(tn),
                   accuracy=float((tp + tn) / len(yte)), precision=float(tp / (tp + fp)), recall=float(tp / (tp + fn)))

# the model: logistic regression (scores between 0 and 1)
m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
m.fit(Xtr, ytr)
score = m.predict_proba(Xte)[:, 1]
res['auc_logistic'] = float(roc_auc_score(yte, score))
fpr, tpr, thr = roc_curve(yte, score)
res['roc_points'] = [[float(a), float(b)] for a, b in zip(fpr[::3], tpr[::3])]
CHASE, MISS = 20000, 300000   # ASSUMED costs for the lesson, UGX
rows = []
for t in [0.50, 0.30, 0.20, 0.15, 0.10, 0.05]:
    pred = (score >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(yte, pred).ravel()
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn)
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    rows.append(dict(threshold=t, flagged=int(tp + fp), tp=int(tp), fp=int(fp), fn=int(fn), tn=int(tn), accuracy=float((tp + tn) / len(yte)),
                     precision=float(prec), recall=float(rec), f1=float(f1), cost_ugx=int(CHASE * (tp + fp) + MISS * fn)))
res['threshold_table'] = rows
bins = np.linspace(0, 1, 21)
hl, _ = np.histogram(score[yte == 1], bins=bins); ho, _ = np.histogram(score[yte == 0], bins=bins)
res['hist'] = dict(bins=[round(float(b), 2) for b in bins], late=[int(x) for x in hl], on_time=[int(x) for x in ho])
res['roc_full'] = [[round(float(a), 4), round(float(b), 4)] for a, b in zip(fpr, tpr)]
res['assumed_costs'] = dict(chase_a_flagged_invoice_ugx=CHASE, a_missed_late_invoice_ugx=MISS)
res['cost_never_flag_ugx'] = int(MISS * yte.sum())

# memorising: an unlimited decision tree against a small tree
tree_deep = DecisionTreeClassifier(random_state=0).fit(Xtr, ytr)
tree_small = DecisionTreeClassifier(max_depth=3, random_state=0).fit(Xtr, ytr)
def accs(mod):
    return dict(train_acc=float(mod.score(Xtr, ytr)), test_acc=float(mod.score(Xte, yte)))
def rec_prec(mod):
    pr = mod.predict(Xte); tn, fp, fn, tp = confusion_matrix(yte, pr).ravel()
    return dict(test_recall=float(tp / (tp + fn)), test_precision=float(tp / (tp + fp)) if tp + fp else 0.0)
res['deep_tree'] = dict(depth=int(tree_deep.get_depth()), leaves=int(tree_deep.get_n_leaves()), **accs(tree_deep), **rec_prec(tree_deep))
res['small_tree'] = dict(depth=3, leaves=int(tree_small.get_n_leaves()), **accs(tree_small), **rec_prec(tree_small))
res['logistic'] = dict(train_acc=float(m.score(Xtr, ytr)), test_acc=float(m.score(Xte, yte)))
res['depth_curve'] = []
for d in [1, 2, 3, 4, 6, 8, 12, None]:
    t_ = DecisionTreeClassifier(max_depth=d, random_state=0).fit(Xtr, ytr)
    res['depth_curve'].append(dict(depth=d if d else int(t_.get_depth()), train_acc=float(t_.score(Xtr, ytr)), test_acc=float(t_.score(Xte, yte))))

# 20 cases for the paper exercise: 6 really late and 14 on time, drawn from the test set at model threshold 0.20.
# The draw seed is the first seed from 7 upward that gives tp=3, fp=2, fn=3, tn=12 (so that every box of the table is used and precision differs from recall).
for seed in range(7, 500):
    r2 = np.random.default_rng(seed)
    late_ids = r2.choice(np.where(yte == 1)[0], 6, replace=False)
    ok_ids = r2.choice(np.where(yte == 0)[0], 14, replace=False)
    fl = lambda ids: int((score[ids] >= 0.20).sum())
    if fl(late_ids) == 3 and fl(ok_ids) == 2:
        break
res['cases20_seed'] = seed
pick = np.concatenate([late_ids, ok_ids]); r2.shuffle(pick)
cases = []
for k, j in enumerate(pick, 1):
    cases.append(dict(case=k, invoice=f'INV{ite[j]+1:04d}', amount_ugx=int(Xte[j, 0]), late12=int(Xte[j, 2]), score=round(float(score[j]), 2),
                      flagged=int(score[j] >= 0.20), really_late=int(yte[j])))
res['cases20'] = cases
c = cases
tp = sum(1 for x in c if x['flagged'] and x['really_late']); fp = sum(1 for x in c if x['flagged'] and not x['really_late'])
fn = sum(1 for x in c if not x['flagged'] and x['really_late']); tn = sum(1 for x in c if not x['flagged'] and not x['really_late'])
res['cases20_answer'] = dict(tp=tp, fp=fp, fn=fn, tn=tn, precision=tp / (tp + fp) if tp + fp else None, recall=tp / (tp + fn))
(OUT / 'results.json').write_text(json.dumps(res, indent=1))
print(json.dumps({k: v for k, v in res.items() if k not in ('roc_points', 'cases20')}, indent=1))
for x in cases: print(x)
