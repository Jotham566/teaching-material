# CML3112 Week10 Design Infrastructure

Lecturer companion to the revised PowerPoint. Slide numbers match this edition. Explain the worked examples directly; revision checks are for individual study.

## Slide 1 — Honest validation and leakage

PURPOSE
Honest validation and leakage

CONNECT
Build on the preceding week. Explain why this example is needed before running it.

EXPLAIN
Civil Engineering and Architecture

LECTURER DETAIL
TEACHING PURPOSE
Honest validation and leakage

LECTURER CUE
Use PowerPoint Presenter View for these notes. Teach one example, pause for every learner to predict, then work an analogous example together. The practice notebook is a learning aid, not an extra graded upload.

EXPLAIN IN ORDINARY WORDS
Training fits rules. Validation helps choose among rules. The final test estimates performance after choices are fixed. Information that would be unavailable at the real prediction time must stay out of the inputs.

CHECK AND EXPECTED ANSWER
May two readings of the same machine appear on both sides when evaluating new machines? No; split by machine. For forecasting, train on the past and evaluate later time.

IF LEARNERS ARE STUCK
Use three envelopes. Keep the final-test envelope closed while selecting features or settings.

NEXT
Today’s learning. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Today’s learning.

## Slide 2 — Today’s learning

PURPOSE
Today’s learning

CONNECT
Build on Honest validation and leakage. Explain why this example is needed before running it.

EXPLAIN
Keep related equipment records together.

Separate training, validation and final testing.

LECTURER DETAIL
TEACHING PURPOSE
Today’s learning

CONNECT
Build on the preceding slide: Honest validation and leakage.

LECTURER CUE
Ask learners to explain this goal in ordinary language. The first successful attempt matters more than covering optional extensions. Defer: Multiple adversarial notebooks, elaborate validation curves and several cross-validation variants are extensions after the core split is understood.

EXPLAIN IN ORDINARY WORDS
Training fits rules. Validation helps choose among rules. The final test estimates performance after choices are fixed. Information that would be unavailable at the real prediction time must stay out of the inputs.

CHECK AND EXPECTED ANSWER
May two readings of the same machine appear on both sides when evaluating new machines? No; split by machine. For forecasting, train on the past and evaluate later time.

IF LEARNERS ARE STUCK
Use three envelopes. Keep the final-test envelope closed while selecting features or settings.

NEXT
Recall and a first attempt. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Connection to the previous lesson.

## Slide 3 — Connection to the previous lesson

PURPOSE
Connection to the previous lesson

CONNECT
Build on Today’s learning. Explain why this example is needed before running it.

EXPLAIN
We have compared predictions with known answers. Now we control which observations may influence training, choices and the final evaluation.

LECTURER DETAIL
TEACHING PURPOSE
Recall and a first attempt

CONNECT
Build on the preceding slide: Today’s learning.

LECTURER CUE

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

NEXT
The engineering context. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Why this week’s tools are needed.

## Slide 4 — Why this week’s tools are needed

PURPOSE
Why this week’s tools are needed

CONNECT
Build on Connection to the previous lesson. Explain why this example is needed before running it.

EXPLAIN
We want evidence about new equipment or future observations. The way we separate data must match that use before any model or preprocessing learns from it.

LECTURER DETAIL
TEACHING PURPOSE
The engineering context

CONNECT
Build on the preceding slide: Recall and a first attempt.

LECTURER CUE
A building team records indoor temperature to investigate comfort. Civil students can discuss construction and inspection; architecture students can discuss shading and ventilation. Explain the quantities before using them.

EXPLAIN IN ORDINARY WORDS
A calculated column stores a result for each row at refresh. A measure is evaluated under the filters of the current visual. SUMX evaluates an expression for each row before adding it.

CHECK AND EXPECTED ANSWER
Should revenue respond to a selected region? Yes; test the measure with that filter and reconcile it to known data.

IF LEARNERS ARE STUCK
Work one order line by hand, then two lines. Name the numerator and denominator populations before an average-order-value measure.

NEXT
Training validation and final test. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Training validation and final test.

## Slide 5 — Training validation and final test

