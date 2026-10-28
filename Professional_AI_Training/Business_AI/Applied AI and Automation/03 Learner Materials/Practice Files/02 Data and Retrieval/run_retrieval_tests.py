"""Runs the retrieval half of Knowledge Assistant Tests.csv against search_library.py.

It checks only what a program can check: were the expected passages (phrases)
among the top results, and were forbidden documents (another matter, a superseded
version) absent? It cannot judge whether an answer preserved an exception or
admitted a gap. Score that by hand in Retrieval Scorecard.csv.

Usage: python3 run_retrieval_tests.py [--method lexical|lsa|sbert|hybrid] [--top 5] [--drop-negations]

The seven original tests (K1 to K7) are mostly exact-wording questions. K3 and K8 use
wording that does not appear in the agreement ("restructuring", "hand the contract to
someone else"). They are the tests where a vector method has a chance to help. A
failure on a test says what this method did with these 40 documents once. It does not
rank the methods.
"""
import csv, sys, argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from search_library import search, set_drop_negations

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--method", default="lexical", choices=["lexical", "lsa", "sbert", "hybrid"]); p.add_argument("--top", type=int, default=5); p.add_argument("--drop-negations", action="store_true")
    a = p.parse_args()
    set_drop_negations(a.drop_negations)
    rows = list(csv.DictReader((Path(__file__).resolve().parent / "Knowledge Assistant Tests.csv").open(encoding="utf-8")))
    print(f"method: {a.method}; top {a.top}; negation words {'dropped' if a.drop_negations else 'kept'}")
    for r in rows:
        res = search(r["question"], a.method, r["user_matters"].split(";"), r["historical"].lower() == "yes", a.top)
        got = [x["chunk"].split(" v")[0] for x in res["results"]]
        texts = " ".join(x["text"] for x in res["results"])
        exp = [x for x in r["expected_phrases"].split(";") if x]; forb = [x for x in r["forbidden_docs"].split(";") if x]
        missing = [e for e in exp if e not in texts]
        leaked = [g for g in got if g in forb]
        status = "PASS" if not missing and not leaked else "FAIL"
        print(f"{r['test_id']} {status:4s} phrases missing {missing or '-'} leaked {leaked or '-'}\n     top: {', '.join(dict.fromkeys(got))}")
main()
