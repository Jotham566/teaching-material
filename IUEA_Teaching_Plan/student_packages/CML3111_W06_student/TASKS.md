# CML3111 A6 — task reference

These are the same tasks shown in the assignment notebook. Work in the notebook; you do not need to complete this file separately.

## Your data

Investigate motor winding temperature; target unit: **deg C**. These are synthetic teaching data. Each row is an operating observation; equipment_id identifies equipment and can repeat.

A record is a dictionary of column names and values. A list of records holds several rows. record_id identifies a row; load_pct is load as a percentage; ambient_c is temperature in degrees C; target is the quantity to predict. Numeric CSV blanks become None. Keep the original data. Your functions are checked on other records following the same published rules.


### `clean_records(records)` — 5 marks

- Return a list of copied records, keeping their original order. Do not change the raw input.
- Keep only the first occurrence of each record_id.
- Drop a record if target is missing or load_pct is outside 0–100 inclusive.
- Using the remaining records, find the median of the non-missing ambient_c values. Use it to fill missing ambient_c.
- Make no other changes.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.


### `summarize_records(clean_records)` — 5 marks

- Return count, mean, minimum, maximum of target and group_means by equipment_id.
- Retain full precision.
- Return a dictionary with exactly count, mean, minimum, maximum and group_means. group_means is a dictionary from equipment ID to its mean target.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.


### `audit_cleaning(raw_records, cleaned_records)` — 2 marks

- Return integer counts describing the two lists you receive; do not change either list.
- raw_count: number of records in raw_records. cleaned_count: number in cleaned_records.
- duplicate_ids: number of cleaned records beyond the first occurrence of each record_id.
- missing_targets: number of cleaned records with target=None.
- invalid_loads: number of cleaned records with load_pct outside 0–100 inclusive.
- Count any defects still present in the supplied cleaned_records; do not assume they are all zero.
- Return a dictionary with exactly raw_count, cleaned_count, duplicate_ids, missing_targets and invalid_loads.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.



## Written questions

Write your answers in the notebook’s **My written evidence** cell. Keep that heading. Use these numbers to organise your answers.

1. **1 mark:** Why should a repeated record_id be kept only once? Explain the effect on counting observations.

2. **1 mark:** Why exclude a missing target or an invalid load rather than inventing or clipping a value?

3. **1 mark:** Why use the median for missing ambient temperature, and why keep the raw data?

4. **2.5 marks:** Explain one meaningful limitation of the data or cleaning decisions.

5. **2.5 marks:** What use is justified by these teaching data? What would be needed before real deployment?


## Submit

ONE completed assignment notebook (.ipynb).

<!-- PANDAS_WORKFLOW_20261015 -->
## Pandas workflow

Run the supplied pandas loading cell first. Analyse tables with pandas inside the required functions; return the exact list or dictionary requested. Where supplied, use records_from_table when a return needs Python None values. Correct existing loop-based solutions remain accepted.
