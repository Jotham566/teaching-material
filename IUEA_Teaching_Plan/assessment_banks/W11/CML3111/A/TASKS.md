# CML3111 W11: Features and ablation — variant A

Investigate motor winding temperature. Target units: deg C. These are synthetic teaching records, not measurements suitable for deployment. Each record is one operating observation; equipment_id repeats across observations.

Use your Student Registration Number in STUDENT_ID, including slashes. In filenames only replace slashes with underscores. Set COHORT to CML3111.

Numeric fields are numbers (missing values become None); parse CSV blanks accordingly. The public function interfaces below let the isolated grader evaluate your implementation on unseen records. The unseen records use the same schema and published rules. Implement the functions in the submitted notebook; do not hardcode the supplied answers. The numerical component does not prove the quality of the full investigation.

Published total: 20 marks. Deterministic component: 10. Written/evidence component: 10.0. Original criterion totals are preserved.

## Engineering questions

Compare base and interaction features on the same equipment-group split: E1–E4 train, E5 validate, E6 final test. Define feature units and availability. Does the measured ablation support retaining the interaction?

## Required interfaces

## Supplied reasoning scenario

The base features are load_pct (%) and ambient_c (degrees C); the candidate interaction is load_pct*ambient_c (% times degrees C). All are available before predicting target. Under one unchanged equipment-group validation split, base MAE is 2.0 and extended MAE is 2.4 target units. Explain the controlled ablation and decide whether to retain the interaction.

Interpret these supplied values for the written marks; they are not claims about results you measured. Your implementation is checked independently.

- make_features(feature_records) — 5 marks within c1. Return one feature row per input, in order: [load_pct, ambient_c, load_pct/100, load_pct*ambient_c]. Use inputs available at prediction time only.

- ablation_metrics(training_records, validation_records) — 5 marks within c2. Fit two sklearn LinearRegression models on the same training records: base features [load_pct, ambient_c] and extended features adding load_pct*ambient_c. Evaluate both on the same validation records. Return base_mae, extended_mae and improvement=base_mae-extended_mae, without rounding. Inputs are complete; never fit on validation targets.

## Full investigation and evidence

Write your own explanation in the markdown cell headed `## My written evidence`. Keep that heading. Task prompts and code comments are excluded from reasoning marks. Complete the required functions and interpret the supplied scenario where provided. Broader project exercises and extra charts are formative practice; they do not add marks to this weekly submission. State units and limitations.

## Written assessment criteria

- Dictionary (2 marks): Award 2 if the response defines load percentage, ambient temperature in degrees C, and their interaction with its product unit, all available before prediction. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

- Control (2 marks): Award 2 if the response holds training/validation membership, model family and evaluation metric constant so the feature change is isolated. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

- Ablation (2 marks): Award 2 if the response interprets 2.4 versus 2.0 as an MAE increase of 0.4 target units, hence worse validation performance. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

- Decision (2 marks): Award 2 if the response drops the interaction for this comparison because measured validation error worsens. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

- Limit (2 marks): Award 2 if the response states that one validation result does not prove the interaction is useless for every dataset or operating condition. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

## Submission

Submit exactly one complete notebook through the cohort form. Keep a downloaded copy. The form link and Kampala deadline are in the student package and final teaching slide.
