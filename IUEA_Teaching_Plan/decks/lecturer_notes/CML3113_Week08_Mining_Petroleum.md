# CML3113 Week08 Mining Petroleum

Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.

## Slide 1 — A first prediction model

TEACHING PURPOSE
A first prediction model

LECTURER CUE
Use PowerPoint Presenter View for these notes. Teach one example, pause for every learner to predict, then work an analogous example together. The practice notebook is a learning aid, not an extra graded upload.

NEXT
Today’s learning. Move on after a learner can explain the current example or required action.

## Slide 2 — Today’s learning

TEACHING PURPOSE
Today’s learning

CONNECT
Build on the preceding slide: A first prediction model.

LECTURER CUE
Ask learners to explain this goal in ordinary language. The first successful attempt matters more than covering optional extensions. Defer: Deriving least squares, leaderboard competition, many residual plots and coefficient inference are reference. R² may be negative and is not an accuracy percentage.

EXPLAIN IN ORDINARY WORDS
A calculated column stores a result for each row at refresh. A measure is evaluated under the filters of the current visual. SUMX evaluates an expression for each row before adding it.

CHECK AND EXPECTED ANSWER
Should revenue respond to a selected region? Yes; test the measure with that filter and reconcile it to known data.

IF LEARNERS ARE STUCK
Work one order line by hand, then two lines. Name the numerator and denominator populations before an average-order-value measure.

NEXT
Recall and a first attempt. Move on after a learner can explain the current example or required action.

## Slide 3 — Recall and a first attempt

TEACHING PURPOSE
Recall and a first attempt

CONNECT
Build on the preceding slide: Today’s learning.

LECTURER CUE
Allow two minutes for everyone to try. Ask pairs to compare. If many cannot begin, show the first step and repeat with changed values. Checkpoint for today: Students identify the target, explain why it is absent from prediction inputs and calculate one absolute error.

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
A numerical prediction. Move on after a learner can explain the current example or required action.

## Slide 5 — A numerical prediction

TEACHING PURPOSE
A numerical prediction

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
Build on the preceding slide: A numerical prediction.

EXPLAIN IN ORDINARY WORDS
Training fits rules. Validation helps choose among rules. The final test estimates performance after choices are fixed. Information that would be unavailable at the real prediction time must stay out of the inputs.

CHECK AND EXPECTED ANSWER
May two readings of the same machine appear on both sides when evaluating new machines? No; split by machine. For forecasting, train on the past and evaluate later time.

IF LEARNERS ARE STUCK
Use three envelopes. Keep the final-test envelope closed while selecting features or settings.

POINT TO THE DEFINITION
Feature and target: Features are inputs available when making a prediction. The target is the quantity we want to predict.
Training validation and test: Training fits the model. Validation helps choose it. The final test estimates performance after choices are fixed. Repeated equipment must stay in the same partition when assessing unseen equipment.

NEXT
Baseline. Move on after a learner can explain the current example or required action.

## Slide 7 — Baseline

TEACHING PURPOSE
Baseline

CONNECT
Build on the preceding slide: Words we will use.

EXPLAIN IN ORDINARY WORDS
A baseline is a deliberately simple reference. For numeric prediction, one example always predicts the training target mean. A more complicated model must earn its complexity by improving a fair comparison.

CHECK AND EXPECTED ANSWER
Why compute the constant from training targets? Evaluation answers must not influence a deployed prediction rule.

IF LEARNERS ARE STUCK
Use training targets 2,4,6: the mean baseline predicts 4 for every new row, whatever its inputs.

POINT TO THE DEFINITION
Baseline: A simple reference prediction. A training-mean baseline predicts the same training mean for every new example.

NEXT
Linear model and tree. Move on after a learner can explain the current example or required action.

## Slide 8 — Linear model and tree

TEACHING PURPOSE
Linear model and tree

CONNECT
Build on the preceding slide: Baseline.

EXPLAIN IN ORDINARY WORDS
Creating a model chooses the kind of rule. fit learns from training inputs and known answers. predict applies the fitted rule to new inputs without receiving their answers.

CHECK AND EXPECTED ANSWER
Does creating a model object train it? No. It must be fitted before prediction.

IF LEARNERS ARE STUCK
Point to inputs, training answers, fit, then new inputs. Keep each input row paired with its own target.

POINT TO THE DEFINITION
Linear model and tree: A linear model combines inputs with learned weights. A regression tree asks feature-threshold questions and predicts a value at each leaf.

NEXT
What learning means in this example. Move on after a learner can explain the current example or required action.

## Slide 9 — What learning means in this example

TEACHING PURPOSE
What learning means in this example

CONNECT
Build on the preceding slide: Linear model and tree.

LECTURER CUE
Use the small invented table below solely to see fit and predict. Real training needs more data, representative evaluation and careful partitioning.

NEXT
Training observations. Move on after a learner can explain the current example or required action.

## Slide 10 — Training observations

TEACHING PURPOSE
Training observations

CONNECT
Build on the preceding slide: What learning means in this example.

LECTURER CUE
Invented numbers for learning. The fitted line predicts 15 at input 2.5. The training mean is also 15 at this one example, so it cannot establish superiority.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
A fitted line is a numerical rule. Move on after a learner can explain the current example or required action.

## Slide 11 — A fitted line is a numerical rule

TEACHING PURPOSE
A fitted line is a numerical rule

CONNECT
Build on the preceding slide: Training observations.

EXPLAIN IN ORDINARY WORDS
Creating a model chooses the kind of rule. fit learns from training inputs and known answers. predict applies the fitted rule to new inputs without receiving their answers.

CHECK AND EXPECTED ANSWER
Does creating a model object train it? No. It must be fitted before prediction.

IF LEARNERS ARE STUCK
Point to inputs, training answers, fit, then new inputs. Keep each input row paired with its own target.

NEXT
Fitting a line to observations. Move on after a learner can explain the current example or required action.

## Slide 12 — Fitting a line to observations

