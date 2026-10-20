# CML3113 Week 8

## Slide 1: A first prediction model

A first prediction model
Explanation to give
Introduce a fitted predictor only after identifying its inputs and known answers. Compare it with a simple baseline and explain its errors in target units.

Worked illustration / lecturer answer
The teaching line through (1,12), (2,14), (3,16), (4,18) predicts 15 at input 2.5. One neat example does not establish real-world accuracy.

Misconception to address
Use this as an orientation to the lesson. Terms and syntax will be unpacked on their own slides; students do not need to know them in advance.

On this slide
Mining and Petroleum Engineering

## Slide 2: Today’s learning

Core practice precedes the assessment brief. Give the class one consistent data-handling approach: pandas for tables, scikit-learn for models, matplotlib for figures.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 3: The supplied file

Uploading a notebook does not upload its modelling_data. Check the exact filename and column headings. Each cohort has its own data, so numerical results can differ.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 4: Operations for the next example

Import and short names
import pandas as pd loads pandas and gives it the short name pd. pd.read_csv refers to a function in that library.

Reading a CSV
pd.read_csv("practice_filename.csv") reads the named file into a DataFrame: a table with labelled columns and row labels. The file must exist in the working folder.

Counting dimensions
equipment_data.shape gives (number of rows, number of columns). shape is a property, so it has no parentheses.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 5: Operations for the next example

Column data types
equipment_data.dtypes reports each column’s stored type. int64 means integers, float64 means decimal numbers, and object often contains text. Numeric blanks commonly appear as NaN.

A preview of rows
equipment_data.head() returns the first five rows. It leaves the table unchanged. A preview is not the entire dataset.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 6: Reading the code syntax

= assigns a value to a name; == compares values. Parentheses pass inputs or continue an expression across lines. print displays a value; len counts entries. int and float convert to integer and decimal numeric values.
Explain these operations before running the following example.

## Slide 7: Loading the supplied observations

= assigns a value to a name; == compares values. Parentheses pass inputs or continue an expression across lines. print displays a value; len counts entries. int and float convert to integer and decimal numeric values.

Step-by-step explanation

import pandas as pd
Load the named tools. Importing a model class does not train a model.

raw_data = pd.read_csv('engineering_data.csv')
raw_data stores original CSV table; keep it unchanged so the analysis can be checked.

print(raw_data.head())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(raw_data.shape)
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(raw_data.dtypes)
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
record_id equipment_id  load_pct  ambient_c  target
0          1           E1     59.15      31.71  14.001
1          2           E2     77.46      29.97  15.147
2          3           E3     69.60      19.87  13.005
3          4           E4     75.98      22.29     NaN
4          5           E5     57.62      23.40  12.554
(91, 5)
record_id         int64
equipment_id     object
load_pct        float64
ambient_c       float64
target          float64
dtype: object

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 8: Rows used for modelling

This follows the issued data rules. Filtering observed targets is different from estimating missing targets. Deduplicate before filtering, so an invalid first occurrence is not replaced by its later duplicate.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 9: Operations for the next example

Reading chained operations
Read a chain from left to right. In equipment_data["target"].mean(), select the target Series first, then calculate its mean. Each step uses the previous step’s result.

A separate working table
equipment_data.copy() creates a working copy. Assigning columns on this copy preserves the source table, so you can compare before and after.

Finding recorded cells
notna() returns True where a value is present. Use it to retain observations with a recorded target before modelling.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 10: Operations for the next example

An inclusive range
series.between(0, 100) is True for values from 0 through 100, including both limits. The resulting mask helps select valid rows.

Selecting columns
equipment_data["column"] returns one labelled column, a Series. equipment_data[["a", "b"]] returns a DataFrame containing those named columns in that order.

Selecting rows with a mask
A column comparison produces one True or False per row. equipment_data[mask] keeps the True rows. & combines masks: both conditions must hold. Parenthesise each comparison.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 11: Operations for the next example

Keeping the first observation
equipment_data.drop_duplicates("record_id") returns rows with the first occurrence of each ID, preserving their order. It does not overwrite the source unless you assign the result.

Membership in a group list
series.isin(["E1", "E2"]) returns True for entries matching either listed label. equipment_data[that_mask] keeps all observations belonging to those groups.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 12: Prepare valid observations

First keep the first record ID. Then ask two questions for each remaining row: is the target recorded, and is load between 0 and 100? Only a row passing both checks stays. Missing inputs are handled later using training data only.

## Slide 13: Preparing the supplied modelling rows — step 1

