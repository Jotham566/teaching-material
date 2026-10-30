# CML3111 Week 14

Each slide shows its text, then the spoken script the lecturer reads aloud.

## Slide 1: Preparing for Practical Test 2

Communications, Electrical, Mechatronics and Robotics Engineering

Advance revision and test-day guide
Test time: confirm with the lecturer

**Spoken script**

Welcome to Week 14. This week we get ready for Practical Test 2, and this deck is for Communications, Electrical, Mechatronics and Robotics Engineering.

Everything in here is revision. We have already met every idea in Weeks 8 to 13, and we prepared for the first test the same way in Week 7. No new code appears today.

We will walk through a whole small test on a practice file, one step at a time, and then we will go through the instructions for test day. The slide says to confirm the test time with the lecturer, so please check it with me.

## Slide 2: Your revision files

01

Use this slide deck and CML3111_Test2_practice.csv. Save both on your laptop.

02

Work through the examples in order in a new Colab notebook. Try each practice question before reading its answer.

03

Practice is ungraded. Keep your notebook for revision. No form submission is needed.

**Spoken script**

You need two things for revision: this slide deck and the practice CSV file named on the slide. Please save both on your laptop.

Open a new Colab notebook and work through the examples in order. For each practice question, try it yourself first, and only then read the answer. That is how the ideas stick.

The practice is ungraded. Nobody marks it, and there is no form to submit. Keep your notebook, because it is a good record to look back on before the test.

## Slide 3: Practice and test-day files

01

BEFORE THE TEST: use CML3111_Test2_practice.csv with the worked examples in this section.

02

ON TEST DAY: the entry page provides a different notebook and engineering_data.csv.

03

The test downloads unlock only during the scheduled test window.

**Spoken script**

There are two sets of files, and it helps to keep them apart in your mind.

Before the test, you use the practice CSV with the worked examples in this deck. It is a small file, made to practise on.

On test day, the entry page gives you a different notebook and a file called engineering underscore data dot csv. Those are the real test materials.

The test downloads unlock only during the scheduled test window, so you will not be able to open them early. You do not need them for revision. The practice file gives you everything you need.

## Slide 4: A new practice notebook in Colab

01

Open colab.research.google.com and sign in. Choose New notebook. Rename it Test revision.

02

Click Connect. Add a code cell with + Code. Run a cell with its triangle button.

03

Run cells from top to bottom. Save with File, then Save.

**Spoken script**

We start by making a fresh notebook in Colab, which is Google's free place for running Python in the browser.

Open colab dot research dot google dot com and sign in. Choose New notebook, and rename it Test revision, so you can find it again.

Next, click Connect. This gives you a computer in the cloud to run your code. A code cell is a box where you type code. Add one with the plus Code button, and run it with the triangle button beside it.

Run your cells from top to bottom, because later cells use names that earlier cells created. Save with File, then Save.

## Slide 5: Uploading your practice CSV

01

In Colab, click the folder icon on the left. Click Upload and choose CML3111_Test2_practice.csv.

02

Wait until the filename appears in the Files panel. Keep its name unchanged.

03

If the session resets, upload the file again before running your cells.

**Spoken script**

Colab cannot see files on your laptop until you upload them, so we upload the practice CSV now.

Click the folder icon on the left. Click Upload, and choose the practice file from your laptop.

Wait until the file name appears in the Files panel, and keep the name exactly as it is. Our code will use that exact name to find the file.

Colab keeps uploaded files only for the current session. If the session resets, the file disappears, so upload it again before you run your cells. If you ever see a file not found message, check these three things: the upload, the spelling of the name, and whether the session reset.

## Slide 6: What each column means

01

reading identifies one measurement. machine identifies the equipment that produced it.

02

load is the equipment load in percent. target is motor temperature, measured in °C.

03

ambient is the surrounding air temperature in °C. A blank cell means the value is missing.

**Spoken script**

Before we touch any code, we need to know what the practice table contains. It has five columns.

The reading column identifies one measurement. The machine column tells us which piece of equipment produced it.

The load column is how hard the equipment is working, as a percentage. The target column is the motor temperature in degrees Celsius. The target is the thing we want to predict.

The ambient column is the temperature of the surrounding air, also in degrees Celsius. A blank cell means that value is missing, and we will see how pandas shows that. These are invented teaching values.

## Slide 7: Reading a CSV with pandas

01

import pandas as pd loads pandas and gives it the short name pd.

02

pd.read_csv(filename) reads the uploaded file. The filename is text, so it needs quotation marks.

03

A name stores the resulting DataFrame. print(table) displays it, and len(table) counts its rows.

**Spoken script**

Reading the file takes three small steps.

First, import pandas as pd loads the pandas library and gives it the short name pd, so we do not have to type the long name each time.

Second, pd dot read underscore csv reads a CSV file. CSV means comma separated values, a plain text table. We give it the file name. The file name is text, so it must sit inside quotation marks.

Third, we store the result under a name of our choice. What we get back is called a DataFrame, which is a table with named columns. Then print shows the table, and len counts how many rows it has.

## Slide 8: Reading the code syntax / Import and short names

= assigns a value to a name; == compares values. Parentheses pass inputs or continue an expression across lines. print displays a value; len counts entries. int and float convert to integer and decimal numeric values.

import pandas as pd loads pandas and gives it the short name pd. pd.read_csv refers to a function in that library.

**Spoken script**

Let us revisit the small symbols we will see in the code, so none of them surprises you.

A single equals sign gives a value a name. Two equals signs compare two values. Parentheses hand inputs to a function, and they can also let one long expression continue onto the next line.

The word print shows a value on the screen. The word len counts how many entries something has. The words int and float turn a value into a whole number or a decimal number.

Finally, import pandas as pd loads pandas and gives it the short name pd. When we write pd dot read underscore csv, we are asking pandas to use its read underscore csv function.

## Slide 9: Reading a CSV

pd.read_csv("filename.csv") reads the named file into a DataFrame: a table with labelled columns and row labels. The file must exist in the working folder.

**Spoken script**

Here is the main idea behind reading a CSV file. We write pd dot read underscore csv, and in brackets we put the file name inside quotation marks.

Pandas opens that file and builds a DataFrame from it. A DataFrame is a table with labelled columns, and each row has its own label too, which is a number starting from zero.

One condition matters. The file must exist in the working folder. In Colab that means you must have uploaded it in the current session. If the name is spelled differently from the file, pandas cannot find it and shows an error. Capital letters count, so copy the name carefully.

