# CML3111 Week 14

## Slide 1: Preparing for Practical Test 2

Send this deck and CML3111_Test2_practice.csv together several days before Test 2. The CSV contains synthetic practice reading_values. All worked data examples use this file. Practice is ungraded. The later test-day section uses different files from the timed portal.

## Slide 2: Your revision files

Share the CSV as a separate attachment beside the PPTX. Students do not need an assessment packet or grader. The practice CSV is intentionally small so they can check every calculation by hand.

## Slide 3: Practice and test-day files

The clearly named practice file avoids confusing it with engineering_data.csv. Portal timing applies to test downloads, not the practice attachment. The repository remains public by the lecturer’s decision, so portal timing is not a claim that public repository files are private.

## Slide 4: A new practice notebook in Colab

A notebook holds code cells and output. Later cells use names created by earlier cells. Confirm the name and saved status. Students do not need a test notebook for this revision.

## Slide 5: Uploading your practice CSV

The Files panel uploads to the temporary session, not into the notebook itself. A FileNotFoundError usually means the file was not uploaded, its filename differs, or the session reset. Do not upload the PPTX into Colab. Avoid a duplicate download name ending in (1).

## Slide 6: What each column means

These are synthetic teaching values, not measurements from an operating site. A row contains one measurement and its associated input conditions. target is a column name, not a unit. M1 and M2 are invented equipment identifiers. read_csv displays missing numeric values as NaN.

## Slide 7: Reading a CSV with pandas

A DataFrame is a table with named columns. The equals sign assigns a result to a name. CSV means comma-separated values. Python is case-sensitive, including the practice_filename.

## Slide 8: Reading the code syntax / Import and short names

= assigns a value to a name; == compares values. Parentheses pass inputs or continue an expression across lines. print displays a value; len counts entries. int and float convert to integer and decimal numeric values.

import pandas as pd loads pandas and gives it the short name pd. pd.read_csv refers to a function in that library.
Explain these operations before running the following example.

## Slide 9: Reading a CSV

pd.read_csv("filename.csv") reads the named file into a DataFrame: a table with labelled columns and row labels. The file must exist in the working folder.
Explain these operations before running the following example.

## Slide 10: Loading the supplied practice file

pd.read_csv("filename.csv") reads the named file into a DataFrame: a table with labelled columns and row labels. The file must exist in the working folder.

Step-by-step explanation

import pandas as pd
Load the named tools. Importing a model class does not train a model.

practice_filename = 'CML3111_Test2_practice.csv'
practice_filename stores the exact name of the accompanying revision CSV.

practice_data = pd.read_csv(practice_filename)
practice_data stores the small practice table read from that CSV.

print(practice_data)
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(len(practice_data))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
reading machine  load  target  ambient
0        1      M1    20      10     20.0
1        2      M1    40      20      NaN
2        3      M2    60      30     30.0
3        4      M2    80      40     40.0
4

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 11: A separate working table / Returning plain values

table.copy() creates a working copy. Assigning columns on this copy preserves the source table, so you can compare before and after.

series.tolist() or array.tolist() returns a Python list of values, without pandas row labels. Preserve their order when pairing actual values and predictions.
Explain these operations before running the following example.

## Slide 12: Selecting columns

table["column"] returns one labelled column, a Series. table[["a", "b"]] returns a DataFrame containing those named columns in that order.
Explain these operations before running the following example.

## Slide 13: Keeping the source table

table["column"] returns one labelled column, a Series. table[["a", "b"]] returns a DataFrame containing those named columns in that order.

Step-by-step explanation

raw_data = practice_data.copy()
raw_data stores original CSV table; keep it unchanged so the analysis can be checked.

print(raw_data['target'].tolist())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
[10, 20, 30, 40]

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 14: Inputs, targets and held-out data

For this small practice, only one feature is used. The assessed notebook specifies its own required feature_columns. Training, validation and final test are roles for data, not different versions of a student paper. A final test estimate becomes optimistic if repeatedly used to select a linear_model.

## Slide 15: Selecting groups without mixing machines

The practice uses M1 for training and M2 for validation to keep the example short. It has no separate final test set. A real test task specifies additional equipment groups. A row-wise random split could place readings from the same machine on both sides.

## Slide 16: Selecting labelled rows / Membership in a group list

table.loc[row_mask] selects rows whose mask is True. With column labels, .loc selects named columns too. .copy() makes a separate working table after selection.

series.isin(["E1", "E2"]) returns True for entries matching either listed label. table[that_mask] keeps all observations belonging to those groups.
Explain these operations before running the following example.