TEACHING PURPOSE
Fitting a line to observations

CONNECT
Build on the preceding slide: A fitted line is a numerical rule.

LECTURER CUE
These are illustrative concrete observations. Point to x, y, one prediction and one residual. A unique slope requires variation in x. A low training error alone does not show generalisation.
Source: existing course illustration figs/fit_by_eye.png. These are illustrative examples, not this cohort’s assessed results.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
Rows must stay paired with their answers. Move on after a learner can explain the current example or required action.

## Slide 13 — Rows must stay paired with their answers

TEACHING PURPOSE
Rows must stay paired with their answers

CONNECT
Build on the preceding slide: Fitting a line to observations.

LECTURER CUE
A list of lists is a table: each inner list holds the features of one observation. y_train holds one target per training row in the same order. Never reorder one without the other.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

NEXT
Rows and arrays before model code. Move on after a learner can explain the current example or required action.

## Slide 14 — Rows and arrays before model code

TEACHING PURPOSE
Rows and arrays before model code

CONNECT
Build on the preceding slide: Rows must stay paired with their answers.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

POINT TO THE DEFINITION
Nested lists: [[1], [2], [3]] has three inner lists: three rows with one feature each. [12, 14, 16] has one target per row in the same order.
NumPy and array: NumPy is a numerical library; np is its short imported name. np.array(...) builds an array. shape reports its dimensions. np.nan represents a missing numerical value.

NEXT
Reading NumPy results. Move on after a learner can explain the current example or required action.

## Slide 15 — Reading NumPy results

TEACHING PURPOSE
Reading NumPy results

CONNECT
Build on the preceding slide: Rows and arrays before model code.

LECTURER CUE
Read one row at a time and use a changed value. This is a syntax reference for the worked examples.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
Rows, columns and named options. Move on after a learner can explain the current example or required action.

## Slide 16 — Rows, columns and named options

TEACHING PURPOSE
Rows, columns and named options

CONNECT
Build on the preceding slide: Reading NumPy results.

LECTURER CUE
Read each symbol before running. Ask everyone to predict. Expected output: (3, 1) then (3,). Explain nested brackets before model.fit(X, y). Keyword arguments such as random_state=42 name an option.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

WALK THROUGH THIS CODE
import loads a library. from selects a tool from it.
print displays a value below the cell.
Square brackets create a list or select an item.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
fit and predict. Move on after a learner can explain the current example or required action.

## Slide 17 — fit and predict

TEACHING PURPOSE
fit and predict

CONNECT
Build on the preceding slide: Rows, columns and named options.

EXPLAIN IN ORDINARY WORDS
Creating a model chooses the kind of rule. fit learns from training inputs and known answers. predict applies the fitted rule to new inputs without receiving their answers.

CHECK AND EXPECTED ANSWER
Does creating a model object train it? No. It must be fitted before prediction.

IF LEARNERS ARE STUCK
Point to inputs, training answers, fit, then new inputs. Keep each input row paired with its own target.

POINT TO THE DEFINITION
fit and predict: fit learns from training inputs and targets. predict uses the fitted rule on new inputs without receiving their true targets.

NEXT
A model object keeps learned information. Move on after a learner can explain the current example or required action.

## Slide 18 — A model object keeps learned information

TEACHING PURPOSE
A model object keeps learned information

CONNECT
Build on the preceding slide: fit and predict.

EXPLAIN IN ORDINARY WORDS
Creating a model chooses the kind of rule. fit learns from training inputs and known answers. predict applies the fitted rule to new inputs without receiving their answers.

CHECK AND EXPECTED ANSWER
Does creating a model object train it? No. It must be fitted before prediction.

IF LEARNERS ARE STUCK
Point to inputs, training answers, fit, then new inputs. Keep each input row paired with its own target.

POINT TO THE DEFINITION
Object and method: LinearRegression() creates a model object. A method is an operation on that object. model.fit(...) stores learned information; model.predict(...) uses it.
Options: An argument such as strategy="mean" names an option. A random seed fixes the starting state of random choices; it does not prove that a model is accurate.

NEXT
An object remembers its fitted state. Move on after a learner can explain the current example or required action.

## Slide 19 — An object remembers its fitted state

TEACHING PURPOSE
An object remembers its fitted state

CONNECT
Build on the preceding slide: A model object keeps learned information.

LECTURER CUE
Read one row at a time and use a changed value. This is a syntax reference for the worked examples.

EXPLAIN IN ORDINARY WORDS
Creating a model chooses the kind of rule. fit learns from training inputs and known answers. predict applies the fitted rule to new inputs without receiving their answers.

CHECK AND EXPECTED ANSWER
Does creating a model object train it? No. It must be fitted before prediction.

IF LEARNERS ARE STUCK
Point to inputs, training answers, fit, then new inputs. Keep each input row paired with its own target.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
Creating, fitting and predicting. Move on after a learner can explain the current example or required action.

## Slide 20 — Creating, fitting and predicting

TEACHING PURPOSE
Creating, fitting and predicting

CONNECT
Build on the preceding slide: An object remembers its fitted state.

LECTURER CUE
Read imports and model creation separately. The model line creates an unfitted object. fit learns; predict applies. Explain the shallow tree now because the W08 assignment asks for it, then revisit classification trees in Week 9.

EXPLAIN IN ORDINARY WORDS
Creating a model chooses the kind of rule. fit learns from training inputs and known answers. predict applies the fitted rule to new inputs without receiving their answers.

CHECK AND EXPECTED ANSWER
Does creating a model object train it? No. It must be fitted before prediction.

IF LEARNERS ARE STUCK
Point to inputs, training answers, fit, then new inputs. Keep each input row paired with its own target.

NEXT
Worked example. Move on after a learner can explain the current example or required action.

## Slide 21 — Worked example

TEACHING PURPOSE
Worked example

CONNECT
Build on the preceding slide: Creating, fitting and predicting.

