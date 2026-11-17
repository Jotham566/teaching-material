"""Session 22: Language models and building with them (tokens, next-token prediction, context window, prompts, hallucination, retrieval-augmented generation, evaluation with precision and recall at k,
a small open model in Colab, privacy, AI-assisted coding). Python lab.

Every number on a slide, in a note or in the lab checks is computed in facts() from the real policy files and feedback.csv with numpy and pandas. Retrieval is TF-IDF cosine similarity written in numpy.
No language model was run here: the sandbox has no transformers or sentence-transformers. Nothing a model wrote is shown. Statements about models are generic and hedged; no closed-model internals.
"""
import collections
import re
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

BUILD = Path(__file__).resolve().parents[1]
DATA = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'data'

STOP = sorted('a an the and or of to in on at is are was were be been it its this that i my me we our you your for with as by from am have has had do does did will would can could very what how when which'.split())
TESTS = [('How long do points last?', 'loyalty_programme.txt', 'Points expire after 12 months'),
         ('How many days do I have to return an item?', 'returns_policy.txt', 'within 7 days of purchase'),
         ('How long do mobile money refunds take?', 'returns_policy.txt', 'up to 3 working days'),
         ('Which towns does delivery not reach?', 'delivery.txt', 'Gulu, Mbale, Mbarara or Fort Portal'),
         ('What is the delivery fee within 5 kilometres?', 'delivery.txt', 'UGX 5,000 within 5 kilometres'),
         ('What percent discount do Gold customers get?', 'loyalty_programme.txt', 'Gold customers receive 5 percent off'),
         ('How long is customer data kept?', 'data_privacy.txt', '3 years after the last purchase'),
         ('What temperature must dairy be stored at?', 'food_safety.txt', 'below 5 degrees Celsius'),
         ('When do branches open on Sunday?', 'opening_hours.txt', 'from 9 am to 6 pm on Sunday'),
         ('What happens when more than 5 percent of a delivery is damaged?', 'supplier_complaints.txt', 'the delivery is rejected'),
         ('Does Lakeside Mart ask for my PIN?', 'mobile_money.txt', "never asks for a customer's PIN"),
         ('Can points be exchanged for cash?', 'loyalty_programme.txt', 'Points cannot be exchanged for cash')]
Q_RET = 'How many days do I have to return an item?'
Q_FAIL1 = 'How long do points last?'
Q_FAIL2 = 'Which towns does delivery not reach?'
TEMP_WORDS = ['long', 'slow', 'quick', 'closed']
TEMP_LOGITS = [2.0, 1.2, 0.4, -0.6]   # illustrative (made-up numbers)
SYSTEM_PROMPT = 'Answer only from the passages below. If the answer is not in the passages, say: I could not find that in the policies.'
RECIPE = ('q = vec("how long do points last")\nscores = T @ q\ntop = np.argsort(-scores, kind="stable")[:3]\nfor i in top:\n    print(round(scores[i], 2), chunks[i][1][:30])')


def n(x):
    return f'{int(x):,}'


def split_chunks(text):
    return re.split(r'(?<=\.)\s+(?=[A-Z])', ' '.join(text.split()))


def tokens(t):
    return [w for w in re.findall('[a-z0-9]+', t.lower()) if w not in STOP]


def softmax_t(logits, t):
    z = np.asarray(logits, float) / t
    z = z - z.max()
    p = np.exp(z)
    return p / p.sum()


def build_prompt(question, passages):
    body = '\n'.join(f'({i + 1}) {p}' for i, p in enumerate(passages))
    return f'{SYSTEM_PROMPT}\n\nPassages:\n{body}\n\nQuestion: {question}\nAnswer:'


