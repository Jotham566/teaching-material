# CML3112 Week 12

Each slide shows its text, then the spoken script the lecturer reads aloud.

## Slide 1: Choosing and explaining a model

Civil Engineering and Architecture

Tuesday 24 November 2026
Tuesday 11:00–14:00, Room 106

**Spoken script**

Welcome to Week 12. Over the past weeks we built models, scored them and checked them for overfitting and leakage.

Today we answer the question an engineer faces next. Several models are available, so which one do we recommend? We compare them on the same rows, apply an error limit and a speed limit, and explain our choice in plain words.

## Slide 2: Today’s learning

WHAT WE WILL DO
Compare candidate models on the same rows, apply the limits an engineer sets, and explain the choice. Meet random forests and boosting, and write the limits of a model in plain words.

HOW YOU WILL SHOW IT
You can select a model that meets stated limits, say who is affected when it is wrong, and describe its purpose, data, scores and limits on one page.

**Spoken script**

This week we choose. Several models can do the job, so we compare them on the same rows, apply the limits an engineer sets, such as error and speed, and explain the choice. We also meet two more families, random forests and boosting. And we finish with the human side: who is affected when a model is wrong. By the end you can select a model that meets stated limits and describe its purpose, data, scores and limits on one page.

## Slide 3: Words for today: choosing a model

**Spoken script**

Six words for choosing a model. A candidate is a model being considered for the job. A constraint is a limit a candidate must meet before it is allowed, for example an error limit or a speed limit. Latency is the time one prediction takes. An ensemble is many models whose answers are combined. A random forest is an ensemble of many trees that each see different rows, and their answers are averaged. Boosting adds small models one after another, each one fixing the mistakes of the last. We only name boosting today, and we study it in Semester 2.

## Slide 4: The supplied file

Extract this week’s student ZIP. Upload engineering_data.csv into Colab using the Files panel, or keep them beside the notebook locally.

The examples below read this file. Run the cells in slide order. Keep the original CSV unchanged.

**Spoken script**

Every example today reads one file called engineering_data dot csv. It comes inside this week's student ZIP, so first we extract the ZIP.

In Colab we open the Files panel on the left and upload engineering_data dot csv there. If we work on our own computer, we keep the file in the same folder as the notebook. Uploading a notebook alone does not upload the data, so the file must be placed separately.

The examples that follow run in slide order, so each cell can use the names made by the cell before it. We never edit the original CSV. It stays exactly as supplied, and all our changes happen on copies inside Python.

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

This cell loads the data and takes a first look at it.

The first line imports pandas and gives it the short name pd, as we have done since Week 3. The second line calls pd dot read underscore csv with the file name. It reads the file and returns a table, which we store under the name raw underscore data. This is our untouched original.

Then we print three things. Dot head shows the first five rows, so we see the column names and a few example values. Dot shape gives two numbers, the count of rows and then the count of columns. Dot dtypes lists each column with its data type, so we can see which columns hold numbers and which hold text.

We compare what prints with the explanation in the notebook. If the column names or the types look wrong, we fix that before going further.

## Slide 6: Preparing the supplied modelling rows: step 1

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

Now we clean the table into modelling data. The first line drops duplicate rows. Dot drop underscore duplicates with record underscore id keeps only the first row for each record ID. Dot copy gives us a separate table, so later changes cannot touch raw underscore data.

Next we ask two yes or no questions about every row. Dot notna on the target column answers True where a target value was recorded. Dot between with zero and one hundred answers True where load percent lies from zero up to one hundred, including both ends.

The ampersand combines the two answers. A row gets True only when both checks pass. We print the first few answers of each check to see the True and False values.

Then we use the combined answers to keep only the passing rows, and copy again. The last line prints the row count before and after cleaning. The second number should be the same or smaller, and the gap tells us how many rows failed a check.

## Slide 7: Choose groups before choosing rows

isin(list_of_labels) answers True when a row’s equipment ID appears in the list.

Here E1–E4 supply training rows, E5 validation rows and E6 test rows.

The groups stay separate so one equipment group cannot appear on both sides.

**Spoken script**

