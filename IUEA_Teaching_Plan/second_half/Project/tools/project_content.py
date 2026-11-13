"""One source of truth for the Engineering ML project: course facts, the data, the Part A tasks (starter code and model solution),
the Part B memo form, the marks and the window rules. The notebooks, the rehearsal, the briefs and the marking guide are all built
from this file, so the numbers and names can never disagree. Numbers come from the NumPy reference, never typed.

The data (decision of 13 November 2026): one real file for every student, the UCI "Steel Industry Energy Consumption" dataset
(CC BY 4.0). It is stored inside the supplied setup cell (bzip2 and base64) and written out with a SHA-256 check, so nothing is
downloaded during the window. The rehearsal uses the same file with another target.
"""
import base64
import bz2
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

VERSION = K.VERSION
CODES = ['CML3112', 'CML3113', 'CML3111']
COHORT = {
    'CML3112': dict(name='Civil Engineering and Architecture', class3='Tuesday 17 November 2026', class4='Tuesday 24 November 2026'),
    'CML3113': dict(name='Mining and Petroleum Engineering', class3='Friday 20 November 2026', class4='Friday 27 November 2026'),
    'CML3111': dict(name='Electrical, Mechatronics, Robotics and Communications', class3='Friday 20 November 2026', class4='Friday 27 November 2026'),
}
PAYER = 'the plant\'s energy manager'
# The window (decision of 13 November 2026): the same for all three courses, online, from anywhere. Confirmed.
WINDOW = dict(opens='Monday 23 November 2026, 00:00', closes='Wednesday 25 November 2026, 23:59', last_full_start='Wednesday 25 November 2026, 20:59',
              iso_open='2026-11-23T00:00:00+03:00', iso_close='2026-11-25T23:59:00+03:00')
WINDOW_TEXT = f'opens {WINDOW["opens"]} and closes {WINDOW["closes"]} Kampala time'
SUPPORT_HOURS = '08:00 to 20:00 each day of the window (lecturer to confirm these hours)'
RESULTS_BY = 'Wednesday 2 December 2026'
MINUTES = 180
REHEARSAL_TEXT = {c: f'{COHORT[c]["class3"]}, right after Class 3' for c in COHORT}
AUTO_MARKS = K.PART_A_MAX                         # 30
PART_B = K.PART_B_MAX                             # 15
TIME_PLAN = [('Setup: open your notebook, run the first cells', 10), ('Tasks 1 and 2: clean the rows, split by month', 35),
             ('Task 3: the three models', 30), ('Task 4: warnings and the cost table', 25), ('Task 5: cross-validation by month', 15),
             ('Tasks 6 and 7: choose a model, open the test set once', 10), ('Task 8: the Part B memo form', 25),
             ('Check, restart and run all, submit', 20), ('Spare time (breaks, reconnecting)', 10)]
assert sum(m for _, m in TIME_PLAN) == MINUTES
OWN_CELLS = ('You may add your own cells. Your work is marked wherever it is, as long as the required function names exist when '
             'the notebook runs from the top.')
SOURCE = P.SOURCE
CITATION = P.CITATION
CFGS = {'exam': P.EXAM, 'rehearsal': P.REHEARSAL}
FEATURE_TEXT = {P.LAG: 'lagging reactive power (kVarh)', P.LEAD: 'leading reactive power (kVarh)', 'NSM': 'seconds since midnight',
                'weekend': '1 on Saturday and Sunday, else 0', P.USAGE: 'energy used (kWh)'}


def numbers(cfg=P.EXAM):
    p = P.pipeline(cfg)
    test = P.test_expected(p['chosen_model'], p['chosen_threshold'], cfg)
    return dict(p=p, chosen=p['chosen_model'], threshold=p['chosen_threshold'], test=test)


def options(code, v=None):
    return M.options(code)


# ------------------------------------------------------------------------------------------------ the supplied cells
def packed_data(width=100):
    data = base64.b64encode(bz2.compress(P.file_bytes(), 9)).decode('ascii')
    return '\n'.join(data[i:i + width] for i in range(0, len(data), width))


_PACKED = None