## Slide 10: Loading the supplied practice file

practice_filename: the exact name of the accompanying revision CSV.

Compare the printed result with the explanation in the notebook.

```python
import pandas as pd
practice_filename = "CML3111_Test2_practice.csv"
practice_data = pd.read_csv(practice_filename)
print(practice_data)
print(len(practice_data))
```

**Spoken script**

Now we load the practice file. We type this code in one cell.

The first line imports pandas as pd. The second line stores the exact file name of the practice CSV in a name called practice underscore filename. The third line calls pd dot read underscore csv with that name and stores the table in practice underscore data.

The fourth line prints the table, and the fifth prints its length.

You should see four rows, with columns reading, machine, load, target and ambient. One ambient cell shows N a N, which is how pandas displays a missing number. The length printed is four. Compare what you see with the explanation in your notebook.

## Slide 11: A separate working table / Returning plain values

table.copy() creates a working copy. Assigning columns on this copy preserves the source table, so you can compare before and after.

series.tolist() or array.tolist() returns a Python list of values, without pandas row labels. Preserve their order when pairing actual values and predictions.

**Spoken script**

Two small tools come next.

The first is dot copy. It makes a separate copy of a table. When we change columns on the copy, the original stays as it was, so we can compare before and after.

The second is dot tolist. It turns a column of values into a plain Python list, without the row labels that pandas attaches. A list is easy to read on the screen.

When we line up actual values with predictions later, the order matters, so we keep the order of the values unchanged. We will use both tools in the next example.

## Slide 12: Selecting columns

table["column"] returns one labelled column, a Series. table[["a", "b"]] returns a DataFrame containing those named columns in that order.

**Spoken script**

Now we recall how to pick columns out of a table.

If we write the table name followed by one column name in quotation marks inside square brackets, we get back that single column. Pandas calls this a Series, which is one labelled column of values.

If we write two pairs of square brackets with column names inside, we get back a smaller table, a DataFrame, containing just those columns in the order we listed them.

The outer brackets select, and the inner brackets make a list of names. Later, the model will want its inputs as a table, so we will use the double bracket form.

## Slide 13: Keeping the source table

raw_data: original CSV table; keep it unchanged so the analysis can be checked.

Compare the printed result with the explanation in the notebook.

```python
raw_data = practice_data.copy()
print(raw_data["target"].tolist())
```

**Spoken script**

The first habit for the test is to keep a raw copy of the data.

We write raw underscore data equals practice underscore data dot copy. This makes a separate table that holds the original rows exactly as they came from the file.

Then print takes the target column of raw underscore data and turns it into a list with tolist. You should see a list of four numbers: ten, twenty, thirty and forty.

We leave raw underscore data alone from now on. If a later cleaning step goes wrong, we can come back to this table and check what the original numbers were. Compare your printed list with the explanation in the notebook.

## Slide 14: Inputs, targets and held-out data

01

Features are the input columns used to predict. In this example, load is the feature and target is the measured result.

02

Training rows teach the model. Validation rows help compare models.

03

Keep final test rows untouched until the model choice is complete.

**Spoken script**

Next we name the roles that data plays.

Features are the input columns we use to make a prediction. In this practice example, load is the feature, and target is the measured result we want to predict.

Training rows are the rows the model learns from. Validation rows are separate rows that we use to check and compare models.

There is also a final test set. We keep those rows untouched until we have finished choosing a model. If we keep peeking at them while we choose, their score stops being an honest check. In this small practice file we use only one feature, and the real test tells you which feature columns to use.

## Slide 15: Selecting groups without mixing machines

01

isin(["M1"]) marks rows belonging to the listed machine.

02

.loc[mask] keeps the rows marked True. .copy() creates a separate table.

03

A machine must belong to one data partition. Otherwise its patterns may leak into evaluation.

**Spoken script**

Our rows come from machines, and several readings come from the same machine. So we split by machine, and each machine goes entirely to one side.

The isin method checks each row and marks it True if its machine is in the list we give. For example, isin with M1 in a list marks all the M1 rows.

Then dot loc with that mask keeps only the rows marked True. Adding dot copy makes a separate working table.

A machine must belong to one partition only. If readings from the same machine sit on both sides, the model has already seen that machine's pattern when we check it, and the result looks better than it should. In this practice file M1 is used for training and M2 for validation.

## Slide 16: Selecting labelled rows / Membership in a group list

table.loc[row_mask] selects rows whose mask is True. With column labels, .loc selects named columns too. .copy() makes a separate working table after selection.

series.isin(["E1", "E2"]) returns True for entries matching either listed label. table[that_mask] keeps all observations belonging to those groups.

**Spoken script**

Here are the two tools for picking rows, explained once more.

The dot loc tool selects the rows where a mask is True. A mask is a column of True and False answers, one for each row. If we also give column labels, dot loc selects those named columns too. Adding dot copy afterwards gives a separate working table.

The isin method builds that mask. It returns True for every entry that matches any label in our list. For example, we can ask for entries equal to E1 or E2.

When we apply the mask to the table, we keep all the readings belonging to those groups. No group is cut in half.

## Slide 17: A small group split

training_data: rows used to learn model settings; only these rows may determine imputation values.

Compare the printed result with the explanation in the notebook.

```python
training_data = raw_data.loc[
    raw_data["machine"].isin(["M1"])
].copy()
validation_data = raw_data.loc[
    raw_data["machine"].isin(["M2"])
].copy()
print(training_data["target"].tolist())
print(validation_data["target"].tolist())
```

**Spoken script**

Now we do the group split in code.

The first statement builds training underscore data. It takes raw underscore data, keeps the rows where the machine column is M1, and copies them.

The second statement builds validation underscore data in the same way, with M2.

The last two lines print the target column of each table as a list. You should see ten and twenty for training, and thirty and forty for validation.

The training rows are the only rows allowed to decide any fill-in values or model settings. The validation rows are kept for checking afterwards. Compare your output with the explanation in the notebook.

## Slide 18: A baseline before a fitted model

01

A baseline is a simple prediction used for comparison.

02

A mean baseline predicts the training target mean for every new row.

03

Never use validation targets to calculate the training mean.

**Spoken script**

Before we fit any model, we need something simple to beat. That is a baseline. A baseline is a basic prediction that we use for comparison.

The mean baseline works like this. We find the average of the target in the training rows, and we predict that same number for every new row. It ignores load and everything else.