Before we split the data, we decide which equipment goes where. The tool for this is the isin method. We give it a list of labels, and for each row it answers True when that row's equipment ID appears in the list.

In this lesson equipment E1 to E4 supply the training rows. Equipment E5 supplies the validation rows, and equipment E6 supplies the test rows.

We keep the groups completely separate. Each machine sits on one side only. If the same machine appeared in both training and validation, the model could recognise it and the score would look better than it deserves. This is the leakage idea from Week 10 applied to whole machines.

## Slide 8: Preparing the supplied modelling rows: step 2

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

This cell builds three True and False columns, one for each group. Nothing prints, because we are only storing answers for the next cell.

The first line takes the equipment ID column and calls isin with the list E1, E2, E3 and E4. Each row gets True if its machine is in that list. We store the result as is underscore training underscore equipment.

The second line does the same with a list holding only E5, giving is underscore validation underscore equipment. The third line uses E6 to make is underscore test underscore equipment.

Notice that each machine appears in exactly one list. That guarantees no row can be both a training row and a test row. The long first line is written across three lines for readability, and Python reads it as one statement because the brackets are still open.

## Slide 9: Preparing the supplied modelling rows: step 3

training_data: rows used to learn model settings; only these rows may determine imputation values.

validation_data: separate rows used to compare models without fitting on them.

**Spoken script**

Two names matter on this slide. Training underscore data holds the rows the model learns from. Every setting we learn, including the values an imputer uses to fill gaps, comes from these rows only. Using other rows would let outside information leak in.

Validation underscore data holds separate rows that we use to compare models. We score on them, but we never fit on them. That makes the comparison fair, because every candidate meets rows it has never seen.

There is also a third table, test underscore data. We keep it locked away until the choice is fixed.

## Slide 10: Preparing the supplied modelling rows: step 3

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

Now we turn the True and False columns into three real tables. Putting a True and False column inside square brackets keeps only the rows marked True. So the first line gives training underscore data, the second gives validation underscore data, and the third gives test underscore data. Each ends with dot copy so the tables are independent.

Then we name the inputs. Feature underscore columns is a list holding load underscore pct and ambient underscore c. These are the columns the model will use to predict cooling load.

The last line prints three row counts, in the order training, validation, test. We check that training is the largest and that none of the three is empty. A model cannot be scored on an empty table.

## Slide 11: The Week 8 line, rebuilt in a few lines

Every line repeats Week 8: split into X and y, fit the pipeline, predict, score.
The names X_valid, linear_model and mae are used again in the next cells.
The printed number is the validation MAE of the line.

The same rows, the same pipeline, the same MAE as Week 8.

```python
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
X_train = training_data[feature_columns]
y_train = training_data["target"]
X_valid = validation_data[feature_columns]
linear_model = make_pipeline(
    SimpleImputer(strategy="median"), LinearRegression())
linear_model.fit(X_train, y_train)
validation_predictions = linear_model.predict(X_valid)
mae = mean_absolute_error(
    validation_data["target"], validation_predictions)
print(round(mae, 4))
```

Output on the slide:

```text
0.7427
```

**Spoken script**

Choosing a model starts with having the candidates ready, so we rebuild the line from Week 8 in a few lines. We split the rows into X and y, fit the pipeline of an imputer and a line on the training rows, predict on the validation rows, and score the predictions with mean absolute error.

Nothing here is new. We repeat it because the next cells reuse three names from it: X valid, linear model and mae. The number printed at the end is the validation MAE of the line. It is the same number that appears in the three-candidates table on the next slide.

## Slide 12: Three candidates on the same validation rows

All three were scored on the same rows, in the same unit.
Speed comes next: a candidate must also be fast enough.

**Spoken script**

Choosing a model means comparing candidates fairly. We score three of them on the same validation rows, so the comparison is fair. The average guess has an error of 9.69 kW. The straight line has 0.74. The tree has 3.39.

The right column applies one constraint from this week's classroom decision: error at most ten. Notice that error is only one of the things an engineer checks. The next slides add speed, and then the full selection rule.

## Slide 13: Candidate evidence and latency

The CSV supplies observations. We build the table of candidates and timings ourselves. Calculate validation MAE from its held-out observations.

