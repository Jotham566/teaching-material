# CML3112 Week08 Design Infrastructure

Lecturer companion to the revised PowerPoint. Slide numbers match this edition. Explain the worked examples directly; revision checks are for individual study.

## Slide 1 — A first prediction model

PURPOSE
A first prediction model

CONNECT
Build on the preceding week. Explain why this example is needed before running it.

EXPLAIN
Civil Engineering and Architecture

LECTURER DETAIL
TEACHING PURPOSE
A first prediction model

LECTURER CUE
Use PowerPoint Presenter View for these notes. Teach one example, pause for every learner to predict, then work an analogous example together. The practice notebook is a learning aid, not an extra graded upload.

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
Build on A first prediction model. Explain why this example is needed before running it.

EXPLAIN
Identify prediction inputs and a measured target.

Fit a simple model and compare prediction errors.

LECTURER DETAIL
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
Weeks 3–6 supplied Python, tables, cleaning and charts. We now use paired inputs and known answers to fit a prediction rule.

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
A regression model predicts a numerical engineering target from measurements available beforehand. The small invented data explain the code; they do not establish real-world accuracy.

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
A numerical prediction. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A numerical prediction.

## Slide 5 — A numerical prediction

PURPOSE
A numerical prediction

CONNECT
Build on Why this week’s tools are needed. Explain why this example is needed before running it.

EXPLAIN
Regression predicts a number, such as cooling load in kW.

A feature is information available when predicting.

The target is the measured answer used during training.

Classification, next week, predicts a category.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Feature and target and Training validation and test.

## Slide 6 — Feature and target and Training validation and test

PURPOSE
Feature and target and Training validation and test

CONNECT
Build on A numerical prediction. Explain why this example is needed before running it.

EXPLAIN
Feature and target: Features are inputs available when making a prediction. The target is the quantity we want to predict.
Training validation and test: Training fits the model. Validation helps choose it. The final test estimates performance after choices are fixed. Repeated equipment must stay in the same partition when assessing unseen equipment.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Baseline.

## Slide 7 — Baseline

PURPOSE
Baseline

CONNECT
Build on Feature and target and Training validation and test. Explain why this example is needed before running it.

EXPLAIN
Baseline: A simple reference prediction. A training-mean baseline predicts the same training mean for every new example.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Linear model and tree.

## Slide 8 — Linear model and tree

PURPOSE
Linear model and tree

CONNECT
Build on Baseline. Explain why this example is needed before running it.

EXPLAIN
Linear model and tree: A linear model combines inputs with learned weights. A regression tree asks feature-threshold questions and predicts a value at each leaf.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
What learning means in this example.

## Slide 9 — What learning means in this example

PURPOSE
What learning means in this example

CONNECT
Build on Linear model and tree. Explain why this example is needed before running it.

EXPLAIN
Training supplies inputs and their known answers.

The model uses those examples to choose its internal numbers.

Prediction applies the fitted model to inputs whose answer we want to estimate.

LECTURER DETAIL
TEACHING PURPOSE
What learning means in this example

CONNECT
Build on the preceding slide: Linear model and tree.

LECTURER CUE
Use the small invented table below solely to see fit and predict. Real training needs more data, representative evaluation and careful partitioning.

NEXT
Training observations. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Training observations.

## Slide 10 — Training observations

PURPOSE
Training observations

CONNECT
Build on What learning means in this example. Explain why this example is needed before running it.

EXPLAIN
Invented numbers for learning.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A fitted line is a numerical rule.

## Slide 11 — A fitted line is a numerical rule

PURPOSE
A fitted line is a numerical rule

CONNECT
Build on Training observations. Explain why this example is needed before running it.

EXPLAIN
For these invented observations, target = 2 × input + 10 matches all four points. 2 is the slope; 10 is the intercept, the value at input zero.

A prediction error is the difference between a prediction and the measured answer. A vertical gap in the picture shows that error.

Fitting chooses the slope and intercept to minimise summed squared errors. Squaring means multiplying an error by itself; a small training error still needs an unseen-data check.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Fitting a line to observations.

## Slide 12 — Fitting a line to observations

PURPOSE
Fitting a line to observations

CONNECT
Build on A fitted line is a numerical rule. Explain why this example is needed before running it.

EXPLAIN
The fitted line minimises the sum of squared vertical errors.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Rows must stay paired with their answers.

