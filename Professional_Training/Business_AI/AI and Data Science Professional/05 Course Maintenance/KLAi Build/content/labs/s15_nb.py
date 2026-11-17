"""Session 15 lab notebook: classification on the Nile Microfinance loans (logistic regression, decision tree, predicted probability, decision threshold and cost).
Expected values in the checks come from content/s15.py facts(), which is built on content/loans_canon.py (NumPy replicas), never typed.

NEEDS: the build sandbox has no scikit-learn, so make_notebooks.py reports UNVERIFIED (every cell compiles). ref/fx_prove_nb.py 15 runs every cell, learner and solution, against a small shim of scikit-learn
built on loans_canon. That proves the cell order and that the learner version reaches show_checks with NOT YET and no traceback. It does NOT prove what real scikit-learn prints: the shim shares the
replica code, so matching numbers are circular. Re-run the solution on real scikit-learn in Colab before the course starts.
Tolerances (a real library can move a count by a few loans): counts at 0.20 within 4 to 8 loans; coefficient of the ratio within 0.05; test AUC within 0.01; threshold from cross-validation within 0.03
(the cost curve is flat from 0.08 to 0.12); costs within UGX 6 million."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'kit'))
sys.path.insert(0, str(HERE.parent))
import nb as NB  # noqa: E402
import s15  # noqa: E402

TITLE = 'Classification'
NEEDS = ['scikit_learn_full']


def _cv_best(F, cost_alarm):
    import numpy as np
    import loans_canon as C
    ytr, oof = F['ytr'], F['oof']
    best, bc = None, None
    for t in np.round(np.arange(0.02, 0.605, 0.01), 2):
        c = C.confusion(ytr, oof >= t)
        cost = c['fn'] * 1_000_000 + c['fp'] * cost_alarm
        if bc is None or cost < bc:
            best, bc = float(t), cost
    return best


def build(solution):
    F = s15.facts()
    T = F['thr_rows'][0.2]
    p = F['p_lr']
    CT = F['cost_test']
    coef_ratio = float(F['coef']['instalment_to_income'])
    nb = NB.Notebook()

    def ans(sol, placeholder, hint):
        return sol if solution else f'{placeholder}   # your code here: {hint}'

    nb.md('# Session 15 lab: Classification, yes or no questions\n\n'
          'You will fit a **logistic regression** and a **decision tree** on the Nile Microfinance loans, read the **predicted probability** each gives, and choose a **decision threshold** from the cost of a missed default '
          'and the cost of a false alarm. All data is fictional and the costs are illustrative teaching numbers.\n\n'
          'Rhythm for every step: **PREDICT** (write your guess), **run**, **READ** the output, **CHANGE** one thing. Cells with `# your code here` hold a placeholder: replace that line with your answer and run the cells in order. '
          'The `check(...)` lines print NOT YET until your number is right. What you keep: this notebook, `loan_risk_scores.csv` and a three-line threshold note.\n\n'
          'One rule for the whole lab: the **test loans are used once**, at the end. The threshold is chosen on the training loans.')
    nb.data_setup()
    nb.check_setup()
    nb.code('import numpy as np\nimport pandas as pd\n\n'
            '# Run this cell once. It lets a check say NOT YET instead of stopping the notebook when your answer is still empty.\n'
            'def safe(f):\n    try:\n        return f()\n    except Exception:\n        return np.nan')

    # ------------------------------------------------------------------ step 1
    nb.step(1, 'Prepare the loans and one-hot encode the text', 'The same preparation as Session 14, so that every session works on the same 8,000 loans. A model needs clean numbers.')
    nb.predict('The file has 8,000 loans. Two have an impossible age (0 and 199). If we replace those ages instead of deleting the loans, how many loans remain?')
    nb.code('loans = pd.read_csv("loans.csv")\nprint(loans.shape)\n'
            'bad_age = (loans.age < 18) | (loans.age > 100)                      # two impossible ages: 0 and 199\n'
            'loans.loc[bad_age, "age"] = loans.loc[~bad_age, "age"].median()      # the median of the valid ages (36); all 8,000 loans stay\n'
            'loans["income_missing"] = loans.monthly_income_ugx.isna().astype(int)   # flag first, then fill\n'
            'median_income = ' + ans('loans.monthly_income_ugx.median()', 'np.nan', 'the median of monthly_income_ugx') + '\n'
            'loans["monthly_income_ugx"] = loans.monthly_income_ugx.fillna(median_income)\n'
            '# the instalment-to-income ratio. The 1.15 is an illustrative assumption for interest and fees, not in the data.\n'
            'loans["instalment_to_income"] = ' + ans('loans.loan_amount_ugx * 1.15 / loans.term_months / loans.monthly_income_ugx', 'np.nan', 'loan_amount_ugx * 1.15 / term_months / monthly_income_ugx') + '\n'
            'print(len(loans), "loans;", loans.income_missing.sum(), "incomes were blank")\n'
            'print(loans["instalment_to_income"].describe().round(2))')
    nb.code(f'check("loans after the preparation", len(loans), {F["rows"]}, 0)\n'
            f'check("default rate", loans["default"].mean(), {F["default_rate"]!r}, 0.001)\n'
            f'check("median income (UGX)", safe(lambda: median_income), {F["median_income"]!r}, 1)\n'
            f'check("median instalment-to-income ratio", safe(lambda: loans["instalment_to_income"].median()), {float(F["loans"].instalment_to_income.median())!r}, 0.005)')
    nb.read('The default rate is about 12.6 percent. Which class is the positive class, and why does the rarity of default matter for a model?')
    nb.md('Next, **one-hot encoding**. We keep the 12 numeric columns of Session 14 and turn the three text variables (gender, occupation, loan_purpose) into 0 and 1 columns. '
          'The district (30 values) stays out, and so does `collection_calls`: it exists only after a loan goes bad, and Session 16 explains why it must stay out.')
    nb.code('FEATURES = ["age", "monthly_income_ugx", "income_missing", "loan_amount_ugx", "term_months", "previous_loans",\n'
            '            "previous_late_payments", "group_loan", "savings_balance_ugx", "has_mobile_money", "distance_to_branch_km", "instalment_to_income"]\n'
            'X = ' + ans('pd.concat([loans[FEATURES], pd.get_dummies(loans[["gender", "occupation", "loan_purpose"]], dtype=int)], axis=1)', 'loans[FEATURES]',
                         'join the 12 FEATURES to pd.get_dummies(loans[["gender", "occupation", "loan_purpose"]], dtype=int) with pd.concat(..., axis=1)') + '\n'
            'y = loans["default"]\nprint(X.shape)')
    nb.code(f'check("columns of X after one-hot encoding", X.shape[1], {F["X_shape"][1]}, 0)\ncheck("a Teacher column exists", int("occupation_Teacher" in X.columns), 1, 0)')
    nb.change('Print `X.columns` and find the columns made from `loan_purpose`. How many are there, and why is there no column called `loan_purpose`?')

    # ------------------------------------------------------------------ step 2
    nb.step(2, 'Split the loans and fit a logistic regression', 'Hide a quarter of the loans, learn from the rest, then ask the model for a probability of default for each hidden loan. '
            'The model is a pipeline: StandardScaler puts every variable on the same scale, then LogisticRegression runs with its defaults (L2 penalty, C = 1.0: regularisation). That is why the coefficients are per 1 standard deviation.')
    nb.predict('Will the coefficient of instalment_to_income be positive or negative? A positive coefficient raises the log-odds of default.')
    nb.code('from sklearn.model_selection import train_test_split\nfrom sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.metrics import roc_auc_score\n\n'
            'X_train, X_test, y_train, y_test = ' + ans('train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)', 'X.iloc[:2000], X.iloc[2000:4000], y.iloc[:2000], y.iloc[2000:4000]',
                                                         'train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)') + '\n'
            'print(len(X_train), len(X_test), int(y_test.sum()))\n'
            'print("first test rows:", X_test.index[:10].tolist())   # with stratify=y and random_state=42 these are the rows of the course notes')
    nb.code('model = ' + ans('make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))', 'make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, C=0.000001))',
                             'make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)). The placeholder has a very strong penalty (C=0.000001)') + '\n'
            'model.fit(X_train, y_train)\n'
            'y_prob = ' + ans('model.predict_proba(X_test)[:, 1]', 'np.full(len(X_test), 0.5)', 'column 1 of model.predict_proba(X_test) is the probability of default') + '\n'
            'coef = pd.Series(model[-1].coef_[0], index=X.columns).sort_values()   # per 1 standard deviation of each variable\nprint(coef.round(2))\n'
            'auc = safe(lambda: roc_auc_score(y_test, y_prob))\nprint("average predicted probability:", round(float(y_prob.mean()), 3), " test AUC:", auc)')
    nb.code(f'check("loans in X_train", len(X_train), {F["n_train"]}, 0)\ncheck("defaults in y_test", int(y_test.sum()), {F["test_pos"]}, 0)\n'
            f'check("average predicted probability", safe(lambda: y_prob.mean()), {float(p.mean())!r}, 0.01)\n'
            f'check("coefficient of instalment_to_income", safe(lambda: coef["instalment_to_income"]), {coef_ratio!r}, 0.05)\n'
            f'check("test AUC", auc, {F["auc_lr"]!r}, 0.01)')
    nb.read('Which three variables push the log-odds of default up most, and which push it down most? Does that match the bar charts in the slides? Why are the two gender coefficients about 0?')
    nb.change('Compute the odds ratio of the ratio with `np.exp(coef["instalment_to_income"])`. In words: how many times larger are the odds of default for each extra standard deviation of the ratio?')

    # ------------------------------------------------------------------ step 3
    nb.step(3, 'Fit a decision tree and read its rules', 'A tree asks yes or no questions. You can read every path.')
    nb.predict('Which variable will the root node use for the first split?')
    nb.code('from sklearn.tree import DecisionTreeClassifier, export_text\n\n'
            'tree = ' + ans('DecisionTreeClassifier(max_depth=3, random_state=42)', 'DecisionTreeClassifier(max_depth=1, random_state=42)', 'DecisionTreeClassifier(max_depth=3, random_state=42)') + '\n'
            'tree.fit(X_train, y_train)\nprint(export_text(tree, feature_names=list(X.columns)))\n'
            'tree_prob = ' + ans('tree.predict_proba(X_test)[:, 1]', 'np.full(len(X_test), 0.5)', 'the probability of default, column 1 of tree.predict_proba(X_test)') + '\n'
            'print("different probabilities the tree gives:", len(set(tree_prob.round(6))))')
    nb.code(f'check("tree depth", tree.get_depth(), 3, 0)\ncheck("leaf nodes", tree.get_n_leaves(), {len(F["t3_leaves"])}, 0)\ncheck("different probabilities", len(set(tree_prob.round(6))), {len(F["t3_leaves"])}, 0)\n'
            f'check("average tree probability", safe(lambda: tree_prob.mean()), {float(F["p_tree"].mean())!r}, 0.01)')
    nb.read('Pick one path from the root to a leaf and say it as a sentence: "If the instalment-to-income ratio is ..., and ..., the model says ... percent of such loans default."')
    nb.change('Refit with max_depth=2. Store the number of leaf nodes in `leaves_depth2`.')
    nb.code('tree2 = DecisionTreeClassifier(max_depth=2, random_state=42)\ntree2.fit(X_train, y_train)\n'
            'leaves_depth2 = ' + ans('tree2.get_n_leaves()', 'np.nan', 'the number of leaf nodes of tree2 (tree2.get_n_leaves())') + '\n'
            'print(leaves_depth2)\ncheck("leaves at depth 2", safe(lambda: leaves_depth2), 4, 0)')

    # ------------------------------------------------------------------ step 4
    nb.step(4, 'Choose the decision threshold from the cost, on the training loans', 'A missed default costs the lender far more than a false alarm. Put illustrative costs on both. '
            'Choose the threshold WITHOUT the test loans: use cross-validated probabilities on the training loans, and compare with the cost rule. Then report the cost on the test loans once.')
    nb.predict('Count the test loans flagged at a decision threshold of 0.20. Will the model flag more or fewer than 100 loans? How many of the 251 defaults will it catch?')
    nb.code('flag = y_prob >= 0.20\nactual = (y_test == 1).to_numpy()\n'
            'tp = ' + ans('int((flag & actual).sum())    # flagged and really defaulted: true positives', 'np.nan', 'loans flagged AND really defaulted (flag & actual)') + '\n'
            'fp = ' + ans('int((flag & ~actual).sum())   # flagged but repaid: false positives (false alarms)', 'np.nan', 'loans flagged but repaid (flag & ~actual)') + '\n'
            'fn = ' + ans('int((~flag & actual).sum())   # not flagged but defaulted: false negatives (missed)', 'np.nan', 'loans not flagged but defaulted (~flag & actual)') + '\n'
            'print("flagged:", int(flag.sum()), " caught:", tp, " false alarms:", fp, " missed:", fn)')
    nb.code(f'check("defaults caught at 0.20", safe(lambda: tp), {T["tp"]}, 4)\ncheck("false alarms at 0.20", safe(lambda: fp), {T["fp"]}, 8)\ncheck("defaults missed at 0.20", safe(lambda: fn), {T["fn"]}, 4)')
    nb.md('This table only describes what happens on the test loans. It does not choose the threshold. Now price the mistakes. These costs are **illustrative**: a missed default loses UGX 1,000,000 of principal and a false alarm loses UGX 100,000 of interest.\n\n'
          'Step A: get an honest probability for every TRAINING loan with **cross-validation** (`cross_val_predict`: five rounds, each loan scored by a model that did not see it).')
    nb.code('from sklearn.model_selection import cross_val_predict\n\n'
            'p_cv = ' + ans('cross_val_predict(model, X_train, y_train, cv=5, method="predict_proba")[:, 1]', 'np.full(len(y_train), 0.5)', 'cross_val_predict(model, X_train, y_train, cv=5, method="predict_proba")[:, 1]') + '\n'
            'actual_train = (y_train == 1).to_numpy()\n'
            'print("training loans:", len(p_cv), " average out-of-fold probability:", round(float(p_cv.mean()), 3))')
    nb.code(f'check("out-of-fold probabilities for every training loan", len(p_cv), {F["n_train"]}, 0)\ncheck("average out-of-fold probability", safe(lambda: p_cv.mean()), {float(F["oof"].mean())!r}, 0.01)')
    nb.md('Step B: the cost of the mistakes at every threshold on the training loans (scaled to 2,000 loans so that it compares with the test loans).')
    nb.code('def total_cost(prob, actual, threshold, cost_miss, cost_alarm):\n    flagged = prob >= threshold\n'
            '    missed = ' + ans('int((~flagged & actual).sum())', '0', 'defaults not flagged: int((~flagged & actual).sum())') + '\n'
            '    alarms = ' + ans('int((flagged & ~actual).sum())', '0', 'repaid loans flagged: int((flagged & ~actual).sum())') + '\n'
            '    return missed * cost_miss + alarms * cost_alarm\n\n'
            'thresholds = np.round(np.arange(0.02, 0.605, 0.01), 2)\nscale = len(y_test) / len(y_train)\n'
            'costs_cv = [total_cost(p_cv, actual_train, t, 1_000_000, 100_000) * scale for t in thresholds]\n'
            'cv_threshold = ' + ans('float(thresholds[int(np.argmin(costs_cv))])', 'np.nan', 'the threshold with the smallest cost (np.argmin)') + '\n'
            'rule = 100_000 / (100_000 + 1_000_000)\n'
            'print("cheapest threshold on the training loans:", cv_threshold, " cost per 2,000 loans:", round(min(costs_cv) / 1e6, 1), "million")\n'
            'print("cost rule: 100,000 / (100,000 + 1,000,000) =", round(rule, 4))')
    nb.code(f'check("threshold from cross-validation", safe(lambda: cv_threshold), {F["cv_t"]!r}, 0.03)\n'
            f'check("training cost at that threshold (UGX million per 2,000 loans)", safe(lambda: min(costs_cv) / 1e6), {F["cost_cv_curve_at_cv_t"] / 1e6!r}, 4)\n'
            f'check("cost rule", rule, {F["rule_thr"]!r}, 0.001)')
    nb.read('Run the next cell. Where is the curve lowest? How far is that from the default threshold of 0.50, and from the cost rule?')
    nb.code('import matplotlib.pyplot as plt\n\nplt.plot(thresholds, np.array(costs_cv) / 1e6)\nplt.axvline(rule, linestyle=":", label="cost rule")\n'
            'plt.axvline(0 if np.isnan(cv_threshold) else cv_threshold, linestyle="--", label="cross-validation")\n'
            'plt.xlabel("decision threshold")\nplt.ylabel("cost per 2,000 loans, UGX million")\nplt.title("Cost of mistakes on the training loans (illustrative costs)")\nplt.legend()\nplt.show()')
    nb.md('Step C: only now use the test loans, **once**, to report the cost of the choices you made.')
    nb.code('cost_default = total_cost(y_prob, actual, 0.50, 1_000_000, 100_000) / 1e6\n'
            'cost_cv_choice = total_cost(y_prob, actual, cv_threshold, 1_000_000, 100_000) / 1e6\n'
            'cost_rule_choice = total_cost(y_prob, actual, rule, 1_000_000, 100_000) / 1e6\n'
            'print("test cost, UGX million. At 0.50:", round(cost_default, 1), " at the cross-validated threshold:", round(cost_cv_choice, 1), " at the rule:", round(cost_rule_choice, 1))')
    nb.code(f'check("test cost at 0.50 (UGX million)", safe(lambda: cost_default), {CT[0.5] / 1e6!r}, 6)\n'
            f'check("test cost at the cross-validated threshold (UGX million)", safe(lambda: cost_cv_choice), {F["cv_row"]["cost"] / 1e6!r}, 6)\n'
            f'check("test cost at the cost rule (UGX million)", safe(lambda: cost_rule_choice), {F["rule_row"]["cost"] / 1e6!r}, 6)')
    nb.change('Make a false alarm cost 500,000 instead of 100,000 and store the new cheapest threshold on the training loans in `cv_threshold_500k`. Predict first: higher or lower than before? What does the rule give?')
    nb.code('costs_500k = [total_cost(p_cv, actual_train, t, 1_000_000, 500_000) * scale for t in thresholds]\n'
            'cv_threshold_500k = ' + ans('float(thresholds[int(np.argmin(costs_500k))])', 'np.nan', 'the threshold with the smallest cost in costs_500k') + '\n'
            'print(cv_threshold_500k, " rule:", round(500_000 / 1_500_000, 3))\n'
            f'check("cheapest threshold when a false alarm costs 500,000", safe(lambda: cv_threshold_500k), {_cv_best(F, 500_000)!r}, 0.05)')

    # ------------------------------------------------------------------ step 5
    nb.step(5, 'Keep: a scored file and a threshold note', 'This is what you can hand to a colleague in credit.')
    nb.code('chosen = round(cv_threshold, 2)\n'
            'scores = ' + ans('pd.DataFrame({"loan_id": loans.loc[X_test.index, "loan_id"].to_numpy(),\n                       "probability": y_prob.round(4),\n                       "flag": (y_prob >= chosen).astype(int)})',
                              'pd.DataFrame({"loan_id": [], "probability": [], "flag": []})',
                              'a DataFrame with columns loan_id, probability and flag (1 when probability >= chosen). Use loans.loc[X_test.index, "loan_id"]') + '\n'
            'scores.to_csv("loan_risk_scores.csv", index=False)\nprint(scores.head())\nprint("loans flagged:", int(scores["flag"].sum()), "of", len(scores))\n'
            f'import os\ncheck("rows in loan_risk_scores.csv", len(scores), {F["n_test"]}, 0)\ncheck("file written", int(os.path.exists("loan_risk_scores.csv")), 1, 0)\n'
            f'check("loans flagged at the chosen threshold", int(scores["flag"].sum()), {F["cv_row"]["flagged"]}, 60)')
    nb.code('show_checks()')
    if solution:
        nb.md(f'### My threshold note (example)\n\n1. **Threshold:** flag a loan when its predicted probability is at least {F["cv_t"]:.2f}. It was chosen by 5-fold cross-validation on the training loans. The cost rule (0.0909) agrees.\n'
              f'2. **Cost:** on the {F["n_test"]:,} test loans, used once, this costs about UGX {F["cv_row"]["cost"] / 1e6:.0f} million with the illustrative costs, against UGX {CT[0.5] / 1e6:.0f} million at the default 0.50.\n'
              '3. **Caution:** the costs are teaching numbers. The lender must replace them with its own, and many flagged loans are good borrowers, so a flag should start a conversation.')
    else:
        nb.md('### My threshold note\n\nWrite three lines.\n\n1. **Threshold:** flag a loan when its predicted probability is at least ... (chosen on the training loans by ...)\n2. **Cost:** on the 2,000 test loans this costs about UGX ... million, against UGX ... million at 0.50.\n3. **Caution:** ...')
    nb.md('**Download** `loan_risk_scores.csv` from the Colab file panel and keep it with this notebook. Next session: how do we tell a model that works from one that only looks good?')
    return nb
