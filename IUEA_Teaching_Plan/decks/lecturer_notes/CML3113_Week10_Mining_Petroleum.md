# CML3113 Week10 Mining Petroleum

Lecturer companion to the revised PowerPoint. Slide numbers match this edition. Explain the worked examples directly; revision checks are for individual study.

## Slide 1 — Honest validation and leakage

PURPOSE
Honest validation and leakage

CONNECT
Previous slide: the preceding week.

EXPLAIN
Mining and Petroleum Engineering

LECTURER CUE
Use PowerPoint Presenter View for these notes. Teach one example, pause for every learner to predict, then work an analogous example together. The practice notebook is a learning aid, not an extra graded upload.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Today’s learning.

REFERENCES


## Slide 2 — Today’s learning

PURPOSE
Today’s learning

CONNECT
Previous slide: Honest validation and leakage.

EXPLAIN
Keep related equipment records together.

Separate training, validation and final testing.

LECTURER CUE
Ask learners to explain this goal in ordinary language. The first successful attempt matters more than covering optional extensions. Defer: Multiple adversarial notebooks, elaborate validation curves and several cross-validation variants are extensions after the core split is understood.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Connection to the previous lesson.

REFERENCES


## Slide 3 — Connection to the previous lesson

PURPOSE
Connection to the previous lesson

CONNECT
Previous slide: Today’s learning.

EXPLAIN
We have compared predictions with known answers. Now we control which observations may influence training, choices and the final evaluation.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Why this week’s tools are needed.

REFERENCES


## Slide 4 — Why this week’s tools are needed

PURPOSE
Why this week’s tools are needed

CONNECT
Previous slide: Connection to the previous lesson.

EXPLAIN
We want evidence about new equipment or future observations. The way we separate data must match that use before any model or preprocessing learns from it.

LECTURER CUE
A pump team records temperature to investigate operation. Mining students can relate this to a dewatering pump; petroleum students to a transfer pump. These are teaching examples, not operating limits.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Training validation and final test.

REFERENCES


## Slide 5 — Training validation and final test

PURPOSE
Training validation and final test

CONNECT
Previous slide: Why this week’s tools are needed.

EXPLAIN
Training data fit the model and preprocessing.

Validation data guide feature and model choices.

The final test evaluates choices after they are fixed.

A fresh test is needed if its answers influenced further choices.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Three sets have different jobs.

REFERENCES


## Slide 6 — Three sets have different jobs

PURPOSE
Three sets have different jobs

CONNECT
Previous slide: Training validation and final test.

EXPLAIN
Which set must stay sealed until choices are fixed?

LECTURER CUE
Ask students to describe what they see before introducing terminology. Generated conceptual teaching illustration.  Source: figs/experiential/ASSET_SOURCES.md.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Generalisation and Overfitting and underfitting.

REFERENCES


## Slide 7 — Generalisation and Overfitting and underfitting

PURPOSE
Generalisation and Overfitting and underfitting

CONNECT
Previous slide: Three sets have different jobs.

EXPLAIN
Generalisation: Performance on new cases from the intended setting, not merely on records already used.

Overfitting and underfitting: Overfitting captures training-specific detail that fails to transfer. Underfitting misses useful patterns. Score gaps are clues, not a complete diagnosis.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Leakage and Group split.

REFERENCES


## Slide 8 — Leakage and Group split

PURPOSE
Leakage and Group split

CONNECT
Previous slide: Generalisation and Overfitting and underfitting.

EXPLAIN
Leakage: Information enters model development that would not legitimately be available, such as the answer or information from evaluation rows.

Group split: Keep all observations from the same equipment in one partition when the goal is prediction for unseen equipment.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Repeated equipment needs group separation.

REFERENCES


## Slide 9 — Repeated equipment needs group separation

PURPOSE
Repeated equipment needs group separation

CONNECT
Previous slide: Leakage and Group split.

EXPLAIN
Readings from the same equipment can share patterns.

Putting that equipment in both training and validation can make evaluation too easy.

For a new-equipment question, keep every row for an equipment ID in one partition.

