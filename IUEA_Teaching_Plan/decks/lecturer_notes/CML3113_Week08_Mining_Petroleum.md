# CML3113 Week08 Mining Petroleum

Lecturer companion to the revised PowerPoint. Slide numbers match this edition. Explain the worked examples directly; revision checks are for individual study.

## Slide 1 — A first prediction model

PURPOSE
A first prediction model

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
Previous slide: A first prediction model.

EXPLAIN
Identify prediction inputs and a measured target.

Fit a simple model and compare prediction errors.

LECTURER CUE
Ask learners to explain this goal in ordinary language. The first successful attempt matters more than covering optional extensions. Defer: Deriving least squares, leaderboard competition, many residual plots and coefficient inference are reference. R² may be negative and is not an accuracy percentage.

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
Weeks 3–6 supplied Python, tables, cleaning and charts. We now use paired inputs and known answers to fit a prediction rule.

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
A regression model predicts a numerical engineering target from measurements available beforehand. The small invented data explain the code; they do not establish real-world accuracy.

LECTURER CUE
A pump team records temperature to investigate operation. Mining students can relate this to a dewatering pump; petroleum students to a transfer pump. These are teaching examples, not operating limits.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A numerical prediction.

REFERENCES


## Slide 5 — A numerical prediction

PURPOSE
A numerical prediction

CONNECT
Previous slide: Why this week’s tools are needed.

EXPLAIN
Regression predicts a number, such as cooling load in kW.

A feature is information available when predicting.

The target is the measured answer used during training.

Classification, next week, predicts a category.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Feature and target and Training validation and test.

REFERENCES


## Slide 6 — Feature and target and Training validation and test

PURPOSE
Feature and target and Training validation and test

CONNECT
Previous slide: A numerical prediction.

EXPLAIN
Feature and target: Features are inputs available when making a prediction. The target is the quantity we want to predict.

Training validation and test: Training fits the model. Validation helps choose it. The final test estimates performance after choices are fixed. Repeated equipment must stay in the same partition when assessing unseen equipment.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Baseline.

REFERENCES


## Slide 7 — Baseline

PURPOSE
Baseline

CONNECT
Previous slide: Feature and target and Training validation and test.

EXPLAIN
Baseline: A simple reference prediction. A training-mean baseline predicts the same training mean for every new example.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Linear model and tree.

REFERENCES


## Slide 8 — Linear model and tree

PURPOSE
Linear model and tree

CONNECT
Previous slide: Baseline.

EXPLAIN
Linear model and tree: A linear model combines inputs with learned weights. A regression tree asks feature-threshold questions and predicts a value at each leaf.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
What learning means in this example.

REFERENCES


## Slide 9 — What learning means in this example

PURPOSE
What learning means in this example

CONNECT
Previous slide: Linear model and tree.

EXPLAIN
Training supplies inputs and their known answers.

The model uses those examples to choose its internal numbers.

Prediction applies the fitted model to inputs whose answer we want to estimate.

LECTURER CUE
Use the small invented table below solely to see fit and predict. Real training needs more data, representative evaluation and careful partitioning.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Training observations.

REFERENCES


## Slide 10 — Training observations

PURPOSE
Training observations

CONNECT
Previous slide: What learning means in this example.

EXPLAIN
Input | Measured target

1 | 12

2 | 14

3 | 16

4 | 18

Invented numbers for learning.

LECTURER CUE
Invented numbers for learning. The fitted line predicts 15 at input 2.5. The training mean is also 15 at this one example, so it cannot establish superiority.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A fitted line is a numerical rule.

REFERENCES


## Slide 11 — A fitted line is a numerical rule

PURPOSE
A fitted line is a numerical rule

CONNECT
Previous slide: Training observations.

EXPLAIN
For these invented observations, target = 2 × input + 10 matches all four points. 2 is the slope; 10 is the intercept, the value at input zero.

A prediction error is the difference between a prediction and the measured answer. A vertical gap in the picture shows that error.

Fitting chooses the slope and intercept to minimise summed squared errors. Squaring means multiplying an error by itself; a small training error still needs an unseen-data check.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Fitting a line to observations.

REFERENCES


## Slide 12 — Fitting a line to observations

PURPOSE
Fitting a line to observations

CONNECT
Previous slide: A fitted line is a numerical rule.

EXPLAIN
The fitted line minimises the sum of squared vertical errors.

LECTURER CUE
These are illustrative concrete observations. Point to x, y, one prediction and one residual. A unique slope requires variation in x. A low training error alone does not show generalisation.
Source: existing course illustration figs/fit_by_eye.png. These are illustrative examples, not this cohort’s assessed results.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Rows must stay paired with their answers.