## Slide 17: A small group split

table.loc[row_mask] selects rows whose mask is True. With column labels, .loc selects named columns too. .copy() makes a separate working table after selection.

series.isin(["E1", "E2"]) returns True for entries matching either listed label. table[that_mask] keeps all observations belonging to those groups.

Step-by-step explanation

training_data = raw_data.loc[raw_data['machine'].isin(['M1'])].copy()
training_data stores rows used to learn model settings; only these rows may determine imputation values.

validation_data = raw_data.loc[raw_data['machine'].isin(['M2'])].copy()
validation_data stores separate rows used to compare models without fitting on them.

print(training_data['target'].tolist())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(validation_data['target'].tolist())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
[10, 20]
[30, 40]

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 18: A baseline before a fitted model

Training targets are 10 and 20, so their mean is 15. The baseline predicts 15 for both validation rows even though their actual targets are 30 and 40. This is a benchmark rather than a model that responds to the input load.

## Slide 19: Repeating a baseline value / Mean of recorded values

[training_target_mean] is a one-item list. Multiplying that list by the number of validation rows repeats its value once per row. This is list repetition, not multiplication of the mean itself.

series.mean() adds known values and divides by their count. pandas skips missing values by default. The result has the same unit as the original column.
Explain these operations before running the following example.

## Slide 20: Training-mean baseline

[training_target_mean] is a one-item list. Multiplying that list by the number of validation rows repeats its value once per row. This is list repetition, not multiplication of the mean itself.

series.mean() adds known values and divides by their count. pandas skips missing values by default. The result has the same unit as the original column.

Step-by-step explanation

training_target_mean = training_data['target'].mean()
training_target_mean stores mean target calculated from training rows only.

baseline_predictions = [training_target_mean] * len(validation_data)
baseline_predictions stores the training mean repeated once per validation observation.

print(baseline_predictions)
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
[np.float64(15.0), np.float64(15.0)]

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 21: Mean absolute error and RMSE

For actual [30, 40] and predicted [15, 15], errors are [15, 25]. MAE = (15 + 25)/2 = 20. Squared errors are [225, 625]. Their mean is 425, whose square root is about 20.62. Squaring penalises larger errors more strongly.

## Slide 22: Matching predictions to the correct rows

The validation table retained original labels 2 and 3. The baseline list becomes a Series labelled 0 and 1. Resetting the actual labels lets corresponding values subtract correctly. Resetting labels cannot fix an incorrectly reordered prediction list.

## Slide 23: Column arithmetic / Squared error and square root

Arithmetic on columns calculates one result per row. Series align by row label. Divide only where the denominator is valid and keep actual and predicted observations paired.

error ** 2 squares each error. After averaging, ** 0.5 takes the square root. This gives root mean squared error, which penalises large errors more strongly than mean absolute error.
Explain these operations before running the following example.

## Slide 24: Aligning positions for subtraction / A labelled column

series.reset_index(drop=True) replaces old row labels with 0, 1, 2, and so on. drop=True discards the old labels. Apply it when pairing with a new prediction Series that has those positional labels.

pd.Series(values) creates a one-dimensional labelled sequence. With an array of fold errors, the default labels are 0, 1, 2 and so on.
Explain these operations before running the following example.

## Slide 25: Rounded display / Magnitude of each error

series.round(3) returns values rounded to three decimal places. Python round(number, 3) rounds one number. Keep unrounded calculations for returned assessment answers.

series.abs() makes negative values positive while leaving nonnegative values unchanged. Averaging these magnitudes gives mean absolute error.
Explain these operations before running the following example.

## Slide 26: Calculating baseline errors — step 1

actual_values: observed targets or labels in the order used for comparison.

predicted_values: predictions aligned with those actual values.

## Slide 27: Calculating baseline errors — step 1

actual_values: observed targets or labels in the order used for comparison.

predicted_values: predictions aligned with those actual values.

Step-by-step explanation

actual_values = validation_data['target'].reset_index(drop=True)
actual_values stores observed targets or labels in the order used for comparison.

predicted_values = pd.Series(baseline_predictions)
predicted_values stores predictions aligned with those actual values.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 28: Compare the baseline with observed targets

Pair each baseline prediction with its validation target. reset_index(drop=True) makes their row labels match by position before subtraction. The training mean must come from training rows only.

## Slide 29: Calculating baseline errors — step 2

Pair each baseline prediction with its validation target. reset_index(drop=True) makes their row labels match by position before subtraction. The training mean must come from training rows only.

Step-by-step explanation

