# ML15 Instructor guide: A complete regression experiment

Private. Keep this file out of the student folder.

**Objective.** By the end: you can split data, fit a model and a baseline on the training part, and compare their errors on held-out homes.

**Question of the day.** Does the rent model beat a plain guess on homes it has never seen?

Prerequisite: ML14 Predicting a number with a line.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

Where it overruns: The unpacking of four names into one line is the hardest part. Draw the four boxes on the board before running.

## Block A. Split the homes

Keep a quarter of the 120 homes back. The model must never see them while it learns.

Ask for the prediction first: Predict how many homes go to training and how many to testing.

```python
import pandas as pd
from sklearn.model_selection import train_test_split
homes = pd.read_csv("synthetic_homes.csv")
X = homes[["area_m2", "rooms"]]
y = homes["rent_ugx"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=7)
print(len(X_train), len(X_test))
```

Correct result: The cell prints 90 and 30. The four names on the left receive training inputs, test inputs, training targets and test targets, in that order. random_state=7 fixes the shuffle so everyone gets the same split.

Investigate, with answers:

- Why do we shuffle before splitting? Answer: The file may be in an order that puts similar homes together. A shuffle gives both parts a fair mix.
- Which of the four names would hold the answers you must not peek at? Answer: y_test.

Modify: Change test_size to 0.2 and run the split again. Answer: 96 homes train and 24 test.

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)
```

## Block B. Baseline against model

Fit a mean-guess baseline and a line on the 90 training homes. Measure both on the 30 held-out homes.

Ask for the prediction first: Predict whether the model's average miss will be smaller than the baseline's, and by roughly how much.

```python
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
baseline = DummyRegressor(strategy="mean").fit(X_train, y_train)
model = LinearRegression().fit(X_train, y_train)
baseline_mae = mean_absolute_error(y_test, baseline.predict(X_test))
model_mae = mean_absolute_error(y_test, model.predict(X_test))
print(round(baseline_mae), round(model_mae))
```

Correct result: The cell prints 110169 and 11889. The baseline misses by about UGX 110169 and the model by about UGX 11889, so on these 30 held-out homes the model is far better. Mean absolute error averages the misses and uses the unit of the target, shillings. The model wins by this much because the homes were generated from a formula, which makes them easy to learn. Real data would not be so kind.

Investigate, with answers:

- What does a mean absolute error of 11889 mean in words? Answer: On average the model's rent estimate is about UGX 11889 away from the real rent.
- Why is this result no evidence about real rents? Answer: The homes are invented from a neat formula, so any line fits them well.

Modify: Fit a model using only area_m2 and print its error. Answer: About UGX 28272, worse than with rooms too.

```python
area_only = LinearRegression().fit(X_train[["area_m2"]], y_train)
area_mae = mean_absolute_error(y_test, area_only.predict(X_test[["area_m2"]]))
```

## Make: reference

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
homes = pd.read_csv("synthetic_homes.csv")
X = homes[["area_m2", "rooms"]]
y = homes["rent_ugx"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=7)
baseline_mae = mean_absolute_error(y_test, DummyRegressor(strategy="mean").fit(X_train, y_train).predict(X_test))
model_mae = mean_absolute_error(y_test, LinearRegression().fit(X_train, y_train).predict(X_test))
print(round(baseline_mae), round(model_mae))
```

Evidence to collect: ML15.ipynb with both errors, the sentence that the model beats the baseline on held-out homes, and the split unchanged.

## Misconceptions to listen for

- Changing random_state until the score looks good is fine.
- The model is tested on the training homes.
- A low error on invented data proves real accuracy.

## Questions to ask, with expected answers

- Why report the baseline error next to the model error? Expected: Without it nobody knows whether the model is better than a plain guess.
- What is held out? Expected: Rows the model never saw while it learned.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
