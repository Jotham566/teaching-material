"""Session 4 demonstration runs. Run from the Build folder:  python demo_runs/s04/s04_run.py
Writes demo_runs/s04/results.json. Tools: Python, scikit-learn (CountVectorizer, TfidfVectorizer, PCA, TSNE), sentence-transformers all-MiniLM-L6-v2 (downloads once)."""
import json, sys
from pathlib import Path
import numpy as np
import sklearn, sentence_transformers
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sentence_transformers import SentenceTransformer
sys.path.insert(0, str(Path(__file__).resolve().parent))
from s04_corpus import TEXTS, SKINS

OUT = Path(__file__).resolve().parent
B_ROOT = OUT.parent.parent.parent.parent   # the Executive Edition folder
res = dict(tool=f'Python {sys.version.split()[0]}, scikit-learn {sklearn.__version__}, sentence-transformers {sentence_transformers.__version__}, model all-MiniLM-L6-v2', run_date='2026-11-06')

# 1. bag of words and TF-IDF on four texts
docs = [t for _, t in TEXTS]
cv = CountVectorizer()
C = cv.fit_transform(docs).toarray()
res['bow'] = dict(ids=[i for i, _ in TEXTS], texts=docs, vocab=list(cv.get_feature_names_out()), counts=C.tolist())
tv = TfidfVectorizer()
T = tv.fit_transform(docs).toarray()
res['tfidf'] = dict(vocab=list(tv.get_feature_names_out()), weights=np.round(T, 3).tolist(), idf=dict(zip(tv.get_feature_names_out(), np.round(tv.idf_, 3).tolist())))

# 1b. TF-IDF on the 40 real (fictional) NVF customer messages
import csv
msgp = B_ROOT / '03 Learner Materials' / 'Practice Files' / '01 Case Company' / 'customer_messages.csv'
rows = list(csv.DictReader(open(msgp, encoding='utf-8')))
mt = [r['text'] for r in rows]; mid = [r['id'] for r in rows]
cv40 = CountVectorizer(); C40 = cv40.fit_transform(mt); voc = cv40.get_feature_names_out()
df = np.asarray((C40 > 0).sum(axis=0)).ravel()
dfd = {w: int(d) for w, d in zip(voc, df)}
tv40 = TfidfVectorizer(); T40 = tv40.fit_transform(mt).toarray(); voc40 = tv40.get_feature_names_out()
tops = {}
for k in ('M01', 'M03', 'M06', 'M08'):
    i = mid.index(k); o = np.argsort(-T40[i])[:5]
    tops[k] = dict(text=mt[i], top=[(voc40[j], round(float(T40[i, j]), 3), int(C40[i, j])) for j in o], n_words=int(C40[i].sum()))
i6 = mid.index('M06')
res['m06_words'] = sorted([dict(word=w, count=int(C40[i6, j]), in_messages=int(df[j]), simple=round(float(C40[i6, j]) * 40 / df[j], 1), real=round(float(T40[i6, j]), 3))
                           for j, w in enumerate(voc) if C40[i6, j] > 0], key=lambda d: -d['simple'])
res['tfidf40'] = dict(n_messages=len(mt), vocab_size=int(len(voc)), docfreq={w: dfd.get(w) for w in ['the', 'please', 'and', 'to', 'my', 'of', 'bags', 'sugar', 'invoice', 'jerrycans', 'maize', 'flour', 'late', 'damaged', 'wet', 'credit', 'mbale']},
                    idf={w: round(float(tv40.idf_[list(voc40).index(w)]), 3) for w in ['the', 'please', 'bags', 'invoice', 'jerrycans', 'sugar', 'wet']}, tops=tops)

# 2. embeddings for every skin
model = SentenceTransformer('all-MiniLM-L6-v2')
raw_model = SentenceTransformer(modules=[model[0], model[1]])   # same model, before its last step (length normalisation)
res['model_modules'] = [type(m).__name__ for m in model]
res['dim'] = int(model.get_sentence_embedding_dimension())

