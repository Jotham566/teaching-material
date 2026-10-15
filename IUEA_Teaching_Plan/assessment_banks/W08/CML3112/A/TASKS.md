# CML3112 A7 — task reference

These are the same tasks shown in the assignment notebook. Work in the notebook; you do not need to complete this file separately.

## Your data

Investigate building cooling load; target unit: **kW**. These are synthetic teaching data. Each row is an operating observation; equipment_id identifies equipment and can repeat.

A record is a dictionary of column names and values. A list of records holds several rows. record_id identifies a row; load_pct is load as a percentage; ambient_c is temperature in degrees C; target is the quantity to predict. Numeric CSV blanks become None. Keep the original data. Your functions are checked on other records following the same published rules.


### `predict_regression(training_records, feature_records)` — 7 marks

- Use load_pct and ambient_c as the two input features. Feature records do not contain target.
- Fit preprocessing on training_records only.
- Fit a baseline that predicts the mean training target.
- Fit linear regression and a decision tree with max_depth=4 and random_state=17.
- Predict for feature_records using all three models.
- Return a dictionary with baseline, linear and tree; each value is a prediction list in feature_records order.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.


### `regression_errors(actual, predicted)` — 3 marks

- Return mae and rmse, calculated over the same paired observations, with full precision.
- Return a dictionary with mae and rmse. MAE is the mean absolute error; RMSE is the square root of the mean squared error. Match actual and predicted by position.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.



## Written questions

**Supplied scenario (use for the written questions):**

On one fixed equipment-group validation set, the training-mean baseline has MAE 8.0, linear regression 2.1 and the depth-4 tree 3.4, all in the assigned target unit. The data are synthetic. Recommend a model for further evaluation, explain limits and specify reproducible data/run instructions.

Write your answers in the notebook’s **My written evidence** cell. Keep that heading. Use these numbers to organise your answers.

1. **3 marks:** Which candidate would you recommend for further evaluation, using the supplied MAE comparison? Explain why.

2. **3 marks:** What can these synthetic validation results tell you—and what can they not establish about real equipment?

3. **2 marks:** Name the input file, cohort identifier and target unit someone needs to reproduce the work.

4. **2 marks:** Describe the run order, group split and preprocessing rules needed to reproduce a fair comparison.


## Submit

ONE completed assignment notebook (.ipynb).
