"""One source of truth for the Engineering ML project: course facts, the data, the tasks (text, starter and model solution), the
Part B memo form, the marks and the window rules. The notebooks, the rehearsal, the briefs and the marking guide are built from this file.

Plain code (lecturer's redesign of 14 November 2026): students write ordinary straight-line code, no function placeholders. Each task
names its INPUT variables and the RESULT names to store. The grader re-runs each task's cells on hidden inputs (own_cells.py).
ONE supplied code cell, "Setup: run me first": the data (the development rows as in the file, and the cleaned test rows) packed inside it
with a SHA-256 check, the constants, choose_model, open_test_set, the silent backup and the countdown line after every cell.
"""
import base64
import bz2
import csv
import hashlib
import io
import json
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
TIME_PLAN = [('Run the setup cell', 5), ('Task 1: clean the data, Chart 1', 40), ('Task 2: split by month', 10),
             ('Task 3: three models, MAE and RMSE, Chart 2', 40), ('Task 4: warnings', 15), ('Tasks 5 and 6: choose, open the test set', 15),
             ('Task 7: MEMO form', 25), ('Restart and run all, Check my work', 20), ('Spare', 10)]
assert sum(m for _, m in TIME_PLAN) == MINUTES
OWN_CELLS = 'Add as many cells as you like under a task; plain code is fine (no functions needed).'
SOURCE = P.SOURCE
CITATION = P.CITATION
CFGS = {'exam': P.EXAM, 'rehearsal': P.REHEARSAL}
SETUP_TITLE = '#@title Setup: run me first'
SETUP_MARKER = '# IUEA-SETUP-CELL'
IDENTITY_LINE = '_IUEA_IDENTITY = {}'


def numbers(cfg=P.EXAM):
    p = P.pipeline(cfg)
    test = P.test_expected(p['chosen_model'], cfg)
    return dict(p=p, chosen=p['chosen_model'], threshold=P.THRESHOLD, test=test)


def options(code, v=None):
    return M.options(code)


# ------------------------------------------------------------------------------------------------ the data inside the setup cell
TEST_COLUMNS = [c for c in P.COLUMNS if c != P.CO2] + ['timestamp', 'month', 'weekend']


def csv_text(rows, columns):
    out = io.StringIO()
    w = csv.writer(out, lineterminator='\n')
    w.writerow(columns)
    for r in rows:
        w.writerow(['' if r.get(c) is None else r.get(c) for c in columns])
    return out.getvalue()


def data_payload():
    """The development rows exactly as written in the file (January to October, as dated) and the cleaned test rows (November and December)."""
    lines = P.file_bytes().decode('utf-8-sig').splitlines()
    dev = [lines[0]] + [l for l in lines[1:] if int(l.split(',')[0][3:5]) <= 10]
    test = P.pipeline(P.EXAM)['test']
    return json.dumps({'development': '\n'.join(dev) + '\n', 'test': csv_text(test, TEST_COLUMNS)}, separators=(',', ':')).encode()


def data_sha():
    return hashlib.sha256(data_payload()).hexdigest()


def packed_data(width=100):
    data = base64.b64encode(bz2.compress(data_payload(), 9)).decode('ascii')
    return '\n'.join(data[i:i + width] for i in range(0, len(data), width))


_PACKED = None