Measure prediction time on this computer. Timing varies by machine and repeated run, so record the measurement conditions.

**Spoken script**

To choose between models we need two kinds of evidence for each one. The first is error. The second is speed.

The CSV file only holds observations. It does not contain a ready table of models and their timings, so we build that table ourselves.

For error, we fit each model on the training rows, predict the validation rows, and calculate the validation MAE. That is the average size of the mistakes, measured in kW.

For speed, we measure latency. Latency is how long one prediction takes, and we state it in milliseconds. A millisecond is one thousandth of a second.

Timing depends on the computer and changes a little from run to run. So we write down the conditions of our measurement, such as which machine we used.

## Slide 14: Operations for the next example

A table from Python values: pd.DataFrame(records) builds a table from row dictionaries. With a dictionary of column lists, keys become column names and each list supplies that column’s values.

**Spoken script**

The next example builds a small table directly from Python values, so we meet that tool first. The function is pd dot DataFrame, and a DataFrame is simply the pandas table we already know.

One way to call it is with a list of records, where each record is a dictionary describing one row.

The other way is with a dictionary of columns. Each key becomes a column name, and the list stored under that key supplies the values of that column. For example, a key called name with a list of model names gives us a name column.

In our example every list will hold exactly one value, so we get a table with one row. Later we can add more rows for more models.

## Slide 15: Measuring elapsed time

perf_counter() reads a high-resolution clock in seconds. Subtract the earlier reading from the later one, then multiply by 1000 for milliseconds. One measured run is an illustration and varies from run to run.

**Spoken script**

To measure speed we need a stopwatch inside Python. It is called perf underscore counter, and we import it from the time module.

Each time we call perf underscore counter, it reads a very precise clock and gives the reading in seconds. A single reading means little. The useful part is the difference between two readings.

So we read the clock before the work and read it again after the work. Subtracting the earlier reading from the later one gives the elapsed seconds.

Seconds are too large for something this fast, so we multiply by one thousand to get milliseconds.

One measured run only illustrates the idea. A reliable speed claim needs repeated measurements.

## Slide 16: Time the prediction step

perf_counter reads seconds from a high-resolution clock.

Read it immediately before and after predict.

Convert elapsed seconds to milliseconds and divide by row count.

One timing is illustrative: repeated measurements are needed for a reliable speed claim.

**Spoken script**

Our speed limit concerns the time a trained model takes to answer. So the stopwatch wraps the predict call alone. Predict is the method that takes input rows and returns one prediction for each row.

We read perf underscore counter immediately before predict and immediately after it. The difference is the elapsed time in seconds. We multiply by one thousand to get milliseconds.

Then we divide by the number of rows. The batch is small, and the limit applies to one row, so dividing gives the mean time per row in this batch. It is a rough guide to the time for a single prediction, since a batch shares some fixed overhead.

One timing is only an illustration. If we want to claim that a model is fast enough, we repeat the measurement several times and look at the results together.

## Slide 17: A measured candidate from the supplied validation data: step 1

prediction_start_time: timer reading immediately before predicting the batch.

Run the cell and read the output below it.

```python
from time import perf_counter
prediction_start_time = perf_counter()
linear_model.predict(X_valid)
prediction_time_ms = (
    (perf_counter() - prediction_start_time)
    * 1000
    / len(validation_data)
)
```

**Spoken script**

This cell times the linear model, the straight line we fitted earlier.

The first line imports perf underscore counter. The second line reads the clock and stores that reading as prediction underscore start underscore time.

The third line asks linear underscore model to predict for X underscore valid, which holds the validation inputs. We have no name on the left, because we only care about how long it takes. Predict uses what the model already learned and does not refit it.

The last statement reads the clock again and subtracts the start reading. That gives seconds. Multiplying by one thousand gives milliseconds. Dividing by len of validation underscore data spreads the time over the rows, so we get milliseconds per row. The result is stored as prediction underscore time underscore ms.

Nothing prints here. We use the stored value in the next cell.

## Slide 18: A measured candidate from the supplied validation data: step 2

candidate_models: table of model names, measured validation errors and prediction times.

