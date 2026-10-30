# CML3111 Week 9

Each slide shows its text, then the spoken script the lecturer reads aloud.

## Slide 1: Classification and the cost of mistakes

Communications, Electrical, Mechatronics and Robotics Engineering

Friday 06 November 2026
Friday 11:00–14:00, Room 115

**Spoken script**

Welcome to Week 9. Until now our models predicted a number. This week we predict a yes or no answer, such as whether a machine should raise an alert.

We also learn how to count the mistakes such a model makes and how to put a price on them. We will build a confusion matrix by hand from a small file of true answers and model answers, then calculate precision, recall and a cost.

## Slide 2: Today’s learning

WHAT WE WILL DO
Turn a number into a yes or no question, teach a model to answer it, and score its answers. Learn the words class, probability, threshold, confusion matrix, precision, recall and F1.

HOW YOU WILL SHOW IT
You can explain why a model that never raises an alert can score 71 percent, and say what a missed alert costs. You can read a confusion matrix and the scores built from it.

**Spoken script**

Today the question changes from how much to yes or no. We will turn the {c['short']} number into an alert, teach a model to answer it, and score its answers honestly. Along the way we learn the words class, probability, threshold, confusion matrix, precision, recall and F1. By the end you can explain why a model that never raises an alert can still score high on accuracy, and why that makes accuracy a poor judge by itself.

## Slide 3: Words for today: the question

**Spoken script**

Five words for the question we ask today. A class is one of the possible answers, such as alert or no alert. A label is the correct class that has been recorded for a row. When there are exactly two classes we call the job binary classification. A probability is a number from zero to one that says how likely a class is. Zero point four seven means forty-seven percent. A threshold is the probability at or above which the model says yes. We will start with zero point five and then move it.

## Slide 4: The supplied file

Extract this week’s student ZIP. Upload classification_case.csv and engineering_data.csv into Colab using the Files panel, or keep them beside the notebook locally.

The examples below read this file. Run the cells in slide order. Keep the original CSV unchanged.

**Spoken script**

Everything today reads from files in this week's student ZIP. We start by extracting the ZIP on our computer. Inside are two CSV files, classification_case dot csv and engineering_data dot csv.

In Colab we open the Files panel and upload both files there. If we work on our own computer, we keep them in the same folder as the notebook. A notebook does not carry its data with it, so the filename and the column headings must match what the code expects, letter for letter.

The examples on the next slides read these files, so we run the cells in the order the slides show them. We never edit the original CSV. If we need a changed table, we make a copy in code and the original stays available for checking. Each cohort has its own data, so numerical results can differ between cohorts.

## Slide 5: Classification turns a number into a yes or no

Same dots. On the left we predict the number. On the right we predict which side of the limit it falls on.

**Spoken script**

In Week 8 we predicted a number, the motor temperature. Today the question changes. Engineers often care about a decision. Do we raise an alert or not?

So we draw a limit line. Here it is 80 deg C. A row at or above the line gets the label alert, written as one. A row below the line gets no alert, written as zero. The dots are the same dots. Only the question changed.

When the answer is one of a few classes, the job is called classification. With exactly two classes it is binary classification. The limit of 80 deg C is a teaching assumption for this course. It is a convenient line to practise on and is not a real safe operating limit.

## Slide 6: Building the alert label

The first six lines repeat Week 8: read, drop copies, keep valid rows.
>= compares each target with the limit, 80.0 deg C. The answer is True or False.
.astype(int) turns True and False into 1 and 0. The training rows are E1 to E4.
sum() adds the ones, so it counts the alerts in the training rows.

The limit is 80.0 deg C, a teaching assumption. The counts use the training rows only.

```python
import pandas as pd
raw = pd.read_csv("engineering_data.csv")
data = raw.drop_duplicates("record_id")
has_target = data["target"].notna()
valid_load = data["load_pct"].between(0, 100)
data = data[has_target & valid_load].copy()
data["alert"] = (data["target"] >= 80.0).astype(int)
groups = ["E1", "E2", "E3", "E4"]
train = data[data["equipment_id"].isin(groups)]
print(len(train), train["alert"].sum())
print(train["alert"].value_counts().to_dict())
```

Output on the slide:

```text
58 17
{0: 41, 1: 17}
```

**Spoken script**

Here is the label in code. The first six lines repeat what we did in Week 8: read the file, drop repeated record IDs, and keep the rows that have a recorded target and a valid load.

The next line builds the column. It compares each target with the limit and gets True or False for every row. As type int turns True into one and False into zero. That new column is the label. Then we pick out the training rows, the equipment groups E1 to E4, and we count only those. The last test group stays sealed.

The last two lines count. We have 58 training rows and 17 of them are alerts. Value counts shows the same thing as a dictionary: 41 rows with no alert and 17 with an alert.

