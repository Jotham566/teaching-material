# CML3113 Week08 Mining Petroleum

Lecturer companion. The same explanations are embedded in the PowerPoint speaker notes. Open Presenter View, or expand the Notes pane when preparing.

## Slide 1 — A first prediction model

A first prediction model
CML3113, Week 8, slide 1

Explanation to give
Introduce a fitted predictor only after identifying its inputs and known answers. Compare it with a simple baseline and explain its errors in target units.

Worked illustration / lecturer answer
The teaching line through (1,12), (2,14), (3,16), (4,18) predicts 15 at input 2.5. One neat example does not establish real-world accuracy.

Misconception to address
Use this as an orientation to the lesson. Terms and syntax will be unpacked on their own slides; students do not need to know them in advance.

On this slide
Mining and Petroleum Engineering

Continue to
Today’s learning

## Slide 2 — Today’s learning

Today’s learning
CML3113, Week 8, slide 2

Explanation to give
Introduce a fitted predictor only after identifying its inputs and known answers. Compare it with a simple baseline and explain its errors in target units.

Worked illustration / lecturer answer
The teaching line through (1,12), (2,14), (3,16), (4,18) predicts 15 at input 2.5. One neat example does not establish real-world accuracy.

Misconception to address
At the end, check the specific outcome shown here using a small previously demonstrated example. A completed file without an explanation is not evidence of understanding.

On this slide
Identify prediction inputs and a measured target.

Fit a simple model and compare prediction errors.

Continue to
Connection to the previous lesson

## Slide 3 — Connection to the previous lesson

Connection to the previous lesson
CML3113, Week 8, slide 3

Explanation to give
Introduce a fitted predictor only after identifying its inputs and known answers. Compare it with a simple baseline and explain its errors in target units.

Worked illustration / lecturer answer
The teaching line through (1,12), (2,14), (3,16), (4,18) predicts 15 at input 2.5. One neat example does not establish real-world accuracy.

Misconception to address
Connect this to the previous result named on this slide. Demonstrate the first step again if necessary; there is no requirement for partner work before the explanation.

On this slide
Weeks 3–6 supplied Python, tables, cleaning and charts. We now use paired inputs and known answers to fit a prediction rule.

Continue to
Why this week’s tools are needed

## Slide 4 — Why this week’s tools are needed

Why this week’s tools are needed
CML3113, Week 8, slide 4

Explanation to give
Introduce a fitted predictor only after identifying its inputs and known answers. Compare it with a simple baseline and explain its errors in target units.

Worked illustration / lecturer answer
The teaching line through (1,12), (2,14), (3,16), (4,18) predicts 15 at input 2.5. One neat example does not establish real-world accuracy.

Misconception to address
Connect this to the previous result named on this slide. Demonstrate the first step again if necessary; there is no requirement for partner work before the explanation.

On this slide
A regression model predicts a numerical engineering target from measurements available beforehand. These small invented datasets demonstrate the code. They cannot establish performance on real engineering data.

Continue to
A numerical prediction

## Slide 5 — A numerical prediction

A numerical prediction
CML3113, Week 8, slide 5

Explanation to give
Classify the task by the answer the system must produce. Regression predicts a quantity with a meaningful numerical scale. Classification predicts a category, even if the labels are encoded as numbers.

Worked illustration / lecturer answer
Predicting days until servicing is regression. Predicting whether servicing is due is classification. A code of 0 for normal and 1 for warning still represents categories.

Misconception to address
Do not choose regression just because the dataset contains numbers. Name the target and explain what a prediction means.

On this slide
Regression predicts a number, such as cooling load in kW.

A feature is information available when predicting.

The target is the measured answer used during training.

Classification, next week, predicts a category.

Continue to
Feature and target and Training validation and test

## Slide 6 — Feature and target and Training validation and test

Feature and target and Training validation and test
CML3113, Week 8, slide 6

Explanation to give
A feature is information available when making a prediction. The target is the answer recorded for training examples. One observation pairs its features with its own target.

Worked illustration / lecturer answer
To predict tomorrow's cooling load, today's available weather information may be a feature. Tomorrow's measured cooling load becomes a target later. It cannot also be an input available now.

Misconception to address
Information recorded after the decision can leak the answer. An identifier or row number is not automatically a meaningful predictor.

On this slide
Feature and target: Features are inputs available when making a prediction. The target is the quantity we want to predict.
Training validation and test: Training fits the model. Validation helps choose it. The final test estimates performance after choices are fixed. Repeated equipment must stay in the same partition when assessing unseen equipment.

Continue to
Baseline

## Slide 7 — Baseline

Baseline
CML3113, Week 8, slide 7

Explanation to give
A baseline is a simple reference prediction against which a more elaborate method is judged. Define its rule clearly before reporting any comparison score.

Worked illustration / lecturer answer
If the training target mean is 15, a mean baseline returns 15 for every observation. Calculate its error on exactly the same evaluation cases used for the proposed model.

Misconception to address
A weaker baseline chosen after seeing the results can exaggerate an improvement. Use the stated baseline and evaluation protocol.

On this slide
Baseline: A simple reference prediction. A training-mean baseline predicts the same training mean for every new example.

Continue to
Linear model and tree

## Slide 8 — Linear model and tree

Linear model and tree
CML3113, Week 8, slide 8

Explanation to give
Use the four teaching pairs to make the learned relationship visible. A one-unit input increase corresponds to a two-unit target increase in this invented dataset.

Worked illustration / lecturer answer
The pairs (1,12), (2,14), (3,16), (4,18) follow target = 10 + 2 × input. For input 2.5, that line gives 15. A tree makes threshold-based group predictions instead.

Misconception to address
These perfectly patterned values explain model behaviour. They do not establish that real engineering data follows an exact line.

On this slide
Linear model and tree: A linear model combines inputs with learned weights. A regression tree asks feature-threshold questions and predicts a value at each leaf.

Continue to
What learning means in this example

## Slide 9 — What learning means in this example

What learning means in this example
CML3113, Week 8, slide 9

Explanation to give
Use the four teaching pairs to make the learned relationship visible. A one-unit input increase corresponds to a two-unit target increase in this invented dataset.

Worked illustration / lecturer answer
The pairs (1,12), (2,14), (3,16), (4,18) follow target = 10 + 2 × input. For input 2.5, that line gives 15. A tree makes threshold-based group predictions instead.

Misconception to address
These perfectly patterned values explain model behaviour. They do not establish that real engineering data follows an exact line.

On this slide
Training supplies inputs and their known answers.

The model uses those examples to choose its internal numbers.

Prediction applies the fitted model to inputs whose answer we want to estimate.

Continue to
Training observations

## Slide 10 — Training observations

Training observations
CML3113, Week 8, slide 10

Explanation to give
Use the four teaching pairs to make the learned relationship visible. A one-unit input increase corresponds to a two-unit target increase in this invented dataset.