def dists(q, D):
    eu = np.linalg.norm(D - q, axis=1)
    ma = np.abs(D - q).sum(axis=1)
    dot = D @ q
    cos = dot / (np.linalg.norm(D, axis=1) * np.linalg.norm(q))
    return eu, ma, dot, cos

def rank(vals, high_is_close):
    o = np.argsort(-vals if high_is_close else vals)
    return [int(i) for i in o]

all_vec, all_lab, all_skin = [], [], []
res['skins'] = {}
for sk, d in SKINS.items():
    P = [f'{h}. {t}' if False else t for _, h, t in d['passages']]
    ids = [i for i, _, _ in d['passages']]
    heads = [h for _, h, _ in d['passages']]
    Q = [q for _, q, _ in d['queries']]
    E = model.encode(P, normalize_embeddings=False)
    EQ = model.encode(Q, normalize_embeddings=False)
    ER = raw_model.encode(P)
    EQR = raw_model.encode(Q)
    tf = TfidfVectorizer(stop_words='english').fit(P)
    TP = tf.transform(P); TQ = tf.transform(Q)
    qres = []
    for qi, (qid, qtext, want) in enumerate(d['queries']):
        eu, ma, dot, cos = dists(EQ[qi], E)
        eur, mar, dotr, cosr = dists(EQR[qi], ER)
        rk = {'cosine': rank(cos, True), 'euclidean': rank(eu, False), 'manhattan': rank(ma, False), 'dot': rank(dot, True)}
        rkr = {'cosine': rank(cosr, True), 'euclidean': rank(eur, False), 'manhattan': rank(mar, False), 'dot': rank(dotr, True)}
        kw = (TP @ TQ[qi].T).toarray().ravel()
        kw_top = [int(i) for i in np.argsort(-kw)[:3]] if kw.max() > 0 else []
        top3 = [dict(id=ids[i], head=heads[i], cosine=round(float(cos[i]), 3)) for i in rk['cosine'][:3]]
        qres.append(dict(qid=qid, query=qtext, want=want, top3=top3, hit_at1=bool(ids[rk['cosine'][0]] == want),
                         want_rank=int(rk['cosine'].index(ids.index(want)) + 1),
                         keyword_top=[dict(id=ids[i], head=heads[i], score=round(float(kw[i]), 3)) for i in kw_top],
                         keyword_hit_at1=bool(kw_top and ids[kw_top[0]] == want), keyword_matches=int((kw > 0).sum()),
                         dists_to_top_cos=dict(cos=round(float(cos[rk['cosine'][0]]), 3), dot=round(float(dot[rk['cosine'][0]]), 3), euclid=round(float(eu[rk['cosine'][0]]), 3),
                                               manhattan=round(float(ma[rk['cosine'][0]]), 2)),
                         norms=dict(query=round(float(np.linalg.norm(EQ[qi])), 4), passage_min=round(float(np.linalg.norm(E, axis=1).min()), 4), passage_max=round(float(np.linalg.norm(E, axis=1).max()), 4)),
                         same_top1=dict((k, bool(v[0] == rk['cosine'][0])) for k, v in rk.items()),
                         same_top3_set=dict((k, bool(set(v[:3]) == set(rk['cosine'][:3]))) for k, v in rk.items()),
                         raw_same_top1=dict((k, bool(v[0] == rkr['cosine'][0])) for k, v in rkr.items()),
                         raw_top1=dict((k, ids[v[0]]) for k, v in rkr.items()),
                         raw_norm_query=round(float(np.linalg.norm(EQR[qi])), 3), raw_norm_range=[round(float(np.linalg.norm(ER, axis=1).min()), 3), round(float(np.linalg.norm(ER, axis=1).max()), 3)]))
    res['skins'][sk] = dict(title=d['title'], ids=ids, heads=heads, queries=qres)
    all_vec += list(E) + list(EQ)
    all_lab += [(i, 'passage', h) for i, h in zip(ids, heads)] + [(q, 'query', t) for q, t, _ in d['queries']]
    all_skin += [sk] * (len(P) + len(Q))

