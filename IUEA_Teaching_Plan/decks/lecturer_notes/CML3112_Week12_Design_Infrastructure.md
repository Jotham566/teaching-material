# CML3112 Week 12

## Slide 1: Choosing and explaining a model

Choosing and explaining a model
Explanation to give
A recommendation must satisfy the practical limits before it wins on a ranking metric. Explain eligibility and tie-breaking separately.

Worked illustration / lecturer answer
A model at 4 error units and 12 ms fails a 10 ms limit even if its error is attractive. Test exact boundaries before ranking eligible candidate_models.

Misconception to address
Use this as an orientation to the lesson. Terms and syntax will be unpacked on their own slides; students do not need to know them in advance.

On this slide
Civil Engineering and Architecture

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
0          1           E1     59.15      31.71  52.547
1          2           E2     77.46      29.97  58.691
2          3           E3     69.60      19.87  47.895
3          4           E4     75.98      22.29     NaN
4          5           E5     57.62      23.40  45.609
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

## Slide 18: Training a model with missing inputs

A model object exists before training. X is two-dimensional and y is one-dimensional. Select inputs in the same order during prediction. A validation target must never enter fit.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 19: Operations for the next example

Returning plain values
series.tolist() or array.tolist() returns a Python list of values, without pandas row labels. Preserve their order when pairing actual values and validation_predictions.

Rounded display
series.round(3) returns values rounded to three decimal places. Python round(number, 3) rounds one number. Keep unrounded calculations for returned assessment answers.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 20: A sequence of model steps / Filling model inputs

make_pipeline(imputer, estimator) links preprocessing and prediction. fit learns the imputer and estimator on training rows. predict applies the learned steps to new rows in the same order.

SimpleImputer(strategy="median") learns a median for each input column during fit. It uses those training medians to fill gaps later. Never learn replacement values from validation or test rows.
Explain these operations before running the following example.

## Slide 21: Creating linear regression / Learning from training examples

LinearRegression() creates an unfitted model. It will learn coefficients and an intercept from training examples. Creating it alone does not train it or make predictions.

model.fit(input_table, observed_targets) learns model settings from paired rows. The two inputs must describe the same observations in the same order. Call fit before predict.
Explain these operations before running the following example.

## Slide 22: Predicting new targets / Selecting a short preview

model.predict(input_table) returns one prediction per input row. Use the same feature columns and order as during training. Prediction uses learned settings; it does not refit the model.

values[:5] selects positions 0 through 4, or fewer if the sequence is shorter. The stop position is excluded. This preview does not change the full array stored in the variable.
Explain these operations before running the following example.

## Slide 23: Standard names for model inputs

These are common machine-learning conventions. Some tutorials write train_x and train_y instead. The names are chosen by the programmer, not special Python keywords. Keep training_data as the full table; selecting X_train must exclude target. Rows in X and y must stay paired. fit uses training pairs; predict receives only X_valid. Compare predictions with y_valid afterwards.

## Slide 24: Separate inputs from answers

X_train contains the input columns; y_train contains their observed targets. X_valid contains the same input columns for validation; y_valid holds the answers for checking predictions. Never include target among the inputs.

## Slide 25: Training and predicting on the supplied data — step 1

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

## Slide 26: Create, then train, then predict

Creating an estimator sets up an empty model. fit learns settings from training inputs and their targets. predict uses those learned settings on new inputs; it does not learn from the validation targets.

## Slide 27: Training and predicting on the supplied data — step 2

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
[44.91, 38.847, 54.982, 34.035, 39.662]

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 28: Matching actual values and predictions

RMSE reacts more strongly to large baseline_errors. Neither metric is a maximum guaranteed error. Pair by row order before calculation. R² is a separate regression measure and can be negative.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 29: Operations for the next example

Adding or replacing a column
equipment_data["name"] = values assigns that column. An array follows row order. A Series aligns by row label, so keep labels paired with the intended observations.

