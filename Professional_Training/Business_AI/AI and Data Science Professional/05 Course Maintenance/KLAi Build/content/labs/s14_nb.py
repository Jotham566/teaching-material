"""Session 14 lab notebook: the machine learning workflow on the Nile Microfinance loans. Expected values come from content/s14_facts.py, which is built on content/loans_canon.py.

NEEDS: no scikit-learn in the build sandbox, so make_notebooks.py proves only that every cell compiles (UNVERIFIED). ref/fx_prove_nb.py runs the cell flow of the learner and the solution
notebooks against a small shim of scikit-learn that is built on loans_canon; that proves the cells run in order and the learner version reports NOT YET without a traceback. It does not prove
what real scikit-learn prints. Every expected number is a NumPy replica number: re-run on real scikit-learn in Colab before the course starts.
Tolerances: counts and the split are exact (rows are fixed by random_state=42); the tree numbers accept the range seen over ten other splits, because a real library may break a tie differently.
"""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'kit'))
import nb as NB  # noqa: E402

_s = importlib.util.spec_from_file_location('s14_facts', HERE.parent / 's14_facts.py')
FX = importlib.util.module_from_spec(_s)
_s.loader.exec_module(FX)

TITLE = 'Machine learning: the workflow'
NEEDS = ['sklearn_DummyClassifier_and_stratified_split']


def r(v, k=4):
    return repr(round(float(v), k))