## Slide 13 — Rows must stay paired with their answers

PURPOSE
Rows must stay paired with their answers

CONNECT
Build on Fitting a line to observations. Explain why this example is needed before running it.

EXPLAIN
Each inner list in X_train is one observation.

y_train contains one target value for each row, in the same order.

Changing the order of only one list attaches answers to the wrong observations.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A matrix is a rectangular table of numbers.

## Slide 14 — A matrix is a rectangular table of numbers

PURPOSE
A matrix is a rectangular table of numbers

CONNECT
Build on Rows must stay paired with their answers. Explain why this example is needed before running it.

EXPLAIN
A matrix has rows and columns. For modelling, one row is one observation and each column is one input feature.

[[1, 20], [2, 22]] has two rows and two columns. The outer list contains rows; each inner list contains that row’s features.

X is a conventional name for this input table. y holds one known target per row. These names have no special power in Python.

LECTURER DETAIL


TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Rows and arrays before model code.

## Slide 15 — Rows and arrays before model code

PURPOSE
Rows and arrays before model code

CONNECT
Build on A matrix is a rectangular table of numbers. Explain why this example is needed before running it.

EXPLAIN
Nested lists: [[1], [2], [3]] has three inner lists: three rows with one feature each. [12, 14, 16] has one target per row in the same order.
NumPy and array: NumPy is a numerical library; np is its short imported name. np.array(...) builds an array. shape reports its dimensions. np.nan represents a missing numerical value.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Reading NumPy results.

## Slide 16 — Reading NumPy results

PURPOSE
Reading NumPy results

CONNECT
Build on Rows and arrays before model code. Explain why this example is needed before running it.

EXPLAIN
Use rounded values only for a labelled display. Keep full precision when the assignment requires it.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Rows, columns and named options.

## Slide 17 — Rows, columns and named options

PURPOSE
Rows, columns and named options

CONNECT
Build on Reading NumPy results. Explain why this example is needed before running it.

EXPLAIN
X has three rows and one feature column. y has three target values.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
fit and predict.

## Slide 18 — fit and predict

PURPOSE
fit and predict

CONNECT
Build on Rows, columns and named options. Explain why this example is needed before running it.

EXPLAIN
fit and predict: fit learns from training inputs and targets. predict uses the fitted rule on new inputs without receiving their true targets.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A model object keeps learned information.

## Slide 19 — A model object keeps learned information

PURPOSE
A model object keeps learned information

CONNECT
Build on fit and predict. Explain why this example is needed before running it.

EXPLAIN
Object and method: LinearRegression() creates a model object. A method is an operation on that object. model.fit(...) stores learned information; model.predict(...) uses it.
Options: An argument such as strategy="mean" names an option. A random seed fixes the starting state of random choices; it does not prove that a model is accurate.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
An object remembers its fitted state.

## Slide 20 — An object remembers its fitted state

PURPOSE
An object remembers its fitted state

CONNECT
Build on A model object keeps learned information. Explain why this example is needed before running it.

EXPLAIN
An object holds state and has methods. A method is a function used through that object.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Creating, fitting and predicting.

## Slide 21 — Creating, fitting and predicting

PURPOSE
Creating, fitting and predicting

CONNECT
Build on An object remembers its fitted state. Explain why this example is needed before running it.

EXPLAIN
LinearRegression() creates a model that has not learned yet.

fit(X_train, y_train) learns from paired training examples.

predict(new_inputs) returns estimates. The actual targets are absent from new_inputs.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Where the modelling tools come from.

## Slide 22 — Where the modelling tools come from

PURPOSE
Where the modelling tools come from

CONNECT
Build on Creating, fitting and predicting. Explain why this example is needed before running it.

EXPLAIN
scikit-learn is an installed machine-learning library. Its Python import name is sklearn. linear_model is the part containing LinearRegression.

from sklearn.linear_model import LinearRegression makes that model class available. LinearRegression() creates an individual model object.

In Colab this library is normally available. If an import fails, use the course setup instructions and retry the import before running model code.

LECTURER DETAIL


TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Worked example.

## Slide 23 — Regression models and errors in Python

PURPOSE
Regression models and errors in Python

CONNECT
Build on Where the modelling tools come from. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Worked example continued.

## Slide 24 — Regression models and errors in Python continued

PURPOSE
Regression models and errors in Python continued

CONNECT
Build on Regression models and errors in Python. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Worked example continued.