LECTURER CUE
Use the small invented table below solely to see fit and predict. Real training needs more data, representative evaluation and careful partitioning. A list of lists is a table: each inner list holds the features of one observation. y_train holds one target per training row in the same order. Never reorder one without the other. Read imports and model creation separately. The model line creates an unfitted object. fit learns; predict applies. Explain the shallow tree now because the W08 assignment asks for it, then revisit classification trees in Week 9.

Complete practice code:
from sklearn.linear_model import LinearRegression
X_train = [[1], [2], [3], [4]]
y_train = [12, 14, 16, 18]
new_inputs = [[2.5]]

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
Worked example continued. Move on after a learner can explain the current example or required action.

## Slide 22 — Worked example continued

TEACHING PURPOSE
Worked example continued

CONNECT
Build on the preceding slide: Worked example.

LECTURER CUE
Use the small invented table below solely to see fit and predict. Real training needs more data, representative evaluation and careful partitioning. A list of lists is a table: each inner list holds the features of one observation. y_train holds one target per training row in the same order. Never reorder one without the other. Read imports and model creation separately. The model line creates an unfitted object. fit learns; predict applies. Explain the shallow tree now because the W08 assignment asks for it, then revisit classification trees in Week 9.

Complete practice code:
model = LinearRegression()
model.fit(X_train, y_train)

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

WALK THROUGH THIS CODE
fit learns using the supplied training observations.
= assigns the value on the right to the name on the left.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Worked example continued. Move on after a learner can explain the current example or required action.

## Slide 23 — Worked example continued

TEACHING PURPOSE
Worked example continued

CONNECT
Build on the preceding slide: Worked example continued.

LECTURER CUE
Use the small invented table below solely to see fit and predict. Real training needs more data, representative evaluation and careful partitioning. A list of lists is a table: each inner list holds the features of one observation. y_train holds one target per training row in the same order. Never reorder one without the other. Read imports and model creation separately. The model line creates an unfitted object. fit learns; predict applies. Explain the shallow tree now because the W08 assignment asks for it, then revisit classification trees in Week 9.

Complete practice code:
predictions = model.predict(new_inputs)
print(predictions.round(2).tolist())

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

WALK THROUGH THIS CODE
predict applies the fitted model to new inputs.
print displays a value below the cell.
= assigns the value on the right to the name on the left.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Expected output. Move on after a learner can explain the current example or required action.

## Slide 24 — Expected output

TEACHING PURPOSE
Expected output

CONNECT
Build on the preceding slide: Worked example continued.

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

NEXT
The mean baseline. Move on after a learner can explain the current example or required action.

## Slide 25 — The mean baseline

TEACHING PURPOSE
The mean baseline

CONNECT
Build on the preceding slide: Expected output.

LECTURER CUE
Use the same training data. This baseline learns their mean, 15, and predicts it for every input. It gives a simple comparison before claiming the line helps.

EXPLAIN IN ORDINARY WORDS
A baseline is a deliberately simple reference. For numeric prediction, one example always predicts the training target mean. A more complicated model must earn its complexity by improving a fair comparison.

CHECK AND EXPECTED ANSWER
Why compute the constant from training targets? Evaluation answers must not influence a deployed prediction rule.

IF LEARNERS ARE STUCK
Use training targets 2,4,6: the mean baseline predicts 4 for every new row, whatever its inputs.

NEXT
The mean baseline in Python. Move on after a learner can explain the current example or required action.

## Slide 26 — The mean baseline in Python

TEACHING PURPOSE
The mean baseline in Python

CONNECT
Build on the preceding slide: The mean baseline.

LECTURER CUE
Use the same training data. This baseline learns their mean, 15, and predicts it for every input. It gives a simple comparison before claiming the line helps.

Complete practice code:
from sklearn.dummy import DummyRegressor
baseline = DummyRegressor(strategy="mean")
baseline.fit(X_train, y_train)
print(baseline.predict(new_inputs).tolist())

EXPLAIN IN ORDINARY WORDS
A baseline is a deliberately simple reference. For numeric prediction, one example always predicts the training target mean. A more complicated model must earn its complexity by improving a fair comparison.

CHECK AND EXPECTED ANSWER
Why compute the constant from training targets? Evaluation answers must not influence a deployed prediction rule.

IF LEARNERS ARE STUCK
Use training targets 2,4,6: the mean baseline predicts 4 for every new row, whatever its inputs.

WALK THROUGH THIS CODE
import loads a library. from selects a tool from it.
fit learns using the supplied training observations.
predict applies the fitted model to new inputs.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
A small regression tree. Move on after a learner can explain the current example or required action.

## Slide 27 — A small regression tree

TEACHING PURPOSE
A small regression tree

CONNECT
Build on the preceding slide: The mean baseline in Python.

LECTURER CUE
A tree learns threshold questions from the training inputs. Each final group, or leaf, predicts a target value. This tree returns 14 for input 2.5 in this toy example. max_depth limits the number of successive decisions. random_state fixes the random seed.

EXPLAIN IN ORDINARY WORDS
Creating a model chooses the kind of rule. fit learns from training inputs and known answers. predict applies the fitted rule to new inputs without receiving their answers.

CHECK AND EXPECTED ANSWER
Does creating a model object train it? No. It must be fitted before prediction.

IF LEARNERS ARE STUCK
Point to inputs, training answers, fit, then new inputs. Keep each input row paired with its own target.

NEXT
A small regression tree in Python. Move on after a learner can explain the current example or required action.

## Slide 28 — A small regression tree in Python

TEACHING PURPOSE
A small regression tree in Python

CONNECT
Build on the preceding slide: A small regression tree.

LECTURER CUE
A tree learns threshold questions from the training inputs. Each final group, or leaf, predicts a target value. This tree returns 14 for input 2.5 in this toy example. max_depth limits the number of successive decisions. random_state fixes the random seed.

Complete practice code:
from sklearn.tree import DecisionTreeRegressor
tree = DecisionTreeRegressor(max_depth=4, random_state=17)
tree.fit(X_train, y_train)
print(tree.predict(new_inputs).tolist())

