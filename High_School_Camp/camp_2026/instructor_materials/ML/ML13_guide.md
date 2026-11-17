# ML13 Instructor guide: Features, targets and an honest baseline

Private. Keep this file out of the student folder.

**Objective.** By the end: you can name the features and the target in a table, and calculate a baseline error that any model must beat.

**Question of the day.** What did the session 1 model learn from, and how well would a plain guess do?

**Where this is used.** Banks and mobile lenders use models to flag unusual payments, and they first ask whether the model beats a plain rule. That plain rule is the baseline. What plain guess would you make for tomorrow's weather?

Prerequisite: ML12 Show your first chart and choose your project question.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

## Block A. The baseline guess

A baseline uses no features at all. It guesses the average of the training targets every time.

Ask for the prediction first: Training prices are 2000, 4000 and 6000. Predict the baseline guess and its error when the real price is 5000.

```python
train_prices = [2000, 4000, 6000]
baseline = sum(train_prices) / len(train_prices)
actual = 5000
error = abs(actual - baseline)
print(baseline, error)
```

Correct result: The cell prints 4000.0 and 1000.0. The training mean 4000.0 is the baseline guess. abs removes the minus sign, so the error is the distance between the guess and the real value, 1000 shillings. A model is worth using only if its errors on unseen examples are smaller than the baseline's.

Investigate, with answers:

- Why must the baseline use only training prices? Answer: Test prices are answers the model has not seen. Using them would be a form of leakage.
- What would the baseline guess be for every new price? Answer: 4000.0, the same number each time.

Modify: Change the actual price to 3000 and recalculate the error. Answer: The error is 1000.0 again, because 3000 is also 1000 below 4000.

```python
actual = 3000
error = abs(actual - baseline)
```

## Block B. Open the session 1 model

The model from session 1 had one feature and one target. Print what it learned.

Ask for the prediction first: Name the feature and the target in this code before you run it.

```python
import pandas as pd
from sklearn.linear_model import LinearRegression
homes = pd.read_csv("synthetic_homes.csv")
X = homes[["area_m2"]]
y = homes["rent_ugx"]
model = LinearRegression().fit(X, y)
slope = model.coef_[0]
intercept = model.intercept_
print(round(slope), round(intercept))
```

Correct result: The cell prints 2996 and 159436. The feature is area_m2, kept in X. The target is rent_ugx, kept in y. fit looked at all 120 homes and found a line: rent is about 159436 shillings plus 2996 shillings for each square metre. That model was scored on nothing at all. Judging it on the same homes it learned from would flatter it, so next session we keep some homes back.

Investigate, with answers:

- Which of these is the feature and which is the target? Answer: area_m2 is the feature, rent_ugx is the target.
- Why is it unfair to test the model on the same 120 homes? Answer: It has already seen their answers. A fair check needs homes it has not seen.

Modify: Add rooms as a second feature and print the two slopes. Answer: About 2992 shillings per square metre and 19345 shillings per room.

```python
X2 = homes[["area_m2", "rooms"]]
model2 = LinearRegression().fit(X2, y)
slopes = [round(model2.coef_[0]), round(model2.coef_[1])]
```

## Make: reference

```python
train_values = [2000, 4000, 6000]
baseline = sum(train_values) / len(train_values)
error = abs(5000 - baseline)
print(baseline, error)
# 4000.0 and 1000.0. The final payment amount would give away the selling price: leakage.
```

Build log entry to look for: ML13.ipynb with baseline 4000.0, error 1000.0, and one named leaked feature.

## Misconceptions to listen for

- The model should be tested on the homes it learned from.
- The baseline is a poor attempt at a model.
- Any column in the table is a fair input.

## Questions to ask, with expected answers

- What are the feature and target in the session 1 model? Expected: Feature: area_m2. Target: rent_ugx.
- What counts as leakage in a rent model? Expected: Any column only known after the rent is agreed, such as the first month's payment received.

## Online version

For a hybrid group. The live class is 90 minutes on video with screen sharing. The learner finishes the build in their own time, about an hour. The full rules are in handbook/HYBRID_DELIVERY.md.

### Live clock, 90 minutes

| Minutes | Activity |
|---|---|
| 5 | Recall: three questions on paper, then say the answers aloud |
| 35 | Block A, The baseline guess: predict, run, investigate. The Modify step moves to the build task. |
| 5 | Break away from the screen |
| 35 | Block B, Open the session 1 model: predict, run, investigate. The Modify step moves to the build task. |
| 10 | Close: say the exit sentence aloud, then the build task is set |

### After-class build task, about an hour

1. Modify, Block A (The baseline guess): Change the actual price to 3000 and recalculate the error.
2. Modify, Block B (Open the session 1 model): Add rooms as a second feature and print the two slopes.
3. Make: For training values [2000, 4000, 6000], find the baseline guess for a new item. If its real value is 5000, calculate the absolute error. Name one leaked feature if you were predicting a selling price.

When you finish, write two sentences: what you changed and how you checked it. Add a build log entry. Send a photo of your work or the notebook by the route the organiser sets, before the next class.

### Next class

In the next class recall, ask: What are the feature and target in the session 1 model? Expected: Feature: area_m2. Target: rent_ugx.

## Build log and feedback

Look at what each of the five learners saved and note one strength and one next step for each. Share them kindly and privately. Nothing is scored or ranked. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and show-and-tells need your judgement.
