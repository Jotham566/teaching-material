# CML3111 ML_PROJECT — task reference

These are the same tasks shown in the assignment notebook. Work in the notebook; you do not need to complete this file separately.

## Your data

Investigate motor winding temperature; target unit: **deg C**. These are synthetic teaching data. Each row is an operating observation; equipment_id identifies equipment and can repeat.

A record is a dictionary of column names and values. A list of records holds several rows. record_id identifies a row; load_pct is load as a percentage; ambient_c is temperature in degrees C; target is the quantity to predict. Numeric CSV blanks become None. Keep the original data. Your functions are checked on other records following the same published rules.


### `predict_regression(training_records, feature_records)` — 10 marks

- Use load_pct and ambient_c as the two input features. Feature records do not contain target.
- Fit preprocessing on training_records only.
- Fit a baseline that predicts the mean training target.
- Fit linear regression and a decision tree with max_depth=4 and random_state=17.
- Predict for feature_records using all three models.
- Return a dictionary with baseline, linear and tree; each value is a prediction list in feature_records order.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.


### `group_split(records)` — 5 marks

- Assign whole equipment groups: E1–E4 to train, E5 to validation, E6 to test.
- Return train, validation and test lists of record_id in input order.
- Do not use target values to choose membership.
- Return a dictionary with train, validation and test. Each value is a list of record_id values.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.


### `regression_errors(actual, predicted)` — 5 marks

- Return mae and rmse, calculated over the same paired observations, with full precision.
- Return a dictionary with mae and rmse. MAE is the mean absolute error; RMSE is the square root of the mean squared error. Match actual and predicted by position.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.



## Report checklist

Put the complete written evidence in your report, with relevant notebook results and chart captions.

1. **Problem definition (15 written marks):** The engineering problem is real, specific and bounded. The ML task is correctly derived from it. The target variable is justified, not merely available.

2. **Data understanding (15 written marks):** Provenance, licence and collection method stated. Defects found and handled with justification. Limitations of the data acknowledged before any modelling.

3. **Methodology (10 written marks):** Appropriate models chosen and compared under one protocol. Pipeline used. Hyperparameters handled sensibly. Choices explained rather than defaulted to.

4. **Engineering reasoning (20 written marks):** Domain knowledge visibly enters the work through features, banding, metric choice or interpretation. The result is discussed as engineering, not as a score.

5. **Validation (5 written marks):** Correct train/test discipline, cross-validation with a reported spread, leakage explicitly checked and ruled out, metric justified against the cost of error.

6. **Communication (10 written marks):** The 2-page brief is readable by a non-specialist engineer. Charts answer questions and are captioned with findings. Uncertainty and limitations stated honestly.

7. **Reproducibility & documentation (5 written marks):** Repository runs from a clean clone. README complete. requirements.txt present. Seeds set. AI use declared. Contribution log present.


## Submit

TWO files together: your completed notebook (.ipynb) AND one complete report (DOCX or selectable-text PDF).

<!-- PANDAS_WORKFLOW_20261015 -->
## Pandas workflow

Run the supplied pandas loading cell first. Analyse tables with pandas inside the required functions; return the exact list or dictionary requested. Where supplied, use records_from_table when a return needs Python None values. Correct existing loop-based solutions remain accepted.
