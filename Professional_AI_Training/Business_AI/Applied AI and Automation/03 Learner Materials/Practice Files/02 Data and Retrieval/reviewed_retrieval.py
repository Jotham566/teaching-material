"""Evidence retrieval for the classroom contract review.

Select a matter, document identity and source purpose before searching. An
executed contract governs obligations; correspondence supplies transaction facts.
An amendment and precedence rule travel with the source they modify. Keyword and
neural candidates are merged and reranked, but the result remains evidence for a
reviewer, not an answer or a security assurance about a real document system.

  python reviewed_retrieval.py "question" --source-id CONTRACT-01
  python reviewed_retrieval.py "earlier wording" --source-id CONTRACT-01 --purpose historical
  python reviewed_retrieval.py "ownership evidence" --purpose facts

Needs the pinned sentence-transformers environment. First use downloads the two
public models. --offline uses the already cached files. Historical comparison
algorithms remain in search_library.py; their saved failures are not rewritten.
"""
import argparse,csv,hashlib,json,re
from functools import lru_cache
from pathlib import Path
import numpy as np
from search_library import bm25,rrf
ROOT=Path(__file__).resolve().parent
EMBEDDER="sentence-transformers/all-MiniLM-L6-v2"
RERANKER="cross-encoder/ms-marco-MiniLM-L-6-v2"

@lru_cache(maxsize=2)
def models(offline=False):
    from sentence_transformers import SentenceTransformer,CrossEncoder
    return (SentenceTransformer(EMBEDDER,local_files_only=offline),
            CrossEncoder(RERANKER,max_length=512,local_files_only=offline))

def permitted_documents(matters,source_id,purpose):
    docs=list(csv.DictReader((ROOT/"Knowledge Library Manifest.csv").open(encoding="utf8")))
    # Filter identity and access before opening a file or returning its metadata.
    docs=[d for d in docs if d["matter"] in set(matters) and (source_id is None or d["document_id"]==source_id)]
    if purpose=="historical":return [d for d in docs if d["status"]=="superseded" and d["type"]=="draft agreement"]
    docs=[d for d in docs if d["status"]=="current"]
    if purpose=="obligations":return [d for d in docs if d["type"]=="agreement"]
    return [d for d in docs if d["type"] not in ("agreement","draft agreement")]

def pieces(d,model):
    path=(ROOT/d["file"]).resolve()
    if ROOT.resolve() not in path.parents:raise ValueError("source path leaves the library")
    text=path.read_text(encoding="utf8")
    if hashlib.sha256(path.read_bytes()).hexdigest()!=d["sha256"]:raise ValueError("source hash differs from the manifest")
    lines=text.splitlines();units=[];cur=[];start=1
    for no,line in enumerate(lines,1):
        if cur and (not line.strip() or re.match(r"(?:==|SECTION |Section \d+\.\d+|Other Changes)",line)):
            units.append((start,no-1,"\n".join(cur)));cur=[]
        if not line.strip():continue
        if not cur:start=no
        cur.append(line)
    if cur:units.append((start,len(lines),"\n".join(cur)))
    out=[];prefix=d["title"]+". "
    budget=model.max_seq_length-len(model.tokenizer.encode(prefix,add_special_tokens=False))-2
    if budget<64:raise ValueError("source title leaves insufficient embedding space")
    budget=min(190,budget)
    for lo,hi,unit in units:
        for sub in re.split(r"(?=\[ADAPTED\] \[TEACHING ADAPTATION \d+\])",unit):
            if not sub.strip():continue
            offsets=model.tokenizer(sub,add_special_tokens=False,return_offsets_mapping=True,verbose=False)["offset_mapping"]
            z=0
            while z<len(offsets):
                end=min(z+budget,len(offsets));body=sub[offsets[z][0]:offsets[end-1][1]]
                inp=prefix+body;size=len(model.tokenizer.encode(inp,verbose=False))
                if size>model.max_seq_length:raise ValueError("embedding input exceeds token budget")
                out.append(dict(id=f"{d['document_id']} {d['version']} L{lo}-{hi} part {len(out)+1}",doc=d["document_id"],
                    version=d["version"],matter=d["matter"],status=d["status"],type=d["type"],title=d["title"],
                    source_file=d["file"],source_sha256=d["sha256"],line_start=lo,line_end=hi,text=body,embedding_tokens=size,
                    mandatory_context=bool("Key Terms will control" in sub or "TEACHING ADAPTATION" in sub)))
                if end==len(offsets):break
                z=end-32
    return out,text

