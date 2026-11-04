"""Session 16 lab notebook: judging a model (baseline, confusion matrix, precision, recall, F1, ROC and AUC, class_weight, leakage, tune before you test, stratified k-fold).
Expected values come from content/s16.py facts(), built on content/loans_canon.py (NumPy replicas).

NEEDS: the build sandbox has no scikit-learn, so make_notebooks.py reports UNVERIFIED (every cell compiles). ref/fx_prove_nb.py 16 runs every cell, learner and solution, against a small shim of
scikit-learn built on loans_canon: it proves the cell order and that the learner version reaches show_checks with NOT YET and no traceback. It does NOT prove what real scikit-learn prints (the shim shares
the replica code, so matching numbers are circular). Re-run the solution on real scikit-learn in Colab before the course starts.
Tolerances (a real library can move a count by a few loans): counts at 0.20 within 4 to 8 loans; precision and recall within 0.02 to 0.04; AUC within 0.01; the best-F1 threshold accepts 0.15 or 0.20
(their F1 values are 0.401 and 0.408); balanced-weight flagged loans within 30; cross-validated AUC within 0.01."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'kit'))
sys.path.insert(0, str(HERE.parent))
import nb as NB  # noqa: E402
import s16  # noqa: E402

TITLE = 'Judging a model'
NEEDS = ['scikit_learn_full']


def build(solution):
    F = s16.facts()
    m = F['m']
    M2, M5 = m[0.2], m[0.5]
    nb = NB.Notebook()

    def ans(sol, placeholder, hint):
        return sol if solution else f'{placeholder}   # your code here: {hint}'

    nb.md('# Session 16 lab: Judging a model\n\n'
          'You will compute accuracy, precision, recall and F1 **by hand with NumPy**, check them against scikit-learn, draw the ROC curve, try `class_weight`, find a column that **leaks** the answer, '
          'tune before you test, and use **stratified cross-validation**. Same 8,000 loans and the same split as Session 15. All data is fictional.\n\n'
          'Rhythm: **PREDICT**, run, **READ**, **CHANGE**. Cells with `# your code here` hold a placeholder: replace that line with your answer and run the cells in order. '
          'The `check(...)` lines print NOT YET until your number is right. What you keep: this notebook and `model_comparison.csv`.')
    nb.data_setup()
    nb.check_setup()
    nb.md('### Preparation (the same as Sessions 14 and 15)\n\nRun this cell. It prepares the 8,000 loans, one-hot encodes the text, splits 75 and 25 with `stratify=y`, and fits the logistic regression pipeline from last session. '
          '`y_prob` holds the predicted probability of default for each test loan. The helper `safe` lets a check say NOT YET instead of stopping the notebook.')
    nb.code('import numpy as np\nimport pandas as pd\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LogisticRegression\n\n'
            'def safe(f):\n    try:\n        return f()\n    except Exception:\n        return np.nan\n\n'
            'loans = pd.read_csv("loans.csv")\n'
            'bad_age = (loans.age < 18) | (loans.age > 100)                      # two impossible ages\nloans.loc[bad_age, "age"] = loans.loc[~bad_age, "age"].median()\n'
            'loans["income_missing"] = loans.monthly_income_ugx.isna().astype(int)\n'
            'loans["monthly_income_ugx"] = loans.monthly_income_ugx.fillna(loans.monthly_income_ugx.median())\n'
            '# 1.15 is an illustrative assumption for interest and fees, not in the data\n'
            'loans["instalment_to_income"] = loans.loan_amount_ugx * 1.15 / loans.term_months / loans.monthly_income_ugx\n'
            'FEATURES = ["age", "monthly_income_ugx", "income_missing", "loan_amount_ugx", "term_months", "previous_loans",\n'
            '            "previous_late_payments", "group_loan", "savings_balance_ugx", "has_mobile_money", "distance_to_branch_km", "instalment_to_income"]\n'
            'X = pd.concat([loans[FEATURES], pd.get_dummies(loans[["gender", "occupation", "loan_purpose"]], dtype=int)], axis=1)\ny = loans["default"]\n'
            'X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)\n'
            'model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))   # C = 1.0 and an L2 penalty are the defaults\n'
            'model.fit(X_train, y_train)\ny_prob = model.predict_proba(X_test)[:, 1]\nactual = (y_test == 1).to_numpy()\n'
            'print(len(X_train), len(X_test), int(actual.sum()), "defaults in the test loans")')

    # ------------------------------------------------------------------ step 1
    nb.step(1, 'The baseline model and the accuracy paradox', 'Before judging a model, score the simplest one.')
    nb.predict('A baseline model says "no default" for every loan. Will its accuracy on the test loans be above or below 0.80? How many defaults will it find?')
    nb.code('from sklearn.dummy import DummyClassifier\n\n'
            'baseline_model = ' + ans('DummyClassifier(strategy="most_frequent")', 'DummyClassifier(strategy="constant", constant=1)', 'DummyClassifier(strategy="most_frequent")') + '\n'
            'baseline_model.fit(X_train, y_train)\n'
            'baseline_acc = ' + ans('baseline_model.score(X_test, y_test)', 'np.nan', 'the accuracy of the baseline on X_test and y_test (hint: baseline_model.score)') + '\n'
            'baseline_flag = baseline_model.predict(X_test)\nbaseline_recall = float(((baseline_flag == 1) & actual).sum() / actual.sum())\nprint("baseline accuracy:", round(baseline_acc, 4), " recall:", baseline_recall)')
    nb.code(f'check("baseline accuracy", safe(lambda: baseline_acc), {F["base_acc"]!r}, 0.001)\ncheck("baseline recall", baseline_recall, 0, 0.001)')
    nb.read('The baseline has a high accuracy and a recall of zero. Why can accuracy not be the only number we report here?')

    # ------------------------------------------------------------------ step 2
    nb.step(2, 'The confusion matrix, precision, recall and F1 by hand', 'Count the four cells with NumPy, apply the formulas, then ask scikit-learn for the same numbers.')
    nb.predict('At a decision threshold of 0.20, will precision be higher or lower than recall? Write down a guess for both.')
    nb.code('flag = y_prob >= 0.20\n'
            'tp = ' + ans('int((flag & actual).sum())      # flagged and really defaulted', 'np.nan', 'flagged AND really defaulted (flag & actual)') + '\n'
            'fp = ' + ans('int((flag & ~actual).sum())     # flagged but repaid', 'np.nan', 'flagged but repaid (flag & ~actual)') + '\n'
            'fn = ' + ans('int((~flag & actual).sum())     # not flagged but defaulted', 'np.nan', 'not flagged but defaulted (~flag & actual)') + '\n'
            'tn = ' + ans('int((~flag & ~actual).sum())    # not flagged and repaid', 'np.nan', 'not flagged and repaid (~flag & ~actual)') + '\n'
            'accuracy = ' + ans('(tp + tn) / (tp + fp + fn + tn)', 'np.nan', '(tp + tn) / all four counts') + '\n'
            'precision = ' + ans('tp / (tp + fp)', 'np.nan', 'tp / (tp + fp)') + '\n'
            'recall = ' + ans('tp / (tp + fn)', 'np.nan', 'tp / (tp + fn)') + '\n'
            'f1 = ' + ans('2 * precision * recall / (precision + recall)', 'np.nan', '2 * precision * recall / (precision + recall)') + '\n'
            'print("TP", tp, "FP", fp, "FN", fn, "TN", tn)\nprint("accuracy", round(accuracy, 3), "precision", round(precision, 3), "recall", round(recall, 3), "F1", round(f1, 3))')
    nb.md('Now ask scikit-learn. Notice that its confusion matrix puts the **negative class first**: `[[TN, FP], [FN, TP]]`.')
    nb.code('from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score\n\n'
            'print(confusion_matrix(y_test, flag))\nprint("precision", round(precision_score(y_test, flag), 3), "recall", round(recall_score(y_test, flag), 3), "F1", round(f1_score(y_test, flag), 3))')
    nb.code(f'check("true positives at 0.20", safe(lambda: tp), {M2["tp"]}, 4)\ncheck("false positives at 0.20", safe(lambda: fp), {M2["fp"]}, 8)\ncheck("false negatives at 0.20", safe(lambda: fn), {M2["fn"]}, 4)\n'
            f'check("true negatives at 0.20", safe(lambda: tn), {M2["tn"]}, 8)\ncheck("precision at 0.20", safe(lambda: precision), {M2["precision"]!r}, 0.02)\ncheck("recall at 0.20", safe(lambda: recall), {M2["recall"]!r}, 0.02)\n'
            f'check("F1 at 0.20", safe(lambda: f1), {M2["f1"]!r}, 0.02)\n'
            'check("your precision equals scikit-learn", safe(lambda: precision), precision_score(y_test, flag), 1e-9)\ncheck("your recall equals scikit-learn", safe(lambda: recall), recall_score(y_test, flag), 1e-9)\n'
            'check("your F1 equals scikit-learn", safe(lambda: f1), f1_score(y_test, flag), 1e-9)')
    nb.read('Compare your accuracy at 0.20 with the baseline accuracy from Step 1. Which is higher? Which model is more useful to a lender, and why?')
    nb.change('Raise the decision threshold to 0.50. Store the new precision in `precision_05` and recall in `recall_05`. Predict first: which goes up and which goes down?')
    nb.code('flag_05 = y_prob >= 0.50\n'
            'precision_05 = ' + ans('precision_score(y_test, flag_05)', 'np.nan', 'precision_score(y_test, flag_05)') + '\n'
            'recall_05 = ' + ans('recall_score(y_test, flag_05)', 'np.nan', 'recall_score(y_test, flag_05)') + '\n'
            'print("precision", round(precision_05, 3), "recall", round(recall_05, 3))\n'
            f'check("precision at 0.50", safe(lambda: precision_05), {M5["precision"]!r}, 0.04)\ncheck("recall at 0.50", safe(lambda: recall_05), {M5["recall"]!r}, 0.02)')
    nb.md('Try five thresholds in a table. The loop is given: read the table, then choose the threshold with the highest F1. (F1 at 0.20 and at 0.15 are close, so the check accepts either.)')
    nb.code('rows = []\nfor t in [0.5, 0.3, 0.2, 0.15, 0.1]:\n    f = y_prob >= t\n    rows.append({"threshold": t, "flagged": int(f.sum()), "precision": precision_score(y_test, f), "recall": recall_score(y_test, f), "f1": f1_score(y_test, f), "accuracy": accuracy_score(y_test, f)})\n'
            'results = pd.DataFrame(rows).set_index("threshold")\nprint(results.round(3))\n'
            'best_t = ' + ans('float(results["f1"].idxmax())', 'np.nan', 'the threshold (index) with the highest f1, results["f1"].idxmax()') + '\n'
            'print("best F1 at threshold", best_t)')
    nb.code('check("threshold with the best F1 (0.15 or 0.20)", safe(lambda: best_t), 0.175, 0.03)')

    # ------------------------------------------------------------------ step 3
    nb.step(3, 'ROC curve, AUC and class_weight', 'AUC judges the ranking of the loans at every threshold at once. The ROC curve plots the true positive rate (recall, sensitivity) against the false positive rate.')
    nb.predict('The AUC is the chance that a random defaulter gets a higher probability than a random repaid loan. Guess the AUC of this model: nearer 0.5, 0.75 or 0.95?')
    nb.code('from sklearn.metrics import roc_auc_score, roc_curve, precision_recall_curve\nimport matplotlib.pyplot as plt\n\n'
            'auc = ' + ans('roc_auc_score(y_test, y_prob)', 'np.nan', 'roc_auc_score(y_test, y_prob). Pass the probabilities, not the yes or no flags') + '\n'
            '# the same number by counting pairs: a defaulter against a repaid loan\npos, neg = y_prob[actual], y_prob[~actual]\n'
            'auc_pairs = ' + ans('float((pos[:, None] > neg[None, :]).mean() + 0.5 * (pos[:, None] == neg[None, :]).mean())', 'np.nan',
                                 'the share of (defaulter, repaid) pairs where the defaulter has the higher probability (ties count half)') + '\n'
            'print("AUC", round(auc, 3), " by pairs", round(auc_pairs, 3), " pairs:", len(pos) * len(neg))\n'
            'print("Gini coefficient = 2 x AUC - 1 =", round(2 * auc - 1, 3))\n'
            'fpr, tpr, _ = roc_curve(y_test, y_prob)\nprec, rec, _ = precision_recall_curve(y_test, y_prob)\n'
            'fig, ax = plt.subplots(1, 2, figsize=(10, 4))\nax[0].plot(fpr, tpr)\nax[0].plot([0, 1], [0, 1], linestyle="--")\nax[0].set_xlabel("false positive rate")\nax[0].set_ylabel("true positive rate (recall)")\nax[0].set_title("ROC curve")\n'
            'ax[1].plot(rec, prec)\nax[1].axhline(actual.mean(), linestyle="--")\nax[1].set_xlabel("recall")\nax[1].set_ylabel("precision")\nax[1].set_title("Precision-recall curve")\nplt.show()')
    nb.code(f'check("AUC", safe(lambda: auc), {F["auc"]!r}, 0.01)\ncheck("AUC by counting pairs equals roc_auc_score", safe(lambda: auc_pairs - auc) + 0.0, 0, 1e-6)')
    nb.read('Find the dashed lines. What does the diagonal in the ROC curve mean, and what does the dashed horizontal line in the precision-recall curve mean?')
    nb.change('Fit the same pipeline with `class_weight="balanced"`. Predict first: will the AUC change a lot? Will more or fewer loans be flagged at a decision threshold of 0.50?')
    nb.code('weighted_model = ' + ans('make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, class_weight="balanced"))', 'make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))',
                                     'make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, class_weight="balanced"))') + '\n'
            'weighted_model.fit(X_train, y_train)\ny_prob_w = weighted_model.predict_proba(X_test)[:, 1]\n'
            'flagged_w = ' + ans('int((y_prob_w >= 0.50).sum())', 'np.nan', 'the number of test loans with y_prob_w at or above 0.50') + '\n'
            'auc_w = roc_auc_score(y_test, y_prob_w)\nrecall_w = recall_score(y_test, y_prob_w >= 0.50)\n'
            'print("flagged at 0.50 with balanced weights:", flagged_w, " plain model:", int((y_prob >= 0.50).sum()))\nprint("recall", round(recall_w, 3), " AUC", round(auc_w, 3))')
    nb.code(f'check("loans flagged with balanced weights", safe(lambda: flagged_w), {F["w05"]["flagged"]}, 30)\ncheck("recall with balanced weights", recall_w, {F["w05"]["recall"]!r}, 0.04)\ncheck("AUC with balanced weights", auc_w, {F["auc_w"]!r}, 0.01)')

    # ------------------------------------------------------------------ step 4
    nb.step(4, 'The leak hunt', 'A model that looks too good to be true usually is. Find the column that gives the answer away.')
    nb.predict('Session 15 left out the column `collection_calls`. If we add it, will the AUC go up a little or a lot? Write your guess.')
    nb.code('correlations = loans[FEATURES + ["collection_calls", "default"]].corr()["default"].drop("default").abs().sort_values(ascending=False)\nprint(correlations.head(4).round(3))\n'
            'leak = ' + ans('correlations.index[0]', '""', 'the name of the variable with the strongest correlation with default') + '\n'
            'calls_by_outcome = loans.groupby("default")["collection_calls"].agg(["mean", "min", "max"])\nprint(calls_by_outcome.round(2))')
    nb.code(f'check("the leaking column is collection_calls", int(leak == "collection_calls"), 1, 0)\ncheck("average calls on defaulted loans", calls_by_outcome.loc[1, "mean"], {F["calls_mean"][1]!r}, 0.01)\n'
            f'check("fewest calls on a defaulted loan", calls_by_outcome.loc[1, "min"], {F["calls_min_default"]}, 0)')
    nb.read('Every defaulted loan has at least one call. When are collection calls made: before or after the loan goes bad? Why does that make this column unusable for a lender who must decide at approval?')
    nb.code('X_leaky = X.copy()\nX_leaky["collection_calls"] = loans["collection_calls"]\n'
            'XL_train, XL_test, yL_train, yL_test = train_test_split(X_leaky, y, test_size=0.25, stratify=y, random_state=42)\n'
            'leaky_model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))\nleaky_model.fit(XL_train, yL_train)\n'
            'y_prob_leaky = ' + ans('leaky_model.predict_proba(XL_test)[:, 1]', 'np.full(len(XL_test), 0.5)', 'the probability of default from leaky_model.predict_proba(XL_test), column 1') + '\n'
            'auc_leaky = ' + ans('roc_auc_score(yL_test, y_prob_leaky)', 'np.nan', 'roc_auc_score of yL_test against y_prob_leaky') + '\n'
            'print("AUC honest", round(auc, 3), " AUC with the leak", round(auc_leaky, 3))')
    nb.code(f'check("AUC of the leaky model", safe(lambda: auc_leaky), {F["auc_leak"]!r}, 0.01)')
    nb.change('The leaky model would fail on a new applicant. Why? Write one sentence in your own words in the cell below.')
    nb.md('> My sentence: ')

    # ------------------------------------------------------------------ step 5
    nb.step(5, 'Tune before you test, stratified cross-validation, and the table you keep', 'One split can be lucky. Five folds, each keeping the same default rate, give a mean and a spread. '
            'Settings are chosen on the training loans (validation set or cross-validation). The test loans are scored once.')
    nb.predict('Will the five fold AUC scores for the honest model be nearly identical or differ by a few hundredths?')
    nb.code('from sklearn.model_selection import StratifiedKFold, cross_val_score\n\ncv = StratifiedKFold(n_splits=5)   # no shuffle: the loans are in date order, so each fold is a block of months\n'
            'print("defaults in each fold of 1,600 loans:", [int(y.iloc[test].sum()) for _, test in cv.split(X, y)])\n'
            'cv_honest = ' + ans('cross_val_score(model, X, y, cv=cv, scoring="roc_auc")', 'np.full(5, np.nan)', 'cross_val_score(model, X, y, cv=cv, scoring="roc_auc")') + '\n'
            'cv_leaky = ' + ans('cross_val_score(model, X_leaky, y, cv=cv, scoring="roc_auc")', 'np.full(5, np.nan)', 'the same with X_leaky') + '\n'
            'print("honest:", cv_honest.round(3), "mean", round(cv_honest.mean(), 3), "std", round(cv_honest.std(ddof=1), 3))\nprint("leaky: ", cv_leaky.round(3), "mean", round(cv_leaky.mean(), 3))')
    nb.code(f'check("defaults in each fold", [int(y.iloc[test].sum()) for _, test in cv.split(X, y)], {F["fold_pos"]!r}, 0)\ncheck("mean AUC, honest features", safe(lambda: cv_honest.mean()), {float(F["cv_honest"].mean())!r}, 0.01)\n'
            f'check("mean AUC, with the leak", safe(lambda: cv_leaky.mean()), {float(F["cv_leak"].mean())!r}, 0.01)')
    nb.read('Does cross-validation find the leak? Look at the leaky scores: are they unstable?')
    nb.change('Tune before you test: run the same cross-validation on the TRAINING loans only (X_train, y_train). These 6,000 loans give folds of 1,200. Compare the mean with the test AUC from Step 3.')
    nb.code('cv_train = ' + ans('cross_val_score(model, X_train, y_train, cv=cv, scoring="roc_auc")', 'np.full(5, np.nan)', 'cross_val_score(model, X_train, y_train, cv=cv, scoring="roc_auc")') + '\n'
            'print("training loans only:", cv_train.round(3), "mean", round(cv_train.mean(), 3), "std", round(cv_train.std(ddof=1), 3), " test AUC:", round(auc, 3))\n'
            f'check("mean AUC on the training loans", safe(lambda: cv_train.mean()), {float(F["cv_train"].mean())!r}, 0.01)')
    nb.md('Last, the **model comparison table** you keep: one row per model, with the evaluation metrics that matter for a lender. The function is given.')
    nb.code('def comparison_row(name, prob, threshold):\n    f = prob >= threshold\n    return {"model": name, "threshold": threshold, "precision": precision_score(y_test, f, zero_division=0), "recall": recall_score(y_test, f, zero_division=0),\n'
            '            "f1": f1_score(y_test, f, zero_division=0), "auc": roc_auc_score(y_test, prob)}\n\n'
            'rows = [comparison_row("Baseline: flag nobody", np.zeros(len(y_test)), 0.5),\n        comparison_row("Logistic regression", y_prob, 0.20),\n        comparison_row("Logistic regression, balanced weights", y_prob_w, 0.50)]\n'
            + ans('rows.append(comparison_row("With collection_calls (leaked, do not use)", y_prob_leaky, 0.20))', 'rows.append(comparison_row("your row here", np.zeros(len(y_test)), 0.5))',
                  'add a fourth row for the leaky model: comparison_row("With collection_calls (leaked, do not use)", y_prob_leaky, 0.20)') + '\n'
            'comparison = pd.DataFrame(rows)\ncomparison.to_csv("model_comparison.csv", index=False)\nprint(comparison.round(3).to_string(index=False))')
    nb.code('check("rows in the comparison table", len(comparison), 4, 0)\n'
            f'check("AUC of the honest model in the table", safe(lambda: comparison.loc[1, "auc"]), {F["auc"]!r}, 0.01)\ncheck("AUC of the leaky model in the table", safe(lambda: comparison.loc[3, "auc"]), {F["auc_leak"]!r}, 0.01)')
    nb.code('show_checks()')
    if solution:
        nb.md(f'### My verdict (example)\n\nThe honest logistic regression has a test AUC of about {F["auc"]:.2f} (Gini {F["gini"]:.2f}) and, at decision threshold 0.20, finds about {M2["recall"] * 100:.0f} percent of the defaults with {M2["precision"] * 100:.0f} percent precision. '
              f'The model with `collection_calls` scores an AUC of {F["auc_leak"]:.2f}, but the column is recorded only after a loan goes bad, so it must be dropped. I would report the honest model, name the threshold chosen on the training loans and its cost (Session 15), '
              f'and give the cross-validated AUC ({F["cv_honest"].mean():.2f}, spread {F["cv_honest"].std(ddof=1):.2f}) with its spread.')
    else:
        nb.md('### My verdict\n\nWrite three sentences: which model you would report and with which threshold, what the leaked column was and why it must go, and what the cross-validated AUC says.')
    nb.md('**Download** `model_comparison.csv` from the Colab file panel and keep it with this notebook. Next session: forests, boosting and overfitting.')
    return nb
