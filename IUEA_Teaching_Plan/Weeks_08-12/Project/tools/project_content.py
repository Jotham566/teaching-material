"""One source of truth for the Engineering ML project: course facts, the data, the tasks (text, starter and model solution), the
Part B memo form, the marks and the window rules. The notebooks, the rehearsal, the briefs and the marking guide are built from this file.

Plain code (lecturer's redesign of 14 November 2026): students write ordinary straight-line code, no function placeholders. Each task
names its INPUT variables and the RESULT names to store. The grader re-runs each task's cells on hidden inputs (own_cells.py).
ONE supplied code cell, "Setup: run me first": the two tables as students receive them (organised, with the added problems) packed inside it
with a SHA-256 check, the constants, choose_model, the silent backup and the clock.
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
sys.path.insert(0, str(PLAN / 'Assessments/grader'))
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
TIME_PLAN = [('Run the setup cell, read the data', 5), ('Question 1, Tasks 1 and 2: clean the houses, Chart 1, split', 25),
             ('Task 3: linear regression and a tree, MAE and RMSE, Chart 2', 30), ('Task 3b: the text columns (recipe given)', 10),
             ('Task 4: choose, use the test set once', 10), ('Question 2, Tasks 5 and 6: clean the machines, split', 15),
             ('Task 7: logistic regression and a tree, counts, precision, recall, F1', 25), ('Task 8: choose, use the test set once', 10),
             ('Task 9: MEMO form', 25), ('Restart and run all, Check my work', 20), ('Spare', 5)]
assert sum(m for _, m in TIME_PLAN) == MINUTES
OWN_CELLS = 'Write your own code under each task and add cells as you need. Store each result under the name given.'
SOURCE = P.SOURCE
CITATION = P.CITATION
CFGS = {'exam': P.EXAM, 'rehearsal': P.REHEARSAL}
SETUP_TITLE = '#@title Setup: run me first. DO NOT EDIT THIS CELL'
SETUP_MARKER = '# IUEA-SETUP-CELL'
IDENTITY_LINE = '_IUEA_IDENTITY = {}'


def numbers(cfg=P.EXAM):
    p = P.pipeline(cfg)
    test = P.test_expected(p['chosen_model'], cfg)
    return dict(p=p, chosen=p['chosen_model'], threshold=P.THRESHOLD, test=test)


def options(code, v=None):
    return M.options(code)


# ------------------------------------------------------------------------------------------------ the data inside the setup cell
def csv_text(rows, columns, delimiter=','):
    out = io.StringIO()
    w = csv.writer(out, lineterminator='\n', delimiter=delimiter)
    w.writerow(columns)
    for r in rows:
        w.writerow(['' if r.get(c) is None else r.get(c) for c in columns])
    return out.getvalue()


def data_payload():
    """The two tables as students receive them (organised, with the added problems), as CSV text."""
    return json.dumps({'houses': csv_text(P.houses_given(), P.H_COLUMNS), 'machines': csv_text(P.machines_given(), P.M_COLUMNS)},
                      separators=(',', ':')).encode()


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
{SETUP_MARKER} (supplied). DO NOT EDIT OR DELETE THIS CELL. Run it first, and again after a restart. It shows your time left.
# Any change made here is undone: the marking computer always uses the original of this cell.
{IDENTITY_LINE[:-2]}{identity}
import base64, bz2, hashlib, io, json, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
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
# Houses: Ames, Iowa sales 2006 to 2010 (De Cock 2011). Machines: AI4I 2020, synthetic data modelled on real machine logs (Matzka 2020).
# Both tables were organised for this project, and a few problems were ADDED on purpose for you to clean (see "The data").
H_TARGET, H_UNIT = {cfg["h_target"]!r}, {cfg["h_unit"]!r}
H_FEATURES = {cfg["h_features"]!r}
TEXT_FEATURES = {cfg["h_text"]!r}
M_TARGET, M_LIMIT = {cfg["m_target"]!r}, {cfg["m_limit"]!r}
M_FEATURES = {cfg["m_features"]!r}
THRESHOLD = {P.THRESHOLD}
MAX_MAE, MAX_MS = {cfg["max_mae"]!r}, {P.MAX_MS}   # the client's limits: teaching numbers, not real ones
LATENCY_MS = {P.LATENCY_MS!r}
houses_raw = pd.read_csv(io.StringIO(_data["houses"]))
machines_raw = pd.read_csv(io.StringIO(_data["machines"]))
def choose_model(maes):
    ok = [m for m in maes if maes[m] is not None and maes[m] <= MAX_MAE and LATENCY_MS[m] <= MAX_MS]
    return min(ok, key=lambda m: (maes[m], LATENCY_MS[m], m)) if ok else None
def choose_warning_model(f1s):
    return "tree" if f1s["tree"] > f1s["logistic"] else "logistic"
print("houses_raw:", houses_raw.shape, "| machines_raw:", machines_raw.shape)
""" + PL.backup_code() + PL.countdown_code()