baseline_errors = actual_values - predicted_values
baseline_errors stores observed validation targets minus baseline predictions.

mae = baseline_errors.abs().mean()
mae stores mean absolute error in the target unit.

rmse = (baseline_errors ** 2).mean() ** 0.5
rmse stores root mean squared error in the target unit.

print(round(mae, 2), round(rmse, 2))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
20.0 20.62

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 30: Practice: compare two predictions

The negative second error means overprediction. A negative error is not automatically a good prediction. Absolute and squared errors prevent positive and negative errors cancelling. Small invented validation data does not demonstrate generalisation to real equipment.

## Slide 31: Practice answer

The negative second error means overprediction. A negative error is not automatically a good prediction. Absolute and squared errors prevent positive and negative errors cancelling. Small invented validation data does not demonstrate generalisation to real equipment.

## Slide 32: Fitting and predicting with scikit-learn

One pair of brackets gives a Series. Double brackets provide a list of column names and keep a DataFrame, which scikit-learn expects for X. y is a one-dimensional target Series. The four practice targets follow target = load / 2 exactly, so the two validation predictions should be 30 and 40.

## Slide 33: Creating linear regression / Learning from training examples

LinearRegression() creates an unfitted model. It will learn coefficients and an intercept from training examples. Creating it alone does not train it or make predictions.

model.fit(input_table, observed_targets) learns model settings from paired rows. The two inputs must describe the same observations in the same order. Call fit before predict.
Explain these operations before running the following example.

## Slide 34: Predicting new targets

model.predict(input_table) returns one prediction per input row. Use the same feature columns and order as during training. Prediction uses learned settings; it does not refit the model.
Explain these operations before running the following example.

## Slide 35: Standard names for model inputs

These are common machine-learning conventions. Some tutorials write train_x and train_y instead. The names are chosen by the programmer, not special Python keywords. Keep training_data as the full table; selecting X_train must exclude target. Rows in X and y must stay paired. fit uses training pairs; predict receives only X_valid. Compare predictions with y_valid afterwards.

## Slide 36: Separate inputs from answers

X_train contains the input columns; y_train contains their observed targets. X_valid contains the same input columns for validation; y_valid holds the answers for checking predictions. Never include target among the inputs.

## Slide 37: A fitted linear model — step 1

X_train contains the input columns; y_train contains their observed targets. X_valid contains the same input columns for validation; y_valid holds the answers for checking predictions. Never include target among the inputs.

Step-by-step explanation

X_train = training_data[['load']]
X_train stores training input columns, excluding the target.

y_train = training_data['target']
y_train stores observed training targets in matching row order.

X_valid = validation_data[['load']]
X_valid stores validation input columns in training-column order.

y_valid = validation_data['target']
y_valid stores observed validation targets, used only for evaluation.

from sklearn.linear_model import LinearRegression
Load the named tools. Importing a model class does not train a model.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 38: Create, then train, then predict

Creating an estimator sets up an empty model. fit learns settings from training inputs and their targets. predict uses those learned settings on new inputs; it does not learn from the validation targets.

## Slide 39: A fitted linear model — step 2

Creating an estimator sets up an empty model. fit learns settings from training inputs and their targets. predict uses those learned settings on new inputs; it does not learn from the validation targets.

Step-by-step explanation

linear_model = LinearRegression()
linear_model stores the linear regression estimator or imputation-and-regression pipeline.

linear_model.fit(X_train, y_train)
model.fit(input_table, observed_targets) learns model settings from paired rows. The two inputs must describe the same observations in the same order. Call fit before predict.

validation_predictions = linear_model.predict(X_valid)
validation_predictions stores one predicted target for each validation row, in the same order.

print(validation_predictions.round(2))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
[30. 40.]

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 40: Missing values and a fair model comparison

Revise the pipeline and decision-tree examples from the previous teaching weeks. Fit SimpleImputer on the training partition only, even though it does not use target values. A tree learns splits and can overfit. Compare errors on the same rows, and follow the supplied model settings. The first linear example uses only load, which has no missing values. The following pipeline adds ambient and learns its missing-value replacement from training rows.

## Slide 41: A pipeline with a median imputer

The training ambient values are 20 and missing, so the learned ambient median is 20. The full-data median would be 30, which includes validation information. That is why filling the entire source table before splitting is wrong for model evaluation.

## Slide 42: The model tools — step 1

feature_columns: the list of input column names supplied to the model.

## Slide 43: The model tools — step 1

feature_columns: the list of input column names supplied to the model.

Step-by-step explanation

from sklearn.impute import SimpleImputer
Load the named tools. Importing a model class does not train a model.