## Slide 7: A model that always says no scores 71 percent

Most rows are no alert, so a model that never raises an alert still looks accurate.

**Spoken script**

Look at the two bars. Most rows are no alert. Now picture a model that does nothing except say no alert for every row.

Its accuracy is the share of rows it answers correctly. On our 58 training rows it would be right on 41 of them. That is 71 percent. It has found zero alerts, and the alerts were the whole point of building the model.

This is the accuracy trap. When one class is much more common than the other, accuracy looks good for a model that has learned nothing. The rest of today gives us better scores: precision, recall and F1. First we need a model that produces probabilities.

## Slide 8: Logistic regression turns a line into a probability

The curve gives a probability between 0 and 1 for every load. Higher load, higher probability of an alert.

**Spoken script**

To answer yes or no, a model first produces a probability. Logistic regression does this. It starts from the same kind of straight line you already know, then bends it into an S shape so the answer always stays between zero and one.

Read the picture. At twenty percent load the curve sits near zero, so an alert is very unlikely. The curve crosses one half at a load of about 78 percent. At ninety percent load the probability of an alert is about 0.8. The dots are the 58 training rows.

The name has regression in it for historical reasons. The job is classification, because the answer is a class. This curve uses load alone so that we can draw it. The model on the next slides uses load and ambient temperature together.

## Slide 9: Features on different scales need a common ruler

scaled value = (value − mean) ÷ standard deviation
Training mean and standard deviation: load_pct 59.9 and 22.7; ambient_c 26.3 and 4.6.
StandardScaler learns these from the training rows only.

**Spoken script**

In our training rows, load runs from about 21 to 93, and ambient temperature runs from about 18 to 34. Some models, logistic regression among them, work better when the inputs share a common scale.

Scaling gives every feature the same ruler. For each value we subtract the training mean and divide by the training standard deviation. The standard deviation is the typical distance from the mean. After scaling, zero means average and one means one standard deviation above average.

Look at the first row. Its load is 59.15. The training mean is 59.9, so the scaled load is -0.03, almost exactly average. Its ambient temperature of 31.71 is above the mean of 26.3, so it scales to 1.18.

The tool is called StandardScaler. It learns the mean and the spread from the training rows during fit, the same way the imputer learned the median. Decision trees do not need scaling, because they only ask whether a value is above or below a cut.

## Slide 10: Splitting the rows and choosing features

train was built on the last slide from groups E1 to E4. E5 validates. E6 stays sealed.
X holds the input columns. y holds the answers.
This time the answer column is alert.

X is a table of features. y is the column of answers.

```python
valid = data[data["equipment_id"] == "E5"]
features = ["load_pct", "ambient_c"]
X_train, y_train = train[features], train["alert"]
X_valid, y_valid = valid[features], valid["alert"]
print(len(train), len(valid))
```

Output on the slide:

```text
58 15
```

**Spoken script**

The split is the one from Week 8. Equipment E1 to E4 are the training rows, which we picked out on the last slide. Here we add E5, the validation group. E6 stays sealed for the final test.

X holds the input columns, load and ambient temperature. y holds the answers. The difference from Week 8 is that the answer column is now alert, zero or one, instead of a temperature.

The print shows 58 training rows and 15 validation rows.

## Slide 11: Fitting a classifier and reading its probabilities

make_pipeline lists the steps in order: fill blanks, scale, classify.
predict_proba returns two columns: the chance of class 0 and of class 1.
[:, 1] keeps the second column, the probability of an alert.
[:5] shows the first five validation rows.

fit learns from the training rows. predict_proba answers for rows the model has not seen.

```python
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
model = make_pipeline(
    SimpleImputer(strategy="median"),
    StandardScaler(),
    LogisticRegression(),
)
model.fit(X_train, y_train)
probability = model.predict_proba(X_valid)[:, 1]
print(probability[:5].round(3))
print(y_valid.to_list()[:5])
```

Output on the slide:

```text
[0.053 0.01  0.466 0.003 0.013]
[0, 0, 1, 0, 0]
```

**Spoken script**

Now the model itself. We list three steps in a pipeline: fill blanks with the median, scale the features, then fit logistic regression. The pipeline learns everything it needs from the training rows when we call fit.

Then we call predict underscore proba. It returns two columns for every row. The first is the chance of class zero. The second is the chance of class one, an alert. The square brackets with a colon and a one keep the second column.

We print the probabilities for the first five validation rows, and below them the true labels. Look at row 3. It really was an alert, and the model gave it a probability of 0.47. That is the model's honest uncertainty.

## Slide 12: A threshold turns a probability into a decision

decision = alert when probability ≥ 0.5, otherwise no alert
Lowering the threshold raises more alerts. Raising it raises fewer.

**Spoken script**

A probability is not yet a decision. To decide we pick a threshold. If the probability is at or above the threshold, the model says alert. Otherwise it says no alert. We start with a threshold of zero point five.

