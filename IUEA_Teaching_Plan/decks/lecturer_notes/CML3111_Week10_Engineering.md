# CML3111 Week10 Engineering

Lecturer companion. The same explanations are embedded in the PowerPoint speaker notes. Open Presenter View, or expand the Notes pane when preparing.

## Slide 1 — Honest validation and leakage

Honest validation and leakage
CML3111, Week 10, slide 1

Explanation to give
Connect evaluation to intended use. Decide how to hold out observations before fitting either preprocessing or the model.

Worked illustration / lecturer answer
When testing new equipment, all observations from equipment A stay in one partition. Training must not learn its missing-value replacements from held-out equipment.

Misconception to address
Use this as an orientation to the lesson. Terms and syntax will be unpacked on their own slides; students do not need to know them in advance.

On this slide
Communications, Electrical, Mechatronics and Robotics Engineering

Continue to
Today’s learning

## Slide 2 — Today’s learning

Today’s learning
CML3111, Week 10, slide 2

Explanation to give
Connect evaluation to intended use. Decide how to hold out observations before fitting either preprocessing or the model.

Worked illustration / lecturer answer
When testing new equipment, all observations from equipment A stay in one partition. Training must not learn its missing-value replacements from held-out equipment.

Misconception to address
At the end, check the specific outcome shown here using a small previously demonstrated example. A completed file without an explanation is not evidence of understanding.

On this slide
Keep related equipment records together.

Separate training, validation and final testing.

Continue to
Connection to the previous lesson

## Slide 3 — Connection to the previous lesson

Connection to the previous lesson
CML3111, Week 10, slide 3

Explanation to give
Connect evaluation to intended use. Decide how to hold out observations before fitting either preprocessing or the model.

Worked illustration / lecturer answer
When testing new equipment, all observations from equipment A stay in one partition. Training must not learn its missing-value replacements from held-out equipment.

Misconception to address
Connect this to the previous result named on this slide. Demonstrate the first step again if necessary; there is no requirement for partner work before the explanation.

On this slide
We have compared predictions with known answers. Now we control which observations may influence training, choices and the final evaluation.

Continue to
Why this week’s tools are needed

## Slide 4 — Why this week’s tools are needed

Why this week’s tools are needed
CML3111, Week 10, slide 4

Explanation to give
Connect evaluation to intended use. Decide how to hold out observations before fitting either preprocessing or the model.

Worked illustration / lecturer answer
When testing new equipment, all observations from equipment A stay in one partition. Training must not learn its missing-value replacements from held-out equipment.

Misconception to address
Connect this to the previous result named on this slide. Demonstrate the first step again if necessary; there is no requirement for partner work before the explanation.

On this slide
We want evidence about new equipment or future observations. The way we separate data must match that use before any model or preprocessing learns from it.

Continue to
Training validation and final test

## Slide 5 — Training validation and final test

Training validation and final test
CML3111, Week 10, slide 5

Explanation to give
Training observations teach the model. Validation observations help choose among models and settings. The final test is reserved for evaluating the chosen method after those choices are fixed.

Worked illustration / lecturer answer
Compare two models using the same validation observations, choose a method, then evaluate it once on the held-out test. Imagine the test as a sealed examination paper.

Misconception to address
Repeatedly checking the test while selecting features or settings makes it part of the selection process, so it no longer gives an independent final check.

On this slide
Training data fit the model and preprocessing.

Validation data guide feature and model choices.

The final test evaluates choices after they are fixed.

A fresh test is needed if its answers influenced further choices.

Continue to
Three sets have different jobs

## Slide 6 — Three sets have different jobs

Three sets have different jobs
CML3111, Week 10, slide 6

Explanation to give
Training observations teach the model. Validation observations help choose among models and settings. The final test is reserved for evaluating the chosen method after those choices are fixed.

Worked illustration / lecturer answer
Compare two models using the same validation observations, choose a method, then evaluate it once on the held-out test. Imagine the test as a sealed examination paper.

Misconception to address
Repeatedly checking the test while selecting features or settings makes it part of the selection process, so it no longer gives an independent final check.

On this slide
Which set must stay sealed until choices are fixed?