Worked illustration / lecturer answer
The pairs (1,12), (2,14), (3,16), (4,18) follow target = 10 + 2 × input. For input 2.5, that line gives 15. A tree makes threshold-based group predictions instead.

Misconception to address
These perfectly patterned values explain model behaviour. They do not establish that real engineering data follows an exact line.

On this slide
Input | Measured target
1 | 12
2 | 14
3 | 16
4 | 18
Invented numbers for learning.

Continue to
A fitted line is a numerical rule

## Slide 11 — A fitted line is a numerical rule

A fitted line is a numerical rule
CML3113, Week 8, slide 11

Explanation to give
A fitted straight line summarises how the target changes with an input in the training examples. Its slope is the change in prediction per unit increase of input; its intercept is the prediction at input zero.

Worked illustration / lecturer answer
The teaching data [1,2,3,4] and [12,14,16,18] follow y = 10 + 2x. At x = 2.5 the line predicts 15. That is an illustration, not evidence of accuracy on engineering measurements.

Misconception to address
Fitting a neat line does not establish causation. Extrapolating beyond the observed range can be unreliable.

On this slide
For these invented observations, target = 2 × input + 10 matches all four points. 2 is the slope; 10 is the intercept, the value at input zero.

A prediction error is the difference between a prediction and the measured answer. A vertical gap in the picture shows that error.

Fitting chooses the slope and intercept to minimise summed squared errors. Squaring means multiplying an error by itself; a small training error still needs an unseen-data check.

Continue to
Fitting a line to observations

## Slide 12 — Fitting a line to observations

Fitting a line to observations
CML3113, Week 8, slide 12

Explanation to give
Use the four teaching pairs to make the learned relationship visible. A one-unit input increase corresponds to a two-unit target increase in this invented dataset.

Worked illustration / lecturer answer
The pairs (1,12), (2,14), (3,16), (4,18) follow target = 10 + 2 × input. For input 2.5, that line gives 15. A tree makes threshold-based group predictions instead.

Misconception to address
These perfectly patterned values explain model behaviour. They do not establish that real engineering data follows an exact line.

On this slide
The fitted line minimises the sum of squared vertical errors.

Continue to
Rows must stay paired with their answers

## Slide 13 — Rows must stay paired with their answers

Rows must stay paired with their answers
CML3113, Week 8, slide 13

Explanation to give
Preserve the relationship between one observation's inputs and its answer. Show shapes and row order before interpreting returned predictions.

Worked illustration / lecturer answer
X has four training rows and y has four targets. predictions.round(2) changes display precision; .tolist() converts a NumPy array to a Python list. Keep full-precision values for metrics when required.

Misconception to address
Rounding a displayed value is different from changing the values used for assessment. Do not shuffle X without applying the same reordering to y.

On this slide
Each inner list in X_train is one observation.

y_train contains one target value for each row, in the same order.

Changing the order of only one list attaches answers to the wrong observations.

Continue to
A matrix is a rectangular table of numbers

## Slide 14 — A matrix is a rectangular table of numbers

A matrix is a rectangular table of numbers
CML3113, Week 8, slide 14

Explanation to give
Explain an input matrix as a table of numbers with one observation per row and one feature per column. The target vector has one answer per observation in the same order.

Worked illustration / lecturer answer
[[1], [2], [3]] has shape (3, 1). [12, 14, 16] has shape (3,). For one new observation with two features, use [[2.5, 22]], not [2.5, 22].

Misconception to address
Swapping feature columns changes their meaning even if dimensions still match. The model expects the same order and units at prediction time.

On this slide
A matrix has rows and columns. For modelling, one row is one observation and each column is one input feature.

[[1, 20], [2, 22]] has two rows and two columns. The outer list contains rows; each inner list contains that row’s features.

X is a conventional name for this input table. y holds one known target per row. These names have no special power in Python.

Continue to
Rows and arrays before model code

## Slide 15 — Rows and arrays before model code

Rows and arrays before model code
CML3113, Week 8, slide 15

Explanation to give
Explain an input matrix as a table of numbers with one observation per row and one feature per column. The target vector has one answer per observation in the same order.

Worked illustration / lecturer answer
[[1], [2], [3]] has shape (3, 1). [12, 14, 16] has shape (3,). For one new observation with two features, use [[2.5, 22]], not [2.5, 22].

Misconception to address
Swapping feature columns changes their meaning even if dimensions still match. The model expects the same order and units at prediction time.

On this slide
Nested lists: [[1], [2], [3]] has three inner lists: three rows with one feature each. [12, 14, 16] has one target per row in the same order.
NumPy and array: NumPy is a numerical library; np is its short imported name. np.array(...) builds an array. shape reports its dimensions. np.nan represents a missing numerical value.

Continue to
Reading NumPy results

## Slide 16 — Reading NumPy results

Reading NumPy results
CML3113, Week 8, slide 16

Explanation to give
Preserve the relationship between one observation's inputs and its answer. Show shapes and row order before interpreting returned predictions.

Worked illustration / lecturer answer
X has four training rows and y has four targets. predictions.round(2) changes display precision; .tolist() converts a NumPy array to a Python list. Keep full-precision values for metrics when required.

Misconception to address
Rounding a displayed value is different from changing the values used for assessment. Do not shuffle X without applying the same reordering to y.

On this slide
Expression | Meaning
np.nan | A missing numeric value marker
X.shape | The array dimensions: rows, columns
predictions.round(2) | Round a new array to two decimal places
predictions.tolist() | Convert the array into a Python list
Use rounded values only for a labelled display. Keep full precision when the assignment requires it.

Continue to
Create an array before reading its shape

## Slide 17 — Create an array before reading its shape

Create an array before reading its shape
CML3113, Week 8, slide 17

Explanation to give
Explain an input matrix as a table of numbers with one observation per row and one feature per column. The target vector has one answer per observation in the same order.

Worked illustration / lecturer answer
[[1], [2], [3]] has shape (3, 1). [12, 14, 16] has shape (3,). For one new observation with two features, use [[2.5, 22]], not [2.5, 22].

Misconception to address
Swapping feature columns changes their meaning even if dimensions still match. The model expects the same order and units at prediction time.

On this slide
NumPy is a library for numerical arrays. import numpy as np makes its tools available through the name np.

An array stores a regular arrangement of values. np.array([[1], [2], [3]]) creates three rows with one value in each.

X.shape reports (3, 1): three rows, one column. np.array([12, 14, 16]) is one-dimensional; its shape is (3,). The comma marks a one-item tuple.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Rows, columns and named options

## Slide 18 — Rows, columns and named options

Rows, columns and named options
CML3113, Week 8, slide 18

Explanation to give
Explain an input matrix as a table of numbers with one observation per row and one feature per column. The target vector has one answer per observation in the same order.

Worked illustration / lecturer answer
[[1], [2], [3]] has shape (3, 1). [12, 14, 16] has shape (3,). For one new observation with two features, use [[2.5, 22]], not [2.5, 22].