@lru_cache(maxsize=None)
def facts():
    F = {}
    chunks = []
    for f in sorted((DATA / 'policies').glob('*.txt')):
        for s in split_chunks(f.read_text()):
            chunks.append((f.name, s))
    F['chunks'] = chunks
    F['n_chunks'] = len(chunks)
    F['n_files'] = len({c[0] for c in chunks})
    F['policy_words'] = sum(len(s.split()) for _, s in chunks)
    F['chunks_per_file'] = dict(collections.Counter(c[0] for c in chunks))
    F['mean_chunk_words'] = F['policy_words'] / len(chunks)
    docs = [tokens(s) for _, s in chunks]
    vocab = sorted({w for d in docs for w in d})
    idx = {w: i for i, w in enumerate(vocab)}
    X = np.zeros((len(docs), len(vocab)))
    for i, d in enumerate(docs):
        for w in d:
            X[i, idx[w]] += 1
    df = (X > 0).sum(axis=0)
    idf = np.log(len(docs) / df)
    T = X * idf
    T = T / np.maximum(np.linalg.norm(T, axis=1, keepdims=True), 1e-9)
    F.update(vocab=vocab, idx=idx, V=len(vocab), X=X, T=T, idf=idf, docs=docs)

    def vec(text):
        v = np.zeros(len(vocab))
        for w in tokens(text):
            if w in idx:
                v[idx[w]] += 1
        v = v * idf
        nv = np.linalg.norm(v)
        return v / nv if nv else v

    def rank_tfidf(q):
        sc = T @ vec(q)
        o = np.argsort(-sc, kind='stable')
        return o, sc

    def rank_overlap(q):
        qs = set(tokens(q))
        sc = np.array([len(qs & set(d)) for d in docs], float)
        o = np.argsort(-sc, kind='stable')
        return o, sc
    F['vec'], F['rank_tfidf'], F['rank_overlap'] = vec, rank_tfidf, rank_overlap
    rel = []
    for q, f, a in TESTS:
        r = {i for i, (nm, s) in enumerate(chunks) if a in s}
        assert len(r) == 1 and chunks[next(iter(r))][0] == f, q
        rel.append(r)
    F['rel'] = rel

    def pk(order, r, k):
        hit = len(set(order[:k]) & r)
        return hit / k, hit / len(r)
    for key, rk in (('tfidf', rank_tfidf), ('overlap', rank_overlap)):
        res = {}
        for k in (1, 3, 5):
            vals = [pk(rk(q)[0], r, k) for (q, f, a), r in zip(TESTS, rel)]
            res[k] = (float(np.mean([v[0] for v in vals])), float(np.mean([v[1] for v in vals])))
        F['pr_' + key] = res
        F['rank_of_right_' + key] = [int(np.where(rk(q)[0] == next(iter(r)))[0][0]) + 1 for (q, f, a), r in zip(TESTS, rel)]
    F['top1_file_ok'] = [chunks[rank_tfidf(q)[0][0]][0] == f for q, f, a in TESTS]
    F['top1_hit'] = [rk == 1 for rk in F['rank_of_right_tfidf']]
    F['n_top1'] = int(sum(F['top1_hit']))
    F['n_fail'] = len(TESTS) - F['n_top1']
    F['fail_idx'] = [i for i, h in enumerate(F['top1_hit']) if not h]
    # worked examples
    o, sc = rank_tfidf(Q_RET)
    F['ret_rows'] = [(int(i) + 1, chunks[i][0], chunks[i][1], float(sc[i])) for i in o[:3]]
    F['ret_rel'] = [i in rel[1] for i in o[:3]]
    for key, q, ix in (('f1', Q_FAIL1, 0), ('f2', Q_FAIL2, 3)):
        o, sc = rank_tfidf(q)
        F[key] = dict(q=q, top=[(chunks[i][0], chunks[i][1], float(sc[i])) for i in o[:3]], rank=F['rank_of_right_tfidf'][ix], right=chunks[next(iter(rel[ix]))][1])
    F['pk_ret'] = {k: pk(rank_tfidf(Q_RET)[0], rel[1], k) for k in (1, 3, 5)}
    F['pk_f1'] = {k: pk(rank_tfidf(Q_FAIL1)[0], rel[0], k) for k in (1, 3, 5)}
    # illustrative ranked list for the precision and recall picture (made-up relevance)
    F['ill_rank'] = [True, False, True, False, False]
    F['ill_total_rel'] = 3
    F['ill_p5'] = sum(F['ill_rank']) / 5
    F['ill_r5'] = sum(F['ill_rank']) / F['ill_total_rel']
    # a tiny language model: which word follows 'was' in the 800 feedback messages
    fb = pd.read_csv(DATA / 'feedback.csv')
    bi = collections.Counter()
    for m in fb.message:
        w = re.findall(r'[a-z]+', m.lower())
        for a, b in zip(w, w[1:]):
            bi[(a, b)] += 1
    ctx = 'was'
    c = {b: v for (a, b), v in bi.items() if a == ctx}
    tot = sum(c.values())
    top = sorted(c.items(), key=lambda x: (-x[1], x[0]))[:5]
    F['bi_ctx'], F['bi_total'], F['bi_distinct'] = ctx, tot, len(c)
    F['bi_top'] = [(w_, v, v / tot) for w_, v in top]
    F['bi_other'] = 1 - sum(p for _, _, p in F['bi_top'])
    # temperature (illustrative logits)
    F['temp'] = {t: [float(p) for p in softmax_t(TEMP_LOGITS, t)] for t in (0.5, 1.0, 2.0)}
    # context window pieces (words of the grounded prompt for Q_RET)
    o, sc = rank_tfidf(Q_RET)
    top3 = [chunks[i][1] for i in o[:3]]
    F['top3_words'] = sum(len(t_.split()) for t_ in top3)
    F['sys_words'] = len(SYSTEM_PROMPT.split())
    F['q_words'] = len(Q_RET.split())
    F['prompt'] = build_prompt(Q_RET, top3)
    F['prompt_words'] = len(F['prompt'].split())
    # loyalty file as chunks for the chunking figure
    F['loyalty_chunks'] = [s for nm, s in chunks if nm == 'loyalty_programme.txt']
    # recipe output
    import contextlib
    import io
    ns = dict(np=np, vec=vec, T=T, chunks=chunks)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(RECIPE, ns)
    F['recipe_out'] = buf.getvalue().strip()
    # audit log example (illustrative entries)
    return F