## Slide 25 — Regression models and errors in Python continued

PURPOSE
Regression models and errors in Python continued

CONNECT
Build on Regression models and errors in Python continued. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Expected output.

## Slide 26 — Regression models and errors results

PURPOSE
Regression models and errors results

CONNECT
Build on Regression models and errors in Python continued. Explain why this example is needed before running it.

EXPLAIN
[15.0]

LECTURER DETAIL
TEACHING PURPOSE
Expected output

CONNECT
Build on the preceding slide: Worked example continued.

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

NEXT
The mean baseline. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
The mean baseline.

## Slide 27 — The mean baseline

PURPOSE
The mean baseline

CONNECT
Build on Regression models and errors results. Explain why this example is needed before running it.

EXPLAIN
Use the same training data.

This baseline learns their mean, 15, and predicts it for every input.

It gives a simple comparison before claiming the line helps.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
The mean baseline in Python.

## Slide 28 — The mean baseline in Python

PURPOSE
The mean baseline in Python

CONNECT
Build on The mean baseline. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A small regression tree.

## Slide 29 — A small regression tree

PURPOSE
A small regression tree

CONNECT
Build on The mean baseline in Python. Explain why this example is needed before running it.

EXPLAIN
A tree learns threshold questions from the training inputs.

Each final group, or leaf, predicts a target value.

This tree returns 14 for input 2.5 in this toy example. max_depth limits the number of successive decisions. random_state fixes the random seed.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A small regression tree in Python.

## Slide 30 — A small regression tree in Python

PURPOSE
A small regression tree in Python

CONNECT
Build on A small regression tree. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Reuse the same preparation on new inputs.

## Slide 31 — Reuse the same preparation on new inputs

PURPOSE
Reuse the same preparation on new inputs

CONNECT
Build on A small regression tree in Python. Explain why this example is needed before running it.

EXPLAIN
Imputer: An imputer fills missing feature values using a stated rule. Fit learns the replacement from training observations only. Prediction reuses that stored replacement.
Pipeline: A pipeline connects preprocessing and a model. make_pipeline creates that connection. Its fit learns both stages on training data; predict applies them to new features.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Preprocessing learned from training only.

## Slide 32 — Preprocessing learned from training only

PURPOSE
Preprocessing learned from training only

CONNECT
Build on Reuse the same preparation on new inputs. Explain why this example is needed before running it.

EXPLAIN
SimpleImputer learns one median for each training column. make_pipeline connects this step to the model. fit learns both steps using only the training examples. predict reuses them on new inputs.

No target is supplied to predict.

The two inputs here are invented practice measurements.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Preprocessing learned from training only in Python (1/2).

## Slide 33 — Preprocessing learned from training only in Python (1/2)

PURPOSE
Preprocessing learned from training only in Python (1/2)

CONNECT
Build on Preprocessing learned from training only. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Preprocessing learned from training only in Python (2/2).

## Slide 34 — Preprocessing learned from training only in Python (2/2)

PURPOSE
Preprocessing learned from training only in Python (2/2)

CONNECT
Build on Preprocessing learned from training only in Python (1/2). Explain why this example is needed before running it.

EXPLAIN
Continue the SAME cell; keep indentation. Run after all parts are entered.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Reading records into a feature table.

## Slide 35 — Reading records into a feature table

PURPOSE
Reading records into a feature table

CONNECT
Build on Preprocessing learned from training only in Python (2/2). Explain why this example is needed before running it.

EXPLAIN
Each inner list is one row, in the same order as the input records.

The target list uses that same row order.

The feature table has no answer column.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Reading records into a feature table in Python.

## Slide 36 — Reading records into a feature table in Python

PURPOSE
Reading records into a feature table in Python

CONNECT
Build on Reading records into a feature table. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
MAE and RMSE.

## Slide 37 — MAE and RMSE

PURPOSE
MAE and RMSE

CONNECT
Build on Reading records into a feature table in Python. Explain why this example is needed before running it.

EXPLAIN
MAE and RMSE: MAE averages absolute prediction errors. RMSE squares errors, averages them and takes the square root. Both use target units. RMSE is more sensitive to large errors.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A prediction error in ordinary numbers.

## Slide 38 — A prediction error in ordinary numbers

PURPOSE
A prediction error in ordinary numbers

CONNECT
Build on MAE and RMSE. Explain why this example is needed before running it.