Misconception to address
Swapping feature columns changes their meaning even if dimensions still match. The model expects the same order and units at prediction time.

Read the displayed code line by line
import numpy as np
Load this library. An alias after as is the shorter name used below.

X = np.array([[1], [2], [3]])
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

y = np.array([12, 14, 16])
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(X.shape)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(y.shape)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
X has three rows and one feature column. y has three target values.

Continue to
fit and predict

## Slide 19 — fit and predict

fit and predict
CML3113, Week 8, slide 19

Explanation to give
A model object starts without learned coefficients. fit uses paired training inputs and answers to learn its state. predict applies that saved state to input rows and returns estimates.

Worked illustration / lecturer answer
In the displayed four-row example, fitting learns a line with intercept 10 and slope 2. Predicting [[2.5]] gives [15.0]. No true answer for 2.5 is passed to predict.

Misconception to address
Creating LinearRegression() is not training. Calling predict before fit fails. An import makes a tool available; it does not run the model.

On this slide
fit and predict: fit learns from training inputs and targets. predict uses the fitted rule on new inputs without receiving their true targets.

Continue to
A model object keeps learned information

## Slide 20 — A model object keeps learned information

A model object keeps learned information
CML3113, Week 8, slide 20

Explanation to give
A model object starts without learned coefficients. fit uses paired training inputs and answers to learn its state. predict applies that saved state to input rows and returns estimates.

Worked illustration / lecturer answer
In the displayed four-row example, fitting learns a line with intercept 10 and slope 2. Predicting [[2.5]] gives [15.0]. No true answer for 2.5 is passed to predict.

Misconception to address
Creating LinearRegression() is not training. Calling predict before fit fails. An import makes a tool available; it does not run the model.

On this slide
Object and method: LinearRegression() creates a model object. A method is an operation on that object. model.fit(...) stores learned information; model.predict(...) uses it.
Options: An argument such as strategy="mean" names an option. A random seed fixes the starting state of random choices; it does not prove that a model is accurate.

Continue to
An object remembers its fitted state

## Slide 21 — An object remembers its fitted state

An object remembers its fitted state
CML3113, Week 8, slide 21

Explanation to give
A model object starts without learned coefficients. fit uses paired training inputs and answers to learn its state. predict applies that saved state to input rows and returns estimates.

Worked illustration / lecturer answer
In the displayed four-row example, fitting learns a line with intercept 10 and slope 2. Predicting [[2.5]] gives [15.0]. No true answer for 2.5 is passed to predict.

Misconception to address
Creating LinearRegression() is not training. Calling predict before fit fails. An import makes a tool available; it does not run the model.

On this slide
Python expression | What it means
model = LinearRegression() | Create an unfitted model object
model.fit(X_train, y_train) | Learn from paired training data
model.predict(X_new) | Use that learned state
random_state=17 | Name an option and set its value
An object holds state and has methods. A method is a function used through that object.

Continue to
Creating, fitting and predicting

## Slide 22 — Creating, fitting and predicting

Creating, fitting and predicting
CML3113, Week 8, slide 22

Explanation to give
A model object starts without learned coefficients. fit uses paired training inputs and answers to learn its state. predict applies that saved state to input rows and returns estimates.

Worked illustration / lecturer answer
In the displayed four-row example, fitting learns a line with intercept 10 and slope 2. Predicting [[2.5]] gives [15.0]. No true answer for 2.5 is passed to predict.

Misconception to address
Creating LinearRegression() is not training. Calling predict before fit fails. An import makes a tool available; it does not run the model.

On this slide
LinearRegression() creates a model that has not learned yet.

fit(X_train, y_train) learns from paired training examples.

predict(new_inputs) returns estimates. The actual targets are absent from new_inputs.

Continue to
Where the modelling tools come from

## Slide 23 — Where the modelling tools come from

Where the modelling tools come from
CML3113, Week 8, slide 23

Explanation to give
A model object starts without learned coefficients. fit uses paired training inputs and answers to learn its state. predict applies that saved state to input rows and returns estimates.

Worked illustration / lecturer answer
In the displayed four-row example, fitting learns a line with intercept 10 and slope 2. Predicting [[2.5]] gives [15.0]. No true answer for 2.5 is passed to predict.

Misconception to address
Creating LinearRegression() is not training. Calling predict before fit fails. An import makes a tool available; it does not run the model.

On this slide
scikit-learn is an installed machine-learning library. Its Python import name is sklearn. linear_model is the part containing LinearRegression.

from sklearn.linear_model import LinearRegression makes that model class available. LinearRegression() creates an individual model object.

In Colab this library is normally available. If an import fails, use the course setup instructions and retry the import before running model code.

Continue to
Regression models and errors in Python

## Slide 24 — Regression models and errors in Python

Regression models and errors in Python
CML3113, Week 8, slide 24

Explanation to give
A model object starts without learned coefficients. fit uses paired training inputs and answers to learn its state. predict applies that saved state to input rows and returns estimates.

Worked illustration / lecturer answer
In the displayed four-row example, fitting learns a line with intercept 10 and slope 2. Predicting [[2.5]] gives [15.0]. No true answer for 2.5 is passed to predict.

Misconception to address
Creating LinearRegression() is not training. Calling predict before fit fails. An import makes a tool available; it does not run the model.

Read the displayed code line by line
from sklearn.linear_model import LinearRegression
Bring the named tool from this library into the current Python session.

X_train = [[1], [2], [3], [4]]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

y_train = [12, 14, 16, 18]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

new_inputs = [[2.5]]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Regression models and errors in Python continued

## Slide 25 — Regression models and errors in Python continued

Regression models and errors in Python continued
CML3113, Week 8, slide 25

Explanation to give
A model object starts without learned coefficients. fit uses paired training inputs and answers to learn its state. predict applies that saved state to input rows and returns estimates.

Worked illustration / lecturer answer
In the displayed four-row example, fitting learns a line with intercept 10 and slope 2. Predicting [[2.5]] gives [15.0]. No true answer for 2.5 is passed to predict.

Misconception to address
Creating LinearRegression() is not training. Calling predict before fit fails. An import makes a tool available; it does not run the model.

Read the displayed code line by line
model = LinearRegression()
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

model.fit(X_train, y_train)
Learn from the supplied training rows and their aligned targets. This changes the fitted object’s state.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Regression models and errors in Python continued

## Slide 26 — Regression models and errors in Python continued

Regression models and errors in Python continued
CML3113, Week 8, slide 26

Explanation to give
A model object starts without learned coefficients. fit uses paired training inputs and answers to learn its state. predict applies that saved state to input rows and returns estimates.

Worked illustration / lecturer answer
In the displayed four-row example, fitting learns a line with intercept 10 and slope 2. Predicting [[2.5]] gives [15.0]. No true answer for 2.5 is passed to predict.

Misconception to address
Creating LinearRegression() is not training. Calling predict before fit fails. An import makes a tool available; it does not run the model.

