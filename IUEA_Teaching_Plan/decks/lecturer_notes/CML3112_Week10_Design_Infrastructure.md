# CML3112 Week 10

Each slide shows its text, then the spoken script the lecturer reads aloud.

## Slide 1: Honest validation and leakage

Civil Engineering and Architecture

Tuesday 10 November 2026
Tuesday 11:00–14:00, Room 106

**Spoken script**

Welcome to Week 10.

This week is about honest validation. We learn how to check a model so that its score really tells us how it will behave on new equipment, and how to spot leakage, which is a score that looks good for the wrong reason.

## Slide 2: Today’s learning

WHAT WE WILL DO
Watch a model memorise its training rows, learn to check it on several held-back groups, and find four ways a score can leak. Learn the words overfitting, cross-validation and data leakage.

HOW YOU WILL SHOW IT
You can explain why training error cannot be trusted, and how you would tell that a score is leaking. You can split by equipment group and report an error with its spread.

**Spoken script**

Last week we scored classifiers. This week we ask whether any score deserves trust. We will watch a model memorise its training rows, then learn to check a model on several held-back groups of equipment, and then meet four ways a score can leak. By the end you can explain why training error cannot be trusted, split the data by equipment group, and report an error together with its spread.

## Slide 3: Words for today: fitting and fairness

**Spoken script**

Six words that describe the central problem of machine learning. Generalisation is how well a model does on rows it has never seen. That is what matters most in practice, because nobody needs a prediction for a row whose answer they already have.

Underfitting means the model is too simple and misses the pattern. Overfitting means the model has memorised the training rows, noise included, and does worse on new rows. The validation set is the group of rows we keep back to compare models and settings. The test set stays sealed until the very end. A hyperparameter is a setting we choose before training, such as the depth of a tree.

Today we watch these words happen in our own data.

## Slide 4: The supplied file

Extract this week’s student ZIP. Upload engineering_data.csv into Colab using the Files panel, or keep them beside the notebook locally.

The examples below read this file. Run the cells in slide order. Keep the original CSV unchanged.

**Spoken script**

Every example this week reads one file, called engineering_data dot csv. It arrives inside this week's student ZIP, so the first job is to extract the ZIP on our computer.

In Colab we open the Files panel on the left and upload the CSV there. If we work locally, we keep the CSV in the same folder as the notebook. Uploading a notebook does not upload its data, so the CSV needs its own upload.

We check the file name and the column headings carefully, because pandas only finds a file whose name matches exactly.

We run the cells in the order the slides show them, since later cells use names that earlier cells create. We never edit the original CSV. Each cohort has its own data, so the numbers on your screen can differ from your neighbour's.

## Slide 5: Loading the supplied observations

raw_data: original CSV table; keep it unchanged so the analysis can be checked.

Run the cell and read the output below it.

```python
import pandas as pd
raw_data = pd.read_csv("engineering_data.csv")
print(raw_data.head())
print(raw_data.shape)
print(raw_data.dtypes)
```

**Spoken script**

We start the notebook by loading the data. The first line imports pandas and gives it the short name pd, as we have done since the early weeks.

The second line calls pd dot read underscore csv with the file name in quotes. It reads the file and returns a table, a DataFrame, which we store under the name raw underscore data. This is our original copy. We keep it unchanged so that anyone can check our analysis later.

Then we print three things. Dot head shows the first five rows, so we can see the column names and what a row looks like. Dot shape gives two numbers, the count of rows and then the count of columns. Dot dtypes lists the type of each column, for example whole numbers, decimals or text.

We read the output and ask three questions. Do the columns match what we expected? Does the row count look sensible? Are the numeric columns really numeric?

## Slide 6: Three sets have different jobs

Which set must stay sealed until choices are fixed?

**Spoken script**

We split our rows into three sets, and each set has one job.

The training rows teach the model. This is where it learns its numbers. The validation rows help us choose. We compare two models, or two settings of one model, and keep the one that scores better on validation. The test rows are saved for the end. We look at them once, after every choice is fixed, to get a final fair mark.

Picture the test set as a sealed exam paper. If we open it while we are still choosing features or settings, we start adjusting our work to fit that paper. The final score then comes from rows that influenced our decisions, so it is no longer an independent check.

The answer to the question on the slide is the test set. It stays sealed until our choices are fixed.

## Slide 7: Rows used for modelling

Keep the first occurrence of each record_id. Retain recorded targets and load_pct within 0–100. Then separate E1–E4 for training, E5 for validation and E6 for the final test_data.

Fill missing input values using training data only. Keep final-test targets out of model selection.

**Spoken script**

Before we model, we decide which rows are allowed in. We follow three rules in this order.

First, we remove duplicates. record underscore id names one observation, so if the same record_id appears twice, we keep only the first occurrence. We do this before any filtering, so an invalid first copy is never replaced by a later duplicate.

Second, we keep rows whose target was actually recorded, and whose load percentage lies between zero and one hundred. A load percentage outside that range is a data error. Removing rows that have no recorded target is a different job from filling a missing input value, and we handle missing inputs later.

Third, we split by equipment. E1 to E4 give the training rows, E5 gives the validation rows, and E6 gives the final test rows.

When we fill missing inputs, we calculate the fill value from training data only. The targets of the test rows take no part in choosing a model.

## Slide 8: Preparing the supplied modelling rows: step 1

modelling_data: copied observations after duplicate and validity checks.

Run the cell and read the output below it.

