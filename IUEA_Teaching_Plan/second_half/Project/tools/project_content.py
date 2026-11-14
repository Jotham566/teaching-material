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
PAYER = 'a property valuer (and, for the warning, the maintenance manager)'
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
TIME_PLAN = [('Run the setup cell', 5), ('Task 1: clean the data, Chart 1', 35), ('Task 2: split into training and validation rows', 10),
             ('Task 3: three models, MAE and RMSE, Chart 2', 40), ('Task 3b: the text columns (recipe given)', 10), ('Task 4: warnings', 15),
             ('Tasks 5 and 6: choose, open the test set', 15), ('Task 7: MEMO form', 25), ('Restart and run all, Check my work', 20), ('Spare', 5)]
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
H_CLEAN_COLUMNS = P.H_KEEP + ['living_m2']


def csv_text(rows, columns, delimiter=','):
    out = io.StringIO()
    w = csv.writer(out, lineterminator='\n', delimiter=delimiter)
    w.writerow(columns)
    for r in rows:
        w.writerow(['' if r.get(c) is None else r.get(c) for c in columns])
    return out.getvalue()


def data_payload():
    """The development rows of both files exactly as written (four fifths of each), and the cleaned test rows (one fifth, opened once)."""
    hl = P.houses_text().splitlines()
    ml = P.machines_text().splitlines()
    ht, mt = P.test_positions(len(hl) - 1), P.test_positions(len(ml) - 1)
    hd = [hl[0]] + [l for i, l in enumerate(hl[1:]) if i not in ht]
    md = [ml[0]] + [l for i, l in enumerate(ml[1:]) if i not in mt]
    _, houses_test, _, machines_test = P.tables()
    return json.dumps({'houses': '\n'.join(hd) + '\n', 'machines': '\n'.join(md) + '\n',
                       'house_test': csv_text(houses_test, H_CLEAN_COLUMNS), 'machine_test': csv_text(machines_test, P.M_KEEP)}, separators=(',', ':')).encode()


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
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer
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
# Houses: Ames, Iowa sales 2006 to 2010 (De Cock 2011). Machines: AI4I 2020, SYNTHETIC data modelled on real maintenance data (Matzka 2020).
H_KEEP = {P.H_KEEP!r}
M_KEEP = {P.M_KEEP!r}
H_TARGET, H_UNIT = {cfg["h_target"]!r}, {cfg["h_unit"]!r}
H_FEATURES = {cfg["h_features"]!r}
TEXT_FEATURES = {cfg["h_text"]!r}
M_TARGET, M_LIMIT = {cfg["m_target"]!r}, {cfg["m_limit"]!r}
M_FEATURES = {cfg["m_features"]!r}
THRESHOLD = {P.THRESHOLD}
MAX_MAE, MAX_MS = {cfg["max_mae"]!r}, {P.MAX_MS}   # the client's limits: teaching numbers, not real ones
LATENCY_MS = {P.LATENCY_MS!r}
houses_raw = pd.read_csv(io.StringIO(_data["houses"]), sep="\\t")
machines_raw = pd.read_csv(io.StringIO(_data["machines"]))
_HOUSE_TEST = pd.read_csv(io.StringIO(_data["house_test"]))
_MACHINE_TEST = pd.read_csv(io.StringIO(_data["machine_test"]))
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
    return _HOUSE_TEST.copy(), _MACHINE_TEST.copy()