Column arithmetic
Arithmetic on columns calculates one result per row. Series align by row label. Divide only where the denominator is valid and keep actual and predicted observations paired.

Mean of recorded values
series.mean() adds known values and divides by their count. pandas skips missing values by default. The result has the same unit as the original column.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 30: Operations for the next example

Magnitude of each error
series.abs() makes negative values positive while leaving nonnegative values unchanged. Averaging these magnitudes gives mean absolute error.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 31: Squared error and square root

error ** 2 squares each error. After averaging, ** 0.5 takes the square root. This gives root mean squared error, which penalises large errors more strongly than mean absolute error.
Explain these operations before running the following example.

## Slide 32: Line up observations and predictions

Copy record IDs and observed targets from validation rows. Add predictions in that same order. Each row now pairs one observation with its own predicted value.

## Slide 33: Errors from the supplied validation observations — step 1

Copy record IDs and observed targets from validation rows. Add predictions in that same order. Each row now pairs one observation with its own predicted value.

Step-by-step explanation

validation_results = validation_data[['record_id', 'target']].copy()
validation_results stores actual and predicted targets paired with each record ID.

validation_results['predicted'] = validation_predictions
validation_results stores actual and predicted targets paired with each record ID.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 34: Measure how far predictions missed

Subtract predicted from observed values. Positive errors mean underprediction; negative errors mean overprediction. abs removes signs for MAE. Squaring before averaging and taking a square root gives RMSE.

## Slide 35: Errors from the supplied validation observations — step 2

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
4           5  45.609  44.910430
10         11  36.634  38.847011
16         17  54.564  54.981598
22         23  33.523  34.035272
28         29  39.277  39.661642
0.7427 0.8835

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 36: Candidate evidence and latency

perf_counter reads a high-resolution clock. Elapsed seconds times 1000 gives milliseconds. This classroom timing is a demonstration, not a production benchmark.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 37: Operations for the next example

A table from Python values
pd.DataFrame(records) builds a table from row dictionaries. With a dictionary of column lists, keys become column names and each list supplies that column’s values.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 38: Measuring elapsed time

perf_counter() reads a high-resolution clock in seconds. Subtract the earlier reading from the later one, then multiply by 1000 for milliseconds. One measured run is an illustration, not a reliable performance benchmark.
Explain these operations before running the following example.

## Slide 39: Time prediction, not training

perf_counter reads seconds from a high-resolution clock. Read it immediately before and after predict. Convert elapsed seconds to milliseconds and divide by row count. One timing is illustrative: repeated measurements are needed for a reliable speed claim.

## Slide 40: A measured candidate from the supplied validation data — step 1

perf_counter reads seconds from a high-resolution clock. Read it immediately before and after predict. Convert elapsed seconds to milliseconds and divide by row count. One timing is illustrative: repeated measurements are needed for a reliable speed claim.

Step-by-step explanation

from time import perf_counter
Load the named tools. Importing a model class does not train a model.

prediction_start_time = perf_counter()
prediction_start_time stores timer reading immediately before predicting the batch.

linear_model.predict(X_valid)
model.predict(input_table) returns one prediction per input row. Use the same feature columns and order as during training. Prediction uses learned settings; it does not refit the model.

prediction_time_ms = (perf_counter() - prediction_start_time) * 1000 / len(validation_data)
prediction_time_ms stores measured batch time in milliseconds divided by validation-row count.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 41: A measured candidate from the supplied validation data — step 2

candidate_models: table of model names, measured validation errors and prediction times.

## Slide 42: A measured candidate from the supplied validation data — step 2

candidate_models: table of model names, measured validation errors and prediction times.

Step-by-step explanation

candidate_models = pd.DataFrame({'name': ['linear'], 'validation_mae': [float(mae)], 'latency_ms': [prediction_time_ms]})
candidate_models stores table of model names, measured validation errors and prediction times.

print(candidate_models)
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
name  validation_mae  latency_ms
0  linear        0.742677    0.022022

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 43: Constraints and tie-breaks