PURPOSE
Training validation and final test

CONNECT
Build on Why this week’s tools are needed. Explain why this example is needed before running it.

EXPLAIN
Training data fit the model and preprocessing.

Validation data guide feature and model choices.

The final test evaluates choices after they are fixed.

A fresh test is needed if its answers influenced further choices.

LECTURER DETAIL
TEACHING PURPOSE
Training validation and final test

CONNECT
Build on the preceding slide: The engineering context.

EXPLAIN IN ORDINARY WORDS
Training fits rules. Validation helps choose among rules. The final test estimates performance after choices are fixed. Information that would be unavailable at the real prediction time must stay out of the inputs.

CHECK AND EXPECTED ANSWER
May two readings of the same machine appear on both sides when evaluating new machines? No; split by machine. For forecasting, train on the past and evaluate later time.

IF LEARNERS ARE STUCK
Use three envelopes. Keep the final-test envelope closed while selecting features or settings.

NEXT
Three sets have different jobs. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Three sets have different jobs.

## Slide 6 — Three sets have different jobs

PURPOSE
Three sets have different jobs

CONNECT
Build on Training validation and final test. Explain why this example is needed before running it.

EXPLAIN
Which set must stay sealed until choices are fixed?

LECTURER DETAIL
TEACHING PURPOSE
Three sets have different jobs

CONNECT
Build on the preceding slide: Training validation and final test.

LECTURER CUE
Ask students to describe what they see before introducing terminology. Generated conceptual teaching illustration.  Source: figs/experiential/ASSET_SOURCES.md.

EXPLAIN IN ORDINARY WORDS
Training fits rules. Validation helps choose among rules. The final test estimates performance after choices are fixed. Information that would be unavailable at the real prediction time must stay out of the inputs.

CHECK AND EXPECTED ANSWER
May two readings of the same machine appear on both sides when evaluating new machines? No; split by machine. For forecasting, train on the past and evaluate later time.

IF LEARNERS ARE STUCK
Use three envelopes. Keep the final-test envelope closed while selecting features or settings.

NEXT
Words we will use. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Generalisation and Overfitting and underfitting.

## Slide 7 — Generalisation and Overfitting and underfitting

PURPOSE
Generalisation and Overfitting and underfitting

CONNECT
Build on Three sets have different jobs. Explain why this example is needed before running it.

EXPLAIN
Generalisation: Performance on new cases from the intended setting, not merely on records already used.
Overfitting and underfitting: Overfitting captures training-specific detail that fails to transfer. Underfitting misses useful patterns. Score gaps are clues, not a complete diagnosis.

LECTURER DETAIL
TEACHING PURPOSE
Words we will use

CONNECT
Build on the preceding slide: Three sets have different jobs.

POINT TO THE DEFINITION
Generalisation: Performance on new cases from the intended setting, not merely on records already used.
Overfitting and underfitting: Overfitting captures training-specific detail that fails to transfer. Underfitting misses useful patterns. Score gaps are clues, not a complete diagnosis.

NEXT
Words we will use. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Leakage and Group split.

## Slide 8 — Leakage and Group split

PURPOSE
Leakage and Group split

CONNECT
Build on Generalisation and Overfitting and underfitting. Explain why this example is needed before running it.

EXPLAIN
Leakage: Information enters model development that would not legitimately be available, such as the answer or information from evaluation rows.
Group split: Keep all observations from the same equipment in one partition when the goal is prediction for unseen equipment.

LECTURER DETAIL
TEACHING PURPOSE
Words we will use

CONNECT
Build on the preceding slide: Words we will use.

EXPLAIN IN ORDINARY WORDS
Training fits rules. Validation helps choose among rules. The final test estimates performance after choices are fixed. Information that would be unavailable at the real prediction time must stay out of the inputs.

CHECK AND EXPECTED ANSWER
May two readings of the same machine appear on both sides when evaluating new machines? No; split by machine. For forecasting, train on the past and evaluate later time.

IF LEARNERS ARE STUCK
Use three envelopes. Keep the final-test envelope closed while selecting features or settings.

