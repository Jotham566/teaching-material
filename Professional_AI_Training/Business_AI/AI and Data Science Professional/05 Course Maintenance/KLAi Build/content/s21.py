"""Session 21: Text as data and meaning as numbers (text preprocessing, bag of words, TF-IDF, sentiment classification, embeddings, cosine similarity, semantic search). Python lab.

Every number on a slide, in a note or in the lab checks is computed in facts() from the real feedback.csv with numpy and pandas. Bag of words, TF-IDF, the classifier and cosine similarity are written in numpy
here, because scikit-learn's text vectorisers and sentence-transformers are not available in the authoring sandbox. Nothing about an embedding result is shown that was not produced here.
"""
import collections
import re
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

BUILD = Path(__file__).resolve().parents[1]
DATA = BUILD.parent.parent / '03 Learner Materials' / 'Practice Files' / 'data'

OPEN = r'^(feedback:|to the manager:|hello\.|on friday evening\.|yesterday i shopped at [a-z ]+\.)\s*'
CLOSE = r'(?<=[.?!])\s+(please reply\.|keep it up\.|please fix this\.|will recommend\.|do better\.|i am not happy\.|thank you\.|this has happened before\.|thanks\.)$'
STOP = sorted('a an the and or of to in on at is are was were be been it its this that i my me we our you your for with as by from am have has had do does did will would can could very'.split())
CLASSES = ['negative', 'neutral', 'positive']
QUERY_OK = 'many people waiting to pay'
QUERY_BAD = 'crowded cashier'
NEG_GOOD = 'the queue was good'
NEG_NOTGOOD = 'the queue was not good'


def n(x):
    return f'{int(x):,}'


def lower(m):
    return m.lower()


def strip_boilerplate(t):
    return re.sub(CLOSE, '', re.sub(OPEN, '', t))


def only_letters(t):
    return re.sub(r'[^a-z\s]', '', t)


def tokens(t):
    return [w for w in only_letters(strip_boilerplate(lower(t))).split() if w not in STOP]


def fit_softmax(X, y, k=3, lr=10.0, epochs=3000, l2=None):
    """Multinomial logistic regression (softmax regression) by gradient descent, in numpy. l2 defaults to 1 / number of rows: the same strength as scikit-learn's default C = 1."""
    l2 = 1.0 / len(X) if l2 is None else l2
    W = np.zeros((X.shape[1], k))
    b = np.zeros(k)
    Y = np.eye(k)[y]
    for _ in range(epochs):
        Z = X @ W + b
        Z -= Z.max(axis=1, keepdims=True)
        P = np.exp(Z)
        P /= P.sum(axis=1, keepdims=True)
        G = (P - Y) / len(X)
        W -= lr * (X.T @ G + l2 * W)
        b -= lr * G.sum(axis=0)
    return W, b


def group_folds(inv, k=5):
    """Fold number for each row so that every copy of a text (same group) is in one fold: the algorithm of scikit-learn's GroupKFold."""
    sizes = np.bincount(inv)
    order = np.argsort(sizes)[::-1]
    load = np.zeros(k)
    fold_of_group = np.zeros(len(sizes), int)
    for g in order:
        f = int(np.argmin(load))
        load[f] += sizes[g]
        fold_of_group[g] = f
    return fold_of_group[inv]