First keep the first record ID. Then ask two questions for each remaining row: is the target recorded, and is load between 0 and 100? Only a row passing both checks stays. Missing inputs are handled later using training data only.

Step-by-step explanation

modelling_data = raw_data.drop_duplicates('record_id').copy()
modelling_data stores copied observations after duplicate and validity checks.

target_is_recorded = modelling_data['target'].notna()
target_is_recorded stores the result of the displayed expression.

load_is_valid = modelling_data['load_pct'].between(0, 100)
load_is_valid stores the result of the displayed expression.

rows_to_keep = target_is_recorded & load_is_valid
rows_to_keep stores the result of the displayed expression.

print(target_is_recorded.head())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(load_is_valid.head())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

modelling_data = modelling_data[rows_to_keep].copy()
modelling_data stores copied observations after duplicate and validity checks.

print(len(raw_data), len(modelling_data))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
0     True
1     True
2     True
3    False
4     True
Name: target, dtype: bool
0    True
1    True
2    True
3    True
4    True
Name: load_pct, dtype: bool
91 88

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 14: Choose groups before choosing rows

isin(list_of_labels) answers True when a row’s equipment ID appears in the list. Here E1–E4 supply training rows, E5 validation rows and E6 test rows. The groups stay separate so one equipment group cannot appear on both sides.

## Slide 15: Preparing the supplied modelling rows — step 2

isin(list_of_labels) answers True when a row’s equipment ID appears in the list. Here E1–E4 supply training rows, E5 validation rows and E6 test rows. The groups stay separate so one equipment group cannot appear on both sides.

Step-by-step explanation

is_training_equipment = modelling_data['equipment_id'].isin(['E1', 'E2', 'E3', 'E4'])
is_training_equipment stores the result of the displayed expression.

is_validation_equipment = modelling_data['equipment_id'].isin(['E5'])
is_validation_equipment stores the result of the displayed expression.

is_test_equipment = modelling_data['equipment_id'].isin(['E6'])
is_test_equipment stores the result of the displayed expression.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 16: Preparing the supplied modelling rows — step 3

training_data: rows used to learn model settings; only these rows may determine imputation values.

validation_data: separate rows used to compare models without fitting on them.

## Slide 17: Preparing the supplied modelling rows — step 3

training_data: rows used to learn model settings; only these rows may determine imputation values.

validation_data: separate rows used to compare models without fitting on them.

Step-by-step explanation

training_data = modelling_data[is_training_equipment].copy()
training_data stores rows used to learn model settings; only these rows may determine imputation values.

validation_data = modelling_data[is_validation_equipment].copy()
validation_data stores separate rows used to compare models without fitting on them.

test_data = modelling_data[is_test_equipment].copy()
test_data stores held-out rows kept aside until the final evaluation.

feature_columns = ['load_pct', 'ambient_c']
feature_columns stores the list of input column names supplied to the model.

print(len(training_data), len(validation_data), len(test_data))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
58 15 15

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 18: Fitting a line to observations

Fitting a line to observations
Explanation to give
Use the four teaching pairs to make the learned relationship visible. A one-unit input increase corresponds to a two-unit target increase in this invented dataset.

Worked illustration / lecturer answer
The pairs (1,12), (2,14), (3,16), (4,18) follow target = 10 + 2 × input. For input 2.5, that line gives 15. A tree makes threshold-based group predictions instead.

Misconception to address
These perfectly patterned values explain model behaviour. They do not establish that real engineering data follows an exact line.

On this slide
The fitted line minimises the sum of squared vertical baseline_errors.

## Slide 19: Training a model with missing inputs

A model object exists before training. X is two-dimensional and y is one-dimensional. Select inputs in the same order during prediction. A validation target must never enter fit.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 20: Operations for the next example

Returning plain values
series.tolist() or array.tolist() returns a Python list of values, without pandas row labels. Preserve their order when pairing actual values and validation_predictions.

Rounded display
series.round(3) returns values rounded to three decimal places. Python round(number, 3) rounds one number. Keep unrounded calculations for returned assessment answers.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 21: A sequence of model steps / Filling model inputs

make_pipeline(imputer, estimator) links preprocessing and prediction. fit learns the imputer and estimator on training rows. predict applies the learned steps to new rows in the same order.

SimpleImputer(strategy="median") learns a median for each input column during fit. It uses those training medians to fill gaps later. Never learn replacement values from validation or test rows.
Explain these operations before running the following example.

## Slide 22: Creating linear regression / Learning from training examples