EXPLAIN
MAE = (2 + 4) / 2 = 3, in the target’s unit. Compare a model against a training-only baseline.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
The operations in the error calculation.

## Slide 39 — The operations in the error calculation

PURPOSE
The operations in the error calculation

CONNECT
Build on A prediction error in ordinary numbers. Explain why this example is needed before running it.

EXPLAIN
zip and paired names: zip(actual, predicted) pairs values at matching positions. for truth, guess in ... assigns each pair to two names. Here both lists must have the same nonzero length.
Square and square root: difference ** 2 squares an error. sqrt reverses a square for nonnegative numbers: sqrt(9) is 3. from math import sqrt makes this tool available.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Two error measures.

## Slide 40 — Two error measures

PURPOSE
Two error measures

CONNECT
Build on The operations in the error calculation. Explain why this example is needed before running it.

EXPLAIN
zip pairs corresponding values. abs measures error size.

Squaring emphasises large errors; taking the square root returns to the original unit.

These functions assume equal-length, nonempty paired observations.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Two error measures in Python (1/2).

## Slide 41 — Two error measures in Python (1/2)

PURPOSE
Two error measures in Python (1/2)

CONNECT
Build on Two error measures. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Two error measures in Python (2/2).

## Slide 42 — Two error measures in Python (2/2)

PURPOSE
Two error measures in Python (2/2)

CONNECT
Build on Two error measures in Python (1/2). Explain why this example is needed before running it.

EXPLAIN
Continue the SAME cell; keep indentation. Run after all parts are entered.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
R² compares against a mean prediction.

## Slide 43 — R² compares against a mean prediction

PURPOSE
R² compares against a mean prediction

CONNECT
Build on Two error measures in Python (2/2). Explain why this example is needed before running it.

EXPLAIN
R² compares squared errors with predicting the mean of the evaluated targets. It is a score, not “percentage accuracy”.

1 means perfect predictions on those observations. 0 matches that mean-prediction reference; a negative score can be worse.

Use the same evaluation observations and report the specified error metric with its units. Constant targets need special handling; this score alone does not prove usefulness.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Revision example and answer.

## Slide 44 — Revision example and answer

PURPOSE
Revision example and answer

CONNECT
Build on R² compares against a mean prediction. Explain why this example is needed before running it.

EXPLAIN
Example: On paper compare actual [10, 20] with predictions [12, 16]. Find MAE and RMSE. Is MAE a plus/minus guarantee for each prediction?

Answer: Absolute errors are 2 and 4: MAE 3. Squared errors 4 and 16: RMSE sqrt(10), about 3.162. MAE is an average, not an individual error bound.

LECTURER DETAIL
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
CML3112   Week 8   45
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
Practice discussion. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Preparing for the assignment.

## Slide 45 — Preparing for the assignment

PURPOSE
Preparing for the assignment

CONNECT
Build on Revision example and answer. Explain why this example is needed before running it.

EXPLAIN
W08 asks for baseline, linear and depth-4 tree prediction lists plus error metrics.

Fit missing-value replacement on training data.

A Pipeline joins preprocessing to the model.

Only load_pct and ambient_c are predictors.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Preparing for the assignment continued.

## Slide 46 — Preparing for the assignment continued

PURPOSE
Preparing for the assignment continued

CONNECT
Build on Preparing for the assignment. Explain why this example is needed before running it.

EXPLAIN
Keep observations from the same equipment in one partition.

The written comparison supplies scenario values.

Distinguish them from your own measured results.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Reading model outputs.

## Slide 47 — Reading model outputs

PURPOSE
Reading model outputs

CONNECT
Build on Preparing for the assignment continued. Explain why this example is needed before running it.

EXPLAIN
A score on training rows describes training fit.

A feature table must preserve the training column names, order and units during prediction.

A one-dimensional list may have the wrong shape for a model expecting rows and columns.

A predicted-versus-actual plot uses the diagonal as perfect agreement; a pattern is not proof of causation.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Reading model outputs continued.

## Slide 48 — Reading model outputs continued

PURPOSE
Reading model outputs continued

CONNECT
Build on Reading model outputs. Explain why this example is needed before running it.

EXPLAIN
Judge MAE against the baseline and the decision’s acceptable error.

R² is not an accuracy percentage.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Your issued task.

## Slide 49 — Your issued task

PURPOSE
Your issued task