POINT TO THE DEFINITION
Leakage: Information enters model development that would not legitimately be available, such as the answer or information from evaluation rows.
Group split: Keep all observations from the same equipment in one partition when the goal is prediction for unseen equipment.

NEXT
Repeated equipment needs group separation. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Repeated equipment needs group separation.

## Slide 9 — Repeated equipment needs group separation

PURPOSE
Repeated equipment needs group separation

CONNECT
Build on Leakage and Group split. Explain why this example is needed before running it.

EXPLAIN
Readings from the same equipment can share patterns.

Putting that equipment in both training and validation can make evaluation too easy.

For a new-equipment question, keep every row for an equipment ID in one partition.

LECTURER DETAIL
TEACHING PURPOSE
Repeated equipment needs group separation

CONNECT
Build on the preceding slide: Words we will use.

LECTURER CUE
Write equipment letters on paper cards and distribute whole groups to train, validation and test. Explain why two observations of the same machine can share information.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
Keeping equipment groups together. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Keeping equipment groups together.

## Slide 10 — Keeping equipment groups together

PURPOSE
Keeping equipment groups together

CONNECT
Build on Repeated equipment needs group separation. Explain why this example is needed before running it.

EXPLAIN
This toy split explains group separation.

LECTURER DETAIL
TEACHING PURPOSE
Keeping equipment groups together

CONNECT
Build on the preceding slide: Repeated equipment needs group separation.

LECTURER CUE
This toy split explains group separation. It does not establish a representative evaluation with only two pieces of equipment.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
Worked example (1/2). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Worked example (1/2).

## Slide 11 — Validation and leakage in Python (1/2)

PURPOSE
Validation and leakage in Python (1/2)

CONNECT
Build on Keeping equipment groups together. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
TEACHING PURPOSE
Worked example (1/2)

CONNECT
Build on the preceding slide: Keeping equipment groups together.

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

EXPLAIN IN ORDINARY WORDS
A dictionary pairs a key with a value. For {"unit":"A", "reading":4}, record["reading"] looks up the key and gives 4. The key is not a list position.

CHECK AND EXPECTED ANSWER
What happens if the key is spelled "Reading" instead? It is a different key; direct lookup can raise KeyError.

IF LEARNERS ARE STUCK
Point to each key and its value. Read the colon as associates-with, then do one exact lookup.

WALK THROUGH THIS CODE
Square brackets create a list or select an item.
Braces hold dictionary key: value pairs here.
= assigns the value on the right to the name on the left.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Worked example (2/2). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Worked example (2/2).

## Slide 12 — Validation and leakage in Python (2/2)

PURPOSE
Validation and leakage in Python (2/2)

CONNECT
Build on Validation and leakage in Python (1/2). Explain why this example is needed before running it.

EXPLAIN
Continue the SAME cell; keep indentation. Run after all parts are entered.

LECTURER DETAIL
TEACHING PURPOSE
Worked example (2/2)

CONNECT
Build on the preceding slide: Worked example (1/2).

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

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

WALK THROUGH THIS CODE
for takes the next item. The indented block repeats.
if tests a condition. The chosen indented block runs.
print displays a value below the cell.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Expected output. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Expected output.

## Slide 13 — Validation and leakage results

PURPOSE
Validation and leakage results

CONNECT
Build on Validation and leakage in Python (2/2). Explain why this example is needed before running it.

EXPLAIN
[1, 2] [3]

LECTURER DETAIL
TEACHING PURPOSE
Expected output

CONNECT
Build on the preceding slide: Worked example (2/2).

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

NEXT
Preprocessing and pipeline. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Preprocessing and pipeline.

## Slide 14 — Preprocessing and pipeline

PURPOSE
Preprocessing and pipeline

CONNECT
Build on Validation and leakage results. Explain why this example is needed before running it.

EXPLAIN
Preprocessing and pipeline: Preprocessing changes inputs, for example filling missing values. A pipeline fits these steps on training data and applies the same fitted changes to new inputs.

LECTURER DETAIL
TEACHING PURPOSE
Preprocessing and pipeline

CONNECT
Build on the preceding slide: Expected output.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

