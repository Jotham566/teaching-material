# CML3113 A10 — task reference

These are the same tasks shown in the assignment notebook. Work in the notebook; you do not need to complete this file separately.

## Your data

Investigate crusher energy demand; target unit: **kWh/t**. These are synthetic teaching data. Each row is an operating observation; equipment_id identifies equipment and can repeat.

A record is a dictionary of column names and values. A list of records holds several rows. record_id identifies a row; load_pct is load as a percentage; ambient_c is temperature in degrees C; target is the quantity to predict. Numeric CSV blanks become None. Keep the original data. Your functions are checked on other records following the same published rules.


### `make_features(feature_records)` — 5 marks

- Return one feature row per input, in order: [load_pct, ambient_c, load_pct/100, load_pct*ambient_c].
- Use inputs available at prediction time only.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.


### `ablation_metrics(training_records, validation_records)` — 5 marks

- Fit two sklearn LinearRegression models on the same training records: base features [load_pct, ambient_c] and extended features adding load_pct*ambient_c.
- Evaluate both on the same validation records.
- Return base_mae, extended_mae and improvement=base_mae-extended_mae, without rounding.
- Inputs are complete; never fit on validation targets.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.



## Written questions

**Supplied scenario (use for the written questions):**

The base features are load_pct (%) and ambient_c (degrees C); the candidate interaction is load_pct*ambient_c (% times degrees C). All are available before predicting target. Under one unchanged equipment-group validation split, base MAE is 2.0 and extended MAE is 2.4 target units. Explain the controlled ablation and decide whether to retain the interaction.

Write your answers in the notebook’s **My written evidence** cell. Keep that heading. Use these numbers to organise your answers.

1. **2 marks:** Define each base feature and the interaction, with units. State when each becomes available.

2. **2 marks:** What must stay unchanged to isolate the effect of adding the interaction?

3. **2 marks:** Calculate and interpret the change in MAE in the supplied comparison.

4. **2 marks:** Would you retain the interaction for this comparison? Justify your decision.

5. **2 marks:** What does this one validation result fail to establish about other datasets or conditions?


## Submit

ONE completed assignment notebook (.ipynb).

<!-- PANDAS_WORKFLOW_20261015 -->
## Pandas workflow

Run the supplied pandas loading cell first. Analyse tables with pandas inside the required functions; return the exact list or dictionary requested. Where supplied, use records_from_table when a return needs Python None values. Correct existing loop-based solutions remain accepted.