**Spoken script**

Here we gather the evidence for each model into one table called candidate underscore models. Each row describes one model.

The table has three columns. Name holds the model's name. Validation underscore mae holds its error on the validation rows, in kW. Latency underscore ms holds the time for one prediction, in milliseconds.

Having everything in one table is useful because the next steps, filtering and ranking, are things pandas does very well. We apply the limits to the columns and let pandas sort out the winner.

Right now the table has the linear model only. Other models, such as the decision tree, can be added as extra rows in the same way.

## Slide 19: A measured candidate from the supplied validation data: step 2

candidate_models: one row per model, with its name, validation error and prediction time.

Run the cell and read the output below it.

```python
candidate_models = pd.DataFrame(
    {
        "name": ["linear"],
        "validation_mae": [float(mae)],
        "latency_ms": [prediction_time_ms],
    }
)
print(candidate_models)
```

**Spoken script**

This cell builds the candidate table and prints it.

We call pd dot DataFrame with a dictionary of three keys. The key name has a list holding the word linear. The key validation underscore mae has a list holding the error we calculated earlier. We wrap it in float, which turns it into a plain decimal number. The key latency underscore ms holds the per row time we just measured.

Each list has one entry, so the table has one row. We store it as candidate underscore models and print it.

In the printout we read across the row. We see the model's name, then its error in kW, then its latency in milliseconds. The left column of plain numbers is the row label that pandas adds automatically.

## Slide 20: The same recipe gives one row per candidate

Same recipe for every row: fit, predict, score the MAE, time the prediction.
Latency depends on your computer, so each student measures it.

**Spoken script**

The table on the previous slide has one row, because we measured only the line. The recipe does not change for other candidates. Fit the candidate on the training rows, predict on the validation rows, score its mean absolute error, and time its predict call. Then add one row to the table.

Here is the table we aim for, with three rows. The error column comes from the same validation rows we used all term. The latency column depends on your computer and on the moment you run it, so we fill it in by measuring in the notebook. In the assignment, the candidate table is handed to you, and your job is to apply the limits and choose.

## Slide 21: Constraints and tie-breaks

For this classroom decision, use MAE at most 10 target units and mean latency at most 10 ms per observation. These are stated practice requirements.

Filter both limits inclusively. sort_values ranks eligible rows by validation_mae, then latency_ms, then name. empty detects no eligible rows.

**Spoken script**

A good model for engineers must pass practical limits, and it must win a fair ranking. We handle those as two separate steps.

For this classroom decision the limits are fixed. The MAE may be at most 10 kW, and the mean latency may be at most 10 milliseconds for one observation. These are practice requirements set for the exercise.

The limits are inclusive. A model that scores exactly the limit still qualifies.

After filtering we rank the survivors with sort underscore values. Sort underscore values orders the rows of a table by the columns we name. We name validation underscore mae first, then latency underscore ms, then name. So the smallest error wins, equal errors are settled by speed, and equal speeds by alphabetical name.

Finally, empty tells us whether the filtered table has no rows. That happens when no model qualifies.

## Slide 22: Operations for the next example

01

Checking for no rows: equipment_data.empty is True when the filtered table has no entries. Check it before attempting to select a first row. empty is a property, without parentheses.

02

Sorting by several columns: equipment_data.sort_values(["validation_mae", "latency_ms", "name"]) sorts ascending by error first. Equal errors use latency, then alphabetical name as tie-breaks.

03

Selecting by row position: equipment_data.iloc[0] selects the first row by its position. ["name"] then selects that row’s name field. An empty table has no row at position zero.

**Spoken script**

Three small pandas tools appear in the next example.

First, dot empty. It is True when a table has no rows. It is a property, so we write it without parentheses. We check it before picking a first row.

Second, sort underscore values. We pass it a list of column names. It sorts upward, smallest first, by the first column. When two rows tie there, the second column decides, and the third column decides after that. In our case that means error, then latency, then name in alphabetical order.

Third, dot iloc. It picks a row by its position in the table, counting from zero. So iloc with zero in square brackets gives the first row. Putting the word name in square brackets after it gives that row's name entry.

