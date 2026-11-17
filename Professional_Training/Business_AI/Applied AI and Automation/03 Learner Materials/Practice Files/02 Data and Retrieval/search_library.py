"""Local search over the fictional knowledge library. Three different things are shown.

  lexical  Word matching (BM25). Counts shared words. No meaning. Always available.
  lsa      A CLASSICAL vector method that needs no download: each chunk becomes a
           vector (TF-IDF reduced by singular value decomposition, "latent semantic
           analysis"), the question becomes a vector in the same space, and chunks
           are ranked by cosine similarity. The space is learned from these 40
           documents only, so it captures only word patterns that co-occur here.
           It is real vector search and it is not a neural embedding model.
  sbert    A NEURAL embedding model (optional). Needs the sentence-transformers
           package and a model such as "all-MiniLM-L6-v2" (about 90 MB, downloaded
           once from Hugging Face on first use, then cached; runs on a laptop CPU).
           It was executed on the teaching Mac; its failures are preserved. See
           "Embedding Demo Run Sheet.txt" for the historical comparison and the
           repaired reviewed_retrieval.py workflow. Install: pip install sentence-transformers
  hybrid   Reciprocal-rank fusion of lexical and the chosen vector method.

Preprocessing (a choice made in this script, not a property of lexical search)
  Words are lower-cased and split on letters and digits. A short list of function
  words (the, of, to ...) is removed. Negation words (not, no, nor, never, without,
  unless, neither) and modal verbs (may, must, shall) are KEPT by default.
  Option --drop-negations removes the negation words as well, which reproduces the
  list this script used in its first version. Some widely used default English stop
  lists remove "no" and "not" and some do not, so check the list in any real search
  system. Keeping the words does not make word matching understand negation: the
  sentences "consent is required" and "consent is not required" still share almost
  every word. Run negation_check.py to see the effect for each method.

Access is applied BEFORE ranking: only chunks from matters the user may read
(--user-matters) and, unless --historical is given, only current versions.
User identity is stipulated for the class; a real system must enforce it.
This script does not generate answers. It shows which passages would be handed to
a language model.

Usage:
  python3 search_library.py "question" [--method lexical|lsa|sbert|hybrid]
          [--user-matters M-01] [--historical] [--top 5] [--min-score 0.1]
          [--chunk-words 120] [--drop-negations] [--model all-MiniLM-L6-v2]
"""
import sys, csv, re, json, math, argparse
from pathlib import Path
from collections import Counter
import numpy as np

ROOT = Path(__file__).resolve().parent
STOP_FUNCTION = set("a an and are as at be but by for from has have if in into is it its of on or that the their there this to was were will with which who whom what when where how do does".split())
NEGATIONS = {"not", "no", "nor", "never", "without", "unless", "neither"}
STOP = set(STOP_FUNCTION)           # default: negations and modal verbs are kept
def set_drop_negations(flag):
    STOP.clear(); STOP.update(STOP_FUNCTION)
    if flag: STOP.update(NEGATIONS)

def tokens(text): return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP]

def load_chunks(user_matters, historical, chunk_words):
    with (ROOT / "Knowledge Library Manifest.csv").open(encoding="utf-8") as f:
        docs = list(csv.DictReader(f))
    chunks = []
    for d in docs:
        if d["matter"] not in user_matters: continue                   # access before ranking
        if d["status"] != "current" and not historical: continue
        text = (ROOT / d["file"]).read_text(encoding="utf-8")
        paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        cur, n = [], 0
        parts = []
        for p in paras:
            w = len(p.split())
            if cur and n + w > chunk_words: parts.append("\n\n".join(cur)); cur, n = [], 0
            cur.append(p); n += w
        if cur: parts.append("\n\n".join(cur))
        for i, t in enumerate(parts, 1):
            chunks.append(dict(doc=d["document_id"], version=d["version"], matter=d["matter"], status=d["status"],
                               title=d["title"], chunk=i, text=t, id=f"{d['document_id']} {d['version']} #{i}"))
    return chunks

def bm25(chunks, q, k1=1.5, b=0.75):
    docs = [tokens(c["title"] + " " + c["text"]) for c in chunks]
    N = len(docs); avg = sum(map(len, docs)) / max(1, N)
    df = Counter(w for d in docs for w in set(d))
    qs = tokens(q); scores = []
    for d in docs:
        tf = Counter(d); s = 0.0
        for w in qs:
            if w in tf:
                idf = math.log(1 + (N - df[w] + 0.5) / (df[w] + 0.5))
                s += idf * tf[w] * (k1 + 1) / (tf[w] + k1 * (1 - b + b * len(d) / avg))
        scores.append(s)
    return np.array(scores)