from sklearn.pipeline import make_pipeline
Load the named tools. Importing a model class does not train a model.

from sklearn.tree import DecisionTreeRegressor
Load the named tools. Importing a model class does not train a model.

feature_columns = ['load', 'ambient']
feature_columns stores the list of input column names supplied to the model.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 44: Separate inputs from answers

X_train contains the input columns; y_train contains their observed targets. X_valid contains the same input columns for validation; y_valid holds the answers for checking predictions. Never include target among the inputs.

## Slide 45: The model tools — step 2

X_train contains the input columns; y_train contains their observed targets. X_valid contains the same input columns for validation; y_valid holds the answers for checking predictions. Never include target among the inputs.

Step-by-step explanation

X_train = training_data[feature_columns]
X_train stores training input columns, excluding the target.

X_valid = validation_data[feature_columns]
X_valid stores validation input columns in training-column order.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 46: A sequence of model steps / Filling model inputs

make_pipeline(imputer, estimator) links preprocessing and prediction. fit learns the imputer and estimator on training rows. predict applies the learned steps to new rows in the same order.

SimpleImputer(strategy="median") learns a median for each input column during fit. It uses those training medians to fill gaps later. Never learn replacement values from validation or test rows.
Explain these operations before running the following example.

## Slide 47: A linear pipeline

make_pipeline(imputer, estimator) links preprocessing and prediction. fit learns the imputer and estimator on training rows. predict applies the learned steps to new rows in the same order.

SimpleImputer(strategy="median") learns a median for each input column during fit. It uses those training medians to fill gaps later. Never learn replacement values from validation or test rows.

Step-by-step explanation

linear_pipeline = make_pipeline(SimpleImputer(strategy='median'), LinearRegression())
linear_pipeline stores median imputer followed by linear regression.

linear_pipeline.fit(X_train, y_train)
model.fit(input_table, observed_targets) learns model settings from paired rows. The two inputs must describe the same observations in the same order. Call fit before predict.

linear_predictions = linear_pipeline.predict(X_valid)
linear_predictions stores validation predictions from the linear pipeline.

print(linear_predictions.round(2))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
[30. 40.]

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 48: A shallow decision tree

The two training loads are 20 and 40. A split near 30 separates their targets 10 and 20. Both validation loads, 60 and 80, follow the higher-load branch and receive 20. Trees do not extend a fitted straight line beyond the training range.

## Slide 49: Creating a regression tree

DecisionTreeRegressor splits inputs into regions with different predicted values. max_depth limits the number of split levels. random_state fixes random choices so the example can be repeated.
Explain these operations before running the following example.

## Slide 50: Compare a second kind of model

A regression tree learns splits in the input columns. max_depth limits its split levels. The imputer fills missing inputs using training medians; the tree then learns from those filled inputs.

## Slide 51: A tree pipeline

A regression tree learns splits in the input columns. max_depth limits its split levels. The imputer fills missing inputs using training medians; the tree then learns from those filled inputs.

Step-by-step explanation

tree_model = make_pipeline(SimpleImputer(strategy='median'), DecisionTreeRegressor(max_depth=2, random_state=7))
tree_model stores the tree regression pipeline being compared on the same validation rows.

tree_model.fit(X_train, y_train)
model.fit(input_table, observed_targets) learns model settings from paired rows. The two inputs must describe the same observations in the same order. Call fit before predict.

tree_predictions = tree_model.predict(X_valid)
tree_predictions stores validation predictions from the tree pipeline.

print(tree_predictions)
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
[20. 20.]

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 52: Practice: compare the three models

The tree errors are 10 and 20, so MAE is 15 and RMSE is sqrt(250), about 15.81. The zero linear error follows the deliberately exact relationship. A separate final test set is still required for an unbiased final evaluation; this miniature example only demonstrates training and validation_data.

## Slide 53: Practice answer

The tree errors are 10 and 20, so MAE is 15 and RMSE is sqrt(250), about 15.81. The zero linear error follows the deliberately exact relationship. A separate final test set is still required for an unbiased final evaluation; this miniature example only demonstrates training and validation_data.

## Slide 54: Test 2 revision checklist

All worked predictions come from the attached CSV. M1 is training and M2 validation_data. The actual test specifies additional groups, a final held-out group, model settings and function return formats. The practice file is intentionally smaller.

## Slide 55: Functions and returned answers

The automated grader calls functions with other equipment_records. A pasted fixed answer can match a displayed example and still fail for another input. print displays a value but does not replace return. The following practice function is unrelated to the assessed function names.