Read the displayed code line by line
predictions = model.predict(new_inputs)
Apply the already fitted rule to these input rows without passing their true targets.

print(predictions.round(2).tolist())
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Regression models and errors results

## Slide 27 — Regression models and errors results

Regression models and errors results
CML3113, Week 8, slide 27

Explanation to give
A model object starts without learned coefficients. fit uses paired training inputs and answers to learn its state. predict applies that saved state to input rows and returns estimates.

Worked illustration / lecturer answer
In the displayed four-row example, fitting learns a line with intercept 10 and slope 2. Predicting [[2.5]] gives [15.0]. No true answer for 2.5 is passed to predict.

Misconception to address
Creating LinearRegression() is not training. Calling predict before fit fails. An import makes a tool available; it does not run the model.

On this slide
[15.0]

Continue to
The mean baseline

## Slide 28 — The mean baseline

The mean baseline
CML3113, Week 8, slide 28

Explanation to give
A baseline is a deliberately simple comparison. The training-mean baseline ignores input differences and always predicts the same number learned from training targets.

Worked illustration / lecturer answer
Targets 12, 14, 16 and 18 have mean 15. This baseline predicts 15 for input 2.5 and also for input 9. A more complex model must earn its extra complexity on held-out observations.

Misconception to address
Compute the mean from training targets only. A model matching the baseline at one point says nothing about which is better overall.

On this slide
Use the same training data.

This baseline learns their mean, 15, and predicts it for every input.

It gives a simple comparison before claiming the line helps.

Continue to
The mean baseline in Python

## Slide 29 — The mean baseline in Python

The mean baseline in Python
CML3113, Week 8, slide 29

Explanation to give
A baseline is a deliberately simple comparison. The training-mean baseline ignores input differences and always predicts the same number learned from training targets.

Worked illustration / lecturer answer
Targets 12, 14, 16 and 18 have mean 15. This baseline predicts 15 for input 2.5 and also for input 9. A more complex model must earn its extra complexity on held-out observations.

Misconception to address
Compute the mean from training targets only. A model matching the baseline at one point says nothing about which is better overall.

Read the displayed code line by line
from sklearn.dummy import DummyRegressor
Bring the named tool from this library into the current Python session.

baseline = DummyRegressor(strategy="mean")
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

baseline.fit(X_train, y_train)
Learn from the supplied training rows and their aligned targets. This changes the fitted object’s state.

print(baseline.predict(new_inputs).tolist())
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
A small regression tree

## Slide 30 — A small regression tree

A small regression tree
CML3113, Week 8, slide 30

Explanation to give
A regression tree asks learned threshold questions. Each path leads to a terminal group, or leaf, whose prediction is based on training targets in that group.

Worked illustration / lecturer answer
In the displayed toy tree, input 2.5 follows <= 2.5, then > 1.5, reaching prediction 14. The straight line gives 15 on the same input because it uses a different rule.

Misconception to address
Thresholds and leaf values depend on the training data. max_depth limits complexity; a fixed random_state helps repetition but does not certify accuracy.

On this slide
A tree learns threshold questions from the training inputs.

Each final group, or leaf, predicts a target value.

This tree returns 14 for input 2.5 in this toy example. max_depth limits the number of successive decisions. random_state fixes the random seed.

Continue to
Trace a regression-tree prediction

## Slide 31 — Trace a regression-tree prediction

Trace a regression-tree prediction
CML3113, Week 8, slide 31

Explanation to give
A regression tree asks learned threshold questions. Each path leads to a terminal group, or leaf, whose prediction is based on training targets in that group.

Worked illustration / lecturer answer
In the displayed toy tree, input 2.5 follows <= 2.5, then > 1.5, reaching prediction 14. The straight line gives 15 on the same input because it uses a different rule.

Misconception to address
Thresholds and leaf values depend on the training data. max_depth limits complexity; a fixed random_state helps repetition but does not certify accuracy.

On this slide
Input or question | Path for input 2.5 | Result
Is input at most 2.5? | Yes: use the lower group | Continue within that group
Is input at most 1.5? | No: use its upper leaf | Training target 14
Leaf prediction | Return the leaf value | 14
This trace describes our fitted four-row teaching tree. A different training set can produce different questions.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
A small regression tree in Python

## Slide 32 — A small regression tree in Python

A small regression tree in Python
CML3113, Week 8, slide 32

Explanation to give
A regression tree asks learned threshold questions. Each path leads to a terminal group, or leaf, whose prediction is based on training targets in that group.

Worked illustration / lecturer answer
In the displayed toy tree, input 2.5 follows <= 2.5, then > 1.5, reaching prediction 14. The straight line gives 15 on the same input because it uses a different rule.

Misconception to address
Thresholds and leaf values depend on the training data. max_depth limits complexity; a fixed random_state helps repetition but does not certify accuracy.

Read the displayed code line by line
from sklearn.tree import DecisionTreeRegressor
Bring the named tool from this library into the current Python session.

tree = DecisionTreeRegressor(max_depth=4, random_state=17)
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

tree.fit(X_train, y_train)
Learn from the supplied training rows and their aligned targets. This changes the fitted object’s state.

print(tree.predict(new_inputs).tolist())
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Reuse the same preparation on new inputs

## Slide 33 — Reuse the same preparation on new inputs

Reuse the same preparation on new inputs
CML3113, Week 8, slide 33

Explanation to give
A pipeline keeps preparation and prediction in one ordered procedure. Fit learns preparation values from training data and then fits the model. Prediction reuses those saved values.

Worked illustration / lecturer answer
For training feature values 20, 22, missing and 24, the learned median is 22. A missing value in a new observation also receives 22, without recalculating from the new observations.

Misconception to address
Filling all records before splitting leaks information. A pipeline avoids that only when its fit receives the correct training subset.

On this slide
Imputer: An imputer fills missing feature values using a stated rule. Fit learns the replacement from training observations only. Prediction reuses that stored replacement.
Pipeline: A pipeline connects preprocessing and a model. make_pipeline creates that connection. Its fit learns both stages on training data; predict applies them to new features.

Continue to
Read the pipeline tools before combining them

## Slide 34 — Read the pipeline tools before combining them

Read the pipeline tools before combining them
CML3113, Week 8, slide 34

Explanation to give
A pipeline keeps preparation and prediction in one ordered procedure. Fit learns preparation values from training data and then fits the model. Prediction reuses those saved values.

Worked illustration / lecturer answer
For training feature values 20, 22, missing and 24, the learned median is 22. A missing value in a new observation also receives 22, without recalculating from the new observations.

Misconception to address
Filling all records before splitting leaks information. A pipeline avoids that only when its fit receives the correct training subset.

On this slide
np.nan is NumPy’s missing-number marker. SimpleImputer(strategy="median") creates a tool that will learn each column’s median from training data.

make_pipeline(imputer, model) joins preparation to prediction in that order. pipeline.fit first learns and applies the imputer, then fits the model.