Here the training targets are ten and twenty, so the mean is fifteen. We predict fifteen for both validation rows, even though the real answers are thirty and forty.

One rule matters a lot. Never use the validation targets to calculate the training mean. If we did, the answers we are testing would leak into the prediction.

## Slide 19: Repeating a baseline value / Mean of recorded values

[training_target_mean] is a one-item list. Multiplying that list by the number of validation rows repeats its value once per row. This is list repetition, not multiplication of the mean itself.

series.mean() adds known values and divides by their count. pandas skips missing values by default. The result has the same unit as the original column.

**Spoken script**

Two small ideas appear in the baseline code.

The first is the mean. Dot mean adds up the known values in a column and divides by how many there are. Pandas skips missing values by default. The answer is in the same unit as the column.

The second is list repetition. We put the mean inside square brackets, which makes a list with one item. Multiplying that list by a whole number repeats the item that many times. If there are two validation rows, we get a list with two copies of the mean.

This repeats the value in the list.

## Slide 20: Training-mean baseline

training_target_mean: mean target calculated from training rows only.

Compare the printed result with the explanation in the notebook.

```python
training_target_mean = training_data["target"].mean()
baseline_predictions = [training_target_mean] * len(
    validation_data
)
print(baseline_predictions)
```

**Spoken script**

Here is the baseline in code.

The first line takes the target column of the training data and calls dot mean. We store the answer in training underscore target underscore mean. Since it comes from training rows only, it is a fair baseline.

The second line puts that value in a one item list and multiplies it by len of validation underscore data. That gives one prediction for each validation row.

The last line prints the list. You will see fifteen twice. NumPy, the number library under pandas, may print each value as np.float64. It is still just the decimal number. Compare it with the explanation in your notebook.

## Slide 21: Mean absolute error and RMSE

01

Error = actual value − predicted value. Absolute error removes the sign.

02

MAE is the mean absolute error. RMSE is the square root of the mean squared error.

03

Lower is better on the same held-out rows. Both use the target’s unit.

**Spoken script**

To judge predictions, we measure how far they are from the real answers.

The error for one row is the actual value minus the predicted value. Taking the absolute value removes the minus sign, so we only see how big the miss was.

Mean absolute error, or MAE, is the average of those absolute errors. RMSE is root mean squared error. We square each error, take the average, and then take the square root.

For our baseline, the actual values are thirty and forty and the predictions are fifteen and fifteen. The errors are fifteen and twenty five, so the MAE is twenty. The squared errors are two hundred and twenty five and six hundred and twenty five, with a mean of four hundred and twenty five. Its square root is about twenty point six two.

Lower is better, on the same rows. Both are in the unit of the target.

## Slide 22: Matching predictions to the correct rows

01

Pandas subtracts Series by row label. A filtered table can keep old labels such as 2 and 3.

02

reset_index(drop=True) replaces those labels with 0 and 1. pd.Series(a_list) also starts at 0.

03

Use the same row order for actual values and validation_predictions.

**Spoken script**

There is one catch when we subtract predictions from actual values. Pandas lines up two columns by their row labels, and it does not go by position.

Our validation table was cut out of the original table, so its rows keep their old labels, which are two and three. A new prediction column starts at zero. If we subtract them directly, the labels do not match.

The fix is reset underscore index with drop equals True. It replaces the old labels with zero and one. Calling pd dot Series on a list also starts its labels at zero.

Once the labels agree, each actual value meets its own prediction. The order of the predictions must also match the order of the rows.

## Slide 23: Column arithmetic / Squared error and square root

Arithmetic on columns calculates one result per row. Series align by row label. Divide only where the denominator is valid and keep actual and predicted observations paired.

error ** 2 squares each error. After averaging, ** 0.5 takes the square root. This gives root mean squared error, which penalises large errors more strongly than mean absolute error.

**Spoken script**

Arithmetic on columns works on every row at once. If we subtract one column from another, we get one answer per row.

Because Series line up by row label, we must keep the actual values and the predictions paired properly. If we ever divide, we also make sure the number we divide by is valid.

To square each error, we write error, then two stars, then the number two. That gives the square of every error. After we average the squared errors, we use two stars and zero point five to take the square root.

The result is root mean squared error. It punishes a few large errors more heavily than mean absolute error does.

## Slide 24: Aligning positions for subtraction / A labelled column

series.reset_index(drop=True) replaces old row labels with 0, 1, 2, and so on. drop=True discards the old labels. Apply it when pairing with a new prediction Series that has those positional labels.

pd.Series(values) creates a one-dimensional labelled sequence. With an array of fold errors, the default labels are 0, 1, 2 and so on.

**Spoken script**

Two tools help us match rows by position.

The first is reset underscore index with drop equals True. It throws away the old row labels and numbers the rows zero, one, two and so on. The drop equals True part tells pandas to discard the old labels. We use it when the other Series has those new positional labels.

The second is pd dot Series. It builds a one dimensional labelled sequence from a list or an array. If we give it an array, for example of errors from several folds, the labels it creates are zero, one, two and so on.

With both Series labelled the same way, subtraction pairs the right values.

## Slide 25: Rounded display / Magnitude of each error

series.round(3) returns values rounded to three decimal places. Python round(number, 3) rounds one number. Keep unrounded calculations for returned assessment answers.

series.abs() makes negative values positive while leaving nonnegative values unchanged. Averaging these magnitudes gives mean absolute error.

**Spoken script**

Two small helpers finish our error calculations.

The dot round method with three inside the brackets gives values rounded to three decimal places. Python also has a plain round function that rounds a single number. Rounding is for display. In the test, we keep the unrounded values for any answers we return.

The dot abs method turns negative numbers into positive ones and leaves the others alone. It gives the size of each error. When we average these sizes, we get the mean absolute error.

Use them as the examples show, and your results will match the explanation in the notebook.

## Slide 26: Calculating baseline errors: step 1

actual_values: observed targets or labels in the order used for comparison.

predicted_values: predictions aligned with those actual values.

**Spoken script**

Before we calculate errors, we give two names to the two lists we compare.

The name actual underscore values holds the observed targets, in the order we use for comparison. These are the real answers.

The name predicted underscore values holds the predictions, lined up with those actual values. Row by row, each prediction must match its own actual value.

This step only sets up the two lists. The next slide shows the code that builds them.

## Slide 27: Calculating baseline errors: step 1

