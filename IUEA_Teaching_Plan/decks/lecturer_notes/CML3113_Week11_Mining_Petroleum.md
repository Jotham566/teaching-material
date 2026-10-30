# CML3113 Week 11

Each slide shows its text, then the spoken script the lecturer reads aloud.

## Slide 1: Creating and testing a useful feature

Mining and Petroleum Engineering

Friday 20 November 2026
Friday 08:00–11:00, Room 105

**Spoken script**

Welcome to Week 11. This week we build new input columns from the columns we already have, and we test whether each new column makes our predictions better.

We also learn to read which input moves a prediction more. By the end of the session you will be able to add a column, compare two models fairly, and decide from the numbers whether the column stays.

## Slide 2: Today’s learning

WHAT WE WILL DO
Build new input columns from the ones we have, test whether each one helps, and read which input moves a prediction more. Learn the words feature engineering, interaction and ablation.

HOW YOU WILL SHOW IT
You can build a derived feature, compare models with and without it on the same rows, and decide from the evidence whether to keep it.

**Spoken script**

Last week we learned how to trust a score. This week we try to improve the model by giving it better inputs. We will build new columns from the ones we have, test whether each one really helps, and learn to read which input moves a prediction more. By the end you can build a derived feature, compare models with and without it on the same rows, and decide from the evidence whether to keep it.

## Slide 3: Words for today: making inputs more useful

**Spoken script**

Six words for today. Feature engineering means building new input columns from the columns you already have. A derived feature is one column calculated from others, such as load divided by one hundred. An interaction multiplies two inputs together, for example load times ambient temperature. Scaling puts inputs on a common ruler, and you used it in Week 9. Ablation means adding or removing one piece and comparing the scores. Available at prediction time is the rule that every input must be something you will really have when the model is used.

Today is where your engineering knowledge beats a better programmer. You know which combinations of measurements mean something physically.

## Slide 4: The supplied file

Extract this week’s student ZIP. Upload engineering_data.csv into Colab using the Files panel, or keep them beside the notebook locally.

The examples below read this file. Run the cells in slide order. Keep the original CSV unchanged.

**Spoken script**

Every example today reads one file called engineering_data dot csv. A CSV file is a table saved as plain text, one row per line, with commas between the columns.

Extract this week's student ZIP folder first. If you work in Colab, open the Files panel and upload engineering_data dot csv there. If you work on your own computer, keep the file in the same folder as your notebook.

The notebook and the data file travel separately, so uploading the notebook does not upload the data. Check that the filename and the column headings match what the code expects.

Run the cells in the order the slides show them, because each cell uses names created by the one before. We never edit the original CSV. It stays as the untouched record, and every change we make happens on copies inside Python.

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

We start by loading the data. The first line imports pandas and gives it the short name pd, as we did in earlier weeks.

The second line calls pd dot read_csv with the filename. It reads the file and returns a DataFrame, which is a table, and we store it under the name raw_data. This table is the original, so we keep it unchanged and can always return to it when we want to check our work.

The next three lines print things about the table. Dot head shows the first five rows, so we can see the column names and a few values. Dot shape gives two numbers, the count of rows and then the count of columns. Dot dtypes lists the type of each column, for example whole numbers, decimals or text.

Look for three things. The column names should match the brief. The row count should look reasonable. And the numeric columns should show as numbers and not as text, because text cannot go into a model.

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

Now we clean the table before modelling. We keep only rows we can trust.

The first line calls drop_duplicates on record_id. If the same record appears twice, only the first copy is kept. Dot copy then makes an independent table called modelling_data, so changes to it never touch raw_data.

The next line asks of every row, is the target recorded. Dot notna gives True where a value is present and False where it is missing. A row with no known answer cannot teach or test a model.

The line after that uses dot between with zero and one hundred. It gives True when load_pct is a valid percentage between those limits.

The and symbol, the ampersand, combines the two checks. A row is kept only when both are True.

