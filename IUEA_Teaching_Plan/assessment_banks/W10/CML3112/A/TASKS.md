# CML3112 W10: Validation and trust — variant A

Investigate building cooling load. Target units: kW. These are synthetic teaching records, not measurements suitable for deployment. Each record is one operating observation; equipment_id repeats across observations.

Use your Student Registration Number in STUDENT_ID, including slashes. In filenames only replace slashes with underscores. Set COHORT to CML3112.

Numeric fields are numbers (missing values become None); parse CSV blanks accordingly. The public function interfaces below let the isolated grader evaluate your implementation on unseen records. The unseen records use the same schema and published rules. Implement the functions in the submitted notebook; do not hardcode the supplied answers. The numerical component does not prove the quality of the full investigation.

Published total: 20 marks. Deterministic component: 10. Written/evidence component: 10.0. Original criterion totals are preserved.

## Engineering questions

Why must repeated equipment observations stay in one partition? Keep E6 untouched during model selection. What change in operating conditions would invalidate your recommendation?

## Required interfaces

## Supplied reasoning scenario

Equipment IDs repeat across operating observations. E1–E4 are training, E5 validation and E6 untouched test. Features are load_pct and ambient_c. The deployment proposal concerns previously unseen equipment in a hotter environment. Explain leakage controls, the scope supported by synthetic data and a plausible failure under this shift.

Interpret these supplied values for the written marks; they are not claims about results you measured. Your implementation is checked independently.

- group_split(records) — 6 marks within c1. Assign whole equipment groups: E1–E4 to train, E5 to validation, E6 to test. Return train, validation and test lists of record_id in input order. Do not use target values to choose membership.

- predict_regression(training_records, feature_records) — 4 marks within c3. Fit a training-mean baseline, linear regression and a decision tree (max_depth=4, random_state=17) using load_pct and ambient_c only. Return three prediction lists under baseline, linear and tree. Feature records have no target. Fit preprocessing only on training data.

## Full investigation and evidence

Write your own explanation in the markdown cell headed `## My written evidence`. Keep that heading. Task prompts and code comments are excluded from reasoning marks. Complete the required functions and interpret the supplied scenario where provided. Broader project exercises and extra charts are formative practice; they do not add marks to this weekly submission. State units and limitations.

## Written assessment criteria

- Groups (2 marks): Award 2 if the response explains that keeping each equipment ID in one partition prevents information from repeated equipment observations leaking across partitions. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

- Fit (2 marks): Award 2 if the response fits preprocessing on training data only and keeps E6 out of fitting and model selection. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

- Scope (3 marks): Award 3 if the response limits the supported claim to synthetic teaching evaluation rather than real equipment deployment. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

- Shift (3 marks): Award 3 if the response explains that unseen equipment or higher ambient temperatures can change the load/target relationship or cause extrapolation errors. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

## Submission

Submit exactly one complete notebook through the cohort form. Keep a downloaded copy. The form link and Kampala deadline are in the student package and final teaching slide.