REFERENCES
Source: existing course illustration figs/fit_by_eye.png. These are illustrative examples, not this cohort’s assessed results.

## Slide 13 — Rows must stay paired with their answers

PURPOSE
Rows must stay paired with their answers

CONNECT
Previous slide: Fitting a line to observations.

EXPLAIN
Each inner list in X_train is one observation.

y_train contains one target value for each row, in the same order.

Changing the order of only one list attaches answers to the wrong observations.

LECTURER CUE
A list of lists is a table: each inner list holds the features of one observation. y_train holds one target per training row in the same order. Never reorder one without the other.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A matrix is a rectangular table of numbers.

REFERENCES


## Slide 14 — A matrix is a rectangular table of numbers

PURPOSE
A matrix is a rectangular table of numbers

CONNECT
Previous slide: Rows must stay paired with their answers.

EXPLAIN
A matrix has rows and columns. For modelling, one row is one observation and each column is one input feature.

[[1, 20], [2, 22]] has two rows and two columns. The outer list contains rows; each inner list contains that row’s features.

X is a conventional name for this input table. y holds one known target per row. These names have no special power in Python.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Rows and arrays before model code.

REFERENCES


## Slide 15 — Rows and arrays before model code

PURPOSE
Rows and arrays before model code

CONNECT
Previous slide: A matrix is a rectangular table of numbers.

EXPLAIN
Nested lists: [[1], [2], [3]] has three inner lists: three rows with one feature each. [12, 14, 16] has one target per row in the same order.

NumPy and array: NumPy is a numerical library; np is its short imported name. np.array(...) builds an array. shape reports its dimensions. np.nan represents a missing numerical value.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Reading NumPy results.

REFERENCES


## Slide 16 — Reading NumPy results

PURPOSE
Reading NumPy results

CONNECT
Previous slide: Rows and arrays before model code.

EXPLAIN
Expression | Meaning

np.nan | A missing numeric value marker

X.shape | The array dimensions: rows, columns

predictions.round(2) | Round a new array to two decimal places

predictions.tolist() | Convert the array into a Python list

Use rounded values only for a labelled display. Keep full precision when the assignment requires it.

LECTURER CUE
Read one row at a time and use a changed value. This is a syntax reference for the worked examples.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Create an array before reading its shape.

REFERENCES


## Slide 17 — Create an array before reading its shape

PURPOSE
Create an array before reading its shape

CONNECT
Previous slide: Reading NumPy results.

EXPLAIN
NumPy is a library for numerical arrays. import numpy as np makes its tools available through the name np.

An array stores a regular arrangement of values. np.array([[1], [2], [3]]) creates three rows with one value in each.

X.shape reports (3, 1): three rows, one column. np.array([12, 14, 16]) is one-dimensional; its shape is (3,). The comma marks a one-item tuple.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Rows, columns and named options.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 18 — Rows, columns and named options

PURPOSE
Rows, columns and named options

CONNECT
Previous slide: Create an array before reading its shape.

EXPLAIN
Read the code in this order:
import numpy as np
X = np.array([[1], [2], [3]])
y = np.array([12, 14, 16])
print(X.shape)
print(y.shape)

import loads a library. from selects a tool from it.

print displays a value below the cell.

Square brackets create a list or select an item.

X has three rows and one feature column. y has three target values.

LECTURER CUE
Read each symbol before running. Ask everyone to predict. Expected output: (3, 1) then (3,). Explain nested brackets before model.fit(X, y). Keyword arguments such as random_state=42 name an option.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
fit and predict.

REFERENCES


## Slide 19 — fit and predict

PURPOSE
fit and predict

CONNECT
Previous slide: Rows, columns and named options.

EXPLAIN
fit and predict: fit learns from training inputs and targets. predict uses the fitted rule on new inputs without receiving their true targets.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A model object keeps learned information.

REFERENCES


## Slide 20 — A model object keeps learned information

PURPOSE
A model object keeps learned information

CONNECT
Previous slide: fit and predict.

EXPLAIN
Object and method: LinearRegression() creates a model object. A method is an operation on that object. model.fit(...) stores learned information; model.predict(...) uses it.

Options: An argument such as strategy="mean" names an option. A random seed fixes the starting state of random choices; it does not prove that a model is accurate.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
An object remembers its fitted state.

REFERENCES


## Slide 21 — An object remembers its fitted state

PURPOSE
An object remembers its fitted state

CONNECT
Previous slide: A model object keeps learned information.

EXPLAIN
Python expression | What it means

model = LinearRegression() | Create an unfitted model object

model.fit(X_train, y_train) | Learn from paired training data

model.predict(X_new) | Use that learned state

random_state=17 | Name an option and set its value

An object holds state and has methods. A method is a function used through that object.

