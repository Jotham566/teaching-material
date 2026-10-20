# CML3112 Week 9

## Slide 1: Classification and the cost of mistakes

Classification and the cost of mistakes
Explanation to give
Move from a numerical prediction to a category decision. Name the positive class before counting correct warnings, false alarms and missed warnings.

Worked illustration / lecturer answer
Actual 1 with predicted 0 is a false negative. If 1 means warning, this is a missed warning, not merely a wrong number.

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

raw_data = pd.read_csv('classification_case.csv')
raw_data stores original CSV table; keep it unchanged so the analysis can be checked.

print(raw_data.head())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(raw_data.shape)
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(raw_data.dtypes)
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
actual  predicted
0       1          1
1       0          0
2       1          0
3       1          1
4       0          1
(6, 2)
actual       int64
predicted    int64
dtype: object

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 8: Every paired result belongs in one cell

Every paired result belongs in one cell
Explanation to give
First name what 1 means. Read the actual label before the prediction. True/false refers to whether the prediction is correct; positive/negative refers to the predicted class.

Worked illustration / lecturer answer
With 1 meaning warning: actual 1, predicted 0 is a false negative, a missed warning. Actual 0, predicted 1 is a false positive, an unnecessary warning.

Misconception to address
Positive does not mean good. A high count of correct normal cases can hide a dangerous number of missed warnings.

On this slide
Read actual first, then predicted_values. Explain the missed warning.

## Slide 9: Counting the supplied paired labels

True positive: actual 1 and predicted 1. False negative: actual 1 and predicted 0. False positive: actual 0 and predicted 1. True negative: both 0. Keep the two columns paired.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 10: Operations for the next example

Selecting columns
equipment_data["column"] returns one labelled column, a Series. equipment_data[["a", "b"]] returns a DataFrame containing those named columns in that order.

Column arithmetic
Arithmetic on columns calculates one result per row. Series align by row label. Divide only where the denominator is valid and keep actual and predicted observations paired.

Adding values and counting True
series.sum() adds its values. For a Boolean mask, True counts as 1 and False as 0. equipment_data.isna().sum() therefore counts missing cells separately for each column.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 11: Selecting rows with a mask

A column comparison produces one True or False per row. table[mask] keeps the True rows. & combines masks: both conditions must hold. Parenthesise each comparison.
Explain these operations before running the following example.

## Slide 12: Keep observations and decisions paired

actual contains the recorded class; predicted contains the model’s decision for the same row. Here 1 means positive and 0 negative. These are already-issued decisions; this exercise does not train a classifier.

## Slide 13: Confusion counts from classification_case.csv — step 1

actual contains the recorded class; predicted contains the model’s decision for the same row. Here 1 means positive and 0 negative. These are already-issued decisions; this exercise does not train a classifier.

Step-by-step explanation

actual_labels = raw_data['actual']
actual_labels stores the recorded class of each observation: 1 means positive and 0 means negative.

predicted_labels = raw_data['predicted']
predicted_labels stores the model’s 0/1 class decisions in matching row order.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 14: Turn each class label into a question

actual == 1 asks whether the real class is positive; predicted == 1 asks whether the model predicted positive. Each comparison returns one True/False answer per row. Equality uses ==; assignment uses =.

## Slide 15: Confusion counts from classification_case.csv — step 2

actual == 1 asks whether the real class is positive; predicted == 1 asks whether the model predicted positive. Each comparison returns one True/False answer per row. Equality uses ==; assignment uses =.

Step-by-step explanation

actual_is_positive = actual_labels == 1
actual_is_positive stores the result of the displayed expression.

prediction_is_positive = predicted_labels == 1
prediction_is_positive stores the result of the displayed expression.

actual_is_negative = actual_labels == 0
actual_is_negative stores the result of the displayed expression.

prediction_is_negative = predicted_labels == 0
prediction_is_negative stores the result of the displayed expression.

print(actual_is_positive.head())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(prediction_is_positive.head())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
0     True
1    False
2     True
3     True
4    False
Name: actual, dtype: bool
0     True
1    False
2    False
3     True
4     True
Name: predicted, dtype: bool

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 16: Count one outcome at a time

A true positive has actual 1 AND predicted 1. Combine the two answer columns with &, then sum the True entries. The other three outcomes use their own pairs of actual and predicted labels.

