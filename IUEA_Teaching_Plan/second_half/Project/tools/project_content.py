"""One source of truth for the Engineering ML project: cohort facts, the Part A tasks (starter code and model solution), the Part B memo form,
the marks and the sitting rules. The notebooks, the rehearsal, the briefs and the marking guide are all built from this file, so the numbers
and names can never disagree. Numbers come from the NumPy reference, never typed.

Terminology follows Build/TERMS.md: baseline model, simple and multiple linear regression, training set, validation set, test set, residual,
imputation, hyperparameter, decision threshold, confusion matrix, data leakage, K-fold and group cross-validation, ablation study.
"""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
PLAN = PROJECT.parents[1]
sys.path.insert(0, str(PROJECT / 'grader_spec'))
sys.path.insert(0, str(PLAN / 'grader'))
import project_numpy_reference as P  # noqa: E402
import project_contracts as K  # noqa: E402
import memo_spec as M  # noqa: E402
from engineering_contracts import DOMAINS  # noqa: E402

VERSION = K.VERSION
CODES = ['CML3112', 'CML3113', 'CML3111']
COHORT = {
    'CML3112': dict(name='Civil Engineering and Architecture', domain='building cooling load', unit='kW', thing='building', payer='the client who pays for the cooling plant',
                    max_mae=2.0, class_day='Tuesday', released='Tuesday 24 November 2026'),
    'CML3113': dict(name='Mining and Petroleum Engineering', domain='crusher energy demand', unit='kWh/t', thing='crusher', payer='the mine manager who pays for the crusher power',
                    max_mae=1.0, class_day='Friday', released='Friday 27 November 2026'),
    'CML3111': dict(name='Electrical, Mechatronics, Robotics and Communications', domain='motor winding temperature', unit='deg C', thing='motor',
                    payer='the maintenance manager who pays for the motors', max_mae=2.0, class_day='Friday', released='Friday 27 November 2026'),
}
# The sitting: the Week 12 class slot. PROPOSED. The lecturer confirms the dates and times (and the room).
SITTING = {'CML3112': dict(day='Tuesday 1 December 2026', start='11:00', end='14:00', iso_start='2026-12-01T11:00:00+03:00', iso_end='2026-12-01T14:00:00+03:00'),
           'CML3113': dict(day='Friday 4 December 2026', start='08:00', end='11:00', iso_start='2026-12-04T08:00:00+03:00', iso_end='2026-12-04T11:00:00+03:00'),
           'CML3111': dict(day='Friday 4 December 2026', start='11:00', end='14:00', iso_start='2026-12-04T11:00:00+03:00', iso_end='2026-12-04T14:00:00+03:00')}
PROPOSED = 'proposed, lecturer to confirm'
MINUTES = 180
SITTING_TEXT = {c: f'{SITTING[c]["day"]}, {SITTING[c]["start"]} to {SITTING[c]["end"]} Kampala time (3 hours; {PROPOSED})' for c in SITTING}
REHEARSAL_TEXT = {c: f'{COHORT[c]["released"]} (after Class 4; {PROPOSED})' for c in COHORT}
AUTO_MARKS = K.PART_A_MAX                         # 30
PART_B = K.PART_B_MAX                             # 15
TIME_PLAN = [('Setup: sign in, open your notebook, run the supplied cells', 10), ('Tasks 1 to 3: cleaning, the split, the three models', 45), ('Tasks 4 to 6: warnings, cross-validation, ablation', 45),
             ('Tasks 7 and 8: choose a model, open the test set once', 15), ('Task 9: the Part B memo form', 25), ('Check, restart and run all, submit', 25), ('Spare time (breaks, reconnecting)', 15)]
assert sum(m for _, m in TIME_PLAN) == MINUTES


def csv_rows(code, v='A'):
    rows = []
    with K.csv_path(code, v).open() as f:
        for r in csv.DictReader(f):
            rows.append(dict(record_id=int(r['record_id']), equipment_id=r['equipment_id'], load_pct=float(r['load_pct']) if r['load_pct'] else None,
                             ambient_c=float(r['ambient_c']) if r['ambient_c'] else None, target=float(r['target']) if r['target'] else None))
    return rows


def numbers(code, v='A'):
    """Cohort numbers for the marking guide's worked example: all from the NumPy reference on the variant's file."""
    rows = csv_rows(code, v)
    p = P.cohort_pipeline(code, rows)
    limit = P.LIMITS[code]
    chosen = P.choose([dict(name=n, validation_mae=p['validation_mae'][n], latency_ms=P.LATENCY_MS[n]) for n in ('baseline', 'linear', 'tree')], COHORT[code]['max_mae'], P.MAX_MS)
    test = P.test_expected(code, rows, chosen, 0.5)
    return dict(p=p, limit=limit, chosen=chosen, test=test)


def options(code, v):
    return M.options(code, v, COHORT[code]['thing'])


# ------------------------------------------------------------------------------------------------ the supplied cells
SETUP_MARK, TEST_MARK = '# IUEA-SETUP-CELL', '# IUEA-TEST-CELL'


