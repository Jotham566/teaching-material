# CML3113 Week 10

## Slide 1: Honest validation and leakage

Honest validation and leakage
Explanation to give
Connect evaluation to intended use. Decide how to hold out observations before fitting either preprocessing or the linear_model.

Worked illustration / lecturer answer
When testing new equipment, all observations from equipment A stay in one partition. Training must not learn its missing-value replacements from held-out equipment.

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

## Slide 8: Three sets have different jobs

Three sets have different jobs
Explanation to give
Training observations teach the linear_model. Validation observations help choose among models and settings. The final test is reserved for evaluating the chosen method after those choices are fixed.

Worked illustration / lecturer answer
Compare two models using the same validation observations, choose a method, then evaluate it once on the held-out test_data. Imagine the test as a sealed examination paper.

Misconception to address
Repeatedly checking the test while selecting features or settings makes it part of the selection process, so it no longer gives an independent final check.

On this slide
Which set must stay sealed until choices are fixed?

## Slide 9: Rows used for modelling

This follows the issued data rules. Filtering observed targets is different from estimating missing targets. Deduplicate before filtering, so an invalid first occurrence is not replaced by its later duplicate.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 10: Operations for the next example

Reading chained operations
Read a chain from left to right. In equipment_data["target"].mean(), select the target Series first, then calculate its mean. Each step uses the previous step’s result.

A separate working table
equipment_data.copy() creates a working copy. Assigning columns on this copy preserves the source table, so you can compare before and after.

Finding recorded cells
notna() returns True where a value is present. Use it to retain observations with a recorded target before modelling.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 11: Operations for the next example

An inclusive range
series.between(0, 100) is True for values from 0 through 100, including both limits. The resulting mask helps select valid rows.

Selecting columns
equipment_data["column"] returns one labelled column, a Series. equipment_data[["a", "b"]] returns a DataFrame containing those named columns in that order.

Selecting rows with a mask
A column comparison produces one True or False per row. equipment_data[mask] keeps the True rows. & combines masks: both conditions must hold. Parenthesise each comparison.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 12: Operations for the next example

Keeping the first observation
equipment_data.drop_duplicates("record_id") returns rows with the first occurrence of each ID, preserving their order. It does not overwrite the source unless you assign the result.

Membership in a group list
series.isin(["E1", "E2"]) returns True for entries matching either listed label. equipment_data[that_mask] keeps all observations belonging to those groups.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 13: Prepare valid observations

First keep the first record ID. Then ask two questions for each remaining row: is the target recorded, and is load between 0 and 100? Only a row passing both checks stays. Missing inputs are handled later using training data only.

## Slide 14: Preparing the supplied modelling rows — step 1

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

## Slide 15: Choose groups before choosing rows

isin(list_of_labels) answers True when a row’s equipment ID appears in the list. Here E1–E4 supply training rows, E5 validation rows and E6 test rows. The groups stay separate so one equipment group cannot appear on both sides.

## Slide 16: Preparing the supplied modelling rows — step 2

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

## Slide 17: Preparing the supplied modelling rows — step 3

training_data: rows used to learn model settings; only these rows may determine imputation values.

validation_data: separate rows used to compare models without fitting on them.

## Slide 18: Preparing the supplied modelling rows — step 3

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

## Slide 19: Training-only filling

Even preprocessing without target labels can leak information about evaluation distributions.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 20: Operations for the next example

Middle recorded value
series.median() sorts known values conceptually and returns the middle one. With an even count, it averages the two middle values. Missing entries do not enter the calculation.

Replacing missing entries
series.fillna(value) returns a column whose missing entries contain value. Recorded values stay unchanged. Assign the returned column to retain the fill.

Rounded display
series.round(3) returns values rounded to three decimal places. Python round(number, 3) rounds one number. Keep unrounded calculations for returned assessment answers.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 21: Operations for the next example

Adding values and counting True
series.sum() adds its values. For a Boolean mask, True counts as 1 and False as 0. equipment_data.isna().sum() therefore counts missing cells separately for each column.

Finding missing cells
isna() returns True for missing entries such as NaN and None. It returns False for a recorded zero. A DataFrame gives a mask for every cell; a Series gives one mask value per row.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 22: Training median from the actual ambient readings

Adding values and counting True: series.sum() adds its values. For a Boolean mask, True counts as 1 and False as 0. equipment_data.isna().sum() therefore counts missing cells separately for each column.

Finding missing cells: isna() returns True for missing entries such as NaN and None. It returns False for a recorded zero. A DataFrame gives a mask for every cell; a Series gives one mask value per row.

Step-by-step explanation

training_ambient_median = training_data['ambient_c'].median()
training_ambient_median stores median ambient temperature calculated only from training rows.