We print the first few True and False values to see the checks working, and look for any False. Then we keep the passing rows and print two lengths. The second length is the count after cleaning, and it can only be the same or smaller than the first. The gap shows how many rows we removed.

## Slide 7: Choose groups before choosing rows

isin(list_of_labels) answers True when a row’s equipment ID appears in the list.

Here E1–E4 supply training rows, E5 validation rows and E6 test rows.

The groups stay separate so one equipment group cannot appear on both sides.

**Spoken script**

Before we pick rows, we decide which equipment goes where. The method isin takes a list of labels and answers True for every row whose equipment ID appears in that list, and False for the others.

We use it to split by equipment. Equipment E1 to E4 supply the training rows, E5 supplies the validation rows, and E6 supplies the test rows.

The groups stay separate for a reason we met in Week 10. If one machine appeared on both sides, the model would be checked on a machine it had already studied, and the score would look better than it deserves. Keeping each machine on one side only means validation and test measure how the model copes with equipment it has never seen.

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

This cell builds three True and False columns, one for each group of equipment.

The first line takes the equipment_id column of modelling_data and applies isin with the list E1, E2, E3 and E4. It stores the answers as is_training_equipment. A row is True when its machine is one of those four.

The second line does the same for the list holding only E5, and calls the result is_validation_equipment.

The third line does the same for E6 and calls the result is_test_equipment.

The lists are written over several lines only to make them easy to read. Python treats the brackets as one expression.

This cell prints nothing. It only stores three sets of answers, and the next cell uses them to pick the actual rows.

## Slide 9: Preparing the supplied modelling rows: step 3

training_data: rows used to learn model settings; only these rows may determine imputation values.

validation_data: separate rows used to compare models without fitting on them.

**Spoken script**

Two of the tables we are about to create need a clear meaning before we build them.

training_data holds the rows the model learns from. Whatever the model learns, including the medians that the imputer uses to fill missing values, comes only from these rows.

validation_data holds separate rows. We use them to compare models, so they are never used for fitting. They act like an exam the model has not seen the questions for.

A third table, the test data, stays aside until the final check.

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

Here we turn the three True and False columns into three tables.

The first line puts the mask is_training_equipment inside square brackets after modelling_data. Python keeps the rows where the mask is True. Dot copy makes the result its own table, called training_data. The next two lines do the same for validation_data and test_data.

Then we write feature_columns, a list holding the two input names, load_pct and ambient_c. These are the inputs our model will use first.

The last line prints three lengths, the number of rows in training, in validation and in test. Check that none of them is zero, and that training has the most rows. If one is zero, the equipment labels or the masks above are wrong.

## Slide 11: A physical relationship can form a feature

Explain each quantity in the relationship and its unit before reading the pattern.

**Spoken script**

A derived feature is a new input column that we calculate from inputs we already have. We build one when we have a reason to think it will help.

Take load_pct divided by 100. It turns a percentage into a fraction between zero and one. The information is the same, written in different units.

Take load_pct times ambient_c. This is an interaction, which means the effect of one input depends on the other. A hot room together with a heavy load may matter more than either one alone. The units of this new column are percent times degrees Celsius, so we always say what a derived column measures before we use it.

An interaction is an idea we test, and it is not a measured law. A sensible story does not guarantee an improvement.

And we only use values we would have at the moment we make a prediction. We never build a feature from the target.

## Slide 12: A straight line misses a curve, and a new feature repairs it

Invented data. Adding x squared as a feature lets the same linear model follow the curve.

**Spoken script**

Why build new features at all? Here is an invented example. The dots follow a curve. On the left, a straight line through x misses the curve at both ends, and its MAE on these points is 2.41. On the right we gave the same linear model one extra input, x squared. That column is a derived feature. Now the fitted line bends with the dots and the MAE on the same points drops to 0.77.

The model type did not change. We changed what the model could see. That is feature engineering. In engineering data the useful new columns are often physical: a ratio, a product, a difference, a rate.