A table with no rows has no position zero, which is why we test for empty first.

## Slide 23: Checking a condition before calculating

if condition: runs its indented statements only when the condition is True. else: handles the other case. Check for a nonzero denominator before division, and for a nonempty table before selecting its first row.

**Spoken script**

Sometimes code must choose between two paths. We do that with if and else, which we met in the first weeks.

The word if is followed by a condition. If the condition is True, Python runs the indented lines underneath it. If it is False, Python skips them. The word else covers the other case, and its indented lines run instead.

This protects us from errors. Before dividing, we check that the number we divide by is nonzero. Before taking the first row of a table, we check that the table has some rows.

In the next examples we use exactly this pattern. If the table of acceptable models is empty, we choose nothing. Otherwise we pick the first row.

## Slide 24: Selection from the measured candidate table: step 1

Run the cell and read the output below it.

Run the cell and read the output below it.

```python
error_is_acceptable = candidate_models["validation_mae"] <= 10
time_is_acceptable = candidate_models["latency_ms"] <= 10
model_is_eligible = error_is_acceptable & time_is_acceptable
```

**Spoken script**

This cell finds which models meet the limits. It stores three True and False columns and prints nothing.

The first line compares the validation underscore mae column with ten using less than or equal to. Every row gets True if its error is at most the limit. The second line does the same with latency underscore ms and the ten millisecond limit.

The third line joins the two with an ampersand. The ampersand means and. A model gets True only when its error and its speed are both within the limits. If either one fails, the model gets False.

The result, model underscore is underscore eligible, is a mask. We used masks in the early pandas weeks to pick rows. The next cell applies this mask to the table.

## Slide 25: Apply both model-selection rules

A candidate must satisfy both the error limit and the time limit.

Compare each column with its limit first, then combine the True/False answers with &.

Filtering can return no rows.

**Spoken script**

A candidate has to satisfy two rules together. A low error alone is not enough, because a very accurate model might take too long to answer. A fast model alone is also not enough, because it might make mistakes that are too large.

So we handle each rule on its own first. We compare one column with its limit, and that gives a column of True and False answers. We do the same for the other column.

Then we combine the two columns of answers with the ampersand. A row survives only if both answers are True.

It is possible that no row survives. If every model breaks at least one limit, the filtered table comes back with zero rows. We need to expect that case and plan for it.

## Slide 26: Selection from the measured candidate table: step 2

eligible_models: candidates satisfying both stated limits.

Run the cell and read the output below it.

```python
eligible_models = candidate_models[model_is_eligible]
```

**Spoken script**

This is a short but important cell. We take candidate underscore models and put model underscore is underscore eligible inside square brackets. The brackets keep only the rows where the mask says True, exactly like the row filtering we practised earlier.

The result is stored as eligible underscore models. It holds every model that meets both limits, and nothing else.

Nothing prints, so we see no output. The table is waiting for the next step, which ranks it.

If no model met both limits, eligible underscore models is simply a table with no rows. It is still a valid table, so Python gives no error here.

## Slide 27: Choose only if an eligible model exists

sort_values orders by error, then time, then name. empty answers whether no rows remain.

Check it before iloc[0], which requests the first row by position.

Return None when no candidate qualifies.

**Spoken script**

Now we pick the winner from the models that passed. First we rank them with sort underscore values, using error, then time, then name. The best candidate moves to the top.

Then we need the first row. The iloc tool picks a row by position, and position zero is the top row. But if the table has no rows at all, asking for position zero causes an error.

So we ask first. Dot empty answers True when no rows remain. If it is True, no model qualified, and we give back None, which is Python's value for nothing here. Otherwise we take the first row and read its name.

This gives a clear and honest answer in every case. Either we name one model, or we report that nobody met the requirements.

## Slide 28: Selection from the measured candidate table: step 3

eligible_models: candidates satisfying both stated limits.

Run the cell and read the output below it.

```python
ranked_models = eligible_models.sort_values(
    ["validation_mae", "latency_ms", "name"]
)
if ranked_models.empty:
    selected_model_name = None
else:
    selected_model_name = ranked_models.iloc[0]["name"]
print(selected_model_name)
```

**Spoken script**