EXPLAIN IN ORDINARY WORDS
Creating a model chooses the kind of rule. fit learns from training inputs and known answers. predict applies the fitted rule to new inputs without receiving their answers.

CHECK AND EXPECTED ANSWER
Does creating a model object train it? No. It must be fitted before prediction.

IF LEARNERS ARE STUCK
Point to inputs, training answers, fit, then new inputs. Keep each input row paired with its own target.

WALK THROUGH THIS CODE
import loads a library. from selects a tool from it.
fit learns using the supplied training observations.
predict applies the fitted model to new inputs.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Reuse the same preparation on new inputs. Move on after a learner can explain the current example or required action.

## Slide 29 — Reuse the same preparation on new inputs

TEACHING PURPOSE
Reuse the same preparation on new inputs

CONNECT
Build on the preceding slide: A small regression tree in Python.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

POINT TO THE DEFINITION
Imputer: An imputer fills missing feature values using a stated rule. Fit learns the replacement from training observations only. Prediction reuses that stored replacement.
Pipeline: A pipeline connects preprocessing and a model. make_pipeline creates that connection. Its fit learns both stages on training data; predict applies them to new features.

NEXT
Preprocessing learned from training only. Move on after a learner can explain the current example or required action.

## Slide 30 — Preprocessing learned from training only

TEACHING PURPOSE
Preprocessing learned from training only

CONNECT
Build on the preceding slide: Reuse the same preparation on new inputs.

LECTURER CUE
SimpleImputer learns one median for each training column. make_pipeline connects this step to the model. fit learns both steps using only the training examples. predict reuses them on new inputs. No target is supplied to predict. The two inputs here are invented practice measurements.

EXPLAIN IN ORDINARY WORDS
Training fits rules. Validation helps choose among rules. The final test estimates performance after choices are fixed. Information that would be unavailable at the real prediction time must stay out of the inputs.

CHECK AND EXPECTED ANSWER
May two readings of the same machine appear on both sides when evaluating new machines? No; split by machine. For forecasting, train on the past and evaluate later time.

IF LEARNERS ARE STUCK
Use three envelopes. Keep the final-test envelope closed while selecting features or settings.

NEXT
Preprocessing learned from training only in Python (1/2). Move on after a learner can explain the current example or required action.

## Slide 31 — Preprocessing learned from training only in Python (1/2)

TEACHING PURPOSE
Preprocessing learned from training only in Python (1/2)

CONNECT
Build on the preceding slide: Preprocessing learned from training only.

LECTURER CUE
SimpleImputer learns one median for each training column. make_pipeline connects this step to the model. fit learns both steps using only the training examples. predict reuses them on new inputs. No target is supplied to predict. The two inputs here are invented practice measurements.

Complete practice code:
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
import numpy as np
train_inputs = [[1, 20], [2, 22], [3, np.nan], [4, 24]]
train_targets = [12, 14, 16, 18]
imputer = SimpleImputer(strategy="median")
model = LinearRegression()
pipeline = make_pipeline(imputer, model)
pipeline.fit(train_inputs, train_targets)
predictions = pipeline.predict([[2.5, np.nan]])
print(predictions.round(2).tolist())

EXPLAIN IN ORDINARY WORDS
Training fits rules. Validation helps choose among rules. The final test estimates performance after choices are fixed. Information that would be unavailable at the real prediction time must stay out of the inputs.

CHECK AND EXPECTED ANSWER
May two readings of the same machine appear on both sides when evaluating new machines? No; split by machine. For forecasting, train on the past and evaluate later time.

IF LEARNERS ARE STUCK
Use three envelopes. Keep the final-test envelope closed while selecting features or settings.

WALK THROUGH THIS CODE
import loads a library. from selects a tool from it.
fit learns using the supplied training observations.
Square brackets create a list or select an item.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Preprocessing learned from training only in Python (2/2). Move on after a learner can explain the current example or required action.

## Slide 32 — Preprocessing learned from training only in Python (2/2)

TEACHING PURPOSE
Preprocessing learned from training only in Python (2/2)

CONNECT
Build on the preceding slide: Preprocessing learned from training only in Python (1/2).

LECTURER CUE
SimpleImputer learns one median for each training column. make_pipeline connects this step to the model. fit learns both steps using only the training examples. predict reuses them on new inputs. No target is supplied to predict. The two inputs here are invented practice measurements.

Complete practice code:
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
import numpy as np
train_inputs = [[1, 20], [2, 22], [3, np.nan], [4, 24]]
train_targets = [12, 14, 16, 18]
imputer = SimpleImputer(strategy="median")
model = LinearRegression()
pipeline = make_pipeline(imputer, model)
pipeline.fit(train_inputs, train_targets)
predictions = pipeline.predict([[2.5, np.nan]])
print(predictions.round(2).tolist())

EXPLAIN IN ORDINARY WORDS
Training fits rules. Validation helps choose among rules. The final test estimates performance after choices are fixed. Information that would be unavailable at the real prediction time must stay out of the inputs.

CHECK AND EXPECTED ANSWER
May two readings of the same machine appear on both sides when evaluating new machines? No; split by machine. For forecasting, train on the past and evaluate later time.

IF LEARNERS ARE STUCK
Use three envelopes. Keep the final-test envelope closed while selecting features or settings.

WALK THROUGH THIS CODE
predict applies the fitted model to new inputs.
print displays a value below the cell.
Square brackets create a list or select an item.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Reading records into a feature table. Move on after a learner can explain the current example or required action.

## Slide 33 — Reading records into a feature table

TEACHING PURPOSE
Reading records into a feature table

CONNECT
Build on the preceding slide: Preprocessing learned from training only in Python (2/2).

LECTURER CUE
Each inner list is one row, in the same order as the input records. The target list uses that same row order. The feature table has no answer column.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
Reading records into a feature table in Python. Move on after a learner can explain the current example or required action.