pipeline.predict applies the already learned imputer to new inputs before predicting. It does not recalculate medians from the new inputs.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Preprocessing learned from training only

## Slide 35 — Preprocessing learned from training only

Preprocessing learned from training only
CML3113, Week 8, slide 35

Explanation to give
A pipeline keeps preparation and prediction in one ordered procedure. Fit learns preparation values from training data and then fits the model. Prediction reuses those saved values.

Worked illustration / lecturer answer
For training feature values 20, 22, missing and 24, the learned median is 22. A missing value in a new observation also receives 22, without recalculating from the new observations.

Misconception to address
Filling all records before splitting leaks information. A pipeline avoids that only when its fit receives the correct training subset.

On this slide
SimpleImputer learns one median for each training column. make_pipeline connects this step to the model. fit learns both steps using only the training examples. predict reuses them on new inputs.

No target is supplied to predict.

The two inputs here are invented practice measurements.

Continue to
Trace the training-only fill step

## Slide 36 — Trace the training-only fill step

Trace the training-only fill step
CML3113, Week 8, slide 36

Explanation to give
A pipeline keeps preparation and prediction in one ordered procedure. Fit learns preparation values from training data and then fits the model. Prediction reuses those saved values.

Worked illustration / lecturer answer
For training feature values 20, 22, missing and 24, the learned median is 22. A missing value in a new observation also receives 22, without recalculating from the new observations.

Misconception to address
Filling all records before splitting leaks information. A pipeline avoids that only when its fit receives the correct training subset.

On this slide
Stage | Second feature values | Action
Training input | 20, 22, missing, 24 | Learn median 22
Training after filling | 20, 22, 22, 24 | Fit the model
New input | Missing second value | Fill with saved 22
No new median is learned during prediction. The model receives the prepared numeric row.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Preprocessing learned from training only in Python (1/2)

## Slide 37 — Preprocessing learned from training only in Python (1/2)

Preprocessing learned from training only in Python (1/2)
CML3113, Week 8, slide 37

Explanation to give
A pipeline keeps preparation and prediction in one ordered procedure. Fit learns preparation values from training data and then fits the model. Prediction reuses those saved values.

Worked illustration / lecturer answer
For training feature values 20, 22, missing and 24, the learned median is 22. A missing value in a new observation also receives 22, without recalculating from the new observations.

Misconception to address
Filling all records before splitting leaks information. A pipeline avoids that only when its fit receives the correct training subset.

Read the displayed code line by line
from sklearn.impute import SimpleImputer
Bring the named tool from this library into the current Python session.

from sklearn.pipeline import make_pipeline
Bring the named tool from this library into the current Python session.

import numpy as np
Load this library. An alias after as is the shorter name used below.

train_inputs = [[1, 20], [2, 22], [3, np.nan], [4, 24]]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

train_targets = [12, 14, 16, 18]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

imputer = SimpleImputer(strategy="median")
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

model = LinearRegression()
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

pipeline = make_pipeline(imputer, model)
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

pipeline.fit(train_inputs, train_targets)
Learn from the supplied training rows and their aligned targets. This changes the fitted object’s state.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Preprocessing learned from training only in Python (2/2)

## Slide 38 — Preprocessing learned from training only in Python (2/2)

Preprocessing learned from training only in Python (2/2)
CML3113, Week 8, slide 38

Explanation to give
A pipeline keeps preparation and prediction in one ordered procedure. Fit learns preparation values from training data and then fits the model. Prediction reuses those saved values.

Worked illustration / lecturer answer
For training feature values 20, 22, missing and 24, the learned median is 22. A missing value in a new observation also receives 22, without recalculating from the new observations.

Misconception to address
Filling all records before splitting leaks information. A pipeline avoids that only when its fit receives the correct training subset.

Read the displayed code line by line
predictions = pipeline.predict([[2.5, np.nan]])
Apply the already fitted rule to these input rows without passing their true targets.

print(predictions.round(2).tolist())
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Continue the SAME cell; keep indentation. Run after all parts are entered.

Continue to
Reading records into a feature table

## Slide 39 — Reading records into a feature table

Reading records into a feature table
CML3113, Week 8, slide 39

Explanation to give
Explain an input matrix as a table of numbers with one observation per row and one feature per column. The target vector has one answer per observation in the same order.

Worked illustration / lecturer answer
[[1], [2], [3]] has shape (3, 1). [12, 14, 16] has shape (3,). For one new observation with two features, use [[2.5, 22]], not [2.5, 22].

Misconception to address
Swapping feature columns changes their meaning even if dimensions still match. The model expects the same order and units at prediction time.

On this slide
Each inner list is one row, in the same order as the input records.

The target list uses that same row order.

The feature table has no answer column.

Continue to
Reading records into a feature table in Python

## Slide 40 — Reading records into a feature table in Python

Reading records into a feature table in Python
CML3113, Week 8, slide 40

Explanation to give
Explain an input matrix as a table of numbers with one observation per row and one feature per column. The target vector has one answer per observation in the same order.

Worked illustration / lecturer answer
[[1], [2], [3]] has shape (3, 1). [12, 14, 16] has shape (3,). For one new observation with two features, use [[2.5, 22]], not [2.5, 22].

Misconception to address
Swapping feature columns changes their meaning even if dimensions still match. The model expects the same order and units at prediction time.

Read the displayed code line by line
rows = [{"length": 2, "width": 3, "area": 6},
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

{"length": 4, "width": 5, "area": 20}]
This line continues the surrounding expression or block; read it together with the preceding line rather than running it alone.

X = []
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

y = []
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

for row in rows:
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

X.append([row["length"], row["width"]])
Evaluate the argument and add it as one new item at the end of this list.

y.append(row["area"])
Evaluate the argument and add it as one new item at the end of this list.

print(X)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(y)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
MAE and RMSE

## Slide 41 — MAE and RMSE

MAE and RMSE
CML3113, Week 8, slide 41

Explanation to give
Match each prediction with the actual value for the same observation. MAE averages error magnitudes. RMSE averages squared errors and then takes the square root, restoring the target unit.

Worked illustration / lecturer answer
Actual [10,20] and predicted [12,16] have differences -2 and 4. MAE is (2+4)/2 = 3. RMSE is sqrt((4+16)/2) = sqrt(10), about 3.1623.

Misconception to address
Signed errors can cancel if simply averaged. MAE is not a plus/minus guarantee for every case, and RMSE is not in squared units after the square root.

On this slide
MAE and RMSE: MAE averages absolute prediction errors. RMSE squares errors, averages them and takes the square root. Both use target units. RMSE is more sensitive to large errors.

Continue to
A prediction error in ordinary numbers

## Slide 42 — A prediction error in ordinary numbers

A prediction error in ordinary numbers
CML3113, Week 8, slide 42

Explanation to give
Match each prediction with the actual value for the same observation. MAE averages error magnitudes. RMSE averages squared errors and then takes the square root, restoring the target unit.