POINT TO THE DEFINITION
Preprocessing and pipeline: Preprocessing changes inputs, for example filling missing values. A pipeline fits these steps on training data and applies the same fitted changes to new inputs.

NEXT
A learned cleaning value comes from training. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A learned cleaning value comes from training.

## Slide 15 — A learned cleaning value comes from training

PURPOSE
A learned cleaning value comes from training

CONNECT
Build on Preprocessing and pipeline. Explain why this example is needed before running it.

EXPLAIN
The training readings are 20, 22 and 24. Their median is 22.

A missing validation value receives the already learned 22.

A new validation reading of 40 must not change the fitted median.

LECTURER DETAIL
TEACHING PURPOSE
A learned cleaning value comes from training

CONNECT
Build on the preceding slide: Preprocessing and pipeline.

LECTURER CUE
Fit a missing-value replacement on training values [20, 22, 24]: the median is 22. A new hotter observation must not change that fitted median.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

NEXT
A training-only fill value. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A training-only fill value in Python (1/2).

## Slide 16 — A training-only fill value in Python (1/2)

PURPOSE
A training-only fill value in Python (1/2)

CONNECT
Build on A learned cleaning value comes from training. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
TEACHING PURPOSE
A training-only fill value in Python (1/2)

CONNECT
Build on the preceding slide: A training-only fill value.

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

EXPLAIN IN ORDINARY WORDS
Training fits rules. Validation helps choose among rules. The final test estimates performance after choices are fixed. Information that would be unavailable at the real prediction time must stay out of the inputs.

CHECK AND EXPECTED ANSWER
May two readings of the same machine appear on both sides when evaluating new machines? No; split by machine. For forecasting, train on the past and evaluate later time.

IF LEARNERS ARE STUCK
Use three envelopes. Keep the final-test envelope closed while selecting features or settings.

WALK THROUGH THIS CODE
import loads a library. from selects a tool from it.
Square brackets create a list or select an item.
= assigns the value on the right to the name on the left.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
A training-only fill value in Python (2/2). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A training-only fill value in Python (2/2).

## Slide 17 — A training-only fill value in Python (2/2)

PURPOSE
A training-only fill value in Python (2/2)

CONNECT
Build on A training-only fill value in Python (1/2). Explain why this example is needed before running it.

EXPLAIN
Continue the SAME cell; keep indentation. Run after all parts are entered.

LECTURER DETAIL
TEACHING PURPOSE
A training-only fill value in Python (2/2)

CONNECT
Build on the preceding slide: A training-only fill value in Python (1/2).

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

EXPLAIN IN ORDINARY WORDS
Training fits rules. Validation helps choose among rules. The final test estimates performance after choices are fixed. Information that would be unavailable at the real prediction time must stay out of the inputs.

CHECK AND EXPECTED ANSWER
May two readings of the same machine appear on both sides when evaluating new machines? No; split by machine. For forecasting, train on the past and evaluate later time.

IF LEARNERS ARE STUCK
Use three envelopes. Keep the final-test envelope closed while selecting features or settings.

WALK THROUGH THIS CODE
for takes the next item. The indented block repeats.
if tests a condition. The chosen indented block runs.
print displays a value below the cell.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Leakage gives away information from the future. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Leakage gives away information from the future.

## Slide 18 — Leakage gives away information from the future

PURPOSE
Leakage gives away information from the future

CONNECT
Build on A training-only fill value in Python (2/2). Explain why this example is needed before running it.

EXPLAIN
Suppose we predict a fault before an inspection.

final_inspection_result exists only after the inspection.

Using it as an input would answer a different, easier question than the one we intended.

LECTURER DETAIL
TEACHING PURPOSE
Leakage gives away information from the future

CONNECT
Build on the preceding slide: A training-only fill value in Python (2/2).

LECTURER CUE
Show a counterexample: if every input contains a field called final_inspection_result recorded after the outcome, an excellent score can be meaningless for earlier prediction.

EXPLAIN IN ORDINARY WORDS
Training fits rules. Validation helps choose among rules. The final test estimates performance after choices are fixed. Information that would be unavailable at the real prediction time must stay out of the inputs.