LECTURER CUE
Write equipment letters on paper cards and distribute whole groups to train, validation and test. Explain why two observations of the same machine can share information.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Keeping equipment groups together.

REFERENCES


## Slide 10 — Keeping equipment groups together

PURPOSE
Keeping equipment groups together

CONNECT
Previous slide: Repeated equipment needs group separation.

EXPLAIN
Observation | Equipment | Partition

1 | A | Training

2 | A | Training

3 | B | Validation

This toy split explains group separation.

LECTURER CUE
This toy split explains group separation. It does not establish a representative evaluation with only two pieces of equipment.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Worked example (1/2).

REFERENCES


## Slide 11 — Validation and leakage in Python (1/2)

PURPOSE
Validation and leakage in Python (1/2)

CONNECT
Previous slide: Keeping equipment groups together.

EXPLAIN
Read the code in this order:
records = [{"id": 1, "equipment": "A"},
           {"id": 2, "equipment": "A"},
           {"id": 3, "equipment": "B"}]
train = []
validation = []

Square brackets create a list or select an item.

Braces hold dictionary key: value pairs here.

= assigns the value on the right to the name on the left.

Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER CUE
Write equipment letters on paper cards and distribute whole groups to train, validation and test. Explain why two observations of the same machine can share information. Fit a missing-value replacement on training values [20, 22, 24]: the median is 22. A new hotter observation must not change that fitted median. Show a counterexample: if every input contains a field called final_inspection_result recorded after the outcome, an excellent score can be meaningless for earlier prediction.

Complete practice code:
records = [{"id": 1, "equipment": "A"},
           {"id": 2, "equipment": "A"},
           {"id": 3, "equipment": "B"}]
train = []
validation = []
for row in records:
    if row["equipment"] == "A":
        train.append(row["id"])
    else:
        validation.append(row["id"])
print(train, validation)

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Worked example (2/2).

REFERENCES


## Slide 12 — Validation and leakage in Python (2/2)

PURPOSE
Validation and leakage in Python (2/2)

CONNECT
Previous slide: Validation and leakage in Python (1/2).

EXPLAIN
Read the code in this order:
for row in records:
    if row["equipment"] == "A":
        train.append(row["id"])
    else:
        validation.append(row["id"])
print(train, validation)

for takes the next item. The indented block repeats.

if tests a condition. The chosen indented block runs.

print displays a value below the cell.

Continue the SAME cell; keep indentation. Run after all parts are entered.

LECTURER CUE
Write equipment letters on paper cards and distribute whole groups to train, validation and test. Explain why two observations of the same machine can share information. Fit a missing-value replacement on training values [20, 22, 24]: the median is 22. A new hotter observation must not change that fitted median. Show a counterexample: if every input contains a field called final_inspection_result recorded after the outcome, an excellent score can be meaningless for earlier prediction.

Complete practice code:
records = [{"id": 1, "equipment": "A"},
           {"id": 2, "equipment": "A"},
           {"id": 3, "equipment": "B"}]
train = []
validation = []
for row in records:
    if row["equipment"] == "A":
        train.append(row["id"])
    else:
        validation.append(row["id"])
print(train, validation)

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Expected output.

REFERENCES


## Slide 13 — Validation and leakage results

PURPOSE
Validation and leakage results

CONNECT
Previous slide: Validation and leakage in Python (2/2).

EXPLAIN
[1, 2] [3]

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Preprocessing and pipeline.

REFERENCES


## Slide 14 — Preprocessing and pipeline

PURPOSE
Preprocessing and pipeline

CONNECT
Previous slide: Validation and leakage results.

EXPLAIN
Preprocessing and pipeline: Preprocessing changes inputs, for example filling missing values. A pipeline fits these steps on training data and applies the same fitted changes to new inputs.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A learned cleaning value comes from training.

REFERENCES


## Slide 15 — A learned cleaning value comes from training

PURPOSE
A learned cleaning value comes from training

CONNECT
Previous slide: Preprocessing and pipeline.

EXPLAIN
The training readings are 20, 22 and 24. Their median is 22.

A missing validation value receives the already learned 22.

A new validation reading of 40 must not change the fitted median.