## Slide 13: Derived features from existing inputs

load_pct / 100 gives load_fraction. Multiplying load_pct by ambient_c gives the load_ambient interaction.

equipment_data["new_name"] = expression adds a column. Apply the same formulas to training and validation rows, without changing raw data.

**Spoken script**

We add two derived columns to our table.

The first is load_fraction. We take load_pct and divide it by 100, so a load of fifty percent becomes zero point five.

The second is load_ambient. We multiply load_pct by ambient_c. This is the interaction from the last slide.

In pandas we add a column by writing the table name, then the new column name in square brackets and quotes, then an equals sign, then the expression. If the name is new, pandas creates the column. If it exists, pandas replaces it.

Two rules matter here. We use the same formulas on the training rows and the validation rows, so the model sees the same kind of input in both. And we never change raw_data. We calculate on a copy.

## Slide 14: Operations for the next example

Adding or replacing a column: equipment_data["name"] = values assigns that column. An array follows row order. A Series aligns by row label, so keep labels paired with the intended observations.

Column arithmetic: Arithmetic on columns calculates one result per row. Series align by row label. Divide only where the denominator is valid and keep actual and predicted observations paired.

**Spoken script**

Three small operations appear in the next example, and we check each one first.

The first is adding or replacing a column. Writing a table, a column name in brackets, an equals sign and some values stores those values as that column. If the values are a plain array, they go in row order. If they are a Series, pandas matches them to rows by the row label, so the labels must belong to the right observations.

The second is column arithmetic. When we divide or multiply columns, pandas does the calculation on every row and returns one result per row. When two Series are combined, pandas again lines them up by row label.

Divide only where the bottom number is valid. Dividing by one hundred is always fine, but dividing by a column that could hold zero would not be. And keep each actual value paired with its own predicted value.

## Slide 15: Defining and calling a function

def gives a reusable block a name and input parameters. The indented statements run when it is called. return sends a result back to the caller; print displays a result but does not return it.

**Spoken script**

A function is a block of code with a name that we can run again and again.

The word def starts the definition. After it comes the function name and, in brackets, the parameters. A parameter is a name for an input that the function will receive when someone calls it.

The indented lines below are the body. They do nothing when we define the function. They run each time we call it.

The word return sends a result back to whoever called the function. The word print is different. It only shows something on the screen, and the value is lost afterwards unless we return it too.

In the next example we write one function that adds our new columns. Then we call it once on the training table and once on the validation table, so both get exactly the same calculation.

## Slide 16: Features from the supplied load and ambient columns (1/2)

Use the inputs and operations defined in the preceding slides.

Continue in the same code cell.

```python
def add_features(equipment_data):
    extended_data = equipment_data.copy()
    extended_data["load_fraction"] = (
        extended_data["load_pct"] / 100
    )
    extended_data["load_ambient"] = (
        extended_data["load_pct"] * extended_data["ambient_c"]
    )
```

**Spoken script**

We define a function called add_features. It takes one input, a table, which we call equipment_data inside the function.

The first line of the body makes a copy of that table and names it extended_data. Everything we change happens on the copy, so the table that was passed in stays as it was.

The next statement creates a column called load_fraction. It takes the load_pct column and divides it by 100. Every row gets its own answer.

The statement after it creates a column called load_ambient. It multiplies the load_pct column by the ambient_c column, row by row. That is our interaction feature.

The long expressions are split over several lines with brackets just to fit the slide. The code continues in the same cell on the next slide, where we send the finished table back.

## Slide 17: Features from the supplied load and ambient columns (2/2)

Use the inputs and operations defined in the preceding slides.

Run the cell and read the output below it.

```python
    return extended_data
training_features = add_features(training_data)
validation_features = add_features(validation_data)
print(
    training_features[
        ["load_pct", "load_fraction", "load_ambient"]
    ].head()
)
```

**Spoken script**