print("houses_raw:", houses_raw.shape, "| machines_raw:", machines_raw.shape, "| H_TARGET:", H_TARGET, "| M_TARGET:", M_TARGET)
""" + PL.backup_code() + PL.countdown_code()


# ------------------------------------------------------------------------------------------------ the tasks
def tasks(cfg=P.EXAM):
    """Each task: key, title, marks (Part A items), text (two or three lines), inputs, results, starter, solution."""
    u, t = cfg['h_unit'], cfg['h_target']
    marks = dict(K.PARTS)
    x = cfg['chart_x']
    s = cfg['split_seed']
    warn = ('a machine failure (`Machine failure` is 1)' if cfg['m_target'] == 'Machine failure' else f'a reading with `{cfg["m_target"]}` at or above `M_LIMIT` ({cfg["m_limit"]})')
    out = []
    out.append(dict(key='clean', title='Clean the two tables', marks=dict(clean=marks['clean']), inputs=['houses_raw', 'machines_raw'], results=['houses', 'machines'],
        text=('`houses`: from `houses_raw` keep only the columns `H_KEEP` (every column except the identifier PID), '
              'drop the houses with `Gr Liv Area` above 4000 sq ft (the data\'s author advises this: 5 unusual sales), and add `living_m2` = `Gr Liv Area` times 0.092903. '
              'Keep the missing values: the imputer fills them later from the training rows only.\n'
              '`machines`: from `machines_raw` keep only `M_KEEP`, which drops the identifiers (`UDI`, `Product ID`) and `TWF`, `HDF`, `PWF`, `OSF`, `RNF` (they record the failure itself and would leak the answer), '
              'and turn `Type` into a number: L is 0, M is 1, H is 2. Do not change the raw tables.\n'
              f'Chart 1: a scatter of `{x}` (across) against `H_TARGET` (up) from `houses`, with a title, both axis names and the unit ({u}).'),
        solution=f'''houses = houses_raw[H_KEEP].copy()
houses = houses[~(houses["Gr Liv Area"] > 4000)]
houses["living_m2"] = houses["Gr Liv Area"] * 0.092903
machines = machines_raw[M_KEEP].copy()
machines["Type"] = machines["Type"].map({{"L": 0, "M": 1, "H": 2}})
print(houses.shape, machines.shape)

plt.figure()
plt.scatter(houses["{x}"], houses[H_TARGET], s=4)
plt.title("Chart 1: {cfg['short']} against {x}")
plt.xlabel("{x}")
plt.ylabel("{cfg['short'].capitalize()} ({u})")
plt.show()
'''))
    out.append(dict(key='split', title='Split into training and validation rows', marks=dict(split=marks['split']), inputs=['houses', 'machines'],
        results=['houses_train', 'houses_valid', 'machines_train', 'machines_valid'],
        text=(f'Use exactly this rule for each table: `houses_valid = houses.sample(frac=0.25, random_state={s})` and `houses_train = houses.drop(houses_valid.index)`; the same for `machines`. '
              'The test rows (a fifth of each file) were set aside in the setup cell: we never tune on them, so they stay an honest test.'),
        solution=f'''houses_valid = houses.sample(frac=0.25, random_state={s})
houses_train = houses.drop(houses_valid.index)
machines_valid = machines.sample(frac=0.25, random_state={s})
machines_train = machines.drop(machines_valid.index)
print(len(houses_train), len(houses_valid), len(machines_train), len(machines_valid))
'''))
    out.append(dict(key='regression', title=f'Question 1: predict {cfg["what"]}', marks=dict(regression=marks['regression'], errors=marks['errors'], leakage=marks['leakage'], charts=marks['charts']),
        inputs=['houses_train', 'houses_valid'], results=['baseline_pred', 'linear_pred', 'tree_pred', 'baseline_mae', 'linear_mae', 'tree_mae', 'baseline_rmse', 'linear_rmse', 'tree_rmse'],
        text=('Fit each model on `houses_train` only (columns `H_FEATURES`, target `H_TARGET`) and predict `houses_valid`: `make_pipeline(SimpleImputer(strategy="median"), model)` with '
              '`DummyRegressor()`, `LinearRegression()` and `DecisionTreeRegressor(max_depth=4, random_state=17)`.\n'
              f'Then the MAE and RMSE of each on `houses_valid`, in {u}.\n'
              f'Chart 2: a bar chart of the three MAE values, with a title, both axis names and the unit ({u}).'),
        solution='''X_train, y_train = houses_train[H_FEATURES], houses_train[H_TARGET]
X_valid, y_valid = houses_valid[H_FEATURES], houses_valid[H_TARGET]
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
    out.append(dict(key='encoded', label='3b', title='Do the text columns help?', marks=dict(encoded=marks['encoded']), inputs=['houses_train', 'houses_valid'],
        results=['encoded_pred', 'encoded_mae'],
        text=('A comparison only (it is not one of the models in Task 5). Copy and adapt this recipe: it fills and one-hot encodes the text columns `TEXT_FEATURES`, learning only from `houses_train`:\n'
              '`make_pipeline(make_column_transformer((SimpleImputer(strategy="median"), H_FEATURES), (make_pipeline(SimpleImputer(strategy="most_frequent"), '
              'OneHotEncoder(handle_unknown="ignore")), TEXT_FEATURES)), LinearRegression())`\n'
              f'Fit it on `houses_train` (columns `H_FEATURES + TEXT_FEATURES`), predict `houses_valid`, and store the predictions and their MAE in {u}.'),
        solution='''encoder = make_column_transformer((SimpleImputer(strategy="median"), H_FEATURES),
                                  (make_pipeline(SimpleImputer(strategy="most_frequent"), OneHotEncoder(handle_unknown="ignore")), TEXT_FEATURES))
encoded = make_pipeline(encoder, LinearRegression()).fit(houses_train[H_FEATURES + TEXT_FEATURES], houses_train[H_TARGET])
encoded_pred = encoded.predict(houses_valid[H_FEATURES + TEXT_FEATURES])
encoded_mae = np.mean(np.abs(houses_valid[H_TARGET] - encoded_pred))
print(encoded_mae, linear_mae)
'''))
    out.append(dict(key='warning', title=f'Question 2: warn of {cfg["m_what"]}', marks=dict(warning=marks['warning']), inputs=['machines_train', 'machines_valid'],
        results=['warning_proba', 'tp', 'fp', 'fn', 'tn', 'precision', 'recall'],
        text=(f'A warning is {warn}: `M_TARGET >= M_LIMIT`. Fit `make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000))` '
              'on `machines_train` (columns `M_FEATURES`) and store the probability of a warning for each `machines_valid` row.\n'
              'Warn when the probability is at least `THRESHOLD` (0.5), compare with the real warnings in `machines_valid`, and store the counts, precision and recall (0 when a count is zero).'),
        solution='''y_train_warn = (machines_train[M_TARGET] >= M_LIMIT).astype(int)
y_valid_warn = (machines_valid[M_TARGET] >= M_LIMIT).astype(int)
warn_model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000))
warn_model.fit(machines_train[M_FEATURES], y_train_warn)
warning_proba = warn_model.predict_proba(machines_valid[M_FEATURES])[:, 1]
warn = (warning_proba >= THRESHOLD).astype(int)
tn, fp, fn, tp = confusion_matrix(y_valid_warn, warn, labels=[0, 1]).ravel()
precision = precision_score(y_valid_warn, warn, zero_division=0)
recall = recall_score(y_valid_warn, warn, zero_division=0)
print(tp, fp, fn, tn, precision, recall)
'''))
    out.append(dict(key='choose', title='Choose one model', marks={}, inputs=['baseline_mae', 'linear_mae', 'tree_mae'], results=['chosen_model'],
        text=(f'Use the supplied rule (MAE at most `MAX_MAE`, {cfg["max_mae"]:,} {u}, a teaching number; time at most `MAX_MS`; then the smallest MAE): '
              '`chosen_model = choose_model({"baseline": baseline_mae, "linear": linear_mae, "tree": tree_mae})`. Never use the test rows to choose.'),
        solution='''chosen_model = choose_model({"baseline": baseline_mae, "linear": linear_mae, "tree": tree_mae})
print(chosen_model)
'''))
    out.append(dict(key='test', title='Open the test rows once', marks=dict(test=marks['test']), inputs=['houses_train', 'houses_valid', 'machines_train', 'machines_valid', 'chosen_model'],
        results=['house_test', 'machine_test', 'test_mae', 'test_recall'],
        text=('After Task 5, run `house_test, machine_test = open_test_set(chosen_model)` ONCE. Refit the chosen model on `houses_train` and `houses_valid` together and the warning model on '
              '`machines_train` and `machines_valid` together, then store the MAE on `house_test` and the recall of the warnings on `machine_test` at 0.5.'),
        solution='''house_test, machine_test = open_test_set(chosen_model)
both = pd.concat([houses_train, houses_valid])
models = {"baseline": DummyRegressor(), "linear": LinearRegression(), "tree": DecisionTreeRegressor(max_depth=4, random_state=17)}
final = make_pipeline(SimpleImputer(strategy="median"), models[chosen_model]).fit(both[H_FEATURES], both[H_TARGET])
test_mae = np.mean(np.abs(house_test[H_TARGET] - final.predict(house_test[H_FEATURES])))
mboth = pd.concat([machines_train, machines_valid])
final_warn = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000))
final_warn.fit(mboth[M_FEATURES], (mboth[M_TARGET] >= M_LIMIT).astype(int))
test_warn = (final_warn.predict_proba(machine_test[M_FEATURES])[:, 1] >= THRESHOLD).astype(int)
test_recall = recall_score((machine_test[M_TARGET] >= M_LIMIT).astype(int), test_warn, zero_division=0)
print(test_mae, test_recall)
'''))
    number = 0
    for task in out:
        task['starter'] = '# Your code here. Store: ' + ', '.join(task['results']) + '\n'
        if 'label' not in task:
            number += 1
            task['label'] = str(number)
    return out


def memo_task_no(cfg=P.EXAM):
    return sum(1 for t in tasks(cfg) if t['label'].isdigit()) + 1


def task_markdown(i, task):
    marks = sum(task['marks'].values())
    head = f'## Task {task.get("label", i)}: {task["title"]}' + (f' ({marks} marks)' if marks else '')
    data = ('\nData: houses from the Ames, Iowa assessor, 2006 to 2010 (De Cock 2011, Journal of Statistics Education 19(3)); machines from AI4I 2020 '
            '(Matzka 2020, UCI, CC BY 4.0), which is SYNTHETIC data modelled on real maintenance data.') if task['key'] == 'clean' else ''
    return f"""{head}
{task['text']}{data}

