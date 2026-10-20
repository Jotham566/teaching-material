# CML3111 DA_PROJECT — task reference

These are the same tasks shown in the assignment notebook. Work in the notebook; you do not need to complete this file separately.

## Your data

Investigate motor winding temperature; target unit: **deg C**. These are synthetic teaching data. Each row is an operating observation; equipment_id identifies equipment and can repeat.

A record is a dictionary of column names and values. A list of records holds several rows. record_id identifies a row; load_pct is load as a percentage; ambient_c is temperature in degrees C; target is the quantity to predict. Numeric CSV blanks become None. Keep the original data. Your functions are checked on other records following the same published rules.


### `clean_records(records)` — 10 marks

- Return a list of copied records, keeping their original order. Do not change the raw input.
- Keep only the first occurrence of each record_id.
- Drop a record if target is missing or load_pct is outside 0–100 inclusive.
- Using the remaining records, find the median of the non-missing ambient_c values. Use it to fill missing ambient_c.
- Make no other changes.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.


### `summarize_records(clean_records)` — 10 marks

- Return count, mean, minimum, maximum of target and group_means by equipment_id.
- Retain full precision.
- Return a dictionary with exactly count, mean, minimum, maximum and group_means. group_means is a dictionary from equipment ID to its mean target.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.


### `build_charts(clean_records)` — 12 marks

- Return at least three actual matplotlib Figure objects: scatter load_pct vs target; bar of mean target by equipment_id in alphabetical order; target histogram with ten equal bins from minimum to maximum.
- Add chart titles and axis labels, including target units.
- A fourth figure, when required, plots record_id vs target in input order.
- Return all four figures as a list of actual matplotlib Figure objects.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.


### `five_findings(clean_records)` — 10 marks

- Return a dict with count, mean, minimum, maximum and group_gap (highest minus lowest equipment mean).
- Each value is a dict with value and unit; count uses observations and other values use the cohort target unit.
- These numerical findings are checked independently of the narrative.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.



## Report checklist

Put the complete written evidence in your report, with relevant notebook results and chart captions.

1. **Question & dataset fit (20 written marks):** A real engineering question is stated, and the chosen dataset can actually answer it. Provenance and licence stated.

2. **Data quality work (15 written marks):** Defects found and handled with written justification. A data quality statement is present.

3. **Analysis & visualisation (8 written marks):** Four or more charts, each answering a stated question. Correct chart types, labelled axes, findings in the captions.

4. **Findings & interpretation (10 written marks):** Conclusions supported by the analysis, stated in engineering terms, with limitations acknowledged.

5. **Individual contribution log (5 written marks):** Present, specific, and consistent with the repository's commit history.


## Submit

TWO files together: your completed notebook (.ipynb) AND one complete report (DOCX or selectable-text PDF).

<!-- PANDAS_WORKFLOW_20261015 -->
## Pandas workflow

Run the supplied pandas loading cell first. Analyse tables with pandas inside the required functions; return the exact list or dictionary requested. Where supplied, use records_from_table when a return needs Python None values. Correct existing loop-based solutions remain accepted.