LECTURER CUE
Read one row at a time and use a changed value. This is a syntax reference for the worked examples.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Creating, fitting and predicting.

REFERENCES


## Slide 22 — Creating, fitting and predicting

PURPOSE
Creating, fitting and predicting

CONNECT
Previous slide: An object remembers its fitted state.

EXPLAIN
LinearRegression() creates a model that has not learned yet.

fit(X_train, y_train) learns from paired training examples.

predict(new_inputs) returns estimates. The actual targets are absent from new_inputs.

LECTURER CUE
Read imports and model creation separately. The model line creates an unfitted object. fit learns; predict applies. Explain the shallow tree now because the W08 assignment asks for it, then revisit classification trees in Week 9.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Where the modelling tools come from.

REFERENCES


## Slide 23 — Where the modelling tools come from

PURPOSE
Where the modelling tools come from

CONNECT
Previous slide: Creating, fitting and predicting.

EXPLAIN
scikit-learn is an installed machine-learning library. Its Python import name is sklearn. linear_model is the part containing LinearRegression.

from sklearn.linear_model import LinearRegression makes that model class available. LinearRegression() creates an individual model object.

In Colab this library is normally available. If an import fails, use the course setup instructions and retry the import before running model code.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Worked example.

REFERENCES


## Slide 24 — Regression models and errors in Python

PURPOSE
Regression models and errors in Python

CONNECT
Previous slide: Where the modelling tools come from.

EXPLAIN
Read the code in this order:
from sklearn.linear_model import LinearRegression
X_train = [[1], [2], [3], [4]]
y_train = [12, 14, 16, 18]
new_inputs = [[2.5]]

import loads a library. from selects a tool from it.

Square brackets create a list or select an item.

= assigns the value on the right to the name on the left.

Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER CUE
Use the small invented table below solely to see fit and predict. Real training needs more data, representative evaluation and careful partitioning. A list of lists is a table: each inner list holds the features of one observation. y_train holds one target per training row in the same order. Never reorder one without the other. Read imports and model creation separately. The model line creates an unfitted object. fit learns; predict applies. Explain the shallow tree now because the W08 assignment asks for it, then revisit classification trees in Week 9.

Complete practice code:
from sklearn.linear_model import LinearRegression
X_train = [[1], [2], [3], [4]]
y_train = [12, 14, 16, 18]
new_inputs = [[2.5]]

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Worked example continued.

REFERENCES


## Slide 25 — Regression models and errors in Python continued

PURPOSE
Regression models and errors in Python continued

CONNECT
Previous slide: Regression models and errors in Python.

EXPLAIN
Read the code in this order:
model = LinearRegression()
model.fit(X_train, y_train)

fit learns using the supplied training observations.

= assigns the value on the right to the name on the left.

Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER CUE
Use the small invented table below solely to see fit and predict. Real training needs more data, representative evaluation and careful partitioning. A list of lists is a table: each inner list holds the features of one observation. y_train holds one target per training row in the same order. Never reorder one without the other. Read imports and model creation separately. The model line creates an unfitted object. fit learns; predict applies. Explain the shallow tree now because the W08 assignment asks for it, then revisit classification trees in Week 9.

Complete practice code:
model = LinearRegression()
model.fit(X_train, y_train)

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Worked example continued.

REFERENCES


## Slide 26 — Regression models and errors in Python continued

PURPOSE
Regression models and errors in Python continued

CONNECT
Previous slide: Regression models and errors in Python continued.

EXPLAIN
Read the code in this order:
predictions = model.predict(new_inputs)
print(predictions.round(2).tolist())

predict applies the fitted model to new inputs.

print displays a value below the cell.

= assigns the value on the right to the name on the left.

Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER CUE
Use the small invented table below solely to see fit and predict. Real training needs more data, representative evaluation and careful partitioning. A list of lists is a table: each inner list holds the features of one observation. y_train holds one target per training row in the same order. Never reorder one without the other. Read imports and model creation separately. The model line creates an unfitted object. fit learns; predict applies. Explain the shallow tree now because the W08 assignment asks for it, then revisit classification trees in Week 9.

Complete practice code:
predictions = model.predict(new_inputs)
print(predictions.round(2).tolist())

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Expected output.

REFERENCES


## Slide 27 — Regression models and errors results

PURPOSE
Regression models and errors results

CONNECT
Previous slide: Regression models and errors in Python continued.

EXPLAIN
[15.0]

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
The mean baseline.

REFERENCES


## Slide 28 — The mean baseline

PURPOSE
The mean baseline

CONNECT
Previous slide: Regression models and errors results.

EXPLAIN
Use the same training data.

This baseline learns their mean, 15, and predicts it for every input.

It gives a simple comparison before claiming the line helps.

