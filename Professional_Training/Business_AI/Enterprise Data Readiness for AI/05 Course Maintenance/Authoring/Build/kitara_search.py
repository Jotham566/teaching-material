"""Small search toolkit for the Kitara document set. numpy and pandas only.

Sessions 5 to 7 import this file and quote its numbers.

  chunk_text(text, size=200, overlap=40)   split text into word chunks that overlap
  extract_text(path, ocr=True)             text from a text PDF, scanned PDF, .docx or .txt
  load_corpus(data_dir)                    metadata plus extracted text for every document
  build_chunks(corpus)                     one row per chunk with doc_id, status and access groups
  BM25(chunks)                             keyword search (k1=1.5, b=0.75)
  MeaningScorer(chunks)                    stand-in for an embedding model: TF-IDF on words and
                                           character 4-grams, reduced to 64 dimensions with SVD
  rrf(rankings, k=60)                      reciprocal rank fusion of ranked lists
  user_can_see(doc_groups, user_groups)    the permission rule used in the pilot
  Searcher(chunks).search(query, method, k, user_groups, current_only)
                                           one call: method is 'bm25', 'meaning' or 'hybrid'; filters are applied before ranking
  recall_at_k, mrr                         scoring helpers

Example
  import kitara_search as ks
  corpus = ks.load_corpus('data')            # reads docs_metadata.csv and every file; OCR runs on the scanned PDFs
  chunks = ks.build_chunks(corpus)
  s = ks.Searcher(chunks)
  s.search('how long before I get my money', 'hybrid', k=5, user_groups='claims')[['doc_id', 'title', 'text']]

The meaning scorer is a teaching stand-in. A real embedding model understands more. It is here so that
every learner can run the same experiment with no download and no key.
"""
import re
from pathlib import Path
import numpy as np
import pandas as pd

STOPWORDS = set("""a an and are as at be been by can do does for from has have how i if in into is it its may me my of on or our
shall should so that the their them then there these they this to us was we were what when where which who will with would you your
must not no any all per than also but about""".split())
TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenise(text):
    """Lowercase, split on anything that is not a letter or digit, drop stopwords."""
    return [t for t in TOKEN_RE.findall(str(text).lower()) if t not in STOPWORDS]


def chunk_text(text, size=200, overlap=40):
    """Split text into chunks of about `size` words, each starting `size - overlap` words after the last."""
    words = str(text).split()
    if not words:
        return []
    step = size - overlap
    out = []
    start = 0
    while True:
        out.append(" ".join(words[start:start + size]))
        if start + size >= len(words):
            break
        start += step
    # a tiny tail adds nothing: fold it into the previous chunk
    if len(out) > 1 and len(out[-1].split()) <= overlap + 10:
        out.pop()
        out[-1] = " ".join(words[start - step:])
    return out


# ------------------------------------------------------------------ reading files
def _ocr_pdf(path, dpi=150):
    import subprocess, tempfile, glob, os
    import pytesseract
    from PIL import Image
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", str(path), os.path.join(td, "p")], check=True)
        pages = sorted(glob.glob(os.path.join(td, "p*.png")))
        return "\n".join(pytesseract.image_to_string(Image.open(p)) for p in pages)


def extract_text(path, ocr=True, ocr_cache=None):
    """Return the text of a document. A PDF with almost no text layer is treated as a scan and read with OCR."""
    path = Path(path)
    suf = path.suffix.lower()
    if suf == ".txt":
        return path.read_text(encoding="utf-8")
    if suf == ".docx":
        import docx
        d = docx.Document(str(path))
        parts = [p.text for p in d.paragraphs]
        for t in d.tables:
            for r in t.rows:
                parts.append(" | ".join(c.text for c in r.cells))
        return "\n".join(parts)
    if suf == ".pdf":
        from pypdf import PdfReader
        rd = PdfReader(str(path))
        text = "\n".join((pg.extract_text() or "") for pg in rd.pages)
        if len(text.strip()) < 40 * max(1, len(rd.pages)):
            if not ocr:
                return text
            if ocr_cache is not None and path.name in ocr_cache:
                return ocr_cache[path.name]
            return _ocr_pdf(path)
        return text
    raise ValueError(f"unsupported file type: {path}")