# ------------------------------------------------------------------------------------------------ the data, introduced to students
def data_markdown():
    """The cell right after Setup: what the two tables are, every column in plain words, and the problems added for cleaning."""
    hp, mp = P.H_PROBLEMS, P.M_PROBLEMS
    return f'''## The data
Setup loads two tables. Both are real published data, organised for this project. **A few problems were added on purpose** for you to clean. Question 1 (Tasks 1 to 4) uses only the houses; Question 2 (Tasks 5 to 8) uses only the machines.

**`houses_raw`**: {len(P.houses_given()):,} house sales in Ames, Iowa (USA), 2006 to 2010. One row is one sale. Question 1 predicts the price.

| Column | Meaning |
|---|---|
| `house_id` | Sale number |
| `neighbourhood` | Area of the city (text) |
| `building_type` | Detached, townhouse, duplex or two-family conversion (text) |
| `overall_quality`, `overall_condition` | Rating from 1 (very poor) to 10 (excellent) |
| `year_built`, `year_remodelled` | Year |
| `living_area_m2`, `basement_area_m2`, `lot_area_m2`, `garage_area_m2` | Area in square metres |
| `lot_frontage_m` | Length of the plot along the street, in metres |
| `bedrooms`, `full_bathrooms`, `garage_cars`, `fireplaces` | Counts |
| `kitchen_quality` | Excellent, good, average, fair or poor (text) |
| **`sale_price_usd`** | Price paid, in US dollars. **The target of Question 1.** |

**`machines_raw`**: {len(P.machines_given()):,} runs of a metal-cutting (milling) machine. The data are synthetic: generated to behave like real machine records. One row is one run. Question 2 warns of a failure.

| Column | Meaning |
|---|---|
| `machine_id` | Record number |
| `product_type` | Product quality: L (low), M (medium) or H (high) |
| `air_temp_k`, `process_temp_k` | Air and process temperature, in kelvin |
| `rotation_speed_rpm` | Spindle speed, in revolutions per minute |
| `torque_nm` | Turning force, in newton metres |
| `tool_wear_min` | Minutes the cutting tool has been in use |
| **`failure`** | 1 if the machine failed during the run, 0 if not. **The target of Question 2.** |

**Problems to clean (Tasks 1 and 5):** duplicate rows, rows with no target value, and impossible values (for example a negative area). Some values are also missing, for example `lot_frontage_m`: leave those for the imputer.'''


QUESTION_HEADINGS = {
    1: '# Question 1: what will a house sell for? (regression)\nTasks 1 to 4 use only `houses_raw`: clean, split, compare linear regression with a decision tree, then test the chosen model once.',
    2: '# Question 2: will this machine run fail? (classification)\nTasks 5 to 8 use only `machines_raw`: clean, split, compare logistic regression with a decision tree, then test the chosen model once.',
}