V = np.array(all_vec)
pca = PCA(n_components=2, random_state=0).fit(V)
Z = pca.transform(V)
res['pca'] = dict(explained=[round(float(x), 4) for x in pca.explained_variance_ratio_], total=round(float(pca.explained_variance_ratio_.sum()), 4),
                  points=[dict(id=l[0], kind=l[1], label=l[2], skin=s, x=round(float(z[0]), 4), y=round(float(z[1]), 4)) for l, s, z in zip(all_lab, all_skin, Z)])
ts = TSNE(n_components=2, perplexity=8, random_state=0, init='pca').fit_transform(V)
res['tsne'] = dict(perplexity=8, points=[dict(id=l[0], x=round(float(z[0]), 3), y=round(float(z[1]), 3)) for l, z in zip(all_lab, ts)])

# 2b. the same query against two passages, four measures, on the raw (un-normalised) and the default (normalised) vectors
def pair(skin, qid, a, b):
    d = SKINS[skin]
    P = [t for _, _, t in d['passages']]; ids = [i for i, _, _ in d['passages']]
    qtext = [q for i, q, _ in d['queries'] if i == qid][0]
    out = dict(skin=skin, qid=qid, query=qtext)
    for tag, mdl in (('normalised', model), ('raw', raw_model)):
        E = mdl.encode(P); q = mdl.encode([qtext])[0]
        eu, ma, dot, cos = dists(q, E)
        out[tag] = {pid: dict(euclid=round(float(eu[ids.index(pid)]), 3), manhattan=round(float(ma[ids.index(pid)]), 2), dot=round(float(dot[ids.index(pid)]), 3),
                              cosine=round(float(cos[ids.index(pid)]), 3), length=round(float(np.linalg.norm(E[ids.index(pid)])), 3)) for pid in (a, b)}
        out[tag]['query_length'] = round(float(np.linalg.norm(q)), 3)
    return out
res['pair_examples'] = [pair('hr', 'Q10', 'H4', 'H5'), pair('finance', 'Q7', 'F5', 'F10'), pair('hr', 'Q12', 'H9', 'H1')]

# 2c. the first eight of the 384 numbers for one query and two clauses
cd = SKINS['contracts']
ctexts = [t for _, _, t in cd['passages']]; cids = [i for i, _, _ in cd['passages']]
vq = model.encode([cd['queries'][0][1]])[0]; vk1 = model.encode([ctexts[cids.index('K1')]])[0]; vk8 = model.encode([ctexts[cids.index('K8')]])[0]
res['sample_vectors'] = dict(query=cd['queries'][0][1], first8=dict(query=[round(float(x), 3) for x in vq[:8]], K1=[round(float(x), 3) for x in vk1[:8]], K8=[round(float(x), 3) for x in vk8[:8]]),
                             cos_q_K1=round(float(vq @ vk1), 3), cos_q_K8=round(float(vq @ vk8), 3), dim=int(len(vq)))

# 3. summary counts
qs = [q for s in res['skins'].values() for q in s['queries']]
res['summary'] = dict(n_queries=len(qs), emb_hit1=sum(q['hit_at1'] for q in qs), emb_hit3=sum(q['want_rank'] <= 3 for q in qs),
                      kw_hit1=sum(q['keyword_hit_at1'] for q in qs),
                      all_four_agree_top1=sum(all(q['same_top1'].values()) for q in qs),
                      euclid_same_top1=sum(q['same_top1']['euclidean'] for q in qs), manhattan_same_top1=sum(q['same_top1']['manhattan'] for q in qs),
                      dot_same_top1=sum(q['same_top1']['dot'] for q in qs),
                      raw_all_four_agree_top1=sum(all(q['raw_same_top1'].values()) for q in qs),
                      raw_euclid_same_top1=sum(q['raw_same_top1']['euclidean'] for q in qs), raw_dot_same_top1=sum(q['raw_same_top1']['dot'] for q in qs),
                      raw_manhattan_same_top1=sum(q['raw_same_top1']['manhattan'] for q in qs))
(OUT / 'results.json').write_text(json.dumps(res, indent=1))
print(json.dumps({k: v for k, v in res.items() if k not in ('pca', 'tsne')}, indent=1)[:9000])