CONNECT
Build on Reading model outputs continued. Explain why this example is needed before running it.

EXPLAIN
Investigate building cooling load.

Target units: kW.

These are synthetic teaching records, not measurements suitable for deployment.

Each record is one operating observation; equipment_id repeats across observations.

LECTURER DETAIL
TEACHING PURPOSE
Your issued task

CONNECT
Build on the preceding slide: Reading model outputs continued.

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
predict_regression(training_records, feature_records). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
predict_regression(training_records, feature_records).

## Slide 50 — predict_regression(training_records, feature_records)

PURPOSE
predict_regression(training_records, feature_records)

CONNECT
Build on Your issued task. Explain why this example is needed before running it.

EXPLAIN
Fit a training-mean baseline, linear regression and a decision tree (max_depth=4, random_state=17) using load_pct and ambient_c only.

Return three prediction lists under baseline, linear and tree.

Feature records have no target.

Fit preprocessing only on training data.

LECTURER DETAIL
TEACHING PURPOSE
predict_regression(training_records, feature_records)

CONNECT
Build on the preceding slide: Your issued task.

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W08/CML3112/A/TASKS.md

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
regression_errors(actual, predicted). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
regression_errors(actual, predicted).

## Slide 51 — regression_errors(actual, predicted)

PURPOSE
regression_errors(actual, predicted)

CONNECT
Build on predict_regression(training_records, feature_records). Explain why this example is needed before running it.

EXPLAIN
Return mae and rmse, calculated over the same paired observations, with full precision.

LECTURER DETAIL
TEACHING PURPOSE
regression_errors(actual, predicted)

CONNECT
Build on the preceding slide: predict_regression(training_records, feature_records).

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W08/CML3112/A/TASKS.md

EXPLAIN IN ORDINARY WORDS
An error compares prediction with measured truth. Absolute error ignores direction. MAE averages absolute errors; RMSE squares, averages, then takes a square root. Both use the target unit.

CHECK AND EXPECTED ANSWER
Actual [4,8], predicted [5,6]: prediction-minus-actual errors [1,-2], MAE=1.5, RMSE=sqrt(2.5), about 1.58.

IF LEARNERS ARE STUCK
Calculate one pair by hand first. For signed percentage error follow the precise sign convention in the issued task.

NEXT
Written evidence. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Written evidence.

## Slide 52 — Written evidence

PURPOSE
Written evidence

CONNECT
Build on regression_errors(actual, predicted). Explain why this example is needed before running it.

EXPLAIN
Use the cell headed “My written evidence”.

Explain the supplied scenario in your own words.

State target units, reasons and limitations.

Submit one complete notebook containing code and written evidence.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Regression and baseline submission.

## Slide 53 — Regression and baseline submission

PURPOSE
Regression and baseline submission

CONNECT
Build on Written evidence. Explain why this example is needed before running it.

EXPLAIN
Opens: 27 Oct 2026, 11:00 Kampala

Deadline: 03 Nov 2026, 11:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Data analysis project.

## Slide 54 — Data analysis project

PURPOSE
Data analysis project

CONNECT
Build on Regression and baseline submission. Explain why this example is needed before running it.

EXPLAIN
Write your own explanation in the markdown cell headed `## My written evidence`.

Keep that heading.

Task prompts and code comments are excluded from reasoning marks.

Complete every original rubric criterion below, not just the checked functions.

LECTURER DETAIL
TEACHING PURPOSE
Data analysis project

CONNECT
Build on the preceding slide: Regression and baseline submission.

LECTURER CUE
# CML3112 DA_PROJECT: Data analysis project — variant A
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Data analysis project continued.

## Slide 55 — Data analysis project continued

PURPOSE
Data analysis project continued

CONNECT
Build on Data analysis project. Explain why this example is needed before running it.

EXPLAIN
Include profiling, justified cleaning, question-led charts and your engineering recommendation where required.

Keep raw data.

State units and distinguish correlation from causation.

Charts must be actual labelled figures in the notebook, not claims that charts exist.

LECTURER DETAIL
TEACHING PURPOSE
Data analysis project continued

CONNECT
Build on the preceding slide: Data analysis project.

LECTURER CUE
# CML3112 DA_PROJECT: Data analysis project — variant A
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Data analysis project continued.

## Slide 56 — Data analysis project continued

PURPOSE
Data analysis project continued

CONNECT
Build on Data analysis project continued. Explain why this example is needed before running it.

