# ML20 Instructor guide: Build the project baseline

Private. Keep this file out of the student folder.

**Objective.** By the end: you can split data into training, validation and locked test, fit a baseline on training only, and draw one descriptive chart.

**Question of the day.** How much does a plain guess miss by, before any model helps?

Prerequisite: ML19 Project data and a safe plan.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | recall |
| 40 | split and baseline |
| 15 | break |
| 35 | chart |
| 70 | build on your own dataset |
| 10 | save and exit check |

Where it overruns: Learners on other datasets need the same steps. Check the split sizes on each project before they go further.

## Block A. Split and fit the baseline

Use the fares as the worked example, then repeat with your own dataset. Lock 20% away, take 25% of the rest for validation, and fit the mean guess on training only.

Ask for the prediction first: Predict the three sizes and whether the baseline will miss fares by more than UGX 3000 on average.

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error
fares = pd.read_csv("synthetic_fares.csv")
X = fares[["distance_km", "rush_hour", "raining"]]
y = fares["fare_ugx"]
X_dev, X_test, y_dev, y_test = train_test_split(X, y, test_size=0.2, random_state=7)
X_train, X_val, y_train, y_val = train_test_split(X_dev, y_dev, test_size=0.25, random_state=7)
baseline = DummyRegressor(strategy="mean").fit(X_train, y_train)
val_baseline_mae = mean_absolute_error(y_val, baseline.predict(X_val))
print(len(X_train), len(X_val), len(X_test), round(val_baseline_mae))
```

Correct result: The cell prints 90, 30, 30 and 4361. The plain guess misses the validation fares by about UGX 4361 on average. Any model you build must beat that on the same validation trips. The baseline was fitted on the 90 training trips only. The 30 test trips stay locked.

Investigate, with answers:

- Why is the baseline fitted on training only? Answer: Fitting it on all rows would let it see the validation and test answers.
- What would make the baseline number meaningless? Answer: Computing it on rows that were used to fit it.

Modify: Print the share of the 150 trips used for training. Answer: 0.6, which is 90 out of 150.

```python
train_share = len(X_train) / len(fares)
```

## Block B. One descriptive chart

Plot the training trips: distance on one axis, fare on the other. Label both with units.

Ask for the prediction first: Predict the shape of the dots: rising, falling or no pattern.

```python
import seaborn as sns
import matplotlib.pyplot as plt
train = X_train.copy()
train["fare_ugx"] = y_train
sns.scatterplot(data=train, x="distance_km", y="fare_ugx")
plt.xlabel("Distance (km)")
plt.ylabel("Fare (UGX)")
plt.title("Fare against distance, training trips")
plt.show()
train_corr = train["distance_km"].corr(train["fare_ugx"])
```

Correct result: The dots rise from left to right with a lot of scatter. The correlation on the 90 training trips is about 0.76. Longer trips cost more, but two trips of equal length can differ by thousands of shillings. That scatter is why even the best line will still miss.

Investigate, with answers:

- What does the scatter around the rising pattern tell you? Answer: Distance is not the whole story, so the model will make errors.
- Why plot only the training trips? Answer: Looking at validation or test answers while choosing would leak information about them.

Modify: Colour the dots by rush_hour by adding hue="rush_hour" to the plot. Answer: Two colours appear, and they overlap a lot: rush hour changes the fare little.

```python
sns.scatterplot(data=train, x="distance_km", y="fare_ugx", hue="rush_hour")
plt.show()
```

## Make: reference

Check the source, the split sizes, a baseline fitted only on training rows, a metric in the target's unit, and a labelled chart. The learner explains every column used.

Evidence to collect: project.ipynb with the split, the baseline error on validation, one labelled chart, a data dictionary and a cleaning log.

## Misconceptions to listen for

- The baseline is a model I do not need to report.
- I can look at the test rows to understand the data.
- A chart should include all rows.

## Questions to ask, with expected answers

- What is the baseline error for the fares example? Expected: About UGX 4361 on validation.
- Which rows may the chart use? Expected: Training rows.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