CHECK AND EXPECTED ANSWER
May two readings of the same machine appear on both sides when evaluating new machines? No; split by machine. For forecasting, train on the past and evaluate later time.

IF LEARNERS ARE STUCK
Use three envelopes. Keep the final-test envelope closed while selecting features or settings.

NEXT
Cross-validation. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Parameters hyperparameters and a fold.

## Slide 19 — Parameters hyperparameters and a fold

PURPOSE
Parameters hyperparameters and a fold

CONNECT
Build on Leakage gives away information from the future. Explain why this example is needed before running it.

EXPLAIN
A parameter is learned during fitting, such as a line’s slope. A hyperparameter is a setting chosen around fitting, such as a tree’s max_depth.

A fold is one part of the development data used for a validation turn. Refit the entire preprocessing and model on the other parts for that turn.

Compare candidate settings using validation evidence. Keep the final test outside that selection process.

LECTURER DETAIL


TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Cross-validation.

## Slide 20 — Cross-validation

PURPOSE
Cross-validation

CONNECT
Build on Parameters hyperparameters and a fold. Explain why this example is needed before running it.

EXPLAIN
Cross-validation: Repeat fitting and validation on several partitions of the training/development data. Respect groups or time order. Keep the final test outside tuning.

LECTURER DETAIL
TEACHING PURPOSE
Cross-validation

CONNECT
Build on the preceding slide: Leakage gives away information from the future.

EXPLAIN IN ORDINARY WORDS
Cross-validation repeats training and validation on different partitions. Each fold gets a newly fitted model and preprocessing. Variation across fold scores shows sensitivity to the partition.

CHECK AND EXPECTED ANSWER
May preprocessing learn from all rows before the folds? No, that would give each validation fold information from outside its training portion.

IF LEARNERS ARE STUCK
Draw three small partitions and label who learns and who is evaluated. Fold spread is not automatically a confidence interval.

POINT TO THE DEFINITION
Cross-validation: Repeat fitting and validation on several partitions of the training/development data. Respect groups or time order. Keep the final test outside tuning.

NEXT
What standard deviation tells us. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
What standard deviation tells us.

## Slide 21 — What standard deviation tells us

PURPOSE
What standard deviation tells us

CONNECT
Build on Cross-validation. Explain why this example is needed before running it.

EXPLAIN
Scores 3, 4 and 5 have mean 4. Their deviations are -1, 0 and 1.

For these three fold scores, population SD = sqrt((1 + 0 + 1) / 3), about 0.82.

SD describes spread around the mean in the score’s units. The next illustration uses this same population convention; it is not a confidence interval.

LECTURER DETAIL
TEACHING PURPOSE
What standard deviation tells us

CONNECT
Build on the preceding slide: Cross-validation.

LECTURER CUE
Square each deviation, average all three, then take the square root. Here we describe the full displayed set. A sample SD would instead divide by n - 1; do not mix conventions.

EXPLAIN IN ORDINARY WORDS
Cross-validation repeats training and validation on different partitions. Each fold gets a newly fitted model and preprocessing. Variation across fold scores shows sensitivity to the partition.

CHECK AND EXPECTED ANSWER
May preprocessing learn from all rows before the folds? No, that would give each validation fold information from outside its training portion.

IF LEARNERS ARE STUCK
Draw three small partitions and label who learns and who is evaluated. Fold spread is not automatically a confidence interval.

NEXT
Each fold takes a turn at validation. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Each fold takes a turn at validation.

## Slide 22 — Each fold takes a turn at validation

PURPOSE
Each fold takes a turn at validation

CONNECT
Build on What standard deviation tells us. Explain why this example is needed before running it.

EXPLAIN
Illustrated spread: population SD 0.39 MPa, not a confidence interval.

LECTURER DETAIL
TEACHING PURPOSE
Each fold takes a turn at validation

CONNECT
Build on the preceding slide: What standard deviation tells us.

LECTURER CUE
The illustrated mean is about 4.30 MPa and population standard deviation about 0.39 MPa. This is fold variation, not a confidence interval. Keep equipment groups together. Keep a separate final test outside model selection.
Source: existing course illustration figs/kfold.png. These are illustrative examples, not this cohort’s assessed results.

