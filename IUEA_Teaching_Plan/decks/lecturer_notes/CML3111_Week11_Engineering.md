# CML3111 Week 11

## Slide 1: Creating and testing a useful feature

Creating and testing a useful feature
Explanation to give
Explain why a calculated input may help and test the idea under an unchanged validation protocol.

Worked illustration / lecturer answer
If validation MAE falls from 5 to 4 after adding one feature, the reduction is 1 target unit, or 20%. A comparison on a different split cannot isolate that change.

Misconception to address
Use this as an orientation to the lesson. Terms and syntax will be unpacked on their own slides; students do not need to know them in advance.

On this slide
Communications, Electrical, Mechatronics and Robotics Engineering

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
0          1           E1     59.15      31.71  76.847
1          2           E2     77.46      29.97  87.047
2          3           E3     69.60      19.87  71.256
3          4           E4     75.98      22.29     NaN
4          5           E5     57.62      23.40  67.034
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

## Slide 18: A physical relationship can form a feature

A physical relationship can form a feature
Explanation to give
A derived feature is a new input calculated from known inputs. Explain its physical or operational reason and its units before presenting it to a linear_model. An interaction allows one input's effect to depend on another.

Worked illustration / lecturer answer
For load_pct 50 and ambient_c 30, the course interaction load_pct * ambient_c is 1500. Separately, load_pct / 100 gives the fraction 0.5. These are different derived quantities. The interaction is a hypothesis to test, not a measured law.

Misconception to address
A plausible physical story does not guarantee an improvement. Do not use the target or information that would only become available after the prediction.

On this slide
Explain each quantity and the unit of the result.

## Slide 19: Derived features from existing inputs

An interaction has combined units. It is not a new measured physical quantity. Use information available at prediction time.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 20: Operations for the next example

Adding or replacing a column
equipment_data["name"] = values assigns that column. An array follows row order. A Series aligns by row label, so keep labels paired with the intended observations.

Column arithmetic
Arithmetic on columns calculates one result per row. Series align by row label. Divide only where the denominator is valid and keep actual and predicted observations paired.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 21: Defining and calling a function

def gives a reusable block a name and input parameters. The indented statements run when it is called. return sends a result back to the caller; print displays a result but does not return it.
Explain these operations before running the following example.

## Slide 22: Features from the supplied load and ambient columns (1/2)

def gives a reusable block a name and input parameters. The indented statements run when it is called. return sends a result back to the caller; print displays a result but does not return it.

Step-by-step explanation

def add_features(equipment_data):
    extended_data = equipment_data.copy()
    extended_data['load_fraction'] = extended_data['load_pct'] / 100
    extended_data['load_ambient'] = extended_data['load_pct'] * extended_data['ambient_c']
    return extended_data
Define the function. Explain each input before the call. Its body runs only when called; return supplies the computed value.

training_features = add_features(training_data)
training_features stores training table containing the engineered feature columns.

validation_features = add_features(validation_data)
validation_features stores validation table with the same feature calculations applied.

print(training_features[['load_pct', 'load_fraction', 'load_ambient']].head())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
load_pct  load_fraction  load_ambient
0     59.15         0.5915     1875.6465
1     77.46         0.7746     2321.4762
2     69.60         0.6960     1382.9520
6     24.66         0.2466      784.4346
7     72.92         0.7292     2005.3000

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 23: Features from the supplied load and ambient columns (2/2)

def gives a reusable block a name and input parameters. The indented statements run when it is called. return sends a result back to the caller; print displays a result but does not return it.

Step-by-step explanation

def add_features(equipment_data):
    extended_data = equipment_data.copy()
    extended_data['load_fraction'] = extended_data['load_pct'] / 100
    extended_data['load_ambient'] = extended_data['load_pct'] * extended_data['ambient_c']
    return extended_data
Define the function. Explain each input before the call. Its body runs only when called; return supplies the computed value.

training_features = add_features(training_data)
training_features stores training table containing the engineered feature columns.

validation_features = add_features(validation_data)
validation_features stores validation table with the same feature calculations applied.

print(training_features[['load_pct', 'load_fraction', 'load_ambient']].head())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
load_pct  load_fraction  load_ambient
0     59.15         0.5915     1875.6465
1     77.46         0.7746     2321.4762
2     69.60         0.6960     1382.9520
6     24.66         0.2466      784.4346
7     72.92         0.7292     2005.3000

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 24: Ablation compares the same observations

A positive improvement means lower error for the extended linear_model. The four-column make_features output also includes load_fraction, but the ablation comparison uses the three specified extended columns.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 25: Operations for the next example

Rounded display
series.round(3) returns values rounded to three decimal places. Python round(number, 3) rounds one number. Keep unrounded calculations for returned assessment answers.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 26: A sequence of model steps / Comparing two prediction sets

make_pipeline(imputer, estimator) links preprocessing and prediction. fit learns the imputer and estimator on training rows. predict applies the learned steps to new rows in the same order.