Continue to
Generalisation and Overfitting and underfitting

## Slide 7 — Generalisation and Overfitting and underfitting

Generalisation and Overfitting and underfitting
CML3111, Week 10, slide 7

Explanation to give
Generalisation means working on relevant observations not used to learn the model. Overfitting captures training-specific detail; underfitting misses useful structure even in training.

Worked illustration / lecturer answer
A very deep tree may memorise noisy training readings. A constant baseline may miss a clear trend. Compare training and validation errors to diagnose these possibilities.

Misconception to address
A gap between errors is evidence to investigate, not proof of one cause. Check whether the evaluation data actually represents future use.

On this slide
Generalisation: Performance on new cases from the intended setting, not merely on records already used.
Overfitting and underfitting: Overfitting captures training-specific detail that fails to transfer. Underfitting misses useful patterns. Score gaps are clues, not a complete diagnosis.

Continue to
Leakage and Group split

## Slide 8 — Leakage and Group split

Leakage and Group split
CML3111, Week 10, slide 8

Explanation to give
If the intended use is new equipment, keep all observations from each equipment ID together in one partition. Otherwise near-related records can make evaluation look easier than deployment.

Worked illustration / lecturer answer
Equipment A recorded on Monday and Tuesday belongs in one partition under a group split. Splitting those two rows across train and validation lets the model see the same equipment on both sides.

Misconception to address
Different record IDs do not guarantee independent equipment. For forecasting, chronology may be the key constraint instead; choose the split to match the stated use.

On this slide
Leakage: Information enters model development that would not legitimately be available, such as the answer or information from evaluation rows.
Group split: Keep all observations from the same equipment in one partition when the goal is prediction for unseen equipment.

Continue to
Repeated equipment needs group separation

## Slide 9 — Repeated equipment needs group separation

Repeated equipment needs group separation
CML3111, Week 10, slide 9

Explanation to give
If the intended use is new equipment, keep all observations from each equipment ID together in one partition. Otherwise near-related records can make evaluation look easier than deployment.

Worked illustration / lecturer answer
Equipment A recorded on Monday and Tuesday belongs in one partition under a group split. Splitting those two rows across train and validation lets the model see the same equipment on both sides.

Misconception to address
Different record IDs do not guarantee independent equipment. For forecasting, chronology may be the key constraint instead; choose the split to match the stated use.

On this slide
Readings from the same equipment can share patterns.

Putting that equipment in both training and validation can make evaluation too easy.

For a new-equipment question, keep every row for an equipment ID in one partition.

Continue to
Keeping equipment groups together

## Slide 10 — Keeping equipment groups together

Keeping equipment groups together
CML3111, Week 10, slide 10

Explanation to give
If the intended use is new equipment, keep all observations from each equipment ID together in one partition. Otherwise near-related records can make evaluation look easier than deployment.

Worked illustration / lecturer answer
Equipment A recorded on Monday and Tuesday belongs in one partition under a group split. Splitting those two rows across train and validation lets the model see the same equipment on both sides.

Misconception to address
Different record IDs do not guarantee independent equipment. For forecasting, chronology may be the key constraint instead; choose the split to match the stated use.

On this slide
Observation | Equipment | Partition
1 | A | Training
2 | A | Training
3 | B | Validation
This small example separates equipment groups.

Continue to
Validation and leakage in Python (1/2)

## Slide 11 — Validation and leakage in Python (1/2)

Validation and leakage in Python (1/2)
CML3111, Week 10, slide 11

Explanation to give
If the intended use is new equipment, keep all observations from each equipment ID together in one partition. Otherwise near-related records can make evaluation look easier than deployment.

Worked illustration / lecturer answer
Equipment A recorded on Monday and Tuesday belongs in one partition under a group split. Splitting those two rows across train and validation lets the model see the same equipment on both sides.

Misconception to address
Different record IDs do not guarantee independent equipment. For forecasting, chronology may be the key constraint instead; choose the split to match the stated use.

Read the displayed code line by line
records = [{"id": 1, "equipment": "A"},
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

{"id": 2, "equipment": "A"},
This line continues the surrounding expression or block; read it together with the preceding line rather than running it alone.

{"id": 3, "equipment": "B"}]
This line continues the surrounding expression or block; read it together with the preceding line rather than running it alone.