_EMBEDDINGS={}
def retrieve(query,source_id=None,purpose="obligations",matters=("M-01",),top=5,offline=False):
    if purpose not in ("obligations","facts","historical"):raise ValueError("choose a source purpose")
    if purpose!="facts" and not source_id:return dict(status="clarify_source",hits=[],mandatory_context=[],note="Select the intended document identity before reviewing obligations or historical wording.")
    docs=permitted_documents(matters,source_id,purpose)
    if not docs:return dict(status="no_source",hits=[],mandatory_context=[],note="No requested source is available in the permitted scope. Do not substitute another document.")
    model,reranker=models(offline)
    if len(model.tokenizer.encode(query,verbose=False))>128:return dict(status="clarify_query",hits=[],mandatory_context=[],note="Shorten the question before retrieval; no query was silently truncated.")
    chunks=[];source_text=[]
    for d in docs:
        cs,txt=pieces(d,model);chunks.extend(cs);source_text.append(txt)
    # A named agreement in the question cannot silently resolve to a different active contract.
    named=re.search(r"\b(?:in|under|from)\s+(?:the\s+)?([A-Z][\w&-]+(?:\s+[A-Z][\w&-]+){0,4})\s+agreement\b",query)
    if named and not any(named.group(1).casefold() in t.casefold() for t in source_text):
        return dict(status="no_source",hits=[],mandatory_context=[],note="The named source is unavailable in this permitted scope. Do not substitute the active agreement.")
    text=[c["title"]+". "+c["text"] for c in chunks];key=hashlib.sha256("\n".join(text).encode()).hexdigest()
    if key not in _EMBEDDINGS:_EMBEDDINGS[key]=model.encode(text,normalize_embeddings=True)
    neural=_EMBEDDINGS[key]@model.encode([query],normalize_embeddings=True)[0];lex=bm25(chunks,query)
    fused=rrf([list(np.argsort(-lex)),list(np.argsort(-neural))]);candidates=sorted(fused,key=fused.get,reverse=True)[:30]
    scores=reranker.predict([(query,text[i]) for i in candidates])
    hits=[dict(chunks[candidates[int(j)]],rank=r+1,rerank_score=round(float(scores[int(j)]),5)) for r,j in enumerate(np.argsort(-scores)[:top])]
    mandatory=[c for c in chunks if c["mandatory_context"]] if purpose=="obligations" else []
    return dict(status="evidence_for_review",purpose=purpose,selected_source=source_id,user_matters=list(matters),
        method="purpose and identity filters; token-bounded chunks; BM25 and neural candidates; cross-encoder reranking; amendment and precedence context",
        embedder=EMBEDDER,reranker=RERANKER,max_embedding_tokens=max(c["embedding_tokens"] for c in chunks),model_limit=model.max_seq_length,
        hits=hits,mandatory_context=mandatory,note="Similarity scores do not establish a legal conclusion, negation, transaction fact or current law. Read the evidence and keep an unresolved fact unresolved.")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("query");p.add_argument("--source-id");p.add_argument("--purpose",choices=["obligations","facts","historical"],default="obligations")
    p.add_argument("--user-matters",default="M-01");p.add_argument("--top",type=int,default=5);p.add_argument("--offline",action="store_true")
    a=p.parse_args();print(json.dumps(retrieve(a.query,a.source_id,a.purpose,a.user_matters.split(","),a.top,a.offline),indent=2))
