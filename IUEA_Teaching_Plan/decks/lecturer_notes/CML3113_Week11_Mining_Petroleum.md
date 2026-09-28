# CML3113 Week11 Mining Petroleum

Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.

## Slide 1 — Creating and testing a useful feature

TEACHING PURPOSE
Creating and testing a useful feature

LECTURER CUE
Use PowerPoint Presenter View for these notes. Teach one example, pause for every learner to predict, then work an analogous example together. The practice notebook is a learning aid, not an extra graded upload.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
Today’s learning. Move on after a learner can explain the current example or required action.

## Slide 2 — Today’s learning

TEACHING PURPOSE
Today’s learning

CONNECT
Build on the preceding slide: Creating and testing a useful feature.

LECTURER CUE
Ask learners to explain this goal in ordinary language. The first successful attempt matters more than covering optional extensions. Defer: Five independent features, a full ColumnTransformer construction and domain-code features are extension. Never invent engineering limits.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
Recall and a first attempt. Move on after a learner can explain the current example or required action.

## Slide 3 — Recall and a first attempt

TEACHING PURPOSE
Recall and a first attempt

CONNECT
Build on the preceding slide: Today’s learning.

LECTURER CUE
Allow two minutes for everyone to try. Ask pairs to compare. If many cannot begin, show the first step and repeat with changed values. Checkpoint for today: Students explain why the largest-looking feature or the most complex model need not improve predictions.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

NEXT
The engineering context. Move on after a learner can explain the current example or required action.

## Slide 4 — The engineering context

TEACHING PURPOSE
The engineering context

CONNECT
Build on the preceding slide: Recall and a first attempt.

LECTURER CUE
A pump team records temperature to investigate operation. Mining students can relate this to a dewatering pump; petroleum students to a transfer pump. These are teaching examples, not operating limits.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
A feature has a meaning. Move on after a learner can explain the current example or required action.

## Slide 5 — A feature has a meaning

TEACHING PURPOSE
A feature has a meaning

CONNECT
Build on the preceding slide: The engineering context.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
Words we will use. Move on after a learner can explain the current example or required action.

## Slide 6 — Words we will use

TEACHING PURPOSE
Words we will use

CONNECT
Build on the preceding slide: A feature has a meaning.

EXPLAIN IN ORDINARY WORDS
A feature is information supplied to a model. An interaction combines inputs, for example area times thickness gives volume. Ablation compares a model with and without a feature using the same evaluation protocol.

CHECK AND EXPECTED ANSWER
Does a lower validation error prove the feature is physically causal? No. It supports prediction under this comparison, subject to leakage and data limitations.

IF LEARNERS ARE STUCK
State when each input becomes available, write its unit, then compare the same rows and metric.

POINT TO THE DEFINITION
Derived feature: A new input calculated from existing inputs. Its definition and unit must be stated.
Ratio and interaction: A ratio divides quantities; an interaction multiplies them. Both need a domain explanation and a unit check.

NEXT
Read the physical example across programmes. Move on after a learner can explain the current example or required action.

## Slide 7 — Read the physical example across programmes

TEACHING PURPOSE
Read the physical example across programmes

CONNECT
Build on the preceding slide: Words we will use.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
A physical relationship can form a feature. Move on after a learner can explain the current example or required action.

## Slide 8 — A physical relationship can form a feature

TEACHING PURPOSE
A physical relationship can form a feature

CONNECT
Build on the preceding slide: Read the physical example across programmes.

LECTURER CUE
Ask students to describe what they see before introducing terminology. Generated conceptual teaching illustration.  Source: figs/experiential/ASSET_SOURCES.md.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
An interaction uses two known inputs. Move on after a learner can explain the current example or required action.

## Slide 9 — An interaction uses two known inputs

TEACHING PURPOSE
An interaction uses two known inputs

CONNECT
Build on the preceding slide: A physical relationship can form a feature.

LECTURER CUE
A derived input must be available when predicting. A useful physical relationship still needs validation.

EXPLAIN IN ORDINARY WORDS
A feature is information supplied to a model. An interaction combines inputs, for example area times thickness gives volume. Ablation compares a model with and without a feature using the same evaluation protocol.