LECTURER CUE
Fit a missing-value replacement on training values [20, 22, 24]: the median is 22. A new hotter observation must not change that fitted median.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A training-only fill value in Python (1/2).

REFERENCES


## Slide 16 — A training-only fill value in Python (1/2)

PURPOSE
A training-only fill value in Python (1/2)

CONNECT
Previous slide: A learned cleaning value comes from training.

EXPLAIN
Read the code in this order:
from statistics import median
training_values = [20, 22, 24]
validation_values = [None, 40]
training_median = median(training_values)
filled_validation = []

import loads a library. from selects a tool from it.

Square brackets create a list or select an item.

= assigns the value on the right to the name on the left.

Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER CUE
The median is learned from training observations. Adding a new validation observation must not change it. A real modelling pipeline follows this same rule for each learned step.

Complete practice code:
from statistics import median
training_values = [20, 22, 24]
validation_values = [None, 40]
training_median = median(training_values)
filled_validation = []
for value in validation_values:
    if value is None:
        filled_validation.append(training_median)
    else:
        filled_validation.append(value)
print(training_median, filled_validation)

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A training-only fill value in Python (2/2).

REFERENCES


## Slide 17 — A training-only fill value in Python (2/2)

PURPOSE
A training-only fill value in Python (2/2)

CONNECT
Previous slide: A training-only fill value in Python (1/2).

EXPLAIN
Read the code in this order:
for value in validation_values:
    if value is None:
        filled_validation.append(training_median)
    else:
        filled_validation.append(value)
print(training_median, filled_validation)

for takes the next item. The indented block repeats.

if tests a condition. The chosen indented block runs.

print displays a value below the cell.

Continue the SAME cell; keep indentation. Run after all parts are entered.

LECTURER CUE
The median is learned from training observations. Adding a new validation observation must not change it. A real modelling pipeline follows this same rule for each learned step.

Complete practice code:
from statistics import median
training_values = [20, 22, 24]
validation_values = [None, 40]
training_median = median(training_values)
filled_validation = []
for value in validation_values:
    if value is None:
        filled_validation.append(training_median)
    else:
        filled_validation.append(value)
print(training_median, filled_validation)

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Leakage gives away information from the future.

REFERENCES


## Slide 18 — Leakage gives away information from the future

PURPOSE
Leakage gives away information from the future

CONNECT
Previous slide: A training-only fill value in Python (2/2).

EXPLAIN
Suppose we predict a fault before an inspection.

final_inspection_result exists only after the inspection.

Using it as an input would answer a different, easier question than the one we intended.

LECTURER CUE
Show a counterexample: if every input contains a field called final_inspection_result recorded after the outcome, an excellent score can be meaningless for earlier prediction.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Parameters hyperparameters and a fold.

REFERENCES


## Slide 19 — Parameters hyperparameters and a fold

PURPOSE
Parameters hyperparameters and a fold

CONNECT
Previous slide: Leakage gives away information from the future.

EXPLAIN
A parameter is learned during fitting, such as a line’s slope. A hyperparameter is a setting chosen around fitting, such as a tree’s max_depth.

A fold is one part of the development data used for a validation turn. Refit the entire preprocessing and model on the other parts for that turn.

Compare candidate settings using validation evidence. Keep the final test outside that selection process.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Cross-validation.

REFERENCES


## Slide 20 — Cross-validation

PURPOSE
Cross-validation

CONNECT
Previous slide: Parameters hyperparameters and a fold.

EXPLAIN
Cross-validation: Repeat fitting and validation on several partitions of the training/development data. Respect groups or time order. Keep the final test outside tuning.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
What standard deviation tells us.

REFERENCES


## Slide 21 — What standard deviation tells us

PURPOSE
What standard deviation tells us

CONNECT
Previous slide: Cross-validation.

EXPLAIN
Scores 3, 4 and 5 have mean 4. Their deviations are -1, 0 and 1.

For these three fold scores, population SD = sqrt((1 + 0 + 1) / 3), about 0.82.

SD describes spread around the mean in the score’s units. The next illustration uses this same population convention; it is not a confidence interval.