def setup_cell(code, v):
    c = COHORT[code]
    text = K.csv_text(code, v)
    return f'''#@title Prepare the data and the libraries - Do not edit this cell
# IUEA-SETUP-CELL  (supplied: do not edit)
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, roc_auc_score

TARGET_NAME = {c['domain']!r}
TARGET_UNIT = {c['unit']!r}
LIMIT = {P.LIMITS[code]!r}          # a row is a WARNING (1) when its target is at or above this limit, in {c['unit']}
MAX_MAE = {c['max_mae']!r}          # the client accepts a typical prediction error (MAE) of at most this many {c['unit']} (invented teaching number)
MAX_MS = {P.MAX_MS}                 # and a prediction time of at most this many milliseconds (invented teaching number)
LATENCY_MS = {P.LATENCY_MS!r}   # invented teaching numbers
MISSED_COST, FALSE_ALARM_COST = {P.MISS_COST}, {P.ALARM_COST}   # invented teaching costs (a false negative costs 5, a false positive costs 1)

_CSV_TEXT = """{text}"""
with open("engineering_data.csv", "w") as _f:          # your own copy of the data file: the same rows every time you run this cell
    _f.write(_CSV_TEXT)

def records_from_table(table):
    """A list of dictionaries, one per row. Missing values (NaN) become None."""
    objects = table.astype(object)
    return objects.where(table.notna(), None).to_dict("records")

raw_table = pd.read_csv("engineering_data.csv")
all_records = records_from_table(raw_table)
development_records = [r for r in all_records if r["equipment_id"] != "E6"]   # E6 is the TEST SET: nothing you write may use it before the very end
print("Rows in the file:", len(raw_table))
print("Rows you may develop with (groups E1 to E5):", len(development_records))
print(raw_table.head())
'''


def test_cell(code):
    return '''#@title Open the test set (run it ONCE, at the very end) - Do not edit this cell
# IUEA-TEST-CELL  (supplied: do not edit)
import json as _json
TEST_OPEN_LOG = []
_TEST_FILE = "test_first_opening.json"

def open_test_set(model_name, threshold):
    """Evaluate ONE chosen model and ONE chosen decision threshold on the test set (group E6), with the functions you wrote. Returns a dictionary."""
    if model_name not in ("baseline", "linear", "tree"):
        raise ValueError('model_name must be "baseline", "linear" or "tree"')
    if not isinstance(threshold, (int, float)) or not 0 < threshold < 1:
        raise ValueError("threshold must be a number between 0 and 1")
    first = _json.load(open(_TEST_FILE)) if os.path.exists(_TEST_FILE) else None
    if first is None:
        _json.dump({"model": model_name, "threshold": threshold}, open(_TEST_FILE, "w"))
    TEST_OPEN_LOG.append([model_name, threshold])
    changed = first is not None and (first["model"] != model_name or first["threshold"] != threshold)
    if changed:
        print("WARNING: THE TEST SET WAS ALREADY OPENED with model", first["model"], "and threshold", first["threshold"],
              "- opening it again with a different choice means it is no longer an honest test.")
    table = pd.read_csv("engineering_data.csv").drop_duplicates("record_id")
    table = table[table["target"].notna() & table["load_pct"].between(0, 100)]
    development = records_from_table(table[table["equipment_id"] != "E6"])
    held_out = records_from_table(table[table["equipment_id"] == "E6"])
    features = [{k: v for k, v in r.items() if k != "target"} for r in held_out]
    actual = [r["target"] for r in held_out]
    errors = regression_errors(actual, fit_predict_regression(development, features)[model_name])
    probability = warning_probabilities(development, features, LIMIT)
    warning = classification_scores([1 if v >= LIMIT else 0 for v in actual], probability, threshold)
    outcome = {"model": model_name, "threshold": threshold, "n_rows": len(held_out), "mae": errors["mae"], "rmse": errors["rmse"],
               "warning": warning, "changed_after_opening": bool(changed)}
    print("Test set opened with", model_name, "and threshold", threshold, "on", len(held_out), "rows")
    print("  MAE", round(errors["mae"], 3), TARGET_UNIT, "| RMSE", round(errors["rmse"], 3), TARGET_UNIT)
    print("  warnings: precision", round(warning["precision"], 3), "recall", round(warning["recall"], 3), "F1", round(warning["f1"], 3), "AUC", round(warning["auc"], 3))
    return outcome
'''