## Slide 34 — Reading records into a feature table in Python

TEACHING PURPOSE
Reading records into a feature table in Python

CONNECT
Build on the preceding slide: Reading records into a feature table.

LECTURER CUE
Each inner list is one row, in the same order as the input records. The target list uses that same row order. The feature table has no answer column.

Complete practice code:
rows = [{"length": 2, "width": 3, "area": 6},
        {"length": 4, "width": 5, "area": 20}]
X = []
y = []
for row in rows:
    X.append([row["length"], row["width"]])
    y.append(row["area"])
print(X)
print(y)

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

WALK THROUGH THIS CODE
for takes the next item. The indented block repeats.
print displays a value below the cell.
append adds one item to the end of a list.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
MAE and RMSE. Move on after a learner can explain the current example or required action.

## Slide 35 — MAE and RMSE

TEACHING PURPOSE
MAE and RMSE

CONNECT
Build on the preceding slide: Reading records into a feature table in Python.

EXPLAIN IN ORDINARY WORDS
An error compares prediction with measured truth. Absolute error ignores direction. MAE averages absolute errors; RMSE squares, averages, then takes a square root. Both use the target unit.

CHECK AND EXPECTED ANSWER
Actual [4,8], predicted [5,6]: prediction-minus-actual errors [1,-2], MAE=1.5, RMSE=sqrt(2.5), about 1.58.

IF LEARNERS ARE STUCK
Calculate one pair by hand first. For signed percentage error follow the precise sign convention in the issued task.

POINT TO THE DEFINITION
MAE and RMSE: MAE averages absolute prediction errors. RMSE squares errors, averages them and takes the square root. Both use target units. RMSE is more sensitive to large errors.

NEXT
A prediction error in ordinary numbers. Move on after a learner can explain the current example or required action.

## Slide 36 — A prediction error in ordinary numbers

TEACHING PURPOSE
A prediction error in ordinary numbers

CONNECT
Build on the preceding slide: MAE and RMSE.

LECTURER CUE
MAE = (2 + 4) / 2 = 3, in the target’s unit. Compare a model against a training-only baseline.

EXPLAIN IN ORDINARY WORDS
Training fits rules. Validation helps choose among rules. The final test estimates performance after choices are fixed. Information that would be unavailable at the real prediction time must stay out of the inputs.

CHECK AND EXPECTED ANSWER
May two readings of the same machine appear on both sides when evaluating new machines? No; split by machine. For forecasting, train on the past and evaluate later time.

IF LEARNERS ARE STUCK
Use three envelopes. Keep the final-test envelope closed while selecting features or settings.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
The operations in the error calculation. Move on after a learner can explain the current example or required action.

## Slide 37 — The operations in the error calculation

TEACHING PURPOSE
The operations in the error calculation

CONNECT
Build on the preceding slide: A prediction error in ordinary numbers.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

POINT TO THE DEFINITION
zip and paired names: zip(actual, predicted) pairs values at matching positions. for truth, guess in ... assigns each pair to two names. Here both lists must have the same nonzero length.
Square and square root: difference ** 2 squares an error. sqrt reverses a square for nonnegative numbers: sqrt(9) is 3. from math import sqrt makes this tool available.

NEXT
Two error measures. Move on after a learner can explain the current example or required action.

## Slide 38 — Two error measures

TEACHING PURPOSE
Two error measures

CONNECT
Build on the preceding slide: The operations in the error calculation.

LECTURER CUE
zip pairs corresponding values. abs measures error size. Squaring emphasises large errors; taking the square root returns to the original unit. These functions assume equal-length, nonempty paired observations.

EXPLAIN IN ORDINARY WORDS
An error compares prediction with measured truth. Absolute error ignores direction. MAE averages absolute errors; RMSE squares, averages, then takes a square root. Both use the target unit.

CHECK AND EXPECTED ANSWER
Actual [4,8], predicted [5,6]: prediction-minus-actual errors [1,-2], MAE=1.5, RMSE=sqrt(2.5), about 1.58.

IF LEARNERS ARE STUCK
Calculate one pair by hand first. For signed percentage error follow the precise sign convention in the issued task.

NEXT
Two error measures in Python (1/2). Move on after a learner can explain the current example or required action.

## Slide 39 — Two error measures in Python (1/2)

TEACHING PURPOSE
Two error measures in Python (1/2)

CONNECT
Build on the preceding slide: Two error measures.

LECTURER CUE
zip pairs corresponding values. abs measures error size. Squaring emphasises large errors; taking the square root returns to the original unit. These functions assume equal-length, nonempty paired observations.

Complete practice code:
from math import sqrt
a = [10, 20]
p = [12, 16]
absolute = []
squared = []
for truth, guess in zip(a, p):
    difference = truth - guess
    absolute.append(abs(difference))
    squared.append(difference ** 2)
print(sum(absolute) / len(a))
print(sqrt(sum(squared) / len(a)))

EXPLAIN IN ORDINARY WORDS
An error compares prediction with measured truth. Absolute error ignores direction. MAE averages absolute errors; RMSE squares, averages, then takes a square root. Both use the target unit.

CHECK AND EXPECTED ANSWER
Actual [4,8], predicted [5,6]: prediction-minus-actual errors [1,-2], MAE=1.5, RMSE=sqrt(2.5), about 1.58.

IF LEARNERS ARE STUCK
Calculate one pair by hand first. For signed percentage error follow the precise sign convention in the issued task.

WALK THROUGH THIS CODE
import loads a library. from selects a tool from it.
for takes the next item. The indented block repeats.
zip pairs items at matching positions in these equal-length lists.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Two error measures in Python (2/2). Move on after a learner can explain the current example or required action.

## Slide 40 — Two error measures in Python (2/2)

TEACHING PURPOSE
Two error measures in Python (2/2)

CONNECT
Build on the preceding slide: Two error measures in Python (1/2).