Here is the full selection logic.

The first statement sorts eligible underscore models by validation underscore mae, then latency underscore ms, then name, and stores the ranked table.

Then comes the if. If ranked underscore models dot empty is True, there are no rows, so we set selected underscore model underscore name to None. In the else branch, at least one model exists. We take iloc zero, the top row, and read its name field.

The last line prints the answer. The output is either the name of a model, or the word None.

We read it as our recommendation. A name means that this model passed both limits and had the smallest error among those that passed. None means we must report that no candidate meets the requirements.

## Slide 29: Interpreting the recommendation

State the data, split, metric, timing method and constraints. Report when the measured model fails a requirement.

Tune hyperparameters using validation or cross-validation. Preserve the final test until the choice is fixed.

**Spoken script**

A recommendation is only useful when others can check how we reached it. So we state the data we used, how we split it, which metric we scored with, how we measured the timing, and what limits we applied.

We also report honestly when the model we measured fails a requirement. A result of None is a finding, and it belongs in the report.

When we tune hyperparameters, which are the settings we choose before training, we do that using the validation rows or using cross-validation. We never use the test rows for it.

The test rows are kept until the choice is fixed. Then we score once on them and report the number. If we peeked earlier, that final number would no longer be an honest estimate.

## Slide 30: A random forest averages many trees

Illustrative numbers. Each tree sees different rows, and the forest averages their answers.

**Spoken script**

One tree can be jumpy. A random forest builds many trees, each trained on a different random sample of the rows, and averages their answers. In the picture, five trees give five different predictions. The forest reports their average. Averaging smooths out the jumpiness of any single tree.

The numbers in this picture are invented to show the idea. In scikit-learn the class is called RandomForestRegressor, and it follows the same create, fit, predict pattern you already know. The setting n estimators is the number of trees. You will try it in the notebook, and you may find that on a clean straight pattern like ours the plain line is hard to beat. A forest earns its place when the pattern is curved or the inputs interact.

## Slide 31: A forest uses the same create, fit, predict pattern

RandomForestRegressor(
    n_estimators=100,
    random_state=17)

n_estimators is the number of trees. random_state fixes the random choices so everyone gets the same forest.
Use it exactly like the other models: forest.fit(X_train, y_train), then forest.predict(X_valid).
Score it with the same MAE on the same validation rows, and compare it with the baseline and the line.

**Spoken script**

Here is the whole forest in one line. N estimators is the number of trees, and random state fixes the random choices so everyone gets the same forest. After that it behaves like every model you have used. Fit on the training rows, predict on the validation rows, and score it with the same MAE.

In the notebook, run it and put its error beside the baseline, the line and the tree. Fair comparison, same rows.

## Slide 32: Boosting adds small trees that fix what is still wrong

Illustrative numbers. Named here and taught in Semester 2.

**Spoken script**

Gradient boosting is another way to combine trees. Instead of many trees averaging at once, it adds small trees one after another. Each new tree is trained to fix what the earlier ones still get wrong. In the picture, the first stage predicts seventy when the truth is eighty, so ten is still missing. The second stage moves the prediction to seventy-seven. The third moves it to seventy-nine point one.

Boosting is behind many winning entries in data competitions, which is why we name it today. These numbers are invented. We study the real thing in Semester 2, after gradient descent, which you previewed in Week 8.

## Slide 33: A model card puts the evidence on one page

**Spoken script**

A model card is a one page note that travels with a model. It answers five questions. What decision does the model support? What rows trained and tested it? How well does it do, beside a baseline? Where should it not be trusted? Who checks it, and when?

The example on the right is for the model we have built. Writing this card is excellent practice for the written evidence in your project, because it forces you to state the limits next to the score.

## Slide 34: Who is affected when a model is wrong

A MISSED ALERT (FALSE NEGATIVE)
Suppose an alert fires when the predicted cooling load passes a limit we choose. If a real problem goes unwarned, equipment can be damaged and people nearby can be put at risk.
Check that the training data looks like where the model will run. A new machine may behave differently from E1 to E4.