def build():
    F = facts()
    ch = F['chunks']
    pt, po = F['pr_tfidf'], F['pr_overlap']
    f1, f2 = F['f1'], F['f2']
    bi = F['bi_top']
    tp = F['temp']
    assert F['n_chunks'] == 59 and F['n_top1'] == 10 and F['fail_idx'] == [0, 3]
    sess = dict(
        num=22, block='Module E: Neural networks and text', short_title='Language models and building with them',
        title='Language models and building with them',
        question='What does a language model do, how do we test one, and how do we make it answer from our own documents?',
        outcomes=['Explain tokens, the context window, prompts and hallucination in plain words',
                  'Build retrieval over a small document set and score it with precision at k and recall at k',
                  'Use AI tools safely: protect customer data and record AI-assisted work in an audit log'],
        outcome_icons=['speech', 'magnifier', 'shield'],
        outcome_note=('Here is what you can do by the end of today. You can explain tokens, the context window, prompts and hallucination in plain words. '
                      'You can build retrieval over a small set of documents and score it with precision at k and recall at k, using an evaluation set you write yourself. '
                      'And you can use AI tools safely: you know what not to paste into a tool you do not control, and you know how to record AI-assisted work in an audit log. All of it runs on the eight Lakeside Mart policy documents.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: picture, plain words, one example by hand'), (10, 'Break'), (45, 'Lab: predict, run, read, change'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: concepts first, then a Python lab on policy documents',
        plan_caption='Pictures and plain words first. Then you open the notebook. Then the checks and what you keep.',
        plan_note=('Two hours, in the same shape as before. Ten minutes of recall and the question of the day. Then forty-five minutes of concepts with laptops closed. '
                   'After the break, forty-five minutes in a Colab notebook: you split the policies into chunks, build a retrieval function, write and score an evaluation set, and build a grounded prompt. '
                   'An optional last cell runs a small open model. The final ten minutes are an exit check and what you keep. Please protect the lab time.'),
        recall_from='Session 21',
        recall=[('Why must text become numbers before a model can compare two messages?', 'A model only does arithmetic. A bag of words, TF-IDF or an embedding gives each message a vector it can measure.'),
                ('What does TF-IDF do to a word that is found in almost every message?', 'It gives the word a weight near zero, so rare words count more.'),
                ('What is semantic search meant to find that a keyword search misses?', 'Messages with a similar meaning but different words, such as crowded cashier and a long queue.')],
        words=[('Token and context window', 'A token is a word or piece of a word that a language model reads and writes. The context window is how many tokens it can read at once.'),
               ('Prompt (system prompt, zero-shot, few-shot)', 'The instruction you give a model. A system prompt sets rules. Zero-shot gives no examples. Few-shot gives a few worked examples.'),
               ('Hallucination', 'Fluent text that no source supports. It can read well and still be false.'),
               ('Retrieval-augmented generation (RAG)', 'Find the relevant chunks of your documents first (retrieval and ranking), then ask the model to answer from them (grounding).'),
               ('Evaluation set (precision at k, recall at k)', 'A labelled list of test questions with the right passage. Precision at k and recall at k score the search.')],
        word_icons=['speech', 'doc', 'question', 'magnifier', 'check'],
        words_note=('Five words for today. A token is the piece of text a language model reads, and the context window is how many tokens it can read at once. A prompt is your instruction, and a system prompt sets the rules. '
                    'Hallucination is fluent text that no source supports. Retrieval-augmented generation, or RAG, finds the relevant chunks of your documents first and then asks the model to answer from them. '
                    'And an evaluation set is a labelled list of test questions that lets you score the search with precision at k and recall at k.'),
        keep='Keep your notebook and, in the folder keep, eval_results.csv (your evaluation set with its scores) and audit_log.csv (what you asked an assistant, what it gave and how you checked it).',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab file', value='eval_results.csv'), dict(label='Your record', value='audit_log.csv'), dict(label='Next session', value='Ship it')]),
        keep_title='Save your notebook, your scores and your audit log',
        next='Session 23: Ship it. We make work reproducible, save a model, build a small app and write a model card.', next_label='Next session',
        keep_note=('Before you go, save your notebook and the two files you made in the folder called keep: eval results dot csv and audit log dot csv. The first shows how well your search works, question by question. '
                   'The second is the habit I want you to keep: whenever an assistant helps you, write down what you asked, what it gave and how you checked it. '
                   'Next session we turn notebooks into something a colleague can run and trust. Bring one document set from your own work that you could search.'),
        cover_note=('Welcome back. Last session we turned customer messages into numbers. Today we look at the technology behind chat assistants: language models. '
                    'You will see what they actually do, why they sometimes invent things, and how to make one answer from your own documents. '
                    'We build the search part ourselves in plain Python over the eight Lakeside Mart policies, and we test it with a list of twelve questions.'),
        use_at_work='Make an assistant answer from your own documents, test the search, and keep an audit log of AI-assisted work.',
        slides=[])
    S = sess['slides']

    # 1 answers
    S.append(dict(kind='table', title='Answers to the three questions from Session 21', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in sess['recall']], widths=[5.0, 7.0], icons=['calculator', 'chart', 'magnifier'],
                  notes=('Here are the answers to the three warm-up questions. A model only does arithmetic, so a message must become a vector first, by counting words, by TF-IDF or by an embedding. '
                         'TF-IDF gives a word that appears in almost every message a weight near zero, so rare words count more. And semantic search aims to find messages with a similar meaning but different words. '
                         'I say aims, because you check that claim yourself with a precision score. Which answer needs more practice?')))

    # 2 tokens
    S.append(dict(kind='wide', title='A language model reads and writes tokens: words, pieces of words and punctuation',
                  visual=dict(kind='k_tokens', tokens=['Lake', 'side', 'points', 'expire', 'after', '12', 'months', '.'], ids=[4721, 1873, 5390, 8802, 2204, 612, 3157, 13], words=6),
                  caption='Illustrative split and made-up numbers. A real tokeniser cuts and numbers text in its own way.',
                  notes=('A language model does not read letters or whole sentences. It reads tokens. A token is a word, a piece of a word or a punctuation mark, and each token has a number in the model\'s list. '
                         'Tokenisation is the step that cuts text into tokens. In this picture, Lakeside is cut into Lake and side, and the full stop is its own token. The split and the numbers are made up to show the idea, because every model has its own list. '
                         'Notice that six words became eight tokens. Models, prices and limits are counted in tokens. Why might a long word cost more tokens?')))

    # 3 next token
    S.append(dict(kind='idea', title='Next-token prediction: the model scores every possible next token and picks one',
                  visual=dict(kind='k_nextword', context='The queue was ...', items=[[w, round(p, 3)] for w, v, p in bi], other=round(F['bi_other'], 3), note=f'Counts of the word after "{F["bi_ctx"]}" in all {F["bi_total"]} cases in feedback.csv. The heading is only an example.'),
                  lead='A language model is trained to predict the next token from the tokens before it.',
                  points=['The bars come from counting our own 800 messages.', 'A large model does the same job with a neural network that reads the whole context.', 'It scores every token it knows, then picks one.'],
                  notes=(f'The core job of a language model is next-token prediction. To show the idea, I built a tiny model from our eight hundred feedback messages. It only counts which word follows was. After was, the word not came {bi[0][1]} times out of {F["bi_total"]}, charged {bi[1][1]} times, and so on. '
                         f'That is {F["bi_distinct"]} different words, with no clear winner. A large language model does the same job, but it uses a neural network that reads the whole context. '
                         'Published research describes such models as trained to predict the next token. Why would one word of context make a poor predictor?')))

    # 4 loop
    S.append(dict(kind='steps', title='One answer is built one token at a time: read, score, pick, add, repeat',
                  steps=[dict(head='Read', text='The prompt so far', icon='doc'), dict(head='Score', text='Every possible next token', icon='calculator'), dict(head='Pick', text='One token', icon='pin'), dict(head='Add', text='It joins the text', icon='pen'), dict(head='Repeat', text='Until it stops', icon='clock')],
                  highlight=None, caption='A 40-token answer means 40 trips round this loop.',
                  notes=('Here is the loop behind every answer from a chat assistant. The model reads the text so far, which is your prompt and anything it has already written. It scores every possible next token. It picks one. '
                         'The picked token is added to the text, and the loop starts again with one more token to read. It stops when it picks a token that means stop. '
                         'So a long answer is many small guesses in a row, each one made from everything written so far. Nothing in the loop looks a fact up. Which step do you think makes the same question give two different answers?')))

    # 5 context window
    S.append(dict(kind='wide', title='The context window limits how many tokens a model can read at once, so we send only what matters',
                  visual=dict(kind='k_context', big_label='Whole document library: thousands of pages (hypothetical)', small=[['Rules', F['sys_words']], ['3 chunks', F['top3_words']], ['Question', F['q_words']]],
                              small_label=f'What retrieval sends: {F["prompt_words"]} words ({F["sys_words"] + F["top3_words"] + F["q_words"]} in the boxes plus {F["prompt_words"] - F["sys_words"] - F["top3_words"] - F["q_words"]} label words)', window_label='Context window (size depends on the model: check its documentation)'),
                  caption='Prompt, pasted text and answer share one window. Word counts: our grounded prompt.',
                  notes=(f'The context window is how many tokens a model can read at once. Everything counts against it: your prompt, any text you paste, and the answer so far. Window sizes differ between models and keep changing, so check the documentation of the one you use. '
                         f'The top bar is a whole document library, which is hypothetical here, and it would not fit in any window. The bottom bar is what retrieval sends for one question in our lab: a short rule, three chunks and the question, {F["prompt_words"]} words in total. '
                         'That is the idea behind retrieval. Why would sending less text sometimes give a better answer?')))

    # 6 prompts
    S.append(dict(kind='table', title='A prompt is your instruction: a system prompt sets rules, and examples turn zero-shot into few-shot',
                  headers=['Kind', 'What it is', 'Example from Lakeside Mart'],
                  rows=[['System prompt', 'Rules and role, set once for the whole conversation', 'Answer only from the passages. If the answer is missing, say so.'],
                        ['Zero-shot prompt', 'A task with no worked examples', 'Label this message as positive, neutral or negative: Slow service at the counter.'],
                        ['Few-shot prompt', 'A task with a few worked examples first', 'Fast checkout. Label: positive. Charged twice. Label: negative. Is milk available? Label:']],
                  widths=[2.4, 4.4, 5.2], icons=['shield', 'doc', 'notebook'],
                  notes=('A prompt is the instruction you give a model. A system prompt sets rules and a role once, for example answer only from the passages. '
                         'A zero-shot prompt gives the task with no examples. A few-shot prompt puts a few worked examples first, so the model sees the pattern before the real case. '
                         'These are different ways of writing the input. They change what the model is likely to write, but they do not make it check a fact. The examples on the slide are from our feedback data. Which kind would you try first for labelling messages?')))

    # 7 temperature
    S.append(dict(kind='idea', title='Temperature is a setting that makes the next-token pick more repeatable or more varied',
                  visual=dict(kind='k_temperature', words=TEMP_WORDS, groups=[[0.5, [round(p, 3) for p in tp[0.5]]], [1.0, [round(p, 3) for p in tp[1.0]]], [2.0, [round(p, 3) for p in tp[2.0]]]]),
                  lead='Many tools offer a setting called temperature. Check the tool documentation for what it does there.',
                  points=['Low temperature: the top token wins more often.', 'High temperature: the choice spreads out.', 'Illustrative made-up scores for The queue was ...'],
                  notes=('Temperature is a setting that many tools expose, and I only want you to know the name and the idea. Check the documentation of your own tool, because the details differ. '
                         'In general, a low temperature makes the model pick the most likely token more often, so answers are more repeatable. A high temperature spreads the choice, so answers vary more. '
                         'The picture uses made-up scores for four words after The queue was. At temperature one half the top word gets about eighty percent. At two it gets about forty two percent. For a policy answer, which would you want?')))

    # 8 hallucination
    S.append(dict(kind='compare', title='Hallucination: a model can write a fluent answer that no source supports',
                  left=dict(head='No policy given', points=['Question: How long do points last?', 'A model can still write a smooth answer with a guessed number of months (hypothetical).', 'Nothing can be checked.']),
                  right=dict(head='Policy passage given', points=['Passage: Points expire after 12 months.', 'The answer can quote the passage.', 'You can check it against the source.']),
                  verdict='Give the model the source. Check the answer.',
                  notes=('Hallucination means fluent text that no source supports. The model writes likely text, so if the policy is not in its prompt, it can still write a smooth answer, perhaps with a guessed number of months. The left example is hypothetical: I did not run a model. '
                         'On the right, the passage Points expire after twelve months is in the prompt. Now the answer can quote it, and you can check it against the source. '
                         'That is the whole idea of retrieval-augmented generation. Hallucination does not disappear, but it becomes checkable. Which of your own documents would you want an assistant to answer from?')))

    # 9 RAG overview
    S.append(dict(kind='steps', title='Retrieval-augmented generation (RAG) finds the relevant chunks first, then answers from them',
                  steps=[dict(head='Chunk', text='Split documents into pieces', icon='doc'), dict(head='Retrieve', text='Find the closest chunks', icon='magnifier'), dict(head='Rank', text='Sort by similarity, keep top k', icon='chart'),
                         dict(head='Ground', text='Put them in the prompt', icon='pen'), dict(head='Answer and check', text='Compare with the source', icon='check')], highlight=None,
                  caption='We build the first three steps in numpy today, and score them with an evaluation set.',
                  notes=('This is the whole RAG pattern. First, chunking: split the documents into short pieces. Second, retrieval: find the chunks closest to the question. Third, ranking: sort them by similarity and keep the top k. '
                         'Fourth, grounding: put those chunks in the prompt and tell the model to answer only from them. Fifth, the model answers and you check the answer against the source chunk. '
                         'Today we build the first three steps ourselves, in plain numpy, and we measure how well they work. Why do we need to measure retrieval separately from the answer?')))

    # 10 chunking
    S.append(dict(kind='wide', title=f'Chunking splits each document into short pieces: the {F["n_files"]} policies become {F["n_chunks"]} chunks',
                  visual=dict(kind='k_chunks', title='loyalty_programme.txt', chunks=F['loyalty_chunks'], total=f'{F["n_chunks"]} chunks in all, about {F["mean_chunk_words"]:.0f} words each ({F["policy_words"]} words)'),
                  caption='Here one sentence is one chunk. Small chunks are precise. Large ones keep context.',
                  notes=(f'Chunking means splitting a document into pieces that can be found and sent separately. Here the loyalty policy has {len(F["loyalty_chunks"])} chunks, one per sentence. Across all {F["n_files"]} policy files we get {F["n_chunks"]} chunks of about {F["mean_chunk_words"]:.0f} words each. '
                         'Chunk size is a design choice. Small chunks are precise but can lose context. Large chunks keep context but bring in unrelated text and use more of the context window. '
                         'Each chunk keeps its file name, so we can say where an answer came from. Would you ever split a contract differently from a menu?')))

    # 11 retrieval and ranking
    rr = F['ret_rows']
    S.append(dict(kind='table', title='Retrieval scores every chunk against the question, and ranking keeps the top k',
                  headers=['Rank', 'Chunk (file)', 'Cosine score'],
                  rows=[[str(i + 1), f'{r[2]} ({r[1]})', f'{r[3]:.2f}'] for i, r in enumerate(rr)], widths=[1.1, 8.6, 2.3], icons=['check', 'cross', 'cross'],
                  note=f'Question: "{Q_RET}" TF-IDF cosine similarity over {F["n_chunks"]} chunks and a vocabulary of {F["V"]} different words, as in Session 21.',
                  notes=(f'Here is retrieval on one question: how many days do I have to return an item? We use the same TF-IDF and cosine similarity as last session, now over the {F["n_chunks"]} chunks. Every chunk gets a score, and ranking sorts them. '
                         f'The top chunk, from the returns policy, scores {rr[0][3]:.2f} and contains the answer: within seven days. The second and third chunks only share words such as return and customer, so they are wrong. '
                         'This is keyword retrieval, because it matches words. Retrieval based on embeddings works the same way with different vectors. How would you know the second chunk is wrong without reading it?')))

    # 12 grounding
    S.append(dict(kind='example', title='Grounding: put the retrieved chunk in the prompt and tell the model to answer only from it',
                  scenario='A grounded prompt with k = 1. The lab builds the same prompt with k = 3.',
                  blocks=[dict(label='System prompt', text=SYSTEM_PROMPT), dict(label='Passage', text=rr[0][2]), dict(label='Question', text=Q_RET)],
                  notes=('Grounding means tying the answer to retrieved text. The prompt has three parts. The system prompt tells the model to answer only from the passages, and to say so if the answer is missing. '
                         f'The passage is the top chunk from retrieval, which is the returns policy sentence. And the question is the learner question. In the lab you build this prompt for the top three chunks, which is {F["prompt_words"]} words. '
                         'The instruction to say I could not find that is important, because it gives the model a safe way out. A model might still ignore an instruction, so you still check the answer. What could go wrong if the retrieved chunk is wrong?')))

    # 13 evaluation set
    S.append(dict(kind='table', title='An evaluation set is a labelled list of test questions with the right passage for each', headers=['Question', 'Right policy file'],
                  rows=[[q, f_] for q, f_, a in TESTS], widths=[5.4, 4.6], split=True,
                  notes=('To know whether retrieval works, you need an evaluation set: a labelled test set of questions where you know the right passage in advance. Here are twelve questions, with the policy file that holds the answer. '
                         'For each one, I copied the answer sentence word for word from the file, and the code confirms that exactly one chunk contains it. That chunk is the relevant chunk. '
                         'Twelve is a small set, so treat the scores as a first look: one question moves a score by 0.08, so write thirty or more before you choose between methods. You write more in the lab. A good evaluation set includes easy and hard questions. Which of these would you expect to be hard for a keyword search?')))

    # 14 precision and recall at k picture
    S.append(dict(kind='idea', title='Precision at k and recall at k score the top k results of a search',
                  visual=dict(kind='k_rank', items=[[i + 1, ['Chunk A', 'Chunk B', 'Chunk C', 'Chunk D', 'Chunk E'][i], bool(r)] for i, r in enumerate(F['ill_rank'])], total_rel=F['ill_total_rel'], k=5),
                  lead='Precision at k: how many of the top k results are right. Recall at k: how many of all the right chunks were found.',
                  points=['Illustrative: 3 chunks are right in total.', f'Top 5 hold 2 of them: precision at 5 = 2/5 = {F["ill_p5"]:.1f}.', f'Recall at 5 = 2/3 = {F["ill_r5"]:.2f}.'],
                  notes=(f'Here is a made-up ranked list. The search returned five chunks, and the gold ones are the relevant chunks. Three chunks in the library are right in total, and the top five hold two of them. '
                         f'Precision at k is the share of the k results that are right: two out of five, which is {F["ill_p5"]:.1f}. Recall at k is the share of all the right chunks that were found: two out of three, which is {F["ill_r5"]:.2f}. '
                         'Precision tells you how clean the results are. Recall tells you how much you missed. Which one matters more when a wrong chunk can lead to a wrong answer?')))

    # 15 formulas
    S.append(dict(kind='formula', title='Precision at k and recall at k are two ratios of the same count',
                  formulas=[('Precision at k', r'$P@k=\frac{\mathrm{relevant\ in\ top\ }k}{k}$'), ('Recall at k', r'$R@k=\frac{\mathrm{relevant\ in\ top\ }k}{\mathrm{all\ relevant}}$')],
                  symbols=[['k', 'How many top results we look at', 'Here k = 3'], ['Relevant in top k', 'Results in the top k that contain the answer', '1 of 3 (return question)'],
                           ['All relevant', 'Chunks that contain the answer', '1 per question here'], ['Worked', 'Return question', f'P@3 = 1/3 = {F["pk_ret"][3][0]:.2f}, R@3 = 1/1 = {F["pk_ret"][3][1]:.2f}'],
                           ['Worked', 'Points question', f'right chunk at rank {f1["rank"]}: P@3 = {F["pk_f1"][3][0]:.0f}, R@3 = {F["pk_f1"][3][1]:.0f}']],
                  widths=[2.0, 5.6, 4.3], size=20,
                  notes=(f'Here are the two formulas. Precision at k divides the number of relevant chunks in the top k by k. Recall at k divides it by the number of all relevant chunks. '
                         f'Worked example one: for the return question, the right chunk is at rank one, so among the top three there is one right chunk. Precision at three is one third, {F["pk_ret"][3][0]:.2f}, and recall at three is one out of one, {F["pk_ret"][3][1]:.2f}. '
                         f'Worked example two: for how long do points last, the right chunk is only at rank {f1["rank"]}, so the top three hold none, and both scores are zero. With one right chunk per question, recall at k is the same as asking whether it is in the top k. Why is precision at three limited to one third here?')))

    # 16 results
    S.append(dict(kind='idea', title=f'On our twelve questions, keyword retrieval puts the right chunk first {F["n_top1"]} times',
                  visual=dict(kind='k_prk', groups=[[k, round(pt[k][0], 3), round(pt[k][1], 3)] for k in (1, 3, 5)]),
                  lead=f'Precision at 1 is {pt[1][0]:.2f}. Recall at 5 is {pt[5][1]:.2f}.',
                  points=['Mean over 12 questions, TF-IDF cosine retrieval.', 'Precision falls as k grows, because only one chunk is right.', 'Recall rises as k grows.'],
                  notes=(f'These are the real scores of our TF-IDF retrieval over the twelve questions. At k equal one, precision and recall are both {pt[1][0]:.2f}: the right chunk was first for {F["n_top1"]} of twelve questions. '
                         f'At k equal three, precision is {pt[3][0]:.2f} and recall is {pt[3][1]:.2f}. At five, recall reaches {pt[5][1]:.2f}, so the right chunk is always in the top five. '
                         'Precision falls as k grows because only one chunk per question is right. So the choice of k is a trade-off: a larger k finds more but sends more text to the model. Which k would you choose for a customer assistant?')))

    # 17 failures
    S.append(dict(kind='table', title='Read the failures: two questions whose right chunk is not first, and why',
                  headers=['Question', 'Top result', 'Why it failed'],
                  rows=[[f1['q'], f'{f1["top"][0][1]} ({f1["top"][0][0]})', f'The word last matches last purchase. The right chunk, Points expire after 12 months, says expire. It is at rank {f1["rank"]}.'],
                        [f2['q'], f'{f2["top"][0][1]} ({f2["top"][0][0]})', f'The title chunk repeats the word delivery. The right chunk is at rank {f2["rank"]}.']],
                  widths=[3.3, 4.2, 4.5], icons=['cross', 'cross'],
                  note='Fixes to try: drop title chunks, add synonyms, or use embeddings. Then score again on the same set.',
                  notes=(f'Always read the failures. For how long do points last, the top result is about data privacy, because the word last also appears in last purchase. The policy says expire, a different word for the same idea, so a keyword search cannot connect them. The right chunk is at rank {f1["rank"]}. '
                         f'For which towns does delivery not reach, the top result is the title chunk, Lakeside Mart Delivery, which repeats the word delivery. The right chunk is at rank {f2["rank"]}. '
                         'Both fixes are cheap to try: drop the title chunks, or use embeddings, which are built for different words with the same meaning. Then you score again on the same set. Why must you keep the set fixed while you test a fix?')))

    # 18 small model locally
    S.append(dict(kind='steps', title='A small open model can run inside your own Colab notebook to write the grounded answer',
                  steps=[dict(head='Pick', text='SmolLM2 360M, Apache 2.0', icon='key'), dict(head='Load', text='Download once in Colab (check current limits)', icon='folder'), dict(head='Build', text='The grounded prompt from the top k chunks', icon='pen'),
                         dict(head='Generate', text='A short answer', icon='gear'), dict(head='Check', text='Compare it with the source chunk', icon='check')], highlight=None,
                  caption='Optional lab step. Small models can be wrong or ignore rules, so checking is not optional.',
                  notes=('This is the last piece of RAG: generation. You can run a small open model inside your own Colab notebook, with no account and no paid service. We use SmolLM2 360M Instruct, a small open model whose model card lists the Apache 2.0 licence, and you should read the model card for any model you use at work. '
                         'Colab limits change, so check the current ones. You download the model once, build the grounded prompt from the top chunks, and generate a short answer. No model output appears in this deck, because it was not run when the deck was written. '
                         'Small models can be wrong or ignore your rules, so the last step is always to check against the source chunk. What would you compare?')))

    # 19 privacy
    S.append(dict(kind='table', title='Do not paste customer data into tools you do not control',
                  headers=['What you want to paste', 'Into a tool you do not control?', 'What to do instead'],
                  rows=[['Customer names, phone numbers, loan files', 'No', 'Remove or mask them first. Use customer numbers.'], ['Passwords, keys and staff records', 'No', 'Keep them out of every prompt.'],
                        ['Public text, such as our eight policies', 'Usually fine', 'Check your organisation\'s rule first.'], ['A made-up example with the same shape', 'Yes', 'Test the prompt on fake data, then run on real data inside your own system.']],
                  widths=[4.1, 3.0, 4.9], icons=['person', 'key', 'doc', 'check'],
                  note='My understanding: under the Uganda Data Protection and Privacy Act, 2019 the data controller is responsible. Sending personal data abroad may need safeguards. Ask your data officer. Not legal advice.',
                  notes=('A simple rule: do not paste customer data into tools you do not control. Customer names, phone numbers and loan files should be removed or masked first, as we did with a regex in Session 21. '
                         'Passwords, keys and staff records stay out of every prompt. Public text, like our policies, is usually fine, but check your organisation\'s rule. A made-up example with the same shape is always safe for testing. '
                         'My understanding is that under the Uganda Data Protection and Privacy Act of 2019 the data controller is responsible for personal data, so ask your data officer. The regulator, as I understand it, is the Personal Data Protection Office. Sending personal data to a service outside Uganda may need extra safeguards, which applies to free chat tools and to Colab. This is not legal advice. Which of your own files would fail this test?')))

    # 20 AI-assisted coding
    S.append(dict(kind='steps', title='AI-assisted coding is safe when you use it, check it and record it',
                  steps=[dict(head='Ask', text='Describe the task in plain words, with no customer data', icon='speech'), dict(head='Read', text='Read every line before you run it', icon='magnifier'), dict(head='Run', text='Test on a tiny example whose answer you know', icon='gear'),
                         dict(head='Check', text='Compare with your own number', icon='calculator'), dict(head='Record', text='Write it in the audit log', icon='notebook')], highlight=None,
                  caption='An assistant can write code that runs and is still wrong. You are responsible for the result.',
                  notes=('Many analysts now use an AI assistant to write code. That is fine when you follow five steps. Ask in plain words, and never include customer data. Read every line before you run it. Run it on a tiny example whose answer you already know. '
                         'Check the result against your own number, the way you recompute a figure an assistant gives you. And record it in an audit log, also called a prompt log. '
                         'Code that runs without an error can still be wrong, and you are the one who signs the report. In this course an assistant is optional help. Which of the five steps do people skip most?')))

    # 21 audit log
    S.append(dict(kind='table', title='An audit log records what you asked, what you got and how you checked it',
                  headers=['What I asked', 'What it gave', 'How I checked', 'Decision'],
                  rows=[['Split a policy text into sentences', 'A regex split', 'Counted 59 chunks and matched two by hand', 'Used it'], ['Explain recall at k', 'A short explanation', 'Recomputed P@k and R@k in numpy', 'Kept the explanation'],
                        ['Group sales by branch in pandas', 'Code with a wrong column name', 'It raised an error', 'Fixed it and noted it']],
                  widths=[3.6, 2.9, 3.5, 2.0], icons=['notebook', 'notebook', 'notebook'], note='Illustrative entries. Your lab saves audit_log.csv with the same columns.',
                  notes=('Here is an audit log, also called a prompt log. Each row records what you asked, what the assistant gave, how you checked it and what you decided. The three entries are illustrative. '
                         'The first split the policy text into sentences, and the check was counting fifty nine chunks and matching two by hand. The third gave code with a wrong column name, the error caught it, and the entry says so. '
                         'A log like this protects you: if someone asks where a number came from, you can show the steps. It takes one minute per entry. In the lab you create one. What would you write after your first entry?')))

    # 22 use at work
    S.append(dict(kind='table', title='Where you will use this at work: answer questions from your own documents, and test the answers',
                  headers=['Your job', 'The documents you meet', 'What today lets you do'],
                  rows=[['Compliance analyst at a bank, using Python', 'Internal policies and circulars', 'Find the right paragraph for a question and show its source, with a recall score.'],
                        ['Customer support lead at a retailer', 'FAQ and returns policy', 'Give agents the right chunk, and test the search on a list of real questions.'],
                        ['Records officer at a ministry', 'Regulations and circulars', 'Build a searchable index, then measure precision at k before you share it.'],
                        ['Programme officer at an NGO', 'Project reports', 'Keep an audit log of every AI-assisted summary and check each one against the report.']],
                  widths=[3.7, 3.3, 5.0], icons=['coin', 'people', 'folder', 'notebook'],
                  notes=('Where will you use this on Monday? A compliance analyst at a bank can find the right paragraph for a question in internal policies and show its source, with a recall score to prove the search works. '
                         'A customer support lead at a retailer can give agents the right chunk, and test the search on a list of real questions. A records officer at a ministry can build a searchable index and measure precision at k before sharing it. '
                         'A programme officer at an NGO can keep an audit log of every AI-assisted summary. These are example jobs. Which is closest to yours?')))

    # 23 bridge
    S.append(dict(kind='code', title='Read the recipe before the lab: four lines rank the chunks for one question',
                  code=RECIPE, output=F['recipe_out'].splitlines(),
                  reads=['First, vec, T and chunks come from lab steps 1 and 2. Line 1: the question becomes a TF-IDF vector.', 'Line 2: one cosine score per chunk.', 'Line 3: keep the three highest, the top k.', 'Lines 4 and 5: print score and chunk start.'],
                  notes=('Before the lab, read the recipe. Line one turns the question into a TF-IDF vector, using the function vec that you build in lab step two, the same idea as last session. Line two multiplies the matrix of chunk vectors by the question vector, which gives one cosine score for every chunk. '
                         'Line three sorts the scores and keeps the top three. Lines four and five print each score with the beginning of the chunk. '
                         'The output below is real. It is the question how long do points last, and you can see the top result starts Data is kept for 3 years, the data privacy chunk about the last purchase. That is the failure we read earlier. What would you change to fix it?')))

    # 24 divider
    S.append(dict(kind='divider', title='Part 2: the Python lab', lead='Close the slides. Open the notebook.', section='Lab',
                  notes=('That is the end of the ideas. Everything you need is on the slides you have just seen, and the notebook repeats each step. '
                         'Open the Colab notebook for Session 22 and run the first two cells. They put the policy files next to the notebook and load the check helper. '
                         'In every step, predict first, run the cell, read the output, and then change one thing. A check line tells you whether your number matches. I will walk around.')))

    # 25 lab map
    S.append(dict(kind='steps', title='The lab has five parts, and you keep an evaluation file and an audit log',
                  steps=[dict(head='1 Chunk', text='Split 8 policies', icon='doc'), dict(head='2 Retrieve', text='TF-IDF cosine, top k', icon='magnifier'), dict(head='3 Evaluate', text='Precision and recall at k', icon='chart'),
                         dict(head='4 Ground', text='Build the prompt', icon='pen'), dict(head='5 Record', text='Optional model, audit log', icon='notebook')], highlight=None,
                  caption='Five parts, ten tasks in 45 minutes. In each one: predict, run, read the output, change one thing.',
                  notes=('Here is the map of the lab. Part one, split the eight policies into chunks. Part two, build the TF-IDF matrix and a retrieve function that returns the top k chunks. '
                         'Part three, run the evaluation set of twelve questions, compute precision at k and recall at k, and read the failures. Part four, build the grounded prompt. '
                         'Part five, optionally run a small open model on it, then write your audit log and save your files. If time is short, finish parts one to four and take part five home. Predict first in every step.')))

    # 26 check numbers
    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Chunks and words in the eight policy files', f'{F["n_chunks"]} and {F["policy_words"]}'], ['Vocabulary size of the chunks (after stop words)', f'{F["V"]}'],
                        ['Cosine score of the top chunk for the return question', f'{rr[0][3]:.2f}, from returns_policy.txt'], ['Mean precision at 1 and recall at 1 (12 questions)', f'{pt[1][0]:.3f} and {pt[1][1]:.3f}'],
                        ['Mean precision at 3 and recall at 3', f'{pt[3][0]:.3f} and {pt[3][1]:.3f}'], ['Plain word overlap (count of shared question words), mean precision at 3', f'{po[3][0]:.3f}'],
                        ['Rank of the right chunk for how long do points last', f'{f1["rank"]}'], ['Words in the grounded prompt for the return question (k = 3)', f'{F["prompt_words"]}']],
                  widths=[7.6, 4.4], icons=['doc', 'grid', 'magnifier', 'check', 'chart', 'gear', 'cross', 'pen'], note='If your number differs, find the step that went wrong. Do not change a number to match.',
                  notes=('Use this table as your own self-check. Nobody marks it. If your numbers match, carry on. If one does not, stop and call me, because later steps use the earlier ones. '
                         'The most common cause is a chunk splitter that differs slightly, which changes the number of chunks and every score after it. Another is forgetting that rank counts from one. '
                         'Do not change a number to make it match. Find out why it is different. What would more chunks do to precision at three?')))

    # 27 error cards
    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[[f'More than {F["n_chunks"]} chunks', 'The splitter also cut after abbreviations or headings.', 'Split only after a full stop that is followed by a capital letter.'],
                        ['FileNotFoundError: policies', 'The policy folder is not next to the notebook.', 'Run the first cell again and check that data.zip was unpacked.'],
                        ['Precision at 3 is 1.0', 'You divided by the number of relevant chunks.', 'Precision divides by k. Recall divides by all relevant.'],
                        ['Every score is 0.0', 'The question has no word in the vocabulary.', 'Check the stop words and the lowercase step.'],
                        ['The model ignores the passage', 'A small model can ignore instructions.', 'Write it in your audit log, and trust the source chunk instead.']],
                  widths=[3.6, 4.1, 4.3], icons=['cross', 'cross', 'cross', 'cross', 'check'],
                  notes=('Five messages you may meet. More chunks than fifty nine means the splitter also cut after abbreviations, so split only after a full stop and a capital letter. A file not found error means the policy folder is not next to the notebook, so run the first cell again. '
                         'A precision of one at k equals three means you divided by the number of relevant chunks. Precision divides by k. Scores that are all zero mean the question had no word in the vocabulary. '
                         'And a small model that ignores the passage is a finding, so record it in your audit log. Read the message first. It usually tells you the answer.')))

    # 28 exit check
    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[['The top 3 results hold 1 right chunk, and 4 chunks in the library are right. What are precision at 3 and recall at 3?', 'Precision at 3 = 1/3 = 0.33. Recall at 3 = 1/4 = 0.25.'],
                        ['A model answers a policy question with a smooth sentence and no source. What is this called, and what do you do?', 'Hallucination. Retrieve the passage, ground the prompt in it, and check the answer against the source.'],
                        ['May you paste a file of customer phone numbers into a free chat tool?', 'No, unless your organisation has cleared the tool and a lawful purpose. It is personal data: mask or remove it first, and ask your data officer.']],
                  widths=[6.2, 5.8], icons=['chart', 'question', 'shield'],
                  notes=('Last, the exit check. Three questions. Write your answers before you look at mine. One, the top three results hold one right chunk, and four chunks in the library are right: what are precision at three and recall at three? '
                         'Two, a model answers a policy question with a smooth sentence and no source. What is that called, and what do you do? '
                         'Three, may you paste a file of customer phone numbers into a free chat tool? The short answers are on the slide. If you got all three, you are ready for Session 23, where we make your work reproducible and ship it.')))

    # ------------------------------------------------------------------ facilitator
    sess['facilitator'] = dict(
        prep=['Run the Session 22 notebook once in Colab before class. Steps 1 to 8 and 10 run with numpy and pandas only. Step 9 (a small open model) needs a download: check the Wi-Fi.',
              'The small open model in step 9 is HuggingFaceTB/SmolLM2-360M-Instruct. Its model card lists the Apache 2.0 licence and about 362 million parameters (checked through search results on 4 November 2026; glance at the card again before class). The step itself has not been run in Colab. Swap MODEL_NAME if the name has changed.',
              'No language model was run when this deck was written. Every score on the slides comes from TF-IDF retrieval written in numpy. Say so if a learner asks which assistant produced the examples.',
              'Make sure each learner has data.zip with the policies folder and feedback.csv. Write the check table (slide 26) on the board.',
              'Remind learners that all data is fictional, and that they must not paste real customer data into any tool.'],
        misconceptions=[('A language model looks facts up', 'It predicts the next token from the context. A fact is only reliable when the source is in the context and you check it.'),
                        ('RAG removes hallucination', 'It makes an answer checkable, because it quotes a source. A model can still ignore the passage or retrieval can pick the wrong chunk.'),
                        ('High precision at 1 means the search is finished', f'It is {pt[1][0]:.2f} on twelve questions. Read the two failures and test on more questions.'),
                        ('Recall at k is the same thing as precision at k', 'Precision divides by k. Recall divides by the number of relevant chunks.'),
                        ('If the code runs, an AI assistant got it right', 'Code can run and still be wrong. Test on an example whose answer you know, then record it.')],
        probes=[('What is a token?', 'A word, a piece of a word or punctuation that the model reads and writes.'),
                ('What happens in one trip round the generation loop?', 'Read the text so far, score every possible next token, pick one, add it.'),
                ('Why send three chunks and not the whole library?', 'The context window is limited, and extra text can distract the model.'),
                ('Why did how long do points last fail?', 'The word last matched last purchase. The policy says expire, a different word.'),
                ('What does a system prompt do?', 'It sets rules and a role for the whole conversation.'),
                ('What is in an audit log row?', 'What you asked, what it gave, how you checked it and your decision.'),
                ('Is a Colab notebook private?', 'It runs in your Google session. Check your organisation\'s rules before you upload personal data.')],
        lab_steps=[('Step 1: chunk', f'{F["n_chunks"]} chunks and {F["policy_words"]} words. A different count means a different splitter.'), ('Step 2: TF-IDF matrix', f'Vocabulary {F["V"]}.'),
                   ('Step 3: retrieve', f'The return question gives returns_policy.txt with score {rr[0][3]:.2f}.'), ('Step 4: evaluation set', 'Twelve questions. Each answer text sits in exactly one chunk.'),
                   ('Step 5: precision and recall at k', f'P@1 {pt[1][0]:.3f}, P@3 {pt[3][0]:.3f}, R@3 {pt[3][1]:.3f}, R@5 {pt[5][1]:.1f}.'), ('Step 6: failures', f'{F["n_fail"]} failures. The points question has its right chunk at rank {f1["rank"]}.'),
                   ('Step 7: change the method', f'Plain word overlap gives P@3 {po[3][0]:.3f}. The two methods are close: the gain from a better method here is small.'), ('Step 8: grounded prompt', f'{F["prompt_words"]} words for k = 3.'),
                   ('Step 9: small model (optional)', 'No number is checked. Ask: does the answer match the source chunk? This step was not run at authoring time.'), ('Step 10: keep', 'eval_results.csv has 12 rows and audit_log.csv has at least one row with five columns.')],
        rescue=['If the concepts run over, shorten the temperature slide (7) and the audit log slide (21). The lab covers both.', 'If only 30 minutes of lab remain, do steps 1 to 6 and 10, and set 7, 8 and 9 as homework.',
                'If the model download fails, skip step 9. The lab does not depend on it.', 'If a learner has no laptop, pair them with a neighbour: one types, one predicts aloud.'],
        after=['Share the notebook and this deck again for learners who were absent.', 'Ask each learner to save eval_results.csv and audit_log.csv and bring one document set from their own work to Session 23.', 'Note any question you could not answer and open the next session with it.'],
        lab_answer_key=[['Step 1 PREDICT: how many chunks will 8 files give?', f'{F["n_chunks"]}, about {F["mean_chunk_words"]:.0f} words each.'], ['Step 3 READ: why is the second chunk wrong for the return question?', 'It shares the words customer and return but not the days.'],
                        ['Step 5 PREDICT: will recall rise or fall as k grows?', 'It rises. Precision falls.'], ['Step 5 READ: why is P@5 at most 0.2?', 'Only one chunk per question is right, and 1/5 = 0.2.'],
                        ['Step 6 READ: why did the points question fail?', 'The word last matched last purchase. The policy says expire.'], ['Step 7 CHANGE: use word overlap.', f'P@3 {po[3][0]:.3f}, a little higher than TF-IDF ({pt[3][0]:.3f}). Overlap also ranks the right chunk third for the points question.'],
                        ['Step 8 CHANGE: set k = 1.', 'The prompt is shorter and has only the top chunk. Compare the words.'], ['Step 9 READ: does the model answer match the source chunk?', 'Not checked here. Record the answer and your check in the audit log.']])
    return sess