The cell continues with the last line of the function, return extended_data. This hands the table with the two new columns back to the caller.

Then we use the function. Calling add_features on training_data gives training_features. Calling it on validation_data gives validation_features. Both tables get the same two formulas, so the training and validation inputs are built the same way.

The final statement prints the first five rows of three columns, load_pct, load_fraction and load_ambient. We use it to check our work. Look at one row and test it in your head. The load_fraction value should equal the load percentage divided by one hundred. The load_ambient value should equal the load percentage multiplied by the ambient temperature. If either check fails, the formula has a mistake.

## Slide 18: Which input moves the prediction more?

effect of one spread = slope × standard deviation
Slopes come from the linear model fitted on the training rows. Spreads are the population standard deviation of the same rows, as StandardScaler calculates it.

**Spoken script**

The two slopes in our model are in different units, so comparing them directly is unfair. A slope of 0.16 for ambient temperature looks bigger than 0.12 for load, yet the load swings over a far wider range.

A fair comparison multiplies each slope by the typical spread of its input, the standard deviation. The result says how much the prediction changes when the input moves by one typical amount.

Here, one typical swing of load changes the prediction by 2.7 kWh/t, and one typical swing of ambient temperature changes it by 0.7 kWh/t. Load matters more. This is how scaling helps us read a model, as well as train it.

## Slide 19: Ablation compares the same observations

Fit one linear model using load_pct and ambient_c. Fit a second using those columns plus load_ambient.

Compare both on the same validation targets. Improvement equals baseline MAE minus extended MAE.

**Spoken script**

Ablation is a fair test of one feature. We take a model, remove the feature we want to judge, and compare the two versions.

Our first model, the base model, is a linear regression using load_pct and ambient_c. The second model, the extended model, is a linear regression using those two columns plus load_ambient. Only one thing differs between them.

Both models are scored on the same validation targets. The score is the MAE we know from Week 8, the average size of the miss in kWh/t.

Improvement equals the base MAE minus the extended MAE. Lower error is better, so a positive improvement means the extra feature helped. A value near zero means it made almost no difference, and a negative value means the extra feature made predictions worse.

## Slide 20: Change one feature set at a time

The base inputs are load and ambient temperature.

The extended inputs also include their product.

Train separate pipelines on the same rows and compare on the same validation rows.

This isolates the effect of adding the feature.

**Spoken script**

To know what a feature does, we change one thing and keep everything else the same.

The base inputs are the load and the ambient temperature. The extended inputs are those same two plus their product.

We train two separate pipelines on exactly the same training rows. A pipeline is a chain of steps that run in order, here an imputer followed by a regression. Then we compare them on exactly the same validation rows.

Because the rows, the model type and the scoring are all identical, any change in the error can be traced to the extra feature. If we also changed the rows or the split, we could not say what caused the difference.

## Slide 21: Paired ablation using the supplied CSV: step 1

base_feature_columns: input columns for the simpler comparison pipeline.

Run the cell and read the output below it.

```python
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
base_feature_columns = ["load_pct", "ambient_c"]
extended_feature_columns = base_feature_columns + ["load_ambient"]
```

**Spoken script**

This cell prepares the tools and the two lists of input columns. It prints nothing.

The first line imports SimpleImputer, which fills missing values using a rule we choose. The second imports make_pipeline, which chains steps together. The third imports LinearRegression, the straight-line model from Week 8. The fourth imports mean_absolute_error, the function that calculates MAE. Importing only makes these tools available. No model is trained yet.

Then we write base_feature_columns, a list with load_pct and ambient_c. These are the inputs of the simpler model.

The last line makes extended_feature_columns by taking the base list and adding a list that contains load_ambient. The plus sign joins the two lists into one longer list. So the extended list holds the base inputs and the feature we are testing.

## Slide 22: Fit both alternatives fairly

Each pipeline learns its own training medians and regression settings.

The base model sees only base columns; the extended model sees the additional feature.