LECTURER CUE
zip pairs corresponding values. abs measures error size. Squaring emphasises large errors; taking the square root returns to the original unit. These functions assume equal-length, nonempty paired observations.

Complete practice code:
from math import sqrt
a = [10, 20]
p = [12, 16]
absolute = []
squared = []
for truth, guess in zip(a, p):
    difference = truth - guess
    absolute.append(abs(difference))
    squared.append(difference ** 2)
print(sum(absolute) / len(a))
print(sqrt(sum(squared) / len(a)))

EXPLAIN IN ORDINARY WORDS
An error compares prediction with measured truth. Absolute error ignores direction. MAE averages absolute errors; RMSE squares, averages, then takes a square root. Both use the target unit.

CHECK AND EXPECTED ANSWER
Actual [4,8], predicted [5,6]: prediction-minus-actual errors [1,-2], MAE=1.5, RMSE=sqrt(2.5), about 1.58.

IF LEARNERS ARE STUCK
Calculate one pair by hand first. For signed percentage error follow the precise sign convention in the issued task.

WALK THROUGH THIS CODE
print displays a value below the cell.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
R² compares against a mean prediction. Move on after a learner can explain the current example or required action.

## Slide 41 — R² compares against a mean prediction

TEACHING PURPOSE
R² compares against a mean prediction

CONNECT
Build on the preceding slide: Two error measures in Python (2/2).

EXPLAIN IN ORDINARY WORDS
R-squared compares squared prediction errors with using the evaluation targets’ mean. One is perfect; zero matches that reference. A negative value is possible.

CHECK AND EXPECTED ANSWER
Does R-squared=0.8 mean 80% of predictions are correct? No; it concerns variation and squared errors, not a count of correct answers.

IF LEARNERS ARE STUCK
Compare errors against a mean predictor on the same evaluation rows. MAE remains useful for a result in physical units.

NEXT
You are a prediction rule. Move on after a learner can explain the current example or required action.

## Slide 42 — You are a prediction rule

TEACHING PURPOSE
You are a prediction rule

CONNECT
Build on the preceding slide: R² compares against a mean prediction.

LECTURER CUE
Do this before revealing the discussion slide. One learner moves or writes the items, the other checks. Swap roles. Every student explains one step. Expected: Prediction is 16. The absolute error is 2 target units. A single result does not show that the model is useful in general.
Wait for an individual prediction before inviting pair discussion. Give a first-step hint if needed.

NEXT
What the activity shows. Move on after a learner can explain the current example or required action.

## Slide 43 — What the activity shows

TEACHING PURPOSE
What the activity shows

CONNECT
Build on the preceding slide: You are a prediction rule.

LECTURER CUE
Ask which step produced this answer. Return to the concrete action if a learner cannot explain it. This is practice feedback, never a quiz key.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

NEXT
Your turn. Move on after a learner can explain the current example or required action.

## Slide 44 — Your turn

TEACHING PURPOSE
Your turn

CONNECT
Build on the preceding slide: What the activity shows.

LECTURER CUE
Give silent thinking time, then let pairs discuss. Rotate who types. This is practice, not a graded quiz. Expected response: Absolute errors are 2 and 4: MAE 3. Squared errors 4 and 16: RMSE sqrt(10), about 3.162. MAE is an average, not an individual error bound.

EXPLAIN IN ORDINARY WORDS
An error compares prediction with measured truth. Absolute error ignores direction. MAE averages absolute errors; RMSE squares, averages, then takes a square root. Both use the target unit.

CHECK AND EXPECTED ANSWER
Actual [4,8], predicted [5,6]: prediction-minus-actual errors [1,-2], MAE=1.5, RMSE=sqrt(2.5), about 1.58.

IF LEARNERS ARE STUCK
Calculate one pair by hand first. For signed percentage error follow the precise sign convention in the issued task.

DISCUSSION KEY FOR THIS SLIDE
DISCUSS THE REASONING
Practice discussion
Absolute errors are 2 and 4: MAE 3. Squared errors 4 and 16: RMSE sqrt(10), about 3.162. MAE is an average, not an individual error bound.
Which step produced this result? What changes if one input changes?
CML3113   Week 8   45
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
Practice discussion. Move on after a learner can explain the current example or required action.

## Slide 45 — Practice discussion

TEACHING PURPOSE
Practice discussion

CONNECT
Build on the preceding slide: Your turn.

LECTURER CUE
Ask how the result was obtained. Reteach the smallest missing step instead of giving a longer lecture.

EXPLAIN IN ORDINARY WORDS
An error compares prediction with measured truth. Absolute error ignores direction. MAE averages absolute errors; RMSE squares, averages, then takes a square root. Both use the target unit.

CHECK AND EXPECTED ANSWER
Actual [4,8], predicted [5,6]: prediction-minus-actual errors [1,-2], MAE=1.5, RMSE=sqrt(2.5), about 1.58.

IF LEARNERS ARE STUCK
Calculate one pair by hand first. For signed percentage error follow the precise sign convention in the issued task.

NEXT
Short explainer and discussion. Move on after a learner can explain the current example or required action.

## Slide 46 — Short explainer and discussion

TEACHING PURPOSE
Short explainer and discussion

CONNECT
Build on the preceding slide: Practice discussion.

LECTURER CUE
Linked by the official StatQuest video index. Full audiovisual preview and excerpt timing still required.
After viewing: Draw an actual value and a prediction, then identify their difference.
Preview before class and stop after the selected short excerpt. If playback fails, teach the worked example. Video is optional. Source: https://www.youtube.com/watch?v=aFDOzpTeg0s

EXPLAIN IN ORDINARY WORDS
Creating a model chooses the kind of rule. fit learns from training inputs and known answers. predict applies the fitted rule to new inputs without receiving their answers.

CHECK AND EXPECTED ANSWER
Does creating a model object train it? No. It must be fitted before prediction.

IF LEARNERS ARE STUCK
Point to inputs, training answers, fit, then new inputs. Keep each input row paired with its own target.