mean_absolute_error(actual, predicted) averages the absolute differences of paired values. Lower is better. Both lists must have the same length and row order; the answer has the target’s unit.
Explain these operations before running the following example.

## Slide 27: Filling model inputs / Creating linear regression

SimpleImputer(strategy="median") learns a median for each input column during fit. It uses those training medians to fill gaps later. Never learn replacement values from validation or test rows.

LinearRegression() creates an unfitted model. It will learn coefficients and an intercept from training examples. Creating it alone does not train it or make predictions.
Explain these operations before running the following example.

## Slide 28: Learning from training examples / Predicting new targets

model.fit(input_table, observed_targets) learns model settings from paired rows. The two inputs must describe the same observations in the same order. Call fit before predict.

model.predict(input_table) returns one prediction per input row. Use the same feature columns and order as during training. Prediction uses learned settings; it does not refit the model.
Explain these operations before running the following example.

## Slide 29: Change one feature set at a time

The base inputs are load and ambient temperature. The extended inputs also include their product. Train separate pipelines on the same rows and compare on the same validation rows. This isolates the effect of adding the feature.

## Slide 30: Paired ablation using the supplied CSV — step 1

The base inputs are load and ambient temperature. The extended inputs also include their product. Train separate pipelines on the same rows and compare on the same validation rows. This isolates the effect of adding the feature.

Step-by-step explanation

from sklearn.impute import SimpleImputer
Load the named tools. Importing a model class does not train a model.

from sklearn.pipeline import make_pipeline
Load the named tools. Importing a model class does not train a model.

from sklearn.linear_model import LinearRegression
Load the named tools. Importing a model class does not train a model.

from sklearn.metrics import mean_absolute_error
Load the named tools. Importing a model class does not train a model.

base_feature_columns = ['load_pct', 'ambient_c']
base_feature_columns stores input columns for the simpler comparison pipeline.

extended_feature_columns = base_feature_columns + ['load_ambient']
extended_feature_columns stores base columns plus the interaction feature being tested.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 31: Fit both alternatives fairly

Each pipeline learns its own training medians and regression settings. The base model sees only base columns; the extended model sees the additional feature. Neither uses validation targets while learning.

## Slide 32: Paired ablation using the supplied CSV — step 2 (1/2)

Each pipeline learns its own training medians and regression settings. The base model sees only base columns; the extended model sees the additional feature. Neither uses validation targets while learning.

Step-by-step explanation

base_pipeline = make_pipeline(SimpleImputer(strategy='median'), LinearRegression())
base_pipeline stores imputer and regression model using only the base columns.

extended_pipeline = make_pipeline(SimpleImputer(strategy='median'), LinearRegression())
extended_pipeline stores a separate imputer and regression model using the extended columns.

base_pipeline.fit(training_features[base_feature_columns], training_data['target'])
model.fit(input_table, observed_targets) learns model settings from paired rows. The two inputs must describe the same observations in the same order. Call fit before predict.

extended_pipeline.fit(training_features[extended_feature_columns], training_data['target'])
model.fit(input_table, observed_targets) learns model settings from paired rows. The two inputs must describe the same observations in the same order. Call fit before predict.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 33: Paired ablation using the supplied CSV — step 2 (2/2)

Each pipeline learns its own training medians and regression settings. The base model sees only base columns; the extended model sees the additional feature. Neither uses validation targets while learning.

Step-by-step explanation

base_pipeline = make_pipeline(SimpleImputer(strategy='median'), LinearRegression())
base_pipeline stores imputer and regression model using only the base columns.

extended_pipeline = make_pipeline(SimpleImputer(strategy='median'), LinearRegression())
extended_pipeline stores a separate imputer and regression model using the extended columns.

base_pipeline.fit(training_features[base_feature_columns], training_data['target'])
model.fit(input_table, observed_targets) learns model settings from paired rows. The two inputs must describe the same observations in the same order. Call fit before predict.

extended_pipeline.fit(training_features[extended_feature_columns], training_data['target'])
model.fit(input_table, observed_targets) learns model settings from paired rows. The two inputs must describe the same observations in the same order. Call fit before predict.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 34: Compare errors on the same rows

Predict both alternatives on matching validation rows. mean_absolute_error compares each prediction with its observed target. Base MAE minus extended MAE is positive when the extra feature helped on this validation set.

## Slide 35: Paired ablation using the supplied CSV — step 3

Predict both alternatives on matching validation rows. mean_absolute_error compares each prediction with its observed target. Base MAE minus extended MAE is positive when the extra feature helped on this validation set.

Step-by-step explanation

base_predictions = base_pipeline.predict(validation_features[base_feature_columns])
base_predictions stores validation predictions from the base pipeline.

base_absolute_error = mean_absolute_error(validation_data['target'], base_predictions)
base_absolute_error stores validation mean absolute error for the base pipeline.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 36: Paired ablation using the supplied CSV — step 4

extended_predictions: validation predictions from the extended pipeline.

extended_absolute_error: validation mean absolute error for the extended pipeline.