## Slide 17: Confusion counts from classification_case.csv — step 3

A true positive has actual 1 AND predicted 1. Combine the two answer columns with &, then sum the True entries. The other three outcomes use their own pairs of actual and predicted labels.

Step-by-step explanation

is_true_positive = actual_is_positive & prediction_is_positive
is_true_positive stores the result of the displayed expression.

true_positive_count = int(is_true_positive.sum())
true_positive_count stores number of rows with actual 1 and predicted 1.

print('True positives:', true_positive_count)
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
True positives: 3

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 18: Confusion counts from classification_case.csv — step 4

false_negative_count: number of missed positives: actual 1 but predicted 0.

false_positive_count: number of false alarms: actual 0 but predicted 1.

## Slide 19: Confusion counts from classification_case.csv — step 4 (1/3)

false_negative_count: number of missed positives: actual 1 but predicted 0.

false_positive_count: number of false alarms: actual 0 but predicted 1.

Step-by-step explanation

false_negative_count = int((actual_is_positive & prediction_is_negative).sum())
false_negative_count stores number of missed positives: actual 1 but predicted 0.

false_positive_count = int((actual_is_negative & prediction_is_positive).sum())
false_positive_count stores number of false alarms: actual 0 but predicted 1.

true_negative_count = int((actual_is_negative & prediction_is_negative).sum())
true_negative_count stores number of rows with actual 0 and predicted 0.

print(false_negative_count, false_positive_count, true_negative_count)
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(true_positive_count + false_negative_count + false_positive_count + true_negative_count, len(raw_data))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
1 1 1
6 6

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 20: Confusion counts from classification_case.csv — step 4 (2/3)

false_negative_count: number of missed positives: actual 1 but predicted 0.

false_positive_count: number of false alarms: actual 0 but predicted 1.

Step-by-step explanation

false_negative_count = int((actual_is_positive & prediction_is_negative).sum())
false_negative_count stores number of missed positives: actual 1 but predicted 0.

false_positive_count = int((actual_is_negative & prediction_is_positive).sum())
false_positive_count stores number of false alarms: actual 0 but predicted 1.

true_negative_count = int((actual_is_negative & prediction_is_negative).sum())
true_negative_count stores number of rows with actual 0 and predicted 0.

print(false_negative_count, false_positive_count, true_negative_count)
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(true_positive_count + false_negative_count + false_positive_count + true_negative_count, len(raw_data))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
1 1 1
6 6

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 21: Confusion counts from classification_case.csv — step 4 (3/3)

false_negative_count: number of missed positives: actual 1 but predicted 0.

false_positive_count: number of false alarms: actual 0 but predicted 1.

Step-by-step explanation

false_negative_count = int((actual_is_positive & prediction_is_negative).sum())
false_negative_count stores number of missed positives: actual 1 but predicted 0.

false_positive_count = int((actual_is_negative & prediction_is_positive).sum())
false_positive_count stores number of false alarms: actual 0 but predicted 1.

true_negative_count = int((actual_is_negative & prediction_is_negative).sum())
true_negative_count stores number of rows with actual 0 and predicted 0.

print(false_negative_count, false_positive_count, true_negative_count)
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

print(true_positive_count + false_negative_count + false_positive_count + true_negative_count, len(raw_data))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
1 1 1
6 6

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 22: Precision recall and cost

Precision asks how many warnings were correct. Recall asks how many real warning cases were found. Neither alone shows all mistakes. The cost is not an approved safety limit.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 23: Operations for the next example

Rounded display
series.round(3) returns values rounded to three decimal places. Python round(number, 3) rounds one number. Keep unrounded calculations for returned assessment answers.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 24: Checking a condition before calculating

if condition: runs its indented statements only when the condition is True. else: handles the other case. Check for a nonzero denominator before division, and for a nonempty table before selecting its first row.
Explain these operations before running the following example.

## Slide 25: Precision: how trustworthy are positive predictions?

The denominator is all predicted positives: true positives plus false positives. Divide correct positive predictions by that total. Check the denominator before dividing; this teaching example uses 0 when it is zero.

## Slide 26: Metrics from the supplied outcomes — step 1