actual_values: observed targets or labels in the order used for comparison.

Compare the printed result with the explanation in the notebook.

```python
actual_values = validation_data["target"].reset_index(drop=True)
predicted_values = pd.Series(baseline_predictions)
```

**Spoken script**

Now we build those two lists.

The first line takes the target column from the validation data and resets its index, so its row labels become zero and one. We store it in actual underscore values.

The second line turns the baseline predictions list into a pandas Series with pd dot Series, and stores it in predicted underscore values. Its labels are also zero and one.

This cell prints nothing. It only stores the two sets of values for the next example. Run it anyway, because the next cell needs these names.

## Slide 28: Compare the baseline with observed targets

Pair each baseline prediction with its validation target. reset_index(drop=True) makes their row labels match by position before subtraction.

The training mean must come from training rows only.

**Spoken script**

We now pair each baseline prediction with the validation target it belongs to.

Because the actual values have their row labels reset, the labels match the predictions by position. That lets pandas subtract them correctly, row by row.

One more reminder about fairness. The training mean we use must come from the training rows only. The validation rows are only for checking.

If you are ever unsure, ask yourself which rows each number came from. A number used to fit must come from training. A number used to judge must come from validation.

## Slide 29: Calculating baseline errors: step 2

actual_values: observed targets or labels in the order used for comparison.

Compare the printed result with the explanation in the notebook.

```python
baseline_errors = actual_values - predicted_values
mae = baseline_errors.abs().mean()
rmse = (baseline_errors**2).mean() ** 0.5
print(round(mae, 2), round(rmse, 2))
```

**Spoken script**

Here is the calculation of the baseline errors.

The first line subtracts the predictions from the actual values and stores the errors. The second line takes the absolute value of each error and averages them. That is the mean absolute error.

The third line squares each error, takes the mean, and raises the result to the power zero point five, which is the square root. That is RMSE.

The last line prints both numbers, each rounded to two decimal places. You should see twenty point zero and twenty point six two. These match the hand calculation we did a moment ago. They are the numbers the better models must beat.

## Slide 30: Practice: compare two predictions

01

Actual values are 30 and 40. New predictions are 28 and 44.

02

Calculate the two errors, MAE and RMSE by hand.

03

Does this improve on the baseline MAE of 20?

**Spoken script**

Time for a practice question, and please work it by hand before we look at the answer.

The actual values are thirty and forty. A new set of predictions is twenty eight and forty four.

First, work out the two errors, using actual minus predicted. Then take the absolute values and average them to get the MAE. After that, square the errors, average them, and take the square root to get the RMSE.

Finally, compare your answers with the baseline MAE of twenty. Does this new prediction improve on the baseline? Take a few minutes before moving to the next slide.

## Slide 31: Practice answer

01

Errors: 2 and −4. Absolute errors: 2 and 4.

02

03

Both errors are lower than the baseline on these same two rows.

**Spoken script**

Here is the answer.

The errors are actual minus predicted. Thirty minus twenty eight is two. Forty minus forty four is minus four. The absolute errors are two and four.

The MAE is the average of two and four, which is three degrees Celsius. For the RMSE, the squared errors are four and sixteen. Their mean is ten, and the square root of ten is about three point one six degrees Celsius.

The baseline had a MAE of twenty and an RMSE of about twenty point six two. Both errors here are much lower, on these same two rows. The negative sign on the second error tells us we predicted too high.

## Slide 32: Fitting and predicting with scikit-learn

01

LinearRegression learns a straight-line relationship. fit(X, y) learns from training features and targets.

02

predict(X_new) uses the fitted relationship on new feature_columns. It does not receive their targets.

03

Double brackets, [["load"]], retain a two-dimensional feature equipment_data.

**Spoken script**

Now we bring in a real model from scikit-learn, a library of machine learning tools.

LinearRegression learns a straight line relationship between the inputs and the target. The method fit takes the training features and the training targets, and learns that line from them.

The method predict takes new feature columns and uses the fitted line to give predictions. It never receives the answers for those rows.

One detail about shape. We write load with two pairs of square brackets, so we get back a table with one column. Scikit-learn expects its inputs as a table. In this practice file, the four targets follow load divided by two exactly, so the line fits the data perfectly.

## Slide 33: Creating linear regression / Learning from training examples

LinearRegression() creates an unfitted model. It will learn coefficients and an intercept from training examples. Creating it alone does not train it or make predictions.

model.fit(input_table, observed_targets) learns model settings from paired rows. The two inputs must describe the same observations in the same order. Call fit before predict.

**Spoken script**

Using a model takes two steps, and the order matters.

Writing LinearRegression with empty brackets creates a model that has not learned anything yet. Later it will learn coefficients, which are the slopes, and an intercept, which is the prediction when load is zero. Creating the model does not train it, and it cannot make predictions yet.

The method fit does the learning. We give it the input table and the observed targets. They must describe the same rows in the same order, so row one of the inputs matches row one of the targets.

We always call fit before predict.

## Slide 34: Predicting new targets

model.predict(input_table) returns one prediction per input row. Use the same feature columns and order as during training. Prediction uses learned settings; it does not refit the model.

**Spoken script**

After fit, we can use the model to predict.

The method predict takes an input table and gives back one prediction for each row. The table must have the same feature columns, in the same order, as the one we used for training. If it does not, the model has no way to read it correctly.

Predicting uses the settings the model has already learned. It does not fit the model again, and it does not look at any targets for the new rows.

This is why we can test a model on validation rows honestly. The model has never seen their answers.

## Slide 35: Standard names for model inputs

01

X_train: training input columns. y_train: the matching observed targets.

02

X_valid: validation input columns. y_valid: their observed targets, kept for evaluation.

03

Capital X usually means a two-dimensional table; lowercase y usually means one target per row.

**Spoken script**

Machine learning code uses a few standard names, and they appear in the practice code.

X underscore train holds the training input columns. y underscore train holds the matching observed targets.

X underscore valid holds the validation input columns. y underscore valid holds their observed targets, and we keep these aside for checking.

The capital X is a reminder that the inputs form a table, with rows and columns. The lowercase y reminds us that there is one target value per row.

These are only naming habits. Some books write train x and train y. We are the ones who choose the names, and the code works with any names as long as we use them consistently. The target column must never appear inside X.

## Slide 36: Separate inputs from answers

X_train contains the input columns; y_train contains their observed targets.

X_valid contains the same input columns for validation; y_valid holds the answers for checking predictions.

