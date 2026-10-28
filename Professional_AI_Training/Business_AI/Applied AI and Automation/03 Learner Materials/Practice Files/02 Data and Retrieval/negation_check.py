"""Does the ranking change when the question says the opposite?

For each pair of opposite statements, this script runs the search for both and
reports whether the top results are the same. It is a demonstration of a limit of
ranking by similarity. It does not judge answers, and it does not claim every search
system behaves this way: the script lets you keep or drop the negation words
(--drop-negations) to see that the effect of "not" on the ranking is small either way.

A ranking that is the same for a statement and its opposite cannot, on its own,
tell the reader which of the two the document supports. A person or a model has to
read the retrieved passage.

Usage: python3 negation_check.py [--method lexical|lsa|sbert|hybrid] [--top 3] [--drop-negations]
"""
import sys, argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from search_library import search, set_drop_negations

PAIRS = [
    ("consent is required for a reorganization within a wholly owned group",
     "consent is not required for a reorganization within a wholly owned group"),
    ("Provider may give support staff access to Customer Content",
     "Provider may not give support staff access to Customer Content"),
    ("the Fees are set out in the signed Fee Schedule",
     "the Fees are not set out in the signed Fee Schedule"),
]
p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
p.add_argument("--method", default="lexical", choices=["lexical", "lsa", "sbert", "hybrid"])
p.add_argument("--top", type=int, default=3); p.add_argument("--drop-negations", action="store_true")
a = p.parse_args(); set_drop_negations(a.drop_negations)
print(f"method: {a.method}; top {a.top}; negation words {'dropped' if a.drop_negations else 'kept'}")
for x, y in PAIRS:
    rx = search(x, a.method, ["M-01"], False, a.top)["results"]; ry = search(y, a.method, ["M-01"], False, a.top)["results"]
    ix = [r["chunk"] for r in rx]; iy = [r["chunk"] for r in ry]
    print(f"\nA: {x}\nB: {y}\n  top for A: {ix}\n  top for B: {iy}\n  same chunks in the same order: {ix == iy}")