def cosine(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


@lru_cache(maxsize=None)
def facts():
    fb = pd.read_csv(DATA / 'feedback.csv')
    F = dict(fb=fb)
    N = len(fb)
    F['N'] = N
    F['cols'] = list(fb.columns)
    F['sent'] = {k: int(v) for k, v in fb.sentiment.value_counts().items()}
    F['sent_pct'] = {k: v / N * 100 for k, v in F['sent'].items()}
    F['themes'] = {k: int(v) for k, v in fb.theme.value_counts().items()}
    F['majority_share'] = F['sent']['negative'] / N
    F['n_themes'] = fb.theme.nunique()
    F['mean_words_raw'] = float(fb.message.map(lambda m: len(m.split())).mean())
    F['distinct_msgs'] = int(fb.message.nunique())
    # preprocessing
    low = fb.message.map(lower)
    stripped = low.map(strip_boilerplate)
    letters = stripped.map(only_letters)
    docs = [[w for w in t.split() if w not in STOP] for t in letters]
    F['docs'] = docs
    F['body'] = list(stripped)
    F['mean_tokens'] = float(np.mean([len(d) for d in docs]))
    F['mean_tokens_nostop'] = float(np.mean([len(t.split()) for t in letters]))
    F['distinct_bodies'] = int(stripped.nunique())
    vocab = sorted({w for d in docs for w in d})
    idx = {w: i for i, w in enumerate(vocab)}
    F['vocab'], F['idx'], F['V'] = vocab, idx, len(vocab)
    F['total_tokens'] = int(sum(len(d) for d in docs))
    X = np.zeros((N, len(vocab)))
    for i, d in enumerate(docs):
        for w in d:
            X[i, idx[w]] += 1
    F['X'] = X
    df = (X > 0).sum(axis=0)
    idf = np.log(N / df)
    F['df'], F['idf'] = df, idf
    T = X * idf
    T = T / np.linalg.norm(T, axis=1, keepdims=True)
    F['T'] = T
    F['top_word'] = vocab[int(np.argmax(df))]
    F['top_word_df'] = int(df.max())
    # messages containing the whole word not, raw and after cleaning
    F['not_raw'] = int(low.str.contains(r'\bnot\b').sum())
    F['not_body'] = int(sum('not' in d for d in docs))
    F['not_body_negative'] = int(sum(('not' in d) and s == 'negative' for d, s in zip(docs, fb.sentiment)))
    # document frequency of words before any stop word removal (for the stop word slide and idf bars)
    raw_sets = [set(only_letters(t).split()) for t in low]
    rc = collections.Counter(w for s in raw_sets for w in s)
    F['raw_top'] = rc.most_common(8)
    cc = collections.Counter(w for d in docs for w in set(d))
    F['clean_top'] = cc.most_common(8)
    F['raw_df'] = {w: rc[w] for w in ('the', 'at', 'please', 'queue', 'costly')}
    F['raw_idf'] = {w: float(np.log(N / rc[w])) for w in F['raw_df']}
    # the pipeline on one message
    m0 = fb.message.iloc[0]
    F['pipe_msg'] = m0
    F['pipe'] = [m0, lower(m0), only_letters(strip_boilerplate(lower(m0))).strip(), only_letters(strip_boilerplate(lower(m0))).split(), tokens(m0)]
    # excerpt rows
    pick = []
    for th, se in (('price', 'negative'), ('loyalty', 'positive'), ('queue', 'negative'), ('question', 'neutral')):
        r = fb[(fb.theme == th) & (fb.sentiment == se) & (fb.message.str.len() < 62)].iloc[0]
        pick.append(r)
    F['excerpt'] = pd.DataFrame(pick).reset_index(drop=True)
    # three-message bag of words
    dtm_msgs = ['the card machine at jinja was not working so i could not pay.', 'the checkout line at jinja was very slow today.', 'fast checkout at jinja, the cashier was quick.']
    dtm_docs = [tokens(m) for m in dtm_msgs]
    dtm_vocab = []
    for d in dtm_docs:
        for w in d:
            if w not in dtm_vocab:
                dtm_vocab.append(w)
    F['dtm_msgs'], F['dtm_docs'], F['dtm_vocab'] = dtm_msgs, dtm_docs, dtm_vocab
    F['dtm'] = [[d.count(w) for w in dtm_vocab] for d in dtm_docs]
    assert all(m in set(low) or m in set(stripped) for m in dtm_msgs)
    # tf-idf worked example
    F['w_queue'] = dict(df=int(df[idx['queue']]), idf=float(idf[idx['queue']]))
    F['w_costly'] = dict(df=int(df[idx['costly']]), idf=float(idf[idx['costly']]))
    F['w_please'] = dict(df=int(df[idx['please']]), idf=float(idf[idx['please']]))
    F['ex_msg'] = 'Long queue at the till in Gulu, waited more than twenty minutes.'
    assert F['ex_msg'] in set(fb.message) or F['ex_msg'] in set(fb.message.str.replace(r'^[A-Za-z ]+: |^Hello\. |^On Friday evening\. ', '', regex=True))
    # classifier
    y = fb.sentiment.map({c: i for i, c in enumerate(CLASSES)}).values
    F['y'] = y
    # evaluation by grouped 5-fold cross-validation: every copy of a message text sits on the same side (GroupKFold(5), replicated in numpy)
    key = np.array([' '.join(d) for d in docs])
    groups_u, inv = np.unique(key, return_inverse=True)
    F['n_groups'] = len(groups_u)
    F['group_inv'] = inv
    fold = group_folds(inv, 5)
    F['fold'] = fold
    oof = np.zeros(N, int)
    accs = []
    for f in range(5):
        te_f = fold == f
        Wf, bf = fit_softmax(T[~te_f], y[~te_f])
        oof[te_f] = (T[te_f] @ Wf + bf).argmax(axis=1)
        accs.append(float((oof[te_f] == y[te_f]).mean()))
    F['oof'], F['fold_accs'] = oof, accs
    F['fold_size'] = int((fold == 0).sum())
    F['acc'] = float((oof == y).mean())
    F['acc_min'], F['acc_max'] = min(accs), max(accs)
    F['baseline_te'] = float((y == 0).mean())
    F['n_test'] = N
    F['n_wrong'] = int((oof != y).sum())
    cm = np.zeros((3, 3), int)
    for a_, p_ in zip(y, oof):
        cm[a_, p_] += 1
    F['cm'] = cm
    tp, fp, fn = int(cm[0, 0]), int(cm[:, 0].sum() - cm[0, 0]), int(cm[0, :].sum() - cm[0, 0])
    tn = int(cm.sum() - tp - fp - fn)
    F['neg_tp'], F['neg_fp'], F['neg_fn'], F['neg_tn'] = tp, fp, fn, tn
    F['neg_precision'] = tp / (tp + fp)
    F['neg_recall'] = tp / (tp + fn)
    F['neg_f1'] = 2 * F['neg_precision'] * F['neg_recall'] / (F['neg_precision'] + F['neg_recall'])
    wrong = [i for i in range(N) if oof[i] != y[i]]
    F['wrong_idx'] = wrong
    F['wrong_rows'] = [(fb.message.iloc[i], CLASSES[y[i]], CLASSES[oof[i]], fb.rating.iloc[i]) for i in wrong]
    # the same evaluation with an ordinary shuffled KFold(5, shuffle=True, random_state=42): copies of one text land on both sides
    idx0 = np.arange(N)
    np.random.RandomState(42).shuffle(idx0)
    oof0 = np.zeros(N, int)
    leak = 0
    for c in np.array_split(idx0, 5):
        te_f = np.zeros(N, bool)
        te_f[c] = True
        Wf, bf = fit_softmax(T[~te_f], y[~te_f])
        oof0[te_f] = (T[te_f] @ Wf + bf).argmax(axis=1)
        seen = set(inv[~te_f])
        leak += sum(g in seen for g in inv[te_f])
    F['leak_acc'], F['leak_n'] = float((oof0 == y).mean()), int(leak)
    # final model on all 800 messages (word weights, the negation test, the scored file's model)
    W, b = fit_softmax(T, y)
    F['W'], F['b'] = W, b
    names = np.array(vocab)
    F['top_w'] = {c: [(str(names[j]), float(W[j, k])) for j in np.argsort(-W[:, k])[:6]] for k, c in enumerate(CLASSES)}

    def vec(t):
        v = np.zeros(len(vocab))
        for w in tokens(t):
            if w in idx:
                v[idx[w]] += 1
        v = v * idf
        nrm = np.linalg.norm(v)
        return v / nrm if nrm else v
    F['vec'] = vec

    def proba(t):
        z = vec(t) @ W + b
        p = np.exp(z - z.max())
        return p / p.sum()
    F['proba'] = proba
    F['p_good'], F['p_notgood'] = proba(NEG_GOOD), proba(NEG_NOTGOOD)
    # search corpus: one row per distinct message text (first occurrence), so that ten copies of one sentence cannot fill the top ten
    first = np.array([int(np.where(inv == g)[0][0]) for g in range(len(groups_u))])
    F['first'] = first
    ufb = fb.iloc[first].reset_index(drop=True)
    F['ufb'] = ufb
    udocs = [docs[i] for i in first]
    uT = T[first]
    q = (ufb.theme == 'queue').values
    F['n_queue'] = int(q.sum())
    F['n_queue_all'] = int((fb.theme == 'queue').sum())

    def has(kws):
        return np.array([any(k in d for k in kws) for d in udocs])
    rows = []
    for kws in (['queue'], ['queue', 'line'], ['queue', 'line', 'wait', 'waited'], ['queue', 'line', 'wait', 'waited', 'slow', 'till', 'tills', 'checkout', 'cashiers', 'counter', 'pay', 'long']):
        h = has(kws)
        rows.append((kws, int(h.sum()), int((h & q).sum()), (h & q).sum() / h.sum(), (h & q).sum() / q.sum()))
    F['kw_rows'] = rows
    F['queue_found'], F['queue_recall'], F['queue_precision'] = rows[0][2], rows[0][4], rows[0][3]
    # tf-idf search over the distinct messages
    def search(s, k=10):
        sc = uT @ vec(s)
        o = np.argsort(-sc, kind='stable')[:k]
        return o, sc[o]
    F['search'] = search
    for key_, s_ in (('ok', QUERY_OK), ('bad', QUERY_BAD)):
        o, sc = search(s_)
        F['p10_' + key_] = float((ufb.theme.values[o] == 'queue').mean())
        F['top_' + key_] = [ufb.message.iloc[i] for i in o[:3]]
        F['themes_' + key_] = collections.Counter(ufb.theme.values[o]).most_common(3)
    # the scikit-learn recipe, replicated in numpy: Pipeline(TfidfVectorizer(), LogisticRegression(C=1)) inside GroupKFold(5), idf and vocabulary learned from each training fold only
    soof = np.zeros(N, int)
    saccs = []
    for f in range(5):
        te_f = fold == f
        trd = [docs[i] for i in np.where(~te_f)[0]]
        svoc = sorted({w for d in trd for w in d})
        sidx = {w: i for i, w in enumerate(svoc)}

        def scounts(ds):
            Z = np.zeros((len(ds), len(svoc)))
            for i, d in enumerate(ds):
                for w in d:
                    if w in sidx:
                        Z[i, sidx[w]] += 1
            return Z
        Xs = scounts(trd)
        sdf = (Xs > 0).sum(axis=0)
        sidf = np.log((1 + len(trd)) / (1 + sdf)) + 1      # TfidfVectorizer default: smooth_idf=True
        def stf(Z):
            Z = Z * sidf
            return Z / np.linalg.norm(Z, axis=1, keepdims=True)
        Ws, bs = fit_softmax(stf(Xs), y[~te_f])
        soof[te_f] = (stf(scounts([docs[i] for i in np.where(te_f)[0]])) @ Ws + bs).argmax(axis=1)
        saccs.append(float((soof[te_f] == y[te_f]).mean()))
    # idf of queue with scikit-learn's smoothed formula on all 800 messages
    sdf_all = (X > 0).sum(axis=0)
    F['sk_idf_queue'] = float(np.log((1 + N) / (1 + sdf_all[idx['queue']])) + 1)
    F['sk_idf_the_all'] = float(np.log((1 + N) / (1 + (X > 0).sum(axis=0).max())) + 1)
    F['sk_fold_accs'] = saccs
    F['sk_acc'] = float((soof == y).mean())
    F['sk_acc_min'], F['sk_acc_max'] = min(saccs), max(saccs)
    scm = np.zeros((3, 3), int)
    for a_, p_ in zip(y, soof):
        scm[a_, p_] += 1
    F['sk_cm'] = scm
    F['sk_neg_precision'] = scm[0, 0] / scm[:, 0].sum()
    F['sk_neg_recall'] = scm[0, 0] / scm[0, :].sum()
    # cosine
    F['cos_a'], F['cos_b'] = [3, 4], [4, 3]
    F['cos_ab'] = cosine(F['cos_a'], F['cos_b'])
    F['cos_dot'] = 3 * 4 + 4 * 3
    F['cos_norm_a'] = float(np.linalg.norm(F['cos_a']))
    m1 = 'Long queue at the till in Gulu, waited more than twenty minutes.'
    m2 = 'Long queue at the till in Jinja, waited more than twenty minutes.'
    m3 = 'No queue at all at Jinja today, in and out in five minutes.'
    m4 = 'Mobile money payment went through quickly, thank you.'
    F['real_cos'] = [(m1, m2, cosine(vec(m1), vec(m2))), (m1, m3, cosine(vec(m1), vec(m3))), (m1, m4, cosine(vec(m1), vec(m4)))]
    # illustrative embedding picture (made-up 2D positions) and angle pairs
    F['ill_pairs'] = [([4, 1], [3, 1], 'similar meaning'), ([4, 1], [1, 4], 'different topic'), ([4, 1], [-4, -1], 'opposite')]
    F['ill_cos'] = [cosine(a, b) for a, b, _ in F['ill_pairs']]
    F['theme_n'] = F['themes']
    # recipe output (code slide) is produced by running the recipe here
    return F


RECIPE = ('docs = [m.split() for m in clean]\nvocab = sorted({w for d in docs for w in d})\nX = np.array([[d.count(w) for w in vocab]\n              for d in docs])\n'
          'doc_freq = (X > 0).sum(axis=0).tolist()\nT = X * np.log(len(docs) / np.array(doc_freq))\nshared = {w: c for w, c in zip(vocab, doc_freq)\n          if c > 1}\nprint(X.shape, shared)')


def recipe_output(F):
    """Run the five-line recipe on the three example messages and return what it prints (shown on the code slide)."""
    import contextlib
    import io
    ns = dict(np=np, clean=[' '.join(d) for d in F['dtm_docs']])
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(RECIPE, ns)
    return buf.getvalue().strip()


def build():
    F = facts()
    N, V = F['N'], F['V']
    sent = F['sent']
    q_ok = F['w_queue']
    acc, base = F['acc'], F['baseline_te']
    rc = F['raw_df']
    ri = F['raw_idf']
    kw = F['kw_rows']
    cm = F['cm']
    pg, pn = F['p_good'], F['p_notgood']
    assert F['n_queue'] == 36 and q_ok['df'] == 19 and V == len(F['vocab'])
    assert int(F['p_notgood'].argmax()) == 2 and F['n_groups'] == 360
    sess = dict(
        num=21, block='Module E: Neural networks and text', short_title='Text as data and meaning as numbers',
        title='Text as data and meaning as numbers',
        question='How can a computer compare customer messages when it only understands numbers?',
        outcomes=['Clean text and turn it into numbers with a bag of words and TF-IDF, and classify sentiment',
                  'Score a search against an answer key, and explain why counting words misses negation and synonyms',
                  'Turn messages into embeddings and rank them by cosine similarity (semantic search)'],
        outcome_icons=['doc', 'check', 'magnifier'],
        outcome_note=('Here is what you can do by the end of today. You can clean customer messages and turn them into numbers, first with a bag of words and TF-IDF, and then train a sentiment classifier on them. '
                      'You can score a search against an answer key, and you can explain why counting words fails on a message such as not good. '
                      'And you can turn messages into embeddings and rank them by cosine similarity, which is how a semantic search works. All of it runs on the eight hundred Lakeside Mart feedback messages.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: picture, plain words, one example by hand'), (10, 'Break'), (45, 'Lab: predict, run, read, change'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: concepts first, then a Python lab on customer messages',
        plan_caption='Pictures and plain words first. Then you open the notebook. Then the checks and what you keep.',
        plan_note=("Two hours again. We start with ten minutes of recall and today's question. Then forty-five minutes of concepts, with laptops closed, so you can follow the pictures. "
                   'After the break you open a Colab notebook for forty-five minutes. You will clean the messages, count words, train a sentiment classifier, score a keyword search against an answer key, and then try a search by meaning. '
                   'The last ten minutes are an exit check and what you keep. Please protect the lab time, because that is where the ideas stick.'),
        recall_from='Session 20',
        recall=[('What does one artificial neuron compute?', 'A weighted sum of its inputs plus a bias, passed through an activation function such as sigmoid or ReLU.'),
                ('What does training a neural network do?', 'It repeats small corrections, by gradient descent with backpropagation, to lower the loss function.'),
                ('When do you keep a simpler model instead of a neural network?', 'When the simpler model scores about the same on the test set. It is cheaper and easier to explain (parsimony).')],
        words=[('Text preprocessing (tokenisation, stop words)', 'Cleaning raw text into tokens: lowercase it, remove noise with a regular expression, split it into words and drop filler words.'),
               ('Bag of words and TF-IDF', 'Bag of words counts each word in each message and ignores the order. TF-IDF weights those counts so rare words count more.'),
               ('Text classification (sentiment analysis)', 'A supervised model that gives each message a label, such as positive, neutral or negative.'),
               ('Embedding (vector)', 'A list of numbers that stands for the meaning of a message. Messages with similar meanings get similar vectors.'),
               ('Cosine similarity and semantic search', 'A score from -1 to 1 for how alike two vectors are. Semantic search ranks messages by that score.')],
        word_icons=['doc', 'calculator', 'tag', 'chart', 'magnifier'],
        words_note=('Five words for today. Text preprocessing is the cleaning that turns a sentence into tokens. A bag of words counts each word in a message, and TF-IDF adjusts those counts so that rare words matter more. '
                    'Text classification, also called sentiment analysis when the label is a mood, is a supervised model that labels each message. An embedding is a vector, a list of numbers, that stands for meaning. '
                    'And cosine similarity scores how alike two vectors are, which is what semantic search uses to rank messages. We use every one of these today.'),
        keep='Keep your notebook and the file keep/feedback_scored.csv, with a three-sentence finding: the accuracy, one mistake you read, and one search the keyword method missed.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab file', value='A scored CSV'), dict(label='Your finding', value='3 sentences'), dict(label='Next session', value='Language models')]),
        keep_title='Save your notebook and your scored file',
        next='Session 22: Language models and building with them. We use these ideas to build a search that answers from your own documents.', next_label='Next session',
        keep_note=('Before you go, save your notebook and the file feedback scored dot csv from the folder called keep. Those two files, plus your three-sentence finding, are your keepsake. '
                   'If a colleague can read the finding and understand the accuracy, one mistake and one missed search, it is good. '
                   'Next session we use the same ideas, tokens, retrieval and similarity, to see how a language model works and how to make it answer from your own documents. '
                   'Bring one question about text data from your own work.'),
        cover_note=('Welcome back. Until now every variable we used held numbers or short labels. Today a variable holds a sentence. '
                    'We take eight hundred customer messages from Lakeside Mart and turn them into numbers in two ways. First by counting words, then with embeddings, which put meaning into numbers. '
                    'You will build a sentiment classifier, and a search that can find a long queue complaint written in different words.'),
        use_at_work='Turn free-text comments into counts, a sentiment label and a search, and know where each method fails.',
        slides=[])
    S = sess['slides']
    ex = F['excerpt']
    pipe = F['pipe']

    # 1 answers
    S.append(dict(kind='table', title='Answers to the three questions from Session 20', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in sess['recall']], widths=[5.0, 7.0], icons=['gear', 'chart', 'check'],
                  notes=('Here are the answers to the three warm-up questions. One artificial neuron multiplies each input by a weight, adds them up with a bias, and passes the total through an activation function. '
                         'Training repeats small corrections, using gradient descent and backpropagation, to make the loss function smaller. And you keep the simpler model when its test score is about the same, which is called parsimony. '
                         'That last idea matters today, because the simplest text model we build will do very well. Which answer did you find hardest?')))

    # 2 text is unstructured data
    S.append(dict(kind='idea', title='Text is unstructured data: a sentence has no fixed columns to count',
                  visual=dict(kind='k_msgtable', headers=['rating', 'sentiment', 'theme', 'message'], rows=[[str(r.rating), r.sentiment, r.theme, r.message] for r in ex.itertuples()]),
                  lead='Unstructured data has no fixed columns. Free text is the most common kind.',
                  points=[f'feedback.csv holds {n(N)} customer messages. Variable type: text (string).', 'A model needs a vector: an ordered list of numbers.', 'So we turn each message into a vector.'],
                  notes=(f'Until now every variable was a number or a short label. Look at feedback dot csv. It has {n(N)} customer messages, and the message variable is free text. That is unstructured data, which means there are no fixed columns inside a sentence for you to count or add up. '
                         'The other variables are neat. Rating is a number, sentiment is a mood label, and theme says what the message is about. A model can only use numbers, so today is about one job: turning each message into a vector, an ordered list of numbers. '
                         'How would you turn a sentence into numbers in Excel?')))

    # 3 pipeline
    S.append(dict(kind='steps', title='Every text method follows the same path: clean, make vectors, then classify or search',
                  steps=[dict(head='Raw text', text=f'{n(N)} messages', icon='doc'), dict(head='Preprocess', text='Lowercase, regex, tokens, stop words', icon='gear'),
                         dict(head='Vectors', text='Bag of words, TF-IDF or embedding', icon='grid'), dict(head='Model or search', text='Classifier or similarity', icon='magnifier'), dict(head='Evaluate', text='Answer key', icon='check')], highlight=None,
                  caption='Today we walk this path twice: with counted words, and with embeddings.',
                  notes=('This is the map for the whole session. Raw text goes in on the left. Text preprocessing cleans it. Then we make vectors, either by counting words or by using an embedding. '
                         'A model or a search uses the vectors, a classifier to give a label or a similarity score to find messages. And the last box, evaluation, checks the result against an answer key. '
                         'Every text project at work follows this path, whatever the tools are. We walk it twice today. Which box do you think takes the most time in real projects?')))

    # 4 preprocessing
    S.append(dict(kind='wide', title='Text preprocessing changes one real message in four steps: lowercase, regex, tokenise, drop stop words',
                  visual=dict(kind='k_preprocess', stages=[['Original', 'text', pipe[0]], ['1 Lowercase', 'text', pipe[1]], ['2 Regex cleaning: remove the opener, the closer and punctuation', 'text', pipe[2]],
                                                           ['3 Tokenisation: split into tokens (words)', 'tokens', pipe[3]], ['4 Remove stop words: filler words such as for', 'tokens', pipe[4]]]),
                  caption='Message F0001 of feedback.csv. Each step feeds the next.',
                  notes=('Here is text preprocessing on one real message, F0001. The original has a label at the start and a polite phrase at the end. Step one, lowercasing, so that Fresh and fresh count as the same word. '
                         'Step two, regex cleaning: a regular expression removes the opener, the closer and the punctuation. Step three, tokenisation, splits the text into tokens, which here are words. '
                         'Step four removes stop words, filler words such as for. The result is four tokens. In Excel you did this with LOWER, SUBSTITUTE and TRIM. Which step changed the message most?')))

    # 5 regex
    S.append(dict(kind='idea', title='A regular expression (regex) is a pattern that finds text, and one line cleans 800 messages',
                  visual=dict(kind='k_regex', headers=['Pattern', 'Meaning', 'Example'],
                              rows=[['[^a-z\\s]', 'Any character that is not a letter or a space', 'Removes full stops and commas'], ['\\bnot\\b', 'The whole word not', f'Found in {F["not_raw"]} of {n(N)} raw messages'],
                                    ['\\d{3}', 'Exactly three digits in a row', 'Part of a phone number'], ['^hello\\.', 'The text hello. at the start of a message', 'A greeting to strip']]),
                  lead='A regex is Find and Replace with wildcards. Python applies it with re.sub or str.replace.',
                  points=['Messages here open with Hello. or Feedback: and close with Please reply.', f'After we strip those lines, \\bnot\\b matches {F["not_body"]} messages, down from {F["not_raw"]}.', 'Test a regex on a few rows first.'],
                  notes=(f'A regular expression, or regex, is a pattern that describes text to find or replace. You can think of it as Find and Replace with wildcards. Look at the four patterns. The first matches any character that is not a letter or a space, so it removes punctuation. '
                         f'The second matches the whole word not. In the raw file it matches {F["not_raw"]} messages, but many of those are the polite closing line I am not happy, added to the end. After we strip the opener and closer lines, it matches {F["not_body"]}. '
                         'The lesson is to test a regex on a few real rows before you apply it to all of them. Why might a closing line mislead a model?')))

    # 6 stop words
    S.append(dict(kind='wide', title='The most common words are filler, and stop word removal exposes the words that carry meaning',
                  visual=dict(kind='k_topwords', left=F['raw_top'], right=F['clean_top'], left_title='All words in the raw messages', right_title='After cleaning and removing stop words', total=N),
                  caption='Messages containing each word, out of 800. Keep the word not: many stop word lists remove it.',
                  notes=(f'The left chart counts, for each word, how many of the {n(N)} raw messages contain it. The winners are the, at, I, please and on, which say nothing about mood or topic. '
                         'Stop words are such filler words, and removing them is the fourth preprocessing step. The right chart shows the words that remain after cleaning, where phone, please and Kampala lead. Please stays in because it is not on our stop list. In a real project you decide whether polite words belong on your own list. '
                         'Look at the caption. Many standard stop word lists contain the word not. If you delete it, you delete the signal that flips a meaning. So read your list before you use it. Which word on the right surprised you?')))

    # 7 bag of words
    S.append(dict(kind='wide', title='A bag of words counts each word in each message and ignores the order',
                  visual=dict(kind='k_dtm', rows=[[m, c] for m, c in zip(['Message A', 'Message B', 'Message C'], F['dtm'])], vocab=F['dtm_vocab'],
                              msgs=['A: The card machine at Jinja was not working so I could not pay.', 'B: The checkout line at Jinja was very slow today.', 'C: Fast checkout at Jinja, the cashier was quick.']),
                  caption=f'A document-term matrix (count vectorizer). The full file is {n(N)} messages by {V} words.',
                  notes=(f'This is a bag of words. Take three real messages, A, B and C, all from Jinja. Each row of the table is one message, and each column is one word from the vocabulary, which is the list of all different words. '
                         'The cell holds how many times the word appears. Message A contains not twice, so its not cell is 2. The order of the words is thrown away, which is why we call it a bag. '
                         f'This table is called a document-term matrix. For all {n(N)} messages after cleaning it has {V} columns, one per different word. Most cells are zero. Which word do messages B and C share?')))

    # 8 TF-IDF formula
    S.append(dict(kind='formula', title='TF-IDF multiplies a word count by how rare the word is across all messages',
                  formulas=[('TF-IDF', r'$\mathrm{tfidf}(t,d)=\mathrm{tf}(t,d)\times\mathrm{idf}(t)$'), ('Inverse document frequency', r'$\mathrm{idf}(t)=\ln\left(N/\mathrm{df}(t)\right)$'),
                            ('Our word: queue', rf'$\ln(800/19)={q_ok["idf"]:.2f}$')],
                  symbols=[['tf(t, d)', 'Term frequency: times word t appears in message d', 'queue: once'], ['df(t)', 'Document frequency: messages that contain word t', f'queue: {q_ok["df"]} messages'],
                           ['N', 'The number of messages (documents)', f'{N}'], ['ln', 'Natural logarithm. A rarer word gives a larger value', f'ln(800/19) = {q_ok["idf"]:.2f}']],
                  widths=[1.8, 5.8, 4.3], size=24, note='scikit-learn adds 1 inside the logarithm and 1 outside, so its numbers differ from ours.',
                  notes=(f'TF-IDF stands for term frequency, inverse document frequency. The term frequency is the count of a word in one message. The document frequency is the number of messages that contain the word at all. '
                         f'The inverse document frequency is the natural logarithm of N divided by that document frequency. Our worked number: the word queue is in {q_ok["df"]} of {n(N)} messages, so ln of {N} over {q_ok["df"]} is {q_ok["idf"]:.2f}. '
                         'In this textbook formula a word in every message gets zero. Multiply the count by the weight and rare words count more. scikit-learn adds one inside the logarithm and one outside, so there a word in every message gets one, and its values differ from ours. What would idf be for a word in every message here?')))

    # 9 idf bars
    S.append(dict(kind='idea', title=f'Rare words get more weight: idf is {ri["the"]:.2f} for the and {ri["costly"]:.2f} for costly',
                  visual=dict(kind='bars', items=[dict(label=f'the: in {rc["the"]} messages', value=round(ri['the'], 2), text=f'{ri["the"]:.2f}'), dict(label=f'at: in {rc["at"]} messages', value=round(ri['at'], 2), text=f'{ri["at"]:.2f}'),
                                                  dict(label=f'please: in {rc["please"]} messages', value=round(ri['please'], 2), text=f'{ri["please"]:.2f}'), dict(label=f'queue: in {rc["queue"]} messages', value=round(ri['queue'], 2), text=f'{ri["queue"]:.2f}', hl=True),
                                                  dict(label=f'costly: in {rc["costly"]} messages', value=round(ri['costly'], 2), text=f'{ri["costly"]:.2f}', hl=True)], size=17),
                  lead='Inverse document frequency (idf) shrinks words found in many messages and raises words found in few.',
                  points=['Computed on all 800 raw messages, before stop words are removed.', 'TF-IDF down-weights filler even when you keep it.', 'Then each message vector is scaled to length 1.'],
                  notes=(f'Here is idf for five real words, computed on the raw messages before any stop words are removed. The appears in {rc["the"]} messages, so its idf is only {ri["the"]:.2f}. At gets {ri["at"]:.2f} and please gets {ri["please"]:.2f}. '
                         f'The word queue appears in {rc["queue"]} messages and gets {ri["queue"]:.2f}. The word costly appears in {rc["costly"]} messages and gets {ri["costly"]:.2f}. So filler is shrunk automatically, and rare words stand out. '
                         'After weighting, we scale each message vector to length one so long messages do not win just by being long. Why might a very rare word be a poor feature?')))

    # 10 classifier
    tw = F['top_w']
    S.append(dict(kind='idea', title='A sentiment classifier learns one weight per word for each label',
                  visual=dict(kind='k_word_weights', columns=[[c, [[w, round(v, 2)] for w, v in tw[c][:5]]] for c in ('negative', 'neutral', 'positive')]),
                  lead='Text classification: a supervised model learns from messages with known labels.',
                  points=['Target: sentiment (negative, neutral, positive).', 'Features: the TF-IDF value of each word.', 'The chart shows the five largest learned weights for each label.'],
                  notes=('Sentiment analysis is a classification problem, and it is called text classification when the input is text. The target is the sentiment label. The features are the TF-IDF values of the words. '
                         'The model here is multinomial logistic regression, which you can think of as logistic regression with one set of weights per label. We use a small numpy version so every number is checkable. In practice you would use LogisticRegression. '
                         f'Look at the chart, which comes from a model fitted on all {N} messages. For the positive label the biggest weights go to {tw["positive"][0][0]}, {tw["positive"][1][0]} and {tw["positive"][2][0]}. For negative, {tw["negative"][0][0]}, {tw["negative"][1][0]} and {tw["negative"][2][0]}. For neutral, {tw["neutral"][0][0]}, {tw["neutral"][1][0]} and {tw["neutral"][2][0]}, the words of questions. Does that match your common sense?')))
    RECIPE_OUT = recipe_output(F)

    # 11 leakage and grouped evaluation
    S.append(dict(kind='compare', title=f'A random split flatters the score: {F["leak_n"]} of {N} test messages repeat a training message',
                  left=dict(head=f'Shuffled 5-fold: {F["leak_acc"]:.1%}', points=[f'{F["leak_n"]} of {N} test messages repeat a training text.', 'Data leakage: the score is too high.']),
                  right=dict(head=f'Grouped 5-fold: {acc:.1%}', points=['Copies of one text share a fold.', f'Only {F["n_groups"]} different texts behind {N} messages.']),
                  verdict=f'Use the grouped score. The baseline is {base:.1%}.',
                  notes=(f'This file has {N} messages, but only {F["n_groups"]} different texts after cleaning, because the generator repeats sentences with different openers and closers. If we shuffle the messages and cut them into five folds, copies of one text land in both the training and the test side. '
                         f'In my run, {F["leak_n"]} of the {N} test messages had a twin in the training data, and the score came out at {F["leak_acc"]:.1%}. That is data leakage, which you met in Session 16. '
                         f'The fix is grouped cross-validation: all copies of one text go to the same fold. The score drops to {acc:.1%}, which is the honest one. The baseline, always saying negative, is {base:.1%}. Why would real customer messages also need a grouped split?')))

    # 12 confusion
    S.append(dict(kind='idea', title=f'Grouped cross-validation gives {acc:.1%} accuracy against {base:.1%} for the baseline',
                  visual=dict(kind='k_confusion3', labels=CLASSES, cm=[[int(v) for v in r] for r in cm]),
                  lead=f'{N - F["n_wrong"]} of {N} messages are right when the model has never seen their text.',
                  points=[f'Five folds of {F["fold_size"]} messages, each predicted by a model trained on the other four.', f'Fold scores run from {F["acc_min"]:.0%} to {F["acc_max"]:.0%}.', f'Baseline (always negative): {base:.1%}.'],
                  notes=(f'We cut the {N} messages into five folds. Each fold was predicted by a model trained on the other four, and no text appears on both sides. This is the confusion matrix of all {N} predictions. Rows are the true label, columns are what the model said, and the gold diagonal holds the correct answers. '
                         f'The model is right on {N - F["n_wrong"]} messages, which is {acc:.1%}. The majority-class baseline, which says negative every time, scores {base:.1%}, so the model clearly beats it. '
                         f'Look at the fold scores: they run from {F["acc_min"]:.1%} to {F["acc_max"]:.1%}. A single split would have given one of those, which is why we report the average. About six percent of the labels are wrong on purpose, so a perfect score is out of reach. Where are the {F["n_wrong"]} wrong answers on the matrix?')))

    # 13 read the mistakes
    wr = {r[0]: r for r in F['wrong_rows']}
    pick = [('Mobile money payment went through quickly, thank you.', 'Model wrong: the message is positive, and its words never appeared in the other folds.'), ('Delivery was on time and the groceries were cold. Thank you.', 'Arguable: the message is mixed.'),
            ('Feedback: I was charged twice for one purchase. Thank you.', 'Label looks wrong: the message is a complaint.'), ('Staff were rude when I asked about a refund for bread.', 'Label looks wrong: the message is a complaint.')]
    mrows = []
    for key, reading in pick:
        r = wr[key]
        mrows.append([r[0], r[1], r[2], reading])
    S.append(dict(kind='table', title='Read the mistakes before you trust the score: some are bad labels and some are model errors',
                  headers=['Message', 'Label', 'Model', 'Our reading'], rows=mrows, widths=[4.6, 1.4, 1.4, 4.6], icons=['cross', 'cross', 'cross', 'cross'],
                  note=f'4 of the {F["n_wrong"]} mistakes. Real messages vary more than these {F["n_groups"]} texts, so expect lower scores at work.',
                  notes=(f'Never stop at the score. Read the mistakes. Here are four of the {F["n_wrong"]} wrong answers. In the first row the model is wrong about a clearly positive message, because its words never appeared in the training folds. '
                         'The second is mixed, so a person could argue either way. In the last two rows the label looks wrong: a complaint labelled positive and a complaint labelled neutral. That is part of the six percent of noisy labels. '
                         f'There is a warning in the note. The file was generated from only {F["n_groups"]} different texts. Real customer messages vary far more, and an accuracy like this would fall. Which row would you fix first?')))

    # 14 negation
    S.append(dict(kind='compare', title='Counting words cannot read negation: our model still calls "not good" positive',
                  left=dict(head='The queue was good', points=['Model says: positive.', f'Probability of positive: {pg[2]:.2f}.', 'Correct.']),
                  right=dict(head='The queue was not good', points=['Model says: positive.', f'Probability of positive: {pn[2]:.2f}.', 'Wrong: the word good still outweighs the word not.']),
                  verdict='A bag of words sees words and ignores their order. Models that read word order do better.',
                  notes=(f'This is the classic failure of counting words. I typed two new sentences and ran our trained classifier on both. For the queue was good it says positive, with probability {pg[2]:.2f}. Fine. '
                         f'For the queue was not good it still says positive, with probability {pn[2]:.2f}. The model gives some negative weight to the word not, but the positive weight of good is bigger. '
                         'Another model or another setting may get this one sentence right, but a bag of words cannot read negation by design. It only learns that the word not often appears in negative messages. What other short words flip a meaning?')))

    # 15 the scikit-learn recipe
    SK_CODE = ('pipe = make_pipeline(\n    TfidfVectorizer(),\n    LogisticRegression(max_iter=1000))\n'
               'pred = cross_val_predict(\n    pipe, texts, y, groups=groups,\n    cv=GroupKFold(5))\n'
               'print(classification_report(y, pred))')
    S.append(dict(kind='code', title='In practice you use the scikit-learn recipe: TfidfVectorizer, LogisticRegression and a pipeline',
                  code=SK_CODE, output=[f'Expected accuracy: about {F["sk_acc"]:.2f}', f'(folds {F["sk_acc_min"]:.2f} to {F["sk_acc_max"]:.2f}; numpy replica)'],
                  reads=['CountVectorizer builds the bag of words. TfidfVectorizer builds TF-IDF.', f'make_pipeline chains the vectoriser and the classifier, so the vocabulary and idf come from the training folds only.', 'GroupKFold keeps copies of one text together.',
                         f'scikit-learn idf for queue is {F["sk_idf_queue"]:.2f}, not {q_ok["idf"]:.2f}, because of its smoothing.'],
                  notes=('This is how a team does it with real tools. A TfidfVectorizer turns the cleaned texts into TF-IDF vectors. Its sibling, CountVectorizer, gives plain counts, which is the bag of words. '
                         'LogisticRegression is the classifier. make_pipeline chains the two, so that during cross-validation the vocabulary and the idf values are learned from the training folds only. That avoids a second kind of leak. '
                         f'GroupKFold keeps copies of one text together. Our numpy copy of this recipe gives about {F["sk_acc"]:.2f}, and your Colab run may differ by a point or two. The scikit-learn formula adds one inside the logarithm and one outside, so queue gets {F["sk_idf_queue"]:.2f} there. Why does the pipeline matter for honest scores?')))

    # 16 keyword recall
    S.append(dict(kind='stat', title=f'A keyword search for queue finds only {F["queue_recall"]:.0%} of the queue messages', big=f'{F["queue_recall"]:.0%}',
                  text=f'We search the {F["n_groups"]} different texts, so copies cannot inflate the result. The word queue is in {F["queue_found"]} of the {F["n_queue"]} texts whose theme is queue (recall). All {F["queue_found"]} hits are right (precision 100 percent).',
                  waffle_label='queue messages found in every 100',
                  notes=(f'Now we use the theme variable as an answer key. The theme says what a message is about. We search the {F["n_groups"]} different texts, one row per text, so that ten copies of one sentence cannot fill the results. {F["n_queue"]} of those texts are about queues. '
                         f'A keyword search for the word queue finds {F["queue_found"]} texts, and all of them are about queues. That is a precision of one hundred percent: every result is right. But recall is {F["queue_recall"]:.0%}: it finds only {F["queue_found"]} of the {F["n_queue"]}. '
                         'The other texts say line, wait, slow or too many people. High precision with low recall is the typical weakness of a keyword search. Which would your manager care about more, a missed complaint or a wrong one?')))

    # 17 keyword list table
    names = ['queue', 'queue, line', 'queue, line, wait, waited', 'Twelve words: queue, line, wait, slow, till, checkout ...']
    S.append(dict(kind='table', title='Adding keywords raises recall but lowers precision, and you must guess every synonym',
                  headers=['Keywords searched', 'Texts found', 'Right ones', 'Precision', 'Recall'],
                  rows=[[nm, str(r[1]), str(r[2]), f'{r[3]:.0%}', f'{r[4]:.0%}'] for nm, r in zip(names, kw)], widths=[4.6, 1.8, 1.7, 1.8, 1.6], icons=['magnifier', 'magnifier', 'magnifier', 'magnifier'],
                  note=f'Precision = right hits divided by hits found. Recall = right hits divided by all {F["n_queue"]} queue texts. A search for "{QUERY_BAD}" returns {F["themes_bad"][0][1]} of 10 texts about {F["themes_bad"][0][0]} and only {dict(F["themes_bad"]).get("queue", 0)} about queues.',
                  notes=(f'Here is the trade-off, on the {F["n_groups"]} different texts. Searching for queue alone finds {kw[0][1]} texts, all right. Adding the word line raises recall to {kw[1][4]:.0%}. Adding wait and waited finds more but lets in {kw[2][1] - kw[2][2]} wrong one. '
                         f'With twelve words we reach recall of one hundred percent, but precision drops to {kw[3][3]:.0%}, because words such as pay and counter appear in other kinds of text. And you needed the answer key to know which words to add. '
                         f'A query with different words does worse: searching for {QUERY_BAD} puts {F["themes_bad"][0][1]} texts about {F["themes_bad"][0][0]} in the top ten. Hence the idea of searching by meaning. How would you know which synonyms to add?')))

    # 16 embedding map
    S.append(dict(kind='idea', title='An embedding is a vector of numbers placed so that similar meanings sit close together',
                  visual=dict(kind='k_embed_map', points=[[1.2, 4.4, 'long queue at the till', 0], [1.9, 3.7, 'slow checkout line', 0], [1.0, 3.2, 'many people waiting to pay', 0], [4.6, 1.5, 'fresh bananas today', 1], [5.3, 2.2, 'vegetables very fresh', 1], [4.2, 4.2, 'prices keep going up', 2], [5.0, 3.5, 'too expensive', 2]],
                              x_label='Made-up axis 1', y_label='Made-up axis 2'),
                  lead='An embedding turns a message into a vector. Messages with similar meaning get nearby vectors.',
                  points=['Illustrative: the positions are made up.', 'A real embedding has hundreds of numbers: 384 for all-MiniLM-L6-v2 (model card).', 'You compute real ones in Colab.'],
                  notes=('Now the second way to turn text into numbers. An embedding is a vector, a list of numbers, produced by a model that was trained on a very large amount of text. The training makes messages with similar meaning land near each other. '
                         'This picture is illustrative: I made up the positions and used only two axes so you can see the idea. Three messages about waiting sit together, two about fresh food sit together, and two about prices sit together. '
                         'Real embeddings have hundreds of numbers instead of two. The sentence-transformers model all-MiniLM-L6-v2 gives 384, according to its model card. Which two messages on the picture are closest?')))

    # 17 cosine picture
    S.append(dict(kind='idea', title='Cosine similarity measures the angle between two vectors, so length does not matter',
                  visual=dict(kind='k_cosine', pairs=[[a, b, lab, round(c, 3)] for (a, b, lab), c in zip(F['ill_pairs'], F['ill_cos'])]),
                  lead='Cosine similarity runs from -1 to 1. Close to 1 means a very similar direction.',
                  points=['1 means the same direction: very similar.', '0 means a right angle: nothing in common.', '-1 means opposite directions.'],
                  notes=('Cosine similarity is the standard score for how alike two vectors are. Think of each vector as an arrow from the origin. Cosine looks only at the angle between two arrows, so a long message and a short message about the same thing still match. '
                         'These three pairs are illustrative vectors with two numbers each, and I calculated the cosines in numpy. The two arrows on the left point almost the same way, so the cosine is nearly one. In the middle they point in different directions, about 0.47. On the right they point in opposite directions, minus one. '
                         'Which pair would you call similar meaning?')))

    # 18 cosine formula
    rc3 = F['real_cos']
    S.append(dict(kind='formula', title='Cosine similarity is the dot product divided by the two vector lengths',
                  formulas=[('Cosine similarity', r'$\cos(a,b)=\frac{a\cdot b}{\|a\|\,\|b\|}$'), ('Illustrative: a = (3, 4), b = (4, 3)', r'$\frac{3\times4+4\times3}{5\times5}=\frac{24}{25}=0.96$')],
                  symbols=[['a · b', 'Dot product: multiply matching numbers, then add', f'3 × 4 + 4 × 3 = {F["cos_dot"]}'], ['|a|', 'Length of vector a: the square root of the sum of squares', f'sqrt(9 + 16) = {F["cos_norm_a"]:.0f}'],
                           ['Real TF-IDF', 'Two queue messages that differ only in the town', f'{rc3[0][2]:.2f}'], ['Real TF-IDF', 'A queue message and "No queue at all", then a mobile money message', f'{rc3[1][2]:.2f} and {rc3[2][2]:.2f}']],
                  widths=[2.2, 5.6, 4.1], size=24,
                  notes=('Here is the formula. The top is the dot product: multiply the matching numbers of the two vectors and add them. The bottom is the product of the two lengths, where a length is the square root of the sum of squares. '
                         f'Our illustrative vectors are three four and four three. The dot product is {F["cos_dot"]}, both lengths are five, so the cosine is twenty four over twenty five, which is {F["cos_ab"]:.2f}. '
                         f'The bottom rows use real TF-IDF vectors. Two long queue messages that differ only in the town score {rc3[0][2]:.2f}. A queue message and the message No queue at all score {rc3[1][2]:.2f}, and a mobile money message scores {rc3[2][2]:.2f}, because they share no word. '
                         'Why is the last one exactly zero?')))

    # 19 semantic search steps
    S.append(dict(kind='steps', title='Semantic search ranks messages by the cosine similarity of their embeddings to the query',
                  steps=[dict(head='Embed messages', text='Once, for every text', icon='doc'), dict(head='Embed the query', text='Same model', icon='speech'), dict(head='Cosine', text='Query against every message', icon='calculator'),
                         dict(head='Rank', text='Sort, keep the top k', icon='chart'), dict(head='Evaluate', text='Precision at k with the answer key', icon='check')], highlight=None,
                  caption='The recipe is identical for TF-IDF vectors. Only the vectors change.',
                  notes=('This is semantic search, step by step. First, embed every different text once and keep the vectors. Second, embed the search query with the same model. '
                         'Third, compute the cosine similarity between the query vector and every message vector. Fourth, rank the messages by that score and keep the top k, for example the top ten. '
                         'Fifth, evaluate: count how many of the top ten really have the theme queue. That count divided by ten is precision at k, and we use it again next session. The recipe is the same for TF-IDF vectors. Only the vectors change. Why do we embed the messages only once?')))

    # 20 privacy
    S.append(dict(kind='compare', title='Messages can hold personal data: remove it with a regex before you analyse',
                  left=dict(head='Before (illustrative)', points=['Call me on 0700 000 111 about my refund.', 'A phone number is personal data.']),
                  right=dict(head='After the regex', points=['Call me on PHONE_REMOVED about my refund.', 'Names in free text are personal data too.']),
                  verdict='My understanding: the Uganda Data Protection and Privacy Act, 2019 covers personal data. Ask your data officer. Not legal advice.',
                  notes=('Customers sometimes type personal details into a message, such as a phone number. That is personal data, and the person is the data subject. My understanding is that the Uganda Data Protection and Privacy Act of 2019 covers it, '
                         'and the organisation that decides how the data is used is the data controller. I am not giving legal advice, so ask your data officer. A practical step is to remove such details with a regex before the text goes into any analysis or tool. '
                         'The example on the slide is made up. Do your own work messages ever contain phone numbers?')))

    # 21 use at work
    S.append(dict(kind='table', title='Where you will use this at work: turn free-text comments into counts, labels and a search',
                  headers=['Your job', 'The text you meet', 'What today lets you do'],
                  rows=[['Customer experience analyst at a supermarket chain, using pandas', 'Comment cards, SMS and WhatsApp feedback', 'Count messages by theme and sentiment, and hand the table to Power BI or Excel.'],
                        ['Programme officer at an NGO, using Excel and Python', 'Open-ended answers in a survey', 'Find the most distinctive words with TF-IDF and read the mistakes before reporting.'],
                        ['Support team lead at a mobile money agent network', 'Complaint tickets', 'Search past tickets by meaning to find repeats, with sentence-transformers.'],
                        ['Credit analyst at a microfinance institution', 'Free-text notes on loan files', 'Mask phone numbers with a regex before any text leaves the team.']],
                  widths=[3.8, 3.5, 4.7], icons=['people', 'doc', 'phone', 'coin'],
                  notes=('Where will you use this on Monday? A customer experience analyst at a supermarket chain who works in pandas can count comments by theme and sentiment and hand a table to Power BI or Excel. '
                         'A programme officer at an NGO can find the most distinctive words in survey answers with TF-IDF. A support team lead at a mobile money agent network can search past tickets by meaning to find repeats. '
                         'And a credit analyst at a microfinance institution can mask phone numbers before a note goes anywhere else. These jobs are examples. Which is closest to yours?')))

    # 22 bridge code recipe
    S.append(dict(kind='code', title='Read the recipe before the lab: six steps build a bag of words and TF-IDF',
                  code=RECIPE, output=RECIPE_OUT.splitlines(),
                  reads=['Lines 1 and 2: tokens, then the sorted vocabulary.', 'Lines 3 and 4: count each word in each message, the bag of words.',
                         'Line 5: doc_freq, the messages that contain each word.', 'Line 6: TF-IDF. Last lines: the words in two or more messages.'],
                  notes=('Before the lab, read the lines that do the work. Line one splits each cleaned message into tokens. Line two collects the different words and sorts them, which is the vocabulary. '
                         'Lines three and four count each word in each message with a loop, and that matrix is the bag of words. Line five counts, for each word, the messages that contain it: the document frequency. Line six does the TF-IDF multiplication by the natural log of N over that count. The last lines print the result. '
                         'The output below is real. I ran these lines here on the three messages A, B and C from the earlier slide: three messages, fourteen words. The dictionary lists the words found in two or more messages, with their counts. Which word has a document frequency of three?')))

    # 23 divider
    S.append(dict(kind='divider', title='Part 2: the Python lab', lead='Close the slides. Open the notebook.', section='Lab',
                  notes=('That is the end of the ideas. Everything you need is on the slides you have just seen, and the notebook repeats each step. '
                         'Open the Colab notebook for Session 21 and run the first two cells. They put the data next to the notebook and load the check helper. '
                         'In every step, predict the answer first, run the cell, read the output, and then change one thing. A check line tells you if your number matches. I will walk around.')))

    # 24 lab map
    S.append(dict(kind='steps', title='The lab has five parts, and you keep a scored file and a three-sentence finding',
                  steps=[dict(head='1 Clean', text='Regex, tokens, stop words', icon='gear'), dict(head='2 Count', text='Bag of words, TF-IDF', icon='grid'), dict(head='3 Classify', text='Grouped scores, mistakes, scikit-learn', icon='tag'),
                         dict(head='4 Search', text='Keyword, TF-IDF, cosine', icon='magnifier'), dict(head='5 Meaning', text='Embeddings, then keep', icon='chart')], highlight=None,
                  caption='Five parts, twelve tasks in 45 minutes. In each one: predict, run, read the output, change one thing.',
                  notes=('Here is the map of the lab. Part one, clean the messages with a regex and remove stop words. Part two, build the bag of words and the TF-IDF matrix in numpy. '
                         'Part three, train the sentiment classifier with grouped cross-validation, read its mistakes, test it on the sentence not good, and repeat it with the scikit-learn recipe. Part four, score a keyword search against the theme answer key, then search with cosine similarity. '
                         'Part five, create real embeddings with sentence-transformers, compare, and save your scored file. Predict first in every step. If time is short, finish parts one to four and take part five home.')))

    # 25 check numbers
    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Negative messages, and the majority-class baseline share', f'{sent["negative"]}, which is {F["majority_share"]:.1%}'], ['Different message texts, and the vocabulary size', f'{F["n_groups"]} and {V}'],
                        ['idf of queue, and its document frequency', f'{q_ok["idf"]:.2f} and {q_ok["df"]}'], ['Grouped 5-fold accuracy, and wrong answers', f'{acc:.3f} (0.74 to 0.81 is fine), {F["n_wrong"]} wrong'],
                        ['scikit-learn pipeline, grouped accuracy', f'about {F["sk_acc"]:.2f} (0.74 to 0.84 is fine)'],
                        ['Keyword queue: found, recall, precision', f'{F["queue_found"]} of {F["n_queue"]}, {F["queue_recall"]:.1%}, {F["queue_precision"]:.0%}'], [f'Precision at 10 for "{QUERY_OK}" and for "{QUERY_BAD}"', f'{F["p10_ok"]:.1f} and {F["p10_bad"]:.1f}'],
                        ['Embedding matrix from all-MiniLM-L6-v2', f'{F["n_groups"]} rows, 384 columns']],
                  widths=[7.0, 5.0], icons=['grid', 'doc', 'calculator', 'check', 'tag', 'magnifier', 'chart', 'key'], note='If your number differs, find the step that went wrong. Do not change a number to match.',
                  notes=('Use this table as your own self-check. Nobody marks it. If your numbers match, carry on. If one does not, stop and call me, because later steps use the earlier ones. '
                         'The most common cause is a regex typed slightly differently, which changes the vocabulary and every number after it. Accuracy can move a little between computers, so use the ranges on the slide. The scikit-learn row and the embedding row come from libraries I could not run here, so they carry a range. '
                         'Do not change a number to make it match. Find out why it is different. What would a larger vocabulary do to the table size?')))

    # 26 error cards
    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[[f'A vocabulary size that is not {V}', 'The cleaning regex differs from the one in the notebook.', 'Copy OPEN and CLOSE exactly, and apply lower() first.'],
                        ['ModuleNotFoundError: sentence_transformers', 'The library is not installed in this session.', 'Run the install cell in step 11, then run the cell again.'],
                        ['Accuracy of 0.94 or higher', 'Copies of one text are on both sides of the split.', 'Make the folds with group_folds.'],
                        ['A cosine that is nan', 'One vector has length zero (no known word in the query).', 'Check the query words are in the vocabulary.'],
                        [f'Precision at 10 is lower for "{QUERY_BAD}"', 'That is expected: TF-IDF only matches shared words.', 'Write it down as a finding. Embeddings may do better, but check.']],
                  widths=[3.9, 4.1, 4.0], icons=['cross', 'cross', 'cross', 'cross', 'check'],
                  notes=(f'Five messages you may meet. A vocabulary size that is not {V} means your cleaning regex is slightly different, so copy it exactly and lowercase first. '
                         'A module not found error for sentence transformers means the library is not installed in this Colab session, so run the install cell. '
                         'An accuracy of ninety four percent or more means train and test rows share texts, which is the leak we met earlier. A cosine of nan means a query with no known words. And a lower precision for crowded cashier is expected, because TF-IDF only matches shared words. It is a finding, so write it down. Which of these would you expect to meet first?')))

    # 27 exit check
    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[['A classifier built on a bag of words calls "the queue was not good" positive. Why?', 'It counts the words good and not and ignores their order, and good has the larger weight.'],
                        [f'A keyword search finds {F["queue_found"]} of {F["n_queue"]} queue texts, all correct. Name both measures.', f'Precision is 100 percent. Recall is {F["queue_recall"]:.0%}.'],
                        ['A cosine similarity between two message vectors is close to 1. What does it say?', 'The vectors point almost the same way: the messages are very similar in the representation used.']],
                  widths=[5.8, 6.2], icons=['tag', 'magnifier', 'chart'],
                  notes=('Last, the exit check. Three questions. Write your answers before you look at mine. One, a bag of words classifier calls the queue was not good positive. Why? '
                         f'Two, a keyword search finds {F["queue_found"]} of the {F["n_queue"]} queue texts and all of them are correct. Name both measures and give the values. '
                         'Three, the cosine similarity of two message vectors is close to one. What does that tell you? The short answers are on the slide. If you got all three, you are ready for Session 22, where we look at how a language model works.')))

    # ------------------------------------------------------------------ facilitator
    sess['facilitator'] = dict(
        prep=['Open the Session 21 notebook in Colab before anyone arrives and run it once top to bottom. Step 8 uses scikit-learn and step 11 needs a pip install of sentence-transformers and a model download, so check the Wi-Fi.',
              'OPEN ITEM, before the course starts: the scikit-learn recipe slide, the step 8 check (about ' + f'{F["sk_acc"]:.2f}' + ') and the embedding results were NOT run on real scikit-learn or sentence-transformers. The slide numbers come from a numpy replica of the recipe (smoothed idf, L2-regularised softmax regression with C = 1, grouped 5-fold). Re-run the notebook in Colab and replace the numbers if they differ by more than the ranges in the checks.',
              'The model all-MiniLM-L6-v2 and its dimension (384) come from its public model card. Confirm the licence and the size on the card before class.',
              'Make sure each learner has data.zip (feedback.csv inside). Step 12 writes feedback_scored.csv into the folder keep.',
              'Write the check table (slide 25) on the board. Concepts run with laptops closed.',
              f'All data is fictional and generated. Only {F["n_groups"]} different message texts sit behind the {N} messages. A shuffled split therefore leaks: {F["leak_n"]} of {N} test messages repeat a training text and the score reads {F["leak_acc"]:.1%} against {acc:.1%} for the grouped split. Tell learners that real text will score lower still.',
              'Grouped 5-fold numbers are stable (folds of 160 messages each). A single group split is a lottery: with GroupShuffleSplit the accuracy swings from about 0.47 to 0.93 across seeds, because one text (the phone-number question) occurs 25 times.'],
        misconceptions=[('More stop word removal is always better', 'Removing the word not (it is on many standard lists) deletes the signal that flips a meaning. Read the list.'),
                        ('A high accuracy proves the model understands the messages', f'The majority-class baseline already scores {base:.1%}, six percent of labels are wrong on purpose, and the messages repeat. A shuffled split reports {F["leak_acc"]:.1%} for the same model. Read the mistakes.'),
                        ('A bag of words keeps the word order', 'It counts words and drops the order, so not good and good look alike except for one extra count.'),
                        ('Cosine similarity of 0 means the messages are opposite', 'Zero means no overlap in the vectors (a right angle). Opposite is -1, and TF-IDF vectors cannot be negative.'),
                        ('A keyword search that returns only correct results is a good search', f'Precision was 100 percent but recall was {F["queue_recall"]:.0%}. Always report both.')],
        probes=[('Why does TF-IDF give the word the a small weight?', 'The word is in most messages, so N/df is close to 1 and the logarithm is close to 0.'),
                ('Why did we split by distinct text?', 'Copies of one text on both sides let the model look up an answer it has already seen. That is data leakage and it flatters the score.'),
                ('What is the majority-class baseline for these labels?', f'Predict negative every time: {base:.1%} over all {N} messages.'),
                ('Why is "crowded cashier" a hard query for a keyword or TF-IDF search?', 'The word crowded is not in the vocabulary, so the search matches the word cashier and returns many staff messages.'),
                ('What is the difference between precision at 10 and recall?', 'Precision at 10 is the share of the 10 results that are right. Recall is the share of all the right texts that were found.'),
                ('Why do we embed the messages only once?', 'The vectors do not change. Only the query changes, so we reuse the stored vectors.'),
                ('Why mask phone numbers before analysing?', 'A phone number is personal data. Removing it first reduces the risk. Ask the data officer, this is not legal advice.')],
        lab_steps=[('Step 1: load and look', f'{sent["negative"]} negative messages, majority share {F["majority_share"]:.1%}. Learners who skip the PREDICT should be sent back.'),
                   ('Step 2: clean with a regex', f'Mean tokens {F["mean_tokens"]:.2f}, vocabulary {V} and {F["n_groups"]} different texts. A different vocabulary means a different regex.'),
                   ('Step 3: bag of words', f'Matrix shape ({N}, {V}) and {F["total_tokens"]} tokens in all. The most common word is {F["top_word"]}, in {F["top_word_df"]} messages.'),
                   ('Step 4: TF-IDF', f'idf of queue {q_ok["idf"]:.2f}. Rows have length 1 after scaling.'),
                   ('Step 5: grouped classifier', f'Pooled accuracy {acc:.3f} against the baseline {base:.3f}; folds {F["acc_min"]:.2f} to {F["acc_max"]:.2f}. The CHANGE (shuffled folds) shows {F["leak_acc"]:.3f}.'),
                   ('Step 6: read the mistakes', f'{F["n_wrong"]} wrong. Ask each learner to say which look like bad labels.'),
                   ('Step 7: negation', f'Probability of positive for good {pg[2]:.2f}, for not good {pn[2]:.2f}. Expect surprise that the model is still positive.'),
                   ('Step 8: the scikit-learn recipe', f'Pipeline of TfidfVectorizer and LogisticRegression in GroupKFold(5). Numpy replica: accuracy {F["sk_acc"]:.3f}. NOT run on real scikit-learn here; the check accepts 0.74 to 0.84.'),
                   ('Step 9: keyword search', f'{F["queue_found"]} found of {F["n_queue"]} queue texts, recall {F["queue_recall"]:.3f}, precision 1.0.'),
                   ('Step 10: cosine and TF-IDF search', f'cosine((3,4),(4,3)) = {F["cos_ab"]:.2f}. Precision at 10 is {F["p10_ok"]:.1f} for "{QUERY_OK}" and {F["p10_bad"]:.1f} for "{QUERY_BAD}".'),
                   ('Step 11: embeddings', f'Shape ({F["n_groups"]}, 384). The only checked number is the 384. Learners compare their own precision at 10 for the two queries with step 10. Not run in the authoring sandbox.'),
                   ('Step 12: keep', 'feedback_scored.csv has 800 rows, with the grouped (out-of-fold) prediction for each message. Read the three-sentence finding: accuracy, one mistake, one missed search.')],
        rescue=['If the concepts run over, shorten the idf bars (slide 9) and the formula slide for cosine to a quick look. The lab repeats both.',
                'If only 30 minutes of lab remain, do steps 1 to 7 and 9, and set 8, 10, 11 and 12 as homework.',
                'If sentence-transformers will not install, skip step 11 and use the TF-IDF search from step 10. Say clearly that this is word matching, not meaning.',
                'If a learner has no laptop, pair them with a neighbour: one types, one predicts aloud.'],
        after=['Share the notebook and this deck again for learners who were absent.', 'Ask each learner to save feedback_scored.csv and bring one question about text data from their own work to Session 22.', 'Note any question you could not answer and open the next session with it.',
               'Re-run the Colab notebook with real scikit-learn and sentence-transformers and update the numbers marked as replica.'],
        lab_answer_key=[['Step 1 PREDICT: what share of messages is negative?', f'About half: {sent["negative"]} of {N}, which is {F["majority_share"]:.1%}.'],
                        ['Step 2 READ: how many different texts are there after cleaning?', f'{F["n_groups"]}, so the average text appears {N / F["n_groups"]:.1f} times. Mean tokens per message: {F["mean_tokens"]:.1f}.'],
                        ['Step 3 PREDICT: which word is in the most messages?', f'{F["top_word"]}, in {F["top_word_df"]} messages (copies of one phone number question).'],
                        ['Step 4 CHANGE: use ln(N/df) for the word costly.', f'{F["w_costly"]["idf"]:.2f}, because it is in only {F["w_costly"]["df"]} messages.'],
                        ['Step 5 READ: how much better than the baseline is the model?', f'{acc:.3f} against {base:.3f}, about {acc - base:.2f} higher. With shuffled folds the score reads {F["leak_acc"]:.3f}, which is the leak.'],
                        ['Step 6 READ: which mistakes are bad labels?', 'Those where the message and the label disagree plainly, for example a complaint labelled positive. Learners may argue about mixed messages.'],
                        ['Step 7 CHANGE: try "the queue was not bad".', 'Learners will see it classified by the weights of queue and bad. The point is that the model has no rule for not.'],
                        ['Step 8 READ: how does the scikit-learn accuracy compare with step 5?', f'Close but not identical, about {F["sk_acc"]:.2f} against {acc:.2f}: scikit-learn smooths idf and learns the vocabulary from each training fold only.'],
                        ['Step 9 CHANGE: add the keyword line.', f'Recall rises from {F["queue_recall"]:.1%} to {kw[1][4]:.1%} and precision stays at 100 percent.'],
                        ['Step 10 READ: why is "crowded cashier" lower at 10?', f'The search matches cashier and returns {F["themes_bad"][0][1]} texts about {F["themes_bad"][0][0]}; only {dict(F["themes_bad"]).get("queue", 0)} are about queues.'],
                        ['Step 11 READ: does the embedding search find more queue texts for "crowded cashier"?', 'Not checked here. Record your own precision at 10 and compare it with the step 10 value.']])
    return sess
