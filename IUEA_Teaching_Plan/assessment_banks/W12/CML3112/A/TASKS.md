# CML3112 W12: Model recommendation — variant A

Investigate building cooling load. Target units: kW. These are synthetic teaching records, not measurements suitable for deployment. Each record is one operating observation; equipment_id repeats across observations.

Use your Student Registration Number in STUDENT_ID, including slashes. In filenames only replace slashes with underscores. Set COHORT to CML3112.

Numeric fields are numbers (missing values become None); parse CSV blanks accordingly. The public function interfaces below let the isolated grader evaluate your implementation on unseen records. The unseen records use the same schema and published rules. Implement the functions in the submitted notebook; do not hardcode the supplied answers. The numerical component does not prove the quality of the full investigation.

Published total: 20 marks. Deterministic component: 8. Written/evidence component: 12.0. Original criterion totals are preserved.

## Engineering questions

Compare candidates under one validation protocol, meeting both error and latency limits. Explain the trade-off and distinguish a local prediction explanation from global feature importance.

## Required interfaces

## Supplied reasoning scenario

Candidates evaluated under the same validation protocol: baseline MAE=2, latency=1ms; linear MAE=2, latency=3ms; tree MAE=1, latency=30ms. Requirements are MAE<=2 and latency<=10ms. Among eligible models choose lowest MAE, then lowest latency, then name. Explain your choice, local explanation versus global importance, and conditions that would change the choice.

Interpret these supplied values for the written marks; they are not claims about results you measured. Your implementation is checked independently.

- select_model(candidates, max_mae, max_ms) — 5 marks within c1. Candidates have name, validation_mae and latency_ms. Keep those meeting both inclusive constraints; select smallest validation_mae, then latency_ms, then name alphabetically. Return the selected name or None. Never use test scores for selection.

- regression_errors(actual, predicted) — 3 marks within c2. Return mae and rmse, calculated over the same paired observations, with full precision.

## Full investigation and evidence

Write your own explanation in the markdown cell headed `## My written evidence`. Keep that heading. Task prompts and code comments are excluded from reasoning marks. Complete the required functions and interpret the supplied scenario where provided. Broader project exercises and extra charts are formative practice; they do not add marks to this weekly submission. State units and limitations.

## Written assessment criteria

- Choice (3 marks): Award 3 if the response chooses baseline: it meets both limits and ties linear on MAE while being faster; tree violates the 10ms limit. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

- Protocol (2 marks): Award 2 if the response requires identical validation data, preprocessing rules and metric definitions for a fair comparison. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

- Explanation (2 marks): Award 2 if the response distinguishes explaining one prediction locally from summarising feature influence across a dataset globally. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

- Assumption (2 marks): Award 2 if the response states that the 10ms budget and comparable measured latencies are assumptions of the decision. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

- Failure (1 marks): Award 1 if the response identifies a plausible failure such as slower target hardware or a shifted operating population. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

- Change (2 marks): Award 2 if the response explains that raising the allowed latency to at least 30ms makes tree eligible and preferred on the supplied MAE. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

## Submission

Submit exactly one complete notebook through the cohort form. Keep a downloaded copy. The form link and Kampala deadline are in the student package and final teaching slide.
