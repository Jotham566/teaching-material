"""Session 2 demonstration script (the lecturer can re-run it live).  Run from this folder:  python learn_run.py
Needs python 3, numpy, scikit-learn.  Reads
  expenses_fictional.csv   FICTIONAL expense claims made by make_expenses.py (fixed seed 2026)
  customer_messages.csv + customer_messages_key.csv   the 40 labelled NVF customer messages (copied here from the Practice Files and Answer Keys folders)
Prints every number used on the Session 2 slides and saves results_s02.json.
"""
import csv, json, warnings
from pathlib import Path
import numpy as np
import sklearn
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold, cross_val_score, cross_val_predict, LeaveOneOut

warnings.filterwarnings('ignore')
HERE = Path(__file__).resolve().parent
print('scikit-learn', sklearn.__version__, 'numpy', np.__version__)
out = {}

# ============================== A. fictional expense claims
rows = list(csv.DictReader(open(HERE / 'expenses_fictional.csv')))
X = np.array([[int(r['amount_ugx']) / 1000, int(r['receipt_attached']), int(r['days_to_file'])] for r in rows])   # amount in thousands of UGX
y = np.array([r['outcome'] for r in rows])
names = ['amount (UGX thousands)', 'receipt attached', 'days to file']
print('\n=== A. FICTIONAL expense claims:', len(rows), 'rows,', int((y == 'queried').sum()), 'queried,', int((y == 'paid').sum()), 'paid')
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=20, random_state=0)
tree_cv = {}
for d in (1, 2, 3, 4, None):
    sc = cross_val_score(DecisionTreeClassifier(max_depth=d, random_state=0), X, y, cv=cv)
    tree_cv[str(d)] = [float(sc.mean()), float(sc.std())]
    print(f'tree depth {d}: cross-validated accuracy {sc.mean():.3f} (spread {sc.std():.3f})')
deep = DecisionTreeClassifier(random_state=0).fit(X, y)
print('unlimited tree: accuracy on the claims it trained on', round(float(deep.score(X, y)), 3), ' leaves', deep.get_n_leaves())
tree = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X, y)
print('\nTree used on the slides (depth 3, trained on all 240):\n' + export_text(tree, feature_names=names, show_weights=True))
print('accuracy on its own training claims', round(float(tree.score(X, y)), 3))

def node(i):
    t = tree.tree_
    cls = list(tree.classes_)
    val = t.value[i][0]
    d = dict(n=int(t.n_node_samples[i]), counts={cls[k]: int(round(val[k] * t.n_node_samples[i] / val.sum())) for k in range(len(cls))})
    if t.children_left[i] != -1:
        d.update(feature=names[t.feature[i]], thr=float(t.threshold[i]), left=node(t.children_left[i]), right=node(t.children_right[i]))
    else:
        d['leaf'] = cls[int(np.argmax(val))]
    return d
out['tree'] = node(0)
out['tree_cv'] = tree_cv
out['tree_train_acc'] = float(tree.score(X, y))
out['deep_train_acc'] = float(deep.score(X, y))

has = X[:, 1] == 1
print('\nSplit on receipt:  with receipt', int(has.sum()), 'claims,', int((y[has] == 'queried').sum()), 'queried;  without receipt', int((~has).sum()), 'claims,', int((y[~has] == 'queried').sum()), 'queried')
out['split_receipt'] = dict(with_n=int(has.sum()), with_q=int((y[has] == 'queried').sum()), without_n=int((~has).sum()), without_q=int((y[~has] == 'queried').sum()), all_n=len(y), all_q=int((y == 'queried').sum()))

# nearest neighbours: claims with a receipt, two measurements: log10(amount) and days to file, both put on the same scale
sub = np.where(has)[0]
Xs = np.c_[np.log10(X[sub, 0] * 1000), X[sub, 2]]
ys = y[sub]
sc2 = StandardScaler().fit(Xs)
Z = sc2.transform(Xs)
q_amount, q_days = 450_000, 31
q = sc2.transform([[np.log10(q_amount), q_days]])
dist = np.sqrt(((Z - q) ** 2).sum(1))
nn = np.argsort(dist)[:5]
print('\nNew claim (receipt attached): UGX', f'{q_amount:,}', 'filed after', q_days, 'days. Five nearest past claims:')
nbrs = []
for j in nn:
    print(f'  {rows[sub[j]]["claim_id"]}  UGX {int(X[sub[j], 0] * 1000):>9,}  {int(X[sub[j], 2]):>2} days  {ys[j]:8s} distance {dist[j]:.2f}')
    nbrs.append(dict(id=rows[sub[j]]['claim_id'], amount=int(X[sub[j], 0] * 1000), days=int(X[sub[j], 2]), outcome=str(ys[j]), dist=float(dist[j])))