Neither uses validation targets while learning.

**Spoken script**

Each pipeline learns by itself. The imputer inside a pipeline works out its own medians from the training rows it receives, and the regression inside learns its own settings from the same rows.

The base pipeline is shown only the base columns. The extended pipeline is shown the extra feature as well.

Neither pipeline looks at the validation targets while it learns. Those answers are kept hidden until we score the predictions. If a model could see them in advance, we would have the leakage problem from Week 10, and the validation score would no longer tell us anything honest.

Fitting each model on the same training rows gives both of them the same starting point.

## Slide 23: Paired ablation using the supplied CSV: step 2 (1/2)

base_feature_columns: input columns for the simpler comparison pipeline.

Continue in the same code cell.

```python
base_pipeline = make_pipeline(
    SimpleImputer(strategy="median"), LinearRegression()
)
extended_pipeline = make_pipeline(
    SimpleImputer(strategy="median"), LinearRegression()
)
```

**Spoken script**

We now build the two pipelines. Building a pipeline does not train it. It only describes the steps.

The function make_pipeline takes the steps in order. The first step is SimpleImputer with strategy set to the word median. It fills any missing input with the median of its column, and the median is taken from the training rows when we fit. The second step is LinearRegression, which fits the straight-line model.

We save the first pipeline as base_pipeline. Then we write the same recipe again and save it as extended_pipeline.

We need two pipelines because they will learn different things. One will see two input columns and the other will see three. The code that makes them is identical, and the difference arrives when we give each one its columns to fit.

## Slide 24: Paired ablation using the supplied CSV: step 2 (2/2)

base_feature_columns: input columns for the simpler comparison pipeline.

Run the cell and read the output below it.

```python
base_pipeline.fit(
    training_features[base_feature_columns],
    training_data["target"],
)
extended_pipeline.fit(
    training_features[extended_feature_columns],
    training_data["target"],
)
```

**Spoken script**

Training comes next. We train both pipelines. The method dot fit takes two inputs, a table of input columns and the matching known answers. It learns from them, and the rows of the two inputs must describe the same observations in the same order.

For the base pipeline we pass the training rows, restricted to base_feature_columns, and the training target column. For the extended pipeline we pass the training rows with extended_feature_columns, and the same target column.

So the only difference between the two calls is the list of columns. The answers are the same and the rows are the same.

The cell prints nothing. Each pipeline has now learned its medians and its line from training rows only. The validation rows have not been touched. We must call fit before predict, and the next cell uses predict.

## Slide 25: Compare errors on the same rows

Predict both alternatives on matching validation rows. mean_absolute_error compares each prediction with its observed target.

Base MAE minus extended MAE is positive when the extra feature helped on this validation set.

**Spoken script**

Next we test both pipelines on the validation rows.

The method dot predict takes input columns and returns one predicted value of crusher energy demand for every row, in kWh/t. We call it on each pipeline with its own columns, using the same validation rows for both.

Then mean_absolute_error compares each prediction with the observed target and averages the size of the misses. The answer is the MAE in kWh/t. Lower means the predictions are closer to the truth.

We get one MAE for the base pipeline and one for the extended pipeline. We subtract the extended MAE from the base MAE. If the result is positive, the extra feature helped on this validation set. If it is zero or negative, it did not.

## Slide 26: Paired ablation using the supplied CSV: step 3

base_feature_columns: input columns for the simpler comparison pipeline.

Run the cell and read the output below it.

```python
base_predictions = base_pipeline.predict(
    validation_features[base_feature_columns]
)
base_absolute_error = mean_absolute_error(
    validation_data["target"], base_predictions
)
```

**Spoken script**

This cell scores the base pipeline.

The first statement calls base_pipeline dot predict on the validation rows. We select only the base_feature_columns from validation_features, because that pipeline was trained on those columns and needs the same ones. The result is a predicted value of crusher energy demand for each validation row, saved as base_predictions.

