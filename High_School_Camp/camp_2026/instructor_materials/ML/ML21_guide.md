# ML21 Instructor guide: Compare, explain and critique

Private. Keep this file out of the student folder.

**Objective.** By the end: you can compare candidate models on the same validation rows, explain why one input is excluded, and check a coding assistant's advice with tests.

**Question of the day.** Does my model beat the baseline fairly, and can I defend each input?

**Where this is used.** When a model helps decide something about people, such as a loan, others ask why. The team must explain which inputs it used and defend them. Can you defend every input in your model?

Prerequisite: ML20 Build the project baseline.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | recall |
| 45 | build and compare |
| 15 | break |
| 20 | supervised coding-assistant critique |
| 75 | project work |
| 15 | save and exit check |

Where it overruns: The 20-minute critique replaces part of the practice block. Close the assistant before returning to project work.

## Block A. A fair comparison

Compare four options on the same 30 validation trips: the plain guess, distance only, three inputs, and three inputs plus tip. A small function keeps every comparison the same.

Ask for the prediction first: Predict which option has the lowest error, and whether you may use it.

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
fares = pd.read_csv("synthetic_fares.csv")
y = fares["fare_ugx"]

def validation_mae(columns, model):
    X = fares[columns]
    X_dev, X_test, y_dev, y_test = train_test_split(X, y, test_size=0.2, random_state=7)
    X_train, X_val, y_train, y_val = train_test_split(X_dev, y_dev, test_size=0.25, random_state=7)
    model.fit(X_train, y_train)
    return mean_absolute_error(y_val, model.predict(X_val))

base = validation_mae(["distance_km"], DummyRegressor(strategy="mean"))
distance_only = validation_mae(["distance_km"], LinearRegression())
three = validation_mae(["distance_km", "rush_hour", "raining"], LinearRegression())
with_tip = validation_mae(["distance_km", "rush_hour", "raining", "tip_ugx"], LinearRegression())
print(round(base), round(distance_only), round(three), round(with_tip))
```

Correct result: The cell prints 4361, 2415, 2255 and 1317. The model with the tip has the lowest error, and it must not be used, because the tip is known only after the trip. Among the allowed models the three-input line wins: it misses by about UGX 2255, against 4361 for the plain guess. Every option used the same split, the same 30 validation trips and the same measure, which is what makes the comparison fair. The held-back set is untouched.

Investigate, with answers:

- Why is the lowest error not the winner here? Answer: The tip column leaks the answer. A model that cheats scores well and predicts nothing in real use.
- What stays the same in a fair comparison? Answer: The rows, the split, and the measure of error.

Modify: Try distance and raining only, and print the validation error. Answer: About UGX 2262, slightly worse than with rush hour too.

```python
distance_rain = validation_mae(["distance_km", "raining"], LinearRegression())
```

## Block B. Check an assistant's advice

A function should multiply a price by a quantity but gives the wrong answer. A tutor shows an assistant's hint, or a tutor-written one, and you test it. Use only this practice function; your project stays separate. You already know functions and assert from session 6.

Ask for the prediction first: Predict what total(2000, 3) gives with the plus sign, and what it should give.

```python
def total(price, quantity):
    return price + quantity

buggy_result = total(2000, 3)
print(buggy_result)

def total(price, quantity):
    return price * quantity

assert total(2000, 3) == 6000
assert total(1000, 0) == 0
assert total(1000, 1) == 1000
```

Correct result: The first print shows 2003, because plus adds the numbers. The required answer is 6000, and multiplying fixes it. The three asserts pass silently. The tests support this small requirement and do not prove the function is right for every input. The tutor's hint says to inspect the arithmetic operator and to try total(2000, 3) and total(1000, 0). A claim that every bug in a total function is fixed by changing + to * goes too far: a different bug would need a different repair.

Investigate, with answers:

- What is useful in the hint and what is unjustified? Answer: Useful: inspect the operator and test with 0. Unjustified: the claim that every bug is fixed by changing + to *.
- Why test with a quantity of 0? Answer: A zero quantity must give a total of 0, which catches many mistakes.
- What goes in AI_USE_LOG.md? Answer: The date and tool, your own attempt, the question asked, the reply, what you accepted or rejected and why, and the tests you ran.

Modify: Add one more assert of your own and run the cell. Answer: For example assert total(500, 4) == 2000.

```python
assert total(500, 4) == 2000
```

## Make: reference

A model that does not beat the baseline is still a good result if the method is sound and you report it plainly. The partner can state the target, baseline and metric without asking.

Build log entry to look for: project.ipynb with the baseline error, one candidate model and its validation error, a written decision, and AI_USE_LOG.md.

## Misconceptions to listen for

- The model with the best score is always the one to use.
- An assistant's advice is correct when it sounds confident.
- Passing three tests proves a function is right for all inputs.

## Questions to ask, with expected answers

- Why is with_tip not a valid candidate? Expected: It uses information from after the trip.
- What does the AI log prove? Expected: That the learner checked and explained the advice.

## Online version

For a hybrid group. The live class is 90 minutes on video with screen sharing. The learner finishes the build in their own time, about an hour. The full rules are in handbook/HYBRID_DELIVERY.md.

### Live clock, 90 minutes

| Minutes | Activity |
|---|---|
| 5 | Recall: three questions on paper, then say the answers aloud |
| 35 | Block A, A fair comparison: predict, run, investigate. The Modify step moves to the build task. |
| 5 | Break away from the screen |
| 35 | Block B, Check an assistant's advice: predict, run, investigate. The Modify step moves to the build task. |
| 10 | Close: say the exit sentence aloud, then the build task is set |

### After-class build task, about an hour

1. Modify, Block A (A fair comparison): Try distance and raining only, and print the validation error.
2. Modify, Block B (Check an assistant's advice): Add one more assert of your own and run the cell.
3. Make: Add model code, the validation error and a short decision to project.ipynb. Ask a partner to name your target and baseline from the notebook alone. Record any assistance in AI_USE_LOG.md or write No AI assistance used.

When you finish, write two sentences: what you changed and how you checked it. Add a build log entry. Send a photo of your work or the notebook by the route the organiser sets, before the next class.

### Next class

In the next class recall, ask: Why is with_tip not a valid candidate? Expected: It uses information from after the trip.

## Build log and feedback

Look at what each of the five learners saved and note one strength and one next step for each. Share them kindly and privately. Nothing is scored or ranked. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and show-and-tells need your judgement.
