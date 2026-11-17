"""Session 9 peek inside the retrieval score: the first six of the 384 numbers of the Q03 question and of clauses 3.2 and 3.1,
the six products, and the full cosine score. Run: python peek_scoring.py   (writes peek_scoring.json)
"""
import csv, json, re
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer

HERE = Path(__file__).parent
chunks = {}
for line in (HERE / 'staff_handbook_excerpt.txt').read_text().splitlines():
    m = re.match(r'^(\d+\.\d+)\s+(.*)', line)
    if m: chunks[m.group(1)] = m.group(2)
q = next(r for r in csv.DictReader(open(HERE / 'handbook_questions_key.csv')) if r['id'] == 'Q03')['question']
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
enc = lambda t: model.encode([t], normalize_embeddings=True)[0]
vq, v32, v31 = enc(q), enc(chunks['3.2']), enc(chunks['3.1'])
K = 6
out = {'question': q, 'dims': int(len(vq)), 'first6': {'question': [round(float(x), 3) for x in vq[:K]],
       '3.2': [round(float(x), 3) for x in v32[:K]], '3.1': [round(float(x), 3) for x in v31[:K]]},
       'products6_3.2': [round(float(a * b), 4) for a, b in zip(vq[:K], v32[:K])], 'partial6_3.2': round(float((vq[:K] * v32[:K]).sum()), 3),
       'products6_3.1': [round(float(a * b), 4) for a, b in zip(vq[:K], v31[:K])], 'partial6_3.1': round(float((vq[:K] * v31[:K]).sum()), 3),
       'positive_products_3.2': int(((vq * v32) > 0).sum()), 'positive_products_3.1': int(((vq * v31) > 0).sum()),
       'sum_pos_3.2': round(float(np.clip(vq * v32, 0, None).sum()), 3), 'sum_neg_3.2': round(float(np.clip(vq * v32, None, 0).sum()), 3),
       'score_3.2': round(float(vq @ v32), 3), 'score_3.1': round(float(vq @ v31), 3), 'length_question': round(float(np.linalg.norm(vq)), 3)}
json.dump(out, open(HERE / 'peek_scoring.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