**Input:** {', '.join('`' + n + '`' for n in task['inputs'])}. **Store:** {', '.join('`' + n + '`' for n in task['results'])}."""


def memo_markdown(code, cfg=P.EXAM, task_no=7):
    limit_opts, next_opts = options(code)
    lim = '\n'.join(f'- **{letter}.** {text}' for letter, text, _, _ in limit_opts)
    nxt = '\n'.join(f'- **{letter}.** {text}' for letter, text, _, _ in next_opts)
    return f'''## Task {task_no}: Part B, the decision memo form ({K.PART_B_MAX} automatic marks)
Fill in `MEMO` in the next cell, for {PAYER}. Use your own numbers, at least two decimals, in {cfg['h_unit']}. You may add one sentence on Task 3b to `answer_choice` (no extra mark).

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
    vm, chosen, unit = n['p']['validation_mae'], n['chosen'], cfg['h_unit']
    others = [m for m in ('baseline', 'linear', 'tree') if m != chosen]
    a1 = (f"I recommend the {NAMES_OF[chosen]} because its validation MAE of {vm[chosen]:.0f} {unit} on the validation houses is lower than the "
          f"{NAMES_OF[others[0]]} ({vm[others[0]]:.0f} {unit}) and the {NAMES_OF[others[1]]} ({vm[others[1]]:.0f} {unit}), and it meets the client limit.")
    a2 = ("The test set is opened only once, at the end, so that it stays an honest estimate on rows the model has never seen; if we used it to choose or tune the model, "
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
    'split': '''### Note: training, validation and test rows
- The model learns from `train`, we compare models on `valid`, and the test rows give one honest estimate at the end.
- `sample(frac=0.25, random_state=29)` picks the same random quarter every time, so everyone gets the same split (the project uses 17, so its numbers differ from these).
- If we tuned or chose on the test rows, they would stop being unseen: the score would look better than it really is (**leakage**).
- Slides: Class 3, "Train-test contamination: validation rows in the training set make the score look perfect".''',
    'regression': '''### Note: fit on the training rows only
- Every number learned from data (the imputation medians, the baseline mean) comes from `train` only, then is applied to `valid`.
- `make_pipeline(SimpleImputer(strategy="median"), model)` does this: it learns in `fit` and reuses in `predict`.
- Learning from all rows lets the model see the rows it is judged on, so the error looks too small.
- Slides: Class 3, "The pipeline rule: fit on the training set only, then apply the same numbers".''',
    'encoded': '''### Note: one-hot encoding (shown in the revision class)
- A model needs numbers. **One-hot encoding** turns a text column into one 0 or 1 column per category: `Neighborhood` "NAmes" becomes a 1 in the column `Neighborhood_NAmes`.
- Like the medians, the categories are learned from `houses_train` only: the pipeline learns them in `fit` and reuses them in `predict`.
- A category that never appears in `houses_train` has no column; `handle_unknown="ignore"` gives it all zeros instead of an error.
- `SimpleImputer(strategy="most_frequent")` fills a missing text value with the commonest category in `houses_train`.''',
    'warning': '''### Note: logistic regression, confusion matrix, precision, recall
- **Logistic regression** gives each row a probability between 0 and 1 (`predict_proba(X)[:, 1]`); warn when it is at least 0.5.
- **Confusion matrix:** TP right warning, FP false alarm, FN missed warning, TN rightly none; `confusion_matrix(actual, warned, labels=[0, 1]).ravel()` gives tn, fp, fn, tp.
- **Precision** = TP / (TP + FP); **recall** = TP / (TP + FN); a zero denominator gives 0.
- Slides: Class 2, "Logistic regression in three lines: score, probability, prediction" and "The confusion matrix counts true and false positives and negatives".''',
    'test': '''### Note: open the test set once, then refit
- The validation set chooses the model; the test set gives **one honest estimate** of the chosen one.
- Looking at the test set and then changing your choice makes its score too good to trust.
- Refit on the training and validation rows together (more data), then measure on `house_test` and `machine_test` once.
- Slides: Class 3, "We choose max_depth on the validation set and keep the test set sealed".''',
}
