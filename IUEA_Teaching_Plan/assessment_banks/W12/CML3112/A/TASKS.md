# CML3112 A11 — task reference

These are the same tasks shown in the assignment notebook. Work in the notebook; you do not need to complete this file separately.

## Your data

Investigate building cooling load; target unit: **kW**. These are synthetic teaching data. Each row is an operating observation; equipment_id identifies equipment and can repeat.

A record is a dictionary of column names and values. A list of records holds several rows. record_id identifies a row; load_pct is load as a percentage; ambient_c is temperature in degrees C; target is the quantity to predict. Numeric CSV blanks become None. Keep the original data. Your functions are checked on other records following the same published rules.


### `select_model(candidates, max_mae, max_ms)` — 5 marks

- Candidates have name, validation_mae and latency_ms.
- Keep those meeting both inclusive constraints; select smallest validation_mae, then latency_ms, then name alphabetically.
- Return the selected name or None.
- Never use test scores for selection.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.


### `regression_errors(actual, predicted)` — 3 marks

- Return mae and rmse, calculated over the same paired observations, with full precision.
- Return a dictionary with mae and rmse. MAE is the mean absolute error; RMSE is the square root of the mean squared error. Match actual and predicted by position.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.



## Written questions

**Supplied scenario (use for the written questions):**

Candidates evaluated under the same validation protocol: baseline MAE=2, latency=1ms; linear MAE=2, latency=3ms; tree MAE=1, latency=30ms. Requirements are MAE<=2 and latency<=10ms. Among eligible models choose lowest MAE, then lowest latency, then name. Explain your choice, local explanation versus global importance, and conditions that would change the choice.

Write your answers in the notebook’s **My written evidence** cell. Keep that heading. Use these numbers to organise your answers.

1. **3 marks:** Apply both limits and the tie-breaking rule. Choose a candidate and justify its eligibility and ranking.

2. **2 marks:** What must be identical for the candidates to be compared fairly?

3. **2 marks:** Explain the difference between a local explanation of one prediction and global feature importance.

4. **2 marks:** State the latency-budget and latency-measurement assumptions behind your decision.

5. **1 mark:** Describe one realistic way the selected model could fail after deployment.

6. **2 marks:** What latency budget would make the tree eligible, and how would that change your choice?


## Submit

ONE completed assignment notebook (.ipynb).