VIDEO ROUTINE
Preview the exact link and stated excerpt before class. State the viewing question first, pause after the example, and ask a learner to explain it. If access fails, use the adjacent worked example and discussion rather than spend class time troubleshooting streaming.

NEXT
After the video. Move on after a learner can explain the current example or required action.

## Slide 47 — After the video

TEACHING PURPOSE
After the video

CONNECT
Build on the preceding slide: Short explainer and discussion.

DELIVER THIS SLIDE
Read the stated purpose, then point to the named example or action on the slide. Ask learners to describe what they will do before moving on. For a break slide, announce the return time; for a section divider, name the next concrete task.

NEXT
Preparing for the assignment. Move on after a learner can explain the current example or required action.

## Slide 48 — Preparing for the assignment

TEACHING PURPOSE
Preparing for the assignment

CONNECT
Build on the preceding slide: After the video.

LECTURER CUE
W08 asks for baseline, linear and depth-4 tree prediction lists plus error metrics. Teach training-only median imputation, Pipeline, list-to-table conversion and dictionary return values before those interfaces. Only load_pct and ambient_c are predictors. Introduce grouped partitions now, not first in Week 10. The written comparison is a supplied scenario; do not pretend to have measured its numbers.

EXPLAIN IN ORDINARY WORDS
A baseline is a deliberately simple reference. For numeric prediction, one example always predicts the training target mean. A more complicated model must earn its complexity by improving a fair comparison.

CHECK AND EXPECTED ANSWER
Why compute the constant from training targets? Evaluation answers must not influence a deployed prediction rule.

IF LEARNERS ARE STUCK
Use training targets 2,4,6: the mean baseline predicts 4 for every new row, whatever its inputs.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Preparing for the assignment continued. Move on after a learner can explain the current example or required action.

## Slide 49 — Preparing for the assignment continued

TEACHING PURPOSE
Preparing for the assignment continued

CONNECT
Build on the preceding slide: Preparing for the assignment.

LECTURER CUE
W08 asks for baseline, linear and depth-4 tree prediction lists plus error metrics. Teach training-only median imputation, Pipeline, list-to-table conversion and dictionary return values before those interfaces. Only load_pct and ambient_c are predictors. Introduce grouped partitions now, not first in Week 10. The written comparison is a supplied scenario; do not pretend to have measured its numbers.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Reading model outputs. Move on after a learner can explain the current example or required action.

## Slide 50 — Reading model outputs

TEACHING PURPOSE
Reading model outputs

CONNECT
Build on the preceding slide: Preparing for the assignment continued.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

NEXT
Reading model outputs continued. Move on after a learner can explain the current example or required action.

## Slide 51 — Reading model outputs continued

TEACHING PURPOSE
Reading model outputs continued

CONNECT
Build on the preceding slide: Reading model outputs.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
An error compares prediction with measured truth. Absolute error ignores direction. MAE averages absolute errors; RMSE squares, averages, then takes a square root. Both use the target unit.

CHECK AND EXPECTED ANSWER
Actual [4,8], predicted [5,6]: prediction-minus-actual errors [1,-2], MAE=1.5, RMSE=sqrt(2.5), about 1.58.

IF LEARNERS ARE STUCK
Calculate one pair by hand first. For signed percentage error follow the precise sign convention in the issued task.

NEXT
Your issued task. Move on after a learner can explain the current example or required action.

## Slide 52 — Your issued task

TEACHING PURPOSE
Your issued task

CONNECT
Build on the preceding slide: Reading model outputs continued.

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
predict_regression(training_records, feature_records). Move on after a learner can explain the current example or required action.

## Slide 53 — predict_regression(training_records, feature_records)

TEACHING PURPOSE
predict_regression(training_records, feature_records)

CONNECT
Build on the preceding slide: Your issued task.

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W08/CML3113/A/TASKS.md

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
regression_errors(actual, predicted). Move on after a learner can explain the current example or required action.

## Slide 54 — regression_errors(actual, predicted)

TEACHING PURPOSE
regression_errors(actual, predicted)

CONNECT
Build on the preceding slide: predict_regression(training_records, feature_records).

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W08/CML3113/A/TASKS.md

EXPLAIN IN ORDINARY WORDS
An error compares prediction with measured truth. Absolute error ignores direction. MAE averages absolute errors; RMSE squares, averages, then takes a square root. Both use the target unit.

CHECK AND EXPECTED ANSWER
Actual [4,8], predicted [5,6]: prediction-minus-actual errors [1,-2], MAE=1.5, RMSE=sqrt(2.5), about 1.58.

IF LEARNERS ARE STUCK
Calculate one pair by hand first. For signed percentage error follow the precise sign convention in the issued task.

NEXT
Written evidence. Move on after a learner can explain the current example or required action.

## Slide 55 — Written evidence

TEACHING PURPOSE
Written evidence

CONNECT
Build on the preceding slide: regression_errors(actual, predicted).

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
Regression and baseline submission. Move on after a learner can explain the current example or required action.

## Slide 56 — Regression and baseline submission

TEACHING PURPOSE
Regression and baseline submission

CONNECT
Build on the preceding slide: Written evidence.

LECTURER CUE
The form link is cohort-specific. Recheck the live form and release status before class. These scheduled assignment dates are separate from the quiz activation window. The issued brief defines the required files, even if the form accepts additional formats. Source: data/submission_links.json

EXPLAIN IN ORDINARY WORDS
A baseline is a deliberately simple reference. For numeric prediction, one example always predicts the training target mean. A more complicated model must earn its complexity by improving a fair comparison.

CHECK AND EXPECTED ANSWER
Why compute the constant from training targets? Evaluation answers must not influence a deployed prediction rule.

IF LEARNERS ARE STUCK
Use training targets 2,4,6: the mean baseline predicts 4 for every new row, whatever its inputs.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Data analysis project. Move on after a learner can explain the current example or required action.

## Slide 57 — Data analysis project