```python
modelling_data = raw_data.drop_duplicates("record_id").copy()
target_is_recorded = modelling_data["target"].notna()
load_is_valid = modelling_data["load_pct"].between(0, 100)
rows_to_keep = target_is_recorded & load_is_valid
print(target_is_recorded.head())
print(load_is_valid.head())
modelling_data = modelling_data[rows_to_keep].copy()
print(len(raw_data), len(modelling_data))
```

**Spoken script**

This cell cleans the table in four moves. Everything here uses ideas from earlier weeks.

The first line takes raw underscore data, calls drop underscore duplicates on the record_id column, which keeps the first row for each record_id, and then makes a copy. We call the result modelling underscore data.

The next line asks of each row, is the target recorded? Dot notna gives True when a value is present and False when it is missing. The line after that asks, is the load between zero and one hundred? Dot between gives True when the value lies in that range, ends included.

Then we join the two questions with an ampersand. A row is kept only when both answers are True.

We print the first five answers of each question to see them in action. Then we use the combined mask to filter the table, and copy again.

The last line prints two counts, the rows we started with and the rows we kept. The kept count can be smaller, and the difference tells us how many rows were removed.

## Slide 9: Choose groups before choosing rows

isin(list_of_labels) answers True when a row’s equipment ID appears in the list.

Here E1–E4 supply training rows, E5 validation rows and E6 test rows.

The groups stay separate so one equipment group cannot appear on both sides.

**Spoken script**

We split by equipment group first, and only then pick the rows. A group here is all the observations that came from one piece of equipment.

The tool is a pandas method called isin. We give it a list of labels, and for each row it answers True when that row's equipment ID appears in the list.

E1 to E4 supply the training rows. E5 supplies the validation rows. E6 supplies the test rows.

We keep the groups separate on purpose. If rows from one machine sat on both sides of the split, the model would meet that machine during training and again during checking, and the score would flatter it. By keeping each machine on one side, the check asks the question we care about, which is how the model does on equipment it has never seen.

## Slide 10: Preparing the supplied modelling rows: step 2

modelling_data: copied observations after duplicate and validity checks.

Run the cell and read the output below it.

```python
is_training_equipment = modelling_data["equipment_id"].isin(
    ["E1", "E2", "E3", "E4"]
)
is_validation_equipment = modelling_data["equipment_id"].isin(
    ["E5"]
)
is_test_equipment = modelling_data["equipment_id"].isin(["E6"])
```

**Spoken script**

This cell builds three masks. A mask is a column of True and False values, one per row, and we used masks for filtering in the pandas weeks.

The first line takes the equipment ID column and calls isin with the list E1, E2, E3, E4. The result, stored as is underscore training underscore equipment, is True for every row from those four machines.

The second line does the same with a list holding only E5, and stores the answer as is underscore validation underscore equipment. The third line does it for E6 and stores is underscore test underscore equipment.

The line breaks inside the brackets only make the code easier to read. Python treats it as one long line.

This cell prints nothing, because it only stores the three masks. The next cell uses them to cut the table into pieces.

## Slide 11: Preparing the supplied modelling rows: step 3

modelling_data: copied observations after duplicate and validity checks.

Run the cell and read the output below it.

```python
training_data = modelling_data[is_training_equipment].copy()
validation_data = modelling_data[is_validation_equipment].copy()
test_data = modelling_data[is_test_equipment].copy()
feature_columns = ["load_pct", "ambient_c"]
print(len(training_data), len(validation_data), len(test_data))
```

**Spoken script**

Now we use the three masks to cut the cleaned table into three tables.

The first line puts the mask inside square brackets after modelling underscore data. That keeps only the rows where the mask is True, and dot copy gives us an independent table. We call it training underscore data. The next two lines do the same and give validation underscore data and test underscore data.

Then we write down the features, the input columns the model will use. feature underscore columns is a list holding load underscore pct and ambient underscore c.

The final line prints the number of rows in each of the three tables, using len, the counter we know from earlier weeks.

We check that all three counts are above zero, and that training is the largest. Because the groups were assigned by equipment, each row lands in exactly one of the three tables.

## Slide 12: Training-only filling

median ignores missing values. Calculate it from training input values and reuse it for validation gaps.

Do not calculate a new median from validation or test observations. A pipeline keeps this rule with the model.

**Spoken script**

Some input values are missing, and we need to fill them. The rule is that every fill value comes from the training rows only.

We use the median, the middle value of a column once the values are sorted. It ignores missing entries. We calculate it from the training input values, and then we reuse that same number to fill gaps in the validation rows.

We never calculate a fresh median from the validation or test rows. If we did, information about those rows would flow into our preparation, and the later score would no longer be a fair check. Even a harmless looking step like this can leak.

Think of the validation rows as arriving later, like new equipment turning up after the model was built. When we get such equipment, we cannot calculate anything from it in advance. We can only use what we learned from the training rows.

A pipeline, the chain of steps from Week 8, keeps this rule together with the model. It learns the fill value from training data every time and applies it to whatever it is given.

## Slide 13: Operations for the next example

01

Middle recorded value: series.median() sorts known values conceptually and returns the middle one. With an even count, it averages the two middle values. Missing entries do not enter the calculation.

02

Replacing missing entries: series.fillna(value) returns a column whose missing entries contain value. Recorded values stay unchanged. Assign the returned column to retain the fill.

03

Rounded display: series.round(3) returns values rounded to three decimal places. Python round(number, 3) rounds one number. Keep unrounded calculations for returned assessment answers.

**Spoken script**

Three small pandas tools appear in the next example.