CHECK AND EXPECTED ANSWER
Does a lower validation error prove the feature is physically causal? No. It supports prediction under this comparison, subject to leakage and data limitations.

IF LEARNERS ARE STUCK
State when each input becomes available, write its unit, then compare the same rows and metric.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
A percentage and its fraction. Move on after a learner can explain the current example or required action.

## Slide 10 — A percentage and its fraction

TEACHING PURPOSE
A percentage and its fraction

CONNECT
Build on the preceding slide: An interaction uses two known inputs.

LECTURER CUE
Begin with a percentage: 40% means 40 / 100 = 0.4. Converting percentage to fraction changes units but adds no new information.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
A combined input needs a reason. Move on after a learner can explain the current example or required action.

## Slide 11 — A combined input needs a reason

TEACHING PURPOSE
A combined input needs a reason

CONNECT
Build on the preceding slide: A percentage and its fraction.

LECTURER CUE
An interaction may help a simple model express a relationship, but usefulness is tested rather than assumed. An interaction involving Celsius is an empirical feature, not automatically a physical law.

EXPLAIN IN ORDINARY WORDS
A feature is information supplied to a model. An interaction combines inputs, for example area times thickness gives volume. Ablation compares a model with and without a feature using the same evaluation protocol.

CHECK AND EXPECTED ANSWER
Does a lower validation error prove the feature is physically causal? No. It supports prediction under this comparison, subject to leakage and data limitations.

IF LEARNERS ARE STUCK
State when each input becomes available, write its unit, then compare the same rows and metric.

NEXT
Words we will use. Move on after a learner can explain the current example or required action.

## Slide 12 — Words we will use

TEACHING PURPOSE
Words we will use

CONNECT
Build on the preceding slide: A combined input needs a reason.

EXPLAIN IN ORDINARY WORDS
A feature is information supplied to a model. An interaction combines inputs, for example area times thickness gives volume. Ablation compares a model with and without a feature using the same evaluation protocol.

CHECK AND EXPECTED ANSWER
Does a lower validation error prove the feature is physically causal? No. It supports prediction under this comparison, subject to leakage and data limitations.

IF LEARNERS ARE STUCK
State when each input becomes available, write its unit, then compare the same rows and metric.

POINT TO THE DEFINITION
Ablation: Compare a model with and without a feature while keeping the data partitions, model family and metric fixed.
Improvement: For an error metric, baseline error minus new error. A negative result means the added feature worsened validation error in that comparison.

NEXT
One change makes a comparison interpretable. Move on after a learner can explain the current example or required action.

## Slide 13 — One change makes a comparison interpretable

TEACHING PURPOSE
One change makes a comparison interpretable

CONNECT
Build on the preceding slide: Words we will use.

LECTURER CUE
Read a two-row results table: base MAE 3, extended MAE 2.5 gives improvement 0.5 target units. Ask which other experimental choices must stay fixed.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

NEXT
Worked example. Move on after a learner can explain the current example or required action.

## Slide 14 — Worked example

TEACHING PURPOSE
Worked example

CONNECT
Build on the preceding slide: One change makes a comparison interpretable.

LECTURER CUE
Begin with a percentage: 40% means 40 / 100 = 0.4. Converting percentage to fraction changes units but adds no new information. An interaction may help a simple model express a relationship, but usefulness is tested rather than assumed. An interaction involving Celsius is an empirical feature, not automatically a physical law. Read a two-row results table: base MAE 3, extended MAE 2.5 gives improvement 0.5 target units. Ask which other experimental choices must stay fixed.

Complete practice code:
load_pct = 40
ambient_c = 25
load_fraction = load_pct / 100
interaction = load_pct * ambient_c
print(load_fraction, interaction)
base_mae = 3.0
extended_mae = 2.5
print(base_mae - extended_mae)

EXPLAIN IN ORDINARY WORDS
An error compares prediction with measured truth. Absolute error ignores direction. MAE averages absolute errors; RMSE squares, averages, then takes a square root. Both use the target unit.