LECTURER CUE
Use the same training data. This baseline learns their mean, 15, and predicts it for every input. It gives a simple comparison before claiming the line helps.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
The mean baseline in Python.

REFERENCES


## Slide 29 — The mean baseline in Python

PURPOSE
The mean baseline in Python

CONNECT
Previous slide: The mean baseline.

EXPLAIN
Read the code in this order:
from sklearn.dummy import DummyRegressor
baseline = DummyRegressor(strategy="mean")
baseline.fit(X_train, y_train)
print(baseline.predict(new_inputs).tolist())

import loads a library. from selects a tool from it.

fit learns using the supplied training observations.

predict applies the fitted model to new inputs.

Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER CUE
Use the same training data. This baseline learns their mean, 15, and predicts it for every input. It gives a simple comparison before claiming the line helps.

Complete practice code:
from sklearn.dummy import DummyRegressor
baseline = DummyRegressor(strategy="mean")
baseline.fit(X_train, y_train)
print(baseline.predict(new_inputs).tolist())

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A small regression tree.

REFERENCES


## Slide 30 — A small regression tree

PURPOSE
A small regression tree

CONNECT
Previous slide: The mean baseline in Python.

EXPLAIN
A tree learns threshold questions from the training inputs.

Each final group, or leaf, predicts a target value.

This tree returns 14 for input 2.5 in this toy example. max_depth limits the number of successive decisions. random_state fixes the random seed.

LECTURER CUE
A tree learns threshold questions from the training inputs. Each final group, or leaf, predicts a target value. This tree returns 14 for input 2.5 in this toy example. max_depth limits the number of successive decisions. random_state fixes the random seed.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Trace a regression-tree prediction.

REFERENCES


## Slide 31 — Trace a regression-tree prediction

PURPOSE
Trace a regression-tree prediction

CONNECT
Previous slide: A small regression tree.

EXPLAIN
Input or question | Path for input 2.5 | Result

Is input at most 2.5? | Yes: use the lower group | Continue within that group

Is input at most 1.5? | No: use its upper leaf | Training target 14

Leaf prediction | Return the leaf value | 14

This trace describes our fitted four-row teaching tree. A different training set can produce different questions.

Read the rows in order. This trace describes our fitted four-row teaching tree. A different training set can produce different questions.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A small regression tree in Python.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 32 — A small regression tree in Python

PURPOSE
A small regression tree in Python

CONNECT
Previous slide: Trace a regression-tree prediction.

EXPLAIN
Read the code in this order:
from sklearn.tree import DecisionTreeRegressor
tree = DecisionTreeRegressor(max_depth=4, random_state=17)
tree.fit(X_train, y_train)
print(tree.predict(new_inputs).tolist())

import loads a library. from selects a tool from it.

fit learns using the supplied training observations.

predict applies the fitted model to new inputs.

Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER CUE
A tree learns threshold questions from the training inputs. Each final group, or leaf, predicts a target value. This tree returns 14 for input 2.5 in this toy example. max_depth limits the number of successive decisions. random_state fixes the random seed.

Complete practice code:
from sklearn.tree import DecisionTreeRegressor
tree = DecisionTreeRegressor(max_depth=4, random_state=17)
tree.fit(X_train, y_train)
print(tree.predict(new_inputs).tolist())

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Reuse the same preparation on new inputs.

REFERENCES


## Slide 33 — Reuse the same preparation on new inputs

PURPOSE
Reuse the same preparation on new inputs

CONNECT
Previous slide: A small regression tree in Python.

EXPLAIN
Imputer: An imputer fills missing feature values using a stated rule. Fit learns the replacement from training observations only. Prediction reuses that stored replacement.

Pipeline: A pipeline connects preprocessing and a model. make_pipeline creates that connection. Its fit learns both stages on training data; predict applies them to new features.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Read the pipeline tools before combining them.

REFERENCES


## Slide 34 — Read the pipeline tools before combining them

PURPOSE
Read the pipeline tools before combining them

CONNECT
Previous slide: Reuse the same preparation on new inputs.

EXPLAIN
np.nan is NumPy’s missing-number marker. SimpleImputer(strategy="median") creates a tool that will learn each column’s median from training data.

make_pipeline(imputer, model) joins preparation to prediction in that order. pipeline.fit first learns and applies the imputer, then fits the model.

pipeline.predict applies the already learned imputer to new inputs before predicting. It does not recalculate medians from the new inputs.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Preprocessing learned from training only.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 35 — Preprocessing learned from training only

PURPOSE
Preprocessing learned from training only

CONNECT
Previous slide: Read the pipeline tools before combining them.

EXPLAIN
SimpleImputer learns one median for each training column. make_pipeline connects this step to the model. fit learns both steps using only the training examples. predict reuses them on new inputs.