# ------------------------------------------------------------------------------------------------ the tasks
def tasks(code, v='A'):
    """Part A tasks. Each: key, title, week, marks (automatic), intro (markdown), cells: list of (starter, solution) code pairs."""
    c = COHORT[code]
    u = c['unit']
    t = []

    t.append(dict(key='clean', title='Clean the rows and look at them', week='Weeks 3 to 7', marks=dict(clean=2), intro=f'''A **record** is one row written as a dictionary: `{{"record_id": 1, "equipment_id": "E1", "load_pct": 59.15, "ambient_c": 31.71, "target": 52.5}}`. A missing value (a blank cell, `NaN` in pandas) is `None`.

`clean_rows(records)` returns a cleaned **copy** of the records, in the same order:
- keep only the first row for each `record_id`;
- drop a row whose `target` is `None`, or whose `load_pct` is `None` or outside 0 to 100 (0 and 100 are valid);
- **do not fill** `ambient_c`. A missing value stays `None`. The models do the imputation later, using the training set only, so that nothing leaks (data leakage).

Never change the list you were given. Then use your function on the development rows and draw **Chart 1**: `load_pct` across, `target` up, with a title and both axis names, and the unit ({u}).''',
                 cells=[('''def clean_rows(records):
    """Return a cleaned copy of the records (see the task text above)."""
    # TODO 1: make an empty list called kept and an empty set called seen.
    # TODO 2: loop over records. If record["record_id"] is already in seen, skip the row (continue). Otherwise add the id to seen.
    # TODO 3: skip the row if target is None, or load_pct is None, or load_pct is below 0 or above 100.
    # TODO 4: add dict(record) (a copy) to kept. Do not touch ambient_c.
    return None   # TODO 5: return kept instead
''', '''def clean_rows(records):
    """Return a cleaned copy of the records (see the task text above)."""
    seen, kept = set(), []
    for record in records:
        if record["record_id"] in seen:
            continue
        seen.add(record["record_id"])
        if record["target"] is None or record["load_pct"] is None or not 0 <= record["load_pct"] <= 100:
            continue
        kept.append(dict(record))
    return kept
'''),
                        ('''development_rows = None      # TODO: call clean_rows on development_records
print("Rows kept:", None)    # TODO: replace None with the number of rows in development_rows

figure, axes = plt.subplots()
# TODO: axes.scatter(...): load_pct on the x axis, target on the y axis (hint: table = pd.DataFrame(development_rows))
# TODO: axes.set_title(...), axes.set_xlabel(...) and axes.set_ylabel(...). Write the unit in the y label.
chart_1 = figure
plt.show()
''', f'''development_rows = clean_rows(development_records)
print("Rows kept:", len(development_rows))

figure, axes = plt.subplots()
table = pd.DataFrame(development_rows)
axes.scatter(table["load_pct"], table["target"])
axes.set_title("Chart 1: {c['domain']} rises with load")
axes.set_xlabel("Load (%)")
axes.set_ylabel("{c['domain'].capitalize()} ({u})")
chart_1 = figure
plt.show()
''')]))

    t.append(dict(key='split', title='Split by whole equipment groups', week='Week 10', marks=dict(split=2), intro='''`group_split(records)` returns a dictionary with three lists of `record_id` values, each in the order the records came in:
- `"train"`: groups E1, E2, E3 and E4 (the **training set**);
- `"validation"`: group E5 (the **validation set**);
- `"test"`: group E6 (the **test set**).

Never use the target to decide where a row goes. Whole machines go together, because a new machine must be a machine the model has never met. Your development rows have no E6 rows, so their `"test"` list is empty. That is correct.''',
                 cells=[('''def group_split(records):
    """Return {"train": [...], "validation": [...], "test": [...]} (lists of record_id, in input order)."""
    # TODO: for each record, look at record["equipment_id"] and put record["record_id"] in the right list.
    return None
''', '''def group_split(records):
    """Return {"train": [...], "validation": [...], "test": [...]} (lists of record_id, in input order)."""
    groups = {"train": ["E1", "E2", "E3", "E4"], "validation": ["E5"], "test": ["E6"]}
    return {name: [r["record_id"] for r in records if r["equipment_id"] in members] for name, members in groups.items()}
'''),
                        ('''split_ids = None     # TODO: group_split(development_rows)
train_rows = None    # TODO: the development rows whose record_id is in split_ids["train"]
valid_rows = None    # TODO: the development rows whose record_id is in split_ids["validation"]
print("Training rows:", None, "| validation rows:", None)   # TODO: replace the Nones with the two counts
''', '''split_ids = group_split(development_rows)
train_rows = [r for r in development_rows if r["record_id"] in set(split_ids["train"])]
valid_rows = [r for r in development_rows if r["record_id"] in set(split_ids["validation"])]
print("Training rows:", len(train_rows), "| validation rows:", len(valid_rows))
''')]))

    t.append(dict(key='regression', title='Question 1: a baseline model, a linear regression and a decision tree', week='Weeks 8 and 9', marks=dict(regression=3, errors=2), intro=f'''**Question 1.** How many {u} of {c['domain']} will a {c['thing']} show at a given load and ambient temperature, for equipment the model has never met?

`fit_predict_regression(training_records, feature_records)` trains (fits) three models on the training records and predicts for the feature records. Use only `load_pct` then `ambient_c`, in that order. The feature records have **no target**.
- every model is a pipeline that first does **imputation** of missing values with the **median of the training rows** (`SimpleImputer(strategy="median")`), then fits;
- `"baseline"`: the baseline model, which always predicts the mean training target (`DummyRegressor`);
- `"linear"`: multiple linear regression (two features), `LinearRegression`;
- `"tree"`: a decision tree, `DecisionTreeRegressor(max_depth=4, random_state=17)`. The `max_depth` is a **hyperparameter**: a setting you choose before training.

Return a dictionary with three lists of predictions, in the order of the feature records. The baseline model must use the **training** rows only: a baseline built with validation or test targets has **leaked**.

`regression_errors(actual, predicted)` returns `{{"mae": ..., "rmse": ...}}` over the same pairs, not rounded. A **residual** is actual minus predicted. MAE (mean absolute error) is the mean of the absolute residuals. RMSE (root mean squared error) is the square root of the mean of the squared residuals.''',
                 cells=[('''def fit_predict_regression(training_records, feature_records):
    """Return {"baseline": [...], "linear": [...], "tree": [...]}."""
    # TODO 1: table = pd.DataFrame(training_records); new = pd.DataFrame(feature_records)
    # TODO 2: X_train = the two feature columns of table; y_train = table["target"]; X_new = the same two columns of new.
    # TODO 3: a dictionary of three pipelines. Each is make_pipeline(SimpleImputer(strategy="median"), <the model>).
    # TODO 4: loop over the dictionary: fit on (X_train, y_train), predict X_new, and store predictions.tolist() under the model's name.
    return None
''', '''def fit_predict_regression(training_records, feature_records):
    """Return {"baseline": [...], "linear": [...], "tree": [...]}."""
    columns = ["load_pct", "ambient_c"]
    table, new = pd.DataFrame(training_records), pd.DataFrame(feature_records)
    X_train, y_train, X_new = table[columns], table["target"], new[columns]
    models = {"baseline": make_pipeline(SimpleImputer(strategy="median"), DummyRegressor(strategy="mean")),
              "linear": make_pipeline(SimpleImputer(strategy="median"), LinearRegression()),
              "tree": make_pipeline(SimpleImputer(strategy="median"), DecisionTreeRegressor(max_depth=4, random_state=17))}
    predictions = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        predictions[name] = [float(v) for v in model.predict(X_new)]
    return predictions
'''),
                        ('''def regression_errors(actual, predicted):
    """Return {"mae": ..., "rmse": ...}, not rounded."""
    # TODO: use numpy: residuals = np.array(actual) - np.array(predicted); MAE uses np.abs and the mean; RMSE uses squares, the mean, then np.sqrt.
    return None
''', '''def regression_errors(actual, predicted):
    """Return {"mae": ..., "rmse": ...}, not rounded."""
    residuals = np.array(actual, dtype=float) - np.array(predicted, dtype=float)
    return {"mae": float(np.mean(np.abs(residuals))), "rmse": float(np.sqrt(np.mean(residuals ** 2)))}
'''),
                        ('''# Evaluate the three models on the validation set (group E5). Keep the names: validation_predictions, validation_mae and validation_rmse.
validation_features = None    # TODO: the validation rows without the "target" key
validation_actual = None      # TODO: the list of validation targets
validation_predictions = None # TODO: fit_predict_regression(train_rows, validation_features)
validation_mae = None         # TODO: a dictionary {"baseline": ..., "linear": ..., "tree": ...} of MAE values, from regression_errors
validation_rmse = None        # TODO: the same with RMSE
print("Validation MAE  (" + TARGET_UNIT + "):", validation_mae)
print("Validation RMSE (" + TARGET_UNIT + "):", validation_rmse)

figure, axes = plt.subplots()
# TODO: a bar chart of the three MAE values, with a title, a y label that includes the unit, and the model names on the x axis.
chart_2 = figure
plt.show()
''', f'''validation_features = [{{k: v for k, v in r.items() if k != "target"}} for r in valid_rows]
validation_actual = [r["target"] for r in valid_rows]
validation_predictions = fit_predict_regression(train_rows, validation_features)
validation_mae = {{name: regression_errors(validation_actual, p)["mae"] for name, p in validation_predictions.items()}}
validation_rmse = {{name: regression_errors(validation_actual, p)["rmse"] for name, p in validation_predictions.items()}}
print("Validation MAE  (" + TARGET_UNIT + "):", validation_mae)
print("Validation RMSE (" + TARGET_UNIT + "):", validation_rmse)

figure, axes = plt.subplots()
axes.bar(list(validation_mae), list(validation_mae.values()))
axes.set_title("Chart 2: prediction error (MAE) on the validation set")
axes.set_xlabel("Model")
axes.set_ylabel("MAE ({u})")
chart_2 = figure
plt.show()
''')]))

    t.append(dict(key='warning', title='Question 2: which rows should raise a warning?', week='Week 9', marks=dict(warning=2, scores=3), intro=f'''**Question 2.** A row is a **warning** (1, the positive class) when its target is at or above `LIMIT` ({P.LIMITS[code]:g} {u}) and **no warning** (0, the negative class) below it. Which rows should raise a warning?

`warning_probabilities(training_records, feature_records, limit)` returns the probability of a warning, for each feature record, from a pipeline of `SimpleImputer(strategy="median")`, `StandardScaler()` and `LogisticRegression(max_iter=1000)` (binary classification), fitted on the training records only. The label is `1` when the training target is `>= limit`. Use `load_pct` then `ambient_c`.

`classification_scores(actual, probability, threshold)` predicts a warning when the probability is `>= threshold` (the **decision threshold**), then returns a dictionary with the confusion matrix counts `tp`, `fp`, `fn`, `tn` (true positives, false positives, false negatives, true negatives) and `precision`, `recall`, `f1`, `cost` and `auc`. A false negative (a missed warning) costs `MISSED_COST` and a false positive (a false alarm) costs `FALSE_ALARM_COST` (invented teaching costs), so `cost = 5 * fn + 1 * fp`. When a ratio has a zero denominator, use 0. `auc` is the ROC AUC of the probabilities and does not depend on the threshold.

Then try decision thresholds 0.3, 0.5 and 0.7 on the validation set, and keep the one with the lowest cost as `chosen_threshold` (if two tie, take the higher one).''',
                 cells=[('''def warning_probabilities(training_records, feature_records, limit):
    """Return a list of warning probabilities, one per feature record."""
    # TODO 1: tables as before; y_train = (training target >= limit) turned into 0 and 1 (astype(int)).
    # TODO 2: model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000)); fit it.
    # TODO 3: predict_proba(X_new) gives two columns: column 1 is the probability of a warning. Return it as a list of floats.
    return None
''', '''def warning_probabilities(training_records, feature_records, limit):
    """Return a list of warning probabilities, one per feature record."""
    columns = ["load_pct", "ambient_c"]
    table, new = pd.DataFrame(training_records), pd.DataFrame(feature_records)
    y_train = (table["target"] >= limit).astype(int)
    model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000))
    model.fit(table[columns], y_train)
    return [float(v) for v in model.predict_proba(new[columns])[:, 1]]
'''),
                        ('''def classification_scores(actual, probability, threshold):
    """Return tp, fp, fn, tn, precision, recall, f1, cost and auc."""
    # TODO 1: predicted = 1 where the probability is at or above the threshold, else 0 (a list comprehension).
    # TODO 2: tn, fp, fn, tp = confusion_matrix(actual, predicted).ravel()   (see Class 2)
    # TODO 3: precision_score, recall_score and f1_score with zero_division=0; roc_auc_score(actual, probability).
    # TODO 4: cost = MISSED_COST * fn + FALSE_ALARM_COST * fp. Turn numpy numbers into int() and float() before returning.
    return None
''', '''def classification_scores(actual, probability, threshold):
    """Return tp, fp, fn, tn, precision, recall, f1, cost and auc."""
    predicted = [1 if p >= threshold else 0 for p in probability]
    tn, fp, fn, tp = confusion_matrix(actual, predicted).ravel()
    return {"tp": int(tp), "fp": int(fp), "fn": int(fn), "tn": int(tn),
            "precision": float(precision_score(actual, predicted, zero_division=0)),
            "recall": float(recall_score(actual, predicted, zero_division=0)),
            "f1": float(f1_score(actual, predicted, zero_division=0)),
            "cost": int(MISSED_COST * fn + FALSE_ALARM_COST * fp),
            "auc": float(roc_auc_score(actual, probability))}
'''),
                        ('''warning_actual = None        # TODO: 1 or 0 for each validation row: is the target at or above LIMIT?
warning_probability = None   # TODO: warning_probabilities(train_rows, validation_features, LIMIT)
threshold_table = {}         # TODO: for each threshold in 0.3, 0.5, 0.7: threshold_table[threshold] = classification_scores(...)
warning_auc = None           # TODO: the "auc" value of any one entry of threshold_table
chosen_threshold = None      # TODO: the threshold with the lowest cost (if two tie, the higher threshold)
for threshold, scores in threshold_table.items():
    print(threshold, scores)
print("Chosen threshold:", chosen_threshold)
''', '''warning_actual = [1 if r["target"] >= LIMIT else 0 for r in valid_rows]
warning_probability = warning_probabilities(train_rows, validation_features, LIMIT)
threshold_table = {}
for threshold in (0.3, 0.5, 0.7):
    threshold_table[threshold] = classification_scores(warning_actual, warning_probability, threshold)
warning_auc = threshold_table[0.5]["auc"]
chosen_threshold = sorted(threshold_table, key=lambda th: (threshold_table[th]["cost"], -th))[0]
for threshold, scores in threshold_table.items():
    print(threshold, scores)
print("Chosen threshold:", chosen_threshold)
''')]))

    t.append(dict(key='trust', title='Can you trust it? Group cross-validation', week='Week 10', marks=dict(groupcv=3), intro='''One validation set of about 15 rows can mislead. **Group cross-validation** (K-fold cross-validation where each fold is a whole equipment group, the idea of `GroupKFold`) gives each machine a turn as the hidden machine.

`group_cv_mae(records)` receives clean records with **no missing values** and uses whole equipment groups. Hold out each of E1, E2, E3, E4 and E5 in turn (E6 is never used). For each fold, fit `LinearRegression` on `load_pct` and `ambient_c` using the other four groups, and compute the MAE on the held-out group. Return `{"folds": [...], "mean": ..., "spread": ...}`: the five MAEs in the order E1 to E5, their mean, and their sample standard deviation (`ddof=1`). Do not round.

**Data leakage check, in your own head:** the imputer, the StandardScaler (standardisation) and the baseline model's mean are all fitted on the training rows only. If any of them had seen validation or test rows, the scores would look better than they are.''',
                 cells=[('''def group_cv_mae(records):
    """Return {"folds": [five MAEs, E1 to E5], "mean": ..., "spread": ...}."""
    # TODO 1: table = pd.DataFrame(records)
    # TODO 2: for group in ["E1", "E2", "E3", "E4", "E5"]: train = rows of the OTHER groups in E1 to E5, test = the rows of group.
    # TODO 3: fit LinearRegression on the two feature columns of train; the MAE on test is np.mean(np.abs(...)).
    # TODO 4: mean = np.mean(folds); spread = np.std(folds, ddof=1).
    return None
''', '''def group_cv_mae(records):
    """Return {"folds": [five MAEs, E1 to E5], "mean": ..., "spread": ...}."""
    columns = ["load_pct", "ambient_c"]
    table = pd.DataFrame(records)
    table = table[table["equipment_id"].isin(["E1", "E2", "E3", "E4", "E5"])]
    folds = []
    for group in ["E1", "E2", "E3", "E4", "E5"]:
        train, test = table[table["equipment_id"] != group], table[table["equipment_id"] == group]
        model = LinearRegression().fit(train[columns], train["target"])
        folds.append(float(np.mean(np.abs(test["target"] - model.predict(test[columns])))))
    return {"folds": folds, "mean": float(np.mean(folds)), "spread": float(np.std(folds, ddof=1))}
'''),
                        ('''complete_rows = None    # TODO: the development rows whose ambient_c is not None
cv_summary = None       # TODO: group_cv_mae(complete_rows)
print("Cross-validated MAE (" + TARGET_UNIT + "):", cv_summary)
''', '''complete_rows = [r for r in development_rows if r["ambient_c"] is not None]
cv_summary = group_cv_mae(complete_rows)
print("Cross-validated MAE (" + TARGET_UNIT + "):", cv_summary)
''')]))

    t.append(dict(key='features', title='Does a new column help? An ablation study', week='Week 11', marks=dict(ablation=2), intro='''`ablation_mae(training_records, validation_records)` is a small **ablation study**: it compares two linear regression models on the same rows. Both records lists are complete (no missing values). Fit `LinearRegression` on the training records twice: with the two base features (`load_pct`, `ambient_c`), and with a third column, the **interaction feature** `load_pct * ambient_c`. Score both on the validation records. Return `{"base_mae": ..., "extended_mae": ..., "improvement": base_mae - extended_mae}`, not rounded. A positive improvement means the new feature helped.''',
                 cells=[('''def ablation_mae(training_records, validation_records):
    """Return base_mae, extended_mae and improvement."""
    # TODO 1: two tables. Build the extra column on both: table["load_x_ambient"] = table["load_pct"] * table["ambient_c"].
    # TODO 2: fit LinearRegression with the base columns, then with the base columns plus load_x_ambient. Same rows, same measure.
    return None
''', '''def ablation_mae(training_records, validation_records):
    """Return base_mae, extended_mae and improvement."""
    train, valid = pd.DataFrame(training_records), pd.DataFrame(validation_records)
    for table in (train, valid):
        table["load_x_ambient"] = table["load_pct"] * table["ambient_c"]
    scores = []
    for columns in (["load_pct", "ambient_c"], ["load_pct", "ambient_c", "load_x_ambient"]):
        model = LinearRegression().fit(train[columns], train["target"])
        scores.append(float(np.mean(np.abs(valid["target"] - model.predict(valid[columns])))))
    return {"base_mae": scores[0], "extended_mae": scores[1], "improvement": scores[0] - scores[1]}
'''),
                        ('''complete_train = None    # TODO: the rows of train_rows whose ambient_c is not None
complete_valid = None    # TODO: the rows of valid_rows whose ambient_c is not None
ablation_result = None   # TODO: ablation_mae(complete_train, complete_valid)
print("Ablation (" + TARGET_UNIT + "):", ablation_result)
''', '''complete_train = [r for r in train_rows if r["ambient_c"] is not None]
complete_valid = [r for r in valid_rows if r["ambient_c"] is not None]
ablation_result = ablation_mae(complete_train, complete_valid)
print("Ablation (" + TARGET_UNIT + "):", ablation_result)
''')]))

    t.append(dict(key='choose', title='Choose one model by a rule', week='Week 11', marks=dict(choose=1), intro=f'''`choose_model(candidates, max_mae, max_ms)` takes a list of dictionaries with `name`, `validation_mae` and `latency_ms`. Keep the candidates whose `validation_mae <= max_mae` **and** `latency_ms <= max_ms` (both limits are inclusive). Among those, choose the smallest `validation_mae`; break a tie by the smaller `latency_ms`, then by the name in alphabetical order. Return the chosen name, or `None` if nobody qualifies. Never use the test set to choose.

The client for this project is {c['payer']}. The client accepts a typical prediction error of at most `MAX_MAE` ({c['max_mae']:g} {u}) and a prediction time of at most `MAX_MS` ({P.MAX_MS} ms). Both numbers are invented for teaching.''',
                 cells=[('''def choose_model(candidates, max_mae, max_ms):
    """Return the chosen model name, or None."""
    # TODO: filter with a list comprehension, then sort with key=lambda c: (c["validation_mae"], c["latency_ms"], c["name"]).
    return None
''', '''def choose_model(candidates, max_mae, max_ms):
    """Return the chosen model name, or None."""
    allowed = [c for c in candidates if c["validation_mae"] <= max_mae and c["latency_ms"] <= max_ms]
    if not allowed:
        return None
    return sorted(allowed, key=lambda c: (c["validation_mae"], c["latency_ms"], c["name"]))[0]["name"]
'''),
                        ('''candidate_table = []     # TODO: one dictionary per model (baseline, linear, tree): name, validation_mae (from your Task 3 results), latency_ms (from LATENCY_MS)
chosen_model = None      # TODO: choose_model(candidate_table, MAX_MAE, MAX_MS)
print(candidate_table)
print("Chosen model:", chosen_model)
''', '''candidate_table = [{"name": name, "validation_mae": validation_mae[name], "latency_ms": LATENCY_MS[name]} for name in ("baseline", "linear", "tree")]
chosen_model = choose_model(candidate_table, MAX_MAE, MAX_MS)
print(candidate_table)
print("Chosen model:", chosen_model)
''')]))

    t.append(dict(key='test', title='Open the test set, once', week='Week 11', marks=dict(test=2, results=2), intro='''Group E6 is the **test set**: a different piece of equipment that nothing so far has used. It gives **one** honest estimate for the model you chose.

How it works. The supplied cell below is marked Do not edit this cell. Run it once to define `open_test_set(model_name, threshold)`. Then call it **one time**, with the model you chose in Task 7 and the decision threshold you chose in Task 4. It trains your functions on all the development rows (E1 to E5), evaluates on E6, prints the result and writes your choice to a small file. If you call it again, the notebook counts a second opening: you lose the "opened once" mark even when the choice is the same, and you lose more if the choice is different.

You must not use E6 to choose a model, a threshold or anything else, and you must not look at it before this call. Report whatever the result is in your Part B form.''',
                 cells=[('__TEST__', '__TEST__'),
                        ('''test_result = None     # TODO: open_test_set(chosen_model, chosen_threshold)
''', '''test_result = open_test_set(chosen_model, chosen_threshold)
''')]))
    return t