# Supplied "watch it learn" cells (lecturer, 17 November 2026): ready to run, not marked. Each sits at the end of its task, after the student's
# own cells, and uses only the task's inputs (the grader reruns a task's cells on hidden rows). Names start with gd_ / gd2_ so they never look
# like a result, and nothing printed is a marked number.
SUPPLIED_MARK = '# IUEA-SUPPLIED'
SUPPLIED_CELLS = {
    'regression': ('''### Supplied: watch linear regression learn (just run it, not marked)
`LinearRegression()` computes its weights directly, in one go: it has no epochs. Gradient descent (Class 1) reaches the same weights step by step:
start every weight at 0, then repeat **new w = old w - learning rate x slope of the loss**.
- **Epochs** are set in the line `epochs = 300`. One epoch is one pass over all the training houses; here every step uses all of them, so one step is one epoch.
- **Learning rate** is set in the line `learning_rate = 0.1`: the size of each step.''',
'''# IUEA-SUPPLIED: do not edit. Just run this cell; it is not marked.
if "houses_train" not in globals():
    print("Do Tasks 1 and 2 first: this cell needs houses_train.")
else:
    gd_imputer = SimpleImputer(strategy="median")
    gd_scaler = StandardScaler()
    gd_filled = gd_imputer.fit_transform(houses_train[H_FEATURES])   # fill gaps with the training medians
    gd_X = gd_scaler.fit_transform(gd_filled)                         # standardise: every feature has mean 0 and standard deviation 1
    gd_y = houses_train[H_TARGET].to_numpy() / 1000                   # price in thousand USD

    epochs = 300                      # how many passes over the training houses
    learning_rate = 0.1               # the size of each step downhill
    gd_w = np.zeros(gd_X.shape[1])    # one weight per feature, all 0 at the start
    gd_b = 0.0                        # the intercept, 0 at the start
    gd_losses = []                    # the loss (MSE) after each epoch
    gd_errors = []                    # the training MAE after each epoch
    for epoch in range(epochs):
        gd_guess = gd_X @ gd_w + gd_b                 # the model's price for every training house: b + w1 x1 + w2 x2 + ...
        gd_gap = gd_guess - gd_y                      # how far off each guess is
        gd_losses.append(np.mean(gd_gap ** 2))        # the loss: mean squared error (MSE)
        gd_errors.append(np.mean(np.abs(gd_gap)))     # the training MAE, in thousand USD
        gd_w = gd_w - learning_rate * 2 * (gd_X.T @ gd_gap) / len(gd_y)   # new w = old w - learning rate x slope of the loss
        gd_b = gd_b - learning_rate * 2 * np.mean(gd_gap)

    print("Loss (MSE) at the start:", round(gd_losses[0]), "| after", epochs, "epochs:", round(gd_losses[-1]))
    print("Training MAE at the start:", round(gd_errors[0], 1), "thousand USD | after", epochs, "epochs:", round(gd_errors[-1], 1))

    plt.figure()
    plt.plot(gd_losses)
    plt.title("Gradient descent: the training loss falls epoch by epoch")
    plt.xlabel("Epoch")
    plt.ylabel("Loss: MSE (thousand USD, squared)")
    plt.show()

    # Regression has no accuracy (a price is never exactly right or wrong): its training curve is the error at each epoch
    plt.figure()
    plt.plot(gd_errors)
    plt.title("Training error at each epoch (lower is better)")
    plt.xlabel("Epoch")
    plt.ylabel("Training MAE (thousand USD)")
    plt.show()

    # The learned weights: gradient descent next to LinearRegression, on the same standardised features
    gd_check = LinearRegression().fit(gd_X, gd_y)
    gd_weights = pd.DataFrame({"feature": H_FEATURES, "gradient descent": gd_w, "LinearRegression": gd_check.coef_})
    display(gd_weights.round(2))
    print("Intercept, gradient descent:", round(gd_b, 2), "| LinearRegression:", round(gd_check.intercept_, 2))
''', '''**How to read the weights table**
- Each row is one feature. A weight is the change in price, **in thousand USD**, when that feature rises by **one standard deviation** (the others held fixed). Example: a living_area_m2 weight of 34 means a house about one standard deviation bigger sells for about 34,000 USD more.
- A positive weight raises the price; a negative one lowers it. Because every feature is on the same scale, a bigger weight (ignoring the sign) means a feature matters more.
- The two columns agree: gradient descent, walking downhill, ends where `LinearRegression()` lands directly.
- The intercept is the price of a house that is average in every feature: the mean training price, in thousand USD.
- These are not the weights printed in Task 3: there the features kept their own units (per m2, per year), so those weights cannot be compared with each other.'''),
    'classify': ('''### Supplied: watch logistic regression learn (just run it, not marked)
Logistic regression learns by gradient descent (Class 2). Each epoch it turns every run's score into a chance of failure (the sigmoid),
measures the log loss, and moves every weight a small step downhill.
- **Epochs** are set in the line `epochs = 1000`: one epoch is one pass over all the training runs.
- **Learning rate** is set in the line `learning_rate = 1.0`.
- The second chart is the **training accuracy** at each epoch: the share of training runs the model calls right.''',
'''# IUEA-SUPPLIED: do not edit. Just run this cell; it is not marked.
if "machines_train" not in globals():
    print("Do Tasks 5 and 6 first: this cell needs machines_train.")
else:
    gd2_imputer = SimpleImputer(strategy="median")
    gd2_scaler = StandardScaler()
    gd2_filled = gd2_imputer.fit_transform(machines_train[M_FEATURES])   # fill gaps with the training medians
    gd2_X = gd2_scaler.fit_transform(gd2_filled)                          # standardise: mean 0, standard deviation 1
    gd2_y = (machines_train[M_TARGET] >= M_LIMIT).astype(int).to_numpy()   # 1 = the run failed, 0 = it did not

    epochs = 1000                       # how many passes over the training runs
    learning_rate = 1.0                 # the size of each step downhill
    gd2_w = np.zeros(gd2_X.shape[1])    # one weight per feature, all 0 at the start
    gd2_b = 0.0                         # the intercept, 0 at the start
    gd2_losses = []                     # the log loss after each epoch
    gd2_accuracy = []                   # the training accuracy after each epoch
    for epoch in range(epochs):
        gd2_chance = 1 / (1 + np.exp(-(gd2_X @ gd2_w + gd2_b)))   # the sigmoid: a chance of failure from 0 to 1
        gd2_losses.append(-np.mean(gd2_y * np.log(gd2_chance) + (1 - gd2_y) * np.log(1 - gd2_chance)))   # log loss
        gd2_accuracy.append(np.mean((gd2_chance >= 0.5) == gd2_y))   # share of training runs called right at threshold 0.5
        gd2_w = gd2_w - learning_rate * (gd2_X.T @ (gd2_chance - gd2_y)) / len(gd2_y)   # new w = old w - learning rate x slope
        gd2_b = gd2_b - learning_rate * np.mean(gd2_chance - gd2_y)

    print("Log loss at the start:", round(gd2_losses[0], 3), "| after", epochs, "epochs:", round(gd2_losses[-1], 3))
    print("Training accuracy at the start:", round(gd2_accuracy[0], 3), "| after", epochs, "epochs:", round(gd2_accuracy[-1], 3))

    plt.figure()
    plt.plot(gd2_losses)
    plt.title("Gradient descent: the training log loss falls epoch by epoch")
    plt.xlabel("Epoch")
    plt.ylabel("Log loss")
    plt.show()

    plt.figure()
    plt.plot(gd2_accuracy)
    plt.title("Training accuracy at each epoch")
    plt.xlabel("Epoch")
    plt.ylabel("Training accuracy")
    plt.show()

    # The learned weights: gradient descent next to LogisticRegression, on the same standardised features
    # (LogisticRegression adds a small penalty, so its weights are close, not equal)
    gd2_check = LogisticRegression(max_iter=1000).fit(gd2_X, gd2_y)
    gd2_weights = pd.DataFrame({"feature": M_FEATURES, "gradient descent": gd2_w, "LogisticRegression": gd2_check.coef_[0]})
    display(gd2_weights.round(2))
    print("Intercept, gradient descent:", round(gd2_b, 2), "| LogisticRegression:", round(gd2_check.intercept_[0], 2))
''', '''**How to read the two charts and the weights table**
- **Accuracy starts near 0.03:** with every weight at 0, every run gets a chance of 0.5, so the model warns about every run and is right only for the few that failed. Within a few epochs it reaches about 0.97 by saying "no failure" to almost every run. Failures are rare, so accuracy looks good even when most failures are missed: that is why we choose the warning model by **F1**.
- **Weights:** each is the change in the log-odds of a failure when that feature rises by one standard deviation (the others held fixed). A positive weight makes a failure more likely; a negative one less likely. On one scale, a bigger weight (ignoring the sign) means a feature matters more.
- The two columns are close: gradient descent ends near where `LogisticRegression()` lands.'''),
}


