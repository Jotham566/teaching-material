# CML3112 TEST2 — task reference

These are the same tasks shown in the assignment notebook. Work in the notebook; you do not need to complete this file separately.

## Your data

Investigate building cooling load; target unit: **kW**. These are synthetic teaching data. Each row is an operating observation; equipment_id identifies equipment and can repeat.

A record is a dictionary of column names and values. A list of records holds several rows. record_id identifies a row; load_pct is load as a percentage; ambient_c is temperature in degrees C; target is the quantity to predict. Numeric CSV blanks become None. Keep the original data. Your functions are checked on other records following the same published rules.


### `group_split(records)` — 10 marks

- Assign whole equipment groups: E1–E4 to train, E5 to validation, E6 to test.
- Return train, validation and test lists of record_id in input order.
- Do not use target values to choose membership.
- Return a dictionary with train, validation and test. Each value is a list of record_id values.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.


### `predict_regression(training_records, feature_records)` — 10 marks

- Use load_pct and ambient_c as the two input features. Feature records do not contain target.
- Fit preprocessing on training_records only.
- Fit a baseline that predicts the mean training target.
- Fit linear regression and a decision tree with max_depth=4 and random_state=17.
- Predict for feature_records using all three models.
- Return a dictionary with baseline, linear and tree; each value is a prediction list in feature_records order.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.


### `regression_errors(actual, predicted)` — 10 marks

- Return mae and rmse, calculated over the same paired observations, with full precision.
- Return a dictionary with mae and rmse. MAE is the mean absolute error; RMSE is the square root of the mean squared error. Match actual and predicted by position.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.



## Written questions

Write your answers in the notebook’s **My written evidence** cell. Keep that heading. Use these numbers to organise your answers.

1. **Task framing (10 written marks):** The ML task is correctly identified, the target named, and regression vs classification correctly chosen and justified.

2. **Data preparation & leakage control (10 written marks):** Cleaning and encoding appropriate. Split made before any fitting. Pipeline used. No leakage present - a leak found by the marker caps this criterion at zero.

3. **Modelling protocol (10 written marks):** At least two models built and compared under identical conditions. Baseline included. Hyperparameters handled sensibly.

4. **Evaluation & metric justification (10 written marks):** Correct metrics computed. Metric choice defended against the cost of error. Cross-validation reported with a spread, not a single number.

5. **Engineering interpretation & limits (20 written marks):** The result is stated in physical or operational units. Three genuine limitations given. A clear position on whether it should be deployed.

6. **Code clarity (10 written marks):** Runs top to bottom. Readable. Commented where the intent is not obvious.

**Data-preparation marking rule:** the required leakage-safe group split must pass for written data-preparation marks. Other criteria are marked separately.

### Part B — invigilator-controlled timing

15 minutes setup; 120 minutes practical; 25 minutes typed offline reasoning with no code execution; 20 minutes collection. No internet, messaging or AI.

Under a Part B subheading answer: Why your main cleaning/model choice? What can your chart/metric not establish? What evidence would change your recommendation? What further data is required?


## Submit

ONE completed assignment notebook (.ipynb).