# ------------------------------------------------------------------------------------------------ the self-check cell (visible)
SELF_CHECK = '''# This cell is a SELF-CHECK. It is not marked. It uses tiny examples with known answers, so you can see at once if a function is wrong.
# The marked (hidden) checks run your functions on OTHER data you cannot see, so passing here does not mean full marks.
def _try(label, test):
    try:
        ok = bool(test())
    except Exception as error:
        ok = False
    print(("PASS  " if ok else "TODO  ") + label)
    return ok

_small = [dict(record_id=1, equipment_id="E1", load_pct=50.0, ambient_c=20.0, target=10.0),
          dict(record_id=1, equipment_id="E1", load_pct=50.0, ambient_c=20.0, target=10.0),
          dict(record_id=2, equipment_id="E2", load_pct=120.0, ambient_c=22.0, target=12.0),
          dict(record_id=3, equipment_id="E5", load_pct=40.0, ambient_c=None, target=None),
          dict(record_id=4, equipment_id="E6", load_pct=100.0, ambient_c=None, target=20.0)]
_checks = []
_checks.append(_try("clean_rows keeps ids 1 and 4 only, in order, and leaves the missing ambient_c as None",
                    lambda: [r["record_id"] for r in clean_rows(_small)] == [1, 4] and clean_rows(_small)[1]["ambient_c"] is None))
_checks.append(_try("clean_rows does not change the list you give it", lambda: (len(_small) == 5 and clean_rows(_small) is not _small)))
_checks.append(_try("group_split puts E1 in train, E5 in validation, E6 in test",
                    lambda: group_split(_small) == {"train": [1, 1, 2], "validation": [3], "test": [4]}))
_toy = [dict(record_id=i, equipment_id="E1", load_pct=10.0 * i, ambient_c=20.0, target=2.0 * i) for i in range(1, 7)]
_new = [dict(record_id=9, equipment_id="E2", load_pct=35.0, ambient_c=None)]
_checks.append(_try("fit_predict_regression returns baseline, linear and tree, one prediction per feature record",
                    lambda: sorted(fit_predict_regression(_toy, _new)) == ["baseline", "linear", "tree"] and all(len(v) == 1 for v in fit_predict_regression(_toy, _new).values())))
_checks.append(_try("the baseline model predicts the mean of the TRAINING targets (7.0)", lambda: abs(fit_predict_regression(_toy, _new)["baseline"][0] - 7.0) < 1e-9))
_checks.append(_try("regression_errors([1, 3], [2, 5]) has mae 1.5 and rmse sqrt(2.5)",
                    lambda: abs(regression_errors([1, 3], [2, 5])["mae"] - 1.5) < 1e-9 and abs(regression_errors([1, 3], [2, 5])["rmse"] - 2.5 ** 0.5) < 1e-9))
_checks.append(_try("classification_scores on a known case (tp 1, fp 1, fn 1, tn 1, cost 6, auc 0.75)",
                    lambda: (lambda s: (s["tp"], s["fp"], s["fn"], s["tn"], s["cost"], round(s["auc"], 2)) == (1, 1, 1, 1, 6, 0.75))(classification_scores([1, 0, 1, 0], [0.9, 0.8, 0.2, 0.1], 0.5))))
_checks.append(_try("warning_probabilities gives numbers between 0 and 1",
                    lambda: all(0 <= p <= 1 for p in warning_probabilities(_toy, _new, 8.0))))
_checks.append(_try("choose_model picks the smallest error that meets both limits",
                    lambda: choose_model([dict(name="a", validation_mae=2, latency_ms=3), dict(name="b", validation_mae=1, latency_ms=30)], 2, 10) == "a"))
_checks.append(_try("group_cv_mae returns five folds, a mean and a spread",
                    lambda: len(group_cv_mae(complete_rows)["folds"]) == 5 and {"mean", "spread"} <= set(group_cv_mae(complete_rows))))
_checks.append(_try("ablation_mae returns base_mae, extended_mae and improvement",
                    lambda: {"base_mae", "extended_mae", "improvement"} <= set(ablation_mae(complete_train, complete_valid))))
for _name in ["validation_mae", "cv_summary", "warning_auc", "ablation_result", "candidate_table", "chosen_model", "chosen_threshold"]:
    _checks.append(_try("the variable " + _name + " has been calculated (it is not None)", lambda: globals().get(_name) is not None))
_checks.append(_try("the test set has been opened exactly once", lambda: len(TEST_OPEN_LOG) == 1))
_checks.append(_try("Chart 1 and Chart 2 each have a title, named axes and the unit",
                    lambda: all(f.axes[0].get_title() and f.axes[0].get_xlabel() and f.axes[0].get_ylabel() for f in (chart_1, chart_2))))
print()
print(sum(_checks), "of", len(_checks), "self-checks pass. Now choose Runtime, Restart session and run all, and check that nothing stops with an error.")
'''