No target is supplied to predict.

The two inputs here are invented practice measurements.

LECTURER CUE
SimpleImputer learns one median for each training column. make_pipeline connects this step to the model. fit learns both steps using only the training examples. predict reuses them on new inputs. No target is supplied to predict. The two inputs here are invented practice measurements.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Trace the training-only fill step.

REFERENCES


## Slide 36 — Trace the training-only fill step

PURPOSE
Trace the training-only fill step

CONNECT
Previous slide: Preprocessing learned from training only.

EXPLAIN
Stage | Second feature values | Action

Training input | 20, 22, missing, 24 | Learn median 22

Training after filling | 20, 22, 22, 24 | Fit the model

New input | Missing second value | Fill with saved 22

No new median is learned during prediction. The model receives the prepared numeric row.

Read the rows in order. No new median is learned during prediction. The model receives the prepared numeric row.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Preprocessing learned from training only in Python (1/2).

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 37 — Preprocessing learned from training only in Python (1/2)

PURPOSE
Preprocessing learned from training only in Python (1/2)

CONNECT
Previous slide: Trace the training-only fill step.

EXPLAIN
Read the code in this order:
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
import numpy as np
train_inputs = [[1, 20], [2, 22], [3, np.nan], [4, 24]]
train_targets = [12, 14, 16, 18]
imputer = SimpleImputer(strategy="median")
model = LinearRegression()
pipeline = make_pipeline(imputer, model)
pipeline.fit(train_inputs, train_targets)

import loads a library. from selects a tool from it.

fit learns using the supplied training observations.

Square brackets create a list or select an item.

Read top to bottom. Run the complete example in the matching practice notebook.

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

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Preprocessing learned from training only in Python (2/2).

REFERENCES


## Slide 38 — Preprocessing learned from training only in Python (2/2)

PURPOSE
Preprocessing learned from training only in Python (2/2)

CONNECT
Previous slide: Preprocessing learned from training only in Python (1/2).

EXPLAIN
Read the code in this order:
predictions = pipeline.predict([[2.5, np.nan]])
print(predictions.round(2).tolist())

predict applies the fitted model to new inputs.

print displays a value below the cell.

Square brackets create a list or select an item.

Continue the SAME cell; keep indentation. Run after all parts are entered.

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

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Reading records into a feature table.

REFERENCES


## Slide 39 — Reading records into a feature table

PURPOSE
Reading records into a feature table

CONNECT
Previous slide: Preprocessing learned from training only in Python (2/2).

EXPLAIN
Each inner list is one row, in the same order as the input records.

The target list uses that same row order.

The feature table has no answer column.

LECTURER CUE
Each inner list is one row, in the same order as the input records. The target list uses that same row order. The feature table has no answer column.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Reading records into a feature table in Python.

REFERENCES


## Slide 40 — Reading records into a feature table in Python

PURPOSE
Reading records into a feature table in Python

CONNECT
Previous slide: Reading records into a feature table.

EXPLAIN
Read the code in this order:
rows = [{"length": 2, "width": 3, "area": 6},
        {"length": 4, "width": 5, "area": 20}]
X = []
y = []
for row in rows:
    X.append([row["length"], row["width"]])
    y.append(row["area"])
print(X)
print(y)

for takes the next item. The indented block repeats.

print displays a value below the cell.

append adds one item to the end of a list.

Read top to bottom. Run the complete example in the matching practice notebook.

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

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
MAE and RMSE.

REFERENCES


## Slide 41 — MAE and RMSE

PURPOSE
MAE and RMSE

CONNECT
Previous slide: Reading records into a feature table in Python.

EXPLAIN
MAE and RMSE: MAE averages absolute prediction errors. RMSE squares errors, averages them and takes the square root. Both use target units. RMSE is more sensitive to large errors.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A prediction error in ordinary numbers.

REFERENCES


## Slide 42 — A prediction error in ordinary numbers

PURPOSE
A prediction error in ordinary numbers

CONNECT
Previous slide: MAE and RMSE.

EXPLAIN
Actual | Prediction | Absolute error

10 | 8 | 2

20 | 24 | 4

MAE = (2 + 4) / 2 = 3, in the target’s unit. Compare a model against a training-only baseline.

LECTURER CUE
MAE = (2 + 4) / 2 = 3, in the target’s unit. Compare a model against a training-only baseline.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
The operations in the error calculation.

REFERENCES


## Slide 43 — The operations in the error calculation

PURPOSE
The operations in the error calculation

CONNECT
Previous slide: A prediction error in ordinary numbers.

EXPLAIN
zip and paired names: zip(actual, predicted) pairs values at matching positions. for truth, guess in ... assigns each pair to two names. Here both lists must have the same nonzero length.