def build(solution):
    F = FX.facts()
    q = F['q_rates']
    nb = NB.Notebook()

    def ans(sol, placeholder, hint):
        """Solution: the model answer. Learner: a harmless placeholder that lets every later cell run, plus a one-line hint."""
        return sol if solution else f'{placeholder}   # your code here: {hint}'

    nb.md('# Session 14 lab: the machine learning workflow\n\n'
          'You will prepare the Nile Microfinance loans (fictional data), split them into a training set and a test set, fit a baseline model and a first model, and read what accuracy hides.\n\n'
          'In every step: **PREDICT**, run, **READ**, **CHANGE** one thing. Cells with `# your code here` hold a placeholder: replace that line with your answer. Run the cells in order. '
          'Before you answer, a `check(...)` line prints NOT YET. It prints OK when your number matches. Run the last cell to count the checks.')
    nb.data_setup()
    nb.check_setup()
    nb.code('import numpy as np\nimport pandas as pd\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.dummy import DummyClassifier\n'
            'from sklearn.tree import DecisionTreeClassifier\nfrom sklearn.metrics import accuracy_score, recall_score, precision_score, confusion_matrix\n\n'
            '# Run this cell once. It lets a check say NOT YET instead of stopping the notebook when your answer is still empty.\n'
            'def safe(f):\n    try:\n        return f()\n    except Exception:\n        return np.nan')

    nb.step(1, 'Look at the loans', 'Each record of loans.csv is one loan. The target is default: 1 if the borrower stopped repaying (the positive class), 0 if the loan was repaid.')
    nb.predict('What share of the 8,000 loans do you think defaulted: about 1 percent, 12 percent or 50 percent?')
    nb.code('loans = pd.read_csv("loans.csv")\n'
            'print(loans.shape)\n'
            'default_rate = ' + ans('loans.default.mean()', 'np.nan', 'the mean of the default column is the share of 1s') + '\n'
            'print(default_rate)\n'
            'print(loans.default.value_counts())\n\n'
            'check("8,000 loans", len(loans), 8000, 0)\n'
            f'check("default rate", safe(lambda: default_rate), {r(F["rate"])}, 0.001)')
    nb.read('Which class is the positive class, and is the data balanced?')

    nb.step(2, 'Prepare: impossible values', 'A borrower cannot be 0 or 199 years old. Mark ages under 18 or over 100, and replace them with the median of the valid ages.')
    nb.predict('Print the youngest and oldest ages with loans.age.sort_values(). How many impossible ages do you expect?')
    nb.code('print(loans.age.sort_values().head(3).tolist(), loans.age.sort_values().tail(3).tolist())\n'
            'bad_age = ' + ans('(loans.age < 18) | (loans.age > 100)', 'pd.Series(False, index=loans.index)', '(loans.age < 18) | (loans.age > 100), with brackets round each test') + '\n'
            'age_median = ' + ans('loans.loc[~bad_age, "age"].median()', 'np.nan', 'the median age of the rows where bad_age is False') + '\n'
            'loans.loc[bad_age, "age"] = age_median\n'
            'print(bad_age.sum(), "ages replaced by", age_median)\n\n'
            f'check("impossible ages", safe(lambda: int(bad_age.sum())), {F["bad_n"]}, 0)\n'
            f'check("median of valid ages", safe(lambda: age_median), {F["age_med"]}, 0)')
    nb.read('Why use the median of the valid ages? What would the mean of all ages, including 199, do?')

    nb.step(3, 'Prepare: missing values with a missing-indicator', 'Make the flag income_missing first. Then fill the blank incomes with the median income. The order matters.')
    nb.predict('About how many incomes are blank: 40, 400 or 4,000?')
    nb.code('loans["income_missing"] = ' + ans('loans.monthly_income_ugx.isna().astype(int)', '0', '1 where the income is blank, 0 elsewhere (.isna().astype(int))') + '\n'
            'median_income = ' + ans('loans.monthly_income_ugx.median()', 'np.nan', 'the median of monthly_income_ugx (blanks are skipped)') + '\n'
            'loans["monthly_income_ugx"] = loans.monthly_income_ugx.fillna(median_income)\n'
            'print(loans.income_missing.sum(), "flagged;", loans.monthly_income_ugx.isna().sum(), "blanks left; median", median_income)\n\n'
            f'check("blank incomes flagged", safe(lambda: int(loans.income_missing.sum())), {F["miss_n"]}, 0)\n'
            'check("no blanks left", safe(lambda: int(loans.monthly_income_ugx.isna().sum())), 0, 0)\n'
            f'check("median income", safe(lambda: median_income), {r(F["inc_med"], 1)}, 1)')
    nb.change('Reload the file in a new cell and fill the blanks BEFORE making the flag. What does income_missing.sum() give now?')

    nb.step(4, 'Prepare: feature engineering', 'Build the instalment-to-income ratio (also called the payment-to-income ratio): the monthly instalment as a share of monthly income. '
            'The instalment is the loan amount times 1.15 divided by the term in months. The 1.15 is an illustrative assumption for interest and fees. It is not in the data.')
    nb.predict('Will the default rate be higher in the group of loans with the highest ratio? By how much?')
    nb.code('loans["instalment_to_income"] = ' + ans('loans.loan_amount_ugx * 1.15 / loans.term_months / loans.monthly_income_ugx', 'np.nan', 'loan_amount_ugx * 1.15 / term_months / monthly_income_ugx') + '\n'
            'top = loans.instalment_to_income > loans.instalment_to_income.quantile(0.75)\n'
            'top_rate = ' + ans('loans.default[top].mean()', 'np.nan', 'the default rate among the loans where top is True') + '\n'
            'print("median ratio", round(loans.instalment_to_income.median(), 3), " default rate in the highest quarter", round(top_rate, 3))\n\n'
            f'check("median ratio", safe(lambda: loans.instalment_to_income.median()), {r(F["ratio_med"])}, 0.005)\n'
            f'check("default rate in the highest quarter of the ratio", safe(lambda: top_rate), {r(q[3])}, 0.01)')
    nb.read('Compare top_rate with the overall default rate. Would this ratio help a model?')

    nb.step(5, 'Choose the features and the target', 'Twelve features known at approval. collection_calls is left out on purpose: it is recorded after a loan goes bad, so it leaks the answer.')
    nb.code('features = ["age", "monthly_income_ugx", "income_missing", "loan_amount_ugx", "term_months", "previous_loans",\n'
            '            "previous_late_payments", "group_loan", "savings_balance_ugx", "has_mobile_money", "distance_to_branch_km", "instalment_to_income"]\n'
            'X = ' + ans('loans[features]', 'loans[["age"]]', 'the feature columns of loans (the list features)') + '\n'
            'y = ' + ans('loans["default"]', 'pd.Series(0, index=loans.index)', 'the target column') + '\n'
            'print(X.shape, y.shape)\n\n'
            'check("12 features", X.shape[1], 12, 0)\n'
            'check("no blanks in X", safe(lambda: int(X.isna().sum().sum())), 0, 0)')

    nb.step(6, 'Split into a training set and a test set', 'Hold back 25 percent of the loans. stratify=y keeps the default rate the same in both parts, and random_state=42 makes the split repeatable. '
            'Note: the medians above were computed on all 8,000 loans before the split. That is a small leakage risk that we accept on purpose for teaching.')
    nb.predict('How many defaults will the test set hold if it keeps the same rate as the whole file?')
    nb.code('X_train, X_test, y_train, y_test = ' + ans('train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)', 'X.iloc[:5], X.iloc[5:10], y.iloc[:5], y.iloc[5:10]',
                                                         'train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)') + '\n'
            'print(len(X_train), len(X_test), "loans;", y_train.sum(), "and", y_test.sum(), "defaults")\n'
            'print("first test rows:", X_test.index[:10].tolist())   # the same rows as the course notes when random_state=42 and stratify=y\n\n'
            f'check("test loans", len(X_test), {F["n_te"]}, 0)\n'
            f'check("defaults in the test set", int(y_test.sum()), {F["d_te"]}, 0)\n'
            f'check("defaults in the training set", int(y_train.sum()), {F["d_tr"]}, 0)')
    nb.change('The prepared file filled the blank incomes with the median of all 8,000 loans. Compute the median income of the training loans only (use the raw income column) and compare. How big is the difference?')
    nb.code('raw_income = pd.read_csv("loans.csv").monthly_income_ugx   # the blanks are still blank in this fresh copy\n'
            'train_median_income = ' + ans('raw_income.loc[X_train.index].median()', 'np.nan', 'the median of raw_income for the rows in X_train (raw_income.loc[X_train.index])') + '\n'
            'print("training rows only:", train_median_income, " all loans:", median_income)\n\n'
            f'check("median income of the training loans", safe(lambda: train_median_income), {r(F["inc_med_train"], 1)}, 1)')

    nb.step(7, 'The baseline model', 'The simplest possible model predicts the majority class for every loan. Every real model has to beat it.')
    nb.predict('What accuracy will the baseline model get on the test set? How many of the real defaults will it catch?')
    nb.code('baseline_model = ' + ans('DummyClassifier(strategy="most_frequent")', 'DummyClassifier(strategy="constant", constant=1)', 'DummyClassifier(strategy="most_frequent")') + '\n'
            'baseline_model.fit(X_train, y_train)\n'
            'y_base = baseline_model.predict(X_test)\n'
            'base_acc = ' + ans('accuracy_score(y_test, y_base)', 'np.nan', 'accuracy_score(y_test, y_base)') + '\n'
            'base_recall = ' + ans('recall_score(y_test, y_base)', 'np.nan', 'recall_score(y_test, y_base)') + '\n'
            'print("baseline accuracy", round(base_acc, 4), " recall", base_recall)\n\n'
            f'check("baseline accuracy", safe(lambda: base_acc), {r(F["base_acc"])}, 0.001)\n'
            'check("baseline recall", safe(lambda: base_recall), 0, 0.001)')
    nb.read('The accuracy looks high. Why is it the accuracy paradox?')

    nb.step(8, 'Fit a first model and read what accuracy hides', 'A decision tree with max_depth=3 learns from the training set. We predict the test set once and compare with the baseline model. '
            f'Expected on the course split: accuracy {F["acc"]:.4f} and {F["tp"]} defaults caught. The checks accept the range seen over ten other splits ({F["acc_lo"]:.3f} to {F["acc_hi"]:.3f}), because a library version may break a tie differently.')
    nb.predict('Will the tree beat the baseline accuracy by a lot, or by about one point? Will it catch most of the defaults?')
    nb.code('model = ' + ans('DecisionTreeClassifier(max_depth=3, random_state=42)', 'DecisionTreeClassifier(max_depth=1, random_state=42)', 'DecisionTreeClassifier(max_depth=3, random_state=42)') + '\n'
            'model.fit(X_train, y_train)\n'
            'y_pred = ' + ans('model.predict(X_test)', 'np.zeros(len(X_test), dtype=int)', 'model.predict(X_test)') + '\n'
            'model_acc = accuracy_score(y_test, y_pred)\n'
            'model_recall = ' + ans('recall_score(y_test, y_pred)', 'np.nan', 'recall_score(y_test, y_pred)') + '\n'
            'print("tree accuracy", round(model_acc, 4), " recall", round(model_recall, 3))\n'
            'print(confusion_matrix(y_test, y_pred))   # rows: truth 0 and 1. columns: predicted 0 and 1\n\n'
            f'check("tree accuracy in the expected range", safe(lambda: model_acc), {r((F["acc_lo"] + F["acc_hi"]) / 2)}, {r((F["acc_hi"] - F["acc_lo"]) / 2 + 0.005)})\n'
            f'check("tree recall in the expected range", safe(lambda: model_recall), {r((F["rec_lo"] + F["rec_hi"]) / 2)}, {r((F["rec_hi"] - F["rec_lo"]) / 2 + 0.03)})\n'
            'check("tree beats the baseline model", safe(lambda: float(model_acc > base_acc)), 1, 0)')
    nb.read('How many defaults did the tree catch (bottom right of the matrix) and how many did it miss (bottom left)? Is it good enough to lend by?')
    nb.change('Fit the tree with max_depth=1, then max_depth=6, and print the accuracy and recall each time. Do not choose a depth by the test score: Session 17 shows how cross-validation on the training loans chooses it.')
    nb.code('for depth in (1, 3, 6):\n'
            '    m = DecisionTreeClassifier(max_depth=depth, random_state=42).fit(X_train, y_train)\n'
            '    p = m.predict(X_test)\n'
            '    print("max_depth", depth, " accuracy", round(accuracy_score(y_test, p), 4), " recall", round(recall_score(y_test, p), 3))')
    nb.change('Add the leaking column collection_calls to the features and fit again. What happens to the accuracy? Why is that useless at approval time?')
    nb.code('leak_train = X_train.assign(collection_calls=loans.loc[X_train.index, "collection_calls"])\n'
            'leak_test = X_test.assign(collection_calls=loans.loc[X_test.index, "collection_calls"])\n'
            'leak_model = DecisionTreeClassifier(max_depth=3, random_state=42).fit(leak_train, y_train)\n'
            'leak_acc = ' + ans('accuracy_score(y_test, leak_model.predict(leak_test))', 'np.nan', 'accuracy_score of leak_model on leak_test') + '\n'
            'print("accuracy with the leaking column", round(leak_acc, 4))\n\n'
            'check("the leak makes accuracy suspiciously high", safe(lambda: float(leak_acc > 0.95)), 1, 0)')

    nb.step(9, 'Keep a prepared file and write your note', 'Save the 12 features and the target as loans_prepared.csv so you can reload it instead of repeating the preparation.')
    nb.code('prepared = X.copy()\n'
            'prepared["default"] = y\n'
            'prepared.to_csv("loans_prepared.csv", index=False)\n'
            'print(pd.read_csv("loans_prepared.csv").shape)\n\n'
            'check("prepared file has 13 columns", pd.read_csv("loans_prepared.csv").shape[1], 13, 0)\n'
            f'check("prepared file has 8,000 rows", pd.read_csv("loans_prepared.csv").shape[0], {F["n"]}, 0)')
    nb.md('## Your three-sentence note\n\nDouble-click and write:\n\n1. Did the first model beat the baseline model, and by how many points of accuracy?\n2. How many of the real defaults did it catch?\n3. What does accuracy hide, and what would you try next?\n\n> My note: ')
    nb.code('show_checks()')
    return nb