CHECK AND EXPECTED ANSWER
Actual [4,8], predicted [5,6]: prediction-minus-actual errors [1,-2], MAE=1.5, RMSE=sqrt(2.5), about 1.58.

IF LEARNERS ARE STUCK
Calculate one pair by hand first. For signed percentage error follow the precise sign convention in the issued task.

WALK THROUGH THIS CODE
print displays a value below the cell.
= assigns the value on the right to the name on the left.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Expected output. Move on after a learner can explain the current example or required action.

## Slide 15 — Expected output

TEACHING PURPOSE
Expected output

CONNECT
Build on the preceding slide: Worked example.

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

NEXT
Read the two-model experiment. Move on after a learner can explain the current example or required action.

## Slide 16 — Read the two-model experiment

TEACHING PURPOSE
Read the two-model experiment

CONNECT
Build on the preceding slide: Expected output.

EXPLAIN IN ORDINARY WORDS
A feature is information supplied to a model. An interaction combines inputs, for example area times thickness gives volume. Ablation compares a model with and without a feature using the same evaluation protocol.

CHECK AND EXPECTED ANSWER
Does a lower validation error prove the feature is physically causal? No. It supports prediction under this comparison, subject to leakage and data limitations.

IF LEARNERS ARE STUCK
State when each input becomes available, write its unit, then compare the same rows and metric.

NEXT
Two models under one protocol. Move on after a learner can explain the current example or required action.

## Slide 17 — Two models under one protocol

TEACHING PURPOSE
Two models under one protocol

CONNECT
Build on the preceding slide: Read the two-model experiment.

LECTURER CUE
Run this complete practice experiment in a fresh session. Both models use the same rows and targets; the second receives one additional input. Read every column before fitting. This invented experiment illustrates procedure, not a measured engineering benefit.

EXPLAIN IN ORDINARY WORDS
A calculated column stores a result for each row at refresh. A measure is evaluated under the filters of the current visual. SUMX evaluates an expression for each row before adding it.

CHECK AND EXPECTED ANSWER
Should revenue respond to a selected region? Yes; test the measure with that filter and reconcile it to known data.

IF LEARNERS ARE STUCK
Work one order line by hand, then two lines. Name the numerator and denominator populations before an average-order-value measure.

NEXT
Two models under one protocol in Python (1/3). Move on after a learner can explain the current example or required action.

## Slide 18 — Two models under one protocol in Python (1/3)

TEACHING PURPOSE
Two models under one protocol in Python (1/3)

CONNECT
Build on the preceding slide: Two models under one protocol.

LECTURER CUE
Run this complete practice experiment in a fresh session. Both models use the same rows and targets; the second receives one additional input. Read every column before fitting. This invented experiment illustrates procedure, not a measured engineering benefit.

Complete practice code:
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
train = [[1, 2], [2, 3], [3, 2], [4, 4], [5, 3]]
y = [3, 5, 5, 8, 8]
validation = [[2, 2], [3, 3]]
truth = [4, 6]
def with_interaction(rows):
    result = []
    for a, b in rows:
        result.append([a, b, a * b])
    return result
base = LinearRegression().fit(train, y)
extended = LinearRegression().fit(with_interaction(train), y)
base_predictions = base.predict(validation)
base_error = mean_absolute_error(truth, base_predictions)
print(round(base_error, 6))
validation_features = with_interaction(validation)
extended_predictions = extended.predict(validation_features)
error = mean_absolute_error(truth, extended_predictions)
print(round(error, 6))

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

WALK THROUGH THIS CODE
import loads a library. from selects a tool from it.
Square brackets create a list or select an item.
= assigns the value on the right to the name on the left.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Two models under one protocol in Python (2/3). Move on after a learner can explain the current example or required action.

## Slide 19 — Two models under one protocol in Python (2/3)

TEACHING PURPOSE
Two models under one protocol in Python (2/3)

CONNECT
Build on the preceding slide: Two models under one protocol in Python (1/3).