def lsa(chunks, q, dims=12):
    docs = [tokens(c["title"] + " " + c["text"]) for c in chunks]
    vocab = sorted({w for d in docs for w in d}); ix = {w: i for i, w in enumerate(vocab)}
    N = len(docs); df = Counter(w for d in docs for w in set(d))
    idf = np.array([math.log((1 + N) / (1 + df[w])) + 1 for w in vocab])
    M = np.zeros((N, len(vocab)))
    for i, d in enumerate(docs):
        for w, c in Counter(d).items(): M[i, ix[w]] = (1 + math.log(c)) * idf[ix[w]]
    M /= np.linalg.norm(M, axis=1, keepdims=True) + 1e-12
    U, S, Vt = np.linalg.svd(M, full_matrices=False)
    k = min(dims, len(S)); V = Vt[:k].T
    D = M @ V; D /= np.linalg.norm(D, axis=1, keepdims=True) + 1e-12
    qv = np.zeros(len(vocab))
    for w, c in Counter(tokens(q)).items():
        if w in ix: qv[ix[w]] = (1 + math.log(c)) * idf[ix[w]]
    if not qv.any(): return np.zeros(N)
    qd = (qv / np.linalg.norm(qv)) @ V
    n = np.linalg.norm(qd)
    return D @ (qd / n) if n else np.zeros(N)

MODEL_NAME = "all-MiniLM-L6-v2"
def sbert(chunks, q):
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        sys.exit("sbert needs: pip install sentence-transformers (model downloads on first use). See Embedding Demo Run Sheet.txt for the executed baseline and repaired route.")
    m = SentenceTransformer(MODEL_NAME)
    E = m.encode([c["title"] + ". " + c["text"] for c in chunks], normalize_embeddings=True)
    e = m.encode([q], normalize_embeddings=True)[0]
    return E @ e

def rrf(rank_lists, k=60):
    out = Counter()
    for order in rank_lists:
        for r, i in enumerate(order): out[i] += 1.0 / (k + r + 1)
    return out

def search(q, method="lexical", user_matters=("M-01",), historical=False, top=5, min_score=None, chunk_words=120, vector="lsa"):
    chunks = load_chunks(set(user_matters), historical, chunk_words)
    if not chunks: return dict(method=method, results=[], note="no permitted chunks")
    vec = (lambda: lsa(chunks, q)) if vector == "lsa" else (lambda: sbert(chunks, q))
    if method == "lexical": s = bm25(chunks, q); label = "lexical BM25 word matching (no vectors)"
    elif method == "lsa": s = lsa(chunks, q); label = "classical vector search: TF-IDF + SVD (LSA), cosine similarity, space learned from this library only (not a neural embedding)"
    elif method == "sbert": s = sbert(chunks, q); label = f"vector search: neural embedding model {MODEL_NAME}, cosine similarity"
    else:
        a, b = bm25(chunks, q), vec()
        f = rrf([list(np.argsort(-a)), list(np.argsort(-b))]); s = np.array([f[i] for i in range(len(chunks))])
        label = f"hybrid: reciprocal-rank fusion of BM25 and {vector} vectors"
    order = np.argsort(-s)[:top]
    res = [dict(rank=r + 1, score=round(float(s[i]), 4), chunk=chunks[i]["id"], matter=chunks[i]["matter"], status=chunks[i]["status"],
                title=chunks[i]["title"], excerpt=" ".join(chunks[i]["text"].split())[:260], text=chunks[i]["text"]) for r, i in enumerate(order) if s[i] > 0]
    note = None
    if min_score is not None:
        kept = [r for r in res if r["score"] >= min_score]
        note = "nothing reached the minimum score: report a gap instead of answering" if not kept else None
        res = kept
    return dict(method=label, user_matters=list(user_matters), historical_versions_included=historical, chunk_words=chunk_words, results=res, note=note)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("query"); p.add_argument("--method", choices=["lexical", "lsa", "sbert", "hybrid"], default="lexical")
    p.add_argument("--vector", choices=["lsa", "sbert"], default="lsa", help="vector method used inside hybrid")
    p.add_argument("--drop-negations", action="store_true", help="also remove not/no/nor/never/without/unless/neither from the index and the query")
    p.add_argument("--model", default=MODEL_NAME, help="sentence-transformers model name or local folder for the sbert method")
    p.add_argument("--user-matters", default="M-01"); p.add_argument("--historical", action="store_true")
    p.add_argument("--top", type=int, default=5); p.add_argument("--min-score", type=float); p.add_argument("--chunk-words", type=int, default=120)
    a = p.parse_args()
    set_drop_negations(a.drop_negations); MODEL_NAME = a.model
    print(json.dumps(search(a.query, a.method, a.user_matters.split(","), a.historical, a.top, a.min_score, a.chunk_words, a.vector), indent=1))