MEMO_SELF_CHECK = '''# MEMO SELF-CHECK (not marked): did you fill in every field, and do your numbers agree with your own notebook?
# It does not tell you whether your choices are the best ones. The marking computer checks that.
def _memo_try(label, test):
    try:
        ok = bool(test())
    except Exception:
        ok = False
    print(("PASS  " if ok else "TODO  ") + label)
    return ok

def _near(a, b):
    return isinstance(a, (int, float)) and isinstance(b, (int, float)) and abs(a - b) <= 0.011

_memo_checks = [
    _memo_try("recommended_model is one of the models you trained", lambda: MEMO["recommended_model"] in validation_mae),
    _memo_try("recommended_threshold is 0.3, 0.5 or 0.7", lambda: MEMO["recommended_threshold"] in (0.3, 0.5, 0.7)),
    _memo_try("validation_mae has your three validation MAE values (two decimals are enough)", lambda: all(_near(MEMO["validation_mae"][k], validation_mae[k]) for k in ("baseline", "linear", "tree"))),
    _memo_try("cv_mean_mae is your cross-validated mean MAE", lambda: _near(MEMO["cv_mean_mae"], cv_summary["mean"])),
    _memo_try("test_mae is the test MAE you saw when you opened the test set", lambda: _near(MEMO["test_mae"], test_result["mae"])),
    _memo_try("test_recall is the test recall you saw (between 0 and 1)", lambda: _near(MEMO["test_recall"], test_result["warning"]["recall"])),
    _memo_try("limits has three different letters", lambda: len({str(x).strip().upper() for x in MEMO["limits"] if str(x).strip()}) == 3),
    _memo_try("next_step is one letter", lambda: len(str(MEMO["next_step"]).strip()) == 1),
    _memo_try("answer_choice has 8 to 80 words", lambda: 8 <= len(str(MEMO["answer_choice"]).split()) <= 80),
    _memo_try("answer_test_set has 8 to 80 words", lambda: 8 <= len(str(MEMO["answer_test_set"]).split()) <= 80),
]
print()
print(sum(_memo_checks), "of", len(_memo_checks), "memo self-checks pass.")
'''