Worked illustration / lecturer answer
Actual [10,20] and predicted [12,16] have differences -2 and 4. MAE is (2+4)/2 = 3. RMSE is sqrt((4+16)/2) = sqrt(10), about 3.1623.

Misconception to address
Signed errors can cancel if simply averaged. MAE is not a plus/minus guarantee for every case, and RMSE is not in squared units after the square root.

On this slide
Actual | Prediction | Absolute error
10 | 8 | 2
20 | 24 | 4
MAE = (2 + 4) / 2 = 3, in the target’s unit. Compare a model against a training-only baseline.

Continue to
The operations in the error calculation

## Slide 43 — The operations in the error calculation

The operations in the error calculation
CML3113, Week 8, slide 43

Explanation to give
Match each prediction with the actual value for the same observation. MAE averages error magnitudes. RMSE averages squared errors and then takes the square root, restoring the target unit.

Worked illustration / lecturer answer
Actual [10,20] and predicted [12,16] have differences -2 and 4. MAE is (2+4)/2 = 3. RMSE is sqrt((4+16)/2) = sqrt(10), about 3.1623.

Misconception to address
Signed errors can cancel if simply averaged. MAE is not a plus/minus guarantee for every case, and RMSE is not in squared units after the square root.

On this slide
zip and paired names: zip(actual, predicted) pairs values at matching positions. for truth, guess in ... assigns each pair to two names. Here both lists must have the same nonzero length.
Square and square root: difference ** 2 squares an error. sqrt reverses a square for nonnegative numbers: sqrt(9) is 3. from math import sqrt makes this tool available.

Continue to
Pair two lists using zip

## Slide 44 — Pair two lists using zip

Pair two lists using zip
CML3113, Week 8, slide 44

Explanation to give
zip pairs items at matching positions. Explain each pair as one observation's truth and prediction, then unpack it into two names.

Worked illustration / lecturer answer
Actual [10,20] with predicted [12,16] produces (10,12), then (20,16). Reversing one list would compare the wrong observations without necessarily causing a Python error.

Misconception to address
zip stops at the shorter input. For error metrics, validate matching nonzero lengths so observations are not silently ignored.

On this slide
zip(actual, predicted) visits matching positions together. for truth, guess in zip(...): unpacks each pair into two names.

For actual [10, 20] and predicted [12, 16], the pairs are (10, 12) and (20, 16). They describe the same observations in the same order.

zip stops at the shorter input. Check equal, nonzero lengths for these error calculations; otherwise a result could ignore observations.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Inspect the pairs before measuring errors

## Slide 45 — Inspect the pairs before measuring errors

Inspect the pairs before measuring errors
CML3113, Week 8, slide 45

Explanation to give
zip pairs items at matching positions. Explain each pair as one observation's truth and prediction, then unpack it into two names.

Worked illustration / lecturer answer
Actual [10,20] with predicted [12,16] produces (10,12), then (20,16). Reversing one list would compare the wrong observations without necessarily causing a Python error.

Misconception to address
zip stops at the shorter input. For error metrics, validate matching nonzero lengths so observations are not silently ignored.

Read the displayed code line by line
actual = [10, 20]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

predicted = [12, 16]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

for truth, guess in zip(actual, predicted):
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

print(truth, guess)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Output: 10 12; 20 16

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Trace absolute and squared errors

## Slide 46 — Trace absolute and squared errors

Trace absolute and squared errors
CML3113, Week 8, slide 46

Explanation to give
Match each prediction with the actual value for the same observation. MAE averages error magnitudes. RMSE averages squared errors and then takes the square root, restoring the target unit.

Worked illustration / lecturer answer
Actual [10,20] and predicted [12,16] have differences -2 and 4. MAE is (2+4)/2 = 3. RMSE is sqrt((4+16)/2) = sqrt(10), about 3.1623.

Misconception to address
Signed errors can cancel if simply averaged. MAE is not a plus/minus guarantee for every case, and RMSE is not in squared units after the square root.

On this slide
Actual and predicted | Absolute error | Squared error
10 and 12 | abs(-2) = 2 | (-2) ** 2 = 4
20 and 16 | abs(4) = 4 | 4 ** 2 = 16
Average | (2 + 4) / 2 = 3 | (4 + 16) / 2 = 10
MAE is 3. RMSE is sqrt(10), approximately 3.1623. sqrt means the nonnegative square root.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Two error measures

## Slide 47 — Two error measures

Two error measures
CML3113, Week 8, slide 47

Explanation to give
Match each prediction with the actual value for the same observation. MAE averages error magnitudes. RMSE averages squared errors and then takes the square root, restoring the target unit.

Worked illustration / lecturer answer
Actual [10,20] and predicted [12,16] have differences -2 and 4. MAE is (2+4)/2 = 3. RMSE is sqrt((4+16)/2) = sqrt(10), about 3.1623.

Misconception to address
Signed errors can cancel if simply averaged. MAE is not a plus/minus guarantee for every case, and RMSE is not in squared units after the square root.

On this slide
zip pairs corresponding values. abs measures error size.

Squaring emphasises large errors; taking the square root returns to the original unit.

These functions assume equal-length, nonempty paired observations.

Continue to
Two error measures in Python (1/2)

## Slide 48 — Two error measures in Python (1/2)

Two error measures in Python (1/2)
CML3113, Week 8, slide 48

Explanation to give
Match each prediction with the actual value for the same observation. MAE averages error magnitudes. RMSE averages squared errors and then takes the square root, restoring the target unit.

Worked illustration / lecturer answer
Actual [10,20] and predicted [12,16] have differences -2 and 4. MAE is (2+4)/2 = 3. RMSE is sqrt((4+16)/2) = sqrt(10), about 3.1623.

Misconception to address
Signed errors can cancel if simply averaged. MAE is not a plus/minus guarantee for every case, and RMSE is not in squared units after the square root.

Read the displayed code line by line
from math import sqrt
Bring the named tool from this library into the current Python session.

a = [10, 20]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

p = [12, 16]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

absolute = []
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

squared = []
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

for truth, guess in zip(a, p):
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

difference = truth - guess
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

absolute.append(abs(difference))
Evaluate the argument and add it as one new item at the end of this list.

squared.append(difference ** 2)
Evaluate the argument and add it as one new item at the end of this list.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Two error measures in Python (2/2)

## Slide 49 — Two error measures in Python (2/2)

Two error measures in Python (2/2)
CML3113, Week 8, slide 49

Explanation to give
Match each prediction with the actual value for the same observation. MAE averages error magnitudes. RMSE averages squared errors and then takes the square root, restoring the target unit.

Worked illustration / lecturer answer
Actual [10,20] and predicted [12,16] have differences -2 and 4. MAE is (2+4)/2 = 3. RMSE is sqrt((4+16)/2) = sqrt(10), about 3.1623.

Misconception to address
Signed errors can cancel if simply averaged. MAE is not a plus/minus guarantee for every case, and RMSE is not in squared units after the square root.