The first is dot median. On a column it returns the middle recorded value. Python sorts the known values in its head and picks the one in the centre. When the count is even, it averages the two middle values. Missing entries are skipped.

The second is dot fillna. We give it a value, and it returns a column in which every missing entry holds that value. The recorded values stay as they were. The original column is untouched until we assign the returned column to a name, so we assign it if we want to keep the fill.

The third is rounding for display. Dot round with the number three, on a column, rounds every value to three decimal places. The plain Python function round, with a number and a three, does the same for a single number. We round only to make printing tidy. In calculations we keep the unrounded values.

## Slide 14: Operations for the next example

Adding values and counting True: series.sum() adds its values. For a Boolean mask, True counts as 1 and False as 0. equipment_data.isna().sum() therefore counts missing cells separately for each column.

Finding missing cells: isna() returns True for missing entries such as NaN and None. It returns False for a recorded zero. A DataFrame gives a mask for every cell; a Series gives one mask value per row.

**Spoken script**

Two more tools help us check for missing values.

Dot isna asks each entry whether it is missing. It returns True for blanks, such as NaN, and False for everything else. A recorded zero is a real value, so isna gives False for it. On a whole DataFrame, isna returns a True or False for every cell. On a single column, it returns one answer per row.

Dot sum adds values up. When the values are True and False, Python counts True as one and False as zero, so the sum becomes a count of the True answers.

Put the two together. equipment underscore data dot isna dot sum counts the missing cells separately for each column. It gives us a quick report of where the gaps are.

We use this check before filling anything, so we know how much filling there is to do, and afterwards to confirm the gaps are gone.

## Slide 15: Training median from the actual ambient readings

training_ambient_median: median ambient temperature calculated only from training rows.

Run the cell and read the output below it.

```python
training_ambient_median = training_data["ambient_c"].median()
filled_validation_ambient = validation_data["ambient_c"].fillna(
    training_ambient_median
)
print(round(float(training_ambient_median), 3))
print(validation_data["ambient_c"].isna().sum())
print(filled_validation_ambient.head())
```

**Spoken script**

This cell fills gaps in the validation rows with a median taken from the training rows.

The first line takes the ambient underscore c column of the training data and calls dot median. The answer is one number, the typical ambient temperature in the training rows. We store it as training underscore ambient underscore median.

The second line takes the validation ambient column and calls fillna with that training median. Every blank in the validation column receives the training value. The result is stored as filled underscore validation underscore ambient.

Then three prints. The first prints the median, with float turning it into a plain Python number and round keeping three decimals. The second counts the blanks in the original validation column. In this cohort the validation rows happen to have none, so the count is zero. The third prints the first five entries of the filled column. With no blanks to fill, these five values are the originals. If a blank had been there, we would see the training median in its place. The one blank in this data sits in a training row, and the pipeline fills it in the same way.

The point to remember is that the validation rows borrow a number from training and never contribute to it.

## Slide 16: Preparing X and y, with a filled copy for tree experiments

X holds the input columns. y holds the answers. The raw X keeps its blanks for pipelines.
median() is worked out from the training rows only.
The filled copies put that same median into any blank, in both tables.

The validation rows borrow the training median and never contribute to it.

```python
X_train = training_data[feature_columns]
y_train = training_data["target"]
X_valid = validation_data[feature_columns]
y_valid = validation_data["target"]
fill_values = X_train.median()
X_train_filled = X_train.fillna(fill_values)
X_valid_filled = X_valid.fillna(fill_values)
print(X_train.shape, X_valid.shape)
```

Output on the slide:

```text
(58, 2) (15, 2)
```

**Spoken script**

We need two tables and two columns of answers for the experiments that follow. X train holds the inputs for the training rows. Y train holds their targets. X valid and y valid do the same for the validation rows. These raw tables keep their blanks, because a pipeline fills blanks by itself.

Some of today's experiments use a tree on its own, and we want the blank filled before it sees the data. So we also make filled copies. Look at the line with median. The medians come from the training rows only. Then fill na puts those medians into any blank, in the training copy and in the validation copy. The validation rows borrow a number from the training rows and add nothing back.

The shape printout confirms the sizes: 58 training rows and 15 validation rows, two feature columns each.

## Slide 17: A flexible model can memorise the training rows

Same dots, three trees. Depth 1 is too simple. Depth 12 chases every dot, noise included.

**Spoken script**

Here are the same training rows with three different trees. On the left the tree may ask only one question, so it draws a single step. It misses the rising pattern. We call that underfitting.

On the right the tree may ask twelve questions in a row. Look how it jumps up and down to touch every dot. It has memorised the training rows, including their random wobble. That is overfitting. In the middle the tree is flexible enough to follow the trend and calm enough to ignore the wobble.

Some books call the left problem bias, meaning too simple, and the right problem variance, meaning too jumpy. You will see those two words in other courses. In Semester 2 we add tools that hold a flexible model back.

## Slide 18: Training error keeps falling while validation error stalls

The loop tries three tree depths.
mean_absolute_error(actual, predicted) is the MAE you computed by hand.
We score the same tree twice: on rows it learned from, and on rows it never saw.

Errors are in kW. The deeper tree fits its training rows almost perfectly.

```python
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
print("depth train valid")
for depth in [1, 4, 8]:
    tree = DecisionTreeRegressor(
        max_depth=depth, random_state=17)
    tree.fit(X_train_filled, y_train)
    train_pred = tree.predict(X_train_filled)
    valid_pred = tree.predict(X_valid_filled)
    train_mae = mean_absolute_error(y_train, train_pred)
    valid_mae = mean_absolute_error(y_valid, valid_pred)
    print(depth, round(train_mae, 2), round(valid_mae, 2))
```