def load_corpus(data_dir, ocr=True, ocr_cache=None):
    """docs_metadata.csv plus a `text` column read from the files under data_dir/docs."""
    data_dir = Path(data_dir)
    meta = pd.read_csv(data_dir / "docs_metadata.csv", dtype=str, keep_default_na=False)
    meta["text"] = [extract_text(data_dir / "docs" / f, ocr=ocr, ocr_cache=ocr_cache) for f in meta.file]
    return meta


def build_chunks(corpus, size=200, overlap=40):
    rows = []
    for r in corpus.itertuples():
        for i, c in enumerate(chunk_text(r.text, size, overlap)):
            rows.append(dict(chunk_id=f"{r.doc_id}-{i + 1:02d}", doc_id=r.doc_id, chunk_no=i + 1, text=c, status=r.status,
                             access_groups=r.access_groups, sensitivity=r.sensitivity, language=r.language, title=r.title))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ keyword search
class BM25:
    def __init__(self, chunks, k1=1.5, b=0.75):
        self.k1, self.b = k1, b
        toks = [tokenise(t) for t in chunks.text]
        vocab = {}
        for t in toks:
            for w in t:
                vocab.setdefault(w, len(vocab))
        self.vocab = vocab
        n = len(toks)
        tf = np.zeros((n, len(vocab)), dtype=np.float32)
        for i, t in enumerate(toks):
            for w in t:
                tf[i, vocab[w]] += 1
        self.tf = tf
        self.dl = tf.sum(1)
        self.avg = self.dl.mean()
        df = (tf > 0).sum(0)
        self.idf = np.log(1 + (n - df + 0.5) / (df + 0.5)).astype(np.float32)

    def scores(self, query):
        s = np.zeros(self.tf.shape[0], dtype=np.float32)
        norm = self.k1 * (1 - self.b + self.b * self.dl / self.avg)
        for w in set(tokenise(query)):
            j = self.vocab.get(w)
            if j is None:
                continue
            f = self.tf[:, j]
            s += self.idf[j] * f * (self.k1 + 1) / (f + norm)
        return s


# ------------------------------------------------------------------ stand-in meaning search
def _char_ngrams(word, n=4):
    w = f" {word} "
    return [w[i:i + n] for i in range(max(1, len(w) - n + 1))]


class MeaningScorer:
    """TF-IDF on word unigrams and character 4-grams, reduced to `dims` dimensions with SVD."""

    def __init__(self, chunks, dims=64, w_word=1.0, w_char=1.0):
        self.dims = dims
        self.w_word, self.w_char = w_word, w_char
        docs = [tokenise(t) for t in chunks.text]
        self.wv, self.cv = {}, {}
        wc, cc = [], []
        for d in docs:
            w = {}
            c = {}
            for t in d:
                w[t] = w.get(t, 0) + 1
                for g in _char_ngrams(t):
                    c[g] = c.get(g, 0) + 1
            wc.append(w)
            cc.append(c)
        for w in wc:
            for t in w:
                self.wv.setdefault(t, len(self.wv))
        for c in cc:
            for t in c:
                self.cv.setdefault(t, len(self.cv))
        n = len(docs)
        self.Xw = self._mat(wc, self.wv, n)
        self.Xc = self._mat(cc, self.cv, n)
        self.idf_w = np.log((1 + n) / (1 + (self.Xw > 0).sum(0))) + 1
        self.idf_c = np.log((1 + n) / (1 + (self.Xc > 0).sum(0))) + 1
        X = np.hstack([w_word * self._tfidf(self.Xw, self.idf_w), w_char * self._tfidf(self.Xc, self.idf_c)])
        U, S, Vt = np.linalg.svd(X, full_matrices=False)
        k = min(dims, len(S))
        # fix the sign of each component so results do not change between machines
        signs = np.sign(Vt[:k][np.arange(k), np.abs(Vt[:k]).argmax(1)])
        signs[signs == 0] = 1
        self.Vt = Vt[:k] * signs[:, None]
        E = X @ self.Vt.T
        self.E = E / (np.linalg.norm(E, axis=1, keepdims=True) + 1e-9)

    @staticmethod
    def _mat(counts, vocab, n):
        M = np.zeros((n, len(vocab)), dtype=np.float32)
        for i, c in enumerate(counts):
            for t, v in c.items():
                M[i, vocab[t]] = v
        return M

    @staticmethod
    def _tfidf(M, idf):
        X = np.log1p(M) * idf
        return X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-9)

    def scores(self, query):
        d = tokenise(query)
        w, c = {}, {}
        for t in d:
            w[t] = w.get(t, 0) + 1
            for g in _char_ngrams(t):
                c[g] = c.get(g, 0) + 1
        qw = np.zeros((1, len(self.wv)), dtype=np.float32)
        qc = np.zeros((1, len(self.cv)), dtype=np.float32)
        for t, v in w.items():
            if t in self.wv:
                qw[0, self.wv[t]] = v
        for t, v in c.items():
            if t in self.cv:
                qc[0, self.cv[t]] = v
        q = np.hstack([self.w_word * self._tfidf(qw, self.idf_w), self.w_char * self._tfidf(qc, self.idf_c)])
        e = q @ self.Vt.T
        e = e / (np.linalg.norm(e) + 1e-9)
        return (self.E @ e.T).ravel()