EXPLAIN
Include captions and a separate readable DOCX/PDF report.

Question & dataset fit (20.0 total): A real engineering question is stated, and the chosen dataset can actually answer it.

Provenance and licence stated.

Data quality work (25.0 total): Defects found and handled with written justification.

LECTURER DETAIL
TEACHING PURPOSE
Data analysis project continued

CONNECT
Build on the preceding slide: Data analysis project continued.

LECTURER CUE
# CML3112 DA_PROJECT: Data analysis project — variant A
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Data analysis project continued.

## Slide 57 — Data analysis project continued

PURPOSE
Data analysis project continued

CONNECT
Build on Data analysis project continued. Explain why this example is needed before running it.

EXPLAIN
A data quality statement is present.

Analysis & visualisation (30.0 total): Four or more charts, each answering a stated question.

Correct chart types, labelled axes, findings in the captions.

Findings & interpretation (20.0 total): Conclusions supported by the analysis, stated in engineering terms, with limitations acknowledged.

LECTURER DETAIL
TEACHING PURPOSE
Data analysis project continued

CONNECT
Build on the preceding slide: Data analysis project continued.

LECTURER CUE
# CML3112 DA_PROJECT: Data analysis project — variant A
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Data analysis project continued.

## Slide 58 — Data analysis project continued

PURPOSE
Data analysis project continued

CONNECT
Build on Data analysis project continued. Explain why this example is needed before running it.

EXPLAIN
Individual contribution log (5.0 total): Present, specific, and consistent with the repository's commit history.

LECTURER DETAIL
TEACHING PURPOSE
Data analysis project continued

CONNECT
Build on the preceding slide: Data analysis project continued.

LECTURER CUE
# CML3112 DA_PROJECT: Data analysis project — variant A
Full assessment requirements belong in the current public task guide; explain only the criterion or task shown on this slide.

EXPLAIN IN ORDINARY WORDS
A repository is the project folder and recorded history. A commit records a chosen change; uploading or pushing shares it. A README tells someone else how to run the work.

CHECK AND EXPECTED ANSWER
Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.

IF LEARNERS ARE STUCK

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

PROJECT UPLOAD SET
For the DA_PROJECT or ML_PROJECT, submit the completed project .ipynb together with one readable DOCX or selectable-text PDF report. This differs from the single-notebook test packet. The current public project guide defines the evidence and rubric; do not substitute weekly practice for the project.

NEXT
Data analysis project submission. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Data analysis project submission.

## Slide 59 — Data analysis project submission

PURPOSE
Data analysis project submission

CONNECT
Build on Data analysis project continued. Explain why this example is needed before running it.

EXPLAIN
Opens: 06 Oct 2026, 11:00 Kampala

Deadline: 27 Oct 2026, 11:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Week 8 quiz.

## Slide 60 — Week 8 quiz

PURPOSE
Week 8 quiz

CONNECT
Build on Data analysis project submission. Explain why this example is needed before running it.

EXPLAIN
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

The lecturer will confirm the exact closing time.

LECTURER DETAIL
TEACHING PURPOSE
Week 8 quiz

CONNECT
Build on the preceding slide: Data analysis project submission.

LECTURER CUE
Activate the matching open_W8_CML3112 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

QUIZ OPERATION
Opening the student link does not activate the quiz. In Quiz Controls run the matching open_W<week>_<cohort> function once when ready. Announce the logged closing time: 24 hours after activation. Five minutes describes expected answering time, not the availability window. Quiz 1 and Quiz 2 require separate activation when collecting catch-up work.

NEXT
Before you leave. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Before you leave.

## Slide 61 — Revision and submission checklist

PURPOSE
Revision and submission checklist

CONNECT
Build on Week 8 quiz. Explain why this example is needed before running it.

EXPLAIN
You can calculate one error and explain why evaluation needs unseen observations.

Save your work and check the required submission files.

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Optional revision video.

## Slide 62 — Optional revision video

PURPOSE
Optional revision video

CONNECT
Build on Revision and submission checklist. Explain why this example is needed before running it.

EXPLAIN
For revision after class.

StatQuest with Josh Starmer
The Essence of Linear Regression!!!

Opening up to 04:00, optional preview-selected excerpt

Listening question: How can a fitted line turn an input into a numerical prediction?

LECTURER DETAIL
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

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
independent revision and the issued task.