train = []
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

validation = []
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Validation and leakage in Python (2/2)

## Slide 12 — Validation and leakage in Python (2/2)

Validation and leakage in Python (2/2)
CML3111, Week 10, slide 12

Explanation to give
If the intended use is new equipment, keep all observations from each equipment ID together in one partition. Otherwise near-related records can make evaluation look easier than deployment.

Worked illustration / lecturer answer
Equipment A recorded on Monday and Tuesday belongs in one partition under a group split. Splitting those two rows across train and validation lets the model see the same equipment on both sides.

Misconception to address
Different record IDs do not guarantee independent equipment. For forecasting, chronology may be the key constraint instead; choose the split to match the stated use.

Read the displayed code line by line
for row in records:
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

if row["equipment"] == "A":
Evaluate this yes/no condition. Execute its indented body only on the matching path.

train.append(row["id"])
Evaluate the argument and add it as one new item at the end of this list.

else:
Use this remaining path when the matching earlier condition did not succeed.

validation.append(row["id"])
Evaluate the argument and add it as one new item at the end of this list.

print(train, validation)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Continue the SAME cell; keep indentation. Run after all parts are entered.

Continue to
Validation and leakage results

## Slide 13 — Validation and leakage results

Validation and leakage results
CML3111, Week 10, slide 13

Explanation to give
If the intended use is new equipment, keep all observations from each equipment ID together in one partition. Otherwise near-related records can make evaluation look easier than deployment.

Worked illustration / lecturer answer
Equipment A recorded on Monday and Tuesday belongs in one partition under a group split. Splitting those two rows across train and validation lets the model see the same equipment on both sides.

Misconception to address
Different record IDs do not guarantee independent equipment. For forecasting, chronology may be the key constraint instead; choose the split to match the stated use.

On this slide
[1, 2] [3]

Continue to
Preprocessing and pipeline

## Slide 14 — Preprocessing and pipeline

Preprocessing and pipeline
CML3111, Week 10, slide 14

Explanation to give
A pipeline keeps preparation and prediction in one ordered procedure. Fit learns preparation values from training data and then fits the model. Prediction reuses those saved values.

Worked illustration / lecturer answer
For training feature values 20, 22, missing and 24, the learned median is 22. A missing value in a new observation also receives 22, without recalculating from the new observations.

Misconception to address
Filling all records before splitting leaks information. A pipeline avoids that only when its fit receives the correct training subset.

On this slide
Preprocessing and pipeline: Preprocessing changes inputs, for example filling missing values. A pipeline fits these steps on training data and applies the same fitted changes to new inputs.

Continue to
A learned cleaning value comes from training

## Slide 15 — A learned cleaning value comes from training

A learned cleaning value comes from training
CML3111, Week 10, slide 15

Explanation to give
A pipeline keeps preparation and prediction in one ordered procedure. Fit learns preparation values from training data and then fits the model. Prediction reuses those saved values.

Worked illustration / lecturer answer
For training feature values 20, 22, missing and 24, the learned median is 22. A missing value in a new observation also receives 22, without recalculating from the new observations.

Misconception to address
Filling all records before splitting leaks information. A pipeline avoids that only when its fit receives the correct training subset.

On this slide
The training readings are 20, 22 and 24. Their median is 22.

A missing validation value receives the already learned 22.

A new validation reading of 40 must not change the fitted median.

Continue to
A training-only fill value in Python (1/2)

## Slide 16 — A training-only fill value in Python (1/2)

A training-only fill value in Python (1/2)
CML3111, Week 10, slide 16

Explanation to give
A pipeline keeps preparation and prediction in one ordered procedure. Fit learns preparation values from training data and then fits the model. Prediction reuses those saved values.

Worked illustration / lecturer answer
For training feature values 20, 22, missing and 24, the learned median is 22. A missing value in a new observation also receives 22, without recalculating from the new observations.

Misconception to address
Filling all records before splitting leaks information. A pipeline avoids that only when its fit receives the correct training subset.