Output on the slide:

```text
depth train valid
1 4.63 5.3
4 1.2 3.39
8 0.06 2.71
```

**Spoken script**

Now the numbers behind the picture. The loop trains three trees, with one, four and eight questions in a row allowed. For each tree we print two errors. The first is the error on the training rows the tree learned from. The second is the error on the validation rows it has never seen.

Read the output. The training error falls steadily, from 4.63 down to 0.06. The validation error improves at first and then stops improving; at depth eight it is 2.71. The gap between the two columns is the sign of overfitting.

This is why we never report the training error as the result of a model. A model always looks good on rows it has already seen.

## Slide 19: The gap between training and validation error is the warning sign

Depth 1 to 10, computed from this cohort's rows. The orange line is the honest score.

**Spoken script**

Here is the same experiment for every depth from one to ten. The dark line is the error on the training rows. It falls all the way to zero, because a deep tree can memorise every row. The orange line is the error on the validation rows. It falls, flattens, and then wobbles around the same level.

The orange line is the honest score. We choose the depth where it stops improving. The dark line reaching zero tells us nothing about new rows. Deeper trees past that point cost more to run and explain, and they deliver no gain. Fifteen rows from one machine give a rough warning, so we look at the overall shape of the two lines.

One more fact to notice. Even the best tree here is worse than the straight line from Week 8, which scored 0.74 kW on these same rows. A tree predicts the average of the training rows that land in each leaf, so it cannot continue a rising trend, and these rows rise in a nearly straight path.

## Slide 20: One validation group can mislead

THE PROBLEM
Our validation group, E5, has only 15 rows. One odd machine or one lucky stretch of data can make a model look better or worse than it is.

THE REMEDY
Score the model several times, each time holding back a different group. Report the average error and how far the scores spread. That is cross-validation.

**Spoken script**

Our validation group has only 15 rows. That is a small sample. One odd machine, or one lucky stretch of data, can make a model look better or worse than it really is.

The remedy is to score the model several times, each time holding back a different group of equipment. We then report the average error and how far the scores spread. That is cross-validation. The next slides show how scikit-learn does it, and why we keep whole equipment groups together.

## Slide 21: Words for today: repeated checks and leaks

**Spoken script**

Five words for the second half of today. A fold is one turn of a repeated check, with one group of equipment held back. Cross-validation means scoring the model on several folds in turn. The spread tells us how far the fold scores differ from each other. A group split keeps whole equipment groups on one side, so one machine never sits on both sides of the line. Data leakage means information from outside the training rows reaches the model. We will meet leakage in detail after the cross-validation slides.

## Slide 22: The Week 8 pipeline, ready to be scored on several folds

This is the Week 8 pipeline: fill blanks with the median, then fit a line.
Nothing is fitted yet. The pipeline is a recipe.
Each fold will fit a fresh copy of this recipe on its own training groups.

A fresh median is learned inside every fold, so no fold borrows from its held-back group.

```python
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
linear_model = make_pipeline(
    SimpleImputer(strategy="median"),
    LinearRegression(),
)
```

Output on the slide:

```text
(nothing printed)
```

**Spoken script**

Cross-validation needs a model to score, so we bring back the pipeline from Week 8. It lists two steps: fill blanks with the median, then fit a straight line. Writing it does not train anything. It is a recipe.

That detail matters for fairness. In each fold, scikit-learn fits a fresh copy of the recipe on that fold's training groups. The median is learned again inside every fold, so a held-back group never lends a number to its own score.

## Slide 23: Each fold takes a turn at validation

An illustration from another engineering field (strength in MPa). Our own fold errors follow on later slides.

**Spoken script**

This figure shows cross-validation. The data is cut into pieces called folds. Each fold takes a turn as the validation piece, while the other folds are used for training. Every turn gives one error score, and together the scores show how steady the model is.

The example in the picture comes from another engineering field and measures the strength of a material in megapascals. The numbers belong to that illustration and are not ours. We use it only to see the shape of the idea.

A standard deviation is a single number describing how far the scores spread around their average. A small value means the folds agree with each other. A large value means the score changes a lot depending on which piece was held back.

The spread describes these particular folds. Our own fold errors, in our own unit, follow on the next slides.

## Slide 24: Cross-validation within training data

GroupKFold keeps each equipment group within one fold. Each fold takes a turn as validation while the remaining folds train the pipeline.

cross_val_score reports one score per fold. neg_mean_absolute_error returns negative MAE, so negate the scores before reporting the fold errors.

**Spoken script**

Now we run cross-validation, using only the training rows. The validation group E5 and the test group E6 stay outside this calculation.

We use a splitting tool called GroupKFold. It keeps every row of an equipment group inside one fold. So when a group is held out, none of its rows leaked into training. Each fold takes a turn as validation while the remaining folds train the model.

The scoring function is cross underscore val underscore score. It does the repeated fitting for us and hands back one score per fold.

There is one oddity. scikit-learn assumes that a bigger score is a better score. Error is the opposite, because smaller error is better. To keep the rule consistent, the scoring name neg underscore mean underscore absolute underscore error gives the mean absolute error with a minus sign in front. So the numbers come back negative. We flip the sign afterwards to get ordinary positive errors, which we call fold underscore absolute underscore errors in the notebook.

## Slide 25: Operations for the next example

01

