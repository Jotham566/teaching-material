"""Retrieval evidence and boundary regressions. Run with the pinned embedding environment.

The first eight reuse the original questions but add explicit source-purpose and
identity inputs, amendment expansion and a stronger K2/K4 assertion. This tests a
changed workflow, not an unqualified improvement of the embedding model. Further
checks use new wording and missing-source, version, token and integrity failures.
No test judges the correctness of a generated legal answer.
"""
import csv,json,tempfile
from pathlib import Path
import reviewed_retrieval as rr
ROOT=Path(__file__).resolve().parent

def main(output=None):
    results=[]
    def record(name,ok,detail):
        results.append(dict(check=name,passed=bool(ok),detail=detail));print(("PASS " if ok else "FAIL ")+name,flush=True)
    rows=list(csv.DictReader((ROOT/"Knowledge Assistant Tests.csv").open(encoding="utf8")))
    for row in rows:
        purpose="historical" if row["historical"]=="yes" else ("facts" if row["test_id"]=="K6" else "obligations")
        r=rr.retrieve(row["question"],None if purpose=="facts" else "CONTRACT-01",purpose,row["user_matters"].split(";"),offline=True)
        ev=r["hits"]+r["mandatory_context"];text=" ".join(x["text"] for x in ev)
        phrases=[x for x in row["expected_phrases"].split(";") if x]
        if row["test_id"]=="K2":phrases.append("before a change of control of Provider takes effect")
        missing=[x for x in phrases if x not in text];leaks=[x["doc"] for x in ev if x["doc"] in row["forbidden_docs"].split(";")]
        status=r["status"]==("no_source" if row["test_id"]=="K4" else "evidence_for_review")
        record(row["test_id"]+" evidence and scope",not missing and not leaks and status,dict(missing=missing,leaks=leaks,result=r))
    for name,q,phrase in [
        ("new wording ownership event","What permission must precede an outside investor taking the controlling stake?","before a change of control"),
        ("new wording transfer","Could the supplier hand its duties to a different legal person?","Neither party may assign"),
        ("exception retained","How would an internal group reshuffle affect the permission position?","if Provider remains responsible")]:
        r=rr.retrieve(q,"CONTRACT-01",offline=True);text=" ".join(x["text"] for x in r["hits"]+r["mandatory_context"])
        record(name,phrase in text and "Key Terms will control" in text,dict(result=r))
    r=rr.retrieve("Review the document","UNAVAILABLE-ID",offline=True)
    record("unknown identity has no substitute or metadata",r["status"]=="no_source" and not r["hits"] and not r["mandatory_context"],r)
    r=rr.retrieve("Review this agreement","CONTRACT-01",matters=("NO-ACCESS",),offline=True)
    record("no permitted matter returns no metadata",r["status"]=="no_source" and not r["hits"],r)
    r=rr.retrieve("Is consent required?",offline=True)
    record("missing document identity asks for clarification",r["status"]=="clarify_source",r)
    r=rr.retrieve("consent "*200,"CONTRACT-01",offline=True)
    record("overlong query is held rather than truncated",r["status"]=="clarify_query",r)
    model,_=rr.models(True);chunks=[]
    for d in rr.permitted_documents(("M-01",),None,"obligations"):
        cs,_=rr.pieces(d,model);chunks+=cs
    record("every embedded input fits the actual model limit",all(c["embedding_tokens"]<=model.max_seq_length for c in chunks),dict(chunks=len(chunks),max_tokens=max(c["embedding_tokens"] for c in chunks),limit=model.max_seq_length))
    record("every evidence chunk is a verbatim source span",all(c["text"] in (ROOT/c["source_file"]).read_text(encoding="utf8") for c in chunks),dict(chunks=len(chunks)))
    draft=rr.retrieve("What did the earlier draft say?","CONTRACT-01","historical",offline=True)
    record("historical results are labelled superseded",bool(draft["hits"]) and all(x["status"]=="superseded" for x in draft["hits"]),draft)
    # Exercise the integrity failure with a separate fixture, leaving the live sources untouched.
    original_root=rr.ROOT
    try:
        with tempfile.TemporaryDirectory() as td:
            rr.ROOT=Path(td);file=rr.ROOT/"changed.txt";file.write_text("altered evidence")
            d=dict(document_id="TEST",version="v1",matter="M-01",status="current",type="agreement",title="Test",file="changed.txt",sha256="0"*64)
            try:rr.pieces(d,model);held=False
            except ValueError as e:held="source hash" in str(e)
            record("changed source is held by the manifest check",held,{"fixture":"separate temporary file"})
    finally:rr.ROOT=original_root
    summary=dict(date=__import__("datetime").datetime.now().astimezone().isoformat(),passed=sum(x["passed"] for x in results),total=len(results),scope="fictional retrieval fixture; source purpose and identity supplied; not a generated-answer or production security evaluation",checks=results)
    if output:Path(output).write_text(json.dumps(summary,indent=2),encoding="utf8")
    print(f"RESULT {summary['passed']}/{summary['total']}")
    return all(x["passed"] for x in results)
if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--output");a=p.parse_args();raise SystemExit(0 if main(a.output) else 1)