Never include target among the inputs.

**Spoken script**

When we train a model, we keep two kinds of columns apart. The inputs are the columns the model is allowed to look at. The answers are the values we want it to predict. In our practice file the input is load, and the answer is target.

We give these standard names. X underscore train holds the input columns for the training rows, and y underscore train holds their observed targets. X underscore valid holds the same input columns for the validation rows. Y underscore valid holds the validation answers, and we keep them aside to check the predictions afterwards.

One rule matters most. The column called target never goes among the inputs. If the answer sits inside the inputs, the model just reads it, and the result tells us nothing.

## Slide 37: A fitted linear model: step 1

X_train: input columns used for training.

Compare the printed result with the explanation in the notebook.

```python
X_train = training_data[["load"]]
y_train = training_data["target"]
X_valid = validation_data[["load"]]
y_valid = validation_data["target"]
from sklearn.linear_model import LinearRegression
```

**Spoken script**

This cell prepares four names and loads the linear regression tool. It prints nothing, so a blank result here is correct.

The first line takes the training table and selects the load column inside double square brackets. The double brackets keep it as a table with one column, which is the shape the model expects for inputs. We store it as X underscore train.

The second line selects target with single brackets. That gives one answer per row, and we store it as y underscore train.

The third and fourth lines do the same for the validation table. X underscore valid holds the validation loads, and y underscore valid holds the validation targets that we use only for checking.

The last line imports LinearRegression from scikit-learn. Importing only brings the tool into the notebook. It does not train anything yet.

## Slide 38: Create, then train, then predict

Creating an estimator sets up an empty model. fit learns settings from training inputs and their targets. predict uses those learned settings on new inputs; it does not learn from the validation targets.

**Spoken script**

Every model we use follows three steps, always in the same order.

First we create it. Creating a model gives us an empty one. It has learned nothing yet, so it cannot predict anything useful.

Second we call fit. Fit hands the model the training inputs together with their training targets. The model studies the pairs and learns its settings. For a straight line, those settings are how steeply it rises and the prediction when load is zero.

Third we call predict. Predict hands the model new inputs, such as the validation rows. It applies what it learned and gives one prediction per row. It never sees the validation targets and it learns nothing from them. We compare its predictions with those targets ourselves, afterwards, when we calculate the errors.

## Slide 39: A fitted linear model: step 2

X_train: input columns used for training.

Compare the printed result with the explanation in the notebook.

```python
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
validation_predictions = linear_model.predict(X_valid)
print(validation_predictions.round(2))
```

**Spoken script**

This cell builds the model, trains it, and predicts.

The first line creates an empty linear regression and stores it under the name linear underscore model.

The second line calls fit with X underscore train and y underscore train. Here the model learns the straight line that links load to target in the training rows.

The third line calls predict on X underscore valid. We get one predicted target for every validation row, in the same order as the rows. We store these as validation underscore predictions.

The last line prints them, rounded to two decimal places.

The output is thirty and forty. These match the actual validation targets exactly, because in this small practice file the targets follow the loads in a perfect straight line. Real test data will never be that tidy, so a perfect result here is a good sign that our code works, and nothing more.

## Slide 40: Missing values and a fair model comparison

01

An imputer learns replacement values, such as a median, from training features only.

02

A pipeline applies the same learned replacement before fitting or predicting.

03

Compare the baseline, linear model and tree on the same validation rows. Keep final test rows separate.

**Spoken script**

This slide gathers three ideas we already met in earlier weeks.

Some cells in our data are blank. A model cannot work with a blank, so we fill it with a replacement value. A tool called an imputer does this. It learns the replacement value, for example the median of a column, and it learns it from the training rows only. If it looked at validation rows, information from the exam paper would leak into our preparation.

A pipeline joins steps into one chain. It applies the same learned replacement before fitting and before predicting, so we never forget it.

Finally, a fair comparison means the baseline, the linear model and the tree are all judged on the same validation rows. The final test rows stay untouched until we have chosen our model.

## Slide 41: A pipeline with a median imputer

01

SimpleImputer(strategy="median") learns one median per training feature.

02

make_pipeline(imputer, model) applies the imputer before the model.

03

Calling fit on the pipeline learns both stages using training rows only.

**Spoken script**

Here we build the chain that fills blanks and then fits a model.

SimpleImputer with strategy set to median looks at each input column in the training rows and works out its median. The median is the middle value when the numbers are sorted. It remembers one median per column.

The function make underscore pipeline takes the imputer and the model and links them. When data enters the pipeline, the imputer fills the blanks first, and the model then works with the filled table.

When we call fit on the pipeline, both stages learn together, and they learn from the training rows only. In our practice file the training ambient values are twenty and one blank, so the learned ambient median is twenty. If a validation row had a blank ambient temperature, it would receive that same twenty. Here neither validation row is blank. This is why we never fill the whole table before splitting.

## Slide 42: The model tools: step 1

feature_columns: the list of input column names supplied to the model.

**Spoken script**

Before we build the next models, we need to name the input columns the models will use.

The slide that follows shows a short list of names. That list is called feature underscore columns. It holds the column names we give to the model as inputs.

Keeping the names in one list has a practical benefit. We write them once, and then every later line can refer to the list. That keeps training and validation using the same columns in the same order, and it avoids typing mistakes.

## Slide 43: The model tools: step 1

feature_columns: the list of input column names supplied to the model.

Compare the printed result with the explanation in the notebook.

```python
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeRegressor
feature_columns = ["load", "ambient"]
```

**Spoken script**

This cell loads three tools and writes down our input columns. It prints nothing.

The first import brings in SimpleImputer, the tool that fills blank cells. The second brings in make underscore pipeline, which chains steps together. The third brings in DecisionTreeRegressor, a model that predicts by splitting the data into groups. Importing only makes the tools available. No model is trained yet.

The last line creates feature underscore columns, a list holding two names, load and ambient. These are the inputs the next models will use. Ambient has a blank in the data, which is why we need the imputer.

Run the cell and expect no output. That is correct.

## Slide 44: Separate inputs from answers

X_train contains the input columns; y_train contains their observed targets.

X_valid contains the same input columns for validation; y_valid holds the answers for checking predictions.

Never include target among the inputs.

**Spoken script**

We return to the input and answer split, because we now use two input columns instead of one.

X underscore train and X underscore valid are tables of inputs. They contain only the columns the model may look at. Y underscore train holds the matching observed targets for the training rows. Y underscore valid holds the validation answers, which we keep for checking predictions.

