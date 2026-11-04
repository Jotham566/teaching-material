"""Session 17 lab: forests, boosting and overfitting on the Nile Microfinance loans (author i).

Expected values come from content/s17_facts.py (NumPy implementations written from the textbook definitions: scikit-learn is not installed in the build sandbox).
Logistic regression, one decision tree and gradient boosting should agree with scikit-learn closely. A random forest and the grid search use random numbers, so those checks allow a range.
NEEDS lists the libraries the sandbox lacks: the runner then proves only that every cell compiles and prints UNVERIFIED."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parents[1] / 'kit'))
import nb as NB  # noqa: E402
import s17_facts as SF  # noqa: E402

TITLE = 'Forests, boosting and overfitting'
NEEDS = ['sklearn']


def build(solution: bool):
    F = SF.facts()
    L = F['lr']
    tr = {r['depth']: r for r in F['tree_rows']}
    gb = F['grid_best']
    tu = F['tuned']
    f100 = F['forest100']
    b100 = F['boost100']
    pf = {r['col']: r for r in F['perm_forest']}
    cols = SF.COLS
    coef_ratio = L['w'][cols.index('instalment_to_income')]
    C = F['canon']
    nb = NB.Notebook()

    def cell(sol, learner):
        nb.code(sol if solution else learner)

    def G(code):
        """A cell that only runs and prints what the learner built. In the learner version it is wrapped so that it prints a friendly line, not an error, while an answer above is still None."""
        if solution:
            nb.code(code)
        else:
            body = '\n'.join('    ' + l for l in code.split('\n'))
            nb.code('try:\n' + body + '\nexcept Exception as err:\n    print("Not yet: an answer above is still None or incomplete (" + type(err).__name__ + ").")')

    nb.md('# Session 17 lab: forests, boosting and overfitting\n\nYou will compare four models on the Nile Microfinance loans, watch overfitting happen, tune a forest with cross-validation, and decide which model to ship.\n\n'
          'Rhythm for every step: **PREDICT** first, **run** the cell, **READ** the output, then **CHANGE** one thing. Cells that say `None  # your code here` are yours to fill in. After each answer a `check` line tells you whether your number is right. '
          'The slides gave the ideas, so use them. Forests use random numbers, so a few checks accept a range.')
    nb.data_setup()
    nb.check_setup()
    nb.code('# A helper so that a check never crashes while your answer is still None. You do not need to read it.\nimport numpy as np\nimport pandas as pd\n\n'
            'def safe(f):\n    try:\n        return float(f())\n    except Exception:\n        return float("nan")')

    # ------------------------------------------------------------------ 1 prepare
    nb.step(1, 'Prepare the loans and split them', 'The same preparation as Sessions 14 to 16. The two impossible ages (0 and 199) become the median age, so all 8,000 loans stay. Blank incomes get a flag and the median income. '
            'We add instalment_to_income (the instalment-to-income ratio) and leave out `collection_calls` because it leaks the answer (Session 16). '
            'The median income is computed on all 8,000 loans before the split, on purpose: it is simple and the leak is tiny. Session 20 shows the leak-free way.')
    nb.predict('How many of the 8,000 loans do you expect to keep? (Hint: the data dictionary mentions two impossible ages. We replace them, we do not delete the rows.)')
    nb.code('loans = pd.read_csv("loans.csv")\n'
            'bad_age = (loans["age"] < 18) | (loans["age"] > 100)   # two impossible ages: 0 and 199\n'
            'loans.loc[bad_age, "age"] = loans.loc[~bad_age, "age"].median()   # the median of the valid ages (36) keeps all 8,000 rows\n'
            'loans["income_missing"] = loans["monthly_income_ugx"].isna().astype(int)   # a flag: 1 when the income was blank\n'
            'loans["monthly_income_ugx"] = loans["monthly_income_ugx"].fillna(loans["monthly_income_ugx"].median())   # median imputation (642,600)\n'
            '# instalment_to_income: loan x 1.15 / term / monthly income. The 1.15 (loan plus 15 percent interest and fees) is an ILLUSTRATIVE assumption: it is not in the data.\n'
            'loans["instalment_to_income"] = loans["loan_amount_ugx"] * 1.15 / loans["term_months"] / loans["monthly_income_ugx"]\nprint(len(loans), "loans kept")')
    cell('features = ["age", "monthly_income_ugx", "income_missing", "loan_amount_ugx", "term_months", "previous_loans", "previous_late_payments",\n            "group_loan", "savings_balance_ugx", "has_mobile_money", "distance_to_branch_km", "instalment_to_income"]\n'
         'X = loans[features]\ny = loans["default"]',
         'features = None   # your code here: a list of the 12 column names (the ten honest number columns, income_missing and instalment_to_income). Leave out collection_calls and default\n'
         'X = None   # your code here: the 12 columns of loans\ny = None   # your code here: the default column')
    G('print(X.shape, round(y.mean(), 4))')
    cell('from sklearn.model_selection import train_test_split\n\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)',
         'from sklearn.model_selection import train_test_split\n\nX_train, X_test, y_train, y_test = None, None, None, None   # your code here: train_test_split with test_size=0.25, stratify=y and random_state=42')
    G('print(len(X_train), len(X_test), "defaults in the test rows:", y_test.sum())\nprint(X_test.index[:10].tolist())   # the same rows as every Session 14 to 17 notebook')
    nb.code(f'check("loans kept", safe(lambda: len(loans)), {F["rows"]}, 0)\ncheck("12 variables", safe(lambda: X.shape[1]), 12, 0)\ncheck("default share", safe(lambda: y.mean()), {F["default_rate"]:.4f}, 0.001)\n'
            f'check("training rows", safe(lambda: len(X_train)), {F["n_train"]}, 0)\ncheck("defaults in the test rows", safe(lambda: y_test.sum()), {C["test_defaults"]}, 0)\n'
            f'check("same test rows as the course (sum of the row numbers)", safe(lambda: sum(X_test.index)), {C["test_index_sum"]}, 0)')
    nb.read(f'The default share is 12.55 percent. If a model said "no default" for every loan, what accuracy would it get on the test rows ({C["baseline_correct"]:,} of 2,000 = {C["baseline_accuracy"]})? Why is accuracy a poor score here (Session 15)?')
    nb.change(f'Remove `stratify=y` from train_test_split and run Steps 1 and 2 again. How many defaults are in the test rows now (about {C["unstratified_test_defaults"]})? Which later numbers move, and by how much?')

    # ------------------------------------------------------------------ 2 baseline
    nb.step(2, 'A simple baseline: scaled logistic regression', 'Scale the variables so their coefficients are comparable (standardisation), then fit a logistic regression. The default C = 1.0 (L2 penalty) shrinks the coefficients, so they depend on the scaling. We score it on the training rows and on the test rows with AUC.')
    nb.predict('Will the AUC be higher on the training rows or on the test rows? About how big will the gap be for a model this simple?')
    cell('from sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.metrics import roc_auc_score\n\n'
         'logistic_model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))\nlogistic_model.fit(X_train, y_train)\n'
         'auc_lr_train = roc_auc_score(y_train, logistic_model.predict_proba(X_train)[:, 1])\nauc_lr_test = roc_auc_score(y_test, logistic_model.predict_proba(X_test)[:, 1])',
         'from sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.metrics import roc_auc_score\n\n'
         'logistic_model = None   # your code here: make_pipeline of StandardScaler() and LogisticRegression(max_iter=1000), then fit on the training rows\n'
         'auc_lr_train = None   # your code here: roc_auc_score of y_train and the predicted chance of default (predict_proba, column 1)\nauc_lr_test = None   # your code here: the same on the test rows')
    G('print(round(auc_lr_train, 3), round(auc_lr_test, 3))')
    cell('coefficients = pd.Series(logistic_model.named_steps["logisticregression"].coef_[0], index=features).sort_values(ascending=False)',
         'coefficients = None   # your code here: a Series of the 12 coefficients (logistic_model.named_steps["logisticregression"].coef_[0]) with the feature names as the index, largest first')
    G('print(coefficients.round(3))')
    nb.code(f'check("logistic AUC, training rows", safe(lambda: auc_lr_train), {L["train"]:.4f}, 0.005)\ncheck("logistic AUC, test rows", safe(lambda: auc_lr_test), {L["test"]:.4f}, 0.005)\n'
            f'check("instalment_to_income coefficient", safe(lambda: coefficients["instalment_to_income"]), {coef_ratio:.4f}, 0.03)')
    nb.read('Which variable has the largest coefficient, and does a positive sign raise or lower the risk of default? Say it in one sentence, as to a credit committee.')
    nb.change('Change C in LogisticRegression to 0.01 (a stronger penalty). What happens to the coefficients and to the test AUC?')

    # ------------------------------------------------------------------ 3 trees
    nb.step(3, 'Watch a decision tree overfit', 'max_depth is the most yes or no questions a loan can be asked. We grow trees of eight depths and score each one on the training rows and on the test rows.')
    nb.predict('What training AUC will a tree with no depth limit get? And what will its test AUC be: close to 0.75, or much lower?')
    cell('from sklearn.tree import DecisionTreeClassifier\n\ndepths = [1, 2, 3, 4, 6, 8, 12, None]\ntree_train = []\ntree_test = []\nfor d in depths:\n    tree_model = DecisionTreeClassifier(max_depth=d, random_state=42)\n    tree_model.fit(X_train, y_train)\n'
         '    tree_train.append(roc_auc_score(y_train, tree_model.predict_proba(X_train)[:, 1]))\n    tree_test.append(roc_auc_score(y_test, tree_model.predict_proba(X_test)[:, 1]))',
         'from sklearn.tree import DecisionTreeClassifier\n\ndepths = [1, 2, 3, 4, 6, 8, 12, None]\ntree_train = []\ntree_test = []\nfor d in depths:\n    tree_model = None   # your code here: a DecisionTreeClassifier with max_depth=d and random_state=42, fitted on the training rows\n'
         '    tree_train.append(None)   # your code here: AUC on the training rows\n    tree_test.append(None)   # your code here: AUC on the test rows')
    G('tree_results = pd.DataFrame({"max_depth": [str(d) for d in depths], "train_auc": tree_train, "test_auc": tree_test}).round(3)\nprint(tree_results)')
    cell('best_depth = depths[int(np.argmax(tree_test))]',
         'best_depth = None   # your code here: the max_depth with the highest test AUC (np.argmax of tree_test)')
    G('print("depth with the best test AUC:", best_depth)\n\nimport matplotlib.pyplot as plt\nplt.plot(range(len(depths)), tree_train, marker="o", label="training")\nplt.plot(range(len(depths)), tree_test, marker="o", label="test")\n'
      'plt.xticks(range(len(depths)), [str(d) for d in depths])\nplt.xlabel("max_depth")\nplt.ylabel("AUC")\nplt.legend()\nplt.show()')
    nb.code(f'check("depth 3 test AUC", safe(lambda: tree_test[2]), {tr[3]["test"]:.4f}, 0.03)\ncheck("no limit: training AUC", safe(lambda: tree_train[-1]), 1.0, 0.002)\ncheck("no limit: test AUC (a range)", safe(lambda: tree_test[-1]), {tr[None]["test"]:.4f}, 0.05)\n'
            f'check("best depth is small (2 to 4)", safe(lambda: best_depth in [2, 3, 4]), 1, 0)')
    nb.read('Where does the gap between the two lines start to open? Name that gap. What is the tree doing to the training loans when the training AUC reaches 1.0?')
    nb.change('Change the scoring from AUC to accuracy (use tree_model.predict and accuracy_score). Does the overfitting still show?')

    # ------------------------------------------------------------------ 4 ensembles
    nb.step(4, 'Two ensembles: a random forest and gradient boosting', 'A random forest averages many deep trees grown on bootstrap samples. Gradient boosting adds shallow trees one at a time, each fitting the residual errors so far.')
    nb.predict('Will the forest\'s training AUC be near 0.75, near 0.85 or near 1.0? Will its test AUC beat the logistic regression?')
    cell('from sklearn.ensemble import RandomForestClassifier\n\nforest = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)\nforest.fit(X_train, y_train)\n'
         'auc_f_train = roc_auc_score(y_train, forest.predict_proba(X_train)[:, 1])\nauc_f_test = roc_auc_score(y_test, forest.predict_proba(X_test)[:, 1])',
         'from sklearn.ensemble import RandomForestClassifier\n\nforest = None   # your code here: a RandomForestClassifier with n_estimators=100, random_state=42, n_jobs=-1, fitted on the training rows\n'
         'auc_f_train = None   # your code here: AUC on the training rows\nauc_f_test = None   # your code here: AUC on the test rows')
    G('print(round(auc_f_train, 3), round(auc_f_test, 3), "gap", round(auc_f_train - auc_f_test, 3))')
    nb.predict('For gradient boosting with learning rate 0.1 and trees of depth 3: will the test AUC keep rising as you add trees up to 500? Sketch the two curves before you run the cell.')
    cell('from sklearn.ensemble import GradientBoostingClassifier\n\nboosting_model = GradientBoostingClassifier(n_estimators=500, learning_rate=0.1, max_depth=3, random_state=42)\nboosting_model.fit(X_train, y_train)\n'
         '# staged_predict_proba gives the predicted chances after 1 tree, 2 trees, ... 500 trees\nboost_train = [roc_auc_score(y_train, p[:, 1]) for p in boosting_model.staged_predict_proba(X_train)]\n'
         'boost_test = [roc_auc_score(y_test, p[:, 1]) for p in boosting_model.staged_predict_proba(X_test)]\nbest_n = int(np.argmax(boost_test)) + 1',
         'from sklearn.ensemble import GradientBoostingClassifier\n\nboosting_model = None   # your code here: GradientBoostingClassifier(n_estimators=500, learning_rate=0.1, max_depth=3, random_state=42), fitted on the training rows\n'
         '# staged_predict_proba gives the predicted chances after 1 tree, 2 trees, ... 500 trees\nboost_train = [None] * 500   # your code here: a list of AUC values on the training rows, one per stage (loop over boosting_model.staged_predict_proba(X_train))\n'
         'boost_test = [None] * 500   # your code here: the same on the test rows\nbest_n = None   # your code here: the number of trees (1 to 500) with the highest test AUC')
    G('print("100 trees:", round(boost_train[99], 3), round(boost_test[99], 3))\nprint("best number of trees:", best_n, round(max(boost_test), 3), "(picked from the test curve: for illustration only)")\n\n'
      'plt.plot(range(1, 501), boost_train, label="training")\nplt.plot(range(1, 501), boost_test, label="test")\nplt.xlabel("number of trees")\nplt.ylabel("AUC")\nplt.legend()\nplt.show()')
    nb.code(f'check("forest training AUC", safe(lambda: auc_f_train), 1.0, 0.01)\ncheck("forest test AUC (a range)", safe(lambda: auc_f_test), {f100["test"]:.4f}, 0.03)\ncheck("forest gap above 0.2", safe(lambda: auc_f_train - auc_f_test > 0.2), 1, 0)\n'
            f'check("boosting, 100 trees: training AUC", safe(lambda: boost_train[99]), {b100["train"]:.4f}, 0.015)\ncheck("boosting, 100 trees: test AUC", safe(lambda: boost_test[99]), {b100["test"]:.4f}, 0.015)\n'
            f'check("boosting: best test AUC", safe(lambda: max(boost_test)), {F["boost_stage_best"]:.4f}, 0.015)\ncheck("boosting peaks before 250 trees", safe(lambda: best_n < 250), 1, 0)')
    nb.read('How big is the forest\'s generalisation gap? Does the forest beat the logistic regression on the test rows? In boosting, what happens to the training and test curves after the peak?')
    nb.change('Re-fit the forest with max_features=None (plain bagging). Does the test AUC go up or down? Why might that be?')

    # ------------------------------------------------------------------ 5 tuning
    nb.step(5, 'Tune the forest with cross-validation, then ask what it relies on', 'GridSearchCV tries every combination of settings with 5-fold cross-validation on the training rows (1,200 loans in each fold). The test rows stay untouched until the end.')
    nb.predict('The grid has 3 values of max_depth and 3 of min_samples_leaf. How many model fits will GridSearchCV run with 5 folds? Will the best cross-validated AUC be higher than the default forest\'s cross-validated AUC of about 0.72?')
    cell('from sklearn.model_selection import GridSearchCV\n\nparam_grid = {"max_depth": [3, 6, None], "min_samples_leaf": [1, 10, 30]}\n'
         'search = GridSearchCV(RandomForestClassifier(n_estimators=100, random_state=42), param_grid, cv=5, scoring="roc_auc", n_jobs=-1)\nsearch.fit(X_train, y_train)   # this takes a few minutes: run it once\n'
         'tuned_forest = search.best_estimator_   # already refitted on all the training rows\nauc_t_train = roc_auc_score(y_train, tuned_forest.predict_proba(X_train)[:, 1])\n'
         'auc_t_test = roc_auc_score(y_test, tuned_forest.predict_proba(X_test)[:, 1])',
         'from sklearn.model_selection import GridSearchCV\n\nparam_grid = {"max_depth": [3, 6, None], "min_samples_leaf": [1, 10, 30]}\n'
         'search = None   # your code here: GridSearchCV of RandomForestClassifier(n_estimators=100, random_state=42) with param_grid, cv=5, scoring="roc_auc", n_jobs=-1; then fit on the training rows (a few minutes: run it once)\n'
         'tuned_forest = None   # your code here: the best model, search.best_estimator_\nauc_t_train = None   # your code here: its AUC on the training rows\nauc_t_test = None   # your code here: its AUC on the test rows')
    G('print("best settings:", search.best_params_)\nprint("best mean cross-validated AUC (the best of nine cells, so a little optimistic):", round(search.best_score_, 3))\nprint("tuned forest: training", round(auc_t_train, 3), "test", round(auc_t_test, 3))\n'
      'print("Several cells score within 0.005 of the best. The best value is at the edge of the grid (min_samples_leaf 30), so a real project would also try 50 and 100.")')
    nb.code(f'check("best cross-validated AUC (a range)", safe(lambda: search.best_score_), {gb["mean"]:.4f}, 0.02)\ncheck("tuned forest test AUC (a range)", safe(lambda: auc_t_test), {tu["test"]:.4f}, 0.03)\n'
            f'check("tuned forest gap is smaller than the default forest gap", safe(lambda: (auc_t_train - auc_t_test) < (auc_f_train - auc_f_test)), 1, 0)')
    nb.predict('Permutation importance shuffles one variable at a time on the test rows. Which variable do you expect to lose the most AUC? Which will lose about nothing?')
    cell('from sklearn.inspection import permutation_importance\n\nimp = permutation_importance(tuned_forest, X_test, y_test, scoring="roc_auc", n_repeats=10, random_state=42)\n'
         'importance = pd.Series(imp.importances_mean, index=features).sort_values(ascending=False)\ntop5 = importance.head(5)',
         'from sklearn.inspection import permutation_importance\n\nimp = None   # your code here: permutation_importance of tuned_forest on the test rows, scoring="roc_auc", n_repeats=10, random_state=42\n'
         'importance = None   # your code here: a Series of imp.importances_mean with the feature names as the index, largest first')
    G('print(importance.round(3))')
    nb.code(f'check("most important variable is instalment_to_income", safe(lambda: importance.index[0] == "instalment_to_income"), 1, 0)\ncheck("instalment_to_income: drop in AUC (a range)", safe(lambda: importance.iloc[0]), {pf["instalment_to_income"]["mean"]:.4f}, 0.03)')
    nb.read('Which variables does the tuned forest rely on? Is the order the same as the order of the logistic coefficients in Step 2? State one thing permutation importance cannot tell you.')
    nb.change('Add a copy of instalment_to_income to X_train and X_test (X_train["ratio_copy"] = X_train["instalment_to_income"]), refit the tuned forest, and run permutation importance again. What happens to the importance of instalment_to_income?')

    # ------------------------------------------------------------------ 6 results
    nb.step(6, 'Build the comparison table and decide', 'Four models, three scores each: training AUC, 5-fold cross-validated AUC on the training rows, and test AUC. Then the decision. The test rows are scored once.')
    nb.predict('Which model will have the highest test AUC? Which will have the largest gap between training and test?')
    cell('from sklearn.model_selection import cross_val_score\n\ncv_lr = cross_val_score(logistic_model, X_train, y_train, cv=5, scoring="roc_auc")\n'
         'cv_tree = cross_val_score(DecisionTreeClassifier(max_depth=3, random_state=42), X_train, y_train, cv=5, scoring="roc_auc")\n'
         'cv_boost = cross_val_score(GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42), X_train, y_train, cv=5, scoring="roc_auc")\n\n'
         'results = pd.DataFrame({\n    "model": ["Logistic regression", "Decision tree, depth 3", "Tuned random forest", "Gradient boosting, 100 trees"],\n'
         '    "train_auc": [auc_lr_train, tree_train[2], auc_t_train, boost_train[99]],\n    "cv_auc": [cv_lr.mean(), cv_tree.mean(), search.best_score_, cv_boost.mean()],\n'
         '    "test_auc": [auc_lr_test, tree_test[2], auc_t_test, boost_test[99]]})\nresults["gap"] = results["train_auc"] - results["test_auc"]\nresults = results.round(3)\n'
         'results.to_csv("model_comparison.csv", index=False)   # your keepsake, saved in your Colab folder (the Files panel on the left)',
         'from sklearn.model_selection import cross_val_score\n\ncv_lr = None   # your code here: cross_val_score of logistic_model on the training rows, cv=5, scoring="roc_auc"\ncv_tree = None   # your code here: the same for DecisionTreeClassifier(max_depth=3, random_state=42)\n'
         'cv_boost = None   # your code here: the same for GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)\n\n'
         'results = None   # your code here: a DataFrame with the columns model, train_auc, cv_auc, test_auc for the four models (logistic regression, tree depth 3, tuned forest, boosting with 100 trees; boost_train[99] and boost_test[99]), plus gap = train_auc - test_auc, rounded to 3 places. Then results.to_csv("model_comparison.csv", index=False)')
    G('print(results)')
    nb.code(f'check("cross-validated AUC, logistic", safe(lambda: cv_lr.mean()), {F["cv_lr"]["mean"]:.4f}, 0.01)\ncheck("cross-validated AUC, tree depth 3", safe(lambda: cv_tree.mean()), {F["cv_tree3"]["mean"]:.4f}, 0.03)\n'
            f'check("cross-validated AUC, boosting", safe(lambda: cv_boost.mean()), {F["cv_boost"]["mean"]:.4f}, 0.015)\ncheck("four models in the table", safe(lambda: len(results)), 4, 0)\n'
            f'check("simplest good model: logistic test AUC is within 0.03 of the best", safe(lambda: results["test_auc"].max() - results.loc[0, "test_auc"] < 0.03), 1, 0)')
    nb.code('show_checks()   # run this to see how many checks pass')
    nb.read('Look at the cv_auc and test_auc columns. Are the differences between the best three models bigger or smaller than the standard deviation between folds (about 0.01 for these models)?')
    nb.md('## Your decision memo\n\nDouble click this cell and write three sentences. (1) Which model would you ship to a credit committee? (2) Which two numbers from `results` support the choice? (3) What would change your mind?\n\n> Memo: \n\nSave the notebook and keep `model_comparison.csv` (it is in your Colab folder: download it from the Files panel). That table and the memo are what you take away from today.')
    return nb
