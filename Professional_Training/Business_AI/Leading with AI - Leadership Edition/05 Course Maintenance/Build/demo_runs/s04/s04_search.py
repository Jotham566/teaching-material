"""Live demonstration helper for Session 4: describe something in plain words and see which passage is closest in meaning.

Run from the Build folder:
  python demo_runs/s04/s04_search.py contracts "Can we walk away from the deal without giving any reason?"
  python demo_runs/s04/s04_search.py finance  "Make sure our books match what the bank says."
  python demo_runs/s04/s04_search.py hr       "I want to quit. How much warning do I have to give?"
  python demo_runs/s04/s04_search.py --file my_passages.txt "my own plain description"      (one passage per line)
Options: --raw  leave the arrow lengths alone (the model's last step, which sets every length to 1, is skipped), so the four measures can disagree.
The first run downloads the model all-MiniLM-L6-v2 (about 90 MB); after that it runs offline."""
import argparse, sys, warnings
from pathlib import Path
import numpy as np
warnings.filterwarnings('ignore')
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
sys.path.insert(0, str(Path(__file__).resolve().parent))
from s04_corpus import SKINS

ap = argparse.ArgumentParser()
ap.add_argument('skin_or_query', nargs='+')
ap.add_argument('--file')
ap.add_argument('--raw', action='store_true')
a = ap.parse_args()
if a.file:
    passages = [l.strip() for l in open(a.file, encoding='utf-8') if l.strip()]
    heads = [p[:40] for p in passages]
    query = ' '.join(a.skin_or_query)
else:
    skin, query = a.skin_or_query[0], ' '.join(a.skin_or_query[1:])
    passages = [t for _, _, t in SKINS[skin]['passages']]
    heads = [h for _, h, _ in SKINS[skin]['passages']]
m = SentenceTransformer('all-MiniLM-L6-v2')
if a.raw:
    m = SentenceTransformer(modules=[m[0], m[1]])
E = m.encode(passages); q = m.encode([query])[0]
eu = np.linalg.norm(E - q, axis=1); ma = np.abs(E - q).sum(axis=1); dot = E @ q; cos = dot / (np.linalg.norm(E, axis=1) * np.linalg.norm(q))
tf = TfidfVectorizer(stop_words='english').fit(passages)
kw = (tf.transform(passages) @ tf.transform([query]).T).toarray().ravel()
print(f'Description: {query}\nVectors: {E.shape[1]} numbers each; length of the description vector {np.linalg.norm(q):.2f}' + ('  (raw lengths)' if a.raw else '  (all lengths are 1)'))
print('\nMeaning search, closest first (cosine; straight line; city blocks; agreement score):')
for i in np.argsort(-cos)[:3]:
    print(f'  {heads[i]:<30} cosine {cos[i]:.3f}  straight {eu[i]:.3f}  blocks {ma[i]:6.2f}  agreement {dot[i]:.3f}')
print('Who wins under each measure:', {'cosine': heads[int(np.argmax(cos))], 'straight line': heads[int(np.argmin(eu))], 'city blocks': heads[int(np.argmin(ma))], 'agreement score': heads[int(np.argmax(dot))]})
print('\nWord search (TF-IDF, shared words only):', 'no passage shares a word with the description' if kw.max() == 0 else ', '.join(f'{heads[i]} ({kw[i]:.2f})' for i in np.argsort(-kw)[:3] if kw[i] > 0))