Square and square root: difference ** 2 squares an error. sqrt reverses a square for nonnegative numbers: sqrt(9) is 3. from math import sqrt makes this tool available.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Pair two lists using zip.

REFERENCES


## Slide 44 — Pair two lists using zip

PURPOSE
Pair two lists using zip

CONNECT
Previous slide: The operations in the error calculation.

EXPLAIN
zip(actual, predicted) visits matching positions together. for truth, guess in zip(...): unpacks each pair into two names.

For actual [10, 20] and predicted [12, 16], the pairs are (10, 12) and (20, 16). They describe the same observations in the same order.

zip stops at the shorter input. Check equal, nonzero lengths for these error calculations; otherwise a result could ignore observations.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Inspect the pairs before measuring errors.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 45 — Inspect the pairs before measuring errors

PURPOSE
Inspect the pairs before measuring errors

CONNECT
Previous slide: Pair two lists using zip.

EXPLAIN
Read the code in this order:
actual = [10, 20]
predicted = [12, 16]
for truth, guess in zip(actual, predicted):
    print(truth, guess)

The first names receive the first pair, then the second pair.

Output: 10 12; 20 16

Expected printed output:
10 12
20 16

Run the complete cell, then trace each line. Expected output:
10 12
20 16

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Trace absolute and squared errors.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 46 — Trace absolute and squared errors

PURPOSE
Trace absolute and squared errors

CONNECT
Previous slide: Inspect the pairs before measuring errors.

EXPLAIN
Actual and predicted | Absolute error | Squared error

10 and 12 | abs(-2) = 2 | (-2) ** 2 = 4

20 and 16 | abs(4) = 4 | 4 ** 2 = 16

Average | (2 + 4) / 2 = 3 | (4 + 16) / 2 = 10

MAE is 3. RMSE is sqrt(10), approximately 3.1623. sqrt means the nonnegative square root.

Read the rows in order. MAE is 3. RMSE is sqrt(10), approximately 3.1623. sqrt means the nonnegative square root.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Two error measures.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 47 — Two error measures

PURPOSE
Two error measures

CONNECT
Previous slide: Trace absolute and squared errors.

EXPLAIN
zip pairs corresponding values. abs measures error size.

Squaring emphasises large errors; taking the square root returns to the original unit.

These functions assume equal-length, nonempty paired observations.

LECTURER CUE
zip pairs corresponding values. abs measures error size. Squaring emphasises large errors; taking the square root returns to the original unit. These functions assume equal-length, nonempty paired observations.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Two error measures in Python (1/2).

REFERENCES


## Slide 48 — Two error measures in Python (1/2)

PURPOSE
Two error measures in Python (1/2)

CONNECT
Previous slide: Two error measures.

EXPLAIN
Read the code in this order:
from math import sqrt
a = [10, 20]
p = [12, 16]
absolute = []
squared = []
for truth, guess in zip(a, p):
    difference = truth - guess
    absolute.append(abs(difference))
    squared.append(difference ** 2)

import loads a library. from selects a tool from it.

for takes the next item. The indented block repeats.

zip pairs items at matching positions in these equal-length lists.

Read top to bottom. Run the complete example in the matching practice notebook.

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

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Two error measures in Python (2/2).

REFERENCES


## Slide 49 — Two error measures in Python (2/2)

PURPOSE
Two error measures in Python (2/2)

CONNECT
Previous slide: Two error measures in Python (1/2).

EXPLAIN
Read the code in this order:
print(sum(absolute) / len(a))
print(sqrt(sum(squared) / len(a)))

print displays a value below the cell.

Continue the SAME cell; keep indentation. Run after all parts are entered.

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

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
R² compares against a mean prediction.

REFERENCES


## Slide 50 — R² compares against a mean prediction

PURPOSE
R² compares against a mean prediction

CONNECT
Previous slide: Two error measures in Python (2/2).

EXPLAIN
R² compares squared errors with predicting the mean of the evaluated targets. It is a score, not “percentage accuracy”.

1 means perfect predictions on those observations. 0 matches that mean-prediction reference; a negative score can be worse.

Use the same evaluation observations and report the specified error metric with its units. Constant targets need special handling; this score alone does not prove usefulness.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Revision example and answer.

REFERENCES


## Slide 51 — Revision example and answer

PURPOSE
Revision example and answer

CONNECT
Previous slide: R² compares against a mean prediction.

EXPLAIN
Example: On paper compare actual [10, 20] with predictions [12, 16]. Find MAE and RMSE. Is MAE a plus/minus guarantee for each prediction?

