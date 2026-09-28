# CML3111 W06: Cleaning and quality — variant A

Investigate motor winding temperature. Target units: deg C. These are synthetic teaching records, not measurements suitable for deployment. Each record is one operating observation; equipment_id repeats across observations.

Use your Student Registration Number in STUDENT_ID, including slashes. In filenames only replace slashes with underscores. Set COHORT to CML3111.

Numeric fields are numbers (missing values become None); parse CSV blanks accordingly. The public function interfaces below let the isolated grader evaluate your implementation on unseen records. The unseen records use the same schema and published rules. Implement the functions in the submitted notebook; do not hardcode the supplied answers. The numerical component does not prove the quality of the full investigation.

Published total: 20 marks. Deterministic component: 12. Written/evidence component: 8.0. Original criterion totals are preserved.

## Engineering questions

What is the cleaned mean target in its unit? Which equipment group has the highest mean, and what is the gap to the lowest? What load/target pattern is visible, and why does it not establish causation?

## Required interfaces

- clean_records(records) — 5 marks within c1. Return copied records in original order: remove repeated record_id after its first occurrence, drop rows with missing target or load_pct outside 0–100 inclusive, then fill missing ambient_c with the median of retained non-missing ambient_c values. Preserve raw input. No other changes.

- summarize_records(clean_records) — 5 marks within c2. Return count, mean, minimum, maximum of target and group_means by equipment_id. Retain full precision.

- audit_cleaning(raw_records, cleaned_records) — 2 marks within c2. Return raw_count and cleaned_count; duplicate_ids is the number of cleaned records beyond the first occurrence of each record_id; missing_targets counts None targets; invalid_loads counts cleaned load_pct outside 0–100 inclusive. Report the actual supplied data, which may still contain defects. Do not change either input. All five values are integer counts.

## Full investigation and evidence

Write your own explanation in the markdown cell headed `## My written evidence`. Keep that heading. Task prompts and code comments are excluded from reasoning marks. Complete the required functions and interpret the supplied scenario where provided. Broader project exercises and extra charts are formative practice; they do not add marks to this weekly submission. State units and limitations.

## Written assessment criteria

- Duplicates (1 marks): Score this independently. Award 1 if the submission explicitly explains that retaining one record per repeated record_id prevents a repeated upload from counting the same observation twice. Merely reporting that a duplicate was removed is not a justification. Otherwise award zero. Cite one short exact sentence supporting this item.

- Invalid (1 marks): Score this independently. Award 1 if the submission justifies excluding a missing target or a physically invalid load rather than inventing or clipping an unsupported value. Otherwise award zero. Cite one short exact sentence supporting this item.

- Impute (1 marks): Score this independently. Award 1 if the submission justifies median imputation of missing ambient temperature while retaining the original raw data. Otherwise award zero. Cite one short exact sentence supporting this item.

- Limitations (2.5 marks): Score this independently. Award 2.5 if the submission identifies at least one meaningful limitation: synthetic data, small sample, repeated equipment observations or imputation uncertainty. Otherwise award zero. Cite one short exact sentence supporting this item.

- Use (2.5 marks): Score this independently. Award 2.5 if the submission restricts use to teaching/practice, or explains that deployment requires representative measured data. Equivalent wording is valid. Otherwise award zero. Cite one short exact sentence supporting this item.

## Submission

Submit exactly one complete notebook through the cohort form. Keep a downloaded copy. The form link and Kampala deadline are in the student package and final teaching slide.