vote = {k: int(sum(ys[nn] == k)) for k in ('queried', 'paid')}
print('vote among 5 neighbours:', vote)
knn_sub = cross_val_score(make_pipeline(StandardScaler(), KNeighborsClassifier(5)), Xs, ys, cv=cv)
print('kNN (k=5) on these receipt claims, cross-validated:', round(float(knn_sub.mean()), 3))
out['knn_demo'] = dict(query=[q_amount, q_days], neighbours=nbrs, vote=vote, points=[[float(a), float(b), str(c)] for (a, b), c in zip(np.c_[X[sub, 0] * 1000, X[sub, 2]], ys)],
                       nn_idx=[int(i) for i in nn], cv=float(knn_sub.mean()))

# the scaling lesson: all three measurements, k = 5
raw = cross_val_score(KNeighborsClassifier(5), X, y, cv=cv).mean()
scaled = cross_val_score(make_pipeline(StandardScaler(), KNeighborsClassifier(5)), X, y, cv=cv).mean()
print(f'\nkNN k=5 on all three measurements: raw numbers {raw:.3f}; put on one scale first {scaled:.3f}')
out['scaling'] = dict(raw=float(raw), scaled=float(scaled))
for k in (1, 3, 5, 9):
    print('  k =', k, 'scaled', round(float(cross_val_score(make_pipeline(StandardScaler(), KNeighborsClassifier(k)), X, y, cv=cv).mean()), 3))
out['majority_expense'] = float(max((y == 'queried').mean(), (y == 'paid').mean()))
print('always say the commonest outcome:', round(out['majority_expense'], 3))

# ============================== B. the 40 NVF customer messages
msgs = list(csv.DictReader(open(HERE / 'customer_messages.csv')))
key = {r['id']: r for r in csv.DictReader(open(HERE / 'customer_messages_key.csv'))}
texts = [m['text'] for m in msgs]
ids = [m['id'] for m in msgs]
lab = np.array([key[i]['true_category'] for i in ids])
tricky = np.array([key[i]['tricky'] == 'yes' for i in ids])
classes = sorted(set(lab))
print('\n=== B. 40 NVF customer messages:', {c: int((lab == c).sum()) for c in classes}, ' tricky:', int(tricky.sum()))
out['class_counts'] = {c: int((lab == c).sum()) for c in classes}

def keyword_rule(t):                      # a simple rule written by the course author for this comparison
    t = t.lower()
    if any(w in t for w in ('damaged', 'wet', 'torn', 'late', 'wrong', 'missing', 'refund', 'complain', 'bad', 'angry', 'leak', 'short')):
        return 'complaint'
    if any(w in t for w in ('paid', 'sent ugx', 'momo', 'payment', 'invoice', 'receipt', 'airtel money', 'balance')):
        return 'payment'
    if any(w in t for w in ('send me', 'please send', 'order', 'bags', 'deliver', 'jerrycan', 'need')):
        return 'order'
    return 'other'
kr = np.array([keyword_rule(t) for t in texts])
kr_acc = float((kr == lab).mean())
print('keyword rule written by the author:', int((kr == lab).sum()), 'of 40 =', round(kr_acc, 3))
maj = float(max((lab == c).mean() for c in classes))
print('always say the commonest category:', maj)

cv2 = RepeatedStratifiedKFold(n_splits=5, n_repeats=20, random_state=0)
res = {}
def cvrun(name, model):
    s = cross_val_score(model, texts, lab, cv=cv2)
    res[name] = dict(mean=float(s.mean()), sd=float(s.std()), lo=float(s.min()), hi=float(s.max()))
    print(f'{name:34s} cross-validated accuracy {s.mean():.3f}  spread (sd) {s.std():.3f}  worst fold {s.min():.2f}  best fold {s.max():.2f}')