NEXT
Choose a split that matches future use. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Choose a split that matches future use.

## Slide 23 — Choose a split that matches future use

PURPOSE
Choose a split that matches future use

CONNECT
Build on Each fold takes a turn at validation. Explain why this example is needed before running it.

EXPLAIN
Equipment or time: For unseen equipment, keep each equipment ID together. For future-time prediction, train on earlier observations and evaluate on later ones.
Scaler and split tool: A scaler learns how to rescale features; fit it on training data. GroupShuffleSplit is a library tool for group separation. Our assignment instead uses its fixed published equipment lists.

LECTURER DETAIL
TEACHING PURPOSE
Choose a split that matches future use

CONNECT
Build on the preceding slide: Each fold takes a turn at validation.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

POINT TO THE DEFINITION
Equipment or time: For unseen equipment, keep each equipment ID together. For future-time prediction, train on earlier observations and evaluate on later ones.
Scaler and split tool: A scaler learns how to rescale features; fit it on training data. GroupShuffleSplit is a library tool for group separation. Our assignment instead uses its fixed published equipment lists.

NEXT
You are the data splitter. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Revision example and answer.

## Slide 24 — Revision example and answer

PURPOSE
Revision example and answer

CONNECT
Build on Choose a split that matches future use. Explain why this example is needed before running it.

EXPLAIN
Example: A second observation from B arrives. Where does it go? Why not put it into training just to balance row counts?

Answer: It stays with B in validation. Mixing a source across partitions can give an overly optimistic estimate for unseen equipment.

LECTURER DETAIL
TEACHING PURPOSE
Your turn

CONNECT
Build on the preceding slide: What the activity shows.

LECTURER CUE
Give silent thinking time, then let pairs discuss. Rotate who types. This is practice, not a graded quiz. Expected response: It stays with B in validation. Mixing a source across partitions can give an overly optimistic estimate for unseen equipment.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

DISCUSSION KEY FOR THIS SLIDE
DISCUSS THE REASONING
Practice discussion
It stays with B in validation. Mixing a source across partitions can give an overly optimistic estimate for unseen equipment.
Which step produced this result? What changes if one input changes?
CML3112   Week 10   27
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
Practice discussion. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Preparing for the assignment.

## Slide 25 — Preparing for the assignment

PURPOSE
Preparing for the assignment

CONNECT
Build on Revision example and answer. Explain why this example is needed before running it.

EXPLAIN
W10 specifies E1–E4 train, E5 validation, E6 test and preserves input order.

Use the assigned equipment_id field and record_id outputs.

Reuse the W08 fitting pattern.

Explain that GroupShuffleSplit and time-based splitting solve different deployment questions; use the rule in the issued task.

LECTURER DETAIL
TEACHING PURPOSE
Preparing for the assignment

CONNECT
Build on the preceding slide: After the video.

LECTURER CUE
W10 specifies E1–E4 train, E5 validation, E6 test and preserves input order. Use the assigned equipment_id field and record_id outputs. Reuse the W08 fitting pattern. Explain that GroupShuffleSplit and time-based splitting solve different deployment questions; use the rule in the issued task.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Interpreting validation results. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Interpreting validation results.

## Slide 26 — Interpreting validation results

PURPOSE
Interpreting validation results

CONNECT
Build on Preparing for the assignment. Explain why this example is needed before running it.

EXPLAIN
Fit an imputer or scaler only on training data; putting it in a Pipeline helps enforce that during cross-validation.

A low training error and high validation error suggest overfitting, but data shift or leakage can also matter.

Missing predictor values need a stated treatment.

Report fold scores and their variation, not just the best fold.

LECTURER DETAIL
TEACHING PURPOSE
Interpreting validation results

CONNECT
Build on the preceding slide: Preparing for the assignment.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
Cross-validation repeats training and validation on different partitions. Each fold gets a newly fitted model and preprocessing. Variation across fold scores shows sensitivity to the partition.