filled_validation_ambient = validation_data['ambient_c'].fillna(training_ambient_median)
filled_validation_ambient stores validation ambient column with gaps filled using the training median.

print(round(float(training_ambient_median), 3))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(validation_data['ambient_c'].isna().sum())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(filled_validation_ambient.head())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
26.07
0
4     23.40
10    33.98
16    34.28
22    30.81
28    21.33
Name: ambient_c, dtype: float64

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 23: Training a model with missing inputs

A model object exists before training. X is two-dimensional and y is one-dimensional. Select inputs in the same order during prediction. A validation target must never enter fit.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 24: Operations for the next example

Returning plain values
series.tolist() or array.tolist() returns a Python list of values, without pandas row labels. Preserve their order when pairing actual values and validation_predictions.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 25: A sequence of model steps / Filling model inputs

make_pipeline(imputer, estimator) links preprocessing and prediction. fit learns the imputer and estimator on training rows. predict applies the learned steps to new rows in the same order.

SimpleImputer(strategy="median") learns a median for each input column during fit. It uses those training medians to fill gaps later. Never learn replacement values from validation or test rows.
Explain these operations before running the following example.

## Slide 26: Creating linear regression / Learning from training examples

LinearRegression() creates an unfitted model. It will learn coefficients and an intercept from training examples. Creating it alone does not train it or make predictions.

model.fit(input_table, observed_targets) learns model settings from paired rows. The two inputs must describe the same observations in the same order. Call fit before predict.
Explain these operations before running the following example.

## Slide 27: Predicting new targets / Selecting a short preview

model.predict(input_table) returns one prediction per input row. Use the same feature columns and order as during training. Prediction uses learned settings; it does not refit the model.

values[:5] selects positions 0 through 4, or fewer if the sequence is shorter. The stop position is excluded. This preview does not change the full array stored in the variable.
Explain these operations before running the following example.

## Slide 28: Standard names for model inputs

These are common machine-learning conventions. Some tutorials write train_x and train_y instead. The names are chosen by the programmer, not special Python keywords. Keep training_data as the full table; selecting X_train must exclude target. Rows in X and y must stay paired. fit uses training pairs; predict receives only X_valid. Compare predictions with y_valid afterwards.

## Slide 29: Separate inputs from answers

X_train contains the input columns; y_train contains their observed targets. X_valid contains the same input columns for validation; y_valid holds the answers for checking predictions. Never include target among the inputs.

## Slide 30: Training and predicting on the supplied data — step 1

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

## Slide 31: Create, then train, then predict

Creating an estimator sets up an empty model. fit learns settings from training inputs and their targets. predict uses those learned settings on new inputs; it does not learn from the validation targets.

## Slide 32: Training and predicting on the supplied data — step 2

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

## Slide 33: Each fold takes a turn at validation

Each fold takes a turn at validation
Explanation to give
A parameter is learned during fit. A hyperparameter is chosen as a setting. Cross-validation repeats fitting with different held-out portions of the development data to assess choices more steadily.

Worked illustration / lecturer answer
If validation errors are 2, 3 and 4, the mean is 3. Their spread indicates sensitivity to the held-out portion. A standard deviation describes that spread; it is not automatically a confidence interval.

Misconception to address
Fit preprocessing separately within each training fold. Keep groups or time order intact where required. The final test remains separate from tuning.

On this slide
Illustrated spread: population SD 0.39 MPa, not a confidence interval.

## Slide 34: Cross-validation within training data

Use only the E1–E4 training partition here. E5 remains the separate validation partition and E6 the final test_data. The imputer is refitted within each training fold.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 35: Operations for the next example

A labelled column
pd.Series(values) creates a one-dimensional labelled sequence. With an array of fold errors, the default labels are 0, 1, 2 and so on.

Mean of recorded values
series.mean() adds known values and divides by their count. pandas skips missing values by default. The result has the same unit as the original column.

Spread of fold errors
series.std(ddof=0) measures how far values spread around their mean. ddof=0 divides squared deviations by the number of values. This describes these folds, not a confidence interval.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 36: Keeping groups together / Scoring repeated splits

GroupKFold(n_splits=4) creates four train/validation splits. All rows of an equipment group stay on one side of each split. Four splits require at least four distinct training groups.

cross_val_score fits a fresh model for each split and scores its held-out rows. groups identifies the equipment groups and cv supplies the split rule. neg_mean_absolute_error returns negative MAE; negate it to report positive errors.
Explain these operations before running the following example.

## Slide 37: Repeat evaluation without mixing groups

Four folds means four held-out group turns. In each turn, learn a fresh pipeline on the other training groups and score the held-out group. This uses training_data only; validation and test tables stay outside this calculation.

## Slide 38: Fold errors calculated from the supplied training rows — step 1