LECTURER CUE
Square each deviation, average all three, then take the square root. Here we describe the full displayed set. A sample SD would instead divide by n - 1; do not mix conventions.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Trace three validation turns.

REFERENCES


## Slide 22 — Trace three validation turns

PURPOSE
Trace three validation turns

CONNECT
Previous slide: What standard deviation tells us.

EXPLAIN
Turn | Fit using | Validate using

1 | Parts B and C | Part A

2 | Parts A and C | Part B

3 | Parts A and B | Part C

Refit preprocessing in every turn. The separate final test is not A, B or C.

Read the rows in order. Refit preprocessing in every turn. The separate final test is not A, B or C.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Each fold takes a turn at validation.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 23 — Each fold takes a turn at validation

PURPOSE
Each fold takes a turn at validation

CONNECT
Previous slide: Trace three validation turns.

EXPLAIN
Illustrated spread: population SD 0.39 MPa, not a confidence interval.

LECTURER CUE
The illustrated mean is about 4.30 MPa and population standard deviation about 0.39 MPa. This is fold variation, not a confidence interval. Keep equipment groups together. Keep a separate final test outside model selection.
Source: existing course illustration figs/kfold.png. These are illustrative examples, not this cohort’s assessed results.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Choose a split that matches future use.

REFERENCES
Source: existing course illustration figs/kfold.png. These are illustrative examples, not this cohort’s assessed results.

## Slide 24 — Choose a split that matches future use

PURPOSE
Choose a split that matches future use

CONNECT
Previous slide: Each fold takes a turn at validation.

EXPLAIN
Equipment or time: For unseen equipment, keep each equipment ID together. For future-time prediction, train on earlier observations and evaluate on later ones.

Scaler and split tool: A scaler learns how to rescale features; fit it on training data. GroupShuffleSplit is a library tool for group separation. Our assignment instead uses its fixed published equipment lists.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Revision example and answer.

REFERENCES


## Slide 25 — Revision example and answer

PURPOSE
Revision example and answer

CONNECT
Previous slide: Choose a split that matches future use.

EXPLAIN
Example: A second observation from B arrives. Where does it go? Why not put it into training just to balance row counts?

Answer: It stays with B in validation. Mixing a source across partitions can give an overly optimistic estimate for unseen equipment.

LECTURER CUE
Give silent thinking time, then let pairs discuss. Rotate who types. This is practice, not a graded quiz. Expected response: It stays with B in validation. Mixing a source across partitions can give an overly optimistic estimate for unseen equipment.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Preparing for the assignment.

REFERENCES


## Slide 26 — Preparing for the assignment

PURPOSE
Preparing for the assignment

CONNECT
Previous slide: Revision example and answer.

EXPLAIN
W10 specifies E1–E4 train, E5 validation, E6 test and preserves input order.

Use the assigned equipment_id field and record_id outputs.

Reuse the W08 fitting pattern.

Explain that GroupShuffleSplit and time-based splitting solve different deployment questions; use the rule in the issued task.

LECTURER CUE
W10 specifies E1–E4 train, E5 validation, E6 test and preserves input order. Use the assigned equipment_id field and record_id outputs. Reuse the W08 fitting pattern. Explain that GroupShuffleSplit and time-based splitting solve different deployment questions; use the rule in the issued task.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Interpreting validation results.

REFERENCES


## Slide 27 — Interpreting validation results

PURPOSE
Interpreting validation results

CONNECT
Previous slide: Preparing for the assignment.

EXPLAIN
Fit an imputer or scaler only on training data; putting it in a Pipeline helps enforce that during cross-validation.

A low training error and high validation error suggest overfitting, but data shift or leakage can also matter.

Missing predictor values need a stated treatment.

Report fold scores and their variation, not just the best fold.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Interpreting validation results continued.

REFERENCES


## Slide 28 — Interpreting validation results continued

PURPOSE
Interpreting validation results continued

CONNECT
Previous slide: Interpreting validation results.

EXPLAIN
Group related observations together when the deployment goal is new equipment.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Your issued task.

REFERENCES


## Slide 29 — Your issued task