def memo_markdown(code, v):
    c = COHORT[code]
    limit_opts, next_opts = options(code, v)
    lim = '\n'.join(f'- **{letter}.** {text}' for letter, text, _, _ in limit_opts)
    nxt = '\n'.join(f'- **{letter}.** {text}' for letter, text, _, _ in next_opts)
    return f'''## Task 9: Part B, the decision memo form ({K.PART_B_MAX} automatic marks)
Your memo is a **form**, not an essay. You write it for **{c['payer']}**. Fill in the dictionary `MEMO` in the next cell. Every value is checked by the marking computer; nothing is read by a person. Use your own numbers, with at least two decimals, in **{c['unit']}**.

| Field | What to enter | Marks |
|---|---|---|
| `recommended_model`, `recommended_threshold` | One of the models you trained (`"baseline"`, `"linear"`, `"tree"`) and one decision threshold (0.3, 0.5 or 0.7). They must be the model and threshold your own rule and cost table chose. | 3 |
| `validation_mae` | The validation MAE of each of the three models, as your notebook computed them. | 3 |
| `test_mae`, `test_recall` | The MAE and the warning recall on the test set from your ONE opening (recall is between 0 and 1). The marking computer recomputes them from your own functions. | 2 |
| `cv_mean_mae` | The mean MAE from your group cross-validation. | 1 |
| `limits` | The letters of the **three** statements below that are **true limits of this study**. Three different letters. One mark for each true one. | 3 |
| `next_step` | One letter: the best next step. | 1 |
| `answer_choice`, `answer_test_set` | Two short written answers of 8 to 80 words each. One mark each. | 2 |

**Limits.** Choose the three statements that are TRUE and are limits of this study (some statements are false):
{lim}

**Next step.** Choose the one best next step:
{nxt}

**Written answers.** Write in your own words, in full sentences.
- `answer_choice`: {M.ANSWERS['answer_choice']['prompt']}
- `answer_test_set`: {M.ANSWERS['answer_test_set']['prompt']}

The lettering of these lists is different for each student, so a list of letters from a classmate will not match your lists.'''