Read the table row by row. The first column is the probability. The second is the decision that follows from the threshold. The third is what really happened. The last column checks the decision.

A threshold is a choice, and we are free to move it. We will do that in a few minutes and watch what changes.

## Slide 13: Words for scoring the answers

**Spoken script**

Before we score anything, six words. In a yes or no problem, positive means the class we are looking for. Here, positive is an alert. Negative is the other class.

Now the four outcomes. A true positive means the model said alert and it was an alert. A false positive means the model said alert but nothing was wrong. That is a false alarm. A false negative means the model said no alert but the limit really was passed. That is a missed alert, and in engineering it is often the costly one. A true negative means the model said no alert and all was well.

Put the four counts in a two by two table and you have a confusion matrix. We will build one by hand from a small file first, and then read the matrix for our own model.

## Slide 14: Loading the supplied observations

raw_data: original CSV table; keep it unchanged so the analysis can be checked.

Run the cell and read the output below it.

```python
import pandas as pd
raw_data = pd.read_csv("classification_case.csv")
print(raw_data.head())
print(raw_data.shape)
print(raw_data.dtypes)
```

**Spoken script**

This cell loads the small file we use for the by-hand drill.

Line one imports pandas and gives it the short name pd, as we have done every week. Line two calls read_csv on classification_case dot csv and stores the table in a variable called raw_data. We keep the name raw_data for the untouched original, so we can always check our work against it.

Line three prints head, which shows the first rows of the table. Line four prints shape, which gives the number of rows and then the number of columns. Line five prints dtypes, which lists the data type of each column.

We look for two columns, actual and predicted, and we expect both to hold whole numbers, shown as int64. Each row is one case. Actual is the true answer for that case. Predicted is what a model said for the same case. What prints matches the explanation in the notebook.

## Slide 15: Every paired result belongs in one cell

Read actual first, then predicted_values. Explain the missed warning.

**Spoken script**

Every row in this file is one pair of answers, side by side. Actual is the truth that was recorded. Predicted is what the model said for the same case. We always read actual first, then predicted.

In this file one means warning. We call that the positive class, because it is the class we are looking for. Zero means no warning, the negative class.

That gives four possible pairs. Actual one with predicted one is a true positive, a warning that was right. Actual zero with predicted zero is a true negative, a quiet case correctly left quiet. Actual zero with predicted one is a false positive, a false alarm. Actual one with predicted zero is a false negative, a missed warning.

The word true or false tells us whether the model was right. The word positive or negative tells us what the model predicted. The missed warning is the costly one, because a real problem passed with no alert at all.

## Slide 16: Counting the supplied paired labels

actual holds the reference label. predicted holds the model decision. In this file, 1 means warning and 0 means no warning.

== compares values. & requires both conditions for each row. Parenthesise each comparison. sum counts the True entries.

**Spoken script**

Now we count each of the four pairs. The actual column holds the reference label, the true class. The predicted column holds the model's decision. In this file one means warning and zero means no warning.

To count a pair we need two checks on the same row at the same time. The double equals sign compares two values and gives True or False. The ampersand joins two checks, and a row passes only when both are True. We put each comparison inside its own parentheses, so Python reads them in the right order.

Then sum adds up the True entries. True counts as one and False counts as zero, so the sum is the number of rows that meet both conditions.

We repeat this with a different pair of conditions for each of the four outcomes.

## Slide 17: Operations for the next example

01

Selecting columns: equipment_data["column"] returns one labelled column, a Series. equipment_data[["a", "b"]] returns a DataFrame containing those named columns in that order.

02

Column arithmetic: Arithmetic on columns calculates one result per row. Series align by row label. Divide only where the denominator is valid and keep actual and predicted observations paired.

03

Adding values and counting True: series.sum() adds its values. For a Boolean mask, True counts as 1 and False as 0. equipment_data.isna().sum() therefore counts missing cells separately for each column.

**Spoken script**

Before the next example we remind ourselves of three pandas tools.

First, selecting columns. Square brackets with one name in quotes give one column, which is a Series. Square brackets holding a list of names give a smaller table with just those columns, in the order we wrote them.

Second, column arithmetic. When we do arithmetic on columns, pandas works on every row at once and gives one result per row. Rows are matched by their labels, so the actual and predicted values must stay paired row for row. If we divide, we first make sure the bottom of the fraction is valid.

Third, adding and counting True. The sum method adds up the values of a column. In a column of True and False, True counts as one and False counts as zero, so sum counts the Trues. If we write isna before sum, we count the missing cells in each column.

## Slide 18: Selecting rows with a mask

A column comparison produces one True or False per row. table[mask] keeps the True rows. & combines masks: both conditions must hold. Parenthesise each comparison.

**Spoken script**