LECTURER CUE
Run this complete practice experiment in a fresh session. Both models use the same rows and targets; the second receives one additional input. Read every column before fitting. This invented experiment illustrates procedure, not a measured engineering benefit.

Complete practice code:
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
train = [[1, 2], [2, 3], [3, 2], [4, 4], [5, 3]]
y = [3, 5, 5, 8, 8]
validation = [[2, 2], [3, 3]]
truth = [4, 6]
def with_interaction(rows):
    result = []
    for a, b in rows:
        result.append([a, b, a * b])
    return result
base = LinearRegression().fit(train, y)
extended = LinearRegression().fit(with_interaction(train), y)
base_predictions = base.predict(validation)
base_error = mean_absolute_error(truth, base_predictions)
print(round(base_error, 6))
validation_features = with_interaction(validation)
extended_predictions = extended.predict(validation_features)
error = mean_absolute_error(truth, extended_predictions)
print(round(error, 6))

EXPLAIN IN ORDINARY WORDS
A feature is information supplied to a model. An interaction combines inputs, for example area times thickness gives volume. Ablation compares a model with and without a feature using the same evaluation protocol.

CHECK AND EXPECTED ANSWER
Does a lower validation error prove the feature is physically causal? No. It supports prediction under this comparison, subject to leakage and data limitations.

IF LEARNERS ARE STUCK
State when each input becomes available, write its unit, then compare the same rows and metric.

WALK THROUGH THIS CODE
def names the function. Inputs go inside parentheses.
for takes the next item. The indented block repeats.
return sends the result back to the caller.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Two models under one protocol in Python (3/3). Move on after a learner can explain the current example or required action.

## Slide 20 — Two models under one protocol in Python (3/3)

TEACHING PURPOSE
Two models under one protocol in Python (3/3)

CONNECT
Build on the preceding slide: Two models under one protocol in Python (2/3).

LECTURER CUE
Run this complete practice experiment in a fresh session. Both models use the same rows and targets; the second receives one additional input. Read every column before fitting. This invented experiment illustrates procedure, not a measured engineering benefit.

Complete practice code:
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
train = [[1, 2], [2, 3], [3, 2], [4, 4], [5, 3]]
y = [3, 5, 5, 8, 8]
validation = [[2, 2], [3, 3]]
truth = [4, 6]
def with_interaction(rows):
    result = []
    for a, b in rows:
        result.append([a, b, a * b])
    return result
base = LinearRegression().fit(train, y)
extended = LinearRegression().fit(with_interaction(train), y)
base_predictions = base.predict(validation)
base_error = mean_absolute_error(truth, base_predictions)
print(round(base_error, 6))
validation_features = with_interaction(validation)
extended_predictions = extended.predict(validation_features)
error = mean_absolute_error(truth, extended_predictions)
print(round(error, 6))

EXPLAIN IN ORDINARY WORDS
A feature is information supplied to a model. An interaction combines inputs, for example area times thickness gives volume. Ablation compares a model with and without a feature using the same evaluation protocol.

CHECK AND EXPECTED ANSWER
Does a lower validation error prove the feature is physically causal? No. It supports prediction under this comparison, subject to leakage and data limitations.

IF LEARNERS ARE STUCK
State when each input becomes available, write its unit, then compare the same rows and metric.

WALK THROUGH THIS CODE
predict applies the fitted model to new inputs.
print displays a value below the cell.
= assigns the value on the right to the name on the left.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Words we will use. Move on after a learner can explain the current example or required action.

## Slide 21 — Words we will use

TEACHING PURPOSE
Words we will use

CONNECT
Build on the preceding slide: Two models under one protocol in Python (3/3).

EXPLAIN IN ORDINARY WORDS
A category is a label, not an amount. Indicator columns record whether a row belongs to each category, usually with 0 or 1. Fit the encoding on training data and reuse it.

CHECK AND EXPECTED ANSWER
Does assigning red=1 and blue=2 mean blue is twice red? No, those are labels.

IF LEARNERS ARE STUCK
Make two rows and two category columns by hand before showing the encoder.