def setup_cell(cfg=P.EXAM, code='CML3112', test_id='ML_PROJECT'):
    global _PACKED
    if _PACKED is None:
        _PACKED = packed_data()
    import pipeline_cells as PL
    identity = json.dumps({'course': code, 'test': test_id})
    return f"""{SETUP_TITLE}
{SETUP_MARKER} (supplied). Run it first, and again after a restart. The marking computer always uses the original of this cell.
{IDENTITY_LINE[:-2]}{identity}
import base64, bz2, hashlib, io, json, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import confusion_matrix, precision_score, recall_score
FULL_NAME = _IUEA_IDENTITY.get("name", "")
STUDENT_ID = _IUEA_IDENTITY.get("registration", "")
COHORT = _IUEA_IDENTITY.get("course", "")
TEST_ID = _IUEA_IDENTITY.get("test", "")
_IUEA_ALLOCATION = _IUEA_IDENTITY.get("allocation", "")
_IUEA_DEADLINE = _IUEA_IDENTITY.get("deadline", "")
_PACKED = '''
{_PACKED}
'''
_bytes = bz2.decompress(base64.b64decode("".join(_PACKED.split())))
if hashlib.sha256(_bytes).hexdigest() != {data_sha()!r}:
    raise RuntimeError("The data in this cell is damaged. Tell your lecturer.")
_data = json.loads(_bytes)
TARGET = {cfg["target"]!r}
TARGET_UNIT = {cfg["unit"]!r}
FEATURES = {cfg["features"]!r}
LIMIT = {cfg["limit"]!r}
THRESHOLD = {P.THRESHOLD}
MAX_MAE, MAX_MS = {cfg["max_mae"]!r}, {P.MAX_MS}
LATENCY_MS = {P.LATENCY_MS!r}
raw = pd.read_csv(io.StringIO(_data["development"]))
_TEST_ROWS = pd.read_csv(io.StringIO(_data["test"]))
def choose_model(maes):
    ok = [m for m in maes if maes[m] is not None and maes[m] <= MAX_MAE and LATENCY_MS[m] <= MAX_MS]
    return min(ok, key=lambda m: (maes[m], LATENCY_MS[m], m)) if ok else None
TEST_OPEN_LOG = []
def open_test_set(model_name):
    if model_name not in ("baseline", "linear", "tree"):
        raise ValueError('use "baseline", "linear" or "tree"')
    if TEST_OPEN_LOG or os.path.exists("test_opened.json"):
        print("WARNING: THE TEST SET WAS ALREADY OPENED. Opening it again means it is no longer an honest test.")
    json.dump({{"model": model_name}}, open("test_opened.json", "w"))
    TEST_OPEN_LOG.append([model_name, THRESHOLD])
    return _TEST_ROWS.copy()
print("raw:", raw.shape, "| TARGET:", TARGET, "| FEATURES:", FEATURES)
""" + PL.backup_code() + PL.countdown_code()