A mask is a column of True and False answers, one for each row. We make one by comparing a column with a value, for example asking whether each entry equals one.

Then we place the mask inside square brackets after the table name. Pandas keeps the rows where the mask is True and drops the rest.

We can combine two masks with the ampersand. Then a row stays only when both conditions hold. Each comparison goes inside its own parentheses.

This is the same filtering we practised in earlier weeks. Today we use the same idea to pick out the rows whose actual and predicted labels match a pattern we care about, so we can count them.

## Slide 19: Keep observations and decisions paired

actual contains the recorded class; predicted contains the model’s decision for the same row.

Here 1 means positive and 0 negative.

These are already-issued decisions; this exercise does not train a classifier.

**Spoken script**

In this drill the model has already made its decisions. We are not training a classifier today. We only score decisions that exist in the file.

The actual column holds the recorded class. The predicted column holds the model's decision for the same row. A row in one column must line up with the same row in the other, so we never sort or shuffle one column without the other.

Here one means positive and zero means negative. Positive is the class we are watching for, which is the warning.

Everything we count next depends on these two columns staying in step.

## Slide 20: Confusion counts from classification_case.csv: step 1

actual_labels: the recorded class of each observation: 1 means positive and 0 means negative.

Run the cell and read the output below it.

```python
actual_labels = raw_data["actual"]
predicted_labels = raw_data["predicted"]
```

**Spoken script**

The first step gives the two columns short, clear names.

actual_labels takes the actual column from raw_data. predicted_labels takes the predicted column. Each one is a Series with one value per row, and the rows stay in their original order, so the pairing is kept.

In actual_labels, one means a positive case and zero means a negative case. In predicted_labels, the same numbers describe what the model decided.

This cell prints nothing, because it only stores values for the next steps. We still run it, since the cells that follow depend on these two names.

## Slide 21: Turn each class label into a question

actual == 1 asks whether the real class is positive; predicted == 1 asks whether the model predicted positive.

Each comparison returns one True/False answer per row.

Equality uses ==; assignment uses =.

**Spoken script**

A class label is a number, but counting is easier with yes or no questions. So we turn each label into a question.

actual double equals one asks, for every row, whether the real class is positive. predicted double equals one asks whether the model said positive. Each question gives one True or False for every row.

A single equals sign stores a value under a name. A double equals sign asks a question and gives back True or False. In this step we use the double equals sign, because we want the answers.

## Slide 22: Confusion counts from classification_case.csv: step 2

actual_labels: the recorded class of each observation: 1 means positive and 0 means negative.

Run the cell and read the output below it.

```python
actual_is_positive = actual_labels == 1
prediction_is_positive = predicted_labels == 1
actual_is_negative = actual_labels == 0
prediction_is_negative = predicted_labels == 0
print(actual_is_positive.head())
print(prediction_is_positive.head())
```

**Spoken script**

This cell builds four columns of True and False answers.

actual_is_positive asks whether each real class is one. prediction_is_positive asks whether each model decision is one. actual_is_negative and prediction_is_negative ask the same questions with zero. We need the negative versions later for false alarms and true negatives.

Then we print the first few entries of the first two columns, using head, to check them.

In the output, each line shows a row number on the left and True or False beside it. At the bottom we see the column name and the type bool, which means True and False values. We compare the two printouts row by row. Where both say True, the model caught a real warning. Where they differ, the model made a mistake.

## Slide 23: Count one outcome at a time

A true positive has actual 1 AND predicted 1.

Combine the two answer columns with &, then sum the True entries.

The other three outcomes use their own pairs of actual and predicted labels.

**Spoken script**

To count one outcome we ask two questions about the same row.

A true positive is a row where actual is one and predicted is one. We combine the two columns of answers with the ampersand, which gives True only where both are True. Then we sum the True entries to get the count.

The other three outcomes follow the same pattern with their own pair of labels. A false negative has actual one and predicted zero. A false positive has actual zero and predicted one. A true negative has actual zero and predicted zero.

One pair of conditions, one count, four times over.

## Slide 24: Confusion counts from classification_case.csv: step 3

actual_labels: the recorded class of each observation: 1 means positive and 0 means negative.

Run the cell and read the output below it.

```python
is_true_positive = actual_is_positive & prediction_is_positive
true_positive_count = int(is_true_positive.sum())
print("True positives:", true_positive_count)
```

**Spoken script**

This cell counts the true positives.

The first line joins actual_is_positive and prediction_is_positive with the ampersand. The result is True for each row where the case was a real warning and the model also said warning.

The second line sums that column, which adds up the Trues. We wrap the result in int to turn it into a plain whole number.

The third line prints a label, True positives, followed by the count. We read the output as the number of real warnings the model caught. We can check it by looking in the file for the rows where both columns show one.

## Slide 25: Confusion counts from classification_case.csv: step 4