POINT TO THE DEFINITION
Encoding: Representing a category numerically. One-hot uses separate indicator columns. Arbitrary integer labels can falsely suggest an order.
Scaling: Changing the numerical scale of features. Fit learned scaling on training data only. It matters for distance-based models but is not required by ordinary decision trees.

NEXT
You are the feature reviewer. Move on after a learner can explain the current example or required action.

## Slide 22 — You are the feature reviewer

TEACHING PURPOSE
You are the feature reviewer

CONNECT
Build on the preceding slide: Words we will use.

LECTURER CUE
Do this before revealing the discussion slide. One learner moves or writes the items, the other checks. Swap roles. Every student explains one step. Expected: Improvement changes from +0.5 to -0.4. The second comparison does not support retaining the feature.
Wait for an individual prediction before inviting pair discussion. Give a first-step hint if needed.

EXPLAIN IN ORDINARY WORDS
A feature is information supplied to a model. An interaction combines inputs, for example area times thickness gives volume. Ablation compares a model with and without a feature using the same evaluation protocol.

CHECK AND EXPECTED ANSWER
Does a lower validation error prove the feature is physically causal? No. It supports prediction under this comparison, subject to leakage and data limitations.

IF LEARNERS ARE STUCK
State when each input becomes available, write its unit, then compare the same rows and metric.

NEXT
What the activity shows. Move on after a learner can explain the current example or required action.

## Slide 23 — What the activity shows

TEACHING PURPOSE
What the activity shows

CONNECT
Build on the preceding slide: You are the feature reviewer.

LECTURER CUE
Ask which step produced this answer. Return to the concrete action if a learner cannot explain it. This is practice feedback, never a quiz key.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

NEXT
Your turn. Move on after a learner can explain the current example or required action.

## Slide 24 — Your turn

TEACHING PURPOSE
Your turn

CONNECT
Build on the preceding slide: What the activity shows.

LECTURER CUE
Give silent thinking time, then let pairs discuss. Rotate who types. This is practice, not a graded quiz. Expected response: Improvement is -0.4. This validation comparison does not support retaining it. One split is limited evidence; the final test remains untouched.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

DISCUSSION KEY FOR THIS SLIDE
DISCUSS THE REASONING
Practice discussion
Improvement is -0.4. This validation comparison does not support retaining it. One split is limited evidence; the final test remains untouched.
Which step produced this result? What changes if one input changes?
CML3113   Week 11   25
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
Practice discussion. Move on after a learner can explain the current example or required action.

## Slide 25 — Practice discussion

TEACHING PURPOSE
Practice discussion

CONNECT
Build on the preceding slide: Your turn.

LECTURER CUE
Ask how the result was obtained. Reteach the smallest missing step instead of giving a longer lecture.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

NEXT
Preparing for the assignment. Move on after a learner can explain the current example or required action.

## Slide 26 — Preparing for the assignment

TEACHING PURPOSE
Preparing for the assignment

CONNECT
Build on the preceding slide: Practice discussion.

LECTURER CUE
W11 names four output features and a two-model ablation. Explain output order, preservation of input rows, full precision and training-only fitting. Use the supplied written scenario for the interpretation requested there. Do not substitute this practice example’s result.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Features without misleading evaluation. Move on after a learner can explain the current example or required action.

## Slide 27 — Features without misleading evaluation

TEACHING PURPOSE
Features without misleading evaluation

CONNECT
Build on the preceding slide: Preparing for the assignment.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
Features without misleading evaluation continued. Move on after a learner can explain the current example or required action.

## Slide 28 — Features without misleading evaluation continued

TEACHING PURPOSE
Features without misleading evaluation continued

CONNECT
Build on the preceding slide: Features without misleading evaluation.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
Your issued task. Move on after a learner can explain the current example or required action.

## Slide 29 — Your issued task

TEACHING PURPOSE
Your issued task

CONNECT
Build on the preceding slide: Features without misleading evaluation continued.

LECTURER CUE
Investigate crusher energy demand. Target units: kWh/t. These are synthetic teaching records, not measurements suitable for deployment. Each record is one operating observation; equipment_id repeats across observations.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
make_features(feature_records). Move on after a learner can explain the current example or required action.

