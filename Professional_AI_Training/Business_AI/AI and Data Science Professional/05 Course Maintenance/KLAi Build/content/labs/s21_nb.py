"""Session 21 lab: text as data and meaning as numbers. Everything runs in numpy and pandas and is verified here, except step 8 (scikit-learn text recipe) and step 11 (sentence-transformers):
those cells are guarded, run only when the library is installed (Colab) and were NOT executed in the authoring sandbox. Expected values come from content/s21.py (facts()).
The learner version runs top to bottom without stopping: unfinished steps report NOT YET."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
BUILD = HERE.parents[2]
sys.path.insert(0, str(BUILD / 'kit'))
import nb as NB  # noqa: E402

_spec = importlib.util.spec_from_file_location('s21_content', BUILD / 'content' / 's21.py')
S = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(S)

TITLE = 'Text as data and meaning as numbers'
NEEDS = []   # steps 8 and 11 are guarded with try/except, so the other steps are verified here


def build(solution: bool) -> NB.Notebook:
    F = S.facts()
    nb = NB.Notebook()

    def todo(hint, sol, lines=None):
        """A cell the learner completes. Learner version: the variable is None with a plain-words hint. Solution: the model answer."""
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

    nb.md('# Session 21: Text as data and meaning as numbers\n\nYou work on the 800 Lakeside Mart customer messages in `feedback.csv`. Rhythm for every step: **predict**, run, **read** the output, **change** one thing. '
          'A line that starts with OK means your number matches. A line that starts with NOT YET means finish that cell. Data is fictional and generated.')
    nb.data_setup()
    nb.check_setup()
    nb.code('# Helper: returns nan instead of stopping when your answer is not ready yet. You do not need to read it.\n'
            'def safe(f):\n    try:\n        return f()\n    except Exception:\n        return float("nan")')

    # step 1
    nb.step(1, 'Load the messages and look first', 'Text is a variable like any other. Load the file and count the labels before any cleaning.')
    nb.code("import os, re\nimport numpy as np\nimport pandas as pd\n\nos.makedirs('keep', exist_ok=True)   # the folder where you save what you keep\nfb = pd.read_csv('feedback.csv')\nprint(fb.shape)\nfb.head()")
    nb.predict('What share of the 800 messages has the sentiment negative: about a fifth, a half or four fifths?')
    todo("count the rows where sentiment is 'negative'", "n_negative = int((fb.sentiment == 'negative').sum())")
    todo('n_negative divided by the number of messages: the majority-class baseline', 'majority_share = n_negative / len(fb)')
    nb.code(f"check('negative messages', safe(lambda: n_negative), {F['sent']['negative']}, 0)\ncheck('majority-class baseline share', safe(lambda: majority_share), {F['majority_share']:.4f}, 0.001)")

    # step 2
    nb.step(2, 'Text preprocessing: lowercase, regex cleaning, tokens, stop words', 'Messages open with Hello. or Feedback: and close with Please reply. A regular expression (regex) removes them. Do not remove the word not.')
    nb.code(f"# Patterns for the opener and closer lines (already written for you)\nOPEN = {S.OPEN!r}\nCLOSE = {S.CLOSE!r}\nSTOP = {S.STOP!r}   # stop words: note that 'not' is NOT in this list")
    nb.predict('How many words will a message have on average once the opener, closer, punctuation and stop words are gone: about 12, 5 or 1?')
    todo('lowercase, remove OPEN, remove CLOSE, then remove every character that is not a letter or space (r"[^a-z\\s]")',
         "clean = (fb.message.str.lower()\n         .str.replace(OPEN, '', regex=True)\n         .str.replace(CLOSE, '', regex=True)\n         .str.replace(r'[^a-z\\s]', '', regex=True))")
    todo('split each clean message into tokens and keep only tokens that are not in STOP',
         'docs = [[w for w in t.split() if w not in STOP] for t in clean]')
    dep("vocab = sorted({w for d in docs for w in d})\nmean_tokens = float(np.mean([len(d) for d in docs]))\nn_texts = clean.nunique()\nprint(len(vocab), 'different words;', round(mean_tokens, 1), 'tokens per message;', n_texts, 'different texts among', len(clean), 'messages')\nclean.head(3).tolist()")
    nb.code(f"check('vocabulary size', safe(lambda: len(vocab)), {F['V']}, 0)\ncheck('mean tokens per message', safe(lambda: mean_tokens), {F['mean_tokens']:.4f}, 0.01)\ncheck('different texts after cleaning', safe(lambda: n_texts), {F['n_groups']}, 0)")
    nb.read('The file has 800 messages but far fewer different texts. What does that mean for a model that is tested on messages it may have already seen? (We deal with this in step 5.)')
    nb.change('Print `fb.message.str.lower().str.contains(r"\\bnot\\b").sum()` and then the same on `clean`. Why do the two counts differ?')

    # step 3
    nb.step(3, 'Bag of words', 'Count each word of the vocabulary in each message. One row per message, one column per word. This is the document-term matrix.')
    nb.predict('Which word is in the most messages? Guess before you run.')
    todo('one row per message, one column per word: d.count(w)', 'X = np.array([[d.count(w) for w in vocab] for d in docs])')
    todo('the number of messages that contain each word is (X > 0).sum(axis=0); take the word with the largest count',
         'top_word = vocab[int((X > 0).sum(axis=0).argmax())]')
    dep("print(X.shape, X.sum(), top_word)")
    nb.code(f"check('columns of X', safe(lambda: X.shape[1]), {F['V']}, 0)\ncheck('tokens counted in X', safe(lambda: X.sum()), {F['total_tokens']}, 0)\ncheck('most common word is {F['top_word']}', safe(lambda: top_word == '{F['top_word']}'), True, 0)")
    nb.read('The top word is a filler about a phone number question. Why does it come first? (Hint: look at `fb.message.value_counts().head(3)`.)')

    # step 4
    nb.step(4, 'TF-IDF', 'Weight each count by how rare the word is: idf = ln(N / df), where df is the number of messages containing the word (the document frequency). Then scale each row to length 1.')
    todo('document frequency: the number of messages in which each word appears, (X > 0).sum(axis=0)', 'doc_freq = (X > 0).sum(axis=0)')
    todo('inverse document frequency: np.log(N / doc_freq) with N = len(fb)', 'idf = np.log(len(fb) / doc_freq)')
    dep("T = X * idf\nT = T / np.linalg.norm(T, axis=1, keepdims=True)   # every row now has length 1\nq = vocab.index('queue')\nprint('queue: document frequency', doc_freq[q], 'idf', round(idf[q], 2))")
    nb.code(f"check('document frequency of queue', safe(lambda: doc_freq[vocab.index('queue')]), {F['w_queue']['df']}, 0)\ncheck('idf of queue', safe(lambda: idf[vocab.index('queue')]), {F['w_queue']['idf']:.4f}, 0.001)")
    nb.change("Print the idf of 'costly' and of 'please'. Which is larger, and why?")

    # step 5
    nb.step(5, 'Sentiment classification, scored on texts the model has not seen', 'Sentiment is the target. The TF-IDF columns are the features. Split by distinct text: all copies of one text go to the same fold (grouped 5-fold cross-validation), so every message is predicted by a model that never saw its text.')
    nb.code("CLASSES = ['negative', 'neutral', 'positive']\ny = fb.sentiment.map({c: i for i, c in enumerate(CLASSES)}).values\n\n"
            "def fit_softmax(X, y, k=3, lr=10.0, epochs=3000):\n    # multinomial logistic regression by gradient descent (already written for you)\n    # the penalty 1/len(X) on the weights is the same strength as scikit-learn's default C = 1\n"
            "    l2 = 1.0 / len(X)\n    W = np.zeros((X.shape[1], k)); b = np.zeros(k); Y = np.eye(k)[y]\n    for _ in range(epochs):\n"
            "        Z = X @ W + b; Z -= Z.max(axis=1, keepdims=True); P = np.exp(Z); P /= P.sum(axis=1, keepdims=True)\n        G = (P - Y) / len(X); W -= lr * (X.T @ G + l2 * W); b -= lr * G.sum(axis=0)\n    return W, b\n\n"
            "def group_folds(group_id, k=5):\n    # fold number for each message, all copies of one text in one fold (the idea inside scikit-learn's GroupKFold)\n    sizes = np.bincount(group_id); order = np.argsort(sizes)[::-1]\n"
            "    load = np.zeros(k); fold_of_group = np.zeros(len(sizes), dtype=int)\n    for g in order:\n        f = int(np.argmin(load)); load[f] += sizes[g]; fold_of_group[g] = f\n    return fold_of_group[group_id]")
    dep("groups = [' '.join(d) for d in docs]                       # the cleaned text of each message\n_, group_id = np.unique(groups, return_inverse=True)   # one number per different text\nfold = group_folds(group_id, 5)\nprint(group_id.max() + 1, 'different texts; messages per fold:', np.bincount(fold))")
    nb.predict('The baseline model says negative for every message. Will the classifier, scored on texts it has not seen, reach 60, 80 or 95 percent?')
    todo('for each fold f: fit on the messages NOT in the fold, predict the messages in the fold, store the predictions',
         "def cv_predict(fold):\n    pred = np.zeros(len(fb), dtype=int)           # one prediction per message, made by a model that never saw its text\n    for f in range(5):\n        test_rows = fold == f\n        W_f, b_f = fit_softmax(T[~test_rows], y[~test_rows])\n        pred[test_rows] = (T[test_rows] @ W_f + b_f).argmax(axis=1)\n    return pred",
         "def cv_predict(fold):\n    return None   # for each of the 5 folds: test_rows = fold == f; fit_softmax on T[~test_rows]; predict T[test_rows]; store in an array of 800 integers")
    dep("oof = cv_predict(fold)   # oof = out-of-fold predictions")
    nb.code("baseline = float((y == 0).mean())   # majority-class baseline: always say negative\naccuracy = safe(lambda: float((oof == y).mean()))\nfold_accuracies = safe(lambda: [round(float((oof[fold == f] == y[fold == f]).mean()), 3) for f in range(5)])\nprint('accuracy', accuracy, 'baseline', baseline, 'by fold', fold_accuracies)")
    nb.code(f"check('grouped 5-fold accuracy', accuracy, {F['acc']:.3f}, 0.04)\ncheck('baseline', baseline, {F['baseline_te']:.3f}, 0.001)")
    nb.read('About 6 percent of the labels are wrong on purpose, and the five fold scores differ. What does that say about trusting one split?')
    nb.change('Now cut the folds at random instead (cell below) and run `cv_predict` again. Compare the accuracy with the grouped one, and count the test messages whose text was also in training.')
    dep("idx0 = np.random.RandomState(42).permutation(len(fb))\nfold_shuffled = np.empty(len(fb), dtype=int)\nfold_shuffled[idx0] = np.arange(len(fb)) // 160   # five random folds of 160 messages\n"
        "oof_shuffled = cv_predict(fold_shuffled)\nleak = 0\nfor f in range(5):\n    seen = set(group_id[fold_shuffled != f])\n    leak += sum(g in seen for g in group_id[fold_shuffled == f])\n"
        "print('shuffled accuracy', float((oof_shuffled == y).mean()), '| test messages with a twin in training:', leak)")
    nb.code(f"check('shuffled 5-fold accuracy (too high)', safe(lambda: float((oof_shuffled == y).mean())), {F['leak_acc']:.4f}, 0.03)\ncheck('test messages with a twin in training', safe(lambda: leak), {F['leak_n']}, 20)")

    # step 6
    nb.step(6, 'Read the mistakes', 'A score is a summary. Read the wrong answers and decide for each: bad label or model error?')
    todo('rows of fb where oof differs from y', 'mistakes = fb[oof != y].assign(model=[CLASSES[i] for i in oof[oof != y]])')
    dep("n_wrong = len(mistakes)\nprint(n_wrong, 'wrong answers')\nmistakes[['message', 'sentiment', 'model']].drop_duplicates('message').head(11)")
    nb.code(f"check('wrong answers', safe(lambda: n_wrong), {F['n_wrong']}, 8)")
    nb.read('How many of the wrong answers look like a bad label (the message and the label disagree plainly)? Write the number and one example.')

    # step 7
    nb.step(7, 'Where counting words fails: negation', 'A bag of words ignores word order. Fit one final model on all 800 messages and test two new sentences.')
    todo('fit on all rows: fit_softmax(T, y)', 'W, b = fit_softmax(T, y)', 'W, b = None, None  # fit_softmax(T, y)')
    nb.code("STOPSET = set(STOP)\ndef tokens(text):\n    t = re.sub(CLOSE, '', re.sub(OPEN, '', text.lower()))\n    return [w for w in re.sub(r'[^a-z\\s]', '', t).split() if w not in STOPSET]\n\n"
            "def predict_proba(text):\n    v = np.zeros(len(vocab))\n    for w in tokens(text):\n        if w in vocab:\n            v[vocab.index(w)] += 1\n    v = v * idf\n    v = v / np.linalg.norm(v)\n    z = v @ W + b\n    p = np.exp(z - z.max())\n    return p / p.sum()")
    nb.predict('Will the model call "the queue was not good" negative or positive?')
    todo("predict_proba('the queue was good')[2]  (index 2 is positive)", "p_good = float(predict_proba('the queue was good')[2])")
    todo("predict_proba('the queue was not good')[2]", "p_notgood = float(predict_proba('the queue was not good')[2])")
    nb.code(f"print(safe(lambda: round(p_good, 2)), safe(lambda: round(p_notgood, 2)))\ncheck('probability of positive: the queue was good', safe(lambda: p_good), {F['p_good'][2]:.3f}, 0.05)\ncheck('probability of positive: the queue was not good', safe(lambda: p_notgood), {F['p_notgood'][2]:.3f}, 0.05)")
    nb.change('Try "the queue was not bad" and "the queue was terrible". Which does the model get right, and which words does it rely on?')

    # step 8
    nb.step(8, 'The same recipe with scikit-learn (the tools used at work)', 'CountVectorizer builds the bag of words. TfidfVectorizer builds TF-IDF. make_pipeline chains the vectoriser and a classifier so the vocabulary and idf are learned from the training folds only.')
    nb.code("try:\n    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\n    from sklearn.linear_model import LogisticRegression\n    from sklearn.metrics import classification_report\n"
            "    from sklearn.model_selection import GroupKFold, cross_val_predict\n    from sklearn.pipeline import make_pipeline\n    HAVE_SK = True\nexcept ImportError:\n    HAVE_SK = False\n    print('scikit-learn is not installed here. Run this step in Colab.')")
    nb.code("if HAVE_SK:\n    texts = [' '.join(d) for d in docs] if docs is not None else []   # the cleaned text of each message")
    nb.predict('The vocabulary of CountVectorizer should match your vocab. Will its idf for queue match the idf you computed in step 4? Guess, then run.')
    todo('CountVectorizer().fit_transform(texts)', "if HAVE_SK:\n    counts = CountVectorizer().fit_transform(texts)\n    tfidf = TfidfVectorizer().fit(texts)\n    idf_queue_sk = float(tfidf.idf_[tfidf.vocabulary_['queue']])",
         "if HAVE_SK:\n    counts = None  # CountVectorizer().fit_transform(texts)\n    tfidf = None   # TfidfVectorizer().fit(texts)\n    idf_queue_sk = None   # tfidf.idf_[tfidf.vocabulary_['queue']]")
    nb.code(f"if HAVE_SK:\n    check('scikit-learn vocabulary size', safe(lambda: counts.shape[1]), {F['V']}, 0)\n    check('scikit-learn idf of queue (smoothed formula)', safe(lambda: idf_queue_sk), {F['sk_idf_queue']:.3f}, 0.02)")
    nb.read('scikit-learn adds 1 inside the logarithm and 1 outside: idf = ln((1 + N) / (1 + df)) + 1. Why is its idf for queue larger than yours?')
    todo('make_pipeline(TfidfVectorizer(), LogisticRegression(max_iter=1000)), then cross_val_predict(pipe, texts, y, groups=group_id, cv=GroupKFold(n_splits=5))',
         "if HAVE_SK:\n    pipe = make_pipeline(TfidfVectorizer(), LogisticRegression(max_iter=1000))\n    pred_sk = cross_val_predict(pipe, texts, y, groups=group_id, cv=GroupKFold(n_splits=5))",
         "if HAVE_SK:\n    pipe = None     # make_pipeline(TfidfVectorizer(), LogisticRegression(max_iter=1000))\n    pred_sk = None  # cross_val_predict(pipe, texts, y, groups=group_id, cv=GroupKFold(n_splits=5))")
    nb.code(f"if HAVE_SK:\n    accuracy_sk = safe(lambda: float((pred_sk == y).mean()))\n    print('accuracy', accuracy_sk)\n    safe(lambda: print(classification_report(y, pred_sk, target_names=CLASSES)))\n"
            f"    check('scikit-learn pipeline, grouped accuracy', accuracy_sk, {F['sk_acc']:.3f}, 0.05)")
    nb.change('Replace LogisticRegression with another classifier from the Session 17 family and compare the grouped accuracy. Which wins, and by how much?')

    # step 9
    nb.step(9, 'Score a keyword search with the answer key', 'The theme variable says what each message is about, so it is an answer key. Search one row per different text, so ten copies of one sentence cannot fill the results.')
    dep("first_row = np.array([np.where(group_id == g)[0][0] for g in range(group_id.max() + 1)])\nufb = fb.iloc[first_row].reset_index(drop=True)      # one row per different text\nudocs = [docs[i] for i in first_row]\nuT = T[first_row]\nprint(len(ufb), 'different texts to search')")
    todo("a True/False array: ufb.theme == 'queue' (use .values)", "is_queue = (ufb.theme == 'queue').values")
    todo("a True/False array: does 'queue' appear in the tokens of each text in udocs", "has_word = np.array(['queue' in d for d in udocs])")
    todo('the number of texts that are both queue texts and contain the word', 'n_found = int((is_queue & has_word).sum())')
    todo('n_found divided by the number of queue texts: recall', 'recall = n_found / is_queue.sum()')
    nb.code(f"print(safe(lambda: n_found), 'of', safe(lambda: is_queue.sum()), 'found; recall', safe(lambda: round(recall, 3)))\ncheck('queue texts found', safe(lambda: n_found), {F['queue_found']}, 0)\ncheck('recall of the keyword search', safe(lambda: recall), {F['queue_recall']:.4f}, 0.005)")
    nb.change("Search for 'queue' or 'line' (use `any(k in d for k in ['queue', 'line'])`). What happens to recall and to precision?")

    # step 10
    nb.step(10, 'Cosine similarity and TF-IDF search', 'Cosine similarity: the dot product of two vectors divided by the product of their lengths.')
    todo('dot product divided by the product of the two vector lengths (np.linalg.norm)', 'def cosine(a, b):\n    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))',
         'def cosine(a, b):\n    return None  # a @ b divided by (length of a times length of b)')
    nb.code(f"c_ab = cosine(np.array([3, 4]), np.array([4, 3]))\nprint(c_ab)\ncheck('cosine of (3,4) and (4,3)', safe(lambda: c_ab), {F['cos_ab']:.2f}, 0.001)")
    nb.code("def query_vector(text):\n    v = np.zeros(len(vocab))\n    for w in tokens(text):\n        if w in vocab:\n            v[vocab.index(w)] += 1\n    v = v * idf\n    return v / np.linalg.norm(v)\n\n"
            "def precision_at_10(text):\n    scores = uT @ query_vector(text)         # rows of uT have length 1, so this is the cosine\n    top = np.argsort(-scores, kind='stable')[:10]\n    return float((ufb.theme.values[top] == 'queue').mean())")
    nb.predict('Which query finds more queue texts in its top 10: "many people waiting to pay" or "crowded cashier"?')
    todo('precision_at_10 of the first query', f"p10_ok = precision_at_10({S.QUERY_OK!r})")
    todo('precision_at_10 of the second query', f"p10_bad = precision_at_10({S.QUERY_BAD!r})")
    nb.code(f"print(p10_ok, p10_bad)\ncheck('precision at 10, many people waiting to pay', safe(lambda: p10_ok), {F['p10_ok']:.1f}, 0.05)\ncheck('precision at 10, crowded cashier', safe(lambda: p10_bad), {F['p10_bad']:.1f}, 0.05)")
    nb.read('The word crowded is not in the vocabulary. Which words did the second query actually use, and what are the top 3 texts about?')

    # step 11
    nb.step(11, 'Semantic search with embeddings (needs sentence-transformers, free in Colab)', 'An embedding model turns each text into a vector of 384 numbers. Then the same cosine search ranks by meaning.')
    nb.code("import sys\nif 'google.colab' in sys.modules:\n    try:\n        import sentence_transformers\n    except ImportError:\n        import subprocess\n        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'sentence-transformers'])\n"
            "try:\n    from sentence_transformers import SentenceTransformer\n    HAVE_ST = True\nexcept ImportError:\n    HAVE_ST = False\n    print('sentence-transformers is not installed here. Run this step in Colab.')")
    nb.predict('Will "crowded cashier" now find more queue texts than in step 10? Write your guess, then run.')
    if solution:
        nb.code("if HAVE_ST:\n    model_st = SentenceTransformer('all-MiniLM-L6-v2')   # check its model card for size and licence\n    emb = model_st.encode(ufb.message.tolist(), normalize_embeddings=True)\n    check('embedding columns (384)', emb.shape[1], 384, 0)\n    check('embedding rows (one per different text)', emb.shape[0], len(ufb), 0)\n"
                "    for text in ['many people waiting to pay', 'crowded cashier']:\n        scores = emb @ model_st.encode([text], normalize_embeddings=True)[0]\n        top = np.argsort(-scores, kind='stable')[:10]\n        print(text, '-> precision at 10:', float((ufb.theme.values[top] == 'queue').mean()))")
    else:
        nb.code("if HAVE_ST:\n    model_st = SentenceTransformer('all-MiniLM-L6-v2')   # check its model card for size and licence\n    emb = None  # model_st.encode(list of texts, normalize_embeddings=True)\n    check('embedding columns (384)', safe(lambda: emb.shape[1]), 384, 0)\n    check('embedding rows (one per different text)', safe(lambda: emb.shape[0]), len(ufb), 0)\n"
                "    for text in ['many people waiting to pay', 'crowded cashier']:\n        try:\n            scores = emb @ model_st.encode([text], normalize_embeddings=True)[0]\n            top = np.argsort(-scores, kind='stable')[:10]\n            print(text, '-> precision at 10:', float((ufb.theme.values[top] == 'queue').mean()))\n        except Exception:\n            print(text, '-> not ready yet')")
    nb.read('Write your two precision-at-10 numbers from this step and compare them with step 10. Which query changed, and why? (No number is printed in the slides because it was not run when the slides were written.)')

    # step 12
    nb.step(12, 'Keep: a scored file and a three-sentence finding', 'Save every message with the prediction a model made without seeing its text. Then write your finding in the cell below.')
    todo('the out-of-fold predictions from step 5: oof', 'all_pred = oof', 'all_pred = None  # the out-of-fold predictions from step 5 (oof)')
    dep("scored = fb[['feedback_id', 'message', 'theme', 'sentiment']].copy()\nscored['predicted_sentiment'] = [CLASSES[i] for i in all_pred]\nscored['correct'] = scored.sentiment == scored.predicted_sentiment\nscored.to_csv('keep/feedback_scored.csv', index=False)\nprint(len(scored), 'rows saved in the folder keep; accuracy on all 800 (grouped):', round(float(scored.correct.mean()), 3))")
    nb.code(f"check('rows in feedback_scored.csv', safe(lambda: len(scored)), 800, 0)\ncheck('accuracy on all 800 messages (grouped predictions)', safe(lambda: scored.correct.mean()), {F['acc']:.3f}, 0.04)\nshow_checks()")
    nb.md('**My finding (three sentences):** 1) the grouped accuracy and the baseline, 2) one mistake I read and who was wrong, 3) one search the keyword method missed.\n\n> ')
    return nb