The second statement calls mean_absolute_error. We give it the true targets from validation_data first and our predictions second. It compares them row by row and averages the size of the differences. We save the answer as base_absolute_error.

Nothing prints here. The value waits for the comparison in the next cell, and it is measured in kWh/t.

## Slide 27: Paired ablation using the supplied CSV: step 4

extended_predictions: validation predictions from the extended pipeline.

extended_absolute_error: validation mean absolute error for the extended pipeline.

**Spoken script**

Two new names appear in the next cell, and we should know what each one holds.

extended_predictions is the list of predicted values of crusher energy demand that the extended pipeline gives for the validation rows. It is the counterpart of base_predictions.

extended_absolute_error is the mean absolute error of those predictions, measured against the real validation targets. It is the counterpart of base_absolute_error.

With these two error values in hand we can compare the two models directly.

## Slide 28: Paired ablation using the supplied CSV: step 4 (1/2)

base_feature_columns: input columns for the simpler comparison pipeline.

Continue in the same code cell.

```python
extended_predictions = extended_pipeline.predict(
    validation_features[extended_feature_columns]
)
extended_absolute_error = mean_absolute_error(
    validation_data["target"], extended_predictions
)
```

**Spoken script**

This cell repeats the scoring for the extended pipeline.

We call extended_pipeline dot predict on the validation rows. Here we select extended_feature_columns, the three inputs, because this pipeline learned from three. We save the answers as extended_predictions.

Then mean_absolute_error compares the real validation targets with extended_predictions, and the average miss is saved as extended_absolute_error.

The cell continues on the next slide with the lines that print. Both errors come from the same validation rows and the same scoring function, so the comparison is fair. The only difference is the extra column the extended pipeline was allowed to use.

## Slide 29: Paired ablation using the supplied CSV: step 4 (2/2)

base_feature_columns: input columns for the simpler comparison pipeline.

Run the cell and read the output below it.

```python
print(
    round(base_absolute_error, 4),
    round(extended_absolute_error, 4),
)
print(round(base_absolute_error - extended_absolute_error, 4))
```

**Spoken script**

These last statements print the result.

The first print shows two numbers, the base error and then the extended error. Round with four decimal places keeps them short enough to read. Both numbers are in kWh/t, and the smaller one belongs to the better model.

The second print takes the base error minus the extended error. If this is positive, the extended model made smaller errors, so the feature helped on the validation rows. If it is negative, the feature made things worse. If it is close to zero, the two models are practically equal.

Before we decide to keep the feature, we ask how big the gain is compared with the size of the error, and whether it is large enough to matter in practice. Your own cohort's data produces its own numbers.

## Slide 30: A feature earns its place only if it helps

Base error 0.6732 kWh/t. With load × ambient 0.6740 kWh/t.

The extra feature changed the validation error by +0.0008 kWh/t. The error went up.
A derived feature inherits the blanks of the columns it is built from. One training row has a blank ambient temperature, so its product is blank and the imputer fills it with a typical value.
With only 15 validation rows the comparison is rough. A feature that adds a column and gives no clear gain should be dropped. Keep the simpler model.

**Spoken script**

Here is the honest result of the ablation on our own data. The base model, using load and ambient temperature, has a validation error of 0.6732 kWh/t. Adding the interaction, load times ambient, gives 0.6740. The change is +0.0008. The error went up, so the extra feature did not help.

Why might the new column struggle? A derived feature inherits the blanks of the columns it comes from. One training row has a blank ambient temperature, so its product is blank as well, and the imputer fills it with a typical product that has nothing to do with that row. We built the product before filling the blank, and the order matters.

We have only fifteen validation rows, so the comparison is rough, and a new feature also adds a column to maintain and one more thing that can go wrong. Our rule is that a feature earns its place only when the improvement is clear. Here it is not, so we keep the simpler model. That is a real engineering judgement, and it is the kind of reasoning that earns marks in your written evidence.