LinearRegression() creates an unfitted model. It will learn coefficients and an intercept from training examples. Creating it alone does not train it or make predictions.

model.fit(input_table, observed_targets) learns model settings from paired rows. The two inputs must describe the same observations in the same order. Call fit before predict.
Explain these operations before running the following example.

## Slide 23: Predicting new targets / Selecting a short preview

model.predict(input_table) returns one prediction per input row. Use the same feature columns and order as during training. Prediction uses learned settings; it does not refit the model.

values[:5] selects positions 0 through 4, or fewer if the sequence is shorter. The stop position is excluded. This preview does not change the full array stored in the variable.
Explain these operations before running the following example.

## Slide 24: Standard names for model inputs

These are common machine-learning conventions. Some tutorials write train_x and train_y instead. The names are chosen by the programmer, not special Python keywords. Keep training_data as the full table; selecting X_train must exclude target. Rows in X and y must stay paired. fit uses training pairs; predict receives only X_valid. Compare predictions with y_valid afterwards.

## Slide 25: Separate inputs from answers

X_train contains the input columns; y_train contains their observed targets. X_valid contains the same input columns for validation; y_valid holds the answers for checking predictions. Never include target among the inputs.

## Slide 26: Training and predicting on the supplied data — step 1

X_train contains the input columns; y_train contains their observed targets. X_valid contains the same input columns for validation; y_valid holds the answers for checking predictions. Never include target among the inputs.

Step-by-step explanation

X_train = training_data[feature_columns]
X_train stores training input columns, excluding the target.

y_train = training_data['target']
y_train stores observed training targets in matching row order.

X_valid = validation_data[feature_columns]
X_valid stores validation input columns in training-column order.

y_valid = validation_data['target']
y_valid stores observed validation targets, used only for evaluation.

from sklearn.impute import SimpleImputer
Load the named tools. Importing a model class does not train a model.

from sklearn.pipeline import make_pipeline
Load the named tools. Importing a model class does not train a model.

from sklearn.linear_model import LinearRegression
Load the named tools. Importing a model class does not train a model.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 27: Create, then train, then predict

Creating an estimator sets up an empty model. fit learns settings from training inputs and their targets. predict uses those learned settings on new inputs; it does not learn from the validation targets.

## Slide 28: Training and predicting on the supplied data — step 2

Creating an estimator sets up an empty model. fit learns settings from training inputs and their targets. predict uses those learned settings on new inputs; it does not learn from the validation targets.

Step-by-step explanation

linear_model = make_pipeline(SimpleImputer(strategy='median'), LinearRegression())
linear_model stores the linear regression estimator or imputation-and-regression pipeline.

linear_model.fit(X_train, y_train)
model.fit(input_table, observed_targets) learns model settings from paired rows. The two inputs must describe the same observations in the same order. Call fit before predict.

validation_predictions = linear_model.predict(X_valid)
validation_predictions stores one predicted target for each validation row, in the same order.

print(validation_predictions[:5].round(3).tolist())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
[11.79, 9.69, 14.015, 8.537, 10.471]

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 29: Baseline and tree comparisons

Both methods answer the same target question. The baseline provides a useful comparison. Tree predictions need not extrapolate a straight line.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 30: A training-mean baseline / Creating a regression tree

DummyRegressor(strategy="mean") learns the mean training target during fit. It predicts that same value for every new row. Compare a more complex model against this simple baseline.

DecisionTreeRegressor splits inputs into regions with different predicted values. max_depth limits the number of split levels. random_state fixes random choices so the example can be repeated.
Explain these operations before running the following example.

## Slide 31: Start with a simple reference

A training-mean baseline predicts the same value for every validation row. fit calculates that value from y_train. Compare its error with the more complex model on the same validation rows.

## Slide 32: Baseline and tree on the same CSV rows — step 1

A training-mean baseline predicts the same value for every validation row. fit calculates that value from y_train. Compare its error with the more complex model on the same validation rows.

Step-by-step explanation

from sklearn.dummy import DummyRegressor
Load the named tools. Importing a model class does not train a model.

from sklearn.tree import DecisionTreeRegressor
Load the named tools. Importing a model class does not train a model.

baseline_model = DummyRegressor(strategy='mean')
baseline_model stores a simple reference predictor which always predicts the training target mean.

baseline_model.fit(X_train, y_train)
model.fit(input_table, observed_targets) learns model settings from paired rows. The two inputs must describe the same observations in the same order. Call fit before predict.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 33: Compare a second kind of model