Answer: Absolute errors are 2 and 4: MAE 3. Squared errors 4 and 16: RMSE sqrt(10), about 3.162. MAE is an average, not an individual error bound.

LECTURER CUE
Give silent thinking time, then let pairs discuss. Rotate who types. This is practice, not a graded quiz. Expected response: Absolute errors are 2 and 4: MAE 3. Squared errors 4 and 16: RMSE sqrt(10), about 3.162. MAE is an average, not an individual error bound.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Preparing for the assignment.

REFERENCES


## Slide 52 — Preparing for the assignment

PURPOSE
Preparing for the assignment

CONNECT
Previous slide: Revision example and answer.

EXPLAIN
W08 asks for baseline, linear and depth-4 tree prediction lists plus error metrics.

Fit missing-value replacement on training data.

A Pipeline joins preprocessing to the model.

Only load_pct and ambient_c are predictors.

LECTURER CUE
W08 asks for baseline, linear and depth-4 tree prediction lists plus error metrics. Teach training-only median imputation, Pipeline, list-to-table conversion and dictionary return values before those interfaces. Only load_pct and ambient_c are predictors. Introduce grouped partitions now, not first in Week 10. The written comparison is a supplied scenario; do not pretend to have measured its numbers.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Preparing for the assignment continued.

REFERENCES


## Slide 53 — Preparing for the assignment continued

PURPOSE
Preparing for the assignment continued

CONNECT
Previous slide: Preparing for the assignment.

EXPLAIN
Keep observations from the same equipment in one partition.

The written comparison supplies scenario values.

Distinguish them from your own measured results.

LECTURER CUE
W08 asks for baseline, linear and depth-4 tree prediction lists plus error metrics. Teach training-only median imputation, Pipeline, list-to-table conversion and dictionary return values before those interfaces. Only load_pct and ambient_c are predictors. Introduce grouped partitions now, not first in Week 10. The written comparison is a supplied scenario; do not pretend to have measured its numbers.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Reading model outputs.

REFERENCES


## Slide 54 — Reading model outputs

PURPOSE
Reading model outputs

CONNECT
Previous slide: Preparing for the assignment continued.

EXPLAIN
A score on training rows describes training fit.

A feature table must preserve the training column names, order and units during prediction.

A one-dimensional list may have the wrong shape for a model expecting rows and columns.

A predicted-versus-actual plot uses the diagonal as perfect agreement; a pattern is not proof of causation.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Reading model outputs continued.

REFERENCES


## Slide 55 — Reading model outputs continued

PURPOSE
Reading model outputs continued

CONNECT
Previous slide: Reading model outputs.

EXPLAIN
Judge MAE against the baseline and the decision’s acceptable error.

R² is not an accuracy percentage.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Your issued task.

REFERENCES


## Slide 56 — Your issued task

PURPOSE
Your issued task

CONNECT
Previous slide: Reading model outputs continued.

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
predict_regression(training_records, feature_records).

REFERENCES


## Slide 57 — predict_regression(training_records, feature_records)

PURPOSE
predict_regression(training_records, feature_records)

CONNECT
Previous slide: Your issued task.

EXPLAIN
Fit a training-mean baseline, linear regression and a decision tree (max_depth=4, random_state=17) using load_pct and ambient_c only.

Return three prediction lists under baseline, linear and tree.

Feature records have no target.

Fit preprocessing only on training data.

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W08/CML3113/A/TASKS.md

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
regression_errors(actual, predicted).

REFERENCES


## Slide 58 — regression_errors(actual, predicted)

PURPOSE
regression_errors(actual, predicted)

CONNECT
Previous slide: predict_regression(training_records, feature_records).

EXPLAIN
Return mae and rmse, calculated over the same paired observations, with full precision.

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W08/CML3113/A/TASKS.md

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Written evidence.

REFERENCES


## Slide 59 — Written evidence

PURPOSE
Written evidence

CONNECT
Previous slide: regression_errors(actual, predicted).

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
Regression and baseline submission.

REFERENCES


## Slide 60 — Regression and baseline submission

PURPOSE
Regression and baseline submission

CONNECT
Previous slide: Written evidence.

EXPLAIN
Opens: 30 Oct 2026, 08:00 Kampala

Deadline: 06 Nov 2026, 08:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

LECTURER CUE
The form link is cohort-specific. Recheck the live form and release status before class. These scheduled assignment dates are separate from the quiz activation window. The issued brief defines the required files, even if the form accepts additional formats. Source: data/submission_links.json

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Data analysis project.

REFERENCES


## Slide 61 — Data analysis project

PURPOSE
Data analysis project

CONNECT
Previous slide: Regression and baseline submission.

EXPLAIN
Write your own explanation in the markdown cell headed `## My written evidence`.

Keep that heading.