## Slide 31: Use only inputs you will have at prediction time

ALLOWED
Load now. Ambient temperature now. A value calculated from those two, such as load divided by 100.
Anything the sensor could report at the moment the prediction is requested.

LEAKS THE ANSWER
The measured target itself. A repair note written after the fault. A monthly average that includes next week.
A feature like these makes training look wonderful and fails in service.

**Spoken script**

One rule applies to every feature you build. You must have it at the moment the prediction is requested. Load now and ambient temperature now are fine. A value calculated from those two, such as load divided by one hundred, is fine too.

Be suspicious of anything that is known only afterwards: the measured target itself, a repair note written after a fault, or a monthly average that includes next week. These leak the answer. The model looks wonderful in training and fails in service. Last week's leakage guard number four is this rule.

## Slide 32: Your issued task

01

Investigate crusher energy demand.

02

Target units: kWh/t.

03

These are synthetic teaching records for practice.

04

Each record is one operating observation; equipment_id repeats across observations.

**Spoken script**

This slide states your task for this week. You are investigating crusher energy demand, and its unit is kWh/t. Say the target and the unit exactly as they appear on the slide.

Each row of the data is one operating observation. The equipment_id column repeats, because the same machine is observed many times. The record_id column is the identifier of each observation. The load_pct column is the load in percent, and ambient_c is the surrounding temperature in degrees Celsius. In the training rows the target holds the known answer.

These are synthetic teaching records, made up for learning. They are not measurements that could be used to operate real equipment, and the relationships we find in them are not calibrated physical laws.

## Slide 33: make_features(feature_records)

Return one feature row per input, in order: [load_pct, ambient_c, load_pct/100, load_pct*ambient_c].

Use inputs available at prediction time only.

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

Your first required function is called make_features, and it takes one input, feature_records. Use the exact function name.

For each record it must return one row of four numbers, in this order. First comes load_pct itself. Second comes ambient_c itself. Third comes load_pct divided by 100. Fourth comes load_pct multiplied by ambient_c.

The result holds one such row per input record, and the rows stay in the same order as the input.

Use only values that are available at the moment a prediction is requested. That means load and ambient temperature, and anything calculated from them. The target never goes into a feature.

Keep the exact names and the exact output order. Check the types and units against the task brief on your own issued task slide.

## Slide 34: ablation_metrics(training_records, validation_records)

Fit two sklearn LinearRegression models on the same training records: base features [load_pct, ambient_c] and extended features adding load_pct*ambient_c.

Evaluate both on the same validation records.

Return base_mae, extended_mae and improvement=base_mae-extended_mae, without rounding.

Inputs are complete; never fit on validation targets.

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

Your second required function is ablation_metrics. It receives training records and validation records.

Inside it you fit two scikit-learn LinearRegression models on the same training records. The base model uses load_pct and ambient_c. The extended model uses those two and also load_pct multiplied by ambient_c.

Then you evaluate both models on the same validation records, using mean absolute error.

The function returns three values, base_mae, extended_mae and improvement. The improvement is base_mae minus extended_mae. Do not round any of them, because the grader compares the exact values.

The inputs are complete, which means no values are missing, so you do not need an imputer here. And never fit on the validation targets. Validation rows are only for scoring the models.

Use the exact function name and the exact output names.

## Slide 35: Written evidence

01

Use the cell headed “My written evidence”.

02

Explain the supplied scenario in your own words.

03

State target units, reasons and limitations.

04

Submit one complete notebook containing code and written evidence.

**Spoken script**

Your notebook needs words as well as code. Find the cell headed My written evidence and write your answer there.

Explain the scenario we supplied in your own words. Say what the target is and give its unit, which is kWh/t. Then give your reasons for the choices you made, and state the limitations of what you found.

A good explanation links a decision to a result. For example, you might say why the imputer takes its medians from the training rows only, and what that protects you from.