from sklearn.pipeline import Pipeline
cvrun('decision tree on words', Pipeline([('v', CountVectorizer(binary=True, min_df=2)), ('m', DecisionTreeClassifier(random_state=0))]))
cvrun('decision tree depth 3 on words', Pipeline([('v', CountVectorizer(binary=True, min_df=2)), ('m', DecisionTreeClassifier(max_depth=3, random_state=0))]))
for k in (1, 3, 5):
    cvrun(f'nearest neighbours k={k} (TF-IDF)', Pipeline([('v', TfidfVectorizer(sublinear_tf=True)), ('m', KNeighborsClassifier(k, metric='cosine'))]))
res['keyword rule (no training)'] = dict(mean=kr_acc, sd=0.0, lo=kr_acc, hi=kr_acc)
res['always the commonest'] = dict(mean=maj, sd=0.0, lo=maj, hi=maj)
out['cv_messages'] = res

# who gets it wrong: leave-one-out for 3 nearest neighbours
loo_knn = cross_val_predict(Pipeline([('v', TfidfVectorizer(sublinear_tf=True)), ('m', KNeighborsClassifier(3, metric='cosine'))]), texts, lab, cv=LeaveOneOut())
loo_tree = cross_val_predict(Pipeline([('v', CountVectorizer(binary=True, min_df=2)), ('m', DecisionTreeClassifier(random_state=0))]), texts, lab, cv=LeaveOneOut())
print('\nLeave-one-out (each message predicted by a model that never saw it): knn3', round(float((loo_knn == lab).mean()), 3), ' tree', round(float((loo_tree == lab).mean()), 3))
print('tricky messages right by knn3:', int((loo_knn[tricky] == lab[tricky]).sum()), 'of', int(tricky.sum()), '; plain messages right:', int((loo_knn[~tricky] == lab[~tricky]).sum()), 'of', int((~tricky).sum()))
print('tricky messages right by tree:', int((loo_tree[tricky] == lab[tricky]).sum()), 'of', int(tricky.sum()), '; plain messages right:', int((loo_tree[~tricky] == lab[~tricky]).sum()), 'of', int((~tricky).sum()))
wr = []
for i in range(40):
    if loo_knn[i] != lab[i]:
        wr.append(dict(id=ids[i], key=str(lab[i]), knn=str(loo_knn[i]), tree=str(loo_tree[i]), tricky=bool(tricky[i]), text=texts[i]))
        print(f'  wrong (knn3): {ids[i]} key {lab[i]} said {loo_knn[i]} (tree said {loo_tree[i]}) tricky={tricky[i]}: {texts[i][:90]}')
out['loo'] = dict(knn=float((loo_knn == lab).mean()), tree=float((loo_tree == lab).mean()), wrong_knn=wr,
                  knn_tricky=[int((loo_knn[tricky] == lab[tricky]).sum()), int(tricky.sum())], knn_plain=[int((loo_knn[~tricky] == lab[~tricky]).sum()), int((~tricky).sum())])

# precedent: nearest three other messages for a chosen message
vec = TfidfVectorizer(sublinear_tf=True).fit(texts)
M = vec.transform(texts)
sim = (M @ M.T).toarray()
np.fill_diagonal(sim, -1)
precs = []
for qid in ('M30', 'M03'):                 # one message with close precedents, one without
    qi = ids.index(qid)
    nb = np.argsort(-sim[qi])[:3]
    print('\nPrecedent for', ids[qi], '[' + lab[qi] + ']', '-', texts[qi])
    prec = dict(query=dict(id=ids[qi], text=texts[qi], key=str(lab[qi])), neighbours=[])
    for j in nb:
        print(f'  {ids[j]} similarity {sim[qi, j]:.2f} [{lab[j]}] {texts[j][:100]}')
        prec['neighbours'].append(dict(id=ids[j], sim=float(sim[qi, j]), cat=str(lab[j]), text=texts[j]))
    precs.append(prec)
out['precedents'] = precs
print('Words the vectoriser counts: vocabulary size', len(vec.vocabulary_))