Read the displayed code line by line
from statistics import median
Bring the named tool from this library into the current Python session.

training_values = [20, 22, 24]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

validation_values = [None, 40]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

training_median = median(training_values)
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

filled_validation = []
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
A training-only fill value in Python (2/2)

## Slide 17 — A training-only fill value in Python (2/2)

A training-only fill value in Python (2/2)
CML3111, Week 10, slide 17

Explanation to give
A pipeline keeps preparation and prediction in one ordered procedure. Fit learns preparation values from training data and then fits the model. Prediction reuses those saved values.

Worked illustration / lecturer answer
For training feature values 20, 22, missing and 24, the learned median is 22. A missing value in a new observation also receives 22, without recalculating from the new observations.

Misconception to address
Filling all records before splitting leaks information. A pipeline avoids that only when its fit receives the correct training subset.

Read the displayed code line by line
for value in validation_values:
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

if value is None:
Evaluate this yes/no condition. Execute its indented body only on the matching path.

filled_validation.append(training_median)
Evaluate the argument and add it as one new item at the end of this list.

else:
Use this remaining path when the matching earlier condition did not succeed.

filled_validation.append(value)
Evaluate the argument and add it as one new item at the end of this list.

print(training_median, filled_validation)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Continue the SAME cell; keep indentation. Run after all parts are entered.

Continue to
Leakage gives away information from the future

## Slide 18 — Leakage gives away information from the future

Leakage gives away information from the future
CML3111, Week 10, slide 18

Explanation to give
If the intended use is new equipment, keep all observations from each equipment ID together in one partition. Otherwise near-related records can make evaluation look easier than deployment.

Worked illustration / lecturer answer
Equipment A recorded on Monday and Tuesday belongs in one partition under a group split. Splitting those two rows across train and validation lets the model see the same equipment on both sides.

Misconception to address
Different record IDs do not guarantee independent equipment. For forecasting, chronology may be the key constraint instead; choose the split to match the stated use.

On this slide
Suppose we predict a fault before an inspection.

final_inspection_result exists only after the inspection.

Using it as an input would answer a different, easier question than the one we intended.

Continue to
Parameters hyperparameters and a fold

## Slide 19 — Parameters hyperparameters and a fold

Parameters hyperparameters and a fold
CML3111, Week 10, slide 19

Explanation to give
A parameter is learned during fit. A hyperparameter is chosen as a setting. Cross-validation repeats fitting with different held-out portions of the development data to assess choices more steadily.

Worked illustration / lecturer answer
If validation errors are 2, 3 and 4, the mean is 3. Their spread indicates sensitivity to the held-out portion. A standard deviation describes that spread; it is not automatically a confidence interval.

Misconception to address
Fit preprocessing separately within each training fold. Keep groups or time order intact where required. The final test remains separate from tuning.

On this slide
A parameter is learned during fitting, such as a line’s slope. A hyperparameter is a setting chosen around fitting, such as a tree’s max_depth.

A fold is one part of the development data used for a validation turn. Refit the entire preprocessing and model on the other parts for that turn.

Compare candidate settings using validation evidence. Keep the final test outside that selection process.

Continue to
Cross-validation

## Slide 20 — Cross-validation

Cross-validation
CML3111, Week 10, slide 20

Explanation to give
A parameter is learned during fit. A hyperparameter is chosen as a setting. Cross-validation repeats fitting with different held-out portions of the development data to assess choices more steadily.

Worked illustration / lecturer answer
If validation errors are 2, 3 and 4, the mean is 3. Their spread indicates sensitivity to the held-out portion. A standard deviation describes that spread; it is not automatically a confidence interval.

Misconception to address
Fit preprocessing separately within each training fold. Keep groups or time order intact where required. The final test remains separate from tuning.

On this slide
Cross-validation: Repeat fitting and validation on several partitions of the training/development data. Respect groups or time order. Keep the final test outside tuning.

Continue to
What standard deviation tells us

## Slide 21 — What standard deviation tells us

What standard deviation tells us
CML3111, Week 10, slide 21

Explanation to give
A parameter is learned during fit. A hyperparameter is chosen as a setting. Cross-validation repeats fitting with different held-out portions of the development data to assess choices more steadily.

