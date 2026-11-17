"""Numbers for Session 18 (finding structure without labels), author i. Everything on a slide, in a note or in a notebook check comes from facts().
RFM, the log transform, scaling, k-means (Lloyd's algorithm with a k-means++ start, best of 10 starts), PCA (singular value decomposition) and an isolation forest are written in NumPy
in ds_i_np.py. scikit-learn's KMeans, PCA and IsolationForest are not installed here: PCA must agree exactly (up to the sign of a component); KMeans agrees on inertia and closely on sizes;
IsolationForest uses random numbers, so its flagged list overlaps ours but is not identical, and the notebook checks allow for that."""
import hashlib
import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ds_i_np as NP  # noqa: E402

BUILD = HERE.parent
DATA = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'data'
K_RANGE = list(range(1, 9))


def compute():
    o = pd.read_csv(DATA / 'orders.csv', parse_dates=['order_date'])
    cust = pd.read_csv(DATA / 'customers.csv')
    F = dict(orders=len(o), walkin=int(o.customer_id.isna().sum()), customers_file=len(cust))
    loyal = o.dropna(subset=['customer_id'])
    F['loyal_orders'] = len(loyal)
    end = o.order_date.max()
    F['end'] = str(end.date()); F['first'] = str(o.order_date.min().date())
    g = loyal.groupby('customer_id').agg(last_order=('order_date', 'max'), frequency=('order_id', 'count'), spend=('order_value_ugx', 'sum'))
    g['recency'] = (end - g['last_order']).dt.days
    rfm = g[['recency', 'frequency', 'spend']]
    F['n_cust'] = len(rfm)
    F['never_ordered'] = int((~cust.customer_id.isin(rfm.index)).sum())
    F['rfm_head'] = [[str(i)] + [int(v) for v in r] for i, r in rfm.head(3).iterrows()]
    F['rfm_stats'] = {c: dict(mean=float(rfm[c].mean()), median=float(rfm[c].median()), sd=float(rfm[c].std()), min=float(rfm[c].min()), max=float(rfm[c].max()), skew=float(rfm[c].skew())) for c in rfm}
    logged = np.log1p(rfm.astype(float))
    F['skew_log'] = {c: float(logged[c].skew()) for c in logged}
    F['c1'] = dict(spend=float(rfm.loc['C0001', 'spend']), logspend=float(logged.loc['C0001', 'spend']))
    L = logged.to_numpy()
    mu, sd = L.mean(0), L.std(0)
    Z = (L - mu) / sd
    F['log_mean'] = dict(zip(rfm.columns, mu.tolist())); F['log_sd'] = dict(zip(rfm.columns, sd.tolist()))
    F['c1']['z_spend'] = float((F['c1']['logspend'] - mu[2]) / sd[2])
    F['raw_sd'] = {c: float(rfm[c].std()) for c in rfm}
    F['scaled_check'] = dict(mean=np.abs(Z.mean(0)).max().item(), sd=Z.std(0).tolist())
    # elbow
    F['inertia'] = {}
    for k in K_RANGE:
        F['inertia'][k] = NP.kmeans(Z, k, 42, 10)[0]
    inertia, lab, C, it = NP.kmeans(Z, 4, 42, 10)
    # the lowest inertia over 60 further starts: is the 10-start answer the global best?
    rr = [NP.kmeans_once(Z, 4, np.random.default_rng(900 + s)) for s in range(60)]
    runs = [r[0] for r in rr]
    sz = np.array([sorted(np.bincount(r[1], minlength=4).tolist()) for r in rr])
    F['k4_size_range'] = [[int(a), int(b)] for a, b in zip(sz.min(0), sz.max(0))]
    F['k4_inertia_best10'] = inertia; F['k4_inertia_min60'] = float(min(runs)); F['k4_inertia_max60'] = float(max(runs))
    F['k4_runs_within'] = int(sum(r < inertia + 1.0 for r in runs))
    # name segments in a fixed order: by mean spend, highest first
    spend_by = [rfm.spend.to_numpy()[lab == j].mean() for j in range(4)]
    order = np.argsort(spend_by)[::-1]
    remap = {int(old): new for new, old in enumerate(order)}
    seg = np.array([remap[int(v)] for v in lab])
    F['seg'] = seg
    F['centroids_scaled'] = np.array([C[o_] for o_ in order])
    df = rfm.assign(segment=seg)
    prof = df.groupby('segment').agg(customers=('spend', 'size'), recency=('recency', 'mean'), orders=('frequency', 'mean'), spend=('spend', 'mean'), total=('spend', 'sum'))
    prof['share_customers'] = prof.customers / prof.customers.sum() * 100
    prof['share_spend'] = prof.total / prof.total.sum() * 100
    F['profile'] = prof.reset_index().to_dict('records')
    F['spend_total'] = float(prof.total.sum())
    inertia3, lab3, _, _ = NP.kmeans(Z, 3, 42, 10)
    F['k3_sizes'] = sorted(int(v) for v in np.bincount(lab3))
    F['k4_inertia'] = inertia
    F['k4_sizes_sorted'] = sorted(int(v) for v in np.bincount(lab))
    # PCA on the scaled, logged RFM
    ev, ratio, comps, scores = NP.pca(Z)
    F['pca'] = dict(ev=ev.tolist(), ratio=ratio.tolist(), comps=comps.tolist(), scores=scores[:, :2].tolist())
    # the percentile rule on all orders
    p99 = float(np.percentile(o.order_value_ugx, 99))
    big = o[o.order_value_ugx > p99]
    F['rule'] = dict(p99=p99, n=len(big), median_all=float(o.order_value_ugx.median()), median_big=float(big.order_value_ugx.median()), max=int(o.order_value_ugx.max()),
                     walkin=int(big.customer_id.isna().sum()), share=len(big) / len(o) * 100, share_value=float(big.order_value_ugx.sum() / o.order_value_ugx.sum() * 100))
    # an isolation forest on the 2,499 customers (scaled, logged RFM), flag the top 1 percent
    sc = NP.isolation_scores(Z, 100, 256, 42)
    nflag = int(np.floor(0.01 * (len(Z) - 1))) + 1       # scikit-learn flags the scores below the 1st percentile of the scores
    flag = np.argsort(-sc)[:nflag]
    F['iso'] = dict(n=nflag, rec=rfm.recency.to_numpy()[flag].tolist(), freq=rfm.frequency.to_numpy()[flag].tolist(), spend=rfm.spend.to_numpy()[flag].tolist(),
                    med_rec=float(np.median(rfm.recency.to_numpy()[flag])), med_freq=float(np.median(rfm.frequency.to_numpy()[flag])), med_spend=float(np.median(rfm.spend.to_numpy()[flag])),
                    top_ids=[str(rfm.index[i]) for i in flag[:3]], top_rows=[[int(rfm.recency.iloc[i]), int(rfm.frequency.iloc[i]), int(rfm.spend.iloc[i])] for i in flag[:3]])
    sc2 = NP.isolation_scores(Z, 100, 256, 7)
    flag2 = set(np.argsort(-sc2)[:nflag].tolist())
    F['iso']['overlap_other_seed'] = len(flag2 & set(flag.tolist()))
    # a hand example of the four moves: 10 real customers, two variables (scaled logged recency and spend), k = 2
    rng = np.random.default_rng(21)
    pick = rng.choice(len(Z), 10, replace=False)
    P = Z[pick][:, [0, 2]]
    cent = P[[int(np.argmin(P[:, 0])), int(np.argmax(P[:, 0]))]].copy()      # start: the most recent and the least recent of the ten
    moves = []
    labs_prev = None
    for step in range(6):
        d = ((P[:, None, :] - cent[None]) ** 2).sum(2); lb = d.argmin(1)
        moves.append(dict(centres=cent.copy().tolist(), labels=lb.tolist(), inertia=float(d[np.arange(len(P)), lb].sum())))
        if labs_prev is not None and (lb == labs_prev).all():
            break
        labs_prev = lb
        cent = np.array([P[lb == j].mean(0) for j in range(2)])
    F['moves'] = dict(points=P.tolist(), ids=[str(rfm.index[i]) for i in pick], steps=moves,
                      raw=[[int(rfm.recency.iloc[i]), int(rfm.frequency.iloc[i]), int(rfm.spend.iloc[i])] for i in pick])
    # 2D picture of every customer: log10 recency+1 and log10 spend
    F['scatter'] = dict(x=np.log10(rfm.recency.to_numpy() + 1).tolist(), y=np.log10(rfm.spend.to_numpy()).tolist(), seg=seg.tolist())
    # the orders behind customer C0001's three RFM numbers
    c1 = loyal[loyal.customer_id == 'C0001'].sort_values('order_date')
    F['c1_orders'] = [[str(d.date()), int(v)] for d, v in zip(c1.order_date, c1.order_value_ugx)]
    # isolation by random cuts: one odd customer and one typical customer among 40 (scaled logged recency and spend)
    rs = np.random.default_rng(8)
    top = int(flag[0])
    others = [i for i in rs.permutation(len(Z)) if i != top][:39]
    S = np.array([top] + others)
    Q = Z[S][:, [0, 2]]
    typ = int(np.argmin(np.abs(Q - np.median(Q, axis=0)).sum(1)))
    if typ == 0:
        typ = 1

    def cuts(target, seed):
        r = np.random.default_rng(seed); alive = np.ones(len(Q), bool); lo = Q.min(0) - 0.15; hi = Q.max(0) + 0.15; out = []
        while alive.sum() > 1:
            a = int(r.integers(2)); v = Q[alive, a]
            if v.min() == v.max():
                break
            c = float(r.uniform(v.min(), v.max()))
            out.append(dict(axis=a, at=c, lo=lo.tolist(), hi=hi.tolist()))
            if Q[target, a] < c:
                alive &= Q[:, a] < c; hi[a] = c
            else:
                alive &= Q[:, a] >= c; lo[a] = c
        return out
    reps = 300
    odd_n = [len(cuts(0, 100 + s)) for s in range(reps)]
    typ_n = [len(cuts(typ, 100 + s)) for s in range(reps)]
    F['isodemo'] = dict(points=Q.tolist(), odd=0, typical=typ, odd_cuts=cuts(0, 100), typ_cuts=cuts(typ, 100), odd_mean=float(np.mean(odd_n)), typ_mean=float(np.mean(typ_n)), reps=reps,
                        odd_row=[int(rfm.recency.iloc[S[0]]), int(rfm.frequency.iloc[S[0]]), int(rfm.spend.iloc[S[0]])], typ_row=[int(rfm.recency.iloc[S[typ]]), int(rfm.frequency.iloc[S[typ]]), int(rfm.spend.iloc[S[typ]])])
    F['Z'] = Z
    F['rfm_np'] = rfm.to_numpy()
    F['ids'] = [str(i) for i in rfm.index]
    return F


def _key():
    h = hashlib.sha1()
    for p in (HERE / 'ds_i_np.py', Path(__file__)):
        h.update(p.read_bytes())
    h.update(str((DATA / 'orders.csv').stat().st_size).encode())
    return h.hexdigest()


_MEM = {}


def facts():
    if 'F' in _MEM:
        return _MEM['F']
    cdir = HERE / '_cache'
    cdir.mkdir(exist_ok=True)
    cp = cdir / 's18_facts.pkl'
    key = _key()
    if cp.exists():
        d = pickle.loads(cp.read_bytes())
        if d.get('key') == key:
            _MEM['F'] = d['F']
            return d['F']
    F = compute()
    cp.write_bytes(pickle.dumps(dict(key=key, F=F)))
    _MEM['F'] = F
    return F


if __name__ == '__main__':
    import time
    t = time.time()
    F = facts()
    print('seconds', round(time.time() - t))
    for k, v in F.items():
        if k in ('Z', 'rfm_np', 'ids', 'seg', 'scatter'):
            continue
        s = str(v)
        print(k, s[:700])