A labelled column: pd.Series(values) creates a one-dimensional labelled sequence. With an array of fold errors, the default labels are 0, 1, 2 and so on.

02

Mean of recorded values: series.mean() adds known values and divides by their count. pandas skips missing values by default. The result has the same unit as the original column.

03

Spread of fold errors: series.std(ddof=0) measures how far values spread around their mean. ddof=0 divides squared deviations by the number of values. This describes these folds, not a confidence interval.

**Spoken script**

Three more pandas tools help us summarise the fold errors.

The first is pd dot Series. We give it a list or array of values, and it returns a Series, a one-dimensional column with labels. For an array of fold errors the labels are zero, one, two and so on.

The second is dot mean. It adds up the recorded values and divides by how many there are. Missing values are skipped by default. The result is in the same unit as the column, so for errors it is in kW.

The third is dot std with ddof equal to zero. Std is the standard deviation, one number for how far the values spread around their mean. ddof is a setting for the divisor. With ddof equal to zero, we divide by the number of values, which is the right choice when we are describing exactly these folds and nothing more.

This spread describes exactly our folds and nothing more.

## Slide 26: Keeping groups together / Scoring repeated splits

GroupKFold(n_splits=4) creates four train/validation splits. All rows of an equipment group stay on one side of each split. Four splits require at least four distinct training groups.

cross_val_score fits a fresh model for each split and scores its held-out rows. groups identifies the equipment groups and cv supplies the split rule. neg_mean_absolute_error returns negative MAE; negate it to report positive errors.

**Spoken script**

Two tools do the work here.

GroupKFold with n underscore splits equal to four creates four splits of the training rows. In each split some groups are set aside for validation and the rest are used for training. All rows of one equipment group stay on the same side. Four splits need at least four different groups in the training data. We have E1 to E4, so each group gets one turn on the validation side.

Then cross underscore val underscore score takes over. For each split it fits a fresh copy of the model on the training side, so nothing carries over between folds, and then scores the held-out rows.

We give it three extra items. groups tells it which equipment group each row belongs to. cv supplies the split rule, which is our GroupKFold. And scoring says which error to use. The name neg underscore mean underscore absolute underscore error gives negative MAE, so we negate the answers to report positive errors.

## Slide 27: Repeat evaluation without mixing groups

Four folds means four held-out group turns.

In each turn, learn a fresh pipeline on the other training groups and score the held-out group.

This uses training_data only; validation and test tables stay outside this calculation.

**Spoken script**

Four folds mean four turns, and in each turn one equipment group is held out.

In turn one we learn from three groups and score on the fourth. In turn two a different group is held out, and so on, until every group has been the unseen one. Each turn starts with a fresh model, so what it learned earlier cannot help it later.

That gives us four separate error scores. Each one answers the same question: how well does the model do on a machine it was never trained on?

All of this uses training underscore data only. The validation table and the test table stay outside the calculation. They are kept for later jobs, so nothing about them can affect how we judge these folds.

## Slide 28: Fold errors calculated from the supplied training rows: step 1

grouped_folds: the split rule that keeps observations from one equipment group together.

Run the cell and read the output below it.

```python
from sklearn.model_selection import GroupKFold, cross_val_score
grouped_folds = GroupKFold(n_splits=4)
```

**Spoken script**

This short cell prepares the splitter.

The first line imports two tools from the scikit-learn module model underscore selection. GroupKFold is the rule for cutting data into folds while keeping groups together. cross underscore val underscore score is the function that runs the repeated fit and score. Importing them only makes them available. Nothing is trained yet.

The second line creates a GroupKFold with n underscore splits equal to four and stores it as grouped underscore folds. That name stands for the split rule. It keeps all observations from one equipment group together and makes four folds.

The cell prints nothing, because it only stores the rule for the next cell.

## Slide 29: Read the scoring convention

scikit-learn uses larger scores as better. neg_mean_absolute_error therefore returns negative errors.

Negate the returned scores to recover ordinary positive MAE; lower MAE is better.

**Spoken script**

A small convention in scikit-learn can confuse us, so we say it clearly.

In scikit-learn, larger scores are always better. That works well for accuracy, where more is good. It would work badly for error, where less is good. To keep the rule the same for every score, scikit-learn reports error with a minus sign. The scoring name neg underscore mean underscore absolute underscore error therefore returns negative errors.

So a result like minus two is actually an error of two. Of two negative scores, the one closer to zero is the better one.

To get back to the ordinary mean absolute error, we negate the returned scores by putting a minus sign in front. Then the numbers are positive again and the usual reading holds. A lower MAE is better.

## Slide 30: Fold errors calculated from the supplied training rows: step 2

grouped_folds: the split rule that keeps observations from one equipment group together.

Run the cell and read the output below it.

```python
negative_error_scores = cross_val_score(
    linear_model,
    X_train,
    y_train,
    groups=training_data["equipment_id"],
    cv=grouped_folds,
    scoring="neg_mean_absolute_error",
)
```

**Spoken script**

This is the cell that does the repeated fitting. It is one function call written over several lines, with one item on each line.

The first item is linear underscore model, the model we built in Week 8. cross underscore val underscore score fits a fresh copy of it in every fold.

The next two items are X underscore train and y underscore train, the input features and the target values from the training rows.

Then groups equals the equipment ID column of the training data. This tells the function which machine each row came from, so rows from one machine stay together.

Then cv equals grouped underscore folds, the rule from the last cell. And scoring equals neg underscore mean underscore absolute underscore error, which asks for negative MAE.