Four folds means four held-out group turns. In each turn, learn a fresh pipeline on the other training groups and score the held-out group. This uses training_data only; validation and test tables stay outside this calculation.

Step-by-step explanation

from sklearn.model_selection import GroupKFold, cross_val_score
Load the named tools. Importing a model class does not train a model.

grouped_folds = GroupKFold(n_splits=4)
grouped_folds stores the split rule that keeps observations from one equipment group together.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 39: Read the scoring convention

scikit-learn uses larger scores as better. neg_mean_absolute_error therefore returns negative errors. Negate the returned scores to recover ordinary positive MAE; lower MAE is better.

## Slide 40: Fold errors calculated from the supplied training rows — step 2

scikit-learn uses larger scores as better. neg_mean_absolute_error therefore returns negative errors. Negate the returned scores to recover ordinary positive MAE; lower MAE is better.

Step-by-step explanation

negative_error_scores = cross_val_score(linear_model, X_train, y_train, groups=training_data['equipment_id'], cv=grouped_folds, scoring='neg_mean_absolute_error')
negative_error_scores stores negative mean absolute errors returned by scikit-learn’s scoring convention.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 41: Report typical error and variation

Each value is the MAE of one held-out fold. mean gives average error. std(ddof=0) describes spread across these four errors; it is not a confidence interval. A large spread suggests performance depends on the held-out equipment.

## Slide 42: Fold errors calculated from the supplied training rows — step 3

Each value is the MAE of one held-out fold. mean gives average error. std(ddof=0) describes spread across these four errors; it is not a confidence interval. A large spread suggests performance depends on the held-out equipment.

Step-by-step explanation

fold_absolute_errors = pd.Series(-negative_error_scores)
fold_absolute_errors stores positive mean absolute error for each validation fold.

print(fold_absolute_errors.round(4).tolist())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(round(float(fold_absolute_errors.mean()), 4))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(round(float(fold_absolute_errors.std(ddof=0)), 4))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
[0.5657, 0.7333, 0.7221, 0.7835]
0.7012
0.0815

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

## Slide 48: group_split(records)

Required interface: group_split(records)

Assign whole equipment groups: E1–E4 to train, E5 to validation, E6 to test.

Return train, validation and test lists of record_id in input order.

Do not use target values to choose membership.

Keep these exact output keys and the function name. You may use descriptive local variable names, such as true_positive_count, but the returned dictionary must use the published key, such as tp. The grader checks keys and values; changing a key changes the interface.

## Slide 49: predict_regression(training_records, feature_records)

Required interface: predict_regression(training_records, feature_records)

Fit a training-mean baseline, linear regression and a decision tree (max_depth=4, random_state=17) using load_pct and ambient_c only.

Return three prediction lists under baseline, linear and tree.

Feature records have no target.

Fit preprocessing only on training data.

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

## Slide 51: Validation and trust submission

Validation and trust submission
Explanation to give
This slide hands over CML3113 W10. Show the exact form title before uploading. The required packet is one completed .ipynb notebook.

Worked illustration / lecturer answer
The recorded cutoff for this form is 2026-11-20T08:00:00+03:00. Check the live form for later changes. A replacement must contain the complete required file set, not just the changed file.

Misconception to address
Students enter their own Student Registration Number as required freeform text. They wait for filenames to appear, press Submit and keep the confirmation. A file saved in Drive or GitHub is not itself a form submission.

On this slide
Opens: 13 Nov 2026, 08:00 Kampala

Deadline: 20 Nov 2026, 08:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

## Slide 52: Week 10 quiz

Week 10 quiz
Explanation to give
This is the CML3113 Week 1 quiz. The student link opens the response form; it does not activate its window. In Quiz Controls use open_W1_CML3113 when ready and read the logged closing time.

Worked illustration / lecturer answer
Explain the distinction between the expected answering time and availability: five minutes of questions can still be available for 24 hours after activation. Enter the learner’s own Student Registration Number and use the registered Google account.

Misconception to address
Read the exact live cutoff before announcing it. Do not promise a new attempt to somebody who already submitted. Quiz catch-up and assignment uploads are separate forms.

On this slide
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

Check the announced quiz closing time.

## Slide 53: Revision and submission checklist

Revision and submission checklist
Explanation to give
Connect evaluation to intended use. Decide how to hold out observations before fitting either preprocessing or the linear_model.

Worked illustration / lecturer answer
When testing new equipment, all observations from equipment A stay in one partition. Training must not learn its missing-value replacements from held-out equipment.

Misconception to address
Close by identifying the actual saved file and its correct submission route. Read the live deadline. For current weekly notebook tasks, students upload their own work, not the practice notebook, ZIP or grading files.

On this slide
You can identify which records may influence preprocessing and model selection.

Save your work and check the required submission files.

## Slide 54: Optional revision video

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