def setup_cell(cfg=P.EXAM):
    global _PACKED
    if _PACKED is None:
        _PACKED = packed_data()
    f = cfg['features']
    if cfg['key'] == 'exam':
        why = '# the power factors are left out: they are calculated from Usage_kWh and the reactive power, so they would leak the answer'
    else:
        why = '# the power factors are left out: they are calculated from the energy and the reactive power, so they would leak the answer'
    return f'''#@title Prepare the data and the libraries - Do not edit this cell
# IUEA-SETUP-CELL  (supplied: do not edit)
# Data: {SOURCE["title"]}, {SOURCE["plant"]}, 2018, one reading every 15 minutes.
# {SOURCE["authors"]} ({SOURCE["year"]}), {SOURCE["publisher"]}, {SOURCE["url"]}. Licence {SOURCE["licence"]}.
# The file is stored inside this cell (compressed), so nothing is downloaded. It is written out and checked with SHA-256.
import base64, bz2, hashlib, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, roc_auc_score

DATA_FILE = {P.DATA_NAME!r}
DATA_SHA256 = {P.DATA_SHA256!r}
_PACKED = """
{_PACKED}
"""
def _data_is_intact():
    return os.path.exists(DATA_FILE) and hashlib.sha256(open(DATA_FILE, "rb").read()).hexdigest() == DATA_SHA256
if not _data_is_intact():
    _raw = bz2.decompress(base64.b64decode("".join(_PACKED.split())))
    if hashlib.sha256(_raw).hexdigest() != DATA_SHA256:
        raise RuntimeError("The data stored in this cell is damaged. Do not edit this cell. Tell your lecturer.")
    with open(DATA_FILE, "wb") as _f:
        _f.write(_raw)

TARGET = {cfg["target"]!r}          # Question 1: {cfg["what"]}
TARGET_UNIT = {cfg["unit"]!r}
FEATURES = {f!r}
{why}; CO2(tCO2) is removed in Task 1 for the same reason
LIMIT = {cfg["limit"]!r}          # a reading is a WARNING (1) when its target is at or above this limit, in {cfg["unit"]} (invented teaching number)
MAX_MAE = {cfg["max_mae"]!r}         # the client accepts a typical prediction error (MAE) of at most this many {cfg["unit"]} (invented teaching number)
MAX_MS = {P.MAX_MS}               # and a prediction time of at most this many milliseconds (invented teaching number)
LATENCY_MS = {P.LATENCY_MS!r}   # invented teaching numbers
MISSED_COST, FALSE_ALARM_COST = {P.MISS_COST}, {P.ALARM_COST}   # invented teaching costs (a false negative costs 5, a false positive costs 1)

def records_from_table(table):
    """A list of dictionaries, one per row. Missing values (NaN) become None."""
    objects = table.astype(object)
    return objects.where(table.notna(), None).to_dict("records")

raw_table = pd.read_csv(DATA_FILE, encoding="utf-8-sig")    # the file starts with a byte-order mark: utf-8-sig removes it
all_records = records_from_table(raw_table)
development_records = [r for r in all_records if int(r["date"][3:5]) <= 10]   # January to October. November and December are the TEST SET.
print("Rows in the file:", len(raw_table))
print("Rows you may develop with (January to October):", len(development_records))
print(raw_table.head())
'''


def choose_cell():
    return '''#@title The model-choice rule - Do not edit this cell
# IUEA-CHOOSE-CELL  (supplied: do not edit)
def choose_model(candidates, max_mae, max_ms):
    """Keep the candidates with validation_mae <= max_mae and latency_ms <= max_ms. Choose the smallest validation_mae;
    break a tie by the smaller latency_ms, then by the name. Return the chosen name, or None if nobody qualifies."""
    allowed = [c for c in candidates if c["validation_mae"] <= max_mae and c["latency_ms"] <= max_ms]
    if not allowed:
        return None
    return sorted(allowed, key=lambda c: (c["validation_mae"], c["latency_ms"], c["name"]))[0]["name"]
'''


def test_cell():
    return '''#@title Open the test set (run it ONCE, at the very end) - Do not edit this cell
# IUEA-TEST-CELL  (supplied: do not edit)
import json as _json
TEST_OPEN_LOG = []
TEST_OUTCOMES = []
_TEST_FILE = "test_first_opening.json"

def open_test_set(model_name, threshold):
    """Evaluate ONE chosen model and ONE chosen decision threshold on the test set (November and December), with the functions you wrote."""
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
    cleaned = clean_rows(all_records)
    development = [r for r in cleaned if r["month"] <= 10]
    held_out = [r for r in cleaned if r["month"] >= 11]
    features = [{k: v for k, v in r.items() if k != TARGET} for r in held_out]
    actual = [r[TARGET] for r in held_out]
    errors = regression_errors(actual, fit_predict_regression(development, features)[model_name])
    probability = warning_probabilities(development, features, LIMIT)
    warning = classification_scores([1 if v >= LIMIT else 0 for v in actual], probability, threshold)
    outcome = {"model": model_name, "threshold": threshold, "n_rows": len(held_out), "mae": errors["mae"], "rmse": errors["rmse"],
               "warning": warning, "changed_after_opening": bool(changed)}
    TEST_OUTCOMES.append(outcome)
    print("Test set opened with", model_name, "and threshold", threshold, "on", len(held_out), "rows")
    print("  MAE", round(errors["mae"], 3), TARGET_UNIT, "| RMSE", round(errors["rmse"], 3), TARGET_UNIT)
    print("  warnings: precision", round(warning["precision"], 3), "recall", round(warning["recall"], 3), "F1", round(warning["f1"], 3), "AUC", round(warning["auc"], 3))
    return outcome
'''


