# CML3111 A9 — task reference

These are the same tasks shown in the assignment notebook. Work in the notebook; you do not need to complete this file separately.

## Your data

Investigate motor winding temperature; target unit: **deg C**. These are synthetic teaching data. Each row is an operating observation; equipment_id identifies equipment and can repeat.

A record is a dictionary of column names and values. A list of records holds several rows. record_id identifies a row; load_pct is load as a percentage; ambient_c is temperature in degrees C; target is the quantity to predict. Numeric CSV blanks become None. Keep the original data. Your functions are checked on other records following the same published rules.


### `group_split(records)` — 6 marks

- Assign whole equipment groups: E1–E4 to train, E5 to validation, E6 to test.
- Return train, validation and test lists of record_id in input order.
- Do not use target values to choose membership.
- Return a dictionary with train, validation and test. Each value is a list of record_id values.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.


### `predict_regression(training_records, feature_records)` — 4 marks

- Use load_pct and ambient_c as the two input features. Feature records do not contain target.
- Fit preprocessing on training_records only.
- Fit a baseline that predicts the mean training target.
- Fit linear regression and a decision tree with max_depth=4 and random_state=17.
- Predict for feature_records using all three models.
- Return a dictionary with baseline, linear and tree; each value is a prediction list in feature_records order.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.



## Written questions

**Supplied scenario (use for the written questions):**

Equipment IDs repeat across operating observations. E1–E4 are training, E5 validation and E6 untouched test. Features are load_pct and ambient_c. The deployment proposal concerns previously unseen equipment in a hotter environment. Explain leakage controls, the scope supported by synthetic data and a plausible failure under this shift.

Write your answers in the notebook’s **My written evidence** cell. Keep that heading. Use these numbers to organise your answers.

1. **2 marks:** Why must all observations from the same equipment ID stay in one partition?

2. **2 marks:** Which data may fit preprocessing? How will E6 be protected during fitting and model selection?

3. **3 marks:** What claim is supported by this synthetic evaluation? Explain its limits for real deployment.

4. **3 marks:** How could unseen equipment or a hotter environment cause the model to fail?


## Submit

ONE completed assignment notebook (.ipynb).

<!-- PANDAS_WORKFLOW_20261015 -->
## Pandas workflow

Run the supplied pandas loading cell first. Analyse tables with pandas inside the required functions; return the exact list or dictionary requested. Where supplied, use records_from_table when a return needs Python None values. Correct existing loop-based solutions remain accepted.