# the tree on words, trained on all 40 (first questions only)
cvz = CountVectorizer(binary=True, min_df=2)
Wm = cvz.fit_transform(texts)
tw = DecisionTreeClassifier(max_depth=3, random_state=0).fit(Wm, lab)
print('\nTree on words (depth 3, all 40 messages):\n' + export_text(tw, feature_names=list(cvz.get_feature_names_out()), show_weights=True))
print('vocabulary size (words used at least twice):', Wm.shape[1], '  accuracy on the 40 it trained on:', round(float(tw.score(Wm, lab)), 3))
out['words_tree_train_acc'] = float(tw.score(Wm, lab))

# ============================== C. five fold scores of ONE 5-fold split (added 11 November 2026 for the worked cross-validation slide)
# The first 5 of the 100 tests above are one complete 5-fold split (repeat 1 of RepeatedStratifiedKFold, random_state=0).
first = list(cv.split(X, y))[:5]
folds = {}
for name, d in (('depth 3', 3), ('unlimited', None)):
    rowsf = []
    for f, (tr, te) in enumerate(first, 1):
        m = DecisionTreeClassifier(max_depth=d, random_state=0).fit(X[tr], y[tr])
        ok_te = int((m.predict(X[te]) == y[te]).sum())
        ok_tr = int((m.predict(X[tr]) == y[tr]).sum())
        rowsf.append(dict(fold=f, test_n=len(te), test_right=ok_te, test_acc=ok_te / len(te), train_n=len(tr), train_right=ok_tr, train_acc=ok_tr / len(tr)))
    mean = sum(r['test_acc'] for r in rowsf) / 5
    folds[name] = dict(folds=rowsf, mean=mean, worst=min(r['test_acc'] for r in rowsf), best=max(r['test_acc'] for r in rowsf))
    print(f'\nClaims, tree {name}, one 5-fold split (repeat 1):')
    for r in rowsf:
        print(f"  fold {r['fold']}: test {r['test_right']} of {r['test_n']} = {r['test_acc']:.4f}   training {r['train_right']} of {r['train_n']} = {r['train_acc']:.4f}")
    print(f"  mean of the 5 test scores {mean:.4f}; worst {folds[name]['worst']:.4f}; best {folds[name]['best']:.4f}")
out['claims_one_split'] = folds
first_m = list(cv2.split(texts, lab))[:5]
rm = []
for f, (tr, te) in enumerate(first_m, 1):
    pm = Pipeline([('v', CountVectorizer(binary=True, min_df=2)), ('m', DecisionTreeClassifier(max_depth=3, random_state=0))])
    pm.fit([texts[i] for i in tr], lab[tr])
    ok = int((pm.predict([texts[i] for i in te]) == lab[te]).sum())
    rm.append(dict(fold=f, test_n=len(te), test_right=ok, test_acc=ok / len(te)))
print('\n40 messages, tree depth 3 on words, one 5-fold split (repeat 1):')
for r in rm:
    print(f"  fold {r['fold']}: {r['test_right']} of {r['test_n']} = {r['test_acc']:.3f}")
print(f"  mean {sum(r['test_acc'] for r in rm) / 5:.3f}")
out['messages_one_split'] = rm
# min-max scaling (the method taught by hand on the slides) for the same k = 5 model on the claims
from sklearn.preprocessing import MinMaxScaler
mm = cross_val_score(make_pipeline(MinMaxScaler(), KNeighborsClassifier(5)), X, y, cv=cv).mean()
print(f'\nkNN k=5 on all three measurements, min-max scaling first: {mm:.3f}  (standard scaling above: {scaled:.3f}; raw: {raw:.3f})')
print('feature ranges in the claims: amount (UGX thousands)', X[:, 0].min(), 'to', X[:, 0].max(), '; days to file', X[:, 2].min(), 'to', X[:, 2].max())
out['scaling_minmax'] = dict(minmax=float(mm), amount_min=float(X[:, 0].min()), amount_max=float(X[:, 0].max()), days_min=float(X[:, 2].min()), days_max=float(X[:, 2].max()))
json.dump(out, open(HERE / 'results_s02.json', 'w'), indent=1)