CHECK AND EXPECTED ANSWER
May preprocessing learn from all rows before the folds? No, that would give each validation fold information from outside its training portion.

IF LEARNERS ARE STUCK
Draw three small partitions and label who learns and who is evaluated. Fold spread is not automatically a confidence interval.

NEXT
Interpreting validation results continued. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Interpreting validation results continued.

## Slide 27 — Interpreting validation results continued

PURPOSE
Interpreting validation results continued

CONNECT
Build on Interpreting validation results. Explain why this example is needed before running it.

EXPLAIN
Group related observations together when the deployment goal is new equipment.

LECTURER DETAIL
TEACHING PURPOSE
Interpreting validation results continued

CONNECT
Build on the preceding slide: Interpreting validation results.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
Your issued task. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Your issued task.

## Slide 28 — Your issued task

PURPOSE
Your issued task

CONNECT
Build on Interpreting validation results continued. Explain why this example is needed before running it.

EXPLAIN
Investigate building cooling load.

Target units: kW.

These are synthetic teaching records, not measurements suitable for deployment.

Each record is one operating observation; equipment_id repeats across observations.

LECTURER DETAIL
TEACHING PURPOSE
Your issued task

CONNECT
Build on the preceding slide: Interpreting validation results continued.

LECTURER CUE
Investigate building cooling load. Target units: kW. These are synthetic teaching records, not measurements suitable for deployment. Each record is one operating observation; equipment_id repeats across observations.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
group_split(records). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
group_split(records).

## Slide 29 — group_split(records)

PURPOSE
group_split(records)

CONNECT
Build on Your issued task. Explain why this example is needed before running it.

EXPLAIN
Assign whole equipment groups: E1–E4 to train, E5 to validation, E6 to test.

Return train, validation and test lists of record_id in input order.

Do not use target values to choose membership.

LECTURER DETAIL
TEACHING PURPOSE
group_split(records)

CONNECT
Build on the preceding slide: Your issued task.

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W10/CML3112/A/TASKS.md

EXPLAIN IN ORDINARY WORDS
Training fits rules. Validation helps choose among rules. The final test estimates performance after choices are fixed. Information that would be unavailable at the real prediction time must stay out of the inputs.

CHECK AND EXPECTED ANSWER
May two readings of the same machine appear on both sides when evaluating new machines? No; split by machine. For forecasting, train on the past and evaluate later time.

IF LEARNERS ARE STUCK
Use three envelopes. Keep the final-test envelope closed while selecting features or settings.

NEXT
predict_regression(training_records, feature_records). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
predict_regression(training_records, feature_records).

## Slide 30 — predict_regression(training_records, feature_records)

PURPOSE
predict_regression(training_records, feature_records)

CONNECT
Build on group_split(records). Explain why this example is needed before running it.

EXPLAIN
Fit a training-mean baseline, linear regression and a decision tree (max_depth=4, random_state=17) using load_pct and ambient_c only.

Return three prediction lists under baseline, linear and tree.

Feature records have no target.

Fit preprocessing only on training data.

LECTURER DETAIL
TEACHING PURPOSE
predict_regression(training_records, feature_records)

CONNECT
Build on the preceding slide: group_split(records).

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W10/CML3112/A/TASKS.md

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
Written evidence. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Written evidence.

## Slide 31 — Written evidence

PURPOSE
Written evidence

CONNECT
Build on predict_regression(training_records, feature_records). Explain why this example is needed before running it.

EXPLAIN
Use the cell headed “My written evidence”.

Explain the supplied scenario in your own words.

State target units, reasons and limitations.

Submit one complete notebook containing code and written evidence.

LECTURER DETAIL
TEACHING PURPOSE
Written evidence

CONNECT
Build on the preceding slide: predict_regression(training_records, feature_records).

LECTURER CUE
Published criterion weights and exact requirements remain in TASKS.md. Broader project exercises are formative and do not add weekly marks. Local automated reasoning assessment remains subject to its release checks.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Validation and trust submission. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Validation and trust submission.

## Slide 32 — Validation and trust submission

PURPOSE
Validation and trust submission

CONNECT
Build on Written evidence. Explain why this example is needed before running it.

