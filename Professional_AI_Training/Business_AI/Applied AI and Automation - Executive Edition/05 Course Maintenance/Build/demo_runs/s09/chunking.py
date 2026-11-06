"""Session 9 demonstration: does the way you cut the document change what retrieval finds?
Same handbook, same model (all-MiniLM-L6-v2), same eight answerable questions. Three ways of cutting:
  clause  = one chunk per numbered clause (30 chunks)
  fixed   = a new chunk every N characters, ignoring clause boundaries (no overlap)
A question counts as 'answered by the top chunk' when the top chunk contains every answer fragment listed below (a text check, not a judgement).
Run:  python chunking.py     (writes chunking_results.json)
"""
import json, re
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer

HERE = Path(__file__).parent
text = (HERE / 'staff_handbook_excerpt.txt').read_text()
body = '\n'.join(l for l in text.splitlines() if re.match(r'^\d+\.\d+\s', l))   # the 30 clauses only, in order

NEEDLES = {   # question -> fragments the top chunk must contain to hold the answer
 'Q01': ('How many working days of paid annual leave does a full-time staff member earn in each leave year?', ['21 working days']),
 'Q02': ('How long before the first day of leave must a leave request reach the line manager?', ['14 days before']),
 'Q03': ('Who must approve an expense claim of UGX 1,500,000?', ['200,001 to UGX 2,000,000', 'Finance Manager']),
 'Q04': ('Within how many days of spending must receipts reach the Finance office?', ['within 14 days of the spending']),
 'Q05': ('How is approved overtime paid on a Sunday?', ['2 times the normal hourly rate on Sundays']),
 'Q06': ('May a staff member paste a customer price list into a public AI tool?', ['unless the Managing Director has approved']),
 'Q07': ('How soon must a lost company laptop be reported, and to whom?', ['Operations Manager within 4 hours']),
 'Q08': ('What is the most the company will pay for one night of accommodation on company travel?', ['180,000 a night']),
}

def clause_chunks():
    return [re.sub(r'^\d+\.\d+\s+', '', l) for l in body.splitlines()]

def fixed_chunks(n):
    flat = body.replace('\n', ' ')
    return [flat[i:i + n] for i in range(0, len(flat), n)]

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
qs = [v[0] for v in NEEDLES.values()]
Q = model.encode(qs, normalize_embeddings=True)
res = {}
for name, chunks in (('clause', clause_chunks()), ('fixed 150 characters', fixed_chunks(150)), ('fixed 300 characters', fixed_chunks(300))):
    C = model.encode(chunks, normalize_embeddings=True)
    S = Q @ C.T
    ok, rows = 0, []
    for qi, (qid, (q, needles)) in enumerate(NEEDLES.items()):
        top = int(np.argmax(S[qi]))
        full = all(nd in chunks[top] for nd in needles)
        ok += full
        rows.append({'q': qid, 'top_score': round(float(S[qi, top]), 3), 'top_chunk_holds_answer': full, 'top_chunk': chunks[top]})
    res[name] = {'n_chunks': len(chunks), 'answered_by_top_chunk': ok, 'of': len(NEEDLES), 'rows': rows}
    print(f'{name}: {len(chunks)} chunks, top chunk holds the whole answer for {ok} of {len(NEEDLES)} questions')
    for r in rows:
        print('   ', r['q'], r['top_score'], 'YES' if r['top_chunk_holds_answer'] else 'no ', '|', r['top_chunk'][:110].replace('\n', ' '))
json.dump(res, open(HERE / 'chunking_results.json', 'w'), indent=1)
