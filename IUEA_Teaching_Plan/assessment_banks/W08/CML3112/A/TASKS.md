# CML3112 W08: Regression and baseline — variant A

Investigate building cooling load. Target units: kW. These are synthetic teaching records, not measurements suitable for deployment. Each record is one operating observation; equipment_id repeats across observations.

Use your Student Registration Number in STUDENT_ID, including slashes. In filenames only replace slashes with underscores. Set COHORT to CML3112.

Numeric fields are numbers (missing values become None); parse CSV blanks accordingly. The public function interfaces below let the isolated grader evaluate your implementation on unseen records. The unseen records use the same schema and published rules. Implement the functions in the submitted notebook; do not hardcode the supplied answers. The numerical component does not prove the quality of the full investigation.

Published total: 20 marks. Deterministic component: 10. Written/evidence component: 10.0. Original criterion totals are preserved.

## Engineering questions

Which model improves on the training-mean baseline on a fixed validation set? Express the error in target units. What limits this comparison?

## Required interfaces

## Supplied reasoning scenario

On one fixed equipment-group validation set, the training-mean baseline has MAE 8.0, linear regression 2.1 and the depth-4 tree 3.4, all in the assigned target unit. The data are synthetic. Recommend a model for further evaluation, explain limits and specify reproducible data/run instructions.

Interpret these supplied values for the written marks; they are not claims about results you measured. Your implementation is checked independently.

- predict_regression(training_records, feature_records) — 7 marks within c1. Fit a training-mean baseline, linear regression and a decision tree (max_depth=4, random_state=17) using load_pct and ambient_c only. Return three prediction lists under baseline, linear and tree. Feature records have no target. Fit preprocessing only on training data.

- regression_errors(actual, predicted) — 3 marks within c1. Return mae and rmse, calculated over the same paired observations, with full precision.

## Full investigation and evidence

Write your own explanation in the markdown cell headed `## My written evidence`. Keep that heading. Task prompts and code comments are excluded from reasoning marks. Complete the required functions and interpret the supplied scenario where provided. Broader project exercises and extra charts are formative practice; they do not add marks to this weekly submission. State units and limitations.

## Written assessment criteria

- Choice (3 marks): The response recommends linear regression as the preferred candidate for further evaluation in the supplied validation comparison. Referring to the supplied table as the reason is sufficient; it need not repeat the numbers. Do not award credit if it recommends another model or gives a contradictory justification, such as preferring a larger MAE.

- Limits (3 marks): Award 3 if the response explicitly cautions that synthetic validation results cannot establish safety or generalisation on real equipment. A claim that synthetic measurements prove real-world safety is incorrect and earns zero; merely mentioning synthetic data without this limitation also earns zero. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

- Data (2 marks): Award 2 if the response specifies that reproduction requires engineering_data.csv, the assigned cohort identifier and the target unit. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

- Protocol (2 marks): Award 2 if the response specifies a clean top-to-bottom run with a fixed group split and training-only preprocessing. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

## Submission

Submit exactly one complete notebook through the cohort form. Keep a downloaded copy. The form link and Kampala deadline are in the student package and final teaching slide.