The returned array is stored as negative underscore error underscore scores, with one entry per fold. Nothing prints here. The next cell turns the scores into positive errors and summarises them.

## Slide 31: Report typical error and variation

Each value is the MAE of one held-out fold. mean gives average error. std(ddof=0) describes the spread across these four errors only.

A large spread suggests performance depends on the held-out equipment.

**Spoken script**

We summarise the four fold errors with two numbers.

Each value is the mean absolute error of one held-out fold, so it is in kW. The mean of the four tells us the typical error across the folds. It is a rough guide, based on four machines, to how wrong the model tends to be on equipment it has not seen.

The standard deviation, written std with ddof equal to zero, tells us the spread across these four errors. It is the usual distance of a fold's error from the mean. It describes these four folds only. A confidence interval is a different tool that we do not use here.

How do we read the two together? When the spread is small compared with the mean, the folds agree and the model behaves consistently. When the spread is large, performance depends on which equipment is held out. That is useful to know before anyone trusts the model on a new machine.

We report both numbers, the mean and the spread, with their unit.

## Slide 32: Fold errors calculated from the supplied training rows: step 3

Run the cell and read the output below it.

Run the cell and read the output below it.

```python
fold_absolute_errors = pd.Series(-negative_error_scores)
print(fold_absolute_errors.round(4).tolist())
print(round(float(fold_absolute_errors.mean()), 4))
print(round(float(fold_absolute_errors.std(ddof=0)), 4))
```

**Spoken script**

This cell turns the raw scores into a report.

The first line puts a minus sign in front of negative underscore error underscore scores, which gives positive errors, and wraps them in pd dot Series. We store that as fold underscore absolute underscore errors, one error per fold.

The first print rounds the four values to four decimal places and turns them into a plain list. We read one error for each held-out equipment group.

The second print gives the mean. We wrap it in float and round it to four decimals. This is the typical error across the folds, in kW.

The third print gives the standard deviation with ddof equal to zero. This is the spread of the four errors around their mean.

When we read the output, we compare the four values with each other. If they are close, the model is steady. If one is far from the rest, one equipment group is behaving differently, and the spread will show it.

## Slide 33: Leakage makes a score look better than it is

Data leakage: information the model should not have reaches the model during training.

Think of an exam. If the exam paper is on your desk the night before, a high mark proves nothing about what you learned.
A leaky score is a mark earned with the paper in hand. It looks wonderful and it fails in real use.
Leakage is common and quiet: the code runs, the score is high, and nothing warns you.

**Spoken script**

Leakage is one of the most common serious mistakes in machine learning. Think of an exam. If the exam paper is on your desk the night before, a high mark proves nothing about what you learned. A leaky score is a mark earned with the paper in hand.

What makes leakage dangerous is that it is quiet. The code runs. The score is high. Nothing warns you. Only a careful look at how the data was prepared reveals it. So we learn the four usual ways it happens, and a guard for each.

## Slide 34: Four ways leakage happens, and a guard for each

Each guard is a habit you can apply while preparing the data.

**Spoken script**

Here are four ways leakage usually happens. One, copies across the split. The same observation sits in the training rows and again in the validation rows, for example a repeated record ID. Two, preparing before splitting. If you work out a median or a scale from all the rows, the validation rows have already influenced the model. Three, the same group on both sides. If rows from one machine sit in training and in the test, the model recognises the machine and the score is inflated. Four, a column that holds the answer. An input that is only known after the outcome, such as a repair record written after a fault.

Each box has a guard. Remove repeated IDs. Fit imputers and scalers on the training rows only. Keep whole equipment groups together. Use only inputs that you will really have at the moment of prediction.

## Slide 35: A leaky score looks wonderful

concat stacks two tables on top of each other.
The first score is honest: the tree never saw the validation rows.
The second score is leaky: we put the validation rows into training first.

Both scores are validation errors in kW. Only the second one is invalid.

```python
import pandas as pd
leaky_X = pd.concat([X_train_filled, X_valid_filled])
leaky_y = pd.concat([y_train, y_valid])
tree = DecisionTreeRegressor(
    max_depth=10, random_state=17)
tree.fit(X_train_filled, y_train)
pred = tree.predict(X_valid_filled)
print("honest", round(mean_absolute_error(y_valid, pred), 2))
tree.fit(leaky_X, leaky_y)
pred = tree.predict(X_valid_filled)
print("leaky ", round(mean_absolute_error(y_valid, pred), 2))
```

Output on the slide:

```text
honest 2.73
leaky  0.0
```

**Spoken script**

Let us leak on purpose and watch what it does. First we score a deep tree honestly: it trains on the training rows and is scored on the validation rows.

Then we cheat. We stack the validation rows into the training table with concat, train again, and score on the same validation rows. The honest error is 2.73 kW. The leaky error is 0.00. A model that has the answers in front of it looks perfect.

No warning appeared. That is why leakage is so dangerous, and why the habits on the previous slide matter.

## Slide 36: Pandas inside the required function

The assignment caller supplies equipment_records. pd.DataFrame(records) gives those records named columns. Calculate with pandas, then return the published Python type.

to_dict("records") makes a list of row dictionaries. Series.tolist() makes a list of values. A grouped Series.to_dict() maps group labels to validation_results.

**Spoken script**

In the assignment, our code lives inside a function, and the function receives its data from outside. The caller gives us a list called equipment underscore records. Each record is a small dictionary for one row.

Inside the function, pd dot DataFrame with the records turns that list into a table with named columns. After that we calculate with the pandas tools we already know, such as masks, groupby and mean.