EXPLAIN
Opens: 10 Nov 2026, 11:00 Kampala

Deadline: 17 Nov 2026, 11:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

LECTURER DETAIL
TEACHING PURPOSE
Validation and trust submission

CONNECT
Build on the preceding slide: Written evidence.

LECTURER CUE
The form link is cohort-specific. Recheck the live form and release status before class. These scheduled assignment dates are separate from the quiz activation window. The issued brief defines the required files, even if the form accepts additional formats. Source: data/submission_links.json

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Week 10 quiz. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Week 10 quiz.

## Slide 33 — Week 10 quiz

PURPOSE
Week 10 quiz

CONNECT
Build on Validation and trust submission. Explain why this example is needed before running it.

EXPLAIN
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

The lecturer will confirm the exact closing time.

LECTURER DETAIL
TEACHING PURPOSE
Week 10 quiz

CONNECT
Build on the preceding slide: Validation and trust submission.

LECTURER CUE
Activate the matching open_W10_CML3112 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

QUIZ OPERATION
Opening the student link does not activate the quiz. In Quiz Controls run the matching open_W<week>_<cohort> function once when ready. Announce the logged closing time: 24 hours after activation. Five minutes describes expected answering time, not the availability window. Quiz 1 and Quiz 2 require separate activation when collecting catch-up work.

NEXT
Before you leave. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Before you leave.

## Slide 34 — Revision and submission checklist

PURPOSE
Revision and submission checklist

CONNECT
Build on Week 10 quiz. Explain why this example is needed before running it.

EXPLAIN
You can identify which records may influence preprocessing and model selection.

Save your work and check the required submission files.

LECTURER DETAIL
TEACHING PURPOSE
Before you leave

CONNECT
Build on the preceding slide: Week 10 quiz.

LECTURER CUE
Ask every learner for an individual response. Record one misconception to revisit at the start of the next class. If a deadline changed, announce the exact Kampala date and update the source registry before rebuilding slides.

EXPLAIN IN ORDINARY WORDS
First remove models that fail the stated error or speed limits. Then apply the stated ranking and tie-break rules to eligible models. The smallest error alone need not decide.

CHECK AND EXPECTED ANSWER
If a model has the lowest error but exceeds the maximum latency, is it eligible? No.

IF LEARNERS ARE STUCK
Write an eligibility column and a separate ranking column. Check the exact boundary rule before sorting.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Optional revision video.

## Slide 35 — Optional revision video

PURPOSE
Optional revision video

CONNECT
Build on Revision and submission checklist. Explain why this example is needed before running it.

EXPLAIN
For revision after class.

StatQuest with Josh Starmer
Machine Learning Fundamentals Cross Validation

Opening up to 04:00, optional preview-selected excerpt

Listening question: Why evaluate using observations not used to fit that particular model?

LECTURER DETAIL
TEACHING PURPOSE
Short explainer and discussion

CONNECT
Build on the preceding slide: Practice discussion.

LECTURER CUE
Linked by the official StatQuest video index. Full audiovisual preview and excerpt timing still required.
After viewing: Explain why our repeated equipment IDs require grouped partitions rather than ordinary random folds.
Preview before class and stop after the selected short excerpt. If playback fails, teach the worked example. Video is optional. Source: https://www.youtube.com/watch?v=fSytzGwwBVw

EXPLAIN IN ORDINARY WORDS
Cross-validation repeats training and validation on different partitions. Each fold gets a newly fitted model and preprocessing. Variation across fold scores shows sensitivity to the partition.

CHECK AND EXPECTED ANSWER
May preprocessing learn from all rows before the folds? No, that would give each validation fold information from outside its training portion.

IF LEARNERS ARE STUCK
Draw three small partitions and label who learns and who is evaluated. Fold spread is not automatically a confidence interval.

VIDEO ROUTINE
Preview the exact link and stated excerpt before class. State the viewing question first, pause after the example, and ask a learner to explain it. If access fails, use the adjacent worked example and discussion rather than spend class time troubleshooting streaming.

NEXT
After the video. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
independent revision and the issued task.