Worked illustration / lecturer answer
If validation errors are 2, 3 and 4, the mean is 3. Their spread indicates sensitivity to the held-out portion. A standard deviation describes that spread; it is not automatically a confidence interval.

Misconception to address
Fit preprocessing separately within each training fold. Keep groups or time order intact where required. The final test remains separate from tuning.

On this slide
Scores 3, 4 and 5 have mean 4. Their deviations are -1, 0 and 1.

For these three fold scores, population SD = sqrt((1 + 0 + 1) / 3), about 0.82.

SD describes spread around the mean in the score’s units. The next illustration uses this same population convention; it is not a confidence interval.

Continue to
Trace three validation turns

## Slide 22 — Trace three validation turns

Trace three validation turns
CML3111, Week 10, slide 22

Explanation to give
A parameter is learned during fit. A hyperparameter is chosen as a setting. Cross-validation repeats fitting with different held-out portions of the development data to assess choices more steadily.

Worked illustration / lecturer answer
If validation errors are 2, 3 and 4, the mean is 3. Their spread indicates sensitivity to the held-out portion. A standard deviation describes that spread; it is not automatically a confidence interval.

Misconception to address
Fit preprocessing separately within each training fold. Keep groups or time order intact where required. The final test remains separate from tuning.

On this slide
Turn | Fit using | Validate using
1 | Parts B and C | Part A
2 | Parts A and C | Part B
3 | Parts A and B | Part C
Refit preprocessing in every turn. The separate final test is not A, B or C.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Each fold takes a turn at validation

## Slide 23 — Each fold takes a turn at validation

Each fold takes a turn at validation
CML3111, Week 10, slide 23

Explanation to give
A parameter is learned during fit. A hyperparameter is chosen as a setting. Cross-validation repeats fitting with different held-out portions of the development data to assess choices more steadily.

Worked illustration / lecturer answer
If validation errors are 2, 3 and 4, the mean is 3. Their spread indicates sensitivity to the held-out portion. A standard deviation describes that spread; it is not automatically a confidence interval.

Misconception to address
Fit preprocessing separately within each training fold. Keep groups or time order intact where required. The final test remains separate from tuning.

On this slide
Illustrated spread: population SD 0.39 MPa, not a confidence interval.

Continue to
Choose a split that matches future use

## Slide 24 — Choose a split that matches future use

Choose a split that matches future use
CML3111, Week 10, slide 24

Explanation to give
A parameter is learned during fit. A hyperparameter is chosen as a setting. Cross-validation repeats fitting with different held-out portions of the development data to assess choices more steadily.

Worked illustration / lecturer answer
If validation errors are 2, 3 and 4, the mean is 3. Their spread indicates sensitivity to the held-out portion. A standard deviation describes that spread; it is not automatically a confidence interval.

Misconception to address
Fit preprocessing separately within each training fold. Keep groups or time order intact where required. The final test remains separate from tuning.

On this slide
Equipment or time: For unseen equipment, keep each equipment ID together. For future-time prediction, train on earlier observations and evaluate on later ones.
Scaler and split tool: A scaler learns how to rescale features; fit it on training data. GroupShuffleSplit is a library tool for group separation. Our assignment instead uses its fixed published equipment lists.

Continue to
Revision example and answer

## Slide 25 — Revision example and answer

Revision example and answer
CML3111, Week 10, slide 25

Explanation to give
Use the displayed example as a short individual revision question, then explain the reasoning behind its answer.

Worked illustration / lecturer answer
Example: A second observation from B arrives. Where does it go? Why not put it into training just to balance row counts?

Answer: It stays with B in validation. Mixing a source across partitions can give an overly optimistic estimate for unseen equipment.

Misconception to address
Trace the operation that changes the value rather than accepting a memorised output. For notebook-state examples, specify which cell is repeated and whether the initialisation ran again.

Continue to
Preparing for the assignment

## Slide 26 — Preparing for the assignment

Preparing for the assignment
CML3111, Week 10, slide 26

Explanation to give
Explain the order: partition data using the stated protocol, fit preparation on training data, fit models, compare on validation data and leave final test data untouched until choices are fixed.