The checking comes after predicting. The model never sees y underscore valid while it learns.

When we build the input tables, we choose columns by name, and the name target must never be in that choice. A model that is given the answer as an input would look excellent in practice and would fail on any real data.

## Slide 45: The model tools: step 2

feature_columns: the list of input column names supplied to the model.

Compare the printed result with the explanation in the notebook.

```python
X_train = training_data[feature_columns]
X_valid = validation_data[feature_columns]
```

**Spoken script**

This cell builds the two input tables using the list of names we just made. It prints nothing.

The first line takes the training data and selects the columns named in feature underscore columns, load and ambient. We store the result as X underscore train.

The second line does exactly the same for the validation data and stores X underscore valid.

Because both lines use the same list, the training and validation tables have the same columns in the same order. That matters, because the model learned the columns in that order and expects them again.

The target column is left out of both tables on purpose. The answers stay in y underscore train and y underscore valid.

Expect no printed result.

## Slide 46: A sequence of model steps / Filling model inputs

make_pipeline(imputer, estimator) links preprocessing and prediction. fit learns the imputer and estimator on training rows. predict applies the learned steps to new rows in the same order.

SimpleImputer(strategy="median") learns a median for each input column during fit. It uses those training medians to fill gaps later. Never learn replacement values from validation or test rows.

**Spoken script**

We have two ideas here, and they fit together.

The function make underscore pipeline links a preprocessing step with a model. When we call fit on the pipeline, the preprocessing step and the model both learn from the training rows. When we call predict, the pipeline applies the learned steps to new rows in the same order, so the filling happens first and the prediction second.

The preprocessing step we use is SimpleImputer with strategy set to median. During fit it learns one median for each input column. Later it uses those training medians to fill any blank cell it meets.

The rule to remember is that replacement values are learned from training rows only. Validation and test rows never contribute to them.

## Slide 47: A linear pipeline

linear_pipeline: median imputer followed by linear regression.

Compare the printed result with the explanation in the notebook.

```python
linear_pipeline = make_pipeline(
    SimpleImputer(strategy="median"), LinearRegression()
)
linear_pipeline.fit(X_train, y_train)
linear_predictions = linear_pipeline.predict(X_valid)
print(linear_predictions.round(2))
```

**Spoken script**

This cell builds a linear regression that can cope with blank cells.

The first statement makes a pipeline. Its first step is a median imputer, and its second step is a linear regression. We store it as linear underscore pipeline.

The next line calls fit with X underscore train and y underscore train. The imputer learns the medians from the training rows, fills the blanks, and then the linear regression learns from the filled table.

The next line calls predict on X underscore valid. The pipeline fills any blank in the validation rows using the training medians, and then predicts. We store the results as linear underscore predictions.

The last line prints them, rounded to two decimals. We get thirty and forty again, which matches the validation targets in this tiny practice file.

## Slide 48: A shallow decision tree

01

A regression tree divides training rows using feature thresholds and predicts a value within each resulting group.

02

max_depth limits the number of levels of splits. random_state fixes the random choices for repeatability.

03

With these tiny training data, loads above the observed range receive the larger training target.

**Spoken script**

A decision tree is a different kind of model from a straight line.

A regression tree asks a series of questions about the inputs, such as whether the load is above some value. Each answer leads to a group of training rows. For a new row, the tree gives the average target of the group where the row lands.

Two settings control it. Max underscore depth limits how many levels of questions the tree may ask. Random underscore state fixes any random choices inside the tree, so that everyone running the cell gets the same result.

In our tiny practice data, the training loads are twenty and forty. The validation loads, sixty and eighty, are higher than anything the tree saw. They fall into the higher group and receive that group's target, which is twenty. A tree cannot continue a rising line beyond the training range.

## Slide 49: Creating a regression tree

DecisionTreeRegressor splits inputs into regions with different predicted values. max_depth limits the number of split levels. random_state fixes random choices so the example can be repeated.

**Spoken script**

A decision tree regressor predicts numbers by cutting the input values into regions. Each region gets its own predicted value, based on the training rows that fell into it.

We control it with two settings. The first is max underscore depth. It limits how many levels of splitting the tree may use. A small depth keeps the tree simple, and a very deep tree can memorise the training rows.

The second is random underscore state. Trees can make small random choices, and this setting fixes them. If we all use the same value, we all get the same tree and the same output, so we can compare our results with the notebook.

In the test, use the settings that the notebook supplies.

## Slide 50: Compare a second kind of model

A regression tree learns splits in the input columns. max_depth limits its split levels.

The imputer fills missing inputs using training medians; the tree then learns from those filled inputs.

**Spoken script**

We now add a second kind of model to compare with the straight line.

A regression tree learns splits in the input columns. Each split is a yes or no question about a column, and the answers lead to groups with their own predictions. Max underscore depth limits how many levels of those questions it can ask.

The tree cannot work with blank cells, so it sits inside a pipeline after the imputer. The imputer fills the missing inputs using medians learned from the training rows. The tree then learns from those filled inputs.

Putting both models through the same kind of pipeline keeps the comparison fair. Each one gets the same filled data, and each one is judged on the same validation rows.

## Slide 51: A tree pipeline

tree_model: the tree regression pipeline being compared on the same validation rows.

Compare the printed result with the explanation in the notebook.

```python
tree_model = make_pipeline(
    SimpleImputer(strategy="median"),
    DecisionTreeRegressor(max_depth=2, random_state=7),
)
tree_model.fit(X_train, y_train)
tree_predictions = tree_model.predict(X_valid)
print(tree_predictions)
```

**Spoken script**

This cell builds the tree version of our pipeline and checks it on the validation rows.

The first statement makes a pipeline with two steps. The imputer fills blank cells with training medians. After it comes a decision tree regressor, with max underscore depth set to two and random underscore state set to seven. We store the pipeline as tree underscore model.

Next we call fit with X underscore train and y underscore train. Both steps learn from the training rows.

Then we call predict on X underscore valid, which gives one prediction per validation row, and we store them as tree underscore predictions. The last line prints them.

The output is twenty and twenty. Both validation loads land in the higher group of the tree, and that group holds the training target of twenty. The tree gives a flat answer outside the range it saw, so it is further from the actual thirty and forty than the linear model was.

## Slide 52: Practice: compare the three models

01

Validation targets: 30 and 40.

02