# ------------------------------------------------------------------ fusion, permissions, search
def rrf(rankings, k=60):
    """Reciprocal rank fusion. `rankings` is a list of lists of chunk positions, best first. Returns fused order."""
    score = {}
    for r in rankings:
        for pos, idx in enumerate(r, start=1):
            score[idx] = score.get(idx, 0.0) + 1.0 / (k + pos)
    return [i for i, _ in sorted(score.items(), key=lambda kv: (-kv[1], kv[0]))]


def user_can_see(doc_groups, user_groups):
    """A user sees a document when it is open to all staff or shares at least one group with the user."""
    dg = set(str(doc_groups).split(";"))
    ug = set(str(user_groups).split(";")) | {"all_staff"}
    return bool(dg & ug)


class Searcher:
    def __init__(self, chunks, depth=50):
        self.chunks = chunks.reset_index(drop=True)
        self.bm25 = BM25(self.chunks)
        self.meaning = MeaningScorer(self.chunks)
        self.depth = depth

    def _rank(self, scores, allowed):
        s = np.where(allowed, scores, -np.inf)
        order = np.argsort(-s, kind="stable")
        return [int(i) for i in order[: self.depth] if np.isfinite(s[i])]

    def search(self, query, method="hybrid", k=5, user_groups=None, current_only=False):
        """Return the top k chunks as a DataFrame. Filters are applied before ranking."""
        allowed = np.ones(len(self.chunks), dtype=bool)
        if user_groups is not None:
            allowed &= self.chunks.access_groups.map(lambda g: user_can_see(g, user_groups)).to_numpy()
        if current_only:
            allowed &= (self.chunks.status == "current").to_numpy()
        bs = self.bm25.scores(query) if method in ("bm25", "hybrid") else None
        # a chunk that shares no word with the query is not a match, so it is never returned by keyword search
        rb = self._rank(bs, allowed & (bs > 0)) if bs is not None else []
        rm = self._rank(self.meaning.scores(query), allowed) if method in ("meaning", "hybrid") else []
        order = rb if method == "bm25" else rm if method == "meaning" else rrf([rb, rm])
        return self.chunks.iloc[order[:k]]


def recall_at_k(ranked_doc_ids, gold_doc_id, k=5):
    return int(gold_doc_id in list(ranked_doc_ids)[:k])


def mrr(ranked_doc_ids, gold_doc_id):
    for i, d in enumerate(ranked_doc_ids, start=1):
        if d == gold_doc_id:
            return 1.0 / i
    return 0.0