Worked illustration / lecturer answer
Compare models on identical held-out observations with the same metric and preprocessing rules. Each cross-validation training fold learns its own preparation values.

Misconception to address
A written claim of no leakage must agree with the executable split and fitting code. Follow the published execution requirement for any criterion linked to the split check.

On this slide
W10 specifies E1–E4 train, E5 validation, E6 test and preserves input order.

Use the assigned equipment_id field and record_id outputs.

Reuse the W08 fitting pattern.

GroupShuffleSplit separates equipment groups. A time-based split separates earlier and later records. Follow the split required by your task.

Continue to
Interpreting validation results

## Slide 27 — Interpreting validation results

Interpreting validation results
CML3111, Week 10, slide 27

Explanation to give
Explain what population the validation result represents. A model evaluated on unseen equipment supports a different claim from one evaluated on new readings from already-seen equipment.

Worked illustration / lecturer answer
If group splitting increases error compared with a row shuffle, the earlier score may have benefited from seeing related equipment. Report both the protocol and the error rather than concealing the harder result.

Misconception to address
A fixed random seed makes the split repeatable, not necessarily representative. Examine group coverage and future operating conditions.

On this slide
Fit an imputer or scaler only on training data; putting it in a Pipeline helps enforce that during cross-validation.

A low training error and high validation error suggest overfitting, but data shift or leakage can also matter.

Missing predictor values need a stated treatment.

Report fold scores and their variation, not just the best fold.

Continue to
Interpreting validation results continued

## Slide 28 — Interpreting validation results continued

Interpreting validation results continued
CML3111, Week 10, slide 28

Explanation to give
Explain what population the validation result represents. A model evaluated on unseen equipment supports a different claim from one evaluated on new readings from already-seen equipment.

Worked illustration / lecturer answer
If group splitting increases error compared with a row shuffle, the earlier score may have benefited from seeing related equipment. Report both the protocol and the error rather than concealing the harder result.

Misconception to address
A fixed random seed makes the split repeatable, not necessarily representative. Examine group coverage and future operating conditions.

On this slide
Group related observations together when the deployment goal is new equipment.

Continue to
Your issued task

## Slide 29 — Your issued task

Your issued task
CML3111, Week 10, slide 29

Explanation to give
Name this cohort’s target and its unit exactly as displayed. Each row is one operating observation, while equipment_id can repeat across several observations.

Worked illustration / lecturer answer
Explain record_id as the identifier of an observation, load_pct as load expressed in percent and ambient_c as temperature in degrees Celsius. The target records the known answer in training data.

Misconception to address
These are synthetic examples for learning. They do not establish a calibrated physical relationship or justify operation of real equipment.

On this slide
Investigate motor winding temperature.

Target units: deg C.

These are synthetic teaching records, not measurements suitable for deployment.

Each record is one operating observation; equipment_id repeats across observations.

Continue to
group_split(records)

## Slide 30 — group_split(records)

group_split(records)
CML3111, Week 10, slide 30

Explanation to give
Choose groups using the task’s deterministic rule, then return record IDs in the required train, validation and test lists.

Worked illustration / lecturer answer
Check that each equipment ID appears in only one partition and that every record is accounted for. A random row split does not satisfy this interface.

Misconception to address
Keep the exact output names and required types. Use the task text for the learner’s own assessed answer; the alternate example explains the method without replacing their work.

On this slide
Assign whole equipment groups: E1–E4 to train, E5 to validation, E6 to test.

Return train, validation and test lists of record_id in input order.

Do not use target values to choose membership.

Continue to
predict_regression(training_records, feature_records)

## Slide 31 — predict_regression(training_records, feature_records)

predict_regression(training_records, feature_records)
CML3111, Week 10, slide 31

Explanation to give
Build feature rows using only the specified input fields and preserve their order. Fit preprocessing and the three requested models using training records only.

Worked illustration / lecturer answer
The returned dictionary contains baseline, linear and tree, each with one prediction per feature record. A feature record deliberately contains no target answer.

Misconception to address
Keep the exact output names and required types. Use the task text for the learner’s own assessed answer; the alternate example explains the method without replacing their work.

