# CML3111 W09: Classification and cost — variant A

Investigate motor winding temperature. Target units: deg C. These are synthetic teaching records, not measurements suitable for deployment. Each record is one operating observation; equipment_id repeats across observations.

Use your Student Registration Number in STUDENT_ID, including slashes. In filenames only replace slashes with underscores. Set COHORT to CML3111.

Numeric fields are numbers (missing values become None); parse CSV blanks accordingly. The public function interfaces below let the isolated grader evaluate your implementation on unseen records. The unseen records use the same schema and published rules. Implement the functions in the submitted notebook; do not hardcode the supplied answers. The numerical component does not prove the quality of the full investigation.

Published total: 20 marks. Deterministic component: 9. Written/evidence component: 11.0. Original criterion totals are preserved.

## Engineering questions

Use classification_case.csv. Positive means a synthetic warning condition. Compute the confusion matrix, precision, recall and cost. Explain the 5:1 missed-warning/false-alarm cost assumption and why accuracy alone is insufficient. These costs are teaching assumptions, not approved operating limits.

## Required interfaces

## Supplied reasoning scenario

There are 100 validation observations: 10 actual warnings and 90 non-warnings. Model A has TP=9, FN=1, FP=3, TN=87; B has TP=10, FN=0, FP=6, TN=84. A missed warning costs 5 teaching cost units and a false alarm costs 1. Choose A or B and justify the trade-off. These are assumed costs, not approved operating limits.

Interpret these supplied values for the written marks; they are not claims about results you measured. Your implementation is checked independently.

- classification_metrics(actual, predicted) — 9 marks within c1. For binary labels return tp, tn, fp, fn, precision, recall and cost=5*fn+fp; use zero for an undefined precision/recall denominator.

## Full investigation and evidence

Write your own explanation in the markdown cell headed `## My written evidence`. Keep that heading. Task prompts and code comments are excluded from reasoning marks. Complete the required functions and interpret the supplied scenario where provided. Broader project exercises and extra charts are formative practice; they do not add marks to this weekly submission. State units and limitations.

## Written assessment criteria

- Costs (3 marks): Award 3 if the response correctly explains that A costs 8 and B costs 6 under cost=5*FN+FP. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

- Tradeoff (2 marks): Award 2 if the response explains that B catches the missed warning but adds three false alarms, so lower accuracy need not mean greater cost. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

- Choice (2 marks): Award 2 if the response chooses B because its total assumed cost is lower, rather than because accuracy alone is higher. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

- Deployment (2 marks): Award 2 if the response requires checking the assumed costs or representative real warning data before deployment. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

- Reproduce (2 marks): Award 2 if the response specifies retaining the actual/predicted labels and rerunning the confusion-matrix calculation with the stated cost rule. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.

## Submission

Submit exactly one complete notebook through the cohort form. Keep a downloaded copy. The form link and Kampala deadline are in the student package and final teaching slide.
