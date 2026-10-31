# ML19 Instructor guide: Project data and a safe plan

Private. Keep this file out of the student folder.

**Objective.** By the end: you can describe a supplied dataset, spot a leakage column, and write a seven-heading project plan the instructor can approve.

**Question of the day.** Which dataset and which question can I answer with a fair test in two weeks?

Prerequisite: ML18 Checkpoint two with a locked test.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | recall |
| 40 | data tour |
| 15 | break |
| 35 | leakage and the seven headings |
| 60 | writing PROJECT_PLAN.md and instructor approval |
| 20 | AI disclosure rules and exit check |

Where it overruns: Instructor approval of each plan is the bottleneck. Visit learners in turn and ask them to finish the baseline heading first.

## Block A. Tour the fares data

synthetic_fares.csv holds 150 invented boda-boda trips. Look at its shape and at how each column moves with the fare.

Ask for the prediction first: Predict which column moves most closely with fare_ugx.

```python
import pandas as pd
fares = pd.read_csv("synthetic_fares.csv")
print(fares.shape)
corr = fares[["distance_km", "rush_hour", "raining", "tip_ugx", "fare_ugx"]].corr()["fare_ugx"].round(2)
print(corr)
```

Correct result: The table has 150 rows and 6 columns. Distance has a correlation of 0.76 with the fare, rain 0.12 and rush hour about minus 0.08. The tip column has the highest value, 0.88. A correlation near 1 means the two columns rise together. The tip rises with the fare because it is a share of the fare, and it is only known after the trip, so using it to predict the fare would be cheating. That makes tip_ugx a leakage column.

Investigate, with answers:

- Why can tip_ugx not be an input? Answer: It is known only after the ride, and it is calculated from the fare. The model would be given the answer.
- Which columns are sensible inputs? Answer: distance_km, rush_hour and raining. All three are known before the ride starts.

Modify: Print the correlation of the fare with the trip_id column. Answer: It is close to zero: trip_id is only a label.

```python
id_corr = fares["trip_id"].corr(fares["fare_ugx"])
```

## Block B. A plan needs seven headings

The plan has seven headings: question, dataset, target, inputs, baseline, evaluation and limits. Write one sentence under each.

Ask for the prediction first: Write the target and two inputs for your project before looking at the example.

Correct result: An example plan: question, can distance and rush hour predict a boda-boda fare; dataset, synthetic_fares.csv; target, fare_ugx; inputs, distance_km, rush_hour and raining; baseline, the mean fare of the training trips; evaluation, mean absolute error in shillings on a locked test; limits, invented data and 150 trips. The options are synthetic_homes.csv (rent from area and rooms), synthetic_fares.csv and the iris flowers. Real people's records are not used. Repeat the AI rules: any assisted step is logged in AI_USE_LOG.md after your own attempt, or the log says No AI assistance used.

Investigate, with answers:

- Which heading stops you using the test answers to choose a model? Answer: Evaluation. It states which rows are locked and which metric is used.
- Why is the home_id column not an input for homes? Answer: It is only a label. It carries no information about rent.

Modify: Write the leakage column you will exclude and why. Answer: For fares: tip_ugx, because it is known only after the trip.

## Make: reference

An approved plan has a narrow question, a supplied dataset, a target present in the file, inputs known beforehand, a baseline fitted on training data, a metric and a locked test, and two stated limits.

Evidence to collect: PROJECT_PLAN.md with seven headings, one named leakage column, and the instructor's approval.

## Misconceptions to listen for

- A highly correlated column is always a good input.
- The plan can change after I see the final test.
- The biggest model is the best project.

## Questions to ask, with expected answers

- Why plan before coding? Expected: Choices made after seeing test results are no longer honest.
- What is the leakage column in fares? Expected: tip_ugx.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