# ------------------------------------------------------------------------------------------------ the tasks
def tasks(cfg=P.EXAM):
    """Each task: key, title, marks (Part A items), text, inputs, results, starter, solution, and 'question' (1 houses, 2 machines).
    Two separate questions, no baseline model (lecturer, 16 November 2026)."""
    u, t = cfg['h_unit'], cfg['h_target']
    marks = dict(K.PARTS)
    x = cfg['chart_x']
    s = cfg['split_seed']
    out = []
    # ------------------------------------------------------------ Question 1: house prices (regression)
    out.append(dict(key='clean_h', question=1, title='Clean the house table', marks=dict(clean_h=marks['clean_h']), inputs=['houses_raw'], results=['houses'],
        text=('Start from a copy: `houses = houses_raw.copy()`. Then:\n'
              '1. Remove duplicate rows.\n'
              '2. Remove the rows with no price (`H_TARGET`).\n'
              f'3. Remove the rows with an impossible value: `living_area_m2` must be above 0 and `year_built` must be {P.LAST_YEAR} or earlier.\n\n'
              'Leave the other missing values: in Task 3 the imputer fills them from the training rows only.\n'
              f'**Chart 1:** a scatter of `{x}` (across) against `H_TARGET` (up), from `houses`, with a title, axis labels and the unit ({u}).'),
        solution=f'''houses = houses_raw.copy()
houses = houses.drop_duplicates()
houses = houses.dropna(subset=[H_TARGET])
houses = houses[(houses["living_area_m2"] > 0) & (houses["year_built"] <= {P.LAST_YEAR})]
print(houses_raw.shape, houses.shape)

plt.figure()
plt.scatter(houses["{x}"], houses[H_TARGET], s=4)
plt.title("Chart 1: {cfg['short']} against living area")
plt.xlabel("Living area (m2)")
plt.ylabel("{cfg['short'].capitalize()} ({u})")
plt.show()
'''))
    out.append(dict(key='split_h', question=1, title='Split the houses into training, validation and test sets', marks=dict(split_h=marks['split_h']), inputs=['houses'],
        results=['houses_train', 'houses_valid', 'houses_test'],
        text=('Use exactly these four lines:\n'
              f'`houses_test = houses.sample(frac=0.2, random_state={s})`  \n'
              '`houses_rest = houses.drop(houses_test.index)`  \n'
              f'`houses_valid = houses_rest.sample(frac=0.25, random_state={s})`  \n'
              '`houses_train = houses_rest.drop(houses_valid.index)`\n\n'
              'This gives 60 percent training, 20 percent validation and 20 percent test rows. Do not use the test rows until Task 4.'),
        solution=f'''houses_test = houses.sample(frac=0.2, random_state={s})
houses_rest = houses.drop(houses_test.index)
houses_valid = houses_rest.sample(frac=0.25, random_state={s})
houses_train = houses_rest.drop(houses_valid.index)
print(len(houses_train), len(houses_valid), len(houses_test))
'''))
    out.append(dict(key='regression', question=1, title='Linear regression and a decision tree', marks=dict(regression=marks['regression'], errors=marks['errors'], leakage=marks['leakage'], charts=marks['charts']),
        inputs=['houses_train', 'houses_valid'], results=['linear_pred', 'tree_pred', 'linear_mae', 'tree_mae', 'linear_rmse', 'tree_rmse'],
        text=('Fit two models on `houses_train` (columns `H_FEATURES`, target `H_TARGET`), each as `make_pipeline(SimpleImputer(strategy="median"), model)`: '
              '`LinearRegression()` and `DecisionTreeRegressor(max_depth=4, random_state=17)`.\n'
              f'Predict `houses_valid` and compute the MAE and RMSE of each, in {u}.\n'
              f'**Chart 2:** a bar chart of the two MAE values, with a title, axis labels and the unit ({u}).'),
        solution='''X_train, y_train = houses_train[H_FEATURES], houses_train[H_TARGET]
X_valid, y_valid = houses_valid[H_FEATURES], houses_valid[H_TARGET]
linear = make_pipeline(SimpleImputer(strategy="median"), LinearRegression()).fit(X_train, y_train)
tree = make_pipeline(SimpleImputer(strategy="median"), DecisionTreeRegressor(max_depth=4, random_state=17)).fit(X_train, y_train)
linear_pred, tree_pred = linear.predict(X_valid), tree.predict(X_valid)
linear_mae = np.mean(np.abs(y_valid - linear_pred))
tree_mae = np.mean(np.abs(y_valid - tree_pred))
linear_rmse = np.sqrt(np.mean((y_valid - linear_pred) ** 2))
tree_rmse = np.sqrt(np.mean((y_valid - tree_pred) ** 2))
print(linear_mae, tree_mae)

plt.figure()
plt.bar(["linear", "tree"], [linear_mae, tree_mae])
plt.title("Chart 2: validation MAE of the two models")
plt.xlabel("Model")
plt.ylabel("MAE (UNIT)")
plt.show()
'''.replace('UNIT', u)))
    out.append(dict(key='encoded', question=1, label='3b', title='Do the text columns help?', marks=dict(encoded=marks['encoded']), inputs=['houses_train', 'houses_valid'],
        results=['encoded_pred', 'encoded_mae'],
        text=('A comparison only: not one of the models in Task 4. Fit this pipeline on `houses_train` (columns `H_FEATURES + TEXT_FEATURES`):\n'
              '`make_pipeline(make_column_transformer((SimpleImputer(strategy="median"), H_FEATURES), (make_pipeline(SimpleImputer(strategy="most_frequent"), '
              'OneHotEncoder(handle_unknown="ignore")), TEXT_FEATURES)), LinearRegression())`\n'
              f'Predict `houses_valid` and compute the MAE, in {u}.'),
        solution='''encoder = make_column_transformer((SimpleImputer(strategy="median"), H_FEATURES),
                                  (make_pipeline(SimpleImputer(strategy="most_frequent"), OneHotEncoder(handle_unknown="ignore")), TEXT_FEATURES))
encoded = make_pipeline(encoder, LinearRegression()).fit(houses_train[H_FEATURES + TEXT_FEATURES], houses_train[H_TARGET])
encoded_pred = encoded.predict(houses_valid[H_FEATURES + TEXT_FEATURES])
encoded_mae = np.mean(np.abs(houses_valid[H_TARGET] - encoded_pred))
print(encoded_mae, linear_mae)
'''))
    out.append(dict(key='test_h', question=1, title='Choose the house model, then use the test set once', marks=dict(test_h=marks['test_h']),
        inputs=['houses_train', 'houses_valid', 'houses_test', 'linear_mae', 'tree_mae'], results=['chosen_house_model', 'test_mae'],
        text=('1. Run `chosen_house_model = choose_model({"linear": linear_mae, "tree": tree_mae})`. '
              f'The rule keeps models with MAE at most `MAX_MAE` ({cfg["max_mae"]:,} {u}) and time at most `MAX_MS`, then takes the smaller MAE.\n'
              '2. Only now use the test rows, once: refit the chosen model on `houses_train` and `houses_valid` together and store its MAE on `houses_test` as `test_mae`.'),
        solution='''chosen_house_model = choose_model({"linear": linear_mae, "tree": tree_mae})
both = pd.concat([houses_train, houses_valid])
models = {"linear": LinearRegression(), "tree": DecisionTreeRegressor(max_depth=4, random_state=17)}
final = make_pipeline(SimpleImputer(strategy="median"), models[chosen_house_model]).fit(both[H_FEATURES], both[H_TARGET])
test_mae = np.mean(np.abs(houses_test[H_TARGET] - final.predict(houses_test[H_FEATURES])))
print(chosen_house_model, test_mae)
'''))
    # ------------------------------------------------------------ Question 2: machine failure (classification)
    out.append(dict(key='clean_m', question=2, title='Clean the machine table', marks=dict(clean_m=marks['clean_m']), inputs=['machines_raw'], results=['machines'],
        text=('Start from a copy: `machines = machines_raw.copy()`. Then:\n'
              '1. Remove duplicate rows.\n'
              '2. Remove the rows with no label (`M_TARGET`).\n'
              '3. Remove the rows with an impossible value: `torque_nm` and `rotation_speed_rpm` must be above 0.\n'
              '4. Change `product_type` to a number (L = 0, M = 1, H = 2).\n\n'
              'Leave the other missing values for the imputer.'),
        solution='''machines = machines_raw.copy()
machines = machines.drop_duplicates()
machines = machines.dropna(subset=[M_TARGET])
machines = machines[(machines["torque_nm"] > 0) & (machines["rotation_speed_rpm"] > 0)].copy()
machines["product_type"] = machines["product_type"].map({"L": 0, "M": 1, "H": 2})
print(machines_raw.shape, machines.shape)
'''))
    out.append(dict(key='split_m', question=2, title='Split the machines into training, validation and test sets', marks=dict(split_m=marks['split_m']), inputs=['machines'],
        results=['machines_train', 'machines_valid', 'machines_test'],
        text=(f'The same four lines as Task 2, for `machines` (`random_state={s}`): `machines_test`, `machines_rest`, `machines_valid`, `machines_train`. '
              'Do not use the test rows until Task 8.'),
        solution=f'''machines_test = machines.sample(frac=0.2, random_state={s})
machines_rest = machines.drop(machines_test.index)
machines_valid = machines_rest.sample(frac=0.25, random_state={s})
machines_train = machines_rest.drop(machines_valid.index)
print(len(machines_train), len(machines_valid), len(machines_test))
'''))
    out.append(dict(key='classify', question=2, title='Logistic regression and a decision tree', marks=dict(classify=marks['classify'], scores=marks['scores']),
        inputs=['machines_train', 'machines_valid'],
        results=['logistic_proba', 'logistic_warn', 'tree_warn', 'logistic_counts', 'tree_counts', 'logistic_precision', 'logistic_recall', 'logistic_f1',
                 'tree_precision', 'tree_recall', 'tree_f1'],
        text=('A warning means a failure: `M_TARGET >= M_LIMIT`. Fit two models on `machines_train` (columns `M_FEATURES`):\n'
              '1. Logistic regression: `make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000))`. '
              'Store the probability of a failure for each `machines_valid` row as `logistic_proba`, and the warnings at `THRESHOLD` (0.5 or more) as `logistic_warn`.\n'
              '2. Decision tree: `make_pipeline(SimpleImputer(strategy="median"), DecisionTreeClassifier(max_depth=3, random_state=17))`. Store its predictions as `tree_warn`.\n'
              '3. For each model: the counts `confusion_matrix(actual, warned, labels=[0, 1]).ravel()` (tn, fp, fn, tp), precision, recall and F1 (0 when a count is zero).'),
        solution='''y_train_warn = (machines_train[M_TARGET] >= M_LIMIT).astype(int)
y_valid_warn = (machines_valid[M_TARGET] >= M_LIMIT).astype(int)
logistic = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000)).fit(machines_train[M_FEATURES], y_train_warn)
logistic_proba = logistic.predict_proba(machines_valid[M_FEATURES])[:, 1]
logistic_warn = (logistic_proba >= THRESHOLD).astype(int)
tree_clf = make_pipeline(SimpleImputer(strategy="median"), DecisionTreeClassifier(max_depth=3, random_state=17)).fit(machines_train[M_FEATURES], y_train_warn)
tree_warn = tree_clf.predict(machines_valid[M_FEATURES])
logistic_counts = confusion_matrix(y_valid_warn, logistic_warn, labels=[0, 1]).ravel()
tree_counts = confusion_matrix(y_valid_warn, tree_warn, labels=[0, 1]).ravel()
logistic_precision = precision_score(y_valid_warn, logistic_warn, zero_division=0)
logistic_recall = recall_score(y_valid_warn, logistic_warn, zero_division=0)
logistic_f1 = f1_score(y_valid_warn, logistic_warn, zero_division=0)
tree_precision = precision_score(y_valid_warn, tree_warn, zero_division=0)
tree_recall = recall_score(y_valid_warn, tree_warn, zero_division=0)
tree_f1 = f1_score(y_valid_warn, tree_warn, zero_division=0)
print(logistic_counts, logistic_f1, tree_counts, tree_f1)
'''))
    out.append(dict(key='test_m', question=2, title='Choose the warning model, then use the test set once', marks=dict(test_m=marks['test_m']),
        inputs=['machines_train', 'machines_valid', 'machines_test', 'logistic_f1', 'tree_f1'], results=['chosen_warning_model', 'test_f1'],
        text=('1. Run `chosen_warning_model = choose_warning_model({"logistic": logistic_f1, "tree": tree_f1})`. The rule takes the higher validation F1 '
              '(a tie goes to logistic regression, the simpler model).\n'
              '2. Only now use the test rows, once: refit the chosen model on `machines_train` and `machines_valid` together and store its F1 on `machines_test` as `test_f1`.'),
        solution='''chosen_warning_model = choose_warning_model({"logistic": logistic_f1, "tree": tree_f1})
mboth = pd.concat([machines_train, machines_valid])
warning_models = {"logistic": make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000)),
                  "tree": make_pipeline(SimpleImputer(strategy="median"), DecisionTreeClassifier(max_depth=3, random_state=17))}
final_warn = warning_models[chosen_warning_model].fit(mboth[M_FEATURES], (mboth[M_TARGET] >= M_LIMIT).astype(int))
if chosen_warning_model == "logistic":
    test_warn = (final_warn.predict_proba(machines_test[M_FEATURES])[:, 1] >= THRESHOLD).astype(int)
else:
    test_warn = final_warn.predict(machines_test[M_FEATURES])
test_f1 = f1_score((machines_test[M_TARGET] >= M_LIMIT).astype(int), test_warn, zero_division=0)
print(chosen_warning_model, test_f1)
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
    data = ''
    return f"""{head}
{task['text']}{data}

**Input:** {', '.join('`' + n + '`' for n in task['inputs'])}. **Store:** {', '.join('`' + n + '`' for n in task['results'])}."""


def memo_markdown(code, cfg=P.EXAM, task_no=7):
    limit_opts, next_opts = options(code)
    lim = '\n'.join(f'- **{letter}.** {text}' for letter, text, _, _ in limit_opts)
    nxt = '\n'.join(f'- **{letter}.** {text}' for letter, text, _, _ in next_opts)
    return f'''## Task {task_no}: Part B, the decision memo form ({K.PART_B_MAX} automatic marks)
Fill in `MEMO` in the next cell, for {PAYER}. Use your own numbers, with at least two decimals (MAE in {cfg['h_unit']}, F1 from 0 to 1).

| Field | Enter | Marks |
|---|---|---|
| `house_model` | `"linear"` or `"tree"`: the house model the rule chose in Task 4. | 2 |
| `house_validation_mae` | The validation MAE of each house model, from your notebook. | 2 |
| `warning_model` | `"logistic"` or `"tree"`: the warning model the rule chose in Task 8. | 2 |
| `warning_validation_f1` | The validation F1 of each warning model, from your notebook. | 1 |
| `test_mae`, `test_f1` | The house test MAE (Task 4) and the warning test F1 (Task 8). | 2 |
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
    "house_model": "",                                       # "linear" or "tree"
    "house_validation_mae": {"linear": None, "tree": None},  # your validation MAE values, in UNIT
    "warning_model": "",                                     # "logistic" or "tree"
    "warning_validation_f1": {"logistic": None, "tree": None},   # your validation F1 values (0 to 1)
    "test_mae": None,                                        # test_mae from Task 4, in UNIT
    "test_f1": None,                                         # test_f1 from Task 8 (0 to 1)
    "limits": ["", "", ""],                                  # three different letters from the Limits list
    "next_step": "",                                         # one letter from the Next step list
    "answer_choice": "",                                     # one or two sentences
    "answer_test_set": "",                                   # one or two sentences
}
'''

NAMES_OF = {'linear': 'linear regression', 'tree': 'decision tree'}


def memo_solution(code, cfg=P.EXAM):
    """A model memo: numbers calculated from the notebook, the true limits, the right next step and two good written answers (typed as plain text)."""
    limit_opts, next_opts = options(code)
    limits = [letter for letter, _, ok, _ in limit_opts if ok][:3]
    nxt = [letter for letter, _, ok, _ in next_opts if ok][0]
    n = numbers(cfg)
    vm, chosen, unit = n['p']['validation_mae'], n['chosen'], cfg['h_unit']
    other = 'tree' if chosen == 'linear' else 'linear'
    a1 = (f"I recommend the {NAMES_OF[chosen]} because its validation MAE of {vm[chosen]:.0f} {unit} on the validation houses is lower than the "
          f"{NAMES_OF[other]} ({vm[other]:.0f} {unit}), and it meets the client limit.")
    a2 = ("The test set is used only once, at the end, so that it stays an honest estimate on rows the model has never seen; if we used it to choose or tune the model, "
          "information would leak and the test score would be optimistic.")
    return f'''MEMO = {{
    "house_model": chosen_house_model,
    "house_validation_mae": {{"linear": round(float(linear_mae), 3), "tree": round(float(tree_mae), 3)}},
    "warning_model": chosen_warning_model,
    "warning_validation_f1": {{"logistic": round(float(logistic_f1), 3), "tree": round(float(tree_f1), 3)}},
    "test_mae": round(float(test_mae), 3),
    "test_f1": round(float(test_f1), 3),
    "limits": {limits!r},
    "next_step": {nxt!r},
    "answer_choice": {a1!r},
    "answer_test_set": {a2!r},
}}
'''


# ------------------------------------------------------------------------------------------------ rehearsal self-study notes
# Short notes for a student who missed the revision class, at most 4 bullets each, right before the task that needs them.
REHEARSAL_NOTES = {
    'clean_h': '''### Note: cleaning
- **Duplicate rows** are the same record entered twice; they count one sale or one machine run twice. `drop_duplicates()` keeps the first copy.
- A row with **no target value** cannot teach the model anything: remove it with `dropna(subset=[...])`.
- An **impossible value** (an area of 0 or less, a house built after the sale) is a recording error: keep only the rows that pass the rule, for example `houses[houses["living_area_m2"] > 0]`.
- Missing values in other columns stay: the imputer fills them later, learning only from the training rows.''',
    'split_h': '''### Note: training, validation and test sets
- The model learns from `train`, we compare models on `valid`, and `test` gives one honest estimate at the end.
- `sample(frac=0.2, random_state=29)` picks the same random rows every time, so everyone gets the same split (the project uses 17, so its numbers differ from these).
- If we chose or tuned the model on the test rows, they would stop being unseen and the score would look better than it really is (**leakage**).
- Slides: Class 3, "Train-test contamination: validation rows in the training set make the score look perfect".''',
    'regression': '''### Note: fit on the training rows only
- Every number learned from data (the imputation medians, the model itself) comes from `train` only, then is applied to `valid`.
- `make_pipeline(SimpleImputer(strategy="median"), model)` does this: it learns in `fit` and reuses in `predict`.
- Learning from all rows lets the model see the rows it is judged on, so the error looks too small.
- Slides: Class 3, "The pipeline rule: fit on the training set only, then apply the same numbers".''',
    'encoded': '''### Note: one-hot encoding (shown in the revision class)
- A model needs numbers. **One-hot encoding** turns a text column into one 0 or 1 column per category: `neighbourhood` "NAmes" becomes a 1 in the column `neighbourhood_NAmes`.
- Like the medians, the categories are learned from `houses_train` only: the pipeline learns them in `fit` and reuses them in `predict`.
- A category that never appears in `houses_train` has no column; `handle_unknown="ignore"` gives it all zeros instead of an error.
- `SimpleImputer(strategy="most_frequent")` fills a missing text value with the commonest category in `houses_train`.''',
    'classify': '''### Note: logistic regression, a decision tree, the confusion matrix and F1
- **Logistic regression** gives each row a probability between 0 and 1 (`predict_proba(X)[:, 1]`); warn when it is at least 0.5. A **decision tree** answers 0 or 1 directly with `predict`.
- **Confusion matrix:** TP right warning, FP false alarm, FN missed failure, TN rightly none; `confusion_matrix(actual, warned, labels=[0, 1]).ravel()` gives tn, fp, fn, tp.
- **Precision** = TP / (TP + FP); **recall** = TP / (TP + FN); **F1** balances the two: 2 x precision x recall / (precision + recall). A zero denominator gives 0.
- Slides: Class 2, "Logistic regression in three lines", "The confusion matrix counts true and false positives and negatives" and the decision tree classifier.''',
    'test_h': '''### Note: use the test set once, then stop
- The validation set chooses the model; the test set gives **one honest estimate** of the chosen one.
- Looking at the test set and then changing your choice makes its score too good to trust.
- Refit on the training and validation rows together (more data), then measure on the test rows once. Question 2 does the same in Task 8.
- Slides: Class 3, "We choose max_depth on the validation set and keep the test set sealed".''',
}