The denominator is all predicted positives: true positives plus false positives. Divide correct positive predictions by that total. Check the denominator before dividing; this teaching example uses 0 when it is zero.

Step-by-step explanation

precision = 0.0
precision stores fraction of positive predictions that are correct.

if true_positive_count + false_positive_count > 0:
    precision = true_positive_count / (true_positive_count + false_positive_count)
Check the condition first, then run only the matching branch. This avoids invalid division or selecting a row that does not exist.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 27: Recall: how many real positives were found?

The denominator is all actual positives: true positives plus false negatives. Divide detected positives by that total. Precision and recall answer different questions even when they happen to have the same value.

## Slide 28: Metrics from the supplied outcomes — step 2

The denominator is all actual positives: true positives plus false negatives. Divide detected positives by that total. Precision and recall answer different questions even when they happen to have the same value.

Step-by-step explanation

recall = 0.0
recall stores fraction of actual positives detected by the model.

if true_positive_count + false_negative_count > 0:
    recall = true_positive_count / (true_positive_count + false_negative_count)
Check the condition first, then run only the matching branch. This avoids invalid division or selecting a row that does not exist.

Verified result with the supplied CSV
This cell stores values for the next example; it does not print a result.

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 29: Metrics from the supplied outcomes — step 3

total_error_cost: five penalty units per missed positive plus one per false alarm in this scenario.

## Slide 30: Metrics from the supplied outcomes — step 3

total_error_cost: five penalty units per missed positive plus one per false alarm in this scenario.

Step-by-step explanation

total_error_cost = 5 * false_negative_count + false_positive_count
total_error_cost stores five penalty units per missed positive plus one per false alarm in this scenario.

print(round(precision, 4), round(recall, 4), total_error_cost)
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
0.75 0.75 6

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 31: Probabilities and thresholds

A threshold at 0.5 labels probabilities at least 0.5 as positive. Do not treat existing 0/1 labels as original probability estimates. Threshold selection requires held-out probability validation_predictions.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 32: Category indicators

This is a representation demonstration. Do not use predicted labels as model input features to predict those same labels. A multiclass metric needs a stated policy for every class.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 33: Operations for the next example

Reading chained operations
Read a chain from left to right. In equipment_data["target"].mean(), select the target Series first, then calculate its mean. Each step uses the previous step’s result.

Category indicator columns
pd.get_dummies(column, prefix="class", dtype=int) creates a 0/1 column per category. prefix names the columns, such as class_0 and class_1. dtype=int displays integers.

Returning plain values
series.tolist() or array.tolist() returns a Python list of values, without pandas row labels. Preserve their order when pairing actual values and validation_predictions.

Reference: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

## Slide 34: Indicators from the supplied class labels

Reading chained operations: Read a chain from left to right. In equipment_data["target"].mean(), select the target Series first, then calculate its mean. Each step uses the previous step’s mean_load_by_equipment_group.

Category indicator columns: pd.get_dummies(column, prefix="class", dtype=int) creates a 0/1 column per category. prefix names the columns, such as class_0 and class_1. dtype=int displays integers.

Returning plain values: series.tolist() or array.tolist() returns a Python list of values, without pandas row labels. Preserve their order when pairing actual values and validation_predictions.

Step-by-step explanation

class_indicator_columns = pd.get_dummies(raw_data['predicted'], prefix='class', dtype=int)
class_indicator_columns stores one integer 0/1 column for each predicted class.

print(class_indicator_columns.head())
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

actual_values = raw_data['actual'].tolist()
actual_values stores observed targets or labels in the order used for comparison.

predicted_values = raw_data['predicted'].tolist()
predicted_values stores predictions aligned with those actual values.

print(len(actual_values), len(predicted_values))
Display these values in the order written. Read their labels and units; displaying them does not alter the stored calculation.

Verified result with the supplied CSV
class_0  class_1
0        0        1
1        1        0
2        1        0
3        0        1
4        0        1
6 6

Run this complete example after the preceding examples. Continuation slides belong to the same notebook cell.

## Slide 35: Your issued task

Your issued task
Explanation to give
The warning labels and costs belong to this teaching scenario. Name what positive means before discussing benefit or harm.

Worked illustration / lecturer answer
Compute the confusion counts from aligned actual/predicted labels, then apply the published cost weights. A false alarm and a missed warning can have different costs.