The figures in the scenario came with it, so describe them as supplied and not as measurements you made yourself.

Submit one complete notebook that contains both your code and your written evidence. Copied prompts and code comments do not replace your own reasoning.

## Slide 36: Features and ablation submission

01

Opens: 20 Nov 2026, 08:00 Kampala

02

Deadline: 27 Nov 2026, 08:00 Kampala

03

Use your full Student Registration Number in the form.

04

Keep the submitted files and confirmation.

Open W11 assignment form

https://docs.google.com/forms/d/e/1FAIpQLSdxAosnTnoXrNZ7QCm8pPQuoa2KxsqFvu_PPsZIQGrJnHMw1g/viewform

**Spoken script**

This slide covers the submission of your Week 11 assignment. Read the opening time and the deadline on the slide, and check them again on the form itself before you submit.

The form asks for your full Student Registration Number. Type it exactly, because this is how we match your work to you.

The file to submit is one completed notebook, with the dot ipynb ending. When you upload it, wait until the filename appears on the form before pressing Submit.

A notebook saved only in Drive or GitHub has not been submitted. Only the form counts.

Keep the submitted file and the confirmation after you finish, as your evidence that you submitted.

## Slide 37: Project preparation

01

Use the published machine learning project brief.

02

Build the evidence gradually in your project notebook.

03

Keep raw data, labelled charts, run instructions and individual contributions.

04

Published deadline: 18 Dec 2026, 08:00 Kampala

**Spoken script**

Your machine learning project is built up gradually, and the work you do now goes into it.

Use the published project brief as your guide. Add evidence to your project notebook a little at a time, as you finish each part.

Keep four things. Keep the raw data, unchanged. Keep your charts, each with labels. Keep the run instructions, so someone else can run your notebook. And keep a record of each person's contribution, specific enough that it can be checked, such as a named file, function or chart and the decision behind it.

Check the project deadline on the slide. Working steadily now makes the final weeks much lighter.

## Slide 38: Words from today

**Spoken script**

Six words to keep. Feature engineering builds new inputs from existing columns. A derived feature is one column calculated from others. An interaction multiplies two inputs. The effect of one spread, which is the slope times the standard deviation, lets us compare inputs fairly. Ablation compares scores with and without one piece. And the prediction time rule says to use only inputs you will have when you predict. In the assignment you build the features and run the ablation yourself.

## Slide 39: Week 11 quiz

01

Answer individually after the lecturer activates the quiz.

02

Available for 24 hours from activation.

03

Use your Student Registration Number and registered account.

04

Check the announced quiz closing time.

Open this week’s quiz

https://forms.gle/3sf2d3vGXpJ4HtvP6

**Spoken script**

This slide is about the Week 11 quiz. You answer it on your own.

The quiz opens when the lecturer activates it, and from that moment it stays open for 24 hours. Check the closing time that is announced for your class.

When you fill in the form, use your Student Registration Number and your registered account. Using a different account can make your answers difficult to match to you.

The link on the slide opens the response form. The link alone does not start the 24 hours. That starts when the lecturer activates the quiz, so wait for that announcement and then answer.

## Slide 40: Revision and submission checklist

Explain to a classmate why load divided by 100 is a derived feature, how you would decide whether to keep a new feature, and why a repair note written after a fault cannot be an input.

Keep raw data unchanged. Restart and run all cells before submitting the required assignment notebook.

Point to your evidence. Save your work.

**Spoken script**

We finish with a check you do on your own. Pick a classmate, or imagine one, and explain three things out loud.

First, why load divided by 100 is a derived feature. Second, how you decide whether to keep a new feature. Third, why a repair note written after a fault cannot be used as an input.

If you can explain these three clearly, you understood the lesson. If you get stuck, go back to the slide where that idea appeared.

Before you submit, keep the raw data unchanged, then restart your notebook and run all cells from the top. If the notebook runs cleanly to the end, it is ready.

Point to your evidence, and save your work.