Task prompts and code comments are excluded from reasoning marks.

Complete every original rubric criterion below, not just the checked functions.

LECTURER CUE
# CML3113 DA_PROJECT: Data analysis project — variant A
Full assessment requirements belong in the current public task guide; explain only the criterion or task shown on this slide.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Data analysis project continued.

REFERENCES


## Slide 62 — Data analysis project continued

PURPOSE
Data analysis project continued

CONNECT
Previous slide: Data analysis project.

EXPLAIN
Include profiling, justified cleaning, question-led charts and your engineering recommendation where required.

Keep raw data.

State units and distinguish correlation from causation.

Charts must be actual labelled figures in the notebook, not claims that charts exist.

LECTURER CUE
# CML3113 DA_PROJECT: Data analysis project — variant A
Full assessment requirements belong in the current public task guide; explain only the criterion or task shown on this slide.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Data analysis project continued.

REFERENCES


## Slide 63 — Data analysis project continued

PURPOSE
Data analysis project continued

CONNECT
Previous slide: Data analysis project continued.

EXPLAIN
Include captions and a separate readable DOCX/PDF report.

Question & dataset fit (20.0 total): A real engineering question is stated, and the chosen dataset can actually answer it.

Provenance and licence stated.

Data quality work (25.0 total): Defects found and handled with written justification.

LECTURER CUE
# CML3113 DA_PROJECT: Data analysis project — variant A
Full assessment requirements belong in the current public task guide; explain only the criterion or task shown on this slide.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Data analysis project continued.

REFERENCES


## Slide 64 — Data analysis project continued

PURPOSE
Data analysis project continued

CONNECT
Previous slide: Data analysis project continued.

EXPLAIN
A data quality statement is present.

Analysis & visualisation (30.0 total): Four or more charts, each answering a stated question.

Correct chart types, labelled axes, findings in the captions.

Findings & interpretation (20.0 total): Conclusions supported by the analysis, stated in engineering terms, with limitations acknowledged.

LECTURER CUE
# CML3113 DA_PROJECT: Data analysis project — variant A
Full assessment requirements belong in the current public task guide; explain only the criterion or task shown on this slide.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Data analysis project continued.

REFERENCES


## Slide 65 — Data analysis project continued

PURPOSE
Data analysis project continued

CONNECT
Previous slide: Data analysis project continued.

EXPLAIN
Individual contribution log (5.0 total): Present, specific, and consistent with the repository's commit history.

LECTURER CUE
# CML3113 DA_PROJECT: Data analysis project — variant A
Full assessment requirements belong in the current public task guide; explain only the criterion or task shown on this slide.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Data analysis project submission.

REFERENCES


## Slide 66 — Data analysis project submission

PURPOSE
Data analysis project submission

CONNECT
Previous slide: Data analysis project continued.

EXPLAIN
Opens: 09 Oct 2026, 08:00 Kampala

Deadline: 30 Oct 2026, 08:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

LECTURER CUE
The form link is cohort-specific. Recheck the live form and release status before class. These scheduled assignment dates are separate from the quiz activation window. The issued brief defines the required files, even if the form accepts additional formats. Source: data/submission_links.json

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Week 8 quiz.

REFERENCES


## Slide 67 — Week 8 quiz

PURPOSE
Week 8 quiz

CONNECT
Previous slide: Data analysis project submission.

EXPLAIN
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

The lecturer will confirm the exact closing time.

LECTURER CUE
Activate the matching open_W8_CML3113 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Before you leave.

REFERENCES


## Slide 68 — Revision and submission checklist

PURPOSE
Revision and submission checklist

CONNECT
Previous slide: Week 8 quiz.

EXPLAIN
You can calculate one error and explain why evaluation needs unseen observations.

Save your work and check the required submission files.

LECTURER CUE
Ask every learner for an individual response. Record one misconception to revisit at the start of the next class. If a deadline changed, announce the exact Kampala date and update the source registry before rebuilding slides.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Optional revision video.

REFERENCES


## Slide 69 — Optional revision video

PURPOSE
Optional revision video

CONNECT
Previous slide: Revision and submission checklist.

EXPLAIN
For revision after class.

StatQuest with Josh Starmer
The Essence of Linear Regression!!!

Opening up to 04:00, optional preview-selected excerpt

Listening question: How can a fitted line turn an input into a numerical prediction?

LECTURER CUE
Linked by the official StatQuest video index. Full audiovisual preview and excerpt timing still required.
After viewing: Draw an actual value and a prediction, then identify their difference.
Preview before class and stop after the selected short excerpt. If playback fails, teach the worked example. Video is optional. Source: https://www.youtube.com/watch?v=aFDOzpTeg0s

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
independent revision and the issued task.

REFERENCES
