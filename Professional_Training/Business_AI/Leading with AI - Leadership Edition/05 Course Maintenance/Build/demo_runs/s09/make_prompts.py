"""Builds the two prompt variants for the recorded assistant runs (no document, retrieved passages only). The full-document variant is Case Runs/prompts/F2b_handbook_questions.md."""
import csv, json
from pathlib import Path
HERE = Path(__file__).parent
res = json.load(open(HERE / 'retrieval_results.json'))
chunks = {c['id']: c['text'] for c in res['chunks']}
qs = res['results']
INSTR = 'Answer each question using only the staff handbook. Quote the clause number for each answer. If the handbook does not say, write "not stated in the handbook".'
head = 'You are a plain AI chat assistant answering a manager.\n\n'
# A. no document
qtxt = '\n'.join(f"{r['id']}. {r['question']}" for r in qs)
a = head + ('The manager asks about the staff handbook of Nile Valley Foods Ltd, a fictional food distributor in Jinja, Uganda (Staff Handbook, Version 4, effective 1 January 2026).\n\n'
            + INSTR + '\n\nQUESTIONS:\n' + qtxt + '\n')
(HERE / 'prompts' / 'A_no_document.md').write_text(a)
# B. retrieved passages only: for each question the three closest chunks, best first
parts = []
for r in qs:
    ps = '\n'.join(f"[{t['clause']}] {chunks[t['clause']]}" for t in r['top5'][:3])
    parts.append(f"{r['id']}. {r['question']}\nPassages retrieved for this question:\n{ps}")
b = head + ('Answer each question using only the passages retrieved for it from the Nile Valley Foods Ltd (fictional) Staff Handbook, Version 4. Quote the clause number (the number in square brackets) for each answer. '
            'If the passages do not say, write "not stated in the handbook".\n\n' + '\n\n'.join(parts) + '\n')
(HERE / 'prompts' / 'B_retrieved_passages.md').write_text(b)
print(len(a.split()), len(b.split()))