false_negative_count: number of missed positives: actual 1 but predicted 0.

false_positive_count: number of false alarms: actual 0 but predicted 1.

**Spoken script**

Two more counts remain.

A false negative is a missed positive. The actual class is one, but the model predicted zero. This is the missed warning.

A false positive is a false alarm. The actual class is zero, but the model predicted one.

We store them in variables called false_negative_count and false_positive_count, so we can read them clearly later.

To tell them apart, we read the actual value first. If a real problem exists and the model stayed silent, we have a false negative. If no problem exists and the model raised an alert anyway, we have a false positive.

## Slide 26: Confusion counts from classification_case.csv: step 4 (1/3)

actual_labels: the recorded class of each observation: 1 means positive and 0 means negative.

Continue in the same code cell.

```python
false_negative_count = int(
    (actual_is_positive & prediction_is_negative).sum()
)
false_positive_count = int(
    (actual_is_negative & prediction_is_positive).sum()
)
```

**Spoken script**

This code is long, so it is split over three slides, but it is one cell.

false_negative_count takes the rows where actual_is_positive and prediction_is_negative are both True. Those are real warnings where the model said no. We join the two columns with the ampersand, sum the Trues, and convert the result with int.

The code is written over several lines. Python allows this inside parentheses.

false_positive_count works the same way, using actual_is_negative and prediction_is_positive. Those are quiet cases where the model raised an alert.

Nothing prints yet. We continue in the same cell on the next slide.

## Slide 27: Confusion counts from classification_case.csv: step 4 (2/3)

actual_labels: the recorded class of each observation: 1 means positive and 0 means negative.

Continue in the same code cell.

```python
true_negative_count = int(
    (actual_is_negative & prediction_is_negative).sum()
)
print(
    false_negative_count,
    false_positive_count,
    true_negative_count,
)
```

**Spoken script**

The cell continues with the third count.

true_negative_count takes the rows where actual_is_negative and prediction_is_negative are both True. Those are quiet cases that the model correctly left quiet.

Then print shows three counts in the order we wrote them: false negatives, then false positives, then true negatives. We read the output from left to right in that order.

Together with the true positives from the earlier cell, we now have all four counts of the confusion matrix. Each one answers a separate question about how the model behaved.

## Slide 28: Confusion counts from classification_case.csv: step 4 (3/3)

actual_labels: the recorded class of each observation: 1 means positive and 0 means negative.

Run the cell and read the output below it.

```python
print(
    true_positive_count
    + false_negative_count
    + false_positive_count
    + true_negative_count,
    len(raw_data),
)
```

**Spoken script**

The last lines of this cell are a check.

We add the four counts together and print that total next to len of raw_data, which is the number of rows in the file. Every row falls into exactly one of the four outcomes, so the two numbers must be equal.

If they differ, we have miscounted somewhere, perhaps with a missing parenthesis or a wrong pair of labels. A print with two items separated by a comma shows them on one line.

We always run this check before calculating anything from the counts. It costs a second and catches mistakes early.

## Slide 29: Precision, recall and cost

Precision is TP divided by TP + FP. Recall is TP divided by TP + FN. The issued policy returns zero when a denominator is zero.

The teaching cost is five units per missed warning plus one per false alarm. Explain the assumption when interpreting the result.

**Spoken script**

Now we score the counts.

Precision asks, of all the alerts the model raised, how many were right. It is true positives divided by true positives plus false positives. Recall asks, of all the real warnings, how many the model found. It is true positives divided by true positives plus false negatives. If a denominator is zero, the issued policy returns zero, so we never divide by zero.

Cost puts a price on mistakes. In our teaching rule, each missed warning costs five units and each false alarm costs one unit. So the cost is five times the false negatives plus the false positives.

These prices are an assumption made for teaching. Whenever we quote a cost, we say this assumption alongside it. A different plant could choose different prices.

## Slide 30: Operations for the next example

Rounded display: series.round(3) returns values rounded to three decimal places. Python round(number, 3) rounds one number. Keep unrounded calculations for returned assessment answers.

**Spoken script**

A short reminder about rounding.

On a Series, the round method with three inside the brackets gives every value to three decimal places. For a single number, Python's round function takes the number first and then the count of decimal places.

We round to make printed output easy to read. For answers that we return in an assessment, we keep the full unrounded value. Rounding early can shift later calculations, and a grader may compare exact values.

## Slide 31: Checking a condition before calculating

if condition: runs its indented statements only when the condition is True. else: handles the other case. Check for a nonzero denominator before division, and for a nonempty table before selecting its first row.

**Spoken script**

Dividing by zero breaks a calculation, so we check first.

The word if, followed by a condition and a colon, starts a block. The indented lines below it run only when the condition is True. The word else handles every other case.