These limits illustrate a decision rule, not an engineering safety standard. The assessment passes its own candidates and limits, which the function must use.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 44: Operations for the next example

Checking for no rows
equipment_data.empty is True when the filtered table has no entries. Check it before attempting to select a first row. empty is a property, without parentheses.

Sorting by several columns
equipment_data.sort_values(["validation_mae", "latency_ms", "name"]) sorts ascending by error first. Equal errors use latency, then alphabetical name as tie-breaks.

Selecting by row position
equipment_data.iloc[0] selects the first row by its position, not its label. ["name"] then selects that row’s name field. An empty table has no row at position zero.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 45: Checking a condition before calculating

if condition: runs its indented statements only when the condition is True. else: handles the other case. Check for a nonzero denominator before division, and for a nonempty table before selecting its first row.
Explain these operations before running the following example.

## Slide 46: Selection from the measured candidate table — step 1

if condition: runs its indented statements only when the condition is True. else: handles the other case. Check for a nonzero denominator before division, and for a nonempty table before selecting its first row.

Step-by-step explanation

error_is_acceptable = candidate_models['validation_mae'] <= 10
error_is_acceptable stores the result of the displayed expression.

time_is_acceptable = candidate_models['latency_ms'] <= 10
time_is_acceptable stores the result of the displayed expression.

model_is_eligible = error_is_acceptable & time_is_acceptable
model_is_eligible stores the result of the displayed expression.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 47: Apply both model-selection rules

A candidate must satisfy both the error limit and the time limit. Compare each column with its limit first, then combine the True/False answers with &. Filtering can return no rows.

## Slide 48: Selection from the measured candidate table — step 2

A candidate must satisfy both the error limit and the time limit. Compare each column with its limit first, then combine the True/False answers with &. Filtering can return no rows.

Step-by-step explanation

eligible_models = candidate_models[model_is_eligible]
eligible_models stores candidates satisfying both stated limits.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 49: Choose only if an eligible model exists

sort_values orders by error, then time, then name. empty answers whether no rows remain. Check it before iloc[0], which requests the first row by position. Return None when no candidate qualifies.

## Slide 50: Selection from the measured candidate table — step 3

sort_values orders by error, then time, then name. empty answers whether no rows remain. Check it before iloc[0], which requests the first row by position. Return None when no candidate qualifies.

Step-by-step explanation

ranked_models = eligible_models.sort_values(['validation_mae', 'latency_ms', 'name'])
ranked_models stores eligible candidates sorted by error, time and name, in that order.

if ranked_models.empty:
    selected_model_name = None
else:
    selected_model_name = ranked_models.iloc[0]['name']
Check the condition first, then run only the matching branch. This avoids invalid division or selecting a row that does not exist.

print(selected_model_name)
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
linear

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 51: Interpreting the recommendation

One candidate demonstrates eligibility, not superiority over untested alternatives. A local explanation does not establish causation.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 52: Pandas inside the required function

Keep the original function names and return types. Do not read a fixed CSV inside the assessed function: hidden tests supply different equipment_records. The separate calling cell reads the CSV.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 53: Operations for the next example

Returning a dictionary
series.to_dict() maps Series labels to values. equipment_data.to_dict("records") instead returns a list of row dictionaries. Choose the form required by the assignment.

Grouping rows
equipment_data.groupby("label")["value"] groups the value column by matching labels. Apply mean() or sum() to calculate one result per group. Missing group labels are excluded by default.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 54: Defining and calling a function

def gives a reusable block a name and input parameters. The indented statements run when it is called. return sends a result back to the caller; print displays a result but does not return it.
Explain these operations before running the following example.

## Slide 55: A function called with the supplied records

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

## Slide 56: Your issued task

Your issued task
Explanation to give
Name this cohort’s target and its unit exactly as displayed. Each row is one operating observation, while equipment_id can repeat across several observations.

Worked illustration / lecturer answer
Explain record_id as the identifier of an observation, load_pct as load expressed in percent and ambient_c as temperature in degrees Celsius. The target records the known answer in training data.

