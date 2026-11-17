"""Check a neural embedding setup BEFORE using it in class.

This is the first thing to run on a machine that has internet access once, or a local
copy of the model. It does not rank anything. It checks that the model loads, that the
vectors have the expected shape and length, that the same text gives the same vector,
and it prints the cosine similarity of a few pairs so you can see what the model does.
Save the output with the date. Do not state in class what the model will do before
you have seen this output on your own machine.

  pip install sentence-transformers
  python3 embedding_selftest.py [--model all-MiniLM-L6-v2] [--save "Observed Embedding Selftest.txt"]

Offline use: download the model once, then pass its folder with --model.
STATUS: executed on the teaching Mac on 27 October 2026. See the dated neural
embedding outputs in Teaching Resources/Observed Runs/Mac Rehearsal 2026-10-27.
"""
import sys, argparse, platform, datetime
p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
p.add_argument("--model", default="all-MiniLM-L6-v2"); p.add_argument("--save")
a = p.parse_args()
try:
    import numpy as np
    import sentence_transformers
    from sentence_transformers import SentenceTransformer
except ImportError as e:
    sys.exit(f"Missing package: {e}. Run: pip install sentence-transformers")
m = SentenceTransformer(a.model)
S = {
 "assign": "Neither party may assign any rights or obligations under this Agreement without the prior written consent of the other party.",
 "hand_over": "Is Equator free to hand the contract over to somebody else?",
 "restructure": "Do we have to consent to Equator's restructuring?",
 "consent": "Provider must obtain Customer's prior written consent before a change of control of Provider takes effect.",
 "fees": "The Fees are set out in the Fee Schedule signed by the parties on the Order Date.",
 "weather": "Heavy rain is expected across the Lake Victoria basin this weekend.",
 "req": "Consent is required for a reorganization within a wholly owned group.",
 "notreq": "Consent is not required for a reorganization within a wholly owned group.",
}
keys = list(S); E = m.encode([S[k] for k in keys], normalize_embeddings=True)
lines = [f"EMBEDDING SELF-TEST {datetime.datetime.now().isoformat(timespec='seconds')}",
         f"model: {a.model}", f"python {platform.python_version()}, numpy {np.__version__}, sentence-transformers {sentence_transformers.__version__}",
         f"vector shape: {E.shape}", f"vector lengths (should be 1.0): min {np.linalg.norm(E,axis=1).min():.4f} max {np.linalg.norm(E,axis=1).max():.4f}"]
E2 = m.encode([S[keys[0]]], normalize_embeddings=True)
lines.append(f"same text, same vector: {bool(np.allclose(E[0], E2[0], atol=1e-5))}")
def cos(x, y): return float(E[keys.index(x)] @ E[keys.index(y)])
for x, y in [("hand_over","assign"),("restructure","consent"),("hand_over","weather"),("fees","weather"),("req","notreq"),("req","weather")]:
    lines.append(f"cosine({x}, {y}) = {cos(x,y):.3f}")
lines.append("Read the pairs yourself. The pair req/notreq shows how close a statement and its opposite sit in the space.")
out = "\n".join(lines); print(out)
if a.save: open(a.save, "w", encoding="utf-8").write(out + "\n")