For precision, the condition is that the number of predicted positives is more than zero. If it is, we divide. If it is not, the value keeps its safe starting value.

The same idea protects any step that needs something to exist. For example, we can check that a table is nonempty before we select its first row.

The indentation matters. It tells Python which lines belong to the check.

## Slide 32: Precision: how trustworthy are positive predictions?

The denominator is all predicted positives: true positives plus false positives.

Divide correct positive predictions by that total.

Check the denominator before dividing; this teaching example uses 0 when it is zero.

**Spoken script**

Precision tells us how much we can trust the model when it says positive.

The bottom of the fraction is every case the model called positive, which is true positives plus false positives. The top is the correct ones, the true positives. So we divide the correct positive predictions by all positive predictions.

A high precision means few false alarms.

Before dividing, we check that the bottom is above zero. A model that never raises an alert has no positive predictions to divide by, and in this example we then use zero.

## Slide 33: Metrics from the supplied outcomes: step 1

precision: fraction of positive predictions that are correct.

Run the cell and read the output below it.

```python
precision = 0.0
if true_positive_count + false_positive_count > 0:
    precision = true_positive_count / (
        true_positive_count + false_positive_count
    )
```

**Spoken script**

We start by setting precision to zero. That is the answer if the model never predicted positive.

The if line asks whether true positives plus false positives is more than zero. When it is, the indented line runs. It replaces precision with true positives divided by true positives plus false positives.

The parentheses stretch over several lines. They keep the sum together, so the division applies to the whole total.

Nothing prints here. The variable precision is stored for the final step, where we print it.

## Slide 34: Recall: how many real positives were found?

The denominator is all actual positives: true positives plus false negatives.

Divide detected positives by that total.

Precision and recall answer different questions even when they happen to have the same value.

**Spoken script**

Recall tells us how many of the real positives the model found.

The bottom of the fraction is every actual positive, which is true positives plus false negatives. The top is the ones the model caught, the true positives. So we divide the detected positives by all actual positives.

A high recall means few missed warnings.

Precision and recall answer different questions. Precision looks at the model's alerts. Recall looks at the real events. They can happen to share the same value, yet they still mean different things. A model that alerts only when it is very sure can have good precision and miss many events.

## Slide 35: Metrics from the supplied outcomes: step 2

recall: fraction of real positives that the model found.

Run the cell and read the output below it.

```python
recall = 0.0
if true_positive_count + false_negative_count > 0:
    recall = true_positive_count / (
        true_positive_count + false_negative_count
    )
```

**Spoken script**

Recall follows the same pattern as precision.

We set recall to zero first. Then the if line asks whether true positives plus false negatives is more than zero. That sum is the number of real positives in the file.

When it is, the indented line replaces recall with true positives divided by that sum.

The only difference from the precision cell is the bottom of the fraction. For precision we used the predicted positives. For recall we use the actual positives.

Nothing prints here. Both values are stored for the next cell.

## Slide 36: Metrics from the supplied outcomes: step 3

total_error_cost: five penalty units per missed positive plus one per false alarm in this scenario.

**Spoken script**

total_error_cost turns the mistakes into one number.

In this scenario each missed positive costs five penalty units and each false alarm costs one. We multiply the false negatives by five and add the false positives. Correct answers cost nothing.

The five to one ratio says that a missed warning is five times as bad as a false alarm. That is a teaching assumption for this scenario.

A lower cost is better, and a cost of zero means the model made no mistakes.

## Slide 37: Metrics from the supplied outcomes: step 3

total_error_cost: five units per missed alert plus one per false alarm.

Run the cell and read the output below it.

```python
total_error_cost = 5 * false_negative_count + false_positive_count
print(round(precision, 4), round(recall, 4), total_error_cost)
```

**Spoken script**

The first line calculates total_error_cost. It is five times false_negative_count plus false_positive_count. The star is the multiplication sign in Python.

The print line shows three values: precision rounded to four decimal places, recall rounded to four decimal places, and the cost. The round function only tidies the printout, and the stored values stay in full.

We read the output from left to right. Precision tells us how trustworthy the alerts are. Recall tells us how many real warnings we caught. The cost adds up the damage under our five to one rule.

We can check all three by hand from our own counts with a calculator.

## Slide 38: The confusion matrix of our model on the validation rows

15 validation rows. Accuracy 93 percent, precision 1.00, recall 0.67.

**Spoken script**

Here is the confusion matrix for our model. The rows are what really happened. The columns are what the model said.

Of the 3 real alerts in the validation rows, the model caught 2 and missed 1. Of the 12 quiet rows, it raised 0 false alarms and answered 12 correctly.

That gives an accuracy of 93 percent, a precision of 1.00 and a recall of 0.67. One caution. There are only 3 real alerts in the validation rows, so a single missed alert moves recall a long way. Treat these numbers as an illustration and judge the model on more data in later weeks.