Misconception to address
These are synthetic examples for learning. They do not establish a calibrated physical relationship or justify operation of real equipment.

On this slide
Investigate building cooling load.

Target units: kW.

These are synthetic teaching records, not measurements suitable for deployment.

Each record is one operating observation; equipment_id repeats across observations.

## Slide 57: select_model(candidates, max_mae, max_ms)

Required interface: select_model(candidates, max_mae, max_ms)

Candidates have name, validation_mae and latency_ms.

Keep those meeting both inclusive constraints; select smallest validation_mae, then latency_ms, then name alphabetically.

Return the selected name or None.

Never use test scores for selection.

Keep these exact output keys and the function name. You may use descriptive local variable names, such as true_positive_count, but the returned dictionary must use the published key, such as tp. The grader checks keys and values; changing a key changes the interface.

## Slide 58: regression_errors(actual, predicted)

Required interface: regression_errors(actual, predicted)

Return mae and rmse, calculated over the same paired observations, with full precision.

Keep these exact output keys and the function name. You may use descriptive local variable names, such as true_positive_count, but the returned dictionary must use the published key, such as tp. The grader checks keys and values; changing a key changes the interface.

## Slide 59: Written evidence

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

## Slide 60: Model recommendation submission

Model recommendation submission
Explanation to give
This slide hands over CML3112 W12. Show the exact form title before uploading. The required packet is one completed .ipynb notebook.

Worked illustration / lecturer answer
The recorded cutoff for this form is 2026-11-24T14:00:00+03:00. Check the live form for later changes. A replacement must contain the complete required file set, not just the changed file.

Misconception to address
Students enter their own Student Registration Number as required freeform text. They wait for filenames to appear, press Submit and keep the confirmation. A file saved in Drive or GitHub is not itself a form submission.

On this slide
Opens: 24 Nov 2026, 11:00 Kampala

Deadline: 24 Nov 2026, 14:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

## Slide 61: Project preparation

Project preparation
Explanation to give
Make contribution evidence specific enough to check. A seed records the starting state of random choices; a contribution log records who produced and explained which work.

Worked illustration / lecturer answer
Name a file, function or chart and the decision behind it. Match that entry to meaningful repository history. Disclose AI assistance according to the assessment policy.

Misconception to address
Many commits do not necessarily mean substantial work, and a seed does not establish accuracy. Both are supporting evidence, not replacements for the analysis.

On this slide
Use the published machine learning project brief.

Build the evidence gradually in your project notebook.

Keep raw data, labelled charts, run instructions and individual contributions.

Published deadline: 15 Dec 2026, 11:00 Kampala

## Slide 62: Week 12 quiz

Week 12 quiz
Explanation to give
This is the CML3112 Week 1 quiz. The student link opens the response form; it does not activate its window. In Quiz Controls use open_W1_CML3112 when ready and read the logged closing time.

Worked illustration / lecturer answer
Explain the distinction between the expected answering time and availability: five minutes of questions can still be available for 24 hours after activation. Enter the learner’s own Student Registration Number and use the registered Google account.

Misconception to address
Read the exact live cutoff before announcing it. Do not promise a new attempt to somebody who already submitted. Quiz catch-up and assignment uploads are separate forms.

On this slide
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

Check the announced quiz closing time.

## Slide 63: Revision and submission checklist

Revision and submission checklist
Explanation to give
A recommendation must satisfy the practical limits before it wins on a ranking metric. Explain eligibility and tie-breaking separately.

Worked illustration / lecturer answer
A model at 4 error units and 12 ms fails a 10 ms limit even if its error is attractive. Test exact boundaries before ranking eligible candidate_models.

Misconception to address
Close by identifying the actual saved file and its correct submission route. Read the live deadline. For current weekly notebook tasks, students upload their own work, not the practice notebook, ZIP or grading files.

On this slide
You can justify a valid candidate with evidence and a stated limitation.

Save your work and check the required submission files.

## Slide 64: Optional revision video

Optional revision video
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