"""Session 9 demonstration: a real retrieval step. Chunk the NVF staff handbook excerpt by clause, embed the chunks and the ten questions
with all-MiniLM-L6-v2 (sentence-transformers), and print the three closest chunks and their cosine similarity for each question.
Run:  python retrieve.py            (writes retrieval_results.json and prints a table)
"""
import csv, json, re, sys
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
import sentence_transformers

HERE = Path(__file__).parent
text = (HERE / 'staff_handbook_excerpt.txt').read_text()

# 1. chunk by clause: a line that starts with a number such as "2.1 "
chunks = []
for line in text.splitlines():
    m = re.match(r'^(\d+\.\d+)\s+(.*)', line)
    if m:
        chunks.append({'id': m.group(1), 'text': m.group(2)})
print(f'{len(chunks)} chunks, sentence-transformers {sentence_transformers.__version__}')

questions = list(csv.DictReader(open(HERE / 'handbook_questions_key.csv')))
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
C = model.encode([c['text'] for c in chunks], normalize_embeddings=True)
Q = model.encode([q['question'] for q in questions], normalize_embeddings=True)
S = Q @ C.T          # cosine similarity, because the vectors are normalised

out = []
for qi, q in enumerate(questions):
    order = np.argsort(-S[qi])[:5]
    top = [{'clause': chunks[i]['id'], 'score': round(float(S[qi, i]), 3)} for i in order]
    hit = q['clause'] in [t['clause'] for t in top[:3]] if q['clause'] != 'none' else None
    out.append({'id': q['id'], 'question': q['question'], 'answer_clause': q['clause'], 'top5': top, 'answer_clause_in_top3': hit,
                'answer_clause_rank': (list(chunks[i]['id'] for i in np.argsort(-S[qi])).index(q['clause']) + 1) if q['clause'] != 'none' else None})
    print(q['id'], 'answer clause', q['clause'], '| top 3:', ', '.join(f"{t['clause']} ({t['score']:.2f})" for t in top[:3]))
json.dump({'chunks': chunks, 'results': out}, open(HERE / 'retrieval_results.json', 'w'), indent=1)