MEMO_STARTER = '''#@title Part B: the decision memo form (fill in every field; do not rename a field)
MEMO = {
    "recommended_model": "",                  # "baseline", "linear" or "tree"
    "recommended_threshold": None,            # 0.3, 0.5 or 0.7
    "validation_mae": {"baseline": None, "linear": None, "tree": None},   # your validation MAE values, in UNIT
    "cv_mean_mae": None,                      # your mean cross-validated MAE, in UNIT
    "test_mae": None,                         # the test MAE from your ONE opening, in UNIT
    "test_recall": None,                      # the test recall from your ONE opening (0 to 1)
    "limits": ["", "", ""],                   # three different letters from the Limits list
    "next_step": "",                          # one letter from the Next step list
    "answer_choice": "",                      # one or two sentences
    "answer_test_set": "",                    # one or two sentences
}
'''


def memo_solution(code, v):
    """A model memo: numbers calculated from the notebook, the true limits, the right next step and two good written answers (typed as plain text)."""
    limit_opts, next_opts = options(code, v)
    limits = [letter for letter, _, ok, _ in limit_opts if ok][:3]
    nxt = [letter for letter, _, ok, _ in next_opts if ok][0]
    n = numbers(code, v)['p']['validation_mae']
    unit = COHORT[code]['unit']
    a1 = (f"I recommend the linear regression model because its validation MAE of {n['linear']:.2f} {unit} is far below the baseline model's {n['baseline']:.2f} {unit} "
          f"and below the decision tree's {n['tree']:.2f} {unit}, and it meets the client limit.")
    a2 = ("The test set is opened only once, at the end, so that it stays an honest estimate on unseen equipment; if we used it to choose or tune the model, "
          "information would leak and the test score would be optimistic.")
    return f'''MEMO = {{
    "recommended_model": chosen_model,
    "recommended_threshold": chosen_threshold,
    "validation_mae": {{name: round(value, 3) for name, value in validation_mae.items()}},
    "cv_mean_mae": round(cv_summary["mean"], 3),
    "test_mae": round(test_result["mae"], 3),
    "test_recall": round(test_result["warning"]["recall"], 3),
    "limits": {limits!r},
    "next_step": {nxt!r},
    "answer_choice": {a1!r},
    "answer_test_set": {a2!r},
}}
'''