A regression tree learns splits in the input columns. max_depth limits its split levels. The imputer fills missing inputs using training medians; the tree then learns from those filled inputs.

## Slide 34: Baseline and tree on the same CSV rows — step 2

A regression tree learns splits in the input columns. max_depth limits its split levels. The imputer fills missing inputs using training medians; the tree then learns from those filled inputs.

Step-by-step explanation

tree_model = make_pipeline(SimpleImputer(strategy='median'), DecisionTreeRegressor(max_depth=4, random_state=17))
tree_model stores the tree regression pipeline being compared on the same validation rows.

tree_model.fit(X_train, y_train)
model.fit(input_table, observed_targets) learns model settings from paired rows. The two inputs must describe the same observations in the same order. Call fit before predict.

print(baseline_model.predict(X_valid)[:5].round(3).tolist())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(tree_model.predict(X_valid)[:5].round(3).tolist())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
[12.528, 12.528, 12.528, 12.528, 12.528]
[11.668, 10.113, 12.561, 8.039, 11.668]

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 35: Matching actual values and predictions

RMSE reacts more strongly to large baseline_errors. Neither metric is a maximum guaranteed error. Pair by row order before calculation. R² is a separate regression measure and can be negative.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 36: Operations for the next example

Adding or replacing a column
equipment_data["name"] = values assigns that column. An array follows row order. A Series aligns by row label, so keep labels paired with the intended observations.

Column arithmetic
Arithmetic on columns calculates one result per row. Series align by row label. Divide only where the denominator is valid and keep actual and predicted observations paired.

Mean of recorded values
series.mean() adds known values and divides by their count. pandas skips missing values by default. The result has the same unit as the original column.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 37: Operations for the next example

Magnitude of each error
series.abs() makes negative values positive while leaving nonnegative values unchanged. Averaging these magnitudes gives mean absolute error.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 38: Squared error and square root

error ** 2 squares each error. After averaging, ** 0.5 takes the square root. This gives root mean squared error, which penalises large errors more strongly than mean absolute error.
Explain these operations before running the following example.

## Slide 39: Line up observations and predictions

Copy record IDs and observed targets from validation rows. Add predictions in that same order. Each row now pairs one observation with its own predicted value.

## Slide 40: Errors from the supplied validation observations — step 1

Copy record IDs and observed targets from validation rows. Add predictions in that same order. Each row now pairs one observation with its own predicted value.

Step-by-step explanation

validation_results = validation_data[['record_id', 'target']].copy()
validation_results stores actual and predicted targets paired with each record ID.

validation_results['predicted'] = validation_predictions
validation_results stores actual and predicted targets paired with each record ID.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 41: Measure how far predictions missed

Subtract predicted from observed values. Positive errors mean underprediction; negative errors mean overprediction. abs removes signs for MAE. Squaring before averaging and taking a square root gives RMSE.

## Slide 42: Errors from the supplied validation observations — step 2

Subtract predicted from observed values. Positive errors mean underprediction; negative errors mean overprediction. abs removes signs for MAE. Squaring before averaging and taking a square root gives RMSE.

Step-by-step explanation

prediction_errors = validation_results['target'] - validation_results['predicted']
prediction_errors stores actual targets minus predictions; signs indicate under- or over-prediction.

mae = prediction_errors.abs().mean()
mae stores mean absolute error in the target unit.

rmse = (prediction_errors ** 2).mean() ** 0.5
rmse stores root mean squared error in the target unit.

print(validation_results.head())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(round(float(mae), 4), round(float(rmse), 4))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
record_id  target  predicted
4           5  12.554  11.790394
10         11   7.620   9.689703
16         17  13.616  14.014617
22         23   8.196   8.536859
28         29  10.187  10.471133
0.6732 0.8148

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 43: Pandas inside the required function

Keep the original function names and return types. Do not read a fixed CSV inside the assessed function: hidden tests supply different equipment_records. The separate calling cell reads the CSV.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 44: Operations for the next example

Returning a dictionary
series.to_dict() maps Series labels to values. equipment_data.to_dict("records") instead returns a list of row dictionaries. Choose the form required by the assignment.

A table from Python values
pd.DataFrame(records) builds a table from row dictionaries. With a dictionary of column lists, keys become column names and each list supplies that column’s values.

Grouping rows
equipment_data.groupby("label")["value"] groups the value column by matching labels. Apply mean() or sum() to calculate one result per group. Missing group labels are excluded by default.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 45: Defining and calling a function

