"""One source of truth for the Engineering ML project: course facts, the data, the tasks (text, starter and model solution), the
Part B memo form, the marks and the window rules. The notebooks, the rehearsal, the briefs and the marking guide are built from this file.

Plain code (lecturer's redesign of 14 November 2026): students write ordinary straight-line code, no function placeholders. Each task
names its INPUT variables and the RESULT names to store. The grader re-runs each task's cells on hidden inputs (own_cells.py).
ONE supplied code cell, "Setup: run me first": the two tables as students receive them (organised, with the added problems) packed inside it
with a SHA-256 check (saved as houses.csv and machines.csv), the silent backup and the clock. Everything students use (imports, column names,
model-choosing rules) is in visible supplied cells at the step that first needs it (lecturer, 17 November 2026).
"""
import base64
import bz2
import csv
import hashlib
import io
import json
import re
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
# Save the two tables as CSV files next to this notebook: the cells below read them.
for _name in ("houses", "machines"):
    with open(_name + ".csv", "w") as _file:
        _file.write(_data[_name])
print("Data ready: houses.csv and machines.csv")
""" + PL.backup_code() + PL.countdown_code()


# ------------------------------------------------------------------------------------------------ the data, introduced to students
def data_markdown():
    """The cell right after Setup: what the two tables are, every column in plain words, and the problems added for cleaning."""
    hp, mp = P.H_PROBLEMS, P.M_PROBLEMS
    return f'''## The data
Setup saves two tables as CSV files (`houses.csv`, `machines.csv`); the supplied cell below this one reads the houses, and the machines are read at the start of Question 2. Each target is named in Task 1 and Task 5, after you have looked at the data. Both are real published data, organised for this project. **A few problems were added on purpose** for you to clean. Question 1 (Tasks 1 to 4) uses only the houses; Question 2 (Tasks 5 to 8) uses only the machines.

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
'''# IUEA-SUPPLIED gd-houses: do not edit. Just run this cell; it is not marked.
# if Tasks 1 and 2 have not made houses_train yet, say so instead of failing
if "houses_train" not in globals():
    print("Do Tasks 1 and 2 first: this cell needs houses_train.")      # a friendly message instead of an error
else:                             # otherwise, run gradient descent
    # the imputer fills missing values with the training medians
    gd_imputer = SimpleImputer(strategy="median")
    # the scaler standardises every feature (mean 0, standard deviation 1)
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
    for epoch in range(epochs):       # repeat once per epoch: predict, measure the loss, step downhill
        gd_guess = gd_X @ gd_w + gd_b                 # the model's price for every training house: b + w1 x1 + w2 x2 + ...
        gd_gap = gd_guess - gd_y                      # how far off each guess is
        gd_losses.append(np.mean(gd_gap ** 2))        # the loss: mean squared error (MSE)
        gd_errors.append(np.mean(np.abs(gd_gap)))     # the training MAE, in thousand USD
        gd_w = gd_w - learning_rate * 2 * (gd_X.T @ gd_gap) / len(gd_y)   # new w = old w - learning rate x slope of the loss
        gd_b = gd_b - learning_rate * 2 * np.mean(gd_gap)              # the same step for the intercept

    # the loss at the first and the last epoch
    print("Loss (MSE) at the start:", round(gd_losses[0]), "| after", epochs, "epochs:", round(gd_losses[-1]))
    # the training MAE at the first and the last epoch
    print("Training MAE at the start:", round(gd_errors[0], 1), "thousand USD | after", epochs, "epochs:", round(gd_errors[-1], 1))

    # Chart: the loss at each epoch
    plt.figure()
    # one point per epoch, joined by a line
    plt.plot(gd_losses)
    plt.title("Gradient descent: the training loss falls epoch by epoch")   # the chart title
    plt.xlabel("Epoch")                                    # the label under the horizontal axis
    plt.ylabel("Loss: MSE (thousand USD, squared)")        # the label beside the vertical axis, with its unit
    # draw the chart
    plt.show()

    # Regression has no accuracy (a price is never exactly right or wrong): its training curve is the error at each epoch
    plt.figure()
    # the training MAE at each epoch
    plt.plot(gd_errors)
    plt.title("Training error at each epoch (lower is better)")             # the chart title
    plt.xlabel("Epoch")                                    # the label under the horizontal axis
    plt.ylabel("Training MAE (thousand USD)")              # the label beside the vertical axis, with its unit
    # draw the chart
    plt.show()

    # The learned weights: gradient descent next to LinearRegression, on the same standardised features
    # LinearRegression solves the same problem directly, with the least-squares formula (no epochs)
    gd_check = LinearRegression().fit(gd_X, gd_y)
    # a table: one row per feature, the weight from each method side by side
    gd_weights = pd.DataFrame({"feature": H_FEATURES, "gradient descent": gd_w, "LinearRegression": gd_check.coef_})
    # show it, rounded to 2 decimals
    display(gd_weights.round(2))
    # the two intercepts
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
'''# IUEA-SUPPLIED gd-machines: do not edit. Just run this cell; it is not marked.
# if Tasks 5 and 6 have not made machines_train yet, say so instead of failing
if "machines_train" not in globals():
    print("Do Tasks 5 and 6 first: this cell needs machines_train.")    # a friendly message instead of an error
else:                             # otherwise, run gradient descent
    # the imputer fills missing values with the training medians
    gd2_imputer = SimpleImputer(strategy="median")
    # the scaler standardises every feature (mean 0, standard deviation 1)
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
    for epoch in range(epochs):       # repeat once per epoch: predict, measure the loss, step downhill
        gd2_chance = 1 / (1 + np.exp(-(gd2_X @ gd2_w + gd2_b)))   # the sigmoid: a chance of failure from 0 to 1
        gd2_losses.append(-np.mean(gd2_y * np.log(gd2_chance) + (1 - gd2_y) * np.log(1 - gd2_chance)))   # log loss
        gd2_accuracy.append(np.mean((gd2_chance >= 0.5) == gd2_y))   # share of training runs called right at threshold 0.5
        gd2_w = gd2_w - learning_rate * (gd2_X.T @ (gd2_chance - gd2_y)) / len(gd2_y)   # new w = old w - learning rate x slope
        gd2_b = gd2_b - learning_rate * np.mean(gd2_chance - gd2_y)     # the same step for the intercept

    # the log loss at the first and the last epoch
    print("Log loss at the start:", round(gd2_losses[0], 3), "| after", epochs, "epochs:", round(gd2_losses[-1], 3))
    # the training accuracy at the first and the last epoch
    print("Training accuracy at the start:", round(gd2_accuracy[0], 3), "| after", epochs, "epochs:", round(gd2_accuracy[-1], 3))

    # Chart: the log loss at each epoch
    plt.figure()
    plt.plot(gd2_losses)                                   # one point per epoch, joined by a line
    plt.title("Gradient descent: the training log loss falls epoch by epoch")   # the chart title
    plt.xlabel("Epoch")                                    # the label under the horizontal axis
    plt.ylabel("Log loss")                                 # the label beside the vertical axis
    # draw the chart
    plt.show()

    # Chart: the training accuracy at each epoch
    plt.figure()
    plt.plot(gd2_accuracy)                                 # one point per epoch, joined by a line
    plt.title("Training accuracy at each epoch")                            # the chart title
    plt.xlabel("Epoch")                                    # the label under the horizontal axis
    plt.ylabel("Training accuracy")                        # the label beside the vertical axis (0 to 1)
    # draw the chart
    plt.show()

    # The learned weights: gradient descent next to LogisticRegression, on the same standardised features
    # (LogisticRegression adds a small penalty, so its weights are close, not equal)
    # LogisticRegression on the same standardised features
    gd2_check = LogisticRegression(max_iter=1000).fit(gd2_X, gd2_y)
    # a table: one row per feature, the weight from each method side by side
    gd2_weights = pd.DataFrame({"feature": M_FEATURES, "gradient descent": gd2_w, "LogisticRegression": gd2_check.coef_[0]})
    # show it, rounded to 2 decimals
    display(gd2_weights.round(2))
    # the two intercepts
    print("Intercept, gradient descent:", round(gd2_b, 2), "| LogisticRegression:", round(gd2_check.intercept_[0], 2))
''', '''**How to read the two charts and the weights table**
- **Accuracy starts near 0.03:** with every weight at 0, every run gets a chance of 0.5, so the model warns about every run and is right only for the few that failed. Within a few epochs it reaches about 0.97 by saying "no failure" to almost every run. Failures are rare, so accuracy looks good even when most failures are missed: that is why we choose the warning model by **F1**.
- **Weights:** each is the change in the log-odds of a failure when that feature rises by one standard deviation (the others held fixed). A positive weight makes a failure more likely; a negative one less likely. On one scale, a bigger weight (ignoring the sign) means a feature matters more.
- The two columns are close: gradient descent ends near where `LogisticRegression()` lands.'''),
}


# Visible supplied cells (lecturer, 17 November 2026): reading the data and naming the columns happen in plain sight, at the stage where they
# are used, not inside Setup. They are filled in and marked "# IUEA-SUPPLIED <id>:"; the marking computer puts the original back if one is
# edited and defines the same names itself if one is deleted (grading_defaults). The two read cells sit OUTSIDE every task section (before
# Task 1, and under the Question 2 heading, which belongs to Task 4's section and does not touch its results), so a hidden-data rerun of a
# task never reads the visible files over its hidden inputs.
SUPPLIED_RE = r'# IUEA-SUPPLIED ([a-z-]+):'
SUPPLIED_HEAD = '# IUEA-SUPPLIED {id}: do not edit. Just run this cell; it is not marked.\n'


def visible_cells(cfg=P.EXAM):
    """{id: (where, source)}. where: 'data' (after The data), 'question2' (under the Question 2 heading) or a task key (before the student's cell)."""
    head = lambda i: SUPPLIED_HEAD.format(id=i)
    return {
        'imports-data': ('data', head('imports-data') + '''# The tools for working with data. "as pd" lets us write pd instead of pandas, and so on.
# numbers and arrays
import numpy as np
# tables (DataFrames): read, look at and clean the data
import pandas as pd
# charts
import matplotlib.pyplot as plt
'''),
        'data-houses': ('data', head('data-houses') + f'''# read the house table from the CSV file that Setup saved: one row per sale
houses_raw = pd.read_csv("houses.csv")
# the size of the table: (rows, columns)
print("houses_raw:", houses_raw.shape)
'''),
        'target-houses': ('clean_h:2', head('target-houses') + f'''# Having looked at the data, decide what we predict: the target (y). Question 1 predicts the sale price, in {cfg["h_unit"]}.
H_TARGET = {cfg["h_target"]!r}
# check that the column exists, and how many prices are missing (cleaning removes those rows: they cannot teach the model)
print("target:", H_TARGET, "| missing prices:", houses_raw[H_TARGET].isna().sum())
'''),
        'data-machines': ('question2', head('data-machines') + f'''# read the machine table from the CSV file that Setup saved: one row per run
machines_raw = pd.read_csv("machines.csv")
# the size of the table: (rows, columns)
print("machines_raw:", machines_raw.shape)
'''),
        'target-machines': ('clean_m:2', head('target-machines') + f'''# Having looked at the data, decide what we predict: the target (y). Question 2 predicts whether a run fails.
M_TARGET = {cfg["m_target"]!r}
# a run counts as a failure when M_TARGET is at or above this limit
M_LIMIT = {cfg["m_limit"]!r}
# check that the column exists, and how many labels are missing (cleaning removes those rows)
print("target:", M_TARGET, "| missing labels:", machines_raw[M_TARGET].isna().sum())
'''),
        'imports-houses': ('regression', head('imports-houses') + '''# The scikit-learn tools for the house models, imported now that we are ready to train
# make_pipeline joins the steps (fill gaps, scale, model) into one model
from sklearn.pipeline import make_pipeline
# SimpleImputer fills missing values with a number learned from the training rows (for example the median)
from sklearn.impute import SimpleImputer
# StandardScaler puts every feature on the same scale (used by the gradient descent cell below)
from sklearn.preprocessing import StandardScaler
# the first model: linear regression
from sklearn.linear_model import LinearRegression
# the second model: a decision tree for numbers (regression)
from sklearn.tree import DecisionTreeRegressor
# the error measures: MAE (mean absolute error) and MSE (mean squared error)
from sklearn.metrics import mean_absolute_error, mean_squared_error
'''),
        'features-houses': ('regression', head('features-houses') + f'''# the number columns the house models read: the features (X). The target H_TARGET is not one of them.
H_FEATURES = {cfg["h_features"]!r}
# how many features, and which
print(len(H_FEATURES), "features:", H_FEATURES)
'''),
        'imports-text': ('encoded', head('imports-text') + '''# The tools for text columns
# OneHotEncoder turns each category (word) into its own 0/1 column
from sklearn.preprocessing import OneHotEncoder
# make_column_transformer prepares the number columns and the text columns differently, in one step
from sklearn.compose import make_column_transformer
'''),
        'features-text': ('encoded', head('features-text') + f'''# the text columns Task 3b adds to the number columns
TEXT_FEATURES = {cfg["h_text"]!r}
# which text columns
print("text features:", TEXT_FEATURES)
'''),
        'imports-machines': ('classify', head('imports-machines') + '''# The scikit-learn tools for the warning models (classification)
# the first model: logistic regression (it gives the probability of a failure)
from sklearn.linear_model import LogisticRegression
# the second model: a decision tree for classes (classification)
from sklearn.tree import DecisionTreeClassifier
# the scores for a warning: the confusion matrix, precision, recall and F1
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
'''),
        'features-machines': ('classify', head('features-machines') + f'''# the columns the machine models read: the features (X). The target M_TARGET is not one of them.
M_FEATURES = {cfg["m_features"]!r}
# how many features, and which
print(len(M_FEATURES), "features:", M_FEATURES)
'''),
        'threshold-machines': ('classify:4', head('threshold-machines') + f'''# Logistic regression gives a probability of a failure (0 to 1). Now decide when a probability becomes a warning.
# warn (1) when the probability of a failure is at or above this threshold; below it, no warning (0)
THRESHOLD = {P.THRESHOLD}
# show the threshold
print("warn when the probability of a failure is at least", THRESHOLD)
'''),
        'rules-houses': ('test_h:1', head('rules-houses') + f'''# The client's requirements for the house model. These are invented teaching numbers, not real ones.
# the largest validation MAE the client accepts, in {cfg["h_unit"]}
MAX_MAE = {cfg["max_mae"]!r}
# the longest time one prediction may take, in milliseconds (ms)
MAX_MS = {P.MAX_MS}
# how long one prediction takes with each model, in ms (given to you, not measured)
LATENCY_MS = {P.LATENCY_MS!r}


# The rule that picks the house model, for example choose_model({{"linear": 22000, "tree": 28000}})
def choose_model(maes):
    # no model chosen yet
    best = None
    # look at each model in turn
    for name in maes:
        # this model's validation MAE
        mae = maes[name]
        # skip a model with no MAE, an MAE above the limit, or a prediction that is too slow
        if mae is None or mae > MAX_MAE or LATENCY_MS[name] > MAX_MS:
            continue
        # keep this model if it is the first to pass, or its MAE is smaller than the best so far
        if best is None or mae < maes[best]:
            best = name
        # on an exact tie, keep the faster model
        elif mae == maes[best] and LATENCY_MS[name] < LATENCY_MS[best]:
            best = name
    # the chosen model's name, or None when no model meets the requirements
    return best


# show the requirements
print("MAE at most", MAX_MAE, "{cfg["h_unit"]}; one prediction at most", MAX_MS, "ms; prediction times:", LATENCY_MS)
'''),
        'rules-machines': ('test_m:1', head('rules-machines') + '''# The rule that picks the warning model, for example choose_warning_model({"logistic": 0.24, "tree": 0.25})
def choose_warning_model(f1s):
    # the decision tree only if its validation F1 is higher
    if f1s["tree"] > f1s["logistic"]:
        return "tree"
    # otherwise (also on a tie) logistic regression, the simpler model
    return "logistic"
'''),
    }


# Task 1 and Task 5 open with the student's own look at the data (step 1), BEFORE the supplied cell that names the target (step 2): a real
# project's order: read, look, decide what to predict, then clean.
EXPLORE_SOLUTION = {'clean_h': '# Step 1: look at the data\nhouses_raw.info()\n',
                    'clean_m': '# Step 1: look at the data\nmachines_raw.info()\n'}


# One text cell per numbered step, then the student's empty code cell for that step (lecturer, 17 November 2026). A step that only says
# "Run the supplied cell below" gets the supplied cell and no empty cell. Supplied cells tied to a step have where = 'task_key:step'.
RUN_ONLY = {('clean_h', 2), ('clean_m', 2), ('regression', 9), ('classify', 8)}
GD_STEP = {'regression': 9, 'classify': 8}                         # the supplied gradient descent block (SUPPLIED_CELLS) sits under this step


def task_steps(task):
    """(lead text, [step texts]) from the task text: a line starting '1. ', '2. ', ... begins a step; other lines join the step above."""
    lead, steps = [], []
    for line in task['text'].split('\n'):
        m = re.match(r'^(\d+)\. (.*)', line)
        if m:
            assert int(m.group(1)) == len(steps) + 1, (task['key'], line)
            steps.append(m.group(2))
        elif steps:
            steps[-1] += '\n' + line
        else:
            lead.append(line)
    return '\n'.join(lead).strip(), [t.strip() for t in steps]


def step_starter(k):
    return f'# Your code here (step {k})\n'


def step_markdown(k, text):
    return f'**Step {k}.** {text}'


def solution_parts(task):
    """{step: model solution code}: where the solution notebook puts its code. Tasks 1 and 5 look first (step 1) and clean after the target
    cell (step 3); Task 7 splits where THRESHOLD is first needed (step 4); every other task's code sits in its step 1 cell."""
    if task['key'] in EXPLORE_SOLUTION:
        return {1: EXPLORE_SOLUTION[task['key']], 3: task['solution']}
    if task['key'] == 'classify':
        head, tail = task['solution'].split('logistic_proba = ', 1)
        return {1: head, 4: 'logistic_proba = ' + tail}
    return {1: task['solution']}


def supplied_sources(cfg=P.EXAM):
    """{id: original source} of every supplied cell outside Setup, for the marking computer to restore."""
    out = {i: src for i, (_, src) in visible_cells(cfg).items()}
    out['gd-houses'] = SUPPLIED_CELLS['regression'][1]
    out['gd-machines'] = SUPPLIED_CELLS['classify'][1]
    return out


def grading_defaults(cfg=P.EXAM):
    """The names the visible cells define, added by the marking computer after Setup, so a deleted supplied cell costs nothing."""
    imports = ''.join(line for i, (_, src) in visible_cells(cfg).items() if i.startswith('imports-')
                      for line in src.splitlines(True) if line.startswith(('import ', 'from ')))
    return (f'''# IUEA-GRADER-DEFAULTS (added by the marking computer)
{imports}houses_raw = pd.read_csv("houses.csv")
machines_raw = pd.read_csv("machines.csv")
H_TARGET = {cfg["h_target"]!r}
M_TARGET, M_LIMIT = {cfg["m_target"]!r}, {cfg["m_limit"]!r}
H_FEATURES = {cfg["h_features"]!r}
TEXT_FEATURES = {cfg["h_text"]!r}
M_FEATURES = {cfg["m_features"]!r}
THRESHOLD = {P.THRESHOLD}
MAX_MAE, MAX_MS = {cfg["max_mae"]!r}, {P.MAX_MS}
LATENCY_MS = {P.LATENCY_MS!r}
def choose_model(maes):
    ok = [m for m in maes if maes[m] is not None and maes[m] <= MAX_MAE and LATENCY_MS[m] <= MAX_MS]
    return min(ok, key=lambda m: (maes[m], LATENCY_MS[m], m)) if ok else None
def choose_warning_model(f1s):
    return "tree" if f1s["tree"] > f1s["logistic"] else "logistic"
''')


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
        text=('Work in the order of a real project: look at the data, decide what to predict, then clean. After each cleaning step, print the shape.\n'
              '1. Look at the data: `houses_raw.head()`, `houses_raw.info()` (column types and missing values) and `houses_raw.describe()` (min and max show impossible values).\n'
              '2. Run the supplied cell below: having looked, it names the target `H_TARGET`, the column Question 1 predicts.\n'
              '3. Count the problems: duplicate rows (`.duplicated().sum()`) and rows with no price (`houses_raw[H_TARGET].isna().sum()`).\n'
              '4. Start from a copy (`houses = houses_raw.copy()`), then remove duplicate rows.\n'
              f'5. Keep only the rows that have a price (`H_TARGET`) and possible values: `living_area_m2` above 0 and `year_built` {P.LAST_YEAR} or earlier.\n'
              '6. Check the result with `houses.isna().sum()` and `houses.describe()`. Leave the other missing values: in Task 3 the imputer fills them from the training rows only.\n'
              f'7. **Chart 1:** a scatter of `{x}` (across) against `H_TARGET` (up), from `houses`, with a title, axis labels and the unit ({u}).'),
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
        text=('1. Split with exactly these four lines (60 percent training, 20 percent validation, 20 percent test):\n'
              f'`houses_test = houses.sample(frac=0.2, random_state={s})`  \n'
              '`houses_rest = houses.drop(houses_test.index)`  \n'
              f'`houses_valid = houses_rest.sample(frac=0.25, random_state={s})`  \n'
              '`houses_train = houses_rest.drop(houses_valid.index)`  \n'
              'In the same cell, print the number of rows in each set.\n'
              '2. Look at the first training rows with `houses_train.head()`. Do not use `houses_test` anywhere else until Task 4.'),
        solution=f'''houses_test = houses.sample(frac=0.2, random_state={s})
houses_rest = houses.drop(houses_test.index)
houses_valid = houses_rest.sample(frac=0.25, random_state={s})
houses_train = houses_rest.drop(houses_valid.index)
print(len(houses_train), len(houses_valid), len(houses_test))
'''))
    out.append(dict(key='regression', question=1, title='Linear regression and a decision tree', marks=dict(regression=marks['regression'], errors=marks['errors'], leakage=marks['leakage'], charts=marks['charts']),
        inputs=['houses_train', 'houses_valid'], results=['linear_pred', 'tree_pred', 'linear_mae', 'tree_mae', 'linear_rmse', 'tree_rmse'],
        text=('Train linear regression first, all the way, then the decision tree. Run the supplied cells below first: they import the scikit-learn tools and name the columns `H_FEATURES`. Use those columns and the target `H_TARGET`.\n'
              '1. Make the features and the target: `X_train` and `y_train` from `houses_train`, `X_valid` and `y_valid` from `houses_valid`. Print their shapes and the missing values in `X_train`.\n'
              '2. Linear regression: create `make_pipeline(SimpleImputer(strategy="median"), LinearRegression())` and fit it on the training rows.\n'
              '3. Read what it learned: the intercept and one weight per feature (`.named_steps["linearregression"]`, then `.intercept_` and `.coef_`).\n'
              '4. Predict the validation rows and store them as `linear_pred`. Compare a few predictions with the real prices.\n'
              f'5. Compute `linear_mae` and `linear_rmse` (the square root of the mean squared error), in {u}.\n'
              '6. Decision tree: `make_pipeline(SimpleImputer(strategy="median"), DecisionTreeRegressor(max_depth=4, random_state=17))`. Fit it and predict the validation rows '
              '(`tree_pred`).\n'
              f'7. Compute `tree_mae` and `tree_rmse`, in {u}.\n'
              f'8. **Chart 2:** a bar chart of the two MAE values, with a title, axis labels and the unit ({u}).\n'
              '9. Run the supplied cell below: it shows gradient descent learning the same weights.'),
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
        text=('A comparison only: not one of the models in Task 4. Use the columns `H_FEATURES + TEXT_FEATURES` (the supplied cells below import the text tools and name `TEXT_FEATURES`).\n'
              '1. Look at the text columns with `houses_train[TEXT_FEATURES].head()`: a model cannot use words directly.\n'
              '2. Build this pipeline. Number columns: fill gaps with the median. Text columns: fill gaps with the most frequent value, then one 0/1 column per category:\n'
              '`make_pipeline(make_column_transformer((SimpleImputer(strategy="median"), H_FEATURES), (make_pipeline(SimpleImputer(strategy="most_frequent"), '
              'OneHotEncoder(handle_unknown="ignore")), TEXT_FEATURES)), LinearRegression())`\n'
              f'3. Fit it on `houses_train`, predict `houses_valid` (`encoded_pred`) and compute `encoded_mae`, in {u}. Compare it with `linear_mae`.'),
        solution='''encoder = make_column_transformer((SimpleImputer(strategy="median"), H_FEATURES),
                                  (make_pipeline(SimpleImputer(strategy="most_frequent"), OneHotEncoder(handle_unknown="ignore")), TEXT_FEATURES))
encoded = make_pipeline(encoder, LinearRegression()).fit(houses_train[H_FEATURES + TEXT_FEATURES], houses_train[H_TARGET])
encoded_pred = encoded.predict(houses_valid[H_FEATURES + TEXT_FEATURES])
encoded_mae = np.mean(np.abs(houses_valid[H_TARGET] - encoded_pred))
print(encoded_mae, linear_mae)
'''))
    out.append(dict(key='test_h', question=1, title='Choose the house model, then use the test set once', marks=dict(test_h=marks['test_h']),
        inputs=['houses_train', 'houses_valid', 'houses_test', 'linear_mae', 'tree_mae'], results=['chosen_house_model', 'test_mae'],
        text=('1. Run the supplied cell below: it states the client\'s limits and defines `choose_model`. Then choose on validation numbers only: `chosen_house_model = choose_model({"linear": linear_mae, "tree": tree_mae})`. '
              f'The rule keeps models with MAE at most `MAX_MAE` ({cfg["max_mae"]:,} {u}) and time at most `MAX_MS`, then takes the smaller MAE.\n'
              '2. Only now: refit the chosen model (the same pipeline as in Task 3) on `houses_train` and `houses_valid` together (`pd.concat`).\n'
              f'3. Use the test rows once: predict `houses_test` and store its MAE as `test_mae`, in {u}.'),
        solution='''chosen_house_model = choose_model({"linear": linear_mae, "tree": tree_mae})
both = pd.concat([houses_train, houses_valid])
models = {"linear": LinearRegression(), "tree": DecisionTreeRegressor(max_depth=4, random_state=17)}
final = make_pipeline(SimpleImputer(strategy="median"), models[chosen_house_model]).fit(both[H_FEATURES], both[H_TARGET])
test_mae = np.mean(np.abs(houses_test[H_TARGET] - final.predict(houses_test[H_FEATURES])))
print(chosen_house_model, test_mae)
'''))
    # ------------------------------------------------------------ Question 2: machine failure (classification)
    out.append(dict(key='clean_m', question=2, title='Clean the machine table', marks=dict(clean_m=marks['clean_m']), inputs=['machines_raw'], results=['machines'],
        text=('The same order as Task 1, for the machines. After each cleaning step, print the shape.\n'
              '1. Look at the data: `machines_raw.head()`, `machines_raw.info()` and `machines_raw.describe()`.\n'
              '2. Run the supplied cell below: having looked, it names the target `M_TARGET` and the failure limit `M_LIMIT`.\n'
              '3. Count duplicate rows and rows with no label (`M_TARGET`).\n'
              '4. Start from a copy (`machines = machines_raw.copy()`), then remove duplicate rows.\n'
              '5. Keep only the rows that have a label and possible values: `torque_nm` and `rotation_speed_rpm` above 0. Leave the other missing values for the imputer.\n'
              '6. Change `product_type` to a number (L = 0, M = 1, H = 2) and check with `machines.head()`.'),
        solution='''machines = machines_raw.copy()
machines = machines.drop_duplicates()
machines = machines.dropna(subset=[M_TARGET])
machines = machines[(machines["torque_nm"] > 0) & (machines["rotation_speed_rpm"] > 0)].copy()
machines["product_type"] = machines["product_type"].map({"L": 0, "M": 1, "H": 2})
print(machines_raw.shape, machines.shape)
'''))
    out.append(dict(key='split_m', question=2, title='Split the machines into training, validation and test sets', marks=dict(split_m=marks['split_m']), inputs=['machines'],
        results=['machines_train', 'machines_valid', 'machines_test'],
        text=(f'1. The same four lines as Task 2, for `machines` (`random_state={s}`): `machines_test`, `machines_rest`, `machines_valid`, `machines_train`. '
              'In the same cell, print the number of rows in each set.\n'
              '2. Look at the first training rows with `machines_train.head()`. Do not use `machines_test` anywhere else until Task 8.'),
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
        text=('Train logistic regression first, all the way, then the decision tree. Run the supplied cells below first: they import the classification tools and name the columns `M_FEATURES`. Use those columns. A warning means a failure: `M_TARGET >= M_LIMIT`.\n'
              '1. Make `X_train` and `X_valid`, and the targets: 1 for a failure, 0 otherwise (`(... >= M_LIMIT).astype(int)`). Print how many failures each set has.\n'
              '2. Logistic regression: create `make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000))` and fit it on the training rows.\n'
              '3. Read its intercept and weights (`.named_steps["logisticregression"]`).\n'
              '4. Run the supplied cell below: it sets `THRESHOLD`. Then store the probability of a failure for each `machines_valid` row as `logistic_proba` (`predict_proba(...)[:, 1]`), and the warnings at `THRESHOLD` '
              '(0.5 or more) as `logistic_warn`.\n'
              '5. Its confusion matrix: `confusion_matrix(actual, warned, labels=[0, 1])`; store `.ravel()` (tn, fp, fn, tp) as `logistic_counts`. Then compute '
              '`logistic_precision`, `logistic_recall` and `logistic_f1` (use `zero_division=0`).\n'
              '6. Decision tree: `make_pipeline(SimpleImputer(strategy="median"), DecisionTreeClassifier(max_depth=3, random_state=17))`. Fit it and store its predictions '
              'as `tree_warn`.\n'
              '7. Compute `tree_counts`, `tree_precision`, `tree_recall` and `tree_f1`.\n'
              '8. Run the supplied cell below: it shows gradient descent and the training accuracy.'),
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
        text=('1. Run the supplied cell below: it defines `choose_warning_model`. Then choose on validation numbers only: `chosen_warning_model = choose_warning_model({"logistic": logistic_f1, "tree": tree_f1})`. The rule takes the higher '
              'validation F1 (a tie goes to logistic regression, the simpler model).\n'
              '2. Only now: refit the chosen model (the same pipeline as in Task 7) on `machines_train` and `machines_valid` together.\n'
              '3. Use the test rows once: predict `machines_test` and store its F1 as `test_f1`.'),
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


def task_heading(i, task):
    """The task's own text cell: heading, the lead line, the input and the results to store. Each step follows in its own cell."""
    marks = sum(task['marks'].values())
    head = f'## Task {task.get("label", i)}: {task["title"]}' + (f' ({marks} mark{"s" if marks != 1 else ""})' if marks else '')
    lead, _ = task_steps(task)
    return f"""{head}
{lead}

**Input:** {', '.join('`' + n + '`' for n in task['inputs'])}. **Store:** {', '.join('`' + n + '`' for n in task['results'])}.""".replace('\n\n\n', '\n\n')


def task_markdown(i, task):
    marks = sum(task['marks'].values())
    head = f'## Task {task.get("label", i)}: {task["title"]}' + (f' ({marks} mark{"s" if marks != 1 else ""})' if marks else '')
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