The last step is returning the answer in exactly the Python type the task publishes. Three conversions help. to underscore dict with the word records in quotes makes a list of row dictionaries. Dot tolist on a Series makes an ordinary list of its values. And on a Series made by grouping, dot to underscore dict makes a dictionary that maps each group label to its result, such as the validation results for that group.

In the assessed function we do not read a CSV. The hidden tests supply different records every time, so the function must work from whatever it is given.

## Slide 37: Operations for the next example

01

Returning a dictionary: series.to_dict() maps Series labels to values. equipment_data.to_dict("records") instead returns a list of row dictionaries. Choose the form required by the assignment.

02

A table from Python values: pd.DataFrame(records) builds a table from row dictionaries. With a dictionary of column lists, keys become column names and each list supplies that column’s values.

03

Grouping rows: equipment_data.groupby("label")["value"] groups the value column by matching labels. Apply mean() or sum() to calculate one result per group. Missing group labels are excluded by default.

**Spoken script**

Three pandas operations appear in the function example.

First, returning a dictionary. Dot to underscore dict on a Series gives a dictionary in which each label maps to its value. Calling to underscore dict on a DataFrame with the word records gives something else, a list of row dictionaries, one per row. We always choose the form that the assignment asks for.

Second, building a table from Python values. pd dot DataFrame with a list of row dictionaries gives a table. With a dictionary of column lists instead, each key becomes a column name and each list supplies the values of that column.

Third, grouping rows. We write the table, then groupby with a label column, then the value column in square brackets. Python collects the value column into one bundle per label. Then we apply mean or sum and get one result per group. Rows whose group label is missing are left out by default.

## Slide 38: Defining and calling a function

def gives a reusable block a name and input parameters. The indented statements run when it is called. return sends a result back to the caller; print displays a result but does not return it.

**Spoken script**

A function is a named block of code that we can run whenever we need it. We make one with the word def, followed by a name and a pair of brackets holding the inputs. The inputs are called parameters.

The indented lines below the def line are the body. They do not run when Python reads the definition. They run each time we call the function by writing its name and giving it values.

The word return sends a result back to whoever called the function. After that call we can store the result in a name or use it in another calculation.

print is different. It shows a value on the screen for us to read, and the function gives nothing back to the program. An assignment function must return its answer, because the grader collects the returned value and never reads what we print.

So when we write a function for the assignment, the last line of the body is a return.

## Slide 39: A function called with the supplied records

equipment_records: the input list of row dictionaries supplied to the function.

Run the cell and read the output below it.

```python
def mean_load_by_equipment(equipment_records):
    equipment_data = pd.DataFrame(equipment_records)
    mean_load_by_equipment_group = equipment_data.groupby(
        "equipment_id"
    )["load_pct"].mean()
    return mean_load_by_equipment_group.to_dict()
equipment_records = modelling_data.to_dict("records")
print(mean_load_by_equipment(equipment_records))
```

**Spoken script**

This cell defines a function and then calls it.

The function is called mean underscore load underscore by underscore equipment, and it takes one parameter, equipment underscore records. Inside, the first line builds a DataFrame from the records. The second line groups the rows by equipment ID, picks the load percentage column and takes its mean. That gives one average load for each equipment group. The last line returns that result as a dictionary, with each equipment ID mapped to its average load.

Nothing has run yet, because a definition only stores the function.

The next line makes the input. raw underscore data dot to underscore dict with records in quotes turns our table into a list of row dictionaries. That is the shape of data the assignment functions receive.

The last line calls the function with that list and prints what it returns. We expect one entry for each equipment group, with a load percentage as its value.

## Slide 40: Words from today

**Spoken script**

Six words to keep. Overfitting is memorising the training rows, noise included. Underfitting is a model too simple for the pattern. Generalisation is doing well on rows never seen. Cross-validation scores the model on several held-back groups in turn, and the spread tells us how stable the result is. Data leakage is information reaching the model that should not. Notice that every one of these words is about trust. In the assignment you will build the group split and report errors that an engineer could rely on.

## Slide 41: Block 1, part C: this week's tasks

Part C of 3. 20 marks.

Today's tasks are part C of the Block 1 pack, worth 20 of its 60 marks. They use group_split and predict_regression.
This is the last part. The pack closes Tuesday 17 November 2026, 11:00 Kampala time. Part A and part B are the earlier weeks' notebooks.
The quiz opens after today's class.

**Spoken script**

This week's tasks are part C of the Block 1 assignment pack, worth twenty marks. They are built around group_split and predict_regression.

This is the last part, so the whole pack is due by Tuesday 17 November at 11:00 Kampala time. In a moment we show where each part is submitted.

The Block 1 quiz opens after today's class.

## Slide 42: Your issued task

01

Investigate building cooling load.

02

Target units: kW.

03

These are synthetic teaching records for practice.

04

Each record is one operating observation; equipment_id repeats across observations.

**Spoken script**

Here is the setting for your own work. In this cohort we investigate cooling load, and its unit is kW.

Each row in the data is one operating observation. record underscore id is the identifier of that observation. load underscore pct is the load in percent, and ambient underscore c is the surrounding temperature in degrees Celsius. The target holds the known answer, and we use it in training.

equipment underscore id repeats across rows, because one machine produces many observations. That is the reason we split by equipment group.

These are synthetic teaching records. They do not describe a calibrated physical relationship, and they are not suitable for running real equipment. We practise the method on them, and we do not rely on the numbers.

