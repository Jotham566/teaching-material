# CML3113 TEST1 — task reference

These are the same tasks shown in the assignment notebook. Work in the notebook; you do not need to complete this file separately.

## Your data

Investigate crusher energy demand; target unit: **kWh/t**. These are synthetic teaching data. Each row is an operating observation; equipment_id identifies equipment and can repeat.

A record is a dictionary of column names and values. A list of records holds several rows. record_id identifies a row; load_pct is load as a percentage; ambient_c is temperature in degrees C; target is the quantity to predict. Numeric CSV blanks become None. Keep the original data. Your functions are checked on other records following the same published rules.


### `summarize_records(clean_records)` — 10 marks

- Return count, mean, minimum, maximum of target and group_means by equipment_id.
- Retain full precision.
- Return a dictionary with exactly count, mean, minimum, maximum and group_means. group_means is a dictionary from equipment ID to its mean target.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.


### `clean_records(records)` — 10 marks

- Return a list of copied records, keeping their original order. Do not change the raw input.
- Keep only the first occurrence of each record_id.
- Drop a record if target is missing or load_pct is outside 0–100 inclusive.
- Using the remaining records, find the median of the non-missing ambient_c values. Use it to fill missing ambient_c.
- Make no other changes.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.


### `build_charts(clean_records)` — 12 marks

- Return at least three actual matplotlib Figure objects: scatter load_pct vs target; bar of mean target by equipment_id in alphabetical order; target histogram with ten equal bins from minimum to maximum.
- Add chart titles and axis labels, including target units.
- A fourth figure, when required, plots record_id vs target in input order.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.


### `five_findings(clean_records)` — 20 marks

- Return a dict with count, mean, minimum, maximum and group_gap (highest minus lowest equipment mean).
- Each value is a dict with value and unit; count uses observations and other values use the cohort target unit.
- These numerical findings are checked independently of the narrative.

Write your function in the matching answer cell in the notebook. Return the requested value; printing alone is not enough.



## Written questions

Write your answers in the notebook’s **My written evidence** cell. Keep that heading. Use these numbers to organise your answers.

1. **Loading & profiling (5 written marks):** Data loaded correctly; shape, types and summary produced; the dataset is described accurately in the student's own words.

2. **Cleaning decisions & justification (10 written marks):** Defects found. Each handling decision stated AND justified. Marks are for the justification - an unjustified correct fix scores roughly half.

3. **Visualisation (8 written marks):** Three charts, each captioned with the question it answers. Correct chart type. Axes labelled with units. No decoration without purpose.

4. **Engineering interpretation (15 written marks):** One recommendation that an engineer could act on, plus a clear statement of what further data would be needed.

5. **Clarity & reproducibility (10 written marks):** Notebook runs top to bottom. Logical order. Markdown explains intent. No dead code.

### Part B — invigilator-controlled timing

15 minutes setup; 120 minutes practical; 25 minutes typed offline reasoning with no code execution; 20 minutes collection. No internet, messaging or AI.

Under a Part B subheading answer: Why your main cleaning/model choice? What can your chart/metric not establish? What evidence would change your recommendation? What further data is required?


## Submit

ONE completed assignment notebook (.ipynb).