A FALSE ALARM (FALSE POSITIVE)
Inspections are wasted, and operators learn to ignore the alerts. A model nobody trusts protects nobody.
Choose the threshold with the people who live with the consequences.

**Spoken script**

Every model makes mistakes, and the mistakes land on someone. Suppose an alert fires when the predicted value passes a limit we choose. A missed alert means a real problem goes unwarned. Equipment can be damaged and people nearby can be put at risk. A false alarm wastes inspections, and operators who hear too many false alarms learn to ignore the alerts. A model nobody trusts protects nobody.

Two habits follow. Choose the threshold together with the people who live with the consequences. And check that the training data looks like the place where the model will run. A new machine may behave differently from the ones we trained on, and a model trained on one fleet can fail on another.

## Slide 35: Take care with data about people

MACHINE DATA
Sensor readings from a motor, a building plant or a crusher carry little personal risk.
Data about workers, drivers or customers is different. It can identify a person.

WHAT TO DO
Uganda's Data Protection and Privacy Act, 2019 protects personal data. Collect only what you need, keep it safe, and say what it is used for.
This is a summary for learning and is not legal advice.

**Spoken script**

Most of our data comes from machines, and machine data carries little personal risk. Data about workers, drivers or customers is different, because it can identify a person.

Uganda's Data Protection and Privacy Act of 2019 protects personal data. The habits that follow are simple. Collect only what you need. Keep it safe. And say what it will be used for. This is a learning summary and is not legal advice, so for a real project, ask for qualified advice.

## Slide 36: Block 2, part B: this week's tasks

Part B of 2. 20 marks.

Today's tasks are part B of the Block 2 pack, worth 20 of its 40 marks. They use select_model and regression_errors.
The pack closes Monday 7 December 2026, 23:59 Kampala time.
There is no quiz after today's class. The Block 2 quiz comes after the Week 13 class.

**Spoken script**

This week's tasks are part B of the Block 2 assignment pack, worth twenty marks. They are built around select_model and regression_errors.

This is the last part, so the whole pack is due by Monday 7 December at 23:59 Kampala time. In a moment we show where each part is submitted.

There is no quiz today. The Block 2 quiz opens after the Week 13 class.

## Slide 37: Your issued task

01

Investigate building cooling load.

02

Target units: kW.

03

These are synthetic teaching records for practice.

04

Each record is one operating observation; equipment_id repeats across observations.

**Spoken script**

This slide gives your own task for the week. We are investigating cooling load.

The unit of the target is kW. Use that unit whenever you write about errors and results.

The records are synthetic teaching data. They are made for learning and are not measurements that could be used to run real equipment.

Each record is one operating observation. A column such as equipment underscore id can repeat, because one machine appears in many observations. Record underscore id identifies each single observation, and the target column holds the known answer that the model learns to predict.

## Slide 38: select_model(candidates, max_mae, max_ms)

Candidates have name, validation_mae and latency_ms.

Keep those meeting both inclusive constraints; select smallest validation_mae, then latency_ms, then name alphabetically.

Return the selected name or None.

Never use test scores for selection.

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

The first required function is select underscore model. It takes three inputs. Candidates is a table with columns name, validation underscore mae and latency underscore ms. Max underscore mae is the error limit, and max underscore ms is the speed limit.

Inside, the function keeps the rows that meet both limits, and the comparison is inclusive, so a value equal to the limit passes. Among those, it picks the one with the smallest validation underscore mae. If errors tie, the smaller latency underscore ms wins. If that ties too, the alphabetically first name wins.

The function returns the chosen name, or None when no candidate qualifies.

It works only with validation scores. Test scores are never used to select. Keep the function name and the output exactly as written, and check the types and units against your issued brief.

## Slide 39: regression_errors(actual, predicted)

Return mae and rmse, calculated over the same paired observations, with full precision.

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

The second required function is regression underscore errors. It takes two inputs. Actual holds the true values of cooling load, and predicted holds what the model said for the same observations. They must line up, so the first actual value pairs with the first predicted value, and so on.

The function returns two numbers. MAE is the mean absolute error, the average size of the mistakes. RMSE is the root mean squared error, which punishes large mistakes more heavily. Both are measured in kW, as in Week 8.