Baseline predictions: 15, 15. Linear: 30, 40. Tree: 20, 20.

03

Calculate MAE and RMSE for each linear_model. Which performs best on these two rows?

**Spoken script**

Now we put the three models side by side on the same two validation rows.

The actual validation targets are thirty and forty. The baseline predicted fifteen and fifteen. The linear model predicted thirty and forty. The tree predicted twenty and twenty.

Your task is to calculate the mean absolute error and the root mean squared error for each of the three. Work from the errors. An error is the actual value minus the predicted value. The absolute error removes the sign. For RMSE, square each error, average the squares, and take the square root.

Try it on paper first, using the same steps we used for the baseline. Then decide which model performs best on these two rows. The next slide gives the answers, so give yourself a real attempt before you move on.

## Slide 53: Practice answer

01

Baseline: MAE 20, RMSE 20.62 °C.

02

Linear: MAE 0, RMSE 0 °C. Tree: MAE 15, RMSE 15.81 °C.

03

Linear performs best here. Two synthetic rows do not prove performance on new equipment.

**Spoken script**

Here are the answers for the three-model comparison.

For the baseline, the MAE is twenty and the RMSE is twenty point six two, in degrees Celsius.

For the linear model, the MAE and the RMSE are both zero, in degrees Celsius. Its predictions of thirty and forty matched the actual validation targets exactly. For the tree, the MAE is fifteen and the RMSE is fifteen point eight one, in degrees Celsius.

The linear model performs best on these two rows.

Remember the limit of this result. Two synthetic rows tell us very little about how a model performs on new equipment. The zero error appears because the practice file was built with an exact straight-line pattern. Real data has noise, which is why the test uses separate groups of machines and unseen data.

## Slide 54: Test 2 revision checklist

01

Explain the machine split and why the ambient median must come from training rows.

02

Rerun both pipelines. Compare their predictions with the baseline on the same validation rows.

03

Calculate MAE and RMSE and explain why a perfect result on this tiny file is not proof of generalisation.

**Spoken script**

This checklist shows what you should be able to do before the test.

First, explain the machine split in your own words. Each machine goes wholly to one side, training or validation, so that no machine appears on both. Then explain why the ambient median must come from training rows. If it came from all rows, the validation rows would influence the filling, and our check would be too kind.

Second, rerun both pipelines in your own notebook, the linear one and the tree. Compare their predictions with the baseline on the same validation rows.

Third, calculate MAE and RMSE, and explain why a perfect result on this tiny file proves nothing about new equipment. The file has very few rows and a pattern that was built to be exact.

If you can do these three things, you are well prepared.

## Slide 55: Functions and returned answers

01

A function is a named calculation. def starts its definition. Indented lines belong to it.

02

An argument supplies the input. return sends the result back to the caller.

03

In the test, keep every supplied function name and calculate from its input.

**Spoken script**

In the test, some answers come from functions, so let us settle what a function is.

A function is a named calculation. The word def starts its definition, and the indented lines underneath belong to it. An argument is the input we hand to the function when we call it. The word return sends the result back to whoever called the function.

On test day, keep every function name exactly as supplied. The grader calls your functions by those names. Calculate from the input the function receives. The grader will call your function with data you have never seen, so a number typed in to match one example will fail on the others.

This is easier than it sounds. We use the same pandas steps we practised, placed inside a function, and we return the final value.

## Slide 56: Defining and calling a function

def gives a reusable block a name and input parameters. The indented statements run when it is called. return sends a result back to the caller; print displays a result but does not return it.

**Spoken script**

A function lets us name a block of code and reuse it.

We start with the word def, then the function's name, then the input names in brackets. Those input names are called parameters. They stand for whatever values we hand over when we call the function.

The lines indented underneath form the body of the function. They do not run when we define it. They run each time we call the function by name with real inputs.

The word return sends a result back to the caller. Print is different. Print shows a value on the screen, but the function does not hand it back, so the caller receives nothing to use. If the test asks a function to return a value, we must use return.

## Slide 57: A practice function

Use the inputs and operations defined in the preceding slides.

Compare the printed result with the explanation in the notebook.

```python
def average_reading(values):
    reading_values = pd.Series(values)
    return float(reading_values.mean())
print(average_reading(raw_data["target"]))
print(average_reading(raw_data["load"]))
```

**Spoken script**

This cell defines a small function and calls it twice.

The first line defines average underscore reading, with one input called values. The next line, indented, turns those values into a pandas Series and stores it as reading underscore values. A Series is one labelled column of values. The following indented line calls the mean method, which adds the values and divides by how many there are. We wrap the answer in float so it comes back as a plain decimal number, and return sends it back.

The last two lines call the function. The first call gives it the target column of our raw copy. The second gives it the load column.

The output is twenty-five and fifty. Those are the averages of the four targets and the four loads. The same function works for both, because it calculates from whatever input it receives. That is how we write the test functions.

## Slide 58: Recording interpretation answers

01

Read each question and its labelled answer options. Choose the option supported by the data or code.

02

In DECISIONS, keep the question identifier unchanged and replace its blank value with your chosen option letter.

03

These letters identify answer choices. The portal assigns your test files automatically.

**Spoken script**

Some questions in the test ask us to read the data or the code and choose an answer. We record the choice in a dictionary called DECISIONS.

Read each question and its labelled options carefully. Choose the option that the data or the code supports.

Then find DECISIONS in the notebook. Each question has an identifier, and it already sits there with a blank value. Keep the identifier exactly as it is, and replace the blank with the letter of your chosen option.

The letters only name the answer choices. They have nothing to do with which test files you receive. The portal gives you your files automatically, so you never choose a version.

## Slide 59: A dictionary entry for a practice question

Use the inputs and operations defined in the preceding slides.

Compare the printed result with the explanation in the notebook.

```python
DECISIONS = {"practice": "B"}
print(DECISIONS["practice"])
```

**Spoken script**

This small cell shows how the answers are stored.

The first line creates a dictionary called DECISIONS. A dictionary pairs a name, called a key, with a value. Here the key is practice, written in quotation marks, and the value is the letter B, also in quotation marks. The curly brackets and the colon set up that pairing.

The second line prints the value stored under the key practice. We look up a dictionary value by writing the key inside square brackets.

The output is B.

In the real test, the keys are the question identifiers already present in the notebook, and you replace each blank value with the letter you chose. This practice entry is only a demonstration and carries no marks.

## Slide 60: Test-day instructions