# ------------------------------------------------------------------------------------------------ the tasks
def tasks(cfg=P.EXAM):
    """Each task: key, title, marks (dict of Part A items), text (two or three lines), inputs, results, starter, solution, alternative."""
    u, t = cfg['unit'], cfg['target']
    marks = dict(K.PARTS)
    x = cfg['features'][0]
    out = []
    out.append(dict(key='clean', title='Clean the data', marks=dict(clean=marks['clean']), inputs=['raw'], results=['clean'],
        text=(f'Make `clean` from `raw`, rows in the same order: add `timestamp` from `date` (`%d/%m/%Y %H:%M`, plus one day when the time is 00:00), '
              '`month` (the month as written in `date`) and `weekend` (1 when `WeekStatus` is "Weekend", else 0); drop the column `CO2(tCO2)`.\n'
              'Drop a repeated `timestamp` (keep the first), a missing `TARGET`, the all-zero reading (`Usage_kWh` and both power factors 0), and impossible values '
              '(energy or reactive power below 0, a power factor outside 0 to 100, `NSM` outside 0 to 85500). Do not change `raw`.\n'
              f'Chart 1: a scatter of `{x}` (across) against `TARGET` (up) from `clean`, with a title, both axis names and the unit ({u}).'),
        solution=f'''clean = raw.copy()
when = pd.to_datetime(clean["date"], format="%d/%m/%Y %H:%M")
clean["month"] = when.dt.month
midnight = (when.dt.hour == 0) & (when.dt.minute == 0)
clean["timestamp"] = (when + pd.to_timedelta(midnight.astype(int), unit="D")).dt.strftime("%Y-%m-%d %H:%M")
clean["weekend"] = (clean["WeekStatus"] == "Weekend").astype(int)
clean = clean.drop(columns=["CO2(tCO2)"])
clean = clean.drop_duplicates(subset="timestamp", keep="first")
nothing = (clean["Usage_kWh"] == 0) & (clean["Lagging_Current_Power_Factor"] == 0) & (clean["Leading_Current_Power_Factor"] == 0)
negative = (clean["Usage_kWh"] < 0) | (clean["Lagging_Current_Reactive.Power_kVarh"] < 0) | (clean["Leading_Current_Reactive_Power_kVarh"] < 0)
bad_pf = ~clean["Lagging_Current_Power_Factor"].between(0, 100) & clean["Lagging_Current_Power_Factor"].notna()
bad_pf = bad_pf | (~clean["Leading_Current_Power_Factor"].between(0, 100) & clean["Leading_Current_Power_Factor"].notna())
bad_nsm = ~clean["NSM"].between(0, 85500) & clean["NSM"].notna()
clean = clean[clean[TARGET].notna() & ~nothing & ~negative & ~bad_pf & ~bad_nsm]
print("rows kept:", len(clean))

plt.figure()
plt.scatter(clean[FEATURES[0]], clean[TARGET], s=2)
plt.title("Chart 1: {cfg['short']} against {x}")
plt.xlabel("{x}")
plt.ylabel("{cfg['short']} ({u})")
plt.show()
'''))
    out.append(dict(key='split', title='Split by month', marks=dict(split=marks['split']), inputs=['clean'], results=['train', 'valid'],
        text='Make `train` (months 1 to 8) and `valid` (months 9 and 10) from `clean`, rows in the same order. Use `month`, never a random split.',
        solution='''train = clean[clean["month"] <= 8]
valid = clean[clean["month"].isin([9, 10])]
print(len(train), len(valid))
'''))
    out.append(dict(key='regression', title='Three models, MAE and RMSE', marks=dict(regression=marks['regression'], errors=marks['errors'], leakage=marks['leakage'], charts=marks['charts']),
        inputs=['train', 'valid'], results=['baseline_pred', 'linear_pred', 'tree_pred', 'baseline_mae', 'linear_mae', 'tree_mae', 'baseline_rmse', 'linear_rmse', 'tree_rmse'],
        text=('Fit each model on `train` only (columns `FEATURES`, target `TARGET`) and predict `valid`: `make_pipeline(SimpleImputer(strategy="median"), model)` with '
              '`DummyRegressor()`, `LinearRegression()` and `DecisionTreeRegressor(max_depth=4, random_state=17)`.\n'
              'Then the MAE and RMSE of each on `valid`.\n'
              f'Chart 2: a bar chart of the three MAE values, with a title, both axis names and the unit ({u}).'),
        solution='''X_train, y_train = train[FEATURES], train[TARGET]
X_valid, y_valid = valid[FEATURES], valid[TARGET]
baseline = make_pipeline(SimpleImputer(strategy="median"), DummyRegressor()).fit(X_train, y_train)
linear = make_pipeline(SimpleImputer(strategy="median"), LinearRegression()).fit(X_train, y_train)
tree = make_pipeline(SimpleImputer(strategy="median"), DecisionTreeRegressor(max_depth=4, random_state=17)).fit(X_train, y_train)
baseline_pred, linear_pred, tree_pred = baseline.predict(X_valid), linear.predict(X_valid), tree.predict(X_valid)
baseline_mae = np.mean(np.abs(y_valid - baseline_pred))
linear_mae = np.mean(np.abs(y_valid - linear_pred))
tree_mae = np.mean(np.abs(y_valid - tree_pred))
baseline_rmse = np.sqrt(np.mean((y_valid - baseline_pred) ** 2))
linear_rmse = np.sqrt(np.mean((y_valid - linear_pred) ** 2))
tree_rmse = np.sqrt(np.mean((y_valid - tree_pred) ** 2))
print(baseline_mae, linear_mae, tree_mae)

plt.figure()
plt.bar(["baseline", "linear", "tree"], [baseline_mae, linear_mae, tree_mae])
plt.title("Chart 2: validation MAE of the three models")
plt.xlabel("Model")
plt.ylabel("MAE (UNIT)")
plt.show()
'''.replace('UNIT', u)))
    out.append(dict(key='warning', title='Which readings should raise a warning?', marks=dict(warning=marks['warning']), inputs=['train', 'valid'],
        results=['warning_proba', 'tp', 'fp', 'fn', 'tn', 'precision', 'recall'],
        text=('A warning is a reading with `TARGET` at or above `LIMIT`. Fit `make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000))` '
              'on `train` and store the probability of a warning for each `valid` row.\n'
              'Warn when the probability is at least `THRESHOLD` (0.5), compare with the real warnings in `valid`, and store the counts, precision and recall (0 when a count is zero).'),
        solution='''y_train_warn = (train[TARGET] >= LIMIT).astype(int)
y_valid_warn = (valid[TARGET] >= LIMIT).astype(int)
warn_model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000))
warn_model.fit(train[FEATURES], y_train_warn)
warning_proba = warn_model.predict_proba(valid[FEATURES])[:, 1]
warn = (warning_proba >= THRESHOLD).astype(int)
tn, fp, fn, tp = confusion_matrix(y_valid_warn, warn, labels=[0, 1]).ravel()
precision = precision_score(y_valid_warn, warn, zero_division=0)
recall = recall_score(y_valid_warn, warn, zero_division=0)
print(tp, fp, fn, tn, precision, recall)
'''))
    out.append(dict(key='choose', title='Choose one model', marks={}, inputs=['baseline_mae', 'linear_mae', 'tree_mae'], results=['chosen_model'],
        text=('Use the supplied rule (MAE at most `MAX_MAE`, time at most `MAX_MS`, then the smallest MAE): '
              '`chosen_model = choose_model({"baseline": baseline_mae, "linear": linear_mae, "tree": tree_mae})`. Never use the test set to choose.'),
        solution='''chosen_model = choose_model({"baseline": baseline_mae, "linear": linear_mae, "tree": tree_mae})
print(chosen_model)
'''))
    out.append(dict(key='test', title='Open the test set once', marks=dict(test=marks['test']), inputs=['train', 'valid', 'chosen_model'], results=['test_rows', 'test_mae', 'test_recall'],
        text=('After Task 5, run `test_rows = open_test_set(chosen_model)` ONCE. Refit the chosen model and the warning model on `train` and `valid` together, '
              'then store the MAE on `test_rows` and the recall of the warnings at 0.5.'),
        solution='''test_rows = open_test_set(chosen_model)
both = pd.concat([train, valid])
models = {"baseline": DummyRegressor(), "linear": LinearRegression(), "tree": DecisionTreeRegressor(max_depth=4, random_state=17)}
final = make_pipeline(SimpleImputer(strategy="median"), models[chosen_model]).fit(both[FEATURES], both[TARGET])
test_mae = np.mean(np.abs(test_rows[TARGET] - final.predict(test_rows[FEATURES])))
final_warn = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000))
final_warn.fit(both[FEATURES], (both[TARGET] >= LIMIT).astype(int))
test_warn = (final_warn.predict_proba(test_rows[FEATURES])[:, 1] >= THRESHOLD).astype(int)
test_recall = recall_score((test_rows[TARGET] >= LIMIT).astype(int), test_warn, zero_division=0)
print(test_mae, test_recall)
'''))
    for task in out:
        task['starter'] = '# Your code here. Store: ' + ', '.join(task['results']) + '\n'
    return out