## Slide 43: group_split(records)

Assign whole equipment groups: E1–E4 to train, E5 to validation, E6 to test.

Return train, validation and test lists of record_id in input order.

Do not use target values to choose membership.

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

The first required function is group underscore split, which takes the argument records.

It must decide which observations go to training, validation and test, and it does so by whole equipment groups. Every observation from E1, E2, E3 and E4 goes to training. Every observation from E5 goes to validation. Every observation from E6 goes to test.

The function returns three lists under the names train, validation and test. Each list holds record underscore id values, and they must appear in the same order as in the input.

The function must not look at target values to decide membership. The equipment ID alone decides.

We keep the function name and the output names exactly as published, because the grader looks for those names. We also check the types, the units and the issued brief before we submit.

## Slide 44: predict_regression(training_records, feature_records)

Fit a training-mean baseline, linear regression and a decision tree (max_depth=4, random_state=17) using load_pct and ambient_c only.

Return three prediction lists under baseline, linear and tree.

Feature records have no target.

Fit preprocessing only on training data.

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

The second required function is predict underscore regression. It takes two inputs, training underscore records and feature underscore records.

Inside, we fit three models on the training records. The first is a baseline that always predicts the training mean. The second is a linear regression. The third is a decision tree with max underscore depth equal to four and random underscore state equal to seventeen. All three use load underscore pct and ambient underscore c as their only inputs.

Any filling of missing input values must be learned from the training records only, exactly as we practised.

Then we predict for the feature records. These records have no target column, because they stand for new observations. The function returns three lists of predictions, one list for each model, under the names baseline, linear and tree.

As always, we keep the function name and these output names exactly, and we check types, units and the issued brief.

## Slide 45: Written evidence

01

Use the cell headed “My written evidence”.

02

Explain the supplied scenario in your own words.

03

State target units, reasons and limitations.

04

Submit one complete notebook containing code and written evidence.

**Spoken script**

Along with the code, we write down our reasoning. The notebook has a cell headed My written evidence, and that is where the writing goes.

In it we explain the supplied scenario in our own words. We state the target and its unit, which is kW for cooling load. We give our reasons for the choices we made, and we state the limitations of what we found.

A good explanation ties a decision to a result. For example, we can say why a median learned from the training rows alone keeps evaluation information out of the preparation.

We describe the scenario figures as supplied. They are given to us, so we do not present them as measurements we made.

The code and the written evidence for this part go in one complete notebook, and that notebook goes into the Block 1 pack.

## Slide 46: Submit the Block 1 assignment pack

01

Part A: Regression and baseline (A7, Week 8)

Open the A7 form

02

Part B: Classification and cost (A8, Week 9)

Open the A8 form

03

Part C: Validation and trust (A9, Week 10)

Open the A9 form

Closes Tuesday 17 November 2026, 11:00 Kampala time. Submit each notebook to its own form, with your full Student Registration Number.

**Spoken script**

This slide is where the Block 1 assignment pack goes in. It has 3 parts, one notebook for each, and each part has its own form.

Open the form for each part in turn, enter your full Student Registration Number, and upload that part's notebook. Do not wait for the last minute, because the pack closes Tuesday 17 November at 11:00 Kampala time, and all parts close together.

A part that is not submitted scores zero for that part. The block marks are never dropped, so each part counts.

## Slide 47: Block 1 quiz: three forms, 15 questions

01

Week 8 form (5 questions)

Open the Week 8 quiz form

02

Week 9 form (5 questions)

Open the Week 9 quiz form

03

Week 10 form (5 questions)

Open the Week 10 quiz form

Opens after today's class. Each form stays open for 24 hours. Use your Student Registration Number and registered account.

**Spoken script**

The Block 1 quiz is three short forms, one for each week of the block, with five questions each. Together they are fifteen questions and fifteen marks.

The forms open after today's class, when the lecturer activates them, and each stays open for twenty-four hours. Open them one after the other and answer individually, using your Student Registration Number and your registered account.

This quiz replaces the three weekly quizzes of Weeks 8, 9 and 10. Like the assignment pack, it counts in full and is not dropped.

## Slide 48: Revision and submission checklist

Explain to a classmate how you would tell that a model is overfitting, and give one way leakage could creep into your own data preparation.

Keep raw data unchanged. Restart and run all cells before you hand in your Block 1 notebooks.

Point to your evidence. Save your work.

**Spoken script**

Here is a check we do individually before leaving.

First, we explain to a classmate how we would tell that a model is overfitting. Then we give one way that leakage could creep into our own data preparation. If we can say both in plain words, we have the main ideas of the week.

Then the practical items. We keep the raw data unchanged. Before we hand in our Block 1 notebooks, we restart the session and run all cells from the top, to confirm that the notebook works from start to finish.

We point to our evidence for each claim, and we save our work.

## Slide 49: Optional revision video

01

For revision after class.

02

StatQuest with Josh Starmer
Machine Learning Fundamentals Cross Validation

03

Opening up to 04:00, optional preview-selected excerpt

04

Listening question: Why evaluate using observations not used to fit that particular model?

Open explainer video

https://www.youtube.com/watch?v=fSytzGwwBVw

**Spoken script**

This video is for revision after class, and it is optional.

It is from StatQuest with Josh Starmer and it is called Machine Learning Fundamentals, Cross Validation. We watch the opening, up to the four minute mark.

We watch with one question in mind. Why do we evaluate a model using observations that were not used to fit that particular model?

After watching, we try to answer in our own words, using the ideas from today. The link is on the slide.