PURPOSE
Your issued task

CONNECT
Previous slide: Interpreting validation results continued.

EXPLAIN
Investigate crusher energy demand.

Target units: kWh/t.

These are synthetic teaching records, not measurements suitable for deployment.

Each record is one operating observation; equipment_id repeats across observations.

LECTURER CUE
Investigate crusher energy demand. Target units: kWh/t. These are synthetic teaching records, not measurements suitable for deployment. Each record is one operating observation; equipment_id repeats across observations.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
group_split(records).

REFERENCES


## Slide 30 — group_split(records)

PURPOSE
group_split(records)

CONNECT
Previous slide: Your issued task.

EXPLAIN
Assign whole equipment groups: E1–E4 to train, E5 to validation, E6 to test.

Return train, validation and test lists of record_id in input order.

Do not use target values to choose membership.

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W10/CML3113/A/TASKS.md

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
predict_regression(training_records, feature_records).

REFERENCES


## Slide 31 — predict_regression(training_records, feature_records)

PURPOSE
predict_regression(training_records, feature_records)

CONNECT
Previous slide: group_split(records).

EXPLAIN
Fit a training-mean baseline, linear regression and a decision tree (max_depth=4, random_state=17) using load_pct and ambient_c only.

Return three prediction lists under baseline, linear and tree.

Feature records have no target.

Fit preprocessing only on training data.

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W10/CML3113/A/TASKS.md

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Written evidence.

REFERENCES


## Slide 32 — Written evidence

PURPOSE
Written evidence

CONNECT
Previous slide: predict_regression(training_records, feature_records).

EXPLAIN
Use the cell headed “My written evidence”.

Explain the supplied scenario in your own words.

State target units, reasons and limitations.

Submit one complete notebook containing code and written evidence.

LECTURER CUE
Published criterion weights and exact requirements remain in TASKS.md. Broader project exercises are formative and do not add weekly marks. Local automated reasoning assessment remains subject to its release checks.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Validation and trust submission.

REFERENCES


## Slide 33 — Validation and trust submission

PURPOSE
Validation and trust submission

CONNECT
Previous slide: Written evidence.

EXPLAIN
Opens: 13 Nov 2026, 08:00 Kampala

Deadline: 20 Nov 2026, 08:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

LECTURER CUE
The form link is cohort-specific. Recheck the live form and release status before class. These scheduled assignment dates are separate from the quiz activation window. The issued brief defines the required files, even if the form accepts additional formats. Source: data/submission_links.json

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Week 10 quiz.

REFERENCES


## Slide 34 — Week 10 quiz

PURPOSE
Week 10 quiz

CONNECT
Previous slide: Validation and trust submission.

EXPLAIN
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

The lecturer will confirm the exact closing time.

LECTURER CUE
Activate the matching open_W10_CML3113 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Before you leave.

REFERENCES


## Slide 35 — Revision and submission checklist

PURPOSE
Revision and submission checklist

CONNECT
Previous slide: Week 10 quiz.

EXPLAIN
You can identify which records may influence preprocessing and model selection.

Save your work and check the required submission files.

LECTURER CUE
Ask every learner for an individual response. Record one misconception to revisit at the start of the next class. If a deadline changed, announce the exact Kampala date and update the source registry before rebuilding slides.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Optional revision video.

REFERENCES


## Slide 36 — Optional revision video

PURPOSE
Optional revision video

CONNECT
Previous slide: Revision and submission checklist.

EXPLAIN
For revision after class.

StatQuest with Josh Starmer
Machine Learning Fundamentals Cross Validation

Opening up to 04:00, optional preview-selected excerpt

Listening question: Why evaluate using observations not used to fit that particular model?

LECTURER CUE
Linked by the official StatQuest video index. Full audiovisual preview and excerpt timing still required.
After viewing: Explain why our repeated equipment IDs require grouped partitions rather than ordinary random folds.
Preview before class and stop after the selected short excerpt. If playback fails, teach the worked example. Video is optional. Source: https://www.youtube.com/watch?v=fSytzGwwBVw

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
independent revision and the issued task.

REFERENCES