## Slide 30 — make_features(feature_records)

TEACHING PURPOSE
make_features(feature_records)

CONNECT
Build on the preceding slide: Your issued task.

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W11/CML3113/A/TASKS.md

EXPLAIN IN ORDINARY WORDS
A feature is information supplied to a model. An interaction combines inputs, for example area times thickness gives volume. Ablation compares a model with and without a feature using the same evaluation protocol.

CHECK AND EXPECTED ANSWER
Does a lower validation error prove the feature is physically causal? No. It supports prediction under this comparison, subject to leakage and data limitations.

IF LEARNERS ARE STUCK
State when each input becomes available, write its unit, then compare the same rows and metric.

NEXT
ablation_metrics(training_records, validation_records). Move on after a learner can explain the current example or required action.

## Slide 31 — ablation_metrics(training_records, validation_records)

TEACHING PURPOSE
ablation_metrics(training_records, validation_records)

CONNECT
Build on the preceding slide: make_features(feature_records).

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W11/CML3113/A/TASKS.md

EXPLAIN IN ORDINARY WORDS
A feature is information supplied to a model. An interaction combines inputs, for example area times thickness gives volume. Ablation compares a model with and without a feature using the same evaluation protocol.

CHECK AND EXPECTED ANSWER
Does a lower validation error prove the feature is physically causal? No. It supports prediction under this comparison, subject to leakage and data limitations.

IF LEARNERS ARE STUCK
State when each input becomes available, write its unit, then compare the same rows and metric.

NEXT
Written evidence. Move on after a learner can explain the current example or required action.

## Slide 32 — Written evidence

TEACHING PURPOSE
Written evidence

CONNECT
Build on the preceding slide: ablation_metrics(training_records, validation_records).

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
Features and ablation submission. Move on after a learner can explain the current example or required action.

## Slide 33 — Features and ablation submission

TEACHING PURPOSE
Features and ablation submission

CONNECT
Build on the preceding slide: Written evidence.

LECTURER CUE
The form link is cohort-specific. Recheck the live form and release status before class. These scheduled assignment dates are separate from the quiz activation window. The issued brief defines the required files, even if the form accepts additional formats. Source: data/submission_links.json

EXPLAIN IN ORDINARY WORDS
A feature is information supplied to a model. An interaction combines inputs, for example area times thickness gives volume. Ablation compares a model with and without a feature using the same evaluation protocol.

CHECK AND EXPECTED ANSWER
Does a lower validation error prove the feature is physically causal? No. It supports prediction under this comparison, subject to leakage and data limitations.

IF LEARNERS ARE STUCK
State when each input becomes available, write its unit, then compare the same rows and metric.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Project preparation. Move on after a learner can explain the current example or required action.

## Slide 34 — Project preparation

TEACHING PURPOSE
Project preparation

CONNECT
Build on the preceding slide: Features and ablation submission.

LECTURER CUE
Explain the released brief now. Confirm its grading-release checks before assigning it. Avoid treating weekly practice as a substitute for the project evidence. The project brief remains authoritative.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Week 11 quiz. Move on after a learner can explain the current example or required action.

## Slide 35 — Week 11 quiz

TEACHING PURPOSE
Week 11 quiz

CONNECT
Build on the preceding slide: Project preparation.

LECTURER CUE
Activate the matching open_W11_CML3113 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

QUIZ OPERATION
Opening the student link does not activate the quiz. In Quiz Controls run the matching open_W<week>_<cohort> function once when ready. Announce the logged closing time: 24 hours after activation. Five minutes describes expected answering time, not the availability window. Quiz 1 and Quiz 2 require separate activation when collecting catch-up work.

NEXT
Before you leave. Move on after a learner can explain the current example or required action.

## Slide 36 — Before you leave

TEACHING PURPOSE
Before you leave

CONNECT
Build on the preceding slide: Week 11 quiz.

LECTURER CUE
Ask every learner for an individual response. Record one misconception to revisit at the start of the next class. If a deadline changed, announce the exact Kampala date and update the source registry before rebuilding slides.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