def task_markdown(i, task):
    marks = sum(task['marks'].values())
    head = f'## Task {i}: {task["title"]}' + (f' ({marks} marks)' if marks else '')
    return f"""{head}
{task['text']}

**Input:** {', '.join('`' + n + '`' for n in task['inputs'])}. **Store:** {', '.join('`' + n + '`' for n in task['results'])}."""


def memo_markdown(code, cfg=P.EXAM, task_no=7):
    limit_opts, next_opts = options(code)
    lim = '\n'.join(f'- **{letter}.** {text}' for letter, text, _, _ in limit_opts)
    nxt = '\n'.join(f'- **{letter}.** {text}' for letter, text, _, _ in next_opts)
    return f'''## Task {task_no}: Part B, the decision memo form ({K.PART_B_MAX} automatic marks)
Fill in `MEMO` in the next cell, for {PAYER}. Use your own numbers, at least two decimals, in {cfg['unit']}.

| Field | Enter | Marks |
|---|---|---|
| `recommended_model` | `"baseline"`, `"linear"` or `"tree"`: the model the rule chose and you opened the test set with. | 3 |
| `validation_mae` | The validation MAE of each model, from your notebook. | 3 |
| `test_mae`, `test_recall` | The MAE and the warning recall (0 to 1) from your one test opening. | 2 |
| `improvement_over_baseline` | Baseline validation MAE minus your model's (0 if you recommend the baseline). | 1 |
| `limits` | Three different letters: the true limits of this study. One mark each. | 3 |
| `next_step` | One letter: the best next step. | 1 |
| `answer_choice`, `answer_test_set` | Two answers in your own words, 8 to 80 words each. One mark each. | 2 |

**Limits** (some statements are false):
{lim}

**Next step:**
{nxt}

**Written answers:**
- `answer_choice`: {M.ANSWERS['answer_choice']['prompt']}
- `answer_test_set`: {M.ANSWERS['answer_test_set']['prompt']}'''