Read the displayed code line by line
print(sum(absolute) / len(a))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(sqrt(sum(squared) / len(a)))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Continue the SAME cell; keep indentation. Run after all parts are entered.

Continue to
R² compares against a mean prediction

## Slide 50 — R² compares against a mean prediction

R² compares against a mean prediction
CML3113, Week 8, slide 50

Explanation to give
Explain R² as a comparison of squared prediction errors with a reference that always predicts the mean of the evaluated targets. It is a relative score, not a percentage of correct predictions.

Worked illustration / lecturer answer
R² = 1 means zero error on these observations. R² = 0 matches that mean reference. A negative value means larger squared error than the reference.

Misconception to address
Do not translate 0.8 into “80% accurate”. Constant targets need special handling, and engineering usefulness still depends on errors in physical units.

On this slide
R² compares squared errors with predicting the mean of the evaluated targets. It is a score, not “percentage accuracy”.

1 means perfect predictions on those observations. 0 matches that mean-prediction reference; a negative score can be worse.

Use the same evaluation observations and report the specified error metric with its units. Constant targets need special handling; this score alone does not prove usefulness.

Continue to
Revision example and answer

## Slide 51 — Revision example and answer

Revision example and answer
CML3113, Week 8, slide 51

Explanation to give
Use the displayed example as a short individual revision question, then explain the reasoning behind its answer.

Worked illustration / lecturer answer
Example: On paper compare actual [10, 20] with predictions [12, 16]. Find MAE and RMSE. Is MAE a plus/minus guarantee for each prediction?

Answer: Absolute errors are 2 and 4: MAE 3. Squared errors 4 and 16: RMSE sqrt(10), about 3.162. MAE is an average, not an individual error bound.

Misconception to address
Trace the operation that changes the value rather than accepting a memorised output. For notebook-state examples, specify which cell is repeated and whether the initialisation ran again.

Continue to
Preparing for the assignment

## Slide 52 — Preparing for the assignment

Preparing for the assignment
CML3113, Week 8, slide 52

Explanation to give
Explain the order: partition data using the stated protocol, fit preparation on training data, fit models, compare on validation data and leave final test data untouched until choices are fixed.

Worked illustration / lecturer answer
Compare models on identical held-out observations with the same metric and preprocessing rules. Each cross-validation training fold learns its own preparation values.

Misconception to address
A written claim of no leakage must agree with the executable split and fitting code. Follow the published execution requirement for any criterion linked to the split check.

On this slide
W08 asks for baseline, linear and depth-4 tree prediction lists plus error metrics.

Fit missing-value replacement on training data.

A Pipeline joins preprocessing to the model.

Only load_pct and ambient_c are predictors.

Continue to
Preparing for the assignment continued

## Slide 53 — Preparing for the assignment continued

Preparing for the assignment continued
CML3113, Week 8, slide 53

Explanation to give
Keep related equipment observations together so the validation really represents equipment the model has not seen.

Worked illustration / lecturer answer
The written question may supply a comparison scenario. Label those numbers as supplied scenario evidence; do not claim they came from a run of your own notebook.

Misconception to address
A supplied scenario and an observed experimental result have different provenance. Both can be interpreted, but should not be confused.

On this slide
Keep observations from the same equipment in one partition.

The written comparison supplies scenario values.

Distinguish them from your own measured results.

Continue to
Reading model outputs

## Slide 54 — Reading model outputs

Reading model outputs
CML3113, Week 8, slide 54

Explanation to give
Read the result in the target's physical unit and identify which observations produced the score. Training fit and evaluation on unseen observations answer different questions.

Worked illustration / lecturer answer
A predicted-versus-actual plot has perfect agreement along the diagonal. Points systematically above or below it suggest bias to investigate. Compare errors with the stated baseline on the same cases.

Misconception to address
A good score without a clear sample, split and unit cannot support an engineering recommendation.

On this slide
A score on training rows describes training fit.

A feature table must preserve the training column names, order and units during prediction.

A one-dimensional list may have the wrong shape for a model expecting rows and columns.

A predicted-versus-actual plot uses the diagonal as perfect agreement; a pattern is not proof of causation.

Continue to
Reading model outputs continued

## Slide 55 — Reading model outputs continued

Reading model outputs continued
CML3113, Week 8, slide 55

Explanation to give
Read the result in the target's physical unit and identify which observations produced the score. Training fit and evaluation on unseen observations answer different questions.

Worked illustration / lecturer answer
A predicted-versus-actual plot has perfect agreement along the diagonal. Points systematically above or below it suggest bias to investigate. Compare errors with the stated baseline on the same cases.

Misconception to address
A good score without a clear sample, split and unit cannot support an engineering recommendation.

On this slide
Judge MAE against the baseline and the decision’s acceptable error.

R² is not an accuracy percentage.

Continue to
Your issued task

## Slide 56 — Your issued task

Your issued task
CML3113, Week 8, slide 56

Explanation to give
Name this cohort’s target and its unit exactly as displayed. Each row is one operating observation, while equipment_id can repeat across several observations.

Worked illustration / lecturer answer
Explain record_id as the identifier of an observation, load_pct as load expressed in percent and ambient_c as temperature in degrees Celsius. The target records the known answer in training data.

Misconception to address
These are synthetic examples for learning. They do not establish a calibrated physical relationship or justify operation of real equipment.

On this slide
Investigate crusher energy demand.

Target units: kWh/t.

These are synthetic teaching records, not measurements suitable for deployment.

Each record is one operating observation; equipment_id repeats across observations.

Continue to
predict_regression(training_records, feature_records)

## Slide 57 — predict_regression(training_records, feature_records)

predict_regression(training_records, feature_records)
CML3113, Week 8, slide 57

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
regression_errors(actual, predicted)

## Slide 58 — regression_errors(actual, predicted)

regression_errors(actual, predicted)
CML3113, Week 8, slide 58

Explanation to give
Pair actual and predicted values by position. Return mae and rmse with full numerical precision.

Worked illustration / lecturer answer
On separate teaching pairs with errors 2 and 4, MAE is 3 and RMSE is sqrt(10). Rounding is for a labelled display, not for the returned metric.

Misconception to address
Keep the exact output names and required types. Use the task text for the learner’s own assessed answer; the alternate example explains the method without replacing their work.

On this slide
Return mae and rmse, calculated over the same paired observations, with full precision.

Continue to
Written evidence

## Slide 59 — Written evidence

Written evidence
CML3113, Week 8, slide 59

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
Regression and baseline submission

## Slide 60 — Regression and baseline submission

Regression and baseline submission
CML3113, Week 8, slide 60

Explanation to give
This slide hands over CML3113 W08. Show the exact form title before uploading. The required packet is one completed .ipynb notebook.

Worked illustration / lecturer answer
The recorded cutoff for this form is 2026-11-06T08:00:00+03:00. Check the live form for later changes. A replacement must contain the complete required file set, not just the changed file.