## Slide 56: Defining and calling a function

def gives a reusable block a name and input parameters. The indented statements run when it is called. return sends a result back to the caller; print displays a result but does not return it.
Explain these operations before running the following example.

## Slide 57: A practice function

def gives a reusable block a name and input parameters. The indented statements run when it is called. return sends a result back to the caller; print displays a result but does not return it.

Step-by-step explanation

def average_reading(values):
    reading_values = pd.Series(values)
    return float(reading_values.mean())
Define the function. Explain each input before the call. Its body runs only when called; return supplies the computed value.

print(average_reading(raw_data['target']))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(average_reading(raw_data['load']))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
25.0
50.0

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 58: Recording interpretation answers

DECISIONS is a Python dictionary in the notebook. Its keys identify questions and its string values hold selected option letters. Use the labels printed in that question. A choice label is unrelated to file allocation. No student should select a paper version or edit the internal allocation cell.

## Slide 59: A dictionary entry for a practice question



Step-by-step explanation

DECISIONS = {'practice': 'B'}
DECISIONS stores the result of the displayed expression.

print(DECISIONS['practice'])
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
B

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 60: Test-day instructions

Pause at this boundary when reviewing in advance. The remaining slides are procedural instructions, not additional practice tasks. No practice file should be submitted to the test form.

## Slide 61: Your test files on test day

The page assigns files automatically. Students do not choose a version. Re-entering the same registration number and Google email retrieves the same allocation. The page can be opened in advance, but downloads are available only during the authorised test window. A phone scan is useful for opening the page, but students must download and use both files on their laptop. Students never choose a test version.

## Slide 62: Opening the notebook and CSV

A notebook upload does not include its modelling_data. Show the folder icon, then Upload. Wait until engineering_data.csv appears. Do not upload a ZIP. The portal prefills the identity cell; students check it and run it before later cells. The final submission cell contains an internal allocation code and is collapsed for clarity. Keep it unchanged.

## Slide 63: One notebook contains all answers

A function is a named block of code. The grader calls that function with different records, so it must calculate from its argument. DECISIONS is a dictionary pairing each question identifier with one option letter. Use a non-assessed demonstration such as {"practice": "B"}. No separate report or prose answer section is required.

## Slide 64: How the 100 marks are allocated

Explain that all marks come from the published checks. Correct code on unseen inputs earns coding marks. Each of the six interpretation choices earns 5 marks. Test 1 contributes 15 points and Test 2 contributes 20 points to the semester total. For example, 80/100 in Test 1 contributes 12 semester points. Partial marks are available for independently checked outputs; charts and cleaning each have a complete contract.

## Slide 65: Order of work

Test 1: duplicate removal keeps the first occurrence. Exclude a missing target or invalid load. Only then calculate the retained ambient median. Test 2: row filters are supplied, but missing ambient values remain. A pipeline learns the median from the training partition and reuses it for validation_data. Fitting a median on all rows leaks evaluation information. Do not reveal assessed option answers during the test_data.

## Slide 66: The three-hour session

Announce the actual start and close time displayed by the form. These periods total 180 minutes. Code execution is allowed during checking. Report internet or runtime problems immediately. Record incidents with the affected learner and time. Do not silently treat a failed upload as a submitted test_data.

## Slide 67: Before submitting

A fresh session has no variables from earlier runs. This exposes cells that depend on stale values or an incorrect order. The supplied CSV example cell calls the implemented functions. The final submission cell creates a button. Clicking it prepares a separate snapshot of the current notebook in Drive; later edits to the working notebook do not change that snapshot. Students must open the generated form link and press Submit. The button alone is not a completed submission.

## Slide 68: Submission and confirmation

Demonstrate the final button using a rehearsal notebook. The button privately shares a saved snapshot with the lecturer and fills the form fields. Tick the form’s email confirmation box before pressing Submit. Do not type snapshot IDs manually. The form records the verified Google email; it must be the same account that owns the snapshot. A new attempt requires clicking the notebook button again and submitting its new form link. The latest on-time attempt is considered; technical or identity errors remain pending. Earlier attempts are retained.

## Slide 69: How grading works

Grades are calculated in a batch on the lecturer’s Mac after the test_data. The Mac can be off during submission. Google Forms and Drive collect the snapshots. Before admitting students, rehearse the entry page, two downloads, notebook button and form confirmation. After the test, export the batch and run Grade_Tests.command with Docker running. A receipt is not a grade. A genuine zero is distinct from pending or infrastructure failure. The attendee register is built from submissions; without an enrolled roster it cannot identify absentees.