Both must be calculated over the same paired observations. Give the results with full precision and do not round them. Keep the exact names, mae and rmse, because the grader looks for them.

## Slide 40: Written evidence

01

Use the cell headed “My written evidence”.

02

Explain the supplied scenario in your own words.

03

State target units, reasons and limitations.

04

Submit one complete notebook containing code and written evidence.

**Spoken script**

Your notebook holds more than code. It also holds your written reasoning.

Find the cell headed My written evidence. In that cell you explain the supplied scenario in your own words. Copying the prompts or the code comments does not count, because we want to read what you understood.

Your explanation should state the target units, give your reasons for the choice you made, and name the limitations of the result. A limitation might be the small data size, or the fact that the data is synthetic.

The code and the written evidence for this part go in one complete notebook, and that notebook goes into the Block 2 pack.

## Slide 41: Project preparation

01

Use the published machine learning project brief.

02

Build the evidence gradually in your project notebook.

03

Keep raw data, labelled charts, run instructions and individual contributions.

04

Published deadline: 15 Dec 2026, 11:00 Kampala

**Spoken script**

Your machine learning project starts now, and the work builds up gradually.

Use the published project brief as your guide. Keep a project notebook, and add evidence to it as you go. Do it in small steps over the weeks, so that nothing has to be rebuilt at the end.

Keep the raw data unchanged, your labelled charts, the instructions for running your work, and a record of what each team member did. For the contributions, name a specific file, function or chart and the decision behind it.

Check the project deadline shown on the slide and plan backwards from it.

## Slide 42: Words from today

**Spoken script**

Six words to keep. A candidate is a model being considered. A constraint is a limit it must meet. A random forest averages many trees. Boosting adds small trees that fix earlier mistakes, and we study it in Semester 2. A model card records purpose, data, scores and limits on one page. A false negative is a missed alert, usually the costly mistake. In the assignment you apply the constraints and choose a model, and you explain the choice in your own words.

## Slide 43: Submit the Block 2 assignment pack

01

Part A: Features and ablation (A10, Week 11)

Open the A10 form

02

Part B: Model recommendation (A11, Week 12)

Open the A11 form

Closes Monday 7 December 2026, 23:59 Kampala time. Submit each notebook to its own form, with your full Student Registration Number.

**Spoken script**

This slide is where the Block 2 assignment pack goes in. It has 2 parts, one notebook for each, and each part has its own form.

Open the form for each part in turn, enter your full Student Registration Number, and upload that part's notebook. Do not wait for the last minute, because the pack closes Monday 7 December at 23:59 Kampala time, and all parts close together.

A part that is not submitted scores zero for that part. The block marks are never dropped, so each part counts.

## Slide 44: Revision and submission checklist

Explain to a classmate how you would choose between two models, and name one limit you would write on a model card.

Keep raw data unchanged. Restart and run all cells before you hand in your Block 2 notebooks.

Point to your evidence. Save your work.

**Spoken script**

Before we finish, here is a short check to do on your own.

Explain to a classmate how you would choose between two models. Start from the limits, then the ranking. Then name one limit you would write on a model card, such as the data it was trained on or where it may not work well.

Before submitting, remember two habits. Keep the raw data unchanged. Then restart the notebook and run all cells from the top, so you know the whole notebook runs cleanly.

As you work, point to your evidence for each claim, and save your work.

## Slide 45: Optional revision video

01

For revision after class.

02

StatQuest with Josh Starmer
Machine Learning Fundamentals: Bias and Variance

03

Opening up to 04:00, optional preview-selected excerpt

04

Listening question: What goes wrong with a model that is too simple, and with one that is too flexible?

Open explainer video

https://www.youtube.com/watch?v=fSytzGwwBVw

**Spoken script**

This optional video is for revision after class. It is a short StatQuest explanation of bias and variance, the two ways a model can go wrong. A model that is too simple misses the pattern, and a model that is too flexible chases noise.

Before you watch, hold one question in mind: what goes wrong with a model that is too simple, and with one that is too flexible? Then watch the opening four minutes and answer it in your own words. The video supports revision of the Week 10 and Week 12 ideas, and watching it is optional.