Misconception to address
Students enter their own Student Registration Number as required freeform text. They wait for filenames to appear, press Submit and keep the confirmation. A file saved in Drive or GitHub is not itself a form submission.

On this slide
Opens: 30 Oct 2026, 08:00 Kampala

Deadline: 06 Nov 2026, 08:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

Continue to
Data analysis project

## Slide 61 — Data analysis project

Data analysis project
CML3113, Week 8, slide 61

Explanation to give
Show the actual markdown answer cell headed My written evidence. This is where the learner explains the choices and the supplied scenario in their own words.

Worked illustration / lecturer answer
A useful explanation connects a decision to a named result and its limitation: for example, why a training-only median avoids using evaluation information. Describe supplied scenario figures as supplied, not as measurements the learner produced.

Misconception to address
Prompts and copied code comments do not substitute for the learner’s reasoning. Weekly work and tests use the notebook; projects also require their separate readable report.

On this slide
Write your own explanation in the markdown cell headed `## My written evidence`.

Keep that heading.

Task prompts and code comments are excluded from reasoning marks.

Complete every original rubric criterion below, not just the checked functions.

Continue to
Data analysis project continued

## Slide 62 — Data analysis project continued

Data analysis project continued
CML3113, Week 8, slide 62

Explanation to give
A chart must answer a stated question and show the actual data result. Explain what one mark represents and label both the quantity and unit before stating the finding.

Worked illustration / lecturer answer
A useful caption names the group or sample, the observed difference and the relevant unit. A limitation states what the plotted observations cannot establish, such as causation or performance at a new site.

Misconception to address
Text claiming “a chart was made” is not the required chart. Check the exact number and kinds required on this slide and in the assessment guide.

On this slide
Include profiling, justified cleaning, question-led charts and your engineering recommendation where required.

Keep raw data.

State units and distinguish correlation from causation.

Charts must be actual labelled figures in the notebook, not claims that charts exist.

Continue to
Data analysis project continued

## Slide 63 — Data analysis project continued

Data analysis project continued
CML3113, Week 8, slide 63

Explanation to give
Problem framing begins with a bounded engineering decision and a defined target. Provenance explains where observations came from; a licence states what reuse is allowed.

Worked illustration / lecturer answer
State the population, measurement period, units and who collected the data. Explain how those observations could answer the chosen question rather than merely describing an interesting file.

Misconception to address
Synthetic teaching data must be labelled as synthetic. A plausible story does not establish that a dataset contains the information or permissions the proposed project needs.

On this slide
Include captions and a separate readable DOCX/PDF report.

Question & dataset fit (20.0 total): A real engineering question is stated, and the chosen dataset can actually answer it.

Provenance and licence stated.

Data quality work (25.0 total): Defects found and handled with written justification.

Continue to
Data analysis project continued

## Slide 64 — Data analysis project continued

Data analysis project continued
CML3113, Week 8, slide 64

Explanation to give
A chart must answer a stated question and show the actual data result. Explain what one mark represents and label both the quantity and unit before stating the finding.

Worked illustration / lecturer answer
A useful caption names the group or sample, the observed difference and the relevant unit. A limitation states what the plotted observations cannot establish, such as causation or performance at a new site.

Misconception to address
Text claiming “a chart was made” is not the required chart. Check the exact number and kinds required on this slide and in the assessment guide.

On this slide
A data quality statement is present.

Analysis & visualisation (30.0 total): Four or more charts, each answering a stated question.

Correct chart types, labelled axes, findings in the captions.

Findings & interpretation (20.0 total): Conclusions supported by the analysis, stated in engineering terms, with limitations acknowledged.

Continue to
Data analysis project continued

## Slide 65 — Data analysis project continued

Data analysis project continued
CML3113, Week 8, slide 65

Explanation to give
Make contribution evidence specific enough to check. A seed records the starting state of random choices; a contribution log records who produced and explained which work.

Worked illustration / lecturer answer
Name a file, function or chart and the decision behind it. Match that entry to meaningful repository history. Disclose AI assistance according to the assessment policy.

Misconception to address
Many commits do not necessarily mean substantial work, and a seed does not establish accuracy. Both are supporting evidence, not replacements for the analysis.

On this slide
Individual contribution log (5.0 total): Present, specific, and consistent with the repository's commit history.

Continue to
Data analysis project submission

## Slide 66 — Data analysis project submission

Data analysis project submission
CML3113, Week 8, slide 66

Explanation to give
This slide hands over CML3113 DA_PROJECT. Show the exact form title before uploading. The required packet is the completed project notebook together with one readable DOCX or selectable-text PDF report.

Worked illustration / lecturer answer
The recorded cutoff for this form is 2026-10-30T08:00:00+03:00. Check the live form for later changes. A replacement must contain the complete required file set, not just the changed file.

Misconception to address
Students enter their own Student Registration Number as required freeform text. They wait for filenames to appear, press Submit and keep the confirmation. A file saved in Drive or GitHub is not itself a form submission.

On this slide
Opens: 09 Oct 2026, 08:00 Kampala

Deadline: 30 Oct 2026, 08:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

Continue to
Week 8 quiz

## Slide 67 — Week 8 quiz

Week 8 quiz
CML3113, Week 8, slide 67

Explanation to give
This is the CML3113 Week 8 quiz. The student link opens the response form; it does not activate its window. In Quiz Controls use open_W8_CML3113 when ready and read the logged closing time.

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

## Slide 68 — Revision and submission checklist

Revision and submission checklist
CML3113, Week 8, slide 68

Explanation to give
Introduce a fitted predictor only after identifying its inputs and known answers. Compare it with a simple baseline and explain its errors in target units.

Worked illustration / lecturer answer
The teaching line through (1,12), (2,14), (3,16), (4,18) predicts 15 at input 2.5. One neat example does not establish real-world accuracy.

Misconception to address
Close by identifying the actual saved file and its correct submission route. Read the live deadline. For current weekly notebook tasks, students upload their own work, not the practice notebook, ZIP or grading files.

On this slide
You can calculate one error and explain why evaluation needs unseen observations.

Save your work and check the required submission files.

Continue to
Optional revision video

## Slide 69 — Optional revision video

Optional revision video
CML3113, Week 8, slide 69

Explanation to give
Give the viewing question before playing the excerpt: How can a fitted line turn an input into a numerical prediction?

Worked illustration / lecturer answer
Use the adjacent worked example as the explanation if the video cannot load. Pause after the relevant example and connect its terms to the names and units already used in this lesson. Preview the displayed link and excerpt before class.

Misconception to address
The video is supporting revision, not a replacement for defining the symbols or a requirement to watch a full tutorial during limited class time.

On this slide
For revision after class.

StatQuest with Josh Starmer
The Essence of Linear Regression!!!

Opening up to 04:00, optional preview-selected excerpt

Listening question: How can a fitted line turn an input into a numerical prediction?

Reference / existing resource
https://www.youtube.com/watch?v=aFDOzpTeg0s