TEACHING PURPOSE
Data analysis project

CONNECT
Build on the preceding slide: Regression and baseline submission.

LECTURER CUE
# CML3113 DA_PROJECT: Data analysis project — variant A
Full assessment requirements belong in the current public task guide; explain only the criterion or task shown on this slide.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

PROJECT UPLOAD SET
For the DA_PROJECT or ML_PROJECT, submit the completed project .ipynb together with one readable DOCX or selectable-text PDF report. This differs from the single-notebook test packet. The current public project guide defines the evidence and rubric; do not substitute weekly practice for the project.

NEXT
Data analysis project continued. Move on after a learner can explain the current example or required action.

## Slide 58 — Data analysis project continued

TEACHING PURPOSE
Data analysis project continued

CONNECT
Build on the preceding slide: Data analysis project.

LECTURER CUE
# CML3113 DA_PROJECT: Data analysis project — variant A
Full assessment requirements belong in the current public task guide; explain only the criterion or task shown on this slide.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

PROJECT UPLOAD SET
For the DA_PROJECT or ML_PROJECT, submit the completed project .ipynb together with one readable DOCX or selectable-text PDF report. This differs from the single-notebook test packet. The current public project guide defines the evidence and rubric; do not substitute weekly practice for the project.

NEXT
Data analysis project continued. Move on after a learner can explain the current example or required action.

## Slide 59 — Data analysis project continued

TEACHING PURPOSE
Data analysis project continued

CONNECT
Build on the preceding slide: Data analysis project continued.

LECTURER CUE
# CML3113 DA_PROJECT: Data analysis project — variant A
Full assessment requirements belong in the current public task guide; explain only the criterion or task shown on this slide.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

PROJECT UPLOAD SET
For the DA_PROJECT or ML_PROJECT, submit the completed project .ipynb together with one readable DOCX or selectable-text PDF report. This differs from the single-notebook test packet. The current public project guide defines the evidence and rubric; do not substitute weekly practice for the project.

NEXT
Data analysis project continued. Move on after a learner can explain the current example or required action.

## Slide 60 — Data analysis project continued

TEACHING PURPOSE
Data analysis project continued

CONNECT
Build on the preceding slide: Data analysis project continued.

LECTURER CUE
# CML3113 DA_PROJECT: Data analysis project — variant A
Full assessment requirements belong in the current public task guide; explain only the criterion or task shown on this slide.

EXPLAIN IN ORDINARY WORDS
Begin with the question and intended comparison. Identify what an axis, bar, point or colour represents, including its unit. A chart summarises data and may hide variation.

CHECK AND EXPECTED ANSWER
For a bar chart comparing amounts, why normally start the value axis at zero? Bar length encodes magnitude; truncation can exaggerate differences.

IF LEARNERS ARE STUCK
Read one mark aloud as a sentence. Check the population, period, filters and units before stating the finding.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

PROJECT UPLOAD SET
For the DA_PROJECT or ML_PROJECT, submit the completed project .ipynb together with one readable DOCX or selectable-text PDF report. This differs from the single-notebook test packet. The current public project guide defines the evidence and rubric; do not substitute weekly practice for the project.

NEXT
Data analysis project continued. Move on after a learner can explain the current example or required action.

## Slide 61 — Data analysis project continued

TEACHING PURPOSE
Data analysis project continued

CONNECT
Build on the preceding slide: Data analysis project continued.

LECTURER CUE
# CML3113 DA_PROJECT: Data analysis project — variant A
Full assessment requirements belong in the current public task guide; explain only the criterion or task shown on this slide.

EXPLAIN IN ORDINARY WORDS
A repository is the project folder and recorded history. A commit records a chosen change; uploading or pushing shares it. A README tells someone else how to run the work.

CHECK AND EXPECTED ANSWER
Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.

IF LEARNERS ARE STUCK
Ask a partner to follow only the README. It should identify the data, files, run order and expected result. Keep secrets out of the repository.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

PROJECT UPLOAD SET
For the DA_PROJECT or ML_PROJECT, submit the completed project .ipynb together with one readable DOCX or selectable-text PDF report. This differs from the single-notebook test packet. The current public project guide defines the evidence and rubric; do not substitute weekly practice for the project.

NEXT
Data analysis project submission. Move on after a learner can explain the current example or required action.

## Slide 62 — Data analysis project submission

TEACHING PURPOSE
Data analysis project submission

CONNECT
Build on the preceding slide: Data analysis project continued.

LECTURER CUE
The form link is cohort-specific. Recheck the live form and release status before class. These scheduled assignment dates are separate from the quiz activation window. The issued brief defines the required files, even if the form accepts additional formats. Source: data/submission_links.json

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

PROJECT UPLOAD SET
For the DA_PROJECT or ML_PROJECT, submit the completed project .ipynb together with one readable DOCX or selectable-text PDF report. This differs from the single-notebook test packet. The current public project guide defines the evidence and rubric; do not substitute weekly practice for the project.

NEXT
Week 8 quiz. Move on after a learner can explain the current example or required action.

## Slide 63 — Week 8 quiz

TEACHING PURPOSE
Week 8 quiz

CONNECT
Build on the preceding slide: Data analysis project submission.

LECTURER CUE
Activate the matching open_W8_CML3113 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

QUIZ OPERATION
Opening the student link does not activate the quiz. In Quiz Controls run the matching open_W<week>_<cohort> function once when ready. Announce the logged closing time: 24 hours after activation. Five minutes describes expected answering time, not the availability window. Quiz 1 and Quiz 2 require separate activation when collecting catch-up work.

NEXT
Before you leave. Move on after a learner can explain the current example or required action.

## Slide 64 — Before you leave

TEACHING PURPOSE
Before you leave

CONNECT
Build on the preceding slide: Week 8 quiz.

LECTURER CUE
Ask every learner for an individual response. Record one misconception to revisit at the start of the next class. If a deadline changed, announce the exact Kampala date and update the source registry before rebuilding slides.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