Misconception to address
These illustrative costs are not approved operational thresholds. Claimed benefits need evaluation on relevant real observations before use in engineering decisions.

On this slide
Use classification_case.csv.

Positive means a synthetic warning condition.

Compute the confusion matrix, precision, recall and total_error_cost.

Explain the 5:1 missed-warning/false-alarm cost assumption and why accuracy alone is insufficient.

## Slide 36: Your issued task continued

Your issued task continued
Explanation to give
The warning labels and costs belong to this teaching scenario. Name what positive means before discussing benefit or harm.

Worked illustration / lecturer answer
Compute the confusion counts from aligned actual/predicted labels, then apply the published cost weights. A false alarm and a missed warning can have different costs.

Misconception to address
These illustrative costs are not approved operational thresholds. Claimed benefits need evaluation on relevant real observations before use in engineering decisions.

On this slide
These costs are teaching assumptions, not approved operating limits.

## Slide 37: classification_metrics(actual, predicted)

Required interface: classification_metrics(actual, predicted)

Return dictionary keys tp, tn, fp, fn, precision, recall and cost.

tp = true positives; tn = true negatives; fp = false positives; fn = false negatives.

cost = 5 * fn + fp. Return zero when a precision or recall denominator is zero.

Keep these exact output keys and the function name. You may use descriptive local variable names, such as true_positive_count, but the returned dictionary must use the published key, such as tp. The grader checks keys and values; changing a key changes the interface.

## Slide 38: Written evidence

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

## Slide 39: Classification and cost submission

Classification and cost submission
Explanation to give
This slide hands over CML3112 W09. Show the exact form title before uploading. The required packet is one completed .ipynb notebook.

Worked illustration / lecturer answer
The recorded cutoff for this form is 2026-11-10T11:00:00+03:00. Check the live form for later changes. A replacement must contain the complete required file set, not just the changed file.

Misconception to address
Students enter their own Student Registration Number as required freeform text. They wait for filenames to appear, press Submit and keep the confirmation. A file saved in Drive or GitHub is not itself a form submission.

On this slide
Opens: 03 Nov 2026, 11:00 Kampala

Deadline: 10 Nov 2026, 11:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

## Slide 40: Week 9 quiz

Week 9 quiz
Explanation to give
This is the CML3112 Week 9 quiz. The student link opens the response form; it does not activate its window. In Quiz Controls use open_W9_CML3112 when ready and read the logged closing time.

Worked illustration / lecturer answer
Explain the distinction between the expected answering time and availability: five minutes of questions can still be available for 24 hours after activation. Enter the learner’s own Student Registration Number and use the registered Google account.

Misconception to address
Read the exact live cutoff before announcing it. Do not promise a new attempt to somebody who already submitted. Quiz catch-up and assignment uploads are separate forms.

On this slide
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

Check the announced quiz closing time.

## Slide 41: Revision and submission checklist

Revision and submission checklist
Explanation to give
Move from a numerical prediction to a category decision. Name the positive class before counting correct warnings, false alarms and missed warnings.

Worked illustration / lecturer answer
Actual 1 with predicted 0 is a false negative. If 1 means warning, this is a missed warning, not merely a wrong number.

Misconception to address
Close by identifying the actual saved file and its correct submission route. Read the live deadline. For current weekly notebook tasks, students upload their own work, not the practice notebook, ZIP or grading files.

On this slide
You can identify a false negative and explain precision and recall with counts.

Save your work and check the required submission files.

## Slide 42: Optional revision video

Optional revision video
Explanation to give
Give the viewing question before playing the excerpt: Which observations are correctly or incorrectly classified?

Worked illustration / lecturer answer
Use the adjacent worked example as the explanation if the video cannot load. Pause after the relevant example and connect its terms to the names and units already used in this lesson. Preview the displayed link and excerpt before class.

Misconception to address
The video is supporting revision, not a replacement for defining the symbols or a requirement to watch a full tutorial during limited class time.

On this slide
For revision after class.

StatQuest with Josh Starmer
Machine Learning Fundamentals The Confusion Matrix

Opening up to 04:00, optional preview-selected excerpt

Listening question: Which observations are correctly or incorrectly classified?

Reference / existing resource
https://www.youtube.com/watch?v=Kdsp6soqA7o