01

The practice section ends here. Keep your revision notebook for study.

02

The following slides explain the timed test files, individual work and submission.

03

Use the portal-issued notebook and CSV for the actual test.

**Spoken script**

This slide marks the end of the practice section. Everything before it is for study, and you should keep your revision notebook to practise from.

The slides that follow explain the real test. They cover the timed test files, working individually, and how to submit.

On the test day, you will use the notebook and the CSV file issued to you by the portal. The practice file stays out of the test. We use it only to revise.

Read the next slides slowly now, so that on the day you already know what to expect.

## Slide 61: Your test files on test day

01

Downloads unlock at the scheduled start time. Open the link or scan its QR code.

02

Enter your name, Google email and Student Registration Number.

03

Download your notebook and engineering_data.csv.

Open your test files

Direct URL (click or copy into your laptop browser):

https://iuea-test-entry.jothammartin-wambi.workers.dev/?test=CML3111%7CTEST2

**Spoken script**

On test day you collect your files from an entry page. Open the link shown on the slide, or scan its QR code with your phone to reach the page.

The downloads unlock at the scheduled start time, so check the slide for the details of the test window.

On the page you enter three things. They are your name, your Google email, and your Student Registration Number. The page then gives you your notebook and the file called engineering underscore data dot csv. Download both onto your laptop.

The page assigns your files automatically, and you do not choose a version.

## Slide 62: Opening the notebook and CSV

01

In Colab: File → Open notebook → Upload. Select the downloaded notebook.

02

Save a copy in Drive. Connect the session.

03

In Files on the left, upload engineering_data.csv.

**Spoken script**

Once you have downloaded both files, we set them up in Colab.

Open Colab, then choose File, then Open notebook, then Upload. Select the notebook you downloaded.

Next, save a copy in your Drive, and connect the session using the Connect button, just as we did in our practice notebook.

Then click the folder icon on the left, and use Upload to add engineering underscore data dot csv. The notebook upload does not bring the CSV with it, so the CSV needs its own upload. Wait until the filename shows in the Files panel before you run any cell that reads it.

If the session resets, upload the CSV again.

## Slide 63: One notebook contains all answers

01

Code tasks have a prompt, function name and marks.

02

Six interpretation questions: record your chosen option letters in DECISIONS.

03

Submit one notebook snapshot using the final button.

**Spoken script**

Everything for the test lives in one notebook.

The code tasks each have a prompt, a function name, and the marks they carry. Read the prompt, and write your code in the function with the name supplied.

There are six interpretation questions. For these you record your chosen option letters in the DECISIONS dictionary, as we practised.

When you finish, you submit one notebook snapshot using the final button. A snapshot is a saved copy of your notebook at that moment.

Everything the grader needs is in that one notebook.

## Slide 64: How the 100 marks are allocated

01

Equipment-group split 20.

02

Baseline, linear and tree predictions 30.

03

MAE and RMSE 20. Structured interpretation 30.

**Spoken script**

The test is marked out of one hundred, and the slide shows where the marks sit.

The equipment-group split is worth twenty marks. This is the step where we separate machines into training and validation.

The baseline, linear and tree predictions are worth thirty marks together.

Calculating MAE and RMSE is worth twenty marks.

The structured interpretation questions are worth thirty marks. Those are the six questions where you record option letters.

All of these steps are things we have practised in this deck, one at a time. If you can follow the practice examples, you can follow the test.

## Slide 65: Order of work

01

Run the supplied row filters, then split by equipment ID.

02

Fit the imputer and models on training records only.

03

Compare validation errors. Keep the specified final-test group untouched.

**Spoken script**

The test has a sensible order, and it follows the practice closely.

We begin by running the row filters that the notebook supplies. After that we split the data by equipment ID, so that each machine goes wholly to one group.

Next we fit the imputer and the models on the training records only. The training rows teach the pipelines, and the other rows stay out of the learning.

Then we compare the validation errors of the baseline, the linear model and the tree on the same validation rows.

Throughout, the specified final-test group stays untouched. We do not look at it, fit on it, or use it to choose between models.

## Slide 66: The three-hour session

01

First 15 minutes: setup and file checks.

02

Next 120 minutes: individual coding tasks.

03

Next 25 minutes: interpretation and checking.

04

Final 20 minutes: prepare the snapshot and submit the form.

**Spoken script**

The test lasts three hours, and the slide divides them into four parts.

The first fifteen minutes are for setup and file checks.

The next one hundred and twenty minutes are for the individual coding tasks. This is the longest block, and the work is yours alone.

The following twenty-five minutes are for interpretation and checking.

The final twenty minutes are for preparing the snapshot and submitting the form.

Check the slide and the form for the actual start and close times.

## Slide 67: Before submitting

01

Restart the Colab session and run cells from the top.

02

Upload the same CSV again if the new session needs it.

03

Fix errors and run the final submission cell.

**Spoken script**

Before we submit, we check that the notebook works from a clean start.

First restart the Colab session and run the cells from the top. A fresh session has forgotten everything from earlier runs. This reveals any cell that was quietly using an old value or running in the wrong order.

Second, if the new session needs the CSV, upload the same file again.

Third, fix any errors that appear, and then run the final submission cell.

This restart check can feel tedious, but it protects you.

## Slide 68: Submission and confirmation

01

Click Submit test at the end of your notebook.

02

Open the generated form link using the same Google account. Check your details.

03

Press Submit before the deadline. Keep the confirmation.

**Spoken script**

Submitting takes three steps, and the slide lists them in order.

First, click Submit test at the end of your notebook. This button prepares a snapshot of your notebook.

Second, open the form link that is generated for you. Use the same Google account that you used for the notebook. Check that your details are correct.

Third, press Submit on the form, before the deadline shown there. Keep the confirmation that you receive.

Clicking the notebook button alone is only the first half. The submission is complete once you have pressed Submit on the form.

## Slide 69: How grading works

01

The lecturer’s grader runs your submitted code on unseen data.

02

The private workbook records identity, submission time, status and marks.

03

A technical or identity problem remains pending until resolved.

**Spoken script**

After the test, the lecturer's grader takes over.

The grader runs your submitted code on unseen data. That is why your functions must calculate from their inputs.

The marks go into a private workbook. For each submission, it records your identity, the submission time, a status, and your marks.

If there is a technical or identity problem with a submission, it stays pending until it is resolved. A pending entry means the problem still needs sorting out.