## Slide 39: F1 combines precision and recall in one number

F1 = 2 × precision × recall ÷ (precision + recall)

F1 is high only when precision and recall are both high.
Our model: precision 1.00, recall 0.67, F1 0.80.
A model that never raises an alert has recall 0, so its F1 is 0, even though its accuracy looked high.

**Spoken script**

Precision and recall pull in different directions, so people often want one number that reflects both. That number is F1. It is a kind of average that is high only when precision and recall are both high.

For our model, precision is 1.00 and recall is 0.67. The formula gives an F1 of 0.80.

Remember the model that always says no alert. Its recall is zero because it finds none of the real alerts. So its F1 is zero, even though its accuracy was high. F1 exposes what accuracy hid.

## Slide 40: Moving the threshold trades false alarms for missed alerts

Lower threshold: more alerts, more false alarms, fewer misses.
Higher threshold: fewer alerts, fewer false alarms, more misses.
Choose the threshold from the cost of each mistake.

**Spoken script**

Now we move the threshold and watch the counts. A low threshold makes the model say alert more often, so we can catch more of the real alerts, and in most data we also pay with more false alarms. A high threshold does the opposite.

Here is what our small sample shows. At a threshold of 0.3 the model catches 3 of the 3 real alerts and raises 0 false alarms. At 0.5 it catches 2 and raises 0. At 0.7 it catches 0 and raises 0. The trade is easy to see in the TP and FP columns, and in the precision and recall columns built from them.

There is no threshold that is best for everybody. The right setting depends on the cost of each mistake. In this week's assignment a missed alert costs five units and a false alarm costs one, so a low threshold is attractive. For a different machine the costs could reverse. Only 3 real alerts sit in the validation rows, so the exact numbers will move with more data.

## Slide 41: The ROC curve shows every threshold at once

Each point is one threshold. AUC is 1.00 here. 1.00 is a perfect ranking and 0.50 is guessing.

**Spoken script**

What if we want to judge the model without choosing one threshold? The ROC curve does that. Every point on the curve is one threshold. The horizontal axis is the false alarm rate, which is the share of quiet rows that raised an alert: false positives divided by false positives plus true negatives. The vertical axis is the detection rate, which is recall.

A model that is only guessing follows the dashed diagonal. A good model climbs quickly toward the top left corner. The area under the curve is called AUC. It has a friendly meaning: pick one real alert and one quiet row at random, and AUC is the chance that the model gives the alert the higher probability.

Our AUC is 1.00. With only 3 real alerts in the validation rows, a very high AUC is easy to reach, so treat it lightly. We introduce the curve now because you will meet it in every machine learning report.

## Slide 42: A decision tree can answer yes or no too

SAME IDEA AS WEEK 8
A tree asks yes or no questions about the inputs. For a classifier, each leaf holds the share of alerts among the training rows that end there, and the tree answers with the majority.
In scikit-learn: DecisionTreeClassifier(max_depth=3, random_state=17).

ON THE VALIDATION ROWS
Tree: TP 2, FP 0, FN 1, TN 12. Precision 1.00, recall 0.67, F1 0.80.
Logistic regression: TP 2, FP 0, FN 1, TN 12. Precision 1.00, recall 0.67, F1 0.80.

**Spoken script**

The tree you met in Week 8 can answer yes or no questions as well. It asks the same kind of questions about the inputs. In a classifier each leaf holds the share of alerts among the training rows that end there, and the tree answers with the majority.

On the right are the scores for a tree of depth three on the same rows, beside the scores for logistic regression. The tree has 2 true positives, 0 false positives and 1 false negative. The two blocks have the same four counts in the same order, so we read the counts first and then the three scores.

With fifteen validation rows the two models are hard to separate. In Week 10 we learn how to compare models more fairly, using several splits.

## Slide 43: Words from today

**Spoken script**

Six words to take away. Accuracy is the share of rows answered correctly, and it can mislead when one class dominates. Precision asks, of the alerts we raised, how many were real. Recall asks, of the real alerts, how many did we find. F1 combines the two. The ROC curve shows performance at every threshold, and AUC is the area under it. Class imbalance means one class is much more common than the other.

In the assignment you will compute the four counts, precision, recall and the cost. You now know what each of those words means.

## Slide 44: Your issued task

01

Use classification_case.csv.

02

Positive means a synthetic warning condition.

03

Compute the confusion matrix, precision, recall and total_error_cost.

04

Explain the 5:1 missed-warning/false-alarm cost assumption and why accuracy alone is insufficient.

**Spoken script**

Your task uses classification_case dot csv, the same small file we worked through together. Positive means a synthetic warning condition, an invented condition built for teaching.

First, compute the confusion matrix, which is the four counts. Then compute precision, recall and total_error_cost.