On this slide
Fit a training-mean baseline, linear regression and a decision tree (max_depth=4, random_state=17) using load_pct and ambient_c only.

Return three prediction lists under baseline, linear and tree.

Feature records have no target.

Fit preprocessing only on training data.

Continue to
Written evidence

## Slide 32 — Written evidence

Written evidence
CML3111, Week 10, slide 32

Explanation to give
Show the actual markdown answer cell headed My written evidence. This is where the learner explains the choices and the supplied scenario in their own words.

Worked illustration / lecturer answer
A useful explanation connects a decision to a named result and its limitation: for example, why a training-only median avoids using evaluation information. Describe supplied scenario figures as supplied, not as measurements the learner produced.

Misconception to address
Prompts and copied code comments do not substitute for the learner’s reasoning. Weekly work and tests use the notebook; projects also require their separate readable report.

On this slide
Use the cell headed “My written evidence”.

Explain the supplied scenario in your own words.

State target units, reasons and limitations.

Submit one complete notebook containing code and written evidence.

Continue to
Validation and trust submission

## Slide 33 — Validation and trust submission

Validation and trust submission
CML3111, Week 10, slide 33

Explanation to give
This slide hands over CML3111 W10. Show the exact form title before uploading. The required packet is one completed .ipynb notebook.

Worked illustration / lecturer answer
The recorded cutoff for this form is 2026-11-20T11:00:00+03:00. Check the live form for later changes. A replacement must contain the complete required file set, not just the changed file.

Misconception to address
Students enter their own Student Registration Number as required freeform text. They wait for filenames to appear, press Submit and keep the confirmation. A file saved in Drive or GitHub is not itself a form submission.

On this slide
Opens: 13 Nov 2026, 11:00 Kampala

Deadline: 20 Nov 2026, 11:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

Continue to
Week 10 quiz

## Slide 34 — Week 10 quiz

Week 10 quiz
CML3111, Week 10, slide 34

Explanation to give
This is the CML3111 Week 1 quiz. The student link opens the response form; it does not activate its window. In Quiz Controls use open_W1_CML3111 when ready and read the logged closing time.

Worked illustration / lecturer answer
Explain the distinction between the expected answering time and availability: five minutes of questions can still be available for 24 hours after activation. Enter the learner’s own Student Registration Number and use the registered Google account.

Misconception to address
Read the exact live cutoff before announcing it. Do not promise a new attempt to somebody who already submitted. Quiz catch-up and assignment uploads are separate forms.

On this slide
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

Check the announced quiz closing time.

Continue to
Revision and submission checklist

## Slide 35 — Revision and submission checklist

Revision and submission checklist
CML3111, Week 10, slide 35

Explanation to give
Connect evaluation to intended use. Decide how to hold out observations before fitting either preprocessing or the model.

Worked illustration / lecturer answer
When testing new equipment, all observations from equipment A stay in one partition. Training must not learn its missing-value replacements from held-out equipment.

Misconception to address
Close by identifying the actual saved file and its correct submission route. Read the live deadline. For current weekly notebook tasks, students upload their own work, not the practice notebook, ZIP or grading files.

On this slide
You can identify which records may influence preprocessing and model selection.

Save your work and check the required submission files.

Continue to
Optional revision video

## Slide 36 — Optional revision video

Optional revision video
CML3111, Week 10, slide 36

Explanation to give
Give the viewing question before playing the excerpt: Why evaluate using observations not used to fit that particular model?

Worked illustration / lecturer answer
Use the adjacent worked example as the explanation if the video cannot load. Pause after the relevant example and connect its terms to the names and units already used in this lesson. Preview the displayed link and excerpt before class.

Misconception to address
The video is supporting revision, not a replacement for defining the symbols or a requirement to watch a full tutorial during limited class time.

On this slide
For revision after class.

StatQuest with Josh Starmer
Machine Learning Fundamentals Cross Validation

Opening up to 04:00, optional preview-selected excerpt

Listening question: Why evaluate using observations not used to fit that particular model?

Reference / existing resource
https://www.youtube.com/watch?v=fSytzGwwBVw