def gives a reusable block a name and input parameters. The indented statements run when it is called. return sends a result back to the caller; print displays a result but does not return it.
Explain these operations before running the following example.

## Slide 46: A function called with the supplied records

def gives a reusable block a name and input parameters. The indented statements run when it is called. return sends a result back to the caller; print displays a result but does not return it.

Step-by-step explanation

def mean_load_by_equipment(equipment_records):
    equipment_data = pd.DataFrame(equipment_records)
    mean_load_by_equipment_group = equipment_data.groupby('equipment_id')['load_pct'].mean()
    return mean_load_by_equipment_group.to_dict()
Define the function. Explain each input before the call. Its body runs only when called; return supplies the computed value.

equipment_records = raw_data.to_dict('records')
equipment_records stores the input list of row dictionaries supplied to the function.

print(mean_load_by_equipment(equipment_records))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
{'E1': 54.9475, 'E2': 61.326, 'E3': 53.46933333333333, 'E4': 66.854, 'E5': 48.10133333333333, 'E6': 51.54}

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 47: Your issued task

Your issued task
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

## Slide 48: predict_regression(training_records, feature_records)

Required interface: predict_regression(training_records, feature_records)

Fit a training-mean baseline, linear regression and a decision tree (max_depth=4, random_state=17) using load_pct and ambient_c only.

Return three prediction lists under baseline, linear and tree.

Feature records have no target.

Fit preprocessing only on training data.

Keep these exact output keys and the function name. You may use descriptive local variable names, such as true_positive_count, but the returned dictionary must use the published key, such as tp. The grader checks keys and values; changing a key changes the interface.

## Slide 49: regression_errors(actual, predicted)

Required interface: regression_errors(actual, predicted)

Return mae and rmse, calculated over the same paired observations, with full precision.

Keep these exact output keys and the function name. You may use descriptive local variable names, such as true_positive_count, but the returned dictionary must use the published key, such as tp. The grader checks keys and values; changing a key changes the interface.

## Slide 50: Written evidence

Written evidence
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

## Slide 51: Regression and baseline submission

Regression and baseline submission
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

## Slide 52: Data analysis project

Data analysis project
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

## Slide 53: Data analysis project continued

Data analysis project continued
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

## Slide 54: Data analysis project continued

Data analysis project continued
Explanation to give
Problem framing begins with a bounded engineering decision and a defined target. Provenance explains where observations came from; a licence states what reuse is allowed.

Worked illustration / lecturer answer
State the population, measurement period, units and who collected the modelling_data. Explain how those observations could answer the chosen question rather than merely describing an interesting file.

Misconception to address
Synthetic teaching data must be labelled as synthetic. A plausible story does not establish that a dataset contains the information or permissions the proposed project needs.

On this slide
Include captions and a separate readable DOCX/PDF report.

Question & dataset fit (20.0 total): A real engineering question is stated, and the chosen dataset can actually answer it.

Provenance and licence stated.

Data quality work (25.0 total): Defects found and handled with written justification.

## Slide 55: Data analysis project continued

Data analysis project continued
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

## Slide 56: Data analysis project continued

Data analysis project continued
Explanation to give
Make contribution evidence specific enough to check. A seed records the starting state of random choices; a contribution log records who produced and explained which work.

Worked illustration / lecturer answer
Name a file, function or chart and the decision behind it. Match that entry to meaningful repository history. Disclose AI assistance according to the assessment policy.

Misconception to address
Many commits do not necessarily mean substantial work, and a seed does not establish accuracy. Both are supporting evidence, not replacements for the analysis.

On this slide
Individual contribution log (5.0 total): Present, specific, and consistent with the repository's commit history.

## Slide 57: Data analysis project submission

Data analysis project submission
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

## Slide 58: Week 8 quiz

Week 8 quiz
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

## Slide 59: Revision and submission checklist

Revision and submission checklist
Explanation to give
Introduce a fitted predictor only after identifying its inputs and known answers. Compare it with a simple baseline and explain its errors in target units.

Worked illustration / lecturer answer
The teaching line through (1,12), (2,14), (3,16), (4,18) predicts 15 at input 2.5. One neat example does not establish real-world accuracy.

Misconception to address
Close by identifying the actual saved file and its correct submission route. Read the live deadline. For current weekly notebook tasks, students upload their own work, not the practice notebook, ZIP or grading files.

On this slide
You can calculate one error and explain why evaluation needs unseen observations.

Save your work and check the required submission files.

## Slide 60: Optional revision video

Optional revision video
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