Finally, explain in your own words the five to one cost assumption, which says a missed warning costs five and a false alarm costs one. Also explain why accuracy alone is insufficient. A model that never raises an alert can still look accurate when most rows are no alert, yet it misses every real warning.

## Slide 45: Your issued task continued

01

These costs are teaching assumptions for practice.

**Spoken script**

One reminder goes with the task. The costs we use are teaching assumptions. They are chosen to show how pricing mistakes changes which model looks best.

Real operating limits have to come from the people responsible for the equipment and its safety, after testing on real observations. In your explanation, say this clearly.

Also say what positive means in this file. Costs and benefits only make sense once the positive class has a name.

## Slide 46: classification_metrics(actual, predicted)

Return dictionary keys tp, tn, fp, fn, precision, recall and cost.

tp = true positives; tn = true negatives; fp = false positives; fn = false negatives.

cost = 5 * fn + fp. Return zero when a precision or recall denominator is zero.

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

Your required function is called classification_metrics. It takes two inputs, actual and predicted, which are the two columns of labels.

It returns a dictionary with seven keys: tp, tn, fp, fn, precision, recall and cost. Here tp is true positives, tn is true negatives, fp is false positives and fn is false negatives.

Precision and recall are calculated as we did in the notebook. The cost is five times fn plus fp. If the bottom of the precision or recall fraction is zero, that value is returned as zero.

The function name and the key names must match exactly, because the grader looks them up by name. Inside the function you may use longer local names such as true_positive_count, but the dictionary keys must be the short ones. Check the types of your values and the issued brief before you submit.

## Slide 47: Written evidence

01

Use the cell headed “My written evidence”.

02

Explain the supplied scenario in your own words.

03

State target units, reasons and limitations.

04

Submit one complete notebook containing code and written evidence.

**Spoken script**

Besides the code, we write our own explanation. Find the cell headed My written evidence and use it.

In that cell, explain the supplied scenario in your own words. State the units of any quantity you mention, for example motor temperature in deg C. Give your reasons for the choices you made, and state the limitations of your result.

Then submit one complete notebook that contains both the code and the written evidence. The explanation shows how you reason, so it must be written by you.

## Slide 48: Classification and cost submission

01

Opens: 06 Nov 2026, 11:00 Kampala

02

Deadline: 13 Nov 2026, 11:00 Kampala

03

Use your full Student Registration Number in the form.

04

Keep the submitted files and confirmation.

Open W09 assignment form

https://docs.google.com/forms/d/e/1FAIpQLSfelPFlgqIQS1vM0QDthocg7aIU_WLXNjL4g1DdZAJyKcm9eA/viewform

**Spoken script**

This slide covers the Week 9 assignment submission. Check the opening time and the deadline shown on the slide, and read the form title before you upload.

Enter your full Student Registration Number in the form. Wait for your filenames to appear, then press submit.

Keep the submitted files and the confirmation. Saving a file in Drive or GitHub does not submit it. The form is the submission.

## Slide 49: Week 9 quiz

01

Answer individually after the lecturer activates the quiz.

02

Available for 24 hours from activation.

03

Use your Student Registration Number and registered account.

04

Check the announced quiz closing time.

Open this week’s quiz

https://forms.gle/U2h5A1itpmZZTogm6

**Spoken script**

This is the Week 9 quiz. It opens when the lecturer activates it, and then it stays open for 24 hours.

Answer it individually. Use your Student Registration Number and your registered account. Check the announced closing time on the slide, and use the link on the slide to open the quiz form.

## Slide 50: Revision and submission checklist

Explain to a classmate why a model that never raises an alert can score 71 percent, and what a missed alert costs in your engineering field.

Keep raw data unchanged. Restart and run all cells before submitting the required assignment notebook.

Point to your evidence. Save your work.

**Spoken script**

Here is the exit check for this week.

Explain to a classmate why a model that never raises an alert can still score a high accuracy, and what a missed alert costs in your own engineering field. If you can say it in plain words, you understand it.

Before you submit, keep your raw data unchanged. Restart the notebook and run all cells from the top, so we know it works from start to end.

Then point to your evidence in the notebook and save your work.

## Slide 51: Optional revision video

01

For revision after class.

02

StatQuest with Josh Starmer
Machine Learning Fundamentals The Confusion Matrix

03

Opening up to 04:00, optional preview-selected excerpt

04

Listening question: Which observations are correctly or incorrectly classified?

Open explainer video

https://www.youtube.com/watch?v=Kdsp6soqA7o

**Spoken script**

This video is optional and is for revision after class. It is from StatQuest with Josh Starmer, and it is called Machine Learning Fundamentals, The Confusion Matrix.

Watch the opening, up to the four minute mark. As you watch, keep one question in mind: which observations are correctly classified, and which are incorrectly classified?

Then try to explain the answer in your own words, using the terms we met today. The link is on the slide.