# ------------------------------------------------------------------------------------------------ the tasks
def tasks(cfg=P.EXAM):
    """Part A tasks. Each: key, title, week, marks (automatic), intro (markdown), cells: list of (starter, solution) code pairs."""
    u, t = cfg['unit'], cfg['target']
    x = cfg['features'][0]
    marks = dict(K.PARTS)
    out = []
    out.append(dict(key='clean', title='Clean the rows and look at them', week='Weeks 3 to 7', marks=dict(clean=marks['clean']), intro=f'''A **record** is one row written as a dictionary, with the column names of the file as keys. A missing value is `None`.

What is really in this file (checked before the project): no missing cells and no repeated rows, but three things you must handle.
- Each day's **last** reading is written with that day's date and the time `00:00` (for example `01/01/2018 00:00` comes straight after `01/01/2018 23:45`). Its real time is midnight at the **end** of that day, so one day must be added to its timestamp.
- One reading (7 November) has every measurement 0: the meter recorded nothing.
- `CO2(tCO2)` is calculated from `Usage_kWh`, so keeping it would leak the answer (data leakage).

`clean_rows(records)` returns a cleaned **copy** of the records, in the same order. For each record:
- make `timestamp`, a text `"YYYY-MM-DD HH:MM"` from `date` (format `"%d/%m/%Y %H:%M"`), with one day added when the time is 00:00; make `month`, the month **as written** in `date` (1 to 12); make `weekend`, `1` when `WeekStatus` is `"Weekend"`, else `0`;
- if the timestamp was already seen, skip the row (keep only the first);
- drop the row if `TARGET` is `None`, or if `Usage_kWh` and both power factors are all 0 (nothing recorded), or if a value is impossible: `Usage_kWh` or either reactive power below 0, a power factor below 0 or above 100 (0 and 100 are valid), `NSM` below 0 or above 85500;
- remove the key `CO2(tCO2)`. Do not fill a missing value: it stays `None`, and the models do the imputation later from the training set only.

The marking checks give your function other rows that contain these problems and others, so write every rule even if this file does not need it. Never change the list you were given. Then use your function on the development rows and draw **Chart 1**: `{x}` across, `{t}` up, with a title, both axis names and the unit ({u}).''',
                     cells=[('''def clean_rows(records):
    """Return a cleaned copy of the records (see the task text above)."""
    # TODO 1: make an empty list called kept and an empty set called seen.
    # TODO 2: loop over records. when = datetime.strptime(record["date"], "%d/%m/%Y %H:%M"); month = when.month
    #         if when.hour == 0 and when.minute == 0: when = when + timedelta(days=1)
    #         timestamp = when.strftime("%Y-%m-%d %H:%M"). If timestamp is in seen, skip the row (continue); otherwise add it to seen.
    # TODO 3: skip the row if record[TARGET] is None, if nothing was recorded, or if a value is impossible (see the task text).
    # TODO 4: row = a copy of record without "CO2(tCO2)"; add row["timestamp"], row["month"] and row["weekend"]; add row to kept.
    return None   # TODO 5: return kept instead
''', '''def clean_rows(records):
    """Return a cleaned copy of the records (see the task text above)."""
    seen, kept = set(), []
    for record in records:
        when = datetime.strptime(record["date"], "%d/%m/%Y %H:%M")
        month = when.month
        if when.hour == 0 and when.minute == 0:
            when = when + timedelta(days=1)
        timestamp = when.strftime("%Y-%m-%d %H:%M")
        if timestamp in seen:
            continue
        seen.add(timestamp)
        if record[TARGET] is None:
            continue
        if record["Usage_kWh"] == 0 and record["Lagging_Current_Power_Factor"] == 0 and record["Leading_Current_Power_Factor"] == 0:
            continue
        if any(record[c] is not None and record[c] < 0 for c in ["Usage_kWh", "Lagging_Current_Reactive.Power_kVarh", "Leading_Current_Reactive_Power_kVarh"]):
            continue
        if any(record[c] is not None and not 0 <= record[c] <= 100 for c in ["Lagging_Current_Power_Factor", "Leading_Current_Power_Factor"]):
            continue
        if record["NSM"] is not None and not 0 <= record["NSM"] <= 85500:
            continue
        row = {k: v for k, v in record.items() if k != "CO2(tCO2)"}
        row["timestamp"], row["month"] = timestamp, month
        row["weekend"] = 1 if record["WeekStatus"] == "Weekend" else 0
        kept.append(row)
    return kept
'''),
                            ('''development_rows = None      # TODO: call clean_rows on development_records
print("Rows kept:", None)    # TODO: replace None with the number of rows in development_rows

figure, axes = plt.subplots()
# TODO: axes.scatter(...): FEATURES[0] on the x axis, TARGET on the y axis, small points (s=2) (hint: table = pd.DataFrame(development_rows))
# TODO: axes.set_title(...), axes.set_xlabel(...) and axes.set_ylabel(...). Write the unit in the y label.
chart_1 = figure
plt.show()
''', f'''development_rows = clean_rows(development_records)
print("Rows kept:", len(development_rows))

figure, axes = plt.subplots()
table = pd.DataFrame(development_rows)
axes.scatter(table[FEATURES[0]], table[TARGET], s=2)
axes.set_title("Chart 1: {cfg['short']} against {FEATURE_TEXT[x].split(' (')[0]}")
axes.set_xlabel("{FEATURE_TEXT[x][0].upper() + FEATURE_TEXT[x][1:]}")
axes.set_ylabel("{cfg['short'].capitalize()} ({u})")
chart_1 = figure
plt.show()
''')]))

    out.append(dict(key='split', title='Split by month', week='Week 10', marks=dict(split=marks['split']), intro='''`time_split(records)` receives cleaned records and returns a dictionary with three lists of `timestamp` values, each in the order the records came in:
- `"train"`: months 1 to 8, January to August (the **training set**);
- `"validation"`: months 9 and 10, September and October (the **validation set**);
- `"test"`: months 11 and 12, November and December (the **test set**).

**Why not a random split?** Readings 15 minutes apart are almost the same. A random split puts near-copies of the same hour in the training set and the validation set, and lets the model learn from days that come after the ones it is tested on. The score would look better than it will be on next month. Splitting by month keeps whole months apart and keeps the future in the future. Your development rows have no November or December rows, so their `"test"` list is empty. That is correct.

When you pick the training and validation rows, look the timestamps up in a **set**. Looking each one up in a list of 23,000 timestamps makes the cell run for minutes, and the marking computer stops a cell after 30 seconds.''',
                     cells=[('''def time_split(records):
    """Return {"train": [...], "validation": [...], "test": [...]} (lists of timestamp, in input order)."""
    # TODO: for each record, look at record["month"] and put record["timestamp"] in the right list.
    return None
''', '''def time_split(records):
    """Return {"train": [...], "validation": [...], "test": [...]} (lists of timestamp, in input order)."""
    groups = {"train": [1, 2, 3, 4, 5, 6, 7, 8], "validation": [9, 10], "test": [11, 12]}
    return {name: [r["timestamp"] for r in records if r["month"] in months] for name, months in groups.items()}
'''),
                            ('''split_ids = None     # TODO: time_split(development_rows)
train_ids, valid_ids = None, None   # TODO: set(split_ids["train"]) and set(split_ids["validation"]) (a set makes the look-up fast)
train_rows = None    # TODO: the development rows whose timestamp is in train_ids
valid_rows = None    # TODO: the development rows whose timestamp is in valid_ids
print("Training rows:", None, "| validation rows:", None)   # TODO: replace the Nones with the two counts
''', '''split_ids = time_split(development_rows)
train_ids, valid_ids = set(split_ids["train"]), set(split_ids["validation"])
train_rows = [r for r in development_rows if r["timestamp"] in train_ids]
valid_rows = [r for r in development_rows if r["timestamp"] in valid_ids]
print("Training rows:", len(train_rows), "| validation rows:", len(valid_rows))
''')]))

    feats = ', '.join(f'`{c}`' for c in cfg['features'])
    out.append(dict(key='regression', title='Question 1: a baseline model, a linear regression and a decision tree', week='Weeks 8 and 9', marks=dict(regression=marks['regression'], errors=marks['errors']),
                     intro=f'''**Question 1.** How much is {cfg['what']}, in {u}, for months the model has never seen?

`fit_predict_regression(training_records, feature_records)` trains (fits) three models on the training records and predicts for the feature records. Use the columns in `FEATURES` ({feats}), in that order. The feature records have **no target**.
- every model is a pipeline that first does **imputation** of missing values with the **median of the training rows** (`SimpleImputer(strategy="median")`), then fits;
- `"baseline"`: the baseline model, which always predicts the mean training target (`DummyRegressor`);
- `"linear"`: multiple linear regression, `LinearRegression`;
- `"tree"`: a decision tree, `DecisionTreeRegressor(max_depth=4, random_state=17)`. The `max_depth` is a **hyperparameter**: a setting you choose before training.

Return a dictionary with three lists of predictions, in the order of the feature records. The baseline model must use the **training** rows only: a baseline built with validation or test targets has **leaked**.

`regression_errors(actual, predicted)` returns `{{"mae": ..., "rmse": ...}}` over the same pairs, not rounded. A **residual** is actual minus predicted. MAE (mean absolute error) is the mean of the absolute residuals. RMSE (root mean squared error) is the square root of the mean of the squared residuals.''',
                     cells=[('''def fit_predict_regression(training_records, feature_records):
    """Return {"baseline": [...], "linear": [...], "tree": [...]}."""
    # TODO 1: table = pd.DataFrame(training_records); new = pd.DataFrame(feature_records)
    # TODO 2: X_train = table[FEATURES]; y_train = table[TARGET]; X_new = new[FEATURES].
    # TODO 3: a dictionary of three pipelines. Each is make_pipeline(SimpleImputer(strategy="median"), <the model>).
    # TODO 4: loop over the dictionary: fit on (X_train, y_train), predict X_new, and store the predictions as a list of floats under the model's name.
    return None
''', '''def fit_predict_regression(training_records, feature_records):
    """Return {"baseline": [...], "linear": [...], "tree": [...]}."""
    table, new = pd.DataFrame(training_records), pd.DataFrame(feature_records)
    X_train, y_train, X_new = table[FEATURES].astype(float), table[TARGET], new[FEATURES].astype(float)
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
                            ('''# Evaluate the three models on the validation set (September and October). Keep the names: validation_predictions, validation_mae and validation_rmse.
validation_features = None    # TODO: the validation rows without the TARGET key
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
''', f'''validation_features = [{{k: v for k, v in r.items() if k != TARGET}} for r in valid_rows]
validation_actual = [r[TARGET] for r in valid_rows]
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

    reason = ('A quarter hour at or above 60 kWh means the plant is drawing at least 240 kW on average, which is when peak-demand charges build up. '
              'The column `Load_Type` is not used for the warning: it follows the clock (a time-of-day band), so it says nothing about what the meter measured.'
              if cfg['key'] == 'exam' else 'A high lagging reactive power is when the plant is most likely to pay a power-factor penalty.')
    out.append(dict(key='warning', title='Question 2: which readings should raise a warning?', week='Weeks 9 and 10', marks=dict(warning=marks['warning'], scores=marks['scores']),
                     intro=f'''**Question 2.** A reading is a **warning** (1, the positive class) when its `{t}` is at or above `LIMIT` ({cfg['limit']:g} {u}) and **no warning** (0, the negative class) below it. {reason} The limit is an invented teaching number. Which readings should raise a warning?

`warning_probabilities(training_records, feature_records, limit)` returns the probability of a warning, for each feature record, from a pipeline of `SimpleImputer(strategy="median")`, `StandardScaler()` and `LogisticRegression(max_iter=1000)` (binary classification), fitted on the training records only. The label is `1` when the training target is `>= limit`. Use the columns in `FEATURES`.

`classification_scores(actual, probability, threshold)` predicts a warning when the probability is `>= threshold` (the **decision threshold**), then returns a dictionary with the confusion matrix counts `tp`, `fp`, `fn`, `tn` (true positives, false positives, false negatives, true negatives) and `precision`, `recall`, `f1`, `cost` and `auc`. A false negative (a missed warning) costs `MISSED_COST` and a false positive (a false alarm) costs `FALSE_ALARM_COST` (invented teaching costs), so `cost = 5 * fn + 1 * fp`. When a ratio has a zero denominator, use 0. `auc` is the ROC AUC of the probabilities and does not depend on the threshold.

Then try decision thresholds 0.3, 0.5 and 0.7 on the validation set, and keep the one with the lowest cost as `chosen_threshold` (if two tie, take the higher one).''',
                     cells=[('''def warning_probabilities(training_records, feature_records, limit):
    """Return a list of warning probabilities, one per feature record."""
    # TODO 1: tables as before; y_train = (training target >= limit) turned into 0 and 1 (astype(int)).
    # TODO 2: model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000)); fit it on table[FEATURES].
    # TODO 3: predict_proba(new[FEATURES]) gives two columns: column 1 is the probability of a warning. Return it as a list of floats.
    return None
''', '''def warning_probabilities(training_records, feature_records, limit):
    """Return a list of warning probabilities, one per feature record."""
    table, new = pd.DataFrame(training_records), pd.DataFrame(feature_records)
    y_train = (table[TARGET] >= limit).astype(int)
    model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000))
    model.fit(table[FEATURES].astype(float), y_train)
    return [float(v) for v in model.predict_proba(new[FEATURES].astype(float))[:, 1]]
'''),
                            ('''def classification_scores(actual, probability, threshold):
    """Return tp, fp, fn, tn, precision, recall, f1, cost and auc."""
    # TODO 1: predicted = 1 where the probability is at or above the threshold, else 0 (a list comprehension).
    # TODO 2: tn, fp, fn, tp = confusion_matrix(actual, predicted, labels=[0, 1]).ravel()   (see Class 2)
    # TODO 3: precision_score, recall_score and f1_score with zero_division=0; roc_auc_score(actual, probability).
    # TODO 4: cost = MISSED_COST * fn + FALSE_ALARM_COST * fp. Turn numpy numbers into int() and float() before returning.
    return None
''', '''def classification_scores(actual, probability, threshold):
    """Return tp, fp, fn, tn, precision, recall, f1, cost and auc."""
    predicted = [1 if p >= threshold else 0 for p in probability]
    tn, fp, fn, tp = confusion_matrix(actual, predicted, labels=[0, 1]).ravel()
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
''', '''warning_actual = [1 if r[TARGET] >= LIMIT else 0 for r in valid_rows]
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

    out.append(dict(key='monthcv', title='Can you trust it? Cross-validation by month', week='Week 10', marks=dict(monthcv=marks['monthcv']), intro='''One validation set of two months can mislead. **Cross-validation by month** (group K-fold cross-validation where each group is one month, the idea of `GroupKFold`) gives each month a turn as the unseen month.

`month_cv_mae(records)` receives clean records with **no missing values**. Hold out each month from 1 to 10 in turn (January to October; months 11 and 12 are never used). For each fold, fit `LinearRegression` on `FEATURES` using the other nine months, and compute the MAE on the held-out month. Return `{"folds": [...], "mean": ..., "spread": ...}`: the ten MAEs in month order, their mean, and their sample standard deviation (`ddof=1`). Do not round.

**Data leakage check, in your own head:** the imputer, the StandardScaler (standardisation) and the baseline model's mean are all fitted on the training rows only. If any of them had seen validation or test rows, the scores would look better than they are.''',
                     cells=[('''def month_cv_mae(records):
    """Return {"folds": [ten MAEs, January to October], "mean": ..., "spread": ...}."""
    # TODO 1: table = pd.DataFrame(records); keep only the rows whose month is 1 to 10.
    # TODO 2: for month in range(1, 11): train = the rows of the OTHER months, test = the rows of this month.
    # TODO 3: fit LinearRegression on train[FEATURES]; the MAE on test is np.mean(np.abs(...)).
    # TODO 4: mean = np.mean(folds); spread = np.std(folds, ddof=1).
    return None
''', '''def month_cv_mae(records):
    """Return {"folds": [ten MAEs, January to October], "mean": ..., "spread": ...}."""
    table = pd.DataFrame(records)
    table = table[table["month"].between(1, 10)]
    folds = []
    for month in range(1, 11):
        train, test = table[table["month"] != month], table[table["month"] == month]
        model = LinearRegression().fit(train[FEATURES].astype(float), train[TARGET])
        folds.append(float(np.mean(np.abs(test[TARGET] - model.predict(test[FEATURES].astype(float))))))
    return {"folds": folds, "mean": float(np.mean(folds)), "spread": float(np.std(folds, ddof=1))}
'''),
                            ('''complete_rows = None    # TODO: the development rows with no missing value in FEATURES or TARGET
cv_summary = None       # TODO: month_cv_mae(complete_rows)
print("Cross-validated MAE (" + TARGET_UNIT + "):", cv_summary)
''', '''complete_rows = [r for r in development_rows if all(r[c] is not None for c in FEATURES + [TARGET])]
cv_summary = month_cv_mae(complete_rows)
print("Cross-validated MAE (" + TARGET_UNIT + "):", cv_summary)
''')]))

    out.append(dict(key='choose', title='Choose one model with the supplied rule', week='Week 10', marks={}, intro=f'''The model-choice rule is supplied (the cell below says Do not edit this cell). Run it, then use it. The rule: keep the models whose validation MAE is at most `MAX_MAE` **and** whose prediction time is at most `MAX_MS` (both limits included); among those, choose the smallest validation MAE; break a tie by the shorter time, then by the name. If no model qualifies, the rule returns `None`. Never use the test set to choose.

The client for this project is {PAYER}. The client accepts a typical prediction error of at most `MAX_MAE` ({cfg['max_mae']:g} {u}) and a prediction time of at most `MAX_MS` ({P.MAX_MS} ms). Both numbers are invented for teaching.

Your part: build `candidate_table`, one dictionary per model with `name`, `validation_mae` (your own Task 3 value) and `latency_ms` (from `LATENCY_MS`), and call `choose_model(candidate_table, MAX_MAE, MAX_MS)`.''',
                     cells=[('__CHOOSE__', '__CHOOSE__'),
                            ('''candidate_table = []     # TODO: one dictionary per model (baseline, linear, tree): name, validation_mae (from your Task 3 results), latency_ms (from LATENCY_MS)
chosen_model = None      # TODO: choose_model(candidate_table, MAX_MAE, MAX_MS)
print(candidate_table)
print("Chosen model:", chosen_model)
''', '''candidate_table = [{"name": name, "validation_mae": validation_mae[name], "latency_ms": LATENCY_MS[name]} for name in ("baseline", "linear", "tree")]
chosen_model = choose_model(candidate_table, MAX_MAE, MAX_MS)
print(candidate_table)
print("Chosen model:", chosen_model)
''')]))

    out.append(dict(key='test', title='Open the test set, once', week='Week 10', marks=dict(test=marks['test']), intro='''November and December are the **test set**: two months that nothing so far has used. They give **one** honest estimate for the model you chose.

How it works. The supplied cell below is marked Do not edit this cell. Run it once to define `open_test_set(model_name, threshold)`. Then call it **one time**, with the model you chose in Task 6 and the decision threshold you chose in Task 4. It cleans the whole file with your `clean_rows`, trains your functions on all the development months (January to October), evaluates on November and December, prints the result and writes your choice to a small file. If you call it again, the notebook counts a second opening: you lose the "opened once" mark even when the choice is the same, and you lose more if the choice is different.

You must not use November or December to choose a model, a threshold or anything else, and you must not look at them before this call. Report whatever the result is in your Part B form.''',
                     cells=[('__TEST__', '__TEST__'),
                            ('''test_result = None     # TODO: open_test_set(chosen_model, chosen_threshold)
''', '''test_result = open_test_set(chosen_model, chosen_threshold)
''')]))
    return out


# ------------------------------------------------------------------------------------------------ the self-check cell (visible)
SELF_CHECK = '''# This cell is a SELF-CHECK. It is not marked. It uses tiny examples with known answers, so you can see at once if a function is wrong.
# The marked (hidden) checks run your functions on OTHER rows you cannot see, so passing here does not mean full marks.
def _try(label, test):
    try:
        ok = bool(test())
    except Exception as error:
        ok = False
    print(("PASS  " if ok else "TODO  ") + label)
    return ok

def _row(date, usage, lag=2.0, lead=0.0, lpf=90.0, dpf=100.0, week="Weekday"):
    h, m = int(date[11:13]), int(date[14:16])
    return {"date": date, "Usage_kWh": usage, "Lagging_Current_Reactive.Power_kVarh": lag, "Leading_Current_Reactive_Power_kVarh": lead,
            "CO2(tCO2)": 0.0, "Lagging_Current_Power_Factor": lpf, "Leading_Current_Power_Factor": dpf, "NSM": h * 3600 + m * 60,
            "WeekStatus": week, "Day_of_week": "Monday", "Load_Type": "Light_Load"}
_small = [_row("01/01/2018 23:45", 3.0), _row("01/01/2018 00:00", 3.5), _row("01/01/2018 00:00", 9.9), _row("02/01/2018 00:15", 4.0),
          _row("02/01/2018 00:30", 0.0, 0.0, 0.0, 0.0, 0.0), _row("09/09/2018 10:00", 50.0, week="Weekend"), _row("20/11/2018 12:00", 40.0, lpf=101.0)]
_small[3][TARGET] = None
_ts = ["2018-01-01 23:45", "2018-01-02 00:00", "2018-09-09 10:00"]
_checks = []
_checks.append(_try("clean_rows keeps 3 rows, in order, with the midnight reading moved to the next day",
                    lambda: [r["timestamp"] for r in clean_rows(_small)] == _ts))
_checks.append(_try("clean_rows adds month (as written) and weekend, and removes CO2(tCO2)",
                    lambda: [r["month"] for r in clean_rows(_small)] == [1, 1, 9] and [r["weekend"] for r in clean_rows(_small)] == [0, 0, 1]
                    and all("CO2(tCO2)" not in r for r in clean_rows(_small))))
_checks.append(_try("clean_rows does not change the list you give it", lambda: (len(_small) == 7 and "CO2(tCO2)" in _small[0] and clean_rows(_small) is not _small)))
_checks.append(_try("time_split puts January in train, September in validation",
                    lambda: time_split(clean_rows(_small)) == {"train": _ts[:2], "validation": _ts[2:], "test": []}))
_toy = [dict({f: float(i) for f in FEATURES}, **{TARGET: 2.0 * i, "month": 1, "timestamp": "2018-01-0%d 10:00" % i}) for i in range(1, 7)]
_new = [dict({f: 3.5 for f in FEATURES}, **{FEATURES[0]: None, "month": 9, "timestamp": "2018-09-01 10:00"})]
_checks.append(_try("fit_predict_regression returns baseline, linear and tree, one prediction per feature record",
                    lambda: sorted(fit_predict_regression(_toy, _new)) == ["baseline", "linear", "tree"] and all(len(v) == 1 for v in fit_predict_regression(_toy, _new).values())))
_checks.append(_try("the baseline model predicts the mean of the TRAINING targets (7.0)", lambda: abs(fit_predict_regression(_toy, _new)["baseline"][0] - 7.0) < 1e-9))
_checks.append(_try("regression_errors([1, 3], [2, 5]) has mae 1.5 and rmse sqrt(2.5)",
                    lambda: abs(regression_errors([1, 3], [2, 5])["mae"] - 1.5) < 1e-9 and abs(regression_errors([1, 3], [2, 5])["rmse"] - 2.5 ** 0.5) < 1e-9))
_checks.append(_try("classification_scores on a known case (tp 1, fp 1, fn 1, tn 1, cost 6, auc 0.75)",
                    lambda: (lambda s: (s["tp"], s["fp"], s["fn"], s["tn"], s["cost"], round(s["auc"], 2)) == (1, 1, 1, 1, 6, 0.75))(classification_scores([1, 0, 1, 0], [0.9, 0.8, 0.2, 0.1], 0.5))))
_checks.append(_try("warning_probabilities gives numbers between 0 and 1",
                    lambda: all(0 <= p <= 1 for p in warning_probabilities(_toy, _new, 8.0))))
_checks.append(_try("month_cv_mae returns ten folds, a mean and a spread",
                    lambda: len(month_cv_mae(complete_rows)["folds"]) == 10 and {"mean", "spread"} <= set(month_cv_mae(complete_rows))))
for _name in ["validation_mae", "cv_summary", "warning_auc", "candidate_table", "chosen_model", "chosen_threshold"]:
    _checks.append(_try("the variable " + _name + " has been calculated (it is not None)", lambda: globals().get(_name) is not None))
_checks.append(_try("the test set has been opened exactly once", lambda: len(TEST_OPEN_LOG) == 1))
_checks.append(_try("Chart 1 and Chart 2 each have a title, named axes and the unit",
                    lambda: all(f.axes[0].get_title() and f.axes[0].get_xlabel() and TARGET_UNIT.lower() in f.axes[0].get_ylabel().lower() for f in (chart_1, chart_2))))
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


def memo_markdown(code, cfg=P.EXAM, task_no=8):
    limit_opts, next_opts = options(code)
    lim = '\n'.join(f'- **{letter}.** {text}' for letter, text, _, _ in limit_opts)
    nxt = '\n'.join(f'- **{letter}.** {text}' for letter, text, _, _ in next_opts)
    return f'''## Task {task_no}: Part B, the decision memo form ({K.PART_B_MAX} automatic marks)
Your memo is a **form**. You write it for **{PAYER}**. Fill in the dictionary `MEMO` in the next cell. Every value is checked by the marking computer; nothing is read by a person. Use your own numbers, with at least two decimals, in **{cfg['unit']}**.

| Field | What to enter | Marks |
|---|---|---|
| `recommended_model`, `recommended_threshold` | One of the models you trained (`"baseline"`, `"linear"`, `"tree"`) and one decision threshold (0.3, 0.5 or 0.7). They must be the model and threshold your rule and cost table chose. | 3 |
| `validation_mae` | The validation MAE of each of the three models, as your notebook computed them. | 3 |
| `test_mae`, `test_recall` | The MAE and the warning recall on the test set from your ONE opening (recall is between 0 and 1). The marking computer recomputes them from your own functions. | 2 |
| `cv_mean_mae` | The mean MAE from your cross-validation by month. | 1 |
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

Each course has its own lettering of these lists.'''


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

NAMES_OF = {'baseline': 'baseline model', 'linear': 'linear regression', 'tree': 'decision tree'}


def memo_solution(code, cfg=P.EXAM):
    """A model memo: numbers calculated from the notebook, the true limits, the right next step and two good written answers (typed as plain text)."""
    limit_opts, next_opts = options(code)
    limits = [letter for letter, _, ok, _ in limit_opts if ok][:3]
    nxt = [letter for letter, _, ok, _ in next_opts if ok][0]
    n = numbers(cfg)
    vm, chosen, unit = n['p']['validation_mae'], n['chosen'], cfg['unit']
    others = [m for m in ('baseline', 'linear', 'tree') if m != chosen]
    a1 = (f"I recommend the {NAMES_OF[chosen]} because its validation MAE of {vm[chosen]:.2f} {unit} on September and October is lower than the "
          f"{NAMES_OF[others[0]]} ({vm[others[0]]:.2f} {unit}) and the {NAMES_OF[others[1]]} ({vm[others[1]]:.2f} {unit}), and it meets the client limit.")
    a2 = ("The test set is opened only once, at the end, so that it stays an honest estimate on months the model has never seen; if we used it to choose or tune the model, "
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