MEMO_STARTER = '''# Fill in every field; do not rename a field.
MEMO = {
    "recommended_model": "",                  # "baseline", "linear" or "tree"
    "validation_mae": {"baseline": None, "linear": None, "tree": None},   # your validation MAE values, in UNIT
    "test_mae": None,                         # the test MAE from your ONE opening, in UNIT
    "test_recall": None,                      # the test recall from your ONE opening (0 to 1)
    "improvement_over_baseline": None,        # baseline validation MAE minus your recommended model's, in UNIT
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
    "validation_mae": {{"baseline": round(float(baseline_mae), 3), "linear": round(float(linear_mae), 3), "tree": round(float(tree_mae), 3)}},
    "test_mae": round(float(test_mae), 3),
    "test_recall": round(float(test_recall), 3),
    "improvement_over_baseline": round(float(baseline_mae) - float({{"baseline": baseline_mae, "linear": linear_mae, "tree": tree_mae}}[chosen_model]), 3),
    "limits": {limits!r},
    "next_step": {nxt!r},
    "answer_choice": {a1!r},
    "answer_test_set": {a2!r},
}}
'''


# ------------------------------------------------------------------------------------------------ rehearsal self-study notes
# Short notes for a student who missed the revision class, at most 4 bullets each, right before the task that needs them.
REHEARSAL_NOTES = {
    'split': '''### Note: split by month
- Readings 15 minutes apart are almost the same, so a random split puts near-copies of training rows in the validation set.
- The score then looks better than it will be next month: that is **leakage**.
- Split by month: train January to August, validate September and October, keep November and December for the test.
- Slides: Class 3, "Train-test contamination: validation rows in the training set make the score look perfect".''',
    'regression': '''### Note: fit on the training rows only
- Every number learned from data (the imputation medians, the baseline mean) comes from `train` only, then is applied to `valid`.
- `make_pipeline(SimpleImputer(strategy="median"), model)` does this: it learns in `fit` and reuses in `predict`.
- Learning from all rows lets the model see the rows it is judged on, so the error looks too small.
- Slides: Class 3, "The pipeline rule: fit on the training set only, then apply the same numbers".''',
    'warning': '''### Note: logistic regression, confusion matrix, precision, recall
- **Logistic regression** gives each row a probability between 0 and 1 (`predict_proba(X)[:, 1]`); warn when it is at least 0.5.
- **Confusion matrix:** TP right warning, FP false alarm, FN missed warning, TN rightly none; `confusion_matrix(actual, warned, labels=[0, 1]).ravel()` gives tn, fp, fn, tp.
- **Precision** = TP / (TP + FP); **recall** = TP / (TP + FN); a zero denominator gives 0.
- Slides: Class 2, "Logistic regression in three lines: score, probability, prediction" and "The confusion matrix counts true and false positives and negatives".''',
    'test': '''### Note: open the test set once, then refit
- The validation set chooses the model; the test set gives **one honest estimate** of the chosen one.
- Looking at the test set and then changing your choice makes its score too good to trust.
- Refit on `train` and `valid` together (more data), then measure on `test_rows` once.
- Slides: Class 3, "We choose max_depth on the validation set and keep the test set sealed".''',
}
