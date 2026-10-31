# ML22 Instructor guide: The final test and a reproducible handover

Private. Keep this file out of the student folder.

**Objective.** By the end: you can run the final test once, report it separately from validation, and hand over a project that reruns from a restarted kernel.

**Question of the day.** How well does my frozen model do on rows nobody has used?

Prerequisite: ML21 Compare, explain and critique.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | recall |
| 40 | final test |
| 15 | break |
| 25 | handover checklist |
| 80 | assemble, rerun and report |
| 10 | save and exit check |

Where it overruns: Learners with different datasets need the same final-test discipline. Check each learner's order of steps.

## Block A. Run the final test once

The fares model with three inputs was chosen on validation. Now run the 30 locked test trips once.

Ask for the prediction first: Predict whether the final test error will be above or below the validation error of 2255.

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
from sklearn.linear_model import LinearRegression
baseline = DummyRegressor(strategy="mean").fit(X_train, y_train)
model = LinearRegression().fit(X_train, y_train)
final_mae = mean_absolute_error(y_test, model.predict(X_test))
final_baseline_mae = mean_absolute_error(y_test, baseline.predict(X_test))
print(round(final_mae), round(final_baseline_mae))
```

Correct result: The cell prints 2936 and 3617. On the locked 30 trips the model misses by about UGX 2936 and the plain guess by about UGX 3617. The model is still better, but its lead is much smaller than the validation lead of 2255 against 4361. This is normal: the test has only 30 trips, and the validation lead may have been lucky. Report the final number as it is, next to the validation number, and do not change the model to improve it.

Investigate, with answers:

- Why report the final score separately from validation? Answer: Validation was used to choose the model, so only the final test is an honest score.
- Can you change the model if the final score is disappointing? Answer: No. Changing it after seeing the test would use the test twice, and a new locked test would be needed.

Modify: Calculate how much smaller the model's error is than the baseline's on the final test, as a percentage. Answer: About 19% smaller.

```python
improvement = (final_baseline_mae - final_mae) / final_baseline_mae * 100
```

## Block B. The handover checklist

Another person should be able to rerun your folder. Work through the list with a partner.

Ask for the prediction first: Write the three things you think a stranger needs first to rerun your project.

Correct result: The checklist: restart the kernel and run all cells from the top; the data file sits beside the notebook; the data origin and the fact that it is synthetic are stated; the final test is reported separately from validation; limits are written next to the result; project.ipynb, the data dictionary and report.pdf or report.docx are saved together; every file opens when reopened. A model on invented teaching data is a demonstration, and nobody should use it to make decisions about people.

Investigate, with answers:

- Why restart the kernel before the final run? Answer: Hidden steps are exposed when the notebook runs from a clean start.
- What does the report say about the model's limits? Answer: The data is invented, the test is small, and the model has not been tried on real trips.

Modify: Swap notebooks with a partner. Follow their instructions without asking questions and note where you stall. Answer: Every stall is a missing instruction. Add it.

## Make: reference

All files open and agree with each other. The final test is clearly separate from validation. Nothing relies on a variable that exists only in an earlier session.

Evidence to collect: A complete local project folder and a clean rerun from a restarted kernel, with the final test reported once.

## Misconceptions to listen for

- A disappointing final score means I should retune.
- The notebook works if it ran once.
- The report only needs the best number.

## Questions to ask, with expected answers

- What does the final test tell you that validation does not? Expected: How the frozen model does on rows no choice ever used.
- What is the first fix when a notebook breaks on rerun? Expected: Restart and run all, and find the first cell that fails.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