## Slide 37: Paired ablation using the supplied CSV — step 4 (1/2)

extended_predictions: validation predictions from the extended pipeline.

extended_absolute_error: validation mean absolute error for the extended pipeline.

Step-by-step explanation

extended_predictions = extended_pipeline.predict(validation_features[extended_feature_columns])
extended_predictions stores validation predictions from the extended pipeline.

extended_absolute_error = mean_absolute_error(validation_data['target'], extended_predictions)
extended_absolute_error stores validation mean absolute error for the extended pipeline.

print(round(base_absolute_error, 4), round(extended_absolute_error, 4))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(round(base_absolute_error - extended_absolute_error, 4))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
0.7775 0.7992
-0.0217

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 38: Paired ablation using the supplied CSV — step 4 (2/2)

extended_predictions: validation predictions from the extended pipeline.

extended_absolute_error: validation mean absolute error for the extended pipeline.

Step-by-step explanation

extended_predictions = extended_pipeline.predict(validation_features[extended_feature_columns])
extended_predictions stores validation predictions from the extended pipeline.

extended_absolute_error = mean_absolute_error(validation_data['target'], extended_predictions)
extended_absolute_error stores validation mean absolute error for the extended pipeline.

print(round(base_absolute_error, 4), round(extended_absolute_error, 4))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(round(base_absolute_error - extended_absolute_error, 4))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
0.7775 0.7992
-0.0217

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 39: Pandas inside the required function

Keep the original function names and return types. Do not read a fixed CSV inside the assessed function: hidden tests supply different equipment_records. The separate calling cell reads the CSV.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 40: Operations for the next example

Returning a dictionary
series.to_dict() maps Series labels to values. equipment_data.to_dict("records") instead returns a list of row dictionaries. Choose the form required by the assignment.

A table from Python values
pd.DataFrame(records) builds a table from row dictionaries. With a dictionary of column lists, keys become column names and each list supplies that column’s values.

Mean of recorded values
series.mean() adds known values and divides by their count. pandas skips missing values by default. The result has the same unit as the original column.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 41: Operations for the next example

Grouping rows
equipment_data.groupby("label")["value"] groups the value column by matching labels. Apply mean() or sum() to calculate one result per group. Missing group labels are excluded by default.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 42: A function called with the supplied records

Grouping rows: equipment_data.groupby("label")["value"] groups the value column by matching labels. Apply mean() or sum() to calculate one result per group. Missing group labels are excluded by default.

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

## Slide 43: Your issued task

Your issued task
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

## Slide 44: make_features(feature_records)

Required interface: make_features(feature_records)

Return one feature row per input, in order: [load_pct, ambient_c, load_pct/100, load_pct*ambient_c].

Use inputs available at prediction time only.

Keep these exact output keys and the function name. You may use descriptive local variable names, such as true_positive_count, but the returned dictionary must use the published key, such as tp. The grader checks keys and values; changing a key changes the interface.

## Slide 45: ablation_metrics(training_records, validation_records)

Required interface: ablation_metrics(training_records, validation_records)

Fit two sklearn LinearRegression models on the same training records: base features [load_pct, ambient_c] and extended features adding load_pct*ambient_c.

Evaluate both on the same validation records.

Return base_mae, extended_mae and improvement=base_mae-extended_mae, without rounding.

Inputs are complete; never fit on validation targets.

Keep these exact output keys and the function name. You may use descriptive local variable names, such as true_positive_count, but the returned dictionary must use the published key, such as tp. The grader checks keys and values; changing a key changes the interface.

## Slide 46: Written evidence

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

## Slide 47: Features and ablation submission

Features and ablation submission
Explanation to give
This slide hands over CML3111 W11. Show the exact form title before uploading. The required packet is one completed .ipynb notebook.

Worked illustration / lecturer answer
The recorded cutoff for this form is 2026-11-27T11:00:00+03:00. Check the live form for later changes. A replacement must contain the complete required file set, not just the changed file.

Misconception to address
Students enter their own Student Registration Number as required freeform text. They wait for filenames to appear, press Submit and keep the confirmation. A file saved in Drive or GitHub is not itself a form submission.

On this slide
Opens: 20 Nov 2026, 11:00 Kampala

Deadline: 27 Nov 2026, 11:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

## Slide 48: Project preparation

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

Published deadline: 18 Dec 2026, 11:00 Kampala

## Slide 49: Week 11 quiz

Week 11 quiz
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

## Slide 50: Revision and submission checklist

Revision and submission checklist
Explanation to give
Explain why a calculated input may help and test the idea under an unchanged validation protocol.

Worked illustration / lecturer answer
If validation MAE falls from 5 to 4 after adding one feature, the reduction is 1 target unit, or 20%. A comparison on a different split cannot isolate that change.

Misconception to address
Close by identifying the actual saved file and its correct submission route. Read the live deadline. For current weekly notebook tasks, students upload their own work, not the practice notebook, ZIP or grading files.

On this slide
You can state the new feature’s meaning and calculate an improvement correctly.

Save your work and check the required submission files.