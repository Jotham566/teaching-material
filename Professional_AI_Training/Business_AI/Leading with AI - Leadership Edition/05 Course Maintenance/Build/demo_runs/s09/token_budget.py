"""Token budget for Q03 (Session 9 slide on the context window). Recorded 11 November 2026 with tiktoken 0.14.0, cl100k_base.
Counts: (1) the instructions plus the question, exactly as in the retrieved-passages prompt built by make_prompts.py;
(2) the three retrieved clauses for Q03 with their [clause] labels; (3) the whole handbook. The answer allowance of 300 tokens is a chosen setting."""
import json
from pathlib import Path
import tiktoken
HERE = Path(__file__).parent
e = tiktoken.get_encoding('cl100k_base')
n = lambda s: len(e.encode(s))
res = json.load(open(HERE / 'retrieval_results.json'))
ch = {c['id']: c['text'] for c in res['chunks']}
r = res['results'][2]
head = 'You are a plain AI chat assistant answering a manager.\n\n'
BI = ('Answer each question using only the passages retrieved for it from the Nile Valley Foods Ltd (fictional) Staff Handbook, Version 4. Quote the clause number (the number in square brackets) for each answer. '
      'If the passages do not say, write "not stated in the handbook".\n\n')
q = f"{r['id']}. {r['question']}\nPassages retrieved for this question:\n"
top = [t['clause'] for t in r['top5'][:3]]
pas = '\n'.join(f"[{c}] {ch[c]}" for c in top)
hb = (HERE / 'staff_handbook_excerpt.txt').read_text()
A = 300
print('tiktoken', tiktoken.__version__, 'cl100k_base')
print('instructions + question', n(head + BI + q))
print('retrieved clauses', top, n(pas), 'per clause', [n(ch[c]) for c in top])
print('whole handbook', n(hb))
print('answer allowance (setting)', A)
print('RAG total', n(head + BI + q) + n(pas) + A)
print('whole handbook total', n(head + BI + q) + n(hb) + A)
