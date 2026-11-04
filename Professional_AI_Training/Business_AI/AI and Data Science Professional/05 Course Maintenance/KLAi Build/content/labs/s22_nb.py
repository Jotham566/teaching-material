"""Session 22 lab: language models and building with them. Chunking, TF-IDF retrieval, an evaluation set with precision and recall at k, a grounded prompt and an audit log all run in numpy and pandas and are verified here.
Step 9 (a small open model through transformers) only runs in Colab and has no check. Expected values come from content/s22.py (facts())."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
BUILD = HERE.parents[2]
sys.path.insert(0, str(BUILD / 'kit'))
import nb as NB  # noqa: E402

_spec = importlib.util.spec_from_file_location('s22_content', BUILD / 'content' / 's22.py')
S = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(S)

TITLE = 'Language models and building with them'
NEEDS = []   # step 9 is guarded, so every other step is verified here
MODEL_NAME = 'HuggingFaceTB/SmolLM2-360M-Instruct'   # SmolLM2 360M Instruct: Apache 2.0 on its model card (checked 4 Nov 2026), about 362M parameters, no account needed


def build(solution: bool) -> NB.Notebook:
    F = S.facts()
    pt, po = F['pr_tfidf'], F['pr_overlap']
    nb = NB.Notebook()

    def todo(hint, sol, lines=None):
        if solution:
            nb.code(sol)
        else:
            nb.code(lines if lines is not None else sol.split('=')[0].strip() + ' = None  # ' + hint)

    def dep(code):
        """A given cell that needs the learner's earlier answers. In the learner version it reports instead of stopping when an answer is still None."""
        if solution:
            nb.code(code)
        else:
            body = '\n'.join('    ' + l if l else l for l in code.split('\n'))
            nb.code('try:\n' + body + '\nexcept Exception as e:\n    print("Finish the cells above first. (" + type(e).__name__ + ")")')

    nb.md('# Session 22: Language models and building with them\n\nYou build the search half of retrieval-augmented generation (RAG) over the eight Lakeside Mart policy files, then score it with an evaluation set. '
          'Rhythm for every step: **predict**, run, **read** the output, **change** one thing. A line that starts with OK means your number matches. Data is fictional. Never paste real customer data into a tool you do not control.')
    nb.data_setup()
    nb.check_setup()
    nb.code('# Helper: returns nan instead of stopping when your answer is not ready yet. You do not need to read it.\ndef safe(f):\n    try:\n        return f()\n    except Exception:\n        return float("nan")')

    # step 1
    nb.step(1, 'Chunking', 'Split each policy file into chunks: here, one sentence per chunk. Keep the file name with every chunk.')
    nb.code("import os, re, sys\nimport numpy as np\nimport pandas as pd\n\nos.makedirs('keep', exist_ok=True)   # the folder where you save what you keep")
    nb.predict('Eight short files of about 90 words each. How many sentence chunks will you get: about 10, 60 or 600?')
    if solution:
        nb.code("chunks = []\nfor name in sorted(os.listdir('policies')):\n    text = ' '.join(open('policies/' + name).read().split())\n    pieces = re.split(r'(?<=\\.)\\s+(?=[A-Z])', text)   # split after a full stop followed by a capital letter\n    chunks += [(name, p) for p in pieces]")
    else:
        nb.code("chunks = []\nfor name in sorted(os.listdir('policies')):\n    text = ' '.join(open('policies/' + name).read().split())\n    pieces = [text]  # your code here: re.split(pattern, text): split after a full stop that is followed by a capital letter\n    chunks += [(name, p) for p in pieces]")
    nb.code(f"n_words = sum(len(p.split()) for _, p in chunks)\nprint(len(chunks), 'chunks,', n_words, 'words')\ncheck('number of chunks', len(chunks), {F['n_chunks']}, 0)\ncheck('words in all chunks', n_words, {F['policy_words']}, 0)")
    nb.change('Print `chunks[28]`. Which file and sentence is it? Then think: what would change if a chunk were two sentences?')

    # step 2
    nb.step(2, 'Vectors for the chunks: bag of words and TF-IDF', 'The same recipe as Session 21, now on chunks. Rows are chunks and columns are words.')
    nb.code(f"STOP = set({S.STOP!r})\n\ndef tokens(text):\n    return [w for w in re.findall('[a-z0-9]+', text.lower()) if w not in STOP]\n\n"
            "docs = [tokens(p) for _, p in chunks]\nvocab = sorted({w for d in docs for w in d})\nindex = {w: i for i, w in enumerate(vocab)}\nX = np.array([[d.count(w) for w in vocab] for d in docs])\nprint(X.shape)")
    todo('number of chunks containing each word: (X > 0).sum(axis=0)', 'df = (X > 0).sum(axis=0)')
    todo('inverse document frequency: np.log(number of chunks / df)', 'idf = np.log(len(chunks) / df)')
    dep("T = X * idf\nT = T / np.maximum(np.linalg.norm(T, axis=1, keepdims=True), 1e-9)   # unit length rows")
    nb.code("def vec(text):\n    v = np.zeros(len(vocab))\n    for w in tokens(text):\n        if w in index:\n            v[index[w]] += 1\n    v = v * idf\n    n = np.linalg.norm(v)\n    return v / n if n else v")
    nb.code(f"check('vocabulary size', len(vocab), {F['V']}, 0)\ncheck('idf of the word points', safe(lambda: idf[index['points']]), {float(F['idf'][F['idx']['points']]):.4f}, 0.001)")

    # step 3
    nb.step(3, 'Retrieval and ranking', 'Score every chunk against the question with cosine similarity, sort the scores, and keep the top k.')
    nb.predict('For "How many days do I have to return an item?", which file will the top chunk come from?')
    todo('the indices of the k highest scores: np.argsort(-scores, kind="stable")[:k] where scores = T @ vec(question)',
         "def retrieve(question, k=3):\n    scores = T @ vec(question)\n    return np.argsort(-scores, kind='stable')[:k]",
         "def retrieve(question, k=3):\n    return None  # scores = T @ vec(question); then the indices of the k highest scores")
    nb.code(f"Q = {S.Q_RET!r}")
    dep("top = retrieve(Q)\nfor i in top:\n    print(round(float(T[i] @ vec(Q)), 2), chunks[i][0], '|', chunks[i][1][:60])")
    nb.code(f"check('top chunk is from returns_policy.txt', safe(lambda: chunks[top[0]][0] == 'returns_policy.txt'), True, 0)\ncheck('score of the top chunk', safe(lambda: float(T[top[0]] @ vec(Q))), {F['ret_rows'][0][3]:.4f}, 0.01)")
    nb.read('The second and third chunks are wrong. Which words did they share with the question?')

    # step 4
    nb.step(4, 'The evaluation set', 'A labelled test set: each question has the exact answer text. A chunk is relevant when it contains that text.')
    rows = ',\n'.join(f'    ({q!r}, {f!r}, {a!r})' for q, f, a in S.TESTS)
    nb.code(f"tests = pd.DataFrame([\n{rows},\n], columns=['question', 'policy', 'answer'])\nprint(len(tests), 'questions')")
    todo('for each answer, the set of chunk indices whose text contains it: {i for i, (_, s) in enumerate(chunks) if a in s}',
         'relevant = [{i for i, (_, s) in enumerate(chunks) if a in s} for a in tests.answer]')
    nb.code("n_relevant = sum(len(r) for r in relevant) if relevant is not None else 0\nprint(n_relevant, 'relevant chunks for', len(tests), 'questions')\ncheck('one relevant chunk per question', n_relevant, 12, 0)")
    nb.change('Add a 13th question of your own: copy a sentence from any policy file as the answer. Run the whole evaluation again later and see how the scores move.')

    # step 5
    nb.step(5, 'Precision at k and recall at k', 'Precision at k = relevant in the top k divided by k. Recall at k = relevant in the top k divided by all relevant chunks.')
    nb.predict('Only one chunk is right per question. What is the largest possible precision at 5? And will recall at 5 be higher or lower than recall at 1?')
    todo('len(set(top[:k]) & rel) / k', 'def precision_at_k(top, rel, k):\n    return len(set(top[:k]) & rel) / k', 'def precision_at_k(top, rel, k):\n    return None  # relevant chunks in the top k, divided by k')
    todo('len(set(top[:k]) & rel) / len(rel)', 'def recall_at_k(top, rel, k):\n    return len(set(top[:k]) & rel) / len(rel)', 'def recall_at_k(top, rel, k):\n    return None  # relevant chunks in the top k, divided by all relevant chunks')
    dep("def evaluate(retriever, k):\n    p = [precision_at_k(retriever(q, 5), rel, k) for q, rel in zip(tests.question, relevant)]\n    r = [recall_at_k(retriever(q, 5), rel, k) for q, rel in zip(tests.question, relevant)]\n    return float(np.mean(p)), float(np.mean(r))\n\n"
            "for k in (1, 3, 5):\n    print('k =', k, 'precision, recall:', [round(v, 3) for v in evaluate(retrieve, k)])\np1, r1 = evaluate(retrieve, 1)\np3, r3 = evaluate(retrieve, 3)\np5, r5 = evaluate(retrieve, 5)")
    nb.code(f"check('mean precision at 1', safe(lambda: p1), {pt[1][0]:.4f}, 0.002)\ncheck('mean recall at 1', safe(lambda: r1), {pt[1][1]:.4f}, 0.002)\ncheck('mean precision at 3', safe(lambda: p3), {pt[3][0]:.4f}, 0.002)\ncheck('mean recall at 3', safe(lambda: r3), {pt[3][1]:.4f}, 0.002)\ncheck('mean recall at 5', safe(lambda: r5), {pt[5][1]:.4f}, 0.002)")
    nb.read('Why does precision fall as k grows while recall rises?')

    # step 6
    nb.step(6, 'Read the failures', 'Find the questions where the right chunk is not ranked first, and see what the search put first instead.')
    todo('for each question, the position (1 is first) of its relevant chunk in the full ranking',
         "def rank_of_right(question, rel):\n    order = list(np.argsort(-(T @ vec(question)), kind='stable'))\n    return order.index(next(iter(rel))) + 1",
         "def rank_of_right(question, rel):\n    return None  # position (1 is first) of the relevant chunk in the full ranking of all chunks")
    dep("tests['rank_of_right'] = [rank_of_right(q, rel) for q, rel in zip(tests.question, relevant)]\nn_fail = int((tests.rank_of_right > 1).sum())\nprint(n_fail, 'questions have the right chunk below rank 1')\ntests[tests.rank_of_right > 1][['question', 'rank_of_right']]")
    nb.code(f"check('questions whose right chunk is not first', safe(lambda: n_fail), {F['n_fail']}, 0)\ncheck('rank of the right chunk for the points question', safe(lambda: tests.rank_of_right.iloc[0]), {F['f1']['rank']}, 0)")
    nb.read('For "How long do points last?" print the top 3 chunks. Why does the word last cause trouble? Write one sentence.')

    # step 7
    nb.step(7, 'Change the method and score it again', 'Replace TF-IDF with plain word overlap: the score is the number of question words found in the chunk. Same evaluation set, same scores.')
    nb.code("def retrieve_overlap(question, k=3):\n    q = set(tokens(question))\n    scores = np.array([len(q & set(d)) for d in docs], float)\n    return np.argsort(-scores, kind='stable')[:k]")
    todo('evaluate(retrieve_overlap, 3) returns precision and recall; keep the precision', 'p3_overlap = evaluate(retrieve_overlap, 3)[0]')
    nb.code(f"print(safe(lambda: round(p3_overlap, 3)))\ncheck('mean precision at 3 with word overlap', safe(lambda: p3_overlap), {po[3][0]:.4f}, 0.002)")
    nb.read('Is the simpler method worse? Twelve questions are too few to prefer one method. Write what you would test next before choosing.')

    # step 8
    nb.step(8, 'Grounding: build the prompt', 'Put the retrieved chunks in the prompt and tell the model to answer only from them.')
    nb.code(f"SYSTEM_PROMPT = {S.SYSTEM_PROMPT!r}")
    todo('system prompt, a blank line, Passages:, the numbered passages, a blank line, Question: and Answer:',
         "def build_prompt(question, passages):\n    body = '\\n'.join(f'({i + 1}) {p}' for i, p in enumerate(passages))\n    return f'{SYSTEM_PROMPT}\\n\\nPassages:\\n{body}\\n\\nQuestion: {question}\\nAnswer:'",
         "def build_prompt(question, passages):\n    return None  # system prompt, then 'Passages:', the numbered passages, then the question and 'Answer:'")
    dep("prompt = build_prompt(Q, [chunks[i][1] for i in retrieve(Q, 3)])\nprint(prompt)")
    nb.code(f"check('words in the grounded prompt', safe(lambda: len(prompt.split())), {F['prompt_words']}, 0)\ncheck('prompt contains the returns sentence', safe(lambda: 'within 7 days of purchase' in prompt), True, 0)")
    nb.change('Set k to 1 and build the prompt again. Count the words. What is the risk of k = 1?')

    # step 9
    nb.step(9, 'Optional: a small open model in Colab', 'Colab only. The model is SmolLM2 360M Instruct (Apache 2.0 licence on its model card). Read the card before you use any model at work. Small models can be wrong or ignore your rules, so read the answer against the source chunk. Use a model that is not gated (no account or access request). Generating 60 tokens on the free CPU may take a minute.')
    nb.code(f"MODEL_NAME = {MODEL_NAME!r}   # Apache 2.0 licence, see the model card\nRUN_MODEL = 'google.colab' in sys.modules\nif RUN_MODEL and isinstance(prompt, str):\n    from transformers import pipeline\n    generator = pipeline('text-generation', model=MODEL_NAME)\n"
            "    answer = generator(prompt, max_new_tokens=60, do_sample=False)[0]['generated_text'][len(prompt):]\n    print(answer)\nelse:\n    print('This step runs in Colab. Skipping.')")
    nb.read('Does the answer match the source chunk? Write the answer, your check and your decision in your audit log (next step).')
    nb.change('Try the chat format: build `messages = [{"role": "user", "content": prompt}]` and pass it to the generator instead of the raw string. Does the answer follow the rules better?')

    # step 10
    nb.step(10, 'Keep: an evaluation file and an audit log', 'Save your scores question by question, and record what you asked an assistant (or the model) and how you checked it.')
    dep("eval_results = tests[['question', 'policy', 'rank_of_right']].copy()\neval_results['top1_correct'] = eval_results.rank_of_right == 1\neval_results['precision_at_3'] = [precision_at_k(retrieve(q, 5), rel, 3) for q, rel in zip(tests.question, relevant)]\n"
            "eval_results['recall_at_3'] = [recall_at_k(retrieve(q, 5), rel, 3) for q, rel in zip(tests.question, relevant)]\neval_results.to_csv('keep/eval_results.csv', index=False)\nprint(len(eval_results), 'rows saved')")
    if solution:
        nb.code("audit_log = pd.DataFrame([{'what_i_asked': 'Explain recall at k in plain words', 'what_it_gave': 'A short explanation', 'how_i_checked': 'Recomputed recall at 3 in numpy for one question', 'decision': 'Kept the explanation'}])\naudit_log.to_csv('keep/audit_log.csv', index=False)\naudit_log")
    else:
        nb.code("audit_log = pd.DataFrame(columns=['what_i_asked', 'what_it_gave', 'how_i_checked', 'decision'])\n# Your turn: add one row, for example audit_log.loc[len(audit_log)] = ['what you asked', 'what it gave', 'how you checked it', 'your decision']\naudit_log.to_csv('keep/audit_log.csv', index=False)\naudit_log")
    nb.code("check('eval_results has 12 rows', safe(lambda: len(eval_results)), 12, 0)\ncheck('audit log has at least one row', min(len(audit_log), 1), 1, 0)\ncheck('audit log has 4 columns', audit_log.shape[1], 4, 0)\nshow_checks()")
    nb.md('**My finding (three sentences):** 1) precision at 1 and recall at 3 of my retrieval, 2) one failure and why, 3) one thing I would change before putting this in front of customers.\n\n> ')
    return nb
