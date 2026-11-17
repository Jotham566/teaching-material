# ML14 Instructor guide: Predicting a number with a line

Private. Keep this file out of the student folder.

**Objective.** By the end: you can guess a line by hand, measure its error, and compare it with the line scikit-learn fits.

**Question of the day.** How close does a straight line get to the rents of eight homes?

**Where this is used.** Rents, fares and crop prices often rise in a steady way with size, distance or season, and a straight line is the simplest model of that. Ride-hailing apps show a fare estimate before the trip starts. How far can one line take you?

Prerequisite: ML13 Features, targets and an honest baseline.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

Where it overruns: Draw the eight homes on a printed scatter plot first and let students sketch a line with a ruler before any code.

## Block A. Guess a line, measure the error

Take the first eight homes. Guess that rent is 100000 plus 3000 for every square metre.

Ask for the prediction first: Predict whether the average error will be under UGX 10000 or over UGX 50000.

```python
import pandas as pd
homes = pd.read_csv("synthetic_homes.csv").head(8)
guess = 100000 + 3000 * homes["area_m2"]
errors = (homes["rent_ugx"] - guess).abs()
print(errors.mean())
```

Correct result: The cell prints 56282.25. Your guess is a straight line with intercept 100000 and slope 3000 shillings per square metre. On average it misses the real rent by about UGX 56282. The line ignores rooms, and the intercept is too low, so most guesses are too small.

Investigate, with answers:

- What does a slope of 3000 mean in words? Answer: Every extra square metre adds UGX 3000 to the guess.
- What would you change to lower the error? Answer: Raise the intercept. Most guesses are below the real rent.

Modify: Try an intercept of 160000 and print the average error. Answer: The average error falls to about UGX 21822.

```python
guess2 = 160000 + 3000 * homes["area_m2"]
error2 = (homes["rent_ugx"] - guess2).abs().mean()
```

## Block B. Let scikit-learn fit the line

Ask LinearRegression to find the best slope and intercept for the same eight homes. Compare its error with the baseline.

Ask for the prediction first: Predict whether the fitted line's error is smaller or larger than your hand-guessed 56282.

```python
from sklearn.linear_model import LinearRegression
X = homes[["area_m2"]]
y = homes["rent_ugx"]
model = LinearRegression().fit(X, y)
fit_error = (y - model.predict(X)).abs().mean()
baseline_error = (y - y.mean()).abs().mean()
print(round(model.coef_[0]), round(model.intercept_), round(fit_error), round(baseline_error))
```

Correct result: The cell prints 3221, 135838, 20077 and 109399. The fitted line has slope 3221 and intercept 135838 and misses by about UGX 20077 on these eight homes. Guessing the mean every time would miss by about UGX 109399. fit found the line, and predict will use it on a new input. These errors are measured on the eight homes the line learned from, so they look better than they will on new homes.

Investigate, with answers:

- Is a smaller error on the training homes proof that the line is good? Answer: No. The line has seen these homes. A fair check uses new homes, which is next session.
- How much better is the fitted line than the baseline? Answer: Its error is about a fifth of the baseline's.

Modify: Predict the rent for a home of 100 square metres. Answer: About UGX 457910.

```python
pred100 = model.predict(pd.DataFrame({"area_m2": [100]}))[0]
```

## Make: reference

```python
from sklearn.linear_model import LinearRegression
X = [[10], [20], [30], [40]]
y = [100, 200, 300, 400]
model = LinearRegression().fit(X, y)
p35 = model.predict([[35]])[0]
print(p35)
# About 350. X holds inputs, y the answers. fit learns the line and predict applies it. 1000 is far outside the inputs it saw.
```

Build log entry to look for: ML14.ipynb with the prediction 350, the four definitions in the student's own words, and the reason 1000 is risky.

## Misconceptions to listen for

- The fitted line must pass through every point.
- A smaller training error always means a better model.
- I can predict anywhere on the line safely.

## Questions to ask, with expected answers

- What does the slope of 3221 mean here? Expected: On these eight homes each extra square metre adds about UGX 3221 of rent.
- Why is the data on the printed scatter plot useful? Expected: It lets you see where a hand-drawn line sits among the points.

## Online version

For a hybrid group. The live class is 90 minutes on video with screen sharing. The learner finishes the build in their own time, about an hour. The full rules are in handbook/HYBRID_DELIVERY.md.

### Live clock, 90 minutes

| Minutes | Activity |
|---|---|
| 5 | Recall: three questions on paper, then say the answers aloud |
| 35 | Block A, Guess a line, measure the error: predict, run, investigate. The Modify step moves to the build task. |
| 5 | Break away from the screen |
| 35 | Block B, Let scikit-learn fit the line: predict, run, investigate. The Modify step moves to the build task. |
| 10 | Close: say the exit sentence aloud, then the build task is set |

### After-class build task, about an hour

1. Modify, Block A (Guess a line, measure the error): Try an intercept of 160000 and print the average error.
2. Modify, Block B (Let scikit-learn fit the line): Predict the rent for a home of 100 square metres.
3. Make: Use X = [[10], [20], [30], [40]] and y = [100, 200, 300, 400]. Fit a line and predict at 35. Explain in your own words what X, y, fit and predict mean, and why predicting at 1000 is risky.

When you finish, write two sentences: what you changed and how you checked it. Add a build log entry. Send a photo of your work or the notebook by the route the organiser sets, before the next class.

### Next class

In the next class recall, ask: What does the slope of 3221 mean here? Expected: On these eight homes each extra square metre adds about UGX 3221 of rent.

## Build log and feedback

Look at what each of the five learners saved and note one strength and one next step for each. Share them kindly and privately. Nothing is scored or ranked. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and show-and-tells need your judgement.
